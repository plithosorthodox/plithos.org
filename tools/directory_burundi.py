#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Burundi.

The Alexandrian Patriarchate and the Moscow Patriarchate's African Exarchate
both publish current structures in Burundi. Only bodies named by their own
competent Church are emitted here. Unnamed communities and one church last
described as unfinished remain in the companion candidate ledger.

    python tools/directory_burundi.py --check
    python tools/directory_burundi.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_DIOCESE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-diocese-of-bujumbura-and-burundi/?lang=en"
)
AX_VISIT = (
    "https://www.patriarchateofalexandria.com/"
    "the-patriarch-supports-the-young-refugees-of-burundi/?lang=en&print=print"
)
AX_GIHUNGE = (
    "https://www.patriarchateofalexandria.com/"
    "burundi-accepts-orthodoxy/?lang=en"
)
RU_SOUTH_AFRICA = (
    "https://exarchate-africa.ru/en/dioceses_cat/south-african-diocese/"
)
RU_PASCHA = (
    "https://exarchate-africa.ru/novosti/"
    "pravoslavnye-obshhiny-v-burundi-vstretili-prazdnik-voskreseniya-hristova/"
)


ROWS = {
    "ax-bujumbura": [
        dict(
            id="bi-ax-bujumbura-dormition-cathedral",
            parent="ax-bujumbura",
            kind="parish",
            rank="Cathedral",
            name="Cathedral of the Dormition of the Theotokos in Bujumbura",
            local="Cathédrale de la Dormition de la Mère de Dieu à Bujumbura",
            country="BI",
            address=[
                "Eglise Orthodoxe de Burundi",
                "Rohero II, Avenue du Congo 3",
                "B.P. 3569, Bujumbura, Burundi",
            ],
            sources=[AX_DIOCESE, AX_VISIT],
        ),
        dict(
            id="bi-ax-buramata-saint-alexios",
            parent="ax-bujumbura",
            kind="parish",
            rank="Church",
            name="Church of Saint Alexios the Man of God in Buramata",
            local="Église Saint-Alexis, l'Homme de Dieu, à Buramata",
            country="BI",
            sources=[AX_DIOCESE, AX_VISIT],
        ),
    ],
    "ru-south-africa": [
        dict(
            id="bi-ru-rumonge-saint-sergius",
            parent="ru-south-africa",
            kind="parish",
            rank="Parish",
            name="Parish of Saint Sergius of Radonezh in Rumonge",
            local="Paroisse Saint-Serge-de-Radonège à Rumonge",
            country="BI",
            sources=[RU_SOUTH_AFRICA, RU_PASCHA],
        ),
    ],
}

EXPECTED = {"ax-bujumbura": 2, "ru-south-africa": 1}
ENGLISH_NAMES = {
    row["id"]: row["name"]
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
    for key in ("address", "languages", "founded"):
        if row.get(key) and (
                not isinstance(row[key], list) or
                not all(isinstance(value, str) for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
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
            if row.get("country") != "BI":
                raise ValueError("%s is outside Burundi" % row_id)
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
            "country": "BI",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Burundi English name map is out of sync")
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
        print("directory Burundi: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Burundi: 3 current officially named bodies across 2 jurisdictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
