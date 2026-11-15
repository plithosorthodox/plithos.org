#!/usr/bin/env python3
"""Validated directory fragments for Azerbaijan.

The Baku and Azerbaijan Diocese publishes a current roster of seven parish
churches, two embassy chapels, and four prison prayer rooms. Two prayer rooms
are named and two are not, so only the eleven named bodies are emitted. Four
current Georgian Orthodox churches are exposed as direct contributions to the
existing Georgian parent. Unnamed and unresolved bodies remain in the
companion candidate ledger.

    python tools/directory_azerbaijan.py --check
    python tools/directory_azerbaijan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

RUSSIAN_ROSTER = "https://pravoslavie.az/eparchy/index/"
RUSSIAN_DIOCESE = "https://patriarchia.ru/org/140"
RUSSIAN_CHURCH = "https://pravoslavie.az/eparchy/churches/?id=%s"

AZERBAIJAN_CHRISTIANITY = (
    "https://multikulturalizm.gov.az/az/post/1130/"
    "azerbaycanda-xristianliq.html"
)
AZERBAIJAN_CHURCHES = (
    "https://multikulturalizm.gov.az/az/post/1729/"
    "azerbaycanda-fealiyyet-gosteren-kilseler.html"
)
GEORGIAN_EMBASSY = "https://azerbaijan.mfa.gov.ge/diaspora"
GEORGIAN_HERETI = "https://patriarchate.ge/news/3339"
GEORGIAN_ALIBEYLI_SERVICE = (
    "https://ganja.mfa.gov.ge/ka/news/479074-"
    "generaluri-konsuli-daestsro-ninoobis-dghesastsauls"
)
GEORGIAN_QAKH_SERVICE = (
    "https://ganja.mfa.gov.ge/news/719150-"
    "generaluri-konsuli-daestsro-mariamobis-dghesastsauls-q-kakhshi"
)


def russian_row(row_id, name, local, rank, sources, address=None):
    row = {
        "id": row_id,
        "parent": "ru-baku",
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "AZ",
        "sources": sources,
    }
    if address:
        row["address"] = address
    return row


RUSSIAN_ROWS = [
    russian_row(
        "az-ru-baku-myrrhbearers-cathedral",
        "Cathedral of the Holy Myrrh-bearing Women in Baku",
        "Кафедральный собор святых Жен-Мироносиц г. Баку",
        "Cathedral Parish",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13575"],
        ["19 Eldar Aghayev Street", "Baku, Azerbaijan"],
    ),
    russian_row(
        "az-ru-baku-nativity-theotokos-cathedral",
        "Cathedral of the Nativity of the Most Holy Theotokos in Baku",
        "Собор Рождества Пресвятой Богородицы г. Баку",
        "Cathedral Parish",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13576"],
        ["205 Shamil Azizbeyov Street", "Baku, Azerbaijan"],
    ),
    russian_row(
        "az-ru-baku-archangel-michael",
        "Church of the Archangel Michael in Baku",
        "Храм Архангела Михаила г. Баку",
        "Parish",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13577"],
        ["38 Zargarpalan Street", "Baku, Azerbaijan"],
    ),
    russian_row(
        "az-ru-ganja-alexander-nevsky",
        "Church of Saint Alexander Nevsky in Ganja",
        "Храм святого благоверного великого князя Александра Невского г. Гянджа",
        "Parish",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13578"],
        ["2 Haji Ali Huseynzade Street", "Ganja, Azerbaijan"],
    ),
    russian_row(
        "az-ru-khachmaz-saint-nicholas",
        "Church of Saint Nicholas the Wonderworker in Khachmaz",
        "Храм святителя Николая Чудотворца г. Хачмаз",
        "Parish",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13579"],
        ["21 Khanlar Street", "Khachmaz, Azerbaijan"],
    ),
    russian_row(
        "az-ru-sumgayit-seraphim-sarov",
        "Church of Saint Seraphim of Sarov in Sumgayit",
        "Храм преподобного Серафима Саровского г. Сумгаит",
        "House Church",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13580"],
        ["Apartment 18, 24/5, 19th Quarter", "Sumgayit, Azerbaijan"],
    ),
    russian_row(
        "az-ru-lankaran-protection-theotokos",
        "Church of the Protection of the Most Holy Theotokos in Lankaran",
        "Храм Покрова Богородицы г. Ленкорань",
        "Parish",
        [RUSSIAN_ROSTER, RUSSIAN_CHURCH % "13644"],
        [
            "Mammad Asadov Street",
            "Russian Cemetery, entrance from I. Nasimi Street",
            "Lankaran, Azerbaijan",
        ],
    ),
    russian_row(
        "az-ru-baku-russian-embassy-alexander-nevsky",
        "Chapel of Saint Alexander Nevsky at the Russian Embassy in Baku",
        "Часовня Александра Невского при Посольстве России в г. Баку",
        "Chapel",
        [RUSSIAN_ROSTER],
    ),
    russian_row(
        "az-ru-baku-belarusian-embassy-cyril-turov",
        "Chapel of Saint Cyril of Turov at the Belarusian Embassy in Baku",
        "Часовня Кирилла Туровского при Посольстве Белоруссии в г. Баку",
        "Chapel",
        [RUSSIAN_ROSTER],
    ),
    russian_row(
        "az-ru-baku-prison-4-anastasia",
        (
            "Prayer Room of Great Martyr Anastasia the Deliverer from "
            "Bonds at Penitentiary Institution No. 4 in Baku"
        ),
        (
            "Молитвенная комната в честь вмч. Анастасии Узорешительницы "
            "на территории пенитенциарного учреждения №4 г. Баку"
        ),
        "Prayer Room",
        [RUSSIAN_ROSTER],
    ),
    russian_row(
        "az-ru-baku-prison-10-george",
        (
            "Prayer Room of Great Martyr George the Victory-Bearer at "
            "Penitentiary Institution No. 10 in Baku"
        ),
        (
            "Молитвенная комната в честь вмч. Георгия Победоносца на "
            "территории пенитенциарного учреждения №10 г. Баку"
        ),
        "Prayer Room",
        [RUSSIAN_ROSTER],
    ),
]


def georgian_row(row_id, name, local, sources):
    return {
        "id": row_id,
        "parent": "georgia",
        "kind": "parish",
        "rank": "Church",
        "name": name,
        "local": local,
        "country": "AZ",
        "sources": sources,
    }


DIRECT_GEORGIA_ROWS = [
    georgian_row(
        "az-ge-qax-ingiloy-saint-george",
        "Saint George Georgian Orthodox Church in Qax Ingiloy",
        "Qaxingiloy kəndində Müqəddəs Georgi gürcü-pravoslav kilsəsi",
        [AZERBAIJAN_CHRISTIANITY, AZERBAIJAN_CHURCHES,
         GEORGIAN_QAKH_SERVICE],
    ),
    georgian_row(
        "az-ge-alibayli-saint-nino",
        "Saint Nino Georgian Orthodox Church in Alibayli",
        "Əlibəyli kəndində Müqəddəs Nino kilsəsi",
        [AZERBAIJAN_CHRISTIANITY, AZERBAIJAN_CHURCHES,
         GEORGIAN_ALIBEYLI_SERVICE],
    ),
    georgian_row(
        "az-ge-meshabash-saint-michael",
        "Saint Michael Georgian Orthodox Church in Meshabash",
        "Meşəbaş kəndində Müqəddəs Mixeyil kilsəsi",
        [AZERBAIJAN_CHRISTIANITY, AZERBAIJAN_CHURCHES,
         GEORGIAN_HERETI],
    ),
    georgian_row(
        "az-ge-kotuklu-holy-trinity",
        "Holy Trinity Georgian Orthodox Church in Kotuklu",
        "Kötüklü kəndində Müqəddəs Sameba kilsəsi",
        [AZERBAIJAN_CHRISTIANITY, AZERBAIJAN_CHURCHES,
         GEORGIAN_HERETI],
    ),
]

ENGLISH_NAMES = {
    row["id"]: row["name"] for row in RUSSIAN_ROWS + DIRECT_GEORGIA_ROWS
}


EXPECTED = {"ru-baku": 11}
DIRECT_GEORGIA_EXPECTED = 4
ALLOWED_RANKS = {
    "Cathedral Parish", "Parish", "House Church", "Chapel",
    "Prayer Room", "Church",
}


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
    return row


def validate_rows(source_rows, parent, all_seen):
    rows = []
    names = set()
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in all_seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != parent:
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if row.get("country") != "AZ":
            raise ValueError("%s is outside Azerbaijan" % row_id)
        if row.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        name = row.get("name", "")
        local = row.get("local", "")
        if not name or not local:
            raise ValueError("%s lacks a usable local or English name" % row_id)
        if any("\u0400" <= char <= "\u04ff" or
               "\u10a0" <= char <= "\u10ff" for char in name):
            raise ValueError("%s has local script in its English name" % row_id)
        if name[:1].islower() or "  " in name or name.endswith(" -"):
            raise ValueError("%s has malformed English text" % row_id)
        key = name.casefold()
        if key in names:
            raise ValueError("duplicate reader-facing name: %s" % name)
        names.add(key)
        rendered = json.dumps(row, ensure_ascii=False)
        if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
            raise ValueError("%s has forbidden punctuation or encoding" % row_id)
        if row.get("address") and (
                not isinstance(row["address"], list) or
                not all(isinstance(value, str) for value in row["address"])):
            raise ValueError("%s has an invalid address" % row_id)
        all_seen.add(row_id)
        rows.append(row)
    return rows


def build_all():
    all_seen = {"ru-baku", "georgia"}
    russian = validate_rows(RUSSIAN_ROWS, "ru-baku", all_seen)
    georgian = validate_rows(DIRECT_GEORGIA_ROWS, "georgia", all_seen)
    combined_names = {}
    for row in russian + georgian:
        key = row["name"].casefold()
        if key in combined_names:
            raise ValueError("duplicate reader-facing name: %s and %s" % (
                combined_names[key], row["id"],
            ))
        combined_names[key] = row["id"]
    if len(russian) != EXPECTED["ru-baku"]:
        raise ValueError("Baku Diocese count changed: %d" % len(russian))
    if len(georgian) != DIRECT_GEORGIA_EXPECTED:
        raise ValueError("Georgian direct count changed: %d" % len(georgian))
    if set(ENGLISH_NAMES) != {row["id"] for row in russian + georgian}:
        raise ValueError("Azerbaijan English name map is out of sync")
    payloads = {
        "ru-baku": {
            "v": 1,
            "parent": "ru-baku",
            "country": "AZ",
            "rows": russian,
        }
    }
    return payloads, georgian


def build():
    return build_all()[0]


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads, georgian = build_all()
    except (OSError, ValueError) as exc:
        print("directory Azerbaijan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(
            {"branches": payloads, "direct_georgia_rows": georgian},
            ensure_ascii=False, indent=2, sort_keys=True,
        ))
    print(
        "Azerbaijan: 11 verified Baku Diocese bodies plus 4 direct Georgian rows"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
