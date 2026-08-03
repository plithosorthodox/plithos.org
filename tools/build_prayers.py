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
    ("heart", "The Jesus Prayer",
     "The prayer of the heart, and the fathers' counsel on keeping it.",
     ["Prayers of the Heart"]),
    ("communion", "Holy Communion",
     "Preparation before the Mysteries, and thanksgiving after.",
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
COMMUNION_PHASE = {
    "I Believe, O Lord, and I Confess": "at-the-chalice",
    "Of Thy Mystical Supper": "at-the-chalice",
}
PHASE_LABEL = {
    "preparation": "The Order of Preparation",
    "at-the-chalice": "Immediately before receiving",
    "thanksgiving": "After receiving",
}


def communion_phase(p):
    if p.get("cat") == "Thanksgiving After Holy Communion":
        return "thanksgiving"
    return COMMUNION_PHASE.get(p.get("title"), "preparation")


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
            "phaseLabel": PHASE_LABEL.get(phase) if phase else None,
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
