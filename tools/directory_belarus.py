#!/usr/bin/env python3
"""Validated current Eastern Orthodox worship bodies in Belarus.

Every emitted row is taken from a current first-party Belarusian Exarchate,
diocesan, deanery, or parish roster. Central totals are used to detect gaps,
not to invent unnamed bodies. Unresolved discrepancies, inaccessible pages,
construction-only material, and out-of-scope bodies remain in the companion
candidate ledger.

    python tools/directory_belarus.py --check
    python tools/directory_belarus.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "belarus.json"

RAW_ROWS = {
  "ru-babruysk": [
    {
      "parent": "ru-babruysk",
      "local": "Барколабовский Вознесенский женский монастырь",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://bobreparhiya.by/borkolabovo_monastery/"
      ],
      "name": "Barkalabava Ascension Convent",
      "id": "by-babruysk-b2579a4760",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "БОРИСОГЛЕБСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Saints Boris and Gleb Church",
      "id": "by-babruysk-e2820bff44",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ЧАСОВНЯ ИКОНЫ БОЖИЕЙ МАТЕРИ \"ВСЕХ СКОРБЯЩИХ РАДОСТЬ\" НИКОЛО-СОФИЙСКОГО ХРАМА",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Joy of All Who Sorrow Icon of the Theotokos Chapel at the Saint Nicholas and Saint Sophia Church",
      "id": "by-babruysk-63c2799a95",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ЧАСОВНЯ ИКОНЫ БОЖИЕЙ МАТЕРИ \"ВЗЫСКАНИЕ ПОГИБШИХ\"",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Seeking of the Lost Icon of the Theotokos Chapel",
      "id": "by-babruysk-db0234d708",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм в честь св. блгв. кн. Александра Невского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Holy Right-believing Prince Alexander Nevsky Church",
      "id": "by-babruysk-0c4d209d4f",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм в честь Собора Белорусских святых Епархиального Духовно-просветительского центра \"Дружба\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Synaxis of the Belarusian Saints Church at the Friendship Diocesan Spiritual and Educational Center",
      "id": "by-babruysk-9053cc5f20",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм в честь иконы Божией Матери \"Спорительница хлебов\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Church in honor of the Icon of the Theotokos \"Multiplier of Wheat\"",
      "id": "by-babruysk-754393795c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ВСЕХ СВЯТЫХ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/glusskiy-okrug-prihod/"
      ],
      "name": "Church of All Saints",
      "id": "by-babruysk-84316d0e79",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИВЕРСКОЙ ИКОНЫ БОЖИЕЙ МАТЕРИ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Church of Iveron Icon of the Theotokos",
      "id": "by-babruysk-74fea9c447",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПРЕОБРАЖЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovsk_klichev_okrug/"
      ],
      "name": "Transfiguration of the Lord Church",
      "id": "by-babruysk-40b9a1693d",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СЕРГИЯ РАДОНЕЖСКОГО",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Saint Sergius of Radonezh Church",
      "id": "by-babruysk-368c773c7a",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ святого апостола Андрея Первозванного",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Church of ST. Apostle Andrew the First-Called",
      "id": "by-babruysk-0de1a62b85",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ святого ВАСИЛИЯ ВЕЛИКОГО",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of ST. Basil the Great",
      "id": "by-babruysk-90f1758fa4",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм прп. Евфросинии Полоцкой",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of Saint Euphrosyne of Polotsk",
      "id": "by-babruysk-f99cbab789",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СВЯТИТЕЛЯ НИКОЛАЯ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Church of ST. Nicholas",
      "id": "by-babruysk-e5645497b6",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-babruysk-b09a40ab4c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ Всемилостивого Спаса",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of the All-Merciful Savior",
      "id": "by-babruysk-f639c2ad83",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "БЛАГОВЕЩЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovsk_klichev_okrug/"
      ],
      "name": "Annunciation of the Most Holy Theotokos Church",
      "id": "by-babruysk-e0eec7dc94",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ УСПЕНИЯ ПРЕСВЯТОЙ БОГОРОДИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-babruysk-490e80da4c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм святого благоверного князя Александра Невского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Church of the Holy Right-believing Prince Alexander Nevsky",
      "id": "by-babruysk-baaf941d95",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СВЯТОЙ ВЕЛИКОМУЧЕНИЦЫ ПАРАСКЕВЫ ПЯТНИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Church of the Great Martyr Paraskeva",
      "id": "by-babruysk-acacbcda92",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СВЯТОЙ ЖИВОНАЧАЛЬНОЙ ТРОИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-babruysk-1575c5f981",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СВЯТОЙ ЖИВОНАЧАЛЬНОЙ ТРОИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-babruysk-38eb931d4c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СВЯТОЙ ЖИВОНАЧАЛЬНОЙ ТРОИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-babruysk-4723beec4a",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ СВЯТОГО ДУХА",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Church of the Holy Spirit",
      "id": "by-babruysk-a55a40eb60",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "СВЯТО-ДУХОВ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Holy Spirit Church",
      "id": "by-babruysk-55202e040f",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм святых бессребеников Космы и Дамиана (историко-культурная ценность)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/glusskiy-okrug-prihod/"
      ],
      "name": "Church of the Holy Unmercenaries Cosmas and Damian (historical and cultural value)",
      "id": "by-babruysk-d1376fdadc",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИКОНЫ БОЖИЕЙ МАТЕРИ \"ЦЕЛИТЕЛЬНИЦА\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Church of the Icon of the Theotokos \"Healer\"",
      "id": "by-babruysk-c1576f332e",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИКОНЫ БОЖИЕЙ МАТЕРИ \"ВСЕХ СКОРБЯЩИХ РАДОСТЬ\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Church of the Icon of the Theotokos \"Joy of All Who Sorrow\"",
      "id": "by-babruysk-9d960e7255",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИКОНЫ БОЖИЕЙ МАТЕРИ \"КАЗАНСКОЙ\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Church of the Icon of the Theotokos \"Kazan\"",
      "id": "by-babruysk-3ee9e5ab1f",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИКОНЫ БОЖИЕЙ МАТЕРИ \"КАЗАНСКОЙ\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of the Icon of the Theotokos \"Kazan\"",
      "id": "by-babruysk-e2a0882908",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИКОНЫ БОЖИЕЙ МАТЕРИ \"ЖИВОНОСНЫЙ ИСТОЧНИК\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Church of the Icon of the Theotokos \"Life-giving Spring\"",
      "id": "by-babruysk-40643db423",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм иконы Божией Матери \"Смоленская\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Church of the Icon of the Theotokos \"Smolensk\"",
      "id": "by-babruysk-ea46d52b6c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм иконы Божией Матери \"Спорительница хлебов\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Church of the Icon of the Theotokos \"Multiplier of Wheat\"",
      "id": "by-babruysk-b30fa94a21",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм иконы Божией Матери \"Неувядаемый Цвет\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Church of the Icon of the Theotokos \"Unfading Color\"",
      "id": "by-babruysk-3b85a52a60",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ИКОНЫ БОЖИЕЙ МАТЕРИ \"ЖИРОВИЦКОЙ\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Zhirovichi Icon of the Theotokos Church",
      "id": "by-babruysk-efb253788b",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм Рождества Христова",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/glusskiy-okrug-prihod/"
      ],
      "name": "Church of the Nativity",
      "id": "by-babruysk-c171e7fa23",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ РОЖДЕСТВА ХРИСТОВА",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Nativity of Christ Church",
      "id": "by-babruysk-044513193c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ РОЖДЕСТВА ИОАННА ПРЕДТЕЧИ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Nativity of Saint John the Baptist Church",
      "id": "by-babruysk-758efcf34b",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Храм Рождества Предтечи Господня Иоанна",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Church of the Nativity of the Baptist John",
      "id": "by-babruysk-f91e555d27",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ РОЖДЕСТВА ПРЕСВЯТОЙ БОГОРОДИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-babruysk-837156f10c",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ РОЖДЕСТВА ПРЕСВЯТОЙ БОГОРОДИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-babruysk-e255fca577",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ РОЖДЕСТВА БОГОРОДИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-babruysk-24f6d2a847",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ХРАМ ПОКРОВА ПРЕСВЯТОЙ БОГОРОДИЦЫ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-babruysk-80917a0c38",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Женский монастырь Святых Жен-Мироносиц",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://bobreparhiya.by/miro_monastery/"
      ],
      "name": "Convent of the Holy Myrrh-Bearing Women",
      "id": "by-babruysk-abb2ee5b73",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "КОСМО - ДАМИАНОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovs-hramy/"
      ],
      "name": "Holy Unmercenaries Cosmas and Damian Church",
      "id": "by-babruysk-45178003be",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "КРЕСТО - ВОЗДВИЖЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Exaltation of the Cross Church",
      "id": "by-babruysk-a6c16e2bd2",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ЕЛИЗАВЕТИНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Saint Elizabeth Church",
      "id": "by-babruysk-f1d54d6e58",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ГЕОРГИЕВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Great Martyr George the Victorious Church",
      "id": "by-babruysk-987c88cbc3",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ИЛЬИНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Prophet Elijah Church",
      "id": "by-babruysk-33bcea1d37",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "МИХАЙЛОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Archangel Michael Church",
      "id": "by-babruysk-c7cbc491ac",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "МИХАЙЛОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Archangel Michael Church",
      "id": "by-babruysk-c96c07bb9b",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Мужской монастырь в честь иконы Божией Матери \"Живоносный Источник\" (Прощанская пустынь)",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://bobreparhiya.by/mujskoi-monastur-proscha/"
      ],
      "name": "Monastery in honor of the Icon of the Theotokos \"Life-giving Spring\" (Proshchanskaya Hermitage)",
      "id": "by-babruysk-b5bec72423",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "НИКОЛО-СОФИЙСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Saint Nicholas and Saint Sophia Church",
      "id": "by-babruysk-a52f91a5f2",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "НИКОЛЬСКИЙ КАФЕДРАЛЬНЫЙ СОБОР",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Saint Nicholas Cathedral",
      "id": "by-babruysk-7460d76453",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "НИКОЛЬСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Saint Nicholas Church",
      "id": "by-babruysk-3e9c1296a1",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "НИКОЛЬСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/glusskiy-okrug-prihod/"
      ],
      "name": "Saint Nicholas Church",
      "id": "by-babruysk-5f4b145b1a",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Никольский ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovsk_klichev_okrug/"
      ],
      "name": "Saint Nicholas Church",
      "id": "by-babruysk-8de7de92e0",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "НИКОЛЬСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Saint Nicholas Church",
      "id": "by-babruysk-dfd1514305",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПАНТЕЛЕИМОНОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Great Martyr and Healer Panteleimon Church",
      "id": "by-babruysk-0d384b896f",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПАНТЕЛЕИМОНОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Great Martyr and Healer Panteleimon Church",
      "id": "by-babruysk-864acebc6d",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПЕТРО - ПАВЛОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-babruysk-437ddb7343",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПЕТРО-ПАВЛОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-babruysk-713542c544",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПЕТРО-ПАВЛОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/kirovsk_klichev_okrug/"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-babruysk-f0d6a029e1",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПОКРОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Protection of the Most Holy Theotokos Church",
      "id": "by-babruysk-b310fdfce9",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ПОКРОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bihov_prihod/"
      ],
      "name": "Protection of the Most Holy Theotokos Church",
      "id": "by-babruysk-cc53a743f8",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Молитвенный дом иконы Божией Матери \"Утоли моя печали\"",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Prayer House of the Icon of the Theotokos \"Quench my sorrows\"",
      "id": "by-babruysk-1c76072ae2",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "Молитвенный дом иконы Божией Матери \"Споручница грешных\"",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Prayer House of the Icon of the Theotokos \"Surety of Sinners\"",
      "id": "by-babruysk-15ae93ecf1",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "РИЗОПОЛОЖЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Deposition of the Robe of the Most Holy Theotokos Church",
      "id": "by-babruysk-00d3d146e4",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "СЕРАФИМОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruiskiy-rayon_prihod/"
      ],
      "name": "Seraphim Church",
      "id": "by-babruysk-864f06295f",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "СЕРАФИМОВСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Seraphim Church",
      "id": "by-babruysk-a81c46434a",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "СРЕТЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/bobruisk_prihod/"
      ],
      "name": "Meeting of the Lord Church",
      "id": "by-babruysk-37671a0afb",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "БОГОЯВЛЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/glusskiy-okrug-prihod/"
      ],
      "name": "Theophany Church",
      "id": "by-babruysk-c73e54f94b",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ТРОИЦКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/glusskiy-okrug-prihod/"
      ],
      "name": "Trinity Church",
      "id": "by-babruysk-394d660ead",
      "country": "BY"
    },
    {
      "parent": "ru-babruysk",
      "local": "ВВЕДЕНСКИЙ ХРАМ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://bobreparhiya.by/osipovichi_okrug/"
      ],
      "name": "Entry of the Most Holy Theotokos into the Temple Church",
      "id": "by-babruysk-fc5cc864bf",
      "country": "BY"
    }
  ],
  "ru-barysaw": [
    {
      "parent": "ru-barysaw",
      "local": "Кафедральный собор святого благоверного князя Александра Невского г. Марьина Горка",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Cathedral of the Holy Right-believing Prince Alexander Nevsky, Maryina Gorka",
      "id": "by-barysaw-56818c2c79",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Часовня-храм Воздвижения Креста Господня аг. Богушевичи",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Chapel-Church of the Exaltation of the Holy Cross agrotown of Bogushevichi",
      "id": "by-barysaw-76e5479f11",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм святителя Алексия митрополита Московского аг. Крайск",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of Saint Alexis, Metropolitan of Moscow agrotown of Kraisk",
      "id": "by-barysaw-6958644559",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм святого Архангела Михаила д. Дехань Смолевичского района.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Church of Saint Michael the Archangel in the village of Dekhan, Smolevichi district",
      "id": "by-barysaw-b4f6ed8e10",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Благовещения Пресвятой Богородицы д. Горно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos in the village of Gorno",
      "id": "by-barysaw-cad4b833d5",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-barysaw-11ee6416b3",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Успения Пресвятой Богородицы д. Сутоки Смолевичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Sutoki, Smolevichi district",
      "id": "by-barysaw-911a344920",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Введения во храм Пресвятой Богородицы д. Малые Бесяды",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Entry of the Most Holy Theotokos into the Temple Church in the village of Malye Besyady",
      "id": "by-barysaw-f36941b0f1",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Воздвижения Креста Господня д. Корень",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Exaltation of the Holy Cross in the village of Koren",
      "id": "by-barysaw-41311f0ea6",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм святого апостола Иоанна Богослова д. Большие Нестановичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Holy Apostle John the Theologian in the village of Bolshie Nestanovichi",
      "id": "by-barysaw-057f618301",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм святого благоверного князя Александра Невского д. Бабий Лес Смолевичского района.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Church of the Holy Right-believing Prince Alexander Nevsky in the village of Babiy Les, Smolevichi district",
      "id": "by-barysaw-1022cba75c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм святого равноапостольного князя Владимира д. Засовье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Holy Equal-to-the-Apostles Prince Vladimir, Zasovye village",
      "id": "by-barysaw-63bbe01262",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм святого святого великомученика Георгия Победоносца д. Совденевичи (приписной)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Great Martyr George the Victorious village of Sovdenevichi (attached)",
      "id": "by-barysaw-b7d8253902",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Покрова Пресвятой Богородицы д. Двиноса",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Dvinos",
      "id": "by-barysaw-487b858a11",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Покрова Пресвятой Богородицы д. Горавец",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Goravets",
      "id": "by-barysaw-7fe37338bc",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Казанской иконы Божией Матери д. Светлый Бор.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in the village of Svetly Bor",
      "id": "by-barysaw-67993eabda",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Рождества Пресвятой Богородицы д. Петровичи Смолевичского района.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in the village of Petrovichi, Smolevichi district",
      "id": "by-barysaw-0dbb0fce91",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Воскресения Христова д. Заречаны (приписной)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Church of the Resurrection of Christ in the village of Zarechany (attributed)",
      "id": "by-barysaw-03904454e4",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Преображения Господня аг. Ситники",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Church of the Transfiguration of the Lord agrotown of Sitniki",
      "id": "by-barysaw-5633735d0b",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Храм Преображения Господня д. Грицковичи Крупского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-krupskogo-blagochiniya"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Gritskovichi, Krupsky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-0f39d0fa23",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Женский монастырь в честь святой блаженной Ксении Петербургской в деревне Барань Борисовского района",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://borisoveparhia.by/ksenevskiy"
      ],
      "name": "Convent in honor of Blessed Xenia of Petersburg in the village of Baran, Borisov district",
      "id": "by-barysaw-a7bed75cb6",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Мужской монастырь в честь Благовещения Пресвятой Богородицы в деревне Малые Ляды Смолевичского района",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://borisoveparhia.by/blagoveshhenskiy"
      ],
      "name": "Monastery in honor of the Annunciation of the Most Holy Theotokos in the village of Malye Lyady, Smolevichi district",
      "id": "by-barysaw-6c4926e234",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма преподобной Евфросинии Полоцкой г.п. Руденск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of Venerable Euphrosyne of Polotsk Rudensk",
      "id": "by-barysaw-10f8897501",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого Архангела Михаила аг. Гайна",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel agrotown of Gaina",
      "id": "by-barysaw-e2ad557152",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого Архангела Михаила аг. Микуличи Березинского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel agrotown of Mikulichi, Berezinsky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-f0be3bc90d",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого Архангела Михаила д. Гребенка Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Grebenka, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-d38066ed35",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого Архангела Михаила в г. Жодино.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/zhodinskoe-blagochinie"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in Zhodino",
      "id": "by-barysaw-9cf1866085",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого Архангела Михаила пос. Правдинский",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel settlement of Pravdinsky",
      "id": "by-barysaw-69990d18d1",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца аг. Крайск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker agrotown of Kraisk",
      "id": "by-barysaw-f057f14289",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца аг. Октябрь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker agrotown of Oktyabr",
      "id": "by-barysaw-2c0b5427f6",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца г.п. Бобр Крупского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-krupskogo-blagochiniya"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in the urban settlement of Bobr, Krupki district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-7670f7e8f3",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца г. Логойска",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Logoisk",
      "id": "by-barysaw-de25bb5410",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца г. Смолевичи.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Smolevichi",
      "id": "by-barysaw-003beea9bc",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца в г. Березино Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the city of Berezino, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-a39e673222",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца в г. Червень Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the city of Cherven, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-c365c7a24f",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца в г. Крупки Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-krupskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the town of Krupki, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-078f50fd71",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца д. Пережир",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Perezhir",
      "id": "by-barysaw-96745c2829",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святителя Николая Чудотворца д. Турец Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Turets, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-7afaeb7db6",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святой праведной Анны д. Дудичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of Righteous Anna in Dudici",
      "id": "by-barysaw-3b6e6bb521",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма преподобного Саввы Освященного аг. Калачи.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of Venerable Savva the Sanctified agrotown of Kalachi",
      "id": "by-barysaw-d19309ee8c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма преподобного Серафима Саровского г.п. Свислочь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov Svislach",
      "id": "by-barysaw-71ca482aa2",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма преподобного Сергия Радонежского в г. Жодино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/zhodinskoe-blagochinie"
      ],
      "name": "Parish of the Church of Venerable Sergius of Radonezh in Zhodino",
      "id": "by-barysaw-81bc6cea4f",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Благовещения Пресвятой Богородицы аг. Слобода Пекалинского с/с Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Annunciation of the Most Holy Theotokos Church in the agrotown of Sloboda, Pekalin village council, Smolevichi district",
      "id": "by-barysaw-c5481735b5",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Вознесения Господня г. Смолевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in Smolevichi",
      "id": "by-barysaw-fe0b90fd5c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Успения Пресвятой Богородицы аг. Блужа",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos agrotown of Bluzha",
      "id": "by-barysaw-6e7aeca599",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Успения Пресвятой Богородицы д. Беларучи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Belaruchi",
      "id": "by-barysaw-326d84202e",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Успения Пресвятой Богородицы д. Косино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Kosino",
      "id": "by-barysaw-c8910ef885",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Успения Пресвятой Богородицы г.п. Холопеничи Крупского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-krupskogo-blagochiniya"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in the urban settlement of Kholopenichi, Krupki district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-b5c644c5d8",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Введения во храм Пресвятой Богородицы пос. Усяж Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Entry of the Most Holy Theotokos into the Temple Church in the settlement of Usyazh, Smolevichi district",
      "id": "by-barysaw-2f7477099c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Богоявления д. Веснино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Epiphany in the village of Vesnino",
      "id": "by-barysaw-d1ddfe602a",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Воздвижения Креста Господня д. Рованичи Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Rovanichi, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-e5acddada9",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма великомученика Георгия Победоносца д. Селецк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Seletsk",
      "id": "by-barysaw-692b5c103a",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого апостола Иоанна Богослова д. Кулики Червенского района",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the village of Kuliki, Chervensky district",
      "id": "by-barysaw-972844b2b6",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святых апостолов Петра и Павла д. Валевачи Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Valevachi, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-f038113273",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святых апостолов Петра и Павла г.п. Плещеницы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul Pleschenitsy",
      "id": "by-barysaw-1517992f16",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого великомученика Георгия Победоносца аг. Гостиловичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious agrotown of Gostilovichi",
      "id": "by-barysaw-099a76d380",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого великомученика Георгия Победоносца аг. Селиба Березинского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious agrotown of Seliba, Berezinsky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-be61b4fc8e",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого великомученика Георгия Победоносца аг. Заболотье Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious agrotown of Zabolotye, Smolevichi district",
      "id": "by-barysaw-6f26e57800",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого великомученика Георгия Победоносца д. Ведрица Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Vedritsa, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-af57c08476",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого великомученика Георгия Победоносца г.п. Смиловичи Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in the urban settlement of Smilovichi, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-e9d09180ce",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого священномученика Владимира Хираско аг. Погост",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Parish of the Hieromartyr Vladimir Hirasko Church in the agrotown of Pogost",
      "id": "by-barysaw-5d3cbc6e1d",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Святой Живоначальной Троицы аг. Блонь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity agrotown of Blon",
      "id": "by-barysaw-8b79be263c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Святой Живоначальной Троицы д. Швабы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Shvaby",
      "id": "by-barysaw-5958bbd9b9",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святой мученицы Татианы аг. Барсуки Смолевичского района",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Great Martyr Tatiana Church in the agrotown of Barsuki, Smolevichi district",
      "id": "by-barysaw-2915710923",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого пророка Илии аг. Дукора",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah agrotown of Dukora",
      "id": "by-barysaw-08f3fd4dca",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого пророка Илии аг. Шацк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah agrotown of Shatsk",
      "id": "by-barysaw-6679797199",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого пророка Илии д. Божино Березинского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Bozhino, Berezinsky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-4353d0a2db",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святого пророка Иоанна Предтечи д. Птичь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Holy Prophet John the Baptist in the village of Ptich",
      "id": "by-barysaw-19d04f146c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святых бессребреников Космы и Дамиана д. Клинок Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Holy Unmercenaries Cosmas and Damian in the village of Klinok, Chervensky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-8941e8b135",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма иконы Божией Матери \"Неопалимая Купина\" г.п. Зеленый Бор Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Burning Bush\" Zeleny Bor, Smolevichi district",
      "id": "by-barysaw-8b8061a3f3",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма иконы Божией Матери \"Избавительница\" в г. Жодино (Архиерейское подворье).",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/zhodinskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Deliverer\" in Zhodino (Bishops' Compound)",
      "id": "by-barysaw-72a0fb9f56",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих Радость\" д. Заполье Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Joy of All Who Sorrow\" in the village of Zapolye, Chervensky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-276b4b720a",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Покрова Пресвятой Богородицы аг. Ухвала Крупского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-krupskogo-blagochiniya"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in the agrotown of Ukhvala, Krupki district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-50d46e9f39",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Покрова Пресвятой Богородицы аг. Слобода Озерицко-Слободского с/с Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in the agrotown of Sloboda, Ozeritsko-Sloboda village council, Smolevichi district",
      "id": "by-barysaw-e67a2ee7b6",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Покрова Пресвятой Богородицы г. Логойска",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in Logoisk",
      "id": "by-barysaw-f5b007ba56",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Остров Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Ostrov, Smolevichi district",
      "id": "by-barysaw-5ae9a96f09",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Талька",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Talka",
      "id": "by-barysaw-c9cdcec0c4",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Казанской иконы Божией Матери д. Околово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos in the village of Okolovo",
      "id": "by-barysaw-6e9f478e80",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Минской иконы Божией Матери г. Смолевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Minsk Icon of the Theotokos in Smolevichi",
      "id": "by-barysaw-edda802cd2",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Христова аг. Алесино Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of Christ agrotown of Alesino, Smolevichi district",
      "id": "by-barysaw-ad0ed89240",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Христова п. Дружный",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Nativity of Christ in Druzhny",
      "id": "by-barysaw-502360d51d",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Христова д. Острошицы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of Christ in the village of Ostroshitsy",
      "id": "by-barysaw-5ac43dd77b",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Христова д. Задомля Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of Christ in the village of Zadomlya, Smolevichi district",
      "id": "by-barysaw-d9c033b43c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Иоанна Предтечи д. Избище",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of John the Baptist in the village of Izbishche",
      "id": "by-barysaw-0680d19f9e",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Пресвятой Богородицы аг.Худовцы Крупского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-krupskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos agrotown of Khudovtsy, Krupsky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-fd81d8747c",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Пресвятой Богородицы аг. Пуховичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos agrotown of Pukhovichi",
      "id": "by-barysaw-4c9f78e15b",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Пресвятой Богородицы аг. Сергеевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/pervoe-puhovichskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos agrotown of Sergeevichi",
      "id": "by-barysaw-2b637061fd",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Плиса Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Plisa, Smolevichi district",
      "id": "by-barysaw-9b9515d5e3",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Янушковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Yanushkovichi",
      "id": "by-barysaw-1b2707acc7",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Воскресения Христова д. Ляды Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Resurrection of Christ in the village of Lyady, Cherven district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-2e614a89e0",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Преображения Господня аг. Камено",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/khramy-i-logoyskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord agrotown of Kameno",
      "id": "by-barysaw-6c08dff6ed",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Преображения Господня в г. Березино Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-berezinskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the city of Berezino, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-918964223b",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Преображения Господня г. Жодино.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/zhodinskoe-blagochinie"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in Zhodino",
      "id": "by-barysaw-4bc7dd2f1e",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма святых бессребреников Космы и Дамиана аг. Драчково Смолевичского района.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-smolevichskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Unmercenary Saints Cosmas and Damian agrotown of Drachkovo, Smolevichi district",
      "id": "by-barysaw-1882179759",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Успения Пресвятой Богородицы д. Рудня Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Rudnya, Chervensky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-3beb4f98d0",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Иваничи Червенского р-на Борисовской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://borisoveparhia.by/hramyi-chervenskogo-blagochiniya"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Ivanichi, Chervensky district, Barysaw Diocese of the Belarusian Orthodox Church",
      "id": "by-barysaw-e995ae8b43",
      "country": "BY"
    },
    {
      "parent": "ru-barysaw",
      "local": "Женский Иоанно-Богословский монастырь в деревне Домашаны Смолевичского района",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://borisoveparhia.by/ioanno-bogoslovskiy"
      ],
      "name": "Saint John the Theologian Convent in Domashany, Smolevichi district",
      "id": "by-barysaw-b312b7efe3",
      "country": "BY"
    }
  ],
  "ru-minsk": [
    {
      "parent": "ru-minsk",
      "local": "Кафедральный собор Преображения Господня в городе Заславле",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-preobrazhenija-gospodnja-v-gorode-zaslavle/"
      ],
      "name": "Cathedral of the Transfiguration of the Lord in the city of Zaslavl",
      "id": "by-minsk-382615e3c9",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм в честь мучениц Веры, Надежды и Любови и матери их Софии в деревне Озерцо",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-v-chest-muchenic-very-nadezhdy-i-ljubovi-i-materi-ih-sofii/"
      ],
      "name": "Martyrs Faith, Hope, and Love and Their Mother Sophia Church in Ozertso",
      "id": "by-minsk-e6223998b8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм равноапостольной Марии Магдалины в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ravnoapostolnoj-marii-magdaliny-v-gorode-minske/"
      ],
      "name": "Church of Equal-to-the-Apostles Mary Magdalene in Minsk",
      "id": "by-minsk-09ca70b05f",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм равноапостольных Мефодия и Кирилла в городе Минске (при Представительстве Патриарха Московского и всея Руси в Белорусском Экзархате)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ravnoapostolnyh-mefodija-i-kirilla-v-gorode-minske/"
      ],
      "name": "Church of Equal-to-the-Apostles Methodius and Cyril in the city of Minsk (under the Representation of the Patriarch of Moscow and All Rus' in the Belarusian Exarchate)",
      "id": "by-minsk-4b092b0bd7",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм равноапостольного князя Владимира в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ravnoapostolnogo-knjazja-vladimira-v-gorode-minske/"
      ],
      "name": "Church of Equal-to-the-Apostles Prince Vladimir in Minsk",
      "id": "by-minsk-b93496b473",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм равноапостольной княгини Ольги в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ravnoapostolnoj-knjagini-olgi-v-gorode-minske/"
      ],
      "name": "Church of Equal-to-the-Apostles Princess Olga in Minsk",
      "id": "by-minsk-d27ce92142",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм праведного Иова Многострадального в городе Минске (Всехсвятского прихода)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-pravednogo-iova-mnogostradalnogo-v-gorode-minske/"
      ],
      "name": "Church of Righteous Job the Long-Suffering in the city of Minsk (All Saints Parish)",
      "id": "by-minsk-222f17974f",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм праведной Софии Слуцкой в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-pravednoj-sofii-sluckoj-v-gorode-minske/"
      ],
      "name": "Righteous Sophia of Slutsk Church in Minsk",
      "id": "by-minsk-b84b8b81f4",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм преподобных Кирилла и Марии Радонежских (прихода преподобного Сергия Радонежского) в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-prepodobnogo-sergija-radonezhskogo-v-gorode-minske/"
      ],
      "name": "Church of Venerable Cyril and Mary of Radonezh (Parish of Venerable Sergius of Radonezh) in the city of Minsk",
      "id": "by-minsk-523de32c53",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Димитрия Ростовского в поселке Михановичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-dimitrija-rostovskogo-v-poselke-mihanovichi/"
      ],
      "name": "Church of Saint Demetrius of Rostov in the village of Mikhanovichi",
      "id": "by-minsk-e2217b5b03",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святой равноапостольной Нины в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatoj-ravnoapostolnoj-niny-v-gorode-minske/"
      ],
      "name": "Church of Equal-to-the-Apostles Nina in Minsk",
      "id": "by-minsk-06536ee962",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм преподобного Иоанна Рыльского прихода праведного Иоанна Кронштадтского в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-pravednogo-ioanna-kronshtadtskogo-v-gorode-minske/"
      ],
      "name": "Church of Venerable John of Rila, Parish of Righteous John of Kronstadt in the city of Minsk",
      "id": "by-minsk-dce0b8c0e7",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Лаврентия Туровского в деревне Щомыслица",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/prihod-hrama-svjatitelja-lavrentija-turovskogo-v-derevne-shomyslica/"
      ],
      "name": "Church of Saint Lawrence of Turov in the village of Shchomyslitsa",
      "id": "by-minsk-3639e7c143",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Луки, архиепископа Крымского и Симферопольского в д. Лесковка Минского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-luki-arhiepiskopa-krymskogo-i-simferopolskogo-v-d-leskovka-minskogo-rajona/"
      ],
      "name": "Church of Saint Luke, Archbishop of Crimea and Simferopol in the village of Leskovka, Minsk district",
      "id": "by-minsk-207a25f6a7",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Луки, архиепископа Симферопольского, в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-luki-arhiepiskopa-simferopolskogo-v-gorode-minske/"
      ],
      "name": "Church of Saint Luke, Archbishop of Simferopol, in the city of Minsk",
      "id": "by-minsk-4c3115b7a1",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Николая Японского в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-nikolaja-japonskogo-v-gorode-minske/"
      ],
      "name": "Church of Saint Nicholas of Japan in Minsk",
      "id": "by-minsk-3a78c21a16",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Николая Чудотворца в городе Минске (микрорайон Шабаны)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-nikolaja-chudotvorca-v-gorode-minske-mikrorajon-shabany/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the city of Minsk (Shabany microdistrict)",
      "id": "by-minsk-e1ef163c81",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Николая Чудотворца в городе Минске (микрорайон Сокол)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-nikolaja-chudotvorca-v-gorode-minske-mikrorajon-sokol/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the city of Minsk (Sokol microdistrict)",
      "id": "by-minsk-2d1688457a",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Николая Чудотворца в поселке Привольный",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-nikolaja-chudotvorca-v-poselke-privolnyj/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Privolny",
      "id": "by-minsk-231752fa77",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Николая Чудотворца в д.Юхновка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-nikolaja-chudotvorca-v-djuhnovka/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Yukhnovka",
      "id": "by-minsk-afd25f54f7",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм преподобного Саввы Освященного в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-prepodobnogo-savvy-osvjashennogo-v-gorode-minske/"
      ],
      "name": "Church of Venerable Savva the Sanctified in the city of Minsk",
      "id": "by-minsk-79f15559e3",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм преподобного Серафима Саровского в деревне Замосточье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-prepodobnogo-serafima-sarovskogo-v-derevne-zamostoche/"
      ],
      "name": "Church of Venerable Seraphim of Sarov in the village of Zamostochye",
      "id": "by-minsk-91dea14591",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Спиридона Тримифунтского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-spiridona-trimifuntskogo/"
      ],
      "name": "Church of Saint Spyridon of Tremithus",
      "id": "by-minsk-29ae141402",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Спиридона Тримифунтского (прихода Рождества Христова) в агрогородке Колодищи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-rozhdestva-hristova-v-agrogorodke-kolodishi/"
      ],
      "name": "Church of Saint Spyridon of Tremithus (Parish of the Nativity of Christ) in the agrotown of Kolodishchi",
      "id": "by-minsk-c82e533704",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святителя Феодосия Черниговского в деревне Петришки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-feodosija-chernigovskogo-v-derevne-petrishki/"
      ],
      "name": "Church of Saint Theodosius of Chernigov in the village of Petrishki",
      "id": "by-minsk-45f2e65975",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Благовещения Пресвятой Богородицы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-blagoveshenija-presvjatoj-bogorodicy-v-gorode-minske/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos in Minsk",
      "id": "by-minsk-baf90a48e9",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Благовещения Пресвятой Богородицы в д. Копище",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-blagoveshenija-presvjatoj-bogorodicy-v-d-kopishe/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos in the village of Kopische",
      "id": "by-minsk-7e1008af19",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм апостола и евангелиста Иоанна Богослова при Минском суворовском училище",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-vo-imja-apostola-i-evangelista-ioanna-bogoslova-pri-minskom-suvorovskom-uchilishe/"
      ],
      "name": "Church of the Apostle and Evangelist John the Theologian at the Minsk Suvorov School",
      "id": "by-minsk-d99f4137f3",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм апостола Андрея Первозванного в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-apostola-andreja-pervozvannogo-v-gorode-minske/"
      ],
      "name": "Church of the Apostle Andrew the First-Called in Minsk",
      "id": "by-minsk-c1219ebf0c",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм апостолов Петра и Павла в деревне Ратомка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-apostolov-petra-i-pavla-v-derevne-ratomka/"
      ],
      "name": "Church of the Apostles Peter and Paul in the village of Ratomka",
      "id": "by-minsk-5ba6dccefc",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм апостолов Петра и Павла в деревне Сеница",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hrama-apostolov-petra-i-pavla-v-derevne-sennica/"
      ],
      "name": "Church of the Apostles Peter and Paul in the village of Senica",
      "id": "by-minsk-d0c890b50d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм апостолов Петра и Павла в деревне Жуковка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-apostolov-petra-i-pavla-v-derevne-zhukovka/"
      ],
      "name": "Church of the Apostles Peter and Paul in the village of Zhukovka",
      "id": "by-minsk-d26ffdad1e",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Архангела Михаила в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-arhangela-mihaila-v-gorode-minske/"
      ],
      "name": "Church of the Archangel Michael in Minsk",
      "id": "by-minsk-f63ddc34de",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм архистратига Михаила в деревне Новый Двор",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hrama-arhistratiga-mihaila-v-derevne-novyj-dvor/"
      ],
      "name": "Church of the Archangel Michael in the village of Novy Dvor",
      "id": "by-minsk-eecc243dec",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Вознесения Господня в агрогородке Колодищи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-voznesenija-gospodnja-v-agrogorodke-kolodishi/"
      ],
      "name": "Church of the Ascension of the Lord in the agrotown of Kolodishchi",
      "id": "by-minsk-52c4e42f6a",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Вознесения Господня в деревне Сёмково",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-voznesenija-gospodnja-v-derevne-semkovo/"
      ],
      "name": "Church of the Ascension of the Lord in the village of Syomkovo",
      "id": "by-minsk-f5c094f0ea",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Вознесения Господня в деревне Ждановичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-voznesenija-gospodnja-v-derevne-zhdanovichi/"
      ],
      "name": "Church of the Ascension of the Lord in the village of Zhdanovichi",
      "id": "by-minsk-fd9d8ca18f",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Успения Пресвятой Богородицы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-uspenija-presvjatoj-bogorodicy-v-gorode-minske/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in Minsk",
      "id": "by-minsk-bf64ceb1d6",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Успения Пресвятой Богородицы в деревне Крупица",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-uspenija-presvjatoj-bogorodicy-v-derevne-krupica/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Krupitsa",
      "id": "by-minsk-762080c1a4",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм младенца Гавриила Белостокского прихода Введения во храм Пресвятой Богородицы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-vvedenija-vo-hram-presvjatoj-bogorodicy-v-gorode-minske/"
      ],
      "name": "Infant Martyr Gabriel of Bialystok Church of the Entry of the Most Holy Theotokos into the Temple Parish in Minsk",
      "id": "by-minsk-6d97ec86e8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм благоверного князя Александра Невского в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-blagovernogo-knjazja-aleksandra-nevskogo-v-gorode-minske/"
      ],
      "name": "Church of the Right-believing Prince Alexander Nevsky in Minsk",
      "id": "by-minsk-3854b1c82d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Собора белорусских святых в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-sobora-belorusskih-svjatyh-v-gorode-minske/"
      ],
      "name": "Church of the Synaxis of the Belarusian Saints in Minsk",
      "id": "by-minsk-9f2dcaf97d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Собора святых земли Белорусской в городе Заславле",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hrama-sobora-svjatyh-zemli-belorusskoj-v-gorode-zaslavle/"
      ],
      "name": "Church of the Synaxis of the Saints of Belarus in the city of Zaslavl",
      "id": "by-minsk-de11718451",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Богоявления в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-bogojavlenija-v-gorode-minske/"
      ],
      "name": "Church of the Epiphany in Minsk",
      "id": "by-minsk-34629fe05d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Воздвижения Креста Господня в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-vozdvizhenija-kresta-gospodnja-v-gorode-minske/"
      ],
      "name": "Church of the Exaltation of the Holy Cross in Minsk",
      "id": "by-minsk-5b6cf2c0e3",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Воздвижения Креста Господня в деревне Королев Стан",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-vozdvizhenija-kresta-gospodnja-v-derevne-korolev-stan/"
      ],
      "name": "Church of the Exaltation of the Holy Cross in the village of Korolev Stan",
      "id": "by-minsk-136e03e351",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм великомученицы Анастасии Узорешительницы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-velikomuchenicy-anastasii-uzoreshitelnicy/"
      ],
      "name": "Church of the Great Martyr Anastasia the Deliverer from Bonds in Minsk",
      "id": "by-minsk-e351c4603f",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм великомученика и целителя Пантелеимона в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-velikomuchenika-i-celitelja-panteleimona-v-gorode-minske/"
      ],
      "name": "Church of the Great Martyr and Healer Panteleimon in Minsk",
      "id": "by-minsk-d381b12fe0",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм великомученика и целителя Пантелеимона в городском поселке Мачулищи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-velikomuchenika-i-celitelja-panteleimona-v-poselke-machulishi/"
      ],
      "name": "Church of the Great Martyr and Healer Panteleimon in the urban village of Machulishchi",
      "id": "by-minsk-7c68dfb03d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм великомученика Димитрия Солунского прихода Рождества Пресвятой Богородицы в деревне Старое Село",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-rozhdestva-presvjatoj-bogorodicy-v-derevne-staroe-selo/"
      ],
      "name": "Church of the Great Martyr Demetrius of Thessalonica Parish of the Nativity of the Most Holy Theotokos in the village of Staroe Selo",
      "id": "by-minsk-04a5ff8492",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Xрам священномученика Владимира Хираско в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/xram-svjashennomuchenika-vladimira-hirasko-v-gorode-minske/"
      ],
      "name": "Church of the Hieromartyr Vladimir Khirasko in the city of Minsk",
      "id": "by-minsk-270dd61388",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "храма святого великомученика и целителя Пантелеимона в г.п. Мачулищи Минского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-velikomuchenika-i-celitelja-panteleimona-v-poselke-machulishi"
      ],
      "name": "Church of the Great Martyr and Healer Panteleimon in the urban settlement of Machulishchi, Minsk district",
      "id": "by-minsk-2288f72dc0",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Святой Живоначальной Троицы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatoj-zhivonachalnoj-troicy-v-gorode-minske/"
      ],
      "name": "Church of the Holy Life-giving Trinity in Minsk",
      "id": "by-minsk-feddcf372c",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Святой Живоначальной Троицы в деревне Боровляны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatoj-zhivonachalnoj-troicy-v-derevne-borovljany/"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Borovlyany",
      "id": "by-minsk-c71115bd8d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Святой Живоначальной Троицы в деревне Хатежино",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatoj-zhivonachalnoj-troicy-v-derevne-hatezhino/"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Khatezhino",
      "id": "by-minsk-da9f640b96",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святого пророка Иоанна Предтечи в агрогородке Шершуны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatogo-proroka-ioanna-predtechi-v-agrogorodke-shershuny/"
      ],
      "name": "Church of the Holy Prophet John the Baptist in the agrotown of Shershuny",
      "id": "by-minsk-be0162e55c",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм святого праведного страстотерпца Евгения Боткина (прихода иконы Божией Матери \"Всецарица\")",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatogo-pravednogo-strastoterpca-evgenija-botkina-prihoda-ikony-bozhiej-materi-vsecarica/"
      ],
      "name": "Church of the Holy Righteous Passion-Bearer Evgeniy Botkin (Parish of the Icon of the Theotokos \"Queen of All\")",
      "id": "by-minsk-7495a203ef",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Святого Духа в поселке Гатово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatogo-duha-v-poselke-gatovo/"
      ],
      "name": "Church of the Holy Spirit in the village of Gatovo",
      "id": "by-minsk-1624a5e257",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Святого Духа в деревне Самохваловичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatogo-duha-v-derevne-samohvalovichi/"
      ],
      "name": "Church of the Holy Spirit in the village of Samokhvalovichi",
      "id": "by-minsk-7d3a27a7b2",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Святой Троицы в городе Минске (Всехсвятского прихода)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatoj-zhivonachalnoj-troicy-v-gorode-minske-vsehsvjatskogo-prihoda/"
      ],
      "name": "Church of the Holy Trinity in Minsk (All Saints Parish)",
      "id": "by-minsk-25c6f8dbbc",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Пресвятой Троицы в д. Пашковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-presvjatoj-troicy-v-d-pashkovichi/"
      ],
      "name": "Church of the Holy Trinity in the village of Pashkovichi",
      "id": "by-minsk-632cf5457f",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Отрада и Утешение\" в деревне Аксаковщина",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-otrada-i-uteshenie-v-derevne-aksakovshina/"
      ],
      "name": "Church of the Icon of the Theotokos \"Joy and Consolation\" in the village of Aksakovshchina",
      "id": "by-minsk-6bd45ccec7",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"В скорбех и печалех Утешение\" в деревне Малиновка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-v-skorbeh-i-pechaleh-uteshenie-v-derevne-malinovka/"
      ],
      "name": "Church of the Icon of the Theotokos \"Consolation in Sorrows and Griefs\" in the village of Malinovka",
      "id": "by-minsk-ae89936635",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Державная\" в городе Минске",
      "rank": "Church",
      "kind": "monastery",
      "sources": [
        "https://pravminsk.by/eparchiya/monastyri/hram-ikony-bozhiej-materi-derzhavnaja-v-gorode-minske/"
      ],
      "name": "Reigning Icon of the Theotokos Church in Minsk",
      "id": "by-minsk-1f02d5a6ac",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Донская\" в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-donskaja-v-gorode-minske/"
      ],
      "name": "Don Icon of the Theotokos Church in Minsk",
      "id": "by-minsk-3fb82a670a",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Неупиваемая Чаша\" в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-neupivaemaja-chasha-v-gorode-minske/"
      ],
      "name": "Church of the Icon of the Theotokos \"Inexhaustible Chalice\" in Minsk",
      "id": "by-minsk-f68ed430ca",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Всех скорбящих Радость\" в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-vseh-skorbjashih-radost-v-gorode-minske/"
      ],
      "name": "Church of the Icon of the Theotokos \"Joy of All Who Sorrow\" in Minsk",
      "id": "by-minsk-d994f7b69b",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Млекопитательница\" в деревне Раубичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-mlekopitatelnica-v-derevne-raubichi/"
      ],
      "name": "Church of the Icon of the Theotokos \"Nursing Mother\" in the village of Raubichi",
      "id": "by-minsk-f7423839b8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Взыскание погибших\" в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-vzyskanie-pogibshih-v-gorode-minske/"
      ],
      "name": "Church of the Icon of the Theotokos \"Seeking the Lost\" in the city of Minsk",
      "id": "by-minsk-2cc604b6d6",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Всецарица\" в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-vsecarica-v-gorode-minske/"
      ],
      "name": "Church of the Icon of the Theotokos \"Queen of All\" in the city of Minsk",
      "id": "by-minsk-b80b19efe7",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм иконы Божией Матери \"Жировичская\" деревни Прилесье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-ikony-bozhiej-materi-zhirovichskaja-derevni-prilese/"
      ],
      "name": "Zhirovichi Icon of the Theotokos Church in Prilesye",
      "id": "by-minsk-e5741ce6f1",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Покрова Пресвятой Богородицы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-pokrova-presvjatoj-bogorodicy-v-gorode-minske/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in Minsk",
      "id": "by-minsk-c687364e07",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Покрова Пресвятой Богородицы в деревне Чачково",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hrama-pokrova-presvjatoj-bogorodicy-v-derevne-chachkovo/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Chachkovo",
      "id": "by-minsk-73efa193b2",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Покрова Пресвятой Богородицы деревни Юзуфово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-pokrova-presvjatoj-bogorodicy-derevni-juzufovo/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Yuzufovo",
      "id": "by-minsk-2611254c27",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Казанской иконы Божией Матери в г. Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-kazanskoj-ikony-bozhiej-materi-v-g-minske/"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in Minsk",
      "id": "by-minsk-1414509775",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Купятицкой иконы Божией Матери (прихода Успения Пресвятой Богородицы) в агрогородке Колодищи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hrama-uspenija-presvjatoj-bogorodicy-v-agrogorodke-kolodishi/"
      ],
      "name": "Church of the Kupyatitskaya Icon of the Theotokos (Parish of the Dormition of the Most Holy Theotokos) in the agrotown of Kolodishchi",
      "id": "by-minsk-f9eaca2b4d",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм мученика Иоанна Воина в деревне Околица",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-muchenika-ioanna-voina-v-derevne-okolica/"
      ],
      "name": "Church of the Martyr John the Warrior in the village of Okolitsa",
      "id": "by-minsk-0003bcc279",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм мученицы Татианы в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-muchenicy-tatiany-v-gorode-minske/"
      ],
      "name": "Church of the Martyr Tatiana in Minsk",
      "id": "by-minsk-52d97004b9",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Минской иконы Божией Матери прихода великомученика Георгия Победоносца в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-velikomuchenika-georgija-pobedonosca-v-gorode-minske/"
      ],
      "name": "Church of the Minsk Icon of the Theotokos of the Parish of the Great Martyr George the Victorious in the city of Minsk",
      "id": "by-minsk-3e725a21a8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Рождества Христова в деревне Новоселье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-rozhdestva-hristova-v-derevne-novosele/"
      ],
      "name": "Church of the Nativity of Christ in the village of Novoselye",
      "id": "by-minsk-f1ae1a1430",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Рождества Иоанна Предтечи в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-rozhdestva-ioanna-predtechi-v-gorode-minske/"
      ],
      "name": "Church of the Nativity of John the Baptist in Minsk",
      "id": "by-minsk-02d3be0582",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Рождества Пресвятой Богородицы в деревне Сёмков Городок",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-rozhdestva-presvjatoj-bogorodicy-v-derevne-semkov-gorodok/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in the village of Syomkov Gorodok",
      "id": "by-minsk-f3e6a69da9",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Рождества Пресвятой Богородицы в деревне Тарасово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-rozhdestva-presvjatoj-bogorodicy-v-derevne-tarasovo/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in the village of Tarasovo",
      "id": "by-minsk-74c8c8c007",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Оптинских старцев в городе Минске (прихода храма Серафима Саровского)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-optinskih-starcev-v-gorode-minske/"
      ],
      "name": "Church of the Optina Elders in the city of Minsk (Parish of the Church of Seraphim of Sarov)",
      "id": "by-minsk-79ea641b07",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм пророка Илии в деревне Касынь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-proroka-ilii-v-derevne-kasyn/"
      ],
      "name": "Church of the Prophet Elijah in the village of Kasyn",
      "id": "by-minsk-edec442b85",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Воскресения Христова в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-voskresenija-hristova-v-gorode-minske/"
      ],
      "name": "Church of the Resurrection of Christ in Minsk",
      "id": "by-minsk-df863375b0",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм праведных Иоакима и Анны в деревне Вишневка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-pravednyh-ioakima-i-anny-v-derevne-vishnevka/"
      ],
      "name": "Church of the Righteous Joachim and Anna in the village of Vishnevka",
      "id": "by-minsk-0efb226652",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Преображения Господня в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-preobrazhenija-gospodnja-v-gorode-minske/"
      ],
      "name": "Church of the Transfiguration of the Lord in Minsk",
      "id": "by-minsk-3c504a2419",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Преображения Господня в деревне Большевик",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-preobrazhenija-gospodnja-v-derevne-bolshevik/"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Bolshevik",
      "id": "by-minsk-568337b6c1",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Преображения Господня в деревне Острошицкий Городок",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-preobrazhenija-gospodnja-v-derevne-ostroshickij-gorodok/"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Ostroshitsky Gorodok",
      "id": "by-minsk-a7b570a28b",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм преподобномученика Афанасия Брестского в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-prepodobnomuchenika-afanasija-brestskogo-v-gorode-minske/"
      ],
      "name": "Church of the Venerable Martyr Athanasius of Brest in the city of Minsk",
      "id": "by-minsk-fd0a826cb5",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Храм Владимирской иконы Божией Матери в городе Минске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-vladimirskoj-ikony-bozhiej-materi-v-gorode-minske/"
      ],
      "name": "Church of the Vladimir Icon of the Theotokos in Minsk",
      "id": "by-minsk-2534b7b5d8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Свято-Духов кафедральный собор города Минска",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/svjato-duhov-kafedralnyj-sobor-v-gorode-minske/"
      ],
      "name": "Holy Spirit Cathedral in Minsk",
      "id": "by-minsk-301a0532d8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Домовой храм в честь Собора Белорусских святых при Минском епархиальном управлении",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/domovoj-hram-v-chest-sobora-belorusskih-svjatyh-pri-minskom-eparhialnom-upravlenii/"
      ],
      "name": "House Church in honor of the Synaxis of the Belarusian Saints at the Minsk Diocesan Administration",
      "id": "by-minsk-f93c40f518",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Домовой храм святителя Кирилла Туровского Минской духовной академии",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-svjatitelja-kirilla-turovskogo-v-gorode-minske/"
      ],
      "name": "House Church of Saint Cyril of Turov of the Minsk Theological Academy",
      "id": "by-minsk-e3e72a6ff8",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Приход храма в честь Всех Святых в городе Минске",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/hram-v-chest-vseh-svjatyh-v-gorode-minske/"
      ],
      "name": "Parish of the Church in honor of All Saints in the city of Minsk",
      "id": "by-minsk-0f0b2cdcc5",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Приход храма Святителя Николая Чудотворца д. Городище Минского р-на",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/prihod-hrama-svjatitelja-nikolaja-chudotvorca-d-gorodishe-minskogo-r-na/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Gorodishche, Minsk district",
      "id": "by-minsk-26d741e681",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Приход храма святой великомученицы Варвары",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/prihod-hrama-svjatoj-velikomuchenicy-varvary/"
      ],
      "name": "Parish of the Church of the Great Martyr Barbara",
      "id": "by-minsk-73c3862945",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Приход храма Рождества Христова дер. Большое Стиклево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/prihod-hrama-rozhdestva-hristova-der-bolshoe-stiklevo/"
      ],
      "name": "Parish of the Church of the Nativity of Christ settlement of Bolshoye Stiklevo",
      "id": "by-minsk-b883628b3e",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Прилуки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/prihod-hrama-rozhdestva-presvjatoj-bogorodicy-d-priluki/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Pryluky",
      "id": "by-minsk-5cc8427c01",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Приход храма Сретения Господня в Минске",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/prihod-hrama-sretenija-gospodnja-v-minske/"
      ],
      "name": "Parish of the Church of the Presentation of the Lord in Minsk",
      "id": "by-minsk-50b11aeaff",
      "country": "BY"
    },
    {
      "parent": "ru-minsk",
      "local": "Петро-Павловский собор в городе Минске",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://pravminsk.by/eparchiya/hramy-i-monastyri/petro-pavlovskij-sobor-goroda-minska/"
      ],
      "name": "Peter and Paul Cathedral in Minsk",
      "id": "by-minsk-7516b88cde",
      "country": "BY"
    }
  ],
  "ru-vitebsk": [
    {
      "parent": "ru-vitebsk",
      "local": "Часовня в честь святой великомученицы Параскевы Пятницы д. Козаногово Шумилинского района",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8238.html"
      ],
      "name": "Chapel in honor of the Great Martyr Paraskeva in the village of Kozanogovo, Shumilinsky district",
      "id": "by-vitebsk-d3b5cb0dbc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Часовня в честь святого великомученика Феодора Стратилата п. Приозерный Шумилинского района",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8215.html"
      ],
      "name": "Chapel in honor of the Great Martyr Theodore Stratelates, Priozerny village, Shumilinsky district",
      "id": "by-vitebsk-b12eba2be5",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Часовня святого преподобного Сергия Радонежского д. Должа Витебского района",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/74635.html"
      ],
      "name": "Chapel of Venerable Sergius of Radonezh in the village of Dolzha, Vitebsk district",
      "id": "by-vitebsk-1e94725d7c",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Часовня великомученицы Параскевы Пятницы г.п. Копысь",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/33057.html"
      ],
      "name": "Chapel of the Great Martyr Paraskeva Kopys",
      "id": "by-vitebsk-d1104dd1e6",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм \"Собор белорусских святых\" аг. Славное Толочинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26024.html"
      ],
      "name": "Church \"Synaxis of the Belarusian Saints\" agrotown of Slavnoe, Tolochinsky district",
      "id": "by-vitebsk-91404bc1dc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм \"Собор Архангела Гавриила\" г. Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4127.html"
      ],
      "name": "Church \"Synaxis of the Archangel Gabriel\" in Vitebsk (House Church)",
      "id": "by-vitebsk-a7ab7c90ad",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм в честь святого преподобного Серафима Саровского г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4148.html"
      ],
      "name": "Church in honor of the Venerable Seraphim of Sarov, Vitebsk",
      "id": "by-vitebsk-69d3940590",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм всех святых г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2373.html"
      ],
      "name": "Church of All Saints in Vitebsk",
      "id": "by-vitebsk-ac4a68326c",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых равноапостольных Кирилла и Мефодия г. Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2389.html"
      ],
      "name": "Church of Equal-to-the-Apostles Cyril and Methodius in Vitebsk (House Church)",
      "id": "by-vitebsk-1d7d570349",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых равноапостольных Константина и Елены г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2398.html"
      ],
      "name": "Church of Saints Equal-to-the-Apostles Constantine and Helena in Vitebsk",
      "id": "by-vitebsk-1251fcd6e9",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых равноапостольных Петра и Павла д. Гили",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26192.html"
      ],
      "name": "Church of Saints Peter and Paul Equal-to-the-Apostles in Gili",
      "id": "by-vitebsk-aca2c32bff",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Алексия, Митрополита Московского, г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8767.html"
      ],
      "name": "Church of Saint Alexy, Metropolitan of Moscow, Orsha",
      "id": "by-vitebsk-80e1851c14",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Алексия, Митрополита Московского, г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4121.html"
      ],
      "name": "Church of Saint Alexy, Metropolitan of Moscow, Vitebsk",
      "id": "by-vitebsk-24a24d4e86",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого Архангела Михаила д. Кривое Село",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/16581.html"
      ],
      "name": "Church of Saint Archangel Michael, Krivoe Selo village",
      "id": "by-vitebsk-9d7cfbd0e3",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого Архангела Михаила г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8755.html"
      ],
      "name": "Church of Saint Archangel Michael, Orsha",
      "id": "by-vitebsk-60ab9a035e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого Архангела Михаила д. Щетники Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25799.html"
      ],
      "name": "Church of Saint Archangel Michael, Shchetniki village, Gorodok district",
      "id": "by-vitebsk-5b6225e129",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого Василия Блаженного с. Пальминка Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25782.html"
      ],
      "name": "Saint Basil the Blessed Church in Palminka, Gorodok district",
      "id": "by-vitebsk-5647443b13",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Василия Великого г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3950.html"
      ],
      "name": "Church of Saint Basil the Great, Vitebsk",
      "id": "by-vitebsk-ffe61ee382",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой блаженной Ксении Петербургской д. Слобода Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8193.html"
      ],
      "name": "Church of Blessed Xenia of Petersburg, Sloboda village, Vitebsk district",
      "id": "by-vitebsk-951657935f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой равноапостольной Елены д. Кировская Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4178.html"
      ],
      "name": "Equal-to-the-Apostles Helen Church in Kirovskaya, Vitebsk district",
      "id": "by-vitebsk-731cc08267",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм преподобного Леонида Усть-Недумского г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8759.html"
      ],
      "name": "Church of Venerable Leonid of Ust-Nedum, Orsha",
      "id": "by-vitebsk-56f8756c0d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм cвятителя Луки Войно-Ясенецкого г. Городка (молитвенная комната)",
      "rank": "Prayer Room",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4288.html"
      ],
      "name": "Saint Luke Voino-Yasenetsky Prayer Room in Gorodok",
      "id": "by-vitebsk-80cb47c903",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой равноапостольной Марии Магдалины д. Холомерье Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25796.html"
      ],
      "name": "Equal-to-the-Apostles Mary Magdalene Church in Kholomerie, Gorodok district",
      "id": "by-vitebsk-81b343fe4f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца д. Добригоры Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4198.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Dobrigory, Beshenkovichi district",
      "id": "by-vitebsk-2bae014f8e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм cвятителя Николая Чудотворца д. Межа",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25780.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Mezha",
      "id": "by-vitebsk-8d3dda03df",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца д. Вышедки Городокского района (молитвенная комната)",
      "rank": "Prayer Room",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4280.html"
      ],
      "name": "Saint Nicholas the Wonderworker Prayer Room in Vyshedki, Gorodok district",
      "id": "by-vitebsk-5fb81b5570",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм cвятителя Николая Чудотворца, аг. Велешковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27184.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, agrotown of Veleshkovichi",
      "id": "by-vitebsk-c7b71b3753",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святителя Николая Чудотворца г. Дубровно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26059.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Dubrovno",
      "id": "by-vitebsk-6db2fd0bbb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца г. п. Коханово Толочинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25997.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Kokhanovo village, Tolochinsky district",
      "id": "by-vitebsk-dc596076cf",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца д. Макаровщина Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8264.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Makarovshchina village, Lepel district",
      "id": "by-vitebsk-8c81d78306",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца г. Сенно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/23434.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Senno",
      "id": "by-vitebsk-f86ae2ab9d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца г. п. Шумилино",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8209.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Shumilino",
      "id": "by-vitebsk-6bf40edd45",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца д. Слободка Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4210.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Slobodka village, Beshenkovichi district",
      "id": "by-vitebsk-e5bfd07c5e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая Чудотворца д. Веречье Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25802.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Verechye village, Gorodok district",
      "id": "by-vitebsk-32ccaf2845",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Николая, архиепископа Мир Ликийского г. Новолукомля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/17608.html"
      ],
      "name": "Church of Saint Nicholas, Archbishop of Myra in Lycia, Novolukomlya",
      "id": "by-vitebsk-d96709623b",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Никиты, епископа Новгородского, д. Никитиха Шумилинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8232.html"
      ],
      "name": "Church of Saint Nikita, Bishop of Novgorod, village of Nikitikha, Shumilinsky district",
      "id": "by-vitebsk-90f510611e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм cвятой равноапостольной Ольги, великой княгини Российской (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8290.html"
      ],
      "name": "Church of Equal-to-the-Apostles Olga, Grand Duchess of Russia (House Church)",
      "id": "by-vitebsk-daf7955a97",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Сергия Радонежского аг. Тулово Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26441.html"
      ],
      "name": "Church of Venerable Sergius of Radonezh agrotown of Tulovo, Vitebsk district",
      "id": "by-vitebsk-3f45e49cae",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Сергия Радонежского д. Копти Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4180.html"
      ],
      "name": "Church of Venerable Sergius of Radonezh in the village of Kopti, Vitebsk district",
      "id": "by-vitebsk-0ffff51668",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Сергия Радонежского д. Лесковичи Шумилинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8236.html"
      ],
      "name": "Church of Venerable Sergius of Radonezh, Leskovichi village, Shumilinsky district",
      "id": "by-vitebsk-8e6c2ea6ee",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Сергия Радонежского д. Юрковщина Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8254.html"
      ],
      "name": "Church of Venerable Sergius of Radonezh, Yurkovshchina village, Lepel district",
      "id": "by-vitebsk-9812126da2",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм cвятителя Спиридона Тримифунтского Чудотворца аг. Мошканы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26561.html"
      ],
      "name": "Church of Saint Spyridon of Tremithus the Wonderworker agrotown of Moshkany",
      "id": "by-vitebsk-c372937d1f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Спиридона Тримифунтского Чудотворца д. Заречье Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4295.html"
      ],
      "name": "Saint Spyridon of Tremithus Church in Zarechye, Gorodok district",
      "id": "by-vitebsk-11f3bb6f82",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святителя Тихона Задонского г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3353.html"
      ],
      "name": "Church of Saint Tikhon of Zadonsk, Vitebsk",
      "id": "by-vitebsk-2a9d2d2263",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Благовещения Пресвятой Богородицы г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3318.html"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos in Vitebsk",
      "id": "by-vitebsk-9c3baf9678",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Вознесения Господня с. Кабище Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25807.html"
      ],
      "name": "Ascension of the Lord Church in Kabishche, Gorodok district",
      "id": "by-vitebsk-dcaa9805f8",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Вознесения Господня д. Хвощно Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25792.html"
      ],
      "name": "Church of the Ascension of the Lord in the village of Khvoshchno, Gorodok district",
      "id": "by-vitebsk-3d355f5e91",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Вознесения Господня д. Лужесно Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4161.html"
      ],
      "name": "Church of the Ascension of the Lord in the village of Luzhesno, Vitebsk district",
      "id": "by-vitebsk-c36690ae12",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Вознесения Господня д. Пышно Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8262.html"
      ],
      "name": "Church of the Ascension of the Lord in the village of Pyshno, Lepel district",
      "id": "by-vitebsk-2da45b242f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Вознесения Господня г. п. Лиозно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27347.html"
      ],
      "name": "Church of the Ascension of the Lord, Liozno",
      "id": "by-vitebsk-0a5022918e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Успения Пресвятой Богородицы аг. Обольцы Толочинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26012.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos agrotown of Oboltsy Tolochinsky district",
      "id": "by-vitebsk-de0ff26e67",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Успения Пресвятой Богородицы г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8203.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in Orsha",
      "id": "by-vitebsk-4cf06662be",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Успения Пресвятой Богородицы г. п. Езерище Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4293.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the town of Ezerishche, Gorodok district",
      "id": "by-vitebsk-ac9b1a4068",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Успения Пресвятой Богородицы д. Победа",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/16589.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Pobeda",
      "id": "by-vitebsk-ef25d5713d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Успения Пресвятой Богородицы г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2420.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in Vitebsk",
      "id": "by-vitebsk-c0cb2b1f70",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Введения во Храм Пресвятой Богородицы г. Толочина",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26031.html"
      ],
      "name": "Entry of the Most Holy Theotokos into the Temple Church in Tolochin",
      "id": "by-vitebsk-ab48376f28",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Богоявления г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3322.html"
      ],
      "name": "Church of the Epiphany in Vitebsk",
      "id": "by-vitebsk-8c84880bf4",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Воздвижения Креста Господня г. п. Лиозно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26074.html"
      ],
      "name": "Church of the Exaltation of the Holy Cross, Liozno",
      "id": "by-vitebsk-665d757354",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм священномученика Афанасия Брестского г. п. Шумилино",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8213.html"
      ],
      "name": "Church of the Hieromartyr Athanasius of Brest, Shumilino",
      "id": "by-vitebsk-7fe16b155b",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм священномученика Афанасия Брестского г.Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2363.html"
      ],
      "name": "Church of the Hieromartyr Athanasius of Brest, Vitebsk (House Church)",
      "id": "by-vitebsk-7abf7ac878",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм священномученика Власия д. Липовцы Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4183.html"
      ],
      "name": "Church of the Hieromartyr Blasius in the village of Lipovtsy, Vitebsk district",
      "id": "by-vitebsk-60ff8af680",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм священномученика Николая пресвитера Витебского д. Старое Село Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26096.html"
      ],
      "name": "Church of the Hieromartyr Nicholas the Presbyter of Vitebsk in the village of Staroye Selo, Vitebsk district",
      "id": "by-vitebsk-2f128a2242",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм священномученика Фаддея, архиепископа Тверского, г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4142.html"
      ],
      "name": "Church of the Hieromartyr Thaddeus, Archbishop of Tver, Vitebsk",
      "id": "by-vitebsk-06ddf13c85",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого апостола Андрея Первозванного г. Городка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4282.html"
      ],
      "name": "Church of the Holy Apostle Andrew the First-Called, Gorodok",
      "id": "by-vitebsk-93e74bebbb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого апостола Андрея Первозванного г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4123.html"
      ],
      "name": "Church of the Holy Apostle Andrew the First-Called, Vitebsk",
      "id": "by-vitebsk-f6bfe7fe17",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого апостола Луки г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3333.html"
      ],
      "name": "Church of the Holy Apostle Luke in Vitebsk",
      "id": "by-vitebsk-a2c901a9e2",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых апостолов Петра и Павла аг. Славени Толочинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26021.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul agrotown of Slaveni Tolochinsky district",
      "id": "by-vitebsk-b0618538a9",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых апостолов Петра и Павла в ИК-8 г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8250.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul in Ik-8, Orsha",
      "id": "by-vitebsk-dc047396fb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых апостолов Петра и Павла д. Браздетчино Оршанского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26104.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul in the village of Brazdetchino, Orsha district",
      "id": "by-vitebsk-69aaf67fcc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых апостолов Петра и Павла г. п. Богушевск Сенненского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26043.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul, Bogushevsk, Sennensky district",
      "id": "by-vitebsk-e627dac9b7",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых апостолов Петра и Павла г. п. Сураж Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4167.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul, Surazh, Vitebsk district",
      "id": "by-vitebsk-981aaee67f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых апостолов Петра и Павла д. Село Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25790.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul, village of Gorodok district",
      "id": "by-vitebsk-5a35e3001a",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого Архистратига Михаила и Небесных Сил Бесплотных г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4140.html"
      ],
      "name": "Church of the Holy Archangel Michael and the Ethereal Heavenly Powers, Vitebsk",
      "id": "by-vitebsk-7d22232c51",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святого Архангела Михаила д. Черея",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/17614.html"
      ],
      "name": "Church of the Holy Archangel Michael in the village of Cherey",
      "id": "by-vitebsk-33c194ea37",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого благоверного великого князя Димитрия Солунского г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4132.html"
      ],
      "name": "Church of the Holy Right-believing Grand Prince Demetrius of Thessalonica, Vitebsk",
      "id": "by-vitebsk-d78b28d92b",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой блаженной Матроны Московской г. Орши (молитвенная комната)",
      "rank": "Prayer Room",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8248.html"
      ],
      "name": "Blessed Matrona of Moscow Prayer Room in Orsha",
      "id": "by-vitebsk-0f2fd9eae9",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой блаженной Матроны Московской г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4146.html"
      ],
      "name": "Church of the Blessed Matrona of Moscow, Vitebsk",
      "id": "by-vitebsk-923d282554",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого благоверного князя Александра Невского аг. Крапивно Оршанского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26112.html"
      ],
      "name": "Church of the Holy Right-believing Prince Alexander Nevsky agrotown of Krapivno, Orsha district",
      "id": "by-vitebsk-06492d5804",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого благоверного князя Александра Невского д. Мартыново Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4200.html"
      ],
      "name": "Church of the Holy Right-believing Prince Alexander Nevsky, village of Martynovo, Beshenkovichi district",
      "id": "by-vitebsk-27f70bf464",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого благоверного князя Александра Невского г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3280.html"
      ],
      "name": "Church of the Holy Right-believing Prince Alexander Nevsky, Vitebsk",
      "id": "by-vitebsk-86b04f3100",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого благоверного князя Романа Рязанского г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3342.html"
      ],
      "name": "Church of the Holy Right-believing Prince Roman of Ryazan, Vitebsk",
      "id": "by-vitebsk-92ade659f8",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого равноапостольного князя Владимира г. Толочина",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/15706.html"
      ],
      "name": "Church of the Holy Equal-to-the-Apostles Prince Vladimir, Tolochin",
      "id": "by-vitebsk-9a1772af08",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой великомученицы Анастасии Узорешительницы г.Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2359.html"
      ],
      "name": "Church of the Great Martyr Anastasia the Deliverer from Bonds in Vitebsk (House Church)",
      "id": "by-vitebsk-5a52789356",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой великомученицы Варвары д. Черейщина Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8256.html"
      ],
      "name": "Church of the Great Martyr Barbara, village of Chereyshchina, Lepel district",
      "id": "by-vitebsk-6be78f3d4a",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой великомученицы Екатерины г. Витебска (домовой при Витебском Епархиальном управлении)Приход храма Святой великомученицы Екатерины г.Витебска Витебской епархии Белорусской Православной Церкви",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2378.html"
      ],
      "name": "Great Martyr Catherine House Church at the Vitebsk Diocesan Administration",
      "id": "by-vitebsk-0a220814e4",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученика Димитрия Солунского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/19284.html"
      ],
      "name": "Church of the Great Martyr Demetrius of Thessalonica",
      "id": "by-vitebsk-17794975e0",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученника Димитрия Солунского д. Прудок Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25785.html"
      ],
      "name": "Church of the Great Martyr Demetrius of Thessalonica, Prudok village, Gorodok district",
      "id": "by-vitebsk-76cabe061e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученика Георгия Победоносца г. Лепеля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8274.html"
      ],
      "name": "Church of the Great Martyr George the Victorious, Lepel",
      "id": "by-vitebsk-9c435874f3",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученика Георгия Победоносца д. Камень Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8280.html"
      ],
      "name": "Church of the Great Martyr George the Victorious, village of Kamen, Lepel district",
      "id": "by-vitebsk-483bbf6120",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученика Георгия Победоносца г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4129.html"
      ],
      "name": "Church of the Great Martyr George the Victorious, Vitebsk",
      "id": "by-vitebsk-38516c2ea5",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученника Целителя Пантелеимона д. Ремни Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/25788.html"
      ],
      "name": "Church of the Great Martyr and Healer Panteleimon in the village of Remni, Gorodok district",
      "id": "by-vitebsk-a86647c95e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого великомученика Целителя Пантелеимона п. Руба",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3338.html"
      ],
      "name": "Great Martyr and Healer Panteleimon Church in the settlement of Ruba",
      "id": "by-vitebsk-c38629c6c5",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой великомученицы Параскевы Пятницы г. Лепеля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8270.html"
      ],
      "name": "Church of the Great Martyr Paraskeva, Lepel",
      "id": "by-vitebsk-47f12da3f9",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой великомученицы Параскевы Пятницы г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2404.html"
      ],
      "name": "Church of the Great Martyr Paraskeva, Vitebsk",
      "id": "by-vitebsk-922c27f1bb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой великомученицы княгини Елисаветы г. Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2380.html"
      ],
      "name": "Church of the Great Martyr Princess Elizabeth, Vitebsk (House Church)",
      "id": "by-vitebsk-b12533e91d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы аг. Бабиничи Оршанского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26098.html"
      ],
      "name": "Church of the Holy Life-giving Trinity agrotown of Babinichi, Orsha district",
      "id": "by-vitebsk-e382a28384",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой Живоначальной Троицы аг. Островно Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4202.html"
      ],
      "name": "Church of the Holy Life-giving Trinity agrotown of Ostrovno Beshenkovichi district",
      "id": "by-vitebsk-2742572a9f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы аг. Улла Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4212.html"
      ],
      "name": "Church of the Holy Life-giving Trinity agrotown of Ulla Beshenkovichi district",
      "id": "by-vitebsk-9c1cad88cb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы г. Городка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4290.html"
      ],
      "name": "Church of the Holy Life-giving Trinity in Gorodok",
      "id": "by-vitebsk-e4c4ba01ce",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8191.html"
      ],
      "name": "Church of the Holy Life-giving Trinity in Orsha",
      "id": "by-vitebsk-b6de886a87",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы г. п. Яновичи Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4169.html"
      ],
      "name": "Church of the Holy Life-giving Trinity in the town of Yanovichi, Vitebsk district",
      "id": "by-vitebsk-6700bd33ae",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы д. Монастырь Толочинского района",
      "rank": "Church",
      "kind": "monastery",
      "sources": [
        "https://vitprav.by/26005.html"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Monastery, Tolochinsky district",
      "id": "by-vitebsk-06661a76bc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы д. Верховье Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4196.html"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Verkhovye, Beshenkovichi district",
      "id": "by-vitebsk-27349ca1b8",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы г. Дубровно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/28201.html"
      ],
      "name": "Church of the Holy Life-giving Trinity, Dubrovno",
      "id": "by-vitebsk-4e730c91ba",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святой Живоначальной Троицы г. п. Ореховск Оршанского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26116.html"
      ],
      "name": "Church of the Holy Life-giving Trinity, Orekhovsk, Orsha district",
      "id": "by-vitebsk-4bffd47ac6",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой преподобномученицы Евдокии п. Верховье Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3272.html"
      ],
      "name": "Church of the Venerable Martyr Evdokia, Verkhovye village, Vitebsk district",
      "id": "by-vitebsk-4180526ef9",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм священномученика Харалампия д. Новка Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4187.html"
      ],
      "name": "Hieromartyr Charalampus Church in Novka, Vitebsk district",
      "id": "by-vitebsk-350c0cb863",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой мученицы Ирины г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2386.html"
      ],
      "name": "Church of the Martyr Irina, Vitebsk",
      "id": "by-vitebsk-e5adf3e915",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого мученика Иоанна Воина д. Мазолово Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4163.html"
      ],
      "name": "Church of the Martyr John the Warrior in the village of Mazolovo, Vitebsk district",
      "id": "by-vitebsk-a3b64c449f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого мученика Лонгина Сотника г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3331.html"
      ],
      "name": "Church of the Martyr Longinus the Centurion, Vitebsk",
      "id": "by-vitebsk-3abcd1c199",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого мученика Меркурия Смоленского пос. Тарный",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4366.html"
      ],
      "name": "Church of the Martyr Mercury, Smolensk settlement of Tarny",
      "id": "by-vitebsk-acdb3dad96",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой мученицы Татианы г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4150.html"
      ],
      "name": "Church of the Martyr Tatiana in Vitebsk",
      "id": "by-vitebsk-4113622038",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых мучеников Бориса и Глеба д. Вымно Витебского района (молитвенная комната)",
      "rank": "Prayer Room",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4154.html"
      ],
      "name": "Holy Martyrs Boris and Gleb Prayer Room in Vymno, Vitebsk district",
      "id": "by-vitebsk-0e728a4e93",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых мучениц Веры, Надежды, Любови и матери их Софии д. Большие Лётцы Витебского района (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4171.html"
      ],
      "name": "Holy Martyrs Faith, Hope, and Love and Their Mother Sophia House Church in Bolshiye Lettsy, Vitebsk district",
      "id": "by-vitebsk-001c950a3c",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых преподобномученниц великой княгини Елисаветы и инокини Варвары г. Городка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4285.html"
      ],
      "name": "Church of the Holy Venerable Martyrs Grand Duchess Elizabeth and Nun Varvara in Gorodok",
      "id": "by-vitebsk-58867658bb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых преподобномучениц великой княгини Елисаветы и инокини Варвары г. Чашники",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8244.html"
      ],
      "name": "Church of the Holy Venerable Martyrs Grand Duchess Elizabeth and Nun Varvara, Chashniki",
      "id": "by-vitebsk-dd4edb42e8",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых мучеников благоверных князей Бориса и Глеба аг. Серковицы Толочинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26018.html"
      ],
      "name": "Holy Right-believing Princes and Passion-Bearers Boris and Gleb Church in the agrotown of Serkovitsy, Tolochin district",
      "id": "by-vitebsk-83c4f086c7",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых Жен-Мироносиц г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4134.html"
      ],
      "name": "Church of the Holy Myrrh-Bearing Women in Vitebsk",
      "id": "by-vitebsk-570ccd955e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Божия Даниила д. Замосточье Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4176.html"
      ],
      "name": "Church of the Holy Prophet Daniel in the village of Zamostochye, Vitebsk district",
      "id": "by-vitebsk-984e896361",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии д. Мишневичи Шумилинского района (молитвенный дом)",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8234.html"
      ],
      "name": "Prophet Elijah Prayer House in Mishnevichi, Shumilino district",
      "id": "by-vitebsk-1b6e233a63",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии д. Павловичи Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4204.html"
      ],
      "name": "Church of the Holy Prophet Elijah in the village of Pavlovichi, Beshenkovichi district",
      "id": "by-vitebsk-02dd364309",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии д. Заполье Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4159.html"
      ],
      "name": "Church of the Holy Prophet Elijah in the village of Zapolye, Vitebsk district",
      "id": "by-vitebsk-3c0041386d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии г. Витебска (воинская часть)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2384.html"
      ],
      "name": "Church of the Holy Prophet Elijah in Vitebsk (military unit)",
      "id": "by-vitebsk-12c58071af",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии г. п. Бешенковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4189.html"
      ],
      "name": "Church of the Holy Prophet Elijah, Beshenkovichi",
      "id": "by-vitebsk-12ee9b1eec",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8205.html"
      ],
      "name": "Church of the Holy Prophet Elijah, Orsha",
      "id": "by-vitebsk-a6b6131589",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого пророка Илии г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3329.html"
      ],
      "name": "Church of the Holy Prophet Elijah, Vitebsk",
      "id": "by-vitebsk-085bf69f96",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого праведного Иоанна Кормянского д. Малые Лётцы Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4185.html"
      ],
      "name": "Church of the Holy Righteous John of Kormyansky, Malye Lettsy village, Vitebsk district",
      "id": "by-vitebsk-a626dcc0d1",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого праведного Иоанна Кронштадтского в ИК-12 г. Орши (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8246.html"
      ],
      "name": "Church of the Holy Righteous John of Kronstadt in Ik-12 in Orsha (House Church)",
      "id": "by-vitebsk-8daf1c4612",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого праведного Иоанна Кронштадтского д. Краснолуки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/17612.html"
      ],
      "name": "Church of the Holy Righteous John of Kronstadt, Krasnoluki village",
      "id": "by-vitebsk-80637875a6",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого праведного Иоанна Русского п. Витьба Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2423.html"
      ],
      "name": "Church of the Holy Righteous John the Russian in Vitba, Vitebsk district",
      "id": "by-vitebsk-f9de7be859",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святого Духа аг. Ляды",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27150.html"
      ],
      "name": "Church of the Holy Spirit agrotown of Lyady",
      "id": "by-vitebsk-e286679374",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Святого Духа г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8199.html"
      ],
      "name": "Church of the Holy Spirit in Vitebsk",
      "id": "by-vitebsk-6963edca71",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святых бессребреников Космы и Дамиана д. Слобода Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8260.html"
      ],
      "name": "Church of the Holy Unmercenaries Cosmas and Damian in the village of Sloboda, Lepel district",
      "id": "by-vitebsk-0c4a8063b8",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Антония Римлянина, Новгородского чудотворца, г.Витебска (нижний храм прихода храма Воскресения Христова г.Витебска)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2361.html"
      ],
      "name": "Church of the Venerable Anthony the Roman, Novgorod Wonderworker, Vitebsk (lower Church of the Parish of the Church of the Resurrection of Christ in Vitebsk)",
      "id": "by-vitebsk-5e34e3cf9c",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святой преподобной Евфросинии Полоцкой г. Витебска (верхний храм)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3326.html"
      ],
      "name": "Upper Church of Venerable Euphrosyne of Polotsk in Vitebsk",
      "id": "by-vitebsk-1ba6a55448",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Иова Почаевского аг. Бабиничи Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/29736.html"
      ],
      "name": "Church of the Venerable Job of Pochaev agrotown of Babinichi, Vitebsk district",
      "id": "by-vitebsk-b7c3ae5fa4",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Иосифа Волоцкого чудотворца п. Заслоново Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8282.html"
      ],
      "name": "Church of the Venerable Joseph of Volotsk the Wonderworker in the village of Zaslonovo, Lepel district",
      "id": "by-vitebsk-2cd82c69a1",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Онуфрия Великого г. п. Оболь Шумилинского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8228.html"
      ],
      "name": "Church of the Venerable Onuphrius the Great, Obol, Shumilinsky district",
      "id": "by-vitebsk-2fbcf19a2b",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм святого преподобного Силуана Афонского г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3348.html"
      ],
      "name": "Church of the Venerable Silouan of Athos, Vitebsk",
      "id": "by-vitebsk-f029ec39dc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Воспитание\" учреждения Витебской епархии \"Православный оздоровительный лагерь \"Дружба\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27482.html"
      ],
      "name": "Upbringing Icon of the Theotokos Church at the Vitebsk Diocese Orthodox Health Camp Druzhba",
      "id": "by-vitebsk-da8a5651d1",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Фальковичская\" д. Вороны Витебского района (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4173.html"
      ],
      "name": "Falkovichi Icon of the Theotokos House Church in Vorony, Vitebsk district",
      "id": "by-vitebsk-12d544bbcb",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Целительница\" г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4144.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Healer\", Vitebsk",
      "id": "by-vitebsk-d046f05f84",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Неупиваемая Чаша\" п. Боровка Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8286.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Inexhaustible Chalice\", Borovka village, Lepel district",
      "id": "by-vitebsk-64b9504aad",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Неупиваемая Чаша\" п. Витьба Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27684.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Inexhaustible Chalice\", Vitba village, Vitebsk district",
      "id": "by-vitebsk-dd83c646d2",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Неупиваемая Чаша\" г. Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2400.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Inexhaustible Chalice\", Vitebsk (House Church)",
      "id": "by-vitebsk-ba5362bd42",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Иверская\" аг. Крынки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27176.html"
      ],
      "name": "Iveron Icon of the Theotokos Church in the agrotown of Krynki",
      "id": "by-vitebsk-d446867682",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Всех скорбящих Радость\" д. Берники (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8201.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Joy of All Who Sorrow\" in the village of Berniki (House Church)",
      "id": "by-vitebsk-c68c56c461",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Всех скорбящих Радость\" г. Витебска (молитвенная комната)",
      "rank": "Prayer Room",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2376.html"
      ],
      "name": "Joy of All Who Sorrow Icon of the Theotokos Prayer Room in Vitebsk",
      "id": "by-vitebsk-839168138d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Казанская\" д. Новосёлки (молитвенный дом)",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4165.html"
      ],
      "name": "Kazan Icon of the Theotokos Prayer House in Novoselki",
      "id": "by-vitebsk-f365483fd6",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Живоносный Источник\", д. Бабиновичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27181.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Life-giving Spring\", Babinovichi village",
      "id": "by-vitebsk-fdeada218c",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Минская\" д. Домжерицы Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8284.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Minsk\" in the village of Domzheritsy, Lepel district",
      "id": "by-vitebsk-b586528c7f",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Взыскание погибших\" г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3324.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Seeking of the Lost\", Vitebsk",
      "id": "by-vitebsk-0ddd5c96f5",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Спорительница хлебов\" д. Стаи Лепельского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8258.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Multiplier of Wheat\" in the village of Stai, Lepel district",
      "id": "by-vitebsk-547ab123d3",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Спорительница хлебов\", аг. Пушки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/27178.html"
      ],
      "name": "Church of the Icon of the Theotokos \"Multiplier of Wheat\", agrotown of Pushki",
      "id": "by-vitebsk-943bec8bf4",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Знамение\" г. Витебска Витебской епархии Белорусской Православной Церкви",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4136.html"
      ],
      "name": "Church of the Icon of the Theotokos \"The Sign\" in Vitebsk, Vitebsk Diocese of the Belarusian Orthodox Church",
      "id": "by-vitebsk-a1c6492e90",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Владимирская\" г. Лепеля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8276.html"
      ],
      "name": "Vladimir Icon of the Theotokos Church in Lepel",
      "id": "by-vitebsk-01289a4c47",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм иконы Божией Матери \"Всецарица\" г. Витебска (молитвенная комната)",
      "rank": "Prayer Room",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4125.html"
      ],
      "name": "Queen of All Icon of the Theotokos Prayer Room in Vitebsk",
      "id": "by-vitebsk-f3f9a6a749",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Покрова Пресвятой Богородицы д. Добромысли Лиозненского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26063.html"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Dobromysli, Liozno district",
      "id": "by-vitebsk-8c52ad4d90",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Покрова Пресвятой Богородицы г. Толочина",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8184.html"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos, Tolochin",
      "id": "by-vitebsk-9840e7bf41",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Казанской иконы Божией Матери д. Придвинье Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4206.html"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in the village of Pridvinye, Beshenkovichi district",
      "id": "by-vitebsk-8ad83c33b5",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Казанской иконы Божией Матери г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8197.html"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in Vitebsk",
      "id": "by-vitebsk-df166fecdc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Казанской иконы Божией Матери п. Яново Сенненского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26051.html"
      ],
      "name": "Church of the Kazan Icon of the Theotokos, Yanovo village, Sennen district",
      "id": "by-vitebsk-86caadfc5d",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Христова г. Лепеля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8266.html"
      ],
      "name": "Church of the Nativity of Christ in Lepel",
      "id": "by-vitebsk-886de674dc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Христова г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8252.html"
      ],
      "name": "Church of the Nativity of Christ in Orsha",
      "id": "by-vitebsk-dcf2d29a83",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Христова г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2413.html"
      ],
      "name": "Church of the Nativity of Christ in Vitebsk",
      "id": "by-vitebsk-2a13123baa",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Пресвятой Богородицы г. Орши",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4880.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in Orsha",
      "id": "by-vitebsk-db0519227b",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Пресвятой Богородицы д. Друцк",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/32194.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in the village of Drutsk",
      "id": "by-vitebsk-c2ffee80ea",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Пресвятой Богородицы д. Свеча Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4208.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in the village of Svecha, Beshenkovichi district",
      "id": "by-vitebsk-db8a5814a5",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Рождества Пресвятой Богородицы г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3340.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in Vitebsk",
      "id": "by-vitebsk-71823a5f41",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Воскресения Христова г. Витебска (верхний храм)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2367.html"
      ],
      "name": "Upper Church of the Resurrection of Christ in Vitebsk",
      "id": "by-vitebsk-50842bf2a0",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Смоленской иконы Божией Матери аг. Октябрьская Витебского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4152.html"
      ],
      "name": "Church of the Smolensk Icon of the Theotokos agrotown of Oktyabrskaya, Vitebsk district",
      "id": "by-vitebsk-ca6a3800f8",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм трех святителей г. Витебска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/3357.html"
      ],
      "name": "Church of the Three Saints in Vitebsk",
      "id": "by-vitebsk-e26e322714",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Преображения Господня г. Лепеля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8268.html"
      ],
      "name": "Church of the Transfiguration of the Lord in Lepel",
      "id": "by-vitebsk-77ff246b3e",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Преображения Господня д. Бочейково Бешенковичского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4194.html"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Bocheykovo, Beshenkovichi district",
      "id": "by-vitebsk-ed348e00a0",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Преображения Господня г. Витебска (нижний храм кафедрального собора )",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2410.html"
      ],
      "name": "Church of the Transfiguration of the Lord in Vitebsk (lower Church of the cathedral)",
      "id": "by-vitebsk-e54394e059",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Преображения Господня г. Барань Оршанского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8903.html"
      ],
      "name": "Church of the Transfiguration of the Lord, Baran, Orsha district",
      "id": "by-vitebsk-1ecd9e58c2",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Преображения Господня г. Чашники",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/8242.html"
      ],
      "name": "Church of the Transfiguration of the Lord, Chashniki",
      "id": "by-vitebsk-bbf2534bcc",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Преображения Господня г. п. Копысь Оршанского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/26108.html"
      ],
      "name": "Church of the Transfiguration of the Lord, Kopys, Orsha district",
      "id": "by-vitebsk-9c7356f0dd",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Владимирской иконы Божией Матери д. Вархи Городокского района",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/4278.html"
      ],
      "name": "Church of the Vladimir Icon of the Theotokos in the village of Varkhi, Gorodok district",
      "id": "by-vitebsk-4b3bf8a738",
      "country": "BY"
    },
    {
      "parent": "ru-vitebsk",
      "local": "Храм Жировицкой иконы Божией Матери г. Витебска (домовой храм)",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://vitprav.by/2382.html"
      ],
      "name": "Church of the Zhirovitsk Icon of the Theotokos in Vitebsk (House Church)",
      "id": "by-vitebsk-49e552f2aa",
      "country": "BY"
    }
  ],
  "ru-homel": [
    {
      "parent": "ru-homel",
      "local": "Приход храма в честь вмц. Веры, Надежды, Любови и матери их Софии, аг.Новая Жизнь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Martyrs Faith, Hope, and Love and Their Mother Sophia Church in the agrotown of Novaya Zhizn",
      "id": "by-homel-4cf5519ab3",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма в честь святого праведного Иоанна Кормянского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of Righteous John of Korma Church",
      "id": "by-homel-00fff34f8a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Успенский женский монастырь",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://eparhiya.by/uspenskij-zhenskij-monastyr/"
      ],
      "name": "Dormition Convent",
      "id": "by-homel-d2839eb47e",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Иоанно-Кормянский женский монастырь",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://eparhiya.by/ioanno-kormyanskij-zhenskij-monastyr/"
      ],
      "name": "Righteous John of Korma Convent",
      "id": "by-homel-067f023dca",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Никольский мужской монастырь",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://eparhiya.by/nikolskij-muzhskoj-monastyr/"
      ],
      "name": "Saint Nicholas Monastery",
      "id": "by-homel-5bdbe92f4c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храм \"Иверской\" иконы Божией Матери",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish Church of the Iveron Icon of the Theotokos",
      "id": "by-homel-edb2caaa57",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма в честь иконы Божией Матери Неупиваемая Чаша (ЛТП - 1) г.Светлогорск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Inexhaustible Chalice Icon of the Theotokos Church at LTP-1 in Svetlogorsk",
      "id": "by-homel-b4b7742af2",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Алексея Лельчицкого",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Alexei Lelchitsky",
      "id": "by-homel-836e3b5710",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Всех Святых, аг.Пиревичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of All Saints, Pirevichi",
      "id": "by-homel-57314d949a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма блаженной Ксении Петербуржской, п.Большевик",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Blessed Xenia of Petersburg, Bolshevik",
      "id": "by-homel-6a24cefd53",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма равноапостольного Николая архиепископа Японского в аг.Дуброва",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of Equal-to-the-Apostles Nicholas, Archbishop of Japan in Dubrova",
      "id": "by-homel-99a8b8b416",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого праведного Иоанна Кормянского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Righteous John of Kormyansk",
      "id": "by-homel-46185b9fe5",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобного Амфилохия Почаевского, аг.Вяжны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of Venerable Amphilochius of Pochaev, agrotown of Vyazhny",
      "id": "by-homel-6e7167d577",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма cвятого апостола Андрея Первозванного",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Andrew the First-Called Apostle",
      "id": "by-homel-763d0a99d4",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Василия Великого аг.Залесье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Basil the Great, Zalesie",
      "id": "by-homel-dafd58d828",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Василия Великого, г. Жлобин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of Saint Basil the Great, Zhlobin",
      "id": "by-homel-79ffae9696",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма св. блгв. кн. Александра Невского, аг.Холмеч",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Holy Right-believing Prince Alexander Nevsky, Kholmech",
      "id": "by-homel-0cc5c102b1",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Кирилла Туровского, г.Светлогорск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of Saint Cyril of Turov, Svetlogorsk",
      "id": "by-homel-29e130cb30",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобной Евфросинии Полоцкой, д.Озерщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Venerable Euphrosyne of Polotsk, village of Ozershchina",
      "id": "by-homel-74dc1dbfe6",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма св. благ. князя Александра Невского д. Нивки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Holy Right-believing Prince Alexander Nevsky Church in Nivki",
      "id": "by-homel-b2a4030c4e",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма св. великомученика Георгия Победоносца, аг.Лукский",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of Great Martyr George the Victorious, agrotown of Luksky",
      "id": "by-homel-a887367124",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Иоасафа Белгородского д. Казацкие Болсуны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Joasaph of Belgorod, Cossack Bolsuny village",
      "id": "by-homel-dd8b963cfc",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобного Иова Почаевского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Venerable Job of Pochaev",
      "id": "by-homel-3a62f2198e",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Луки (Войно-Ясенецкого), г.Речица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Luke (Voino-Yasenetsky), Rechitsa",
      "id": "by-homel-2ce7d16b31",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Луки Крымского и Апостола и Евангелиста Луки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Luke of Crimea and Apostle and Evangelist Luke",
      "id": "by-homel-3dacd7148d",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобной Манефы Гомельской, д.Севруки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Venerable Manefa of Gomel, Sevruki village",
      "id": "by-homel-e16005efc3",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого Архангела Михаила",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel",
      "id": "by-homel-579c9f87af",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого Архангела Михаила аг. Борщовка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel agrotown of Borschovka",
      "id": "by-homel-ebd0b27b7e",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого Архангела Михаила, аг.Ровенская Слобода",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel, Rivne Sloboda",
      "id": "by-homel-c0150779e6",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого Архангела Михаила, аг.Широкое",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel, Shirokoe",
      "id": "by-homel-50014f9adb",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого Архангела Михаила, аг.Папоротное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel, the village of Fern",
      "id": "by-homel-31d20fe3c1",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святого Архангела Михаила, д.Хальч",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel, village of Khalch",
      "id": "by-homel-ac5b7844f0",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца аг.Коротковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Korotkovichi",
      "id": "by-homel-b2d92896fb",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая чудотворца в г.п. Корма",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the town of Stern",
      "id": "by-homel-17f62588a1",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг.Бобовичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, agrotown of Bobovichi",
      "id": "by-homel-0c74683232",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг. Даниловичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, agrotown of Danilovichi",
      "id": "by-homel-9d81637f31",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг. Поповка (Ленино)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, agrotown of Popovka (Lenino)",
      "id": "by-homel-b01c584979",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д.Бронное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Bronnoye",
      "id": "by-homel-7117b1d71c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, г.Буда-Кошелево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Buda-Koshelevo",
      "id": "by-homel-58a6678f15",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, г.Добруш",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Dobrush",
      "id": "by-homel-698f80cbab",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, г. Гомель",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Gomel",
      "id": "by-homel-29831f3519",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д.Ивольск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Ivolsk",
      "id": "by-homel-027113d8cf",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг.Неглюбка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Neglyubka",
      "id": "by-homel-e835f9a1f8",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг.Полесье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Polesie",
      "id": "by-homel-270b1687ff",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг.Рогинь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Roginj",
      "id": "by-homel-b92488f50e",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д.Романовичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Romanovichi village",
      "id": "by-homel-de640a82b9",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д. Ст.Белица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Saint Belitsa",
      "id": "by-homel-4965b1a13a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д.Староселье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Staroselye village",
      "id": "by-homel-bb6c514d84",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг.Столбун",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Stolbun",
      "id": "by-homel-0de7c94f0b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д. Усохская Буда",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Usokhskaya Buda",
      "id": "by-homel-76e388a0d9",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, аг.Уть",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Ut",
      "id": "by-homel-cb0c035d5b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, г. Васильевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Vasilievichi",
      "id": "by-homel-0e41ee3f56",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Николая Чудотворца, д.Старый Кривск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, village of Stary Krivsk",
      "id": "by-homel-c2d2e6846b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святителя Николая Чудотворца, д.Якимова Слобода",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Yakimova Sloboda",
      "id": "by-homel-d0b0a47e76",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святителя Николая Чудотворца, д.Железники",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Zhelezniki village",
      "id": "by-homel-e0183d61b2",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобного Никиты исповедника, аг.Поколюбичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Venerable Nikita the Confessor, agrotown of Pokolyubichi",
      "id": "by-homel-433478eb7c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма св. Царственных страст. и всех новмч. и исп. Российских, аг.Заходы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Royal passions. and all new martyrs. and Spanish Russian, agrotown of Zakhody",
      "id": "by-homel-6bdc95a2af",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобного Серафима Саровского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov",
      "id": "by-homel-dc23e1ebae",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобного Серафима Саровского, г. Жлобин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov, Zhlobin",
      "id": "by-homel-3c9b721927",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма преподобного Сергия Радонежского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Venerable Sergius of Radonezh",
      "id": "by-homel-e16a7bdf38",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святителя Феодосия Черниговского, д.Новая Буда",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Theodosius of Chernigov, Novaya Buda village",
      "id": "by-homel-6123ff4847",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святителя Тихона Задонского аг.Иваки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of Saint Tikhon of Zadonsk in Ivaki",
      "id": "by-homel-1ad1721c83",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Архистратига Михаила (Костюковка)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Archangel Michael (Kostyukovka)",
      "id": "by-homel-1808fdb250",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Архангела Михаила, г.п.Тереховка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Archangel Michael, Terekhovka",
      "id": "by-homel-c91fa11c5a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Архангела Михаила, аг.Тихиничи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Archangel Michael, Tikhinichi",
      "id": "by-homel-791bed58be",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Вознесения Господня д.Рудня Маримонова",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Rudnya Marimonova",
      "id": "by-homel-6a0d96f543",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Вознесения Господня, д.Грабовка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord, Grabovka village",
      "id": "by-homel-770cd0decb",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Вознесения Господня, аг.Новая Гута",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord, Novaya Guta",
      "id": "by-homel-610a1c25b5",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы аг.Городец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in Gorodets",
      "id": "by-homel-298e161860",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы в г.Рогачеве",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in Rogachev",
      "id": "by-homel-7d8f110361",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы д.Песочная Буда",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Pesochnaya Buda",
      "id": "by-homel-bff18a1da7",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы, аг. Жгунь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos, agrotown of Zhgun",
      "id": "by-homel-5078a77517",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы, аг.Черетянка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos, Cheretyanka",
      "id": "by-homel-d6d28fa742",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы, аг.Красное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos, Krasnoye",
      "id": "by-homel-5085855f8f",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы, д.Новый Барсук",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos, Novy Barsuk village",
      "id": "by-homel-c8ccf367fb",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Успения Пресвятой Богородицы, д.Узнаж",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos, Uznazh village",
      "id": "by-homel-ec832cb8eb",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Введения во храм Пресвятой Богородицы, д.Дубровка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Entry of the Most Holy Theotokos into the Temple Church, Dubrovka",
      "id": "by-homel-f8689baf83",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Введения во храм Пресвятой Богородицы, г.п. Цагельня",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Entry of the Most Holy Theotokos into the Temple Church in the urban settlement of Tsagelnya",
      "id": "by-homel-9c705f613a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Богоявления, аг.Короватичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Epiphany, Korovatichi",
      "id": "by-homel-94e0e48804",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма \"Грузинской\" иконы Божией Матери",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Georgian Icon of the Theotokos",
      "id": "by-homel-ac03107657",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма священномученика Пиония в д. Уза",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Hieromartyr Pionius in the village of Uza",
      "id": "by-homel-71b038d373",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого апостола Иоанна Богослова, д.Березки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian, Berezki village",
      "id": "by-homel-e0cafcfa0c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого апостола Иоанна Богослова, д.Ямполь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian, Yampol village",
      "id": "by-homel-96eadf97a5",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святых апостолов Петра и Павла д.Перелевка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Perelevka",
      "id": "by-homel-881c87afb6",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святых апостолов Петра и Павла, аг.Поболово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul, agrotown of Pobolovo",
      "id": "by-homel-336196c35c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святых апостолов Петра и Павла, г.Светлогорск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul, Svetlogorsk",
      "id": "by-homel-1874513003",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого благоверного князя Александра Невского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky",
      "id": "by-homel-45c112158c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого благоверного князя Александра Невского, г.Рогачев",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky, Rogachev",
      "id": "by-homel-2c7273a2dd",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого благоверного князя Олега Брянского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Oleg Bryansky",
      "id": "by-homel-6472aac82b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого равноапостольного князя Владимира, г.п.Заречье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Prince Vladimir, Zarechye",
      "id": "by-homel-283487ff23",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого великомученика и целителя Пантелеимона",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon",
      "id": "by-homel-8b74f92886",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святой великомученицы Варвары, аг.Боровики",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of the Great Martyr Barbara, Boroviki",
      "id": "by-homel-b110a54b4c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святой великомученицы Екатерины, д. Гадичево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Great Martyr Catherine, Gadichevo village",
      "id": "by-homel-67622268b3",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого великомученика Георгия Победоносца",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious",
      "id": "by-homel-0e0779d80c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого великомученика Георгия Победоносца, г.п.Красный Берег",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious, Krasny Bereg",
      "id": "by-homel-bc69336162",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого великомученика Георгия Победоносца, аг.Белое Болото",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious, White Swamp",
      "id": "by-homel-00909f5d2f",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святой Живоначальной Троицы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity",
      "id": "by-homel-f2d0d7f192",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святой Живоначальной Троицы в аг.Крупец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Krupets",
      "id": "by-homel-7f12ffcaf7",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святой Живоначальной Троицы, д.Недойка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity, Nedoika village",
      "id": "by-homel-5e1384148b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святой Живоначальной Троицы, д.Шарпиловка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity, Sharpilovka village",
      "id": "by-homel-baa317979a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святой Живоначальной Троицы, аг.Заспа",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity, Zaspa",
      "id": "by-homel-ca328e7837",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святой Живоначальной Троицы, г. Жлобин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity, Zhlobin",
      "id": "by-homel-ad48fb58df",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святого мученика Иоанна Воина, г. Жлобин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of the Martyr John the Warrior, Zhlobin",
      "id": "by-homel-4a884aa071",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святой мученицы Татианы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Martyr Tatiana",
      "id": "by-homel-d417250795",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святой мироносицы равноапостольной Марии Магдалины, гп.Паричи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of the Holy Myrrh-Bearer Mary Magdalene, Equal-to-the-Apostles, Parichi",
      "id": "by-homel-63eded8de5",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма святых благоверных князей Петра и Февронии Муромских",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Holy Right-believing Prince Peter and Princess Fevronia of Murom Church",
      "id": "by-homel-6e51a353bd",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святого Духа д.Кравцовка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Holy Spirit in the village of Kravtsovka",
      "id": "by-homel-76c7207170",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святого Духа, аг.Дворец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Holy Spirit, agrotown of Palace",
      "id": "by-homel-c2d8996f39",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Святых Двенадцати Апостолов, аг.Чирковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of the Holy Twelve Apostles, Chirkovichi",
      "id": "by-homel-347f4b8bbd",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма иконы Божией Матери \"Достойно есть\", аг.Яново",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"It Is Truly Meet\", agrotown of Yanovo",
      "id": "by-homel-2744c1a90c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих Радость\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Joy of All Who Sorrow\"",
      "id": "by-homel-c61c5f3c18",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих радость\", д.Лопатино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Joy of All Who Sorrow\", Lopatino village",
      "id": "by-homel-fe963f99fa",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих Радость\", д.Тереничи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Joy of All Who Sorrow\", Terenichi village",
      "id": "by-homel-05958fadb1",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма иконы Божией Матери \"Скоропослушница\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the She Who Is Quick to Hear Icon of the Theotokos Church",
      "id": "by-homel-921bdbea61",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма иконы Божией Матери \"Юровичская-Милосердная\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Yurovichi Merciful Icon of the Theotokos Church",
      "id": "by-homel-90e7d9bccf",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Бабичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, agrotown of Babichi",
      "id": "by-homel-1703e1a9d2",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Еремино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, agrotown of Eremino",
      "id": "by-homel-92e6f73dab",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг. Защебье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, agrotown of Zashchebe",
      "id": "by-homel-3ae614ba2a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Болотня",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Bolotnya",
      "id": "by-homel-a0553aeb48",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Ботвиново",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Botvinovo",
      "id": "by-homel-465347bd58",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, д.Долголесье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Dolgolesye village",
      "id": "by-homel-5dc548991f",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, г.п.Довск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Dovsk",
      "id": "by-homel-ccf89dc7c8",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Глазовка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Glazovka",
      "id": "by-homel-4f2c37cf44",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, д.Головинцы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Golovintsy village",
      "id": "by-homel-fbfd84f56d",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Кирово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Kirovo",
      "id": "by-homel-38612ab3dd",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, аг.Коммунар",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Kommunar",
      "id": "by-homel-a8ef8ad0f4",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, г.Речица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Rechitsa",
      "id": "by-homel-157a96cc0c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, г.п.Стрешин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Streshin",
      "id": "by-homel-e618060ecd",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Покрова Пресвятой Богородицы, деревня Телеши",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Teleshi village",
      "id": "by-homel-72d82aa946",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Казанской иконы Божией Матери аг.Лучин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos agrotown of Luchin",
      "id": "by-homel-86abd48dc3",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Казанской иконы Божией Матери, н.п.Мичуринская",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos, Michurinskaya settlement",
      "id": "by-homel-32da279a70",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Казанской иконы Божией Матери, д.Милоград",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos, Milograd village",
      "id": "by-homel-0be96b0b55",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Казанской иконы Божией Матери, аг.Октябрь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos, Oktyabr",
      "id": "by-homel-96ff4a58e3",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы аг.Прибытки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in Pribytki",
      "id": "by-homel-80fd109421",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы аг.Терешковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in Tereshkovichi",
      "id": "by-homel-9a1dd206bf",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, д.Чеботовичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Chebotovichi",
      "id": "by-homel-713029af7b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, д.Глыбоцкое",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Glybotskoe village",
      "id": "by-homel-77d607417f",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, аг.Губичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Gubichi",
      "id": "by-homel-96e7aadb86",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, д.Козье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Kozye village",
      "id": "by-homel-d9c3137508",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, аг.Красный Партизан",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://dobrush-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Krasny Partizan",
      "id": "by-homel-a82a35f47a",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, д.Солоное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://zhlobin-deanery.cerkov.ru/blagochinie1/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Solonoe village",
      "id": "by-homel-ddf482fdab",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы г.п.Урицкое",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Uritskoye",
      "id": "by-homel-1db78477f9",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Рождества Пресвятой Богородицы, г.п.Уваровичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://byda-koshelev.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos, Uvarovichi",
      "id": "by-homel-c83afe6077",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Почаевской иконы Божией Матери, д.Борщевка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Pochaev Icon of the Theotokos, Borshchevka village",
      "id": "by-homel-8d3bddab38",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма пророка Илии аг.Журавичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rogachev-deanery.cerkov.ru/blagochinie-2/"
      ],
      "name": "Parish of the Church of the Prophet Elijah agrotown of Zhuravichi",
      "id": "by-homel-a670c92cab",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Скитковской иконы Божией Матери",
      "rank": "Parish",
      "kind": "monastery",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Skitkovo Icon of the Theotokos",
      "id": "by-homel-dc05014a76",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Смоленской иконы Божией Матери, с.Терюха",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Smolensk Icon of the Theotokos, Teryukha village",
      "id": "by-homel-7b243fcdae",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Тихвинской иконы Божией Матери, н.п.Ченки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://rai-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Tikhvin Icon of the Theotokos, Chenki",
      "id": "by-homel-ebe339cd10",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Преображения Господня",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://gomel-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord",
      "id": "by-homel-05c06ffe1c",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Преображения Господня, г.Чечерск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord, Chechersk",
      "id": "by-homel-33f7fcee93",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Преображения Господня, г.Светлогорск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://svetlogorsk.cerkov.ru/o-blagochinii-2/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord, Svetlogorsk",
      "id": "by-homel-81bef05e26",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход храма Преображения Господня, г. Ветка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://checherskoe.cerkov.ru/blagochinie/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord, Vetka",
      "id": "by-homel-65d0fc1946",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Приход Свято-Успенского собора, г.Речица",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://rechica.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Holy Dormition Cathedral, Rechitsa",
      "id": "by-homel-beb8295317",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Религиозная организация \"Религиозная община \"Приход храма преподобной Евфросинии Полоцкой аг.Малиновка Лоевского района Гомельской епархии Белорусской Православной Церкви\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://loev-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of Venerable Euphrosyne of Polotsk Church in Malinovka, Loyew district, Homel Diocese of the Belarusian Orthodox Church",
      "id": "by-homel-da5690109b",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Религиозная организация \"Религиозная община \"Приход храма Святой Живоначальной Троицы г.п.Лоев Гомельской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://loev-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Holy Life-giving Trinity Church in the urban settlement of Loyew, Homel Diocese of the Belarusian Orthodox Church",
      "id": "by-homel-703ed8b7ec",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Религиозная организация \"Религиозная община \"Приход храма иконы Божией Матери \"Всех скорбящих Радость\" д.Бывальки Лоевского района Гомельской епархии Белорусской Православной Церкви\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://loev-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Joy of All Who Sorrow Icon of the Theotokos Church in Byvalki, Loyew district, Homel Diocese of the Belarusian Orthodox Church",
      "id": "by-homel-2307c44466",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Религиозная организация \"Религиозная община \"Приход храма Покрова Пресвятой Богородицы аг.Переделка Лоевского района Гомельской епархии Белорусской Православной Церкви\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://loev-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Peredelka, Loyew district, Homel Diocese of the Belarusian Orthodox Church",
      "id": "by-homel-2d5d4bbd05",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Религиозная организация \"Религиозная община \"Приход храма Рождества Пресвятой Богородицы аг.Уборок Лоевского района Гомельской епархии Белорусской Православной Церкви\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://loev-deanery.cerkov.ru/o-blagochinii/"
      ],
      "name": "Parish of the Nativity of the Most Holy Theotokos Church in Uborok, Loyew district, Homel Diocese of the Belarusian Orthodox Church",
      "id": "by-homel-982b2319b8",
      "country": "BY"
    },
    {
      "parent": "ru-homel",
      "local": "Тихвинский женский монастырь",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://eparhiya.by/tihvinskij-zhenskij-monastyr/"
      ],
      "name": "Tikhvin Convent",
      "id": "by-homel-21ea31ff79",
      "country": "BY"
    }
  ],
  "ru-mahilyow": [
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма в честь равноапостольного князя Владимира",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church in honor of Equal-to-the-Apostles Prince Vladimir",
      "id": "by-mahilyow-5d03b739f3",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Свято-Крестовоздвиженский Борисо-Глебский собор",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Exaltation of the Cross and Saints Boris and Gleb Cathedral",
      "id": "by-mahilyow-013095f177",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Свято-Успенский мужской монастырь д. Пустынки (к. XIV в., 1808)",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/monastyri/"
      ],
      "name": "Holy Dormition Monastery in the village of Pustynki (14th century, 1808)",
      "id": "by-mahilyow-1f560a786f",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма в честь святых Веры, Надежды, Любови и их матери Софии д. Романовичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Martyrs Faith, Hope, and Love and Their Mother Sophia Church in Romanovichi",
      "id": "by-mahilyow-157bb4b53f",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма в честь св.праведных Иоакима и Анны г. Могилёв",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Righteous Joachim and Anna Church in Mahilyow",
      "id": "by-mahilyow-7ad8d0334b",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма прп. Серафима Саровского г. Могилёв",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Church of Saint Seraphim of Sarov, Mahilyow",
      "id": "by-mahilyow-8aa02dc6de",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма прп. Сергия Радонежского д. Дашковка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of Saint Sergius of Radonezh, Dashkovka village",
      "id": "by-mahilyow-a398a2afdb",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма апостолов Петра и Павла д. Махово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Apostles Peter and Paul in the village of Makhovo",
      "id": "by-mahilyow-c89476a776",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Успения Пресвятой Богородицы д. Голени",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Goleni",
      "id": "by-mahilyow-32ef8071c0",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Успения Пресвятой Богородицы д. Сухари",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Sukhari",
      "id": "by-mahilyow-80b0420522",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма святого великомученика и целителя Пантелеимона д. Кадино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon in the village of Kadino",
      "id": "by-mahilyow-701ab7cdfd",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Святой Живоначальной Троицы д. Восход",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Voskhod",
      "id": "by-mahilyow-d69b550ce6",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма иконы Божией Матери \"Всецарица\" г. Могилёв",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Queen of All\", Mahilyow",
      "id": "by-mahilyow-8f91f3d307",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Вейно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Veyno",
      "id": "by-mahilyow-fe94647323",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Казанской иконы Божией Матери г. Могилёв",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos, Mahilyow",
      "id": "by-mahilyow-e7f54b53bd",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Рождества Иоанна Крестителя аг. Буйничи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Nativity of John the Baptist agrotown of Buinichi",
      "id": "by-mahilyow-7d4188b4ca",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма Царственных Страстотерпцев г. Могилёв",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Church of the Royal Passion-Bearers in Mahilyow",
      "id": "by-mahilyow-ba5a7c7ff1",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход Свято-Троицкого храма д. Полыковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Holy Trinity Church in the village of Polykovichi",
      "id": "by-mahilyow-620d72003c",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход Спасо-Преображенского кафедрального собора г. Могилёва",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Transfiguration of the Lord Cathedral in Mahilyow",
      "id": "by-mahilyow-b40e9d73aa",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход Трехсвятительского собора (свтт. Василия Великого, Григория Богослова и Иоанна Златоуста) г. Могилёв",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-gorodskoe-blagochinie/"
      ],
      "name": "Parish of the Three Holy Hierarchs Cathedral in Mahilyow",
      "id": "by-mahilyow-b0962d990c",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Свято-Никольский женский монастырь г. Могилёв (1636)",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/monastyri/"
      ],
      "name": "Saint Nicholas Convent, Mahilyow (1636)",
      "id": "by-mahilyow-3e41f90eac",
      "country": "BY"
    },
    {
      "parent": "ru-mahilyow",
      "local": "Приход храма в честь блж. Матроны Московской",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://mogeparhia.by/xramy-eparxii/mogilevskoe-rajonnoe-blagochinie/"
      ],
      "name": "Parish of the Blessed Matrona of Moscow Church",
      "id": "by-mahilyow-e40eeb7b68",
      "country": "BY"
    }
  ],
  "ru-maladzyechna": [
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма в честь иконы Божией Матери \"Неопалимая Купина\" д. Кукшевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-v-chest-ikony-bozhiej-materi-neopalimaya-kupina-d-kukshevichi/"
      ],
      "name": "Parish of the Church in honor of the Icon of the Theotokos \"Burning Bush\" in the village of Kukshevichi",
      "id": "by-maladzyechna-42edbd2407",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Кафедральный собор святой праведной Анны г. Столбцы (Благочиннический центр)",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/kafedralnyj-sobor-svyatoj-pravednoj-anny-g-stolbczy-blagochinnicheskij-czentr/"
      ],
      "name": "Cathedral of Righteous Anna, Stolbtsy (Deanery Center)",
      "id": "by-maladzyechna-608561899b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Кафедральный собор Успения Пресвятой Богородицы г. Молодечно",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/kafedralnyj-sobor-uspeniya-presvyatoj-bogorodiczy-g-molodechno/"
      ],
      "name": "Cathedral of the Dormition of the Most Holy Theotokos, Molodechno",
      "id": "by-maladzyechna-91cf7f21e2",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Храм святого великомученника Георгия Победоносца, п. Новоколосово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/hram-svyatogo-velikomuchennika-georgiya-pobedonoscza-p-novokolosovo/"
      ],
      "name": "Church of the Great Martyr George the Victorious, Novokolosovo",
      "id": "by-maladzyechna-694aab0646",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Храм Воскресения Христова г. Столбцы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/hram-voskresenya-hristova-g-stolbczy/"
      ],
      "name": "Church of the Resurrection of Christ, Stolbtsy",
      "id": "by-maladzyechna-70515ba9d7",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого праведного Иосифа Обручника в аг. Ижа",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-svyatogo-pravednogo-iosifa-obruchnika-v-ag-izha/"
      ],
      "name": "Parish of the Church of Righteous Joseph the Betrothed in agrotown of Izha",
      "id": "by-maladzyechna-ce45be620b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святых равноапостольных Константина и Елены г. Воложин (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatyh-ravnoapostolnyh-konstantina-i-eleny-g-volozhin-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of Saints Constantine and Helen Equal-to-the-Apostles, Volozhin (deanery center)",
      "id": "by-maladzyechna-07f1300b92",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святых равноапостольных Мефодия и Кирилла г.п. Свирь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatyh-ravnoapostolnyh-mefodiya-i-kirilla-g-p-svir/"
      ],
      "name": "Parish of the Church of Saints Methodius and Cyril Equal-to-the-Apostles Svir",
      "id": "by-maladzyechna-3e08191505",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого Архангела Михаила аг. Налибоки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-svyatogo-arhangela-mihaila-d-naliboki/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel agrotown of Naliboki",
      "id": "by-maladzyechna-217c99d42e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого Архангела Михаила д. Граничи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-svyatogo-arhangela-mihaila-d-granichi/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Granichi",
      "id": "by-maladzyechna-32c7486fb4",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца д. Миколаевщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-nikolaevshhina/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Mikolaevshchina",
      "id": "by-maladzyechna-f93312a750",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца д. Могильно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-uzdenskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-mogilno/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Mogilno",
      "id": "by-maladzyechna-2f094ece10",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святителя Николая Чудотворца д. Мороськи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-moroski/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Moroski",
      "id": "by-maladzyechna-629150af5c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца д. Пряльники",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-pryalniki/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Pryalniki",
      "id": "by-maladzyechna-c280149787",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца д. Рубежевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-rubezhevichi/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Rubezhevichi",
      "id": "by-maladzyechna-a5eb55e0a1",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца д. Станьково",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-stankovo/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Stankovo",
      "id": "by-maladzyechna-f61f066b53",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца д. Старые Габы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-starye-gaby/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Starye Gaby",
      "id": "by-maladzyechna-a6b8314f1b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца п. Чисть",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-p-chist/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Chist",
      "id": "by-maladzyechna-0205bf5872",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святителя Николая Чудотворца п. Энергетиков",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-p-energetikov/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Energetikov village",
      "id": "by-maladzyechna-034050e0c9",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святителя Николая Чудотворца д. Словенск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-chudotvorcza-d-slovensk/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker, Slovensk",
      "id": "by-maladzyechna-d8a82a2856",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святителя Николая, архиепископа Мир Ликийских, д. Латыголь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-arhiepiskopa-mir-likijskih-d-latygol/"
      ],
      "name": "Parish of the Church of Saint Nicholas, Archbishop of Myra in Lycia, Latygol village",
      "id": "by-maladzyechna-1cf5cefe6f",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святителя Николая, архиепископа Мир Ликийских, д. Судники",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-svyatitelya-nikolaya-arhiepiskopa-mir-likijskih-d-sudniki/"
      ],
      "name": "Parish of the Church of Saint Nicholas, Archbishop of Myra in Lycia, Sudniki village",
      "id": "by-maladzyechna-072226ee8e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Праведной Анны д. Першаи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-svyatoj-pravednoj-anny-d-pershai/"
      ],
      "name": "Parish of the Church of Righteous Anna in the village of Pershai",
      "id": "by-maladzyechna-cb1c633531",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святой праведной Анны в д. Теплень",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-svyatoj-pravednoj-anny-v-d-teplen/"
      ],
      "name": "Parish of the Church of Righteous Anna in the village of Tepleny",
      "id": "by-maladzyechna-6f636ca924",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма преподобного Серафима Саровского г. Молодечно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-serafima-sarovskogo-g-molodechno/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov, Molodechno",
      "id": "by-maladzyechna-3d095d9604",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святителя Тихона, Патриарха Всероссийского г. Вилейка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-svyatitelya-tihona-patriarha-vserossijskogo-g-vilejka/"
      ],
      "name": "Parish of the Church of Saint Tikhon, Patriarch of All-Russia, Vileika",
      "id": "by-maladzyechna-2ebf3212ee",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Благовещения Пресвятой Богородицы д. Забрезье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-blagoveshheniya-presvyatoj-bogorodiczy-d-zabreze/"
      ],
      "name": "Parish of the Church of the Annunciation of the Most Holy Theotokos in the village of Zabreze",
      "id": "by-maladzyechna-6aca117a8a",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Вознесения Господня д. Яршевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-vozneseniya-gospodnya-d-yarshevichi/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Yarshevichi",
      "id": "by-maladzyechna-b87c0ac623",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Вознесения Господня д. Засковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-vozneseniya-gospodnya-d-zaskovichi/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Zaskovichi",
      "id": "by-maladzyechna-453a39148e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Вознесения Господня г. Фаниполь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-vozneseniya-gospodnya-g-fanipol/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord, Fanipol",
      "id": "by-maladzyechna-565af7bfb3",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Новый Свержень",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-novyj-sverzhen/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Novy Sverzhen",
      "id": "by-maladzyechna-1670b69c5b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Плебань",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-pleban/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Pleban",
      "id": "by-maladzyechna-92df41825a",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Понятичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-ponyatichi/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Ponyatichi",
      "id": "by-maladzyechna-78b9ffd3ec",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Рабунь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-rabun/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Rabun",
      "id": "by-maladzyechna-c77850dfe3",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Ручица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-ruchicza/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Ruchitsa",
      "id": "by-maladzyechna-1a8d8bee4c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Спягло",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-spyaglo/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Spyaglo",
      "id": "by-maladzyechna-a538133074",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Успения Пресвятой Богородицы д. Вязынь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-uspeniya-presvyatoj-bogorodiczy-d-vyazyn/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Vyazyn",
      "id": "by-maladzyechna-2c6d242e09",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма благоверного князя Александра Невского д. Турец-Бояры",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-blagovernogo-knyazya-aleksandra-nevskogo-d-turecz-boyary/"
      ],
      "name": "Parish of the Church of the Right-believing Prince Alexander Nevsky in the village of Turets-Boyary",
      "id": "by-maladzyechna-3390fc9aad",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма благоверного князя Александра Невского д. Великие Кривичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-blagovernogo-knyazya-aleksandra-nevskogo-d-velikie-krivichi/"
      ],
      "name": "Parish of the Church of the Right-believing Prince Alexander Nevsky in the village of Velikie Krivichi",
      "id": "by-maladzyechna-59e6c11519",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Собора Белорусских святых д. Шашки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-sobora-belorusskih-svyatyh-d-shashki/"
      ],
      "name": "Parish of the Church of the Synaxis of the Belarusian Saints in the village of Shashki",
      "id": "by-maladzyechna-dcc5fe87b3",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Собора Белорусских святых аг. Любань",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-sobora-belorusskih-svyatyh-d-lyuban/"
      ],
      "name": "Parish of the Synaxis of the Belarusian Saints Church in the agrotown of Lyuban",
      "id": "by-maladzyechna-c5e5642aba",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Положения Честной Ризы Пресвятой Богородицы во Влахерне д. Груздово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-polozheniya-chestnoj-rizy-presvyatoj-bogorodiczy-vo-vlaherne-d-gruzdovo/"
      ],
      "name": "Parish of the Deposition of the Robe of the Most Holy Theotokos at Blachernae Church in Gruzdovo",
      "id": "by-maladzyechna-65de387c68",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Введения во храм Пресвятой Богородицы д. Раевка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-vvedeniya-presvyatoj-bogorodiczy-d-raevka/"
      ],
      "name": "Parish of the Entry of the Most Holy Theotokos into the Temple Church in the village of Raevka",
      "id": "by-maladzyechna-2b671eb335",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Сорока мучеников Севастийских д. Костыки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-soroka-muchenikov-sevastijskih-d-kostyki/"
      ],
      "name": "Parish of the Church of the Forty Martyrs of Sebaste in the village of Kostyki",
      "id": "by-maladzyechna-40c7bd88db",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святых апостолов Петра и Павла аг. Озеро",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-uzdenskogo-blagochiniya/prihod-hrama-svyatyh-apostolov-petra-i-pavla-d-ozero/"
      ],
      "name": "Parish of Saints Peter and Paul Church in the agrotown of Ozero",
      "id": "by-maladzyechna-4f7b448e83",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святых Апостолов Петра и Павла д. Косута",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-svyatyh-apostolov-petra-i-pavla-d-kosuta/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Kosuta",
      "id": "by-maladzyechna-a7ad5a8f65",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святых апостолов Петра и Павла г. Узда (Благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-uzdenskogo-blagochiniya/prihod-hrama-svyatyh-apostolov-petra-i-pavla-g-uzda-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul, Uzda (Deanery Center)",
      "id": "by-maladzyechna-67f32e4d1e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого благоверного князя Александра Невского д. Хожево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-svyatogo-blagovernogo-knyazya-aleksandra-nevskogo-d-hozhevo/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky in the village of Khozhevo",
      "id": "by-maladzyechna-a7dc6f9aa1",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого благоверного князя Александра Невского д. Слобода",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatogo-blagovernogo-knyazya-aleksandra-nevskogo-d-sloboda/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky, Sloboda village",
      "id": "by-maladzyechna-d21e1cc9d2",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого великомученика и целителя Пантелеимона аг. Выверы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-i-czelitelya-panteleimona-ag-vyvery/"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon agrotown of Versions",
      "id": "by-maladzyechna-4c437f4944",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого великомученика Димитрия Солунского д. Мясота",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-dimitriya-solunskogo-d-myasota/"
      ],
      "name": "Parish of the Church of the Great Martyr Demetrius of Thessalonica in the village of Myasota",
      "id": "by-maladzyechna-4bc4ba5e6f",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого великомученика Георгия Победоносца д. Бельковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-belkovshhina/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Belkovshchina",
      "id": "by-maladzyechna-dd9682073e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого великомученика Георгия Победоносца д. Дубина-Юрздыцкая",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-dubina-yurzdyczkaya/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Dubina-Yurzdytskaya",
      "id": "by-maladzyechna-d056b85f64",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого великомученика Георгия Победоносца д. Лоск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-losk/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Losk",
      "id": "by-maladzyechna-6be8075068",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого великомученика Георгия Победоносца д. Слободка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-slobodka/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Slobodka",
      "id": "by-maladzyechna-f1caed258e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого великомученика Георгия Победоносца д. Вардомичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-vardomichi/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Vardomichi",
      "id": "by-maladzyechna-8c6c14e812",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого великомученика Георгия Победоносца г. Молодечно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-g-molodechno/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious, Molodechno",
      "id": "by-maladzyechna-725bf0c0b7",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого великомученика Георгия Победоносца п. Партизанский",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-svyatogo-velikomuchenika-georgiya-pobedonoscza-p-partizanskij/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious, Partizansky village",
      "id": "by-maladzyechna-9d46bb3948",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы аг. Долгиново",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-ag-dolginovo/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity agrotown of Dolginovo",
      "id": "by-maladzyechna-4c1ce14c79",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы аг. Княгинин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-d-knyaginin/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity agrotown of Knyaginin",
      "id": "by-maladzyechna-70dbaf19d7",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы аг. Лебедево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-ag-lebedevo/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity agrotown of Lebedevo",
      "id": "by-maladzyechna-5c4e69f5c1",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы аг. Марково",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-ag-markovo/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity agrotown of Markovo",
      "id": "by-maladzyechna-de7218db12",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы г. Мядель (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-g-myadel-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in Myadel (deanery center)",
      "id": "by-maladzyechna-623e4d402f",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы д. Городок",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-d-gorodok/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Gorodok",
      "id": "by-maladzyechna-9d3b69da37",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы д. Киевец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-d-kievecz/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Kievets",
      "id": "by-maladzyechna-b1e87e6f9f",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы д. Некасецк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-d-nekaseczk/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Nekasetsk",
      "id": "by-maladzyechna-4afca650af",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Живоначальной Троицы г.п. Кривичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatoj-zhivonachalnoj-troiczy-g-p-krivichi/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity Krivichi",
      "id": "by-maladzyechna-46cbc27aa7",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святых мучеников Антония, Иоанна и Евстафия Виленских д. Подберезь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatyh-muchenikov-antoniya-ioanna-i-evstafiya-vilenskih-d-podberez/"
      ],
      "name": "Parish of the Church of the Holy Martyrs Anthony, John and Eustathius of Vilna in the village of Podberez",
      "id": "by-maladzyechna-7c456156af",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого пророка Илии аг. Нарочь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ilii-ag-naroch/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah agrotown of Naroch",
      "id": "by-maladzyechna-40e109b48f",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого пророка Илии аг. Саковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ilii-ag-sakovshhina/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah agrotown of Sakovshchina",
      "id": "by-maladzyechna-9414dd05f6",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого пророка Илии д. Илья",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ilii-d-ilya/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah village Elijah",
      "id": "by-maladzyechna-959f129786",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого пророка Илии г.п. Радошковичи (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ilii-g-p-radoshkovichi/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah urban settlement of Radoshkovichi (deanery center)",
      "id": "by-maladzyechna-3c7b66b4d0",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого пророка Илии д. Дещенка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-uzdenskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ilii-d-deshhenka/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Deshchenka",
      "id": "by-maladzyechna-d0e459654c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого пророка Илии к.п. Нарочь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ilii-d-naroch/"
      ],
      "name": "Parish of the Prophet Elijah Church in Naroch",
      "id": "by-maladzyechna-096f1d0078",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого пророка Иоанна Крестителя д. Галимцы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-svyatogo-proroka-ioanna-krestitelya-d-galimczy/"
      ],
      "name": "Parish of the Church of the Holy Prophet John the Baptist in the village of Galimtsy",
      "id": "by-maladzyechna-5ae1a71d91",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святой праведной Елисаветы д. Затемень",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-svyatoj-pravednoj-elisavety-d-zatemen/"
      ],
      "name": "Parish of the Church of the Holy Righteous Elizabeth in the village of Temene",
      "id": "by-maladzyechna-139d3a229b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святого праведного Иосифа Обручника д. Городилово (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-svyatogo-pravednogo-iosifa-obruchnika-d-gorodilovo-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Holy Righteous Joseph the Betrothed in the village of Gorodilovo (deanery center)",
      "id": "by-maladzyechna-068093aa41",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святого Духа д. Речки (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-svyatogo-duha-d-rechki-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Holy Spirit in the village of Rechki (deanery center)",
      "id": "by-maladzyechna-33dc60cb5a",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святых бессребреников Космы и Дамиана д. Вишнево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-svyatyh-bessrebrennikov-kosmy-i-damiana-d-vishnevo/"
      ],
      "name": "Parish of the Church of the Holy Unmercenaries Cosmas and Damian in the village of Vishnevo",
      "id": "by-maladzyechna-dc56e9f293",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Святой Преподобной Евфросинии Полоцкой г/п Ивенец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-svyatoj-prepodobnoj-evfrosinii-poloczkoj-g-p-ivenecz/"
      ],
      "name": "Parish of the Church of the Venerable Euphrosyne of Polotsk, Ivenets",
      "id": "by-maladzyechna-47a6854335",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма иконы Божией Матери \"Неупиваемая Чаша\" д. Великий Двор",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-ikony-bozhiej-materi-neupivaemaya-chasha-d-velikij-dvor/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Inexhaustible Chalice\" in the village of Velikiy Dvor",
      "id": "by-maladzyechna-2ca38ec955",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма иконы Божией Матери Казанская п. Путчино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-ikony-bozhiej-materi-kazanskaya-p-putchino/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos of Kazan, Putchino",
      "id": "by-maladzyechna-c79e139864",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы аг. Городьки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-ag-gorodki/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos agrotown of Gorodki",
      "id": "by-maladzyechna-cbcfd124a9",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы г. Молодечно (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-g-molodechno-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in Molodechno (deanery center)",
      "id": "by-maladzyechna-0400bdea66",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Аталезь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-atalez/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Atalez",
      "id": "by-maladzyechna-fdb5c8e111",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Беница",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-benicza/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Benitsa",
      "id": "by-maladzyechna-3b44fdbf74",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Бубны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-bubny/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Bubny",
      "id": "by-maladzyechna-096525765c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Доры",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-dory/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Dory",
      "id": "by-maladzyechna-f7db4c58f3",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Хотляны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-uzdenskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-hotlyany/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Khotlyany",
      "id": "by-maladzyechna-62cf89c5c3",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Красное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-krasnoe/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Krasnoe",
      "id": "by-maladzyechna-67fda9c550",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова пресвятой Богородицы д. Любковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-lyubkovshhina/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Lyubkovshchina",
      "id": "by-maladzyechna-af71181df7",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Осиповщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-d-osipovshhina/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Osipovshchina",
      "id": "by-maladzyechna-8dd1df99c7",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы г. Дзержинск (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-g-dzerzhinsk-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Dzerzhinsk (deanery center)",
      "id": "by-maladzyechna-f07b825c3b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Покрова Пресвятой Богородицы г. Вилейка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-pokrova-presvyatoj-bogorodiczy-g-vilejka/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, Vileika",
      "id": "by-maladzyechna-5a6f1ba00b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Христова г. Молодечно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-molodechnenskogo-blagochiniya/prihod-hrama-rozhdestva-hristova-g-molodechno/"
      ],
      "name": "Parish of the Church of the Nativity of Christ in Molodechno",
      "id": "by-maladzyechna-adf9e01893",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Иоанна Предтечи аг. Вишневец (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-svyatogo-proroka-ioanna-krestitelya-ag-vishnevecz/"
      ],
      "name": "Parish of the Church of the Nativity of John the Baptist agrotown of Vishnevets (deanery center)",
      "id": "by-maladzyechna-bebc72ce92",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Иоанна Предтечи д. Олехновичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-rozhdestva-ioanna-predtechi-d-olehnovichi/"
      ],
      "name": "Parish of the Church of the Nativity of John the Baptist in the village of Olekhnovichi",
      "id": "by-maladzyechna-f1d0529f6d",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Иоанна Предтечи д. Засулье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-stolbczovskogo-blagochiniya/prihod-hrama-rozhdestva-ioanna-predtechi-d-zasule/"
      ],
      "name": "Parish of the Church of the Nativity of John the Baptist in the village of Zasulye",
      "id": "by-maladzyechna-fd790742ee",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Пресвятой Богородицы аг. Куренец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-rozhdestva-presvyatoj-bogorodiczy-ag-kurenecz/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos agrotown of Kurenets",
      "id": "by-maladzyechna-88157ad1e1",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Добрынево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-rozhdestva-presvyatoj-bogorodiczy-d-dobrynevo/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Dobrynevo",
      "id": "by-maladzyechna-51f3458c4c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Дуброво",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-radoshkovichskogo-blagochiniya/prihod-hrama-rozhdestva-presvyatoj-bogorodiczy-d-dubrovo/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Dubrovo",
      "id": "by-maladzyechna-1cbe9909f9",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Мильча",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dolginovskogo-blagochiniya/prihod-hrama-rozhdestva-presvyatoj-bogorodiczy-d-milcha/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Milcha",
      "id": "by-maladzyechna-cb75356e3a",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Полочаны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-rozhdestva-presvyatoj-bogorodiczy-d-polochany/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Polochany",
      "id": "by-maladzyechna-32f1770e15",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Старый Свержень",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vishneveczkogo-blagochiniya/prihod-hrama-rozhdestva-presvyatoj-bogorodiczy-d-staryj-sverzhen/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Stary Sverzhen",
      "id": "by-maladzyechna-23a72befb1",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Новомучеников Белорусских г. Дзержинск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-novomuchenikov-belorusskih-g-dzerzhinsk/"
      ],
      "name": "Parish of the Church of the New Martyrs of Belarus, Dzerzhinsk",
      "id": "by-maladzyechna-f71d5b92e0",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма пророка Иоанна Предтечи д. Баровцы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-proroka-ioanna-predtechi-d-barovczy/"
      ],
      "name": "Parish of the Church of the Prophet John the Baptist in the village of Barovtsi",
      "id": "by-maladzyechna-d922d0173e",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня аг. Черкассы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-d-cherkassy/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord agrotown of Cherkasy",
      "id": "by-maladzyechna-5a5e3c477b",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня аг. Раков (Благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-rakovskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-ag-rakov-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord agrotown of Rakov (Deanery Center)",
      "id": "by-maladzyechna-5924ff738c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня д. Довбени",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-d-dovbeni/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Dovbeni",
      "id": "by-maladzyechna-869c0b0123",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня д. Носилово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-gorodilovskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-d-nosilovo/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Nosilovo",
      "id": "by-maladzyechna-8083d9a220",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня д. Заболотье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-ilyanskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-d-zabolote/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Zabolotye",
      "id": "by-maladzyechna-ee1ffbc98c",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня д. Занарочь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-myadelskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-d-zanaroch/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Zanaroch",
      "id": "by-maladzyechna-d2fc1837e0",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма Преображения Господня г. Воложин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-volozhinskogo-blagochiniya/prihod-hrama-preobrazheniya-gospodnya-g-volozhin/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord, Volozhin",
      "id": "by-maladzyechna-ce8cb30c52",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма святых бессребреников Космы и Дамиана п. Негорелое",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-dzerzhinskogo-blagochiniya/prihod-hrama-svyatyh-bessrebrenikov-kosmy-i-damiana-p-negoreloe/"
      ],
      "name": "Parish of the Church of the Unmercenary Saints Cosmas and Damian, Negoreloye village",
      "id": "by-maladzyechna-2f8405a2fc",
      "country": "BY"
    },
    {
      "parent": "ru-maladzyechna",
      "local": "Приход храма преподобной Марии Египетской г. Вилейка (благочиннический центр)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://molod-eparchy.by/ru/hramy-vilejskogo-blagochiniya/prihod-hrama-prepodobnoj-marii-egipetskoj-g-vilejka-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Church of the Venerable Mary of Egypt, Vileika (deanery center)",
      "id": "by-maladzyechna-3fc77e460a",
      "country": "BY"
    }
  ],
  "ru-slutsk": [
    {
      "parent": "ru-slutsk",
      "local": "Кафедральный собор святого Архангела Михаила в г. Слуцке",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/kafedralnyj-sobor-svyatogo-arhangela-mihaila-v-g-sluczke/"
      ],
      "name": "Cathedral of Saint Michael the Archangel in Slutsk",
      "id": "by-slutsk-6153b6de50",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм равноапостольных Мефодия и Кирилла г.п.Уречье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-ravnoapostolnyh-mefodiya-i-kirilla-g-p-ureche/"
      ],
      "name": "Church of Equal-to-the-Apostles Methodius and Cyril, Urechye",
      "id": "by-slutsk-37d747e6a3",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм праведной Софии, княгини Слуцкой, женского монастыря в честь праведной Софии, княгини Слуцкой, г. Слуцка",
      "rank": "Church",
      "kind": "monastery",
      "sources": [
        "https://sluck-eparchiya.by/hram-pravednoj-sofii-knyagini-sluczkoj-zhenskogo-monastyrya-v-chest-pravednoj-sofii-knyagini-sluczkoj-g-sluczka/"
      ],
      "name": "Righteous Sophia of Slutsk Church at the Righteous Sophia of Slutsk Convent in Slutsk",
      "id": "by-slutsk-1c4ccd07a5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителей Николая и Спиридона Чудотворцев в г. Солигорске",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-svyatitelej-nikolaya-chudotvorcza-i-spiridona-trimifuntskogo-g-soligorska/"
      ],
      "name": "Church of Saints Nicholas and Spyridon the Wonderworkers in Soligorsk",
      "id": "by-slutsk-f9740965f5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого Архангела Михаила д. Сороги",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-arhangela-mihaila-d-sorogi/"
      ],
      "name": "Church of Saint Archangel Michael in the village of Sorogi",
      "id": "by-slutsk-a2f7d445e6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Димитрия Ростовского д. Долгое",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-dimitriya-rostovskogo-d-dolgoe/"
      ],
      "name": "Church of Saint Demetrius of Rostov, Dolgoye",
      "id": "by-slutsk-691425c04b",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм преподобной Евфросинии Полоцкой аг. Сковшин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-prepodobnoj-evfrosinii-poloczkoj-ag-skovshin/"
      ],
      "name": "Church of Venerable Euphrosyne of Polotsk agrotown of Skovshin",
      "id": "by-slutsk-7d88432632",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм преподобной Евфросинии Полоцкой аг.Сосны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-prepodobnoj-evfrosinii-poloczkoj-ag-sosny/"
      ],
      "name": "Church of Venerable Euphrosyne of Polotsk agrotown of Sosny",
      "id": "by-slutsk-39d90dbdb1",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Георгия Могилевского г.п. Красная Слобода",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-georgiya-mogilevskogo-g-p-krasnaya-sloboda/"
      ],
      "name": "Church of Saint George of Mahilyow Krasnaya Sloboda",
      "id": "by-slutsk-6a6d861d29",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Иоанна Богослова д. Кирово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-ioanna-bogoslova-d-kirovo/"
      ],
      "name": "Church of Saint John the Theologian, Kirovo",
      "id": "by-slutsk-eb6f4a407c",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг. Лучники",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-luchniki/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker agrotown of Archers",
      "id": "by-slutsk-c1bf7a0c64",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг. Лядно",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-lyadno/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker agrotown of Cool",
      "id": "by-slutsk-d8bca812dd",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг.Грицкевичи (1861)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-griczkevichi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker agrotown of Gritskevichi (1861)",
      "id": "by-slutsk-8bcd970dad",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг.Юшевичи (1929)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-yushevichi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker agrotown of Yushevichi (1929)",
      "id": "by-slutsk-4f2139d95b",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг.Грозово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-grozovo/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in Grozovo",
      "id": "by-slutsk-c32c67bec6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца д. Гаврильчицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-d-gavrilchiczy/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Gavrilchitsy",
      "id": "by-slutsk-79481987f5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца д. Обидемля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-d-obidemlya/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Obidemlya",
      "id": "by-slutsk-8ded5052dd",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца г.п. Старобин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-g-p-starobin/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker Starobin",
      "id": "by-slutsk-68e4f30c83",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца д.Тимковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-d-timkovichi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker village of Timkovichi",
      "id": "by-slutsk-8365a258c7",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг.Малые Городятичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-malye-gorodyatichi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Malye Gorodyatichi",
      "id": "by-slutsk-3f6199b000",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца аг.Синявка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-ag-sinyavka/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Sinyavka",
      "id": "by-slutsk-d374883b05",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца г. Старые Дороги - благочиннический центр",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-g-starye-dorogi-blagochinnicheskij-czentr/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Starye Dorogi - deanery center",
      "id": "by-slutsk-b8ef5b6638",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святителя Николая Чудотворца г.п.Уречье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatitelya-nikolaya-chudotvorcza-g-p-ureche/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Urechye",
      "id": "by-slutsk-55dd4deb00",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм преподобного Симеона Столпника д. Борок",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-prepodobnogo-simeona-stolpnika-d-borok/"
      ],
      "name": "Church of Venerable Simeon the Stylite, Borok village",
      "id": "by-slutsk-1f929fb4ed",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Благовещения Пресвятой Богородицы д.Куноса (1887)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-blagoveshheniya-presvyatoj-bogorodiczy-d-kunosa/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos in the village of Kunos (1887)",
      "id": "by-slutsk-170324cc3b",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Благовещения Пресвятой Богородицы д. Старые Терушки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-blagoveshheniya-presvyatoj-bogorodiczy-d-starye-terushki/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos in the village of Starye Terushki",
      "id": "by-slutsk-d66d739d0f",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм апостола Иоанна Богослова д.Русаки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-apostola-ioanna-bogoslova-d-rusaki/"
      ],
      "name": "Church of the Apostle John the Theologian in the village of Rusaki",
      "id": "by-slutsk-06e1716089",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Вознесения Господня в г.Копыле - благочиннический центр",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-vozneseniya-gospodnya-v-g-kopyle-blagochinnicheskij-czentr/"
      ],
      "name": "Church of the Ascension of the Lord in Kopyl - deanery center",
      "id": "by-slutsk-70d1187673",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Вознесения Господня г.Несвижа - благочиннический центр (2016)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-vozneseniya-gospodnya-g-nesvizha-blagochinnicheskij-czentr/"
      ],
      "name": "Church of the Ascension of the Lord in Nesvizh - deanery center (2016)",
      "id": "by-slutsk-a22a0a6a0e",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Вознесения Господня д. Большой Рожан",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-vozneseniya-gospodnya-d-bolshoj-rozhan/"
      ],
      "name": "Church of the Ascension of the Lord in the village of Bolshoy Rozhan",
      "id": "by-slutsk-49f2117af6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Вознесения Господня д.Киевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-vozneseniya-gospodnya-d-kievichi/"
      ],
      "name": "Church of the Ascension of the Lord in the village of Kievichi",
      "id": "by-slutsk-24a25ea27d",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Успения Пресвятой Богородицы аг.Речень",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-uspeniya-presvyatoj-bogorodiczy-ag-rechen/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos agrotown of Receni",
      "id": "by-slutsk-e98f5e2246",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Успения Пресвятой Богородицы д.Бабичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-uspeniya-presvyatoj-bogorodiczy-d-babichi/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Babichi",
      "id": "by-slutsk-e06237f4d6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Успения Пресвятой Богородицы д.Васильчицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-uspeniya-presvyatoj-bogorodiczy-d-vasilchiczy/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Vasilchitsy",
      "id": "by-slutsk-097869541c",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Усекновения главы Иоанна Предтечи д.Межная Слобода",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-useknoveniya-glavy-ioanna-predtechi-d-mezhnaya-sloboda/"
      ],
      "name": "Church of the Beheading of John the Baptist, Mezhnaya Sloboda village",
      "id": "by-slutsk-91683bd273",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм блаженной Матроны Московской г. Солигорска",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-blazhennoj-matrony-moskovskoj-g-soligorska/"
      ],
      "name": "Church of the Blessed Matrona of Moscow, Soligorsk",
      "id": "by-slutsk-00899de859",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм благоверного князя Александра Невского в г. Слуцке",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-blagovernogo-knyazya-aleksandra-nevskogo-v-g-sluczke/"
      ],
      "name": "Church of the Right-believing Prince Alexander Nevsky in Slutsk",
      "id": "by-slutsk-fd6a8f1058",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм благоверного князя Александра Невского п. Новое",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-blagovernogo-knyazya-aleksandra-nevskogo-p-novoe/"
      ],
      "name": "Church of the Right-believing Prince Alexander Nevsky, Novoe village",
      "id": "by-slutsk-fe9c254110",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Собора Белорусских святых в г.Несвиже",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-sobora-belorusskih-svyatyh-v-g-nesvizhe/"
      ],
      "name": "Church of the Synaxis of the Belarusian Saints in Nesvizh",
      "id": "by-slutsk-d0b6c22ee6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Воздвижения Креста Господня д.Большая Лысица (1918)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-vozdvizheniya-kresta-gospodnya-d-bolshaya-lysicza/"
      ],
      "name": "Church of the Exaltation of the Holy Cross in the village of Bolshaya Lysitsa (1918)",
      "id": "by-slutsk-7ebcc36941",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Воздвижения Креста Господня д.Цепра",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-vozdvizheniya-kresta-gospodnya-d-czepra/"
      ],
      "name": "Church of the Exaltation of the Holy Cross in the village of Tsepra",
      "id": "by-slutsk-1420af9c85",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм великомученика Георгия Победоносца д.Велешино-1",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-velikomuchenika-georgiya-pobedonoscza-d-veleshino-1/"
      ],
      "name": "Church of the Great Martyr George the Victorious, Veleshino-1",
      "id": "by-slutsk-09b8889127",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого апостола Иоанна Богослова г.п. Старобин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-apostola-ioanna-bogoslova-g-p-starobin/"
      ],
      "name": "Church of the Holy Apostle John the Theologian Starobin",
      "id": "by-slutsk-845775ec9e",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого апостола Иоанна Богослова д.Савково",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-apostola-ioanna-bogoslova-d-savkovo/"
      ],
      "name": "Church of the Holy Apostle John the Theologian, Savkovo",
      "id": "by-slutsk-ae3a331c9c",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святых апостолов Петра и Павла аг.Грицевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatyh-apostolov-petra-i-pavla-ag-griczevichi/"
      ],
      "name": "Church of the Holy Apostles Peter and Paul agrotown of Gritsevichi",
      "id": "by-slutsk-0ac68539b2",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святых апостолов Петра и Павла д.Бучатино",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatyh-apostolov-petra-i-pavla-d-buchatino/"
      ],
      "name": "Church of the Holy Apostles Peter and Paul in the village of Buchatino",
      "id": "by-slutsk-67ff7746c8",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого великомученика Георгия Победоносца аг. Залужье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-velikomuchenika-georgiya-pobedonoscza-ag-zaluzhe/"
      ],
      "name": "Church of the Great Martyr George the Victorious agrotown of Zaluzhye",
      "id": "by-slutsk-12adc3ee48",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого великомученика Георгия Победоносца аг.Островки (1844)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-velikomuchenika-georgiya-pobedonoscza-ag-ostrovki/"
      ],
      "name": "Church of the Great Martyr George the Victorious in Ostrovka (1844)",
      "id": "by-slutsk-3a38fd7179",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого великомученика Георгия Победоносца д.Лешня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-leshnya/"
      ],
      "name": "Church of the Great Martyr George the Victorious in the village of Leshnya",
      "id": "by-slutsk-84e8bab2da",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого великомученика Георгия Победоносца д. Ветка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-velikomuchenika-georgiya-pobedonoscza-d-vetka/"
      ],
      "name": "Church of the Great Martyr George the Victorious in the village of Vetka",
      "id": "by-slutsk-c9eff2b680",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого великомученика Георгия Победоносца г.Несвижа (1955)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-velikomuchenika-georgiya-pobedonoscza-g-nesvizha/"
      ],
      "name": "Church of the Great Martyr George the Victorious, Nesvizh (1955)",
      "id": "by-slutsk-bfe2e37e7c",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Нерукотворного образа Господня д.Кудиновичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-nerukotvornogo-obraza-gospodnya-d-kudinovichi/"
      ],
      "name": "Church of the Holy Image of the Lord Not Made by Hands, village of Kudinovichi",
      "id": "by-slutsk-f94143c49b",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Святой Живоначальной Троицы аг.Таль",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatoj-zhivonachalnoj-troiczy-ag-tal/"
      ],
      "name": "Church of the Holy Life-giving Trinity agrotown of Tal",
      "id": "by-slutsk-03ac4bbfc4",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Святой Живоначальной Троицы аг.Солтановщина (1826)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatoj-zhivonachalnoj-troiczy-ag-soltanovshhina/"
      ],
      "name": "Church of the Holy Life-giving Trinity in Soltanovshchina (1826)",
      "id": "by-slutsk-cc43156c43",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Святой Живоначальной Троицы д.Телядовичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatoj-zhivonachalnoj-troiczy-d-telyadovichi/"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Telyadovichi",
      "id": "by-slutsk-e211bc6690",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого мученика Вонифатия д. Павловка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-muchenika-vonifatiya-d-pavlovka/"
      ],
      "name": "Church of the Martyr Boniface, Pavlovka village",
      "id": "by-slutsk-74d9e02516",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святой мученицы Наталии д.Закальное",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatoj-mucheniczy-natalii-d-zakalnoe/"
      ],
      "name": "Church of the Martyr Natalia, Zakalnoe village",
      "id": "by-slutsk-94b60d82d3",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святых мучениц Веры, Надежды, Любви и матери их Софии аг. Пасека",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatyh-muchenicz-very-nadezhdy-lyubvi-i-materi-ih-sofii-ag-paseka/"
      ],
      "name": "Holy Martyrs Faith, Hope, and Love and Their Mother Sophia Church in the agrotown of Paseka",
      "id": "by-slutsk-9c60d3ff32",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого пророка Илии аг.Орешница",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-proroka-ilii-ag-oreshnicza/"
      ],
      "name": "Church of the Holy Prophet Elijah agrotown of Oreshnitsa",
      "id": "by-slutsk-6d4e76ec94",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святого пророка Иоанна Предтечи д.Затурья (2014)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-proroka-ioanna-predtechi-d-zaturya/"
      ],
      "name": "Church of the Holy Prophet John the Baptist village of Zaturya (2014)",
      "id": "by-slutsk-0499a788c5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святой праведной Анны аг.Оношки (2000)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatoj-pravednoj-anny-ag-onoshki/"
      ],
      "name": "Church of the Holy Righteous Anna in Onoshka (2000)",
      "id": "by-slutsk-7b354423f6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святых бессребреников Космы и Дамиана аг. Щитковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatyh-bessrebrenikov-kosmy-i-damiana-ag-shhitkovichi/"
      ],
      "name": "Church of the Holy Unmercenaries Cosmas and Damian agrotown of Shchitkovichi",
      "id": "by-slutsk-8b3e72ae47",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм святых бессребренников Космы и Дамиана аг.Снов (1836)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatyh-bessrebrennikov-kosmy-i-damiana-ag-snov/"
      ],
      "name": "Holy Unmercenaries Cosmas and Damian Church in the agrotown of Snov (1836)",
      "id": "by-slutsk-9e6714f98d",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм иконы Божией Матери \"Целительница\" в г. Слуцке",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-ikony-bozhiej-materi-czelitelnicza-v-g-sluczke/"
      ],
      "name": "Church of the Icon of the Theotokos \"Healer\" in Slutsk",
      "id": "by-slutsk-9e8afeb91a",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы аг. Весея",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-ag-veseya/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos agrotown of Veseya",
      "id": "by-slutsk-09fd094bf5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы аг.Лань (1844)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-ag-lan/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos agrotown of Lan (1844)",
      "id": "by-slutsk-93ae3d64ea",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д. Болотчицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-bolotchiczy/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Bolotchitsy",
      "id": "by-slutsk-24f24912ee",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д. Хоростово",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-horostovo/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Khorostovo",
      "id": "by-slutsk-96df7a1226",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д.Кузьмичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-kuzmichi/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Kuzmichi",
      "id": "by-slutsk-22fe708b09",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д. Осово (приписной)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-osovo-pripisnoj/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Osovo (attributed)",
      "id": "by-slutsk-9fe1297c27",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д.Песочное",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-pesochnoe/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Pesochnoe",
      "id": "by-slutsk-fd8a221197",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д.Потейки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-potejki/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Poteyki",
      "id": "by-slutsk-a35c4f915f",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д.Семежево",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-semezhevo/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Semezhevo",
      "id": "by-slutsk-c785e04ab2",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д. Серяги",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-seryagi/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Seryaga",
      "id": "by-slutsk-3de9896745",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Покрова Пресвятой Богородицы д.Великая Липа (1873)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-velikaya-lipa/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Velikaya Lipa (1873)",
      "id": "by-slutsk-916225cde0",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Казанской иконы Божией Матери аг.Друцковщизна (2008)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-kazanskoj-ikony-bozhiej-materi-ag-druczkovshhizna/"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in Drutskovshchizna (2008)",
      "id": "by-slutsk-10c46fb22d",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Казанской иконы Божией Матери г.Любани",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-kazanskoj-ikony-bozhiej-materi-g-lyubani/"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in Lyuban",
      "id": "by-slutsk-8cf13a7ee1",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "храм Казанской иконы Божией Матери д. Кунцевщина",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-kazanskoj-ikony-bozhiej-materi-d-kunczevshhina/"
      ],
      "name": "Church of the Kazan Icon of the Theotokos in the village of Kuntsevshchina",
      "id": "by-slutsk-c1abf4d739",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм мученицы Параскевы Пятницы д. Гоцк",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-mucheniczy-paraskevy-pyatniczy-d-goczk/"
      ],
      "name": "Church of the Martyr Paraskeva in the village of Gotsk",
      "id": "by-slutsk-7d0cb7bc3d",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Рождества Христова аг. Прусы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-rozhdestva-hristova-ag-prusy/"
      ],
      "name": "Church of the Nativity of Christ agrotown of Prussians",
      "id": "by-slutsk-abcc3d1304",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Рождества Пресвятой Богородицы аг. Греск",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-rozhdestva-presvyatoj-bogorodiczy-ag-gresk/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos agrotown of Gresk",
      "id": "by-slutsk-578d5eeecd",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Рождества Пресвятой Богородицы аг.Осовец",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-rozhdestva-presvyatoj-bogorodiczy-ag-osovecz/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in Osovets",
      "id": "by-slutsk-e67218b81c",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Рождества Пресвятой Богородицы г.п.Городея",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-rozhdestva-presvyatoj-bogorodiczy-g-p-gorodeya/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos, Gorodeya",
      "id": "by-slutsk-dae452c8d1",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм страстотерпицы царицы Александры д.Камень",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-strastoterpiczy-czariczy-aleksandry-d-kamen/"
      ],
      "name": "Church of the Passion-Bearer Queen Alexandra, Kamen village",
      "id": "by-slutsk-8a8684f125",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Воскресения Христова г.Клецка - благочиннический центр",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-voskreseniya-hristova-g-kleczka-blagochinnicheskij-czentr/"
      ],
      "name": "Church of the Resurrection of Christ in Kletsk - deanery center",
      "id": "by-slutsk-6969303d1d",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Преображения Господня аг. Языль",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-preobrazheniya-gospodnya-ag-yazyl/"
      ],
      "name": "Church of the Transfiguration of the Lord agrotown of Yazyl",
      "id": "by-slutsk-47a27bb6b6",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Преображения Господня в г.Любани - благочиннический центр",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-preobrazheniya-gospodnya-g-lyuban-blagochinnicheskij-czentr/"
      ],
      "name": "Church of the Transfiguration of the Lord in Lyuban - deanery center",
      "id": "by-slutsk-3bfec931c7",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Преображения Господня д.Доросино",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-preobrazheniya-gospodnya-d-dorosino/"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Dorosino",
      "id": "by-slutsk-eed93d249b",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Преображения Господня д. Краснодворцы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-preobrazheniya-gospodnya-d-krasnodvorczy/"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Krasnodvortsy",
      "id": "by-slutsk-06ad1bbc2f",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм Преображения Господня д.Нагорное",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-preobrazheniya-gospodnya-d-nagornoe/"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Nagornoye",
      "id": "by-slutsk-7d81b994b5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Храм бессребренников Космы и Дамиана женского монастыря в честь праведной Софии, княгини Слуцкой г. Слуцка",
      "rank": "Church",
      "kind": "monastery",
      "sources": [
        "https://sluck-eparchiya.by/hram-bessrebrennikov-kosmy-i-damiana-zhenskogo-monastyrya-v-chest-pravednoj-sofii-knyagini-sluczkoj-g-sluczka/"
      ],
      "name": "Holy Unmercenaries Cosmas and Damian Church at the Righteous Sophia of Slutsk Convent in Slutsk",
      "id": "by-slutsk-031c6e6262",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход кафедрального собора Рождества Христова в г. Солигорске - благочиннический центр",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-kafedralnogo-sobora-rozhdestva-hristova-v-g-soligorske-blagochinnicheskij-czentr/"
      ],
      "name": "Parish of the Cathedral of the Nativity of Christ in Soligorsk - deanery center",
      "id": "by-slutsk-b6551130c2",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма святой праведной Софии, княгини Слуцкой аг. Величковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-svyatoj-pravednoj-sofii-knyagini-sluczkoj-ag-velichkovichi/"
      ],
      "name": "Parish of Righteous Sophia of Slutsk Church in the agrotown of Velichkovichi",
      "id": "by-slutsk-3f94dd7f5a",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма святой праведной Софии, княгини Слуцкой аг. Вежи Слуцкого района",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatoj-pravednoj-sofii-knyagini-sluczkoj-ag-vezhi-sluczkogo-rajona/"
      ],
      "name": "Parish of Righteous Sophia of Slutsk Church in the agrotown of Vezhi, Slutsk district",
      "id": "by-slutsk-b69ff72bde",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма преподобного Серафима Саровского г. Солигорска",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-prepodobnogo-serafima-sarovskogo-g-soligorska/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov in Soligorsk",
      "id": "by-slutsk-6ed024f8df",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма великомученицы Варвары и мученика Трифона г. Солигорска",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-velikomucheniczy-varvary-i-muchenika-trifona-g-soligorska/"
      ],
      "name": "Parish of the Church of the Great Martyr Barbara and Martyr Tryphon in Soligorsk",
      "id": "by-slutsk-3d3c2f3c14",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма святых апостолов Петра и Павла д.Новоселки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-svyatyh-apostolov-petra-i-pavla-d-novoselki/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Novoselki",
      "id": "by-slutsk-2a9f888af5",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма святых мучениц Веры, Надежды, Любови и матери их Софии в г. Слуцке",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-svyatyh-muchenicz-very-nadezhdy-lyubovi-i-materi-ih-sofii-v-g-sluczke/"
      ],
      "name": "Parish of the Holy Martyrs Faith, Hope, and Love and Their Mother Sophia Church in Slutsk",
      "id": "by-slutsk-0caaf8d98f",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма святого пророка Илии аг. Козловичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatogo-proroka-ilii-ag-kozlovichi/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah agrotown of Kozlovichi",
      "id": "by-slutsk-fe81ea7626",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Чижевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-pokrova-presvyatoj-bogorodiczy-d-chizhevichi/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Chizhevichi",
      "id": "by-slutsk-d6f0f55b46",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма святых праведной княгини Софии и мученика младенца Гавриила Слуцких агрогородка Гацук",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-svyatyh-pravednoj-knyagini-sofii-i-muchenika-mladencza-gavriila-sluczkih-agrogorodka-gaczuk/"
      ],
      "name": "Parish of Righteous Sophia of Slutsk and Infant Martyr Gabriel of Slutsk Church in the agrotown of Gatsuk",
      "id": "by-slutsk-9c79983470",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма Преображения Господня д. Гольчичи Слуцкого района",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/hram-preobrazheniya-gospodnya-d-golchichi-sluczkogo-rajona/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Golchichi, Slutsk district",
      "id": "by-slutsk-9f84b68e4c",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход храма Преображения Господня д.Старица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-hrama-preobrazheniya-gospodnya-d-staricza/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Staritsa",
      "id": "by-slutsk-325ace6dc1",
      "country": "BY"
    },
    {
      "parent": "ru-slutsk",
      "local": "Приход кафедрального собора святителя Николая Чудотворца и храм преподобного Паисия Святогорца в г. Слуцке",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://sluck-eparchiya.by/prihod-kafedralnogo-sobora-svyatitelya-nikolaya-chudotvorcza-i-hram-prepodobnogo-paisiya-svyatogorcza-v-g-sluczke/"
      ],
      "name": "Parish of the Cathedral of Venerable Nicholas the Wonderworker and the Church of Venerable Paisius of the Holy Mountain in Slutsk",
      "id": "by-slutsk-fc710d619e",
      "country": "BY"
    }
  ],
  "ru-turaw": [
    {
      "parent": "ru-turaw",
      "local": "Кафедральный собор святителей Кирилла и Лаврентия Туровских г. Туров",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15805/"
      ],
      "name": "Cathedral of Saints Cyril and Lawrence of Turov, Turov",
      "id": "by-turaw-99ee1b0e59",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Кафедральный собор святого Архангела Михаила г. Мозырь",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15827/"
      ],
      "name": "Cathedral of Saint Archangel Michael, Mozyr",
      "id": "by-turaw-3259edd7e0",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Собор Казанской иконы Божией Матери г. Калинковичи",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15832/"
      ],
      "name": "Cathedral of the Kazan Icon of the Theotokos, Kalinkovichi",
      "id": "by-turaw-957ff41542",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Собор Рождества Пресвятой Богородицы аг. Юровичи",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15807/"
      ],
      "name": "Cathedral of the Nativity of the Most Holy Theotokos agrotown of Jurovichi",
      "id": "by-turaw-5ba026436a",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм в честь святителя Николая Чудотворца д. Антонов",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15800/"
      ],
      "name": "Church in honor of Saint Nicholas the Wonderworker, Antonov village",
      "id": "by-turaw-5f069521d1",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм в честь святителя Спиридона Тримифутского г. Калинковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15831/"
      ],
      "name": "Saint Spyridon of Tremithus Church in Kalinkovichi",
      "id": "by-turaw-a6efb19ab6",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм в честь святого апостола Иоанна Богослова г. Наровля",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15819/"
      ],
      "name": "Church in honor of the Holy Apostle John the Theologian, Narovlya",
      "id": "by-turaw-91db5f2988",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм в честь cвятой великомученицы Параскевы Пятницы д. Вербовичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15791/"
      ],
      "name": "Church in honor of the Great Martyr Paraskeva in the village of Verbovichi",
      "id": "by-turaw-4fa4c29b32",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Всех Святых г. Туров",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15804/"
      ],
      "name": "Church of All Saints in Turov",
      "id": "by-turaw-7e1f5bf3a9",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Иоанна Тобольского д. Боровое",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15796/"
      ],
      "name": "Church of John of Tobolsk, Borovoe village",
      "id": "by-turaw-29347455d6",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила аг. Рудня Михалковская",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15765/"
      ],
      "name": "Church of Saint Archangel Michael agrotown of Rudnya Mikhalkovskaya",
      "id": "by-turaw-44ac92b163",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила аг. Слобода",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15808/"
      ],
      "name": "Church of Saint Archangel Michael agrotown of Sloboda",
      "id": "by-turaw-bf21401765",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила д. Дуброва",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15785/"
      ],
      "name": "Church of Saint Archangel Michael in Dubrova",
      "id": "by-turaw-154ff82150",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила д. Лясковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15775/"
      ],
      "name": "Church of Saint Archangel Michael in the village of Lyaskovichi",
      "id": "by-turaw-1c7540bb65",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила д. Люденевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15776/"
      ],
      "name": "Church of Saint Archangel Michael in the village of Lyudenevichi",
      "id": "by-turaw-8f18e23ee0",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила д. Ричев",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15767/"
      ],
      "name": "Church of Saint Archangel Michael in the village of Richev",
      "id": "by-turaw-d5caf1e5d4",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила пос. Червоное,",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15755/"
      ],
      "name": "Church of Saint Archangel Michael settlement of Chervonoye",
      "id": "by-turaw-c729874991",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила д. Рудня Антоновская",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15766/"
      ],
      "name": "Church of Saint Archangel Michael, Rudnya Antonovskaya village",
      "id": "by-turaw-2446709c9d",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Василия Великого д. Белев",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15798/"
      ],
      "name": "Church of Saint Basil the Great village of Belev",
      "id": "by-turaw-af31fe8ce7",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого Архангела Михаила ст. Копцевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15754/"
      ],
      "name": "Church of Saint Michael the Archangel Saint Koptsevichi",
      "id": "by-turaw-20857b553b",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Николая Чудотворца г.п. Брагин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15836/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker Bragin",
      "id": "by-turaw-d3103b831c",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Николая Чудотворца д. Тонеж",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15760/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker in the village of Tonezh",
      "id": "by-turaw-a05c5eec09",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Николая Чудотворца д. Храпков",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15758/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker village Khrapkov",
      "id": "by-turaw-3c223cc1b1",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Святителя Николая Чудотворца г. Калинковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15830/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Kalinkovichi",
      "id": "by-turaw-d0fc12ce1e",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Николая Чудотворца г. Мозырь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15823/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Mozyr",
      "id": "by-turaw-e77a00c5bc",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Николая Чудотворца г. Петриков",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15817/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker, Petrikov",
      "id": "by-turaw-9f5008052b",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого преподобного Сергия Радонежского г. Мозырь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15821/"
      ],
      "name": "Church of Venerable Sergius of Radonezh, Mozyr",
      "id": "by-turaw-e722879f47",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святителя Феодосия Черниговского г. Житковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15816/"
      ],
      "name": "Church of Saint Theodosius of Chernigov, Zhitkovichi",
      "id": "by-turaw-0d350e9410",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Благовещения Пресвятой Богородицы аг. Прудок",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15810/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos agrotown of Prudok",
      "id": "by-turaw-9ebbce0832",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Вознесения Господня г.Петриков",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15818/"
      ],
      "name": "Church of the Ascension of the Lord in Petrikov",
      "id": "by-turaw-af03b87178",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Вознесения Господня д. Новоселки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15771/"
      ],
      "name": "Church of the Ascension of the Lord in the village of Novoselki",
      "id": "by-turaw-0b01c8be3c",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Вознесения Господня г.п.Комарин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15801/"
      ],
      "name": "Church of the Ascension of the Lord Komarin",
      "id": "by-turaw-8ca7e3a7e0",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Успения Пресвятой Богородицы д. Кошевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15782/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Koshevichi",
      "id": "by-turaw-7c5422ca3d",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Успения Пресвятой Богородицы д. Липляны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15777/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Liplyany",
      "id": "by-turaw-1588b362de",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Успения Пресвятой Богородицы д. Милошевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15773/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos in the village of Milosevici",
      "id": "by-turaw-dd8d5076c6",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Успения Пресвятой Богородицы г. Калинковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15829/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos, Kalinkovichi",
      "id": "by-turaw-a21807ebec",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Собора Белорусских святых аг. Криничный",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15812/"
      ],
      "name": "Synaxis of the Belarusian Saints Church in the agrotown of Krinichny",
      "id": "by-turaw-2da14f715f",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Введения во храм Пресвятой Богородицы г. Мозырь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15826/"
      ],
      "name": "Entry of the Most Holy Theotokos into the Temple Church, Mozyr",
      "id": "by-turaw-2f3a0a15c5",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Богоявления д. Симоничи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15762/"
      ],
      "name": "Church of the Epiphany in the village of Simonici",
      "id": "by-turaw-5f352af8b2",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Воздвижения Креста Господня д. Погост",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15769/"
      ],
      "name": "Church of the Exaltation of the Holy Cross in the village of Pogost",
      "id": "by-turaw-784817ef85",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Воздвижения Креста Господня д. Вересница",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15790/"
      ],
      "name": "Church of the Exaltation of the Holy Cross, Veresnitsa village",
      "id": "by-turaw-be5c91baa1",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм священномученика Алексия Лельчицкого д. Сырод",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15761/"
      ],
      "name": "Church of the Hieromartyr Alexy Lelchitsky village of Syrod",
      "id": "by-turaw-fa94ab4fff",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм священномученика Макария Киевского д. Скрыгалов",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15809/"
      ],
      "name": "Church of the Hieromartyr Macarius of Kyiv, Skrygalov village",
      "id": "by-turaw-370b0ce8c5",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого апостола Иоанна Богослова д. Милевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15774/"
      ],
      "name": "Church of the Holy Apostle John the Theologian in the village of Milevichi",
      "id": "by-turaw-c3603bf47f",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святых апостолов Петра и Павла г. п. Озаричи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15803/"
      ],
      "name": "Church of the Holy Apostles Peter and Paul, Ozarichi",
      "id": "by-turaw-52d9687b8d",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого великомученика Георгия Победоносца д. Великие Автюки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15792/"
      ],
      "name": "Church of the Great Martyr George the Victorious in the village of Velikie Avtyuki",
      "id": "by-turaw-3396296ead",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого великомученика Георгия Победоносца д. Боровое",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15797/"
      ],
      "name": "Church of the Great Martyr George the Victorious, Borovoe village",
      "id": "by-turaw-797f4f859e",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого великомученика Георгия Победоносца г.Мозырь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15822/"
      ],
      "name": "Church of the Great Martyr George the Victorious, Mozyr",
      "id": "by-turaw-77181978a4",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святой великомученицы Параскевы Пятницы аг. Малые Автюки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/17009/"
      ],
      "name": "Church of the Great Martyr Paraskeva agrotown of Malye Avtyuki",
      "id": "by-turaw-61f8d2cf54",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святой великомученицы Параскевы Пятницы г. Житковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15815/"
      ],
      "name": "Church of the Great Martyr Paraskeva, Zhitkovichi",
      "id": "by-turaw-9b8eaf1530",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Нерукотворного Образа Господня аг. Заширье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15814/"
      ],
      "name": "Church of the Holy Image of the Lord Not Made by Hands agrotown of Zashirye",
      "id": "by-turaw-b9c7b9aa4f",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Нерукотворного Образа Господня д. Красная Слобода",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15781/"
      ],
      "name": "Church of the Holy Image of the Lord Not Made by Hands, Krasnaya Sloboda village",
      "id": "by-turaw-a5ce48c84a",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Святой Живоначальной Троицы д. Бабуничи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15799/"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Babunichi",
      "id": "by-turaw-d9ba4abb9e",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Святой Живоначальной Троицы д. Глушковичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15788/"
      ],
      "name": "Church of the Holy Life-giving Trinity in the village of Glushkovichi",
      "id": "by-turaw-71101cfb11",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Святой Живоначальной Троицы г. п. Лельчицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15828/"
      ],
      "name": "Church of the Holy Life-giving Trinity, Lelchitsy",
      "id": "by-turaw-363c4c31bf",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Святой Живоначальной Троицы г. Ельск",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15834/"
      ],
      "name": "Church of the Holy Life-giving Trinity, Yelsk",
      "id": "by-turaw-515383c04a",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святых мучениц Веры, Надежды, Любови и матери их Софии г. Мозырь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15820/"
      ],
      "name": "Holy Martyrs Faith, Hope, and Love and Their Mother Sophia Church in Mozyr",
      "id": "by-turaw-de2b5c2514",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого пророка Илии д. Волосовичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15789/"
      ],
      "name": "Church of the Holy Prophet Elijah, Volosovichi",
      "id": "by-turaw-29b93bc629",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм святого преподобного Онуфрия Великого д.Семенча",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15763/"
      ],
      "name": "Church of the Venerable Onuphrius the Great village of Semencha",
      "id": "by-turaw-0337ca9985",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм иконы Божией Матери \"Неупиваемая Чаша\" д. Углы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15759/"
      ],
      "name": "Inexhaustible Chalice Icon of the Theotokos Church in Ugli",
      "id": "by-turaw-d0fe28a5d9",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм иконы Божией Матери \"Всех скорбящих Радость\" г. Мозырь",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15825/"
      ],
      "name": "Church of the Icon of the Theotokos \"Joy of All Who Sorrow\", Mozyr",
      "id": "by-turaw-0bbcb0524b",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм иконы Божией Матери \"Скоропослушница\" д. Козенки",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15813/"
      ],
      "name": "She Who Is Quick to Hear Icon of the Theotokos Church in Kozenki",
      "id": "by-turaw-b86f94a0e9",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм иконы Божией Матери \"Споручница грешных\" г. Мозырь-11 УЖ",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15824/"
      ],
      "name": "Church of the Icon of the Theotokos \"Surety of Sinners\", Mozyr-11 Uzh",
      "id": "by-turaw-27b50a7f4a",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храма иконы Божией Матери \"Умиление\" д. Васьковка",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15793/"
      ],
      "name": "Church of the Icon of the Theotokos \"Tenderness\" in the village of Vaskovka",
      "id": "by-turaw-b22e781594",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм иконы Божией Матери \"Нечаянная Радость\" д. Куритичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15779/"
      ],
      "name": "Church of the Icon of the Theotokos \"Unexpected Joy\", Kuritichi village",
      "id": "by-turaw-2ffecaf212",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Покрова Пресвятой Богородицы д. Приболовичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15768/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos in the village of Pribolovichi",
      "id": "by-turaw-89d2aae144",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Покрова Пресвятой Богородицы г. Хойники",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15833/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos, Khoiniki",
      "id": "by-turaw-741ebb857a",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Покрова Пресвятой Богородицы г. п. Копаткевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15806/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos, Kopatkevichi",
      "id": "by-turaw-a6bbda2a94",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Покрова Пресвятой Богородицы г. п. Октябрьский",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15802/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos, Oktyabrsky",
      "id": "by-turaw-b1cb6d2ee1",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Иверской иконы Божией Матери д. Запесочье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15784/"
      ],
      "name": "Church of the Iveron Icon of the Theotokos in the village of Zapesochye",
      "id": "by-turaw-50e994d0c6",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Казанской иконы Божией Матери Брагинский р-н, д. Маложин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15835/"
      ],
      "name": "Church of the Kazan Icon of the Theotokos Braginsky district, Malozhin village",
      "id": "by-turaw-326bb2ee2a",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Чуда святого Архангела Михаила д. Домановичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15786/"
      ],
      "name": "Church of the Miracle of Saint Michael the Archangel in the village of Domanovichi",
      "id": "by-turaw-6a80ef27bf",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Рождества Христова д. Дзержинск",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15787/"
      ],
      "name": "Church of the Nativity of Christ, Dzerzhinsk",
      "id": "by-turaw-d54b7bccf8",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Рождества Пресвятой Богородицы аг. Юровичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15757/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos agrotown of Jurovichi",
      "id": "by-turaw-f8687137f1",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Рождества Пресвятой Богородицы д. Буйновичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15795/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos in the village of Buinovichi",
      "id": "by-turaw-bcf0845186",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Рождества Пресвятой Богородицы д. Ленин",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15778/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos, Lenin village",
      "id": "by-turaw-1624966375",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Введения во храм Пресвятой Богородицы д. Махновичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15811/"
      ],
      "name": "Entry of the Most Holy Theotokos into the Temple Church in the village of Makhnovichi",
      "id": "by-turaw-2d3b728c2b",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Сретения Господня п. Хвоенск",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15756/"
      ],
      "name": "Church of the Presentation of the Lord, Khvoensk village",
      "id": "by-turaw-eba45da262",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Воскресения Христова д. Букча",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15794/"
      ],
      "name": "Church of the Resurrection of Christ in the village of Bukcha",
      "id": "by-turaw-e36c39e1c4",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Воскресения Христова д. Новое Полесье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15772/"
      ],
      "name": "Church of the Resurrection of Christ in the village of New Polesie",
      "id": "by-turaw-2329619372",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Храм Преображения Господня д.Селец",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15764/"
      ],
      "name": "Church of the Transfiguration of the Lord in the village of Selets",
      "id": "by-turaw-5df7d457aa",
      "country": "BY"
    },
    {
      "parent": "ru-turaw",
      "local": "Приход храма святого Архангела Михаила д. Киров",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://turov.by/eparchia/temples/15783/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel, Kirov",
      "id": "by-turaw-b5db3d66f7",
      "country": "BY"
    }
  ],
  "ru-brest": [
    {
      "parent": "ru-brest",
      "local": "Свято-Рождество-Богородичный женский монастырь на Госпитальном острове Брестской крепости",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Holy Nativity of the Most Holy Theotokos Convent on the Hospital Island of the Brest Fortress",
      "id": "by-brest-5f47908f40",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход в честь святой блаженной Ксении Петербургской в д. Тельмы-1 Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish in honor of the Blessed Xenia of Petersburg in the village of Telmy-1, Brest district of the Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-783a4dc2ad",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход в честь святого праведного Иоанна Русского в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish in honor of the Holy Righteous John the Russian in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-b013d31a0d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход в честь иконы Божия Матери \"Призри на смирение\" в д. Запруды Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Look Upon Humility Icon of the Theotokos Church in Zaprudy, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c84241bf0e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход в честь Малоритской иконы Божией Матери г. Малорита Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish in honor of the Malorita Icon of the Theotokos in the city of Malorita of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4ba490f5cd",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход кафедрального собора преподобного Симеона Столпника в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Cathedral of Venerable Simeon the Stylite in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a49267c5c1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход кафедрального собора святого благоверного князя Александра Невского в г. Кобрине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Cathedral of the Holy Right-believing Prince Alexander Nevsky in Kobrin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-0d12209892",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход собора Воскресения Христова в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Cathedral of the Resurrection of Christ in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7d6333598f",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь святителя Спиридона Тримифунтского чудотворца в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of Saint Spyridon of Tremithus Church in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e86122d634",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь святого священномученика Харлампия в д. Могилевцы Пружанского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Hieromartyr Charalampus Church in Mahilyowtsy, Pruzhany district, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-b0b41ae29d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь преподобномученика Макария, игумена Каменецкого в г. Каменец Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church in honor of the Venerable Martyr Macarius, Abbot of Kamenets in the city of Kamenets of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-5e9f041058",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь Владимирской иконы Божией Матери д. Тюхиничи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church in honor of the Vladimir Icon of the Theotokos in the village of Tyukhinichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-042d2f08af",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь Жировичской иконы Божией Матери в агрогородке Турна Большая (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church in honor of the Zhirovichi Icon of the Theotokos in the agrotown of Turna Bolshaya (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-32f0234dcb",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Всех Святых д. Старое Село Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of All Saints in the village of Staroye Selo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-63a82d26d9",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой блаженной Валентины Минской в агрогородке Ракитница Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Blessed Valentina of Minsk Church in the agrotown of Rakitnitsa, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8215cb7bf1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Кирилла Туровского в г. Жабинка Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Cyril of Turov in Zhabinka, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-41e07b22b0",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобной Евфросинии Полоцкой в г. Дрогичине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Euphrosyne of Polotsk in the city of Drogichin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d687392236",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Луки в г.п. Домачево Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Luke the Apostle in the town of Domachevo, Brest district, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4430fc65cf",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой равноапостольной Марии Магдалины в агрогородке Сигневичи Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Mary Magdalene Equal-to-the-Apostles in the agrotown of Signevichi, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-148d5c347a",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в г. Берёзе Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in Bereza of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-143f297491",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в агрогородке Осовцы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the agrotown of Osovtsy, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-95eb7fc0f2",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в агрогородке Остромечево Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the agrotown of Ostromechevo of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-3f9bbdf3a1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в агрогородке Рясна Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the agrotown of Ryasna, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d8e3d8a1cd",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в агрогородке Степанки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the agrotown of Stepanki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8a14aeddbf",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в д. Бородичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Borodich, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8034c03382",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в д. Черск Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Chersk, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4870c00a9d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в д. Еремичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Eremichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-1362f842d2",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в д. Масевичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Masevichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6a59d809b0",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в д. Токари Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Tokari, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-920e04cc83",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-065fd58ec8",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в г. Кобрине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Kobrin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f0dce3bc26",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в г. Малорита Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Malorita, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-380f091e02",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в г. Пружаны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in Pruzhany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-fbba4c7fdc",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в агрогородке Озяты Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the agrotown of Ozyaty of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d3116d7ccb",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в агрогородке Первомайская Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the agrotown of Pervomaiskaya, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7bf3495625",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в агрогородке Смоляница Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the agrotown of Smolyanitsa of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-37cc990671",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в агрогородке Закозель Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the agrotown of Zakozel of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8447eb393c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в г.п. Шерешево Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the town of Shereshevo of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-634bab2476",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Большие Сехновичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Bolshiye Sekhnovichi of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2d90a6a28b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Черняково Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Chernyakovo, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7e672b9b6f",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Люта Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Lyuta, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-44df051006",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Радость Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Radost, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-606540ece0",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Верхолесье Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Verkholesye, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-878181e6e1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Верховичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Verkhovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-cd8cdf273a",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Волчин Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Volchin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8f3b5d0aae",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Замшаны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Zamshany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-3b5395cd14",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Николая Чудотворца в д. Засимовичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Zasimovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2259396a0f",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Онуфрия Великого в агрогородке Спорово Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Onuphrius the Great in the agrotown of Sporovo, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6b00103814",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Онуфрия Великого в агрогородке Ставы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Onuphrius the Great in the agrotown of Stavy of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-296a914a65",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Онуфрия Великого в д. Борщево Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Onuphrius the Great in the village of Borshchevo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2d1c3fb736",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Серафима Саровского в г. Белоозёрске Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov in Beloozersk, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4a41c8c36c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Серафима Саровского в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8e3eb4fa15",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Серафима Саровского в агрогородке Ореховский Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Seraphim of Sarov in the agrotown of Orekhovsky, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-cabc3f0bd3",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Сергия Радонежского в агрогородке Клепачи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Sergius of Radonezh in the agrotown of Klepachi of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c3066b9f6e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Симеона Столпника в г. Каменец Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Simeon the Stylite in Kamenets, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d7a22355ce",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма преподобного Симеона Столпника в агрогородке Малеч Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Venerable Simeon the Stylite in the agrotown of Malech, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f229a25425",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святителя Тихона, патриарха Московского и всея Руси в д. Деревная Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Tikhon, Patriarch of Moscow and All Rus' in the village of Derevnaya, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e17f686932",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма апостола Фомы в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Apostle Thomas in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-b4bd73ec07",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Вознесения Господня в д. Огородники Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Ogorodniki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ab982cc761",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Вознесения Господня в д. Вельямовичи Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Velyamovichi, Brest district, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2c988ed29b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в агрогородке Гвозница Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the agrotown of Gvoznitsa of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-116a8e4eea",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в агрогородке Липники Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the agrotown of Lipniki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f288516826",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в агрогородке Селец Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the agrotown of Selets, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f37df87b91",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Бульково Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Bulkovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f37319c40c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Лосинцы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Losintsy of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-3823ad45d2",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Паниквы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Panikvy, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-92a88d09e9",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Перковичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Perkovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-47bd57449c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Речица Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Rechitsa of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-71ca7b4a36",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Тевли Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Tevli, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c945873f76",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Успения Пресвятой Богородицы в д. Шишово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in Shishovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6dde70a317",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в агрогородке Сухополь Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the agrotown of Sukhopol, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6c0411c7f3",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в д. Берёза Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Bereza, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6523b3df20",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в д. Матвеевичи Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Matveevichi, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-b96725a290",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в д. Омеленец Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Omelenets, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d54feab971",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в д. Оранчицы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Oranchitsy, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a50378e835",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в д. Зельзин Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Zelzin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-995f6a3484",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в г. Высокое Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in Vysokoye, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d203f541cb",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма великомученицы Параскевы Пятницы в д. Николаево Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the village of Nikolaevo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e0302146f5",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Андрея Первозванного в д. Пашуки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle Andrew the First-Called in the village of Pashuki, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ad39e8606c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Иоанна Богослова в агрогородке Черни Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the agrotown of Cherni, Brest region of the Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-74b60c9774",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Иоанна Богослова в агрогородке Киселёвцы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the agrotown of Kiselyovtsy of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e1cb147761",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Иоанна Богослова в агрогородке Стригинь Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the agrotown of Strigin, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-262c025f3a",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Иоанна Богослова в д. Черевачицы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the village of Cherevachitsy, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f5ac8824ac",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Иоанна Богослова в д. Корчицы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the village of Korchitsa, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-bd67fdde04",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Иоанна Богослова в д. Приборово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle John the Theologian in the village of Priborovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f6fb7c1791",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Луки в агрогородке Лука Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostle Luke in the agrotown of Luke of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ad2bc97809",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в г. Кобрине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in Kobrin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c4096a874d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в г. Берёзе Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the city of Bereza of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-11605bb6f1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в г.п. Ружаны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the town of Ruzhany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-de18a7c46f",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в д. Городище Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Gorodishche of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-641ad47b17",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в д. Малые Косичи Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Malye Kosichi, Brest region, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d4f8572ea7",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в д. Мокрое Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Mokroe, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-180b26fe7e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых апостолов Петра и Павла в д. Сварынь Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Svaryn, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-fbf832c810",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой блаженной Матроны Московской в агрогородке Большие Радваничи Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Blessed Matrona of Moscow in the agrotown of Bolshie Radvanichi, Brest region, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-01fcb50bac",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого благоверного князя Александра Невского в г. Пружаны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky in Pruzhany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-554c31fd5c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого благоверного князя Александра Невского в д. Близная Пружанского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky in the village of Bliznaya, Pruzhany district, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f444072cd6",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого равноапостольного князя Владимира в агрогородке Мухавец Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Prince Vladimir in the agrotown of Mukhavets, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f2f24902e3",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого равноапостольного князя Владимира в агрогородке Стригово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Prince Vladimir in the agrotown of Strigovo of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a5d53699ea",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого равноапостольного князя Владимира в агрогородке Ворониловичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Prince Vladimir in the agrotown of Voronilovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ce9e07adb1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого равноапостольного князя Владимира в д.Бронная Гора Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Prince Vladimir in the village of Bronnaya Gora, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f89a6cfe8b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого равноапостольного князя Владимира в д. Чижевщина Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Prince Vladimir in the village of Chizhevshchina of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-07c6431ce0",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых равноапостольных царя Константина и царицы Елены в д. Завершье Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Tsar Constantine and Queen Helena in the village of Zavershye of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a95a798aff",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой великомученицы Варвары в д. Суходол Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Barbara in the village of Sukhodol, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-95e5c3689e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Димитрия Солунского в д. Леликово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Demetrius of Thessalonica in the village of Lelikovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-46a1de0148",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Димитрия Солунского в д. Рогозно Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Demetrius of Thessalonica in the village of Rogozno, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e4590983ec",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Георгия Победоносца в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-848377dedf",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Георгия Победоносца в г. Кобрине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in Kobrin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-65cc0e589d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Георгия Победоносца в агрогородке Каменюки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the agrotown of Kamenyuki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-290148f430",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Георгия Победоносца в д. Воловель Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Volovel of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e869ded845",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого великомученика Никиты в г. Жабинка Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Nikita in Zhabinka, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6aed0b8ffd",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой великомученицы Параскевы Пятницы в агрогородке Чернавчицы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the agrotown of Chernavchitsy of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-1a99521345",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой великомученицы Параскевы Пятницы в агрогородке Дивин Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the agrotown of Divin of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-684ab1647e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой великомученицы Параскевы Пятницы в агрогородке Орехово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the agrotown of Orekhovo of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-5cf674cb15",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой великомученицы Параскевы Пятницы в д. Сычи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the village of Sychi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7396e7d114",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a012674f40",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в агрогородке Бездеж Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the agrotown of Bezdezh, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-935ab75db1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в агрогородке Междулесье Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the agrotown of Mezhdlesie, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c33f55463e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в агрогородке Пески Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the agrotown of Peski, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-19d220910a",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в агрогородке Войская Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the agrotown of Voyskaya, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f3e16fa506",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в д. Козище Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Kozische of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-5a7b5bb7fb",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Святой Живоначальной Троицы в д. Зёлово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Zelovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7118c00883",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых мучениц Веры, Надежды, Любови и матери их Софии в агрогородке Беловежский Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Holy Martyrs Faith, Hope, and Love and Their Mother Sophia Church in the agrotown of Belovezhsky, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-23464d4b8f",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых мучениц Веры, Надежды, Любови и матери их Софии в агрогородке Страдечь Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Holy Martyrs Faith, Hope, and Love and Their Mother Sophia Church in the agrotown of Stradech, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-1deee9340e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых благоверных князей Петра и Февронии Муромских в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Holy Right-believing Prince Peter and Princess Fevronia of Murom Church in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ec90fe6848",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого пророка Илии в агрогородке Великорита Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the agrotown of Velikorita of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-38f34debc3",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого пророка Илии в д. Бельск Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Belsk, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-79ea1e6c6d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого пророка Илии д. Дубок Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Dubok, Brest district, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4c3178fa46",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого пророка Иоанна Предтечи в агрогородке Хидры Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Prophet John the Baptist in the agrotown of Khidra of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ae73cb2447",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого пророка Иоанна Предтечи в агрогородке Соколово Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Prophet John the Baptist in the agrotown of Sokolovo, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a1d9dae59e",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых преподобных Александра Пересвета и Андрея Осляби в в/ч 2187 в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Holy Venerables Alexander Peresvet and Andrei Oslyabya Church at Military Unit 2187 in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-de03cdc7a1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого праведного Иоанна Кормянского в д. Глинянки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Righteous John of Kormyansky in the village of Glinyanki, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-3728781b08",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святых Царственных Страстотерпцев в д. Хрисо Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Holy Royal Passion-Bearers in the village of Khriso, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7a42b49f55",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой преподобной Параскевы Сербской в д. Болота Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Venerable Paraskeva of Serbia in the village of Bolota, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f1bc4aee38",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святой преподобной Параскевы Сербской в д. Збироги Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Venerable Paraskeva of Serbia in the village of Zbirogi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-528af4b429",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Пресвятой Богородицы \"Спорительница хлебов\" в агрогородке Хорева Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Multiplier of Wheat Icon of the Theotokos Church in the agrotown of Khorev, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2d4102830b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Всецарица\" в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Queen of All\" in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d4199bb58d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Избавительница\" в агрогородке Пески Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Deliverer\" in the agrotown of Peski, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-769c8b3b09",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Неупиваемая Чаша\" в агрогородке Ленинский Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Inexhaustible Chalice\" in the agrotown of Leninsky, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-37b7eea28c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Неупиваемая Чаша\" в д. Камень Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Inexhaustible Chalice\" in the village of Kamen of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-b0ee2459ef",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих Радость\" в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Joy of All Who Sorrow\" in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-23549f5856",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Нечаянная Радость\" в д. Новые Засимовичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Unexpected Joy\" in the village of Novye Zasimovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-206bf89382",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Буховичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Bukhovichi of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e19f1962da",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Детковичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Detkovichi of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-419838fa9a",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Хомск Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Khomsk of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e17e1f59ba",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Оса Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Osa of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-cfa953426b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Радостово Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Radostovo of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-9ac784d464",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Ревятичи Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Revyatichi, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-488fad56c6",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Рудники Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Rudniki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-57e86b45cd",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Томашовка Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Tomashovka of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-77fa88bbed",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в агрогородке Видомля Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the agrotown of Vidomlya of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4f3ccbe244",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Чемери Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Chemeri, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4de4e1506c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Городечно Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Gorodechno, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ae2ccdfe09",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Каменица Жировецкая Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Kamenitsa Zhirovetskaya, Brest district of the Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ec5b9bd400",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Хабовичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Khabovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-61edfa844d",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Малые Щитники Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Malye Shchitniki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-3ef54cdbe9",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Октябрь Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Oktyabr, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2612a5ab89",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Орепичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Orepichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-68ed49db5b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Покры Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Pokry of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-4dc8f2d450",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Прилуки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Priluki, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e2c9e89738",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в д. Збураж Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Zburazh, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-466f0feca6",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Покрова Пресвятой Богородицы в г. Жабинка Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in Zhabinka, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-745b2afaba",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Казанской иконы Божией Матери в агрогородке Мурава Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos in the agrotown of Murava, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-6e7740f921",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Казанской иконы Божией Матери в д. Толково Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos in the village of Tolkovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ceb4e389ef",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Луковской иконы Божией Матери агрогородка Луково Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Lukovo Icon of the Theotokos in the agrotown of Lukovo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-bc703fc44b",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Христова в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8187196340",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Христова в г. Кобрине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity in Kobrin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e6964e53bb",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Иоанна Предтечи в агрогородке Матеевичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b6%d0%b0%d0%b1%d0%b8%d0%bd%d0%ba%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of John the Baptist in the agrotown of Mateevichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e9f07cad72",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7c316f9882",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в агрогородке Черняны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the agrotown of Chernyany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-1aaedc627f",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в агрогородке Дивин Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the agrotown of Divin of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-dab4e5c3a0",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в агрогородке Ляховцы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the agrotown of Lyakhovtsy of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-658e37d264",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в агрогородке Лысково Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the agrotown of Lyskovo of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c3b80d2774",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в агрогородке Мокраны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the agrotown of Mokrany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-874086b567",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в агрогородке Повитье Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the agrotown of Povitye of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-5a0842a137",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Доропеевичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Doropeevichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-7a787193dc",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Индычи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Indychi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-3731d45b45",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Ляховичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Lyakhovichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ce2bb0caca",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Субботы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Saturday, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-29ee684395",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Щебрин Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Shchebrin, Brest district, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-9ec7bc7201",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Вавуличи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Vavulichi, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-710340c7b5",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рождества Пресвятой Богородицы в д. Здитово Берёзовского района Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d0%b5%d1%80%d0%b5%d0%b7%d0%be%d0%b2%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Zditovo, Berezovsky district of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-a49f8fc417",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Введения во храм Пресвятой Богородицы в г. Кобрине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Entry of the Most Holy Theotokos into the Temple Church in Kobrin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-0e0a0473a3",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Сретения Господня в г. Дрогичине Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Presentation of the Lord in the city of Drogichin, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-90773b8bc8",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воскресения Христова в г.п. Антополь Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Resurrection of Christ in the town of Antopol of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-9331c86588",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Рожковской иконы Божией Матери в д. Рожковка Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Rozhkovskaya Icon of the Theotokos in the village of Rozhkovka of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2378352ef0",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Трех Cвятителей в д. Радеж Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Three Saints in the village of Radezh, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-c797105502",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Тихвинской иконы Божией Матери в г. Бресте Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Tikhvin Icon of the Theotokos in Brest, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-63abd733a2",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в г. Пружаны Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in Pruzhany, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d610bff171",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в агрогородке Новая Попина Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the agrotown of Novaya Popina of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8de37e5a72",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в агрогородке Олтуш Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the agrotown of Oltush, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-51bde953f9",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в д. Теребунь Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Terebun, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f3e36247c6",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в д. Тростяница Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Trostyanitsa of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f44d31da6a",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход гарнизонного храма святителя Николая Чудотворца в Брестской крепости Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b3%d0%be%d1%80%d0%be%d0%b4%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the garrison Church of Saint Nicholas the Wonderworker in the Brest Fortress of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-83c44ba7cf",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход иконы Божией Матери \"Взыскание погибших\" в д. Клейники Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Icon of the Theotokos \"Seeking the Lost\" in the village of Kleiniki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-1d6f8167bf",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Спасо-Преображенский мужской монастырь д. Хмелево",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Transfiguration of the Lord Monastery in Khmelevo",
      "id": "by-brest-789d91a6c1",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Спасский женский монастырь г. Кобрина",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Savior Convent in Kobrin",
      "id": "by-brest-7f10f40b08",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Свято-Афанасьевский мужской монастырь г. Бреста",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Saint Athanasius Monastery in Brest",
      "id": "by-brest-2ce4b61a7c",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь иконы Пресвятой Богородицы \"Споручница грешных\" дер. Щерчево Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bf%d1%80%d1%83%d0%b6%d0%b0%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Surety of Sinners Icon of the Theotokos Church in Shcherchevo, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-ede2701d46",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма в честь Третьего обретения главы Иоанна Предтечи в агрогородке Медно Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church in honor of the Third Finding of the Head of John the Baptist in the agrotown of Medno-Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-d17c845163",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого апостола Марка в агрогородке Новосёлки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Mark the Apostle in the agrotown of Novoselki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e95e2b7d12",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма святого Архангела Михаила в агрогородке Новосёлки Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the agrotown of Novoselki of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-563bbbabda",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Благовещения Пресвятой Богородицы в агрогородке Большие Мотыкалы Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Annunciation of the Most Holy Theotokos in the agrotown of Bolshie Motykaly, Brest district, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-0cc581da61",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Вознесения Господня в агрогородке Городец Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%be%d0%b1%d1%80%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the agrotown of Gorodets of the Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-2c9e6d4437",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Богоявления в агрогородке Именин Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Epiphany in the agrotown of Imenin of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e43300d524",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в агрогородке Головчицы Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the agrotown of Golovchitsy of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-37ccce4af6",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Воздвижения Креста Господня в агрогородке Вистычи Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the agrotown of Vistychi, Brest region, Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-e86d47e6ff",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма иконы Божией Матери \"Знамение\" в аг. Знаменка Брестского района Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Sign Icon of the Theotokos Church in the agrotown of Znamenka, Brest district, Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-74fc2a15e9",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в агрогородке Брашевичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b4%d1%80%d0%be%d0%b3%d0%b8%d1%87%d0%b8%d0%bd%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the agrotown of Brashevichi of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-14de00a367",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в агрогородке Дмитровичи Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%ba%d0%b0%d0%bc%d0%b5%d0%bd%d0%b5%d1%86%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the agrotown of Dmitrovichi of the Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-bba3b18bb4",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в агрогородке Хотислав Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%bc%d0%b0%d0%bb%d0%be%d1%80%d0%b8%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the agrotown of Khotislav of the Brest diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-f33519aeed",
      "country": "BY"
    },
    {
      "parent": "ru-brest",
      "local": "Приход храма Преображения Господня в агрогородке Медно Брестской епархии Белорусской Православной Церкви (Белорусского Экзархата Московского Патриархата)",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pravbrest.by/%d0%b1%d1%80%d0%b5%d1%81%d1%82%d1%81%d0%ba%d0%be%d0%b5-%d1%80%d0%b0%d0%b9%d0%be%d0%bd%d0%bd%d0%be%d0%b5-%d0%b1%d0%bb%d0%b0%d0%b3%d0%be%d1%87%d0%b8%d0%bd%d0%b8%d0%b5/"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the agrotown of Medno-Brest Diocese of the Belarusian Orthodox Church (Belarusian Exarchate of the Moscow Patriarchate)",
      "id": "by-brest-8acf6d2425",
      "country": "BY"
    }
  ],
  "ru-hrodna": [
    {
      "parent": "ru-hrodna",
      "local": "Приход храма в честь иконы Божией Матери \"Всецарица\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/vsefarifa/"
      ],
      "name": "Parish of the Church in honor of the Icon of the Theotokos \"Queen of All\"",
      "id": "by-hrodna-6452cd2d8d",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма в честь Минской иконы Божией Матери",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-v-chest-minskoi-ikony-bozhiei-materi/"
      ],
      "name": "Parish of the Church in honor of the Minsk Icon of the Theotokos",
      "id": "by-hrodna-89ead344be",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Кафедральный собор апостолов Петра и Павла",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/kafedral-nyi-sobor-apostolov-petra-i-pavla/"
      ],
      "name": "Cathedral of the Apostles Peter and Paul",
      "id": "by-hrodna-79eb1af699",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Кафедральный собор Покрова Пресвятой Богородицы",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/kafedral-nyi-sobor-pokrov-presvyatoi-bogorodify/"
      ],
      "name": "Cathedral of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-2e38c54d52",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Часовня в честь благоверного великого князя Александра Невского",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/aleksandro-nevskaya-chasovnya/"
      ],
      "name": "Chapel in honor of the Right-believing Grand Prince Alexander Nevsky",
      "id": "by-hrodna-581de1afc4",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Часовня в честь Покрова Пресвятой Богородицы",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/chasovnya-pokrova-presvyatoi-bogorodify-deshkovichi/"
      ],
      "name": "Chapel in honor of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-8887761203",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм в честь иконы Божией Матери \"Скоропослушница\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/skoroposlushnifa/"
      ],
      "name": "She Who Is Quick to Hear Icon of the Theotokos Church",
      "id": "by-hrodna-beb73a20ba",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм равноапостольного князя Владимира",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-ravnoapostol-nogo-knyazya-vladimira/"
      ],
      "name": "Church of Equal-to-the-Apostles Prince Vladimir",
      "id": "by-hrodna-bdac893f3d",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм праведной Анны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pravednoi-anny-zadvoryane/"
      ],
      "name": "Church of Righteous Anna",
      "id": "by-hrodna-0f852e77d3",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм праведной Анны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pravednoi-anny/"
      ],
      "name": "Church of Righteous Anna",
      "id": "by-hrodna-e534c2a474",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм праведного Иоанна Кормянского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pravednogo-ioanna-kormyanskogo/"
      ],
      "name": "Church of Righteous John of Kormyansk",
      "id": "by-hrodna-aebfb4a3b7",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святого преподобного Антония Киево-Печерского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatogo-prepodobnogo-antoniya-kievo-pecherskogo-d-dobrosel-fy/"
      ],
      "name": "Church of Venerable Anthony of Kiev-Pechersk",
      "id": "by-hrodna-d4d504d320",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобной Евфросинии Полоцкой",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnoi-evfrosinii-polofkoi-radun/"
      ],
      "name": "Church of Venerable Euphrosyne of Polotsk",
      "id": "by-hrodna-220772b625",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобной Евфросинии Полоцкой",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnoi-evfrosinii-polofkoi/"
      ],
      "name": "Church of Venerable Euphrosyne of Polotsk",
      "id": "by-hrodna-2fd6cfaf64",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Луки, архиепископа Симферопольского и Крымского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-luki-krymskogo/"
      ],
      "name": "Church of Saint Luke, Archbishop of Simferopol and Crimea",
      "id": "by-hrodna-f3618d0a6f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобной Марфы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnoi-marfy-grodno/"
      ],
      "name": "Church of Venerable Martha",
      "id": "by-hrodna-75ba251685",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобного Мартина Туровского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnogo-martina-turovskogo-zheludok/"
      ],
      "name": "Church of Venerable Martin of Turov",
      "id": "by-hrodna-f3e049371a",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-samuilovichi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-00f48aa297",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-0aca2e29c9",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-volkovysk/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-0f627c0469",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-lasha/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-131e17e5f4",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-dyatlovichi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-311cdba35f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-tureisk/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-5cccaa6c75",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-b-berestovifa/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-80f6acea9b",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-naroshi/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-8702f0f79a",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-peski/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-c86035d85f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatitelya-nikolaya-chudotvorfa-dubno/"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-hrodna-ffe028112c",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобной Параскевы Сербской",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnoi-paraskevy-serbskoi-sventifa/"
      ],
      "name": "Church of Venerable Paraskeva of Serbia",
      "id": "by-hrodna-baa4c225a3",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобного Серафима Саровского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnogo-serafima-sarovskogo/"
      ],
      "name": "Church of Venerable Seraphim of Sarov",
      "id": "by-hrodna-fa9478cf0d",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Благовещения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-blagovesheniya-presvyatoi-bogorodify-volkovysk/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos",
      "id": "by-hrodna-312cbb3235",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Благовещения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-blagovesheniya-presvyatoi-bogorodify/"
      ],
      "name": "Church of the Annunciation of the Most Holy Theotokos",
      "id": "by-hrodna-fe3fc4eeb2",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм апостола Иоанна Богослова",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-apostola-ioanna-bogoslova/"
      ],
      "name": "Church of the Apostle John the Theologian",
      "id": "by-hrodna-97e10d1395",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-apostolov-petra-i-pavla-gornostaevichi/"
      ],
      "name": "Church of the Apostles Peter and Paul",
      "id": "by-hrodna-2d210e81d4",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-apostolov-petra-i-pavla-volpa/"
      ],
      "name": "Church of the Apostles Peter and Paul",
      "id": "by-hrodna-8d0a7d37a7",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-arkhangela-mikhaila-izabelin/"
      ],
      "name": "Church of the Archangel Michael",
      "id": "by-hrodna-0b5fa3380e",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-arkhangela-mikhaila-synkovichi/"
      ],
      "name": "Church of the Archangel Michael",
      "id": "by-hrodna-2503e3872f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-arkhangela-mikhaila-novyi-dvor/"
      ],
      "name": "Church of the Archangel Michael",
      "id": "by-hrodna-4547235ee0",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-arkhangela-mikhaila-shuchin/"
      ],
      "name": "Church of the Archangel Michael",
      "id": "by-hrodna-7fe68b7df1",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-arkhangela-mikhaila-ostrovo/"
      ],
      "name": "Church of the Archangel Michael",
      "id": "by-hrodna-860571cfa2",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-arkhangela-mikhaila/"
      ],
      "name": "Church of the Archangel Michael",
      "id": "by-hrodna-f11da73156",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-uspeniya-presvyatoi-bogorodify-dobrovolya/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-hrodna-492bf74ff3",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-uspeniya-presvyatoi-bogorodify-gorbachi/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-hrodna-5c5b0114e7",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-uspeniya-presvyatoi-bogorodify-gol-ni/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-hrodna-8f0a21d3ff",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-uspeniya-presvyatoi-bogorodify-shnipki/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-hrodna-eea4cac3a4",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-uspeniya-presvyatoi-bogorodify/"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-hrodna-f3e62f398d",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Августовской иконы Божией Матери",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-avgustovskoi-ikony-bozhiei-materi/"
      ],
      "name": "Church of the August Icon of the Theotokos",
      "id": "by-hrodna-e7d55efa98",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм благоверного князя Александра Невского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-blagovernogo-knyazya-aleksandra-nevskogo-voronovo/"
      ],
      "name": "Church of the Right-believing Prince Alexander Nevsky",
      "id": "by-hrodna-24aa4f2969",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм благоверного князя Александра Невского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-blagovernogo-knyazya-aleksandra-nevskogo-vertelishki/"
      ],
      "name": "Church of the Right-believing Prince Alexander Nevsky",
      "id": "by-hrodna-7bdbdc1e1a",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм благоверного князя Александра Невского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-blagovernogo-knyazya-aleksandra-nevskogo/"
      ],
      "name": "Church of the Right-believing Prince Alexander Nevsky",
      "id": "by-hrodna-7de43f8fdf",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Собора Белорусских святых",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-sobora-belorusskikh-svyatykh/"
      ],
      "name": "Church of the Synaxis of the Belarusian Saints",
      "id": "by-hrodna-0c550f0d9a",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храма Собора Белорусских святых - Архиерейское подворье",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/svbs/"
      ],
      "name": "Church of the Synaxis of the Belarusian Saints - Bishop's Compound",
      "id": "by-hrodna-24aa2d7212",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Введения во храм Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vvedeniya-vo-khram-presvyatoi-bogorodify/"
      ],
      "name": "Entry of the Most Holy Theotokos into the Temple Church",
      "id": "by-hrodna-bdfed954bc",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vozdvizheniya-kresta-gospodnya-kolontai/"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-hrodna-00a9b9abf7",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vozdvizheniya-kresta-gospodnya-golovachi/"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-hrodna-4671ac1705",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vozdvizheniya-kresta-gospodnya/"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-hrodna-585291984e",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vozdvizheniya-kresta-gospodnya-grifevichi/"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-hrodna-ad4ec22392",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vozdvizheniya-kresta-gospodnya-svisloch/"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-hrodna-d60bd4b8f9",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученика Димитрия Солунского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenika-dimitriya-solunskogo/"
      ],
      "name": "Church of the Great Martyr Demetrius of Thessalonica",
      "id": "by-hrodna-72eb4a3f72",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученика Георгия Победоносца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenika-georgiya-pobedonosfa-krasnosel-skii/"
      ],
      "name": "Church of the Great Martyr George the Victorious",
      "id": "by-hrodna-6012ee1743",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученика Георгия Победоносца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenika-georgiya-pobedonosfa-golynka/"
      ],
      "name": "Church of the Great Martyr George the Victorious",
      "id": "by-hrodna-79da6f9c77",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученика Георгия Победоносца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenika-georgiya-pobedonosfa/"
      ],
      "name": "Church of the Great Martyr George the Victorious",
      "id": "by-hrodna-7b52b52c7c",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученика Георгия Победоносца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenika-georgiya-pobedonosfa-slovatichi/"
      ],
      "name": "Church of the Great Martyr George the Victorious",
      "id": "by-hrodna-d264ed1977",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученицы Параскевы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenify-paraskevy/"
      ],
      "name": "Church of the Great Martyr Paraskeva",
      "id": "by-hrodna-019a9d5bda",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм великомученицы Параскевы Пятницы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-velikomuchenify-paraskevy-pyatnify-bershty/"
      ],
      "name": "Church of the Great Martyr Paraskeva",
      "id": "by-hrodna-39a2ede65f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Святой Живоначальной Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatoi-zhivonachal-noi-troify-porozovo/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-hrodna-541419f35e",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Святой Живоначальной Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatoi-zhivonachal-noi-troify-podorosk/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-hrodna-63d47ce52f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Святой Живоначальной Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatoi-zhivonachal-noi-troify-kurilovichi/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-hrodna-83150f61a7",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Святой Живоначальной Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatoi-zhivonachal-noi-troify/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-hrodna-b032821723",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Святой Живоначальной Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatoi-zhivonachal-noi-troify-zel-va/"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-hrodna-f8d7327bda",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Святого Духа",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-svyatogo-dukha/"
      ],
      "name": "Church of the Holy Spirit",
      "id": "by-hrodna-87b9455815",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм иконы Божией Матери \"Всех скорбящих Радость\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-ikony-bozhiei-materi-vsekh-skorbyashikh-radost/"
      ],
      "name": "Church of the Icon of the Theotokos \"Joy of All Who Sorrow\"",
      "id": "by-hrodna-98e4cf474a",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-belavichi/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-2ce64e43ad",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-volkovysk/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-51904c7ba6",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-orlya/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-568816e534",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-ostrovskii/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-63d94f55e3",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-olekshify/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-ac9c4ca7b0",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-c40e123f32",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-v-d-mil-kovshina/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-d08b0eb500",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-pervomaiskaya/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-d1521e480c",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-pokrova-presvyatoi-bogorodify-yatvesk/"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-hrodna-e34e2982f9",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Казанской иконы Божией Матери",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-kazanskoi-ikony-bozhiei-materi/"
      ],
      "name": "Church of the Kazan Icon of the Theotokos",
      "id": "by-hrodna-f46cc8f4fb",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм мучеников благоверных князей Бориса и Глеба (Коложская церковь)",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-strastoterpfev-blagovernykh-knyazei-borisa-i-gleba-kolozhskaya-ferkov/"
      ],
      "name": "Church of the Martyrs of the Right-believing Princes Boris and Gleb (Kolozha Church)",
      "id": "by-hrodna-34cd752c78",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Христова",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-khristova-rozhanka/"
      ],
      "name": "Church of the Nativity",
      "id": "by-hrodna-fba7c9afb0",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Иоанна Предтечи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-ioanna-predtechi-shenef/"
      ],
      "name": "Church of the Nativity of John the Baptist",
      "id": "by-hrodna-12ffcaf788",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Иоанна Предтечи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-ioanna-predtechi-lunno/"
      ],
      "name": "Church of the Nativity of John the Baptist",
      "id": "by-hrodna-3283167dfb",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-gudevichi/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-02faa79240",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-rakovichi/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-15e35c8925",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-svisloch/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-2a20995a66",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-murovanka/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-2ba1a4b271",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-cherlena/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-3b1f7e0d43",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-selyuki/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-5cd54fc9a3",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-massolyany/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-9271a19fb9",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-rozhdestva-presvyatoi-bogorodify-pafevichi/"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-hrodna-a715c63c1d",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм новомучеников и исповедников земли Белорусской",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-novomuchenikov-i-ispovednikov-zemli-belorusskoi-v-g-skidele/"
      ],
      "name": "Church of the New Martyrs and Confessors of the Belarusian Land",
      "id": "by-hrodna-7984821398",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм пророка Илии",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-proroka-ilii/"
      ],
      "name": "Church of the Prophet Elijah",
      "id": "by-hrodna-4d137df4ee",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Преображения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-preobrazheniya-gospodnya-volpa/"
      ],
      "name": "Church of the Transfiguration of the Lord",
      "id": "by-hrodna-2c387a2ec0",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Преображения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-preobrazheniya-gospodnya-komotovo/"
      ],
      "name": "Church of the Transfiguration of the Lord",
      "id": "by-hrodna-2f6784a804",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Преображения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-preobrazheniya-gospodnya-ostrino/"
      ],
      "name": "Church of the Transfiguration of the Lord",
      "id": "by-hrodna-4d8084ebb3",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Преображения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-preobrazheniya-gospodnya-derechin/"
      ],
      "name": "Church of the Transfiguration of the Lord",
      "id": "by-hrodna-65f37a7499",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Преображения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-preobrazheniya-gospodnya/"
      ],
      "name": "Church of the Transfiguration of the Lord",
      "id": "by-hrodna-ef4bc5bbfe",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм преподобномученика Серафима, архимандрита Жировичского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-prepodobnomuchenika-serafima-matveevfy/"
      ],
      "name": "Church of the Venerable Martyr Seraphim, Archimandrite of Zhirovichi",
      "id": "by-hrodna-c1b7ceb9be",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Храм Виленских мучеников Антония, Иоанна и Евстафия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/khram-vilenskikh-muchenikov/"
      ],
      "name": "Church of the Vilna Martyrs Anthony, John and Eustathius",
      "id": "by-hrodna-f2171e5ede",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Домовый храм преподобной Параскевы Сербской",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/domovyi-khram-prepodobnoi-paraskevy-serbskoi/"
      ],
      "name": "House Church of Venerable Paraskeva of Serbia",
      "id": "by-hrodna-46f2ed3f33",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Домовая церковь святителя Кирилла Туровского",
      "rank": "House Church",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/domovaya-ferkov-svyatitelya-kirilla-turovskogo/"
      ],
      "name": "House Church of Saint Cyril of Turov",
      "id": "by-hrodna-9dc7d7086f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма равноапостольных Кирилла и Мефодия, учителей Словенских",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-ravnoapostol-nykh-kirilla-i-mefodiya-uchitelei-slovenskikh/"
      ],
      "name": "Parish of the Church of Equal-to-the-Apostles Cyril and Methodius, Slovenian teachers",
      "id": "by-hrodna-639e3b5a6c",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма праведной Софии, княгини Слуцкой",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-pravednoi-sofii-knyagini-slufkoi/"
      ],
      "name": "Parish of Righteous Sophia of Slutsk Church",
      "id": "by-hrodna-a16d6a0c16",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма святителя Спиридона Тримифунтского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-svyatitelya-spiridona-trimifuntskogo/"
      ],
      "name": "Parish of the Church of Saint Spyridon of Tremithus",
      "id": "by-hrodna-2c58766f6b",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма Усекновения главы Иоанна Предтечи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-useknoveniya-glavy-ioanna-predtechi/"
      ],
      "name": "Parish of the Church of the Beheading of John the Baptist",
      "id": "by-hrodna-acd819f0be",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма благоверного князя Александра Невского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-blagovernogo-knyazya-aleksandra-nevskogo-grodno/"
      ],
      "name": "Parish of the Church of the Right-believing Prince Alexander Nevsky",
      "id": "by-hrodna-fa359f783b",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма Богоявления",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-bogoyavleniya/"
      ],
      "name": "Parish of the Church of the Epiphany",
      "id": "by-hrodna-0c837097f6",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма великомученика и целителя Пантелеимона",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-velikomuchenika-i-felitelya-panteleimona/"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon",
      "id": "by-hrodna-788018bd84",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма Нерукотворного Образа Господня",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-nerukotvornogo-obraza-gospodnya/"
      ],
      "name": "Parish of the Church of the Holy Image of the Lord Not Made by Hands",
      "id": "by-hrodna-32e7b1fb77",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма иконы Божией Матери \"Утоли моя печали\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-ikony-bozhiei-materi-utoli-moya-pechali/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Quiet My Sorrows\"",
      "id": "by-hrodna-489a8b0cef",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма иконы Божией Матери \"Взыскание погибших\"",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-ikony-bozhiei-materi-vzyskanie-pogibshikh/"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Seeking the Lost\"",
      "id": "by-hrodna-3a059852fa",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма Рождества Христова",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-rozhdestva-khristova/"
      ],
      "name": "Parish of the Church of the Nativity",
      "id": "by-hrodna-0f4c1942aa",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма Сретения Господня",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-sreteniya-gospodnya/"
      ],
      "name": "Parish of the Church of the Presentation of the Lord",
      "id": "by-hrodna-25e813dbae",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма Воскресения Христова",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-voskreseniya-khristova/"
      ],
      "name": "Parish of the Church of the Resurrection of Christ",
      "id": "by-hrodna-73dd8dd27f",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма преподобномученика Афанасия Брестского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-prepodobnomuchenika-afanasiya-brestskogo/"
      ],
      "name": "Parish of the Church of the Venerable Martyr Athanasius of Brest",
      "id": "by-hrodna-269b67d413",
      "country": "BY"
    },
    {
      "parent": "ru-hrodna",
      "local": "Приход храма преподобномученика Серафима Жировичского",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://orthos.org/khramy/kartochki-khramov/prikhod-khrama-prepodobnomuchenika-serafima-zhirovichskogo/"
      ],
      "name": "Parish of the Church of the Venerable Martyr Seraphim of Zhirovichi",
      "id": "by-hrodna-bfbdef5f62",
      "country": "BY"
    }
  ],
  "ru-lida": [
    {
      "parent": "ru-lida",
      "local": "Архистратиго -Михайловский кафедральный собор в г. Лида Лидской епархии Белорусской Православной Церкви.",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=316"
      ],
      "name": "Archangel Michael's Cathedral in Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-79dcb25642",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Архиерейское подворье в честь преподобного Серафима Саровского в деревне Велички",
      "rank": "Metochion",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=42163"
      ],
      "name": "Episcopal Metochion in honor of Venerable Seraphim of Sarov in Wieliczki",
      "id": "by-lida-74b93d60be",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Войсковой храм преподобного Сергия, игумена Радонежского Лидского пограничного отряда.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=324"
      ],
      "name": "Military Church of Venerable Sergius, abbot of the Radonezh Lida border detachment",
      "id": "by-lida-0ec9a74c7e",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Христа Спасителя г. Лида Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=330"
      ],
      "name": "Parish of the Cathedral of Christ the Savior in Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-1e3fcc9851",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма в честь святой праведной Софии Слуцкой агрогородка Дворище",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=41343"
      ],
      "name": "Parish of Righteous Sophia of Slutsk Church in the agrotown of Dvorishte",
      "id": "by-lida-51e8d547e4",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святителя Николая Чудотворца д. Лебеда Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=280"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Lebed, Lida district of the Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-e0fffd2461",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Святителя Николая Чудотворца п. Юратишки Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=198"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Yuratishki, Ivyevsky district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-f471e4d7d8",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Благовещения Пресвятой Богородицы д. Рацевичи Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=243"
      ],
      "name": "Parish of the Church of the Annunciation of the Most Holy Theotokos in the village of Ratsevichi, Smorgon district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-910a1c0628",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Успения Пресвятой Богородицы с. Радивонишки Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=286"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in Radivonishki, Lida district, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-a8d4357e0a",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Воздвижения Животворящего Креста Господня д. Бобры Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=268"
      ],
      "name": "Parish of the Church of the Exaltation of the Life-giving Cross of the Lord in the village of Bobry, Lida district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-9056861026",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Святых Апостолов Петра и Павла а.г.Трабы Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=200"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul agrotown of Traby, Ivyevsky district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-4a47872090",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святых апостолов Петра и Павла города Островец Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=186"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the city of Ostrovets, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-03af2a7222",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святых апостолов Петра и Павла деревни Светляны Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=245"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Svetlyany, Smorgon district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-0cd3fe14aa",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого Архистратига Михаила Божия Сморгонского района Лидской епархии Белоруской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=233"
      ],
      "name": "Parish of the Church of the Holy Archangel Michael of God, Smorgon region, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-b61d299f7c",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святой блаженной Матроны Московской поселка Первомайский Лидского района",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=41926"
      ],
      "name": "Parish of the Church of the Blessed Matrona of Moscow in the village of Pervomaisky, Lida district",
      "id": "by-lida-ef5061eea9",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого благоверного князя Александра Невского аг. Крево Сморгонского района Лидской епархии Белоруской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=239"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky agrotown of Krevo of the Smorgon region of the Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-8dfb58406a",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого благоверного князя Александра Невского г. Лида Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=318"
      ],
      "name": "Parish of the Church of the Holy Right-believing Prince Alexander Nevsky in the city of Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-a236ec5f2d",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святых равноапостольных царя Константина и царицы Елены агрогородка Жодишки Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=241"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Tsar Constantine and Queen Helena in the agrotown of Zhodishki, Smorgon district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-7ce7ed27fb",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого великомученика и целителя Пантелеимона г. Лида Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=322"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon in the city of Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-33dbd80110",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого великомученика Георгия Победоносца г. Лида Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=328"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the city of Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-ffb1fe5e49",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого великомученика Георгия Победоносца д. Гольшаны Ошмянского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=222"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Golshany, Oshmyany district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-0eba8bcf50",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого великомученика целителя Пантелеимона д. Бакшты Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=202"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon in the village of Bakshty, Ivyevsky District, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-a2b6178be7",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого мученика младенца Гавриила Белостокского, Слуцкого г.Ивье Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=196"
      ],
      "name": "Parish of the Church of the Holy Infant Martyr Gabriel of Bialystok, Slutsk, Ivye, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-5a8544c6a5",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма священномученика Киприана пресвитера Ятранского агрогородка Дитва Лидского района",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=41463"
      ],
      "name": "Parish of the Hieromartyr Cyprian, Presbyter of Yatran, Church in the agrotown of Ditva, Lida district",
      "id": "by-lida-0b3ac8608b",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма священномученика Петра, митрополита Крутицкого аг.ст. Ошмяны Ошмянского района Лидской епархии Белоруской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=350"
      ],
      "name": "Parish of the Hieromartyr Peter, Metropolitan of Krutitsy, Church in Oshmyany, Oshmyany district, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-5f8af98ae6",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святых мучеников Антония, Иоанна, Евстафия Виленских города Сморгони Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=392"
      ],
      "name": "Parish of the Church of the Holy Martyrs Anthony, John, Eustathius of Vilna in the city of Smorgon, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-eed66d090c",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого пророка Илии д. Михайловщина Ошмянского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=224"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Mikhailovshchina, Oshmyany district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-77634ba70b",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святого пророка Илии деревни Ольховка Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=188"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Olkhovka, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-291d519416",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Святого Духа д. Сукневичи Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=249"
      ],
      "name": "Parish of the Church of the Holy Spirit in the village of Suknevichi, Smorgon district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-81119725bf",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма иконы Божией Матери \"В скорбях и печалях Утешение\" г. Сморгони Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=394"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Consolation in Sorrows and Griefs\" in the city of Smorgon, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-1ea4f16400",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих Радость\" деревни Кевлы Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=237"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Joy of All Who Sorrow\" in the village of Kevly, Smorgon district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-5cd8fccc69",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма иконы Божией Матери \"Взыскание погибших\" г. Лида Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=320"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Seeking the Lost\" in the city of Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-3850713444",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма иконы Божией Матери \"Всецарица\" в г. Лида Лидской епархии Белоруской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=326"
      ],
      "name": "Parish of the Church of the Icon of the Theotokos \"Queen of All\" in the city of Lida, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-63712792be",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы аг. Гончары Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=272"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos agrotown of Gonchary of the Lida district of the Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-17a369bb8e",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы аг. Гончары Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=282"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos agrotown of Gonchary of the Lida district of the Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-7bb494fbed",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы аг. Залесье Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=235"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos agrotown of Zalesie, Smorgon region, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-96ad9cd693",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Мыто Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=284"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Myto, Lida district of the Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-ccb3237e05",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Николаево Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=212"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Nikolaevo, Ivyevsky district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-2eb76bf740",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы, д. Збляны Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=278"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos, village of Zblyany, Lida district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-0f59dcdc7f",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Рождества Пресвятой Богородицы аг. Голдово Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=270"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos agrotown of Goldovo, Lida district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-69a1e32fe6",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Рождество Пресвятой Богородицы д. Докудово Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=276"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Dokudovo, Lida district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-9bb9979969",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Воскресения Христова города Ошмяны Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=348"
      ],
      "name": "Parish of the Church of the Resurrection of Christ in the city of Oshmyany, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-d8a1be3e19",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Царственных страстотерпцев д. Солы Сморгонского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=247"
      ],
      "name": "Parish of the Church of the Royal Passion-Bearers in the village of Soly, Smorgon region, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-81622c5070",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Преображения Господня города Сморгонь Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=390"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the city of Smorgon, Lida Diocese of the Belarusian Orthodox Church",
      "id": "by-lida-ed81a3b618",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Преображения Господня д. Дикушки Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=274"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Dikushki, Lida district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-149db19248",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма преподобной Евфросинии игуменьи и княжны Полоцкой д. Вишнево Сморгонского района Лидской епархии Белорусской Православной Церкви",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=231"
      ],
      "name": "Parish of the Church of the Venerable Euphrosyne, Abbess and Princess of Polotsk, village of Vishnevo, Smorgon district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-199be30553",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Жировичской иконы Божией Матери г. Березовка Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=266"
      ],
      "name": "Parish of the Church of the Zhirovichi Icon of the Theotokos in the city of Berezovka, Lida district of the Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-34d835c6c8",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Воздвижения Креста Господня агрогородка Белица Лидского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=264"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the agrotown of Belitsa, Lida district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-8dfe2974ff",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма святой великомученицы Варвары д. Чапунь Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=214"
      ],
      "name": "Parish of the Church of the Great Martyr Barbara in the village of Chapun, Ivyevsky district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-5455f64513",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Святой Живоначальной Троицы села Морино Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=210"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Morino, Ivyevsky district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-2c42a53011",
      "country": "BY"
    },
    {
      "parent": "ru-lida",
      "local": "Приход храма Покрова Пресвятой Богородицы села Князиковцы Ивьевского района Лидской епархии Белорусской Православной Церкви.",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://lida-eparhia.by/?page_id=208"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Knyazikovtsy, Ivyevsky district, Lida diocese of the Belarusian Orthodox Church",
      "id": "by-lida-9a2f52d409",
      "country": "BY"
    }
  ],
  "ru-pinsk": [
    {
      "parent": "ru-pinsk",
      "local": "собора Покрова Пресвятой Богородицы г.Барановичи",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Cathedral of the Protection of the Most Holy Theotokos, Baranovichi",
      "id": "by-pinsk-de3d389151",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого преподобного Антония Великого г.Коссово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Venerable Anthony the Great, Kossovo",
      "id": "by-pinsk-b8a82964f7",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой блаженной Валентины Минской г.Барановичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Blessed Valentina of Minsk Church in Baranovichi",
      "id": "by-pinsk-0072f020fd",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой равноапостольной Марии Магдалины д.Ольгомель",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Equal-to-the-Apostles Mary Magdalene Church in Olgomel",
      "id": "by-pinsk-40054278a7",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого Архангела Михаила аг.Рубель",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel agrotown of Rubel",
      "id": "by-pinsk-105d5fe6ac",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого Архангела Михаила д.Начь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Nach",
      "id": "by-pinsk-eb3c30da78",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого Архангела Михаила д.Одрижин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Odrizhin",
      "id": "by-pinsk-36ae4497fb",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого Архангела Михаила д.Ремель",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Michael the Archangel in the village of Remel",
      "id": "by-pinsk-7c34a5b666",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святителя Николая Чудотворца д.Дружиловичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Druzhilovichi",
      "id": "by-pinsk-e45d7efc2d",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святителя Николая Чудотворца д.Коротичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Korotichi",
      "id": "by-pinsk-1c6390ff31",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святителя Николая Чудотворца д.Малаховцы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Malakhovtsy",
      "id": "by-pinsk-ca0606e7e4",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святителя Николая Чудотворца д.Мальковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Malkovichi",
      "id": "by-pinsk-a7cd6de412",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святителя Николая Чудотворца д.Полонка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Nicholas the Wonderworker in the village of Polonka",
      "id": "by-pinsk-b65880123c",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой Параскевы Сербской д.Ополь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Paraskeva of Serbia in the village of Opol",
      "id": "by-pinsk-db36bc4a2e",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Св.преп. Антония Киево-Печерского д.Подгорная",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of Saint Anthony of the Kyiv Caves Church in Podgornaya",
      "id": "by-pinsk-f60248dafc",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой праведной Анны д.Любищицы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Righteous Anne in the village of Lyubishtsy",
      "id": "by-pinsk-2032d1e3f5",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого преподобного Сергия Радонежского д.Миловиды",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Venerable Sergius of Radonezh in the village of Milovidy",
      "id": "by-pinsk-7f4779eb8f",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святителя Тихона Патриарха Московского г.Ганцевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of Saint Tikhon Patriarch of Moscow, Gantsevichi",
      "id": "by-pinsk-73d902e843",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Вознесения Господня д.Ляховичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Lyakhovichi",
      "id": "by-pinsk-6a659e1a74",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Вознесения Господня д.Молодово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Ascension of the Lord in the village of Molodovo",
      "id": "by-pinsk-80c49bc373",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Успения Пресвятой Богородицы д.Бытень",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Byten",
      "id": "by-pinsk-e52df036ac",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Успения Пресвятой Богородицы д.Ольпень",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Olpen",
      "id": "by-pinsk-f98e8a6c93",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Успения Пресвятой Богородицы д.Снитово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Dormition of the Most Holy Theotokos in the village of Snitovo",
      "id": "by-pinsk-496bb1b662",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воздвижения Креста Господня д.Бродница",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Brodnitsa",
      "id": "by-pinsk-bb8d57988d",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воздвижения Креста Господня д.Гощево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Goshchevo",
      "id": "by-pinsk-b1b765c1dd",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воздвижения Креста Господня д.Хотомель",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Khotomel",
      "id": "by-pinsk-259a195f9d",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воздвижения Креста Господня д.Святая Воля",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Svyataya Volya",
      "id": "by-pinsk-c739c1c213",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воздвижения Креста Господня д.Вороцевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross in the village of Vorotsevichi",
      "id": "by-pinsk-24321be11a",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воздвижения Креста Господня г.п.Городище",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Exaltation of the Holy Cross, Gorodishche",
      "id": "by-pinsk-dab94aae5c",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого апостола и евангелиста Иоанна Богослова д.Семигостичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Apostle and Evangelist John the Theologian in the village of Semigoschi",
      "id": "by-pinsk-9e4edca4ae",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святых Первоверховных апостолов Петра и Павла д.Мохро",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Mokhro",
      "id": "by-pinsk-b33adcdfda",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святых Первоверховных апостолов Петра и Павла д.Молчадь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Apostles Peter and Paul in the village of Molchad",
      "id": "by-pinsk-cfb372e0b6",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого благоверного великого князя Александра Невского д.Столовичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Right-believing Grand Prince Alexander Nevsky in the village of Stolovichi",
      "id": "by-pinsk-b3922e59c4",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого благоверного великого князя Александра Невского д.Стрельно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Right-believing Grand Prince Alexander Nevsky in the village of Strelno",
      "id": "by-pinsk-851f015ae8",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого благоверного великого князя Александра Невского г.Барановичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Right-believing Grand Prince Alexander Nevsky, Baranovichi",
      "id": "by-pinsk-bc3bdf4430",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой блаженной Матероны Московской г.Ганцевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Blessed Matrona of Moscow Church in Gantsevichi",
      "id": "by-pinsk-3391558506",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого равноапостольного великого князя Владимира д.Огаревичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Equal-to-the-Apostles Grand Duke Vladimir village Ogarevichi",
      "id": "by-pinsk-bfc2e6ba1d",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого великомученика и целителя Пантелеимона д.Крошин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr and Healer Panteleimon in the village of Kroshin",
      "id": "by-pinsk-0b15ed3354",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого великомученика Георгия Победоносца д.Чудин",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Chudin",
      "id": "by-pinsk-04cce1d1ab",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого великомученика Георгия Победоносца д.Лядец",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Lyadets",
      "id": "by-pinsk-340c3373e2",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого великомученика Георгия Победоносца д.Яглевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious in the village of Yaglevichi",
      "id": "by-pinsk-aaae054530",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого великомученика Георгия Победоносца г.Барановичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr George the Victorious, Baranovichi",
      "id": "by-pinsk-73ff69a91c",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой великомученицы Параскевы д.Ольшаны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the village of Olshany",
      "id": "by-pinsk-987cfca680",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой великомученицы Параскевы Пятницы д.Бережное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Great Martyr Paraskeva in the village of Berezhnoe",
      "id": "by-pinsk-fe1e1d8676",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой Живоначальной Троицы г.п.Телеханы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the town of Telekhany",
      "id": "by-pinsk-0a58f885e4",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой Живоначальной Троицы д.Достоево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Dostoevo",
      "id": "by-pinsk-0178e74109",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой Живоначальной Троицы д.Оздамичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Ozdamici",
      "id": "by-pinsk-98fff6d237",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой Живоначальной Троицы д.Туры",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Tura",
      "id": "by-pinsk-c91e59fa1b",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святой Живоначальной Троицы д.Вольно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Life-giving Trinity in the village of Volno",
      "id": "by-pinsk-ff3cdbdc1a",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святых Жен-Мироносиц г.Барановичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Myrrh-Bearing Women in Baranovichi",
      "id": "by-pinsk-15b4c3a8db",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого пророка Божия Илии д.Адаховщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Adakhovshchina",
      "id": "by-pinsk-45bde9ebcd",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого пророка Божия Илии д.Велемичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Prophet Elijah in the village of Velemichi",
      "id": "by-pinsk-eec30b136f",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святых бессребреников Космы и Дамиана д.Лутки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Holy Unmercenaries Cosmas and Damian in the village of Lutki",
      "id": "by-pinsk-4db849a498",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Святого преподобного Серафима Саровского д.Карчево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Venerable Seraphim of Sarov in the village of Karchevo",
      "id": "by-pinsk-21cb52c1f6",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Иконы Божией Матери \"Державная\" г.Ивацевичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Reigning Icon of the Theotokos Church in Ivatsevichi",
      "id": "by-pinsk-b558c6aae7",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Покрова Пресвятой Богородицы г.Иваново",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in Ivanovo",
      "id": "by-pinsk-1dded0031c",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Покрова Пресвятой Богородицы д.Люсино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Lyusino",
      "id": "by-pinsk-eb6f22dc63",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Покрова Пресвятой Богородицы д.Выгонощи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Protection of the Most Holy Theotokos in the village of Vygonoshchi",
      "id": "by-pinsk-00f7b3ef3f",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Иверской иконы Божией Матери д.Сочивки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Iveron Icon of the Theotokos in the village of Sochivki",
      "id": "by-pinsk-e65e5d54f6",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Казанской иконы Божией Матери г.Давид-Городок",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos in David-Gorodok",
      "id": "by-pinsk-c004a38a4c",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Казанской иконы Божией Матери д.Лесная",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos in the village of Lesnaya",
      "id": "by-pinsk-e4665ce2bf",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Казанской иконы Божией Матери д.Тышковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Kazan Icon of the Theotokos in the village of Tyshkovichi",
      "id": "by-pinsk-2a74144d5e",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Христова д.Большое Малешево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of Christ in the village of Bolshoye Maleshevo",
      "id": "by-pinsk-7f767c780c",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Христова д.Толмачево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of Christ in the village of Tolmachevo",
      "id": "by-pinsk-cea1500044",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Пресвятой Богородицы д.Глинная",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Glinnaya",
      "id": "by-pinsk-076e0dd57d",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Пресвятой Богородицы д.Хоромск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Khoromsk",
      "id": "by-pinsk-4d10d778ed",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Пресвятой Богородицы д.Лясковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Lyaskovichi",
      "id": "by-pinsk-6c2cac9523",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Пресвятой Богородицы д.Раздяловичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Razdyalovichi",
      "id": "by-pinsk-88cb8b6562",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Рождества Пресвятой Богородицы д.Русино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Nativity of the Most Holy Theotokos in the village of Rusino",
      "id": "by-pinsk-8a8c7cdb98",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Воскресения Христова д.Теребличи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Resurrection of Christ in the village of Tereblichi",
      "id": "by-pinsk-ee8f8d3561",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Преображения Господня д.Мотоль",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Motol",
      "id": "by-pinsk-879fb6d4be",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма Преображения Господня д.Новая Мышь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Transfiguration of the Lord in the village of Novaya Mysh",
      "id": "by-pinsk-ddc804e082",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "прихода храма преподобномученика Афанасия Брестского д.Яечковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://pinskeparh.by/dukhovenstvo"
      ],
      "name": "Parish of the Church of the Venerable Martyr Athanasius of Brest in the village of Yaechkovichi",
      "id": "by-pinsk-3eded083b5",
      "country": "BY"
    },
    {
      "parent": "ru-pinsk",
      "local": "Свято-Варваринский женский монастырь г.Пинска",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://pinskeparh.by/monastyri"
      ],
      "name": "Saint Barbara's Convent in Pinsk",
      "id": "by-pinsk-8f4037486d",
      "country": "BY"
    }
  ],
  "ru-navahrudak": [
    {
      "parent": "ru-navahrudak",
      "local": "Собор святых мучеников Бориса и Глеба",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/novogrudok/sobor-svjatykh-muchenikov-borisa-i-gleba.html"
      ],
      "name": "Cathedral of the Holy Martyrs Boris and Gleb",
      "id": "by-navahrudak-785ac758bb",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Часовня в честь иконы Божией Матери \"Неупиваемая Чаша\"",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/brolniki.html"
      ],
      "name": "Chapel in honor of the Icon of the Theotokos \"Inexhaustible Chalice\"",
      "id": "by-navahrudak-da887508e2",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь всех Белорусских Святых",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/radun.html"
      ],
      "name": "Church in honor of all Belarusian Saints",
      "id": "by-navahrudak-1707c92c18",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Святого Архистратига Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/miratichi.html"
      ],
      "name": "Church in honor of Saint Archangel Michael",
      "id": "by-navahrudak-36e42f48af",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Святого Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/vseljub.html"
      ],
      "name": "Church in honor of Saint Archangel Michael",
      "id": "by-navahrudak-8ec6fc953b",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь преподобной Евфросинии Полоцкой",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/voroncha.html"
      ],
      "name": "Church in honor of Venerable Euphrosyne of Polotsk",
      "id": "by-navahrudak-a92f4aac1d",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь св. мч. Иоанна Воина в 11-й мехбригаде (в/ч 33933), Слоним",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/slonim/khram-v-chest-sv-mch-ioanna-voina-v-11-i-mekhbrigade-vch-33933-slonim.html"
      ],
      "name": "Martyr John the Warrior Church at the 11th Mechanized Brigade (Military Unit 33933) in Slonim",
      "id": "by-navahrudak-1ffde4c697",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/volkovichi.html"
      ],
      "name": "Dormition of the Most Holy Theotokos Church",
      "id": "by-navahrudak-76dc6b48f5",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/voinevichi.html"
      ],
      "name": "Church in honor of the Exaltation of the Holy Cross",
      "id": "by-navahrudak-861b838f45",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь священномученика Петра, митрополита Крутицкого",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/chemery.html"
      ],
      "name": "Hieromartyr Peter, Metropolitan of Krutitsy, Church",
      "id": "by-navahrudak-60ce0d9cb1",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храме в честь священномученика Владимира Хрищановича",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/gezgaly.html"
      ],
      "name": "Church in honor of the Hieromartyr Vladimir Khrishchanovich",
      "id": "by-navahrudak-e54eae88af",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/zareche.html"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-navahrudak-9790375e2e",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/valevka.html"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-navahrudak-9de35b1698",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/cvenzovec.html"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-navahrudak-b77899f868",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/vereskovo.html"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-navahrudak-bd2d2bb74a",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/mizgiri.html"
      ],
      "name": "Saints Peter and Paul Church",
      "id": "by-navahrudak-e8398faab0",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Святого Великомученика и Победоносца Георгия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/vseljub/ltp-5.html"
      ],
      "name": "Church in honor of the Great Martyr and Victorious George",
      "id": "by-navahrudak-d29fb6c53f",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святого великомученика Димитрия Солунского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/shchorsy.html"
      ],
      "name": "Church in honor of the Great Martyr Demetrius of Thessalonica",
      "id": "by-navahrudak-98d006601d",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святого благоверного князя Александра Невского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/zagore-sennenskoe.html"
      ],
      "name": "Holy Right-believing Prince Alexander Nevsky Church",
      "id": "by-navahrudak-d8570bdfa9",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святого пророка Божия Ильи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/ljubcha.html"
      ],
      "name": "Prophet Elijah Church",
      "id": "by-navahrudak-5584e61fb6",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь святого праведного Иоанна Кронштадтского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/okhonovo.html"
      ],
      "name": "Righteous John of Kronstadt Church",
      "id": "by-navahrudak-6b321d7648",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Святой Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/derevnaja.html"
      ],
      "name": "Church in honor of the Holy Trinity",
      "id": "by-navahrudak-a25f3cc4ff",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь иконы Божией Матери \"Живоносный Источник\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/mizhevichi.html"
      ],
      "name": "Church in honor of the Icon of the Theotokos \"Life-giving Spring\"",
      "id": "by-navahrudak-b3c1fd0877",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь иконы Божией Матери \"Споручница грешных\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/slonim/khram-v-chest-ikony-bozhiei-materi-sporuchnica-greshnykh.html"
      ],
      "name": "Church in honor of the Icon of the Theotokos \"Surety of Sinners\"",
      "id": "by-navahrudak-b9f798f93d",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь иконы Божией Матери \"Нечаянная Радость\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/novogrudok/khram-v-chest-ikony-bozhiei-materi-nechajannaja-radost.html"
      ],
      "name": "Church in honor of the Icon of the Theotokos \"Unexpected Joy\"",
      "id": "by-navahrudak-4daaabc934",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь иконы Божией Матери, именуемой \"Всецарица\"",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/krutilovichi.html"
      ],
      "name": "Church in honor of the Icon of the Theotokos, called \"Queen of All\"",
      "id": "by-navahrudak-386c3d64fc",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Казанской иконы Божией Матери",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/negnevichi.html"
      ],
      "name": "Church in honor of the Kazan Icon of the Theotokos",
      "id": "by-navahrudak-13c8c445a9",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Казанской иконы Божией Матери",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/shilovichi.html"
      ],
      "name": "Church in honor of the Kazan Icon of the Theotokos",
      "id": "by-navahrudak-ca01ef502a",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Казанской иконы Божией Матери",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/berezhno.html"
      ],
      "name": "Church in honor of the Kazan Icon of the Theotokos",
      "id": "by-navahrudak-cc17844503",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/polbereg.html"
      ],
      "name": "Church in honor of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-3960a91bbb",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм в честь Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/jatra.html"
      ],
      "name": "Church in honor of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-3de594a635",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Всех Святых",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/dolnaja-ruta.html"
      ],
      "name": "Church of All Saints",
      "id": "by-navahrudak-78a6fa3bc6",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святой праведной Анны",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/zagore.html"
      ],
      "name": "Church of Righteous Anna",
      "id": "by-navahrudak-5c30c9dc48",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Святого Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/ljubno.html"
      ],
      "name": "Church of Saint Archangel Michael",
      "id": "by-navahrudak-7bfb8e59c0",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Святого Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/cirin.html"
      ],
      "name": "Church of Saint Archangel Michael",
      "id": "by-navahrudak-93f1783dff",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Святого Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/perevoloka.html"
      ],
      "name": "Church of Saint Archangel Michael",
      "id": "by-navahrudak-dd383631e8",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого Архангела Михаила",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/ruda-javorskaja.html"
      ],
      "name": "Church of Saint Archangel Michael",
      "id": "by-navahrudak-edf7c2d0e6",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святителя Гурия Казанского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/partizanovka.html"
      ],
      "name": "Church of Saint Gury of Kazan",
      "id": "by-navahrudak-286b6b0f5c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святителя Николая",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/ozernica.html"
      ],
      "name": "Church of Saint Nicholas",
      "id": "by-navahrudak-14aa36bfee",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/vysock.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-navahrudak-1783622da6",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/kryshelovshchina.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-navahrudak-592a1af709",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/nogorodovichi.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-navahrudak-6448a1ea53",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святителя Николая Чудотворца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/novye-devjatkovichi.html"
      ],
      "name": "Church of Saint Nicholas the Wonderworker",
      "id": "by-navahrudak-6cf605b46c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм преподобного Серафима Саровского",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/senkovshchina.html"
      ],
      "name": "Church of Venerable Seraphim of Sarov",
      "id": "by-navahrudak-ba819c8210",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Вознесения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/medvjadko.html"
      ],
      "name": "Church of the Ascension of the Lord",
      "id": "by-navahrudak-4344ec24f0",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Вознесения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/eremichi.html"
      ],
      "name": "Church of the Ascension of the Lord",
      "id": "by-navahrudak-9edbceee1e",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/kozlovshchina.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-navahrudak-85ee237d78",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/lavrishevo.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-navahrudak-c99d6c1d14",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/ljubanichi.html"
      ],
      "name": "Church of the Dormition of the Most Holy Theotokos",
      "id": "by-navahrudak-db50297b1f",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Воздвижения Креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/deljatichi.html"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-navahrudak-588c1d70c4",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Воздвижения креста Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/zbochno.html"
      ],
      "name": "Church of the Exaltation of the Holy Cross",
      "id": "by-navahrudak-97463d4a72",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/bolshie-zhukhovichi.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul",
      "id": "by-navahrudak-56c373ea9a",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святых апостолов Петра и Павла",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/korelichi-petro-pavlovskii.html"
      ],
      "name": "Church of the Holy Apostles Peter and Paul",
      "id": "by-navahrudak-ace181a3b0",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святых равноапостольных великого князя Владимира и великой княгини Ольги д. Селявичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/seljavichi.html"
      ],
      "name": "Church of the Holy Equal-to-the-Apostles Grand Duke Vladimir and Grand Duchess Olga village Selyavichi",
      "id": "by-navahrudak-ca04491c02",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Святого Великомученика и Победоносца Георгия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/malvorobevichi.html"
      ],
      "name": "Church of the Great Martyr and Victorious George",
      "id": "by-navahrudak-4cd1f81871",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого великомученика и победоносца Георгия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/kupisk.html"
      ],
      "name": "Church of the Great Martyr and Victorious George",
      "id": "by-navahrudak-5eabce7e9c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого Великомученика и Победоносца Георгия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/mir-georgievskii.html"
      ],
      "name": "Church of the Great Martyr and Victorious George",
      "id": "by-navahrudak-a5b95f9733",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого Великомученика и Победоносца Георгия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/zapole.html"
      ],
      "name": "Church of the Great Martyr and Victorious George",
      "id": "by-navahrudak-ade6a6aafb",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого Великомученика и Победоносца Георгия",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/poreche.html"
      ],
      "name": "Church of the Great Martyr and Victorious George",
      "id": "by-navahrudak-d355c79791",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Святого великомученика и Победоносца Георгия в д. Бол. Воробьевичи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/bolvorobevichi.html"
      ],
      "name": "Great Martyr George the Victorious Church in Bolshiye Vorobievichi",
      "id": "by-navahrudak-06c1366225",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святой великомученицы Варвары",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/raica-vmcvarvary.html"
      ],
      "name": "Church of the Great Martyr Barbara",
      "id": "by-navahrudak-c682e54adf",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого великомученика Георгия Победоносца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/pasinichi.html"
      ],
      "name": "Church of the Great Martyr George the Victorious",
      "id": "by-navahrudak-25328d0e25",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого великомученика Георгия Победоносца",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/gorka.html"
      ],
      "name": "Church of the Great Martyr George the Victorious",
      "id": "by-navahrudak-6ef84b4722",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Святой Живоначальной Троицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/mir-troickii.html"
      ],
      "name": "Church of the Holy Life-giving Trinity",
      "id": "by-navahrudak-61b7348f51",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святой мученицы Параскевы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/starye-devjatkovichi.html"
      ],
      "name": "Church of the Martyr Paraskeva",
      "id": "by-navahrudak-2b411d222e",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святых благоверных князей Бориса и Глеба",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/nakryshki.html"
      ],
      "name": "Holy Right-believing Princes Boris and Gleb Church",
      "id": "by-navahrudak-d230a2e695",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого пророка Илии",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/klepachi.html"
      ],
      "name": "Church of the Holy Prophet Elijah",
      "id": "by-navahrudak-62d4b7bc29",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого пророка Божия Илии",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/surinka.html"
      ],
      "name": "Church of the Holy Prophet Elijah",
      "id": "by-navahrudak-fff9d660c2",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого пророка Иоанна Предтечи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/malaja-krakotka.html"
      ],
      "name": "Church of the Holy Prophet John the Baptist",
      "id": "by-navahrudak-c14fd48477",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм святого преподобного Серафима Вырицкого",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/kaishovka.html"
      ],
      "name": "Church of the Venerable Seraphim of Vyritsky",
      "id": "by-navahrudak-ccfacb3003",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/turec.html"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-navahrudak-1e2c082d4d",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/dvorec.html"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-navahrudak-488872566a",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Покрова Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/simakovo.html"
      ],
      "name": "Church of the Protection of the Most Holy Theotokos",
      "id": "by-navahrudak-f622175205",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Христова",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/pavlovo.html"
      ],
      "name": "Church of the Nativity",
      "id": "by-navahrudak-c861a1a81a",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Иоанна Предтечи",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/malye-zhukhovichi.html"
      ],
      "name": "Church of the Nativity of John the Baptist",
      "id": "by-navahrudak-21b3529d5c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/troshchicy.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-29a900ef13",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/novoelnja.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-75ca60c2c6",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/mizhevichi-rozhdestva-bogorodicy.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-b2d813644f",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/javor.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-f5392062f2",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Рождества Божией Матери",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/jarutichi.html"
      ],
      "name": "Church of the Nativity of the Most Holy Theotokos",
      "id": "by-navahrudak-456b5667cd",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм пророка Илии",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/lykovichi.html"
      ],
      "name": "Church of the Prophet Elijah",
      "id": "by-navahrudak-6d179e391c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Воскресения Христова",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/luki.html"
      ],
      "name": "Church of the Resurrection of Christ",
      "id": "by-navahrudak-7ee16873cf",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Воскресения Христова",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/velikaja-sloboda.html"
      ],
      "name": "Church of the Resurrection of Christ",
      "id": "by-navahrudak-eb77e400ce",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм Преображения Господня",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/korelichskoe-blagochinie/raica-preobrazhenskii.html"
      ],
      "name": "Church of the Transfiguration of the Lord",
      "id": "by-navahrudak-385fa859dc",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Храм преподобномученика Афанасия Брестского.",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/slonim/khram-prepodobnomuchenika-afanasija-brestskogo.html"
      ],
      "name": "Church of the Venerable Martyr Athanasius of Brest",
      "id": "by-navahrudak-24bea041cc",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Дятлово, собор святых Новомучеников и Исповедников Церкви Русской",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/djatlovo-sobor-svjatykh-novomuchenikov-i-ispovednikov-cerkvi-russkoi.html"
      ],
      "name": "Dyatlovo, Cathedral of the Holy New Martyrs and Confessors of the Russian Church",
      "id": "by-navahrudak-4872d6b6d4",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Дятлово, Преображенский храм",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/djatlovskoe-blagochinie/djatlovo-preobrazhenskii-khram.html"
      ],
      "name": "Dyatlovo, Transfiguration Church",
      "id": "by-navahrudak-77de575156",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Свято-Благовещенский женский монастырь в г.Слониме",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://www.eparhia.by/eparkhija/monastyri/svjato-blagoveshchenskii-zhenskii-monastyr-v-gslonime.html"
      ],
      "name": "Holy Annunciation Convent in Slonim",
      "id": "by-navahrudak-22a0990396",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Свято-Троицкий собор",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/slonim/svjato-troickii-sobor.html"
      ],
      "name": "Holy Trinity Cathedral",
      "id": "by-navahrudak-ee5f77d41c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Спасо-Преображенский Кафедральный собор",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/slonimskoe-blagochinie/slonim/spaso-preobrazhenskii-kafedralnyi-sobor.html"
      ],
      "name": "Transfiguration of the Lord Cathedral",
      "id": "by-navahrudak-c4d34f3f3c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Свято-Амвросиевский женский монастырь",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://www.eparhia.by/eparkhija/monastyri/svjato-amvrosievskii-zhenskii-monastyr.html"
      ],
      "name": "Saint Ambrose Convent",
      "id": "by-navahrudak-d329a99a1c",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Свято-Елисеевский Лавришевский мужской монастырь",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://www.eparhia.by/eparkhija/monastyri/svjato-eliseevskii-lavrishevskii-muzhskoi-monastyr.html"
      ],
      "name": "Saint Elisha Lavrishevo Monastery",
      "id": "by-navahrudak-dd8c58fc1e",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Свято-Никольский Кафедральный собор",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/novogrudok/svjato-nikolskii-kafedralnyi-sobor.html"
      ],
      "name": "Saint Nicholas Cathedral",
      "id": "by-navahrudak-c61fedb7c7",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "Свято-Зосимо-Савватиевский Велико-Кракотский мужской монастырь",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://www.eparhia.by/eparkhija/monastyri/svjato-zosimo-savvatievskii-veliko-krakotskii-muzhskoi-monastyr.html"
      ],
      "name": "Saints Zosimas and Sabbatius Vyalikaya Krakotka Monastery",
      "id": "by-navahrudak-12cfec7af0",
      "country": "BY"
    },
    {
      "parent": "ru-navahrudak",
      "local": "д.Волковичи, храм Успения Пресвятой Богородицы",
      "rank": "Church",
      "kind": "parish",
      "sources": [
        "https://www.eparhia.by/eparkhija/prikhody/novogrudskoe-blagochinie/jatra/dvolkovichi-khram-uspenija-presvjatoi-bogorodicy.html"
      ],
      "name": "Volkovichi village, Church of the Dormition of the Most Holy Theotokos",
      "id": "by-navahrudak-abd39503f0",
      "country": "BY"
    }
  ],
  "ru-polatsk": [
    {
      "parent": "ru-polatsk",
      "local": "Приход храма в честь иконы Божией Матери \"Одигитрии\"г. Дисна",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Hodegetria Icon of the Theotokos Church in Disna",
      "id": "by-polatsk-e4887ccd2b",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храмаВознесения Господняг. п. Россоны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/rossonskoe"
      ],
      "name": "Parish of the Ascension of the Lord Church in Rossony",
      "id": "by-polatsk-67e0123655",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма cвятой праведной Анныд. Слобода",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Righteous Anna Church in Sloboda",
      "id": "by-polatsk-0ffb0d1364",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Березвечский женский монастырь в честь Архистратига Божия Михаила",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Berezvechsky Convent in honor of the Archangel of God Michael",
      "id": "by-polatsk-e501692014",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Кафедральный собор Богоявленияг. Полоцк",
      "rank": "Cathedral",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Epiphany Cathedral in Polatsk",
      "id": "by-polatsk-b0ad094b53",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня в честь Рождества Богородицыг.п. Бегомль",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Nativity of the Most Holy Theotokos Chapel in the urban settlement of Begoml",
      "id": "by-polatsk-071535d55f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Иоанна Крестителя д. Черневичи",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Saint John the Baptist Chapel in Chernevichi",
      "id": "by-polatsk-9dfa505588",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Святого Духад. Цветино",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Holy Spirit Chapel in Tsvetino",
      "id": "by-polatsk-0c752de5b0",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Святителя Луки Войно-Ясенецкого в Браславской районной больнице",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Chapel of Saint Luke Voino-Yasenetsky in the Braslav regional hospital",
      "id": "by-polatsk-46d009d08b",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня святой праведной Анны д. Угольники",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Righteous Anna Chapel in Ugolniki",
      "id": "by-polatsk-f231d7d689",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня великомученицы Анастасии Узорешительницыс. Горки",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Great Martyr Anastasia the Deliverer from Bonds Chapel in Gorki",
      "id": "by-polatsk-e8d8657b99",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня святого равноапостольного князя Владимирад. Осиногородок",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Holy Equal-to-the-Apostles Prince Vladimir Chapel in Osinogorodok",
      "id": "by-polatsk-3403de6adb",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Святого великомученика Пантелеимонапромузел Ксты",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Great Martyr and Healer Panteleimon Chapel at the Ksty Industrial Hub",
      "id": "by-polatsk-f31e3474fa",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Святого князя Владимирад. Ист",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Holy Prince Vladimir Chapel in Ist",
      "id": "by-polatsk-01f736b648",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня cвятых первоверховный апостолов Петра и Павлад. Басянки",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Holy Chief Apostles Peter and Paul Chapel in Basyanki",
      "id": "by-polatsk-7966b95ef7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня иконы Божией Матери \"Взыскание погибших\"г.п. Боровуха",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Seeking of the Lost Icon of the Theotokos Chapel in Borovukha",
      "id": "by-polatsk-32c2c4f224",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Покрова Пресвятой Богородицыд. Копыльщина",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Protection of the Most Holy Theotokos Chapel in Kopylshchyna",
      "id": "by-polatsk-89813d4960",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня Казанской иконы Божией Материд. Заутье",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Kazan Icon of the Theotokos Chapel in Zautye",
      "id": "by-polatsk-fbc1f218e7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Часовня пророка Илии д. Вороново",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Prophet Elijah Chapel in Voronovo",
      "id": "by-polatsk-9045ad7d64",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "ЧасовняВоскресения Христовасанаторий \"Лесное\"",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Resurrection of Christ Chapel at Lesnoye Sanatorium",
      "id": "by-polatsk-2988c40cab",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "ЧасовняТрех Святителейд. Папшули",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Three Holy Hierarchs Chapel in Papshuli",
      "id": "by-polatsk-6683716270",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Храм-часовня святителя Николая Чудотворца д. Вашково",
      "rank": "Chapel",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/ushachskoe"
      ],
      "name": "Saint Nicholas the Wonderworker Church-Chapel in Vashkovo",
      "id": "by-polatsk-856825a476",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храм УспенияПресвятой Богородицыд. Маньковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in Mankovichi",
      "id": "by-polatsk-eb04b451a0",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход собора Рождества Пресвятой Богородицы г. Глубокое",
      "rank": "Cathedral Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Cathedral of the Nativity of the Most Holy Theotokos in Glubokoe",
      "id": "by-polatsk-ba927be354",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Всех Святыхг. п. Бегомль",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of All Saints Church in the urban settlement of Begoml",
      "id": "by-polatsk-770c29dbb7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Равноапостольного Князя Владимира д. Узречье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Equal-to-the-Apostles Prince Vladimir Church in Uzrechye",
      "id": "by-polatsk-96ea28c2e7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святой блаженной Ксении Петербургскойг. Полоцк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Blessed Xenia of Petersburg Church in Polatsk",
      "id": "by-polatsk-d80f055e66",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святого Духад. Березино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Holy Spirit Church in Berezino",
      "id": "by-polatsk-63886506e8",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма преподобной Евфросинии Полоцкой д. Боровка",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of Venerable Euphrosyne of Polatsk Church in Borovka",
      "id": "by-polatsk-d0bfa7e3be",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма преподобной Евфросинии Полоцкой д. Росица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of Venerable Euphrosyne of Polatsk Church in Rositsa",
      "id": "by-polatsk-a4494a09dc",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святого Архангела Михаила д. Бигосово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of Archangel Michael Church in Bigosovo",
      "id": "by-polatsk-f5bfbe1c60",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма cвятого Архангела Михаилад. Пестуны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of Archangel Michael Church in Pestuny",
      "id": "by-polatsk-79eb438867",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святителя Николая Чудотворца (Молитвенный дом) г.п.Ушачи",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/ushachskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Prayer House in the urban settlement of Ushachi",
      "id": "by-polatsk-b025f2a976",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святителя Николая Чудотворца д. Калиновое",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Kalinovoye",
      "id": "by-polatsk-0fe720ef25",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворца д. Заборье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Zaborye",
      "id": "by-polatsk-2c549a77f7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворца г. Верхнедвинск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Verkhnedvinsk",
      "id": "by-polatsk-facd4cb3a3",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворца г. п. Видзы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in the urban settlement of Vidzy",
      "id": "by-polatsk-160ad0fcad",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворцад. Бабыничи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Babynichi",
      "id": "by-polatsk-87338e37ca",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святого Николая Чудотворцад. Чересы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Cheresy",
      "id": "by-polatsk-1f1fb6a053",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворцад. Коллективное",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Kollektivnoye",
      "id": "by-polatsk-06aa928b83",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворца с. Иказнь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Ikazn",
      "id": "by-polatsk-478cb5ec97",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святителя Николая Чудотворцад. Германовичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Germanovichi",
      "id": "by-polatsk-92c74cb834",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма СвятителяНиколая Чудотворцад. Краснополье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/rossonskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Krasnopolye",
      "id": "by-polatsk-c72d03e45a",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворцад. Новый Погост",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Novy Pogost",
      "id": "by-polatsk-ce23bedf7f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святителя Николая Чудотворцаг. Поставы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Postavy",
      "id": "by-polatsk-570def5e58",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святителя Николая Чудотворцад. Шити",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Shiti",
      "id": "by-polatsk-d54150eb52",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Николая Чудотворцад. Узмены",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of Saint Nicholas the Wonderworker Church in Uzmeny",
      "id": "by-polatsk-e2e404b3e7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма преподобного Серафима Саровскогод. Ямно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of Venerable Seraphim of Sarov Church in Yamno",
      "id": "by-polatsk-60e2a2b011",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма преподобного Сергия Радонежскогод. Полота",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of Venerable Sergius of Radonezh Church in Polota",
      "id": "by-polatsk-1edc456631",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святителя Тихонад. Фариново",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of Saint Tikhon Church in Farinovo",
      "id": "by-polatsk-b1cdd5195a",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Благовещенья Пресвятой Богородицыд. Рымки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of the Annunciation of the Most Holy Theotokos Church in Rymki",
      "id": "by-polatsk-3e551fea2f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Апостолов Петра и Павла д. Дрисвяты",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of Saints Peter and Paul Church in Drisvyaty",
      "id": "by-polatsk-206830db13",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Апостолов Петра и Павла д. Прозороки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of Saints Peter and Paul Church in Prozoroki",
      "id": "by-polatsk-542d1805d5",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Апостолов Петра и Павла д. Замошье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of Saints Peter and Paul Church in Zamoshye",
      "id": "by-polatsk-117fd4ea44",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма апостолов Петра и Павлад. Южное Гнездилово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of Saints Peter and Paul Church in Yuzhnoye Gnezdilovo",
      "id": "by-polatsk-2fea843ca2",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Вознесения Господня д. Поречье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Ascension of the Lord Church in Porechye",
      "id": "by-polatsk-db0deb5ba3",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Вознесения Господняд. Азино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Ascension of the Lord Church in Azino",
      "id": "by-polatsk-f8f2aeb10f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Успения Пресвятой Богородицы д. Ковали",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in Kovali",
      "id": "by-polatsk-691b745569",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Успения Пресвятой Богородицы д. Сарья",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in Sarya",
      "id": "by-polatsk-359909b0bd",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Успения Пресвятой Богородицы г. Браслав",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in Braslav",
      "id": "by-polatsk-34235c7ee9",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Успение Пресвятой Богородицыг. п. Шарковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of the Dormition of the Most Holy Theotokos Church in the urban settlement of Sharkovshchina",
      "id": "by-polatsk-096c581118",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Усекновения главы Иоанна Предтечид. Крулевщизна",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Beheading of Saint John the Baptist Church in Krulevshchizna",
      "id": "by-polatsk-e62596ab2b",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма благоверных князей Бориса и Глеба д. Волынцы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of the Holy Right-believing Princes Boris and Gleb Church in Volyntsy",
      "id": "by-polatsk-a07f2cb62d",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Воздвижения Креста Господняд. Дригучи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Exaltation of the Cross Church in Driguchi",
      "id": "by-polatsk-ffcf91dc06",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Воздвижение Креста Господняд. Цветино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Exaltation of the Cross Church in Tsvetino",
      "id": "by-polatsk-14c4d9421a",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Воздвижение Креста Господня д. Забелье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Exaltation of the Cross Church in Zabelie",
      "id": "by-polatsk-3ccec06d59",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика и целителя Пантелеимона д. Дерковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Great Martyr and Healer Panteleimon Church in Derkovshchina",
      "id": "by-polatsk-45e248cd8f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика и целителя Пантелеимонаг.Полоцк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Great Martyr and Healer Panteleimon Church in Polatsk",
      "id": "by-polatsk-d972189c94",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика и целителя Пантелеимонаг.п. Боровуха",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Great Martyr and Healer Panteleimon Church in the urban settlement of Borovukha",
      "id": "by-polatsk-c59f49a761",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика Георгия Победоносца г. п. Освея",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in the urban settlement of Osveya",
      "id": "by-polatsk-dd10d2627a",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика Георгия Победоносца г. п. Подсвилье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in the urban settlement of Podsvilye",
      "id": "by-polatsk-695cd35ffe",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика Георгия Победоносцад. Ситцы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in Sitsy",
      "id": "by-polatsk-63e50f68cb",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика Георгия Победоносцад. Домашковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in Domashkovichi",
      "id": "by-polatsk-2345111ac5",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученика Георгия Победоносцад. Тумиловичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in Tumilovichi",
      "id": "by-polatsk-2cfe15ee46",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Великомученика Георгия Победоносцаг.п. Боровуха",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in the urban settlement of Borovukha",
      "id": "by-polatsk-87cda30682",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма великомученицы Параскевы Пятницыд. Ореховно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/ushachskoe"
      ],
      "name": "Parish of the Great Martyr Paraskeva Church in Orekhovo",
      "id": "by-polatsk-729f39b10f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святых апостолов Петра и Павла (Молитвенный дом)д. Кубличи",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/ushachskoe"
      ],
      "name": "Parish of Saints Peter and Paul Prayer House in Kublichi",
      "id": "by-polatsk-91fca75593",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святых апостолов Петра и Павлад. Григоровичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of Saints Peter and Paul Church in Grigorovichi",
      "id": "by-polatsk-6ed9ecaab0",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святого Архангела Михаилаг. Новополоцк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of Archangel Michael Church in Novopolotsk",
      "id": "by-polatsk-575abc5c4f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святого Великомученика Георгия Победоносца г. п. Друя",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in the urban settlement of Druya",
      "id": "by-polatsk-d47d052c34",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святого великомученика Георгия Победоносцад. Гомель",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in Gomel",
      "id": "by-polatsk-19a6fe02ba",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма cвятого великомученика Георгия Победоносцад. Перебродье",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Great Martyr George the Victorious Church in Perebrodye",
      "id": "by-polatsk-7e938dfb7e",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святой Живоначальной Троицы д. Псуя",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Holy Life-giving Trinity Church in Psuya",
      "id": "by-polatsk-ae4dd93922",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святой Живоначальной Троицыд. Леонполь",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Holy Life-giving Trinity Church in Leonpol",
      "id": "by-polatsk-5ff91552a9",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святых мучениц Минодоры,Митродоры, Нимфодорыг. п. Ушачи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/ushachskoe"
      ],
      "name": "Parish of the Holy Martyrs Minodora, Metrodora, and Nymphodora Church in the urban settlement of Ushachi",
      "id": "by-polatsk-fbec2ceb76",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святого пророка Илиид. Иоды",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of the Prophet Elijah Church in Iody",
      "id": "by-polatsk-41bd2039cb",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма cвятого пророка Илиид. Камайск",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Prophet Elijah Church in Kamaisk",
      "id": "by-polatsk-0d372a87aa",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма святого пророка Илиид. Шкунтики",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of the Prophet Elijah Church in Shkuntiki",
      "id": "by-polatsk-2b0b6758cd",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Святого Духа с. Козьяны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of the Holy Spirit Church in Kozyany",
      "id": "by-polatsk-1e5b8099b0",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма иконы Божией Матери \"Всех скорбящих Радость\"г. п. Шарковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of the Joy of All Who Sorrow Icon of the Theotokos Church in the urban settlement of Sharkovshchina",
      "id": "by-polatsk-a37512f1b8",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма иконы Божией Матери \"Спорительница хлебов\"а.г. Кушлики",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Multiplier of Wheat Icon of the Theotokos Church in the agrotown of Kushliki",
      "id": "by-polatsk-882776f375",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма иконы Божией Матери \"Нечаянная Радость\"г. Новополоцк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Unexpected Joy Icon of the Theotokos Church in Novopolotsk",
      "id": "by-polatsk-064aeacdd7",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицы (Молитвенный дом)д. Дубровка",
      "rank": "Prayer House",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/ushachskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Prayer House in Dubrovka",
      "id": "by-polatsk-9158a13a2e",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Богино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Bogino",
      "id": "by-polatsk-c7989fc13f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицы д. Бушики",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Bushiki",
      "id": "by-polatsk-78ee8ce72a",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицыд. Дедино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Dedino",
      "id": "by-polatsk-d26484f453",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицыг. Докшицы",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Dokshitsy",
      "id": "by-polatsk-c95e77c322",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицыд. Ласица",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Lasitsa",
      "id": "by-polatsk-d73e334b5a",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицыд. Осиногородок",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Osinogorodok",
      "id": "by-polatsk-a7ba43ba81",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицыг. Полоцк",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Polatsk",
      "id": "by-polatsk-9b3cf6b0ad",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Покрова Пресвятой Богородицыд. Труды",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Protection of the Most Holy Theotokos Church in Trudy",
      "id": "by-polatsk-c3de8ac217",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Иверской иконы Божией Материд.Мыщено",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Iveron Icon of the Theotokos Church in Myshcheno",
      "id": "by-polatsk-3425cfd2b4",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма казанской иконы Божией Матери д.Борковичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of the Kazan Icon of the Theotokos Church in Borkovichi",
      "id": "by-polatsk-7874252521",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Казанской иконы Божией Матери д. Новый Двор",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of the Kazan Icon of the Theotokos Church in Novy Dvor",
      "id": "by-polatsk-47a16ff11b",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма мученицы Параскевы Пятницы д. Черневичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Great Martyr Paraskeva Church in Chernevichi",
      "id": "by-polatsk-79e8686bf4",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма мученицы Параскевы Пятницы д. Плиса",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Great Martyr Paraskeva Church in Plisa",
      "id": "by-polatsk-151e6a042f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Рождества святого Иоанна Предтечид. Груздова",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of the Nativity of Saint John the Baptist Church in Gruzdovo",
      "id": "by-polatsk-ca4a8d23e6",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Рождества Пресвятой Богородицы д. Голубичи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Nativity of the Most Holy Theotokos Church in Golubichi",
      "id": "by-polatsk-b6f4343057",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Рождества Пресвятой Богородицыд. Богатырская",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Nativity of the Most Holy Theotokos Church in Bogatyrskaya",
      "id": "by-polatsk-f01231ae64",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Рождества Пресвятой Богородицыс. Лужки",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/sharkovshchinskoe"
      ],
      "name": "Parish of the Nativity of the Most Holy Theotokos Church in Luzhki",
      "id": "by-polatsk-8d6f5e5c4c",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Рождества Пресвятой Богородицыд. Вороничи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Nativity of the Most Holy Theotokos Church in Voronichi",
      "id": "by-polatsk-e23beac59d",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма положения ризы Пресвятой Богородицы во Влахернег. Миоры",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Deposition of the Robe of the Most Holy Theotokos at Blachernae Church in Miory",
      "id": "by-polatsk-d91159c8f9",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Сретения Господня и преподобного Серафима Саровскогог.п. Ветрино",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Meeting of the Lord and Venerable Seraphim of Sarov Church in the urban settlement of Vetrino",
      "id": "by-polatsk-a2fac35205",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма пророка Иоанна Предтечи д. Бобруйщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Prophet John the Baptist Church in Bobruishchyna",
      "id": "by-polatsk-26f3b57256",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Воскресения Христоваг. Дисна",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Resurrection of Christ Church in Disna",
      "id": "by-polatsk-8e5a317b25",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Воскресения Христоваг.п. Воропаево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/postavskoe"
      ],
      "name": "Parish of the Resurrection of Christ Church in the urban settlement of Voropaevo",
      "id": "by-polatsk-af9550f1af",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Преображения Господня д. Чурилово",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/verkhnedvinskoe"
      ],
      "name": "Parish of the Transfiguration of the Lord Church in Churilovo",
      "id": "by-polatsk-0285513f53",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Преображения Господня д. Мамаи",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Transfiguration of the Lord Church in Mamai",
      "id": "by-polatsk-c4ec199fe1",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Преображения Господняд. Язно",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Transfiguration of the Lord Church in Yazno",
      "id": "by-polatsk-18b9afeada",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Преображения Господняд. Порплище",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Transfiguration of the Lord Church in Porplishche",
      "id": "by-polatsk-765b790b98",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Преображения Господняд. Шпаковщина",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/polotskoe"
      ],
      "name": "Parish of the Transfiguration of the Lord Church in Shpakovshchina",
      "id": "by-polatsk-92b3315e8f",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Преображения Господня с. Верхнее",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/glubokskoe"
      ],
      "name": "Parish of the Transfiguration of the Lord Church in Verkhneye",
      "id": "by-polatsk-74427a403e",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Свято-Пантелеимоновский женский монастырь",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/braslavskoe"
      ],
      "name": "Saint Panteleimon Convent",
      "id": "by-polatsk-b3ecf9a39d",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма Нерукотворного Образа Господняд. Таргуны",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/dokshitskoe"
      ],
      "name": "Parish of the Image of the Savior Not Made by Hands Church in Targuny",
      "id": "by-polatsk-022780f0df",
      "country": "BY"
    },
    {
      "parent": "ru-polatsk",
      "local": "Приход храма нерукотворного образа Господняд. Николаево",
      "rank": "Parish",
      "kind": "parish",
      "sources": [
        "https://eparhia992.by/eparkhiya/blagochiniya/miorskoe"
      ],
      "name": "Parish of the Image of the Savior Not Made by Hands Church in Nikolaevo",
      "id": "by-polatsk-b9684fd0a8",
      "country": "BY"
    }
  ],
  "belarus": [
    {
      "parent": "belarus",
      "local": "Свято-Успенский Жировичский ставропигиальный мужской монастырь",
      "rank": "Monastery",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Holy Dormition Zhirovichi Stauropegial Monastery",
      "id": "by-belarus-79e9aaae11",
      "country": "BY"
    },
    {
      "parent": "belarus",
      "local": "Свято-Рождество-Богородичный ставропигиальный женский монастырь в г. Гродно",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Nativity of the Most Holy Theotokos Stauropegial Convent in Hrodna",
      "id": "by-belarus-00582104af",
      "country": "BY"
    },
    {
      "parent": "belarus",
      "local": "Спасо-Евфросиниевский ставропигиальный женский монастырь в г. Полоцке",
      "rank": "Convent",
      "kind": "monastery",
      "sources": [
        "https://church.by/belorusskiy-ekzarhat/monastyri/"
      ],
      "name": "Savior and Saint Euphrosyne Stauropegial Convent in Polatsk",
      "id": "by-belarus-d3440643aa",
      "country": "BY"
    }
  ]
}

EXPECTED = {
  "belarus": 3,
  "ru-babruysk": 75,
  "ru-barysaw": 97,
  "ru-brest": 211,
  "ru-homel": 159,
  "ru-hrodna": 119,
  "ru-lida": 51,
  "ru-mahilyow": 22,
  "ru-maladzyechna": 115,
  "ru-minsk": 102,
  "ru-navahrudak": 95,
  "ru-pinsk": 74,
  "ru-polatsk": 125,
  "ru-slutsk": 104,
  "ru-turaw": 82,
  "ru-vitebsk": 180
}
EXPECTED_TOTAL = 1614
ALLOWED_KINDS = {"parish", "monastery"}
ALLOWED_RANKS = {
    "Parish", "Church", "Cathedral", "Cathedral Parish", "Chapel",
    "House Church", "Prayer House", "Prayer Room", "Metochion",
    "Monastery", "Convent", "Skete",
}
FORBIDDEN = ("\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
             "\u00ab", "\u00bb", "\ufffd")
BAD_ENGLISH_FRAGMENTS = (
    "borisoglebsky", "joy of all who sorry", "blgv", " book ",
    "arrival ", "spreader of loaves", "support of sinners", "supportress",
    "vsetsaritsa", "all-tsarina", "pattern maker", "sotnik", "trimif",
    "barkolabovsky", "cosmo - damianovsky", "cross - vozdvizhensky",
    "elizabethin", "georgievsky", "ilyinsky", "nicolo-sophia",
    "petro - paul", "room church", "sretensky", "tephenal", "vedensky",
    "ioanno-kormyansky", "nikolsky monastery", "spaso-preobrazhensky",
    "duhad", "baby gabriel", "panteleimonag", "god materi", "materona",
    "grand martyr.", 'religious organization "religious community"',
)
NON_BODY_LOCALS = {"Монастыри", "Храмы и монастыри"}
EXCLUDED_NON_BODY_IDS = {
    "by-mahilyow-245330a4b1", "by-mahilyow-d02f9fc737",
    "by-minsk-81ee974f8e", "by-minsk-5fead28d39",
    "by-minsk-adbb8465aa", "by-minsk-00ba2345de",
    "by-minsk-99efd53162", "by-minsk-1963aac663",
    "by-minsk-7a908651b0", "by-minsk-1a947c44d8",
    "by-minsk-958a44e290", "by-minsk-8af6b20b9b",
}
RANK_LABELS = {
    "Parish": "Parish",
    "Church": "Church",
    "Cathedral": "Cathedral",
    "Cathedral Parish": "Cathedral",
    "Chapel": "Chapel",
    "House Church": "House Church",
    "Prayer House": "Prayer House",
    "Prayer Room": "Prayer Room",
    "Metochion": "Metochion",
    "Monastery": "Monastery",
    "Convent": "Convent",
    "Skete": "Skete",
}

ALL_SOURCE_ROWS = [
    row for source_rows in RAW_ROWS.values() for row in source_rows
]
ENGLISH_NAMES = {row["id"]: row["name"] for row in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {}


def clean(source):
    row = {
        key: list(value) if isinstance(value, list) else value
        for key, value in source.items()
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
    if row.get("address") and (
            not isinstance(row["address"], list) or
            not all(isinstance(value, str) for value in row["address"])):
        raise ValueError("%s has an invalid address" % row.get("id"))
    return row


def validate_rows(source_rows, parent, seen):
    rows = []
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != parent:
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if row.get("country") != "BY":
            raise ValueError("%s is outside Belarus" % row_id)
        if row.get("kind") not in ALLOWED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable name or local name" % row_id)
        if row.get("address"):
            rendered_address = " ".join(row["address"]).casefold()
            if re.search(r"(?:\bтел|\bмоб|\bфакс|\+375)", rendered_address):
                raise ValueError("%s publishes a telephone or fax number" % row_id)
        if row["local"].startswith("Благочинный ") or row["local"] in NON_BODY_LOCALS:
            raise ValueError("%s is an administrative label, not a body" % row_id)
        english_name = row["name"].casefold()
        for fragment in BAD_ENGLISH_FRAGMENTS:
            if fragment in english_name:
                raise ValueError(
                    "%s carries machine-literal English: %s"
                    % (row_id, fragment)
                )
        expected_label = RANK_LABELS.get(row["rank"])
        if expected_label and expected_label.casefold() not in english_name:
            raise ValueError(
                "%s English name does not match its %s rank"
                % (row_id, row["rank"])
            )
        public_row = {
            key: value for key, value in row.items() if key != "local"
        }
        rendered = json.dumps(public_row, ensure_ascii=False)
        if any(mark in rendered for mark in FORBIDDEN):
            raise ValueError("%s has forbidden punctuation or encoding" % row_id)
        seen.add(row_id)
        rows.append(row)
    return rows


def build_all():
    seen = set(RAW_ROWS)
    payloads = {}
    for parent, source_rows in RAW_ROWS.items():
        rows = validate_rows(source_rows, parent, seen)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "BY",
            "rows": rows,
        }
    total = sum(len(payload["rows"]) for payload in payloads.values())
    if total != EXPECTED_TOTAL:
        raise ValueError("Belarus total must remain %d" % EXPECTED_TOTAL)
    row_ids = {
        row["id"] for payload in payloads.values() for row in payload["rows"]
    }
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Belarus English name map is out of sync")
    return payloads


def build():
    return build_all()


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["BY"]:
        raise ValueError("Belarus candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Belarus candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("total") != EXPECTED_TOTAL:
        raise ValueError("Belarus candidate ledger total is out of sync")
    for parent, expected in EXPECTED.items():
        if summary.get(parent) != expected:
            raise ValueError("Belarus ledger count is out of sync for %s" % parent)
    required = (
        "candidates", "exclusions", "official_jurisdiction_audit",
        "source_reconciliations",
    )
    for key in required:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Belarus candidate ledger lacks %s" % key)
    item_ids = []
    for section in ("candidates", "exclusions"):
        for item in ledger[section]:
            item_id = item.get("candidate_id")
            if not item_id or not re.fullmatch(r"[a-z0-9-]+", item_id):
                raise ValueError("candidate ledger carries an invalid id")
            if item.get("country") != "BY":
                raise ValueError("%s is outside Belarus" % item_id)
            item_ids.append(item_id)
    if len(item_ids) != len(set(item_ids)):
        raise ValueError("Belarus candidate ledger has duplicate ids")
    held_nonbody_ids = set()
    for exclusion in ledger["exclusions"]:
        for item in exclusion.get("items") or []:
            item_id = item.get("id")
            local = item.get("local")
            source = item.get("source")
            if not item_id or not local or not str(source).startswith("https://"):
                raise ValueError(
                    "Belarus non-body exclusion lacks exact source evidence"
                )
            if item_id in held_nonbody_ids:
                raise ValueError("Belarus non-body exclusion has duplicate ids")
            held_nonbody_ids.add(item_id)
    if held_nonbody_ids != EXCLUDED_NON_BODY_IDS:
        raise ValueError("Belarus non-body exclusion ledger is out of sync")
    for section in required:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Belarus ledger item must cite one to three sources"
                )
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError(
                    "Belarus ledger item carries a non-HTTPS source"
                )
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in FORBIDDEN):
        raise ValueError("Belarus candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build_all()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Belarus: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Belarus: %d current bodies across %d canonical parents"
            % (EXPECTED_TOTAL, len(EXPECTED))
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
