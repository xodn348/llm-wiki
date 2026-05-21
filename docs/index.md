# llm-wiki

> A personal LLM-maintained wiki of **paradigm-shifting scientific papers** —
> the ones that founded a field, caused a paradigm shift, or enabled
> subsequent breakthroughs. [Karpathy LLM Wiki][karp] pattern, Codex-driven
> "why this mattered" prose, OpenAlex / MeSH concepts, deployed via MkDocs.

[karp]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## v1.5 status

The wiki indexes **848 papers** confirmed Fleming-tier by an LLM filter
(Codex / GPT-5) over 3,392 candidates from nine authoritative seed
sources (OpenAlex high-citation slice, Nobel laureates, Karpathy's ML
reading list, Van Noorden Top 100, NIH Landmarks, APS Centennial,
Garfield Citation Classics, Wikipedia "Important publications in X").
**All 848 papers** carry an LLM-written *Why this mattered* section
grounded in the abstract and historical context.

Paper-level graph: **1,438 edges** (929 cite + 509 enables), every edge
carries a one-sentence LLM "why related" label.

New in v1.5:

- [**Topics**](topic/index.md) — papers clustered by OpenAlex top-level
  concept, each topic with an LLM 2-paragraph synthesis.
- [**Lineages**](lineage/index.md) — longest chains in the `enables`
  subgraph, walked step-by-step with grounded prose.
- [**Concepts**](concepts.md) — sortable, filterable browser over all
  3,273 OpenAlex Concepts present in the corpus, click-to-expand papers.
- **PDF corpus** — 129 open-access PDFs cached locally (282 MB,
  gitignored), seeding Phase 2 chunk-level work. 636 remain paywalled.

Also shipping: an **Obsidian vault** (`obsidian-vault/` in the repo) —
848 paper notes + 293 concept hub notes linked via `[[wikilinks]]`,
for force-directed graph browsing with tag-based color and search
filters. Open the folder as a vault in Obsidian.

Examples in the corpus:

- **Shannon — A Mathematical Theory of Communication (1948)**
- **Watson–Crick → PCR → Human Genome → AlphaFold** lineage
- **Lowry / Bradford / Laemmli** foundational biochem assays
- **Metropolis MCMC (1953)**, **Random Forests (2001)**, **ResNet (2016)**
- **Benjamini–Hochberg FDR (1995)**, **Kaplan–Meier (1958)**

## Visualisations

- [**UMAP map**](viz/map.html) — every paper as a point, coloured by year,
  TF-IDF over title + abstract. Hover for the title.
- [**Chunk graph**](viz/graph.html) — paper-level citation + enables edges
  with LLM-written "why related" labels (hover an edge to see).

## Browse

- [Papers](paper/index.md) — every Fleming-tier paper page
- [Topics](topic/index.md) — by OpenAlex top-level concept
- [Lineages](lineage/index.md) — chains of `enables` edges
- [Concepts](concepts.md) — searchable concept browser
- [Spec](superpowers/specs/2026-05-14-llm-wiki-design.md) — full design

## How papers are picked

Three-stage funnel:

1. **Authoritative seed** — 9 sources: OpenAlex (`cited_by_count > 10k
   pre-2010` ∪ `> 5k post-2010`), Karpathy / Awesome-DL reading lists,
   Nobel laureates, Van Noorden Top 100, NIH Landmarks, APS Centennial,
   Garfield Citation Classics, Wikipedia "Important publications in X".
   **3,392 candidates total**.
2. **Dedup** — by DOI primary, fuzzy `(title, year)` secondary. Cross-
   source corroboration is preserved in the merged `source_tag`.
3. **LLM tier filter** — Codex judges each on Fleming criteria
   (founded a field / caused paradigm shift / enabled breakthroughs /
   universally taught). **848 confirmed**, 1,400 rejected (~37% pass
   rate over the OpenAlex pool).

See [the spec][spec] for details.

[spec]: superpowers/specs/2026-05-14-llm-wiki-design.md

## Standards (interop)

DOI · OpenAlex Concepts · MeSH · CSL-JSON · JSON-LD + schema.org ·
Markdown + YAML · Parquet · DuckDB · ChromaDB · GraphML / GEXF.
Every artefact is one conversion away from any other system.

## Repo

[github.com/xodn348/llm-wiki](https://github.com/xodn348/llm-wiki) · MIT
