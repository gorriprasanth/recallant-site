"""Final Recallant intelligence-house presentation. Historical evidence is unchanged."""
import hashlib
from bs4 import BeautifulSoup


def fragment(value):
    return BeautifulSoup(value, 'html.parser')


ROUTES = [('services.html', 'Services'), ('plans.html', 'Plans & fees'), ('sample-snapshot.html', 'Sample'), ('helpdesk-study.html', 'Research'), ('fieldnotes.html', 'Fieldnotes')]
TITLES = dict(ROUTES + [('method.html','Method'),('about.html','About Recallant'),('contact.html','Start an enquiry'),('use-cases.html','Use cases'),('privacy.html','Privacy')])


def symbol(kind):
    paths = {
      'question': '<path d="M7 9h42v30H26L14 49V39H7z"/><path d="M22 20c0-7 13-7 13 0 0 5-7 4-7 10m0 5h.01"/>',
      'answer': '<rect x="10" y="5" width="37" height="46" rx="3"/><path d="M18 16h20m-20 8h20m-20 8h12m-12 8h20"/><path d="m36 48 6 6 11-13"/>',
      'source': '<rect x="6" y="7" width="30" height="38" rx="2"/><path d="M13 16h16m-16 7h16m-16 7h8"/><path d="m31 42 8-8c8-8 18 2 10 10l-7 7c-5 5-12 1-12-3m6-6 4-4"/>',
      'page': '<rect x="7" y="6" width="44" height="45" rx="3"/><path d="M7 16h44M16 25h25m-25 7h17M16 42h13m8-5 5 5-5 5m5-5H31"/>'
    }
    return '<svg class="rj-symbol" viewBox="0 0 58 58" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[kind]+'</svg>'


def directory(current):
    links=''.join('<a href="'+url+'"'+(' aria-current="page"' if current==url else '')+'>'+label+'</a>' for url,label in ROUTES)
    return '<nav class="rj-directory" aria-label="Explore Recallant"><div class="wrap rj-directory-desktop">'+links+'</div><details class="wrap rj-directory-mobile"><summary>Explore Recallant <span aria-hidden="true">+</span></summary><div>'+links+'</div></details></nav>'


def home():
    hero='<section class="rj-identity"><img class="rj-optical-art" src="assets/img/recallant-optical-hero.webp" width="1536" height="1024" alt="Original Recallant artwork: an optical lens revealing layers of evidence pages" fetchpriority="high" decoding="async"/><div class="wrap rj-identity-copy"><p class="eyebrow">Search &amp; AI visibility / For B2B teams</p><h1 id="page-title">What do AI answers<br>say about you?</h1><p class="rj-deck">We review your website and saved AI answers, then prioritise what to explain, verify or improve.</p><div class="ctas"><a class="btn btn--signal" href="#rj-choose-title">Choose your starting point</a><a class="arrow-link" href="sample-snapshot.html">Inspect a sample ↗</a></div></div><div class="wrap rj-identity-caption"><span>Recallant / A specialist business from Signal &amp; Syllable</span><span>Original optical artwork</span></div></section>'
    offers='<section class="wrap rj-choose" aria-labelledby="rj-choose-title"><div class="rj-section-heading"><p class="eyebrow">Two focused starting points</p><h2 id="rj-choose-title">Choose your starting point.</h2></div><div class="rj-offers"><article><div><p class="rj-offer-type">Improve the website</p><h3>Visibility &amp; Enquiry Pilot</h3><p>One domain, up to ten pages. Up to five evidence-linked findings, one priority-page draft and one consolidated revision.</p></div><div class="rj-offer-footer"><p class="rj-fee">₹14,400 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-pilot">See the pilot scope ↗</a></div></article><article><div><p class="rj-offer-type">Understand AI visibility</p><h3>AI Visibility Audit</h3><p>One domain, one priority audience and an agreed evidence set. An improvement brief and one consolidated revision.</p></div><div class="rj-offer-footer"><p class="rj-fee"><small>From</small> ₹45,000 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-audit">Explore the audit ↗</a></div></article></div><p class="rj-scope-note">Pilot evidence: up to 25 authorised captures you supply, across five questions. Without captures: website review only, not an AI baseline. Fresh collection and paid tools cost extra. <a href="plans.html">Full scope and exclusions</a>.</p><div class="rj-currency" data-currency-controls=""></div></section>'
    rows=[('What is the best helpdesk software for a small business?',5),('Which customer service platform is best for an ecommerce store?',0),('Which helpdesk has the best AI chatbot for customer support?',3)]
    trace='<div class="rj-inline-trace" aria-label="Evidence review process">'+''.join('<div>'+symbol(kind)+'<span>'+label+'</span></div>' for kind,label in [('question','Keep the question'),('answer','Save the answer'),('source','Check the citation'),('page','Review the page')])+'</div>'
    evidence='<section class="wrap rj-observation"><div><p class="eyebrow">Retained research / 6 October 2026</p><h2>Same brand.<br>Different questions.</h2><p>Freshdesk mentions across five saved Perplexity answers per question.</p>'+trace+'<p class="rj-reading-note">A missing mention is a reason to investigate, not proof of its cause.</p><a class="arrow-link" href="sample-snapshot.html">Inspect the sample ↗</a></div><figure><figcaption>Mentions, not recommendations</figcaption>'+''.join('<div class="rj-result"><p>'+question+'</p><div><span class="rj-result-dots" aria-hidden="true">'+''.join('<i'+(' class="filled"' if i<count else '')+'></i>' for i in range(5))+'</span><strong>'+str(count)+' / 5</strong></div></div>' for question,count in rows)+'<p class="rj-source-note">Historical observations, not live monitoring. Freshdesk is not a client. The retained study covers 44 questions and 220 answers; the explorer exposes 40 questions.</p><a class="arrow-link" href="helpdesk-study.html">Study and limitations ↗</a></figure></section>'
    library='<aside class="wrap rj-library-invite" aria-labelledby="rj-library-title"><div><p class="eyebrow">Fieldnotes / Research library</p><h2 id="rj-library-title">Go deeper when you need to.</h2><p>Four practical guides to AI evidence, tool selection and enquiries. Read online or keep the PDF.</p></div><a class="arrow-link" href="fieldnotes.html">Explore Fieldnotes ↗</a></aside>'
    close='<section class="rj-close"><div class="wrap"><h2>Bring the question.<br>We’ll agree the scope.</h2><a class="btn btn--signal" href="contact.html">Start an enquiry</a></div></section>'
    return hero+offers+evidence+library+close


def apply(b):
    css=b.ROOT/'assets/css/journal-direction.css'
    version=hashlib.sha256(css.read_bytes()).hexdigest()[:10]
    for name,html in list(b.PAGES.items()):
        doc=BeautifulSoup(html,'html.parser')
        if not doc.body:continue
        doc.body['class']=list(dict.fromkeys([*doc.body.get('class',[]),'rc-journal']))
        if doc.head:
            for old in doc.select('link[href^="assets/css/journal-direction.css"]'):old.decompose()
            doc.head.append(doc.new_tag('link',rel='stylesheet',href='assets/css/journal-direction.css?v='+version))
        main=doc.find('main')
        nav=doc.select_one('header.nav')
        for old in doc.select('.rj-directory,.rj-breadcrumb,.rj-page-next'):old.decompose()
        if nav and name!='index.html':nav.insert_after(fragment(directory(name)))
        if name=='index.html':
            if not main:raise ValueError('Missing Recallant homepage main')
            main.clear()
            main['class']=list(dict.fromkeys(main.get('class',[])+['rj-home']))
            main.append(fragment(home()))
            if doc.title:doc.title.string='Recallant — Search & AI Visibility for B2B Teams'
            for meta in doc.select('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]'):
                meta['content']='Understand what saved AI answers say about your category, and what your website needs to explain better. Evidence-led reviews for B2B teams.'
        elif main:
            if name=='services.html':
                fit=doc.select_one('section[aria-labelledby="fit-title"] .text-page')
                if fit:
                    fit.clear()
                    fit.append(fragment('<p class="eyebrow">The right fit</p><h2 id="fit-title">A clear buyer. A question worth answering.</h2><p>For B2B teams with a defined product and someone ready to act on the findings. Evidence collection, repeat measurement and implementation are agreed separately.</p><p><span id="pr"></span><span id="websites"></span><span id="brand"></span>Need broader positioning, website or campaign work? <a href="https://signalandsyllable.com/what-we-do">Explore Signal &amp; Syllable</a>. These projects are scoped separately.</p>'))
            if name=='plans.html':
                terms=doc.select_one('section[aria-labelledby="pilot-details-title"] .text-page')
                if terms and not terms.select_one('details.rj-pilot-terms'):
                    for old in terms.select('.eyebrow,#pilot-details-title'):old.decompose()
                    details=doc.new_tag('details',attrs={'class':'rj-pilot-terms'})
                    summary=doc.new_tag('summary',id='pilot-details-title')
                    summary.string='Pilot inputs, timing and exclusions'
                    details.append(summary)
                    content=doc.new_tag('div',attrs={'class':'rj-pilot-terms-body'})
                    for child in list(terms.contents):content.append(child.extract())
                    details.append(content);terms.append(details)
            title=TITLES.get(name)
            if not title:
                h=main.find('h1');title=h.get_text(' ',strip=True) if h else 'Recallant'
            crumb=doc.new_tag('nav',attrs={'class':'wrap rj-breadcrumb','aria-label':'Breadcrumb'})
            link=doc.new_tag('a',href='index.html');link.string='Recallant home';crumb.append(link)
            sep=doc.new_tag('span',attrs={'aria-hidden':'true'});sep.string='/';crumb.append(sep)
            current=doc.new_tag('span',attrs={'aria-current':'page'});current.string=title;crumb.append(current)
            main.insert_before(crumb)
            sequence=['services.html','plans.html','sample-snapshot.html','method.html']
            if name in sequence:
                idx=sequence.index(name);previous=sequence[(idx-1)%len(sequence)];following=sequence[(idx+1)%len(sequence)]
                main.append(fragment('<nav class="wrap rj-page-next" aria-label="Related pages"><a href="'+previous+'"><small>Explore</small>← '+TITLES[previous]+'</a><a href="'+following+'"><small>Continue to</small>'+TITLES[following]+' →</a></nav>'))
        for closing in doc.select('.closing-cta'):
            lead=closing.select_one('.lede')
            if lead:lead.string='Tell us the question. We will agree the evidence, scope and fee.'
            heading=closing.select_one('h2')
            if heading:heading.string='Ready for a clearer next step?'
        b.PAGES[name]=str(doc)
