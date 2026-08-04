#!/usr/bin/env python3
"""
Add Against Heresies to the Library.

The shelf ran from Clement of Rome to John of Damascus without the one book
that stands between them on almost every question a reader arrives with.
Against Heresies, written about 180, is the earliest sustained statement of
what the Church holds as against what merely calls itself Christian: that the
faith is what the apostles handed down and the churches they founded still
teach, that this can be traced bishop by bishop, that the Eucharist is the
Body and Blood and not a figure, that the Son became what we are to make us
what He is. Ask when any of those was first written down at length and the
answer is this book, and it was not here.

Irenaeus is a saint of the Church, Hieromartyr Irenaeus of Lyons, and is
already in the Saints index at 23 August, so the work links to a life the
site already holds.

The source is New Advent's edition of the Ante-Nicene Fathers translation by
Alexander Roberts and William Rambaut, published 1885, public domain. One
page per chapter, 168 of them.

The structure is read off the table of contents rather than assembled from a
guessed range. ingest_canons.py hand-listed its sections once and dropped
seven councils in silence; the chapter counts per book are known numbers, so
this checks them and refuses to write if they disagree.

    python3 tools/ingest_irenaeus.py --check    # fetch and report, write nothing
    python3 tools/ingest_irenaeus.py --write
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
OUT = ROOT / "data" / "library" / "irenaeus-against-heresies.json"
INDEX = ROOT / "data" / "library" / "works-index.json"
CACHE = Path("/tmp/plithos-irenaeus")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
TOC = "https://www.newadvent.org/fathers/0103.htm"

# Ante-Nicene Fathers, Vol. 1. If the table of contents yields anything else,
# something has moved and the run stops rather than publishing a book with a
# hole in it.
EXPECTED = {1: 31, 2: 35, 3: 25, 4: 41, 5: 36}

ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}

WORK = {
    "work_id": "irenaeus-against-heresies",
    "title": "Against Heresies",
    "author": "St Irenaeus of Lyons",
    "date": "c. 180",
    "translator": "Alexander Roberts and William Rambaut",
    "pub_year": 1885,
    "source": "Ante-Nicene Fathers, Vol. 1",
    "publisher": "Christian Literature Publishing Company, Buffalo",
    "source_class": "patristic",
    "description": "Written against the Gnostic teachers of the second century, "
                   "and in the course of refuting them the earliest full account "
                   "of what the Church holds and how she knows it: the faith "
                   "received from the apostles, kept by the churches they "
                   "founded, and traceable through the bishops they appointed. "
                   "Irenaeus heard Polycarp, who had heard the Apostle John.",
    "digitized": "New Advent",
    "rights": "Public domain",
    "saint": "Hieromartyr Irenaeus, Bishop of Lyons",
    "is_saint": True,
}


def fetch(url, name, delay=1.2):
    p = CACHE / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


def toc_chapters():
    """[(book, chapter, url)] read off the table of contents."""
    body = fetch(TOC, "toc.htm")
    found = {}
    for m in re.finditer(r'href="[^"]*?(0103(\d)(\d\d))\.htm"', body, re.I):
        stem, book, chap = m.group(1), int(m.group(2)), int(m.group(3))
        if book in EXPECTED:
            found[(book, chap)] = "https://www.newadvent.org/fathers/%s.htm" % stem
    return found


def chapter_text(body):
    """New Advent puts the chapter title in <h1> and the body after it."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>(.*?)(?=<h2[^>]*>\s*About this page|\Z)",
                  body, re.S | re.I)
    if not m:
        raise ValueError("page shape not recognised")
    head = clean_text(m.group(1))
    trunk = re.sub(r"<em>.*?Please help support the mission.*?</em>", "",
                   m.group(2), flags=re.S | re.I)
    # The per-chapter argument sits in the first <p> as a bold summary; keep it.
    return head, strip_scripture_refs(clean_text(trunk))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    found = toc_chapters()
    # Chapter 0 is the book's preface, which is text and not front matter:
    # the sentence Irenaeus is most quoted for stands in the preface to Book V.
    # It is carried, but the counts checked below are of chapters.
    counts = {}
    for (b, c) in found:
        if c:
            counts[b] = counts.get(b, 0) + 1
    print("chapters found in the table of contents:")
    bad = False
    for b in sorted(EXPECTED):
        got, want = counts.get(b, 0), EXPECTED[b]
        flag = "" if got == want else "   <-- expected %d" % want
        if got != want:
            bad = True
        print("   Book %-4s %3d%s" % (ROMAN[b], got, flag))
    if bad:
        print("\nthe table of contents does not match the known chapter counts; "
              "stopping rather than publishing a book with a hole in it")
        return 1

    units = []
    n = 0
    for (b, c) in sorted(found):
        body = fetch(found[(b, c)], "%d-%02d.htm" % (b, c))
        head, text = chapter_text(body)
        if not text.strip():
            print("empty chapter: Book %s, %d" % (ROMAN[b], c))
            return 1
        n += 1
        units.append({
            "unit_id": "irenaeus-against-heresies::u%03d" % n,
            "work_id": WORK["work_id"],
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": WORK["source_class"],
            "ordinal": n,
            "citation_anchor": ("Against Heresies, Book %s, Preface" % ROMAN[b]
                                if c == 0 else
                                "Against Heresies, Book %s, Chapter %d" % (ROMAN[b], c)),
            "chapter_title": head,
            "text": text,
        })
        if n % 40 == 0:
            print("   ... %d chapters" % n)

    words = sum(len(u["text"].split()) for u in units)
    dashes = sum(len(re.findall(r"[–—]", u["text"])) for u in units)
    smart = sum(len(re.findall(r"[‘’“”]", u["text"])) for u in units)
    prefaces = sum(1 for u in units if u["citation_anchor"].endswith("Preface"))
    print("\n%d units (%d chapters and %d prefaces), %s words"
          % (len(units), len(units) - prefaces, prefaces, format(words, ",")))
    print("house text rules: %d dashes, %d smart quotes remaining" % (dashes, smart))

    if args.write:
        OUT.write_text(json.dumps({"work": WORK, "units": units},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        cat = [w for w in cat if w["work_id"] != WORK["work_id"]]
        cat.append(dict(WORK))
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %s and added it to the catalogue"
              % OUT.relative_to(ROOT))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
