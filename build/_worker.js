// Anderson Glass & Glazing — Pages advanced-mode worker
// Serves the static site and handles POST /api/enquiry.
// Enquiries go to Resend when RESEND_API_KEY is set; otherwise the client is told to
// fall back to a pre-filled mail composer so no lead is ever lost.
//
// Accepts JSON or multipart/form-data (with up to 4 photos).

const MAX = { name: 120, phone: 40, email: 160, suburb: 120, service: 80, message: 4000 };

// Upload contract — mirrored in assets/site2.js so the browser can fail fast.
const UPLOAD = {
  files: 4,
  perFile: 2 * 1024 * 1024,   // 2 MiB each
  total: 8 * 1024 * 1024,     // 8 MiB combined
  types: ["image/jpeg", "image/png", "image/webp"],
};

const RATE = { window: 10 * 60 * 1000, max: 5 };
const hits = new Map(); // isolate-local best effort; resets when the isolate recycles

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
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Identify an image by its first bytes rather than trusting the declared type.
function sniff(u8) {
  if (u8.length > 3 && u8[0] === 0xff && u8[1] === 0xd8 && u8[2] === 0xff) return "image/jpeg";
  if (u8.length > 8 && u8[0] === 0x89 && u8[1] === 0x50 && u8[2] === 0x4e && u8[3] === 0x47) return "image/png";
  if (u8.length > 12 && u8[0] === 0x52 && u8[1] === 0x49 && u8[2] === 0x46 && u8[3] === 0x46 &&
      u8[8] === 0x57 && u8[9] === 0x45 && u8[10] === 0x42 && u8[11] === 0x50) return "image/webp";
  return null;
}

function toBase64(u8) {
  let bin = "";
  const chunk = 0x8000;
  for (let i = 0; i < u8.length; i += chunk) {
    bin += String.fromCharCode.apply(null, u8.subarray(i, i + chunk));
  }
  return btoa(bin);
}

function safeName(name, mime) {
  const ext = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp" }[mime] || "jpg";
  const base = String(name || "photo").replace(/\.[^.]+$/, "").replace(/[^a-zA-Z0-9._-]/g, "-").slice(0, 40);
  return (base || "photo") + "." + ext;
}

function rateLimited(ip) {
  const now = Date.now();
  const rec = hits.get(ip);
  if (!rec || now > rec.resetAt) {
    hits.set(ip, { count: 1, resetAt: now + RATE.window });
    if (hits.size > 5000) for (const [k, v] of hits) if (now > v.resetAt) hits.delete(k);
    return false;
  }
  rec.count += 1;
  return rec.count > RATE.max;
}

async function parseBody(request) {
  const ct = (request.headers.get("content-type") || "").toLowerCase();
  const fields = {};
  const files = [];

  if (ct.includes("multipart/form-data")) {
    let fd;
    try {
      fd = await request.formData();
    } catch {
      return { error: "bad_form" };
    }
    for (const [k, v] of fd.entries()) {
      if (typeof v === "string") fields[k] = v;
      else if (v && typeof v.size === "number" && v.size > 0) files.push(v);
    }
  } else {
    let body;
    try {
      body = await request.json();
    } catch {
      return { error: "bad_json" };
    }
    Object.assign(fields, body || {});
  }
  return { fields, files };
}

async function handleEnquiry(request, env) {
  const ip = request.headers.get("cf-connecting-ip") || request.headers.get("x-forwarded-for") || "unknown";
  if (rateLimited(ip)) return json({ ok: false, error: "rate_limited" }, 429);

  // hard cap before doing any work
  const declared = Number(request.headers.get("content-length") || 0);
  if (declared > UPLOAD.total + 512 * 1024) return json({ ok: false, error: "too_large" }, 413);

  const parsed = await parseBody(request);
  if (parsed.error) return json({ ok: false, error: parsed.error }, 400);
  const { fields, files } = parsed;

  // honeypot: real users never fill this
  if (clean(fields.company_website, "name")) return json({ ok: true });

  const name = clean(fields.name, "name");
  const phone = clean(fields.phone, "phone");
  const email = clean(fields.email, "email");
  const suburb = clean(fields.suburb, "suburb");
  const service = clean(fields.service, "service");
  const message = clean(fields.message, "message");
  const page = clean(fields.page, "suburb");

  if (!name || !phone) return json({ ok: false, error: "missing_fields" }, 422);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: "bad_email" }, 422);

  // ---- photos -------------------------------------------------------------
  if (files.length > UPLOAD.files) return json({ ok: false, error: "too_many_photos" }, 413);

  let totalBytes = 0;
  const attachments = [];
  for (const f of files) {
    if (f.size > UPLOAD.perFile) return json({ ok: false, error: "photo_too_large" }, 413);
    totalBytes += f.size;
    if (totalBytes > UPLOAD.total) return json({ ok: false, error: "photos_too_large" }, 413);

    const buf = new Uint8Array(await f.arrayBuffer());
    const mime = sniff(buf);
    if (!mime || !UPLOAD.types.includes(mime)) {
      return json({ ok: false, error: "unsupported_photo_type" }, 415);
    }
    attachments.push({ filename: safeName(f.name, mime), content: toBase64(buf) });
  }

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
    attachments.length ? `Photos:    ${attachments.length} attached (${Math.round(totalBytes / 1024)} KB)` : "",
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
${attachments.length ? `<tr><td><b>Photos</b></td><td>${attachments.length} attached</td></tr>` : ""}
</table>
<pre style="font-family:ui-monospace,monospace;white-space:pre-wrap;font-size:14px">${escapeHtml(message || "(no message)")}</pre>`;

  const payload = {
    from,
    to: [to],
    subject,
    text: lines.join("\n"),
    html,
    ...(email ? { reply_to: email } : {}),
    ...(attachments.length ? { attachments } : {}),
  };

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { authorization: "Bearer " + apiKey, "content-type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const detail = await res.text();
      console.error("resend_failed", res.status, detail.slice(0, 500));
      return json({ ok: false, fallback: "mailto", reason: "provider_error" }, 502);
    }
    const data = await res.json().catch(() => ({}));
    return json({ ok: true, id: data.id || null, photos: attachments.length });
  } catch (err) {
    console.error("resend_exception", String(err).slice(0, 300));
    return json({ ok: false, fallback: "mailto", reason: "network" }, 502);
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // one canonical host: www -> apex
    if (url.hostname.startsWith("www.")) {
      return Response.redirect(`https://${url.hostname.slice(4)}${url.pathname}${url.search}`, 301);
    }

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
