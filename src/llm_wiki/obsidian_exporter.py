"""Export the wiki as an Obsidian vault for interactive graph browsing.

Output layout::

    obsidian-vault/
    ├── README.md                ← landing page with vault usage
    ├── papers/<slug>.md         ← one note per Fleming-tier paper
    └── concepts/<slug>.md       ← hub note per OpenAlex concept that
                                   appears in >= MIN_CONCEPT_PAPERS papers

Each paper note uses ``[[wikilinks]]`` for related papers and concept
mentions so Obsidian's graph view shows them as edges. Concept notes
are minimal — Obsidian's "Linked mentions" panel turns them into
auto-aggregating hubs.

Open the resulting folder as a vault: ``Obsidian → Open folder as vault → obsidian-vault``.
"""
from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import Any

import polars as pl
import yaml

from .config import PATHS
from .storage import doi_slug, read_parquet

logger = logging.getLogger(__name__)

VAULT_DIR = PATHS.root / "obsidian-vault"
PAPERS_DIR = VAULT_DIR / "papers"
CONCEPTS_DIR = VAULT_DIR / "concepts"

MIN_CONCEPT_PAPERS = 3
TOP_CONCEPTS_PER_PAPER = 5


def _concept_slug(name: str) -> str:
    """Filesystem-safe slug for a concept name."""
    s = re.sub(r"[^\w\s-]", "", name).strip().lower()
    return re.sub(r"[\s_]+", "-", s)


def _frontmatter(meta: dict[str, Any], concept_names: list[str]) -> str:
    fm = {
        "title": meta.get("title"),
        "doi": meta.get("doi"),
        "year": meta.get("year"),
        "venue": meta.get("venue"),
        "authors": meta.get("authors"),
        "citations": meta.get("citations"),
        "openalex_id": meta.get("openalex_id"),
        "tags": [_concept_slug(n) for n in concept_names],
    }
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"


def _related_section(
    doi: str,
    edges: pl.DataFrame,
    by_doi: dict[str, dict[str, Any]],
) -> str:
    """Return a markdown 'Related' section using ``[[wikilinks]]``."""
    out_links: list[str] = []
    in_links: list[str] = []

    for r in edges.filter(pl.col("src_doi") == doi).iter_rows(named=True):
        tgt = by_doi.get(r["tgt_doi"])
        if not tgt or not tgt.get("doi"):
            continue
        slug = doi_slug(tgt["doi"])
        title = (tgt.get("title") or tgt["doi"]).replace("[", "(").replace("]", ")")
        label = (r.get("label") or "").strip()
        out_links.append(f"- **{r['type']}** → [[{slug}|{title}]]" + (f" — {label}" if label else ""))

    for r in edges.filter(pl.col("tgt_doi") == doi).iter_rows(named=True):
        src = by_doi.get(r["src_doi"])
        if not src or not src.get("doi"):
            continue
        slug = doi_slug(src["doi"])
        title = (src.get("title") or src["doi"]).replace("[", "(").replace("]", ")")
        label = (r.get("label") or "").strip()
        in_links.append(f"- **{r['type']}** ← [[{slug}|{title}]]" + (f" — {label}" if label else ""))

    if not out_links and not in_links:
        return ""
    parts = ["\n## Related\n"]
    if out_links:
        parts.append("\n### Outgoing")
        parts.extend(out_links)
    if in_links:
        parts.append("\n### Incoming")
        parts.extend(in_links)
    return "\n".join(parts) + "\n"


def _concept_section(concepts: list[dict[str, Any]]) -> str:
    """Render concept mentions so Obsidian links papers to concept hubs."""
    if not concepts:
        return ""
    lines = ["\n## Concepts\n"]
    for c in concepts[:TOP_CONCEPTS_PER_PAPER]:
        name = c.get("name")
        if not name:
            continue
        slug = _concept_slug(name)
        score = c.get("score") or 0
        lines.append(f"- [[{slug}|{name}]] ({score:.2f})")
    return "\n".join(lines) + "\n"


def _readme(paper_count: int, concept_count: int, edge_count: int) -> str:
    return f"""# llm-wiki Obsidian Vault

Open this folder as an Obsidian vault — `Obsidian → Open folder as vault → obsidian-vault/`.

## What's in here

- **{paper_count} paper notes** under `papers/` — one per Fleming-tier paper
- **{concept_count} concept hub notes** under `concepts/` — every OpenAlex concept appearing in ≥ {MIN_CONCEPT_PAPERS} papers
- **{edge_count} edges** rendered as `[[wikilinks]]` in each paper's *Related* section

## How to use the graph

1. Open the graph view (`Cmd/Ctrl + G`).
2. Group by tag for color-by-field (Computer science, Biology, Physics, …).
3. Filter to one concept (e.g. `tag:#computer-science`) to slice down.
4. Hover an edge to see the LLM-written "why related" label.

## Regenerating

```
uv run llm-wiki obsidian
```

Re-runs are idempotent and reuse existing notes' frontmatter.
"""


def export() -> None:
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    edges = read_parquet(PATHS.edges)
    if metadata.is_empty():
        raise RuntimeError("No metadata. Run `llm-wiki enrich` first.")

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)

    by_doi: dict[str, dict[str, Any]] = {r["doi"]: r for r in metadata.iter_rows(named=True)}

    # Count concept occurrences so we know which hubs to materialise.
    concept_counts: dict[str, int] = defaultdict(int)
    concept_canonical: dict[str, str] = {}  # slug → display name
    for r in metadata.iter_rows(named=True):
        for c in (r.get("concepts") or [])[:TOP_CONCEPTS_PER_PAPER]:
            name = c.get("name")
            if not name:
                continue
            slug = _concept_slug(name)
            concept_counts[slug] += 1
            concept_canonical[slug] = name

    hub_slugs = {s for s, n in concept_counts.items() if n >= MIN_CONCEPT_PAPERS}

    # Paper notes
    papers_written = 0
    for r in metadata.iter_rows(named=True):
        doi = r["doi"]
        if not doi:
            continue
        slug = doi_slug(doi)
        concepts = (r.get("concepts") or [])[:TOP_CONCEPTS_PER_PAPER]
        concept_names = [c.get("name") for c in concepts if c.get("name")]
        body = "\n".join(
            [
                _frontmatter(r, concept_names),
                f"# {r.get('title') or doi}",
                "",
                "## Abstract",
                "",
                r.get("abstract") or "_(no abstract available)_",
                "",
                _concept_section(concepts),
                _related_section(doi, edges, by_doi),
                "## Sources",
                "",
                f"- DOI: <https://doi.org/{doi}>",
                f"- OpenAlex: <{r.get('openalex_id')}>" if r.get("openalex_id") else "",
            ]
        )
        (PAPERS_DIR / f"{slug}.md").write_text(body, encoding="utf-8")
        papers_written += 1

    # Concept hubs
    for slug in hub_slugs:
        name = concept_canonical[slug]
        body = (
            "---\n"
            f"title: {name}\n"
            "type: concept\n"
            f"paper_count: {concept_counts[slug]}\n"
            "---\n\n"
            f"# {name}\n\n"
            f"_OpenAlex concept hub — {concept_counts[slug]} papers tagged._\n\n"
            "See *Linked mentions* in Obsidian's right sidebar for the full list.\n"
        )
        (CONCEPTS_DIR / f"{slug}.md").write_text(body, encoding="utf-8")

    (VAULT_DIR / "README.md").write_text(
        _readme(papers_written, len(hub_slugs), edges.shape[0]),
        encoding="utf-8",
    )

    logger.info(
        "vault written: %d papers + %d concept hubs at %s",
        papers_written, len(hub_slugs), VAULT_DIR,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    export()
