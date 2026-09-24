#!/usr/bin/env python3
"""Build a service page from the uk-market-entry shell. build(spec) writes <slug>.html and adds the sitemap entry."""
import re,json,datetime
def build(s):
    src=open("uk-market-entry.html").read()
    today=s.get("date",datetime.date.today().isoformat()); url="https://westernlegal.co.uk/"+s["slug"]
    head=src[:src.find("</header>")]; body=src[src.find("</header>"):src.find("<footer")]; foot=src[src.find("<footer"):]
    head=re.sub(r"<title>[^<]*</title>",f"<title>{s['title']}</title>",head)
    for tag,val in [("description",s["desc"]),("twitter:title",s["title"]),("twitter:description",s["desc"])]:
        head=re.sub(rf'<meta name="{tag}" content="[^"]*"',f'<meta name="{tag}" content="{val}"',head)
    for tag,val in [("og:title",s["title"]),("og:description",s["desc"]),("og:url",url),("og:image","https://westernlegal.co.uk/img/"+s["image"])]:
        head=re.sub(rf'<meta property="{tag}" content="[^"]*"',f'<meta property="{tag}" content="{val}"',head)
    head=re.sub(r'<link rel="canonical" href="[^"]*"',f'<link rel="canonical" href="{url}"',head)
    head=re.sub(r'<link rel="preload" as="image" href="[^"]*"',f'<link rel="preload" as="image" href="/img/{s["image"]}"',head)
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faqs"]]}
    svc={"@context":"https://schema.org","@type":"Service","name":s["service_name"],"serviceType":s["service_name"],"url":url,"description":s["desc"],"areaServed":s.get("area",["GB"]),"provider":{"@type":"Organization","name":"Western Legal","url":"https://westernlegal.co.uk"},"offers":[{"@type":"Offer","name":r[0],"price":r[2],"priceCurrency":"GBP","description":r[1]} for r in s["rows"] if r[2]]}
    scripts=re.findall(r'<script type="application/ld\+json">.*?</script>',head,re.S)
    head=head.replace(scripts[0],'<script type="application/ld+json">'+json.dumps(faq,ensure_ascii=False)+'</script>',1)
    if len(scripts)>1: head=head.replace(scripts[1],'<script type="application/ld+json">'+json.dumps(svc,ensure_ascii=False)+'</script>',1)
    # crumbs, hero
    body=re.sub(r'<div class="wrap crumbs">.*?</div>',f'<div class="wrap crumbs"><a href="/">Western Legal</a> / {s["crumb"]}</div>',body,count=1,flags=re.S)
    body=re.sub(r'<div class="eyebrow">[^<]*</div>',f'<div class="eyebrow">{s["eyebrow"]}</div>',body,count=1)
    body=re.sub(r'<h1>.*?</h1>',f'<h1>{s["h1"]}</h1>',body,count=1,flags=re.S)
    body=re.sub(r'<p class="lede">.*?</p>',f'<p class="lede">{s["lede"]}</p>',body,count=1,flags=re.S)
    body=re.sub(r'<div class="qq-fee">[^<]*</div>',f'<div class="qq-fee">{s["qqfee"]}</div>',body,count=1)
    body=body.replace('<input type="hidden" name="matter" value="Selling into the UK from abroad">',f'<input type="hidden" name="matter" value="{s["matter"]}">')
    body=re.sub(r'<div class="cta">.*?</div>',f'<div class="cta"><a class="btn tape" href="#contact">{s["cta"]}</a><a class="btn ghost" href="{s["cta2"][0]}">{s["cta2"][1]}</a></div>',body,count=1,flags=re.S)
    body=re.sub(r'<div class="proof">.*?</div></div>','<div class="proof">'+"".join(f'<div><b>{b}</b>{t}</div>' for b,t in s["proof"])+'</div></div>',body,count=1,flags=re.S)
    body=re.sub(r'<img class="photo" src="[^"]*" alt="[^"]*"',f'<img class="photo" src="/img/{s["image"]}" alt="{s["image_alt"]}"',body,count=1)
    body=re.sub(r'<h2>The market-entry fee schedule\.</h2>',f'<h2>{s["fees_h2"]}</h2>',body,count=1)
    rows="".join(f'<tr><td><b>{n}</b></td><td style="color:var(--slate);font-size:14px">{d}</td><td class="fee"><b>{("from £"+f"{f:,}") if isinstance(f,int) else f}</b></td></tr>' for n,d,f,*_ in s["rows"])
    body=re.sub(r'<tbody>.*?</tbody>',f'<tbody>{rows}</tbody>',body,count=1,flags=re.S)
    body=re.sub(r'<div class="note">.*?</div>',f'<div class="note">{s["note"]} Schedule current as at {datetime.date.fromisoformat(today).strftime("%-d %B %Y")}.</div>',body,count=1,flags=re.S)
    body=re.sub(r'<h2>Built for companies entering Britain from abroad\.</h2>',f'<h2>{s["why_h2"]}</h2>',body,count=1)
    steps="".join(f'<div class="step reveal"><div class="n">{k}</div><h3>{h}</h3><p>{p}</p></div>' for k,h,p in s["steps"])
    body=re.sub(r'<div class="steps">.*?</div>\n</div></section>',f'<div class="steps">{steps}</div>\n</div></section>',body,count=1,flags=re.S)
    body=re.sub(r'<h2>UK expansion FAQs\.</h2>',f'<h2>{s["faq_h2"]}</h2>',body,count=1)
    faqs="".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in s["faqs"])
    body=re.sub(r'<div class="faq reveal">.*?</div>\n<div class="readnext reveal">.*?</div></div></section>',f'<div class="faq reveal">{faqs}</div>\n<div class="readnext reveal"><span class="k">Read next</span>'+"".join(f'<a href="{h}">{t}</a>' for h,t in s["readnext"])+'</div></div></section>',body,count=1,flags=re.S)
    page=head+body+foot
    page=re.sub(r"WL-2026-\d\d-\d\d",f"WL-{today}",page)
    open(s["slug"]+".html","w").write(page)
    sm=open("sitemap.xml").read()
    if url not in sm: sm=sm.replace("</urlset>",f"<url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url></urlset>"); open("sitemap.xml","w").write(sm)
    txt=re.sub(r'<[^>]+>',' ',body); return len(txt.split()), re.findall(r'[—–]|\b\w+-\w+\b',txt)[:12], ("all EU" in txt, "law firm" in txt.lower())
