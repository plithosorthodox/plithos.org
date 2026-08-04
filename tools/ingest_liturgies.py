#!/usr/bin/env python3
"""
Add the Liturgy of St James and the Liturgy of St Mark.

The shelf has held one Liturgy, the Chrysostom, in five languages side by
side. These are the other two the Church has kept: the rite of Jerusalem,
served there and in the churches that received it on the twenty-third of
October, and the rite of Alexandria. They are not variants of the Byzantine
service but its elder relations, and a reader who has only ever heard one
Liturgy finds in them almost every part of it - the Trisagion, the kiss of
peace, the epiclesis, the Holy Things unto the holy - set in a different
order and in different words.

The third liturgy printed beside them in this volume is that of Adæus and
Maris, the East Syriac anaphora. It is not here: it belongs to the Church of
the East, which separated from the Orthodox Church at Ephesus, and the shelf
does not carry a rite the Church did not receive.

Structure is the edition's own numbering, walked in order. Reading it off a
pattern instead finds fifty-four sections in the fifty of St James, because
the Creed begins "I believe in one God" and a psalm begins "I will bless the
Lord"; a number is accepted only where the next one in sequence is due.

    python3 tools/ingest_liturgies.py --check
    python3 tools/ingest_liturgies.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_ephraim import page_text  # noqa: E402  (the same digitization)

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"

ANF_PUB = "Christian Literature Publishing Company, Buffalo"
COMMON = {
    "pub_year": 1886,
    "source": "Ante-Nicene Fathers, Vol. 7",
    "publisher": ANF_PUB,
    "source_class": "liturgical",
    "language": "en",
    "digitized": "Christian Classics Ethereal Library",
    "rights": "Public domain",
    "is_saint": True,
}

WORKS = [
    {
        "page": "anf07.xii.ii.html",
        "sections": 50,
        "phrases": ["Holy God, holy mighty, holy immortal",
                    "Hail, Mary, highly favoured",
                    "The holy things unto holy",
                    "I believe in one God, Father Almighty"],
        "work": {
            "work_id": "liturgy-of-st-james",
            "title": "The Divine Liturgy of James the Holy Apostle and "
                     "Brother of the Lord",
            "author": "St James the Brother of the Lord",
            "date": "4th-5th century",
            "translator": "William Macdonald",
            "saint": "Apostle James, the Brother of the Lord",
            "description": "The Liturgy of Jerusalem, served in the church "
                           "where the Church herself began and kept to this "
                           "day on the feast of St James. It is the fullest of "
                           "the ancient rites and the one the Byzantine "
                           "Liturgy grew from: the same Trisagion, the same "
                           "kiss of peace, the same calling down of the Spirit "
                           "upon the gifts, the same cry that the holy things "
                           "are for the holy, in older and longer words. The "
                           "great intercession names the Theotokos, the saints "
                           "and the departed by name, and the prayers of the "
                           "priest are given whole, including those he says "
                           "under his breath.",
        },
    },
    {
        "page": "anf07.xii.iii.html",
        "sections": 23,
        "phrases": ["Peace be to all",
                    "Lord, have mercy",
                    "I believe in one God",
                    "who by Thy might hast vanquished hell"],
        "work": {
            "work_id": "liturgy-of-st-mark",
            "title": "The Divine Liturgy of the Holy Apostle and Evangelist "
                     "Mark, The Disciple of the Holy Peter",
            "author": "St Mark the Evangelist",
            "date": "4th-5th century",
            "translator": "George Ross Merry",
            "saint": "Apostle and Evangelist Mark",
            "description": "The Liturgy of Alexandria, the church St Mark "
                           "founded, kept under his name as the rite of "
                           "Jerusalem is kept under St James's. Its order is "
                           "not the Byzantine one - the great intercession "
                           "comes before the anaphora rather than within it, "
                           "and the prayers for the rise of the Nile stand "
                           "where a northern rite asks for seasonable weather "
                           "- and it is the plainest evidence the shelf holds "
                           "that the Church's worship was one thing said "
                           "differently in different places.",
        },
    },
]

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman(n):
    out = ""
    for v, s in ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"),
                 (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += s
            n -= v
    return out


def sections(text, want):
    """[(citation, text)] for the numbered sections, walked in order.

    Each number is looked for only from where the previous one ended, and only
    the next one due is accepted. A pattern that takes any roman numeral at the
    head of a line also takes the Creed and two psalms.
    """
    marks, pos = [], 0
    for n in range(1, want + 1):
        num = roman(n)
        m = re.compile(r"(?m)^%s\.?\s+" % num).search(text, pos)
        if not m:
            return None, "section %s not found after section %s" % (num, roman(n - 1))
        marks.append((m.start(), m.end(), num))
        pos = m.end()
    out = []
    for i, (start, after, num) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out.append((num, text[after:stop].strip()))
    # What stands above the first number is the rubric that opens the service
    # - who is speaking, and where he is standing - with the running title of
    # the volume above it. The title is dropped and the rubric is kept.
    opening = [p.strip() for p in re.split(r"\n\s*\n", text[:marks[0][0]])
               if p.strip()]
    while opening and (opening[0].startswith("EARLY LITURGIES")
                       or "Divine Liturgy of" in opening[0]):
        opening.pop(0)
    if opening:
        out[0] = (out[0][0], "\n\n".join(opening) + "\n\n" + out[0][1])
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    built, failed = [], 0
    for entry in WORKS:
        meta = dict(COMMON, **entry["work"])
        wid = meta["work_id"]
        text = page_text(entry["page"])
        missing = [p for p in entry["phrases"] if p not in text]
        if missing:
            print("  FAIL  %-22s did not carry %r" % (wid, missing[0]))
            failed += 1
            continue
        got, err = sections(text, entry["sections"])
        if err:
            print("  FAIL  %-22s %s" % (wid, err))
            failed += 1
            continue
        units = []
        for n, (num, body) in enumerate(got, start=1):
            if len(body.split()) < 5:
                print("  FAIL  %-22s section %s is empty" % (wid, num))
                failed += 1
                units = []
                break
            units.append({
                "unit_id": "%s::u%02d" % (wid, n),
                "work_id": wid,
                "work_title": meta["title"],
                "author": meta["author"],
                "source_class": "liturgical",
                "ordinal": n,
                "citation_anchor": num,
                "text": body,
            })
        if not units:
            continue
        bad = sum(u["text"].count("�") for u in units)
        if bad:
            print("  FAIL  %-22s %d replacement characters" % (wid, bad))
            failed += 1
            continue
        words = sum(len(u["text"].split()) for u in units)
        print("  ok    %-22s %2d sections  %7s words"
              % (wid, len(units), format(words, ",")))
        built.append((meta, units))

    if failed:
        print("\n%d failed; nothing written" % failed)
        return 1

    if args.write:
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        for meta, units in built:
            OUTDIR.joinpath(meta["work_id"] + ".json").write_text(
                json.dumps({"work": meta, "units": units},
                           ensure_ascii=False, indent=1), encoding="utf-8")
            cat = [w for w in cat if w["work_id"] != meta["work_id"]]
            cat.append(meta)
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %d works" % len(built))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
