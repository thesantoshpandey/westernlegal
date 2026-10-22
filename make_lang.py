#!/usr/bin/env python3
"""Local language desk pages (22 Oct 2026): /de, /schweiz, /nl, /sv, /fi.
Built from the /ja template. Figures come only from the existing desk schedules
(/germany, /switzerland, /netherlands, /nordics) as listed in prices.json.
Scope on every page: English law and UK trade mark procedure only. No local law,
no EU law. Title is "Solicitor (England and Wales)" in every language, never a
local lawyer title. Run: python3 make_lang.py"""
import json, html, re

V_CSS = '20261010a'
V_WL = '20261022a'
V_CONSENT = '20261022a'
V_TRACK = '20260917b'
MARK = 'WL-2026-10-22'

HEAD_TRACK = ('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}(function(){var c=null;try{c=localStorage.getItem(\'wl_consent\')}catch(e){}if(!c)document.documentElement.classList.add(\'cpending\');var g=(c===\'accepted\')?\'granted\':\'denied\';gtag(\'consent\',\'default\',{ad_storage:g,analytics_storage:g,ad_user_data:g,ad_personalization:g,functionality_storage:\'granted\',security_storage:\'granted\',wait_for_update:500});window.uetq=window.uetq||[];window.uetq.push(\'consent\',\'default\',{ad_storage:g});})();</script>'
              '<script async src="https://www.googletagmanager.com/gtag/js?id=AW-17980143249"></script>'
              '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","AW-17980143249");</script>'
              '<script>(function(w,d,t,u,o){w[u]=w[u]||[],o.ts=(new Date).getTime();var n=d.createElement(t);n.src="https://bat.bing.net/bat.js?ti="+o.ti+("uetq"!=u?"&q="+u:""),n.async=1,n.onload=n.onreadystatechange=function(){var s=this.readyState;s&&"loaded"!==s&&"complete"!==s||(o.q=w[u],w[u]=new UET(o),w[u].push("pageLoad"),n.onload=n.onreadystatechange=null)};var i=d.getElementsByTagName(t)[0];i.parentNode.insertBefore(n,i);})(window,document,"script","uetq",{ti:"343268376",enableAutoSpaTracking:true});</script>'
              f'<script src="/js/consent.js?v={V_CONSENT}" defer></script><script src="/js/tracking.js?v={V_TRACK}" defer></script>')

STYLE = """<style>
body.lx h1,body.lx h2,body.lx h3{letter-spacing:0;hyphens:auto;overflow-wrap:break-word}
body.lx .eyebrow,body.lx .kicker{letter-spacing:.06em}
body.lx .qq{display:block}
body.lx .hero .wrap{grid-template-columns:1.15fr .85fr}
body.lx .ennote{display:inline-block;margin-top:14px;padding:8px 12px;border:1px solid var(--gold);color:var(--ink);font-weight:600;font-size:15px}
body.lx .jsec{padding:56px 0;border-top:1px solid var(--rule)}
body.lx .jsec:nth-of-type(even){background:#0E2445}
body.lx .jsec h2{font-size:clamp(22px,3vw,30px);margin:8px 0 10px}
body.lx .jsec p.sub{max-width:62ch}
body.lx .schedule{margin-top:22px}
body.lx .scope{font-size:14px;color:#C3D0E2;max-width:70ch}
body.lx .steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:24px}
body.lx .steps3 div{border-left:2px solid var(--gold);padding-left:14px}
body.lx .steps3 b{display:block;color:var(--gold);font-size:13px;letter-spacing:.06em;margin-bottom:6px}
body.lx .imp{margin-top:28px;font-size:13.5px;color:#C3D0E2;max-width:74ch;line-height:1.6}
body.lx .imp h3{font-size:15px;color:var(--ink);margin:0 0 8px}
body.lx .imp a{color:var(--ink);text-decoration:underline;display:inline}
@media(max-width:767px){body.lx .hero .wrap{grid-template-columns:1fr} body.lx .steps3{grid-template-columns:1fr} body.lx .hero .art{display:none} body.lx .ennote{font-size:14px}}
body.lx .hero .ennote{order:3}
@media(min-width:768px){
 body.lx .hero h1{font-size:clamp(30px,3.1vw,44px);line-height:1.25}
 body.lx .qq{max-width:540px;margin-top:22px}
 body.lx .qq-fee{font-size:19px;font-weight:700;color:var(--gold);margin-bottom:4px}
 body.lx .qq-proof{font-size:13.5px;color:#C3D0E2;margin-bottom:14px}
 body.lx .qqform input[type=text]{display:block;width:100%;box-sizing:border-box;padding:15px 16px;margin:0 0 10px;font-size:16px;background:rgba(255,255,255,.05);border:1px solid var(--rule);color:var(--ink);border-radius:2px}
 body.lx .qq-btn{display:block;width:100%;padding:16px;font-size:16px;font-weight:700;margin:4px 0 0}
 body.lx .qq-micro,body.lx .qq-wa{font-size:13.5px;color:#C3D0E2;margin:10px 0 0}
 body.lx .qq-wa{display:block}
 body.lx .qq-wa a{color:var(--ink);text-decoration:underline}
}
</style>"""

def esc(x): return html.escape(x, quote=True)

def table(head, rows):
    h = f'<thead><tr><th>{head[0]}</th><th>{head[1]}</th><th style="text-align:right">{head[2]}</th></tr></thead>'
    b = ''.join(f'<tr><td><b>{a}</b></td><td style="color:var(--slate);font-size:14px">{c}</td><td class="fee" style="text-align:right;white-space:nowrap">{f}</td></tr>' for a, c, f in rows)
    return f'<table>{h}<tbody>{b}</tbody></table>'

def section(sid, s, P):
    return (f'<section class="jsec" id="{sid}"><div class="wrap"><span class="kicker">{s["kicker"]}</span><h2>{s["h2"]}</h2>'
            f'<p class="sub">{s["sub"]}</p><div class="schedule">{table(P["thead"], s["rows"])}<p class="fee-confirm">{P["confirm"]}</p></div></div></section>')

def offers(P):
    out = []
    for s in P['sections']:
        for name, _, fee in s['rows']:
            c = re.search(r'\b(EUR|CHF|SEK|GBP)\b', fee)
            m = re.search(r"\d[\d\.' ,]*", fee)
            if not c or not m: continue
            n = re.sub(r'[^\d]', '', m.group(0))
            out.append({'@type': 'Offer', 'name': name, 'priceCurrency': c.group(1), 'price': n, 'description': P['novat']})
    return out[:6]

def build(P):
    lang = P['lang']; slug = P['slug']; url = f'https://westernlegal.co.uk/{slug}'
    schema = {'@context': 'https://schema.org', '@type': 'ProfessionalService', 'name': 'Western Legal', 'url': url, 'inLanguage': lang,
              'description': P['desc'], 'address': {'@type': 'PostalAddress', 'streetAddress': '19 The Circle, Queen Elizabeth Street', 'addressLocality': 'London', 'postalCode': 'SE1 2JE', 'addressCountry': 'GB'},
              'areaServed': P['area'], 'availableLanguage': [lang[:2], 'en'], 'makesOffer': offers(P)}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Western Legal', 'item': 'https://westernlegal.co.uk/'},
        {'@type': 'ListItem', 'position': 2, 'name': P['crumb'], 'item': url}]}
    alts = ''.join(f'<link rel="alternate" hreflang="{h}" href="https://westernlegal.co.uk/{s}">' for h, s in P['alts'])
    opts = ''.join(f'<option value="{v}">{t}</option>' for v, t in P['form']['opts'])
    F = P['form']
    secs = ''.join(section(sid, s, P) for sid, s in zip(P['ids'], P['sections']))
    steps = ''.join(f'<div><b>{t}</b>{d}</div>' for t, d in P['how']['steps'])
    imp = P['imp']
    imp_html = (f'<div class="imp"><h3>{imp["h"]}</h3><p>' + '<br>'.join(f'{k}: {v}' for k, v in imp['rows']) + '</p></div>')
    footer = open('ja.html', encoding='utf-8').read()
    footer = footer[footer.find('<footer class="site">'):footer.find('</footer>') + 9]
    footer = re.sub(r' · <a href="tel:[^"]*"[^>]*>[^<]*</a>', '', footer)
    footer = footer.replace('真 WL-2026-09-25', f'真 {MARK}')
    page = f'''<!doctype html><html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(P["title"])}</title><meta name="description" content="{esc(P["desc"])}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="{lang}" href="{url}">{alts}<link rel="alternate" hreflang="en-GB" href="https://westernlegal.co.uk/{P["desk"]}">
<meta property="og:title" content="{esc(P["title"])}"><meta property="og:description" content="{esc(P["desc"])}">
<meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:locale" content="{P["locale"]}">
<meta property="og:site_name" content="Western Legal">
<meta property="og:image" content="https://westernlegal.co.uk/img/hero-city.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="content-version" content="真 {MARK}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="/img/hero-city.jpg" fetchpriority="high">
<link rel="stylesheet" href="/css/wl.css?v={V_CSS}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script><link rel="icon" href="/logo-favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/logo-favicon.svg"><meta name="theme-color" content="#13294B">{HEAD_TRACK}{STYLE}</head>
<body class="lx">
<header class="site"><div class="wrap">
<a class="brand" href="/{slug}"><img class="brandmark" src="/logo-wordmark-cream.svg" alt="Western Legal" width="1092" height="78" decoding="async"><small>{P["brandsmall"]}</small></a>
<nav class="main"><a class="btn" href="#qq"><span class="bl">{P["navbtn"]}</span><span class="bs">{P["navbtn_s"]}</span></a></nav>
</div></header>
<section class="hero"><div class="wrap">
<div>
<div class="eyebrow">{P["eyebrow"]}</div>
<h1><span class="h1l">{P["h1l"]}</span><span class="h1s">{P["h1s"]}</span></h1>
<p class="lede">{P["lede"]}</p>
<p class="ennote">{P["note"]}</p>
<div class="qq" id="qq">
<div class="qq-fee">{F["fee"]}</div>
<div class="qq-proof">{F["proof"]}</div>
<form class="qqform" id="qqform" novalidate data-mode="short:true" data-endpoint="/api/lead">
<div style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="text" name="name" placeholder="{esc(F["name"])}" autocomplete="name" aria-label="{esc(F["name"])}">
<input type="text" name="contact" placeholder="{esc(F["contact"])}" autocomplete="email" aria-label="{esc(F["contact"])}">
<select name="has" class="qq-sel" required aria-label="{esc(F["has"])}"><option value="" selected disabled>{F["has"]}</option>{opts}</select>
<label class="qq-date"><span>{F["by"]}</span><input type="date" name="by" required></label>
<input type="hidden" name="matter" value="{P["matter"]}">
<input type="hidden" name="lang" value="{lang[:2]}">
<input type="hidden" name="short" value="true">
<button type="submit" class="btn qq-btn">{F["btn"]} &rarr;</button>
<p class="qq-micro">{F["micro"]}</p>
</form>
<p class="qq-wa">{F["wa"]} <a href="https://wa.me/447822014066" target="_blank" rel="noopener">{F["wa_link"]}</a></p>
</div>
</div>
<div class="art"><img class="photo" src="/img/hero-city.jpg" alt="{esc(P["img_alt"])}" fetchpriority="high" loading="eager" width="1400" height="933"></div>
</div></section>
{secs}
<section class="jsec" id="how"><div class="wrap"><span class="kicker">{P["how"]["kicker"]}</span><h2>{P["how"]["h2"]}</h2>
<div class="steps3">{steps}</div>
<p class="scope" style="margin-top:28px">{P["scope"]}</p>
<p class="scope">{P["company"]}</p>
{imp_html}
<p style="margin-top:22px"><a class="btn tape" href="#qq">{F["btn"]}</a></p>
</div></section>
{footer}
<script src="/js/wl.js?v={V_WL}" defer></script>
<a class="wa-float" href="https://wa.me/447822014066" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M16 3C9.4 3 4 8.4 4 15c0 2.1.6 4.2 1.6 6L4 29l8.2-1.5c1.2.5 2.5.8 3.8.8 6.6 0 12-5.4 12-12S22.6 3 16 3zm0 21.8c-1.2 0-2.4-.3-3.5-.8l-.6-.3-4.9.9 1-4.7-.3-.6c-.9-1.6-1.4-3.4-1.4-5.3 0-5.4 4.4-9.8 9.8-9.8s9.8 4.4 9.8 9.8-4.5 10.8-9.9 10.8zm5.4-7.3c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.1-.7-1.7-1-2.3-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.3 5.2 4.6.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.2-.3-.2-.6-.4z"/></svg></a><nav class="actionbar sticky" data-sticky="true" aria-label="{esc(P["navbtn_s"])}"><a href="https://wa.me/447822014066" target="_blank" rel="noopener">WhatsApp</a><a class="primary" href="#qq">{P["navbtn_s"]}</a></nav></body></html>
'''
    open(f'{slug}.html', 'w', encoding='utf-8').write(page)
    return page

# ---------------------------------------------------------------- content
SRA = 'Solicitors Regulation Authority, The Cube, 199 Wharfside Street, Birmingham B1 1RN'
RULES = '<a href="https://www.sra.org.uk/solicitors/standards-regulations/" target="_blank" rel="noopener">SRA Standards and Regulations</a>'
MAIL = '<a href="mailto:sp@westernlegal.co.uk">sp@westernlegal.co.uk</a>'

def de_common(cur, sym, n):
    """German text shared by /de (Germany, EUR) and /schweiz (Switzerland, CHF).
    sym: currency label shown; n: dict of figures already formatted."""
    ss = 'ss' if cur == 'CHF' else 'ß'
    return dict(
        thead=['Leistung', 'Umfang', 'Preis'],
        confirm=('Ihr Festpreis wird schriftlich bestätigt, sobald wir Ihre Unterlagen gesehen haben. '
                 f'Bei Zahlung innerhalb von 24 Stunden nach dieser Bestätigung gilt der ermä{ss}igte Preis.'),
        novat='keine MwSt.' if cur == 'EUR' else 'keine MWST',
        brandsmall='Solicitor (England und Wales) · London',
        navbtn='Festpreis anfragen', navbtn_s='Angebot',
        form=dict(fee=f'Festpreis · {"keine MwSt." if cur == "EUR" else "keine MWST"} · in {sym}',
                  proof='Solicitor (England und Wales) · SRA 641612',
                  name='Ihr Name (Firma)', contact='E-Mail oder WhatsApp-Nummer', has='Was liegt Ihnen vor?',
                  opts=[('Contract to sign', 'Vertrag zur Unterschrift'), ('Notice or letter received', 'Erhaltenes Schreiben oder Mahnung'),
                        ('Heads of terms', 'Eckpunkte oder Term Sheet'), ('Draft lease', 'Entwurf eines Mietvertrags in England'), ('Nothing yet', 'Noch nichts')],
                  by='Frist für Unterschrift oder Antwort', btn='Festpreisangebot anfordern',
                  micro='Antwort innerhalb einer Stunde während der britischen Geschäftszeiten.',
                  wa='Lieber per WhatsApp?', wa_link='Hier schreiben'),
        h1s='Englisches Recht zum Festpreis.',
        note=f'Anfragen, Unterlagen und schriftliche Beratung auf Deutsch. {"Massgeblich" if cur == "CHF" else "Maßgeblich"} ist die englische Fassung.',
        img_alt='Londoner City',
        how=dict(kicker='So läuft es ab', h2='Alles schriftlich.', steps=[
            ('1. Anfrage senden', 'Senden Sie über das Formular oben Ihren Namen und Ihre Kontaktdaten.'),
            ('2. Festpreis erhalten', 'Umfang und Festpreis erhalten Sie schriftlich per E-Mail. Das Angebot gilt 30 Tage.'),
            ('3. Zahlung und Beginn', 'Nach Zahlung per Karte, Apple Pay, Google Pay oder Überweisung beginnen wir.')]),
        company=('Western Legal Corporation Limited (eingetragen in England und Wales, Gesellschaftsnummer 10453250, Sitz 19 The Circle, Queen Elizabeth Street, London SE1 2JE). '
                 'Die Arbeit übernimmt Santosh Pandey, Solicitor (England und Wales), SRA-Nr. 641612. Die Western Legal Corporation Limited ist selbst nicht von der Solicitors Regulation Authority zugelassen; '
                 'die berufsrechtliche Aufsicht betrifft den Solicitor persönlich.'),
        imp=dict(h='Anbieterkennzeichnung', rows=[
            ('Anbieter', 'Western Legal Corporation Limited, 19 The Circle, Queen Elizabeth Street, London SE1 2JE, Vereinigtes Königreich'),
            ('Rechtsform und Register', 'Private company limited by shares, eingetragen beim Companies House (England und Wales) unter der Nummer 10453250'),
            ('Vertretungsberechtigt', 'Santosh Pandey, Director'),
            ('Kontakt', f'{MAIL}, WhatsApp +44 7822 014 066'),
            ('Berufsbezeichnung', 'Solicitor (England und Wales), verliehen im Vereinigten Königreich, SRA-Nr. 641612'),
            ('Aufsichtsbehörde', SRA),
            ('Berufsrechtliche Regelungen', RULES),
            ('Berufshaftpflichtversicherung', 'Versicherungssumme £2,000,000 je Schadensfall'),
            ('Umsatzsteuer', 'Es wird keine Umsatzsteuer berechnet.')]),
    )

DE = de_common('EUR', 'Euro', {})
DE.update(
    lang='de', slug='de', desk='germany', area='DE', locale='de_DE', cur='EUR', crumb='Deutschland',
    alts=[('de-CH', 'schweiz')],
    title='UK Marke anmelden und englisches Recht | Festpreise in EUR',
    desc='Britische Markenanmeldung, Verträge nach englischem Recht und Forderungen gegen britische Firmen. Solicitor (England und Wales), Festpreise in EUR.',
    matter='Germany desk enquiry (de)',
    eyebrow='Für deutsche Unternehmen mit Geschäft im Vereinigten Königreich',
    h1l='Britische Marke, Verträge nach englischem Recht, offene Rechnungen in England. Der Festpreis steht schriftlich fest, bevor die Arbeit beginnt.',
    lede='Santosh Pandey, Solicitor (England und Wales), betreut Ihr Anliegen nach englischem Recht. Alle Preise sind Festpreise in Euro, ohne Mehrwertsteuer.',
    ids=['trademark', 'contracts', 'debt', 'gdpr'],
    sections=[
        dict(kicker='Britische Marke', h2='Ihre Marke im Vereinigten Königreich schützen.',
             sub=('Eine Unionsmarke, die nach dem 1. Januar 2021 eingetragen wurde, gilt im Vereinigten Königreich nicht. Für den britischen Markt brauchen Sie eine eigene Anmeldung beim britischen Markenamt (UKIPO) '
                  'und eine Zustelladresse im Vereinigten Königreich, in Gibraltar oder auf den Kanalinseln. Beides übernehmen wir: Recherche, Waren- und Dienstleistungsverzeichnis, Anmeldung innerhalb von 48 Stunden und die üblichen Antworten im Verfahren.'),
             rows=[('Britische Marke, eine Klasse', 'Anmeldung beim UKIPO innerhalb von 48 Stunden nach Beauftragung, mit britischer Zustelladresse', 'ab EUR 645'),
                   ('Jede weitere Klasse', 'Bei der Anmeldung hinzugefügt', 'EUR 285'),
                   ('Verteidigung im Widerspruchsverfahren', 'TM8 und Beweisrunden, Festpreis für die gesamte Verteidigung', 'EUR 1.405')]),
        dict(kicker='Verträge nach englischem Recht', h2='Verträge mit britischen Partnern prüfen und entwerfen.',
             sub=('Wir prüfen Verträge, die Ihnen britische Kunden, Lieferanten oder Partner vorlegen, mit schriftlichem Risikobericht und Änderungsvorschlägen, '
                  'oder entwerfen den Vertrag nach Ihren Konditionen. Gegenstand ist immer ein Vertrag, für den englisches Recht gilt.'),
             rows=[('Geheimhaltungsvereinbarung (NDA)', 'Entwurf oder Prüfung nach englischem Recht', 'ab EUR 285'),
                   ('Vertragsprüfung mit Änderungen', 'Vertriebs-, Liefer-, Lizenz-, SaaS- oder Dienstleistungsverträge, mit schriftlichem Risikobericht', 'ab EUR 695'),
                   ('Allgemeine Geschäftsbedingungen', 'Kunden- oder Lieferanten-AGB nach englischem Recht', 'ab EUR 760'),
                   ('Individueller Handelsvertrag', 'Nach Ihren kaufmännischen Konditionen entworfen', 'ab EUR 1.460')]),
        dict(kicker='Offene Rechnungen in England', h2='Wenn eine britische Firma nicht zahlt.',
             sub=('Wir fordern Geschäftsforderungen gegen Gesellschaften in England und Wales ein: mit einem förmlichen Aufforderungsschreiben vor Klageerhebung (letter before action), '
                  'der Korrespondenz und der Vergleichsverhandlung. Wird ein Gerichtsverfahren nötig, sagen wir es vorher und übergeben die vorbereitete Akte an einen beauftragten Barrister.'),
             rows=[('Aufforderungsschreiben an eine britische Firma', 'Förmliche Zahlungsaufforderung wegen einer Geschäftsforderung gegen eine Gesellschaft in England und Wales', 'ab EUR 695')]),
        dict(kicker='UK GDPR', h2='Kunden im Vereinigten Königreich, aber keine Niederlassung dort?',
             sub=('Wer ohne Niederlassung im Vereinigten Königreich Personen dort Waren oder Dienstleistungen anbietet oder deren Verhalten beobachtet, muss unter Umständen nach Artikel 27 UK GDPR '
                  'schriftlich einen Vertreter im Vereinigten Königreich benennen. Wir prüfen das schriftlich und übernehmen, wo nötig, die Vertretung und die britischen Datenschutzunterlagen.'),
             rows=[('UK GDPR und Website-Paket', 'Datenschutzerklärung, Cookie-Einwilligung, Bedingungen und Verarbeitungsverzeichnis für den britischen Markt', 'ab EUR 695'),
                   ('Vertreter im Vereinigten Königreich (jährlich)', 'Jahresfestpreis, vor Beginn schriftlich angeboten', 'Angebot schriftlich')])],
    scope=('Diese Seite betrifft englisches Recht und das britische Markenverfahren. Zum deutschen Recht und zum Recht der Europäischen Union beraten wir nicht. '
           'Prozessvertretung vor Gericht übernehmen wir nicht selbst; wird sie nötig, sagen wir es vorher und übergeben an einen beauftragten Barrister.'),
)

CH = de_common('CHF', 'CHF', {})
CH.update(
    lang='de-CH', slug='schweiz', desk='switzerland', area='CH', locale='de_CH', cur='CHF', crumb='Schweiz',
    alts=[('de-DE', 'de')],
    title='UK Marke und englisches Recht für Schweizer Firmen | CHF',
    desc='Britische Markenanmeldung, Verträge nach englischem Recht und UK GDPR für Schweizer Unternehmen. Solicitor (England und Wales), Festpreise in CHF.',
    matter='Switzerland desk enquiry (de)',
    eyebrow='Für Schweizer Unternehmen mit Geschäft im Vereinigten Königreich',
    h1l='Britische Marke, Verträge nach englischem Recht, UK GDPR. Der Festpreis steht schriftlich fest, bevor die Arbeit beginnt.',
    lede='Santosh Pandey, Solicitor (England und Wales), betreut Ihr Anliegen nach englischem Recht. Alle Preise sind Festpreise in Schweizer Franken, ohne Mehrwertsteuer.',
    ids=['trademark', 'contracts', 'gdpr'],
    sections=[
        dict(kicker='Britische Marke', h2='Ihre Marke im Vereinigten Königreich schützen.',
             sub=('Eine Schweizer Marke schützt das Vereinigte Königreich nicht, eine Unionsmarke, die nach dem 1. Januar 2021 eingetragen wurde, ebenfalls nicht. Für den britischen Markt brauchen Sie eine eigene Anmeldung beim britischen Markenamt (UKIPO) '
                  'und eine Zustelladresse im Vereinigten Königreich, in Gibraltar oder auf den Kanalinseln. Beides übernehmen wir: Recherche, Waren- und Dienstleistungsverzeichnis, Anmeldung innerhalb von 48 Stunden und die üblichen Antworten im Verfahren.'),
             rows=[('Britische Marke, eine Klasse', 'Anmeldung beim UKIPO innerhalb von 48 Stunden nach Beauftragung, mit britischer Zustelladresse', "ab CHF 850"),
                   ('Jede weitere Klasse', 'Bei der Anmeldung hinzugefügt', 'CHF 375'),
                   ('Verteidigung im Widerspruchsverfahren', 'TM8 und Beweisrunden, Festpreis für die gesamte Verteidigung', "CHF 1'850")]),
        dict(kicker='Verträge nach englischem Recht', h2='Verträge mit britischen Partnern prüfen und entwerfen.',
             sub=('Wir prüfen Verträge, die Ihnen britische Kunden, Lieferanten oder Partner vorlegen, mit schriftlichem Risikobericht und Änderungsvorschlägen, '
                  'oder entwerfen den Vertrag nach Ihren Konditionen. Gegenstand ist immer ein Vertrag, für den englisches Recht gilt.'),
             rows=[('Geheimhaltungsvereinbarung (NDA)', 'Entwurf oder Prüfung nach englischem Recht', 'ab CHF 375'),
                   ('Vertragsprüfung mit Änderungen', 'Vertriebs-, Liefer-, Lizenz-, SaaS- oder Dienstleistungsverträge, mit schriftlichem Risikobericht und Verhandlungspunkten', 'ab CHF 900'),
                   ('Allgemeine Geschäftsbedingungen', 'Kunden- oder Lieferanten-AGB nach englischem Recht', 'ab CHF 995'),
                   ('Individueller Handelsvertrag', 'Nach Ihren kaufmännischen Konditionen entworfen', "ab CHF 1'900")]),
        dict(kicker='UK GDPR', h2='Kunden im Vereinigten Königreich, aber keine Niederlassung dort?',
             sub=('Wer ohne Niederlassung im Vereinigten Königreich Personen dort Waren oder Dienstleistungen anbietet oder deren Verhalten beobachtet, muss unter Umständen nach Artikel 27 UK GDPR '
                  'schriftlich einen Vertreter im Vereinigten Königreich benennen. Wir prüfen das schriftlich und übernehmen, wo nötig, die Vertretung und die britischen Datenschutzunterlagen.'),
             rows=[('Prüfung und Vertreter im Vereinigten Königreich', 'Ob Artikel 27 UK GDPR für Sie gilt, und wo nötig die Vertretung zum Jahresfestpreis', 'Angebot schriftlich')])],
    scope=('Diese Seite betrifft ausschliesslich englisches Recht und das britische Markenverfahren. '
           'Prozessvertretung vor Gericht übernehmen wir nicht selbst; wird sie nötig, sagen wir es vorher und übergeben an einen beauftragten Barrister.'),
)

NL = dict(
    lang='nl', slug='nl', desk='netherlands', area='NL', locale='nl_NL', cur='EUR', crumb='Nederland', alts=[],
    title='Merk registreren in het VK en Engels recht | Vaste prijzen',
    desc='Britse merkregistratie, contracten naar Engels recht en UK GDPR. Solicitor (Engeland en Wales), vaste prijzen in euro, geen btw.',
    matter='Netherlands desk enquiry (nl)', thead=['Dienst', 'Omvang', 'Prijs'],
    confirm='Uw vaste prijs wordt schriftelijk bevestigd zodra wij uw documenten hebben gezien. Betaalt u binnen 24 uur na die bevestiging, dan geldt de verlaagde prijs.',
    novat='geen btw', brandsmall='Solicitor (Engeland en Wales) · Londen', navbtn='Vaste prijs aanvragen', navbtn_s='Offerte',
    eyebrow='Voor Nederlandse bedrijven die zaken doen in het Verenigd Koninkrijk',
    h1l='Uw merk in het Verenigd Koninkrijk, contracten naar Engels recht en UK GDPR. De vaste prijs staat schriftelijk vast voordat het werk begint.',
    h1s='Engels recht tegen een vaste prijs.',
    lede='Santosh Pandey, solicitor (Engeland en Wales), behandelt uw zaak naar Engels recht. Alle prijzen zijn vaste prijzen in euro, zonder btw.',
    note='Vragen, documenten en schriftelijk advies in het Nederlands. De Engelse versie is leidend.',
    form=dict(fee='Vaste prijs · geen btw · in euro', proof='Solicitor (Engeland en Wales) · SRA 641612',
              name='Uw naam (bedrijf)', contact='E-mailadres of WhatsAppnummer', has='Wat heeft u?',
              opts=[('Contract to sign', 'Te tekenen contract'), ('Notice or letter received', 'Ontvangen brief of aanmaning'),
                    ('Heads of terms', 'Heads of terms of intentieverklaring'), ('Draft lease', 'Concept huurovereenkomst in Engeland'), ('Nothing yet', 'Nog niets')],
              by='Uiterste datum voor tekenen of antwoorden', btn='Vaste prijs aanvragen',
              micro='Antwoord binnen het uur tijdens Britse kantooruren.', wa='Liever WhatsApp?', wa_link='Stuur hier een bericht'),
    img_alt='De City van Londen',
    ids=['trademark', 'contracts', 'gdpr'],
    sections=[
        dict(kicker='Brits merk', h2='Bescherm uw merk in het Verenigd Koninkrijk.',
             sub=('Een Uniemerk dat na 1 januari 2021 is ingeschreven, geldt niet in het Verenigd Koninkrijk. Voor de Britse markt is een eigen aanvraag nodig bij het Britse merkenbureau (UKIPO), '
                  'met een correspondentieadres in het Verenigd Koninkrijk, Gibraltar of op de Kanaaleilanden. Wij regelen beide: onderzoek, de lijst van waren en diensten, indiening binnen 48 uur en de gebruikelijke reacties in de procedure.'),
             rows=[('Brits merk, één klasse', 'Ingediend bij het UKIPO binnen 48 uur na opdracht, met Brits correspondentieadres', 'vanaf EUR 745'),
                   ('Elke extra klasse', 'Toegevoegd bij indiening', 'EUR 325'),
                   ('Verweer in een oppositie', 'TM8 en bewijsrondes, vaste prijs voor het hele verweer', 'EUR 1.610')]),
        dict(kicker='Contracten naar Engels recht', h2='Contracten met Britse partners beoordelen en opstellen.',
             sub=('Wij beoordelen contracten die Britse klanten, leveranciers of partners u voorleggen, met een schriftelijk risicorapport en voorstellen tot wijziging, '
                  'of stellen het contract op volgens uw voorwaarden. Het gaat altijd om een contract waarop Engels recht van toepassing is.'),
             rows=[('Geheimhoudingsovereenkomst (NDA)', 'Opgesteld of beoordeeld naar Engels recht', 'vanaf EUR 325'),
                   ('Contractbeoordeling met wijzigingen', 'Distributie-, leverings-, licentie-, SaaS- of dienstverleningsovereenkomsten, met schriftelijk risicorapport en onderhandelingspunten', 'vanaf EUR 800'),
                   ('Algemene voorwaarden', 'Klant- of leveranciersvoorwaarden naar Engels recht', 'vanaf EUR 875'),
                   ('Maatwerkcontract', 'Opgesteld op basis van uw commerciële voorwaarden', 'vanaf EUR 1.680')]),
        dict(kicker='UK GDPR', h2='Klanten in het Verenigd Koninkrijk, maar geen vestiging daar?',
             sub=('Wie zonder vestiging in het Verenigd Koninkrijk goederen of diensten aanbiedt aan personen daar, of hun gedrag volgt, moet mogelijk op grond van artikel 27 UK GDPR '
                  'schriftelijk een vertegenwoordiger in het Verenigd Koninkrijk aanwijzen. Wij beoordelen dat schriftelijk en verzorgen waar nodig de vertegenwoordiging en de Britse privacydocumenten.'),
             rows=[('UK GDPR en websitepakket', 'Privacyverklaring, cookietoestemming, voorwaarden en verwerkingsregister voor de Britse markt', 'vanaf EUR 695'),
                   ('Vertegenwoordiger in het VK (per jaar)', 'Vaste jaarprijs, vooraf schriftelijk geoffreerd', 'Schriftelijke offerte')])],
    how=dict(kicker='Zo werkt het', h2='Alles schriftelijk.', steps=[
        ('1. Aanvraag sturen', 'Stuur via het formulier hierboven uw naam en contactgegevens.'),
        ('2. Vaste prijs ontvangen', 'U ontvangt de omvang en de vaste prijs schriftelijk per E-mail. De offerte is 30 dagen geldig.'),
        ('3. Betaling en start', 'Na betaling per kaart, Apple Pay, Google Pay of bankoverschrijving beginnen wij.')]),
    scope=('Deze pagina betreft Engels recht en de Britse merkenprocedure. Over Nederlands recht en het recht van de Europese Unie adviseren wij niet. '
           'Vertegenwoordiging voor de rechter verzorgen wij niet zelf; als die nodig wordt, zeggen wij dat vooraf en dragen wij de zaak over aan een ingeschakelde barrister.'),
    company=('Western Legal Corporation Limited (ingeschreven in Engeland en Wales, bedrijfsnummer 10453250, statutair adres 19 The Circle, Queen Elizabeth Street, London SE1 2JE). '
             'De werkzaamheden worden verricht door Santosh Pandey, solicitor (Engeland en Wales), SRA-nummer 641612. Western Legal Corporation Limited is zelf niet erkend door de Solicitors Regulation Authority; '
             'het toezicht geldt de solicitor persoonlijk.'),
    imp=dict(h='Gegevens van de aanbieder', rows=[
        ('Aanbieder', 'Western Legal Corporation Limited, 19 The Circle, Queen Elizabeth Street, London SE1 2JE, Verenigd Koninkrijk'),
        ('Rechtsvorm en register', 'Private company limited by shares, ingeschreven bij Companies House (Engeland en Wales) onder nummer 10453250'),
        ('Bestuurder', 'Santosh Pandey, Director'),
        ('Contact', f'{MAIL}, WhatsApp +44 7822 014 066'),
        ('Beroepstitel', 'Solicitor (Engeland en Wales), verleend in het Verenigd Koninkrijk, SRA-nummer 641612'),
        ('Toezichthouder', SRA),
        ('Beroepsregels', RULES),
        ('Beroepsaansprakelijkheidsverzekering', 'Verzekerd bedrag £2,000,000 per aanspraak'),
        ('Btw', 'Er wordt geen btw in rekening gebracht.')]),
)

SV = dict(
    lang='sv', slug='sv', desk='nordics', area='SE', locale='sv_SE', cur='SEK', crumb='Sverige', alts=[],
    title='Varumärke i Storbritannien och engelsk rätt | Fasta priser',
    desc='Brittisk varumärkesansökan, avtal enligt engelsk rätt och krav mot brittiska bolag. Solicitor (England och Wales), fasta priser i SEK, ingen moms.',
    matter='Sweden desk enquiry (sv)', thead=['Tjänst', 'Omfattning', 'Pris'],
    confirm='Ert fasta pris bekräftas skriftligt när vi har sett era handlingar. Betalar ni inom 24 timmar efter bekräftelsen gäller det rabatterade priset.',
    novat='ingen moms', brandsmall='Solicitor (England och Wales) · London', navbtn='Begär fast pris', navbtn_s='Offert',
    eyebrow='För svenska företag med affärer i Storbritannien',
    h1l='Ert varumärke i Storbritannien, avtal enligt engelsk rätt och obetalda fakturor i England. Det fasta priset bestäms skriftligt innan arbetet börjar.',
    h1s='Engelsk rätt till fast pris.',
    lede='Santosh Pandey, solicitor (England och Wales), handlägger ert ärende enligt engelsk rätt. Alla priser är fasta priser, utan moms.',
    note='Frågor, handlingar och skriftlig rådgivning på svenska. Den engelska versionen gäller.',
    form=dict(fee='Fast pris · ingen moms · i SEK', proof='Solicitor (England och Wales) · SRA 641612',
              name='Ert namn (företag)', contact='E-post eller WhatsAppnummer', has='Vad har ni?',
              opts=[('Contract to sign', 'Avtal att underteckna'), ('Notice or letter received', 'Mottaget brev eller krav'),
                    ('Heads of terms', 'Heads of terms eller avsiktsförklaring'), ('Draft lease', 'Utkast till hyresavtal i England'), ('Nothing yet', 'Inget ännu')],
              by='Sista dag för underskrift eller svar', btn='Begär fast pris',
              micro='Svar inom en timme under brittisk kontorstid.', wa='Hellre WhatsApp?', wa_link='Skriv här'),
    img_alt='City of London',
    ids=['trademark', 'contracts', 'debt', 'gdpr'],
    sections=[
        dict(kicker='Brittiskt varumärke', h2='Skydda ert varumärke i Storbritannien.',
             sub=('Ett EU-varumärke som registrerats efter den 1 januari 2021 gäller inte i Storbritannien. För den brittiska marknaden krävs en egen ansökan hos den brittiska varumärkesmyndigheten (UKIPO) '
                  'och en delgivningsadress i Storbritannien, Gibraltar eller på Kanalöarna. Vi sköter båda: sökning, förteckning över varor och tjänster, ansökan inom 48 timmar och de vanliga svaren i förfarandet.'),
             rows=[('Brittiskt varumärke, en klass', 'Ansökan hos UKIPO inom 48 timmar efter uppdrag, med brittisk delgivningsadress', 'från SEK 7 100'),
                   ('Varje ytterligare klass', 'Läggs till vid ansökan', 'SEK 3 100'),
                   ('Försvar i invändningsförfarande', 'TM8 och bevisomgångar, fast pris för hela försvaret', 'SEK 15 400')]),
        dict(kicker='Avtal enligt engelsk rätt', h2='Granskning och upprättande av avtal med brittiska parter.',
             sub=('Vi granskar avtal som brittiska kunder, leverantörer eller partner lägger fram, med en skriftlig riskrapport och ändringsförslag, '
                  'eller upprättar avtalet utifrån era villkor. Det gäller alltid avtal där engelsk rätt är tillämplig.'),
             rows=[('Sekretessavtal (NDA)', 'Upprättat eller granskat enligt engelsk rätt', 'från SEK 3 100'),
                   ('Avtalsgranskning med ändringar', 'Distributions-, leverans-, licens-, SaaS- eller tjänsteavtal, med skriftlig riskrapport', 'från SEK 7 600'),
                   ('Allmänna villkor', 'Kund- eller leverantörsvillkor enligt engelsk rätt', 'från SEK 8 300'),
                   ('Skräddarsytt affärsavtal', 'Upprättat utifrån era kommersiella villkor', 'från SEK 16 000')]),
        dict(kicker='Obetalda fakturor i England', h2='När ett brittiskt bolag inte betalar.',
             sub=('Vi driver in företagsfordringar mot bolag i England och Wales: med ett formellt kravbrev före rättegång (letter before action), korrespondensen och förlikningsförhandlingen. '
                  'Om en domstolsprocess blir nödvändig säger vi det i förväg och lämnar över den förberedda akten till en anlitad barrister.'),
             rows=[('Kravbrev till ett brittiskt bolag', 'Formellt betalningskrav för en företagsfordran mot ett bolag i England och Wales', 'från SEK 7 600')]),
        dict(kicker='UK GDPR', h2='Kunder i Storbritannien men inget etableringsställe där?',
             sub=('Den som utan etablering i Storbritannien erbjuder varor eller tjänster till personer där, eller övervakar deras beteende, kan enligt artikel 27 i UK GDPR '
                  'behöva utse en skriftlig företrädare i Storbritannien. Vi bedömer det skriftligt och sköter vid behov företrädarskapet och de brittiska dataskyddshandlingarna.'),
             rows=[('UK GDPR och webbpaket', 'Integritetspolicy, cookiesamtycke, villkor och register över behandling för den brittiska marknaden', 'från EUR 695'),
                   ('Företrädare i Storbritannien (per år)', 'Fast årspris, offereras skriftligt i förväg', 'Skriftlig offert')])],
    how=dict(kicker='Så går det till', h2='Allt sker skriftligt.', steps=[
        ('1. Skicka förfrågan', 'Skicka ert namn och era kontaktuppgifter via formuläret ovan.'),
        ('2. Få ett fast pris', 'Omfattning och fast pris får ni skriftligt via E-post. Offerten gäller i 30 dagar.'),
        ('3. Betalning och start', 'Vi börjar efter betalning med kort, Apple Pay, Google Pay eller banköverföring.')]),
    scope=('Denna sida gäller engelsk rätt och det brittiska varumärkesförfarandet. Vi ger inte råd om svensk rätt eller EU-rätt. '
           'Vi företräder inte själva klienter i domstol; om det blir nödvändigt säger vi det i förväg och lämnar över till en anlitad barrister.'),
    company=('Western Legal Corporation Limited (registrerat i England och Wales, bolagsnummer 10453250, säte 19 The Circle, Queen Elizabeth Street, London SE1 2JE). '
             'Arbetet utförs av Santosh Pandey, solicitor (England och Wales), SRA-nummer 641612. Western Legal Corporation Limited är inte självt auktoriserat av Solicitors Regulation Authority; '
             'tillsynen gäller solicitorn personligen.'),
    imp=dict(h='Uppgifter om tjänsteleverantören', rows=[
        ('Leverantör', 'Western Legal Corporation Limited, 19 The Circle, Queen Elizabeth Street, London SE1 2JE, Storbritannien'),
        ('Bolagsform och register', 'Private company limited by shares, registrerat hos Companies House (England och Wales) under nummer 10453250'),
        ('Företrädare', 'Santosh Pandey, Director'),
        ('Kontakt', f'{MAIL}, WhatsApp +44 7822 014 066'),
        ('Yrkestitel', 'Solicitor (England och Wales), utfärdad i Storbritannien, SRA-nummer 641612'),
        ('Tillsynsmyndighet', SRA),
        ('Yrkesregler', RULES),
        ('Ansvarsförsäkring', 'Försäkringsbelopp £2,000,000 per skada'),
        ('Moms', 'Ingen moms debiteras.')]),
)

FI = dict(
    lang='fi', slug='fi', desk='nordics', area='FI', locale='fi_FI', cur='EUR', crumb='Suomi', alts=[],
    title='Tavaramerkki Britanniaan ja Englannin laki | Kiinteä hinta',
    desc='Brittiläinen tavaramerkkihakemus, Englannin lain mukaiset sopimukset ja perintä brittiyhtiöiltä. Solicitor (Englanti ja Wales), kiinteät hinnat euroina.',
    matter='Finland desk enquiry (fi)', thead=['Palvelu', 'Sisältö', 'Hinta'],
    confirm='Kiinteä hintanne vahvistetaan kirjallisesti, kun olemme nähneet asiakirjanne. Jos maksatte 24 tunnin kuluessa vahvistuksesta, saatte alennetun hinnan.',
    novat='ei arvonlisäveroa', brandsmall='Solicitor (Englanti ja Wales) · Lontoo', navbtn='Pyydä kiinteä hinta', navbtn_s='Tarjous',
    eyebrow='Suomalaisille yrityksille, jotka toimivat Isossa-Britanniassa',
    h1l='Tavaramerkkinne Isossa-Britanniassa, Englannin lain mukaiset sopimukset ja maksamattomat laskut Englannissa. Kiinteä hinta sovitaan kirjallisesti ennen työn aloittamista.',
    h1s='Englannin lakia kiinteään hintaan.',
    lede='Santosh Pandey, solicitor (Englanti ja Wales), hoitaa asianne Englannin lain mukaan. Kaikki hinnat ovat kiinteitä hintoja euroina, ilman arvonlisäveroa.',
    note='Kysymykset, asiakirjat ja kirjallinen neuvonta suomeksi. Englanninkielinen versio on ratkaiseva.',
    form=dict(fee='Kiinteä hinta · ei arvonlisäveroa · euroina', proof='Solicitor (Englanti ja Wales) · SRA 641612',
              name='Nimenne (yritys)', contact='Sähköposti tai WhatsApp-numero', has='Mitä teillä on?',
              opts=[('Contract to sign', 'Allekirjoitettava sopimus'), ('Notice or letter received', 'Saatu kirje tai vaatimus'),
                    ('Heads of terms', 'Heads of terms tai aiesopimus'), ('Draft lease', 'Vuokrasopimuksen luonnos Englannissa'), ('Nothing yet', 'Ei vielä mitään')],
              by='Allekirjoituksen tai vastauksen määräpäivä', btn='Pyydä kiinteä hinta',
              micro='Vastaamme tunnin sisällä Britannian toimistoaikana.', wa='Mieluummin WhatsApp?', wa_link='Kirjoittakaa tästä'),
    img_alt='Lontoon City',
    ids=['trademark', 'contracts', 'debt', 'gdpr'],
    sections=[
        dict(kicker='Brittiläinen tavaramerkki', h2='Suojatkaa tavaramerkkinne Isossa-Britanniassa.',
             sub=('EU-tavaramerkki, joka on rekisteröity 1. tammikuuta 2021 jälkeen, ei ole voimassa Isossa-Britanniassa. Britannian markkinoille tarvitaan oma hakemus Britannian tavaramerkkivirastoon (UKIPO) '
                  'ja tiedoksiantoosoite Isossa-Britanniassa, Gibraltarilla tai Kanaalisaarilla. Hoidamme molemmat: haun, tavara- ja palveluluettelon, hakemuksen 48 tunnin kuluessa ja tavanomaiset vastaukset menettelyssä.'),
             rows=[('Brittiläinen tavaramerkki, yksi luokka', 'Hakemus UKIPO:lle 48 tunnin kuluessa toimeksiannosta, brittiläisellä tiedoksiantoosoitteella', 'alkaen 645 EUR'),
                   ('Jokainen lisäluokka', 'Lisätään hakemukseen', '285 EUR'),
                   ('Puolustus väitemenettelyssä', 'TM8 ja näyttökierrokset, kiinteä hinta koko puolustukselle', '1 405 EUR')]),
        dict(kicker='Englannin lain mukaiset sopimukset', h2='Sopimukset brittiläisten kumppanien kanssa tarkastettuna ja laadittuna.',
             sub=('Tarkastamme sopimukset, joita brittiläiset asiakkaat, toimittajat tai kumppanit teille esittävät, ja annamme kirjallisen riskiraportin ja muutosehdotukset, '
                  'tai laadimme sopimuksen ehtojenne pohjalta. Kyse on aina sopimuksesta, johon sovelletaan Englannin lakia.'),
             rows=[('Salassapitosopimus (NDA)', 'Laadittu tai tarkastettu Englannin lain mukaan', 'alkaen 285 EUR'),
                   ('Sopimuksen tarkastus ja muutokset', 'Jakelu-, toimitus-, lisenssi-, SaaS- tai palvelusopimukset kirjallisella riskiraportilla', 'alkaen 695 EUR'),
                   ('Yleiset sopimusehdot', 'Asiakas- tai toimittajaehdot Englannin lain mukaan', 'alkaen 760 EUR'),
                   ('Räätälöity kauppasopimus', 'Laadittu kaupallisten ehtojenne pohjalta', 'alkaen 1 460 EUR')]),
        dict(kicker='Maksamattomat laskut Englannissa', h2='Kun brittiläinen yhtiö ei maksa.',
             sub=('Perimme yritysten saatavia Englannin ja Walesin yhtiöiltä: muodollisella maksuvaatimuksella ennen oikeudenkäyntiä (letter before action), kirjeenvaihdolla ja sovintoneuvotteluilla. '
                  'Jos oikeudenkäynti tulee tarpeelliseksi, kerromme sen etukäteen ja luovutamme valmistellun aineiston toimeksiannetulle barristerille.'),
             rows=[('Maksuvaatimus brittiläiselle yhtiölle', 'Muodollinen maksuvaatimus yrityssaatavasta Englannin ja Walesin yhtiöltä', 'alkaen 695 EUR')]),
        dict(kicker='UK GDPR', h2='Asiakkaita Isossa-Britanniassa, mutta ei toimipaikkaa siellä?',
             sub=('Jos tarjoatte ilman toimipaikkaa Isossa-Britanniassa tavaroita tai palveluja siellä oleville henkilöille tai seuraatte heidän käyttäytymistään, teidän on ehkä nimettävä UK GDPR:n 27 artiklan mukaan '
                  'kirjallisesti edustaja Isoon-Britanniaan. Arvioimme asian kirjallisesti ja hoidamme tarvittaessa edustuksen ja brittiläiset tietosuojan asiakirjat.'),
             rows=[('UK GDPR ja verkkosivupaketti', 'Tietosuojaseloste, evästesuostumus, ehdot ja käsittelyseloste Britannian markkinoille', 'alkaen 695 EUR'),
                   ('Edustaja Isossa-Britanniassa (vuosittain)', 'Kiinteä vuosihinta, tarjous kirjallisesti etukäteen', 'Kirjallinen tarjous')])],
    how=dict(kicker='Näin se toimii', h2='Kaikki kirjallisesti.', steps=[
        ('1. Lähettäkää pyyntö', 'Lähettäkää nimenne ja yhteystietonne yllä olevalla lomakkeella.'),
        ('2. Saatte kiinteän hinnan', 'Laajuuden ja kiinteän hinnan saatte kirjallisesti sähköpostilla. Tarjous on voimassa 30 päivää.'),
        ('3. Maksu ja aloitus', 'Aloitamme, kun maksu on suoritettu kortilla, Apple Paylla, Google Paylla tai pankkisiirrolla.')]),
    scope=('Tämä sivu koskee Englannin lakia ja Britannian tavaramerkkimenettelyä. Emme neuvo Suomen lainsäädännöstä emmekä EU-oikeudesta. '
           'Emme itse edusta asiakkaita tuomioistuimessa; jos se tulee tarpeelliseksi, kerromme sen etukäteen ja luovutamme asian toimeksiannetulle barristerille.'),
    company=('Western Legal Corporation Limited (rekisteröity Englannissa ja Walesissa, yritysnumero 10453250, kotipaikka 19 The Circle, Queen Elizabeth Street, London SE1 2JE). '
             'Työn tekee Santosh Pandey, solicitor (Englanti ja Wales), SRA-numero 641612. Western Legal Corporation Limited ei itse ole Solicitors Regulation Authorityn hyväksymä; '
             'valvonta koskee solicitoria henkilökohtaisesti.'),
    imp=dict(h='Tietoa palveluntarjoajasta', rows=[
        ('Palveluntarjoaja', 'Western Legal Corporation Limited, 19 The Circle, Queen Elizabeth Street, London SE1 2JE, Iso-Britannia'),
        ('Yhtiömuoto ja rekisteri', 'Private company limited by shares, rekisteröity Companies Houseen (Englanti ja Wales) numerolla 10453250'),
        ('Edustaja', 'Santosh Pandey, Director'),
        ('Yhteystiedot', f'{MAIL}, WhatsApp +44 7822 014 066'),
        ('Ammattinimike', 'Solicitor (Englanti ja Wales), myönnetty Isossa-Britanniassa, SRA-numero 641612'),
        ('Valvova viranomainen', SRA),
        ('Ammattisäännöt', RULES),
        ('Vastuuvakuutus', 'Vakuutusmäärä £2,000,000 vahinkoa kohden'),
        ('Arvonlisävero', 'Arvonlisäveroa ei veloiteta.')]),
)

PAGES = [DE, CH, NL, SV, FI]

if __name__ == '__main__':
    for P in PAGES:
        build(P)
        print('built', P['slug'] + '.html')
