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
    hero='<section class="rj-identity"><img class="rj-optical-art" src="assets/img/recallant-optical-hero.webp" width="1536" height="1024" alt="Original Recallant artwork: an optical lens revealing layers of evidence pages" fetchpriority="high" decoding="async"/><div class="wrap rj-identity-copy"><p class="eyebrow">Search &amp; AI visibility / For B2B teams</p><h1 id="page-title">When buyers ask,<br>where do<br>you stand?</h1><p class="rj-deck">Understand what saved AI answers say about your category. Find what your website needs to explain better.</p><div class="ctas"><a class="btn btn--signal" href="#rj-choose-title">Choose your starting point</a><a class="arrow-link" href="sample-snapshot.html">Inspect a sample ↗</a></div></div><div class="wrap rj-identity-caption"><span>Recallant / A specialist business from Signal &amp; Syllable</span><span>Original optical artwork</span></div></section>'
    offers='<section class="wrap rj-choose" aria-labelledby="rj-choose-title"><div class="rj-section-heading"><p class="eyebrow">Two focused starting points</p><h2 id="rj-choose-title">A clearer page.<br>A better-informed decision.</h2></div><div class="rj-offers"><article><div><p class="rj-offer-type">Improve the website</p><h3>Visibility &amp; Enquiry Pilot</h3><p>One domain, up to ten pages. Up to five evidence-linked findings, one priority-page draft and one consolidated revision.</p></div><div class="rj-offer-footer"><p class="rj-fee">₹14,400 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-pilot">See the pilot scope ↗</a></div></article><article><div><p class="rj-offer-type">Understand AI visibility</p><h3>AI Visibility Audit</h3><p>One domain, one priority audience and an agreed evidence set. An improvement brief and one consolidated revision.</p></div><div class="rj-offer-footer"><p class="rj-fee"><small>From</small> ₹45,000 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-audit">Explore the audit ↗</a></div></article></div><p class="rj-scope-note">The pilot can analyse up to 25 authorised captures you supply across at most five questions. Without captures, it is a website review—not an AI visibility baseline. Fresh collection and paid tools are separately scoped. <a href="plans.html">Full scope and exclusions</a>.</p><div class="rj-currency" data-currency-controls=""></div></section>'
    nodes=[('question','The question','“Best helpdesk for a small business?”'),('answer','The answer','Freshdesk appeared in five saved answers.'),('source','The source','Inspect the citations and their actual support.'),('page','The next check','Verify relevance before proposing a page change.')]
    diagram='<section class="rj-trace"><div class="wrap"><div class="rj-section-heading"><p class="eyebrow">How evidence becomes useful</p><h2>Keep the question<br>attached to the answer.</h2></div><div class="rj-trace-flow">'+''.join('<div>'+symbol(kind)+'<h3>'+title+'</h3><p>'+copy+'</p></div>' for kind,title,copy in nodes)+'</div><div class="rj-trace-foot"><p>Illustrated with the dated study below. A missing mention does not establish its cause.</p><a class="arrow-link" href="method.html">Read the method ↗</a></div></div></section>'
    rows=[('What is the best helpdesk software for a small business?',5),('Which customer service platform is best for an ecommerce store?',0),('Which helpdesk has the best AI chatbot for customer support?',3)]
    evidence='<section class="wrap rj-observation"><div><p class="eyebrow">Retained research / 6 October 2026</p><h2>Same brand.<br>Different questions.</h2><p>Freshdesk mentions across five saved Perplexity answers per question.</p><a class="arrow-link" href="sample-snapshot.html">Open the full sample ↗</a></div><figure><figcaption>Mentions, not recommendations</figcaption>'+''.join('<div class="rj-result"><p>'+question+'</p><div><span class="rj-result-dots" aria-hidden="true">'+''.join('<i'+(' class="filled"' if i<count else '')+'></i>' for i in range(5))+'</span><strong>'+str(count)+' / 5</strong></div></div>' for question,count in rows)+'<p class="rj-source-note">Historical observations, not live monitoring. Freshdesk is not a client. The retained study covers 44 questions and 220 answers; the explorer exposes 40 questions.</p><a class="arrow-link" href="helpdesk-study.html">Study and limitations ↗</a></figure></section>'
    reports=[('the-evidence-desk','The Evidence Desk','What does an answer actually support?'),('the-tuesday-test','The Tuesday Test','Choose tools by testing real work.'),('named-cited-chosen','Named. Cited. Chosen?','A mention is not a recommendation.'),('the-enquiry-ledger','The Enquiry Ledger','Follow attention into useful conversations.')]
    library='<section class="wrap rj-library"><div class="rj-library-heading"><div><p class="eyebrow">Fieldnotes</p><h2>Read deeper.<br>Leave clearer.</h2></div><a class="arrow-link" href="fieldnotes.html">All reports &amp; PDFs ↗</a></div><div class="rj-reading-list">'+''.join('<a href="fieldnotes-'+slug+'.html"><h3>'+title+'</h3><span>'+desc+'</span><b aria-hidden="true">↗</b></a>' for slug,title,desc in reports)+'</div></section>'
    close='<section class="rj-close"><div class="wrap"><h2>Bring the question.<br>We’ll agree the scope.</h2><a class="btn btn--signal" href="contact.html">Start an enquiry</a></div></section>'
    return hero+offers+diagram+evidence+library+close


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
        b.PAGES[name]=str(doc)
