#!/usr/bin/env python3
"""Validate exact named Kassandreia bodies from current official sources.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_kassandreia_country.py --check
    python tools/directory_kassandreia_country.py --check-live
    python tools/directory_kassandreia_country.py --dump
"""

import argparse
from collections import Counter
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "kassandreia_country.json"
)
PARENT = "ep-kassandreia"
ROSTER_PAGE = (
    "https://www.imkassandreias.gr/index.php/el/ieroi-naoi/pinakas"
)
MONASTERIES_PAGE = (
    "https://www.imkassandreias.gr/index.php/el/ieresmones"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-kassandreias/"
)
LEGAL_PAGE = (
    "https://www.e-nomothesia.gr/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-ekklesias-3650-1983-2019.html"
)
CHURCH_OF_GREECE_PDF = (
    "https://www.ecclesia.gr/greek/press/ekklisia/"
    "2019_decembrios.pdf"
)


# Greek seat | Greek dedication | exact displayed phone and postal contact
ROSTER_ROWS = r'''
Πολύγυρος|Μητροπολιτικός Ναός Ἁγίου Νικολάου|23710.23009/63100
Πολύγυρος|Ἁγίου Χαραλάμπους|23710.22214/63100
Ἅγιος Ἀντώνιος|Ἁγίου Ἀντωνίου|23960.41740/57006
Ἅγιος Μάμμας|Κοιμήσεως τῆς Θεοτόκου|23730.91710/63200
Ἅγιος Νικόλαος|Ἁγίου Γεωργίου|23750.32095/63087
Ἅγιος Παντελεήμων|Ἁγίου Παντελεήμονος|23730.51486/63200
Ἁγία Παρασκευή-Θεσ/νίκης|Ἁγίας Παρασκευῆς|23960.41259/57001
Ἁγία Παρασκευή-Κασσανδρείας|Τιμίου Προδρόμου|23740.62155/63085
Ἅγιος Παῦλος|Ἁγίου Γρηγορίου τοῦ Θεολόγου|23990.48498/63080
Ἄθυτος|Ἁγίου Δημητρίου|23740.91317/63077
Ἀμπελάκια|Ἁγίων Ἀναργύρων|23920.75397/63080
Βάβδος|Κοιμήσεως τῆς Θεοτόκου|23710.91030/63084
Βασιλικά|Ἁγίου Γεωργίου|23960.22322/57006
Βατοπέδιον|Ἁγίου Παντελεήμονος|23710.98331/63071
Βράσταμα|Εὐαγγελισμοῦ τῆς Θεοτόκου|23710.71318/63100
Γαλαρινός|Ἁγίου Νικολάου|23960.31349/57006
Γερακινῆς|Ἁγίων Θεοδώρων|23710.51676/63100
Γεωπονικά|Ἁγίας Μαρίνης|23990.33998/63080
Νέα Γωνιά|Κοιμήσεως τῆς Θεοτόκου|23990.22934/63080
Διονυσίου|Τιμίου Προδρόμου|23730.21812/63200
Παραλία Διονυσίου|Τιμίου Προδρόμου|23730.26694/63200
Ἐλαιοχώρια|Ἁγίου Γεωργίου|23730.71061/63080
Ζωγράφου|Ἁγίων Κωνσταντίνου καί Ἑλένης|23730.23977/63200
Νέα Ἡράκλεια|Ἁγίου Γεωργίου|23990.21670/63080
Θέρμη|Ἁγίου Νικολάου|2310.462116/57001
Καλάνδρα|Κοιμήσεως τῆς Θεοτόκου|23740.41120/63077
Καλλιθέα|Ἁγίου Νικολάου|23740.22876/63077
Νεά Καλλικράτεια|Ὁσίας Παρασκευῆς τῆς Ἐπιβατινῆς|23990.21294/63080
Καλύβες|Ἁγίου Μοδέστου|23710.51393/63100
Καρδία|Γενεσίου τῆς Θεοτόκου|23920.61138/57500
Κασσανδρεία|Γενεσίου τῆς Θεοτόκου|23740.22388/63077
Κασσανδρινό|Κοιμήσεως τῆς Θεοτόκου|23750-41.493/63077
Κελλί|Γενεσίου τῆς Θεοτόκου|23710-71.320/63078
Κηπούπολις|Μεταμορφώσεως τοῦ Σωτῆρος|23920-51.070/63080
Κρήνη|Ἁγίου Γεωργίου|23730.73202/63088
Κρυοπηγή|Ἁγίου Γεωργίου|23740.51074/53077
Λακκιά|Ἁγίου Δημητρίου|23960-23590/57006
Λάκκωμα|Κοιμήσεως τῆς Θεοτόκου|23920-31.451/63080
Νέος Μαρμαρᾶς|Παμμεγίστων Ταξιαρχῶν|23750.71690/ τ.κ. 63081
Μεσημέρι|Ἁγίου Παντελεήμονος|23920-92028/57500
Μεταγγίτσι|Ἁγίας Παρασκευῆς|23750-92353/63078
Μεταμόρφωση|Μεταμορφώσεως τοῦ Σωτῆρος καί Ἁγίου Βασιλείου τοῦ Μεγάλου|23750-71125/63088
Μονοπήγαδο|Μεταμορφώσεως τοῦ Σωτῆρος|23960-25209/57006
Νέα Μουδανιά|Ἁγίου Γεωργίου Παναγία Κορυφινή|23730-21002/63200
Νικήτη|Ἁγίου Νικήτα Κοιμήσεως τῆς Θεοτόκου|23750-22831/63088
Ὄλυνθος|Ἁγίου Ἀθανασίου|23730-91294/63200
Ὁρμύλια|Ἁγίου Γεωργίου|23710.41245/63071
Παλιούρι|Ἁγίου Γεωργίου|23740-92077/63085
Ἄνω Περαία|Μεταμορφώσεως τοῦ Σωτῆρος|23920-22.563/57019
Κάτω Περαία|Ἁγίων Ἀποστόλων Πέτρου καί Παύλου|23920-29039/57019
Πετράλωνα|Προφήτου Ἠλιού|23730-71.102/63080
Πευκοχώρι|Ἁγίου Ἀθανασίου|23740-61467/63085
Νέα Πλάγια|Ἁγίου Γεωργίου|23730-31.026/63200
Πλαγιάρι|Ἁγίου Δημητρίου|23920-61.350/57500
Πλανά|Ἁγίας Φωτεινῆς|23730-31.460/63078
Πολύχρονο|Ἁγίου Ἀθανασίου|23740-52225/63078
Πορταριά|Κοιμήσεως τῆς Θεοτόκου|23730-23467/63200
Νέα Ποτίδαια|Ἁγίου Γεωργίου|23730-41603/63200
Πυργαδίκια|Γενεσίου τῆς Θεοτόκου|23750-53.102/63078
Νέα Ῥαιδεστός|Ἁγίου Ἀθανασίου|2310-464.230/57001
Νέο Ῥύσιο|Μεταμορφώσεως τοῦ Σωτῆρος|23920-71.220/57001
Σάρτη|Κοιμήσεως τῆς Θεοτόκου|23750-94520/63072
Σήμανδρα|Ἁγίων Δώδεκα Ἀποστόλων|23730-61.342/63200
Νέα Σκιώνη|Ἁγίου Νικολάου|6944443140/63077
Σουρωτή|Ἁγίων Ἀναργύρων|23960.41744/57006
Συκιά|Ἁγίου Ἀθανασίου|23750-41.384/63072
Νέα Σύλλατα|Κοιμήσεως τῆς Θεοτόκου|23990-21746/63080
Κάτω Σχολάρι|Ἁγίου Γεωργίου|23920-91.310/57500
Σωζόπολη|Μεταμορφώσεως τοῦ Σωτῆρος|23730-81.256/53200
Ταγαράδες|Τιμίου Προδρόμου|23920.72242/54500
Ταξιάρχης|Ἁγίου Ἀρχαγγέλου|23710-94185/63100
Νέα Τένεδος|Κοιμήσεως τῆς Θεοτόκου|23730-53203/63200
Νέα Τρίγλια|Παναγίας Παντοβασιλίσσης|23730-51245/63079
Τρίλοφος|Ἁγίου Ἀθανασίου|29320-61247/57500
Νέα Φλογητά|Ἁγίου Γεωργίου|23730-31804/63200
Φούρκα|Ἁγίων Τριῶν Ἱεραρχῶν|23740-43834/63077
Νέα Φώκαια|Ἁγίου Νικολάου|23740-81858/63077
Χανιώτη|Ἁγίου Ἰωάννου τοῦ Χρυσοστόμου|23740-51424/63085
'''


SEAT_NAMES = {
    "Πολύγυρος": "Polygyros",
    "Ἅγιος Ἀντώνιος": "Agios Antonios",
    "Ἅγιος Μάμμας": "Agios Mamas",
    "Ἅγιος Νικόλαος": "Agios Nikolaos",
    "Ἅγιος Παντελεήμων": "Agios Panteleimon",
    "Ἁγία Παρασκευή-Θεσ/νίκης": "Agia Paraskevi, Thessaloniki",
    "Ἁγία Παρασκευή-Κασσανδρείας": "Agia Paraskevi, Kassandra",
    "Ἅγιος Παῦλος": "Agios Pavlos",
    "Ἄθυτος": "Afytos",
    "Ἀμπελάκια": "Ampelakia",
    "Βάβδος": "Vavdos",
    "Βασιλικά": "Vasilika",
    "Βατοπέδιον": "Vatopedi",
    "Βράσταμα": "Vrastama",
    "Γαλαρινός": "Galarinos",
    "Γερακινῆς": "Gerakini",
    "Γεωπονικά": "Geoponika",
    "Νέα Γωνιά": "Nea Gonia",
    "Διονυσίου": "Dionysiou",
    "Παραλία Διονυσίου": "Paralia Dionysiou",
    "Ἐλαιοχώρια": "Elaiochoria",
    "Ζωγράφου": "Zografou",
    "Νέα Ἡράκλεια": "Nea Irakleia",
    "Θέρμη": "Thermi",
    "Καλάνδρα": "Kalandra",
    "Καλλιθέα": "Kallithea",
    "Νεά Καλλικράτεια": "Nea Kallikrateia",
    "Καλύβες": "Kalyves",
    "Καρδία": "Kardia",
    "Κασσανδρεία": "Kassandreia",
    "Κασσανδρινό": "Kassandrino",
    "Κελλί": "Kelli",
    "Κηπούπολις": "Kipoupoli",
    "Κρήνη": "Krini",
    "Κρυοπηγή": "Kryopigi",
    "Λακκιά": "Lakkia",
    "Λάκκωμα": "Lakkoma",
    "Νέος Μαρμαρᾶς": "Neos Marmaras",
    "Μεσημέρι": "Mesimeri",
    "Μεταγγίτσι": "Metangitsi",
    "Μεταμόρφωση": "Metamorfosi",
    "Μονοπήγαδο": "Monopigado",
    "Νέα Μουδανιά": "Nea Moudania",
    "Νικήτη": "Nikiti",
    "Ὄλυνθος": "Olynthos",
    "Ὁρμύλια": "Ormylia",
    "Παλιούρι": "Paliouri",
    "Ἄνω Περαία": "Ano Peraia",
    "Κάτω Περαία": "Kato Peraia",
    "Πετράλωνα": "Petralona",
    "Πευκοχώρι": "Pefkochori",
    "Νέα Πλάγια": "Nea Plagia",
    "Πλαγιάρι": "Plagiari",
    "Πλανά": "Plana",
    "Πολύχρονο": "Polychrono",
    "Πορταριά": "Portaria",
    "Νέα Ποτίδαια": "Nea Potidaia",
    "Πυργαδίκια": "Pyrgadikia",
    "Νέα Ῥαιδεστός": "Nea Raidestos",
    "Νέο Ῥύσιο": "Neo Rysio",
    "Σάρτη": "Sarti",
    "Σήμανδρα": "Simandra",
    "Νέα Σκιώνη": "Nea Skioni",
    "Σουρωτή": "Souroti",
    "Συκιά": "Sykia",
    "Νέα Σύλλατα": "Nea Syllata",
    "Κάτω Σχολάρι": "Kato Scholari",
    "Σωζόπολη": "Sozopoli",
    "Ταγαράδες": "Tagarades",
    "Ταξιάρχης": "Taxiarchis",
    "Νέα Τένεδος": "Nea Tenedos",
    "Νέα Τρίγλια": "Nea Triglia",
    "Τρίλοφος": "Trilofos",
    "Νέα Φλογητά": "Nea Flogita",
    "Φούρκα": "Fourka",
    "Νέα Φώκαια": "Nea Fokaia",
    "Χανιώτη": "Chaniotis",
}


DEDICATIONS = {
    "Μητροπολιτικός Ναός Ἁγίου Νικολάου": "Saint Nicholas",
    "Ἁγίου Χαραλάμπους": "Saint Charalambos",
    "Ἁγίου Ἀντωνίου": "Saint Anthony",
    "Κοιμήσεως τῆς Θεοτόκου": "Dormition of the Theotokos",
    "Ἁγίου Γεωργίου": "Saint George",
    "Ἁγίου Παντελεήμονος": "Saint Panteleimon",
    "Ἁγίας Παρασκευῆς": "Saint Paraskevi",
    "Τιμίου Προδρόμου": "Saint John the Forerunner",
    "Ἁγίου Γρηγορίου τοῦ Θεολόγου": "Saint Gregory the Theologian",
    "Ἁγίου Δημητρίου": "Saint Demetrius",
    "Ἁγίων Ἀναργύρων": "Holy Unmercenaries",
    "Εὐαγγελισμοῦ τῆς Θεοτόκου": "Annunciation of the Theotokos",
    "Ἁγίου Νικολάου": "Saint Nicholas",
    "Ἁγίων Θεοδώρων": "Holy Theodores",
    "Ἁγίας Μαρίνης": "Saint Marina",
    "Ἁγίων Κωνσταντίνου καί Ἑλένης": "Saints Constantine and Helen",
    "Ὁσίας Παρασκευῆς τῆς Ἐπιβατινῆς": "Venerable Paraskevi of Epivates",
    "Ἁγίου Μοδέστου": "Saint Modest",
    "Γενεσίου τῆς Θεοτόκου": "Nativity of the Theotokos",
    "Μεταμορφώσεως τοῦ Σωτῆρος": "Transfiguration of the Savior",
    "Παμμεγίστων Ταξιαρχῶν": "Holy Archangels",
    "Μεταμορφώσεως τοῦ Σωτῆρος καί Ἁγίου Βασιλείου τοῦ Μεγάλου": "Transfiguration of the Savior and Saint Basil the Great",
    "Ἁγίου Γεωργίου Παναγία Κορυφινή": "Saint George and Panagia Koryfini",
    "Ἁγίου Νικήτα Κοιμήσεως τῆς Θεοτόκου": "Saint Niketas and Dormition of the Theotokos",
    "Ἁγίου Ἀθανασίου": "Saint Athanasius",
    "Ἁγίων Ἀποστόλων Πέτρου καί Παύλου": "Holy Apostles Peter and Paul",
    "Προφήτου Ἠλιού": "Prophet Elijah",
    "Ἁγίας Φωτεινῆς": "Saint Photini",
    "Ἁγίων Δώδεκα Ἀποστόλων": "Holy Twelve Apostles",
    "Ἁγίου Ἀρχαγγέλου": "Holy Archangel",
    "Παναγίας Παντοβασιλίσσης": "Panagia Pantovasilissa",
    "Ἁγίων Τριῶν Ἱεραρχῶν": "Holy Three Hierarchs",
    "Ἁγίου Ἰωάννου τοῦ Χρυσοστόμου": "Saint John Chrysostom",
}


# source marker | local title | dedication | seat | address | rank | phone | year
MONASTIC_ROWS = r'''
Κοίμησις Θεοτόκου|Ἱερά Μονή Κοιμήσεως Θεοτόκου|Dormition of the Theotokos|Polygyros|Πολύγυρος, Τ.Κ. 631 00|Monastery||1963
Ἅγιος Ἀρσένιος ὁ Καππαδόκης|Ἱερά Μονή Ἁγίου Ἀρσενίου τοῦ Καππαδόκου|Saint Arsenios the Cappadocian|Vatopedi|Βατοπαίδιον Χαλκιδικῆς, Τ.Κ. 631 00|Monastery|23710-41880|1986
Ὅσιος Ἰωάννης ὁ Ρῶσος καί Ὁμολογητής|Ἱερά Μονή Ὁσίου Ἰωάννου τοῦ Ρώσου καί Ὁμολογητοῦ|Venerable John the Russian and Confessor|Pefkochori|Πευκοχώριον, Τ.Κ. 630 85|Monastery|23740-61656|1989
Ἀπόστολος καί Εὐαγγελιστής Ἰωάννης ὁ Θεολόγος|Ἱερά Μονή Ἀποστόλου καί Εὐαγγελιστοῦ Ἰωάννου τοῦ Θεολόγου|Apostle and Evangelist John the Theologian|Vasilika|Βασιλικά Θεσσαλονίκης, Τ.Κ. 570 06|Monastery|23960-41320|1972
Ἅγιος Ἰωάννης ὁ Πρόδρομος|Ἱερά Μονή Ἁγίου Ἰωάννου τοῦ Προδρόμου|Saint John the Forerunner|Metamorfosi|Μεταμόρφωσις Χαλκιδικῆς, Τ.Κ. 630 88|Monastery|23750-61592|1977
Ἱερά Μονή Ἁγίου Στεφάνου|Ἱερά Μονή Ἁγίου Στεφάνου|Saint Stephen|Peraia|Περαία Θεσσαλονίκης, Τ.Κ. 570 19|Monastery|23920-23505|1999
Ἱερόν Σταυροπηγιακόν καί Πατριαρχικόν Μετόχιον Εὐαγγελισμοῦ τῆς Θεοτόκου|Ἱερόν Σταυροπηγιακόν καί Πατριαρχικόν Μετόχιον Εὐαγγελισμοῦ τῆς Θεοτόκου τῆς Ἱερᾶς Μονῆς Σίμωνος Πέτρας|Annunciation of the Theotokos Metochion of Simonopetra|Ormylia|Ὁρμυλία Χαλκιδικῆς, Τ.Κ. 630 71|Patriarchal Metochion|23710- 41278|
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
    live_rows = []
    roster_lines = ROSTER_ROWS.strip().splitlines()
    if len(roster_lines) != 78:
        raise ValueError("expected 78 current official parish rows")
    roster_seats = set()
    roster_dedications = set()
    for index, raw in enumerate(roster_lines, 1):
        seat_local, dedication_local, contact = raw.split("|", 2)
        phone, postal_text = contact.rsplit("/", 1)
        postal = re.sub(r"\D", "", postal_text)
        if len(postal) != 5:
            raise ValueError("invalid postal contact in roster row %d" % index)
        roster_seats.add(seat_local)
        roster_dedications.add(dedication_local)
        seat = SEAT_NAMES.get(seat_local)
        dedication = DEDICATIONS.get(dedication_local)
        if not seat or not dedication:
            raise ValueError("missing English map for roster row %d" % index)
        rank = "Metropolitan Church" if index == 1 else "Parish Church"
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-kassandreia-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (dedication_local, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat_local, "Τ.Κ. %s" % postal],
            "phones": [phone],
            "sources": [ROSTER_PAGE],
            "contact_sources": [ROSTER_PAGE],
            "contact_checked": CHECKED,
        }
        rows.append(item)
        live_rows.append((seat_local, dedication_local, contact))
    if roster_seats != set(SEAT_NAMES):
        raise ValueError("Kassandreia seat map coverage drifted")
    if roster_dedications != set(DEDICATIONS):
        raise ValueError("Kassandreia dedication map coverage drifted")
    markers = {}
    monastic_lines = MONASTIC_ROWS.strip().splitlines()
    if len(monastic_lines) != 7:
        raise ValueError("expected seven current monastic institutions")
    for raw in monastic_lines:
        (marker, local, dedication, seat, address, rank, phone,
         founded) = raw.split("|", 7)
        index = len(rows) + 1
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-kassandreia-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address],
            "sources": [MONASTERIES_PAGE, PATRIARCHATE_PAGE],
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [MONASTERIES_PAGE]
            item["contact_checked"] = CHECKED
        if founded:
            item["founded"] = [founded]
        rows.append(item)
        markers[item["id"]] = [marker] + ([phone] if phone else [])
    return rows, live_rows, markers


ROWS, LIVE_ROSTER_ROWS, MONASTIC_LIVE_MARKERS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 85
EXPECTED_OWNER_COUNTS = {PARENT: 85}
EXPECTED_KINDS = {"monastery": 7, "parish": 78}
EXPECTED_RANKS = {
    "Metropolitan Church": 1,
    "Monastery": 6,
    "Parish Church": 77,
    "Patriarchal Metochion": 1,
}
EXPECTED_CONTACT_BODIES = 84
EXPECTED_PHONE_BODIES = 84
EXPECTED_PHONE_VALUES = 84
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 85
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
        "imkassandreias.gr", "www.imkassandreias.gr",
        "ec-patr.org", "www.ec-patr.org",
        "e-nomothesia.gr", "www.e-nomothesia.gr",
        "ecclesia.gr", "www.ecclesia.gr",
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
        raise ValueError("Kassandreia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kassandreia candidate ledger date drifted")
    expected_summary = {
        PARENT: 85,
        "total": 85,
        "exact_current_parish_rows": 78,
        "monastery_kind_rows": 7,
        "parish_kind_rows": 78,
        "contact_bodies": 84,
        "phone_bodies": 84,
        "public_phone_values": 84,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 85,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Kassandreia ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Kassandreia ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kassandreia ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Kassandreia ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Kassandreia ledger has duplicate candidate ids")
    if FORBIDDEN_PUNCTUATION.search(
            json.dumps(ledger, ensure_ascii=False)):
        raise ValueError("Kassandreia ledger has forbidden punctuation")
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
        raise ValueError("Kassandreia English name coverage drifted")
    if set(ENGLISH_SEATS) != {
            item["seat"] for item in result if item.get("seat")}:
        raise ValueError("Kassandreia English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Kassandreia parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Kassandreia kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Kassandreia rank totals drifted: %r" %
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
        raise ValueError("Kassandreia contact coverage drifted: %r" %
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


class RosterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif self.table is not None and tag == "tr":
            self.row = []
        elif self.row is not None and tag in ("td", "th"):
            self.cell = []
        elif self.cell is not None and tag in ("br", "p", "div"):
            self.cell.append(" ")

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            value = html.unescape("".join(self.cell)).replace("\u00a0", " ")
            self.row.append(re.sub(r"\s+", " ", value).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_source(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=60) as response:
        if response.status >= 400:
            raise ValueError("%s returned HTTP %s" % (url, response.status))
        return (
            response.headers.get("Content-Type", "").lower(),
            response.read(),
        )


def check_live_sources():
    content_type, payload = fetch_source(ROSTER_PAGE)
    if "html" not in content_type:
        raise ValueError("current roster returned a non-HTML response")
    parser = RosterParser()
    parser.feed(payload.decode("utf-8", "replace"))
    candidates = [table for table in parser.tables if len(table) == 79]
    if len(candidates) != 1 or candidates[0][0][:2] != [
            "Περιοχή", "Ιερός Ναός"]:
        raise ValueError("current roster table shape drifted")
    actual = [tuple((row[0], row[1], row[3]))
              for row in candidates[0][1:]]
    if actual != LIVE_ROSTER_ROWS:
        for index, pair in enumerate(zip(actual, LIVE_ROSTER_ROWS), 1):
            if pair[0] != pair[1]:
                raise ValueError(
                    "current roster row %d drifted: %r != %r" %
                    (index, pair[0], pair[1])
                )
        raise ValueError("current roster count drifted")

    content_type, payload = fetch_source(MONASTERIES_PAGE)
    if "html" not in content_type:
        raise ValueError("monastery roster returned a non-HTML response")
    monastery_text = normalize_source_text(
        payload.decode("utf-8", "replace")
    )
    for row_id, markers in MONASTIC_LIVE_MARKERS.items():
        if any(normalize_source_text(marker) not in monastery_text
               for marker in markers):
            raise ValueError("monastery source marker drifted for %s" % row_id)

    content_type, payload = fetch_source(PATRIARCHATE_PAGE)
    if "html" not in content_type:
        raise ValueError("Patriarchate profile returned a non-HTML response")
    patriarchate_text = normalize_source_text(
        payload.decode("utf-8", "replace")
    )
    for marker in ("Ἐνοριακοί Ναοί· 79", "Ἱεραί Μοναί"):
        if normalize_source_text(marker) not in patriarchate_text:
            raise ValueError("Patriarchate reconciliation marker drifted")

    content_type, payload = fetch_source(LEGAL_PAGE)
    if "html" not in content_type:
        raise ValueError("legal roster returned a non-HTML response")
    legal_text = normalize_source_text(payload.decode("utf-8", "replace"))
    for marker in (
        "Συνολικός αριθμός Ενοριών: 79",
        "Τριάδιον",
        "Νέα Όλυνθος",
    ):
        if normalize_source_text(marker) not in legal_text:
            raise ValueError("legal roster reconciliation marker drifted")

    content_type, payload = fetch_source(CHURCH_OF_GREECE_PDF)
    if "pdf" not in content_type or not payload.startswith(b"%PDF"):
        raise ValueError("Church of Greece bulletin is not a valid PDF")


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
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Kassandreia: %d exact named bodies; %d carry current public "
            "body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Kassandreia: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
