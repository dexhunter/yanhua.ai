/**
 * Cloudflare Worker yanhua-subscribe (https://subscribe.yanhua.ai):
 * subscriptions and card analytics for yanhua.ai. This file is what is
 * deployed; keep it in sync with the live script.
 *
 * Bindings: CARD_ANALYTICS (Durable Object CardAnalyticsDO, object
 * name "global", key-value storage key "cards"), secret RESEND_API_KEY,
 * plain RESEND_AUDIENCE_ID (General segment). Optional plain
 * RESEND_SEGMENT_EN / RESEND_SEGMENT_ZH override the language segments.
 *
 * GET  /stats            -> { ok, subscribers, cards }
 * POST /event            -> { ok, updated }
 * POST / {email, lang}   -> Resend contact, { ok, lang }
 *
 * Email language: lang is "en" or "zh" (anything else -> "zh"). It is
 * stored as the contact property `lang` and as membership in exactly one
 * language segment, plus General. scripts/send_newsletter_resend.py
 * sends one broadcast per language segment, so each reader gets one
 * email a day in one language. The welcome email is in that language too.
 */
const SEGMENT_EN = "a1431dc1-2c68-4154-a9c5-db6a941f2b52";
const SEGMENT_ZH = "a587e8b8-f849-47ae-9e63-e58eca856083";
const FROM = { en: "Yanhua Daily <digest@yanhua.ai>", zh: "演化日报 <digest@yanhua.ai>" };

export class CardAnalyticsDO {
  constructor(ctx, env) {
    this.ctx = ctx;
    this.env = env;
  }

  async fetch(request) {
    const url = new URL(request.url);
    const cards = (await this.ctx.storage.get("cards")) || {};

    if (request.method === "POST" && url.pathname === "/event") {
      let body = {};
      try {
        body = await request.json();
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: "bad_json" }), { status: 400 });
      }
      const events = Array.isArray(body.events) ? body.events : [body];
      let updated = 0;
      for (const ev of events) {
        if (!ev || typeof ev.id !== "string") continue;
        const id = ev.id.trim().slice(0, 96);
        if (!id || !/^[a-z0-9-]+$/i.test(id)) continue;
        const row = cards[id] || { id, views: 0, dwellMs: 0, flips: 0, clicks: 0, copies: 0, updatedAt: 0 };
        const type = String(ev.type || "");
        if (type === "view") {
          row.views += 1;
        } else if (type === "dwell") {
          const ms = Math.max(0, Math.min(180000, Number(ev.ms) || 0));
          if (ms >= 500) row.dwellMs += Math.round(ms);
        } else if (type === "flip") {
          row.flips += 1;
        } else if (type === "click") {
          row.clicks += 1;
        } else if (type === "copy") {
          row.copies += 1;
        }
        if (typeof ev.dwellMs === "number" && ev.dwellMs > 0) {
          row.dwellMs += Math.round(Math.min(180000, ev.dwellMs));
        }
        row.updatedAt = Date.now();
        cards[id] = row;
        updated += 1;
      }
      if (updated > 0) {
        await this.ctx.storage.put("cards", cards);
      }
      return new Response(JSON.stringify({ ok: true, updated }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    const list = Object.values(cards).map((c) => {
      const views = c.views || 0;
      const dwellMs = c.dwellMs || 0;
      const flips = c.flips || 0;
      const clicks = c.clicks || 0;
      const copies = c.copies || 0;
      const avgDwellSec = views > 0 ? Math.round(dwellMs / views / 100) / 10 : Math.round(dwellMs / 100) / 10;
      const totalDwellSec = Math.round(dwellMs / 1000);
      const score = Math.round((views * 2 + (dwellMs / 4000) + flips * 3 + clicks * 5 + copies * 6) * 10) / 10;
      return {
        id: c.id,
        views,
        dwellMs,
        totalDwellSec,
        avgDwellSec,
        flips,
        clicks,
        copies,
        score,
        updatedAt: c.updatedAt || 0
      };
    });
    list.sort((a, b) => b.score - a.score || b.dwellMs - a.dwellMs || b.views - a.views);

    return new Response(JSON.stringify({ ok: true, cards: list }), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  }
}

export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    const url = new URL(request.url);
    const audienceId = env.RESEND_AUDIENCE_ID || "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003";

    if (request.method === "POST" && (url.pathname === "/event" || url.pathname === "/api/event")) {
      try {
        if (env.CARD_ANALYTICS) {
          const id = env.CARD_ANALYTICS.idFromName("global");
          const stub = env.CARD_ANALYTICS.get(id);
          const res = await stub.fetch("https://do/event", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: await request.text()
          });
          const data = await res.json();
          return new Response(JSON.stringify(data), {
            status: res.status,
            headers: { ...cors, "Content-Type": "application/json" }
          });
        }
        return new Response(JSON.stringify({ ok: false, error: "no_do" }), {
          status: 200,
          headers: { ...cors, "Content-Type": "application/json" }
        });
      } catch (err) {
        return new Response(JSON.stringify({ ok: false, error: String(err) }), {
          status: 200,
          headers: { ...cors, "Content-Type": "application/json" }
        });
      }
    }

    if (request.method === "GET" && (url.pathname === "/stats" || url.pathname === "/api/stats" || url.pathname === "/analytics")) {
      let subscribers = 0;
      let cards = [];
      try {
        const res = await fetch(`https://api.resend.com/audiences/${audienceId}/contacts`, {
          headers: { "Authorization": `Bearer ${env.RESEND_API_KEY}` }
        });
        const data = await res.json();
        const contacts = Array.isArray(data.data) ? data.data.filter(c => !c.unsubscribed) : [];
        subscribers = contacts.length;
      } catch (err) {}

      try {
        if (env.CARD_ANALYTICS) {
          const id = env.CARD_ANALYTICS.idFromName("global");
          const stub = env.CARD_ANALYTICS.get(id);
          const doRes = await stub.fetch("https://do/stats");
          const doData = await doRes.json();
          if (Array.isArray(doData.cards)) cards = doData.cards;
        }
      } catch (err) {}

      return new Response(JSON.stringify({ ok: true, subscribers, cards }), {
        status: 200,
        headers: { ...cors, "Content-Type": "application/json" }
      });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ ok: true, service: "yanhua-subscribe" }), {
        status: 200,
        headers: { ...cors, "Content-Type": "application/json" }
      });
    }

    try {
      let email = "";
      let rawLang = "";
      const ct = (request.headers.get("content-type") || "").toLowerCase();
      if (ct.includes("application/json")) {
        const body = await request.json();
        email = String(body.email || "").trim().toLowerCase();
        rawLang = String(body.lang || "");
      } else {
        const form = await request.formData();
        email = String(form.get("email") || "").trim().toLowerCase();
        rawLang = String(form.get("lang") || "");
      }
      const lang = normLang(rawLang);

      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        return new Response(JSON.stringify({ ok: false, error: "invalid_email" }), {
          status: 400,
          headers: { ...cors, "Content-Type": "application/json" }
        });
      }

      const segments = {
        en: env.RESEND_SEGMENT_EN || SEGMENT_EN,
        zh: env.RESEND_SEGMENT_ZH || SEGMENT_ZH
      };
      // Create is an upsert in Resend: an existing contact gets the new
      // property value and these segments added, and keeps its old ones.
      const contactRes = await resend(env, "POST", "https://api.resend.com/contacts", {
        email: email,
        unsubscribed: false,
        properties: { lang: lang },
        segments: [{ id: audienceId }, { id: segments[lang] }]
      });
      if (!contactRes.ok) {
        return new Response(JSON.stringify({ ok: false, error: contactRes.data }), {
          status: contactRes.status,
          headers: { ...cors, "Content-Type": "application/json" }
        });
      }
      // One language only: leave the other language segment (404 when not in it).
      const other = lang === "en" ? segments.zh : segments.en;
      const left = await resend(env, "DELETE", "https://api.resend.com/contacts/" + encodeURIComponent(email) + "/segments/" + other);
      if (!left.ok && left.status !== 404) {
        return new Response(JSON.stringify({ ok: false, error: "segment", detail: left.data }), {
          status: 502,
          headers: { ...cors, "Content-Type": "application/json" }
        });
      }

      const welcome = WELCOME[lang];
      await resend(env, "POST", "https://api.resend.com/emails", {
        from: FROM[lang],
        to: [email],
        subject: welcome.subject,
        html: welcome.html
      }).catch(() => {});

      return new Response(JSON.stringify({ ok: true, id: contactRes.data && contactRes.data.id, lang: lang }), {
        status: 200,
        headers: { ...cors, "Content-Type": "application/json" }
      });
    } catch (err) {
      return new Response(JSON.stringify({ ok: false, error: String(err) }), {
        status: 500,
        headers: { ...cors, "Content-Type": "application/json" }
      });
    }
  }
};

// Welcome email, styled like the daily email ("Indigo soft": white card on
// lavender-grey #f3f3f9, ink #1c1b3a, indigo accent #4f46b8).
function welcomeHtml(lang, title, body, cta, href) {
  const serif = "Georgia,'Noto Serif SC','Songti SC',serif";
  const sans = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif";
  const brand = lang === "en" ? "YANHUA DAILY" : "演化日报";
  return `<!DOCTYPE html><html lang="${lang === "en" ? "en" : "zh-Hans"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>` +
    `<body style="margin:0;padding:0;background:#f3f3f9;color:#1c1b3a;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f3f3f9" style="background:#f3f3f9;"><tr><td align="center" style="padding:28px 12px 36px;">` +
    `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;width:100%;"><tr><td style="padding:0 0 16px;border-bottom:3px solid #4f46b8;"><p style="margin:0;font-family:${serif};font-size:26px;line-height:1.25;font-weight:600;color:#1c1b3a;">${brand}</p></td></tr>` +
    `<tr><td style="padding-top:16px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="background:#ffffff;border:1px solid #dcdcef;border-radius:8px;"><tr><td style="padding:22px 22px 20px;font-family:${sans};color:#1c1b3a;">` +
    `<h2 style="margin:0 0 10px;font-family:${serif};font-size:21px;line-height:1.35;font-weight:600;color:#1c1b3a;">${title}</h2>` +
    `<p style="margin:0 0 18px;font-size:15px;line-height:1.7;color:#55557a;">${body}</p>` +
    `<a href="${href}" style="display:inline-block;padding:10px 16px;border-radius:8px;background:#4f46b8;color:#ffffff;font-size:14px;line-height:1.4;font-weight:700;text-decoration:none;">${cta}</a>` +
    `</td></tr></table></td></tr></table></td></tr></table></body></html>`;
}

const WELCOME = {
  en: {
    subject: "You're subscribed to Yanhua Daily",
    html: welcomeHtml("en", "Welcome to Yanhua Daily",
      "You're subscribed, with English as your email language. Once a day you'll get one email with that day's cards on recursive self-improvement and agent harness search, each opening with a one-sentence takeaway.",
      "Read the latest cards on yanhua.ai", "https://yanhua.ai/?lang=en")
  },
  zh: {
    subject: "已订阅演化日报",
    html: welcomeHtml("zh", "欢迎订阅演化日报",
      "订阅成功，邮件语言为中文。每天一封，收录当天关于递归自我改进与智能体框架搜索的全部闪卡，每张都以一句话结论开头。",
      "在 yanhua.ai 阅读最新闪卡", "https://yanhua.ai/")
  }
};

function normLang(value) {
  return String(value || "").trim().toLowerCase().indexOf("en") === 0 ? "en" : "zh";
}

async function resend(env, method, url, payload) {
  const init = { method: method, headers: { Authorization: `Bearer ${env.RESEND_API_KEY}` } };
  if (payload !== undefined) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(payload);
  }
  for (let attempt = 0; attempt < 4; attempt += 1) {
    const res = await fetch(url, init);
    if (res.status === 429 && attempt < 3) {
      await new Promise((resolve) => setTimeout(resolve, 600 * (attempt + 1)));
      continue;
    }
    const data = await res.json().catch(() => ({}));
    return { ok: res.ok, status: res.status, data: data };
  }
  return { ok: false, status: 429, data: {} };
}
