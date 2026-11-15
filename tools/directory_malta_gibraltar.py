#!/usr/bin/env python3
"""Validated directory fragments for Malta and Gibraltar.

The official-source union preserves every current canonical body and worship
site that could be tied to a recognized Eastern Orthodox authority. Search
and map results are discovery aids only.

    python tools/directory_malta_gibraltar.py --check
    python tools/directory_malta_gibraltar.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"
COUNTRIES = {"GI", "MT"}

MALTA_EXARCHATE = (
    "https://ec-patr.org/entities/patriarhiki-eksarxia-melitis/"
)
MALTA_ROMANIAN = (
    "https://episcopia-italiei.it/ro/parohii-filii-si-paraclise/"
    "5510-malta-republica"
)
MALTA_SERBIAN_CURRENT = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/16495."
    "episkop-andrej-posetio-srpsku-zajednicu-na-malti.html"
)
MALTA_SERBIAN_PARISH = (
    "https://spc.rs/sr/news/iz-zivota-crkve/8358."
    "kanonska-poseta-episkopa-andreja-malti.html"
)
MALTA_RUSSIAN_FOUNDING = "https://patriarchia.ru/article/98218"
MALTA_RUSSIAN_CURRENT = (
    "https://romanianchurchmalta.com/"
    "eastern-orthodox-christianity-in-malta/"
)
GIBRALTAR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
GIBRALTAR_FOUNDING = (
    "https://orthodox-europe.org/content/"
    "first-liturgy-gibraltar-with-kursk-icon/"
)


def row(row_id, parent, country, name, local, rank, sources, address=None,
        site=None, services=None, founded=None, languages=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": country,
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    if services:
        value["services"] = services
    if founded:
        value["founded"] = founded
    if languages:
        value["languages"] = languages
    return value


ROWS = {
    "ep-malta": [
        row(
            "mt-ep-saint-george-cathedral",
            "ep-malta",
            "MT",
            "Greek Orthodox Cathedral of Saint George",
            "Ἱερός Ναός Ἁγίου Γεωργίου",
            "Cathedral",
            [MALTA_EXARCHATE],
            address=[
                "83 Merchants Street",
                "Valletta VLT 1177, Malta",
            ],
        ),
        row(
            "mt-ep-saint-nicholas-church",
            "ep-malta",
            "MT",
            "Church of Saint Nicholas",
            "Ἱερός Ναός Ἁγίου Νικολάου",
            "Church",
            [MALTA_EXARCHATE],
            address=[
                "Merchants Street and Saint Nicholas Street",
                "Valletta VLT 1177, Malta",
            ],
        ),
        row(
            "mt-ep-greek-speaking-parish",
            "ep-malta",
            "MT",
            "Greek-Speaking Parish of the Patriarchal Exarchate of Malta",
            "Ἑλληνόφωνος Ἐνορία",
            "Parish",
            [MALTA_EXARCHATE],
            languages=["Greek"],
        ),
        row(
            "mt-ep-ukrainian-speaking-parish",
            "ep-malta",
            "MT",
            "Ukrainian-Speaking Parish of the Patriarchal Exarchate of Malta",
            "Οὐκρανόφωνος Ἐνορία",
            "Parish",
            [MALTA_EXARCHATE],
            languages=["Ukrainian"],
        ),
        row(
            "mt-ep-georgian-speaking-parish",
            "ep-malta",
            "MT",
            "Georgian-Speaking Parish of the Patriarchal Exarchate of Malta",
            "Γεωργιανόφωνος Ἐνορία",
            "Parish",
            [MALTA_EXARCHATE],
            languages=["Georgian"],
        ),
    ],
    "ro-italy": [
        row(
            "mt-ro-nativity-saint-john-baptist",
            "ro-italy",
            "MT",
            "Parish of the Nativity of Saint John the Baptist",
            "Parohia Nașterea Sfântului Ioan Botezătorul",
            "Parish",
            [MALTA_ROMANIAN],
            address=[
                "Church of Saint Rocco",
                "Saint Ursula Street",
                "Valletta, Malta",
            ],
            site=MALTA_ROMANIAN,
        ),
    ],
    "sr-switzerland": [
        row(
            "mt-sr-saints-paul-nicholas",
            "sr-switzerland",
            "MT",
            "Serbian Orthodox Parish of the Holy Apostle Paul and Saint Nicholas",
            "Српска православна црквена општина Светог апостола Павла и Светог Николе на Малти",
            "Parish",
            [MALTA_SERBIAN_CURRENT, MALTA_SERBIAN_PARISH],
        ),
    ],
    "russia": [
        row(
            "mt-ru-saint-paul-apostle",
            "russia",
            "MT",
            "Russian Orthodox Parish of Saint Paul the Apostle",
            "Приход Святого Первоверховного Апостола Павла",
            "Parish",
            [MALTA_RUSSIAN_FOUNDING, MALTA_RUSSIAN_CURRENT],
            address=[
                "Church of Our Lady of Damascus",
                "132A Archbishop Street",
                "Valletta, Malta",
            ],
            founded=[
                "Принять новообразованный приход в честь Святого Первоверховного Апостола Павла в г. Валлетта, Мальта, в юрисдикцию Русской Православной Церкви Московского Патриархата.",
            ],
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "gi-rocor-saint-frideswide",
            "ru-great-britain-and-western-europe-rocor",
            "GI",
            "Parish of Saint Frideswide in Gibraltar",
            "Приходъ въ честь преподобной Фридесвиды",
            "Parish",
            [GIBRALTAR_DIRECTORY, GIBRALTAR_FOUNDING],
            address=[
                "The King's Chapel",
                "302 Main Street",
                "Gibraltar GX11 1AA",
            ],
        ),
    ],
}


EXPECTED = {
    "ep-malta": 5,
    "ro-italy": 1,
    "ru-great-britain-and-western-europe-rocor": 1,
    "russia": 1,
    "sr-switzerland": 1,
}

EXPECTED_COUNTRIES = {"GI": 1, "MT": 8}

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
    prohibited = ("\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d")
    if any(mark in serialized for mark in prohibited):
        raise ValueError("%s contains prohibited punctuation" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    country_counts = {country: 0 for country in COUNTRIES}
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        countries = set()
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off unknown parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") != "parish":
                raise ValueError("%s has unsupported kind" % row_id)
            country = item.get("country")
            if country not in COUNTRIES:
                raise ValueError("%s has invalid country: %s" %
                                 (row_id, country))
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            countries.add(country)
            country_counts[country] += 1
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
        raise ValueError("Malta and Gibraltar parent counts changed: %r" % actual)
    if country_counts != EXPECTED_COUNTRIES:
        raise ValueError("Malta and Gibraltar country counts changed: %r" %
                         country_counts)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != sum(EXPECTED.values()):
        raise ValueError("Malta and Gibraltar English name coverage changed")
    return payloads


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = ["missing directory parent: %s" % parent
              for parent in payloads if parent not in base_ids]
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def manifest(payloads=None):
    payloads = payloads or build()
    return {parent: {"url": "/data/directory/%s.v1.json" % parent,
                     "count": len(payload["rows"]),
                     "countries": payload["countries"]}
            for parent, payload in sorted(payloads.items())}


def export(payloads=None):
    return {"branches": payloads or build()}


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
        print("directory Malta and Gibraltar: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(export(payloads), ensure_ascii=False, indent=2))
        return 0
    print("Malta and Gibraltar: %d bodies and worship sites under %d canonical parents" %
          (sum(EXPECTED.values()), len(EXPECTED)))
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
