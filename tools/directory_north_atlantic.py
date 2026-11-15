#!/usr/bin/env python3
"""Directory rows for the Faroe Islands and Greenland.

These North Atlantic bodies belong to the Romanian Orthodox Diocese of
Northern Europe. The shared north-west Europe owner merges them with the
same diocesan branch used by Denmark, Norway, and Sweden.

    python tools/directory_north_atlantic.py --check
    python tools/directory_north_atlantic.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-14"
ROMANIAN_MAP = (
    "https://episcopiascandinavia.se/wp-content/uploads/2026/10/"
    "3.-MOBIL_harta_parohii_Scandinavia_v3.html"
)
FAROE_DIRECTORY = (
    "https://episcopiascandinavia.se/"
    "parohia-ortodoxa-romana-din-insulele-feroe/"
)
FAROE_CURRENT = (
    "https://episcopiascandinavia.se/page/206/?start=11"
)
GREENLAND_DIRECTORY = (
    "https://episcopiascandinavia.se/category/"
    "parohii-si-manastiri-ro/"
)


ROWS = {
    "ro-northern-europe": [
        {
            "id": "fo-ro-torshavn-mistress-islands",
            "parent": "ro-northern-europe",
            "kind": "parish",
            "rank": "Parish",
            "name": (
                "Parish of the Mistress of the Faroe Islands Icon, "
                "Saints Symeon the Stylite and Dionysius Exiguus, and "
                "Saint Brendan the Navigator in Torshavn"
            ),
            "local": (
                "Parohia Cinstirea Icoanei Maicii Domnului "
                "\"Stăpâna Insulelor Feroe\" de la Tórshavn, Sfinții "
                "Cuvioși Simeon Stâlpnicul și Dionisie Exiguul din "
                "Dobrogea şi Sfântul Cuvios Brendan Călătorul, "
                "Luminătorul Insulelor Feroe"
            ),
            "country": "FO",
            "address": [
                "Strada Velbastaðvegur, cod postal 100, Tórshavn",
            ],
            "sources": [FAROE_DIRECTORY, ROMANIAN_MAP, FAROE_CURRENT],
        },
        {
            "id": "gl-ro-peter-paul-mission",
            "parent": "ro-northern-europe",
            "kind": "parish",
            "rank": "Mission",
            "name": "Mission of the Holy Apostles Peter and Paul in Greenland",
            "local": "Misiunea Sfinții Apostoli Petru și Pavel",
            "country": "GL",
            "sources": [GREENLAND_DIRECTORY, ROMANIAN_MAP],
        },
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {"ro-northern-europe": 2}


def clean(source):
    out = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("address") and (not isinstance(out["address"], list) or
                               not all(isinstance(line, str)
                                       for line in out["address"])):
        raise ValueError("%s has an invalid address" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    countries = set()
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has an unsupported kind" % row_id)
            if item.get("country") not in {"FO", "GL"}:
                raise ValueError("%s is outside the North Atlantic scope" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            seen.add(row_id)
            countries.add(item["country"])
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "countries": sorted(countries),
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("North Atlantic parent counts changed: %r" % actual)
    if set(ENGLISH_NAMES) != {
            item["id"] for source_rows in ROWS.values()
            for item in source_rows}:
        raise ValueError("North Atlantic English name coverage changed")
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


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory North Atlantic: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("North Atlantic branches: 2 rows")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
