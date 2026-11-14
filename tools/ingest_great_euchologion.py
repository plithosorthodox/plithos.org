#!/usr/bin/env python3
"""Build the 1869 Great Euchologion record and its seven formal prayers.

The source transcript is checked against the printed pages in the public-
domain Venice facsimile. The ingester verifies both the fixed source file and
the hash of every prayer before it writes the Library payload.

    python tools/ingest_great_euchologion.py --check
    python tools/ingest_great_euchologion.py --write
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "tools" / "manuscripts" / "great_euchologion_1869_exorcisms.json"
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
WORK_ID = "great-euchologion-1869-el"
SOURCE_JSON_SHA256 = "b345d6c84ba6bc9ce3334c7cf880528a10df11b0b5f61be1af21a9244d56e15e"
PDF_SHA256 = "a1fd0b94b7cfddeb8d1d8d307a3a9aa53aef22142556f80baf7ee421d4b5e7d5"


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def read_source():
    raw = SOURCE.read_bytes()
    source_json_digest = sha256(raw)
    if SOURCE_JSON_SHA256 and source_json_digest != SOURCE_JSON_SHA256:
        raise ValueError("source JSON SHA256 %s, expected %s" %
                         (source_json_digest, SOURCE_JSON_SHA256))
    data = json.loads(raw.decode("utf-8"))
    if data.get("schema") != "plithos.source-transcription.v1":
        raise ValueError("unexpected source transcription schema")
    record = data.get("library_record") or {}
    source = data.get("source") or {}
    if record.get("work_id") != WORK_ID:
        raise ValueError("source work_id does not match %s" % WORK_ID)
    if source.get("pdf_sha256") != PDF_SHA256:
        raise ValueError("facsimile SHA256 changed")
    units = data.get("units") or []
    if len(units) != 7:
        raise ValueError("found %d prayers, expected 7" % len(units))
    if [unit.get("ordinal") for unit in units] != list(range(1, 8)):
        raise ValueError("prayer ordinals are not 1 through 7")
    expected_attributions = (["Μέγας Βασίλειος"] * 3 +
                             ["Ἰωάννης ὁ Χρυσόστομος"] * 4)
    if [unit.get("traditional_attribution") for unit in units] != expected_attributions:
        raise ValueError("traditional attribution sequence changed")
    for unit in units:
        text = unit.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("prayer %s has no text" % unit.get("ordinal"))
        digest = sha256(text.encode("utf-8"))
        if digest != unit.get("text_sha256"):
            raise ValueError("prayer %s text SHA256 changed" % unit.get("ordinal"))
        if not unit.get("heading") or not unit.get("page_anchor"):
            raise ValueError("prayer %s is missing its printed heading or pages" %
                             unit.get("ordinal"))
    return data, source_json_digest


def build():
    data, source_digest = read_source()
    record = data["library_record"]
    source = data["source"]
    title = record["short_title"]
    full_source = "%s (%s; %s: %s, %d)" % (
        source["title"], source["edition"], source["publication_place"],
        source["publisher"], source["publication_year"])
    work = {
        "work_id": WORK_ID,
        "title": title,
        "author": "Orthodox Church",
        "language": "el",
        "date": "1869",
        "translator": None,
        "pub_year": 1869,
        "publisher": source["publisher"],
        "source": full_source,
        "source_url": source["source_url"],
        "facsimile_url": source["source_url"],
        "facsimile_label": "Open the complete 696-page facsimile",
        "facsimile_only": False,
        "service_book": True,
        "source_class": "liturgical",
        "description": (
            "The complete 1869 Venice edition of the Great Euchologion in "
            "Greek. It contains the services of the seven Mysteries, the "
            "daily cycle, blessings, consecrations, prayers for particular "
            "needs, the baptismal exorcisms, and the seven formal exorcism "
            "prayers traditionally attributed to St Basil the Great and St "
            "John Chrysostom. This Library record provides the complete "
            "public-domain facsimile and a checked transcription of the "
            "seven formal exorcism prayers."
        ),
        "digitized": "Google Books, via Wikimedia Commons",
        "rights": "Public Domain",
        "rights_url": source["source_url"],
        "editor": record["editor"],
        "edition": record["edition"],
        "source_pdf_sha256": source["pdf_sha256"],
        "transcribed_pages": source["printed_pages"],
        "saint": None,
        "is_saint": False,
        "purpose": "The life of prayer",
        "centuries": [19],
        "century": 19,
        "period": "19th century",
    }
    units = []
    for source_unit in data["units"]:
        ordinal = source_unit["ordinal"]
        units.append({
            "unit_id": "%s::prayer-%d" % (WORK_ID, ordinal),
            "work_id": WORK_ID,
            "work_title": title,
            "author": work["author"],
            "source_class": work["source_class"],
            "ordinal": ordinal,
            "citation_anchor": source_unit["heading"],
            "chapter_title": data["section_heading"],
            "unit_type": "formal_exorcism_prayer",
            "traditional_attribution": source_unit["traditional_attribution"],
            "printed_minister_label": source_unit.get("printed_minister_label"),
            "normalized_minister_role": source_unit["normalized_minister_role"],
            "rubric": source_unit.get("rubric"),
            "page_anchor": source_unit["page_anchor"],
            "editorial_notes": source_unit.get("editorial_notes") or [],
            "text_sha256": source_unit["text_sha256"],
            "source_text_sha256": source_unit["text_sha256"],
            "text": source_unit["text"],
        })
    return {"work": work, "units": units}, source_digest


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        payload, source_digest = build()
        path = OUTDIR / (WORK_ID + ".json")
        expected = encoded(payload)
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        rows = [row for row in index if row.get("work_id") != WORK_ID]
        rows.append(payload["work"])
        rows.sort(key=lambda row: row.get("work_id", ""))
        if args.write:
            path.write_bytes(expected)
            INDEX.write_bytes(encoded(rows))
        stale = []
        if not path.exists() or path.read_bytes() != expected:
            stale.append(str(path.relative_to(ROOT)))
        if json.loads(INDEX.read_text(encoding="utf-8")) != rows:
            stale.append(str(INDEX.relative_to(ROOT)))
        if stale:
            raise ValueError("stale: " + ", ".join(stale))
        print("%s: %d prayers, source sha256 %s" %
              (WORK_ID, len(payload["units"]), source_digest))
        return 0
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
