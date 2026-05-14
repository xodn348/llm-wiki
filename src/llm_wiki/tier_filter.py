"""LLM filter: candidates → Fleming-tier core."""
from __future__ import annotations

import logging
from typing import Any

import polars as pl

from .config import PATHS
from .llm_client import LLMClient
from .storage import read_parquet, write_parquet

logger = logging.getLogger(__name__)

SYSTEM = (
    "You are a meticulous historian of science. For each paper, decide whether "
    "it is Fleming-tier — i.e. a paper that:\n"
    "  (a) founded a new field, OR\n"
    "  (b) caused a paradigm shift, OR\n"
    "  (c) directly enabled subsequent breakthroughs, OR\n"
    "  (d) is universally taught as foundational.\n"
    "Reject: high-citation but incremental; review-only; methods refinement; "
    "popular but not transformative; survey/textbook chapters."
)


def _batch_prompt(batch: list[dict[str, Any]]) -> str:
    lines = [
        "Classify each of the following papers. Output a JSON array of "
        "objects with the same length and order as the input, each shaped "
        '{"id": <input id>, "tier": "fleming" | "reject", "reason": "<one sentence>"}. '
        "Be strict: when in doubt, reject."
    ]
    for i, c in enumerate(batch):
        title = c.get("title") or "(no title)"
        year = c.get("year") or "?"
        venue = c.get("venue") or ""
        cites = c.get("citations") or 0
        lines.append(
            f"{i}. {title} | year={year} | venue={venue} | citations={cites}"
        )
    return "\n".join(lines)


def filter_heuristic(*, citation_floor: int = 5000, drop_no_doi: bool = True) -> pl.DataFrame:
    """LLM-free fallback. Accept curated-list rows + high-cite OpenAlex rows."""
    candidates = read_parquet(PATHS.candidates)
    if candidates.is_empty():
        raise RuntimeError("No candidates. Run `llm-wiki seed` first.")
    df = candidates
    # awesome_ml is hand-curated → always keep
    curated = df.filter(pl.col("source_tag").str.contains("awesome_ml"))
    # OpenAlex rows passing the citation floor
    if "citations" in df.columns:
        oa = df.filter(
            pl.col("source_tag").str.contains("openalex")
            & (pl.col("citations").fill_null(0) >= citation_floor)
        )
    else:
        oa = pl.DataFrame()
    out = pl.concat([curated, oa], how="diagonal_relaxed").unique(subset=["doi"])
    if drop_no_doi:
        out = out.filter(pl.col("doi").is_not_null())
    out = out.with_columns(
        pl.lit("fleming").alias("tier"),
        pl.lit("heuristic: curated-list OR OpenAlex citations >= floor").alias("reason"),
    )
    write_parquet(out, PATHS.core)
    logger.info("heuristic filter: %d papers accepted (no LLM)", len(out))
    return out


def filter_candidates(*, batch_size: int = 25, limit: int | None = None) -> pl.DataFrame:
    candidates = read_parquet(PATHS.candidates)
    if candidates.is_empty():
        raise RuntimeError(
            "No candidates. Run `llm-wiki seed` first."
        )
    if limit:
        candidates = candidates.head(limit)

    llm = LLMClient()
    rows = candidates.to_dicts()
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        prompt = _batch_prompt(batch)
        try:
            verdict = llm.json(prompt, system=SYSTEM, max_tokens=2048)
        except Exception as e:  # noqa: BLE001
            logger.warning("batch %d-%d failed: %s — keeping all as candidates",
                           start, start + len(batch), e)
            accepted.extend(batch)
            continue
        if not isinstance(verdict, list):
            logger.warning("batch %d returned non-list verdict; keeping all", start)
            accepted.extend(batch)
            continue
        by_id = {int(v.get("id", -1)): v for v in verdict if isinstance(v, dict)}
        for i, c in enumerate(batch):
            v = by_id.get(i, {})
            tier = (v.get("tier") or "").lower()
            reason = v.get("reason") or ""
            row = dict(c, tier=tier, reason=reason)
            (accepted if tier == "fleming" else rejected).append(row)
        logger.info(
            "batch %d–%d: accepted %d / %d",
            start, start + len(batch),
            sum(1 for c in batch if by_id.get(rows.index(c) - start, {}).get("tier") == "fleming"),
            len(batch),
        )

    core_df = pl.from_dicts(accepted) if accepted else pl.DataFrame()
    write_parquet(core_df, PATHS.core)
    rej_df = pl.from_dicts(rejected) if rejected else pl.DataFrame()
    if not rej_df.is_empty():
        write_parquet(rej_df, PATHS.raw / "rejected.parquet")
    logger.info(
        "filter complete: accepted=%d rejected=%d", len(accepted), len(rejected)
    )
    return core_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    filter_candidates()
