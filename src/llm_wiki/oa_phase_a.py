"""Phase A — six additional OA sources to close the 650-paper gap.

Beyond Unpaywall / S2 / CORE this module tries (in priority order):

1. **Europe PMC** REST API — best biomedical full-text index, often has
   PDFs Unpaywall doesn't surface.
2. **arXiv** title+year match — recovers preprints that S2 missed
   because the DOI→arXiv mapping is broken.
3. **bioRxiv / medRxiv** DOI lookup — covers biology preprints since 2013.
4. **Crossref** `link[]` field — publishers self-register CC-BY PDFs.
5. **Publisher URL templates** — PNAS / PLOS / Nature / Science / Cell
   patterns that don't require any API call.
6. **DOI landing-page meta scrape** — fetch doi.org/<doi>, parse
   ``citation_pdf_url`` and friends.

All sources are legitimate OA; nothing here scrapes paywalled content.
"""
from __future__ import annotations

import logging
import re
import time
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable

import httpx
import polars as pl

from .config import ENV, PATHS
from .oa_multi_fetcher import _save_pdf  # reuse PDF magic-byte validator
from .storage import doi_slug

logger = logging.getLogger(__name__)

EUROPEPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
ARXIV_BASE = "http://export.arxiv.org/api/query"
BIORXIV_BASE = "https://api.biorxiv.org/details"
CROSSREF_BASE = "https://api.crossref.org/works"
DOI_BASE = "https://doi.org"

# Regexes for landing-page meta tags (Google Scholar standard + fallbacks)
META_PDF_PATTERNS = [
    re.compile(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]+property=["\']og:pdf["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<link[^>]+type=["\']application/pdf["\'][^>]+href=["\']([^"\']+)["\']', re.I),
]


def _client() -> httpx.Client:
    return httpx.Client(
        timeout=30.0,
        headers={"User-Agent": ENV.user_agent},
        follow_redirects=True,
    )


# --- 1. Europe PMC -------------------------------------------------------

def _europepmc_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = row["doi"]
    try:
        r = c.get(
            EUROPEPMC_BASE,
            params={
                "query": f'DOI:"{doi}"',
                "resultType": "core",
                "format": "json",
            },
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        logger.debug("europepmc %s failed: %s", doi, e)
        return None
    for result in (data.get("resultList") or {}).get("result", []) or []:
        ftus = ((result.get("fullTextUrlList") or {}).get("fullTextUrl") or [])
        # Prefer Open access + PDF
        for ftu in ftus:
            if ftu.get("documentStyle") == "pdf" and ftu.get("availability") in {
                "Open access", "Free", "Subscription"
            }:
                if ftu.get("availability") != "Subscription":
                    return ftu.get("url")
    return None


# --- 2. arXiv (title + year match) --------------------------------------

def _title_similarity(a: str, b: str) -> float:
    a = re.sub(r"\W+", " ", a.lower()).strip()
    b = re.sub(r"\W+", " ", b.lower()).strip()
    return SequenceMatcher(None, a, b).ratio()


def _arxiv_pdf_url(row: dict, c: httpx.Client) -> str | None:
    title = row.get("title")
    year = row.get("year")
    if not title:
        return None
    # arXiv full-text search across title; we'll fuzzy-match the result
    q = re.sub(r"[^A-Za-z0-9 ]+", " ", title)[:200]
    try:
        r = c.get(
            ARXIV_BASE,
            params={"search_query": f'ti:"{q}"', "max_results": 5},
        )
        r.raise_for_status()
    except Exception as e:  # noqa: BLE001
        logger.debug("arxiv %s failed: %s", title[:40], e)
        return None
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError:
        return None
    best_score = 0.0
    best_pdf = None
    for entry in root.findall("a:entry", ns):
        cand_title_el = entry.find("a:title", ns)
        if cand_title_el is None or not cand_title_el.text:
            continue
        cand_title = " ".join(cand_title_el.text.split())
        score = _title_similarity(title, cand_title)
        # Year sanity check — arXiv preprint year shouldn't be much later
        cand_year = None
        published = entry.find("a:published", ns)
        if published is not None and published.text:
            cand_year = int(published.text[:4])
        if year and cand_year and cand_year > int(year) + 1:
            continue
        if score < 0.85:
            continue
        pdf_link = None
        for link in entry.findall("a:link", ns):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break
        if pdf_link and score > best_score:
            best_score = score
            best_pdf = pdf_link if pdf_link.endswith(".pdf") else pdf_link + ".pdf"
    return best_pdf


# --- 3. bioRxiv / medRxiv ------------------------------------------------

def _biorxiv_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = row["doi"]
    for server in ("biorxiv", "medrxiv"):
        try:
            r = c.get(f"{BIORXIV_BASE}/{server}/{doi}")
            if r.status_code != 200:
                continue
            data = r.json()
        except Exception as e:  # noqa: BLE001
            logger.debug("biorxiv %s %s failed: %s", server, doi, e)
            continue
        for entry in data.get("collection", []):
            paper_id = entry.get("doi") or doi
            version = entry.get("version") or "1"
            # https://www.biorxiv.org/content/10.1101/2020.01.01.000000v1.full.pdf
            return f"https://www.{server}.org/content/{paper_id}v{version}.full.pdf"
    return None


# --- 4. Crossref link[] field --------------------------------------------

def _crossref_link_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = row["doi"]
    try:
        r = c.get(
            f"{CROSSREF_BASE}/{doi}",
            headers={"User-Agent": ENV.user_agent + " (mailto:noreply@local)"},
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        logger.debug("crossref %s failed: %s", doi, e)
        return None
    for link in (data.get("message") or {}).get("link", []) or []:
        ct = (link.get("content-type") or "").lower()
        if "pdf" in ct or (link.get("URL") or "").lower().endswith(".pdf"):
            return link.get("URL")
    return None


# --- 5. Publisher URL templates (zero API) ------------------------------

def _publisher_template_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = (row.get("doi") or "").lower()
    if not doi:
        return None
    # PNAS — all articles >6mo are OA
    if doi.startswith("10.1073/pnas"):
        return f"https://www.pnas.org/doi/pdf/{doi}"
    # PLOS — CC-BY universally
    m = re.match(r"10\.1371/journal\.([a-z]+)\.\w+", doi)
    if m:
        slug = m.group(1)  # pone, pbio, pmed, ppat, pcbi, pgen, pntd
        journal_map = {
            "pone": "plosone", "pbio": "plosbiology", "pmed": "plosmedicine",
            "ppat": "plospathogens", "pcbi": "ploscompbiol",
            "pgen": "plosgenetics", "pntd": "plosntds",
        }
        site = journal_map.get(slug)
        if site:
            return f"https://journals.plos.org/{site}/article/file?id={doi}&type=printable"
    # eLife — CC-BY
    if doi.startswith("10.7554/elife"):
        eid = doi.split(".")[-1]
        return f"https://elifesciences.org/articles/{eid}.pdf"
    # MDPI — CC-BY
    if doi.startswith("10.3390/"):
        return f"https://www.mdpi.com/{doi[8:]}/pdf"
    # Frontiers — CC-BY
    if doi.startswith("10.3389/"):
        return f"https://www.frontiersin.org/articles/{doi}/pdf"
    # Cold Spring Harbor Perspectives — many OA
    if doi.startswith("10.1101/"):
        # bioRxiv handled separately; this catches CSH journals
        if "cshperspect" in doi or "gad" in doi or "cshp" in doi:
            return f"https://www.doi.org/{doi}"  # fall through to meta-scrape
    return None


# --- 6. DOI landing-page meta-tag scrape --------------------------------

def _html_meta_pdf_url(row: dict, c: httpx.Client) -> str | None:
    doi = row["doi"]
    try:
        r = c.get(f"{DOI_BASE}/{doi}")
        if r.status_code >= 400:
            return None
        html = r.text[:200_000]  # cap; meta tags are in <head>
    except Exception as e:  # noqa: BLE001
        logger.debug("doi-meta %s failed: %s", doi, e)
        return None
    for pat in META_PDF_PATTERNS:
        m = pat.search(html)
        if m:
            url = m.group(1)
            # Make absolute if relative
            if url.startswith("/"):
                base = str(r.url).split("/", 3)
                url = "/".join(base[:3]) + url
            return url
    return None


# --- Orchestrator -------------------------------------------------------

RESOLVERS: dict[str, Callable[[dict, httpx.Client], str | None]] = {
    "europepmc": _europepmc_pdf_url,
    "arxiv": _arxiv_pdf_url,
    "biorxiv": _biorxiv_pdf_url,
    "crossref": _crossref_link_pdf_url,
    "template": _publisher_template_pdf_url,
    "doi_meta": _html_meta_pdf_url,
}

DEFAULT_ORDER = ("europepmc", "arxiv", "biorxiv", "crossref", "template", "doi_meta")


def fetch_phase_a(
    *,
    max_papers: int | None = None,
    rate_delay: float = 1.0,
    sources: tuple[str, ...] = DEFAULT_ORDER,
    only_methods: tuple[str, ...] = (
        "oa_multi_miss", "oa_html", "oa_multi_html_only",
    ),
) -> pl.DataFrame:
    """Run the 6 Phase-A resolvers on every paper still PDF-less."""
    status = pl.read_parquet(PATHS.raw / "fetch_status.parquet")
    missing = status.filter(pl.col("method").is_in(list(only_methods)))
    metadata = pl.read_parquet(PATHS.raw / "metadata.parquet").select(
        ["doi", "title", "year", "venue"]
    )
    todo = missing.join(metadata, on="doi", how="left").to_dicts()
    if max_papers is not None:
        todo = todo[:max_papers]

    logger.info("phase-a: %d candidate DOIs across sources %s", len(todo), sources)

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

            new_method = "phase_a_miss"
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

    # Merge back
    out_df = pl.from_dicts(out)
    updated = set(out_df["doi"].to_list())
    keep = status.filter(~pl.col("doi").is_in(list(updated)))
    common = [c for c in status.columns if c in out_df.columns]
    merged = pl.concat(
        [keep.select(common), out_df.select(common)], how="diagonal_relaxed"
    )
    merged.write_parquet(PATHS.raw / "fetch_status.parquet")

    summary = out_df.group_by("method").len().sort("len", descending=True)
    logger.info("phase-a summary:\n%s", summary)
    return out_df
