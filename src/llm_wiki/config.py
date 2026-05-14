"""Project paths + environment config. Single source of truth for filesystem layout."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Paths:
    root: Path = PROJECT_ROOT
    data: Path = PROJECT_ROOT / "data"
    raw: Path = PROJECT_ROOT / "data" / "raw"
    seed: Path = PROJECT_ROOT / "data" / "raw" / "seed"
    candidates: Path = PROJECT_ROOT / "data" / "raw" / "candidates.parquet"
    core: Path = PROJECT_ROOT / "data" / "raw" / "core.parquet"
    metadata: Path = PROJECT_ROOT / "data" / "raw" / "metadata.parquet"
    papers: Path = PROJECT_ROOT / "data" / "raw" / "papers"
    graph: Path = PROJECT_ROOT / "data" / "graph"
    nodes: Path = PROJECT_ROOT / "data" / "graph" / "nodes.parquet"
    edges: Path = PROJECT_ROOT / "data" / "graph" / "edges.parquet"
    graph_gexf: Path = PROJECT_ROOT / "data" / "graph" / "graph.gexf"
    duckdb: Path = PROJECT_ROOT / "data.duckdb"
    vectors: Path = PROJECT_ROOT / "data" / "vectors"
    docs: Path = PROJECT_ROOT / "docs"
    docs_paper: Path = PROJECT_ROOT / "docs" / "paper"
    docs_topic: Path = PROJECT_ROOT / "docs" / "topic"
    docs_lineage: Path = PROJECT_ROOT / "docs" / "lineage"
    docs_viz: Path = PROJECT_ROOT / "docs" / "viz"

    def ensure(self) -> None:
        for p in [
            self.data, self.raw, self.seed, self.papers, self.graph, self.vectors,
            self.docs_paper, self.docs_topic, self.docs_lineage, self.docs_viz,
        ]:
            p.mkdir(parents=True, exist_ok=True)


PATHS = Paths()


@dataclass(frozen=True)
class Env:
    openalex_email: str = os.getenv("OPENALEX_EMAIL", "xodn348@tamu.edu")
    openalex_api_key: str | None = os.getenv("OPENALEX_API_KEY") or None
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY") or None
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY") or None
    claude_session_key: str | None = os.getenv("CLAUDE_SESSION_KEY") or None
    user_agent: str = "llm-wiki/0.1.0 (https://github.com/xodn348/llm-wiki; mailto:xodn348@tamu.edu)"


ENV = Env()
