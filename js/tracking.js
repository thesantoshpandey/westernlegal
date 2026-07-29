/* WL attribution: captures ad/click params on landing, persists 90 days (first-touch),
   injects hidden fields into every form so /api/lead receives attribution. */
(function () {
  var KEY = 'wl_attr', DAYS = 90;
  var FIELDS = ['gclid','gbraid','wbraid','utm_source','utm_medium','utm_campaign','utm_term','utm_content'];
  function now() { return Date.now(); }
  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (v && v.ts && (now() - v.ts) < DAYS * 864e5) return v; } catch (e) {}
    return null;
  }
  function capture() {
    var q = new URLSearchParams(location.search), found = false, d = {};
    FIELDS.forEach(function (f) { var v = q.get(f); if (v) { d[f] = v; found = true; } });
    if (!found) return read();
    var existing = read();
    if (existing) return existing; /* first-touch wins within 90 days */
    d.ts = now(); d.landing = location.pathname; d.ref = document.referrer || '';
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {}
    return d;
  }
  function inject() {
    var a = capture() || {};
    var fields = {
      utm_source: a.utm_source || '', utm_medium: a.utm_medium || '',
      utm_campaign: a.utm_campaign || '', utm_term: a.utm_term || '',
      gclid: a.gclid || a.gbraid || a.wbraid || '',
      page: location.pathname, referrer: a.ref || document.referrer || ''
    };
    Array.prototype.forEach.call(document.forms, function (form) {
      Object.keys(fields).forEach(function (name) {
        if (!fields[name]) return;
        if (form.querySelector('[name="' + name + '"]')) return; /* don't duplicate */
        var i = document.createElement('input');
        i.type = 'hidden'; i.name = name; i.value = fields[name];
        form.appendChild(i);
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject);
  else inject();
})();
