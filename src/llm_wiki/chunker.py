"""Per-paper PageIndex semantic tree.

PageIndex turns long documents into hierarchical TOC-style trees with
section-level summaries — strict upgrade over arbitrary token chunking.
We invoke it as a library and store the resulting tree at
``data/raw/papers/<slug>/tree.json``.

If PageIndex is unavailable, we fall back to a naive heading-based
tree from the markdown — the rest of the pipeline still works.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

import polars as pl

from .config import PATHS
from .storage import doi_slug, read_parquet, write_parquet

logger = logging.getLogger(__name__)


def _try_pageindex(md_text: str) -> dict[str, Any] | None:
    try:
        import pageindex  # type: ignore[import-not-found]
    except Exception:
        return None
    try:
        # Library API is small; fall back gracefully if it changes.
        if hasattr(pageindex, "build_tree"):
            return pageindex.build_tree(md_text)  # type: ignore[no-any-return]
        if hasattr(pageindex, "PageIndexClient"):
            client = pageindex.PageIndexClient()
            return client.tree_from_markdown(md_text)  # type: ignore[no-any-return]
    except Exception as e:  # noqa: BLE001
        logger.warning("pageindex failed: %s — falling back to heading-tree", e)
    return None


_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def _heading_tree(md: str) -> dict[str, Any]:
    """Fallback: build tree from Markdown headings."""
    nodes: list[dict[str, Any]] = []
    for m in _HEADING.finditer(md):
        nodes.append({"level": len(m.group(1)), "title": m.group(2).strip(),
                      "start": m.start()})
    if not nodes:
        return {
            "title": "root",
            "children": [{"title": "Body", "summary": md[:500], "children": []}],
        }
    nodes.append({"level": 0, "title": "_end", "start": len(md)})
    children: list[dict[str, Any]] = []
    for i, n in enumerate(nodes[:-1]):
        body = md[n["start"]:nodes[i + 1]["start"]].strip()
        children.append(
            {"title": n["title"], "level": n["level"], "summary": body[:400],
             "children": []}
        )
    return {"title": "root", "children": children}


def _md_for(slug: str) -> str | None:
    paper_dir = PATHS.papers / slug
    md = paper_dir / "full.md"
    if md.exists():
        return md.read_text(encoding="utf-8", errors="ignore")
    pdf = paper_dir / "full.pdf"
    if pdf.exists():
        # Best-effort PDF→text via pypdf if available; we don't make it a
        # hard dep because PDF parsing quality is bad anyway.
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf))
            text = "\n\n".join(p.extract_text() or "" for p in reader.pages)
            md.write_text(text, encoding="utf-8")
            return text
        except Exception as e:  # noqa: BLE001
            logger.debug("pdf->text for %s failed: %s", slug, e)
    html = paper_dir / "landing.html"
    if html.exists():
        try:
            from markdownify import markdownify as md_from_html
            text = md_from_html(html.read_text(encoding="utf-8", errors="ignore"))
            md.write_text(text, encoding="utf-8")
            return text
        except Exception as e:  # noqa: BLE001
            logger.debug("html->md for %s failed: %s", slug, e)
    return None


def chunk_all() -> pl.DataFrame:
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    if metadata.is_empty():
        raise RuntimeError("No metadata. Run earlier stages first.")
    rows: list[dict[str, Any]] = []
    leaves: list[dict[str, Any]] = []

    for r in metadata.iter_rows(named=True):
        doi = r["doi"]
        slug = doi_slug(doi)
        md = _md_for(slug)
        if not md:
            rows.append({"doi": doi, "tree_status": "no_content"})
            continue
        tree = _try_pageindex(md) or _heading_tree(md)
        (PATHS.papers / slug / "tree.json").write_text(
            json.dumps(tree, indent=2, default=str), encoding="utf-8"
        )
        leaf_count = _walk_leaves(tree, doi, slug, leaves)
        rows.append({"doi": doi, "tree_status": "ok", "leaves": leaf_count})

    statuses = pl.from_dicts(rows)
    write_parquet(statuses, PATHS.raw / "chunk_status.parquet")
    nodes_df = pl.from_dicts(leaves) if leaves else pl.DataFrame()
    write_parquet(nodes_df, PATHS.nodes)
    logger.info("chunked: %d papers → %d leaves", len(rows), len(leaves))
    return statuses


def _walk_leaves(node: dict[str, Any], doi: str, slug: str, sink: list[dict[str, Any]],
                 *, path: list[str] | None = None) -> int:
    path = path or []
    here = path + [str(node.get("title", "?"))]
    children = node.get("children") or []
    if not children:
        sink.append(
            {
                "doi": doi,
                "slug": slug,
                "node_id": "/".join(here),
                "title": node.get("title"),
                "summary": (node.get("summary") or node.get("text") or "")[:1000],
            }
        )
        return 1
    return sum(_walk_leaves(c, doi, slug, sink, path=here) for c in children)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    chunk_all()
