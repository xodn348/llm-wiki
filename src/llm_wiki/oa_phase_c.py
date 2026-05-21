"""Phase C — async, batched, faster.

Replaces sequential Phase A. Three big wins:

1. **Crossref bulk** — one `?filter=doi:A,B,C,...` query returns up to
   50 papers' ``link[]`` fields at once. We fetch all CC-BY-registered
   PDFs in seconds, not 500 seconds.
2. **Concurrent fanout** — for each remaining paper, fire Europe PMC /
   OpenAIRE / DOI-meta in parallel and take the first hit.
3. **OpenAIRE Explore** — new source: EU-funded research aggregator
   (covers institutional repositories Unpaywall misses).

Drops arXiv (rate-limit unworkable) and bioRxiv (low yield).
"""
from __future__ import annotations

import asyncio
import logging
import re

import httpx
import polars as pl

from .config import ENV, PATHS
from .storage import doi_slug

logger = logging.getLogger(__name__)

EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OPENAIRE = "https://api.openaire.eu/search/publications"
CROSSREF = "https://api.crossref.org/works"
OSTI = "https://www.osti.gov/api/v1/records"

META_PATTERNS = [
    re.compile(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]+property=["\']og:pdf["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<link[^>]+type=["\']application/pdf["\'][^>]+href=["\']([^"\']+)["\']', re.I),
]


# --- Helpers ------------------------------------------------------------

def _publisher_template(doi: str) -> str | None:
    """Pure URL construction; no API call."""
    d = doi.lower()
    if d.startswith("10.1073/pnas"):
        return f"https://www.pnas.org/doi/pdf/{d}"
    m = re.match(r"10\.1371/journal\.([a-z]+)\.\w+", d)
    if m:
        slug = m.group(1)
        journal_map = {
            "pone": "plosone", "pbio": "plosbiology", "pmed": "plosmedicine",
            "ppat": "plospathogens", "pcbi": "ploscompbiol",
            "pgen": "plosgenetics", "pntd": "plosntds",
        }
        site = journal_map.get(slug)
        if site:
            return f"https://journals.plos.org/{site}/article/file?id={d}&type=printable"
    if d.startswith("10.7554/elife"):
        return f"https://elifesciences.org/articles/{d.split('.')[-1]}.pdf"
    if d.startswith("10.3390/"):
        return f"https://www.mdpi.com/{d[8:]}/pdf"
    if d.startswith("10.3389/"):
        return f"https://www.frontiersin.org/articles/{d}/pdf"
    return None


async def _save_pdf_async(url: str, dest, client: httpx.AsyncClient) -> int:
    try:
        r = await client.get(url)
        r.raise_for_status()
    except Exception:
        return 0
    ct = (r.headers.get("content-type") or "").lower()
    if "pdf" not in ct and not url.lower().endswith(".pdf"):
        if not r.content.startswith(b"%PDF"):
            return 0
    if not r.content.startswith(b"%PDF"):
        return 0
    dest.write_bytes(r.content)
    return len(r.content)


# --- Stage 0: Crossref bulk pre-fetch -----------------------------------

async def _crossref_bulk(dois: list[str], client: httpx.AsyncClient) -> dict[str, str]:
    """Returns {doi_lower: pdf_url} for any DOIs Crossref has link[] PDFs for."""
    found: dict[str, str] = {}
    chunk_size = 50
    sem = asyncio.Semaphore(5)

    async def _one_chunk(chunk: list[str]) -> None:
        async with sem:
            q = ",".join(f"doi:{d}" for d in chunk)
            try:
                r = await client.get(CROSSREF, params={"filter": q, "rows": chunk_size})
                if r.status_code != 200:
                    return
                items = r.json().get("message", {}).get("items", [])
            except Exception as e:  # noqa: BLE001
                logger.debug("crossref chunk failed: %s", e)
                return
            for item in items:
                d = (item.get("DOI") or "").lower()
                for link in item.get("link", []) or []:
                    ct = (link.get("content-type") or "").lower()
                    url = link.get("URL") or ""
                    if "pdf" in ct or url.lower().endswith(".pdf"):
                        found[d] = url
                        break

    chunks = [dois[i : i + chunk_size] for i in range(0, len(dois), chunk_size)]
    await asyncio.gather(*(_one_chunk(c) for c in chunks))
    return found


# --- Per-paper resolvers (async) ----------------------------------------

async def _europepmc(doi: str, client: httpx.AsyncClient) -> str | None:
    try:
        r = await client.get(
            EUROPEPMC,
            params={"query": f'DOI:"{doi}"', "resultType": "core", "format": "json"},
        )
        if r.status_code != 200:
            return None
        data = r.json()
    except Exception:
        return None
    for result in (data.get("resultList") or {}).get("result", []) or []:
        for ftu in ((result.get("fullTextUrlList") or {}).get("fullTextUrl") or []):
            if ftu.get("documentStyle") != "pdf":
                continue
            if ftu.get("availability") in {"Open access", "Free"}:
                return ftu.get("url")
    return None


async def _openaire(doi: str, client: httpx.AsyncClient) -> str | None:
    try:
        r = await client.get(OPENAIRE, params={"doi": doi, "format": "json"})
        if r.status_code != 200:
            return None
        data = r.json()
    except Exception:
        return None
    results = ((data.get("response") or {}).get("results") or {}).get("result", []) or []
    for result in results:
        entity = ((result.get("metadata") or {}).get("oaf:entity") or {})
        oaf_result = entity.get("oaf:result", {}) or {}
        children = oaf_result.get("children", {}) or {}
        instances = children.get("instance", []) or []
        if not isinstance(instances, list):
            instances = [instances]
        for inst in instances:
            access = ((inst.get("accessright") or {}).get("@classid") or "").upper()
            if access != "OPEN":
                continue
            urls = inst.get("webresource", []) or []
            if not isinstance(urls, list):
                urls = [urls]
            for u in urls:
                url = u.get("url") if isinstance(u, dict) else None
                if url and (".pdf" in url.lower() or "openaccess" in url.lower()):
                    return url
            if urls:
                first = urls[0]
                if isinstance(first, dict) and first.get("url"):
                    return first["url"]
    return None


async def _doi_meta(doi: str, client: httpx.AsyncClient) -> str | None:
    try:
        r = await client.get(f"https://doi.org/{doi}")
        if r.status_code >= 400:
            return None
        html = r.text[:200_000]
    except Exception:
        return None
    for pat in META_PATTERNS:
        m = pat.search(html)
        if m:
            url = m.group(1)
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("/"):
                base = str(r.url).split("/", 3)
                url = "/".join(base[:3]) + url
            return url
    return None


async def _osti(doi: str, client: httpx.AsyncClient) -> str | None:
    try:
        r = await client.get(OSTI, params={"q": f'doi:"{doi}"', "rows": 1})
        if r.status_code != 200:
            return None
        data = r.json()
    except Exception:
        return None
    records = data if isinstance(data, list) else data.get("records") or []
    for rec in records:
        for link in rec.get("links", []) or []:
            href = link.get("href") or ""
            rel = (link.get("rel") or "").lower()
            if "fulltext" in rel or href.lower().endswith(".pdf"):
                if href.startswith("/"):
                    href = "https://www.osti.gov" + href
                return href
    return None


# --- Orchestrator -------------------------------------------------------

async def _process_one(
    row: dict,
    crossref_bulk: dict[str, str],
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
) -> dict:
    async with sem:
        doi = row["doi"]
        slug = doi_slug(doi)
        paper_dir = PATHS.papers / slug
        paper_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = paper_dir / "full.pdf"

        # already on disk (recovered from prior runs)
        if pdf_path.exists() and pdf_path.stat().st_size > 1024:
            with pdf_path.open("rb") as f:
                if f.read(5).startswith(b"%PDF"):
                    return {"doi": doi, "method": "cached",
                            "pdf_bytes": pdf_path.stat().st_size}

        # 1. Crossref bulk hit?
        url = crossref_bulk.get(doi.lower())
        if url:
            n = await _save_pdf_async(url, pdf_path, client)
            if n > 1024:
                return {"doi": doi, "method": "crossref_pdf", "pdf_bytes": n}

        # 2. Publisher template (no API)
        url = _publisher_template(doi)
        if url:
            n = await _save_pdf_async(url, pdf_path, client)
            if n > 1024:
                return {"doi": doi, "method": "template_pdf", "pdf_bytes": n}

        # 3. Fire 4 sources concurrently
        tasks = {
            "europepmc": _europepmc(doi, client),
            "openaire": _openaire(doi, client),
            "osti": _osti(doi, client),
            "doi_meta": _doi_meta(doi, client),
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        for name, res in zip(tasks.keys(), results):
            if isinstance(res, str) and res:
                n = await _save_pdf_async(res, pdf_path, client)
                if n > 1024:
                    return {"doi": doi, "method": f"{name}_pdf", "pdf_bytes": n}
        return {"doi": doi, "method": "phase_c_miss", "pdf_bytes": 0}


async def _run_async(concurrency: int = 20, max_papers: int | None = None) -> pl.DataFrame:
    status = pl.read_parquet(PATHS.raw / "fetch_status.parquet")
    pdf_methods = {"oa_pdf", "s2_pdf", "core_pdf", "europepmc_pdf",
                   "crossref_pdf", "doi_meta_pdf", "template_pdf",
                   "openaire_pdf", "osti_pdf"}
    missing = status.filter(~pl.col("method").is_in(list(pdf_methods)))
    metadata = pl.read_parquet(PATHS.raw / "metadata.parquet").select(
        ["doi", "title", "year"]
    )
    todo = missing.join(metadata, on="doi", how="left").to_dicts()
    todo = [r for r in todo if r.get("doi")]
    if max_papers is not None:
        todo = todo[:max_papers]

    logger.info("phase-c: %d candidate DOIs, concurrency=%d", len(todo), concurrency)

    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency)
    timeout = httpx.Timeout(30.0, connect=10.0)
    headers = {"User-Agent": ENV.user_agent + " (mailto:noreply@local)"}

    async with httpx.AsyncClient(
        limits=limits, timeout=timeout, headers=headers, follow_redirects=True
    ) as client:
        # Stage 0: Crossref bulk
        logger.info("crossref bulk pre-fetch for %d DOIs...", len(todo))
        cr_bulk = await _crossref_bulk([r["doi"] for r in todo], client)
        logger.info("crossref bulk → %d link-PDF candidates", len(cr_bulk))

        # Stage 1: per-paper fanout
        sem = asyncio.Semaphore(concurrency)
        out: list[dict] = []
        chunk_size = 50
        for i in range(0, len(todo), chunk_size):
            chunk = todo[i : i + chunk_size]
            chunk_results = await asyncio.gather(
                *(_process_one(r, cr_bulk, client, sem) for r in chunk),
                return_exceptions=False,
            )
            out.extend(chunk_results)
            hits = sum(1 for r in out if r["pdf_bytes"] > 0)
            logger.info("[%d/%d] Hits so far: %d", len(out), len(todo), hits)
            # Checkpoint fetch_status every 50 papers
            _checkpoint(status, out)

    out_df = pl.from_dicts(out)
    summary = out_df.group_by("method").len().sort("len", descending=True)
    logger.info("phase-c summary:\n%s", summary)
    return out_df


def _checkpoint(status: pl.DataFrame, out: list[dict]) -> None:
    if not out:
        return
    out_df = pl.from_dicts(out)
    updated = set(out_df["doi"].to_list())
    keep = status.filter(~pl.col("doi").is_in(list(updated)))
    common = [c for c in status.columns if c in out_df.columns]
    merged = pl.concat(
        [keep.select(common), out_df.select(common)], how="diagonal_relaxed"
    )
    merged.write_parquet(PATHS.raw / "fetch_status.parquet")


def fetch_phase_c(*, max_papers: int | None = None, concurrency: int = 20) -> pl.DataFrame:
    return asyncio.run(_run_async(concurrency=concurrency, max_papers=max_papers))
