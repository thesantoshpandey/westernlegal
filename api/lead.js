// Lead intake: emails enquiry via Resend with full ad attribution.
// Falls back client-side to FormSubmit/WhatsApp if this returns non-200.
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  try {
    const d = req.body || {};
    const key = process.env.RESEND_API_KEY;
    if (!key) return res.status(500).json({ ok: false, error: 'no key' });
    const esc = (s) => String(s || '').replace(/</g, '&lt;');
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
        reply_to: d.email || undefined,
        subject: `New enquiry — ${d.matter || 'General'} — ${d.name || ''}${adSourced}`,
        html
      })
    });
    if (!r.ok) return res.status(502).json({ ok: false });
    return res.status(200).json({ ok: true });
  } catch (e) { return res.status(500).json({ ok: false }); }
};
