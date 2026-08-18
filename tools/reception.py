#!/usr/bin/env python3
"""
Say plainly how the Church received a work, where that is a question.

Most of the shelf needs no such note. Athanasius on the Incarnation is
simply Athanasius on the Incarnation. But a handful of books are here for
what they preserve rather than for what they teach, and one of them is the
book the Church answered. A reader who opens On First Principles without
knowing that ought to be told, in the entry, not left to find out.

The rule this encodes, which governs additions as much as it does what is
already here: a work belongs on the shelf if the Church received it, and a
work written after its author left the Church does not. Tatian's Address
was written while he was still in her; the Encratite writings of his later
years are not here and will not be. Clement's Instructor and Stromateis are
here; the Hypotyposes, on which the censure of Photius fell, is lost, and
would not be here if it were not.

Every note below states a fact of the record: a council, a censure, a date.
None of them argues, and none of them softens.

    python3 tools/reception.py --check
    python3 tools/reception.py --write
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "library.html"
INDEX = ROOT / "data" / "library" / "works-index.json"

# The whole Corpus Areopagiticum carries the same note, so it is written
# once. Five copies of a paragraph drift apart the first time one is edited.
AREOPAGITE = (
    "These writings were transmitted under the name of the Dionysius whom "
    "the Apostle Paul converted at Athens, and they are not his: they "
    "show a liturgy and a vocabulary of about the year 500. The Church "
    "received the writings and read them as her own, and St Maximus the "
    "Confessor wrote on them; she never received a claim about whose "
    "hand held the pen. They are kept under the name the manuscripts "
    "carry, and the date given is the date they were written."
)

CAUTIONS = {
    "passion-of-perpetua":
        "The Church honours these martyrs and has kept their day since the "
        "third century; Perpetua, Felicity and their companions stand in the "
        "calendar on the first of February. The text itself carries the marks "
        "of the Montanists, who claimed it: the framing preface speaks in "
        "their manner of new prophecy, and Tertullian, who had gone over to "
        "them, is often supposed to have edited it. What Perpetua wrote in "
        "prison is her own and is why the book is here. The frame around it "
        "is the reason the note is here.",

    "dionysius-divine-names": AREOPAGITE,
    "dionysius-mystic-theology": AREOPAGITE,
    "dionysius-heavenly-hierarchy": AREOPAGITE,
    "dionysius-ecclesiastical-hierarchy": AREOPAGITE,
    "dionysius-letters": AREOPAGITE,

    "liturgy-of-st-james":
        "The Church has served this Liturgy in Jerusalem from antiquity and "
        "keeps it still on the feast of St James, and she has never taught "
        "that the Apostle wrote out the text that carries his name. It grew "
        "in the church he governed and is called by his, as a rite is called "
        "by the see that serves it. What St Cyril of Jerusalem describes to "
        "his catechumens in the fourth century is recognisably this service; "
        "the manuscripts that preserve it are later, and it is given here as "
        "they have it.",

    "liturgy-of-st-mark":
        "The rite of Alexandria, kept under the name of the Evangelist who "
        "founded that church, on the same footing as the Liturgy of St James "
        "is kept under his: the Church received the service, not a claim "
        "about whose hand wrote it down. It is not in use in the Orthodox "
        "Church today, and is here as the worship of Alexandria in the "
        "centuries when it was.",

    "aphrahat-select-demonstrations":
        "Aphrahat is not given the title of a saint here. The Orthodox Church "
        "commemorates a Persian named Aphraates on the twenty-ninth of "
        "January, and he is another man: the hermit of Antioch whom Theodoret "
        "met as a boy and who died some sixty years after the Sage. The two "
        "are constantly taken for one. Nothing Aphrahat wrote was ever "
        "censured, and no council names him; he wrote a century before "
        "Ephesus, in a church that had not yet been divided by the "
        "controversies the Greek world was about to have. His eighth "
        "Demonstration teaches that the soul sleeps in the grave until the "
        "resurrection, which is not what the Church holds, and what she holds "
        "is said in her own prayers for the departed.",

    "origen-de-principiis":
        "Origen is named among the condemned at the Fifth Ecumenical Council, "
        "and the speculations this book is best known for, the pre-existence "
        "of souls and a final restoration of all things, are among the "
        "teachings the Church rejected. It is kept here as a document of the "
        "third century and as the book the Church later answered, not as a "
        "statement of the faith. Read it knowing what she decided.",

    "clement-instructor":
        "The Orthodox Church does not commemorate Clement of Alexandria, and "
        "he is not given the title of a saint here. The censure of Photius "
        "fell on his Hypotyposes, a book now lost and not among those kept "
        "here; of the Instructor he wrote favourably. Read as a witness to "
        "the Alexandria of about the year 200, not as a rule of faith.",

    "clement-stromata":
        "The Orthodox Church does not commemorate Clement of Alexandria, and "
        "he is not given the title of a saint here. The censure of Photius "
        "fell on his Hypotyposes, a book now lost and not among those kept "
        "here. The Stromateis reasons freely with Greek philosophy and was "
        "never a rule of faith; read it as the exploration it is.",

    "tatian-address-greeks":
        "Tatian wrote this while he was still in the Church, about the year "
        "170. After the martyrdom of his teacher Justin he left her and led "
        "the Encratites, who condemned marriage and the eating of flesh. "
        "Nothing he wrote afterwards is kept here.",

    "eusebius-church-history":
        "Eusebius was provisionally excommunicated at Antioch in 325 for "
        "Arian sympathies and cleared at Nicaea the same year, and the "
        "Seventh Ecumenical Council named him an Arian. He is read here as "
        "the Church's first historian, for the documents and the accounts of "
        "the martyrs that he alone preserved, and not as a teacher of "
        "doctrine.",

    "shepherd-of-hermas":
        "The Shepherd was read aloud in some churches in the early centuries "
        "and is quoted by the Fathers, but it is not among the canonical "
        "Scriptures and was not received as such.",

    "second-clement":
        "This homily was copied and read beside the letter of Clement of Rome "
        "and came to be called his second epistle. It is neither his nor a "
        "letter, and it is not among the canonical Scriptures. It is kept here "
        "as what it is, the oldest surviving sermon preached to a Christian "
        "congregation.",

    "epistle-of-barnabas":
        "This letter was read in some churches in the early centuries and "
        "stands in the Codex Sinaiticus after the New Testament, but it is "
        "not among the canonical Scriptures and was not received as such.",
}


# A description should say what a book is. The warning belongs in the note,
# where it is labelled and cannot be mistaken for part of the summary.
DESCRIPTIONS = {
    "origen-de-principiis":
        "The first systematic treatment of Christian doctrine, treating God, "
        "the rational creation, the world, free will, and Scripture.",
}


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

    allw = corpus["works"] + lazy
    by = {w["work_id"]: w for w in allw}

    missing = [wid for wid in CAUTIONS if wid not in by]
    for wid in missing:
        print("no work on the shelf called %s" % wid)

    changed = 0
    for w in allw:
        desc = DESCRIPTIONS.get(w["work_id"])
        if desc and w.get("description") != desc:
            w["description"] = desc
            changed += 1
        want = CAUTIONS.get(w["work_id"])
        if want:
            if w.get("caution") != want:
                w["caution"] = want
                changed += 1
        elif "caution" in w:
            del w["caution"]
            changed += 1

    print("%d works, %d carry a note (%d changed)"
          % (len(allw), sum(1 for w in allw if w.get("caution")), changed))
    for w in allw:
        if w.get("caution"):
            print("   %-30s %s" % (w["work_id"], w["title"][:44]))

    if args.write:
        line = "const CORPUS = " + json.dumps(corpus, ensure_ascii=False,
                                              separators=(",", ":")) + ";"
        READER.write_text(src[:i] + line + src[j:], encoding="utf-8")
        INDEX.write_text(json.dumps(lazy, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote library.html and works-index.json")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
