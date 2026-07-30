/* Western Legal shared JS */
(function () {
  // Clock: London
  function tick() {
    var f = function (tz) {
      try {
        return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: tz }).format(new Date());
      } catch (e) { return ''; }
    };
    var l = document.getElementById('clock-ldn');
    if (l) l.textContent = f('Europe/London');
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
  var ATTR_FIELDS = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'landing_page', 'first_seen'];
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
      fetch('https://formsubmit.co/ajax/trademark@westernlegal.co.uk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          _subject: 'New enquiry - ' + (data.matter || 'General') + ' - ' + (data.name || ''),
          name: data.name, email: data.email, phone: data.phone,
          matter: data.matter, message: data.message,
          page: data.page, referrer: data.referrer,
          gclid: data.gclid, gbraid: data.gbraid, wbraid: data.wbraid,
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
