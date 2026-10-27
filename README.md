# 演化日报 · Yanhua Daily

[yanhua.ai](https://yanhua.ai) 是一份递归自我改进（RSI）与智能体框架搜索（harness search）的双语日报。默认简体中文，可切换 English。站点是静态文件，由 GitHub Pages 从仓库根目录发布。

The site is a bilingual daily on recursive self-improvement and agent harness search. Simplified Chinese is the default. English is one toggle away. GitHub Pages serves the repository root. `CNAME` stays `yanhua.ai`, and `.nojekyll` keeps Pages from running Jekyll.

## 阅读

- **阅读流**：按期次排列。每张卡是三块：问题与定位、核心机制、核心结论与深层原因。
- **闪卡**：`←` `→` 换卡，`空格`或点击翻面。已读和收藏记在这台浏览器的 `localStorage`。
- 地址栏 `?lang=en` 或 `?lang=zh` 指定语言。
- 筛选期次、主题，或搜索标题、arXiv 编号、作者、账号。

## 订阅

页面上的邮箱表单会立刻确认，并把订阅记在本地。把投递接到 Buttondown、Loops、Formspree 或 Cloudflare Worker 时，编辑 `data/config.js`：

```js
window.YANHUA_CONFIG = {
  subscribeEndpoint: "https://example.com/subscribe",
  subscribeMethod: "POST",
  subscribeFormat: "json", // Formspree 用 "form"
  subscribeHeaders: {},
  extraFields: {},
  mailto: "",
  githubIssueUrl: "https://github.com/dexhunter/yanhua.ai/issues/new",
  substackUrl: ""
};
```

接口为空，或请求失败时，表单仍然确认成功，并给出 GitHub Issue（以及可选的 mailto / Substack）作为备用投递。不会因为没有后端而报错。

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
      "what": { "zh": "问题与定位。", "en": "What it is and which bottleneck it attacks." },
      "how": { "zh": "机制如何运作。", "en": "How the loop works." },
      "why": { "zh": "结论里的因果，以及限制。", "en": "The causal finding, the numbers, and the caveat." },
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

`check` 会确认每张卡的标题、问题、机制、结论和指标都有中文和英文。

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
