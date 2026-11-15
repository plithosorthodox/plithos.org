#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Congo-Kinshasa.

Five current Alexandrian diocesan parents already remain in the directory
spine. Current first-party Church sources establish nine named Alexandrian
churches or parishes and two Moscow Patriarchate deaneries with ten named
parishes. The live Moscow diocesan roster reports nineteen parishes in all,
so aggregate-only, older, uncertain, and affiliation-unclear identities remain
in the companion candidate ledger.

    python tools/directory_congo_dr.py --check
    python tools/directory_congo_dr.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "congo_dr.json"
)

AX_KINSHASA_NICHOLAS = (
    "https://www.patriarchateofalexandria.com/"
    "o-patriarchis-alexandreias-epsalle-toys-chairetismoys-stin-kinsasa/"
)
AX_KINSHASA_MARK = (
    "https://www.patriarchateofalexandria.com/"
    "thyranoixia-toy-anakainisthentos-ieroy-naoy-toy-agioy-markoy-"
    "kinsasas/"
)
AX_KINSHASA_PARISHES = (
    "https://www.patriarchateofalexandria.com/"
    "egkainia-nipiagogeioy-stin-kinsasa/"
)
AX_KANANGA_ANDREW = (
    "https://www.patriarchateofalexandria.com/"
    "chara-megali-gia-tin-orthodoxi-ierapostoli/"
)
AX_KISANGANI_CHURCHES = (
    "https://iekisangani.com/"
    "%ce%b9%ce%b5%cf%81%ce%bf%ce%af-%ce%bd%ce%b1%ce%bf%ce%af/"
)
AX_KISANGANI_PARENT = (
    "https://www.patriarchateofalexandria.com/"
    "iera-episkopi-kisangkani/"
)

RU_ROSTER = (
    "https://exarchate-africa.ru/dioceses_cat/"
    "yuzhno-afrikanskaya-eparhiya/"
)
RU_ROSTER_EN = (
    "https://exarchate-africa.ru/en/dioceses_cat/"
    "south-african-diocese/"
)
RU_RAPHAEL = (
    "https://exarchate-africa.ru/novosti/"
    "provedeny-otdelochnye-raboty-vo-vremennom-hrame-arhangela-rafaila-"
    "v-stolicze-dr-kongo/"
)
RU_EASTER = (
    "https://exarchate-africa.ru/fotoalbomy/"
    "veruyushhie-v-demokraticheskoj-respublike-kongo-vstretili-svetloe-"
    "hristovo-voskresenie/"
)
RU_MOSES = (
    "https://exarchate-africa.ru/novosti/"
    "v-velikuyu-subbotu-na-prihode-prepodobnogo-moiseya-murina-v-dr-"
    "kongo-krestilis-11-chelovek/"
)
RU_TENKE_CONSTRUCTION = (
    "https://exarchate-africa.ru/novosti/"
    "sostoyalos-osvyashhenie-zakladnogo-kamnya-v-osnovanie-hrama-"
    "svyatitelya-nikolaya-chudotvorcza-na-yuge-dr-kongo/"
)
RU_HUMANITARIAN = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihodah-russkoj-pravoslavnoj-czerkvi-v-demokraticheskoj-"
    "respublike-kongo-prohodit-gumanitarnaya-akcziya/"
)
RU_SOUTHERN_VISIT = (
    "https://exarchate-africa.ru/novosti/"
    "blagochinnyj-prihodov-v-dr-kongo-sovershaet-poezdku-po-obshhinam-"
    "na-yuge-strany/"
)
RU_GEORGE_CONSTRUCTION = (
    "https://exarchate-africa.ru/novosti/"
    "osvyashhen-zakladnoj-kamen-v-osnovanie-budushhego-hrama-v-chest-"
    "velikomuchenika-georgiya-v-dr-kongo/"
)
RU_PANTELEIMON = (
    "https://exarchate-africa.ru/novosti/"
    "prestolnyj-prazdnik-otmetili-na-prihode-velikomuchenika-"
    "panteleimona-v-dr-kongo-2/"
)
RU_VLADIMIR = (
    "https://exarchate-africa.ru/novosti/"
    "okazana-prodovolstvennaya-pomoshh-pravoslavnym-veruyushhim-v-"
    "kolvezi-dr-kongo/"
)
RU_CATHERINE = (
    "https://exarchate-africa.ru/novosti/"
    "svyashhennik-v-dr-kongo-sovershil-missionerskuyu-poezdku-v-"
    "provincziyu-verhnyaya-katanga-na-yuge-strany/"
)


def row(row_id, parent, kind, rank, name, local, sources, seat=None,
        emails=None, phones=None, contact_sources=None):
    has_contacts = bool(emails or phones)
    return {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "CD",
        "sources": sources,
        "emails": emails,
        "phones": phones,
        "contact_sources": contact_sources if has_contacts else None,
        "contact_checked": CHECKED if has_contacts else None,
    }


AX_KINSHASA_ROWS = [
    row(
        "cd-ax-kinshasa-nicholas",
        "ax-kinshasa",
        "parish",
        "Metropolitan Church",
        "Saint Nicholas Metropolitan Church of the Hellenic Community of Kinshasa",
        (
            "Ιερός Μητροπολιτικός Ναός του Αγίου Νικολάου της "
            "Ελληνικής Κοινότητας Κινσάσας"
        ),
        [AX_KINSHASA_NICHOLAS],
        "Kinshasa",
    ),
    row(
        "cd-ax-kinshasa-mark",
        "ax-kinshasa",
        "parish",
        "Church",
        "Saint Mark Church in Kinshasa",
        "Ιερός Ναός Αγίου Μάρκου Κινσάσας",
        [AX_KINSHASA_MARK],
        "Kinshasa",
    ),
    row(
        "cd-ax-kinshasa-archangels",
        "ax-kinshasa",
        "parish",
        "Parish",
        "Holy Archangels Parish in Kinshasa",
        "Ενορία των Αρχαγγέλων στην Κινσάσα",
        [AX_KINSHASA_PARISHES],
        "Kinshasa",
    ),
    row(
        "cd-ax-kinshasa-axion-esti",
        "ax-kinshasa",
        "parish",
        "Parish",
        "Panagia Axion Esti Parish in Kinshasa",
        'Ενορία της Παναγίας "Άξιον Εστί"',
        [AX_KINSHASA_PARISHES],
        "Kinshasa",
    ),
]

AX_KANANGA_ROWS = [
    row(
        "cd-ax-kananga-andrew",
        "ax-kananga",
        "parish",
        "Church",
        "Saint Andrew Church in Kananga",
        "Ιερός Ναός του Αγίου Ανδρέου",
        [AX_KANANGA_ANDREW],
        "Kananga",
    ),
]

AX_KISANGANI_ROWS = [
    row(
        "cd-ax-kisangani-annunciation",
        "ax-kisangani",
        "parish",
        "Church",
        "Annunciation of the Theotokos Church in Kisangani",
        "Ιερός Ναός Ευαγγελισμού της Θεοτόκου",
        [AX_KISANGANI_CHURCHES, AX_KISANGANI_PARENT],
        "Kisangani",
    ),
    row(
        "cd-ax-bunia-nicholas",
        "ax-kisangani",
        "parish",
        "Church",
        "Saint Nicholas Church in Bunia",
        "Ιερός Ναός Αγίου Νικολάου",
        [AX_KISANGANI_CHURCHES, AX_KISANGANI_PARENT],
        "Bunia",
    ),
    row(
        "cd-ax-isiro-demetrius",
        "ax-kisangani",
        "parish",
        "Church",
        "Saint Demetrius Church in Isiro",
        "Ιερός Ναός Αγίου Δημητρίου",
        [AX_KISANGANI_CHURCHES, AX_KISANGANI_PARENT],
        "Isiro",
    ),
    row(
        "cd-ax-lake-albert-athanasius-lazarus",
        "ax-kisangani",
        "parish",
        "Church",
        "Saints Athanasius and Lazarus Church at Lake Albert",
        "Ιερός Ναός Αγίου Αθανασίου & Αγίου Λαζάρου",
        [AX_KISANGANI_CHURCHES, AX_KISANGANI_PARENT],
        "Lake Albert",
    ),
]

RU_ROWS = [
    row(
        "cd-ru-kinshasa-deanery",
        "ru-south-africa",
        "diocese",
        "Deanery",
        "Deanery of Kinshasa in the Democratic Republic of the Congo",
        "Благочиние Киншасы Демократической Республики Конго",
        [RU_ROSTER],
        emails=["nicolasmusoya@gmail.com"],
        contact_sources=[RU_ROSTER_EN, RU_ROSTER],
    ),
    row(
        "cd-ru-southern-deanery",
        "ru-south-africa",
        "diocese",
        "Deanery",
        "Southern Deanery of the Democratic Republic of the Congo",
        "Южное благочиние Демократической Республики Конго",
        [RU_ROSTER],
        emails=["nicolasmusoya@gmail.com"],
        contact_sources=[RU_ROSTER_EN, RU_ROSTER],
    ),
    row(
        "cd-ru-kinshasa-raphael",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of the Archangel Raphael in Kinshasa",
        "Приход Архангела Рафаила в г. Киншаса",
        [RU_RAPHAEL, RU_ROSTER],
        "Kinshasa",
    ),
    row(
        "cd-ru-kinshasa-andrew",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of the Apostle Andrew in Kinshasa",
        "Приход апостола Андрея в Киншасе",
        [RU_EASTER, RU_ROSTER],
        "Kinshasa",
    ),
    row(
        "cd-ru-kikwit-moses-black",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of Saint Moses the Black in Kikwit",
        "Приход преподобного Моисея Мурина в с. Киквите",
        [RU_MOSES, RU_ROSTER],
        "Kikwit, Kwilu Province",
    ),
    row(
        "cd-ru-tenke-nicholas",
        "ru-south-africa",
        "parish",
        "Church Under Construction",
        "Saint Nicholas the Wonderworker Church Under Construction in Tenke",
        "Приход святителя Николая Чудотворца в с. Тенке",
        [RU_ROSTER, RU_TENKE_CONSTRUCTION, RU_HUMANITARIAN],
        "Tenke, Lualaba Province",
        emails=["nicolasmusoya@gmail.com"],
        contact_sources=[RU_ROSTER_EN, RU_ROSTER],
    ),
    row(
        "cd-ru-luena-nicholas",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of Saint Nicholas the Wonderworker in Luena",
        "Приход святителя Николая Чудотворца в с. Луена",
        [RU_SOUTHERN_VISIT, RU_ROSTER],
        "Luena, Haut-Lomami Province",
    ),
    row(
        "cd-ru-katala-george",
        "ru-south-africa",
        "parish",
        "Church Under Construction",
        "Great Martyr George the Victory-Bearer Church Under Construction in Katala",
        "Приход великомученика Георгия Победоносца в с. Катала",
        [RU_SOUTHERN_VISIT, RU_GEORGE_CONSTRUCTION],
        "Katala, Haut-Lomami Province",
    ),
    row(
        "cd-ru-fungurume-panteleimon",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of the Great Martyr Panteleimon in Fungurume",
        "Приход великомученика Пантелеимона в г. Фунгуреме",
        [RU_PANTELEIMON, RU_ROSTER],
        "Fungurume, Lualaba Province",
    ),
    row(
        "cd-ru-kolwezi-vladimir",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of Equal-to-the-Apostles Prince Vladimir in Kolwezi",
        "Приход равноапостольного князя Владимира в г. Колвези",
        [RU_VLADIMIR, RU_ROSTER],
        "Kolwezi, Lualaba Province",
    ),
    row(
        "cd-ru-kazumba-catherine",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of the Great Martyr Catherine in Kazumba",
        "Приход великомученицы Екатерины в с. Казумба",
        [RU_CATHERINE, RU_ROSTER],
        "Kazumba, Haut-Katanga Province",
    ),
    row(
        "cd-ru-uvira-peter-paul",
        "ru-south-africa",
        "parish",
        "Parish",
        "Parish of the Holy Chief Apostles Peter and Paul in Uvira",
        "Приход первоверховных апостолов Петра и Павла в с. Увира",
        [RU_HUMANITARIAN, RU_EASTER, RU_ROSTER],
        "Uvira, South Kivu Province",
    ),
]

ROWS = {
    "ax-kinshasa": AX_KINSHASA_ROWS,
    "ax-kananga": AX_KANANGA_ROWS,
    "ax-katanga": [],
    "ax-goma": [],
    "ax-kisangani": AX_KISANGANI_ROWS,
    "ru-south-africa": RU_ROWS,
}
EXPECTED = {
    "ax-kinshasa": 4,
    "ax-kananga": 1,
    "ax-katanga": 0,
    "ax-goma": 0,
    "ax-kisangani": 4,
    "ru-south-africa": 12,
}
EXPECTED_TOTAL = 21
EXPECTED_RUSSIAN_PARISHES = 10
EXPECTED_RUSSIAN_DEANERIES = 2
EXPECTED_DIRECT_CONTACT_ROWS = 3
EXPECTED_EMAIL_INSTANCES = 3
EXPECTED_PHONE_INSTANCES = 0
ALLOWED_RANKS = {
    "Church", "Parish", "Metropolitan Church",
    "Church Under Construction", "Deanery",
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
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         item.get("id"))
    return item


def validate_row(item, branch_parent):
    row_id = item.get("id")
    if not row_id or not re.fullmatch(r"[a-z0-9-]+", row_id):
        raise ValueError("invalid or missing id: %s" % row_id)
    if item.get("parent") != branch_parent:
        raise ValueError("%s hangs off the wrong parent" % row_id)
    if item.get("country") != "CD":
        raise ValueError("%s is outside Congo-Kinshasa" % row_id)
    if item.get("kind") not in ("diocese", "parish"):
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if item.get("rank") == "Deanery":
        if item.get("kind") != "diocese":
            raise ValueError("%s has malformed deanery hierarchy" % row_id)
    elif item.get("kind") != "parish":
        raise ValueError("%s uses diocese kind for a worship body" % row_id)
    if not item.get("name") or not item.get("local"):
        raise ValueError("%s lacks a usable name" % row_id)
    emails = item.get("emails") or []
    phones = item.get("phones") or []
    has_contacts = bool(emails or phones)
    contact_sources = item.get("contact_sources") or []
    if has_contacts:
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s has a stale contact check date" % row_id)
        if not contact_sources or len(contact_sources) > 3:
            raise ValueError("%s has invalid contact sources" % row_id)
        if not all(str(url).startswith("https://")
                   for url in contact_sources):
            raise ValueError("%s has a non-HTTPS contact source" % row_id)
        if any(not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
               for email in emails):
            raise ValueError("%s has an invalid email" % row_id)
        if any(not isinstance(phone, str) or not phone.strip()
               for phone in phones):
            raise ValueError("%s has an invalid phone" % row_id)
    elif contact_sources or item.get("contact_checked"):
        raise ValueError("%s has contact metadata without a contact" % row_id)


def build():
    payloads = {}
    seen = set(ROWS)
    total = 0
    for branch_parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if row_id in seen:
                raise ValueError("duplicate id: %s" % row_id)
            validate_row(item, branch_parent)
            seen.add(row_id)
            rows.append(item)
        if len(rows) != EXPECTED[branch_parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (branch_parent, EXPECTED[branch_parent]))
        total += len(rows)
        payloads[branch_parent] = {
            "v": 1,
            "parent": branch_parent,
            "country": "CD",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Congo-Kinshasa must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if sum(item["kind"] == "parish" for item in RU_ROWS) != \
            EXPECTED_RUSSIAN_PARISHES:
        raise ValueError("Congo-Kinshasa Russian parish total is out of sync")
    if sum(item["rank"] == "Deanery" for item in RU_ROWS) != \
            EXPECTED_RUSSIAN_DEANERIES:
        raise ValueError("Congo-Kinshasa Russian deanery total is out of sync")
    all_rows = [item for payload in payloads.values()
                for item in payload["rows"]]
    if sum(bool(item.get("emails") or item.get("phones"))
           for item in all_rows) != EXPECTED_DIRECT_CONTACT_ROWS:
        raise ValueError("Congo-Kinshasa contact row total is out of sync")
    if sum(len(item.get("emails") or []) for item in all_rows) != \
            EXPECTED_EMAIL_INSTANCES:
        raise ValueError("Congo-Kinshasa email total is out of sync")
    if sum(len(item.get("phones") or []) for item in all_rows) != \
            EXPECTED_PHONE_INSTANCES:
        raise ValueError("Congo-Kinshasa phone total is out of sync")
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Congo-Kinshasa English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "CD":
        raise ValueError("Congo-Kinshasa candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Congo-Kinshasa ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    expected_summary = {
        "existing_alexandrian_parents": 5,
        "ax-kinshasa": 4,
        "ax-kananga": 1,
        "ax-katanga": 0,
        "ax-goma": 0,
        "ax-kisangani": 4,
        "ru-south-africa": 12,
        "russian_named_deaneries": 2,
        "russian_named_parishes": 10,
        "russian_roster_total_parishes": 19,
        "russian_aggregate_only_remainder": 9,
        "new_subordinate_bodies": 21,
    }
    if summary != expected_summary:
        raise ValueError("Congo-Kinshasa ledger totals are out of sync")
    required_lists = (
        "candidates", "dedupe_notes", "official_jurisdiction_audit",
        "exclusions",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Congo-Kinshasa ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "CD":
            raise ValueError("%s is outside Congo-Kinshasa" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Congo-Kinshasa ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Congo-Kinshasa ledger item must cite one to three sources"
                )
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Congo-Kinshasa ledger has a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Congo-Kinshasa ledger has forbidden punctuation")
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
        print("directory Congo-Kinshasa: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Congo-Kinshasa: 21 current subordinate bodies, including 9 "
            "Alexandrian bodies and 2 Russian deaneries with 10 named "
            "parishes, plus 5 existing Alexandrian parents"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
