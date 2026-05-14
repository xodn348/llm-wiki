# llm-wiki — Schema (Karpathy LLM Wiki Layer 3)

This file is the **schema layer** of the [Karpathy LLM Wiki pattern][karp]:
it defines structure, conventions, and operations for any LLM (or human)
working on this wiki.

[karp]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Three-layer architecture

| Layer | Where | What | Mutability |
|-------|-------|------|-----------|
| **1. Raw** | `data/raw/` | seed dumps, candidates, core, fetched papers, OpenAlex metadata | immutable; only `ingest` writes |
| **2. Wiki** | `docs/paper/`, `docs/topic/`, `docs/lineage/`, `docs/viz/` | LLM-generated markdown + viz HTML | regenerated; only `wiki` / `viz` write |
| **3. Schema** | this file + `mkdocs.yml` + `pyproject.toml` | structure & operations | hand-edited by maintainer |

Spec lives at `docs/superpowers/specs/2026-05-14-llm-wiki-design.md` and
is the source of truth for design decisions.

## Three operations (Karpathy)

### `ingest` — add or refresh source material

```
uv run llm-wiki seed     # 1. assemble candidates from 9 sources
uv run llm-wiki filter   # 2. LLM tier filter → ~600 Fleming-tier
uv run llm-wiki enrich   # 3. OpenAlex bulk metadata
uv run llm-wiki fetch    # 4. download papers (OA → TAMU → manual)
uv run llm-wiki chunk    # 5. PageIndex trees
uv run llm-wiki tag      # 6. OpenAlex Concepts + MeSH
uv run llm-wiki graph    # 7. build chunk-level graph (5 edge types)
uv run llm-wiki label    # 8. LLM "why related" labels
uv run llm-wiki wiki     # 9. (re)generate wiki markdown
uv run llm-wiki viz      # 10. UMAP + Cytoscape HTML
```

`uv run llm-wiki all` runs the whole chain.

Each step is **idempotent** and **incremental** — re-running only
processes what changed.

### `query` — ask a question against the wiki

```
uv run llm-wiki query "What enabled CRISPR?"
```

Drops valuable answers back as new entries in `docs/topic/` or
`docs/lineage/`.

### `lint` — health check

```
uv run llm-wiki lint
```

Detects: contradictions across pages, stale claims (cite-only, no
content), missing cross-references, broken graph edges, papers in core
without an open page.

## Conventions

### Paper page (`docs/paper/<doi-slug>.md`)

```yaml
---
title: <paper title>
doi: 10.1038/...
openalex_id: W...
authors: [Author1, Author2]
year: YYYY
publication: <venue>
fleming_tier: true
seed_sources: [nobel, van_noorden_100]
concepts: [openalex_id1, mesh_term1]
---

# Title

## Why this mattered (paradigm shift)
<LLM-generated, 1–3 paragraphs>

## What it enabled
- [Linked downstream paper](../paper/<doi>.md) — <LLM "why" label>
- ...

## Method / key idea
<PageIndex tree summary, top 1–2 levels>

## Related
- **Builds on** [paper](../paper/<doi>.md) — <label>
- **Same method** [paper](../paper/<doi>.md) — <label>
- **Contradicts** [paper](../paper/<doi>.md) — <label>

## Sources
- Original: https://doi.org/<doi>
- OpenAlex: https://openalex.org/W...
- PDF: data/raw/papers/<doi>/full.pdf
```

### Topic page (`docs/topic/<slug>.md`)

LLM-aggregated synthesis of N Fleming-tier papers sharing a concept
cluster. Auto-generated; human-editable.

### Lineage page (`docs/lineage/<chain>.md`)

Traces an `enables` chain — e.g. `1953-double-helix → 1985-pcr →
2001-human-genome → 2021-alphafold`. Each step is one or two
paragraphs of LLM narrative grounded in the linked paper pages.

## Graph conventions

5 edge types: `cite`, `builds-on`, `enables`, `same-method`, `contradicts`.
Every edge has a one-sentence LLM-written `why` label. Stored in
`data/graph/edges.parquet`; exported to `data/graph/graph.gexf` for
Cytoscape/Gephi.

## Standards (do not deviate)

| Concern | Standard |
|---------|----------|
| Identifiers | DOI primary, OpenAlex Work ID secondary, arXiv ID where applicable |
| Bibliographic | CSL-JSON |
| Concepts | OpenAlex Concepts + MeSH + CSO |
| Graph | JSON-LD + schema.org/CreativeWork (+ GraphML/GEXF export) |
| Wiki | Markdown + YAML frontmatter |
| Embeddings | Parquet |
| Vector DB | ChromaDB |
| Analytics DB | DuckDB |

No project-private formats. Every artefact is one conversion away from
any other system.

## When unsure

Read the spec at `docs/superpowers/specs/2026-05-14-llm-wiki-design.md`
or follow the Karpathy gist linked at the top.
