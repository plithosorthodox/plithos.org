#!/usr/bin/env python3
"""Current officially named Orthodox bodies in Hong Kong.

The current metropolitan and parish directories name one congregation of the
Ecumenical Patriarchate and one parish of the Chinese Autonomous Orthodox
Church under the present oversight of the Moscow Patriarchate.

    python tools/directory_hong_kong.py --check
    python tools/directory_hong_kong.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-15"

EP_DIRECTORY = "https://omhksea.org/metropolis-of-hong-kong/hong-kong"
EP_SERVICES = "https://omhksea.org/about/services"
MP_PARISH = "https://orthodoxy.hk/"
MP_HISTORY = "https://www.rlc.hk/parish/history_of_parish/"
MP_SYNOD = "https://patriarchia.ru/article/96570"

ENGLISH_NAMES = {
    "hk-ep-saint-luke-cathedral": (
        "Cathedral of the Holy Apostle and Evangelist Luke"
    ),
    "hk-cn-saints-peter-paul": (
        "Parish of the Holy Apostles Peter and Paul in Hong Kong"
    ),
}


ROWS = {
    "ep-hongkong": [
        dict(
            id="hk-ep-saint-luke-cathedral",
            parent="ep-hongkong",
            kind="parish",
            rank="Cathedral Parish",
            name=ENGLISH_NAMES["hk-ep-saint-luke-cathedral"],
            local="Saint Luke Orthodox Cathedral",
            country="HK",
            dedication="The Holy Apostle and Evangelist Luke",
            address=[
                "704 Universal Trade Center",
                "3 Arbuthnot Road, Central",
                "Hong Kong",
            ],
            site=EP_DIRECTORY,
            sources=[EP_DIRECTORY, EP_SERVICES],
        ),
    ],
    "china": [
        dict(
            id="hk-cn-saints-peter-paul",
            parent="china",
            kind="parish",
            rank="Parish",
            name=ENGLISH_NAMES["hk-cn-saints-peter-paul"],
            local="Приход святых апостолов Петра и Павла в Гонконге",
            country="HK",
            dedication="The Holy Apostles Peter and Paul",
            address=[
                "12/F, Lee Fung Commercial Building",
                "32-36 Des Voeux Road West, Sheung Wan",
                "Hong Kong",
            ],
            languages=["Church Slavonic", "Chinese", "English"],
            site=MP_PARISH,
            founded=[
                "The parish was officially restored by the Holy Synod of the Russian Orthodox Church on October 6, 2008."
            ],
            sources=[MP_PARISH, MP_HISTORY, MP_SYNOD],
        ),
    ],
}

EXPECTED_COUNTS = {"ep-hongkong": 1, "china": 1}


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
            if row.get("country") != "HK":
                raise ValueError("%s is outside Hong Kong" % row_id)
            if row.get("kind") != "parish" or not row.get("local"):
                raise ValueError("%s lacks its official parish identity" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED_COUNTS[parent]:
            raise ValueError("%s must publish exactly %d row" %
                             (parent, EXPECTED_COUNTS[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "rows": rows,
            "country": "HK",
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("English name coverage differs from Hong Kong rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        elif args.check:
            errors = problems(payloads)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("Hong Kong directory data is current (2 rows)")
        else:
            print(json.dumps(manifest(payloads), ensure_ascii=False,
                             indent=2))
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
