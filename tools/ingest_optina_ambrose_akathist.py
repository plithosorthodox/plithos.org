#!/usr/bin/env python3
"""Build the Church Slavonic Akathist to St Ambrose of Optina.

Optina Monastery publishes the complete received text on its official site
and permits use of site materials when the source is linked. The builder
reads only the article, verifies the full heading sequence and repeated
refrains, and pins the resulting canonical text by digest.

    python tools/ingest_optina_ambrose_akathist.py --check
    python tools/ingest_optina_ambrose_akathist.py --write
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
WORK_ID = "akathist-ambrose-optina-cu"
EDITION_OF = "akathist-ambrose-optina"
URL = "https://www.optina.ru/prayers_akafist_amvr/"
TITLE = "Акафист преподобному Амвросию Оптинскому"
CANONICAL_SHA256 = "001920ea93d18123db3e12510711ff1f693e73fa482685ab8d4d216770ca274d"
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def clean(value):
    value = unicodedata.normalize("NFC", value.replace("\xa0", " "))
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    return value.strip()


class ArticleParser(HTMLParser):
    """Read headings and paragraphs only after the article's exact title."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.article = 0
        self.capture = None
        self.buffer = []
        self.started = False
        self.heading = None
        self.paragraphs = []
        self.divisions = []

    def finish_unit(self):
        if self.heading is not None:
            self.divisions.append(
                (self.heading, "\n\n".join(self.paragraphs))
            )
            self.heading = None
            self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        del attrs
        if tag == "article":
            self.article += 1
        elif self.article and tag in ("h1", "h3", "p") and self.capture is None:
            self.capture = tag
            self.buffer = []
        elif self.article and tag == "br" and self.capture:
            self.buffer.append("\n")

    def handle_endtag(self, tag):
        if self.article and tag == self.capture:
            value = clean("".join(self.buffer))
            if tag == "h1" and value == TITLE:
                self.started = True
            elif self.started and tag == "h3":
                self.finish_unit()
                self.heading = value
            elif (self.started and tag == "p" and self.heading is not None
                  and value and not value.startswith("←")):
                self.paragraphs.append(value)
            self.capture = None
            self.buffer = []
        if tag == "article":
            self.finish_unit()
            self.article -= 1

    def handle_data(self, data):
        if self.article and self.capture:
            self.buffer.append(data)


def fetch_source():
    request = urllib.request.Request(URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def expected_headings():
    headings = []
    for number in range(1, 14):
        headings.append("Конда́к %d" % number)
        if number <= 12:
            headings.append("И́кос %d" % number)
    headings.extend([
        "И́кос 1",
        "Конда́к 1",
        "Моли́твы преподо́бному Амвро́сию, ста́рцу О́птинскому",
        "Тропа́рь, глас 5",
        "Конда́к, глас 2",
    ])
    return headings


def parse_source(raw):
    parser = ArticleParser()
    parser.feed(raw.decode("utf-8"))
    parser.close()
    divisions = parser.divisions
    if not parser.started:
        raise ValueError("the exact article title is absent")
    headings = [heading for heading, _text in divisions]
    if headings != expected_headings():
        raise ValueError("source heading sequence changed: %r" % headings)
    if any(not text for _heading, text in divisions):
        raise ValueError("an empty unit was found")
    if sum(text.count("Аллилу́иа.") for _heading, text in divisions) != 12:
        raise ValueError("the akathist must contain 12 Alleluia closings")
    refrain = (
        "Ра́дуйся, преподо́бне Амвро́сие, богому́дрый учи́телю "
        "ве́ры и благоче́стия."
    )
    if sum(text.count(refrain) for _heading, text in divisions) != 15:
        raise ValueError("the common refrain and its repeated pair are incomplete")
    if any(character in text for _heading, text in divisions
           for character in "\u2013\u2014"):
        raise ValueError("the source contains a typographic dash")
    canonical = json.dumps(
        divisions, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    digest = sha256(canonical)
    if digest != CANONICAL_SHA256:
        raise ValueError("canonical SHA256 %s, expected %s" %
                         (digest, CANONICAL_SHA256))
    return divisions, digest


def build():
    divisions, digest = parse_source(fetch_source())
    work = {
        "work_id": WORK_ID,
        "edition_of": EDITION_OF,
        "title": TITLE,
        "author": "Anonymous",
        "language": "cu",
        "date": "approved in 1988",
        "translator": None,
        "pub_year": 1988,
        "source": (
            "Акафист преподобному Амвросию Оптинскому, approved by the "
            "Russian Orthodox Church under Patriarch Pimen on September 22, "
            "1988; published by Optina Monastery"
        ),
        "source_url": URL,
        "source_class": "liturgical",
        "description": (
            "The complete Church Slavonic Akathist to St Ambrose of Optina: "
            "thirteen kontakia, twelve ikoi, the direction to repeat the "
            "final kontakion and return to the first ikos and kontakion, and "
            "the concluding prayer. This is the text approved by the Russian "
            "Orthodox Church under Patriarch Pimen on September 22, 1988 and "
            "published by Optina Monastery."
        ),
        "digitized": "Optina Monastery",
        "license": "Reuse permitted with source attribution",
        "rights": "Reuse permitted with a source link to www.optina.ru",
        "rights_url": URL,
        "attribution": "Source: Optina Monastery, www.optina.ru",
        "transcription_url": URL,
        "saint": None,
        "is_saint": False,
    }
    units = []
    for ordinal, (heading, text) in enumerate(divisions, 1):
        units.append({
            "unit_id": "%s::u%03d" % (WORK_ID, ordinal),
            "work_id": WORK_ID,
            "work_title": TITLE,
            "author": work["author"],
            "source_class": work["source_class"],
            "ordinal": ordinal,
            "citation_anchor": heading,
            "chapter_title": None,
            "text": text,
        })
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
        output = OUTDIR / (WORK_ID + ".json")
        expected = encoded(payload)
        catalog = json.loads(INDEX.read_text(encoding="utf-8"))
        old = next((row for row in catalog
                    if row.get("work_id") == WORK_ID), None)
        entry = dict(old or {})
        entry.update(payload["work"])
        rows = [row for row in catalog if row.get("work_id") != WORK_ID]
        rows.append(entry)
        rows.sort(key=lambda row: row.get("work_id", ""))
        if args.write:
            output.write_bytes(expected)
            INDEX.write_bytes(encoded(rows))
        if not output.exists() or output.read_bytes() != expected:
            raise ValueError("stale: %s" % output.relative_to(ROOT))
        current = next((row for row in json.loads(
            INDEX.read_text(encoding="utf-8"))
            if row.get("work_id") == WORK_ID), None)
        if current is None or any(
                current.get(field) != value
                for field, value in payload["work"].items()):
            raise ValueError("stale: %s" % INDEX.relative_to(ROOT))
        print("%s: %d units, canonical sha256 %s" %
              (WORK_ID, len(payload["units"]), digest))
        return 0
    except (KeyError, OSError, UnicodeError, ValueError,
            json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
