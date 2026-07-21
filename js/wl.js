/* Western Legal shared JS */
(function () {
  // Dual clocks: London / Delhi
  function tick() {
    var f = function (tz) {
      try {
        return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: tz }).format(new Date());
      } catch (e) { return ''; }
    };
    var l = document.getElementById('clock-ldn');
    var d = document.getElementById('clock-del');
    if (l) l.textContent = f('Europe/London');
    if (d) d.textContent = f('Asia/Kolkata');
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

  // Lead form: POST to /api/lead with UTM capture; fall back to WhatsApp on failure
  var form = document.querySelector('form.lead');
  if (!form) return;
  var params = new URLSearchParams(location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term'].forEach(function (k) {
    var el = form.querySelector('[name="' + k + '"]');
    if (el) el.value = params.get(k) || '';
  });
  var ref = form.querySelector('[name="referrer"]');
  if (ref) ref.value = document.referrer || '';
  var pg = form.querySelector('[name="page"]');
  if (pg) pg.value = location.pathname;

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
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
      window.location.href = 'https://wa.me/447915318920?text=' + msg.replace(/\n/g,'%0A');
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
          utm_source: data.utm_source, utm_medium: data.utm_medium,
          utm_campaign: data.utm_campaign, utm_term: data.utm_term
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