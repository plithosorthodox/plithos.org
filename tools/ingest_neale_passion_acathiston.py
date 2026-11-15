#!/usr/bin/env python3
"""Build Archbishop Innocent's Passion Acathiston in Neale's English.

John Mason Neale translated this complete office for chapter VII of
``Voices from the East`` (London: Joseph Masters, 1859).  The chapter is
available as a transcription at Project Canterbury and as a full-view scan
at Internet Archive.  The English edition is in the public domain.

The Project Canterbury source is pinned by its byte digest.  This builder
keeps the edition's wording, capitalization, punctuation, and section order.
It joins line-wrapped HTML text, removes presentation markup, and reconciles
documented transcription errors against the 1859 facsimile.

    python tools/ingest_neale_passion_acathiston.py --check
    python tools/ingest_neale_passion_acathiston.py --write

``--write`` intentionally emits only the work file. Catalogue publication and
the reader-facing indexes remain separate editorial steps.
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"

WORK_ID = "akathist-divine-passion-en"
EDITION_OF = "akathist-divine-passion"
SOURCE_URL = "https://anglicanhistory.org/neale/voices1859/07.html"
FACSIMILE_URL = "https://archive.org/details/voicesfromeastd00macagoog"
SOURCE_SHA256 = "ec87eb7963a338ef05611d4992707c8f3ab729ed7dd33ac0ca0187d744bd8071"
CANONICAL_SHA256 = "f9fe343dd7378c577a9ebb4025eda0dce485c0a90cd81f7b360f679cea3e680e"
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"

# Project Canterbury transcription errors checked against the 1859 facsimile.
# Each old fragment is deliberately long enough to identify one reading only.
REPAIRS = (
    ("Man 1'jhom thou hast confessed", "Man Whom thou hast confessed", 179),
    ("Alleluia, Allelnia,. Alleluia.",
     "Alleluia, Alleluia, Alleluia.", 180),
    ("to the Soy, and to the HOLY GHOST", "to the SON, and to the HOLY GHOST", 183),
    ("didst hring forth the supreme Physician",
     "didst bring forth the supreme Physician", 183),
    ("teach me to hear all things", "teach me to bear all things", 183),
    ("O my JESUS, ad give joy", "O my JESUS, and give joy", 184),
    ("when thon sawest the Jews", "when thou sawest the Jews", 184),
    ("but, Gou Eternal, Thou didst", "but, GOD Eternal, Thou didst", 188),
    ("make mc worthy of all Thy sufferings",
     "make me worthy of all Thy sufferings", 193),
    ("I know that Thou wart begotten", "I know that Thou wast begotten", 195),
    ("receive me, Who east myself", "receive me, Who cast myself", 197),
    ("JESUS, SON of Gou, remember us", "JESUS, SON of GOD, remember us", 197),
    ("celebrate GOD OUF Redeemer", "celebrate GOD our Redeemer", 197),
    ("to the SONS and to the HOLY GHOST", "to the SON and to the HOLY GHOST", 200),
    ("cried out, How should I not weep",
     "cried out, \"How should I not weep", 203),
    ("free will for me How shall I bury Thee",
     "free will for me! How shall I bury Thee", 203),
    ("stands in tenor and dismay", "stands in terror and dismay", 204),
)


class ParagraphParser(HTMLParser):
    """Read paragraph text and remember which paragraphs are headings."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.paragraphs = []
        self.current = None
        self.centered = False
        self.skipped = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in ("script", "style"):
            self.skipped += 1
            return
        if self.skipped:
            return
        if tag == "p":
            self._finish()
            self.current = []
            self.centered = False
        elif tag == "center" and self.current is not None:
            self.centered = True
        elif tag == "br" and self.current is not None:
            self.current.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script", "style") and self.skipped:
            self.skipped -= 1
            return
        if self.skipped:
            return
        if tag == "p":
            self._finish()

    def handle_data(self, data):
        if not self.skipped and self.current is not None:
            self.current.append(data)

    def close(self):
        HTMLParser.close(self)
        self._finish()

    def _finish(self):
        if self.current is None:
            return
        text = "".join(self.current).replace("\r", " ").replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            self.paragraphs.append((self.centered, text))
        self.current = None
        self.centered = False


def fetch_source():
    request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError("source digest %s, expected %s" %
                         (digest, SOURCE_SHA256))
    return raw


def source_paragraphs(raw):
    parser = ParagraphParser()
    parser.feed(raw.decode("utf-8"))
    parser.close()
    rows = parser.paragraphs
    chapter = next((number for number, (_centered, text) in enumerate(rows)
                    if text.startswith("Chapter VII. Acathiston; or,")), None)
    if chapter is None:
        raise ValueError("chapter heading is absent")
    selected = []
    for centered, text in rows[chapter + 1:]:
        if text == "Project Canterbury":
            break
        selected.append((centered, text))
    if not selected:
        raise ValueError("chapter text is absent")
    return repair_transcription(selected)


def repair_transcription(rows):
    """Replace only readings that disagree with the 1859 facsimile."""
    repaired = list(rows)
    for old, new, page in REPAIRS:
        matches = [(number, text.count(old))
                   for number, (_centered, text) in enumerate(repaired)
                   if old in text]
        if sum(count for _number, count in matches) != 1:
            raise ValueError("facsimile repair for p. %d matched %d times" %
                             (page, sum(count for _number, count in matches)))
        number = matches[0][0]
        centered, text = repaired[number]
        repaired[number] = (centered, text.replace(old, new))
    return repaired


def split_units(rows):
    """Use every centered source heading as the edition's own division."""
    units = []
    heading = "Introduction and Opening Prayers"
    body = []
    for centered, text in rows:
        if centered:
            if body:
                units.append((heading, "\n\n".join(body)))
            elif units:
                # The edition sets the direction under LAUDS as another
                # centred line. It is the first line of that division, not
                # an empty division of its own.
                body.append(text)
                continue
            heading = text
            body = []
        else:
            body.append(text)
    if body:
        units.append((heading, "\n\n".join(body)))
    if len(units) != 44:
        raise ValueError("found %d divisions, expected 44" % len(units))

    anchors = [anchor for anchor, _text in units]
    core = anchors.index("KONTAKION 1.")
    end = anchors.index("KONTAKION 13.")
    akathist = anchors[core:end + 1]
    kontakia = [value for value in akathist
                if value.startswith("KONTAKION")]
    oikoi = [value for value in akathist if value.startswith("OIKOS")]
    if len(akathist) != 25 or len(kontakia) != 13 or len(oikoi) != 12:
        raise ValueError("the complete 13-kontakion, 12-oikos sequence is absent")
    expected = []
    for number in range(1, 14):
        suffix = "." if number != 11 else ""
        expected.append("KONTAKION %d%s" % (number, suffix))
        if number <= 12:
            expected.append("OIKOS %d." % number)
    if akathist != expected:
        raise ValueError("the akathist sequence changed: %r" % akathist)
    core_units = units[core:end + 1]
    if sum(text.count("Alleluia") for _anchor, text in core_units) != 12:
        raise ValueError("the twelve Akathist Alleluia refrains are absent")
    odd_quotes = [anchor for anchor, text in units if text.count('"') % 2]
    if odd_quotes:
        raise ValueError("unbalanced quotation marks in %r" % odd_quotes)
    complete_text = "\n".join(text for _anchor, text in units)
    if complete_text.count("vail of the Temple") != 1:
        raise ValueError("the edition's 'vail of the Temple' reading changed")
    if any(mark in complete_text for mark in ("\u2013", "\u2014", "\u2018", "\u2019",
                                               "\u201c", "\u201d")):
        raise ValueError("curly quotation mark or long dash in source text")
    return units


def build():
    raw = fetch_source()
    divisions = split_units(source_paragraphs(raw))
    title = (
        "Acathiston; or, Prayers in honour of the Divine Passion of our "
        "Lord Jesus Christ"
    )
    author = "St Innocent of Kherson and Taurida"
    work = {
        "work_id": WORK_ID,
        "edition_of": EDITION_OF,
        "title": title,
        "author": author,
        "language": "en",
        "date": "composed before 1857; this English translation 1859",
        "translator": "John Mason Neale",
        "pub_year": 1859,
        "publisher": "Joseph Masters, London",
        "source": (
            "Innocent, Archbishop of Odessa, \"Acathiston; or, Prayers in "
            "honour of the Divine Passion of our Lord Jesus Christ,\" in "
            "Voices from the East: Documents on the Present State and "
            "Working of the Oriental Church, chapter VII (London: Joseph "
            "Masters, 1859), pp. 175-205"
        ),
        "source_url": SOURCE_URL,
        "facsimile_url": FACSIMILE_URL,
        "source_class": "liturgical",
        "description": (
            "The 1859 edition identifies the author as Innocent, Archbishop "
            "of Odessa; he is venerated as St Innocent of Kherson and "
            "Taurida. John Mason Neale's English translation contains the "
            "opening prayers, odes and canon, the complete Akathist of "
            "thirteen kontakia and twelve oikoi, the adoration of the five "
            "wounds, and the concluding odes, praises, and troparia. The "
            "wording, capitalization, punctuation, and section order are "
            "those of the 1859 edition."
        ),
        "digitized": "Project Canterbury; facsimile at Internet Archive",
        "license": "Public Domain",
        "rights_url": FACSIMILE_URL,
        "saint": None,
        "is_saint": True,
        "purpose": "The life of prayer",
        "centuries": [19],
        "century": 19,
        "period": "19th century",
    }
    units = []
    for ordinal, (anchor, text) in enumerate(divisions, 1):
        units.append({
            "unit_id": "%s::u%03d" % (WORK_ID, ordinal),
            "work_id": WORK_ID,
            "work_title": title,
            "author": author,
            "source_class": "liturgical",
            "ordinal": ordinal,
            "citation_anchor": anchor,
            "chapter_title": None,
            "text": text,
        })
    canonical = json.dumps(divisions, ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    if CANONICAL_SHA256 and digest != CANONICAL_SHA256:
        raise ValueError("canonical digest %s, expected %s" %
                         (digest, CANONICAL_SHA256))
    return {"work": work, "units": units}, digest


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        payload, digest = build()
        path = OUTDIR / (WORK_ID + ".json")
        body = encoded(payload)
        catalog = json.loads(INDEX.read_text(encoding="utf-8"))
        old = next((row for row in catalog
                    if row.get("work_id") == WORK_ID), None)
        entry = dict(old or {})
        entry.update(payload["work"])
        rows = [row for row in catalog if row.get("work_id") != WORK_ID]
        rows.append(entry)
        rows.sort(key=lambda row: row.get("work_id", ""))
        chars = sum(len(unit["text"]) for unit in payload["units"])
        print("%s: %d units, %s characters, canonical sha256 %s" %
              (WORK_ID, len(payload["units"]), format(chars, ","), digest))
        if args.write:
            path.write_bytes(body)
            INDEX.write_bytes(encoded(rows))
            print("wrote %s" % path.relative_to(ROOT))
        elif not path.exists() or path.read_bytes() != body:
            raise ValueError("stale or missing %s" % path.relative_to(ROOT))
        current = next((row for row in json.loads(
            INDEX.read_text(encoding="utf-8"))
            if row.get("work_id") == WORK_ID), None)
        if current is None or any(
                current.get(field) != value
                for field, value in payload["work"].items()):
            raise ValueError("stale: %s" % INDEX.relative_to(ROOT))
        return 0
    except (KeyError, OSError, ValueError, UnicodeError,
            json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
