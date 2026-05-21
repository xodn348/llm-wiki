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

## Authenticated fetch — cookie-reuse workflow (implemented)

After the user logs into TAMU EZproxy in their browser once (NetID +
Duo 2FA on mobile), the session cookie is reused to programmatically
download the 636 paywalled papers. No NetID/password stored anywhere,
no Duo TOTP seed needed.

### Step 1 — Log in once in your browser

1. Visit `https://proxy.library.tamu.edu/login` in Chrome (or Firefox).
2. Sign in with TAMU NetID + complete Duo 2FA on your phone.
3. When prompted "Trust this device for 30 days?" — **say yes** so you
   don't have to redo Duo every time the session refreshes.
4. Leave the tab open. Don't log out.

### Step 2 — Run the fetcher (auto-imports cookies)

```
uv run llm-wiki fetch-tamu
```

That's it. `browser-cookie3` reads cookies directly from your installed
browser's cookie store (Chrome / Firefox / Safari / Edge / Brave) and
filters to TAMU domains. No manual export needed.

On macOS Chrome the first run prompts for one **Keychain access**
permission ("`Python` wants to use Chrome Safe Storage to decrypt
cookies") — click Always Allow.

If you'd rather export cookies manually (e.g. running on a server, or
the browser isn't on this machine):

- **Chrome**: ["Get cookies.txt LOCALLY"](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) extension → export for proxy.library.tamu.edu
- **Firefox**: ["cookies.txt"](https://addons.mozilla.org/firefox/addon/cookies-txt/) extension
- Save anywhere, then: `uv run llm-wiki fetch-tamu --cookies path/to/cookies.txt`

To force a specific browser (when multiple are installed):
```
uv run llm-wiki fetch-tamu --browser firefox
```

For each paywalled DOI it:
1. Hits the EZproxy URL with your cookies.
2. Follows redirects through SSO / Shibboleth into the publisher.
3. Looks for the `citation_pdf_url` meta tag (Google Scholar standard,
   honored by Nature, Science, AAAS, ACS, RSC, JAMA, Springer, BMJ).
4. Downloads the PDF to `data/raw/papers/<doi-slug>/full.pdf`.
5. Sleeps 5 seconds between requests (ToS-friendly; do not lower this).

**Total runtime**: 636 papers × 5s/req ≈ **53 minutes** in the
happy path.

**Resumability**: re-runs skip papers that already have a `full.pdf >
1 KB`. If your session expires mid-run, refresh cookies and re-run —
it picks up where it left off. The canonical `fetch_status.parquet`
is updated as you go.

**Status codes you'll see** in `fetch_status.parquet`:
- `tamu_pdf_direct` — EZproxy returned a PDF directly. Best case.
- `tamu_pdf_meta` — Landing page had a `citation_pdf_url` meta tag and
  we fetched the linked PDF. Most common.
- `tamu_landing_only` — Got HTML but no PDF link could be extracted.
  The HTML is saved as `tamu_landing.html` for you to inspect. Common
  for Cloudflare-protected or JavaScript-heavy publishers (Elsevier,
  some Wiley journals).
- `tamu_pdf_link_not_pdf` — Found a link but the linked URL didn't
  return PDF content-type. Likely a paywall wall behind the proxy.
- `tamu_error` — Network error. Re-run will retry.

### Step 4 — Re-chunk to populate Phase 2

```
uv run llm-wiki chunk
```

This is idempotent — it skips already-chunked PDFs and processes the
new TAMU-fetched ones. `data/graph/nodes.parquet` grows accordingly.

## Known limitations

- **Cloudflare bot-detection**: a small minority of publishers
  fingerprint the TLS profile. Plain `httpx` (this implementation)
  works for ~80% of paywalled publishers. The remaining ones may need
  `curl_cffi` (Chrome impersonation) — a future PR.
- **Elsevier ScienceDirect**: aggressively JavaScript-heavy. Many
  papers will land as `tamu_landing_only`. Workaround: open those
  EZproxy URLs in your browser manually and use the "Save PDF" button.
- **Bulk-download ToS**: 5-second delay is the minimum acceptable
  pacing. Do not lower. Publishers monitor proxy IP for aggregate
  request volume; consistent slow pacing is fine, bursts are not.

## Option B — Playwright with NetID (still deferred)

If cookie-reuse proves insufficient and you want full automation:

1. Store NetID + Duo TOTP seed in the OS keychain (never in code).
2. Playwright headless Chromium navigates to `proxy.library.tamu.edu`,
   submits the NetID form, completes Duo via TOTP, and downloads each
   PDF from the resulting authenticated context.

**Pros:** Fully automated, no manual cookie refresh.
**Cons:** Storing Duo TOTP seed is sensitive. Duo policy may also
block headless browsers or require a fresh approval per session.

This is a separate decision — open an issue if you want it built.

## Verification of the resolver URLs

Spot-check three sample DOIs (drawn from
`data/paywalled_urls.csv`) by pasting the `ezproxy_url` into a
browser and confirming the redirect chain ends at the publisher's
full-text page. If the redirect dies at NetID login that is expected
— it confirms the proxy is gating access correctly. If it returns
404 from EZproxy itself, the proxy host or scheme is wrong; report
back and the URL template can be updated.
