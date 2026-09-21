#!/usr/bin/env python3
"""Create an insights article from the standard shell. Usage: import and call build(spec)."""
import re,json,datetime
def build(spec):
    src=open("insights/section-25-notice-received.html").read()
    head=src[:src.find("</head>")]; mid=src[src.find("</head>"):src.find("<article")]; tail=src[src.find("</article>"):]
    slug=spec["slug"]; url=f"https://westernlegal.co.uk/insights/{slug}"; today=spec.get("date",datetime.date.today().isoformat())
    dt=datetime.date.fromisoformat(today); nice=f"{dt.day} {dt.strftime('%B %Y')}"
    head=re.sub(r"<title>[^<]*</title>",f"<title>{spec['seo_title']}</title>",head)
    for tag,val in [("description",spec["desc"]),("twitter:title",spec["seo_title"]),("twitter:description",spec["desc"])]:
        head=re.sub(rf'<meta name="{tag}" content="[^"]*"',f'<meta name="{tag}" content="{val}"',head)
    for tag,val in [("og:title",spec["seo_title"]),("og:description",spec["desc"]),("og:url",url),("og:image",spec["image"])]:
        head=re.sub(rf'<meta property="{tag}" content="[^"]*"',f'<meta property="{tag}" content="{val}"',head)
    head=re.sub(r'<link rel="canonical" href="[^"]*"',f'<link rel="canonical" href="{url}"',head)
    schema={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":spec["seo_title"],"description":spec["desc"],"datePublished":today,"dateModified":today,"mainEntityOfPage":url,"image":spec["image"],"author":{"@type":"Person","name":"Santosh Pandey","jobTitle":"Solicitor of England and Wales","url":"https://westernlegal.co.uk/about"},"publisher":{"@type":"Organization","name":"Western Legal","url":"https://westernlegal.co.uk","logo":{"@type":"ImageObject","url":"https://westernlegal.co.uk/logo-wordmark-navy.svg"}},"about":{"@type":"Thing","name":spec["about"]},"mentions":[{"@type":"Service","name":spec["service_name"],"url":"https://westernlegal.co.uk"+spec["service"]}]},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in spec["faqs"]]}]}
    head=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script>',head,count=1,flags=re.S)
    body=f'<article class="article"><div class="wrap" style="max-width:820px;padding-top:34px">\n<span class="kicker">{spec["kicker"]} · {spec["mins"]} min read · {nice}</span>\n<h1>{spec["h1"]}</h1>\n<p class="lede">{spec["lede"]}</p>\n<div class="fastnote reveal" style="margin:22px 0"><span class="k">FIXED FEE</span><p>{spec["feebox"]} No VAT. Advice by Santosh Pandey, Solicitor of England and Wales, SRA No. 641612. Handled entirely in writing. <a href="{spec["service"]}">{spec["service_link"]}</a>.</p></div>\n'+spec["html"]+'\n<div class="faq reveal" style="margin-top:34px"><h2 style="font-size:20px">Questions clients ask</h2>'
    for q,a in spec["faqs"]: body+=f"<details><summary>{q}</summary><p>{a}</p></details>"
    body+='</div>\n<div class="readnext reveal"><span class="k">Read next</span>'+"".join(f'<a href="{h}">{t}</a>' for h,t in spec["readnext"])+'</div>\n</div>'
    page=head+mid+body+tail
    page=re.sub(r"WL-2026-\d\d-\d\d",f"WL-{today}",page)
    open(f"insights/{slug}.html","w").write(page)
    idx=open("insights/index.html").read()
    card=f'<div class="art-card reveal"><span class="tag">{spec["kicker"]}</span><h3><a href="/insights/{slug}">{spec["card_title"]}</a></h3><p>{spec["card_text"]}</p></div>'
    if f"/insights/{slug}" not in idx: idx=idx.replace('<div class="art-grid">','<div class="art-grid">'+card,1); open("insights/index.html","w").write(idx)
    sm=open("sitemap.xml").read()
    if url not in sm:
        sm=sm.replace("</urlset>",f"<url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url></urlset>")
        sm=re.sub(r"(<loc>https://westernlegal.co.uk/insights</loc><lastmod>)[0-9-]+",rf"\g<1>{today}",sm); open("sitemap.xml","w").write(sm)
    words=len(re.sub(r'<[^>]+>',' ',body).split()); bad=re.findall(r'[—–]|\S[a-z]-[a-z]\S*',re.sub(r'<[^>]+>',' ',body))
    return words,bad
