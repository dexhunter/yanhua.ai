<div align="center" id="readme-top">

<a href="https://yanhua.ai"><img src="assets/banner.png" alt="演化日报 · yanhua.ai — Where agents rewrite their own harnesses" width="100%"></a>

<p align="center">
  <a href="https://yanhua.ai"><img src="https://img.shields.io/badge/Live_Site-yanhua.ai-8e2f27?style=for-the-badge" alt="Live Site"></a>
  <a href="https://yanhua.ai"><img src="https://img.shields.io/badge/Cadence-09%3A00%20%26%2018%3A00%20UTC%2B0-1b1714?style=for-the-badge" alt="09:00 &amp; 18:00 UTC+0"></a>
  <a href="https://yanhua.ai"><img src="https://img.shields.io/badge/Daily_Email-Resend%20%C2%B7%20%E6%AF%8F%E6%97%A5%E5%90%88%E8%BE%91-14633c?style=for-the-badge" alt="Resend · 每日合辑"></a>
  <a href="https://yanhua.ai/feed.xml"><img src="https://img.shields.io/badge/RSS_/_Atom-feed.xml-b85d19?style=for-the-badge" alt="RSS / Atom"></a>
  <a href="https://yanhua.ai/data/digests.json"><img src="https://img.shields.io/badge/JSON_Feed-digests.json-1e4e79?style=for-the-badge" alt="JSON Feed"></a>
</p>

[Live Reader](https://yanhua.ai) · [Flash-Card Deck](https://yanhua.ai/#deck) · [RSS Feed](https://yanhua.ai/feed.xml) · [Digest JSON](https://yanhua.ai/data/digests.json) · [简体中文](README.md)

</div>

<br>

## ❯❯ What is Yanhua Daily

**Yanhua Daily** (演化日报) is a bilingual research daily at [yanhua.ai](https://yanhua.ai). It follows agents that rewrite their own harnesses, with an edition at 09:00 and another at 18:00 UTC+0. The site defaults to Simplified Chinese. English is the same edition behind one toggle.

Each card opens with one sentence you can finish: what improved, by how much, and why the mechanism holds. The problem, the method, and the checkable numbers come after that. Sources resolve to the paper, the repository, or the original post.

GitHub Pages serves the repository root. `CNAME` is `yanhua.ai`, and `.nojekyll` keeps Pages from processing the files.

## ❯❯ Core Coverage

The daily reads papers, repositories, and posts along four lines. The on-site filters are finer: `harness-search`, `co-evolution`, `verification`, `agentic-rl`, `embodied`, and `memory-skills`. Those tags still sit inside the table below.

| **Agent Harness Search** | **Recursive Self-Improvement (RSI)** |
| --- | --- |
| Search, rewrite, and move the harness itself: prompts, tools, skills, the execution membrane, and rollbackable adapters. The weights can stay fixed. | The system uses its own runs to change how the next round works. The evolution is in the loop, not only in a single training job. |
| **Verification & Anti-Reward-Hacking** | **Self-Evolving Code & Embodied Agents** |
| The verifier stays apart from the proposer. A gap in the scorer gets exploited immediately, so the check cannot belong to the thing being optimized. | Code agents and robots turn today's failures into the next plan, skill, or recovery rule, without retraining the weights for every venue. |

## ❯❯ Three-Part Card Anatomy

<p align="center">
  <img src="assets/banner.svg" alt="Card anatomy specimen: one-sentence takeaway, tabular metrics, problem and mechanism, then arXiv, GitHub, and X" width="100%">
</p>

<p align="center"><em>How a card is read: one sentence, then a metric table, then the problem and the mechanism. Sources land on arXiv, GitHub, and X.</em></p>

A card is not a retelling of a tweet. `why`, `what`, and `how` come from reading the paper or the repository. `why` is one sentence, `what` is one sentence, and `how` is at most two.

### ❯ 1-Sentence Takeaway

The conclusion sits at the top, in `why`. It states the result and the reason in ordinary language. The metric table (`pills`) follows immediately. Figures are monospaced tabular numerals. Movement uses the site's own green and lacquer, with a tone of `up`, `down`, or `flat`. A `value` may be a string or `{ "zh", "en" }`.

### ❯ Problem & Mechanism

`what` is the problem and the setup. `how` is the mechanism and the evidence. Both have to survive a return to the source, not stop at the quote-tweet. In the reader they sit in two columns. On a flash card, the front keeps the conclusion and the numbers. The back is these two passages.

### ❯ arXiv / GitHub / X

Every card can be opened through to a paper, a repository, an article, or the original post. `arxiv` opens `https://arxiv.org/abs/…`, `repo` opens GitHub, and `handle` plus post links open X.

An `@handle` in the prose becomes a link to `https://x.com/<handle>`. Metric tokens stay text, so they are not treated as mentions: `PR@1`, `pass@1`, and `Best@1` remain as written. Email addresses and a bare `@1` are left alone too.

## ❯❯ Reading Surfaces & Feeds

### ❯ Reader Stream

Editions run down the page. The header filters by edition and topic, and searches titles, arXiv ids, authors, and handles. `?lang=zh` or `?lang=en` sets the language. The paper theme switches between `#f4efe6` and the dark sheet.

### ❯ 3D Flip Flash-Cards

Switch the header to **Deck**. The card flips on the Y axis. The front is the title, the one-sentence conclusion, and the metrics. The back is the problem and the mechanism. `Space` or `Enter` flips. `J` / `K` or `←` / `→` moves between cards. There is no account, and the browser does not store read or saved state.

### ❯ Evening Combined Email

Each evening, that day's morning and evening editions go out as one message through Resend. The sender is `演化日报 · Yanhua Daily <digest@yanhua.ai>`. There is no permanent subscribe button. Near the end of the page, a small dialog opens with `dialog.show()` in the bottom-right corner and does not cover the reading. The form `POST`s `{email, lang, source}` to [https://subscribe.yanhua.ai](https://subscribe.yanhua.ai). `RESEND_API_KEY` lives only on the Worker and in GitHub Actions.

A normal Pages deploy only syncs GitHub issues labeled `subscribe`. To send mail, run the workflow by hand and check “Email the latest edition through Resend”.

### ❯ RSS / JSON

- RSS / Atom: <https://yanhua.ai/feed.xml>
- JSON Feed: <https://yanhua.ai/feed.json>
- Raw dataset: <https://yanhua.ai/data/digests.json>

Feed entries lead with the one-sentence conclusion and linkify a safe `@handle`.

## ❯❯ Repository & CLI Workflow

The canonical dataset is `data/digests.json`. The page reads the same document as `data/digests.js`. There is no separate `digest.json` at the repository root. The Cloudflare Worker behind the subscribe dialog is `scripts/cloudflare-resend-worker.js`, deployed at `https://subscribe.yanhua.ai`.

| Path | Role |
| --- | --- |
| `data/digests.json` | Bilingual source of editions and cards |
| `data/digests.js` | The same document for the page |
| `scripts/update_digest.py` | Validate, rebuild `digests.js`, RSS, and the JSON Feed, and stamp `?v=` cache tokens on assets in `index.html` |
| `scripts/send_newsletter_resend.py` | Render the morning-plus-evening HTML and broadcast it with Resend |
| `scripts/cloudflare-resend-worker.js` | Cloudflare Worker behind the corner subscribe dialog |
| `feed.xml` / `feed.json` | Public feeds |
| `index.html` · `assets/` · `data/config.js` | Page, styles, and subscribe endpoint config |

Validate, then build:

```bash
python3 scripts/update_digest.py check && python3 scripts/update_digest.py build
```

`check` only validates. `build` validates again, then writes the page data and the feeds. Append an edition with `slot` set to `morning`, `evening`, or `""` for a single edition that day:

```bash
python3 scripts/update_digest.py append editions/2026-10-28-evening.json
```

Appending the same `id` replaces that edition. New editions are inserted at the front.

Mail:

```bash
python3 scripts/send_newsletter_resend.py --preview /tmp/daily_email_preview.html
python3 scripts/send_newsletter_resend.py --preview /tmp/daily_email_preview.html --date 2026-10-27
python3 scripts/send_newsletter_resend.py --sync-only
python3 scripts/send_newsletter_resend.py --send --date 2026-10-27
```

`--preview` writes the HTML locally, does not call Resend, and does not need a key. Without `--date`, the date is the newest edition's date. `--send` syncs the list, then broadcasts that day's morning and evening editions as one message. `--sync-only` syncs and does not send. Until the domain is verified, the sender falls back to `onboarding@resend.dev`.

<p align="center">
  <a href="#readme-top"><img src="https://img.shields.io/badge/-Back_to_top-1b1714?style=flat-square" alt="Back to top"></a>
</p>
