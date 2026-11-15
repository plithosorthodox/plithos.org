#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Uganda.

Current competent Church sources establish four Alexandrian administrative
centres, two current Alexandrian bodies suitable for this country module,
three Moscow Exarchate deaneries, sixteen individually reconciled Russian
Church parishes or mission bodies, and three separately documented church
construction sites. The live Moscow roster reports twenty-six parishes, so
the aggregate-only remainder and every unresolved identity remain in the
companion candidate ledger.

    python tools/directory_uganda.py --check
    python tools/directory_uganda.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "uganda.json"

AX_KAMPALA = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-mitropoli-kampalas/"
)
AX_UGANDA_OFFICIAL = "https://x.com/Orthodox_ug"
AX_MBARARA_CURRENT = (
    "https://x.com/Orthodox_ug/status/2093285485439270973"
)
AX_NICHOLAS_CURRENT = (
    "https://x.com/Orthodox_ug/status/2094854455694967099"
)

RU_ROSTER_EN = (
    "https://exarchate-africa.ru/en/dioceses_cat/"
    "south-african-diocese/"
)
RU_ROSTER_RU = (
    "https://exarchate-africa.ru/dioceses_cat/"
    "yuzhno-afrikanskaya-eparhiya/"
)
RU_DEANERIES = (
    "https://exarchate-africa.ru/novosti/"
    "sostoyalos-sobranie-blagochinnyh-czerkovnyh-okrugov-ugandy/"
)
RU_TOUR = (
    "https://exarchate-africa.ru/novosti/"
    "zavershilas-poezdka-patriarshego-ekzarha-afriki-v-ugandu/"
)
RU_ALEXIS = (
    "https://exarchate-africa.ru/novosti/"
    "v-nedelyu-26-yu-po-pyatidesyatnicze-mitropolit-konstantin-sovershil-"
    "liturgiyu-na-prihode-svyatitelya-aleksiya-v-ugande/"
)
RU_CENTRAL_MISSION = (
    "https://exarchate-africa.ru/novosti/"
    "obrazovatelnaya-missiya-duhovno-prosvetitelskogo-czentra-apostola-"
    "marka-prodolzhaetsya-v-ugande/"
)
RU_SOPHIA = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-svyatoj-troiczy-na-prihode-mucheniczy-sofii-v-ugande-"
    "krestilis-15-chelovek/"
)
RU_VLADIMIR = (
    "https://exarchate-africa.ru/novosti/"
    "sostoyalos-sobranie-duhovenstva-czentralnogo-blagochiniya-v-ugande/"
)
RU_JOHN = (
    "https://exarchate-africa.ru/novosti/"
    "v-missionerskom-czentre-svyatitelya-ioanna-shanhajskogo-v-ugande-"
    "otsluzhen-moleben-na-nachalo-uchebnogo-goda-2/"
)
RU_JOHN_CONSTRUCTION = (
    "https://exarchate-africa.ru/novosti/"
    "v-den-pamyati-treh-vselenskih-svyatitelej-sovershena-liturgiya-na-"
    "prihode-svyatitelya-ioanna-shanhajskogo-v-ugande/"
)
RU_RUBAARE = (
    "https://exarchate-africa.ru/novosti/"
    "v-vostochnom-blagochinii-ugandy-proshlo-sobranie-duhovenstva-i-"
    "prihozhan/"
)
RU_TRINITY = (
    "https://exarchate-africa.ru/novosti/"
    "v-velikuyu-subbotu-na-zapade-ugandy-tainstvo-kreshheniya-prinyali-"
    "dvadczat-chelovek/"
)
RU_TRINITY_BUILT = (
    "https://exarchate-africa.ru/novosti/"
    "na-vostoke-ugandy-vozveden-hram-v-chest-svyatoj-troiczy/"
)
RU_CATHERINE = (
    "https://exarchate-africa.ru/novosti/"
    "odinnadczat-mestnyh-zhitelej-kreshheny-v-vostochnoj-ugande/"
)
RU_ANTHONY = (
    "https://exarchate-africa.ru/novosti/"
    "shest-chelovek-na-prihode-prepodobnogo-antoniya-velikogo-v-ugande-"
    "proshli-chin-oglasheniya/"
)
RU_PATRICK = (
    "https://exarchate-africa.ru/novosti/"
    "na-vostoke-ugandy-55-mestnyh-zhitelej-prinyali-tainstvo-kreshheniya/"
)
RU_APOSTLE_PETER = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-rozhdestva-presvyatoj-bogorodiczy-v-ugande-soversheny-"
    "tainstva-kreshheniya-i-braka/"
)
RU_TRANSFIGURATION = (
    "https://exarchate-africa.ru/novosti/"
    "v-missionerskom-czentre-svyatitelya-ioanna-shanhajskogo-v-ugande-"
    "kreshheny-32-mestnyh-zhitelya/"
)
RU_LIFE_SPRING = (
    "https://exarchate-africa.ru/novosti/"
    "desyat-zhitelej-na-severe-ugandy-prinyali-tainstvo-kreshheniya/"
)
RU_LIFE_SPRING_CURRENT = (
    "https://exarchate-africa.ru/novosti/"
    "delegacziya-duhovno-prosvetitelskogo-czentra-ekzarhata-posetila-"
    "severnoe-blagochinie-ugandy/"
)
RU_ANNUNCIATION = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-uspeniya-presvyatoj-bogorodiczy-sovershena-liturgiya-na-"
    "ostrove-bukasa-v-ugande/"
)
ROCOR_ANNUNCIATION = (
    "https://directory.synod.com/listing/260/"
    "holy-annunciation-church-of-bukasa-island/"
)


def row(row_id, parent, kind, rank, name, local, sources, seat=None):
    return {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "UG",
        "sources": sources,
    }


ROWS = {
    "alexandria": [
        row(
            "ax-mbarara",
            "alexandria",
            "diocese",
            "Diocese",
            "Holy Diocese of Mbarara and Western Uganda",
            "Holy Diocese of Mbarara and Western Uganda",
            [AX_MBARARA_CURRENT, AX_UGANDA_OFFICIAL],
            "Mbarara",
        ),
    ],
    "ax-kampala": [
        row(
            "ug-ax-kampala-namungoona-nicholas",
            "ax-kampala",
            "parish",
            "Cathedral",
            "Saint Nicholas Cathedral in Namungoona, Kampala",
            "Saint Nicholas Cathedral in Namungoona, Kampala",
            [AX_NICHOLAS_CURRENT, AX_KAMPALA, AX_UGANDA_OFFICIAL],
            "Namungoona, Kampala",
        ),
    ],
    "ru-south-africa": [
        row(
            "ug-ru-central-deanery",
            "ru-south-africa",
            "diocese",
            "Deanery",
            "Central Deanery of Uganda",
            "Центральное благочиние Республики Уганда",
            [RU_ROSTER_EN, RU_ROSTER_RU, RU_DEANERIES],
        ),
        row(
            "ug-ru-eastern-deanery",
            "ru-south-africa",
            "diocese",
            "Deanery",
            "Eastern Deanery of Uganda",
            "Восточное благочиние Республики Уганда",
            [RU_ROSTER_EN, RU_ROSTER_RU, RU_DEANERIES],
        ),
        row(
            "ug-ru-northern-deanery",
            "ru-south-africa",
            "diocese",
            "Deanery",
            "Northern Deanery of Uganda",
            "Северное благочиние Республики Уганда",
            [RU_ROSTER_EN, RU_ROSTER_RU, RU_DEANERIES],
        ),
        row(
            "ug-ru-nkokonjeru-alexis-moscow",
            "ug-ru-central-deanery",
            "parish",
            "Parish",
            "Parish of Saint Alexis, Metropolitan of Moscow, in Nkokonjeru",
            "Приход святителя Алексия, митрополита Московского, в с. Нкоконджеру",
            [RU_ALEXIS, RU_CENTRAL_MISSION, RU_TOUR],
            "Nkokonjeru",
        ),
        row(
            "ug-ru-nkokonjeru-alexis-church-construction",
            "ug-ru-central-deanery",
            "parish",
            "Church Under Construction",
            "Saint Alexis of Moscow Church Under Construction in Nkokonjeru",
            "Строящийся храм святителя Алексия, митрополита Московского, в с. Нкоконджеру",
            [RU_ALEXIS, RU_TOUR],
            "Nkokonjeru",
        ),
        row(
            "ug-ru-mawangala-peter-paul",
            "ug-ru-central-deanery",
            "parish",
            "Parish",
            "Parish of the Holy Apostles Peter and Paul in Mawangala",
            "Приход святых апостолов Петра и Павла в с. Мавангала",
            [RU_CENTRAL_MISSION, RU_ALEXIS, RU_TOUR],
            "Mawangala",
        ),
        row(
            "ug-ru-martyr-sophia",
            "ug-ru-central-deanery",
            "parish",
            "Parish",
            "Parish of the Martyr Sophia",
            "Приход мученицы Софии",
            [RU_SOPHIA, RU_ROSTER_RU],
        ),
        row(
            "ug-ru-bugolo-vladimir",
            "ug-ru-central-deanery",
            "parish",
            "Parish",
            "Parish of Saint Vladimir Equal-to-the-Apostles in Bugolo",
            "Приход святого равноапостольного князя Владимира в с. Буголо",
            [RU_VLADIMIR, RU_ROSTER_RU],
            "Bugolo",
        ),
        row(
            "ug-ru-kiboga-john-shanghai-center",
            "ug-ru-eastern-deanery",
            "parish",
            "Missionary Center",
            "Saint John of Shanghai Missionary Center in Kiboga",
            "Миссионерский центр святителя Иоанна Шанхайского в г. Кибога",
            [RU_JOHN, RU_ROSTER_EN, RU_ROSTER_RU],
            "Kiboga",
        ),
        row(
            "ug-ru-kiboga-john-shanghai-church-construction",
            "ug-ru-eastern-deanery",
            "parish",
            "Church Under Construction",
            "Saint John of Shanghai Church Under Construction in Kiboga",
            "Строящийся храм святителя Иоанна Шанхайского в г. Кибога",
            [RU_JOHN_CONSTRUCTION, RU_TOUR],
            "Kiboga",
        ),
        row(
            "ug-ru-rubaare-symeon-new-theologian",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of Saint Symeon the New Theologian in Rubaare",
            "Приход преподобного Симеона Нового Богослова в г. Рубааре",
            [RU_RUBAARE, RU_TOUR],
            "Rubaare",
        ),
        row(
            "ug-ru-rubaare-all-saints-egypt",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of All Saints Who Shone Forth in the Land of Egypt in Rubaare",
            "Приход Всех святых, в земле Египетской просиявших, в г. Рубааре",
            [RU_RUBAARE, RU_TOUR],
            "Rubaare",
        ),
        row(
            "ug-ru-mwitanzige-holy-trinity",
            "ug-ru-eastern-deanery",
            "parish",
            "Church",
            "Holy Trinity Church in Mwitanzige",
            "Храм Святой Троицы в с. Мвитанзиге",
            [RU_TRINITY, RU_TRINITY_BUILT, RU_TOUR],
            "Mwitanzige",
        ),
        row(
            "ug-ru-nsinze-catherine",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of Saint Catherine the Great Martyr in Nsinze",
            "Приход святой великомученицы Екатерины в г. Нсинзе",
            [RU_CATHERINE, RU_ROSTER_RU],
            "Nsinze",
        ),
        row(
            "ug-ru-wamala-anthony-great",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of Saint Anthony the Great in Wamala",
            "Приход преподобного Антония Великого в с. Вамала",
            [RU_ANTHONY, RU_TOUR],
            "Wamala",
        ),
        row(
            "ug-ru-mbale-patrick-ireland",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of Saint Patrick, Enlightener of Ireland, in Mbale",
            "Приход святителя Патрикия, просветителя Ирландии, в г. Мбале",
            [RU_PATRICK, RU_ROSTER_RU],
            "Mbale",
        ),
        row(
            "ug-ru-mukongoro-apostle-peter",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of the Apostle Peter in Mukongoro",
            "Приход апостола Петра в с. Муконгоро",
            [RU_APOSTLE_PETER, RU_ROSTER_RU],
            "Mukongoro",
        ),
        row(
            "ug-ru-nakabale-transfiguration",
            "ug-ru-eastern-deanery",
            "parish",
            "Parish",
            "Parish of the Transfiguration of the Lord in Nakabale",
            "Преображенский приход в с. Накабале",
            [RU_TRANSFIGURATION, RU_ROSTER_RU],
            "Nakabale",
        ),
        row(
            "ug-ru-gulu-archangel-michael",
            "ug-ru-northern-deanery",
            "parish",
            "Parish",
            "Parish of the Archangel Michael and the Other Bodiless Powers in Gulu",
            "Приход Архистратига Божия Михаила и прочих сил бесплотных в с. Гулу",
            [RU_DEANERIES, RU_TOUR, RU_ROSTER_RU],
            "Gulu",
        ),
        row(
            "ug-ru-life-giving-spring",
            "ug-ru-northern-deanery",
            "parish",
            "Parish",
            "Parish of the Icon of the Mother of God Life-Giving Spring",
            "Приход иконы Божией Матери «Живоносный Источник»",
            [RU_LIFE_SPRING, RU_LIFE_SPRING_CURRENT, RU_TOUR],
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "ug-rocor-bukasa-annunciation",
            "ru-great-britain-and-western-europe-rocor",
            "parish",
            "Church",
            "Holy Annunciation Church on Bukasa Island",
            "Holy Annunciation Church on Bukasa Island",
            [ROCOR_ANNUNCIATION, RU_ANNUNCIATION],
            "Bukasa Island",
        ),
        row(
            "ug-rocor-bukasa-annunciation-construction",
            "ru-great-britain-and-western-europe-rocor",
            "parish",
            "Church Under Construction",
            "Annunciation of the Theotokos Church Under Construction on Bukasa Island",
            "Строящийся храм Благовещения Пресвятой Богородицы на острове Букаса",
            [ROCOR_ANNUNCIATION, RU_ANNUNCIATION],
            "Bukasa Island",
        ),
    ],
}

EXPECTED = {
    "alexandria": 1,
    "ax-kampala": 1,
    "ru-south-africa": 20,
    "ru-great-britain-and-western-europe-rocor": 2,
}
EXPECTED_TOTAL = 24
EXPECTED_RUSSIAN_NAMED_BODIES = 16
EXPECTED_RUSSIAN_DEANERIES = 3
EXPECTED_CONSTRUCTION_SITES = 3
ALLOWED_RANKS = {
    "Diocese", "Deanery", "Cathedral", "Parish", "Church",
    "Missionary Center", "Church Under Construction",
}
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}
ENGLISH_SEATS = {
    item["seat"]: item["seat"]
    for source_rows in ROWS.values()
    for item in source_rows
    if item.get("seat")
}


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


def validate_row(item, branch_parent, branch_seen):
    row_id = item.get("id")
    if not row_id or not re.fullmatch(r"[a-z0-9-]+", row_id):
        raise ValueError("invalid or missing id: %s" % row_id)
    if item.get("parent") not in branch_seen:
        raise ValueError("%s hangs off an unknown parent" % row_id)
    if item.get("country") != "UG":
        raise ValueError("%s is outside Uganda" % row_id)
    if item.get("kind") not in ("diocese", "parish"):
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if item.get("rank") in ("Diocese", "Deanery"):
        if item.get("kind") != "diocese":
            raise ValueError("%s has malformed administrative rank" % row_id)
    elif item.get("kind") != "parish":
        raise ValueError("%s uses diocese kind for a worship body" % row_id)
    if not item.get("name") or not item.get("local"):
        raise ValueError("%s lacks a usable name" % row_id)


def build():
    payloads = {}
    all_seen = set(ROWS)
    total = 0
    for branch_parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {branch_parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if row_id in all_seen:
                raise ValueError("duplicate id: %s" % row_id)
            validate_row(item, branch_parent, branch_seen)
            all_seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        if len(rows) != EXPECTED[branch_parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (branch_parent, EXPECTED[branch_parent]))
        total += len(rows)
        payloads[branch_parent] = {
            "v": 1,
            "parent": branch_parent,
            "country": "UG",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Uganda must publish exactly %d rows" % EXPECTED_TOTAL)
    russian_rows = ROWS["ru-south-africa"]
    roster_bodies = sum(
        item["kind"] == "parish" and
        item["rank"] != "Church Under Construction"
        for item in russian_rows
    ) + 1
    if roster_bodies != EXPECTED_RUSSIAN_NAMED_BODIES:
        raise ValueError("Uganda Russian named-body total is out of sync")
    if sum(item["rank"] == "Deanery" for item in russian_rows) != \
            EXPECTED_RUSSIAN_DEANERIES:
        raise ValueError("Uganda Russian deanery total is out of sync")
    if sum(
        item["rank"] == "Church Under Construction"
        for source_rows in ROWS.values()
        for item in source_rows
    ) != EXPECTED_CONSTRUCTION_SITES:
        raise ValueError("Uganda construction-site total is out of sync")
    if set(ENGLISH_NAMES) != all_seen - set(ROWS):
        raise ValueError("Uganda English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "UG":
        raise ValueError("Uganda candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Uganda candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("total") != EXPECTED_TOTAL:
        raise ValueError("Uganda candidate ledger total is out of sync")
    for parent, count in EXPECTED.items():
        if summary.get(parent) != count:
            raise ValueError("Uganda ledger count is out of sync for %s" %
                             parent)
    if summary.get("russian_named_parishes_and_missions") != \
            EXPECTED_RUSSIAN_NAMED_BODIES:
        raise ValueError("Uganda ledger Russian body total is out of sync")
    if summary.get("churches_under_construction") != \
            EXPECTED_CONSTRUCTION_SITES:
        raise ValueError("Uganda ledger construction total is out of sync")
    for key in ("candidates", "source_reconciliations",
                "official_jurisdiction_audit"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Uganda candidate ledger lacks %s" % key)
        for item in ledger[key]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Uganda ledger item has invalid sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Uganda ledger item has a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Uganda candidate ledger has forbidden punctuation")
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
        print("directory Uganda: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Uganda: 24 current named bodies across Alexandrian, "
            "Moscow Exarchate, and ROCOR structures"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
