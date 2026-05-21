"""Per-paper semantic chunking.

For each cached PDF at ``data/raw/papers/<slug>/full.pdf`` we produce:

* ``tree.json`` — hierarchical chunk tree (root → leaves)
* ``leaves.parquet`` — flat table of leaf chunks for fast scans

and we aggregate every leaf across every paper into
``data/graph/nodes.parquet`` (the input to ``graph_builder`` and
``concept_tagger``).

PageIndex vs fallback
---------------------

The ``pageindex`` PyPI package is a thin client for VectifyAI's hosted
PageIndex API (requires an OpenAI-style API key against their service —
there is no library-mode that plugs into an arbitrary LLM callable like
our Codex backend). To keep the pipeline free and offline we therefore
ship a **fallback chunker**: ``pypdf`` extracts the text, we split on
~1500-character windows with 200-char overlap, and we build a 2-level
tree (paper-root → chunk leaves).

When/if PageIndex grows a local mode or the user sets
``PAGEINDEX_API_KEY``, ``_try_pageindex_api`` upgrades the per-PDF
output transparently — the rest of the pipeline only sees ``tree.json``.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import polars as pl
from tqdm import tqdm

from .config import PATHS
from .storage import write_parquet

logger = logging.getLogger(__name__)

# Fallback chunker parameters — tuned for paper-length PDFs.
_CHUNK_CHARS = 1500
_CHUNK_OVERLAP = 200
_MIN_PDF_BYTES = 1024
_EXCERPT_CHARS = 500


# --- public entry --------------------------------------------------------


def chunk_all(force: bool = False) -> pl.DataFrame:
    """Scan cached PDFs, build per-paper trees, aggregate nodes.parquet.

    :param force: if True, re-chunk PDFs even when ``tree.json`` is newer.
    :returns: a polars DataFrame with one row per processed PDF
        (columns: ``doi_slug``, ``status``, ``leaves``).
    """
    PATHS.ensure()
    pdfs = _discover_pdfs(PATHS.papers)
    if not pdfs:
        raise RuntimeError(
            f"No PDFs found under {PATHS.papers}. Run `llm-wiki fetch` first."
        )

    pageindex_client = _maybe_pageindex_client()
    if pageindex_client is not None:
        logger.info("PageIndex API key found — using hosted PageIndex.")
    else:
        logger.info("PageIndex unavailable — using pypdf fallback chunker.")

    status_rows: list[dict[str, Any]] = []
    all_nodes: list[dict[str, Any]] = []
    failures = 0

    for pdf_path in tqdm(pdfs, desc="chunking PDFs", unit="pdf"):
        slug = pdf_path.parent.name
        tree_path = pdf_path.parent / "tree.json"
        leaves_path = pdf_path.parent / "leaves.parquet"

        if not force and _is_fresh(tree_path, pdf_path) and leaves_path.exists():
            try:
                leaves_df = pl.read_parquet(leaves_path)
                all_nodes.extend(_leaves_to_nodes(leaves_df, slug))
                status_rows.append(
                    {"doi_slug": slug, "status": "cached", "leaves": leaves_df.height}
                )
                continue
            except Exception as e:  # noqa: BLE001
                logger.debug("cache reload failed for %s: %s — re-chunking", slug, e)

        try:
            tree = _build_tree(pdf_path, pageindex_client=pageindex_client)
            leaves = _walk_leaves(tree)
            if not leaves:
                raise RuntimeError("tree produced zero leaves")
            tree_path.write_text(
                json.dumps(tree, indent=2, default=str), encoding="utf-8"
            )
            leaves_df = pl.DataFrame(leaves)
            write_parquet(leaves_df, leaves_path)
            all_nodes.extend(_leaves_to_nodes(leaves_df, slug))
            status_rows.append(
                {"doi_slug": slug, "status": "ok", "leaves": len(leaves)}
            )
        except Exception as e:  # noqa: BLE001
            failures += 1
            logger.warning("chunk failed for %s: %s", slug, e)
            tree_path.write_text(
                json.dumps({"error": str(e), "slug": slug}, indent=2),
                encoding="utf-8",
            )
            status_rows.append({"doi_slug": slug, "status": "error", "leaves": 0})

    nodes_df = (
        pl.DataFrame(all_nodes)
        if all_nodes
        else pl.DataFrame(
            schema={
                "doi": pl.Utf8,
                "node_id": pl.Utf8,
                "parent_id": pl.Utf8,
                "depth": pl.Int64,
                "title": pl.Utf8,
                "summary": pl.Utf8,
                "text_excerpt": pl.Utf8,
            }
        )
    )
    write_parquet(nodes_df, PATHS.nodes)

    status_df = pl.DataFrame(status_rows)
    _print_summary(status_df, nodes_df, failures=failures)
    return status_df


# --- discovery -----------------------------------------------------------


def _discover_pdfs(papers_root: Path) -> list[Path]:
    """All ``<slug>/full.pdf`` files larger than 1 KB, sorted for determinism."""
    if not papers_root.exists():
        return []
    out: list[Path] = []
    for slug_dir in sorted(papers_root.iterdir()):
        if not slug_dir.is_dir():
            continue
        pdf = slug_dir / "full.pdf"
        try:
            if pdf.exists() and pdf.stat().st_size > _MIN_PDF_BYTES:
                out.append(pdf)
        except OSError:
            continue
    return out


def _is_fresh(tree_path: Path, pdf_path: Path) -> bool:
    if not tree_path.exists():
        return False
    try:
        # Also reject stub error-trees — re-attempt them on next run.
        data = json.loads(tree_path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "error" in data:
            return False
        return tree_path.stat().st_mtime >= pdf_path.stat().st_mtime
    except (OSError, json.JSONDecodeError):
        return False


# --- PageIndex (optional, hosted) ---------------------------------------


def _maybe_pageindex_client() -> Any | None:
    api_key = os.getenv("PAGEINDEX_API_KEY")
    if not api_key:
        return None
    try:
        import pageindex  # type: ignore[import-not-found]

        return pageindex.PageIndexClient(api_key)
    except Exception as e:  # noqa: BLE001
        logger.warning("PageIndexClient init failed: %s — using fallback", e)
        return None


def _try_pageindex_api(pdf_path: Path, client: Any) -> dict[str, Any] | None:
    """Submit a PDF to the hosted PageIndex service and fetch the tree.

    Returns None on any failure so the caller can fall back transparently.
    The hosted API processes asynchronously; we poll briefly then bail —
    long-running jobs are out of scope for this stage.
    """
    try:
        sub = client.submit_document(str(pdf_path))
        doc_id = sub.get("doc_id") or sub.get("id")
        if not doc_id:
            return None
        import time

        for _ in range(30):
            if client.is_retrieval_ready(doc_id):
                break
            time.sleep(2)
        return client.get_tree(doc_id, node_summary=True)
    except Exception as e:  # noqa: BLE001
        logger.debug("pageindex hosted API failed for %s: %s", pdf_path.name, e)
        return None


# --- fallback (pypdf + sliding-window) ----------------------------------


def _build_tree(pdf_path: Path, *, pageindex_client: Any | None) -> dict[str, Any]:
    """Return a normalised tree: ``{title, children: [...]}`` with ``children``
    optionally nested. Leaves carry ``title``, ``summary``, ``text``."""
    if pageindex_client is not None:
        tree = _try_pageindex_api(pdf_path, pageindex_client)
        if tree:
            return _normalise_pageindex_tree(tree, pdf_path.parent.name)

    text = _extract_pdf_text(pdf_path)
    return _sliding_window_tree(text, pdf_path.parent.name)


def _extract_pdf_text(pdf_path: Path) -> str:
    """Extract page-concatenated text via pypdf; surface a clear error if empty."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception:  # noqa: BLE001
            t = ""
        if t.strip():
            parts.append(t)
    text = "\n\n".join(parts).strip()
    if not text:
        raise RuntimeError("pypdf extracted no text (scanned/encrypted PDF?)")
    return text


def _sliding_window_tree(text: str, slug: str) -> dict[str, Any]:
    """2-level tree: paper root → sliding-window chunk leaves."""
    children: list[dict[str, Any]] = []
    i = 0
    idx = 0
    step = _CHUNK_CHARS - _CHUNK_OVERLAP
    while i < len(text):
        excerpt = text[i : i + _CHUNK_CHARS]
        leaf_id = f"c{idx:04d}"
        children.append(
            {
                "node_id": leaf_id,
                "title": _synthesize_title(excerpt, idx),
                "summary": excerpt[:_EXCERPT_CHARS],
                "text": excerpt,
                "children": [],
            }
        )
        idx += 1
        i += step
    return {
        "node_id": "root",
        "title": slug,
        "summary": f"{idx} chunks via pypdf fallback",
        "children": children,
    }


def _synthesize_title(excerpt: str, idx: int) -> str:
    """First non-trivial line of the chunk, capped — beats a bare 'Chunk N'."""
    for line in excerpt.splitlines():
        line = line.strip()
        if len(line) >= 8:
            return (line[:80] + "...") if len(line) > 80 else line
    return f"Chunk {idx}"


def _normalise_pageindex_tree(raw: Any, slug: str) -> dict[str, Any]:
    """Map PageIndex's API shape into our internal ``{title, children, ...}``."""

    def visit(node: Any) -> dict[str, Any]:
        if not isinstance(node, dict):
            return {"title": str(node), "children": []}
        kids = node.get("children") or node.get("nodes") or []
        return {
            "node_id": str(node.get("id") or node.get("node_id") or ""),
            "title": node.get("title") or node.get("name") or "section",
            "summary": node.get("summary") or node.get("node_summary") or "",
            "text": node.get("text") or "",
            "children": [visit(k) for k in kids],
        }

    if isinstance(raw, dict) and "tree" in raw:
        raw = raw["tree"]
    if isinstance(raw, list):
        return {
            "node_id": "root",
            "title": slug,
            "summary": "",
            "children": [visit(n) for n in raw],
        }
    return visit(raw)


# --- tree → leaves --------------------------------------------------------


def _walk_leaves(
    tree: dict[str, Any],
    *,
    parent_id: str | None = None,
    depth: int = 0,
    sink: list[dict[str, Any]] | None = None,
    path: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Depth-first walk; collect leaf nodes with their path/depth."""
    if sink is None:
        sink = []
    here_path = (path or []) + [str(tree.get("node_id") or tree.get("title") or "n")]
    children = tree.get("children") or []
    if not children:
        leaf_id = "/".join(here_path) if len(here_path) > 1 else here_path[0]
        text = tree.get("text") or tree.get("summary") or ""
        sink.append(
            {
                "leaf_id": leaf_id,
                "parent_id": parent_id or "",
                "depth": depth,
                "title": str(tree.get("title") or leaf_id)[:200],
                "summary": str(tree.get("summary") or "")[:_EXCERPT_CHARS],
                "text_excerpt": str(text)[:_EXCERPT_CHARS],
            }
        )
        return sink
    my_id = "/".join(here_path)
    for child in children:
        _walk_leaves(child, parent_id=my_id, depth=depth + 1, sink=sink, path=here_path)
    return sink


def _leaves_to_nodes(leaves_df: pl.DataFrame, slug: str) -> list[dict[str, Any]]:
    """Project a per-paper leaves table into rows for the global nodes parquet."""
    doi = _slug_to_doi(slug)
    rows: list[dict[str, Any]] = []
    for r in leaves_df.iter_rows(named=True):
        rows.append(
            {
                "doi": doi,
                "node_id": f"{slug}:{r['leaf_id']}",
                "parent_id": f"{slug}:{r['parent_id']}" if r.get("parent_id") else "",
                "depth": int(r["depth"]),
                "title": r.get("title") or "",
                "summary": r.get("summary") or "",
                "text_excerpt": r.get("text_excerpt") or "",
            }
        )
    return rows


def _slug_to_doi(slug: str) -> str:
    """Best-effort inverse of ``doi_slug``: ``10_1038_xxx`` → ``10.1038/xxx``.

    Lossy (the original DOI may have had additional non-word chars merged
    into ``_``), so downstream code should join on ``slug`` when an exact
    DOI match is required. We carry both via ``node_id`` (slug-prefixed)
    and ``doi`` (this reconstruction).
    """
    if not slug:
        return ""
    head, _, tail = slug.partition("_")
    if head.isdigit() and tail:
        registrant, _, rest = tail.partition("_")
        if rest:
            return f"{head}.{registrant}/{rest.replace('_', '-')}"
        return f"{head}.{tail}"
    return slug


# --- summary -------------------------------------------------------------


def _print_summary(
    status_df: pl.DataFrame, nodes_df: pl.DataFrame, *, failures: int
) -> None:
    total = status_df.height
    ok = status_df.filter(pl.col("status").is_in(["ok", "cached"])).height
    leaves = nodes_df.height
    avg = (leaves / ok) if ok else 0.0
    print()
    print("=" * 60)
    print(f"PDFs processed : {total}  (ok={ok}, failed={failures})")
    print(f"Total leaves   : {leaves}")
    print(f"Avg leaves/pdf : {avg:.1f}")
    if not nodes_df.is_empty():
        depth_dist = nodes_df.group_by("depth").len().sort("depth")
        print("Depth distribution:")
        for row in depth_dist.iter_rows(named=True):
            print(f"  depth={row['depth']:>2}  count={row['len']}")
    print("=" * 60)
    logger.info("Wrote %d nodes to %s", leaves, PATHS.nodes)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    chunk_all()
