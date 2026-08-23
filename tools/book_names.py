#!/usr/bin/env python3
"""What each language calls the books, so the navigation can be read.

    python3 tools/book_names.py --check
    python3 tools/book_names.py --write

The buttons that carry a reader from one book to the next are the site
speaking, not the edition, so they are labelled in the language the site is
set to. That only works if the site knows what the books are called in that
language. A Georgian reader opening the Old Testament was given his headings
in Georgian and every book beside them named in English.

The names are not invented here. Each is taken from the edition that language
reads, which is the one authority for what it calls its own books.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from ingest_nt import cached                     # noqa: E402
from nt_sources import SOURCES, NT_ORDER         # noqa: E402
from book_names_table import FULL_OT, DEUTERO, NT   # noqa: E402

INDEX = ROOT / "scripture" / "index.json"


def apply_ot(write):
    """The Old Testament names, in every language offered here.

    The ingesters write this table from each edition's own book titles, which
    is right as far as it goes and goes only as far as the books that edition
    carries. Everything else is here, and this is applied after any ingest -
    an ingest will overwrite what it knows about and leave the rest alone.
    """
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    names = idx["names"]
    changed = {}
    for lang, table in list(FULL_OT.items()) + list(DEUTERO.items()):
        have = names.setdefault(lang, {})
        for nr, name in table.items():
            if have.get(str(nr)) != name:
                changed[lang] = changed.get(lang, 0) + 1
                have[str(nr)] = name
    for lang in sorted(changed):
        print("  %-4s %3d Old Testament names" % (lang, changed[lang]))
    if changed and write:
        for lang in names:
            names[lang] = {k: names[lang][k]
                           for k in sorted(names[lang], key=int)}
        INDEX.write_text(json.dumps(idx, ensure_ascii=False),
                         encoding="utf-8")
        import scripture_index
        scripture_index.sync()
        print("  wrote scripture/index.json and index.v2.json")
    return bool(changed)


def helloao_names(tid):
    d = cached("%s.books" % tid,
               "https://bible.helloao.org/api/%s/books.json" % tid)
    return {b["id"]: b.get("name") for b in (d or {}).get("books", [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    ot = apply_ot(a.write)

    p = ROOT / "library.html"
    s = io.open(p, encoding="utf-8").read()
    i = s.index("NT_BOOK_NAMES")
    j = s.index("=", i)
    k = s.index("\n", j)
    table = json.loads(s[j + 1:k].rstrip(";"))

    changed = []
    for lang, src in sorted(SOURCES.items()):
        if src[0] != "helloao":
            continue                     # only the editions that name their own
        names = helloao_names(src[1])
        want = {}
        for book, _nr, code in NT_ORDER:
            n = names.get(code)
            if n:
                want[book] = n
        if len(want) != len(NT_ORDER):
            print("  %s: the edition names %d of %d books, not taken"
                  % (lang, len(want), len(NT_ORDER)))
            continue
        # Added, never replaced. What is already written is in the language
        # a reader of the site would use and is cased for reading: Greek
        # stands as "Kata Matthaion" where the edition prints its title in
        # majuscules throughout, and Hindi keeps the names a Hindi Christian
        # knows rather than the ones this particular edition coined. A name
        # already here was chosen; this only fills in the languages that have
        # none.
        if lang in table:
            continue
        changed.append("%s (%d names, from the edition it reads)"
                       % (lang, len(want)))
        table[lang] = want

    for lang, want in sorted(NT.items()):
        if table.get(lang) != want:
            changed.append("%s (%d New Testament names)" % (lang, len(want)))
            table[lang] = want
    for x in changed:
        print("  %s" % x)
    missing = [l for l in sorted(SOURCES) if l not in table and l != "en"]
    if missing:
        print("  still named only in English: %s" % ", ".join(missing))
    if not changed:
        print("  the New Testament table already says what the editions say")
        return 0 if not ot or a.write else 1
    if not a.write:
        print("\n(--write to apply)")
        return 1
    line = "=" + json.dumps(table, ensure_ascii=False,
                            separators=(",", ":")) + ";"
    io.open(p, "w", encoding="utf-8").write(s[:j] + line + s[k:])
    print("\nwrote library.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
