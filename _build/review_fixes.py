"""Bounded review improvements; preserve evidence and the current pilot scope."""
import hashlib
import json
import re
from bs4 import BeautifulSoup

def apply(b):
 for name,html in list(b.PAGES.items()):
  doc=BeautifulSoup(html,'html.parser')
  for table in doc.select('.table-wrap'):
   table['tabindex']='0';table['role']='region';table['aria-label']='Research data table'
  for chart in doc.select('.rangechart'):
   chart.attrs.pop('aria-hidden',None);chart['tabindex']='0';chart['role']='region';chart['aria-label']='Share-of-voice chart; full values are in the following table'
  logos=doc.select('svg.rc-wordmark')
  if logos:
   original=BeautifulSoup(str(logos[0]),'html.parser').svg
   for el in original.select('[d]'):
    el['d']=re.sub(r'-?\d+\.\d+(?:[eE][-+]?\d+)?',lambda m:format(round(float(m[0]),2),'.2f').rstrip('0').rstrip('.'),el['d'])
   symbol=doc.new_tag('symbol',id='recallant-logo');symbol['viewBox']=original.get('viewbox',original.get('viewBox'))
   for child in list(original.contents):symbol.append(child.extract())
   sprite=doc.new_tag('svg',attrs={'xmlns':'http://www.w3.org/2000/svg','width':'0','height':'0','aria-hidden':'true','focusable':'false','style':'position:absolute;overflow:hidden'});sprite.append(symbol);doc.body.insert(0,sprite)
   for logo in logos:
    logo.clear();logo['focusable']='false';logo['aria-hidden']='true';logo.append(doc.new_tag('use',href='#recallant-logo'))
  if name=='index.html':
   doc.select_one('.rc-cover-copy .eyebrow').string='AI search visibility research for B2B software'
   doc.select_one('.rc-deck').string='We show where your brand appears in AI answers, which sources get cited, and what to fix first, with the evidence attached.'
  if name=='research.html':
   # No promise of an unpublished deliverable without a verified shareable asset.
   for h in doc.select('h3'):
    if 'ITSM and MSP' in h.get_text():
     article=h.find_parent('article')
     if article:article.decompose()
  for a in doc.select('a[href]'):
   if a['href'].split('?')[0] in ['https://signalandsyllable.com/'+s for s in ['pressroom','pagecraft','signal-map','services','products']]:a['href']='https://signalandsyllable.com/what-we-do'
   if a['href']=='https://signalandsyllable.com/packages':a['href']='https://signalandsyllable.com/pricing'
  for node in list(doc.find_all(string=True)):
   if node.parent.name in ('script','style'):continue
   text=str(node).replace('Explore the Visibility Pilot','Explore the Visibility & Enquiry Pilot')
   if text!=str(node):node.replace_with(text)
  if name=='plans.html':
   doc.title.string='Visibility & Enquiry Pilot, audit and support | Recallant'
   for el in doc.select('meta[property="og:title"],meta[name="twitter:title"]'):el['content']=doc.title.string
   graph=[]
   for card in doc.select('.offer-card'):
    price_text=card.select_one('.lede')
    match=re.search(r'₹([\d,]+)',price_text.get_text() if price_text else '')
    if not match:continue
    label=card.h2.get_text();fixed=card.get('id')=='visibility-pilot';monthly='/ month' in price_text.get_text()
    price={'@type':'UnitPriceSpecification' if monthly else 'PriceSpecification','priceCurrency':'INR','valueAddedTaxIncluded':False,'price' if fixed else 'minPrice':int(match[1].replace(',',''))}
    if monthly:price['billingDuration']='P1M'
    desc=price_text.find_next_sibling('p')
    graph.append({'@type':'Service','name':label,'description':desc.get_text() if desc else label,'provider':{'@id':b.SITE+'/#organization'},'offers':{'@type':'Offer','url':b.SITE+'/plans.html#'+card['id'],'priceSpecification':price}})
   el=doc.new_tag('script',type='application/ld+json');el.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':'));doc.head.append(el)
  if name not in ('404.html','index.html') and not any('BreadcrumbList' in s.get_text() for s in doc.select('script[type="application/ld+json"]')):
   schema=doc.new_tag('script',type='application/ld+json');schema.string=json.dumps({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':b.SITE+'/'},{'@type':'ListItem','position':2,'name':doc.h1.get_text(' ',strip=True),'item':b.SITE+'/'+name}]},ensure_ascii=False,separators=(',',':'));doc.head.append(schema)
  if name=='404.html':
   for el in doc.select('script[type="application/ld+json"]'):el.decompose()
  if name in ('index.html','plans.html','research.html'):
   doc.head.append(doc.new_tag('link',rel='preload',href='assets/fonts/newsreader-latin-v1.woff2',attrs={'as':'font','type':'font/woff2','crossorigin':''}))
  for el in doc.select('script[src],link[rel=stylesheet]'):
   key='src' if el.name=='script' else 'href';path=el[key].split('?')[0];f=b.ROOT/path
   if f.is_file():el[key]=path+'?v='+hashlib.sha256(f.read_bytes()).hexdigest()[:10]
  # Share artwork is produced from the matching local source in this release.
  if name!='helpdesk-study.html':
   for el in doc.select('meta[property="og:image:alt"],meta[name="twitter:image:alt"]'):el['content']='Recallant: the answer is not the whole story. AI search visibility research for B2B software.'
  b.PAGES[name]=str(doc)
