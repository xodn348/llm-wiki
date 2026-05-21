# Contributing to llm-wiki

Thanks for wanting to help. llm-wiki is a small, opinionated wiki of
paradigm-shifting scientific papers. The two highest-value
contributions are **suggesting a Fleming-tier paper we missed** and
**flagging a paper the LLM filter judged wrongly**.

## Quick start

```bash
git clone https://github.com/xodn348/llm-wiki.git
cd llm-wiki
uv sync --extra dev
uv run llm-wiki --help
```

This installs the CLI, dev dependencies (ruff, pytest, mkdocs), and
prints the full subcommand list. To preview the site locally:

```bash
uv run mkdocs serve
```

## How to suggest a Fleming-tier paper

A paper is **Fleming-tier** if any of these hold:

- **(a)** founded a new field
- **(b)** caused a paradigm shift
- **(c)** enabled subsequent breakthroughs
- **(d)** is universally taught as foundational

A paper is **not** Fleming-tier if it is:

- high-citation but incremental
- review-only / survey
- methods refinement without conceptual contribution
- popular but not transformative
- textbook chapter / report / opinion

You have two routes.

### Route 1 — open an issue

Open a GitHub Issue titled:

```
Suggest Fleming-tier: <paper title>
```

Include:

- DOI (preferred) or OpenAlex Work ID or arXiv ID
- Year, venue, authors
- Which Fleming criterion it meets (a / b / c / d) and one sentence
  of why
- Optional: links to historical assessments (Nobel citation, Garfield
  classic, NIH landmark, etc.)

We'll add it to a manual seed list and let the LLM filter judge it on
the next ingest pass.

### Route 2 — open a PR

If you want to skip the queue, append the DOI to a manual curated
seed file at `data/raw/seed/curated.json`. The file does not exist
yet — be the first to create it. Convention:

```json
{
  "source": "curated",
  "added": "YYYY-MM-DD",
  "by": "<your github handle>",
  "papers": [
    {
      "doi": "10.1038/171737a0",
      "title": "A Structure for Deoxyribose Nucleic Acid",
      "year": 1953,
      "criterion": "b",
      "reason": "Established the double-helix model that grounded all of molecular biology."
    }
  ]
}
```

The `seed_assembler` will pick it up automatically on the next
`llm-wiki seed` run, dedup against existing candidates, and pass
the new papers through the tier filter.

## How to flag a misjudged paper

If the LLM filter accepted a paper you think is incremental, or
rejected one you think is paradigm-shifting, open an issue titled:

```
Misjudged Fleming-tier: <doi>
```

Include:

- DOI
- Whether the call was a false accept or false reject
- One sentence on why the call was wrong (one of the criteria above)

We'll re-check the call manually and either correct the verdict or
explain the reasoning. Flagged misjudgments are the v1 quality
mitigation — they directly improve the corpus.

## How to rebuild the corpus from scratch

The full pipeline. Each step is idempotent and incremental.

```bash
uv run llm-wiki seed       # 1. assemble candidates from 9 sources
uv run llm-wiki filter     # 2. LLM Fleming-tier filter
uv run llm-wiki enrich     # 3. OpenAlex metadata
uv run llm-wiki fetch      # 4. download OA PDFs
uv run llm-wiki chunk      # 5. PageIndex semantic trees
uv run llm-wiki tag        # 6. OpenAlex Concepts + MeSH
uv run llm-wiki graph      # 7. paper-level + chunk-level edges
uv run llm-wiki label      # 8. LLM "why related" edge labels
uv run llm-wiki wiki       # 9. render paper pages
uv run llm-wiki viz        # 10. UMAP map + Cytoscape graph
uv run llm-wiki topic      # 11. topic cluster pages
uv run llm-wiki lineage    # 12. lineage walks
uv run llm-wiki concepts   # 13. concept browser
```

Or `uv run llm-wiki all` for the lot. Re-running only processes what
changed. See [`CLAUDE.md`](CLAUDE.md) for the canonical operation list
and [`PROJECT.md`](PROJECT.md) for the current phase status.

## LLM backend setup

The default backend is **Codex CLI**, which is free if you have a
ChatGPT Plus / Pro account. Install instructions:
[github.com/openai/codex](https://github.com/openai/codex).

The fallback chain tries each in order until one succeeds:

| Backend | Env var | Notes |
|---------|---------|-------|
| `codex` (default) | none | uses local `codex` binary |
| `claude_session` | `CLAUDE_SESSION_KEY` | reuses your Claude Code session |
| `gemini` | `GEMINI_API_KEY` | Google AI Studio key |
| `anthropic` | `ANTHROPIC_API_KEY` | paid Anthropic API key |

Set `LLM_WIKI_BACKEND=<name>` to force a specific one. The filter,
label, "why this mattered", topic synthesis, and lineage narrative
steps all use whichever backend resolves first.

## Style / code quality

```bash
uv run ruff check         # lint
uv run ruff format        # format
uv run pytest             # tests
```

CI runs all three on every PR. Keep changes surgical — match the
existing code style even if you'd write it differently.

## Project shape

| File | What |
|------|------|
| [`PROJECT.md`](PROJECT.md) | Roadmap. Four phases, current status, definitions of done. |
| [`CLAUDE.md`](CLAUDE.md) | Schema. Karpathy LLM Wiki Layer 3 — page conventions, graph edge types, standards. |
| [`docs/about.md`](docs/about.md) | Methodology, criteria, caveats. Read this first if you're new. |
| [`docs/superpowers/specs/2026-05-14-llm-wiki-design.md`](docs/superpowers/specs/2026-05-14-llm-wiki-design.md) | Full design spec. Source of truth for design decisions. |
| [`CHANGELOG.md`](CHANGELOG.md) | What shipped in each release. |

Thanks again. Open an issue if anything in this guide is unclear.
