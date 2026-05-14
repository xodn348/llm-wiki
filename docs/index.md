# llm-wiki

> A personal LLM-maintained wiki of **paradigm-shifting scientific papers** —
> the ones that founded a field, caused a paradigm shift, or enabled
> subsequent breakthroughs. [Karpathy LLM Wiki][karp] pattern, Codex-driven
> "why this mattered" prose, OpenAlex / MeSH concepts, deployed via MkDocs.

[karp]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## v1 status

The wiki currently indexes **96 papers** confirmed Fleming-tier by an LLM
filter (Codex / GPT-5) over a 200-paper heuristic shortlist drawn from
~3,000 candidates (OpenAlex high-citation slice + curated reading lists).
Each paper has an LLM-written *Why this mattered* section grounded in
its abstract and historical context.

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

- [Spec](superpowers/specs/2026-05-14-llm-wiki-design.md) — full design
- [Papers](paper/index.md) — every Fleming-tier paper page

## How papers are picked

Three-stage funnel:

1. **Authoritative seed** — OpenAlex (`cited_by_count > 5,000`) + Karpathy
   reading list / Awesome ML Papers. ~3,155 candidates from 4 sources.
2. **Heuristic shortlist** — top by citation; trimmed to 200 for v1.
3. **LLM tier filter** — Codex judges each on Fleming criteria
   (founded a field / caused paradigm shift / enabled breakthroughs /
   universally taught). 96 of 200 confirmed.

The same pipeline scales to all 3,155 candidates and to `~600` core
papers as more sources (Nobel references, NIH Landmarks, APS Centennial,
Wikipedia "Year in science") are wired in. See [the spec][spec] for
details.

[spec]: superpowers/specs/2026-05-14-llm-wiki-design.md

## Standards (interop)

DOI · OpenAlex Concepts · MeSH · CSL-JSON · JSON-LD + schema.org ·
Markdown + YAML · Parquet · DuckDB · ChromaDB · GraphML / GEXF.
Every artefact is one conversion away from any other system.

## Repo

[github.com/xodn348/llm-wiki](https://github.com/xodn348/llm-wiki) · MIT
