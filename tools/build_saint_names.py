#!/usr/bin/env python3
"""
Publish the saints' names in every language, for the pages that lack them.

The calendar has carried translated names for a long time: one thousand five
hundred and twenty-eight commemorations in twenty-one languages, assembled in
index.html. The Saints index never got them. It has no language control at
all, so a reader who has set the site to Greek or Russian meets the calendar
in his own tongue, opens the Saints page, and finds fifteen hundred names in
English - names that were already sitting translated one page away.

This lifts that table out of index.html and writes it one file to a language,
so the Saints page can fetch the one language its reader has chosen instead
of a megabyte and a half of all of them. Where the calendar does not yet carry
a language's rendering, tools/saint_names/<lang>.py may fill that missing slot
for the Saints page. A supplement cannot add a commemoration or replace a
calendar name.

    python3 tools/build_saint_names.py --check
    python3 tools/build_saint_names.py --write
"""
import argparse
import importlib
import json
import pkgutil
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
OUT = ROOT / "data"
SUPPLEMENT_DIR = Path(__file__).resolve().parent / "saint_names"

# The inner objects use bare two- and three-letter language keys, which is
# JavaScript and not JSON.
BARE_KEY = re.compile(r'([{,])\s*([A-Za-z]{2,3})\s*:')


# A comma before the closing brace is legal JavaScript and not legal JSON.
TRAILING = re.compile(r",(\s*[}\]])")


def jsobj(src):
    return json.loads(TRAILING.sub(r"\1", BARE_KEY.sub(r'\1"\2":', src)))


def balanced(src, start):
    """The object literal beginning at start, to its matching brace.

    Counted rather than matched by pattern, and blind to braces inside
    strings, because a saint's name may contain anything at all.
    """
    depth, i, instr, esc = 0, start, False, False
    while i < len(src):
        c = src[i]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[start:i + 1], i + 1
        i += 1
    raise SystemExit("an object literal never closed")


def names():
    src = PAGE.read_text(encoding="utf-8")
    i = src.index("const NAMES_I18N=")
    blob, pos = balanced(src, src.index("{", i))
    table = jsobj(blob)
    # Everything after the literal is added a name at a time.
    for m in re.finditer(r'NAMES_I18N\[("(?:[^"\\]|\\.)*")\]\s*=\s*', src[pos:]):
        key = json.loads(m.group(1))
        obj, _ = balanced(src, pos + m.end())
        table[key] = jsobj(obj)
    return table


def add_supplements(table):
    """Add names translated for the Saints page but absent from the calendar.

    The calendar remains the authority wherever it already has a name. A
    supplement may fill a missing language value, but may neither introduce a
    commemoration nor replace a calendar rendering.
    """
    if not SUPPLEMENT_DIR.exists():
        return table
    sys.path.insert(0, str(SUPPLEMENT_DIR.parent))
    for found in pkgutil.iter_modules([str(SUPPLEMENT_DIR)]):
        lang = found.name
        mod = importlib.import_module("saint_names." + lang)
        text = getattr(mod, "TEXT", {})
        extra = [k for k in text if k not in table]
        overlap = [k for k in text if k in table and table[k].get(lang)]
        empty = [k for k, v in text.items()
                 if not isinstance(v, str) or not v.strip()]
        if extra or overlap or empty:
            raise SystemExit(
                "%s saint-name supplement has %d extra, %d overlapping, "
                "and %d empty value(s)" %
                (lang, len(extra), len(overlap), len(empty)))
        for key, value in text.items():
            table[key][lang] = value
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    table = add_supplements(names())
    langs = sorted({l for v in table.values() for l in v})
    print("%d commemorations, %d languages" % (len(table), len(langs)))

    per = {}
    for l in langs:
        per[l] = {k: v[l] for k, v in table.items() if v.get(l)}
    short = [l for l in langs if len(per[l]) < len(table)]
    for l in langs:
        n = len(per[l])
        print("   %-4s %5d names%s" % (l, n, "" if n == len(table)
                                       else "   (%d missing)" % (len(table) - n)))
    if short:
        print("\n%d language(s) do not name every commemoration; the English "
              "stands where a name is missing." % len(short))

    if args.write:
        for l in langs:
            p = OUT / ("saint-names.v1.%s.json" % l)
            p.write_text(json.dumps(per[l], ensure_ascii=False,
                                    separators=(",", ":")), encoding="utf-8")
        total = sum((OUT / ("saint-names.v1.%s.json" % l)).stat().st_size
                    for l in langs)
        print("\nwrote %d files, %s KB in all"
              % (len(langs), format(total // 1024, ",")))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
