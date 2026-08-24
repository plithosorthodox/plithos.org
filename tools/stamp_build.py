#!/usr/bin/env python3
"""
Stamp every page with the build it is published as, and write version.json.

A browser can keep a page long after that page has been replaced, and the
reader has no way to tell: the site looks live, but a section that has since
moved simply does nothing when tapped. The shared UI layer compares the stamp
in the page against version.json, which is never cached, and refetches the
page when they differ.

Run this before publishing whenever a page has changed:

    python3 tools/stamp_build.py

The stamp is today's date with a letter, so several publications in one day
are distinct. Pass one explicitly to set it by hand:

    python3 tools/stamp_build.py 2026-08-03c
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "saints.html", "library.html",
         "prayers.html", "rule.html", "glossary.html", "contact.html"]
VERSION = ROOT / "version.json"

TAG = re.compile(r'<meta name="plithos-build" content="[^"]*">')
ANCHOR = '<meta charset="utf-8">'


def next_build():
    today = datetime.date.today().isoformat()
    current = ""
    if VERSION.exists():
        try:
            current = json.loads(VERSION.read_text(encoding="utf-8")).get("build", "")
        except ValueError:
            current = ""
    if not current.startswith(today):
        return today + "a"
    suffix = current[len(today):] or "a"
    return today + _next_suffix(suffix)


def _next_suffix(s):
    """a, b, ... z, aa, ab, ... zz, aaa - and never past z into punctuation.

    Twenty-six publications in a day was not foreseen. It happened on 24
    August and the twenty-seventh stamp was `2026-08-24{`, which is chr(ord
    ('z')+1) and is not a letter. Nothing broke - the stamp is only ever
    compared for equality - but it would have gone on into `|`, `}` and out
    the other side of ASCII."""
    if not s:
        return "a"
    if not s.isalpha() or not s.islower():
        # a suffix that is not letters can only be the `{` this used to
        # produce, which means the single letters are already spent
        return "aa"
    out = list(s)
    i = len(out) - 1
    while i >= 0:
        if out[i] != "z":
            out[i] = chr(ord(out[i]) + 1)
            return "".join(out)
        out[i] = "a"
        i -= 1
    return "a" + "".join(out)


def main():
    build = sys.argv[1] if len(sys.argv) > 1 else next_build()
    if build.startswith("-"):
        sys.exit("stamp_build.py takes a build stamp, not an option: %r.\n"
                 "Run it with no argument for today's stamp, or pass one like 2026-08-03c."
                 % build)
    tag = '<meta name="plithos-build" content="%s">' % build

    for name in PAGES:
        path = ROOT / name
        s = path.read_text(encoding="utf-8")
        if TAG.search(s):
            s = TAG.sub(tag, s, count=1)
        elif ANCHOR in s:
            s = s.replace(ANCHOR, ANCHOR + tag, 1)
        else:
            print("ERROR: %s has no <meta charset> to stamp beside" % name)
            return 1
        path.write_text(s, encoding="utf-8")
        print("  %-22s %s" % (name, build))

    VERSION.write_text(json.dumps({"build": build}) + "\n", encoding="utf-8")
    print("wrote version.json  %s" % build)
    return 0


if __name__ == "__main__":
    sys.exit(main())
