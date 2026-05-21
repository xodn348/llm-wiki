# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [v1.5] — 2026-05-21

### Added
- 5 new seed sources wired: Van Noorden Top 100, NIH Landmark
  Publications, APS Centennial Papers, Garfield Citation Classics,
  Wikipedia "Important publications in X" — bringing the seed total
  to **9 of 9** authoritative sources (3,392 candidates).
- **Topic cluster pages** — 15 topic pages clustered by OpenAlex
  top-level concept, each with an LLM 2-paragraph synthesis
  (`docs/topic/`).
- **Lineage pages** — 11 chains walked step-by-step through the
  `enables` subgraph with grounded LLM prose (`docs/lineage/`).
- **Concept browser** — client-side searchable browser at
  `docs/concepts.md` over all 3,273 OpenAlex Concepts in the corpus.
- **PDF cache** — 129 open-access papers cached locally via
  Unpaywall (282 MB, gitignored) — Phase 2 chunk-level kick-off
  material.
- New CLI subcommands: `llm-wiki topic`, `llm-wiki lineage`,
  `llm-wiki concepts`.

### Changed
- `seed_assembler.assemble()` is now incremental on `--only` runs —
  appends new sources without re-pulling existing ones.
- `mkdocs.yml` nav exposes Topics, Lineages, Concepts.
- Garfield Citation Classics falls back gracefully when the upenn.edu
  archive is offline (host has been intermittent).

## [v1.4] — 2026-05-20

### Added
- **Full LLM "Why this mattered" prose on all 848 papers** (up from
  581 in v1.3). Every Fleming-tier paper now carries 1–3 paragraphs
  grounded in its abstract and historical context.
- **Obsidian vault exporter** — `obsidian-vault/` ships 848 paper
  notes + 293 concept hub notes linked via `[[wikilinks]]` for
  force-directed graph browsing in Obsidian.

## [v1.3] — 2026-05-19

### Added
- LLM "Why this mattered" prose generated for 581 of 848 papers.

## [v1.2] — 2026-05-19

### Changed
- **Corpus expanded 96 → 848 Fleming-tier papers** — the LLM tier
  filter ran across the full OpenAlex high-citation slice plus the
  initial seed sources, accepting ~37% of judged candidates.

### Added
- `tier_filter` incremental mode — skips already-judged DOIs and
  appends new judgments to `data/raw/core.parquet`.
- `PROJECT.md` — 4-phase roadmap (collect → connect → browse →
  distribute) as the active source of truth for what's shipping next.

## [v1.1] — 2026-05-14

### Added
- LLM "why related" labels on all 71 paper-level edges — every
  citation and enables edge now carries a one-sentence grounded
  explanation.
- Paper pages updated to surface "What it enabled" and "Related"
  sections with edge labels inline.

## [v1] — 2026-05-14

### Added
- Real LLM Fleming-tier filter via Codex — replaces the v0 stub.
- 96 papers passing the filter, each with an LLM-written "Why this
  mattered" section.

## [v0] — 2026-05-14

### Added
- Initial scaffold: 10-component pipeline (seed → filter → enrich →
  fetch → chunk → tag → graph → label → wiki → viz) and the
  Karpathy LLM Wiki three-layer layout (`data/raw/`, `docs/`,
  `CLAUDE.md`).
- Ingested 200 papers, built paper-level graph, rendered UMAP map
  and Cytoscape graph, deployed to GitHub Pages.
- CI: install `--extra dev`, ruff relaxed for the v0 codebase.
