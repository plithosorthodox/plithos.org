#!/usr/bin/env python3
"""Build the exact current Servia and Kozani body roster."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


PARENT = "ep-servia-kozani"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "servia_kozani_country.json"

LOCAL_BASE = "https://imsk.gr"


def local_url(slug):
    return LOCAL_BASE + "/" + quote(slug) + "/"


REGION_URLS = {
    "kozani": local_url("αρχιερατική-περιφέρεια-κοζάνης"),
    "aiani": local_url("αρχιερατική-περιφέρεια-αιανής"),
    "velvento": local_url("αρχιερατική-περιφέρεια-βελβενδού"),
    "drepano": local_url("αρχιερατική-περιφέρεια-δρεπάνου"),
    "krokos": local_url("αρχιερατική-περιφέρεια-κρόκου"),
    "servia": local_url("αρχιερατική-περιφέρεια-σερβίων"),
}
MONASTERIES_URL = local_url("ιερές-μονές")
PROGRAM_URL = local_url("πρόγραμμα-ενοριών")
BARADATOS_URL = local_url("εορτή-αγίου-βαραδάτου")
EP_URL = "https://ec-patr.org/entities/iera-mitropoli-servion-kozanis/"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"

NICHOLAS_SITE = "http://agiosnikolaoskozanis.gr/"
NICHOLAS_CONTACT = NICHOLAS_SITE + quote("επικοινωνήστε") + "/"
ATHANASIUS_SITE = "https://inaakoz.blogspot.com/"
TRANSFIGURATION_SITE = "https://inmetkoz.blogspot.com/"


# Fields are region, English seat, Greek seat, English dedication, Greek
# dedication, rank, and whether the exact parish appears in the 2019
# Church of Greece regulation. The two current additions are named on the
# current Krokos page and are not inferred from the Patriarchate aggregate.
PARISH_SOURCE = r"""
kozani|Kozani|Κοζάνη|Saint Nicholas|Αγίου Νικολάου|Metropolitan Cathedral|1
kozani|Kozani|Κοζάνη|Saint Demetrius|Αγίου Δημητρίου|Parish Church|1
kozani|Kozani|Κοζάνη|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
kozani|Kozani|Κοζάνη|Saint Nikanor|Αγίου Νικάνορος|Parish Church|1
kozani|Kozani|Κοζάνη|Saint Athanasius|Αγίου Αθανασίου|Parish Church|1
kozani|Kozani|Κοζάνη|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|1
kozani|Kozani|Κοζάνη|Panagia Faneromeni|Παναγίας Φανερωμένης|Parish Church|1
kozani|Kozani|Κοζάνη|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church|1
kozani|Alonakia|Αλωνάκια|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church|1
kozani|Anthotopos|Ανθότοπος|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
kozani|Vatero|Βατερό|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
kozani|Exochi|Εξοχή|Prophet Elijah|Προφήτου Ηλιού|Parish Church|1
kozani|Kalamia|Καλαμιά|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church|1
kozani|Nea Kardia|Νέα Καρδιά|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
kozani|Koila|Κοίλα|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Parish Church|1
kozani|Lygeri|Λυγερή|Saint George|Αγίου Γεωργίου|Parish Church|1
kozani|Melissia|Μελίσσια|Saint George|Αγίου Γεωργίου|Parish Church|1
kozani|Nea Nikopolis|Νέα Νικόπολη|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church|1
kozani|Xirolimni|Ξηρολίμνη|Saint George|Αγίου Γεωργίου|Parish Church|1
kozani|Oinoi|Οινόη|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church|1
kozani|Petrana|Πετρανά|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church|1
kozani|Ptelea|Πτελέα|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|1
kozani|Skiti|Σκήτη|Saint Demetrius|Αγίου Δημητρίου|Parish Church|1
aiani|Aiani|Αιανή|Saint George|Αγίου Γεωργίου|Parish Church|1
aiani|Agia Paraskevi|Αγία Παρασκευή|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|1
aiani|Argillos|Άργιλλος|Saint George|Αγίου Γεωργίου|Parish Church|1
aiani|Kerasia|Κερασιά|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|1
aiani|Kleitos|Κλείτος|Saint George|Αγίου Γεωργίου|Parish Church|1
aiani|Kteni|Κτένι|Saint Demetrius|Αγίου Δημητρίου|Parish Church|1
aiani|Lefkovrysi|Λευκόβρυση|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
aiani|Lefkopigi|Λευκοπηγή|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|1
aiani|Protochori|Πρωτοχώρι|Saint George|Αγίου Γεωργίου|Parish Church|1
aiani|Rodiani|Ροδιανή|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|1
velvento|Velvento|Βελβεντό|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
velvento|Velvento|Βελβεντό|Saint Dionysius|Αγίου Διονυσίου|Parish Church|1
velvento|Agia Kyriaki|Αγία Κυριακή|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
velvento|Vathylakkos|Βαθύλακκος|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|1
velvento|Imera|Ίμερα|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Parish Church|1
velvento|Katafygio|Καταφύγιο|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
velvento|Lefkara|Λεύκαρα|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
velvento|Mesiani|Μεσιανή|Saint George|Αγίου Γεωργίου|Parish Church|1
velvento|Neraida|Νεράιδα|Saint George|Αγίου Γεωργίου|Parish Church|1
velvento|Palaiogratsano|Παλαιογράτσανο|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
velvento|Platanorevma|Πλατανόρευμα|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church|1
velvento|Polyfyto|Πολύφυτο|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|1
velvento|Roditis|Ροδίτης|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
drepano|Agios Dimitrios|Άγιος Δημήτριος|Saint Demetrius|Αγίου Δημητρίου|Parish Church|1
drepano|Agios Charalambos|Άγιος Χαράλαμπος|Saint Charalambos|Αγίου Χαραλάμπους|Parish Church|1
drepano|Akrini|Ακρινή|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church|1
drepano|Avgi|Αυγή|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church|1
drepano|Voskochori|Βοσκοχώρι|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|1
drepano|Galani|Γαλάνη|Ascension of the Savior|Αναλήψεως του Σωτήρος|Parish Church|1
drepano|Ano Drepano|Άνω Δρέπανο|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
drepano|Kato Drepano|Κάτω Δρέπανο|Holy Trinity|Αγίας Τριάδος|Parish Church|1
drepano|Thymaria|Θυμαριά|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church|1
drepano|Kapnochori|Καπνοχώρι|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
drepano|Koilada|Κοιλάδα|Prophet Elijah|Προφήτου Ηλιού|Parish Church|1
drepano|Livera|Λιβερά|Exaltation of the Precious Cross|Υψώσεως του Τιμίου Σταυρού|Parish Church|1
drepano|Mavrodendri|Μαυροδένδρι|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
drepano|Pontokomi|Ποντοκώμη|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church|1
drepano|Polymylos|Πολύμυλος|Saint George|Αγίου Γεωργίου|Parish Church|1
drepano|Ryakio|Ρυάκιο|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
drepano|Sidera|Σιδερά|Saint George|Αγίου Γεωργίου|Parish Church|1
drepano|Tetralofos|Τετράλοφος|Panagia of Blachernae|Παναγίας Βλαχερνών|Parish Church|1
drepano|Nea Charavgi|Νέα Χαραυγή|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
krokos|Krokos|Κρόκος|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
krokos|Amygdalia|Αμυγδαλιά|Saint John the Theologian|Αγίου Ιωάννου του Θεολόγου|Parish Church|1
krokos|Anatoli|Ανατολή|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|0
krokos|Kaisareia|Καισάρεια|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|1
krokos|Karyditsa|Καρυδίτσα|Saint John the Theologian|Αγίου Ιωάννου του Θεολόγου|Parish Church|1
krokos|Kipos|Κήπος|Saint George|Αγίου Γεωργίου|Parish Church|1
krokos|Kontovouni|Κοντοβούνι|Saint Athanasius|Αγίου Αθανασίου|Parish Church|1
krokos|Ano Komi|Άνω Κώμη|Saint George|Αγίου Γεωργίου|Parish Church|1
krokos|Kato Komi|Κάτω Κώμη|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
krokos|Milea|Μηλέα|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|1
krokos|Pyrgos|Πύργος|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
krokos|Sparto|Σπάρτο|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου|Parish Church|1
krokos|Stavroti|Σταυρωτή|Holy Trinity|Αγίας Τριάδος|Parish Church|0
servia|Servia|Σέρβια|Saint Kyriaki|Αγίας Κυριακής|Cathedral Church|1
servia|Servia|Σέρβια|Saint George|Αγίου Γεωργίου|Parish Church|1
servia|Avles|Αυλές|Saint George|Αγίου Γεωργίου|Parish Church|1
servia|Goules|Γούλες|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
servia|Elati|Ελάτη|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
servia|Kastania|Καστανιά|Saints Theodore|Αγίων Θεοδώρων|Parish Church|1
servia|Kranidia|Κρανίδια|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
servia|Lava|Λάβα|Saint Achilles|Αγίου Αχιλλείου|Parish Church|1
servia|Lazarades|Λαζαράδες|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church|1
servia|Livadero|Λιβαδερό|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
servia|Metaxas|Μεταξάς|Saint Demetrius|Αγίου Δημητρίου|Parish Church|1
servia|Mikrovalto|Μικρόβαλτο|Saint George|Αγίου Γεωργίου|Parish Church|1
servia|Polyrrhacho|Πολύρραχο|Saint George|Αγίου Γεωργίου|Parish Church|1
servia|Prosilio|Προσήλιο|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
servia|Rymnio|Ρύμνιο|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|1
servia|Tranovalto|Τρανόβαλτο|Saint Athanasius|Αγίου Αθανασίου|Parish Church|1
servia|Trigoniko|Τριγωνικό|Saint Demetrius|Αγίου Δημητρίου|Parish Church|1
servia|Frourio|Φρούριο|Saint Nicholas|Αγίου Νικολάου|Parish Church|1
"""


PARISH_CONTACTS = {
    ("Κοζάνη", "Αγίου Νικολάου"): {
        "phones": ["+30 2461034433", "+30 2461035929", "+30 2461028801"],
        "emails": ["agiosnikolaoskozanis@yahoo.com"],
        "site": NICHOLAS_SITE,
        "contact": NICHOLAS_CONTACT,
        "address": ["Πανδώρας 2", "50131 Κοζάνη", "Ελλάδα"],
    },
    ("Κοζάνη", "Αγίου Δημητρίου"): {"phones": ["+30 2461034762"]},
    ("Κοζάνη", "Αγίων Κωνσταντίνου και Ελένης"): {
        "phones": ["+30 2461034827", "+30 2461033891"],
    },
    ("Κοζάνη", "Αγίου Νικάνορος"): {"phones": ["+30 2461022840"]},
    ("Κοζάνη", "Αγίας Παρασκευής"): {"phones": ["+30 2461030584"]},
    ("Κοζάνη", "Αγίου Αθανασίου"): {
        "phones": ["+30 2461030320"], "site": ATHANASIUS_SITE,
    },
    ("Κοζάνη", "Παναγίας Φανερωμένης"): {"phones": ["+30 2461032855"]},
    ("Κοζάνη", "Μεταμορφώσεως του Σωτήρος"): {
        "phones": ["+30 2461034322"], "site": TRANSFIGURATION_SITE,
    },
    ("Αλωνάκια", "Γεννήσεως της Θεοτόκου"): {"phones": ["+30 2461091089"]},
    ("Ανθότοπος", "Αγίων Κωνσταντίνου και Ελένης"): {"phones": ["+30 2461091089"]},
    ("Βατερό", "Κοιμήσεως της Θεοτόκου"): {"phones": ["+30 2461039009"]},
    ("Εξοχή", "Προφήτου Ηλιού"): {"phones": ["+30 2461022572"]},
    ("Καλαμιά", "Αγίου Παντελεήμονος"): {"phones": ["+30 2461091700"]},
    ("Νέα Καρδιά", "Αγίου Νικολάου"): {"phones": ["+30 2461501735"]},
    ("Κοίλα", "Αγίων Πέτρου και Παύλου"): {"phones": ["+30 2461045710"]},
    ("Λυγερή", "Αγίου Γεωργίου"): {"phones": ["+30 2461091166"]},
    ("Νέα Νικόπολη", "Γεννήσεως της Θεοτόκου"): {"phones": ["+30 2461020609"]},
    ("Ξηρολίμνη", "Αγίου Γεωργίου"): {"phones": ["+30 2461091700"]},
    ("Σκήτη", "Αγίου Δημητρίου"): {"phones": ["+30 2461091166"]},
    ("Αιανή", "Αγίου Γεωργίου"): {"phones": ["+30 2461098309"]},
    ("Βελβεντό", "Κοιμήσεως της Θεοτόκου"): {
        "phones": ["+30 2464031994", "+30 2464500288"],
    },
    ("Βελβεντό", "Αγίου Διονυσίου"): {
        "phones": ["+30 2464031946", "+30 2464031863"],
    },
    ("Αγία Κυριακή", "Κοιμήσεως της Θεοτόκου"): {"phones": ["+30 2464031863"]},
    ("Πλατανόρευμα", "Γεννήσεως της Θεοτόκου"): {"phones": ["+30 2464021065"]},
    ("Κάτω Δρέπανο", "Αγίας Τριάδος"): {
        "phones": ["+30 2461092990", "+30 2461030892"],
    },
    ("Άγιος Δημήτριος", "Αγίου Δημητρίου"): {
        "phones": ["+30 2461094690", "+30 2461090860"],
    },
    ("Κρόκος", "Αγίου Νικολάου"): {"phones": ["+30 2461064182"]},
    ("Σέρβια", "Αγίας Κυριακής"): {
        "phones": ["+30 2464022235", "+30 2464023553"],
    },
    ("Σέρβια", "Αγίου Γεωργίου"): {
        "phones": ["+30 2464021235", "+30 2464022694"],
    },
    ("Γούλες", "Αγίου Νικολάου"): {"phones": ["+30 2464023472"]},
    ("Κρανίδια", "Αγίου Νικολάου"): {"phones": ["+30 2464024422"]},
    ("Λαζαράδες", "Κοιμήσεως της Θεοτόκου"): {"phones": ["+30 2464051133"]},
    ("Λιβαδερό", "Αγίου Νικολάου"): {"phones": ["+30 2464041268"]},
    ("Μεταξάς", "Αγίου Δημητρίου"): {"phones": ["+30 2464061253"]},
    ("Μικρόβαλτο", "Αγίου Γεωργίου"): {"phones": ["+30 2464051677"]},
    ("Πολύρραχο", "Αγίου Γεωργίου"): {"phones": ["+30 2464023762"]},
    ("Προσήλιο", "Αγίου Νικολάου"): {"phones": ["+30 2464041268"]},
    ("Ρύμνιο", "Τιμίου Προδρόμου"): {"phones": ["+30 2464051605"]},
    ("Τρανόβαλτο", "Αγίου Αθανασίου"): {"phones": ["+30 2464051231"]},
    ("Τριγωνικό", "Αγίου Δημητρίου"): {"phones": ["+30 2464051605"]},
    ("Φρούριο", "Αγίου Νικολάου"): {"phones": ["+30 2464051133"]},
}


ADDITIONAL_SOURCE = [
    {
        "key": "anargyroi-pilgrimage-kozani",
        "kind": "parish", "rank": "Pilgrimage Church",
        "name": "Holy Unmercenaries Pilgrimage Church in Kozani",
        "local": "Ιερός Προσκυνηματικός Ναός Αγίων Αναργύρων Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461036192", "+30 2461092907"],
        "sources": [REGION_URLS["kozani"], LEGAL_URL, PROGRAM_URL],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "george-exochi",
        "kind": "parish", "rank": "Church",
        "name": "Saint George Church in Exochi",
        "local": "Ιερός Ναός Αγίου Γεωργίου Εξοχής",
        "seat": "Exochi", "local_seat": "Εξοχή",
        "sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "panteleimon-care-home",
        "kind": "parish", "rank": "Institutional Church",
        "name": "Saint Panteleimon Church at the Tialeio Ecclesiastical Care Home",
        "local": "Ιδρυματικός Ιερός Ναός Αγίου Παντελεήμονος Τιαλείου Εκκλησιαστικού Γηροκομείου",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461030478", "+30 2461031834", "+30 2461092907"],
        "sources": [REGION_URLS["kozani"], EP_URL],
        "contact_sources": [REGION_URLS["kozani"], EP_URL],
    },
    {
        "key": "george-cemetery-kozani",
        "kind": "parish", "rank": "Cemetery Church",
        "name": "Saint George Cemetery Church in Kozani",
        "local": "Κοιμητηριακός Ιερός Ναός Αγίου Γεωργίου Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461026669", "+30 2461034772"],
        "sources": [REGION_URLS["kozani"], PROGRAM_URL],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "luke-hospital-kozani",
        "kind": "parish", "rank": "Hospital Church",
        "name": "Saint Luke Hospital Church in Kozani",
        "local": "Νοσοκομειακός Ιερός Ναός Αγίου Λουκά Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461067795", "+30 2461031957"],
        "sources": [REGION_URLS["kozani"]],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "eleutherios-country-kozani", "kind": "parish",
        "rank": "Country Church", "name": "Saint Eleutherius Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Αγίου Ελευθερίου Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461034762"], "sources": [REGION_URLS["kozani"]],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "anna-country-kozani", "kind": "parish", "rank": "Country Church",
        "name": "Saint Anna Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Αγίας Άννης Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461034322"], "sources": [REGION_URLS["kozani"], TRANSFIGURATION_SITE],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "thomas-country-kozani", "kind": "parish", "rank": "Country Church",
        "name": "Saint Thomas Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Αγίου Θωμά Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461026749", "+30 2461034433"],
        "sources": [REGION_URLS["kozani"]], "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "forty-martyrs-country-kozani", "kind": "parish",
        "rank": "Country Church", "name": "Forty Martyrs Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Αγίων Τεσσαράκοντα Μαρτύρων Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461034762"], "sources": [REGION_URLS["kozani"]],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "theodore-country-kozani", "kind": "parish", "rank": "Country Church",
        "name": "Saints Theodore Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Αγίων Θεοδώρων Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461022840"], "sources": [REGION_URLS["kozani"]],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "kyriaki-country-kozani", "kind": "parish", "rank": "Country Church",
        "name": "Saint Kyriaki Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Αγίας Κυριακής Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461022840"], "sources": [REGION_URLS["kozani"]],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "life-giving-spring-country-kozani", "kind": "parish",
        "rank": "Country Church", "name": "Life-giving Spring Country Church in Kozani",
        "local": "Ιερό Εξωκκλήσιο Ζωοδόχου Πηγής Κοζάνης",
        "seat": "Kozani", "local_seat": "Κοζάνη",
        "phones": ["+30 2461031605"], "sources": [REGION_URLS["kozani"]],
        "contact_sources": [REGION_URLS["kozani"]],
    },
    {
        "key": "baradatos-metropolitan-chapel", "kind": "parish",
        "rank": "Metropolitan Chapel",
        "name": "Saint Baradatos Metropolitan Chapel at Lake Polyfytos",
        "local": "Ιερό Μητροπολιτικό Παρεκκλήσιο Οσίου Βαραδάτου",
        "seat": "Lake Polyfytos", "local_seat": "Λίμνη Πολυφύτου",
        "sources": [EP_URL, BARADATOS_URL],
    },
]


MONASTIC_SOURCE = [
    {
        "key": "holy-trinity-lariou", "rank": "Monastery",
        "name": "Holy Trinity Lariou Monastery", "local": "Ιερά Μονή Αγίας Τριάδος Λαριούς",
        "seat": "Aiani", "local_seat": "Αιανή", "postal": "50004",
        "phones": ["+30 2461098209"],
    },
    {
        "key": "anthony-siapka", "rank": "Patriarchal and Stavropegic Monastery",
        "name": "Saint Anthony of Siapka Patriarchal and Stavropegic Monastery",
        "local": "Πατριαρχική και Σταυροπηγιακή Μονή Αγίου Αντωνίου Σιάπκας",
        "seat": "Kastania", "local_seat": "Καστανιά Σερβίων", "postal": "50500",
        "phones": ["+30 2464021806", "+30 6979851211"],
    },
    {
        "key": "nectarios-palaiogratsano", "rank": "Monastery",
        "name": "Saint Nektarios Monastery in Palaiogratsano",
        "local": "Ιερά Μονή Αγίου Νεκταρίου Παλαιογρατσάνου",
        "seat": "Palaiogratsano", "local_seat": "Παλαιογράτσανο", "postal": "50400",
        "phones": ["+30 2464024667"],
    },
    {
        "key": "panagia-zidaniou", "rank": "Monastery",
        "name": "Panagia Zidaniou Monastery", "local": "Ιερά Μονή Παναγίας Ζιδανίου",
        "seat": "Mikrovalto", "local_seat": "Μικρόβαλτο", "postal": "50500",
        "phones": ["+30 2464051210"],
    },
    {
        "key": "holy-trinity-velvento", "rank": "Monastic Church",
        "name": "Holy Trinity Monastic Church in Velvento",
        "local": "Μοναστηριακός Ναός Αγίας Τριάδος Βελβεντού",
        "seat": "Velvento", "local_seat": "Βελβεντό", "postal": "50400",
    },
    {
        "key": "john-forerunner-vazelon", "rank": "Institutional Monastic Church",
        "name": "Saint John the Forerunner of Vazelon Institutional Monastic Church",
        "local": "Ιδρυματικός Ναός Τιμίου Προδρόμου Βαζελώνος",
        "seat": "Kozani Regional Unit", "local_seat": "Περιφερειακή Ενότητα Κοζάνης",
        "postal": "50100", "sources": [EP_URL],
    },
]


FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
ALLOWED_HOSTS = {
    "imsk.gr", "www.imsk.gr", "ec-patr.org", "ecclesiagreece.gr",
    "agiosnikolaoskozanis.gr", "inaakoz.blogspot.com",
    "inmetkoz.blogspot.com",
}


def unique(values):
    result = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:76]


def parse_parish_source():
    rows = []
    for raw in (line for line in PARISH_SOURCE.splitlines() if line.strip()):
        parts = raw.split("|")
        if len(parts) != 7:
            raise ValueError("invalid Servia and Kozani parish row: %s" % raw)
        region, seat, local_seat, dedication, local_dedication, rank, legal = parts
        rows.append({
            "region": region, "seat": seat, "local_seat": local_seat,
            "dedication": dedication, "local_dedication": local_dedication,
            "rank": rank, "legal": legal == "1",
        })
    if len(rows) != 96:
        raise ValueError("expected 96 exact current parishes, found %d" % len(rows))
    if sum(item["legal"] for item in rows) != 94:
        raise ValueError("expected 94 exact legal parish rows")
    return rows


def parish_name(source):
    if source["rank"] == "Metropolitan Cathedral":
        return "%s Metropolitan Cathedral in %s" % (
            source["dedication"], source["seat"]
        )
    if source["rank"] == "Cathedral Church":
        return "%s Cathedral Church in %s" % (
            source["dedication"], source["seat"]
        )
    return "%s Parish Church in %s" % (source["dedication"], source["seat"])


def build_rows():
    rows = []
    for source in parse_parish_source():
        number = len(rows) + 1
        sources = [REGION_URLS[source["region"]]]
        if source["legal"]:
            sources.append(LEGAL_URL)
        contact = PARISH_CONTACTS.get(
            (source["local_seat"], source["local_dedication"]), {}
        )
        if contact.get("site"):
            sources.append(contact["site"])
        item = {
            "id": "gr-ep-servia-kozani-%03d-%s" % (
                number, slug(source["dedication"] + " " + source["seat"])
            ),
            "parent": PARENT, "kind": "parish", "rank": source["rank"],
            "name": parish_name(source),
            "local": "Ιερός Ναός %s %s" % (
                source["local_dedication"], source["local_seat"]
            ),
            "seat": source["seat"], "country": "GR",
            "address": list(contact.get("address") or [
                source["local_seat"], "Περιφερειακή Ενότητα Κοζάνης", "Ελλάδα"
            ]),
            "sources": unique(sources),
        }
        for key in ("phones", "emails"):
            if contact.get(key):
                item[key] = list(contact[key])
        if contact.get("site"):
            item["site"] = contact["site"]
        if contact:
            contact_sources = [REGION_URLS[source["region"]]]
            if contact.get("contact"):
                contact_sources.append(contact["contact"])
            if contact.get("site"):
                contact_sources.append(contact["site"])
            item["contact_sources"] = unique(contact_sources)
            item["contact_checked"] = CHECKED
        rows.append(item)

    for source in ADDITIONAL_SOURCE:
        number = len(rows) + 1
        item = {
            "id": "gr-ep-servia-kozani-%03d-%s" % (number, source["key"]),
            "parent": PARENT, "kind": source["kind"], "rank": source["rank"],
            "name": source["name"], "local": source["local"],
            "seat": source["seat"], "country": "GR",
            "address": [
                source["local_seat"], "Περιφερειακή Ενότητα Κοζάνης", "Ελλάδα"
            ],
            "sources": list(source["sources"]),
        }
        for key in ("phones", "emails"):
            if source.get(key):
                item[key] = list(source[key])
        if source.get("site"):
            item["site"] = source["site"]
        if source.get("contact_sources"):
            item["contact_sources"] = list(source["contact_sources"])
            item["contact_checked"] = CHECKED
        rows.append(item)

    for source in MONASTIC_SOURCE:
        number = len(rows) + 1
        sources = list(source.get("sources") or [MONASTERIES_URL, EP_URL])
        item = {
            "id": "gr-ep-servia-kozani-%03d-%s" % (number, source["key"]),
            "parent": PARENT, "kind": "monastery", "rank": source["rank"],
            "name": source["name"], "local": source["local"],
            "seat": source["seat"], "country": "GR",
            "address": [
                source["local_seat"], source["postal"] + " Π.Ε. Κοζάνης", "Ελλάδα"
            ],
            "sources": sources,
        }
        if source.get("phones"):
            item["phones"] = list(source["phones"])
            item["contact_sources"] = sources
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 115
EXPECTED_OWNER_COUNTS = {PARENT: 115}
EXPECTED_KINDS = {"monastery": 6, "parish": 109}
EXPECTED_RANKS = {
    "Cathedral Church": 1,
    "Cemetery Church": 1,
    "Church": 1,
    "Country Church": 7,
    "Hospital Church": 1,
    "Institutional Church": 1,
    "Institutional Monastic Church": 1,
    "Metropolitan Cathedral": 1,
    "Metropolitan Chapel": 1,
    "Monastic Church": 1,
    "Monastery": 3,
    "Parish Church": 94,
    "Patriarchal and Stavropegic Monastery": 1,
    "Pilgrimage Church": 1,
}
EXPECTED_CONTACT_BODIES = 56
EXPECTED_PHONE_BODIES = 56
EXPECTED_PHONE_VALUES = 72
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 3
EXPECTED_ADDRESS_BODIES = 115
EXISTING_PARENTS = {PARENT}


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s carries a non-competent source: %s" % (label, value))


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
    if contact_sources:
        if len(contact_sources) > 3:
            raise ValueError("%s has too many contact sources" % item.get("id"))
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s body site lacks identity provenance" % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Servia and Kozani candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Servia and Kozani candidate ledger date drifted")
    expected_summary = {
        PARENT: 115,
        "total": 115,
        "current_exact_parishes": 96,
        "legal_named_parish_rows": 94,
        "current_named_parish_additions": 2,
        "pilgrimage_churches": 1,
        "other_exact_worship_bodies": 12,
        "active_monasteries": 4,
        "other_monastic_bodies": 2,
        "contact_bodies": 56,
        "phone_bodies": 56,
        "public_phone_values": 72,
        "email_bodies": 1,
        "public_email_values": 1,
        "body_owned_sites": 3,
        "address_bodies": 115,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Servia and Kozani ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Servia and Kozani ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Servia and Kozani ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Servia and Kozani candidate IDs repeat")
    expected_section_counts = {
        "candidates": 9,
        "source_reconciliations": 9,
        "official_parent_audit": 2,
        "exclusions": 3,
    }
    actual_section_counts = {
        key: len(ledger[key]) for key in expected_section_counts
    }
    if actual_section_counts != expected_section_counts:
        raise ValueError(
            "Servia and Kozani ledger section counts drifted: %r"
            % actual_section_counts
        )
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
            raise ValueError("duplicate Servia and Kozani ID: %s" % row_id)
        parent = item.get("parent")
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s has wrong country" % row_id)
        if item.get("kind") not in ("parish", "monastery"):
            raise ValueError("%s has invalid kind" % row_id)
        for field in ("name", "local", "seat", "rank"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        text = json.dumps(item, ensure_ascii=False)
        if FORBIDDEN_PUNCTUATION.search(text):
            raise ValueError("%s carries forbidden punctuation" % row_id)
        signature = unicodedata.normalize("NFKC", item["local"]).casefold()
        signature = re.sub(r"\s+", " ", signature).strip()
        if signature in signatures:
            raise ValueError("%s duplicates %s" % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[parent] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Servia and Kozani English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Servia and Kozani English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Servia and Kozani parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Servia and Kozani kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Servia and Kozani rank totals drifted: %r" % dict(rank_counts))
    coverage = (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site")) for item in result),
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
        raise ValueError("Servia and Kozani contact coverage drifted: %r" % (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value
                    if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def all_source_urls():
    values = set(REGION_URLS.values())
    values.update({MONASTERIES_URL, PROGRAM_URL, BARADATOS_URL,
                   EP_URL, LEGAL_URL})
    for row in ROWS:
        values.update(row.get("sources") or [])
        values.update(row.get("contact_sources") or [])
        if row.get("site"):
            values.add(row["site"])
    return sorted(values)


def fetch_live_source(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=45) as response:
        if response.status >= 400:
            raise ValueError("HTTP %s" % response.status)
        content_type = response.headers.get("Content-Type", "").lower()
        payload = response.read()
        if "pdf" in content_type or url.endswith(".pdf"):
            if not payload.startswith(b"%PDF") or len(payload) < 20000:
                raise ValueError("invalid PDF payload")
            return None
        if "html" not in content_type:
            raise ValueError("unexpected content type %s" % content_type)
        return payload.decode("utf-8", "replace")


REGION_MARKERS = {
    "kozani": (
        "ΚΑΘΕΔΡΙΚΟΣ ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ",
        "ΠΡΟΦΗΤΗΣ ΗΛΙΑΣ-ΕΞΟΧΗ",
        "ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ-ΕΞΟΧΗ",
        "ΝΟΣΟΚΟΜΕΙΑΚΟΣ ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΛΟΥΚΑ",
        "ΖΩΟΔΟΧΟΣ ΠΗΓΗ",
    ),
    "aiani": ("ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ- ΑΙΑΝΗ", "ΡΟΔΙΑΝΗ"),
    "velvento": ("ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ-ΒΕΛΒΕΝΤΟΣ", "ΠΟΛΥΦΥΤΟΣ"),
    "drepano": ("ΑΓΙΑΣ ΤΡΙΑΔΑΣ-ΚΑΤΩ ΔΡΕΠΑΝΟ", "ΑΥΓΗ", "ΝΕΑ ΧΑΡΑΥΓΗ"),
    "krokos": ("ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ - ΑΝΑΤΟΛΗ", "ΑΓΙΑΣ ΤΡΙΑΔΟΣ - ΣΤΑΥΡΩΤΗ"),
    "servia": ("ΚΑΘΕΔΡΙΚΟΣ ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΚΥΡΙΑΚΗΣ", "ΦΡΟΥΡΙΟΝ"),
}


def check_live_sources():
    failures = []
    source_payloads = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_live_source, url): url
                   for url in all_source_urls()}
        for future in as_completed(futures):
            url = futures[future]
            try:
                source_payloads[url] = future.result()
            except Exception as exc:
                failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join("%s [%s]" % pair for pair in sorted(failures))
        raise ValueError("live Servia and Kozani source check failed: %s" % rendered)

    normalized = {url: normalize_source_text(payload or "")
                  for url, payload in source_payloads.items()}
    for region, markers in REGION_MARKERS.items():
        text = normalized[REGION_URLS[region]]
        for marker in markers:
            if normalize_source_text(marker) not in text:
                raise ValueError("live %s marker failed: %s" % (region, marker))

    monastery_text = normalized[MONASTERIES_URL]
    for marker in (
            "ΙΕΡΑ ΜΟΝΗ ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΛΑΡΙΟΥΣ",
            "ΙΕΡΑ ΣΤΑΥΡΟΠΗΓΙΑΚΗ ΜΟΝΗ ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ ΣΙΑΠΚΑΣ",
            "ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΝΕΚΤΑΡΙΟΥ", "ΠΑΝΑΓΙΑΣ ΖΙΔΑΝΙΟΥ",
            "ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΒΕΛΒΕΝΔΟΥ"):
        if normalize_source_text(marker) not in monastery_text:
            raise ValueError("live monastery marker failed: %s" % marker)

    ep_text = normalized[EP_URL]
    for marker in (
            "Ενοριακοί Ναοί 95", "Παρεκκλήσια 8", "Εξωκκλήσια 350",
            "Ναοί Κοιμητηρίων 54", "Μοναστηριακοί Ναοί 5",
            "Τ. Προδρόμου Βαζελῶνος", "Ἁγίου Βαραδάτου"):
        if normalize_source_text(marker) not in ep_text:
            raise ValueError("live Patriarchate marker failed: %s" % marker)

    program_text = normalized[PROGRAM_URL]
    for marker in ("Κοιμητηριακός Ναός Αγίου Γεωργίου",
                   "Ιερός Προσκυνηματικός Ναός Αγίων Αναργύρων"):
        if normalize_source_text(marker) not in program_text:
            raise ValueError("live program marker failed: %s" % marker)
    if "ομωνυμο ιερο μητροπολιτικο παρεκκλησιο" not in normalized[BARADATOS_URL]:
        raise ValueError("live Saint Baradatos chapel marker failed")

    contact_failures = []
    for row in ROWS:
        contact_sources = row.get("contact_sources") or []
        for phone in row.get("phones") or []:
            digits = re.sub(r"\D", "", phone)[-10:]
            source_digits = [
                re.sub(r"\D", "", normalized.get(url, ""))
                for url in contact_sources
            ]
            if not any(digits in value or digits[-5:] in value
                       for value in source_digits):
                contact_failures.append((row["id"], phone))
        for email in row.get("emails") or []:
            if not any(
                    email.casefold() in normalized.get(url, "") or
                    email.casefold() in (source_payloads.get(url) or "").casefold()
                    for url in contact_sources):
                contact_failures.append((row["id"], email))
    if contact_failures:
        raise ValueError("live Servia and Kozani contact marker failed: %r" % contact_failures)


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        check_live_sources()
        print("Servia and Kozani live source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Servia and Kozani check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
