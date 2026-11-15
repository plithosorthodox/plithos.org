#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Mongolia.

The Moscow Patriarchate's current foreign institutions directory and its
March 2026 parish report establish one current Orthodox parish in Mongolia.

    python tools/directory_mongolia.py --check
    python tools/directory_mongolia.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
FOREIGN_INSTITUTIONS = "https://calendar.rop.ru/?inc=12"
CURRENT_REPORT = "https://mospat.ru/ru/news/94072/"
HISTORY = "https://pravoslavie.ru/159479.html"


DIRECT_RUSSIA_ROWS = [
    {
        "id": "mn-ru-ulaanbaatar-holy-trinity",
        "parent": "russia",
        "kind": "parish",
        "rank": "Stavropegic Parish",
        "name": "Holy Trinity Parish in Ulaanbaatar",
        "local": "Свято-Троицкий приход в Улан-Баторе",
        "seat": "Ulaanbaatar",
        "country": "MN",
        "checked": CHECKED,
        "address": [
            "Bayanzurkh District, 15th Microdistrict",
            "55a Marshal Zhukov Avenue, Ulaanbaatar",
        ],
        "sources": [FOREIGN_INSTITUTIONS, CURRENT_REPORT, HISTORY],
    },
]

EXPECTED_TOTAL = 1
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for row in DIRECT_RUSSIA_ROWS
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for row in DIRECT_RUSSIA_ROWS
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
    for key in ("address", "languages", "founded"):
        if row.get(key) and (
                not isinstance(row[key], list) or
                not all(isinstance(value, str) for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    return row


def build():
    rows = []
    seen = {"russia"}
    for source in DIRECT_RUSSIA_ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != "russia" or row.get("country") != "MN":
            raise ValueError("%s hangs outside Mongolia's direct branch" %
                             row_id)
        if row.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable name" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED_TOTAL:
        raise ValueError("Mongolia must publish exactly one current row")
    if set(ENGLISH_NAMES) != seen - {"russia"}:
        raise ValueError("Mongolia English name map is out of sync")
    return {
        "russia": {
            "v": 1,
            "parent": "russia",
            "country": "MN",
            "rows": rows,
        }
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Mongolia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Mongolia: 1 current stavropegic parish in Ulaanbaatar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
