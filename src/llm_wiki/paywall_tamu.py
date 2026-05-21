"""TAMU institutional access resolver for paywalled DOIs.

Generates browser-clickable URLs that use Texas A&M University Libraries'
licensed subscriptions to reach the publisher's full text. This is the
*authorized patron* path — no DRM circumvention, no scraping of locked
content. The user logs in with their NetID once per session and clicks
through to download.

Three fallback strategies (priority order):

1. **EZproxy** — wraps the DOI in `proxy.library.tamu.edu/login?url=…`.
   Most reliable; works for any publisher TAMU subscribes to.
2. **OpenURL** — query against TAMU's link resolver (best-effort; TAMU
   does not publicly advertise a stable OpenURL endpoint, so this
   targets the discovery layer search at `search.library.tamu.edu`).
3. **LibKey** — Third Iron's one-click article resolver. TAMU's exact
   library slug is not publicly listed, so we emit the generic
   `libkey.io/{doi}` form which redirects through the user's
   browser-detected institution (works if LibKey Nomad is installed
   or the user is on the TAMU network).

See `docs/paywall.md` for the research write-up, ToS, and the planned
authenticated-fetch follow-up.
"""
from __future__ import annotations

import logging
import urllib.parse
from pathlib import Path

import polars as pl

from .config import PATHS

logger = logging.getLogger(__name__)

# Texas A&M University Libraries EZproxy login endpoint.
# Verified via library.tamu.edu (proxy.library.tamu.edu appears in
# canonical off-campus URLs across the libraries' public pages).
EZPROXY_LOGIN = "https://proxy.library.tamu.edu/login"

# Best-effort OpenURL target. TAMU's discovery layer is the public
# entry point for resource resolution; passing a DOI via the OpenURL
# `rft_id=info:doi/...` parameter is honored by most Alma/Primo
# installations even when a dedicated SFX hostname is not exposed.
OPENURL_BASE = "https://search.library.tamu.edu/discovery/openurl"
OPENURL_INSTITUTION = "01TAMUS_TAMU"

# LibKey article resolver. The generic `libkey.io/{doi}` redirects
# based on browser context; the institution-scoped form
# `libkey.io/libraries/{slug}/{doi}` requires TAMU's slug which is
# not publicly listed. We emit the generic form as the safer default.
LIBKEY_BASE = "https://libkey.io"


def resolve_via_ezproxy(doi: str) -> str | None:
    """Wrap ``https://doi.org/{doi}`` in TAMU's EZproxy login URL.

    Returns the URL string only — the actual fetch requires the user's
    NetID session in the browser. Returns None for empty input.
    """
    if not doi:
        return None
    target = f"https://doi.org/{doi}"
    return f"{EZPROXY_LOGIN}?url={urllib.parse.quote(target, safe='')}"


def resolve_via_openurl(
    doi: str,
    year: int | None = None,
    title: str | None = None,
) -> str | None:
    """Generate an OpenURL query against TAMU's link resolver.

    Uses NISO Z39.88 OpenURL 1.0 parameters. The DOI is the primary key;
    ``year`` and ``title`` are supplementary hints the resolver may use
    to disambiguate. Returns None for empty DOI.
    """
    if not doi:
        return None
    params: dict[str, str] = {
        "url_ver": "Z39.88-2004",
        "rft_id": f"info:doi/{doi}",
        "rfr_id": "info:sid/llm-wiki",
        "svc.fulltext": "yes",
        "institution": OPENURL_INSTITUTION,
    }
    if year is not None:
        params["rft.date"] = str(year)
    if title:
        params["rft.atitle"] = title
    return f"{OPENURL_BASE}?{urllib.parse.urlencode(params)}"


def resolve_via_libkey(doi: str) -> str | None:
    """Generate a LibKey article resolver URL.

    Uses the generic ``libkey.io/{doi}`` form which works through
    LibKey Nomad (browser extension) or on-campus IP. The
    institution-scoped form would be ``libkey.io/libraries/tamu/…``
    but TAMU's exact slug is not publicly documented; the generic form
    redirects appropriately for an authorized patron.
    """
    if not doi:
        return None
    return f"{LIBKEY_BASE}/{urllib.parse.quote(doi, safe='/')}"


def candidate_urls(
    doi: str,
    *,
    year: int | None = None,
    title: str | None = None,
) -> list[str]:
    """Return all available proxied URLs in priority order.

    Order: EZproxy → OpenURL → LibKey. The caller (typically the user
    in a browser) opens these in turn until one yields the PDF.
    """
    urls = [
        resolve_via_ezproxy(doi),
        resolve_via_openurl(doi, year=year, title=title),
        resolve_via_libkey(doi),
    ]
    return [u for u in urls if u]


def paywalled_dois() -> pl.DataFrame:
    """Return paywalled DOIs joined with metadata (title, year, venue).

    Source: ``data/raw/fetch_status.parquet`` filtered to
    ``method in ('no_open_url', 'failed')`` joined with
    ``data/raw/metadata.parquet`` on ``doi``.
    """
    status = pl.read_parquet(PATHS.raw / "fetch_status.parquet")
    paywalled = status.filter(pl.col("method").is_in(["no_open_url", "failed"]))
    metadata = pl.read_parquet(PATHS.metadata).select(
        ["doi", "title", "year", "venue"]
    )
    return paywalled.join(metadata, on="doi", how="left").select(
        ["doi", "title", "year", "venue", "method"]
    )


def write_proxied_urls(out: str | Path = "data/paywalled_urls.csv") -> Path:
    """Write a CSV of proxied URLs for every paywalled paper.

    Columns: ``doi, title, year, venue, ezproxy_url, openurl, libkey_url``.
    Returns the resolved output path.
    """
    df = paywalled_dois()
    rows = df.to_dicts()
    enriched = []
    for row in rows:
        doi = row["doi"]
        year = row.get("year")
        title = row.get("title")
        enriched.append({
            "doi": doi,
            "title": title,
            "year": year,
            "venue": row.get("venue"),
            "ezproxy_url": resolve_via_ezproxy(doi),
            "openurl": resolve_via_openurl(doi, year=year, title=title),
            "libkey_url": resolve_via_libkey(doi),
        })
    out_path = Path(out)
    if not out_path.is_absolute():
        out_path = PATHS.root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pl.DataFrame(enriched).write_csv(out_path)
    logger.info("wrote %d proxied URLs to %s", len(enriched), out_path)
    return out_path
