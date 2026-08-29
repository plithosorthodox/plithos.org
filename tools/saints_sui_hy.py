#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Saints page's own words in Armenian.

Armenian's vocabulary is finished - 10,632 of 10,632, published - and hy is in
TERMS_LANGS, so saints.html already fetches Armenian names for an Armenian
reader. The interface was the last thing on the page still in English for him.

Every noun is copied from what is published rather than proposed. Armenian is
the awkward case, because the site is not of one mind about its orthography
and docs/ARMENIAN.md says so plainly: the names table and the hundred prayers
are CLASSICAL (Mesropian), while data/ui-i18n.v5.hy.json and
data/rule-i18n.v5.hy.json are REFORMED. The doc calls that a defect in those
files rather than a fork. So the words are taken from the calendar's own
interface and re-spelled classically on the way in, exactly as the doc does
for the glossary - Հիշատակ becomes յիշատակ, Տոն becomes տօն, Իրավասություն
becomes իրաւասութիւն - and the ranks come from the finished terms table,
which is classical already:

    Վանական      monastic          Սրբապետ      hierarch
    Երանելի      venerable         Մարգարէ      prophet
    Նահատակ      martyr            Խոստովանող   confessor
    Մեծ նահատակ  great-martyr      Սքանչելագործ wonderworker
    Աշխարհական   layman            Մասունքներ   relics

The prose is modern Eastern Armenian in the classical spelling, which is the
combination the Church and the diaspora publishers have used for a century and
the one the finished vocabulary writes: ում է 202 times, ում են 260, ւում է
77, and the Western կ' not once. The prayers are grabar and are quoted, not
imitated.

A century is the field that could not be copied. docs/ARMENIAN.md settles on
European digits rather than the Armenian letter numerals, so the figure
stands - but the Armenian ordinal splits, 1-ին against 2-րդ and everything
after, which no existing centuryNum branch can express. Hence ARNUM.

    python3 tools/saints_sui_hy.py --check
    python3 tools/saints_sui_hy.py --write
"""
import argparse
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "saints.html")

ARNUM = (u'const ARNUM=["","1-ին","2-րդ","3-րդ","4-րդ","5-րդ","6-րդ","7-րդ",'
         u'"8-րդ","9-րդ","10-րդ","11-րդ","12-րդ","13-րդ","14-րդ","15-րդ",'
         u'"16-րդ","17-րդ","18-րդ","19-րդ","20-րդ","21-րդ"];\n')

ARNOTE = (u'/* Armenian counts a century in European digits, as its own\n'
          u'   register notes settle, but its ordinal is 1-ին and then -րդ. */\n')

HY = u''' hy:{
  months:["Յունուար","Փետրուար","Մարտ","Ապրիլ","Մայիս","Յունիս","Յուլիս","Օգոստոս","Սեպտեմբեր","Հոկտեմբեր","Նոյեմբեր","Դեկտեմբեր"],
  mabbr:["Յունու.","Փետր.","Մարտ","Ապր.","Մայիս","Յունիս","Յուլիս","Օգոս.","Սեպտ.","Հոկտ.","Նոյեմ.","Դեկտ."],
  dayFirst:true,centuryNum:"armenian",
  title:"Սրբեր",
  lede:"Ուղղափառ տարուայ ամէն յիշատակ՝ ընտրելի ըստ դասի, վայրի եւ նշանի, դասաւորելի ըստ օրուայ կամ անուան։ Դարը, ծագումը եւ հովանաւորութիւնը աւելանում են այնպէս, ինչպէս գրւում է իւրաքանչիւր վարք։",
  search:"Որոնել սուրբ ըստ անուան",
  language:"Լեզու",
  filters:"Ընտրանք",
  allOrders:"Բոլոր դասերը",anyAttr:"Ամէն նշան",anyPlace:"Ամէն վայր",anyCountry:"Բոլոր երկրները",anyMonth:"Ամէն ամիս",allJur:"Բոլոր իրաւասութիւնները",
  great:"Մեծ տօներ",sortName:"Անուն",sortDate:"Օր",
  showing:"Ցուցադրւում է %2 յիշատակից %1-ը",
  none:"Այս ընտրանքին յարմար սուրբ չկայ։",
  note:"Այլ ընտրանքներ՝ ըստ դարի, ծագման վայրի եւ հովանաւորութեան, կերեւան այստեղ, երբ գրւում է իւրաքանչիւր սրբի վարքը։",
  close:"Փակել",greatFeast:"Մեծ տօն",world:"Աշխարհում՝",
  nolife:"Այս վարքը դեռ գրուած չէ։",
  inIcon:"Սրբապատկերում",more:"+ եւս %1",century:"%1 դար",bc:"Ք.ա.",bcFmt:"%2 %1",lifespan:"%1 - %2",unknownYear:"?",
  fLived:"Ապրել է",fCentury:"Դար",fEra:"Դարաշրջան",fRank:"Դաս",fState:"Կարգ",fOrigin:"Ծագում",fRegion:"Երկրամաս",
  fGlorified:"Սրբադասման տարի",fCanonized:"Սրբադասում",fRelics:"Մասունքներ",fPatronPlaces:"Հովանաւոր",
  fPatronWork:"Արհեստների հովանաւոր",fPatronCauses:"Բարեխօս",fTitles:"Կոչւում է նաեւ",
  fFeastRank:"Տօնի աստիճան",fRelated:"Առնչուող յիշատակներ",
  tagline:"ըստ ամբողջի"
 },
'''

# The reformed spellings the site's other Armenian files use. None of them
# belongs in a block that stands beside the classical names table.
REFORMED = [u"և", u"ություն", u"Հովհաննես", u"Աստվածածին", u"սարկավագ",
            u"մարգարե", u"Հիսուս", u"Տոն", u"Իրավասություն", u"բարեխոս"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    bad = [w for w in REFORMED if w in HY]
    if bad:
        print("the block carries a reformed spelling: %s" % " ".join(bad))
        return 1
    body = re.sub(r'[a-zA-Z_]+:|"[a-zA-Z.-]*"|true|false|%1|%2', "", HY)
    stray = re.findall(r"[A-Za-zЀ-ӿͰ-Ͽ]", body)
    if stray:
        print("the block carries foreign script: %s" % "".join(sorted(set(stray))))
        return 1

    src = io.open(PAGE, encoding="utf-8").read()
    here = bool(re.search(r"[{,]\s*hy\s*:\s*\{\s*\n?\s*months", src))
    nums = "ARNUM" in src
    if not a.write:
        print("the Saints page speaks Armenian: %s%s"
              % ("yes" if here else "NO",
                 "" if nums else " (and counts its centuries in English)"))
        return 0 if here and nums else 1
    if here:
        print("Armenian is already in SUI; nothing to do")
        return 0

    if not nums:
        anchor = u'function _num(n){var k=ui("centuryNum");'
        if anchor not in src:
            print("_num is not where it was")
            return 1
        src = src.replace(anchor, ARNOTE + ARNUM + anchor, 1)
        old = u' if(k==="plain")return ""+n;'
        if old not in src:
            print("the plain branch is not where it was")
            return 1
        src = src.replace(old, old + u'\n if(k==="armenian")return ARNUM[n]||n;', 1)

    m = re.search(r"SUI\s*=\s*\{", src)
    if not m:
        print("SUI is not where it was")
        return 1
    at = src.index("{", m.end() - 1) + 1
    src = src[:at] + "\n" + HY.rstrip("\n") + src[at:]
    io.open(PAGE, "w", encoding="utf-8").write(src)
    print("the Saints page now speaks Armenian")
    return 0


if __name__ == "__main__":
    sys.exit(main())
