---
name: 演化日报
description: A bilingual research daily on warm paper, with vermilion used as a seal.
colors:
  paper: "#f4efe6"
  raised: "#fbf7f0"
  ink: "#1b1714"
  muted: "#5c5348"
  line: "#ddd4c6"
  lacquer: "#8e2f27"
  lacquer-ink: "#7a241e"
  wash: "#f6e6e1"
  good: "#14633c"
  on-lacquer: "#fffaf6"
  paper-dark: "#12110f"
  raised-dark: "#1c1b18"
  ink-dark: "#f3ecdf"
  muted-dark: "#cbbfae"
  line-dark: "#3a342c"
  lacquer-dark: "#e7b2a6"
  lacquer-ink-dark: "#f0c2b8"
  wash-dark: "#2a1d1a"
  good-dark: "#8fd0aa"
  on-lacquer-dark: "#1b1714"
typography:
  display:
    fontFamily: "Noto Serif SC, Source Han Serif SC, Songti SC, serif"
    fontSize: "clamp(2.4rem, 5vw, 3.6rem)"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Noto Serif SC, Source Han Serif SC, Songti SC, serif"
    fontSize: "1.48rem"
    fontWeight: 600
    lineHeight: 1.28
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Noto Serif SC, Source Han Serif SC, Songti SC, serif"
    fontSize: "1.15rem"
    fontWeight: 500
    lineHeight: 1.65
    letterSpacing: "normal"
  body:
    fontFamily: "Noto Sans SC, Source Han Sans SC, PingFang SC, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Noto Sans SC, Source Han Sans SC, PingFang SC, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.04em"
  mono:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "0.8rem"
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: "normal"
rounded:
  none: "0"
  badge: "0.25rem"
  source: "0.3rem"
  verdict: "0.375rem"
  window: "0.75rem"
  seal: "999px"
spacing:
  hairline: "1px"
  control-x: "0.7rem"
  control-y: "0.42rem"
  card: "1.25rem"
  shell: "1.75rem"
  column: "3rem"
  nav: "4.25rem"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.42rem 0.7rem"
  button-primary-hover:
    backgroundColor: "{colors.lacquer}"
    textColor: "{colors.on-lacquer}"
    rounded: "{rounded.none}"
    padding: "0.42rem 0.7rem"
  button-secondary:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.42rem 0.7rem"
  button-secondary-hover:
    backgroundColor: "{colors.lacquer}"
    textColor: "{colors.on-lacquer}"
    rounded: "{rounded.none}"
    padding: "0.42rem 0.7rem"
  source-link:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.source}"
    padding: "0.38rem 0.65rem"
  source-link-hover:
    backgroundColor: "{colors.wash}"
    textColor: "{colors.lacquer-ink}"
    rounded: "{rounded.source}"
    padding: "0.38rem 0.65rem"
  verdict:
    backgroundColor: "{colors.wash}"
    textColor: "{colors.ink}"
    rounded: "{rounded.verdict}"
    padding: "0.95rem 1.05rem 1.05rem"
    typography: "{typography.title}"
  search:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.55rem 0.65rem"
  chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.muted}"
    rounded: "{rounded.none}"
    padding: "0.28rem 0.1rem"
  stats-strip:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.muted}"
    rounded: "{rounded.none}"
    padding: "0.32rem 0.65rem"
---

# Design System: 演化日报

## Overview

**Creative North Star: "The Lacquer Gazette"**

演化日报 is a research daily printed on warm paper. The frame — masthead, rail, ground, and the vermilion seal — belongs to that gazette. The column inside it stays a document: a serif lead, a sans body, a measure near 68 characters, and headings that can be scanned. Vermilion is rare. It marks the seal on a conclusion, the current item in the rail, and a link the reader is about to follow.

The north star is read from the shipped interface: paper `#f4efe6`, lacquer `#8e2f27`, Noto Serif SC for the lead, Noto Sans SC for the UI. Dark scheme swaps the same roles rather than inventing a second palette. The name "The Lacquer Gazette" was not chosen in a separate interview.

Density is editorial, not dashboard. A card is one study. Metrics sit in a ledger row. Source links are the last line of the card. Flash cards use one turn, the flip, and otherwise stay still.

**Key Characteristics:**

- Warm paper ground, ink text, one vermilion used as a seal.
- Serif for the editorial subtitle, the card title, and the conclusion. Sans for the rail, labels, and body of the mechanism.
- A 1px hairline is the divider. Metrics are a row, not a stack of boxes.
- Icons are drawn at 14px. The page does not use emoji as icons.
- Nothing set smaller than 0.72rem (11.52px at a 16px root).

## Colors

The light scheme is the paper the daily is set on. The dark scheme reassigns the same roles for a dim room. Frontmatter `colors.*` entries without a `-dark` suffix are the light values. `-dark` entries are the dark scheme only.

### Primary
- **Lacquer** (`colors.lacquer`): the seal, the focus ring, the hover of a control, and the current-topic dot. In the dark scheme the same role is **Lacquer, night** (`colors.lacquer-dark`), a pale vermilion on near-black paper.
- **Lacquer ink** (`colors.lacquer-ink`): vermilion used as text and as the figure in a metric. Dark scheme: `colors.lacquer-ink-dark`.

### Secondary
- **Verified green** (`colors.good`): a metric that moved up. It is not a second brand color and does not appear in the masthead. Dark scheme: `colors.good-dark`.

### Neutral
- **Paper** (`colors.paper`): the page ground and the card surface. Dark scheme: `colors.paper-dark`.
- **Raised sheet** (`colors.raised`): nav controls, the search field, source links, and the stats strip. Dark scheme: `colors.raised-dark`.
- **Ink** (`colors.ink`): text and the primary button. Dark scheme: `colors.ink-dark`.
- **Muted ink** (`colors.muted`): secondary text, placeholders, and ledger labels. It is a warm brown, not neutral gray. Dark scheme: `colors.muted-dark`.
- **Hairline** (`colors.line`): 1px rules between sections, pills, and days. Dark scheme: `colors.line-dark`.
- **Wash** (`colors.wash`): the conclusion block only. Dark scheme: `colors.wash-dark`.
- **On lacquer** (`colors.on-lacquer`): text on a lacquer fill, including the seal and hovered buttons. Dark scheme: `colors.on-lacquer-dark`.

### Named Rules
**The Seal Rule.** Lacquer is a seal, a word, or a 1px hairline. It is not a stripe down the side of a card. A `border-left` or `border-right` thicker than 1px is not part of this system.

**The One Voice Rule.** On a card, lacquer shows up on the seal, the section labels, and the source the pointer is on. The rest of the card is ink on paper.

## Typography

**Display Font:** Noto Serif SC (with Source Han Serif SC, Songti SC, serif)
**Body Font:** Noto Sans SC (with Source Han Sans SC, PingFang SC, sans-serif)
**Label/Mono Font:** JetBrains Mono (with ui-monospace, monospace) for arXiv ids, counts, and source links

**Character:** The serif carries the sentence a person reads. The sans carries the chrome. Mono is for identifiers and numbers, not for the conclusion.

### Hierarchy
- **Brand** (600, 1.35rem): the site name in the nav. It is the only title. The editorial bar under it is one muted serif line at 0.95rem, with the stats strip on the same baseline. There is no second page title.
- **Headline** (600, 1.48rem, line-height 1.28): the card title. Edition titles sit just under that, at 1.45rem, on one baseline with the edition count.
- **Title** (500, 1.15rem, line-height 1.65): the conclusion, set as a serif lead inside the wash.
- **Body** (400, 1rem, line-height 1.5, measure 68ch): the page default. Mechanism copy is 0.95rem at line-height 1.65. English reading line-height drops from 1.75 to 1.65.
- **Label** (600, 0.75rem): rail headings, context labels, and the seal. The seal is 0.72rem, which is the floor. Rail headings may use 0.08em tracking and uppercase Latin; Chinese labels stay in the same size without forced caps.

### Named Rules
**The Floor Rule.** No `font-size` on this site is below 0.72rem. At a 16px root that is 11.52px. The seal, the ledger label, and the rail heading sit on that floor and do not go under it.

**The Serif Lead Rule.** The conclusion is the serif. UI labels beside it stay sans, small, and inline, so the sentence remains the heading of that block.

## Layout

The page is a sticky nav, then a two-column shell: a rail at `minmax(12rem, 16rem)` and a reading column at `var(--measure)` (68ch), separated by 3rem. The shell is centered. The column opens with one editorial line and the stats strip; the latest edition name is only the first edition heading. The footer is one line: the tagline on the left, RSS and JSON on the right. Below 900px the rail stacks above the column and its lists wrap. Below 640px the domain in the nav hides and the stats grid becomes one column.

Inside a card the order is fixed: title and byline, conclusion, ledger, then the two-column problem and mechanism, then the source links. The context block is separated from the conclusion by a 1px `var(--line)` rule, with more space above that rule than between a context heading and its paragraph. Flash cards keep the same order, split across the two faces, and end on the flip control plus the source links.

## Elevation & Depth

The reading column is flat. Cards in the reader are paper set off by a 1px hairline, not by a shadow. Depth shows up in two places: the flash card, which lifts with an offset shadow while it is the object in hand, and the subscribe window, which floats over the page.

### Shadow Vocabulary
- **Card in hand** (`box-shadow: 0 1px 0 rgb(28 23 18 / 5%), 0 24px 44px -28px rgb(28 23 18 / 48%)`): the flash-card sheet and modal dialogs. The dark scheme deepens the same shape.
- **Window** (`box-shadow: 0 22px 54px -12px rgb(0 0 0 / 42%), 0 4px 14px -2px rgb(0 0 0 / 18%)`): the subscribe window only.

### Named Rules
**The Flat Column Rule.** A card in the reader does not wear a shadow. If a surface needs to lift, it is the card being held (the flash card) or a window over the page.

## Shapes

Corners are mostly square, like a newspaper. The exceptions are small and named: the RSI badge at 0.25rem, a source link at 0.3rem, the conclusion wash at 0.375rem, the subscribe window at 0.75rem, and the seal, which is a pill. Rules are 1px. The focus ring is a 2px lacquer outline, offset 2px.

## Components

### Buttons
- **Shape:** square corners (0).
- **Primary:** ink fill, paper text, padding 0.42rem 0.7rem. Used for the flip control and the subscribe submit.
- **Hover / Focus:** the fill becomes lacquer and the text becomes on-lacquer. Focus uses the page's 2px lacquer outline.
- **Secondary:** raised sheet, ink text, 1px hairline. Prev and next on the deck. Disabled drops to 45% opacity.

### Chips
- **Style:** text in the rail, no box. The pressed topic adds a 0.38rem lacquer dot before the label.
- **State:** muted when idle, ink when pressed.

### Cards / Containers
- **Corner Style:** square on the reader card. The conclusion inside it is the only rounded block (0.375rem).
- **Background:** paper for the card, wash for the conclusion, raised for source links.
- **Shadow Strategy:** none on a reader card. The flash card uses the card-in-hand shadow.
- **Border:** 1px hairline around the card. The conclusion uses a 1px rule mixed from lacquer at 24% and the hairline color. No side stripe.
- **Internal Padding:** 1.25rem 1.2rem on a reader card. 1.35rem 1.3rem on a flash card.

### The conclusion
- **Style:** serif lead at 1.15rem / 500 / 1.65, on the wash. The label 一句话结论 / Key Takeaway is an inline lacquer pill, not a line above the sentence.
- **State:** the sentence is the content. It does not toggle.

### The ledger
- **Style:** one row of value plus label, tabular numbers, mono figures. Items are separated by a 1px hairline, not wrapped in boxes. Up is verified green. Down is lacquer ink.

### Source links
- **Style:** inline row at the end of the card. 14×14 icon, 0.38rem gap, 0.3rem radius, mono label. Paper and repository icons are stroked at 1.6. The X mark is a filled path.
- **Hover / Focus:** border and text shift to lacquer over 150ms, `cubic-bezier(0.22, 1, 0.36, 1)`, and the ground tints to the wash.

### Inputs / Fields
- **Style:** search and email fields are a 1px hairline on the raised sheet, square corners, lacquer caret.
- **Focus:** the page outline.
- **Error:** an invalid email turns the hairline lacquer and reveals the field error.

### Navigation
- **Style:** a sticky bar on paper with a 1px bottom rule. The wordmark is serif. RSI is a mono badge. Mode and language are a segmented control: pressed segment is ink on paper.
- **Mobile:** the rail becomes a wrapping row under the nav. The theme control keeps its icon and hides the word.

### Stats
- **Style:** a mono strip of three publication counts — cards, editions, papers indexed. The dialog adds visitors, views, and subscribers, then repeats the publication counts, then one sentence on the 09:00 and 18:00 UTC+0 cadence.

## Do's and Don'ts

### Do:
- **Do** set the conclusion as a serif lead on the wash, with the seal inline at 0.72rem.
- **Do** separate the problem and the mechanism from the conclusion with a 1px hairline and more space above the headings than below them.
- **Do** end the card on the source links, with a 14px drawn icon and a 150ms hover.
- **Do** keep mono for ids, counts, and source labels, and tabular figures in the ledger and the stats strip.
- **Do** keep every font size at or above 0.72rem.

### Don't:
- **Don't** put a lacquer stripe thicker than 1px on the left or right of a card, a callout, or a list row.
- **Don't** wrap a metric in its own bordered card inside the study card.
- **Don't** use an emoji or a Unicode dingbat as an icon. Draw the mark.
- **Don't** set a label above the card title. The title is the heading. The seal belongs inside the conclusion.
- **Don't** add a shadow to every card in the reader. Lift only the flash card and the windows.
