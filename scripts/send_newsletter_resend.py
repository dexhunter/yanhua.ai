#!/usr/bin/env python3
"""Sync subscribers into Resend, and send the daily digest in one language per reader.

Every subscriber picks one email language, English or 中文, in the
subscribe dialog. The worker (scripts/cloudflare-resend-worker.js)
stores it twice on the Resend contact:

  * contact property  lang = "en" | "zh"   (fallback "zh")
  * segment membership  exactly one of
      SEGMENT_EN  a1431dc1-2c68-4154-a9c5-db6a941f2b52  "Email language: English"
      SEGMENT_ZH  a587e8b8-f849-47ae-9e63-e58eca856083  "Email language: 中文"
    plus the General segment 0f2fbb4e-3333-43c1-a0d2-16c69a7c3003 (all readers)

  python3 scripts/send_newsletter_resend.py --sync-only
  python3 scripts/send_newsletter_resend.py --send
  python3 scripts/send_newsletter_resend.py --send --date 2026-10-27
  python3 scripts/send_newsletter_resend.py --send --dry-run
  python3 scripts/send_newsletter_resend.py --preview /tmp/daily.html --lang en

--sync-only adds label:subscribe GitHub issue emails (with their
"lang: en|zh" line, default zh) and makes sure every contact sits in
exactly one language segment. Contacts with no language get zh.
It sends no mail.

--send does that sync, then creates one broadcast per language, each to
its own segment only, so nobody gets two emails. The once-per-day guard
skips a language when Resend already has a broadcast for that date and
language, or any broadcast created on the same UTC day for that
language's segment or for the General segment. --dry-run runs the sync
and the guard and prints what would be sent, without creating a broadcast.

--preview writes the HTML for one language (default zh) and does not
call Resend. The date defaults to the newest edition's date.

Senders: "Yanhua Daily <digest@yanhua.ai>" for English and
"演化日报 <digest@yanhua.ai>" for Chinese (override with RESEND_FROM_EN /
RESEND_FROM_ZH). If RESEND_API_KEY is missing, --sync-only and --send
exit 0 so a Pages deploy is not marked failed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_digest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "digests.json"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ISSUE_LANG_RE = re.compile(r"^\s*lang\s*:\s*([A-Za-z]+)", re.IGNORECASE | re.MULTILINE)
API = "https://api.resend.com"
DEFAULT_AUDIENCE = "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003"
DEFAULT_SEGMENTS = {
    "en": "a1431dc1-2c68-4154-a9c5-db6a941f2b52",
    "zh": "a587e8b8-f849-47ae-9e63-e58eca856083",
}
LANGS = ("zh", "en")
DEFAULT_LANG = "zh"
LANG_PROPERTY = "lang"
DEFAULT_FROM = {
    "en": "Yanhua Daily <digest@yanhua.ai>",
    "zh": "演化日报 <digest@yanhua.ai>",
}
FALLBACK_FROM = "onboarding@resend.dev"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLOT_ORDER = {"morning": 0, "": 1, "evening": 2}
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Songti SC','Noto Serif SC',serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Noto Sans SC','Microsoft YaHei',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SITE = "https://yanhua.ai/"
REPLY_TO = "digest@yanhua.ai"
UNSUBSCRIBE_URL = "{{{RESEND_UNSUBSCRIBE_URL}}}"
_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
# Broadcasts that never reach anyone do not count toward the daily limit.
DEAD_STATUSES = {"failed", "canceled", "cancelled"}

STRINGS = {
    "en": {
        "html_lang": "en",
        "brand": "Yanhua Daily",
        "masthead": "YANHUA DAILY",
        "tagline": "Recursive self-improvement &amp; agent harness search",
        "read": "Read the cards on yanhua.ai",
        "conclusion": "Takeaway",
        "problem": "Problem",
        "how": "How it works &amp; evidence",
        "slot": {"morning": "Morning edition", "evening": "Evening edition", "": "Daily edition"},
        "unsubscribe": "Unsubscribe",
        "feed_json": "JSON Feed",
        "about": "One email a day with that day's cards. The site updates at 09:00 and 18:00 UTC.",
        "link": "Link",
        "paper": "Paper",
        "repo": "Repo",
        "x_post": "X Post",
        "sep": ": ",
    },
    "zh": {
        "html_lang": "zh-Hans",
        "brand": "演化日报",
        "masthead": "演化日报",
        "tagline": "递归自我改进与智能体框架搜索",
        "read": "在 yanhua.ai 阅读闪卡",
        "conclusion": "核心结论",
        "problem": "问题背景",
        "how": "核心机制与实证",
        "slot": {"morning": "早间版", "evening": "晚间版", "": "当日版"},
        "unsubscribe": "退订",
        "feed_json": "JSON 订阅源",
        "about": "每天一封，收录当天的全部闪卡。网站每天 09:00 与 18:00（UTC）更新。",
        "link": "链接",
        "paper": "论文",
        "repo": "仓库",
        "x_post": "X 原帖",
        "sep": "：",
    },
}

# The authors field is written in English. These connectives are the only
# English words in it apart from names and institutions, so the Chinese
# email swaps them.
ZH_AUTHOR_WORDS = (
    (re.compile(r";\s*shared by\s+", re.IGNORECASE), "；分享："),
    (re.compile(r",?\s*commentary by\s+", re.IGNORECASE), "；评论："),
    (re.compile(r";\s*listed by\s+", re.IGNORECASE), "；收录："),
    (re.compile(r";\s*posted by\s+", re.IGNORECASE), "；发布："),
    (re.compile(r"^shared by\s+", re.IGNORECASE), "分享："),
)


def env(name: str) -> str:
    return os.environ.get(name, "").strip()


def norm_lang(value: object) -> str:
    text = str(value or "").strip().lower()
    if text.startswith("en"):
        return "en"
    if text.startswith("zh") or text in {"cn", "chinese", "中文"}:
        return "zh"
    return ""


def request(method: str, url: str, payload: dict | None = None, token: str = "") -> tuple[int, dict | list | str]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json", "User-Agent": "yanhua-digest"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        headers["Content-Type"] = "application/json"
    for attempt in range(4):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                raw = response.read().decode("utf-8")
                return response.status, json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429 and attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            try:
                body: dict | list | str = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                body = raw[:500]
            return exc.code, body
    return 429, {}


# ---------------------------------------------------------------- subscribers


def segment_ids() -> dict[str, str]:
    return {
        "en": env("RESEND_SEGMENT_EN") or DEFAULT_SEGMENTS["en"],
        "zh": env("RESEND_SEGMENT_ZH") or DEFAULT_SEGMENTS["zh"],
    }


def github_subscribers() -> dict[str, str]:
    """email -> lang ("" when the issue does not say)."""
    repo = env("GITHUB_REPOSITORY") or "dexhunter/yanhua.ai"
    token = env("GH_TOKEN") or env("GITHUB_TOKEN")
    found: dict[str, str] = {}
    for page in range(1, 6):
        url = f"https://api.github.com/repos/{repo}/issues?labels=subscribe&state=all&per_page=100&page={page}"
        status, body = request("GET", url, token=token)
        if status in {401, 403, 404}:
            print(f"github issues lookup returned {status}; continuing with none")
            return found
        if status >= 300 or not isinstance(body, list):
            print(f"github issues lookup returned {status}")
            return found
        if not body:
            break
        for issue in body:
            if not isinstance(issue, dict) or "pull_request" in issue:
                continue
            text = f"{issue.get('title') or ''}\n{issue.get('body') or ''}"
            match = ISSUE_LANG_RE.search(text)
            lang = norm_lang(match.group(1)) if match else ""
            for email in EMAIL_RE.findall(text):
                found.setdefault(email.lower(), lang)
        if len(body) < 100:
            break
    return found


def list_contacts(key: str, segment: str = "") -> list[dict]:
    rows: list[dict] = []
    after = ""
    for _ in range(50):
        query = {"limit": "100"}
        if segment:
            query["segment_id"] = segment
        if after:
            query["after"] = after
        status, body = request("GET", f"{API}/contacts?{urllib.parse.urlencode(query)}", token=key)
        if status >= 300 or not isinstance(body, dict):
            raise RuntimeError(f"could not list contacts ({status})")
        batch = [row for row in body.get("data") or [] if isinstance(row, dict)]
        rows.extend(batch)
        if not body.get("has_more") or not batch:
            break
        after = str(batch[-1].get("id") or "")
        if not after:
            break
    return rows


def ensure_lang_property(key: str) -> None:
    status, body = request("GET", f"{API}/contact-properties", token=key)
    if status < 300 and isinstance(body, dict):
        if any((row or {}).get("key") == LANG_PROPERTY for row in body.get("data") or []):
            return
    status, body = request("POST", f"{API}/contact-properties", {
        "key": LANG_PROPERTY, "type": "string", "fallback_value": DEFAULT_LANG,
    }, token=key)
    if status not in {200, 201, 409, 422}:
        raise RuntimeError(f"could not create the lang contact property ({status} {body})")


def contact_lang(key: str, ident: str) -> str:
    status, body = request("GET", f"{API}/contacts/{urllib.parse.quote(ident)}", token=key)
    if status >= 300 or not isinstance(body, dict):
        return ""
    prop = (body.get("properties") or {}).get(LANG_PROPERTY)
    if isinstance(prop, dict):
        prop = prop.get("value")
    # Before the lang property existed, the worker wrote the choice into
    # first_name ("zh" / "en" / "both"). "both" reads as no choice.
    return norm_lang(prop) or norm_lang(body.get("first_name") if body.get("first_name") in {"en", "zh"} else "")


def set_contact_lang(key: str, ident: str, lang: str, segments: dict[str, str], general: str) -> None:
    """Store lang on the contact and keep it in exactly one language segment."""
    quoted = urllib.parse.quote(ident)
    status, body = request("PATCH", f"{API}/contacts/{quoted}", {"properties": {LANG_PROPERTY: lang}}, token=key)
    if status >= 300:
        raise RuntimeError(f"could not set lang on a contact ({status} {body})")
    for seg in (general, segments[lang]):
        status, body = request("POST", f"{API}/contacts/{quoted}/segments/{seg}", token=key)
        if status >= 300 and status != 409:
            raise RuntimeError(f"could not add a contact to segment {seg} ({status} {body})")
    other = segments["en" if lang == "zh" else "zh"]
    status, body = request("DELETE", f"{API}/contacts/{quoted}/segments/{other}", token=key)
    if status >= 300 and status != 404:
        raise RuntimeError(f"could not remove a contact from segment {other} ({status} {body})")


def add_contact(key: str, general: str, email: str) -> None:
    # Language segment and property are set by reconcile_languages().
    payload: dict = {
        "email": email,
        "unsubscribed": False,
        "segments": [{"id": general}],
    }
    status, body = request("POST", f"{API}/contacts", payload, token=key)
    if status not in {200, 201, 409}:
        legacy, _legacy_body = request(
            "POST",
            f"{API}/audiences/{urllib.parse.quote(general)}/contacts",
            {"email": email, "unsubscribed": False},
            token=key,
        )
        if legacy not in {200, 201, 409}:
            raise RuntimeError(f"could not add a contact ({status}, legacy {legacy})")


def reconcile_languages(key: str, general: str, segments: dict[str, str], hints: dict[str, str]) -> dict[str, int]:
    everyone = {str(row.get("id")): row for row in list_contacts(key)}
    members = {lang: {str(row.get("id")) for row in list_contacts(key, seg)} for lang, seg in segments.items()}
    in_general = {str(row.get("id")) for row in list_contacts(key, general)}
    counts = {"en": 0, "zh": 0}
    for cid, row in everyone.items():
        email = str(row.get("email") or "").lower()
        in_en, in_zh = cid in members["en"], cid in members["zh"]
        if in_en != in_zh and cid in in_general:
            counts["en" if in_en else "zh"] += 0 if row.get("unsubscribed") else 1
            continue
        lang = contact_lang(key, cid)
        if not lang:
            lang = hints.get(email) or DEFAULT_LANG
        if in_en and in_zh:
            print(f"contact {cid} was in both language segments; keeping {lang}")
        elif not in_en and not in_zh:
            print(f"contact {cid} had no language segment; assigning {lang}")
        set_contact_lang(key, cid, lang, segments, general)
        counts[lang] += 0 if row.get("unsubscribed") else 1
    return counts


def sync(key: str, general: str) -> dict[str, int]:
    segments = segment_ids()
    ensure_lang_property(key)
    hints = github_subscribers()
    # Only create contacts Resend does not have yet. Create is an upsert,
    # so re-posting an existing one would undo an unsubscribe.
    known = {str(row.get("email") or "").lower() for row in list_contacts(key)}
    added = 0
    for email, lang in hints.items():
        if email in known:
            continue
        add_contact(key, general, email)
        added += 1
    print(f"found {len(hints)} subscribe-issue address(es); added {added} new contact(s) to Resend")
    counts = reconcile_languages(key, general, segments, hints)
    print(f"active subscribers by email language: zh {counts['zh']}, en {counts['en']}")
    return counts


# ---------------------------------------------------------------- rendering


def load_doc() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def resolve_date(doc: dict, requested: str | None) -> str:
    if requested:
        if not DATE_RE.fullmatch(requested):
            raise SystemExit(f"invalid --date {requested}; use YYYY-MM-DD")
        return requested
    editions = doc.get("editions") or []
    if not editions or not editions[0].get("date"):
        raise SystemExit("digests.json has no edition date to default to")
    return str(editions[0]["date"])


def editions_for_date(doc: dict, target_date: str) -> list[dict]:
    matched = [edition for edition in doc.get("editions") or [] if edition.get("date") == target_date]
    matched.sort(key=lambda edition: (SLOT_ORDER.get(edition.get("slot") or "", 1), str(edition.get("id") or "")))
    return matched


def items_for_edition(doc: dict, edition_id: str) -> list[dict]:
    return [item for item in doc.get("items") or [] if item.get("edition") == edition_id]


def text_of(value: object, lang: str) -> str:
    """One language only. Falls back to the other language only when the field
    is missing, which update_digest.py check already rejects."""
    if isinstance(value, dict):
        other = "en" if lang == "zh" else "zh"
        return str(value.get(lang) or value.get(other) or "")
    return str(value or "")


def linked(text: str, item: dict) -> str:
    """linkify() already escapes text and skips PR@1, pass@1, and Best@1."""
    html = update_digest.linkify(text, item)
    return html.replace("<a ", '<a style="color:#4f46b8;text-decoration:underline;" ')


def subject_date(target_date: str) -> str:
    year, month, day = target_date.split("-")
    return f"{int(day)} {_MONTHS[int(month) - 1]} {year}"


def subject_for(target_date: str, total: int, lang: str = "en") -> str:
    if lang == "zh":
        return f"演化日报 · {target_date} · {total} 篇"
    noun = "paper" if total == 1 else "papers"
    return f"Yanhua Daily · {subject_date(target_date)} · {total} {noun}"


def preview_text_for(total: int, lang: str = "en") -> str:
    if lang == "zh":
        return f"今日 {total} 篇：递归自我改进与智能体框架搜索。"
    noun = "paper" if total == 1 else "papers"
    return f"{total} {noun} on recursive self-improvement and agent harness search."


def day_summary(target_date: str, editions: list[dict], total: int, lang: str) -> str:
    slots = {edition.get("slot") or "" for edition in editions}
    names = [STRINGS[lang]["slot"][slot] for slot in ("morning", "evening") if slot in slots]
    if lang == "zh":
        inner = (" + ".join(names) + " · " if names else "") + f"共 {total} 篇"
        return f"{target_date} 每日合辑（{inner}）"
    noun = "paper" if total == 1 else "papers"
    inner = (" + ".join(names) + " · " if names else "") + f"{total} {noun}"
    return f"Daily digest, {subject_date(target_date)} ({inner})"


def authors_text(authors: str, lang: str) -> str:
    if lang != "zh":
        return authors
    for pattern, repl in ZH_AUTHOR_WORDS:
        authors = pattern.sub(repl, authors)
    return authors


def pill_html(pill: dict, lang: str) -> str:
    value = text_of(pill.get("value"), lang)
    label = str(pill.get(lang) or pill.get("label") or pill.get("en" if lang == "zh" else "zh") or "")
    tone = str(pill.get("tone") or "flat")
    color = {"up": "#1f7a55", "down": "#b83a4b"}.get(tone, "#1c1b3a")
    return (
        '<span style="display:inline-block;margin:0 8px 8px 0;padding:8px 10px;'
        'border:1px solid #dcdcef;border-radius:8px;background:#f3f3f9;vertical-align:top;">'
        f'<b style="display:block;font-family:{MONO};font-size:14px;line-height:1.35;color:{color};">{escape(value)}</b>'
        f'<span style="display:block;margin-top:3px;font-family:{SANS};font-size:11px;line-height:1.35;color:#64648a;">{escape(label)}</span>'
        "</span>"
    )


def profile_html(handle: str) -> str:
    parts: list[str] = []
    for match in update_digest.HANDLE_RE.finditer(handle):
        name = match.group(1)
        href = escape(f"https://x.com/{name}", quote=True)
        parts.append(f'<a href="{href}" style="color:#4f46b8;text-decoration:underline;">@{escape(name)}</a>')
    return " · ".join(parts)


def byline_html(item: dict, lang: str) -> str:
    bits: list[str] = []
    arxiv = str(item.get("arxiv") or "").strip()
    if arxiv:
        href = escape(f"https://arxiv.org/abs/{arxiv}", quote=True)
        bits.append(
            f'<a href="{href}" style="color:#4f46b8;text-decoration:none;border:1px solid #dcdcef;'
            f'border-radius:8px;padding:2px 7px;background:#f3f3f9;">arXiv:{escape(arxiv)}</a>'
        )
    authors = str(item.get("authors") or "").strip()
    if authors:
        bits.append(linked(authors_text(authors, lang), item))
    profiles = profile_html(str(item.get("handle") or "").strip())
    if profiles:
        bits.append(profiles)
    if not bits:
        return ""
    return (
        f'<p style="margin:8px 0 0;font-family:{SANS};font-size:13px;line-height:1.6;color:#55557a;">'
        + " · ".join(bits)
        + "</p>"
    )


def source_links(item: dict, lang: str) -> list[tuple[str, str]]:
    """(label, url) in one language. Bare x.com profile links are left to the byline."""
    words = STRINGS[lang]
    raw = [dict(link) for link in (item.get("links") or []) if link.get("url")]
    seen = {str(link["url"]) for link in raw}
    arxiv = str(item.get("arxiv") or "").strip()
    if arxiv:
        url = f"https://arxiv.org/abs/{arxiv}"
        if url not in seen:
            raw.insert(0, {"zh": "论文", "en": "Paper", "url": url})
            seen.add(url)
    repo = str(item.get("repo") or "").strip()
    if repo:
        url = repo if repo.startswith("http") else f"https://github.com/{repo.lstrip('/')}"
        if url not in seen:
            raw.append({"zh": "仓库", "en": "Repo", "url": url})
    out: list[tuple[str, str]] = []
    emitted: set[str] = set()
    for link in raw:
        url = str(link["url"])
        match = update_digest.X_URL_RE.match(url)
        if (match and not match.group(2)) or url in emitted:
            continue
        emitted.add(url)
        label = str(link.get(lang) or "").strip()
        if match:
            handle = match.group(1)
            if not label or label.casefold() in update_digest.GENERIC_POST_LABELS:
                label = words["x_post"]
            if f"@{handle}".casefold() not in label.casefold():
                label = f"{label} · @{handle}"
        elif not label:
            ax = update_digest.ARXIV_RE.search(url)
            label = words["paper"] if ax else words["link"]
        ax = update_digest.ARXIV_RE.search(url)
        if ax and not match and label in {"论文", "Paper"}:
            label = f"{label} arXiv:{ax.group(1)}"
        out.append((label, url))
    return out


def source_html(item: dict, lang: str) -> str:
    links = []
    for label, url in source_links(item, lang):
        links.append(
            f'<a href="{escape(url, quote=True)}" style="display:inline-block;margin:0 8px 8px 0;padding:6px 10px;'
            "border:1px solid #dcdcef;border-radius:8px;background:#f3f3f9;color:#1c1b3a;"
            f'text-decoration:none;font-family:{SANS};font-size:13px;line-height:1.4;">{escape(label)}</a>'
        )
    if not links:
        return ""
    return '<p style="margin:16px 0 0;padding-top:12px;border-top:1px solid #dcdcef;">' + "".join(links) + "</p>"


def prose_block(kicker: str, body_html: str) -> str:
    return (
        f'<p style="margin:16px 0 6px;font-family:{SANS};font-size:11px;line-height:1.4;'
        f'letter-spacing:0.08em;text-transform:uppercase;color:#4f46b8;font-weight:700;">{kicker}</p>'
        f'<p style="margin:0;font-family:{SANS};font-size:15px;line-height:1.65;color:#1c1b3a;">{body_html}</p>'
    )


def card_url(item: dict) -> str:
    return f"{SITE}?mode=deck#{item.get('id') or ''}"


def card_html(item: dict, lang: str) -> str:
    words = STRINGS[lang]
    item_id = escape(str(item.get("id") or ""), quote=True)
    title = escape(text_of(item.get("title"), lang))
    pills = "".join(pill_html(pill, lang) for pill in (item.get("pills") or []) if isinstance(pill, dict))
    pills_html = f'<p style="margin:14px 0 0;font-family:{SANS};line-height:1;">{pills}</p>' if pills else ""
    return f"""
<table role="presentation" id="{item_id}" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="margin:0 0 16px;background:#ffffff;border:1px solid #dcdcef;border-radius:8px;">
  <tr>
    <td style="padding:20px 22px 18px;font-family:{SANS};color:#1c1b3a;">
      <h2 style="margin:0;font-family:{SERIF};font-size:22px;line-height:1.35;font-weight:600;color:#1c1b3a;">
        <a href="{escape(card_url(item), quote=True)}" style="color:#1c1b3a;text-decoration:none;">{title}</a>
      </h2>
      {byline_html(item, lang)}
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#efeefc" style="margin:16px 0 0;background:#efeefc;border:1px solid #cbc8f0;border-radius:6px;">
        <tr>
          <td style="padding:14px 16px 16px;">
            <p style="margin:0;font-family:{SERIF};font-size:18px;font-weight:500;line-height:1.65;color:#1c1b3a;"><span style="display:inline-block;margin:0 8px 0 0;padding:2px 7px;border-radius:4px;background:#4f46b8;color:#ffffff;font-family:{SANS};font-size:12px;font-weight:700;letter-spacing:0.04em;line-height:1.4;vertical-align:2px;">{words["conclusion"]}</span>{linked(text_of(item.get("why"), lang), item)}</p>
          </td>
        </tr>
      </table>
      {pills_html}
      {prose_block(words["problem"], linked(text_of(item.get("what"), lang), item))}
      {prose_block(words["how"], linked(text_of(item.get("how"), lang), item))}
      {source_html(item, lang)}
    </td>
  </tr>
</table>
""".strip()


def section_heading(edition: dict, count: int, lang: str) -> str:
    name = STRINGS[lang]["slot"].get(edition.get("slot") or "", STRINGS[lang]["slot"][""])
    if lang == "zh":
        return f"{name} · {count} 篇"
    return f"{name} · {count} {'paper' if count == 1 else 'papers'}"


def section_html(edition: dict, items: list[dict], show_heading: bool, lang: str) -> str:
    cards = "\n".join(card_html(item, lang) for item in items)
    if not show_heading:
        return cards
    label = escape(text_of(edition.get("label"), lang))
    return f"""
<h2 style="margin:28px 0 12px;font-family:{SERIF};font-size:18px;line-height:1.4;font-weight:600;color:#1c1b3a;">{escape(section_heading(edition, len(items), lang))}</h2>
<p style="margin:-6px 0 14px;font-family:{SANS};font-size:13px;line-height:1.5;color:#55557a;">{label}</p>
{cards}
""".strip()


def card_plain(item: dict, lang: str) -> str:
    words = STRINGS[lang]
    lines = [text_of(item.get("title"), lang).strip()]
    if item.get("id"):
        lines.append(card_url(item))
    lines.extend(["", words["conclusion"], text_of(item.get("why"), lang).strip()])
    links = source_links(item, lang)
    if links:
        lines.append("")
        lines.extend(f"{label}{words['sep']}{url}" for label, url in links)
    return "\n".join(lines).strip()


def plain_daily_email(subject: str, preview: str, grouped: list[tuple[dict, list[dict]]], show_heading: bool, lang: str) -> str:
    words = STRINGS[lang]
    blocks: list[str] = []
    for edition, items in grouped:
        if show_heading:
            blocks.append(section_heading(edition, len(items), lang))
        blocks.append("\n\n".join(card_plain(item, lang) for item in items))
    body = "\n\n".join(block for block in blocks if block).strip()
    return "\n".join([
        subject, "", preview, "", SITE, "", body, "", "----", "",
        f"{words['brand']} · yanhua.ai",
        words["about"],
        f"{words['unsubscribe']}{words['sep']}{UNSUBSCRIBE_URL}",
        "",
    ])


def render_daily_email(requested_date: str | None = None, lang: str = DEFAULT_LANG) -> tuple[str, str, str, str]:
    if lang not in STRINGS:
        raise SystemExit(f"unknown language {lang}; use en or zh")
    words = STRINGS[lang]
    doc = load_doc()
    target_date = resolve_date(doc, requested_date)
    editions = editions_for_date(doc, target_date)
    grouped = [(edition, items_for_edition(doc, str(edition.get("id") or ""))) for edition in editions]
    grouped = [(edition, items) for edition, items in grouped if items]
    if not grouped:
        raise SystemExit(f"no items for {target_date}")
    total = sum(len(items) for _, items in grouped)
    subject = subject_for(target_date, total, lang)
    preview = preview_text_for(total, lang)
    summary = day_summary(target_date, [edition for edition, _ in grouped], total, lang)
    show_heading = len(grouped) > 1 or any((edition.get("slot") or "") in {"morning", "evening"} for edition, _ in grouped)
    sections = "\n".join(section_html(edition, items, show_heading, lang) for edition, items in grouped)
    text = plain_daily_email(subject, preview, grouped, show_heading, lang)
    html = f"""<!DOCTYPE html>
<html lang="{words['html_lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(subject)}</title>
</head>
<body style="margin:0;padding:0;background:#f3f3f9;color:#1c1b3a;">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#f3f3f9;">{escape(preview)}</div>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f3f3f9" style="background:#f3f3f9;">
    <tr>
      <td align="center" style="padding:28px 12px 36px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;width:100%;">
          <tr>
            <td style="padding:0 0 18px;border-bottom:3px solid #4f46b8;">
              <p style="margin:0;font-family:{SERIF};font-size:28px;line-height:1.25;font-weight:600;color:#1c1b3a;">{words['masthead']}</p>
              <p style="margin:8px 0 0;font-family:{SANS};font-size:14px;line-height:1.55;color:#55557a;">{words['tagline']}</p>
              <p style="margin:14px 0 0;">
                <span style="display:inline-block;padding:6px 10px;border:1px solid #dcdcef;border-radius:8px;background:#efeefc;color:#4f46b8;font-family:{SANS};font-size:13px;line-height:1.4;font-weight:700;">{escape(summary)}</span>
              </p>
              <p style="margin:14px 0 0;">
                <a href="{SITE}" style="display:inline-block;padding:10px 16px;border-radius:8px;background:#4f46b8;color:#ffffff;font-family:{SANS};font-size:14px;line-height:1.4;font-weight:700;text-decoration:none;">{words['read']}</a>
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding-top:8px;">
              {sections}
            </td>
          </tr>
          <tr>
            <td style="padding:22px 0 0;border-top:1px solid #dcdcef;font-family:{SANS};font-size:13px;line-height:1.7;color:#55557a;">
              <p style="margin:0 0 8px;">{words['brand']} · <a href="{SITE}" style="color:#4f46b8;text-decoration:underline;">yanhua.ai</a></p>
              <p style="margin:0 0 8px;">
                <a href="https://yanhua.ai/feed.xml" style="color:#4f46b8;text-decoration:underline;">RSS</a>
                ·
                <a href="https://yanhua.ai/feed.json" style="color:#4f46b8;text-decoration:underline;">{words['feed_json']}</a>
                ·
                <a href="{UNSUBSCRIBE_URL}" style="color:#4f46b8;text-decoration:underline;">{words['unsubscribe']}</a>
              </p>
              <p style="margin:0;">{words['about']}</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return subject, html, text, preview


def write_preview(path: str, requested_date: str | None, lang: str) -> None:
    subject, html, text, _preview = render_daily_email(requested_date, lang)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    out.with_suffix(".txt").write_text(text, encoding="utf-8")
    print(f"subject: {subject}")
    print(f"wrote {out} and {out.with_suffix('.txt')}")


# ---------------------------------------------------------------- sending


def from_addresses(lang: str) -> list[str]:
    primary = env(f"RESEND_FROM_{lang.upper()}") or DEFAULT_FROM[lang]
    fallback = env("RESEND_FROM_FALLBACK") or FALLBACK_FROM
    return [primary] if fallback == primary else [primary, fallback]


def domain_rejected(status: int, body: dict | list | str) -> bool:
    if status not in {403, 422}:
        return False
    lowered = (body if isinstance(body, str) else json.dumps(body)).lower()
    return "domain" in lowered or "verif" in lowered or "from" in lowered


def broadcast_name(target_date: str, lang: str, subject: str) -> str:
    # The name is internal to Resend; the guard keys on its prefix.
    return f"yanhua {target_date} {lang} · {subject}"


def list_broadcasts(key: str, pages: int = 5) -> list[dict]:
    rows: list[dict] = []
    after = ""
    for _ in range(pages):
        query = {"limit": "100"}
        if after:
            query["after"] = after
        status, body = request("GET", f"{API}/broadcasts?{urllib.parse.urlencode(query)}", token=key)
        if status >= 300 or not isinstance(body, dict):
            raise RuntimeError(f"could not list broadcasts ({status}); refusing to send without the daily check")
        batch = [row for row in body.get("data") or [] if isinstance(row, dict)]
        rows.extend(batch)
        if not body.get("has_more") or not batch:
            break
        after = str(batch[-1].get("id") or "")
    return rows


def blocking_broadcast(rows: list[dict], target_date: str, lang: str, segment: str, general: str, today: str) -> dict | None:
    """A broadcast that means this language already got (or is getting) its email."""
    legacy_name = f"Yanhua Daily · {subject_date(target_date)}"
    prefix = f"yanhua {target_date} {lang} "
    for row in rows:
        if str(row.get("status") or "").lower() in DEAD_STATUSES:
            continue
        name = str(row.get("name") or "")
        seg = str(row.get("segment_id") or row.get("audience_id") or "")
        created = str(row.get("created_at") or "")[:10]
        if name.startswith(prefix):
            return row
        if seg == general and name.startswith(legacy_name):
            return row
        if created == today and seg in {segment, general}:
            return row
    return None


def create_broadcast(key: str, segment: str, lang: str, name: str, subject: str, html: str, text: str, preview: str) -> str:
    addresses = from_addresses(lang)
    for index, sender in enumerate(addresses):
        payload = {
            "segment_id": segment,
            "from": sender,
            "reply_to": [REPLY_TO],
            "subject": subject,
            "preview_text": preview,
            "html": html,
            "text": text,
            "name": name,
            "send": True,
        }
        status, body = request("POST", f"{API}/broadcasts", payload, token=key)
        if status in {200, 201}:
            return str((body or {}).get("id") if isinstance(body, dict) else "")
        retry = index + 1 < len(addresses) and domain_rejected(status, body)
        if not retry:
            raise RuntimeError(f"broadcast failed: {status} {body}")
        print(f"sender {sender} is not verified yet; trying {addresses[index + 1]}")
    raise RuntimeError("broadcast failed")


def send(key: str, general: str, requested_date: str | None, counts: dict[str, int], dry_run: bool) -> None:
    segments = segment_ids()
    target_date = resolve_date(load_doc(), requested_date)
    today = datetime.now(timezone.utc).date().isoformat()
    existing = list_broadcasts(key)
    for lang in LANGS:
        subject, html, text, preview = render_daily_email(target_date, lang)
        if counts.get(lang, 0) <= 0:
            print(f"[{lang}] no active subscribers; nothing to send")
            continue
        block = blocking_broadcast(existing, target_date, lang, segments[lang], general, today)
        if block:
            print(
                f"[{lang}] already sent today: broadcast {block.get('id')} "
                f"\"{block.get('name')}\" ({block.get('status')}); not sending again"
            )
            continue
        name = broadcast_name(target_date, lang, subject)
        if dry_run:
            print(f"[{lang}] dry run: would send \"{subject}\" to {counts[lang]} subscriber(s) in segment {segments[lang]}")
            continue
        broadcast_id = create_broadcast(key, segments[lang], lang, name, subject, html, text, preview)
        print(f"[{lang}] sent broadcast {broadcast_id} \"{subject}\" to {counts[lang]} subscriber(s)")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sync-only", action="store_true")
    group.add_argument("--send", action="store_true")
    group.add_argument("--preview", metavar="PATH", help="write the rendered HTML (and .txt) email and do not call Resend")
    parser.add_argument("--date", metavar="YYYY-MM-DD", help="edition date; default is the newest edition's date")
    parser.add_argument("--lang", choices=LANGS, default=DEFAULT_LANG, help="language for --preview")
    parser.add_argument("--dry-run", action="store_true", help="with --send: sync and check, but create no broadcast")
    args = parser.parse_args(argv)
    if args.preview:
        write_preview(args.preview, args.date, args.lang)
        return 0
    key = env("RESEND_API_KEY")
    general = env("RESEND_AUDIENCE_ID") or DEFAULT_AUDIENCE
    if not key:
        print("RESEND_API_KEY is unset; skipping.")
        return 0
    try:
        counts = sync(key, general)
        if args.send:
            send(key, general, args.date, counts, args.dry_run)
    except Exception as exc:
        print(f"resend {'send' if args.send else 'sync'} failed: {exc}", file=sys.stderr)
        return 1 if args.send else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
