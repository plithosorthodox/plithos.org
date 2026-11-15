#!/usr/bin/env python3
"""Validated directory fragments for four Western European microstates.

This module preserves current canonical Orthodox bodies and recurring worship
sites in Andorra, Monaco, San Marino, and Vatican City. It emits isolated
fragments for later merging and never writes shared directory data.

    python tools/directory_microstates.py --check
    python tools/directory_microstates.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"
COUNTRIES = {"AD", "MC", "SM", "VA"}

ANDORRA_CURRENT = "https://eparchia.patriarchia.ru/article/122320"
ANDORRA_DIOCESE = (
    "https://orthodoxspain.com/"
    "arxiepiskop-nestor-posetil-kazanskuyu-obshhinu-knyazhestva-andorra-"
    "i-vstretilsya-s-episkopom-i-sporavitelem-knyazhestva"
)
MONACO_EP = (
    "https://mgro.fr/fr/paroisse/"
    "chapelle-la-toute-sainte-mere-de-dieu/"
)
MONACO_ROCOR_FEAST = (
    "https://orthodox-europe.org/content/monaco-altar-feast-2026/"
)
ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
MONACO_KORSUN_FEAST = (
    "https://www.egliserusse.eu/"
    "Fete-onomastique-de-la-paroisse-des-Saints-Martyrs-imperiaux-a-"
    "Monaco_a2490.html"
)
MONACO_KORSUN_SYNOD = "https://patriarchia.ru/db/text/5730334"
SAN_MARINO_EP = (
    "https://ortodossia.it/luoghi-di-culto/"
    "parrocchia-di-san-michele-arcangelo-2/"
)
SAN_MARINO_EP_PATRIARCHATE = (
    "https://ec-patr.org/entities/iera-mitropoli-italias-melitis/"
)
SAN_MARINO_ROMANIAN = (
    "https://www.episcopia-italiei.it/it/parrocchie/"
    "404-san-marino-repubblica"
)
SAN_MARINO_ROMANIAN_LIST = (
    "https://episcopia-italiei.it/ro/organizare-2026-context/8830-parohii2026"
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
    "ru-spain-and-portugal": [
        row(
            "ad-ru-kazan-icon-community",
            "ru-spain-and-portugal",
            "AD",
            "Kazan Icon of the Mother of God Orthodox Community in Andorra",
            "Община в честь Казанской иконы Божией Матери",
            "Community",
            [ANDORRA_CURRENT, ANDORRA_DIOCESE],
            services=[
                "Богослужения совершаются ежемесячно в предоставляемом католической епархией Урхеля древнем романском храме святых Иулиана и Германа.",
            ],
        ),
    ],
    "ep-france": [
        row(
            "mc-ep-all-holy-mother-of-god-chapel",
            "ep-france",
            "MC",
            "Chapel of the All-Holy Mother of God",
            "Chapelle la-Toute-Sainte-Mère-de-Dieu",
            "Chapel",
            [MONACO_EP],
            address=["Place de la Visitation", "98000 Monaco"],
            site=MONACO_EP,
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "mc-rocor-saint-elena",
            "ru-great-britain-and-western-europe-rocor",
            "MC",
            "Parish of the Holy Equal-to-the-Apostles Empress Elena",
            "Paroisse de la Sainte Impératrice Elena",
            "Parish",
            [ROCOR_DIRECTORY, MONACO_ROCOR_FEAST],
            address=[
                "St Paul's Church",
                "22 avenue de Grande-Bretagne",
                "Monte-Carlo, Monaco",
            ],
        ),
    ],
    "ru-korsun": [
        row(
            "mc-ru-holy-royal-passion-bearers",
            "ru-korsun",
            "MC",
            "Parish of the Holy Royal Passion-Bearers in Monaco",
            "Paroisse des Saints Martyrs impériaux à Monaco",
            "Parish",
            [MONACO_KORSUN_FEAST, MONACO_KORSUN_SYNOD],
            founded=[
                "Включить приход святых Царственных Страстотерпцев в Княжестве Монако в состав Корсунской епархии.",
            ],
        ),
    ],
    "ep-italy": [
        row(
            "sm-ep-saint-michael-archangel",
            "ep-italy",
            "SM",
            "Parish of Saint Michael the Archangel",
            "Parrocchia di San Michele Arcangelo",
            "Parish",
            [SAN_MARINO_EP, SAN_MARINO_EP_PATRIARCHATE],
            address=[
                "Chiesa di San Michele",
                "Strada San Michele",
                "Località Serravalle, Repubblica di San Marino",
            ],
            site=SAN_MARINO_EP,
            services=[
                "Divina Liturgia: Primo e Secondo Sabato del mese ore 10,30",
            ],
        ),
    ],
    "ro-italy": [
        row(
            "sm-ro-saint-marina",
            "ro-italy",
            "SM",
            "Parish of the Holy Great Martyr Marina",
            "Parohia Sfânta Mare Muceniță Marina",
            "Parish",
            [SAN_MARINO_ROMANIAN_LIST, SAN_MARINO_ROMANIAN],
            address=[
                "Chiesa di Ca' Centino",
                "Strada Canepa",
                "47890 San Marino, Repubblica di San Marino",
            ],
            site=SAN_MARINO_ROMANIAN,
            founded=[
                "Din data de 12 februarie 2016, prin decizia Preasfințitului Părinte Episcop Siluan, să se înființeze ca Parohia Ortodoxă Română cu hramul Sfânta Mare Muceniță Marina (17 iulie) din San Marino (Republica), Protopopiatul Emilia-Romagna II.",
            ],
        ),
    ],
}


EXPECTED = {
    "ep-france": 1,
    "ep-italy": 1,
    "ro-italy": 1,
    "ru-great-britain-and-western-europe-rocor": 1,
    "ru-korsun": 1,
    "ru-spain-and-portugal": 1,
}

EXPECTED_COUNTRIES = {
    "AD": 1,
    "MC": 3,
    "SM": 2,
    "VA": 0,
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
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") != "parish":
                raise ValueError("%s has unsupported kind: %s" %
                                 (row_id, item.get("kind")))
            country = item.get("country")
            if country not in COUNTRIES:
                raise ValueError("%s has invalid microstate code: %s" %
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
        payload = {
            "v": 1,
            "parent": parent,
            "rows": rows,
        }
        if len(countries) == 1:
            payload["country"] = next(iter(countries))
        else:
            payload["countries"] = sorted(countries)
        payloads[parent] = payload
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("microstate parent counts changed: %r" % actual)
    if country_counts != EXPECTED_COUNTRIES:
        raise ValueError("microstate country counts changed: %r" % country_counts)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 6:
        raise ValueError("microstate English name coverage changed")
    return payloads


def contributions(payloads=None):
    """Return all rows grouped for the shared directory builders."""
    payloads = payloads or build()
    return {parent: list(payload["rows"])
            for parent, payload in payloads.items()}


def manifest(payloads=None):
    payloads = payloads or build()
    result = {}
    for parent, payload in sorted(payloads.items()):
        item = {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "merge_required": True,
        }
        if "country" in payload:
            item["country"] = payload["country"]
        else:
            item["countries"] = payload["countries"]
        result[parent] = item
    return result


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
        errors.append("microstate row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def candidate_ledger_problems():
    path = ROOT / "tools" / "directory_candidates" / "microstates.json"
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    errors = []
    if ledger.get("countries") != ["AD", "MC", "SM", "VA"]:
        errors.append("microstate candidate ledger country order changed")
    summary = ledger.get("published_summary") or {}
    if summary.get("total") != sum(EXPECTED.values()):
        errors.append("microstate candidate ledger total does not match rows")
    serialized = json.dumps(ledger, ensure_ascii=False)
    prohibited = ("\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d")
    if any(mark in serialized for mark in prohibited):
        errors.append("microstate candidate ledger contains prohibited punctuation")
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        errors = repository_problems(payloads) + candidate_ledger_problems()
    except (OSError, ValueError) as exc:
        print("directory microstates: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Microstates: 6 current bodies across 4 countries")
    for country in ("AD", "MC", "SM", "VA"):
        print("%s: %d" % (country, EXPECTED_COUNTRIES[country]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
