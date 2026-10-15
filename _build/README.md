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
- Study text: `_build/content/study-source.html`, published word for word on `helpdesk-study.html`.
- Explorer data: `_build/data/helpdesk-explorer.json`, made by `_build/extract_explorer.py` from the raw
  study run in the project workspace (the raw answers are not in this repository).
- Every number on the site comes from the October 2026 helpdesk study. Don't add figures without a source.

## Request form

The snapshot form is sent by [Formspree](https://formspree.io/) (free plan) to `hello@recallant.com`.
Its endpoint is `FORM_ACTION` in `_build/build.py`, written into the form's `action`. `assets/js/site.js`
posts JSON to that same address and shows a sent or error state; without JavaScript the form posts there
directly. Submissions also appear in the Formspree dashboard. The hidden `_gotcha` field is Formspree's
honeypot. To change where requests go, change the form's email in Formspree, not the site. Plan and study
links preselect the form's "I'm interested in" choice through their `data-interest` attribute.
(FormSubmit was used briefly in October 2026 and dropped after its activation link failed.)

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
