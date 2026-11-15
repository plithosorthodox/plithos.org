#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Benin.

The Alexandrian Diocese of Benin, Togo and Burkina Faso publishes five Benin
parishes. The Moscow Patriarchate's North African Diocese separately publishes
one of its two Benin parishes by name. The unnamed second parish remains in the
companion candidate ledger.

    python tools/directory_benin.py --check
    python tools/directory_benin.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_DIOCESE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-episkopi-mpenin-togko-kai-mpoyrkina-faso/?lang=en"
)
AX_ABOUT = "https://www.orthodoxie-benin-togo-burkina.com/a-propos"
AX_HOME = "https://www.orthodoxie-benin-togo-burkina.com/"
RU_NORTH_AFRICA = (
    "https://exarchate-africa.ru/en/dioceses_cat/diocese-of-north-africa/"
)
RU_PASCHA = (
    "https://exarchate-africa.ru/fr/actualite/"
    "les-celebrations-de-paques-ont-eu-lieu-a-la-paroisse-de-la-nativite-"
    "du-christ-au-benin/"
)


def row(row_id, parent, rank, name, local, sources):
    return {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "BJ",
        "sources": sources,
    }


ROWS = {
    "ax-benin": [
        row(
            "bj-ax-porto-novo-saint-catherine-cathedral",
            "ax-benin",
            "Cathedral",
            "Cathedral of Saint Catherine of Alexandria in Porto-Novo",
            "Cathédrale Sainte Catherine d'Alexandrie à Porto-Novo",
            [AX_DIOCESE, AX_ABOUT, AX_HOME],
        ),
        row(
            "bj-ax-abomey-calavi-holy-trinity",
            "ax-benin",
            "Parish",
            "Parish of the Holy Trinity in Abomey-Calavi",
            "Paroisse Sainte Trinité à Abomey-Calavi",
            [AX_DIOCESE, AX_ABOUT],
        ),
        row(
            "bj-ax-afotonou-saint-john-chrysostom",
            "ax-benin",
            "Parish",
            "Parish of Saint John Chrysostom in Afotonou",
            "Paroisse Saint Jean Chrysostome à Afotonou",
            [AX_DIOCESE, AX_ABOUT],
        ),
        row(
            "bj-ax-abomey-saint-moses",
            "ax-benin",
            "Parish",
            "Parish of Saint Moses in Abomey",
            "Paroisse Saint Moïse à Abomey",
            [AX_DIOCESE, AX_ABOUT],
        ),
        row(
            "bj-ax-sekou-saint-george",
            "ax-benin",
            "Parish",
            "Parish of Saint George in Sékou",
            "Paroisse Saint Georges à Sékou",
            [AX_DIOCESE, AX_ABOUT],
        ),
    ],
    "ru-north-africa": [
        row(
            "bj-ru-cotonou-nativity-christ",
            "ru-north-africa",
            "Parish",
            "Parish of the Nativity of Christ in Cotonou",
            "Paroisse de la Nativité du Christ à Cotonou",
            [RU_NORTH_AFRICA, RU_PASCHA],
        ),
    ],
}

EXPECTED = {"ax-benin": 5, "ru-north-africa": 1}
ENGLISH_NAMES = {
    item["id"]: item["name"]
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
            if item.get("country") != "BJ":
                raise ValueError("%s is outside Benin" % row_id)
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
            "country": "BJ",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Benin English name map is out of sync")
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
        print("directory Benin: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Benin: 6 current officially named bodies across 2 jurisdictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
