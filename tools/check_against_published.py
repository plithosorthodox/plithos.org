#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What this calendar prints, against what the Churches publish.

The site's readings were once reported as unverified for want of a rule.
There is no need of a rule: the Churches publish their calendars, and this
compares ours against theirs, day by day.

    oca.org/readings/daily/YYYY/MM/DD       a new-calendar Church
    days.pravoslavie.ru/Days/YYYYMMDD.html  an old-calendar Church, and the
                                            URL takes the JULIAN date

The test is deliberately one-sided and says so. A published page lists
several pairs - the vespers prophecies, the matins Gospel, the saint's own
readings and the day's - and which is which cannot be told from the order:
the great feasts put the festal pair last and the Lenten Saturdays put it
first. So this does not try to pick the right one. It asks only whether the
Gospel THIS SITE prints appears anywhere among the readings that Church
publishes for that day. A hit is agreement. A miss is a definite error and
is printed in full for a person to look at.

    python3 tools/check_against_published.py --year 2027
    python3 tools/check_against_published.py --year 2027 --sundays-only
"""
import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0 Safari/537.36")

# The Gospel books, as each side names them.
EN = r"(?:Matthew|Mark|Luke|John)"
RU = r"(?:Мф|Мк|Лк|Ин)"
RU2EN = {"Мф": "Matt.", "Мк": "Mark", "Лк": "Luke", "Ин": "John"}
ROMAN = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,
         "X":10,"XI":11,"XII":12,"XIII":13,"XIV":14,"XV":15,"XVI":16,
         "XVII":17,"XVIII":18,"XIX":19,"XX":20,"XXI":21,"XXII":22,
         "XXIII":23,"XXIV":24,"XXV":25,"XXVI":26,"XXVII":27,"XXVIII":28}


def fetch(url):
    out = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "40", url],
                         capture_output=True).stdout.decode("utf-8", "replace")
    t = re.sub(r"<script.*?</script>", "", out, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def oca_gospels(iso):
    y, m, d = iso.split("-")
    t = fetch("https://www.oca.org/readings/daily/%s/%s/%s" % (y, m, d))
    return set(re.findall(EN + r"\s+\d+:\d+", t))


def prav_gospels(iso):
    """The Moscow page gives chapter in Roman numerals: Лк., 30 зач., VII, 11-16."""
    t = fetch("https://days.pravoslavie.ru/Days/%s.html" % iso.replace("-", ""))
    out = set()
    for m in re.finditer(RU + r"\.?,?\s*(?:\d+\s*зач\.?,?\s*)?([IVXL]+),?\s*(\d+)", t):
        book = RU2EN[m.group(0).split(".")[0].split(",")[0].strip()]
        ch = ROMAN.get(m.group(1))
        if ch:
            out.add("%s %d:%s" % (book, ch, m.group(2)))
    return out


def norm(ref):
    """Down to book, chapter and first verse, which is what both sides agree on."""
    m = re.match(r"([1-3]?\s?[A-Za-z.]+)\s+(\d+):(\d+)", (ref or "").strip())
    if not m:
        return None
    book = m.group(1).rstrip(".").strip()
    book = {"Matt": "Matthew", "Mk": "Mark", "Jn": "John"}.get(book, book)
    return "%s %s:%s" % (book, m.group(2), m.group(3))


def ours(iso, juris):
    js = ("""
import fs from 'fs';
import { calendar } from '%s/assets/plithos-calendar.v2.js';
const T=JSON.parse(fs.readFileSync('%s/data/calendar-tables.v2.json','utf8'));
const o=calendar(T,null,'en')('%s',{juris:'%s',lang:'en'});
console.log(JSON.stringify({g:(o.readings||{}).gospel||null,n:o.day_name||o.headline}));
""" % (ROOT, ROOT, iso, juris))
    p = os.path.join(ROOT, ".probe.mjs")
    open(p, "w").write(js)
    try:
        out = subprocess.check_output(["node", p]).decode()
    finally:
        os.remove(p)
    return json.loads(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2027)
    ap.add_argument("--sundays-only", action="store_true")
    a = ap.parse_args()

    days = []
    d = datetime.date(a.year, 1, 1)
    while d.year == a.year:
        if d.weekday() == 6:
            days.append(d)
        d += datetime.timedelta(days=1)
    if not a.sundays_only:
        for mo, da in ((1, 6), (2, 2), (3, 25), (8, 6), (8, 15),
                       (9, 8), (9, 14), (11, 21), (12, 25)):
            days.append(datetime.date(a.year, mo, da))
    days = sorted(set(days))

    print("%d days of %d, against the calendars the Churches publish\n"
          % (len(days), a.year))
    tally = {}
    for label, juris, get, shift in (
            ("oca (new calendar), oca.org", "oca", oca_gospels, 0),
            ("russian (old calendar), days.pravoslavie.ru", "russian",
             prav_gospels, -13)):
        hit = miss = skip = 0
        misses = []
        for day in days:
            iso = day.isoformat()
            mine = ours(iso, juris)
            g = norm(mine["g"])
            if not g:
                skip += 1
                continue
            url_day = (day + datetime.timedelta(days=shift)).isoformat()
            pub = {norm(x) for x in get(url_day)}
            pub.discard(None)
            if not pub:
                skip += 1
                continue
            if g in pub:
                hit += 1
            else:
                miss += 1
                misses.append("    %s  %s\n        we print %s\n"
                              "        they publish %s"
                              % (iso, (mine["n"] or "")[:44], mine["g"],
                                 ", ".join(sorted(pub)[:6])))
        tally[label] = (hit, miss, skip)
        print("  %s" % label)
        print("    %d of %d agree; %d disagree; %d not comparable"
              % (hit, hit + miss, miss, skip))
        for m in misses:
            print(m)
        print()
    bad = sum(v[1] for v in tally.values())
    print("%d disagreement(s) in all." % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
