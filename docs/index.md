# llm-wiki

> A personal LLM-maintained wiki of **paradigm-shifting scientific papers** —
> the ones that founded a field, caused a paradigm shift, or enabled
> subsequent breakthroughs. Karpathy [LLM Wiki][karp] pattern, PageIndex
> trees, OpenAlex/MeSH concepts, deployed via MkDocs.

[karp]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## v0 status

This first deployment indexes **~200 papers** drawn from the top of an
authoritative seed (OpenAlex `cited_by_count > 5000` + Karpathy /
Awesome ML reading lists), filtered to those with citations ≥ 31,000.

The full pipeline is in place; LLM-generated "why this mattered" prose
and per-leaf chunk graphs are queued for a later run.

## Visualisations

- [**UMAP map**](viz/map.html) — every paper as a point, coloured by year,
  TF-IDF over title + abstract. Hover for the title.
- [**Chunk graph**](viz/graph.html) — paper-level graph of citation +
  enables edges (same-method edges activate after PageIndex chunking).

## Browse

- [Spec](superpowers/specs/2026-05-14-llm-wiki-design.md) — full design
- [Papers](paper/index.md) — every Fleming-tier paper page

## How papers are picked

The current cut is a **citation-floor heuristic** (top of the OpenAlex
high-citation slice + the Karpathy/Awesome reading list). The more
expensive **LLM tier filter** ("would Fleming have called this
paradigm-shifting?") is implemented and ready, awaiting a working LLM
key. See [`src/llm_wiki/tier_filter.py`][tf] in the repo.

[tf]: https://github.com/xodn348/llm-wiki/blob/main/src/llm_wiki/tier_filter.py

## Standards used

DOI · OpenAlex Concepts · MeSH · CSL-JSON · JSON-LD + schema.org ·
Markdown + YAML · Parquet · DuckDB · ChromaDB · GraphML / GEXF.
Every artefact is one conversion away from any other system.

## Repo

[github.com/xodn348/llm-wiki](https://github.com/xodn348/llm-wiki) · MIT
