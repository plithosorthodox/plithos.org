#!/usr/bin/env python3
"""Validate exact named Nea Krini and Kalamaria bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_nea_krini_country.py --check
    python tools/directory_nea_krini_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "nea_krini_country.json"
)
PARENT = "ep-nea-krini"
ROSTER_PAGE = "https://imkal.gr/churches/"
HISTORY_PAGE = "https://imkal.gr/istoriko/"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-neas-krinis-kalamarias/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/neas-krenes-kai-kalamarias"
)


# local | dedication | seat | rank | phone | email | address | detail page
BODY_ROWS = r'''
Ιερός Μητροπολιτικός Ναός Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Kalamaria|Metropolitan Church|2310 481 690|met.metamorfosewskal@gmail.com|Μητροπολίτου Χρυσάνθου 1, Θεσσαλονίκη, 551 32|https://imkal.gr/churches/metamorfoseos-tou-sotiros/
Ιερός Καθεδρικός Ναός Αγίου Νικολάου|Saint Nicholas|Aretso, Kalamaria|Cathedral|2310 444 482|agiosnikolaosaretsous@gmail.com|Αγίου Νικολάου 18, Καλαμαριά 551 32|https://imkal.gr/churches/agiou-nikolaou-kathedrikos/
Ιερός Ναός Αγίου Παντελεήμονος|Saint Panteleimon|Votsi, Kalamaria|Parish Church|2310 431 010|agiospanteleimwn2024@gmail.com|Ελ. Βενιζέλου και, Παντελεήμονος 1, Καλαμαριά 551 33|https://imkal.gr/churches/agios-panteleimonas-votsi/
Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|Saint John the Forerunner|Katirli, Kalamaria|Parish Church|2310 454 890|AgiosioannisKatirli@hotmail.com|Ι. Πασαλίδη & Μουδανιών γωνία, Καλαμαριά 551 32|https://imkal.gr/churches/agios-ioannis-prodromou-katirli/
Ιερός Ναός Ευαγγελισμού της Θεοτόκου|Annunciation of the Theotokos|Mikro Emvolo, Kalamaria|Parish Church|2310 410 530|evagelismos.kalamarias@gmail.com|Βλασίου Γαβριηλίδη 113, Καλαμαριά 551 31|https://imkal.gr/churches/evagelismou-tis-theotokou/
Ιερός Ναός Αγίων Χαραλάμπους & Αργυρής|Saints Charalambos and Argyri|Kifisia|Parish Church|23160 76918||Αλκύονος 3, Καλαμαριά 551 34|https://imkal.gr/churches/agiwn-charalampous-argirys/
Ιερός Ναός Παμμεγίστων Ταξιαρχών|Holy Archangels|Kouri, Kalamaria|Parish Church|2310 455 055|pamtaxkal@outlook.com|Θεραπειών 22, Καλαμαριά 551 32|https://imkal.gr/churches/pammegistwn-taxiarxwn-kouri/
Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Nea Krini, Kalamaria|Parish Church|2310 444 876|inagiasparaskevis@hotmail.com|Σμύρνης 60, Καλαμαριά 551 32|https://imkal.gr/churches/agia-paraskevi/
Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|Saint John the Forerunner|Nea Krini, Kalamaria|Parish Church|2310 432 322|agiosioannis.neaskrinis@gmail.com|Λουκιανού 6, Καλαμαριά 551 32|https://imkal.gr/churches/agios-ioannis-prodromou-krini/
Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Foinikas, Kalamaria|Parish Church|2310 471 906|ierosnaoskimiseostheotokoy@hotmail.com|Μυστρά 1, Καλαμαριά 551 34|https://imkal.gr/churches/koimiseos-ths-theotokou-foinikas/
Ιερός Ναός Αγίου Παύλου|Saint Paul|Nea Krini, Kalamaria|Parish Church|2310 432 334|agpavlos2003@gmail.com|Πολυβίου 53, Καλαμαριά 551 32|https://imkal.gr/churches/agios-pavlos/
Ιερός Ναός Αγίου Γεωργίου|Saint George|Epanomi|Parish Church|2392 042 797|inagiougeorgiou16@gmail.com|Σχολείου 9, Επανομή 575 00|https://imkal.gr/churches/agios-georgios-epanomi/
Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Epanomi|Parish Church|2392 045 527|belis1980@yahoo.gr|28ης Οκτωβρίου 19, Επανομή 575 00|https://imkal.gr/churches/koimiseos-ths-theotokou-epanomi/
Ιερός Ναός Αγίου Αργυρίου του Επανομίτου|Saint Argyrios of Epanomi|Epanomi|Parish Church|2392 045 026|agiosargyrios@gmail.com|Αγίου Αργυρίου, Αγίας Τριάδος, Θερμαϊκός 575 00|https://imkal.gr/churches/agios-argyrios-epanomitis/
Ιερός Ναός Παναγίας Φανερωμένης|Panagia Faneromeni|Nea Michaniona|Parish Church|2392 031 392|theos25@otenet.gr|Ντάνια, 25ης Μαρτίου, Νέα Μηχανιώνα 570 04|https://imkal.gr/churches/panagias-faneromenhs-mhxaniona/
Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Nea Michaniona|Parish Church|698 828 3791|agiosnikolaosneasmichanionas@gmail.com|Πολυτεχνείου 52, Νέα Μηχανιώνα 570 04|https://imkal.gr/churches/agios-nikolaos-mhxaniona/
Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Angelochori|Parish Church|2392 057 490|i.n.agiounikolaouaggeloxwriou@gmail.com|Αγίου Νικολάου, Αγγελοχώρι 570 04|https://imkal.gr/churches/agios-nikolaos-aggeloxori/
Ιερός Ναός Αγίας Τριάδος|Holy Trinity|Tourist Coast of Thermaikos|Parish Church|2392 051 153|in.ag.trias@gmail.com|Νώντα Γκελου, Αγ. Τριάδα 570 19|https://imkal.gr/churches/agias-triados-thermaikos/
Ιερός Ναός Παμμεγίστων Ταξιαρχών|Holy Archangels|Kerasia|Parish Church|2392 031 900|inptaxiarhon@yahoo.gr|Καραϊσκάκη, Γυγενών, Νέα Κεράσια 570 04|https://imkal.gr/churches/pammegiston-taxiarxon-kerasia/
Ιερός Ναός Οσίας Παρασκευής της Επιβατηνής|Venerable Paraskevi of Epivates|Neoi Epivates|Parish Church|2392 023 933|inoparaskevis@gmail.com|Οσίας Παρασκευής 1, Νέοι Επιβάτες 570 19|https://imkal.gr/churches/osia-paraskevi-epivatini/
Ιερός Ναός Αγίων Στεφάνου & Αναργύρων|Saints Stephen and the Holy Unmercenaries|Neoi Epivates|Parish Church|2310 471 906|enoria.agiou.stefanou.ne@gmail.com|Δημοκρατίας 246, Νέοι Επιβάτες 570 19|https://imkal.gr/churches/agios-stefanos-anargyrwn/
Παρεκκλήσι Αγίου Νεομάρτυρος Γεωργίου εκ Κρήνης|Saint Neomartyr George of Krini|Nea Krini|Chapel|2310481810|parekklisia@imkal.gr|Γαγγύλη Μανώλη 16, Καλαμαριά 551 32|https://imkal.gr/churches/parekklisi-agios-georgios-neakrini/
Παρεκκλήσι Αγίων Αλεξάνδρου & Μοδέστου|Saints Alexander and Modest|former Kodra Camp, Kalamaria|Chapel|2310481810|parekklisia@imkal.gr|Πρώην στρατόπεδο «Κόδρα» Καλαμαριά|https://imkal.gr/churches/parekklisi-agiwn-alexandrou-modestou/
Παρεκκλήσι Παναγίας Μεγαλόγχαρης & Αγίου Νικολάου|Panagia Megalochari and Saint Nicholas|NAOKTH, Kalamaria|Chapel|2310481810|parekklisia@imkal.gr|Νικ. Πλαστήρα 2, Καλαμαριά 551 31|https://imkal.gr/churches/parekklisi-megaloharis-nikolaou/
Παρεκκλήσι Αγίας Κυριακής|Saint Kyriaki|Drosia settlement, Nea Michaniona|Chapel||parekklisia@imkal.gr|Οικισμός «Δροσιά», Νέα Μηχανιώνα|https://imkal.gr/churches/parekklisi-agias-kyriakis-mhxaniona/
Παρεκκλήσι Αγίων Κωνσταντίνου & Ελένης|Saints Constantine and Helen|Kyverneio, Kalamaria|Chapel||parekklisia@imkal.gr|Εντός του Κυβερνείου Καλαμαριάς (Παλατάκι)|https://imkal.gr/churches/parekklisi-agiwn-konstantinou-elenhs/
Παρεκκλήσι Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Epanomi Beach|Chapel||parekklisia@imkal.gr|Παραλία Επανομή, 575 00|https://imkal.gr/churches/parekklisi-metamorfoseos-tou-sotitos-epanomi/
Παρεκκλήσι Αγίου Παύλου|Saint Paul|Saint Paul General Hospital of Thessaloniki|Hospital Chapel||fathersymeon@gmail.com|ΓΝΘ «Άγιος Παύλος», Εθ. Αντιστάσεως 161, Καλαμαριά 551 34|https://imkal.gr/churches/parekklisi-agiou-pavlou/
Παρεκκλήσι Αγίου Λαζάρου|Saint Lazarus|Kalamaria Municipal Cemetery|Cemetery Chapel|2310481810 εσωτ. 2|imnkrkal@otenet.gr|Δημοτικό Κοιμητήριο Καλαμαριάς;;Κων/νου Καραμανλή 40, Καλαμαριά 551 32|https://imkal.gr/churches/parekklisi-agiou-lazarou/
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "body"


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def build_rows():
    rows = []
    body_lines = BODY_ROWS.strip().splitlines()
    if len(body_lines) != 29:
        raise ValueError("expected 21 parish pages and eight chapel pages")
    for index, raw in enumerate(body_lines, 1):
        (local, dedication, seat, rank, phone, email, address,
         detail_page) = raw.split("|", 7)
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-nea-krini-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": address.split(";;"),
            "site": detail_page,
            "sources": [ROSTER_PAGE, detail_page],
        }
        if phone:
            item["phones"] = [phone]
        if email:
            item["emails"] = [email]
        if phone or email:
            item["contact_sources"] = [detail_page]
            item["contact_checked"] = CHECKED
        rows.append(item)
    rows.append({
        "id": "gr-ep-nea-krini-030-saint-catherine-monastery-epanomi",
        "parent": PARENT,
        "kind": "monastery",
        "rank": "Monastery",
        "name": "Saint Catherine Monastery in Epanomi",
        "local": "Ἱερά Μονή Ἁγίας Αἰκατερίνης",
        "seat": "Epanomi",
        "country": "GR",
        "address": ["Επανομή"],
        "sources": [PATRIARCHATE_PAGE],
    })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 30
EXPECTED_OWNER_COUNTS = {PARENT: 30}
EXPECTED_KINDS = {"monastery": 1, "parish": 29}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Chapel": 1,
    "Chapel": 6,
    "Hospital Chapel": 1,
    "Metropolitan Church": 1,
    "Monastery": 1,
    "Parish Church": 19,
}
EXPECTED_CONTACT_BODIES = 29
EXPECTED_PHONE_BODIES = 25
EXPECTED_PHONE_VALUES = 25
EXPECTED_EMAIL_BODIES = 28
EXPECTED_EMAIL_VALUES = 28
EXPECTED_SITE_BODIES = 29
EXPECTED_ADDRESS_BODIES = 30
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


def validate_url(value, label):
    parsed = urlparse(value)
    allowed = {
        "imkal.gr", "www.imkal.gr", "ec-patr.org", "www.ec-patr.org",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
    }
    if parsed.scheme != "https" or parsed.netloc not in allowed:
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
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError("contact source is outside identity sources")
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s site lacks source provenance" % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Nea Krini candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Nea Krini candidate ledger date drifted")
    expected_summary = {
        PARENT: 30,
        "total": 30,
        "exact_parish_pages": 21,
        "exact_chapel_pages": 8,
        "parish_kind_rows": 29,
        "monastery_kind_rows": 1,
        "contact_bodies": 29,
        "phone_bodies": 25,
        "public_phone_values": 25,
        "email_bodies": 28,
        "public_email_values": 28,
        "official_detail_sites": 29,
        "address_bodies": 30,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Nea Krini ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Nea Krini ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Nea Krini ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Nea Krini ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Nea Krini ledger has duplicate candidate ids")
    if FORBIDDEN_PUNCTUATION.search(
            json.dumps(ledger, ensure_ascii=False)):
        raise ValueError("Nea Krini ledger has forbidden punctuation")
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
            raise ValueError("%s lacks name, local name, or seat" % row_id)
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
            raise ValueError("%s duplicates %s after normalization" % (
                row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (
            EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Nea Krini English name coverage drifted")
    if set(ENGLISH_SEATS) != {
            item["seat"] for item in result if item.get("seat")}:
        raise ValueError("Nea Krini English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Nea Krini parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Nea Krini kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Nea Krini rank totals drifted: %r" %
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
        raise ValueError("Nea Krini contact coverage drifted: %r" %
                         (coverage,))
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
            "Nea Krini and Kalamaria: %d exact named bodies; %d carry "
            "current public contact paths" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Nea Krini and Kalamaria: %s" % exc,
              file=sys.stderr)
        raise SystemExit(1)
