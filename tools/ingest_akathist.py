#!/usr/bin/env python3
"""
The Akathist Hymn to the Most Holy Theotokos, in the languages it is sung in.

The oldest and greatest of the akathists, sung standing - which is what the
name says - on the Fridays of the Great Fast and whole on the Saturday of the
fifth week. It is of the sixth century and its author is not known, though the
Church has long named Romanos the Melodist among those it may be.

The hymn has one shape everywhere: twenty-four stanzas whose first letters run
through the Greek alphabet, alternating between the shorter kontakion, which
ends Alleluia, and the longer oikos, which ends with the salutation to the
Bride unwedded and carries twelve Hails of its own. A thirteenth kontakion is
sung at the end. Because the shape is fixed, the languages can be set beside
one another line for line, as the Divine Liturgies on this shelf are.

    python3 tools/ingest_akathist.py --check
    python3 tools/ingest_akathist.py --write

Each language is a work of its own, and all of them name the same edition_of,
which is how the reader knows to put them in columns.

Sources. The texts are the received ones, taken as they stand: nothing here is
rendered, and where a language is missing it is missing because no text of it
was found that may be published, not because it was thought unnecessary.
"""
import argparse
import json
import re
import sys
import time
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

# The hymn as the Church sings it: thirteen kontakia and twelve oikoi, and
# they alternate. Anything else means the page changed under us.
KONTAKIA, OIKOI = 13, 12


def fetch(lang, page):
    p = CACHE / ("%s.json" % lang)
    if not p.exists():
        url = ("https://%s.wikisource.org/w/api.php?action=parse&page=%s"
               "&prop=wikitext&format=json&formatversion=2"
               % (lang, urllib.parse.quote(page)))
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=40) as r:
            p.write_bytes(r.read())
        time.sleep(2)
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


def split_russian(w):
    """The Russian page heads every stanza, so it is read off the headings."""
    parts = re.split(r"\n?=+\s*(Кондак|Икос)\s*(\d+)\s*=+\n?", w)
    out = []
    for i in range(1, len(parts) - 1, 3):
        kind, num, body = parts[i], int(parts[i + 1]), parts[i + 2]
        out.append((kind, num, strip_markup(body)))
    return out


def split_greek(w):
    """The Greek page heads nothing, so the stanzas are found by the words
    they end with: a kontakion closes with Alleluia, an oikos with the
    salutation to the Bride unwedded. That is the hymn's own division and it
    does not depend on how a page was typed.

    The whole hymn sits inside a centring template, so the verse is lifted out
    of it first. Stripping templates before that empties the page."""
    poems = re.findall(r"<poem>(.*?)</poem>", w, re.S)
    body = strip_markup("\n\n".join(poems) if poems else w)
    # The Greek service prints the kontakion of the Annunciation before the
    # hymn. It is not one of the twenty-five stanzas, and the hymn proper
    # begins at the words to the Champion Leader.
    start = body.find("Τῇ ὑπερμάχῳ")
    if start > 0:
        body = body[start:]
    # Keep the closing words with the stanza they belong to.
    pieces = re.split(r"(Ἀλληλού[ιϊ]α\.?|Χαῖρε, Νύμφη ἀνύμφευτε\.?)", body)
    out, k, o = [], 0, 0
    for i in range(0, len(pieces) - 1, 2):
        text = (pieces[i] + pieces[i + 1]).strip()
        if not text:
            continue
        if "Ἀλληλού" in pieces[i + 1]:
            k += 1
            out.append(("Κοντάκιον", k, text))
        else:
            o += 1
            out.append(("Οἶκος", o, text))
    return out


LANGS = [
    {
        "lang": "el", "wiki": "el", "page": "Ακάθιστος ύμνος",
        "split": split_greek,
        "title": "The Akathist Hymn to the Most Holy Theotokos (Greek)",
        "source": "Received Greek text of the Orthodox Church",
    },
    {
        "lang": "ru", "wiki": "ru", "page": "Акафист Пресвятой Богородице",
        "split": split_russian,
        "title": "The Akathist Hymn to the Most Holy Theotokos (Russian)",
        "source": "Received Russian text of the Orthodox Church",
    },
]

DESC = ("Sung standing, which is what its name says, on the Fridays of the "
        "Great Fast and whole on the Saturday of the fifth week. Twenty-four "
        "stanzas whose first letters run through the Greek alphabet, and a "
        "hundred and forty-four salutations beginning Hail, each one addressed "
        "to the Mother of God. It is of the sixth century; the Church has long "
        "named Romanos the Melodist among those who may have written it, and "
        "does not say so certainly.")


def build(spec):
    w = fetch(spec["wiki"], spec["page"])
    got = spec["split"](w)
    k = sum(1 for kind, _n, _t in got if kind in ("Кондак", "Κοντάκιον"))
    o = sum(1 for kind, _n, _t in got if kind in ("Икос", "Οἶκος"))
    if (k, o) != (KONTAKIA, OIKOI):
        return None, "%d kontakia and %d oikoi, expected %d and %d" % (
            k, o, KONTAKIA, OIKOI)
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
        print("\nwrote %d editions and updated the catalogue" % len(built))
    elif not a.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
