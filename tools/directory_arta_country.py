#!/usr/bin/env python3
"""Validate exact named Arta Metropolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_arta_country.py --check
    python tools/directory_arta_country.py --check-live
    python tools/directory_arta_country.py --dump
"""

import argparse
from collections import Counter
import html
from http.client import IncompleteRead
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib.parse import quote, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-arta"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "arta_country.json"
)

LEGAL_2019 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/iera-metropole-artes"
)
HOME = "https://www.imartis.gr/"
MONASTERY_DIRECTORY = HOME + "μητρόπολη/ιερές-μονές.html"
METROPOLITAN_CHAPELS = (
    HOME + "μητρόπολη/ενορίες/μητροπολιτικά-παρεκκλήσια.html"
)

REGION_URLS = {
    "A_CITY": HOME + "μητρόπολη/ενορίες/α-περιφέρεια-άρτα.html",
    "A_NEAR": HOME + "μητρόπολη/ενορίες/α-περιφέρεια-περίχωρα.html",
    "B": HOME + "μητρόπολη/ενορίες/β-περιφέρεια.html",
    "C": HOME + "μητρόπολη/ενορίες/γ-περιφέρεια.html",
    "D": HOME + "μητρόπολη/ενορίες/δ-περιφέρεια.html",
    "E": HOME + "μητρόπολη/ενορίες/ε-περιφέρεια.html",
}

DETAIL_URLS = {
    "ARTA_DEMETRIUS": REGION_URLS["A_CITY"].replace(
        ".html", "/11-ενορία-αγίου-δημητρίου.html"
    ),
    "ARTA_GEORGE": REGION_URLS["A_CITY"].replace(
        ".html", "/12-ενορία-αγίου-γεωργίου.html"
    ),
    "ARTA_PANTOKRATOR": REGION_URLS["A_CITY"].replace(
        ".html", "/13-ενορία-παντοκράτορος.html"
    ),
    "ARTA_NICHOLAS": REGION_URLS["A_CITY"].replace(
        ".html", "/15-ενορία-αγίου-νικολάου.html"
    ),
    "ARTA_APOSTLES": REGION_URLS["A_CITY"].replace(
        ".html", "/19-ενορία-αγίων-αποστόλων.html"
    ),
    "ARTA_ARCHANGELS": REGION_URLS["A_CITY"].replace(
        ".html", "/25-ενορία-παμμεγίστων-ταξιαρχών.html"
    ),
    "ARTA_MAXIMUS": REGION_URLS["A_CITY"].replace(
        ".html", "/26-ενορία-αγίου-μαξίμου-του-γραικού.html"
    ),
    "ANARGYROI": (
        HOME + "component/content/article/123-ενορία-αγίων-αναργύρων.html"
        "?catid=15"
    ),
    "ZYGOS": REGION_URLS["B"].replace(
        ".html", "/145-ενορία-ζυγού.html"
    ),
    "KLEIDI": REGION_URLS["B"].replace(
        ".html", "/149-ενορία-κλειδίου.html"
    ),
}

MONASTERY_URLS = {
    "KATO_PANAGIA": (
        HOME + "μητρόπολη/ιερές-μονές/20-ιερά-μονή-κάτω-παναγιάς.html"
    ),
    "THEOTOKIO": (
        HOME + "μητρόπολη/ιερές-μονές/21-ιερά-μονή-θεοτοκιού.html"
    ),
    "ROVELISTA": (
        HOME + "μητρόπολη/ιερές-μονές/"
        "22-ιερά-μονή-παναγίας-της-ροβέλιστας.html"
    ),
    "MELATES": (
        HOME + "μητρόπολη/ιερές-μονές/23-ιερά-μονή-μελατών.html"
    ),
    "PARASKEVI_PRAMANTA": (
        HOME + "μητρόπολη/ιερές-μονές/901-ιερά-μονή-μελατών-2.html"
    ),
    "CATHERINE_KATARRAKTIS": (
        HOME + "μητρόπολη/ιερές-μονές/902-ιερά-μονή-μελατών-3.html"
    ),
    "GEORGE_VOURGARELI": (
        HOME + "μητρόπολη/ιερές-μονές/"
        "24-ιερά-μονή-αγίου-γεωργίου-βουργαρελίου.html"
    ),
}

METROPOLITAN_CHAPEL_URLS = {
    "JOHN": (
        HOME + "component/content/article/"
        "27-ιερός-ναός-αγίου-ιωάνου-του-θεολόγου.html?catid=20"
    ),
    "GIATRISSA": (
        HOME + "component/content/article/"
        "29-ιερός-ναός-παναγίας-γιάτρισσας,-νοσοκομείο-άρτης.html"
        "?catid=20"
    ),
    "FANEROMENI": (
        HOME + "component/content/article/"
        "147-ιερός-ναός-παναγίας-φανερωμένης.html?catid=20"
    ),
    "ENTRANCE": (
        HOME + "component/content/article/"
        "72-ο-ναός-της-μητροπόλεως-στην-άρτα.html?catid=20"
    ),
}


# region|key|English seat|Greek seat|English dedication|Greek dedication|
# rank|Greek address|phones|detail token
PARISH_SOURCE = r'''
A_CITY|arta-saint-demetrius|Arta|Άρτα|Saint Demetrius|Αγίου Δημητρίου|Metropolitan Church|Πλατεία Αγίου Δημητρίου, 47100 Άρτα|26810-28067|ARTA_DEMETRIUS
A_CITY|arta-saint-george|Arta|Άρτα|Saint George|Αγίου Γεωργίου|Parish Church|Οδός Σκουφά, 47100 Άρτα|26810-26315|ARTA_GEORGE
A_CITY|arta-pantokrator|Arta|Άρτα|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church|Πλατεία Παντοκράτορος, 47100 Άρτα|26810-75072|ARTA_PANTOKRATOR
A_CITY|arta-saint-nicholas|Arta|Άρτα|Saint Nicholas|Αγίου Νικολάου|Parish Church|Πλατεία Αγίου Νικολάου, 47100 Άρτα|26810-22417,26810-26138,697-201-8988|ARTA_NICHOLAS
A_CITY|arta-holy-apostles|Arta|Άρτα|Holy Apostles|Αγίων Αποστόλων|Parish Church|Οδός Αγίων Αποστόλων 49, 47100 Άρτα|26810-70734|ARTA_APOSTLES
A_CITY|arta-holy-archangels|Arta|Άρτα|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|47100 Άρτα|26810-23796|ARTA_ARCHANGELS
A_CITY|arta-saint-maximus|Arta|Άρτα|Saint Maximus the Greek|Αγίου Μαξίμου του Γραικού|Parish Church|47100 Άρτα|26810-26340|ARTA_MAXIMUS
A_NEAR|agios-dimitrios-peta|Agios Dimitrios Peta|Άγιος Δημήτριος Πέτα|Saint Demetrius|Αγίου Δημητρίου|Parish Church|Άγιος Δημήτριος Πέτα||
A_NEAR|agioi-anargyroi|Agioi Anargyroi|Άγιοι Ανάργυροι|Saint Therapon|Αγίου Θεράποντος|Parish Church|Άγιοι Ανάργυροι|26810-26195,26810-24691|ANARGYROI
A_NEAR|amfithea|Amfithea|Αμφιθέα|Holy Apostles|Αγίων Αποστόλων|Parish Church|Αμφιθέα||
A_NEAR|glykorryzo|Glykorryzo|Γλυκόρριζο|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Γλυκόρριζο||
A_NEAR|kleisto|Kleisto|Κλειστό|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Κλειστό||
A_NEAR|kommeno|Kommeno|Κομμένο|Saints Peter and Paul|Αγίων Αποστόλων Πέτρου και Παύλου|Parish Church|Κομμένο||
A_NEAR|kompoti|Kompoti|Κομπότι|Saint George|Αγίου Γεωργίου|Parish Church|Κομπότι||
A_NEAR|limini|Limini|Λιμίνη|Saint Nicholas|Αγίου Νικολάου|Parish Church|Λιμίνη||
A_NEAR|loutrotopos|Loutrotopos|Λουτρότοπος|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|Λουτρότοπος||
A_NEAR|megarchi|Megarchi|Μεγάρχη|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Μεγάρχη||
A_NEAR|neochoraki|Neochoraki|Νεοχωράκι|Saint George|Αγίου Γεωργίου|Parish Church|Νεοχωράκι||
A_NEAR|peranthi|Peranthi|Περάνθη|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church|Περάνθη||
A_NEAR|peta|Peta|Πέτα|Saint George|Αγίου Γεωργίου|Parish Church|Πέτα||
A_NEAR|sellades|Sellades|Σελλάδες|Saint George|Αγίου Γεωργίου|Parish Church|Σελλάδες||
A_NEAR|sykees|Sykees|Συκιές|Life-Giving Spring|Ζωοδόχου Πηγής|Parish Church|Συκιές||
A_NEAR|foteino|Foteino|Φωτεινό|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Φωτεινό||
B|anemorrachi|Anemorrachi|Ανεμορράχη|Saint Nicholas|Αγίου Νικολάου|Parish Church|Ανεμορράχη||
B|ano-kalentini|Ano Kalentini|Άνω Καλεντίνη|Saint George|Αγίου Γεωργίου|Parish Church|Άνω Καλεντίνη||
B|ano-petra|Ano Petra|Άνω Πέτρα|Saint George|Αγίου Γεωργίου|Parish Church|Άνω Πέτρα||
B|velentziko|Velentziko|Βελεντζικό|Holy Unmercenaries|Αγίων Αναργύρων|Parish Church|Βελεντζικό||
B|giannioti|Giannioti|Γιαννιώτι|Nativity of Saint John the Forerunner|Γενεσίου Τιμίου Προδρόμου|Parish Church|Γιαννιώτι||
B|dimario|Dimario|Δημαριό|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|Δημαριό||
B|distrato|Distrato|Δίστρατο|Holy Trinity|Αγίας Τριάδος|Parish Church|Δίστρατο||
B|dichomiri|Dichomiri|Διχομοίρι|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Διχομοίρι||
B|domosko-diasello|Domosko Diasello|Δομοσκό Διασέλλου|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Δομοσκό Διασέλλου||
B|zygos|Zygos|Ζυγός|Saint George|Αγίου Γεωργίου|Parish Church|Ζυγός|697-010-0769|ZYGOS
B|kalloni|Kalloni|Καλλονή|Saint Menas|Αγίου Μηνά|Parish Church|Καλλονή||
B|kato-kalentini|Kato Kalentini|Κάτω Καλεντίνη|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Κάτω Καλεντίνη||
B|kentriko|Kentriko|Κεντρικό|Saint Nicholas|Αγίου Νικολάου|Parish Church|Κεντρικό||
B|kleidi|Kleidi|Κλειδί|Saint Kyriaki|Αγίας Κυριακής|Parish Church|Κλειδί|698-628-5550|KLEIDI
B|makrykampos-diasello|Makrykampos Diasello|Μακρύκαμπος Διασέλλου|Saint Kosmas of Aetolia|Αγίου Κοσμά Αιτωλού|Parish Church|Μακρύκαμπος Διασέλλου||
B|markiniada|Markiniada|Μαρκινιάδα|Saint George|Αγίου Γεωργίου|Parish Church|Μαρκινιάδα||
B|melates|Melates|Μελάτες|Saint Nicholas|Αγίου Νικολάου|Parish Church|Μελάτες||
B|xerokampos|Xerokampos|Ξηρόκαμπος|Saint Thomas|Αγίου Θωμά|Parish Church|Ξηρόκαμπος||
B|palaiochoraki|Palaiochoraki|Παλαιοχωράκι|Saint George|Αγίου Γεωργίου|Parish Church|Παλαιοχωράκι||
B|pera-kalentini|Pera Kalentini|Πέρα Καλεντίνη|Beheading of Saint John the Forerunner|Αποτομής Κεφαλής Τιμίου Προδρόμου|Parish Church|Πέρα Καλεντίνη||
B|retsiana|Retsiana|Ρετσιανά|Saint George|Αγίου Γεωργίου|Parish Church|Ρετσιανά||
B|skoulikaria|Skoulikaria|Σκουληκαριά|Saint Nicholas|Αγίου Νικολάου|Parish Church|Σκουληκαριά||
B|tympa|Tympa|Τύμπα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Τύμπα||
B|chelona|Chelona|Χελώνα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Χελώνα||
C|agnanta|Agnanta|Άγναντα|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Άγναντα||
C|ampelochori|Ampelochori|Αμπελοχώρι|Saint Nicholas|Αγίου Νικολάου|Parish Church|Αμπελοχώρι||
C|ano-graikiko|Ano Graikiko|Άνω Γραικικό|Entrance of the Theotokos|Εισοδίων Θεοτόκου|Parish Church|Άνω Γραικικό||
C|kalarrytes|Kalarrytes|Καλαρρύτες|Saint Nicholas|Αγίου Νικολάου|Parish Church|Καλαρρύτες||
C|katarraktis|Katarraktis|Καταρράκτης|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Καταρράκτης||
C|kato-graikiko|Kato Graikiko|Κάτω Γραικικό|Prophet Elijah|Προφήτου Ηλίου|Parish Church|Κάτω Γραικικό||
C|koukoulia|Koukoulia|Κουκούλια|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Κουκούλια||
C|ktistades|Ktistades|Κτιστάδες|Saint Nicholas|Αγίου Νικολάου|Parish Church|Κτιστάδες||
C|lepiana|Lepiana|Λεπιανά|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|Λεπιανά||
C|makrykampos-lepiana|Makrykampos Lepiana|Μακρύκαμπος Λεπιανών|Saint Nicholas|Αγίου Νικολάου|Parish Church|Μακρύκαμπος Λεπιανών||
C|matsouki|Matsouki|Ματσούκι|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Ματσούκι||
C|melissourgoi|Melissourgoi|Μελισσουργοί|Saint Nicholas|Αγίου Νικολάου|Parish Church|Μελισσουργοί||
C|milea|Milea|Μηλέα|Transfiguration of the Savior|Μεταμορφώσεως Σωτήρος|Parish Church|Μηλέα||
C|mikrospilia|Mikrospilia|Μικροσπηλιά|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|Μικροσπηλιά||
C|mouchousti|Mouchousti|Μουχούστι|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Parish Church|Μουχούστι||
C|palaiochori-agnanta|Palaiochori Agnanta|Παλαιοχώρι Αγνάντων|Transfiguration of the Savior|Μεταμορφώσεως Σωτήρος|Parish Church|Παλαιοχώρι Αγνάντων||
C|pramanta|Pramanta|Πράμαντα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Πράμαντα||
C|ramia|Ramia|Ράμια|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Ράμια||
C|raftanaioi|Raftanaioi|Ραφταναίοι|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Parish Church|Ραφταναίοι||
C|romano-gouriana|Romano and Gouriana|Ρωμανό και Γουριανά|Saint Nicholas|Αγίου Νικολάου|Parish Church|Ρωμανό και Γουριανά||
C|sgara|Sgara|Σγάρα|Saint George|Αγίου Γεωργίου|Parish Church|Σγάρα||
C|tsopela|Tsopela|Τσόπελα|Saint Thomas|Αγίου Θωμά|Parish Church|Τσόπελα||
C|frasta|Frasta|Φράστα|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|Φράστα||
C|christoi|Christoi|Χριστοί|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου|Parish Church|Χριστοί||
D|ampelia-palaiokatouno|Ampelia Palaiokatouno|Αμπέλια Παλαιοκατούνου|Saints Theodore|Αγίων Θεοδώρων|Parish Church|Αμπέλια Παλαιοκατούνου||
D|ano-athamanio|Ano Athamanio|Άνω Αθαμάνιο|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Άνω Αθαμάνιο||
D|vourgareli|Vourgareli|Βουργαρέλι|Saint Nicholas|Αγίου Νικολάου|Parish Church|Βουργαρέλι||
D|theodoriana|Theodoriana|Θεοδώριανα|Saint George|Αγίου Γεωργίου|Parish Church|Θεοδώριανα||
D|kato-athamanio|Kato Athamanio|Κάτω Αθαμάνιο|Saint Charalambos|Αγίου Χαραλάμπους|Parish Church|Κάτω Αθαμάνιο||
D|kapsala|Kapsala|Κάψαλα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Κάψαλα||
D|kypseli|Kypseli|Κυψέλη|Saint Nicholas|Αγίου Νικολάου|Parish Church|Κυψέλη||
D|mesounta|Mesounta|Μεσούντα|Saint Nicholas|Αγίου Νικολάου|Parish Church|Μεσούντα||
D|palaiokatouno|Palaiokatouno|Παλαιοκάτουνο|Entrance of the Theotokos|Εισοδίων της Θεοτόκου|Parish Church|Παλαιοκάτουνο||
D|palaiochori-athamanio|Palaiochori Athamanio|Παλαιοχώρι Αθαμανίου|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Παλαιοχώρι Αθαμανίου||
D|pigi-tetrakomo|Pigi Tetrakomo|Πηγή Τετρακώμου|Saint Spyridon|Αγίου Σπυρίδωνος|Parish Church|Πηγή Τετρακώμου||
D|tetrakomo|Tetrakomo|Τετράκωμο|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|Τετράκωμο||
E|aidonia-piges|Aidonia Piges|Αηδόνια Πηγών|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|Αηδόνια Πηγών||
E|ampelia-megalochari|Ampelia Megalochari|Αμπέλια Μεγαλόχαρης|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Parish Church|Αμπέλια Μεγαλόχαρης||
E|astrochori|Astrochori|Αστροχώρι|Saint Barbara|Αγίας Βαρβάρας|Parish Church|Αστροχώρι||
E|vouliagmeno|Vouliagmeno|Βουλιαγμένο|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|Βουλιαγμένο||
E|elati|Elati|Ελάτη|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Parish Church|Ελάτη||
E|itea-piges|Itea Piges|Ιτέα Πηγών|Saints Basil and George|Αγίου Βασιλείου & Αγίου Γεωργίου|Parish Church|Ιτέα Πηγών||
E|kastanea|Kastanea|Καστανέα|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Καστανέα||
E|langada-miliana|Langada Miliana|Λαγκάδα Μηλιανών|Holy Apostles|Αγίων Αποστόλων|Parish Church|Λαγκάδα Μηλιανών||
E|megalochari|Megalochari|Μεγαλόχαρη|Saint Kosmas of Aetolia|Αγίου Κοσμά του Αιτωλού|Parish Church|Μεγαλόχαρη||
E|mesopyrgos|Mesopyrgos|Μεσόπυργος|Saint Demetrius|Αγίου Δημητρίου|Parish Church|Μεσόπυργος||
E|milea-piges|Milea Piges|Μηλέα Πηγών|Saint George|Αγίου Γεωργίου|Parish Church|Μηλέα Πηγών||
E|miliana|Miliana|Μηλιανά|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|Μηλιανά||
E|piges|Piges|Πηγές|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Parish Church|Πηγές||
E|stournari|Stournari|Στουρνάρι|Saint Nicholas|Αγίου Νικολάου|Parish Church|Στουρνάρι||
'''

SOURCE_URLS = {
    **DETAIL_URLS,
    **MONASTERY_URLS,
    **METROPOLITAN_CHAPEL_URLS,
    "LEGAL": LEGAL_2019,
    "COG": CHURCH_OF_GREECE_PAGE,
    "MONASTERY_DIRECTORY": MONASTERY_DIRECTORY,
    "METROPOLITAN_CHAPELS": METROPOLITAN_CHAPELS,
}


# key|kind|rank|English name|Greek local name|English seat|Greek address|
# source tokens|phones|contact tokens|live markers
OTHER_SOURCE = r'''
demetrius-sophia-chapel|parish|Parish Chapel|Saint Sophia Chapel of Saint Demetrius Parish, Arta|Παρεκκλήσιο Αγίας Σοφίας|Arta|Άρτα|ARTA_DEMETRIUS|||ΑΓΙΑΣ ΣΟΦΙΑΣ
demetrius-spyridon-chapel|parish|Parish Chapel|Saint Spyridon Chapel of Saint Demetrius Parish, Arta|Παρεκκλήσιο Αγίου Σπυρίδωνος|Arta|Άρτα|ARTA_DEMETRIUS|||ΑΓΙΟΥ ΣΠΥΡΙΔΩΝΟΣ
demetrius-constantine-chapel|parish|Parish Chapel|Saint Constantine Chapel of Saint Demetrius Parish, Arta|Παρεκκλήσιο Αγίου Κωνσταντίνου|Arta|Άρτα|ARTA_DEMETRIUS|||ΑΓΙΟΥ ΚΩΝΣΤΑΝΤΙΝΟΥ
george-paraskevi-chapel|parish|Parish Chapel|Saint Paraskevi Chapel of Saint George Parish, Arta|Παρεκκλήσιο Αγίας Παρασκευής|Arta|Άρτα|ARTA_GEORGE|||ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ
george-mark-chapel|parish|Parish Chapel|Saint Mark Chapel of Saint George Parish, Arta|Παρεκκλήσιο Αγίου Μάρκου|Arta|Άρτα|ARTA_GEORGE|||ΑΓΙΟΥ ΜΑΡΚΟΥ
george-nicholas-chapel|parish|Parish Chapel|Saint Nicholas Chapel of Saint George Parish, Arta|Παρεκκλήσιο Αγίου Νικολάου|Arta|Άρτα|ARTA_GEORGE|||ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ
panagia-kassopitra-chapel|parish|Parish Chapel|Panagia Kassopitra Chapel of Saint George Parish, Arta|Παρεκκλήσιο Κασσοπίτρας|Arta|Άρτα|ARTA_GEORGE|||ΚΑΣΣΟΠΙΤΡΑΣ
george-holy-theodores-chapel|parish|Parish Chapel|Holy Theodores Chapel of Saint George Parish, Arta|Παρεκκλήσιο Αγίων Θεοδώρων|Arta|Άρτα|ARTA_GEORGE|||ΑΓΙΩΝ ΘΕΟΔΩΡΩΝ
panagia-parigoritissa-chapel|parish|Parish Chapel|Panagia Parigoritissa Chapel of Pantokrator Parish, Arta|Παναγία Παρηγορήτισσα|Arta|Άρτα|ARTA_PANTOKRATOR|||ΠΑΝΑΓΙΑ ΠΑΡΗΓΟΡΗΤΙΣΣΑ
parigoritissa-archangels-chapel|parish|Parish Chapel|Holy Archangels Chapel at Panagia Parigoritissa, Arta|ΠΑΜ. ΤΑΞΙΑΡΧΩΝ (ΠΑΡΗΓΟΡΗΤΙΣΣΑΣ)|Arta|Άρτα|ARTA_PANTOKRATOR|||ΠΑΜ. ΤΑΞΙΑΡΧΩΝ
pantokrator-all-saints-chapel|parish|Parish Chapel|All Saints Chapel of Pantokrator Parish, Arta|Παρεκκλήσιο Αγίων Πάντων|Arta|Άρτα|ARTA_PANTOKRATOR|||ΑΓΙΩΝ ΠΑΝΤΩΝ
nicholas-theodora-chapel|parish|Parish Chapel|Saint Theodora Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Αγίας Θεοδώρας|Arta|Άρτα|ARTA_NICHOLAS|||ΑΓΙΑΣ ΘΕΟΔΩΡΑΣ
nicholas-annunciation-chapel|parish|Parish Chapel|Annunciation Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Ευαγγελιστρίας|Arta|Άρτα|ARTA_NICHOLAS|||ΕΥΑΓΓΕΛΙΣΤΡΙΑΣ
nicholas-transfiguration-chapel|parish|Parish Chapel|Transfiguration of the Savior Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Μεταμορφώσεως Σωτήρος|Arta|Άρτα|ARTA_NICHOLAS|||ΜΕΤΑΜΟΡΦΩΣΗΣ ΣΩΤΗΡΟΣ
nicholas-presentation-chapel|parish|Parish Chapel|Presentation of Christ Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Υπαπαντής|Arta|Άρτα|ARTA_NICHOLAS|||ΥΠΑΠΑΝΤΗΣ
nicholas-basil-chapel|parish|Parish Chapel|Saint Basil Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Αγίου Βασιλείου|Arta|Άρτα|ARTA_NICHOLAS|||ΑΓΙΟΥ ΒΑΣΙΛΕΙΟΥ
nicholas-george-batzis-chapel|parish|Parish Chapel|Saint George Batzis Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Αγίου Γεωργίου Μπατζή|Arta|Άρτα|ARTA_NICHOLAS|||ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΜΠΑΤΖΗ
nicholas-all-saints-castle-chapel|parish|Parish Chapel|All Saints of the Castle Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Αγίων Πάντων Κάστρου|Arta Castle|Κάστρο Άρτας|ARTA_NICHOLAS|||ΑΓΙΟΙ ΠΑΝΤΕΣ ΚΑΣΤΡΟΥ
nicholas-kosmas-chapel|parish|Parish Chapel|Saint Kosmas of Aetolia Chapel of Saint Nicholas Parish, Arta|Παρεκκλήσιο Αγίου Κοσμά Αιτωλού|Arta|Άρτα|ARTA_NICHOLAS|||ΑΓΙΟΥ ΚΟΣΜΑ ΑΙΤΩΛΟΥ
kleidi-paraskevi-chapel|parish|Parish Chapel|Saint Paraskevi Chapel of Saint Kyriaki Parish, Kleidi|Παρεκκλήσιο Αγίας Παρασκευής|Kleidi|Κλειδί|KLEIDI|||ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ
kleidi-george-chapel|parish|Parish Chapel|Saint George Chapel of Saint Kyriaki Parish, Kleidi|Παρεκκλήσιο Αγίου Γεωργίου|Kleidi|Κλειδί|KLEIDI|||ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ
kleidi-nicholas-chapel|parish|Parish Chapel|Saint Nicholas Chapel of Saint Kyriaki Parish, Kleidi|ΑΓΙΟΥ ΝΙΚΟΛΑΟΣ|Kleidi|Κλειδί|KLEIDI|||ΑΓΙΟΥ ΝΙΚΟΛΑΟΣ
kleidi-apostles-chapel|parish|Parish Chapel|Holy Apostles Chapel of Saint Kyriaki Parish, Kleidi|Παρεκκλήσιο Αγίων Αποστόλων|Kleidi|Κλειδί|KLEIDI|||ΑΓΙΩΝ ΑΠΟΣΤΟΛΩΝ
kleidi-beheading-chapel|parish|Parish Chapel|Beheading of Saint John the Forerunner Chapel, Kleidi|Παρεκκλήσιο Αποτομής Κάρας Τιμίου Προδρόμου|Kleidi|Κλειδί|KLEIDI|||ΑΠΟΤΟΜΗΣ ΚΑΡΑΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ
kleidi-nativity-forerunner-chapel|parish|Parish Chapel|Nativity of Saint John the Forerunner Chapel, Kleidi|Παρεκκλήσιο Γενεσίου Τιμίου Προδρόμου|Kleidi|Κλειδί|KLEIDI|||ΓΕΝΕΣΙΟΥ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ
kleidi-transfiguration-chapel|parish|Parish Chapel|Transfiguration of the Savior Chapel, Kleidi|Παρεκκλήσιο Μεταμορφώσεως Σωτήρος|Kleidi|Κλειδί|KLEIDI|||ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΣΩΤΗΡΟΣ
john-theologian-metropolitan-chapel|parish|Metropolitan Chapel|Saint John the Theologian Metropolitan Chapel at the Spiritual Center, Arta|Ιερός Ναός Αγίου Ιωάννου του Θεολόγου, Πνευματικό Κέντρο|Arta|Πνευματικό Κέντρο, Άρτα|METROPOLITAN_CHAPELS,JOHN|||Αγίου Ιωάννου του Θεολόγου;Πνευματικό Κέντρο
panagia-giatrissa-hospital-chapel|parish|Metropolitan Chapel|Panagia Giatrissa Hospital Chapel, Arta|Ιερός Ναός Παναγίας Γιάτρισσας, Νοσοκομείο Άρτης|Arta|Νοσοκομείο Άρτης|METROPOLITAN_CHAPELS,GIATRISSA|||Παναγίας Γιάτρισσας;Νοσοκομείο Άρτης
panagia-faneromeni-care-home-chapel|parish|Metropolitan Chapel|Panagia Faneromeni Metropolitan Chapel at the Care Home, Arta|Ιερός Ναός Παναγίας Φανερωμένης, Γηροκομείο|Arta|Γηροκομείο, Άρτα|METROPOLITAN_CHAPELS,FANEROMENI|||Παναγίας Φανερωμένης;Γηροκομείο
entrance-theotokos-metropolis-chapel|parish|Metropolitan Chapel|Entrance of the Theotokos Metropolitan Chapel, Arta|Ιερός Ναός Εισοδίων της Θεοτόκου, Μητρόπολη Άρτης|Arta|Μητρόπολη Άρτης|METROPOLITAN_CHAPELS,ENTRANCE|||Εισοδίων της Θεοτόκου
kato-panagia-monastery|monastery|Monastery|Kato Panagia Monastery, Arta|Ιερά Μονή Κάτω Παναγιάς|Arta|Κάτω Παναγιά, Άρτα|KATO_PANAGIA,COG|26810-27660,26810-24829|KATO_PANAGIA,COG|Ιερά Μονή Κάτω Παναγιάς;2681027660;2681024829
theotokio-monastery|monastery|Monastery|Theotokio Monastery, Arta|Ιερά Μονή Θεοτοκιού|Theotokio|Θεοτοκιό Άρτης|THEOTOKIO,COG|26810-83815|THEOTOKIO,COG|Ιερά Μονή Θεοτοκιού;26810-83815
panagia-rovelista-monastery|monastery|Monastery|Panagia Rovelista Monastery, Arta|Ιερά Μονή Παναγίας της Ροβέλιστας|Arta Regional Unit|Ροβέλιστα Άρτης|ROVELISTA,COG|26810-67760|ROVELISTA,COG|Παναγίας της Ροβέλιστας;26810-67760
melates-monastery|monastery|Monastery|Melates Monastery|Ιερά Μονή Μελατών|Melates|Μελάτες Άρτης|MELATES,COG|||Ιερά Μονή Μελατών
paraskevi-pramanta-monastery|monastery|Monastery|Saint Paraskevi Monastery, Pramanta|Ιερά Μονή Αγίας Παρασκευής Πραμάντων|Pramanta|Πράμαντα Ιωαννίνων|PARASKEVI_PRAMANTA|||Αγίας Παρασκευής Πραμάντων;Δύναμη: 1
catherine-katarraktis-monastery|monastery|Monastery|Saint Catherine Monastery, Katarraktis|Ιερά Μονή Αγίας Αικατερίνης Καταρράκτου|Katarraktis|Καταρράκτης Άρτης|CATHERINE_KATARRAKTIS|26850-51267|CATHERINE_KATARRAKTIS|Αγίας Αικατερίνης Καταρράκτου;2685051267
panagia-hodegetria-metochion|monastery|Metochion|Panagia Hodegetria Metochion of Kato Panagia Monastery, Arta|Μετόχι Παναγίας Οδηγήτριας Ιεράς Μονής Κάτω Παναγιάς|Arta|Άρτα|KATO_PANAGIA|||Μετόχι της Ιεράς Μονής είναι η Παναγία Οδηγήτρια
vyliza-monastery-metochion|monastery|Metochion|Vyliza Monastery Metochion of Kato Panagia Monastery, Matsouki|Μοναστήρι της Βύλιζας, Μετόχι Ιεράς Μονής Κάτω Παναγιάς|Matsouki|Ματσούκι Τζουμέρκων|KATO_PANAGIA|||μετόχια του;μοναστήρι της Βύλιζας;Ματσούκι
george-vourgareli-metochion|monastery|Metochion|Saint George Monastery Metochion of Melates Monastery, Vourgareli|Μετόχι Ιεράς Μονής Μελατών, Μονή Αγίου Γεωργίου Βουργαρελίου|Vourgareli|Βουργαρέλι Άρτης|GEORGE_VOURGARELI|||αποτελεί σήμερα μετόχι;Ιεράς Μονής Μελατών
anna-kato-panagia-chapel|monastery|Monastery Chapel|Saint Anna Chapel at Kato Panagia Monastery|Παρεκκλήσι Αγίας Άννας Ιεράς Μονής Κάτω Παναγιάς|Arta|Ιερά Μονή Κάτω Παναγιάς, Άρτα|KATO_PANAGIA|||παρεκκλήσι της Αγίας Άννας
zacharias-kato-panagia-church|monastery|Monastery Church|Saint Zacharias the New Martyr Church at Kato Panagia Monastery|Ναός Νεομάρτυρος Αγίου Ζαχαρίου του εξ Άρτης|Arta|Έξω από την Ιερά Μονή Κάτω Παναγιάς, Άρτα|KATO_PANAGIA|||ναός προς τιμήν του νεομάρτυρος Αγίου Ζαχαρίου
'''


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def split_values(value, separator=","):
    return [item.strip() for item in value.split(separator) if item.strip()]


def source_values(value):
    return [SOURCE_URLS[token.strip()] for token in value.split(",")
            if token.strip()]


def parse_parishes():
    rows = []
    lines = [line for line in PARISH_SOURCE.splitlines() if line.strip()]
    if len(lines) != 97:
        raise ValueError("expected 97 exact Arta parish rows")
    regional_counts = Counter()
    for number, raw in enumerate(lines, 1):
        parts = raw.split("|")
        if len(parts) != 10:
            raise ValueError("invalid Arta parish row: %s" % raw)
        (region, key, seat, greek_seat, dedication, greek_dedication,
         rank, address, phones_text, detail_token) = parts
        regional_counts[region] += 1
        if rank == "Metropolitan Church":
            name = "%s of %s, %s" % (rank, dedication, seat)
            local = "Μητροπολιτικός Ναός %s, %s" % (
                greek_dedication, greek_seat
            )
        else:
            name = "Parish Church of %s, %s" % (dedication, seat)
            local = "Ιερός Ναός %s, %s" % (
                greek_dedication, greek_seat
            )
        sources = [REGION_URLS[region], LEGAL_2019]
        directory_marker = {
            "kleisto": "Κοίμησης Θεοτόκου",
            "foteino": "Κοίμησης Θεοτόκου",
            "pera-kalentini": "Τιμίου Προδρόμου",
            "milea": "Μετομόρφωσης Σωτήρος",
            "palaiochori-agnanta": "Μεταμόρφωσης Σωτήρος",
        }.get(key, greek_dedication)
        markers = [directory_marker]
        if detail_token:
            sources.append(DETAIL_URLS[detail_token])
            markers.append(greek_dedication)
        row = {
            "id": "gr-arta-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": sources,
            "live_markers": markers,
        }
        phones = split_values(phones_text)
        if phones:
            row["phones"] = phones
            row["contact_sources"] = [DETAIL_URLS[detail_token]]
            row["contact_checked"] = CHECKED
        rows.append(row)
    expected_regions = {
        "A_CITY": 7,
        "A_NEAR": 16,
        "B": 24,
        "C": 24,
        "D": 12,
        "E": 14,
    }
    if dict(sorted(regional_counts.items())) != expected_regions:
        raise ValueError("Arta regional parish totals drifted")
    return rows


def parse_other_rows(start_number):
    rows = []
    lines = [line for line in OTHER_SOURCE.splitlines() if line.strip()]
    if len(lines) != 41:
        raise ValueError("expected 41 exact Arta dependent rows")
    for offset, raw in enumerate(lines, start_number):
        parts = raw.split("|")
        if len(parts) != 11:
            raise ValueError("invalid Arta dependent row: %s" % raw)
        (key, kind, rank, name, local, seat, address, source_tokens,
         phones_text, contact_tokens, marker_text) = parts
        row = {
            "id": "gr-arta-%03d-%s" % (offset, key),
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": source_values(source_tokens),
            "live_markers": split_values(marker_text, ";"),
        }
        phones = split_values(phones_text)
        if phones:
            row["phones"] = phones
        contact_sources = source_values(contact_tokens)
        if contact_sources:
            row["contact_sources"] = contact_sources
            row["contact_checked"] = CHECKED
        rows.append(row)
    return rows


PARISH_ROWS = parse_parishes()
OTHER_ROWS = parse_other_rows(len(PARISH_ROWS) + 1)
ROWS = PARISH_ROWS + OTHER_ROWS
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 138
EXPECTED_OWNER_COUNTS = {PARENT: 138}
EXPECTED_KINDS = {"monastery": 11, "parish": 127}
EXPECTED_RANKS = {
    "Metochion": 3,
    "Metropolitan Chapel": 4,
    "Metropolitan Church": 1,
    "Monastery": 6,
    "Monastery Chapel": 1,
    "Monastery Church": 1,
    "Parish Chapel": 26,
    "Parish Church": 96,
}
EXPECTED_CONTACT_BODIES = 14
EXPECTED_PHONE_BODIES = 14
EXPECTED_PHONE_VALUES = 18
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 138
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imartis.gr",
    "www.imartis.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PERSON_KEYS = {
    "abbess", "abbot", "bishop", "clergy", "clergy_name",
    "contact_name", "person", "rector",
}
PERSON_NAME_RE = re.compile(
    r"\b(?:Bishop|Archbishop|Abbot|Abbess|Archpriest|"
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
        raise ValueError("Arta candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Arta candidate ledger date drifted")
    expected_summary = {
        PARENT: 138,
        "total": 138,
        "legal_parish_rows": 97,
        "parish_kind_rows": 127,
        "monastery_kind_rows": 11,
        "current_exact_dependent_worship_rows": 41,
        "contact_bodies": 14,
        "phone_bodies": 14,
        "public_phone_values": 18,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 138,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Arta ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Arta ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Arta ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [item.get("candidate_id")
                     for item in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Arta ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Arta ledger has forbidden punctuation")
    reject_person_fields(ledger, "Arta ledger")
    if PERSON_NAME_RE.search(rendered):
        raise ValueError("Arta ledger contains a clergy name")
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
        raise ValueError("Arta English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Arta rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Arta kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Arta parent totals drifted")
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
    expected = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected:
        raise ValueError("Arta contact coverage drifted: %r" % (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def safe_url(value):
    parsed = urlsplit(value)
    return urlunsplit((
        parsed.scheme,
        parsed.netloc,
        quote(parsed.path, safe="/%"),
        quote(parsed.query, safe="=&,%"),
        parsed.fragment,
    ))


def fetch(url):
    request = Request(safe_url(url), headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
        "Cache-Control": "no-cache",
    })
    last_error = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                try:
                    payload = response.read()
                except IncompleteRead as exc:
                    if len(exc.partial) < 10000:
                        raise
                    payload = exc.partial
                content_type = response.headers.get("Content-Type", "").lower()
            return payload, content_type
        except OSError as exc:
            last_error = exc
            time.sleep(attempt + 1)
    raise last_error


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = unicase(text)
    return re.sub(r"\s+", " ", text)


def compact_digits(value):
    return re.sub(r"\D", "", value)


def check_live_sources():
    required = {url for row in ROWS for url in row.get("sources", [])}
    required.update({MONASTERY_DIRECTORY, METROPOLITAN_CHAPELS})
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
        page = normalized_page(payload)
        if "please wait while your request is being verified" in page:
            raise ValueError("live source returned a verification page: %s" % url)
        cache[url] = page

    monastery_directory = cache[MONASTERY_DIRECTORY]
    for marker in (
            "Ιερά Μονή Κάτω Παναγιάς", "Ιερά Μονή Θεοτοκιού",
            "Ιερά Μονή Παναγίας της Ροβέλιστας", "Ιερά Μονή Μελατών",
            "Ιερά Μονή Αγίας Παρασκευής Πραμάντων",
            "Ιερά Μονή Αγίας Αικατερίνης Καταρράκτου",
            "Ιερά Μονή Αγίου Γεωργίου Βουργαρελίου"):
        if unicase(marker) not in monastery_directory:
            raise ValueError("monastery directory lacks marker: %s" % marker)
    cog = cache[CHURCH_OF_GREECE_PAGE]
    for marker in (
            "Ι. Μ. Μελατών", "Κάτω Παναγίας", "Ροβελίστης",
            "Ι. Μ. Θεοτοκιού", "26810-27660", "26810-67760",
            "83 815"):
        if unicase(marker) not in cog:
            raise ValueError("Church of Greece page lacks marker: %s" % marker)

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
    print("Arta live sources: %d URLs checked" % len(required))


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
        print(
            "Arta: 138 exact bodies; 97 parishes, 30 parish and "
            "metropolitan chapels, 6 monasteries, 3 metochia, and "
            "2 monastery worship bodies"
        )
        print("Contacts: 14 bodies; 18 phone values; no emails or body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Arta: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
