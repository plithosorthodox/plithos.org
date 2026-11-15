#!/usr/bin/env python3
"""Validate exact named Mithymna worship bodies from official sources.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_mithymna_country.py --check
    python tools/directory_mithymna_country.py --check-live
    python tools/directory_mithymna_country.py --dump
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "ep-mithymna"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "mithymna_country.json"
)

LEGAL_2019 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/"
    "2019_avgoustos_septembrios.pdf"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-mithimnis/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/methymnes"
)
TAXIARCHS_SITE = "https://www.taxiarhismantamadou.gr/"
TAXIARCHS_CONTACT = "https://www.taxiarhismantamadou.gr/epikoinonia"
SAINT_BASIL_SOURCE = (
    "https://www.taxiarhismantamadou.gr/announcement/"
    "eorte-tes-upsoseos-tou-timioy-kai-zoopoiou-stayrou-14-9-2026"
)
FORERUNNER_SOURCE = (
    "https://www.taxiarhismantamadou.gr/announcement/"
    "iera-panigyris-tes-anamnisis-tes-apotomes-tis-timias-kefales-"
    "tou-agioy-endoxoy-3"
)
SAINT_STEPHEN_SOURCE = (
    "https://www.taxiarhismantamadou.gr/announcement/"
    "th-leitoyrgia-ieras-panigyreos-agioy-stefanoy-02-08-2026"
)
TRICHEROUSA_SOURCE = (
    "https://www.taxiarhismantamadou.gr/announcement/"
    "eorte-tes-timias-zonis-31-8-2025"
)
SAINT_CHARALAMBOS_SOURCE = (
    "https://www.taxiarhismantamadou.gr/announcement/"
    "th-leitoyrgia-ieras-panigyreos-agioy-haralampoys-halikas-27-07-2025"
)
SAINT_NEKTARIOS_SOURCE = (
    "https://www.taxiarhismantamadou.gr/announcement/"
    "eorte-tou-agioy-nektarioy-9-11-2023"
)

SOURCES = {
    "L19": LEGAL_2019,
    "EP": PATRIARCHATE_PAGE,
    "COG": CHURCH_OF_GREECE_PAGE,
    "TAX": TAXIARCHS_CONTACT,
    "BASIL": SAINT_BASIL_SOURCE,
    "FORERUNNER": FORERUNNER_SOURCE,
    "STEPHEN": SAINT_STEPHEN_SOURCE,
    "TRICHEROUSA": TRICHEROUSA_SOURCE,
    "CHARALAMBOS": SAINT_CHARALAMBOS_SOURCE,
    "NEKTARIOS": SAINT_NEKTARIOS_SOURCE,
}


# Exact table order from Regulation 2167/1624/2019.
# English seat|Greek seat|English dedication|Greek dedication
PARISH_SOURCE = r'''
Kalloni|Καλλονή|Life-Giving Spring|Ζωοδόχου Πηγής
Kalloni|Καλλονή|Saint John the Forerunner|Αγίου Ιωάννου Προδρόμου
Kalloni|Καλλονή|Saint Nektarios|Αγίου Νεκταρίου
Agia Paraskevi|Αγία Παρασκευή|Holy Archangels|Παμμεγίστων Ταξιαρχών
Anemotia|Ανεμώτια|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος
Antissa|Άντισσα|Saint John the Theologian|Αγίου Ιωάννου Θεολόγου
Arisvi|Αρίσβη|Holy Unmercenaries|Αγίων Αναργύρων
Vatousa|Βατούσα|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Dafia|Δάφια|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Keramio|Κεράμιο|Saint George|Αγίου Γεωργίου
Napi|Νάπη|Saint John the Theologian|Αγίου Ιωάννου Θεολόγου
Papiana|Παπιανά|Saint Nicholas|Αγίου Νικολάου
Parakoila|Παράκοιλα|Holy Archangels|Παμμεγίστων Ταξιαρχών
Pterounta|Πτερούντα|Saint John the Theologian|Αγίου Ιωάννου Θεολόγου
Revma|Ρεύμα|Saint John the Forerunner|Αγίου Ιωάννου Προδρόμου
Skala Kallonis|Σκάλα Καλλονής|Saint Anna|Αγίας Άννας
Skalochori|Σκαλοχώρι|Saint George|Αγίου Γεωργίου
Filia|Φίλια|Holy Archangels|Παμμεγίστων Ταξιαρχών
Chidira|Χίδηρα|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Mithymna|Μήθυμνα|Saint Panteleimon|Αγίου Παντελεήμονος
Mithymna|Μήθυμνα|Holy Archangels|Παμμεγίστων Ταξιαρχών
Mithymna|Μήθυμνα|Saint Kyriaki|Αγίας Κυριακής
Vafeios|Βαφειός|Saint Paraskevi|Αγίας Παρασκευής
Lafiona|Λαφιώνα|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Petra|Πέτρα|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Petrion|Πετρίον|Saint Kyriaki|Αγίας Κυριακής
Skoutaros|Σκουτάρος|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Mantamados|Μανταμάδος|Holy Archangels|Παμμεγίστων Ταξιαρχών
Argennos|Άργεννος|Saint George|Αγίου Γεωργίου
Kapi|Κάπη|Saint George|Αγίου Γεωργίου
Kleio|Κλειώ|Holy Trinity|Αγίας Τριάδος
Lepetymnos|Λεπέτυμνος|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Pelopi|Πελόπη|Holy Archangels|Παμμεγίστων Ταξιαρχών
Skala Sykamineas|Σκάλα Συκαμινέας|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου
Stypsi|Στύψη|Holy Trinity|Αγίας Τριάδος
Sykaminea|Συκαμινέα|Saint Photini|Αγίας Φωτεινής
Ypsilometopo|Υψηλομέτωπο|Holy Archangels|Παμμεγίστων Ταξιαρχών
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


def parish_row(index, raw):
    seat, greek_seat, dedication, greek_dedication = raw.split("|", 3)
    name = "Parish Church of %s, %s" % (dedication, seat)
    rank = "Parish Church"
    sources = [LEGAL_2019]
    row = {
        "id": "gr-ep-mithymna-%03d-%s" % (index, slug(name)),
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": "Ιερός Ναός %s, %s" % (greek_dedication, greek_seat),
        "seat": seat,
        "country": "GR",
        "address": [seat, "Lesvos", "Greece"],
        "sources": sources,
    }
    if dedication == "Dormition of the Theotokos" and seat == "Petra":
        row["rank"] = "Pilgrimage Parish Church"
        row["name"] = (
            "Dormition of the Theotokos Pilgrimage Parish Church, Petra"
        )
        row["local"] = (
            "Ιερός Προσκυνηματικός Ναός Κοιμήσεως της Θεοτόκου, Πέτρα"
        )
        row["sources"] = [LEGAL_2019, PATRIARCHATE_PAGE]
        row["live_markers"] = ["Κοιμήσεως τῆς Θεοτόκου ἐν Πέτρᾳ"]
    if dedication == "Holy Archangels" and seat == "Mantamados":
        row.update({
            "rank": "Pilgrimage Parish Church",
            "name": "Holy Archangels Pilgrimage Parish Church, Mantamados",
            "local": (
                "Ιερός Προσκυνηματικός Ναός Παμμεγίστων Ταξιαρχών "
                "Μανταμάδου"
            ),
            "address": ["Mantamados 81104", "Lesvos", "Greece"],
            "phones": [
                "22530-61214",
                "22530-61221",
                "22530-61218",
                "22530-61923",
                "22530-61359",
            ],
            "emails": ["info@taxiarhismantamadou.gr"],
            "site": TAXIARCHS_SITE,
            "sources": [LEGAL_2019, PATRIARCHATE_PAGE, TAXIARCHS_CONTACT],
            "contact_sources": [TAXIARCHS_CONTACT],
            "contact_checked": CHECKED,
            "live_markers": [
                "ΙΕΡΟΣ ΠΡΟΣΚΥΝΗΜΑΤΙΚΟΣ ΝΑΟΣ",
                "22530 61214",
                "22530 61221",
                "22530 61218",
                "22530 61923",
                "22530 61359",
                "info@taxiarhismantamadou.gr",
            ],
        })
    if dedication == "Holy Trinity" and seat == "Stypsi":
        row.update({
            "phones": ["22530-91270"],
            "address": ["Stypsi 81109", "Lesvos", "Greece"],
            "sources": [LEGAL_2019, CHURCH_OF_GREECE_PAGE],
            "contact_sources": [CHURCH_OF_GREECE_PAGE],
            "contact_checked": CHECKED,
            "live_markers": ["Αγίας Τριάδος Στύψης", "22530-91.270"],
        })
    return row


def exact_row(index, key, kind, rank, name, local, seat, address,
              source_tokens, phones="", emails="", site="",
              contact_tokens="", markers=""):
    row = {
        "id": "gr-ep-mithymna-%03d-%s" % (index, key),
        "parent": PARENT,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "GR",
        "address": [address, "Lesvos", "Greece"],
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
    current = PARISH_SOURCE.strip().splitlines()
    if len(current) != 37:
        raise ValueError("expected 37 exact legal parish rows")
    rows = [parish_row(index, raw)
            for index, raw in enumerate(current, start=1)]
    rows.extend([
        exact_row(
            38, "leimonos-monastery", "monastery", "Monastery",
            "Patriarchal and Stavropegic Leimonos Monastery, Kalloni",
            "Ιερά Πατριαρχική και Σταυροπηγιακή Μονή Λειμώνος",
            "Kalloni", "Kalloni 81107", "EP,COG",
            phones="22530-22289", contact_tokens="COG",
            markers="Μονή Λειμῶνος,22530-22289"
        ),
        exact_row(
            39, "myrsiniotissa-monastery", "monastery", "Monastery",
            "Myrsiniotissa Monastery, Kalloni",
            "Ιερά Μονή Μυρσινιωτίσσης", "Kalloni", "Kalloni 81107",
            "EP,COG", phones="22530-22729", contact_tokens="COG",
            markers="Μυρσινιωτίσσης,22530-22729"
        ),
        exact_row(
            40, "perivoli-monastery", "monastery", "Monastery",
            "Perivoli Monastery, Antissa", "Ιερά Μονή Περιβολής",
            "Antissa", "Antissa 81103", "EP,COG",
            phones="22530-56249", contact_tokens="COG",
            markers="Περιβολῆς,22530-56249"
        ),
        exact_row(
            41, "saint-basil-mantamados", "parish", "Church",
            "Saint Basil Church, Mantamados",
            "Ιερός Ναός Αγίου Βασιλείου, Μανταμάδος",
            "Mantamados", "Mantamados", "BASIL,EP",
            markers="Ἱερὸ Ναὸ Ἁγίου Βασιλείου"
        ),
        exact_row(
            42, "forerunner-platania", "parish", "Country Church",
            "Saint John the Forerunner Country Church, Platania",
            "Εξωκκλήσιο Τιμίου Προδρόμου, Πλατάνια Μανταμάδου",
            "Platania, Mantamados", "Platania, Mantamados",
            "FORERUNNER,EP", markers="ἐξωκκλήσιο,Πλατάνια"
        ),
        exact_row(
            43, "saint-stephen-mantamados", "parish", "Country Church",
            "Saint Stephen Country Church, Mantamados",
            "Παλαιοχριστιανικό Εξωκκλήσιο Αγίου Στεφάνου, Μανταμάδος",
            "Mantamados", "Saint Stephen area, Mantamados",
            "STEPHEN,EP", markers="παλαιοχριστιανικοῦ,Ἁγίου Στεφάνου"
        ),
        exact_row(
            44, "panagia-tricherousa-skidia", "parish", "Country Church",
            "Panagia Tricherousa Country Church, Skidia",
            "Εξωκκλήσιο Παναγίας Τριχερούσης, Σκίδια Μανταμάδου",
            "Skidia, Mantamados", "Skidia, Mantamados",
            "TRICHEROUSA,EP", markers="Τριχερούσης,Σκίδια"
        ),
        exact_row(
            45, "saint-charalambos-chalika", "parish", "Country Church",
            "Saint Charalambos Country Church, Chalika",
            "Εξωκκλήσιο Αγίου Χαραλάμπους, Χαλίκα Μανταμάδου",
            "Chalika, Mantamados", "Chalika, Mantamados",
            "CHARALAMBOS,EP", markers="Ἁγίου Χαραλάμπους,Χαλίκα"
        ),
        exact_row(
            46, "saint-nektarios-mantamados", "parish", "Country Church",
            "Saint Nektarios Country Church, Mantamados",
            "Εξωκκλήσιο Αγίου Νεκταρίου, Μανταμάδος",
            "Mantamados", "Mantamados", "NEKTARIOS,EP",
            markers="Ἁγίου Νεκταρίου,ἐξωκκλήσιο,Μανταμάδου"
        ),
    ])
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 46
EXPECTED_OWNER_COUNTS = {PARENT: 46}
EXPECTED_KINDS = {"monastery": 3, "parish": 43}
EXPECTED_RANKS = {
    "Church": 1,
    "Country Church": 5,
    "Monastery": 3,
    "Parish Church": 35,
    "Pilgrimage Parish Church": 2,
}
EXPECTED_CONTACT_BODIES = 5
EXPECTED_PHONE_BODIES = 5
EXPECTED_PHONE_VALUES = 9
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 46
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "ec-patr.org",
    "www.taxiarhismantamadou.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PERSON_KEYS = {
    "abbess",
    "abbot",
    "bishop",
    "clergy",
    "clergy_name",
    "contact_name",
    "person",
    "rector",
}
PERSON_NAME_RE = re.compile(
    r"\b(?:Metropolitan|Bishop|Archbishop|Abbot|Abbess|Archpriest|"
    r"Priest|Deacon|Rector)\s+[A-Z][A-Za-z'-]+"
)


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def reject_person_fields(value, label):
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).casefold() in PERSON_KEYS:
                raise ValueError("%s contains a personal-name field" % label)
            reject_person_fields(item, label)
    elif isinstance(value, list):
        for item in value:
            reject_person_fields(item, label)


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
        raise ValueError("Mithymna candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Mithymna candidate ledger date drifted")
    expected_summary = {
        PARENT: 46,
        "total": 46,
        "legal_parish_rows": 37,
        "parish_kind_rows": 43,
        "monastery_kind_rows": 3,
        "current_exact_dependent_worship_rows": 6,
        "contact_bodies": 5,
        "phone_bodies": 5,
        "public_phone_values": 9,
        "email_bodies": 1,
        "public_email_values": 1,
        "body_owned_sites": 1,
        "address_bodies": 46,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Mithymna ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Mithymna ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Mithymna ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Mithymna ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Mithymna ledger has forbidden punctuation")
    reject_person_fields(ledger, "Mithymna ledger")
    if PERSON_NAME_RE.search(rendered):
        raise ValueError("Mithymna ledger contains a clergy name")
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
        reject_person_fields(item, row_id)
        if PERSON_NAME_RE.search(json.dumps(item, ensure_ascii=False)):
            raise ValueError("%s contains a clergy name" % row_id)
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
        raise ValueError("Mithymna English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Mithymna rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Mithymna kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Mithymna parent totals drifted")
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
        raise ValueError("Mithymna contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Cache-Control": "no-cache",
    })
    with urlopen(request, timeout=60) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
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
    required.add(TAXIARCHS_SITE)
    cache = {}
    for url in sorted(required):
        payload, content_type = fetch(url)
        if url.lower().endswith(".pdf"):
            if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                raise ValueError("live source is not a PDF: %s" % url)
            cache[url] = payload
            continue
        if "html" not in content_type and not payload.lstrip().startswith(b"<"):
            raise ValueError("live source is not HTML: %s" % url)
        cache[url] = normalized_page(payload)

    ep = cache[PATRIARCHATE_PAGE]
    for marker in ("Ἐνοριακοί Ναοί 37", "Παρεκκλήσια 60",
                   "Ἐξωκκλήσια 300", "Μοναστηριακοί Ναοί 4",
                   "Μονή Λειμῶνος", "Μυρσινιωτίσσης", "Περιβολῆς",
                   "Ταξιαρχῶν, ἐν Μανταμάδῳ", "Θεοτόκου ἐν Πέτρᾳ"):
        if unicase(marker) not in ep:
            raise ValueError("Patriarchate page lacks marker: %s" % marker)
    cog = cache[CHURCH_OF_GREECE_PAGE]
    for marker in ("Αγίας Τριάδος Στύψης", "22530-91.270",
                   "22530-22289", "22530-22729", "22530-56249"):
        if unicase(marker) not in cog:
            raise ValueError("Church of Greece page lacks marker: %s" % marker)
    tax = cache[TAXIARCHS_CONTACT]
    for marker in ("ΙΕΡΟΣ ΠΡΟΣΚΥΝΗΜΑΤΙΚΟΣ ΝΑΟΣ", "22530 61214",
                   "22530 61221", "22530 61218", "22530 61923",
                   "22530 61359", "info@taxiarhismantamadou.gr"):
        if unicase(marker) not in tax:
            raise ValueError("Mantamados contact page lacks marker: %s" % marker)

    for row in ROWS:
        string_pages = " ".join(
            cache[url] for url in row.get("sources", [])
            if isinstance(cache[url], str)
        )
        for marker in row.get("live_markers") or []:
            if unicase(marker) not in string_pages:
                raise ValueError("%s lacks live marker %s" %
                                 (row["id"], marker))
        contact_sources = row.get("contact_sources") or []
        if not contact_sources:
            continue
        pages = " ".join(cache[url] for url in contact_sources)
        digit_pages = compact_digits(pages)
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digit_pages:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
        for email in row.get("emails") or []:
            if unicase(email) not in pages:
                raise ValueError("%s lacks live email %s" %
                                 (row["id"], email))
    print("Mithymna live sources: %d URLs checked" % len(required))


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
        print("Mithymna: 46 exact bodies; 37 legal parishes, 3 monasteries, "
              "1 church, and 5 country churches")
        print("Contacts: 5 bodies; 9 phones; 1 email; 1 body site")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Mithymna: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
