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
