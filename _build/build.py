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
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "_build"

SITE = "https://recallant.com"
EMAIL = "hello@recallant.com"
LINKEDIN = "https://www.linkedin.com/in/prasanth-gorripati-44805b209/"
UPDATED = "2026-10-15"
# Requests are delivered by Formspree (formspree.io): this form's endpoint, set up in the
# Formspree account for hello@recallant.com. The script posts JSON to the same address.
FORM_ACTION = "https://formspree.io/f/testform"
ORG_ID = f"{SITE}/#org"
PERSON_ID = f"{SITE}/about.html#prasanth"

NAV = [("services.html", "Services"), ("plans.html", "Plans"),
       ("research.html", "Research"), ("about.html", "About")]


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

EXPLORER = json.loads((HERE / "data" / "helpdesk-explorer.json").read_text())
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
      <a class="btn btn--signal btn--sm" href="#get-snapshot">Get a free snapshot</a>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="menu" id="menu" hidden>
  <nav aria-label="Mobile">
{menu}
  </nav>
  <a class="btn btn--signal" href="#get-snapshot">Get a free snapshot</a>
  <p class="menu__note">Or email <a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>"""


def cta_band(title: str = "See what AI says about you.",
             lede: str = "Send your product name. You’ll get a one-page snapshot by email.",
             interests: list[str] | None = None) -> str:
    """The request form. `interests` adds a visible choice; links with data-interest preselect it."""
    checks = [
        "20 questions your buyers ask, run several times each",
        "Where you’re named, where you’re missing, and which pages AI cites",
        "Free, and no call needed",
    ]
    lis = "".join(f"<li>{icon('check')}<span>{c}</span></li>" for c in checks)
    if interests:
        opts = "".join(f"<option>{o}</option>" for o in ["A free snapshot", *interests])
        interest = f"""<div class="field">
          <label for="sf-interest">I’m interested in</label>
          <select id="sf-interest" name="interest">{opts}</select>
        </div>"""
    else:
        interest = '<input type="hidden" name="interest" value="A free snapshot">'
    return f"""<section class="band band--night" id="get-snapshot" aria-labelledby="cta-title">
  <div class="wrap cta">
    <div class="cta__copy">
      <p class="eyebrow">Free snapshot</p>
      <h2 class="h2" id="cta-title">{title}</h2>
      <p class="lede">{lede}</p>
      <ul class="cta__list">{lis}</ul>
      <p><a class="arrow-link" href="sample-snapshot.html">See a sample snapshot {icon('arrow')}</a></p>
    </div>
    <form class="snap-form" data-snapshot-form action="{FORM_ACTION}" method="post">
      <div class="snap-form__fields">
        <h3>Request your snapshot</h3>
        <input type="hidden" name="_subject" value="Snapshot request from recallant.com">
        <div class="snap-form__hp" aria-hidden="true">
          <label for="sf-hp">Leave this field empty</label>
          <input id="sf-hp" name="_gotcha" tabindex="-1" autocomplete="off">
        </div>
        {interest}
        <div class="field">
          <label for="sf-email">Work email</label>
          <input id="sf-email" name="email" type="email" autocomplete="email" required placeholder="you@company.com" aria-describedby="sf-email-error">
          <p class="field__error" id="sf-email-error" hidden>Add an email address we can reply to.</p>
        </div>
        <div class="field">
          <label for="sf-product">Product or company</label>
          <input id="sf-product" name="product" autocomplete="organization" required placeholder="e.g. Acme Helpdesk" aria-describedby="sf-product-error">
          <p class="field__error" id="sf-product-error" hidden>Add your product or company name.</p>
        </div>
        <div class="field">
          <label for="sf-site">Website <span>(optional)</span></label>
          <input id="sf-site" name="website" autocomplete="url" inputmode="url" placeholder="acme.com">
        </div>
        <div class="field">
          <label for="sf-rivals">Competitors to compare <span>(optional)</span></label>
          <input id="sf-rivals" name="competitors" placeholder="Up to three">
        </div>
        <button class="btn btn--signal" type="submit">{icon('mail')}<span>Send my request</span></button>
        <p class="snap-form__note">We’ll reply to the email address you give here.</p>
        <p class="snap-form__status" role="status" aria-live="polite"></p>
      </div>
      <div class="snap-form__done" tabindex="-1" hidden>
        <span class="snap-form__tick">{icon('check')}</span>
        <h3>Request sent.</h3>
        <p>Thanks. We’ll reply to <b data-sent-to></b>.</p>
        <button class="text-btn" type="button" data-form-reset>Send another request</button>
      </div>
      <div class="snap-form__alt">
        <span>Or email <b data-copy-text>{EMAIL}</b></span>
        <button class="copy-btn" type="button" data-copy="{EMAIL}">{icon('copy')}<span>Copy</span></button>
      </div>
    </form>
  </div>
</section>"""


FOOTER = f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="./" aria-label="Recallant home">{MARK}<span>Recallant</span></a>
        <p>AI search visibility for B2B brands. Bengaluru, India.</p>
      </div>
      <nav aria-labelledby="f-explore">
        <h2 id="f-explore">Explore</h2>
        <ul><li><a href="services.html">Services</a></li><li><a href="plans.html">Plans</a></li><li><a href="research.html">Research</a></li><li><a href="about.html">About</a></li></ul>
      </nav>
      <nav aria-labelledby="f-research">
        <h2 id="f-research">Research</h2>
        <ul><li><a href="helpdesk-study.html">Helpdesk study</a></li><li><a href="sample-snapshot.html">Sample snapshot</a></li><li><a href="#get-snapshot">Free snapshot</a></li></ul>
      </nav>
      <nav aria-labelledby="f-contact">
        <h2 id="f-contact">Contact</h2>
        <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li></ul>
      </nav>
    </div>
    <div class="footer__base">
      <span>© 2026 Recallant.</span>
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
    "description": "Recallant measures and improves how AI assistants like ChatGPT, Gemini and Perplexity describe and recommend B2B brands.",
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
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');</script>
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
    PAGES[file] = doc


cta_band_for: dict[str, str] = {}


# ================================================================== HOME

def home() -> None:
    src = Sources([STUDY_SOURCE, SAMPLE_SOURCE])

    def row(name, n, zero=False):
        z = " is-zero" if zero else ""
        return f'<div class="reading__row{z}"><span>{name}</span>{pips(n)}<span class="num">{n}/5</span></div>'

    instrument = f"""<figure class="instrument" data-instrument aria-labelledby="inst-cap">
      <div class="instrument__frame">
        <div class="instrument__bar">
          <span class="instrument__engine"><span class="engine-glyph">{icon('search')}</span>Perplexity</span>
          <span class="instrument__meta"><span>Run 1 of 5</span><span class="hide-sm">· 6 Oct 2026 · live web search</span></span>
        </div>
        <div class="instrument__body">
          <div class="instrument__answer">
            <span class="instrument__scan" aria-hidden="true"></span>
            <p class="instrument__q">What is the best customer support software for a SaaS startup?</p>
            <ul class="instrument__sources" aria-label="Sources in this answer">
              <li class="is-own"><span class="src-n">1</span>plain.com</li>
              <li class="is-own"><span class="src-n">2</span>plain.com</li>
              <li><span class="src-n">3</span>editorialge.com</li>
              <li><span class="src-n">5</span>cometly.com</li>
              <li><span class="src-n">6</span>rework.com</li>
            </ul>
            <div class="instrument__text">
              <p>For most <strong>B2B SaaS startups with technical customers, <mark class="brandmark brandmark--first" style="--at:900">Plain</mark><span class="brandtag" style="--at:900">1st pick</span> is a strong default</strong>: it’s built for SaaS support and works across email, Slack, Discord, Teams, and other channels, with AI included on all plans.<span class="ref is-own">1</span><span class="ref is-own">2</span></p>
              <p>The best choice depends on how your customers seek help:</p>
              <ul>
                <li><strong><mark class="brandmark" style="--at:1150">Plain</mark>:</strong> Best for technical B2B products and teams handling support in Slack or Discord.<span class="ref is-own">1</span><span class="ref is-own">2</span></li>
                <li><strong><mark class="brandmark" style="--at:1350">Freshdesk</mark>:</strong> Worth considering if affordability and straightforward ticketing are priorities; a free program is available for small teams.<span class="ref">3</span></li>
                <li><strong><mark class="brandmark" style="--at:1550">Tidio</mark>:</strong> A fit for a small team that wants to automate common questions with an AI chatbot.<span class="ref">5</span></li>
              </ul>
              <p>Before choosing, prioritize the channels your customers already use, then compare the total cost as your support volume and team grow.<span class="ref">6</span></p>
            </div>
          </div>
          <div class="instrument__reading">
            <p class="reading__head"><span class="live-dot" aria-hidden="true"></span>Recallant reading · all 5 runs</p>
            <div class="reading__group">
              <p class="reading__label">Recommended first</p>
              {row('Plain', 4)}{row('Intercom', 1)}
            </div>
            <div class="reading__group">
              <p class="reading__label">Named in the answer</p>
              {row('Plain', 5)}{row('Freshdesk', 5)}{row('Tidio', 3)}{row('Intercom', 1)}{row('Help Scout', 0, True)}
            </div>
            <div class="reading__group">
              <p class="reading__label">Own site cited</p>
              {row('plain.com', 5)}{row('helpscout.com', 4)}{row('freshworks.com', 0, True)}
            </div>
            <p class="reading__insight">{icon('bulb')}<span>Help Scout’s blog was a source in 4 of 5 answers. Help Scout was named in none.</span></p>
          </div>
        </div>
      </div>
      <figcaption class="stage__caption" id="inst-cap">A real answer from our helpdesk study, shown in full: Perplexity, run 1 of 5, 6 October 2026. The reading on the right covers all 5 runs. <a href="helpdesk-study.html">Read the study</a></figcaption>
    </figure>"""

    units = "".join('<span class="unit on"></span>' if i < 3 else
                    ('<span class="unit part"></span>' if i == 3 else '<span class="unit"></span>')
                    for i in range(23))

    fixes_panel = f"""<div class="viz-panel">
          <div class="viz-panel__head"><span class="viz-panel__title">What to fix first</span><span class="viz-panel__meta">From the sample snapshot</span></div>
          <ol class="viz-fixes">
            <li><span>Answer the niche questions directly</span><span class="chip chip--plain">Content</span></li>
            <li><span>Own the how-to questions</span><span class="chip chip--plain">Content</span></li>
            <li><span>Fix the third-party lists</span><span class="chip chip--plain">PR</span></li>
          </ol>
        </div>"""

    measure_tile = f"""<article class="tile tile--measure">
        <p class="tile__eyebrow">Measure</p>
        <h3>AI visibility consulting</h3>
        <p>Monthly tracking of where ChatGPT, Gemini and Perplexity name you, which sources they trust, and what to fix first.</p>
        <a class="arrow-link" href="services.html#visibility">Learn more {icon('arrow')}<span class="sr-only"> about AI visibility consulting</span></a>
        <div class="tile__viz viz-stack">{sov_panel(8, note='Whiskers show 95% ranges. Real numbers from our helpdesk study.')}{fixes_panel}</div>
      </article>"""

    publish_viz = """<div class="viz-panel viz-article" aria-hidden="true">
          <div class="va-title"></div>
          <div class="va-line" style="width:88%"></div>
          <div class="va-answer"><span class="va-tag">Direct answer</span><div class="va-line" style="width:100%"></div><div class="va-line" style="width:76%"></div></div>
          <div class="va-table"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
          <div class="va-src"><span>[1] data</span><span>[2] method</span><span>[3] sources</span></div>
        </div>"""

    build_viz = """<div class="viz-browser" aria-hidden="true">
          <div class="vb-bar"><i></i><i></i><i></i><span class="vb-url">yourbrand.com/pricing</span></div>
          <div class="vb-body">
            <div class="vb-page"><div class="va-title"></div><div class="va-line" style="width:92%"></div><div class="va-line" style="width:70%"></div><div class="va-table"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
            <div class="vb-code"><span class="k">"@type"</span>: <span class="s">"SoftwareApplication"</span>,
<span class="k">"name"</span>: <span class="s">"Your product"</span>,
<span class="k">"offers"</span>: { … },
<span class="k">"faq"</span>: [ … ]</div>
          </div>
          <div class="vb-checks"><span class="chip">""" + icon("check") + """Structured data</span><span class="chip">""" + icon("check") + """Fast pages</span><span class="chip">""" + icon("check") + """Clear answers</span></div>
        </div>"""

    protect_viz = """<div class="viz-profiles" aria-hidden="true">
          <div class="vp-row"><span class="vp-ico">WEB</span><span class="vp-text"><b>Your website</b><span>Category, pricing, description</span></span><span class="chip">""" + icon("check") + """Source of truth</span></div>
          <div class="vp-row"><span class="vp-ico">IN</span><span class="vp-text"><b>LinkedIn page</b><span>Description and category</span></span><span class="chip">""" + icon("check") + """Matches</span></div>
          <div class="vp-row"><span class="vp-ico">REV</span><span class="vp-text"><b>Review profile</b><span>Pricing from last year</span></span><span class="chip chip--warn">Outdated</span></div>
          <div class="vp-row"><span class="vp-ico">DIR</span><span class="vp-text"><b>Directory listing</b><span>Listed in the wrong category</span></span><span class="chip chip--warn">Fix</span></div>
        </div>"""

    doc = f"""<div class="doc" role="img" aria-label="Preview of the sample snapshot for Freshdesk">
          <div class="doc__head">
            <div>
              <div class="doc__brand">{MARK}Recallant</div>
              <p class="doc__title">Freshdesk: what AI says today</p>
              <p class="doc__meta">Perplexity · 40 questions · 5 runs · 6 Oct 2026</p>
            </div>
            <span class="doc__stamp">Sample</span>
          </div>
          <div class="doc__kpis">
            <div><strong>61%</strong><span>of answers name Freshdesk</span></div>
            <div><strong>21%</strong><span>recommend it first (Zendesk: 25%)</span></div>
            <div><strong>13%</strong><span>cite its own site (Help Scout: 21%)</span></div>
          </div>
          <div class="doc__sec"><span class="doc__marker">1</span><h4>Where you’re named</h4>
            <ul class="doc__list"><li><span>Best helpdesk for a small business</span><b>First, 5 of 5</b></li><li><span>Best helpdesk for companies in India</span><b>First, 5 of 5</b></li><li><span>Best Zendesk alternatives</span><b>First, 5 of 5</b></li></ul>
          </div>
          <div class="doc__sec"><span class="doc__marker">2</span><h4>Where you’re missing</h4>
            <div class="doc__miss"><span class="hd">Buyer question</span><span class="hd">Named</span><span class="hd">First instead</span>
              <span>Platform for an ecommerce store</span><span>0 of 5</span><span>Gorgias</span>
              <span>Shared inbox tool for support</span><span>0 of 5</span><span>Help Scout</span>
              <span>Helpdesk with the best AI chatbot</span><span>3 of 5</span><span>Intercom</span>
            </div>
          </div>
          <div class="doc__sec"><span class="doc__marker">3</span><h4>Which pages AI relies on</h4>
            <div class="doc__bars"><div><span>g2.com</span><i><b style="width:100%"></b></i><span>56</span></div><div><span>getmacha.com</span><i><b style="width:71%"></b></i><span>40</span></div><div><span>kayako.com</span><i><b style="width:55%"></b></i><span>31</span></div></div>
          </div>
          <div class="doc__sec"><span class="doc__marker">4</span><h4>What to fix first</h4>
            <ol class="doc__fix"><li>Answer the niche questions directly.</li><li>Own the how-to questions.</li><li>Fix the third-party lists.</li></ol>
          </div>
        </div>"""

    principles = [
        ("scale", "Evidence over opinion.", "Every recommendation points to the answers and sources behind it."),
        ("info", "Honest limits.", "We say which assistants we measured, when, and what we didn’t measure."),
        ("shield", "Nothing fake.", "No bought reviews, links or mentions, ever."),
        ("page", "Plain reporting.", "One page you can read in two minutes, not a dashboard you have to decode."),
    ]
    principle_html = "".join(f'<div class="principle reveal" style="--d:{i * 80}">{icon(ic)}<h3>{t}</h3><p>{p}</p></div>'
                             for i, (ic, t, p) in enumerate(principles))

    explorer_html = explorer(HOME_QUESTIONS, "home", tabs=False, more=(
        f'<p class="explorer__more">{len(HOME_QUESTIONS)} of the study’s 40 questions. '
        f'<a href="helpdesk-study.html#explore">See all 40 {icon("arrow")}</a></p>'))

    body = f"""<section class="band band--night band--first hero" aria-labelledby="hero-title">
  <div class="wrap">
    <a class="hero__pill rise" style="--d:0" href="helpdesk-study.html"><b>New study</b><span>We read 220 AI answers<span class="hide-sm"> about helpdesk software</span></span>{icon('arrow')}</a>
    <h1 class="h-hero hero__title rise" style="--d:80" id="hero-title">Be the answer<span class="dot">.</span></h1>
    <p class="lede hero__lede rise" style="--d:160">Your buyers now ask ChatGPT, Gemini and Perplexity what to buy. Recallant measures what those assistants say about you, then works on the content, coverage and pages that change it.</p>
    <div class="ctas ctas--center hero__ctas rise" style="--d:240">
      <a class="btn btn--signal" href="#get-snapshot">Get a free snapshot</a>
      <a class="arrow-link" href="#how">See how it works {icon('arrow')}</a>
    </div>
    <p class="hero__fine rise" style="--d:300"><span>Free, one page</span><span>No call needed</span><span>ChatGPT, Gemini and Perplexity</span></p>
    <div class="stage">
    {instrument}
    </div>
  </div>
</section>

<section class="band band--paper" aria-labelledby="shift-title">
  <div class="wrap shift">
    <div class="shift__copy reveal">
      <p class="eyebrow">The shift</p>
      <h2 class="h2" id="shift-title">Ten blue links became one answer.</h2>
      <p class="lede">Buyers used to search, click and compare. Now many ask an assistant and read one answer. That answer usually names three or four products.</p>
      <p class="lede"><strong class="ink">If yours isn’t one of them, you never hear about the deal you lost.</strong></p>
    </div>
    <figure class="units-card reveal" style="--d:120" aria-labelledby="units-cap">
      <div class="units-card__num"><strong>3.6</strong><span>of 23 brands</span></div>
      <div class="units" role="img" aria-label="3.6 of 23 brands named in an average answer">{units}</div>
      <div class="units-legend" aria-hidden="true"><span><i class="k-on"></i>Named in an average answer</span><span><i class="k-off"></i>Left out</span></div>
      <figcaption class="units-note" id="units-cap">Support tools named in an average Perplexity answer to a “best helpdesk for…” question, out of the 23 we tracked. Based on 80 answers to 16 questions.{src.cite(1)}</figcaption>
    </figure>
  </div>
</section>

<section class="band band--mist" aria-labelledby="cited-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">From our October 2026 helpdesk study</p>
      <h2 class="h2" id="cited-title">Being cited isn’t being chosen.</h2>
      <p class="lede">We asked Perplexity 44 questions that helpdesk buyers ask, 5 times each, and read every answer.</p>
    </div>
    <div class="stats">
      <div class="stat reveal"><div class="stat__num">220</div><p class="stat__label">AI answers analysed</p></div>
      <div class="stat reveal" style="--d:80"><div class="stat__num">3<small>×</small></div><p class="stat__label">Help Scout’s site was cited three times as often (21% of answers) as Help Scout was recommended first (7%)</p></div>
      <div class="stat reveal" style="--d:160"><div class="stat__num">8 <small>of</small> 10</div><p class="stat__label">how-to questions got answers that named no helpdesk product at all{src.cite(1)}</p></div>
    </div>
    <div class="wide reveal">{dumbbell(src)}</div>
    <p class="after-chart reveal"><a class="arrow-link" href="helpdesk-study.html">Read the study {icon('arrow')}</a></p>
  </div>
</section>

<section class="band band--paper" aria-labelledby="ask-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Try it</p>
      <h2 class="h2" id="ask-title">Ask what buyers ask.</h2>
      <p class="lede">Pick a question from the study. See who Perplexity recommended first, who it named, and whose pages it read, across 5 runs.</p>
    </div>
    <div class="reveal">{explorer_html}</div>
  </div>
</section>

<section class="band band--mist" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">What we do</p>
      <h2 class="h2" id="services-title">Everything AI reads about your brand.</h2>
      <p class="lede">AI assistants build their answers from your site, the articles that rank, the lists that compare you and the reviews about you. We work on all of it, as one monthly plan.</p>
    </div>
    <div class="bento">
      {measure_tile}
      <article class="tile tile--publish reveal" style="--d:80">
        <p class="tile__eyebrow">Publish</p>
        <h3>Articles and reports</h3>
        <p>Research and articles that answer the exact questions your buyers ask, written so assistants can quote them.</p>
        <a class="arrow-link" href="services.html#content">Learn more {icon('arrow')}<span class="sr-only"> about articles and reports</span></a>
        <div class="tile__viz">{publish_viz}</div>
      </article>
      <article class="tile tile--earn reveal" style="--d:160">
        <p class="tile__eyebrow">Earn</p>
        <h3>PR management</h3>
        <p>Accurate mentions in the publications, comparison lists and review sites that AI answers rely on.</p>
        <a class="arrow-link" href="services.html#pr">Learn more {icon('arrow')}<span class="sr-only"> about PR management</span></a>
        <div class="tile__viz">{minibars(3)}</div>
      </article>
      <article class="tile tile--build reveal">
        <p class="tile__eyebrow">Build</p>
        <h3>Website creation and care</h3>
        <p>Fast, clearly structured sites that people trust and machines can read, kept current every month.</p>
        <a class="arrow-link" href="services.html#websites">Learn more {icon('arrow')}<span class="sr-only"> about website creation and care</span></a>
        <div class="tile__viz">{build_viz}</div>
      </article>
      <article class="tile tile--protect reveal" style="--d:80">
        <p class="tile__eyebrow">Protect</p>
        <h3>Brand management</h3>
        <p>One consistent story across your profiles and listings, and corrections when an assistant gets you wrong.</p>
        <a class="arrow-link" href="services.html#brand">Learn more {icon('arrow')}<span class="sr-only"> about brand management</span></a>
        <div class="tile__viz">{protect_viz}</div>
      </article>
    </div>
  </div>
</section>

<section class="band band--night" aria-labelledby="snapshot-title">
  <div class="wrap showcase">
    <div class="doc-stage reveal">
      {doc}
    </div>
    <div class="showcase__copy reveal" style="--d:120">
      <p class="eyebrow">Start here</p>
      <h2 class="h2" id="snapshot-title">One page. Everything AI says about you.</h2>
      <p class="lede">The free snapshot: 20 questions your buyers ask, run several times. One page on where you’re named, where you’re missing, and why.{src.cite(2)}</p>
      <ol class="callouts">
        <li><div><h3>Where you’re named</h3><p>How often you’re named, and how often you’re recommended first.</p></div></li>
        <li><div><h3>Where you’re missing</h3><p>The buyer questions where a rival is recommended instead.</p></div></li>
        <li><div><h3>Which pages AI relies on</h3><p>The sites the answers cite, so you know where to be present.</p></div></li>
        <li><div><h3>What to fix first</h3><p>Three changes, in order, with the evidence behind each.</p></div></li>
      </ol>
      <div class="ctas">
        <a class="btn btn--signal" href="#get-snapshot">Get a free snapshot</a>
        <a class="arrow-link" href="sample-snapshot.html">See the full sample {icon('arrow')}</a>
      </div>
    </div>
  </div>
</section>

<section class="band band--paper" id="how" aria-labelledby="how-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">How it works</p>
      <h2 class="h2" id="how-title">Measure. Fix. Measure again.</h2>
    </div>
    <ol class="steps">
      <li class="step reveal"><span class="step__n">1</span><h3>Snapshot</h3><p>We run the questions your buyers ask and show you, on one page, what AI says today. Free, and no call needed.</p><p class="step__meta">Free · one page</p></li>
      <li class="step reveal" style="--d:80"><span class="step__n">2</span><h3>Plan</h3><p>We agree on the gaps worth closing and the plan that fits: measurement only, or content, PR, website and brand work too.</p><p class="step__meta">Quoted after the snapshot</p></li>
      <li class="step reveal" style="--d:160"><span class="step__n">3</span><h3>Every month</h3><p>We do the work, then re-run the same questions, so you can see what moved and what didn’t.</p><p class="step__meta">Same questions, every month</p></li>
    </ol>
    <p class="loopnote reveal">{icon('loop')}<span>The question set stays fixed, so changes from one month to the next can be tested for significance.</span></p>
  </div>
</section>

<section class="band band--mist" aria-labelledby="evidence-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">How we work</p>
      <h2 class="h2" id="evidence-title">Evidence, not guesswork.</h2>
      <p class="lede">Most advice about “AI SEO” is guesswork. We start by measuring: the same buyer questions, asked many times, with every answer and every cited source recorded.</p>
    </div>
    <div class="principles">{principle_html}</div>
    <div class="founder reveal">
      <img src="assets/img/prasanth-640.jpg" alt="Prasanth G" width="88" height="88" loading="lazy" decoding="async">
      <div>
        <p class="founder__name">Prasanth G</p>
        <p class="founder__role">Founder · Bengaluru, India</p>
        <p class="founder__bio">Recallant is run by Prasanth G, who has a background in IT and business analysis, working with B2B software companies everywhere.</p>
      </div>
      <div class="founder__links">
        <a class="btn btn--quiet btn--sm" href="{LINKEDIN}" rel="noopener">LinkedIn {icon('external')}</a>
        <a class="btn btn--quiet btn--sm" href="about.html">About Recallant</a>
      </div>
    </div>
  </div>
</section>"""

    graph = [ORG, PERSON, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Recallant",
                           "publisher": {"@id": ORG_ID}, "inLanguage": "en"}]
    page(file="index.html", title="Recallant: AI search visibility for B2B brands",
         desc="Recallant measures what ChatGPT, Gemini and Perplexity say about your brand, then improves the content, PR, website and listings those answers rely on.",
         body=body, tone="night", graph=graph, sources=src)


# ================================================================== SERVICES

def services() -> None:
    src = Sources([STUDY_SOURCE])
    content_viz = """<div class="viz-panel viz-article" aria-hidden="true">
            <div class="viz-panel__head"><span class="viz-panel__title">How to choose a helpdesk for a 10-person team</span><span class="viz-panel__meta">Article</span></div>
            <div class="va-answer"><span class="va-tag">Direct answer, first</span><div class="va-line" style="width:100%"></div><div class="va-line" style="width:94%"></div><div class="va-line" style="width:62%"></div></div>
            <div class="va-line" style="width:96%"></div><div class="va-line" style="width:88%"></div>
            <div class="va-table"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
            <div class="va-line" style="width:92%"></div><div class="va-line" style="width:70%"></div>
            <div class="va-src"><span>[1] pricing pages, checked 6 Oct</span><span>[2] our data</span><span>[3] method</span></div>
          </div>"""
    websites_viz = """<div class="viz-browser" aria-hidden="true">
            <div class="vb-bar"><i></i><i></i><i></i><span class="vb-url">yourbrand.com/pricing</span></div>
            <div class="vb-body">
              <div class="vb-page"><div class="va-title"></div><div class="va-line" style="width:92%"></div><div class="va-line" style="width:76%"></div><div class="va-table"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="va-line" style="width:84%"></div></div>
              <div class="vb-code"><span class="k">"@type"</span>: <span class="s">"SoftwareApplication"</span>,
<span class="k">"name"</span>: <span class="s">"Your product"</span>,
<span class="k">"applicationCategory"</span>:
  <span class="s">"BusinessApplication"</span>,
<span class="k">"offers"</span>: { … }</div>
            </div>
            <div class="vb-checks"><span class="chip">""" + icon("check") + """Structured data</span><span class="chip">""" + icon("check") + """Fast pages</span><span class="chip">""" + icon("check") + """Clear headings</span><span class="chip">""" + icon("check") + """FAQ that answers</span></div>
          </div>"""
    brand_viz = """<div class="viz-panel" aria-hidden="true">
            <div class="viz-panel__head"><span class="viz-panel__title">Profile audit</span><span class="viz-panel__meta">Illustration</span></div>
            <div class="viz-profiles">
              <div class="vp-row"><span class="vp-ico">WEB</span><span class="vp-text"><b>Your website</b><span>Category, pricing, description</span></span><span class="chip">""" + icon("check") + """Source of truth</span></div>
              <div class="vp-row"><span class="vp-ico">IN</span><span class="vp-text"><b>LinkedIn page</b><span>Description and category</span></span><span class="chip">""" + icon("check") + """Matches</span></div>
              <div class="vp-row"><span class="vp-ico">REV</span><span class="vp-text"><b>Review profile</b><span>Pricing from last year</span></span><span class="chip chip--warn">Outdated</span></div>
              <div class="vp-row"><span class="vp-ico">DIR</span><span class="vp-text"><b>Directory listing</b><span>Listed in the wrong category</span></span><span class="chip chip--warn">Fix</span></div>
              <div class="vp-row"><span class="vp-ico">AI</span><span class="vp-text"><b>What assistants say</b><span>Checked every month</span></span><span class="chip chip--plain">Monitored</span></div>
            </div>
          </div>"""

    def service(anchor, ic, eyebrow, title, text, items, viz, cap, mist=False, flip=False):
        lis = "".join(f"<li>{icon('check')}<span>{i}</span></li>" for i in items)
        cls = "service" + (" band--mist" if mist else " band--paper") + (" service--flip" if flip else "")
        return f"""<section class="{cls}" id="{anchor}" aria-labelledby="{anchor}-title">
    <div class="wrap service__grid">
      <div class="service__copy reveal">
        <span class="service__icon">{icon(ic)}</span>
        <p class="eyebrow">{eyebrow}</p>
        <h2 class="h2" id="{anchor}-title">{title}</h2>
        <p>{text}</p>
        <ul class="checks">{lis}</ul>
      </div>
      <figure class="service__viz reveal" style="--d:120">
        {viz}
        <figcaption class="service__viz-cap">{cap}</figcaption>
      </figure>
    </div>
  </section>"""

    sections = [
        service("visibility", "chart", "AI visibility consulting", "Know where you stand.",
                "Every month we ask AI assistants the questions your buyers ask, several times each, and measure who gets named, who gets recommended first, and which sources the answers rely on. Then we tell you what to change, in order.",
                ["Your buyer questions, run on ChatGPT, Gemini and Perplexity",
                 "Share of voice against the competitors you choose",
                 "The pages and sites each answer cites",
                 "A prioritised fix list, and a monthly strategy session",
                 "The same questions re-run each month, so changes are measurable"],
                sov_panel(6), f"Real numbers from our helpdesk study. Your report shows the same view for your category.{src.cite(1)}"),
        service("content", "doc", "Articles and reports", "Content AI can quote.",
                "Assistants quote pages that answer a question directly and back it with evidence. We write research reports and articles built around the questions your buyers actually ask.",
                ["Original research reports in your category",
                 "Articles that answer buyer questions plainly",
                 "Comparison and alternatives pages written fairly",
                 "Facts, sources and dates on every claim",
                 "Topics chosen from what the measurement shows is missing"],
                content_viz, "Illustration: an article built around one buyer question, with the answer first, a comparison table and dated sources.",
                mist=True, flip=True),
        service("pr", "megaphone", "PR management", "Get mentioned where AI looks.",
                "Much of what AI says comes from third parties: industry press, comparison lists, review marketplaces. We find the sources the answers in your category rely on and work to get you represented in them accurately.",
                ["A map of the publications and lists AI cites in your category",
                 "Pitches, briefings and corrections to editors and list owners",
                 "Help getting honest reviews from real customers",
                 "Press releases for news that deserves one",
                 "Never paid reviews, bought links or fake mentions"],
                minibars(6, "Sites Perplexity cited most", "helpdesk answers out of 220"),
                f"From our helpdesk study: Perplexity mostly cited listicles and other vendors’ blogs, not Freshdesk’s own pages.{src.cite(1)}"),
        service("websites", "browser", "Website creation and care", "Built for people. Readable by AI.",
                "We design and build fast, clean websites with clear answers, structured data and pages that match how buyers ask. Then we keep them current, every month.",
                ["Design and build of marketing sites",
                 "Structured data, clean headings and fast pages",
                 "Product, pricing and FAQ pages that answer real questions",
                 "Monthly updates, fixes and new pages",
                 "Hosting setup and domain help"],
                websites_viz, "Illustration: a pricing page with structured data that assistants can read.",
                mist=True, flip=True),
        service("brand", "ribbon", "Brand management", "One clear story, everywhere.",
                "When your website, LinkedIn page, review profiles and directory listings disagree, AI assistants repeat the confusion. We keep your facts consistent everywhere and watch what assistants say about you.",
                ["An audit of your profiles and listings",
                 "One consistent description, category and set of facts",
                 "Updates when your product, pricing or positioning changes",
                 "Monthly checks of how AI describes you",
                 "Corrections when an assistant gets you wrong"],
                brand_viz, "Illustration: a profile audit flags the facts that disagree."),
    ]
    localnav = "".join(f'<li><a href="#{a}">{icon(ic)}{label}</a></li>' for a, ic, label in [
        ("visibility", "chart", "AI visibility"), ("content", "doc", "Articles and reports"), ("pr", "megaphone", "PR"),
        ("websites", "browser", "Websites"), ("brand", "ribbon", "Brand")])
    body = f"""<section class="band band--paper band--first page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow rise">Services</p>
    <h1 class="h-display rise" style="--d:80" id="page-title">One brand.<br>Every answer.</h1>
    <p class="lede rise" style="--d:160">Five services that work on the same goal: when someone asks an AI assistant what to buy, your brand is in the answer, described correctly.</p>
  </div>
</section>
<div class="services-wrap">
  <nav class="localnav" aria-label="Services">
    <div class="wrap"><ul data-spy>{localnav}</ul></div>
  </nav>
  {''.join(sections)}
</div>"""
    graph = [ORG, breadcrumbs([("Services", SITE + "/services.html")])] + [
        {"@type": "Service", "name": n, "serviceType": n, "description": d, "provider": {"@id": ORG_ID},
         "areaServed": "Worldwide", "url": f"{SITE}/services.html#{a}"}
        for a, n, d in [
            ("visibility", "AI visibility consulting", "Monthly tracking of where ChatGPT, Gemini and Perplexity name a brand, which sources they trust, and what to fix first."),
            ("content", "Articles and reports", "Research and articles that answer the exact questions buyers ask, written so assistants can quote them."),
            ("pr", "PR management", "Accurate mentions in the publications, comparison lists and review sites that AI answers rely on."),
            ("websites", "Website creation and care", "Fast, clearly structured sites that people trust and machines can read, kept current every month."),
            ("brand", "Brand management", "One consistent story across profiles and listings, and corrections when an assistant gets a brand wrong."),
        ]]
    cta_band_for["services.html"] = cta_band("Start with a free snapshot.", "See where you stand before you decide anything.")
    page(file="services.html", title="Services: AI visibility, content, PR, websites and brand | Recallant",
         desc="AI visibility consulting, articles and reports, PR management, website creation and care, and brand management, all aimed at being named in AI answers.",
         body=body, current="services.html", graph=graph, sources=src)


# ================================================================== PLANS

PLANS = [
    ("Visibility", "", "For teams that want the data and advice, and do the work themselves.",
     ["Monthly AI visibility report on ChatGPT, Gemini and Perplexity", "Competitor share of voice",
      "Sources and pages each answer cites", "Prioritised fix list", "Monthly strategy session"]),
    ("Growth", "Recommended", "For teams that want the fixes written and placed for them.",
     ["Everything in Visibility", "Articles and reports each month", "PR outreach to the sources AI cites",
      "Review and listing improvements", "Monthly results review"]),
    ("Brand", "", "For teams that want one partner for their whole presence.",
     ["Everything in Growth", "Website care and new pages", "Brand management across profiles and listings",
      "Corrections when AI gets you wrong", "Quarterly strategy review"]),
]

FAQ = [
    ("Can you guarantee that AI will recommend us?",
     "No, and nobody honestly can. AI answers change, and they depend on sources nobody controls. What we promise is measurement you can check, work aimed at the gaps it shows, and the same questions re-run every month so you can see the effect."),
    ("Which AI assistants do you measure?",
     "ChatGPT, Gemini and Perplexity by default. We can add others if your buyers use them."),
    ("Why is pricing on request?",
     "The work depends on your category, your competitors and how much content and PR you need. After the free snapshot we send a fixed monthly quote, so you know the cost before you commit."),
    ("How long is the commitment?",
     "Plans are billed monthly. The terms, including notice to cancel, are agreed in writing before any work starts."),
    ("Do you buy reviews, links or mentions?",
     "Never. Paid or fake reviews break the review sites’ rules, and they put your reputation at risk. Everything we earn for you is real."),
    ("What happens in the free snapshot?",
     'We run 20 questions your buyers ask, several times each, and send one page showing where you’re named, where you’re missing, and which pages AI is citing. No call needed. <a class="text-link" href="sample-snapshot.html">See a sample snapshot</a>.'),
]


def plans() -> None:
    cards = []
    for i, (name, tag, for_text, items) in enumerate(PLANS):
        featured = bool(tag)
        lis = "".join(f'<li{" class=" + chr(34) + "is-inherit" + chr(34) if it.startswith("Everything in") else ""}>{icon("check")}<span>{it}</span></li>'
                      for it in items)
        cards.append(f"""<article class="plan{' plan--featured' if featured else ''} reveal" style="--d:{i * 80}" aria-labelledby="plan-{name.lower()}">
        {f'<span class="plan__tag">{tag}</span>' if tag else ''}
        <h2 class="plan__name" id="plan-{name.lower()}">{name}</h2>
        <p class="plan__for">{for_text}</p>
        <div class="plan__price"><strong>Pricing on request</strong><span>Billed monthly · quoted after your free snapshot</span></div>
        <ul class="checks">{lis}</ul>
        <a class="btn {'btn--signal' if featured else 'btn--quiet'}" href="#get-snapshot" data-interest="{name} plan">Ask about {name}</a>
      </article>""")

    yes = f'{icon("check")}<span class="sr-only">Included</span>'
    no = '<span class="no" aria-hidden="true"></span><span class="sr-only">Not included</span>'
    matrix = [
        ("Measure and advise", PLANS[0][3], (1, 1, 1)),
        ("Fixes written and placed", PLANS[1][3][1:], (0, 1, 1)),
        ("Your whole presence", PLANS[2][3][1:], (0, 0, 1)),
    ]
    trs = []
    for group, items, flags in matrix:
        trs.append(f'<tr class="grp"><th colspan="4" scope="colgroup">{group}</th></tr>')
        for it in items:
            tds = "".join(f'<td class="c">{yes if f else no}</td>' for f in flags)
            trs.append(f'<tr><th scope="row">{it}</th>{tds}</tr>')

    faq = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div><p>{a}</p></div></details>' for q, a in FAQ)

    body = f"""<section class="band band--paper band--first page-hero page-hero--center" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow rise">Plans</p>
    <h1 class="h-display rise" style="--d:80" id="page-title">Pick your plan.</h1>
    <p class="lede rise" style="--d:160">Monthly subscriptions, from measurement and advice to a team that runs your whole presence. Every plan starts with a free snapshot, and we quote after it.</p>
  </div>
</section>

<section class="band band--mist band--tight" aria-label="Plans">
  <div class="wrap">
    <div class="plans">
      {''.join(cards)}
    </div>
  </div>
</section>

<section class="band band--paper" aria-labelledby="compare-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Compare</p>
      <h2 class="h2" id="compare-title">What each plan includes.</h2>
    </div>
    <div class="compare-wrap reveal">
      <table class="compare">
        <caption class="sr-only">What each plan includes</caption>
        <thead><tr><th scope="col"><span class="sr-only">Included work</span></th><th class="c" scope="col">Visibility</th><th class="c is-featured" scope="col">Growth</th><th class="c" scope="col">Brand</th></tr></thead>
        <tbody>{''.join(trs)}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="band band--mist" aria-labelledby="extras-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Without a subscription</p>
      <h2 class="h2" id="extras-title">Projects and one-offs.</h2>
    </div>
    <div class="extras">
      <article class="extra reveal">
        <p class="tile__eyebrow">Project</p>
        <h3>Website build</h3>
        <p>A new marketing site, designed and built to be clear for buyers and readable by AI. Add monthly care afterwards, or move to the Brand plan.</p>
        <a class="arrow-link" href="#get-snapshot" data-interest="Website build">Ask about a website {icon('arrow')}</a>
      </article>
      <article class="extra reveal" style="--d:80">
        <p class="tile__eyebrow">One-off</p>
        <h3>AI visibility audit</h3>
        <p>A full question set across your category, competitor share of voice, and the pages and sources to fix first. No subscription needed.</p>
        <a class="arrow-link" href="#get-snapshot" data-interest="AI visibility audit">Ask about an audit {icon('arrow')}</a>
      </article>
    </div>
  </div>
</section>

<section class="band band--paper" aria-labelledby="faq-title">
  <div class="wrap wrap--text">
    <div class="section-head reveal">
      <h2 class="h2" id="faq-title">Questions.</h2>
    </div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>"""
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in FAQ]}
    cta_band_for["plans.html"] = cta_band("Start with the snapshot.",
                                          "Every plan starts with a free one-page snapshot. We quote after it.",
                                          interests=[f"{p[0]} plan" for p in PLANS] + ["Website build", "AI visibility audit"])
    page(file="plans.html", title="Plans: monthly AI visibility subscriptions | Recallant",
         desc="Monthly plans for AI search visibility: Visibility, Growth and Brand, plus website builds and one-off audits. Every plan starts with a free snapshot.",
         body=body, current="plans.html", graph=[ORG, breadcrumbs([("Plans", SITE + "/plans.html")]), faq_ld])


# ================================================================== RESEARCH

def research() -> None:
    method = [
        ("01", "Fix the questions", "We write the questions buyers ask, in four groups: best-for, alternatives, comparisons and how-to. The set stays the same from month to month."),
        ("02", "Ask more than once", "Each question is asked several times, so one lucky or unlucky answer doesn’t decide the result."),
        ("03", "Read every answer", "Every brand mention, first recommendation and cited source is recorded. A brand named in the question is left out of that question’s numbers."),
        ("04", "Show the uncertainty", "Results come with 95% ranges, and we publish the method and its limits."),
    ]
    method_html = "".join(f'<li class="reveal" style="--d:{i * 80}"><span class="kicker">{n}</span><h3>{t}</h3><p>{p}</p></li>'
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
        <h2>Which helpdesks does AI recommend, and whose pages does it trust?</h2>
        <p>44 buyer questions, 5 runs each, 220 Perplexity answers. Freshdesk is named most, Zendesk is recommended first more often, and niche questions have different winners.</p>
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
        <p class="kicker">Sample · What you get for free</p>
        <h3>Sample snapshot: Freshdesk</h3>
        <p>The one-page snapshot every client starts with, filled in with Freshdesk’s numbers from our helpdesk study.</p>
        <span class="arrow-link">See the sample {icon('arrow')}</span>
      </a>
      <article class="card reveal" style="--d:80">
        <p class="kicker">October 2026 · IT management software</p>
        <h3>ITSM and MSP tools in AI answers</h3>
        <p>44 ITSM and MSP buyer questions, 220 Perplexity answers. One MSP tool was named in over a third of answers but recommended first in only 1 of 70.</p>
        <a class="arrow-link" href="#get-snapshot" data-interest="IT management study">Request the study {icon('arrow')}</a>
      </article>
    </div>
  </div>
</section>

<section class="band band--mist" aria-labelledby="method-title">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">How we measure</p>
      <h2 class="h2" id="method-title">The same questions, asked many times.</h2>
      <p class="lede">Every study and every client report follows the same four rules.</p>
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
    raw = (HERE / "content" / "study-source.html").read_text()
    first_p_end = raw.index("</p>") + 4
    byline = re.sub(r"<[^>]+>", "", raw[:first_p_end]).strip()
    assert byline == "6 October 2026 · Prasanth G, Recallant", byline
    s = raw[first_p_end:].lstrip()
    s = s.replace("<p>", '<p class="lead">', 1)
    s = re.sub(r'<tr class="(?:header|odd|even)">', "<tr>", s)
    s = s.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    s = s.replace('<a\nhref="http', '<a rel="noopener" href="http').replace('<a href="http', '<a rel="noopener" href="http')

    # Charts: visual twins of the tables that follow them; the text stays word for word.
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
    named_html = "".join(f'<li><span>{q}</span><span class="qlist__meta">{pips(5)}<span>First in 5 of 5</span></span></li>' for q in named)
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
          <h1 id="page-title">Freshdesk: what AI says today</h1>
          <p class="sheet__meta">Perplexity · 40 buyer questions about helpdesk software · 5 runs each · 6 October 2026</p>
        </div>
        <span class="stamp">{icon('doc')}Sample</span>
      </header>
      <div class="notice">{icon('info')}<p>This is a sample of the free snapshot, filled in with Freshdesk’s numbers from our <a href="helpdesk-study.html">public helpdesk study</a>. Freshdesk is not a client. Your snapshot uses 20 questions chosen for your product and competitors.</p></div>
      <div class="kpis">
        <div class="kpi"><strong>61%</strong><div class="meter" aria-hidden="true"><b style="width:61%"></b></div><span>of answers name Freshdesk</span></div>
        <div class="kpi"><strong>21%</strong><div class="meter" aria-hidden="true"><b style="width:21%"></b><s style="left:25%"></s></div><span>recommend it first (Zendesk: 25%)</span></div>
        <div class="kpi"><strong>13%</strong><div class="meter" aria-hidden="true"><b style="width:13%"></b><s style="left:21%"></s></div><span>cite Freshworks’ own site (Help Scout: 21%)</span></div>
      </div>
      <p class="kpi-key" aria-hidden="true"><span><i class="kk-bar"></i>Freshdesk</span><span><i class="kk-tick"></i>Leading rival</span></p>

      <section class="sheet__sec" aria-labelledby="s1">
        <h2 id="s1"><span>01</span>Where you’re named</h2>
        <p>Freshdesk is the most-named helpdesk, with the largest share of brand mentions (19%, against Zendesk’s 14%). It was recommended first in all 5 runs of these questions:</p>
        <ul class="qlist">{named_html}</ul>
      </section>

      <section class="sheet__sec" aria-labelledby="s2">
        <h2 id="s2"><span>02</span>Where you’re missing</h2>
        <div class="table-wrap"><table>
          <thead><tr><th>Buyer question</th><th>Freshdesk named</th><th>Recommended first instead</th></tr></thead>
          <tbody>{missing_html}</tbody>
        </table></div>
      </section>

      <section class="sheet__sec" aria-labelledby="s3">
        <h2 id="s3"><span>03</span>Which pages AI relies on</h2>
        <p>Answers cite listicles and other vendors’ blogs far more than Freshdesk’s own pages. The sites cited most, counted as answers out of 220:</p>
        <div class="hbars" role="img" aria-label="g2.com 56, getmacha.com 40, kayako.com 31 answers out of 220">{bars}</div>
        <p>On how-to questions, hubspot.com was cited in 20 of 50 answers, and freshworks.com in 9.</p>
      </section>

      <section class="sheet__sec" aria-labelledby="s4">
        <h2 id="s4"><span>04</span>What to fix first</h2>
        <ol class="fixes">
          <li><div><b>Answer the niche questions directly.</b><span>Publish pages for ecommerce support, shared inboxes and AI chatbots. Rivals win these because their pages match the question.</span></div></li>
          <li><div><b>Own the how-to questions.</b><span>Practical guides on SLAs, routing and WhatsApp support, where HubSpot’s blog is cited most today.</span></div></li>
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


# ================================================================== ABOUT

def about() -> None:
    timeline = [
        ("May 2026", "Recallant starts", "With one question: when buyers ask AI what to buy, who gets recommended, and why?", False),
        ("October 2026", "First public study", 'Helpdesk software: 44 buyer questions, 220 Perplexity answers, published with the method and its limits. <a class="text-link" href="helpdesk-study.html">Read it</a>.', False),
        ("October 2026", "IT management study", "44 ITSM and MSP buyer questions, 220 answers. Available on request.", False),
        ("Now", "Free snapshots for B2B brands", 'Send your product name and get a one-page snapshot. <a class="text-link" href="#get-snapshot">Request yours</a>.', True),
    ]
    tl = "".join(f'<li{" class=" + chr(34) + "is-now" + chr(34) if now else ""}><span class="kicker">{d}</span><h3>{t}</h3><p>{p}</p></li>'
                 for d, t, p, now in timeline)
    body = f"""<section class="band band--paper band--first page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow rise">About</p>
    <h1 class="h-display rise" style="--d:80" id="page-title">Measure first.</h1>
    <p class="lede rise" style="--d:160">Recallant started in May 2026 with one question: when buyers ask AI what to buy, who gets recommended, and why?</p>
  </div>
</section>

<section class="band band--paper band--flush">
  <div class="wrap about-intro">
    <div class="prose reveal">
      <h2>Why Recallant exists</h2>
      <p>Buyers used to search, click and compare. Now many ask an assistant and read one answer. That answer usually names three or four products. If yours isn’t one of them, you never hear about the deal you lost.</p>
      <p>Most advice about “AI SEO” is guesswork. We start by measuring: the same buyer questions, asked many times, with every answer and every cited source recorded. Then we work on what the data shows, and measure again.</p>

      <h2>How we work</h2>
      <ul>
        <li><strong>Evidence over opinion.</strong> Every recommendation points to the answers and sources behind it.</li>
        <li><strong>Honest limits.</strong> We say which assistants we measured, when, and what we didn’t measure.</li>
        <li><strong>Nothing fake.</strong> No bought reviews, links or mentions, ever.</li>
        <li><strong>Plain reporting.</strong> One page you can read in two minutes, not a dashboard you have to decode.</li>
      </ul>

      <h2>Founder</h2>
      <p>Recallant is run by Prasanth G, who has a background in IT and business analysis. Based in Bengaluru, India, working with B2B software companies everywhere.</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}" rel="noopener">LinkedIn</a></p>
    </div>
    <aside class="profile reveal" style="--d:120" aria-label="Founder">
      <img src="assets/img/prasanth-640.jpg" alt="Prasanth G, founder of Recallant" width="320" height="320">
      <div>
        <p class="profile__name">Prasanth G</p>
        <p class="profile__role">Founder, Recallant</p>
      </div>
      <dl>
        <div><dt>Based in</dt><dd>Bengaluru, India</dd></div>
        <div><dt>Background</dt><dd>IT and business analysis</dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>LinkedIn</dt><dd><a href="{LINKEDIN}" rel="noopener">View profile</a></dd></div>
      </dl>
    </aside>
  </div>
</section>

<section class="band band--mist" aria-labelledby="so-far-title">
  <div class="wrap wrap--text">
    <div class="section-head reveal">
      <p class="eyebrow">So far</p>
      <h2 class="h2" id="so-far-title">The story so far.</h2>
    </div>
    <ol class="timeline reveal">{tl}</ol>
  </div>
</section>"""
    about_ld = {"@type": "AboutPage", "url": SITE + "/about.html", "about": {"@id": ORG_ID}, "mainEntity": {"@id": PERSON_ID}}
    page(file="about.html", title="About Recallant",
         desc="Recallant measures what AI assistants say about B2B brands and improves it. Founded in May 2026 by Prasanth G, based in Bengaluru, India.",
         body=body, current="about.html",
         graph=[ORG, PERSON, about_ld, breadcrumbs([("About", SITE + "/about.html")])])


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
    pages = ["", "services.html", "plans.html", "research.html", "helpdesk-study.html", "sample-snapshot.html", "about.html"]
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{UPDATED}</lastmod></url>\n" for p in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "</urlset>\n")


LLMS = f"""# Recallant

> Recallant measures what AI assistants (ChatGPT, Gemini, Perplexity) say about B2B brands when buyers ask for recommendations, and improves the content, PR, website and listings those answers rely on. Based in Bengaluru, India. Founder: Prasanth G. Contact: {EMAIL}.

## Services
- [Services]({SITE}/services.html): AI visibility consulting, articles and reports, PR management, website creation and care, brand management.
- [Plans]({SITE}/plans.html): monthly plans (Visibility, Growth, Brand), website builds and one-off audits. Pricing on request after a free snapshot.

## Research
- [Helpdesk AI visibility study, October 2026]({SITE}/helpdesk-study.html): 44 buyer questions, 5 runs each, 220 Perplexity answers, with method and limits, and a question-by-question explorer.
- [Sample snapshot]({SITE}/sample-snapshot.html): what the free one-page snapshot looks like, using Freshdesk's numbers from the helpdesk study.

## About
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
    home()
    services()
    plans()
    research()
    study()
    sample()
    about()
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
            (out / name).write_text(doc)
        print("preview written to", out)
        return

    for name, doc in PAGES.items():
        (ROOT / name).write_text(doc)
    (ROOT / "sitemap.xml").write_text(sitemap())
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    (ROOT / "llms.txt").write_text(LLMS)
    (ROOT / "favicon.svg").write_text(favicon_svg())
    (HERE / "data" / "mark-square.svg").write_text(favicon_svg(rounded=False))
    print("built:", ", ".join(sorted(PAGES)))


if __name__ == "__main__":
    main(sys.argv[1:])
