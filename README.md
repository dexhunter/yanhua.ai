<div align="center" id="readme-top">

<a href="https://yanhua.ai"><img src="assets/banner.png" alt="演化日报 · yanhua.ai — Where agents rewrite their own harnesses" width="100%"></a>

<p align="center">
  <a href="https://yanhua.ai"><img src="https://img.shields.io/badge/Live_Site-yanhua.ai-8e2f27?style=for-the-badge" alt="Live Site"></a>
  <a href="https://yanhua.ai"><img src="https://img.shields.io/badge/Cadence-09%3A00%20%26%2018%3A00%20London-1b1714?style=for-the-badge" alt="09:00 &amp; 18:00 London"></a>
  <a href="https://yanhua.ai"><img src="https://img.shields.io/badge/Daily_Email-Resend%20%C2%B7%20%E6%AF%8F%E6%97%A5%E5%90%88%E8%BE%91-14633c?style=for-the-badge" alt="Resend · 每日合辑"></a>
  <a href="https://yanhua.ai/feed.xml"><img src="https://img.shields.io/badge/RSS_/_Atom-feed.xml-b85d19?style=for-the-badge" alt="RSS / Atom"></a>
  <a href="https://yanhua.ai/data/digests.json"><img src="https://img.shields.io/badge/JSON_Feed-digests.json-1e4e79?style=for-the-badge" alt="JSON Feed"></a>
</p>

[Live Reader · 在线阅读](https://yanhua.ai) · [Flash-Card Deck · 闪卡模式](https://yanhua.ai/#deck) · [RSS Feed](https://yanhua.ai/feed.xml) · [JSON API](https://yanhua.ai/data/digests.json)

</div>

<br>

## ❯❯ What is 演化日报 · yanhua.ai

<p align="center">
  <img src="assets/banner.svg" alt="Card anatomy specimen: one-sentence takeaway, tabular metrics, problem and mechanism, then arXiv, GitHub, and X" width="100%">
</p>

<p align="center"><em>一张闪卡的读法：一句话结论，一张指标表，然后才是问题与机制。来源落到 arXiv、GitHub 与 X。</em></p>

**演化日报**是一份给研究者的双语日报，站点在 [yanhua.ai](https://yanhua.ai)。它每天两次追踪智能体如何改写自己的 harness：早上 09:00 与晚上 18:00（Europe/London）各出一版。默认简体中文，English 是同一期内容上的一个开关。每张卡先给一句能读完的结论，说明改进了什么、改进了多少、机制为什么成立，再把问题、做法和可核对的数字放在下面。

**Yanhua Daily** is a bilingual research daily for people who read papers, repositories, and posts about agents that rewrite their own harnesses. It publishes at 09:00 and 18:00 Europe/London. Simplified Chinese is the default; English is the same edition behind one toggle. A card opens with one sentence you can finish — what improved, by how much, and why the mechanism holds — then sets the problem, the method, and the checkable numbers underneath.

GitHub Pages 从仓库根目录发布静态站点。`CNAME` 是 `yanhua.ai`，`.nojekyll` 让 Pages 按原样提供文件。

## ❯❯ Core Coverage · 核心追踪方向

日报围着四条线读文献、仓库和帖子。筛选器里的标签比这四格更细（`harness-search`、`co-evolution`、`verification`、`agentic-rl`、`embodied`、`memory-skills`），读的时候仍落在这张表上。

| **Agent Harness Search · 智能体框架搜索** | **Recursive Self-Improvement · 递归自我改进** |
| --- | --- |
| 搜索、改写、迁移 harness 本身：提示、工具、技能、执行膜、可回滚的适配器。权重可以不动。 | 系统用自己的运行结果改下一轮的做法。演化发生在循环上，而不只发生在一次训练里。 |
| **Verification & Anti-Reward-Hacking · 验证与防作弊** | **Self-Evolving Code & Embodied Agents · 自演化代码与具身** |
| 验证器必须和提议者隔开。评分器上的漏洞会被立刻钻穿，所以核对不能交给正在被优化的那一方。 | 代码代理与机器人把当天的失败写成下一次还能用的计划、技能或恢复规则，而不必为每个场景重训权重。 |

The same four lines, in English: harness search over prompts, tools, skills, and rollbackable adapters; recursive self-improvement of the loop rather than one training run; verification that stays outside the proposer, because a scorer with a gap gets gamed; and self-evolving code or embodied agents that turn today's failures into the next plan without retraining the weights.

## ❯❯ Three-Part Card Anatomy · 三段式精读闪卡

卡不是一条推文的转述。`why`、`what`、`how` 都来自对论文或仓库的阅读。`why` 必须是一句，`what` 必须是一句，`how` 至多两句。

### ❯ 一句话结论 · 1-Sentence Takeaway

结论放在最上面（`why`）。它用人话写明结果和原因，而不是把摘要再压短一截。指标表（`pills`）紧跟在结论后面，数字用等宽、等宽数字排列，涨跌用站点自己的绿色与漆红，而不是另做一套徽章。

The takeaway is one sentence at the top of the card. The table under it is the same fact in numbers: label, value, and a tone of `up`, `down`, or `flat`. A value may be a string or `{ "zh", "en" }`.

### ❯ 问题与机制 · Problem & Mechanism

`what` 是问题与设置，`how` 是机制与实证。两段都要能回到原文，而不是停在转发语上。列表模式里它们分成两列；闪卡的背面是这两段，正面仍是结论和指标。

### ❯ 来源 · arXiv / GitHub / X

每张卡都要能点到论文、仓库、文章或原帖。`arxiv` 打开 `https://arxiv.org/abs/…`，`repo` 打开 GitHub，`handle` 和帖子链接打开 X。

正文里的 `@handle` 会变成指向 `https://x.com/<handle>` 的链接。指标记号保持原样，不会被当成提及：`PR@1`、`pass@1`、`Best@1` 仍是文本。邮箱和裸 `@1` 也不会被链走。

## ❯❯ Reading Surfaces & Feeds · 阅读方式与订阅

### ❯ Reader Stream · 列表

按期次往下读。页眉可以切期次、主题，也可以搜标题、arXiv 编号、作者和账号。`?lang=zh` 或 `?lang=en` 指定语言。纸色主题在浅色 `#f4efe6` 与深色之间切换。

### ❯ 3D Flip Flash-Cards · 闪卡

页眉切到 **闪卡 / Deck**。卡片沿 Y 轴翻转：正面是标题、一句结论和指标，背面是问题与机制。`Space` 或 `Enter` 翻面，`J` / `K` 或 `←` / `→` 换卡。站点没有账号，也不在浏览器里记已读或收藏。

### ❯ Evening Combined Email · 每日晚间合辑

晚上把当天的早间版和晚间版合成一封信，经 Resend 发出。发件人是 `演化日报 · Yanhua Daily <digest@yanhua.ai>`。页面上没有常驻订阅按钮：滚到靠近页尾时，右下角用 `dialog.show()` 打开一扇不挡阅读的小窗。表单 `POST` 到 [https://subscribe.yanhua.ai](https://subscribe.yanhua.ai)，正文是 `{email, lang, source}`。`RESEND_API_KEY` 只放在 Worker 和 GitHub Actions 里。

Pages 的普通部署只同步带 `subscribe` 标签的 Issue 名单。要发信，在 Actions 里手动运行 workflow，并勾上 “Email the latest edition through Resend”。

### ❯ RSS / JSON

- RSS / Atom：<https://yanhua.ai/feed.xml>
- JSON Feed：<https://yanhua.ai/feed.json>
- 原始数据集：<https://yanhua.ai/data/digests.json>

订阅源把一句结论放在条目最前，并把安全的 `@handle` 写成链接。

## ❯❯ Repository & CLI Workflow · 仓库结构与发布流程

规范数据集是 `data/digests.json`（页面通过 `data/digests.js` 读取同一份文档）。仓库里没有单独的根级 `digest.json`。订阅 Worker 是 `scripts/cloudflare-resend-worker.js`，部署在 `https://subscribe.yanhua.ai`。

| Path | Role |
| --- | --- |
| `data/digests.json` | 期次与卡片的双语源数据 |
| `data/digests.js` | 给页面用的同一份数据 |
| `scripts/update_digest.py` | 校验、重建 `digests.js` / RSS / JSON Feed，并给 `index.html` 里的资源盖上 `?v=` 缓存戳 |
| `scripts/send_newsletter_resend.py` | 生成早间 + 晚间合辑 HTML，并用 Resend 广播 |
| `scripts/cloudflare-resend-worker.js` | 右下角订阅窗背后的 Cloudflare Worker |
| `feed.xml` / `feed.json` | 公开订阅源 |
| `index.html` · `assets/` · `data/config.js` | 页面、样式与订阅接口配置 |

校验然后构建：

```bash
python3 scripts/update_digest.py check && python3 scripts/update_digest.py build
```

`check` 只校验。`build` 会再校验一次，然后写出前端数据和订阅源。追加一期（`slot` 取 `morning`、`evening`，或 `""` 表示当天只有一版）：

```bash
python3 scripts/update_digest.py append editions/2026-10-28-evening.json
```

同 `id` 再追加会替换那一期。新期插到最前。

邮件：

```bash
python3 scripts/send_newsletter_resend.py --preview /tmp/daily_email_preview.html
python3 scripts/send_newsletter_resend.py --preview /tmp/daily_email_preview.html --date 2026-10-27
python3 scripts/send_newsletter_resend.py --sync-only
python3 scripts/send_newsletter_resend.py --send --date 2026-10-27
```

`--preview` 只写 HTML，不调用 Resend，也不需要密钥。`--date` 缺省时用最新一期的日期。`--send` 会先同步名单，再把该日的早间版和晚间版合成一封广播。`--sync-only` 只同步，不发信。域名尚未验证时，发件人会退回 `onboarding@resend.dev`。

<p align="center">
  <a href="#readme-top"><img src="https://img.shields.io/badge/-Back_to_top-1b1714?style=flat-square" alt="Back to top"></a>
</p>
