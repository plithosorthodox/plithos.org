#!/usr/bin/env python3
"""Validate exact named Mytilene worship bodies from official sources.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_mytilene_country.py --check
    python tools/directory_mytilene_country.py --check-live
    python tools/directory_mytilene_country.py --dump
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "ep-mytilene"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "mytilene_country.json"
)

LEGAL_2019 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
LEGAL_2015 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2015_iounios.pdf"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-mytilinis/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/mytilenes-eressou-kai-plomariou"
)
KALYVITES_SITE = "https://kalivitis-mitilini.gr/"
KALYVITES_CONTACT = "https://kalivitis-mitilini.gr/epikoinonia"
KALYVITES_CHAPEL_BASE = (
    "https://kalivitis-mitilini.gr/pareklisia-enorias-kaliviti-mitilinis/"
)
KALYVITES_CHAPELS = {
    "nektarios": KALYVITES_CHAPEL_BASE + "pareklisi-agios-nektarios",
    "kampadena": KALYVITES_CHAPEL_BASE + "pareklisi-panagias-kampadenas",
    "myrtidiotissa": KALYVITES_CHAPEL_BASE +
                       "pareklisi-panagia-mirtidiotisa",
    "grigorousa": KALYVITES_CHAPEL_BASE +
                    "pareklisi-panagias-grigorousa",
}
VISIT_GREECE = (
    "https://www.visitgreece.gr/en/experiences/religious-tourism/"
    "monasteries/pilgrimage-trails-on-lesvos-island"
)
RAPHAEL_SITE = "https://ieramoni-agiou-rafail.gr/en/"

SOURCES = {
    "L19": LEGAL_2019,
    "L15": LEGAL_2015,
    "EP": PATRIARCHATE_PAGE,
    "COG": CHURCH_OF_GREECE_PAGE,
    "KAL": KALYVITES_CONTACT,
    "VISIT": VISIT_GREECE,
    "RAPHAEL": RAPHAEL_SITE,
}


# Exact table order from the 2019 Church of Greece regulation.
# English seat|Greek seat|English dedication|Greek dedication
PARISH_SOURCE = r'''
Mytilene|Μυτιλήνη|Saint Athanasius|Αγίου Αθανασίου
Mytilene|Μυτιλήνη|Saint Therapon|Αγίου Θεράποντος
Mytilene|Μυτιλήνη|Saint George|Αγίου Γεωργίου
Mytilene|Μυτιλήνη|Saints Theodore|Αγίων Θεοδώρων
Mytilene|Μυτιλήνη|Saint Nicholas|Αγίου Νικολάου
Mytilene|Μυτιλήνη|Holy Trinity|Αγίας Τριάδος
Mytilene|Μυτιλήνη|Saint John Kalyvites|Αγίου Ιωάννου Καλυβίτου
Mytilene|Μυτιλήνη|Saint John the Forerunner|Τιμίου Προδρόμου
Langada, Mytilene|Λαγκάδα Μυτιλήνης|Life-Giving Spring|Ζωοδόχου Πηγής
Mytilene|Μυτιλήνη|Saint Symeon|Αγίου Συμεών
Panagia Chrysomallousa, Mytilene|Παναγία Χρυσομαλλούσα, Μυτιλήνη|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Agia Marina|Αγία Μαρίνα|Saint Marina|Αγίας Μαρίνας
Agiasos|Αγιάσος|Holy Trinity|Αγίας Τριάδος
Agra|Άγρα|Saint Demetrius|Αγίου Δημητρίου
Akleidio|Ακλειδιού|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου
Akrasi|Ακράσι|Saint Paraskevi|Αγίας Παρασκευής
Alifanta|Αλυφαντά|Saint George|Αγίου Γεωργίου
Vareia|Βαρειά|Life-Giving Spring|Ζωοδόχου Πηγής
Vasilika|Βασιλικά|Nativity of the Theotokos|Γενεσίου της Θεοτόκου
Vrisa|Βρίσα|Life-Giving Spring|Ζωοδόχου Πηγής
Eressos|Ερεσός|Saint Irene|Αγίας Ειρήνης
Eressos|Ερεσός|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Eressos|Ερεσός|Saint Constantine|Αγίου Κωνσταντίνου
Skala Eressos|Σκάλα Ερεσού|Saint Andrew of Crete|Αγίου Ανδρέου Κρήτης
Thermi|Θερμή|Entrance of the Theotokos|Εισοδίων της Θεοτόκου
Ippios|Ίππειος|Saint Procopius|Αγίου Προκοπίου
Kato Tritos|Κάτω Τρίτος|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Kerameia|Κεραμειά|Saint George|Αγίου Γεωργίου
Komi|Κώμη|Saint Theoktisti|Αγίας Θεοκτίστης
Nees Kydonies|Νέες Κυδωνίες|Saint George Chionopitis|Αγίου Γεωργίου Χιονοπίτη
Lampou Myloi|Λάμπου Μύλοι|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου
Lisvori|Λισβόρι|Saint John the Forerunner|Τιμίου Προδρόμου
Loutra|Λουτρά|Saint George|Αγίου Γεωργίου
Megalochori|Μεγαλοχώρι|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος
Mesagros|Μεσαγρός|Life-Giving Spring|Ζωοδόχου Πηγής
Mesotopos|Μεσότοπος|Entrance of the Theotokos|Εισοδίων της Θεοτόκου
Mistegna|Μιστεγνά|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Moria|Μόρια|Saint Basil|Αγίου Βασιλείου
Mychos|Μυχός|Saint George|Αγίου Γεωργίου
Neochori|Νεοχώρι|Saint Constantine|Αγίου Κωνσταντίνου
Palaiokipos|Παλαιόκηπος|Saint Hermolaus|Αγίου Ερμολάου
Palaiochori|Παλαιοχώρι|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου
Pamfila|Πάμφιλα|Saint Barbara|Αγίας Βαρβάρας
Panagiouda|Παναγιούδα|Nativity of the Theotokos|Γενεσίου της Θεοτόκου
Pappados|Παπάδος|Holy Archangels|Παμμεγίστων Ταξιαρχών
Perama|Πέραμα|Saint Panteleimon|Αγίου Παντελεήμονος
Pigi|Πηγή|Life-Giving Spring|Ζωοδόχου Πηγής
Plagia|Πλαγιά|Holy Trinity|Αγίας Τριάδος
Plakados|Πλακάδος|Saint Blaise|Αγίου Βλασίου
Pligonio|Πληγώνιο|Saint George|Αγίου Γεωργίου
Plomari|Πλωμάρι|Saint Paraskevi|Αγίας Παρασκευής
Plomari|Πλωμάρι|Saint John Chrysostom|Αγίου Ιωάννου Χρυσοστόμου
Plomari|Πλωμάρι|Saint Nicholas|Αγίου Νικολάου
Polichnitos|Πολιχνίτος|Saint George|Αγίου Γεωργίου
Polichnitos|Πολιχνίτος|Saint Paul|Αγίου Παύλου
Skala Polichnitou|Σκάλα Πολιχνίτου|Saint John the Forerunner|Τιμίου Προδρόμου
Pyrgi|Πυργί|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Pyrgoi Thermis|Πύργοι Θερμής|Saint Nicholas|Αγίου Νικολάου
Pyrgoi Peramatos|Πύργοι Περάματος|Saint Nicholas|Αγίου Νικολάου
Sigri|Σίγρι|Holy Trinity|Αγίας Τριάδος
Skopelos|Σκόπελος|Saint George|Αγίου Γεωργίου
Sykounta|Συκούντα|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Stavros|Σταυρός|Saint Paraskevi|Αγίας Παρασκευής
Taxiarches|Ταξιάρχες|Holy Archangels|Παμμεγίστων Ταξιαρχών
Trigona|Τρίγωνα|Saint Anthony|Αγίου Αντωνίου
Ano Chali|Άνω Χάλικα|Holy Fathers|Αγίων Πατέρων
Kato Chali|Κάτω Χάλικα|Saint George|Αγίου Γεωργίου
'''


# Exact legal identities present in the 2015 regulation but omitted from the
# 2019 table. The current Patriarchate aggregate of 72 parish churches equals
# the 67 rows above plus these five still legally recognized identities.
RETAINED_PARISH_SOURCE = r'''
Ampeliko|Αμπελικό|Saint Nicholas|Αγίου Νικολάου
Asomatos|Ασώματος|Holy Archangels|Παμμεγίστων Ταξιαρχών
Afalon|Αφάλων|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου
Mesagros|Μεσαγρός|Saint Nektarios|Αγίου Νεκταρίου
Kournela|Κουρνέλα|Saint John the Forerunner|Τιμίου Προδρόμου
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "body"


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def source_values(value):
    return [SOURCES[token.strip()] for token in value.split(",")
            if token.strip()]


def parish_row(index, raw, source_tokens):
    seat, greek_seat, dedication, greek_dedication = raw.split("|", 3)
    name = "Parish Church of %s, %s" % (dedication, seat)
    row = {
        "id": "gr-ep-mytilene-%03d-%s" % (index, slug(name)),
        "parent": PARENT,
        "kind": "parish",
        "rank": "Parish Church",
        "name": name,
        "local": "Ιερός Ναός %s, %s" % (greek_dedication, greek_seat),
        "seat": seat,
        "country": "GR",
        "address": [seat, "Greece"],
        "sources": source_values(source_tokens),
    }
    if dedication == "Saint John Kalyvites" and seat == "Mytilene":
        row.update({
            "phones": ["2251022391", "6948527881"],
            "emails": ["info@kalivitis-mitilini.gr"],
            "site": KALYVITES_SITE,
            "sources": [LEGAL_2019, KALYVITES_CONTACT],
            "contact_sources": [KALYVITES_CONTACT],
            "contact_checked": CHECKED,
            "live_markers": ["Αγ. Ιωάννης Καλυβίτης", "2251022391",
                             "6948527881", "info@kalivitis-mitilini.gr"],
        })
    if dedication == "Saint Nicholas" and seat == "Ampeliko":
        row.update({
            "phones": ["22520-91042"],
            "sources": [LEGAL_2015, CHURCH_OF_GREECE_PAGE],
            "contact_sources": [CHURCH_OF_GREECE_PAGE],
            "contact_checked": CHECKED,
            "live_markers": ["Αγ. Νικολάου Αμπελικού", "22520-91.042"],
        })
    return row


def exact_row(index, key, kind, rank, name, local, seat, address,
              source_tokens, phones="", emails="", site="",
              contact_tokens="", markers=""):
    row = {
        "id": "gr-ep-mytilene-%03d-%s" % (index, key),
        "parent": PARENT,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "GR",
        "address": [address, "Greece"],
        "sources": source_values(source_tokens),
        "live_markers": split_values(markers),
    }
    if phones:
        row["phones"] = split_values(phones)
    if emails:
        row["emails"] = split_values(emails)
    if site:
        row["site"] = site
    if contact_tokens:
        row["contact_sources"] = source_values(contact_tokens)
        row["contact_checked"] = CHECKED
    return row


def build_rows():
    rows = []
    current = PARISH_SOURCE.strip().splitlines()
    retained = RETAINED_PARISH_SOURCE.strip().splitlines()
    if len(current) != 67 or len(retained) != 5:
        raise ValueError("expected 67 current-table and 5 retained parishes")
    for raw in current:
        rows.append(parish_row(len(rows) + 1, raw, "L19"))
    for raw in retained:
        rows.append(parish_row(len(rows) + 1, raw, "L15,EP"))

    rows.append(exact_row(
        73, "panagia-agiasos", "parish", "Pilgrimage Church",
        "Dormition of the Theotokos Pilgrimage Church, Agiasos",
        "Ιερό Προσκύνημα Κοιμήσεως της Θεοτόκου Αγιάσου",
        "Agiasos", "Agiasos 81101", "L19,EP,VISIT",
        phones="22520-22242", contact_tokens="EP,VISIT",
        markers="Παναγία,22520-22242"
    ))
    rows.append(exact_row(
        74, "george-melanta", "parish", "Pilgrimage Church",
        "Saint George Melanta Pilgrimage Church, Polichnitos",
        "Ιερό Προσκύνημα Αγίου Γεωργίου Μελαντά",
        "Polichnitos", "Polichnitos 81300", "EP",
        markers="Ἅγιος Γεώργιος Μελαντᾶ"
    ))
    rows.append(exact_row(
        75, "john-ypsilou", "monastery", "Monastery",
        "Saint John the Theologian Ypsilou Monastery, Antissa",
        "Ιερά Μονή Αγίου Ιωάννου Θεολόγου Υψηλού",
        "Antissa", "Antissa 81103", "L15,EP,VISIT",
        phones="22530-56259", contact_tokens="EP,VISIT",
        markers="Ὑψηλοῦ,22530-56259"
    ))
    rows.append(exact_row(
        76, "archangels-pithariou", "monastery", "Monastery",
        "Holy Archangels Pithariou Monastery, Eressos",
        "Ιερά Μονή Ταξιαρχών Πιθαρίου",
        "Eressos", "Eressos 81105", "L15,EP,VISIT",
        phones="22530-53239", contact_tokens="EP,VISIT",
        markers="Πιθαρίου,22530-53239"
    ))
    rows.append(exact_row(
        77, "panagia-damandriou", "monastery", "Monastery",
        "Panagia Damandriou Monastery, Polichnitos",
        "Ιερά Μονή Παναγίας Δαμανδρίου",
        "Polichnitos", "Polichnitos 81300", "L15,EP",
        phones="22520-41319", contact_tokens="EP",
        markers="Παναγίας Δαμανδρίου,22520-41319"
    ))
    rows.append(exact_row(
        78, "saints-raphael-nicholas-irene", "monastery", "Monastery",
        "Saints Raphael, Nicholas and Irene Monastery, Thermi",
        "Ιερά Μονή Αγίων Ραφαήλ, Νικολάου και Ειρήνης",
        "Thermi", "Thermi 81100", "EP,VISIT,RAPHAEL",
        phones="22510-71259,22510-71708",
        emails="contact@ieramoni-agiou-rafail.gr",
        site=RAPHAEL_SITE, contact_tokens="EP,VISIT",
        markers="Ἁγίου Ραφαήλ,22510-71259,2251071708,contact@ieramoni-agiou-rafail.gr"
    ))
    rows.append(exact_row(
        79, "prophet-elijah-ypsilou-metochion", "monastery",
        "Monastery Metochion",
        "Prophet Elijah Metochion of Ypsilou Monastery, Mytilene",
        "Μετόχιο Προφήτου Ηλιού Ιεράς Μονής Υψηλού",
        "Mytilene", "Mytilene 81100", "EP",
        phones="22510-47724", contact_tokens="EP",
        markers="Προφ. Ἠλιού,22510-47724"
    ))
    chapel_rows = (
        ("nektarios-chapel", "Saint Nektarios Parish Chapel",
         "Παρεκκλήσι Αγίου Νεκταρίου", "nektarios", "Άγιος Νεκτάριος"),
        ("panagia-kampadena-chapel", "Panagia Kampadena Parish Chapel",
         "Παρεκκλήσι Παναγίας Καμπαδένας", "kampadena",
         "Παναγία Καμπαδένα"),
        ("panagia-myrtidiotissa-chapel",
         "Panagia Myrtidiotissa Parish Chapel",
         "Παρεκκλήσι Παναγίας Μυρτιδιώτισσας", "myrtidiotissa",
         "Παναγία Μυρτιδιώτισσα"),
        ("panagia-grigorousa-chapel", "Panagia Grigorousa Parish Chapel",
         "Παρεκκλήσι Παναγίας Γρηγορούσας", "grigorousa",
         "Παναγία Γρηγορούσα"),
    )
    for key, name, local, source_key, marker in chapel_rows:
        index = len(rows) + 1
        url = KALYVITES_CHAPELS[source_key]
        row = exact_row(
            index, key, "parish", "Parish Chapel", name, local,
            "Mytilene", "Mytilene 81100", "KAL", markers=marker
        )
        row["sources"] = [url]
        rows.append(row)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 83
EXPECTED_OWNER_COUNTS = {PARENT: 83}
EXPECTED_KINDS = {"monastery": 5, "parish": 78}
EXPECTED_RANKS = {
    "Monastery": 4,
    "Monastery Metochion": 1,
    "Parish Chapel": 4,
    "Parish Church": 72,
    "Pilgrimage Church": 2,
}
EXPECTED_CONTACT_BODIES = 8
EXPECTED_PHONE_BODIES = 8
EXPECTED_PHONE_VALUES = 10
EXPECTED_EMAIL_BODIES = 2
EXPECTED_EMAIL_VALUES = 2
EXPECTED_SITE_BODIES = 2
EXPECTED_ADDRESS_BODIES = 83
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "ec-patr.org",
    "kalivitis-mitilini.gr",
    "www.visitgreece.gr",
    "ieramoni-agiou-rafail.gr",
}
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
    if parsed.scheme != "https" or parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


def clean(source):
    item = {key: value for key, value in source.items()
            if value not in (None, "", [])}
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must carry one to three sources" % item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    contact_sources = list(item.get("contact_sources") or [])
    if item.get("phones") or item.get("emails"):
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks current contact provenance" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
        if source_url not in sources:
            raise ValueError("contact source is outside identity sources")
    site = item.get("site")
    if site:
        validate_url(site, item.get("id"))
        source_hosts = {urlparse(value).netloc for value in sources}
        if urlparse(site).netloc not in source_hosts:
            raise ValueError("%s site host lacks an identity source" % item.get("id"))
    item.pop("live_markers", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Mytilene candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Mytilene candidate ledger date drifted")
    expected_summary = {
        PARENT: 83,
        "total": 83,
        "regulated_parish_rows": 72,
        "parish_kind_rows": 78,
        "monastery_kind_rows": 5,
        "contact_bodies": 8,
        "phone_bodies": 8,
        "public_phone_values": 10,
        "email_bodies": 2,
        "public_email_values": 2,
        "body_owned_sites": 2,
        "address_bodies": 83,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Mytilene ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Mytilene ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Mytilene ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Mytilene ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Mytilene ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
    signatures = {}
    ranks = Counter()
    kinds = Counter()
    owners = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in ids or row_id in EXISTING_PARENTS:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has the wrong parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has the wrong country" % row_id)
        if item.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if item.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.fullmatch(email):
                raise ValueError("%s carries an invalid email" % row_id)
        signature = (item["parent"], unicase(item["local"]),
                     unicase(item["seat"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s" %
                             (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        owners[item["parent"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Mytilene English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Mytilene rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Mytilene kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Mytilene parent totals drifted")
    coverage = (
        sum(bool(x.get("phones") or x.get("emails") or x.get("site"))
            for x in result),
        sum(bool(x.get("phones")) for x in result),
        sum(len(x.get("phones") or []) for x in result),
        sum(bool(x.get("emails")) for x in result),
        sum(len(x.get("emails") or []) for x in result),
        sum(bool(x.get("site")) for x in result),
        sum(bool(x.get("address")) for x in result),
    )
    expected = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected:
        raise ValueError("Mytilene contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request_url = url
    if url == VISIT_GREECE:
        request_url += "?audit=plithos"
    request = Request(request_url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Cache-Control": "no-cache",
    })
    try:
        with urlopen(request, timeout=60) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type", "").lower()
    except HTTPError as exc:
        if url == RAPHAEL_SITE and exc.code == 403:
            return b"", "http-403"
        raise
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = unicase(text)
    return re.sub(r"\s+", " ", text)


def compact_digits(value):
    return re.sub(r"\D", "", value)


def check_live_sources():
    required = {url for row in ROWS for url in row.get("sources", [])}
    cache = {}
    for url in sorted(required):
        payload, content_type = fetch(url)
        if url == RAPHAEL_SITE and content_type == "http-403":
            cache[url] = ""
            continue
        if url.lower().endswith(".pdf"):
            if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                raise ValueError("live source is not a PDF: %s" % url)
            cache[url] = payload
            continue
        if "html" not in content_type and not payload.lstrip().startswith(b"<"):
            raise ValueError("live source is not HTML: %s" % url)
        cache[url] = normalized_page(payload)

    ep = cache[PATRIARCHATE_PAGE]
    for marker in ("Ἐνοριακοί Ναοί 72", "Παναγίας Δαμανδρίου",
                   "Προφ. Ἠλιού", "Ἅγιος Γεώργιος Μελαντᾶ"):
        if unicase(marker) not in ep:
            raise ValueError("Patriarchate page lacks marker: %s" % marker)
    cog = cache[CHURCH_OF_GREECE_PAGE]
    for marker in ("Αγ. Νικολάου Αμπελικού", "22520-91.042"):
        if unicase(marker) not in cog:
            raise ValueError("Church of Greece page lacks marker: %s" % marker)
    kal = cache[KALYVITES_CONTACT]
    for marker in ("Αγ. Ιωάννης Καλυβίτης", "2251022391",
                   "6948527881", "info@kalivitis-mitilini.gr"):
        if unicase(marker) not in kal:
            raise ValueError("Kalyvites page lacks marker: %s" % marker)
    visit = cache[VISIT_GREECE]
    for marker in ("2251071708", "contact@ieramoni-agiou-rafail.gr",
                   "2252022242", "2253056259", "2253053239"):
        if unicase(marker) not in visit:
            raise ValueError("Visit Greece page lacks marker: %s" % marker)

    for row in ROWS:
        contact_sources = row.get("contact_sources") or []
        if not contact_sources:
            continue
        pages = " ".join(
            cache[url] for url in contact_sources
            if isinstance(cache[url], str)
        )
        digit_pages = compact_digits(pages)
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digit_pages:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
        for email in row.get("emails") or []:
            if unicase(email) not in pages:
                raise ValueError("%s lacks live email %s" %
                                 (row["id"], email))
    print("Mytilene live sources: %d URLs checked" % len(required))


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.check_live:
        check_live_sources()
    elif args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Mytilene: 83 exact bodies; 72 parishes, 2 pilgrimage "
              "churches, 4 monasteries, 1 metochion, and 4 chapels")
        print("Contacts: 8 bodies; 10 phones; 2 emails; 2 body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Mytilene: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
