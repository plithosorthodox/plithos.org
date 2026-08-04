#!/usr/bin/env python3
"""
Say what each work on the shelf is about, so it can be read by subject.

Author, century, purpose and translator tell a reader who wrote a thing, when,
and what kind of thing it is. None of them answers the question most people
actually arrive with, which is about a subject: what does the Church hold
about the Eucharist, about icons, about what happens when we die.

The tags are topical and nothing more. They say a work treats a subject; they
do not say it treats it first, or best, or definitively. No tag claims
priority and none ranks. That restraint is the point: the shelf is for
research and reading, and a reader who is told which book is "the earliest" on
a question has been handed a conclusion instead of the sources.

A work carries every topic it genuinely treats at length, not every topic it
mentions. Against Heresies touches nearly everything; it is tagged for what a
reader would actually go to it for.

    python3 tools/topics.py --check
    python3 tools/topics.py --write
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "plithos_reader.html"
INDEX = ROOT / "data" / "library" / "works-index.json"

# The vocabulary. Fixed and closed: a tag invented per work is a tag nobody
# can browse by. Ordered as a reader would think rather than alphabetically,
# since this is also the order the facet offers them in.
TOPICS = [
    # God
    "The Holy Trinity",
    "Christ, God and man",
    "The Holy Spirit",
    "Knowing God",
    # creation and the creature
    "Creation",
    "Man, soul and body",
    "Free will and providence",
    "Angels and demons",
    "Deification",
    # the Church
    "The Church",
    "Apostolic tradition",
    "Bishops, priests and deacons",
    "The Theotokos",
    "The saints and their relics",
    # the mysteries
    "Baptism and chrismation",
    "The Eucharist",
    "Repentance and confession",
    "Marriage and virginity",
    # worship and life
    "The Divine Liturgy",
    "Prayer",
    "Fasting",
    "Icons and images",
    "Almsgiving and the poor",
    "The monastic life",
    # the end, and the world
    "The last things",
    "The departed",
    "Martyrdom and persecution",
    # the sources
    "Reading Scripture",
    "Christ foretold in the prophets",
    "The councils and the canons",
    "Answering heresy",
    "Answering the pagans",
]

T = set(TOPICS)

WORKS = {
 "athanasius-contra-gentes": ["Answering the pagans", "Creation", "Knowing God"],
 "athanasius-on-the-incarnation": ["Christ, God and man", "Deification", "Creation"],
 "athanasius-life-of-antony": ["The monastic life", "Angels and demons", "Prayer"],
 "athenagoras-plea": ["Answering the pagans", "The Holy Trinity", "The last things"],
 "basil-hexaemeron": ["Creation", "Reading Scripture"],
 "basil-on-the-holy-spirit": ["The Holy Spirit", "The Holy Trinity", "Apostolic tradition"],
 "basil-letters": ["Bishops, priests and deacons", "The councils and the canons",
                   "The Church", "Repentance and confession", "Answering heresy"],
 "canons-ecumenical": ["The councils and the canons", "Bishops, priests and deacons",
                       "Repentance and confession", "Fasting", "Marriage and virginity"],
 "cassian-conferences": ["The monastic life", "Prayer", "Free will and providence"],
 "cassian-institutes": ["The monastic life", "Prayer", "Fasting"],
 "chrysostom-homilies-hebrews": ["Reading Scripture", "The Eucharist", "Christ, God and man"],
 "chrysostom-homilies-john": ["Reading Scripture", "Christ, God and man"],
 "chrysostom-homilies-matthew": ["Reading Scripture", "Prayer", "Almsgiving and the poor"],
 "chrysostom-homilies-romans": ["Reading Scripture", "Free will and providence"],
 "chrysostom-on-the-priesthood": ["Bishops, priests and deacons", "The Divine Liturgy"],
 "chrysostom-statues": ["Repentance and confession", "Almsgiving and the poor", "Fasting"],
 "clement-instructor": ["Man, soul and body", "Almsgiving and the poor"],
 "clement-stromata": ["Knowing God", "Reading Scripture", "Answering the pagans"],
 "clement-of-rome-first-epistle": ["The Church", "Apostolic tradition",
                                   "Bishops, priests and deacons", "Prayer"],
 "cyprian-unity-of-the-church": ["The Church", "Bishops, priests and deacons"],
 "cyprian-lords-prayer": ["Prayer", "Reading Scripture"],
 "cyprian-on-the-lapsed": ["Repentance and confession", "Martyrdom and persecution",
                           "The Church"],
 "cyprian-on-mortality": ["The departed", "The last things", "Martyrdom and persecution"],
 "cyprian-works-and-alms": ["Almsgiving and the poor", "Repentance and confession"],
 "cyprian-dress-of-virgins": ["Marriage and virginity"],
 "cyprian-to-demetrian": ["Answering the pagans", "Martyrdom and persecution"],
 "cyprian-vanity-of-idols": ["Answering the pagans"],
 "cyprian-on-patience": ["Man, soul and body"],
 "cyprian-jealousy-and-envy": ["Man, soul and body", "Angels and demons"],
 "cyril-jerusalem-catechetical-lectures": ["Baptism and chrismation", "The Eucharist",
                                           "The Divine Liturgy", "The Holy Trinity",
                                           "Christ, God and man", "The last things"],
 "didache": ["Baptism and chrismation", "The Eucharist", "Fasting", "Prayer",
             "Bishops, priests and deacons"],
 "didache-grc": ["Baptism and chrismation", "The Eucharist", "Fasting", "Prayer",
                 "Bishops, priests and deacons"],
 "dionysius-divine-names": ["Knowing God", "The Holy Trinity", "Creation"],
 "dionysius-mystic-theology": ["Knowing God"],
 "dionysius-heavenly-hierarchy": ["Angels and demons", "Knowing God"],
 "dionysius-ecclesiastical-hierarchy": ["The Divine Liturgy", "Baptism and chrismation",
                                        "The Eucharist", "The monastic life",
                                        "The departed", "Bishops, priests and deacons"],
 "dionysius-letters": ["Knowing God", "Christ, God and man"],
 "epistle-of-barnabas": ["Christ foretold in the prophets", "Reading Scripture"],
 "epistle-to-diognetus": ["Answering the pagans", "The Church"],
 "eusebius-church-history": ["The Church", "Apostolic tradition",
                             "Martyrdom and persecution", "Answering heresy"],
 "fragments-of-papias": ["Apostolic tradition", "Reading Scripture"],
 "gregory-great-pastoral-rule": ["Bishops, priests and deacons"],
 "gregory-nazianzen-select-orations": ["The Holy Trinity", "The Holy Spirit",
                                       "Christ, God and man", "Baptism and chrismation"],
 "gregory-nyssa-great-catechism": ["Christ, God and man", "The Holy Trinity",
                                   "Baptism and chrismation", "The Eucharist"],
 "gregory-nyssa-making-of-man": ["Man, soul and body", "Creation", "The last things"],
 "gregory-nyssa-soul-and-resurrection": ["Man, soul and body", "The last things",
                                         "The departed"],
 "gregory-nyssa-on-virginity": ["Marriage and virginity", "The monastic life"],
 "gregory-nyssa-holy-spirit-macedonians": ["The Holy Spirit", "The Holy Trinity",
                                           "Answering heresy"],
 "gregory-nyssa-holy-trinity": ["The Holy Trinity"],
 "gregory-nyssa-not-three-gods": ["The Holy Trinity"],
 "gregory-nyssa-on-the-faith": ["The Holy Trinity"],
 "gregory-nyssa-meletius": ["The departed", "Bishops, priests and deacons"],
 "gregory-nyssa-baptism-of-christ": ["Baptism and chrismation", "Christ, God and man"],
 "gregory-nyssa-infants-early-deaths": ["The departed", "Free will and providence"],
 "gregory-nyssa-on-pilgrimages": ["Prayer"],
 "hippolytus-christ-and-antichrist": ["The last things", "Reading Scripture",
                                      "Christ foretold in the prophets"],
 "hippolytus-scriptural-fragments": ["Reading Scripture", "The last things",
                                     "Christ foretold in the prophets"],
 "ignatius-seven-epistles": ["The Church", "Bishops, priests and deacons",
                             "The Eucharist", "Christ, God and man",
                             "Martyrdom and persecution"],
 "irenaeus-against-heresies": ["Apostolic tradition", "Answering heresy", "The Church",
                               "The Eucharist", "Deification", "Christ, God and man",
                               "Creation"],
 "john-damascus-exposition": ["The Holy Trinity", "Christ, God and man", "Creation",
                              "Man, soul and body", "Icons and images",
                              "The saints and their relics", "Baptism and chrismation",
                              "The Eucharist", "The Theotokos", "Angels and demons"],
 "john-damascus-holy-images": ["Icons and images", "The saints and their relics",
                               "The Theotokos", "Apostolic tradition"],
 "justin-first-apology": ["The Divine Liturgy", "The Eucharist",
                          "Baptism and chrismation", "Answering the pagans"],
 "justin-second-apology": ["Answering the pagans", "Martyrdom and persecution"],
 "justin-dialogue-trypho": ["Christ foretold in the prophets", "Reading Scripture",
                            "Christ, God and man"],
 "martyrdom-of-polycarp": ["Martyrdom and persecution", "The saints and their relics"],
 "methodius-banquet": ["Marriage and virginity", "Reading Scripture"],
 "nicene-constantinopolitan-creed": ["The Holy Trinity", "Christ, God and man",
                                     "The Holy Spirit", "The councils and the canons"],
 "origen-de-principiis": ["Creation", "Free will and providence", "Man, soul and body",
                          "Reading Scripture"],
 "aphrahat-select-demonstrations": ["The last things", "The monastic life",
                                    "Fasting", "Prayer", "Christ, God and man",
                                    "Martyrdom and persecution",
                                    "Bishops, priests and deacons",
                                    "Reading Scripture"],
 "ephraim-nisibene-hymns": ["The last things", "The departed",
                            "Repentance and confession",
                            "Bishops, priests and deacons"],
 "ephraim-nativity-hymns": ["Christ, God and man", "The Theotokos",
                            "Christ foretold in the prophets"],
 "ephraim-epiphany-hymns": ["Baptism and chrismation", "Christ, God and man",
                            "Repentance and confession"],
 "ephraim-the-pearl": ["Christ, God and man", "Knowing God"],
 "ephraim-homilies": ["Christ, God and man", "Repentance and confession"],
 "liturgy-of-st-basil-propers": ["The Divine Liturgy", "The Eucharist",
                                 "Prayer", "The Theotokos", "The departed",
                                 "Christ, God and man", "Creation",
                                 "Man, soul and body"],
 "liturgy-of-st-james": ["The Divine Liturgy", "The Eucharist", "Prayer",
                         "The Theotokos", "The saints and their relics",
                         "The departed", "Bishops, priests and deacons"],
 "liturgy-of-st-mark": ["The Divine Liturgy", "The Eucharist", "Prayer",
                        "The Theotokos", "The saints and their relics",
                        "The departed", "Bishops, priests and deacons"],
 "outside-testimony": ["The Divine Liturgy", "Martyrdom and persecution"],
 "polycarp-to-the-philippians": ["The Church", "Bishops, priests and deacons", "Prayer"],
 "second-clement": ["Repentance and confession", "The last things", "The Church"],
 "seven-ecumenical-councils": ["The councils and the canons", "Christ, God and man",
                               "Icons and images", "Answering heresy"],
 "shepherd-of-hermas": ["Repentance and confession", "Angels and demons", "The Church"],
 "tatian-address-greeks": ["Answering the pagans", "Creation"],
 "theophilus-autolycus": ["Answering the pagans", "The Holy Trinity", "Creation"],
 "vincent-lerins-commonitory": ["Apostolic tradition", "Answering heresy"],
}

# The whole New Testament and the Divine Liturgy stand as one card each on the
# shelf, so their topics are set by prefix rather than one entry per language.
PREFIX = [
    ("bible-", ["Reading Scripture", "Christ, God and man",
                "Christ foretold in the prophets"]),
    ("divine-liturgy-", ["The Divine Liturgy", "The Eucharist", "Prayer",
                         "The Theotokos", "The saints and their relics",
                         "The departed"]),
]


# A Greek edition is the same book and carries the same subjects; saying so
# once here keeps the two from drifting apart.
MIRROR = {"shepherd-of-hermas-grc": "shepherd-of-hermas", 'second-clement-grc': 'second-clement', 'polycarp-philippians-grc': 'polycarp-to-the-philippians', 'martyrdom-of-polycarp-grc': 'martyrdom-of-polycarp', 'epistle-to-diognetus-grc': 'epistle-to-diognetus', 'epistle-of-barnabas-grc': 'epistle-of-barnabas', 'clement-first-epistle-grc': 'clement-of-rome-first-epistle', 'ignatius-seven-epistles-grc': 'ignatius-seven-epistles'}


def topics_for(wid):
    if wid in MIRROR:
        return WORKS[MIRROR[wid]]
    if wid in WORKS:
        return WORKS[wid]
    for pre, tags in PREFIX:
        if wid.startswith(pre):
            return tags
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    bad = [t for tags in list(WORKS.values()) + [x[1] for x in PREFIX]
           for t in tags if t not in T]
    if bad:
        print("tags outside the vocabulary: %s" % sorted(set(bad)))
        return 1

    src = READER.read_text(encoding="utf-8")
    i = src.index("const CORPUS")
    eq = src.index("=", i)
    j = src.index("\n", i)
    corpus = json.loads(src[eq + 1:j].rstrip().rstrip(";"))
    lazy = json.loads(INDEX.read_text(encoding="utf-8"))
    allw = corpus["works"] + lazy

    missing, changed = [], 0
    for w in allw:
        tags = topics_for(w["work_id"])
        if tags is None:
            missing.append(w["work_id"])
            continue
        if w.get("topics") != tags:
            w["topics"] = tags
            changed += 1

    for wid in missing:
        print("  no topics for %s" % wid)

    counts = {}
    for w in allw:
        for t in w.get("topics", []):
            counts[t] = counts.get(t, 0) + 1
    print("%d works, %d changed, %d untagged"
          % (len(allw), changed, len(missing)))
    print("\ntopics in use: %d of %d" % (len(counts), len(TOPICS)))
    for t in TOPICS:
        print("   %-34s %3d" % (t, counts.get(t, 0)))
    unused = [t for t in TOPICS if t not in counts]
    if unused:
        print("\nnot used by any work: %s" % unused)

    if args.write and not missing:
        line = "const CORPUS = " + json.dumps(corpus, ensure_ascii=False,
                                              separators=(",", ":")) + ";"
        READER.write_text(src[:i] + line + src[j:], encoding="utf-8")
        INDEX.write_text(json.dumps(lazy, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote plithos_reader.html and works-index.json")
    elif args.write:
        print("\nnothing written; every work needs a topic first")
        return 1
    elif not args.check:
        print("\nnothing written; pass --write")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
