#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Saints page's own words, in the languages that lack them.

saints.html carries its interface in SUI, one block to a language, and a
language absent from it meets the page in English however complete its saints
are. Georgian's vocabulary and calendar entries are published and its lives
are nearly done, so it would otherwise have fifteen hundred saints in Georgian
under an English page.

These are the site's own words - headings, filter labels, a lede - and not
liturgical text, so they are written here as the rest of the site's copy is.
The vocabulary they draw on is the one docs/GEORGIAN.md settled: ერისკაცობაში
for the name a monastic bore in the world, შერაცხვა for glorification,
ნაწილები for relics, წოდება for the rank.

Two fields are not words and are easy to get wrong by copying English:
dayFirst is true, because Georgian writes the day before the month, and
centuryNum is roman, as Georgian sets centuries.

    python3 tools/saints_sui.py --check
    python3 tools/saints_sui.py --write
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "saints.html")

KA = u''' ka:{
  months:["იანვარი","თებერვალი","მარტი","აპრილი","მაისი","ივნისი","ივლისი","აგვისტო","სექტემბერი","ოქტომბერი","ნოემბერი","დეკემბერი"],
  mabbr:["იან.","თებ.","მარ.","აპრ.","მაი.","ივნ.","ივლ.","აგვ.","სექ.","ოქტ.","ნოე.","დეკ."],
  dayFirst:true,centuryNum:"roman",
  title:"წმინდანები",
  lede:"მართლმადიდებლური წელიწადის ყოველი ხსენება, წოდების, ადგილისა და ნიშნის მიხედვით არჩევით და დღის ან სახელის მიხედვით დალაგებით. საუკუნე, წარმომავლობა და მფარველობა დაემატება იმის კვალად, თუ როგორ იწერება ერთი და ერთი ცხოვრება.",
  search:"მოძებნეთ წმინდანი სახელით",
  language:"ენა",
  filters:"არჩევა",
  allOrders:"ყველა წოდება",anyAttr:"ნებისმიერი ნიშანი",anyPlace:"ნებისმიერი ადგილი",anyCountry:"ნებისმიერი ქვეყანა",anyMonth:"ნებისმიერი თვე",allJur:"ყველა იურისდიქცია",
  great:"დიდი დღესასწაულები",sortName:"სახელით",sortDate:"დღით",
  showing:"ნაჩვენებია %1 ხსენება %2-დან",
  none:"არცერთი ხსენება არ შეესაბამება ამ არჩევას.",
  note:"დამატებითი არჩევა - საუკუნის, წარმომავლობისა და მფარველობის მიხედვით - აქ გამოჩნდება, როგორც ერთი და ერთი წმინდანის ცხოვრება იწერება.",
  close:"დახურვა",greatFeast:"დიდი დღესასწაული",world:"ერისკაცობაში:",
  nolife:"ეს ცხოვრება ჯერ არ დაწერილა.",
  inIcon:"ხატწერაში",more:"+ კიდევ %1",century:"%1 საუკუნე",bc:"ქრისტემდე",lifespan:"%1 - %2",unknownYear:"?",
  fLived:"სიცოცხლის წლები",fCentury:"საუკუნე",fEra:"ეპოქა",fRank:"წოდება",fState:"წესი",fOrigin:"წარმომავლობა",fRegion:"მხარე",
  fGlorified:"შერაცხვის წელი",fCanonized:"შერაცხა",fRelics:"წმ. ნაწილები",fPatronPlaces:"მფარველი ადგილებისა",
  fPatronWork:"მფარველი საქმიანობისა",fPatronCauses:"მეოხი",fTitles:"აგრეთვე იწოდება",
  fFeastRank:"დღესასწაულის წოდება",fRelated:"დაკავშირებული ხსენებები",
  tagline:"მთელის მიხედვით"
 },
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    here = bool(re.search(r"[{,]\s*ka\s*:\s*\{", src))
    if not a.write:
        print("the Saints page speaks Georgian: %s" % ("yes" if here else "NO"))
        return 0 if here else 1
    if here:
        print("Georgian is already in SUI; nothing to do")
        return 0
    m = re.search(r"SUI\s*=\s*\{", src)
    if not m:
        print("SUI is not where it was")
        return 1
    at = src.index("{", m.end() - 1) + 1
    src = src[:at] + "\n" + KA.rstrip("\n") + src[at:]
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("the Saints page now speaks Georgian")
    return 0


if __name__ == "__main__":
    sys.exit(main())
