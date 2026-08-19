#!/usr/bin/env python3
"""
The Akathist Hymn to the Most Holy Theotokos, in the languages it is sung in.

The oldest and greatest of the akathists, sung standing - which is what the
name says - on the Fridays of the Great Fast and whole on the Saturday of the
fifth week. It is of the sixth century and its author is not known, though the
Church has long named Romanos the Melodist among those it may be.

    python3 tools/ingest_akathist.py --check
    python3 tools/ingest_akathist.py --write

The shape of the hymn, which is what this verifies against

Twenty-five stanzas. A kontakion opens, then a kontakion and an oikos
alternate to the end. The oikos is the longer, carries twelve salutations
beginning Hail, and closes with the greeting to the Bride unwedded; the
kontakion is the shorter and closes with Alleluia.

The first kontakion is the exception and it is the whole difficulty: it closes
with the Bride unwedded like an oikos, not with Alleluia. So the hymn has
thirteen closings of one kind and twelve of the other, not thirteen and
thirteen, and a count of thirteen Alleluias will never be found in a sound
text. This was asserted the wrong way round once and the Greek was rejected
for being right. The two closings are the hymn's own division, they are the
same in every language, and the printed edition of 1917 - which sets the Greek
and an English verse translation on facing pages - counts them the same way.

Sources. The texts are the received ones, taken as they stand: nothing here is
rendered.

A note on where a text may be taken from. Greek Wikisource carries the
received Byzantine text under a heading that names it and no dispute attaches
to it. The Russian akathists there are a different matter: in August 2025 the
editors of that wiki listed the whole group of them for deletion as, in their
own words, a collage from internet blogs without sources, probably
self-published and a breach of copyright, and one of them had already been
described on its talk page as a Soviet reworking rather than the text of the
Triodion. None of them is used here, and a Russian text will be taken from a
printed edition or not at all.
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
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-akathist")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
BASE = "akathist-theotokos"

STANZAS = 25          # the whole hymn
ALLELUIA = 12         # kontakia 2 to 13
BRIDE = 13            # kontakion 1 and the twelve oikoi


def fetch(lang, page):
    # Keyed on the page as well as the language. It was keyed on the language
    # alone, and nine different akathists then came back as nine copies of the
    # first one - each dividing correctly and each reporting the same 1,654
    # words, which is the only reason it was caught.
    slug = re.sub(r"[^\w]+", "-", page, flags=re.U).strip("-")
    p = CACHE / ("%s.%s.json" % (lang, slug))
    if not p.exists():
        url = ("https://%s.wikisource.org/w/api.php?action=parse&page=%s"
               "&prop=wikitext&format=json&formatversion=2"
               % (lang, urllib.parse.quote(page)))
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=40) as r:
                    p.write_bytes(r.read())
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(15 * (attempt + 1))
        time.sleep(3)
    d = json.loads(p.read_text(encoding="utf-8"))
    if "error" in d:
        raise SystemExit("%s: %s" % (lang, d["error"].get("info")))
    return d["parse"]["wikitext"]


def strip_markup(w):
    w = re.sub(r"<noinclude>.*?</noinclude>", "", w, flags=re.S)
    w = re.sub(r"\{\{[^{}]*\}\}", "\n", w)
    w = re.sub(r"\{\{[^{}]*\}\}", "\n", w)          # nested, one level
    w = re.sub(r"\[\[(?:[^]|]*\|)?([^]]*)\]\]", r"\1", w)
    w = re.sub(r"</?poem>|</?div[^>]*>|<br\s*/?>", "\n", w)
    w = re.sub(r"'''?", "", w)
    w = re.sub(r"<[^>]+>", "", w)
    w = re.sub(r"^[=\s]*=+\s*|\s*=+\s*$", "", w, flags=re.M)
    w = re.sub(r"[ \t]+", " ", w)
    w = re.sub(r"\n{3,}", "\n\n", w)
    return w.strip()


# The two closings, which are how the hymn divides itself.
# Written loosely on purpose. The closing is not printed the same way twice:
# the kontakia give Χαῖρε Νύμφη ἀνύμφευτε without the comma and the oikoi with
# it, and the bride is capitalised in some stanzas and not in others. Each of
# those three variations, taken strictly, swallowed one stanza into the one
# before it - and the alphabet below then reported an Α and a Δ missing from a
# page that carries both. Match the words; let the printer set them as he did.
GREEK_CLOSE = re.compile(
    r"(Ἀλληλού[ιϊ]α\.?|Χαῖρε,?\s*Νύμφη [Ἀἀ]νύμφευτε\.?)")

# The heading the Greek prints over the oikoi. It belongs to the page, not to
# the first stanza, which would otherwise begin with it.
GREEK_HEADING = re.compile(r"^\s*ΟΙ ΟΙΚΟΙ\s*(?:\[[^]]*\])?\s*", re.M)

# The acrostic. The twenty-four stanzas after the opening kontakion begin with
# the letters of the Greek alphabet in order, which is the hymn's own signature
# and the one check that says WHICH stanza is missing rather than how many.
ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"


def initial(text):
    """The stanza's letter, with its breathing and accent taken off."""
    c = text.strip()[:1]
    d = unicodedata.normalize("NFD", c)
    return "".join(x for x in d if not unicodedata.combining(x)).upper()


def split_greek(w):
    """Found by the words the stanzas end with, not by how the page was typed.

    The whole hymn sits inside a centring template, so the verse is lifted out
    of it first; stripping templates before that empties the page. The service
    prints the kontakion of the Annunciation ahead of the hymn, and the hymn
    proper begins at the words to the Champion Leader."""
    poems = re.findall(r"<poem>(.*?)</poem>", w, re.S)
    body = strip_markup("\n\n".join(poems) if poems else w)
    start = body.find("Τῇ ὑπερμάχῳ")
    if start > 0:
        body = body[start:]
    body = GREEK_HEADING.sub("", body)
    pieces = GREEK_CLOSE.split(body)
    out = []
    for i in range(0, len(pieces) - 1, 2):
        text = (pieces[i] + pieces[i + 1]).strip()
        if text:
            out.append(("Ἀλληλού" in pieces[i + 1], text))
    stanzas = name_stanzas(out, "Κοντάκιον", "Οἶκος")
    check_acrostic(stanzas)
    return stanzas


def name_stanzas(pieces, kontakion, oikos):
    """Give each stanza its name and number.

    Which is which does not follow from the closing alone, because the first
    kontakion closes as an oikos does. It follows from the order, which is
    fixed: a kontakion opens the hymn and then the two alternate to the end.
    The closings are then checked against that order, so a text that alternates
    differently from the hymn is refused rather than renumbered."""
    out = []
    k = o = 0
    for n, (alleluia, text) in enumerate(pieces, 1):
        if n == 1 or n % 2 == 1:
            k += 1
            kind, num = kontakion, k
            want_alleluia = (n != 1)
        else:
            o += 1
            kind, num = oikos, o
            want_alleluia = False
        if alleluia != want_alleluia:
            raise ValueError(
                "stanza %d closes with %s; the hymn has %s there"
                % (n, "Alleluia" if alleluia else "the Bride unwedded",
                   "Alleluia" if want_alleluia else "the Bride unwedded"))
        out.append((kind, num, text))
    return out


def check_acrostic(stanzas):
    """The twenty-four after the opening kontakion spell the alphabet.

    A count alone says only that something is wrong. This says what: it names
    the letters that are absent, and a missing letter is a missing stanza. It
    applies to the Greek, where the acrostic is in the words themselves; a
    translation keeps the order of the stanzas but not their initials, so it
    is not asked of one."""
    got = [initial(t) for _k, _n, t in stanzas[1:]]
    missing = [c for c in ALPHABET if c not in set(got)]
    if missing:
        raise ValueError("the acrostic is broken; no stanza begins %s"
                         % " ".join(missing))
    if got != list(ALPHABET):
        raise ValueError("the acrostic runs %s" % " ".join(got))


LANGS = [
    {
        "lang": "el", "wiki": "el", "page": "Ακάθιστος ύμνος",
        "split": split_greek,
        "title": "The Akathist Hymn to the Most Holy Theotokos (Greek)",
        "source": "Received Greek text of the Orthodox Church",
    },
]

DESC = ("Sung standing, which is what its name says, on the Fridays of the "
        "Great Fast and whole on the Saturday of the fifth week. Twenty-four "
        "stanzas whose first letters run through the Greek alphabet, and a "
        "hundred and forty-four salutations beginning Hail, each one addressed "
        "to the Mother of God, with a kontakion before them and a thirteenth "
        "at the end. It is of the sixth century; the Church has long named "
        "Romanos the Melodist among those who may have written it, and does "
        "not say so certainly. This is the Greek, which is the original.")


def build(spec):
    w = fetch(spec["wiki"], spec["page"])
    try:
        got = spec["split"](w)
    except ValueError as e:
        return None, str(e)
    if len(got) != STANZAS:
        return None, "%d stanzas, expected %d" % (len(got), STANZAS)
    wid = "%s-%s" % (BASE, spec["lang"])
    units = []
    for n, (kind, num, text) in enumerate(got, 1):
        if not text.strip():
            return None, "stanza %d is empty" % n
        units.append({
            "unit_id": "%s::u%03d" % (wid, n),
            "work_id": wid,
            "work_title": spec["title"],
            "author": "Anonymous, of the sixth century",
            "source_class": "liturgical",
            "ordinal": n,
            "citation_anchor": "%s %d" % (kind, num),
            "chapter_title": None,
            "text": text,
        })
    return units, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    built, failed = [], []
    for spec in LANGS:
        units, err = build(spec)
        if err:
            failed.append(spec["lang"])
            print("  FAIL  %-4s %s" % (spec["lang"], err))
            continue
        words = sum(len(u["text"].split()) for u in units)
        bad = sum(len(re.findall(r"[–—]", u["text"])) for u in units)
        print("  ok    %-4s %2d stanzas  %6s words  %d dashes"
              % (spec["lang"], len(units), format(words, ","), bad))
        built.append((spec, units))

    # A language that verifies is published; one that does not is named and
    # left out. The hymn is fixed in shape, so a text that will not divide
    # into it is a text this has not understood, and a liturgical text is the
    # last thing to guess at.
    if failed:
        print("\n  not published: %s" % ", ".join(failed))

    if a.write:
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        for spec, units in built:
            wid = "%s-%s" % (BASE, spec["lang"])
            meta = {
                "work_id": wid,
                "edition_of": BASE,
                "title": spec["title"],
                "author": "Anonymous, of the sixth century",
                "language": spec["lang"],
                "date": "6th century",
                "source": spec["source"],
                "source_class": "liturgical",
                "description": DESC,
                "digitized": "Wikisource",
                "license": "Public Domain",
                "saint": None,
                "is_saint": False,
            }
            OUTDIR.joinpath(wid + ".json").write_text(
                json.dumps({"work": meta, "units": units},
                           ensure_ascii=False, indent=1), encoding="utf-8")
            cat = [x for x in cat if x["work_id"] != wid]
            cat.append(meta)
        cat.sort(key=lambda x: x["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %d edition(s) and updated the catalogue" % len(built))
    elif not a.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
