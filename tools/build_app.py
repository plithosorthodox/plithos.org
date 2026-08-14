#!/usr/bin/env python3
"""
Assemble the whole site into the app, so it opens with no connection.

The site is a set of static files served from plithos.org. The app carries the
same files inside itself and serves them from its own local origin. Nothing is
fetched over the network while a reader uses it, and nothing can be: the app is
built without the permission that would allow it (tools/harden_manifest.py).
This script gathers the files the app is made of into app/www.

    python3 tools/build_app.py

What it does, and why each step is needed:

  1. The pages. The seven pages are copied with two changes. The Google Fonts
     request - the only thing on the whole site that reached a remote host - is
     removed and replaced with a link to the fonts kept beside the app. And the
     links between pages are rewritten from the site's clean paths (/saints) to
     the files those paths stand for (saints.html), because inside the app
     there is no server to perform that translation. Nothing else is touched;
     the text and data the pages carry are copied exactly.

  2. The shared script. It loses the check that asks the site whether a newer
     build has been published, since nothing inside a download can publish one.
     It gains a small helper that resolves any remaining clean path at the
     moment a link is followed - the links written into the pages are rewritten
     above, but some are built at runtime from the data files, and those can
     only be caught as they are used.

  3. The content. The prayers, the Fathers, the saints' lives, the Scriptures
     and the search index are copied in, but only the editions the pages
     actually ask for. On the site every file carries a version in its name so
     that a change reaches readers holding an old copy, and the superseded
     editions have to stay where they are. A download has no such history, so
     carrying them would add eighty megabytes to what a reader waits for and
     nothing would ever read them.

Everything here asserts what it expects to find, so a change in the site stops
the build rather than producing an app that is quietly missing something.

Run tools/vendor_fonts.py first if app/vendor/fonts is empty.
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WWW = ROOT / "app" / "www"
FONTS_SRC = ROOT / "app" / "vendor" / "fonts"

PAGES = ["index.html", "saints.html", "library.html", "prayers.html",
         "rule.html", "glossary.html", "contact.html"]

# The six pages reached by name, and the calendar, which is the site root.
ROUTES = "saints|library|prayers|rule|glossary|contact"

# The only remote load on the site: strip every Google Fonts link, then point
# the page at the copies kept with the app.
GOOGLE_FONTS = re.compile(r"<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*")
LOCAL_FONTS = '<link rel="stylesheet" href="assets/fonts/plithos-fonts.css">'
HEAD_OPEN = re.compile(r"(<head[^>]*>)", re.I)

# A page's public URL is its filename with the extension taken off. Inside the
# app the filename is all there is, so the path form is turned back into it.
LINK_ROUTE = re.compile(r'href="/(%s)((?:[#?][^"]*)?)"' % ROUTES)
LINK_ROOT = re.compile(r'href="/((?:[#?][^"]*)?)"')

# Anything under these prefixes is fetched at runtime; anything else that
# matches a versioned family name is an edition no longer asked for.
DATA_LITERAL = re.compile(r"(?:data|scripture)/[A-Za-z0-9._/-]*")

# Left in the shared script, to catch the links built at runtime from data.
LOCALIZER = r'''
  /* This copy runs inside the app, where each page is a file (saints.html),
     not the site's clean path (/saints). The pages' own links are rewritten
     when the app is assembled; these are the ones built while it runs, from
     the data files, which can only be caught as they are followed. */
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


def die(msg):
    raise SystemExit("build_app: " + msg)


def cut(s, start, end, what, leave=""):
    i = s.find(start)
    if i < 0:
        die("shared script shape changed: no %s" % what)
    j = s.find(end, i)
    if j < 0:
        die("shared script shape changed: %s does not end" % what)
    return s[:i] + leave + s[j:]


def asset_names():
    """The shared script and stylesheet the pages actually ask for, read from
    the pages rather than written here, since their names carry a version that
    changes whenever they do."""
    want = None
    for name in PAGES:
        s = (ROOT / name).read_text(encoding="utf-8")
        found = (sorted(set(re.findall(r"assets/plithos-ui\.v\d+\.js", s))),
                 sorted(set(re.findall(r"assets/plithos-ui\.v\d+\.css", s))))
        if len(found[0]) != 1 or len(found[1]) != 1:
            die("%s names %d scripts and %d stylesheets; expected one of each"
                % (name, len(found[0]), len(found[1])))
        if want is None:
            want = found
        elif found != want:
            die("%s asks for %s but the other pages ask for %s"
                % (name, found, want))
    js, css = want[0][0], want[1][0]
    for rel in (js, css):
        if not (ROOT / rel).exists():
            die("the pages ask for %s, which does not exist" % rel)
    return js, css


def build_shared_js(js_rel):
    js = (ROOT / js_rel).read_text(encoding="utf-8")

    marker = '"use strict";\n'
    if marker not in js:
        die("shared script shape changed: no strict marker")
    js = js.replace(marker, marker + LOCALIZER, 1)

    # The search result the reader chooses, and "search every word of the
    # Fathers" from a page that is not the Library: the two places the script
    # sends the reader somewhere itself.
    a = "window.location.href = e.u;"
    if a not in js:
        die("shared script shape changed: search-go line moved")
    js = js.replace(a, "window.location.href = toLocal(e.u);", 1)

    b = 'else window.location.href = "/library#find=" + encodeURIComponent(q);'
    if b not in js:
        die("shared script shape changed: inside-the-books line moved")
    js = js.replace(
        b,
        'else window.location.href = toLocal("/library") + "#find=" + encodeURIComponent(q);',
        1)

    # Nothing in a download can publish a newer build, so nothing in it needs
    # to ask. The check comes out, with the two names it read, the helper it
    # called, and the line of the header that announced it.
    js = cut(js,
             "  /* --------------------------------------------------------------- freshness */",
             "  /* ------------------------------------------------------------------ theme */",
             "freshness block")
    js = cut(js,
             " *   3. A check that the page in front of the reader is the page we publish.",
             " * ES5-flavoured to match the house style",
             "freshness header note",
             leave=" *\n")
    for dead in ('  var BUILD_URL = "/version.json";\n',
                 '  var BUILD_KEY = "plithos.freshened";\n',
                 '  freshen();\n'):
        if dead not in js:
            die("shared script shape changed: %r not found" % dead.strip())
        js = js.replace(dead, "", 1)
    for gone in ("freshen", "version.json", "BUILD_URL"):
        if gone in js:
            die("the freshness check is still referenced (%s) after removal" % gone)
    return js


def build_page(name):
    s = (ROOT / name).read_text(encoding="utf-8")
    if not GOOGLE_FONTS.search(s):
        print("  ! %s: no Google Fonts link found (already local?)" % name)
    s = GOOGLE_FONTS.sub("", s)
    if not HEAD_OPEN.search(s):
        die("%s: no <head> to place the fonts link" % name)
    s = HEAD_OPEN.sub(r"\1\n" + LOCAL_FONTS, s, count=1)

    s, n1 = LINK_ROUTE.subn(r'href="\1.html\2"', s)
    s, n2 = LINK_ROOT.subn(r'href="index.html\1"', s)
    return s, n1 + n2


def wanted_prefixes():
    """Every data path the pages and the shared script can ask for. Most are
    written with the language or the work spliced into the middle, so what is
    found is a prefix rather than a filename."""
    lits = set()
    for name in PAGES:
        lits |= set(DATA_LITERAL.findall((ROOT / name).read_text(encoding="utf-8")))
    js_rel, _ = asset_names()
    lits |= set(DATA_LITERAL.findall((ROOT / js_rel).read_text(encoding="utf-8")))
    lits = {x for x in lits if len(x) > 5}
    if not lits:
        die("no data paths found in the pages - the shape has changed")
    return sorted(lits)


def copy_content(prefixes):
    kept = dropped = 0
    kept_b = dropped_b = 0
    for d in ("data", "scripture"):
        for base, _dirs, files in os.walk(ROOT / d):
            for f in files:
                src = Path(base) / f
                rel = src.relative_to(ROOT).as_posix()
                size = src.stat().st_size
                if not any(rel.startswith(p) for p in prefixes):
                    dropped += 1
                    dropped_b += size
                    continue
                dst = WWW / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                kept += 1
                kept_b += size
    print("content: %d files kept (%.0f MB); %d superseded editions left behind (%.0f MB)"
          % (kept, kept_b / 1e6, dropped, dropped_b / 1e6))


def check_output():
    """Two things that would break the app quietly rather than loudly."""
    # Android's asset packager silently drops names that begin with a dot or an
    # underscore. A data file lost that way is a feature that simply does
    # nothing, with no error anywhere to say so.
    hostile = []
    for base, dirs, files in os.walk(WWW):
        for n in list(dirs) + files:
            if n.startswith(".") or n.startswith("_"):
                hostile.append(str(Path(base).relative_to(WWW) / n))
    if hostile:
        die("these names are dropped by the Android packager: %s" % hostile[:10])

    # Anything the pages would load from another host. A <link> is only a load
    # for certain relations; canonical, alternate and the rest are metadata a
    # reader's browser never fetches, and the pages are full of them.
    loads = re.compile(
        r'<(?:script|img|iframe|source|video|audio|embed|object)\b[^>]*'
        r'(?:src|srcset|data)="(?:https?:)?//[^"]+', re.I)
    link_tag = re.compile(r"<link\b[^>]*>", re.I)
    fetching_rel = re.compile(
        r'rel="\s*(?:stylesheet|preload|modulepreload|prefetch|dns-prefetch|'
        r'preconnect|icon|shortcut icon|apple-touch-icon|manifest)\s*"', re.I)
    remote_href = re.compile(r'href="(?:https?:)?//', re.I)
    css_remote = re.compile(r"url\(\s*[\"']?(?:https?:)?//", re.I)
    other = re.compile(r"\bnew WebSocket\b|\bEventSource\b|sendBeacon|importScripts|"
                       r"serviceWorker\s*\.\s*register")
    bad = []
    for p in sorted(WWW.glob("*.html")) + sorted((WWW / "assets").glob("*.js")) \
            + sorted((WWW / "assets").glob("*.css")):
        s = p.read_text(encoding="utf-8", errors="replace")
        for rx, what in ((loads, "remote subresource"), (css_remote, "remote css url"),
                         (other, "network primitive")):
            for m in rx.findall(s):
                bad.append("%s: %s %s" % (p.name, what, str(m)[:90]))
        for tag in link_tag.findall(s):
            if fetching_rel.search(tag) and remote_href.search(tag):
                bad.append("%s: remote link %s" % (p.name, tag[:90]))
    if bad:
        die("the assembled app would reach the network:\n  " + "\n  ".join(bad[:10]))
    print("checked: no remote subresources, no names the packager would drop")


def main():
    if not FONTS_SRC.exists() or not any(FONTS_SRC.glob("*.woff2")):
        die("app/vendor/fonts is empty - run tools/vendor_fonts.py first")

    js_rel, css_rel = asset_names()
    prefixes = wanted_prefixes()

    if WWW.exists():
        shutil.rmtree(WWW)
    (WWW / "assets" / "fonts").mkdir(parents=True)

    links = 0
    for name in PAGES:
        text, n = build_page(name)
        (WWW / name).write_text(text, encoding="utf-8")
        links += n
    print("pages: %d copied, fonts made local, %d links pointed at their files"
          % (len(PAGES), links))

    (WWW / "assets" / Path(js_rel).name).write_text(
        build_shared_js(js_rel), encoding="utf-8")
    shutil.copy2(ROOT / css_rel, WWW / "assets" / Path(css_rel).name)
    for f in FONTS_SRC.iterdir():
        shutil.copy2(f, WWW / "assets" / "fonts" / f.name)
    print("assets: %s (localized, freshness check removed), %s, %d font files"
          % (Path(js_rel).name, Path(css_rel).name,
             sum(1 for _ in (WWW / "assets" / "fonts").iterdir())))

    copy_content(prefixes)
    check_output()

    total = sum(f.stat().st_size for f in WWW.rglob("*") if f.is_file())
    count = sum(1 for f in WWW.rglob("*") if f.is_file())
    print("app/www assembled: %d files, %.0f MB" % (count, total / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
