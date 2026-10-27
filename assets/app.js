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
      subscribeLead: "留下邮箱。日报用中文写成，也可以只收英文，或两份都收。",
      toastTitle: "订阅演化日报",
      toastLead: "觉得有用？留下邮箱，每日更新直达收件箱。",
      dismiss: "关闭",
      slipTitle: "订阅日报",
      slipBody: "每天一版。中文为主，可选英文或双语。RSS 同样开放。",
      email: "邮箱",
      emailPh: "you@lab.edu",
      langPref: "语言偏好",
      zh: "中文",
      en: "English",
      both: "双语",
      invalid: "请输入有效的邮箱地址。",
      saved: "已记下。这台浏览器会记住你的订阅。",
      sent: "订阅请求已送达。这台浏览器也记住了你的选择。",
      fallback: "在线名册还没有接上。地址已经保存在这台设备上，也可以从这里送出。",
      github: "通过 GitHub Issue 送出",
      mailto: "用邮件送出",
      close: "关闭",
      themeDark: "切换到深色",
      themeLight: "切换到浅色",
      searchLabel: "搜索",
      searchPh: "搜索标题、arXiv、作者",
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
      frontHint: "按 Space 或 Enter，或点击卡片，翻到问题与机制。",
      backHint: "按 Space 或 Enter，返回结论与指标。",
      keys: "Space / Enter 翻转卡片 · J / K 或 ← / → 上一张 / 下一张",
      emptyTitle: "没有匹配的卡片",
      emptyBody: "换一个关键词，或清除筛选。",
      clear: "清除筛选",
      count: function (n) { return n + " 篇"; },
      progress: function (i, n) { return i + " / " + n; },
      footer: "演化日报记录递归自我改进与智能体框架搜索。权重可以冻结，核对不能交给正在被优化的那一方。",
      feeds: "订阅源",
      rss: "RSS",
      json: "JSON",
      paper: "论文",
      source: "来源",
      visitors: "访客",
      views: "阅读",
      subscribers: "订阅",
      statsTitle: "站点统计",
      statsLead: "访客和阅读来自公开计数器。订阅数是 Resend 名册里的人数。",
      totalCards: "卡片总数",
      editionCount: "期数",
      papersIndexed: "收录论文",
      cadence: "yanhua.ai 每天更新两次，伦敦时间 09:00 与 18:00。早晚两版合在当晚的每日邮件摘要里寄出。",
      failed: "没有送出。请再试一次。",
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
      subscribeLead: "Leave an email. The daily is written in Chinese. You can take English only, or both.",
      toastTitle: "Subscribe to Yanhua Daily",
      toastLead: "Enjoying the cards? Get new editions by email.",
      dismiss: "Dismiss",
      slipTitle: "Subscribe",
      slipBody: "One edition a day. Chinese by default, English or bilingual if you prefer. RSS is open too.",
      email: "Email",
      emailPh: "you@lab.edu",
      langPref: "Language preference",
      zh: "中文",
      en: "English",
      both: "Bilingual",
      invalid: "Enter a valid email address.",
      saved: "Saved. This browser will remember your subscription.",
      sent: "The subscription request was delivered. This browser remembers your choice too.",
      fallback: "The online list is not connected yet. The address is saved on this device, and you can send it from here.",
      github: "Send via GitHub Issue",
      mailto: "Send by email",
      close: "Close",
      themeDark: "Switch to dark",
      themeLight: "Switch to light",
      searchLabel: "Search",
      searchPh: "Search titles, arXiv ids, authors",
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
      frontHint: "Press Space or Enter, or click the card, for the problem and the mechanism.",
      backHint: "Press Space or Enter to return to the conclusion and the numbers.",
      keys: "Space / Enter flips the card · J / K or ← / → previous / next",
      emptyTitle: "No cards match",
      emptyBody: "Try another query, or clear the filters.",
      clear: "Clear filters",
      count: function (n) { return n === 1 ? "1 card" : n + " cards"; },
      progress: function (i, n) { return i + " / " + n; },
      footer: "Yanhua Daily records recursive self-improvement and agent harness search. Weights may stay frozen. The check must not belong to the thing being optimized.",
      feeds: "Feeds",
      rss: "RSS",
      json: "JSON",
      paper: "Paper",
      source: "Source",
      visitors: "Visitors",
      views: "Views",
      subscribers: "Subscribers",
      statsTitle: "Site analytics",
      statsLead: "Visitors and views come from a public counter. Subscribers is the Resend audience count.",
      totalCards: "Total cards",
      editionCount: "Editions",
      papersIndexed: "Papers indexed",
      cadence: "yanhua.ai updates twice a day, at 09:00 and 18:00 London time. Both editions are combined into the evening daily email digest.",
      failed: "That did not go through. Try again.",
      issueList: "View subscriptions on GitHub",
      analyticsConfig: "Configure external analytics"
    }
  };

  const state = {
    lang: document.documentElement.lang === "en" ? "en" : "zh",
    mode: localStorage.getItem("yanhua-mode") === "deck" ? "deck" : "reader",
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
  const stats = { uv: null, pv: null, subscribers: null, cards: null, editions: null, papers: null };
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
    const posts = {};
    raw.forEach(function (link) {
      if (!link || !link.url) return;
      const match = X_URL.exec(link.url);
      if (match) {
        const key = match[1].toLowerCase();
        const prev = posts[key];
        if (!prev || (match[2] && String(prev.url).indexOf("/status/") === -1)) {
          posts[key] = { handle: match[1], url: link.url };
        }
        return;
      }
      docs.push(link);
    });
    String(item.handle || "").replace(/@([A-Za-z0-9_]{1,15})/g, function (full, name, offset, whole) {
      if (!isHandleMention(whole, offset, name)) return full;
      const key = name.toLowerCase();
      if (!posts[key]) posts[key] = { handle: name, url: "https://x.com/" + name };
      return "";
    });
    return { docs: docs, posts: Object.keys(posts).map(function (key) { return posts[key]; }) };
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
  function sources(item) {
    const bag = sourceBag(item);
    const parts = bag.docs.map(function (link) {
      return sourceAnchor(link.url, sourceKind(link), sourceText(link));
    }).concat(bag.posts.map(function (post) {
      return sourceAnchor(post.url, "x", "@" + post.handle);
    }));
    return parts.length ? '<div class="source-row">' + parts.join("") + "</div>" : "";
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
    if (item.arxiv) bits.push('<a href="https://arxiv.org/abs/' + esc(item.arxiv) + '" target="_blank" rel="noopener noreferrer">' + esc(item.arxiv) + '</a>');
    if (item.authors) bits.push(esc(item.authors));
    if (item.handle) bits.push(linkify(item.handle, item));
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
    const openSub = document.getElementById("open-sub");
    if (openSub) openSub.textContent = t("subscribe");
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

  function renderRail() {
    if (!rail) return;
    const editions = data.editions.map(function (edition) {
      const current = state.edition === edition.id ? ' aria-current="page"' : "";
      return '<a href="#edition-' + esc(edition.id) + '" data-edition="' + esc(edition.id) + '"' + current + '>' + esc(tx(edition.label)) + '</a>';
    }).join("");
    const tags = data.tags.map(function (tag) {
      return '<button type="button" class="chip" data-tag="' + esc(tag.id) + '" aria-pressed="' + (state.tag === tag.id) + '">' + esc(tx(tag.label)) + '</button>';
    }).join("");
    rail.innerHTML =
      '<label for="q">' + esc(t("searchLabel")) + '</label>' +
      '<input class="search" id="q" type="search" placeholder="' + esc(t("searchPh")) + '" value="' + esc(state.q) + '">' +
      '<h2>' + esc(t("editions")) + '</h2>' +
      '<div class="rail-list"><a href="#content" data-edition="all"' + (state.edition === "all" ? ' aria-current="page"' : "") + '>' + esc(t("allEditions")) + '</a>' + editions + '</div>' +
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
    const list = visible();
    const latest = data.editions[0];
    mast.innerHTML =
      '<h1>' + esc(tx(data.site.title)) + '</h1>' +
      '<p class="lede">' + esc(tx(data.site.tagline)) + (state.lang === "zh" ? "。" : ". ") + esc(tx(data.site.description)) + '</p>' +
      '<p class="meta-line"><span>' + esc(tx(latest.label)) + '  ·  ' + esc(t("count")(list.length)) + '</span>' + statsStrip() + '</p>';
  }

  function renderReader(list) {
    if (!stage) return;
    if (!list.length) {
      stage.innerHTML = empty();
      return;
    }
    const groups = [];
    data.editions.forEach(function (edition) {
      const rows = list.filter(function (item) { return item.edition === edition.id; });
      if (!rows.length) return;
      groups.push(
        '<section class="edition-block" id="edition-' + esc(edition.id) + '">' +
          '<h2>' + esc(tx(edition.label)) + '</h2>' +
          '<div class="edition-count">' + esc(t("count")(rows.length)) + '</div>' +
          rows.map(article).join("") +
        '</section>'
      );
    });
    stage.innerHTML = groups.join("");
  }
  function article(item) {
    return '<article class="entry" id="' + esc(item.id) + '">' +
      '<div class="entry-top"><div><h3><a href="#' + esc(item.id) + '">' + esc(tx(item.title)) + '</a></h3>' + byline(item) + '</div></div>' +
      verdict(item) + pills(item) + contextGrid(item) + sources(item) +
      '</article>';
  }
  function empty() {
    return '<div class="empty"><p>' + esc(t("emptyTitle")) + '</p><p>' + esc(t("emptyBody")) + '</p><button type="button" class="btn" id="clear-filters">' + esc(t("clear")) + '</button></div>';
  }

  function renderDeck(list) {
    if (!stage) return;
    if (!list.length) {
      stage.innerHTML = empty();
      return;
    }
    if (state.index >= list.length) state.index = 0;
    const item = list[state.index];
    const edition = editionById(item.edition);
    const frontHidden = state.flipped ? " inert" : "";
    const backHidden = state.flipped ? "" : " inert";
    stage.innerHTML =
      '<div class="deck-toolbar"><p class="deck-progress">' + esc(tx(edition.label)) + '  ·  ' + esc(t("progress")(state.index + 1, list.length)) + '</p><p class="keys">' + esc(t("keys")) + '</p></div>' +
      '<div class="deck-stage' + (state.flipped ? " is-flipped" : "") + '" id="deck-stage">' +
        '<div class="deck-spin">' +
          '<article class="face face-front deck-sheet" id="' + esc(item.id) + '"' + frontHidden + '>' +
            '<h2>' + esc(tx(item.title)) + '</h2>' +
            byline(item) +
            verdict(item) +
            pills(item) +
            '<p class="hint">' + esc(t("frontHint")) + '</p>' +
            deckActions(item) +
          '</article>' +
          '<article class="face face-back deck-sheet"' + backHidden + '>' +
            '<h2>' + esc(tx(item.title)) + '</h2>' +
            '<p class="deck-kicker">' + esc(tx(edition.label)) + '</p>' +
            contextGrid(item) +
            '<p class="hint">' + esc(t("backHint")) + '</p>' +
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
    foot.innerHTML = '<div class="colophon-inner"><p>' + esc(t("footer")) + '</p><div class="foot-stats">' + statsStrip() + '</div><p class="feed-row"><a href="/feed.xml">' + esc(t("rss")) + '</a><a href="/feed.json">' + esc(t("json")) + '</a></p></div>';
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
      '<p class="stats-links">' +
        '<a href="https://github.com/dexhunter/yanhua.ai/issues?q=label%3Asubscribe" target="_blank" rel="noopener noreferrer">' + esc(t("issueList")) + '</a>' +
        '<a href="https://github.com/dexhunter/yanhua.ai/blob/main/data/config.js" target="_blank" rel="noopener noreferrer">' + esc(t("analyticsConfig")) + '</a>' +
      '</p>';
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

  document.body.addEventListener("click", function (event) {
    const setBtn = event.target.closest("[data-set]");
    if (setBtn) {
      const key = setBtn.dataset.set;
      const value = setBtn.dataset.value;
      if (key === "lang") {
        state.lang = value;
        localStorage.setItem("yanhua-lang", value);
      } else if (key === "mode") {
        state.mode = value;
        state.flipped = false;
        localStorage.setItem("yanhua-mode", value);
      }
      render();
      return;
    }
    if (event.target.closest("#theme-btn")) {
      setScheme(scheme() === "dark" ? "light" : "dark");
      return;
    }
    if (event.target.closest("#open-sub")) {
      openSubWindow();
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
    const editionLink = event.target.closest("[data-edition]");
    if (editionLink) {
      state.edition = editionLink.dataset.edition;
      state.index = 0;
      state.flipped = false;
      render();
      return;
    }
    const tagBtn = event.target.closest("[data-tag]");
    if (tagBtn) {
      state.tag = tagBtn.dataset.tag;
      state.index = 0;
      state.flipped = false;
      render();
      return;
    }
    if (event.target.closest("#clear-filters")) {
      state.q = "";
      state.tag = "all";
      state.edition = "all";
      state.index = 0;
      render();
      return;
    }
    if (event.target.closest("#deck-prev")) { step(-1); return; }
    if (event.target.closest("#deck-next")) { step(1); return; }
    if (event.target.closest(".js-deck-flip")) {
      state.flipped = !state.flipped;
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
    const typing = event.target.closest("input, textarea, select");
    if (typing) return;
    if (state.mode !== "deck") return;
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const key = event.key;
    if (key === "ArrowRight" || key === "j" || key === "J") { event.preventDefault(); step(1); }
    else if (key === "ArrowLeft" || key === "k" || key === "K") { event.preventDefault(); step(-1); }
    else if (key === " " || event.code === "Space" || key === "Enter") {
      if (event.target.closest("button, a")) return;
      event.preventDefault();
      state.flipped = !state.flipped;
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

  function focusHash() {
    const id = decodeURIComponent(location.hash.replace("#", ""));
    if (!id || id === "content") return;
    const item = data.items.find(function (row) { return row.id === id; });
    if (!item) return;
    if (state.mode === "deck") {
      const list = visible();
      const at = list.findIndex(function (row) { return row.id === id; });
      if (at >= 0) state.index = at;
      render();
    }
    const node = document.getElementById(id);
    if (node) node.scrollIntoView({ block: "start" });
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
    paintStats();
  }
  async function loadStats() {
    const visitUrl = SITE + "/";
    try {
      const visit = await readCounter(visitUrl, true);
      if (visit) {
        if (typeof visit.site_uv === "number") stats.uv = visit.site_uv;
        if (typeof visit.site_pv === "number") stats.pv = visit.site_pv;
      }
    } catch (err) {
      try {
        const visit = await readCounter(visitUrl, false);
        if (visit) {
          if (typeof visit.site_uv === "number") stats.uv = visit.site_uv;
          if (typeof visit.site_pv === "number") stats.pv = visit.site_pv;
        }
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
  render();
  loadStats();
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
