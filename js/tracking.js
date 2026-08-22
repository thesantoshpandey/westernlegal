/* Western Legal - ad attribution & click conversions (adapted for this site)
   Form-submit conversion is NOT fired here: wl.js fires it success-only
   (AW-17980143249/_293CM3WqaIcEJHtzP1C). This file: gclid/UTM capture (90d),
   hidden-field injection, WhatsApp/phone click conversions. */
(function () {
  'use strict';
  var CONFIG = {
    CONV_FORM_SUBMIT: '',            // intentionally empty - handled in wl.js on success
    CONV_PHONE_CLICK: 'AW-17980143249/vvkCCNLK7OUcEJHtzP1C',    // Phone click, Secondary/Observation
    CONV_WHATSAPP_CLICK: 'AW-17980143249/0WpDCNXK7OUcEJHtzP1C', // WhatsApp click, Secondary/Observation
    STORAGE_KEY: 'wl_attribution',
    TTL_DAYS: 90
  };
  var TRACKED_PARAMS = ['gclid','gbraid','wbraid','utm_source','utm_medium','utm_campaign','utm_term','utm_content'];
  function readStored(){try{var raw=localStorage.getItem(CONFIG.STORAGE_KEY);if(!raw)return null;var d=JSON.parse(raw);if(Date.now()-d.first_seen_ts>CONFIG.TTL_DAYS*864e5){localStorage.removeItem(CONFIG.STORAGE_KEY);return null;}return d;}catch(e){return null;}}
  function captureFromUrl(){var p=new URLSearchParams(window.location.search);var found={},has=false;TRACKED_PARAMS.forEach(function(k){var v=p.get(k);if(v){found[k]=v;has=true;}});if(!has)return;var ex=readStored()||{};var m=Object.assign({},ex,found);if(ex.gclid)m.gclid=ex.gclid;m.landing_page=ex.landing_page||(window.location.pathname+window.location.search);m.first_seen_ts=ex.first_seen_ts||Date.now();m.first_seen=ex.first_seen||new Date().toISOString();try{localStorage.setItem(CONFIG.STORAGE_KEY,JSON.stringify(m));}catch(e){}}
  var LEAD_FIELDS=['gclid','gbraid','wbraid','utm_source','utm_medium','utm_campaign','utm_term','utm_content','landing_page','first_seen'];
  function injectHiddenFields(){var d=readStored();if(!d)return;document.querySelectorAll('form').forEach(function(f){LEAD_FIELDS.forEach(function(n){if(!d[n])return;var i=f.querySelector('input[name="'+n+'"]');if(!i){i=document.createElement('input');i.type='hidden';i.name=n;f.appendChild(i);}i.value=d[n];});});}
  function fire(sendTo){if(typeof window.gtag!=='function')return;if(!sendTo||!/^AW-\d+\/(?=[A-Za-z0-9_-]*[a-z])[A-Za-z0-9_-]{8,}$/.test(sendTo))return;window.gtag('event','conversion',{send_to:sendTo});}
  function bind(){document.addEventListener('click',function(e){var a=e.target.closest?e.target.closest('a[href]'):null;if(!a)return;var h=a.getAttribute('href')||'';if(h.indexOf('tel:')===0){fire(CONFIG.CONV_PHONE_CLICK);}else if(/wa\.me|api\.whatsapp\.com|whatsapp:/.test(h)){fire(CONFIG.CONV_WHATSAPP_CLICK);}});}
  function init(){captureFromUrl();injectHiddenFields();bind();}
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);}else{init();}
  window.WL_getAttribution=readStored;
})();
