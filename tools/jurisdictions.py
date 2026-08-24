#!/usr/bin/env python3
"""What each Church keeps, and what she does not.

    python3 tools/jurisdictions.py --check
    python3 tools/jurisdictions.py --write

The calendar here is one calendar. Its base is the synaxarion of the Orthodox
Church in America, and choosing a jurisdiction changes four things: whether
the reckoning is old or new, whether the rite is Western, the name and cross
shown at the head of the month, and a short list of that Church's own
commemorations which are ADDED to the base.

Nothing is ever taken away, and that is the defect. A Greek reader is shown
St Herman of Alaska, St Peter the Aleut and St Alexis Toth - North American
commemorations his Church does not keep - and an Antiochian reader is not
shown St Raphael of Brooklyn at all, because he is nowhere on the site. Ten
jurisdictions share one calendar and twenty-nine local entries between them.

This adds the missing half: OMIT_FIXED, so a jurisdiction can decline a
commemoration that is not hers. The lists themselves are a matter of record -
each Church publishes her own calendar - and are filled from those calendars
with the source named, never from inference. An omission asserted without a
source would tell a reader his Church does not keep a feast that she does,
which is worse than the fault it fixes.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"

# jurisdiction -> [{"name": <substring of the base entry>, "src": <where this
# is read from>}]. A base commemoration whose name contains the string is not
# shown for that jurisdiction.
#
# EMPTY ON PURPOSE. The capability lands first and the lists are filled from
# each Church's published calendar, one jurisdiction at a time, with the
# source recorded beside every line. See docs/JURISDICTIONS.md.
OMIT_FIXED = {}


def literal(src, name):
    m = re.search(r"const %s\s*=" % name, src)
    if not m:
        raise ValueError(name)
    eq = src.index("=", m.start())
    j = src.index("\n", m.start())
    return m.start(), j, json.loads(src[eq + 1:j].rstrip().rstrip(";"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    src = io.open(PAGE, encoding="utf-8").read()

    i, j, local = literal(src, "LOCAL_FIXED")
    print("local commemorations, by jurisdiction:")
    for k in sorted(local):
        print("   %-12s %d" % (k, len(local[k])))
    print("   %-12s %d" % ("total", sum(len(v) for v in local.values())))

    have = "const OMIT_FIXED=" in src
    print("\nOMIT_FIXED present: %s" % ("yes" if have else "no"))
    for k in sorted(OMIT_FIXED):
        print("   %-12s declines %d" % (k, len(OMIT_FIXED[k])))
    if not OMIT_FIXED:
        print("   nothing declined yet; the lists are filled from each")
        print("   Church's own calendar, with the source named")

    if not a.write:
        return 0
    if have:
        i2, j2, _ = literal(src, "OMIT_FIXED")
        line = ("const OMIT_FIXED=" +
                json.dumps(OMIT_FIXED, ensure_ascii=False,
                           separators=(",", ":")) + ";")
        src = src[:i2] + line + src[j2:]
    else:
        line = ("\nconst OMIT_FIXED=" +
                json.dumps(OMIT_FIXED, ensure_ascii=False,
                           separators=(",", ":")) + ";")
        src = src[:i] + line.lstrip("\n") + "\n" + src[i:]
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("\nwrote index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
