#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Zambia.

The existing Alexandrian metropolitan parent remains in the directory spine.
Current competent Church sources establish three Alexandrian churches and a
Russian Church deanery with five individually named parishes. Two of the
Russian parish churches are under construction and are represented once with
that current status. Aggregate-only and uncertain identities remain in the
companion candidate ledger.

    python tools/directory_zambia.py --check
    python tools/directory_zambia.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "zambia.json"

AX_PARENT = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-zamvia/?lang=en"
)
AX_BASIL = (
    "https://www.patriarchateofalexandria.com/"
    "deyteri-imera-tis-patriarchikis-episkepseos-sti-zampia/"
)
AX_CHRYSOSTOM = (
    "https://www.patriarchateofalexandria.com/"
    "i-triti-imera-tis-patriarchikis-episkepseos-toy-patriarchoy-"
    "alexandreias-sti-zampia/"
)
AX_ALEXANDER = (
    "https://www.patriarchateofalexandria.com/"
    "tetarti-imera-tis-patriarchikis-poimantikis-periodeias-toy-"
    "patriarchi-alexandreias-k-k-theodoroy-v-sti-zampia/"
)

RU_ROSTER_RU = (
    "https://exarchate-africa.ru/dioceses_cat/"
    "yuzhno-afrikanskaya-eparhiya/"
)
RU_LUSAKA = (
    "https://exarchate-africa.ru/novosti/"
    "v-predprazdnstvo-bogoyavleniya-sovershena-liturgiya-v-hrame-"
    "arhangela-mihaila-v-stolicze-zambii/"
)
RU_LUSAKA_LATEST = (
    "https://exarchate-africa.ru/novosti/"
    "klirik-hrama-arhistratiga-mihaila-v-lusake-zambiya-prinyal-"
    "uchastie-v-yarmarke-kultur-v-russkom-dome/"
)
RU_LUSAKA_VISIT = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-pokrova-presvyatoj-bogorodiczy-mitropolit-konstantin-"
    "sovershil-liturgiyu-v-stolicze-zambii/"
)
RU_DEMETRIUS = (
    "https://exarchate-africa.ru/novosti/"
    "proshlo-soveshhanie-po-stroitelstvu-hrama-svyatitelya-dimitriya-"
    "rostovskogo-v-g-luanshya-zambiya/"
)
RU_DEMETRIUS_WORSHIP = (
    "https://exarchate-africa.ru/novosti/"
    "v-nedelyu-o-rasslablennom-sovershena-liturgiya-na-prihode-"
    "svyatitelya-dimitriya-rostovskogo-v-zambii/"
)
RU_PETER_PAUL = (
    "https://exarchate-africa.ru/novosti/"
    "blagochinnyj-prihodov-v-zambii-posetil-pravoslavnuyu-obshhinu-"
    "na-zapade-strany/"
)
RU_GEORGE = (
    "https://exarchate-africa.ru/novosti/"
    "v-zambii-kreshheny-14-mestnyh-zhitelej/"
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
        "country": "ZM",
        "sources": sources,
    }


AX_ROWS = [
    row(
        "zm-ax-lusaka-mission-saint-basil",
        "ax-zambia",
        "parish",
        "Church",
        "Saint Basil Church at the Lusaka Missionary Centre",
        "Ιερό Ναό Αγίου Βασιλείου του Ιεραποστολικού Κέντρου της Λουσάκα",
        [AX_BASIL, AX_PARENT],
        "Lusaka",
    ),
    row(
        "zm-ax-chirundu-chrysostom-papasarantopoulos",
        "ax-zambia",
        "parish",
        "Church",
        "Saint Chrysostomos Papasarantopoulos Church in Chirundu",
        "Ιερού Ναού του Αγίου Χρυσοστόμου Παπασαραντόπουλου",
        [AX_CHRYSOSTOM, AX_PARENT],
        "Chirundu",
    ),
    row(
        "zm-ax-makeni-saint-alexander",
        "ax-zambia",
        "parish",
        "Church",
        "Saint Alexander Community Church in Makeni, Lusaka",
        (
            "Ιερό Κοινοτικό Ναό του Αγίου Αλεξάνδρου της Ελληνικής "
            "Κοινότητας Λουσάκα και Επαρχιακών Περιοχών (Μακένι)"
        ),
        [AX_ALEXANDER, AX_PARENT],
        "Makeni, Lusaka",
    ),
]

RU_ROWS = [
    row(
        "zm-ru-zambia-deanery",
        "ru-south-africa",
        "diocese",
        "Deanery",
        "Deanery of the Republic of Zambia",
        "Благочиние Республики Замбия",
        [RU_ROSTER_RU, RU_LUSAKA_VISIT],
    ),
    row(
        "zm-ru-lusaka-archangel-michael",
        "zm-ru-zambia-deanery",
        "parish",
        "House Church",
        "Archangel Michael House Church in Lusaka",
        "Храм Архангела Михаила",
        [RU_ROSTER_RU, RU_LUSAKA, RU_LUSAKA_LATEST],
        "Lusaka",
    ),
    row(
        "zm-ru-chongwe-constantine-helena",
        "zm-ru-zambia-deanery",
        "parish",
        "Church Under Construction",
        (
            "Equal-to-the-Apostles Constantine and Helena Church Under "
            "Construction in Chongwe"
        ),
        "Приход равноапостольных Константина и Елены",
        [RU_ROSTER_RU, RU_LUSAKA_VISIT],
        "Chongwe",
    ),
    row(
        "zm-ru-luanshya-demetrius-rostov",
        "zm-ru-zambia-deanery",
        "parish",
        "Church Under Construction",
        "Saint Demetrius of Rostov Church Under Construction in Luanshya",
        "Приход святителя Димитрия Ростовского в г. Луаншья",
        [RU_DEMETRIUS, RU_DEMETRIUS_WORSHIP],
        "Luanshya",
    ),
    row(
        "zm-ru-mongu-peter-paul",
        "zm-ru-zambia-deanery",
        "parish",
        "Parish",
        "Parish of the Holy Apostles Peter and Paul in Mongu",
        "Приход святых равноапостольных апостолов Петра и Павла в г. Монгу",
        [RU_PETER_PAUL, RU_ROSTER_RU],
        "Mongu",
    ),
    row(
        "zm-ru-mwense-george",
        "zm-ru-zambia-deanery",
        "parish",
        "Parish",
        "Parish of the Great Martyr George the Victory-Bearer in Mwense",
        "Приход великомученика Георгия Победоносца в г. Мвензе",
        [RU_GEORGE, RU_ROSTER_RU],
        "Mwense",
    ),
]

ROWS = {
    "ax-zambia": AX_ROWS,
    "ru-south-africa": RU_ROWS,
}
EXPECTED = {
    "ax-zambia": 3,
    "ru-south-africa": 6,
}
EXPECTED_TOTAL = 9
EXPECTED_RUSSIAN_PARISHES = 5
EXPECTED_RUSSIAN_DEANERIES = 1
ALLOWED_RANKS = {
    "Church", "Parish", "House Church", "Church Under Construction",
    "Deanery",
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
    if item.get("country") != "ZM":
        raise ValueError("%s is outside Zambia" % row_id)
    if item.get("kind") not in ("diocese", "parish"):
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if item.get("rank") == "Deanery":
        if item.get("kind") != "diocese" or item.get("parent") != branch_parent:
            raise ValueError("%s has malformed deanery hierarchy" % row_id)
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
            "country": "ZM",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Zambia must publish exactly %d rows" % EXPECTED_TOTAL)
    if sum(item["kind"] == "parish" for item in RU_ROWS) != \
            EXPECTED_RUSSIAN_PARISHES:
        raise ValueError("Zambia Russian parish total is out of sync")
    if sum(item["rank"] == "Deanery" for item in RU_ROWS) != \
            EXPECTED_RUSSIAN_DEANERIES:
        raise ValueError("Zambia Russian deanery total is out of sync")
    if set(ENGLISH_NAMES) != all_seen - set(ROWS):
        raise ValueError("Zambia English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "ZM":
        raise ValueError("Zambia candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Zambia candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    expected_summary = {
        "existing_ax-zambia_parent": 1,
        "ax-zambia": 3,
        "ru-south-africa": 6,
        "russian_named_deaneries": 1,
        "russian_named_parishes": 5,
        "russian_roster_total_parishes": 7,
        "russian_aggregate_only_remainder": 2,
        "new_subordinate_bodies": 9,
    }
    if summary != expected_summary:
        raise ValueError("Zambia candidate ledger totals are out of sync")
    required_lists = (
        "candidates", "dedupe_notes", "official_jurisdiction_audit",
        "exclusions",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Zambia candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "ZM":
            raise ValueError("%s is outside Zambia" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Zambia candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Zambia ledger item must cite one to three sources"
                )
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Zambia ledger carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Zambia candidate ledger has forbidden punctuation")
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
        print("directory Zambia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Zambia: 9 current bodies, including 3 Alexandrian churches "
            "and 1 Russian deanery with 5 named parishes, plus the existing "
            "Alexandrian metropolitan parent"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
