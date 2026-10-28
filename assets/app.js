(function () {
  const data = window.YANHUA_DIGESTS;
  const config = window.YANHUA_CONFIG || {};
  if (!data || !Array.isArray(data.items)) {
    document.getElementById("content").textContent = "Digest data missing.";
    return;
  }

  const COPY = {
    zh: {
      docTitle: "演化日报 · 递归自我改进与框架搜索",
      description: "演化日报：递归自我改进与智能体框架搜索。中文为主，可切换英文。",
      skip: "跳到正文",
      modeLabel: "阅读方式",
      langLabel: "语言",
      deck: "闪卡",
      reader: "阅读流",
      subscribe: "订阅",
      subscribeTitle: "订阅演化日报",
      toastTitle: "订阅演化日报",
      toastLead: "觉得有用？留下邮箱，每日更新直达收件箱。",
      dismiss: "关闭",
      email: "邮箱",
      emailPh: "you@lab.edu",
      langPref: "语言偏好",
      zh: "中文",
      en: "English",
      both: "双语",
      invalid: "请输入有效的邮箱地址。",
      sent: "订阅成功，每日更新将发送至你的邮箱。",
      github: "通过 GitHub Issue 送出",
      close: "关闭",
      themeDark: "切换到深色",
      themeLight: "切换到浅色",
      searchPh: "搜索标题、arXiv、作者",
      mastSub: "递归自我改进与智能体框架搜索 · 每日双语精读闪卡",
      editions: "期次",
      allEditions: "全部期次",
      topics: "主题",
      allTopics: "全部主题",
      what: "问题与背景",
      how: "核心机制",
      why: "一句话结论",
      prev: "上一张",
      next: "下一张",
      flip: "翻转卡片",
      keys: "Space / Enter 翻转卡片 · J / K 或 ← / → 上一张 / 下一张",
      emptyTitle: "没有匹配的卡片",
      emptyBody: "换一个关键词，或清除筛选。",
      clear: "清除筛选",
      copyLink: "复制链接",
      copied: "已复制链接",
      count: function (n) { return n + " 篇"; },
      progress: function (i, n) { return i + " / " + n; },
      footer: "演化日报 · 聚焦递归自我改进（RSI）、智能体框架（Harness）搜索与自主科研的每日双语研究简报。",
      feeds: "订阅源",
      rss: "RSS",
      json: "JSON",
      paper: "论文",
      source: "来源",
      visitors: "访客",
      views: "阅读",
      subscribers: "订阅",
      statsTitle: "站点统计",
      statsLead: "访客与阅读量来自公开访问统计，订阅数为当前邮件列表人数。",
      totalCards: "卡片总数",
      editionCount: "期数",
      papersIndexed: "收录论文",
      mostRead: "读者最关注的研究卡片",
      mostReadNote: "按阅读时长、卡片翻阅、原文点击与分享综合排序",
      mostReadEmpty: "暂无卡片阅读明细，浏览或点击卡片后自动统计。",
      rankMeta: function (views, seconds, actions) {
        return "阅读 " + views + " 次 · 停留 " + seconds + "s · 点击/翻转 " + actions + " 次";
      },
      cadence: "每日 09:00 与 18:00（UTC+0）更新当期内容，晚间更新后发送每日汇总邮件。",
      failed: "提交失败，请稍后重试。",
      issueList: "在 GitHub 查看订阅",
      analyticsConfig: "配置外部统计"
    },
    en: {
      docTitle: "Yanhua Daily · RSI & Harness Search",
      description: "Yanhua Daily: recursive self-improvement and agent harness search, in Chinese and English.",
      skip: "Skip to content",
      modeLabel: "Reading mode",
      langLabel: "Language",
      deck: "Flash cards",
      reader: "Reader",
      subscribe: "Subscribe",
      subscribeTitle: "Subscribe to Yanhua Daily",
      toastTitle: "Subscribe to Yanhua Daily",
      toastLead: "Enjoying the cards? Get new editions by email.",
      dismiss: "Dismiss",
      email: "Email",
      emailPh: "you@lab.edu",
      langPref: "Language preference",
      zh: "中文",
      en: "English",
      both: "Bilingual",
      invalid: "Enter a valid email address.",
      sent: "Subscribed! Daily updates will be sent to your inbox.",
      github: "Send via GitHub Issue",
      close: "Close",
      themeDark: "Switch to dark",
      themeLight: "Switch to light",
      searchPh: "Search titles, arXiv ids, authors",
      mastSub: "Recursive self-improvement & agent harness search · Daily bilingual flash cards",
      editions: "Editions",
      allEditions: "All editions",
      topics: "Topics",
      allTopics: "All topics",
      what: "Problem & context",
      how: "Core mechanism",
      why: "Key Takeaway",
      prev: "Previous",
      next: "Next",
      flip: "Flip card",
      keys: "Space / Enter flips the card · J / K or ← / → previous / next",
      emptyTitle: "No cards match",
      emptyBody: "Try another query, or clear the filters.",
      clear: "Clear filters",
      copyLink: "Copy link",
      copied: "Link copied",
      count: function (n) { return n === 1 ? "1 card" : n + " cards"; },
      progress: function (i, n) { return i + " / " + n; },
      footer: "Yanhua Daily · A daily bilingual digest on recursive self-improvement (RSI), agent harness search, and autonomous research.",
      feeds: "Feeds",
      rss: "RSS",
      json: "JSON",
      paper: "Paper",
      source: "Source",
      visitors: "Visitors",
      views: "Views",
      subscribers: "Subscribers",
      statsTitle: "Site analytics",
      statsLead: "Live visitor and view counts alongside current email newsletter subscribers.",
      totalCards: "Total cards",
      editionCount: "Editions",
      papersIndexed: "Papers indexed",
      mostRead: "Most-Read Research Cards",
      mostReadNote: "Ranked by dwell time, card flips, source clicks, and link shares",
      mostReadEmpty: "Card engagement will appear here as readers browse and click cards.",
      rankMeta: function (views, seconds, actions) {
        const viewLabel = views === 1 ? "1 view" : views + " views";
        const actionLabel = actions === 1 ? "1 click/flip" : actions + " clicks/flips";
        return viewLabel + " · " + seconds + "s read · " + actionLabel;
      },
      cadence: "Updated daily at 09:00 and 18:00 UTC+0, with a combined daily digest email sent after the evening update.",
      failed: "Submission failed. Please try again.",
      issueList: "View subscriptions on GitHub",
      analyticsConfig: "Configure external analytics"
    }
  };

  function modeFromLocation() {
    const mode = new URLSearchParams(location.search).get("mode");
    if (mode === "deck" || mode === "reader") return mode;
    return localStorage.getItem("yanhua-mode") === "deck" ? "deck" : "reader";
  }
  const state = {
    lang: document.documentElement.lang === "en" ? "en" : "zh",
    mode: modeFromLocation(),
    edition: "all",
    tag: "all",
    q: "",
    index: 0,
    flipped: false,
    sub: loadSub()
  };

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const stage = document.getElementById("stage");
  const mast = document.getElementById("mast");
  const rail = document.getElementById("rail");
  const foot = document.getElementById("foot");
  const statsDialog = document.getElementById("stats-dialog");
  const subDialog = document.getElementById("sub-dialog");
  const VERCOUNT = "https://events.vercount.one/api/v2/log";
  const SITE = String(config.siteUrl || "https://yanhua.ai").replace(/\/$/, "");
  const stats = { uv: null, pv: null, subscribers: null, cards: null, editions: null, papers: null, engagement: [] };
  const sessionDelta = {};
  const viewedOnce = {};
  const activeSince = {};
  let eventQueue = [];
  let flushTimer = null;
  let readerObserver = null;
  (function seedPublication() {
    const counts = publicationCounts();
    stats.cards = counts.cards;
    stats.editions = counts.editions;
    stats.papers = counts.papers;
  })();
  let pointer = null;

  function loadSub() {
    try { return JSON.parse(localStorage.getItem("yanhua-subscription") || "null"); }
    catch (err) { return null; }
  }
  function t(key) { return COPY[state.lang][key]; }
  function tx(block) {
    if (!block) return "";
    if (typeof block === "string") return block;
    return block[state.lang] || block.zh || "";
  }
  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }
  const X_URL = /^https?:\/\/(?:www\.)?(?:x|twitter)\.com\/([A-Za-z0-9_]{1,15})(?:\/status\/(\d+))?\/?(?:[?#].*)?$/i;
  function handleUrlMap(item) {
    const map = {};
    (item && item.links || []).forEach(function (link) {
      const match = X_URL.exec(link.url || "");
      if (!match) return;
      const key = match[1].toLowerCase();
      const prev = map[key];
      if (!prev || (match[2] && prev.indexOf("/status/") === -1)) map[key] = link.url;
    });
    return map;
  }
  function isHandleMention(text, offset, name) {
    if (offset > 0 && /[A-Za-z0-9_.-]/.test(text.charAt(offset - 1))) return false;
    if (!name || !/[A-Za-z_]/.test(name) || /^\d+$/.test(name)) return false;
    const rest = text.slice(offset + 1 + name.length);
    if (/^[A-Za-z0-9_]/.test(rest) || /^\.[A-Za-z0-9_]/.test(rest)) return false;
    return true;
  }
  function linkify(text, item) {
    const map = handleUrlMap(item || {});
    return esc(text).replace(/@([A-Za-z0-9_]{1,15})/g, function (full, name, offset, whole) {
      if (!isHandleMention(whole, offset, name)) return full;
      const href = map[name.toLowerCase()] || ("https://x.com/" + name);
      return '<a href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">@' + esc(name) + "</a>";
    });
  }
  function paragraphs(text, item) {
    return String(text).split(/\n\n+/).filter(Boolean).map(function (part) {
      return "<p>" + linkify(part.trim(), item) + "</p>";
    }).join("");
  }
  function arxivIdFrom(url) {
    const match = String(url).match(/arxiv\.org\/(?:abs|pdf)\/(\d{4}\.\d{4,5})(?:v\d+)?/i);
    return match ? match[1] : "";
  }
  function githubSlug(url) {
    const match = String(url).match(/^https?:\/\/(?:www\.)?github\.com\/([^/#?\s]+)\/([^/#?\s]+)/i);
    if (!match) return "";
    return match[1] + "/" + match[2].replace(/\.git$/, "");
  }
  function sourceBag(item) {
    const raw = (item.links || []).slice();
    const seen = {};
    raw.forEach(function (link) { if (link && link.url) seen[link.url] = true; });
    if (item.arxiv) {
      const url = "https://arxiv.org/abs/" + item.arxiv;
      if (!seen[url]) {
        raw.unshift({ zh: "论文", en: "Paper", url: url });
        seen[url] = true;
      }
    }
    if (item.repo) {
      const url = /^https?:\/\//i.test(item.repo) ? item.repo : "https://github.com/" + String(item.repo).replace(/^\//, "");
      if (!seen[url]) raw.push({ zh: "仓库", en: "Repo", url: url });
    }
    const docs = [];
    const posts = [];
    const seenStatus = {};
    raw.forEach(function (link) {
      if (!link || !link.url) return;
      const match = X_URL.exec(link.url);
      if (match && match[2]) {
        if (!seenStatus[link.url]) {
          seenStatus[link.url] = true;
          posts.push({ handle: match[1], url: link.url, zh: link.zh, en: link.en });
        }
        return;
      }
      if (match) return;
      docs.push(link);
    });
    return { docs: docs, posts: posts };
  }
  function genericPostLabel(text, handle, lang) {
    const value = String(text || "").trim();
    if (!value) return true;
    if (value.replace(/^@/, "").toLowerCase() === String(handle || "").toLowerCase()) return true;
    const folded = value.toLowerCase();
    if (lang === "zh") return folded === "分享" || folded === "原文" || folded === "帖子" || folded === "推文" || folded === "x" || folded === "x 原帖";
    return folded === "post" || folded === "source" || folded === "thread" || folded === "x" || folded === "x post";
  }
  function postLabel(post) {
    const label = state.lang === "zh" ? post.zh : post.en;
    if (!genericPostLabel(label, post.handle, state.lang)) return String(label);
    return (state.lang === "zh" ? "X 原帖 · @" : "X Post · @") + post.handle;
  }
  function profileLinks(handle) {
    const html = [];
    String(handle || "").replace(/@([A-Za-z0-9_]{1,15})/g, function (full, name, offset, whole) {
      if (!isHandleMention(whole, offset, name)) return full;
      html.push('<a class="byline-handle" href="https://x.com/' + encodeURIComponent(name) + '" target="_blank" rel="noopener noreferrer">@' + esc(name) + "</a>");
      return "";
    });
    return html.join(" · ");
  }
  function sourceIcon(kind) {
    if (kind === "repo") {
      return '<svg class="source-ico" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M5 4.1 2.5 7 5 9.9M9 4.1 11.5 7 9 9.9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    }
    if (kind === "x") {
      return '<svg class="source-ico" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M14.06 3h3.16l-6.9 7.89L18.4 21h-3.2l-5.02-6.56L5.3 21H2.13l7.38-8.44L2.7 3h3.28l4.54 6.01L14.06 3Zm-1.11 16.2h1.75L7.16 4.68H5.3l7.65 14.52Z"/></svg>';
    }
    return '<svg class="source-ico" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M3.2 1.7h5l2.6 2.6v8H3.2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8.1 1.8v2.6h2.6M5 7.2h4M5 9.3h3.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function sourceText(link) {
    const ax = arxivIdFrom(link.url);
    if (ax) return (state.lang === "zh" ? "论文 arXiv:" : "Paper arXiv:") + ax;
    const slug = githubSlug(link.url);
    if (slug) return "GitHub: " + slug;
    return tx(link) || (state.lang === "zh" ? "原文" : "Source");
  }
  function sourceKind(link) {
    if (arxivIdFrom(link.url)) return "paper";
    if (githubSlug(link.url)) return "repo";
    return "paper";
  }
  function sourceAnchor(url, kind, label) {
    return '<a class="source-link" href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + sourceIcon(kind) + "<span>" + esc(label) + "</span></a>";
  }
  function linkIcon() {
    return '<svg class="source-ico" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M5.55 8.45 8.45 5.55" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M7.9 9.7 6.55 11.05a2.05 2.05 0 1 1-2.9-2.9L5.05 6.75" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.1 4.3 7.45 2.95a2.05 2.05 0 1 1 2.9 2.9L8.95 7.25" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function cardPermalink(item) {
    const query = state.lang === "en" ? "?mode=deck&lang=en" : "?mode=deck";
    return SITE + "/" + query + "#" + encodeURIComponent(item.id);
  }
  function copyLinkButton(item) {
    return '<button type="button" class="source-link copy-link" data-copy-link="' + esc(cardPermalink(item)) + '" data-copy-id="' + esc(item.id) + '">' + linkIcon() + '<span>' + esc(t("copyLink")) + "</span></button>";
  }
  function sources(item) {
    const bag = sourceBag(item);
    const parts = bag.docs.map(function (link) {
      return sourceAnchor(link.url, sourceKind(link), sourceText(link));
    }).concat(bag.posts.map(function (post) {
      return sourceAnchor(post.url, "x", postLabel(post));
    }));
    return '<div class="source-row">' + parts.join("") + copyLinkButton(item) + "</div>";
  }
  function verdict(item) {
    return '<aside class="verdict-box"><p class="verdict-text"><span class="verdict-kicker">' + esc(t("why")) + "</span> " + linkify(tx(item.why), item) + "</p></aside>";
  }
  function contextGrid(item) {
    return '<div class="context-grid">' +
      '<section class="context-col"><h4>' + esc(t("what")) + "</h4>" + paragraphs(tx(item.what), item) + "</section>" +
      '<section class="context-col"><h4>' + esc(t("how")) + "</h4>" + paragraphs(tx(item.how), item) + "</section>" +
      "</div>";
  }
  function scheme() {
    const meta = document.querySelector('meta[name="color-scheme"]').content;
    if (meta === "light" || meta === "dark") return meta;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function setScheme(next) {
    document.querySelector('meta[name="color-scheme"]').content = next;
    localStorage.setItem("yanhua-color-scheme", next);
    const theme = document.querySelector('meta[name="theme-color"]');
    if (theme) theme.content = next === "dark" ? "#12110f" : "#f4efe6";
    paintThemeButton();
  }
  function editionById(id) {
    return data.editions.find(function (edition) { return edition.id === id; });
  }
  function tagById(id) {
    return data.tags.find(function (tag) { return tag.id === id; });
  }
  function matches(item) {
    if (state.edition !== "all" && item.edition !== state.edition) return false;
    if (state.tag !== "all" && item.tags.indexOf(state.tag) === -1) return false;
    const q = state.q.trim().toLowerCase();
    if (!q) return true;
    const edition = editionById(item.edition);
    const hay = [
      item.id, item.arxiv, item.authors, item.handle, item.repo,
      tx(item.title), item.title.zh, item.title.en,
      item.what.zh, item.what.en, item.how.zh, item.how.en, item.why.zh, item.why.en,
      edition ? edition.label.zh + " " + edition.label.en : "",
      item.tags.map(function (id) {
        const tag = tagById(id);
        return tag ? tag.label.zh + " " + tag.label.en : id;
      }).join(" ")
    ].join(" ").toLowerCase();
    return hay.indexOf(q) !== -1;
  }
  function visible() { return data.items.filter(matches); }

  function pills(item) {
    if (!item.pills || !item.pills.length) return "";
    return '<div class="pills">' + item.pills.map(function (pill) {
      return '<span class="pill ' + esc(pill.tone || "") + '"><b>' + esc(tx(pill.value)) + '</b><span>' + esc(tx(pill)) + '</span></span>';
    }).join("") + "</div>";
  }
  function byline(item) {
    const bits = [];
    if (item.authors) bits.push(esc(item.authors));
    const profiles = profileLinks(item.handle);
    if (profiles) bits.push(profiles);
    (item.tags || []).forEach(function (id) {
      const tag = tagById(id);
      if (!tag) return;
      const pressed = state.tag === id ? ' aria-pressed="true"' : "";
      bits.push('<button type="button" class="byline-tag" data-tag="' + esc(id) + '"' + pressed + '>' + esc(tx(tag.label)) + '</button>');
    });
    return bits.length ? '<p class="byline">' + bits.join(" · ") + "</p>" : "";
  }
  function deckActions(item) {
    return '<div class="deck-actions">' +
      '<button type="button" class="btn-primary js-deck-flip">' + esc(t("flip")) + "</button>" +
      sources(item) +
      "</div>";
  }

  function radio(prefix, value, label, checked) {
    return '<label><input type="radio" name="' + prefix + '-lang" value="' + value + '"' + (checked ? " checked" : "") + '> ' + esc(label) + '</label>';
  }

  function paintChrome() {
    document.documentElement.lang = state.lang === "en" ? "en" : "zh-Hans";
    document.documentElement.dataset.flipped = state.mode === "deck" && state.flipped ? "true" : "false";
    document.title = t("docTitle");
    const desc = document.querySelector('meta[name="description"]');
    if (desc) desc.content = t("description");
    const skip = document.getElementById("skip-link");
    if (skip) skip.textContent = t("skip");
    const mode = document.getElementById("mode-switch");
    if (mode) {
      mode.setAttribute("aria-label", t("modeLabel"));
      mode.innerHTML =
        seg("mode", "reader", t("reader"), state.mode === "reader") +
        seg("mode", "deck", t("deck"), state.mode === "deck");
    }
    const lang = document.getElementById("lang-switch");
    if (lang) {
      lang.setAttribute("aria-label", t("langLabel"));
      lang.innerHTML =
        seg("lang", "zh", "中文", state.lang === "zh") +
        seg("lang", "en", "EN", state.lang === "en");
    }
    paintThemeButton();
    const url = new URL(location.href);
    url.searchParams.set("lang", state.lang);
    history.replaceState(null, "", url.pathname + url.search + url.hash);
  }
  function seg(name, value, label, pressed) {
    return '<button type="button" data-set="' + name + '" data-value="' + value + '" aria-pressed="' + pressed + '">' + esc(label) + '</button>';
  }
  function paintThemeButton() {
    const dark = scheme() === "dark";
    const btn = document.getElementById("theme-btn");
    if (!btn) return;
    const label = dark ? t("themeLight") : t("themeDark");
    btn.setAttribute("aria-label", label);
    btn.innerHTML = (dark ? sun() : moon()) + '<span>' + esc(label) + '</span>';
  }
  function moon() {
    return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M15.5 3.5a8 8 0 1 0 5 12.5A8.5 8.5 0 0 1 15.5 3.5z"/></svg>';
  }
  function sun() {
    return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="3.2"/><path d="M12 3.5v2.2M12 18.3v2.2M3.5 12h2.2M18.3 12h2.2M6 6l1.6 1.6M16.4 16.4 18 18M18 6l-1.6 1.6M7.6 16.4 6 18"/></svg>';
  }

  function editionSize(id) {
    return data.items.filter(function (item) { return item.edition === id; }).length;
  }
  function railCount(n) {
    return '<span class="rail-count">' + esc(String(n)) + "</span>";
  }
  function renderRail() {
    if (!rail) return;
    const editions = data.editions.map(function (edition) {
      const current = state.edition === edition.id ? ' aria-current="page"' : "";
      return '<a href="#edition-' + esc(edition.id) + '" data-edition="' + esc(edition.id) + '"' + current + '><span>' + esc(tx(edition.label)) + "</span>" + railCount(editionSize(edition.id)) + "</a>";
    }).join("");
    const tags = data.tags.map(function (tag) {
      return '<button type="button" class="chip" data-tag="' + esc(tag.id) + '" aria-pressed="' + (state.tag === tag.id) + '">' + esc(tx(tag.label)) + '</button>';
    }).join("");
    rail.innerHTML =
      '<input class="search" id="q" type="search" placeholder="' + esc(t("searchPh")) + '" aria-label="' + esc(t("searchPh")) + '" value="' + esc(state.q) + '">' +
      '<h2>' + esc(t("editions")) + '</h2>' +
      '<div class="rail-list"><a href="#content" data-edition="all"' + (state.edition === "all" ? ' aria-current="page"' : "") + '><span>' + esc(t("allEditions")) + "</span>" + railCount(data.items.length) + "</a>" + editions + '</div>' +
      '<h2>' + esc(t("topics")) + '</h2>' +
      '<div class="rail-list"><button type="button" class="chip" data-tag="all" aria-pressed="' + (state.tag === "all") + '">' + esc(t("allTopics")) + '</button>' + tags + '</div>';
  }

  function isPaperItem(item) {
    if (item.arxiv && String(item.arxiv).trim()) return true;
    return (item.links || []).some(function (link) {
      const url = String(link && link.url || "");
      if (/arxiv\.org\/(?:abs|pdf)\//i.test(url)) return true;
      const label = String((link && (link.en || link.zh)) || "").trim().toLowerCase();
      return label === "paper" || label === "论文";
    });
  }
  function publicationCounts() {
    return {
      cards: data.items.length,
      editions: data.editions.length,
      papers: data.items.filter(isPaperItem).length
    };
  }
  function statText(key) {
    const value = stats[key];
    return value == null ? "—" : String(value);
  }
  function statsStrip() {
    return '<button type="button" class="stats-strip" data-open-stats aria-haspopup="dialog">' +
      '<span>' + esc(t("totalCards")) + ' <b data-stat="cards">' + esc(statText("cards")) + '</b></span>' +
      '<span>' + esc(t("editionCount")) + ' <b data-stat="editions">' + esc(statText("editions")) + '</b></span>' +
      '<span>' + esc(t("papersIndexed")) + ' <b data-stat="papers">' + esc(statText("papers")) + '</b></span>' +
      '</button>';
  }
  function paintStats() {
    document.querySelectorAll("[data-stat]").forEach(function (node) {
      const key = node.getAttribute("data-stat");
      if (!Object.prototype.hasOwnProperty.call(stats, key)) return;
      node.textContent = statText(key);
    });
  }
  function renderMast() {
    if (!mast) return;
    mast.innerHTML =
      '<div class="mast-bar">' +
        '<p class="mast-sub">' + esc(t("mastSub")) + '</p>' +
        statsStrip() +
      '</div>';
  }

  function filtersActive() {
    return state.edition !== "all" || state.tag !== "all" || state.q.trim() !== "";
  }
  function filterBar(list) {
    if (!filtersActive()) return "";
    const bits = [];
    if (state.edition !== "all") {
      const edition = editionById(state.edition);
      if (edition) bits.push(esc(tx(edition.label)));
    }
    if (state.tag !== "all") {
      const tag = tagById(state.tag);
      if (tag) bits.push(esc(tx(tag.label)));
    }
    if (state.q.trim()) bits.push(esc(state.q.trim()));
    return '<div class="active-filters" role="status">' +
      '<p><span>' + bits.join(" · ") + '</span> <span class="active-count">' + esc(t("count")(list.length)) + "</span></p>" +
      '<button type="button" class="btn" id="clear-filters">' + esc(t("clear")) + "</button></div>";
  }
  function renderReader(list) {
    if (!stage) return;
    const bar = filterBar(list);
    if (!list.length) {
      stage.innerHTML = bar + empty(bar !== "");
      return;
    }
    const groups = [];
    data.editions.forEach(function (edition) {
      const rows = list.filter(function (item) { return item.edition === edition.id; });
      if (!rows.length) return;
      groups.push(
        '<section class="edition-block" id="edition-' + esc(edition.id) + '">' +
          '<div class="edition-head"><h2>' + esc(tx(edition.label)) + '</h2>' +
          '<div class="edition-count">' + esc(t("count")(rows.length)) + '</div></div>' +
          rows.map(article).join("") +
        '</section>'
      );
    });
    stage.innerHTML = bar + groups.join("");
  }
  function article(item) {
    return '<article class="entry" id="' + esc(item.id) + '">' +
      '<div class="entry-top"><div><h3><a href="#' + esc(item.id) + '">' + esc(tx(item.title)) + '</a></h3>' + byline(item) + '</div></div>' +
      verdict(item) + pills(item) + contextGrid(item) + sources(item) +
      '</article>';
  }
  function empty(withBar) {
    const button = withBar ? "" : '<button type="button" class="btn" id="clear-filters">' + esc(t("clear")) + "</button>";
    return '<div class="empty"><p>' + esc(t("emptyTitle")) + '</p><p>' + esc(t("emptyBody")) + "</p>" + button + "</div>";
  }

  function renderDeck(list) {
    if (!stage) return;
    const bar = filterBar(list);
    if (!list.length) {
      stage.innerHTML = bar + empty(bar !== "");
      return;
    }
    if (state.index >= list.length) state.index = 0;
    const item = list[state.index];
    const edition = editionById(item.edition);
    const frontHidden = state.flipped ? " inert" : "";
    const backHidden = state.flipped ? "" : " inert";
    stage.innerHTML = bar +
      '<div class="deck-toolbar"><p class="deck-progress">' + esc(tx(edition.label)) + '  ·  ' + esc(t("progress")(state.index + 1, list.length)) + '</p><p class="keys">' + esc(t("keys")) + '</p></div>' +
      '<div class="deck-stage' + (state.flipped ? " is-flipped" : "") + '" id="deck-stage">' +
        '<div class="deck-spin">' +
          '<article class="face face-front deck-sheet" id="' + esc(item.id) + '"' + frontHidden + '>' +
            '<h2>' + esc(tx(item.title)) + '</h2>' +
            byline(item) +
            verdict(item) +
            pills(item) +
            deckActions(item) +
          '</article>' +
          '<article class="face face-back deck-sheet"' + backHidden + '>' +
            '<h2>' + esc(tx(item.title)) + '</h2>' +
            contextGrid(item) +
            deckActions(item) +
          '</article>' +
        '</div>' +
      '</div>' +
      '<div class="deck-nav">' +
        '<button type="button" class="btn" id="deck-prev"' + (state.index === 0 ? " disabled" : "") + '>' + esc(t("prev")) + '</button>' +
        '<button type="button" class="btn" id="deck-next"' + (state.index === list.length - 1 ? " disabled" : "") + '>' + esc(t("next")) + '</button>' +
      '</div>';
  }

  function renderFoot() {
    if (!foot) return;
    foot.innerHTML = '<div class="colophon-inner"><p>' + esc(t("footer")) + '</p><p class="feed-row"><a href="/feed.xml">' + esc(t("rss")) + '</a><span aria-hidden="true">·</span><a href="/feed.json">' + esc(t("json")) + '</a></p></div>';
  }
  function renderSubWindow() {
    if (!subDialog) return;
    const current = subDialog.querySelector("input[type=email]");
    const draft = current ? current.value : (state.sub ? state.sub.email : "");
    const focused = current && document.activeElement === current;
    const sub = state.sub;
    const statusHtml = sub ? '<p class="status" role="status">' + esc(t("sent")) + '</p>' : '<p class="status" role="status"></p>';
    subDialog.innerHTML =
      '<div class="sub-win-titlebar">' +
        '<div class="sub-win-brand"><span class="sub-win-dot" aria-hidden="true"></span><h2 id="sub-title">订阅演化日报 · Subscribe</h2></div>' +
        '<button type="button" id="close-sub" aria-label="关闭">×</button>' +
      '</div>' +
      '<div class="sub-win-body">' +
        '<form class="subscribe-form">' +
          '<p>' + esc(t("toastLead")) + '</p>' +
          '<div class="slip-row">' +
            '<label class="vh" for="sub-email">' + esc(t("email")) + '</label>' +
            '<input id="sub-email" name="email" type="email" required autocomplete="email" inputmode="email" placeholder="' + esc(t("emailPh")) + '" value="' + esc(draft) + '">' +
            '<button class="btn-primary" type="submit">' + esc(t("subscribe")) + '</button>' +
          '</div>' +
          '<p class="field-error">' + esc(t("invalid")) + '</p>' +
          '<fieldset class="lang-picks"><legend class="vh">' + esc(t("langPref")) + '</legend>' +
            radio("sub", "zh", "中文", !sub || sub.lang === "zh") +
            radio("sub", "en", "English", sub && sub.lang === "en") +
            radio("sub", "both", "双语", sub && sub.lang === "both") +
          '</fieldset>' +
          statusHtml +
          '<div class="feed-row"><a href="/feed.xml">' + esc(t("rss")) + '</a><span aria-hidden="true">·</span><a href="/feed.json">' + esc(t("json")) + '</a></div>' +
        '</form>' +
      '</div>';
    if (focused) {
      const input = subDialog.querySelector("input[type=email]");
      if (input) input.focus();
    }
  }
  function subDismissed() {
    try { return sessionStorage.getItem("yanhua-sub-dismissed") === "1"; }
    catch (err) { return false; }
  }
  function closeSubWindow() {
    try { sessionStorage.setItem("yanhua-sub-dismissed", "1"); } catch (err) {}
    if (subDialog && subDialog.open) subDialog.close();
  }
  function openSubWindow() {
    if (!subDialog || subDialog.open || typeof subDialog.show !== "function") return;
    subDialog.show();
  }
  function maybeOpenSub() {
    if (state.sub || subDismissed()) return;
    openSubWindow();
  }
  function renderStats() {
    if (!statsDialog) return;
    statsDialog.innerHTML =
      '<div class="dialog-head"><h2 id="stats-title">' + esc(t("statsTitle")) + '</h2><button type="button" class="icon-btn" id="close-stats">' + esc(t("close")) + '</button></div>' +
      '<p class="lede">' + esc(t("statsLead")) + '</p>' +
      '<div class="stats-grid">' +
        '<div class="stats-cell"><b data-stat="uv">' + esc(statText("uv")) + '</b><span>' + esc(t("visitors")) + ' UV</span></div>' +
        '<div class="stats-cell"><b data-stat="pv">' + esc(statText("pv")) + '</b><span>' + esc(t("views")) + ' PV</span></div>' +
        '<div class="stats-cell"><b data-stat="subscribers">' + esc(statText("subscribers")) + '</b><span>' + esc(t("subscribers")) + '</span></div>' +
      '</div>' +
      '<div class="stats-grid">' +
        '<div class="stats-cell"><b data-stat="cards">' + esc(statText("cards")) + '</b><span>' + esc(t("totalCards")) + '</span></div>' +
        '<div class="stats-cell"><b data-stat="editions">' + esc(statText("editions")) + '</b><span>' + esc(t("editionCount")) + '</span></div>' +
        '<div class="stats-cell"><b data-stat="papers">' + esc(statText("papers")) + '</b><span>' + esc(t("papersIndexed")) + '</span></div>' +
      '</div>' +
      '<p class="stats-note">' + esc(t("cadence")) + '</p>' +
      engagementHtml() +
      '<p class="stats-links">' +
        '<a href="https://github.com/dexhunter/yanhua.ai/issues?q=label%3Asubscribe" target="_blank" rel="noopener noreferrer">' + esc(t("issueList")) + '</a>' +
        '<a href="https://github.com/dexhunter/yanhua.ai/blob/main/data/config.js" target="_blank" rel="noopener noreferrer">' + esc(t("analyticsConfig")) + '</a>' +
      '</p>';
  }

  function round1(value) {
    return Math.round(value * 10) / 10;
  }
  function scoreOf(row) {
    return round1((row.dwellMs || 0) / 1000 * 0.25) + (row.views || 0) * 2 + (row.flips || 0) * 3 + (row.clicks || 0) * 5 + (row.copies || 0) * 6;
  }
  function finalizeRow(row) {
    row.totalDwellSec = Math.floor((row.dwellMs || 0) / 1000);
    row.avgDwellSec = row.views > 0 ? round1(row.dwellMs / row.views / 1000) : 0;
    row.score = scoreOf(row);
    return row;
  }
  function emptyDelta() {
    return { views: 0, dwellMs: 0, flips: 0, clicks: 0, copies: 0 };
  }
  function touchDelta(id, type, ms) {
    const row = sessionDelta[id] || (sessionDelta[id] = emptyDelta());
    if (type === "view") row.views += 1;
    else if (type === "flip") row.flips += 1;
    else if (type === "click") row.clicks += 1;
    else if (type === "copy") row.copies += 1;
    else if (type === "dwell") row.dwellMs += ms || 0;
  }
  function queueEvent(event) {
    if (!event || !event.id || !event.type) return;
    touchDelta(event.id, event.type, event.ms);
    eventQueue.push(event);
    if (!flushTimer) flushTimer = setTimeout(flushEvents, 3000);
  }
  function flushEvents() {
    if (flushTimer) {
      clearTimeout(flushTimer);
      flushTimer = null;
    }
    if (!eventQueue.length) return Promise.resolve(true);
    const batch = eventQueue.slice();
    eventQueue = [];
    const endpoint = String(config.eventsEndpoint || "").trim();
    if (!endpoint) return Promise.resolve(false);
    return fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ events: batch }),
      keepalive: true
    }).then(function (response) {
      if (!response.ok) throw new Error("event");
      return true;
    }).catch(function () {
      eventQueue = batch.concat(eventQueue);
      return false;
    });
  }
  function snapshotDelta() {
    const copy = {};
    Object.keys(sessionDelta).forEach(function (id) {
      copy[id] = {
        views: sessionDelta[id].views,
        dwellMs: sessionDelta[id].dwellMs,
        flips: sessionDelta[id].flips,
        clicks: sessionDelta[id].clicks,
        copies: sessionDelta[id].copies
      };
    });
    return copy;
  }
  function subtractDelta(base) {
    Object.keys(base).forEach(function (id) {
      const row = sessionDelta[id];
      if (!row) return;
      ["views", "dwellMs", "flips", "clicks", "copies"].forEach(function (key) {
        row[key] = Math.max(0, (row[key] || 0) - (base[id][key] || 0));
      });
      if (!row.views && !row.dwellMs && !row.flips && !row.clicks && !row.copies) delete sessionDelta[id];
    });
  }
  function refreshEngagement() {
    return flushEvents().then(function (ok) {
      const accounted = ok ? snapshotDelta() : null;
      return loadResendStats().then(function () {
        if (accounted) subtractDelta(accounted);
        if (statsDialog && statsDialog.open) renderStats();
      });
    }).catch(function () {});
  }
  function mergedEngagement() {
    const known = {};
    data.items.forEach(function (item) { known[item.id] = true; });
    const map = {};
    (stats.engagement || []).forEach(function (row) {
      if (!row || !known[row.id]) return;
      map[row.id] = {
        id: row.id,
        views: row.views || 0,
        dwellMs: row.dwellMs || 0,
        flips: row.flips || 0,
        clicks: row.clicks || 0,
        copies: row.copies || 0
      };
    });
    Object.keys(sessionDelta).forEach(function (id) {
      if (!known[id]) return;
      if (!map[id]) map[id] = { id: id, views: 0, dwellMs: 0, flips: 0, clicks: 0, copies: 0 };
      const delta = sessionDelta[id];
      map[id].views += delta.views || 0;
      map[id].dwellMs += delta.dwellMs || 0;
      map[id].flips += delta.flips || 0;
      map[id].clicks += delta.clicks || 0;
      map[id].copies += delta.copies || 0;
    });
    return Object.keys(map).map(function (id) { return finalizeRow(map[id]); }).filter(function (row) {
      return row.views || row.dwellMs || row.flips || row.clicks || row.copies;
    }).sort(function (a, b) {
      return b.score - a.score || b.dwellMs - a.dwellMs;
    }).slice(0, 8);
  }
  function engagementHtml() {
    const rows = mergedEngagement();
    const body = rows.length ? '<ol class="rank-list">' + rows.map(function (row) {
      const item = data.items.find(function (candidate) { return candidate.id === row.id; });
      const edition = item ? editionById(item.edition) : null;
      const actions = (row.clicks || 0) + (row.flips || 0);
      return '<li class="rank-row"><div><button type="button" data-open-card="' + esc(row.id) + '">' + esc(item ? tx(item.title) : row.id) + '</button><div class="rank-edition">' + esc(edition ? tx(edition.label) : "") + '</div></div><div class="rank-meta">' + esc(t("rankMeta")(row.views || 0, row.totalDwellSec || 0, actions)) + "</div></li>";
    }).join("") + "</ol>" : '<p class="rank-empty">' + esc(t("mostReadEmpty")) + "</p>";
    return '<section class="card-rank"><h3>' + esc(t("mostRead")) + '</h3><p class="rank-note">' + esc(t("mostReadNote")) + "</p>" + body + "</section>";
  }
  function noteEnter(id) {
    if (!id || document.visibilityState !== "visible" || activeSince[id]) return;
    activeSince[id] = Date.now();
  }
  function noteLeave(id, minMs) {
    const start = activeSince[id];
    if (!start) return;
    delete activeSince[id];
    const elapsed = Date.now() - start;
    if (elapsed < minMs) return;
    if (!viewedOnce[id]) {
      viewedOnce[id] = true;
      queueEvent({ id: id, type: "view" });
    }
    queueEvent({ id: id, type: "dwell", ms: Math.min(180000, elapsed) });
  }
  function leaveAll(minMs) {
    Object.keys(activeSince).forEach(function (id) { noteLeave(id, minMs); });
  }
  function noteFlip() {
    if (state.mode !== "deck") return;
    const list = visible();
    const item = list[state.index];
    if (item) queueEvent({ id: item.id, type: "flip" });
  }
  function cardIdFrom(node) {
    const entry = node.closest(".entry");
    if (entry && entry.id) return entry.id;
    if (node.closest("#deck-stage") || node.closest(".deck-sheet")) {
      const list = visible();
      const item = list[state.index];
      return item ? item.id : "";
    }
    return "";
  }
  function bindReaderWatch() {
    if (readerObserver) readerObserver.disconnect();
    if (!("IntersectionObserver" in window)) return;
    readerObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        const id = entry.target.id;
        if (!id) return;
        if (entry.isIntersecting && entry.intersectionRatio >= 0.55 && document.visibilityState === "visible") noteEnter(id);
        else noteLeave(id, 1800);
      });
    }, { threshold: [0, 0.55, 1] });
    document.querySelectorAll(".entry").forEach(function (node) { readerObserver.observe(node); });
  }
  function syncReading() {
    if (document.visibilityState !== "visible") {
      leaveAll(state.mode === "deck" ? 1500 : 1800);
      return;
    }
    if (state.mode === "deck") {
      if (readerObserver) {
        readerObserver.disconnect();
        readerObserver = null;
      }
      const list = visible();
      const current = list[state.index] ? list[state.index].id : "";
      Object.keys(activeSince).forEach(function (id) {
        if (id !== current) noteLeave(id, 1500);
      });
      if (current) noteEnter(current);
      return;
    }
    Object.keys(activeSince).forEach(function (id) {
      if (!document.getElementById(id)) noteLeave(id, 1800);
    });
    bindReaderWatch();
  }

  function render() {
    try {
      paintChrome();
      renderRail();
      renderMast();
      const list = visible();
      if (state.mode === "deck") renderDeck(list);
      else renderReader(list);
      renderFoot();
      renderSubWindow();
      renderStats();
      syncReading();
    } catch (err) {
      const fallback = document.getElementById("boot-fallback");
      if (fallback) fallback.hidden = false;
    }
  }

  function step(delta) {
    const list = visible();
    const next = state.index + delta;
    if (next < 0 || next >= list.length) return;
    state.index = next;
    state.flipped = false;
    render();
    const stageEl = document.getElementById("deck-stage");
    if (stageEl) stageEl.scrollIntoView({ block: "nearest", behavior: reduced ? "auto" : "smooth" });
  }
  function scrolledPastContent() {
    const content = document.getElementById("content");
    if (!content) return false;
    return window.scrollY > content.getBoundingClientRect().top + window.scrollY + 4;
  }
  function scrollAfterFilter() {
    if (!scrolledPastContent()) return;
    const bar = document.querySelector(".active-filters");
    const edition = state.edition !== "all" ? document.getElementById("edition-" + state.edition) : null;
    const target = bar || edition || document.getElementById("content");
    if (!target) return;
    target.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" });
  }
  function stepReader(delta) {
    const entries = Array.prototype.slice.call(document.querySelectorAll(".entry"));
    if (!entries.length) return;
    const nav = document.querySelector(".nav");
    const anchor = (nav ? nav.getBoundingClientRect().height : 0) + 20;
    let current = entries.findIndex(function (el) {
      return el.classList.contains("is-current") || el === document.activeElement || el.contains(document.activeElement);
    });
    if (current < 0) {
      let best = Infinity;
      entries.forEach(function (el, i) {
        const distance = Math.abs(el.getBoundingClientRect().top - anchor);
        if (distance < best) {
          best = distance;
          current = i;
        }
      });
      if (Math.abs(entries[current].getBoundingClientRect().top - anchor) > 24) {
        markEntry(entries, current);
        return;
      }
    }
    const next = current + delta;
    if (next < 0 || next >= entries.length) return;
    markEntry(entries, next);
  }
  function markEntry(entries, index) {
    entries.forEach(function (el) { el.classList.remove("is-current"); });
    const node = entries[index];
    node.classList.add("is-current");
    node.tabIndex = -1;
    node.focus({ preventScroll: true });
    node.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" });
  }
  function dialogOpen() {
    return (statsDialog && statsDialog.open) || (subDialog && subDialog.open);
  }
  function copyText(text) {
    const fallback = function () {
      return new Promise(function (resolve, reject) {
        const area = document.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.left = "-9999px";
        document.body.appendChild(area);
        area.select();
        const ok = document.execCommand("copy");
        area.remove();
        if (ok) resolve();
        else reject(new Error("copy"));
      });
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(fallback);
    }
    return fallback();
  }

  document.body.addEventListener("click", function (event) {
    const setBtn = event.target.closest("[data-set]");
    if (setBtn) {
      const key = setBtn.dataset.set;
      const value = setBtn.dataset.value;
      if (key === "lang") {
        state.lang = value;
        localStorage.setItem("yanhua-lang", value);
      } else if (key === "mode") {
        leaveAll(state.mode === "deck" ? 1500 : 1800);
        state.mode = value;
        state.flipped = false;
        localStorage.setItem("yanhua-mode", value);
        const modeUrl = new URL(location.href);
        modeUrl.searchParams.set("mode", value);
        history.replaceState(null, "", modeUrl.pathname + modeUrl.search + modeUrl.hash);
      }
      render();
      return;
    }
    if (event.target.closest("#theme-btn")) {
      setScheme(scheme() === "dark" ? "light" : "dark");
      return;
    }
    if (event.target.closest("#close-sub")) {
      closeSubWindow();
      return;
    }
    if (event.target.closest("[data-open-stats]")) {
      openStats();
      return;
    }
    if (event.target.closest("#close-stats")) {
      closeStats();
      return;
    }
    const sourceLink = event.target.closest("a.source-link");
    if (sourceLink) {
      const sourceId = cardIdFrom(sourceLink);
      if (sourceId) queueEvent({ id: sourceId, type: "click" });
    }
    const rankBtn = event.target.closest("[data-open-card]");
    if (rankBtn) {
      const rankId = rankBtn.getAttribute("data-open-card");
      closeStats();
      if (rankId && ensureCardVisible(rankId)) {
        render();
        if (state.mode === "reader") {
          const node = document.getElementById(rankId);
          if (node) node.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" });
        }
      }
      return;
    }
    const copyBtn = event.target.closest("[data-copy-link]");
    if (copyBtn) {
      event.preventDefault();
      const url = copyBtn.getAttribute("data-copy-link");
      const copyId = copyBtn.getAttribute("data-copy-id");
      if (copyId) queueEvent({ id: copyId, type: "copy" });
      try {
        const parsed = new URL(url);
        history.replaceState(null, "", parsed.pathname + parsed.search + parsed.hash);
      } catch (err) {}
      const label = copyBtn.querySelector("span");
      copyText(url).then(function () {
        if (!label || !copyBtn.isConnected) return;
        label.textContent = t("copied");
        copyBtn.classList.add("is-copied");
        window.setTimeout(function () {
          if (!copyBtn.isConnected) return;
          label.textContent = t("copyLink");
          copyBtn.classList.remove("is-copied");
        }, 1600);
      }).catch(function () {});
      return;
    }
    const editionLink = event.target.closest("[data-edition]");
    if (editionLink) {
      event.preventDefault();
      const past = scrolledPastContent();
      state.edition = editionLink.dataset.edition;
      state.index = 0;
      state.flipped = false;
      render();
      if (past) scrollAfterFilter();
      return;
    }
    const tagBtn = event.target.closest("[data-tag]");
    if (tagBtn) {
      const past = scrolledPastContent();
      state.tag = tagBtn.dataset.tag;
      state.index = 0;
      state.flipped = false;
      render();
      if (past) scrollAfterFilter();
      return;
    }
    if (event.target.closest("#clear-filters")) {
      const past = scrolledPastContent();
      state.q = "";
      state.tag = "all";
      state.edition = "all";
      state.index = 0;
      render();
      if (past) scrollAfterFilter();
      return;
    }
    if (event.target.closest("#deck-prev")) { step(-1); return; }
    if (event.target.closest("#deck-next")) { step(1); return; }
    if (event.target.closest(".js-deck-flip")) {
      state.flipped = !state.flipped;
      noteFlip();
      render();
      return;
    }
    if (event.target.closest("#deck-stage")) {
      if (event.target.closest("a, button")) return;
      if (state.suppressFlip) {
        state.suppressFlip = false;
        return;
      }
      state.flipped = !state.flipped;
      noteFlip();
      render();
    }
  });

  document.body.addEventListener("input", function (event) {
    if (event.target.id !== "q") return;
    const y = window.scrollY;
    state.q = event.target.value;
    state.index = 0;
    state.flipped = false;
    render();
    window.scrollTo(0, y);
    const q = document.getElementById("q");
    if (q) {
      q.focus();
      const len = q.value.length;
      q.setSelectionRange(len, len);
    }
  });

  document.body.addEventListener("submit", function (event) {
    const form = event.target.closest(".subscribe-form");
    if (!form) return;
    event.preventDefault();
    const input = form.querySelector("input[type=email]");
    const email = input.value.trim();
    if (!input.checkValidity() || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      input.reportValidity();
      return;
    }
    const langInput = form.querySelector("input[type=radio]:checked");
    const pref = langInput ? langInput.value : "zh";
    subscribe(email, pref, form);
  });

  document.addEventListener("keydown", function (event) {
    if (event.isComposing || event.key === "Process") return;
    const key = event.key;
    const typing = event.target && event.target.closest && event.target.closest("input, textarea, select");
    if (key === "Escape" && event.target && event.target.id === "q") {
      if (!dialogOpen()) event.preventDefault();
      event.target.blur();
      if (!dialogOpen() && filtersActive() && state.q) {
        state.q = "";
        state.index = 0;
        state.flipped = false;
        render();
      }
      return;
    }
    if (typing || dialogOpen()) return;
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (key === "/") {
      event.preventDefault();
      const q = document.getElementById("q");
      if (!q) return;
      q.focus();
      q.select();
      return;
    }
    if (state.mode === "reader") {
      if (key === "j" || key === "J") { event.preventDefault(); stepReader(1); }
      else if (key === "k" || key === "K") { event.preventDefault(); stepReader(-1); }
      return;
    }
    if (state.mode !== "deck") return;
    if (key === "ArrowRight" || key === "j" || key === "J") { event.preventDefault(); step(1); }
    else if (key === "ArrowLeft" || key === "k" || key === "K") { event.preventDefault(); step(-1); }
    else if (key === " " || event.code === "Space" || key === "Enter") {
      if (event.target.closest("button, a")) return;
      event.preventDefault();
      state.flipped = !state.flipped;
      noteFlip();
      render();
    }
  });

  stage.addEventListener("pointerdown", function (event) {
    if (!event.target.closest("#deck-stage")) return;
    pointer = { x: event.clientX, y: event.clientY };
  });
  stage.addEventListener("pointerup", function (event) {
    if (!pointer || state.mode !== "deck") return;
    const dx = event.clientX - pointer.x;
    const dy = event.clientY - pointer.y;
    pointer = null;
    if (Math.abs(dx) < 48 || Math.abs(dx) < Math.abs(dy)) return;
    state.suppressFlip = true;
    step(dx < 0 ? 1 : -1);
  });

  if (!("closedBy" in HTMLDialogElement.prototype)) {
    if (statsDialog) {
      statsDialog.addEventListener("click", function (event) {
        if (event.target !== statsDialog) return;
        const rect = statsDialog.getBoundingClientRect();
        const inside = rect.top <= event.clientY && event.clientY <= rect.bottom && rect.left <= event.clientX && event.clientX <= rect.right;
        if (!inside) statsDialog.close();
      });
    }
  }

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (!localStorage.getItem("yanhua-color-scheme")) paintThemeButton();
  });
  window.addEventListener("storage", function (event) {
    if (event.key === "yanhua-color-scheme") {
      document.querySelector('meta[name="color-scheme"]').content = event.newValue || "light dark";
      paintThemeButton();
    }
  });
  window.addEventListener("hashchange", focusHash);

  function hashCardId() {
    const id = decodeURIComponent(String(location.hash || "").replace(/^#/, ""));
    if (!id || id === "content") return "";
    return data.items.some(function (row) { return row.id === id; }) ? id : "";
  }
  function ensureCardVisible(id) {
    const item = data.items.find(function (row) { return row.id === id; });
    if (!item) return false;
    const shown = visible().some(function (row) { return row.id === id; });
    if (!shown) {
      state.edition = "all";
      state.tag = "all";
      state.q = "";
    }
    const at = visible().findIndex(function (row) { return row.id === id; });
    if (at >= 0) state.index = at;
    state.flipped = false;
    return at >= 0;
  }
  function revealCard(id) {
    if (!ensureCardVisible(id)) return false;
    if (new URLSearchParams(location.search).get("mode") !== "reader") {
      state.mode = "deck";
      localStorage.setItem("yanhua-mode", "deck");
    }
    return true;
  }
  function focusHash() {
    const id = hashCardId();
    if (!id) return;
    const explicitReader = new URLSearchParams(location.search).get("mode") === "reader";
    revealCard(id);
    render();
    if (explicitReader || state.mode === "reader") {
      const node = document.getElementById(id);
      if (node) node.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" });
    }
  }

  async function subscribe(email, pref) {
    const endpoint = (config.subscribeEndpoint || "").trim();
    let delivered = false;
    if (endpoint) {
      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, lang: pref, source: "yanhua.ai" })
        });
        const body = await response.json().catch(function () { return {}; });
        delivered = response.ok && body.ok !== false;
      } catch (err) {
        delivered = false;
      }
    }
    if (delivered) {
      const record = { email: email, lang: pref, at: new Date().toISOString() };
      state.sub = record;
      localStorage.setItem("yanhua-subscription", JSON.stringify(record));
      const list = JSON.parse(localStorage.getItem("yanhua-subscriptions") || "[]");
      list.push(record);
      localStorage.setItem("yanhua-subscriptions", JSON.stringify(list));
      loadResendStats();
    }
    paintStatus(delivered, email, pref);
  }

  function issueUrl(email, pref) {
    const base = config.githubIssueUrl || "https://github.com/dexhunter/yanhua.ai/issues/new";
    const title = "Subscribe: " + email;
    const body = "email: " + email + "\nlang: " + pref + "\nsource: yanhua.ai\n";
    const join = base.indexOf("?") === -1 ? "?" : "&";
    return base + join + "title=" + encodeURIComponent(title) + "&body=" + encodeURIComponent(body) + "&labels=subscribe";
  }

  function safeHost(value) {
    const text = String(value || "").trim().replace(/^https?:\/\//, "").split("/")[0];
    return /^[A-Za-z0-9.-]+$/.test(text) ? text : "";
  }
  function mountExternalAnalytics() {
    const token = String(config.cloudflareBeaconToken || "").trim();
    if (token && !document.querySelector("script[data-cf-beacon]")) {
      const script = document.createElement("script");
      script.defer = true;
      script.src = "https://static.cloudflareinsights.com/beacon.min.js";
      script.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
      document.head.appendChild(script);
    }
    const goatRaw = String(config.goatcounterCode || "").trim();
    if (goatRaw && !document.querySelector("script[data-goatcounter]")) {
      let host = goatRaw.replace(/^https?:\/\//, "").split("/")[0];
      if (host && host.indexOf(".") === -1) host = host + ".goatcounter.com";
      host = safeHost(host);
      if (host) {
        const script = document.createElement("script");
        script.async = true;
        script.src = "https://gc.zgo.at/count.js";
        script.setAttribute("data-goatcounter", "https://" + host + "/count");
        document.head.appendChild(script);
      }
    }
    const domain = safeHost(config.plausibleDomain);
    if (domain && !document.querySelector("script[data-domain='" + domain + "']")) {
      const script = document.createElement("script");
      script.defer = true;
      script.src = "https://plausible.io/js/script.js";
      script.setAttribute("data-domain", domain);
      document.head.appendChild(script);
    }
  }
  async function readCounter(url, increment) {
    const response = await fetch(increment ? VERCOUNT : VERCOUNT + "?url=" + encodeURIComponent(url), increment ? {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    } : { method: "GET" });
    if (!response.ok) throw new Error("counter");
    const body = await response.json();
    return body && body.data ? body.data : null;
  }
  async function loadResendStats() {
    const endpoint = (config.statsEndpoint || "").trim();
    if (!endpoint) return;
    const response = await fetch(endpoint);
    if (!response.ok) return;
    const body = await response.json();
    if (body && typeof body.subscribers === "number") stats.subscribers = body.subscribers;
    if (body && Array.isArray(body.cards)) stats.engagement = body.cards;
    paintStats();
  }
  function applyVisit(visit) {
    if (!visit) return;
    const pagePv = typeof visit.page_pv === "number" ? visit.page_pv : 0;
    const sitePv = typeof visit.site_pv === "number" ? visit.site_pv : 0;
    if (typeof visit.site_pv === "number") stats.pv = visit.site_pv;
    if (typeof visit.site_uv !== "number") return;
    if (visit.site_uv === 0 && (pagePv > 0 || sitePv > 0)) {
      const basis = pagePv || sitePv;
      stats.uv = sitePv > 0 ? Math.min(basis, sitePv) : basis;
      return;
    }
    stats.uv = visit.site_uv;
  }
  async function loadStats() {
    const visitUrl = SITE + "/";
    try {
      const visit = await readCounter(visitUrl, true);
      applyVisit(visit);
    } catch (err) {
      try {
        const visit = await readCounter(visitUrl, false);
        applyVisit(visit);
      } catch (again) {}
    }
    try {
      await loadResendStats();
    } catch (err) {}
    paintStats();
  }
  function setStatsParam(on) {
    const url = new URL(location.href);
    if (on) url.searchParams.set("stats", "1");
    else url.searchParams.delete("stats");
    history.replaceState(null, "", url.pathname + url.search + url.hash);
  }
  function openStats() {
    if (!statsDialog) return;
    renderStats();
    if (!statsDialog.open) statsDialog.showModal();
    setStatsParam(true);
    refreshEngagement();
  }
  function closeStats() {
    if (statsDialog && statsDialog.open) statsDialog.close();
    setStatsParam(false);
  }

  function paintStatus(delivered, email, pref) {
    document.querySelectorAll(".subscribe-form .status").forEach(function (node) {
      if (delivered) {
        node.textContent = t("sent");
        return;
      }
      const bits = ['<span>' + esc(t("failed")) + '</span>'];
      bits.push('<a href="' + esc(issueUrl(email, pref)) + '" target="_blank" rel="noopener noreferrer">' + esc(t("github")) + '</a>');
      node.innerHTML = bits.join(" ");
    });
  }

  if (statsDialog) {
    statsDialog.addEventListener("close", function () {
      const url = new URL(location.href);
      if (url.searchParams.get("stats") !== "1") return;
      url.searchParams.delete("stats");
      history.replaceState(null, "", url.pathname + url.search + url.hash);
    });
  }
  if (subDialog) {
    subDialog.addEventListener("close", function () {
      try { sessionStorage.setItem("yanhua-sub-dismissed", "1"); } catch (err) {}
    });
  }
  mountExternalAnalytics();
  if (hashCardId()) revealCard(hashCardId());
  render();
  loadStats();
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") {
      leaveAll(state.mode === "deck" ? 1500 : 1800);
      flushEvents();
    } else {
      syncReading();
    }
  });
  window.addEventListener("pagehide", function () {
    leaveAll(state.mode === "deck" ? 1500 : 1800);
    flushEvents();
  });
  if (subDialog && "IntersectionObserver" in window) {
    const footer = document.getElementById("foot");
    if (footer) {
      const subObserver = new IntersectionObserver(function (entries) {
        if (entries.some(function (entry) { return entry.isIntersecting; })) maybeOpenSub();
      }, { rootMargin: "0px 0px 260px 0px" });
      subObserver.observe(footer);
    }
  } else {
    window.addEventListener("scroll", function () {
      if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 260) maybeOpenSub();
    }, { passive: true });
  }
  if (new URLSearchParams(location.search).get("stats") === "1") openStats();
  focusHash();
})();
