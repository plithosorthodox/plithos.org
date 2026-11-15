#!/usr/bin/env python3
"""Directory rows for Luxembourg.

The official-source union preserves every current canonical jurisdiction
documented for the country, including communities outside the four bodies in
the state convention.

    python tools/directory_luxembourg.py --check
    python tools/directory_luxembourg.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

EP_PARISHES = "https://orthodoxia.be/fr/paroisses/"
EP_NICHOLAS = (
    "https://orthodoxia.be/fr/enoria/"
    "cathedrale-saint-nicolas-a-weiler-la-tour/"
)
EP_VOLODYMYR = (
    "https://orthodoxia.be/fr/enoria/"
    "paroisse-des-saints-anargyres-a-luxembourg/"
)
EP_INTERORTHODOX = (
    "https://orthodoxia.be/fr/2026/03/10/"
    "concelebration-du-2eme-dimanche-du-careme-au-grand-duche-de-luxembourg/"
)
ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
ROCOR_CURRENT = "https://orthodox-europe.org/content/luxembourg-unction/"
SERBIAN_BENELUX = "https://dioceseserbe.org/fr/benelux/"
SERBIAN_DIOCESE = "https://dioceseserbe.org/fr/diocese/"
ROMANIAN_DIRECTORY = "https://mitropolia-ro.de/parohii-luxemburg/"
ROMANIAN_PARISH = "https://bisericaortodoxa.lu/"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
BULGARIAN_VISIT = (
    "https://bg-patriarshia.bg/news/"
    "arhiereysko-poseshtenie-i-duhovna-radost-za-pravoslavnite-ba"
)
BULGARIAN_HASSEL = (
    "https://bnrnews.bg/radiobulgaria/post/525953/"
    "parva-sveta-liturgiya-v-noviya-hram-na-pravoslavnite-balgari-v-lyuksemburg"
)
MACEDONIAN_DIOCESE = "https://mpee.mk/category/za-eparxijata"
MACEDONIAN_REFERENCE = (
    "https://js.ugd.edu.mk/index.php/YFNTS/article/download/7479/5795/13678"
)


def row(row_id, parent, name, local, address, sources,
        rank="Parish", site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "LU",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


ROWS = {
    "ep-belgium": [
        row(
            "lu-ep-weiler-saint-nicholas-cathedral", "ep-belgium",
            "Saint Nicholas Orthodox Cathedral in Weiler-la-Tour",
            "Cathédrale de Saint Nicolas, Grand-Duché de Luxembourg",
            ["1A Rue du Schlammestée", "L-5770 Weiler-la-Tour"],
            [EP_PARISHES, EP_NICHOLAS], rank="Cathedral",
            site="http://www.orthodoxia.lu/",
        ),
        row(
            "lu-ep-dommeldange-saint-volodymyr", "ep-belgium",
            "Saint Volodymyr Equal-to-the-Apostles Orthodox Parish in Dommeldange",
            "Paroisse de Saint Wolodimir égal aux Apôtres",
            [
                "Église Saint-Hubert",
                "2A Rue du Château at Rue des Hauts-Fourneaux",
                "L-1329 Dommeldange",
            ],
            [EP_PARISHES, EP_VOLODYMYR, EP_INTERORTHODOX],
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "lu-rocor-luxembourg-peter-paul",
            "ru-great-britain-and-western-europe-rocor",
            "Saints Peter and Paul Russian Orthodox Church in Luxembourg",
            "Храмъ свв. апп. Петра и Павла",
            ["10 Rue J.-P. Probst", "L-2352 Luxembourg"],
            [ROCOR_DIRECTORY, ROCOR_CURRENT], rank="Church",
            site="https://egliserusse.lu/",
        ),
    ],
    "sr-western-europe": [
        row(
            "lu-sr-luxembourg-constantine-helen", "sr-western-europe",
            "Saints Constantine and Helen Serbian Orthodox Parish in Luxembourg",
            "Парохија Светог Константина и Јелене",
            ["150 Rue de Hollerich", "L-1740 Luxembourg"],
            [SERBIAN_BENELUX, SERBIAN_DIOCESE],
            site="https://www.spclux.lu/",
        ),
    ],
    "ro-germany": [
        row(
            "lu-ro-luxembourg-nativity-matthew", "ro-germany",
            "Nativity of the Lord and Saint Matthew the Apostle Romanian Orthodox Parish in Luxembourg",
            'Parohia Ortodoxă Română "Nașterea Domnului și Sf. Ap. și Ev. Matei"',
            ["1 Rue Vauban", "L-2663 Pfaffenthal, Luxembourg"],
            [ROMANIAN_DIRECTORY, ROMANIAN_PARISH],
            site=ROMANIAN_PARISH,
        ),
    ],
    "bg-western-central-europe": [
        row(
            "lu-bg-luxembourg-saint-john-rila", "bg-western-central-europe",
            "Saint John of Rila Bulgarian Orthodox Church Community in Luxembourg",
            'БПЦО "Св. Преп. Йоан Рилски" - Люксембург',
            ["Église Sainte-Lucie", "Rue de l'Église", "L-5761 Hassel"],
            [BULGARIAN_DIRECTORY, BULGARIAN_VISIT, BULGARIAN_HASSEL],
            rank="Church Community",
        ),
    ],
    "mk-europe": [
        row(
            "lu-mk-luxembourg-apostle-thomas", "mk-europe",
            "Holy Apostle Thomas Macedonian Orthodox Church Community in Luxembourg",
            'МПЦО "Св. Апостол Тома" - Луксембург',
            [], [MACEDONIAN_DIOCESE, MACEDONIAN_REFERENCE],
            rank="Church Community",
        ),
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "bg-western-central-europe": 1,
    "ep-belgium": 2,
    "mk-europe": 1,
    "ro-germany": 1,
    "ru-great-britain-and-western-europe-rocor": 1,
    "sr-western-europe": 1,
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
            if item.get("country") != "LU":
                raise ValueError("%s is outside Luxembourg" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            serialized = json.dumps(item, ensure_ascii=False)
            if "\u2013" in serialized or "\u2014" in serialized:
                raise ValueError("%s contains a long dash" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "LU",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Luxembourg parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 7:
        raise ValueError("Luxembourg English name coverage changed")
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
        errors.append("Luxembourg row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": ["LU"],
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
        print("directory Luxembourg: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Luxembourg branches: 7 bodies under 6 canonical parents")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
