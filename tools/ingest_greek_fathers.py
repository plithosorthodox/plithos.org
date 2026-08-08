#!/usr/bin/env python3
"""
Add the Apostolic Fathers in Greek, beside the English already here.

The Didache showed the shape. This does the rest of the collection Kirsopp
Lake printed in the Loeb Apostolic Fathers, 1912: the Greek text, emitted as
another edition of a book the shelf already holds, so the two read side by
side and the shelf still shows one book.

An edition is only offered alongside another when the two divide the work the
same way. Setting chapter 5 of one against chapter 7 of the other because the
rows happened to line up would be worse than not offering it at all, so every
entry declares how many sections it must yield and the run stops if the count
disagrees with the English.

The count check earned itself on the first run. Lake prints sixty-five
chapters of the First Epistle of Clement; the English edition then on this
shelf printed fifty-nine and stopped before the long prayer that closes the
letter. Rather than align the two badly, the English was replaced with the
edition that carries all sixty-five, and they now stand together.

The Shepherd is not here yet: Lake does not divide it by the same anchors and
it needs its own reading.

    python3 tools/ingest_greek_fathers.py --check
    python3 tools/ingest_greek_fathers.py --write
"""
import argparse
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "library.html"
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-greek-fathers")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
BASE = "https://www.ccel.org/l/lake/fathers/"

# The date a work was written, not the date this edition was printed. The
# Library shows it first and shows nothing at all when it is missing.
DATES = {
    "second-clement-grc": "c. 140",
    "polycarp-philippians-grc": "c. 110",
    "martyrdom-of-polycarp-grc": "c. 156",
    "epistle-to-diognetus-grc": "2nd century",
    "epistle-of-barnabas-grc": "late 1st-early 2nd century",
    "clement-first-epistle-grc": "c. 96",
    "ignatius-seven-epistles-grc": "c. 107",
}

COMMON = {
    "language": "grc",
    "translator": "",
    "pub_year": 1912,
    "source": "The Apostolic Fathers, Loeb Classical Library",
    "publisher": "William Heinemann, London",
    "source_class": "patristic",
    "digitized": "Christian Classics Ethereal Library",
    "rights": "Public domain",
}

# Roman numerals as Lake sets them, in order, so a chapter can be found by
# name rather than by counting.
ROMAN = []
for _i in range(1, 80):
    _n, _s = _i, ""
    for _v, _r in ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"),
                   (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while _n >= _v:
            _s += _r
            _n -= _v
    ROMAN.append(_s)


def roman(n):
    return ROMAN[n - 1]


# work_id of the Greek, its English partner (or None), the pages, how many
# chapters the pages must yield, the Greek title, the author, and a phrase
# that has to survive.
WORKS = [
    ("second-clement-grc", "second-clement", ["clement-ii_clement.htm"], 20,
     "Ὁμιλία ἀρχαία", "An unknown preacher",
     "Ἀδελφοί, οὕτως δεῖ ἡμᾶς φρονεῖν",
     "The Greek of the oldest surviving Christian sermon, as Lake printed it."),
    ("polycarp-philippians-grc", "polycarp-to-the-philippians",
     ["polycarp-philippians.htm"], 14,
     "Πολυκάρπου πρὸς Φιλιππησίους", "St Polycarp of Smyrna", "Πολύκαρπος",
     "The Greek of Polycarp's letter to the Philippians."),
    ("martyrdom-of-polycarp-grc", "martyrdom-of-polycarp", ["martyrdom.htm"], 22,
     "Μαρτύριον τοῦ ἁγίου Πολυκάρπου", "The Church of Smyrna",
     "ἐκκλησία τοῦ θεοῦ ἡ παροικοῦσα Σμύρναν",
     "The Greek of the letter the church of Smyrna sent after Polycarp's death."),
    ("epistle-to-diognetus-grc", "epistle-to-diognetus", ["diognetus.htm"], 12,
     "Πρὸς Διόγνητον", "Mathetes", "Διόγνητε",
     "The Greek of the letter to Diognetus."),
    ("epistle-of-barnabas-grc", "epistle-of-barnabas",
     ["barnabas_a.htm", "barnabas_b.htm"], 21,
     "Βαρνάβα ἐπιστολή", "St Barnabas the Apostle", "Χαίρετε",
     "The Greek of the letter transmitted under the name of Barnabas."),
    ("clement-first-epistle-grc", "clement-of-rome-first-epistle",
     ["clement-i_clement_a.htm", "clement-i_clement_b.htm",
      "clement-i_clement_c.htm"], 65,
     "Κλήμεντος πρὸς Κορινθίους Α", "St Clement of Rome", "Κορινθίων",
     "The Greek of Clement's letter to the Corinthians as Lake printed it, "
     "in the sixty-five chapters the Bryennios manuscript supplies."),
]

# The seven letters of Ignatius. Lake gives each its own page; the English
# edition on this shelf carries one unit per letter, so the Greek does too and
# the chapters within a letter run together as the letter.
IGNATIUS = [
    ("ignatius-ephesians.htm", "Πρὸς Ἐφεσίους"),
    ("ignatius-magnesians.htm", "Πρὸς Μαγνησιεῖς"),
    ("ignatius-trallians.htm", "Πρὸς Τραλλιανούς"),
    ("ignatius-romans.htm", "Πρὸς Ῥωμαίους"),
    ("ignatius-philadelphians.htm", "Πρὸς Φιλαδελφεῖς"),
    ("ignatius-smyrnaeans.htm", "Πρὸς Σμυρναίους"),
    ("ignatius-polycarp.htm", "Πρὸς Πολύκαρπον"),
]


def same(hay, needle):
    """Compared under NFC. Polytonic Greek writes the same visible letter two
    ways, oxia and tonos, and they do not compare equal."""
    return (unicodedata.normalize("NFC", needle)
            in unicodedata.normalize("NFC", hay))


def decode(raw):
    """Decode by what the page declares, not by hope.

    CCEL serves these pages as windows-1252 with the Greek in numeric
    entities and the Greek numeral sign as a cp1252 right quote. Decoding
    them as UTF-8 with errors="replace" succeeds, looks like Greek, and
    silently substitutes U+FFFD for every one of those bytes. That is how
    four hundred and sixteen replacement characters reached the shelf.
    """
    m = re.search(rb"charset=([\w-]+)", raw[:4000], re.I)
    declared = m.group(1).decode("ascii", "replace").lower() if m else "utf-8"
    for enc in (declared, "utf-8", "cp1252"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


def fetch(page):
    p = CACHE / page
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(BASE + page, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = decode(r.read())
    p.write_text(body, encoding="utf-8")
    time.sleep(0.6)
    return body


def clean(seg):
    seg = re.sub(r"<(script|style)\b.*?</\1>", " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<(p|br|div)\b[^>]*>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"</p>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"<[^>]+>", "", seg)
    seg = html.unescape(seg)
    seg = seg.translate(dict.fromkeys(map(ord, "–—‒―"), "-"))
    seg = seg.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
                         0x00A0: " "})
    paras = [re.sub(r"[ \t]+", " ", x).strip() for x in re.split(r"\n\s*\n", seg)]
    drop = re.compile(r"\A(TOC|\[\s*TOC\s*\]|\d+)\Z", re.I)
    return "\n\n".join(x for x in paras if x and not drop.match(x))


# CCEL's anchor names are navigation, not text, and one of them is a typo:
# the fifty-third chapter of Clement is targeted XLIII, which is forty-three
# and is already used. The chapters are in the right order and the text is
# whole; only the link target is wrong. The exception is named here rather
# than waved through by loosening the check, so a second one still fails.
KNOWN_ANCHOR_TYPOS = {"clement-first-epistle-grc": {53: "XLIII"}}

# Where a letter opens with its address before the first numbered chapter,
# that address is text and belongs to the letter. It is carried into chapter
# I, which is where the English editions keep it, so the counts still agree.
SALUTATION = {"polycarp-philippians-grc", "martyrdom-of-polycarp-grc"}


def chapters(pages, want, wid=None):
    """Every roman-numbered chapter across the pages, in order."""
    out = []
    for page in pages:
        body = fetch(page)
        marks = [(m.group(1), m.start())
                 for m in re.finditer(r'<a name="([IVXLC]+)"', body)]
        end = body.find("</body>")
        if end < 0:
            end = len(body)
        for k, (num, pos) in enumerate(marks):
            stop = marks[k + 1][1] if k + 1 < len(marks) else end
            text = clean(body[pos:stop])
            text = re.sub(r"\A\s*%s\s*\n+" % num, "", text)
            out.append((num, text))
    if len(out) != want:
        return None, "%d chapters, %d expected" % (len(out), want)
    typos = KNOWN_ANCHOR_TYPOS.get(wid, {})
    for k, (num, text) in enumerate(out):
        if num != roman(k + 1) and typos.get(k + 1) != num:
            return None, "chapter %d is marked %s" % (k + 1, num)
        if not text.strip():
            return None, "chapter %s is empty" % num

    if wid in SALUTATION:
        body = fetch(pages[0])
        m = re.search(r'<a name="I"', body)
        head = clean(body[:m.start()])
        paras = [x for x in head.split("\n\n") if x.strip()]
        # The address is the last paragraph before chapter I; everything above
        # it is the page's own furniture and the title in capitals.
        if not paras or not re.search(r"[\u1F00-\u1FFF\u0370-\u03FF]", paras[-1]):
            return None, "no salutation found before chapter I"
        out[0] = (out[0][0], paras[-1] + "\n\n" + out[0][1])
    return out, None


def english_units(wid):
    p = OUTDIR / (wid + ".json")
    if p.exists():
        return len(json.loads(p.read_text(encoding="utf-8"))["units"])
    src = READER.read_text(encoding="utf-8")
    i = src.index("const CORPUS")
    eq = src.index("=", i)
    j = src.index("\n", i)
    C = json.loads(src[eq + 1:j].rstrip().rstrip(";"))
    return sum(1 for u in C["units"] if u["work_id"] == wid)


def build_ignatius():
    units = []
    for n, (page, title) in enumerate(IGNATIUS, start=1):
        body = fetch(page)
        marks = [m.start() for m in re.finditer(r'<a name="[IVXLC]+"', body)]
        if not marks:
            return None, "%s has no chapters" % page
        end = body.find("</body>")
        text = clean(body[marks[0]:(end if end > 0 else len(body))])
        if not text.strip():
            return None, "%s came out empty" % page
        units.append({
            "unit_id": "ignatius-seven-epistles-grc::u%02d" % n,
            "work_id": "ignatius-seven-epistles-grc",
            "work_title": "Ἰγνατίου ἐπιστολαί",
            "author": "St Ignatius of Antioch",
            "source_class": "patristic",
            "ordinal": n,
            "citation_anchor": title,
            "text": text,
        })
    return units, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    built, failed = [], []

    for wid, partner, pages, want, title, author, must, desc in WORKS:
        got, err = chapters(pages, want, wid)
        if err:
            failed.append((wid, err))
            print("  FAIL  %-30s %s" % (wid, err))
            continue
        if partner:
            n = english_units(partner)
            if n != want:
                failed.append((wid, "English partner has %d units, Greek %d"
                               % (n, want)))
                print("  FAIL  %-30s English %d, Greek %d; not aligned"
                      % (wid, n, want))
                continue
        units = [{
            "unit_id": "%s::u%02d" % (wid, k + 1),
            "work_id": wid,
            "work_title": title,
            "author": author,
            "source_class": "patristic",
            "ordinal": k + 1,
            "citation_anchor": "%s %s" % (title.split()[-1], num),
            "text": text,
        } for k, (num, text) in enumerate(got)]
        bad = sum(u["text"].count("\ufffd") for u in units)
        if bad:
            failed.append((wid, "%d replacement characters" % bad))
            print("  FAIL  %-30s %d replacement characters" % (wid, bad))
            continue
        if not same(" ".join(u["text"] for u in units), must):
            failed.append((wid, "the phrase %r did not survive" % must))
            print("  FAIL  %-30s %r did not survive" % (wid, must))
            continue
        meta = dict(COMMON, work_id=wid, title=title, author=author,
                    date=DATES[wid], description=desc)
        if partner:
            meta["edition_of"] = partner
        built.append((meta, units))
        gk = sum(len(re.findall(r"[Ͱ-Ͽἀ-῿]", u["text"])) for u in units)
        print("  ok    %-30s %3d chapters  %7s Greek chars  %s"
              % (wid, len(units), format(gk, ","),
                 "beside " + partner if partner else "stands alone"))

    units, err = build_ignatius()
    if err:
        failed.append(("ignatius-seven-epistles-grc", err))
        print("  FAIL  ignatius-seven-epistles-grc  %s" % err)
    else:
        n = english_units("ignatius-seven-epistles")
        if n != len(units):
            failed.append(("ignatius-seven-epistles-grc",
                           "English has %d, Greek %d" % (n, len(units))))
            print("  FAIL  ignatius-seven-epistles-grc  English %d, Greek %d"
                  % (n, len(units)))
        else:
            meta = dict(COMMON, work_id="ignatius-seven-epistles-grc",
                        date=DATES["ignatius-seven-epistles-grc"],
                        edition_of="ignatius-seven-epistles",
                        title="Ἰγνατίου ἐπιστολαί",
                        author="St Ignatius of Antioch",
                        description="The Greek of the seven letters Ignatius "
                                    "wrote on the road to Rome, one unit to a "
                                    "letter as the English edition has them.")
            built.append((meta, units))
            gk = sum(len(re.findall(r"[Ͱ-Ͽἀ-῿]", u["text"])) for u in units)
            print("  ok    %-30s %3d letters   %7s Greek chars  beside %s"
                  % ("ignatius-seven-epistles-grc", len(units),
                     format(gk, ","), "ignatius-seven-epistles"))

    if failed:
        print("\n%d failed; nothing written" % len(failed))
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
        print("\nwrote %d Greek editions" % len(built))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
