#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Iraq.

The official site of the Antiochian Archdiocese of Baghdad, Kuwait and
Dependencies publishes the current Iraqi liturgy schedule, contact roster,
and parish news. Those records establish two churches in Baghdad and one
parish in Erbil. Older or map-only bodies remain in the candidate ledger.

    python tools/directory_iraq.py --check
    python tools/directory_iraq.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

ARCHDIOCESE = "https://gocarch.info/iraq/"
CONTACTS = "https://gocarch.info/contact/"
ANDREW_FEAST = (
    "https://gocarch.info/news/"
    "%D8%A8%D8%BA%D8%AF%D8%A7%D8%AF-%D8%B9%D9%8A%D8%AF-"
    "%D8%A7%D9%84%D8%B1%D8%B3%D9%88%D9%84-"
    "%D8%A7%D9%86%D8%AF%D8%B1%D8%A7%D9%88%D8%B3-"
    "%D8%B4%D9%81%D9%8A%D8%B9-"
    "%D8%A7%D9%84%D9%83%D9%86%D9%8A%D8%B3%D8%A9/"
)
ERBIL_PARISH = (
    "https://gocarch.info/news/"
    "%D8%A3%D8%B1%D8%A8%D9%8A%D9%84-%D9%85%D8%AD%D8%B7%D8%A7%D8%AA-"
    "%D9%81%D9%8A-%D8%B1%D8%B9%D9%8A%D8%A9-"
    "%D8%A3%D8%B1%D8%A8%D9%8A%D9%84/"
)


def body(row_id, name, local, seat, rank, sources, address=None):
    row = {
        "id": row_id,
        "parent": "an-baghdad",
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "IQ",
        "sources": sources,
    }
    if address:
        row["address"] = address
    return row


ROWS = {
    "an-baghdad": [
        body(
            "iq-an-baghdad-saint-george-cathedral",
            "Saint George Cathedral in Baghdad",
            "كاتدرائية القديس جاورجيوس",
            "Baghdad",
            "Cathedral",
            [ARCHDIOCESE, CONTACTS],
            ["بغداد، حي الرياض، محلة ٩٠٨، شارع ١٧، مبنى ٨٥"],
        ),
        body(
            "iq-an-baghdad-apostle-andrew",
            "Church of the Apostle Andrew in Baghdad",
            "كنيسة الرسول اندراوس",
            "Baghdad",
            "Church",
            [ARCHDIOCESE, ANDREW_FEAST],
            ["بغداد، ساحة الطيران، كمب الكيلاني"],
        ),
        body(
            "iq-an-erbil-saint-abraham",
            "Saint Abraham of Arbela Church in Erbil",
            "كنيسة القديس ابراهيم الاربيلي",
            "Erbil",
            "Church",
            [ARCHDIOCESE, CONTACTS, ERBIL_PARISH],
        ),
    ],
}
EXPECTED = {"an-baghdad": 3}
EXPECTED_TOTAL = 3
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
            if row.get("country") != "IQ":
                raise ValueError("%s is outside Iraq" % row_id)
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
            "country": "IQ",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Iraq must publish exactly %d rows" % EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Iraq English name map is out of sync")
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
        print("directory Iraq: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Iraq: 3 current bodies under the Patriarchate of Antioch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
