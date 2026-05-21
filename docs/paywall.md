# Paywalled paper access via TAMU institutional subscriptions

After the open-access fetch pass (Unpaywall + OpenAlex), **636 of 848
Fleming-tier papers** remain behind publisher paywalls:

| `fetch_status.method` | Count |
|------------------------|-------|
| `oa_pdf`               | 129   |
| `oa_html`              | 83    |
| `no_open_url`          | 495   |
| `failed`               | 141   |

The remaining 636 (`no_open_url` + `failed`) need an authenticated path.
Texas A&M University Libraries holds active subscriptions to the major
journal aggregators (Nature group, Science/AAAS, Cell Press/Elsevier
ScienceDirect, Wiley, Springer Nature, IEEE Xplore, ACM DL, ACS, RSC,
JSTOR, ProQuest), so the user — an authorized TAMU patron — can reach
the PDFs through three institutional gateways.

This module (`src/llm_wiki/paywall_tamu.py`) generates browser-clickable
URLs for each of those gateways. The user clicks; the publisher serves;
the user saves locally. No DRM is circumvented, no scraping of licensed
content takes place, and no programmatic auth is attempted in this pass.

## Three resolver mechanisms

### 1. EZproxy (primary — most reliable)

TAMU operates a standard OCLC EZproxy server at:

```
https://proxy.library.tamu.edu/login?url=<encoded-target>
```

This is the canonical off-campus access route, advertised on the TAMU
Libraries help pages and embedded across the libraries' database
links. EZproxy intercepts the request, authenticates the patron via
TAMU NetID (SSO / CAS), then rewrites the destination's URLs so
subsequent links route back through the proxy.

**Example produced by `resolve_via_ezproxy`:**

```
https://proxy.library.tamu.edu/login?url=https%3A%2F%2Fdoi.org%2F10.1038%2Fnature14539
```

The user opens this in any browser → NetID login (if not cached) →
DOI redirects to publisher → publisher recognizes the proxied IP and
serves the licensed PDF.

**Auth required:** TAMU NetID (Duo MFA). Cookie persists ~8 hours.

**Downstream HTTP behavior:** typically a 3–5 hop redirect chain:
`proxy.library.tamu.edu` → CAS SSO (if no cookie) → `doi.org` →
publisher landing → publisher PDF (often through the proxy host).

### 2. OpenURL (secondary — best-effort)

TAMU uses the Ex Libris Alma/Primo discovery stack. Primo accepts
NISO Z39.88-2004 OpenURL queries at its discovery layer. The exact
hostname for a dedicated SFX/360Link resolver is not publicly
advertised by the libraries, so the module targets the discovery
endpoint as the safest bet:

```
https://search.library.tamu.edu/discovery/openurl
  ?url_ver=Z39.88-2004
  &rft_id=info:doi/<doi>
  &rfr_id=info:sid/llm-wiki
  &svc.fulltext=yes
  &institution=01TAMUS_TAMU
  &rft.date=<year>
  &rft.atitle=<title>
```

If TAMU's Primo configuration recognises the OpenURL, it will surface
the publisher's full-text link (and the patron clicks through with
their NetID session). If not, this resolves to the discovery search
result for the DOI, which still lets the patron find the holdings.

**Auth required:** NetID (same as EZproxy; cookie shared).

### 3. LibKey (tertiary — fastest when it works)

Third Iron's LibKey services (BrowZine, LibKey Nomad, LibKey
Discovery) provide one-click DOI → PDF resolution against the
patron's home institution. TAMU's specific LibKey library slug
(`libkey.io/libraries/<slug>/articles/<doi>`) is not publicly
documented, so the module emits the generic article resolver:

```
https://libkey.io/<doi>
```

This works if the user has the **LibKey Nomad** browser extension
installed (it injects TAMU as the home institution) OR is on the TAMU
campus IP range. Otherwise it falls back to LibKey's open-access
resolver.

### Federated login (Shibboleth)

Many publishers also accept direct Shibboleth federated login —
"Login via institution" → search "Texas A&M" → NetID SSO. The module
does not generate per-publisher Shibboleth URLs (too many publishers,
no stable pattern), but the user can fall back to this manually for
sites where EZproxy struggles (notably some Elsevier ScienceDirect
flows).

## Legality / Terms of Service

This is **authorized institutional access by a current TAMU patron
for personal research use** — exactly what the libraries' subscription
contracts grant. The module:

- Does **not** scrape, decrypt, or circumvent any access control.
- Does **not** redistribute the downloaded PDFs.
- Does **not** automate large-volume downloads (a typical publisher
  ToS red flag — most subscriber agreements prohibit "systematic
  downloading"). The PDFs are clicked one at a time by the human
  patron after NetID login.

**Top caveat for the user:** even though access is authorized,
**publisher Terms of Service prohibit "systematic" or "bulk"
downloading.** Clicking 636 links manually over several sessions is
fine; running a script that hits 636 publisher endpoints in 10
minutes will trip rate limits and may get the TAMU proxy's IP block
flagged by Elsevier / ACS / Wiley. Pace any future automated fetcher
to <1 request / 5 seconds and rotate which publishers are hit.

## How to use (today, manual)

```bash
uv run llm-wiki paywall
# wrote 636 rows to data/paywalled_urls.csv
```

CSV columns: `doi, title, year, venue, ezproxy_url, openurl, libkey_url`.

Open `data/paywalled_urls.csv` in a spreadsheet, sort by venue (so
you batch one publisher at a time and only NetID-auth once per
publisher session), and click the `ezproxy_url` column. Save PDFs
into `data/raw/papers/<doi-slug>/full.pdf` to match the layout
`paper_fetcher.py` expects.

## Future work (deferred)

Two paths exist for programmatic authenticated fetching. Both are
out of scope for this PR — they require security/privacy decisions
the user has not yet made.

### Option A: Browser session cookie reuse

1. User logs into `proxy.library.tamu.edu` in Chrome.
2. Export the `ezproxy` cookie (e.g., via the `browser-cookie3`
   Python library or a manual export).
3. Inject the cookie into an `httpx.Client` and replay each
   `ezproxy_url`.

**Pros:** No credentials stored anywhere; cookie expires in hours.
**Cons:** Manual cookie refresh every session. Some publishers
fingerprint the User-Agent / TLS profile — `curl_cffi` may be
needed for Cloudflare-fronted sites.

### Option B: Playwright with NetID credentials

1. Store NetID + Duo TOTP seed in the OS keychain (never in code).
2. Playwright headless Chromium navigates to `proxy.library.tamu.edu`,
   submits the NetID form, completes Duo via TOTP, and downloads each
   PDF from the resulting authenticated context.

**Pros:** Fully automated.
**Cons:** Storing Duo TOTP seed is sensitive (the user must decide
whether to permit it). Duo policy may also block headless browsers
or require a fresh approval per session. Rate-limit aggressively to
stay under publisher "systematic download" thresholds.

A future PR can implement Option A (lower risk, no credential storage)
as `src/llm_wiki/paywall_fetcher.py`, reading cookies from a
user-provided `.cookies.json` or browser export.

## Verification of the resolver URLs

Spot-check three sample DOIs (drawn from
`data/paywalled_urls.csv`) by pasting the `ezproxy_url` into a
browser and confirming the redirect chain ends at the publisher's
full-text page. If the redirect dies at NetID login that is expected
— it confirms the proxy is gating access correctly. If it returns
404 from EZproxy itself, the proxy host or scheme is wrong; report
back and the URL template can be updated.
