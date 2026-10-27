/**
 * Cloudflare Worker for yanhua.ai subscriptions.
 *
 * Browsers must not hold RESEND_API_KEY. Point data/config.js
 * subscribeEndpoint at this worker, then:
 *   wrangler secret put RESEND_API_KEY
 * Optional: SEND_WELCOME=1
 *
 * The General audience is the default, same id as
 * data/config.js resendAudienceId. Set RESEND_AUDIENCE_ID only to
 * override it. Reads env bindings first, then process.env.
 *
 * Sender is 演化日报 · Yanhua Daily <digest@yanhua.ai> once domain
 * de1ea356-1c37-419f-bffa-be649f64b080 verifies. Until then, welcome
 * mail falls back to onboarding@resend.dev.
 */
const DEFAULT_AUDIENCE = "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003";
const DEFAULT_FROM = "演化日报 · Yanhua Daily <digest@yanhua.ai>";
const FALLBACK_FROM = "onboarding@resend.dev";

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = origin === "https://yanhua.ai" || origin === "https://www.yanhua.ai";
    const headers = {
      "Access-Control-Allow-Origin": allowed ? origin : "https://yanhua.ai",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json"
    };
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
    if (request.method !== "POST") return json({ error: "method" }, 405, headers);
    let body = {};
    try { body = await request.json(); } catch (err) { return json({ error: "json" }, 400, headers); }
    const email = String(body.email || "").trim();
    const lang = body.lang === "en" || body.lang === "both" ? body.lang : "zh";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ error: "email" }, 400, headers);
    const key = setting(env, "RESEND_API_KEY");
    const audience = setting(env, "RESEND_AUDIENCE_ID") || DEFAULT_AUDIENCE;
    if (!key) return json({ error: "config" }, 500, headers);

    const created = await resend(key, "POST", "https://api.resend.com/contacts", {
      email: email,
      unsubscribed: false,
      segments: [{ id: audience }]
    });
    if (!created.ok && created.status !== 409) {
      const legacy = await resend(key, "POST", "https://api.resend.com/audiences/" + audience + "/contacts", {
        email: email,
        unsubscribed: false
      });
      if (!legacy.ok && legacy.status !== 409) return json({ error: "resend" }, 502, headers);
    }
    if (setting(env, "SEND_WELCOME") === "1") await sendWelcome(env, key, email, lang);
    return json({ ok: true }, 200, headers);
  }
};

function setting(env, name) {
  if (env && env[name]) return String(env[name]);
  if (typeof process !== "undefined" && process.env && process.env[name]) return process.env[name];
  return "";
}

async function sendWelcome(env, key, email, lang) {
  const subject = lang === "en" ? "You are subscribed to Yanhua Daily" : "已订阅演化日报";
  const html = "<p>" + subject + ".</p><p><a href=\"https://yanhua.ai/\">yanhua.ai</a></p>";
  const primary = setting(env, "RESEND_FROM") || DEFAULT_FROM;
  const fallback = setting(env, "RESEND_FROM_FALLBACK") || FALLBACK_FROM;
  const first = await resend(key, "POST", "https://api.resend.com/emails", {
    from: primary,
    to: [email],
    subject: subject,
    html: html
  });
  if (first.ok || primary === fallback) return;
  if (first.status === 403 || first.status === 422) {
    await resend(key, "POST", "https://api.resend.com/emails", {
      from: fallback,
      to: [email],
      subject: subject,
      html: html
    });
  }
}

function json(payload, status, headers) {
  return new Response(JSON.stringify(payload), { status: status, headers: headers });
}

async function resend(key, method, url, payload) {
  const response = await fetch(url, {
    method: method,
    headers: {
      Authorization: "Bearer " + key,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  return { ok: response.ok, status: response.status };
}
