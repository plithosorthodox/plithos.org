#!/usr/bin/env python3
"""
Emit data/prayers.v2.json from the PRAYERS array embedded in index.html, and
attach the section each prayer belongs to.

index.html keeps its own inline copy - the calendar's prayer overlay still
uses it, and nothing there changes. prayers.html fetches this file instead of
carrying a second hand-maintained copy. tools/check_site.py fails the build if
the two drift apart.

The 100 prayers arrived under 26 categories, many holding one or two prayers,
which is why the section felt scattered. SECTIONS below regroups them the way
a printed Orthodox prayer book is ordered - the daily rule first, then the
Hours, the Jesus Prayer, preparation for Communion, and so outward from the
self to the household and the departed. The original `cat` value is preserved
on every prayer and shown as a sub-heading, so nothing is lost or renamed.

    python3 tools/build_prayers.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n_prayers as I18N
import i18n_prayer_text as TEXT

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "prayers.v2.json"

# section id, English title, one-line description, and the categories it holds
SECTIONS = [
    ("daily", "Morning and Evening",
     "The fixed rule of the day, said on rising and before sleep.",
     ["Daily Prayers"]),
    ("hours", "The Hours",
     "The prayer of the Church through the day, from midnight to compline.",
     ["The Hours of Prayer"]),
    ("heart", "The Jesus Prayer and Short Prayers",
     "The Jesus Prayer itself, and other brief prayers for use through the day.",
     ["Prayers of the Heart"]),
    ("communion", "Holy Communion",
     "Preparation before the Mysteries, and thanksgiving after. The Fathers "
     "make a pure conscience the condition of approaching, not the quantity "
     "of prayer said beforehand - see On the Prayer Rule.",
     ["Before Holy Communion", "Thanksgiving After Holy Communion"]),
    ("intercession", "The Theotokos, the Angels, and the Saints",
     "Prayers to the Mother of God, the bodiless powers, and the saints.",
     ["To the Most Holy Theotokos", "To the Holy Angels",
      "To the Saint of the Day", "Akathists"]),
    ("others", "For Others",
     "For family, for kindred, for the living and for the departed.",
     ["For Others", "For Family and Loved Ones", "For Children",
      "For Kindred", "For the Departed"]),
    ("self", "For Oneself",
     "Repentance, the spiritual life, and prayer in affliction.",
     ["For Oneself", "For the Spiritual Life", "For Chastity and Purity",
      "Finding a Spiritual Father", "In Distress and Affliction"]),
    ("occasions", "Life and Its Occasions",
     "The home, travel, work and study, marriage, and the bearing of children.",
     ["For Mother and Child", "For the Home", "For Travelers",
      "For Work and School", "In Seeking a Spouse",
      "For the Victims of Abortion"]),
    ("psalms", "Psalms",
     "The psalms most used in private prayer.",
     ["Psalms"]),
]


# Which part of the Communion sequence a prayer belongs to. Keyed by title so
# the assignment is explicit and reviewable rather than inferred.
#
# "I believe, O Lord, and I confess" and "Of Thy Mystical Supper" are the two
# said at the chalice itself in the received order; the rest form the body of
# the Order of Preparation, kept the evening before or the morning of
# according to local custom and one's spiritual father.
# Only one prayer in the "Prayers of the Heart" category is the Jesus Prayer.
# The other eight are short prayers of the heart, which is not the same thing:
# the Jesus Prayer is a single received formula with recognised shorter forms,
# said continually, and grouping the rest under its name obscured that.
HEART_GROUP = {"The Jesus Prayer": "The Jesus Prayer"}
HEART_DEFAULT = "Short prayers for use through the day"


COMMUNION_PHASE = {
    "I Believe, O Lord, and I Confess": "at-the-chalice",
    "Of Thy Mystical Supper": "at-the-chalice",
}
PHASE_LABEL = {
    "preparation": "The Order of Preparation",
    "at-the-chalice": "Immediately before receiving",
    "thanksgiving": "After receiving",
}

# What each part of the sequence actually is, and when it is said. Without
# this the section reads as an undifferentiated wall of long prayers, which
# invites the idea that all of it is a threshold to be cleared.
PHASE_DESC = {
    "preparation": "Ten prayers, by five authors, kept on the evening before "
                   "receiving or on the morning itself according to local "
                   "custom. Prayer books print them as one continuous order, "
                   "but they are not ten versions of one thing: they run from "
                   "133 words to 696, and each takes up a different aspect of "
                   "approaching. How much is said is set by one's spiritual "
                   "father. Where only a little is possible, the three "
                   "shortest - St John of Damascus, the Second of St John "
                   "Chrysostom, and the Verses of St Symeon Metaphrastes - "
                   "together come to under five minutes.",
    "at-the-chalice": "Said at the chalice itself, after the Gifts are brought "
                      "out. In most parishes the whole congregation says these "
                      "together with the priest.",
    "thanksgiving": "Said after returning from the chalice, at the end of the "
                    "Liturgy or on coming home.",
}

HEART_DESC = {
    "The Jesus Prayer": "One prayer, said continually rather than once: "
                        "Lord Jesus Christ, Son of God, have mercy on me, a "
                        "sinner. The Fathers permit shorter forms where that "
                        "is too much - Lord Jesus Christ, have mercy on me, or "
                        "simply Lord, have mercy. It needs no book and no "
                        "voice, and can be carried through an ordinary day.",
    "Short prayers for use through the day": "Brief prayers for particular "
                                             "needs. They are not the Jesus "
                                             "Prayer, and are not said "
                                             "continually in the same way, but "
                                             "they are short enough to be said "
                                             "at any moment.",
}


# What each prayer of the Order actually says, written from its text. Without
# this the Order reads as ten interchangeable long prayers, which is both
# inaccurate and discouraging: they differ in length by a factor of five and
# in subject entirely. Lengths are counted from the text at build time.
PRAYER_DESC = {
    "Prayer of St. Basil the Great":
        "Traces the whole economy of salvation - creation, the Incarnation, "
        "the Supper - and only then asks to partake without condemnation.",
    "First Prayer of St. John Chrysostom":
        "Takes up the centurion's words, that one is not worthy for Christ to "
        "come under his roof, and applies them to the soul as a house fallen "
        "into ruin.",
    "Prayer of St. John of Damascus":
        "Brief. Asks forgiveness for offences committed knowingly and "
        "unknowingly before approaching.",
    "Prayer of St. Basil the Great Before Receiving":
        "Confesses outright that one partakes unworthily, and asks that the "
        "Mysteries be for healing rather than judgement.",
    "Prayer of St. Symeon Metaphrastes":
        "On the Incarnation as the ground of our approach: Christ took our "
        "whole nature, and so we may come.",
    "Prayer of St. Symeon the New Theologian":
        "The longest and most personal of the Order - from sullied lips, from "
        "an abominable heart - and the most searching in its self-accusation.",
    "Second Prayer of St. John Chrysostom":
        "The centurion again, but resolved: since Christ wills to dwell in "
        "him, he takes courage and approaches.",
    "Third Prayer of St. John Chrysostom":
        "A plain petition for the remission of sins committed from youth, "
        "without extended imagery.",
    "Second Prayer of St. John of Damascus":
        "Standing at the doors of the sanctuary, pleading the Publican, the "
        "Canaanite woman and the Thief.",
    "Before Communion: Verses of St. Symeon Metaphrastes":
        "Verses said while approaching: burn me not as I partake, for Thou "
        "art Fire which consumeth the unworthy.",
    "I Believe, O Lord, and I Confess":
        "The confession of faith in the Mysteries themselves. Said aloud by "
        "the whole congregation in most parishes.",
    "Of Thy Mystical Supper":
        "The shortest of all, and the one nobody omits: like the thief will I "
        "confess Thee. Said by everyone at the chalice.",
    "Thanksgiving After Communion":
        "Thanks for having been received, and asks that the Gifts be for "
        "healing rather than judgement.",
    "Thanksgiving of St. Basil the Great":
        "Thanks for all things, closing with the song of Simeon.",
}


def communion_phase(p):
    if p.get("cat") == "Thanksgiving After Holy Communion":
        return "thanksgiving"
    return COMMUNION_PHASE.get(p.get("title"), "preparation")


def group_label(sid, p):
    """The heading a prayer sits under inside its section."""
    if sid == "communion":
        return PHASE_LABEL.get(communion_phase(p))
    if sid == "heart":
        return HEART_GROUP.get(p.get("title"), HEART_DEFAULT)
    return None


def group_desc(sid, p):
    """A line of context under that heading."""
    if sid == "communion":
        return PHASE_DESC.get(communion_phase(p))
    if sid == "heart":
        return HEART_DESC.get(group_label(sid, p))
    return None


def load_prayers():
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    i = s.index("const PRAYERS=")
    j = s.index("\n", i)
    return json.loads(s[i + len("const PRAYERS="):j].rstrip().rstrip(";"))


def main():
    prayers = load_prayers()

    cat_to_section = {}
    for sid, _title, _desc, cats in SECTIONS:
        for c in cats:
            if c in cat_to_section:
                print("ERROR: category %r is claimed by two sections" % c)
                return 1
            cat_to_section[c] = sid

    unmapped = sorted({p["cat"] for p in prayers} - set(cat_to_section))
    if unmapped:
        print("ERROR: these categories are in index.html but not in SECTIONS:")
        for c in unmapped:
            print("   %s" % c)
        print("Add them to SECTIONS - a prayer with no section would be "
              "unreachable on prayers.html.")
        return 1

    out = []
    for n, p in enumerate(prayers):
        sid = cat_to_section[p["cat"]]
        phase = communion_phase(p) if sid == "communion" else None
        out.append({
            "i": n,                       # index into the original PRAYERS array
            "s": sid,
            "phase": phase,
            "phaseLabel": group_label(sid, p),
            "phaseDesc": group_desc(sid, p),
            "desc": PRAYER_DESC.get(p.get("title")),
            "words": len((p.get("body") or "").split()),
            "cat": p["cat"],
            "title": p.get("title", ""),
            "body": p.get("body", ""),
            "note": p.get("note", ""),
            "src": p.get("src", ""),
            "hour": p.get("hour"),
        })

    # The headings within a section and the category headings are looked up the
    # same way by the page, so they travel in one table.
    groups = dict(TEXT.CATS)
    groups.update(I18N.GROUPS)

    # GROUP_DESC and DESCS are written against the heading and the prayer they
    # belong to, which reads better beside the English they replace. The page
    # has the English line itself in hand, so they are rekeyed to it here.
    group_descs = {}
    for phase, eng in PHASE_DESC.items():
        group_descs[eng] = TEXT.GROUP_DESC.get(PHASE_LABEL[phase], {})
    for label, eng in HEART_DESC.items():
        group_descs[eng] = TEXT.GROUP_DESC.get(label, {})
    descs = dict((eng, TEXT.DESCS.get(title, {}))
                 for title, eng in PRAYER_DESC.items())

    payload = {
        "v": 1,
        "langs": I18N.LANGS,
        "ui": I18N.UI,
        "groups": groups,
        "groupDescs": group_descs,
        "descs": descs,
        "notes": TEXT.NOTES,
        "sources": TEXT.SOURCES,
        "measure": I18N.MEASURE,
        "sections": [{"id": s, "title": t, "desc": d,
                      "tr": I18N.SECTIONS.get(s, {}),
                      "descTr": I18N.SECTION_DESC.get(s, {})}
                     for s, t, d, _ in SECTIONS],
        "prayers": out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

    counts = {}
    for p in out:
        counts[p["s"]] = counts.get(p["s"], 0) + 1
    print("wrote %s  (%.0f KB)" % (OUT.relative_to(ROOT), OUT.stat().st_size / 1024))
    for sid, title, _d, _c in SECTIONS:
        print("  %-14s %3d  %s" % (sid, counts.get(sid, 0), title))
    print("  %-14s %3d" % ("TOTAL", len(out)))

    # Anything a reader would still meet in English under another language's
    # name. Reported, not fatal: a new prayer should be publishable the day it
    # is added, with its descriptive matter following.
    langs = [x for x in I18N.LANGS if x != "en"]
    gaps = 0
    for label, keys, table in (
            ("category heading", {p["cat"] for p in out}, groups),
            ("heading within a section",
             {p["phaseLabel"] for p in out if p["phaseLabel"]}, groups),
            ("line under a heading",
             {p["phaseDesc"] for p in out if p["phaseDesc"]}, group_descs),
            ("prayer description",
             {p["desc"] for p in out if p["desc"]}, descs),
            ("note", {p["note"] for p in out if p["note"]}, TEXT.NOTES),
            ("source line", {p["src"] for p in out if p["src"]}, TEXT.SOURCES)):
        for k in sorted(keys):
            short = [x for x in langs if x not in table.get(k, {})]
            if short:
                gaps += 1
                print("  %s in English for %s: %s"
                      % (label, ",".join(short), k[:60]))
    if not gaps:
        print("  every heading, description, note and source line is carried "
              "in all %d languages" % len(I18N.LANGS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
