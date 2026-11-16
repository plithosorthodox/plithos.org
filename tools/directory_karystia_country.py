#!/usr/bin/env python3
"""Validate exact current Karystia and Skyros worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_karystia_country.py --check
    python tools/directory_karystia_country.py --check-live
    python tools/directory_karystia_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-karystia"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "karystia_country.json"
)
REGULATION_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2020_februarios.pdf"
)
EARLIER_LEGAL_ACT = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2015_iounios.pdf"
)
PROFILE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "karystias-kai-skyrou"
)
KARYSTOS_PARISH = "https://www.agiosnikolaoskarystos.gr/"
KARYSTOS_CEMETERY_REPAIR = (
    "https://www.agiosnikolaoskarystos.gr/2024/12/blog-post_24.html?m=0"
)
KARYSTOS_CEMETERY_CURRENT = (
    "https://www.agiosnikolaoskarystos.gr/2026/11/blog-post_01.html"
)
CHAPEL_HOME = "https://www.parekklisi.gr/"
CHAPEL_HISTORY = "https://www.parekklisi.gr/istoriko"
CHAPEL_CONTACT = "https://www.parekklisi.gr/contact"
KYMIS_METROPOLITAN = (
    "https://www.parekklisi.gr/posts/item/"
    "eorti-ag-athanasioy-polioyxoy-kymis"
)
ALIVERI_METROPOLITAN = (
    "https://www.parekklisi.gr/posts/item/eorti-osioy-loyka-en-steirio"
)

# Legal district | English seat | exact legal table identity | dedication.
PARISH_SOURCE = r'''
Kymi|Kymi|ΚΥΜΗ - ΑΓ. ΑΘΑΝΑΣΙΟΣ|Saint Athanasius
Kymi|Kymi|ΚΥΜΗ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Kymi|ΚΥΜΗ - ΠΑΜ. ΤΑΞΙΑΡΧΑΙ|Holy Archangels
Kymi|Kymi|ΚΥΜΗ - ΑΓ. ΤΡΙΑΣ|Holy Trinity
Kymi|Agios Vlasios|ΑΓΙΟΣ ΒΛΑΣΙΟΣ - ΕΙΣ. ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos
Kymi|Agios Georgios|ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Kymi|Andronianoi|ΑΝΔΡΟΝΙΑΝΟΙ - ΕΙΣ. ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos
Kymi|Ano Potamia|ΑΝΩ ΠΟΤΑΜΙΑ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Avlonari|ΑΥΛΩΝΑΡΙΟΝ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Kymi|Vitala|ΒΙΤΑΛΑ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Kymi|Vrysi|ΒΡΥΣΗ - ΑΓ. ΤΡΙΑΣ|Holy Trinity
Kymi|Dafni|ΔΑΦΝΗ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Dendra|ΔΕΝΔΡΑ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Kymi|Dirrevma|ΔΙΡΡΕΥΜΑ - ΑΓ. ΑΝΑΡΓΥΡΟΙ|Holy Unmercenaries
Kymi|Enoria|ΕΝΟΡΙΑ - ΓΕΝ. ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos
Kymi|Episkopi|ΕΠΙΣΚΟΠΗ - ΑΓ. ΑΠΟΣΤΟΛΟΙ|Holy Apostles
Kymi|Kaddi|ΚΑΔΔΙΟΝ - ΑΓ. ΔΗΜΗΤΡΙΟΣ|Saint Demetrius
Kymi|Kalimerianoi|ΚΑΛΗΜΕΡΙΑΝΟΙ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Kymi|Kipoi|ΚΗΠΟΙ - ΕΙΣ. ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos
Kymi|Koili|ΚΟΙΛΗ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Kymi|Konistres|ΚΟΝΙΣΤΡΑΙ - ΑΓ. ΤΡΙΑΣ|Holy Trinity
Kymi|Ano Kourouni|ΚΟΥΡΟΥΝΙ ΑΝΩ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Kymi|Kato Kourouni|ΚΟΥΡΟΥΝΙ ΚΑΤΩ - ΟΣ. ΣΕΡΑΦΕΙΜ|Venerable Seraphim
Kymi|Kremastos|ΚΡΕΜΑΣΤΟΣ - ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Saint John the Forerunner
Kymi|Krinianoi|ΚΡΙΝΙΑΝΟΙ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Kymi|Lofiskos|ΛΟΦΙΣΚΟΣ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Makrychori|ΜΑΚΡΥΧΩΡΙΟΝ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Manikia|ΜΑΝΙΚΙΑ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Monodri|ΜΟΝΟΔΡΙΟΝ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Oxylithos|ΟΞΥΛΙΘΟΣ - ΑΓ. ΑΘΑΝΑΣΙΟΣ|Saint Athanasius
Kymi|Oxylithos|ΟΞΥΛΙΘΟΣ - ΑΓ. ΑΝΑΡΓΥΡΟΙ|Holy Unmercenaries
Kymi|Orio|ΟΡΙΟΝ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Oktonia|ΟΚΤΩΝΙΑ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Oktonia|ΟΚΤΩΝΙΑ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Kymi|Paralia Kymis|ΠΑΡΑΛΙΑ ΚΥΜΗΣ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Kymi|Platana|ΠΛΑΤΑΝΑ - ΑΓ. ΣΟΦΙΑ|Saint Sophia
Kymi|Pyrgi|ΠΥΡΓΙ - ΑΓ. ΠΑΡΑΣΚΕΥΗ|Saint Paraskevi
Kymi|Pyrgos|ΠΥΡΓΟΣ - ΓΕΝ. ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos
Kymi|Taxiarches|ΤΑΞΙΑΡΧΑΙ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Kymi|Trachili|ΤΡΑΧΗΛΙ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Kymi|Orologio|ΩΡΟΛΟΓΙΟΝ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Aliveri|Aliveri|ΑΛΙΒΕΡΙΟΝ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Aliveri|Aliveri|ΑΛΙΒΕΡΙΟΝ - ΑΓ. ΜΑΡΙΝΑ|Saint Marina
Aliveri|Agios Loukas|ΑΓΙΟΣ ΛΟΥΚΑΣ - ΟΣ. ΛΟΥΚΑΣ|Venerable Luke
Aliveri|Agios Ioannis|ΑΓΙΟΣ ΙΩΑΝΝΗΣ - ΑΓ. ΔΗΜΗΤΡΙΟΣ|Saint Demetrius
Aliveri|Argyro|ΑΡΓΥΡΟΣ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Aliveri|Achladeri|ΑΧΛΑΔΕΡΗ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Aliveri|Velos|ΒΕΛΟΣ - ΑΓ. ΠΑΡΑΣΚΕΥΗ|Saint Paraskevi
Aliveri|Gavala|ΓΑΒΑΛΑ - ΑΓ. ΔΗΜΗΤΡΙΟΣ|Saint Demetrius
Aliveri|Dystos|ΔΥΣΤΟΣ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Aliveri|Drosia|ΔΡΟΣΙΑ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Aliveri|Zaraka|ΖΑΡΑΚΑ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Aliveri|Tharounia|ΘΑΡΡΟΥΝΙΑ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Aliveri|Karavos|ΚΑΡΑΒΟΣ - ΑΓ. ΚΩΝΣΤΑΝΤΙΝΟΣ|Saint Constantine
Aliveri|Katakalos|ΚΑΤΑΚΑΛΟΣ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Aliveri|Koskina|ΚΟΣΚΙΝΑ - ΜΕΤΑΜ. ΣΩΤΗΡΟΣ|the Transfiguration of the Savior
Aliveri|Koustoumalou|ΚΟΥΣΤΟΥΜΑΛΟΥ - ΜΕΤΑΜ. ΣΩΤΗΡΟΣ|the Transfiguration of the Savior
Aliveri|Koutoumoula|ΚΟΥΤΟΥΜΟΥΛΑ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Aliveri|Krieza|ΚΡΙΕΖΑ - ΑΓ. ΤΡΙΑΣ|Holy Trinity
Aliveri|Lepoura|ΛΕΠΟΥΡΑ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Aliveri|Neochori|ΝΕΟΧΩΡΙΟΝ - ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Saint John the Forerunner
Aliveri|Panagia|ΠΑΝΑΓΙΑ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Aliveri|Paramerites|ΠΑΡΑΜΕΡΙΤΕΣ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Aliveri|Parthenio|ΠΑΡΘΕΝΙΟΝ - ΓΕΝ. ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos
Aliveri|Perivolia|ΠΕΡΙΒΟΛΙΑ - ΕΥΑΓΓ. ΘΕΟΤΟΚΟΥ|the Annunciation of the Theotokos
Aliveri|Petries|ΠΕΤΡΙΕΣ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Aliveri|Agioi Apostoloi|ΑΓΙΟΙ ΑΠΟΣΤΟΛΟΙ - ΑΓ. ΑΠΟΣΤΟΛΟΙ|Holy Apostles
Aliveri|Kalentzi|ΚΑΛΕΝΤΖΙ - ΠΑΜΜ. ΤΑΞΙΑΡΧΑΙ|Holy Archangels
Karystos|Karystos|ΚΑΡΥΣΤΟΣ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
Karystos|Agios Dimitrios|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ - ΑΓ. ΚΩΝΣΤΑΝΤΙΝΟΣ|Saint Constantine
Karystos|Aetos|ΑΕΤΟΣ - ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos
Karystos|Almyropotamos|ΑΛΜΥΡΟΠΟΤΑΜΟΣ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Karystos|Amygdalia|ΑΜΥΓΔΑΛΙΑ - ΑΓ. ΣΠΥΡΙΔΩΝ|Saint Spyridon
Karystos|Giannitsi|ΓΙΑΝΝΙΤΣΙΟΝ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Karystos|Zoodochos Pigi|ΖΩΟΔΟΧΟΣ ΠΗΓΗ - ΖΩΟΔ. ΠΗΓΗ|the Life-Giving Spring
Karystos|Kallianoi|ΚΑΛΛΙΑΝΟΙ - ΠΑΜ. ΤΑΞΙΑΡΧΑΙ|Holy Archangels
Karystos|Kalyvia|ΚΑΛΥΒΙΑ - ΠΑΜ. ΤΑΞΙΑΡΧΑΙ|Holy Archangels
Karystos|Katsaroni|ΚΑΤΣΑΡΩΝΙΟΝ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Karystos|Kapsala|ΚΑΨΑΛΑ - ΠΑΜ. ΤΑΞΙΑΡΧΑΙ|Holy Archangels
Karystos|Komito|ΚΟΜΙΤΟΝ - ΖΩΟΔ. ΠΗΓΗ|the Life-Giving Spring
Karystos|Kouveloi|ΚΟΥΒΕΛΑΙ - ΑΓ. ΔΗΜΗΤΡΙΟΣ|Saint Demetrius
Karystos|Marmari|ΜΑΡΜΑΡΙΟΝ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Karystos|Mastrogiannaioi|ΜΑΣΤΡΟΓΙΑΝΝΑΙΟΙ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Karystos|Mesochoria|ΜΕΣΟΧΩΡΙΑ - ΑΓ. ΙΩΑΝΝΗΣ|Saint John
Karystos|Mourtia|ΜΟΥΡΤΙΑ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Karystos|Myloi|ΜΥΛΟΙ - ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Saint John the Forerunner
Karystos|Nea Styra|ΝΕΑ ΣΤΥΡΑ - ΑΓ. ΚΩΝΣΤΑΝΤΙΝΟΣ|Saint Constantine
Karystos|Paradeisi|ΠΑΡΑΔΕΙΣΙΟΝ - ΓΕΝ. ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos
Karystos|Palaia Chora|ΠΑΛΑΙΑ ΧΩΡΑ - ΜΕΤΑΜ. ΣΩΤΗΡΟΣ|the Transfiguration of the Savior
Karystos|Polypotamos|ΠΟΛΥΠΟΤΑΜΟΣ - ΑΓ. ΑΝΔΡΕΑΣ|Saint Andrew
Karystos|Stoupaioi|ΣΤΟΥΠΑΙΟΙ - ΑΓ. ΓΕΩΡΓΙΟΣ|Saint George
Karystos|Styra|ΣΤΥΡΑ - ΓΕΝ. ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos
Skyros|Skyros|ΝΗΣΟΣ ΣΚΥΡΟΣ - ΕΙΣ. ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos
Skyros|Skyros|ΝΗΣΟΣ ΣΚΥΡΟΣ - ΓΕΝ. ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos
Skyros|Skyros|ΝΗΣΟΣ ΣΚΥΡΟΣ - ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Saint John the Forerunner
Skyros|Linaria|ΛΙΝΑΡΙΑ - ΑΓ. ΝΙΚΟΛΑΟΣ|Saint Nicholas
'''

# Exact current profile identity | English name | seat | address | phone.
MONASTERY_SOURCE = r'''
Ιερά Μονή Τιμίου Προδρόμου Καρυών-Αχλαδερής|Monastery of Saint John the Forerunner at Karyes-Achladeri|Karyes-Achladeri|Karyes-Achladeri|2223041488
Ιερά Μονή Μεταμορφώσεως του Σωτήρος Κύμης|Monastery of the Transfiguration of the Savior, Kymi|Kymi|Kymi|2222022616
Ιερά Μονή Κοιμήσεως της Θεοτόκου Μάτζαρη|Monastery of the Dormition of the Theotokos at Matzari|Oxylithos|Matzari, Oxylithos|2222046100
Ιερά Μονή Αγίου Χαραλάμπους Λευκών|Monastery of Saint Charalampus at Lefkon|Avlonari|Lefkon, Avlonari|2223034242
Ιερά Μονή Αγίου Αντωνίου Αχλαδερής|Monastery of Saint Anthony at Achladeri|Achladeri|Achladeri, Avlonari|2223041998
'''

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "agiosnikolaoskarystos.gr",
    "www.agiosnikolaoskarystos.gr",
    "parekklisi.gr",
    "www.parekklisi.gr",
    "kimis-aliveriou.gr",
    "www.kimis-aliveriou.gr",
    "visit-kimi-aliveri.gr",
    "www.visit-kimi-aliveri.gr",
    "xo.gr",
    "www.xo.gr",
    "vrisko.gr",
    "www.vrisko.gr",
}
EXPECTED_TOTAL = 103
EXPECTED_REGION_COUNTS = {
    "Aliveri": 27,
    "Karystos": 24,
    "Kymi": 41,
    "Skyros": 4,
}
EXPECTED_KINDS = {"monastery": 5, "parish": 98}
EXPECTED_RANKS = {
    "Cemetery Church": 1,
    "Chapel": 1,
    "Metropolitan Church": 2,
    "Monastery": 5,
    "Parish Church": 94,
}
EXPECTED_PHONE_BODIES = 5
EXPECTED_PHONE_VALUES = 5
EXPECTED_EMAIL_BODIES = 2
EXPECTED_EMAIL_VALUES = 2
EXPECTED_SITE_BODIES = 2


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
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


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s has an unsupported URL: %s" % (label, value))


def build_rows():
    rows = []
    region_counts = Counter()
    parish_lines = PARISH_SOURCE.strip().splitlines()
    if len(parish_lines) != 96:
        raise ValueError("expected 96 legal parish source rows")
    for number, raw in enumerate(parish_lines, 1):
        region, seat, local, dedication = raw.split("|", 3)
        region_counts[region] += 1
        rank = (
            "Metropolitan Church" if number in (1, 42)
            else "Parish Church"
        )
        sources = [REGULATION_PDF]
        if number == 1:
            sources.append(KYMIS_METROPOLITAN)
        elif number == 42:
            sources.append(ALIVERI_METROPOLITAN)
        elif number == 69:
            sources.append(KARYSTOS_PARISH)
        row = {
            "id": "gr-karystia-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s of %s, %s" % (rank, dedication, seat),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": sources,
            "checked": CHECKED,
        }
        if number == 69:
            row["emails"] = ["agiosnikolaoskarystos@gmail.com"]
            row["site"] = KARYSTOS_PARISH
            row["contact_sources"] = [KARYSTOS_PARISH]
            row["contact_checked"] = CHECKED
        rows.append(row)
    if dict(sorted(region_counts.items())) != EXPECTED_REGION_COUNTS:
        raise ValueError("legal district totals drifted: %r" % region_counts)

    for number, raw in enumerate(MONASTERY_SOURCE.strip().splitlines(), 97):
        local, name, seat, address, phone = raw.split("|", 4)
        rows.append({
            "id": "gr-karystia-%03d" % number,
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "phones": [phone],
            "sources": [PROFILE],
            "checked": CHECKED,
            "contact_sources": [PROFILE],
            "contact_checked": CHECKED,
        })

    rows.append({
        "id": "gr-karystia-102",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Chapel",
        "name": (
            "Chapel of Saints Paisios, Porphyrios, and Iakovos the "
            "Forgiver, Karystos"
        ),
        "local": (
            "Ιερό Παρεκκλήσι Αγίων Παϊσίου του Αγιορείτου, Πορφυρίου "
            "του Καυσοκαλυβίτου και Ιακώβου του με Συγχωρείτε"
        ),
        "seat": "Karystos",
        "country": "GR",
        "address": [
            "Intersection toward Marmari, Lepoura-Karystos provincial road",
            "Karystos",
            "Greece",
        ],
        "emails": ["info@parekklisi3agion.gr"],
        "site": CHAPEL_HOME,
        "sources": [CHAPEL_HISTORY, CHAPEL_CONTACT],
        "checked": CHECKED,
        "contact_sources": [CHAPEL_CONTACT],
        "contact_checked": CHECKED,
    })
    rows.append({
        "id": "gr-karystia-103",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Cemetery Church",
        "name": (
            "Cemetery Church of the Nativity of Saint John the Forerunner, "
            "Karystos"
        ),
        "local": (
            "Ιερός Ναός Γενεσίου του Τιμίου Προδρόμου στο "
            "Κοιμητήριο Καρύστου"
        ),
        "seat": "Karystos",
        "country": "GR",
        "address": ["Karystos Cemetery", "Greece"],
        "sources": [KARYSTOS_CEMETERY_REPAIR, KARYSTOS_CEMETERY_CURRENT],
        "checked": CHECKED,
    })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


LIVE_CHECKS = {
    PROFILE: {
        "Τ. Προδρόμου Καρυών-Αχλαδερής",
        "Μεταμορφώσεως Σωτήρος Κύμης",
        "Κοιμήσεως Θεοτόκου Μάτζαρη",
        "Αγίου Χαραλάμπους Λευκών",
        "Αγ. Αντωνίου Αχλαδερής",
    },
    KARYSTOS_PARISH: {
        "Ιερός Ναός Αγίου Νικολάου Καρύστου",
        "agiosnikolaoskarystos@gmail.com",
    },
    KARYSTOS_CEMETERY_REPAIR: {
        "Γενέσιον του Τιμίου Προδρόμου",
        "Κοιμητήριον Καρύστου",
    },
    KARYSTOS_CEMETERY_CURRENT: {
        "Ιερό Ναό Αγίου Ιωάννου",
        "Κοιμητήριον Καρύστου",
    },
    CHAPEL_HISTORY: {
        "Ιερά Μητρόπολη Καρυστίας & Σκύρου",
        "Παϊσίου, Πορφυρίου, Ιακώβου",
    },
    CHAPEL_CONTACT: {
        "info@parekklisi3agion.gr",
        "επαρχιακής οδού Καρύστου προς Μαρμάρι",
    },
    KYMIS_METROPOLITAN: {
        "Μητροπολιτικό Ιερό Ναό του Αγίου Αθανασίου",
        "Αθανασίου Πολιούχου Κύμης",
    },
    ALIVERI_METROPOLITAN: {
        "Μητροπολιτικού Ιερού Ναού Αγίου Γεωργίου Αλιβερίου",
    },
}


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Karystia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Karystia candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "regulated_parish_rows": 96,
        "current_monastery_rows": 5,
        "current_exact_chapel_rows": 1,
        "current_exact_cemetery_rows": 1,
        "parish_kind_rows": 98,
        "monastery_kind_rows": 5,
        "contact_bodies": 7,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "public_fax_values": 0,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_TOTAL,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Karystia ledger summary drifted")
    for key in (
            "candidates", "source_reconciliations",
            "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Karystia ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Karystia ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    for source in ROWS:
        item = {
            key: value for key, value in source.items()
            if value not in (None, "", [])
        }
        row_id = item.get("id")
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") != PARENT or item.get("country") != "GR":
            raise ValueError("%s has the wrong parent or country" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(value)
               for value in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        sources = list(item.get("sources") or [])
        if not sources or len(sources) > 3:
            raise ValueError("%s lacks valid sources" % row_id)
        for source_url in sources:
            validate_url(source_url, row_id)
        item["sources"] = sources
        item["cite"] = list(sources)
        contact_sources = list(item.get("contact_sources") or [])
        has_contact = bool(
            item.get("phones") or item.get("emails") or item.get("site")
        )
        if has_contact:
            if not contact_sources or item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            for phone in item.get("phones") or []:
                if not re.fullmatch(r"[26]\d{9}", phone):
                    raise ValueError("%s carries an invalid phone" % row_id)
            for email in item.get("emails") or []:
                if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                    raise ValueError("%s carries an invalid email" % row_id)
            if item.get("site"):
                validate_url(item["site"], row_id)
            for source_url in contact_sources:
                validate_url(source_url, row_id)
                if source_url not in sources:
                    raise ValueError("contact source is outside identity sources")
        elif contact_sources or "contact_checked" in item:
            raise ValueError(
                "%s carries contact provenance without contact data" % row_id
            )
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Karystia English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Karystia rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Karystia kind totals drifted: %r" % dict(kinds))
    phone_bodies = sum(bool(item.get("phones")) for item in result)
    phone_values = sum(len(item.get("phones") or []) for item in result)
    email_bodies = sum(bool(item.get("emails")) for item in result)
    email_values = sum(len(item.get("emails") or []) for item in result)
    site_bodies = sum(bool(item.get("site")) for item in result)
    contact_bodies = sum(bool(
        item.get("phones") or item.get("emails") or item.get("site")
    ) for item in result)
    if (phone_bodies, phone_values) != (
            EXPECTED_PHONE_BODIES, EXPECTED_PHONE_VALUES):
        raise ValueError("Karystia phone coverage drifted")
    if (email_bodies, email_values, site_bodies, contact_bodies) != (
            EXPECTED_EMAIL_BODIES, EXPECTED_EMAIL_VALUES,
            EXPECTED_SITE_BODIES, 7):
        raise ValueError("Karystia contact coverage drifted")
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    }
    if url in (REGULATION_PDF, EARLIER_LEGAL_ACT):
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=90) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return unicase(" ".join(text.split()))


def check_live():
    checks = dict(LIVE_CHECKS)
    checks[REGULATION_PDF] = set()
    checks[EARLIER_LEGAL_ACT] = set()

    def one(item):
        url, markers = item
        payload, content_type = fetch(url)
        if url in (REGULATION_PDF, EARLIER_LEGAL_ACT):
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("Karystia legal source is not a PDF: %s" % url)
            return url
        if "html" not in content_type:
            raise ValueError("non-HTML Karystia source: %s" % url)
        page = normalized_page(payload)
        missing = [marker for marker in markers
                   if unicase(" ".join(marker.split())) not in page]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        return url

    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(one, checks.items()))
    return len(checks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        data = build()
        if args.check_live:
            checked = check_live()
            print("Karystia live checks passed for %d source pages" % checked)
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Karystia checks passed: %d bodies, %d phone bodies, "
                "%d email bodies, %d body sites" % (
                    len(rows),
                    sum(bool(item.get("phones")) for item in rows),
                    sum(bool(item.get("emails")) for item in rows),
                    sum(bool(item.get("site")) for item in rows),
                )
            )
    except Exception as exc:
        print("Karystia check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
