#!/usr/bin/env python3
"""
Bring the three reading faces into the app so it needs no connection to wear
them. The pages ask Google for Fraunces, Spectral and IBM Plex Mono; here
those requests are answered once and kept, so the installed app carries the
fonts it displays rather than reaching out for them each time it opens.

This is a one-time gathering, run by hand where a connection exists. Its
output lives in app/vendor/fonts and is committed; the app build only copies
it. Re-run it if the pages ever ask for different weights.

    python3 tools/vendor_fonts.py

It reads the exact css2 requests out of the pages, fetches each stylesheet as
a current browser would (so the modern woff2 files come back), downloads every
font file the stylesheets name, and writes a single plithos-fonts.css whose
src rules point at the local copies.
"""
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "saints.html", "library.html", "prayers.html",
         "rule.html", "glossary.html", "contact.html"]
OUT = ROOT / "app" / "vendor" / "fonts"

# A current Chrome, so css2 serves woff2 rather than older formats.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

FACE = re.compile(r"@font-face\s*{[^}]*}", re.S)
SRC = re.compile(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)")
FAMILY = re.compile(r"font-family:\s*'([^']+)'")


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def css2_urls():
    seen, urls = set(), []
    pat = re.compile(r"https://fonts\.googleapis\.com/css2\?[^\"']+")
    for name in PAGES:
        for u in pat.findall((ROOT / name).read_text(encoding="utf-8")):
            if u not in seen:
                seen.add(u)
                urls.append(u)
    return urls


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    urls = css2_urls()
    if not urls:
        print("no css2 requests found in the pages")
        return 1
    print("%d stylesheet request(s) to vendor" % len(urls))

    faces, files, seen_face = [], {}, set()
    for u in urls:
        css = fetch(u)
        for block in FACE.findall(css):
            m = SRC.search(block)
            if not m:
                continue
            font_url = m.group(1)
            fam = FAMILY.search(block)
            fname = files.get(font_url)
            if not fname:
                h = hashlib.sha1(font_url.encode()).hexdigest()[:10]
                fname = "%s-%s.woff2" % (slug(fam.group(1)) if fam else "font", h)
                (OUT / fname).write_bytes(fetch(font_url, binary=True))
                files[font_url] = fname
                print("  %-34s %s" % (fname, font_url.split("/")[-1][:40]))
            local = block.replace(font_url, fname)
            key = re.sub(r"\s+", " ", local).strip()
            if key not in seen_face:
                seen_face.add(key)
                faces.append(local.strip())

    header = ("/* The reading faces, kept with the app so it wears them "
              "offline.\n   Gathered by tools/vendor_fonts.py from the same "
              "css2 requests the\n   pages make. Fraunces, Spectral and IBM "
              "Plex Mono, SIL Open Font License. */\n")
    (OUT / "plithos-fonts.css").write_text(
        header + "\n".join(faces) + "\n", encoding="utf-8")
    print("wrote %d font files and %d @font-face rules to %s"
          % (len(files), len(faces), OUT.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
