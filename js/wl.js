/* Western Legal shared JS */
(function () {
  // Clocks: the desks we work across
  function tick() {
    var f = function (tz) {
      try {
        return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: tz }).format(new Date());
      } catch (e) { return ''; }
    };
    var zones = {
      'ldn': 'Europe/London', 'zrh': 'Europe/Zurich', 'ams': 'Europe/Amsterdam',
      'dub': 'Europe/Dublin', 'sto': 'Europe/Stockholm', 'hel': 'Europe/Helsinki',
      'dxb': 'Asia/Dubai', 'nyc': 'America/New_York', 'lax': 'America/Los_Angeles'
    };
    Object.keys(zones).forEach(function (k) {
      var t = f(zones[k]);
      var a = document.getElementById('clk-' + k); if (a) a.textContent = t;
      var b = document.getElementById('clk2-' + k); if (b) b.textContent = t;
    });
  }
  tick(); setInterval(tick, 30000);

  // Scroll reveal (respects reduced motion via CSS)
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  // Lead form: POST to /api/lead. Fallbacks: FormSubmit, then WhatsApp.
  var form = document.querySelector('form.lead');
  if (!form) return;

  var ref = form.querySelector('[name="referrer"]');
  if (ref) ref.value = document.referrer || '';
  var pg = form.querySelector('[name="page"]');
  if (pg) pg.value = location.pathname;

  // Attribution: tracking.js owns capture (localStorage, first-touch, 90d).
  // Backfill from storage only - NEVER blank a field. This fixes the bug where
  // fields were overwritten with '' whenever the submit page URL had no UTMs.
  var ATTR_FIELDS = ['gclid', 'gbraid', 'wbraid', 'msclkid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'landing_page', 'first_seen'];
  function fillAttribution() {
    var att = (typeof window.WL_getAttribution === 'function' && window.WL_getAttribution()) || {};
    ATTR_FIELDS.forEach(function (k) {
      if (!att[k]) return;
      var el = form.querySelector('[name="' + k + '"]');
      if (!el) { el = document.createElement('input'); el.type = 'hidden'; el.name = k; form.appendChild(el); }
      if (!el.value) el.value = att[k];
    });
  }
  fillAttribution();

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    fillAttribution(); // re-check at submit time in case tracking.js stored after this ran
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true; btn.textContent = 'Sending…';
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    function success() {
      if (typeof gtag === 'function') { gtag('event', 'conversion', { send_to: 'AW-17980143249/_293CM3WqaIcEJHtzP1C' }); }
      window.uetq = window.uetq || []; window.uetq.push('event', 'submit', { event_category: 'form', event_label: (data.matter || 'General') });
      form.style.display = 'none';
      var ok = document.querySelector('.form-ok');
      if (ok) ok.style.display = 'block';
    }
    function whatsappFallback() {
      btn.disabled = false; btn.textContent = 'Send enquiry';
      var msg = 'New enquiry via westernlegal.co.uk%0A' + 'Matter: ' + (data.matter||'') + '%0AName: ' + (data.name||'') + '%0AEmail: ' + (data.email||'') + '%0APhone: ' + (data.phone||'') + '%0A' + (data.message||'');
      window.location.href = 'https://wa.me/447822014066?text=' + msg.replace(/\n/g,'%0A');
    }
    function formsubmitFallback() {
      fetch('https://formsubmit.co/ajax/intake@westernlegal.co.uk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          _subject: '[FALLBACK] New enquiry - ' + (data.matter || 'General') + ' - ' + (data.name || '') + (data.msclkid ? ' [BING CLICK]' : (data.gclid || data.gbraid || data.wbraid ? ' [AD CLICK]' : '')),
          name: data.name, email: data.email, phone: data.phone,
          matter: data.matter, message: data.message,
          page: data.page, referrer: data.referrer,
          gclid: data.gclid, gbraid: data.gbraid, wbraid: data.wbraid, msclkid: data.msclkid,
          utm_source: data.utm_source, utm_medium: data.utm_medium,
          utm_campaign: data.utm_campaign, utm_term: data.utm_term,
          utm_content: data.utm_content,
          landing_page: data.landing_page, first_seen: data.first_seen
        })
      }).then(function (r) { return r.json(); }).then(function (out) {
        if (!out || String(out.success) !== 'true') throw new Error('fs failed');
        success();
      }).catch(whatsappFallback);
    }
    // Primary: own endpoint (Resend, own-domain DKIM). Fallbacks: FormSubmit, then WhatsApp.
    fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error('api failed'); success(); })
      .catch(formsubmitFallback);
  });
})();

/* practice areas dropdown: tap to open on any narrow or touch device */
(function(){
  var d=document.querySelector('.navdrop'); if(!d) return;
  var t=d.querySelector('.navdrop-t'); if(!t) return;
  t.setAttribute('role','button'); t.setAttribute('aria-expanded','false');
  function narrow(){ return window.matchMedia('(max-width: 900px)').matches || window.matchMedia('(hover: none)').matches; }
  t.addEventListener('click',function(e){
    if(!narrow()) return;
    e.preventDefault(); e.stopPropagation();
    var hdr=document.querySelector('header.site');
    if(hdr) document.documentElement.style.setProperty('--droptop',Math.max(0,hdr.getBoundingClientRect().bottom)+8+'px');
    var open=d.classList.toggle('open');
    t.setAttribute('aria-expanded',open?'true':'false');
  });
  document.addEventListener('click',function(e){
    if(!d.contains(e.target)){ d.classList.remove('open'); t.setAttribute('aria-expanded','false'); }
  });
  d.querySelectorAll('.dropmenu a').forEach(function(a){
    a.addEventListener('click',function(){ d.classList.remove('open'); t.setAttribute('aria-expanded','false'); });
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){ d.classList.remove('open'); t.setAttribute('aria-expanded','false'); }
  });
  var startY=null;
  window.addEventListener('scroll',function(){
    if(!d.classList.contains('open')) return;
    if(window.matchMedia('(hover:hover) and (min-width:901px)').matches) return;
    if(startY===null){ startY=window.scrollY; return; }
    if(Math.abs(window.scrollY-startY)>220){ d.classList.remove('open'); t.setAttribute('aria-expanded','false'); startY=null; }
  },{passive:true});
})();

/* focusFirstField: clicking a quote CTA puts the cursor in the name box */
(function(){
  function go(){
    if(location.hash!=='#enquiry') return;
    var f=document.getElementById('enquiry'); if(!f) return;
    var first=f.querySelector('input[name="name"],input:not([type=hidden])');
    if(first) setTimeout(function(){ try{ first.focus({preventScroll:true}); }catch(e){ first.focus(); } },320);
  }
  window.addEventListener('hashchange',go);
  document.addEventListener('click',function(e){
    var a=e.target.closest && e.target.closest('a[href$="#enquiry"]');
    if(a) setTimeout(go,340);
  });
  go();
})();

/* HOVER INTENT: open on hover, close after a delay so cursor drift does not dismiss it */
(function(){
  var d=document.querySelector('.navdrop'); if(!d) return;
  var t=d.querySelector('.navdrop-t'); var m=d.querySelector('.dropmenu'); if(!m) return;
  var timer=null;
  function desktop(){ return window.matchMedia('(hover:hover) and (min-width:901px)').matches; }
  function open(){ if(!desktop()) return; clearTimeout(timer); d.classList.add('open'); if(t) t.setAttribute('aria-expanded','true'); }
  function close(){ if(!desktop()) return; clearTimeout(timer); timer=setTimeout(function(){ d.classList.remove('open'); if(t) t.setAttribute('aria-expanded','false'); },420); }
  [t,m,d].forEach(function(el){
    if(!el) return;
    el.addEventListener('mouseenter',open);
    el.addEventListener('mouseleave',close);
  });
})();
