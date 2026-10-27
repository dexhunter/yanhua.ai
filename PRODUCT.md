# Product

<!-- impeccable:product-schema 1 -->

<!-- Product facts are taken from the repository and from the brief for this change. No separate interview round was available in this session. -->

## Platform

web

## Users

Researchers reading a bilingual daily on recursive self-improvement and agent harness search. They arrive to understand one paper, repo, or post at a time: a conclusion they can finish, then the problem, the mechanism, and numbers they can check. Simplified Chinese is the default reading. English is the same edition, one toggle away.

## Product Purpose

演化日报 (Yanhua Daily) publishes that daily at [yanhua.ai](https://yanhua.ai). A card is the unit of reading. Success is a conclusion a researcher can finish, with a path to the paper, repository, or post, plus an open feed and an email digest of the day's editions.

## Positioning

The card leads with one human-readable conclusion, then sets the problem, the mechanism, and the checkable numbers underneath. A neighboring paper list or social feed could not truthfully copy that order and still be this daily.

## Operating Context

The site is static files. GitHub Pages serves the repository root. `CNAME` is `yanhua.ai`. Source of an edition is `data/digests.json`, rebuilt by `scripts/update_digest.py` into `data/digests.js`, `feed.xml`, and `feed.json`.

The site updates twice a day, at 09:00 and 18:00 UTC+0. The morning and evening editions are combined into the evening daily email. Mail goes out from the newsletter script in GitHub Actions. The in-page subscribe form posts `{email, lang, source}` to `https://subscribe.yanhua.ai`. There is no user account.

Reading has two modes. The reader lists editions as a column. Flash cards show the conclusion and the numbers on the front and the problem and mechanism on the back. `Space` or `Enter` flips a card. `J` / `K` or `←` / `→` move between cards.

## Capabilities and Constraints

- Bilingual cards (zh default, en toggle), edition and topic filters, and search across title, arXiv id, author, and handle.
- Every card ends on a source link: paper, repository, or post.
- Publication counts on the stats strip and in the stats dialog are calculated from the digest: total cards, editions, and papers indexed (an item with an arXiv id or a paper URL). Visitor, view, and subscriber counts stay in the stats dialog; they come from the public counter and the Resend audience, not from an account.
- No sign-in. The site does not mark cards read and does not bookmark them. Those controls and the All / Unseen / Saved filter are out of the product.
- Subscribe, RSS (`/feed.xml`), and JSON Feed (`/feed.json`) are the ways to follow new editions.
- `RESEND_API_KEY` stays on the worker and in GitHub Actions. It is not in the static site.

## Brand Commitments

The name is 演化日报 / Yanhua Daily. The domain is yanhua.ai. The masthead mark is the RSI badge. The voice is a research daily: a conclusion in plain language, then the evidence, in Chinese first.

## Evidence on Hand

- `data/digests.json` and `data/digests.js`: the edition archive the page reads.
- `feed.xml` and `feed.json`: the same cards as feeds.
- `README.md`: how to append an edition and how subscribe is wired.
- `favicon.svg`: the mark.

Do not invent subscriber quotes, benchmarks, or a second product name.

## Product Principles

- The conclusion comes first, and it stays checkable against a paper, a repository, or a post.
- Chinese is the default reading. English is the same card, not a second publication.
- There is no account, so there is no private reading state on the card.
- Two UTC editions a day fold into one evening email. The page and the digest tell the same schedule.
- A card that cannot point at a source does not ship.

## Accessibility & Inclusion

The page is a document: a skip link, a real heading order, and keyboard controls for the card deck (`Space` / `Enter` to flip, `J` / `K` or arrow keys to move). Color scheme follows the system and can be pinned. Reduced motion drops the card flip. Body text stays in a reading face on a warm paper ground. No separate conformance target was set beyond those commitments.
