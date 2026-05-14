"""OpenAlex bulk metadata enrichment for confirmed core papers."""
from __future__ import annotations

import logging
import time
from typing import Any

import httpx
import polars as pl

from .config import ENV, PATHS
from .storage import normalize_doi, read_parquet, write_parquet

logger = logging.getLogger(__name__)

OA_BASE = "https://api.openalex.org/works"
SELECT_FIELDS = (
    "id,doi,title,display_name,publication_year,publication_date,"
    "cited_by_count,is_retracted,authorships,primary_location,"
    "abstract_inverted_index,concepts,referenced_works,type,language"
)


def _client() -> httpx.Client:
    return httpx.Client(
        timeout=30.0,
        headers={"User-Agent": ENV.user_agent},
        follow_redirects=True,
        params={"mailto": ENV.openalex_email},
    )


def _abstract_from_inverted(idx: dict[str, list[int]] | None) -> str | None:
    if not idx:
        return None
    pos: list[tuple[int, str]] = []
    for word, positions in idx.items():
        for p in positions:
            pos.append((p, word))
    pos.sort()
    return " ".join(w for _, w in pos)


def _enrich_one(c: httpx.Client, doi: str) -> dict[str, Any] | None:
    try:
        r = c.get(f"{OA_BASE}/https://doi.org/{doi}", params={"select": SELECT_FIELDS})
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        logger.warning("OpenAlex %s -> %d", doi, e.response.status_code)
        return None
    except Exception as e:  # noqa: BLE001
        logger.warning("OpenAlex %s failed: %s", doi, e)
        return None


def _to_row(w: dict[str, Any]) -> dict[str, Any]:
    doi = normalize_doi((w.get("doi") or "").replace("https://doi.org/", "") or None)
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
    authors = ", ".join(
        a.get("author", {}).get("display_name") or "?"
        for a in (w.get("authorships") or [])[:8]
    )
    concepts = [
        {"id": cn.get("id"), "name": cn.get("display_name"), "level": cn.get("level"),
         "score": cn.get("score")}
        for cn in (w.get("concepts") or [])
    ]
    return {
        "doi": doi,
        "openalex_id": w.get("id"),
        "title": w.get("display_name") or w.get("title"),
        "year": w.get("publication_year"),
        "publication_date": w.get("publication_date"),
        "citations": w.get("cited_by_count", 0),
        "venue": venue,
        "authors": authors,
        "abstract": _abstract_from_inverted(w.get("abstract_inverted_index")),
        "concepts": concepts,
        "referenced_works": w.get("referenced_works") or [],
        "type": w.get("type"),
        "language": w.get("language"),
        "is_retracted": w.get("is_retracted", False),
    }


def enrich(rate_delay: float = 0.15) -> pl.DataFrame:
    PATHS.ensure()
    core = read_parquet(PATHS.core)
    if core.is_empty():
        raise RuntimeError("No core. Run `llm-wiki filter` first.")
    dois = [d for d in core["doi"].drop_nulls().to_list() if d]
    logger.info("enriching %d DOIs from OpenAlex", len(dois))

    rows: list[dict[str, Any]] = []
    with _client() as c:
        for i, doi in enumerate(dois, 1):
            w = _enrich_one(c, doi)
            if w:
                rows.append(_to_row(w))
            if i % 50 == 0:
                logger.info("enriched %d / %d", i, len(dois))
            time.sleep(rate_delay)

    df = pl.from_dicts(rows)
    write_parquet(df, PATHS.metadata)
    logger.info("metadata written: %d rows (of %d requested)", len(rows), len(dois))
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    enrich()
