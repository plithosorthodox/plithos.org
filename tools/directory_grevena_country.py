#!/usr/bin/env python3
"""Validate exact named Grevena bodies from competent first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_grevena_country.py --check
    python tools/directory_grevena_country.py --check-live
    python tools/directory_grevena_country.py --dump
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
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "grevena_country.json"
)
PARENT = "ep-grevena"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-grevenon/"
)
PARISH_REGULATION = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_iounios.pdf"
)
CONTACT_PAGE = (
    "https://imgre.gr/%CE%B5%CF%80%CE%B9%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CE%BD%CE%B9%CE%B1/"
)
CLERGY_PAGE = (
    "https://imgre.gr/%CE%BF-%CE%BA%CE%BB%CE%B7%CF%81%CE%BF%CF%83/"
)
MONASTERY_PAGE = (
    "https://imgre.gr/%CE%B9%CE%B5%CF%81%CE%B5%CF%83-%CE%BC%CE%BF%CE%BD%CE%B5%CF%83/"
)
ZAVORADA_PROFILE = (
    "https://imgre.gr/%CE%B9%CE%B5%CF%81%CE%B5%CF%83-%CE%BC%CE%BF%CE%BD%CE%B5%CF%83/"
    "%CE%B9-%CE%BC-%CE%BF%CF%83%CE%B9%CE%BF%CF%85-%CE%BD%CE%B9%CE%BA%CE%B1%CE%BD%CF%89%CF%81%CE%B1/"
)


# Seat, exact dedication in the official regulation, English dedication.
# Source order is retained across the four archieratiki regions.
PARISH_RECORDS = r"""
Grevena|Ευαγγελισμοῦ τῆς Θεοτόκου|Annunciation of the Theotokos
Varosi|Ἁγίου Γεωργίου|Saint George
Agios Georgios|Ἁγίων Ἀποστόλων|Holy Apostles
Aidonia|Ἁγίου Ἀθανασίου|Saint Athanasius
Amygdalies|Ἁγίου Δημητρίου|Saint Demetrius
Asprokampos|Ἁγίου Παντελεήμονος|Saint Panteleimon
Vatolakkos|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Doxaras|Ἁγίου Γεωργίου|Saint George
Ekklisies|Εἰσοδίων τῆς Θεοτόκου|Entry of the Theotokos
Elatos|Ἁγίου Ἀθανασίου|Saint Athanasius
Elefthero A|Ἁγίου Ἀθανασίου|Saint Athanasius
Elefthero B|Παμμεγίστων Ταξιαρχῶν|Holy Archangels
Kalamitsi|Ἁγίου Ἀθανασίου|Saint Athanasius
Kalochi|Ἁγίου Νικολάου|Saint Nicholas
Kallirachi|Ἁγίων Πέτρου καί Παύλου|Saints Peter and Paul
Kastro|Ἁγίου Χαραλάμπους|Saint Charalambos
Kivotos|Ἁγίου Γεωργίου|Saint George
Klimataki|Ἁγίου Γεωργίου|Saint George
Kokkinia|Ἁγίου Δημητρίου|Saint Demetrius
Kydonies|Ἁγίου Ἀθανασίου|Saint Athanasius
Kyrakali|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Leipsi|Ἁγίου Νικολάου|Saint Nicholas
Lochmi|Παμμεγίστων Ταξιαρχῶν|Holy Archangels
Mavranaioi|Αγίου Δημητρίου|Saint Demetrius
Mavronoros|Αγίου Θεοδώρου Στρατηλάτου|Saint Theodore Stratelates
Megalo Seirini|Αγίου Δημητρίου|Saint Demetrius
Mesolakkos|Αγίας Παρασκευής|Saint Paraskevi
Milea|Αγίου Δημητρίου|Saint Demetrius
Mikro Seirini|Αγίας Παρασκευής|Saint Paraskevi
Myrsini|Αγίου Γεωργίου|Saint George
Nea Trapezounta|Αγίου Γεωργίου|Saint George
Oropedio|Παμμεγίστων Ταξιαρχών|Holy Archangels
Palaiokastro|Τιμίου Προδρόμου|Holy Forerunner
Polydendro|Παμμεγίστων Ταξιαρχών|Holy Archangels
Rodia|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Syndendro|Αγίου Νικολάου|Saint Nicholas
Taxiarchis|Αγίου Αθανασίου|Saint Athanasius
Agallaioi|Αγίου Δημητρίου|Saint Demetrius
Agapi|Αγίου Αθανασίου|Saint Athanasius
Agioi Theodoroi|Αγίων Θεοδώρων|Holy Theodore Martyrs
Aimilianos|Προφήτου Ηλιού|Prophet Elijah
Anthrakia|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Anoixi|Αγίου Νικολάου|Saint Nicholas
Vari|Αγίου Δημητρίου|Saint Demetrius
Dafnero|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Despotis|Αγίου Αθανασίου|Saint Athanasius
Dimitra|Αγίου Νικολάου|Saint Nicholas
Diporo|Αγίου Δημητρίου|Saint Demetrius
Eleftherochori|Αγίου Γεωργίου|Saint George
Exarchos|Αγίου Νικολάου|Saint Nicholas
Itea|Αγίου Νικολάου|Saint Nicholas
Karpero|Αγίας Τριάδος|Holy Trinity
Katakali|Αγίου Γεωργίου|Saint George
Kentro|Αγίου Γεωργίου|Saint George
Knidi|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Mikrokleisoura|Ἁγίας Τριάδος|Holy Trinity
Neochori|Γεννέσιον τῆς Θεοτόκου|Nativity of the Theotokos
Nisi|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Panagia|Ἁγίου Δημητρίου|Saint Demetrius
Palaiochori|Ἁγίας Παρασκευῆς|Saint Paraskevi
Paliorgia|Ἁγίου Νικολάου|Saint Nicholas
Pigaditsa|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Pistiko|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Pontini|Ἁγίας Παρασκευῆς|Saint Paraskevi
Poros|Παμμεγίστων Ταξιαρχῶν|Holy Archangels
Pyloroi|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Sarakina|Ἁγίου Νικολάου|Saint Nicholas
Sitaras|Ἁγίας Κυριακῆς|Saint Kyriaki
Trikokkia|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Trifyllio|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Fellio|Ἁγίου Νικολάου|Saint Nicholas
Chromio|Παμμεγίστων Ταξιαρχῶν|Holy Archangels
Avdella|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Alatopetra|Ἁγίου Παντελεήμονος|Saint Panteleimon
Anavryta|Ἁγίου Γεωργίου|Saint George
Ziakas|Παμμεγίστων Ταξιαρχῶν|Holy Archangels
Kallithea|Ἁγίου Νικολάου|Saint Nicholas
Kipoureio|Ἁγίου Νικολάου|Saint Nicholas
Kosmati|Ἁγίου Νικολάου|Saint Nicholas
Kranea|Ἁγίων Πάντων|All Saints
Lavda|Ἁγίου Γεωργίου|Saint George
Megaro|Ἁγίου Δημητρίου|Saint Demetrius
Mesolouri|Ἁγίου Δημητρίου|Saint Demetrius
Mikrolivado|Ἁγίου Γεωργίου|Saint George
Monachiti|Ἁγίου Δημητρίου|Saint Demetrius
Panorama|Γενέσιον τῆς Θεοτόκου|Nativity of the Theotokos
Paroreio|Προφήτου Ἠλιοῦ|Prophet Elijah
Perivoli|Ἁγίου Γεωργίου|Saint George
Platanistos|Ἁγίων Πάντων|All Saints
Polyneri|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Pronia|Ἁγίου Ἀθανασίου|Saint Athanasius
Prosforo|Ἁγίου Δημητρίου|Saint Demetrius
Samarina|Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos
Smixi|Ἁγίου Νικολάου|Saint Nicholas
Spilaio|Ἁγίου Ἀθανασίου|Saint Athanasius
Stavros|Ἁγίου Νικολάου|Saint Nicholas
Trikomo|Ἁγίου Γεωργίου|Saint George
Filippeoi|Ἁγίων Κωνσταντίνου καὶ Ἑλένης|Saints Constantine and Helen
"""


CHAPEL_RECORDS = [
    {
        "name": "Saint Achillios Institutional Chapel in Grevena",
        "local": "Παρεκκλήσιο τοῦ Ἁγίου Ἀχιλλείου",
        "seat": "Grevena",
        "rank": "Institutional Chapel",
        "address": ["Nursing home, Grevena"],
        "source": "https://imgre.gr/mia-politeia-tou-ouranou-stinetai-fetos/",
        "probe": "Αγίου Αχιλλείου",
    },
    {
        "name": "Saint Christopher Chapel in Grevena",
        "local": "Παρεκκλήσιο τοῦ Ἁγίου Χριστοφόρου πόλεως Γρεβενῶν",
        "seat": "Grevena",
        "rank": "Chapel",
        "address": ["Grevena"],
        "source": "https://imgre.gr/eorti-agiou-christoforou/",
        "probe": "Αγίου Χριστοφόρου",
    },
    {
        "name": "Prophet Elijah the Tishbite Chapel in Grevena",
        "local": "Ἱερό Παρεκκλήσιο Προφήτου Ἠλιοῦ τοῦ Θεσβίτου πόλεως Γρεβενῶν",
        "seat": "Grevena",
        "rank": "Chapel",
        "address": ["Grevena"],
        "source": "https://imgre.gr/anakoinosi-4/",
        "probe": "Προφήτου Ηλιού του Θεσβίτου",
    },
    {
        "name": "Apostle Philip Episcopal Chapel in Grevena",
        "local": "Μητροπολιτικό Παρεκκλήσιο Ἁγίου Ἀποστόλου Φιλίππου",
        "seat": "Grevena",
        "rank": "Episcopal Chapel",
        "address": ["Episcopate, Grevena"],
        "source": "https://imgre.gr/eorti-tou-agiou-filippou-sto-mitropolitiko-parekklisio/",
        "probe": "Αγίου Αποστόλου Φιλίππου",
    },
    {
        "name": "Saint Emilianos Memorial Chapel in Grevena",
        "local": "Ἱερό Παρεκκλήσιο τοῦ Ἁγίου Αἰμιλιανοῦ",
        "seat": "Grevena",
        "rank": "Memorial Chapel",
        "address": ["Martyrdom site of Metropolitan Emilianos, Grevena"],
        "source": "https://imgre.gr/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%ce%bc%ce%bc%ce%b1-%ce%bb%ce%b1%cf%84%cf%81%ce%b5%cf%85%cf%84%ce%b9%ce%ba%cf%8e%ce%bd-%ce%b5%ce%ba%ce%b4%ce%b7%ce%bb%cf%8e%cf%83%ce%b5%cf%89%ce%bd-%ce%bc%ce%bd-2/",
        "probe": "Παρεκκλήσιο του Αγίου Αιμιλιανού",
    },
    {
        "name": "Saint Paisios the Athonite Country Church in Kentro",
        "local": "Ἐξωκκλήσιο Ἁγίου Παϊσίου",
        "seat": "Kentro",
        "rank": "Country Church",
        "address": ["Kentro"],
        "source": "https://imgre.gr/eorti-agiou-paisiou/",
        "probe": "Εξωκκλήσιο του Αγίου Παϊσίου",
    },
    {
        "name": "Holy Archangels Chapel in Elefthero B",
        "local": "Παρεκκλήσιο τῶν Παμμεγίστων Ταξιαρχῶν",
        "seat": "Elefthero B",
        "rank": "Chapel",
        "address": ["Elefthero B"],
        "source": "https://imgre.gr/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%af%ce%be%ce%b9%ce%b1-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%af%ce%bf%cf%85-%cf%80%ce%b1%ce%bc%ce%bc%ce%b5%ce%b3%ce%af%cf%83%cf%84%cf%89%ce%bd/",
        "probe": "Παρεκκλησίου των Παμμεγίστων Ταξιαρχών",
    },
    {
        "name": "Saint Paraskevi Metropolitan Chapel in Grevena",
        "local": "Μητροπολιτικό Παρεκκλήσιο Ἁγίας Παρασκευῆς",
        "seat": "Grevena",
        "rank": "Metropolitan Chapel",
        "address": ["Grevena"],
        "source": "https://imgre.gr/%cf%80%cf%8e%cf%82-%ce%b8%ce%b1-%ce%bb%ce%b5%ce%b9%cf%84%ce%bf%cf%85%cf%81%ce%b3%ce%ae%cf%83%ce%bf%cf%85%ce%bd-%ce%bf%ce%b9-%ce%bd%ce%b1%ce%bf%ce%af-%cf%84%ce%b7%cf%82-%cf%80%cf%8c%ce%bb%ce%b5%cf%89/",
        "probe": "ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ",
    },
    {
        "name": "Saint Kalliopi Chapel in Palaiokastro",
        "local": "Παρεκκλήσιο τῆς Ἁγίας Καλλιόπης",
        "seat": "Palaiokastro",
        "rank": "Chapel",
        "address": ["Palaiokastro"],
        "source": "https://imgre.gr/%cf%80%cf%81%ce%bf%ce%b3%cf%81%ce%b1%ce%bc%ce%bc%ce%b1-%ce%b1%ce%ba%ce%bf%ce%bb%ce%bf%cf%85%ce%b8%ce%b9%cf%89%ce%bd-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%ce%b9%cf%84%ce%bf%cf%85-%ce%b3-5/",
        "probe": "Νεόκτιστο Παρεκκλήσιο της Αγίας",
    },
    {
        "name": "Saint Anastasia Parish Chapel in Megalo Seirini",
        "local": "Ἱερό Παρεκκλήσιο τῆς Ἁγίας Ἀναστασίας",
        "seat": "Megalo Seirini",
        "rank": "Parish Chapel",
        "address": ["Beneath Saint Demetrius Parish Church, Megalo Seirini"],
        "source": "https://imgre.gr/%ce%b5%ce%bf%cf%81%cf%84%ce%ae-%ce%b1%ce%b3%ce%af%ce%b1%cf%82-%ce%b1%ce%bd%ce%b1%cf%83%cf%84%ce%b1%cf%83%ce%af%ce%b1%cf%82-%cf%83%cf%84%ce%bf-%ce%bc%ce%b5%ce%b3%ce%ac%ce%bb%ce%bf-%cf%83%ce%b5%ce%b9/",
        "probe": "παρεκκλήσιον της Αγίας Αναστασίας",
    },
    {
        "name": "Saints Catherine and Charalambos Cemetery Chapel in Milea",
        "local": "Παρεκκλήσιο Ἁγίας Αἰκατερίνης καὶ Ἁγίου Χαραλάμπους",
        "seat": "Milea",
        "rank": "Cemetery Chapel",
        "address": ["Milea Cemetery"],
        "source": "https://imgre.gr/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%af%ce%be%ce%b9%ce%b1-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%af%ce%bf%cf%85-%ce%b1%ce%b3%ce%af%ce%b1%cf%82-%ce%b1%ce%b9%ce%ba%ce%b1%cf%84/",
        "probe": "Παρεκκλησίου Αγίας Αικατερίνης και Αγίου Χαραλάμπους",
    },
    {
        "name": "Saint Eleftherios Institutional Chapel in Grevena",
        "local": "Ἱερό Παρεκκλήσιο τοῦ Ἁγίου Ἐλευθερίου",
        "seat": "Grevena",
        "rank": "Institutional Chapel",
        "address": ["Grevena Correctional Institution"],
        "source": "https://imgre.gr/%ce%bc%ce%af%ce%b1-%cf%80%ce%bf%ce%b9%ce%bc%ce%b1%ce%bd%cf%84%ce%b9%ce%ba%ce%ae-%cf%84%cf%89%ce%bd-%cf%86%cf%85%ce%bb%ce%b1%ce%ba%cf%8e%ce%bd-%ce%b3%ce%b9%ce%b1-%ce%ba%cf%81%ce%b1%cf%84%ce%bf%cf%85/",
        "probe": "Παρεκκλήσιο του αγίου Ελευθερίου",
    },
    {
        "name": "Saint Andrew the First-Called University Chapel in Grevena",
        "local": "Ἱερό Παρεκκλήσιο τοῦ Ἁγίου Ἀνδρέα τοῦ Πρωτοκλήτου",
        "seat": "Grevena",
        "rank": "University Chapel",
        "address": ["TEI Grevena"],
        "source": "https://imgre.gr/%ce%b1%ce%b3%ce%b9%ce%b1%cf%83%ce%bc%ce%bf%cf%83-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%cf%85-%cf%84-%ce%b5-%ce%b9-%ce%b3%cf%81%ce%b5%ce%b2%ce%b5%ce%bd%cf%89%ce%bd/",
        "probe": "Παρεκκλησίου του Αγίου Ανδρέα του Πρωτοκλήτου",
    },
    {
        "name": "Saint Kyriaki Byzantine Chapel in Mavronoros",
        "local": "Βυζαντινό Παρεκκλήσιο Ἁγίας Κυριακῆς",
        "seat": "Mavronoros",
        "rank": "Byzantine Chapel",
        "address": ["Mavronoros"],
        "source": "https://imgre.gr/%cf%80%ce%b1%ce%bd%ce%b7%ce%b3%cf%85%cf%81%ce%b9%ce%ba%ce%bf%cf%83-%ce%b5%cf%83%cf%80%ce%b5%cf%81%ce%b9%ce%bd%ce%bf%cf%83-%ce%b1%ce%b3-%ce%ba%cf%85%cf%81%ce%b9%ce%b1%ce%ba%ce%b7%cf%83-%cf%83%cf%84/",
        "probe": "Βυζαντινό Παρεκκλήσιο",
    },
]


OTHER_RECORDS = [
    {
        "name": "Nativity of Saint John the Forerunner Country Church in Kalochi",
        "local": "Ἐξωκκλήσιο Γενεθλίου τοῦ Τιμίου Προδρόμου",
        "seat": "Kalochi",
        "kind": "parish",
        "rank": "Country Church",
        "address": ["Kalochi"],
        "source": "https://imgre.gr/%ce%b5%ce%bf%cf%81%cf%84%ce%ae-%ce%b3%ce%b5%ce%bd%ce%b5%ce%b8%ce%bb%ce%af%ce%bf%cf%85-%cf%84%ce%bf%cf%85-%cf%84%ce%b9%ce%bc%ce%af%ce%bf%cf%85-%cf%80%cf%81%ce%bf%ce%b4%cf%81%cf%8c%ce%bc%ce%bf%cf%85/",
        "probe": "Εξωκκλησίου του Γενεθλίου του Προδρόμου",
    },
    {
        "name": "Saint Demetrius Metochion of Zavorada Monastery",
        "local": "Ἱερὸν Μετόχιον τοῦ Ἁγίου Δημητρίου",
        "seat": "Zavorada",
        "kind": "monastery",
        "rank": "Metochion",
        "address": ["Zavorada"],
        "source": "https://imgre.gr/me-monastiki-labrotita-i-iera-panigyris-tis-ieras-monis-metamorfoseos-tou-sotiros-zavordas/",
        "probe": "Ιστορικό Μετόχιο του Αγίου Δημητρίου",
    },
    {
        "name": (
            "Dormition of the Theotokos at Spilaio Metochion of "
            "Zavorada Monastery"
        ),
        "local": (
            "Ἱερὰ Μονὴ Παναγίας τοῦ Σπηλαίου, Μετόχιο τῆς "
            "Ἱερᾶς Μονῆς Ἁγίου Νικάνορος Ζάβορδας"
        ),
        "seat": "Spilaio",
        "kind": "monastery",
        "rank": "Metochion",
        "address": ["Spilaio, Grevena"],
        "source": "https://imgre.gr/proti-koura-eis-monachon-meta-apo-polla-eti-sto-spilaio-grevenon/",
        "probe": "Ιερά Μονή Παναγίας του Σπηλαίου, μετόχιο",
    },
    {
        "name": "Transfiguration of the Savior Katholikon at Zavorada Monastery",
        "local": "Καθολικὸν Μεταμορφώσεως τοῦ Σωτῆρος",
        "seat": "Zavorada",
        "kind": "monastery",
        "rank": "Monastery Church",
        "address": ["Patriarchal and Stavropegic Monastery of Venerable Nikanor", "Zavorada"],
        "source": ZAVORADA_PROFILE,
        "probe": "Μονή του Οσίου Νικάνορα (Μεταμορφώσεως του Σωτήρος) Ζάβορδας",
    },
    {
        "name": "Saint Athanasius Monastery Chapel at Zavorada",
        "local": "Παρεκκλήσιο τοῦ Ἁγίου Ἀθανασίου",
        "seat": "Zavorada",
        "kind": "monastery",
        "rank": "Monastery Chapel",
        "address": ["Patriarchal and Stavropegic Monastery of Venerable Nikanor", "Zavorada"],
        "source": ZAVORADA_PROFILE,
        "probe": "Παρεκκλήσι του Αγίου Αθανασίου",
    },
    {
        "name": "Hermitage of Venerable Nikanor near Zavorada",
        "local": "Σκήτη τοῦ Ὁσίου Νικάνορος",
        "seat": "Zavorada",
        "kind": "monastery",
        "rank": "Hermitage",
        "address": ["Near the Monastery of Zavorada"],
        "source": ZAVORADA_PROFILE,
        "probe": "Υπάρχει η σκήτη του Οσίου",
    },
]


def parse_records(value, fields):
    rows = []
    for line in value.strip().splitlines():
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != fields:
            raise ValueError("invalid Grevena source record: %s" % line)
        rows.append(parts)
    return rows


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def unicase(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value.casefold()).strip()


def build_rows():
    records = parse_records(PARISH_RECORDS, 3)
    if len(records) != 98:
        raise ValueError("Grevena parish regulation alignment drifted")
    rows = []
    index = 0
    for offset, (seat, local_dedication, english_dedication) in enumerate(records):
        index += 1
        rank = "Metropolitan Cathedral" if offset == 0 else "Parish Church"
        name = "%s %s in %s" % (english_dedication, rank, seat)
        local = local_dedication
        sources = [PARISH_REGULATION]
        address = [seat]
        if offset == 0:
            name = (
                "Annunciation of the Theotokos and Saint Achillios "
                "Metropolitan Cathedral in Grevena"
            )
            local = (
                "Ἱερός Μητροπολιτικός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου "
                "καὶ Ἁγίου Ἀχιλλίου"
            )
            sources.append(CONTACT_PAGE)
            address = ["Εὐαγγελίστριας 19", "Grevena"]
        rows.append({
            "id": "gr-ep-grevena-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": address,
            "sources": sources,
        })
    for record in CHAPEL_RECORDS:
        index += 1
        rows.append({
            "id": "gr-ep-grevena-%03d-%s" % (index, slug(record["name"])),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": record["name"],
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "sources": [record["source"]],
        })
    for record in OTHER_RECORDS:
        index += 1
        rows.append({
            "id": "gr-ep-grevena-%03d-%s" % (index, slug(record["name"])),
            "parent": PARENT,
            "kind": record["kind"],
            "rank": record["rank"],
            "name": record["name"],
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "sources": [record["source"]],
        })
    index += 1
    name = (
        "Patriarchal and Stavropegic Monastery of Venerable Nikanor "
        "at Zavorada"
    )
    rows.append({
        "id": "gr-ep-grevena-%03d-%s" % (index, slug(name)),
        "parent": PARENT,
        "kind": "monastery",
        "rank": "Patriarchal and Stavropegic Monastery",
        "name": name,
        "local": (
            "Ἱερὰ Πατριαρχικὴ καὶ Σταυροπηγιακὴ Μονὴ Ὁσίου "
            "Νικάνορος Ζάβορδας"
        ),
        "seat": "Zavorada",
        "country": "GR",
        "address": ["512 00 Deskati", "Grevena"],
        "phones": ["24620-25261"],
        "sources": [PATRIARCHATE_PAGE, MONASTERY_PAGE],
        "contact_sources": [PATRIARCHATE_PAGE],
        "contact_checked": CHECKED,
    })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 119
EXPECTED_OWNER_COUNTS = {PARENT: 119}
EXPECTED_KINDS = {"monastery": 6, "parish": 113}
EXPECTED_RANKS = {
    "Byzantine Chapel": 1,
    "Cemetery Chapel": 1,
    "Chapel": 4,
    "Country Church": 2,
    "Episcopal Chapel": 1,
    "Hermitage": 1,
    "Institutional Chapel": 2,
    "Memorial Chapel": 1,
    "Metropolitan Cathedral": 1,
    "Metropolitan Chapel": 1,
    "Metochion": 2,
    "Monastery Chapel": 1,
    "Monastery Church": 1,
    "Parish Chapel": 1,
    "Parish Church": 97,
    "Patriarchal and Stavropegic Monastery": 1,
    "University Chapel": 1,
}
EXPECTED_CONTACT_BODIES = 1
EXPECTED_PHONE_BODIES = 1
EXPECTED_PHONE_VALUES = 1
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 119
EXISTING_PARENTS = {PARENT}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
COMPETENT_HOSTS = {
    "ec-patr.org",
    "ecclesiagreece.gr",
    "imgre.gr",
    "www.ec-patr.org",
    "www.ecclesiagreece.gr",
    "www.imgre.gr",
}


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
    if parsed.scheme != "https" or parsed.netloc not in COMPETENT_HOSTS:
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
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Grevena candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED or ledger.get("parent") != PARENT:
        raise ValueError("Grevena candidate ledger date or parent drifted")
    expected_summary = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "parish_kind_rows": EXPECTED_KINDS["parish"],
        "monastery_kind_rows": EXPECTED_KINDS["monastery"],
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Grevena ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Grevena ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Grevena ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Grevena ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Grevena ledger has duplicate candidate ids")
    for value in walk_strings(ledger):
        if FORBIDDEN_PUNCTUATION.search(value):
            raise ValueError("Grevena ledger carries forbidden punctuation")
    return ledger


def validate_rows():
    cleaned = [clean(row) for row in ROWS]
    if len(cleaned) != EXPECTED_TOTAL:
        raise ValueError("Grevena total drifted: %d" % len(cleaned))
    ids = [row["id"] for row in cleaned]
    if len(ids) != len(set(ids)):
        raise ValueError("Grevena ids collide")
    signatures = []
    for row in cleaned:
        row_id = row["id"]
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("invalid id: %s" % row_id)
        if row.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has an unknown parent" % row_id)
        if row.get("country") != "GR":
            raise ValueError("%s has the wrong country" % row_id)
        if row.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        for field in ("name", "local", "rank", "seat"):
            if not row.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        if row.get("checked") != CHECKED:
            raise ValueError("%s carries an unexpected checked date" % row_id)
        if row.get("address") in (None, [], [""]):
            raise ValueError("%s lacks an official locality or address" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in row["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        for email in row.get("emails") or []:
            if not EMAIL_RE.fullmatch(email):
                raise ValueError("%s has invalid email %s" % (row_id, email))
        for phone in row.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s has invalid phone %s" % (row_id, phone))
        for value in walk_strings(row):
            if FORBIDDEN_PUNCTUATION.search(value):
                raise ValueError("%s carries forbidden punctuation" % row_id)
        signatures.append((unicase(row["name"]), unicase(row["seat"])))
    if len(signatures) != len(set(signatures)):
        raise ValueError("Grevena English identities collide")
    owner_counts = Counter(row["parent"] for row in cleaned)
    kind_counts = Counter(row["kind"] for row in cleaned)
    rank_counts = Counter(row["rank"] for row in cleaned)
    if dict(owner_counts) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Grevena owner counts drifted")
    if dict(kind_counts) != EXPECTED_KINDS:
        raise ValueError("Grevena kind counts drifted")
    if dict(rank_counts) != EXPECTED_RANKS:
        raise ValueError("Grevena rank counts drifted: %r" % dict(rank_counts))
    metrics = {
        "contact_bodies": sum(
            bool(row.get("phones") or row.get("emails") or row.get("site"))
            for row in cleaned
        ),
        "phone_bodies": sum(bool(row.get("phones")) for row in cleaned),
        "phone_values": sum(len(row.get("phones") or []) for row in cleaned),
        "email_bodies": sum(bool(row.get("emails")) for row in cleaned),
        "email_values": sum(len(row.get("emails") or []) for row in cleaned),
        "site_bodies": sum(bool(row.get("site")) for row in cleaned),
        "address_bodies": sum(bool(row.get("address")) for row in cleaned),
    }
    expected = {
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "email_values": EXPECTED_EMAIL_VALUES,
        "site_bodies": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
    }
    if metrics != expected:
        raise ValueError("Grevena contact metrics drifted: %r" % metrics)
    if set(ENGLISH_NAMES) != set(ids):
        raise ValueError("Grevena English-name coverage drifted")
    expected_seats = {row["seat"] for row in cleaned if row.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Grevena English-seat coverage drifted")
    return cleaned


def build():
    rows = validate_rows()
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": rows,
        }
    }


def all_source_urls():
    urls = {PATRIARCHATE_PAGE, PARISH_REGULATION,
            CONTACT_PAGE, CLERGY_PAGE, MONASTERY_PAGE, ZAVORADA_PROFILE}
    for row in ROWS:
        urls.update(row.get("sources") or [])
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        for entry in ledger.get(key) or []:
            urls.update(entry.get("sources") or [])
    return sorted(urls)


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    return unicase(re.sub(r"\s+", " ", value).strip())


def check_live_sources():
    failures = []
    source_texts = {}
    for url in all_source_urls():
        try:
            request = Request(url, headers={
                "User-Agent": "Mozilla/5.0 Plithos directory source audit",
            })
            with urlopen(request, timeout=45) as response:
                if response.status >= 400:
                    failures.append((url, "HTTP %s" % response.status))
                    continue
                payload = response.read()
                content_type = response.headers.get("Content-Type", "").lower()
                if url == PARISH_REGULATION:
                    if "pdf" not in content_type or not payload.startswith(b"%PDF"):
                        failures.append((url, "unexpected PDF response"))
                else:
                    if "html" not in content_type:
                        failures.append(
                            (url, "unexpected content type %s" % content_type)
                        )
                    source_texts[url] = normalize_source_text(
                        payload.decode("utf-8", "replace")
                    )
        except Exception as exc:
            failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join("%s [%s]" % pair for pair in failures)
        raise ValueError("live Grevena source check failed: %s" % rendered)
    probes = [
        (PATRIARCHATE_PAGE, "Ενοριακοί Ναοί: 98"),
        (CONTACT_PAGE, "Ιερός Μητροπολιτικός Ναός"),
        (CLERGY_PAGE, "Κλήρος"),
        (MONASTERY_PAGE, "Ιερά Πατριαρχική και Σταυροπηγιακή Μονή"),
    ]
    probes.extend((row["source"], row["probe"])
                  for row in CHAPEL_RECORDS)
    probes.extend((row["source"], row["probe"])
                  for row in OTHER_RECORDS)
    missing = []
    for url, probe in probes:
        if unicase(probe) not in source_texts.get(url, ""):
            missing.append((url, probe))
    if missing:
        raise ValueError("live Grevena source-name check failed: %r" % missing)


def stats(rows):
    return {
        "total": len(rows),
        "kinds": dict(sorted(Counter(row["kind"] for row in rows).items())),
        "ranks": dict(sorted(Counter(row["rank"] for row in rows).items())),
        "phones": sum(len(row.get("phones") or []) for row in rows),
        "emails": sum(len(row.get("emails") or []) for row in rows),
        "sites": sum(bool(row.get("site")) for row in rows),
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args(argv)
    payloads = build()
    rows = payloads[PARENT]["rows"]
    if args.check_live:
        check_live_sources()
    if args.dump:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(stats(rows), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Grevena: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
