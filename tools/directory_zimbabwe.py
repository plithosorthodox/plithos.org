#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Zimbabwe.

The Alexandrian and Moscow parent rows already exist in the directory spine.
This module publishes only subordinate bodies whose current identity is
supported by competent first-party Church records. Parallel jurisdictions are
preserved without adjudication.

    python tools/directory_zimbabwe.py --check
    python tools/directory_zimbabwe.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "zimbabwe.json"
)
CHECKED = "2026-11-15"

AX_HISTORY = "https://ierazimpampoue.com/istoriko/"
AX_PHOTOS = "https://ierazimpampoue.com/photografies/"
AX_HOLY_TRINITY = (
    "https://www.patriarchateofalexandria.com/"
    "50-chronia-ieras-mitropoleos-zimpampoye/"
)
AX_SAINT_GEORGE = (
    "https://www.patriarchateofalexandria.com/"
    "episkepsi-tis-athm-sto-ierapostoliko-kentro-ag-georgioy-marontera-"
    "toy-zimpampoye/"
)
AX_SAINT_NECTARIOS = (
    "https://www.patriarchateofalexandria.com/"
    "episkepsi-tis-athm-sto-ierapostoliko-kentro-toy-ag-nektarioy-charare/"
)

RU_ROSTER = (
    "https://exarchate-africa.ru/en/dioceses_cat/south-african-diocese/"
)
RU_PARISH = "https://www.nativityoftheotokos.com/"
RU_PARISH_RU = "https://www.nativityoftheotokos.com/ru"
RU_TWO_PARISHES = "https://www.nativityoftheotokos.com/news/5"
RU_VISIT = (
    "https://exarchate-africa.ru/en/news/"
    "visit-of-metropolitan-constantine-of-cairo-and-north-africa-to-the-"
    "countries-of-west-and-southern-africa/"
)


def body(row_id, parent, name, local, seat, rank, sources, address=None,
         site=None, founded=None):
    return {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "ZW",
        "address": address,
        "site": site,
        "founded": founded,
        "sources": sources,
    }


AX_ROWS = [
    body(
        "zw-ax-harare-holy-trinity", "ax-zimbabwe",
        "Holy Trinity Cathedral in Harare",
        "Καθεδρικό Ναό της Αγίας Τριάδος",
        "Harare", "Cathedral",
        [AX_HISTORY, AX_PHOTOS, AX_HOLY_TRINITY],
    ),
    body(
        "zw-ax-marondera-saint-george", "ax-zimbabwe",
        "Saint George Missionary Center in Marondera",
        "ιεραποστολικό κέντρο Αγίου Γεωργίου Μαροντέρα",
        "Marondera", "Missionary Center",
        [AX_HISTORY, AX_PHOTOS, AX_SAINT_GEORGE],
    ),
    body(
        "zw-ax-harare-saint-nectarios", "ax-zimbabwe",
        "Saint Nectarios Missionary Center in Harare",
        "ιεραποστολικό κέντρο του Αγίου Νεκταρίου",
        "Harare", "Missionary Center",
        [AX_HISTORY, AX_PHOTOS, AX_SAINT_NECTARIOS],
    ),
]

RUSSIAN_ROWS = [
    body(
        "zw-ru-harare-nativity-theotokos", "ru-south-africa",
        "Parish of the Nativity of the Most Holy Theotokos in Harare",
        "Приход Рождества Пресвятой Богородицы",
        "Harare", "Parish", [RU_ROSTER, RU_PARISH, RU_PARISH_RU],
        address=[
            "Kingsmead Private Chapel, Cnr Rayl Road and Kingsmead Road, "
            "Borrowdale, Harare.",
        ],
        site=RU_PARISH,
        founded="est. 2025",
    ),
    body(
        "zw-ru-harare-sergius-radonezh", "ru-south-africa",
        "Saint Sergius of Radonezh Parish in Harare",
        "Приход святого Сергия",
        "Harare", "Parish", [RU_TWO_PARISHES, RU_VISIT, RU_PARISH_RU],
    ),
]

ROWS = {
    "ax-zimbabwe": AX_ROWS,
    "ru-south-africa": RUSSIAN_ROWS,
}
EXPECTED = {
    "ax-zimbabwe": 3,
    "ru-south-africa": 2,
}
EXPECTED_TOTAL = 5
ALLOWED_KINDS = {"parish"}
ALLOWED_RANKS = {"Cathedral", "Missionary Center", "Parish"}
FORBIDDEN_FIELDS = {
    "bishop", "clergy", "contact", "email", "phone", "telephone",
}
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for rows in ROWS.values()
    for item in rows
}
ENGLISH_SEATS = {
    item["seat"]: item["seat"]
    for rows in ROWS.values()
    for item in rows
    if item.get("seat")
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
    return item


def build():
    payloads = {}
    seen = set(ROWS)
    names = {}
    locations = {}
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
                raise ValueError("%s hangs off the wrong branch" % row_id)
            if item.get("country") != "ZW":
                raise ValueError("%s is outside Zimbabwe" % row_id)
            if item.get("kind") not in ALLOWED_KINDS:
                raise ValueError("%s has an unsupported kind" % row_id)
            if item.get("rank") not in ALLOWED_RANKS:
                raise ValueError("%s has an unsupported rank" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a usable local or English name" %
                                 row_id)
            if FORBIDDEN_FIELDS.intersection(item):
                raise ValueError("%s carries a forbidden contact field" %
                                 row_id)
            if item.get("address") and (
                    not isinstance(item["address"], list) or
                    not all(isinstance(line, str) and line.strip()
                            for line in item["address"])):
                raise ValueError("%s has an invalid address" % row_id)
            if item.get("site") and not item["site"].startswith("https://"):
                raise ValueError("%s carries a non-HTTPS site" % row_id)
            if item.get("site") and row_id != (
                    "zw-ru-harare-nativity-theotokos"):
                raise ValueError("%s carries a site that is not its own" %
                                 row_id)
            name_key = item["name"].casefold()
            if name_key in names:
                raise ValueError("duplicate reader-facing name: %s and %s" % (
                    names[name_key], row_id,
                ))
            location_key = (
                parent, item["local"].casefold(), item["seat"].casefold(),
            )
            if location_key in locations:
                raise ValueError("duplicate body identity: %s and %s" % (
                    locations[location_key], row_id,
                ))
            rendered = json.dumps(item, ensure_ascii=False)
            if any(mark in rendered for mark in (
                    "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
                    "\u201c", "\u201d")):
                raise ValueError("%s has forbidden punctuation or encoding" %
                                 row_id)
            seen.add(row_id)
            names[name_key] = row_id
            locations[location_key] = row_id
            rows.append(item)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "ZW",
            "rows": rows,
        }
    row_ids = {
        item["id"] for payload in payloads.values() for item in payload["rows"]
    }
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Zimbabwe English name map is out of sync")
    if sum(len(payload["rows"]) for payload in payloads.values()) != (
            EXPECTED_TOTAL):
        raise ValueError("Zimbabwe branch total must remain %d" %
                         EXPECTED_TOTAL)
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "ZW":
        raise ValueError("Zimbabwe candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Zimbabwe candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if (summary.get("new_subordinate_bodies") != EXPECTED_TOTAL or
            summary.get("ax-zimbabwe") != 3 or
            summary.get("ru-south-africa") != 2 or
            summary.get("canonical_jurisdictions") != 2 or
            summary.get("current_construction_sites") != 0):
        raise ValueError("Zimbabwe candidate ledger totals are out of sync")
    required_lists = (
        "candidates", "reconciliation", "exclusions",
        "official_jurisdiction_audit",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Zimbabwe candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "ZW":
            raise ValueError("%s is outside Zimbabwe" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Zimbabwe candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Zimbabwe ledger item must cite one to three sources"
                )
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError(
                    "Zimbabwe ledger item carries a non-HTTPS source"
                )
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("Zimbabwe candidate ledger has forbidden punctuation")
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
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Zimbabwe: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Zimbabwe: 5 current officially named subordinate bodies across "
            "2 existing parent branches"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
