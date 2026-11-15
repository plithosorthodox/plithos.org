#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Tajikistan.

The Dushanbe Diocese's fifteenth-anniversary review names seven active
churches in 2026. Current diocesan reports also establish five worship
communities which clergy visit for prayer and pastoral care.

    python tools/directory_tajikistan.py --check
    python tools/directory_tajikistan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
PARENT = "ru-dushanbe"
DIOCESE_REVIEW = "https://lifted.asia/?p=25406"
CATHEDRAL = "https://lifted.asia/?p=25254"
TURSUNZADE = "https://lifted.asia/?p=25321"
IVERON_BASE = "https://lifted.asia/?p=11726"
NUREK = "https://lifted.asia/?p=21263"
DUSTI = "https://lifted.asia/?p=25150"
COMMUNITIES = "https://lifted.asia/?p=24383"
KULYAB = "https://lifted.asia/?p=23952"
PANJIKENT = "https://lifted.asia/?p=23517"
PANJ_DUSTI = "https://lifted.asia/?p=22824"
SHAARTUZ = "https://lifted.asia/?p=22503"


def body(row_id, name, local, seat, rank="Church", sources=None):
    return {
        "id": row_id,
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "TJ",
        "sources": list(sources or [DIOCESE_REVIEW]),
    }


ROWS = [
    body(
        "tj-ru-dushanbe-saint-nicholas-cathedral",
        "Saint Nicholas Cathedral in Dushanbe",
        "Свято-Никольский кафедральный собор",
        "Dushanbe",
        rank="Cathedral",
        sources=[DIOCESE_REVIEW, CATHEDRAL],
    ),
    body(
        "tj-ru-tursunzade-protection-theotokos",
        "Protection of the Most Holy Theotokos Church in Tursunzade",
        "Храм Покрова Пресвятой Богородицы",
        "Tursunzade",
        sources=[DIOCESE_REVIEW, TURSUNZADE],
    ),
    body(
        "tj-ru-khujand-saint-mary-magdalene",
        "Saint Mary Magdalene Church in Khujand",
        "Храм равноапостольной Марии Магдалины",
        "Khujand",
    ),
    body(
        "tj-ru-buston-iveron-icon",
        "Iveron Icon of the Mother of God Church in Buston",
        "Храм Иверской иконы Божией Матери",
        "Buston",
    ),
    body(
        "tj-ru-bokhtar-archangel-michael",
        "Archangel Michael Church in Bokhtar",
        "Храм Архистратига Михаила",
        "Bokhtar",
    ),
    body(
        "tj-ru-dushanbe-iveron-military-chapel",
        "Iveron Icon of the Mother of God Military Chapel in Dushanbe",
        "Храм-часовня Иверской иконы Божией Матери при 201-й военной базе",
        "Dushanbe",
        rank="Military Parish",
        sources=[DIOCESE_REVIEW, IVERON_BASE],
    ),
    body(
        "tj-ru-nurek-saint-alexander-nevsky-chapel",
        "Saint Alexander Nevsky Military Chapel in Nurek",
        "Храм-часовня святого благоверного князя Александра Невского",
        "Nurek",
        rank="Military Parish",
        sources=[DIOCESE_REVIEW, NUREK],
    ),
    body(
        "tj-ru-kulyab-orthodox-community",
        "Orthodox Community and Cemetery Chapel in Kulyab",
        "Православная община Куляба и часовня на русском кладбище",
        "Kulyab",
        rank="Church Community",
        sources=[COMMUNITIES, KULYAB],
    ),
    body(
        "tj-ru-panjikent-orthodox-community",
        "Orthodox Community in Panjikent",
        "Православная община Пенджикента",
        "Panjikent",
        rank="Community",
        sources=[COMMUNITIES, PANJIKENT],
    ),
    body(
        "tj-ru-dusti-orthodox-community",
        "Orthodox Community in Dusti",
        "Православная община посёлка Дусти",
        "Dusti",
        rank="Community",
        sources=[DUSTI, PANJ_DUSTI],
    ),
    body(
        "tj-ru-panj-orthodox-community",
        "Orthodox Community in Panj",
        "Православная община посёлка Пяндж",
        "Panj",
        rank="Community",
        sources=[PANJ_DUSTI],
    ),
    body(
        "tj-ru-shaartuz-orthodox-community",
        "Orthodox Community in Shaartuz",
        "Православная община посёлка Шаартуз",
        "Shaartuz",
        rank="Community",
        sources=[SHAARTUZ],
    ),
]

EXPECTED_TOTAL = 12
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}
ALLOWED_RANKS = {
    "Cathedral",
    "Church",
    "Military Parish",
    "Church Community",
    "Community",
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
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    return row


def build():
    rows = []
    seen = {PARENT}
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != PARENT or row.get("country") != "TJ":
            raise ValueError("%s hangs outside the Tajikistan branch" % row_id)
        if row.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        if not row.get("name") or not row.get("local") or not row.get("seat"):
            raise ValueError("%s lacks a usable name or seat" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED_TOTAL:
        raise ValueError("Tajikistan must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - {PARENT}:
        raise ValueError("Tajikistan English name map is out of sync")
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "TJ",
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
        print("directory Tajikistan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print(
        "Tajikistan: 12 current bodies under the Dushanbe Diocese "
        "(7 churches and 5 worship communities)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
