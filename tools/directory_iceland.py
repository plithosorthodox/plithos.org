#!/usr/bin/env python3
"""Directory rows for Iceland.

The four published communities belong to parent bodies which also cover other
countries. This module therefore emits validated Iceland fragments and does
not write final branch payloads. Merge each fragment with the matching parent
payload before publication.

    python tools/directory_iceland.py --check
    python tools/directory_iceland.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

EP_SWEDEN = "https://ec-patr.org/entities/iera-mitropoli-soyidias/"
MOSCOW_JOINT_SERVICE = (
    "https://eparchia.patriarchia.ru/article/117598?path=/news/europe"
)
MOSCOW_CURRENT = "https://eparchia.patriarchia.ru/article/123540"
MOSCOW_PARISH_NAME = (
    "https://eparchia.patriarchia.ru/article/121054?path=/news/europe"
)
RUSSIAN_PARISH = "http://www.orthodox.is/"
SERBIAN_DIRECTORY = (
    "https://www.spc.rs/sr/82.eparhije-srpske-pravoslavne-crkve.html"
)
SERBIAN_PARISH = "https://www.spc.is/icelandic/index.php"
ICELAND_RELIGION_STATISTICS = (
    "https://px.hagstofa.is/pxen/pxweb/en/Samfelag/"
    "Samfelag__menning__5_trufelog__trufelog/MAN10001.px/"
)
ROMANIAN_PARISHES = "https://www.eorii.com/?p=parohii"

ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
ANTIOCH_DIRECTORY = "https://www.antiochian-orthodox.com/parish-directory"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
GEORGIAN_PATRIARCHATE = "https://patriarchate.ge/"
UOC_FOREIGN_PARISHES = (
    "https://vzcz.church.ua/2026/02/09/"
    "pro-sluzhinnya-zaxidnojevropejskogo-vikariatstva-"
    "ukrajinskoji-pravoslavnoji-cerkvi/"
)
OCU_DIASPORA = (
    "https://www.pomisna.info/uk/document-post/"
    "dopovid-predstoyatelya-na-arhiyerejskomu-sobori-15-grudnya-2020-roku/"
)
OCA_DIRECTORY = "https://www.oca.org/parishes/search"
MACEDONIAN_CHURCH = "http://www.mpc.org.mk/"


def row(row_id, parent, name, local, address, sources,
        rank="Parish", site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "IS",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


ROWS = {
    "ep-sweden": [
        row(
            "is-ep-reykjavik-apostle-bartholomew", "ep-sweden",
            "Apostle Bartholomew Greek Orthodox Parish",
            "Ἐνορία Ἀποστόλου Βαρθολομαίου εἰς Ρέϊκιαβικ Ἰσλανδίας",
            ["Friðrikskapella", "Reykjavik, Iceland"],
            [EP_SWEDEN], site=EP_SWEDEN,
        ),
    ],
    "russia": [
        row(
            "is-russia-reykjavik-saint-nicholas-stauropegic", "russia",
            "St Nicholas Stauropegic Parish of the Moscow Patriarchate in Reykjavik",
            "Никольский ставропигиальный приход Московского Патриархата в Рейкьявике",
            ["Öldugata 44", "101 Reykjavik, Iceland"],
            [MOSCOW_PARISH_NAME, MOSCOW_CURRENT, RUSSIAN_PARISH],
            rank="Stauropegic Parish", site=RUSSIAN_PARISH,
        ),
    ],
    "ro-ireland-iceland": [
        row(
            "is-ro-reykjavik-resurrection", "ro-ireland-iceland",
            "Parish of the Resurrection of the Lord in Reykjavik",
            "Parohia Învierea Domnului", ["Reykjavik, Iceland"],
            [ROMANIAN_PARISHES], site=ROMANIAN_PARISHES,
        ),
    ],
    "sr-scandinavia": [
        row(
            "is-serbian-reykjavik-nativity-theotokos", "sr-scandinavia",
            "Parish of the Nativity of the Most Holy Theotokos in Iceland",
            "Serbneska rétttrúnaðarkirkjan",
            [], [SERBIAN_DIRECTORY, MOSCOW_JOINT_SERVICE,
                 ICELAND_RELIGION_STATISTICS], site=SERBIAN_PARISH,
        ),
    ],
}


# These parents already carry, or will carry, rows from other countries. The
# Iceland payloads are country fragments, never replacements for those files.
SHARED_MULTI_COUNTRY_PARENTS = frozenset(ROWS)


# Exported for tools/directory_names/en.py. The map is derived so the English
# catalogue label cannot drift from the row label.
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "ep-sweden": 1,
    "ro-ireland-iceland": 1,
    "russia": 1,
    "sr-scandinavia": 1,
}


# Official directories and central Church sources checked for additional
# Iceland bodies. These checks found no row to publish. The civil registry is
# also recorded in tools/directory_candidates/iceland.json.
AUDITED_NO_ROWS = {
    "antioch": ANTIOCH_DIRECTORY,
    "bulgaria": BULGARIAN_DIRECTORY,
    "georgia": GEORGIAN_PATRIARCHATE,
    "macedonia": MACEDONIAN_CHURCH,
    "oca": OCA_DIRECTORY,
    "ru-great-britain-and-western-europe-rocor": ROCOR_DIRECTORY,
    "ukraine-ocu": OCU_DIASPORA,
    "ukraine-uoc": UOC_FOREIGN_PARISHES,
}


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
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") != "parish":
                raise ValueError("%s has unsupported kind: %s" %
                                 (row_id, item.get("kind")))
            if item.get("country") != "IS":
                raise ValueError("%s is outside Iceland" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "IS",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Iceland parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 4:
        raise ValueError("Iceland English name coverage changed")
    if SHARED_MULTI_COUNTRY_PARENTS != frozenset(EXPECTED):
        raise ValueError("Iceland shared parent coverage changed")
    if set(AUDITED_NO_ROWS) != {
            "antioch", "bulgaria", "georgia", "macedonia", "oca",
            "ru-great-britain-and-western-europe-rocor", "ukraine-ocu",
            "ukraine-uoc"}:
        raise ValueError("Iceland no-row jurisdiction audit changed")
    return payloads


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = []
    for parent in payloads:
        if parent not in base_ids:
            errors.append("missing directory parent: %s" % parent)
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Iceland row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "IS",
            "merge_required": True,
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
        errors = repository_problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Iceland: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Iceland branches: 4 parishes under 4 shared parents")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    print("additional canonical jurisdictions audited without Iceland rows: %d" %
          len(AUDITED_NO_ROWS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
