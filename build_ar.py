#!/usr/bin/env python3
"""Build /ar, the Arabic desk for Gulf clients (27 Nov 2026). Run from the westernlegal repo root.
Uses build() from make_lang.py (the /de /nl /ja builder) with current asset versions, then makes the page RTL.
Every fee is an existing schedule row in prices.json (/commercial-lease-solicitor, /landlord-solicitor, /gulf), in GBP.
Gulf copy rules (16 Sep 2026): Solicitor of England and Wales in full, no consultant wording, no UAE address or
phone, GBP only, Saudi Arabia not solicited."""
import re
src = open('make_lang.py', encoding='utf-8').read()
exec(src[:src.find('# ---------------------------------------------------------------- content')])
V_CSS, V_WL, V_CONSENT, V_TRACK, MARK = '20261127a', '20261127b', '20261117a', '20261113a', 'WL-2026-11-27'
HEAD_TRACK = HEAD_TRACK.replace('consent.js?v=20261022a', 'consent.js?v=' + V_CONSENT).replace('tracking.js?v=20260917b', 'tracking.js?v=' + V_TRACK)
NEED['ar'] = ('ما الذي تحتاجونه؟ سطر واحد يكفي (اختياري)', 'ما الذي تحتاجونه (اختياري)')

SRA_ = 'Solicitors Regulation Authority, The Cube, 199 Wharfside Street, Birmingham B1 1RN'
RULES_ = '<a href="https://www.sra.org.uk/solicitors/standards-regulations/" target="_blank" rel="noopener">SRA Standards and Regulations</a>'
MAIL_ = '<a href="mailto:sp@westernlegal.co.uk">sp@westernlegal.co.uk</a>'
Q = 'يُحدَّد لكل قضية'
FROM = 'ابتداءً من '

AR = dict(
    lang='ar', slug='ar', desk='gulf', alts=[], locale='ar_AE', crumb='بالعربية', matter='Arabic desk enquiry',
    area=[{'@type': 'Country', 'name': n} for n in ('United Arab Emirates', 'Qatar', 'Kuwait', 'Bahrain', 'Oman')],
    title='محامٍ في إنجلترا وويلز لعملاء الخليج | Western Legal',
    desc='العقارات التجارية في إنجلترا وويلز، والشركات والعقود البريطانية، والنزاعات أمام محاكم المراكز المالية في الخليج. أتعاب ثابتة بالجنيه الإسترليني.',
    novat='دون ضريبة القيمة المضافة',
    brandsmall='لندن · لعملاء الخليج', navbtn='اطلبوا عرض أتعاب ثابت', navbtn_s='عرض أتعاب',
    eyebrow='للشركات والعائلات في الخليج',
    h1l='عقاراتكم وشركاتكم ونزاعاتكم في بريطانيا وأمام محاكم المراكز المالية، بأتعاب ثابتة.',
    h1s='محامٍ في لندن. أتعاب ثابتة.',
    lede=('نخدم الشركات والعائلات في الإمارات وقطر والكويت والبحرين وعُمان في عقاراتها التجارية في إنجلترا وويلز، '
          'وفي شركاتها وعقودها الخاضعة للقانون الإنجليزي، وفي نزاعاتها أمام محاكم المراكز المالية في الخليج. '
          'يتولى العمل محامٍ ذو خبرة، كتابةً، بأتعاب ثابتة تُحدَّد كتابةً قبل البدء.'),
    note='نستقبل استفساراتكم ومستنداتكم بالعربية، وتصدر المشورة والمستندات بالإنجليزية.',
    img_alt='مبانٍ في حي المال في لندن',
    form=dict(fee='أتعاب ثابتة بالجنيه الإسترليني · دون ضريبة القيمة المضافة',
              proof='Solicitor في إنجلترا وويلز · SRA 641612 · وفي أيرلندا · S28750',
              name='الاسم', contact='البريد الإلكتروني أو رقم واتساب', btn='احصلوا على عرض أتعاب ثابت',
              micro='نرد خلال ساعة في أوقات العمل.', wa='تفضّلون واتساب؟', wa_link='راسلونا', opts=[]),
    thead=('الخدمة', 'ما تشمله', 'الأتعاب'),
    confirm='تُحدَّد أتعابكم الثابتة كتابةً بعد الاطلاع على مستنداتكم. ادفعوا خلال 24 ساعة من هذا التأكيد لتحصلوا على الأتعاب المخفّضة.',
    ids=['property', 'companies', 'courts'],
    sections=[
        dict(kicker='العقارات التجارية في إنجلترا وويلز', h2='عقود الإيجار التجارية، للمالك والمستأجر.',
             sub=('للعائلات والشركات الخليجية التي تملك عقارات تجارية في إنجلترا وويلز أو تستأجرها: مراجعة العقود والتفاوض عليها وتجديدها. '
                  'حين يتطلب القانون صكاً رسمياً أو تسجيلاً في السجل العقاري، يتولاه محامٍ مرخّص نكلّفه.'),
             rows=[('مراجعة عقد الإيجار وتقرير المخاطر (للمالك أو المستأجر)', 'تعليقات كاملة على مسودة العقد وتقرير بلغة واضحة عن الإصلاح ومراجعة الأجرة وحق الإنهاء والتنازل والضمانات، مع التعديلات المقترحة.', FROM + '£750'),
                   ('الشروط الأولية للاتفاق (Heads of terms)، صياغة أو مراجعة', 'ضبط الصفقة التجارية قبل صياغة العقد، وهي أقل المراحل تكلفةً لكسب كل خلاف لاحق.', FROM + '£450'),
                   ('عقد إيجار جديد أو تجديد حتى الصيغة المتفق عليها', 'من الشروط الأولية إلى الصيغة النهائية المتفق عليها: المشورة والتفاوض مع الطرف الآخر، مع تكليف محامٍ مرخّص بإعداد الصك والتعامل مع السجل العقاري حيث يتطلب القانون ذلك.', FROM + '£1,450'),
                   ('التفاوض حتى الإتمام', 'إدارة الصفقة كاملة: التفاوض والصيغة المتفق عليها والإتمام، بالتنسيق مع المحامي المرخّص الذي يعد الصك ويتولى التسجيل.', FROM + '£2,450'),
                   ('إذن التنازل أو التأجير من الباطن أو التعديل', 'المشورة والتفاوض على شروط الموافقة مع المالك أو المستأجر حتى الصيغة المتفق عليها؛ وحين يكون الإذن صكاً يعده محامٍ مرخّص نكلّفه.', FROM + '£850'),
                   ('تقييم إشعار المادة 25 (قانون المالك والمستأجر لسنة 1954)', 'قراءة الإشعار والعقد، والتحقق من صحة الإشعار، وتحديد تاريخ الإنهاء والموعد النهائي أمام المحكمة، ورأي مكتوب في خياراتكم.', '£495'),
                   ('التجديد والإصلاحات المستحقة عند انتهاء الإيجار والإنهاء بسبب الإخلال', 'الجانب النزاعي من عقود الإيجار التجارية، يُسعَّر لكل حالة.', FROM + '£850')]),
        dict(kicker='الشركات والعقود البريطانية', h2='شركاتكم وعقودكم الخاضعة للقانون الإنجليزي.',
             sub='اتفاقيات المساهمين والمشاريع المشتركة، والعقود التجارية، وقرارات الشركات البريطانية، والمطالبة بالديون المستحقة على شركات في إنجلترا وويلز.',
             rows=[('اتفاقية المساهمين أو المشروع المشترك', 'أحكام السيطرة والتخارج والجمود ونقل الأسهم.', FROM + '£1,650'),
                   ('مراجعة العقود والتعليق عليها', 'عقود التوزيع والتوريد والوكالة والترخيص والخدمات، مع تقرير مكتوب بالمخاطر.', FROM + '£595'),
                   ('عقد تجاري معدّ خصيصاً', 'يُصاغ من شروطكم التجارية وفق القانون الإنجليزي.', FROM + '£1,250'),
                   ('قرارات مجلس الإدارة والمساهمين', 'محاضر مجلس الإدارة والقرارات المكتوبة وفق قانون الشركات البريطاني.', FROM + '£295'),
                   ('بند التحكيم واستراتيجية التنفيذ', 'صياغة بند تسوية النزاعات بحيث يكون الحكم قابلاً للتنفيذ حيث توجد الأصول.', FROM + '£570'),
                   ('إنذار ما قبل الدعوى لشركة بريطانية', 'مطالبة رسمية بدين تجاري مستحق على شركة في إنجلترا وويلز.', FROM + '£595')]),
        dict(kicker='محاكم المراكز المالية', h2='النزاعات أمام محاكم قطر ودبي وأبوظبي والبحرين.',
             sub=('<a href="/qfc-court">المحكمة المدنية والتجارية لمركز قطر للمال</a>، و<a href="/difc-courts">محاكم مركز دبي المالي العالمي</a>، '
                  'و<a href="/adgm-courts">محاكم سوق أبوظبي العالمي</a>، و<a href="/bahrain-commercial-court">محكمة البحرين التجارية الدولية</a>. '
                  'نتحقق أولاً من اختصاص المحكمة في رأي مكتوب، ونؤكد لكم كتابةً قبل التكليف من سيمثلكم في الجلسة وبموجب أي قيد.'),
             rows=[('مراجعة الدعوى ورأي مكتوب في فرص النجاح', 'قراءة مستنداتكم ورأي مكتوب في الاختصاص والموضوع والمواعيد والتكلفة المتوقعة لكل مرحلة، قبل رفع أي دعوى.', Q),
                   ('صحيفة الدعوى أو مذكرة الدفاع', 'تُصاغ من مستنداتكم ومن الدعوى المقامة عليكم.', Q),
                   ('طلب مستعجل', 'طلب واحد، كالأمر الوقتي أو ضمان التكاليف أو الإفصاح، مع الإفادة الداعمة.', Q),
                   ('تنفيذ حكم تحكيم', 'طلب الاعتراف بحكم تحكيم وتنفيذه أمام المحكمة المختصة.', Q),
                   ('يوم جلسة', 'التحضير والمرافعة ليوم جلسة واحد.', Q)]),
    ],
    how=dict(kicker='كيف نعمل', h2='ثلاث خطوات، كلها كتابةً.',
             steps=[('أرسلوا المستندات', 'العقد أو المسودة أو الرسالة التي وصلتكم، وأي موعد نهائي.'),
                    ('أتعاب ثابتة كتابةً', 'تُحدَّد الأتعاب وموعد التسليم كتابةً قبل بدء أي عمل.'),
                    ('التسليم', 'يصلكم العمل كتابةً في الموعد المحدد، دون أي إضافة لاحقة على الأتعاب.')]),
    scope=('نقدّم المشورة في القانون الإنجليزي، ونتولى العمل أمام محاكم المراكز المالية المذكورة أعلاه. لا نقدّم المشورة في قوانين الإمارات أو قطر أو الكويت أو البحرين أو عُمان خارج تلك المحاكم، '
           'وعند الحاجة إلى القانون المحلي نتعاون مع محامٍ مقيّد في الدولة المعنية ونخطركم قبل تكبّد أي تكلفة.'),
    company=('Western Legal Corporation Limited شركة مسجلة في إنجلترا وويلز برقم 10453250، ومقرها 19 The Circle, Queen Elizabeth Street, London SE1 2JE. '
             'الشركة ذاتها ليست مرخّصة من هيئة تنظيم المحامين، والتنظيم المهني شخصي للمحامي. ويُؤكَّد لكم كتابةً قبل التكليف تأمين المسؤولية المهنية الذي يغطي عملكم.'),
    imp=dict(h='المعلومات المهنية', rows=[('المحامي', 'سانتوش باندي'),
                                          ('الصفة في إنجلترا وويلز', 'Solicitor of England and Wales، رقم القيد SRA 641612'),
                                          ('الصفة في أيرلندا', 'Solicitor (Ireland)، Law Society of Ireland رقم S28750، مقيّد في سجل المحامين منذ 25 نوفمبر 2026، دون شهادة مزاولة أيرلندية حتى الآن'),
                                          ('الجهة التنظيمية', SRA_), ('القواعد المهنية', RULES_), ('البريد الإلكتروني', MAIL_)]),
)

CREDS = ('<section class="jsec" id="credentials"><div class="wrap"><span class="kicker">المؤهلات</span><h2>من يتولى عملكم.</h2><ul class="creds">'
         '<li><b>سانتوش باندي، محامٍ (Solicitor) في إنجلترا وويلز</b> رقم القيد لدى هيئة تنظيم المحامين SRA 641612.</li>'
         '<li><b>محامٍ (Solicitor) في أيرلندا</b> جمعية المحامين في أيرلندا (Law Society of Ireland) رقم S28750، مقيّد في سجل المحامين منذ 25 نوفمبر 2026، ولا يحمل بعد شهادة مزاولة أيرلندية.</li>'
         '<li><b>حق المثول أمام المحكمة المدنية والتجارية لمركز قطر للمال</b> بموجب المادة 30.1 من قواعد وإجراءات المحكمة، ما لم تقرر المحكمة خلاف ذلك.</li>'
         '</ul></div></section>\n')

RTL = """<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet"><style>
html[dir=rtl] body{font-family:'Montserrat','IBM Plex Sans Arabic',system-ui,sans-serif}
html[dir=rtl] *{letter-spacing:0!important}
html[dir=rtl] body.lx .hero h1,html[dir=rtl] body.lx h2{line-height:1.45}
html[dir=rtl] body.lx .lede,html[dir=rtl] body.lx p{line-height:1.85}
html[dir=rtl] body.lx .steps3 div{border-left:0;border-right:2px solid var(--gold);padding-left:0;padding-right:14px}
html[dir=rtl] th:last-child,html[dir=rtl] td.fee{text-align:left!important}
html[dir=rtl] .qqform input,html[dir=rtl] .qqform textarea{text-align:right}
html[dir=rtl] body.lx .creds{list-style:none;padding:0;margin:18px 0 0;max-width:70ch}
html[dir=rtl] body.lx .creds li{padding:12px 0;border-bottom:1px solid var(--rule)}
html[dir=rtl] body.lx .creds b{display:block;color:var(--ink)}
html[dir=rtl] footer.site{text-align:left}
</style>"""

ADV_OLD = 'Reserved legal activities and matters requiring court advocacy are conducted with instructed counsel.'
ADV_NEW = ('Reserved legal activities in England and Wales are conducted with instructed counsel. Who appears before a court named on this page, '
           'and on what basis, is confirmed in writing before you instruct.')

page = build(AR)
page = page.replace('<html lang="ar">', '<html lang="ar" dir="rtl">', 1)
page = page.replace('</head>', RTL + '</head>', 1)
page = page.replace('<footer class="site">', '<footer class="site" dir="ltr">', 1)
assert ADV_OLD in page; page = page.replace(ADV_OLD, ADV_NEW)
page = page.replace('autocomplete="name" aria-label', 'autocomplete="name" dir="auto" aria-label').replace('autocomplete="email" aria-label', 'autocomplete="email" dir="auto" aria-label')
page = page.replace('<textarea name="need"', '<textarea name="need" dir="auto"')
page = page.replace('&rarr;', '&larr;')
# the off screen honeypot (left:-9999px) widens an RTL page to 10,000px; hide it in place instead
HP_OLD = 'style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden"'
assert HP_OLD in page
page = page.replace(HP_OLD, 'style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap"')
i = page.find('</div></section>', page.find('<section class="hero">')) + len('</div></section>')
page = page[:i] + '\n' + CREDS + page[i:]
page = page.replace('<script src="/js/wl.js', '<script>window.WL_PAGE_EVENTS={prefix:"ar",labels:{form_submit:"",whatsapp_tap:""}};</script><script src="/js/wl.js', 1)
# keep the pound sign before the figure inside right to left text
b0 = page.find('<body'); f0 = page.find('<footer')
page = page[:b0] + re.sub(r'£[\d,]+', lambda m: '<span dir="ltr">' + m.group(0) + '</span>', page[b0:f0]) + page[f0:]
assert 'S28750' in page and 'dir="rtl"' in page
open('ar.html', 'w', encoding='utf-8').write(page)
print('ar.html', len(page))
