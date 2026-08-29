#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The language of the edition, stated rather than assumed.

Every entry in data/library/works-index.json carries the language of the text
the reader is actually given - `en` for a work served in an English
translation, `grc` for the Loeb Greek of the Apostolic Fathers, `el` for the
received Greek of the Akathist. Forty-six of the ninety-seven carried nothing.

Nothing was visibly wrong, and that is the whole of the problem. library.html
fills the gap itself, in two places - once for the works inside the page and
once for the works it fetches - so the catalogue said nothing where the reader
was shown English, and the two agreed only because the guess happened to be
right every time. Anything else reading the file, and the search index is one,
has no such guess.

The evidence is in the entry and is not inferred from silence: each of the
forty-six names an English translator and an English series - Wallis and
Pratten and Salmond in the Ante-Nicene Fathers, Moore and Wilson in the
Nicene and Post-Nicene, Parker's Dionysius, Mary Allies' Damascene, Davis's
Readings in Ancient History. Four of them - Sharbil, Barsamya, Habib, Shamuna
and Guria - are Syriac in the original, which is why the field says what is
served and not what was written.

An entry with a language already set is never touched.

    python3 tools/catalogue_language.py --check
    python3 tools/catalogue_language.py --write
"""
import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "data", "library", "works-index.json")

# A translator named in English, or an English series, is the evidence that the
# text served is English. A work with neither is not guessed at.
ENGLISH_SERIES = re.compile(
    r"Ante-Nicene Fathers|Nicene and Post-Nicene Fathers|"
    r"The Works of Dionysius the Areopagite|"
    r"St John Damascene on Holy Images|"
    r"Readings in Ancient History", re.I)


def evidence(w):
    """Why this entry's edition is English, or None if it cannot be shown."""
    src = w.get("source") or ""
    tr = (w.get("translator") or "").strip()
    if ENGLISH_SERIES.search(src):
        return "%s, tr. %s" % (src.split(";")[0].strip(), tr or "unnamed")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    works = json.load(io.open(INDEX, encoding="utf-8"))
    blank = [w for w in works if not w.get("language")]
    shown = [w for w in blank if evidence(w)]
    dark = [w for w in blank if not evidence(w)]

    if not a.write:
        print("%d works in the catalogue, %d state their language"
              % (len(works), len(works) - len(blank)))
        if blank:
            print("  %d state none; %d can be shown to be English"
                  % (len(blank), len(shown)))
        for w in dark:
            print("  no evidence either way: %s (%s)"
                  % (w["work_id"], w.get("source") or "no source"))
        return 0 if not blank else 1

    if dark:
        print("refusing to guess for %d works with no English series named:"
              % len(dark))
        for w in dark:
            print("  %s" % w["work_id"])
        return 1

    for w in shown:
        w["language"] = "en"
    io.open(INDEX, "w", encoding="utf-8").write(
        json.dumps(works, ensure_ascii=False, indent=1) + "\n")
    print("%d entries now state their edition's language" % len(shown))
    return 0


if __name__ == "__main__":
    sys.exit(main())
