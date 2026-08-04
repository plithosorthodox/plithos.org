#!/usr/bin/env python3
"""
Ingest the canon law of the Church into the Library.

What this covers: the Apostolic Canons, the canons of the seven Ecumenical
Councils and of the local councils received with them, the African Code, and
the canonical epistles of the Fathers. Trullo's second canon receives all of
it by name, which is why it belongs together in one work.

Source. Nicene and Post-Nicene Fathers, Second Series, Volume 14, "The Seven
Ecumenical Councils of the Undivided Church", edited with notes by Henry R.
Percival, published 1900. Public domain. Text from the Christian Classics
Ethereal Library, which reproduces the printed volume.

CCEL puts one canon on one page, with Percival's notes and excursus on pages
of their own. This takes the canons and their Ancient Epitomes, and leaves the
nineteenth-century commentary out: the canon is what the Church legislated,
the commentary is one editor's gloss on it.

    python3 tools/ingest_canons.py            # fetch, normalise, emit
    python3 tools/ingest_canons.py --install  # also copy into data/library

Raw pages are cached, so a re-run is cheap and does not hit the server again.
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path("/tmp/claude-0/-home-user-plithos-org/canons-raw")
CACHE.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "data" / "library"

BASE = "https://www.ccel.org/ccel/schaff/"
TOC = BASE + "npnf214.toc.html"
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"

DASHES = dict.fromkeys(map(ord, "–—‒―"), "-")
QUOTES = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x00A0: " "}

# The volume's Appendix carries the rest of the canonical corpus the Church
# receives: the Apostolic Canons, ratified by name in Trullo's second canon and
# standing first in every Orthodox collection, and the canonical epistles of
# the Fathers ratified in the same place. None of it is one canon to a page, so
# the council walk below cannot see any of it, and all of it was missing.
APPENDIX = "npnf214.xvii."
APPENDIX_SKIP = {"npnf214.xvii.html", "npnf214.xvii.i.html",
                 "npnf214.xvii.ii.html", "npnf214.xvii.iii.html"}

# Percival's headings for these run to a full line. Matched in order.
APPENDIX_SHORT = [
    (r"Altogether August Apostles",        "The Apostolic Canons"),
    (r"First Canonical Epistle.*Basil",    "St Basil, First Canonical Epistle"),
    (r"Second Canonical Epistle of the Same", "St Basil, Second Canonical Epistle"),
    (r"Third Epistle of the Same to the Same", "St Basil, Third Canonical Epistle"),
    (r"Blessed Amphilochius on the Difference of Mea",
                                           "St Basil to Amphilochius, on measures"),
    (r"Diodorus Bishop of Tarsus",         "St Basil to Diodorus of Tarsus"),
    (r"Gregory a Presbyter",               "St Basil to the presbyter Gregory"),
    (r"Chorepiscopi",                      "St Basil to the chorepiscopi"),
    (r"Should Not Ordain for Money",        "St Basil to his suffragans, on ordination"),
    (r"Wrote to Blessed Amphilochius on the Ho",
                                           "St Basil, On the Holy Spirit, ch. 27"),
    (r"Nicopolitans",                      "St Basil to the Nicopolitans"),
    (r"Dionysius, the Archbishop of Alexandria", "St Dionysius of Alexandria to Basilides"),
    (r"Peter, Archbishop of Alexandria",   "St Peter of Alexandria, Canons"),
    (r"Neoc\w{1,2}sarea, who is called Th", "St Gregory Thaumaturgus, Canonical Epistle"),
    (r"Athanasius to the Monk Ammus",      "St Athanasius to the monk Ammun"),
    (r"XXXIX\. Festal Epistle",            "St Athanasius, Thirty-ninth Festal Epistle"),
    (r"Athanasius to Ruffinian",           "St Athanasius to Rufinian"),
    (r"Gregory, Bishop of Nyssa",          "St Gregory of Nyssa to Letoius"),
    (r"Gregory Theologus",                 "St Gregory the Theologian, on the books of Scripture"),
    (r"Amphilochius the Bishop to Seleucus", "St Amphilochius to Seleucus, on the books of Scripture"),
    (r"Timothy the Most Holy Bishop",      "Timothy of Alexandria, Canonical Answers"),
    (r"Prosphonesus of Theophilus",        "Theophilus of Alexandria, Prosphonesus"),
    (r"Commonitory of the Same",           "Theophilus of Alexandria, Commonitory"),
    (r"Same to Agatho",                    "Theophilus of Alexandria to Agatho"),
    (r"Same to Menas",                     "Theophilus of Alexandria to Menas"),
    (r"Those Called Cathari",              "Theophilus of Alexandria, on the Cathari"),
    (r"Cyril, Archbishop of",              "St Cyril of Alexandria, Canonical Epistle"),
    (r"Bishops of Libya and Pentapolis",   "St Cyril to the bishops of Libya and Pentapolis"),
    (r"Gennadius",                         "Gennadius of Constantinople, Encyclical"),
]


def fetch(url, name, delay=1.2):
    p = CACHE / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read().decode("utf-8", errors="replace")
            break
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


def clean(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    # CCEL repeats each footnote inline, inside a span.mnote right after the
    # marker. Flattening the tags first would drop the editor's notes into the
    # middle of a sentence of the canon, so they come out before that happens.
    s = re.sub(r'<span[^>]*class="[^"]*mnote[^"]*"[^>]*>.*?</span>\s*</span>',
               "", s, flags=re.S | re.I)
    s = re.sub(r'<span[^>]*class="[^"]*(?:mnote|Footnote)[^"]*"[^>]*>.*?</span>',
               "", s, flags=re.S | re.I)
    s = re.sub(r"<sup\b[^>]*>.*?</sup>", "", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).translate(DASHES).translate(QUOTES)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


ROMAN = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}


def unroman(s):
    n = last = 0
    for ch in reversed(s.upper()):
        v = ROMAN.get(ch, 0)
        n = n - v if v < last else n + v
        last = max(last, v)
    return n


def canon_pages():
    """(href, council, canon_number) for every canon page, in volume order.

    The volume nests each canon under the page that collects its council's
    canons, which in turn sits under the council itself, and the nesting is
    carried in the filename: npnf214.vii.vi.i.html is canon I of the canon
    collection vii.vi, under council vii. Walking that beats a hand-written
    list of section prefixes, which silently drops any council whose prefix
    was guessed wrong - the first attempt at this lost seven of them."""
    toc = fetch(TOC, "toc.html")
    titles, order = {}, []
    for href, label in re.findall(
            r'href="([^"]*npnf214[^"]*\.html)"[^>]*>(.*?)</a>', toc, re.S):
        name = href.split("/")[-1]
        if name in titles:
            continue
        titles[name] = re.sub(r"\s+", " ", clean(label)).strip()
        order.append(name)

    def ancestors(name):
        parts = name[:-len(".html")].split(".")
        for i in range(len(parts) - 1, 0, -1):
            yield ".".join(parts[:i]) + ".html"

    def council_of(name):
        best = ""
        for anc in ancestors(name):
            t = titles.get(anc, "")
            if not t:
                continue
            if re.search(r"Council|Synod|Code", t, re.I):
                return shorten(t)
            best = best or t.rstrip(".")
        return best or "Unattributed"

    out = []
    for name in order:
        m = re.match(r"Canon ([IVXLC]+)\.?$", titles.get(name, ""))
        if m:
            out.append((name, council_of(name), unroman(m.group(1))))
    return out


# Percival's chapter titles run to a full line and more; a citation wants the
# council and its year. Matched in order, first hit wins, so the more specific
# patterns come first. Carthage must precede the bare "Carthage" of Sardica's
# neighbours, and Nice II before Nice I, since both name the same city.
SHORT = [
    (r"African Church|assembled at Carthage",   "The African Code (419)"),
    (r"Ecumenical Seventh|Second Council of Nice", "Nicaea II (787)"),
    (r"318 Holy Fathers|First Council of Nice", "Nicaea I (325)"),
    (r"Trullo|Quinisext",                       "The Council in Trullo (692)"),
    # Neocaesarea's heading dates itself against Ancyra by name, so it has to
    # be matched before Ancyra or its fifteen canons are filed under Ancyra.
    (r"Neoc\w{1,2}sarea",                       "Neocaesarea (c. 315)"),
    (r"Ancyra",                                 "Ancyra (314)"),
    (r"Gangra",                                 "Gangra (c. 340)"),
    (r"Antioch",                                "Antioch (341)"),
    (r"Laodicea",                               "Laodicea (c. 364)"),
    (r"Sardica",                                "Sardica (343)"),
    (r"First Council of Constantinople",        "Constantinople I (381)"),
    (r"Second Council of Constantinople",       "Constantinople II (553)"),
    (r"Council of Ephesus",                     "Ephesus (431)"),
    (r"Chalcedon",                              "Chalcedon (451)"),
]


def shorten(title):
    for pat, name in SHORT:
        if re.search(pat, title, re.I):
            return name
    return title.rstrip(".")


# Percival prints the canon, then a nineteenth-century apparatus: the ancient
# epitome, then the Greek and Latin commentators and his own excursus. Only the
# canon and the epitome are the Church's; the rest is one editor's gloss and is
# left out. These names mark where that apparatus begins.
GLOSSATORS = (r"Van Espen|Zonaras|Balsamon|Aristenus|Hefele|Beveridge|Johnson|"
              r"Justellus|Bright|Lambert|Fulton|Dionysius|Aristenus|Excursus|"
              r"Notes|Daniel Butler|Smith|Tillemont|Routh|Bingham")


def canon_text(body):
    """The canon itself plus its Ancient Epitome, without Percival's notes."""
    m = re.search(r'<div[^>]*class="[^"]*book-content[^"]*"[^>]*>', body)
    if not m:
        return ""
    tail = body[m.end():]
    stop = re.search(r'<div[^>]*class="[^"]*(?:footnotes|content-foot)[^"]*"', tail)
    t = clean(tail[:stop.start()] if stop else tail)

    # Drop everything up to and including the "Canon N." heading itself. The
    # page number and the section title precede it and are not the canon.
    m = re.search(r"Canon [IVXLC]+\.\s*", t)
    if m:
        t = t[m.end():]

    canon = re.split(r"\bNotes\.", t)[0].strip()
    epi = ""
    m = re.search(r"Ancient Epitome\b[^.]*\.\s*(.*?)(?=\s(?:%s)\b|\Z)"
                  % GLOSSATORS, t, re.S)
    if m:
        epi = re.sub(r"\s+", " ", m.group(1)).strip()
        # a footnote marker between "Ancient Epitome" and "of Canon N" leaves
        # the second half stranded at the head of the epitome
        epi = re.sub(r"^of Canon [IVXLC]+\.\s*", "", epi)
    canon = re.sub(r"^\d+\s+", "", canon).strip()
    if epi and epi.lower() not in canon.lower():
        canon += "\n\nAncient Epitome. " + epi
    return canon


# Field names follow the existing catalogue exactly; plithos_reader.html reads
# work_id, title, author, date, translator, pub_year, source, source_class,
# description and digitized off these entries, and shows nothing it cannot find.
def page_text(body):
    """The reading text of a CCEL page, without the site chrome or footnotes."""
    m = re.search(r'<div[^>]*class="[^"]*book-content[^"]*"[^>]*>', body)
    if not m:
        return ""
    tail = body[m.end():]
    stop = re.search(r'<div[^>]*class="[^"]*(?:footnotes|content-foot)[^"]*"', tail)
    return clean(tail[:stop.start()] if stop else tail)


def appendix_pages():
    """(href, short title) for each document of the canonical Appendix."""
    toc = fetch(TOC, "toc.html")
    out, seen = [], set()
    for href, label in re.findall(
            r'href="([^"]*npnf214[^"]*\.html)"[^>]*>(.*?)</a>', toc, re.S):
        name = href.split("/")[-1]
        if name in seen or not name.startswith(APPENDIX) or name in APPENDIX_SKIP:
            continue
        seen.add(name)
        title = re.sub(r"\s+", " ", clean(label)).strip()
        short = next((s for p, s in APPENDIX_SHORT if re.search(p, title, re.I)), None)
        if short:
            out.append((name, short))
        else:
            print("  no short title for %s: %s" % (name, title[:70]))
    return out


def split_canons(text):
    """[(number, text)] for a page that carries many canons in one document.

    Percival sometimes merges two canons under one heading, as 'Canon III.
    (III. and IV.)', so the count of headings is not the count of canons and
    the heading's own number is the one to keep."""
    marks = list(re.finditer(r"Canon ([IVXLC]+)\.\s*(?:\([^)]*\)\s*)?", text))
    out = []
    for k, m in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        body = re.split(r"\bNotes\.", body)[0].strip()
        body = re.sub(r"\s*«\s*Prev.*$", "", body, flags=re.S).strip()
        if len(body) > 15:
            out.append((unroman(m.group(1)), body))
    return out


META = {
    "work_id": "canons-ecumenical",
    "title": "The Canons of the Councils",
    "author": "The Councils of the Church",
    "date": "1st to 8th century",
    "translator": "Henry R. Percival",
    "pub_year": 1900,
    "source": ("Nicene and Post-Nicene Fathers, Series 2, Vol. 14: "
               "The Seven Ecumenical Councils of the Undivided Church"),
    "source_class": "canons",
    "description": ("The canon law of the Church: the Apostolic Canons, the "
                    "canons of the seven Ecumenical Councils and of the local "
                    "councils received with them, the African Code, and the "
                    "canonical epistles of the Fathers. Each conciliar canon "
                    "carries its ancient epitome."),
    "language": "en",
    "digitized": "Christian Classics Ethereal Library",
    "license": "Public Domain",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true",
                    help="write into data/library and update works-index.json")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    pages = canon_pages()
    if args.limit:
        pages = pages[:args.limit]
    print("%d canon pages" % len(pages))

    units, skipped = [], 0
    for i, (name, council, num) in enumerate(pages, 1):
        try:
            body = fetch(BASE + name, name)
        except Exception as e:
            print("  fetch failed %s: %s" % (name, e))
            skipped += 1
            continue
        text = canon_text(body)
        if len(text) < 40:
            skipped += 1
            continue
        units.append({
            "unit_id": "%s::u%03d" % (META["work_id"], len(units) + 1),
            "work_id": META["work_id"],
            "work_title": META["title"],
            "author": META["author"],
            "source_class": META["source_class"],
            "ordinal": len(units) + 1,
            "citation_anchor": "%s, Canon %d" % (council, num),
            "text": text,
        })
        if i % 50 == 0:
            print("  %d/%d" % (i, len(pages)))

    # The Appendix: the Apostolic Canons and the canonical epistles of the
    # Fathers, both received by Trullo's second canon. Neither is one canon to
    # a page, so they come in by document rather than by page.
    for name, short in appendix_pages():
        try:
            body = fetch(BASE + name, name)
        except Exception as e:
            print("  fetch failed %s: %s" % (name, e))
            skipped += 1
            continue
        text = page_text(body)
        if not text:
            skipped += 1
            continue
        pieces = split_canons(text)
        if not pieces:
            # a document with no numbered canons, kept whole
            whole = re.split(r"\bNotes\.", text)[0].strip()
            whole = re.sub(r"^\d+\s+[IVXLC]*\.?\s*", "", whole).strip()
            pieces = [(None, whole)] if len(whole) > 60 else []
        for num, body_text in pieces:
            units.append({
                "unit_id": "%s::u%03d" % (META["work_id"], len(units) + 1),
                "work_id": META["work_id"],
                "work_title": META["title"],
                "author": META["author"],
                "source_class": META["source_class"],
                "ordinal": len(units) + 1,
                "citation_anchor": ("%s, Canon %d" % (short, num)) if num else short,
                "text": body_text,
            })

    print("%d canons, %d skipped" % (len(units), skipped))
    words = sum(len(u["text"].split()) for u in units)
    bad = sum(len(re.findall(r"[–—]", u["text"])) for u in units)
    print("%d words, %d stray dashes" % (words, bad))

    out = {"work": META, "units": units}
    if args.install:
        OUT.joinpath(META["work_id"] + ".json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        idx = OUT / "works-index.json"
        cat = json.loads(idx.read_text(encoding="utf-8"))
        entry = dict(META)
        entry["units"] = len(units)
        # Replace, never skip. Skipping an entry that already exists left the
        # catalogue holding the first run's fields - an old title, a stale unit
        # count, and field names the reader does not read, so the Library card
        # showed no date and no description and reported no error anywhere.
        cat = [w for w in cat if w.get("work_id") != META["work_id"]] + [entry]
        cat.sort(key=lambda w: (w.get("title") or "").lower())
        idx.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        print("installed data/library/%s.json" % META["work_id"])
    else:
        p = CACHE / "preview.json"
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("preview at %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
