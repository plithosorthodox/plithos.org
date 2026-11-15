#!/usr/bin/env python3
"""Validate exact named Siderokastron bodies from Church sources.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_siderokastron_country.py --check
    python tools/directory_siderokastron_country.py --check-live
    python tools/directory_siderokastron_country.py --dump
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
PARENT = "ep-siderokastron"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" /
    "siderokastron_country.json"
)

OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
TRANSCRIPTION = (
    "https://www.e-nomothesia.gr/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-ekklesias-1115-859-2019.html"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-sidirokastroy/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/siderokastrou"
)
KIRYKOS_CONTACT = (
    "https://www.moni-kirikou-ioulittis.gr/"
    "%CE%B5%CF%80%CE%B9%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CE%BD%CE%AF%CE%B1"
)
KIRYKOS_SITE = "https://www.moni-kirikou-ioulittis.gr/"
STEPHEN_LOCATION_PDF = (
    "https://www.ecclesiagreece.gr/greek/press/ekklisia/material/"
    "1996_02_2.pdf"
)
TRIMORPHOS_SOURCE = "https://www.impantokratoros.gr/DCB300C4.el.aspx"
FORERUNNER_SITE = "https://www.timiosprodromos.gr/"

SOURCES = {
    "PDF": OFFICIAL_PDF,
    "TRANSCRIPTION": TRANSCRIPTION,
    "EP": PATRIARCHATE_PAGE,
    "COG": CHURCH_OF_GREECE_PAGE,
    "KIRYKOS": KIRYKOS_CONTACT,
    "STEPHEN_LOCATION": STEPHEN_LOCATION_PDF,
    "TRIMORPHOS": TRIMORPHOS_SOURCE,
    "FORERUNNER": FORERUNNER_SITE,
}


# Exact legal-roster order from the Church of Greece regulation.
# raw seat|English seat|Greek seat|raw dedication|Greek dedication|English dedication
PARISH_SOURCE = r'''
ΣΙΔΗΡΟΚΑΣΤΡΟΝ|Sidirokastro|Σιδηρόκαστρο|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΣΙΔΗΡΟΚΑΣΤΡΟΝ|Sidirokastro|Σιδηρόκαστρο|ΕΥΑΓΓΕΛΙΣΤΡΙΑ|Ευαγγελίστρια|Annunciation of the Theotokos
ΑΓΚΙΣΤΡΟΝ|Agkistro|Άγκιστρο|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΑΚΡΙΤΟΧΩΡΙΟΝ|Akritochori|Ακριτοχώρι|ΑΓ. ΚΩΝ. & ΕΛΕΝΗ|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen
ΑΜΠΕΛΑ|Ampela|Άμπελα|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΑΧΛΑΔΟΧΩΡΙΟΝ|Achladochori|Αχλαδοχώρι|ΠΡΟΦ. ΗΛΙΑΣ|Προφήτου Ηλιού|Prophet Elijah
ΒΑΜΒΑΚΟΦΥΤΟΝ|Vamvakofyto|Βαμβακόφυτο|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΒΥΡΩΝΕΙΑ|Vyronia|Βυρώνεια|ΑΓ. ΑΠΟΣΤΟΛΟΙ|Αγίων Αποστόλων|Holy Apostles
ΚΑΜΑΡΩΤΟΝ|Kamaroto|Καμαρωτό|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΚΑΠΝΟΦΥΤΟΝ|Kapnofyto|Καπνόφυτο|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΚΑΡΥΔΟΧΩΡΙΟΝ|Karydochori|Καρυδοχώρι|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Ν. ΠΕΤΡΙΤΣΙΟΝ|Neo Petritsi|Νέο Πετρίτσι|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΠΡΟΜΑΧΩΝ|Promachonas|Προμαχώνας|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΣΧΙΣΤΟΛΙΘΟΣ|Schistolithos|Σχιστόλιθος|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΣΤΡΥΜΟΝΟΧΩΡΙΟΝ|Strymonochori|Στρυμονοχώρι|ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Τιμίου Προδρόμου|Saint John the Forerunner
ΟΜΑΛΟ ΘΡΑΚΙΚΟ|Omalos Thrakiko|Ομαλό Θρακικό|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΘΕΡΜΟΠΗΓΗ|Thermopigi|Θερμοπηγή|ΑΓ. ΑΠΟΣΤΟΛΟΙ|Αγίων Αποστόλων|Holy Apostles
Φ. ΠΕΤΡΑ|Faia Petra|Φαιά Πέτρα|ΠΡΟΦ. ΗΛΙΑΣ|Προφήτου Ηλιού|Prophet Elijah
ΧΑΡΟΠΟΝ|Charopo|Χαροπό|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΧΟΡΤΕΡΟΝ|Chortero|Χορτερό|ΑΓ. ΑΝΤΩΝΙΟΣ|Αγίου Αντωνίου|Saint Anthony
ΗΡΑΚΛΕΙΑ|Irakleia|Ηράκλεια|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΑΜΜΟΥΔΙΑ|Ammoudia|Αμμουδιά|ΤΑΞΙΑΡΧΑΙ|Ταξιαρχών|Holy Archangels
ΑΜΜΟΥΔΙΑ|Ammoudia|Αμμουδιά|ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Τιμίου Προδρόμου|Saint John the Forerunner
ΒΑΛΤΕΡΟΝ|Valtero|Βαλτερό|ΑΓ. ΤΡΙΑΣ|Αγίας Τριάδος|Holy Trinity
ΓΕΦΥΡΟΥΔΙΟΝ|Gefyroudi|Γεφυρούδι|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΓΟΝΙΜΟΝ|Gonimo|Γόνιμο|ΑΓ. ΠΑΝΤΕΛΕΗΜΩΝ|Αγίου Παντελεήμονος|Saint Panteleimon
ΔΑΣΟΧΩΡΙΟΝ|Dasochori|Δασοχώρι|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΖΕΥΓΟΛΑΤΙΟΝ|Zevgolatio|Ζευγολατιό|ΑΓ. ΝΙΚΟΛΑΟΣ|Αγίου Νικολάου|Saint Nicholas
Ν. ΗΡΑΚΛΕΙΑ|Nea Irakleia|Νέα Ηράκλεια|ΓΕΝ. ΘΕΟΤΟΚΟΥ|Γενεσίου Θεοτόκου|Nativity of the Theotokos
ΚΑΛΟΚΑΣΤΡΟ|Kalokastro|Καλόκαστρο|ΑΓ. ΑΘΑΝΑΣΙΟΣ|Αγίου Αθανασίου|Saint Athanasius
ΚΟΙΜΗΣΙΣ|Koimisi|Κοίμηση|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΛΙΜΝΟΧΩΡΙΟΝ|Limnochori|Λιμνοχώρι|ΠΡΟΦ. ΗΛΙΑΣ|Προφήτου Ηλιού|Prophet Elijah
ΛΙΘΟΤΟΠΟΣ|Lithotopos|Λιθότοπος|ΑΓ. ΧΑΡΑΛΑΜΠΗΣ|Αγίου Χαραλάμπους|Saint Charalambos
ΜΕΓΑΛΟΧΩΡΙΟΝ|Megalochori|Μεγαλοχώρι|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΠΟΝΤΙΣΜΕΝΟΝ|Pontismeno|Ποντισμένο|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΣΙΜΩΝ|Simon|Σιμών|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΤΡΙΑΔΑ|Triada|Τριάδα|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΧΕΙΜΑΡΡΟΣ|Cheimarros|Χείμαρρος|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΧΡΥΣΟΧΩΡΑΦΑ|Chrysochorafa|Χρυσοχώραφα|ΑΓ. ΝΙΚΟΛΑΟΣ|Αγίου Νικολάου|Saint Nicholas
ΨΩΜΟΤΟΠΙΟΝ|Psommotopi|Ψωμοτόπι|ΖΩΟΔΟΧΟΣ ΠΗΓΗ|Ζωοδόχου Πηγής|Life-Giving Spring
ΑΝΩ ΠΟΡΟΙΑ|Ano Poroia|Άνω Πορόια|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΚΑΤΩ ΠΟΡΟΙΑ|Kato Poroia|Κάτω Πορόια|ΤΙΜ. ΠΡΟΔΡΟΜΟΣ|Τιμίου Προδρόμου|Saint John the Forerunner
ΑΝΑΤΟΛΗ|Anatoli|Ανατολή|ΠΡΟΦ. ΗΛΙΑΣ|Προφήτου Ηλιού|Prophet Elijah
ΘΕΟΔΩΡΕΙΟΝ|Theodoreio|Θεοδώρειο|ΜΕΤΑΜ. ΣΩΤΗΡΟΣ|Μεταμορφώσεως Σωτήρος|Transfiguration of the Savior
ΚΑΣΤΑΝΟΥΣΑ|Kastanousa|Καστανούσα|ΑΓΙΑ ΤΡΙΑΣ|Αγίας Τριάδος|Holy Trinity
ΚΑΣΤΑΝΟΥΣΑ|Kastanousa|Καστανούσα|ΑΓ. ΚΩΝ & ΕΛΕΝΗ|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen
ΚΑΛΟΧΩΡΙΟΝ|Kalochori|Καλοχώρι|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΚΕΡΚΙΝΗ|Kerkini|Κερκίνη|ΑΓ. ΤΡΙΑΣ|Αγίας Τριάδος|Holy Trinity
ΚΟΡΥΦΟΥΔΙΟΝ|Koryfoudi|Κορυφούδι|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΛΕΙΔΑΔΙΑ|Leidadia|Λειδάδια|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΜΑΚΡΥΝΙΤΣΑ|Makrynitsa|Μακρυνίτσα|ΓΕΝ. ΘΕΟΤΟΚΟΥ|Γενεσίου Θεοτόκου|Nativity of the Theotokos
ΜΑΝΔΡΑΚΙΟΝ|Mandraki|Μανδράκι|ΓΕΝ. ΘΕΟΤΟΚΟΥ|Γενεσίου Θεοτόκου|Nativity of the Theotokos
ΜΟΝΑΣΤΗΡΑΚΙΟΝ|Monastiraki|Μοναστηράκι|ΑΓ. ΒΑΣΙΛΕΙΟΣ|Αγίου Βασιλείου|Saint Basil
ΝΕΟΧΩΡΙΟΝ|Neochori|Νεοχώρι|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΟΔΗΓΗΤΡΙΑ|Odigitria|Οδηγήτρια|ΑΓ. ΠΑΝΤΕΛΕΗΜΩΝ|Αγίου Παντελεήμονος|Saint Panteleimon
ΠΑΡΑΠΟΤΑΜΟΣ|Parapotamos|Παραπόταμος|ΑΓ. ΑΘΑΝΑΣΙΟΣ|Αγίου Αθανασίου|Saint Athanasius
ΠΛΑΤΑΝΑΚΙΑ|Platanakia|Πλατανάκια|ΖΩΟΔΟΧΟΣ ΠΗΓΗ|Ζωοδόχου Πηγής|Life-Giving Spring
ΡΟΔΟΠΟΛΙΣ|Rodopoli|Ροδόπολη|ΤΙΜ. ΣΤΑΥΡΟΣ|Τιμίου Σταυρού|Holy Cross
ΣΙΔΗΡΟΧΩΡΙΟΝ|Sidirochori|Σιδηροχώρι|ΑΓ. ΚΥΡΙΑΚΗ|Αγίας Κυριακής|Saint Kyriaki
ΣΤΑΥΡΟΔΡΟΜΙΟΝ|Stavrodromi|Σταυροδρόμι|ΑΓ. ΑΠΟΣΤΟΛΟΙ|Αγίων Αποστόλων|Holy Apostles
ΚΛΕΙΔΙ|Kleidi|Κλειδί|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΑΕΤΟΒΟΥΝΙΟΝ|Aetovouni|Αετοβούνι|ΜΕΤΑΜ. ΣΩΤΗΡΟΣ|Μεταμορφώσεως Σωτήρος|Transfiguration of the Savior
ΛΑΓΩΝΙΟΝ|Lagonio|Λαγώνιο|ΑΓ. ΠΕΤΡΟΣ ΚΑΙ ΠΑΥΛΟΣ|Αγίων Αποστόλων Πέτρου και Παύλου|Saints Peter and Paul
ΜΕΤΑΛΛΟΝ|Metallo|Μέταλλο|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΠΟΛΥΒΡΥΣΟΝ|Polyvryso|Πολύβρυσο|ΚΟΙΜ. ΘΕΟΤΟΚΟΥ|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΦΙΛΥΡΑ|Filyra|Φιλύρα|ΑΓ. ΑΘΑΝΑΣΙΟΣ|Αγίου Αθανασίου|Saint Athanasius
ΚΑΠΝΟΤΟΠΟΣ|Kapnotopos|Καπνότοπος|ΑΓ. ΑΝΑΡΓΥΡΟΙ|Αγίων Αναργύρων|Holy Unmercenaries
ΚΑΤΩ ΚΑΡΥΔΙΑ|Kato Karydia|Κάτω Καρυδιά|ΑΓ. ΑΘΑΝΑΣΙΟΣ|Αγίου Αθανασίου|Saint Athanasius
ΚΡΑΣΟΧΩΡΙΟΝ|Krasochori|Κρασοχώρι|ΤΑΞΙΑΡΧΑΙ|Ταξιαρχών|Holy Archangels
ΜΕΣΣΑΙΑ|Messaia|Μεσσαία|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΘΕΟΔΩΡΙΤΣΙ|Theodoritsi|Θεοδωρίτσι|ΑΡΧΑΓ. ΜΙΧΑΗΛ|Αρχαγγέλου Μιχαήλ|Archangel Michael
ΠΑΛΑΙΑ ΚΑΣΤΑΝΟΥΣΑ|Palaia Kastanousa|Παλαιά Καστανούσα|ΑΓ. ΤΡΙΑΣ|Αγίας Τριάδος|Holy Trinity
ΚΟΡΥΦΟΥΔΙΟΝ|Koryfoudi|Κορυφούδι|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΜΕΣΟΛΟΦΟΣ|Mesolofos|Μεσόλοφος|ΜΕΤΑΜ. ΣΩΤΗΡΟΣ|Μεταμορφώσεως Σωτήρος|Transfiguration of the Savior
ΑΓΡΙΟΛΕΥΚΗ|Agrioleuki|Αγριολεύκη|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
ΔΑΦΝΟΥΣΑ|Dafnousa|Δαφνούσα|ΙΩΑΝ. ΘΕΟΛΟΓΟΣ|Αγίου Ιωάννου του Θεολόγου|Saint John the Theologian
ΜΑΝΙΤΑΡΙΟΝ|Manitario|Μανιτάρι|ΑΓ. ΔΗΜΗΤΡΙΟΣ|Αγίου Δημητρίου|Saint Demetrius
ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗ|Agias Paraskevi|Αγίας Παρασκευή|ΑΓ. ΓΕΩΡΓΙΟΣ|Αγίου Γεωργίου|Saint George
'''


# key|rank|English name|Greek local name|English seat|Greek address|phones|
# site|identity source tokens|contact source tokens|live markers
MONASTIC_SOURCE = r'''
kirykos-julitta|Monastery|Saints Kirykos and Julitta Monastery, Sidirokastro|Ιερά Μονή Αγίων Κηρύκου και Ιουλίττης|Sidirokastro|Σιδηρόκαστρο|23230-22395|https://www.moni-kirikou-ioulittis.gr/|EP,COG,KIRYKOS|EP,COG,KIRYKOS|Κηρύκου;Ιουλίττης;2323022395
stephen-chrysostom|Monastery|Holy Protomartyr Stephen and Saint John Chrysostom Monastery, Faia Petra|Ιερά Μονή Αγίου Πρωτομάρτυρος Στεφάνου και Αγίου Ιωάννου Χρυσοστόμου|Faia Petra|Φαιά Πέτρα|23230-24516||EP,COG,STEPHEN_LOCATION|EP,COG|Στεφάνου;Χρυσοστόμου;2323024516
george-trimorphos|Monastery|Saint George Trimorphos Monastery, Monastiraki|Ιερά Μονή Αγίου Γεωργίου Τριμόρφου|Monastiraki|Μοναστηράκι|2327300381,23270-22795||EP,COG,TRIMORPHOS|EP,COG|Αγίου Γεωργίου;2327300381;2327022795
holy-protection|Monastery|Holy Protection Monastery|Ιερά Μονή Αγίας Σκέπης|Siderokastron Metropolis|Ιερά Μητρόπολις Σιδηροκάστρου|23270-22094||EP,COG|EP,COG|Αγίας Σκέπης;2327022094
barbara|Monastery|Saint Barbara Monastery|Ιερά Μονή Αγίας Βαρβάρας|Siderokastron Metropolis|Ιερά Μητρόπολις Σιδηροκάστρου|23230-22987||EP,COG|EP,COG|Αγίας Βαρβάρας;2323022987
panagia-goumera|Monastery|Nativity of the Theotokos, Panagia Goumera Monastery, Makrynitsa|Ιερά Μονή Γενεσίου της Θεοτόκου Παναγίας Γουμερά|Makrynitsa|Μακρυνίτσα|23270-22017||EP|EP|Παναγία Γουμερά;2327022017
george-koryfoudi|Monastery|Saint George Monastery of Koryfoudi, Lake Kerkini|Ιερά Μονή Αγίου Γεωργίου Κορυφουδίου Λίμνης Κερκίνης|Koryfoudi|Κορυφούδι, Λίμνη Κερκίνη|23270-51578||EP|EP|Αγίου Γεωργίου;Κορυφουδίου;2327051578
prophet-elijah-kato-poroia|Monastery|Prophet Elijah Monastery, Kato Poroia|Ιερά Μονή Προφήτου Ηλιού Κάτω Ποροΐων|Kato Poroia|Κάτω Πορόια|||EP||Προφήτου Ηλιού;Κάτω Ποροΐων
forerunner-hermitage|Hermitage|Honorable Forerunner Hermitage, Akritochori|Ησυχαστήριο Τιμίου Προδρόμου Ακριτοχωρίου|Akritochori|Ακριτοχώρι|23230-71189|https://www.timiosprodromos.gr/|EP,COG,FORERUNNER|EP,COG|Τιμίου Προδρόμου;2323071189
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


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def source_values(value):
    return [SOURCES[token.strip()] for token in value.split(",")
            if token.strip()]


def build_rows():
    rows = []
    parish_lines = PARISH_SOURCE.strip().splitlines()
    if len(parish_lines) != 78:
        raise ValueError("expected 78 regulated Siderokastron parishes")
    for index, raw in enumerate(parish_lines, 1):
        (raw_seat, seat, greek_seat, raw_dedication,
         local_dedication, dedication) = raw.split("|", 5)
        rank = "Parish Church"
        name = "%s of %s, %s" % (rank, dedication, seat)
        rows.append({
            "id": "gr-ep-siderokastron-%03d-%s" %
                  (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (local_dedication, greek_seat),
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [OFFICIAL_PDF],
            "legal_markers": [raw_seat, raw_dedication],
        })
    for raw in MONASTIC_SOURCE.strip().splitlines():
        fields = raw.split("|", 10)
        (key, rank, name, local, seat, address, phones, site,
         source_tokens, contact_tokens, markers) = fields
        index = len(rows) + 1
        row = {
            "id": "gr-ep-siderokastron-%03d-%s" % (index, key),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": source_values(source_tokens),
            "live_markers": [x for x in markers.split(";") if x],
        }
        if phones:
            row["phones"] = split_values(phones)
        if site:
            row["site"] = site
        if contact_tokens:
            row["contact_sources"] = source_values(contact_tokens)
            row["contact_checked"] = CHECKED
        rows.append(row)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 87
EXPECTED_OWNER_COUNTS = {PARENT: 87}
EXPECTED_KINDS = {"monastery": 9, "parish": 78}
EXPECTED_RANKS = {
    "Hermitage": 1,
    "Monastery": 8,
    "Parish Church": 78,
}
EXPECTED_CONTACT_BODIES = 8
EXPECTED_PHONE_BODIES = 8
EXPECTED_PHONE_VALUES = 9
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 2
EXPECTED_ADDRESS_BODIES = 87
EXISTING_PARENTS = {PARENT}
ALLOWED_DUPLICATE_IDS = {
    "gr-ep-siderokastron-049-parish-church-of-saint-george-koryfoudi",
    "gr-ep-siderokastron-073-parish-church-of-saint-george-koryfoudi",
}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "www.e-nomothesia.gr",
    "ec-patr.org",
    "www.e-patr.org",
    "www.moni-kirikou-ioulittis.gr",
    "www.timiosprodromos.gr",
    "ieramonipanagiagoumera.gr",
    "www.impantokratoros.gr",
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
    site = item.get("site")
    if site:
        validate_url(site, item.get("id"))
        source_hosts = {urlparse(value).netloc for value in sources}
        if urlparse(site).netloc not in source_hosts:
            raise ValueError("%s site host lacks an identity source" % item.get("id"))
    item.pop("legal_markers", None)
    item.pop("live_markers", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Siderokastron candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Siderokastron candidate ledger date drifted")
    expected_summary = {
        PARENT: 87,
        "total": 87,
        "regulated_parish_rows": 78,
        "parish_kind_rows": 78,
        "monastery_kind_rows": 9,
        "contact_bodies": 8,
        "phone_bodies": 8,
        "public_phone_values": 9,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 2,
        "address_bodies": 87,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Siderokastron ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Siderokastron ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Siderokastron ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Siderokastron ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Siderokastron ledger has forbidden punctuation")
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
            pair = {row_id, signatures[signature]}
            if pair != ALLOWED_DUPLICATE_IDS:
                raise ValueError("%s duplicates %s" %
                                 (row_id, signatures[signature]))
        else:
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
        raise ValueError("Siderokastron English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Siderokastron rank totals drifted")
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Siderokastron kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Siderokastron parent totals drifted")
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
        raise ValueError("Siderokastron contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
    })
    context = None
    with urlopen(request, timeout=60, context=context) as response:
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
    cache = {}
    urls = sorted({url for row in ROWS for url in row.get("sources", [])} |
                  {TRANSCRIPTION})
    for url in urls:
        payload, content_type = fetch(url)
        if url.lower().endswith(".pdf"):
            if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                raise ValueError("live source is not a PDF: %s" % url)
            cache[url] = payload
        else:
            if "html" not in content_type and not payload.lstrip().startswith(b"<"):
                raise ValueError("live source is not HTML: %s" % url)
            cache[url] = normalized_page(payload)

    legal = cache[TRANSCRIPTION]
    for marker in ("Συνολικός αριθμός Ενοριών: 78",
                   "ΣΙΔΗΡΟΚΑΣΤΡΟΝ", "ΚΟΡΥΦΟΥΔΙΟΝ",
                   "ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗ"):
        if unicase(marker) not in legal:
            raise ValueError("legal transcription lacks marker: %s" % marker)

    for row in ROWS[78:]:
        pages = " ".join(
            cache[url] for url in row["sources"]
            if isinstance(cache[url], str)
        )
        digit_pages = compact_digits(pages)
        for marker in row.get("live_markers") or []:
            if marker.isdigit():
                if marker not in digit_pages:
                    raise ValueError("%s lacks live marker %s" %
                                     (row["id"], marker))
            elif unicase(marker) not in pages:
                raise ValueError("%s lacks live marker %s" %
                                 (row["id"], marker))
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digit_pages:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
    print("Siderokastron live sources: %d URLs checked" % len(urls))


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
        print("Siderokastron: 87 exact bodies; 78 regulated parishes, "
              "8 monasteries, and 1 hermitage")
        print("Contacts: 8 bodies; 9 phones; 0 emails; 2 body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Siderokastron: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
