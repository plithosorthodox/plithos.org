#!/usr/bin/env python3
"""
Give the books of the Bible their names in the language they are read in.

A reader who opened the Greek Old Testament found its group headings in
Greek, its chapter label in Greek, and its books listed as Genesis, Exodus,
Leviticus. The names in scripture/index.json were English for forty-two of
the fifty-one Greek books, thirty-nine of the forty-eight Church Slavonic,
and thirty-two each of the Serbian, Ukrainian and Japanese; the New Testament
had no names but English in any of its nineteen languages, because its
bundles are keyed by the English book name and nothing else was ever written.

Names are curated here, one entry per book, and every one of them is checked
against a real edition before it is written. The attestation is a page that
lists the books of the Bible in that language - its own table of contents,
in effect - fetched and cached. A name that does not occur there fails the
run. That is the whole point: a book's name in Greek or Slavonic is a fact
about an edition, not something to be supplied from memory, and this file
would be the easiest place on the site to quietly invent one.

Where the edition prints a qualifier the shelf does not need - Wikisource
distinguishes the two Greek Daniels, Theodotion's and the Seventy's - the
name is attested by its opening rather than in full, and the qualifier is
dropped. That is the only latitude allowed.

    python3 tools/book_names.py --check
    python3 tools/book_names.py --write
"""
import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "scripture" / "index.json"
READER = ROOT / "library.html"
CACHE = Path("/tmp/plithos-booknames")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"

# Where each language's book names are read from. A page that lists the books
# of the Bible in that language; the text of it is the attestation corpus.
ATTEST = {
    "el": [("el.wikisource.org", "Παλαιά Διαθήκη (Rahlfs)"),
           ("el.wikisource.org", "Η Αγία Γραφή"),
           ("el.wikipedia.org", "Παλαιά Διαθήκη"),
           ("el.wikipedia.org", "Καινή Διαθήκη"),
           ("el.wikipedia.org",
            "Κατάλογος των βιβλίων της Αγίας Γραφής σύμφωνα με την "
            "Ορθόδοξη Εκκλησία")],
    "uk": [("uk.wikisource.org", "Біблія (Огієнко)")],
}

# Old Testament: the site's book number -> the name the edition gives it.
OT = {
    "el": {
        1: "Γένεσις", 2: "Έξοδος", 3: "Λευϊτικόν", 4: "Αριθμοί",
        5: "Δευτερονόμιον", 6: "Ιησούς του Ναυή", 7: "Κριταί", 8: "Ρουθ",
        9: "Βασιλειών Α'", 10: "Βασιλειών Β'", 11: "Βασιλειών Γ'",
        12: "Βασιλειών Δ'", 13: "Παραλειπομένων Α'", 14: "Παραλειπομένων Β'",
        15: "Έσδρας Β'", 16: "Νεεμίας", 17: "Εσθήρ", 18: "Ιώβ", 19: "Ψαλμοί",
        20: "Παροιμίαι", 21: "Εκκλησιαστής", 22: "Άσμα Ασμάτων",
        23: "Ησαΐας", 24: "Ιερεμίας", 25: "Θρήνοι Ιερεμίου", 26: "Ιεζεκιήλ",
        27: "Δανιήλ", 28: "Ωσηέ", 29: "Ιωήλ", 30: "Αμώς", 31: "Οβδίας",
        32: "Ιωνάς", 33: "Μιχαίας", 34: "Ναούμ", 35: "Αμβακούμ",
        36: "Σοφονίας", 37: "Αγγαίος", 38: "Ζαχαρίας", 39: "Μαλαχίας",
        67: "Έσδρας Α'", 69: "Τωβίτ", 70: "Ιουδίθ", 73: "Σοφία Σολομώντος",
        74: "Σοφία Σειράχ", 75: "Βαρούχ", 76: "Επιστολή Ιερεμίου",
        77: "Σουσάννα", 78: "Βηλ και Δράκων",
        80: "Μακκαβαίων Α'", 81: "Μακκαβαίων Β'", 82: "Μακκαβαίων Γ'",
        83: "Μακκαβαίων Δ'",
    },
    "uk": {
        1: "Перша книга Мойсеєва: Буття",
        2: "Друга книга Мойсеєва: Вихід",
        3: "Третя книга Мойсеєва: Левит",
        4: "Четверта книга Мойсеєва: Числа",
        5: "П'ята книга Мойсеєва: Повторення Закону",
        6: "Книга Ісуса Навина", 7: "Книга Суддів", 8: "Книга Рут",
        9: "Перша книга Самуїлова", 10: "Друга книга Самуїлова",
        11: "Перша книга царів", 12: "Друга книга царів",
        13: "Перша книга хроніки", 14: "Друга книга хроніки",
        15: "Книга Ездри", 16: "Книга Неемії", 17: "Книга Естер",
        18: "Книга Йова", 19: "Книга Псалмів",
        20: "Книга приказок Соломонових", 21: "Книга Екклезіястова",
        22: "Пісня над піснями", 23: "Книга пророка Ісаї",
        24: "Книга пророка Єремії", 25: "Плач Єремії",
        26: "Книга пророка Єзекіїля", 27: "Книга пророка Даниїла",
        28: "Книга пророка Осії", 29: "Книга пророка Йоіла",
        30: "Книга пророка Амоса", 31: "Книга пророка Овдія",
        32: "Книга пророка Йони", 33: "Книга пророка Михея",
        34: "Книга пророка Наума", 35: "Книга пророка Авакума",
        36: "Книга пророка Софонії", 37: "Книга пророка Огія",
        38: "Книга пророка Захарія", 39: "Книга пророка Малахії",
    },
}

# New Testament: the key the bundles use -> the name the edition gives it.
NT = {
    "el": {
        "Matthew": "Κατά Ματθαίον", "Mark": "Κατά Μάρκον",
        "Luke": "Κατά Λουκάν", "John": "Κατά Ιωάννην",
        "Acts": "Πράξεις των Αποστόλων", "Romans": "Προς Ρωμαίους",
        "1 Corinthians": "Προς Κορινθίους Α'",
        "2 Corinthians": "Προς Κορινθίους Β'",
        "Galatians": "Προς Γαλάτας", "Ephesians": "Προς Εφεσίους",
        "Philippians": "Προς Φιλιππησίους", "Colossians": "Προς Κολοσσαείς",
        "1 Thessalonians": "Προς Θεσσαλονικείς Α'",
        "2 Thessalonians": "Προς Θεσσαλονικείς Β'",
        "1 Timothy": "Προς Τιμόθεον Α'", "2 Timothy": "Προς Τιμόθεον Β'",
        "Titus": "Προς Τίτον", "Philemon": "Προς Φιλήμονα",
        "Hebrews": "Προς Εβραίους", "James": "Ιακώβου",
        "1 Peter": "Πέτρου Α'", "2 Peter": "Πέτρου Β'",
        "1 John": "Ιωάννου Α'", "2 John": "Ιωάννου Β'",
        "3 John": "Ιωάννου Γ'", "Jude": "Ιούδα",
        "Revelation": "Αποκάλυψις Ιωάννου",
    },
    "uk": {
        "Matthew": "Євангелія від св. Матвія",
        "Mark": "Євангелія від св. Марка",
        "Luke": "Євангелія від св. Луки",
        "John": "Євангелія від св. Івана",
        "Acts": "Дії святих апостолів",
        "Romans": "Послання св. апостола Павла до римлян",
        "1 Corinthians": "Перше послання св. апостола Павла до коринтян",
        "2 Corinthians": "Друге послання св. апостола Павла до коринтян",
        "Galatians": "Послання св. апостола Павла до галатів",
        "Ephesians": "Послання св. апостола Павла до ефесян",
        "Philippians": "Послання св. апостола Павла до филип'ян",
        "Colossians": "Послання св. апостола Павла до колосян",
        "1 Thessalonians": "Перше послання св. апостола Павла до солунян",
        "2 Thessalonians": "Друге послання св. апостола Павла до солунян",
        "1 Timothy": "Перше послання св. апостола Павла до Тимофія",
        "2 Timothy": "Друге послання св. апостола до Тимофія",
        "Titus": "Послання св. апостола Павла до Тита",
        "Philemon": "Послання св. апостола Павла до Филимона",
        "Hebrews": "Послання до євреїв",
        "James": "Соборне послання св. апостола Якова",
        "1 Peter": "Перше соборне послання св. апостола Петра",
        "2 Peter": "Друге соборне послання св. апостола Петра",
        "1 John": "Перше соборне послання св. апостола Івана",
        "2 John": "Друге соборне послання св. апостола Івана",
        "3 John": "Третє соборне послання св. апостола Івана",
        "Jude": "Соборне послання св. апостола Юди",
        "Revelation": "Об'явлення св. Івана Богослова",
    },
}


def fetch(host, page):
    key = re.sub(r"\W+", "_", host + "_" + page)[:80] + ".json"
    p = CACHE / key
    if not p.exists():
        q = urllib.parse.urlencode({"action": "parse", "prop": "text|links",
                                    "page": page, "redirects": "1",
                                    "format": "json"})
        req = urllib.request.Request("https://%s/w/api.php?%s" % (host, q),
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            p.write_bytes(r.read())
        time.sleep(0.3)
    return json.loads(p.read_text(encoding="utf-8"))


def corpus(lang):
    """Everything the attesting pages say, as one string."""
    out = []
    for host, page in ATTEST[lang]:
        d = fetch(host, page)
        if "parse" not in d:
            raise SystemExit("%s: %s did not answer" % (lang, page))
        out.append(re.sub(r"<[^>]+>", " ", d["parse"]["text"]["*"]))
        out.extend(l["*"] for l in d["parse"].get("links", []))
    return norm(" ".join(out))


def norm(s):
    """Compared without accents.

    Editions differ over the accentuation of the same name - one prints
    Λευϊτικόν and another Λευιτικόν, one Ἀμβακούμ and another Ἀββακούμ - and
    the stored name keeps whatever this edition writes. The comparison is
    what has to be forgiving, not the text.
    """
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("’", "'").replace("΄", "'").replace("᾽", "'")
    return re.sub(r"\s+", " ", s).lower()


def attested(name, hay):
    n = norm(name)
    if n in hay:
        return True
    # Wikisource tells the two Greek Daniels apart in the page title; the
    # shelf has one Daniel and takes the name without the qualifier.
    return (n + " (") in hay


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    english = idx["names"]["en"]
    bad, changed = [], 0

    for lang in sorted(set(list(OT) + list(NT))):
        hay = corpus(lang)
        for nr, name in sorted(OT.get(lang, {}).items()):
            if not attested(name, hay):
                bad.append("%s Old Testament %s: %r is not in the edition"
                           % (lang, nr, name))
        for book, name in sorted(NT.get(lang, {}).items()):
            if not attested(name, hay):
                bad.append("%s New Testament %s: %r is not in the edition"
                           % (lang, book, name))
        ot, nt = OT.get(lang, {}), NT.get(lang, {})
        left = [nr for nr in idx["avail"].get(lang, [])
                if nr not in ot and english.get(str(nr))]
        print("%-4s %2d of %d Old Testament books, %2d of 27 in the New%s"
              % (lang, len(ot), len(idx["avail"].get(lang, [])), len(nt),
                 ";  still English: %s" % ", ".join(english[str(n)] for n in left[:6])
                 if left else ""))

    if bad:
        print("\n%d name(s) not found in the edition they claim:" % len(bad))
        for b in bad:
            print("   %s" % b)
        return 1

    # What the shelf would still show in English.
    for lang, names in idx["names"].items():
        if lang == "en":
            continue
        same = [k for k, v in names.items() if english.get(k) == v
                and k not in {str(n) for n in OT.get(lang, {})}]
        if same:
            print("  %-4s %d Old Testament books still read in English" %
                  (lang, len(same)))

    if args.write:
        for lang, names in OT.items():
            tgt = idx["names"].setdefault(lang, {})
            for nr, name in names.items():
                if tgt.get(str(nr)) != name:
                    tgt[str(nr)] = name
                    changed += 1
        INDEX.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
        src = READER.read_text(encoding="utf-8")
        line = "const NT_BOOK_NAMES=" + json.dumps(NT, ensure_ascii=False,
                                                   separators=(",", ":")) + ";"
        if "const NT_BOOK_NAMES=" in src:
            src = re.sub(r"const NT_BOOK_NAMES=.*?;\n", line + "\n", src,
                         count=1, flags=re.S)
        else:
            anchor = "const unitsByWork = {};"
            src = src.replace(anchor, line + "\n" + anchor, 1)
        READER.write_text(src, encoding="utf-8")
        print("\nwrote %d Old Testament names and the New Testament table"
              % changed)
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
