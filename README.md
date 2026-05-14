# llm-wiki

> Personal LLM-maintained wiki of **paradigm-shifting scientific papers**
> (Fleming-tier: Nobel-grade, field-founders, papers that enabled subsequent
> breakthroughs). Chunk-level graph + topic atlas, [Karpathy LLM Wiki][karp]
> pattern conformant.

[karp]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**Live wiki:** https://xodn348.github.io/llm-wiki/

## What this is

A few hundred papers across all of science, picked because they actually
changed how humans understand or do something — not because they have
high citations this year. For each paper:

- **Why it mattered** (paradigm shift, lineage of impact)
- **What it enabled** (downstream breakthroughs)
- **How it relates** to other paradigm-shifting papers — at the **chunk
  level**, with LLM-written explanations on every edge

Built around three open primitives:

| Primitive | Used for |
|-----------|----------|
| [Karpathy LLM Wiki pattern][karp] | Three-layer architecture (Raw / Wiki / Schema), `ingest` / `query` / `lint` operations |
| [PageIndex][pi] | Per-paper semantic tree (sections + summaries) instead of arbitrary chunks |
| [OpenAlex][oa] Concepts + MeSH | Standard concept tagging that interoperates with everything else |

[pi]: https://github.com/VectifyAI/PageIndex
[oa]: https://openalex.org/

## How papers are picked

Seeded from 9 authoritative sources, then LLM-filtered to Fleming-tier
(see [`docs/superpowers/specs/2026-05-14-llm-wiki-design.md`][spec]):

1. Nobel Prize references (1901–2024)
2. Van Noorden "Top 100 papers" (Nature, 2014)
3. Wikipedia "Year in science" 1900–2024
4. NIH Landmark Publications
5. APS Centennial Papers
6. Karpathy AI reading list + Awesome ML Papers
7. Garfield Citation Classics
8. OpenAlex `cited_by_count > 10000 AND year < 2010`
9. Wikipedia "List of Nobel laureates" key publications

Dedup → ~1500 candidates → LLM tier filter → ~600 confirmed Fleming-tier.

[spec]: docs/superpowers/specs/2026-05-14-llm-wiki-design.md

## Standards used (interop)

| Layer | Standard |
|-------|----------|
| Identifiers | DOI / OpenAlex Work ID / arXiv ID |
| Bibliographic | CSL-JSON |
| Concepts | OpenAlex Concepts + MeSH + CSO |
| Graph | JSON-LD + schema.org/CreativeWork (+ GraphML/GEXF export) |
| Wiki content | Markdown + YAML frontmatter |
| Embeddings | Parquet |
| Storage | DuckDB + ChromaDB |

No project-private formats are introduced — every artefact is one
conversion away from any other system.

## Run it

```bash
uv sync
uv run llm-wiki all          # full pipeline
uv run llm-wiki seed         # 1. assemble candidates from 9 sources
uv run llm-wiki filter       # 2. LLM tier filter
uv run llm-wiki enrich       # 3. OpenAlex metadata
uv run llm-wiki fetch        # 4. download papers
uv run llm-wiki chunk        # 5. PageIndex trees
uv run llm-wiki tag          # 6. concept tagging
uv run llm-wiki graph        # 7. cross-paper graph
uv run llm-wiki label        # 8. LLM "why related" labels
uv run llm-wiki wiki         # 9. generate markdown wiki
uv run llm-wiki viz          # 10. UMAP map + Cytoscape graph
mkdocs serve                 # preview locally
```

## License

MIT
