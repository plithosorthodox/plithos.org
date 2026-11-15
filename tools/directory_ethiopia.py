#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Ethiopia.

The current Alexandrian archdiocese page establishes the territorial see in
Addis Ababa. The Patriarchate's own Greek record names Saint Frumentius as
the cathedral of the Greek community. Bodies that maps or older records
suggest, but that no current competent Church roster confirms, remain in the
country candidate ledger.

    python tools/directory_ethiopia.py --check
    python tools/directory_ethiopia.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_DIOCESE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-aksum/?lang=en"
)
AX_CATHEDRAL_GREEK = (
    "https://www.patriarchateofalexandria.com/"
    "istoriki-enthronisi-toy-neoy-mitropolitoy-axomis/"
)
MAP_CATHEDRAL = (
    "https://www.waze.com/live-map/directions/"
    "st-froumentios-greek-orthodox-church-haile-selassie-street-"
    "addis-ababa-%E1%8A%A0%E1%8B%B2%E1%88%B5-%E1%8A%A0%E1%89%A0%E1%89%A3"
    "?to=place.w.25428058.254018440.14815945"
)


ROWS = {
    "ax-aksum": [
        {
            "id": "et-ax-addis-ababa-saint-frumentius-cathedral",
            "parent": "ax-aksum",
            "kind": "parish",
            "rank": "Cathedral",
            "name": "Saint Frumentius Cathedral of the Greek Community of Addis Ababa",
            "local": (
                "Ιερός Καθεδρικός Ναός Αγίου Φρουμεντίου της Ελληνικής "
                "Κοινότητας Αντίς Αμπέμπα"
            ),
            "seat": "Addis Ababa",
            "country": "ET",
            "address": [
                "Haile Selassie Street",
                "Addis Ababa",
                "Ethiopia",
            ],
            "sources": [AX_DIOCESE, AX_CATHEDRAL_GREEK, MAP_CATHEDRAL],
        },
    ],
}
EXPECTED = {"ax-aksum": 1}
EXPECTED_TOTAL = 1
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in ROWS.values()
    for row in rows
}


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    return row


def build():
    payloads = {}
    seen = set(ROWS)
    total = 0
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if row.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if row.get("country") != "ET":
                raise ValueError("%s is outside Ethiopia" % row_id)
            if row.get("kind") != "parish":
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        total += len(rows)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "ET",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Ethiopia must publish exactly %d row" %
                         EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Ethiopia English name map is out of sync")
    return payloads


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Ethiopia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Ethiopia: 1 current body under the Patriarchate of Alexandria")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
