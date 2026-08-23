#!/usr/bin/env python3
"""Spanish and Portuguese read the canon the Church reads.

    python3 tools/ingest_scripture_usfm.py --check es
    python3 tools/ingest_scripture_usfm.py --write es pt

What was published was Reina-Valera for Spanish and the Biblia Livre for
Portuguese: thirty-nine books of the Hebrew canon. A reader in either language
could not open Wisdom, Sirach, Tobit, Judith or the Maccabees at all, and the
Daniel and the Esther he was given were the short ones.

No Orthodox Bible was ever made in either language. docs/BASELINE.md records
the whole search: every free Reina-Valera and every free Almeida is sixty-six
books, the Valera 1602 Purificada included, and neither Spanish nor Portuguese
Wikisource has a whole Bible to take. What exists is two editions that carry
the whole canon, both public domain:

    es   spabll     Santa Biblia libre Latinoamericano
    pt   porbrbsl   Biblia Portuguesa Mundial

The cost is real and is stated rather than hidden: those readers gain the
books the Church reads and lose a translation many of them know by heart.

Both set the Greek Daniel and the Greek Esther as books of their own beside
the Hebrew ones, and both carry Psalm 151 separately. The Church reads the
Greek, so Daniel is the Greek Daniel here and Esther the Greek Esther, and
Psalm 151 is set where the Psalter ends rather than off on its own. Susanna,
Bel and the Song of the Three Youths are not separate books in these editions;
they stand inside Daniel at chapters 13, 14 and 3, which is where the edition
puts them and so where they are left.
"""
import argparse
import io
import json
import re
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "scripture" / "index.json"
CACHE = ROOT / ".cache" / "usfm"
sys.path.insert(0, str(ROOT / "tools"))
UA = {"User-Agent": "plithos.org scripture ingest"}

SHORT = ("The Greek Daniel and the Greek Esther, which the Church reads, "
         "stand here in place of the shorter Hebrew ones; Susanna, Bel and "
         "the Song of the Three Youths are within Daniel, at chapters 13, 14 "
         "and 3, as this edition sets them.")

# lang -> (eBible id, name, autonym, edition, licence, direction)
EDITIONS = {
    "es": ("spabll", "Spanish", "Español",
           "Santa Biblia libre Latinoamericano", "Public Domain", "ltr"),
    "pt": ("porbrbsl", "Portuguese", "Português",
           "Biblia Portuguesa Mundial", "Public Domain", "ltr"),
}

# USFM book code -> the number this site gives the book. Where an edition
# prints both a Hebrew and a Greek form of a book, the Greek is taken, because
# that is the one the Church reads.
BOOKS = [
    ("GEN", 1), ("EXO", 2), ("LEV", 3), ("NUM", 4), ("DEU", 5), ("JOS", 6),
    ("JDG", 7), ("RUT", 8), ("1SA", 9), ("2SA", 10), ("1KI", 11),
    ("2KI", 12), ("1CH", 13), ("2CH", 14), ("EZR", 15), ("NEH", 16),
    ("ESG", 17), ("JOB", 18), ("PSA", 19), ("PRO", 20), ("ECC", 21),
    ("SNG", 22), ("ISA", 23), ("JER", 24), ("LAM", 25), ("EZK", 26),
    ("DAG", 27), ("HOS", 28), ("JOL", 29), ("AMO", 30), ("OBA", 31),
    ("JON", 32), ("MIC", 33), ("NAM", 34), ("HAB", 35), ("ZEP", 36),
    ("HAG", 37), ("ZEC", 38), ("MAL", 39),
    ("1ES", 67), ("2ES", 68), ("TOB", 69), ("JDT", 70), ("WIS", 73),
    ("SIR", 74), ("BAR", 75), ("LJE", 76), ("MAN", 79), ("1MA", 80),
    ("2MA", 81), ("3MA", 82), ("4MA", 83),
]
# Where the Greek form is wanting, the Hebrew stands in its place.
FALLBACK = {"ESG": "EST", "DAG": "DAN"}

PAIRED = ("f", "x", "fig", "fe", "ef", "ex")


def clean(t):
    """The words, without the apparatus.

    USFM carries the footnotes, the cross references and a Strong's number on
    almost every word of these editions. None of that is the translation."""
    for m in PAIRED:                       # notes, references, illustrations
        t = re.sub(r"\\%s\b.*?\\%s\*" % (m, m), " ", t, flags=re.S)
    # \w word|strong="H1234"\w*  ->  word
    t = re.sub(r"\\\+?w\s+([^|\\]*?)(\|[^\\]*?)?\\\+?w\*", r"\1", t)
    # the remaining character styles keep their words and lose their marks
    t = re.sub(r"\\\+?(nd|add|bk|it|bd|em|qt|sc|tl|pn|wj|no|ord|sig|sls|"
               r"dc|k|w)\*?", " ", t)
    t = re.sub(r"\|[^\\]*?(?=\\|$)", " ", t)
    t = re.sub(r"\\[a-z0-9\-]+\*?", " ", t)   # paragraph and title markers
    t = t.replace("\u00a0", " ")
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"\s+([,.;:!?])", r"\1", t).strip()


def get(url, tries=4):
    for i in range(tries):
        try:
            r = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(r, timeout=180) as h:
                return h.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def archive(tid):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / ("%s_usfm.zip" % tid)
    if not p.exists():
        p.write_bytes(get("https://ebible.org/Scriptures/%s_usfm.zip" % tid))
    return zipfile.ZipFile(str(p))


def parse(text):
    """One book, as {chapter: {verse: words}}, in the edition's numbering."""
    out, chap = {}, None
    # \c and \v are the only structure that matters; everything between one
    # \v and the next belongs to that verse however many paragraphs it spans.
    for piece in re.split(r"(\\c\s+\d+|\\v\s+\d+[a-z]?)", text):
        m = re.match(r"\\c\s+(\d+)", piece)
        if m:
            chap = m.group(1)
            out.setdefault(chap, {})
            verse = None
            continue
        m = re.match(r"\\v\s+(\d+)", piece)
        if m:
            verse = m.group(1)
            continue
        if chap is None or not out.get(chap) and verse is None:
            continue
        try:
            if verse:
                got = clean(piece)
                if got:
                    out[chap][verse] = (out[chap].get(verse, "") + " " + got).strip()
        except NameError:
            pass
    return {c: v for c, v in out.items() if v}


def book_text(z, tid, code):
    names = [n for n in z.namelist() if re.search(r"-%s%s\.usfm$" % (code, tid), n)]
    if not names:
        return None, None
    raw = z.read(names[0]).decode("utf-8", "replace")
    title = None
    for line in raw.split("\n")[:20]:
        m = re.match(r"\\(?:toc2|h)\s+(.+?)\s*$", line)
        if m and not title:
            title = m.group(1).strip()
    return parse(raw), (title or code)


def build(lang, write):
    tid, name, autonym, edition, lic, direction = EDITIONS[lang]
    z = archive(tid)
    out = ROOT / "scripture" / lang
    built, total, notes = [], 0, []
    for code, nr in BOOKS:
        chapters, title = book_text(z, tid, code)
        if chapters is None and code in FALLBACK:
            chapters, title = book_text(z, tid, FALLBACK[code])
            if chapters:
                notes.append("%s stands in for %s" % (FALLBACK[code], code))
        if not chapters:
            print("  --    %-5s %2d  not in this edition" % (code, nr))
            continue
        if code == "PSA":
            # Psalm 151 is printed as a book of its own and belongs at the
            # end of the Psalter, which is where the Church reads it.
            extra, _t = book_text(z, tid, "PS2")
            if extra:
                chapters["151"] = extra.get("1", {})
                notes.append("Psalm 151 set at the end of the Psalter")
        top = max(int(c) for c in chapters)
        rows = []
        for c in range(1, top + 1):
            vs = chapters.get(str(c), {})
            hi = max((int(v) for v in vs), default=0)
            rows.append([vs.get(str(v), "") for v in range(1, hi + 1)])
        n = sum(len([v for v in r if v]) for r in rows)
        total += n
        print("  ok    %-5s %2d -> %-26s %3d chapters %7s verses"
              % (code, nr, title[:26], len(rows), format(n, ",")))
        built.append((nr, title, rows))
    print("\n%s: %d books, %s verses" % (lang, len(built), format(total, ",")))
    for x in notes:
        print("  note: %s" % x)
    if not write:
        return
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.json"):
        f.unlink()
    for nr, title, rows in built:
        (out / ("%d.json" % nr)).write_text(
            json.dumps({"l": lang, "b": nr, "n": title, "c": rows},
                       ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    idx["langs"] = [l for l in idx["langs"] if l["code"] != lang]
    idx["langs"].append({
        "code": lang, "name": name, "autonym": autonym,
        "tradition": "septuagint", "edition": edition,
        "license": lic, "dir": direction, "note": SHORT})
    idx["langs"].sort(key=lambda l: l["code"])
    idx["avail"][lang] = sorted(nr for nr, _t, _r in built)
    idx["names"][lang] = {str(nr): t for nr, t, _r in built}
    INDEX.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    import scripture_index
    scripture_index.sync()
    print("wrote %d books and told the index about them" % len(built))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("langs", nargs="*")
    a = ap.parse_args()
    for l in (a.langs or sorted(EDITIONS)):
        print("==", l)
        build(l, a.write)
    return 0


if __name__ == "__main__":
    sys.exit(main())
