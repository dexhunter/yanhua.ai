/**
 * Cloudflare Worker for yanhua.ai subscriptions and card analytics.
 *
 * Browsers must not hold RESEND_API_KEY. data/config.js points
 * subscribeEndpoint, statsEndpoint, and eventsEndpoint here.
 *   wrangler secret put RESEND_API_KEY
 * Optional: SEND_WELCOME=1
 *
 * Durable Object: bind class CardAnalyticsDO as CARD_ANALYTICS
 * with a SQLite migration (`new_sqlite_classes = ["CardAnalyticsDO"]`).
 * The object name is "yanhua-cards".
 *
 * GET  /stats   -> { ok, subscribers, cards }
 * POST /event   -> { ok, updated }
 * POST / and POST /subscribe -> Resend contact
 * other routes  -> { ok:true, service:"yanhua-subscribe" }
 *
 * Card score matches the live counter:
 *   round1(dwellSeconds * 0.25) + views*2 + flips*3 + clicks*5 + copies*6
 * Each dwell event is capped at 180000 ms.
 */
const DEFAULT_AUDIENCE = "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003";
const DEFAULT_FROM = "演化日报 · Yanhua Daily <digest@yanhua.ai>";
const FALLBACK_FROM = "onboarding@resend.dev";
const DWELL_CAP_MS = 180000;

export default {
  async fetch(request, env) {
    const headers = corsHeaders();
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: headers });
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";
    if (request.method === "GET" && path === "/stats") return statsResponse(env, headers);
    if (request.method === "POST" && path === "/event") return eventResponse(request, env, headers);
    if (request.method === "POST" && (path === "/" || path === "/subscribe")) return subscribeResponse(request, env, headers);
    return json({ ok: true, service: "yanhua-subscribe" }, 200, headers);
  }
};

export class CardAnalyticsDO {
  constructor(ctx, env) {
    this.ctx = ctx;
    this.env = env;
    this.sql = ctx.storage.sql;
    ctx.blockConcurrencyWhile(async () => {
      this.sql.exec(
        "CREATE TABLE IF NOT EXISTS cards (" +
          "id TEXT PRIMARY KEY," +
          "views INTEGER NOT NULL DEFAULT 0," +
          "dwell_ms INTEGER NOT NULL DEFAULT 0," +
          "flips INTEGER NOT NULL DEFAULT 0," +
          "clicks INTEGER NOT NULL DEFAULT 0," +
          "copies INTEGER NOT NULL DEFAULT 0," +
          "updated_at INTEGER NOT NULL DEFAULT 0" +
        ")"
      );
    });
  }

  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/stats") return json(this.snapshot(), 200, {});
    if (request.method === "POST") {
      let body = {};
      try { body = await request.json(); } catch (err) { return json({ ok: false, error: "bad_json" }, 400, {}); }
      return json({ ok: true, updated: this.ingest(body) }, 200, {});
    }
    return json({ ok: false, error: "method" }, 405, {});
  }

  ingest(body) {
    const events = Array.isArray(body && body.events) ? body.events : (body && body.id ? [body] : []);
    let updated = 0;
    events.forEach((event) => {
      if (!event || typeof event !== "object") return;
      const id = String(event.id || "").trim();
      if (!id || id.length > 160) return;
      const type = String(event.type || "");
      const now = Date.now();
      this.sql.exec(
        "INSERT INTO cards (id, views, dwell_ms, flips, clicks, copies, updated_at) VALUES (?, 0, 0, 0, 0, 0, ?) " +
          "ON CONFLICT(id) DO UPDATE SET updated_at = excluded.updated_at",
        id,
        now
      );
      if (type === "view") this.sql.exec("UPDATE cards SET views = views + 1, updated_at = ? WHERE id = ?", now, id);
      else if (type === "flip") this.sql.exec("UPDATE cards SET flips = flips + 1, updated_at = ? WHERE id = ?", now, id);
      else if (type === "click") this.sql.exec("UPDATE cards SET clicks = clicks + 1, updated_at = ? WHERE id = ?", now, id);
      else if (type === "copy") this.sql.exec("UPDATE cards SET copies = copies + 1, updated_at = ? WHERE id = ?", now, id);
      else if (type === "dwell") {
        const ms = Number(event.ms);
        if (Number.isFinite(ms) && ms > 0) {
          const capped = Math.min(DWELL_CAP_MS, Math.floor(ms));
          this.sql.exec("UPDATE cards SET dwell_ms = dwell_ms + ?, updated_at = ? WHERE id = ?", capped, now, id);
        }
      }
      updated += 1;
    });
    return updated;
  }

  snapshot() {
    const rows = this.sql.exec(
      "SELECT id, views, dwell_ms, flips, clicks, copies, updated_at FROM cards ORDER BY updated_at DESC"
    ).toArray();
    const cards = rows.map((row) => {
      const dwellMs = Number(row.dwell_ms) || 0;
      const views = Number(row.views) || 0;
      const flips = Number(row.flips) || 0;
      const clicks = Number(row.clicks) || 0;
      const copies = Number(row.copies) || 0;
      const dwellSeconds = dwellMs / 1000;
      return {
        id: row.id,
        views: views,
        dwellMs: dwellMs,
        totalDwellSec: Math.floor(dwellSeconds),
        avgDwellSec: views > 0 ? round1(dwellMs / views / 1000) : 0,
        flips: flips,
        clicks: clicks,
        copies: copies,
        score: round1(dwellSeconds * 0.25) + views * 2 + flips * 3 + clicks * 5 + copies * 6,
        updatedAt: Number(row.updated_at) || 0
      };
    });
    cards.sort((a, b) => b.score - a.score || b.updatedAt - a.updatedAt);
    return cards;
  }
}

function round1(value) {
  return Math.round(value * 10) / 10;
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Content-Type": "application/json"
  };
}

function analytics(env) {
  if (!env || !env.CARD_ANALYTICS || !env.CARD_ANALYTICS.idFromName) return null;
  return env.CARD_ANALYTICS.get(env.CARD_ANALYTICS.idFromName("yanhua-cards"));
}

async function statsResponse(env, headers) {
  const subscribers = await countSubscribers(env);
  let cards = [];
  const stub = analytics(env);
  if (stub) {
    const response = await stub.fetch("https://analytics.internal/stats");
    cards = await response.json();
  }
  return json({ ok: true, subscribers: subscribers, cards: cards }, 200, headers);
}

async function eventResponse(request, env, headers) {
  let body = {};
  try { body = await request.json(); }
  catch (err) { return json({ ok: false, error: "bad_json" }, 400, headers); }
  const stub = analytics(env);
  if (!stub) return json({ ok: true, updated: 0 }, 200, headers);
  const response = await stub.fetch("https://analytics.internal/event", {
    method: "POST",
    body: JSON.stringify(body)
  });
  const payload = await response.json();
  return json(payload, response.status, headers);
}

async function subscribeResponse(request, env, headers) {
  let body = {};
  try { body = await request.json(); }
  catch (err) { return json({ ok: false, error: err && err.message ? err.message : "bad_json" }, 400, headers); }
  const email = String(body.email || "").trim();
  const lang = body.lang === "en" || body.lang === "both" ? body.lang : "zh";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ ok: false, error: "invalid_email" }, 400, headers);
  const key = setting(env, "RESEND_API_KEY");
  const audience = setting(env, "RESEND_AUDIENCE_ID") || DEFAULT_AUDIENCE;
  if (!key) return json({ ok: false, error: "config" }, 500, headers);

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
    if (!legacy.ok && legacy.status !== 409) return json({ ok: false, error: "resend" }, 502, headers);
  }
  if (setting(env, "SEND_WELCOME") === "1") await sendWelcome(env, key, email, lang);
  return json({ ok: true }, 200, headers);
}

async function countSubscribers(env) {
  const key = setting(env, "RESEND_API_KEY");
  const audience = setting(env, "RESEND_AUDIENCE_ID") || DEFAULT_AUDIENCE;
  if (!key) return 0;
  let count = 0;
  let after = "";
  for (let page = 0; page < 20; page += 1) {
    const url = "https://api.resend.com/audiences/" + audience + "/contacts?limit=100" + (after ? "&after=" + encodeURIComponent(after) : "");
    const response = await fetch(url, { headers: { Authorization: "Bearer " + key } });
    if (!response.ok) return count;
    const body = await response.json().catch(function () { return {}; });
    const rows = Array.isArray(body.data) ? body.data : [];
    count += rows.length;
    if (!body.has_more || !rows.length) break;
    after = rows[rows.length - 1] && rows[rows.length - 1].id ? rows[rows.length - 1].id : "";
    if (!after) break;
  }
  return count;
}

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
