"""Smoke test seed dedup logic without hitting the network."""
from __future__ import annotations

from llm_wiki.seed_assembler import _dedup


def test_dedup_by_doi_merges_source_tags() -> None:
    rows = [
        {"title": "X", "doi": "10.1/x", "source_tag": "a"},
        {"title": "X", "doi": "10.1/x", "source_tag": "b"},
        {"title": "Y", "doi": "10.2/y", "source_tag": "a"},
    ]
    out = _dedup(rows)
    assert len(out) == 2
    by_doi = {r["doi"]: r for r in out}
    assert by_doi["10.1/x"]["source_tag"] == "a|b"


def test_dedup_no_doi_uses_fuzzy_title_year() -> None:
    rows = [
        {"title": "Attention Is All You Need", "year": 2017, "source_tag": "a"},
        {"title": "attention is all you need!", "year": 2017, "source_tag": "b"},
        {"title": "Different Paper", "year": 2017, "source_tag": "c"},
    ]
    out = _dedup(rows)
    assert len(out) == 2
