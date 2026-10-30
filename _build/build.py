#!/usr/bin/env python3
"""Generate the Recallant website (https://recallant.com) from this one file.

Usage, from the repository root:
    python3 _build/build.py                  # write the site into the repository root
    python3 _build/build.py --preview DIR    # write a copy for a claude.ai artifact preview

Standard library only. GitHub Pages publishes the root of `main`; Jekyll skips folders
that start with an underscore, so nothing in _build/ is served.

Every number on the site comes from the October 2026 helpdesk study (220 Perplexity
answers, collected 6 Oct 2026). Per-question data for the explorer lives in
_build/data/helpdesk-explorer.json (see extract_explorer.py); the study text lives in
_build/content/study-source.html and is published word for word.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "_build"

SITE = "https://recallant.com"
HOSTING_PROVIDER = os.environ.get("RECALLANT_HOSTING_PROVIDER", "GitHub Pages")
if HOSTING_PROVIDER not in {"GitHub Pages", "Cloudflare"}:
    raise ValueError("RECALLANT_HOSTING_PROVIDER must be GitHub Pages or Cloudflare")
EMAIL = "hello@recallant.com"
LINKEDIN = "https://www.linkedin.com/in/prasanth-s-44805b209/"
UPDATED = "2026-10-29"
ORG_ID = f"{SITE}/#org"
PERSON_ID = f"{SITE}/about.html#prasanth"

NAV = [("services.html", "Services"), ("plans.html", "Plans"),
       ("research.html", "Research"), ("method.html", "Method"), ("about.html", "About")]


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def asset_version() -> str:
    h = hashlib.sha256()
    for p in ("assets/css/site.css", "assets/js/site.js"):
        h.update((ROOT / p).read_bytes())
    return h.hexdigest()[:10]


# ------------------------------------------------------------------ icons and the mark

_ICON_PATHS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 8V6.5A2.5 2.5 0 0 0 13.5 4h-7A2.5 2.5 0 0 0 4 6.5v7A2.5 2.5 0 0 0 6.5 16H8"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6l7-3z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
    "loop": '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 3.5V8h4.5"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 20.5V16h-4.5"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    "chart": '<path d="M4 20h16"/><path d="M7 16v-5M12 16V6M17 16v-8"/>',
    "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 17h5"/>',
    "megaphone": '<path d="M4 10v4a1 1 0 0 0 1 1h2l6 4V5L7 9H5a1 1 0 0 0-1 1z"/><path d="M16.5 9a3.5 3.5 0 0 1 0 6M19 6.5a7 7 0 0 1 0 11"/>',
    "browser": '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9h18M6.5 6.6h.01M9.2 6.6h.01"/>',
    "ribbon": '<circle cx="12" cy="9" r="5.5"/><path d="M8.6 13.4L7.5 21l4.5-2.5 4.5 2.5-1.1-7.6"/>',
    "scale": '<path d="M12 4v16M7 20h10M5 7h14"/><path d="M5 7l-3 6.5a3.2 3.2 0 0 0 6 0L5 7zM19 7l-3 6.5a3.2 3.2 0 0 0 6 0L19 7z"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6h.01"/>',
    "page": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M4 7.5l8 5.5 8-5.5"/>',
    "external": '<path d="M7 17L17 7M9 7h8v8"/>',
    "spark": '<path d="M12 3.5l1.9 5 5 1.9-5 1.9-1.9 5-1.9-5-5-1.9 5-1.9z"/>',
}


def icon(name: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            f'{_ICON_PATHS[name]}</svg>')


# Inter Bold "R" (opsz 32), in font units: x 111-1286, cap height 1490, y up.
R_FONT_PATH = (
    "M111.28 0V1490H707.48Q875.36 1490 997.77 1430.41Q1120.18 1370.82 1186.54 1261.22Q1252.9 1151.62 "
    "1252.9 1001.28Q1252.9 853.64 1183.08 745.7Q1113.26 637.76 986.81 579.25Q860.36 520.74 689.16 520.74"
    "H295.52V768.22H688.9Q770.3 768.22 829.14 796.97Q887.98 825.72 919.88 878.22Q951.78 930.72 951.78 "
    "1001.28Q951.78 1072.84 919.65 1124.61Q887.52 1176.38 828.68 1205.13Q769.84 1233.88 687.98 1233.88"
    "H418.72V0ZM955.6 0 615.04 673.24H938.38L1286.02 0Z")


def r_path(cap: float = 30.0, left: float = 13.9, base: float = 46.0) -> str:
    """The R glyph, scaled into the 64-unit mark: cap height `cap`, left edge `left`, baseline `base`."""
    s = cap / 1490.0
    tokens = re.findall(r"[MVHQLZ]|-?\d+(?:\.\d+)?", R_FONT_PATH)
    X = lambda v: f"{left + (float(v) - 111.28) * s:.2f}"
    Y = lambda v: f"{base - float(v) * s:.2f}"
    out, i, cmd = [], 0, ""
    while i < len(tokens):
        t = tokens[i]
        if t in "MVHQLZ":
            cmd = t
            out.append(t)
            i += 1
        elif cmd in ("M", "L"):
            out.append(f"{X(tokens[i])} {Y(tokens[i + 1])}")
            i += 2
        elif cmd == "V":
            out.append(Y(t))
            i += 1
        elif cmd == "H":
            out.append(X(t))
            i += 1
        elif cmd == "Q":
            out.append(f"{X(tokens[i])} {Y(tokens[i + 1])} {X(tokens[i + 2])} {Y(tokens[i + 3])}")
            i += 4
        else:
            raise ValueError(f"unexpected token {t!r}")
    return re.sub(r"([MVHQLZ]) ", r"\1", " ".join(out))


R_D = r_path()
DOT = 'cx="45.6" cy="41.5" r="4.5"'
MARK = (f'<svg class="brand__mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
        f'<rect class="m-bg" width="64" height="64" rx="15"/><path class="m-r" d="{R_D}"/>'
        f'<circle class="m-dot" {DOT}/></svg>')


def favicon_svg(rounded: bool = True) -> str:
    rx = ' rx="15"' if rounded else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<rect width="64" height="64"{rx} fill="#050807"/><path d="{R_D}" fill="#f2f5f3"/>'
            f'<circle {DOT} fill="#5ccaa8"/></svg>\n')


# ------------------------------------------------------------------ small building blocks

def pips(n: int, total: int = 5, extra: str = "") -> str:
    marks = "".join(f'<i class="on" style="--p:{i}"></i>' if i < n else "<i></i>" for i in range(total))
    return f'<span class="pips{extra}" aria-hidden="true">{marks}</span>'


class Sources:
    """Numbered sources for one page, rendered as citation markers and a list at the end."""

    def __init__(self, items):
        self.items = items  # list of (short label, full html)

    def cite(self, n: int) -> str:
        label = esc(self.items[n - 1][0])
        return f'<a class="cite" href="#src-{n}" data-tip="{label}" aria-label="Source {n}: {label}">{n}</a>'

    def band(self) -> str:
        lis = "\n".join(f'        <li id="src-{i}"><span>{i}</span><span>{full}</span></li>'
                        for i, (_, full) in enumerate(self.items, 1))
        return f"""<aside class="sources-band" aria-labelledby="sources-title">
  <div class="wrap">
    <div class="sources">
      <h2 id="sources-title">Sources</h2>
      <ol>
{lis}
      </ol>
    </div>
  </div>
</aside>"""


STUDY_SOURCE = ("Recallant helpdesk study, October 2026",
                'Recallant, <a href="helpdesk-study.html">AI Visibility Study: Helpdesk Software (October 2026)</a>. '
                "44 buyer questions asked 5 times each on Perplexity with live web search; 220 answers collected 6 October 2026.")
SAMPLE_SOURCE = ("Sample snapshot: Freshdesk",
                 'Recallant, <a href="sample-snapshot.html">Sample snapshot: Freshdesk</a>, built from the same study data. '
                 "Freshdesk is not a client.")


# ------------------------------------------------------------------ study data used in charts

SCORECARD = [  # brand, named in %, share of voice %, low, high, top pick %, own site cited %
    ("Freshdesk", 61, 19.0, 15, 23, 21, 13),
    ("Zendesk", 46, 13.8, 10, 18, 25, 14),
    ("Zoho Desk", 39, 12.2, 8, 16, 7, 5),
    ("Help Scout", 25, 7.9, 4, 12, 7, 21),
    ("Intercom", 25, 7.6, 5, 11, 5, 15),
    ("HubSpot Service Hub", 19, 6.1, 3, 9, 0, 14),
    ("Gorgias", 13, 4.1, 1, 7, 4, 2),
    ("Hiver", 13, 4.0, 1, 8, 4, 13),
    ("Tidio", 12, 3.8, 1, 8, 0, 0),
    ("Freshservice", 11, 3.5, 0, 7, 4, 0),
    ("Jira Service Management", 11, 3.5, 1, 7, 0, 2),
    ("Front", 11, 3.4, 1, 5, 0, 3),
]
SC = {row[0]: row for row in SCORECARD}

CITED_SITES = [  # domain, answers citing it (of 220), what it is
    ("g2.com", 56, "Review marketplace"),
    ("getmacha.com", 40, "Vendor blog (comparisons)"),
    ("kayako.com", 31, "Rival helpdesk's blog"),
    ("cloudtalk.io", 25, "Vendor blog (listicles)"),
    ("eesel.ai", 25, "Vendor blog"),
    ("rework.com", 21, "Software guides"),
    ("ringly.io", 18, "Vendor blog (alternatives lists)"),
    ("helpdesk.com", 16, "Vendor blog (listicles)"),
    ("capterra.com", 14, "Review marketplace"),
]

EXPLORER = json.loads((HERE / "data" / "helpdesk-explorer.json").read_text(encoding="utf-8"))
EX_BY_ID = {q["id"]: q for q in EXPLORER}
HOME_QUESTIONS = ["d02", "d01", "d05", "d09", "d13", "p05"]
CAT_ORDER = ["Best for", "Alternatives", "Comparisons", "How-to"]


def short_brand(name: str) -> str:
    return "HubSpot" if name == "HubSpot Service Hub" else name


# ------------------------------------------------------------------ charts (static HTML, no script needed)

def sov_panel(n: int = 5, title: str = "Share of voice", meta: str = "Helpdesk software · Perplexity · Oct 2026",
              note: str = "Bars show each brand’s share of all brand mentions. Whiskers show 95% ranges.") -> str:
    top = 25.0
    rows = []
    for name, _, sov, lo, hi, _, _ in SCORECARD[:n]:
        rows.append(
            f'<div class="sov__row"><span class="sov__name" title="{esc(name)}">{esc(short_brand(name))}</span>'
            f'<span class="sov__track"><span class="sov__bar" style="width:{sov / top * 100:.1f}%"></span>'
            f'<span class="sov__range" style="left:{lo / top * 100:.1f}%;width:{(hi - lo) / top * 100:.1f}%"></span></span>'
            f'<span class="sov__val">{sov:.1f}%</span></div>')
    return f"""<div class="viz-panel" role="img" aria-label="{esc(title)}: {esc(', '.join(f'{short_brand(r[0])} {r[2]:.1f}%' for r in SCORECARD[:n]))}">
  <div class="viz-panel__head"><span class="viz-panel__title">{esc(title)}</span><span class="viz-panel__meta">{esc(meta)}</span></div>
  <div class="sov">{''.join(rows)}</div>
  <p class="viz-note">{note}</p>
</div>"""


def minibars(n: int = 3, title: str = "Sites AI cites most", meta: str = "answers out of 220") -> str:
    top = CITED_SITES[0][1]
    rows = "".join(
        f'<div class="minibars__row"><span>{esc(d)}</span><span class="num">{c}</span>'
        f'<i><b style="width:{c / top * 100:.1f}%"></b></i></div>' for d, c, _ in CITED_SITES[:n])
    label = ", ".join(f"{d} {c}" for d, c, _ in CITED_SITES[:n])
    return f"""<div class="viz-panel" role="img" aria-label="{esc(title)}, {esc(meta)}: {esc(label)}">
  <div class="viz-panel__head"><span class="viz-panel__title">{esc(title)}</span><span class="viz-panel__meta">{esc(meta)}</span></div>
  <div class="minibars">{rows}</div>
</div>"""


def dumbbell(src: Sources) -> str:
    groups = [
        ("Chosen more often than cited", ["Zendesk", "Freshdesk", "Zoho Desk", "Gorgias"]),
        ("Cited more often than chosen", ["Help Scout", "Intercom", "HubSpot Service Hub", "Hiver"]),
    ]
    top = 30.0
    grid = "".join(f'<i style="left:{t / top * 100:.0f}%"></i>' for t in (0, 10, 20, 30))
    out = []
    for gname, brands in groups:
        out.append(f'<div class="db__group">{esc(gname)}</div>')
        for b in brands:
            _, _, _, _, _, first, cited = SC[b]
            lo, hi = sorted((first, cited))
            label = short_brand(b)
            show = b == "Help Scout"
            vals = (f'<span class="db__val" style="left:{cited / top * 100:.1f}%">{cited}%</span>'
                    f'<span class="db__val" style="left:{first / top * 100:.1f}%">{first}%</span>') if show else ""
            out.append(
                f'<div class="db__row"><span class="db__label" title="{esc(b)}">{esc(label)}</span>'
                f'<span class="db__track"><span class="db__grid">{grid}</span>'
                f'<span class="db__line" style="left:{lo / top * 100:.1f}%;width:{(hi - lo) / top * 100:.1f}%"></span>'
                f'<span class="db__dot db__dot--cited" style="left:{cited / top * 100:.1f}%" tabindex="0" '
                f'data-tip="{esc(b)}|Own site cited in {cited}% of answers"></span>'
                f'<span class="db__dot db__dot--first" style="left:{first / top * 100:.1f}%" tabindex="0" '
                f'data-tip="{esc(b)}|Recommended first in {first}% of answers"></span>{vals}</span></div>')
    ticks = "".join(f'<span style="left:{t / top * 100:.0f}%">{t}%</span>' for t in (0, 10, 20, 30))
    rows = "".join(f"<tr><td>{esc(b)}</td><td class=\"num\">{SC[b][6]}%</td><td class=\"num\">{SC[b][5]}%</td></tr>"
                   for _, bs in groups for b in bs)
    return f"""<figure class="chart-card" aria-labelledby="db-title">
  <div class="chart-card__head">
    <div>
      <h3 class="chart-card__title" id="db-title">Own site cited vs recommended first</h3>
      <p class="chart-card__sub">Share of Perplexity answers to 40 non-branded buyer questions.{src.cite(1)}</p>
    </div>
    <div class="legend" aria-hidden="true"><span><i class="key-dot key-dot--cited"></i>Own site cited</span><span><i class="key-dot key-dot--first"></i>Recommended first</span></div>
  </div>
  <div class="db" data-chart>
    {''.join(out)}
    <div class="db__axis" aria-hidden="true"><span></span><span class="db__ticks">{ticks}</span></div>
  </div>
  <details class="numbers">
    <summary>Show the numbers</summary>
    <div class="table-wrap"><table>
      <thead><tr><th>Brand</th><th class="num">Own site cited</th><th class="num">Recommended first</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
  </details>
</figure>"""


def range_chart() -> str:
    top = 25.0
    grid = "".join(f'<i style="left:{t / top * 100:.0f}%"></i>' for t in (0, 5, 10, 15, 20, 25))
    rows = []
    for name, _, sov, lo, hi, _, _ in SCORECARD:
        focus = " is-focus" if name == "Freshdesk" else ""
        rows.append(
            f'<div class="rangechart__row{focus}"><span class="rangechart__name" title="{esc(name)}">{esc(name)}</span>'
            f'<span class="rangechart__track"><span class="rangechart__grid">{grid}</span>'
            f'<span class="rangechart__range" style="left:{lo / top * 100:.1f}%;width:{(hi - lo) / top * 100:.1f}%"></span>'
            f'<span class="rangechart__dot" style="left:{sov / top * 100:.1f}%" tabindex="0" '
            f'data-tip="{esc(name)}|{sov:.1f}% share of voice (95% range {lo}%–{hi}%)"></span></span>'
            f'<span class="rangechart__val">{sov:.1f}%</span></div>')
    ticks = "".join(f'<span style="left:{t / top * 100:.0f}%">{t}%</span>' for t in (0, 5, 10, 15, 20, 25))
    return f"""<figure class="chart-card" aria-labelledby="rc-title">
  <div class="chart-card__head">
    <div>
      <h3 class="chart-card__title" id="rc-title">Share of voice, with 95% ranges</h3>
      <p class="chart-card__sub">The 12 brands in the scorecard below. Overlapping ranges mean the order is not certain.</p>
    </div>
    <div class="legend" aria-hidden="true"><span><i class="key-dot key-dot--first"></i>Share of voice</span><span><i class="key-range"></i>95% range</span></div>
  </div>
  <div class="rangechart" data-chart aria-hidden="true">
    {''.join(rows)}
    <div class="rangechart__axis"><span></span><span class="db__ticks">{ticks}</span><span></span></div>
  </div>
</figure>"""


def cited_sites_chart() -> str:
    top = 60.0
    rows = []
    for d, c, kind in CITED_SITES:
        review = " is-review" if kind == "Review marketplace" else ""
        rows.append(f'<div class="hbars__row"><span class="hbars__name">{esc(d)}</span>'
                    f'<span class="hbars__track"><span class="hbars__bar{review}" style="width:{c / top * 100:.1f}%"></span>'
                    f'<span class="hbars__val">{c}</span></span></div>')
    return f"""<figure class="chart-card" aria-labelledby="cs-title">
  <div class="chart-card__head">
    <div>
      <h3 class="chart-card__title" id="cs-title">Third-party sites cited most</h3>
      <p class="chart-card__sub">Answers citing each site, out of 220. The table below has the same numbers.</p>
    </div>
    <div class="legend" aria-hidden="true"><span><i class="key-bar"></i>Vendor blogs and guides</span><span><i class="key-bar key-bar--review"></i>Review marketplaces</span></div>
  </div>
  <div class="hbars" aria-hidden="true">{''.join(rows)}</div>
</figure>"""


# ------------------------------------------------------------------ the question explorer

def ex_leader(item) -> str:
    first = item["first"]
    if not first:
        return "No pick"
    top = first[0][1]
    leaders = [b for b, c in first if c == top]
    return leaders[0] if len(leaders) == 1 else "Split"


def ex_result(item) -> str:
    """Server-rendered result; assets/js/site.js renders the same markup on selection."""
    n = item["runs"]
    out = [f'<p class="kicker">{esc(item["cat"])} · {n} runs</p>',
           f'<h3 class="explorer__question">{esc(item["q"])}</h3>']
    first, named = item["first"], item["named"]
    if first:
        top = first[0][1]
        leaders = [b for b, c in first if c == top]
        rest = [(b, c) for b, c in first if c != top]
        name = leaders[0] if len(leaders) == 1 else ", ".join(leaders[:-1]) + " and " + leaders[-1]
        label = "Recommended first" if len(leaders) == 1 else "Recommended first, split"
        meta = f"{top} of {n} runs" + (" each" if len(leaders) > 1 else "")
        out.append(f'<div class="explorer__first"><div><p class="kicker">{label}</p><strong>{esc(name)}</strong></div>'
                   f'<div class="explorer__firstmeta">{pips(top, n)}<span>{meta}</span></div></div>')
        if rest:
            out.append('<p class="explorer__also">Also first: '
                       + ", ".join(f"{esc(b)} ({c} of {n})" for b, c in rest) + "</p>")
    else:
        if item["cat"] == "Comparisons" and not named:
            msg = "Only the two brands in the question were named"
        elif not named:
            msg = "No helpdesk product was named in any answer"
        else:
            msg = "No single brand was recommended first"
        out.append(f'<div class="explorer__first is-none"><div><p class="kicker">Recommended first</p>'
                   f'<strong>{msg}</strong></div></div>')

    def rows(pairs, empty):
        if not pairs:
            return f'<ul class="rowlist"><li class="empty">{empty}</li></ul>'
        return '<ul class="rowlist">' + "".join(
            f'<li><span class="nm">{esc(a)}</span>{pips(c, n, " pips--sm")}<span class="num">{c}/{n}</span></li>'
            for a, c in pairs) + "</ul>"

    empty_named = "None besides the two in the question" if item["cat"] == "Comparisons" else "None"
    out.append('<div class="explorer__cols">'
               f'<div class="explorer__col"><h4 class="kicker">Named in the answers</h4>{rows(named, empty_named)}</div>'
               f'<div class="explorer__col"><h4 class="kicker">Sources cited most</h4>{rows(item["sources"], "None")}</div>'
               '</div>')
    return "".join(out)


def explorer(ids, key: str, tabs: bool, foot_extra: str = "", more: str = "") -> str:
    items = [EX_BY_ID[i] for i in ids]
    first = items[0]
    tab_html = ""
    if tabs:
        counts = {c: sum(1 for q in items if q["cat"] == c) for c in CAT_ORDER}
        tab_html = ('<div class="explorer__tabs" role="group" aria-label="Question groups">' + "".join(
            f'<button class="explorer__tab" type="button" data-cat="{esc(c)}" '
            f'aria-pressed="{"true" if c == first["cat"] else "false"}">{esc(c)} <span class="dim">{counts[c]}</span></button>'
            for c in CAT_ORDER if counts[c]) + "</div>")
    opts = []
    for c in CAT_ORDER:
        group = [q for q in items if q["cat"] == c]
        if not group:
            continue
        o = "".join(f'<option value="{q["id"]}"{" selected" if q is first else ""}>{esc(q["q"])}</option>' for q in group)
        opts.append(f'<optgroup label="{esc(c)}">{o}</optgroup>' if tabs else o)
    lis = "".join(
        f'<li{" hidden" if tabs and q["cat"] != first["cat"] else ""} data-cat="{esc(q["cat"])}">'
        f'<button class="explorer__q" type="button" data-id="{q["id"]}" aria-pressed="{"true" if q is first else "false"}">'
        f'<span>{esc(q["q"])}</span><span class="explorer__lead">{esc(ex_leader(q))}</span></button></li>' for q in items)
    data = json.dumps(items, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    foot = ("Perplexity with live web search, 6 October 2026. Counts are runs out of 5. "
            "Brands named in the question are left out, as in the study." + foot_extra)
    fallback = "".join(f'<details><summary>{esc(q["q"])}</summary>{ex_result(q)}</details>' for q in items[1:])
    return f"""<div class="explorer" data-explorer="{key}">
  <div class="explorer__list">
    {tab_html}
    <label class="sr-only" for="ex-select-{key}">Choose a question</label>
    <select id="ex-select-{key}" data-ex-select>{''.join(opts)}</select>
    <ul class="explorer__qs" data-ex-list>{lis}</ul>
    {more}
  </div>
  <div class="explorer__result" data-ex-result aria-live="polite">{ex_result(first)}<p class="explorer__foot">{foot}</p></div>
</div>
<noscript><div class="explorer-fallback"><h3>More questions from the study</h3>{fallback}</div></noscript>
<script type="application/json" id="ex-data-{key}">{data}</script>"""


# ------------------------------------------------------------------ chrome: nav, menu, call to action, footer

def nav(current: str, tone: str) -> str:
    links = "\n".join(
        f'      <a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}>{label}</a>'
        for h, label in NAV)
    menu = "\n".join(f'    <a class="menu__link" style="--i:{i}" href="{h}">{label}</a>'
                     for i, (h, label) in enumerate([("./", "Home")] + NAV))
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="nav" id="nav" data-tone="{tone}">
  <div class="wrap nav__inner">
    <a class="brand" href="./" aria-label="Recallant home">{MARK}<span>Recallant</span></a>
    <nav class="nav__links" aria-label="Main">
{links}
    </nav>
    <div class="nav__cta">
      <a class="btn btn--signal btn--sm" href="contact.html">Start an enquiry</a>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" hidden>
  <nav aria-label="Mobile">
{menu}
  </nav>
  <a class="btn btn--signal" href="contact.html">Start an enquiry</a>
  <p class="menu__note">Or email <a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>"""


def cta_band(title="Find your next useful step.", lede="Tell us about your product and the buyer question that matters.", interests=None):
    return f'''<section class="band band--night" id="get-snapshot" aria-labelledby="cta-title"><div class="wrap closing-cta"><div><p class="eyebrow">Start a conversation</p><h2 class="h2" id="cta-title">Find your next useful step.</h2><p class="lede">Start with a snapshot request, a focused pilot, or a scoped audit. We will confirm the right fit before work begins.</p></div><div><a class="btn btn--signal" href="contact.html">Choose your enquiry {icon('arrow')}</a><p class="closing-note">Enquiries are reviewed through our shared Signal &amp; Syllable desk.</p></div></div></section>'''


FOOTER = f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="./" aria-label="Recallant home">{MARK}<span>Recallant</span></a>
        <p>AI search visibility for B2B brands.</p><p>A specialist product from <a href="https://signalandsyllable.com/">Signal &amp; Syllable ↗</a></p>
      </div>
      <nav aria-labelledby="f-explore">
        <h2 id="f-explore">Explore</h2>
        <ul><li><a href="services.html">Services</a></li><li><a href="plans.html">Plans</a></li><li><a href="research.html">Research</a></li><li><a href="method.html">Method</a></li><li><a href="about.html">About</a></li></ul>
      </nav>
      <nav aria-labelledby="f-research">
        <h2 id="f-research">Research</h2>
        <ul><li><a href="helpdesk-study.html">Helpdesk study</a></li><li><a href="sample-snapshot.html">Sample snapshot</a></li><li><a href="contact.html#snapshot">Free snapshot</a></li></ul>
      </nav>
      <nav aria-labelledby="f-contact">
        <h2 id="f-contact">Contact</h2>
        <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li></ul>
      </nav>
    </div>
    <div class="footer__base">
      <span>© 2026 Recallant. <a href="privacy.html">Privacy</a> · <a href="contact.html">Contact</a></span>
      <span class="footer__promise">{icon('shield')}We never buy reviews, links or mentions.</span>
    </div>
  </div>
</footer>"""


# ------------------------------------------------------------------ page shell

def breadcrumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": name, "item": url}
        for i, (name, url) in enumerate([("Home", SITE + "/")] + items, 1)]}


ORG = {
    "@type": "Organization", "@id": ORG_ID, "name": "Recallant", "url": SITE + "/",
    "logo": SITE + "/apple-touch-icon.png", "email": EMAIL,
    "description": "AI search visibility research and focused website improvements for B2B software brands, with platform and question scope agreed for each project.",
    "founder": {"@id": PERSON_ID},
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
    "areaServed": "Worldwide",
}
PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": "Prasanth G", "jobTitle": "Founder",
    "worksFor": {"@id": ORG_ID}, "url": SITE + "/about.html",
    "image": SITE + "/assets/img/prasanth-640.jpg", "sameAs": [LINKEDIN],
    "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
}

PAGES: dict[str, str] = {}


def page(*, file: str, title: str, desc: str, body: str, current: str = "", tone: str = "paper",
         graph=None, og_image: str = "og.png", og_alt: str = "Recallant: Be the answer.",
         og_type: str = "website", noindex: bool = False, sources: Sources | None = None) -> None:
    canonical = SITE + "/" + ("" if file == "index.html" else file)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph or []}, ensure_ascii=False, indent=1)
    robots = "noindex" if noindex else "index, follow, max-image-preview:large"
    theme = "#050807" if tone == "night" else "#ffffff"
    v = asset_version()
    doc = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Recallant">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{theme}">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/inter-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css?v={v}">
<script src="assets/js/site.js?v={v}" defer></script>
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{nav(current, tone)}
<main id="main">
{body}
{cta_band_for.get(file, cta_band())}
</main>
{sources.band() if sources else ''}
{FOOTER}
</body>
</html>
"""
    from evidence_language import correct_page
    PAGES[file] = correct_page(doc, file)


cta_band_for: dict[str, str] = {}


# ================================================================== RESEARCH

def research() -> None:
    method = [
        ("01", "Fix the questions", "We write the questions buyers ask, in four groups: best-for, alternatives, comparisons and how-to. The set stays the same from month to month."),
        ("02", "Ask more than once", "Each question is asked several times, so one lucky or unlucky answer doesn’t decide the result."),
        ("03", "Read every answer", "Every brand mention, first recommendation and cited source is recorded. A brand named in the question is left out of that question’s numbers."),
        ("04", "Show the uncertainty", "Results come with 95% ranges, and we publish the method and its limits."),
    ]
    method_html = "".join(f'<li class="reveal" style="--d:{i * 80}"><h3>{t}</h3><p>{p}</p></li>'
                          for i, (n, t, p) in enumerate(method))
    body = f"""<section class="band band--paper band--first page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow rise">Research</p>
    <h1 class="h-display rise" style="--d:80" id="page-title">What AI actually says.</h1>
    <p class="lede rise" style="--d:160">We publish what we measure, with the method and the limits, so you can judge it for yourself.</p>
  </div>
</section>

<section class="band band--paper band--flush" aria-label="Studies">
  <div class="wrap">
    <article class="feature-study reveal">
      <div class="feature-study__copy">
        <p class="kicker">October 2026 · Helpdesk software</p>
        <h2>Which helpdesks appear, and whose pages are cited?</h2>
        <p>44 buyer questions, 5 runs each, 220 Perplexity answers. Freshdesk is named most, Zendesk is recommended first more often, and the order changes across niche questions.</p>
        <div class="metachips"><span class="metachip">44 questions</span><span class="metachip">5 runs each</span><span class="metachip">220 answers</span><span class="metachip">Perplexity</span></div>
        <div class="ctas">
          <a class="btn btn--signal" href="helpdesk-study.html">Read the study</a>
          <a class="arrow-link" href="helpdesk-study.html#explore">Explore the answers {icon('arrow')}</a>
        </div>
      </div>
      {sov_panel(6, note='Whiskers show 95% ranges.')}
    </article>
    <div class="cards-2 wide">
      <a class="card reveal" href="sample-snapshot.html">
        <p class="kicker">Sample · Inside the report</p>
        <h3>Sample snapshot: Freshdesk</h3>
        <p>An inspectable report format using Freshdesk’s numbers from the public helpdesk study.</p>
        <span class="arrow-link">See the sample {icon('arrow')}</span>
      </a>
      <article class="card reveal" style="--d:80">
        <p class="kicker">October 2026 · IT management software</p>
        <h3>ITSM and MSP tools in AI answers</h3>
        <p>44 ITSM and MSP buyer questions, 220 Perplexity answers. One MSP tool was named in over a third of answers but recommended first in only 1 of 70.</p>
        <a class="arrow-link" href="contact.html#audit">Request the study {icon('arrow')}</a>
      </article>
    </div>
  </div>
</section>

<section class="band band--mist" aria-labelledby="method-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">How we measure</p>
      <h2 class="h2" id="method-title">The same questions, asked many times.</h2>
      <p class="lede">These principles guide the measurement scope agreed for each project.</p>
    </div>
    <ol class="method">{method_html}</ol>
  </div>
</section>"""
    cta_band_for["research.html"] = cta_band("Want your category measured?",
                                             "Start with a free one-page snapshot on 20 questions your buyers ask.",
                                             interests=["IT management study"])
    page(file="research.html", title="Research: AI visibility studies | Recallant",
         desc="Recallant’s published studies of what AI assistants recommend in B2B software categories, with method and limits.",
         body=body, current="research.html", graph=[ORG, breadcrumbs([("Research", SITE + "/research.html")])])


# ================================================================== STUDY

def study() -> None:
    raw = (HERE / "content" / "study-source.html").read_text(encoding="utf-8")
    first_p_end = raw.index("</p>") + 4
    byline = re.sub(r"<[^>]+>", "", raw[:first_p_end]).strip()
    assert byline == "6 October 2026 · Prasanth G, Recallant", byline
    s = raw[first_p_end:].lstrip()
    s = s.replace("<p>", '<p class="lead">', 1)
    s = re.sub(r'<tr class="(?:header|odd|even)">', "<tr>", s)
    s = s.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    s = s.replace('<a\nhref="http', '<a rel="noopener" href="http').replace('<a href="http', '<a rel="noopener" href="http')

    # Charts use the preserved table values; evidence_language clarifies metric labels.
    anchor = "with the highest share of voice, across 40 non-branded questions:</p>"
    assert anchor in s
    s = s.replace(anchor, anchor + "\n" + range_chart(), 1)
    anchor = "them out of 220:</p>"
    assert anchor in s
    s = s.replace(anchor, anchor + "\n" + cited_sites_chart(), 1)

    # The explorer goes before the appendix.
    explore = f"""<h2 id="explore">Explore the answers</h2>
<p>Every non-branded question in the study, with who Perplexity recommended first, who it named and which sources it cited most, run by run.</p>
<div class="explore-embed">{explorer([q["id"] for q in EXPLORER], "study", tabs=True)}</div>
"""
    anchor = '<h2 id="appendix-the-44-questions">'
    assert anchor in s
    s = s.replace(anchor, explore + anchor, 1)

    toc_items = [
        ("scorecard", "Scorecard"),
        ("where-freshdesk-wins-and-where-it-is-missing", "Where Freshdesk wins"),
        ("who-gets-cited", "Who gets cited"),
        ("what-this-means", "What this means"),
        ("spot-check-chatgpt-app", "ChatGPT spot check"),
        ("how-it-was-measured-and-its-limits", "Method and limits"),
        ("explore", "Explore the answers"),
        ("appendix-the-44-questions", "The 44 questions"),
    ]
    for anchor_id, _ in toc_items:
        assert f'id="{anchor_id}"' in s, anchor_id
    toc = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc_items)

    facts = [("44", "buyer questions"), ("5", "runs per question"), ("220", "Perplexity answers"),
             ("23", "brands tracked"), ("~5", "sources cited per answer")]
    facts_html = "".join(f"<div><strong>{n}</strong><span>{t}</span></div>" for n, t in facts)

    body = f"""<div class="progress" aria-hidden="true" data-progress></div>
<section class="band band--night band--first article-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow rise"><a href="research.html">Research</a> · Helpdesk software</p>
    <h1 class="rise" style="--d:80" id="page-title">AI Visibility Study: Helpdesk Software (October 2026)</h1>
    <p class="byline rise" style="--d:160"><img src="assets/img/prasanth-640.jpg" alt="" width="34" height="34"><span><b>Prasanth G</b>, Recallant · 6 October 2026</span></p>
    <div class="facts rise" style="--d:240">{facts_html}</div>
    <div class="ctas rise" style="--d:300"><a class="arrow-link" href="#explore">Explore the answers {icon('arrow')}</a><a class="arrow-link" href="#how-it-was-measured-and-its-limits">Method and limits {icon('arrow')}</a></div>
  </div>
</section>
<section class="band band--paper band--tight">
  <div class="wrap article-layout">
    <nav class="toc" aria-label="On this page">
      <p class="kicker">On this page</p>
      <ol data-spy>{toc}</ol>
    </nav>
    <article class="prose" data-article>
{s}
    </article>
  </div>
</section>"""
    report = {"@type": "Report", "@id": SITE + "/helpdesk-study.html#report",
              "headline": "AI Visibility Study: Helpdesk Software (October 2026)",
              "description": "Which helpdesk brands Perplexity recommends, and whose pages it cites: 44 buyer questions, 5 runs each, 220 answers, collected 6 October 2026.",
              "datePublished": "2026-10-06", "author": {"@id": PERSON_ID}, "publisher": {"@id": ORG_ID},
              "image": SITE + "/og-study.png", "mainEntityOfPage": SITE + "/helpdesk-study.html", "inLanguage": "en",
              "about": ["AI search visibility", "Helpdesk software", "Perplexity"]}
    cta_band_for["helpdesk-study.html"] = cta_band(
        "Want your brand measured the same way?",
        "Send your product name and get a free one-page snapshot on 20 questions your buyers ask. No call needed.")
    page(file="helpdesk-study.html", title="Helpdesk AI Visibility Study (Oct 2026) | Recallant",
         desc="Which helpdesk brands does Perplexity recommend, and whose pages does it cite? 44 buyer questions, 5 runs each, 220 answers, collected 6 October 2026.",
         body=body, current="research.html", tone="night", og_image="og-study.png",
         og_alt="AI Visibility Study: Helpdesk Software, October 2026", og_type="article",
         graph=[ORG, PERSON, report, breadcrumbs([("Research", SITE + "/research.html"),
                                                  ("Helpdesk study", SITE + "/helpdesk-study.html")])])


# ================================================================== SAMPLE SNAPSHOT

def sample() -> None:
    named = ["Best helpdesk software for a small business", "Best omnichannel support for email, chat and WhatsApp",
             "Best helpdesk for companies in India", "Best helpdesk for a remote support team", "Best Zendesk alternatives"]
    named_html = "".join(f'<li><span>{q}</span><span class="qlist__meta">{pips(5)}<span>First named in 5 of 5</span></span></li>' for q in named)
    missing = [
        ("Best customer service platform for an ecommerce store", "0 of 5", "Gorgias (5 of 5)"),
        ("Best shared inbox tool for customer support", "0 of 5", "Help Scout (5 of 5)"),
        ("Helpdesk with the best AI chatbot", "3 of 5", "Intercom (5 of 5)"),
        ("Replacing a shared Gmail inbox", "2 of 5", "Help Scout (5 of 5)"),
        ("Best support software for a SaaS startup", "5 of 5", "Plain (4 of 5)"),
    ]
    missing_html = "".join(f"<tr><td>{q}</td><td>{n}</td><td>{f}</td></tr>" for q, n, f in missing)
    bars = "".join(f'<div class="hbars__row"><span class="hbars__name">{d}</span><span class="hbars__track">'
                   f'<span class="hbars__bar" style="width:{c / 60 * 100:.1f}%"></span>'
                   f'<span class="hbars__val">{c}</span></span></div>' for d, c, kind in CITED_SITES[:3])
    body = f"""<section class="band band--mist band--first sample-band" aria-labelledby="page-title">
  <div class="wrap">
    <p class="crumbs rise"><a href="research.html">Research</a> <span aria-hidden="true">/</span> Sample snapshot</p>
    <article class="sheet rise" style="--d:80">
      <header class="sheet__head">
        <div>
          <p class="kicker">AI visibility snapshot</p>
          <h1 id="page-title">Freshdesk: a view from the study</h1>
          <p class="sheet__meta">Perplexity · 40 buyer questions about helpdesk software · 5 runs each · 6 October 2026</p>
        </div>
        <span class="stamp">{icon('doc')}Sample</span>
      </header>
      <div class="notice">{icon('info')}<p>This is a sample of the free snapshot, filled in with Freshdesk’s numbers from our <a href="helpdesk-study.html">public helpdesk study</a>. Freshdesk is not a client. The scope of a new snapshot is confirmed after we review your product and available evidence.</p></div>
      <div class="kpis">
        <div class="kpi"><strong>61%</strong><div class="meter" aria-hidden="true"><b style="width:61%"></b></div><span>of answers name Freshdesk</span></div>
        <div class="kpi"><strong>21%</strong><div class="meter" aria-hidden="true"><b style="width:21%"></b><s style="left:25%"></s></div><span>recommend it first (Zendesk: 25%)</span></div>
        <div class="kpi"><strong>13%</strong><div class="meter" aria-hidden="true"><b style="width:13%"></b><s style="left:21%"></s></div><span>cite Freshworks’ own site (Help Scout: 21%)</span></div>
      </div>
      <p class="kpi-key" aria-hidden="true"><span><i class="kk-bar"></i>Freshdesk</span><span><i class="kk-tick"></i>Leading rival</span></p>

      <section class="sheet__sec" aria-labelledby="s1">
        <h2 id="s1">Where you’re named</h2>
        <p>Freshdesk is the most-named helpdesk, with the largest share of brand mentions (19%, against Zendesk’s 14%). It was recommended first in all 5 runs of these questions:</p>
        <ul class="qlist">{named_html}</ul>
      </section>

      <section class="sheet__sec" aria-labelledby="s2">
        <h2 id="s2">Where you’re missing</h2>
        <div class="table-wrap"><table>
          <thead><tr><th>Buyer question</th><th>Freshdesk named</th><th>Recommended first instead</th></tr></thead>
          <tbody>{missing_html}</tbody>
        </table></div>
      </section>

      <section class="sheet__sec" aria-labelledby="s3">
        <h2 id="s3">Which pages AI relies on</h2>
        <p>Answers cite listicles and other vendors’ blogs far more than Freshdesk’s own pages. The sites cited most, counted as answers out of 220:</p>
        <div class="hbars" role="img" aria-label="g2.com 56, getmacha.com 40, kayako.com 31 answers out of 220">{bars}</div>
        <p>On how-to questions, hubspot.com was cited in 20 of 50 answers, and freshworks.com in 9.</p>
      </section>

      <section class="sheet__sec" aria-labelledby="s4">
        <h2 id="s4">What to fix first</h2>
        <ol class="fixes">
          <li><div><b>Answer the niche questions directly.</b><span>Check whether ecommerce support, shared inboxes or AI chatbots match the product’s actual strengths. Where they do, review whether its pages answer those questions clearly. The study does not establish why a brand is absent.</span></div></li>
          <li><div><b>Own the how-to questions.</b><span>Review practical guides on SLAs, routing and WhatsApp support against product capabilities. HubSpot’s blog was frequently cited in this dated sample.</span></div></li>
          <li><div><b>Fix the third-party lists.</b><span>Make sure G2 and the most-cited comparison articles describe Freshdesk accurately.</span></div></li>
        </ol>
      </section>
    </article>
  </div>
</section>"""
    cta_band_for["sample-snapshot.html"] = cta_band(
        "Get yours, free.",
        "Send your product name and the competitors you care about. You’ll get this page for your brand by email.")
    page(file="sample-snapshot.html", title="Sample AI visibility snapshot: Freshdesk | Recallant",
         desc="What the free Recallant snapshot looks like: where AI names a brand, where it's missing, which pages it relies on, and what to fix first. Sample uses Freshdesk's public study data.",
         body=body, current="research.html",
         graph=[ORG, breadcrumbs([("Research", SITE + "/research.html"), ("Sample snapshot", SITE + "/sample-snapshot.html")])])


# ================================================================== 404

def not_found() -> None:
    body = f"""<section class="band band--night band--first nf" aria-labelledby="page-title">
  <div class="wrap">
    <p class="kicker">Error 404</p>
    <h1 class="h-display" id="page-title">Not found<span class="hl">.</span></h1>
    <p class="lede">This page doesn’t exist. Try the home page instead.</p>
    <div class="ctas ctas--center">
      <a class="btn btn--signal" href="./">Go home</a>
      <a class="arrow-link" href="helpdesk-study.html">Read the helpdesk study {icon('arrow')}</a>
    </div>
  </div>
</section>"""
    page(file="404.html", title="Page not found | Recallant", desc="This page doesn't exist.",
         body=body, tone="night", noindex=True, graph=[ORG])


def make_absolute(doc: str) -> str:
    """404.html is served at any missing path, so its links and assets must be root-absolute."""
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"(?:[a-z]+:|#|/|data:)", url):
            return m.group(0)
        return f'{attr}="/{"" if url == "./" else url}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, doc)


# ================================================================== extras

def sitemap() -> str:
    pages = ["", "services.html", "plans.html", "research.html", "helpdesk-study.html", "sample-snapshot.html", "about.html", "method.html", "contact.html", "privacy.html"]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "</urlset>\n")


LLMS = f"""# Recallant

> AI search visibility research and focused website improvements for B2B software brands. A specialist product from Signal & Syllable. Bengaluru, India. Contact: {EMAIL}.

- [Services]({SITE}/services.html): agreed measurement, evidence-led improvements and follow-up.
- [Plans]({SITE}/plans.html): snapshot request, INR 14,400 pre-tax Visibility & Enquiry Pilot, scoped audit and ongoing support.
- [Method]({SITE}/method.html): mention rate, share of voice, citations and first-named order proxy; these do not measure revenue or verified preference.
- [Research]({SITE}/research.html): published study and sample.
- [Helpdesk study]({SITE}/helpdesk-study.html): 44 questions, 220 saved Perplexity answers collected 6 October 2026. Historical evidence, not current live search.
- [Sample]({SITE}/sample-snapshot.html): Freshdesk example, not a client result.
- [Contact]({SITE}/contact.html): choose a request and continue to the shared Signal & Syllable review-and-send form.
- [Privacy]({SITE}/privacy.html)
- [About]({SITE}/about.html)
"""


def to_fragment(doc: str, title: str) -> str:
    """Turn a full page into the body-only form a claude.ai artifact expects for its main page."""
    head = re.search(r"<head>(.*?)</head>", doc, re.S).group(1)
    body = re.search(r"<body>(.*)</body>", doc, re.S).group(1)
    head = re.sub(r"<title>.*?</title>\n?", "", head)
    head = re.sub(r'<meta (?:charset|name="viewport")[^>]*>\n?', "", head)
    return (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f"{head.strip()}\n{body.strip()}\n")


def main(argv) -> None:
    import studio_pages, offer_pages
    b = sys.modules[__name__]
    studio_pages.home(b)
    offer_pages.services(b)
    offer_pages.plans(b)
    offer_pages.method(b)
    offer_pages.contact(b)
    offer_pages.privacy(b)
    research()
    study()
    sample()
    studio_pages.about(b)
    not_found()
    PAGES["404.html"] = make_absolute(PAGES["404.html"])

    if len(argv) >= 2 and argv[0] == "--preview":
        out = pathlib.Path(argv[1])
        out.mkdir(parents=True, exist_ok=True)
        for name, doc in PAGES.items():
            if name == "404.html":
                continue
            if name == "index.html":
                (out / "index-fragment.html").write_text(to_fragment(doc, "Recallant Website"))
            (out / name).write_text(doc, encoding="utf-8", newline="\n")
        print("preview written to", out)
        return

    out = ROOT
    if argv:
        if len(argv) != 2 or argv[0] != "--output":
            raise ValueError("Use no arguments, --output DIR, or --preview DIR")
        out = pathlib.Path(argv[1]).resolve()
        out.mkdir(parents=True, exist_ok=True)
    for name, doc in PAGES.items():
        (out / name).write_text(doc, encoding="utf-8", newline="\n")
    (out / "sitemap.xml").write_text(sitemap(), encoding="utf-8", newline="\n")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8", newline="\n")
    (out / "llms.txt").write_text(LLMS, encoding="utf-8", newline="\n")
    (out / "favicon.svg").write_text(favicon_svg(), encoding="utf-8", newline="\n")
    if out == ROOT:
        (HERE / "data" / "mark-square.svg").write_text(favicon_svg(rounded=False), encoding="utf-8", newline="\n")
    print("built:", ", ".join(sorted(PAGES)))


if __name__ == "__main__":
    main(sys.argv[1:])
