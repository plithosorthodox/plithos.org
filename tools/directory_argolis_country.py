#!/usr/bin/env python3
"""Build the exact current Argolis body roster."""

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


PARENT = "gr-argolis"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "argolis_country.json"

LOCAL_BASE = "https://www.imargolidos.gr"
PARISH_URL = LOCAL_BASE + "/%CE%B9%CE%B5%CF%81%CE%BF%CE%AF-%CE%BD%CE%B1%CE%BF%CE%AF/"
MONASTERY_URL = LOCAL_BASE + "/%CE%B9%CE%B5%CF%81%CE%AD%CF%82-%CE%BC%CE%BF%CE%BD%CE%AD%CF%82/"
ADMIN_URL = LOCAL_BASE + "/%CE%B4%CE%B9%CE%BF%CE%AF%CE%BA%CE%B7%CF%83%CE%B7-%CF%85%CF%80%CE%B7%CF%81%CE%B5%CF%83%CE%AF%CE%B5%CF%82/"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2019_january.pdf"


PARISH_SOURCE = r"""
Nafplio|Ναύπλιον|Saint George|Άγιος Γεώργιος|+30 27520-28028
Nafplio|Ναύπλιον|Nativity of the Theotokos|Γενέσιον Θεοτόκου|+30 27520-24166
Nafplio|Ναύπλιον|Saint Nicholas|Άγιος Νικόλαος|+30 27520-23552
Nafplio|Ναύπλιον|Holy Trinity|Αγία Τριάς|+30 27520-24915
Nafplio|Ναύπλιον|Annunciation of the Theotokos|Ευαγγελίστρια|+30 27520-27778
Nafplio|Ναύπλιον|Saints Constantine and Helen|Άγ. Κωνσταντίνος-Ελένη|+30 27520-25100
Aria|Άρεια|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Lefkakia|Λευκάκια|Meeting of the Lord|Υπαπαντής Χριστού|+30 27520-61740
Pyrgiotika|Πυργιώτικα|Saint George|Άγιος Γεώργιος|
Argos|Άργος|Saint Peter|Άγιος Πέτρος|+30 27510-67572
Argos|Άργος|Saint Basil|Άγιος Βασίλειος|+30 27510-67571
Argos|Άργος|Saint Nicholas|Άγιος Νικόλαος|+30 27510-68337
Argos|Άργος|Dormition of the Theotokos|Κοίμησις Θεοτόκου|+30 27510-67372
Argos|Άργος|Saint John the Forerunner|Τίμιος Πρόδρομος|+30 27510-68420
Elliniko|Ελληνικό|Saint George|Άγιος Γεώργιος|+30 27510-21535
Kefalari|Κεφαλάρι|Life-giving Spring|Ζωοδόχος Πηγή|+30 27510-86478
Dalamanara|Δαλαμανάρα|Life-giving Spring|Ζωοδόχος Πηγή|+30 27510-67737
Ira|Ήρα|Saint George|Άγιος Γεώργιος|+30 27510-31575
Inachos|Ίναχος|Saint Demetrius|Άγιος Δημήτριος|+30 27510-31119
Kourtaki|Κουρτάκι|Saint Athanasius|Άγιος Αθανάσιος|
Laloukas|Λάλουκας|Saint Barbara|Αγία Βαρβάρα|
Agios Dimitrios|Άγιος Δημήτριος|Saint Nicholas|Άγιος Νικόλαος|+30 27520-26576
Arachnaio|Αραχναίο|Saint Athanasius|Άγιος Αθανάσιος|
Argoliko|Αργολικό|Dormition of the Theotokos|Κοίμησις Θεοτόκου|+30 27520-43985
Agia Triada|Αγία Τριάς|Holy Trinity|Αγία Τριάς|+30 27520-44610
Anyfi|Ανυφί|Saint Demetrius|Άγιος Δημήτριος|+30 27520-44024
Iraio|Ηραίον|Saint Nicholas|Άγιος Νικόλαος|
Manesi|Μάνεσι|Saints Constantine and Helen|Άγ. Κωνσταντίνος-Ελένη|
Midea|Μιδέα|Saint John the Forerunner|Τίμιος Πρόδρομος|+30 27520-43148
Panariti|Παναρήτι|Nativity of the Theotokos|Γενέσιον Θεοτόκου|+30 27520-43227
Poulakida|Πουλακίδα|Saint Demetrius|Άγιος Δημήτριος|+30 27520-43078
Agios Adrianos|Άγιος Αδριανός|Saint Nicholas|Άγιος Νικόλαος|+30 27510-89290
Asini|Ασίνη|Saint Demetrius|Άγιος Δημήτριος|+30 27520-61329
Drepano|Δρέπανο|Saints Adrian and Natalia|Άγ. Αδριανός-Ναταλία|+30 27520-92315
Iria|Ίρια|Dormition of the Theotokos|Κοίμησις Θεοτόκου|+30 27520-94261
Neo Roino|Νέο Ροϊνό|Saint Marina|Αγία Μαρίνα|+30 27520-24783
Nea Tiryntha|Νέα Τίρυνθα|Holy Cincture of the Theotokos|Τιμία Ζώνη|+30 27520-36262
Tolo|Τολό|Saints Constantine and Helen|Άγ. Κωνσταντίνος-Ελένη|+30 27520-59938
Tsello|Τσέλλο|Saint Paraskevi|Αγία Παρασκευή|
Achladokampos|Αχλαδόκαμπος|Saint Demetrius|Άγιος Δημήτριος|+30 27510-81470
Karya|Καρυά|Saint John the Forerunner|Τίμιος Πρόδρομος|
Kiveri|Κιβέρι|Saint John the Forerunner|Τίμιος Πρόδρομος|+30 27510-47870
Myloi|Μύλοι|Holy Apostles|Άγιοι Απόστολοι|+30 27510-47410
Nea Kios|Νέα Κίος|Theomana|Θεομάνα|+30 27510-51691
Skafidaki|Σκαφιδάκι|Saint Marina|Αγία Μαρίνα|
Tourniki|Τουρνίκι|Saint Athanasius|Άγιος Αθανάσιος|
Chouni|Χούνη|Transfiguration of the Savior|Μεταμ. Σωτήρος|
Vrousti|Βρούστι|Saint Athanasius|Άγιος Αθανάσιος|
Limnes|Λίμνες|Meeting of the Lord|Υπαπαντή Χριστού|+30 27510-83331
Mborsia|Μπόρσια|Holy Archangels|Παμμ. Ταξιάρχαι|
Mykines|Μυκήνες|Saint Panteleimon|Άγιος Παντελεήμων|+30 27510-47528
Prosymni|Προσύμνη|Saint Catherine|Αγία Αικατερίνη|+30 27510-89309
Fichtia|Φίχτια|Annunciation of the Theotokos|Ευαγγελισμός Θεοτόκου|
Neo Iraio|Νέο Ηραίον|Dormition of the Theotokos|Κοίμησις Θεοτόκου|+30 27510-21195
Pyrgella|Πυργέλλα|Saint Nicholas|Άγιος Νικόλαος|+30 27510-20901
Adami|Αδάμι|Saint Demetrius|Άγιος Δημήτριος|+30 27530-22795
Arkadiko|Αρκαδικό|Dormition of the Theotokos|Κοίμησις Θεοτόκου|+30 27530-31750
Ancient Epidaurus|Αρχαία Επίδαυρος|Saint Nicholas|Άγιος Νικόλαος|+30 27530-41452
Giannouleika|Γιαννουλέικα|Saint George|Άγιος Γεώργιος|+30 27530-31186
Dimaina|Δήμαινα|Saints Constantine and Helen|Άγ. Κωνσταντίνος-Ελένη|
Lygourio|Λυγουριό|Holy Trinity|Αγία Τριάς|+30 27530-22689
Nea Epidaurus|Νέα Επίδαυρος|Annunciation of the Theotokos|Ευαγγελισμός Θεοτόκου|+30 27530-31500
Agios Nikolaos|Άγιος Νικόλαος|Saint Nicholas|Άγιος Νικόλαος|
Alea|Αλέα|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Gymno|Γυμνό|Holy Trinity|Αγία Τριάς|
Exochi|Εξοχή|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Kapareli|Καπαρέλι|Saint John the Forerunner|Τίμιος Πρόδρομος|+30 27510-71414
Kefalovryso|Κεφαλόβρυσο|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Lyrkeia|Λυρκεία|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Sterna|Στέρνα|Holy Trinity|Αγία Τριάς|
Koutsopodi|Κουτσοπόδι|Saint Kyriaki|Αγία Κυριακή|
Koutsopodi|Κουτσοπόδι|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Malantreni|Μαλαντρένι|Saint Athanasius|Άγιος Αθανάσιος|
Neochori|Νεοχώρι|Saint George|Άγιος Γεώργιος|
Skoteini|Σκοτεινή|Dormition of the Theotokos|Κοίμησις Θεοτόκου|
Stathaika|Σταθαΐικα|Saint John the Theologian|Άγ. Ιωάννης Θεολόγος|
Schoinochori|Σχοινοχώρι|Saint Demetrius|Άγιος Δημήτριος|
Frousiona|Φρουσιούνα|Saint John the Forerunner|Τίμιος Πρόδρομος|
"""


PILGRIMAGE_SOURCE = [
    ("anastasios-nafplio", "Saint Anastasios Pilgrimage Church", "Ιερός Προσκυνηματικός Ναός Αγίου Αναστασίου", "Nafplio", "Ναύπλιον", "+30 27520-23095"),
    ("catherine-argos", "Saint Catherine Pilgrimage Church", "Ιερός Προσκυνηματικός Ναός Αγίας Αικατερίνης", "Argos", "Άργος", "+30 27510-68153"),
    ("ignatius-zogka", "Saint Ignatius Pilgrimage Church", "Ιερός Προσκυνηματικός Ναός Αγίου Ιγνατίου", "Zogka of Elliniko, Argos", "Ζόγκας Ελληνικού Άργους", "+30 27510-86016"),
]


MONASTERY_SOURCE = [
    ("photini", "Saint Photini the Samaritan Woman Monastery", "Ιερά Μονή Αγίας Φωτεινής Σαμαρείτιδος", "Nafplio", "Λόφος Ευαγγελιστρίας, Τ.Κ. 21100 Ναύπλιο", "+30 27520-28733", "Monastery"),
    ("akathist", "Panagia of the Akathist Hymn Hesychasterion", "Ιερόν Ησυχαστήριον Παναγίας του Ακαθίστου Ύμνου", "Achladokampos", "Τ.Κ. 21057 Αχλαδόκαμπος", "+30 6947-203885", "Hesychasterion"),
    ("theodosius", "Venerable Theodosius Monastery", "Ιερά Μονή Οσίου Θεοδοσίου", "Agia Triada", "Τ.Κ. 21055 Αγία Τριάς", "+30 27520-44240", "Monastery"),
    ("archangels", "Holy Archangels Monastery", "Ιερά Μονή Παμμεγίστων Ταξιαρχών", "Nea Epidaurus", "Τ.Κ. 21054 Νέα Επίδαυρος", "+30 27530-31142", "Monastery"),
    ("demetrius-karakala", "Saint Demetrius Karakala Monastery", "Ιερά Μονή Αγίου Δημητρίου Καρακαλά", "Agios Adrianos", "Τ.Κ. 21100 Άγιος Αδριανός", "+30 27520-91196", "Monastery"),
    ("dormition-kalamiou", "Dormition of the Theotokos Kalamiou Monastery", "Ιερά Μονή Κοιμήσεως Θεοτόκου Καλαμίου", "Lygourio", "Τ.Κ. 21052 Λυγουριό", "+30 27530-22160", "Monastery"),
    ("marina", "Saint Marina Monastery", "Ιερά Μονή Αγίας Μαρίνης", "Argos", "Τ.Κ. 21200 Άργος", "+30 27510-66400", "Monastery"),
    ("forerunner", "Saint John the Forerunner Monastery", "Ιερά Μονή Τιμίου Προδρόμου", "Mborsia", "Τ.Κ. 21200 Μπόρσια", "+30 27510-76399", "Monastery"),
    ("agia-moni", "Life-giving Spring Agia Moni Hesychasterion", "Ιερόν Ησυχαστήριον Ζωοδόχου Πηγής Αγίας Μονής", "Aria, Nafplio", "Τ.Κ. 21100 Άρεια Ναυπλίου", "+30 27520-27764", "Hesychasterion"),
    ("macrina", "Saint Macrina Hesychasterion", "Ιερόν Ησυχαστήριον Αγίας Μακρίνης", "Anavalos Kiveriou", "Τ.Κ. 21200 Ανάβαλος Κιβερίου", "+30 27510-47205", "Hesychasterion"),
]


DEPENDENCY_SOURCE = [
    ("talandio", "Dormition of the Theotokos Talandio Monastery Dependency", "Μετόχιον Κοιμήσεως Θεοτόκου Ταλαντίου", "Arachnaio", "Αραχναίο"),
    ("agnountos", "Dormition of the Theotokos Agnountos Monastery Dependency", "Μετόχιον Κοιμήσεως Θεοτόκου Αγνούντος", "Nea Epidaurus", "Νέα Επίδαυρος"),
    ("polemarcha", "Panagia Polemarcha Monastery Dependency", "Μετόχιον Παναγίας «Πολεμάρχα»", "Epidaurus", "Επίδαυρος"),
]


ALLOWED_HOSTS = {
    "www.imargolidos.gr", "imargolidos.gr", "ecclesiagreece.gr", "www.ecclesiagreece.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]")


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "body"


def parse_parishes():
    rows = []
    for line in PARISH_SOURCE.strip().splitlines():
        seat, local_seat, dedication, local_dedication, phone = line.split("|")
        item = {
            "id": "gr-argolis-%03d-%s" % (len(rows) + 1, slug(seat + "-" + dedication)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Parish Church",
            "name": "%s Parish Church in %s" % (dedication, seat),
            "local": "Ιερός Ναός %s, %s" % (local_dedication, local_seat),
            "seat": seat,
            "country": "GR",
            "address": [local_seat, "Αργολίδα", "Ελλάδα"],
            "sources": [PARISH_URL, LEGAL_URL],
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [PARISH_URL]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


def build_rows():
    rows = parse_parishes()
    for key, name, local, seat, local_seat, phone in PILGRIMAGE_SOURCE:
        rows.append({
            "id": "gr-argolis-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "parish", "rank": "Pilgrimage Church",
            "name": name + " in " + seat, "local": local + ", " + local_seat,
            "seat": seat, "country": "GR", "address": [local_seat, "Αργολίδα", "Ελλάδα"],
            "phones": [phone], "sources": [PARISH_URL, LEGAL_URL],
            "contact_sources": [PARISH_URL], "contact_checked": CHECKED,
        })
    for key, name, local, seat, address, phone, rank in MONASTERY_SOURCE:
        rows.append({
            "id": "gr-argolis-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "monastery", "rank": rank,
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [address, "Αργολίδα", "Ελλάδα"], "phones": [phone],
            "sources": [MONASTERY_URL], "contact_sources": [MONASTERY_URL],
            "contact_checked": CHECKED,
        })
    for key, name, local, seat, local_seat in DEPENDENCY_SOURCE:
        rows.append({
            "id": "gr-argolis-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "monastery", "rank": "Monastery Dependency",
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [local_seat, "Αργολίδα", "Ελλάδα"], "sources": [MONASTERY_URL],
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 94
EXPECTED_OWNER_COUNTS = {PARENT: 94}
EXPECTED_KINDS = {"monastery": 13, "parish": 81}
EXPECTED_RANKS = {
    "Hesychasterion": 3,
    "Monastery": 7,
    "Monastery Dependency": 3,
    "Parish Church": 78,
    "Pilgrimage Church": 3,
}
EXISTING_PARENTS = {PARENT}


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s carries a non-competent source: %s" % (label, value))


def clean(source):
    item = {key: value for key, value in source.items() if value not in (None, "", [])}
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
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date" % item.get("id"))
    return item


def coverage_tuple(rows):
    return (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site")) for item in rows),
        sum(bool(item.get("phones")) for item in rows),
        sum(len(item.get("phones") or []) for item in rows),
        sum(bool(item.get("emails")) for item in rows),
        sum(len(item.get("emails") or []) for item in rows),
        sum(bool(item.get("site")) for item in rows),
        sum(bool(item.get("address")) for item in rows),
    )


def validate_ledger(expected_coverage=None):
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Argolis candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Argolis candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_parishes": 78,
        "current_pilgrimages": 3,
        "current_monasteries_and_hesychasteria": 10,
        "current_monastery_dependencies": 3,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Argolis ledger summary drifted at %s" % key)
    if expected_coverage:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites", "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Argolis ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Argolis ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Argolis ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Argolis candidate IDs repeat")
    return ledger


def build():
    ids = set()
    signatures = {}
    owner_counts = Counter()
    kind_counts = Counter()
    rank_counts = Counter()
    result = []
    for source in ROWS:
        item = clean(source)
        row_id = item["id"]
        if row_id in ids:
            raise ValueError("duplicate Argolis ID: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has wrong country" % row_id)
        if item.get("kind") not in ("parish", "monastery"):
            raise ValueError("%s has invalid kind" % row_id)
        for field in ("name", "local", "seat", "rank"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        rendered = json.dumps(item, ensure_ascii=False)
        if FORBIDDEN_PUNCTUATION.search(rendered):
            raise ValueError("%s carries forbidden punctuation" % row_id)
        signature = unicodedata.normalize(
            "NFKC", "%s|%s|%s" % (item["local"], item["seat"], item["rank"])
        ).casefold()
        signature = re.sub(r"\s+", " ", signature).strip()
        if signature in signatures:
            raise ValueError("%s duplicates %s" % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[item["parent"]] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Argolis English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Argolis English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Argolis parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Argolis kind totals drifted: %r" % dict(kind_counts))
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Argolis rank totals drifted: %r" % dict(rank_counts))
    coverage = coverage_tuple(result)
    validate_ledger(coverage)
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_live_source(url, allow_access_control=False):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8",
        "Connection": "close",
    })
    try:
        with urlopen(request, timeout=45) as response:
            content_type = response.headers.get("Content-Type", "").lower()
            payload = response.read()
    except HTTPError as exc:
        if allow_access_control and exc.code in (403, 520):
            return None
        raise
    if "pdf" in content_type or url.endswith(".pdf"):
        if not payload.startswith(b"%PDF") or len(payload) < 100000:
            raise ValueError("invalid PDF payload")
        return None
    if "html" not in content_type:
        raise ValueError("unexpected content type %s" % content_type)
    return payload.decode("utf-8", "replace")


def check_markers(url, markers):
    payload = fetch_live_source(url, allow_access_control=True)
    if payload is None:
        return
    text = normalize_source_text(payload)
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("live Argolis marker failed at %s: %s" % (url, marker))


def check_live_sources():
    check_markers(PARISH_URL, (
        "Άγιος Γεώργιος", "Ναύπλιον", "27520-28028", "Θεομάνα", "Νέα Κίος",
        "Κοίμησις Θεοτόκου", "Κουτσοπόδι", "Άγιος Αναστάσιος", "27520-23095",
    ))
    check_markers(MONASTERY_URL, (
        "Αγίας Φωτεινής Σαμαρείτιδος", "6947-203885", "Παμμεγίστων Ταξιαρχών",
        "Κοιμήσεως Θεοτόκου Ταλαντίου", "Παναγίας «Πολεμάρχα»", "ΔΙΑΛΕΛΥΜΕΝΕΣ ΙΕΡΕΣ ΜΟΝΕΣ",
    ))
    check_markers(ADMIN_URL, (
        "Ενοριακοί: 78", "Παρεκκλήσια: 98", "Εξωκκλήσια: 270",
        "Ναοί Κοιμητηρίων: 95", "Προσκυνηματικοί: 3", "Ιδιωτικοί Ναοί: 59",
        "Μοναστηριακοί Ναοί: 9",
    ))
    fetch_live_source(LEGAL_URL)
    build()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        check_live_sources()
        print("Argolis live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Argolis check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
