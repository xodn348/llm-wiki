"""Fetch the actual paper content for each core DOI.

Strategy: open-access first via OpenAlex's `best_oa_location.pdf_url`;
fall back to Unpaywall (free, no key) for OA discovery; final fallback is
to leave a stub note so manual upload is possible.
"""
from __future__ import annotations

import logging
import time

import httpx
import polars as pl

from .config import ENV, PATHS
from .storage import doi_slug, read_parquet, write_parquet

logger = logging.getLogger(__name__)

UNPAYWALL = "https://api.unpaywall.org/v2"


def _client() -> httpx.Client:
    return httpx.Client(
        timeout=60.0,
        headers={"User-Agent": ENV.user_agent},
        follow_redirects=True,
    )


def _open_url_for(doi: str, c: httpx.Client) -> str | None:
    try:
        r = c.get(f"{UNPAYWALL}/{doi}", params={"email": ENV.openalex_email})
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        logger.debug("unpaywall %s failed: %s", doi, e)
        return None
    best = data.get("best_oa_location") or {}
    return best.get("url_for_pdf") or best.get("url")


def fetch(rate_delay: float = 0.5) -> pl.DataFrame:
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    if metadata.is_empty():
        raise RuntimeError("No metadata. Run `llm-wiki enrich` first.")
    dois = [d for d in metadata["doi"].drop_nulls().to_list() if d]
    logger.info("fetching %d papers", len(dois))

    statuses: list[dict] = []
    with _client() as c:
        for i, doi in enumerate(dois, 1):
            slug = doi_slug(doi)
            paper_dir = PATHS.papers / slug
            paper_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = paper_dir / "full.pdf"
            html_path = paper_dir / "landing.html"
            status: dict = {"doi": doi, "slug": slug, "method": None,
                            "pdf_bytes": 0, "html_bytes": 0}

            if pdf_path.exists() and pdf_path.stat().st_size > 1024:
                status["method"] = "cached"
                status["pdf_bytes"] = pdf_path.stat().st_size
                statuses.append(status)
                continue

            url = _open_url_for(doi, c)
            if url:
                try:
                    rr = c.get(url)
                    rr.raise_for_status()
                    ctype = (rr.headers.get("content-type") or "").lower()
                    if "pdf" in ctype or url.lower().endswith(".pdf"):
                        pdf_path.write_bytes(rr.content)
                        status["method"] = "oa_pdf"
                        status["pdf_bytes"] = len(rr.content)
                    else:
                        html_path.write_bytes(rr.content)
                        status["method"] = "oa_html"
                        status["html_bytes"] = len(rr.content)
                except Exception as e:  # noqa: BLE001
                    logger.debug("download %s failed: %s", url, e)
                    status["method"] = "failed"
            else:
                status["method"] = "no_open_url"

            statuses.append(status)
            if i % 25 == 0:
                logger.info("fetched %d / %d", i, len(dois))
            time.sleep(rate_delay)

    df = pl.from_dicts(statuses)
    write_parquet(df, PATHS.raw / "fetch_status.parquet")
    summary = df.group_by("method").len()
    logger.info("fetch summary:\n%s", summary)
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    fetch()
