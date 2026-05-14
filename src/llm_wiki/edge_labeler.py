"""LLM 'why related' labels for each edge."""
from __future__ import annotations

import logging
from typing import Any

import polars as pl

from .config import PATHS
from .llm_client import LLMClient
from .storage import read_parquet, write_parquet

logger = logging.getLogger(__name__)


SYSTEM = (
    "You explain relationships between scientific papers in one short sentence. "
    "Be concrete: name the specific concept, method, or claim that links them."
)


def label_all(*, batch: int = 20, max_edges: int | None = None) -> pl.DataFrame:
    edges = read_parquet(PATHS.edges)
    metadata = read_parquet(PATHS.metadata)
    if edges.is_empty():
        raise RuntimeError("No edges. Run `llm-wiki graph` first.")
    by_doi = {r["doi"]: r for r in metadata.iter_rows(named=True)}
    rows = edges.to_dicts()
    if max_edges:
        rows = rows[:max_edges]

    llm = LLMClient()

    out: list[dict[str, Any]] = []
    for start in range(0, len(rows), batch):
        chunk = rows[start : start + batch]
        prompt_lines = [
            "For each edge, output a JSON array of objects "
            '{"id": <input id>, "label": "<one sentence>"}.'
        ]
        for i, e in enumerate(chunk):
            src = by_doi.get(e["src_doi"], {})
            tgt = by_doi.get(e["tgt_doi"], {})
            prompt_lines.append(
                f"{i}. type={e['type']} | "
                f"src={src.get('title') or e['src_doi']} ({src.get('year')}) | "
                f"tgt={tgt.get('title') or e['tgt_doi']} ({tgt.get('year')})"
            )
        try:
            verdict = llm.json("\n".join(prompt_lines), system=SYSTEM, max_tokens=2048)
        except Exception as e:  # noqa: BLE001
            logger.warning("label batch %d crashed: %s", start, e)
            for r in chunk:
                out.append(dict(r, label=None))
            continue
        by_id = {int(v.get("id", -1)): v.get("label") for v in verdict if isinstance(v, dict)}
        for i, r in enumerate(chunk):
            out.append(dict(r, label=by_id.get(i)))

    df = pl.from_dicts(out)
    write_parquet(df, PATHS.edges)  # overwrite with labels
    logger.info("labeled %d edges", len(out))
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    label_all()
