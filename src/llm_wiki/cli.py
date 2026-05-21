"""CLI: ``llm-wiki <stage>``. Each stage is independently runnable."""
from __future__ import annotations

import logging

import typer
from rich.logging import RichHandler

from . import (
    chunker,
    concept_tagger,
    edge_labeler,
    graph_builder,
    metadata_enricher,
    obsidian_exporter,
    paper_fetcher,
    seed_assembler,
    tier_filter,
    viz_renderer,
    wiki_generator,
)

app = typer.Typer(help="llm-wiki: pipeline for Fleming-tier paper wiki")


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True, markup=False, show_path=False)],
    )


@app.callback()
def root(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    _setup_logging(verbose)


@app.command()
def seed(only: str | None = typer.Option(None, "--only", help="comma-separated source names")) -> None:
    """1. Assemble candidates from authoritative sources."""
    sources = [s.strip() for s in only.split(",")] if only else None
    seed_assembler.assemble(source_names=sources)


@app.command(name="filter")
def filter_(
    batch: int = 25,
    limit: int | None = None,
    heuristic: bool = typer.Option(False, help="Skip LLM; use citation-floor heuristic"),
    citation_floor: int = 5000,
) -> None:
    """2. LLM tier filter → core. Use --heuristic when LLM unavailable."""
    if heuristic:
        tier_filter.filter_heuristic(citation_floor=citation_floor)
    else:
        tier_filter.filter_candidates(batch_size=batch, limit=limit)


@app.command()
def enrich() -> None:
    """3. OpenAlex metadata for core."""
    metadata_enricher.enrich()


@app.command()
def fetch() -> None:
    """4. Download paper PDFs (open-access first)."""
    paper_fetcher.fetch()


@app.command()
def chunk(force: bool = typer.Option(False, "--force", help="Re-chunk PDFs even if tree.json is up-to-date.")) -> None:
    """5. Build PageIndex semantic trees."""
    chunker.chunk_all(force=force)


@app.command()
def tag() -> None:
    """6. Concept tagging from OpenAlex Concepts."""
    concept_tagger.tag_all()


@app.command()
def graph() -> None:
    """7. Build cross-paper graph."""
    graph_builder.build()


@app.command()
def label(batch: int = 20, max_edges: int | None = None) -> None:
    """8. LLM 'why related' labels."""
    edge_labeler.label_all(batch=batch, max_edges=max_edges)


@app.command()
def wiki(max_papers: int | None = None, no_llm: bool = False) -> None:
    """9. Generate wiki markdown pages."""
    wiki_generator.generate(max_papers=max_papers, with_llm=not no_llm)


@app.command()
def viz() -> None:
    """10. UMAP map + Cytoscape graph."""
    viz_renderer.render_all()


@app.command()
def obsidian() -> None:
    """11. Export as Obsidian vault for interactive graph browsing."""
    obsidian_exporter.export()


@app.command()
def topic() -> None:
    """12. Generate topic cluster pages from OpenAlex concepts."""
    from . import topic_pages
    topic_pages.generate_topics()


@app.command()
def lineage() -> None:
    """13. Generate lineage chain pages from enables edges."""
    from . import topic_pages
    topic_pages.generate_lineages()


@app.command()
def concepts() -> None:
    """14. Generate the concept browser page from OpenAlex concepts."""
    from . import concept_search
    concept_search.generate_concept_browser()


@app.command()
def paywall(out: str = "data/paywalled_urls.csv") -> None:
    """15. Generate proxied URLs for paywalled papers via TAMU."""
    from . import paywall_tamu
    paywall_tamu.write_proxied_urls(out)


@app.command(name="fetch-tamu")
def fetch_tamu(
    cookies: str = typer.Option("~/.config/llm-wiki/tamu-cookies.txt", "--cookies",
                                help="Path to Netscape cookies.txt exported from your TAMU-authenticated browser"),
    max_papers: int | None = typer.Option(None, "--max-papers"),
    delay: float = typer.Option(5.0, "--delay",
                                help="Seconds between requests (ToS-friendly; do not lower below 5)"),
) -> None:
    """16. Download paywalled papers via TAMU EZproxy using your browser cookies.

    Workflow:
      1. Log into proxy.library.tamu.edu in a browser (NetID + Duo).
      2. Export cookies (Chrome: 'Get cookies.txt LOCALLY' extension).
      3. Save to ~/.config/llm-wiki/tamu-cookies.txt
      4. Run this command.
    """
    from . import paywall_tamu
    paywall_tamu.fetch_with_tamu_cookies(cookies, max_papers=max_papers, rate_delay=delay)


@app.command()
def all_(skip_llm: bool = False) -> None:  # noqa: PLR0913
    """Run the entire pipeline."""
    seed_assembler.assemble()
    if not skip_llm:
        tier_filter.filter_candidates()
    metadata_enricher.enrich()
    paper_fetcher.fetch()
    chunker.chunk_all()
    concept_tagger.tag_all()
    graph_builder.build()
    if not skip_llm:
        edge_labeler.label_all()
    wiki_generator.generate(with_llm=not skip_llm)
    viz_renderer.render_all()


if __name__ == "__main__":
    app()
