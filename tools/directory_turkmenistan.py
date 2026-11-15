#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Turkmenistan.

The official site of the Patriarchal Deanery of the Parishes of the Russian
Orthodox Church in Turkmenistan publishes all twelve current churches under
its three church districts. Each row below is taken from that roster and its
individual church page.

    python tools/directory_turkmenistan.py --check
    python tools/directory_turkmenistan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

DEANERY = "https://orthodoxy.tm/"
PATRIARCHATE = "https://patriarchia.ru/org/262"
ASHGABAT_DISTRICT = "https://orthodoxy.tm/site/articles?catids%5B0%5D=8"
BALKAN_DISTRICT = "https://orthodoxy.tm/site/articles?catids%5B0%5D=9"
TURKMENABAT_DISTRICT = "https://orthodoxy.tm/site/articles?catids%5B0%5D=10"


def body(row_id, name, local, seat, address, page, district):
    return {
        "id": row_id,
        "parent": "ru-turkmenistan",
        "kind": "parish",
        "rank": "Church",
        "name": name,
        "local": local,
        "seat": seat,
        "country": "TM",
        "address": address,
        "site": page,
        "sources": [page, district, PATRIARCHATE],
    }


ROWS = {
    "ru-turkmenistan": [
        body(
            "tm-ru-ashgabat-alexander-nevsky",
            "Saint Alexander Nevsky Church in Ashgabat",
            "храм святого благоверного великого князя Александра Невского",
            "Ashgabat",
            ["744012, г. Ашхабад", "30-й мкр, ул. Махтумкули 176/1"],
            "https://orthodoxy.tm/209",
            ASHGABAT_DISTRICT,
        ),
        body(
            "tm-ru-ashgabat-saint-nicholas",
            "Saint Nicholas the Wonderworker Church in Ashgabat",
            "храм святителя и Чудотворца Николая",
            "Ashgabat",
            ["744002, г. Ашхабад", "ул. 2091, ул. Амандурды Мередова 1"],
            "https://orthodoxy.tm/210",
            ASHGABAT_DISTRICT,
        ),
        body(
            "tm-ru-ashgabat-resurrection",
            "Church of the Resurrection of Christ in Ashgabat",
            "храм Воскресения Христова",
            "Ashgabat",
            ["г. Ашхабад", "проспект Туркменбаши шаёлы, 38 А"],
            "https://orthodoxy.tm/211",
            ASHGABAT_DISTRICT,
        ),
        body(
            "tm-ru-ashgabat-cyril-methodius",
            "Saints Cyril and Methodius Church in Ashgabat",
            "храм святых равноапостольных Кирилла и Мефодия",
            "Ashgabat",
            [
                "745222, г. Ашхабад",
                "микрорайон Абадан, Абаданское шоссе, 150 Б",
            ],
            "https://orthodoxy.tm/212",
            ASHGABAT_DISTRICT,
        ),
        body(
            "tm-ru-tejen-apostle-thomas",
            "Holy Apostle Thomas Church in Tejen",
            "храм святого апостола Фомы",
            "Tejen",
            ["г. Теджен", "ул. Кероглы 12"],
            "https://orthodoxy.tm/213",
            ASHGABAT_DISTRICT,
        ),
        body(
            "tm-ru-dashoguz-seeking-the-lost",
            "Church of the Seeking the Lost Icon of the Mother of God in Dashoguz",
            "храм в честь иконы Божией Матери \"Взыскание погибших\"",
            "Dashoguz",
            ["г. Дашогуз", "ул. Гёроглы, д. 2/1"],
            "https://orthodoxy.tm/214",
            ASHGABAT_DISTRICT,
        ),
        body(
            "tm-ru-balkanabat-nativity-theotokos",
            "Nativity of the Most Holy Theotokos Church in Balkanabat",
            "храм Рождества Пресвятой Богородицы",
            "Balkanabat",
            ["Балканский велаят, г. Балканабат", "216 квартал, улица Эсгерлер"],
            "https://orthodoxy.tm/220",
            BALKAN_DISTRICT,
        ),
        body(
            "tm-ru-turkmenbashi-archangel-michael",
            "Archangel Michael Church in Turkmenbashi",
            "храм Архистратига Божия Михаила",
            "Turkmenbashi",
            ["745000, г. Туркменбаши", "ул. Оразовой, 28"],
            "https://orthodoxy.tm/219",
            BALKAN_DISTRICT,
        ),
        body(
            "tm-ru-turkmenabat-peter-paul",
            "Holy Apostles Peter and Paul Church in Turkmenabat",
            "храм святых первоверховных апостолов Петра и Павла",
            "Turkmenabat",
            ["746100, г. Туркменабад", "ул. Берды Кербабаева, 1"],
            "https://orthodoxy.tm/218",
            TURKMENABAT_DISTRICT,
        ),
        body(
            "tm-ru-turkmenabat-saint-nicholas",
            "Saint Nicholas the Wonderworker Church in Turkmenabat",
            "храм святителя Николая Чудотворца",
            "Turkmenabat",
            ["г. Туркменабад", "проспект Махтумкули, 16 А"],
            "https://orthodoxy.tm/217",
            TURKMENABAT_DISTRICT,
        ),
        body(
            "tm-ru-bayramaly-saint-alexis",
            "Saint Alexis, Metropolitan of Moscow Church in Bayramaly",
            "храм святителя Алексия, Митрополита Московского",
            "Bayramaly",
            ["746000, г. Байрамали", "ул. Заруднева, 6"],
            "https://orthodoxy.tm/216",
            TURKMENABAT_DISTRICT,
        ),
        body(
            "tm-ru-mary-protection-theotokos",
            "Protection of the Mother of God Church in Mary",
            "храм Покрова Божией Матери",
            "Mary",
            ["745400, г. Мары", "ул. Сейди, 8/10"],
            "https://orthodoxy.tm/215",
            TURKMENABAT_DISTRICT,
        ),
    ],
}
EXPECTED = {"ru-turkmenistan": 12}
EXPECTED_TOTAL = 12
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in ROWS.values()
    for row in rows
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
    if row.get("site") and not row["site"].startswith("https://"):
        raise ValueError("%s carries a non-HTTPS site" % row.get("id"))
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    return row


def build():
    payloads = {}
    seen = set(ROWS)
    total = 0
    for parent, source_rows in ROWS.items():
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
            if row.get("country") != "TM":
                raise ValueError("%s is outside Turkmenistan" % row_id)
            if row.get("kind") != "parish":
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        total += len(rows)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "TM",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Turkmenistan must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Turkmenistan English name map is out of sync")
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
        print("directory Turkmenistan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Turkmenistan: 12 current churches under the Russian Orthodox Church")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
