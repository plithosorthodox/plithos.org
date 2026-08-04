#!/usr/bin/env python3
"""
Add the Corpus Areopagiticum.

Four works and a book of letters that stand behind most of what the Orthodox
tradition later says about hierarchy, about the sacraments as a visible order
of holy things, and about the God who is known by unknowing. St Maximus the
Confessor wrote scholia on them; the Seventh Council cites them; the whole
apophatic vocabulary of the East comes through them.

Sourced from sacred-texts.com's edition of John Parker's translation, London
1897, public domain. Its index page exposes no links, so the sections are
enumerated directly and the ranges are asserted below: a work that gains or
loses a chapter stops the run rather than publishing short.

The authorship is a real question and is answered in the entry's caution
rather than papered over. The Church received these writings; she did not
receive a claim about who held the pen.

    python3 tools/ingest_areopagite.py --check
    python3 tools/ingest_areopagite.py --write
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-areopagite")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
AUTHOR = "Dionysius the Areopagite"

COMMON = {
    "author": AUTHOR,
    "date": "c. 500",
    "translator": "John Parker",
    "pub_year": 1897,
    "source": "The Works of Dionysius the Areopagite",
    "publisher": "James Parker and Co., London and Oxford",
    "source_class": "patristic",
    "digitized": "sacred-texts.com",
    "rights": "Public domain",
    "saint": None,
    "is_saint": False,
}

# work_id -> (title, first page, last page, how many CAPUT chapters that range
#             must yield, description)
WORKS = [
    ("dionysius-divine-names", "On Divine Names", 4, 16, 13,
     "On what may be said of God from the names Scripture gives Him: Good, "
     "Being, Life, Wisdom, Power, Peace. The argument throughout is that every "
     "name is given from what God does rather than from what He is, and that "
     "He remains beyond all of them."),
    ("dionysius-mystic-theology", "Mystic Theology", 19, 23, 5,
     "Five short chapters, and the root of the apophatic tradition of the "
     "East: that God is known by putting away what He is not, that the "
     "affirmations fail before the denials do, and that at the last even the "
     "denials must be let go."),
    ("dionysius-heavenly-hierarchy", "On the Heavenly Hierarchy", 44, 58, 15,
     "On the ranks of the angels and how each order receives light and passes "
     "it on. This is where the familiar ordering comes from, seraphim and "
     "cherubim and thrones down to the angels who are sent to men, and the "
     "principle that God works through an order rather than around it."),
    ("dionysius-ecclesiastical-hierarchy", "Ecclesiastical Hierarchy", 59, 65, 7,
     "On the visible order of the Church as the earthly answer to the heavenly "
     "one: baptism, the synaxis, the chrism, the ordinations, the monastic "
     "tonsure, and the burial of the dead, each treated as a rite and then as "
     "what the rite means."),
]

LETTERS = ("dionysius-letters", "Letters", 25, 35, 11,
           "Eleven letters as this edition prints them, from a note of a few "
           "lines to a treatise on the divine judgement. The seventh answers a "
           "philosopher who had attacked the Christians; the eighth rebukes a "
           "monk who had refused communion to a penitent.")

CAUTION = (
    "These writings were transmitted under the name of the Dionysius whom the "
    "Apostle Paul converted at Athens, and they are not his: they show a "
    "liturgy and a vocabulary of about the year 500. The Church received the "
    "writings and read them as her own, and St Maximus the Confessor wrote on "
    "them; she never received a claim about whose hand held the pen. They are "
    "kept here under the name the manuscripts carry, and the date given is the "
    "date they were written."
)


def fetch(n):
    p = CACHE / ("dio%02d.htm" % n)
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    url = "https://www.sacred-texts.com/chr/dio/dio%02d.htm" % n
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(0.6)
    return body


def strip(seg):
    seg = re.sub(r"<(script|style)\b.*?</\1>", " ", seg, flags=re.S | re.I)
    # The edition marks its print pagination mid-sentence, in a green anchor:
    # "manifesting the whole <a name=page_13>p. 13</a> supremely-Divine".
    # Left in, it reads as text.
    seg = re.sub(r'<a name="page_\d+">.*?</a>', " ", seg, flags=re.S | re.I)
    seg = re.sub(r"<(p|br|div|h\d|li)\b[^>]*>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"</(p|div|h\d|li)>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"<[^>]+>", "", seg)
    seg = html.unescape(seg)
    seg = seg.translate(dict.fromkeys(map(ord, "–—‒―"), "-"))
    seg = seg.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
                         0x00A0: " "})
    paras = [re.sub(r"[ \t]+", " ", x).strip() for x in re.split(r"\n\s*\n", seg)]
    drop = re.compile(r"\A(Sacred Texts|Christianity|Index|Previous|Next|"
                      r"Buy this Book.*|p\.\s*\d+|\d+)\Z", re.I)
    return [x for x in paras if x and not drop.match(x)]


def body_of(n):
    """The text between the navigation and the footnotes."""
    raw = fetch(n)
    # The credit line sits directly above the text. Its words also appear in
    # the page head, so take the last occurrence, not the first: the first
    # match let the whole navigation column through as if it were text.
    i = raw.rfind("at sacred-texts.com")
    seg = raw[i + len("at sacred-texts.com"):] if i > 0 else raw
    cut = re.search(r"<h[1-4][^>]*>\s*Footnotes", seg, re.I)
    if cut:
        seg = seg[:cut.start()]
    caput = None
    # The heading carries an anchor tag inside it, so the words are not
    # adjacent to the tag that opens them.
    for m in re.finditer(r"<h[1-4][^>]*>(.*?)</h[1-4]>", seg, re.S | re.I):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1))))
        mm = re.match(r"\s*(CAPUT\s+[IVXL]+)", t, re.I)
        if mm:
            # title() would render CAPUT II as "Caput Ii".
            word, _, num = mm.group(1).strip().partition(" ")
            caput = "Caput %s" % num.upper()
            break
    paras = strip(seg)
    # The running credit line the site puts above every page.
    paras = [p for p in paras
             if not p.startswith("The Works of Dionysius the Areopagite, tr.")]
    return caput, "\n\n".join(paras)


def build_work(wid, title, first, last, chapters, desc, numbered_letters=False):
    units, seen = [], []
    for i, n in enumerate(range(first, last + 1), start=1):
        caput, text = body_of(n)
        if not text.strip():
            return None, "page dio%02d is empty" % n
        if numbered_letters:
            anchor = "Letter %s" % ROMAN[i]
        else:
            if not caput:
                return None, "page dio%02d carries no chapter heading" % n
            anchor = "%s, %s" % (title, caput)
            seen.append(caput)
        units.append({
            "unit_id": "%s::u%02d" % (wid, i),
            "work_id": wid,
            "work_title": title,
            "author": AUTHOR,
            "source_class": "patristic",
            "ordinal": i,
            "citation_anchor": anchor,
            "text": text,
        })
    if len(units) != chapters:
        return None, "%d sections, %d expected" % (len(units), chapters)
    return units, None


ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    built, failed = [], []
    todo = [(w[0], w[1], w[2], w[3], w[4], w[5], False) for w in WORKS]
    todo.append((LETTERS[0], LETTERS[1], LETTERS[2], LETTERS[3], LETTERS[4],
                 LETTERS[5], True))

    for wid, title, first, last, count, desc, letters in todo:
        units, err = build_work(wid, title, first, last, count, desc, letters)
        if err:
            failed.append((wid, err))
            print("  FAIL  %-38s %s" % (wid, err))
            continue
        words = sum(len(u["text"].split()) for u in units)
        bad = sum(len(re.findall(r"[–—‘’“”]", u["text"])) for u in units)
        print("  ok    %-38s %2d units  %7s words  %d dashes/smart quotes"
              % (wid, len(units), format(words, ","), bad))
        meta = dict(COMMON, work_id=wid, title=title, description=desc)
        built.append((meta, units))

    if failed:
        print("\n%d of %d failed; nothing written" % (len(failed), len(todo)))
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
        print("\nwrote %d works and updated the catalogue" % len(built))
        print("the caution for these belongs in tools/reception.py")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
