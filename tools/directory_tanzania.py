#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Tanzania.

Three existing Alexandrian diocesan parents remain in the directory spine.
Current official sources establish four Alexandrian subordinate bodies and
two Russian Church deaneries with seventeen individually reconciled parishes
or church projects. The live Russian roster reports thirty-one parishes, so
the fourteen aggregate-only positions remain in the candidate ledger.

    python tools/directory_tanzania.py --check
    python tools/directory_tanzania.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools/directory_candidates/tanzania.json"
AX = "https://www.patriarchateofalexandria.com/"
RU = "https://exarchate-africa.ru/"


def ax(path):
    return AX + path


def ru(path):
    return RU + path


AX_IRINOPOLIS = ax(
    "archdioceses/holy-archdiocese-of-irinopolis/?lang=en")
AX_PARASKEVI = ax(
    "i-kardia-tis-tanzanias-ypodechthike-ton-patriarchi-alexandreias/")
AX_ARUSHA = ax(
    "archdioceses/holy-diocese-of-arusha-and-central-tanzania/?lang=en")
AX_ANNUNCIATION = ax(
    "i-orthodoxia-stin-tanzania-ayxanei-kai-karpoforei/")
AX_ANNUNCIATION_CATHEDRAL = ax(
    "afixi-toy-alexandrinoy-prokathimenoy-stin-tanzania/")
AX_BUKOBA = ax(
    "archdioceses/holy-diocese-of-bukoba-and-west-tanzania/?lang=en")
AX_BUKOBA_VISIT = ax("anastaseos-imera-stin-episkopi-mpoykompas/")
RU_ROSTER_EN = ru("en/dioceses_cat/south-african-diocese/")
RU_ROSTER_RU = ru("dioceses_cat/yuzhno-afrikanskaya-eparhiya/")
RU_VISIT = ru(
    "novosti/zavershilas-poezdka-patriarshego-ekzarha-afriki-"
    "mitropolita-konstantina-v-tanzaniyu/")


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
        "country": "TZ",
        "sources": sources,
        "emails": emails,
        "phones": phones,
        "contact_sources": contact_sources if has_contacts else None,
        "contact_checked": CHECKED if has_contacts else None,
    }


ROWS = {
    "ax-irinopolis": [
        row(
            "tz-ax-dar-es-salaam-paraskevi-cathedral",
            "ax-irinopolis", "parish", "Metropolitan Cathedral",
            "Saint Paraskevi Metropolitan Cathedral in Dar es Salaam",
            "Ιερός Μητροπολιτικός Ναός Αγίας Παρασκευής Ντάρ Ες Σαλάμ",
            [AX_PARASKEVI, AX_IRINOPOLIS], "Dar es Salaam"),
    ],
    "ax-arusha": [
        row(
            "tz-ax-arusha-annunciation-cathedral",
            "ax-arusha", "parish", "Cathedral",
            "Annunciation of the Theotokos Cathedral in Arusha",
            "Καθεδρικός Ιερός Ναός Ευαγγελισμού της Θεοτόκου Αρούσας",
            [AX_ANNUNCIATION_CATHEDRAL, AX_ANNUNCIATION, AX_ARUSHA],
            "Arusha"),
    ],
    "ax-bukoba": [
        row(
            "tz-ax-bukoba-holy-apostles-cathedral",
            "ax-bukoba", "parish", "Metropolitan Cathedral",
            "Holy Apostles Metropolitan Cathedral in Bukoba",
            "Μητροπολιτικός Ναός Αγίων Αποστόλων Μπουκόμπας",
            [AX_BUKOBA, AX_BUKOBA_VISIT], "Bukoba"),
        row(
            "tz-ax-kibuye-macrina-monastery",
            "ax-bukoba", "monastery", "Monastery",
            "Monastery of Saint Macrina in Kibuye",
            "Ιερά Μονή Αγίας Μακρίνας Κιμπούγιε",
            [AX_BUKOBA_VISIT, AX_BUKOBA], "Kibuye"),
    ],
    "ru-south-africa": [
        row(
            "tz-ru-central-deanery", "ru-south-africa", "diocese",
            "Deanery", "Central Deanery of the United Republic of Tanzania",
            "Центральное благочиние Объединенной Республики Танзания",
            [RU_ROSTER_RU, RU_ROSTER_EN, ru(
                "novosti/naznachen-novyj-blagochinnyj-czentralnogo-"
                "okruga-v-tanzanii/")],
            emails=["filaretoskimaro@gmail.com"],
            contact_sources=[RU_ROSTER_EN, RU_ROSTER_RU]),
        row(
            "tz-ru-northern-deanery", "ru-south-africa", "diocese",
            "Deanery", "Northern Deanery of the United Republic of Tanzania",
            "Северное благочиние Объединенной Республики Танзания",
            [RU_ROSTER_RU, RU_ROSTER_EN, ru(
                "novosti/mitropolit-konstantin-vozglavil-sobranie-"
                "duhovenstva-severnogo-blagochiniya-tanzanii-3/")],
            emails=["petermajuni@gmail.com"],
            contact_sources=[RU_ROSTER_EN, RU_ROSTER_RU]),
        row(
            "tz-ru-dar-es-salaam-matrona", "tz-ru-central-deanery",
            "parish", "Parish",
            "Parish of Blessed Matrona of Moscow in Dar es Salaam",
            "Приход блаженной Матроны Московской в г. Дар-эс-Салам",
            [ru("novosti/v-nedelyu-o-bludnom-syne-glava-patriarshego-"
                "ekzarhata-afriki-sovershil-liturgiyu-v-dar-es-salame-"
                "tanzaniya/"), RU_ROSTER_RU], "Dar es Salaam",
            emails=["filaretoskimaro@gmail.com"],
            contact_sources=[RU_ROSTER_EN, RU_ROSTER_RU]),
        row(
            "tz-ru-kisarawe-nina", "tz-ru-central-deanery", "parish",
            "Parish", "Parish of Saint Nina Equal-to-the-Apostles in Kisarawe",
            "Приход святой равноапостольной Нины в г. Кисараве",
            [ru("novosti/v-prazdnik-ikony-bozhiej-materi-troeruchicza-"
                "mitropolit-konstantin-sovershil-liturgiyu-na-prihode-"
                "svyatoj-niny-v-tanzanii-2/"), RU_VISIT], "Kisarawe"),
        row(
            "tz-ru-kimamba-nicholas", "tz-ru-central-deanery", "parish",
            "Church", "Saint Nicholas the Wonderworker Church in Kimamba",
            "Храм святителя Николая Чудотворца в с. Кимамба",
            [ru("novosti/v-nikolskom-hrame-v-s-kimamba-tanzaniya-pyat-"
                "chelovek-prinyali-tainstvo-kreshheniya/"),
             ru("novosti/mitropolit-konstantin-osvyatil-hram-svyatitelya-"
                "nikolaya-chudotvorcza-v-tanzanii-i-sovershil-liturgiyu-"
                "v-novoosvyashhennom-hrame-2/"), RU_VISIT],
            "Kimamba, Morogoro Region"),
        row(
            "tz-ru-melela-vladimir", "tz-ru-central-deanery", "parish",
            "Parish", "Parish of Saint Vladimir Equal-to-the-Apostles in Melela",
            "Приход святого равноапостольного великого князя Владимира в с. Мелела",
            [ru("novosti/provedena-beseda-po-osnovam-pravoslavnoj-very-v-"
                "obshhine-plemeni-masai-v-tanzanii/")], "Melela"),
        row(
            "tz-ru-nyamahana-catherine", "tz-ru-central-deanery",
            "parish", "Parish",
            "Parish of Saint Catherine the Great Martyr in Nyamahana",
            "Приход великомученицы Екатерины в с. Ньямахана",
            [ru("novosti/sem-chelovek-prinyali-tainstvo-kreshheniya-na-"
                "prihode-velikomucheniczy-ekateriny-v-tanzanii/")],
            "Nyamahana"),
        row(
            "tz-ru-venda-theotokos-construction", "tz-ru-central-deanery",
            "parish", "Church Under Construction",
            "Church of the Most Holy Theotokos Under Construction in Venda",
            "Строящийся храм в честь Пресвятой Богородицы в с. Венда",
            [ru("donations/pomozhem-postroit-hram-presvyatoj-bogorodiczy-"
                "v-tanzanii/")], "Venda, Iringa Region"),
        row(
            "tz-ru-mafuluto-cyril-alexandria", "tz-ru-central-deanery",
            "parish", "Parish", "Parish of Saint Cyril of Alexandria in Mafuluto",
            "Приход святителя Кирилла Александрийского в с. Мафулуто",
            [ru("novosti/27-chelovek-kreshheny-v-okruge-iringa-tanzaniya/")],
            "Mafuluto, Iringa Region"),
        row(
            "tz-ru-imamba-cyril", "tz-ru-northern-deanery", "parish",
            "Parish", "Parish of Saint Cyril Equal-to-the-Apostles in Imamba",
            "Приход равноапостольного Кирилла, учителя Словенского, в с. Имамба",
            [RU_ROSTER_RU, ru("fotoalbomy/na-prihode-ravnoapostolnogo-"
                "kirilla-v-tanzanii-soversheno-tainstvo-kreshheniya/")],
            "Imamba", emails=["petermajuni@gmail.com"],
            contact_sources=[RU_ROSTER_EN, RU_ROSTER_RU]),
        row(
            "tz-ru-kikatiti-seraphim-sarov", "tz-ru-northern-deanery",
            "parish", "Parish", "Parish of Saint Seraphim of Sarov in Kikatiti",
            "Приход преподобного Серафима Саровского в г. Кикатити",
            [ru("novosti/mitropolit-konstantin-posetil-prihod-"
                "prepodobnogo-serafima-sarovskogo-na-severe-tanzanii/"),
             RU_VISIT], "Kikatiti, Arusha Region"),
        row(
            "tz-ru-runyinya-george", "tz-ru-northern-deanery", "parish",
            "Parish", "Parish of Saint George the Victory-Bearer in Runyinya",
            "Приход великомученика Георгия Победоносца в с. Руньинья",
            [ru("novosti/sostoyalos-sobranie-duhovenstva-severnogo-"
                "blagochiniya-tanzanii/")], "Runyinya"),
        row(
            "tz-ru-silayo-nicholas", "tz-ru-northern-deanery", "parish",
            "Parish", "Parish of Saint Nicholas the Wonderworker in Silayo",
            "Приход святителя Николая Чудотворца в с. Силайо",
            [ru("novosti/v-severnom-blagochinii-tanzanii-prinyali-"
                "tainstvo-kreshheniya-16-mestnyh-zhitelej/")], "Silayo"),
        row(
            "tz-ru-butengo-nicholas", "tz-ru-northern-deanery", "parish",
            "Parish", "Parish of Saint Nicholas the Wonderworker in Butengo",
            "Приход святителя Николая Чудотворца в с. Бутенго",
            [ru("novosti/v-nedelyu-8-yu-po-pyatidesyatnicze-patriarshij-"
                "ekzarh-afriki-sovershil-liturgiyu-na-nikolskom-prihode-"
                "v-tanzanii-2/"), RU_VISIT], "Butengo"),
        row(
            "tz-ru-musoma-demetrius", "tz-ru-northern-deanery", "parish",
            "Parish", "Parish of Saint Demetrius the Great Martyr in Musoma",
            "Приход великомученика Димитрия Солунского в г. Мусома",
            [ru("novosti/priobreten-tent-dlya-prihoda-velikomuchenika-"
                "dimitriya-solunskogo-v-tanzanii/"), RU_VISIT], "Musoma"),
        row(
            "tz-ru-mwanza-annunciation", "tz-ru-northern-deanery",
            "parish", "Parish", "Annunciation Parish in Mwanza",
            "Благовещенский приход в г. Мванза",
            [ru("novosti/patriarshij-ekzarh-afriki-sovershil-tainstvo-"
                "kreshheniya-v-vodah-ozera-viktoriya/"), RU_VISIT], "Mwanza"),
        row(
            "tz-ru-bugaza-peter-paul", "tz-ru-northern-deanery",
            "parish", "Parish",
            "Parish of the Holy Apostles Peter and Paul in Bugaza",
            "Приход святых апостолов Петра и Павла в с. Бугаза",
            [ru("novosti/episkop-konstantin-sovershil-liturgiyu-i-"
                "kreshhenie-na-prihode-app-petra-i-pavla-v-tanzanii/")],
            "Bugaza"),
        row(
            "tz-ru-mgajwale-cosmas-damian", "tz-ru-northern-deanery",
            "parish", "Parish", "Parish of Saints Cosmas and Damian in Mgajwale",
            "Приход святых бессребреников Космы и Дамиана в с. Мгаджвале",
            [ru("novosti/i-o-patriarshego-ekzarha-afriki-sovershil-"
                "moleben-na-prihode-svv-kosmy-i-damiana-v-tanzanii/")],
            "Mgajwale"),
        row(
            "tz-ru-nyakahama-anthony-great", "tz-ru-northern-deanery",
            "parish", "Parish", "Parish of Saint Anthony the Great in Nyakahama",
            "Приход преподобного Антония Великого в с. Ньякахама",
            [ru("novosti/episkop-konstantin-sovershil-moleben-na-"
                "prihode-v-chest-prp-antoniya-velikogo-v-tanzanii/")],
            "Nyakahama"),
    ],
}

EXPECTED = {"ax-irinopolis": 1, "ax-arusha": 1, "ax-bukoba": 2,
            "ru-south-africa": 19}
EXPECTED_TOTAL = 23
EXPECTED_RUSSIAN_DEANERIES = 2
EXPECTED_RUSSIAN_PARISHES = 17
EXPECTED_RUSSIAN_ROSTER_PARISHES = 31
ALLOWED_KINDS = {"diocese", "parish", "monastery"}
ALLOWED_RANKS = {
    "Deanery", "Parish", "Church", "Cathedral",
    "Metropolitan Cathedral", "Monastery", "Church Under Construction",
}
ENGLISH_NAMES = {r["id"]: r["name"] for rows in ROWS.values() for r in rows}
ENGLISH_SEATS = {
    r["seat"]: r["seat"] for rows in ROWS.values() for r in rows
    if r.get("seat")
}


def clean(source):
    item = {k: v for k, v in source.items() if v not in (None, "", [])}
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
        raise ValueError("%s carries forbidden punctuation" % item.get("id"))
    return item


def validate_row(item, branch_parent, branch_seen):
    row_id = item.get("id")
    if not row_id or not re.fullmatch(r"[a-z0-9-]+", row_id):
        raise ValueError("invalid or missing id: %s" % row_id)
    if item.get("parent") not in branch_seen:
        raise ValueError("%s hangs off an unknown parent" % row_id)
    if item.get("country") != "TZ":
        raise ValueError("%s is outside Tanzania" % row_id)
    if item.get("kind") not in ALLOWED_KINDS:
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if item.get("rank") == "Deanery":
        if item.get("kind") != "diocese" or item.get("parent") != branch_parent:
            raise ValueError("%s has malformed deanery hierarchy" % row_id)
    elif item.get("kind") == "diocese":
        raise ValueError("%s uses diocese kind for a non-deanery" % row_id)
    if item.get("kind") == "monastery" and item.get("rank") != "Monastery":
        raise ValueError("%s has malformed monastery rank" % row_id)
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
            row_id = item["id"]
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
            "v": 1, "parent": branch_parent, "country": "TZ", "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Tanzania must publish exactly %d rows" % EXPECTED_TOTAL)
    russian = ROWS["ru-south-africa"]
    if sum(r["rank"] == "Deanery" for r in russian) != \
            EXPECTED_RUSSIAN_DEANERIES:
        raise ValueError("Tanzania Russian deanery total is out of sync")
    if sum(r["kind"] == "parish" for r in russian) != \
            EXPECTED_RUSSIAN_PARISHES:
        raise ValueError("Tanzania Russian parish total is out of sync")
    if EXPECTED_RUSSIAN_ROSTER_PARISHES - EXPECTED_RUSSIAN_PARISHES != 14:
        raise ValueError("Tanzania Russian roster remainder is out of sync")
    if set(ENGLISH_NAMES) != all_seen - set(ROWS):
        raise ValueError("Tanzania English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "TZ":
        raise ValueError("Tanzania candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Tanzania candidate ledger check date is out of sync")
    expected = {
        "existing_alexandrian_parents": 3,
        "alexandrian_subordinate_bodies": 4,
        "ru-south-africa": 19,
        "russian_named_deaneries": 2,
        "russian_named_parishes": 17,
        "russian_roster_total_parishes": 31,
        "russian_aggregate_only_remainder": 14,
        "new_subordinate_bodies": 23,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Tanzania candidate ledger totals are out of sync")
    sections = ("candidates", "reconciliation",
                "official_jurisdiction_audit", "exclusions")
    for key in sections:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Tanzania candidate ledger lacks %s" % key)
    ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "TZ":
            raise ValueError("%s is outside Tanzania" % candidate_id)
        ids.append(candidate_id)
    if len(ids) != len(set(ids)):
        raise ValueError("Tanzania candidate ledger has duplicate ids")
    for section in sections:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Tanzania ledger item has bad source count")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Tanzania ledger carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("Tanzania candidate ledger has forbidden punctuation")
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
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Tanzania: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Tanzania: 23 current officially named subordinate bodies "
              "across 4 existing parent branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
