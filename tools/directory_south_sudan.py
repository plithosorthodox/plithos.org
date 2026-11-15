#!/usr/bin/env python3
"""Current officially identifiable Eastern Orthodox bodies in South Sudan.

The current Alexandrian diocesan page establishes the Diocese of Juba and
South Sudan. Its February 2025 visit record identifies the Saint Panteleimon
chapel as an active worship body. Historical churches, unnamed communities,
and a foundation-only missionary centre remain in the candidate ledger.

    python tools/directory_south_sudan.py --check
    python tools/directory_south_sudan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_DIOCESE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-episkopi-mpenin-tsoympa-kai-notioy-soydan/?lang=en"
)
AX_VISIT = (
    "https://www.patriarchateofalexandria.com/"
    "istoriki-episkepsi-toy-patriarchi-alexandreias-sto-notio-soydan/"
)
AX_LITURGY = (
    "https://www.patriarchateofalexandria.com/"
    "proti-patriarchiki-theia-leitoyrgia-sto-notio-soydan/"
)


ROWS = {
    "ax-juba": [
        {
            "id": "ss-ax-juba-saint-panteleimon-chapel",
            "parent": "ax-juba",
            "kind": "parish",
            "rank": "Chapel",
            "name": "Saint Panteleimon Chapel in Juba",
            "local": "Παρεκκλήσιο Αγίου Παντελεήμονος στην Τζούμπα",
            "seat": "Juba",
            "country": "SS",
            "address": [
                "within Dr. Linderman's polyclinic",
                "Juba, South Sudan",
            ],
            "sources": [AX_DIOCESE, AX_VISIT, AX_LITURGY],
        },
    ],
}

EXPECTED = {"ax-juba": 1}
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
            if row.get("country") != "SS":
                raise ValueError("%s is outside South Sudan" % row_id)
            if row.get("kind") != "parish":
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "SS",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("South Sudan English name map is out of sync")
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
        print("directory South Sudan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("South Sudan: 1 current officially identifiable worship body")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
