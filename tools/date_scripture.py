#!/usr/bin/env python3
"""
Give every New Testament entry in the Library a date.

The nineteen scripture works in the embedded CORPUS carried no date and no
edition year, so the Library showed them with the date line simply absent.
Every other work in the Library leads with the date of the work itself, and
scripture should not be the exception.

Two different dates are involved and the distinction matters:

  date      the work's own date. For the New Testament that is the first
            century, in the same sense that the Conferences are c. 426. This
            is what the reader shows in bold.
  pub_year  the year THIS translation was first published, shown against the
            edition in the source line.

Edition years are set only where they are certain or where the bundle itself
records them. Where the edition is known but its year is not established here,
the edition is named and no year is given: a wrong date on a scripture edition
is worse than none, and this site does not guess at provenance.

    python3 tools/date_scripture.py --check    # report, change nothing
    python3 tools/date_scripture.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "plithos_reader.html"

NT_DATE = "1st century"

# lang -> (edition as it should be shown, first publication year or None)
EDITIONS = {
    "en":  ("King James Version", 1611),
    "ru":  ("Russian Synodal Version", 1876),
    "uk":  ("Panteleimon Kulish", 1871),
    "it":  ("Riveduta", 1927),
    "ja":  ("Raguet-yaku", 1910),
    "el":  ("Robinson-Pierpont Byzantine Majority Text", 2018),
    "zh":  ("Chinese Union Version", 1919),
    "ro":  ("Cornilescu", 1921),
    "sr":  ("Vuk Karadzic", 1847),
    # Edition known, year not established here. Named without a year. Some of
    # these also need their provenance confirmed before a year is asserted: the
    # bundles were built from open-repo texts whose identifiers do not settle
    # which revision they hold, and at least three of those revisions have
    # candidates that are not public domain. A date would imply a check that
    # has not happened.
    "ar":  ("Smith and Van Dyck", 1860),
    "arc": ("Peshitta", None),
    "de":  ("Schlachter", None),
    "es":  ("Reina-Valera", None),
    "fr":  ("Ostervald and Martin tradition", None),
    "hi":  ("Hindi Old Version", None),
    "hy":  ("Western Armenian", None),
    "ko":  ("Korean public-domain edition", None),
    "pt":  ("Almeida", None),
    "sw":  ("Swahili public-domain edition", None),
}


def load_corpus(src):
    i = src.index("const CORPUS")
    eq = src.index("=", i)
    j = src.index("\n", i)
    line = src[eq + 1:j].rstrip().rstrip(";")
    return json.loads(line), i, eq, j


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    src = READER.read_text(encoding="utf-8")
    corpus, i, eq, j = load_corpus(src)

    changed, unknown, missing = 0, [], []
    for w in corpus["works"]:
        wid = w.get("work_id") or ""
        m = re.match(r"^bible-([a-z]{2,3})$", wid)
        if not m:
            if not w.get("date"):
                missing.append(wid)
            continue
        lang = m.group(1)
        ed = EDITIONS.get(lang)
        if not ed:
            unknown.append(lang)
            continue
        name, year = ed
        before = (w.get("date"), w.get("pub_year"), w.get("source"))
        w["date"] = NT_DATE
        w["source"] = name
        if year:
            w["pub_year"] = year
        else:
            w.pop("pub_year", None)
        if before != (w.get("date"), w.get("pub_year"), w.get("source")):
            changed += 1

    for lang in unknown:
        print("no edition recorded for bible-%s" % lang)
    for wid in missing:
        print("no date on non-scripture work %s" % wid)

    dated = sum(1 for w in corpus["works"] if w.get("date"))
    print("%d works, %d dated, %d updated" % (len(corpus["works"]), dated, changed))
    no_year = sorted(l for l, (n, y) in EDITIONS.items() if not y)
    print("edition named without a year: %s" % ", ".join(no_year))

    if args.write:
        line = "const CORPUS = " + json.dumps(corpus, ensure_ascii=False,
                                              separators=(",", ":")) + ";"
        READER.write_text(src[:i] + line + src[j:], encoding="utf-8")
        print("wrote plithos_reader.html")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 1 if unknown or missing else 0


if __name__ == "__main__":
    sys.exit(main())
