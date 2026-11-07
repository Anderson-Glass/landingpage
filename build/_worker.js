// Anderson Glass & Glazing — Pages advanced-mode worker
// Serves the static site and handles POST /api/enquiry.
// Enquiries go to Resend when RESEND_API_KEY is set; otherwise the client is told to
// fall back to a pre-filled mail composer so no lead is ever lost.

const MAX = { name: 120, phone: 40, email: 160, suburb: 120, service: 80, message: 4000 };

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

function clean(value, key) {
  return typeof value === "string" ? value.trim().slice(0, MAX[key] || 500) : "";
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function handleEnquiry(request, env) {

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "bad_json" }, 400);
  }

  // honeypot: real users never fill this
  if (clean(body.company_website, "name")) return json({ ok: true });

  const name = clean(body.name, "name");
  const phone = clean(body.phone, "phone");
  const email = clean(body.email, "email");
  const suburb = clean(body.suburb, "suburb");
  const service = clean(body.service, "service");
  const message = clean(body.message, "message");
  const page = clean(body.page, "suburb");

  if (!name || !phone) return json({ ok: false, error: "missing_fields" }, 422);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: "bad_email" }, 422);

  const apiKey = env.RESEND_API_KEY;
  if (!apiKey) {
    // Not configured yet: let the client fall back to the mail composer.
    return json({ ok: false, fallback: "mailto", reason: "not_configured" }, 503);
  }

  const to = env.ENQUIRY_TO || "ben@andersonglass.com.au";
  const from = env.ENQUIRY_FROM || "Anderson Glass Website <quotes@andersonglass.com.au>";
  const subject = `Website enquiry — ${service || "General"}${suburb ? " — " + suburb : ""}`;

  const lines = [
    `Name:      ${name}`,
    `Phone:     ${phone}`,
    email ? `Email:     ${email}` : "",
    suburb ? `Suburb:    ${suburb}` : "",
    `Service:   ${service}`,
    page ? `Sent from: ${page}` : "",
    "",
    message || "(no message)",
  ].filter(Boolean);

  const html = `<h2 style="font-family:sans-serif">Website enquiry</h2>
<table style="font-family:system-ui,sans-serif;font-size:15px;line-height:1.5">
<tr><td><b>Name</b></td><td>${escapeHtml(name)}</td></tr>
<tr><td><b>Phone</b></td><td>${escapeHtml(phone)}</td></tr>
${email ? `<tr><td><b>Email</b></td><td>${escapeHtml(email)}</td></tr>` : ""}
${suburb ? `<tr><td><b>Suburb</b></td><td>${escapeHtml(suburb)}</td></tr>` : ""}
<tr><td><b>Service</b></td><td>${escapeHtml(service)}</td></tr>
${page ? `<tr><td><b>Page</b></td><td>${escapeHtml(page)}</td></tr>` : ""}
</table>
<pre style="font-family:ui-monospace,monospace;white-space:pre-wrap;font-size:14px">${escapeHtml(message || "(no message)")}</pre>`;

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { authorization: `Bearer ${apiKey}`, "content-type": "application/json" },
      body: JSON.stringify({
        from,
        to: [to],
        subject,
        text: lines.join("\n"),
        html,
        ...(email ? { reply_to: email } : {}),
      }),
    });

    if (!res.ok) {
      const detail = await res.text();
      console.error("resend_failed", res.status, detail.slice(0, 500));
      return json({ ok: false, fallback: "mailto", reason: "provider_error" }, 502);
    }
    const data = await res.json().catch(() => ({}));
    return json({ ok: true, id: data.id || null });
  } catch (err) {
    console.error("resend_exception", String(err).slice(0, 300));
    return json({ ok: false, fallback: "mailto", reason: "network" }, 502);
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/api/enquiry" || url.pathname === "/api/enquiry/") {
      if (request.method === "POST") return handleEnquiry(request, env);
      return json({ ok: false, error: "method_not_allowed" }, 405);
    }

    if (url.pathname.startsWith("/api/")) {
      return json({ ok: false, error: "not_found" }, 404);
    }

    // everything else is a static asset
    return env.ASSETS.fetch(request);
  },
};
