#!/usr/bin/env python3
"""
Give every work in the Library the tags a reader browses by.

The catalogue could be read but not sorted through. A reader who wanted
Chrysostom, or the fourth century, or something written to defend the faith,
had only a full-text search over the corpus, which finds words inside books
rather than books themselves.

Four fields are set here, and each one is curated rather than derived:

  author    one canonical spelling. The corpus held "St. John Chrysostom",
            "St John Chrysostom" and "John Chrysostom" for the same man, so
            eleven of his works would have filed under three different names.
  saint     the exact name this author carries in the Saints index, so a work
            can link to the life of the person who wrote it. Null where the
            author is not among the saints, which is a real answer and not a
            gap: Origen was condemned at the Fifth Council, Tatian ended an
            Encratite, Eusebius was an Arian sympathiser.
  is_saint  whether the Orthodox Church venerates this author, which is not
            the same question as whether the index holds his life. The field
            was already there and held True, False and null across the eleven
            works of one man. It decides whether the shelf gives him a title,
            so it is not a field to leave to whatever the last import wrote.
  purpose   what the work was written to do, in the reader's terms rather
            than a cataloguer's. Derived from a curated table, because the
            existing genre field held "apology" and "apologetic" as separate
            values and covered only three quarters of the shelf.
  century   a number, from the work's own date.

    python3 tools/tag_library.py --check
    python3 tools/tag_library.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "plithos_reader.html"
INDEX = ROOT / "data" / "library" / "works-index.json"

# The New Testament bundles carried the identifier of the text they were built
# from in the author field, so the Library listed a man named "kjv
# (public-domain), NT per plithos manifest".
SCRIPTURE_AUTHOR = "The Apostles and Evangelists"

# canonical author -> (venerated as a saint in the Orthodox Church,
#                      the saint's name in plithos_saints.html or None)
#
# The two are separate facts. A man can be venerated and still be missing
# from the index, which is a gap; and he can be absent from the index because
# the Church does not venerate him, which is an answer. Running them together
# is how a title gets attached to a name the Church has not given it to.
#
# Matched by hand. A fuzzy match put St Gregory the Great under St Gregory
# Palamas, which is a different man by six centuries.
AUTHORS = {
    "St John Chrysostom":        (True, "Repose of Saint John Chrysostom, Archbishop of Constantinople"),
    "St Athanasius the Great":   (True, "Saint Athanasius the Great, Archbishop of Alexandria"),
    "St Justin the Philosopher": (True, "Martyr Justin the Philosopher and those with him at Rome"),
    "St Basil the Great":        (True, "Saint Basil the Great, Archbishop of Caesarea in Cappadocia"),
    "St John of Damascus":       (True, "Venerable John of Damascus"),
    "St Gregory the Theologian": (True, "Saint Gregory the Theologian, Archbishop of Constantinople"),
    "St Gregory of Nyssa":       (True, "Saint Gregory, Bishop of Nyssa"),
    "St Cyril of Jerusalem":     (True, "Saint Cyril, Archbishop of Jerusalem"),
    "St Clement of Rome":        (True, "Hieromartyr Clement, Pope of Rome"),
    "St Ignatius of Antioch":    (True, "Hieromartyr Ignatius the God-Bearer, Bishop of Antioch"),
    "St Polycarp of Smyrna":     (True, "Hieromartyr Polycarp, Bishop of Smyrna"),
    "St John Cassian":           (True, "Venerable John Cassian the Roman"),
    "St Vincent of Lerins":      (True, "Saint Vincent of Lerins"),
    "St Gregory the Dialogist":  (True, "Saint Gregory Dialogus, Pope of Rome"),
    "St Barnabas the Apostle":   (True, "Apostle Barnabas of the Seventy"),
    "St Hermas of the Seventy":  (True, "Apostle Hermas of the Seventy"),
    "The Twelve Apostles":       (True, "Synaxis of the Holy, Glorious and All-Praised Twelve Apostles"),
    "St Irenaeus of Lyons":      (True, "Hieromartyr Irenaeus, Bishop of Lyons"),
    "St Cyprian of Carthage":    (True, "Hieromartyr Cyprian, Bishop of Carthage"),
    "St Hippolytus of Rome":     (True, "Hieromartyr Hippolytus, and those with him"),
    "St Methodius of Olympus":   (True, "Hieromartyr Methodius, Bishop of Patara"),
    "St Ephraim the Syrian":     (True, "Venerable Ephraim the Syrian"),
    "The Apostles and Evangelists": (True, None),
    # Commemorated on 6 December and on 22 February in the Prologue of Ohrid;
    # neither is on the calendar of the Orthodox Church in America, which is
    # where most of the index comes from. Both now have a life to link to.
    "St Theophilus of Antioch":  (True, "Saint Theophilus, Bishop of Antioch"),
    "St Papias of Hierapolis":   (True, "Saint Papias, Bishop of Hierapolis"),
    # Not among the saints, and each for a reason. Clement of Alexandria is
    # not commemorated in the Orthodox Church: veneration ceased after
    # Photius held that he had degraded the Son to the rank of a creature.
    # He is read and he is not titled.
    "Clement of Alexandria":     (False, None),
    "Origen":                    (False, None),
    "Tatian":                    (False, None),
    "Eusebius of Caesarea":      (False, None),
    "Athenagoras of Athens":     (False, None),
    "Mathetes":                  (False, None),
    # The homily copied beside Clement's letter and long called his second.
    # It is not his, and the preacher's name is not known.
    "An unknown preacher":       (False, None),
    # Not persons.
    "The Church of Smyrna":      (False, None),
    "The Ecumenical Councils":   (False, None),
    "The Councils of the Church": (False, None),
    # Not Christians at all. A governor, a historian and a satirist, kept
    # for what they saw rather than for anything they believed.
    "Witnesses outside the Church": (False, None),
    # The Corpus Areopagiticum is received and read; the Areopagite of Acts
    # 17 did not write it, and the shelf does not give him the title on the
    # strength of a name a manuscript carries.
    "Dionysius the Areopagite":  (False, None),
}

# work_id -> (canonical author, purpose)
WORKS = {
 "john-damascus-exposition":        ("St John of Damascus", "Doctrine"),
 "athanasius-life-of-antony":       ("St Athanasius the Great", "Lives of the saints"),
 "athanasius-contra-gentes":        ("St Athanasius the Great", "Defence of the faith"),
 "athanasius-on-the-incarnation":   ("St Athanasius the Great", "Doctrine"),
 "athenagoras-plea":                ("Athenagoras of Athens", "Defence of the faith"),
 "tatian-address-greeks":           ("Tatian", "Defence of the faith"),
 "theophilus-autolycus":            ("St Theophilus of Antioch", "Defence of the faith"),
 "irenaeus-against-heresies":       ("St Irenaeus of Lyons", "Defence of the faith"),
 "second-clement":                  ("An unknown preacher", "Preaching"),
 "cyprian-unity-of-the-church":     ("St Cyprian of Carthage", "Doctrine"),
 "cyprian-lords-prayer":            ("St Cyprian of Carthage", "The life of prayer"),
 "cyprian-on-mortality":            ("St Cyprian of Carthage", "The Christian life"),
 "cyprian-works-and-alms":          ("St Cyprian of Carthage", "The Christian life"),
 "hippolytus-christ-and-antichrist": ("St Hippolytus of Rome", "Scripture opened"),
 "hippolytus-scriptural-fragments": ("St Hippolytus of Rome", "Scripture opened"),
 "cyprian-on-the-lapsed":           ("St Cyprian of Carthage", "Repentance and confession"),
 "cyprian-dress-of-virgins":        ("St Cyprian of Carthage", "The Christian life"),
 "cyprian-to-demetrian":            ("St Cyprian of Carthage", "Defence of the faith"),
 "cyprian-vanity-of-idols":         ("St Cyprian of Carthage", "Defence of the faith"),
 "cyprian-on-patience":             ("St Cyprian of Carthage", "The Christian life"),
 "cyprian-jealousy-and-envy":       ("St Cyprian of Carthage", "The Christian life"),
 "outside-testimony":               ("Witnesses outside the Church", "Witness to the apostles"),
 "dionysius-divine-names":          ("Dionysius the Areopagite", "Doctrine"),
 "dionysius-mystic-theology":       ("Dionysius the Areopagite", "The spiritual life"),
 "dionysius-heavenly-hierarchy":    ("Dionysius the Areopagite", "Doctrine"),
 "dionysius-ecclesiastical-hierarchy": ("Dionysius the Areopagite", "The Divine Liturgy"),
 "dionysius-letters":               ("Dionysius the Areopagite", "Letters"),
 "gregory-nyssa-on-virginity":        ("St Gregory of Nyssa", "The Christian life"),
 "gregory-nyssa-making-of-man":       ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-soul-and-resurrection": ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-holy-spirit-macedonians": ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-holy-trinity":        ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-not-three-gods":      ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-on-the-faith":        ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-meletius":            ("St Gregory of Nyssa", "Preaching"),
 "gregory-nyssa-baptism-of-christ":   ("St Gregory of Nyssa", "Preaching"),
 "gregory-nyssa-infants-early-deaths": ("St Gregory of Nyssa", "Doctrine"),
 "gregory-nyssa-on-pilgrimages":      ("St Gregory of Nyssa", "The Christian life"),
 "methodius-banquet":               ("St Methodius of Olympus", "The Christian life"),
 # The purpose here is the kind of thing a work is, and these are hymns: they
 # were written to be sung, and Ephraim's whole method was to teach the faith
 # in metre because the heretics of Edessa were already singing theirs.
 "ephraim-nisibene-hymns":          ("St Ephraim the Syrian", "Hymns"),
 "ephraim-nativity-hymns":          ("St Ephraim the Syrian", "Hymns"),
 "ephraim-epiphany-hymns":          ("St Ephraim the Syrian", "Hymns"),
 "ephraim-the-pearl":               ("St Ephraim the Syrian", "Hymns"),
 "ephraim-homilies":                ("St Ephraim the Syrian", "Preaching"),
 "john-damascus-holy-images":       ("St John of Damascus", "Defence of the faith"),
 "basil-letters":                   ("St Basil the Great", "Letters"),
 "justin-first-apology":            ("St Justin the Philosopher", "Defence of the faith"),
 "justin-second-apology":           ("St Justin the Philosopher", "Defence of the faith"),
 "justin-dialogue-trypho":          ("St Justin the Philosopher", "Defence of the faith"),
 "vincent-lerins-commonitory":      ("St Vincent of Lerins", "Doctrine"),
 "nicene-constantinopolitan-creed": ("The Ecumenical Councils", "Canon law and the Councils"),
 "seven-ecumenical-councils":       ("The Ecumenical Councils", "Canon law and the Councils"),
 "canons-ecumenical":               ("The Councils of the Church", "Canon law and the Councils"),
 "epistle-of-barnabas":             ("St Barnabas the Apostle", "Letters"),
 "basil-on-the-holy-spirit":        ("St Basil the Great", "Doctrine"),
 "basil-hexaemeron":                ("St Basil the Great", "Scripture opened"),
 "clement-of-rome-first-epistle":   ("St Clement of Rome", "Letters"),
 "cyril-jerusalem-catechetical-lectures": ("St Cyril of Jerusalem", "Instruction of catechumens"),
 "gregory-nazianzen-select-orations": ("St Gregory the Theologian", "Preaching"),
 "gregory-nyssa-great-catechism":   ("St Gregory of Nyssa", "Instruction of catechumens"),
 "ignatius-seven-epistles":         ("St Ignatius of Antioch", "Letters"),
 "chrysostom-on-the-priesthood":    ("St John Chrysostom", "The pastor's office"),
 "epistle-to-diognetus":            ("Mathetes", "Defence of the faith"),
 "fragments-of-papias":             ("St Papias of Hierapolis", "Witness to the apostles"),
 "polycarp-to-the-philippians":     ("St Polycarp of Smyrna", "Letters"),
 "martyrdom-of-polycarp":           ("The Church of Smyrna", "Lives of the saints"),
 "eusebius-church-history":         ("Eusebius of Caesarea", "The history of the Church"),
 "chrysostom-homilies-romans":      ("St John Chrysostom", "Scripture opened"),
 "chrysostom-homilies-hebrews":     ("St John Chrysostom", "Scripture opened"),
 "chrysostom-homilies-john":        ("St John Chrysostom", "Scripture opened"),
 "chrysostom-homilies-matthew":     ("St John Chrysostom", "Scripture opened"),
 "chrysostom-statues":              ("St John Chrysostom", "Preaching"),
 "origen-de-principiis":            ("Origen", "Doctrine"),
 "gregory-great-pastoral-rule":     ("St Gregory the Dialogist", "The pastor's office"),
 "cassian-conferences":             ("St John Cassian", "The spiritual life"),
 "cassian-institutes":              ("St John Cassian", "The spiritual life"),
 "second-clement-grc":                ("An unknown preacher", "Preaching"),
 "polycarp-philippians-grc":          ("St Polycarp of Smyrna", "Letters"),
 "martyrdom-of-polycarp-grc":         ("The Church of Smyrna", "Lives of the saints"),
 "epistle-to-diognetus-grc":          ("Mathetes", "Defence of the faith"),
 "epistle-of-barnabas-grc":           ("St Barnabas the Apostle", "Letters"),
 "clement-first-epistle-grc":         ("St Clement of Rome", "Letters"),
 "ignatius-seven-epistles-grc":       ("St Ignatius of Antioch", "Letters"),
 "shepherd-of-hermas-grc":         ("St Hermas of the Seventy", "The spiritual life"),
 "didache-grc":                     ("The Twelve Apostles", "The Christian life"),
 "didache":                         ("The Twelve Apostles", "The Christian life"),
 "clement-instructor":              ("Clement of Alexandria", "The Christian life"),
 "clement-stromata":                ("Clement of Alexandria", "Doctrine"),
 "shepherd-of-hermas":              ("St Hermas of the Seventy", "The spiritual life"),
}
LITURGY_PURPOSE = "The Divine Liturgy"
SCRIPTURE_PURPOSE = "Holy Scripture"

ORDINALS = {1: "1st", 2: "2nd", 3: "3rd"}


def centuries_of(date):
    """Every century a work's own date names, earliest first.

    Dates in the catalogue are written several ways, and a work that falls
    through lands in a "(no date)" bucket nobody browses. An ordinal wins
    if the string names a century at all, in whatever abbreviation ("4th
    century", "4th-5th c."); otherwise the years decide, down to two
    digits, since 1 Clement is dated "c. 96".

    A work whose date spans a range belongs to all of it, not to one end.
    The canons were gathered between the apostles and the Seventh Council,
    and a reader looking through the fourth century should find Nicaea
    among them.
    """
    if not date:
        return []
    d = str(date)
    if re.search(r"(?:centur|cent\.|\bc\.)", d, re.I):
        n = [int(x) for x in re.findall(r"(\d{1,2})\s*(?:st|nd|rd|th)", d, re.I)]
        if n:
            return list(range(min(n), max(n) + 1))
    y = [int(x) for x in re.findall(r"\b(\d{1,4})\b", d)]   # c. 96, 325-787, 387
    if y:
        lo, hi = (min(y) - 1) // 100 + 1, (max(y) - 1) // 100 + 1
        return list(range(lo, hi + 1))
    return []


def century_of(date):
    """The century a work is filed under: the first one its date names."""
    c = centuries_of(date)
    return c[0] if c else None


def label(c):
    return "%s century" % ORDINALS.get(c, "%dth" % c) if c else None


def tag(w, report):
    wid = w.get("work_id") or ""
    if wid.startswith("bible-"):
        author, purpose = SCRIPTURE_AUTHOR, SCRIPTURE_PURPOSE
    elif wid.startswith("divine-liturgy-"):
        author, purpose = "St John Chrysostom", LITURGY_PURPOSE
    elif wid in WORKS:
        author, purpose = WORKS[wid]
    else:
        report.append("no tags curated for %s" % wid)
        return False
    if author not in AUTHORS:
        report.append("%s: author %r has no entry in AUTHORS" % (wid, author))
        return False
    before = (w.get("author"), w.get("saint"), w.get("purpose"), w.get("is_saint"),
              w.get("century"), w.get("centuries"))
    venerated, saint = AUTHORS[author]
    w["author"] = author
    w["saint"] = saint
    w["is_saint"] = venerated
    w["purpose"] = purpose
    cc = centuries_of(w.get("date"))
    w["centuries"] = cc
    w["century"] = cc[0] if cc else None
    w["period"] = label(w["century"])
    return before != (w.get("author"), w.get("saint"), w.get("purpose"), w.get("is_saint"),
                      w.get("century"), w.get("centuries"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    src = READER.read_text(encoding="utf-8")
    i = src.index("const CORPUS")
    eq = src.index("=", i)
    j = src.index("\n", i)
    corpus = json.loads(src[eq + 1:j].rstrip().rstrip(";"))
    lazy = json.loads(INDEX.read_text(encoding="utf-8"))

    report, changed = [], 0
    for w in corpus["works"] + lazy:
        if tag(w, report):
            changed += 1

    for line in report:
        print("  %s" % line)

    allw = corpus["works"] + lazy
    import collections
    print("%d works, %d retagged" % (len(allw), changed))
    print("\nauthors: %d" % len(set(w["author"] for w in allw)))
    for a, n in collections.Counter(w["author"] for w in allw).most_common():
        ven, s = AUTHORS.get(a, (False, None))
        note = ("-> " + s[:42]) if s else ("venerated; not in the Saints index"
                                           if ven else "not among the saints")
        print("   %-30s %2d  %s" % (a, n, note))
    print("\npurposes:")
    for p, n in collections.Counter(w["purpose"] for w in allw).most_common():
        print("   %-30s %d" % (p, n))
    print("\ncenturies (a work counts in every century its date names):")
    bucket = collections.Counter()
    for w in allw:
        for c in (w.get("centuries") or [None]):
            bucket[c] += 1
    for c, n in sorted(bucket.items(), key=lambda x: (x[0] is None, x[0] or 0)):
        print("   %-30s %d" % (label(c) or "(no date)", n))

    if args.write:
        line = "const CORPUS = " + json.dumps(corpus, ensure_ascii=False,
                                              separators=(",", ":")) + ";"
        READER.write_text(src[:i] + line + src[j:], encoding="utf-8")
        INDEX.write_text(json.dumps(lazy, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote plithos_reader.html and works-index.json")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main())
