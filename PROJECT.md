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

**Current state**: 4 of 9 sources wired → 3,155 candidates → 96 confirmed
Fleming-tier from a 200-paper heuristic shortlist (48 % pass rate). Need
to extend filter to the remaining ~2,000 candidates and wire the other 5
seed sources to reach ~600.

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

**Current state**: paper-level cite + enables done (71 edges, all labeled).
Chunk-level needs PDF fetch → PageIndex pass → tag → graph rebuild.

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

## Current state — 2026-05-19

- v1.1 deployed at https://xodn348.github.io/llm-wiki/
- 96 Fleming-tier papers, paper-level graph (71 labeled edges)
- LLM backend: Codex CLI (free)
- Next action: extend Phase 1 — filter remaining ~2,000 heuristic
  candidates and wire 5 more seed sources to reach the 600 target.
