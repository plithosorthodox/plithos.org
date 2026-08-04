#!/usr/bin/env python3
"""
Add the Shepherd of Hermas in Greek.

The rest of Lake's Apostolic Fathers went in with a shared splitter that cuts
on roman-numbered anchors. The Shepherd does not yield to it. It is divided
into Visions, Mandates and Similitudes rather than chapters; it is spread over
seven pages, one section running across two of them; and the anchors carry
their own damage - mandate four is targeted "madate", parable four has a space
in it, and several are used twice.

So the twenty-seven sections are found two ways and both are checked.

The Visions and Mandates are found by their Greek headings, because those are
the text and the anchors are not. That also settles the fifth Vision, which
has no vision anchor at all and is not headed Ὅρασις: Lake heads it
Ἀποκάλυψις ε', the fifth revelation, which is why counting Ὅρασις gives four.

The Similitudes are found by their anchors, because Lake heads the first of
them with a title over the whole set rather than a number of its own.

Entities are unescaped before anything is located, so a Greek heading and an
anchor tag can be found in the same string. The pages are windows-1252.

    python3 tools/ingest_shepherd_greek.py --check
    python3 tools/ingest_shepherd_greek.py --write
"""
import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_greek_fathers import fetch, clean  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "library" / "shepherd-of-hermas-grc.json"
INDEX = ROOT / "data" / "library" / "works-index.json"

PAGES = ["shepherd_a.htm", "shepherd_b.htm", "shepherd_c.htm", "shepherd_d.htm",
         "shepherd_e.htm", "shepherd_f.htm", "shepherd_g.htm"]

# Greek numerals as Lake sets them, with the keraia. Stigma stands for six.
GK = ["", "α", "β", "γ", "δ", "ε", "ς", "ζ", "η", "θ", "ι", "ια", "ιβ"]
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

WORK = {
    "work_id": "shepherd-of-hermas-grc",
    "edition_of": "shepherd-of-hermas",
    "language": "grc",
    "title": "Ποιμὴν τοῦ Ἑρμᾶ",
    "author": "St Hermas of the Seventy",
    "date": "c. 140",
    "translator": "",
    "pub_year": 1912,
    "source": "The Apostolic Fathers, Loeb Classical Library",
    "publisher": "William Heinemann, London",
    "source_class": "patristic",
    "description": "The Shepherd as Lake printed it: five Visions, twelve "
                   "Mandates and ten Similitudes, in the divisions the English "
                   "edition here also keeps. The tenth Similitude is in Latin, "
                   "which is how it survives; the Greek of the closing section "
                   "is lost and the edition prints the old Latin version in its "
                   "place.",
    "digitized": "Christian Classics Ethereal Library",
    "rights": "Public domain",
    "saint": "Apostle Hermas of the Seventy",
    "is_saint": True,
}


def marks(body):
    """(position, citation) for each of the twenty-seven sections.

    Searched against a normalised copy. This edition writes the alpha of
    Ἀποκάλυψις with oxia where a keyboard gives tonos, so a literal written
    here does not match a heading that is identical to it on screen. The copy
    is the same length as the original, which is asserted, so a position found
    in one is the same position in the other and the text that gets stored is
    still the edition's own characters, accent for accent.
    """
    # Normalised one character at a time. Whole-string NFC also composes the
    # decomposed sequences in this page and shortens it, and a position found
    # in a shorter string is not a position in the original. Per character,
    # oxia becomes tonos and nothing else moves, so the copy lines up exactly.
    def flat(ch):
        n = unicodedata.normalize("NFC", ch)
        return n if len(n) == 1 else ch
    probe = "".join(flat(ch) for ch in body)
    if len(probe) != len(body):
        return None, "normalising moved the text; positions cannot be shared"
    body = probe
    found = []
    for n in range(1, 6):
        # The fifth is Ἀποκάλυψις, not Ὅρασις. Counting only Ὅρασις finds four
        # and reports nothing wrong, which is the failure to avoid here.
        word = "Ἀποκάλυψις" if n == 5 else "Ὅρασις"
        m = re.search(r"%s\s*%s\s*[’']" % (word, GK[n]), body)
        if not m:
            return None, "Vision %d (%s %s) not found" % (n, word, GK[n])
        # Cited as the edition heads it. Lake calls the fifth a revelation
        # and not a vision, and renaming it here would be correcting him.
        found.append((m.start(), m.end(), "%s %s" % (word, GK[n])))
    for n in range(1, 13):
        m = re.search(r"Ἐντολ[ὴή]\s*%s\s*[’']" % GK[n], body)
        if not m:
            return None, "Mandate %d (Ἐντολὴ %s) not found" % (n, GK[n])
        found.append((m.start(), m.end(), "Ἐντολὴ %s" % GK[n]))
    for n in range(1, 11):
        # Lake titles the whole set of Similitudes and numbers them only in
        # the anchors, so these are found there. Anchor names are normalised:
        # "madate" and "parable IV" are the source's own slips.
        pat = r'<a name="\s*(?:parable[_ ]%s)\s*"' % ROMAN[n]
        m = re.search(pat, body, re.I)
        if not m:
            return None, "Similitude %d (parable_%s) not found" % (n, ROMAN[n])
        # The anchor is not text; the collection title that follows it is,
        # so a Similitude begins where its anchor begins.
        found.append((m.start(), m.start(), "Παραβολὴ %s" % GK[n]))
    found.sort()
    if len(found) != 27:
        return None, "%d sections, 27 expected" % len(found)
    return found, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    # One string for the whole book. Similitude IX runs across two pages, so
    # splitting page by page would cut it in half.
    parts = []
    for p in PAGES:
        raw = fetch(p)
        # Drop the navigation that opens and closes every page before joining,
        # or it lands in the middle of a section.
        raw = re.sub(r"\[\s*(TOC|Part \d+)\s*\]", " ", raw)
        parts.append(html.unescape(raw))
    body = "\n".join(parts)

    found, err = marks(body)   # positions hold in the original, see marks()
    if err:
        print(err)
        return 1

    units = []
    for i, (pos, textfrom, cite) in enumerate(found):
        stop = found[i + 1][0] if i + 1 < len(found) else len(body)
        # Sliced from the end of the heading match rather than re-matching the
        # heading in the text. Re-matching would need the literal to agree with
        # the edition's accents, which is the trap this file already documents.
        text = clean(body[textfrom:stop])
        # Whatever punctuation trailed the heading goes with it.
        text = re.sub(r"\A[\s.'\u2019]+", "", text)
        if len(text.split()) < 40:
            print("%s came out with %d words" % (cite, len(text.split())))
            return 1
        units.append({
            "unit_id": "shepherd-of-hermas-grc::u%02d" % (i + 1),
            "work_id": WORK["work_id"],
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": "patristic",
            "ordinal": i + 1,
            "citation_anchor": cite,
            "text": text,
        })

    bad = sum(u["text"].count("�") for u in units)
    if bad:
        print("%d replacement characters: the pages did not decode" % bad)
        return 1

    english = json.loads((ROOT / "data" / "library" /
                          "shepherd-of-hermas.json").read_text(encoding="utf-8"))
    if len(english["units"]) != len(units):
        print("English has %d sections, Greek %d; not aligned"
              % (len(english["units"]), len(units)))
        return 1

    greek = sum(len(re.findall(r"[Ͱ-Ͽἀ-῿]", u["text"])) for u in units)
    print("%d sections, %s Greek characters" % (len(units), format(greek, ",")))
    for u in (units[0], units[4], units[5], units[17], units[-1]):
        print("   %-14s %s" % (u["citation_anchor"], u["text"][:64]))

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
