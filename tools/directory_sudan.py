#!/usr/bin/env python3
"""Current officially identifiable Eastern Orthodox bodies in Sudan.

The current Patriarchate of Alexandria register establishes the Holy
Archdiocese of Nubia. A current United Nations damage assessment and the
Patriarchate's own body-level record establish its Annunciation cathedral.

    python tools/directory_sudan.py --check
    python tools/directory_sudan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_NUBIA = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-mitropoli-noyvias/"
)
AX_CATHEDRAL = (
    "https://www.patriarchateofalexandria.com/"
    "patriarchal-divine-liturgy-in-khartoum/?lang=en&print=print"
)
UNOSAT_DAMAGE = (
    "https://www.unosat.org/static/unosat_filesystem/4225/"
    "CE20231504SDN_UNOSAT_Sudan_CHS_20251210_v1-1.pdf"
)


ROWS = {
    "ax-nubia": [
        {
            "id": "sd-ax-khartoum-annunciation-cathedral",
            "parent": "ax-nubia",
            "kind": "parish",
            "rank": "Cathedral",
            "name": "Cathedral Church of the Annunciation of the Theotokos in Khartoum",
            "local": "Ιερός Καθεδρικός Ναός Ευαγγελισμού της Θεοτόκου Χαρτούμ",
            "seat": "Khartoum",
            "country": "SD",
            "sources": [AX_NUBIA, AX_CATHEDRAL, UNOSAT_DAMAGE],
        },
    ],
}

EXPECTED = {"ax-nubia": 1}
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
            if item.get("country") != "SD":
                raise ValueError("%s is outside Sudan" % row_id)
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
            "country": "SD",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Sudan English name map is out of sync")
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
        print("directory Sudan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Sudan: 1 current officially identifiable worship body")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
