"""Final visual direction: a specialist research journal, preserving all evidence."""
import hashlib
from bs4 import BeautifulSoup


def fragment(value):
    return BeautifulSoup(value, 'html.parser')


def apply(b):
    css = b.ROOT / 'assets/css/journal-direction.css'
    version = hashlib.sha256(css.read_text(encoding='utf-8').encode()).hexdigest()[:10]
    for name, html in list(b.PAGES.items()):
        doc = BeautifulSoup(html, 'html.parser')
        if not doc.body:
            continue
        doc.body['class'] = [*doc.body.get('class', []), 'rc-journal']
        doc.head.append(doc.new_tag('link', rel='stylesheet', href='assets/css/journal-direction.css?v=' + version))
        nav = doc.select_one('header.nav')
        if nav:
            nav.insert_after(fragment('''<nav class="rj-directory" aria-label="Find your Recallant starting point"><div class="wrap"><span>Find your starting point</span><a href="plans.html#visibility-pilot">Website &amp; enquiry pilot</a><a href="plans.html#visibility-audit">AI visibility audit</a><a href="sample-snapshot.html">See a sample</a><a href="fieldnotes.html">Read Fieldnotes</a></div></nav>'''))
        if name == 'index.html':
            cover = doc.select_one('.rc-cover')
            if not cover:
                raise ValueError('Missing Recallant homepage cover')
            cover.clear()
            cover['class'] = ['rj-hero', 'wrap']
            cover.append(fragment('''<div class="rj-hero-copy"><p class="eyebrow">Search visibility. Answer intelligence.</p><h1 id="page-title">When buyers ask,<br><em>do you appear?</em></h1><p class="rj-deck">Find out what AI answers say about your category—and what your website needs to explain better.</p><p>A dated evidence brief and a practical page-improvement plan. For B2B founders and marketing teams.</p><div class="ctas"><a class="btn btn--signal" href="#rj-choose-title">Find the right starting point ↗</a><a class="arrow-link" href="sample-snapshot.html">Look inside a sample ↗</a></div><div class="rj-byline"><span>By Signal &amp; Syllable</span><span>Research → interpretation → action</span></div></div><figure class="rj-hero-art"><div class="rj-art-frame"><img src="assets/img/recallant-evidence-stilllife.webp" width="1024" height="1280" alt="Original editorial still life: transparent glass over research pages, with saffron highlights on a cobalt work surface" fetchpriority="high"/><div class="rj-art-caption"><span>The useful part of an answer</span><strong>What can<br>you verify?</strong></div></div><figcaption>Original concept artwork. Research examples below use dated, inspectable evidence.</figcaption></figure>'''))
            # One simple service decision comes before the deeper research material.
            picker = fragment('''<section class="rj-choose wrap" aria-labelledby="rj-choose-title"><div class="rj-section-title"><p class="eyebrow">Two ways to begin</p><h2 id="rj-choose-title">What do you<br><em>need to know?</em></h2><p>You can start small. Choose the decision you need help with; we agree the scope before work begins.</p></div><div class="rj-choices"><article><span class="rj-choice-label">Improve the website</span><h3>“Our pages need to<br>answer buyers better.”</h3><p>Start with the Visibility &amp; Enquiry Pilot: a focused website review, up to five evidence-linked findings and one priority-page draft.</p><p class="rj-fee">₹14,400 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-pilot">See the pilot scope ↗</a></article><article><span class="rj-choice-label">Understand AI visibility</span><h3>“What do AI answers<br>say about our category?”</h3><p>Start with an AI Visibility Audit. Agree the questions, answer evidence and comparisons, then examine where your business appears.</p><p class="rj-fee">From ₹45,000 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-audit">Explore an audit ↗</a></article></div><p class="rj-scope-note">The pilot analyses up to 25 permitted answer captures you supply. Without captures, it is a website review—not an AI visibility baseline. Fresh collection is separately scoped. <a href="plans.html">Compare all offers and exclusions</a>.</p></section>''').section
            cover.insert_after(picker)
            # The detailed pilot is already on Plans; avoid making visitors read it twice.
            pilot = doc.select_one('.rc-fieldnote')
            if pilot:
                pilot.decompose()
            evidence = fragment('''<section class="rj-evidence" aria-labelledby="rj-evidence-title"><div class="wrap"><div class="rj-evidence-intro"><p class="eyebrow">Look behind the headline</p><h2 id="rj-evidence-title">A mention is a clue.<br><em>Follow it.</em></h2><p>Our work follows the evidence from the buyer’s question to the page you can improve. No mystery score required.</p></div><ol class="rj-evidence-path"><li><span>01 / The question</span><h3>What is the buyer<br>trying to decide?</h3><p>Define the product, audience and decision before interpreting an answer.</p></li><li><span>02 / The answer</span><h3>Who appears?<br>In what context?</h3><p>Separate a mention from an actual recommendation. Keep the saved answer and its date.</p></li><li><span>03 / The source</span><h3>What does the<br>citation support?</h3><p>Open the source. Check the passage, relevance and limits—not only the link.</p></li><li><span>04 / The improvement</span><h3>What should your<br>page explain?</h3><p>Turn supported findings into a useful page brief. An absence alone does not explain its cause.</p></li></ol><a class="arrow-link" href="method.html">Read the research method ↗</a></div></section>''').section
            picker.insert_after(evidence)
            research_sample = fragment('''<section class="rj-observation wrap" aria-labelledby="rj-observation-title"><div><p class="eyebrow">A finding you can inspect</p><h2 id="rj-observation-title">Same brand.<br><em>Different questions.</em></h2><p>Freshdesk appeared in all five saved answers to the small-business question—and none of the five ecommerce answers below.</p><p>That difference tells us where to investigate. It does not tell us why it happened.</p><a class="arrow-link" href="sample-snapshot.html">Open the complete sample ↗</a></div><figure><figcaption>Freshdesk mentions / five saved answers per question</figcaption><div class="rj-result"><p>What is the best helpdesk software for a small business?</p><div><span aria-hidden="true">● ● ● ● ●</span><strong>5 / 5</strong></div></div><div class="rj-result"><p>Which customer service platform is best for an ecommerce store?</p><div><span aria-hidden="true">○ ○ ○ ○ ○</span><strong>0 / 5</strong></div></div><div class="rj-result"><p>Which helpdesk has the best AI chatbot for customer support?</p><div><span aria-hidden="true">● ● ● ○ ○</span><strong>3 / 5</strong></div></div><p class="rj-scope-note">Perplexity · 6 October 2026 · Historical research, not live monitoring. Freshdesk is not a client. Counts show mentions, not recommendations.</p></figure></section>''').section
            evidence.insert_after(research_sample)
            reading = doc.select_one('.rc-ed-reading')
            if reading:
                reading['class'] = ['wrap', 'rj-library']
                reading.clear()
                reading.append(fragment('''<div class="rj-section-title"><p class="eyebrow">The Recallant reading room</p><h2 id="rc-ed-reading-title">Big questions.<br><em>Readable answers.</em></h2><p>Four illustrated field guides. Clear summaries, practical examples and the detail behind them. Read online or keep the PDF.</p><a class="arrow-link" href="fieldnotes.html">Enter the reading room ↗</a></div><div class="rj-books">'''+''.join(f'''<a class="rj-book" href="fieldnotes-{slug}.html"><img src="assets/fieldnotes/{slug}-01.svg" width="595" height="842" loading="lazy" alt="{title} report cover"/><span>{topic}</span><h3>{title}</h3><p>{desc}</p></a>''' for slug,title,topic,desc in [
                    ('the-evidence-desk','The Evidence Desk','Trusting an answer','Check what an AI answer can actually support.'),
                    ('the-tuesday-test','The Tuesday Test','Choosing AI tools','Test a tool against the work you really do.'),
                    ('named-cited-chosen','Named. Cited. Chosen?','Understanding visibility','Being mentioned is not being recommended.'),
                    ('the-enquiry-ledger','The Enquiry Ledger','Following the enquiry','See which attention becomes a useful conversation.')])+'</div>'))
                reading.extract()
                record=doc.select_one('.rc-record')
                if record:
                    record.insert_after(reading)
            # Currency display stays available even after removing the old pilot block.
            picker.append(fragment('<div class="rj-currency" data-currency-controls=""></div>'))
        if name == 'services.html':
            first = doc.select_one('.page-hero .wrap')
            if first:
                first.append(fragment('''<div class="rj-service-route"><a href="#visibility"><strong>Understand</strong><span>Questions, saved answers and sources</span></a><a href="#content"><strong>Improve</strong><span>A clearer page and next step</span></a><a href="#monitoring"><strong>Revisit</strong><span>An agreed comparison over time</span></a></div>'''))
        b.PAGES[name] = str(doc)
