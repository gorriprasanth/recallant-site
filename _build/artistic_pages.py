"""Recallant's search-result identity and research-journal presentation.

Preserves historical evidence and enquiry destinations; owner-approved November 2026.
"""
import hashlib
from bs4 import BeautifulSoup


def home(b):
    explorer=b.explorer(b.HOME_QUESTIONS,'home',tabs=False,more='<p class="explorer__more">Six questions from the saved study. <a href="helpdesk-study.html#explore">Explore all 40 non-branded questions →</a></p>')
    body=f'''<div class="rc-edition wrap"><span>Independent research / Search &amp; AI visibility</span><span>For B2B software businesses</span></div>
<section class="rc-cover wrap" aria-labelledby="page-title">
 <div class="rc-cover-copy"><p class="eyebrow">Look beyond the mention.</p><h1 id="page-title">The answer is <br>not the <em>whole <br>story.</em></h1><p class="rc-deck">Understand where your brand appears in AI answers, which sources get cited, and what deserves attention next.</p><div class="ctas"><a class="btn btn--signal" href="research.html">Explore the evidence {b.icon('arrow')}</a><a class="arrow-link" href="services.html">What we do {b.icon('arrow')}</a></div></div>
 <figure class="rc-cover-art"><img src="assets/img/reading-aperture.svg" width="620" height="620" alt="An original optical print: a search lens reveals a highlighted result among overlapping circles"><figcaption><span>The visible result</span><span>Recallant / Original illustration</span></figcaption></figure>
</section>
<section class="rc-record wrap" aria-label="Published study scope"><div><span class="eyebrow">From our research archive</span><a href="helpdesk-study.html">Helpdesk software,<br>under examination. ↗</a><small>Perplexity · Collected 6 October 2026</small></div><dl><div><dt>Buyer questions</dt><dd>44</dd></div><div><dt>Saved answers</dt><dd>220</dd></div><div><dt>Runs per question</dt><dd>5</dd></div></dl></section>
<section class="rc-lab band band--paper" aria-labelledby="ask-title"><div class="wrap"><div class="rc-section-heading"><div><p class="eyebrow">The open notebook</p><h2 id="ask-title">Follow a question.<br><em>See who appears.</em></h2></div><p>Choose a question to inspect the brands named and sources cited across five saved answers. This is the 6 October study, not a live AI search.</p></div>{explorer}<p class="evidence-caption">First-named counts record order among tracked brands. A mention, a citation and an affirmative recommendation are different signals. <a href="method.html">Read the definitions ↗</a></p></div></section>
<section class="rc-practice band band--paper"><div class="wrap rc-practice-grid"><div><p class="eyebrow">Research with a next step</p><h2>Make the <br>evidence <br><em>useful.</em></h2><p>Start with one business decision. Agree the questions, sources and scope before work begins.</p><a class="arrow-link" href="services.html">Explore the services {b.icon('arrow')}</a></div><div class="rc-practice-list"><article><span class="rc-margin-note">Observe</span><div><h3>Visibility research</h3><p>Map brand mentions, source citations and question-level gaps across an agreed set of AI answers.</p><a href="services.html#visibility">See the research scope ↗</a></div></article><article><span class="rc-margin-note">Improve</span><div><h3>A clearer priority page</h3><p>Turn supported findings into a focused review, one priority-page draft and a clearer enquiry route.</p><a href="plans.html#visibility-pilot">Explore the Visibility &amp; Enquiry Pilot ↗</a></div></article><article><span class="rc-margin-note">Revisit</span><div><h3>Compare over time</h3><p>Agree a repeatable measurement scope and review what changes, alongside the work completed.</p><a href="plans.html#ongoing-support">Discuss ongoing support ↗</a></div></article></div></div></section>
<section class="rc-fieldnote wrap"><div class="rc-fieldnote-title"><p class="eyebrow">Inside a deliverable</p><h2>The findings.<br>The sources.<br><em>The next decision.</em></h2><p>Open the Freshdesk sample to see where a brand appears, where it is absent and which pages deserve investigation.</p><a class="btn btn--signal" href="sample-snapshot.html">Read the sample {b.icon('arrow')}</a></div><aside><p class="eyebrow">A focused starting point</p><h3>Visibility &amp;<br>Enquiry Pilot</h3><p class="rc-pilot-price">₹14,400</p><small>Plus applicable taxes</small><p>One domain. One buyer question. Up to five findings and one priority-page draft.</p><a href="plans.html#visibility-pilot">Read the complete scope ↗</a></aside><div class="rc-currency-slot" data-currency-controls></div><p class="rc-fieldnote-caption">The Freshdesk sample uses our published helpdesk research. It is a research example, not a client result. Fresh answer collection is a separate scope.</p></section>'''
    b.page(file='index.html',title='Recallant — see the evidence behind AI visibility',desc='AI search visibility research and focused website improvements for B2B software brands. Inspect the answers, understand the sources and decide what to improve.',body=body,tone='paper',graph=[b.ORG,b.PERSON])


def apply(b):
    wordmark=(b.HERE/'data/editorial-wordmark.svg').read_text(encoding='utf-8')
    # Git normalizes text line endings; hash normalized text on Windows and Linux alike.
    version=hashlib.sha256((b.ROOT/'assets/css/editorial.css').read_text(encoding='utf-8').encode('utf-8')).hexdigest()[:10]
    for name,html in list(b.PAGES.items()):
        doc=BeautifulSoup(html,'html.parser');doc.body['class']=['rc-editorial','rc-'+name.removesuffix('.html')]
        for logo in doc.select('a.brand'):
            logo.clear();logo.append(BeautifulSoup(wordmark.replace('role="img" aria-label="Recallant"','aria-hidden="true"'),'html.parser'))
        # Keep the studio relationship in the footer; give the specialist its own masthead.
        for note in doc.select('.brand__note'):note.decompose()
        doc.head.append(doc.new_tag('link',rel='stylesheet',href='assets/css/editorial.css?v='+version))
        doc.find('meta',attrs={'name':'theme-color'})['content']='#f7f5ed'
        if name!='helpdesk-study.html':
            for meta in doc.select('meta[property="og:image:alt"], meta[name="twitter:image:alt"]'):
                meta['content']='Recallant - Be found. Understand why. Search and AI visibility research.'
        if name=='services.html':
            doc.select_one('.offer-grid')['class'].append('rc-service-index')
        if name=='plans.html':
            doc.select_one('.offer-grid')['class'].append('rc-plan-index')
        if name=='research.html':
            hero=doc.select_one('.page-hero .wrap')
            hero.append(BeautifulSoup('<p class="rc-journal-tag">The Recallant research library / Evidence with its method attached</p>','html.parser'))
        b.PAGES[name]=str(doc)
