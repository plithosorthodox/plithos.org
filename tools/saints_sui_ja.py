#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Saints page's own words in Japanese.

saints.html carries its interface in SUI, one block to a language, and a
language absent from it meets the page in English however complete its saints
are. Japanese has its vocabulary, its calendar entries and all but the last
two hundred of its lives, so it would otherwise have fifteen hundred saints in
Japanese under an English page.

The nouns are not proposed here. Every one of them is already published
somewhere in this repository and is copied from there:

    記憶      a commemoration        the calendar's own ui.commem
    聖人      a saint                the calendar's ui.q_saint and the nav
    管轄      a jurisdiction         the calendar's ui.jurisdiction
    言語      language               the calendar's ui.language
    大祭      a great feast          data/saint-terms.v5.ja.json, "Great Feast"
    聖遺物    relics                 the glossary
    列聖      the glorification      the glossary
    聖像画    iconography            the terms table, 21 times
    転達      an intercession        the terms table, "intercession"
    紀元前    before Christ          the lives, written 紀元前5世紀

Three fields are not words, and copying the English on any of them would be
wrong in a way no proofreader of the text itself would catch:

  centuryNum is plain. The lives count in kanji figures - 十二世紀 - because
  they are prose, but the interface counts in the figures the interface
  already uses: the calendar's own months are 1月 and not 一月, and a century
  standing in a filter beside them is 12世紀.

  mdFmt exists because Japanese joins a month to a day rather than ordering
  them. Neither dayFirst branch can write 1月15日; the pattern can.

  listSep is 、 and not a comma, and listSepLong is ／ where the English
  sets a semicolon between phrases that carry commas of their own.

    python3 tools/saints_sui_ja.py --check
    python3 tools/saints_sui_ja.py --write
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "saints.html")

JA = u''' ja:{
  months:["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
  mabbr:["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
  dayFirst:false,centuryNum:"plain",mdFmt:"%1%2日",listSep:"、",listSepLong:"／",
  title:"聖人",
  lede:"正教会の一年のすべての記憶を、位、地、特徴によって絞り込み、日付または名前で並べ替えることができます。世紀、出自、庇護は、一人一人の生涯が書かれるにつれて加わります。",
  search:"聖人を名前で検索",
  language:"言語",
  filters:"絞り込み",
  allOrders:"すべての位",anyAttr:"すべての特徴",anyPlace:"すべての地",anyCountry:"すべての国",anyMonth:"すべての月",allJur:"すべての管轄",
  great:"大祭",sortName:"名前",sortDate:"日付",
  showing:"%2件の記憶のうち%1件を表示",
  none:"この絞り込みに該当する聖人はありません。",
  note:"世紀、出自の地、庇護による絞り込みは、一人一人の聖人の生涯が書かれるにつれてここに現れます。",
  close:"閉じる",greatFeast:"大祭",world:"俗名",
  nolife:"この聖人の生涯はまだ書かれていません。",
  inIcon:"聖像画",more:"ほか%1件",century:"%1世紀",bc:"紀元前",bcFmt:"%2%1年",yearFmt:"%1年",lifespan:"%1 - %2",unknownYear:"不詳",
  fLived:"生没年",fCentury:"世紀",fEra:"時代",fRank:"位",fState:"身分",fOrigin:"出自",fRegion:"地方",
  fGlorified:"列聖の年",fCanonized:"列聖",fRelics:"聖遺物",fPatronPlaces:"守護する地",
  fPatronWork:"守護する職",fPatronCauses:"転達",fTitles:"称号",
  fFeastRank:"祭日の位",fRelated:"関連する記憶",
  tagline:"全体に従って"
 },
'''

# The one vocabulary a Japanese Orthodox reader checks first, and the one a
# dictionary supplies instead. None of the right-hand column belongs on this
# site; see docs/JAPANESE.md.
FORBIDDEN = [u"キリスト", u"イエス", u"聖霊",
             u"ペテロ", u"ヨハネ", u"マリア"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    bad = [w for w in FORBIDDEN if w in JA]
    if bad:
        print("the block carries a word from outside the Church: %s"
              % " ".join(bad))
        return 1
    src = io.open(PAGE, encoding="utf-8").read()
    here = bool(re.search(r"[{,]\s*ja\s*:\s*\{\s*\n?\s*months", src))
    if not a.write:
        print("the Saints page speaks Japanese: %s" % ("yes" if here else "NO"))
        return 0 if here else 1
    if here:
        print("Japanese is already in SUI; nothing to do")
        return 0
    m = re.search(r"SUI\s*=\s*\{", src)
    if not m:
        print("SUI is not where it was")
        return 1
    at = src.index("{", m.end() - 1) + 1
    src = src[:at] + "\n" + JA.rstrip("\n") + src[at:]
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("the Saints page now speaks Japanese")
    return 0


if __name__ == "__main__":
    sys.exit(main())
