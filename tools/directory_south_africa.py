#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in South Africa.

Current competent first-party Church records establish fourteen Alexandrian
worship bodies, one Moscow Exarchate deanery with five roster bodies and one
subordinate chapel, one Romanian Orthodox community, and one Serbian Orthodox
parish. Parallel structures are preserved without deciding their competing
territorial claims. Older-only, aggregate-only, uncertain, affiliation-unclear,
and discovery-only identities remain in the companion candidate ledger.

    python tools/directory_south_africa.py --check
    python tools/directory_south_africa.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "south_africa.json"
)

AX_JOHANNESBURG = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-johannesburg-and-pretoria/?lang=en"
)
AX_GOOD_HOPE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-the-cape-of-good-hope/?lang=en"
)
AX_CONSTANTINE_HELEN_CURRENT = "https://hellenicjhb.org.za/"
AX_HOLY_PASSION = (
    "https://www.patriarchateofalexandria.com/"
    "his-beatitude-at-the-services-of-the-holy-passion-and-the-epitaphios-"
    "in-south-africa/?lang=en&print=print"
)
AX_PANTANASSA = (
    "https://www.patriarchateofalexandria.com/"
    "the-patriarch-of-alexandria-at-the-celebration-of-the-feast-of-the-"
    "entrance-of-the-theotokos-in-johannesburg/?lang=en"
)
AX_PRETORIA_CURRENT = "https://behellenic.co.za/"
AX_PRETORIA_CHURCH = "https://behellenic.co.za/church/"
AX_KRUGERSDORP = "https://westrandhellenic.co.za/our-church/"
AX_NICHOLAS_JAPAN = "https://orthodox.co.za/"
AX_SUPPORT_2018 = (
    "https://www.patriarchateofalexandria.com/"
    "the-patriarch-of-alexandria-supports-the-greeks-of-south-africa/"
    "?lang=en"
)
AX_BIRTHDAY_2021 = (
    "https://www.patriarchateofalexandria.com/"
    "the-67th-birthday-of-the-patriarch-of-alexandria/?lang=en"
)
AX_REMOTE_2021 = (
    "https://www.patriarchateofalexandria.com/"
    "the-patriarch-of-alexandria-in-the-remote-greek-communities-of-"
    "central-south-africa/?lang=en"
)
AX_CAPE_ST_GEORGE = "https://www.hcct.co.za/st-george-cathedral/"
AX_CAPE_ST_RAPHAEL = (
    "https://www.hcct.co.za/st-raphael-orthodox-church/"
)

RU_ROSTER_EN = (
    "https://exarchate-africa.ru/en/dioceses_cat/"
    "south-african-diocese/"
)
RU_ROSTER_RU = (
    "https://exarchate-africa.ru/dioceses_cat/"
    "yuzhno-afrikanskaya-eparhiya/"
)
RU_PARISH_LIST = (
    "https://www.st-sergius.info/en/category/"
    "yuzhno-afrikanskaya-eparhiya/"
)
RU_SERGIUS = (
    "https://www.st-sergius.info/en/hram-prp-sergiya-radonezhskogo/"
)
RU_SERGIUS_SITE = "https://www.st-sergius.info/en/"
RU_MARY_EGYPT = (
    "https://www.st-sergius.info/en/hram-prp-marii-egipetskoj/"
)
RU_JOHN_CLIMACUS = (
    "https://www.st-sergius.info/en/hram-prp-ioanna-lestvichnika/"
)
RU_JOHN_SITE = "https://www.theladderon136.com/blank-page"
RU_THOMAS = (
    "https://www.st-sergius.info/en/"
    "pravoslavnaya-missionerskaya-obshhina-vo-imya-svyatogo-apostola-fomy/"
)
RU_ANNUNCIATION = (
    "https://www.st-sergius.info/en/"
    "bogosluzheniya-v-rodeboshe-kejptaun/"
)
RU_VLADIMIR = (
    "https://www.st-sergius.info/en/chasovnya-vo-imya-svyatogo-"
    "ravnoapostolnogo-velikogo-knyazya-vladimira/"
)

RO_COMMUNITY = (
    "https://patriarhia.ro/en/organization-of-the-romanian-orthodox-church/"
    "external-representations-and-communities/"
)

SR_PARISH = "https://serbianorthodoxchurch.co.za/"
SR_CURRENT_SCHEDULE = (
    "https://serbianorthodoxchurch.co.za/announcements/2026-01-06-"
    "announcement-in-serbian-and-english-about-st-thomas-serbian-orthodox-"
    "church-christmas-new-year-and-january-schedule-of-services-and-"
    "celebrations/"
)
SR_CANONICAL_HISTORY = "https://svetitoma.org.za/o-crkvi/"


def row(row_id, parent, kind, rank, name, local, sources, seat=None,
        site=None, emails=None, phones=None, contact_sources=None):
    has_contacts = bool(emails or phones)
    return {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "site": site,
        "country": "ZA",
        "sources": sources,
        "emails": emails,
        "phones": phones,
        "contact_sources": contact_sources if has_contacts else None,
        "contact_checked": CHECKED if has_contacts else None,
    }


ROWS = {
    "ax-johannesburg": [
        row(
            "za-ax-johannesburg-constantine-helen",
            "ax-johannesburg",
            "parish",
            "Cathedral",
            "Cathedral of Saints Constantine and Helen in Johannesburg",
            "Cathedral of Saints Constantine and Helen in Johannesburg",
            [AX_CONSTANTINE_HELEN_CURRENT, AX_HOLY_PASSION,
             AX_JOHANNESBURG],
            "Johannesburg",
            site=AX_CONSTANTINE_HELEN_CURRENT,
            emails=["admin.hcj@gmail.com"],
            phones=["+27 82 330 6911"],
            contact_sources=[AX_CONSTANTINE_HELEN_CURRENT],
        ),
        row(
            "za-ax-johannesburg-pantanassa-entrance",
            "ax-johannesburg",
            "parish",
            "Metropolitan Church",
            "Metropolitan Church of the Entrance of the Theotokos "
            "Pantanassa in Johannesburg",
            "Ιερός Μητροπολιτικός Ναός Εισοδίων της Θεοτόκου "
            "Παντάνασσα",
            [AX_PANTANASSA, AX_JOHANNESBURG],
            "Johannesburg",
        ),
        row(
            "za-ax-pretoria-annunciation-cathedral",
            "ax-johannesburg",
            "parish",
            "Cathedral",
            "Cathedral of the Annunciation of the Theotokos in Pretoria",
            "Ιερός Καθεδρικός Ναός Ευαγγελισμού της Θεοτόκου",
            [AX_PRETORIA_CHURCH, AX_PRETORIA_CURRENT,
             AX_JOHANNESBURG],
            "Pretoria",
            site=AX_PRETORIA_CHURCH,
            emails=["office@behellenic.com"],
            phones=["+27 (0)12 362 1400"],
            contact_sources=[AX_PRETORIA_CHURCH],
        ),
        row(
            "za-ax-krugersdorp-andrew",
            "ax-johannesburg",
            "parish",
            "Church",
            "Saint Andrew Greek Orthodox Church in Krugersdorp",
            "Saint Andrew Greek Orthodox Church",
            [AX_KRUGERSDORP, AX_JOHANNESBURG],
            "Krugersdorp",
            site=AX_KRUGERSDORP,
            phones=["076 226 2924"],
            contact_sources=[AX_KRUGERSDORP],
        ),
        row(
            "za-ax-johannesburg-nicholas-japan",
            "ax-johannesburg",
            "parish",
            "Parish",
            "Saint Nicholas of Japan Orthodox Church in Johannesburg",
            "Saint Nicholas of Japan Orthodox Church",
            [AX_NICHOLAS_JAPAN, AX_JOHANNESBURG],
            "Johannesburg",
            site=AX_NICHOLAS_JAPAN,
            emails=["st.nicholas.japan@gmail.com"],
            phones=["082-827-5049"],
            contact_sources=[AX_NICHOLAS_JAPAN],
        ),
        row(
            "za-ax-alberton-dormition",
            "ax-johannesburg",
            "parish",
            "Church",
            "Church of the Dormition of the Theotokos in Alberton",
            "Ορθόδοξος Ναός της Κοιμήσεως της Θεοτόκου",
            [AX_HOLY_PASSION, AX_JOHANNESBURG],
            "Alberton",
        ),
        row(
            "za-ax-springs-basil",
            "ax-johannesburg",
            "parish",
            "Church",
            "Church of Saint Basil in Springs",
            "Ιερός Ναός Αγίου Βασιλείου",
            [AX_SUPPORT_2018, AX_JOHANNESBURG],
            "Springs",
        ),
        row(
            "za-ax-brakpan-george",
            "ax-johannesburg",
            "parish",
            "Church",
            "Church of Saint George in Brakpan",
            "Ιερός Ναός Αγίου Γεωργίου",
            [AX_HOLY_PASSION, AX_JOHANNESBURG],
            "Brakpan",
        ),
        row(
            "za-ax-germiston-holy-forerunner",
            "ax-johannesburg",
            "parish",
            "Church",
            "Community Church of the Holy Forerunner in Germiston",
            "Community Church of the Holy Forerunner in Germiston",
            [AX_BIRTHDAY_2021, AX_JOHANNESBURG],
            "Germiston",
        ),
        row(
            "za-ax-klerksdorp-dormition",
            "ax-johannesburg",
            "parish",
            "Church",
            "Church of the Dormition of the Theotokos in Klerksdorp",
            "Church of the Dormition of the Theotokos",
            [AX_REMOTE_2021, AX_JOHANNESBURG],
            "Klerksdorp",
        ),
    ],
    "ax-good-hope": [
        row(
            "za-ax-cape-town-george-cathedral",
            "ax-good-hope",
            "parish",
            "Cathedral",
            "Saint George Cathedral in Cape Town",
            "Saint George Cathedral",
            [AX_CAPE_ST_GEORGE, AX_GOOD_HOPE],
            "Cape Town",
            site=AX_CAPE_ST_GEORGE,
            emails=["info@hcct.co.za"],
            phones=["021 433 2374"],
            contact_sources=[AX_CAPE_ST_GEORGE],
        ),
        row(
            "za-ax-cape-town-raphael",
            "ax-good-hope",
            "parish",
            "Church",
            "Saint Raphael Orthodox Church in Cape Town",
            "Saint Raphael Orthodox Church",
            [AX_CAPE_ST_RAPHAEL, AX_GOOD_HOPE],
            "Cape Town",
            site=AX_CAPE_ST_RAPHAEL,
            emails=["kykkotis@iafrica.com"],
            phones=["021 689 7639"],
            contact_sources=[AX_CAPE_ST_RAPHAEL],
        ),
        row(
            "za-ax-bloemfontein-annunciation",
            "ax-good-hope",
            "parish",
            "Church",
            "Church of the Annunciation of the Theotokos in Bloemfontein",
            "Ιερός Ναός Ευαγγελισμού της Θεοτόκου",
            [AX_REMOTE_2021, AX_GOOD_HOPE],
            "Bloemfontein",
        ),
        row(
            "za-ax-welkom-dormition",
            "ax-good-hope",
            "parish",
            "Church",
            "Church of the Dormition of the Theotokos in Welkom",
            "Church of the Dormition of the Theotokos",
            [AX_REMOTE_2021, AX_GOOD_HOPE],
            "Welkom",
        ),
    ],
    "ru-south-africa": [
        row(
            "za-ru-south-africa-deanery",
            "ru-south-africa",
            "diocese",
            "Deanery",
            "Deanery of the Republic of South Africa",
            "Благочиние Южно-Африканской Республики",
            [RU_ROSTER_EN, RU_ROSTER_RU, RU_PARISH_LIST],
            emails=["lugovoi@gmail.com"],
            contact_sources=[RU_ROSTER_EN],
        ),
        row(
            "za-ru-midrand-sergius-cathedral",
            "za-ru-south-africa-deanery",
            "parish",
            "Cathedral",
            "Cathedral of Saint Sergius of Radonezh in Midrand",
            "Кафедральный собор преподобного Сергия Радонежского",
            [RU_ROSTER_EN, RU_SERGIUS, RU_PARISH_LIST],
            "Midrand",
            site=RU_SERGIUS_SITE,
            emails=["lugovoi@gmail.com", "rector@st-sergius.info"],
            phones=["+27 11 318 0150", "+27 76 565 2225"],
            contact_sources=[RU_ROSTER_EN, RU_SERGIUS],
        ),
        row(
            "za-ru-midrand-vladimir-chapel",
            "za-ru-midrand-sergius-cathedral",
            "parish",
            "Chapel",
            "Chapel of the Holy Equal-to-the-Apostles Grand Duke Vladimir "
            "in Midrand",
            "Часовня во имя святого равноапостольного великого князя "
            "Владимира",
            [RU_VLADIMIR, RU_SERGIUS],
            "Midrand",
        ),
        row(
            "za-ru-robertson-mary-egypt",
            "za-ru-south-africa-deanery",
            "parish",
            "Church",
            "Church of Saint Mary of Egypt in Robertson",
            "Храм преподобной Марии Египетской",
            [RU_MARY_EGYPT, RU_PARISH_LIST, RU_ROSTER_EN],
            "Robertson",
            emails=["vaderzacharias@gmail.com"],
            phones=["+27 73 639 0836"],
            contact_sources=[RU_MARY_EGYPT],
        ),
        row(
            "za-ru-cape-town-john-climacus",
            "za-ru-south-africa-deanery",
            "parish",
            "Parish",
            "Parish of Saint John Climacus in Cape Town",
            "Приход преподобного Иоанна Лествичника",
            [RU_JOHN_CLIMACUS, RU_ROSTER_EN, RU_JOHN_SITE],
            "Cape Town",
            site=RU_JOHN_SITE,
            emails=["theladderchapel@gmail.com"],
            phones=["+27 82 451 1572"],
            contact_sources=[RU_JOHN_CLIMACUS, RU_ROSTER_EN],
        ),
        row(
            "za-ru-bloemfontein-thomas",
            "za-ru-south-africa-deanery",
            "parish",
            "Missionary Community",
            "Orthodox Missionary Community of Saint Thomas the Apostle "
            "in Bloemfontein",
            "Православная миссионерская община во имя святого апостола "
            "Фомы",
            [RU_THOMAS, RU_PARISH_LIST, RU_ROSTER_EN],
            "Bloemfontein",
            emails=["jr@rossouws.net"],
            phones=["+27 79 695 2600"],
            contact_sources=[RU_THOMAS],
        ),
        row(
            "za-ru-rondebosch-annunciation",
            "za-ru-south-africa-deanery",
            "parish",
            "Chapel",
            "Chapel of the Annunciation of the Most Holy Theotokos "
            "in Rondebosch",
            "Часовня Благовещения Пресвятой Богородицы",
            [RU_ANNUNCIATION, RU_PARISH_LIST, RU_ROSTER_EN],
            "Rondebosch, Cape Town",
            phones=["+27 82 44 60615"],
            contact_sources=[RU_ANNUNCIATION],
        ),
    ],
    "romania": [
        row(
            "za-ro-johannesburg-community",
            "romania",
            "parish",
            "Community",
            "Romanian Orthodox Community in South Africa, Johannesburg",
            "Comunitatea Ortodoxă Română din Africa de Sud "
            "(Johannesburg)",
            [RO_COMMUNITY],
            "Johannesburg",
            emails=["tvrazvan@yahoo.com"],
            phones=["+27 825 498 033", "+27 114 534 515"],
            contact_sources=[RO_COMMUNITY],
        ),
    ],
    "serbia": [
        row(
            "za-sr-johannesburg-thomas",
            "serbia",
            "parish",
            "Parish",
            "Saint Thomas Serbian Orthodox Church in Johannesburg",
            "Saint Thomas Serbian Orthodox Church",
            [SR_PARISH, SR_CURRENT_SCHEDULE, SR_CANONICAL_HISTORY],
            "Sunninghill, Johannesburg",
            site=SR_PARISH,
            emails=["serborthchurchsa@gmail.com"],
            phones=["+27 63 296 3862"],
            contact_sources=[SR_PARISH],
        ),
    ],
}

EXPECTED = {
    "ax-johannesburg": 10,
    "ax-good-hope": 4,
    "ru-south-africa": 7,
    "romania": 1,
    "serbia": 1,
}
EXPECTED_TOTAL = 23
EXPECTED_ALEXANDRIAN_BODIES = 14
EXPECTED_RUSSIAN_DEANERIES = 1
EXPECTED_RUSSIAN_ROSTER_BODIES = 5
EXPECTED_RUSSIAN_SUBORDINATE_CHAPELS = 1
EXPECTED_CONTACT_ROWS = 14
EXPECTED_EMAIL_ROWS = 12
EXPECTED_PHONE_ROWS = 13
EXPECTED_EMAIL_VALUES = 13
EXPECTED_PHONE_VALUES = 15
ALLOWED_RANKS = {
    "Cathedral", "Metropolitan Church", "Church", "Parish", "Community",
    "Deanery", "Chapel", "Missionary Community",
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


def validate_row(item, branch_seen):
    row_id = item.get("id")
    if not row_id or not re.fullmatch(r"[a-z0-9-]+", row_id):
        raise ValueError("invalid or missing id: %s" % row_id)
    if item.get("parent") not in branch_seen:
        raise ValueError("%s hangs off an unknown parent" % row_id)
    if item.get("country") != "ZA":
        raise ValueError("%s is outside South Africa" % row_id)
    if item.get("kind") not in ("diocese", "parish"):
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if item.get("rank") == "Deanery":
        if item.get("kind") != "diocese":
            raise ValueError("%s has malformed administrative rank" % row_id)
    elif item.get("kind") != "parish":
        raise ValueError("%s uses diocese kind for a worship body" % row_id)
    if not item.get("name") or not item.get("local"):
        raise ValueError("%s lacks a usable name" % row_id)
    if item.get("site") and not item["site"].startswith("https://"):
        raise ValueError("%s carries a non-HTTPS body site" % row_id)
    emails = item.get("emails") or []
    phones = item.get("phones") or []
    contact_sources = item.get("contact_sources") or []
    if emails or phones:
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s has an outdated contact check" % row_id)
        if not contact_sources or len(contact_sources) > 3:
            raise ValueError("%s has invalid contact sources" % row_id)
        if not all(str(url).startswith("https://")
                   for url in contact_sources):
            raise ValueError("%s has a non-HTTPS contact source" % row_id)
        if len(emails) != len(set(emails)) or len(phones) != len(set(phones)):
            raise ValueError("%s has duplicate contact values" % row_id)
        if not all(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value)
                   for value in emails):
            raise ValueError("%s has an invalid public email" % row_id)
        if not all(isinstance(value, str) and value.strip()
                   for value in phones):
            raise ValueError("%s has an invalid public phone" % row_id)
    elif contact_sources or item.get("contact_checked"):
        raise ValueError("%s has contact metadata without contacts" % row_id)


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
            validate_row(item, branch_seen)
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
            "country": "ZA",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("South Africa must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if sum(len(ROWS[parent]) for parent in
           ("ax-johannesburg", "ax-good-hope")) != \
            EXPECTED_ALEXANDRIAN_BODIES:
        raise ValueError("South Africa Alexandrian total is out of sync")
    russian_rows = ROWS["ru-south-africa"]
    if sum(item["rank"] == "Deanery" for item in russian_rows) != \
            EXPECTED_RUSSIAN_DEANERIES:
        raise ValueError("South Africa Russian deanery total is out of sync")
    roster_bodies = sum(
        item["parent"] == "za-ru-south-africa-deanery"
        for item in russian_rows
    )
    if roster_bodies != EXPECTED_RUSSIAN_ROSTER_BODIES:
        raise ValueError("South Africa Russian roster total is out of sync")
    if sum(
        item["parent"] == "za-ru-midrand-sergius-cathedral"
        for item in russian_rows
    ) != EXPECTED_RUSSIAN_SUBORDINATE_CHAPELS:
        raise ValueError("South Africa Russian chapel total is out of sync")
    if set(ENGLISH_NAMES) != all_seen - set(ROWS):
        raise ValueError("South Africa English name map is out of sync")
    contact_rows = [
        item for source_rows in ROWS.values() for item in source_rows
        if item.get("emails") or item.get("phones")
    ]
    if len(contact_rows) != EXPECTED_CONTACT_ROWS:
        raise ValueError("South Africa contact row total is out of sync")
    if sum(bool(item.get("emails")) for item in contact_rows) != \
            EXPECTED_EMAIL_ROWS:
        raise ValueError("South Africa email row total is out of sync")
    if sum(bool(item.get("phones")) for item in contact_rows) != \
            EXPECTED_PHONE_ROWS:
        raise ValueError("South Africa phone row total is out of sync")
    if sum(len(item.get("emails") or []) for item in contact_rows) != \
            EXPECTED_EMAIL_VALUES:
        raise ValueError("South Africa public email total is out of sync")
    if sum(len(item.get("phones") or []) for item in contact_rows) != \
            EXPECTED_PHONE_VALUES:
        raise ValueError("South Africa public phone total is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "ZA":
        raise ValueError("South Africa candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("South Africa candidate ledger date is out of sync")
    summary = ledger.get("published_summary") or {}
    for parent, count in EXPECTED.items():
        if summary.get(parent) != count:
            raise ValueError("South Africa ledger count is out of sync for %s" %
                             parent)
    if summary.get("alexandrian_named_bodies") != \
            EXPECTED_ALEXANDRIAN_BODIES:
        raise ValueError("South Africa ledger Alexandrian total is out of sync")
    if summary.get("russian_roster_bodies") != \
            EXPECTED_RUSSIAN_ROSTER_BODIES:
        raise ValueError("South Africa ledger Russian roster is out of sync")
    if summary.get("total") != EXPECTED_TOTAL:
        raise ValueError("South Africa ledger total is out of sync")
    required_lists = (
        "candidates", "source_reconciliations",
        "official_jurisdiction_audit",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("South Africa candidate ledger lacks %s" % key)
        for item in ledger[key]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("South Africa ledger item has invalid sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError(
                    "South Africa ledger item has a non-HTTPS source"
                )
    candidate_ids = [
        item.get("candidate_id") for item in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("South Africa ledger carries an invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("South Africa ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError(
            "South Africa candidate ledger has forbidden punctuation"
        )
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
        print("directory South Africa: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "South Africa: 23 current named bodies across Alexandrian, "
            "Moscow Exarchate, Romanian, and Serbian structures"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
