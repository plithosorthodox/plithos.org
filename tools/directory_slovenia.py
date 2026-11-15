#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Slovenia.

The official-source union preserves overlapping Serbian, Romanian, and
Macedonian structures without treating one national jurisdiction as a proxy
for another.

    python tools/directory_slovenia.py --check
    python tools/directory_slovenia.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-15"

SERBIAN_CONTACTS = "https://mitropolija-zagrebacka.org/kontakti/"
SERBIAN_SERVICES = "https://mitropolija-zagrebacka.org/raspored-bogosluzenja/"
SERBIAN_NATIVITY_MONASTERY = (
    "https://mitropolija-zagrebacka.org/"
    "liturgija-u-manastiru-rodjenja-presvete-bogorodice/"
)
SERBIAN_NATIVITY_FOUNDING = (
    "https://spc.rs/sr/news/4008.prvi-pravoslavni-manastir-u-sloveniji.html"
)
SERBIAN_VINDOL_MONASTERY = (
    "https://mitropolija-zagrebacka.org/"
    "duhovski-ponedjeljak-u-manastiru-na-vindolu/"
)
ROMANIAN_EXTERNAL = (
    "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
    "reprezentante-si-comunitati-externe/"
)
ROMANIAN_HISTORY = "https://parohiaortodoxa.si/istoric/"
ROMANIAN_PARISH = "https://parohiaortodoxa.si/"
MACEDONIAN_DIRECTORY = (
    "https://mpee.mk/category/juzno-evropsko-namesnistvo-2"
)


def row(row_id, parent, name, local, sources, rank="Parish", kind="parish",
        address=None, site=None, services=None, founded=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "SI",
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
    return value


SERBIAN_ROWS = [
    row(
        "si-sr-koper-saint-sava", "sr-zagreb-ljubljana",
        "Saint Sava Serbian Orthodox Church in Koper",
        "Храм Светог Саве",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Ulica talcev 3", "6000 Koper, Slovenia"],
    ),
    row(
        "si-sr-kranj-archangel-michael", "sr-zagreb-ljubljana",
        "Holy Archangel Michael Serbian Orthodox Church in Kranj",
        "Храм Светог Архангела Михаила",
        [SERBIAN_CONTACTS], rank="Church",
        address=["Golniška 16", "4000 Kranj, Slovenia"],
    ),
    row(
        "si-sr-ljubljana-cyril-methodius", "sr-zagreb-ljubljana",
        "Saints Cyril and Methodius Serbian Orthodox Church in Ljubljana",
        "Храм Светих Кирила и Методија",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Prešernova cesta 35", "1000 Ljubljana, Slovenia"],
        site="https://spcoljubljana.si/",
    ),
    row(
        "si-sr-maribor-cyril-methodius", "sr-zagreb-ljubljana",
        "Saints Cyril and Methodius Serbian Orthodox Church in Maribor",
        "Храм Светих Кирила и Методија",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Tržaška cesta 13", "2000 Maribor, Slovenia"],
    ),
    row(
        "si-sr-nova-gorica-holy-trinity", "sr-zagreb-ljubljana",
        "Holy Trinity Serbian Orthodox Church in Nova Gorica",
        "Храм Свете Тројице",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Kidričeva ulica 34 B", "5000 Nova Gorica, Slovenia"],
    ),
    row(
        "si-sr-novo-mesto-saint-sava", "sr-zagreb-ljubljana",
        "Saint Sava Serbian Orthodox Church in Novo Mesto",
        "Храм Светог Саве",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Na žago 16", "8000 Novo Mesto, Slovenia"],
    ),
    row(
        "si-sr-celje-burning-relics-sava", "sr-zagreb-ljubljana",
        "Burning of the Relics of Saint Sava Serbian Orthodox Church in Celje",
        "Храм Спаљивања моштију Светог Саве",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Kulturniška ulica 32", "3000 Celje, Slovenia"],
    ),
    row(
        "si-sr-postojna-protection-theotokos", "sr-zagreb-ljubljana",
        "Protection of the Most Holy Theotokos Serbian Orthodox Church in Postojna",
        "Храм Покрова Пресвете Богородице",
        [SERBIAN_CONTACTS, SERBIAN_SERVICES], rank="Church",
        address=["Notranjska ulica 1", "6230 Postojna, Slovenia"],
    ),
    row(
        "si-sr-smartno-protection-theotokos", "sr-zagreb-ljubljana",
        "Protection of the Most Holy Theotokos Serbian Orthodox Church in Šmartno pri Litiji",
        "Храм Покрова Пресвете Богородице у Шмартном при Литији",
        [SERBIAN_SERVICES], rank="Recurring Worship Site",
        address=["Šmartno pri Litiji, Slovenia"],
        services=["Divine Liturgy is served on the first Saturday of each month."],
    ),
    row(
        "si-sr-kocevje-basil-ostrog", "sr-zagreb-ljubljana",
        "Saint Basil of Ostrog Serbian Orthodox Church in Kočevje",
        "Храм Светог Василија Острошког у Кочевју",
        [SERBIAN_SERVICES], rank="Recurring Worship Site",
        address=["Kočevje, Slovenia"],
        services=["Divine Liturgy is served on the last Saturday of each month."],
    ),
    row(
        "si-sr-ravne-cosmas-damian", "sr-zagreb-ljubljana",
        "Saints Cosmas and Damian Serbian Orthodox Church in Ravne na Koroškem",
        "Храм Светих Козме и Дамјана у Равнама на Корошкем",
        [SERBIAN_SERVICES], rank="Recurring Worship Site",
        address=["Ravne na Koroškem, Slovenia"],
        services=["Divine Liturgy is served on Sundays."],
    ),
    row(
        "si-sr-dolenje-laknice-nativity-monastery",
        "sr-zagreb-ljubljana",
        "Nativity of the Most Holy Theotokos Monastery in Dolenje Laknice",
        "Манастир Рођења Пресвете Богородице у Долењим Лакницама",
        [SERBIAN_NATIVITY_FOUNDING, SERBIAN_NATIVITY_MONASTERY],
        rank="Monastery", kind="monastery",
        address=["Dolenje Laknice", "near Novo Mesto, Slovenia"],
        founded=[
            "The monastery property was acquired in 2021.",
            "The first Divine Liturgy in its newly built church was served on 25 October 2026.",
        ],
    ),
    row(
        "si-sr-vindol-luke-peter-monastery", "sr-zagreb-ljubljana",
        "Holy Apostle Luke and Saint Peter of Cetinje Monastery at Vindol",
        "Манастир Светог апостола Луке и Светог Петра Цетињског на Виндолу",
        [SERBIAN_VINDOL_MONASTERY], rank="Monastery", kind="monastery",
        address=["Vindol, Lesično, Slovenia"],
        services=[
            "Matins and Divine Liturgy are served each Monday beginning at 07:30 and 09:00 respectively."
        ],
    ),
]


ROMANIAN_ROWS = [
    row(
        "si-ro-ljubljana-ascension-staniloae", "romania",
        "Ascension of the Lord and Saint Confessor Priest Dumitru Stăniloae Romanian Orthodox Parish in Ljubljana",
        "Parohia Ortodoxă Română din Ljubljana, Înălțarea Domnului și Sfântul Preot Mărturisitor Dumitru Stăniloae",
        [ROMANIAN_EXTERNAL, ROMANIAN_HISTORY, ROMANIAN_PARISH],
        address=["Biserica Hristos Mântuitorul", "Podutiška cesta 20",
                 "1000 Ljubljana, Slovenia"],
        site=ROMANIAN_PARISH,
        founded=["The parish was established on 4 June 2021."],
    ),
]


MACEDONIAN_ROWS = [
    row(
        "si-mk-kranj-holy-trinity", "mk-europe",
        "Holy Trinity Macedonian Orthodox Church Community in Kranj",
        "МПЦО Света Тројца, Крањ, Словенија",
        [MACEDONIAN_DIRECTORY], rank="Church Community",
    ),
    row(
        "si-mk-ljubljana-clement-ohrid", "mk-europe",
        "Saint Clement of Ohrid Macedonian Orthodox Church Community in Ljubljana",
        "МПЦО Свети Климент Охрдски, Љубљана",
        [MACEDONIAN_DIRECTORY], rank="Church Community",
    ),
    row(
        "si-mk-koper-theophany", "mk-europe",
        "Theophany Macedonian Orthodox Church Community in Koper",
        "МПЦО Богојавленије Водици, Копер, Словенија",
        [MACEDONIAN_DIRECTORY], rank="Church Community",
    ),
]


ROWS = {
    "mk-europe": MACEDONIAN_ROWS,
    "romania": ROMANIAN_ROWS,
    "sr-zagreb-ljubljana": SERBIAN_ROWS,
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "mk-europe": 3,
    "romania": 1,
    "sr-zagreb-ljubljana": 13,
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
    for key in ("address", "services", "founded"):
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
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if not item.get("local"):
                raise ValueError("%s has no local name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "SI",
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Slovenia counts changed: %r" % counts)
    return payloads


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Slovenia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Slovenia: 17 verified bodies across 3 canonical parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
