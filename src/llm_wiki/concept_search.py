"""Client-side concept browser.

Reads OpenAlex Concepts from ``data/raw/metadata.parquet``, builds an
inverted index (concept -> [papers]), and writes a single static
``docs/concepts.md`` page with an embedded JSON blob and vanilla JS for
sorting, filtering, and click-to-expand paper lists.

Public API:
    generate_concept_browser() -> int   # number of unique concepts indexed
"""
from __future__ import annotations

import json
import logging
from collections import defaultdict

from .config import PATHS
from .storage import read_parquet, doi_slug

logger = logging.getLogger(__name__)


def _short_concept_id(raw_id: str | None) -> str:
    """Strip the OpenAlex URL prefix; keep just the ``C...`` id."""
    if not raw_id:
        return ""
    return raw_id.rsplit("/", 1)[-1]


def _build_index() -> tuple[dict, int]:
    """Return (index_payload, total_papers).

    Payload shape (designed to keep the embedded JSON compact by storing
    paper metadata once and referencing it by index):

        {
          "papers": [[slug, title, year], ...],   # 0-indexed paper table
          "concepts": [
            {"id": "C123", "name": "...", "level": 0, "p": [12, 47, ...]},
            ...
          ]
        }

    Concepts are sorted by paper count (desc), then name (asc).
    """
    df = read_parquet(PATHS.metadata)
    if df.is_empty():
        raise RuntimeError(
            f"No metadata at {PATHS.metadata}. Run `llm-wiki enrich` first."
        )

    papers: list[list] = []          # [slug, title, year]

    # concept_id -> {name, level, paper_idxs: [int]}
    bucket: dict[str, dict] = defaultdict(
        lambda: {"name": "", "level": 0, "paper_idxs": []}
    )

    for row in df.iter_rows(named=True):
        doi = row.get("doi")
        if not doi:
            continue
        slug = doi_slug(doi)
        title = row.get("title") or doi
        year = row.get("year")
        idx = len(papers)
        papers.append([slug, title, year])

        seen_on_paper: set[str] = set()
        for c in (row.get("concepts") or []):
            cid = _short_concept_id(c.get("id"))
            if not cid or cid in seen_on_paper:
                continue
            seen_on_paper.add(cid)
            entry = bucket[cid]
            if not entry["name"]:
                entry["name"] = c.get("name") or cid
                entry["level"] = int(c.get("level") or 0)
            entry["paper_idxs"].append(idx)

    concepts_out: list[dict] = []
    for cid, info in bucket.items():
        # Sort each concept's paper list by year desc, then title asc.
        idxs = sorted(
            info["paper_idxs"],
            key=lambda i: (-(papers[i][2] or 0), papers[i][1].lower()),
        )
        concepts_out.append(
            {
                "id": cid,
                "name": info["name"],
                "level": info["level"],
                "p": idxs,
            }
        )
    concepts_out.sort(key=lambda c: (-len(c["p"]), c["name"].lower()))

    return {"papers": papers, "concepts": concepts_out}, len(papers)


_PAGE_TEMPLATE = """# Concepts

Browse the {n_concepts} OpenAlex Concepts present across the
{n_papers} Fleming-tier papers in this corpus. Click a concept to expand its
paper list. Use the search box to filter concepts by name, and the column
headers to re-sort.

<div class="concept-browser">
  <input id="concept-search" type="search"
         placeholder="Filter concepts (e.g. 'biology', 'machine learning')..."
         autocomplete="off" spellcheck="false" />
  <div class="concept-meta">
    <span id="concept-visible-count">{n_concepts}</span> of {n_concepts} concepts
    &middot; sort:
    <button type="button" data-sort="count" class="concept-sort active">papers</button>
    <button type="button" data-sort="name" class="concept-sort">name</button>
    <button type="button" data-sort="level" class="concept-sort">level</button>
  </div>
  <table id="concept-table">
    <thead>
      <tr><th>Concept</th><th>Level</th><th>Papers</th></tr>
    </thead>
    <tbody id="concept-tbody"></tbody>
  </table>
</div>

<script id="concept-index" type="application/json">
{index_json}
</script>

<style>
.concept-browser {{ margin-top: 1rem; }}
.concept-browser #concept-search {{
  width: 100%; padding: 0.5rem 0.75rem; font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lightest, #ccc);
  border-radius: 4px; box-sizing: border-box;
}}
.concept-browser .concept-meta {{
  margin: 0.5rem 0; font-size: 0.85rem;
  color: var(--md-default-fg-color--light, #666);
}}
.concept-browser .concept-sort {{
  background: none; border: 1px solid transparent; cursor: pointer;
  padding: 2px 6px; margin: 0 2px; font: inherit;
  color: var(--md-primary-fg-color, #1976d2);
}}
.concept-browser .concept-sort.active {{
  border-color: currentColor; border-radius: 3px;
}}
.concept-browser #concept-table {{
  width: 100%; border-collapse: collapse; margin-top: 0.5rem;
}}
.concept-browser #concept-table th,
.concept-browser #concept-table td {{
  text-align: left; padding: 6px 10px;
  border-bottom: 1px solid var(--md-default-fg-color--lightest, #eee);
  vertical-align: top;
}}
.concept-browser #concept-table th {{ background: rgba(0,0,0,0.03); }}
.concept-browser .concept-row {{ cursor: pointer; }}
.concept-browser .concept-row:hover {{ background: rgba(0,0,0,0.04); }}
.concept-browser .concept-row .concept-name::before {{
  content: '\\25B6'; display: inline-block; width: 1em;
  font-size: 0.7em; transition: transform 0.15s;
  color: var(--md-default-fg-color--light, #888);
}}
.concept-browser .concept-row.open .concept-name::before {{ transform: rotate(90deg); }}
.concept-browser .concept-papers td {{ padding: 0 10px 10px 32px; background: rgba(0,0,0,0.015); }}
.concept-browser .concept-papers ul {{ margin: 4px 0; padding-left: 1.2em; }}
.concept-browser .concept-papers li {{ margin: 2px 0; font-size: 0.9em; }}
.concept-browser .concept-papers .year {{
  color: var(--md-default-fg-color--light, #888); margin-right: 0.4em;
}}
.concept-browser .level-badge {{
  display: inline-block; min-width: 1.5em; text-align: center;
  padding: 1px 6px; border-radius: 3px; font-size: 0.8em;
  background: rgba(25, 118, 210, 0.1);
}}
</style>

<script>
(function () {{
  const dataNode = document.getElementById('concept-index');
  if (!dataNode) return;
  const payload = JSON.parse(dataNode.textContent);
  const papers = payload.papers;       // [[slug, title, year], ...]
  const concepts = payload.concepts;   // [{{id, name, level, p: [idx,...]}}]

  const tbody = document.getElementById('concept-tbody');
  const search = document.getElementById('concept-search');
  const visibleCount = document.getElementById('concept-visible-count');
  const sortButtons = document.querySelectorAll('.concept-sort');

  let sortKey = 'count';
  let filterText = '';

  const sorters = {{
    count: (a, b) => b.p.length - a.p.length || a.name.localeCompare(b.name),
    name:  (a, b) => a.name.localeCompare(b.name),
    level: (a, b) => a.level - b.level || b.p.length - a.p.length,
  }};

  function escapeHtml(s) {{
    return String(s).replace(/[&<>"']/g, c => ({{
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }}[c]));
  }}

  function paperListHtml(idxs) {{
    return idxs.map(i => {{
      const p = papers[i];   // [slug, title, year]
      return '<li><span class="year">' + (p[2] || '?') + '</span>' +
             '<a href="paper/' + escapeHtml(p[0]) + '/">' +
             escapeHtml(p[1]) + '</a></li>';
    }}).join('');
  }}

  function render() {{
    const needle = filterText.trim().toLowerCase();
    const filtered = needle
      ? concepts.filter(c => c.name.toLowerCase().includes(needle))
      : concepts.slice();
    filtered.sort(sorters[sortKey]);
    visibleCount.textContent = filtered.length;

    const rows = filtered.map(c => (
      '<tr class="concept-row" data-id="' + escapeHtml(c.id) + '">' +
        '<td class="concept-name">' + escapeHtml(c.name) + '</td>' +
        '<td><span class="level-badge">L' + c.level + '</span></td>' +
        '<td>' + c.p.length + '</td>' +
      '</tr>' +
      '<tr class="concept-papers" data-for="' + escapeHtml(c.id) + '" hidden>' +
        '<td colspan="3"><ul></ul></td>' +
      '</tr>'
    ));
    tbody.innerHTML = rows.join('');
  }}

  // Lazy-fill the <ul> on first expansion so initial render stays fast.
  tbody.addEventListener('click', (ev) => {{
    const row = ev.target.closest('.concept-row');
    if (!row) return;
    const id = row.dataset.id;
    const detail = tbody.querySelector('.concept-papers[data-for="' + CSS.escape(id) + '"]');
    if (!detail) return;
    const ul = detail.querySelector('ul');
    if (!ul.dataset.filled) {{
      const c = concepts.find(x => x.id === id);
      if (c) {{
        ul.innerHTML = paperListHtml(c.p);
        ul.dataset.filled = '1';
      }}
    }}
    const open = !detail.hidden;
    detail.hidden = open;
    row.classList.toggle('open', !open);
  }});

  search.addEventListener('input', (ev) => {{
    filterText = ev.target.value;
    render();
  }});

  sortButtons.forEach(btn => {{
    btn.addEventListener('click', () => {{
      sortKey = btn.dataset.sort;
      sortButtons.forEach(b => b.classList.toggle('active', b === btn));
      render();
    }});
  }});

  render();
}})();
</script>
"""


def generate_concept_browser() -> int:
    """Build ``docs/concepts.md`` from ``data/raw/metadata.parquet``.

    Returns:
        Number of unique concepts indexed.
    """
    payload, total_papers = _build_index()
    n_concepts = len(payload["concepts"])

    # Keep the embedded payload compact: separators with no spaces.
    index_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    page = _PAGE_TEMPLATE.format(
        n_concepts=n_concepts,
        n_papers=total_papers,
        index_json=index_json,
    )

    out = PATHS.docs / "concepts.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    logger.info(
        "wrote %s: %d concepts across %d papers (%d bytes)",
        out, n_concepts, total_papers, out.stat().st_size,
    )
    return n_concepts


__all__ = ["generate_concept_browser"]
