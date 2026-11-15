#!/usr/bin/env python3
"""Validate exact named Didymoteichon bodies from first-party rosters.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_didymoteichon_country.py --check
    python tools/directory_didymoteichon_country.py --dump
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
    / "didymoteichon_country.json"
)
PARENT = "ep-didymoteichon"
ROSTER_PAGE = (
    "https://imdos.gr/sample-page/"
    "%CE%B5%CE%BD%CE%BF%CF%81%CE%AF%CE%B5%CF%82-"
    "%CE%B5%CF%86%CE%B7%CE%BC%CE%AD%CF%81%CE%B9%CE%BF%CE%B9/"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-didymoteixoy-orestiados-soyflioy/"
)
MONASTERY_PAGE = (
    "https://imdos.gr/sample-page/"
    "%CE%BC%CE%BF%CE%BD%CE%AD%CF%82-"
    "%CE%BC%CE%B5%CF%84%CF%8C%CF%87%CE%B9%CE%B1/"
)
FEAST_PAGE = (
    "https://imdos.gr/"
    "%CF%80%CE%B1%CE%BD%CE%B7%CE%B3%CF%85%CF%81%CE%B5%CE%B9%CF%83-"
    "%CE%B9%CE%B5%CF%81%CF%89%CE%BD-"
    "%CE%BD%CE%B1%CF%89%CE%BD/"
)

ROSTERS = [
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged.png",
        "rows": [
            ("Didymoteicho", "Διδυμότειχον 683 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "25530-23120", "Metropolitan Church"),
            ("Didymoteicho", "Διδυμότειχον 683 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "25530-22808", "Parish Church"),
            ("Didymoteicho", "Διδυμότειχον 683 00", "Σωτῆρος Χριστοῦ", "Christ the Savior", "25530-23012", "Parish Church"),
            ("Didymoteicho", "Διδυμότειχον 683 00", "Ἅγ. Ἰωάννης Βατάτζης", "Saint John Vatatzes", "25533-00706", "Parish Church"),
            ("Asvestades", "Ἀσβεστάδες 683 00", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Asimenio", "Ἀσημένιον 683 00", "Ἅγ. Παρασκευή", "Saint Paraskevi", "", "Parish Church"),
            ("Ellinochori", "Ἑλληνοχώριον 683 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Evgeniko", "Εὐγενικόν 683 00", "Ἅγ. Τριάς", "Holy Trinity", "", "Parish Church"),
            ("Thyrea", "Θυρέα 683 00", "Προφ. Ἠλίας", "Prophet Elijah", "", "Parish Church"),
            ("Isaakio", "Ἰσαάκιον 683 00", "Ἀπόστ. Πέτρος & Παῦλος", "Apostles Peter and Paul", "", "Parish Church"),
            ("Karoti", "Καρωτή 683 00", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Koufovouno", "Κουφόβουνον 683 00", "Προφ. Ἠλίας", "Prophet Elijah", "", "Parish Church"),
            ("Kyani", "Κυανή 683 00", "Ἅγ. Εἰρήνη", "Saint Irene", "", "Parish Church"),
            ("Lagos", "Λαγός 683 00", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Mani", "Μάνη 683 00", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Neoi Psathades", "Νέοι Ψαθάδες 683 00", "Ἅγ. Παντελεήμων", "Saint Panteleimon", "", "Parish Church"),
            ("Petrades", "Πετράδες 683 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Poimeniko", "Ποιμενικόν 683 00", "Ἅγ. Ἀπόστολοι", "Holy Apostles", "", "Parish Church"),
            ("Prangio", "Πραγγίον 683 00", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Pythio", "Πύθιον 683 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Rigio", "Ρήγιον 683 00", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Sitaria", "Σιταριά 683 00", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Sitochori", "Σιτοχώριον 683 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Sofiko", "Σοφικόν 683 00", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged-%CE%BC%CE%B5%CF%84%CE%B1%CE%BE%CE%B1%CE%B4%CF%89%CE%BD.png",
        "rows": [
            ("Metaxades", "Μεταξάδες 680 10", "Προφ. Ἠλίας", "Prophet Elijah", "25530-51016", "Parish Church"),
            ("Alepochori", "Ἀλεποχώριον 680 10", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Asproneri", "Ἀσπρονέριον 680 10", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Vrysi", "Βρύση 680 10", "Ἅγ. Παρασκευή", "Saint Paraskevi", "", "Parish Church"),
            ("Vrysika", "Βρυσικά 683 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Giatrades", "Γιατράδες 680 10", "Προφ. Ἠλίας", "Prophet Elijah", "", "Parish Church"),
            ("Doxa", "Δόξα 680 10", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Elafochori", "Ἐλαφοχώριον 680 10", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Ladi", "Λάδη 680 10", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Paliouri", "Παλιούριον 680 10", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Polia", "Πολιά 680 10", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Savra", "Σαύρα 680 10", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Chionades", "Χιονάδες 680 10", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged-%CE%BF%CF%81%CE%B5%CF%83%CF%84%CE%B1%CE%B4%CE%B1.png",
        "rows": [
            ("Orestiada", "Ὀρεστιάς 682 00", "Ἅγ. Θεόδωροι", "Holy Theodore Martyrs", "25520-22008", "Metropolitan Church"),
            ("Orestiada", "Ὀρεστιάς 682 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "25520-22707", "Parish Church"),
            ("Orestiada", "Ὀρεστιάς 682 00", "Ἅγ. Δημήτριος", "Saint Demetrius", "25520-24277", "Parish Church"),
            ("Orestiada", "Ὀρεστιάς 682 00", "Παμμ. Ταξιάρχαι", "Holy Archangels", "25524-01022", "Parish Church"),
            ("Orestiada", "Ὀρεστιάς 682 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "25520-25114", "Parish Church"),
            ("Orestiada", "Ὀρεστιάς 682 00", "Προφ. Ἠλίας", "Prophet Elijah", "25520-29200", "Parish Church"),
            ("Orestiada", "Ὀρεστιάς 682 00", "Ἀνάστασις Κυρίου - Ἅγ. Κύριλλος", "Resurrection of the Lord and Saint Cyril", "", "Parish Church"),
            ("Ampelakia", "Ἀμπελάκια 682 00", "Ἅγ. Παντελεήμων", "Saint Panteleimon", "", "Parish Church"),
            ("Valtos", "Βάλτος 682 00", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Thourio", "Θούριον 682 00", "Θεία Ἀνάληψις", "Ascension of the Lord", "25520-31812", "Parish Church"),
            ("Lepti", "Λεπτή 682 00", "Ἅγ. Σπυρίδων", "Saint Spyridon", "25520-92251", "Parish Church"),
            ("Megali Doxipara", "Μεγάλη Δοξιπάρα 682 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Neo Chorio", "Νεοχώριον 682 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "25520-92575", "Parish Church"),
            ("Patagi", "Παταγή 682 00", "Ἅγ. Νικόλαος", "Saint Nicholas", "", "Parish Church"),
            ("Pyrgos", "Πύργος 682 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Sakkos", "Σάκκος 682 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Chandras", "Χανδράς 682 00", "Ἅγ. Ἰωάννης Πρόδρ.", "Saint John the Forerunner", "", "Parish Church"),
            ("Cheimonio", "Χειμώνιον 682 00", "Ἅγ. Ἰωάννης Πρόδρ.", "Saint John the Forerunner", "25520-31031", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/%CE%99.%CE%9C.-%CE%94%CE%99%CE%94%CE%A5%CE%9C%CE%9F%CE%A4%CE%95%CE%99%CE%A7%CE%9F%CE%A5_%CE%A4%CE%A3%CE%95%CE%A0%CE%97%CE%A3-2026-%CE%A0%CE%99%CE%9D%CE%91%CE%9A%CE%95%CE%A3_Page_07.jpg",
        "rows": [
            ("Nea Vyssa", "Νέα Βύσσα 680 01", "Ἅγ. Γεώργιος", "Saint George", "25520-71468", "Parish Church"),
            ("Nea Vyssa", "Νέα Βύσσα 680 01", "Ἅγ. Κων/νος", "Saint Constantine", "", "Parish Church"),
            ("Kavyli", "Καβύλη 682 00", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Kastanies", "Καστανιές 680 08", "Ἅγ. Γεώργιος", "Saint George", "25520-85218", "Parish Church"),
            ("Rizia", "Ρίζια 680 14", "Παμμ. Ταξιάρχαι", "Holy Archangels", "25520-94011", "Parish Church"),
            ("Sterna", "Στέρνα 682 00", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged-%CF%84%CF%81%CE%B9%CE%B3%CF%89%CE%BD%CE%BF%CF%85.png",
        "rows": [
            ("Dikaia", "Δίκαια 680 07", "Ἅγ. Δημήτριος", "Saint Demetrius", "25560-31647", "Parish Church"),
            ("Arzos", "Ἄρζος 680 07", "Ζωοδ. Πηγή", "Life-Giving Spring", "", "Parish Church"),
            ("Dilofo", "Δίλοφος 680 07", "Ἅγ. Τριάς", "Holy Trinity", "", "Parish Church"),
            ("Elaia", "Ἐλαία 680 07", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Therapeio", "Θεράπειον 680 06", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Kanadas", "Καναδάς 680 07", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Komara", "Κόμαρα 680 07", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Krios", "Κριός 680 07", "Ἅγ. Ἀνάργυροι", "Holy Unmercenaries", "", "Parish Church"),
            ("Marasia", "Μαράσια 680 07", "Μεταμόρφωσις Σωτῆρος", "Transfiguration of the Savior", "", "Parish Church"),
            ("Milia", "Μηλέα 680 06", "Ἅγ. Ἀπόστολοι", "Holy Apostles", "", "Parish Church"),
            ("Ormenio", "Ὀρμένιον 680 07", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Pali", "Πάλλη 680 07", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Pentalofos", "Πεντάλοφος 680 07", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Petrota", "Πετρωτά 680 07", "Παμμ. Ταξιάρχαι", "Holy Archangels", "", "Parish Church"),
            ("Plati", "Πλάτη 680 07", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Ptelea", "Πτελέα 680 07", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Spilaio", "Σπήλαιον 680 07", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged-%CE%9A%CF%85%CF%80%CF%81%CE%AF%CE%BD%CE%BF%CF%85.png",
        "rows": [
            ("Kyprinos", "Κυπρίνος 680 06", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Ammovouno", "Ἀμμόβουνον 680 06", "Ἅγ. Τριάς", "Holy Trinity", "", "Parish Church"),
            ("Galini", "Γαλήνη 680 06", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Zoni", "Ζώνη 680 06", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "", "Parish Church"),
            ("Keramos", "Κέραμος 680 06", "Ἅγ. Διονύσιος", "Saint Dionysius", "", "Parish Church"),
            ("Mikri Doxipara", "Μικρά Δοξιπάρα 680 06", "Ζωοδ. Πηγή", "Life-Giving Spring", "", "Parish Church"),
            ("Fylakio", "Φυλάκιον 680 06", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Chelidona", "Χελιδόνα 680 06", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged-%CE%A3%CE%BF%CF%85%CF%86%CE%BB%CE%AF%CE%B9%CE%BF%CF%85.png",
        "rows": [
            ("Soufli", "Σουφλίον 684 00", "Ἅγ. Γεώργιος", "Saint George", "25540-22272", "Metropolitan Church"),
            ("Soufli", "Σουφλίον 684 00", "Ἀπόστολος Ἀνδρέας", "Apostle Andrew", "", "Parish Church"),
            ("Soufli", "Σουφλίον 684 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "25540-22522", "Parish Church"),
            ("Giannouli", "Γιαννούλη 684 00", "Παμμ. Ταξιάρχαι", "Holy Archangels", "", "Parish Church"),
            ("Dadia", "Δαδιά 684 00", "Ἅγ. Νικόλαος", "Saint Nicholas", "25540-32228", "Parish Church"),
            ("Kornofolea", "Κορνοφωλέα 684 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Kotronia", "Κοτρωνιά 684 00", "Κοίμ. Θεοτόκου", "Dormition of the Theotokos", "", "Parish Church"),
            ("Sidiro", "Σιδηρώ 684 00", "Προφ. Ἠλίας", "Prophet Elijah", "", "Parish Church"),
        ],
    },
    {
        "source": "https://imdos.gr/wp-content/uploads/2025/07/merged-%CE%9F%CF%81%CF%86%CE%AD%CF%89%CF%82.png",
        "rows": [
            ("Lavara", "Λάβαρα 680 04", "Ἅγ. Δημήτριος", "Saint Demetrius", "25530-31561", "Parish Church"),
            ("Agriani", "Ἀγριάνη 684 00", "Ἅγ. Παρασκευή", "Saint Paraskevi", "", "Parish Church"),
            ("Amorio", "Ἀμόριον 680 04", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Kissario", "Κισσάριον 680 04", "Ἀπ. Πέτρος & Παῦλος", "Apostles Peter and Paul", "", "Parish Church"),
            ("Korymvos", "Κόρυμβος 684 00", "Παμμ. Ταξιάρχαι", "Holy Archangels", "", "Parish Church"),
            ("Kyriaki", "Κυριακή 684 00", "Ἅγ. Δημήτριος", "Saint Demetrius", "", "Parish Church"),
            ("Mandra", "Μάνδρα 684 00", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
            ("Mavrokklisi", "Μαυροκκλήσιον 684 00", "Προφ. Ἠλίας", "Prophet Elijah", "", "Parish Church"),
            ("Mega Dereio", "Μέγα Δέρειον 680 04", "Μεταμ. Σωτῆρος", "Transfiguration of the Savior", "", "Parish Church"),
            ("Mikro Dereio", "Μικρόν Δέρειον 680 04", "Ἅγ. Γεώργιος", "Saint George", "", "Parish Church"),
            ("Protokklisi", "Πρωτοκκλήσιον 684 00", "Ἅγ. Ἀθανάσιος", "Saint Athanasius", "25540-81326", "Parish Church"),
            ("Roussa", "Ρούσσα 680 04", "Ἅγ. Κων/νος & Ἑλένη", "Saints Constantine and Helen", "", "Parish Church"),
        ],
    },
]

SHRINE_SOURCE = (
    "https://imdos.gr/wp-content/uploads/2025/07/"
    "%CE%99.%CE%9C.-%CE%94%CE%99%CE%94%CE%A5%CE%9C%CE%9F%CE%A4%CE%95%CE%99%CE%A7%CE%9F%CE%A5_"
    "%CE%A4%CE%A3%CE%95%CE%A0%CE%97%CE%A3-2026-"
    "%CE%A0%CE%99%CE%9D%CE%91%CE%9A%CE%95%CE%A3_Page_12.jpg"
)

EXTRA_ROWS = [
    {
        "name": "Panagia Eleftherotria Cathedral Shrine in Didymoteicho",
        "local": "Ἱερός Καθεδρικός Προσκυνηματικός Ναός Παναγίας Ἐλευθερωτρίας Διδυμοτείχου",
        "seat": "Didymoteicho",
        "rank": "Cathedral and Shrine",
        "kind": "parish",
        "address": ["Διδυμότειχον 683 00"],
        "phones": ["25530-25284"],
        "sources": [ROSTER_PAGE, SHRINE_SOURCE],
        "contact_sources": [SHRINE_SOURCE],
    },
    {
        "name": "Saint Barbara Shrine in Orestiada",
        "local": "Ἱερός Προσκυνηματικός Ναός Ἁγίας Βαρβάρας Ὀρεστιάδος",
        "seat": "Orestiada",
        "rank": "Shrine",
        "kind": "parish",
        "address": ["Ὀρεστιάς 682 00"],
        "sources": [ROSTER_PAGE, SHRINE_SOURCE],
    },
    {
        "name": "Nativity of the Theotokos Monastery in Dadia, Soufli",
        "local": "Ἱερά Μονή Γενεθλίου Θεοτόκου Δαδιᾶς Σουφλίου",
        "seat": "Dadia, Soufli",
        "rank": "Monastery",
        "kind": "monastery",
        "address": ["684 00 Δαδιά - Σουφλίον"],
        "phones": ["25540-51361"],
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
        "contact_sources": [PATRIARCHATE_PAGE],
    },
    {
        "name": "Protection of the Theotokos and Saint Paraskevi Monastery in Nea Vyssa",
        "local": "Ἱερά Μονή Ἁγίας Σκέπης - Ἁγίας Παρασκευῆς Νέας Βύσσης",
        "seat": "Nea Vyssa",
        "rank": "Monastery",
        "kind": "monastery",
        "address": ["680 01 Νέα Βύσσα"],
        "phones": ["25520-72988"],
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
        "contact_sources": [PATRIARCHATE_PAGE],
    },
    {
        "name": "Saint Paraskevi Monastery in Didymoteicho",
        "local": "Ἱερά Μονή Ἁγίας Παρασκευῆς Διδυμοτείχου",
        "seat": "Didymoteicho",
        "rank": "Monastery",
        "kind": "monastery",
        "address": ["683 00 Διδυμότειχον"],
        "phones": ["25530-26945"],
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
        "contact_sources": [PATRIARCHATE_PAGE],
    },
    {
        "name": "Life-Giving Spring Monastery in Didymoteicho",
        "local": "Ἱερά Μονή Ζωοδόχου Πηγῆς ἐν Διδυμοτείχῳ",
        "seat": "Didymoteicho",
        "rank": "Monastery",
        "kind": "monastery",
        "address": ["683 00 Διδυμότειχον"],
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE, "https://imdos.gr/2026/05/04/%CE%B1%CF%81%CF%87%CE%BF%CE%BC%CE%AD%CE%BD%CE%BF%CF%85-%CF%84%CE%BF%CF%85-%CE%BC%CE%B7%CE%BD%CF%8C%CF%82-%CE%BC%CE%B1%CE%90%CE%BF%CF%85/"],
    },
    {
        "name": "Holy Forty Virgin Martyrs Cemetery Church in Orestiada",
        "local": "Νέος Κοιμητηριακός Ναός Ἁγίων Τεσσαράκοντα Παρθένων Ὀρεστιάδος",
        "seat": "Orestiada",
        "rank": "Cemetery Church",
        "kind": "parish",
        "address": ["Ὀρεστιάδα"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Holy Forty Virgin Martyrs Chapel in Petrota",
        "local": "Παρεκκλήσιον Ἁγίων Τεσσαράκοντα Παρθένων Πετρωτῶν",
        "seat": "Petrota",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Πετρωτά"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Unburnt Bush Chapel in Mikro Dereio",
        "local": "Ἱερό Παρεκκλήσιο Ἀκαταφλέκτου Βάτου Μικροῦ Δερείου",
        "seat": "Mikro Dereio",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Μικρό Δέρειο"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Sozon Cemetery Chapel in Metaxades",
        "local": "Κοιμητηριακόν Παρεκκλήσιον Ἁγίου Σώζοντος Μεταξάδων",
        "seat": "Metaxades",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Μεταξάδες"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Euphemia Chapel in Prangio",
        "local": "Παρεκκλήσιον Ἁγίας Εὐφημίας Πραγγίου",
        "seat": "Prangio",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Πραγγίον"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Sophia Chapel in Cheimonio",
        "local": "Παρεκκλήσιον Ἁγίας Σοφίας Χειμωνίου",
        "seat": "Cheimonio",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Χειμώνιον"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Sophia Chapel in Fylakio",
        "local": "Παρεκκλήσιον Ἁγίας Σοφίας Φυλακίου",
        "seat": "Fylakio",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Φυλάκιον"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Sophia Chapel in Elafochori",
        "local": "Παρεκκλήσιον Ἁγίας Σοφίας Ἐλαφοχωρίου",
        "seat": "Elafochori",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Ἐλαφοχώριον"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Eustathius Chapel at the Holy Theodore Martyrs Church in Orestiada",
        "local": "Παρεκκλήσιον Ἁγίου Εὐσταθίου Ἱεροῦ Ναοῦ Ἁγίων Θεοδώρων Ὀρεστιάδος",
        "seat": "Orestiada",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Ὀρεστιάδα"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Eustathius Outlying Chapel in Pyrgos",
        "local": "Ἐξωκκλήσιον Ἁγίου Εὐσταθίου Πύργου",
        "seat": "Pyrgos",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Πύργος"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint John the Theologian Chapel in Karoti",
        "local": "Παρεκκλήσιον Ἁγίου Ἰωάννου τοῦ Θεολόγου Καρωτῆς",
        "seat": "Karoti",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Καρωτή"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint John the Theologian Chapel in Dadia",
        "local": "Παρεκκλήσιον Ἁγίου Ἰωάννου τοῦ Θεολόγου Δαδιᾶς",
        "seat": "Dadia",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Δαδιά"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint John the Theologian Chapel in Giatrades",
        "local": "Παρεκκλήσιον Ἁγίου Ἰωάννου τοῦ Θεολόγου Γιατράδων",
        "seat": "Giatrades",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Γιατράδες"],
        "sources": [FEAST_PAGE],
    },
    {
        "name": "Saint Nectarius Chapel in Didymoteicho",
        "local": "Ἱερό Παρεκκλήσιο Ἁγίου Νεκταρίου Διδυμοτείχου",
        "seat": "Didymoteicho",
        "rank": "Chapel",
        "kind": "parish",
        "address": ["Διδυμότειχον"],
        "sources": [FEAST_PAGE],
    },
]


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:72]


def build_rows():
    rows = []
    index = 0
    for roster in ROSTERS:
        source_url = roster["source"]
        for seat, address, local_name, dedication, phone, rank in roster["rows"]:
            index += 1
            name = "%s Parish Church in %s" % (dedication, seat)
            if rank == "Metropolitan Church":
                name = "%s Metropolitan Church in %s" % (dedication, seat)
            item = {
                "id": "gr-ep-didymoteichon-%03d-%s" % (index, slug(name)),
                "parent": PARENT,
                "kind": "parish",
                "rank": rank,
                "name": name,
                "local": "%s, %s" % (local_name, address.split(" 68")[0]),
                "seat": seat,
                "country": "GR",
                "address": [address],
                "sources": [ROSTER_PAGE, source_url],
            }
            if phone:
                item["phones"] = [phone]
                item["contact_sources"] = [source_url]
                item["contact_checked"] = CHECKED
            rows.append(item)
    for extra in EXTRA_ROWS:
        index += 1
        item = dict(extra)
        item.update({
            "id": "gr-ep-didymoteichon-%03d-%s" % (
                index, slug(item["name"])
            ),
            "parent": PARENT,
            "country": "GR",
        })
        if item.get("contact_sources"):
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 126
EXPECTED_OWNER_COUNTS = {PARENT: 126}
EXPECTED_KINDS = {"monastery": 4, "parish": 122}
EXPECTED_RANKS = {
    "Cathedral and Shrine": 1,
    "Cemetery Church": 1,
    "Chapel": 13,
    "Metropolitan Church": 3,
    "Monastery": 4,
    "Parish Church": 103,
    "Shrine": 1,
}
EXPECTED_CONTACT_BODIES = 28
EXPECTED_PHONE_BODIES = 28
EXPECTED_PHONE_VALUES = 28
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 126
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
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in {"ec-patr.org", "imdos.gr"}:
        raise ValueError("%s carries a non-competent source: %s" %
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
        raise ValueError("Didymoteichon candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Didymoteichon candidate ledger date drifted")
    expected_summary = {
        PARENT: 126,
        "total": 126,
        "parish_kind_rows": 122,
        "monastery_kind_rows": 4,
        "contact_bodies": 28,
        "phone_bodies": 28,
        "public_phone_values": 28,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 126,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Didymoteichon ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Didymoteichon ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Didymoteichon ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Didymoteichon ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Didymoteichon ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Didymoteichon ledger has forbidden punctuation")
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
        signature = (parent, unicase(item["local"]))
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
        raise ValueError("Didymoteichon English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Didymoteichon English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Didymoteichon parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Didymoteichon kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Didymoteichon rank totals drifted: %r" %
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
        raise ValueError("Didymoteichon contact coverage drifted: %r"
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
            "Didymoteichon: %d exact named bodies; %d carry current "
            "institutional contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Didymoteichon: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
