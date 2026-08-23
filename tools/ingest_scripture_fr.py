#!/usr/bin/env python3
"""The French Old Testament, from the Septuagint.

    python3 tools/ingest_scripture_fr.py --check
    python3 tools/ingest_scripture_fr.py --write

What was published here was Darby: a translation from the Hebrew, made by a
Plymouth Brother, carrying the thirty-nine books of the Hebrew canon and no
others. A French reader could not open Wisdom, or Sirach, or Tobit, or the
Maccabees at all, and what he could open was not the text the Church reads.

This is Pierre Giguet's translation of the Septuagint, Paris 1872, made from
the Sixtine edition of 1587. It is the Greek Old Testament the Church has
always read, in French, and it carries the books that go with it. Giguet died
in 1873; the edition is long out of copyright, and French Wikisource has
transcribed and proofread the whole of it from the scans of all four volumes.

The New Testament is not taken from here. French already reads Darby's New
Testament, which is a translation from the Greek and is not the same objection.
"""
import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripture" / "fr"
INDEX = ROOT / "scripture" / "index.json"
CACHE = Path("/tmp/plithos-fr-bible")
CACHE.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
BASE = "Traduction de la Septante et du Nouveau Testament"

# Giguet's own names for the books, against the numbers this site gives them,
# read off the edition's own list of subpages and not guessed. He follows the
# Septuagint throughout, so the four books of Kingdoms are I to IV Rois and
# not Samuel and Kings; two subpages named I Samuel and II Samuel exist and
# are empty, and are not these books.
#
# He gives Esdras and Nehemie, which is the Septuagint's Esdras B divided as
# the Church divides it, and does not print Esdras A. There is therefore no
# book 67 in French, and saying so is better than putting something else there.
BOOKS = {
    "Genèse": 1, "Exode": 2, "Lévitique": 3, "Nombres": 4, "Deutéronome": 5,
    "Josué": 6, "Juges": 7, "Ruth": 8,
    "I Rois": 9, "II Rois": 10, "III Rois": 11, "IV Rois": 12,
    "I Chroniques": 13, "II Chroniques": 14, "Esdras": 15, "Néhémie": 16,
    "Esther": 17, "Job": 18, "Psaumes": 19, "Proverbes": 20,
    "Ecclésiaste": 21, "Cantique": 22, "Isaïe": 23, "Jérémie": 24,
    "Lamentations": 25, "Ezéchiel": 26, "Daniel": 27, "Osée": 28,
    "Joel": 29, "Amos": 30, "Abdias": 31, "Jonas": 32, "Michée": 33,
    "Nahum": 34, "Habacuc": 35, "Sophonie": 36, "Aggée": 37,
    "Zacharie": 38, "Malachie": 39,
    "Tobit": 69, "Judith": 70, "Sagesse": 73, "Ecclésiastique": 74,
    "Baruch": 75, "Lettre de Jérémie": 76, "Suzanne": 77,
    "Bel et le dragon": 78, "I Machabées": 80, "II Machabées": 81,
}

# The edition heads its chapters in Roman numerals, and the Psalter says
# PSAUME where the rest say CHAPITRE.
HEAD = re.compile(
    r'<h[23][^>]*>\s*(?:CHAPITRE|PSAUME|CHAP\.)\s*([IVXLCDM]+)\s*</h[23]>',
    re.I)
PARA = re.compile(r'<p[^>]*>(.*?)</p>', re.S)
VERSE = re.compile(r'^\s*(\d+)\s*[. ]\s*(.+)$', re.S)
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman(s):
    n = 0
    for i, c in enumerate(s.upper()):
        v = ROMAN[c]
        n += -v if i + 1 < len(s) and ROMAN[s[i + 1].upper()] > v else v
    return n


def fetch(page):
    slug = re.sub(r"[^\w]+", "-", page, flags=re.U).strip("-")
    p = CACHE / (slug + ".json")
    if not p.exists():
        url = ("https://fr.wikisource.org/w/api.php?action=parse&page=%s"
               "&prop=text&format=json&formatversion=2"
               % urllib.parse.quote(page))
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        for attempt in range(8):
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    p.write_bytes(r.read())
                break
            except Exception:
                if attempt == 7:
                    raise
                time.sleep(20 * (attempt + 1))
        time.sleep(4)
    d = json.loads(p.read_text(encoding="utf-8"))
    if "error" in d:
        return None
    return d["parse"]["text"]


def clean(s):
    """The verse, without the page's furniture.

    Wikisource marks where each leaf of the scan begins, sets the running
    heads and the editor's notes apart, and links the notes into the text.
    None of that is Giguet's words."""
    s = re.sub(r"<span[^>]*class=\"[^\"]*pagenum[^\"]*\"[^>]*>.*?</span>",
               " ", s, flags=re.S)
    s = re.sub(r"<sup[^>]*>.*?</sup>", " ", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace(" ", " ").replace("​", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def book(name):
    """One book, as chapters of verses."""
    t = fetch("%s/%s" % (BASE, name))
    if t is None:
        return None, "the page is not there"
    parts = HEAD.split(t)
    if len(parts) < 3:
        return None, "no chapter headings"
    chapters = {}
    for i in range(1, len(parts) - 1, 2):
        n, body = roman(parts[i]), parts[i + 1]
        verses = {}
        for para in PARA.findall(body):
            txt = clean(para)
            if not txt:
                continue
            m = VERSE.match(txt)
            if not m:
                continue
            verses[int(m.group(1))] = m.group(2).strip()
        if verses:
            # The edition's own numbering, with a gap left as a gap.
            top = max(verses)
            chapters[n] = [verses.get(k, "") for k in range(1, top + 1)]
    if not chapters:
        return None, "chapters found but no verses in them"
    top = max(chapters)
    return [chapters.get(k, []) for k in range(1, top + 1)], None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True
    want = {a.only: BOOKS[a.only]} if a.only else BOOKS
    built, failed, verses = [], [], 0
    for name, nr in sorted(want.items(), key=lambda kv: kv[1]):
        chapters, err = book(name)
        if err:
            failed.append((name, err))
            print("  FAIL  %-24s %s" % (name, err))
            continue
        n = sum(len([v for v in c if v]) for c in chapters)
        verses += n
        print("  ok    %-24s %2d -> %3d chapters %7s verses"
              % (name, nr, len(chapters), format(n, ",")))
        built.append((name, nr, chapters))
    print("\n%d books, %s verses" % (len(built), format(verses, ",")))
    if failed:
        print("not built: %s" % ", ".join(n for n, _ in failed))
    if not a.write:
        return 1 if failed else 0
    OUT.mkdir(parents=True, exist_ok=True)
    for name, nr, chapters in built:
        OUT.joinpath("%d.json" % nr).write_text(
            json.dumps({"l": "fr", "b": nr, "n": name, "c": chapters},
                       ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    idx["langs"] = [l for l in idx["langs"] if l["code"] != "fr"]
    idx["langs"].append({
        "code": "fr", "name": "French", "autonym": "Français",
        "tradition": "septuagint",
        "edition": "Giguet, d'apres les Septante (1872)",
        "license": "Public Domain", "dir": "ltr"})
    idx["langs"].sort(key=lambda l: l["code"])
    on_disk = {int(f.stem) for f in OUT.glob("*.json")}
    avail = {nr for _n, nr, _c in built} & on_disk
    idx["avail"]["fr"] = sorted(avail)
    names = dict(idx["names"].get("fr", {}))
    for name, nr, _c in built:
        names[str(nr)] = name
    idx["names"]["fr"] = {k: v for k, v in sorted(names.items(), key=lambda kv: int(kv[0]))}
    INDEX.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    import scripture_index
    scripture_index.sync()
    print("wrote %d books and told the index about them" % len(built))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
