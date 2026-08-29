#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Saints page's own words in Swahili.

This is not work held for the day the lives finish. Swahili's vocabulary and
its calendar entries are already published and saints.html already loads
both, so a Swahili reader meets fifteen hundred saints in Swahili under an
English interface today, and has since the terms landed.

The nouns are copied from what is published rather than proposed:

    Ukumbusho             a commemoration    the calendar's ui.commem
    Mtakatifu             a saint            the calendar's ui.q_saint
    Mamlaka               a jurisdiction     the calendar's ui.jurisdiction
    Lugha                 language           the calendar's ui.language
    Nchi zote             all countries      the calendar's ui.cfAll
    Sikukuu Kuu           a great feast      the glossary, and the terms table
    Masalia               relics             the glossary
    Kutangazwa mtakatifu  the glorification  the glossary
    Ikoni                 the icon           the glossary
    maombezi              an intercession    the terms table
    karne                 a century          the terms table, karne ya kwanza

A century is the one field that cannot be copied from English. Swahili counts
it in words after ya - karne ya kwanza, karne ya nne - which is how the terms
table writes it in prose, so the interface is given the same words rather than
a figure. Only the first two are irregular; from the third the ordinal is the
plain cardinal.

    python3 tools/saints_sui_sw.py --check
    python3 tools/saints_sui_sw.py --write
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "saints.html")

SWNUM = (u'const SWNUM=["","kwanza","pili","tatu","nne","tano","sita","saba",'
         u'"nane","tisa","kumi","kumi na moja","kumi na mbili","kumi na tatu",'
         u'"kumi na nne","kumi na tano","kumi na sita","kumi na saba",'
         u'"kumi na nane","kumi na tisa","ishirini","ishirini na moja"];\n')

SWNOTE = (u'/* Swahili counts a century in words after ya, as the lives count'
          u' it:\n   karne ya kwanza, karne ya nne. Only the first two are'
          u' irregular. */\n')

SW = u''' sw:{
  months:["Januari","Februari","Machi","Aprili","Mei","Juni","Julai","Agosti","Septemba","Oktoba","Novemba","Desemba"],
  mabbr:["Jan.","Feb.","Mac.","Apr.","Mei","Jun.","Jul.","Ago.","Sep.","Okt.","Nov.","Des."],
  dayFirst:true,centuryNum:"swahili",
  title:"Watakatifu",
  lede:"Kila ukumbusho wa mwaka wa Kiorthodoksi, wenye kuchujwa kwa daraja, mahali na sifa, na kupangwa kwa siku au kwa jina. Karne, asili na ulinzi huongezwa kadiri maisha ya kila mmoja yanavyoandikwa.",
  search:"Tafuta mtakatifu kwa jina",
  language:"Lugha",
  filters:"Vichujio",
  allOrders:"Madaraja yote",anyAttr:"Sifa yoyote",anyPlace:"Mahali popote",anyCountry:"Nchi zote",anyMonth:"Mwezi wowote",allJur:"Mamlaka zote",
  great:"Sikukuu Kuu",sortName:"Jina",sortDate:"Tarehe",
  showing:"Zinaonyeshwa %1 kati ya ukumbusho %2",
  none:"Hakuna mtakatifu anayelingana na vichujio hivi.",
  note:"Vichujio vingine, vya karne, mahali pa asili na ulinzi, vitaonekana hapa kadiri maisha ya kila mtakatifu yanavyoandikwa.",
  close:"Funga",greatFeast:"Sikukuu Kuu",world:"Ulimwenguni:",
  nolife:"Maisha haya bado hayajaandikwa.",
  inIcon:"Katika ikoni",more:"+ %1 zaidi",century:"karne ya %1",bc:"KK",lifespan:"%1 hadi %2",unknownYear:"?",
  fLived:"Aliishi",fCentury:"Karne",fEra:"Zama",fRank:"Daraja",fState:"Hali",fOrigin:"Asili",fRegion:"Eneo",
  fGlorified:"Mwaka wa kutangazwa mtakatifu",fCanonized:"Kutangazwa mtakatifu",fRelics:"Masalia",fPatronPlaces:"Mlinzi wa",
  fPatronWork:"Mlinzi wa kazi",fPatronCauses:"Mwombezi kwa",fTitles:"Pia huitwa",
  fFeastRank:"Daraja la sikukuu",fRelated:"Zinazohusiana",
  tagline:"kulingana na yote"
 },
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    here = bool(re.search(r"[{,]\s*sw\s*:\s*\{\s*\n?\s*months", src))
    nums = "SWNUM" in src
    if not a.write:
        print("the Saints page speaks Swahili: %s%s"
              % ("yes" if here else "NO",
                 "" if nums else " (and counts its centuries in English)"))
        return 0 if here and nums else 1
    if here:
        print("Swahili is already in SUI; nothing to do")
        return 0

    if not nums:
        anchor = u'function _num(n){var k=ui("centuryNum");'
        if anchor not in src:
            print("_num is not where it was")
            return 1
        src = src.replace(anchor, SWNOTE + SWNUM + anchor, 1)
        old = u' if(k==="plain")return ""+n;'
        if old not in src:
            print("the plain branch is not where it was")
            return 1
        src = src.replace(old, old + u'\n if(k==="swahili")return SWNUM[n]||n;', 1)

    m = re.search(r"SUI\s*=\s*\{", src)
    if not m:
        print("SUI is not where it was")
        return 1
    at = src.index("{", m.end() - 1) + 1
    src = src[:at] + "\n" + SW.rstrip("\n") + src[at:]
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("the Saints page now speaks Swahili")
    return 0


if __name__ == "__main__":
    sys.exit(main())
