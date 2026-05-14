"""Render UMAP 2D map + Cytoscape graph as standalone HTML."""
from __future__ import annotations

import json
import logging

import numpy as np

from .config import PATHS
from .storage import read_parquet

logger = logging.getLogger(__name__)


def render_umap_map() -> None:
    metadata = read_parquet(PATHS.metadata)
    if metadata.is_empty():
        logger.warning("no metadata; skip umap")
        return

    # Cheap embeddings: TF-IDF on title+abstract, then UMAP. Avoids any LLM call.
    from sklearn.feature_extraction.text import TfidfVectorizer
    import umap

    text = [
        f"{r.get('title') or ''} {(r.get('abstract') or '')[:2000]}"
        for r in metadata.iter_rows(named=True)
    ]
    if len(text) < 5:
        logger.warning("too few papers for UMAP (%d)", len(text))
        return
    vec = TfidfVectorizer(max_features=4096, stop_words="english")
    X = np.asarray(vec.fit_transform(text).todense())  # type: ignore[union-attr]
    n_neighbors = min(15, max(2, len(text) - 1))
    reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=0.1, metric="cosine", random_state=42)
    coords = reducer.fit_transform(X)

    points = []
    for r, (x, y) in zip(metadata.iter_rows(named=True), coords, strict=False):
        points.append({"x": float(x), "y": float(y),
                       "title": r.get("title"), "doi": r.get("doi"),
                       "year": r.get("year")})
    html = _UMAP_TEMPLATE.replace("__POINTS__", json.dumps(points))
    (PATHS.docs_viz / "map.html").write_text(html, encoding="utf-8")
    logger.info("wrote UMAP map for %d points", len(points))


def render_cytoscape_graph() -> None:
    metadata = read_parquet(PATHS.metadata)
    edges = read_parquet(PATHS.edges)
    if metadata.is_empty() or edges.is_empty():
        logger.warning("no metadata/edges; skip cytoscape")
        return

    nodes_data = [
        {"data": {"id": r["doi"], "label": (r.get("title") or "?")[:60],
                  "year": r.get("year") or 0}}
        for r in metadata.iter_rows(named=True)
    ]
    edges_data = [
        {"data": {"id": f"e{i}", "source": e["src_doi"], "target": e["tgt_doi"],
                  "type": e["type"], "label": e.get("label") or ""}}
        for i, e in enumerate(edges.iter_rows(named=True))
    ]
    payload = {"nodes": nodes_data, "edges": edges_data}
    html = _CYTOSCAPE_TEMPLATE.replace("__PAYLOAD__", json.dumps(payload))
    (PATHS.docs_viz / "graph.html").write_text(html, encoding="utf-8")
    logger.info("wrote Cytoscape graph: %d nodes, %d edges",
                len(nodes_data), len(edges_data))


def render_all() -> None:
    PATHS.ensure()
    render_umap_map()
    render_cytoscape_graph()


_UMAP_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><title>llm-wiki — UMAP map</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>body{margin:0;font-family:system-ui;background:#0b0f17;color:#cdd6e4}
#title{position:absolute;top:8px;left:12px;font-size:14px;opacity:.8}</style>
</head><body>
<div id="title">llm-wiki — UMAP map of paradigm-shifting papers (TF-IDF over title+abstract)</div>
<div id="plot" style="width:100vw;height:100vh"></div>
<script>
const points = __POINTS__;
const trace = {
  x: points.map(p=>p.x), y: points.map(p=>p.y), mode: "markers",
  marker: { size: 7, color: points.map(p=>p.year || 1900), colorscale: "Viridis", showscale: true },
  text: points.map(p=>`<b>${p.title}</b><br>${p.year || ""}<br>${p.doi || ""}`),
  hoverinfo: "text"
};
const layout = {
  paper_bgcolor: "#0b0f17", plot_bgcolor: "#0b0f17", font: {color: "#cdd6e4"},
  xaxis: {visible:false}, yaxis: {visible:false}, margin: {l:0,r:0,t:0,b:0}
};
Plotly.newPlot("plot", [trace], layout, {responsive:true});
</script></body></html>
"""


_CYTOSCAPE_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><title>llm-wiki — chunk graph</title>
<script src="https://unpkg.com/cytoscape@3.30.1/dist/cytoscape.min.js"></script>
<style>html,body,#cy{width:100%;height:100%;margin:0;background:#0b0f17}
#title{position:absolute;top:8px;left:12px;font-size:14px;color:#cdd6e4;opacity:.8;font-family:system-ui}</style>
</head><body>
<div id="title">llm-wiki — chunk graph (drag, scroll to zoom; hover edges for "why related")</div>
<div id="cy"></div>
<script>
const data = __PAYLOAD__;
const cy = cytoscape({
  container: document.getElementById("cy"),
  elements: [].concat(data.nodes, data.edges),
  style: [
    { selector: "node", style: {
        "background-color": "#5b8def", "label": "data(label)", "color": "#cdd6e4",
        "font-size": "9px", "text-valign":"center", "text-halign":"center",
        "text-wrap":"wrap","text-max-width":80
      }},
    { selector: "edge", style: {
        "width": 1, "line-color": "#7a8aa3", "target-arrow-color": "#7a8aa3",
        "target-arrow-shape": "triangle", "curve-style": "bezier",
        "label": "data(type)", "font-size": "8px", "color": "#aab",
        "text-rotation":"autorotate"
      }},
    { selector: "edge[type='cite']", style: { "line-color":"#7e8aa1" }},
    { selector: "edge[type='enables']", style: { "line-color":"#3aa666" }},
    { selector: "edge[type='same-method']", style: { "line-color":"#c79a4a" }},
    { selector: "edge[type='contradicts']", style: { "line-color":"#d35050" }}
  ],
  layout: { name: "cose", animate: false, idealEdgeLength: 80 }
});
cy.on("mouseover", "edge", e => { e.target.style({ "label": e.target.data("label") || e.target.data("type") }); });
cy.on("mouseout", "edge", e => { e.target.style({ "label": e.target.data("type") }); });
</script></body></html>
"""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    render_all()
