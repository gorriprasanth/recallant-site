"""Correct the interpretation of retained figures without changing the dataset."""
import re

NOTE = '''<aside class="measurement-note"><strong>How to read these figures</strong><p>This is evidence collected on 6 October 2026. “First named” records naming order among tracked brands; it does not establish an affirmative recommendation. Headline rates use the study’s weighting. Own-site citation rates apply to eligible answers with inline citations, while source counts use the denominator printed beside them. <a href="method.html">Measurement definitions →</a></p></aside>'''


def correct_page(doc, file):
    # The ten-answer manual ChatGPT spot check is separate from automated ordering.
    manual = None
    if file == 'helpdesk-study.html':
        match = re.search(r'<h2 id="spot-check-chatgpt-app">.*?(?=<h2 id="how-it-was-measured-and-its-limits">)', doc, re.S)
        if match:
            manual = match.group(0)
            doc = doc[:match.start()] + 'RECALLANT_MANUAL_SPOTCHECK' + doc[match.end():]
    for old,new in [
        ('Recommended first', 'First named'), ('recommended first', 'named first'),
        ('recommend it first', 'name it first'), ('Top pick', 'First named'),
        ('top pick', 'first named'), ('first recommendation', 'first-named brand'),
        ('Chosen more often than cited', 'Named first more often than cited'),
        ('Cited more often than chosen', 'Cited more often than named first'),
        ('Chosen more than cited', 'Named first more than cited'),
        ('Cited more than chosen', 'Cited more than named first'),
    ]:
        doc = doc.replace(old,new)
    doc = re.sub(r'share of answers that recommend the brand\s+first', 'weighted rate at which the brand is named first (an order proxy)', doc)
    doc = re.sub(r'share of answers that link to the\s+brand\x27s own site', 'weighted rate of eligible inline-cited answers that cite the brand\x27s own site', doc)
    doc = re.sub(r'Rivals win these today because their content matches the question\.', 'Review whether the relevant product pages answer these questions. Naming order alone does not establish the cause.', doc)
    doc = re.sub(r'<span class="doc__marker">\d+</span>', '', doc)
    if manual:
        doc = doc.replace('RECALLANT_MANUAL_SPOTCHECK',manual)
    if file == 'helpdesk-study.html':
        doc = doc.replace('<article class="prose" data-article>', '<article class="prose" data-article>'+NOTE)
    if file == 'sample-snapshot.html':
        doc = doc.replace('<div class="kpis">', NOTE+'<div class="kpis">')
        doc = doc.replace('of answers name Freshdesk', 'weighted mention rate')
        doc = doc.replace('cite Freshworks’ own site (Help Scout: 21%)', 'own-site citation rate (Help Scout: 21%)')
    return doc
