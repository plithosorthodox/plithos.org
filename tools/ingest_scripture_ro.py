#!/usr/bin/env python3
"""
The Romanian Old Testament, from the Holy Synod's edition of 1914.

Romania is among the largest of the Orthodox Churches and its saints, its
calendar, its vocabulary and its lives are all written here in Romanian - and
until now a Romanian reader who opened a reading from the Old Testament was
given it in English. Sixteen languages had an Old Testament and Romanian was
not one of them.

The text is BIBLIA, ADICA DUMNEZEEASCA SCRIPTURA A LEGII VECHI SI A CELEI
NOUA, Editia Sfantului Sinod, Bucharest 1914. It is the Orthodox Church of
Romania's own edition, it follows the Septuagint - Facerea 1:1 reads "Intru
inceput au facut Dumnezeu cerul si pamantul", which renders epoiesen ho theos
and not the Hebrew singular - and it carries the whole canon the Church reads,
the deuterocanonical books with it. Printed in 1914, it is long out of
copyright.

    python3 tools/ingest_scripture_ro.py --check
    python3 tools/ingest_scripture_ro.py --write

Why not the others that were offered. The 1982 Bible is the Patriarchate's and
is in copyright, whatever a wiki may be hosting; Cornilescu's of 1921 is a
Protestant translation from the Hebrew and its author died in 1975, so it is
in copyright too and would not belong here in any case. The Bucharest Bible of
1688 is free and Orthodox and was the other real candidate; 1914 was preferred
because it is the Synod's own and its Romanian is the Romanian the rest of
this site is written in.
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripture" / "ro"
INDEX = ROOT / "scripture" / "index.json"
CACHE = Path("/tmp/plithos-ro-bible")
CACHE.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
BASE = "Biblia 1914"

# The Synod's own names for the books, against the numbers this site gives
# them. These are read off the edition's table of contents and not guessed:
# guessing them first cost twenty-two books, which failed as "the page is not
# there" while the pages sat there under names slightly different from the
# ones assumed - Paralipomene and not Paralipomena, Tovit and not Tobit,
# Macavei and not Macabei, Estir, Pilde, Ionà, Malahia, Manasì. CLAUDE.md says
# to take the structure from the source's own contents rather than hand-listing
# it, and says it because tools/ingest_canons.py lost seven councils the same
# way. This is that mistake made a second time and corrected the same way.
#
# The New Testament is not taken. Romanian already has one here.
BOOKS = {
    "Facerea": 1, "Eșirea": 2, "Leviticul": 3, "Numerii": 4, "A doua lege": 5,
    "Isus Navì": 6, "Judecătorii": 7, "Rut": 8,
    "1 Împărați": 9, "2 Împărați": 10, "3 Împărați": 11, "4 Împărați": 12,
    "1 Paralipomene": 13, "2 Paralipomene": 14,
    "Esdra": 15, "Neemia": 16, "Estir": 17,
    "Iov": 18, "Psaltirea": 19, "Pilde": 20,
    "Eclisiastul": 21, "Cântarea cântărilor": 22,
    "Isaia": 23, "Ieremia": 24, "Plângerile Ieremiei": 25, "Iezechiil": 26,
    "Daniil": 27, "Osie": 28, "Ioil": 29, "Amos": 30, "Avdie": 31, "Ionà": 32,
    "Miheea": 33, "Naum": 34, "Avacum": 35, "Sofonie": 36, "Agheu": 37,
    "Zaharia": 38, "Malahia": 39,
    # The books read with the Old Testament. Three were identified by their
    # own first words rather than by their titles, because the titles this
    # edition gives them do not say which book they are:
    #   "3 Esdra" opens "Si a adus Iosiea pastile in Ierusalim", which is
    #     Josiah keeping the passover, so it is 1 Esdras and not 4 Ezra.
    #   "Cartea Ieremiei" opens "Isvodul cartei, care a trimis Ieremiea catre
    #     cei ce erau sa se duca robiti in Vavilon" - the copy of the letter -
    #     so it is the Letter of Jeremiah and not a second Jeremiah.
    "3 Esdra": 67, "Tovit": 69, "Iudita": 70,
    "Înțelepciunea lui Solomon": 73, "Sirah": 74,
    "Varuh": 75, "Cartea Ieremiei": 76,
    "Susana": 77,
    "Istoria omorîrei balaurului și a sfărâmării lui Vil": 78,
    "Rugăciunea lui Manasì": 79,
    "1 Macavei": 80, "2 Macavei": 81, "3 Macavei": 82,
}

# "Cantarea celor trei tineri" - the Prayer of Azariah and the Song of the
# Three Youths - is printed as a book of its own in this edition and is not
# one in the scheme this site uses, where it belongs to the third chapter of
# Daniel. It is left out rather than given a number it does not have.

# The Psalter heads its chapters PSALMUL and every other book CAP., and the
# hundred and fifty-first psalm is headed NECANONIC besides - which the
# Church reads, so it is taken like the rest.
CHAPTER = re.compile(
    r"^==+\s*(?:CAP\.?|PSALMUL(?:\s+NECANONIC)?)\s*(\d+)\s*\.?\s*==+\s*$", re.M)
VERSE = re.compile(r'<span id="(\d+)\.(\d+)"\s*/?>')


def fetch(page):
    slug = re.sub(r"[^\w]+", "-", page, flags=re.U).strip("-")
    p = CACHE / (slug + ".json")
    if not p.exists():
        url = ("https://ro.wikisource.org/w/api.php?action=parse&page=%s"
               "&prop=wikitext&format=json&formatversion=2"
               % urllib.parse.quote(page))
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    p.write_bytes(r.read())
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(15 * (attempt + 1))
        time.sleep(2)
    d = json.loads(p.read_text(encoding="utf-8"))
    if "error" in d:
        return None
    return d["parse"]["wikitext"]


def clean(s):
    """The verse, without the apparatus printed beside it.

    The edition sets cross references in a right-aligned block against each
    verse and marks the chapter's subject in a centred line above it. Both
    belong to the page and not to the words, and both come out."""
    s = re.sub(r"<div[^>]*>.*?</div>", " ", s, flags=re.S)
    s = re.sub(r"<center>.*?</center>", " ", s, flags=re.S)
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    s = re.sub(r"\[\[(?:[^]|]*\|)?([^]]*)\]\]", r"\1", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"'''?", "", s)
    s = re.sub(r"[ \t ]+", " ", s)
    return s.strip(" \n—-")


def book(name):
    """One book, as chapters of verses."""
    w = fetch("%s/%s" % (BASE, name))
    if w is None:
        return None, "the page is not there"
    parts = CHAPTER.split(w)
    if len(parts) < 3:
        return None, "no chapter headings"
    chapters = {}
    for i in range(1, len(parts) - 1, 2):
        n, body = int(parts[i]), parts[i + 1]
        marks = list(VERSE.finditer(body))
        if not marks:
            continue
        verses = {}
        for j, m in enumerate(marks):
            end = marks[j + 1].start() if j + 1 < len(marks) else len(body)
            num = int(m.group(2))
            text = clean(body[m.end():end])
            # The edition sets the verse number at the head of the verse. It
            # is the page's furniture, not the words, and the file keeps its
            # verses by position, so a number left in would be printed twice.
            # Only the number this verse actually is comes off: a figure that
            # happens to open a verse and is not its own number stays.
            text = re.sub(r"^%d\s*[.)]\s*" % num, "", text)
            if text:
                verses[num] = text
        if verses:
            # Kept in the edition's own numbering, and a gap left as a gap:
            # a verse the Synod did not print is not one to invent, and the
            # chapter must not silently shift by one because of it.
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
    ap.add_argument("--only", help="one book, by its Romanian name")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    want = {a.only: BOOKS[a.only]} if a.only else BOOKS
    built, failed, verses = [], [], 0
    for name, nr in sorted(want.items(), key=lambda kv: kv[1]):
        chapters, err = book(name)
        if err:
            failed.append((name, err))
            print("  FAIL  %-30s %s" % (name, err))
            continue
        n = sum(len([v for v in c if v]) for c in chapters)
        verses += n
        print("  ok    %-30s %3d ->  %3d chapters  %6s verses"
              % (name, nr, len(chapters), format(n, ",")))
        built.append((name, nr, chapters))

    print("\n%d books, %s verses" % (len(built), format(verses, ",")))
    if failed:
        print("not built: %s" % ", ".join(n for n, _ in failed))

    if a.write:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, nr, chapters in built:
            OUT.joinpath("%d.json" % nr).write_text(
                json.dumps({"l": "ro", "b": nr, "n": name, "c": chapters},
                           ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8")
        idx = json.loads(INDEX.read_text(encoding="utf-8"))
        idx["langs"] = [l for l in idx["langs"] if l["code"] != "ro"]
        idx["langs"].append({
            "code": "ro", "name": "Romanian", "autonym": "Română",
            "tradition": "septuagint",
            "edition": "Ediția Sfântului Sinod (1914)",
            "license": "Public Domain", "dir": "ltr"})
        idx["langs"].sort(key=lambda l: l["code"])
        idx["avail"]["ro"] = sorted(nr for _n, nr, _c in built)
        idx["names"]["ro"] = {str(nr): name for name, nr, _c in built}
        INDEX.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
        print("wrote %d books and told the index about them" % len(built))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
