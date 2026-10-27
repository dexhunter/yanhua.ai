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
      savedOnly: "只看收藏",
      what: "01  问题与定位",
      how: "02  核心机制",
      why: "03  核心结论与深层原因",
      read: "标为已读",
      unread: "标为未读",
      readMark: "已读",
      save: "收藏",
      savedMark: "已收藏",
      prev: "上一张",
      next: "下一张",
      flip: "翻面",
      frontHint: "空格或点击卡片，翻到机制与结论。",
      backHint: "空格返回问题与指标。",
      keys: "← → 换卡   空格翻面",
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
      source: "来源"
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
      savedOnly: "Bookmarks",
      what: "01  Problem",
      how: "02  Mechanism",
      why: "03  Conclusion and why",
      read: "Mark read",
      unread: "Mark unread",
      readMark: "Read",
      save: "Bookmark",
      savedMark: "Bookmarked",
      prev: "Previous",
      next: "Next",
      flip: "Flip",
      frontHint: "Press space or click the card for the mechanism and the conclusion.",
      backHint: "Press space to return to the problem and the numbers.",
      keys: "← → next card    Space flip",
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
      source: "Source"
    }
  };

  const state = {
    lang: document.documentElement.lang === "en" ? "en" : "zh",
    mode: localStorage.getItem("yanhua-mode") === "deck" ? "deck" : "reader",
    edition: "all",
    tag: "all",
    q: "",
    savedOnly: false,
    index: 0,
    flipped: false,
    read: loadSet("yanhua-read"),
    saved: loadSet("yanhua-bookmarks"),
    sub: loadSub()
  };

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const stage = document.getElementById("stage");
  const mast = document.getElementById("mast");
  const rail = document.getElementById("rail");
  const foot = document.getElementById("foot");
  const dialog = document.getElementById("sub-dialog");
  let pointer = null;

  function loadSet(key) {
    try { return new Set(JSON.parse(localStorage.getItem(key) || "[]")); }
    catch (err) { return new Set(); }
  }
  function storeSet(key, set) {
    localStorage.setItem(key, JSON.stringify(Array.from(set)));
  }
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
  function paragraphs(text) {
    return String(text).split(/\n\n+/).filter(Boolean).map(function (part) {
      return "<p>" + esc(part.trim()) + "</p>";
    }).join("");
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
    if (state.savedOnly && !state.saved.has(item.id)) return false;
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
  function links(item) {
    return (item.links || []).map(function (itemLink) {
      return '<a href="' + esc(itemLink.url) + '" target="_blank" rel="noopener noreferrer">' + esc(tx(itemLink)) + '</a>';
    }).join("");
  }
  function byline(item) {
    const bits = [];
    if (item.arxiv) bits.push('<a href="https://arxiv.org/abs/' + esc(item.arxiv) + '" target="_blank" rel="noopener noreferrer">' + esc(item.arxiv) + '</a>');
    if (item.authors) bits.push(esc(item.authors));
    if (item.handle) bits.push(esc(item.handle));
    return bits.length ? '<p class="byline">' + bits.join(" · ") + "</p>" : "";
  }
  function beats(item) {
    return '<div class="beats">' +
      '<section class="beat"><h4>' + esc(t("what")) + '</h4>' + paragraphs(tx(item.what)) + '</section>' +
      '<section class="beat"><h4>' + esc(t("how")) + '</h4>' + paragraphs(tx(item.how)) + '</section>' +
      '<section class="beat why"><h4>' + esc(t("why")) + '</h4>' + paragraphs(tx(item.why)) + '</section>' +
      '</div>';
  }
  function actions(item) {
    const read = state.read.has(item.id);
    const saved = state.saved.has(item.id);
    return '<div class="entry-actions">' +
      '<div class="links">' + links(item) + '</div>' +
      '<button type="button" class="text-btn" data-act="read" data-id="' + esc(item.id) + '" aria-pressed="' + read + '">' + esc(read ? t("readMark") : t("read")) + '</button>' +
      '<button type="button" class="text-btn" data-act="save" data-id="' + esc(item.id) + '" aria-pressed="' + saved + '">' + esc(saved ? t("savedMark") : t("save")) + '</button>' +
      '</div>';
  }

  function slip(idPrefix) {
    const sub = state.sub;
    const status = sub ? '<p class="status" role="status">' + esc(t("saved")) + '</p>' : '<p class="status" role="status"></p>';
    return '<form class="slip subscribe-form" data-prefix="' + idPrefix + '">' +
      '<div class="slip-copy"><strong>' + esc(t("slipTitle")) + '</strong><p>' + esc(t("slipBody")) + '</p></div>' +
      '<div class="slip-row">' +
        '<label class="vh" for="' + idPrefix + '-email">' + esc(t("email")) + '</label>' +
        '<input id="' + idPrefix + '-email" name="email" type="email" required autocomplete="email" inputmode="email" placeholder="' + esc(t("emailPh")) + '" value="' + esc(sub ? sub.email : "") + '">' +
        '<button class="btn-primary" type="submit">' + esc(t("subscribe")) + '</button>' +
      '</div>' +
      '<p class="field-error">' + esc(t("invalid")) + '</p>' +
      '<fieldset class="lang-picks"><legend class="vh">' + esc(t("langPref")) + '</legend>' +
        radio(idPrefix, "zh", t("zh"), !sub || sub.lang === "zh") +
        radio(idPrefix, "en", t("en"), sub && sub.lang === "en") +
        radio(idPrefix, "both", t("both"), sub && sub.lang === "both") +
      '</fieldset>' +
      status +
      '<div class="feed-row"><span>' + esc(t("feeds")) + '</span><a href="/feed.xml">' + esc(t("rss")) + '</a><a href="/feed.json">' + esc(t("json")) + '</a></div>' +
      '</form>';
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
    document.getElementById("skip-link").textContent = t("skip");
    document.getElementById("mode-switch").setAttribute("aria-label", t("modeLabel"));
    document.getElementById("lang-switch").setAttribute("aria-label", t("langLabel"));
    document.getElementById("mode-switch").innerHTML =
      seg("mode", "reader", t("reader"), state.mode === "reader") +
      seg("mode", "deck", t("deck"), state.mode === "deck");
    document.getElementById("lang-switch").innerHTML =
      seg("lang", "zh", "中文", state.lang === "zh") +
      seg("lang", "en", "EN", state.lang === "en");
    document.getElementById("open-sub").textContent = t("subscribe");
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
      '<div class="rail-list"><button type="button" class="chip" data-tag="all" aria-pressed="' + (state.tag === "all") + '">' + esc(t("allTopics")) + '</button>' + tags + '</div>' +
      '<h2>' + esc(t("save")) + '</h2>' +
      '<button type="button" class="chip" id="saved-only" aria-pressed="' + state.savedOnly + '">' + esc(t("savedOnly")) + '</button>';
  }

  function renderMast() {
    const list = visible();
    const latest = data.editions[0];
    mast.innerHTML =
      '<h1>' + esc(tx(data.site.title)) + '</h1>' +
      '<p class="lede">' + esc(tx(data.site.tagline)) + (state.lang === "zh" ? "。" : ". ") + esc(tx(data.site.description)) + '</p>' +
      '<p class="meta-line">' + esc(tx(latest.label)) + '  ·  ' + esc(t("count")(list.length)) + '</p>' +
      slip("hero");
  }

  function renderReader(list) {
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
      pills(item) + beats(item) + actions(item) +
      '</article>';
  }
  function empty() {
    return '<div class="empty"><p>' + esc(t("emptyTitle")) + '</p><p>' + esc(t("emptyBody")) + '</p><button type="button" class="btn" id="clear-filters">' + esc(t("clear")) + '</button></div>';
  }

  function renderDeck(list) {
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
            '<p class="deck-kicker">' + esc(tx(item.metric)) + '</p>' +
            '<h2>' + esc(tx(item.title)) + '</h2>' +
            byline(item) + pills(item) +
            '<section class="beat"><h4>' + esc(t("what")) + '</h4>' + paragraphs(tx(item.what)) + '</section>' +
            '<p class="hint">' + esc(t("frontHint")) + '</p>' +
          '</article>' +
          '<article class="face face-back deck-sheet"' + backHidden + '>' +
            '<p class="deck-kicker">' + esc(tx(edition.label)) + '</p>' +
            '<h2>' + esc(tx(item.title)) + '</h2>' +
            '<section class="beat"><h4>' + esc(t("how")) + '</h4>' + paragraphs(tx(item.how)) + '</section>' +
            '<section class="beat why"><h4>' + esc(t("why")) + '</h4>' + paragraphs(tx(item.why)) + '</section>' +
            '<p class="hint">' + esc(t("backHint")) + '</p>' +
          '</article>' +
        '</div>' +
      '</div>' +
      '<div class="deck-nav">' +
        '<button type="button" class="btn" id="deck-prev"' + (state.index === 0 ? " disabled" : "") + '>' + esc(t("prev")) + '</button>' +
        '<button type="button" class="btn-primary" id="deck-flip">' + esc(t("flip")) + '</button>' +
        '<button type="button" class="btn" id="deck-next"' + (state.index === list.length - 1 ? " disabled" : "") + '>' + esc(t("next")) + '</button>' +
      '</div>' +
      actions(item);
  }

  function renderFoot() {
    foot.innerHTML = '<div class="colophon-inner"><p>' + esc(t("footer")) + '</p>' + slip("foot") + '</div>';
  }
  function renderDialog() {
    dialog.innerHTML =
      '<div class="dialog-head"><h2 id="sub-title">' + esc(t("subscribeTitle")) + '</h2><button type="button" class="icon-btn" id="close-sub">' + esc(t("close")) + '</button></div>' +
      '<p class="lede">' + esc(t("subscribeLead")) + '</p>' +
      slip("dlg");
  }

  function render() {
    paintChrome();
    renderRail();
    renderMast();
    const list = visible();
    if (state.mode === "deck") renderDeck(list);
    else renderReader(list);
    renderFoot();
    renderDialog();
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
      renderDialog();
      dialog.showModal();
      const input = dialog.querySelector("input[type=email]");
      if (input) input.focus();
      return;
    }
    if (event.target.closest("#close-sub")) {
      dialog.close();
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
    if (event.target.closest("#saved-only")) {
      state.savedOnly = !state.savedOnly;
      state.index = 0;
      render();
      return;
    }
    if (event.target.closest("#clear-filters")) {
      state.q = "";
      state.tag = "all";
      state.edition = "all";
      state.savedOnly = false;
      state.index = 0;
      render();
      return;
    }
    const act = event.target.closest("[data-act]");
    if (act) {
      const set = act.dataset.act === "read" ? state.read : state.saved;
      const key = act.dataset.act === "read" ? "yanhua-read" : "yanhua-bookmarks";
      if (set.has(act.dataset.id)) set.delete(act.dataset.id);
      else set.add(act.dataset.id);
      storeSet(key, set);
      render();
      return;
    }
    if (event.target.closest("#deck-prev")) { step(-1); return; }
    if (event.target.closest("#deck-next")) { step(1); return; }
    if (event.target.closest("#deck-flip")) {
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
    if (event.key === "ArrowRight") { event.preventDefault(); step(1); }
    else if (event.key === "ArrowLeft") { event.preventDefault(); step(-1); }
    else if (event.key === " " || event.code === "Space") { event.preventDefault(); state.flipped = !state.flipped; render(); }
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
    dialog.addEventListener("click", function (event) {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      const inside = rect.top <= event.clientY && event.clientY <= rect.bottom && rect.left <= event.clientX && event.clientX <= rect.right;
      if (!inside) dialog.close();
    });
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

  async function subscribe(email, pref, form) {
    const record = { email: email, lang: pref, at: new Date().toISOString() };
    state.sub = record;
    localStorage.setItem("yanhua-subscription", JSON.stringify(record));
    const list = JSON.parse(localStorage.getItem("yanhua-subscriptions") || "[]");
    list.push(record);
    localStorage.setItem("yanhua-subscriptions", JSON.stringify(list));

    const endpoint = (config.subscribeEndpoint || "").trim();
    let delivered = false;
    if (endpoint) {
      try {
        const format = config.subscribeFormat === "form" ? "form" : "json";
        const payload = Object.assign({ email: email, lang: pref, source: "yanhua.ai" }, config.extraFields || {});
        const headers = Object.assign({}, config.subscribeHeaders || {});
        let body;
        if (format === "form") body = new URLSearchParams(payload);
        else {
          headers["Content-Type"] = "application/json";
          body = JSON.stringify(payload);
        }
        const response = await fetch(endpoint, {
          method: config.subscribeMethod || "POST",
          headers: headers,
          body: body
        });
        delivered = response.ok;
      } catch (err) {
        delivered = false;
      }
    }
    paintStatus(delivered, email, pref);
  }

  function issueUrl(email, pref) {
    const base = config.githubIssueUrl || "https://github.com/dexhunter/yanhua.ai/issues/new";
    const title = "Subscribe: " + email;
    const body = "email: " + email + "\nlang: " + pref + "\nsource: yanhua.ai\n";
    const join = base.indexOf("?") === -1 ? "?" : "&";
    return base + join + "title=" + encodeURIComponent(title) + "&body=" + encodeURIComponent(body);
  }

  function paintStatus(delivered, email, pref) {
    document.querySelectorAll(".subscribe-form .status").forEach(function (node) {
      if (delivered) {
        node.textContent = t("sent");
        return;
      }
      const bits = ['<span>' + esc(endpointMissing() ? t("fallback") : t("saved")) + '</span>'];
      if (!delivered) {
        bits.push('<a href="' + esc(issueUrl(email, pref)) + '" target="_blank" rel="noopener noreferrer">' + esc(t("github")) + '</a>');
        if (config.mailto) {
          bits.push('<a href="mailto:' + esc(config.mailto) + '?subject=' + encodeURIComponent("Subscribe " + email) + '&body=' + encodeURIComponent(email + "\n" + pref) + '">' + esc(t("mailto")) + '</a>');
        }
        if (config.substackUrl) bits.push('<a href="' + esc(config.substackUrl) + '" target="_blank" rel="noopener noreferrer">Substack</a>');
      }
      node.innerHTML = bits.join(" ");
    });
  }
  function endpointMissing() {
    return !(config.subscribeEndpoint || "").trim();
  }

  render();
  focusHash();
})();
