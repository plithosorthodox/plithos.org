#!/usr/bin/env python3
"""Current officially named Orthodox bodies for Qatar.

The Jerusalem Patriarchate currently names three worship sites under its
Patriarchal Representation in Qatar. The Antiochian Patriarchate separately
names a Vicariate of the State of Qatar, whose representative is based at the
Archdiocese of Baghdad, Kuwait and Dependencies.

    python tools/directory_qatar.py --check
    python tools/directory_qatar.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-15"

JE_ADMIN = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "patriarchal-management-committees/"
)
JE_ARABIC = (
    "https://ar.jerusalem-patriarchate.info/"
    "%D8%A7%D9%84%D9%86%D9%8A%D8%A7%D8%A8%D8%A7%D8%AA-"
    "%D8%A7%D9%84%D8%A8%D8%B7%D8%B1%D9%8A%D8%B1%D9%83%D9%8A%D8%A9/"
)
JE_CALENDAR = (
    "https://ar.jerusalem-patriarchate.info/wp-content/uploads/2025/03/"
    "ARABIC_CALENDAR_OF_PATRIARCHATE-2025_R.pdf"
)
AN_VICARIATES = (
    "https://www.antiochpatriarchate.org/en/category/"
    "antiochian-vicariates-and-representatives-of-his-beatitude/108/"
)
AN_DIRECTORY = (
    "https://www.antiochpatriarchate.org/images/pages/"
    "dalil-20242023-12-19-07-53-37.pdf"
)

ENGLISH_NAMES = {
    "qa-je-doha-saints-isaac-george-makarios": (
        "Church of St. Isaac the Syriac, St. George, and St. Makarios of Jerusalem"
    ),
    "qa-je-doha-dormition-chapel": (
        "Chapel of the Dormition of the Theotokos in Doha"
    ),
    "qa-je-al-khor-saint-nicholas": (
        "House of Prayer of St. Nicholas in Al Khor"
    ),
    "qa-an-vicariate": "Antiochian Vicariate of the State of Qatar",
}


ROWS = {
    "je-qatar": [
        dict(
            id="qa-je-doha-saints-isaac-george-makarios",
            parent="je-qatar",
            kind="parish",
            rank="Church",
            name=ENGLISH_NAMES["qa-je-doha-saints-isaac-george-makarios"],
            local=(
                "كنيسة القدّيس إسحق السرياني والقديس جيورجيوس "
                "والقديس مكاريوس الأورشليمي في الدوحة"
            ),
            country="QA",
            dedication=(
                "St. Isaac the Syriac, St. George, and St. Makarios of Jerusalem"
            ),
            address=[
                "Patriarchal Representation in Qatar",
                "P.O. Box 23417, Doha, Qatar",
            ],
            site="https://www.qorthodox.org/",
            sources=[JE_ADMIN, JE_ARABIC, JE_CALENDAR],
        ),
        dict(
            id="qa-je-doha-dormition-chapel",
            parent="je-qatar",
            kind="parish",
            rank="Chapel",
            name=ENGLISH_NAMES["qa-je-doha-dormition-chapel"],
            local="كنيسة رقاد والدة الإله في الدوحة",
            country="QA",
            dedication="The Dormition of the Theotokos",
            address=[
                "Patriarchal Representation in Qatar",
                "P.O. Box 23417, Doha, Qatar",
            ],
            site="https://www.qorthodox.org/",
            sources=[JE_ADMIN, JE_ARABIC, JE_CALENDAR],
        ),
        dict(
            id="qa-je-al-khor-saint-nicholas",
            parent="je-qatar",
            kind="parish",
            rank="Prayer House",
            name=ENGLISH_NAMES["qa-je-al-khor-saint-nicholas"],
            local="مصلّى القديس نيقولاوس في الخور",
            country="QA",
            dedication="Saint Nicholas the Wonderworker",
            sources=[JE_ADMIN, JE_ARABIC, JE_CALENDAR],
        ),
    ],
    "an-baghdad": [
        dict(
            id="qa-an-vicariate",
            parent="an-baghdad",
            kind="diocese",
            rank="Vicariate",
            name=ENGLISH_NAMES["qa-an-vicariate"],
            local="معتمدية دولة قطر",
            country="QA",
            address=[
                "Greek Orthodox Archdiocese of Baghdad, Kuwait and Dependencies",
                "P.O. Box 8173, Al-Salmiya 22052, Kuwait",
            ],
            site=AN_VICARIATES,
            sources=[AN_VICARIATES, AN_DIRECTORY],
        ),
    ],
}

EXPECTED_COUNTS = {"je-qatar": 3, "an-baghdad": 1}


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if row.get("site") and not row["site"].startswith("http"):
        raise ValueError("%s carries a non-URL site" % row.get("id"))
    for key in ("address", "languages", "founded"):
        if row.get(key) and (not isinstance(row[key], list) or
                             not all(isinstance(value, str)
                                     for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    for value in row.values():
        texts = value if isinstance(value, list) else [value]
        for text in texts:
            if isinstance(text, str) and ("\u2013" in text or "\u2014" in text):
                raise ValueError("%s carries a forbidden long dash" %
                                 row.get("id"))
    return row


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if row.get("parent") != parent:
                raise ValueError("%s is grouped under the wrong parent" % row_id)
            if row.get("country") != "QA":
                raise ValueError("%s is outside Qatar" % row_id)
            if not row.get("local"):
                raise ValueError("%s lacks its official local identity" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED_COUNTS[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED_COUNTS[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "rows": rows,
            "country": "QA",
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("English name coverage differs from Qatar rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
        }
        for parent, payload in sorted(payloads.items())
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        elif args.check:
            errors = problems(payloads)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("Qatar directory data is current (4 rows)")
        else:
            print(json.dumps(manifest(payloads), ensure_ascii=False,
                             indent=2))
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
