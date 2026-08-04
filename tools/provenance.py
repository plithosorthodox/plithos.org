#!/usr/bin/env python3
"""
Separate the four things a Library entry runs together.

A work has an author and a date. The book it is read from has a translator,
a publisher, and a year of its own, and those are not the same thing: the
Homilies on Matthew were preached about 390 and the translation on this
shelf was published in 1888. The catalogue held both numbers but showed
them in one undifferentiated line, so a reader could not tell which was
which, and it held no publisher at all.

Four fields are settled here:

  translator  who rendered it into the language it is read in. Absent where
              the text is in its own language, which is itself information:
              the Greek Liturgy has no translator and should not appear to.
  source      the edition or volume the text is taken from, with the series
              named one way. The catalogue wrote "Series II" and "Series 2"
              for the same series.
  publisher   who published that edition. Set only for editions whose
              publisher is established. The scripture bundles are left
              without one: naming a publisher for a text whose revision is
              not settled would assert a check that has not been made.
  pub_year    the year that edition was published, as distinct from the
              date the work was written.

    python3 tools/provenance.py --check
    python3 tools/provenance.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "plithos_reader.html"
INDEX = ROOT / "data" / "library" / "works-index.json"

# The two nineteenth-century American series the patristic shelf is drawn
# from. Both were reprinted many times; these are the original publishers of
# the editions whose text and pagination the digitizations follow.
ANF = "Christian Literature Publishing Company, Buffalo"
NPNF = "Christian Literature Company, New York"

# source volume (after normalising) -> publisher
PUBLISHERS = {
    "Ante-Nicene Fathers": ANF,
    "Nicene and Post-Nicene Fathers": NPNF,
}

# work_id -> publisher, for editions outside the two series.
PUBLISHER_BY_WORK = {
    "divine-liturgy-chrysostom-en": "Williams & Norgate, London",
    "divine-liturgy-chrysostom-de": "Liturgical Commission of the Orthodox "
                                    "Bishops' Conference in Germany",
}

# The same man, entered two ways.
TRANSLATOR_FIX = {
    "F. Crombie": "Frederick Crombie",
}

# Translators the catalogue left blank.
TRANSLATOR_BY_WORK = {
    # The creed is printed in Percival's volume in his rendering, as are the
    # canons and the acts beside it.
    "nicene-constantinopolitan-creed": "Henry R. Percival",
}

# Scripture editions named for the men who made them. Where an edition is
# known by its translator, that is who the translator is, and the reader
# should be able to see it rather than infer it from the edition name.
SCRIPTURE_TRANSLATORS = {
    "ro":  "Dumitru Cornilescu",
    "sr":  "Vuk Karadzic",
    "uk":  "Panteleimon Kulish",
    "pt":  "Joao Ferreira de Almeida",
    "ja":  "Emile Raguet",
    "ar":  "Eli Smith and Cornelius Van Dyck",
    "es":  "Casiodoro de Reina, revised by Cipriano de Valera",
    "fr":  "Jean-Frederic Ostervald and David Martin",
    "de":  "Franz Eugen Schlachter",
    "it":  "Giovanni Luzzi",
}

# The volume title belongs to the description, not to the citation.
SOURCE_FIX = {
    "Nicene and Post-Nicene Fathers, Series 2, Vol. 14: "
    "The Seven Ecumenical Councils of the Undivided Church":
        "Nicene and Post-Nicene Fathers, Series 2, Vol. 14",
    "The Divine Liturgy of St. John Chrysostom: the Greek Text with a "
    "Rendering in English (Williams & Norgate, London)":
        "The Divine Liturgy of St. John Chrysostom: the Greek Text with a "
        "Rendering in English",
    "Received German text of the Orthodox Church (Liturgical Commission, OBKD)":
        "Received German text of the Orthodox Church",
}

DIGITIZED_FIX = {
    "Christian Classics Ethereal Library": "CCEL",
}

ROMAN = {"I": "1", "II": "2", "III": "3"}


def normalise_source(s):
    """One spelling of the series. The catalogue held two."""
    if not s:
        return s
    s = SOURCE_FIX.get(s, s)
    return re.sub(r"\bSeries (I{1,3})\b",
                  lambda m: "Series " + ROMAN[m.group(1)], s)


def publisher_for(w):
    if w["work_id"] in PUBLISHER_BY_WORK:
        return PUBLISHER_BY_WORK[w["work_id"]]
    src = w.get("source") or ""
    for prefix, pub in PUBLISHERS.items():
        if src.startswith(prefix):
            return pub
    return None


def fix(w, report):
    before = json.dumps(w, sort_keys=True, ensure_ascii=False)
    wid = w.get("work_id") or ""

    w["source"] = normalise_source(w.get("source"))

    tr = w.get("translator")
    tr = TRANSLATOR_FIX.get(tr, tr)
    if not tr:
        tr = TRANSLATOR_BY_WORK.get(wid)
    m = re.match(r"^bible-([a-z]{2,3})$", wid)
    if m and not tr:
        tr = SCRIPTURE_TRANSLATORS.get(m.group(1))
    if tr:
        w["translator"] = tr
    else:
        w.pop("translator", None)

    d = w.get("digitized")
    if d in DIGITIZED_FIX:
        w["digitized"] = DIGITIZED_FIX[d]

    pub = publisher_for(w)
    if pub:
        w["publisher"] = pub
    else:
        w.pop("publisher", None)
        if w.get("pub_year") and not wid.startswith("bible-"):
            report.append("%s: a year of publication with no publisher" % wid)

    return json.dumps(w, sort_keys=True, ensure_ascii=False) != before


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

    report, changed = [], 0
    allw = corpus["works"] + lazy
    for w in allw:
        if fix(w, report):
            changed += 1

    for line in report:
        print("  %s" % line)

    import collections
    print("%d works, %d changed" % (len(allw), changed))
    print("\nseries and editions:")
    for s, n in collections.Counter(w.get("source") for w in allw).most_common(8):
        print("   %-58s %d" % (s, n))
    print("\npublishers:")
    for p, n in collections.Counter(w.get("publisher") for w in allw).most_common():
        print("   %-58s %d" % (p or "(none recorded)", n))
    no_tr = [w["work_id"] for w in allw if not w.get("translator")]
    print("\nno translator (the text is in its own language, or the edition "
          "is not named for one): %d" % len(no_tr))
    for wid in no_tr:
        print("   %s" % wid)

    if args.write:
        line = "const CORPUS = " + json.dumps(corpus, ensure_ascii=False,
                                              separators=(",", ":")) + ";"
        READER.write_text(src[:i] + line + src[j:], encoding="utf-8")
        INDEX.write_text(json.dumps(lazy, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote plithos_reader.html and works-index.json")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main())
