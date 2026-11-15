#!/usr/bin/env python3
"""Current officially named canonical Orthodox bodies in Vietnam.

The Philippines and Vietnam Diocese's current clergy roster and recent parish
records establish four current parishes. The exarchal map supplies the older
three-parish baseline and the one exact street address it publishes.

    python tools/directory_vietnam.py --check
    python tools/directory_vietnam.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
PARENT = "ru-philippines-and-vietnam"
CLERGY = "https://phvieparchy.org/en/priesthood/"
MAP = "https://exarchate.asia/en/karta-prihodov/"
HANOI = "https://phvieparchy.org/en/parish-news/novyj-klirik-v-hanoe/"
NHA_TRANG = "https://phvieparchy.org/en/parish-news/liturgiya-v-nyachange-3/"
VUNG_TAU = "https://phvieparchy.org/en/parish-news/prestolnyj-prazdnik-v-vungtau-3/"
HO_CHI_MINH = (
    "https://phvieparchy.org/en/parish-news/"
    "pokrov-presvyatoj-bogorodiczy-5/"
)


ROWS = [
    {
        "id": "vn-ru-hanoi-saint-xenia",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": "Saint Xenia of Petersburg Parish in Hanoi",
        "local": "Saint Xenia of Petersburg Parish, Hanoi",
        "dedication": "Saint Xenia of Petersburg",
        "seat": "Hanoi",
        "country": "VN",
        "address": ["Hanoi, Vietnam"],
        "sources": [CLERGY, HANOI, MAP],
    },
    {
        "id": "vn-ru-nha-trang-saint-nicholas",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": "Saint Nicholas the Wonderworker Parish in Nha Trang",
        "local": "Saint Nicholas the Wonderworker Parish, Nha Trang",
        "dedication": "Saint Nicholas the Wonderworker",
        "seat": "Nha Trang",
        "country": "VN",
        "address": ["Nha Trang, Vietnam"],
        "sources": [CLERGY, NHA_TRANG],
    },
    {
        "id": "vn-ru-vung-tau-kazan-icon",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": "Kazan Icon of the Mother of God Parish in Vung Tau",
        "local": "Kazan icon of the Mother of God Parish, Vung Tau",
        "dedication": "The Kazan Icon of the Mother of God",
        "seat": "Vung Tau",
        "country": "VN",
        "address": [
            "2 Nguyen Thai Hoc, Ward 7",
            "Vung Tau City, Ba Ria Vung Tau, Vietnam",
        ],
        "sources": [CLERGY, VUNG_TAU, MAP],
    },
    {
        "id": "vn-ru-ho-chi-minh-intercession",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": "Intercession of the Mother of God Parish in Ho Chi Minh City",
        "local": "Intercession of the Mother of God Parish, Ho Chi Minh City",
        "dedication": "The Intercession of the Mother of God",
        "seat": "Ho Chi Minh City",
        "country": "VN",
        "address": ["Ho Chi Minh City, Vietnam"],
        "sources": [CLERGY, HO_CHI_MINH, MAP],
    },
]

EXPECTED = 4
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
        if row.get("parent") != PARENT or row.get("country") != "VN":
            raise ValueError("%s is grouped outside Vietnam" % row_id)
        if row.get("kind") != "parish" or row.get("rank") != "Parish":
            raise ValueError("%s has an unsupported kind or rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable official identity" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED:
        raise ValueError("Vietnam must publish exactly %d rows" % EXPECTED)
    if set(ENGLISH_NAMES) != seen:
        raise ValueError("Vietnam English name map is out of sync")
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "VN",
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
        print("directory Vietnam: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Vietnam: 4 current bodies under 1 canonical branch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
