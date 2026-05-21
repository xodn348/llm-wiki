"""Generate topic-cluster and lineage-chain wiki pages.

Phase-3 navigation aids on top of the per-paper pages produced by
:mod:`wiki_generator`.

- :func:`generate_topics` groups the Fleming-tier corpus by the highest-scoring
  top-level OpenAlex Concept on each paper (preferring level 0, falling back to
  level 1) and writes one page per cluster with an LLM 2-paragraph synthesis.
- :func:`generate_lineages` finds the longest paths in the ``enables`` subgraph
  of ``data/graph/edges.parquet`` and writes a narrative wiki page for each,
  grounding step-by-step prose in the existing edge labels.

Both helpers fall back to a structural-only page if the LLM backend errors so
the build never breaks on transient Codex stream issues.
"""
from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import Any

import networkx as nx
import polars as pl
import yaml

from .config import PATHS
from .llm_client import LLMClient, LLMError
from .storage import doi_slug, read_parquet

logger = logging.getLogger(__name__)

TOPIC_SYSTEM = (
    "You write encyclopedic wiki entries about clusters of Fleming-tier "
    "(paradigm-shifting) scientific papers. Be precise, neutral, and ground every "
    "claim in the supplied paper titles or in well-known historical context."
)

LINEAGE_SYSTEM = (
    "You narrate intellectual lineages between Fleming-tier scientific papers. "
    "Each step is a real 'enables' relationship with a one-sentence label. "
    "Stay grounded in the supplied titles and labels — do not invent results."
)

TOPIC_PLACEHOLDER = "_[Topic synthesis pending — LLM backend unavailable]_"
LINEAGE_PLACEHOLDER = "_[Step narrative pending — LLM backend unavailable]_"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(text: str) -> str:
    return _SLUG_RE.sub("-", text.lower()).strip("-")


# ---------------------------------------------------------------------------
# Topics
# ---------------------------------------------------------------------------


def _pick_top_concept(concepts: list[dict[str, Any]] | None) -> dict[str, Any] | None:
    """Return the highest-scoring level-0 concept, else highest level-1."""
    if not concepts:
        return None
    for level in (0, 1):
        ranked = sorted(
            (c for c in concepts if c.get("level") == level),
            key=lambda c: -(c.get("score") or 0.0),
        )
        if ranked:
            return ranked[0]
    return None


def _topic_synthesis_prompt(name: str, papers: list[dict[str, Any]]) -> str:
    bullets = "\n".join(
        f"- {p.get('year')}  {p.get('title')}" for p in papers[:60]
    )
    extra = f"\n(plus {len(papers) - 60} more)" if len(papers) > 60 else ""
    return (
        f"Write a 2-paragraph synthesis of what the Fleming-tier papers in the "
        f"topic '{name}' collectively represent. Highlight the dominant lineages, "
        f"the major paradigm shifts within this topic, and how it connects to "
        f"adjacent fields. Markdown only, no headers, ~180-260 words.\n\n"
        f"Papers in this cluster (sorted by year):\n{bullets}{extra}\n"
    )


def _topic_frontmatter(name: str, count: int, concept_id: str) -> str:
    fm = {"title": name, "papers": count, "top_concept_id": concept_id}
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"


def _write_topic_index(topics: list[tuple[str, int, str]]) -> None:
    """Auto-generated landing page listing all topic clusters."""
    topics_sorted = sorted(topics, key=lambda t: -t[1])
    lines = [
        "---",
        "title: Topics",
        "---",
        "",
        "# Topic clusters",
        "",
        "Fleming-tier papers grouped by their dominant OpenAlex top-level "
        "Concept (level 0, falling back to level 1). Each page links every "
        "paper in the cluster and includes an LLM-written synthesis of what "
        "the cluster represents.",
        "",
        f"_{len(topics_sorted)} clusters, sorted by paper count._",
        "",
    ]
    for name, count, slug in topics_sorted:
        lines.append(f"- [{name}]({slug}.md) — {count} papers")
    lines.append("")
    (PATHS.docs_topic / "index.md").write_text("\n".join(lines), encoding="utf-8")


def generate_topics(min_papers: int = 5, with_llm: bool = True) -> int:
    """Group papers by top OpenAlex Concept and write one page per cluster.

    Args:
        min_papers: minimum cluster size to emit a page.
        with_llm: if False (or if the backend errors), use a placeholder synthesis.

    Returns:
        Number of topic pages written (excluding the index).
    """
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    if metadata.is_empty():
        raise RuntimeError("No metadata. Run earlier stages first.")

    buckets: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"papers": [], "concept_id": None}
    )
    for row in metadata.iter_rows(named=True):
        top = _pick_top_concept(row.get("concepts"))
        if not top:
            continue
        name = top["name"]
        buckets[name]["papers"].append(row)
        buckets[name]["concept_id"] = top["id"]

    llm: LLMClient | None = None
    if with_llm:
        try:
            llm = LLMClient()
        except LLMError as e:  # pragma: no cover - depends on env
            logger.warning("LLM unavailable, writing structural-only topics: %s", e)
            llm = None

    written: list[tuple[str, int, str]] = []
    for name, bucket in sorted(buckets.items(), key=lambda kv: -len(kv[1]["papers"])):
        papers = sorted(bucket["papers"], key=lambda p: (p.get("year") or 0))
        if len(papers) < min_papers:
            continue
        slug = _slugify(name)
        out = PATHS.docs_topic / f"{slug}.md"

        synthesis = TOPIC_PLACEHOLDER
        if llm is not None:
            try:
                synthesis = llm.text(
                    _topic_synthesis_prompt(name, papers),
                    system=TOPIC_SYSTEM,
                    max_tokens=900,
                ).strip() or TOPIC_PLACEHOLDER
            except Exception as e:  # noqa: BLE001 - any backend failure → fallback
                logger.warning("topic LLM failed for %r: %s", name, e)
                synthesis = TOPIC_PLACEHOLDER

        body_lines = [
            _topic_frontmatter(name, len(papers), bucket["concept_id"]),
            f"# {name}",
            "",
            f"_{len(papers)} Fleming-tier papers._",
            "",
            "## Synthesis",
            "",
            synthesis,
            "",
            "## Papers",
            "",
        ]
        for p in papers:
            doi = p.get("doi")
            if not doi:
                continue
            title = p.get("title") or doi
            year = p.get("year") or "?"
            body_lines.append(
                f"- {year} — [{title}](../paper/{doi_slug(doi)}.md)"
            )
        body_lines.append("")
        out.write_text("\n".join(body_lines), encoding="utf-8")
        written.append((name, len(papers), slug))
        logger.info("topic: %s (%d papers) -> %s", name, len(papers), out.name)

    _write_topic_index(written)
    logger.info("wrote %d topic pages", len(written))
    return len(written)


# ---------------------------------------------------------------------------
# Lineages
# ---------------------------------------------------------------------------


def _enables_dag(edges: pl.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    sub = edges.filter(pl.col("type") == "enables")
    for r in sub.iter_rows(named=True):
        G.add_edge(r["src_doi"], r["tgt_doi"], label=r.get("label") or "")
    return G


def _longest_chains(G: nx.DiGraph, min_length: int, max_pages: int) -> list[list[str]]:
    """Return up to ``max_pages`` longest distinct paths in ``G`` with >=min_length nodes."""
    if not nx.is_directed_acyclic_graph(G):
        raise RuntimeError("enables subgraph is not a DAG; expected forward-in-time edges")
    sources = [n for n in G if G.in_degree(n) == 0]
    sinks = [n for n in G if G.out_degree(n) == 0]
    chains: list[list[str]] = []
    for s in sources:
        for t in sinks:
            for path in nx.all_simple_paths(G, s, t):
                if len(path) >= min_length:
                    chains.append(path)
    # Deduplicate (just in case) and sort longest first; tie-break by first DOI for determinism.
    seen: set[tuple[str, ...]] = set()
    unique: list[list[str]] = []
    for p in sorted(chains, key=lambda p: (-len(p), p[0])):
        key = tuple(p)
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
        if len(unique) >= max_pages:
            break
    return unique


def _lineage_title(papers: list[dict[str, Any]]) -> str:
    chunks = []
    for p in papers:
        year = p.get("year") or "?"
        title = (p.get("title") or "untitled").strip()
        # Short label: first 6 words
        short = " ".join(title.split()[:6])
        chunks.append(f"{year} {short}")
    return " → ".join(chunks)


def _lineage_step_prompt(
    src: dict[str, Any], tgt: dict[str, Any], label: str
) -> str:
    return (
        f"Write 1-2 short paragraphs (~100-160 words total) explaining how "
        f"'{src.get('title')}' ({src.get('year')}) enabled "
        f"'{tgt.get('title')}' ({tgt.get('year')}). The recorded edge label is:\n"
        f"  \"{label}\"\n"
        f"Stay grounded in that label and well-known historical context. "
        f"Do not invent specific quantitative results. Markdown only, no headers."
    )


def _lineage_frontmatter(title: str, length_edges: int, start_doi: str, end_doi: str) -> str:
    fm = {
        "title": title,
        "length": length_edges,
        "start_doi": start_doi,
        "end_doi": end_doi,
    }
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"


def _write_lineage_index(entries: list[tuple[str, int, str]]) -> None:
    """Auto-generated landing page listing all lineage chains."""
    lines = [
        "---",
        "title: Lineages",
        "---",
        "",
        "# Enables lineages",
        "",
        "Longest paths through the ``enables`` subgraph of the paper-level "
        "citation network. Each page walks the chain step by step, grounding "
        "every transition in the recorded edge label.",
        "",
        f"_{len(entries)} lineages, sorted by chain length._",
        "",
    ]
    for title, length, slug in entries:
        lines.append(f"- [{title}]({slug}.md) — {length} steps")
    lines.append("")
    (PATHS.docs_lineage / "index.md").write_text("\n".join(lines), encoding="utf-8")


def generate_lineages(
    min_length: int = 3, max_pages: int = 10, with_llm: bool = True
) -> int:
    """Find longest paths in the enables-subgraph and emit one page per chain.

    Args:
        min_length: minimum number of papers (nodes) in a chain.
        max_pages: cap on number of lineage pages emitted.
        with_llm: if False (or if backend errors), step prose falls back to a placeholder.

    Returns:
        Number of lineage pages written (excluding the index).
    """
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    edges = read_parquet(PATHS.edges)
    if metadata.is_empty() or edges.is_empty():
        raise RuntimeError("Need metadata + edges. Run earlier stages first.")
    by_doi = {r["doi"]: r for r in metadata.iter_rows(named=True)}

    G = _enables_dag(edges)
    chains = _longest_chains(G, min_length=min_length, max_pages=max_pages)
    if not chains:
        logger.warning("no enables-chains of length >= %d found", min_length)
        _write_lineage_index([])
        return 0

    llm: LLMClient | None = None
    if with_llm:
        try:
            llm = LLMClient()
        except LLMError as e:  # pragma: no cover - depends on env
            logger.warning("LLM unavailable, writing structural-only lineages: %s", e)
            llm = None

    written: list[tuple[str, int, str]] = []
    used_slugs: set[str] = set()
    for chain in chains:
        papers = [by_doi.get(d) for d in chain]
        if any(p is None for p in papers):
            logger.debug("skipping chain with missing paper metadata: %s", chain)
            continue
        title = _lineage_title(papers)
        # Build a slug that is unique per chain — many chains share a long
        # prefix when truncated, so anchor on first+last DOI plus length.
        base = _slugify(title)[:90] or _slugify(chain[0])
        slug = f"{base}-{doi_slug(chain[0])[:12]}-{doi_slug(chain[-1])[:12]}-{len(chain)}"
        if slug in used_slugs:
            slug = f"{slug}-{len(used_slugs)}"
        used_slugs.add(slug)
        out = PATHS.docs_lineage / f"{slug}.md"

        body = [
            _lineage_frontmatter(title, len(chain) - 1, chain[0], chain[-1]),
            f"# {title}",
            "",
            f"_{len(chain)} papers, {len(chain) - 1} `enables` steps._",
            "",
            "## Chain",
            "",
        ]
        for p in papers:
            doi = p["doi"]
            body.append(
                f"1. **{p.get('year')}** — [{p.get('title')}](../paper/{doi_slug(doi)}.md)"
            )
        body.append("")
        body.append("## Walkthrough")
        body.append("")

        for src_p, tgt_p in zip(papers[:-1], papers[1:]):
            edge_label = G[src_p["doi"]][tgt_p["doi"]].get("label", "")
            body.append(
                f"### {src_p.get('year')} → {tgt_p.get('year')}: "
                f"[{src_p.get('title')}](../paper/{doi_slug(src_p['doi'])}.md) "
                f"enables [{tgt_p.get('title')}](../paper/{doi_slug(tgt_p['doi'])}.md)"
            )
            body.append("")
            body.append(f"> {edge_label}" if edge_label else "> _(no edge label)_")
            body.append("")
            prose = LINEAGE_PLACEHOLDER
            if llm is not None:
                try:
                    prose = llm.text(
                        _lineage_step_prompt(src_p, tgt_p, edge_label),
                        system=LINEAGE_SYSTEM,
                        max_tokens=500,
                    ).strip() or LINEAGE_PLACEHOLDER
                except Exception as e:  # noqa: BLE001
                    logger.warning(
                        "lineage LLM failed for %s -> %s: %s",
                        src_p["doi"], tgt_p["doi"], e,
                    )
                    prose = LINEAGE_PLACEHOLDER
            body.append(prose)
            body.append("")

        out.write_text("\n".join(body), encoding="utf-8")
        written.append((title, len(chain) - 1, slug))
        logger.info("lineage: %s (%d steps) -> %s", title[:60], len(chain) - 1, out.name)

    _write_lineage_index(written)
    logger.info("wrote %d lineage pages", len(written))
    return len(written)


__all__ = ["generate_topics", "generate_lineages"]
