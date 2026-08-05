// Lead intake: emails enquiry via Resend with full ad attribution.
// Falls back client-side to FormSubmit/WhatsApp if this returns non-200.
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  try {
    const d = req.body || {};
    // honeypot: real users never see or fill this field
    if (d.website || d.company_url) return res.status(200).json({ ok: true });
    if (!d.name || (!d.email && !d.phone)) return res.status(400).json({ ok: false, error: 'name and email or phone required' });
    // field caps: reject oversized payloads used for spam and abuse
    const cap = (v, n) => String(v || '').slice(0, n);
    const tooLong = ['name','email','phone','matter'].some(k => String(d[k] || '').length > 200) || String(d.message || '').length > 5000;
    if (tooLong) return res.status(400).json({ ok: false, error: 'field too long' });
    const emailOk = !d.email || /^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(String(d.email).trim());
    if (!emailOk) return res.status(400).json({ ok: false, error: 'invalid email' });
    ['name','email','phone','matter'].forEach(k => { if (d[k]) d[k] = cap(d[k], 200); });
    if (d.message) d.message = cap(d.message, 5000);
    const key = process.env.RESEND_API_KEY;
    if (!key) return res.status(500).json({ ok: false, error: 'no key' });
    const esc = (s) => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    const row = (k, v) => `<tr><td style="padding:4px 12px 4px 0;color:#55677E;vertical-align:top;white-space:nowrap">${k}</td><td style="padding:4px 0">${esc(v)}</td></tr>`;
    const attribution = [
      row('page', d.page), row('referrer', d.referrer),
      row('gclid', d.gclid), row('gbraid', d.gbraid), row('wbraid', d.wbraid),
      row('utm_source', d.utm_source), row('utm_medium', d.utm_medium),
      row('utm_campaign', d.utm_campaign), row('utm_term', d.utm_term), row('utm_content', d.utm_content),
      row('landing_page', d.landing_page), row('first_seen', d.first_seen),
      row('ts', new Date().toISOString())
    ].join('');
    const adSourced = (d.gclid || d.gbraid || d.wbraid) ? ' [AD CLICK]' : '';
    const html = `<h2 style="color:#13294B">New enquiry — westernlegal.co.uk${adSourced}</h2>
      <table style="font-size:14px">
      ${row('name', d.name)}${row('email', d.email)}${row('phone', d.phone)}${row('matter', d.matter)}
      </table>
      <p style="white-space:pre-wrap">${esc(d.message)}</p><hr>
      <table style="font-size:12px;color:#888">${attribution}</table>`;
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Western Legal Website <leads@westernlegal.co.uk>',
        to: ['trademark@westernlegal.co.uk'],
        reply_to: (emailOk && d.email) ? String(d.email).trim() : undefined,
        subject: `New enquiry: ${String(d.matter || 'General').replace(/[\r\n]/g, ' ')} - ${String(d.name || '').replace(/[\r\n]/g, ' ')}${adSourced}`,
        html
      })
    });
    if (!r.ok) return res.status(502).json({ ok: false });
    return res.status(200).json({ ok: true });
  } catch (e) { return res.status(500).json({ ok: false }); }
};
