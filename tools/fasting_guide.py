# -*- coding: utf-8 -*-
"""The guide's section on fasting.

The Guide overlay carried a colour legend for the five degrees and nothing
that said what any of them means, when the Church fasts, or why two Orthodox
calendars can print a different degree for the same day. This writes that
section into the KEY table and teaches renderKey to show it.

Everything asserted here is carried in the Library and cited by name in the
source line: the Didache, the Apostolic Canons, Gangra, the Council in
Trullo, St Peter of Alexandria and St John Chrysostom.

    python3 tools/fasting_guide.py --write
"""
import io, json, re, sys

PATH = "index.html"

BODY = u"""<p>Fasting is not a diet and it is not a payment. It is the body's share in what the soul is doing, and the Church has never let it stand by itself: it is given together with prayer and with almsgiving, and it is the third of these that shows whether the other two were real. St John Chrysostom said it to his own people in Antioch: "Do you fast? Give me proof of it by your works. Is it said by what kind of works? If you see a poor man, take pity on him."</p>

<h4>Wednesday and Friday</h4>

<p>These two days are the oldest fast in the Church, older than Lent. The Didache, which belongs to the first century, already takes them for granted: "let not your fasts be with the hypocrites, for they fast on the second and fifth day of the week; but fast on the fourth day and the Preparation." Wednesday is kept because on that day the Lord was betrayed, and Friday because on that day He suffered. St Peter of Alexandria gives those two reasons and no others.</p>

<p>They are kept as a strict fast through the whole year, apart from the fast-free weeks below, and they are not a counsel. The sixty-ninth of the Apostolic Canons deposes a cleric who does not keep them and cuts off a layman who does not, "unless he be hindered by some bodily infirmity". That clause is the canon's own exception, and every later relaxation rests on it.</p>

<h4>Sunday</h4>

<p>Sunday is never a fast day. It is the day of the Resurrection, and to fast on it is to mourn on the morning the Church has been given for rejoicing. The Council of Gangra anathematized whoever fasts on Sunday "under pretence of asceticism", and the sixty-sixth Apostolic Canon deposes a cleric found fasting on the Lord's Day or on the Sabbath, "excepting the one only": Great and Holy Saturday, the single Saturday of the year on which the Church does fast, and then only until midnight.</p>

<p>Inside a fasting season Sunday is not therefore fast-free. The season goes on, but it is relaxed. Wine and oil are given, in the Apostles' and Nativity Fasts fish as well, and the day itself is kept as a feast. Saturdays are relaxed the same way, which is why the Council in Trullo rebuked the Church of Rome for fasting the Saturdays of Lent.</p>

<h4>When the Church fasts</h4>

<p>Four seasons. Great Lent with Holy Week. The Apostles' Fast, which begins on the Monday after All Saints and ends on the eve of Saints Peter and Paul, so that its length moves with the date of Pascha and can be a single week or six. The Dormition Fast, the first fourteen days of August. The Nativity Fast, forty days from the fifteenth of November.</p>

<p>Three single days are kept strictly wherever in the week they fall: the Exaltation of the Cross, the Beheading of the Forerunner, and the eve of Theophany. Wednesday and Friday keep the rest of the year.</p>

<p>Five times the fast is lifted altogether: Bright Week; the week after Pentecost; the days from the Nativity to the eve of Theophany; and the week after the Sunday of the Publican and the Pharisee, which is left fast-free precisely so that nobody may fast in the Pharisee's manner. Cheesefare week is the fast running backwards: the meat is already gone, but dairy, eggs and fish are kept all week, Wednesday and Friday with the rest.</p>

<h4>The degrees</h4>

<ul><li><b>Strict.</b> No meat, dairy, eggs, fish, wine or oil. In its full monastic form this is xerophagy, dry food taken once a day after Vespers; in ordinary parish use it is the abstinence without the single meal.</li>
<li><b>Wine and oil.</b> The same abstinence, with wine and olive oil given. Usually a saint's day, a Saturday or a Sunday.</li>
<li><b>Fish.</b> Fish permitted, and wine and oil with it.</li>
<li><b>Dairy.</b> No meat; dairy, eggs and fish permitted. Cheesefare week.</li>
<li><b>Fast-free.</b> No fast of any kind.</li></ul>

<h4>Why calendars differ</h4>

<p>The rule printed here is the one the Church received in the Typikon of the Great Lavra of St Sabbas, and that is a monastic rule. It is the standard against which everything else is measured, not a description of what a layman is expected to manage. What he actually keeps is set by his bishop and by his own spiritual father, and the local Churches have not set it identically. The Greek usage gives fish through most of the Apostles' and Nativity Fasts; the Slavic usage keeps fish to Saturdays and Sundays; several jurisdictions publish a lighter rule for the same seasons. They are keeping one fast, and none of them is the exception to it.</p>

<p>Choose a Church at the head of the calendar and the degrees follow that Church's own published rule where it differs from the others. But the disposition of a fast belongs to a priest and not to a page. Ask yours. He may lighten what is printed here, and he may know a reason to keep it as printed that this page cannot.</p>

<h4>Who is excused</h4>

<p>The canon that binds the fast names the exception in the same breath, and the Church has always read it widely: the sick, and anyone whose treatment or condition requires food; women who are pregnant or nursing; small children; the old and the frail; travellers, and guests at another's table, where refusing what has been set out would wound the host more than the meat would wound you.</p>

<p>None of this is a dispensation to be applied for. It is the ordinary judgement of a priest, which is why the fast was given to a Church and not to a rulebook. The one thing nobody is excused from is the reason for it. He who cannot fast from food should not therefore fast from mercy.</p>"""

SRC = ("The canons are in the Library and may be read there: the Didache 8; "
       "the Apostolic Canons 66 and 69; Gangra 18; the Council in Trullo 55 "
       "and 89; St Peter of Alexandria, Canon 15; and St John Chrysostom, "
       "Homilies on the Statues 3. The seasons and the degrees follow the Typikon.")

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

    # 1. the copy itself, at the head of KEY
    if "fastBody:" not in src:
        i = src.index("const KEY={")
        ins = ("fastBody:%s,fastSrc:%s,"
               % (json.dumps(BODY), json.dumps(SRC)))
        src = src[:i + len("const KEY={")] + ins + src[i + len("const KEY={"):]
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
