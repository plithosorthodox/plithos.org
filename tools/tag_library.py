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

# canonical author -> the saint's name in plithos_saints.html, or None.
# Matched by hand. A fuzzy match put St Gregory the Great under St Gregory
# Palamas, which is a different man by six centuries.
AUTHORS = {
    "St John Chrysostom":        "Repose of Saint John Chrysostom, Archbishop of Constantinople",
    "St Athanasius the Great":   "Saint Athanasius the Great, Archbishop of Alexandria",
    "St Justin the Philosopher": "Martyr Justin the Philosopher and those with him at Rome",
    "St Basil the Great":        "Saint Basil the Great, Archbishop of Caesarea in Cappadocia",
    "St John of Damascus":       "Venerable John of Damascus",
    "St Gregory the Theologian": "Saint Gregory the Theologian, Archbishop of Constantinople",
    "St Gregory of Nyssa":       "Saint Gregory, Bishop of Nyssa",
    "St Cyril of Jerusalem":     "Saint Cyril, Archbishop of Jerusalem",
    "St Clement of Rome":        "Hieromartyr Clement, Pope of Rome",
    "St Ignatius of Antioch":    "Hieromartyr Ignatius the God-Bearer, Bishop of Antioch",
    "St Polycarp of Smyrna":     "Hieromartyr Polycarp, Bishop of Smyrna",
    "St John Cassian":           "Venerable John Cassian the Roman",
    "St Vincent of Lerins":      "Saint Vincent of Lerins",
    "St Gregory the Dialogist":  "Saint Gregory Dialogus, Pope of Rome",
    "St Barnabas the Apostle":   "Apostle Barnabas of the Seventy",
    "St Hermas of the Seventy":  "Apostle Hermas of the Seventy",
    "The Twelve Apostles":       "Synaxis of the Holy, Glorious and All-Praised Twelve Apostles",
    # Venerated, but not presently in the Saints index. Listed so the gap is
    # visible rather than silent; see the report at the end of a run.
    "St Theophilus of Antioch":  None,
    "St Papias of Hierapolis":   None,
    "St Clement of Alexandria":  None,
    # Not among the saints, and each for a reason.
    "Origen":                    None,
    "Tatian":                    None,
    "Eusebius of Caesarea":      None,
    "Athenagoras of Athens":     None,
    "The Church of Smyrna":      None,
    "The Ecumenical Councils":   None,
    "The Councils of the Church": None,
    "Mathetes":                  None,
    SCRIPTURE_AUTHOR:            None,
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
 "didache":                         ("The Twelve Apostles", "The Christian life"),
 "clement-instructor":              ("St Clement of Alexandria", "The Christian life"),
 "clement-stromata":                ("St Clement of Alexandria", "Doctrine"),
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
    before = (w.get("author"), w.get("saint"), w.get("purpose"),
              w.get("century"), w.get("centuries"))
    w["author"] = author
    w["saint"] = AUTHORS[author]
    w["purpose"] = purpose
    cc = centuries_of(w.get("date"))
    w["centuries"] = cc
    w["century"] = cc[0] if cc else None
    w["period"] = label(w["century"])
    return before != (w.get("author"), w.get("saint"), w.get("purpose"),
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
        s = AUTHORS.get(a)
        print("   %-30s %2d  %s" % (a, n, ("-> " + s[:44]) if s else "(not in the Saints index)"))
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
