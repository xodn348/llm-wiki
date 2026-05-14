"""DuckDB + parquet helpers. Single source of truth: parquet on disk; DuckDB views."""
from __future__ import annotations

from pathlib import Path

import duckdb
import polars as pl

from .config import PATHS


def write_parquet(df: pl.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path, compression="zstd")


def read_parquet(path: Path) -> pl.DataFrame:
    if not path.exists():
        return pl.DataFrame()
    return pl.read_parquet(path)


def upsert_parquet(df: pl.DataFrame, path: Path, key: str) -> pl.DataFrame:
    """Append rows whose key isn't already present."""
    existing = read_parquet(path)
    if existing.is_empty():
        write_parquet(df, path)
        return df
    seen = set(existing[key].to_list())
    fresh = df.filter(~pl.col(key).is_in(list(seen)))
    if fresh.is_empty():
        return existing
    out = pl.concat([existing, fresh], how="diagonal_relaxed")
    write_parquet(out, path)
    return out


def duck() -> duckdb.DuckDBPyConnection:
    """DuckDB connection that exposes every parquet in data/ as a view."""
    con = duckdb.connect(str(PATHS.duckdb))
    for name, path in [
        ("candidates", PATHS.candidates),
        ("core", PATHS.core),
        ("metadata", PATHS.metadata),
        ("nodes", PATHS.nodes),
        ("edges", PATHS.edges),
    ]:
        if path.exists():
            con.execute(
                f"CREATE OR REPLACE VIEW {name} AS SELECT * FROM read_parquet('{path}')"
            )
    return con


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
    return doi or None


def doi_slug(doi: str) -> str:
    """Filename-safe slug for a DOI: keep alphanumerics, replace separators with `_`."""
    return "".join(c if c.isalnum() else "_" for c in doi.lower()).strip("_")


__all__ = [
    "write_parquet",
    "read_parquet",
    "upsert_parquet",
    "duck",
    "normalize_doi",
    "doi_slug",
]
