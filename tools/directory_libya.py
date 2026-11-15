#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Libya.

The current Patriarchate of Alexandria register establishes the Holy
Metropolis of Libya and identifies its metropolitan church in Tripoli.
Other historical or visiting-service records remain in the candidate ledger.

    python tools/directory_libya.py --check
    python tools/directory_libya.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_LIBYA = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-mitropoli-mpotsoyanas/"
)
PASCHA_2026 = "https://vema.com.au/the-feast-of-pascha-in-tripoli-libya/"
PASTORAL_2026 = "https://vema.com.au/pastoral-visit-to-tripoli-libya/"


ROWS = {
    "ax-libya": [
        {
            "id": "ly-ax-tripoli-saint-george-slaves",
            "parent": "ax-libya",
            "kind": "parish",
            "rank": "Metropolitan Church",
            "name": "Metropolitan Church of Saint George of the Slaves in Tripoli",
            "local": "Ιερός Μητροπολιτικός Ναός Αγίου Γεωργίου των Σκλάβων Τριπόλεως",
            "seat": "Tripoli",
            "country": "LY",
            "address": [
                "Saint Mary's Square",
                "Old Town, Tripoli, Libya",
            ],
            "sources": [AX_LIBYA, PASCHA_2026, PASTORAL_2026],
        },
    ],
}

EXPECTED = {"ax-libya": 1}
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for rows in ROWS.values()
    for item in rows
}
ENGLISH_SEATS = {
    item["seat"]: item["seat"]
    for rows in ROWS.values()
    for item in rows
}


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % item.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    rendered = json.dumps(item, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         item.get("id"))
    return item


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if item.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if item.get("country") != "LY":
                raise ValueError("%s is outside Libya" % row_id)
            if item.get("kind") != "parish":
                raise ValueError("%s has an unsupported kind" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(item)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "LY",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Libya English name map is out of sync")
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
        print("directory Libya: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Libya: 1 current officially named worship body")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
