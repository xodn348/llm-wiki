"""Multi-source OA fetcher — finds full text beyond Unpaywall.

Unpaywall's index misses ~75 % of paywalled papers. This module tries
three additional public sources in priority order, all free, all legit:

1. **Semantic Scholar Academic Graph API** — Allen AI's index. Returns
   ``openAccessPdf.url`` for many papers Unpaywall doesn't catch
   (preprints, author-uploaded copies on .edu pages).
2. **Internet Archive Scholar** — fatcat.wiki / scholar.archive.org
   indexes preprints, repository copies, and arxiv/biorxiv mirrors.
3. **CORE** — UK-based OA aggregator, 200M+ papers. Free API tier
   without a key gives lower rate limits but works for occasional use.

For each DOI we already failed on (Unpaywall ``no_open_url`` /
``failed``), try each in order, save the first PDF that comes back.

This is the *legitimate-only* path. It does NOT touch ResearchGate,
Sci-Hub, or any other gray/illegal source.
"""
from __future__ import annotations

import logging
import os
import time
from pathlib import Path

import httpx
import polars as pl

from .config import ENV, PATHS
from .storage import doi_slug

logger = logging.getLogger(__name__)

S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"
IA_SCHOLAR_BASE = "https://scholar.archive.org/search"
CORE_BASE = "https://api.core.ac.uk/v3/search/outputs"


def _client() -> httpx.Client:
    return httpx.Client(
        timeout=30.0,
        headers={"User-Agent": ENV.user_agent},
        follow_redirects=True,
    )


# --- Source 1: Semantic Scholar -----------------------------------------


def _s2_pdf_url(doi: str, c: httpx.Client) -> str | None:
    """Hit S2 Academic Graph and return openAccessPdf.url if present."""
    try:
        r = c.get(
            f"{S2_BASE}/DOI:{doi}",
            params={"fields": "openAccessPdf,externalIds"},
        )
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        logger.debug("s2 %s failed: %s", doi, e)
        return None
    pdf = data.get("openAccessPdf") or {}
    return pdf.get("url")


# --- Source 2: Internet Archive Scholar ---------------------------------

# scholar.archive.org search returns JSON with hits containing
# `fulltext.access_url` for indexed PDFs.

def _ia_scholar_pdf_url(doi: str, c: httpx.Client) -> str | None:
    try:
        r = c.get(
            IA_SCHOLAR_BASE,
            params={"q": f'doi:"{doi}"', "format": "json"},
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        logger.debug("ia_scholar %s failed: %s", doi, e)
        return None
    for hit in data.get("results", []):
        full = hit.get("fulltext") or {}
        url = full.get("access_url")
        if url:
            return url
    return None


# --- Source 3: CORE -----------------------------------------------------


def _core_pdf_url(doi: str, c: httpx.Client) -> str | None:
    """Search CORE for the DOI; return downloadUrl of the first hit."""
    headers = {}
    core_key = os.getenv("CORE_API_KEY")
    if core_key:
        headers["Authorization"] = f"Bearer {core_key}"
    try:
        r = c.post(
            CORE_BASE,
            json={"q": f'doi:"{doi}"', "limit": 1},
            headers=headers,
        )
        if r.status_code == 429:
            logger.debug("core %s rate-limited", doi)
            return None
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        logger.debug("core %s failed: %s", doi, e)
        return None
    for hit in data.get("results", []):
        url = hit.get("downloadUrl")
        if url:
            return url
    return None


# --- Orchestrator -------------------------------------------------------


def _save_pdf(url: str, dest: Path, c: httpx.Client) -> int:
    """Download URL → write to dest if response is PDF. Return bytes written."""
    try:
        r = c.get(url)
        r.raise_for_status()
    except Exception as e:  # noqa: BLE001
        logger.debug("download %s failed: %s", url, e)
        return 0
    ctype = (r.headers.get("content-type") or "").lower()
    if "pdf" not in ctype and not url.lower().endswith(".pdf"):
        # Some servers serve PDFs as octet-stream — check magic bytes
        if not r.content.startswith(b"%PDF"):
            return 0
    dest.write_bytes(r.content)
    return len(r.content)


def fetch_oa_multi(
    *,
    max_papers: int | None = None,
    rate_delay: float = 1.0,
    skip_existing: bool = True,
    sources: tuple[str, ...] = ("s2", "ia", "core"),
) -> pl.DataFrame:
    """For every DOI without a local PDF, try S2 → IA Scholar → CORE.

    Honors a 1-second rate delay between papers by default. Each public
    API has its own per-IP rate limit; 1 req/sec is comfortably under
    all three.

    Updates ``data/raw/fetch_status.parquet`` with new methods:
    ``s2_pdf``, ``ia_pdf``, ``core_pdf``, or ``oa_multi_miss``.
    """
    status = pl.read_parquet(PATHS.raw / "fetch_status.parquet")
    missing = status.filter(
        pl.col("method").is_in(["no_open_url", "failed", "tamu_failed",
                                "tamu_landing_only", "tamu_error",
                                "tamu_pdf_link_not_pdf"])
    )
    metadata = pl.read_parquet(PATHS.metadata).select(["doi", "title", "year"])
    todo = missing.join(metadata, on="doi", how="left").to_dicts()
    if max_papers is not None:
        todo = todo[:max_papers]

    logger.info("oa-multi: %d candidate DOIs to try across sources %s",
                len(todo), sources)

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

            if skip_existing and pdf_path.exists() and pdf_path.stat().st_size > 1024:
                out.append({"doi": doi, "method": "cached",
                            "pdf_bytes": pdf_path.stat().st_size})
                continue

            new_method = "oa_multi_miss"
            new_bytes = 0
            for src in sources:
                resolver = {"s2": _s2_pdf_url, "ia": _ia_scholar_pdf_url,
                            "core": _core_pdf_url}[src]
                url = resolver(doi, c)
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

    # Merge into canonical fetch_status
    out_df = pl.from_dicts(out)
    updated = set(out_df["doi"].to_list())
    keep = status.filter(~pl.col("doi").is_in(list(updated)))
    common = [c for c in status.columns if c in out_df.columns]
    merged = pl.concat(
        [keep.select(common), out_df.select(common)], how="diagonal_relaxed"
    )
    merged.write_parquet(PATHS.raw / "fetch_status.parquet")

    summary = out_df.group_by("method").len().sort("len", descending=True)
    logger.info("oa-multi summary:\n%s", summary)
    return out_df
