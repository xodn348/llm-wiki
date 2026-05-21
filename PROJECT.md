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

**Current state**: **9 of 9 sources wired → 3,392 candidates → 848 confirmed
Fleming-tier**. All seed sources active: OpenAlex (classics + recent),
Nobel laureates, Karpathy/Awesome-DL, Van Noorden Top 100, NIH
Landmarks, APS Centennial, Garfield Classics (host down at integration
— stub returns []), Wikipedia "Important publications in X". Garfield's
upenn.edu archive is intermittently offline; falls back gracefully.
**237 new candidates** from the 5 newly-wired sources are still
unjudged — next `llm-wiki filter` run will append to core.

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
labeled** (929 cite + 509 enables). **129 PDFs cached** via Unpaywall
OA (282 MB local, gitignored) — Phase 2 chunk-level kick-off material.
636 papers paywalled / no OA copy. Chunk-level still needs PageIndex
pass → tag → graph rebuild on the 129 OA-available papers (the 636
paywalled stay at paper-level only).

**Definition of done**: chunk-level graph with ≥3 edge types per paper
on average, every edge labeled.

### Phase 3 — Browse

Make the wiki navigable. Decide on ontology depth here.

| Sub-task | Default | Decision |
|---------|---------|---------|
| Static wiki | Markdown + MkDocs Material | ✅ already deployed |
| Topic / lineage pages | LLM-aggregated cluster summaries | ✅ v1.5 — 15 topics, 11 lineages |
| UMAP map | 2D map of papers, year-coloured | ✅ already deployed |
| Cytoscape graph | interactive, hover for labels | ✅ already deployed |
| Full-text search | MkDocs built-in `search` plugin | ✅ |
| Concept search | DuckDB query over `metadata.parquet` concepts | ✅ v1.5 — `docs/concepts.md`, 3,273 concepts |
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

## Current state — 2026-05-21

- v1.5 deployed at https://xodn348.github.io/llm-wiki/
- **848 Fleming-tier papers** with full LLM "Why this mattered" prose,
  paper-level graph with **1,438 labeled edges**
- All **9 seed sources wired** → 3,392 candidates (237 newly added,
  not-yet-judged by tier filter — next pass will append to core)
- New browse surfaces: **15 topic pages** (clustered by OpenAlex
  top-level concept), **11 lineage pages** (longest paths in the
  enables-subgraph), **concept browser** over 3,273 OpenAlex concepts
  (`docs/concepts.md`)
- **129 PDFs cached** via Unpaywall OA (282 MB, gitignored), 83 HTML
  landing pages, 636 paywalled — Phase 2 chunk-level can now start
- Obsidian vault (`obsidian-vault/`) shipped — 848 paper notes +
  293 concept hubs, `[[wikilinks]]` for graph browsing
- LLM backend: Codex CLI (free)
- Next action: (a) `llm-wiki filter` over the 237 newly-added
  candidates, (b) Phase 2 — PageIndex on the 129 OA PDFs →
  chunk-level edges (builds-on / same-method / contradicts).
