# llm-wiki — Project Roadmap

Single source of truth for what we're building and in what order.

Technical detail lives in [`docs/superpowers/specs/2026-05-14-llm-wiki-design.md`][spec];
this file is the *plan*.

[spec]: docs/superpowers/specs/2026-05-14-llm-wiki-design.md

## North star

> Build a small, durable, LLM-maintained wiki of the papers that **actually
> changed how humans understand or do something** — at the level of
> Fleming's penicillin (1929). Make their relationships visible as a graph
> you can browse, search, and learn from. Ship it open-source.

## Fleming-tier — what counts

A paper is **Fleming-tier** if any of:

- (a) **founded a new field**
- (b) **caused a paradigm shift**
- (c) **enabled subsequent breakthroughs**
- (d) is **universally taught as foundational**

A paper is **not** Fleming-tier if it is:
- high-citation but incremental
- review-only / survey
- methods refinement without conceptual contribution
- popular but not transformative
- textbook chapter / report / opinion

Target corpus: **~600 papers across all of science** (acceptable range 200–1500).

## The four phases

### Phase 1 — Collect (active)

Build the Fleming-tier corpus by funnelling authoritative seed sources
through an LLM tier filter.

| Stage | Source / Method | Estimated yield |
|------|-----------------|-----------------|
| Seed | 9 authoritative sources (Nobel refs, Van Noorden Top 100, Wikipedia Year in Science, NIH Landmarks, APS Centennial, Karpathy/Awesome ML, Garfield Classics, OpenAlex `cited_by_count>10000 AND year<2010`, Wikipedia Nobel laureates) | ~3,000–6,000 candidates |
| Dedup | DOI primary, fuzzy (title, year) secondary | → unique candidates |
| LLM tier filter | Codex judges Fleming criteria, batch=20 | ~30–50 % pass rate |
| Manual review | Spot-check rejections + missed classics | — |

**Current state**: 4 of 9 sources wired → 3,155 candidates → **848 confirmed
Fleming-tier** (96 prior + 752 from extended filter, ~37% pass rate over
the full openalex pool). Right at the top of the 600 ± 200 target. Five
other seed sources (Van Noorden Top 100, NIH Landmarks, APS Centennial,
Garfield Classics, Wikipedia Year in Science) still pending — those
would mostly add pre-1950 coverage that OpenAlex misses.

**Definition of done**: 600 ± 200 papers in `data/raw/core.parquet`,
each with OpenAlex metadata enriched, each with a paper page.

### Phase 2 — Connect

Use **Karpathy LLM Wiki** pattern + **PageIndex** semantic trees to build
a chunk-level graph linking the corpus.

| Layer | What | Mechanism |
|------|------|-----------|
| Paper-level | cite / enables edges | OpenAlex referenced_works + time-gap heuristic |
| Chunk-level | builds-on / same-method / contradicts | PageIndex tree leaves + LLM judgements |
| Edge labels | One-sentence "why related" on every edge | LLM (Codex), already working at v1.1 |
| Concept overlay | OpenAlex Concepts + MeSH | already wired |

**Current state**: paper-level cite + enables done — **1,438 edges, all
labeled** (929 cite + 509 enables). Chunk-level needs PDF fetch →
PageIndex pass → tag → graph rebuild.

**Definition of done**: chunk-level graph with ≥3 edge types per paper
on average, every edge labeled.

### Phase 3 — Browse

Make the wiki navigable. Decide on ontology depth here.

| Sub-task | Default | Decision |
|---------|---------|---------|
| Static wiki | Markdown + MkDocs Material | ✅ already deployed |
| Topic / lineage pages | LLM-aggregated cluster summaries | to do |
| UMAP map | 2D map of papers, year-coloured | ✅ already deployed |
| Cytoscape graph | interactive, hover for labels | ✅ already deployed |
| Full-text search | MkDocs built-in `search` plugin | ✅ |
| Concept search | DuckDB query over `metadata.parquet` concepts | to do |
| **Ontology** | OpenAlex Concepts + MeSH as overlay | **open** — adopt a formal ontology (e.g. publish JSON-LD with `schema.org/CreativeWork` + custom predicates) only if it pays for itself in downstream interop |

**Definition of done**: a visitor can land on the site and either browse
by topic, search by concept, or follow the graph from any paper to its
intellectual ancestors and descendants — within 3 clicks.

### Phase 4 — Distribute

Ship as MIT open-source for anyone to fork, contribute to, or rebuild
their own corpus.

- ✅ MIT license already on repo
- ✅ Repo is public
- ✅ GitHub Pages deployment automated via Actions
- to do: release tag + CHANGELOG once Phase 1+2 are at "done"
- to do: README contribution guide ("how to suggest a Fleming-tier paper",
  "how to rebuild the corpus from scratch")
- to do: `mkdir docs/about/` page explaining methodology, criteria,
  caveats (publisher bias, time bias, LLM-judgment caveats)

## Non-goals (for now)

- Real-time auto-update (manual `ingest` only)
- Multi-user editing
- Mobile-optimised UI
- Languages other than English
- Exhaustive Fleming-tier judgments — LLM filter + manual spot-check is
  the v1 quality bar

## Current state — 2026-05-20

- v1.4 deployed at https://xodn348.github.io/llm-wiki/
- **848 Fleming-tier papers**, paper-level graph with **1,438 labeled edges**
- **All 848 papers** have full LLM "why this mattered" prose
- Obsidian vault (`obsidian-vault/`) shipped — 848 paper notes +
  293 concept hubs, `[[wikilinks]]` for graph browsing
- LLM backend: Codex CLI (free)
- Next action: Phase 2 (PDF fetch → PageIndex → chunk-level graph).
  Optional Phase 1 polish: wire the 5 remaining seed sources
  (Van Noorden, NIH Landmarks, APS Centennial, Garfield Classics,
  Wikipedia Year-in-Science).
