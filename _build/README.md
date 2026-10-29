# Building recallant.com

The site is plain HTML, CSS and a little JavaScript, served by GitHub Pages from the root of `main`
(custom domain in `CNAME`). Every push to `main` goes live. Jekyll skips folders that start with an
underscore, so nothing in `_build/` is published.

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
The existing hello@recallant.com forwarding address remains in the footer; no DNS/mail records changed.
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
The existing GitHub Pages branch deployment remains the hosting mechanism; no paid plan was added.
Inspect all pages at phone/tablet/desktop widths and the enquiry links before an authorised release.

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
`404.html` uses root-absolute links because GitHub Pages serves it at any missing path.
