#!/usr/bin/env python3
"""Sync GitHub subscribe issues into Resend, and optionally send the latest edition.

yanhua.ai is a static site, so this runs in GitHub Actions where
RESEND_API_KEY stays in a repo secret (process.env / os.environ).
The General audience is the default and matches data/config.js
resendAudienceId. Set RESEND_AUDIENCE_ID only to override it. A legacy
audience id still works through /audiences/<id>/contacts when the
segment call fails.

  python3 scripts/send_newsletter_resend.py --sync-only
  python3 scripts/send_newsletter_resend.py --send

--sync-only adds label:subscribe issue emails to the segment and does
not send mail. --send does that sync, then creates a Resend broadcast
for the newest edition. The sender is
演化日报 · Yanhua Daily <digest@yanhua.ai> once domain
de1ea356-1c37-419f-bffa-be649f64b080 verifies, and onboarding@resend.dev
until then. If RESEND_API_KEY is missing the script exits 0 so a Pages
deploy is not marked failed.
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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "digests.json"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
API = "https://api.resend.com"
DEFAULT_AUDIENCE = "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003"
DEFAULT_FROM = "演化日报 · Yanhua Daily <digest@yanhua.ai>"
FALLBACK_FROM = "onboarding@resend.dev"


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


def latest_edition_html() -> tuple[str, str]:
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    edition = doc["editions"][0]
    items = [item for item in doc["items"] if item.get("edition") == edition["id"]]
    label = edition["label"]["zh"]
    blocks = [
        "<p>演化日报 / Yanhua Daily</p>",
        f"<h1>{html_escape(label)}</h1>",
    ]
    for item in items:
        blocks.append("<article>")
        blocks.append(f"<h2>{html_escape(item['title']['zh'])}</h2>")
        blocks.append(f"<p><strong>核心结论</strong> {html_escape(item['why']['zh'])}</p>")
        blocks.append(f"<p>{html_escape(item['why']['en'])}</p>")
        blocks.append("</article>")
    blocks.append('<p><a href="https://yanhua.ai/">yanhua.ai</a></p>')
    blocks.append("<p>{{{RESEND_UNSUBSCRIBE_URL}}}</p>")
    subject = f"演化日报 · {label}"
    return subject, "\n".join(blocks)


def html_escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


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


def send(key: str, segment: str) -> None:
    subject, html = latest_edition_html()
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
    args = parser.parse_args(argv)
    key = env("RESEND_API_KEY")
    segment = env("RESEND_AUDIENCE_ID") or DEFAULT_AUDIENCE
    if not key:
        print("RESEND_API_KEY is unset; skipping.")
        return 0
    try:
        sync(key, segment)
        if args.send:
            send(key, segment)
    except Exception as exc:
        print(f"resend sync failed: {exc}", file=sys.stderr)
        return 1 if args.send else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
