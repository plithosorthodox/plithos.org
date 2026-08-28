#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Saints kept on the civil date, not thirteen days after it.

The synaxarion is a table of menaion dates: the calendar takes the civil day,
subtracts the Julian offset for a Church on the old calendar, and looks the
result up. That is right for a saint of the fourth century, whose day is a
day of the Church's own reckoning.

It is wrong for a saint of the twentieth, whose day is the day he died by the
clock on the wall. St Tikhon reposed on 7 April 1925 - which was 25 March in
the Julian calendar, the feast of the Annunciation - and both Churches keep
him on 7 April: the OCA because that is the date it prints, Moscow because 25
March old style IS 7 April. This site kept him on 7 April for a Church on the
new calendar and on 20 April for a Church on the old, which is nobody's date.

  Repose of St Tikhon        oca.org 2026-04-07;
                             days.pravoslavie.ru 2026-03-25 Julian, headed
                             "March 25/April 7", Преставление свт. Тихона (1925)
  Glorification of St Tikhon days.pravoslavie.ru 2026-09-26 Julian,
                             Свт. Тихона... (прославление, 1989) = 9 October
  St Matrona of Moscow       days.pravoslavie.ru 2026-04-19 Julian,
                             Блж. Матроны Московской (1952) = 2 May

An entry marked c:1 is looked up on the civil date instead, so it falls on the
same day for every Church. Everything else is untouched.

    python3 tools/civil_commemorations.py --check
    python3 tools/civil_commemorations.py --write
"""
import argparse
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

CIVIL = [
    "Repose of Saint Tikhon, Patriarch of Moscow, Enlightener of North America",
    "Glorification of Saint Tikhon, Patriarch of Moscow and All Russia, Enlightener of North America",
    "Saint Matrona of Moscow",
]

OLD = ('{const men=mode==="old"?addDays(d,-juliOffset(y)):d;'
       'const mk=pad(men.getMonth()+1)+"-"+pad(men.getDate());'
       'const syn=SYNAXARION[mk];if(syn)for(const s of syn){'
       'if(principal&&s.g)continue;if(out.some(o=>o.name===s.n))continue;'
       'out.push({name:s.n,great:!!s.g,cal:"",mmdd:mk});}}')

NEW = ('{const men=mode==="old"?addDays(d,-juliOffset(y)):d;'
       'const mk=pad(men.getMonth()+1)+"-"+pad(men.getDate());'
       'const ck=pad(d.getMonth()+1)+"-"+pad(d.getDate());'
       '/* A saint of the twentieth century is kept on the day he reposed by '
       'the civil clock, which is the same day for every Church; a saint of '
       'the fourth is kept on a menaion date, which is not. */'
       'const take=(key,wantCivil)=>{const syn=SYNAXARION[key];if(!syn)return;'
       'for(const s of syn){if(!!s.c!==wantCivil)continue;'
       'if(principal&&s.g)continue;if(out.some(o=>o.name===s.n))continue;'
       'out.push({name:s.n,great:!!s.g,cal:"",mmdd:key});}};'
       'take(mk,false);take(ck,true);}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    marked = [n for n in CIVIL
              if ("{n:%s,c:1}" % json.dumps(n, ensure_ascii=False)) in src]
    hooked = "take(mk,false);take(ck,true);" in src

    if not a.write:
        print("kept on the civil date: %d of %d; the calendar %s"
              % (len(marked), len(CIVIL),
                 "looks them up that way" if hooked else "does NOT"))
        for n in CIVIL:
            if n not in marked:
                print("   not marked: " + n)
        return 0 if (len(marked) == len(CIVIL) and hooked) else 1

    for n in CIVIL:
        q = json.dumps(n, ensure_ascii=False)
        plain, civil = "{n:%s}" % q, "{n:%s,c:1}" % q
        if civil in src:
            continue
        if plain not in src:
            print("not in the synaxarion: " + n)
            return 1
        src = src.replace(plain, civil, 1)
    if not hooked:
        if OLD not in src:
            print("the synaxarion lookup is not where it was")
            return 1
        src = src.replace(OLD, NEW, 1)
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("%d saints are now kept on the same day by every Church" % len(CIVIL))
    return 0


if __name__ == "__main__":
    sys.exit(main())
