#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Tunisia.

The current Patriarchate of Alexandria register establishes the Holy
Archdiocese of Carthage. Official patriarchal and Moscow records establish
three exact current worship bodies in Tunis and Bizerte.

    python tools/directory_tunisia.py --check
    python tools/directory_tunisia.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_CARTHAGE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-carthage/?lang=en"
)
AX_TUNIS_VISIT = (
    "https://www.patriarchateofalexandria.com/"
    "his-beatitude-pays-a-pastoral-visit-to-tunisia/?lang=en"
)
AX_PENTECOST = (
    "https://www.patriarchateofalexandria.com/"
    "sunday-of-pentecost-in-tunis/?lang=en"
)
RU_ROSTER = (
    "https://exarchate-africa.ru/en/dioceses_cat/diocese-of-north-africa/"
)
RU_TUNIS_70 = "https://mospat.ru/en/news/94365/"
ROCOR_TUNIS_70 = (
    "https://www.synod.com/synod/eng2026/20260609_print_entunisia.html"
)


def row(row_id, parent, rank, name, local, seat, address, sources):
    return {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "TN",
        "address": address,
        "sources": sources,
    }


ROWS = {
    "ax-carthage": [
        row(
            "tn-ax-tunis-saint-george",
            "ax-carthage",
            "Cathedral",
            "Metropolitan Church of Saint George in Tunis",
            "Ιερός Μητροπολιτικός Ναός Αγίου Γεωργίου Τύνιδος",
            "Tunis",
            ["5 Rue de Rome", "1000 Tunis, Tunisie"],
            [AX_CARTHAGE, AX_TUNIS_VISIT, AX_PENTECOST],
        ),
    ],
    "ru-north-africa": [
        row(
            "tn-ru-tunis-resurrection-christ",
            "ru-north-africa",
            "Church",
            "Church of the Resurrection of Christ in Tunis",
            "Храм Воскресения Христова в Тунисе",
            "Tunis",
            ["12 Avenue Mohamed V", "Tunis, Tunisie"],
            [RU_ROSTER, RU_TUNIS_70, ROCOR_TUNIS_70],
        ),
        row(
            "tn-ru-bizerte-alexander-nevsky",
            "ru-north-africa",
            "Church",
            "Church of Saint Alexander Nevsky in Bizerte",
            "Храм святого благоверного великого князя Александра Невского в Бизерте",
            "Bizerte",
            ["Eglise Russe", "Rue d'Espagne prolongee", "Bizerte, Tunisie"],
            [RU_ROSTER],
        ),
    ],
}

EXPECTED = {"ax-carthage": 1, "ru-north-africa": 2}
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
            if item.get("country") != "TN":
                raise ValueError("%s is outside Tunisia" % row_id)
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
            "country": "TN",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Tunisia English name map is out of sync")
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
        print("directory Tunisia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Tunisia: 3 current officially named bodies across 2 jurisdictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
