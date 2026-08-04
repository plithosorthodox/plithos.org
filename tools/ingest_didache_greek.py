#!/usr/bin/env python3
"""
Add the Didache in the Greek it was written in.

Everything patristic on this shelf has been an English translation. That is a
reasonable place to start and a poor place to stop: where the original
survives and is public domain, the original is the text and the translation is
the help. The Didache is the natural first, being short, being Greek, and
being the oldest thing here.

The text is the one Kirsopp Lake printed in the Loeb Apostolic Fathers, 1912,
from the Jerusalem manuscript Bryennios found in 1873. Public domain.

The work is emitted as a second edition of the same book rather than as a
separate book: it carries edition_of, so the shelf shows one Didache and the
reader can set the Greek and the English side by side, as it already can with
the Liturgy and now with both Testaments.

    python3 tools/ingest_didache_greek.py --check
    python3 tools/ingest_didache_greek.py --write
"""
import argparse
import html
import unicodedata
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "library" / "didache-grc.json"
INDEX = ROOT / "data" / "library" / "works-index.json"
CACHE = Path("/tmp/plithos-didache")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
SRC = "https://www.ccel.org/l/lake/fathers/didache.htm"

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI"]
CHAPTERS = 16

WORK = {
    "work_id": "didache-grc",
    "edition_of": "didache",
    "language": "grc",
    "title": "Διδαχὴ τῶν δώδεκα ἀποστόλων",
    "author": "The Twelve Apostles",
    "date": "c. 100",
    "translator": "",
    "pub_year": 1912,
    "source": "The Apostolic Fathers, Loeb Classical Library",
    "publisher": "William Heinemann, London",
    "source_class": "patristic",
    "description": "The Greek of the Didache as Kirsopp Lake printed it, from "
                   "the manuscript Philotheos Bryennios found at Constantinople "
                   "in 1873, which is the only complete copy the Church has.",
    "digitized": "Christian Classics Ethereal Library",
    "rights": "Public domain",
    "saint": "Synaxis of the Holy, Glorious and All-Praised Twelve Apostles",
    "is_saint": True,
}

# A phrase from the opening and one from the last chapter. Greek that has been
# through a bad decode still looks like Greek; these do not survive it.
#
# Compared under NFC. Polytonic Greek writes the same visible letter two ways:
# this edition sets the upsilon of δύο as U+1F7B, oxia, where a keyboard gives
# U+03CD, tonos. The two look identical and do not compare equal, which is how
# a check on Greek text passes review and then fails silently. The comparison
# is normalised; the text that is stored is not, because the site keeps every
# accent as the edition set it.
MUST_FIRST = "Ὁδοὶ δύο εἰσί"
MUST_LAST = "Γρηγορεῖτε"


def same(hay, needle):
    return (unicodedata.normalize("NFC", needle)
            in unicodedata.normalize("NFC", hay))


def fetch():
    p = CACHE / "didache-grc.htm"
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(SRC, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(0.8)
    return body


def clean(seg):
    seg = re.sub(r"<(script|style)\b.*?</\1>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<(p|br|div)\b[^>]*>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"</p>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"<[^>]+>", "", seg)
    seg = html.unescape(seg)
    # House rules, and nothing else: the Greek keeps every breathing and accent.
    seg = seg.translate(dict.fromkeys(map(ord, "–—‒―"), "-"))
    seg = seg.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
                         0x00A0: " "})
    paras = [re.sub(r"[ \t]+", " ", x).strip() for x in re.split(r"\n\s*\n", seg)]
    return "\n\n".join(x for x in paras if x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    body = fetch()
    marks = []
    for n in range(1, CHAPTERS + 1):
        m = re.search(r'<a name="%s"' % ROMAN[n], body)
        if not m:
            print("chapter %s is not marked in the source" % ROMAN[n])
            return 1
        marks.append(m.start())
    if marks != sorted(marks):
        print("the chapters are not in order in the source")
        return 1

    end = body.find("</body>")
    units = []
    for n in range(1, CHAPTERS + 1):
        stop = marks[n] if n < CHAPTERS else (end if end > 0 else len(body))
        text = clean(body[marks[n - 1]:stop])
        # The anchor itself renders as the bare numeral above the chapter.
        text = re.sub(r"\A\s*%s\s*\n+" % ROMAN[n], "", text)
        if not text.strip():
            print("chapter %s came out empty" % ROMAN[n])
            return 1
        units.append({
            "unit_id": "didache-grc::u%02d" % n,
            "work_id": "didache-grc",
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": "patristic",
            "ordinal": n,
            "citation_anchor": "Διδαχή %s" % ROMAN[n],
            "text": text,
        })

    if not same(units[0]["text"], MUST_FIRST):
        print("the opening of chapter I did not survive the fetch")
        return 1
    if not same(units[-1]["text"], MUST_LAST):
        print("the last chapter did not survive the fetch")
        return 1

    greek = sum(len(re.findall(r"[Ͱ-Ͽἀ-῿]", u["text"])) for u in units)
    latin = sum(len(re.findall(r"[A-Za-z]", u["text"])) for u in units)
    print("%d chapters, %s Greek characters, %d Latin characters"
          % (len(units), format(greek, ","), latin))
    print("first:  %s" % units[0]["text"][:90])
    print("last:   %s" % units[-1]["text"][:90])

    if args.write:
        OUT.write_text(json.dumps({"work": WORK, "units": units},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
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
