# -*- coding: utf-8 -*-
"""The guide's section on fasting.

The Guide carried a colour legend for the five degrees and nothing that said
what any of them means. This writes that section into the KEY table and
teaches renderKey to show it.

It states what is kept and cites where each rule is written. It does not
exhort, and it does not adjudicate: where the Churches differ it says so and
names both usages.

Two things are called fasting and the first draft ran them together, saying
that Sunday is never a fast day. That is true only of the fast from foods.
The fast before Communion is total and is kept on whatever day one communes,
Sunday included - Carthage 41, received by the Council in Trullo in Canon 29,
which withdrew the single exception Carthage had allowed. Both canons are in
the Library.

    python3 tools/fasting_guide.py --write
"""
import io, json, re, sys

PATH = "index.html"

BODY = u"""<p>Two things are called fasting, and they are kept differently.</p>

<h4>The fast before Communion</h4>

<p>Total abstinence from food and drink before receiving the Holy Mysteries, in the usual reckoning from midnight. It is kept on whatever day one communes, Sunday and feast days included, and it ends when Communion has been received. The Council of Carthage ruled that the Sacraments of the Altar are not celebrated except by those who are fasting; the Council in Trullo received that canon and withdrew the one exception it had allowed.</p>

<p>It is separate from everything below, which concerns the fast from certain foods on the days the Church appoints.</p>

<h4>Wednesday and Friday</h4>

<p>The oldest fast in the Church. The Didache, of the first century, takes them for granted: "fast on the fourth day and the Preparation." Wednesday is kept for the betrayal and Friday for the Crucifixion. They are kept as a strict fast through the year apart from the fast-free weeks below. Apostolic Canon 69 binds them on clergy and laity alike, excepting anyone "hindered by some bodily infirmity."</p>

<h4>Sunday</h4>

<p>The fast from foods is not kept on a Sunday. The Council of Gangra anathematizes fasting on Sunday "under pretence of asceticism", and Apostolic Canon 66 deposes a cleric found fasting on the Lord's Day or the Sabbath, "excepting the one only", which is Great and Holy Saturday.</p>

<p>Within a fasting season the season continues on Sunday but is relaxed: wine and oil, and in the Apostles' and Nativity fasts fish as well. Saturdays are relaxed the same way, which is why the Council in Trullo rebuked the Roman practice of fasting the Saturdays of Lent.</p>

<h4>The seasons</h4>

<p>Great Lent with Holy Week. The Apostles' Fast, from the Monday after All Saints to the eve of Saints Peter and Paul, its length varying with the date of Pascha. The Dormition Fast, the first fourteen days of August. The Nativity Fast, from the fifteenth of November to the twenty-fourth of December.</p>

<p>Three single days are kept strictly wherever in the week they fall: the Exaltation of the Cross, the Beheading of the Forerunner, and the eve of Theophany.</p>

<h4>Fast-free</h4>

<p>Bright Week; the week after Pentecost; the days from the Nativity to the eve of Theophany; and the week after the Sunday of the Publican and the Pharisee. Cheesefare week permits dairy, eggs and fish all week, Wednesday and Friday included, but no meat.</p>

<h4>The degrees</h4>

<ul><li><b>Strict.</b> No meat, dairy, eggs, fish, wine or oil. In its monastic form this is xerophagy, dry food taken once a day after Vespers.</li>
<li><b>Wine and oil.</b> The same abstinence, with wine and olive oil.</li>
<li><b>Fish.</b> Fish, and wine and oil with it.</li>
<li><b>Dairy.</b> No meat; dairy, eggs and fish permitted.</li>
<li><b>Fast-free.</b> No fast.</li></ul>

<h4>Why calendars differ</h4>

<p>The rule printed here follows the Typikon of the Great Lavra of St Sabbas, a monastic rule received as the common standard. What a layman keeps is set by his bishop and his spiritual father, and the local Churches have not set it identically: Greek usage gives fish through most of the Apostles' and Nativity fasts, Slavic usage keeps fish to Saturdays and Sundays, and several jurisdictions publish a lighter rule for those seasons. Choosing a Church at the head of the calendar changes what this page prints.</p>

<h4>Exceptions</h4>

<p>Apostolic Canon 69 names bodily infirmity. The Church applies this to the sick and to those whose treatment requires food, to pregnant and nursing women, to young children, to the old and the frail, and to travellers and guests at another table. The application is a matter for a priest.</p>"""

SRC = ("The canons are in the Library and may be read there: the Didache 8; "
       "the Apostolic Canons 66 and 69; Gangra 18; Carthage 41; the Council "
       "in Trullo 29, 55 and 89; and St Peter of Alexandria 15. The seasons "
       "and the degrees follow the Typikon.")

CSS_ANCHOR = ".keyterms{margin:0}"
CSS_ADD = (".keypanel h4{font-family:var(--display);font-weight:600;font-size:14.5px;"
           "color:var(--ink);margin:18px 0 2px}"
           ".keypanel ul{margin:4px 0 12px;padding-left:20px;font-size:13.5px;"
           "line-height:1.55;color:var(--ink-soft)}"
           ".keypanel ul li{margin:4px 0}"
           ".keypanel ul li b{color:var(--ink);font-weight:600}")

RENDER_OLD = ('<h3>${t("fast")}</h3><div class="keylegend">${sw}</div>')
RENDER_NEW = ('<h3>${t("fast")}</h3><div class="keylegend">${sw}</div>'
              '${o.fastBody||KEY.fastBody}'
              '<p class="keynote keyrulesrc">${o.fastSrc||KEY.fastSrc}</p>')


def apply(src):
    changed = []

    # 1. the copy itself, at the head of KEY. Written afresh each time, so a
    #    correction to the text lands rather than being declined as present.
    ins = "fastBody:%s,fastSrc:%s," % (json.dumps(BODY), json.dumps(SRC))
    i = src.index("const KEY={") + len("const KEY={")
    if src[i:i + len("fastBody:")] == "fastBody:":
        j = i
        depth, instr, q, esc = 0, False, "", False
        while j < len(src):
            ch = src[j]
            if instr:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == q:
                    instr = False
            elif ch in "\"'":
                instr, q = True, ch
            elif ch == "," and depth == 0 and src[j + 1:j + 9] == "fastSrc:":
                depth = 1
            elif ch == "," and depth == 1:
                j += 1
                break
            j += 1
        old = src[i:j]
        if old == ins:
            pass
        else:
            src = src[:i] + ins + src[j:]
            changed.append("KEY.fastBody/fastSrc rewritten")
    else:
        src = src[:i] + ins + src[i:]
        changed.append("KEY.fastBody/fastSrc")

    # 2. renderKey shows it under the legend it explains
    if "${o.fastBody||KEY.fastBody}" not in src:
        if RENDER_OLD not in src:
            raise SystemExit("renderKey: legend template not found")
        src = src.replace(RENDER_OLD, RENDER_NEW, 1)
        changed.append("renderKey")

    # 3. headings and lists inside the panel
    if ".keypanel h4{" not in src:
        src = src.replace(CSS_ANCHOR, CSS_ADD + CSS_ANCHOR, 1)
        changed.append("keypanel css")

    return src, changed


def main():
    src = io.open(PATH, encoding="utf-8").read()
    out, changed = apply(src)
    if "--write" in sys.argv:
        io.open(PATH, "w", encoding="utf-8").write(out)
        print("wrote %s: %s" % (PATH, ", ".join(changed) or "nothing"))
    else:
        print("would change: %s" % (", ".join(changed) or "nothing"))


if __name__ == "__main__":
    main()
