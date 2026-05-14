---
title: llm-wiki — Fleming-tier scientific paper wiki
date: 2026-05-14
status: approved
---

# llm-wiki — Fleming-tier scientific paper wiki

## Goal

A persistent LLM-maintained wiki of paradigm-shifting scientific papers
(Fleming-tier: Nobel-grade, field-founders, papers that enabled subsequent
breakthroughs). Each paper is presented with:

- Why the discovery mattered
- What it enabled (lineage of follow-on work)
- How it relates to other paradigm-shifting papers (chunk-level graph)
- LLM-generated explanations on every relationship edge

The wiki is git-tracked Markdown, statically deployed to GitHub Pages,
conformant to the Karpathy LLM Wiki pattern, and uses standard formats
(DOI, CSL-JSON, OpenAlex Concepts/MeSH, JSON-LD, Markdown+YAML, Parquet,
GraphML) so the data interoperates with any other system.

## Non-goals (v0)

- Real-time updates (manual `ingest` only)
- Multi-user editing
- Mobile-optimised UI
- Languages other than English
- Exhaustive Fleming-tier judgments — LLM filter + manual spot-check is
  the v0 quality bar

## Architecture (Karpathy LLM Wiki pattern, strict)

Three layers, mirrored to disk:

```
~/code/llm-wiki/
├── data/raw/                Layer 1 (immutable)
│   ├── seed/                9 authoritative source dumps (.json)
│   ├── candidates.parquet   ~1500 deduped candidates
│   ├── core.parquet         ~600 LLM-confirmed Fleming-tier
│   ├── papers/<doi>/        PDF + full.md + tree.json (PageIndex output)
│   └── metadata.parquet     OpenAlex full enrichment
├── docs/                    Layer 2 (LLM-generated wiki, served by MkDocs)
│   ├── paper/<doi>.md
│   ├── topic/<slug>.md
│   ├── lineage/<chain>.md
│   ├── superpowers/specs/   This spec lives here
│   └── viz/                 UMAP map.html, graph.html
├── data/graph/
│   ├── nodes.parquet        chunk-level nodes (PageIndex leaves)
│   ├── edges.parquet        5-typed edges + LLM "why related" labels
│   └── graph.gexf           Cytoscape/Gephi export
├── data.duckdb              Single analytics DB (queryable from anywhere)
├── data/vectors/            ChromaDB (per-leaf embeddings)
├── CLAUDE.md                Layer 3 — Schema (ingest/query/lint commands)
├── mkdocs.yml               Static site config
└── src/llm_wiki/            Implementation (10 components)
```

## Components (10, each independently testable)

| # | Module | In | Out | External deps |
|---|--------|-----|-----|--------------|
| 1 | `seed_assembler` | 9 source URLs | `candidates.parquet` (~1500) | requests, BeautifulSoup |
| 2 | `tier_filter` | candidates | `core.parquet` (~600) | LLM (Claude session key) |
| 3 | `metadata_enricher` | core | `metadata.parquet` | OpenAlex API |
| 4 | `paper_fetcher` | core DOIs | `papers/<doi>/pdf` | OA → TAMU proxy → manual |
| 5 | `chunker` | PDFs/HTML | `papers/<doi>/tree.json` | **PageIndex** library |
| 6 | `concept_tagger` | leaves + abstract | tag table | OpenAlex Concepts + MeSH |
| 7 | `graph_builder` | leaves + tags + refs | `edges.parquet` (5 types) | embeddings + heuristics |
| 8 | `edge_labeler` | edges | LLM-written "why related" labels | LLM |
| 9 | `wiki_generator` | all of the above | `docs/paper|topic|lineage/*.md` | jinja2 |
| 10 | `viz_renderer` | graph + UMAP | `docs/viz/*.html` | Cytoscape.js, UMAP, plotly |

A `cli.py` (typer-based) wraps every component:
`llm-wiki seed | filter | enrich | fetch | chunk | tag | graph | label | wiki | viz | all`

## 9 authoritative seed sources

1. Nobel Prize references (nobelprize.org, 1901–2024 lectures + key citations)
2. Van Noorden "Top 100 papers" (Nature 2014, 514:550–553)
3. Wikipedia "Year in science" 1900–2024 (each year's discoveries + source DOIs)
4. NIH Landmark Publications
5. APS Centennial Papers (physics, 1899–1998)
6. Karpathy AI reading list + Awesome ML Papers (GitHub)
7. Garfield Citation Classics (when accessible)
8. OpenAlex query: `cited_by_count > 10000 AND publication_year < 2010`
   (auto-filter for "14+ years lasting ultra-high citation")
9. Wikipedia "List of Nobel laureates" — each laureate's "key publications"

After dedup (DOI primary, fuzzy title+year secondary): ~1500 candidates.

## tier_filter prompt (component 2)

For each candidate, single-shot LLM judgment:

> "Is this paper Fleming-tier? Criteria:
> (a) Founded a new field, OR
> (b) Caused paradigm shift, OR
> (c) Enabled subsequent breakthroughs, OR
> (d) Is universally taught as foundational.
>
> Reject if: high-citation but incremental; review article; methods-only
> without conceptual contribution; popular but not transformative.
>
> Output JSON: {tier: 'fleming' | 'reject', reason: <one sentence>}"

Run in batch=20 for cost. ~75 batches → ~$3 → ~600 confirmed.

## Data flow

```
9 sources (web/API)
  ──► seed_assembler ──► candidates.parquet (1500)
       └─► tier_filter (LLM) ──► core.parquet (600)
            └─► metadata_enricher (OpenAlex) ──► metadata.parquet
                 └─► paper_fetcher (parallel, 10 workers) ──► papers/<doi>/pdf
                      └─► html2md/pdf2md ──► full.md
                           └─► chunker (PageIndex) ──► tree.json
                                └─► concept_tagger ──► tags
                                     └─► graph_builder ──► edges.parquet
                                          └─► edge_labeler (LLM) ──► labeled edges
                                               └─► wiki_generator ──► docs/*.md
                                                    └─► viz_renderer ──► docs/viz/*.html
                                                         └─► mkdocs build
                                                              └─► gh-pages deploy
```

Every step caches to parquet/SQLite and is idempotent. Re-runs only do
the work that's stale.

## 5 edge types

| Type | How detected | Example label |
|------|--------------|--------------|
| `cite` | OpenAlex references graph | *"AlphaFold uses ESM protein model as baseline"* |
| `builds-on` | LLM over (cite + semantic) | *"Transformer generalises the attention mechanism from Bahdanau et al."* |
| `enables` | LLM follow-up trace | *"PCR enabled the Human Genome Project"* |
| `same-method` | shared concept tag + LLM check | *"Both use X-ray crystallography"* |
| `contradicts` | explicit LLM detection | *"A claims effect X under condition C; B finds none under same C"* |

## Standards (interop)

- **Identifiers**: DOI primary, OpenAlex Work ID secondary, arXiv ID where applicable
- **Bibliographic**: CSL-JSON (Zotero/Mendeley/Pandoc compatible)
- **Concepts**: OpenAlex Concepts (primary), MeSH (biomed overlay), CSO (CS overlay)
- **Graph**: JSON-LD with schema.org/CreativeWork + custom predicates
- **Wiki content**: Markdown + YAML frontmatter (Obsidian/Logseq/MkDocs portable)
- **Embeddings**: Parquet (DuckDB/polars/HF datasets)
- **Storage**: SQLite/DuckDB (analytics) + ChromaDB (vector) + plain files (content)
- **Graph export**: GraphML / GEXF (Cytoscape/Gephi)

No project-private formats are introduced.

## 909 Fleming-AI corpus — supporting layer

The existing 909 papers in TAMU GDrive `Fleming-AI/papers/` are not
Fleming-tier (they are high-cite 2015–2026 multi-disciplinary). They
become a **supporting context layer**: each Fleming-tier core paper page
references modern follow-up work from the 909 when overlap is detected.

## Deploy

- **MkDocs Material** as static site generator
- **GitHub Pages** from `gh-pages` branch
- **GitHub Actions** workflow: on push to `main` → run `mkdocs gh-deploy`
- Public site at `https://xodn348.github.io/llm-wiki/`

## Cost & runtime

| Stage | LLM calls | $ | wall time (parallelised) |
|------|-----------|----|---|
| Seed assembly | 0 | 0 | 30 min |
| Tier filter (1500 → 600) | ~75 batch | $3 | 1 h |
| Metadata enrichment | 0 | 0 | 5 min |
| Paper fetch (600) | 0 | 0 | 2 h |
| PageIndex (600) | ~6 000 | $15 | 3 h |
| Concept tagging | minor | $2 | 30 min |
| Edge gen + labeling | ~3 000 | $30 | 2 h |
| Wiki gen | ~1 000 | $5 | 1 h |
| Viz | 0 | 0 | immediate |
| Deploy | 0 | 0 | 5 min |
| **Total v0** | | **~$55** | **~10 h serial / ~4 h parallel** |
| Monthly maintenance | | ~$5 | 1 h |

Note: Using `CLAUDE_SESSION_KEY` makes most of this free (Claude.ai session,
no API billing). Estimates above assume API usage; session-key actual will
be ~$0.

## Test plan

- **Unit**: each component on mocked inputs
- **Integration**: smoke test on 5–10 papers covering different publishers
- **Manual review**: user reads 5 generated paper pages and judges
  "Fleming-tier appropriate"
- **Acceptance**: 600 papers ingested, graph rendered, can navigate
  AlphaFold → Transformer → Attention → backprop chain via labeled edges

## Out of scope (v0)

- Real-time auto-update
- Collaborative editing
- Mobile UI
- Non-English sources
- All-corner-case Fleming-tier judgements (LLM + spot-check is enough for v0)

## Future (v1+)

- Auto-discovery: surface new papers that may be Fleming-tier as they're
  cited by existing ones
- Multi-language sources
- Dedicated paper detail pages with embedded viz
- API surface for queries (`/api/papers/<doi>`, `/api/graph/<concept>`)
- Optional integration with Zotero / Obsidian / Logseq via the standard
  formats already produced
