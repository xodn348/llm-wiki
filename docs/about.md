---
title: About llm-wiki
---

# About llm-wiki

## What this is

llm-wiki is a small, curated, LLM-maintained wiki of scientific papers
that actually changed how humans understand or do something — at the
level of Fleming's 1929 paper on penicillin. It is *not* a comprehensive
bibliography of science, *not* a survey of the most-cited papers of the
last decade, and *not* a textbook. It is a deliberately narrow slice:
~848 papers across all of science, picked because each one is plausibly
**paradigm-shifting** in its field.

Around each paper the wiki carries an LLM-written "Why this mattered"
section, a paper-level citation/enables graph with one-sentence "why
related" labels on every edge, topic clusters by OpenAlex concept,
lineage walks through the `enables` subgraph, and a concept browser
over the 3,273 OpenAlex concepts present in the corpus. The whole
thing is generated from open data, runs on a single laptop, and ships
as MIT open-source so anyone can fork it and rebuild their own corpus.

## Fleming-tier criteria

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

The bar is "would a working scientist in the field point at this paper
as one of the handful that changed how the field thinks?" Citation
count alone does not clear it.

## The pipeline

The corpus is assembled by funnelling nine authoritative seed sources
through an LLM tier filter, then enriching, graphing, labelling, and
rendering.

| Stage | What | How |
|------|------|-----|
| **1. Seed** | Pull candidates from 9 sources | Nobel Prize references, Van Noorden Top 100, Wikipedia "Year in Science" 1900–2024, NIH Landmark Publications, APS Centennial Papers, Karpathy AI reading list + Awesome ML Papers, Garfield Citation Classics, OpenAlex `cited_by_count > 10k pre-2010` ∪ `> 5k post-2010`, Wikipedia "Important publications in X". **3,392 candidates total**. |
| **2. Dedup** | Collapse duplicates | DOI primary, fuzzy `(title, year)` secondary; cross-source corroboration preserved as `source_tag`. |
| **3. LLM tier filter** | Judge each candidate | Codex (GPT-5) reads title + abstract + citation count, applies the Fleming criteria, returns accept/reject + reason. Batch of 20. Incremental — only unjudged DOIs are re-scored. |
| **4. Enrich** | Metadata | OpenAlex bulk pull — authors, venue, year, concepts, MeSH terms, referenced works. |
| **5. Fetch** | PDFs where available | Unpaywall OA → 129 of 848 cached locally. The other 636 stay paper-level only. |
| **6. Graph** | Paper-level edges | OpenAlex `referenced_works` for `cite`, time-gap heuristic over shared concepts for `enables`. 1,438 edges. |
| **7. Label** | LLM "why related" | Codex writes a one-sentence label for every edge, grounded in the two paper abstracts. |
| **8. Render** | Static site | MkDocs Material — paper pages, topic clusters (15), lineage walks (11), concept browser, UMAP map, Cytoscape graph. |

Each step is idempotent and incremental. Re-running only touches what
changed. See [`PROJECT.md`](https://github.com/xodn348/llm-wiki/blob/main/PROJECT.md)
for the active roadmap and [`docs/superpowers/specs/2026-05-14-llm-wiki-design.md`](superpowers/specs/2026-05-14-llm-wiki-design.md)
for the full design.

## What we kept vs cut

Of 3,392 candidates the LLM tier filter has judged so far, **848
passed** and 1,400 were rejected — roughly a **37% acceptance rate**
over the OpenAlex pool. (237 newly added candidates from the v1.5
seed sources are still unjudged and will be appended on the next
filter pass.)

What typically gets rejected:

- **High-cite but incremental** — a popular variant of an existing
  method, or a high-impact application paper that didn't change the
  underlying theory.
- **Surveys and reviews** — even canonical ones. The wiki points at
  the primary sources a review summarises.
- **Methods refinement** — a faster algorithm, a cleaner proof, a
  larger benchmark. Useful, not paradigm-shifting.
- **Popular but not transformative** — viral papers that didn't durably
  change how the field works.
- **Reports, opinions, perspectives** — not original empirical or
  theoretical contributions.

What gets kept that surprises people:

- **Old foundational papers with modest raw citation counts** — they
  set up so much of the field that their ideas are now cited via
  textbooks instead of the original.
- **Method papers that founded a new way of doing science** — Lowry's
  protein assay, Laemmli's SDS-PAGE, Bradford, Kaplan–Meier.
  Mechanistically narrow, but they enabled thousands of downstream
  discoveries.

## Caveats

These are real and worth being upfront about.

### Publisher / venue bias

The OpenAlex seed slice ranks by `cited_by_count`, which over-represents
papers from high-impact-factor venues (Nature, Science, Cell, PNAS,
NEJM). Genuinely paradigm-shifting work published in lower-profile
venues — domain journals, conference proceedings, technical reports —
is systematically under-sampled. The other eight seed sources partly
compensate (Nobel references, NIH Landmarks, APS Centennial all draw
from a wider venue distribution), but the bias is structural and
non-zero.

### Time bias

Recent transformative work needs decades of citations to surface in
OpenAlex's high-cite slice. The post-2010 cutoff is relaxed to
`cited_by_count > 5k` to partially correct for this, but a paper
published in the last five years is still much less likely to be
caught by the seed than a paper from 1980. AlphaFold (2021) only
barely makes the recent-giants cutoff. Anything from 2023+ is
essentially absent.

### English-language bias

The corpus is English-only. Foundational Soviet, Chinese, Japanese,
French and German papers — Kolmogorov, Pontryagin, Ito, Bourbaki,
Wegener in his original German — are under-represented unless they
have widely cited English translations. OpenAlex itself indexes
non-English work but the seed lists and the LLM filter prompt are
both English-centric.

### Open-access bias for full text

Only 129 of 848 papers (**~15%**) have an open-access PDF cached
locally. The Phase 2 chunk-level graph (builds-on / same-method /
contradicts edges derived from PageIndex trees over full text) will
therefore only cover that subset. The other 636 paywalled papers
stay at paper-level only, with edges from OpenAlex `referenced_works`
plus the enables heuristic.

### LLM judgment caveat

The tier filter is Codex / GPT-5 making accept/reject calls from
title, abstract, and citation count. It is not a domain expert. It
will sometimes accept a high-cite paper that working scientists in
the field would call merely incremental, and it will sometimes
reject a paradigm-shifter whose abstract under-sells what the paper
actually did. Manual review of rejections is the v1 mitigation but
it is incomplete — the project welcomes flagged misjudgments via
GitHub Issues (see [CONTRIBUTING.md](https://github.com/xodn348/llm-wiki/blob/main/CONTRIBUTING.md)).

### Pre-1950 coverage gap

OpenAlex's index thins out before WWII. For older work the corpus
relies on the Nobel Prize references, Garfield Citation Classics,
and Wikipedia "Important publications in X" seeds to fill in. Many
genuinely foundational pre-1950 papers (Fleming 1929 itself, Mendel
1866, Carnot 1824, Maxwell 1865) are present, but the floor is
uneven and depends on whether those seed sources happen to list them.

## How to suggest a paper

Open a GitHub Issue with the title `Suggest Fleming-tier: <paper title>`
and the criteria checklist from [CONTRIBUTING.md](https://github.com/xodn348/llm-wiki/blob/main/CONTRIBUTING.md).
Or open a PR appending the DOI to `data/raw/seed/curated.json` (see
the contribution guide for the convention).

To flag a paper the filter accepted or rejected wrongly, open an
issue titled `Misjudged Fleming-tier: <doi>` with one sentence on
why the call was wrong.

## License + attribution

- **Code and project structure** — MIT. Fork it, rebuild your own
  corpus, change the criteria, ship it.
- **Paper metadata** — sourced from [OpenAlex](https://openalex.org/),
  released under CC0. Attribution is courtesy, not required.
- **LLM-written prose** — the "Why this mattered" sections, edge
  labels, topic syntheses, and lineage narratives are LLM-generated
  text grounded in paper abstracts. If you reuse them, attribute to
  the llm-wiki project and link back; the wiki itself attributes the
  underlying papers to their original authors.
