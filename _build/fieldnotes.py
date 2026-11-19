"""Build accessible editorial pages; PDF companion is generated separately."""
from pathlib import Path
import html, json, textwrap, hashlib
from fieldnotes_content import ISSUES, SOURCES, DATE

def e(t): return html.escape(str(t), quote=True)
def diagram(kind, accent):
    # Each diagram has a visible descriptive caption in HTML and PDF.
    sets = {
      'triage': [('KEEP','Supported'),('REWRITE','Narrower evidence'),('HOLD','Unavailable evidence'),('CORRECT / REMOVE','Contradicted')],
      'blindreview': [('HIDE','Remove tool names'),('SCORE','Apply the same rules'),('REVEAL','Compare the source tools'),('RESOLVE','Record disagreements')],
      'trialdecision': [('RETEST','Use held-out cases'),('RESTRICT','Keep it off this job'),('SIMPLIFY','Use a non-AI fix')],
      'shortlist': [('START','Tools already available'),('FILTER','Requirements and data rules'),('CAP','Two or three candidates')],
      'visibilityoverview': [('ASK','A useful buyer question'),('READ','The complete answer'),('CHECK','The source and context'),('ACT','One evidence-led decision')],
      'enquiryoverview': [('DEFINE','A distinct enquiry'),('LOG','Keep its record together'),('LABEL','Include unknown sources'),('FOLLOW UP','Assign the next action')],
      'month': [('WEEK 1','Define and check delivery'),('WEEK 2','One useful page fix'),('WEEK 3','Read the new enquiries'),('WEEK 4','Summarise and decide')],
      'visibilityaction': [('FIND','One information gap'),('FIX','The source you control'),('RECORD','The change and its date')],
      'claims': [('Delivery','Dispatch is not arrival'),('Assembly','Confirm the actual service'),('Warranty','Check duration and exclusions')],
      'source': [('WHO','Responsible source'),('WHAT','Exact supporting passage'),('WHEN','Date and applicable version')],
      'ledger': [('Draft','Arrives in three days'),('Record','Dispatch within three working days'),('Decision','Correct the promise')],
      'timeline': [('SOURCE CHANGES','Owner confirms the new fact'),('COPY CHANGES','Revise every active version'),('REVIEW TRIGGER','Set the next relevant check')],
      'beforeafter': [('BEFORE','Free assembly. Three-day delivery.'),('CHECK','Which record supports each promise?'),('AFTER','Confirm timing and assembly for the address.')],
      'review': [('Reader A','Checks the claim'),('Reader B','Challenges the evidence'),('Resolution','Return to the source')],
      'worksheet': [('RECORD','Question / evidence / date'),('DECIDE','Keep / revise / hold'),('ASSIGN','Next action / owner / review trigger')],
      'stop': [('Optional claim','Remove if unsupported'),('Essential fact','Ask the responsible person'),('High consequence','Obtain qualified review')],
      'action': [('Choose one','A useful real-world task'),('Make it inspectable','Retain the evidence'),('Decide the next move','Name the owner')],
      'task': [('INPUT','Approved order notes'),('OUTPUT','Checkable draft production brief'),('BOUNDARY','No order placed automatically')],
      'gates': [('REQUIREMENTS','Define a usable result'),('HARD FAILURES','Name the errors that stop release'),('PREFERENCES','Then compare ease of use')],
      'qualification': [('NEED','A service we can deliver'),('LOCATION','Within our service area'),('DETAIL','Enough to discuss the next step')],
      'testpack': [('NORMAL','Complete and consistent'),('MISSING','Ask for the absent fact'),('CONFLICT','Flag the contradiction'),('EMPTY','Invent nothing')],
      'structure': [('FORMAT','Does the field exist?'),('MEANING','Does it match the source?'),('ACTION','Is this use authorised?')],
      'tradeoff': [('LOCAL','Hardware, maintenance, full data path'),('HOSTED','Service limits, terms, recurring cost'),('BOTH','Test the actual operational constraint')],
      'calendar': [('DAYS 1–2','Rules and test pack'),('DAYS 3–6','Runs and full output review'),('DAYS 7–10','Failures and held-out repeats'),('DAYS 11–14','Supervised work and decision')],
      'ladder': [('MENTION','The name appears'),('CITATION','A source is referenced'),('RECOMMENDATION','The wording expresses fit'),('FIRST-NAMED','Position in the text'),('ENQUIRY','A separate business event')],
      'answer': [('QUESTION','What should I check before ordering?'),('ANSWER','Workshop A offers a compact model.'),('READING','Named here; no preference established')],
      'sampling': [('FIX','Questions and conditions'),('CAPTURE','Every answer and failure'),('CLASSIFY','Evidence-backed labels'),('COMPARE','Equivalent populations only')],
      'study': [('44 questions','Five runs each: 220 answers'),('40 questions','Non-branded explorer subset'),('6 Oct 2026','Historical collection date')],
      'report': [('IMPRESSION','A reported visibility observation'),('CLICK','A different interaction'),('ENQUIRY','A business record, not an impression')],
      'page': [('FIT','Dimensions and materials'),('TERMS','Delivery and assembly'),('PROOF','Relevant product photographs'),('NEXT STEP','How to confirm an order')],
      'journey': [('SUBMITTED','Browser confirmation'),('RECEIVED','Inbox delivery'),('ANSWERED','Useful response'),('OUTCOME','Booked / declined / unresolved')],
      'records': [('SEARCH','Impressions and clicks'),('WEBSITE','Observed visits and actions'),('BUSINESS','Distinct enquiries and outcomes')],
      'experiment': [('QUESTION','Do buyers understand assembly?'),('CHANGE','Explain it beside the specification'),('OBSERVE','Read the next enquiries')],
      'smallnumbers': [('BEFORE','3 of 8 ask about assembly'),('AFTER','1 of 6 ask about assembly'),('CONCLUSION','Small samples; no causal proof')],
    }
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="320" viewBox="0 0 1000 320" role="img"><title>{e(kind.replace("_"," "))} explanation</title><rect width="1000" height="320" fill="#f1eee5"/>']
    def text(x,y,s,size=20,fill='#20302d',family='Arial',weight='normal'):
      parts.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}">{e(s)}</text>')
    if kind in ('timebars','channels','qualified','denominator'):
      configs={
       'timebars': [('Manual',12,'12 min'),('Assisted total',9,'2 + 1 + 6 = 9 min')],
       'channels': [('Referral',6,'6'),('Search',5,'5'),('Social',2,'2'),('AI chat',1,'1'),('Unknown',6,'6')],
       'qualified': [('Source A',4,'4 qualified / 5 enquiries = 80%'),('Source B',12,'12 qualified / 30 enquiries = 40%')],
       'denominator': [('Attempted',10,'10'),('Usable',8,'8'),('Mentions',3,'3 of 8 usable = 37.5%'),('Failed',2,'2')],
      }
      rows=configs[kind]; maxv=max(x[1] for x in rows); dy=210/len(rows)
      text(28,34,'ILLUSTRATIVE NUMBERS - NOT CLIENT RESULTS',14,accent,weight='bold')
      for n,(label,value,note) in enumerate(rows):
       yy=76+n*dy;text(28,yy+15,label,20)
       parts.append(f'<rect x="200" y="{yy}" width="{value/maxv*350}" height="24" fill="{accent if label!="Unknown" else "#5c6461"}"/>')
       text(575,yy+19,note,18)
      text(28,300,'Qualified enquiry count; shared zero and scale.' if kind=='qualified' else 'Bars use a shared zero and scale within this figure.',15)
    elif kind=='ledger':
      text(28,35,'CLAIM CHECK / INVENTED WORKSHOP EXAMPLE',15,accent,weight='bold')
      for n,(claim,evidence,status,action) in enumerate([('Arrives in 3 days','Dispatch within 3 working days','Narrower','REWRITE'),('Assembly included','No verified service record','Unavailable','HOLD'),('Lifetime warranty','Defined duration and exclusions','Contradicted','CORRECT')]):
       yy=70+n*75;parts.append(f'<path d="M28 {yy+48}H970" stroke="#b5beb6"/>')
       text(28,yy,claim,19);text(290,yy,evidence,16);text(665,yy,status,17);text(840,yy,action,17,accent,weight='bold')
      text(28,302,'Evidence status and publication action are recorded separately.',15)
    elif kind in ('testpack','calendar','month','blindreview','visibilityoverview','enquiryoverview'):
      rows=sets[kind]
      for n,(label,desc) in enumerate(rows):
       x=30+(n%2)*485;y=25+(n//2)*145
       parts.append(f'<rect x="{x}" y="{y}" width="455" height="125" fill="#ffffff"/><rect x="{x}" y="{y}" width="7" height="125" fill="{accent}"/>')
       text(x+22,y+35,label,18,accent,weight='bold')
       for j,line in enumerate(textwrap.wrap(desc,33)):text(x+22,y+72+j*26,line,23)
    elif kind in ('records','report','ladder'):
      rows=sets[kind]
      for n,(label,desc) in enumerate(rows):
       yy=50+n*(220/len(rows));text(30,yy,label,20,accent,weight='bold');text(290,yy,desc,24)
       parts.append(f'<path d="M30 {yy+20}H950" stroke="#bcc3ba"/>')
      text(30,302,'Separate observations. No automatic progression or attribution is implied.',15)
    elif kind in ('beforeafter','answer','claims','source'):
      rows=sets[kind];parts.append('<rect x="25" y="25" width="590" height="260" fill="#fffdf7"/>')
      text(50,65,rows[0][0],17,accent,weight='bold')
      for j,line in enumerate(textwrap.wrap(rows[0][1],30)):text(50,110+j*33,line,28)
      parts.append(f'<path d="M60 225H555" stroke="{accent}" stroke-width="3"/>')
      for n,(label,desc) in enumerate(rows[1:]):
       yy=70+n*125;text(660,yy,label,17,accent,weight='bold')
       for j,line in enumerate(textwrap.wrap(desc,25)):text(660,yy+32+j*26,line,20)
    else:
      rows=sets.get(kind,sets['action']); w=940/len(rows)
      parts.append(f'<path d="M30 74H970" stroke="{accent}" stroke-width="2"/>')
      for n,(label,desc) in enumerate(rows):
       x=30+n*w
       parts.append(f'<circle cx="{x+14}" cy="74" r="14" fill="{accent}"/>')
       text(x,120,label,20,accent,weight='bold')
       for j,line in enumerate(textwrap.wrap(desc, max(15,int(w/14)))):text(x,165+j*29,line,22)
    parts.append('</svg>')
    result=''.join(parts)
    if kind not in ('timebars','channels','qualified','denominator','ledger','testpack','calendar','month','blindreview','visibilityoverview','enquiryoverview','records','report','ladder','beforeafter','answer','claims','source'):
      result=result.replace('height="320"','height="260"').replace('viewBox="0 0 1000 320"','viewBox="0 0 1000 260"')
    return result

def render(b):
  root=b.ROOT; art=root/'assets/fieldnotes';art.mkdir(exist_ok=True)
  index=[]
  for num,i in enumerate(ISSUES,1):
    slug=i['slug']; refs=set(); chunks=[]
    contents=''.join(f'<li><a href="#section-{j}">{e(p["title"])}</a></li>' for j,p in enumerate(i['pages'],1))
    for j,p in enumerate(i['pages'],1):
      refs.update(p['refs']); v=p['visual']; fn=f'{slug}-{j:02}.svg';(art/fn).write_text(diagram(v,i['accent']),encoding='utf-8')
      paragraphs=''.join(f'<p>{e(t)}</p>' for t in p['paragraphs'])
      if v=='worksheet':
       heads={'evidence':['Claim','Source and date','Evidence status','Action and owner'],'tools':['Test case','Hard failure?','Handling time','Decision and limit'],'visibility':['Question and surface','Capture and date','Label and passage','Next action'],'enquiry':['Enquiry reference','Source or unknown','Status','Next action and owner']}[i['motif']]
       paragraphs+='<table class="fn-sheet"><caption>Reusable worksheet: copy these fields into your working record.</caption><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>Record here</td>' for h in heads)+'</tr>' for _ in range(2))+'</tbody></table>'
      source=' '.join(f'<a href="{e(SOURCES[r][1])}">{e(SOURCES[r][0])}</a>' for r in p['refs'])
      chunks.append(f'<section class="fn-section" id="section-{j}"><p class="fn-label">FIELDNOTE {j:02}</p><h2>{e(p["title"])}</h2><p class="fn-deck">{e(p["deck"])}</p><figure><img src="assets/fieldnotes/{fn}" alt="{e(p["takeaway"])}" width="1000" height="320" loading="lazy"><figcaption>{e(p["takeaway"])} Workshop examples and hypothetical numbers are illustrative. Dated study figures are identified separately.</figcaption></figure><div class="fn-prose">{paragraphs}</div><p class="fn-source">{source}</p></section>')
    sources=''.join(f'<li><a href="{e(SOURCES[r][1])}">{e(SOURCES[r][0])}</a> - checked {DATE}.</li>' for r in sorted(refs))
    if not sources:sources='<li>Original Recallant editorial workflow and invented examples. No fresh empirical study is claimed.</li>'
    body=f'<article class="fn-article" style="--fn-accent:{i["accent"]}"><header class="fn-cover"><p class="fn-label">RECALLANT FIELDNOTES / ISSUE {num:02}</p><h1>{e(i["title"])}</h1><p class="fn-subtitle">{e(i["subtitle"])}</p><p class="fn-date">Published {DATE} · Weekly reading series · Editorial guide</p><p class="fn-gist">{e(i["gist"])}</p><a class="btn" href="assets/fieldnotes/{slug}.pdf" download>Download the 12-page edition (PDF)</a><p class="fn-small">This HTML edition is the accessible reading alternative to the visual PDF.</p></header><nav class="fn-contents" aria-label="In this issue"><h2>In this issue</h2><ol>{contents}</ol></nav>{"".join(chunks)}<section class="fn-section"><h2>Sources and editorial method</h2><p>These reports combine original practical guidance with the specific primary references linked beside factual claims. They are not fresh tool benchmarks, customer case studies or guarantees. Examples are invented; historical research stays dated. AI-assisted drafting and critique supported production. Source checks, corrections and final artifact inspection were completed before publication.</p><ul>{sources}</ul><p>Correction or question? <a href="mailto:hello@recallant.com">hello@recallant.com</a></p><a href="fieldnotes.html">Explore all four issues</a></section></article>'
    b.page(file=f'fieldnotes-{slug}.html',title=f'{i["title"]} | Recallant Fieldnotes',desc=i['gist'],body=body,current='research.html')
    index.append(f'<a class="fn-index-row" href="fieldnotes-{slug}.html" style="--fn-accent:{i["accent"]}"><span class="fn-issue">ISSUE {num:02}</span><h2>{e(i["title"])}</h2><p>{e(i["subtitle"])}</p><span>Read online or download PDF →</span></a>')
  b.page(file='fieldnotes.html',title='Fieldnotes | Recallant',desc='Four practical editorial reports on AI evidence, tool selection, search visibility and enquiries.',body='<section class="fn-article"><header class="fn-cover"><p class="fn-label">THE RECALLANT READING ROOM</p><h1>Fieldnotes.</h1><p class="fn-subtitle">A clearer view of AI, search and the decisions behind the numbers.</p><p>Four weekly reading editions, available together. Each includes a visual explanation, a worked example, a practical check sheet and clear limits. Published 19 November 2026; future distribution does not imply a future source check.</p></header>'+''.join(index)+'</section>',current='research.html')
  for name,doc in list(b.PAGES.items()):
    if name.startswith('fieldnotes'):
      version=hashlib.sha256((root/'assets/css/fieldnotes.css').read_text(encoding='utf-8').encode('utf-8')).hexdigest()[:12]
      b.PAGES[name]=doc.replace('</head>',f'<link rel="stylesheet" href="assets/css/fieldnotes.css?v={version}"></head>')
  b.PAGES['research.html']=b.PAGES['research.html'].replace('</main>','<section class="wrap fn-research-link"><h2>Read the Fieldnotes series</h2><p>Four practical reports: checking AI answers, choosing tools, interpreting visibility and following enquiries.</p><a class="btn" href="fieldnotes.html">Open the reading room</a></section></main>')

if __name__=='__main__':
 print(json.dumps(ISSUES,ensure_ascii=False))
