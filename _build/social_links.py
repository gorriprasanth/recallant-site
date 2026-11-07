"""Plain owned-profile links; no embeds, trackers or platform scripts."""
from bs4 import BeautifulSoup
from pathlib import Path
import json

def enrich(html, links):
    doc = BeautifulSoup(html, 'html.parser')
    footer = doc.find('footer')
    if not footer:
        return html
    for old in footer.select('.owned-social-links'):
        old.decompose()
    section = doc.new_tag('nav', attrs={'class':'owned-social-links', 'aria-label':'Follow us'})
    section['style'] = 'display:block;max-width:1280px;margin:24px auto 0;padding:24px clamp(20px,4vw,64px);border-top:1px solid currentColor'
    heading = doc.new_tag('p'); heading.string = 'Follow us'; heading['style'] = 'margin:0 0 12px;font-weight:600'
    section.append(heading)
    listing = doc.new_tag('ul'); listing['style'] = 'display:flex;flex-wrap:wrap;gap:4px 24px;list-style:none;margin:0;padding:0'
    for item in links:
        li = doc.new_tag('li'); a = doc.new_tag('a', href=item['url'])
        a.string = item['label']; a['style'] = 'display:inline-flex;align-items:center;min-height:44px;text-decoration:underline;text-underline-offset:4px'
        li.append(a); listing.append(li)
    section.append(listing); footer.append(section)
    company = next(x['url'] for x in links if x['label']=='LinkedIn')
    for a in footer.select('a[href]'):
        if 'linkedin.com/in/' in a['href']:
            a['href'] = company
    for script in doc.select('script[type="application/ld+json"]'):
        try: data = json.loads(script.string or '')
        except (ValueError, TypeError): continue
        def update(obj):
            if isinstance(obj, dict):
                if obj.get('@type') == 'Organization': obj['sameAs'] = [x['url'] for x in links]
                for val in obj.values(): update(val)
            elif isinstance(obj,list):
                for val in obj: update(val)
        update(data); script.string = json.dumps(data,ensure_ascii=False,separators=(',',':'))
    return str(doc)

def load():
    return json.loads(Path(__file__).with_name('social-links.json').read_text(encoding='utf-8'))
