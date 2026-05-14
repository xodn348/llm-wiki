"""Generate wiki markdown pages from metadata + edges + LLM 'why mattered' text."""
from __future__ import annotations

import logging
import yaml
from typing import Any

import polars as pl

from .config import PATHS
from .llm_client import LLMClient
from .storage import doi_slug, read_parquet

logger = logging.getLogger(__name__)


WHY_SYSTEM = (
    "You write encyclopedic wiki entries about Fleming-tier (paradigm-shifting) "
    "scientific papers. Be precise, neutral, ground every claim in the paper or "
    "well-known historical context."
)


def _why_prompt(meta: dict[str, Any]) -> str:
    return (
        f"Write a 2–3 paragraph 'Why this mattered' section for the paper:\n\n"
        f"Title: {meta.get('title')}\n"
        f"Authors: {meta.get('authors')}\n"
        f"Year: {meta.get('year')}\n"
        f"Venue: {meta.get('venue')}\n"
        f"Citations: {meta.get('citations')}\n\n"
        f"Abstract: {meta.get('abstract') or '(no abstract available)'}\n\n"
        f"Focus on the paradigm shift, what was newly possible after this paper, "
        f"and how it relates to subsequent breakthroughs. Markdown only, no headers."
    )


def _frontmatter(meta: dict[str, Any]) -> str:
    fm = {
        "title": meta.get("title"),
        "doi": meta.get("doi"),
        "openalex_id": meta.get("openalex_id"),
        "year": meta.get("year"),
        "venue": meta.get("venue"),
        "authors": meta.get("authors"),
        "citations": meta.get("citations"),
        "fleming_tier": True,
        "concepts": [c.get("name") for c in (meta.get("concepts") or [])][:10],
    }
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"


def _edges_for(doi: str, edges: pl.DataFrame, by_doi: dict[str, dict]) -> str:
    if edges.is_empty():
        return ""
    out = ["\n## Related\n"]
    for r in edges.filter(pl.col("src_doi") == doi).iter_rows(named=True):
        tgt = by_doi.get(r["tgt_doi"])
        if not tgt:
            continue
        slug = doi_slug(r["tgt_doi"])
        title = tgt.get("title") or r["tgt_doi"]
        label = r.get("label") or ""
        out.append(f"- **{r['type']}** → [{title}]({slug}.md) — {label}")
    for r in edges.filter(pl.col("tgt_doi") == doi).iter_rows(named=True):
        src = by_doi.get(r["src_doi"])
        if not src:
            continue
        slug = doi_slug(r["src_doi"])
        title = src.get("title") or r["src_doi"]
        label = r.get("label") or ""
        out.append(f"- **{r['type']}** ← [{title}]({slug}.md) — {label}")
    return "\n".join(out) + "\n"


def generate(*, max_papers: int | None = None, with_llm: bool = True) -> int:
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    edges = read_parquet(PATHS.edges)
    if metadata.is_empty():
        raise RuntimeError("No metadata. Run earlier stages first.")
    by_doi = {r["doi"]: r for r in metadata.iter_rows(named=True)}
    rows = list(metadata.iter_rows(named=True))
    if max_papers:
        rows = rows[:max_papers]

    llm = LLMClient() if with_llm else None
    written = 0
    for r in rows:
        doi = r["doi"]
        if not doi:
            continue
        slug = doi_slug(doi)
        out = PATHS.docs_paper / f"{slug}.md"

        why = ""
        if llm is not None:
            try:
                why = llm.text(_why_prompt(r), system=WHY_SYSTEM, max_tokens=900)
            except Exception as e:  # noqa: BLE001
                logger.warning("why-prompt failed for %s: %s", doi, e)
                why = ""

        body = "\n".join(
            [
                _frontmatter(r),
                f"# {r.get('title')}",
                "",
                "## Why this mattered",
                "",
                why or "_TBD_",
                "",
                "## Abstract",
                "",
                r.get("abstract") or "_(no abstract available)_",
                "",
                _edges_for(doi, edges, by_doi),
                "",
                "## Sources",
                "",
                f"- DOI: [https://doi.org/{doi}](https://doi.org/{doi})",
                f"- OpenAlex: [{r.get('openalex_id')}]({r.get('openalex_id')})"
                if r.get("openalex_id") else "",
            ]
        )
        out.write_text(body, encoding="utf-8")
        written += 1
    logger.info("wrote %d paper pages", written)
    return written


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    generate()
