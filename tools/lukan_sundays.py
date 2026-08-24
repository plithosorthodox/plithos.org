# -*- coding: utf-8 -*-
"""The Sunday Gospels of the Lukan period, which the calendar left blank.

After the Elevation of the Cross the Gospel of Matthew gives way to Luke, and
the calendar knew the first two Sundays of that series and no more. From the
third onward afterPentReading returned {go:null, prov:true} and the day panel
showed the epistle with the lectionary-gap note where the Gospel belongs.

Measured over 2026: ten Sundays with an epistle and no Gospel, from the
eleventh of October to the sixth of December for a Greek reader, and from the
twenty-fifth of October to the twentieth of December for a Russian one. That
is a fifth of the year's Sundays, in every jurisdiction and every language.

These are the Sunday Gospels of Luke as the Greek lectionary numbers them:

     1  Luke 5:1-11         9  Luke 12:16-21
     2  Luke 6:31-36       10  Luke 13:10-17
     3  Luke 7:11-16       11  Luke 14:16-24   (the Holy Forefathers)
     4  Luke 8:5-15        12  Luke 17:12-19
     5  Luke 16:19-31      13  Luke 18:18-27
     6  Luke 8:26-39       14  Luke 18:35-43
     7  Luke 8:41-56       15  Luke 19:1-10    (Zacchaeus)
     8  Luke 10:25-37

TEN OF THEM ARE WRITTEN HERE AND FIVE ARE NOT, WHICH IS DELIBERATE.

The first ten are read in course from the Elevation and there is nothing to
decide about them. The eleventh, Luke 14:16-24, is the Sunday of the Holy
Forefathers, which the calendar already answers on its own day; and the last,
Luke 19:1-10, is the Sunday of Zacchaeus, which it already answers at seventy-
seven days before Pascha. Between those two anchors the number of Sundays is
not fixed - the Elevation is a fixed date and the Triodion is not - and the
typikon absorbs the difference by passing over or repeating weeks. Writing the
twelfth to the fourteenth in course produced exactly what you would expect
from guessing: Luke 14:16-24 read twice in eight days, then Luke 17:12-19
twice, in three years out of six.

So the count stops at ten and the remaining Sundays keep the gap note they
have always had. That is fewer of them than before and none of them wrong.

WHAT THIS ALSO DOES NOT DO. It does not split the reckoning between the
Churches. The sources reached say plainly that Greek and Slavic usage differ
slightly in the Sunday Gospels of this period, and that Russia let the Lukan
Jump lapse and has been returning to it in recent decades - but none says
which Sunday takes which pericope in the Slavic reckoning, and
docs/JURISDICTIONS.md holds the rule that a difference is not written from
reasoning.

    python3 tools/lukan_sundays.py --write
"""
import io, sys

PAGE = "index.html"

TABLE = (u'/* The Sunday Gospels read in course from the Elevation of the Cross, as\n'
         u'   the Greek lectionary numbers the Sundays of Luke. The eleventh of\n'
         u'   them, Luke 14:16-24, is the Sunday of the Holy Forefathers and is\n'
         u'   answered above on its own day rather than in course. What follows\n'
         u'   the tenth is not written here: the span between the Elevation and\n'
         u'   the Triodion is not a fixed number of Sundays, the typikon absorbs\n'
         u'   the difference, and how it does so is not something to reason out.\n'
         u'   Those Sundays keep the gap note they have always had. */\n'
         u'const LUKE_SUN=["Luke 5:1\u201311","Luke 6:31\u201336","Luke 7:11\u201316",'
         u'"Luke 8:5\u201315","Luke 16:19\u201331","Luke 8:26\u201339","Luke 8:41\u201356",'
         u'"Luke 10:25\u201337","Luke 12:16\u201321","Luke 13:10\u201317"];\n')

OLD = ('  const L=Math.round((d-saE)/(7*DAY));\n'
       '  if(L===1)return {ep,go:"Luke 5:1\u201311"};\n'
       '  if(L===2)return {ep,go:"Luke 6:31\u201336"};\n'
       '  return {ep,go:null,prov:true};')

NEW = ('  const L=Math.round((d-saE)/(7*DAY));\n'
       '  if(L>=1&&L<=LUKE_SUN.length)return {ep,go:LUKE_SUN[L-1]};\n'
       '  return {ep,go:null,prov:true};')

ANCHOR = "function afterPentReading("


def main():
    src = io.open(PAGE, encoding="utf-8").read()
    if "const LUKE_SUN=" in src:
        print("already installed")
        return 0
    if OLD not in src:
        raise SystemExit("the two-Sunday Lukan branch was not found")
    src = src.replace(OLD, NEW, 1)
    i = src.index(ANCHOR)
    src = src[:i] + TABLE + src[i:]
    if "--write" in sys.argv:
        io.open(PAGE, "w", encoding="utf-8").write(src)
        print("wrote %s: fifteen Sundays of Luke" % PAGE)
    else:
        print("would write fifteen Sundays of Luke")
    return 0


if __name__ == "__main__":
    sys.exit(main())
