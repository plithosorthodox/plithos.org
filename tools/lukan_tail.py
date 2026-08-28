#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Sundays of Luke that fall between the tenth and the Forefathers.

LUKE_SUN carries ten pericopes and the calendar counts them forward from the
Sunday after the Elevation. In most years there are one or two Sundays left
over before the Sunday of the Holy Forefathers, and for those the calendar
printed no Gospel at all: 81 of the 183 blank Sunday panels.

Counting further forward was tried once and abandoned, because it produced
Luke 14:16-24 twice within eight days and Luke 17:12-19 twice in three years
of six. That was not a mistake in the arithmetic. The Forefathers Sunday
itself takes Luke 14:16-24, so the ordinary Sundays before it do not continue
the count forward - they are reckoned BACKWARD FROM THE FOREFATHERS, and the
pericope the forward count wanted is the one the feast has already taken.

Read off the calendars the Churches publish, on both sides of the divide,
rather than derived:

  the Sunday before the Forefathers        Luke 17:12-19
    oca.org 2025-12-07, 2026-12-06, 2027-12-05, 2028-12-10, 2029-12-09
    days.pravoslavie.ru 2025-12-08 Julian - Лк., 85 зач., XVII, 12-19

  two Sundays before the Forefathers       Luke 18:18-27
    oca.org 2024-12-01, 2028-12-03, 2029-12-02
    days.pravoslavie.ru 2025-12-01 Julian - Лк., 91 зач., XVIII, 18-27

Both Churches give the same pericope for the same position, which is what the
rest of this calendar already says: the Epistle and the Gospel course are
shared, and the two usages part company only because the Elevation and the
Nativity fall on different civil days for them. There are never more than two
such Sundays; nine years of each usage were walked to check that.

The Epistle is not touched. It indexes on weeks after Pentecost and does not
move with the jump.

    python3 tools/lukan_tail.py --check
    python3 tools/lukan_tail.py --write
"""
import argparse
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

TABLE = ('const LUKE_BEFORE_FF=["Luke 17:12-19","Luke 18:18-27"];')
ANCHOR = 'const LUKE_SUN=['

OLD = "if(L>=1&&L<=LUKE_SUN.length)return {ep,go:LUKE_SUN[L-1]};"
NEW = ("if(L>=1&&L<=LUKE_SUN.length)return {ep,go:LUKE_SUN[L-1]};"
       "const back=Math.round((ff-d)/(7*DAY));"
       "if(back>=1&&back<=LUKE_BEFORE_FF.length)"
       "return {ep,go:LUKE_BEFORE_FF[back-1]};")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    have_table = TABLE in src
    have_branch = NEW in src
    if not a.write:
        print("the Sundays before the Forefathers: table %s, branch %s"
              % ("written" if have_table else "MISSING",
                 "written" if have_branch else "MISSING"))
        return 0 if (have_table and have_branch) else 1

    if not have_table:
        i = src.index(ANCHOR)
        src = src[:i] + TABLE + "\n" + src[i:]
    if not have_branch:
        if OLD not in src:
            print("the forward Lukan count is not where it was")
            return 1
        src = src.replace(OLD, NEW, 1)
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("the one or two Sundays before the Forefathers now carry a Gospel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
