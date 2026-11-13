/* Keep the language a reader chose in the address as well as in the browser.
 *
 * Cloudflare serves each translated page at /<language>/<page>, while English
 * keeps the bare page address. The page controls already repaint in place and
 * store the choice; this small companion makes that state shareable and makes
 * navigation keep the same language.
 */
(function () {
  "use strict";

  var LANGS = {el:1,ru:1,ro:1,uk:1,de:1,es:1,ar:1,fr:1,pt:1,it:1,sr:1,
    ka:1,zh:1,ja:1,ko:1,sw:1,hy:1,arc:1,hi:1,bn:1,ur:1,bg:1};
  var PAGES = {calendar:"",saints:"saints",churches:"churches",
    library:"library",prayers:"prayers",rule:"rule",glossary:"glossary",
    contact:"contact"};

  function chosen() {
    var lang = "en";
    try { lang = localStorage.getItem("plithos.lang") || "en"; } catch (e) {}
    return LANGS[lang] ? lang : "en";
  }

  function currentPage() {
    var bits = location.pathname.split("/").filter(function (x) { return x; });
    if (bits.length && LANGS[bits[0]]) bits.shift();
    var page = bits.length ? bits[bits.length - 1] : "";
    page = page.replace(/\.html$/, "");
    return page === "index" ? "" : page;
  }

  function pathFor(lang, page) {
    return "/" + (lang === "en" ? "" : lang + "/") + page;
  }

  function keepLanguageInNav(lang) {
    var links = document.querySelectorAll(".topnav [data-nav]");
    var i, page;
    for (i = 0; i < links.length; i++) {
      page = PAGES[links[i].getAttribute("data-nav")];
      if (typeof page === "string") links[i].setAttribute("href", pathFor(lang, page));
    }
  }

  function identifyAddress(lang) {
    var page = currentPage();
    var known = page === "";
    var key;
    for (key in PAGES) if (PAGES[key] === page) known = true;
    if (!known) return;

    var path = pathFor(lang, page);
    if (location.pathname !== path) {
      history.replaceState(history.state, "", path + location.search + location.hash);
    }
    var here = "https://plithos.org" + path;
    var canonical = document.querySelector('link[rel="canonical"]');
    var og = document.querySelector('meta[property="og:url"]');
    if (canonical) canonical.setAttribute("href", here);
    if (og) og.setAttribute("content", here);
    keepLanguageInNav(lang);
  }

  function changed(e) {
    var lang = e && e.detail;
    identifyAddress(LANGS[lang] ? lang : chosen());
  }

  function init() {
    keepLanguageInNav(chosen());
    document.addEventListener("plithos:lang", changed);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
