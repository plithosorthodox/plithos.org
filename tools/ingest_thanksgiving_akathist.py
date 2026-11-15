#!/usr/bin/env python3
"""Build Pankovskyi's English Akathist of Thanksgiving.

The manuscript is a transcription of the complete translation printed in
TranscUlturAl 1, no. 4 (2011), pages 91-102. The journal places the work under
the Creative Commons Attribution 3.0 License. The source names Iaroslav
Pankovskyi as the translator from Ukrainian and names the original author as
unknown.

This command writes only the work payload. Catalogue publication and the
reader-facing indexes remain separate editorial steps.

    python tools/ingest_thanksgiving_akathist.py --check
    python tools/ingest_thanksgiving_akathist.py --write
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT = ROOT / "tools" / "manuscripts" / "pankovskyi_gratitude_2011.json"
OUTPUT = ROOT / "data" / "library" / "akathist-thanksgiving-en.json"
INDEX = ROOT / "data" / "library" / "works-index.json"
WORK_ID = "akathist-thanksgiving-en"
TITLE = "ACATHISTUS: Gratitude to God for Everything (English)"
TEXT_SHA256 = "c5b9b3afa48d3a6554d29769c93aa540610718533faf0dc8c679d9dc98d3b9d6"
SOURCE_PDF_SHA256 = "b406abdba380bf716077c2d62f1d3eaa5735d97ba19b9cf78a664ff3b4c5f479"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def text_digest(units):
    divisions = [[unit["citation_anchor"], unit["text"]] for unit in units]
    canonical = json.dumps(
        divisions, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def expected_headings():
    headings = []
    for number in range(1, 14):
        headings.append("Kontakion %d" % number)
        if number <= 12:
            headings.append("Oikos %d" % number)
    return headings


def validate_work(work):
    expected = {
        "work_id": WORK_ID,
        "edition_of": "akathist-thanksgiving",
        "title": TITLE,
        "author": "Anonymous",
        "language": "en",
        "translator": "Iaroslav Pankovskyi",
        "pub_year": 2011,
        "source_url": (
            "https://journals.library.ualberta.ca/tc/index.php/TC/"
            "article/download/9850/7751/24819"
        ),
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "source_class": "liturgical",
        "rights": (
            "This work is licensed under a Creative Commons Attribution "
            "3.0 License."
        ),
        "license": "Creative Commons Attribution 3.0",
        "rights_url": "https://creativecommons.org/licenses/by/3.0/",
        "attribution": (
            "Introduction and translation from Ukrainian by Iaroslav "
            "Pankovskyi, University of Alberta"
        ),
        "source_language": "Ukrainian",
    }
    for field, value in expected.items():
        if work.get(field) != value:
            raise ValueError("%s changed: %r" % (field, work.get(field)))
    if "CC BY 3.0" not in work.get("license_attribution", ""):
        raise ValueError("the complete CC BY 3.0 attribution is missing")
    if "en dash in Kontakion 1" not in work.get("license_changes", ""):
        raise ValueError("the required change notice is missing")


def build():
    manuscript = json.loads(MANUSCRIPT.read_text(encoding="utf-8"))
    work = manuscript["work"]
    validate_work(work)

    source_units = manuscript["units"]
    headings = [unit.get("citation_anchor") for unit in source_units]
    if headings != expected_headings():
        raise ValueError("the 25 source headings are incomplete or out of order")
    if [unit.get("ordinal") for unit in source_units] != list(range(1, 26)):
        raise ValueError("the source ordinals are incomplete or out of order")
    if any(not unit.get("text", "").strip() for unit in source_units):
        raise ValueError("the manuscript contains an empty stanza")

    digest = text_digest(source_units)
    if digest != TEXT_SHA256:
        raise ValueError("text SHA256 %s, expected %s" % (digest, TEXT_SHA256))
    if sum(unit["text"].count("Alleluia") for unit in source_units) != 12:
        raise ValueError("the akathist must contain twelve Alleluia closings")
    refrain = "Glory to You, Lord, forever"
    if sum(unit["text"].count(refrain) for unit in source_units) != 13:
        raise ValueError("the thanksgiving refrain must occur thirteen times")

    forbidden = "\u2013\u2014\u2018\u2019\u201c\u201d"
    for unit in source_units:
        if any(character in unit["text"] for character in forbidden):
            raise ValueError(
                "%s contains forbidden punctuation" % unit["citation_anchor"]
            )

    units = []
    for ordinal, source in enumerate(source_units, 1):
        units.append({
            "unit_id": "%s::u%03d" % (WORK_ID, ordinal),
            "work_id": WORK_ID,
            "work_title": TITLE,
            "author": work["author"],
            "source_class": work["source_class"],
            "ordinal": ordinal,
            "citation_anchor": source["citation_anchor"],
            "chapter_title": None,
            "text": source["text"],
        })
    return {"work": work, "units": units}, digest


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        payload, digest = build()
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
            OUTPUT.write_bytes(expected)
            INDEX.write_bytes(encoded(rows))
        if not OUTPUT.exists() or OUTPUT.read_bytes() != expected:
            raise ValueError("stale: %s" % OUTPUT.relative_to(ROOT))
        current = next((row for row in json.loads(
            INDEX.read_text(encoding="utf-8"))
            if row.get("work_id") == WORK_ID), None)
        if current is None or any(
                current.get(field) != value
                for field, value in payload["work"].items()):
            raise ValueError("stale: %s" % INDEX.relative_to(ROOT))
        print("%s: %d units, text sha256 %s" % (
            WORK_ID, len(payload["units"]), digest
        ))
        return 0
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
