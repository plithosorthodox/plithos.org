#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The readings for Pascha, and for the days the table had no room for.

PASCHAL_READINGS was reached only through PASCHAL_NAMES: the calendar asked
for a name first and took the readings that came with it. The four great
movable feasts are named in TWELVE_MOVABLE instead, so the branch was never
taken for them and the table was never asked. The result was that Pascha,
Palm Sunday, the Ascension and Pentecost - the four days a reader is most
likely to look up, and Pascha above all - showed the feast and no readings at
all, in every jurisdiction and every language. A hundred and sixty-two of the
three hundred and forty-five blank Sunday panels were these three Sundays.

Sourced, not remembered. Each pair was read off a published calendar and,
where the two usages could differ, off one from each side:

  Pascha            Acts 1:1-8 | John 1:1-17
                    oca.org/readings/daily/2026/04/12 and
                    days.pravoslavie.ru/Days/20260330.html - identical
  Palm Sunday       Phil. 4:4-9 | John 12:1-18
  Ascension         Acts 1:1-12 | Luke 24:36-53
  Pentecost         Acts 2:1-11 | John 7:37-52, 8:12
                    oca.org/readings/daily/2026/{04/05,05/21,05/31}

The Presanctified Liturgy of Great Monday, Tuesday and Wednesday has a Gospel
and no Epistle, and that is how they are entered:

  Great and Holy Monday     Matt. 21:18-43
  Great and Holy Tuesday    Matt. 24:36-26:2
  Great and Holy Wednesday  Matt. 26:6-16

TWO DAYS ARE LEFT BLANK ON PURPOSE, and their blankness is the right answer
rather than a gap. Clean Monday has no Liturgy: its readings are the Old
Testament at the Sixth Hour and at Vespers, and there is no Epistle and no
Gospel to give. Great and Holy Friday has no Liturgy either; the Epistle and
Gospel a reader would find belong to the Royal Hours and to Vespers, and
printing one pair as the day's would say a Liturgy is served when none is.

    python3 tools/paschal_readings.py --check
    python3 tools/paschal_readings.py --write
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

ADD = {
    "-7": {"ep": "Phil. 4:4-9", "go": "John 12:1-18"},
    "0":  {"ep": "Acts 1:1-8", "go": "John 1:1-17"},
    "39": {"ep": "Acts 1:1-12", "go": "Luke 24:36-53"},
    "49": {"ep": "Acts 2:1-11", "go": "John 7:37-52, 8:12"},
    "-6": {"ep": "", "go": "Matt. 21:18-43"},
    "-5": {"ep": "", "go": "Matt. 24:36-26:2"},
    "-4": {"ep": "", "go": "Matt. 26:6-16"},
}

# The calendar asked PASCHAL_NAMES first and only then the readings. It now
# asks the readings whatever names the day, so a feast named in
# TWELVE_MOVABLE keeps its name and gains its readings.
OLD_BRANCH = ("if(PASCHAL_NAMES[key]){dayName=tn(PASCHAL_NAMES[key]);"
              "dayReading=PASCHAL_READINGS[key]||null;}")
NEW_BRANCH = ("if(PASCHAL_READINGS[key])dayReading=PASCHAL_READINGS[key];"
              "if(PASCHAL_NAMES[key]){dayName=tn(PASCHAL_NAMES[key]);}")


# Bare keys are JavaScript and not JSON; the table also spans several lines,
# so its end is found by matching braces rather than by looking for a newline.
BARE_KEY = re.compile(r'([{,])\s*(-?[A-Za-z0-9_]+)\s*:')
TRAILING = re.compile(r",(\s*[}\]])")


def fix(chunk):
    """Bare keys to JSON keys, and no trailing comma. Never inside a string."""
    return TRAILING.sub(r"\1", BARE_KEY.sub(r'\1"\2":', chunk))


def span(src, at):
    depth = 0
    for k in range(at, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return k + 1
    return None


def table(src):
    m = re.search(r"const PASCHAL_READINGS\s*=\s*", src)
    if not m:
        return None, None, None
    end = span(src, m.end())
    if end is None:
        return None, None, None
    raw = src[m.end():end]
    # Bare keys are made into JSON keys only OUTSIDE string literals.
    # "John 7:37-52, 8:12" carries a comma and then a colon, and a regex that
    # does not know it is inside a string reads that as a key and quietly
    # writes "8":12 into the middle of a scripture reference.
    parts, buf, i, n = [], [], 0, len(raw)
    while i < n:
        if raw[i] == '"':
            parts.append(fix("".join(buf)))
            buf = []
            j = i + 1
            while j < n and raw[j] != '"':
                j += 2 if raw[j] == "\\" else 1
            parts.append(raw[i:j + 1])
            i = j + 1
        else:
            buf.append(raw[i])
            i += 1
    parts.append(fix("".join(buf)))
    return json.loads("".join(parts)), m.end(), end


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    cur, i, j = table(src)
    if cur is None:
        print("PASCHAL_READINGS is not where it was")
        return 1

    missing = [k for k in ADD if k not in cur]
    branch_ok = NEW_BRANCH in src
    if not a.write:
        print("%d of %d readings written; the calendar %s the table for a day "
              "TWELVE_MOVABLE names"
              % (len(ADD) - len(missing), len(ADD),
                 "asks" if branch_ok else "does NOT ask"))
        if missing:
            print("  still missing: " + " ".join(sorted(missing, key=int)))
        return 0 if (not missing and branch_ok) else 1

    cur.update({k: v for k, v in ADD.items() if k not in cur})
    ordered = {k: cur[k] for k in sorted(cur, key=int)}
    src = (src[:i] + json.dumps(ordered, ensure_ascii=False,
                                separators=(",", ":")) + src[j:])
    if OLD_BRANCH in src:
        src = src.replace(OLD_BRANCH, NEW_BRANCH, 1)
    elif NEW_BRANCH not in src:
        print("the branch that reads PASCHAL_READINGS is not where it was")
        return 1
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("%d days now carry their readings; the calendar asks the table "
          "whatever names the day" % len(ADD))
    return 0


if __name__ == "__main__":
    sys.exit(main())
