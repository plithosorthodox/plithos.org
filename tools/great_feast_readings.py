#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The nine great feasts of the fixed calendar, with their own readings.

They had none. The Nativity of Christ and the Theophany printed the ordinary
day's Epistle and no Gospel at all; the Dormition and the Elevation printed
the ordinary day's pair entire, under the feast's name - so a reader who
opened the Dormition was given Matthew 19:3-12, on marriage and divorce,
where the Church reads Luke 10:38-42 and 11:27-28.

The four movable ones - Palm Sunday, Pascha, the Ascension and Pentecost -
were given theirs in an earlier pass and are in PASCHAL_READINGS.

Read off oca.org, which lists the feast's own pair last after the vespers
prophecies, the matins Gospel and the ordinary day's reading. Two were
cross-checked against days.pravoslavie.ru, on the other side of the calendar,
and agree exactly: the Nativity gives Гал. 209 зач. IV, 4-7 and Мф. 3 зач.
II, 1-12, and the Dormition Лк. 54 зач. X, 38-42; XI, 27-28. These are texts
the whole Church holds in common; nothing here differs between the usages.

    python3 tools/great_feast_readings.py --check
    python3 tools/great_feast_readings.py --write
"""
import argparse
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

# Keyed by the menaion date, which is how the calendar files a fixed feast.
READINGS = {
    "9-8":   {"ep": "Phil. 2:5-11",           "go": "Luke 10:38-42; 11:27-28"},
    "9-14":  {"ep": "1 Cor. 1:18-24",
              "go": "John 19:6-11, 13-20, 25-28, 30-35"},
    "11-21": {"ep": "Heb. 9:1-7",             "go": "Luke 10:38-42; 11:27-28"},
    "12-25": {"ep": "Gal. 4:4-7",             "go": "Matt. 2:1-12"},
    "1-6":   {"ep": "Titus 2:11-14; 3:4-7",   "go": "Matt. 3:13-17"},
    "2-2":   {"ep": "Heb. 7:7-17",            "go": "Luke 2:22-40"},
    "3-25":  {"ep": "Heb. 2:11-18",           "go": "Luke 1:24-38"},
    "8-6":   {"ep": "2 Pet. 1:10-19",         "go": "Matt. 17:1-9"},
    "8-15":  {"ep": "Phil. 2:5-11",           "go": "Luke 10:38-42; 11:27-28"},
}

TABLE = "const GREAT_READINGS=%s;" % json.dumps(
    READINGS, ensure_ascii=False, separators=(",", ":"))
ANCHOR = "const LUKE_TAIL=["

# A great feast is kept on its own day whatever else the day carries, so the
# override goes after the ordinary reckoning rather than inside it.
OLD = ("if(dayReading===null && d.getDay()>=1 && d.getDay()<=5 "
       "&& off>=-53 && off<=-1) dayReading={aliturgical:true};")
NEW = ("for(const f of TWELVE_FIXED){const c=fixedCivil(f.mo,f.da,y,mode);"
       "if(c.getMonth()===d.getMonth()&&c.getDate()===d.getDate()){"
       "const gr=GREAT_READINGS[f.mo+\"-\"+f.da];if(gr)dayReading=gr;break;}}"
       + OLD)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    have_table = "const GREAT_READINGS=" in src
    have_hook = "GREAT_READINGS[f.mo" in src
    if not a.write:
        print("the great feasts' readings: table %s, applied %s"
              % ("written" if have_table else "MISSING",
                 "yes" if have_hook else "NO"))
        return 0 if (have_table and have_hook) else 1

    if not have_table:
        i = src.index(ANCHOR)
        src = src[:i] + TABLE + "\n" + src[i:]
    if not have_hook:
        if OLD not in src:
            print("the aliturgical fallback is not where it was")
            return 1
        src = src.replace(OLD, NEW, 1)
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("%d great feasts now carry their own readings" % len(READINGS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
