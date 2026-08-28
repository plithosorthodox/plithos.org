#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The end of the Lukan course: December, January, and the otstupka.

LUKE_SUN carries ten pericopes counted forward from the Sunday after the
Elevation. Everything after the tenth was blank: 183 of the 2,817 Sunday
panels over six years and nine Churches printed no Gospel at all.

Counting further forward was tried once and abandoned, because it produced
Luke 14:16-24 twice within eight days. That was not an arithmetic mistake:
the Sunday of the Holy Forefathers takes Luke 14:16-24 itself, and the
Sundays around it are not a plain continuation.

WHAT THE PUBLISHED CALENDARS ACTUALLY DO, read off oca.org and
days.pravoslavie.ru for thirty-five Sundays across nine years and both
usages, and reproduced here rather than derived:

  LUKE_TAIL = the course past the tenth, minus the one the feast takes:
      Luke 17:12-19, Luke 18:18-27, Luke 18:35-43

  DECEMBER. The one or two ordinary Sundays before the Forefathers take the
  pool from its start, counting BACKWARD from the feast: the Sunday nearest
  the Forefathers gets Luke 17:12-19, the one before it Luke 18:18-27.

  JANUARY. Between the Sunday after the Theophany and the Sunday of
  Zacchaeus the course finishes, but it is filled from the END of the pool,
  so that Luke 18:35-43 is always the last Lukan Sunday of the year. Where
  there is only room for one, Luke 18:18-27 is simply not read that year -
  which is what the OCA prints for 18 January 2026, and is the observation
  that broke two simpler models before this one.

  THE OTSTUPKA. Whatever January Sundays remain take the Matthean Sundays
  the Lukan jump skipped in the autumn, in order, ending on the Sunday
  before Zacchaeus: the tail of MATT_GO. Five such Sundays occur in 2024 and
  the OCA reads Matthew 22, 22, 25 and 15 across four of them.

  The Epistle is not touched. It indexes on weeks after Pentecost and does
  not move with the jump.

Both usages give the same pericope in the same position; they part company
only because the Elevation and the Nativity fall on different civil days for
them. All thirty-five published readings agree with the site.

This tool now only reports whether the page still carries that reckoning;
the reckoning itself lives in index.html and is copied into the engine by
tools/build_calendar_engine.py.

    python3 tools/lukan_tail.py --check
"""
import argparse
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

WANT = [
    ('const LUKE_TAIL=["Luke 17:12-19","Luke 18:18-27","Luke 18:35-43"];',
     "the pool of Lukan Sundays past the tenth"),
    ("if(back>=1&&back<=2)return {ep,go:LUKE_TAIL[back-1]};",
     "December, counting back from the Forefathers"),
    ("const luk=Math.min(gap,LUKE_TAIL.length-dec);",
     "January, filled from the end of the pool"),
    ("const M=gap-luk, m=j-luk;",
     "the otstupka, taking the tail of the Matthean course"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.parse_args()
    src = io.open(PAGE, encoding="utf-8").read()
    missing = [why for frag, why in WANT if frag not in src]
    for frag, why in WANT:
        print("  %-5s %s" % ("ok" if frag in src else "GONE", why))
    if missing:
        print("\nthe end of the Lukan course is no longer reckoned in index.html")
        return 1
    print("\nthe end of the Lukan course is reckoned as the calendars print it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
