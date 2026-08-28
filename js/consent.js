/* Western Legal consent banner. Defaults are set inline in <head> before any tag loads.
   This file only renders the notice and applies the visitor's choice. */
(function () {
  var KEY = 'wl_consent';
  function read() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function write(v) { try { localStorage.setItem(KEY, v); localStorage.setItem(KEY + '_at', new Date().toISOString()); } catch (e) {} }

  function apply(state) {
    var g = state === 'accepted' ? 'granted' : 'denied';
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        ad_storage: g, analytics_storage: g, ad_user_data: g, ad_personalization: g
      });
    }
    window.uetq = window.uetq || [];
    window.uetq.push('consent', 'update', { ad_storage: g });
  }

  function close(el) { el.classList.remove('show'); setTimeout(function () { el.remove(); }, 220); }

  function banner() {
    var w = document.createElement('div');
    w.className = 'consent';
    w.setAttribute('role', 'dialog');
    w.setAttribute('aria-live', 'polite');
    w.setAttribute('aria-label', 'Cookie choices');
    w.innerHTML =
      '<div class="consent-in">' +
        '<div class="consent-copy">' +
          '<b>Cookies on this site</b>' +
          '<p>We use essential cookies to make the site work. With your permission we also use analytics and advertising cookies to understand how the site is found and used. You can change your choice at any time. See our <a href="/privacy">privacy notice</a>.</p>' +
        '</div>' +
        '<div class="consent-btns">' +
          '<button type="button" class="btn" data-c="accepted">Accept</button>' +
          '<button type="button" class="btn ghost" data-c="essential">Essential only</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(w);
    requestAnimationFrame(function () { w.classList.add('show'); });
    w.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-c]');
      if (!b) return;
      var choice = b.getAttribute('data-c');
      write(choice);
      apply(choice);
      close(w);
    });
  }

  function init() {
    var stored = read();
    if (stored) { apply(stored); }
    else { banner(); }
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href="#cookie-settings"],a[data-cookie-settings]');
      if (!a) return;
      e.preventDefault();
      try { localStorage.removeItem(KEY); } catch (err) {}
      if (!document.querySelector('.consent')) banner();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
