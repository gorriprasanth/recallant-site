"""Optional final-page presentation pass for Recallant's evidence-led redesign.

Integration: import evidence_desk; evidence_desk.apply(b) after review_fixes.apply(b)
and before social_links.enrich. Does not write files, change research data, prices,
booking URLs, enquiry destinations or assets. Root provides scoped rc-ed-* CSS.
"""
import json
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup


def _fragment(markup):
    return BeautifulSoup(markup, 'html.parser')


def _remove_unverified_locality(value):
    if isinstance(value, dict):
        if value.get('addressLocality') == 'Bengaluru':
            value.pop('addressLocality')
        for child in value.values():
            _remove_unverified_locality(child)
    elif isinstance(value, list):
        for child in value:
            _remove_unverified_locality(child)


def _homepage(doc):
    cover = doc.select_one('.rc-cover')
    if cover is None:
        raise ValueError('Recallant homepage cover missing; do not silently drop content')
    cover['class'] = ['rc-cover', 'wrap', 'rc-ed-cover']
    cover.clear()
    cover.append(_fragment('''
<div class="rc-ed-lead">
  <p class="eyebrow">Search &amp; AI visibility / For B2B software</p>
  <h1 id="page-title">See where you appear.<br><em>Know what to improve.</em></h1>
  <p class="rc-deck">We examine the answers your buyers see, trace the sources behind them and turn the evidence into a focused website improvement brief.</p>
  <div class="ctas"><a class="btn btn--signal" href="sample-snapshot.html">Inspect a real research sample ↗</a><a class="arrow-link" href="plans.html">Choose a starting point ↗</a></div>
  <p class="rc-ed-scope-note">A saved answer is evidence of that answer, not a guarantee of future visibility. Fresh collection is separately scoped.</p>
</div>
<figure class="rc-ed-specimen">
 <figcaption><span class="eyebrow">Inside a Recallant snapshot</span><strong>One brand. Different buyer questions.</strong><span>Freshdesk · Historical research example</span></figcaption>
 <div class="rc-ed-table-wrap"><table><caption>Freshdesk mentions across five saved answers per question</caption><thead><tr><th scope="col">Buyer question</th><th scope="col">Named</th></tr></thead><tbody><tr><th scope="row">Helpdesk for a small business</th><td><strong>5 / 5</strong></td></tr><tr><th scope="row">Customer service for an ecommerce store</th><td><strong>0 / 5</strong></td></tr><tr><th scope="row">Helpdesk with the best AI chatbot</th><td><strong>3 / 5</strong></td></tr></tbody></table></div>
 <div class="rc-ed-annotation"><span class="eyebrow">What this tells us</span><p>Visibility varies with the question. An absence identifies something to investigate; it does not explain the cause.</p></div>
 <div class="rc-ed-annotation rc-ed-annotation--action"><span class="eyebrow">A useful next check</span><p>If ecommerce support fits the product, check whether its pages answer that buyer’s question clearly.</p></div>
 <p class="rc-ed-source">Perplexity · 6 October 2026. Extracted from our <a href="sample-snapshot.html">published Freshdesk sample</a>. Freshdesk is not a client. This is not live monitoring.</p>
</figure>'''))
    edition = doc.select_one('.rc-edition')
    if edition:
        edition.decompose()
    source_questions = json.loads((Path(__file__).parent / 'data/helpdesk-explorer.json').read_text(encoding='utf-8'))
    exact = {q['id']: q['q'] for q in source_questions}
    for row, key in zip(cover.select('tbody th'), ['d01', 'd05', 'd09']):
        row.string = exact[key]
    # Keep examples and service explanations on their dedicated pages.
    for extra in doc.select('.rc-cases-index, .rc-practice'):
        extra.decompose()
    # Existing sample area becomes a direct, bounded pilot offer.
    pilot = doc.select_one('.rc-fieldnote')
    if pilot:
        title = pilot.select_one('.rc-fieldnote-title')
        title.clear()
        title.append(_fragment('<p class="eyebrow">A defined first project</p><h2>One buyer question.<br><em>One clearer page.</em></h2><p>Review up to ten agreed public pages on one English-language domain. Receive up to five evidence-linked findings, one priority-page draft of up to 1,000 words and an enquiry recommendation.</p><p>Answer analysis uses up to 25 permitted captures you supply, across at most five agreed questions. Without those captures, this is a website review, not an AI visibility baseline. Fresh collection is separate.</p><a class="arrow-link" href="plans.html#visibility-pilot">Read the full scope and exclusions ↗</a>'))
        caption = pilot.select_one('.rc-fieldnote-caption')
        if caption:
            caption.clear()
            caption.append(_fragment('<a href="services.html">Explore the services</a> · <a href="use-cases.html">See illustrative use cases</a> · One consolidated factual and clarity revision.'))
    # Move the existing illustrative situations before the detailed archive.
    cases = doc.select_one('.rc-cases-index')
    if cases:
        cases.extract()
        cases['class'].append('rc-ed-situations')
        cover.insert_after(cases)
    practice = doc.select_one('.rc-practice')
    if practice and cases:
        practice.extract()
        cases.insert_after(practice)
    # Preserve the complete interactive explorer and its JS hooks, but make its
    # depth deliberate. Native details remains available without JavaScript.
    lab = doc.select_one('.rc-lab')
    sample = doc.select_one('.rc-fieldnote')
    if sample:
        sample.extract()
        cover.insert_after(sample)
    record = doc.select_one('.rc-record')
    if record:
        note = doc.new_tag('p', attrs={'class':'rc-ed-source'})
        note.string = 'Full archive: 44 questions, including four branded questions, and 220 answers. The explorer covers the 40 non-branded questions (200 answers). Five runs per question; collected 6 October 2026.'
        record.append(note)
    if record and sample:
        record.extract()
        sample.insert_after(record)
    if lab:
        lab.extract()
        if record:
            record.insert_after(lab)
        else:
            doc.main.append(lab)
        lab['class'].append('rc-ed-archive')
        lab_wrap = lab.select_one('.wrap')
        heading = lab.select_one('.rc-section-heading')
        if lab_wrap and heading:
            details = doc.new_tag('details', attrs={'class':'rc-ed-explorer-details'})
            summary = doc.new_tag('summary')
            summary.string = 'Open the six-question research explorer'
            details.append(summary)
            for child in list(lab_wrap.contents):
                if child is not heading:
                    details.append(child.extract())
            lab_wrap.append(details)
    report_section = _fragment('''<section class="wrap rc-ed-reading" aria-labelledby="rc-ed-reading-title">
<div class="rc-ed-reading-head"><p class="eyebrow">Recallant Fieldnotes</p><h2 id="rc-ed-reading-title">Research you can<br><em>put to work.</em></h2><p>Four illustrated reports on checking AI answers, choosing tools, interpreting visibility and understanding enquiries. Read online or download the PDFs from each issue.</p><a class="arrow-link" href="fieldnotes.html">Browse the complete library ↗</a></div>
<div class="rc-ed-issues">
<a href="fieldnotes-the-evidence-desk.html"><span class="eyebrow">Checking answers</span><h3>The Evidence Desk</h3><p>Check an AI answer before it reaches a customer.</p><span>Read the report ↗</span></a>
<a href="fieldnotes-the-tuesday-test.html"><span class="eyebrow">Choosing tools</span><h3>The Tuesday Test</h3><p>Choose an AI tool using the work you actually do.</p><span>Read the report ↗</span></a>
<a href="fieldnotes-named-cited-chosen.html"><span class="eyebrow">Reading visibility</span><h3>Named. Cited. Chosen?</h3><p>Separate being mentioned from being recommended.</p><span>Read the report ↗</span></a>
<a href="fieldnotes-the-enquiry-ledger.html"><span class="eyebrow">Following enquiries</span><h3>The Enquiry Ledger</h3><p>Find out which attention becomes a useful conversation.</p><span>Read the report ↗</span></a>
</div></section>''').section
    closing = doc.select_one('#get-snapshot')
    if closing:
        closing.insert_before(report_section)
        closing.extract()
        doc.main.append(closing)
    else:
        doc.main.append(report_section)


def apply(b):
    """Transform b.PAGES in memory; caller owns build, CSS and publication."""
    css = Path(__file__).resolve().parent.parent / 'assets/css/evidence-desk.css'
    version = hashlib.sha256(css.read_text(encoding='utf-8-sig').encode('utf-8')).hexdigest()[:10]
    for name, html in list(b.PAGES.items()):
        doc = BeautifulSoup(html, 'html.parser')
        if not doc.body or 'rc-ed-site' in doc.body.get('class', []):
            continue
        doc.body['class'] = [*doc.body.get('class', []), 'rc-ed-site']
        doc.head.append(doc.new_tag('link', rel='stylesheet', href='assets/css/evidence-desk.css?v=' + version))
        for script in doc.select('script[type="application/ld+json"]'):
            payload = json.loads(script.string or script.get_text())
            _remove_unverified_locality(payload)
            script.string = json.dumps(payload, ensure_ascii=False)
        nav = doc.select_one('nav.nav__links')
        if nav and not nav.select_one('a[href="fieldnotes.html"]'):
            link = doc.new_tag('a', href='fieldnotes.html')
            link.string = 'Fieldnotes'
            research = nav.select_one('a[href="research.html"]')
            if research:
                research.insert_after(link)
            else:
                nav.append(link)
        if name == 'index.html':
            _homepage(doc)
        elif name in ('services.html', 'research.html'):
            closing = doc.select_one('#get-snapshot')
            if closing:
                closing.extract()
                doc.main.append(closing)
        b.PAGES[name] = str(doc)
"""Locality in generated llms.txt is outside b.PAGES. The integrating release
must separately remove that unverified city from the llms() generator; do not
replace it with a precise residential address. Existing source evidence remains
untouched by this presentation module.
"""
