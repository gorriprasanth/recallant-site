"""Recallant's specialist introduction, grounded in the retained public study."""


def home(b):
    explorer = b.explorer(b.HOME_QUESTIONS, 'home', tabs=False, more='<p class="explorer__more">Six questions from the saved study. <a href="helpdesk-study.html#explore">Explore all 40 →</a></p>')
    body = f'''<section class="band band--night band--first recallant-hero" aria-labelledby="page-title">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">AI search visibility · B2B software</p>
      <h1 id="page-title">Be the answer<span class="dot">.</span><br><span class="hero-secondary">Start with <br>the evidence.</span></h1>
      <p class="lede">Understand where your brand appears in AI answers, which sources get cited, and what deserves attention next.</p>
      <div class="ctas"><a class="btn btn--signal" href="contact.html">Find your starting point {b.icon('arrow')}</a><a class="arrow-link" href="sample-snapshot.html">See a real sample</a></div>
      <p class="hero-caption">Research, a focused improvement pilot, and scoped ongoing support.</p>
    </div>
    <a class="evidence-window" href="helpdesk-study.html" aria-label="Read the helpdesk study behind this comparison">
      <div class="evidence-window__top"><span class="status-dot"></span>RECALLANT / EVIDENCE NOTE <span>↗</span></div>
      <p class="kicker">Help Scout · Helpdesk study</p>
      <h2>A source in the answer.<br>A different place in the list.</h2>
      <div class="signal-bars"><div><span>Own site cited</span><b>21%</b><i style="--bar:84%"></i></div><div><span>First brand named</span><b>7%</b><i style="--bar:28%"></i></div></div>
      <p class="evidence-reading">Being cited and being named first measure different things. Neither alone tells you whether a buyer chose the product.</p>
      <div class="evidence-window__foot">Perplexity · 6 Oct 2026<br>Weighted study rates · naming order is a proxy</div>
    </a>
  </div>
</section>
<div class="research-strip"><div class="wrap"><span><strong>220</strong> saved Perplexity answers</span><span><strong>44</strong> buyer questions</span><span><strong>5</strong> runs per question</span><a href="method.html">Read the measurement method ↗</a></div></div>
<section class="band band--paper" aria-labelledby="ask-title"><div class="wrap">
  <div class="section-head split-head"><div><p class="eyebrow">Inside the research</p><h2 class="h2" id="ask-title">Ask a buyer’s question.<br>Inspect the answer.</h2></div><p>Choose a question to see the brands named and sources cited across five saved answers. This explorer uses the 6 October study, not a live AI search.</p></div>
  {explorer}
  <p class="evidence-caption">First-named counts record order among tracked brands. A mention, a citation and an affirmative recommendation are different signals. <a class="text-link" href="method.html">How to read them</a>.</p>
</div></section>
<section class="band band--mist" aria-labelledby="work-title"><div class="wrap">
  <div class="section-head split-head"><div><p class="eyebrow">From observation to action</p><h2 class="h2" id="work-title">Know what to<br>work on next.</h2></div><p>Start with one business decision. We connect evidence to a clear next step, with the questions, sources and scope agreed before work begins.</p></div>
  <div class="offer-grid">
    <article class="offer-card"><p class="eyebrow">Understand</p><h3>Visibility research</h3><p>Map brand mentions, source citations and question-level gaps across an agreed set of AI answers.</p><a class="arrow-link" href="services.html#visibility">Explore the research {b.icon('arrow')}</a></article>
    <article class="offer-card offer-card--featured"><p class="eyebrow">Improve</p><h3>Visibility &amp;<br>Enquiry Pilot</h3><p>A focused review, up to five prioritised findings, one priority-page draft and a clearer enquiry route.</p><p class="offer-price">₹14,400 <small>plus applicable taxes</small></p><a class="arrow-link" href="plans.html#visibility-pilot">See the complete scope {b.icon('arrow')}</a></article>
    <article class="offer-card"><p class="eyebrow">Learn</p><h3>Compare over time</h3><p>Agree a repeatable measurement scope and review what changes, alongside the work completed.</p><a class="arrow-link" href="plans.html#ongoing-support">Discuss ongoing support {b.icon('arrow')}</a></article>
  </div>
</div></section>
<section class="band band--paper" aria-labelledby="sample-title"><div class="wrap sample-intro">
  <div><p class="eyebrow">A deliverable you can inspect</p><h2 class="h2" id="sample-title">The findings.<br>The sources.<br>The next decision.</h2></div>
  <div><p class="lede">Open the Freshdesk sample to see how a brand’s visibility becomes a focused review: where it appears, where it is absent, and which pages deserve investigation.</p><p>Built from the published helpdesk study. It is a research example, not a client result.</p><div class="ctas"><a class="btn btn--signal" href="sample-snapshot.html">Open the sample {b.icon('arrow')}</a><a class="arrow-link" href="research.html">Browse the research</a></div></div>
</div></section>'''
    b.page(file='index.html', title='Recallant — AI search visibility, grounded in evidence', desc='AI search visibility research and focused website improvements for B2B software brands. Explore the evidence, compare the offers and start a Recallant enquiry.', body=body, tone='night', graph=[b.ORG,b.PERSON])


def about(b):
    body=f'''<section class="band band--paper band--first page-hero"><div class="wrap"><p class="eyebrow">About Recallant</p><h1 class="h-display" id="page-title">A clearer picture.<br>A better next step.</h1><p class="lede">Recallant is the AI search visibility specialist within Signal &amp; Syllable, focused on B2B software brands.</p></div></section>
<section class="band band--paper band--flush"><div class="wrap about-intro"><div class="prose">
<h2>Measure before making a recommendation.</h2><p>Which brands appear when buyers ask about your category? Which sources are cited? Which questions deserve a closer look? Recallant brings those observations together, then helps turn them into a focused improvement brief.</p>
<p>Our public helpdesk study gives you something concrete to inspect: saved answers, source patterns and an interactive question explorer. The results describe that sample and collection date.</p>
<h2>One specialist. A connected studio.</h2><p>Recallant concentrates on visibility research and evidence-led priorities. When a project needs wider positioning, website, editorial or campaign work, <a href="https://signalandsyllable.com/products">Signal &amp; Syllable’s product collection</a> provides the next conversation. Additional work is scoped separately.</p>
<h2>The person behind the work.</h2><p>Prasanth G founded Recallant and brings a background in IT and business analysis. Based in Bengaluru, India.</p><p><a class="text-link" href="{b.LINKEDIN}">Professional profile ↗</a></p>
<h2>What you can expect.</h2><ul><li>A written scope and fee before a paid engagement.</li><li>Sources and measurement definitions alongside findings.</li><li>A clear distinction between observed patterns and proposed actions.</li><li>Your review before content is published.</li></ul>
</div><aside class="profile" aria-label="Founder"><img src="assets/img/prasanth-640.jpg" alt="Prasanth G, founder of Recallant" width="320" height="320"><div><p class="profile__name">Prasanth G</p><p class="profile__role">Founder, Recallant</p></div><dl><div><dt>Based in</dt><dd>Bengaluru, India</dd></div><div><dt>Background</dt><dd>IT and business analysis</dd></div><div><dt>Studio</dt><dd><a href="https://signalandsyllable.com/">Signal &amp; Syllable ↗</a></dd></div></dl></aside></div></section>'''
    b.page(file='about.html',title='About Recallant — research with a practical next step',desc='Meet Recallant, the AI search visibility specialist within Signal & Syllable, founded by Prasanth G.',body=body,current='about.html',graph=[b.ORG,b.PERSON])
