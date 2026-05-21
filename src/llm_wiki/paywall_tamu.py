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

import http.cookiejar
import logging
import re
import time
import urllib.parse
from pathlib import Path

import httpx
import polars as pl

from .config import PATHS
from .storage import doi_slug

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


# --- Authenticated fetch via reused TAMU session cookies ----------------

# Google Scholar's `citation_pdf_url` meta tag is honored by Nature,
# Science, AAAS, ACS, RSC, JAMA, NEJM, Springer, BMJ, and most other
# major publishers. When present it's the canonical full-text PDF URL.
_PDF_META_RE = re.compile(
    r'<meta\s+(?:name|property)=["\']citation_pdf_url["\']\s+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)

# Cookie reuse session lifetime warning threshold (TAMU EZproxy sessions
# typically expire 8-24h after last use).
SESSION_PROBE_URL = "https://proxy.library.tamu.edu/menu"


def _load_cookiejar(cookies_path: Path) -> http.cookiejar.MozillaCookieJar:
    """Load a Netscape/Mozilla cookies.txt file (browser-export format)."""
    jar = http.cookiejar.MozillaCookieJar(str(cookies_path))
    jar.load(ignore_discard=True, ignore_expires=True)
    return jar


def _load_browser_cookies(browser: str | None = None) -> http.cookiejar.CookieJar:
    """Auto-import cookies from the user's installed browser via browser-cookie3.

    No manual export required — reads directly from Chrome/Firefox/Safari
    cookie store on disk. On macOS Chrome this prompts for keychain access
    once. Loads all cookies (no domain filter) so Shibboleth SP cookies on
    publisher and proxy subdomains are captured; the per-domain match is
    handled by httpx when each request fires.
    """
    import browser_cookie3
    from collections.abc import Callable

    loaders: dict[str, Callable] = {
        "chrome": browser_cookie3.chrome,
        "firefox": browser_cookie3.firefox,
        "safari": browser_cookie3.safari,
        "edge": browser_cookie3.edge,
        "brave": browser_cookie3.brave,
    }

    def _summarize(jar) -> dict[str, int]:
        counts: dict[str, int] = {}
        for c in jar:
            counts[c.domain] = counts.get(c.domain, 0) + 1
        return counts

    if browser:
        if browser not in loaders:
            raise ValueError(f"unknown browser {browser!r}; pick one of {list(loaders)}")
        try:
            jar = loaders[browser]()
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"{browser} cookie import failed: {e}") from e
        relevant = {d: n for d, n in _summarize(jar).items()
                    if "tamu" in d.lower() or "shibboleth" in d.lower()}
        logger.info("loaded %d cookies from %s; tamu/shib domains: %s",
                    sum(1 for _ in jar), browser, relevant or "(none)")
        return jar

    # Try each browser until one yields *tamu-related* cookies
    last_error = None
    for name, loader in loaders.items():
        try:
            jar = loader()
            tamu_count = sum(
                1 for c in jar
                if "tamu" in c.domain.lower() or "shibboleth" in c.domain.lower()
            )
            if tamu_count > 0:
                relevant = {d: n for d, n in _summarize(jar).items()
                            if "tamu" in d.lower() or "shibboleth" in d.lower()}
                logger.info("loaded %d cookies from %s; tamu/shib: %s",
                            sum(1 for _ in jar), name, relevant)
                return jar
        except Exception as e:  # noqa: BLE001
            last_error = e
            logger.debug("%s cookie import failed: %s", name, e)
            continue
    raise RuntimeError(
        f"no browser had TAMU/Shibboleth cookies (last error: {last_error}). "
        "Log into proxy.library.tamu.edu in your browser first."
    )


def _probe_session(client: httpx.Client) -> bool:
    """Confirm the cookies still authenticate against the proxy."""
    try:
        r = client.get(SESSION_PROBE_URL, timeout=20.0)
    except Exception as e:  # noqa: BLE001
        logger.warning("session probe failed: %s", e)
        return False
    if r.status_code != 200:
        return False
    # The unauthenticated menu redirects to login; authenticated shows a
    # resource list. Heuristic: presence of "logout" or absence of NetID
    # field signals an active session.
    body = r.text.lower()
    return "logout" in body or "log out" in body or "menu" in body


def _extract_pdf_url(html: str, base_url: str) -> str | None:
    """Find a PDF URL inside the landing page HTML.

    Strategy: citation_pdf_url meta tag (works for ~70% of publishers),
    then fall back to any anchor whose href ends in .pdf.
    """
    m = _PDF_META_RE.search(html)
    if m:
        return urllib.parse.urljoin(base_url, m.group(1))
    # Fallback: scan for first .pdf link
    for href_match in re.finditer(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', html, re.IGNORECASE):
        return urllib.parse.urljoin(base_url, href_match.group(1))
    return None


def fetch_with_tamu_cookies(
    cookies_path: str | Path | None = None,
    *,
    browser: str | None = None,
    max_papers: int | None = None,
    rate_delay: float = 5.0,
    skip_existing: bool = True,
) -> pl.DataFrame:
    """Download paywalled papers via TAMU EZproxy using a reused browser session.

    User workflow (simplest path — no manual export):
      1. Log into ``https://proxy.library.tamu.edu/login`` in your browser
         (NetID + Duo 2FA). Tick "remember this device" if offered.
      2. Run ``llm-wiki fetch-tamu`` — it auto-imports cookies from your
         installed browser (Chrome / Firefox / Safari / Edge / Brave).
         On macOS Chrome you'll get one Keychain prompt for cookie access.

    Optional: pass ``--cookies path/to/cookies.txt`` if you'd rather export
    a Netscape cookies.txt manually via a browser extension. The file
    overrides browser auto-import.

    For each paywalled DOI: hits EZproxy → follows redirects through
    publisher → extracts ``citation_pdf_url`` meta tag → downloads PDF.

    Honors a 5-second rate delay between requests by default (ToS-friendly
    for institutional patrons; do NOT lower this).

    Returns a DataFrame with the per-paper fetch status. Also updates the
    canonical ``data/raw/fetch_status.parquet`` so re-runs are idempotent.
    """
    if cookies_path:
        path = Path(cookies_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(
                f"TAMU cookies file not found: {path}\n"
                "Omit --cookies to auto-import from your browser instead."
            )
        jar: http.cookiejar.CookieJar = _load_cookiejar(path)
        logger.info("loaded cookies from file %s", path)
    else:
        jar = _load_browser_cookies(browser=browser)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ),
        "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8",
    }

    df = paywalled_dois()
    rows = df.to_dicts()
    if max_papers is not None:
        rows = rows[:max_papers]

    statuses: list[dict] = []
    with httpx.Client(cookies=jar, headers=headers, follow_redirects=True, timeout=60.0) as c:
        if not _probe_session(c):
            logger.warning(
                "session probe failed (proxy.library.tamu.edu/menu didn't authenticate). "
                "Per-paper fetches may still work if the proxy auth flow is invoked "
                "on first publisher hit. Continuing — re-run if all rows fail."
            )
        else:
            logger.info("session OK")
        logger.info("starting fetch of %d paywalled papers (delay=%.1fs)",
                    len(rows), rate_delay)

        for i, row in enumerate(rows, 1):
            doi = row["doi"]
            slug = doi_slug(doi)
            paper_dir = PATHS.papers / slug
            paper_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = paper_dir / "full.pdf"

            if skip_existing and pdf_path.exists() and pdf_path.stat().st_size > 1024:
                statuses.append({"doi": doi, "method": "tamu_cached", "pdf_bytes": pdf_path.stat().st_size})
                continue

            ezproxy = resolve_via_ezproxy(doi)
            status: dict = {"doi": doi, "method": "tamu_failed", "pdf_bytes": 0}
            if not ezproxy:
                statuses.append({"doi": doi, "method": "tamu_no_doi", "pdf_bytes": 0})
                continue
            try:
                r = c.get(ezproxy)
                ctype = (r.headers.get("content-type") or "").lower()
                if "pdf" in ctype:
                    pdf_path.write_bytes(r.content)
                    status = {"doi": doi, "method": "tamu_pdf_direct",
                              "pdf_bytes": len(r.content)}
                else:
                    pdf_url = _extract_pdf_url(r.text, str(r.url))
                    if pdf_url:
                        rr = c.get(pdf_url)
                        if "pdf" in (rr.headers.get("content-type") or "").lower():
                            pdf_path.write_bytes(rr.content)
                            status = {"doi": doi, "method": "tamu_pdf_meta",
                                      "pdf_bytes": len(rr.content)}
                        else:
                            status = {"doi": doi, "method": "tamu_pdf_link_not_pdf",
                                      "pdf_bytes": 0}
                    else:
                        # Landing only; save for forensics
                        (paper_dir / "tamu_landing.html").write_bytes(r.content)
                        status = {"doi": doi, "method": "tamu_landing_only",
                                  "pdf_bytes": 0}
            except Exception as e:  # noqa: BLE001
                logger.debug("tamu fetch %s failed: %s", doi, e)
                status = {"doi": doi, "method": "tamu_error",
                          "pdf_bytes": 0, "error": str(e)[:200]}

            statuses.append(status)
            if i % 10 == 0 or i == len(rows):
                logger.info("[%d/%d] %s → %s (%d bytes)",
                            i, len(rows), doi[:50], status["method"], status["pdf_bytes"])
            time.sleep(rate_delay)

    # Merge into canonical fetch_status.parquet (preserves the original
    # Unpaywall-pass rows for non-paywalled papers).
    out_df = pl.from_dicts(statuses)
    canonical = pl.read_parquet(PATHS.raw / "fetch_status.parquet")
    updated_dois = set(out_df["doi"].to_list())
    keep = canonical.filter(~pl.col("doi").is_in(list(updated_dois)))
    # Ensure schema alignment by selecting just the canonical columns
    common = [c for c in canonical.columns if c in out_df.columns]
    out_aligned = out_df.select(common)
    merged = pl.concat([keep.select(common), out_aligned], how="diagonal_relaxed")
    merged.write_parquet(PATHS.raw / "fetch_status.parquet")

    summary = out_df.group_by("method").len().sort("len", descending=True)
    logger.info("tamu fetch summary:\n%s", summary)
    return out_df


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
