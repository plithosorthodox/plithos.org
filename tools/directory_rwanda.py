#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Rwanda.

The Patriarchate of Alexandria and the Moscow Patriarchate's African
Exarchate both publish current structures in Rwanda. Only worship bodies
named by competent first-party Church sources are emitted. Aggregate counts,
unnamed communities, and occasional services remain in the companion ledger.

    python tools/directory_rwanda.py --check
    python tools/directory_rwanda.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "rwanda.json"

AX_DIOCESE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-episkopi-kigkali-kai-royantas/?lang=en"
)
AX_DECREE = (
    "https://www.patriarchateofalexandria.com/"
    "entetalmenos-patriarchikos-epitroposeis-tin-artisystaton-ieran-"
    "episkopin-royantas/?print=print"
)
AX_RWAMAGANA = (
    "https://www.patriarchateofalexandria.com/"
    "oloklirosi-tis-poimantikis-periodeias-tis-a-th-m-stin-royanta/"
)
RU_DIOCESE = (
    "https://exarchate-africa.ru/dioceses_cat/"
    "yuzhno-afrikanskaya-eparhiya/"
)
RU_CURRENT_CLERGY = (
    "https://exarchate-africa.ru/novosti/"
    "ierej-georgij-maksimov-posetil-ruandu/"
)
RU_NYAMATA = (
    "https://exarchate-africa.ru/novosti/"
    "v-ruande-k-czerkvi-hristovoj-prisoedinilis-eshhe-vosem-chelovek/"
)
RU_DORMITION = (
    "https://exarchate-africa.ru/novosti/"
    "v-svetlyj-ponedelnik-k-czerkvi-hristovoj-v-ruande-prisoedinilis-"
    "pyat-mestnyh-zhitelej/"
)
RU_EASTERN_PARISHES = (
    "https://exarchate-africa.ru/novosti/"
    "prodolzhaetsya-poezdka-missionerskoj-gruppy-pod-rukovodstvom-"
    "iereya-georgiya-maksimova/"
)


ROWS = {
    "ax-kigali": [
        dict(
            id="rw-ax-rwamagana-peter-paul",
            parent="ax-kigali",
            kind="parish",
            rank="Church",
            name=(
                "Church of the Chief Apostles Peter and Paul in Rwamagana"
            ),
            local=(
                "Ιερός Ναός των Πρωτοκορυφαίων Αποστόλων Πέτρου και "
                "Παύλου"
            ),
            seat="Rwamagana",
            country="RW",
            sources=[AX_DIOCESE, AX_DECREE, AX_RWAMAGANA],
        ),
    ],
    "ru-south-africa": [
        dict(
            id="rw-ru-nyamata-john-chrysostom",
            parent="ru-south-africa",
            kind="parish",
            rank="Parish",
            name="Parish of Saint John Chrysostom in Nyamata",
            local="Приход святителя Иоанна Златоуста в Ньямате",
            seat="Nyamata",
            country="RW",
            sources=[RU_NYAMATA, RU_CURRENT_CLERGY],
        ),
        dict(
            id="rw-ru-southern-province-dormition",
            parent="ru-south-africa",
            kind="parish",
            rank="Parish",
            name=(
                "Parish of the Dormition of the Theotokos in Southern "
                "Province"
            ),
            local="Приход Успения Пресвятой Богородицы",
            seat="Southern Province",
            country="RW",
            sources=[RU_DORMITION, RU_CURRENT_CLERGY],
        ),
        dict(
            id="rw-ru-churazo-seraphim-sarov",
            parent="ru-south-africa",
            kind="parish",
            rank="Parish",
            name="Parish of Saint Seraphim of Sarov in Churazo",
            local="Приход преподобного Серафима Саровского в Чуразо",
            seat="Churazo",
            country="RW",
            sources=[RU_EASTERN_PARISHES, RU_CURRENT_CLERGY],
        ),
        dict(
            id="rw-ru-gatore-basil-great",
            parent="ru-south-africa",
            kind="parish",
            rank="Parish",
            name="Parish of Saint Basil the Great in Gatore",
            local="Приход святителя Василия Великого в Гаторе",
            seat="Gatore",
            country="RW",
            sources=[RU_EASTERN_PARISHES, RU_CURRENT_CLERGY],
        ),
    ],
}

EXPECTED = {"ax-kigali": 1, "ru-south-africa": 4}
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {
    "Rwamagana": "Rwamagana",
    "Nyamata": "Nyamata",
    "Southern Province": "Southern Province",
    "Churazo": "Churazo",
    "Gatore": "Gatore",
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
            if row.get("country") != "RW":
                raise ValueError("%s is outside Rwanda" % row_id)
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
            "country": "RW",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Rwanda English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "RW":
        raise ValueError("Rwanda candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Rwanda candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("total") != sum(EXPECTED.values()):
        raise ValueError("Rwanda candidate ledger total is out of sync")
    for parent, count in EXPECTED.items():
        if summary.get(parent) != count:
            raise ValueError("Rwanda ledger count is out of sync for %s" %
                             parent)
    for key in ("candidates", "source_reconciliations",
                "official_jurisdiction_audit"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Rwanda candidate ledger lacks %s" % key)
        for item in ledger[key]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Rwanda ledger item has invalid sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Rwanda ledger item has a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Rwanda candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Rwanda: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Rwanda: 5 current named bodies across 2 jurisdictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
