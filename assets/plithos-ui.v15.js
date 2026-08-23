/* Plithos shared UI.
 *
 * Two things every page gets, without touching that page's own code:
 *
 *   1. The search. There is one on this site and this is it: Ctrl/Cmd-K, or
 *      "/", from any page. It reaches saints, prayers, library works,
 *      scripture books, glossary terms, the tags the Library shelf is sorted
 *      by, and the words inside the books themselves. Each page holds only
 *      its own dataset inline and cannot see the others', so the palette
 *      fetches data/search-index.v9.json, once, on first open.
 *
 *      That index carries what things are called, not what they say. The
 *      words of the Fathers are five megabytes and cannot travel to every
 *      page, so the Library lends its own full-text search to this box
 *      through window.PLITHOS_BOOKS while the reader is on the Library, and
 *      from anywhere else the box offers to take him there with the question
 *      already asked. See insideTheBooks() below.
 *
 *      A tag result opens the shelf already narrowed to it, so a subject, an
 *      author, a century, a purpose or a translator can be reached from any
 *      page on the site and everything filed under it comes back together.
 *
 *   2. A dark theme toggle. The pages all declare the same custom properties,
 *      so assets/plithos-ui.css re-themes them by overriding those tokens.
 *
 *   3. A check that the page in front of the reader is the page we publish.
 *      A browser can hold a page long after it has been replaced, and a
 *      reader has no way to tell. See freshen() below.
 *
 * ES5-flavoured to match the house style in the app pages. No dependencies.
 */
(function () {
  "use strict";

  var INDEX_URL = "data/search-index.v9.json";
  var THEME_KEY = "plithos.theme";
  var LANG_KEY = "plithos.lang";
  var BUILD_URL = "/version.json";
  var BUILD_KEY = "plithos.freshened";

  /* ------------------------------------------------------------------ words */

  /* Everything the shared chrome says to a reader is held here rather than
     written into the markup below, so a language can be added by supplying
     one file and changing nothing else. English is the fallback and is kept
     inline, so it costs no request and survives a failed one.

     data/ui-i18n.v5.en.json is the same table as a file: it is the sheet a
     translator copies. The other languages are read from
     data/ui-i18n.v5.<code>.json, fetched once beside the index.

     "tags" carries the names of the tags on the Library shelf, keyed by the
     dimension and value the shelf filters on rather than by the English word,
     so a translated name still opens the right shelf. Anything missing from a
     bundle falls back to English rather than to nothing. */
  var EN = {
    searchAria: "Search everything",
    searchPlaceholder: "Search saints, prayers, the Fathers, scripture, terms",
    searchLabel: "Search",
    esc: "Esc",
    hintMove: "move",
    hintOpen: "open",
    hintClose: "close",
    nothingFound: "Nothing found for",
    themeDark: "Dark theme",
    themeLight: "Light theme",
    toDark: "Switch to dark theme",
    toLight: "Switch to light theme",
    home: "Plithos home",
    language: "Language",
    title: "title",
    titles: "titles",
    months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    groups: { s: "Saints", w: "Library", p: "Prayers",
              b: "Scripture", g: "Glossary", t: "On the shelf",
              x: "Inside the books" },
    searchBooks: "Search every word of the Fathers for",
    counts: { s: "saints", w: "works", p: "prayers",
              b: "books of scripture", g: "glossary terms", t: "tags" },
    dims: { topics: "Subject", author: "Author", century: "Century",
            purpose: "Purpose", translator: "Translator" },
    tags: {}
  };

  var T = EN, langWords = null;

  function pageLang() {
    try { return localStorage.getItem(LANG_KEY) || "en"; } catch (e) { return "en"; }
  }

  /* One shallow merge over the English table. The nested tables are merged a
     level deeper so a bundle that translates six group headings and no tag
     names still gets English for the rest. */
  function useWords(d) {
    if (!d) return;
    var out = {}, k;
    for (k in EN) if (EN.hasOwnProperty(k)) out[k] = EN[k];
    for (k in d) if (d.hasOwnProperty(k)) {
      if (d[k] && typeof d[k] === "object" && !(d[k] instanceof Array) && EN[k]) {
        var sub = {}, j;
        for (j in EN[k]) if (EN[k].hasOwnProperty(j)) sub[j] = EN[k][j];
        for (j in d[k]) if (d[k].hasOwnProperty(j) && d[k][j]) sub[j] = d[k][j];
        out[k] = sub;
      } else if (d[k] && (k !== "months" ||
                 (d[k] instanceof Array && d[k].length === 12))) out[k] = d[k];
    }
    T = out;
  }

  function loadWords() {
    if (langWords) return langWords;
    var lang = pageLang();
    if (lang === "en" || !window.fetch) return (langWords = Promise.resolve(EN));
    langWords = fetch("data/ui-i18n.v5." + lang + ".json")
      .then(function (r) {
        /* A path that does not exist answers 200 with the whole calendar. */
        if (!r.ok) return null;
        var ct = (r.headers.get("content-type") || "").toLowerCase();
        return ct.indexOf("json") < 0 ? null : r.json();
      })
      .then(function (d) { useWords(d); return T; })
      .catch(function () { return EN; });
    return langWords;
  }

  /* --------------------------------------------------------------- freshness */

  /* Every page carries the build it was published with; version.json carries
     the build now published, and is never cached. When they differ, the page
     in the browser is not the page on the site: fetch it again past the cache
     and show the reader the current one.

     Guarded so it can only ever run once per stale build per visit, and does
     nothing at all if anything is missing or unreachable - a page that fails
     this check should still work, it just will not correct itself. */
  function freshen() {
    var meta = document.querySelector('meta[name="plithos-build"]');
    var mine = meta && meta.getAttribute("content");
    if (!mine || !window.fetch) return;
    try { if (sessionStorage.getItem(BUILD_KEY) === mine) return; } catch (e) {}

    fetch(BUILD_URL, { cache: "no-store" }).then(function (r) {
      /* A path that does not exist returns the whole of index.html with a 200,
         so r.ok is not a sufficient guard. */
      var ct = (r.headers.get("content-type") || "").toLowerCase();
      if (!r.ok || ct.indexOf("json") < 0) return null;
      return r.json();
    }).then(function (v) {
      if (!v || !v.build || v.build === mine) return;
      try { sessionStorage.setItem(BUILD_KEY, mine); } catch (e) {}
      /* reload() alone would be served the same stale copy. Refetching the
         document past the cache first replaces that entry. */
      fetch(location.href, { cache: "reload" }).then(reload, reload);
    }, function () {});
  }

  function reload() { location.reload(); }

  /* ------------------------------------------------------------------ theme */

  function systemDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function storedTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }

  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    var b = document.getElementById("pl-theme");
    if (b) {
      b.textContent = t === "dark" ? T.themeLight : T.themeDark;
      b.setAttribute("aria-label", t === "dark" ? T.toLight : T.toDark);
    }
  }

  function initTheme() {
    applyTheme(storedTheme() || (systemDark() ? "dark" : "light"));
    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function () {
        if (!storedTheme()) applyTheme(mq.matches ? "dark" : "light");
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }

  function toggleTheme() {
    var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
    applyTheme(next);
  }

  /* ------------------------------------------------------------- search data */

  var DATA = null, loading = null;

  function loadIndex() {
    if (DATA) return Promise.resolve(DATA);
    if (loading) return loading;
    loading = fetch(INDEX_URL)
      .then(function (r) {
        /* Cloudflare Pages answers a missing path with HTTP 200 and the whole
           of index.html, so r.ok alone is not a safe test. */
        if (!r.ok) return null;
        var ct = (r.headers.get("content-type") || "").toLowerCase();
        if (ct.indexOf("json") < 0) return null;
        return r.json();
      })
      .then(function (d) {
        DATA = (d && d.e) ? d : { e: [], counts: {} };
        return DATA;
      })
      .catch(function () {
        DATA = { e: [], counts: {} };
        return DATA;
      });
    return loading;
  }

  /* ---------------------------------------------------------------- matching */

  function fold(s) {
    s = (s || "").toLowerCase();
    if (s.normalize) s = s.normalize("NFD").replace(/[̀-ͯ]/g, "");
    return s.replace(/[^a-z0-9Ͱ-῿　-퟿ ]+/g, " ").replace(/\s+/g, " ").trim();
  }

  function rank(n, q) {
    if (!n) return 0;
    if (n === q) return 100;
    if (n.indexOf(q) === 0) return 80;
    if (n.indexOf(" " + q) >= 0) return 60;
    if (n.indexOf(q) > 0) return 40;
    return 0;
  }

  function score(entry, q) {
    var s = rank(entry._f || (entry._f = fold(entry.n)), q);
    /* A translated tag is searchable under both names: the reader's word and
       the English one the shelf is built on. */
    if (entry.k === "t") {
      var tn = tagName(entry);
      if (tn !== entry.n) s = Math.max(s, rank(entry._t || (entry._t = fold(tn)), q));
    }
    if (s) return s;
    var m = entry._m || (entry._m = fold(entry.m));
    if (m.indexOf(q) >= 0) return 15;
    return 0;
  }

  /* Tags come first when they score as well as anything else: a reader who
     types a subject usually wants everything filed under it, not the one work
     whose title happens to carry the word. */
  var ORDER = ["t", "s", "w", "p", "b", "g"];

  /* What the site holds, read out before anything is typed. Kept in the order
     a reader would name them, which is not the order results group in. */
  var COUNT_ORDER = ["s", "w", "p", "b", "g", "t"];

  /* A tag is matched on its translated name as well as its English one, so
     the shelf can be reached in the reader's own language. */
  function tagName(e) {
    return (e.x && T.tags[e.x]) || e.n;
  }

  function displayName(e) {
    return e.k === "t" ? tagName(e) : e.n;
  }

  function displayMeta(e) {
    if (e.k !== "t") return e.m;
    var dim = String(e.x || "").split(":")[0];
    var n = e.c || 0;
    return (T.dims[dim] || dim) + " · " + n + " " + (n === 1 ? T.title : T.titles);
  }

  function search(q, limit) {
    var f = fold(q);
    if (f.length < 2) return [];
    var all = DATA ? DATA.e : [], out = [], i, sc;
    for (i = 0; i < all.length; i++) {
      sc = score(all[i], f);
      if (sc) out.push({ e: all[i], s: sc });
    }
    out.sort(function (a, b) {
      if (b.s !== a.s) return b.s - a.s;
      if ((b.e.g || 0) !== (a.e.g || 0)) return (b.e.g || 0) - (a.e.g || 0);
      return displayName(a.e).length - displayName(b.e).length;
    });
    out = out.slice(0, limit || 40);

    /* Bucket by kind so each heading appears exactly once, and order the
       buckets by their strongest hit. Sorting on score alone interleaved the
       kinds and produced repeated "Library"/"Saints" headings. */
    var buckets = {}, order = [];
    out.forEach(function (r) {
      if (!buckets[r.e.k]) { buckets[r.e.k] = []; order.push(r.e.k); }
      buckets[r.e.k].push(r);
    });
    order.sort(function (a, b) {
      var d = buckets[b][0].s - buckets[a][0].s;
      return d || (ORDER.indexOf(a) - ORDER.indexOf(b));
    });
    var flat = [];
    order.forEach(function (k) { flat = flat.concat(buckets[k]); });
    return flat;
  }

  /* ------------------------------------------------------------------- panel */

  var ov, input, results, hits = [], cursor = -1;

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function dayLabel(mmdd) {
    if (!mmdd) return "";
    var p = mmdd.split("-");
    var m = T.months[(+p[0]) - 1];
    return m ? m + " " + (+p[1]) : "";
  }

  function build() {
    ov = document.createElement("div");
    ov.className = "pl-ov";
    ov.id = "pl-ov";
    ov.hidden = true;
    ov.setAttribute("role", "dialog");
    ov.setAttribute("aria-modal", "true");
    ov.setAttribute("aria-label", T.searchAria);
    ov.innerHTML =
      '<div class="pl-panel">' +
        '<div class="pl-head">' +
          '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.5" y2="16.5"></line></svg>' +
          '<input id="pl-input" type="search" autocomplete="off" spellcheck="false" placeholder="' + esc(T.searchPlaceholder) + '">' +
          '<button class="pl-esc" type="button" id="pl-close">' + esc(T.esc) + '</button>' +
        '</div>' +
        '<div class="pl-results" id="pl-results" role="listbox"></div>' +
        '<div class="pl-foot"><span><b>&uarr;&darr;</b> ' + esc(T.hintMove) + '</span>' +
          '<span><b>&crarr;</b> ' + esc(T.hintOpen) + '</span>' +
          '<span><b>Esc</b> ' + esc(T.hintClose) + '</span></div>' +
      '</div>';
    document.body.appendChild(ov);
    input = ov.querySelector("#pl-input");
    results = ov.querySelector("#pl-results");

    ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
    ov.querySelector("#pl-close").addEventListener("click", close);
    input.addEventListener("input", render);
    input.addEventListener("keydown", onKey);
  }

  /* The bundle can arrive after the panel is built. Rebuilding it would drop
     what the reader has typed, so the words are replaced in place. */
  function relabel() {
    if (!ov) return;
    ov.setAttribute("aria-label", T.searchAria);
    input.setAttribute("placeholder", T.searchPlaceholder);
    ov.querySelector("#pl-close").textContent = T.esc;
    var f = ov.querySelectorAll(".pl-foot span"), w = [T.hintMove, T.hintOpen, T.hintClose], i;
    for (i = 0; i < f.length && i < 3; i++) {
      f[i].lastChild.nodeValue = " " + w[i];
    }
    if (!ov.hidden) render();
  }

  function render() {
    var q = input.value;
    hits = search(q, 40);
    cursor = hits.length ? 0 : -1;
    if (fold(q).length < 2) {
      var c = (DATA && DATA.counts) || {}, line = [];
      COUNT_ORDER.forEach(function (k) {
        if (c[k]) line.push(c[k] + " " + T.counts[k]);
      });
      results.innerHTML = '<div class="pl-empty">' + esc(line.join("  ·  ")) + '</div>';
      return;
    }
    if (!hits.length) {
      /* Nothing is named this. The words may still be in the books, and this
         is the moment the reader most needs to be told he can look there. */
      results.innerHTML = '<div class="pl-empty">' + esc(T.nothingFound) +
        ' &ldquo;' + esc(q) + '&rdquo;</div>' + insideTheBooks(q);
      wireBooks(q);
      return;
    }
    var html = "", lastK = null, i;
    for (i = 0; i < hits.length; i++) {
      var e = hits[i].e, meta = displayMeta(e);
      if (e.k !== lastK) {
        html += '<div class="pl-group">' + esc(T.groups[e.k] || "") + "</div>";
        lastK = e.k;
      }
      html += '<button class="pl-hit' + (i === cursor ? " on" : "") +
        (e.k === "t" ? " pl-tag" : "") + '" role="option" data-i="' + i + '">' +
        (e.g ? '<span class="pl-star" aria-hidden="true">✦</span>' : "") +
        '<span class="pl-name">' + esc(displayName(e)) + "</span>" +
        (meta ? '<span class="pl-meta">' + esc(meta) + "</span>" : "") +
        (e.d ? '<span class="pl-day">' + esc(dayLabel(e.d)) + "</span>" : "") +
        "</button>";
    }
    html += insideTheBooks(q);
    results.innerHTML = html;
    var btns = results.querySelectorAll(".pl-hit[data-i]");
    for (i = 0; i < btns.length; i++) {
      btns[i].addEventListener("click", function () { go(+this.getAttribute("data-i")); });
    }
    wireBooks(q);
  }

  /* ------------------------------------------------- inside the books

     The index this palette loads carries what things are called, not what
     they say: the words of the Fathers run to five megabytes and cannot
     travel to every page. So the Library lends its own full-text search to
     this box while the reader is on the Library, and from anywhere else the
     box offers to take him there with the question already asked.

     Either way there is one search on the site, and it reaches the words. */

  function booksApi() {
    return (window.PLITHOS_BOOKS && typeof window.PLITHOS_BOOKS.search === "function")
      ? window.PLITHOS_BOOKS : null;
  }

  var bookHits = [];

  function insideTheBooks(q) {
    bookHits = [];
    if (fold(q).length < 2) return "";
    var api = booksApi(), out = "";
    if (api) {
      try { bookHits = api.search(q) || []; } catch (e) { bookHits = []; }
    }
    out += '<div class="pl-group">' + esc(T.groups.x) + "</div>";
    bookHits.forEach(function (b, j) {
      out += '<button class="pl-hit" role="option" data-b="' + j + '">' +
        '<span class="pl-name">' + esc(b.name || "") + "</span>" +
        '<span class="pl-meta">' + esc([b.where, b.author].filter(Boolean).join(" · ")) + "</span>" +
        "</button>";
    });
    /* The way through to everything, not only the first few, and the only
       row there is when the Library is not the page we are standing on. */
    out += '<button class="pl-hit pl-more" role="option" data-all="1">' +
      '<span class="pl-name">' + esc(T.searchBooks) + "</span>" +
      '<span class="pl-meta">&ldquo;' + esc(q) + "&rdquo;</span></button>";
    return out;
  }

  function wireBooks(q) {
    var api = booksApi();
    var rows = results.querySelectorAll(".pl-hit[data-b]"), i;
    for (i = 0; i < rows.length; i++) {
      rows[i].addEventListener("click", function () {
        var b = bookHits[+this.getAttribute("data-b")];
        if (!b || !api) return;
        close();
        api.open(b.work, b.unit);
      });
    }
    var all = results.querySelector(".pl-hit[data-all]");
    if (all) all.addEventListener("click", function () {
      close();
      if (api && typeof api.showAll === "function") api.showAll(q);
      else window.location.href = "/library#find=" + encodeURIComponent(q);
    });
  }

  function move(delta) {
    if (!hits.length) return;
    cursor = (cursor + delta + hits.length) % hits.length;
    var btns = results.querySelectorAll(".pl-hit"), i;
    for (i = 0; i < btns.length; i++) {
      var on = +btns[i].getAttribute("data-i") === cursor;
      btns[i].classList.toggle("on", on);
      if (on && btns[i].scrollIntoView) btns[i].scrollIntoView({ block: "nearest" });
    }
  }

  function go(i) {
    var e = hits[i] && hits[i].e;
    if (!e) return;
    close();
    window.location.href = e.u;
  }

  function onKey(ev) {
    if (ev.key === "ArrowDown") { ev.preventDefault(); move(1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); move(-1); }
    else if (ev.key === "Enter") { ev.preventDefault(); go(cursor); }
    else if (ev.key === "Escape") { ev.preventDefault(); close(); }
  }

  function open() {
    loadWords();
    if (!ov) build();
    ov.hidden = false;
    input.value = "";
    results.innerHTML = "";
    loadIndex().then(function () { if (!ov.hidden) render(); });
    setTimeout(function () { input.focus(); }, 20);
  }

  function close() {
    if (ov) ov.hidden = true;
  }

  /* --------------------------------------------------------------- launchers */

  function typingInField(el) {
    if (!el) return false;
    var t = (el.tagName || "").toLowerCase();
    return t === "input" || t === "textarea" || t === "select" || el.isContentEditable;
  }

  function mountControls() {
    var slot = document.querySelector("[data-plithos-ui]");
    if (!slot) {
      slot = document.querySelector("header nav") || document.querySelector("nav");
      if (!slot) return;
    }
    var wrap = document.createElement("span");
    wrap.style.display = "inline-flex";
    wrap.style.alignItems = "center";
    wrap.style.gap = "8px";
    wrap.style.marginInlineStart = "8px";

    var isMac = /mac|iphone|ipad/i.test(navigator.platform || navigator.userAgent || "");
    var launch = document.createElement("button");
    launch.type = "button";
    launch.className = "pl-launch";
    launch.setAttribute("aria-label", T.searchAria);
    launch.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.5" y2="16.5"></line></svg>' +
      '<span class="pl-launch-word">' + esc(T.searchLabel) + '</span>' +
      '<kbd class="pl-launch-kbd">' + (isMac ? "⌘K" : "Ctrl K") + "</kbd>";
    launch.addEventListener("click", open);

    var theme = document.createElement("button");
    theme.type = "button";
    theme.className = "pl-theme";
    theme.id = "pl-theme";
    theme.addEventListener("click", toggleTheme);

    wrap.appendChild(launch);
    wrap.appendChild(theme);
    slot.appendChild(wrap);
    applyTheme(document.documentElement.getAttribute("data-theme") || "light");
  }

  /* The wordmark reads as a home link on every page but was only wired on the
     Library, where it went to the Library's own home rather than the site's.
     Make it a real link everywhere. On the calendar, which is already home,
     clear any deep link and go back to today instead of reloading 6.8 MB. */
  function mountHome() {
    var brand = document.querySelector(".brand");
    if (!brand || brand.closest("a")) return;
    var onIndex = /(^|\/)(index\.html)?$/.test(location.pathname);

    brand.setAttribute("role", "link");
    brand.setAttribute("tabindex", "0");
    brand.setAttribute("aria-label", T.home);
    brand.style.cursor = "pointer";

    var go = function () {
      if (onIndex) {
        if (location.hash) history.pushState(null, "", location.pathname + location.search);
        var t = document.getElementById("today");
        if (t) t.click();
        window.scrollTo(0, 0);
      } else {
        location.href = "index.html";
      }
    };
    brand.onclick = go;
    brand.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); go(); }
    });
  }

  /* ------------------------------------------------------- language pickers */

  /* A native <select> cannot contain an <svg>, which is why only the calendar
     showed flags - it uses a custom menu. This upgrades any plain language
     <select> into the same flag menu, keeping the original element in the DOM
     so the page's own change handler still fires. */
  var FLAGS = null;

  function flagMenu(sel) {
    var wrap = document.createElement("div");
    wrap.className = "pl-lang";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "pl-langbtn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    var menu = document.createElement("div");
    menu.className = "pl-langmenu";
    menu.setAttribute("role", "listbox");
    menu.hidden = true;

    function label(code) {
      var o = sel.querySelector('option[value="' + code + '"]');
      return o ? o.textContent : code;
    }
    function paint() {
      btn.innerHTML = (FLAGS[sel.value] || "") + "<span>" + label(sel.value) + "</span>" +
                      '<span class="pl-caret" aria-hidden="true">\u25be</span>';
      btn.setAttribute("aria-label", T.language + ": " + label(sel.value));
    }
    function close() { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); }

    Array.prototype.forEach.call(sel.options, function (o) {
      var it = document.createElement("button");
      it.type = "button";
      it.className = "pl-langopt";
      it.setAttribute("role", "option");
      it.innerHTML = (FLAGS[o.value] || "") + "<span>" + o.textContent + "</span>";
      it.addEventListener("click", function () {
        sel.value = o.value;
        sel.dispatchEvent(new Event("change", { bubbles: true }));
        paint(); close();
      });
      menu.appendChild(it);
    });

    btn.addEventListener("click", function () {
      var open = menu.hidden;
      menu.hidden = !open;
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
    sel.addEventListener("change", paint);

    paint();
    wrap.appendChild(btn);
    wrap.appendChild(menu);
    sel.parentNode.insertBefore(wrap, sel);
    sel.classList.add("pl-hidden-select");
    return wrap;
  }

  function mountLangPickers() {
    var sels = document.querySelectorAll("select#langpick, select[data-lang-select]");
    if (!sels.length) return;
    fetch("data/flags.v2.json")
      .then(function (r) {
        if (!r.ok) return null;
        var ct = (r.headers.get("content-type") || "").toLowerCase();
        if (ct.indexOf("json") < 0) return null;
        return r.json();
      })
      .then(function (d) {
        if (!d) return;              /* leave the plain select in place */
        FLAGS = d;
        Array.prototype.forEach.call(sels, flagMenu);
      })
      .catch(function () {});
  }

  /* Everything the shared chrome says, said again in the words now loaded. */
  function paintChrome() {
    applyTheme(document.documentElement.getAttribute("data-theme") || "light");
    var l = document.querySelector(".pl-launch");
    if (l) {
      l.setAttribute("aria-label", T.searchAria);
      var w = l.querySelector(".pl-launch-word");
      if (w) w.textContent = T.searchLabel;
    }
    var brand = document.querySelector(".brand[role=link]");
    if (brand) brand.setAttribute("aria-label", T.home);
    relabel();
  }

  /* A page announces that the reader has changed language; the chrome is not
     the page's to repaint, so it repaints itself. Without this the search
     button and the palette keep the language the page was opened in. */
  function onLangChange() {
    langWords = null;
    T = EN;
    loadWords().then(paintChrome);
  }

  function init() {
    /* The theme toggle and the search button are chrome the reader sees on
       every page, so the words are fetched at load rather than waiting for
       the palette to be opened. English pays nothing: it is already here. */
    loadWords().then(paintChrome);
    mountControls();
    mountHome();
    mountLangPickers();
    document.addEventListener("plithos:lang", onLangChange);
    document.addEventListener("keydown", function (ev) {
      var k = (ev.key || "").toLowerCase();
      if ((ev.metaKey || ev.ctrlKey) && k === "k") { ev.preventDefault(); open(); return; }
      if (k === "/" && !ev.metaKey && !ev.ctrlKey && !ev.altKey &&
          !typingInField(document.activeElement) && (!ov || ov.hidden)) {
        ev.preventDefault(); open();
      }
    });
  }

  initTheme();
  freshen();
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
