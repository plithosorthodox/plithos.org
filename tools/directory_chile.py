#!/usr/bin/env python3
"""Validated current Eastern Orthodox directory fragments for Chile.

Only bodies supported by a competent current Church source are emitted.
Overlapping jurisdictional claims, historical bodies, cultural associations,
and search-discovered bodies remain in the companion candidate ledger.

    python tools/directory_chile.py --check
    python tools/directory_chile.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "chile.json"

ANTIOCH_HOME = "https://www.chileortodoxo.cl/"
ANTIOCH_PARISHES = "https://www.chileortodoxo.cl/parroquias.html"
ANTIOCH_HISTORY = "https://www.chileortodoxo.cl/historia.html"
ANTIOCH_CLERGY = "https://www.chileortodoxo.cl/estructura.html"
ANTIOCH_NATIVITY = "https://nsvmortodoxa.cl/"

EP_BUENOS_AIRES = (
    "https://ec-patr.org/entities/iera-mitropoli-mpoyenos-aires/"
)
EP_SANTIAGO = "https://www.iglesiaortodoxagriega.cl/nuestra-parroquia"

MOSCOW_ROSTER = "https://southamerica.cerkov.ru/xramy-eparxii/"
MOSCOW_SANTIAGO_2026 = (
    "https://southamerica.cerkov.ru/2026/09/16/"
    "v-xrame-vo-imya-svyatogo-apostola-evangelista-ioanna-bogoslova-"
    "goroda-santyago-respublika-chili-byla-sovershena-bozhestvennaya-"
    "liturgiya/"
)

SERBIAN_DIRECTORY = (
    "https://www.iglesiaortodoxaserbiasca.org/_files/ugd/"
    "e8757a_bcd3fd85dc81441196589a1b3065f8bd.pdf"
)
SERBIAN_DIOCESE = "https://www.iglesiaortodoxaserbiasca.org/diocesis"
SERBIAN_CHILE = (
    "https://www.iglesiaortodoxaserbiasca.org/single-post/2019/03/27/"
    "visita-a-chile-de-su-eminencia-kirilo-obispo-de-buenos-aires-"
    "centro-y-sur-am%C3%A9rica"
)

ROCOR_DIRECTORY = "https://directory.synod.com/listings/"
ROCOR_SANTIAGO = (
    "https://directory.synod.com/listing/101/"
    "church-of-the-holy-trinity-and-icon-of-virgin-of/"
)
ROCOR_SANTIAGO_2026 = "https://iglesiarusa.info/?p=7425"
ROCOR_NECTARIOS = (
    "https://directory.synod.com/listing/100/"
    "parroquia-de-san-nectario-de-pentapolis/"
)

ROMANIAN_CHILE = "https://iglesiaortodoxarumana.org/chile/"
ROMANIAN_ALMANAC = "https://www.mitropolia.us/pdf/2025.05.15-almanah.pdf"
ROMANIAN_CONSECRATION = (
    "https://www.mitropolia.us/index.php/en/1921-the-historic-visit-of-"
    "his-eminence-metropolitan-nicolae-to-latin-america-the-fourth-"
    "spiritual-pilgrimage"
)


def body(row_id, parent, name, local, seat, rank, sources, address=None,
         site=None, kind="parish"):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "CL",
        "checked": CHECKED,
        "sources": sources,
    }
    if address:
        row["address"] = address
    if site:
        row["site"] = site
    return row


ANTIOCH_ROWS = [
    body(
        "cl-an-santiago-saint-george-cathedral", "an-santiago",
        "Saint George Cathedral in Santiago", "Catedral Ortodoxa San Jorge",
        "Santiago", "Cathedral Parish",
        [ANTIOCH_HOME, ANTIOCH_PARISHES, ANTIOCH_CLERGY],
        ["Santa Filomena 372, Recoleta", "Santiago, Chile"],
    ),
    body(
        "cl-an-santiago-nativity-theotokos", "an-santiago",
        "Nativity of the Most Holy Virgin Mary Parish in Santiago",
        "Parroquia Natividad de la Santísima Virgen María", "Santiago",
        "Parish", [ANTIOCH_HOME, ANTIOCH_PARISHES, ANTIOCH_NATIVITY],
        ["Avenida Pedro de Valdivia 92, Providencia", "Santiago, Chile"],
        site=ANTIOCH_NATIVITY,
    ),
    body(
        "cl-an-santiago-saint-nicholas", "an-santiago",
        "Saint Nicholas Church in Santiago", "Iglesia Ortodoxa San Nicolás",
        "Santiago", "Church",
        [ANTIOCH_HOME, ANTIOCH_PARISHES, ANTIOCH_CLERGY],
        ["Eusebio Lillo 472, Recoleta", "Santiago, Chile"],
    ),
    body(
        "cl-an-vina-del-mar-dormition-theotokos", "an-santiago",
        "Dormition of the Most Holy Virgin Mary Church in Viña del Mar",
        "Iglesia Ortodoxa de la Dormición de la Santísima Virgen María",
        "Viña del Mar", "Church",
        [ANTIOCH_HOME, ANTIOCH_PARISHES, ANTIOCH_CLERGY],
        ["1 Poniente 420", "Viña del Mar, Chile"],
    ),
    body(
        "cl-an-rancagua-saint-george", "an-santiago",
        "Saint George Church in Rancagua", "Iglesia Ortodoxa San Jorge",
        "Rancagua", "Church",
        [ANTIOCH_HOME, ANTIOCH_PARISHES, ANTIOCH_CLERGY],
        ["Pedro José Campos 945, Población Manso de Velasco", "Rancagua, Chile"],
    ),
    body(
        "cl-an-santiago-saint-helen", "an-santiago",
        "Saint Helen Church in Santiago", "Iglesia Ortodoxa Santa Elena",
        "Santiago", "Church",
        [ANTIOCH_HOME, ANTIOCH_PARISHES, ANTIOCH_CLERGY],
        ["General San Martín 13026, Población Raúl del Canto, La Pintana",
         "Santiago, Chile"],
    ),
]


EP_ROWS = [
    body(
        "cl-ep-santiago-constantine-helen", "ep-buenos-aires",
        "Saints Constantine and Helen Church in Santiago",
        "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης", "Santiago", "Church",
        [EP_BUENOS_AIRES, EP_SANTIAGO],
        ["Avenida Grecia 2461, Ñuñoa", "Santiago, Chile"],
        site="https://www.iglesiaortodoxagriega.cl/",
    ),
    body(
        "cl-ep-las-cabras-nativity-theotokos", "ep-buenos-aires",
        "Nativity of the Theotokos Church in El Manzano",
        "Ἱερός Ναός τῆς Γεννήσεως τῆς Παναγίας", "El Manzano", "Church",
        [EP_BUENOS_AIRES],
        ["Callejón Los Urbanos 556", "El Manzano, Las Cabras, Chile"],
    ),
    body(
        "cl-ep-antofagasta-holy-cross-chapel", "ep-buenos-aires",
        "Exaltation of the Holy Cross Chapel in Antofagasta",
        "Ἱερόν Παρεκκλήσιον τῆς Ὑψώσεως τοῦ Τιμίου Σταυροῦ",
        "Antofagasta", "Chapel", [EP_BUENOS_AIRES],
        ["Sucre 462", "Antofagasta, Chile"],
    ),
]


MOSCOW_ROWS = [
    body(
        "cl-ru-santiago-john-theologian", "ru-argentina-and-south-america",
        "Saint John the Theologian Church in Santiago",
        "Храм святого апостола и евангелиста Иоанна Богослова в Сантьяго",
        "Santiago", "Church", [MOSCOW_ROSTER, MOSCOW_SANTIAGO_2026],
        ["Santa Rosa 12890, La Pintana", "Santiago, Chile"],
    ),
]


SERBIAN_ROWS = [
    body(
        "cl-sr-santiago-nikolai-zica", "sr-buenos-aires",
        "Saint Nikolai of Zica and Ohrid and All America Parish in Santiago",
        "Parroquia Santo Obispo Nikolai de Zica y Ohrid, y de Toda América",
        "Santiago", "Parish", [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        site="https://www.pravoslavie.cl/",
    ),
    body(
        "cl-sr-chile-chico-resurrection-monastery", "sr-buenos-aires",
        "Resurrection of the Lord Monastery in Chile Chico",
        "Monasterio de la Resurrección del Señor", "Chile Chico", "Monastery",
        [SERBIAN_DIRECTORY, SERBIAN_CHILE],
        ["Chacra 22 Lote B, Bahija Jara", "6050000 Chile Chico, Chile"],
        kind="monastery",
    ),
]


ROCOR_ROWS = [
    body(
        "cl-rocor-santiago-holy-trinity-kazan", "ru-south-america-rocor",
        "Church of the Holy Trinity and Icon of the Virgin of Kazan in Santiago",
        "Храм Святой Троицы и Казанской иконы Божией Матери", "Santiago",
        "Church", [ROCOR_SANTIAGO, ROCOR_SANTIAGO_2026],
        ["Avenida Holanda 3576, Ñuñoa", "Santiago, Chile"],
        site=ROCOR_SANTIAGO,
    ),
    body(
        "cl-rocor-valdivia-nectarios-pentapolis", "ru-south-america-rocor",
        "Saint Nectarios of Pentapolis Parish in Valdivia",
        "Parroquia de San Nectario de Pentápolis", "Valdivia", "Parish",
        [ROCOR_NECTARIOS, ROCOR_DIRECTORY],
        ["Calle Aníbal Pinto 2175", "Valdivia, Chile"],
        site=ROCOR_NECTARIOS,
    ),
]


ROMANIAN_ROWS = [
    body(
        "cl-ro-concepcion-silouan-philothea", "romanian-americas",
        "Saint Silouan the Athonite and Saint Philothea of Argeș Romanian "
        "Orthodox Church in Concepción",
        "Iglesia Ortodoxa Rumana San Siluan del Monte Athos", "Concepción",
        "Parish", [ROMANIAN_CHILE, ROMANIAN_ALMANAC, ROMANIAN_CONSECRATION],
        ["Alhambra 300-B, Chiguayante", "Concepción, Chile"],
        site=ROMANIAN_CHILE,
    ),
]


ROWS = {
    "an-santiago": ANTIOCH_ROWS,
    "ep-buenos-aires": EP_ROWS,
    "ru-argentina-and-south-america": MOSCOW_ROWS,
    "sr-buenos-aires": SERBIAN_ROWS,
    "ru-south-america-rocor": ROCOR_ROWS,
    "romanian-americas": ROMANIAN_ROWS,
}

EXPECTED = {
    "an-santiago": 6,
    "ep-buenos-aires": 3,
    "ru-argentina-and-south-america": 1,
    "sr-buenos-aires": 2,
    "ru-south-america-rocor": 2,
    "romanian-americas": 1,
}
EXPECTED_TOTAL = 15
ALLOWED_KINDS = {"parish", "monastery"}
ALLOWED_RANKS = {"Cathedral Parish", "Parish", "Church", "Chapel", "Monastery"}

ALL_SOURCE_ROWS = sum(ROWS.values(), [])
ENGLISH_NAMES = {row["id"]: row["name"] for row in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ALL_SOURCE_ROWS}


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if row.get("site") and not row["site"].startswith("https://"):
        raise ValueError("%s carries a non-HTTPS site" % row.get("id"))
    return row


def address_key(row):
    values = row.get("address") or []
    if not values:
        return None
    return "|".join(value.casefold().strip() for value in values)


def validate_rows(source_rows, parent, all_seen, all_names, all_addresses):
    rows = []
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in all_seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != parent:
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if row.get("country") != "CL":
            raise ValueError("%s is outside Chile" % row_id)
        if row.get("kind") not in ALLOWED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        if not row.get("name") or not row.get("local") or not row.get("seat"):
            raise ValueError("%s lacks a usable name, local name, or seat" % row_id)
        if row["name"][:1].islower() or "  " in row["name"]:
            raise ValueError("%s has malformed English text" % row_id)
        name_key = row["name"].casefold()
        if name_key in all_names:
            raise ValueError("duplicate reader-facing name: %s and %s" % (
                all_names[name_key], row_id,
            ))
        if row.get("address") and (
                not isinstance(row["address"], list) or
                not all(isinstance(value, str) for value in row["address"])):
            raise ValueError("%s has an invalid address" % row_id)
        physical_key = address_key(row)
        if physical_key and physical_key in all_addresses:
            raise ValueError("duplicate physical address: %s and %s" % (
                all_addresses[physical_key], row_id,
            ))
        rendered = json.dumps(row, ensure_ascii=False)
        if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
            raise ValueError("%s has forbidden punctuation or encoding" % row_id)
        all_seen.add(row_id)
        all_names[name_key] = row_id
        if physical_key:
            all_addresses[physical_key] = row_id
        rows.append(row)
    return rows


def build():
    all_seen = {
        "an-santiago", "ep-buenos-aires", "ru-argentina-and-south-america",
        "sr-buenos-aires", "ru-south-america-rocor", "romanian-americas",
    }
    all_names = {}
    all_addresses = {}
    payloads = {}
    for parent, source_rows in ROWS.items():
        rows = validate_rows(
            source_rows, parent, all_seen, all_names, all_addresses,
        )
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "CL",
            "rows": rows,
        }
    row_ids = {
        row["id"] for payload in payloads.values() for row in payload["rows"]
    }
    if sum(len(payload["rows"]) for payload in payloads.values()) != EXPECTED_TOTAL:
        raise ValueError("Chile branch total must remain %d" % EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Chile English name map is out of sync")
    if set(ENGLISH_SEATS) != {row["seat"] for row in ALL_SOURCE_ROWS}:
        raise ValueError("Chile English seat map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "CL":
        raise ValueError("Chile candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Chile candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("worship_bodies") != EXPECTED_TOTAL:
        raise ValueError("Chile candidate ledger total is out of sync")
    for parent, expected in EXPECTED.items():
        if summary.get(parent) != expected:
            raise ValueError("Chile ledger count is out of sync for %s" % parent)
    required_lists = ("candidates", "exclusions", "official_jurisdiction_audit")
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Chile candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "CL":
            raise ValueError("%s is outside Chile" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Chile candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Chile ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Chile ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Chile candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Chile: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Chile: 15 current unique worship bodies across 6 branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
