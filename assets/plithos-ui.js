/* Plithos shared UI.
 *
 * Two things every page gets, without touching that page's own code:
 *
 *   1. A command palette on Ctrl/Cmd-K (or "/") that searches the whole site
 *      at once - saints, prayers, library works, scripture books. Each page
 *      holds only its own dataset inline and cannot see the others', so the
 *      palette fetches data/search-index.v1.json, built by
 *      tools/build_search_index.py. It is fetched once, on first open, so it
 *      costs nothing on pages nobody searches from.
 *
 *   2. A dark theme toggle. The pages all declare the same custom properties,
 *      so assets/plithos-ui.css re-themes them by overriding those tokens.
 *
 * ES5-flavoured to match the house style in the app pages. No dependencies.
 */
(function () {
  "use strict";

  var INDEX_URL = "data/search-index.v1.json";
  var THEME_KEY = "plithos.theme";

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
      b.textContent = t === "dark" ? "Light theme" : "Dark theme";
      b.setAttribute("aria-label", t === "dark" ? "Switch to light theme" : "Switch to dark theme");
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

  function score(entry, q) {
    var n = entry._f || (entry._f = fold(entry.n));
    if (n === q) return 100;
    if (n.indexOf(q) === 0) return 80;
    var wordStart = n.indexOf(" " + q);
    if (wordStart >= 0) return 60;
    if (n.indexOf(q) > 0) return 40;
    var m = entry._m || (entry._m = fold(entry.m));
    if (m.indexOf(q) >= 0) return 15;
    return 0;
  }

  var ORDER = ["s", "w", "p", "b"];
  var LABEL = { s: "Saints", w: "Library", p: "Prayers", b: "Scripture" };

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
      return a.e.n.length - b.e.n.length;
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

  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function dayLabel(mmdd) {
    if (!mmdd) return "";
    var p = mmdd.split("-");
    var m = MON[(+p[0]) - 1];
    return m ? m + " " + (+p[1]) : "";
  }

  function build() {
    ov = document.createElement("div");
    ov.className = "pl-ov";
    ov.id = "pl-ov";
    ov.hidden = true;
    ov.setAttribute("role", "dialog");
    ov.setAttribute("aria-modal", "true");
    ov.setAttribute("aria-label", "Search everything");
    ov.innerHTML =
      '<div class="pl-panel">' +
        '<div class="pl-head">' +
          '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.5" y2="16.5"></line></svg>' +
          '<input id="pl-input" type="search" autocomplete="off" spellcheck="false" placeholder="Search saints, prayers, the Fathers, scripture">' +
          '<button class="pl-esc" type="button" id="pl-close">Esc</button>' +
        '</div>' +
        '<div class="pl-results" id="pl-results" role="listbox"></div>' +
        '<div class="pl-foot"><span><b>&uarr;&darr;</b> move</span><span><b>&crarr;</b> open</span><span><b>Esc</b> close</span></div>' +
      '</div>';
    document.body.appendChild(ov);
    input = ov.querySelector("#pl-input");
    results = ov.querySelector("#pl-results");

    ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
    ov.querySelector("#pl-close").addEventListener("click", close);
    input.addEventListener("input", render);
    input.addEventListener("keydown", onKey);
  }

  function render() {
    var q = input.value;
    hits = search(q, 40);
    cursor = hits.length ? 0 : -1;
    if (fold(q).length < 2) {
      var c = (DATA && DATA.counts) || {};
      results.innerHTML = '<div class="pl-empty">' +
        esc([
          c.s ? c.s + " saints" : "",
          c.w ? c.w + " works" : "",
          c.p ? c.p + " prayers" : "",
          c.b ? c.b + " books of scripture" : ""
        ].filter(Boolean).join("  ·  ")) + '</div>';
      return;
    }
    if (!hits.length) {
      results.innerHTML = '<div class="pl-empty">Nothing found for &ldquo;' + esc(q) + '&rdquo;</div>';
      return;
    }
    var html = "", lastK = null, i;
    for (i = 0; i < hits.length; i++) {
      var e = hits[i].e;
      if (e.k !== lastK) {
        html += '<div class="pl-group">' + esc(LABEL[e.k] || "") + "</div>";
        lastK = e.k;
      }
      html += '<button class="pl-hit' + (i === cursor ? " on" : "") + '" role="option" data-i="' + i + '">' +
        (e.g ? '<span class="pl-star" aria-hidden="true">✦</span>' : "") +
        '<span class="pl-name">' + esc(e.n) + "</span>" +
        (e.m ? '<span class="pl-meta">' + esc(e.m) + "</span>" : "") +
        (e.d ? '<span class="pl-day">' + esc(dayLabel(e.d)) + "</span>" : "") +
        "</button>";
    }
    results.innerHTML = html;
    var btns = results.querySelectorAll(".pl-hit");
    for (i = 0; i < btns.length; i++) {
      btns[i].addEventListener("click", function () { go(+this.getAttribute("data-i")); });
    }
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
    launch.setAttribute("aria-label", "Search everything");
    launch.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="20" y1="20" x2="16.5" y2="16.5"></line></svg>' +
      '<span>Search</span><kbd class="pl-launch-kbd">' + (isMac ? "⌘K" : "Ctrl K") + "</kbd>";
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
    brand.setAttribute("aria-label", "Plithos home");
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

  function init() {
    mountControls();
    mountHome();
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
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
