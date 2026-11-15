#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Uzbekistan.

The official Tashkent and Uzbekistan Diocese parish roster names 38 bodies.
Its current parish galleries and recent official reports establish ten more
active bodies which have not yet been added to that text roster.

    python tools/directory_uzbekistan.py --check
    python tools/directory_uzbekistan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
PARENT = "ru-tashkent"
PARISHES = "https://pravoslavie.uz/archdiocese/parishes/"


def body(row_id, name, local, seat, rank="Church", kind="parish",
         address=None, sources=None):
    row = {
        "id": row_id,
        "parent": PARENT,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "UZ",
        "sources": list(sources or [PARISHES]),
    }
    if address:
        row["address"] = list(address)
    return row


ROWS = {PARENT: [
    body(
        "uz-ru-almalyk-dormition",
        "Dormition of the Most Holy Theotokos Church in Almalyk",
        u"Храм Успения Пресвятой Богородицы",
        "Almalyk",
        address=[u"104-й квартал, ул. Алпомыш 29", u"702400, г. Алмалык"],
    ),
    body(
        "uz-ru-angren-seeking-lost",
        "Seeking the Lost Icon of the Mother of God Prayer House in Angren",
        u"Молитвенный дом в честь иконы Божией Матери «Взыскание погибших»",
        "Angren",
        rank="Prayer House",
        address=[u"ул. Алмалыкская, 33", u"702500, г. Ангрен, Ташкентская область"],
    ),
    body(
        "uz-ru-andijan-all-saints",
        "All Saints Prayer House in Andijan",
        u"Молитвенный дом Всех святых",
        "Andijan",
        rank="Prayer House",
        address=[u"ул. Мусаева, 10", u"710000, г. Андижан"],
    ),
    body(
        "uz-ru-akhangaran-apostle-thomas",
        "Holy Apostle Thomas Prayer House in Akhangaran",
        u"Молитвенный дом святого апостола Фомы",
        "Akhangaran",
        rank="Prayer House",
        address=[u"53-й квартал, ул. Ахунбабаева, д. 2", u"г. Ахангаран, Ташкентская область"],
    ),
    body(
        "uz-ru-bekabad-presentation",
        "Presentation of the Lord Church in Bekabad",
        u"Храм Сретения Господня",
        "Bekabad",
        address=[u"ул. Поповича, 2", u"702902, г. Бекабад, Ташкентская область"],
    ),
    body(
        "uz-ru-bukhara-archangel-michael",
        "Archangel Michael Church in Bukhara",
        u"Храм Архистратига Михаила",
        "Bukhara",
        address=[u"ул. Карши Дарвоза, 4", u"705004, г. Бухара"],
    ),
    body(
        "uz-ru-gazalkent-joy-all-sorrow",
        "Joy of All Who Sorrow Icon of the Mother of God Prayer House in Gazalkent",
        u"Молитвенный дом в честь иконы Божией Матери «Всех скорбящих Радосте»",
        "Gazalkent",
        rank="Prayer House",
        address=[u"ул. Дустлик, 15", u"702180, г. Газалкент"],
    ),
    body(
        "uz-ru-gulistan-saint-nicholas",
        "Saint Nicholas the Wonderworker Church in Gulistan",
        u"Храм святителя Николая, архиепископа Мир Ликийских, чудотворца",
        "Gulistan",
        address=[u"ул. Туркестанская, 94", u"707000, г. Гулистан, Сырдарьинская область"],
    ),
    body(
        "uz-ru-denau-protection-theotokos",
        "Protection of the Most Holy Theotokos Prayer House in Denau",
        u"Молитвенный дом Покрова Пресвятой Богородицы",
        "Denau",
        rank="Prayer House",
        address=[u"ул. Нозима Мирзаева, 46", u"733500, г. Денау, Сурхандарьинская область"],
    ),
    body(
        "uz-ru-jizzakh-saint-nicholas",
        "Saint Nicholas the Wonderworker Church in Jizzakh",
        u"Храм святителя Николая, архиепископа Мир Ликийских, чудотворца",
        "Jizzakh",
        address=[u"ул. О. Азимова, 7", u"708000, г. Джизак"],
    ),
    body(
        "uz-ru-dostabad-protection-convent",
        "Holy Protection Convent in Dostabad",
        u"Свято-Покровский женский монастырь",
        "Dostabad",
        rank="Convent",
        kind="monastery",
        address=[u"ул. Баркамол овлод, 85", u"110900, г. Достабад, Ташкентская область"],
    ),
    body(
        "uz-ru-zarafshan-saint-nicholas",
        "Saint Nicholas the Wonderworker Church in Zarafshan",
        u"Храм Святителя Николая, архиепископа Мир Ликийских, чудотворца",
        "Zarafshan",
        address=[u"ул. Мира, 1", u"706801, г. Зарафшан, Навоийская область"],
    ),
    body(
        "uz-ru-kagan-saint-nicholas",
        "Saint Nicholas the Wonderworker Church in Kagan",
        u"Храм Святителя Николая, архиепископа Мир Ликийских, чудотворца",
        "Kagan",
        address=[u"ул. Истирохат, 186", u"706100, г. Каган, Бухарская область"],
    ),
    body(
        "uz-ru-karshi-protection-theotokos",
        "Protection of the Most Holy Theotokos Prayer House in Karshi",
        u"Молитвенный дом Покрова Пресвятой Богородицы",
        "Karshi",
        rank="Prayer House",
        address=[u"ул. Бозор, 1", u"730000, г. Карши"],
    ),
    body(
        "uz-ru-kattakurgan-saint-vladimir",
        "Holy Equal-to-the-Apostles Grand Prince Vladimir Prayer House in Kattakurgan",
        u"Молитвенный дом святого Равноапостольного великого князя Владимира",
        "Kattakurgan",
        rank="Prayer House",
        address=[u"ул. Закира Рахманова, 7", u"704200, г. Каттакурган, Самаркандская область"],
    ),
    body(
        "uz-ru-kokand-kazan-icon",
        "Kazan Icon of the Mother of God Church in Kokand",
        u"Храм в честь Казанской иконы Божией Матери",
        "Kokand",
        address=[u"ул. Урдатоги, 70", u"713000, г. Коканд"],
    ),
    body(
        "uz-ru-krasnogorsk-faith-hope-love-sophia",
        "Holy Martyrs Faith, Hope, Love, and Their Mother Sophia Prayer House in Krasnogorsk",
        u"Молитвенный дом святых мучениц Веры, Надежды, Любови и матери их Софии",
        "Krasnogorsk",
        rank="Prayer House",
    ),
    body(
        "uz-ru-kuvasay-john-kronstadt",
        "Saint John of Kronstadt Church in Kuvasay",
        u"Храм святого праведного Иоанна Кронштадтского",
        "Kuvasay",
        address=[u"ул. Мустакиллик, 21", u"713830, г. Кувасай, Ферганская область"],
    ),
    body(
        "uz-ru-navoi-saint-sergius",
        "Saint Sergius of Radonezh Church in Navoi",
        u"Храм Преподобного Сергия Радонежского",
        "Navoi",
        address=[u"ул. Ибн-Сино, 26а", u"706800, г. Навои"],
    ),
    body(
        "uz-ru-namangan-archangel-michael",
        "Archangel Michael Church in Namangan",
        u"Храм Архангела Божия Михаила",
        "Namangan",
        address=[u"ул. Темир йул, 50", u"718004, г. Наманган"],
    ),
    body(
        "uz-ru-nukus-saint-panteleimon",
        "Saint Panteleimon Church in Nukus",
        u"Храм святого великомученика и целителя Пантелеимона",
        "Nukus",
        address=[u"ул. Таттбаева, 7а", u"742000, г. Нукус, Республика Каракалпакстан"],
    ),
    body(
        "uz-ru-samarkand-saint-george",
        "Saint George the Great Martyr Church in Samarkand",
        u"Храм святого великомученика Георгия Победоносца",
        "Samarkand",
        address=[u"ул. Бирлик, 66", u"140100, г. Самарканд"],
    ),
    body(
        "uz-ru-samarkand-saint-alexis-cathedral",
        "Saint Alexis, Metropolitan of Moscow Cathedral in Samarkand",
        u"Собор святителя Алексия, Митрополита Московского",
        "Samarkand",
        rank="Cathedral",
        address=[u"ул. Бобир-Мирзо, 1", u"140105, г. Самарканд"],
    ),
    body(
        "uz-ru-samarkand-protection-theotokos",
        "Protection of the Most Holy Theotokos Church in Samarkand",
        u"Храм Покрова Пресвятой Богородицы",
        "Samarkand",
        address=[u"ул. Хусейн Бойкаро, 24", u"140100, г. Самарканд"],
    ),
    body(
        "uz-ru-syrdarya-protection-theotokos",
        "Protection of the Most Holy Theotokos Church in Syrdarya",
        u"Храм Покрова Пресвятой Богородицы",
        "Syrdarya",
        address=[u"ул. Гулистан, 97", u"708400, г. Сырдарья"],
    ),
    body(
        "uz-ru-tashkent-dormition-cathedral",
        "Dormition of the Mother of God Cathedral in Tashkent",
        u"Кафедральный собор Успения Божией Матери",
        "Tashkent",
        rank="Cathedral",
        address=[u"ул. Авлиёота, 91", u"700015, г. Ташкент"],
    ),
    body(
        "uz-ru-tashkent-alexander-nevsky",
        "Saint Alexander Nevsky Church in Tashkent",
        u"Храм святого благоверного великого князя Александра Невского",
        "Tashkent",
        address=[u"ул. Боткина, 106", u"г. Ташкент"],
    ),
    body(
        "uz-ru-tashkent-saint-hermogenes",
        "Saint Hermogenes, Patriarch of Moscow Church in Tashkent",
        u"Храм священномученика Ермогена, Патриарха Московского",
        "Tashkent",
        address=[u"ул. Ойшаханум, 1-й тупик, д. 3", u"700143, г. Ташкент"],
    ),
    body(
        "uz-ru-tashkent-saint-vladimir",
        "Holy Equal-to-the-Apostles Grand Prince Vladimir Church in Tashkent",
        u"Храм святого Равноапостольного великого князя Владимира",
        "Tashkent",
        address=[u"ул. Катартал, Домрабадское кладбище № 2", u"700183, г. Ташкент"],
    ),
    body(
        "uz-ru-tashkent-trinity-nicholas-convent",
        "Holy Trinity and Saint Nicholas Convent in Tashkent",
        u"Свято-Троице-Никольский женский монастырь",
        "Tashkent",
        rank="Convent",
        kind="monastery",
        address=[u"ул. 8 марта, 7", u"700005, г. Ташкент"],
    ),
    body(
        "uz-ru-termez-alexander-nevsky",
        "Saint Alexander Nevsky Church in Termez",
        u"Храм святого благоверного великого князя Александра Невского",
        "Termez",
        address=[u"ул. Сафара Сахибова / проспект Ходжаева", u"732000, г. Термез, Сурхандарьинская область"],
    ),
    body(
        "uz-ru-urgench-job-long-suffering",
        "Patriarch Job the Long-Suffering Church in Urgench",
        u"Храм патриарха Иова Многострадального",
        "Urgench",
        address=[u"ул. Ешлик 20/1", u"220100, г. Ургенч, Хорезмская область"],
    ),
    body(
        "uz-ru-uchkuduk-all-saints-russia",
        "All Saints Who Shone Forth in the Russian Land Church in Uchkuduk",
        u"Храм всех святых, в земле Российской просиявших",
        "Uchkuduk",
        address=[u"6 квартал, ул. Амира Темура, д. 28", u"706880, г. Учкудук, Навоийская область"],
    ),
    body(
        "uz-ru-fergana-saint-sergius",
        "Saint Sergius of Radonezh Church in Fergana",
        u"Храм Преподобного Сергия Радонежского",
        "Fergana",
        address=[u"ул. Саккокий, 8", u"712000, г. Фергана"],
    ),
    body(
        "uz-ru-khavast-saint-nicholas",
        "Saint Nicholas the Wonderworker Prayer House in Khavast",
        u"Молитвенный дом святителя Николая, архиепископа Мир Ликийских Чудотворца",
        "Khavast",
        rank="Prayer House",
        address=[u"ул. Ахмад Ясовий, 97", u"708200, пос. Хаваст, г. Янгиер, Сырдарьинская область"],
    ),
    body(
        "uz-ru-chinaz-saint-alexander-kusht",
        "Saint Alexander, Abbot of Kusht Church in Yangi-Chinaz",
        u"Храм преподобного Александра, игумена Куштского",
        "Yangi-Chinaz",
        address=[u"ул. Дустлик, 2а", u"пос. Янги-Чиназ, Чиназский район, Ташкентская область"],
    ),
    body(
        "uz-ru-chirchik-trinity-george-monastery",
        "Holy Trinity and Saint George Monastery in Chirchik",
        u"Свято-Троице-Георгиевский мужской монастырь",
        "Chirchik",
        rank="Monastery",
        kind="monastery",
        address=[u"проспект А. Навои, 1а", u"г. Чирчик, Ташкентская область"],
    ),
    body(
        "uz-ru-yangiyul-seeking-lost",
        "Seeking the Lost Icon of the Mother of God Church in Yangiyul",
        u"Храм в честь иконы Божией Матери «Взыскание погибших»",
        "Yangiyul",
        address=[u"ул. Чарикова, 264", u"702805, г. Янгиюль, Ташкентская область"],
    ),
    body(
        "uz-ru-tashkent-john-baptist-baptistery",
        "Saint John the Forerunner and Baptist Baptistery Church in Tashkent",
        u"Храм-крещальня в честь святого Иоанна Предтечи, Крестителя Господня",
        "Tashkent",
        sources=["https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=4092"],
    ),
    body(
        "uz-ru-tashkent-saint-sergius-synodal-centre",
        "Saint Sergius of Radonezh Church at the Synodal Centre in Tashkent",
        u"Храм преподобного Сергия Радонежского при Синодальном центре Среднеазиатского митрополичьего округа",
        "Tashkent",
        sources=[
            "https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=3887",
            "https://pravoslavie.uz/news/96287/",
        ],
    ),
    body(
        "uz-ru-tashkent-all-saints-russia-house-church",
        "All Saints Who Shone Forth in the Russian Church House Church in Tashkent",
        u"Домовый храм в честь Всех святых, в земле Русской просиявших, при Синоде Среднеазиатского митрополичьего округа",
        "Tashkent",
        rank="House Church",
        sources=[
            "https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=3794",
            "https://pravoslavie.uz/news/115455/",
        ],
    ),
    body(
        "uz-ru-fergana-saint-nicholas-prayer-house",
        "Saint Nicholas the Wonderworker Prayer House in Fergana",
        u"Молитвенный дом в честь святителя Николая, архиепископа Мирликийского, Чудотворца",
        "Fergana",
        rank="Prayer House",
        sources=["https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=3729"],
    ),
    body(
        "uz-ru-tashkent-transfiguration-cathedral",
        "Transfiguration Cathedral Under Construction in Tashkent",
        u"Строящийся Спасо-Преображенский собор",
        "Tashkent",
        rank="Church Under Construction",
        sources=["https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=2962"],
    ),
    body(
        "uz-ru-urtasaray-all-saints-central-asia",
        "Synaxis of All Saints of the Central Asian Metropolitan District Church in Urtasaray",
        u"Храм Собора всех святых Среднеазиатского митрополичьего округа",
        "Urtasaray",
        sources=[
            "https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=2784",
            "https://pravoslavie.uz/news/109454/",
        ],
    ),
    body(
        "uz-ru-tashkent-job-royal-martyrs",
        "Saint Job the Long-Suffering and the Royal Passion-Bearers Church in Tashkent",
        u"Храм в честь святого праведного Иова Многострадального и Царственных страстотерпцев",
        "Tashkent",
        sources=["https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=2340"],
    ),
    body(
        "uz-ru-tashkent-saint-luke-seminary",
        "Saint Luke of Crimea Seminary Church in Tashkent",
        u"Храм святителя Луки Крымского при Ташкентской православной духовной семинарии",
        "Tashkent",
        rank="Seminary Church",
        sources=[
            "https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=1901",
            "https://pravoslavie.uz/news/73673/",
        ],
    ),
    body(
        "uz-ru-dzhambul-archangel-michael",
        "Archangel Michael Church in Dzhambul",
        u"Храм Архангела Божия Михаила",
        "Dzhambul",
        sources=[
            "https://pravoslavie.uz/photo/?PAGE_NAME=section&SECTION_ID=333",
            "https://pravoslavie.uz/news/108195/",
        ],
    ),
    body(
        "uz-ru-tashkent-saint-george-chapel",
        "Saint George the Great Martyr Chapel in Tashkent",
        u"Часовня в честь святого великомученика Георгия Победоносца",
        "Tashkent",
        rank="Chapel",
        sources=["https://pravoslavie.uz/news/117502/"],
    ),
]}

EXPECTED = {PARENT: 48}
EXPECTED_TOTAL = 48
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
            if row.get("country") != "UZ":
                raise ValueError("%s is outside Uzbekistan" % row_id)
            if row.get("kind") not in ("parish", "monastery"):
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
            "country": "UZ",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Uzbekistan must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Uzbekistan English name map is out of sync")
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
        print("directory Uzbekistan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Uzbekistan: 48 current bodies under the Russian Orthodox Church")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
