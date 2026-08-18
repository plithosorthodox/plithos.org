#!/usr/bin/env python3
"""
Add works that New Advent serves one page to a section.

ingest_batch.py handles a whole treatise on a single page. This handles the
other layout: an index that links to a page per discourse, per letter, per
book. It is the shape ingest_irenaeus.py was written for, generalised, so the
next such work does not need a third script.

The page list is read off the index rather than assembled from a guessed
range, and every entry declares what the index is expected to yield. Where a
source carries less than the complete work, the entry says so in a number and
the description says so in words: a reader is entitled to know that the
edition stops somewhere, and 325 letters presented as "the letters" is a
quiet lie.

    python3 tools/ingest_pages.py --check
    python3 tools/ingest_pages.py --write --only methodius-banquet
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest import clean_text, strip_scripture_refs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-pages")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
ANF_PUB = "Christian Literature Publishing Company, Buffalo"

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]


def methodius_anchor(n, stem):
    """Page 062300 is the introduction; 062301 onward are the discourses."""
    k = int(stem[-2:])
    return ("The Banquet of the Ten Virgins, Introduction" if k == 0
            else "The Banquet of the Ten Virgins, Discourse %s" % ROMAN[k])


def basil_anchor(n, stem):
    return "Letter %d" % int(stem[-3:])



def chrysostom_anchor(word="Homily"):
    """New Advent numbers these two ways - 230101 for a long series, 23051 for
    a short one - so the unit is whatever follows the four digits of the
    series. Several open with the Argument, which the edition numbers zero."""
    def anchor(n, stem):
        k = int(stem[4:])
        return "Argument" if k == 0 else "%s %d" % (word, k)
    return anchor


CATALOGUE = [
    {
        "work_id": "methodius-banquet",
        "index": "https://www.newadvent.org/fathers/0623.htm",
        "pattern": r'href="[^"]*?(0623\d\d)\.htm"',
        "pages": 12,
        "anchor": methodius_anchor,
        "work": {
            "title": "The Banquet of the Ten Virgins",
            "author": "St Methodius of Olympus",
            "date": "c. 290",
            "translator": "William R. Clark",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 6",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "Ten virgins in a garden, each giving a discourse in "
                           "praise of chastity, in deliberate imitation of Plato's "
                           "Symposium and in answer to it. The earliest sustained "
                           "Christian treatment of virginity, written by the bishop "
                           "who was the first to answer Origen at length.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Hieromartyr Methodius, Bishop of Patara",
            "is_saint": True,
        },
    },
    {
        "work_id": "basil-letters",
        "index": "https://www.newadvent.org/fathers/3202.htm",
        "pattern": r'href="[^"]*?(3202\d{3})\.htm"[^>]*>\s*(?:<[^>]*>\s*)?Letter\s+\d+',
        "pages": 325,
        "anchor": basil_anchor,
        "running_head": "ST. BASIL OF CAESAREA",
        "work": {
            "title": "The Letters",
            "author": "St Basil the Great",
            "date": "357-378",
            "translator": "Blomfield Jackson",
            "pub_year": 1895,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 8",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "Twenty years of a bishop's correspondence: consolation "
                           "to the bereaved, rebuke to the powerful, instruction to "
                           "his clergy, and the canonical letters to Amphilochius "
                           "that the Church later received as canon law. Among them "
                           "are the letters written while the Arian party held the "
                           "East and Basil held Caesarea almost alone. This edition "
                           "carries 325 of the 366 letters it numbers; most of those "
                           "it does not print fall among the ones it marks as of "
                           "doubtful authorship.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Saint Basil the Great, Archbishop of Caesarea in Cappadocia",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-acts",
        "index": "https://www.newadvent.org/fathers/2101.htm",
        "pattern": r'href="[^"]*?(2101\d{2})\.htm"',
        "pages": 55,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on the Acts of the Apostles",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 400",
            "translator": "J. Walker, J. Sheppard and H. Browne, revised by George B. Stevens",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 11",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Fifty-five homilies preached at Constantinople on the acts of the Apostles, and the only commentary on that book to come down whole from the early Church in Greek. Chrysostom takes the young Church house by house and city by city, and turns almost every chapter to the manner of life it asks of those who read it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-1corinthians",
        "index": "https://www.newadvent.org/fathers/2201.htm",
        "pattern": r'href="[^"]*?(2201\d{2})\.htm"',
        "pages": 45,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on First Corinthians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 392",
            "translator": "Talbot W. Chambers",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 12",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Forty-four homilies on the letter written to a church divided against itself, opened for a congregation that knew the same divisions. The chapters on the Eucharist, on love, and on the resurrection of the body are among the most quoted of all his preaching. The Argument stands first, as the edition prints it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-2corinthians",
        "index": "https://www.newadvent.org/fathers/2202.htm",
        "pattern": r'href="[^"]*?(2202\d{2})\.htm"',
        "pages": 30,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Second Corinthians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 392",
            "translator": "Talbot W. Chambers",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 12",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Thirty homilies on the most personal of the Apostle's letters, in which Paul defends his own ministry and boasts only of his weakness. Chrysostom, who would himself be driven from his see twice, reads it as a bishop reading a bishop.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-ephesians",
        "index": "https://www.newadvent.org/fathers/2301.htm",
        "pattern": r'href="[^"]*?(2301\d{2})\.htm"',
        "pages": 25,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Ephesians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 393",
            "translator": "Gross Alexander",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Twenty-four homilies on the letter of the one Body and the one Head, carrying his long treatment of marriage as the image of Christ and the Church, and of the armour of God. The Argument stands first, as the edition prints it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-philippians",
        "index": "https://www.newadvent.org/fathers/2302.htm",
        "pattern": r'href="[^"]*?(2302\d{2})\.htm"',
        "pages": 16,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Philippians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 400",
            "translator": "John A. Broadus",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Fifteen homilies on the letter of joy written from a prison, including the hymn of Christ's self-emptying, which Chrysostom expounds against those who would make the Son less than the Father. The Argument stands first, as the edition prints it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-colossians",
        "index": "https://www.newadvent.org/fathers/2303.htm",
        "pattern": r'href="[^"]*?(2303\d{2})\.htm"',
        "pages": 12,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Colossians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 399",
            "translator": "John A. Broadus",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Twelve homilies on the fulness of Christ, in whom all things hold together, preached against a piety that would put angels and observances between God and man.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-1thessalonians",
        "index": "https://www.newadvent.org/fathers/2304.htm",
        "pattern": r'href="[^"]*?(2304\d{2})\.htm"',
        "pages": 11,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on First Thessalonians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 400",
            "translator": "John A. Broadus",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Eleven homilies on the earliest of the Apostle's letters, on the dead who sleep in Christ and the day that comes as a thief, and on the quiet labour asked of those who wait for it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-2thessalonians",
        "index": "https://www.newadvent.org/fathers/2305.htm",
        "pattern": r'href="[^"]*?(2305\d)\.htm"',
        "pages": 5,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Second Thessalonians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 400",
            "translator": "John A. Broadus",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Five homilies on the letter written to a church shaken by the report that the day of the Lord had already come, and on the man of sin who must be revealed before it does.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-1timothy",
        "index": "https://www.newadvent.org/fathers/2306.htm",
        "pattern": r'href="[^"]*?(2306\d{2})\.htm"',
        "pages": 19,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on First Timothy",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 397",
            "translator": "Philip Schaff",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Eighteen homilies on the ordering of the Church: what is asked of a bishop, of a deacon, of a widow, and of the rich. The Argument stands first, as the edition prints it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-2timothy",
        "index": "https://www.newadvent.org/fathers/2307.htm",
        "pattern": r'href="[^"]*?(2307\d{2})\.htm"',
        "pages": 10,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Second Timothy",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 397",
            "translator": "Philip Schaff",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Ten homilies on the last letter the Apostle wrote, from a second imprisonment and in view of his death, charging a young bishop to keep what was entrusted to him.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-titus",
        "index": "https://www.newadvent.org/fathers/2308.htm",
        "pattern": r'href="[^"]*?(2308\d)\.htm"',
        "pages": 6,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Titus",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 397",
            "translator": "Philip Schaff",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Six homilies on the letter to a bishop left in Crete to set in order what remained, and on the grace that teaches men to live soberly in the present age.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-homilies-philemon",
        "index": "https://www.newadvent.org/fathers/2309.htm",
        "pattern": r'href="[^"]*?(2309\d)\.htm"',
        "pages": 4,
        "anchor": chrysostom_anchor(),
        "work": {
            "title": "Homilies on Philemon",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 397",
            "translator": "Philip Schaff",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Three homilies on the shortest of the Apostle's letters, sent back with a runaway slave. Chrysostom opens by answering those who thought so small a letter unworthy of Scripture. The Argument stands first, as the edition prints it.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
    {
        "work_id": "chrysostom-commentary-galatians",
        "index": "https://www.newadvent.org/fathers/2310.htm",
        "pattern": r'href="[^"]*?(2310\d)\.htm"',
        "pages": 6,
        "anchor": chrysostom_anchor("Chapter"),
        "work": {
            "title": "Commentary on Galatians",
            "author": "St John Chrysostom",
            "language": "en",
            "date": "c. 395",
            "translator": "Gross Alexander",
            "pub_year": 1889,
            "source": "Nicene and Post-Nicene Fathers, Series 1, Vol. 13",
            "publisher": "Christian Literature Publishing Co., Buffalo",
            "source_class": "patristic",
            "description": "Not homilies but a continuous commentary, the only one of its kind to survive from him, following the letter chapter by chapter through the quarrel over the law and the freedom for which Christ has set us free.",
            "digitized": "New Advent",
            "license": "Public Domain",
            "saint": "Repose of Saint John Chrysostom, Archbishop of Constantinople",
            "is_saint": True,
        },
    },
]


def fetch(url, name, delay=1.1):
    p = CACHE / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


def page_body(body, running_head=None):
    m = re.search(r"<h1[^>]*>(.*?)</h1>(.*?)(?=<h2[^>]*>\s*About this page|\Z)",
                  body, re.S | re.I)
    if not m:
        raise ValueError("page shape not recognised")
    head = clean_text(m.group(1))
    trunk = re.sub(r"<em>.*?Please help support the mission.*?</em>", "",
                   m.group(2), flags=re.S | re.I)
    text = strip_scripture_refs(clean_text(trunk))
    # Where the source repeats the author as a running head above every page,
    # it lands as the opening line of each unit: 325 letters each beginning
    # "ST. BASIL OF CAESAREA". That is furniture, not text.
    if running_head:
        text = re.sub(r"\A\s*%s\s*\n+" % re.escape(running_head), "", text,
                      flags=re.I)
    return head, text


def build(entry):
    idx = fetch(entry["index"], entry["work_id"] + "-index.htm")
    stems = sorted(set(re.findall(entry["pattern"], idx)))
    if len(stems) != entry["pages"]:
        return None, ("the index yields %d pages, %d expected"
                      % (len(stems), entry["pages"]))

    wid = entry["work_id"]
    units = []
    for n, stem in enumerate(stems, start=1):
        head, text = page_body(fetch("https://www.newadvent.org/fathers/%s.htm" % stem,
                                     "%s-%s.htm" % (wid, stem)),
                               entry.get("running_head"))
        if not text.strip():
            return None, "page %s is empty" % stem
        units.append({
            "unit_id": "%s::u%03d" % (wid, n),
            "work_id": wid,
            "work_title": entry["work"]["title"],
            "author": entry["work"]["author"],
            "source_class": entry["work"]["source_class"],
            "ordinal": n,
            "citation_anchor": entry["anchor"](n, stem),
            "chapter_title": head,
            "text": text,
        })
        if n % 75 == 0:
            print("        ... %d pages" % n)
    return units, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    todo = [e for e in CATALOGUE if not args.only or e["work_id"] == args.only]
    built, failed = [], []
    for entry in todo:
        print("  %s ..." % entry["work_id"])
        units, err = build(entry)
        if err:
            failed.append((entry["work_id"], err))
            print("  FAIL  %-24s %s" % (entry["work_id"], err))
            continue
        words = sum(len(u["text"].split()) for u in units)
        bad = sum(len(re.findall(r"[–—‘’“”]", u["text"])) for u in units)
        print("  ok    %-24s %4d units  %9s words  %d dashes/smart quotes"
              % (entry["work_id"], len(units), format(words, ","), bad))
        built.append((entry, units))

    if failed:
        print("\n%d of %d failed; nothing written" % (len(failed), len(todo)))
        return 1

    if args.write:
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        for entry, units in built:
            meta = dict(entry["work"], work_id=entry["work_id"])
            OUTDIR.joinpath(entry["work_id"] + ".json").write_text(
                json.dumps({"work": meta, "units": units},
                           ensure_ascii=False, indent=1), encoding="utf-8")
            cat = [w for w in cat if w["work_id"] != entry["work_id"]]
            cat.append(meta)
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %d works and updated the catalogue" % len(built))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
