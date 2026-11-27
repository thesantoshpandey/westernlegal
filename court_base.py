#!/usr/bin/env python3
"""Shared page builder for the financial centre court pages (26 Nov 2026).
Built from the business-solicitor shell. Run from the westernlegal repo root."""
import re, json, html

SHELL = open('business-solicitor.html', encoding='utf-8').read()
HEAD_END = SHELL.find('</head>')
HEADER_START = SHELL.find('<header class="site">')
HEADER_END = SHELL.find('</header>') + len('</header>')
FOOTER_START = SHELL.find('<footer class="site">')
FOOTER = SHELL[FOOTER_START:]
NAV = SHELL[HEADER_START:HEADER_END]
BODY_OPEN = SHELL[SHELL.find('<body'):HEADER_START]

TP = ('<p class="tpline" style="order:2;margin:10px 0 0;font-size:14px;font-weight:600;letter-spacing:.01em">'
      '<a href="https://uk.trustpilot.com/review/westernlegal.co.uk" target="_blank" rel="noopener" '
      'style="color:#E8B54A;text-decoration:none"><span aria-hidden="true">★★★★★</span> '
      'Rated 5 stars on Trustpilot by every client who has reviewed us</a></p>')

STAMP = SHELL[SHELL.find('<svg class="stamp"'):SHELL.find('</svg>', SHELL.find('<svg class="stamp"')) + 6]
CONTACT = SHELL[SHELL.find('<section id="contact"'):FOOTER_START]
DATE = '26 November 2026'
MARK = 'WL-2026-11-26'

ADVOCACY_OLD = 'Reserved legal activities and matters requiring court advocacy are conducted with instructed counsel.'
ADVOCACY_NEW = ('Reserved legal activities in England and Wales are conducted with instructed counsel. Who appears before the court '
                'named on this page, and on what basis, is confirmed in writing before you instruct.')

STD_BASIS = [
    'Western Legal Corporation Limited is not itself authorised by the Solicitors Regulation Authority; regulation is personal to the solicitor. '
    'The professional indemnity insurance that applies to your matter is confirmed to you in writing before you instruct.',
    'Court fees, and any costs the court orders a party to pay, are separate from our fee. Court fees are confirmed to you before they are paid.',
]

def e(x):
    return html.escape(x, quote=False)

def page(p):
    url = 'https://westernlegal.co.uk/' + p['slug']
    head = SHELL[:HEAD_END]
    head = re.sub(r'<title>.*?</title>', '<title>' + e(p['title']) + '</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + e(p['desc']) + '">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + url + '">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + e(p['title']) + '">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + e(p['desc']) + '">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="' + url + '">', head)
    head = head.replace('/img/hero-city.jpg', '/img/' + p['img'])
    head = re.sub(r'<meta name="content-version" content="[^"]*">', '<meta name="content-version" content="真 ' + MARK + '">', head)
    head = head.replace('/js/tracking.js?v=20260917b', '/js/tracking.js?v=20261113a')
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r'<[^>]+>', '', a))}} for q, a in p['faq']]}
    offers = [{"@type": "Offer", "name": name, "description": scope} for name, scope, fee in p['rows']]
    service = {"@context": "https://schema.org", "@type": "Service", "name": p['service'], "serviceType": p['service'],
               "url": url, "description": p['desc'], "areaServed": [p['area']],
               "provider": {"@type": "Organization", "name": "Western Legal", "url": "https://westernlegal.co.uk"},
               "offers": offers}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Western Legal", "item": "https://westernlegal.co.uk/"},
        {"@type": "ListItem", "position": 2, "name": p['crumb'], "item": url}]}
    ld = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in (faq, service, crumbs))
    head = head + ld + '</head>'

    proof = ''.join('<div><b>%s</b>%s</div>' % (a, b) for a, b in p['proof'])
    hero = f'''<div class="wrap crumbs"><a href="/">Western Legal</a> / {e(p['crumb'])}</div>
<section class="hero" style="padding-top:40px"><div class="wrap">
<div>
<div class="eyebrow">{p['eyebrow']}</div>
<h1><span class="h1l">{p['h1l']}</span><span class="h1s">{p['h1s']}</span></h1>{TP}
<p class="lede">{p['lede']}</p><p class="writtenline">{p['written']}</p>
<div class="qq" id="qq">
<div class="qq-fee">{p['qqfee']}</div><div class="qq-scope">{p['qqscope']}</div>
<div class="qq-proof">Solicitor of England &amp; Wales · SRA 641612</div>
<form class="qqform" id="qqform" novalidate onsubmit="return false" data-mode="short:true" data-endpoint="/api/lead">
<div style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="text" name="name" placeholder="Your name" autocomplete="name" aria-label="Your name">
<input type="text" name="contact" placeholder="Email or WhatsApp number" autocomplete="email" aria-label="Email or WhatsApp number">
<textarea name="need" rows="2" maxlength="600" placeholder="What do you need? One line is enough (optional)" aria-label="What do you need (optional)"></textarea>
<input type="hidden" name="matter" value="{e(p['matter'])}">
<input type="hidden" name="short" value="true">
<button type="submit" class="btn qq-btn">Get my fixed quote &rarr;</button>
<p class="qq-micro">Replies within the hour in business hours.</p>
</form>
<p class="qq-wa">Prefer WhatsApp? <a href="https://wa.me/447822014066" target="_blank" rel="noopener">Message us</a></p>
</div><div class="cta"><a class="btn tape" href="#contact">Get my fixed quote</a><a class="btn ghost" href="#jurisdiction">What the court hears</a></div>
<div class="proof">{proof}</div>
</div>
<div class="art"><img class="photo" src="/img/{p['img']}" alt="{e(p['alt'])}" fetchpriority="high" loading="eager" width="{p['w']}" height="{p['h']}"></div>
</div></section>
'''
    cards = ''.join('<div class="step reveal"><div class="n">%s</div><h3>%s</h3><p>%s</p></div>' % c for c in p['cards'])
    who = f'''
<section id="what-we-do" class="tint"><div class="wrap">
<span class="kicker">Who it is for</span>
<h2>{p['who_h2']}</h2>
<p class="lede" style="max-width:820px">{p['who_lede']}</p>
<div class="steps">{cards}</div>
<p style="max-width:820px;margin-top:28px">{p['who_more']}</p>
</div></section>
'''
    heads = ''.join('<div class="cell reveal"><h3>%s</h3><p>%s</p></div>' % (a, b) for a, b in p['heads'])
    jur = f'''
<section id="jurisdiction"><div class="wrap">
<span class="kicker">Jurisdiction</span>
<h2>{p['jur_h2']}</h2>
<div class="grid c2" style="margin-top:28px">{heads}</div>
<div style="max-width:820px;margin-top:32px"><h3>{p['not_h3']}</h3><p style="margin-top:10px">{p['not_p']}</p></div>
</div></section>
'''
    aud = ('<section id="rights-of-audience" class="tint"><div class="wrap" style="max-width:860px"><span class="kicker">Rights of audience</span><h2>'
           + p['aud_h2'] + '</h2>' + ''.join('<p style="margin-top:14px">' + x + '</p>' for x in p['aud'] + STD_BASIS) + '</div></section>\n')
    rows = ''.join('<tr><td><b>%s</b></td><td style="color:var(--slate);font-size:14px">%s</td><td class="fee"><b>%s</b></td></tr>' % (e(a), e(b), e(c)) for a, b, c in p['rows'])
    fees = f'''
<section id="fees"><div class="wrap">
<span class="kicker">Fees</span>
<h2>{p['fees_h2']}</h2>
<div class="reveal" style="margin-top:36px;border:1px solid var(--tape);background:var(--panel);padding:14px 20px;font-family:var(--mono);font-size:13px;color:var(--ink)"><b style="color:var(--tape)"><b>FIXED FEES</b>: each stage agreed in writing before any work on it begins, with the date it will be delivered. The fee quoted is the fee paid, and it does not change after you accept it.</div><div class="schedule reveal">{STAMP}
<div class="head"><span class="t">Schedule of fees</span><span class="t">Fixed fee per stage · No VAT</span></div>
<table><thead><tr><th>Item</th><th>What it covers</th><th style="text-align:right">Fee</th></tr></thead>
<tbody>{rows}</tbody></table><p class="fee-confirm">The fixed fee for each stage, and its delivery date, are confirmed in writing once the papers have been read.</p>
<div class="note">Each stage is quoted for your matter and fixed in writing before you pay anything; the fee does not change after that. No VAT is charged: the fee quoted is the fee paid. Court fees, and any costs the court orders a party to pay, are separate. Schedule current as at {DATE}.</div>
</div>
</div></section>
'''
    steps = ''.join('<div class="step reveal"><div class="n">%02d</div><h3>%s</h3><p>%s</p></div>' % (i + 1, a, b) for i, (a, b) in enumerate(p['how']))
    how = f'''
<section class="tint"><div class="wrap">
<span class="kicker">How it works</span>
<h2>{p['how_h2']}</h2>
<div class="steps">{steps}</div>
</div></section>
'''
    faqs = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), a) for q, a in p['faq'])
    rn = ''.join('<a href="%s">%s</a>' % (h, t) for h, t in p['readnext'])
    faqsec = f'''
<section><div class="wrap">
<span class="kicker">Common questions</span>
<h2>{p['faq_h2']}</h2>
<div class="faq reveal">{faqs}</div>
<div class="readnext reveal"><span class="k">Read next</span>{rn}</div></div></section>
'''
    local = ''
    if p.get('ar'):
        a = p['ar']
        local = ('<section class="tint"><div class="wrap" style="max-width:860px"><h2 lang="ar" dir="rtl">' + a['h2'] + '</h2>'
                 + ''.join('<p lang="ar" dir="rtl">' + x + '</p>' for x in a['p'])
                 + '<p lang="ar" dir="rtl"><a href="/ar">الصفحة العربية الكاملة: العقارات والشركات والنزاعات أمام محاكم المراكز المالية</a></p>'
                 + '<p style="font-size:13.5px;color:var(--slate);margin-top:14px">Advice, pleadings and correspondence are in English. '
                 'Enquiries and documents are welcome in Arabic, and certified translation or an interpreter is arranged where needed, '
                 'with the cost agreed before it is incurred.</p></div></section>\n')
    contact = CONTACT.replace('<section id="contact" class="tint">', '<section id="contact">')
    foot = FOOTER.replace('真 WL-2026-11-05', '真 ' + MARK)
    assert ADVOCACY_OLD in foot
    foot = foot.replace(ADVOCACY_OLD, ADVOCACY_NEW)
    foot = foot.replace('</body></html>', '<script>window.WL_PAGE_EVENTS={prefix:"%s",labels:{form_submit:"",whatsapp_tap:""}};</script></body></html>' % p['events'])
    out = head + '\n' + BODY_OPEN + NAV + '\n' + hero + who + jur + aud + fees + how + faqsec + local + contact + foot
    open(p['slug'] + '.html', 'w', encoding='utf-8').write(out)
    print('wrote', p['slug'], len(out))
