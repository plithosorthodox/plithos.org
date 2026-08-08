#!/usr/bin/env python3
"""
Add saints the Church venerates whose writings the Library already holds.

Two of the Fathers on the shelf had no life to link to, not because the
Church does not honour them but because the index was built from one
reckoning and they are commemorated in another. Both are commemorated in the
Prologue of Ohrid: Theophilus of Antioch on 6 December, Papias of Hierapolis
on 22 February. Neither appears on the calendar of the Orthodox Church in
America, which is where most of the index comes from.

Nothing here is composed. Every fact in these two lives is either from
Eusebius, whose Church History this site hosts and which is cited by book
and chapter below, or from the commemoration itself. Where the record is
silent the field is left empty: neither man has a settled iconographic type,
so neither is given one.

A saint has to be added in two places or he is half-present: the index on
saints.html, which holds the life, and the calendar in index.html,
which holds the day. This does both.

    python3 tools/add_saints.py --check
    python3 tools/add_saints.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAINTS_PAGE = ROOT / "saints.html"
CALENDAR = ROOT / "index.html"

THEOPHILUS_LIFE = (
    "Saint Theophilus, Bishop of Antioch, was the sixth to hold that see in "
    "succession from the apostles, following Hero, Cornelius and Eros, and he "
    "governed the church of Antioch for thirteen years in the latter half of "
    "the second century. He was schooled in Greek learning and came to the "
    "faith not by preaching but by reading: taking up the Holy Scriptures to "
    "refute them, he was overcome by them, and was baptized. What he had been "
    "given he spent his life giving back, and the Church remembers him chiefly "
    "as one of her first apologists, a bishop who answered the educated pagan "
    "in the pagan's own terms.\n\n"
    "His three books to Autolycus survive, addressed to a learned friend who "
    "had mocked the Christians and asked to be shown their God. Theophilus "
    "answers that God is seen by the eyes of the soul, and that a man whose "
    "soul is clouded by sin can no more see Him than a man with cataracts can "
    "see the sun; that the Scriptures of the Hebrews are older than the "
    "writings of the Greeks and truer; and that the resurrection is no stranger "
    "a thing than the seed that rots in the ground and rises. Eusebius records "
    "that he wrote also against the heresy of Hermogenes, drawing on the "
    "Apocalypse of John, and against Marcion, and that he left catechetical "
    "books besides; of these only the books to Autolycus have come down.\n\n"
    "He reposed about the year 181. The Church honours in Theophilus the "
    "apologist's particular courage, which is not the martyr's but is near it: "
    "to stand in front of the learning of the age and say that the faith has "
    "nothing to hide and will answer any question put to it honestly."
)

PAPIAS_LIFE = (
    "Saint Papias, Bishop of Hierapolis in Phrygia, belonged to the generation "
    "that stood next to the apostles and could still ask those who had heard "
    "them. Saint Irenaeus calls him an ancient man, a hearer of John and a "
    "companion of Polycarp of Smyrna; he was contemporary with the daughters of "
    "the Apostle Philip, who dwelt at Hierapolis, and he reports what he heard "
    "from them.\n\n"
    "He wrote five books, the Exposition of the Oracles of the Lord, and they "
    "are lost; what survives are the fragments other writers quoted, and they "
    "are among the most valuable few pages the early Church has left. Papias "
    "explains in his preface that he did not trust books as he trusted living "
    "witnesses, and that whenever he met anyone who had followed the elders he "
    "would ask what the elders had said; and it is from him that the Church has "
    "the earliest account of how two of the Gospels came to be written, that "
    "Mark, having become the interpreter of Peter, wrote down accurately, though "
    "not in order, whatsoever he remembered of the things said or done by Christ, "
    "being careful of one thing, not to omit any of the things which he had heard "
    "and not to state any of them falsely.\n\n"
    "The Church honours in Papias the witness who asked, and wrote down what he "
    "was told, and so handed on to every century after him the testimony of men "
    "who had known the men who had known the Lord."
)

NEW = [
    {
        "name": "Saint Theophilus, Bishop of Antioch",
        "feasts": ["12-06"],
        "type": "Hierarch",
        "great": False,
        "jur": [],
        "place": "Antioch, Syria",
        "origin": "",
        "region": "Syria",
        "sex": "male",
        "state": "Clergy",
        "rank": "Bishop",
        "bornYear": None,
        "reposedYear": 181,
        "century": 2,
        "glorifiedYear": None,
        "era": "Apostolic Age",
        "patronPlaces": ["Antioch"],
        "patronWork": ["apologists", "catechists", "those who teach the faith to unbelievers"],
        "patronCauses": [
            "those brought to faith by reading the Scriptures",
            "the answering of honest objections",
        ],
        "attributes": ["church-father"],
        "titles": ["Bishop of Antioch", "the Apologist"],
        "baptismalName": "",
        "relics": "",
        "icon": "",
        "canonizedBy": "Pre-congregational veneration",
        "feastRank": "Simple",
        "related": [
            "Hieromartyr Ignatius the God-Bearer, an earlier bishop of the same see (December 20)",
            "Saint Philogonius, Bishop of Antioch (December 20)",
        ],
        "life": THEOPHILUS_LIFE,
    },
    {
        "name": "Saint Papias, Bishop of Hierapolis",
        "feasts": ["02-22"],
        "type": "Hierarch",
        "great": False,
        "jur": [],
        "place": "Hierapolis, Phrygia",
        "origin": "",
        "region": "Asia Minor",
        "sex": "male",
        "state": "Clergy",
        "rank": "Bishop",
        "bornYear": None,
        "reposedYear": None,
        "century": 2,
        "glorifiedYear": None,
        "era": "Apostolic Age",
        "patronPlaces": ["Hierapolis"],
        "patronWork": ["those who gather testimony", "catechists"],
        "patronCauses": [
            "the handing on of what was received",
            "the memory of the eyewitnesses",
        ],
        "attributes": ["church-father"],
        "titles": ["Bishop of Hierapolis"],
        "baptismalName": "",
        "relics": "",
        "icon": "",
        "canonizedBy": "Pre-congregational veneration",
        "feastRank": "Simple",
        "related": [
            "Hieromartyr Polycarp, Bishop of Smyrna, his companion (February 23)",
            "Repose of the Holy Apostle and Evangelist John the Theologian, whose hearer he was (September 26)",
            "Holy, All-Praised Apostle Philip, who dwelt at Hierapolis (November 14)",
        ],
        "life": PAPIAS_LIFE,
    },
]

# The short entry the calendar shows beside the day, keyed by the same name.
INFO = {
    "Saint Theophilus, Bishop of Antioch": {
        "type": "Hierarch · 2nd c.",
        "life": "The sixth bishop of Antioch in succession from the apostles, who "
                "came to the faith by reading the Scriptures he had taken up to "
                "refute. His three books to Autolycus survive, answering a learned "
                "pagan friend who had asked to be shown the Christians' God. He "
                "governed Antioch thirteen years and reposed about the year 181.",
        "patron": "Invoked by apologists and catechists, and by those brought to "
                  "faith through reading.",
        "src": "The Prologue of Ohrid; Eusebius, Church History IV.20 and IV.24.",
    },
    "Saint Papias, Bishop of Hierapolis": {
        "type": "Hierarch · 2nd c.",
        "life": "Bishop of Hierapolis in Phrygia, called by Saint Irenaeus a hearer "
                "of John and a companion of Polycarp. His five books, the Exposition "
                "of the Oracles of the Lord, are lost but for the fragments others "
                "quoted, which preserve the earliest account the Church has of how "
                "the Gospels of Mark and Matthew came to be written.",
        "patron": "Invoked by those who gather and hand on testimony.",
        "src": "The Prologue of Ohrid; Eusebius, Church History III.36 and III.39.",
    },
}


def load_line(path, const):
    src = path.read_text(encoding="utf-8")
    i = src.index("const %s" % const)
    eq = src.index("=", i)
    j = src.index("\n", i)
    return src, i, eq, j


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    # --- the index that holds the life -------------------------------------
    ssrc, si, seq, sj = load_line(SAINTS_PAGE, "SAINTS=")
    saints = json.loads(ssrc[seq + 1:sj].rstrip().rstrip(";"))
    have = {s["name"] for s in saints}
    fields = set(saints[0])

    added = []
    for entry in NEW:
        extra = set(entry) - fields
        missing = fields - set(entry)
        if extra:
            print("%s: fields the index does not use: %s"
                  % (entry["name"], ", ".join(sorted(extra))))
            return 1
        if missing:
            print("%s: fields left unset: %s"
                  % (entry["name"], ", ".join(sorted(missing))))
            return 1
        if entry["name"] in have:
            print("already present: %s" % entry["name"])
            continue
        saints.append(entry)
        added.append(entry)

    saints.sort(key=lambda s: s["name"])

    # --- the calendar that holds the day -----------------------------------
    csrc = CALENDAR.read_text(encoding="utf-8")
    ci = csrc.index("const SAINT_INFO")
    ceq = csrc.index("=", ci)
    cj = csrc.index("\n", ci)
    info = json.loads(csrc[ceq + 1:cj].rstrip().rstrip(";"))
    for name, rec in INFO.items():
        info[name] = rec

    lines = csrc.split("\n")
    for entry in NEW:
        day = entry["feasts"][0]
        key = '"%s":[' % day
        hit = [k for k, l in enumerate(lines) if l.startswith(key)]
        if len(hit) != 1:
            print("the calendar has %d entries for %s" % (len(hit), day))
            return 1
        k = hit[0]
        if entry["name"] in lines[k]:
            continue
        lines[k] = lines[k].replace(
            "}],", '},{n:%s}],' % json.dumps(entry["name"], ensure_ascii=False), 1) \
            if lines[k].endswith("}],") else lines[k]
        if entry["name"] not in lines[k]:
            print("could not place %s on %s" % (entry["name"], day))
            return 1

    print("%d saints in the index (%d added)" % (len(saints), len(added)))
    for e in added:
        print("   %s  %s" % (e["feasts"][0], e["name"]))

    if args.write:
        line = "const SAINTS=" + json.dumps(saints, ensure_ascii=False,
                                            separators=(",", ":")) + ";"
        SAINTS_PAGE.write_text(ssrc[:si] + line + ssrc[sj:], encoding="utf-8")

        csrc2 = "\n".join(lines)
        ci = csrc2.index("const SAINT_INFO")
        ceq = csrc2.index("=", ci)
        cj = csrc2.index("\n", ci)
        iline = "const SAINT_INFO=" + json.dumps(info, ensure_ascii=False) + ";"
        CALENDAR.write_text(csrc2[:ci] + iline + csrc2[cj:], encoding="utf-8")
        print("\nwrote saints.html and index.html")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
