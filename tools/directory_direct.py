#!/usr/bin/env python3
"""Bodies which answer directly to a Church rather than a local diocese.

The files are grouped by canonical parent, so a single branch may contain
bodies in several countries. Country filters still find each row through the
branch manifest's countries list.

    python tools/directory_direct.py --check
    python tools/directory_direct.py --write
"""

import argparse
import json
import sys
from pathlib import Path

import directory_australia
import directory_belgium
import directory_denmark
import directory_estonia
import directory_finland
import directory_iceland
import directory_ireland
import directory_liechtenstein
import directory_malta_gibraltar
import directory_norway
import directory_slovenia
import directory_sweden
import directory_switzerland


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-14"

MP_EXTERNAL = "https://calendar.rop.ru/?inc=12"
MP_JAPAN = "https://www.orthodoxjapan.jp/seizou.html"
MP_JAPAN_VISIT = "https://mospat.ru/en/news/93807/pdf/"

RO_EXTERNAL = (
    "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
    "reprezentante-si-comunitati-externe/"
)
RO_JAPAN = "https://romanianorthodoxy.jp/about/"
RO_JAPAN_HOME = "https://romanianorthodoxy.jp/"
RO_MINAMI = (
    "https://romanianorthodoxy.jp/laying-of-the-cornerstone-for-the-church-"
    "in-minami-alps-yamanashi-march-14-2026/"
)


ROWS = {
    "russia": [
        dict(id="jp-mp-tokyo-st-nicholas-metochion", parent="russia",
             kind="parish", rank="Metochion",
             name="Church of Saint Nicholas the Wonderworker, Russian Orthodox Church Metochion",
             local="Храм святителя Николая Чудотворца", country="JP",
             address=[
                 "2-12-17 Honkomagome",
                 "Bunkyo-ku, Tokyo 113-0021",
             ],
             sources=[MP_EXTERNAL, MP_JAPAN, MP_JAPAN_VISIT]),
        dict(id="jp-mp-meguro-st-alexander-nevsky", parent="russia",
             kind="parish", rank="Church",
             name="Church of Saint Alexander Nevsky in Meguro",
             local="Храм святого благоверного великого князя Александра Невского",
             country="JP",
             address=[
                 "6-2-2 Shimo-Meguro",
                 "Meguro-ku, Tokyo",
             ],
             sources=[MP_EXTERNAL, MP_JAPAN, MP_JAPAN_VISIT]),
    ],
    "romania": [
        dict(id="jp-ro-tokyo-st-george", parent="romania",
             kind="parish", rank="Parish",
             name="Parish of Saint George the Great Martyr in Tokyo",
             local="Parohia Sfântul Mare Mucenic Gheorghe", country="JP",
             address=[
                 "2-37-13 Fujimidai",
                 "Kunitachi, Tokyo 186-0003",
             ],
             site="https://romanianorthodoxy.jp/",
             founded=[
                 "The parish was established in 2008.",
                 "The Church of St. George the Great Martyr was consecrated on 3 November 2020.",
             ],
             sources=[RO_EXTERNAL, RO_JAPAN, RO_JAPAN_HOME]),
        dict(id="jp-ro-osaka-chapel", parent="romania",
             kind="parish", rank="Chapel",
             name="Romanian Orthodox Chapel in Osaka",
             local="capelă ortodoxă în Osaka", country="JP",
             founded=[
                 "The Orthodox chapel in Osaka was established in 2022.",
             ],
             sources=[RO_EXTERNAL, RO_JAPAN]),
        dict(id="jp-ro-minami-alps-lazarus-dimitrios", parent="romania",
             kind="parish", rank="Church",
             name="Church of the Resurrection of Lazarus and Saint Dimitrios the New in Minami-Alps",
             local="church dedicated to The Resurrection of Lazarus and Saint Dimitrios the New",
             country="JP",
             founded=[
                 "The first Divine Liturgy in the church was celebrated on 1 November 2026.",
             ],
             sources=[RO_JAPAN_HOME, RO_MINAMI]),
    ],
}

# Stauropegial bodies remain under their direct patriarchal parent even when
# a country also has a locally governed Church. Country modules export these
# exceptional rows so this multi-country branch owns the single payload.
ROWS["russia"].extend(directory_denmark.DIRECT_RUSSIA_ROWS)
ROWS["russia"].extend(directory_estonia.DIRECT_RUSSIA_ROWS)
ROWS["russia"].extend(directory_finland.DIRECT_RUSSIA_ROWS)
ROWS["russia"].extend(directory_iceland.build()["russia"]["rows"])
ROWS["russia"].extend(directory_ireland.ROWS["russia"])
ROWS["russia"].extend(directory_malta_gibraltar.build()["russia"]["rows"])
ROWS["russia"].extend(directory_australia.build()["russia"])
ROWS["russia"].extend(directory_norway.build()["russia"]["rows"])
ROWS["russia"].extend(directory_sweden.DIRECT_RUSSIA_ROWS)
ROWS["russia"].extend(directory_switzerland.build()["russia"]["rows"])
ROWS["romania"].extend(directory_liechtenstein.DIRECT_ROMANIA_ROWS)
ROWS["romania"].extend(directory_belgium.build()["romania"]["rows"])
ROWS["romania"].extend(directory_slovenia.build()["romania"]["rows"])


def clean(row):
    out = {key: value for key, value in row.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    for key in ("address", "languages", "services", "founded"):
        if out.get(key) and (not isinstance(out[key], list) or
                             not all(isinstance(item, str)
                                     for item in out[key])):
            raise ValueError("%s has invalid %s" % (out.get("id"), key))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        countries = set()
        branch_seen = {parent}
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if row.get("parent") not in branch_seen:
                raise ValueError("%s hangs off unknown parent %r"
                                 % (row_id, row.get("parent")))
            if row.get("kind") not in {"diocese", "parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if row.get("kind") == "parish" and not row.get("local"):
                raise ValueError("%s is a parish without its own name" % row_id)
            if not row.get("country"):
                raise ValueError("%s carries no country" % row_id)
            if row.get("site") and not row["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            countries.add(row["country"])
            rows.append(row)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "countries": sorted(countries),
            "rows": rows,
        }
    if len(payloads["russia"]["rows"]) != 45:
        raise ValueError("the direct Russia branch must have 45 rows")
    if len(payloads["romania"]["rows"]) != 6:
        raise ValueError("the direct Romania branch must have 6 rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": payload["countries"],
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
        print("wrote %s (%d rows)"
              % (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    expected = set()
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        expected.add(path.name)
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
        print("directory direct branches: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("2 direct parents, 50 subordinate bodies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
