"""Print companions with vector charts, embedded fonts, links and bookmarks."""
from pathlib import Path
from io import BytesIO
import sys, html, hashlib, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import pymupdf
from fieldnotes_content import ISSUES,SOURCES,DATE
from fieldnotes import diagram
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/fieldnotes'; OUT.mkdir(exist_ok=True)
PROOF=ROOT.parent/'recallant-weekly/proofs';PROOF.mkdir(parents=True,exist_ok=True)
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Display','georgia.ttf'),('Italic','georgiai.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
INK='#20302d'; PAPER='#f8f6ef'; W,H=612,792
def para(c,text,x,y,w,size=10.4,font='Body',color=INK,leading=None):
 s=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.52,textColor=HexColor(color))
 p=Paragraph(text,s);pw,ph=p.wrap(w,1000)
 if y-ph<50:raise ValueError(f'Overflow: {text[:70]} y={y} height={ph}')
 p.drawOn(c,x,y-ph);return y-ph
def base(c,i,num,page):
 c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(HexColor(i['accent']));c.rect(36,H-43,540,2,fill=1,stroke=0)
 c.setFont('Bold',9);c.drawString(36,H-30,'RECALLANT / FIELDNOTES')
 c.setFillColor(HexColor(INK));c.setFont('Body',8);c.drawRightString(576,H-30,f'ISSUE {num:02}  /  {DATE.upper()}')
 c.setStrokeColor(HexColor('#c7c7bd'));c.line(36,39,576,39)
 c.setFont('Body',8);c.drawString(36,25,'recallant.com  /  '+i['title']);c.drawRightString(576,25,f'{page:02} / 12')
def drawsvg(c,s,x,y,width):
 d=svg2rlg(BytesIO(s.encode()));scale=width/d.width;d.scale(scale,scale);renderPDF.draw(d,c,x,y)
def cover(c,i,num):
 base(c,i,num,1)
 c.setFillColor(HexColor(i['accent']));c.setFont('Bold',12);c.drawString(36,702,'EVIDENCE FOR EVERYDAY DECISIONS')
 y=para(c,html.escape(i['title']),36,670,530,58,'Display',leading=61)
 y=para(c,html.escape(i['subtitle']),38,y-24,470,23,'Italic')
 # Distinct visual identities: proofreading marks, workbench grid, lens, ledger.
 c.setStrokeColor(HexColor(i['accent']));c.setFillColor(HexColor(i['accent']))
 if i['motif']=='visibility':
  for r in [88,65,42]:c.circle(438,270,r,stroke=1,fill=0)
  c.setLineWidth(8);c.line(500,208,550,158);c.setLineWidth(1)
  c.setFont('Display',32);c.drawString(47,296,'Named.');c.drawString(47,249,'Cited.');c.drawString(47,202,'Chosen?')
 elif i['motif']=='evidence':
  for j,w in enumerate([340,430,270,390]):
   c.setStrokeColor(HexColor('#adb3aa'));c.line(60,340-j*39,60+w,340-j*39)
  c.setStrokeColor(HexColor(i['accent']));c.setLineWidth(3);c.circle(258,262,42);c.line(280,229,373,180);c.setLineWidth(1)
  c.setFont('Italic',18);c.drawString(377,175,'source?')
 elif i['motif']=='tools':
  for j in range(4):
   for k in range(3):
    c.setStrokeColor(HexColor('#a9b9b6'));c.rect(45+j*131,180+k*53,116,42,fill=0,stroke=1)
  c.setFillColor(HexColor(i['accent']));c.rect(176,233,116,42,fill=1,stroke=0)
  c.setFillColor(HexColor('#ffffff'));c.setFont('Bold',13);c.drawString(193,248,'TEST IT')
 else:
  for j in range(6):c.line(45,180+j*30,563,180+j*30)
  for x in [45,220,350,455,563]:c.line(x,180,x,330)
  c.setFont('Display',24);c.drawString(58,346,'What arrived?');c.drawString(355,346,'What next?')
 para(c,html.escape(i['gist']),38,135,505,12)
 c.showPage()
def worksheet(c,i,y):
 headers={
 'evidence':['Claim','Source / date','Evidence status','Action / owner'],
 'tools':['Test case','Hard failure?','Handling time','Decision / limit'],
 'visibility':['Question / surface','Capture / date','Label + passage','Next action'],
 'enquiry':['Enquiry reference','Source / unknown','Status','Next action / owner'],
 }[i['motif']]
 x=36; widths=[135]*4
 c.setFillColor(HexColor(i['accent']));c.rect(x,y-28,540,28,fill=1,stroke=0)
 for n,h in enumerate(headers):para(c,html.escape(h),x+n*135+7,y-6,122,8.3,'Bold','#ffffff')
 c.setStrokeColor(HexColor('#9aa59c'))
 examples={'evidence':['Delivery claim','Service spec / date','Narrower','Rewrite / owner'], 'tools':['Missing finish','Invented finish','Record minutes','Hold / clarify'], 'visibility':['Desk suitability','Saved answer / date','Mention / passage','Check page'], 'enquiry':['Example enquiry','Unknown','Needs detail','Reply / owner']}
 for n,t in enumerate(examples[i['motif']]):para(c,html.escape(t),x+n*135+7,y-35,122,8.3)
 for j in range(4):
  yy=y-28-j*34;c.line(x,yy,x+540,yy)
 for j in range(5):c.line(x+j*135,y-28,x+j*135,y-130)
 c.line(x,y-130,x+540,y-130)
 c.setFont('Body',8);c.setFillColor(HexColor(INK));c.drawString(x,y-146,'First row is illustrative. Print and complete the blank rows; protect customer information.')
def content(c,i,num,p,j):
 base(c,i,num,j+2);c.bookmarkPage(f'section{j}');c.addOutlineEntry(p['title'],f'section{j}',0)
 c.setFillColor(HexColor(i['accent']));c.setFont('Bold',9);c.drawString(36,719,f'{j+1:02}  /  PRACTICAL FIELDNOTE')
 y=para(c,html.escape(p['title']),36,697,530,30,'Display',leading=34)
 y=para(c,html.escape(p['deck']),36,y-12,530,13,'Italic')
 is_sheet=p['visual']=='worksheet'
 if is_sheet:
  worksheet(c,i,y-20); texttop=y-183
 else:
  drawsvg(c,diagram(p['visual'],i['accent']),36,y-200,540)
  texttop=y-224
 # Balanced columns: one introductory paragraph left, remaining text right.
 left=p['paragraphs'][0];right='<br/><br/>'.join(html.escape(t) for t in p['paragraphs'][1:])
 yl=para(c,html.escape(left),36,texttop,252,10.6)
 yr=para(c,right,324,texttop,252,10.6)
 bottom=min(yl,yr)-22
 c.setStrokeColor(HexColor(i['accent']));c.line(36,bottom,576,bottom)
 para(c,html.escape(p['takeaway']),36,bottom-10,520,12,'Bold',i['accent'])
 c.setFillColor(HexColor('#59635d'));c.setFont('Body',7.5)
 c.drawString(36,57,'Fictional workshop. Documented data and source scope are identified in the text.')
 for k,r in enumerate(p['refs']):
  c.linkURL(SOURCES[r][1],(36,42+k*8,570,50+k*8),relative=0,thickness=0)
 c.showPage()
def sources(c,i,num):
 base(c,i,num,12);para(c,'The evidence behind<br/>this edition.',36,705,520,38,'Display',leading=43)
 y=580
 refs=sorted({r for p in i['pages'] for r in p['refs']})
 for r in refs:
  title,url=SOURCES[r];y=para(c,html.escape(title),36,y,530,13,'Bold')-8
  y=para(c,f'<link href="{html.escape(url,quote=True)}" color="{i["accent"]}">{html.escape(url)}</link>',36,y,530,9)-20
 if not refs:y=para(c,'Original practical guidance and invented teaching examples; no fresh empirical study is claimed.',36,y,530,12)-20
 y=para(c,'Source check: '+DATE+'. References support the specific factual passages marked in the online edition. They do not endorse Recallant or establish customer outcomes.',36,y,530,10.5)-26
 y=para(c,'How this edition was made',36,y,530,22,'Display')-12
 y=para(c,'Original editorial writing and diagrams, with AI-assisted drafting and independent critique. Arithmetic, claims and final layouts were checked before release. This is a practical guide, not a controlled evaluation, professional advice or a promise of commercial results. The accompanying HTML provides structured headings, readable text and source links; this visual PDF is not claimed to be PDF/UA certified.',36,y,530,11)-24
 y=para(c,'Read the series / report a correction',36,y,530,20,'Display')-12
 para(c,'<link href="https://recallant.com/fieldnotes.html">recallant.com/fieldnotes.html</link><br/><link href="mailto:hello@recallant.com">hello@recallant.com</link>',36,y,530,11)
 c.showPage()
manifest=[]
for num,i in enumerate(ISSUES,1):
 target=OUT/(i['slug']+'.pdf');c=canvas.Canvas(str(target),pagesize=(W,H),pageCompression=1)
 c.setTitle(i['title']+' | Recallant Fieldnotes');c.setAuthor('Recallant');c.setSubject(i['subtitle'])
 cover(c,i,num)
 for j,p in enumerate(i['pages']):content(c,i,num,p,j)
 sources(c,i,num);c.save()
 doc=pymupdf.open(target);assert len(doc)==12
 for n,page in enumerate(doc):
  assert page.get_text().strip(),(target,n)
  page.get_pixmap(matrix=pymupdf.Matrix(1.1,1.1)).save(PROOF/f'{i["slug"]}-{n+1:02}.png')
 manifest.append(dict(file=str(target),pages=len(doc),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(PROOF.parent/'pdf-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Built and rendered four 12-page PDFs.')
