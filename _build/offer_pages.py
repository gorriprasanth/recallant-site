"""Recallant's scoped offers, measurement method and shared enquiry route.

These pages use the existing builder's shell. The historical research data is
owned by build.py and the retained study sources; nothing here rewrites it.
"""
from html import escape
from urllib.parse import urlencode


ENQUIRY_DESK = "https://signalandsyllable.com/contact"
CONTACT_EMAIL = "gorripatiprasanth@gmail.com"


def _enquiry(request):
    return escape(ENQUIRY_DESK + "?" + urlencode({"service": "Recallant", "request": request}), quote=True)


def _hero(label, title, intro):
    return f'''<section class="band band--paper band--first page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow">{label}</p>
    <h1 class="h-display" id="page-title">{title}</h1>
    <p class="lede">{intro}</p>
  </div>
</section>'''


def services(b):
    body = _hero("Services", "Turn the answer into<br>a useful next move.",
                 "Understand how your brand appears in a defined set of AI answers, connect the findings to your buyer’s decision, and choose what to improve first.")
    body += '''<section class="band band--mist" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">The work</p><h2 class="h2" id="services-title">Measure. Make sense. Improve.</h2></div>
    <div class="offer-grid">
      <article class="offer-card" id="visibility">
        <p class="eyebrow">Visibility review</p><h3>See the evidence behind the answer.</h3>
        <p>Start with the questions a buyer would actually ask. Inspect brand mentions, linked sources and first-named order across the agreed sample.</p>
        <ul class="detail-list"><li>A defined question set, market and competitor list</li><li>Agreed answer surfaces, collection method and dates</li><li>Separate observations for mentions and citations</li><li>A record of usable, missing and failed captures</li></ul>
        <a class="arrow-link" href="method.html">Read the method <span aria-hidden="true">↗</span></a>
      </article>
      <article class="offer-card" id="content">
        <p class="eyebrow">Priority improvements</p><h3>Give the buyer a clearer decision.</h3>
        <p>Translate supported findings into a focused action brief. Review the pages, product facts and buyer questions that matter before choosing what to write.</p>
        <ul class="detail-list"><li>Prioritised findings with the evidence alongside</li><li>Buyer-question and page mapping</li><li>Clearer product, comparison and decision-page copy</li><li>An enquiry recommendation tied to the buyer’s next step</li></ul>
        <a class="arrow-link" href="plans.html#visibility-pilot">Explore the Visibility Pilot <span aria-hidden="true">↗</span></a>
      </article>
      <article class="offer-card" id="monitoring">
        <p class="eyebrow">Agreed follow-up</p><h3>Compare changes on a consistent basis.</h3>
        <p>When repeat measurement is useful, agree the questions, cadence and source of each comparison. Keep edits and changes in the sample visible.</p>
        <ul class="detail-list"><li>A repeatable, agreed measurement scope</li><li>Comparable periods and clearly labelled exceptions</li><li>A change log for reviewed content and interpretations</li><li>A practical review of the next priorities</li></ul>
        <a class="arrow-link" href="contact.html#monitoring">Discuss ongoing support <span aria-hidden="true">↗</span></a>
      </article>
    </div>
  </div>
</section>
<section class="band band--paper" aria-labelledby="fit-title">
  <div class="wrap text-page">
    <p class="eyebrow">Built around your scope</p><h2 class="h2" id="fit-title">A useful question comes first.</h2>
    <p>Recallant is for B2B founders and marketing teams with a clear product, an identifiable buyer and someone who can act on the findings. Start with one decision: a shortlist, a comparison, a product-fit question or a useful demo enquiry.</p>
    <p>The platform, API or consumer-app surface, language, sample size and collection method are confirmed before work begins. Supplied saved answers and fresh collection are different scopes. Repeat measurement and implementation are agreed separately.</p>
    <p id="pr"><strong>Press and source outreach:</strong> <a class="text-link" href="https://signalandsyllable.com/pressroom">Pressroom</a> prepares scoped press materials and source opportunities; coverage is an editorial decision.</p><p id="websites"><strong>Website projects:</strong> <a class="text-link" href="https://signalandsyllable.com/pagecraft">Pagecraft</a> covers separately scoped website work.</p><p id="brand"><strong>Positioning:</strong> <a class="text-link" href="https://signalandsyllable.com/signal-map">Signal Map</a> helps clarify your message and buyer decision.</p><p>Need a broader website, editorial or positioning project? Recallant connects with the other services at <a class="text-link" href="https://signalandsyllable.com/">Signal &amp; Syllable</a>.</p>
    <a class="arrow-link" href="research.html">Explore the research <span aria-hidden="true">↗</span></a>
  </div>
</section>'''
    b.page(file="services.html", title="AI visibility research and practical improvements | Recallant",
           desc="A defined AI-answer sample, prioritised findings, buyer-focused content and agreed follow-up. Explore Recallant’s services.",
           body=body, current="services.html", tone="paper")


def plans(b):
    body = _hero("Ways to work together", "Start with the right<br>size of question.",
                 "A focused pilot, a broader visibility audit or an ongoing partnership. Choose the starting point; we confirm the scope before work begins.")
    body += '''<section class="band band--mist" aria-labelledby="offers-title">
  <div class="wrap">
    <h2 class="sr-only" id="offers-title">Recallant offers</h2>
    <div class="offer-grid">
      <article class="offer-card" id="snapshot">
        <p class="eyebrow">A first look</p><h2>Free snapshot</h2><p class="lede">Scope confirmed first</p>
        <p>Tell us your product, website and the question you want to understand. We review whether a small, relevant snapshot can give you a useful starting point.</p>
        <ul class="detail-list"><li>A short, agreed question and evidence scope</li><li>Available evidence and its date made clear</li><li>A concise observation and possible next step</li></ul>
        <p>We confirm what can be reviewed before preparing it. Fresh AI sampling, all-platform coverage and a fixed question count are not automatically included.</p>
        <a class="btn btn--quiet" href="contact.html#snapshot">Ask about a snapshot</a>
      </article>
      <article class="offer-card" id="visibility-pilot">
        <p class="eyebrow">A focused starting point</p><h2>Visibility &amp; Enquiry Pilot</h2><p class="lede">₹14,400 <small>plus applicable taxes</small></p>
        <p>One buyer, one decision and one priority page. A bounded website review with saved-answer analysis where the agreed evidence is available.</p>
        <ul class="detail-list"><li>One English-language domain, up to ten agreed public pages</li><li>Up to five prioritised, evidence-linked findings</li><li>One priority-page draft, up to 1,000 words</li><li>An enquiry recommendation and source-backed handover</li><li>One consolidated factual and clarity revision</li></ul>
        <a class="btn btn--signal" href="contact.html#pilot">Discuss the pilot</a>
      </article>
      <article class="offer-card" id="visibility-audit">
        <p class="eyebrow">A wider question set</p><h2>AI Visibility Audit</h2><p class="lede">Quoted to scope</p>
        <p>A dedicated measurement project for your category, competitors and buyer questions. A larger or freshly collected sample is specified in the proposal.</p>
        <ul class="detail-list"><li>Agreed questions, surfaces and sample design</li><li>Separate mention, citation and first-named observations</li><li>Competitor and source patterns within the sample</li><li>A prioritised improvement brief with supporting evidence</li></ul>
        <p>This is a separate engagement from the smaller Visibility &amp; Enquiry Pilot.</p>
        <a class="btn btn--quiet" href="contact.html#audit">Scope an audit</a>
      </article>
      <article class="offer-card" id="ongoing-support">
        <p class="eyebrow">After the first review</p><h2>Ongoing support</h2><p class="lede">Quoted to scope</p>
        <p>Build a repeatable programme around the priorities the first engagement identifies. Agree measurement, content and implementation responsibilities together.</p>
        <ul class="detail-list"><li>An agreed cadence and comparable question set</li><li>Selected content improvements and review points</li><li>Changes, missing evidence and next actions recorded</li><li>Deliverables and commercial terms confirmed in writing</li></ul>
        <p>Collection, publishing access and paid tools are agreed before they become part of the work.</p>
        <a class="btn btn--quiet" href="contact.html#monitoring">Discuss ongoing support</a>
      </article>
    </div>
  </div>
</section>
<section class="band band--paper" aria-labelledby="pilot-details-title">
  <div class="wrap text-page">
    <p class="eyebrow">The pilot, in detail</p><h2 class="h2" id="pilot-details-title">A clear beginning. A useful handover.</h2>
    <dl class="detail-list">
      <dt>Starting material</dt><dd>Your public domain, intended buyer, the decision to improve and confirmed product facts. For answer visibility, supply up to 25 authorised saved captures across at most five agreed questions, including dates and sources.</dd>
      <dt>Without saved answers</dt><dd>The pilot covers the agreed website pages. It does not report an AI-answer visibility baseline without the required evidence.</dd>
      <dt>Timing</dt><dd>Target first delivery is five working days after complete intake and a confirmed start date. Timing and terms are confirmed in the proposal.</dd>
      <dt>Revision</dt><dd>One consolidated round of factual corrections and clarity changes to the agreed scope, requested within seven calendar days of delivery. A different audience, page or offer needs a revised scope.</dd>
      <dt>Separate work</dt><dd>Fresh AI sampling, design/build work, publishing, ongoing monitoring, analytics setup, paid tools, outreach and additional domains or languages are not included in this pilot.</dd>
    </dl>
    <p>The handover links each finding to its source and makes the proposed change clear. A visibility review does not guarantee rankings, citations, recommendations, enquiries or revenue.</p>
    <a class="arrow-link" href="sample-snapshot.html">Inspect a research example <span aria-hidden="true">↗</span></a>
  </div>
</section>'''
    b.page(file="plans.html", title="Visibility Pilot, AI audit and ongoing support | Recallant",
           desc="Explore the ₹14,400 Visibility & Enquiry Pilot, a scoped free snapshot, a broader AI Visibility Audit and ongoing support.",
           body=body, current="plans.html", tone="paper")


def method(b):
    body = _hero("The method", "Keep the question.<br>Keep the evidence.",
                 "A useful visibility finding lets you inspect what was asked, what came back and how the conclusion was reached.")
    body += '''<section class="band band--mist" aria-labelledby="measures-title">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Read the measures correctly</p><h2 class="h2" id="measures-title">Different signals. Different meanings.</h2></div>
    <div class="offer-grid">
      <article class="offer-card"><h3>Brand mention</h3><p>The answer names the brand under the study’s stated matching rules. A mention can occur in a comparison, a criticism or a passing reference.</p></article>
      <article class="offer-card"><h3>Source citation</h3><p>The answer links to a retained source. An owned-domain citation and a third-party citation are separate observations; neither alone proves endorsement.</p></article>
      <article class="offer-card"><h3>First-named order</h3><p>The first tracked brand named under the study’s exclusions. This is an order proxy, not an affirmative recommendation or verified preference.</p></article>
      <article class="offer-card"><h3>Business outcomes</h3><p>Traffic, qualified enquiries and revenue need their own evidence and definitions. They cannot be inferred from a mention, citation or first-named position.</p></article>
    </div>
  </div>
</section>
<section class="band band--paper" aria-labelledby="record-title">
  <div class="wrap text-page">
    <p class="eyebrow">From sample to decision</p><h2 class="h2" id="record-title">Make every finding inspectable.</h2>
    <h3>Agree the question and the surface</h3>
    <p>Define the brand, competitors, exact questions, market, language, collection dates and permitted source. API results and consumer-app observations are recorded separately. An API response does not establish what every person will see in the consumer app.</p>
    <h3>Preserve the answer and the coverage</h3>
    <p>Retain the question, capture date, answer reference and source links. Count usable, failed and missing captures separately. A missing capture is not an answer that omitted the brand.</p>
    <h3>Show the denominator</h3>
    <p>A raw count such as “two of five saved answers” and a weighted aggregate answer different questions. Report the unit, eligible population and weighting. Share of voice is relative to the brands tracked; it is not market share.</p>
    <h3>Separate observation from interpretation</h3>
    <p>A changed question may produce a different answer. That observation does not by itself explain the cause or prove that rewriting a page will change the result. Recommendations to improve a page should state the evidence, the proposed action and what needs checking.</p>
    <h3>Compare like with like</h3>
    <p>For repeat work, keep the agreed question set and method consistent or explain what changed. Preserve the first report and issue dated corrections. A movement between samples does not establish that one edit caused it.</p>
    <h3>Read the public study in context</h3>
    <p>Our published helpdesk study retains its October 2026 data. It is original research, not a commissioned customer result or a current visibility check. Historical “top pick” or “recommended first” labels refer to the first-named order proxy described above. Affirmative recommendations were not separately classified.</p>
    <p><a class="text-link" href="helpdesk-study.html">Read the helpdesk study</a> or <a class="text-link" href="sample-snapshot.html">explore its sample snapshot</a>.</p>
  </div>
</section>'''
    b.page(file="method.html", title="How Recallant measures AI-answer visibility | Method",
           desc="Understand mentions, citations, first-named order, sample boundaries and evidence-led recommendations in Recallant’s reports.",
           body=body, current="method.html", tone="paper")


def contact(b):
    routes = [
        ("snapshot", "A free snapshot", "A focused first look at your product and buyer question. We confirm the available evidence and scope before preparing it.", "recallant-snapshot", "Request a snapshot"),
        ("pilot", "The Visibility & Enquiry Pilot", "The ₹14,400 pilot: a bounded website review, supported findings, one priority-page draft and an enquiry recommendation.", "recallant-pilot", "Discuss the pilot"),
        ("audit", "A wider AI Visibility Audit", "A dedicated question set, named competitors and an agreed collection method. We scope the sample and quote before work begins.", "recallant-audit", "Scope an audit"),
        ("monitoring", "Ongoing support", "Repeat measurement, selected improvements and a review cadence built around an agreed programme.", "recallant-monitoring", "Discuss ongoing support"),
    ]
    cards = "".join(f'''<article class="offer-card contact-route" id="{anchor}">
      <h2>{escape(title)}</h2><p>{escape(copy)}</p>
      <a class="btn btn--signal" href="{_enquiry(request)}">{escape(label)} <span aria-hidden="true">↗</span></a>
      <p class="small">Continues to Signal &amp; Syllable’s enquiry desk.</p>
    </article>''' for anchor, title, copy, request, label in routes)
    body = _hero("Start a conversation", "What would you like<br>to understand?",
                 "Choose a starting point. Recallant enquiries are handled through the shared Signal &amp; Syllable enquiry desk, with your interest selected.")
    body += f'''<section class="band band--mist" aria-label="Choose your Recallant enquiry"><div class="wrap offer-grid">{cards}</div></section>
<section class="band band--paper" aria-labelledby="next-title">
  <div class="wrap text-page">
    <p class="eyebrow">What happens next</p><h2 class="h2" id="next-title">Your question. A considered next step.</h2>
    <p>The link opens our shared form on signalandsyllable.com. Add your contact details, public website and the buyer question you want to explore. Review your brief there, then explicitly send it. Opening a link does not submit an enquiry.</p>
    <p>We use your enquiry to discuss fit, available evidence, scope and next steps. A submitted enquiry does not book a delivery slot or start a paid engagement.</p>
    <h3>Prefer email?</h3>
    <p>Write to <a class="text-link" href="mailto:{CONTACT_EMAIL}?subject=Recallant%20enquiry">{CONTACT_EMAIL}</a> with your product, public website and the question you want to answer. This is also the backup route if the shared form is unavailable.</p>
    <p>Share public material first. Leave passwords, API keys and private customer records out of your enquiry. Read <a class="text-link" href="privacy.html">how enquiries are handled</a>.</p>
  </div>
</section>'''
    b.cta_band_for["contact.html"] = ""
    b.page(file="contact.html", title="Discuss a snapshot, pilot or AI visibility audit | Recallant",
           desc="Choose your Recallant enquiry: a free snapshot, Visibility & Enquiry Pilot, wider audit or ongoing support. Review and send through our shared enquiry desk.",
           body=body, current="contact.html", tone="paper")


def privacy(b):
    provider = b.HOSTING_PROVIDER
    provider_url = "https://www.cloudflare.com/privacypolicy/" if provider == "Cloudflare" else "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"
    provider_label = "Cloudflare’s privacy policy" if provider == "Cloudflare" else "GitHub’s privacy statement"
    body = _hero("Privacy", "A clear route<br>for your enquiry.",
                 "Recallant is part of Signal & Syllable. This page explains what happens when you browse this website or contact us.")
    body += f'''<section class="band band--paper" aria-labelledby="privacy-title">
  <div class="wrap text-page">
    <h2 class="h2" id="privacy-title">Browsing recallant.com</h2>
    <p>Shared links can carry four short labels for their source, link type, campaign and content reference. With JavaScript available, valid labels follow page links on this website and the four Recallant enquiry choices into the shared studio form. We do not save them in cookies or browser storage, collect a full referring URL or add visitor analytics. The form shows the labels so you can clear them before reviewing and sending your enquiry.</p>
    <p>This is a static website hosted through {provider}. We have not added analytics, advertising trackers or a local enquiry form to this version. The research explorer works in your browser with the published study data; choosing a question does not send us your contact details.</p>
    <p>The hosting provider may process technical request information, such as IP address, browser details and access logs, to serve and protect the website. Its handling is described in <a class="text-link" href="{provider_url}">{provider_label}</a>.</p>
    <h3>Using the shared enquiry desk</h3>
    <p>Enquiry buttons take you to signalandsyllable.com, where Signal &amp; Syllable operates the shared form. The link passes your selected Recallant interest; it does not submit personal information from this website.</p>
    <p>On that form, the contact details and project information you choose to submit are processed through Cloudflare hosting and AgentMail email delivery, then sent to our receiving email account. The form includes a review step and requires an explicit send action. Read the <a class="text-link" href="https://signalandsyllable.com/privacy">Signal &amp; Syllable privacy notice</a> before submitting.</p>
    <h3>Contacting us by email</h3>
    <p>An email link opens your email application. Sending your message shares its contents and address with our receiving email service at <a class="text-link" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. We use an enquiry to respond and discuss the requested work; it does not subscribe you to marketing updates.</p>
    <h3>What to share</h3>
    <p>Use public links and a brief description of your business question. Do not send passwords, account keys, private customer records or confidential documents through the initial enquiry route. Any additional material needed for an engagement is agreed separately.</p>
    <h3>Questions or corrections</h3>
    <p>For questions about an enquiry, or to request a correction or deletion, contact <a class="text-link" href="mailto:{CONTACT_EMAIL}?subject=Recallant%20privacy%20request">{CONTACT_EMAIL}</a>. Include enough information for us to identify your request without resending sensitive material. Handling follows the shared enquiry privacy notice linked above.</p>
    <h3>Other websites</h3>
    <p>Research sources, LinkedIn and other external links have their own privacy practices. Clicking those links takes you to the relevant provider’s website.</p>
  </div>
</section>'''
    b.cta_band_for["privacy.html"] = ""
    b.page(file="privacy.html", title="Privacy and enquiry handling | Recallant",
           desc="How Recallant’s static website and shared Signal & Syllable enquiry desk handle browsing and contact information.",
           body=body, current="privacy.html", tone="paper")
