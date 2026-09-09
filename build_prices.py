#!/usr/bin/env python3
"""Generate prices.json and prices.md from every schedule table on the site. Single source of truth for quoting."""
import re,glob,json,html,datetime
rows=[];pages=0
def clean(x): return html.unescape(re.sub(r'<[^>]+>','',x)).replace('\xa0',' ').strip()
for f in sorted(glob.glob("*.html")):
    s=open(f).read()
    tables=re.findall(r'<table[^>]*>(.*?)</table>',s,re.S)
    if not tables: continue
    pages+=1
    slug="/"+f[:-5] if f!="index.html" else "/"
    title=clean(re.search(r'<title>([^<]*)',s).group(1)).split("|")[0].strip()
    for t in tables:
        for tr in re.findall(r'<tr>(.*?)</tr>',t,re.S):
            tds=re.findall(r'<td[^>]*>(.*?)</td>',tr,re.S)
            if len(tds)<2: continue
            name=clean(tds[0]);desc=clean(tds[1]) if len(tds)>2 else "";fee=clean(tds[-1])
            if not re.search(r'£|€|\$|\b(EUR|USD|CHF|GBP|AED|SEK|NOK|DKK|SAR|BRL|MXN)\b',fee): continue
            rows.append({"page":slug,"page_title":title,"product":name,"scope":desc,"fee":fee})
stamp=datetime.date.today().isoformat()
json.dump({"generated":stamp,"source":"https://westernlegal.co.uk schedules","rules":["Quote only what appears here, at the fee shown. 'from' means the base tier; anything beyond the stated scope is quoted in writing before work.","No VAT is charged. Official fees are included only where the scope says so.","Instant pay exists for UK trade mark filing only (one, two or three classes). Everything else is quote first.","If a figure is not in this file it is not a Western Legal price."],"count":len(rows),"rows":rows},open("prices.json","w"),indent=1,ensure_ascii=False)
with open("prices.md","w") as m:
    m.write(f"# Western Legal master price list\nGenerated {stamp} from the live schedules. {len(rows)} rows across {pages} pages. No VAT. If a figure is not here it is not a Western Legal price.\n\n")
    cur=None
    for r in rows:
        if r["page"]!=cur: cur=r["page"];m.write(f"\n## {r['page_title']}  ({cur})\n")
        m.write(f"- {r['product']} | {r['fee']} | {r['scope']}\n")
print(len(rows),"rows",pages,"pages")
