#!/usr/bin/env python3
"""The current official parish directories for Singapore.

The Ecumenical Patriarchate's Metropolitanate of Singapore and the Moscow
Patriarchate's Diocese of Singapore each publish one current congregation in
the country. Search and map results are not source rows here.

    python tools/directory_singapore.py --check
    python tools/directory_singapore.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-15"

EP_DIRECTORY = "https://omsgsa.org/parishes-singapore"
EP_CATHEDRAL = "https://orthodoxchurch.sg/"
MP_DIRECTORY = "https://exarchate.asia/karta-prihodov/"
MP_PARISH = "https://singapore.cerkov.ru/"
MP_CURRENT = "https://patriarchia.ru/document/120274"

ENGLISH_NAMES = {
    "sg-ep-holy-resurrection-cathedral": (
        "Holy Resurrection Orthodox Christian Cathedral of Singapore"
    ),
    "sg-ru-dormition-theotokos": (
        "Parish of the Dormition of the Theotokos in Singapore"
    ),
}


ROWS = {
    "ep-singapore": [
        dict(
            id="sg-ep-holy-resurrection-cathedral",
            parent="ep-singapore",
            kind="parish",
            rank="Cathedral Parish",
            name=ENGLISH_NAMES["sg-ep-holy-resurrection-cathedral"],
            local="Holy Resurrection Orthodox Christian Cathedral of Singapore",
            country="SG",
            dedication="The Holy Resurrection of Christ",
            address=[
                "Catholic Archdiocesan Education Centre",
                "2 Highland Road",
                "Singapore 549102",
            ],
            site=EP_CATHEDRAL,
            sources=[EP_DIRECTORY, EP_CATHEDRAL],
        ),
    ],
    "ru-singapore": [
        dict(
            id="sg-ru-dormition-theotokos",
            parent="ru-singapore",
            kind="parish",
            rank="Parish",
            name=ENGLISH_NAMES["sg-ru-dormition-theotokos"],
            local="Приход Успения Пресвятой Богородицы в Сингапуре",
            country="SG",
            dedication="The Dormition of the Most Holy Theotokos",
            address=["110 Highland Road", "Singapore 549190"],
            languages=["Church Slavonic"],
            site=MP_PARISH,
            founded=[
                "Приход в честь Успения Божией Матери был учрежден Священным Синодом Русской Православной Церкви 12 октября 2007 года.",
                "Официальная регистрация прихода в соответствии с законодательством Сингапура была завершена 12 декабря 2008 года.",
            ],
            sources=[MP_DIRECTORY, MP_PARISH, MP_CURRENT],
        ),
    ],
}

EXPECTED_COUNTS = {"ep-singapore": 1, "ru-singapore": 1}


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if row.get("site") and not row["site"].startswith("http"):
        raise ValueError("%s carries a non-URL site" % row.get("id"))
    for key in ("address", "languages", "founded"):
        if row.get(key) and (not isinstance(row[key], list) or
                             not all(isinstance(value, str)
                                     for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    for value in row.values():
        texts = value if isinstance(value, list) else [value]
        for text in texts:
            if isinstance(text, str) and ("\u2013" in text or "\u2014" in text):
                raise ValueError("%s carries a forbidden long dash" %
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
            if row.get("parent") != parent:
                raise ValueError("%s is grouped under the wrong parent" % row_id)
            if row.get("country") != "SG":
                raise ValueError("%s is not a Singapore row" % row_id)
            if row.get("kind") != "parish" or not row.get("local"):
                raise ValueError("%s lacks its official parish identity" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED_COUNTS[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED_COUNTS[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "rows": rows,
            "country": "SG",
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("English name coverage differs from Singapore rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "SG",
        }
        for parent, payload in sorted(payloads.items())
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Singapore: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Singapore branches: 2 parents, 2 parishes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
