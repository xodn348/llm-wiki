# llm-wiki

> A curated, LLM-maintained wiki of **paradigm-shifting scientific papers** —
> Fleming-tier work that founded a field, caused a paradigm shift, or
> enabled subsequent breakthroughs.

**Live wiki:** [xodn348.github.io/llm-wiki](https://xodn348.github.io/llm-wiki/)

**v1.5:** 848 papers · 1,438 labeled edges · 15 topics · 11 lineages · 3,273 concepts · MIT license

## The 30-second pitch

A small, durable, LLM-maintained wiki of the papers that **actually
changed how humans understand or do something** — at the level of
Fleming's penicillin (1929). Their relationships are visible as a
graph you can browse, search, and learn from. The whole thing is
generated from open data, runs on a single laptop, and ships as MIT
open-source.

For each paper: an LLM-written "Why this mattered" section, a paper-level
citation + enables graph with one-sentence "why related" labels on every
edge, topic clusters by OpenAlex concept, lineage walks through the
`enables` subgraph, and a concept browser over the 3,273 OpenAlex
concepts present in the corpus.

The wiki is built around three open primitives:

| Primitive | Used for |
|-----------|----------|
| [Karpathy LLM Wiki pattern][karp] | Three-layer architecture (Raw / Wiki / Schema), `ingest` / `query` / `lint` |
| [PageIndex][pi] | Per-paper semantic tree instead of arbitrary chunks |
| [OpenAlex][oa] Concepts + MeSH | Standard concept tagging that interoperates with everything |

[karp]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
[pi]: https://github.com/VectifyAI/PageIndex
[oa]: https://openalex.org/

## Quick start

```bash
git clone https://github.com/xodn348/llm-wiki.git
cd llm-wiki
uv sync --extra dev
uv run llm-wiki --help
uv run mkdocs serve            # preview locally at http://localhost:8000
```

Full pipeline (each step idempotent + incremental):

```bash
uv run llm-wiki all            # seed → filter → enrich → fetch → chunk
                               # → tag → graph → label → wiki → viz
                               # → topic → lineage → concepts
```

## Pointers

| Where | What |
|-------|------|
| [docs/about.md](docs/about.md) | Methodology, Fleming-tier criteria, the six caveats users should know |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to suggest a paper, flag a misjudgment, rebuild the corpus |
| [PROJECT.md](PROJECT.md) | Four-phase roadmap and current status |
| [CLAUDE.md](CLAUDE.md) | Schema layer — page conventions, edge types, standards |
| [CHANGELOG.md](CHANGELOG.md) | What shipped in each release |
| [Live site](https://xodn348.github.io/llm-wiki/) | The deployed wiki |

## License

MIT — see [LICENSE](LICENSE). Paper metadata sourced from
[OpenAlex](https://openalex.org/) under CC0. LLM-written prose
(the "Why this mattered" sections, edge labels, topic syntheses,
lineage narratives) is generated content — attribute to the
llm-wiki project if reused, and to the original authors for the
underlying papers.
