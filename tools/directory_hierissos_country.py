#!/usr/bin/env python3
"""Validate exact named Hierissos bodies from current first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_hierissos_country.py --check
    python tools/directory_hierissos_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "hierissos_country.json"
)
PARENT = "ep-hierissos"
ROSTER_PAGE = "https://web.im-ierissou.gr/ieroi-naoi-efimerioi/"
MONASTERY_PAGE = "https://web.im-ierissou.gr/ieres-mones/"
ADMIN_PAGE = "https://web.im-ierissou.gr/dioikisi/"
HISTORY_PAGE = (
    "https://web.im-ierissou.gr/i-istoria-tis-ieras-mitropoleos/"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-ierissoy-agioy-oroys-ardamerioy/"
)


# local | dedication | seat | Greek seat | rank | phones | body site
ROSTER_ROWS = r'''
Ἐνορία Ἁγίου Στεφάνου Ἀρναίας|Saint Stephen|Arnaia|Ἀρναία|Metropolitan Cathedral|23720 23020,6944 214112,6978 617164,6981171866|https://www.inagioustefanouarnaias.com/
Ἐνορία Ἁγίων Ἀναργύρων Ἀρναίας|Holy Unmercenaries|Arnaia|Ἀρναία|Parish Church|23720 22287,6942 966002|
Ἐνορία Ἁγίου Γεωργίου Βαρβάρας|Saint George|Varvara|Βαρβάρα|Parish Church|23720 51232,6942 561101|
Ἐνορία Ἁγίου Βασιλείου Μεγάλης Παναγίας|Saint Basil|Megali Panagia|Μεγάλη Παναγία|Parish Church|23720 31568,6944 452410,6946 506011|
Ἱερό Προσκύνημα Μεγάλης Παναγίας|Megali Panagia|Megali Panagia|Μεγάλη Παναγία|Pilgrimage Church|23720 31262,6945 258456|
Ἐνορία Ἁγίου Γεωργίου Νεοχωρίου|Saint George|Neochori|Νεοχώρι|Parish Church|23720 41752,6937 283902|
Ἐνορία Παμμμεγίστων Ταξιαρχῶν Παλαιοχωρίου|Holy Archangels|Palaiochori|Παλαιοχώρι|Parish Church|23720 41604,23720 41725|
Ἐνορία Γενεσίου τῆς Θεοτόκου Σταγείρων|Nativity of the Theotokos|Stageira|Στάγειρα|Parish Church|2376 100400,6943 881043|
Ἐνορία Εἰσοδίων τῆς Θεοτόκου Στανοῦ|Entry of the Theotokos|Stanos|Στανός|Parish Church|23720 61408,6937 158085|
Ἐνορία Ἁγίου Νικολάου Στρατονίκης|Saint Nicholas|Stratoniki|Στρατονίκη|Parish Church|23760 41410,6972 407301|
Ἐνορία Γενεσίου τῆς Θεοτόκου Ἱερισσοῦ|Nativity of the Theotokos|Ierissos|Ἱερισσός|Cathedral|23770 22657,6988557712|
Ἐνορία Ἁγίου Νικολάου Ἱερισσοῦ|Saint Nicholas|Ierissos|Ἱερισσός|Parish Church|23770 23445,6949521995|
Ἐνορία Ἁγίου Νικολάου Ἀμμουλιανῆς|Saint Nicholas|Ammouliani|Ἀμμουλιανή|Parish Church|23770 51106,6973 236254,23770 51148|
Ἐνορία Παναγίας Γοματίου|Panagia|Gomati|Γομάτι|Parish Church|23770 41363,6948 063090,23770 23371|
Ἐνορία Παναγίας Νέων Ρόδων|Panagia|Nea Roda|Νέα Ρόδα|Parish Church|23770 31074,6973 532985,23770 31410|
Ἐνορία Ἁγίων Κωνσταντίνου & Ἑλένης Οὐρανουπόλεως|Saints Constantine and Helen|Ouranoupoli|Οὐρανούπολη|Parish Church|23770 71154,6985 572651|
Ἐνορία Ἁγίας Βαρβάρας Στρατωνίου|Saint Barbara|Stratoni|Στρατώνι|Parish Church|23760 22113,6986 698195|
Ἐνορία Κοιμήσεως τῆς Θεοτόκου Ἁγίου Προδρόμου|Dormition of the Theotokos|Agios Prodromos|Ἅγιος Πρόδρομος|Parish Church|23710 96034,6947 996019,6988896416|
Ἐνορία Κοιμήσεως τῆς Θεοτόκου Ἀρδαμερίου|Dormition of the Theotokos|Ardameri|Ἀρδαμέρι|Parish Church|6931782920|
Ἐνορία Κοιμήσεως τῆς Θεοτόκου Γαλατίστης|Dormition of the Theotokos|Galatista|Γαλάτιστα|Parish Church|23710 31431,23960 31309|
Ἐνορία Ἁγίου Γεωργίου Γαλατίστης|Saint George|Galatista|Γαλάτιστα|Parish Church|23710 31755,6979 425980,23710 31654,6977 418230|
Ἐνορία Ἁγίου Ἀθανασίου Παλαιοκάστρου|Saint Athanasius|Palaiokastro|Παλαιόκαστρο|Parish Church|23710 24012,6975 542653|
Ἐνορία Ἁγίου Ἁνδρέου Περιστερᾶς|Saint Andrew|Peristera|Περιστερά|Parish Church|23960 51275,6945439910|
Ἐνορία Ἁγίου Ἀθανασίου Λειβαδίου|Saint Athanasius|Livadi|Λειβάδι|Parish Church|23960 61221,6906696229|
Ἐνορία Ἁγίου Γεωργίου Ζαγκλιβερίου|Saint George|Zagliveri|Ζαγκλιβέρι|Parish Church|23930 31183,6978 323199|
Ἐνορία Ἁγίας Ἀκυλίνης Ζαγκλιβερίου|Saint Aquilina|Zagliveri|Ζαγκλιβέρι|Parish Church|6945 943651,23931 12130|
Ἐνορία Ὁσίου Ἀθανασίου Ἁγίου Χαραλάμπους|Saint Athanasius|Agios Charalambos|Ἅγιος Χαράλαμπος|Parish Church|6972 084377,23920 64622|
Ἐνορία Ἁγίας Παρασκευῆς Ἀδάμ|Saint Paraskevi|Adam|Ἀδάμ|Parish Church|23930 61278,6945 505802|
Ἐνορία Ἁγίας Παρασκευή Δουμπιῶν|Saint Paraskevi|Doumpia|Δουμπιά|Parish Church|23710 92267,6979 511767,6971 827702|
Ἐνορία Ζωοδόχου Πηγῆς Ν. Καλινδοίων (Καλαμωτοῦ)|Life-Giving Spring|Nea Kallindoia|Νέα Καλίνδοια|Parish Church|23930 81358,6938481288|
Ἐνορία Ἁγίου Γεωργίου Μεσοκώμου|Saint George|Mesokomo|Μεσόκωμο|Parish Church|6948 129474|
Ἐνορία Προφήτου Ἠλιού Πετροκεράσων|Prophet Elijah|Petrokerasa|Πετροκέρασα|Parish Church|23930 71404,6940 830422,23930 71367|
Ἐνορία Παμμεγίστων Ταξιαρχῶν Σανῶν|Holy Archangels|Sana|Σανά|Parish Church|23710 92342,6934 384602|
Ἐνορία Μεταμορφώσεως τοῦ Σωτῆρος Σαρακήνας|Transfiguration of the Savior|Sarakina|Σαρακήνα|Parish Church|23930 22779,6972 084377|
Ἐνορία Ἁγίου Γεωργίου Ἀπολλωνίας|Saint George|Apollonia|Ἀπολλωνία|Parish Church|6977 868105|
Ἐνορία Ἀποστόλου Παύλου Νέας Ἀπολλωνίας|Apostle Paul|Nea Apollonia|Νέα Ἀπολλωνία|Parish Church|23930 41288,6948 200162|
Ἐνορία Τιμίου Προδρόμου Νέας Μαδύτου|Saint John the Forerunner|Nea Madytos|Νέα Μάδυτος|Parish Church|23970 41401,6945 400354|
Ἐνορία Ἁγίων Ἀναργύρων Κοκκαλοῦς|Holy Unmercenaries|Kokkalou|Κοκκαλού|Parish Church|6945 374873|
Ἐνορία Ἁγίου Ἀθανασίου Πλατείας|Saint Athanasius|Plateia|Πλατεία|Parish Church||
Ἐνορία Ἁγίου Σπυρίδωνος Περιστερῶνος|Saint Spyridon|Peristeronas|Περιστερώνας|Parish Church|6984 4557116|
Ἐνορία Ἁγίου Γεωργίου Μελισσουργοῦ|Saint George|Melissourgos|Μελισσουργός|Parish Church|23930 41930,6974 282290|
Λουτρά Νέας Ἀπολλωνίας|Loutra Neas Apollonias|Nea Apollonia|Νέα Ἀπολλωνία|Pilgrimage Church|6948 200162|
Ἐνορία Ἁγίας Παρασκευῆς Κάτω Σταυροῦ|Saint Paraskevi|Kato Stavros|Κάτω Σταυρός|Parish Church|23970 65632,6986 539206,6983624850|
Ἐνορία Ὁσίου Αὐξεντίου Κάτω Σταυροῦ|Saint Auxentios|Kato Stavros|Κάτω Σταυρός|Parish Church|23970 61011,6987 651032|
Ἐνορία Ἁγίου Δημητρίου Ἄνω Σταυροῦ|Saint Demetrius|Ano Stavros|Ἄνω Σταυρός|Parish Church|23970 61844,6977341186|
Ἐνορία Ἁγίας Κυριακῆς Ὀλυμπιάδος|Saint Kyriaki|Olympiada|Ὀλυμπιάδα|Parish Church|23760 51589,6987484860|
Ἐνορία Ἁγίας Τριάδος Μοδίου|Holy Trinity|Modi|Μόδι|Parish Church|23970 51159,6974 830506|
Ἱερό Προσκύνημα Ἁγίας Μαρίνης Μοδίου|Saint Marina|Modi|Μόδι|Pilgrimage Church|23970 51150,69866 29887|
Ἐνορία Ἁγίου Γεωργίου Παλαιοχώρας|Saint George|Palaiochora|Παλαιοχώρα|Parish Church|23710 61321,6944 651878|
Ἐνορία Ἁγίου Δημητρίου Γεροπλατάνου|Saint Demetrius|Geroplatanos|Γεροπλάτανος|Parish Church|23710 61616,6983 653865|
Ἐνορία Κοιμήσεως τῆς Θεοτόκου Ριζῶν|Dormition of the Theotokos|Riza|Ριζά|Parish Church|23960 51030,6907332104|
Ἐνορία Ἁγίου Νικολάου Κρήμνης|Saint Nicholas|Kremni|Κρήμνη|Parish Church|23710 95227,6936 429487|
Ἐνορία Ἁγίου Γεωργίου Μαραθούσης|Saint George|Marathousa|Μαραθούσα|Parish Church|23710 95223,6974 374501|
Ἐνορία Μεταμορφώσεως τοῦ Σωτῆρος Πλατανοχωρίου|Transfiguration of the Savior|Platanohori|Πλατανοχώρι|Parish Church|6942 015594|
'''


# local | dedication | seat | Greek seat | rank | phones | emails | site
MONASTIC_ROWS = r'''
Ἱερὰ Μονὴ Ἁγίου Χριστοφόρου|Saint Christopher|Arnaia|Ἀρναία|Monastery|2372022899||
Ἱερὰ Μονὴ Ἁγίου Γενναδίου|Saint Gennadios|Livadi|Λειβάδι|Monastery|6977234951||
Μοναστικὸς Οἶκος Παναγία ἡ Χαρὰ τῶν θλιβομένων|Panagia, Joy of All Who Sorrow|Palaiochori|Παλαιοχώρι|Monastic House|23720 41725||
Ἱερὰ Μονὴ Εὐαγγελισμοῦ τῆς Θεοτόκου|Annunciation of the Theotokos|Olympiada|Ὀλυμπιάδα|Monastery|23760 51200||
Ἱερὰ Μονὴ Ἁγίου Κοσμᾶ Αἰτωλοῦ|Saint Kosmas Aitolos|Arnaia|Ἀρναία|Monastery|6944 122365,23723 04064|i.m.agiou.kosma.arnaia@gmail.com|http://skamnipatrokosma.weebly.com/
Ἡσυχαστήριο Παναγίας Φοβερᾶς Προστασίας|Panagia Fovera Prostasia|Megali Panagia|Μεγάλη Παναγία|Hermitage|2372032134||
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
    return "%s of %s, %s" % (rank, dedication, seat)


def add_contacts(item, phones, emails, site, source):
    if phones:
        item["phones"] = phones.split(",")
    if emails:
        item["emails"] = emails.split(",")
    if site:
        item["site"] = site
    if phones or emails:
        item["contact_sources"] = [source]
        item["contact_checked"] = CHECKED


def build_rows():
    rows = []
    index = 0
    roster_lines = ROSTER_ROWS.strip().splitlines()
    monastic_lines = MONASTIC_ROWS.strip().splitlines()
    if len(roster_lines) != 54:
        raise ValueError("expected 54 numbered Hierissos church rows")
    if len(monastic_lines) != 6:
        raise ValueError("expected six Hierissos monastic institutions")
    for raw in roster_lines:
        (local, dedication, seat, greek_seat, rank, phones,
         site) = raw.split("|", 6)
        index += 1
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-hierissos-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [greek_seat, "Greece"],
            "sources": [ROSTER_PAGE],
        }
        add_contacts(item, phones, "", site, ROSTER_PAGE)
        rows.append(item)
    for raw in monastic_lines:
        (local, dedication, seat, greek_seat, rank, phones, emails,
         site) = raw.split("|", 7)
        index += 1
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-hierissos-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [greek_seat, "Greece"],
            "sources": [MONASTERY_PAGE],
        }
        add_contacts(item, phones, emails, site, MONASTERY_PAGE)
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 60
EXPECTED_OWNER_COUNTS = {PARENT: 60}
EXPECTED_KINDS = {"monastery": 6, "parish": 54}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Hermitage": 1,
    "Metropolitan Cathedral": 1,
    "Monastic House": 1,
    "Monastery": 4,
    "Parish Church": 49,
    "Pilgrimage Church": 3,
}
EXPECTED_CONTACT_BODIES = 59
EXPECTED_PHONE_BODIES = 59
EXPECTED_PHONE_VALUES = 118
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 2
EXPECTED_ADDRESS_BODIES = 60
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
        "web.im-ierissou.gr", "ec-patr.org", "www.ec-patr.org",
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
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Hierissos candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Hierissos candidate ledger date drifted")
    expected_summary = {
        PARENT: 60,
        "total": 60,
        "parish_kind_rows": 54,
        "monastery_kind_rows": 6,
        "contact_bodies": 59,
        "phone_bodies": 59,
        "public_phone_values": 118,
        "email_bodies": 1,
        "public_email_values": 1,
        "body_owned_sites": 2,
        "address_bodies": 60,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Hierissos ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Hierissos ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Hierissos ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Hierissos ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Hierissos ledger has duplicate candidate ids")
    if FORBIDDEN_PUNCTUATION.search(
            json.dumps(ledger, ensure_ascii=False)):
        raise ValueError("Hierissos ledger has forbidden punctuation")
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
        raise ValueError("Hierissos English name coverage drifted")
    if set(ENGLISH_SEATS) != {
            item["seat"] for item in result if item.get("seat")}:
        raise ValueError("Hierissos English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Hierissos parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Hierissos kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Hierissos rank totals drifted: %r" %
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
        raise ValueError("Hierissos contact coverage drifted: %r" %
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
            "Hierissos: %d exact named bodies; %d carry current public "
            "contact paths" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Hierissos: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
