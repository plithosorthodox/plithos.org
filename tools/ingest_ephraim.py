#!/usr/bin/env python3
"""
Add St Ephraim the Syrian.

The greatest hymnographer the Church has, whose Lenten prayer every Orthodox
Christian says, and the shelf had nothing of his.

The text is Nicene and Post-Nicene Fathers, Series 2, Volume 13. The structure
is taken from the volume's own table of contents rather than assembled here,
and every section asserts the number of pieces the edition's own title pages
name: nineteen hymns on the Nativity, fifteen for the Epiphany, seven on the
faith, three homilies.

Two of the Nisibene pieces are not hymns but the editor saying what is
missing, and both are kept. The first records that Hymn VIII is wanting and
that the earlier part of IX is too; the second records that XXII to XXV are
wanting, that XXVI survives as a fragment, and that XXVII to XXXIV concern
Edessa. They are three lines each and they are the most useful lines in the
series, because they tell a reader where the gaps are.

That first note is also why this is built from here rather than from the
other transcription of the same volume, which followed a slip in the printed
contents - it lists the note as "Hymn XIII.", the number of a hymn printed
five pages later - and, resolving the duplicate, dropped the note altogether.
A reader of that copy would find forty-six pieces, no error of any kind, and
no way to learn that a hymn was missing.

    python3 tools/ingest_ephraim.py --check
    python3 tools/ingest_ephraim.py --write
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
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-ephraim")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
SITE = "https://www.ccel.org/ccel/schaff/"
TOC = "npnf213.toc.html"

DASHES = dict.fromkeys(map(ord, "–—‒―"), "-")
QUOTES = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x00A0: " "}

COMMON = {
    "author": "St Ephraim the Syrian",
    "pub_year": 1898,
    "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 13",
    "publisher": "Christian Literature Company, New York",
    "source_class": "patristic",
    "digitized": "Christian Classics Ethereal Library",
    "rights": "Public domain",
    "saint": "Venerable Ephraim the Syrian",
    "is_saint": True,
    "language": "en",
}

# The section's page in the volume's contents, and the prefix its pieces carry.
# Titles are the edition's own, from its title pages: it calls them nineteen
# hymns on the Nativity of Christ in the flesh and fifteen for the Epiphany,
# and the count is part of the title rather than a claim made here.
#
# work_id, contents page, pieces, title, date, translator, description
WORKS = [
    ("ephraim-nisibene-hymns", "npnf213.iii.iv", 48, "The Nisibene Hymns",
     "c. 350-363", "J. T. Sarsfield Stopford, revised by John Gwynn",
     "Hymns written while Nisibis was under siege by the Persians and after "
     "its surrender drove Ephraim into exile at Edessa. They move between the "
     "city's walls and the soul's; a set in the middle honours the three "
     "bishops who held the city, and the long closing sequence is an argument "
     "with Death and Satan, who are given speeches of their own and answer "
     "back. This edition carries forty-five of the seventy-seven hymns, "
     "printing them in the numbering of the whole series so the gaps are "
     "visible, and it marks each gap where it falls: two of the pieces here "
     "are the editor's own brackets recording which hymns are wanting, which "
     "survives only as a fragment, and which concern Edessa."),
    ("ephraim-nativity-hymns", "npnf213.iii.v", 20,
     "Nineteen Hymns on the Nativity of Christ in the Flesh", "4th century",
     "J. B. Morris and A. Edward Johnston",
     "Hymns for the Feast of the Nativity, on the God who was carried by the "
     "one He carries, and on what it is for the Ancient of Days to be an "
     "infant. The eleventh is given wholly to the Virgin Mother speaking to "
     "her Child."),
    ("ephraim-epiphany-hymns", "npnf213.iii.vi", 16,
     "Fifteen Hymns For the Feast of the Epiphany", "4th century",
     "A. Edward Johnston",
     "Hymns for the Theophany, on the Jordan, on the descent into the water, "
     "and on what baptism does to the one baptised. The thirteenth is headed "
     "the Hymn of the Baptized and is sung in their own voice."),
    ("ephraim-the-pearl", "npnf213.iii.vii", 8,
     "The Pearl. Seven Hymns on the Faith", "4th century",
     "J. B. Morris and A. Edward Johnston",
     "Seven short hymns on faith, turning on a pearl Ephraim says he took up "
     "and questioned, and which answered him about the Son."),
    ("ephraim-homilies", "npnf213.iii.viii", 4, "Three Homilies", "4th century",
     "A. Edward Johnston",
     "Three homilies: on our Lord, on admonition and repentance, and on the "
     "sinful woman who anointed His feet. The last is a dialogue, and the "
     "seller of ointment is given lines."),
]


# The volume's contents lists the first of the two editor's brackets as
# "Hymn XIII.", the number of a hymn it prints five entries later, so two
# different pieces arrive under one name and the note is the one that would
# vanish. The edition's own way of naming such a note is the range it covers -
# it heads the second one "Hymn XXII-XXXIV" - and that convention is followed
# here rather than the misprint.
MISNUMBERED = {"npnf213.iii.iv.ix.html": "Hymn VIII-IX"}


def fetch(name, delay=0.4):
    p = CACHE / name
    if p.exists():
        return p.read_text(encoding="utf-8")
    req = urllib.request.Request(SITE + name, headers={"User-Agent": UA})
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                raw = r.read()
            break
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)
    # Declared charset, then the two encodings this site actually serves. A
    # bare decode with errors="replace" put four hundred replacement
    # characters into every Greek work on this shelf before anyone noticed.
    m = re.search(rb"charset=([\w-]+)", raw[:4000], re.I)
    declared = m.group(1).decode("ascii", "replace").lower() if m else "utf-8"
    body = None
    for enc in (declared, "utf-8", "cp1252"):
        try:
            body = raw.decode(enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    if body is None:
        body = raw.decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


def clean(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    # CCEL prints each footnote inline, in a span right after its marker.
    # Flattening the tags first would drop a note into the middle of a line.
    s = re.sub(r'<span[^>]*class="[^"]*mnote[^"]*"[^>]*>.*?</span>\s*</span>',
               "", s, flags=re.S | re.I)
    s = re.sub(r'<span[^>]*class="[^"]*(?:mnote|Footnote)[^"]*"[^>]*>.*?</span>',
               "", s, flags=re.S | re.I)
    s = re.sub(r"<sup\b[^>]*>.*?</sup>", "", s, flags=re.S | re.I)
    # The page numbers of the print edition, set inline wherever a page turned.
    s = re.sub(r'<span[^>]*class="[^"]*\bpb\b[^"]*"[^>]*>.*?</span>', " ", s,
               flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.I)
    # Inline markup closes up rather than opening a gap. A word set in small
    # capitals or italic is its own element, and turning every tag into a
    # space breaks the line the edition set tight: "Resp .- To Thee" for
    # "Resp.-To Thee".
    s = re.sub(r"</?(?:span|i|b|em|strong|a|small|sub)\b[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).translate(DASHES).translate(QUOTES)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def page_text(name):
    """The reading text of a page: what lies between the two navigation bars.

    The site repeats a small table of previous-and-next links above the text
    and below it, and the printed page sits between them. Cutting on the
    content div instead is not enough here - the page that carries only the
    editor's bracket has that div nested inside another whose class name also
    contains the word, and the bracket came out as a login prompt.
    """
    body = fetch(name)
    top = re.search(r'id="book_navbar_top".*?</table>', body, flags=re.S)
    bottom = re.search(r'<table[^>]*id="book_navbar_bottom"', body)
    if not (top and bottom):
        return ""
    seg = body[top.end():bottom.start()]
    stop = re.search(r'<div[^>]*class="[^"]*(?:footnotes|content-foot)[^"]*"',
                     seg)
    return clean(seg[:stop.start()] if stop else seg)


def contents(prefix):
    """(page, heading) for each piece of a section, in the volume's own order.

    Read off the table of contents rather than guessed at, and the title page
    is dropped because it is the section's own front matter and its heading is
    already the work's title.
    """
    toc = fetch(TOC)
    out, seen = [], set()
    for href, label in re.findall(
            r'href="([^"]*npnf213[^"]*\.html)"[^>]*>(.*?)</a>', toc, re.S):
        name = href.split("/")[-1]
        stem = name[:-len(".html")]
        if name in seen or not stem.startswith(prefix + "."):
            continue
        # Only the section's own children, not its grandchildren.
        if stem[len(prefix) + 1:].count(".") or stem == prefix + ".i":
            continue
        seen.add(name)
        title = re.sub(r"\s+", " ", clean(label)).strip(" .")
        out.append((name, MISNUMBERED.get(name, title)))
    return out


def head(text, heading):
    """The piece without the front matter standing above it.

    The first page of every section opens with the title of the whole set, a
    printer's rule, and then the piece's own heading; later pages open with
    the heading alone. All of it is said again by the shelf, so the text
    begins after the heading - and only if the heading is actually found in
    the first few lines, so that a piece which carries none, like the
    editor's brackets, comes through whole.
    """
    def flat(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    lines = text.split("\n")
    want, seen = flat(heading), 0
    for i, line in enumerate(lines):
        if not flat(line):
            continue
        if flat(line) in want:
            return "\n".join(lines[i + 1:]).strip()
        seen += 1
        if seen > 4:          # the front matter is never deeper than this
            break
    return text.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    built, failed = [], []
    for wid, prefix, want, title, date, translator, desc in WORKS:
        got = contents(prefix)
        if len(got) != want - 1:      # the title page is not one of the pieces
            failed.append(wid)
            print("  FAIL  %-28s %d pieces, %d expected"
                  % (wid, len(got), want - 1))
            continue
        units, short = [], None
        for n, (page, heading) in enumerate(got, start=1):
            text = head(page_text(page), heading)
            # The editor's brackets are three lines long and belong here. Every
            # hymn is hundreds of words, so anything short that is not a
            # bracket is a page that did not come down whole.
            if len(text.split()) < 60 and not text.startswith("["):
                short = "%s: %d words" % (heading, len(text.split()))
                break
            units.append({
                "unit_id": "%s::u%02d" % (wid, n),
                "work_id": wid,
                "work_title": title,
                "author": COMMON["author"],
                "source_class": "patristic",
                "ordinal": n,
                "citation_anchor": heading,
                "text": text,
            })
        if short:
            failed.append(wid)
            print("  FAIL  %-28s %s came out short" % (wid, short))
            continue
        bad = sum(u["text"].count("�") for u in units)
        if bad:
            failed.append(wid)
            print("  FAIL  %-28s %d replacement characters" % (wid, bad))
            continue
        notes = sum(1 for u in units if u["text"].startswith("["))
        words = sum(len(u["text"].split()) for u in units)
        print("  ok    %-28s %2d pieces  %7s words%s"
              % (wid, len(units), format(words, ","),
                 "  (%d editor's note%s)" % (notes, "" if notes == 1 else "s")
                 if notes else ""))
        built.append((dict(COMMON, work_id=wid, title=title, date=date,
                           translator=translator, description=desc), units))

    if failed:
        print("\n%d failed; nothing written" % len(failed))
        return 1

    if args.write:
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        for meta, units in built:
            OUTDIR.joinpath(meta["work_id"] + ".json").write_text(
                json.dumps({"work": meta, "units": units},
                           ensure_ascii=False, indent=1), encoding="utf-8")
            cat = [w for w in cat if w["work_id"] != meta["work_id"]]
            cat.append(meta)
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %d works" % len(built))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
