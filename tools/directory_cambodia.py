#!/usr/bin/env python3
"""Current officially named canonical Orthodox bodies in Cambodia.

The official Cambodian parish directory of the Moscow Patriarchate names two
church parishes and one parish in formation. The current regional map and
recent worship records independently confirm the two church parishes.

    python tools/directory_cambodia.py --check
    python tools/directory_cambodia.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
PARENT = "ru-thailand"
PARISHES = "https://orthodoxchurchcambodia.org/english-version-parishes/"
MAP = "https://exarchate.asia/en/karta-prihodov/"
PHNOM_PENH = (
    "https://orthodoxchurchcambodia.org/2024/09/06/"
    "%D0%BF%D0%B0%D1%82%D1%80%D0%B8%D0%B0%D1%80%D1%88%D0%B8%D0%B9-"
    "%D1%8D%D0%BA%D0%B7%D0%B0%D1%80%D1%85-"
    "%D1%8E%D0%B3%D0%BE-%D0%B2%D0%BE%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%BE%D0%B9-"
    "%D0%B0%D0%B7%D0%B8%D0%B8/"
)
CAMBODIA_HOME = "https://orthodoxchurchcambodia.org/"


ROWS = [
    {
        "id": "kh-ru-phnom-penh-saint-george",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": "Parish of the Holy Great-Martyr George in Phnom Penh",
        "local": "Parish of the Holy Great-Martyr George",
        "dedication": "The Holy Great-Martyr George",
        "seat": "Phnom Penh",
        "country": "KH",
        "address": [
            "Phum Roung Chakr, Sangkat Phnom Penh Thmey",
            "Khan Sen Sok, Phnom Penh, Kingdom of Cambodia",
        ],
        "languages": ["Church Slavonic", "English", "Khmer"],
        "founded": ["Parish founded: in 2012"],
        "sources": [PARISHES, PHNOM_PENH, MAP],
    },
    {
        "id": "kh-ru-sihanoukville-saint-panteleimon",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": "Parish of the Holy Great-Martyr Panteleimon in Sihanoukville",
        "local": "Parish of the Holy Great-Martyr Panteleimon",
        "dedication": "The Holy Great-Martyr and Healer Panteleimon",
        "seat": "Sihanoukville",
        "country": "KH",
        "address": [
            "Phum 3, Sangkat 3",
            "Sihanoukville, Kingdom of Cambodia",
        ],
        "languages": ["Church Slavonic", "Khmer"],
        "founded": ["Parish founded: 2012"],
        "sources": [PARISHES, CAMBODIA_HOME, MAP],
    },
    {
        "id": "kh-ru-siem-reap-kazan-icon",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish in Formation",
        "name": "Parish of Our Lady of Kazan in Siem Reap",
        "local": "Parish of Our Lady of Kazan",
        "dedication": "The Kazan Icon of the Mother of God",
        "seat": "Siem Reap",
        "country": "KH",
        "address": ["Siem Reap, Kingdom of Cambodia"],
        "languages": ["Church Slavonic", "English", "Khmer"],
        "founded": ["Parish founded: 2022"],
        "sources": [PARISHES],
    },
]

EXPECTED = 3
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}
FORBIDDEN_FIELDS = {
    "contact", "contacts", "email", "phone", "telephone", "clergy",
    "priest", "rector", "abbot", "abbess",
}
FORBIDDEN_PUNCTUATION = (
    "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d", "\ufffd",
)


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if len(sources) != len(set(sources)):
        raise ValueError("%s repeats a source" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if FORBIDDEN_FIELDS.intersection(row):
        raise ValueError("%s carries contact or personnel prose" % row.get("id"))
    for key in ("address", "languages", "founded", "sources", "cite"):
        if row.get(key) and (
                not isinstance(row[key], list) or
                not all(isinstance(value, str) for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in FORBIDDEN_PUNCTUATION):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    return row


def build():
    rows = []
    seen = set()
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != PARENT or row.get("country") != "KH":
            raise ValueError("%s is grouped outside Cambodia" % row_id)
        if row.get("kind") != "parish" or row.get("rank") not in {
                "Parish", "Parish in Formation"}:
            raise ValueError("%s has an unsupported kind or rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable official identity" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED:
        raise ValueError("Cambodia must publish exactly %d rows" % EXPECTED)
    if set(ENGLISH_NAMES) != seen:
        raise ValueError("Cambodia English name map is out of sync")
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "KH",
            "rows": rows,
        },
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
        print("directory Cambodia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Cambodia: 3 current bodies under 1 canonical branch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
