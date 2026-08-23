#!/usr/bin/env python3
"""The Library's entry for each New Testament, kept true to what is published.

    python3 tools/library_bibles.py --check
    python3 tools/library_bibles.py --write

The reader is told, above every chapter, whose translation he is reading. That
line is written in library.html and the text is in data/, and the two drifted:
the French entry named Ostervald and Martin over a text that was neither, and
the Romanian named Cornilescu. This writes the entries from one place, so that
what the page says and what the reader is given cannot come apart again.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

APOSTLES = "The Apostles and Evangelists"

# work_id suffix -> what the entry says.
ENTRIES = {
    "en": ("English", "King James Version", 1611, None,
           "The New Testament in English, in the Authorized Version of 1611."),
    "ar": ("Arabic", "Smith and Van Dyck", 1865,
           "Eli Smith and Cornelius Van Dyck",
           "The New Testament in Arabic, in the Smith and Van Dyck "
           "translation, with the vowel points as the edition prints them."),
    "arc": ("Aramaic", "Peshitta", None, None,
            "The New Testament in Aramaic, in the Syriac Peshitta."),
    "cu": ("Church Slavonic", "Elizabeth Bible", 1751, None,
           "The New Testament in Church Slavonic, in the Elizabeth Bible of "
           "1751, the edition the Slavic Churches read in their services. It "
           "is the edition this site's Church Slavonic Old Testament is "
           "taken from."),
    "de": ("German", "Schlachter", 1951, "Franz Eugen Schlachter",
           "The New Testament in German, in the Schlachter translation."),
    "el": ("Greek", "Byzantine Majority Text", None, None,
           "The Greek New Testament in the Byzantine textform, the text "
           "received and read by the Orthodox Church. The passage of the "
           "woman taken in adultery stands in its place in John."),
    "es": ("Spanish", "Reina-Valera", 1909,
           "Casiodoro de Reina, revised by Cipriano de Valera",
           "The New Testament in Spanish, in the Reina-Valera translation."),
    "fr": ("French", "Darby", None, "John Nelson Darby",
           "The New Testament in French, in the Darby translation. It is the "
           "edition this site's French Old Testament is taken from."),
    "hi": ("Hindi", "Hindi Contemporary Version", 2019, None,
           "The New Testament in Hindi. It is the edition this site's Hindi "
           "Old Testament is taken from."),
    "hy": ("Armenian", "Western Armenian", None, None,
           "The New Testament in Western Armenian."),
    "it": ("Italian", "Riveduta", 1927, "Giovanni Luzzi",
           "The New Testament in Italian, in the Riveduta translation."),
    "ja": ("Japanese", "Raguet-yaku", 1910, "Emile Raguet",
           "The New Testament in Japanese, in the Raguet translation."),
    "ko": ("Korean", "Korean public-domain edition", None, None,
           "The New Testament in Korean."),
    "pt": ("Portuguese", "Biblia Livre", None, None,
           "The New Testament in Portuguese, in the Biblia Livre. It is the "
           "edition this site's Portuguese Old Testament is taken from."),
    "ro": ("Romanian", "Editia Sfantului Sinod", 1914, None,
           "The New Testament in Romanian, in the Holy Synod's edition of "
           "1914, the Orthodox Church of Romania's own. It is the edition "
           "this site's Romanian Old Testament is taken from."),
    "ru": ("Russian", "Russian Synodal Version", 1876, None,
           "The New Testament in Russian, in the Synodal translation."),
    "sr": ("Serbian", "Vuk Karadzic", 1847, "Vuk Karadzic",
           "The New Testament in Serbian, in the translation of Vuk "
           "Karadzic."),
    "sw": ("Swahili", "Maandiko Matakatifu", 2024, None,
           "The New Testament in Swahili. It is the edition this site's "
           "Swahili Old Testament is taken from."),
    "uk": ("Ukrainian", "Panteleimon Kulish", 1871, "Panteleimon Kulish",
           "The New Testament in Ukrainian, in the translation of "
           "Panteleimon Kulish."),
    "zh": ("Chinese", "Chinese Union Version", 1919, None,
           "The New Testament in Chinese, in the Union Version, in "
           "simplified characters."),
    "bn": ("Bengali", "Bengali Contemporary Version", 2022, None,
           "The New Testament in Bengali. It is the edition this site's "
           "Bengali Old Testament is taken from."),
    "ur": ("Urdu", "Urdu Contemporary Version", 2024, None,
           "The New Testament in Urdu. It is the edition this site's Urdu "
           "Old Testament is taken from."),
}


def corpus(html):
    i = html.index("const CORPUS = ")
    j = html.index("\n", i)
    line = html[i:j]
    body = line[len("const CORPUS = "):].rstrip(";")
    return i, j, json.loads(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    p = ROOT / "library.html"
    html = io.open(p, encoding="utf-8").read()
    i, j, c = corpus(html)
    have = {w["work_id"]: w for w in c["works"]}
    changed, added = [], []
    for lang, (name, source, year, translator, desc) in sorted(ENTRIES.items()):
        wid = "bible-" + lang
        if not (ROOT / "data" / ("bible.v3.%s.b64" % lang)).exists():
            if wid in have:
                print("  %s has an entry and no text" % wid)
            continue
        want = {
            "work_id": wid,
            "title": "The New Testament (%s)" % name,
            "author": APOSTLES,
            "translator": translator,
            "pub_year": year,
            "source": source,
            "language": lang,
            "description": desc,
        }
        w = have.get(wid)
        if w is None:
            base = dict(have.get("bible-en", {}))
            base.update(want)
            c["works"].append(base)
            added.append(wid)
            continue
        diff = [k for k, v in want.items() if w.get(k) != v]
        if diff:
            w.update(want)
            changed.append("%s (%s)" % (wid, ", ".join(diff)))
    for x in changed:
        print("  changed %s" % x)
    for x in added:
        print("  added   %s" % x)
    if not (changed or added):
        print("  the entries already say what is published")
        return 0
    if not a.write:
        print("\n(--write to apply)")
        return 1
    line = "const CORPUS = " + json.dumps(c, ensure_ascii=False,
                                          separators=(",", ":")) + ";"
    io.open(p, "w", encoding="utf-8").write(html[:i] + line + html[j:])
    print("\nwrote library.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
