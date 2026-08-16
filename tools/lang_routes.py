#!/usr/bin/env python3
"""
One address per language, and the links that tie them together.

The site is written in twenty-two languages and had one address for each page.
A reader chose his language and his browser remembered it; a search engine
records one version of one address, so twenty-one languages were written down
nowhere they could be found.

Each language now answers at a path of its own - /el/rule beside /rule - which
functions/<lang>/ serves by handing back the same file with its language set.
This writes those handlers, the alternates that must sit on the English pages,
and the sitemap that offers all of it.

    python3 tools/lang_routes.py --check
    python3 tools/lang_routes.py --write

Three things have to agree or a search engine ignores the lot:

  every language page names every other, and names the English
  every English page names every language, which is the return link Google
    requires and the half most often left out
  the sitemap lists all of them

The English keeps its bare path. It is the address the site has always had and
the only one indexed today, and moving it would cost what is already there.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FUNCS = ROOT / "functions"
SITE = "https://plithos.org"

LANGS = ["el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it", "sr",
         "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur"]

NAMES = {"el": "Greek", "ru": "Russian", "ro": "Romanian", "uk": "Ukrainian",
         "de": "German", "es": "Spanish", "ar": "Arabic", "fr": "French",
         "pt": "Portuguese", "it": "Italian", "sr": "Serbian",
         "ka": "Georgian", "zh": "Chinese", "ja": "Japanese", "ko": "Korean",
         "sw": "Swahili", "hy": "Armenian", "arc": "Syriac", "hi": "Hindi",
         "bn": "Bengali", "ur": "Urdu"}

# slug -> (file, changefreq, priority)
PAGES = [("", "index.html", "daily", "1.0"),
         ("saints", "saints.html", "weekly", "0.9"),
         ("library", "library.html", "weekly", "0.9"),
         ("prayers", "prayers.html", "weekly", "0.8"),
         ("rule", "rule.html", "weekly", "0.8"),
         ("glossary", "glossary.html", "monthly", "0.7"),
         ("contact", "contact.html", "monthly", "0.5")]

HANDLER = '''/* %s. See ../_lang.js - every language answers the same way. */
import { serve } from "../_lang.js";

export const onRequest = (context) => serve(context, "%s");
'''

MARK = "<!-- the same page in the other languages -->"


def alternates(slug):
    tail = "/" + slug if slug else "/"
    out = [MARK,
           '<link rel="alternate" hreflang="en" href="%s%s">' % (SITE, tail)]
    for l in LANGS:
        out.append('<link rel="alternate" hreflang="%s" href="%s/%s%s">'
                   % (l, SITE, l, ("/" + slug) if slug else ""))
    out.append('<link rel="alternate" hreflang="x-default" href="%s%s">'
               % (SITE, tail))
    return "".join(out)


def sitemap(lastmod):
    rows = []
    for slug, _f, freq, pri in PAGES:
        rows.append((SITE + "/" + slug, freq, pri))
    for l in LANGS:
        for slug, _f, freq, pri in PAGES:
            loc = SITE + "/" + l + (("/" + slug) if slug else "")
            # A language page is never more important than the page itself.
            rows.append((loc, freq, "%.1f" % max(0.3, float(pri) - 0.2)))
    body = "".join(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n"
        "  </url>\n" % (loc, lastmod, freq, pri) for loc, freq, pri in rows)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + "</urlset>\n"), len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    notes = []

    # 1. a handler for each language
    made = 0
    for l in LANGS:
        p = FUNCS / l / "[[path]].js"
        want = HANDLER % (NAMES[l], l)
        if not p.exists() or p.read_text(encoding="utf-8") != want:
            made += 1
            if a.write:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(want, encoding="utf-8")
    notes.append("%d handler(s) %s" % (made, "written" if a.write else "to write"))

    # 2. the return links on the English pages
    touched = 0
    for slug, f, _freq, _pri in PAGES:
        page = ROOT / f
        s = page.read_text(encoding="utf-8")
        block = alternates(slug)
        if MARK in s:
            new = re.sub(re.escape(MARK) + r'(?:<link rel="alternate"[^>]*>)*',
                         block, s, count=1)
        else:
            m = re.search(r'<link rel="canonical" href="[^"]*">', s)
            if not m:
                raise SystemExit("%s has no canonical to sit beside" % f)
            new = s[:m.end()] + block + s[m.end():]
        if new != s:
            touched += 1
            if a.write:
                page.write_text(new, encoding="utf-8")
    notes.append("%d English page(s) %s"
                 % (touched, "given alternates" if a.write else "to touch"))

    # 3. the sitemap
    old = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    m = re.search(r"<lastmod>([\d-]+)</lastmod>", old)
    xml, n = sitemap(m.group(1) if m else "2026-08-16")
    if a.write:
        (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    notes.append("sitemap offers %d addresses" % n)

    for x in notes:
        print("  " + x)
    print("written" if a.write else "(--check: nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
