#!/usr/bin/env python3
"""
Assemble the whole site into the app, so it opens with no connection.

The site is a set of static files served from plithos.org. The app carries the
same files inside itself and serves them from its own local origin, so nothing
is fetched over the network while a reader uses it. This script gathers those
files into app/www, which the Android build then packages.

    python3 tools/build_app.py

What it does, and why each step is needed:

  1. The pages. The seven pages are copied with one change to each head: the
     Google Fonts request - the only thing on the whole site that reaches a
     remote host - is removed and replaced with a link to the fonts kept in
     app/vendor/fonts by tools/vendor_fonts.py. Nothing else in a page is
     touched; the data they carry inline is copied byte for byte.

  2. The links. On the site a page is reached at a clean path (/saints); in
     the app it is a file (saints.html). The shared script is given a small
     helper that turns the site's own path form back into the file beside it,
     both when a link is followed and when the search sends the reader across
     pages. The pages themselves are not rewritten - the helper does it at the
     moment of navigation - so their inline text stays exactly as published.

  3. The content. data/ and scripture/ - the prayers, the Fathers, the
     saints' lives, the Scriptures, the search index - are copied whole, since
     the pages load them on demand and in the app that demand must be met from
     inside.

Run tools/vendor_fonts.py first if app/vendor/fonts is empty.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WWW = ROOT / "app" / "www"
FONTS_SRC = ROOT / "app" / "vendor" / "fonts"

PAGES = ["index.html", "saints.html", "library.html", "prayers.html",
         "rule.html", "glossary.html", "contact.html"]

# The only remote load on the site: strip every Google Fonts link, then point
# the page at the copies kept with the app.
GOOGLE_FONTS = re.compile(r"<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*")
LOCAL_FONTS = '<link rel="stylesheet" href="assets/fonts/plithos-fonts.css">'
HEAD_OPEN = re.compile(r"(<head[^>]*>)", re.I)

# Turn the site's clean paths back into the files that sit beside index.html,
# at the moment a link is followed or the search jumps across pages. Added to
# the shared script rather than to any page, so the pages stay as published.
LOCALIZER = r'''
  /* This copy runs inside the app, where each page is a file (saints.html),
     not the site's clean path (/saints). Any link written in the site's path
     form is turned back into the file beside it - when a link is clicked, and
     when the search sends the reader to another page. */
  function toLocal(u) {
    if (typeof u !== "string" || !u) return u;
    if (u.charAt(0) !== "/" || u.charAt(1) === "/") return u;
    if (u === "/") return "index.html";
    if (u.charAt(1) === "#" || u.charAt(1) === "?") return "index.html" + u.slice(1);
    var m = u.match(/^\/(saints|library|prayers|rule|glossary|contact)(?=$|[#?\/])([\s\S]*)$/);
    return m ? m[1] + ".html" + m[2] : u;
  }
  document.addEventListener("click", function (ev) {
    if (ev.defaultPrevented || ev.button) return;
    var a = ev.target && ev.target.closest ? ev.target.closest("a[href]") : null;
    if (!a) return;
    var raw = a.getAttribute("href"), loc = toLocal(raw);
    if (loc !== raw) a.setAttribute("href", loc);
  }, true);
'''


def build_shared_js():
    """The shared script, with the localizer added and its two cross-page
    navigations routed through it."""
    js = (ROOT / "assets" / "plithos-ui.v9.js").read_text(encoding="utf-8")

    marker = '"use strict";\n'
    if marker not in js:
        raise SystemExit("shared script shape changed: no strict marker")
    js = js.replace(marker, marker + LOCALIZER, 1)

    # The search result the reader chooses.
    a = "window.location.href = e.u;"
    if a not in js:
        raise SystemExit("shared script shape changed: search-go line moved")
    js = js.replace(a, "window.location.href = toLocal(e.u);", 1)

    # "Search every word of the Fathers" from a page that is not the Library.
    b = 'else window.location.href = "/library#find=" + encodeURIComponent(q);'
    if b not in js:
        raise SystemExit("shared script shape changed: inside-the-books line moved")
    js = js.replace(
        b, 'else window.location.href = toLocal("/library") + "#find=" + encodeURIComponent(q);', 1)
    return js


def build_page(name):
    s = (ROOT / name).read_text(encoding="utf-8")
    if not GOOGLE_FONTS.search(s):
        print("  ! %s: no Google Fonts link found (already local?)" % name)
    s = GOOGLE_FONTS.sub("", s)
    if HEAD_OPEN.search(s):
        s = HEAD_OPEN.sub(r"\1\n" + LOCAL_FONTS, s, count=1)
    else:
        raise SystemExit("%s: no <head> to place the fonts link" % name)
    return s


def main():
    if not FONTS_SRC.exists() or not any(FONTS_SRC.glob("*.woff2")):
        raise SystemExit("app/vendor/fonts is empty - run tools/vendor_fonts.py first")

    if WWW.exists():
        shutil.rmtree(WWW)
    (WWW / "assets" / "fonts").mkdir(parents=True)

    for name in PAGES:
        (WWW / name).write_text(build_page(name), encoding="utf-8")
    print("pages: %d copied, fonts made local" % len(PAGES))

    (WWW / "assets" / "plithos-ui.v9.js").write_text(build_shared_js(), encoding="utf-8")
    shutil.copy2(ROOT / "assets" / "plithos-ui.v5.css", WWW / "assets" / "plithos-ui.v5.css")
    for f in FONTS_SRC.iterdir():
        shutil.copy2(f, WWW / "assets" / "fonts" / f.name)
    print("assets: shared script (localized), stylesheet, %d font files"
          % sum(1 for _ in (WWW / "assets" / "fonts").iterdir()))

    for d in ("data", "scripture"):
        shutil.copytree(ROOT / d, WWW / d)
        n = sum(1 for _ in (WWW / d).rglob("*") if _.is_file())
        print("%s: %d files" % (d, n))

    shutil.copy2(ROOT / "version.json", WWW / "version.json")

    total = sum(f.stat().st_size for f in WWW.rglob("*") if f.is_file())
    print("app/www assembled: %.0f MB" % (total / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
