# Building recallant.com

The site is plain HTML, CSS and a little JavaScript, served by the Cloudflare Free Worker
`recallant-site` at https://recallant.com/. Namecheap remains the domain registrar. Verified
updates to `main` publish through GitHub Actions; pull requests run checks without deployment
credentials. Only the explicit public-file package is uploaded, never the repository root.

## Rebuild the pages

```
python3 _build/build.py
```

This regenerates every `.html` page, `sitemap.xml`, `robots.txt`, `llms.txt` and `favicon.svg` from
`_build/build.py` (standard library only). Edit copy there, never in the generated HTML.

- Styles: `assets/css/site.css`. Behaviour: `assets/js/site.js`. Both are cache-busted by a content hash.
- Fonts: Inter and Geist Mono, self-hosted in `assets/fonts` (SIL Open Font License, see the LICENSE files).
- Study source: `_build/content/study-source.html`, retained unchanged; metric wording clarified when rendering `helpdesk-study.html`.
- Explorer data: `_build/data/helpdesk-explorer.json`, made by `_build/extract_explorer.py` from the raw
  study run in the project workspace (the raw answers are not in this repository).
- Every number on the site comes from the October 2026 helpdesk study. Don't add figures without a source.

## Enquiry journey

`contact.html` provides four deliberate choices: snapshot, pilot, audit and ongoing support.
Each opens the shared Signal & Syllable enquiry desk with an allowlisted Recallant context.
The visitor reviews and explicitly sends there. Server validation, fixed-recipient delivery,
native fallback and retry identity remain in the Signal & Syllable project. This static site
collects no enquiry fields or API keys. Backup: gorripatiprasanth@gmail.com.
The existing hello@recallant.com address remains in the footer. Cloudflare Email Routing now
forwards it to gorripatiprasanth@gmail.com; catch-all stays disabled. The owner confirmed the
single labelled migration test in that Inbox on 30 October 2026. This is inbound forwarding,
not a new outbound business mailbox. The shared enquiry service and its fixed recipient are unchanged.
Formspree is no longer referenced by the site; its account and historical submissions were not deleted.

Four bounded UTM labels can follow same-site page links and the four approved shared enquiry URLs while JavaScript is available. The shared form displays them as optional editable enquiry fields. No cookies, browser storage, full referrer collection or analytics service is added. Without JavaScript, ordinary page navigation cannot preserve these labels. `_build/check_campaign.cjs` checks the real Home → Services → Contact journey, approved destinations and malformed-query exclusions; CI runs it after the site build.

## Source and evidence

`studio_pages.py` authors the homepage and About; `offer_pages.py` authors Services, Plans,
Method, Contact and Privacy. The original study file and explorer JSON remain unchanged.
`evidence_language.py` clarifies automated first-named metric labels at render time, preserves
all data values, and leaves the separately observed manual ChatGPT spot check distinct.
The public figures are dated research evidence, not proof of a customer outcome.
Private overview/handoff files are deliberately outside this public repository.

## Verification and publishing

Run `python _build/build.py` then `python _build/check_site.py` before publishing.
The GitHub workflow runs these checks and checks that generated pages match the sources.
Cloudflare is the production hosting mechanism; no paid plan was added. GitHub Pages is retired.
Inspect all pages at phone/tablet/desktop widths and the enquiry links before an authorised release.

## Active Cloudflare hosting

The owner-approved domain and mail cutover completed on 30 October 2026. The Cloudflare package preserves the 11 documents, `.html` URLs, Google verification file, CNAME, fonts/licences and research/enquiry destinations. Nameservers are `annalise.ns.cloudflare.com` and `mitch.ns.cloudflare.com`; both apex and www are bound to the production Worker. The initial automated release passed at https://github.com/gorriprasanth/recallant-site/actions/runs/41000487766 (57 public checks, zero retries or emails). Domain and mail changes do not authorize fresh research-engine execution or outreach.

`_build/cloudflare/public-files.json` is the exact 29-file public allowlist. `npm run build:cloudflare` writes only those files to ignored `.cloudflare/public`; never upload the repository root. Worker, generator, configuration, lockfile, workflow and verification files stay outside that directory. `_config.yml` retains exclusions for the legacy GitHub Pages recovery build. Do not re-enable Pages or add `.nojekyll` as part of an ordinary release.

The ordinary Python build defaults to `RECALLANT_HOSTING_PROVIDER="GitHub Pages"`. Cloudflare packaging uses the separate `--output` mode with provider `Cloudflare`, without rewriting the tracked root pages. Only its Privacy page differs; all other public bytes must match the root build. The old `--preview` artifact mode is not a hosting package because it omits 404 and adds a fragment.

With Node 22 and Python 3.13:

```text
npm ci --no-audit --no-fund
npm run verify
```

Verification runs the existing evidence/link/campaign checks, validates package/source hashes, rejects private and encoded paths, checks the branded 404 status, and tests the actual local Worker. Its child process receives no deployment credentials, and no enquiry is sent. `cf:dry-run` validates the upload without publishing. Worker-first routing enforces the allowlist and security/cache/no-transform headers. Production HTTP and www requests redirect to HTTPS apex while preserving `.html` paths and query strings; unknown routes stay 404. All production asset responses come from the allowlisted package.

Preview and production are separate Workers. `preview` enables a public workers.dev address with noindex/no-store headers and a disallowing robots response; this is not password protection. The production Worker disables workers.dev and version preview URLs. Custom domains are intentionally absent from configuration: the existing apex and www bindings are managed in the Cloudflare dashboard and preserved by deployment. Do not replace them or alter DNS during routine publishing. There are no form keys, email secrets, analytics bindings or model integrations in this static Worker.

For an authorized preview release to the existing account, deployment commands are:

```text
node _build/cloudflare/preflight.mjs preview
npx --no-install wrangler deploy --env preview
node _build/cloudflare/check_public.mjs --base https://recallant-site-preview.signal-and-syllable.workers.dev --preview
```

Use the exact preview URL returned by deployment. The preflight requires the reviewed `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` in the environment and never prints them. For the initial local operator session only, `node _build/cloudflare/preflight.mjs preview --operator-oauth` permits an already-approved Wrangler OAuth session without opening or copying its credential file. Confirm the intended Wrangler identity first. This exception is rejected in CI.

The GitHub workflow verifies pull requests without secrets. Production deployment requires successful verification, the `production` environment, main-only permissions, both deployment secrets, and repository variable `CLOUDFLARE_DEPLOY_ENABLED=true` (enabled after cutover). The encrypted publishing token permits editing only `recallant-site`, expires 30 October 2027, and cannot manage Signal & Syllable or DNS. Main runs are serialized; preflight also rejects a checked-out revision that is no longer remote main. Public hash/header/private-path checks follow deployment and never send an enquiry. Set the gate to `false` to pause automatic publishing without taking the current site offline.

For an authorized local production release, use `npm run deploy:production`; CI uses the same preflight immediately before Wrangler. `CLOUDFLARE_DEPLOY_ENABLED=true`, a clean committed main checkout and an exact current remote-main match are required. For an explicit local OAuth session, run the production preflight with `--operator-oauth` after `npm run verify`, followed immediately by `npx --no-install wrangler deploy`. Root source/SEO files and the old GitHub Pages configuration are retained for recovery; reactivating old hosting would require an intentional DNS/privacy/mail review.

Relevant platform contracts: [HTML handling](https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/), [Worker-first asset binding](https://developers.cloudflare.com/workers/static-assets/binding/), and [Wrangler environments](https://developers.cloudflare.com/workers/wrangler/configuration/).

## Social images and icons (optional, needs Node and Playwright)

```
NODE_PATH="$(npm root -g)" node _build/render.mjs   # og.png, og-study.png, apple-touch-icon.png
python3 _build/make_ico.py                          # favicon.ico (needs Pillow)
```

The templates are `_build/og/og.html` and `_build/og/og-study.html`.

## Preview copy

```
python3 _build/build.py --preview /path/to/dir
```

writes the pages plus `index-fragment.html`, the body-only form a claude.ai artifact uses as its main page.

## Keep

`CNAME` and `googlef44257636166e7ad.html` (Google Search Console verification) must stay in the root.
`404.html` uses root-absolute links so the branded missing-page response works at any path.
