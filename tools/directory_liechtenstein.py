#!/usr/bin/env python3
"""Directory rows for Liechtenstein.

The official-source union preserves each current canonical worship community
or mission documented in the principality. The Romanian Patriarchate ministry
is exported separately because the source documents the patriarchate but does
not identify an immediate eparchy.

    python tools/directory_liechtenstein.py --check
    python tools/directory_liechtenstein.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

LOCAL_CURRENT = "https://orthodoxie.li/"
LOCAL_GREEK = (
    "https://orthodoxie.li/liechtenstein-orthodox-Orthodoxe-Kirche/"
    "griechische-gemeinde"
)
LOCAL_SERBIAN = (
    "https://orthodoxie.li/liechtenstein-orthodox-Orthodoxe-Kirche/"
    "serbische-gemeinde"
)
LOCAL_REFUGEES = (
    "https://orthodoxie.li/liechtenstein-orthodox-Orthodoxe-Kirche/"
    "fluechtlingsseelsorge"
)
LOCAL_REGION = (
    "https://orthodoxie.li/liechtenstein-orthodox-Orthodoxe-Kirche/"
    "orthodoxe-kirchen-der-region"
)
LOCAL_2024 = "https://orthodoxie.li/download_file/view/198/1"
EP_SWITZERLAND = "https://ec-patr.org/entities/iera-mitropoli-elvetias/"
SERBIAN_MELS = (
    "https://spc.rs/sr/news/13965."
    "slava-parohije-svetog-vladike-nikolaja-u-melsu.html"
)
ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
ROCOR_MISSION = (
    "https://orthodox-europe.org/content/first-liturgy-in-lichtenstein/"
)


def row(row_id, parent, name, local, rank, sources, address=None,
        site=None, services=None, founded=None, languages=None):
    return {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "LI",
        "address": address,
        "site": site,
        "services": services,
        "founded": founded,
        "languages": languages,
        "sources": sources,
    }


ROWS = {
    "ep-switzerland": [
        row(
            "li-ep-greek-community", "ep-switzerland",
            "Greek Orthodox Community in Liechtenstein",
            "Griechische Gemeinde der Christlich-Orthodoxen Kirche in Liechtenstein",
            "Worship Community",
            [LOCAL_GREEK, EP_SWITZERLAND, LOCAL_2024],
            site=LOCAL_GREEK,
            services=[
                "Gottesdienste mehrmals jährlich in Schaan, in der Laurentiuskirche und St. Peter, sowie in Vaduz in der Johanneskirche.",
            ],
            languages=["Byzantinisch-Griechisch"],
        ),
    ],
    "sr-switzerland": [
        row(
            "li-sr-serbian-community", "sr-switzerland",
            "Serbian Orthodox Community in Liechtenstein",
            "Serbische Gemeinde der Christlich-Orthodoxen Kirche in Liechtenstein",
            "Worship Community",
            [LOCAL_SERBIAN, SERBIAN_MELS, LOCAL_2024],
            site=LOCAL_SERBIAN,
            services=[
                "Gottesdienste mehrmals jährlich in Schaan, in der Laurentiuskirche und St. Peter, sowie in Vaduz in der Johanneskirche.",
            ],
            languages=["Kirchenslawisch", "Serbisch"],
        ),
    ],
    "romania": [
        row(
            "li-ro-refugee-pastoral-ministry", "romania",
            "Romanian Patriarchate Pastoral Ministry for Orthodox Refugees in Liechtenstein",
            "Ukrainisch-, moldawisch- und russischsprachige Gemeinde des Rumänischen Patriarchats",
            "Pastoral Ministry",
            [LOCAL_REFUGEES, LOCAL_REGION, LOCAL_2024],
            address=["Johanneskirche", "Schaanerstrasse 22", "9490 Vaduz"],
            site=LOCAL_REFUGEES,
            services=[
                "Gewöhnlich am ersten Sonntag im Monat um 09:30 in der Johanneskirche Vaduz.",
                "Weiterer Gottesdienstort im Galluszentrum Grabs.",
            ],
            founded=[
                "Der Kirchenverband organisiert diese Seelsorge seit Mai 2022.",
            ],
            languages=["Kirchenslawisch"],
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "li-rocor-liechtenstein-mission",
            "ru-great-britain-and-western-europe-rocor",
            "Liechtenstein Mission", "Лихтенштейнская Миссия", "Mission",
            [ROCOR_MISSION, ROCOR_DIRECTORY],
            address=["Johanneskirche", "Schaanerstrasse 22", "9490 Vaduz"],
            site=ROCOR_MISSION,
            founded=[
                "Основана указом Правящего архиерея в мае 2025 г.",
                "Первая Божественная литургия была совершена 6 / 19 августа 2026 г.",
            ],
        ),
    ],
}


DIRECT_ROMANIA_ROWS = ROWS["romania"]
LOCAL_PAYLOAD_PARENTS = (
    "ep-switzerland",
    "sr-switzerland",
    "ru-great-britain-and-western-europe-rocor",
)
EXPECTED = {
    "ep-switzerland": 1,
    "romania": 1,
    "ru-great-britain-and-western-europe-rocor": 1,
    "sr-switzerland": 1,
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
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
    for field in ("address", "services", "founded", "languages"):
        if (out.get(field) and
                (not isinstance(out[field], list) or
                 not all(isinstance(line, str) for line in out[field]))):
            raise ValueError("%s has invalid %s" % (out.get("id"), field))
    serialized = json.dumps(out, ensure_ascii=False)
    if "\u2013" in serialized or "\u2014" in serialized:
        raise ValueError("%s contains a long dash" % out.get("id"))
    return out


def _build_all():
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
            if item.get("country") != "LI":
                raise ValueError("%s is outside Liechtenstein" % row_id)
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
            "country": "LI",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Liechtenstein parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 4:
        raise ValueError("Liechtenstein English name coverage changed")
    return payloads


def build():
    """Build branch payloads, excluding the direct Romanian root row."""
    payloads = _build_all()
    return {parent: payloads[parent] for parent in LOCAL_PAYLOAD_PARENTS}


def contributions(payloads=None):
    """Return all rows grouped for the shared directory builders."""
    payloads = payloads or _build_all()
    return {parent: list(payload["rows"])
            for parent, payload in payloads.items()}


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
            "merge_required": True,
        }
        for parent, payload in sorted(payloads.items())
    }


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
        errors.append("Liechtenstein row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        all_payloads = _build_all()
        errors = repository_problems(all_payloads)
    except (OSError, ValueError) as exc:
        print("directory Liechtenstein: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(all_payloads, ensure_ascii=False, indent=2))
        return 0
    print("Liechtenstein: 4 bodies under 4 canonical parents")
    for parent, count in sorted(EXPECTED.items()):
        suffix = " direct row" if parent == "romania" else " branch row"
        print("%s: %d%s" % (parent, count, suffix))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
