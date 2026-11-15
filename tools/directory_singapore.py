#!/usr/bin/env python3
"""The current official parish directories for Singapore and Malaysia.

The Ecumenical Patriarchate's Metropolitanate of Singapore and the Moscow
Patriarchate's Diocese of Singapore each publish one current congregation in
Singapore. The Moscow exarchate also publishes four current Malaysian
parishes. Search and map results are not source rows here.

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
MP_DIOCESES = "https://exarchate.asia/en/patriarshij-ekzarhat/eparhii/"

ENGLISH_NAMES = {
    "sg-ep-holy-resurrection-cathedral": (
        "Holy Resurrection Orthodox Christian Cathedral of Singapore"
    ),
    "sg-ru-dormition-theotokos": (
        "Parish of the Dormition of the Theotokos in Singapore"
    ),
    "my-ru-kuala-lumpur-archangel-michael": (
        "Parish of the Archangel Michael in Kuala Lumpur"
    ),
    "my-ru-penang-saint-george": (
        "Parish of the Great Martyr George in Penang"
    ),
    "my-ru-johor-bahru-annunciation": (
        "Parish of the Annunciation of the Most Holy Theotokos in Johor Bahru"
    ),
    "my-ru-lukut-saint-andrew": (
        "Parish of the Apostle Andrew the First-Called in Lukut"
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
        dict(
            id="my-ru-kuala-lumpur-archangel-michael",
            parent="ru-singapore",
            kind="parish",
            rank="Parish",
            name=ENGLISH_NAMES["my-ru-kuala-lumpur-archangel-michael"],
            local="Приход Архистратига Божия Михаила в Куала-Лумпуре",
            country="MY",
            dedication="The Archangel Michael",
            address=[
                "5 Lorong Damai 6, off Jalan Ampang",
                "Kuala Lumpur 55000",
                "Malaysia",
            ],
            sources=[MP_DIRECTORY, MP_DIOCESES],
        ),
        dict(
            id="my-ru-penang-saint-george",
            parent="ru-singapore",
            kind="parish",
            rank="Parish",
            name=ENGLISH_NAMES["my-ru-penang-saint-george"],
            local="Приход в честь вмч. Георгия Победоносца на о. Пенанг",
            country="MY",
            dedication="Saint George the Great Martyr",
            sources=[MP_DIRECTORY, MP_DIOCESES],
        ),
        dict(
            id="my-ru-johor-bahru-annunciation",
            parent="ru-singapore",
            kind="parish",
            rank="Parish",
            name=ENGLISH_NAMES["my-ru-johor-bahru-annunciation"],
            local=(
                "Приход в честь Благовещения Пресвятой Богородицы "
                "в Джохор Бару"
            ),
            country="MY",
            dedication="The Annunciation of the Most Holy Theotokos",
            sources=[MP_DIRECTORY, MP_DIOCESES],
        ),
        dict(
            id="my-ru-lukut-saint-andrew",
            parent="ru-singapore",
            kind="parish",
            rank="Parish",
            name=ENGLISH_NAMES["my-ru-lukut-saint-andrew"],
            local=(
                "Приход в честь Св. апостола Андрея Первозванного в Лукуте"
            ),
            country="MY",
            dedication="Saint Andrew the First-Called",
            sources=[MP_DIRECTORY, MP_DIOCESES],
        ),
    ],
}

EXPECTED_COUNTS = {"ep-singapore": 1, "ru-singapore": 5}


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
            if row.get("country") not in {"SG", "MY"}:
                raise ValueError("%s is outside Singapore and Malaysia" % row_id)
            if row.get("kind") != "parish" or not row.get("local"):
                raise ValueError("%s lacks its official parish identity" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED_COUNTS[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED_COUNTS[parent]))
        countries = sorted({row["country"] for row in rows})
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "rows": rows,
        }
        if len(countries) == 1:
            payloads[parent]["country"] = countries[0]
        else:
            payloads[parent]["countries"] = countries
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("English name coverage differs from Singapore rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    answer = {}
    for parent, payload in sorted(payloads.items()):
        spec = {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
        }
        if "countries" in payload:
            spec["countries"] = payload["countries"]
        else:
            spec["country"] = payload["country"]
        answer[parent] = spec
    return answer


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
    print("Singapore and Malaysia branches: 2 parents, 6 parishes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
