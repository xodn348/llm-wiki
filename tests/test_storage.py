"""Round-trip storage helpers."""
from __future__ import annotations

import polars as pl

from llm_wiki.storage import doi_slug, normalize_doi


def test_normalize_doi_strips_url_prefix() -> None:
    assert normalize_doi("https://doi.org/10.1038/Nature12373") == "10.1038/nature12373"
    assert normalize_doi("DOI:10.1000/xyz") == "10.1000/xyz"
    assert normalize_doi(None) is None
    assert normalize_doi("") is None


def test_doi_slug_filename_safe() -> None:
    s = doi_slug("10.1038/s41586-021-03819-2")
    assert "/" not in s and " " not in s
    assert s.startswith("10_1038_")


def test_polars_roundtrip(tmp_path) -> None:
    from llm_wiki.storage import read_parquet, upsert_parquet, write_parquet

    df = pl.DataFrame({"doi": ["a", "b"], "x": [1, 2]})
    p = tmp_path / "x.parquet"
    write_parquet(df, p)
    again = read_parquet(p)
    assert again.shape == (2, 2)
    merged = upsert_parquet(pl.DataFrame({"doi": ["b", "c"], "x": [9, 3]}), p, key="doi")
    assert set(merged["doi"].to_list()) == {"a", "b", "c"}
    assert merged.filter(pl.col("doi") == "b")["x"].item() == 2  # original kept
