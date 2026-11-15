#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Malawi.

The existing Alexandrian diocesan parent remains in the directory spine.
Current official Moscow Patriarchate records name two Malawi deaneries and
fifteen parishes. The live diocesan roster reports thirty-four parishes in
total, so unnamed, older, conflicting, and aggregate-only identities remain
in the companion candidate ledger.

    python tools/directory_malawi.py --check
    python tools/directory_malawi.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "malawi.json"

RU_ROSTER = (
    "https://exarchate-africa.ru/en/dioceses_cat/"
    "south-african-diocese/"
)
RU_DEANERIES = (
    "https://exarchate-africa.ru/novosti/"
    "mitropolit-konstantin-provel-onlajn-soveshhanie-s-novonaznachennymi-"
    "blagochinnymi-severnogo-i-yuzhnogo-czerkovnyh-okrugov-malavi/"
)
RU_GEORGE = (
    "https://exarchate-africa.ru/novosti/"
    "eshhe-chetyre-desyatka-chelovek-prinyali-tainstvo-kreshheniya-v-"
    "okruge-zomba-malavi/"
)
RU_ANDREW = (
    "https://exarchate-africa.ru/novosti/"
    "dvadczat-predstavitelej-naroda-mangandzha-v-malavi-prinyali-"
    "tainstvo-kreshheniya/"
)
RU_THEOPHAN = (
    "https://exarchate-africa.ru/novosti/"
    "v-g-nazombe-v-malavi-proshla-konferencziya-dlya-pravoslavnyh-"
    "zhenshhin/"
)
RU_MATRONA = (
    "https://exarchate-africa.ru/novosti/"
    "v-okruge-zomba-malavi-krestilis-16-predstavitelej-narodov-yao-i-"
    "mangandzha/"
)
RU_PETER_PAUL_CHIMWAWA = (
    "https://exarchate-africa.ru/novosti/"
    "prihod-apostolov-petra-i-pavla-v-okruge-chiradzulu-malavi-otmetil-"
    "prestolnyj-prazdnik/"
)
RU_LUKE_CRIMEA = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihode-svyatitelya-luki-krymskogo-v-malavi-desyat-chelovek-"
    "prinyali-tainstvo-kreshheniya/"
)
RU_NICHOLAS = (
    "https://exarchate-africa.ru/novosti/"
    "na-nikolskom-prihode-v-malavi-sostoyalsya-seminar-dlya-aktivnyh-"
    "prihozhan/"
)
RU_NICHOLAS_PLACE = (
    "https://exarchate-africa.ru/novosti/"
    "prazdnik-vozdvizheniya-kresta-gospodnya-otmetili-na-nikolskom-"
    "prihode-v-malavi/"
)
RU_CYRIL = (
    "https://exarchate-africa.ru/en/news/"
    "another-112-representatives-of-the-lomwe-and-manganja-peoples-"
    "baptized-in-southern-malawi/"
)
RU_CYRIL_RU = (
    "https://exarchate-africa.ru/novosti/"
    "eshhe-112-predstavitelej-narodov-lomve-i-mangandzha-kreshheny-na-"
    "yuge-malavi/"
)
RU_VLADIMIR = (
    "https://exarchate-africa.ru/novosti/"
    "v-nedelyu-o-bludnom-syne-patriarshij-ekzarh-afriki-sovershil-"
    "liturgiyu-na-knyaz-vladimirskom-prihode-v-malavi/"
)
RU_MARY = (
    "https://exarchate-africa.ru/en/news/"
    "the-visit-of-the-patriarchal-exarch-of-africa-metropolitan-"
    "konstantin-to-malawi-has-begun/"
)
RU_ANTHONY = (
    "https://exarchate-africa.ru/novosti/"
    "mitropolit-konstantin-peredal-gumanitarnuyu-pomoshh-"
    "nuzhdayushhimsya-na-prihode-prepodobnogo-antoniya-velikogo-v-"
    "malavi/"
)
RU_PETER_MACARIUS = (
    "https://exarchate-africa.ru/novosti/"
    "patriarshij-ekzarh-afriki-posetil-s-gumanitarnoj-missiej-prihody-"
    "apostolov-petra-i-pavla-i-prepodobnogo-makariya-velikogo-v-malavi/"
)


def parish(row_id, name, local, sources, seat=None):
    return {
        "id": row_id,
        "parent": "ru-south-africa",
        "kind": "parish",
        "rank": "Parish",
        "name": name,
        "local": local,
        "seat": seat,
        "country": "MW",
        "sources": sources,
    }


def deanery(row_id, name, local):
    return {
        "id": row_id,
        "parent": "ru-south-africa",
        "kind": "diocese",
        "rank": "Deanery",
        "name": name,
        "local": local,
        "country": "MW",
        "sources": [RU_DEANERIES],
    }


ROWS = [
    deanery(
        "mw-ru-northern-deanery",
        "Northern Deanery of Malawi",
        "Северное благочиние",
    ),
    deanery(
        "mw-ru-southern-deanery",
        "Southern Deanery of Malawi",
        "Южное благочиние",
    ),
    parish(
        "mw-ru-zomba-george-victory-bearer",
        "Parish of the Great Martyr George the Victory-Bearer in Zomba District",
        "Приход великомученика Георгия Победоносца в округе Зомба",
        [RU_GEORGE, RU_DEANERIES],
    ),
    parish(
        "mw-ru-ndawawa-apostle-andrew",
        "Parish of the Apostle Andrew in Ndawawa",
        "Приход апостола Андрея в с. Ндавава",
        [RU_ANDREW, RU_DEANERIES],
        "Ndawawa",
    ),
    parish(
        "mw-ru-nazombe-theophan-recluse",
        "Parish of Saint Theophan the Recluse in Nazombe",
        "Приход святителя Феофана Затворника в г. Назомбе",
        [RU_THEOPHAN, RU_DEANERIES],
        "Nazombe",
    ),
    parish(
        "mw-ru-nanhunda-matrona-moscow",
        "Parish of Blessed Matrona of Moscow in Nanhunda",
        "Приход блаженной Матроны Московской в с. Нанхунда",
        [RU_MATRONA, RU_DEANERIES],
        "Nanhunda",
    ),
    parish(
        "mw-ru-chimwawa-peter-paul",
        "Parish of the Holy Apostles Peter and Paul in Chimwawa",
        "Приход святых апостолов Петра и Павла в с. Чимвава",
        [RU_PETER_PAUL_CHIMWAWA, RU_DEANERIES],
        "Chimwawa",
    ),
    parish(
        "mw-ru-chombe-luke-crimea",
        "Parish of Saint Luke of Crimea in Chombe",
        "Приход святителя Луки Крымского в с. Чомбе",
        [RU_LUKE_CRIMEA, RU_DEANERIES],
        "Chombe",
    ),
    parish(
        "mw-ru-chikovi-nicholas",
        "Parish of Saint Nicholas the Wonderworker in Chikovi",
        "Приход святителя Николая Чудотворца в с. Чикови",
        [RU_NICHOLAS, RU_NICHOLAS_PLACE, RU_DEANERIES],
        "Chikovi",
    ),
    parish(
        "mw-ru-nambazo-cyril",
        "Parish of Saint Cyril Equal-to-the-Apostles in Nambazo",
        "Приход равноапостольного Кирилла в с. Намбазо",
        [RU_CYRIL, RU_CYRIL_RU, RU_DEANERIES],
        "Nambazo",
    ),
    parish(
        "mw-ru-mtokodo-vladimir",
        "Parish of Great Prince Vladimir Equal-to-the-Apostles in Mtokodo",
        "Приход равноапостольного великого князя Владимира в с. Мтокодо",
        [RU_VLADIMIR, RU_DEANERIES],
        "Mtokodo",
    ),
    parish(
        "mw-ru-lumbadzi-mary-egypt",
        "Parish of Saint Mary of Egypt in Lumbadzi",
        "Приход преподобной Марии Египетской в с. Лумбадзи",
        [RU_MARY, RU_DEANERIES],
        "Lumbadzi",
    ),
    parish(
        "mw-ru-dyeratu-anthony-great",
        "Parish of Saint Anthony the Great in Dyeratu",
        "Приход преподобного Антония Великого в с. Дьерату",
        [RU_ANTHONY, RU_DEANERIES],
        "Dyeratu",
    ),
    parish(
        "mw-ru-makande-peter-paul",
        "Parish of the Holy Apostles Peter and Paul in Makande",
        "Приход первоверховных апостолов Петра и Павла в с. Маканде",
        [RU_PETER_MACARIUS, RU_DEANERIES],
        "Makande",
    ),
    parish(
        "mw-ru-likulezi-macarius-great",
        "Parish of Saint Macarius the Great in Likulezi",
        "Приход преподобного Макария Великого в с. Ликулези",
        [RU_PETER_MACARIUS, RU_DEANERIES],
        "Likulezi",
    ),
    parish(
        "mw-ru-migovi-john-climacus",
        "Parish of Saint John Climacus in Migovi",
        "Приход преподобного Иоанна Лествичника в с. Мигови",
        [RU_PETER_MACARIUS, RU_DEANERIES],
        "Migovi",
    ),
    parish(
        "mw-ru-namasoko-basil-great",
        "Parish of Saint Basil the Great in Namasoko",
        "Приход преподобного Василия Великого в с. Намасоко",
        [RU_PETER_MACARIUS, RU_DEANERIES],
        "Namasoko",
    ),
]

EXPECTED = 17
EXPECTED_PARISHES = 15
EXPECTED_DEANERIES = 2
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {
    item["seat"]: item["seat"] for item in ROWS if item.get("seat")
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


def build():
    rows = []
    seen = {"ru-south-africa"}
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if item.get("parent") != "ru-south-africa":
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if item.get("country") != "MW":
            raise ValueError("%s is outside Malawi" % row_id)
        if item.get("kind") not in ("diocese", "parish"):
            raise ValueError("%s has an unsupported kind" % row_id)
        if ((item.get("kind") == "diocese" and
             item.get("rank") != "Deanery") or
                (item.get("kind") == "parish" and
                 item.get("rank") != "Parish")):
            raise ValueError("%s has an inconsistent kind and rank" % row_id)
        if not item.get("name") or not item.get("local"):
            raise ValueError("%s lacks a usable name" % row_id)
        seen.add(row_id)
        rows.append(item)
    if len(rows) != EXPECTED:
        raise ValueError("Malawi must publish exactly %d rows" % EXPECTED)
    if sum(item["kind"] == "parish" for item in rows) != EXPECTED_PARISHES:
        raise ValueError("Malawi parish total is out of sync")
    if sum(item["rank"] == "Deanery" for item in rows) != EXPECTED_DEANERIES:
        raise ValueError("Malawi deanery total is out of sync")
    if set(ENGLISH_NAMES) != seen - {"ru-south-africa"}:
        raise ValueError("Malawi English name map is out of sync")
    return {
        "ru-south-africa": {
            "v": 1,
            "parent": "ru-south-africa",
            "country": "MW",
            "rows": rows,
        },
    }


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "MW":
        raise ValueError("Malawi candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Malawi candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if (summary.get("ru-south-africa") != EXPECTED or
            summary.get("russian_named_parishes") != EXPECTED_PARISHES or
            summary.get("russian_named_deaneries") != EXPECTED_DEANERIES or
            summary.get("russian_roster_total") != 34 or
            summary.get("russian_aggregate_only_remainder") != 19):
        raise ValueError("Malawi candidate ledger totals are out of sync")
    required_lists = ("candidates", "official_jurisdiction_audit", "exclusions")
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Malawi candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "MW":
            raise ValueError("%s is outside Malawi" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Malawi candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Malawi ledger item must cite one to three sources"
                )
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError(
                    "Malawi ledger item carries a non-HTTPS source"
                )
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Malawi candidate ledger has forbidden punctuation")
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
        print("directory Malawi: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Malawi: 17 current Russian Church bodies, including 2 "
            "deaneries and 15 named parishes, "
            "plus the existing Alexandrian diocesan parent"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
