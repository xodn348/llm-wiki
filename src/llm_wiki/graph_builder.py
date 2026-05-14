"""Build the chunk-level graph (5 edge types).

Edges:
- ``cite`` — paper A's metadata.referenced_works contains paper B
- ``builds-on`` — cite + LLM judgment (placeholder; LLM step in edge_labeler)
- ``enables`` — reverse of cite, only when downstream is "much later" (heuristic)
- ``same-method`` — leaves share top concept tag (level<=2)
- ``contradicts`` — assigned later by LLM scan; emitted blank here

Each edge here is unlabeled; ``edge_labeler`` adds the LLM "why" prose.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

import polars as pl

from .config import PATHS
from .storage import read_parquet, write_parquet

logger = logging.getLogger(__name__)


def _doi_from_openalex_id(meta: pl.DataFrame) -> dict[str, str]:
    out: dict[str, str] = {}
    for r in meta.iter_rows(named=True):
        if r.get("openalex_id") and r.get("doi"):
            out[r["openalex_id"]] = r["doi"]
    return out


def build() -> pl.DataFrame:
    PATHS.ensure()
    metadata = read_parquet(PATHS.metadata)
    nodes = read_parquet(PATHS.nodes)
    tags = read_parquet(PATHS.graph / "tags.parquet")
    if metadata.is_empty() or nodes.is_empty():
        raise RuntimeError("Need metadata and nodes. Run earlier stages first.")

    edges: list[dict[str, Any]] = []
    oa_to_doi = _doi_from_openalex_id(metadata)
    metadata_dois = set(metadata["doi"].to_list())

    # 1. cite edges
    for r in metadata.iter_rows(named=True):
        src_doi = r["doi"]
        for ref_oa in r.get("referenced_works") or []:
            tgt_doi = oa_to_doi.get(ref_oa)
            if tgt_doi and tgt_doi != src_doi and tgt_doi in metadata_dois:
                edges.append(
                    {
                        "src_doi": src_doi,
                        "tgt_doi": tgt_doi,
                        "src_node": "/".join([str(r["title"] or "?")]),
                        "tgt_node": None,
                        "type": "cite",
                        "weight": 1.0,
                        "label": None,
                    }
                )

    # 2. enables edges (cite reversed, time gap >= 5 yrs)
    by_doi_year = {r["doi"]: r["year"] for r in metadata.iter_rows(named=True)}
    cite_pairs = [(e["src_doi"], e["tgt_doi"]) for e in edges if e["type"] == "cite"]
    for src, tgt in cite_pairs:
        sy, ty = by_doi_year.get(src), by_doi_year.get(tgt)
        if sy and ty and (sy - ty) >= 5:
            edges.append(
                {
                    "src_doi": tgt,  # earlier paper enables...
                    "tgt_doi": src,  # ...later paper
                    "src_node": None,
                    "tgt_node": None,
                    "type": "enables",
                    "weight": 0.8,
                    "label": None,
                }
            )

    # 3. same-method edges via shared top-2 concepts
    if not tags.is_empty():
        per_concept: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for r in tags.iter_rows(named=True):
            if r.get("concept_level") is not None and r["concept_level"] <= 2:
                per_concept[r["concept_id"]].append((r["doi"], r["node_id"]))
        for members in per_concept.values():
            # cap fan-out per concept to avoid explosions
            for i, (d1, n1) in enumerate(members[:30]):
                for d2, n2 in members[i + 1 : i + 31]:
                    if d1 == d2:
                        continue
                    edges.append(
                        {
                            "src_doi": d1, "tgt_doi": d2,
                            "src_node": n1, "tgt_node": n2,
                            "type": "same-method", "weight": 0.4,
                            "label": None,
                        }
                    )

    df = pl.from_dicts(edges) if edges else pl.DataFrame()
    write_parquet(df, PATHS.edges)
    logger.info("graph built: %d edges", len(edges))
    _emit_gexf(metadata, df)
    return df


def _emit_gexf(metadata: pl.DataFrame, edges: pl.DataFrame) -> None:
    """Write a Gephi/Cytoscape-friendly GEXF export."""
    import xml.etree.ElementTree as ET
    gexf = ET.Element("gexf", xmlns="http://www.gexf.net/1.3", version="1.3")
    graph = ET.SubElement(gexf, "graph", mode="static", defaultedgetype="directed")
    nodes_el = ET.SubElement(graph, "nodes")
    for r in metadata.iter_rows(named=True):
        ET.SubElement(nodes_el, "node", id=r["doi"] or "?", label=r["title"] or "?")
    edges_el = ET.SubElement(graph, "edges")
    if not edges.is_empty():
        for i, e in enumerate(edges.iter_rows(named=True)):
            ET.SubElement(
                edges_el, "edge",
                id=str(i), source=e["src_doi"], target=e["tgt_doi"],
                label=e["type"], weight=str(e["weight"]),
            )
    tree = ET.ElementTree(gexf)
    tree.write(PATHS.graph_gexf, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    build()
