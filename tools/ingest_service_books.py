#!/usr/bin/env python3
"""Build the public-domain facsimile records in the Service Books section.

The facsimile is the text for these records. The short unit in each payload is
an index of the offices found in the volume so the Library search can find the
book without presenting unverified OCR as liturgical text.

    python tools/ingest_service_books.py --check
    python tools/ingest_service_books.py --write
"""
import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"


BOOKS = [
    {
        "work": {
            "work_id": "service-book-hapgood-1906",
            "title": (
                "Service Book of the Holy Orthodox-Catholic Apostolic "
                "(Greco-Russian) Church"
            ),
            "author": "Orthodox Church",
            "language": "en",
            "date": "1906; revised edition 1922",
            "translator": "Isabel Florence Hapgood",
            "pub_year": 1922,
            "publisher": "Association Press",
            "source": (
                "Service Book of the Holy Orthodox-Catholic Apostolic Church, "
                "revised edition with endorsement by Patriarch Tikhon "
                "(New York: Association Press, 1922)"
            ),
            "source_url": "https://archive.org/details/gtu_A32400004109975B",
            "facsimile_url": (
                "https://archive.org/download/gtu_A32400004109975B/"
                "gtu_A32400004109975B.pdf"
            ),
            "facsimile_label": "Open the complete 615-page facsimile",
            "facsimile_only": True,
            "service_book": True,
            "source_class": "liturgical",
            "description": (
                "The complete 1922 revised edition of Isabel Florence "
                "Hapgood's English service book, compiled and translated "
                "from the Church Slavonic service books of the Russian "
                "Church and collated with Greek service books. Its 615 pages "
                "include the daily offices, the Divine Liturgies, principal "
                "feasts, Baptism, Chrismation, Confession, Crowning, Unction, "
                "ordinations, burial offices, water blessings, prayers for "
                "journeys, thanksgivings, and other blessings. Hapgood states "
                "that no single volume could contain every Orthodox office; "
                "this is the broad selection she judged ordinarily needed."
            ),
            "digitized": "Internet Archive",
            "rights": "Public Domain",
            "rights_url": "https://archive.org/details/gtu_A32400004109975B",
            "saint": None,
            "is_saint": False,
            "purpose": "The life of prayer",
            "centuries": [20],
            "century": 20,
            "period": "20th century",
        },
        "anchor": "Contents of the complete facsimile",
        "text": (
            "Daily offices: Vespers, Matins, the First, Third, Sixth, and "
            "Ninth Hours, Typica, and Great Compline. Divine Liturgies: St "
            "John Chrysostom, St Basil, and the Presanctified Gifts. "
            "Sacramental and pastoral offices: prayers at childbirth and "
            "naming, Baptism, Chrismation, Confession, Crowning, Unction, "
            "ordinations, prayers at death, burials, Panikhida, reception of "
            "converts, water blessings, church and house rites, journeys, "
            "thanksgivings, Moleben, Communion prayers, and blessings of "
            "food and objects. Propers: the principal feasts, Great Thursday, "
            "Great Friday, Great Saturday, Pascha, the Eight Tones, and "
            "explanatory notes."
        ),
    },
    {
        "work": {
            "work_id": "euchology-shann-1891",
            "title": "Euchology: A Manual of Prayers of the Holy Orthodox Church",
            "author": "Orthodox Church",
            "language": "en",
            "date": "1891",
            "translator": "G. V. Shann",
            "pub_year": 1891,
            "publisher": "T. W. Stainbank",
            "source": (
                "Euchology: A Manual of Prayers of the Holy Orthodox Church, "
                "done into English by G. V. Shann (Kidderminster: T. W. "
                "Stainbank, 1891)"
            ),
            "source_url": "https://ccel.org/ccel/shann/euchology/euchology.ii.html",
            "facsimile_url": (
                "https://www.ccel.org/ccel/s/shann/euchology/cache/euchology.pdf"
            ),
            "facsimile_label": "Open the complete public-domain facsimile",
            "facsimile_only": True,
            "service_book": True,
            "source_class": "liturgical",
            "description": (
                "G. V. Shann's 1891 English manual, written principally as a "
                "vade mecum for the laity. It gives a brief but complete "
                "synopsis of the daily worship of the Orthodox Church, "
                "including Vespers, Compline, Nocturns, Matins, the Hours, "
                "Typica, audible portions of the Divine Liturgy, prayers "
                "before and after Holy Communion, Sunday and weekday "
                "offices, services for the principal feasts, the Passion and "
                "Paschal offices, canons, diptychs, and the calendar. This "
                "Library record provides the complete public-domain "
                "facsimile while the text is checked against the printed "
                "pages."
            ),
            "digitized": "Christian Classics Ethereal Library",
            "rights": "Public Domain",
            "rights_url": "https://ccel.org/ccel/shann/euchology/euchology.ii.html",
            "saint": None,
            "is_saint": False,
            "purpose": "The life of prayer",
            "centuries": [19],
            "century": 19,
            "period": "19th century",
        },
        "anchor": "Contents of the complete facsimile",
        "text": (
            "Daily offices: Great Vespers and Great Matins, Little Daily "
            "Vespers, Great and Little Compline, Nocturns, Daily Matins, the "
            "First, Third, Sixth, and Ninth Hours, Typica, and the audible "
            "parts of the Divine Liturgy. Devotions: prayers before and "
            "after Holy Communion, the Diptychs, the Sunday office in the "
            "Eight Tones, weekday offices, penitential canons, the Great "
            "Canon, services of the Passion and Pascha, offices for the "
            "principal feasts, troparia and kontakia for the year, and the "
            "calendar."
        ),
    },
]


def payload(entry):
    work = entry["work"]
    return {
        "work": work,
        "units": [{
            "unit_id": work["work_id"] + "::contents",
            "work_id": work["work_id"],
            "work_title": work["title"],
            "author": work["author"],
            "source_class": work["source_class"],
            "ordinal": 1,
            "citation_anchor": entry["anchor"],
            "chapter_title": None,
            "unit_type": "facsimile_index",
            "text": entry["text"],
        }],
    }


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    built = [payload(entry) for entry in BOOKS]
    rows = json.loads(INDEX.read_text(encoding="utf-8"))
    ids = {item["work"]["work_id"] for item in built}
    rows = [row for row in rows if row.get("work_id") not in ids]
    rows.extend(item["work"] for item in built)
    rows.sort(key=lambda row: row.get("work_id", ""))
    expected_index = encoded(rows)

    if args.write:
        for item in built:
            path = OUTDIR / (item["work"]["work_id"] + ".json")
            path.write_bytes(encoded(item))
        INDEX.write_bytes(expected_index)

    stale = []
    for item in built:
        path = OUTDIR / (item["work"]["work_id"] + ".json")
        if not path.exists() or path.read_bytes() != encoded(item):
            stale.append(str(path.relative_to(ROOT)))
    if json.loads(INDEX.read_text(encoding="utf-8")) != rows:
        stale.append(str(INDEX.relative_to(ROOT)))
    if stale:
        print("stale: " + ", ".join(stale), file=sys.stderr)
        return 1
    print("service books: %d complete facsimile records" % len(built))
    return 0


if __name__ == "__main__":
    sys.exit(main())
