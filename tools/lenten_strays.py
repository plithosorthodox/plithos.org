#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lent, taken off 2024's dates and put back on the paschalion.

Eight movable Lenten commemorations were sitting in the FIXED synaxarion, on
the civil dates they happened to fall on in 2024 - Pascha that year was the
fifth of May. So every year since, on the seventh of April, the calendar has
announced the Third Sunday of Great Lent and the Veneration of the Cross, in
every jurisdiction and every language, whatever day of the week it was and
whether or not it was Lent at all. The real Sunday of the Veneration of the
Cross was being computed correctly all along, twenty-three days earlier.

Six of the eight are exact duplicates of days the paschalion already names,
and are simply removed:

  Beginning of Great Lent                        Clean Monday, -48
  1st Sunday: Sunday of Orthodoxy                -42
  2nd Sunday: St Gregory Palamas                 -35
  3rd Sunday: Veneration of the Cross            -28
  4th Sunday: St John Climacus                   -21
  5th Sunday: St Mary of Egypt                   -14

The other two the paschalion did not name, so removing them alone would have
lost them. They are moved to their offsets and given the readings both
Churches print:

  1st Saturday of Great Lent, the Miracle of the Boiled Wheat   -43
      Heb. 1:1-12 | Mark 2:23-3:5
      oca.org 2026-02-28, where St Theodore the Recruit's own pair
      (2 Tim. 2:1-10, John 15:17-16:2) is listed beside the day's.
  5th Saturday of Great Lent, of the Akathist to the Theotokos  -15
      Heb. 9:24-28 | Mark 8:27-31
      oca.org 2026-03-28 and days.pravoslavie.ru 2026-03-15 Julian, which
      lists the day's readings first and the Theotokos readings of the
      Akathist second (Евр. 320 зач. IX, 1-7 and Лк. 54 зач. X, 38-42).
      The Akathist is sung at Matins; the Liturgy keeps the Saturday's own.

Their English wording is kept exactly as it was, because both names are
already translated into the twenty-one languages and the translations are
keyed on the English.

    python3 tools/lenten_strays.py --check
    python3 tools/lenten_strays.py --write
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

STRAYS = [
    "Beginning of Great Lent",
    "1st Saturday of Great Lent: The Miracle of the Boiled Wheat",
    "1st Sunday of Great Lent: Sunday of Orthodoxy",
    "2nd Sunday of Great Lent: St Gregory Palamas",
    "3rd Sunday of Great Lent: Veneration of the Cross",
    "4th Sunday of Great Lent: St John Climacus (of the Ladder)",
    "5th Saturday of Great Lent: of the Akathist to the Theotokos",
    "5th Sunday of Great Lent: St Mary of Egypt",
]

MOVED = {
    "-43": ("1st Saturday of Great Lent: The Miracle of the Boiled Wheat",
            {"ep": "Heb. 1:1-12", "go": "Mark 2:23-3:5"}),
    "-15": ("5th Saturday of Great Lent: of the Akathist to the Theotokos",
            {"ep": "Heb. 9:24-28", "go": "Mark 8:27-31"}),
}


def entries(name):
    """Every form the synaxarion writes the object in.

    The Akathist Saturday carries g:1, being marked a great day, and a form
    that only matched the plain object left it behind while the other seven
    were removed."""
    q = json.dumps(name, ensure_ascii=False)
    return ["{n:%s,g:1}" % q, "{n:%s}" % q]


def entry(name):
    return entries(name)[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    i = src.index("const SYNAXARION")
    j = src.index("\nconst ", i + 10)
    syn = src[i:j]

    left = [n for n in STRAYS if any(e in syn for e in entries(n))]
    named = [k for k in MOVED if '"%s":"%s"' % (k, MOVED[k][0]) in src
             or "%s:%s" % (k, json.dumps(MOVED[k][0], ensure_ascii=False)) in src]

    if not a.write:
        print("Lenten days still pinned to 2024's dates: %d of %d"
              % (len(left), len(STRAYS)))
        for n in left:
            print("   " + n)
        print("the two Saturdays moved to the paschalion: %d of 2" % len(named))
        return 0 if (not left and len(named) == 2) else 1

    for n in STRAYS:
        for e in entries(n):
            if e not in syn:
                continue
            # Take the comma with it, whichever side it is on.
            for pat in (e + ",", "," + e, e):
                if pat in syn:
                    syn = syn.replace(pat, "", 1)
                    break
            break
    src = src[:i] + syn + src[j:]

    for off, (name, r) in MOVED.items():
        key = json.dumps(off)
        if key + ":" in src[src.index("const PASCHAL_NAMES"):
                            src.index("const PASCHAL_NAMES") + 4000]:
            continue
        for table, value in (("PASCHAL_NAMES", json.dumps(name, ensure_ascii=False)),
                             ("PASCHAL_READINGS",
                              json.dumps(r, ensure_ascii=False,
                                         separators=(",", ":")))):
            m = re.search(r"const %s\s*=\s*\{" % table, src)
            at = m.end()
            src = src[:at] + "%s:%s," % (key, value) + src[at:]

    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("Lent is off 2024's dates; the two Saturdays keep their names "
          "and gain their readings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
