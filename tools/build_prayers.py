#!/usr/bin/env python3
"""
Emit data/prayers.v1.json from the PRAYERS array embedded in index.html, and
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

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "prayers.v1.json"

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
    "preparation": "Ten prayers by St Basil the Great, St John Chrysostom, "
                   "St John of Damascus, St Symeon Metaphrastes and St Symeon "
                   "the New Theologian. Prayer books print them as one "
                   "continuous order, kept on the evening before receiving or "
                   "on the morning itself, according to local custom. How much "
                   "of it is said is set by one's spiritual father.",
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
            "cat": p["cat"],
            "title": p.get("title", ""),
            "body": p.get("body", ""),
            "note": p.get("note", ""),
            "src": p.get("src", ""),
            "hour": p.get("hour"),
        })

    payload = {
        "v": 1,
        "sections": [{"id": s, "title": t, "desc": d} for s, t, d, _ in SECTIONS],
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
