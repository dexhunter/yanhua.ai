#!/usr/bin/env python3
"""Build and extend the Yanhua daily digest.

Source of truth: data/digests.json
Regenerates:     data/digests.js, feed.xml, feed.json
                 and the ?v= cache token on local assets in index.html

Usage
-----
  python3 scripts/update_digest.py build
  python3 scripts/update_digest.py check
  python3 scripts/update_digest.py append path/to/edition.json

An edition file looks like:

{
  "edition": {
    "id": "2026-10-28",
    "date": "2026-10-28",
    "slot": "",
    "label": {"zh": "2026-10-28", "en": "28 Oct 2026"}
  },
  "items": [
    {
      "id": "unique-slug",
      "edition": "2026-10-28",
      "tags": ["harness-search"],
      "title": {"zh": "……", "en": "……"},
      "what": {"zh": "一句问题。", "en": "One sentence on the problem."},
      "how": {"zh": "一两句机制，关键数字放这里。", "en": "One or two sentences on the mechanism and the key numbers."},
      "why": {"zh": "一句人话结论。", "en": "One human-readable sentence stating the conclusion."},
      "metric": {"zh": "……", "en": "……"},
      "pills": [{"zh": "指标", "en": "Metric", "value": "1.0", "tone": "up"}],
      "arxiv": "2610.00000",
      "authors": "Name et al.",
      "handle": "@someone",
      "links": [{"zh": "论文", "en": "Paper", "url": "https://arxiv.org/abs/2610.00000"}]
    }
  ]
}

Each calendar date is one edition. append canonicalizes the id to that
date, clears slot, and strips 早间版 / 晚间版 / Morning / Evening from
the label. A new date is inserted at the front. Appending the same date
prepends the new cards and keeps cards from earlier that day. Matching
item ids are updated in place, so a re-run is idempotent. Pass
--replace-edition to overwrite the whole date instead.

  python3 scripts/update_digest.py append path/to/edition.json
  python3 scripts/update_digest.py append path/to/edition.json --replace-edition
"""

from __future__ import annotations

import json
import re
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
INDEX = ROOT / "index.html"
SITE = "https://yanhua.ai"
ASSET_RE = re.compile(
    r'(?P<prefix>(?:href|src)=")/(?P<path>assets/app\.css|assets/app\.js|data/config\.js|data/digests\.js)(?:\?v=[^"]*)?"'
)

REQUIRED_I18N = ("title", "what", "how", "why", "metric")
SENTENCE_BOUNDS = {"what": (1, 1), "how": (1, 2), "why": (1, 1)}
SLOTS = {"morning": (9, 0), "evening": (18, 0), "": (12, 0)}
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLOT_LABEL_RE = re.compile(r"早间版|晚间版|\bMorning\b|\bEvening\b")
# A real @mention: not glued to a metric or email (PR@1, pass@1, user@domain.com),
# not a bare @1, and not followed by .tld.
HANDLE_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])@(?=[A-Za-z0-9_]*[A-Za-z_])([A-Za-z0-9_]{1,15})(?![A-Za-z0-9_])(?!\.[A-Za-z0-9_])"
)
X_URL_RE = re.compile(
    r"^https?://(?:www\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})(?:/status/(\d+))?/?(?:[?#].*)?$",
    re.IGNORECASE,
)
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)
GITHUB_RE = re.compile(r"^https?://(?:www\.)?github\.com/([^/#?\s]+)/([^/#?\s]+)", re.IGNORECASE)
PAPER_ICON = (
    '<svg class="source-ico" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" focusable="false">'
    '<path d="M3.2 1.7h5l2.6 2.6v8H3.2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M8.1 1.8v2.6h2.6M5 7.2h4M5 9.3h3.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
REPO_ICON = (
    '<svg class="source-ico" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" focusable="false">'
    '<path d="M5 4.1 2.5 7 5 9.9M9 4.1 11.5 7 9 9.9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
X_ICON = (
    '<svg class="source-ico" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M14.06 3h3.16l-6.9 7.89L18.4 21h-3.2l-5.02-6.56L5.3 21H2.13l7.38-8.44L2.7 3h3.28l4.54 6.01L14.06 3Zm-1.11 16.2h1.75L7.16 4.68H5.3l7.65 14.52Z"/>'
    "</svg>"
)
SOURCE_ICONS = {"paper": PAPER_ICON, "repo": REPO_ICON, "x": X_ICON}
# A sentence end is CJK terminal punctuation, or . ! ? that is not the dot inside a decimal.
SENT_RE = re.compile(r"(?<!\d)[.!?](?!\d)|[。！？]|(?<=\d)[.!?](?!\d)(?=\s|$)")


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_json(doc: dict) -> None:
    DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sentence_count(text: str) -> int:
    return len(SENT_RE.findall(text.strip()))


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
                continue
            bounds = SENTENCE_BOUNDS.get(key)
            if not bounds:
                continue
            lo, hi = bounds
            for lang in ("zh", "en"):
                count = sentence_count(str(block[lang]))
                if not lo <= count <= hi:
                    errors.append(f"{ident}: {key}.{lang} has {count} sentences, want {lo}-{hi}")
        if not item.get("tags"):
            errors.append(f"{ident}: no tags")
        if not source_entries(item):
            errors.append(f"{ident}: no paper, repo, post, or other source link")
    return errors


def edition_stamp(edition: dict, index: int) -> datetime:
    hour, minute = SLOTS.get(edition.get("slot") or "", (12, 0))
    year, month, day = (int(part) for part in edition["date"].split("-"))
    return datetime(year, month, day, hour, minute + index, tzinfo=timezone.utc)


def handle_url_map(item: dict) -> dict[str, str]:
    found: dict[str, str] = {}
    for link in item.get("links") or []:
        match = X_URL_RE.match(str(link.get("url") or ""))
        if not match:
            continue
        key = match.group(1).lower()
        url = str(link["url"])
        prev = found.get(key)
        if prev is None or (match.group(2) and "/status/" not in prev):
            found[key] = url
    return found


def linkify(text: str, item: dict) -> str:
    urls = handle_url_map(item)

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        href = urls.get(name.lower()) or f"https://x.com/{name}"
        return f'<a href="{escape(href)}" target="_blank" rel="noopener noreferrer">@{escape(name)}</a>'

    return HANDLE_RE.sub(repl, escape(text))


def source_entries(item: dict) -> list[dict]:
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
    docs: list[dict] = []
    posts: dict[str, dict] = {}
    for link in raw:
        match = X_URL_RE.match(str(link["url"]))
        if match:
            key = match.group(1).lower()
            prev = posts.get(key)
            if prev is None or (match.group(2) and "/status/" not in str(prev["url"])):
                posts[key] = {"handle": match.group(1), "url": link["url"]}
            continue
        docs.append(link)
    for match in HANDLE_RE.finditer(str(item.get("handle") or "")):
        key = match.group(1).lower()
        if key not in posts:
            posts[key] = {"handle": match.group(1), "url": f"https://x.com/{match.group(1)}"}
    entries: list[dict] = []
    for link in docs:
        url = str(link["url"])
        ax = ARXIV_RE.search(url)
        gh = GITHUB_RE.match(url)
        if ax:
            ident = ax.group(1)
            label = f"论文 arXiv:{ident}"
            kind = "paper"
        elif gh:
            slug = f"{gh.group(1)}/{gh.group(2).removesuffix('.git')}"
            label = f"GitHub: {slug}"
            kind = "repo"
        else:
            label = str(link.get("zh") or link.get("en") or "原文")
            kind = "paper"
        entries.append({"url": url, "label": label, "icon": kind})
    for post in posts.values():
        entries.append({"url": post["url"], "label": f"@{post['handle']}", "icon": "x"})
    return entries


def source_html(item: dict) -> str:
    parts = [
        (
            f'<a class="source-link" href="{escape(entry["url"])}" target="_blank" rel="noopener noreferrer">'
            f'{SOURCE_ICONS[entry["icon"]]}{escape(entry["label"])}</a>'
        )
        for entry in source_entries(item)
    ]
    if not parts:
        return ""
    return "<p>" + " ".join(parts) + "</p>"


def item_html(item: dict) -> str:
    zh = (
        f"<p><strong>核心结论</strong> {linkify(item['why']['zh'], item)}</p>"
        f"<p><strong>问题背景</strong> {linkify(item['what']['zh'], item)}</p>"
        f"<p><strong>核心机制与实证</strong> {linkify(item['how']['zh'], item)}</p>"
    )
    en = (
        "<hr/>"
        f"<p><strong>Takeaway</strong> {linkify(item['why']['en'], item)}</p>"
        f"<p><strong>Problem</strong> {linkify(item['what']['en'], item)}</p>"
        f"<p><strong>How &amp; Evidence</strong> {linkify(item['how']['en'], item)}</p>"
    )
    return zh + en + source_html(item)


def cache_token(doc: dict) -> str:
    edition = ""
    editions = doc.get("editions") or []
    if editions and isinstance(editions[0], dict):
        edition = re.sub(r"[^A-Za-z0-9._-]", "", str(editions[0].get("id") or ""))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{edition}-{stamp}" if edition else stamp


def bust_asset_urls(doc: dict) -> None:
    if not INDEX.is_file():
        return
    token = cache_token(doc)
    html = INDEX.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        return f'{match.group("prefix")}/{match.group("path")}?v={token}"'

    updated, count = ASSET_RE.subn(repl, html)
    if count and updated != html:
        INDEX.write_text(updated, encoding="utf-8")


def write_js(doc: dict) -> None:
    payload = json.dumps(doc, ensure_ascii=False, indent=2)
    JS.write_text(f"window.YANHUA_DIGESTS = {payload};\n", encoding="utf-8")
    bust_asset_urls(doc)


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
        description = item["why"]["zh"]
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


def english_date(iso: str) -> str:
    year, month, day = (int(part) for part in iso.split("-"))
    return f"{day} {MONTHS[month - 1]} {year}"


def canonical_edition(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise SystemExit("edition must be an object")
    edition = dict(raw)
    raw_id = str(edition.get("id") or "").strip()
    date = str(edition.get("date") or "").strip()
    if not date:
        match = DATE_RE.match(raw_id)
        date = match.group(0) if match else ""
    if not DATE_RE.fullmatch(date):
        raise SystemExit(f"edition date must be YYYY-MM-DD, got {date or raw_id!r}")
    label = edition.get("label") if isinstance(edition.get("label"), dict) else {}
    zh = str(label.get("zh") or "").strip()
    en = str(label.get("en") or "").strip()
    if not zh or not en or SLOT_LABEL_RE.search(zh) or SLOT_LABEL_RE.search(en):
        label = {"zh": date, "en": english_date(date)}
    else:
        label = {"zh": zh, "en": en}
    edition["id"] = date
    edition["date"] = date
    edition["slot"] = ""
    edition["label"] = label
    return edition


def edition_matches(existing: dict, edition: dict) -> bool:
    existing_id = str(existing.get("id") or "")
    existing_date = str(existing.get("date") or "")
    date = edition["date"]
    return existing_id == edition["id"] or existing_date == date or existing_id.startswith(date + "-")


def merge_items(doc: dict, edition: dict, incoming: list[dict], replace: bool) -> None:
    old_ids = {str(existing.get("id") or "") for existing in doc.get("editions") or [] if edition_matches(existing, edition)}
    old_ids.add(edition["id"])
    seen: set[str] = set()
    prepared: list[dict] = []
    for item in incoming:
        if not isinstance(item, dict) or not str(item.get("id") or "").strip():
            raise SystemExit("every appended item needs an id")
        item_id = str(item["id"])
        if item_id in seen:
            raise SystemExit(f"duplicate id in append file: {item_id}")
        seen.add(item_id)
        item["edition"] = edition["id"]
        prepared.append(item)

    editions: list[dict] = []
    placed = False
    for existing in doc.get("editions") or []:
        if edition_matches(existing, edition):
            if not placed:
                editions.append(edition)
                placed = True
            continue
        editions.append(existing)
    if not placed:
        editions.insert(0, edition)
    doc["editions"] = editions

    remaining = [item for item in doc.get("items") or [] if str(item.get("id") or "") not in seen]
    result: list[dict] = []
    pending: list[dict] = []
    inserted = False

    def flush() -> None:
        nonlocal inserted
        if inserted:
            return
        result.extend(prepared)
        if not replace:
            result.extend(pending)
        inserted = True

    for item in remaining:
        belongs = str(item.get("edition") or "") in old_ids
        if belongs and replace:
            flush()
            continue
        if belongs:
            item["edition"] = edition["id"]
            pending.append(item)
            continue
        if pending and not inserted:
            flush()
        result.append(item)
    if not inserted:
        if pending:
            flush()
        else:
            result = prepared + result
    doc["items"] = result


def append(path: Path, replace: bool = False) -> int:
    doc = load()
    patch = json.loads(path.read_text(encoding="utf-8"))
    edition = canonical_edition(patch["edition"])
    items = patch.get("items")
    if not isinstance(items, list):
        raise SystemExit("append file needs an items array")
    merge_items(doc, edition, items, replace)
    found = problems(doc)
    if found:
        print("\n".join(found), file=sys.stderr)
        return 1
    save_json(doc)
    return build()


def main(argv: list[str]) -> int:
    args = list(argv[1:])
    replace = "--replace-edition" in args
    args = [arg for arg in args if arg != "--replace-edition"]
    if not args or args[0] not in {"build", "check", "append"}:
        print(__doc__)
        return 2
    if args[0] == "check":
        found = problems(load())
        if found:
            print("\n".join(found), file=sys.stderr)
            return 1
        print("ok")
        return 0
    if args[0] == "build":
        return build()
    if len(args) != 2:
        print("append needs a path to an edition json file", file=sys.stderr)
        return 2
    return append(Path(args[1]), replace=replace)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
