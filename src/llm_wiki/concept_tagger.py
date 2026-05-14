"""Tag every leaf with concepts.

For each paper, we already have OpenAlex Concepts in metadata. This
module materialises a (leaf_id → concept_id[]) table by inheriting the
paper's concepts to all its leaves. v1 can refine per-leaf with LLM.
"""
from __future__ import annotations

import logging
from typing import Any

import polars as pl

from .config import PATHS
from .storage import read_parquet, write_parquet

logger = logging.getLogger(__name__)


def tag_all() -> pl.DataFrame:
    PATHS.ensure()
    nodes = read_parquet(PATHS.nodes)
    metadata = read_parquet(PATHS.metadata)
    if nodes.is_empty() or metadata.is_empty():
        raise RuntimeError("Need both nodes and metadata. Run earlier stages first.")

    # Build (doi → concept_ids) lookup
    concepts_by_doi: dict[str, list[dict[str, Any]]] = {}
    for r in metadata.iter_rows(named=True):
        concepts_by_doi[r["doi"]] = r.get("concepts") or []

    rows: list[dict[str, Any]] = []
    for n in nodes.iter_rows(named=True):
        for cn in concepts_by_doi.get(n["doi"], []):
            rows.append(
                {
                    "doi": n["doi"],
                    "node_id": n["node_id"],
                    "concept_id": cn.get("id"),
                    "concept_name": cn.get("name"),
                    "concept_level": cn.get("level"),
                    "concept_score": cn.get("score"),
                }
            )

    df = pl.from_dicts(rows) if rows else pl.DataFrame()
    write_parquet(df, PATHS.graph / "tags.parquet")
    logger.info("tagged: %d (leaf, concept) pairs", len(rows))
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    tag_all()
