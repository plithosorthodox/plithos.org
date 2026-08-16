/* A page in one language, at a URL of its own.
 *
 * The site offers twenty-two languages and, until now, one address for each
 * page. A reader chose his language in the page and the choice was kept in his
 * browser, which serves him well and serves a search engine not at all: an
 * engine records one version of one address, so twenty-one of the twenty-two
 * were never written down anywhere they could be found. Searching for the
 * calendar in Greek did not lead here, and no amount of describing the page in
 * English was going to change that.
 *
 * So each language is given its own path - /el/rule beside /rule - and this
 * answers it. Nothing is copied: the same file is served, with four things
 * changed in passing.
 *
 *   the lang attribute, so the document says what it is
 *   the canonical, pointing at this address rather than the English one
 *   a link to every other language, and to the English as the one they
 *     all fall back to, so the twenty-two are known to belong together
 *   one line that sets the language before the page reads it
 *
 * That last line is why no page had to be altered. Every page already asks the
 * browser what language the reader chose; this simply answers before the
 * question is put.
 *
 * The English keeps its bare path. It is the address the site has always had,
 * it is the one already written down elsewhere, and moving it would cost the
 * only pages that are indexed today.
 */

export const LANGS = ["el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt",
  "it", "sr", "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur"];

/* Right to left, so the document can say so before any stylesheet loads. */
const RTL = { ar: 1, ur: 1, arc: 1 };

/* The seven pages, by the path the site gives them. */
const PAGES = {
  "": "index.html",
  "saints": "saints.html",
  "library": "library.html",
  "prayers": "prayers.html",
  "rule": "rule.html",
  "glossary": "glossary.html",
  "contact": "contact.html",
};

const SITE = "https://plithos.org";

function alternates(slug) {
  const tail = slug ? "/" + slug : "/";
  let out = '<link rel="alternate" hreflang="en" href="' + SITE + tail + '">';
  for (const l of LANGS) {
    out += '<link rel="alternate" hreflang="' + l + '" href="' +
      SITE + "/" + l + (slug ? "/" + slug : "") + '">';
  }
  /* The address to offer a reader whose language we do not keep. */
  out += '<link rel="alternate" hreflang="x-default" href="' + SITE + tail + '">';
  return out;
}

export async function serve(context, lang) {
  const { request, env } = context;
  const url = new URL(request.url);

  /* /el, /el/, /el/rule - anything else under the prefix is not a page. */
  const parts = url.pathname.split("/").filter(Boolean);
  const slug = parts.length > 1 ? parts.slice(1).join("/") : "";
  const file = Object.prototype.hasOwnProperty.call(PAGES, slug)
    ? PAGES[slug] : null;
  if (file === null) {
    return new Response(null, {
      status: 301,
      headers: { Location: SITE + "/" + (slug || "") },
    });
  }

  const asset = await env.ASSETS.fetch(new URL("/" + file, url.origin));
  if (!asset.ok) return asset;

  const here = SITE + "/" + lang + (slug ? "/" + slug : "");
  const preset = '<script>try{localStorage.setItem("plithos.lang",' +
    JSON.stringify(lang) + ');}catch(e){}</script>';

  const out = new HTMLRewriter()
    .on("html", {
      element(el) {
        el.setAttribute("lang", lang);
        if (RTL[lang]) el.setAttribute("dir", "rtl");
      },
    })
    .on('link[rel="canonical"]', {
      element(el) { el.setAttribute("href", here); },
    })
    .on("head", {
      /* The language is set before the page's own scripts run, and the
         alternates sit with the rest of the head. */
      element(el) { el.prepend(preset + alternates(slug), { html: true }); },
    })
    .transform(asset);

  const headers = new Headers(out.headers);
  headers.set("content-type", "text/html; charset=utf-8");
  headers.set("cache-control", "public, max-age=0, must-revalidate");
  return new Response(out.body, { status: 200, headers });
}
