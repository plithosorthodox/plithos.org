#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Cameroon.

The Moscow Patriarchate's North African Diocese currently reports 27
parishes across Cameroon's Central and Western deaneries. Current official
reports identify 24 of those parishes by both dedication and place. The
count-only remainder and older Alexandrian body-level records stay in the
companion candidate ledger.

    python tools/directory_cameroon.py --check
    python tools/directory_cameroon.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

RU_ROSTER = (
    "https://exarchate-africa.ru/en/dioceses_cat/diocese-of-north-africa/"
)
RU_YAOUNDE_PASCHA = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-svyatoj-pashi-v-stolicze-kameruna-soversheny-"
    "bogosluzheniya-i-tainstvo-kreshheniya/"
)
RU_DEMETRIUS = (
    "https://exarchate-africa.ru/novosti/"
    "prestolnyj-prazdnik-otmetili-na-prihode-velikomuchenika-"
    "dimitriya-solunskogo-v-stolicze-kameruna/"
)
RU_SERAPHIM = (
    "https://exarchate-africa.ru/novosti/"
    "priobreteny-eshhe-dva-tenta-dlya-prihodov-v-kenii-i-kamerune/"
)
RU_BENEDICT = (
    "https://exarchate-africa.ru/novosti/"
    "v-nedelyu-vseh-svyatyh-v-zemle-egipetskoj-prosiyavshih-v-"
    "stolicze-kameruna-krestilis-12-chelovek/"
)
RU_RAPHAEL = (
    "https://exarchate-africa.ru/bez-rubriki/"
    "v-stolicze-kameruna-k-czerkvi-hristovoj-prisoedinilis-"
    "shestnadczat-chelovek/"
)
RU_ANNUNCIATION = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-blagoveshheniya-presvyatoj-bogorodiczy-sostoyalsya-"
    "prestolnyj-prazdnik-na-blagoveshhenskom-prihode-v-kamerune/"
)
RU_NICHOLAS = (
    "https://exarchate-africa.ru/novosti/"
    "37-zhitelej-kamerunskogo-seleniya-ntui-stali-chadami-czerkvi-"
    "hristovoj/"
)
RU_FAR_NORTH = (
    "https://exarchate-africa.ru/novosti/"
    "sostoyalas-poezdka-svyashhennika-georgiya-maksimova-v-region-"
    "krajnij-sever-kameruna/"
)
RU_FAR_NORTH_WATER = (
    "https://exarchate-africa.ru/novosti/"
    "obustroeny-skvazhiny-na-prihodah-svyatitelya-nektariya-i-"
    "svyatitelya-aleksiya-v-kamerune/"
)
RU_FAR_NORTH_PASCHA = (
    "https://exarchate-africa.ru/novosti/"
    "v-regione-krajnij-sever-kameruna-24-zhitelya-prinyali-"
    "tainstvo-kreshheniya/"
)
RU_PETER_PAUL = (
    "https://exarchate-africa.ru/novosti/"
    "provedena-beseda-po-osnovam-pravoslavnoj-very-v-obshhine-"
    "svyatyh-apostolov-petra-i-pavla-na-severe-kameruna/"
)
RU_JOHN_BABLA = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-pokrova-presvyatoj-bogorodiczy-na-severe-kameruna-"
    "25-zhitelej-prinyali-tainstvo-kreshheniya/"
)
RU_TRINITY = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-uspeniya-presvyatoj-bogorodiczy-v-kamerune-v-"
    "czerkov-hristovu-vstupili-10-chelovek/"
)
RU_NATIVITY_JOHN = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihode-rozhdestva-ioanna-predtechi-v-kamerune-proshli-"
    "prestolnye-torzhestva/"
)
RU_ALL_SAINTS = (
    "https://exarchate-africa.ru/novosti/"
    "prazdnik-uspeniya-presvyatoj-bogorodiczy-otmetili-na-prihode-"
    "vseh-svyatyh-v-g-bertua-kamerun/"
)
RU_DORMITION_EBOLOWA = (
    "https://exarchate-africa.ru/novosti/"
    "na-uspenskom-prihode-na-yuge-kameruna-sostoyalos-tainstvo-"
    "kreshheniya/"
)
RU_WESTERN_2024 = (
    "https://exarchate-africa.ru/novosti/"
    "eshhe-46-chelovek-byli-prinyaty-v-russkuyu-pravoslavnuyu-"
    "czerkov-v-kamerun/"
)


def row(row_id, name, local, sources):
    return {
        "id": row_id,
        "parent": "ru-north-africa",
        "kind": "parish",
        "rank": "Parish",
        "name": name,
        "local": local,
        "country": "CM",
        "sources": sources,
    }


ROWS = [
    row(
        "cm-ru-yaounde-resurrection-christ",
        "Parish of the Resurrection of Christ in Yaounde",
        "Приход Воскресения Христова в Яунде",
        [RU_ROSTER, RU_YAOUNDE_PASCHA],
    ),
    row(
        "cm-ru-yaounde-demetrius-thessalonica",
        "Parish of the Great Martyr Demetrius of Thessalonica in Yaounde",
        "Приход великомученика Димитрия Солунского в Яунде",
        [RU_DEMETRIUS],
    ),
    row(
        "cm-ru-yaounde-seraphim-sarov",
        "Parish of Saint Seraphim of Sarov in Yaounde",
        "Приход преподобного Серафима Саровского в Яунде",
        [RU_SERAPHIM],
    ),
    row(
        "cm-ru-yaounde-benedict-nursia",
        "Parish of Saint Benedict of Nursia in Yaounde",
        "Приход преподобного Венедикта Нурсийского в Яунде",
        [RU_BENEDICT],
    ),
    row(
        "cm-ru-yaounde-archangel-raphael",
        "Parish of the Archangel Raphael in Yaounde",
        "Приход Архангела Рафаила в Яунде",
        [RU_RAPHAEL],
    ),
    row(
        "cm-ru-mbalmayo-annunciation",
        "Parish of the Annunciation in Mbalmayo",
        "Благовещенский приход в Мбальмайо",
        [RU_ANNUNCIATION],
    ),
    row(
        "cm-ru-ntui-nicholas",
        "Parish of Saint Nicholas the Wonderworker in Ntui",
        "Приход святителя Николая Чудотворца в Нтуи",
        [RU_NICHOLAS],
    ),
    row(
        "cm-ru-gadissou-nectarios-aegina",
        "Parish of Saint Nectarios of Aegina in Gadissou",
        "Приход святителя Нектария Эгинского в Гадиссу",
        [RU_FAR_NORTH, RU_FAR_NORTH_WATER],
    ),
    row(
        "cm-ru-varkalak-gerasimos-jordan",
        "Parish of Saint Gerasimos of the Jordan in Varkalak",
        "Приход преподобного Герасима Иорданского в Варкалаке",
        [RU_FAR_NORTH],
    ),
    row(
        "cm-ru-gangalang-alexius-moscow",
        "Parish of Saint Alexius of Moscow in Gangalang",
        "Приход святителя Алексия Московского в Гангаланге",
        [RU_FAR_NORTH, RU_FAR_NORTH_WATER],
    ),
    row(
        "cm-ru-mulwudaye-demetrius-rostov",
        "Parish of Saint Demetrius of Rostov in Mulwudaye",
        "Приход святителя Димитрия Ростовского в Мулвудайе",
        [RU_FAR_NORTH, RU_FAR_NORTH_PASCHA],
    ),
    row(
        "cm-ru-doukoulah-sergius-radonezh",
        "Parish of Saint Sergius of Radonezh in Doukoulah",
        "Приход преподобного Сергия Радонежского в Дукуле",
        [RU_FAR_NORTH, RU_FAR_NORTH_PASCHA],
    ),
    row(
        "cm-ru-djawar-cyril",
        "Parish of Saint Cyril in Djawar",
        "Приход равноапостольного Кирилла в Джаваре",
        [RU_FAR_NORTH],
    ),
    row(
        "cm-ru-dikdim-macarius-moscow",
        "Parish of Saint Macarius of Moscow in Dikdim",
        "Приход святителя Макария Московского в Дикдиме",
        [RU_FAR_NORTH, RU_FAR_NORTH_WATER],
    ),
    row(
        "cm-ru-tungui-george",
        "Parish of the Great Martyr George in Tungui",
        "Приход великомученика Георгия Победоносца в Тунгуи",
        [RU_FAR_NORTH, RU_FAR_NORTH_WATER],
    ),
    row(
        "cm-ru-kourbi-panteleimon",
        "Parish of the Great Martyr Panteleimon in Kourbi",
        "Приход великомученика Пантелеимона в Курби",
        [RU_FAR_NORTH_WATER],
    ),
    row(
        "cm-ru-dobinga-peter-paul",
        "Parish of the Holy Apostles Peter and Paul in Dobinga",
        "Приход святых апостолов Петра и Павла в Добинге",
        [RU_PETER_PAUL],
    ),
    row(
        "cm-ru-babla-john-baptist",
        "Parish of Saint John the Baptist in Babla",
        "Приход святого Иоанна Предтечи в Бабле",
        [RU_JOHN_BABLA],
    ),
    row(
        "cm-ru-douala-life-giving-trinity",
        "Parish of the Life-Giving Trinity in Douala",
        "Приход Живоначальной Троицы в Дуале",
        [RU_ROSTER, RU_TRINITY],
    ),
    row(
        "cm-ru-douala-nativity-john-baptist",
        "Parish of the Nativity of Saint John the Baptist in Douala",
        "Приход Рождества Иоанна Предтечи в Дуале",
        [RU_NATIVITY_JOHN],
    ),
    row(
        "cm-ru-bertoua-all-saints",
        "Parish of All Saints in Bertoua",
        "Приход Всех святых в Бертуа",
        [RU_ALL_SAINTS],
    ),
    row(
        "cm-ru-ebolowa-dormition",
        "Parish of the Dormition of the Theotokos in Ebolowa",
        "Приход Успения Пресвятой Богородицы в Эболове",
        [RU_DORMITION_EBOLOWA],
    ),
    row(
        "cm-ru-bivong-bane-dormition",
        "Parish of the Dormition of the Theotokos in Bivong-Bane",
        "Приход Успения Пресвятой Богородицы в Бивонг-Бане",
        [RU_WESTERN_2024],
    ),
    row(
        "cm-ru-bikok-constantine-helen",
        "Parish of Saints Constantine and Helen in Bikok",
        "Приход равноапостольных Константина и Елены в Бикоке",
        [RU_WESTERN_2024],
    ),
]

EXPECTED = 24
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % item.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    rendered = json.dumps(item, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         item.get("id"))
    return item


def build():
    rows = []
    seen = {"ru-north-africa"}
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if item.get("parent") != "ru-north-africa":
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if item.get("country") != "CM":
            raise ValueError("%s is outside Cameroon" % row_id)
        if item.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if not item.get("name") or not item.get("local"):
            raise ValueError("%s lacks a usable name" % row_id)
        seen.add(row_id)
        rows.append(item)
    if len(rows) != EXPECTED:
        raise ValueError("Cameroon must publish exactly %d rows" % EXPECTED)
    if set(ENGLISH_NAMES) != seen - {"ru-north-africa"}:
        raise ValueError("Cameroon English name map is out of sync")
    return {
        "ru-north-africa": {
            "v": 1,
            "parent": "ru-north-africa",
            "country": "CM",
            "rows": rows,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Cameroon: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Cameroon: 24 current officially named bodies under the Moscow "
          "Patriarchate, plus the existing Alexandrian diocesan parent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
