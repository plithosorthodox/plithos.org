#!/usr/bin/env python3
"""Current officially named canonical Orthodox bodies in Laos.

Current official exarchal records establish one registered Russian Orthodox
parish in Vientiane, with regular worship and a church-building project.

    python tools/directory_laos.py --check
    python tools/directory_laos.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
PARENT = "ru-thailand"
PERMIT = (
    "https://exarchate.asia/2025/04/08/"
    "prihod-russkoj-pravoslavnoj-czerkvi-v-laose-poluchil-"
    "razreshenie-na-osushhestvlenie-religioznoj-deyatelnosti/"
)
LITURGY = (
    "https://exarchate.asia/en/2026/06/07/"
    "v-nedelyu-1-yu-po-pyatidesyatnicze-patriarshij-ekzarh-"
    "yugo-vostochnoj-azii-sovershil-bozhestvennuyu-liturgiyu-"
    "v-hrame-svyatogo-blagovernogo-velikogo-knyazya-aleksandra-"
    "nevskogo-v-g-ventyan-laos/"
)
CURRENT = (
    "https://exarchate.asia/en/2026/06/10/"
    "patriarshij-ekzarh-yugo-vostochnoj-azii-provyol-ryad-"
    "oficzialnyh-vstrech-v-stolicze-laosskoj-narodno-"
    "demokraticheskoj-respubliki/"
)


ROWS = [
    {
        "id": "la-ru-vientiane-saint-alexander-nevsky",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish",
        "name": (
            "Parish of the Holy Right-Believing Grand Prince "
            "Alexander Nevsky in Vientiane"
        ),
        "local": (
            "приход святого благоверного великого князя "
            "Александра Невского в Вьентьяне"
        ),
        "dedication": "Saint Alexander Nevsky",
        "seat": "Vientiane",
        "country": "LA",
        "address": ["Vientiane, Laos"],
        "sources": [PERMIT, LITURGY, CURRENT],
    },
]

EXPECTED = 1
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
        if row.get("parent") != PARENT or row.get("country") != "LA":
            raise ValueError("%s is grouped outside Laos" % row_id)
        if row.get("kind") != "parish" or row.get("rank") != "Parish":
            raise ValueError("%s has an unsupported kind or rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable official identity" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED:
        raise ValueError("Laos must publish exactly one current row")
    if set(ENGLISH_NAMES) != seen:
        raise ValueError("Laos English name map is out of sync")
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "LA",
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
        print("directory Laos: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Laos: 1 current body under 1 canonical branch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
