#!/usr/bin/env python3
"""
Add Aphrahat the Persian Sage.

The earliest Syriac father whose work survives whole, writing in the Persian
empire in the years Shapur's persecution was falling on the Church there, and
outside the Greek world entirely: he argues from Scripture and from the Syriac
tradition, and quotes no philosopher. What he describes - the fast, the vigil,
the covenant of the ascetics, the prayers of the Church for her dead - is a
Christianity that had not passed through Athens.

The volume is the one St Ephraim came from, and the helpers are his. Only
eight of the twenty-three Demonstrations are printed here, with the Letter
that prompted them; the edition names those eight on its own title page, by
their numbers in the whole series, and this asserts that list rather than
whatever the contents happens to hold.

He is not given the title of a saint. The Orthodox Church commemorates a
Persian named Aphraates on the twenty-ninth of January, and he is a different
man - the hermit of Antioch whom Theodoret knew as a boy and who died some
sixty years after the Sage. The two are constantly run together, and the
reception note in tools/reception.py says so.

    python3 tools/ingest_aphrahat.py --check
    python3 tools/ingest_aphrahat.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_ephraim import contents, page_text  # noqa: E402  (same volume)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "library" / "aphrahat-select-demonstrations.json"
INDEX = ROOT / "data" / "library" / "works-index.json"

WORK = {
    "work_id": "aphrahat-select-demonstrations",
    "title": "Select Demonstrations",
    "author": "Aphrahat the Persian Sage",
    "date": "c. 337-345",
    "translator": "John Gwynn",
    "pub_year": 1898,
    "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 13",
    "publisher": "Christian Literature Company, New York",
    "source_class": "patristic",
    "language": "en",
    "description": "Written in the Persian empire while Shapur's persecution "
                   "was falling on the Church there, and the earliest Syriac "
                   "prose the Church has whole. Aphrahat answers an inquirer "
                   "point by point on faith, on the monastic life, on the "
                   "resurrection, on the office of a pastor, on Christ the Son "
                   "of God, and on persecution and death, arguing throughout "
                   "from Scripture and from the practice of his own churches "
                   "and citing no philosopher at all. This edition prints "
                   "eight of the twenty-three Demonstrations, keeping their "
                   "numbers in the whole series, together with the letter that "
                   "prompted them.",
    "digitized": "Christian Classics Ethereal Library",
    "rights": "Public domain",
    "saint": None,
    "is_saint": False,
}

# The edition's own title page names which eight it prints, and their numbers
# in the series of twenty-three. Taken from there rather than from the list of
# pages, so that a page which went missing cannot pass as a complete selection.
EXPECTED = [
    "Letter of an Inquirer",
    "Demonstration I.-Of Faith",
    "Demonstration V.-Of Wars",
    "Demonstration VI.-Of Monks",
    "Demonstration VIII.-Of the Resurrection of the Dead",
    "Demonstration X.-Of Pastors",
    "Demonstration XVII.-Of Christ the Son of God",
    "Demonstration XXI.-Of Persecution",
    "Demonstration XXII.-Of Death and the Latter Times",
]


def flat(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def piece(name):
    """(heading, text) for one page, headed as the edition heads it.

    The heading comes off the page and not off the contents, which drops the
    number: the contents calls the eighth Demonstration "Of the Resurrection
    of the Dead", and a reader who cannot see that it is the eighth of
    twenty-three cannot tell what is missing around it.
    """
    lines = [x for x in page_text(name).split("\n")]
    heading, start = None, 0
    for i, line in enumerate(lines[:8]):
        if not line.strip():
            continue
        # Front matter: the author's name and the printer's rule above the
        # first page of the set, and the running title above each Demonstration.
        if re.fullmatch(r"-{4,}|Aphrahat\.?|The \"Demonstrations\" of Aphrahat\.",
                        line.strip()):
            continue
        heading, start = line.strip().rstrip("."), i + 1
        break
    return heading, "\n".join(lines[start:]).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    pages = contents("npnf213.ix") or contents("npnf213.iii.ix")
    if len(pages) != len(EXPECTED):
        print("%d pieces, %d expected" % (len(pages), len(EXPECTED)))
        return 1

    units = []
    for n, ((name, _), want) in enumerate(zip(pages, EXPECTED), start=1):
        heading, text = piece(name)
        if not heading or flat(heading) != flat(want):
            print("piece %d is headed %r; the edition names %r"
                  % (n, heading, want))
            return 1
        # The inquirer's letter is three hundred words; every Demonstration
        # runs to thousands, so this only catches a page that came down empty.
        if len(text.split()) < 250:
            print("%s came out with %d words" % (heading, len(text.split())))
            return 1
        units.append({
            "unit_id": "%s::u%02d" % (WORK["work_id"], n),
            "work_id": WORK["work_id"],
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": "patristic",
            "ordinal": n,
            "citation_anchor": heading,
            "text": text,
        })

    bad = sum(u["text"].count("�") for u in units)
    if bad:
        print("%d replacement characters: the pages did not decode" % bad)
        return 1

    words = sum(len(u["text"].split()) for u in units)
    print("%d pieces, %s words" % (len(units), format(words, ",")))
    for u in units:
        print("   %-52s %6s words" % (u["citation_anchor"],
                                      format(len(u["text"].split()), ",")))

    if args.write:
        OUT.write_text(json.dumps({"work": WORK, "units": units},
                                  ensure_ascii=False, indent=1),
                       encoding="utf-8")
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        cat = [w for w in cat if w["work_id"] != WORK["work_id"]]
        cat.append(dict(WORK))
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %s" % OUT.relative_to(ROOT))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
