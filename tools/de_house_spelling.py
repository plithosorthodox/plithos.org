#!/usr/bin/env python3
"""
Bring the German on the calendar to the house spelling.

The German was written before the register for the language was settled, and
it carries two things the house rules do not allow: the sharp s, and the long
dash. The site writes ss everywhere, because the pages are read in
Switzerland as well as in Germany and Austria and Grossmaertyrer is correct
in all three; and it writes hyphens rather than dashes in every language.
See docs/GERMAN.md.

German is the only language on the site that uses the sharp s at all, so it
can be found without knowing which table a string belongs to. The dash is
not: it is corrected only inside a German value, because the same character
stands in English copy elsewhere in the page and that is a separate matter.

library.html is deliberately left alone. Its German is the Divine Liturgy,
which is reproduced as its translator set it and is not the site's to
respell.

    python3 tools/de_house_spelling.py --check
    python3 tools/de_house_spelling.py --write
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The site's own German. The Liturgy in library.html is not on this list.
PAGES = ("index.html", "contact.html")

# One commemoration's German name, as the tables write it.
DE = re.compile(r'(?<=[{,])de:"((?:[^"\\]|\\.)*)"')

DASHES = (("—", "-"), ("–", "-"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    total = 0
    for name in PAGES:
        page = ROOT / name
        src = page.read_text(encoding="utf-8")
        was = src

        sharp = src.count("ß")
        src = src.replace("ß", "ss")

        dashed = []

        def one(m):
            v = m.group(1)
            for bad, good in DASHES:
                v = v.replace(bad, good)
            if v != m.group(1):
                dashed.append((m.group(1), v))
            return 'de:"%s"' % v

        src = DE.sub(one, src)

        print("%-14s %3d sharp s, %d long dash" % (name, sharp, len(dashed)))
        for a, b in dashed:
            print("               %s\n               %s" % (a, b))

        total += sharp + len(dashed)
        if args.write and src != was:
            page.write_text(src, encoding="utf-8")
            print("               written")

    print("\n%d corrections in all" % total)
    if not args.write and not args.check:
        print("nothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
