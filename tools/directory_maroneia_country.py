#!/usr/bin/env python3
"""Validate exact named Maroneia and Komotini bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_maroneia_country.py --check
    python tools/directory_maroneia_country.py --check-live
    python tools/directory_maroneia_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "ep-maroneia"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "maroneia_country.json"
)

PARISH_INDEX_URL = "https://immaroniaskomotinis.gr/index.php/sports/soccer"
EP_URL = "https://ec-patr.org/entities/iera-mitropoli-maroneias-komotinis/"
REGULATION_URL = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2018_december.pdf"
)
MONASTERY_INDEX_URL = (
    "https://immaroniaskomotinis.gr/index.php/ierai-monai"
)
BASE = "https://immaroniaskomotinis.gr"

PARISH_PAGE_URLS = {
    page_id: (
        BASE + "/index.php/component/sppagebuilder/?view=page&id=%d"
        % page_id
    )
    for page_id in (16, 28, 29, 30, 31, 32, 33, 34, 35)
}


# key|English seat|Greek seat|postal code|English dedication|Greek dedication|
# exact displayed card title|public telephone|page id|rank
PARISH_SOURCE = r"""
dormition-komotini|Komotini|Κομοτηνή|69100|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.ΜΗΤΡ. Ν.ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ|2531022827|16|Metropolitan Cathedral
george-komotini|Komotini|Κομοτηνή|69100|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΟΜΟΤΗΝΗΣ|2531022609|16|Parish Church
annunciation-komotini|Komotini|Κομοτηνή|69100|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου|Ι.ΚΑΘ. Ν.ΕΥΑΓΓΕΛΙΣΜΟΥ ΤΗΣ ΘΕΟΤΟΚΟΥ|2531024457|16|Cathedral
kosmas-komotini|Komotini|Κομοτηνή|69100|Saint Kosmas of Aetolia|Αγίου Κοσμά του Αιτωλού|Ι.Ν. ΑΓΙΟΥ ΚΟΣΜΑ ΤΟΥ ΑΙΤΩΛΟΥ|2531037179|16|Parish Church
barbara-komotini|Komotini|Κομοτηνή|69100|Saint Barbara|Αγίας Βαρβάρας|Ι. Ν. ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ ΚΟΜΟΤΗΝΗΣ|2531024510|16|Parish Church
wisdom-komotini|Komotini|Κομοτηνή|69100|Wisdom of God|Της του Θεού Σοφίας|Ι.Ν. ΤΗΣ ΤΟΥ ΘΕΟΥ ΣΟΦΙΑΣ ΚΟΜΟΤΗΝΗΣ|2531022640|16|Parish Church
stylianos-komotini|Komotini|Κομοτηνή|69100|Saint Stylianos|Αγίου Στυλιανού|Ι.Ν. ΑΓΙΟΥ ΣΤΥΛΙΑΝΟΥ ΚΟΜΟΤΗΝΗΣ|2531026909|16|Parish Church
holy-trinity-agioi-theodoroi|Agioi Theodoroi|Άγιοι Θεόδωροι|69100|Holy Trinity|Αγίας Τριάδος|Ι.Ν. ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΑΓΙΩΝ ΘΕΟΔΩΡΩΝ||16|Parish Church
archangels-nea-adriani|Nea Adriani|Νέα Αδριανή|69100|Holy Archangels|Παμμεγίστων Ταξιαρχών|Ι.Ν. ΠΑΜΜ. ΤΑΞΙΑΡΧΩΝ ΝΕΑΣ ΑΝΔΡΙΑΝΗΣ|2531031831|28|Parish Church
dormition-aetolofos|Aetolofos|Αετόλοφος|69300|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΑΕΤΟΛΟΦΟΥ|2532052218|28|Parish Church
paraskevi-amaxades|Amaxades|Αμαξάδες|69200|Saint Paraskevi|Αγίας Παρασκευής|Ι.Ν. ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΑΜΑΞΑΔΩΝ|2534031389|28|Parish Church
demetrius-amfia|Amfia|Άμφια|69300|Saint Demetrius|Αγίου Δημητρίου|Ι.Ν. ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΑΜΦΙΩΝ||28|Parish Church
ascension-aetokoryfi|Aetokoryfi|Αετοκορυφή|69300|Ascension of the Savior|Αναλήψεως του Σωτήρος|Ι.Ν. ΑΝΑΛΗΨΕΩΣ ΤΟΥ ΣΩΤΗΡΟΣ ΑΕΤΟΚΟΡΥΦΗΣ|2533031294|28|Parish Church
athanasius-aigeiros|Aigeiros|Αίγειρος|69100|Saint Athanasius|Αγίου Αθανασίου|Ι.Ν. ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΑΙΓΕΙΡΟΥ|2531097386|28|Parish Church
george-ambrosia|Ambrosia|Αμβροσία|69100|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΜΒΡΟΣΙΑΣ|2531072766|28|Parish Church
demetrius-anthochorio|Anthochorio|Ανθοχώριον|69100|Saint Demetrius|Αγίου Δημητρίου|Ι.Ν. ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΑΝΘΟΧΩΡΙΟΥ|2531035728|28|Parish Church
george-aratos|Aratos|Άρατος|69100|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΡΑΤΟΥ||29|Parish Church
paraskevi-arsakeio|Arsakeio|Αρσάκειον|69300|Saint Paraskevi|Αγίας Παρασκευής|Ι.Ν. ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΑΡΣΑΚΕΙΟΥ||29|Parish Church
nicholas-asomatoi|Asomatoi|Ασώματοι|69100|Saint Nicholas|Αγίου Νικολάου|Ι.Ν. ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΑΣΩΜΑΤΩΝ|6974813348|29|Parish Church
sophia-glyfada|Glyfada|Γλυφάδα|69100|Saint Sophia|Αγίας Σοφίας|Ι.Ν.ΑΓΙΑΣ ΣΟΦΙΑΣ ΓΛΥΦΑΔΑΣ|2531097185|29|Parish Church
george-arisvi|Arisvi|Αρίσβη|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΡΙΣΒΗΣ||29|Parish Church
george-askites|Askites|Ασκηταί|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΣΚΗΤΩΝ|2533041360|29|Parish Church
paul-glykoneri|Glykoneri|Γλυκονέριον|67063|Saint Paul|Αγίου Παύλου|Ι.Ν.ΑΓΙΟΥ ΠΑΥΛΟΥ ΓΛΥΚΟΝΕΡΙΟΥ|2531097186|29|Parish Church
dormition-gratini|Gratini|Γρατινή|69100|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜ. ΤΗΣ ΘΕΟΤΟΚΟΥ ΓΡΑΤΙΝΗΣ|2531092257|29|Parish Church
constantine-helen-dialampi|Dialampi|Διαλαμπή|69200|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι.Ν. ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ ΔΙΑΛΑΜΠΗΣ|2534022446|30|Parish Church
tryphon-evrenos|Evrenos|Έβρενος|69300|Saint Tryphon|Αγίου Τρύφωνος|Ι.Ν. ΑΓΙΟΥ ΤΡΥΦΩΝΟΣ ΕΒΡΕΝΟΥ||30|Parish Church
dormition-iasio|Iasio|Ιάσιον|69300|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΙΑΣΙΟΥ||30|Parish Church
catherine-imeros|Imeros|Ίμερος|69400|Saint Catherine|Αγίας Αικατερίνης|Ι.Ν. ΑΓΙΑΣ ΑΙΚΑΤΕΡΙΝΗΣ ΙΜΕΡΟΥ|2531035262|30|Parish Church
nicholas-dioni|Dioni|Διώνη|69300|Saint Nicholas|Αγίου Νικολάου|Ι.Ν. ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΔΙΩΝΗΣ|2533031294|30|Parish Church
constantine-helen-thrylorio|Thrylorio|Θρυλόριον|69100|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι.Ν.ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ ΘΡΥΛΟΡΙΟΥ||30|Parish Church
nicholas-iasmos|Iasmos|Ίασμος|69200|Saint Nicholas|Αγίου Νικολάου|Ι.Ν. ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΙΑΣΜΟΥ|2534022682|30|Parish Church
dormition-kallithea|Kallithea|Καλλιθέα|69100|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΚΑΛΛΙΘΕΑΣ||30|Parish Church
demetrius-nea-kallisti|Nea Kallisti|Νέα Καλλίστη|69100|Saint Demetrius|Αγίου Δημητρίου|Ι.Ν. ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΚΑΛΛΙΣΤΗΣ||31|Parish Church
george-kizari|Kizari|Κίζαρι|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΙΖΑΡΙ||31|Parish Church
athanasius-kosmio|Kosmio|Κόσμιον|69100|Saint Athanasius|Αγίου Αθανασίου|Ι.Ν. ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΚΟΣΜΙΟΥ||31|Parish Church
panteleimon-mikro-kranovounio|Mikro Kranovounio|Μικρό Κρανοβούνιον|69100|Saint Panteleimon|Αγίου Παντελεήμονος|Ι.Ν. ΑΓΙΟΥ ΠΑΝΤ/ΝΟΣ ΜΙΚΡΟΥ ΚΡΑΝΟΒΟΥΝΙΟΥ|2531029550|31|Parish Church
transfiguration-karydia|Karydia|Καρυδιά|69100|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Ι.Ν. ΜΕΤ/ΣΕΩΣ ΤΟΥ ΣΩΤΗΡΟΣ ΚΑΡΥΔΙΑΣ||31|Parish Church
george-kirki|Kirki|Κίρκη|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΙΡΚΗΣ||31|Parish Church
george-krovili|Krovili|Κρωβύλη|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΡΩΒΥΛΗΣ||31|Parish Church
nativity-theotokos-mega-kranovounio|Mega Kranovounio|Μεγάλο Κρανοβούνιον||Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Ι.Ν. ΓΕΝΕΣΙΟΥ ΤΗΣ ΘΕΟΤΟΚΟΥ ΜΕΓΑΛΟΥ ΚΡΑΝΟΒΟΥΝΙΟΥ||31|Parish Church
archangels-lofario|Lofario|Λοφάριον|69300|Holy Archangels|Παμμεγίστων Ταξιαρχών|Ι.Ν. ΠΑΜΜ/ΣΤΩΝ ΤΑΞΙΑΡΧΩΝ ΛΟΦΑΡΙΟΥ||32|Parish Church
dormition-maroneia|Maroneia|Μαρώνεια|69400|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΜΑΡΩΝΕΙΑΣ|2533041360|32|Parish Church
holy-trinity-mesouni|Mesouni|Μεσούνη|69100|Holy Trinity|Αγίας Τριάδος|Ι.Ν. ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΜΕΣΣΟΥΝΗΣ||32|Parish Church
george-mesti|Mesti|Μέστη|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΜΕΣΤΗΣ||32|Parish Church
nativity-theotokos-lykeio|Lykeio|Λύκειον|69300|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Ι.Ν. ΓΕΝΝΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΛΥΚΕΙΟΥ|2531041460|32|Parish Church
holy-cross-mesochorio|Mesochorio|Μεσοχώριον|69100|Holy Cross|Τιμίου Σταυρού|Ι.Ν. ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ ΜΕΣΟΧΩΡΙΟΥ|2531091146|32|Parish Church
paraskevi-mesi|Mesi|Μέσση|67063|Saint Paraskevi|Αγίας Παρασκευής|Ι.Ν. ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΜΕΣΗΣ||32|Parish Church
spyridon-mosaiko|Mosaiko|Μωσαϊκόν|69200|Saint Spyridon|Αγίου Σπυρίδωνος|Ι.Ν. ΑΓΙΟΥ ΣΠΥΡΙΔΩΝΟΣ ΜΩΣΑΪΚΟΥ|2534022446|32|Parish Church
archangels-xylagani|Xylagani|Ξυλαγανή|69400|Holy Archangels|Παμμεγίστων Ταξιαρχών|Ι.Ν. ΠΑΜΜ/ΤΩΝ ΤΑΞΙΑΡΧΩΝ ΞΥΛΑΓΑΝΗΣ||33|Parish Church
prophet-elijah-palladio|Palladio|Παλλάδιον|69100|Prophet Elijah|Προφήτου Ηλιού|Ι.Ν. ΠΡΟΦΗΤΟΥ ΗΛΙΟΥ ΠΑΛΛΑΔΙΟΥ||33|Parish Church
dormition-nea-petra|Nea Petra|Νέα Πέτρα|69400|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΝΕΑΣ ΠΕΤΡΑΣ|2533022845|33|Parish Church
forerunner-pelagia|Pelagia|Πελαγία|69400|Saint John the Forerunner|Τιμίου Προδρόμου|Ι.Ν. ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΠΕΛΑΓΙΑΣ|2531098321|33|Parish Church
basil-pagouria|Pagouria|Παγούρια|69100|Saint Basil|Αγίου Βασιλείου|Ι.Ν. ΑΓΙΟΥ ΒΑΣΙΛΕΙΟΥ ΠΑΓΟΥΡΙΩΝ||33|Parish Church
george-pamforo|Pamforo|Πάμφορον|69100|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΠΑΜΦΟΡΟΥ||33|Parish Church
constantine-helen-paradimi|Paradimi|Παραδημή|69100|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι.Ν. ΑΓΙΩΝ ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ ΠΑΡΑΔΗΜΗΣ||33|Parish Church
prophet-elijah-pandrosos|Pandrosos|Πάνδροσος|69100|Prophet Elijah|Προφήτου Ηλιού|Ι.Ν. ΠΡΟΦΗΤΟΥ ΗΛΙΟΥ ΠΑΝΔΡΟΣΟΥ|2531025257|33|Parish Church
constantine-helen-polyanthos|Polyanthos|Πολύανθος|69200|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι.Ν. ΑΓΙΩΝ ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ ΠΟΛΥΑΝΘΟΥ|2534022497|34|Parish Church
george-porpi|Porpi|Πόρπη|69100|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΠΟΡΠΗΣ|2535021185|34|Parish Church
dormition-roditis|Roditis|Ροδίτης|69100|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΡΟΔΙΤΗ|2531092315|34|Parish Church
demetrius-nea-santa|Nea Santa|Νέα Σάντα|69300|Saint Demetrius|Αγίου Δημητρίου|Ι.Ν. ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΝΕΑ ΣΑΝΤΑΣ||34|Parish Church
george-proskynitai|Proskynitai|Προσκυνηταί|69400|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΠΡΟΣΚΥΝΗΤΩΝ|2533041592|34|Parish Church
holy-trinity-protato|Protato|Πρωτάτον|69300|Holy Trinity|Αγίας Τριάδος|Ι.Ν. ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΠΡΩΤΑΤΟΥ||34|Parish Church
athanasius-salpi|Salpi|Σάλπη|69100|Saint Athanasius|Αγίου Αθανασίου|Ι.Ν. ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΣΑΛΠΗΣ||34|Parish Church
constantine-helen-sapes|Sapes|Σάππαι|69300|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι.Ν. ΑΓΙΩΝ ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ ΣΑΠΠΩΝ||34|Parish Church
theodore-neo-sidirochori|Neo Sidirochori|Νέο Σιδηροχώριον|69300|Saint Theodore Stratelates|Αγίου Θεοδώρου του Στρατηλάτου|Ι.Ν.ΑΓ. ΘΕΟΔΩΡΟΥ ΤΟΥ ΣΤΡΑΤΗΛΑΤΟΥ Ν.ΣΙΔΗΡΟΧΩΡΙΟΥ||35|Parish Church
george-sykorrachi|Sykorrachi|Συκορράχη|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΣΥΚΟΡΡΑΧΗΣ||35|Parish Church
demetrius-yfantai|Yfantai|Υφανταί|69100|Saint Demetrius|Αγίου Δημητρίου|Ι.Ν. ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΥΦΑΝΤΩΝ|2531091146|35|Parish Church
george-chamilo|Chamilo|Χαμηλόν|69300|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΧΑΜΗΛΟΥ||35|Parish Church
demetrius-strymi|Strymi|Στρύμη|69300|Saint Demetrius|Αγίου Δημητρίου|Ι.Ν. ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΣΤΡΥΜΗΣ||35|Parish Church
george-sostis|Sostis|Σώστης|69200|Saint George|Αγίου Γεωργίου|Ι.Ν. ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΣΩΣΤΟΥ||35|Parish Church
dormition-fanari|Fanari|Φανάριον|69150|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι.Ν. ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΦΑΝΑΡΙΟΥ|2531031261|35|Parish Church
"""


def parse_parishes():
    rows = []
    markers = {}
    for number, raw in enumerate(
            (line for line in PARISH_SOURCE.splitlines() if line.strip()), 1):
        parts = raw.split("|")
        if len(parts) != 10:
            raise ValueError("invalid Maroneia parish source row: %s" % raw)
        (key, seat, seat_local, postal, dedication, dedication_local,
         source_phrase, phone, page_text, rank) = parts
        page_id = int(page_text)
        source_url = PARISH_PAGE_URLS[page_id]
        row_id = "gr-ep-maroneia-%03d-%s" % (number, key)
        address = seat_local
        if postal:
            address += ", Τ.Κ. " + postal
        item = {
            "id": row_id,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s Parish Church in %s" % (dedication, seat),
            "local": "Ιερός Ναός %s, %s" % (
                dedication_local, seat_local
            ),
            "seat": seat,
            "country": "GR",
            "address": [address],
            "sources": [source_url],
        }
        marker_seat = seat_local
        marker_seat_overrides = {
            "holy-trinity-agioi-theodoroi": "Αγ. Θεόδωροι",
            "archangels-nea-adriani": "Αδριανή Ν.",
            "demetrius-nea-kallisti": "Καλλίστη Ν.",
            "panteleimon-mikro-kranovounio": "Κρανοβούνιον Μικρό",
            "theodore-neo-sidirochori": "Σιδηροχώριον Ν.",
        }
        marker_seat = marker_seat_overrides.get(key, marker_seat)
        live_markers = [source_phrase, marker_seat]
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [source_url]
            item["contact_checked"] = CHECKED
            live_markers.append(phone)
        rows.append(item)
        markers[row_id] = live_markers
    return rows, markers


ROWS, LIVE_MARKERS = parse_parishes()


def add_row(item, markers):
    ROWS.append(item)
    LIVE_MARKERS[item["id"]] = markers


def local_article(path):
    return BASE + "/index.php/all-content/item/" + path


add_row({
    "id": "gr-ep-maroneia-072-saint-demetrius-pilgrimage-kassitera",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Pilgrimage Church",
    "name": "Saint Demetrius Pilgrimage Church in Kassitera",
    "local": "Ιερός Προσκυνηματικός Ναός Αγίου Δημητρίου Κασσιτερών",
    "seat": "Kassitera",
    "country": "GR",
    "address": ["Κασσιτερά"],
    "sources": [
        REGULATION_URL,
        local_article(
            "4198-esperinos-eortis-agiou-partheniou-kai-monaxiki-"
            "koura-stin-iera-mitropoli"
        ),
    ],
}, ["Ἱερὸ Ναὸ τοῦ Ἁγίου Δημητρίου Κασσιτερῶν"])

add_row({
    "id": "gr-ep-maroneia-073-saint-eugene-pilgrimage-nea-romania",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Pilgrimage Church",
    "name": "Saint Eugene of Trebizond Pilgrimage Church in Nea Romania",
    "local": "Ιερός Προσκυνηματικός Ναός Αγίου Ευγενίου Νέας Ρωμανίας",
    "seat": "Nea Romania",
    "country": "GR",
    "address": ["Νέα Ρωμανία, Πετρωτά"],
    "sources": [
        REGULATION_URL,
        local_article(
            "4447-panigyrikos-esperinos-agiou-evgeniou-tou-"
            "trapezountiou-stin-iera-mitropoli"
        ),
    ],
}, ["Ἱερό Προσκυνηματικό Ναό Ἁγίου Εὐγενίου Νέας Ρωμανίας"])

add_row({
    "id": "gr-ep-maroneia-074-maximus-kavsokalyvites-monastery",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Monastery of Venerable Maximus Kavsokalyvites of Papikion Oros",
    "local": "Ιερά Μονή Οσίου Μαξίμου Καυσοκαλύβη Παπικίου Όρους",
    "seat": "Papikion Oros",
    "country": "GR",
    "address": ["Περιοχή Σώστου, Παπίκιο Όρος"],
    "phones": ["25310-20254", "25310-72738"],
    "sources": [
        EP_URL,
        BASE + "/index.php/component/sppagebuilder/page/482",
    ],
    "contact_sources": [EP_URL],
    "contact_checked": CHECKED,
}, [
    "Ὁσίου Μαξίμου Καυσοκαλύβη Παπικίου Ὄρους",
    "25310-20254", "25310-72738",
])

add_row({
    "id": "gr-ep-maroneia-075-saint-christopher-monastery",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Monastery of Saint Christopher in Komotini",
    "local": "Ιερά Μονή Αγίου Χριστοφόρου Κομοτηνής",
    "seat": "Komotini",
    "country": "GR",
    "address": ["Εθνική Οδός Κομοτηνής - Ξάνθης, 5 χλμ. από Κομοτηνή"],
    "phones": ["25310-72871"],
    "sources": [
        EP_URL,
        BASE + "/index.php/component/sppagebuilder/page/479",
    ],
    "contact_sources": [EP_URL],
    "contact_checked": CHECKED,
}, ["Ἁγίου Χριστοφόρου Κομοτηνῆς", "25310-72871"])

add_row({
    "id": "gr-ep-maroneia-076-panagia-phaneromeni-monastery",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Panagia Phaneromeni Monastery of Vathyrriakos",
    "local": "Ιερά Μονή Παναγίας Φανερωμένης Βαθυρρύακος",
    "seat": "Vathyrriakos",
    "country": "GR",
    "address": ["Θέση Φατήρ Γιακά, κοντά στην Αίγειρο"],
    "phones": ["25310-97022"],
    "sources": [
        EP_URL,
        BASE + "/index.php/component/sppagebuilder/page/483",
    ],
    "contact_sources": [EP_URL],
    "contact_checked": CHECKED,
}, ["Παναγίας Φανερωμένης Βαθυρρύακος", "25310-97022"])

add_row({
    "id": "gr-ep-maroneia-077-entry-theotokos-pandrosos-monastery",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Monastery of the Entry of the Theotokos in Pandrosos",
    "local": "Ιερά Μονή Εισοδίων της Θεοτόκου Πανδρόσου",
    "seat": "Pandrosos",
    "country": "GR",
    "address": ["Κοντά στην Πάνδροσο, 10 χλμ. από Κομοτηνή"],
    "phones": ["25310-33262"],
    "sources": [
        EP_URL,
        BASE + "/index.php/component/sppagebuilder/page/485",
    ],
    "contact_sources": [EP_URL],
    "contact_checked": CHECKED,
}, ["Εἰσοδίων τῆς Θεοτόκου Πανδρόσου", "25310-33262"])


def add_exact(record):
    number = len(ROWS) + 1
    item = {
        "id": "gr-ep-maroneia-%03d-%s" % (number, record["key"]),
        "parent": PARENT,
        "kind": record.get("kind", "parish"),
        "rank": record["rank"],
        "name": record["name"],
        "local": record["local"],
        "seat": record["seat"],
        "country": "GR",
        "address": list(record["address"]),
        "sources": list(record["sources"]),
    }
    add_row(item, list(record["markers"]))


EXACT_RECORDS = [
    {
        "key": "john-chrysostom-municipal-depot-komotini",
        "name": "Saint John Chrysostom Institutional Chapel at the Komotini Municipal Depot",
        "local": "Ιερό Παρεκκλήσιο Αγίου Ιωάννου του Χρυσοστόμου στο Αμαξοστάσιο του Δήμου Κομοτηνής",
        "seat": "Komotini",
        "rank": "Institutional Chapel",
        "address": ["Αμαξοστάσιο Δήμου Κομοτηνής"],
        "sources": [local_article(
            "4644-eorti-tou-agiou-ioannou-tou-xrysostomou-stin-iera-"
            "mitropoli"
        )],
        "markers": ["ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΤΟΥ ΧΡΥΣΟΣΤΟΜΟΥ", "ἁμαξοστασίου"],
    },
    {
        "key": "menas-elderly-care-komotini",
        "name": "Saint Menas Institutional Chapel at the Elderly Care Unit in Komotini",
        "local": "Ιερό Παρεκκλήσιο Αγίου Μηνά της Μονάδας Φροντίδας Ηλικιωμένων Κομοτηνής",
        "seat": "Komotini",
        "rank": "Institutional Chapel",
        "address": ["Μονάδα Φροντίδας Ηλικιωμένων, Κομοτηνή"],
        "sources": [local_article(
            "4640-eorti-tou-agiou-mina-stin-iera-mitropoli"
        )],
        "markers": ["Ἁγίου Μηνᾶ", "Γηροκομεῖο"],
    },
    {
        "key": "nectarius-xylagani",
        "name": "Saint Nectarius Chapel in Xylagani",
        "local": "Ιερό Παρεκκλήσιο Αγίου Νεκταρίου Ξυλαγανής",
        "seat": "Xylagani",
        "rank": "Chapel",
        "address": ["Ξυλαγανή"],
        "sources": [local_article(
            "4636-i-eorti-tou-agiou-nektariou-episkopou-pentapoleos-"
            "stin-iera-mitropoli"
        )],
        "markers": ["ΑΓΙΟΥ ΝΕΚΤΑΡΙΟΥ", "Ξυλαγανῆς"],
    },
    {
        "key": "venerable-david-proskynitai",
        "name": "Venerable David Chapel in Proskynitai",
        "local": "Ιερό Παρεκκλήσιο Οσίου Δαβίδ Προσκυνητών",
        "seat": "Proskynitai",
        "rank": "Chapel",
        "address": ["Προσκυνηταί"],
        "sources": [local_article(
            "4629-eorti-osiou-david-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο τοῦ Ὁσίου Δαβίδ Προσκυνητῶν"],
    },
    {
        "key": "anastasia-romana-komotini",
        "name": "Venerable Martyr Anastasia the Roman Chapel in Komotini",
        "local": "Ιερό Παρεκκλήσιο Οσιομάρτυρος Αναστασίας της Ρωμαίας Κομοτηνής",
        "seat": "Komotini",
        "rank": "Chapel",
        "address": ["Αύλειος χώρος Ιερού Ναού Αγίας Βαρβάρας, Κομοτηνή"],
        "sources": [local_article(
            "4626-eorti-osias-megalomartyros-anastasias-tis-romaias-"
            "stin-iera-mitropoli"
        )],
        "markers": ["Ἁγίας Ὁσιομάρτυρος Ἀναστασίας", "Ἁγίας Βαρβάρας Κομοτηνῆς"],
    },
    {
        "key": "holy-protection-kourdalos-camp",
        "name": "Holy Protection Military Chapel at Major Ioannis Kourdalos Camp",
        "local": "Ιερό Παρεκκλήσιο Αγίας Σκέπης Στρατοπέδου Ταγματάρχου Ιωάννου Κούρδαλου",
        "seat": "Nea Kallisti",
        "rank": "Military Chapel",
        "address": ["Στρατόπεδο Ταγματάρχου Ιωάννου Κούρδαλου, Νέα Καλλίστη"],
        "sources": [local_article(
            "4625-eorti-agias-skepis-tis-yperagias-theotokou-kai-"
            "iroiko-epos-tou-1940-stin-iera-mitropoli"
        )],
        "markers": ["Ἁγίας Σκέπης", "Ταγματάρχου Ἰωάννου Κούρδαλου"],
    },
    {
        "key": "artemius-rodopi-police",
        "name": "Saint Artemius Institutional Chapel at the Rodopi Police Directorate",
        "local": "Ιερό Παρεκκλήσιο Αγίου Αρτεμίου Αστυνομικής Διεύθυνσης Ροδόπης",
        "seat": "Komotini",
        "rank": "Institutional Chapel",
        "address": ["Αστυνομική Διεύθυνση Ροδόπης, Κομοτηνή"],
        "sources": [local_article(
            "4603-eorti-agiou-artemiou-stin-iera-mitropoli"
        )],
        "markers": ["ΑΓΙΟΥ ΑΡΤΕΜΙΟΥ", "Ἀστυνομική Διεύθυνση Ροδόπης"],
    },
    {
        "key": "dionysius-areopagite-yfantai",
        "name": "Saint Dionysius the Areopagite Chapel in Yfantai",
        "local": "Ιερό Παρεκκλήσιο Αγίου Διονυσίου του Αρεοπαγίτου Υφαντών",
        "seat": "Yfantai",
        "rank": "Chapel",
        "address": ["Υφανταί"],
        "sources": [local_article(
            "4583-i-eorti-tou-agiou-dionysiou-tou-areopagitou-stin-"
            "iera-mitropoli"
        )],
        "markers": ["Ἁγίου Διονυσίου τοῦ Ἀρεοπαγίτου", "Ὑφαντῶν"],
    },
    {
        "key": "romanos-melodist-music-school",
        "name": "Venerable Romanos the Melodist Institutional Chapel at Komotini Music School",
        "local": "Ιερό Παρεκκλήσιο Οσίου Ρωμανού του Μελωδού Μουσικού Σχολείου Κομοτηνής",
        "seat": "Komotini",
        "rank": "Institutional Chapel",
        "address": ["Μουσικό Γυμνάσιο - Λύκειο Κομοτηνής"],
        "sources": [local_article("4580-immkomotinis")],
        "markers": ["Ρωμανοῦ τοῦ Μελωδοῦ", "Μουσικοῦ Γυμνασίου"],
    },
    {
        "key": "kallisti-nea-kallisti",
        "name": "Saint Kallisti Chapel in Nea Kallisti",
        "local": "Ιερό Παρεκκλήσιο Αγίας Καλλίστης Νέας Καλλίστης",
        "seat": "Nea Kallisti",
        "rank": "Chapel",
        "address": ["Νέα Καλλίστη"],
        "sources": [
            local_article(
                "4538-panigyrikos-esperinos-agias-kallistis-stin-iera-"
                "mitropoli"
            ),
            BASE + "/index.php/programma-sevasmiotatou/item/"
            "2298-programma-sevasmiotatou-mitropolitou-maroneias-kai-"
            "komotinis-k-panteleimonos",
        ],
        "markers": ["Ἱερό Παρεκκλήσιο Ἁγίας Καλλίστης", "Νέα Καλλίστη"],
    },
    {
        "key": "george-argyroupolis-parcharia-nymfaia",
        "name": "Saint George of Argyroupolis Chapel at Parcharia in Nymfaia",
        "local": "Ιερό Εξωκκλήσιο Αγίου Γεωργίου του εξ Αργυρουπόλεως στα Παρχάρια Νυμφαίας",
        "seat": "Nymfaia",
        "rank": "Chapel",
        "address": ["Περιοχή Παρχάρια, Νυμφαία"],
        "sources": [
            local_article(
                "4165-theofaneia-sto-iero-eksokklisio-agiou-georgiou-"
                "argyroupoleos-sta-parxaria-nymfaias"
            ),
            local_article(
                "4533-eorti-tis-koimiseos-tis-theotokou-me-to-"
                "iouliano-imerologio-stin-iera-mitropoli"
            ),
        ],
        "markers": ["Ἁγίου Γεωργίου τοῦ ἐξ Ἀργυρουπόλεως", "Παρχάρια"],
    },
    {
        "key": "phanourios-salpi",
        "name": "Saint Phanourios Chapel in Salpi",
        "local": "Ιερό Παρεκκλήσιο Αγίου Φανουρίου Σάλπης",
        "seat": "Salpi",
        "rank": "Chapel",
        "address": ["Σάλπη"],
        "sources": [local_article(
            "4528-eorti-agiou-fanouriou-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο Ἁγίου Φανουρίου Σάλπης"],
    },
    {
        "key": "rose-unfading-aigeiros",
        "name": "Rose Unfading Chapel at the Aigeiros Viticultural Station",
        "local": "Παρεκκλήσιο Ρόδον το Αμάραντον Αμπελουργικού Σταθμού Αιγείρου",
        "seat": "Aigeiros",
        "rank": "Chapel",
        "address": ["Αμπελουργικός Σταθμός Αιγείρου"],
        "sources": [local_article(
            "4522-panigyrikos-esperinos-epi-ti-apodosei-tis-eortis-"
            "tis-koimiseos-tis-theotokou-stin-iera-mitropoli"
        ), local_article(
            "4519-iera-panigyris-ieras-monis-panagias-faneromenis-"
            "vathyrryakos"
        )],
        "markers": ["Ρόδον τό Ἀμάραντον", "ἀμπελουργικοῦ Σταθμοῦ Αἰγείρου"],
    },
    {
        "key": "panteleimon-hospital-komotini",
        "name": "Saint Panteleimon Institutional Chapel at Komotini General Hospital",
        "local": "Ιερό Παρεκκλήσιο Αγίου Παντελεήμονος Γενικού Νοσοκομείου Κομοτηνής",
        "seat": "Komotini",
        "rank": "Institutional Chapel",
        "address": ["Γενικό Νοσοκομείο Κομοτηνής"],
        "sources": [local_article(
            "4228-i-akolouthia-tis-a-staseos-ton-xairetismon-pros-"
            "tin-yperagia-theotoko-stin-iera-mitropoli"
        )],
        "markers": ["Ἁγίου Παντελεήμονος", "Νοσοκομείου Κομοτηνῆς"],
    },
    {
        "key": "prophet-elijah-proskynitai",
        "name": "Prophet Elijah Chapel near KAAΥ Proskynitai",
        "local": "Ιερό Παρεκκλήσιο Προφήτου Ηλιού έναντι των ΚΑΑΥ Προσκυνητών",
        "seat": "Proskynitai",
        "rank": "Chapel",
        "address": ["Έναντι ΚΑΑΥ Προσκυνητών"],
        "sources": [local_article(
            "4484-i-eorti-tou-profitou-iliou-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο Προφήτου Ἠλιού", "ΚΑΑΥ Προσκυνητῶν"],
    },
    {
        "key": "paisios-annunciation-cathedral-komotini",
        "name": "Venerable Paisios the Athonite Chapel at the Annunciation Cathedral in Komotini",
        "local": "Ιερό Παρεκκλήσιο Οσίου Παϊσίου του Αγιορείτου Καθεδρικού Ναού Ευαγγελισμού της Θεοτόκου Κομοτηνής",
        "seat": "Komotini",
        "rank": "Chapel",
        "address": ["Αύλειος χώρος Καθεδρικού Ναού Ευαγγελισμού της Θεοτόκου, Κομοτηνή"],
        "sources": [local_article(
            "4474-eorti-tou-osiou-patros-imon-paisiou-stin-iera-"
            "mitropoli"
        )],
        "markers": ["Ἁγίου Παϊσίου τοῦ Ἁγιορείτου", "Καθεδρικοῦ Ναοῦ Εὐαγγελισμοῦ"],
    },
    {
        "key": "kyriaki-exintari-komotini",
        "name": "Saint Kyriaki Chapel at Exintari Square in Komotini",
        "local": "Ιερό Παρεκκλήσιο Αγίας Κυριακής πλατείας Εξηντάρη Κομοτηνής",
        "seat": "Komotini",
        "rank": "Chapel",
        "address": ["Πλατεία Εξηντάρη, Κομοτηνή"],
        "sources": [local_article(
            "4470-i-eorti-agias-kyriakis-stin-iera-mitropoli"
        )],
        "markers": ["Ἁγίου Γεωργίου Κομοτηνῆς", "πλατεία Ἑξηντάρη"],
    },
    {
        "key": "kyriaki-roditis",
        "name": "Saint Kyriaki Chapel in Roditis",
        "local": "Ιερό Παρεκκλήσιο Αγίας Κυριακής Ροδίτη",
        "seat": "Roditis",
        "rank": "Chapel",
        "address": ["Ροδίτης"],
        "sources": [local_article(
            "4470-i-eorti-agias-kyriakis-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο τῆς Ἁγίας Κυριακῆς Ροδίτη"],
    },
    {
        "key": "unmercenaries-dormition-bell-tower-komotini",
        "name": "Holy Unmercenaries Cosmas and Damian Chapel at the Dormition Metropolitan Church in Komotini",
        "local": "Ιερό Παρεκκλήσιο Αγίων Αναργύρων Κοσμά και Δαμιανού Μητροπολιτικού Ναού Κοιμήσεως της Θεοτόκου Κομοτηνής",
        "seat": "Komotini",
        "rank": "Chapel",
        "address": ["Κωδωνοστάσιο Μητροπολιτικού Ναού Κοιμήσεως της Θεοτόκου, Κομοτηνή"],
        "sources": [local_article(
            "4458-eorti-agion-anargyron-stin-iera-mitropoli"
        )],
        "markers": ["Κοσμᾶ καὶ Δαμιανοῦ", "κωδωνοστάσιον τοῦ Ναοῦ"],
    },
    {
        "key": "unmercenaries-skaloma",
        "name": "Holy Unmercenaries Chapel in Skaloma",
        "local": "Ιερό Παρεκκλήσιο Αγίων Αναργύρων Σκαλώματος",
        "seat": "Skaloma",
        "rank": "Chapel",
        "address": ["Σκάλωμα"],
        "sources": [local_article(
            "4458-eorti-agion-anargyron-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο τῶν Ἁγίων Ἀναργύρων Σκαλώματος"],
    },
    {
        "key": "holy-apostles-wisdom-komotini",
        "name": "Holy Apostles Chapel at the Wisdom of God Church in Komotini",
        "local": "Ιερό Παρεκκλήσιο Αγίων Αποστόλων Ναού της του Θεού Σοφίας Κομοτηνής",
        "seat": "Komotini",
        "rank": "Chapel",
        "address": ["Ιερός Ναός της του Θεού Σοφίας, Κομοτηνή"],
        "sources": [local_article(
            "4454-i-eorti-tis-synakseos-ton-agion-apostolon-stin-iera-"
            "mitropoli"
        )],
        "markers": ["Ναό Τῆς Τοῦ Θεοῦ Σοφίας", "Παρεκκλήσιο τοῦ Ναοῦ"],
    },
    {
        "key": "holy-apostles-molyvoti",
        "name": "Holy Apostles Chapel in Molyvoti",
        "local": "Ιερό Παρεκκλήσιο Αγίων Αποστόλων Μολυβωτής",
        "seat": "Molyvoti",
        "rank": "Chapel",
        "address": ["Μολυβωτή"],
        "sources": [local_article(
            "4453-o-esperinos-tis-synakseos-ton-agion-apostolon-stin-"
            "iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο Ἁγίων Ἀποστόλων Μολυβωτῆς"],
    },
    {
        "key": "nativity-forerunner-sarakatsani-glykoneri",
        "name": "Nativity of Saint John the Forerunner Chapel at the Sarakatsani Settlement in Glykoneri",
        "local": "Ιερό Παρεκκλήσιο Γενεθλίου του Τιμίου Προδρόμου Οικισμού Σαρακατσάνων Γλυκονερίου",
        "seat": "Glykoneri",
        "rank": "Chapel",
        "address": ["Οικισμός Σαρακατσάνων Γλυκονερίου"],
        "sources": [local_article(
            "4445-i-eorti-tou-genethliou-tou-timiou-prodromou-stin-"
            "iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιον στόν οἰκισμό Σαρακατσάνων Γλυκονερίου"],
    },
    {
        "key": "nativity-forerunner-nymfaia",
        "name": "Nativity of Saint John the Forerunner Chapel in Nymfaia",
        "local": "Ιερό Παρεκκλήσιο Γενέσεως Τιμίου Προδρόμου Νυμφαίας",
        "seat": "Nymfaia",
        "rank": "Chapel",
        "address": ["Νυμφαία"],
        "sources": [local_article(
            "4445-i-eorti-tou-genethliou-tou-timiou-prodromou-stin-"
            "iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιον Γενέσεως Τιμίου Προδρόμου Νυμφαίας"],
    },
    {
        "key": "irene-askites",
        "name": "Saint Irene Chapel in Askites",
        "local": "Ιερό Παρεκκλήσιο Αγίας Ειρήνης Ασκητών",
        "seat": "Askites",
        "rank": "Chapel",
        "address": ["Ασκηταί"],
        "sources": [local_article(
            "4380-theia-leitourgia-stous-askites-kai-epimnimosyni-"
            "deisi"
        )],
        "markers": ["Παρεκκλήσιο Ἁγίας Εἰρήνης Ἀσκητῶν"],
    },
    {
        "key": "athanasius-strymi",
        "name": "Saint Athanasius Chapel in Strymi",
        "local": "Ιερό Παρεκκλήσιο Αγίου Αθανασίου Στρύμης",
        "seat": "Strymi",
        "rank": "Chapel",
        "address": ["Στρύμη"],
        "sources": [local_article(
            "4344-eorti-epi-tin-anakomidi-ton-ieron-leipsanon-tou-"
            "agiou-athanasiou-patriarxou-aleksandreias-stin-iera-"
            "mitropoli"
        )],
        "markers": ["Παρεκκλήσιο τοῦ Ἁγίου Ἀθανασίου Στρύμης"],
    },
    {
        "key": "apostle-mark-sostis",
        "name": "Apostle Mark Chapel in Sostis",
        "local": "Ιερό Παρεκκλήσιο Αποστόλου Μάρκου Σώστη",
        "seat": "Sostis",
        "rank": "Chapel",
        "address": ["Σώστης"],
        "sources": [local_article(
            "4327-i-eorti-tou-evaggelistou-markou-stin-iera-"
            "mitropoli"
        )],
        "markers": ["Αποστόλου", "Μάρκου", "Σώστη"],
    },
    {
        "key": "nectarius-annunciation-cathedral-komotini",
        "name": "Saint Nectarius Chapel at the Annunciation Cathedral in Komotini",
        "local": "Ιερό Παρεκκλήσιο Αγίου Νεκταρίου Καθεδρικού Ναού Ευαγγελισμού της Θεοτόκου Κομοτηνής",
        "seat": "Komotini",
        "rank": "Chapel",
        "address": ["Καθεδρικός Ναός Ευαγγελισμού της Θεοτόκου, Κομοτηνή"],
        "sources": [local_article(
            "4320-savvato-tis-diakainisimou-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο Ἁγίου Νεκταρίου", "Καθεδρικοῦ Ναοῦ Εὐαγγελισμοῦ"],
    },
    {
        "key": "life-giving-spring-gratini",
        "name": "Life-Giving Spring Chapel in Gratini",
        "local": "Ιερό Παρεκκλήσιο Ζωοδόχου Πηγής Γρατινής",
        "seat": "Gratini",
        "rank": "Chapel",
        "address": ["Γρατινή"],
        "sources": [local_article(
            "4316-i-eorti-tis-zoodoxou-pigis-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο Ζωοδόχου Πηγῆς", "Γρατινῆς"],
    },
    {
        "key": "raphael-nicholas-irene-polyanthos",
        "name": "Saints Raphael, Nicholas and Irene Chapel in Polyanthos",
        "local": "Ιερό Παρεκκλήσιο Αγίων Ραφαήλ, Νικολάου και Ειρήνης Πολυάνθου",
        "seat": "Polyanthos",
        "rank": "Chapel",
        "address": ["Πολύανθος"],
        "sources": [local_article(
            "4312-i-eorti-ton-neofanon-martyron-rafail-nikolaou-kai-"
            "eirinis-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιο Ἁγίων Ραφαῆλ, Νικολάου καί Εἰρήνης Πολυάνθου"],
    },
    {
        "key": "anthony-iasmos",
        "name": "Saint Anthony Chapel in Iasmos",
        "local": "Ιερό Παρεκκλήσιο Αγίου Αντωνίου Ιάσμου",
        "seat": "Iasmos",
        "rank": "Chapel",
        "address": ["Ίασμος"],
        "sources": [local_article(
            "4162-eorti-tou-agiou-antoniou-stin-iera-mitropoli"
        )],
        "markers": ["Παρεκκλήσιον Ἁγίου Ἀντωνίου Ἰάσμου"],
    },
    {
        "key": "three-holy-children-fire-service",
        "name": "Three Holy Children Institutional Chapel at the Regional Fire Service Headquarters",
        "local": "Ιερό Παρεκκλήσιο Αγίων Τριών Παίδων Περιφερειακής Πυροσβεστικής Διοίκησης Ανατολικής Μακεδονίας και Θράκης",
        "seat": "Komotini",
        "rank": "Institutional Chapel",
        "address": ["Έδρα Περιφερειακής Πυροσβεστικής Διοίκησης Ανατολικής Μακεδονίας και Θράκης"],
        "sources": [local_article(
            "4104-i-eorti-ton-agion-trion-paidon-en-kamino-prostaton-"
            "tis-pyrosvestikis-ypiresias-stin-iera-mitropoli"
        )],
        "markers": ["παρεκκλήσιο τῶν Ἁγίων Τριῶν Παίδων", "Διοίκησης Ἀνατολικῆς Μακεδονίας"],
    },
    {
        "key": "demetrius-mountaineering-refuge",
        "name": "Saint Demetrius Chapel at Charalambos Dimou Mountaineering Refuge",
        "local": "Ιερό Εξωκκλήσιο Αγίου Δημητρίου Ορειβατικού Καταφυγίου Χαράλαμπος Δήμου",
        "seat": "Fylakas",
        "rank": "Chapel",
        "address": ["Ορειβατικό Καταφύγιο Χαράλαμπος Δήμου, θέση Φύλακας, οροσειρά Ροδόπης"],
        "sources": [local_article(
            "4618-agiasmos-ton-thyranoiksion-sto-eksokklisio-tou-"
            "agiou-dimitriou-sto-katafygio-tou-ellinikou-oreivatikou-"
            "syllogou-komotinis"
        )],
        "markers": ["Ἐξωκκλήσιο Ἁγίου Δημητρίου", "Χαράλαμπος Δήμου", "Φύλακας"],
    },
    {
        "key": "peter-athonite-kerasia-papikion",
        "name": "Venerable Peter the Athonite Chapel at Kerasia of Papikion Oros",
        "local": "Ιερό Εξωκκλήσιο Οσίου Πέτρου του Αθωνίτου στην Κερασιά Παπικίου Όρους",
        "seat": "Kerasia, Papikion Oros",
        "rank": "Chapel",
        "address": ["Κερασιά Παπικίου Όρους"],
        "sources": [local_article(
            "4427-eorti-osiou-petrou-tou-athonitou-stin-iera-"
            "mitropoli"
        )],
        "markers": ["Ὁσίου Πέτρου τοῦ Ἀθωνίτου", "Κερασιά τοῦ Παπικίου Ὄρους"],
    },
    {
        "key": "irene-arriana",
        "name": "Saint Irene Chapel in Arriana",
        "local": "Ιερό Εξωκκλήσιο Αγίας Ειρήνης Αρριανών",
        "seat": "Arriana",
        "rank": "Chapel",
        "address": ["Αρριανά"],
        "sources": [local_article(
            "4349-i-eorti-tis-agias-megalomartyros-eirinis-stin-iera-"
            "mitropoli"
        )],
        "markers": ["Ἐξωκκλήσιον Ἁγίας Εἰρήνης Ἀρριανῶν"],
    },
    {
        "key": "adrianopolitan-new-martyrs-maximus-monastery",
        "name": "Adrianopolitan New Martyrs Chapel at Venerable Maximus Kavsokalyvites Monastery",
        "local": "Ιερό Παρεκκλήσιο Αδριανουπολιτών Νεομαρτύρων Αγίου Κυρίλλου και Αγίου Μιχαήλ Μαυροειδούς",
        "seat": "Papikion Oros",
        "rank": "Monastic Chapel",
        "address": ["Ιερά Μονή Οσίου Μαξίμου Καυσοκαλύβη, Παπίκιο Όρος"],
        "sources": [BASE + "/index.php/component/sppagebuilder/page/482"],
        "markers": ["Παρεκκλήσιον τῶν Ἀνδριανουπολιτῶν Νεομαρτύρων", "Ἁγίου Μιχαὴλ Μαυροειδοῦς"],
    },
    {
        "key": "life-giving-spring-phaneromeni-monastery",
        "name": "Life-Giving Spring Chapel at Panagia Phaneromeni Monastery",
        "local": "Ιερό Παρεκκλήσιο Ζωοδόχου Πηγής Ιεράς Μονής Παναγίας Φανερωμένης Βαθυρρύακος",
        "seat": "Vathyrriakos",
        "rank": "Monastic Chapel",
        "address": ["Ιερά Μονή Παναγίας Φανερωμένης Βαθυρρύακος"],
        "sources": [BASE + "/index.php/component/sppagebuilder/page/483"],
        "markers": ["παρεκκλήσιο ἀφιερωμένο στή Ζωοδόχο Πηγή"],
    },
    {
        "key": "archangels-pandrosos-monastery",
        "name": "Archangels Michael and Gabriel Chapel at the Entry of the Theotokos Monastery",
        "local": "Ιερό Παρεκκλήσιο Αρχαγγέλων Μιχαήλ και Γαβριήλ Ιεράς Μονής Εισοδίων της Θεοτόκου Πανδρόσου",
        "seat": "Pandrosos",
        "rank": "Monastic Chapel",
        "address": ["Ιερά Μονή Εισοδίων της Θεοτόκου Πανδρόσου"],
        "sources": [BASE + "/index.php/component/sppagebuilder/page/485"],
        "markers": ["παρεκκλήσιο τῶν Ἀρχαγγέλων Μιχαὴλ καὶ Γαβριήλ"],
    },
    {
        "key": "life-giving-spring-cemetery-komotini",
        "name": "Life-Giving Spring Cemetery Church in Komotini",
        "local": "Ιερός Κοιμητηριακός Ναός Ζωοδόχου Πηγής Κομοτηνής",
        "seat": "Komotini",
        "rank": "Cemetery Church",
        "address": ["Δημοτικό Κοιμητήριο Κομοτηνής"],
        "sources": [local_article(
            "4317-eorti-zoodoxou-pigis-ston-iero-koimitiriako-nao-"
            "komotinis"
        )],
        "markers": ["Κοιμητηριακό Ναό τῆς Ζωοδόχου Πηγῆς Κομοτηνῆς"],
    },
    {
        "key": "eleutherius-detention-facility-komotini",
        "name": "Saint Eleutherius Institutional Church at the Komotini Detention Facility",
        "local": "Ιερός Ναός Αγίου Ελευθερίου Καταστήματος Κράτησης Κομοτηνής",
        "seat": "Komotini",
        "rank": "Institutional Church",
        "address": ["Κατάστημα Κράτησης Κομοτηνής"],
        "sources": [local_article(
            "4309-i-kyriaki-tou-pasxa-stin-iera-mitropoli"
        )],
        "markers": ["Ναό Ἁγίου Ἐλευθερίου", "Καταστήματος Κράτησης Κομοτηνῆς"],
    },
]


for exact_record in EXACT_RECORDS:
    add_exact(exact_record)


ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}


EXPECTED_TOTAL = 117
EXPECTED_OWNER_COUNTS = {PARENT: 117}
EXPECTED_KINDS = {"monastery": 4, "parish": 113}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Church": 1,
    "Chapel": 28,
    "Institutional Chapel": 6,
    "Institutional Church": 1,
    "Metropolitan Cathedral": 1,
    "Military Chapel": 1,
    "Monastery": 4,
    "Monastic Chapel": 3,
    "Parish Church": 69,
    "Pilgrimage Church": 2,
}
EXPECTED_CONTACT_BODIES = 41
EXPECTED_PHONE_BODIES = 41
EXPECTED_PHONE_VALUES = 42
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 117
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
    if parsed.netloc not in {
            "immaroniaskomotinis.gr", "ec-patr.org",
            "ecclesiagreece.gr"}:
        raise ValueError(
            "%s carries a non-competent source: %s" % (label, value)
        )


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
        raise ValueError("Maroneia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Maroneia candidate ledger date drifted")
    expected_summary = {
        PARENT: 117,
        "total": 117,
        "current_parish_cards": 71,
        "parish_kind_rows": 113,
        "monastery_kind_rows": 4,
        "exact_current_chapel_bodies": 38,
        "exact_current_cemetery_churches": 1,
        "exact_current_institutional_churches": 1,
        "pilgrimage_churches": 2,
        "monasteries": 4,
        "contact_bodies": 41,
        "phone_bodies": 41,
        "public_phone_values": 42,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 117,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Maroneia ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Maroneia ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Maroneia ledger item has invalid sources")
            for source_url in sources:
                validate_url(
                    source_url, entry.get("candidate_id") or key
                )
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Maroneia ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Maroneia ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Maroneia candidate ledger has forbidden punctuation")
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
        raise ValueError("Maroneia English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Maroneia English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Maroneia parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Maroneia kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Maroneia rank totals drifted: %r"
                         % dict(sorted(rank_counts.items())))
    exact_chapels = sum(
        item["rank"] in {
            "Chapel", "Institutional Chapel", "Military Chapel",
            "Monastic Chapel",
        }
        for item in result
    )
    if exact_chapels != 38:
        raise ValueError("Maroneia exact chapel total drifted")
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
        raise ValueError("Maroneia contact coverage drifted: %r"
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


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def all_source_urls():
    values = {PARISH_INDEX_URL, MONASTERY_INDEX_URL}
    for row in ROWS:
        values.update(row.get("sources") or [])
        values.update(row.get("contact_sources") or [])
        if row.get("site"):
            values.add(row["site"])
    ledger = validate_ledger()
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        for entry in ledger[key]:
            values.update(entry.get("sources") or [])
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
            if not payload.startswith(b"%PDF"):
                raise ValueError("invalid PDF payload")
            return None
        if "html" not in content_type:
            raise ValueError("unexpected content type %s" % content_type)
        return normalize_source_text(payload.decode("utf-8", "replace"))


def check_live_sources():
    failures = []
    source_texts = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(fetch_live_source, url): url
            for url in all_source_urls()
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                source_texts[url] = future.result()
            except Exception as exc:
                failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join(
            "%s [%s]" % pair for pair in sorted(failures)
        )
        raise ValueError("live Maroneia source check failed: %s" % rendered)
    marker_failures = []
    for row in ROWS:
        markers = [normalize_source_text(value)
                   for value in LIVE_MARKERS[row["id"]]]
        if not any(
            source_texts.get(url) is not None and
            all(marker in source_texts.get(url, "") for marker in markers)
            for url in row["sources"]
        ):
            marker_failures.append((row["id"], LIVE_MARKERS[row["id"]]))
    if marker_failures:
        raise ValueError(
            "live Maroneia exact-source marker check failed: %r"
            % marker_failures
        )


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
            "Maroneia: %d exact named bodies; %d carry current public "
            "body-associated contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Maroneia: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
