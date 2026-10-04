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

  function close(el) { el.classList.remove('show'); document.body.classList.remove('consent-open'); document.documentElement.classList.remove('cpending'); setTimeout(function () { el.remove(); }, 220); }

  var LANG = (document.documentElement.lang || '').toLowerCase().slice(0, 2);
  var JA = LANG === 'ja', TR = LANG === 'tr';
  function banner() {
    var w = document.createElement('div');
    w.className = 'consent';
    w.setAttribute('role', 'dialog');
    w.setAttribute('aria-live', 'polite');
    w.setAttribute('aria-label', 'Cookie choices');
    w.innerHTML =
      '<div class="consent-in">' +
        '<div class="consent-copy">' +
          (JA ? '<b>クッキーについて</b>' : TR ? '<b>Çerezler</b>' : '<b>Cookies on this site</b>') +
          (TR ? '<p class="cc-long">Sitenin çalışması için gerekli çerezleri kullanırız. Onayınız olursa, sitenin nasıl bulunduğunu ve kullanıldığını anlamak için analiz ve reklam çerezlerini de kullanırız. Tercihinizi istediğiniz zaman değiştirebilirsiniz. Ayrıntılar için <a href="/privacy">gizlilik bildirimimize</a> (İngilizce) bakın.</p>' + '<p class="cc-short">Onayınızla analiz ve reklam çerezleri kullanırız. <a href="/privacy">Gizlilik bildirimi</a></p>' : '') +
          (JA ? '<p class="cc-long">本サイトの動作に必要なクッキーを使用します。ご同意いただいた場合に限り、サイトの利用状況を把握するための分析用・広告用クッキーも使用します。設定はいつでも変更できます。詳しくは<a href="/privacy">プライバシーポリシー</a>（英語）をご覧ください。</p>' +
                '<p class="cc-short">ご同意いただいた場合に限り、分析用・広告用クッキーを使用します。<a href="/privacy">プライバシーポリシー</a></p>' : '') +
          ((JA || TR) ? '' : '<p class="cc-long">We use essential cookies to make the site work. With your permission we also use analytics and advertising cookies to understand how the site is found and used. You can change your choice at any time. See our <a href="/privacy">privacy notice</a>.</p>' +
          '<p class="cc-short">We use analytics and advertising cookies with your permission. <a href="/privacy">Privacy notice</a></p>') +
        '</div>' +
        '<div class="consent-btns">' +
          '<button type="button" class="btn" data-c="accepted">' + (JA ? '同意する' : TR ? 'Kabul et' : 'Accept') + '</button>' +
          '<button type="button" class="btn ghost" data-c="essential">' + (JA ? '必須のみ' : TR ? 'Yalnızca zorunlu' : 'Essential only') + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(w);
    document.body.classList.add('consent-open');
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
    if (stored) { apply(stored); document.documentElement.classList.remove('cpending'); }
    else { banner(); }
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href="#cookie-settings"],a[data-cookie-settings]');
      if (!a) return;
      e.preventDefault();
      try { localStorage.removeItem(KEY); } catch (err) {}
      document.documentElement.classList.add('cpending');
      if (!document.querySelector('.consent')) banner();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
