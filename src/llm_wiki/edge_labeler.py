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
    all_rows = edges.to_dicts()
    labeled = [r for r in all_rows if r.get("label")]
    to_label = [r for r in all_rows if not r.get("label")]
    if max_edges:
        to_label = to_label[:max_edges]
    logger.info("edges: %d total, %d already labeled, %d to label",
                len(all_rows), len(labeled), len(to_label))

    if not to_label:
        return edges

    llm = LLMClient()

    out: list[dict[str, Any]] = list(labeled)
    rows = to_label
    save_every = max(1, 200 // batch)  # checkpoint roughly every 200 edges
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

        batch_idx = start // batch
        if batch_idx % save_every == save_every - 1:
            _checkpoint(out, all_rows, start + len(chunk), len(rows))

    df = pl.from_dicts(out + [r for r in all_rows if r not in labeled and r["src_doi"] is None])
    # Combine: prior labeled + newly labeled + any rows we never touched (limit case)
    written = {(r["src_doi"], r["tgt_doi"], r["type"]) for r in out}
    untouched = [r for r in all_rows if (r["src_doi"], r["tgt_doi"], r["type"]) not in written]
    df = pl.from_dicts(out + untouched)
    write_parquet(df, PATHS.edges)
    logger.info("labeled %d edges (total rows in file: %d)", len(out) - len(labeled), len(df))
    return df


def _checkpoint(out: list[dict[str, Any]], all_rows: list[dict[str, Any]], done: int, total: int) -> None:
    written = {(r["src_doi"], r["tgt_doi"], r["type"]) for r in out}
    untouched = [r for r in all_rows if (r["src_doi"], r["tgt_doi"], r["type"]) not in written]
    df = pl.from_dicts(out + untouched)
    write_parquet(df, PATHS.edges)
    logger.info("checkpoint: %d/%d edges labeled", done, total)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    label_all()
