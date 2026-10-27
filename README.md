# 演化日报 · Yanhua Daily

[yanhua.ai](https://yanhua.ai) 是一份递归自我改进（RSI）与智能体框架搜索（harness search）的双语日报。默认简体中文，可切换 English。站点是静态文件，由 GitHub Pages 从仓库根目录发布。

The site is a bilingual daily on recursive self-improvement and agent harness search. Simplified Chinese is the default. English is one toggle away. GitHub Pages serves the repository root. `CNAME` stays `yanhua.ai`, and `.nojekyll` keeps Pages from running Jekyll.

## 阅读

- **阅读流**：按期次排列。每张卡先给一句结论，下面是指标，再以两列放问题背景和机制。文中的 `@handle` 可以点开，卡片底部有论文、仓库或帖子链接。
- **闪卡**：正面是标题、一句结论和指标，背面是问题与机制。`←` `→` 换卡，`空格`或点击翻面。已读和收藏记在这台浏览器的 `localStorage`。
- 地址栏 `?lang=en` 或 `?lang=zh` 指定语言。
- 筛选期次、主题，或搜索标题、arXiv 编号、作者、账号。

## 订阅

页眉没有订阅按钮。滚到页尾附近时，右下角用 `dialog.show()` 打开一扇不挡页面的小窗；关掉之后这一次浏览不再自动出现。已经订阅过的浏览器也不会再自动弹出。

表单 `POST` 到 `https://subscribe.yanhua.ai`，正文是 `{email, lang, source}`。订阅数来自 `GET https://subscribe.yanhua.ai/stats`。密钥 `RESEND_API_KEY` 只放在 Worker 上。名单进 Resend 的 General segment（`0f2fbb4e-3333-43c1-a0d2-16c69a7c3003`）。

- **每日寄出**：`scripts/send_newsletter_resend.py` 在 GitHub Actions 里用仓库密钥 `RESEND_API_KEY` 同步带 `subscribe` 标签的 Issue，并在手动运行 workflow 且勾上 “Email the latest edition through Resend” 时，把最新一期做成 Resend broadcast。发信人是 `演化日报 · Yanhua Daily <digest@yanhua.ai>`，域名未验证时改用 `onboarding@resend.dev`。普通的 Pages 部署只同步名单，不发信。

编辑 `data/config.js`：

```js
window.YANHUA_CONFIG = {
  subscribeEndpoint: "https://subscribe.yanhua.ai",
  statsEndpoint: "https://subscribe.yanhua.ai/stats",
  resendAudienceId: "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003",
  subscribeMethod: "POST",
  subscribeFormat: "json", // Formspree 用 "form"
  subscribeHeaders: {},
  extraFields: {},
  mailto: "",
  githubIssueUrl: "https://github.com/dexhunter/yanhua.ai/issues/new",
  substackUrl: "",
  cloudflareBeaconToken: "",
  goatcounterCode: "",
  plausibleDomain: ""
};
```

Worker 接受之后，这台浏览器才记住订阅。请求失败时窗口里会说明没有送出，并给出一个带 `subscribe` 标签的 GitHub Issue 作为备用。

## 访问与订阅统计

页眉和页脚的统计条用 [vercount](https://events.vercount.one/api/v2/log) 记录 `https://yanhua.ai/` 的访客（UV）和阅读（PV）。订阅数是 `https://subscribe.yanhua.ai/stats` 返回的 Resend 名册人数。点统计条，或打开 `?stats=1`，可以看到这三项、本机已读和收藏。

可选的外部统计写在 `data/config.js`。留空则只用上面的内置计数：

```js
cloudflareBeaconToken: "", // Cloudflare Web Analytics token
goatcounterCode: "",       // "yanhua" 或 "yanhua.goatcounter.com"
plausibleDomain: ""        // "yanhua.ai"
```

RSS：<https://yanhua.ai/feed.xml>  
JSON Feed：<https://yanhua.ai/feed.json>

## 追加一期

源数据是 `data/digests.json`。新增一期写成一个 JSON 文件，例如 `editions/2026-10-28-evening.json`：

```json
{
  "edition": {
    "id": "2026-10-28-evening",
    "date": "2026-10-28",
    "slot": "evening",
    "label": { "zh": "2026-10-28 晚间版", "en": "28 Oct 2026 · Evening" }
  },
  "items": [
    {
      "id": "unique-slug",
      "edition": "2026-10-28-evening",
      "tags": ["harness-search"],
      "title": { "zh": "标题", "en": "Title" },
      "what": { "zh": "一句问题。", "en": "One sentence on the problem." },
      "how": { "zh": "一两句机制，关键数字放这里。", "en": "One or two sentences on the mechanism, with the key numbers." },
      "why": { "zh": "一句人话结论，说明结果以及为什么。", "en": "One sentence stating the conclusion and why it holds." },
      "metric": { "zh": "一句话指标", "en": "One-line metric" },
      "pills": [{ "zh": "指标", "en": "Metric", "value": "1.0", "tone": "up" }],
      "arxiv": "2610.00000",
      "authors": "Name et al.",
      "handle": "@someone",
      "links": [{ "zh": "论文", "en": "Paper", "url": "https://arxiv.org/abs/2610.00000" }]
    }
  ]
}
```

`slot` 取 `morning`、`evening`，或 `""`（一天一期）。`tags` 用：`harness-search`、`co-evolution`、`verification`、`agentic-rl`、`embodied`、`memory-skills`。`tone` 取 `up`、`down`、`flat`。`value` 可以是字符串，或 `{ "zh": "……", "en": "……" }`。

然后：

```bash
python3 scripts/update_digest.py append editions/2026-10-28-evening.json
```

这条命令把新一期插到最前，替换同 id 的旧一期，并重新写出：

- `data/digests.json`
- `data/digests.js`
- `feed.xml`
- `feed.json`

只重算前端数据和订阅源、不改内容时：

```bash
python3 scripts/update_digest.py build
python3 scripts/update_digest.py check
```

`check` 会确认每张卡的标题、问题、机制、结论和指标都有中文和英文，`what` 与 `why` 各是一句，`how` 不超过两句，并且每张卡都能落到论文、仓库、文章或帖子链接。订阅源把这句结论放在条目最前，并把 `@handle` 写成可点击的链接。

## 文件

| 路径 | 作用 |
| --- | --- |
| `index.html` | 页面 |
| `CNAME` | `yanhua.ai` |
| `.nojekyll` | 让 GitHub Pages 按原样发布 |
| `favicon.svg` | 标志 |
| `assets/` | 样式与交互 |
| `data/digests.json` | 日报源数据 |
| `data/digests.js` | 给页面用的同一份数据 |
| `data/config.js` | 订阅接口 |
| `feed.xml` / `feed.json` | 订阅源 |
| `scripts/update_digest.py` | 追加一期并重建订阅源 |
