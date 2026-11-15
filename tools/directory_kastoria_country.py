#!/usr/bin/env python3
"""Validate exact named Kastoria bodies from current first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_kastoria_country.py --check
    python tools/directory_kastoria_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "kastoria_country.json"
)
PARENT = "ep-kastoria"
ADMIN_PAGE = "https://www.imkastorias.gr/dioikitiki-diarthrosi/"
MONASTERY_PAGE = "https://www.imkastorias.gr/ieres-mones/"
CHAPEL_PAGE = (
    "https://www.imkastorias.gr/"
    "parekklisia-byzantini-kai-metabyzantina/"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-kastorias/"
)
PARASKEVI_SITE = "https://www.imk-agparaskeve.gr/"


PARISH_GROUPS = [
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/01-arxieratiki-perifereia-kastorias/"
        ),
        "modified": "2023-09-13T13:30:20",
        "rows": r'''
Καστοριά|52100|Κοίμ. Θεοτόκου (Μητροπολιτικός)
Καστοριά|52100|Αγ. Γεώργιος
Καστοριά|52100|Αγ. Κων/νος & Ελένη
Καστοριά|52100|Άγ. Πάντες
Καστοριά|52100|Άγιος Νικάνωρ
Απόσκεπος|52100|Κοίμ. Θεοτόκου
Κεφαλάριον|52100|Όσιος Ναούμ
Σιδηροχώριον|52100|Άγ. Αθανάσιος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/"
            "02-arxieratiki-perifereia-argous-orestikou/"
        ),
        "modified": "2023-09-13T13:31:23",
        "rows": r'''
Αμμουδάρα|52200|Άγ. Νικόλαος
Αμπελόκηποι|52100|Κοίμ. Θεοτόκου
Αμπελοχώριον|52200|Αγ. Σπυρίδων
Άργος Ορεστικόν|52200|Άγ. Νεκτάριος
Άργος Ορεστικόν|52200|Αγ. Παρασκευή
Ασπροκκλησιά|52200|Άγ. Αθανάσιος
Ασπρονέριον|52200|Προφ. Hλίας
Βοτάνιον|52200|Τίμ. Πρόδρομος
Δισπηλιόν|52200|Άγ. Νικόλαος
Κρεμαστόν|52200|Άγ. Αθανάσιος
Κωσταράζιον|52200|Άγ. Δημήτριος
Μηλίτσα|52200|Άγ. Δημήτριος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/03-arxieratiki-perifereia-korissou/"
        ),
        "modified": "2023-09-13T13:32:49",
        "rows": r'''
Βασιλειάδα|52052|Εισόδια Θεοτόκου
Βέργα|52052|Κοίμ. Θεοτόκου
Γέρμα|52200|Άγ. Γεώργιος
Κορησσός|52052|Κοίμ. Θεοτόκου
Κλεισούρα|52054|Άγ. Δημήτριος
Κλεισούρα|52054|Άγ. Νικόλαος
Λιθιά Άνω|52052|Ἅγ. Δημήτριος
Λιθιά Κάτω|52052|Κοίμ. Θεοτόκου
Μαυροχώριον|52056|Αγ. Βαρβάρα
Μελισσότοπος|52052|Ἅγ. Ἀθανάσιος
Πολυκάρπη|52056|Αγ. Βαρβάρα
Σταυροπόταμος|52052|Αγ. Τριάς
Τσιρίλοβο|52052|Άγ. Νικόλαος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/04-arxieratiki-perifereia-aetou/"
        ),
        "modified": "2023-09-13T13:34:15",
        "rows": r'''
Αετός|53075|Άγ. Γεώργιος
Αγραπιδέα|53075|Άγ. Χαράλαμπος
Ασπρόγεια|53075|Μετ. Σωτήρος
Βαλτόνερα|53200|Αγ. Κων/νος & Ελένη
Βαρυκό|52054|Άγ. Δημήτριος
Λέχοβο|53076|Άγ. Δημήτριος
Λιμνοχώριον|53200|Κοιμ. Θεοτόκου
Νυμφαίον|53078|Άγ. Νικόλαος
Πεδινόν|53200|Άγ. Γεώργιος
Σκλήθρον|53075|Άγ. Γεώργιος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/05-arxieratiki-perifereia-toixiou/"
        ),
        "modified": "2023-09-13T13:36:19",
        "rows": r'''
Βυσσινέα|52100|Άγ. Νικόλαος
Μεταμόρφωση|52100|Μεταμ. Σωτήρος
Οξυά|52100|Άγ. Κων/νος & Ελένη
Ποιμενικό|52100|Άγ. Γεώργιος
Πολυκέρασος|52100|Άγ. Νικόλαος
Τοιχιό|52100|Κοίμ. Θεοτόκου
Φωτεινή|52100|Κοίμ. Θεοτόκου
Περικοπή|52100|Κοίμ. Θεοτόκου
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/06-arxieratiki-perifereia-pentavrysou/"
        ),
        "modified": "2023-09-13T13:37:35",
        "rows": r'''
Αυγή|52200|Άγ. Δημήτριος
Ομορφοκκλησιά|52200|Άγ. Γεώργιος
Πεντάβρυσος|52200|Κοίμ. Θεοτόκου
Ποριά|52200|Άγ. Παρασκευή
Τσάκωνη|52200|Κοίμ. Θεοτόκου
Υψηλόν|52200|Άγ. Νικόλαος
Χιλιόδενδρον|52200|Γεν. Θεοτόκου
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/07-arxieratiki-perifereia-koresteion/"
        ),
        "modified": "2023-09-13T13:38:53",
        "rows": r'''
Άγ. Αντώνιος|52055|Άγ. Αντώνιος
Ανταρτικόν|53076|Άγ. Νικόλαος
Βατοχώριον|53076|Άγ. Νικόλαος
Γάβρος|52055|Άγ. Νικόλαος
Κρανιώνα|52055|Άγ. Δημήτριος
Κρυσταλλοπηγή|53076|Άγ. Γεώργιος
Κώττας|53076|Κοίμ. Θεοτόκου
Μακροχώριον|52055|Άγ. Νικόλαος
Μαυρόκαμπος|52055|Άγ. Δημήτριος
Μελάς|52055|Άγ. Ευστάθιος
Πράσινο|53076|Άγ. Γεώργιος
Τρίγωνο|53076|Άγ. Νικόλαος
Χαλάρα|52055|Άγ. Νικόλαος
Κορυφή|52055|Άγ. Νικόλαος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/08-arxieratiki-perifereia-laxanokipon/"
        ),
        "modified": "2020-02-20T12:30:33",
        "rows": r'''
Βράχος|52200|Κοίμ. Θεοτόκου
Ζευγοστάσιον|52200|Κοίμ Θεοτόκου
Καστανόφυτον|52200|Κοίμ. Θεοτόκου
Κρύα Νερά|52200|Κοίμ. Θεοτόκου
Λακκώματα|52200|Ευαγγ. Θεοτόκου
Λαχανόκηποι|52200|Άγ. Αθανάσιος
Λάγγα|52200|Άγ. Νικόλαος
Μελάνθιον|52200|Κοίμ. Θεότοκου
Νίκη|52200|Άγ. Γεώργιος
Περιβόλια Άνω|52200|Άγ. Αθανάσιος
Περιβόλια Κάτω|52200|Άγ. Δημήτριος
Σπήλαια|52200|Άγ. Κυριακή
Πετροπουλάκι|52200|Άγ. Νικόλαος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/09-arxieratiki-perifereia-mesopotamias/"
        ),
        "modified": "2020-03-12T09:44:17",
        "rows": r'''
Αγ. Κυριακή|52050|Αγ. Κυριακή
Δενδροχώριον|52050|Άγ. Νικόλαος
Ν. Ζούζουλη|52050|Άγ. Γεώργιος
Ιεροπηγή|52050|Αγ. Παρασκευή
Καλοχώριον|52050|Άγ. Νικόλαος
Κολοκυνθού|52050|Άγ. Νικόλαος
Κορομηλέα|52100|Ύψ. Τιμίου Σταυρού
Λεύκη|52100|Αγ. Τριάς
Μανιάκοι|52100|Αγ. Παρασκευή
Μεσοποταμία|52050|Άγ. Κων/νος & Ελένη
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/10-arxieratiki-perifereia-dipotamias/"
        ),
        "modified": "2020-03-12T09:45:17",
        "rows": r'''
Ακόντιον|52050|Κοίμ. Θεότοκου
Διποταμία|52050|Κοίμ. Θεοτόκου
Καλή Βρύση|52050|Άγ. Δημήτριος
Κομνηνάδες|52050|Γεν. Θεοτόκου
Μεσόβραχος|52050|Άγ. Γεώργιος
Οινόη|52050|Κοίμ. Θεοτόκου
Πολυάνεμος|52050|Αγ. Ματρώνα
Πτεριά Άνω|52050|Άγ. Γεώργιος
Πτεριά Κάτω|52050|Κοίμ. Θεοτόκου
Χιονάτον|52050|Άγ. Νικόλαος
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/11-arxieratiki-perifereia-nestoriou/"
        ),
        "modified": "2020-03-12T09:45:47",
        "rows": r'''
Αγία Άννα|52051|Κοίμ. Θεοτόκου
Γιαννοχώρι|52051|Κοίμ. Θεοτόκου
Γράμμος|52051|Κοίμ. Θεοτόκου
Κρανοχώριον|52051|Άγ. Ανάργυροι
Κοτύλη|52051|Άγ. Γεώργιος
Κυψέλη|52051|Αγ. Παρασκευή
Λιβαδοτόπι|52051|Άγ. Νικόλαος
Μονόπυλον|52051|Αγ. Ματρώνα
Νεστόριον Άνω|52051|Παμμ. Ταξιάρχαι
Νεστόριον Κάτω|52051|Κοίμ. Θεοτόκου
Πεύκον|52051|Αγ. Παρασκευή
Πτελέα|52051|Άγ. Δημήτριος
Σλημνήτσα|52051|Κοίμ. Θεοτόκου
Στενά|52051|Κοίμ. Θεοτόκου
''',
    },
    {
        "url": (
            "https://www.imkastorias.gr/arxeio-arthron/"
            "arxieratikes-perifereies/12-arxieratiki-perifereia-eptaxoriou/"
        ),
        "modified": "2020-03-12T09:46:41",
        "rows": r'''
Επταχώριον|50007|Αγ. Παρασκευή
Ζούζουλη|50007|Άγ. Γεώργιος
Πευκόφυτον|50007|Κοίμ. Θεοτόκου
Χρυσή|50007|Μεταμ. Σωτήρος
''',
    },
]


DEDICATIONS = {
    "Άγ. Αθανάσιος": "Saint Athanasius",
    "Άγ. Ανάργυροι": "Holy Unmercenaries",
    "Άγ. Αντώνιος": "Saint Anthony",
    "Άγ. Γεώργιος": "Saint George",
    "Άγ. Δημήτριος": "Saint Demetrius",
    "Άγ. Ευστάθιος": "Saint Eustathius",
    "Άγ. Κυριακή": "Saint Kyriaki",
    "Άγ. Κων/νος & Ελένη": "Saints Constantine and Helen",
    "Άγ. Νεκτάριος": "Saint Nectarios",
    "Άγ. Νικόλαος": "Saint Nicholas",
    "Άγ. Πάντες": "All Saints",
    "Άγ. Παρασκευή": "Saint Paraskevi",
    "Άγ. Χαράλαμπος": "Saint Charalambos",
    "Άγιος Νικάνωρ": "Saint Nicanor",
    "Όσιος Ναούμ": "Venerable Naum",
    "Ύψ. Τιμίου Σταυρού": "Exaltation of the Holy Cross",
    "Αγ. Βαρβάρα": "Saint Barbara",
    "Αγ. Γεώργιος": "Saint George",
    "Αγ. Κυριακή": "Saint Kyriaki",
    "Αγ. Κων/νος & Ελένη": "Saints Constantine and Helen",
    "Αγ. Ματρώνα": "Saint Matrona",
    "Αγ. Παρασκευή": "Saint Paraskevi",
    "Αγ. Σπυρίδων": "Saint Spyridon",
    "Αγ. Τριάς": "Holy Trinity",
    "Γεν. Θεοτόκου": "Nativity of the Theotokos",
    "Εισόδια Θεοτόκου": "Entry of the Theotokos",
    "Ευαγγ. Θεοτόκου": "Annunciation of the Theotokos",
    "Κοίμ Θεοτόκου": "Dormition of the Theotokos",
    "Κοίμ. Θεοτόκου": "Dormition of the Theotokos",
    "Κοίμ. Θεοτόκου (Μητροπολιτικός)": "Dormition of the Theotokos",
    "Κοίμ. Θεότοκου": "Dormition of the Theotokos",
    "Κοιμ. Θεοτόκου": "Dormition of the Theotokos",
    "Μετ. Σωτήρος": "Transfiguration of the Savior",
    "Μεταμ. Σωτήρος": "Transfiguration of the Savior",
    "Παμμ. Ταξιάρχαι": "Holy Archangels",
    "Προφ. Hλίας": "Prophet Elijah",
    "Τίμ. Πρόδρομος": "Saint John the Forerunner",
    "Ἅγ. Δημήτριος": "Saint Demetrius",
    "Ἅγ. Ἀθανάσιος": "Saint Athanasius",
}


PARISH_CONTACTS = r'''
Καστοριά|Κοίμ. Θεοτόκου (Μητροπολιτικός)|24670 28970,26470 24081,24670 26250
Καστοριά|Αγ. Γεώργιος|24670 28903,24670 26113
Καστοριά|Αγ. Κων/νος & Ελένη|24670 83676,24670 85877
Καστοριά|Άγ. Πάντες|24670 76005
Καστοριά|Άγιος Νικάνωρ|24670 27037
Απόσκεπος|Κοίμ. Θεοτόκου|24670 22982
Κεφαλάριον|Όσιος Ναούμ|24670 71036
Αμπελόκηποι|Κοίμ. Θεοτόκου|24670 61886
Αμπελοχώριον|Αγ. Σπυρίδων|24670 43614
Άργος Ορεστικόν|Άγ. Νεκτάριος|24670 44403,24670 44452
Άργος Ορεστικόν|Αγ. Παρασκευή|24670 42303,24670 41473,24670 22409
Δισπηλιόν|Άγ. Νικόλαος|24670 85295
Κωσταράζιον|Άγ. Δημήτριος|24670 73443
Μηλίτσα|Άγ. Δημήτριος|24670 73070
Βασιλειάδα|Εισόδια Θεοτόκου|6978796967
Γέρμα|Άγ. Γεώργιος|6933403099
Κορησσός|Κοίμ. Θεοτόκου|24670 51380
Κλεισούρα|Άγ. Νικόλαος|6948523844
Λιθιά Κάτω|Κοίμ. Θεοτόκου|24670 85839
Μαυροχώριον|Αγ. Βαρβάρα|24670 74619,24670 74028
Πολυκάρπη|Αγ. Βαρβάρα|24670 74555
Αετός|Άγ. Γεώργιος|23860 41571
Βαρυκό|Άγ. Δημήτριος|24670 26179
Λέχοβο|Άγ. Δημήτριος|24630 82438
Λιμνοχώριον|Κοιμ. Θεοτόκου|24630 41237
Νυμφαίον|Άγ. Νικόλαος|24630 31384
Πεδινόν|Άγ. Γεώργιος|6973184767
Σκλήθρον|Άγ. Γεώργιος|24630 31300
Βυσσινέα|Άγ. Νικόλαος|24670 21170
Πολυκέρασος|Άγ. Νικόλαος|24670 98309
Τοιχιό|Κοίμ. Θεοτόκου|24670 72212
Φωτεινή|Κοίμ. Θεοτόκου|24670 72156
Αυγή|Άγ. Δημήτριος|24670 71110
Ομορφοκκλησιά|Άγ. Γεώργιος|24670 97316
Πεντάβρυσος|Κοίμ. Θεοτόκου|24670 97385
Ποριά|Άγ. Παρασκευή|24670 71101
Τσάκωνη|Κοίμ. Θεοτόκου|24670 97316
Χιλιόδενδρον|Γεν. Θεοτόκου|6936934551
Άγ. Αντώνιος|Άγ. Αντώνιος|24670 33012
Βατοχώριον|Άγ. Νικόλαος|24670 28394
Κρυσταλλοπηγή|Άγ. Γεώργιος|24670 86043
Μελάς|Άγ. Ευστάθιος|24670 86062
Λακκώματα|Ευαγγ. Θεοτόκου|6980727642
Λαχανόκηποι|Άγ. Αθανάσιος|24673 00350
Λάγγα|Άγ. Νικόλαος|24673 00850
Μελάνθιον|Κοίμ. Θεότοκου|24670 24946
Νίκη|Άγ. Γεώργιος|24670 61759
Αγ. Κυριακή|Αγ. Κυριακή|24670 61195
Δενδροχώριον|Άγ. Νικόλαος|24670 81095
Ν. Ζούζουλη|Άγ. Γεώργιος|24670 26482
Ιεροπηγή|Αγ. Παρασκευή|24670 91491
Καλοχώριον|Άγ. Νικόλαος|6984144794
Κολοκυνθού|Άγ. Νικόλαος|24670 71645
Μανιάκοι|Αγ. Παρασκευή|6945162742
Μεσοποταμία|Άγ. Κων/νος & Ελένη|24670 61264
Διποταμία|Κοίμ. Θεοτόκου|24670 91229
Κομνηνάδες|Γεν. Θεοτόκου|24670 91331
Οινόη|Κοίμ. Θεοτόκου|24670 72167
Πτεριά Άνω|Άγ. Γεώργιος|24670 92476
Χιονάτον|Άγ. Νικόλαος|24670 91326
Κοτύλη|Άγ. Γεώργιος|24670 86734
Νεστόριον Άνω|Παμμ. Ταξιάρχαι|24670 31025
Πευκόφυτον|Κοίμ. Θεοτόκου|6979135438
Χρυσή|Μεταμ. Σωτήρος|24670 84203
'''


CHAPEL_ROWS = r'''
Αγ. Αθανασίου|Saint Athanasius|Kastoria|Chapel|
Αγ. Νικολάου (Ομονοίας)|Saint Nicholas at Omonoia|Kastoria|Chapel|
Αγ. Νικολάου (Καραβιδά)|Saint Nicholas Karavidas|Kastoria|Chapel|
Αγ. Νικολάου (Ρέζα)|Saint Nicholas Reza|Kastoria|Chapel|
Αγ. Νικολάου (Τσίντσιρα)|Saint Nicholas Tsintsiras|Kastoria|Chapel|
Αγ. Νικολάου (Λιάνου)|Saint Nicholas Lianos|Kastoria|Chapel|
Αγ. Νικολάου (Πασσά)|Saint Nicholas Passas|Kastoria|Chapel|
Αγ. Νικολάου (Σκαπέρδα)|Saint Nicholas Skaperdas|Kastoria|Chapel|
Αγ. Αναργύρων (Ζάχου)|Holy Unmercenaries Zachos|Kastoria|Chapel|
Αγ. Αναργύρων (Γυμνασίου)|Holy Unmercenaries at the Gymnasium|Kastoria|Chapel|
Κοιμ. Θεοτόκου (Κουμπελίδικη)|Dormition of the Theotokos, Koumpelidiki|Kastoria|Chapel|
Κοιμ. Θεοτόκου (Ξενία)|Dormition of the Theotokos at Xenia|Kastoria|Chapel|
Αγ. Αθανασίου (Ξενία)|Saint Athanasius at Xenia|Kastoria|Chapel|
Αγ. Αθανασίου (Μητροπόλεως)|Saint Athanasius at the Metropolis|Kastoria|Chapel|
Αγ. Παρασκευής (Ξενία)|Saint Paraskevi at Xenia|Kastoria|Chapel|
Αγ. Παρασκευής (Ντολτσού)|Saint Paraskevi at Doltsos|Kastoria|Chapel|
Αγ. Ανδρέου (Ντολτσού)|Saint Andrew at Doltsos|Kastoria|Chapel|
Ζωοδ. Πηγής (Εβραΐδος)|Life-Giving Spring, Evraidos|Kastoria|Chapel|
Αγ. Πέτρου και Παύλου (Τελωνείου)|Saints Peter and Paul at the Customs House|Kastoria|Chapel|
Αγ. Αλυπίου|Saint Alypius|Kastoria|Chapel|
Εισοδ. Θεοτόκου (Επιμελητηρίου)|Entry of the Theotokos at the Chamber of Commerce|Kastoria|Chapel|
Τιμ. Προδρόμου (Ομονοίας)|Saint John the Forerunner at Omonoia|Kastoria|Chapel|
Γεν. Θεοτόκου (Παπαδάμου)|Nativity of the Theotokos, Papadamos|Kastoria|Chapel|
Αγ. Δημητρίου (Ταλίδη)|Saint Demetrius Talidis|Kastoria|Chapel|
Αγ. Τριών (Πλατ. Μητροπόλεως)|Three Hierarchs at Metropolis Square|Kastoria|Chapel|
Παμμ. Ταξιαρχών (Γυμνασίου)|Holy Archangels at the Gymnasium|Kastoria|Chapel|
Παμμ. Ταξιαρχών (Μητροπόλεως)|Holy Archangels at the Metropolis|Kastoria|Chapel|
Αγ. Νικολάου και Χαραλάμπους (Υψηλάντη)|Saints Nicholas and Charalambos on Ypsilanti|Kastoria|Chapel|
Αγ. Ανδρέου|Saint Andrew|Kastoria|Chapel|
Αγ. Νικολάου και Ελευθερίου|Saints Nicholas and Eleutherius|Kastoria|Chapel|
Αγ. Πέτρου και Παύλου|Saints Peter and Paul|Kastoria|Chapel|
Παναγίας της Ελεούσης|Panagia Eleousa|Kastoria|Chapel|
Αγ. Γεωργίου (Λιμπάνια)|Saint George at Limbania|Kastoria|Chapel|
Παναγίας του Μοζεμβίκη (Αγ. Μηνά)|Panagia of Mozemvikis and Saint Menas|Kastoria|Chapel|
Παναγίας Βλαχερνών|Panagia Blachernae|Kastoria|Chapel|
Αγ. Αποστόλων των Δώδεκα|Twelve Apostles|Kastoria|Chapel|
Αγ. Ιωάννου του Θεολόγου|Saint John the Theologian|Kastoria|Chapel|
Αγ. Αποστόλου Θωμά|Apostle Thomas|Kastoria|Chapel|
Αγ. Νικολάου (Τράιτσε)|Saint Nicholas Traitce|Kastoria|Chapel|
Αγ. Στυλιανού|Saint Stylianos|Kastoria|Chapel|
Αγ. Στεφάνου|Saint Stephen|Kastoria|Chapel|
Αγ. Γεωργίου (Πολιτείας)|Saint George at Politeia|Kastoria|Chapel|
Αγ. Κυριακής|Saint Kyriaki|Kastoria|Chapel|
Αγ. Αθανασίου|Saint Athanasius|Kastoria|Chapel|
Αγ. Δημητρίου (Γκολογκίνα)|Saint Demetrius Gkologkina|Kastoria|Chapel|
Αγ. Δημητρίου (Κίτσιου)|Saint Demetrius Kitsiou|Kastoria|Chapel|
Αγ. Αναργύρων|Holy Unmercenaries|Kastoria|Chapel|
Αγ. Νικολάου (Χατζηγιάννη)|Saint Nicholas Chatzigiannis|Kastoria|Chapel|
Αγ. Θεοδώρων|Holy Theodore Martyrs|Kastoria|Chapel|
Αγ. Γεωργίου (Νανά)|Saint George Nanas|Kastoria|Chapel|
Αγ. Παντελεήμονος|Saint Panteleimon|Kastoria|Chapel|
Εισόδια Θεοτόκου|Entry of the Theotokos|Kastoria|Chapel|
Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Kastoria|Chapel|
Αγ. Νικολάου (Τζώτζα)|Saint Nicholas Tzotzas|Kastoria|Chapel|
Αγ. Λουκά|Saint Luke|Kastoria|Chapel|
Τιμ. Προδρόμου (Απόζαρι)|Saint John the Forerunner at Apozari|Kastoria|Chapel|
Παμμ. Ταξιαρχών (Απόζαρι)|Holy Archangels at Apozari|Kastoria|Chapel|
Παναγίας Φανερωμένης|Panagia Phaneromeni|Kastoria|Chapel|
Αγίας Βαρβάρας|Saint Barbara|Kastoria|Chapel|
Αγίου Σπυρίδωνος|Saint Spyridon|Kastoria|Chapel|
Άγιος Τρύφων - Νέα Λεύκη|Saint Tryphon|Nea Lefki|Chapel|24670 81149
Αγ. Παντελεήμων - Νομαρχιακό Νοσοκομείο Καστοριάς|Saint Panteleimon at Kastoria General Hospital|Kastoria|Chapel|
Άγιος Αθανάσιος - Θέση Βουνό πόλεως Καστοριάς|Saint Athanasius at Vouno|Kastoria|Chapel|
Άγιος Λάζαρος - Γηροκομείο|Saint Lazarus at the Nursing Home|Kastoria|Chapel|
Άγιος Γεώργιος - Καστοριά (Πεζικό)|Saint George, Infantry|Kastoria|Military Chapel|
Αγία Βαρβάρα - Άργος Ορεστικό (Πυροβολικό)|Saint Barbara, Artillery|Argos Orestiko|Military Chapel|
Προφήτης Ηλίας - Βίτσι (Αεροπορία)|Prophet Elijah, Air Force|Vitsi|Military Chapel|
'''


MONASTERY_ROWS = [
    ("Κοιμήσεως Θεοτόκου - Παναγία Μαυριώτισσα",
     "Panagia Mavriotissa", "Kastoria", "24670 22714"),
    ("Αγίων Αναργύρων Μελισσοτόπου", "Holy Unmercenaries",
     "Melissotopos", "24670 98309"),
    ("Αγίας Παρασκευής Βασιλειάδος", "Saint Paraskevi",
     "Vasileiada", "24670 98298"),
    ("Αγίου Γεωργίου Επταχωρίου", "Saint George",
     "Eptachori", "24670 85584"),
    ("Ιερά Μονή Γενεθλίου της Θεοτόκου Κλεισούρας",
     "Nativity of the Theotokos", "Kleisoura", "24630 94330"),
    ("Αγίου Νικολάου Τσιριλόβου", "Saint Nicholas",
     "Tsirilovo", "24670 51228"),
    ("Παναγίας Φανερωμένης", "Panagia Phaneromeni",
     "Agia Kyriaki", "24670 62128"),
    ("Ιερά Μονή Αγίου Γεωργίου Μελανθίου", "Saint George",
     "Melanthio", ""),
]


SEAT_OVERRIDES = {
    "Αγ. Κυριακή": "Agia Kyriaki",
    "Άγ. Αντώνιος": "Agios Antonios",
    "Ν. Ζούζουλη": "Nea Zouzouli",
}
GREEK_MAP = {
    "Α": "A", "Β": "V", "Γ": "G", "Δ": "D", "Ε": "E",
    "Ζ": "Z", "Η": "I", "Θ": "Th", "Ι": "I", "Κ": "K",
    "Λ": "L", "Μ": "M", "Ν": "N", "Ξ": "X", "Ο": "O",
    "Π": "P", "Ρ": "R", "Σ": "S", "Τ": "T", "Υ": "Y",
    "Φ": "F", "Χ": "Ch", "Ψ": "Ps", "Ω": "O",
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}


def transliterate(value):
    if value in SEAT_OVERRIDES:
        return SEAT_OVERRIDES[value]
    plain = "".join(
        char for char in unicodedata.normalize("NFD", value)
        if unicodedata.category(char) != "Mn"
    )
    return "".join(GREEK_MAP.get(char, char) for char in plain)


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


def make_name(dedication, rank, seat, context=""):
    if context:
        return "%s of %s, %s, %s" % (rank, dedication, context, seat)
    return "%s of %s, %s" % (rank, dedication, seat)


def parse_contacts():
    result = {}
    for raw in PARISH_CONTACTS.strip().splitlines():
        seat, temple, values = raw.split("|", 2)
        key = (seat, temple)
        if key in result:
            raise ValueError("duplicate Kastoria contact key: %r" % (key,))
        result[key] = values.split(",")
    return result


def build_rows():
    contacts = parse_contacts()
    used_contacts = set()
    rows = []
    index = 0
    for group in PARISH_GROUPS:
        for raw in group["rows"].strip().splitlines():
            greek_seat, postal_code, temple = raw.split("|", 2)
            dedication = DEDICATIONS.get(temple)
            if not dedication:
                raise ValueError("untranslated Kastoria dedication: %s" % temple)
            seat = transliterate(greek_seat)
            rank = (
                "Metropolitan Cathedral"
                if temple == "Κοίμ. Θεοτόκου (Μητροπολιτικός)"
                else "Parish Church"
            )
            name = make_name(dedication, rank, seat)
            index += 1
            item = {
                "id": "gr-ep-kastoria-%03d-%s" % (index, slug(name)),
                "parent": PARENT,
                "kind": "parish",
                "rank": rank,
                "name": name,
                "local": "%s, %s" % (temple, greek_seat),
                "seat": seat,
                "country": "GR",
                "address": [greek_seat, postal_code, "Greece"],
                "sources": [group["url"]],
            }
            contact_key = (greek_seat, temple)
            if contact_key in contacts:
                item["phones"] = contacts[contact_key]
                item["contact_sources"] = [group["url"]]
                item["contact_checked"] = CHECKED
                used_contacts.add(contact_key)
            if contact_key == ("Άργος Ορεστικόν", "Αγ. Παρασκευή"):
                item["site"] = PARASKEVI_SITE
            rows.append(item)
    if used_contacts != set(contacts):
        missing = sorted(set(contacts) - used_contacts)
        raise ValueError("unused Kastoria parish contacts: %r" % missing)
    chapel_lines = CHAPEL_ROWS.strip().splitlines()
    if len(chapel_lines) != 67:
        raise ValueError("expected 67 exact chapel rows")
    for offset, raw in enumerate(chapel_lines):
        local, dedication, seat, rank, phone = raw.split("|", 4)
        context = ""
        if offset < 28:
            context = "Dormition Parish"
        elif offset < 60:
            context = "Saint George Parish"
        name = make_name(dedication, rank, seat, context)
        local_name = local
        if context == "Dormition Parish":
            local_name = "%s, Α΄ Ενορία Κοιμήσεως Θεοτόκου" % local
        elif context == "Saint George Parish":
            local_name = "%s, Β΄ Ενορία Αγίου Γεωργίου" % local
        index += 1
        item = {
            "id": "gr-ep-kastoria-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local_name,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [CHAPEL_PAGE],
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [CHAPEL_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)
    for local, dedication, seat, phone in MONASTERY_ROWS:
        rank = "Monastery"
        name = make_name(dedication, rank, seat)
        index += 1
        item = {
            "id": "gr-ep-kastoria-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [MONASTERY_PAGE],
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [MONASTERY_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 198
EXPECTED_OWNER_COUNTS = {PARENT: 198}
EXPECTED_KINDS = {"monastery": 8, "parish": 190}
EXPECTED_RANKS = {
    "Chapel": 64,
    "Metropolitan Cathedral": 1,
    "Military Chapel": 3,
    "Monastery": 8,
    "Parish Church": 122,
}
EXPECTED_CONTACT_BODIES = 72
EXPECTED_PHONE_BODIES = 72
EXPECTED_PHONE_VALUES = 80
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 198
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


def validate_source_url(value, label):
    parsed = urlparse(value)
    allowed = {"www.imkastorias.gr", "ec-patr.org", "www.ec-patr.org"}
    if parsed.scheme != "https" or parsed.netloc not in allowed:
        raise ValueError("%s has a non-competent source URL: %s" %
                         (label, value))


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
        validate_source_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    if item.get("site"):
        parsed = urlparse(item["site"])
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("%s has an invalid body site" % item.get("id"))
    contact_sources = list(item.get("contact_sources") or [])
    if contact_sources:
        if len(contact_sources) > 3:
            raise ValueError("%s has too many contact sources" % item.get("id"))
        for source_url in contact_sources:
            validate_source_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError(
                    "%s contact source is outside identity sources"
                    % item.get("id")
                )
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Kastoria candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kastoria candidate ledger date drifted")
    expected_summary = {
        PARENT: 198,
        "total": 198,
        "parish_kind_rows": 190,
        "monastery_kind_rows": 8,
        "contact_bodies": 72,
        "phone_bodies": 72,
        "public_phone_values": 80,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 1,
        "address_bodies": 198,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Kastoria ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Kastoria ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kastoria ledger item has invalid sources")
            for source_url in sources:
                validate_source_url(
                    source_url, entry.get("candidate_id") or key
                )
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Kastoria ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Kastoria ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Kastoria ledger has forbidden punctuation")
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
        raise ValueError("Kastoria English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Kastoria English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Kastoria parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Kastoria kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Kastoria rank totals drifted: %r" %
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
        raise ValueError("Kastoria contact coverage drifted: %r"
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
            "Kastoria: %d exact named bodies; %d carry current public "
            "contact paths" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Kastoria: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
