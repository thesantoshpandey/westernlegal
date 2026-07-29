// Lead intake: emails enquiry via Resend. Falls back client-side to FormSubmit/WhatsApp if this returns non-200.
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  try {
    const d = req.body || {};
    const key = process.env.RESEND_API_KEY;
    if (!key) return res.status(500).json({ ok: false, error: 'no key' });
    const esc = (s) => String(s || '').replace(/</g, '&lt;');
    const html = `<h2>New enquiry — westernlegal.co.uk</h2>
      <p><b>Matter:</b> ${esc(d.matter)}<br><b>Name:</b> ${esc(d.name)}<br>
      <b>Email:</b> ${esc(d.email)}<br><b>Phone:</b> ${esc(d.phone)}</p>
      <p>${esc(d.message)}</p><hr>
      <p style="color:#888;font-size:12px">Page: ${esc(d.page)} · Referrer: ${esc(d.referrer)}<br>
      UTM: ${esc(d.utm_source)} / ${esc(d.utm_medium)} / ${esc(d.utm_campaign)} / ${esc(d.utm_term)}<br>GCLID: ${esc(d.gclid)}</p>`;
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Western Legal <leads@westernlegal.co.uk>',
        to: ['trademark@westernlegal.co.uk'],
        reply_to: d.email || undefined,
        subject: `New enquiry — ${d.matter || 'General'} — ${d.name || ''}`,
        html
      })
    });
    if (!r.ok) return res.status(502).json({ ok: false });
    return res.status(200).json({ ok: true });
  } catch (e) { return res.status(500).json({ ok: false }); }
};
