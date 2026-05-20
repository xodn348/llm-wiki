# llm-wiki Obsidian Vault

Open this folder as an Obsidian vault — `Obsidian → Open folder as vault → obsidian-vault/`.

## What's in here

- **848 paper notes** under `papers/` — one per Fleming-tier paper
- **293 concept hub notes** under `concepts/` — every OpenAlex concept appearing in ≥ 3 papers
- **1438 edges** rendered as `[[wikilinks]]` in each paper's *Related* section

## How to use the graph

1. Open the graph view (`Cmd/Ctrl + G`).
2. Group by tag for color-by-field (Computer science, Biology, Physics, …).
3. Filter to one concept (e.g. `tag:#computer-science`) to slice down.
4. Hover an edge to see the LLM-written "why related" label.

## Regenerating

```
uv run llm-wiki obsidian
```

Re-runs are idempotent and reuse existing notes' frontmatter.
