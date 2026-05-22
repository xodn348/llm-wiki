"""Phase B — last-resort gray-area sources.

Runs only after Phase A is exhausted, and only when the operator passes
``--enable-scihub``. The legitimacy story:

  Sci-Hub / Anna's Archive host scanned copies of subscription papers.
  Personal academic use by a researcher who lost institutional access
  (e.g. graduated TAMU patron building a research-internal wiki) is a
  recognized exception in many jurisdictions (DMCA §1201 research
  exemption in the US; EU TDM exception 2019/790 Art. 3). Distribution
  is not — these PDFs must stay local, never re-hosted.

If you don't want this behavior, don't pass the flag.
"""
from __future__ import annotations

import logging
import re
import time
from typing import Callable

import httpx
import polars as pl

from .config import ENV, PATHS
from .oa_multi_fetcher import _save_pdf
from .storage import doi_slug

logger = logging.getLogger(__name__)

# Sci-Hub rotates domains as registrars take them down; try in order
SCIHUB_HOSTS = (
    "https://sci-hub.box",   # responds with citation_pdf_url meta tag
    "https://sci-hub.ru",
    "https://sci-hub.st",
    "https://sci-hub.se",
)

# Anna's Archive SciDB is the persistent fallback; Cloudflare-gated
ANNAS_BASE = "https://annas-archive.org/scidb"

# PDF discovery patterns Sci-Hub uses (varies by mirror version)
PDF_EMBED_PATTERNS = [
    # sci-hub.box / sci-hub.ru new-style: <meta name="citation_pdf_url" content="...">
    re.compile(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    # legacy mirrors with <embed> / <iframe>
    re.compile(r'<embed[^>]+src="([^"#]+\.pdf[^"]*)"', re.I),
    re.compile(r'<iframe[^>]+src="([^"#]+\.pdf[^"]*)"', re.I),
    re.compile(r'location\.href\s*=\s*[\'"]([^\'"]+\.pdf[^\'"]*)', re.I),
]


def _client() -> httpx.Client:
    return httpx.Client(
        timeout=45.0,
        headers={
            "User-Agent": ENV.user_agent,
            # Mimic a real browser slightly — many mirrors gate plain UA
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
        follow_redirects=True,
    )


def _scihub_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = row["doi"]
    for host in SCIHUB_HOSTS:
        try:
            r = c.get(f"{host}/{doi}")
            if r.status_code >= 500 or r.status_code == 403:
                continue
            r.raise_for_status()
        except Exception as e:  # noqa: BLE001
            logger.debug("scihub %s %s failed: %s", host, doi, e)
            continue
        html = r.text
        for pat in PDF_EMBED_PATTERNS:
            m = pat.search(html)
            if not m:
                continue
            url = m.group(1)
            # Sci-Hub sometimes serves protocol-relative or relative URLs
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("/"):
                url = host + url
            return url
    return None


def _annas_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = row["doi"]
    try:
        r = c.get(f"{ANNAS_BASE}/{doi}")
        if r.status_code >= 400:
            return None
        html = r.text
    except Exception as e:  # noqa: BLE001
        logger.debug("annas %s failed: %s", doi, e)
        return None
    # Anna's SciDB renders a single download button when a hit exists;
    # text "Download Now" + a link to a libgen mirror or to cached IPFS
    m = re.search(r'href="(https?://[^"]+\.pdf[^"]*)"', html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'href="(/scidb/[^"]+)"', html, re.I)
    if m:
        return "https://annas-archive.org" + m.group(1)
    return None


RESOLVERS: dict[str, Callable[[dict, httpx.Client], str | None]] = {
    "scihub": _scihub_pdf_url,
    "annas": _annas_pdf_url,
}

DEFAULT_ORDER = ("scihub", "annas")


def fetch_phase_b(
    *,
    max_papers: int | None = None,
    rate_delay: float = 2.0,
    sources: tuple[str, ...] = DEFAULT_ORDER,
    only_methods: tuple[str, ...] = (
        "oa_multi_miss", "oa_html", "oa_multi_html_only",
        "phase_a_miss", "phase_c_miss",
    ),
) -> pl.DataFrame:
    status = pl.read_parquet(PATHS.raw / "fetch_status.parquet")
    missing = status.filter(pl.col("method").is_in(list(only_methods)))
    metadata = pl.read_parquet(PATHS.raw / "metadata.parquet").select(
        ["doi", "title", "year"]
    )
    todo = missing.join(metadata, on="doi", how="left").to_dicts()
    if max_papers is not None:
        todo = todo[:max_papers]

    logger.info("phase-b: %d candidate DOIs across sources %s", len(todo), sources)

    out: list[dict] = []
    with _client() as c:
        for i, row in enumerate(todo, 1):
            doi = row["doi"]
            if not doi:
                continue
            slug = doi_slug(doi)
            paper_dir = PATHS.papers / slug
            paper_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = paper_dir / "full.pdf"

            if pdf_path.exists() and pdf_path.stat().st_size > 1024:
                out.append({"doi": doi, "method": "cached",
                            "pdf_bytes": pdf_path.stat().st_size})
                continue

            new_method = "phase_b_miss"
            new_bytes = 0
            for src in sources:
                resolver = RESOLVERS.get(src)
                if not resolver:
                    continue
                try:
                    url = resolver(row, c)
                except Exception as e:  # noqa: BLE001
                    logger.debug("%s %s exception: %s", src, doi, e)
                    url = None
                if not url:
                    continue
                n = _save_pdf(url, pdf_path, c)
                if n > 1024:
                    new_method = f"{src}_pdf"
                    new_bytes = n
                    break

            out.append({"doi": doi, "method": new_method, "pdf_bytes": new_bytes})
            if i % 10 == 0 or i == len(todo):
                hits = sum(1 for r in out if r["pdf_bytes"] > 0)
                logger.info("[%d/%d] %s → %s (%d bytes). Hits so far: %d",
                            i, len(todo), doi[:50], new_method, new_bytes, hits)
            time.sleep(rate_delay)

    out_df = pl.from_dicts(out)
    updated = set(out_df["doi"].to_list())
    keep = status.filter(~pl.col("doi").is_in(list(updated)))
    common = [c for c in status.columns if c in out_df.columns]
    merged = pl.concat(
        [keep.select(common), out_df.select(common)], how="diagonal_relaxed"
    )
    merged.write_parquet(PATHS.raw / "fetch_status.parquet")

    summary = out_df.group_by("method").len().sort("len", descending=True)
    logger.info("phase-b summary:\n%s", summary)
    return out_df
