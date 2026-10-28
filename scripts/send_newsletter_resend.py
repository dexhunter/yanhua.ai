#!/usr/bin/env python3
"""Sync GitHub subscribe issues into Resend, and optionally send a daily digest.

yanhua.ai is a static site, so this runs in GitHub Actions where
RESEND_API_KEY stays in a repo secret (process.env / os.environ).
The General audience is the default and matches data/config.js
resendAudienceId. Set RESEND_AUDIENCE_ID only to override it. A legacy
audience id still works through /audiences/<id>/contacts when the
segment call fails.

  python3 scripts/send_newsletter_resend.py --sync-only
  python3 scripts/send_newsletter_resend.py --send
  python3 scripts/send_newsletter_resend.py --preview /tmp/daily_email_preview.html
  python3 scripts/send_newsletter_resend.py --send --date 2026-10-27

--sync-only adds label:subscribe issue emails to the segment and does
not send mail. --send does that sync, then creates a Resend broadcast
for that day's single edition. The date
defaults to the newest edition's date. --preview writes that same HTML
and does not call Resend. The sender is
演化日报 · Yanhua Daily <digest@yanhua.ai> once domain
de1ea356-1c37-419f-bffa-be649f64b080 verifies, and onboarding@resend.dev
until then. If RESEND_API_KEY is missing, --sync-only and --send exit 0
so a Pages deploy is not marked failed. --preview does not need the key.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_digest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "digests.json"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
API = "https://api.resend.com"
DEFAULT_AUDIENCE = "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003"
DEFAULT_FROM = "演化日报 · Yanhua Daily <digest@yanhua.ai>"
FALLBACK_FROM = "onboarding@resend.dev"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLOT_ORDER = {"morning": 0, "": 1, "evening": 2}
SLOT_HEADING = {
    "morning": "早间版 · Morning Edition",
    "evening": "晚间版 · Evening Edition",
    "": "当日 · Daily Edition",
}
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Songti SC','Noto Serif SC',serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Noto Sans SC','Microsoft YaHei',sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SITE = "https://yanhua.ai/"


def env(name: str) -> str:
    return os.environ.get(name, "").strip()


def request(method: str, url: str, payload: dict | None = None, token: str = "") -> tuple[int, dict | list | str]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json", "User-Agent": "yanhua-digest"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body: dict | list | str = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = raw[:500]
        return exc.code, body


def github_subscribe_emails() -> list[str]:
    repo = env("GITHUB_REPOSITORY") or "dexhunter/yanhua.ai"
    token = env("GH_TOKEN") or env("GITHUB_TOKEN")
    found: list[str] = []
    seen: set[str] = set()
    for page in range(1, 6):
        url = f"https://api.github.com/repos/{repo}/issues?labels=subscribe&state=all&per_page=100&page={page}"
        status, body = request("GET", url, token=token)
        if status == 401 or status == 403 or status == 404:
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
            for email in EMAIL_RE.findall(text):
                key = email.lower()
                if key not in seen:
                    seen.add(key)
                    found.append(email)
        if len(body) < 100:
            break
    return found


def add_contact(key: str, segment: str, email: str) -> None:
    status, _body = request("POST", f"{API}/contacts", {
        "email": email,
        "unsubscribed": False,
        "segments": [{"id": segment}],
    }, token=key)
    if status in {200, 201, 409}:
        return
    legacy, _legacy_body = request(
        "POST",
        f"{API}/audiences/{urllib.parse.quote(segment)}/contacts",
        {"email": email, "unsubscribed": False},
        token=key,
    )
    if legacy not in {200, 201, 409}:
        raise RuntimeError(f"could not add a contact ({status}, legacy {legacy})")


def sync(key: str, segment: str) -> int:
    emails = github_subscribe_emails()
    for email in emails:
        add_contact(key, segment, email)
    print(f"synced {len(emails)} subscribe-issue address(es) into Resend")
    return len(emails)


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
    if isinstance(value, dict):
        return str(value.get(lang) or value.get("zh") or value.get("en") or "")
    return str(value or "")


def linked(text: str, item: dict) -> str:
    """linkify() already escapes text and skips PR@1, pass@1, and Best@1."""
    html = update_digest.linkify(text, item)
    return html.replace(
        "<a ",
        '<a style="color:#b02a24;text-decoration:underline;" ',
    )


def day_summary(target_date: str, editions: list[dict], total: int) -> str:
    names: list[str] = []
    slots = {edition.get("slot") or "" for edition in editions}
    if "morning" in slots:
        names.append("早间版")
    if "evening" in slots:
        names.append("晚间版")
    if names:
        inner = " + ".join(names) + f" · 共 {total} 篇"
    else:
        inner = f"共 {total} 篇"
    return f"{target_date} 每日合辑（{inner}）"


def subject_for(target_date: str, total: int) -> str:
    return f"演化日报 · {target_date} 每日合辑 ({total} 篇) | Yanhua Daily Digest"


def pill_html(pill: dict) -> str:
    value = pill.get("value")
    zh_value = text_of(value, "zh")
    en_value = text_of(value, "en") if isinstance(value, dict) else ""
    zh_label = str(pill.get("zh") or pill.get("label") or "")
    en_label = str(pill.get("en") or "")
    tone = str(pill.get("tone") or "flat")
    color = {"up": "#2c6b45", "down": "#b02a24"}.get(tone, "#181412")
    bits = [
        f'<b style="display:block;font-family:{MONO};font-size:14px;line-height:1.35;color:{color};">{escape(zh_value)}</b>'
    ]
    if en_value and en_value != zh_value:
        bits.append(
            f'<span style="display:block;font-family:{MONO};font-size:12px;line-height:1.35;color:#5e564c;">{escape(en_value)}</span>'
        )
    label = f'<span style="display:block;margin-top:3px;font-family:{SANS};font-size:11px;line-height:1.35;color:#6b6258;">{escape(zh_label)}</span>'
    if en_label and en_label != zh_label:
        label += f'<span style="display:block;font-family:{SANS};font-size:11px;line-height:1.35;color:#8a8074;">{escape(en_label)}</span>'
    bits.append(label)
    inner = "".join(bits)
    return (
        '<span style="display:inline-block;margin:0 8px 8px 0;padding:8px 10px;'
        "border:1px solid #e3dacb;border-radius:8px;background:#f4efe6;vertical-align:top;\">"
        f"{inner}</span>"
    )


def byline_html(item: dict) -> str:
    bits: list[str] = []
    arxiv = str(item.get("arxiv") or "").strip()
    if arxiv:
        href = escape(f"https://arxiv.org/abs/{arxiv}", quote=True)
        bits.append(
            f'<a href="{href}" style="color:#b02a24;text-decoration:none;border:1px solid #e3dacb;'
            f'border-radius:8px;padding:2px 7px;background:#f4efe6;">arXiv:{escape(arxiv)}</a>'
        )
    authors = str(item.get("authors") or "").strip()
    if authors:
        bits.append(escape(authors))
    handle = str(item.get("handle") or "").strip()
    profiles = profile_html(handle)
    if profiles:
        bits.append(profiles)
    if not bits:
        return ""
    return (
        f'<p style="margin:8px 0 0;font-family:{SANS};font-size:13px;line-height:1.6;color:#5e564c;">'
        + " · ".join(bits)
        + "</p>"
    )


def prose_block(kicker: str, zh_html: str, en_html: str) -> str:
    return (
        f'<p style="margin:16px 0 6px;font-family:{SANS};font-size:11px;line-height:1.4;'
        f'letter-spacing:0.08em;text-transform:uppercase;color:#b02a24;font-weight:700;">{escape(kicker)}</p>'
        f'<p style="margin:0 0 6px;font-family:{SANS};font-size:15px;line-height:1.65;color:#181412;">{zh_html}</p>'
        f'<p style="margin:0;font-family:{SANS};font-size:14px;line-height:1.6;color:#5e564c;">{en_html}</p>'
    )


def profile_html(handle: str) -> str:
    parts: list[str] = []
    for match in update_digest.HANDLE_RE.finditer(handle):
        name = match.group(1)
        href = escape(f"https://x.com/{name}", quote=True)
        parts.append(
            f'<a href="{href}" style="color:#b02a24;text-decoration:underline;">@{escape(name)}</a>'
        )
    return " · ".join(parts)


def source_html(item: dict) -> str:
    links = []
    for entry in update_digest.source_entries(item):
        href = escape(str(entry["url"]), quote=True)
        label = escape(str(entry["label"]))
        links.append(
            f'<a href="{href}" style="display:inline-block;margin:0 8px 8px 0;padding:6px 10px;'
            "border:1px solid #e3dacb;border-radius:8px;background:#f4efe6;color:#181412;"
            f'text-decoration:none;font-family:{SANS};font-size:13px;line-height:1.4;">{label}</a>'
        )
    if not links:
        return ""
    return (
        '<p style="margin:16px 0 0;padding-top:12px;border-top:1px solid #e3dacb;">'
        + "".join(links)
        + "</p>"
    )


def card_html(item: dict) -> str:
    item_id = escape(str(item.get("id") or ""), quote=True)
    title_zh = escape(text_of(item.get("title"), "zh"))
    title_en = escape(text_of(item.get("title"), "en"))
    pills = "".join(pill_html(pill) for pill in (item.get("pills") or []) if isinstance(pill, dict))
    pills_html = (
        f'<p style="margin:14px 0 0;font-family:{SANS};line-height:1;">{pills}</p>' if pills else ""
    )
    return f"""
<table role="presentation" id="{item_id}" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#fbf8f2" style="margin:0 0 16px;background:#fbf8f2;border:1px solid #e3dacb;border-radius:8px;">
  <tr>
    <td style="padding:20px 22px 18px;font-family:{SANS};color:#181412;">
      <h2 style="margin:0;font-family:{SERIF};font-size:22px;line-height:1.35;font-weight:600;color:#181412;">
        <a href="{SITE}/?mode=deck#{item_id}" style="color:#181412;text-decoration:none;">{title_zh}</a>
      </h2>
      <p style="margin:4px 0 0;font-family:{SERIF};font-size:15px;line-height:1.45;font-style:italic;color:#5e564c;">{title_en}</p>
      {byline_html(item)}
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f6ece8" style="margin:16px 0 0;background:#f6ece8;border:1px solid #d7b0a3;border-radius:6px;">
        <tr>
          <td style="padding:14px 16px 16px;">
            <p style="margin:0 0 8px;font-family:{SERIF};font-size:18px;font-weight:500;line-height:1.65;color:#181412;"><span style="display:inline-block;margin:0 8px 0 0;padding:2px 7px;border-radius:4px;background:#b02a24;color:#fbf8f2;font-family:{SANS};font-size:12px;font-weight:700;letter-spacing:0.04em;line-height:1.4;vertical-align:2px;">核心结论</span>{linked(text_of(item.get("why"), "zh"), item)}</p>
            <p style="margin:0;font-family:{SERIF};font-size:15px;font-weight:500;line-height:1.65;color:#5e564c;">{linked(text_of(item.get("why"), "en"), item)}</p>
          </td>
        </tr>
      </table>
      {pills_html}
      {prose_block("问题背景 · Problem", linked(text_of(item.get("what"), "zh"), item), linked(text_of(item.get("what"), "en"), item))}
      {prose_block("核心机制与实证 · How & Evidence", linked(text_of(item.get("how"), "zh"), item), linked(text_of(item.get("how"), "en"), item))}
      {source_html(item)}
    </td>
  </tr>
</table>
""".strip()


def section_html(edition: dict, items: list[dict], show_heading: bool) -> str:
    cards = "\n".join(card_html(item) for item in items)
    if not show_heading:
        return cards
    slot = edition.get("slot") or ""
    heading = SLOT_HEADING.get(slot, SLOT_HEADING[""])
    label_zh = escape(text_of(edition.get("label"), "zh"))
    label_en = escape(text_of(edition.get("label"), "en"))
    count = len(items)
    return f"""
<h2 style="margin:28px 0 12px;font-family:{SERIF};font-size:18px;line-height:1.4;font-weight:600;color:#181412;">{escape(heading)} · {count} 篇</h2>
<p style="margin:-6px 0 14px;font-family:{SANS};font-size:13px;line-height:1.5;color:#5e564c;">{label_zh} · {label_en}</p>
{cards}
""".strip()


def render_daily_email(requested_date: str | None = None) -> tuple[str, str]:
    doc = load_doc()
    target_date = resolve_date(doc, requested_date)
    editions = editions_for_date(doc, target_date)
    grouped = [(edition, items_for_edition(doc, str(edition.get("id") or ""))) for edition in editions]
    grouped = [(edition, items) for edition, items in grouped if items]
    if not grouped:
        raise SystemExit(f"no items for {target_date}")
    total = sum(len(items) for _, items in grouped)
    subject = subject_for(target_date, total)
    summary = day_summary(target_date, [edition for edition, _ in grouped], total)
    show_heading = len(grouped) > 1 or any((edition.get("slot") or "") in {"morning", "evening"} for edition, _ in grouped)
    sections = "\n".join(section_html(edition, items, show_heading) for edition, items in grouped)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(subject)}</title>
</head>
<body style="margin:0;padding:0;background:#f4efe6;color:#181412;">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#f4efe6;">{escape(summary)} · Yanhua Daily Digest</div>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f4efe6" style="background:#f4efe6;">
    <tr>
      <td align="center" style="padding:28px 12px 36px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;width:100%;">
          <tr>
            <td style="padding:0 0 18px;border-bottom:3px solid #b02a24;">
              <p style="margin:0;font-family:{SERIF};font-size:28px;line-height:1.25;font-weight:600;color:#181412;">演化日报 · YANHUA.AI</p>
              <p style="margin:8px 0 0;font-family:{SANS};font-size:14px;line-height:1.55;color:#5e564c;">递归自我改进与智能体框架搜索 · Recursive Self-Improvement &amp; Agent Harness Search</p>
              <p style="margin:14px 0 0;">
                <span style="display:inline-block;padding:6px 10px;border:1px solid #e3dacb;border-radius:8px;background:#f6ece8;color:#b02a24;font-family:{SANS};font-size:13px;line-height:1.4;font-weight:700;">{escape(summary)}</span>
              </p>
              <p style="margin:14px 0 0;">
                <a href="{SITE}" style="display:inline-block;padding:10px 16px;border-radius:8px;background:#b02a24;color:#fbf8f2;font-family:{SANS};font-size:14px;line-height:1.4;font-weight:700;text-decoration:none;">阅读闪卡 · Read on yanhua.ai</a>
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding-top:8px;">
              {sections}
            </td>
          </tr>
          <tr>
            <td style="padding:22px 0 0;border-top:1px solid #e3dacb;font-family:{SANS};font-size:13px;line-height:1.7;color:#5e564c;">
              <p style="margin:0 0 8px;">演化日报 · Yanhua Daily · <a href="{SITE}" style="color:#b02a24;text-decoration:underline;">yanhua.ai</a></p>
              <p style="margin:0 0 8px;">
                <a href="https://yanhua.ai/feed.xml" style="color:#b02a24;text-decoration:underline;">RSS</a>
                ·
                <a href="https://yanhua.ai/feed.json" style="color:#b02a24;text-decoration:underline;">JSON Feed</a>
                ·
                <a href="{{{{{{RESEND_UNSUBSCRIBE_URL}}}}}}" style="color:#b02a24;text-decoration:underline;">退订 / Unsubscribe</a>
              </p>
              <p style="margin:0;">递归自我改进与智能体框架搜索。这封信是当天的一版，09:00 与 18:00（UTC+0）各更新一次。</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return subject, html


def write_preview(path: str, requested_date: str | None) -> None:
    subject, html = render_daily_email(requested_date)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"subject: {subject}")
    print(f"wrote {out}")


def from_addresses() -> list[str]:
    primary = env("RESEND_FROM") or DEFAULT_FROM
    fallback = env("RESEND_FROM_FALLBACK") or FALLBACK_FROM
    if fallback == primary:
        return [primary]
    return [primary, fallback]


def domain_rejected(status: int, body: dict | list | str) -> bool:
    if status not in {403, 422}:
        return False
    text = body if isinstance(body, str) else json.dumps(body)
    lowered = text.lower()
    return "domain" in lowered or "verif" in lowered or "from" in lowered


def send(key: str, segment: str, requested_date: str | None) -> None:
    subject, html = render_daily_email(requested_date)
    last_status = 0
    last_body: dict | list | str = ""
    addresses = from_addresses()
    for index, sender in enumerate(addresses):
        status, body = request("POST", f"{API}/broadcasts", {
            "segment_id": segment,
            "from": sender,
            "subject": subject,
            "html": html,
            "name": subject,
            "send": True,
        }, token=key)
        if status in {200, 201}:
            print(f"sent broadcast {subject} from {sender}")
            return
        legacy, legacy_body = request("POST", f"{API}/broadcasts", {
            "audience_id": segment,
            "from": sender,
            "subject": subject,
            "html": html,
            "name": subject,
            "send": True,
        }, token=key)
        if legacy in {200, 201}:
            print(f"sent broadcast {subject} from {sender}")
            return
        last_status, last_body = status, body
        retry = index + 1 < len(addresses) and (domain_rejected(status, body) or domain_rejected(legacy, legacy_body))
        if not retry:
            print(
                f"broadcast failed: {status} {body}; legacy {legacy} {legacy_body}",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(f"sender {sender} is not verified yet; trying {addresses[index + 1]}")
    print(f"broadcast failed: {last_status} {last_body}", file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sync-only", action="store_true")
    group.add_argument("--send", action="store_true")
    group.add_argument("--preview", metavar="PATH", help="write the rendered HTML email and do not call Resend")
    parser.add_argument("--date", metavar="YYYY-MM-DD", help="edition date; default is the newest edition's date")
    args = parser.parse_args(argv)
    if args.preview:
        write_preview(args.preview, args.date)
        return 0
    key = env("RESEND_API_KEY")
    segment = env("RESEND_AUDIENCE_ID") or DEFAULT_AUDIENCE
    if not key:
        print("RESEND_API_KEY is unset; skipping.")
        return 0
    try:
        sync(key, segment)
        if args.send:
            send(key, segment, args.date)
    except Exception as exc:
        print(f"resend sync failed: {exc}", file=sys.stderr)
        return 1 if args.send else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
