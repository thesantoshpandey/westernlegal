#!/usr/bin/env python3
"""Western Legal site audit. Run before every deploy: python3 audit.py"""
import re, glob, json, os, sys, html as H
from collections import Counter, defaultdict

FAIL=[]; WARN=[]
def fail(cat,msg): FAIL.append((cat,msg))
def warn(cat,msg): WARN.append((cat,msg))

PAGES=sorted(glob.glob('*.html'))+sorted(glob.glob('insights/*.html'))
LEGAL={'privacy.html','terms.html','complaints.html'}
NOINDEX={'portal.html','thank-you.html'}
def txt(f): return open(f,encoding='utf-8',errors='ignore').read()

# ---------- structure ----------
for f in PAGES:
    s=txt(f)
    d=len(re.findall(r'<div\b',s))-s.count('</div>')
    if d: fail('structure',f'{f}: div imbalance {d}')
    if len(re.findall(r'<h1',s))!=1 and f not in NOINDEX:
        fail('structure',f'{f}: {len(re.findall(r"<h1",s))} h1 tags')
    if 'lang="en-GB"' not in s: fail('structure',f'{f}: missing lang')
    if 'name="viewport"' not in s: fail('structure',f'{f}: missing viewport')

# ---------- meta ----------
titles=Counter(); descs=Counter()
for f in PAGES:
    s=txt(f)
    t=re.search(r'<title>(.*?)</title>',s,re.S)
    d=re.search(r'<meta name="description" content="(.*?)"',s,re.S)
    if not t: fail('meta',f'{f}: no title'); continue
    T=H.unescape(t.group(1)); titles[T]+=1
    if len(T)>62: warn('meta',f'{f}: title {len(T)} chars')
    if not d: fail('meta',f'{f}: no description')
    else:
        D=H.unescape(d.group(1)); descs[D]+=1
        if len(D)>160: warn('meta',f'{f}: description {len(D)} chars')
    for k,p in [('canonical','rel="canonical"'),('og:title','property="og:title"'),
                ('og:image','property="og:image"'),('og:url','property="og:url"'),
                ('twitter','name="twitter:card"'),('robots','name="robots"')]:
        if p not in s: fail('meta',f'{f}: missing {k}')
    if f in NOINDEX and 'noindex' not in s: fail('meta',f'{f}: should be noindex')
for T,c in titles.items():
    if c>1: fail('meta',f'duplicate title x{c}: {T[:60]}')
for D,c in descs.items():
    if c>1 and D: fail('meta',f'duplicate description x{c}: {D[:60]}')

# ---------- schema ----------
for f in PAGES:
    s=txt(f)
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: json.loads(b)
        except Exception as e: fail('schema',f'{f}: invalid JSON-LD {e}')
    if f not in LEGAL|NOINDEX and 'BreadcrumbList' not in s and f!='index.html':
        warn('schema',f'{f}: no BreadcrumbList')

# ---------- links and images ----------
have={f[:-5] for f in glob.glob('*.html')} | {'insights'} | {'insights/'+f.split('/')[-1][:-5] for f in glob.glob('insights/*.html')} | {''}
red={r['source'].lstrip('/') for r in json.load(open('vercel.json')).get('redirects',[])}
imgs=set(os.listdir('img'))
for f in PAGES:
    s=txt(f)
    for m in re.finditer(r'href="/([a-z0-9\-/]*)"',s):
        u=m.group(1).rstrip('/')
        if u and u not in have and u not in red and not u.startswith(('img','css','js','api')):
            fail('links',f'{f}: broken link /{u}')
    for m in re.finditer(r'href="(/[a-z0-9\-/]*\.html)"',s):
        fail('links',f'{f}: .html link {m.group(1)}')
    for m in re.finditer(r'/img/([A-Za-z0-9._-]+)',s):
        if m.group(1) not in imgs: fail('images',f'{f}: missing /img/{m.group(1)}')
    for m in re.finditer(r'<img (?![^>]*alt=)[^>]*>',s):
        fail('a11y',f'{f}: img without alt')

# ---------- prices ----------
GLOBAL={'£650','£995','£750','£150','£555','£245','£1,200','£299','£399','£345','£425','£550','£450','£145','£649'}
KEEP={'£20,000','£2,000','£700','£5,000','£350','£500','£0','£2,700','£1,950','£2,000,000','£250,000'}
for f in [x for x in glob.glob('*.html') if x not in LEGAL]:
    s=txt(f)
    sched=set(re.findall(r'£[\d,]+',' '.join(re.findall(r'<td class="fee"><b>(.*?)</b></td>',s))))
    if not sched: continue
    body=re.sub(r'<table.*?</table>','',s,flags=re.S)
    for a in set(re.findall(r'£[\d,]+(?=[^0-9])',body)):
        if a.rstrip(',') not in sched|GLOBAL|KEEP:
            fail('prices',f'{f}: {a} not in its own schedule')
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: dd=json.loads(b)
        except: continue
        if dd.get('@type')=='Service':
            nums=[re.sub(r'[£,]','',x) for x in re.findall(r'£([\d,]+)',' '.join(re.findall(r'<td class="fee"><b>(.*?)</b></td>',s)))]
            for o in dd.get('offers',[]):
                p=o.get('priceSpecification',{}).get('price')
                cur=o.get('priceSpecification',{}).get('priceCurrency')
                if cur=='GBP' and p and p not in nums:
                    fail('prices',f'{f}: schema offer {p} not in schedule')

# ---------- hero chip prices ----------
# A hero chip pairs a price with a label. Both must agree with the schedule row
# whose item text the label points at. Comparing figures alone misses the case
# where the figure is real but attached to the wrong service.
STOP={'from','the','and','with','for','a','an','of','to','in','pack','fixed','per','your','our'}
def toks(x): return {w for w in re.findall(r'[a-z]+',x.lower()) if w not in STOP and len(w)>3}
for f in [x for x in glob.glob('*.html') if x not in LEGAL]:
    s=txt(f)
    rows=re.findall(r'<tr><td><b>(.*?)</b></td>.*?<td class="fee"><b>(.*?)</b></td></tr>', s, re.S)
    if not rows: continue
    sched=[(H.unescape(re.sub(r'<[^>]+>','',r[0])), set(re.findall(r'£[\d,]+',r[1]))) for r in rows]
    hero=re.search(r'<section class="hero".*?</section>',s,re.S)
    if not hero: continue
    for chip in re.findall(r'<div><b>(£[\d,]+)</b>([^<]{4,90})</div>', hero.group(0)):
        price,label=chip[0],H.unescape(chip[1])
        lt=toks(label)
        if not lt: continue
        best=None; score=0
        for item,prices in sched:
            ov=len(lt & toks(item))
            if ov>score: score, best = ov, (item,prices)
        if best and score>=1 and price not in best[1]:
            fail('prices', f'{f}: hero chip "{label.strip()[:38]}" says {price} but the schedule row "{best[0][:38]}" says {"/".join(sorted(best[1]))}')

# ---------- compliance ----------
for f in PAGES:
    s=txt(f)
    bare=len(re.findall(r'SRA[- ]regulated',re.sub(r'SRA-regulated solicitor','',s)))
    if bare: fail('compliance',f'{f}: {bare} bare "SRA-regulated"')
    if re.search(r'Regulated by the Solicitors Regulation Authority(?!;)',s): fail('compliance',f'{f}: firm-level SRA claim')
    if f.split('/')[-1] not in LEGAL and re.search(r'\b[Ii]ndia\b|\bDelhi\b|\bNRI\b',s):
        fail('compliance',f'{f}: India reference')
    if 'id="contact"' in s and 'professional indemnity insurance of' not in s and f not in NOINDEX:
        warn('compliance',f'{f}: no PII disclosure line')
    for legacy,label in [('d4af37','retired gold hex'),('formsubmit.co','legacy form action'),
                         ('917042333175','retired India WhatsApp'),('447915318920','old WhatsApp'),
                         ('logo-email.png','deleted logo ref'),('nav-portal','legacy nav')]:
        if legacy in s: fail('legacy',f'{f}: {label} ({legacy})')

# ---------- forms and tracking ----------
for f in glob.glob('*.html'):
    s=txt(f)
    if '<form' not in s: continue
    if 'name="website"' not in s: fail('forms',f'{f}: no honeypot')
    if 'name="matter"' not in s: fail('forms',f'{f}: no matter field')
    if '<optgroup' not in s: warn('forms',f'{f}: dropdown not grouped')
    if f!='index.html' and 'href="/#contact"' in s and 'id="contact"' in s:
        fail('forms',f'{f}: cross-page /#contact link')
for f in PAGES:
    s=txt(f)
    if 'wl.css' in s and 'tracking.js' not in s: fail('tracking',f'{f}: no tracking.js')
    if 'wl.css' in s and 'AW-17980143249' not in s: fail('tracking',f'{f}: no gtag')
tr=open('js/tracking.js').read()
if 'LABEL_HERE' in tr: warn('tracking',f'tracking.js: {tr.count("LABEL_HERE")} placeholder labels unset')

# ---------- sitemap ----------
sm=open('sitemap.xml').read()
try:
    import xml.etree.ElementTree as ET; ET.fromstring(sm)
except Exception as e: fail('sitemap',f'invalid XML: {e}')
listed={u.replace('https://westernlegal.co.uk','').strip('/') for u in re.findall(r'<loc>([^<]*)</loc>',sm)}
for u in listed:
    if u and u not in have: fail('sitemap',f'lists non-existent /{u}')
for p in have:
    if p in ('','index','portal','thank-you','insights/index'): continue
    if p not in listed: fail('sitemap',f'missing /{p}')
if len(set(re.findall(r'<lastmod>([^<]*)</lastmod>',sm)))>1: warn('sitemap','mixed lastmod dates')

# ---------- report ----------
print('='*70)
print(f'AUDIT: {len(PAGES)} pages, {len(imgs)} images, {len(listed)} sitemap URLs')
print('='*70)
if FAIL:
    print(f'\n{len(FAIL)} FAILURES')
    g=defaultdict(list)
    for c,m in FAIL: g[c].append(m)
    for c in sorted(g):
        print(f'\n  [{c}] {len(g[c])}')
        for m in g[c][:14]: print('   ',m)
        if len(g[c])>14: print(f'    ... {len(g[c])-14} more')
else: print('\nNO FAILURES')
if WARN:
    g=defaultdict(list)
    for c,m in WARN: g[c].append(m)
    print(f'\n{len(WARN)} WARNINGS')
    for c in sorted(g):
        print(f'\n  [{c}] {len(g[c])}')
        for m in g[c][:8]: print('   ',m)
        if len(g[c])>8: print(f'    ... {len(g[c])-8} more')
sys.exit(1 if FAIL else 0)
