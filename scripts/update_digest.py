#!/usr/bin/env python3
"""Build and extend the Yanhua daily digest.

Source of truth: data/digests.json
Regenerates:     data/digests.js, feed.xml, feed.json

Usage
-----
  python3 scripts/update_digest.py build
  python3 scripts/update_digest.py check
  python3 scripts/update_digest.py append path/to/edition.json

An edition file looks like:

{
  "edition": {
    "id": "2026-10-28-evening",
    "date": "2026-10-28",
    "slot": "evening",
    "label": {"zh": "2026-10-28 晚间版", "en": "28 Oct 2026 · Evening"}
  },
  "items": [
    {
      "id": "unique-slug",
      "edition": "2026-10-28-evening",
      "tags": ["harness-search"],
      "title": {"zh": "……", "en": "……"},
      "what": {"zh": "……", "en": "……"},
      "how": {"zh": "……", "en": "……"},
      "why": {"zh": "……", "en": "……"},
      "metric": {"zh": "……", "en": "……"},
      "pills": [{"zh": "指标", "en": "Metric", "value": "1.0", "tone": "up"}],
      "arxiv": "2610.00000",
      "authors": "Name et al.",
      "handle": "@someone",
      "links": [{"zh": "论文", "en": "Paper", "url": "https://arxiv.org/abs/2610.00000"}]
    }
  ]
}

slot is "morning", "evening", or "" for a single daily edition.
New editions are inserted at the front. Re-appending an existing edition
id replaces that edition's items.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "digests.json"
JS = ROOT / "data" / "digests.js"
RSS = ROOT / "feed.xml"
JSON_FEED = ROOT / "feed.json"
SITE = "https://yanhua.ai"

REQUIRED_I18N = ("title", "what", "how", "why", "metric")
SLOTS = {"morning": (9, 0), "evening": (18, 0), "": (12, 0)}


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_json(doc: dict) -> None:
    DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def problems(doc: dict) -> list[str]:
    errors: list[str] = []
    editions = {e["id"] for e in doc.get("editions", [])}
    seen: set[str] = set()
    if not doc.get("editions"):
        errors.append("no editions")
    for item in doc.get("items", []):
        ident = item.get("id", "")
        if not ident:
            errors.append("item missing id")
            continue
        if ident in seen:
            errors.append(f"duplicate id {ident}")
        seen.add(ident)
        if item.get("edition") not in editions:
            errors.append(f"{ident}: unknown edition {item.get('edition')}")
        for key in REQUIRED_I18N:
            block = item.get(key)
            if not isinstance(block, dict) or not str(block.get("zh", "")).strip() or not str(block.get("en", "")).strip():
                errors.append(f"{ident}: missing zh/en for {key}")
        if not item.get("tags"):
            errors.append(f"{ident}: no tags")
    return errors


def edition_stamp(edition: dict, index: int) -> datetime:
    hour, minute = SLOTS.get(edition.get("slot") or "", (12, 0))
    year, month, day = (int(part) for part in edition["date"].split("-"))
    return datetime(year, month, day, hour, minute + index, tzinfo=timezone.utc)


def item_html(item: dict) -> str:
    def para(text: str) -> str:
        return "".join(f"<p>{escape(part.strip())}</p>" for part in text.split("\n\n") if part.strip())

    zh = (
        f"<p><strong>问题与定位</strong> {escape(item['what']['zh'])}</p>"
        f"<p><strong>核心机制</strong> {escape(item['how']['zh'])}</p>"
        f"<p><strong>结论</strong> {escape(item['why']['zh'])}</p>"
    )
    en = (
        "<hr/>"
        f"{para(item['what']['en'])}{para(item['how']['en'])}{para(item['why']['en'])}"
    )
    return zh + en


def write_js(doc: dict) -> None:
    payload = json.dumps(doc, ensure_ascii=False, indent=2)
    JS.write_text(f"window.YANHUA_DIGESTS = {payload};\n", encoding="utf-8")


def write_feeds(doc: dict) -> None:
    by_edition = {e["id"]: e for e in doc["editions"]}
    counts: dict[str, int] = {}
    rss_items: list[str] = []
    json_items: list[dict] = []
    newest: datetime | None = None

    for item in doc["items"]:
        edition = by_edition[item["edition"]]
        index = counts.get(edition["id"], 0)
        counts[edition["id"]] = index + 1
        stamp = edition_stamp(edition, index)
        newest = stamp if newest is None or stamp > newest else newest
        link = f"{SITE}/#{item['id']}"
        title = f"{item['title']['zh']} / {item['title']['en']}"
        description = " ".join(
            [item["what"]["zh"], item["how"]["zh"], item["why"]["zh"]]
        )
        content = item_html(item)
        rss_items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{escape(title)}</title>",
                    f"      <link>{escape(link)}</link>",
                    f"      <guid isPermaLink=\"true\">{escape(link)}</guid>",
                    f"      <pubDate>{format_datetime(stamp)}</pubDate>",
                    f"      <category>{escape(edition['label']['zh'])}</category>",
                    f"      <description>{escape(description)}</description>",
                    f"      <content:encoded><![CDATA[{content}]]></content:encoded>",
                    "    </item>",
                ]
            )
        )
        json_items.append(
            {
                "id": link,
                "url": link,
                "title": title,
                "summary": description,
                "content_html": content,
                "date_published": stamp.isoformat(),
                "tags": item.get("tags", []),
                "language": "zh-Hans",
            }
        )

    updated = newest or datetime.now(timezone.utc)
    channel_title = "演化日报 · Yanhua RSI & Harness Search"
    channel_desc = "递归自我改进与智能体框架搜索日报。Recursive self-improvement and agent harness search, in Chinese and English."
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{escape(channel_title)}</title>
    <link>{SITE}/</link>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>{escape(channel_desc)}</description>
    <language>zh-Hans</language>
    <lastBuildDate>{format_datetime(updated)}</lastBuildDate>
{chr(10).join(rss_items)}
  </channel>
</rss>
"""
    RSS.write_text(rss, encoding="utf-8")
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": channel_title,
        "home_page_url": f"{SITE}/",
        "feed_url": f"{SITE}/feed.json",
        "description": channel_desc,
        "language": "zh-Hans",
        "items": json_items,
    }
    JSON_FEED.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> int:
    doc = load()
    found = problems(doc)
    if found:
        print("\n".join(found), file=sys.stderr)
        return 1
    write_js(doc)
    write_feeds(doc)
    print(f"built {len(doc['items'])} cards, {len(doc['editions'])} editions")
    return 0


def append(path: Path) -> int:
    doc = load()
    patch = json.loads(path.read_text(encoding="utf-8"))
    edition = patch["edition"]
    items = patch["items"]
    for item in items:
        item["edition"] = edition["id"]
    doc["editions"] = [e for e in doc["editions"] if e["id"] != edition["id"]]
    doc["editions"].insert(0, edition)
    doc["items"] = [item for item in doc["items"] if item.get("edition") != edition["id"]]
    doc["items"] = list(items) + doc["items"]
    found = problems(doc)
    if found:
        print("\n".join(found), file=sys.stderr)
        return 1
    save_json(doc)
    return build()


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"build", "check", "append"}:
        print(__doc__)
        return 2
    if argv[1] == "check":
        found = problems(load())
        if found:
            print("\n".join(found), file=sys.stderr)
            return 1
        print("ok")
        return 0
    if argv[1] == "build":
        return build()
    if len(argv) < 3:
        print("append needs a path to an edition json file", file=sys.stderr)
        return 2
    return append(Path(argv[2]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
