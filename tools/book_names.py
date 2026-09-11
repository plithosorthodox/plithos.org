# -*- coding: utf-8 -*-
"""The books of Scripture, named in the reader's own language.

The calendar prints the day's readings as references - "Matt. 5:1-12;
Heb. 11:33-40" - and localises the book with BOOK_I18N in index.html.
That table stood in seven languages, so a reader in the other fourteen
met a wholly translated page with English book names in the middle of it.

Nothing here is composed. The site already publishes every one of these
names, in two places:

    library.html        NT_BOOK_NAMES, the twenty-seven books of the New
                        Testament in all twenty-two languages, taken from
                        each language's own edition
    scripture/index.json  the "names" table, fifty-five Old Testament
                        books in twenty-three languages, likewise

This reads both and fills the gaps. It never overwrites a name that is
already there.

    python3 tools/book_names.py            report
    python3 tools/book_names.py --write    fill them in

Chinese is the one language that needs a hand. The site is published in
simplified Chinese - LANG_NAMES calls it 简体中文, the scriptures are
simplified, and the saints' lives write 马太福音 - but NT_BOOK_NAMES was
entered in traditional characters. The same names in the site's own
script are below, and they are written back to library.html too, so the
Library stops labelling a simplified text with traditional headings.
"""

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
LIBRARY = os.path.join(ROOT, "library.html")
SCRIPTURE = os.path.join(ROOT, "scripture", "index.json")

# The abbreviation the lectionary prints -> the book it stands for.
NT = {
    "Matt.": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John",
    "Acts": "Acts", "Rom.": "Romans", "1 Cor.": "1 Corinthians",
    "2 Cor.": "2 Corinthians", "Gal.": "Galatians", "Eph.": "Ephesians",
    "Phil.": "Philippians", "Col.": "Colossians", "Heb.": "Hebrews",
    "Titus": "Titus", "James": "James", "1 Pet.": "1 Peter",
    "2 Pet.": "2 Peter", "1 Tim.": "1 Timothy", "2 Tim.": "2 Timothy",
    "1 Thess.": "1 Thessalonians", "2 Thess.": "2 Thessalonians",
    "Jude": "Jude", "Rev.": "Revelation", "1 John": "1 John",
    "2 John": "2 John", "3 John": "3 John",
}

# The same, against the book numbers scripture/index.json uses. The four
# books of Kingdoms are what the lectionary calls Samuel and Kings.
OT = {
    "Gen.": 1, "Ex.": 2, "Lev.": 3, "Num.": 4,
    "1 Sam.": 9, "2 Sam.": 10, "1 Kgs.": 11, "2 Kgs.": 12,
    "Est.": 17, "Prov.": 20, "Isa.": 23, "Jer.": 24, "Ezek.": 26,
    "Dan.": 27, "Hos.": 28, "Joel": 29, "Jon.": 32, "Mal.": 39,
    "Jth.": 70, "Sir.": 74,
}

# Traditional as entered -> the same name in the script the site publishes.
ZH = {
    "馬太福音": "马太福音", "馬可福音": "马可福音", "路加福音": "路加福音",
    "約翰福音": "约翰福音", "使徒行傳": "使徒行传", "羅馬書": "罗马书",
    "哥林多前書": "哥林多前书", "哥林多後書": "哥林多后书",
    "加拉太書": "加拉太书", "以弗所書": "以弗所书", "腓立比書": "腓立比书",
    "歌羅西書": "歌罗西书", "帖撒羅尼迦前書": "帖撒罗尼迦前书",
    "帖撒羅尼迦後書": "帖撒罗尼迦后书", "提摩太前書": "提摩太前书",
    "提摩太後書": "提摩太后书", "提多書": "提多书", "腓利門書": "腓利门书",
    "希伯來書": "希伯来书", "雅各書": "雅各书", "彼得前書": "彼得前书",
    "彼得後書": "彼得后书", "約翰壹書": "约翰壹书", "約翰貳書": "约翰贰书",
    "約翰參書": "约翰叁书", "猶大書": "犹大书", "啟示錄": "启示录",
}


def literal(text, name):
    """The whole of a brace-balanced assignment, and where it sits."""
    i = text.find(name)
    if i < 0:
        raise SystemExit("%s is not in the page" % name)
    start = text.index("{", i)
    depth = 0
    for k in range(start, len(text)):
        if text[k] == "{":
            depth += 1
        elif text[k] == "}":
            depth -= 1
            if not depth:
                return start, k + 1
    raise SystemExit("%s never closes" % name)


def read_books():
    lib = io.open(LIBRARY, encoding="utf-8").read()
    a, b = literal(lib, "NT_BOOK_NAMES")
    nt = json.loads(lib[a:b])
    ot = json.load(io.open(SCRIPTURE, encoding="utf-8"))["names"]
    return nt, ot


def collides(names):
    """lz() replaces one abbreviation at a time, longest first.

    A rendering that contains a shorter abbreviation would be caught by
    the next round and mangled. Nothing does today; this is here so that
    nothing does tomorrow either.
    """
    order = sorted(names, key=len, reverse=True)
    bad = []
    for n, key in enumerate(order):
        for later in order[n + 1:]:
            if later in names[key]:
                bad.append((key, later))
    return bad


def main():
    write = "--write" in sys.argv
    nt, ot = read_books()
    src = io.open(INDEX, encoding="utf-8").read()

    langs = re.search(r"LANG_NAMES=\{(.*?)\};", src).group(1)
    langs = [m.group(1) for m in re.finditer(r"(\w+):\"", langs)]
    langs = [l for l in langs if l != "en"]

    a, b = literal(src, "BOOK_I18N=")
    body = src[a:b]
    rows = re.findall(r'^\s*"([^"]+)":\{(.*?)\},\s*$', body, re.M)
    if len(rows) != len(NT) + len(OT):
        raise SystemExit("BOOK_I18N holds %d books, not %d"
                         % (len(rows), len(NT) + len(OT)))

    table, order = {}, []
    for key, inner in rows:
        order.append(key)
        table[key] = dict(
            (m.group(1), json.loads('"%s"' % m.group(2)))
            for m in re.finditer(r'(\w+):"((?:[^"\\]|\\.)*)"', inner))

    filled, absent = 0, []
    for key in order:
        for lang in langs:
            if table[key].get(lang):
                continue
            if key in NT:
                name = nt.get(lang, {}).get(NT[key])
                if lang == "zh" and name:
                    name = ZH.get(name, name)
            else:
                name = ot.get(lang, {}).get(str(OT[key]))
                if name:
                    name = name.lstrip(u"﻿")
            if not name:
                absent.append((lang, key))
                continue
            table[key][lang] = name
            filled += 1

    for lang in langs:
        clash = collides(dict((k, table[k][lang])
                              for k in order if table[k].get(lang)))
        for key, later in clash:
            print("  %s: %r would be caught again by %r"
                  % (lang, table[key][lang], later))

    for lang, key in absent:
        print("  no published name for %s in %s" % (key, lang))

    short = [l for l in langs
             if sum(1 for k in order if table[k].get(l)) != len(order)]
    print("%d books, %d renderings filled in, %d languages short"
          % (len(order), filled, len(short)))

    if not write:
        return 0

    out = ["{"]
    for key in order:
        inner = ",".join(
            '%s:%s' % (l, json.dumps(table[key][l], ensure_ascii=False))
            for l in langs if table[key].get(l))
        out.append(' %s:{%s},' % (json.dumps(key, ensure_ascii=False), inner))
    out.append("}")
    io.open(INDEX, "w", encoding="utf-8").write(
        src[:a] + "\n".join(out) + src[b:])
    print("wrote index.html")

    lib = io.open(LIBRARY, encoding="utf-8").read()
    a, b = literal(lib, "NT_BOOK_NAMES")
    books = json.loads(lib[a:b])
    turned = sum(1 for v in books.get("zh", {}).values() if v in ZH)
    books["zh"] = dict((k, ZH.get(v, v)) for k, v in books["zh"].items())
    if turned:
        io.open(LIBRARY, "w", encoding="utf-8").write(
            lib[:a] + json.dumps(books, ensure_ascii=False) + lib[b:])
        print("wrote library.html: %d Chinese names in the site's own script"
              % turned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
