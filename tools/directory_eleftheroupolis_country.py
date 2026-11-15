#!/usr/bin/env python3
"""Validate exact named Eleftheroupolis bodies from first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_eleftheroupolis_country.py --check
    python tools/directory_eleftheroupolis_country.py --dump
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates"
    / "eleftheroupolis_country.json"
)
PARENT = "ep-eleftheroupolis"
ROSTER_PAGE = (
    "https://imelef.gr/"
    "%CE%B5%CE%BD%CE%BF%CF%81%CE%AF%CE%B5%CF%82-"
    "%CE%BA%CE%BB%CE%AE%CF%81%CE%BF%CF%82"
)
METROPOLITAN_CATHEDRAL_PAGE = (
    "https://imelef.gr/"
    "%CE%BC%CE%B7%CF%84%CF%81%CE%BF%CF%80%CE%BF%CE%BB%CE%B9%CF%84%CE%B9%CE%BA%CF%8C%CF%82-"
    "%CE%B9%CE%B5%CF%81%CF%8C%CF%82-%CE%BD%CE%B1%CF%8C%CF%82-"
    "%CE%B1%CE%B3%CE%AF%CE%BF%CF%85-%CE%BD%CE%B9%CE%BA%CE%BF"
)
SAINT_ELEUTHERIUS_PUBLICATION = (
    "https://imelef.gr/wp-content/uploads/2021/02/Amvon_1.pdf"
)
MONASTERY_FORERUNNER = (
    "https://imelef.gr/"
    "%CE%B9%CE%B5%CF%81%CE%B1-%CE%BC%CE%BF%CE%BD%CE%B7-"
    "%CF%84%CE%B9%CE%BC%CE%B9%CE%BF%CF%85-"
    "%CF%80%CF%81%CE%BF%CE%B4%CF%81%CE%BF%CE%BC%CE%BF%CF%85-"
    "%CE%BD%CE%B9%CE%BA%CE%B7%CF%83%CE%B9%CE%B1%CE%BD%CE%B7"
)
MONASTERY_DEMETRIUS = (
    "https://imelef.gr/"
    "%CE%B9%CE%B5%CF%81%CE%B1-%CE%BC%CE%BF%CE%BD%CE%B7-"
    "%CE%B1%CE%B3%CE%B9%CE%BF%CF%85-"
    "%CE%B4%CE%B7%CE%BC%CE%B7%CF%84%CF%81%CE%B9%CE%BF%CF%85"
)
MONASTERY_PANTELEIMON = (
    "https://imelef.gr/"
    "%CE%B9%CE%B5%CF%81%CE%B1-%CE%BC%CE%BF%CE%BD%CE%B7-"
    "%CE%B1%CE%B3%CE%B9%CE%BF%CF%85-"
    "%CF%80%CE%B1%CE%BD%CF%84%CE%B5%CE%BB%CE%B5%CE%B7%CE%BC%CE%BF%CE%BD%CE%BF%CF%83"
)
SAINT_NECTARIUS_NEWS = "https://imelef.gr/archives/17533"
SAINT_PARASKEVI_PAGE = "https://imelef.gr/archives/12159"
MEETING_AND_PAISIOS_NEWS = "https://imelef.gr/archives/17276"
MARY_MAGDALENE_NEWS = "https://imelef.gr/archives/17319"
OLD_AVLI_ELIJAH_NEWS = "https://imelef.gr/archives/17315"
NIKISIANI_ELIJAH_NEWS = "https://imelef.gr/archives/17311"


PARISH_ROWS = r'''
Eleftheroupolis|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|25920-22398|Metropolitan Cathedral|cathedral
Eleftheroupolis|Ιερός Ναός Αγίου Ελευθερίου|Saint Eleutherius|25920-22269|Cathedral|cathedral
Akrovouni|Ιερός Ναός Κοιμήσεως Θεοτόκου|Dormition of the Theotokos|25920-22984|Parish Church|
Avli|Ιερός Ναός Προφήτου Ηλιού|Prophet Elijah|25920-52070|Parish Church|
Domatia|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen|25920-51297|Parish Church|
Exochi|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi||Parish Church|
Kipia|Ιερός Ναός Αγίου Γεωργίου|Saint George|25920-51477|Parish Church|
Melissa|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius||Parish Church|
Melissokomeio|Ιερός Ναός Αγίου Γεωργίου|Saint George||Parish Church|
Mesia|Ιερός Ναός Αγίας Βαρβάρας|Saint Barbara|25920-52343|Parish Church|
Mesotopos|Ιερός Ναός Τιμίου Προδρόμου|Saint John the Forerunner||Parish Church|
Pyrgochori|Ιερός Ναός Αγίου Αντωνίου|Saint Anthony|2510-250014|Parish Church|
Sidirochori|Ιερός Ναός Αγίου Γεωργίου|Saint George||Parish Church|
Chrysokastro|Ιερός Ναός Παμμεγίστων Ταξιαρχών|Holy Archangels|25920-51986|Parish Church|
Agios Andreas|Ιερός Ναός Ἁγίου Ἀνδρέου|Saint Andrew|25940-23273|Parish Church|
Elaiochori|Ιερός Ναός Αγίου Γεωργίου|Saint George|25940-92200|Parish Church|
Eleftheres|Ιερός Ναός Παμεγίστων Ταξιαρχών|Holy Archangels|25940-92174|Parish Church|
Myrtofyto|Ιερός Ναός Κοιμήσεως Θεοτόκου|Dormition of the Theotokos|25940-92061|Parish Church|
Nea Iraklitsa|Ιερός Ναός Παναγίας Φανερωμένης και Αγίου Γεωργίου|Panagia Phaneromeni and Saint George|25940-21028|Parish Church|
Nea Peramos|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas||Parish Church|
Nea Peramos|Ιερός Ναός Παναγίας Φανερωμένης|Panagia Phaneromeni||Parish Church|
Folia|Ιερός Ναός Αγίου Γεωργίου|Saint George|25940-92090|Parish Church|
Akropotamos|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius||Parish Church|
Galipsos|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|25920-41298|Parish Church|
Kariani|Ιερός Ναός Αγίου Αθανασίου|Saint Athanasius|2510-243612|Parish Church|
Kokkinochori|Ιερός Ναός Αγίου Νέστορος|Saint Nestor|25920-44996|Parish Church|
Mesoropi|Ιερός Ναός Αγίου Γεωργίου|Saint George|25920-93363|Parish Church|
Moustheni|Ιερός Ναός Κοιμήσεως Θεοτόκου|Dormition of the Theotokos|25920-51422|Parish Church|
Orfanio|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos||Parish Church|
Ofrinio|Ιερός Ναός Αγίου Γεωργίου|Saint George|25920-41638|Parish Church|
Paralia Ofriniou|Ιερός Ναός Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior||Parish Church|
Platanotopos|Ιερός Ναός Αγίου Ἀθανασίου|Saint Athanasius|25920-44064|Parish Church|
Podochori|Ιερός Ναός Αγίου Γεωργίου|Saint George||Parish Church|
Agios Christoforos|Ιερός Ναός Αγίου Ιωάννου Θεολόγου|Saint John the Theologian||Parish Church|
Antifilippoi|Ιερός Ναός Ζωοδόχου Πηγής|Life-Giving Spring|25920-43988|Parish Church|
Georgiani|Ιερός Ναός Υψώσεως Τιμίου Σταυρού|Exaltation of the Holy Cross|25920-61846|Parish Church|
Dryada|Ιερός Ναός Αγίου Παντελεήμονος|Saint Panteleimon|25920-43982|Parish Church|
Nikisiani|Ιερός Ναός Εισοδίων της Θεοτόκου|Entry of the Theotokos|25920-61298|Parish Church|
Palaiochori|Ιερός Ναός Αγίου Γεωργίου - Αποστόλου Θωμά|Saint George and Apostle Thomas|25920-43342|Parish Church|
Chortokopi|Ιερός Ναός Αγίου Ευγενίου|Saint Eugene||Parish Church|
'''


MONASTIC_ROWS = [
    {
        "seat": "Nikisiani",
        "local": "Ιερά Μονή Τιμίου Προδρόμου Νικησιανής",
        "dedication": "Saint John the Forerunner",
        "phone": "25920-61415",
        "address": ["Ιερά Μονή Τιμίου Προδρόμου", "640 01 ΝΙΚΗΣΙΑΝΗ"],
        "source": MONASTERY_FORERUNNER,
    },
    {
        "seat": "Nikisiani",
        "local": "Ιερά Μονή Αγίου Δημητρίου Νικησιανής",
        "dedication": "Saint Demetrius",
        "phone": "25920-61215",
        "address": ["Ιερά Μονή Αγίου Δημητρίου", "640 01 ΝΙΚΗΣΙΑΝΗ"],
        "source": MONASTERY_DEMETRIUS,
    },
    {
        "seat": "Chrysokastro",
        "local": "Ιερά Μονή Αγίου Παντελεήμονος Χρυσοκάστρου",
        "dedication": "Saint Panteleimon",
        "phone": "25920-51449",
        "address": [
            "Ιερά Μονή Αγίου Παντελεήμονος, Χρυσόκαστρο",
            "641 00 ΕΛΕΥΘΕΡΟΥΠΟΛΙΣ",
        ],
        "source": MONASTERY_PANTELEIMON,
    },
]


PILGRIMAGE_ROWS = [
    {
        "seat": "Eleftheroupolis",
        "local": "Προσκυνηματικός Ιερός Ναός Αγίου Νεκταρίου Ελευθερουπόλεως",
        "dedication": "Saint Nectarius",
        "rank": "Pilgrimage Church",
        "source": SAINT_NECTARIUS_NEWS,
    },
    {
        "seat": "Agiasma, Eleftheroupolis",
        "local": "Προσκυνηματικός Ναΐσκος Αγίας Παρασκευής στο Αγίασμα Ελευθερούπολης",
        "dedication": "Saint Paraskevi",
        "rank": "Pilgrimage Church",
        "source": SAINT_PARASKEVI_PAGE,
    },
]


ADDITIONAL_ROWS = [
    {
        "seat": "Galipsos",
        "local": "Ιερός Ναός Υπαπαντής του Σωτήρος και Οσίου Παϊσίου του Αγιορείτου Γαληψού",
        "dedication": "Meeting of the Lord and Venerable Paisios the Athonite",
        "rank": "Church",
        "source": MEETING_AND_PAISIOS_NEWS,
    },
    {
        "seat": "Domatia",
        "local": "Ιερό Παρεκκλήσιο Αγίας Μαρίας της Μαγδαληνής Δωματίων",
        "dedication": "Saint Mary Magdalene",
        "rank": "Chapel",
        "source": MARY_MAGDALENE_NEWS,
    },
    {
        "seat": "Palaia Avli",
        "local": "Παλαιός Ιερός Ναός Προφήτου Ηλιού Παλαιάς Αυλής",
        "dedication": "Prophet Elijah",
        "rank": "Historic Church",
        "source": OLD_AVLI_ELIJAH_NEWS,
    },
    {
        "seat": "Nikisiani",
        "local": "Ιερό Παρεκκλήσιο Προφήτου Ηλιού Νικησιανής",
        "dedication": "Prophet Elijah",
        "rank": "Chapel",
        "source": NIKISIANI_ELIJAH_NEWS,
    },
]


def slug(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_lines(block, columns):
    result = []
    for line in block.strip().splitlines():
        values = [value.strip() for value in line.split("|")]
        if len(values) != len(columns):
            raise ValueError("invalid Eleftheroupolis source row: %s" % line)
        result.append(dict(zip(columns, values)))
    return result


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def build_rows():
    rows = []
    index = 0
    columns = ("seat", "local", "dedication", "phone", "rank", "detail")
    for record in parse_lines(PARISH_ROWS, columns):
        index += 1
        name = make_name(record["dedication"], record["rank"],
                         record["seat"])
        sources = [ROSTER_PAGE]
        if record["detail"] == "cathedral" and index == 1:
            sources.append(METROPOLITAN_CATHEDRAL_PAGE)
        elif record["detail"] == "cathedral" and index == 2:
            sources.append(SAINT_ELEUTHERIUS_PUBLICATION)
        item = {
            "id": "gr-ep-eleftheroupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "sources": sources,
        }
        if record["phone"]:
            item["phones"] = [record["phone"]]
            item["contact_sources"] = [ROSTER_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)
    for record in MONASTIC_ROWS:
        index += 1
        rank = "Monastery"
        name = make_name(record["dedication"], rank, record["seat"])
        rows.append({
            "id": "gr-ep-eleftheroupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "phones": [record["phone"]],
            "sources": [record["source"]],
            "contact_sources": [record["source"]],
            "contact_checked": CHECKED,
        })
    for record in PILGRIMAGE_ROWS:
        index += 1
        name = make_name(record["dedication"], record["rank"],
                         record["seat"])
        rows.append({
            "id": "gr-ep-eleftheroupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "sources": [record["source"]],
        })
    for record in ADDITIONAL_ROWS:
        index += 1
        name = make_name(record["dedication"], record["rank"],
                         record["seat"])
        rows.append({
            "id": "gr-ep-eleftheroupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "sources": [record["source"]],
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 49
EXPECTED_OWNER_COUNTS = {PARENT: 49}
EXPECTED_KINDS = {"monastery": 3, "parish": 46}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Chapel": 2,
    "Church": 1,
    "Historic Church": 1,
    "Metropolitan Cathedral": 1,
    "Monastery": 3,
    "Parish Church": 38,
    "Pilgrimage Church": 2,
}
EXPECTED_CONTACT_BODIES = 30
EXPECTED_PHONE_BODIES = 30
EXPECTED_PHONE_VALUES = 30
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 3
EXISTING_PARENTS = {PARENT}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def unicase(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value.casefold()).strip()


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc not in {
            "imelef.gr", "www.imelef.gr"}:
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must carry one to three sources" % item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    contact_sources = list(item.get("contact_sources") or [])
    if contact_sources:
        if len(contact_sources) > 3:
            raise ValueError("%s has too many contact sources" % item.get("id"))
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError(
                    "%s contact source is outside identity sources"
                    % item.get("id")
                )
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date"
                             % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s body-owned site lacks provenance"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Eleftheroupolis candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Eleftheroupolis candidate ledger date drifted")
    expected_summary = {
        PARENT: 49,
        "total": 49,
        "parish_kind_rows": 46,
        "monastery_kind_rows": 3,
        "contact_bodies": 30,
        "phone_bodies": 30,
        "public_phone_values": 30,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 3,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Eleftheroupolis ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Eleftheroupolis ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Eleftheroupolis ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Eleftheroupolis ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Eleftheroupolis ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Eleftheroupolis ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
    signatures = {}
    rank_counts = Counter()
    kind_counts = Counter()
    owner_counts = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        parent = item.get("parent")
        if not row_id or row_id in ids or row_id in EXISTING_PARENTS:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s lacks parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s carries the wrong country" % row_id)
        if item.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s carries an unsupported kind" % row_id)
        if item.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s carries an unsupported rank" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError(
                "%s lacks an English name, Greek name, or seat" % row_id
            )
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.match(email):
                raise ValueError("%s carries an invalid email" % row_id)
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        signature = (parent, unicase(item["local"]), unicase(item["seat"]))
        if signature in signatures:
            raise ValueError(
                "%s duplicates %s after Greek normalization"
                % (row_id, signatures[signature])
            )
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d"
                         % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Eleftheroupolis English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Eleftheroupolis English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Eleftheroupolis parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Eleftheroupolis kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Eleftheroupolis rank totals drifted: %r" %
                         dict(sorted(rank_counts.items())))
    coverage = (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site"))
            for item in result),
        sum(bool(item.get("phones")) for item in result),
        sum(len(item.get("phones") or []) for item in result),
        sum(bool(item.get("emails")) for item in result),
        sum(len(item.get("emails") or []) for item in result),
        sum(bool(item.get("site")) for item in result),
        sum(bool(item.get("address")) for item in result),
    )
    expected_coverage = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected_coverage:
        raise ValueError("Eleftheroupolis contact coverage drifted: %r"
                         % (coverage,))
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Eleftheroupolis: %d exact named bodies; %d carry current "
            "institutional contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Eleftheroupolis: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
