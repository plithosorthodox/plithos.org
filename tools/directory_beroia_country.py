#!/usr/bin/env python3
"""Validate exact named Beroia bodies from current first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_beroia_country.py --check
    python tools/directory_beroia_country.py --dump
    python tools/directory_beroia_country.py --check-live
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "beroia_country.json"
)
PARENT = "ep-beroia"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-moni-veroias-naoysis-kampanias/"
)
INSTITUTIONAL_PAGE = "https://imverias.gr/proskinimatikoi-idrimatikoi-naoi/"


SOURCE_GROUPS = [
    {
        "key": "beroia",
        "url": "https://imverias.gr/arxieratiki-perifereia-verias/",
        "modified": "2026-10-06T20:06:32",
        "rows": r'''
M|Beroia|Βέροια|Ιερός Μητροπολιτικός Ναός Αγίων Αποστόλων Πέτρου και Παύλου Βεροίας (17ου αι.)|Holy Apostles Peter and Paul|Metropolitan Cathedral|2331022300
C|Χριστού Παντοκράτορος (16ου αιώνος)|Christ Pantocrator|Chapel
C|Παναγίας Φανερωμένης (16ου αιώνος)|Panagia Phaneromene|Chapel
C|Παναγίας Βαλτεσινής - Εισόδιων της Θεοτόκου (18ου αιώνος)|Panagia Valtessini and Entry of the Theotokos|Chapel
C|Αγίου Διονυσίου|Saint Dionysius|Chapel
C|Παναγίας Παλαιοφορίτισας ή Παντάνασσας (16ου αιώνος)|Panagia Palaioforitissa or Pantanassa|Chapel
C|Αγίων Θεοδώρων (15ου αιώνος)|Holy Theodore Martyrs|Chapel
C|Αγίου Δημητρίου (16ου αιώνος)|Saint Demetrius|Chapel
C|Αγίου Βλασίου (13ου αιώνος)|Saint Blaise|Chapel
C|Αντιφωνητού (Μονή του Σωτήρος Χριστού, 14ου αιώνος)|Christ Antiphonetes, Monastery of Christ the Savior|Chapel
C|Μικροί Άγιοι Ανάργυροι (17ου αιώνος)|Little Holy Unmercenaries|Chapel
C|Αγίου Νικολάου Φραντζή (κουβούκλιο)|Saint Nicholas Frantzis|Shrine
C|Αγίων Κωνσταντίνου και Ελένης (κουβούκλιο)|Saints Constantine and Helen|Shrine
M|Beroia|Βέροια|Ιερός Προσκυνηματικός Ναός Οσίου Αντωνίου του Νέου, Πολιούχου Βεροίας|Venerable Anthony the New, Patron of Beroia|Pilgrimage Church|2331022260
C|Αγίου Νικολα΄ου του Άρχοντος Καλοκρατά (Λαμαρινά - 15ου αιώνος)|Saint Nicholas of Archon Kalokratas at Lamarina|Chapel
C|Αγίου Γεωργίου (Αρχοντος Γραμματικού - 13ου αιώνος)|Saint George of Archon Grammatikos|Chapel
C|Αγίου Ιωάννου του Θεολόγου|Saint John the Theologian|Chapel
M|Beroia|Βέροια|Ιερός Ναός Αγίων Αναργύρων Βεροίας|Holy Unmercenaries|Parish Church|2331022944
C|Aγίων Αναργύρων (16ου αιώνος - παλαιός ναός)|Old Holy Unmercenaries|Chapel
C|Μεταμορφώσεως του Σωτήρος (16ου αιώνος)|Transfiguration of the Savior|Chapel
C|Αγίων Νικολάου του Ψαρά και Φανουρίου (16ου αιώνος)|Saints Nicholas the Fisherman and Phanourios|Chapel
C|Παναγίας Περιβλέπτου (14ου αιώνος)|Panagia Peribleptos|Chapel
C|Οσίου Παταπίου (15ου αιώνος)|Venerable Patapios|Chapel
C|Αγίας Άννης (19ου αιώνος)|Saint Anna|Chapel
C|Aγίου Βασιλείου (19ου αιώνος)|Saint Basil|Chapel
C|Αγίας Βαρβάρας|Saint Barbara|Chapel
M|Beroia|Βέροια|Ιερός Ναός Αγίου Γεωργίου Βεροίας (14ου αι.)|Saint George|Parish Church|2331064153
C|Παναγίας Δεξιάς (14ου αιώνος)|Panagia Dexia|Chapel
C|Αγίας Παρασκευής (14ου αιώνος)|Saint Paraskevi|Chapel
C|Αγίου Ανδρέου (16ου αιώνος)|Saint Andrew|Chapel
C|Προφήτου Ηλίου|Prophet Elijah|Chapel
C|Αγίου Νικολάου του μοναχού Ανθίμου (16ου αιώνος)|Saint Nicholas of Monk Anthimos|Chapel
C|Αγίου Νικολάου της Δεξιάς (18ου αιώνος)|Saint Nicholas of Dexia|Chapel
C|Αγίου Νικολάου (17ου αιώνος)|Saint Nicholas|Chapel
C|Αγίας Παρασκευής της Δεξιάς (18ου αιώνος)|Saint Paraskevi of Dexia|Chapel
M|Beroia|Βέροια|Ιερός Ναός Αγίου Σάββα - Κυριώτισσας Βεροίας (14ου αι.)|Saint Sabbas and Panagia Kyriotissa|Parish Church|2331022034
C|Υπαπαντής του Χριστού ή Παναγούδα (14ου αιώνος)|Presentation of Christ or Panagouda|Chapel
C|Παναγίας Γοργοϋπηκόου (14ου αιώνος)|Panagia Gorgoepikoos|Chapel
C|Αγίου Ανδρέου (15ου αιώνος)|Saint Andrew|Chapel
M|Beroia|Βέροια|Ιερός Ναός Αγίου Ιωάννου του Ελεήμονος Βεροίας (19ου αι.)|Saint John the Merciful|Parish Church|
C|Αγίων Σπυρίδωνος, Νικολάου και Ελευθερίου (19ου αιώνος)|Saints Spyridon, Nicholas, and Eleutherius|Chapel
C|Αγίας Αννης (15ου αιώνος)|Saint Anna|Chapel
C|Αγίου Νιολάου της Γούρνας (15ου αιώνος - οδ. Παστέρ)|Saint Nicholas of Gourna on Pasteur Street|Chapel
C|Αγίου Νικολάου Μακαριώτησσας (16ου αιώνος - οδ. Κωντογιωργάκη)|Saint Nicholas Makariotissa on Kontogiorgaki Street|Chapel
C|Αγίου Στεφάνου (16ου αιώνος)|Saint Stephen|Chapel
C|Παναγίας Ευαγγελίστρια (16ου αιώνος)|Annunciation of the Theotokos|Chapel
C|Αγίου Γεωργίου του Μικρού (15ου αιώνος)|Little Saint George|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Χριστού (Μονή του Καλοθέτου, 13ου αιώνος)|Christ, Monastery of Kalothetos|Chapel
C|Αγίων Κηρύκου και Ιουλίττης (14ου αιώνος)|Saints Cyricus and Julitta|Chapel
C|Προφήτου Ηλιού (19ου αιώνος)|Prophet Elijah|Chapel
M|Beroia|Βέροια|Ιερός Ναός Αγίας Παρασκευής Βεροίας|Saint Paraskevi|Parish Church|2331028172
M|Beroia|Βέροια|Ιερός Ναός Αναλήψεως του Κυρίου - Αγίου Νεκταρίου Βεροίας|Ascension of the Lord and Saint Nectarios|Parish Church|2331028619
M|Beroia|Βέροια|Ιερός Ναός Οσίου Νικοδήμου - Αγίων Κωνσταντίνου και Ελένης Βεροίας|Venerable Nicodemus and Saints Constantine and Helen|Parish Church|2331070342
C|Οσίου Αμφιλοχίου του εν Πάτμω|Venerable Amphilochios of Patmos|Chapel
M|Beroia|Βέροια|Ιερός Ναός Υπαπαντή του Κυρίου Βεροίας|Presentation of the Lord|Parish Church|2331073890
C|Παναγίας Χαβιαρά (15ου αιώνος)|Panagia Chaviara|Chapel
C|Αγίου Προκοπίου|Saint Procopius|Chapel
M|Beroia|Βέροια|Ιερός Ναός Αγίου Τιμοθέου Βεροίας|Saint Timothy|Parish Church|2331026927
M|Beroia|Βέροια|Ιερός Ναός Αγίου Αθανασίου Βεροίας (Κοιμητήρια)|Saint Athanasius|Cemetery Church|2331021415
M|Panorama, Beroia|Πανόραμα Βεροίας|Ιερός Ναός Αγίας Τριάδος Πανοράματος Βεροίας|Holy Trinity|Parish Church|2331060963
''',
    },
    {
        "key": "naoussa",
        "url": "https://imverias.gr/arxieratiki-perifereia-naoussis/",
        "modified": "2025-11-13T10:04:49",
        "rows": r'''
M|Naoussa|Νάουσα|Ιερός Μητροπολιτικός Ναός Μεταμορφώσεως του Σωτήρος Ναούσης|Transfiguration of the Savior|Metropolitan Cathedral|2332022237
C|Μεταμορφώσεως του Σωτήρος (έξω Αγιος Σωτήρας)|Transfiguration of the Savior, Exo Agios Sotiras|Country Church
C|Αγίας Τριάδος|Holy Trinity|Chapel
C|Υπαπαντής του Κυρίου|Presentation of the Lord|Chapel
M|Naoussa|Νάουσα|Ιερός Ναός Αγίου Γεωργίου Ναούσης|Saint George|Parish Church|2332022490
M|Naoussa|Νάουσα|Ιερός Ναός Αγίου Δημητρίου Ναούσης|Saint Demetrius|Parish Church|2332022705
C|Αγίου Νικολάου|Saint Nicholas|Chapel
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Υπαπαντής του Κυρίου|Presentation of the Lord|Chapel
C|Αγίου Παντελεήμονος|Saint Panteleimon|Chapel
C|Αγίας Τριάδος|Holy Trinity|Chapel
M|Naoussa|Νάουσα|Ιερός Ναός Κοιμήσεως της Θεοτόκου Ναούσης|Dormition of the Theotokos|Parish Church|2332022272
C|Αγίου Αθανασίου (Κοιμητήρια)|Saint Athanasius|Cemetery Church
C|Οσίου Θεοφάνους|Venerable Theophanes|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Τιμίου Προδρόμου|Holy Forerunner|Chapel
C|Αγίας Άννης και Οσίου Γερασίμου του Υμνογράφου|Saint Anna and Venerable Gerasimos the Hymnographer|Chapel
M|Naoussa|Νάουσα|Ιερός Ναός Αγίου Μηνά Ναούσης|Saint Menas|Parish Church|2332028327
C|Τιμίου Προδρόμου (Μέσα Πρόδρομος)|Holy Forerunner, Mesa Prodromos|Chapel
M|Naoussa|Νάουσα|Ιερός Ναός Ευαγγελισμού της Θεοτόκου Ναούσης|Annunciation of the Theotokos|Parish Church|2332026055
C|Αγίου Ιωάννου του Θεολόγου|Saint John the Theologian|Chapel
M|Arkochori|Αρκοχώρι|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
C|Αγίου Νικολάου|Saint Nicholas|Chapel
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
M|Stenimachos|Στενήμαχος|Ιερός Ναός Αγίων Αναργύρων|Holy Unmercenaries|Parish Church|2332042992
C|Αγίου Τρύφωνος|Saint Tryphon|Chapel
''',
    },
    {
        "key": "alexandria",
        "url": "https://imverias.gr/arxieratikhperifereiaalexandreias/",
        "modified": "2026-10-06T20:18:14",
        "rows": r'''
M|Alexandria|Αλεξάνδρεια|Ιερός Μητροπολιτικός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Metropolitan Cathedral|2333022021
C|Αγίου Αθανασίου (Κοιμητήρια)|Saint Athanasius|Cemetery Church
C|Αγίου Γεωργίου|Saint George|Chapel
C|Οσίου Πορφυρίου του Καυσοκαλυβίτου|Venerable Porphyrios of Kavsokalyvia|Chapel
M|Alexandria|Αλεξάνδρεια|Ιερός Ναός Αγίου Αλεξάνδρου|Saint Alexander|Parish Church|2333028170
C|Αγίου Ιωάννου του Κουκουζέλου|Saint John Koukouzelis|Chapel
M|Alexandria|Αλεξάνδρεια|Ιερός Ναός Αγίων Κυρίλλου και Μεθοδίου|Saints Cyril and Methodius|Parish Church|2333024500
C|Αγίου Δημητρίου|Saint Demetrius|Chapel
C|Οσίου Εφραίμ Νέας Μάκρης|Venerable Ephraim of Nea Makri|Chapel
M|Vrysaki|Βρυσάκι|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|
M|Kampochori|Καμποχώρι|Ιερός Ναός Αγίου Γεωργίου και Αγίας Ιερουσαλήμ|Saint George and Saint Jerusalem|Parish Church|
C|Οσίου Παισίου του Αγιορείτου|Venerable Paisios of Mount Athos|Chapel
M|Kapsochori|Καψοχώρι|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2333024359
C|Αγίου Δημητρίου (Κοιμητήρια)|Saint Demetrius|Cemetery Church
C|Αγίου Φανουρίου|Saint Phanourios|Chapel
M|Loutros|Λουτρός|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen|Parish Church|
C|Αγίων Ραφαήλ, Νικολάου και Ειρήνης|Saints Raphael, Nicholas, and Irene|Chapel
C|Αγίων Κωνσταντίνου & Ελένης (Κοιμητήρια)|Saints Constantine and Helen|Cemetery Church
M|Neochori|Νεοχώρι|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2333022861
C|Αγίου Δημητρίου (Κοιμητήρια)|Saint Demetrius|Cemetery Church
M|Niseli|Νησέλι|Ιερός Ναός Αγίου Ιωάννου του Θεολόγου|Saint John the Theologian|Parish Church|
M|Nisi|Νησί|Ιερός Ναός Αγίων Αναργύρων|Holy Unmercenaries|Parish Church|
C|Αγίων Αναργύρων (παλαιός μοναστηριακός ναός)|Holy Unmercenaries, Old Monastic Church|Historic Monastic Church
C|Αγίας Παρασκευής (εξωκλήσι)|Saint Paraskevi|Country Church
C|Αγίου Παντελεήμονος|Saint Panteleimon|Chapel
M|Schoinas|Σχοινάς|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
C|Αγίας Ειρήνης Χρυσοβαλάντου|Saint Irene Chrysovalantou|Chapel
''',
    },
    {
        "key": "kampania",
        "url": "https://imverias.gr/arxieratiki-perifereia-kampanias/",
        "modified": "2026-10-06T20:19:36",
        "rows": r'''
M|Chalastra|Χαλάστρα|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2310792241
C|Αγίων Θεοδώρων (Κοιμητήρια)|Holy Theodore Martyrs|Cemetery Church
C|Αγίου Δημητρίου|Saint Demetrius|Chapel
M|Chalastra|Χαλάστρα|Ιερός Ναός Αγίων Νεομαρτύρων Αθανασίου και Ιωάννου|New Martyrs Athanasius and John|Parish Church|2310794908
C|Αγίων Αθανασίου και Γερασίμου του Υμνογράφου|Saints Athanasius and Gerasimos the Hymnographer|Chapel
C|Αγίου Νικολάου|Saint Nicholas|Chapel
C|Οσίας Πολυξένης|Venerable Polyxene|Chapel
M|Anatoliko|Ανατολικό|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|2310718004
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Αγίων Γεωργίου και Φανουρίου|Saints George and Phanourios|Chapel
C|Αγίου Πνεύματος|Holy Spirit|Chapel
M|Kymina|Κύμινα|Ιερός Ναός Αγίων Αποστόλων Πέτρου και Παύλου|Holy Apostles Peter and Paul|Parish Church|2391041208
C|Αγίου Νεκταρίου|Saint Nectarios|Chapel
C|Αγίου Αντωνίου (εξωκλήσι)|Saint Anthony|Country Church
C|Προφήτου Ηλιού (εξωκλήσι)|Prophet Elijah|Country Church
C|Κοιμήσεως της Θεοτόκου (εξωκλήσι)|Dormition of the Theotokos|Country Church
M|Vrachia|Βραχιά|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2391031001
M|Nea Malgara|Νέα Μάλγαρα|Ιερός Ναός Γενεσίου της Θεοτόκου|Nativity of the Theotokos|Parish Church|2391041366
C|Αγίων Αναργύρων|Holy Unmercenaries|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Αγίου Χριστοφόρου|Saint Christopher|Chapel
M|Adendro|Άδενδρο|Ιερός Ναός Αγίου Αθανασίου|Saint Athanasius|Parish Church|2391031295
C|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen|Chapel
C|Αγίου Παντελεήμονος|Saint Panteleimon|Chapel
C|Παναγίας Προυσσιωτίσης|Panagia Prousiotissa|Chapel
C|Αρχαγγέλου Μιχαήλ (Κοιμητήρια)|Archangel Michael|Cemetery Church
''',
    },
    {
        "key": "meliki",
        "url": "https://imverias.gr/arxieratiki-perifereia-melikis/",
        "modified": "2025-11-13T10:06:33",
        "rows": r'''
M|Meliki|Μελίκη|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2331304536
C|Αγίου Νικολάου (Κοιμητήρια)|Saint Nicholas|Cemetery Church
C|Αγίας Τριάδος - Αποστόλου Τίτου|Holy Trinity and Apostle Titus|Chapel
C|Αγίου Λουκά|Saint Luke|Chapel
C|Αγίας Κυριακής|Saint Kyriaki|Chapel
M|Agia Triada|Αγία Τριάδα|Ιερός Ναός Αγίας Ειρήνης Χρυσοβαλάντου|Saint Irene Chrysovalantou|Parish Church|
C|Τιμίου Προδρόμου|Holy Forerunner|Chapel
C|Αγίας Τριάδος|Holy Trinity|Chapel
M|Agkathia|Αγκαθιά|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|2331099577
C|Αγίων Γεωργίου και Νικάνωρος|Saints George and Nicanor|Chapel
M|Kypseli|Κυψέλη|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
C|Αγίου Δημητρίου|Saint Demetrius|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
M|Neokastro|Νεόκαστρο|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|2331081598
C|Αγίου Γεωργίου|Saint George|Chapel
C|Αγίας Αικατερίνης|Saint Catherine|Chapel
M|Neos Prodromos|Νέος Πρόδρομος|Ιερός Ναός Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Parish Church|
M|Palaios Prodromos|Παλαιός Πρόδρομος|Ιερός Ναός Αγίων Αποστόλων|Holy Apostles|Parish Church|
C|Αγίων Αποστόλων Πέτρου και Παύλου (Κοιμητήρια)|Holy Apostles Peter and Paul|Cemetery Church
M|Trilofia|Τριλοφιά|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|
''',
    },
    {
        "key": "plateos",
        "url": "https://imverias.gr/arxieratiki-perifereia-platos/",
        "modified": "2026-10-06T20:26:40",
        "rows": r'''
M|Platy|Πλατύ|Ιερός Ναός Γενέσεως της Θεοτόκου Πλατέoς|Nativity of the Theotokos|Parish Church|2331064100
C|Αγίων Αρσενίου και Παισίου|Saints Arsenios and Paisios|Chapel
M|Arachos|Άραχος|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen|Parish Church|
M|Kleidi|Κλειδί|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2333071400
C|Ζωοδόχου Πηγής|Life-Giving Spring|Chapel
C|Αγίου Δημητρίου|Saint Demetrius|Chapel
C|Αγίου Νικολάου|Saint Nicholas|Chapel
M|Koryfi|Κορυφή|Ιερός Ναός Αγίας Παρασκευής και Αγίου Παντελεήμονος|Saint Paraskevi and Saint Panteleimon|Parish Church|2333071793
C|Αγίων Θεοδώρων (Κοιμητήρια)|Holy Theodore Martyrs|Cemetery Church
M|Kydonia|Κυδωνιά|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|
C|Αγίου Παντελεήμονος|Saint Panteleimon|Chapel
M|Lianovergi|Λιανοβέργι|Ιερός Ναός Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Parish Church|2333063911
C|Αγίου Αθανασίου (Κοιμητήρια)|Saint Athanasius|Cemetery Church
C|Αγίας Αναστασίας|Saint Anastasia|Chapel
M|Neochoropoulo|Νεοχωρόπουλο|Ιερός Ναός Αγίων Αποστόλων|Holy Apostles|Parish Church|
C|Αγίου Ιωάννου Θεολόγου (Κοιμητήρια)|Saint John the Theologian|Cemetery Church
M|Niseloudi and Palaiochora|Νησελούδι και Παλαιόχωρα|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
C|Αγίας Άννης (Νησελούδι)|Saint Anna in Niseloudi|Chapel
C|Αγίου Αθανασίου (Παλαιόχωρα)|Saint Athanasius in Palaiochora|Chapel
M|Palaiochori|Παλαιοχώρι|Ιερός Ναός Τιμίου Προδρόμου|Holy Forerunner|Parish Church|
C|Γενέσεως του Τιμίου Προδρόμου|Nativity of the Holy Forerunner|Chapel
M|Platanos|Πλάτανος|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|
M|Prasinada|Πρασινάδα|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|
M|Trikala|Τρίκαλα|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
C|Αγίας Τριάδος|Holy Trinity|Chapel
C|Αγίου Κοσμά του Αιτωλού|Saint Cosmas of Aetolia|Chapel
C|Οσίου Εφραίμ Νέας Μάκρης|Venerable Ephraim of Nea Makri|Chapel
C|Όσιας Σοφίας της Κλεισούρας|Venerable Sophia of Kleisoura|Chapel
C|Οσίων Δαβίδ και Ιακώβου (εντός του Ι. Ν.)|Venerable David and James, inside the parish church|Chapel
''',
    },
    {
        "key": "eirinoupoleos",
        "url": "https://imverias.gr/arxieratiki-perifereia-eirinoupoleos/",
        "modified": "2025-11-13T10:04:34",
        "rows": r'''
M|Angelochori|Αγγελοχώρι|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
C|Αγίων Ραφαήλ, Νικολάου και Ειρήνης|Saints Raphael, Nicholas, and Irene|Chapel
C|Αγίας Ειρήνη|Saint Irene|Chapel
M|Archangelos|Αρχάγγελος|Ιερός Ναός Αγίων Αρχαγγέλων|Holy Archangels|Parish Church|
C|Αγίων Αρχαγγέλων (παλαιός ναός)|Old Holy Archangels|Chapel
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
M|Ano Zervochori|Άνω Ζερβοχώρι|Ιερός Ναός Προφήτου Ηλιού|Prophet Elijah|Parish Church|
M|Kato Zervochori|Κάτω Ζερβοχώρι|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|
C|Αγίου Νικολάου (παλαιός Ναός)|Old Saint Nicholas|Chapel
M|Kopanos|Κοπανός|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2332042252
C|Αγίου Νικολάου|Saint Nicholas|Chapel
C|Αγίων Πάντων|All Saints|Chapel
C|Αγίου Κοσμά του Αιτωλού|Saint Cosmas of Aetolia|Chapel
M|Monospita|Μονόσπιτα|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|2331042140
M|Polyplatanos|Πολυπλάτανος|Ιερός Ναός Αγίου Χριστοφόρου|Saint Christopher|Parish Church|2332047138
C|Αγίου Χριστοφόρου (παλαιός ναός)|Old Saint Christopher|Chapel
M|Chariesa|Χαρίεσσα|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2332042842
C|Αγίων Ραφαήλ, Νικολάου και Ειρήνης (Κοιμητήρια)|Saints Raphael, Nicholas, and Irene|Cemetery Church
C|Ζωοδόχου Πηγής (εξωκλήσι)|Life-Giving Spring|Country Church
''',
    },
    {
        "key": "antigonidon",
        "url": "https://imverias.gr/arxieratiki-perifereia-antigonidon/",
        "modified": "2026-10-06T20:28:10",
        "rows": r'''
M|Kavasila|Καβάσιλα|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2331038005
M|Episkopi|Επισκοπή|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|
C|Αγίας Αικατερίνης (Κοιμητήρια)|Saint Catherine|Cemetery Church
M|Kalochori|Καλοχώρι|Ιερός Ναός Γενεσίου της Θεοτόκου|Nativity of the Theotokos|Parish Church|
M|Kefalochori|Κεφαλοχώρι|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2331097133
M|Xechasmeni|Ξεχασμένη|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|2331097135
C|Αγίου Δημητρίου (18ος αι.)|Eighteenth-century Saint Demetrius|Chapel
M|Palaio Skylitsi|Παλαιό Σκυλίτσι|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen|Parish Church|
C|Αγίου Νικολάου (Κοιμητήρια)|Saint Nicholas|Cemetery Church
M|Rapsomaniki|Ραψομανίκη|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|
M|Stavros|Σταυρός|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
C|Αγίας Παρασκευής (Κοιμητήρια)|Saint Paraskevi|Cemetery Church
''',
    },
    {
        "key": "apostle-paul",
        "url": "https://imverias.gr/arxieratiki-perifereia-apostolou-pavlou/",
        "modified": "2025-11-13T10:12:46",
        "rows": r'''
M|Makrochori|Μακροχώρι|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|2331041718
C|Αγίου Θεοδώρου|Saint Theodore|Chapel
M|Makrochori|Μακροχώρι|Ιερός Ναός Τιμίου Προδρόμου|Holy Forerunner|Parish Church|2331041239
M|Diavatos|Διαβατός|Ιερός Ναός Αγίων Κωνσταντίνου, Ελένης και Ελευθερίου|Saints Constantine, Helen, and Eleutherius|Parish Church|2331041831
C|Αγίων Αποστόλων Πέτρου και Παύλου|Holy Apostles Peter and Paul|Chapel
C|Αγίου Λουκά Συμφερουπόλεως (εντός του Ι.Ν.)|Saint Luke of Simferopol, inside the parish church|Chapel
M|Kouloura|Κουλούρα|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|2331097354
C|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen|Chapel
C|Αγίου Δημητρίου|Saint Demetrius|Chapel
M|Nea Lykogianni|Νέα Λυκογιάννη|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
M|Palaia Lykogianni|Παλαιά Λυκογιάννη|Ιερός Ναός Αγίων Αποστόλων|Holy Apostles|Parish Church|
M|Nea Nikomedeia|Νέα Νικομήδεια|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|2331090235
C|Αγίου Παντελεήμονος|Saint Panteleimon|Chapel
''',
    },
    {
        "key": "vergina",
        "url": "https://imverias.gr/arxieratiki-perifereia-verginis/",
        "modified": "2025-11-13T10:11:15",
        "rows": r'''
M|Vergina|Βεργίνα|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2331092325
C|Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Chapel
C|Αγίου Φωτίου|Saint Photios|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Αγίων Θεοδώρων|Holy Theodore Martyrs|Chapel
C|Αγίου Γεωργίου|Saint George|Chapel
M|Palatitsia|Παλατίτσια|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2331092554
C|Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Chapel
C|Αγίου Δημητρίου (16ος αι.)|Sixteenth-century Saint Demetrius|Chapel
M|Polydendri|Πολυδένδρι|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
C|Αγίου Αθανασίου (Κοιμητήρια)|Saint Athanasius|Cemetery Church
C|Αγίου Χριστοφόρου|Saint Christopher|Chapel
C|Αγίου Νικολάου|Saint Nicholas|Chapel
M|Rizomata|Ριζώματα|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2331096344
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Οσίου Δαβίδ του εν Ευβοία|Venerable David of Euboea|Chapel
M|Daskio|Δάσκιο|Ιερός Ναός Αγίας Τριάδος|Holy Trinity|Parish Church|
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
C|Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Chapel
M|Sykia|Συκιά|Ιερός Ναός Τιμίου Προδρόμου|Holy Forerunner|Parish Church|
C|Αγίου Αθανασίου (εξωκλήσι - περιοχή Βάτα)|Saint Athanasius in Vata|Country Church
M|Sphikia|Σφηκιά|Ιερός Ναός Αγίων Κωνσταντίνου & Ελένης|Saints Constantine and Helen|Parish Church|
C|Αγίου Αθανασίου (Κοιμητήρια)|Saint Athanasius|Cemetery Church
C|Αγίου Γεωργίου|Saint George|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Αγίου Δημητρίου|Saint Demetrius|Chapel
C|Αγίων Αποστόλων|Holy Apostles|Chapel
M|Charadra|Χαράδρα|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
M|Elafina|Ελαφίνα|Ιερός Ναός Αγίας Παρασκευής|Saint Paraskevi|Parish Church|
M|Metochi|Μετόχι|Ιερός Ναός Αγίου Παντελεήμονος|Saint Panteleimon|Parish Church|2331028227
C|Αγίων Κωνσταντίνου και Ελένης (Κοιμητήρια)|Saints Constantine and Helen|Cemetery Church
''',
    },
    {
        "key": "dovra",
        "url": "https://imverias.gr/arxieratiki-perifereia-dovras/",
        "modified": "2023-04-04T08:25:21",
        "rows": r'''
M|Agios Georgios|Άγιος Γεώργιος|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2331051210
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
C|Αγίου Γεωργίου|Saint George|Chapel
M|Agia Marina|Αγία Μαρίνα|Ιερός Ναός Αγίας Μαρίνας|Saint Marina|Parish Church|2331051178
M|Patrida|Πατρίδα|Ιερός Ναός Υπαπαντής του Χριστού|Presentation of Christ|Parish Church|2331066422
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Αγίου Νικολάου|Saint Nicholas|Chapel
M|Trilofos|Τρίλοφος|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
C|Αγίας Παρασκευής (Κοιμητήρια)|Saint Paraskevi|Cemetery Church
C|Αγίου Τρύφωνος|Saint Tryphon|Chapel
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
M|Fytia|Φυτιά|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|
C|Αγίων Αθανασίου, Μητροφάνους και Διονυσίου του Ρήτορος|Saints Athanasius, Metrophanes, and Dionysius the Rhetor|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
C|Αγίου Μοδέστου|Saint Modestus|Chapel
C|Αγίων Θεοδώρων|Holy Theodore Martyrs|Chapel
C|Αγίου Νικολάου (Μαρούσα)|Saint Nicholas in Marousa|Chapel
C|Αγίου Αθανασίου (παλαιός Ναός)|Old Saint Athanasius|Chapel
M|Kostochori|Κωστοχώρι|Ιερός Ναός Αγίων Αποστόλων|Holy Apostles|Parish Church|
C|Τιμίου Προδρόμου|Holy Forerunner|Chapel
C|Μεταμόρφωση του Σωτήρος|Transfiguration of the Savior|Chapel
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
''',
    },
    {
        "key": "beroia-outskirts",
        "url": "https://imverias.gr/arxieratiki-perifereia-perichoron-verias/",
        "modified": "2023-04-04T08:28:30",
        "rows": r'''
M|Agia Varvara|Αγία Βαρβάρα|Ιερός Ναός Αγίας Βαρβάρας και Aγίου Τρύφωνος|Saint Barbara and Saint Tryphon|Parish Church|2331091515
C|Αγίου Νικολάου (Κοιμητήρια)|Saint Nicholas|Cemetery Church
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Αγίων Αλεξάνδρου και Γεωργίου Καρσλίδη|Saints Alexander and George Karslides|Chapel
M|Ammos|Άμμος|Ιερός Ναός Αγίου Γεωργίου και Οσίου Ιακώβου|Saint George and Venerable Iakovos|Parish Church|
C|Αγίας Παρασκευή (Εξωκλήσι)|Saint Paraskevi|Country Church
M|Asomata|Ασώματα|Ιερός Ναός Παμμεγίστων Ταξιαρχών|Holy Archangels|Parish Church|
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
C|Αγίας Παρασκευής|Saint Paraskevi|Chapel
M|Georgiani|Γεωργιανοί|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
C|Αγίου Νεκταρίου (Κοιμητήρια)|Saint Nectarios|Cemetery Church
M|Tripotamos|Τριπόταμος|Ιερός Ναός Αγίων Αποστόλων|Holy Apostles|Parish Church|2331063518
C|Αγίου Αθανασίου (Ντουρμάνι)|Saint Athanasius in Ntourmani|Chapel
C|Αγίου Νικολάου - Παναγίας|Saint Nicholas and the Panagia|Chapel
C|Αγίου Γεωργίου (Κομνήνιο)|Saint George in Komnenio|Chapel
C|Αγίου Νικολάου (Κομνήνιο)|Saint Nicholas in Komnenio|Chapel
M|Rachi|Ράχη|Ιερός Ναός Αγίου Αθανασίου|Saint Athanasius|Parish Church|2331062171
C|Αναλήψεως (Κότσικα)|Ascension in Kotsika|Chapel
M|Tagarochori|Ταγαροχώρι|Ιερός Ναός Προφήτου Ηλιού|Prophet Elijah|Parish Church|
M|Messi|Μέση|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2331041743
M|Kastania|Καστανιά|Ιερός Ναός Τιμίου Προδρόμου|Holy Forerunner|Parish Church|
C|Προφήτου Ηλιού|Prophet Elijah|Chapel
C|Αγίου Χριστοφόρου|Saint Christopher|Chapel
M|Lazochoi|Λαζοχώρι|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
M|Seli|Σέλι|Ιερός Ναός Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Parish Church|2331026009
C|Αγίων Αποστόλων|Holy Apostles|Chapel
C|Αναλήψεως του Κυρίου|Ascension of the Lord|Chapel
M|Koumaria|Κουμαριά|Ιερός Ναός Αγίου Νικολάου|Saint Nicholas|Parish Church|
C|Μικρής Παναγιάς|Little Panagia|Chapel
C|Αγίου Γεωργίου|Saint George|Chapel
M|Xirolivado|Ξηρολίβαδο|Ιερός Ναός Προφήτου Ηλιού|Prophet Elijah|Parish Church|2331026009
C|Αγίου Αθανασίου|Saint Athanasius|Chapel
M|Lefkopetra|Λευκόπετρα|Ιερός Ναός Αγίου Γεωργίου|Saint George|Parish Church|
C|Αγίων Αποστόλων Πέτρου και Παύλου|Holy Apostles Peter and Paul|Chapel
M|Mikri Santa|Μικρή Σάντα|Ιερός Ναός Αγίου Δημητρίου|Saint Demetrius|Parish Church|
C|Αγίου Αθανασίου (Κοιμητήρια)|Saint Athanasius|Cemetery Church
''',
    },
]


MONASTIC_RECORDS = [
    {
        "local": "Πατριαρχική καί Σταυροπηγιακή Μονή Τιμίου Προδρόμου Σκήτης Βεροίας",
        "name": "Patriarchal and Stavropegial Monastery of the Holy Forerunner at the Skete of Beroia",
        "seat": "Skete of Beroia",
        "address": ["Ι. Μονή Τιμίου Προδρόμου, Τ.Θ. 10, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastery",
        "site": "https://apotomi.gr/",
        "sources": [
            PATRIARCHATE_PAGE,
            "https://imverias.gr/moni-timiou-prodromou-skiti/",
            "https://apotomi.gr/",
        ],
    },
    {
        "local": "Παναγίας Δοβρᾶ",
        "name": "Panagia Dovra Monastery",
        "seat": "Beroia",
        "address": ["Ι. Μ. Παναγίας Δοβρά, Τ.Θ.241, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastery",
        "phones": ["2331027599"],
        "sources": [PATRIARCHATE_PAGE, "https://imverias.gr/iera-moni-panagias-dovra/"],
    },
    {
        "local": "Γεν. Θεοτόκου Καλλίπετρας - Ράχη Βεροίας",
        "name": "Nativity of the Theotokos Kallipetra Monastery",
        "seat": "Rachi, Beroia",
        "address": ["Ι.Μ. Θεοτόκου Καλλίπετρας, Τ.Θ. Ράχη, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastery",
        "site": "https://imkallipetras.gr/",
        "emails": ["imkallipetras@gmail.com"],
        "sources": [
            PATRIARCHATE_PAGE,
            "https://imverias.gr/iera-moni-kallitetras/",
            "https://imkallipetras.gr/",
        ],
    },
    {
        "local": "Τιμίου Προδρόμου Ναούσης",
        "name": "Holy Forerunner Monastery in Naoussa",
        "seat": "Naoussa",
        "address": ["Ι.Μ. Τιμίου Προδρόμου Ναούσης, Τ.Κ. 592 00, Νάουσα Ημαθίας"],
        "rank": "Monastery",
        "phones": ["2332051168"],
        "site": "https://improdromounaousas.gr/",
        "emails": ["improdromounaousas@outlook.com"],
        "sources": [
            "https://imverias.gr/iera-moni-timiou-prodromou-naoussis/",
            "https://improdromounaousas.gr/",
            "https://improdromounaousas.gr/contact/",
        ],
    },
    {
        "local": "Πατριαρχική καί Σταυροπηγιακή Μονή Ἁγίου Ἀθανασίου Σφηνίτσης",
        "name": "Patriarchal and Stavropegial Monastery of Saint Athanasius of Sphinitsa",
        "seat": "Agkathia",
        "address": ["Ι. Μ. Αγίου Αθανασίου Σφηνίτσης, Αγκαθιά Ημαθίας, Τ.Κ. 590 31, Μελίκη"],
        "rank": "Monastery",
        "phones": ["2331099231", "2331099142"],
        "sources": [PATRIARCHATE_PAGE, "https://imverias.gr/iera-moni-agiou-athanasiou-sfinitsis/"],
    },
    {
        "local": "Ἁγίας Κυριακῆς (παρά τό χωρίον Λουτρός)",
        "name": "Saint Kyriaki Monastery near Loutros",
        "seat": "Loutros",
        "address": ["Ι. Μ. Αγίας Κυριακής, Λουτρό Ημαθίας, Τ.Κ. 593 00, Αλεξάνδρεια"],
        "rank": "Monastery",
        "phones": ["2333088350"],
        "sources": [PATRIARCHATE_PAGE, "https://imverias.gr/iera-moni-agias-kyriakis-loutrou/"],
    },
    {
        "local": "Ἁγίων Πάντων Δήμου Βεργίνης",
        "name": "All Saints Monastery in Vergina",
        "seat": "Vergina",
        "address": ["Βεργίνα"],
        "rank": "Monastery",
        "phones": ["2331301440"],
        "sources": [PATRIARCHATE_PAGE, "https://imverias.gr/iera-moni-agion-panton-verginis/"],
    },
    {
        "local": "Μεταμορφώσεως Σωτῆρος Μουτσιάλης",
        "name": "Transfiguration of the Savior Moutsiali Monastery",
        "seat": "Moutsiali, Beroia",
        "address": ["Ι.Μ. Μεταμορφώσεως του Σωτήρος Μουτσιάλης, Τ.Θ.241, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastery",
        "phones": ["2331043443"],
        "site": "https://moutsiali.gr/",
        "sources": [
            PATRIARCHATE_PAGE,
            "https://imverias.gr/iera-moni-metamorfoseos-moutsiali/",
            "https://moutsiali.gr/epikoinonia/",
        ],
    },
    {
        "local": "Ἱερά Μονή Παμμεγίστων Ταξιαρχῶν Ναούσης",
        "name": "Holy Archangels Monastery in Naoussa",
        "seat": "Naoussa",
        "address": ["Νάουσα, Τ.Κ. 59200"],
        "rank": "Monastery under Re-establishment",
        "sources": [PATRIARCHATE_PAGE, "https://imverias.gr/iera-moni-taxiarxon-naoussis/"],
    },
    {
        "local": "Ἱερά Μονή Ζωοδόχου Πηγῆς (Παναγιοπούλα) Ναούσης",
        "name": "Life-Giving Spring Panagiopoula Monastery in Naoussa",
        "seat": "Naoussa",
        "address": ["Νάουσα, Τ.Κ. 59200"],
        "rank": "Monastery under Re-establishment",
        "sources": [
            PATRIARCHATE_PAGE,
            "https://imverias.gr/%ce%b9%ce%b5%cf%81%ce%ac-%ce%bc%ce%bf%ce%bd%ce%ae-%ce%b6%cf%89%ce%bf%ce%b4%cf%8c%cf%87%ce%bf%cf%85-%cf%80%ce%b7%ce%b3%ce%ae%cf%82-%cf%80%ce%b1%ce%bd%ce%b1%ce%b3%ce%b9%ce%bf%cf%80%ce%bf%cf%8d/",
        ],
    },
    {
        "local": "Ἱερά Μονή Παναγίας Πανυμνήτου καί Προφήτου Ἠλιοῦ",
        "name": "Panagia Panymnetos and Prophet Elijah Monastery by the Aliakmon",
        "seat": "Aliakmon River, Beroia",
        "address": ["Παρά τόν Ἁλιάκμονα, Τ.Κ. 59100"],
        "rank": "Monastery under Re-establishment",
        "sources": [PATRIARCHATE_PAGE, "https://imverias.gr/iera-moni-profitou-iliou-skitis/"],
    },
]


MONASTIC_CHURCHES = [
    {
        "local": "Παρεκκλήσι του Αγίου Γεωργίου στον Αλιάκμονα",
        "name": "Saint George Monastic Chapel on the Aliakmon",
        "seat": "Aliakmon River, Beroia",
        "address": ["Παρά τόν Ἁλιάκμονα, Τ.Κ. 59100"],
        "rank": "Monastic Chapel",
        "sources": [
            "https://apotomi.gr/",
            "https://apotomi.gr/%ce%bc%ce%bf%ce%bd%ce%b1%cf%83%cf%84%ce%ae%cf%81%ce%b9/%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%ae%cf%83%ce%b9-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%ce%b3%ce%b5%cf%89%cf%81%ce%b3%ce%af%ce%bf%cf%85-%cf%83%cf%84%ce%bf%ce%bd-%ce%b1%ce%bb/",
        ],
    },
    {
        "local": "ναός τοῦ Ἁγίου Γερασίμου",
        "name": "Saint Gerasimos Monastic Church at Panagia Dovra Monastery",
        "seat": "Beroia",
        "address": ["Ι. Μ. Παναγίας Δοβρά, Τ.Θ.241, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastic Church",
        "sources": ["https://imverias.gr/iera-moni-panagias-dovra/"],
    },
    {
        "local": "παρεκκλήσιο πρός τιμήν του",
        "name": "Saint Cosmas of Aetolia Monastic Chapel at Panagia Dovra Monastery",
        "seat": "Beroia",
        "address": ["Ι. Μ. Παναγίας Δοβρά, Τ.Θ.241, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-panagias-dovra/"],
    },
    {
        "local": "ἐκκλησάκι τοῦ Ἁγίου Μεγαλομάρτυρος Μηνᾶ",
        "name": "Great Martyr Menas Monastic Chapel at Panagia Dovra Monastery",
        "seat": "Beroia",
        "address": ["Ι. Μ. Παναγίας Δοβρά, Τ.Θ.241, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-panagias-dovra/"],
    },
    {
        "local": "παρεκκλησίου τῆς Ἁγίας Θεοπρομήτορος Ἄννης",
        "name": "Saint Anna Monastic Chapel at Kallipetra Monastery",
        "seat": "Rachi, Beroia",
        "address": ["Ι.Μ. Θεοτόκου Καλλίπετρας, Τ.Θ. Ράχη, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-kallitetras/"],
    },
    {
        "local": "παρεκκλησίου τοῦ Ὁσίου Ἰωσήφ τοῦ Ἡσυχαστοῦ",
        "name": "Venerable Joseph the Hesychast Monastic Chapel at Kallipetra Monastery",
        "seat": "Rachi, Beroia",
        "address": ["Ι.Μ. Θεοτόκου Καλλίπετρας, Τ.Θ. Ράχη, Τ.Κ. 591 00, Βέροια"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-kallitetras/"],
    },
    {
        "local": "παρεκκλήσιο τῶν Ἀρχαγγέλων",
        "name": "Holy Archangels Monastic Chapel at the Holy Forerunner Monastery in Naoussa",
        "seat": "Naoussa",
        "address": ["Ι.Μ. Τιμίου Προδρόμου Ναούσης, Τ.Κ. 592 00, Νάουσα Ημαθίας"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-timiou-prodromou-naoussis/"],
    },
    {
        "local": "παρεκκλησίου πρός τιμήν τῶν Εἰσοδίων τῆς Ὑπεραγίας Θεοτόκου καί τῶν ἁγίων Νεομαρτύρων τῆς Ναούσης",
        "name": "Entry of the Theotokos and Holy New Martyrs of Naoussa Monastic Chapel",
        "seat": "Naoussa",
        "address": ["Ι.Μ. Τιμίου Προδρόμου Ναούσης, Τ.Κ. 592 00, Νάουσα Ημαθίας"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-timiou-prodromou-naoussis/"],
    },
    {
        "local": "ἐσωτερικοῦ παρεκκλησίου ἀφιερωμένου στήν ἁγία Ὀλυμπιάδα",
        "name": "Saint Olympiada Monastic Chapel at Saint Athanasius of Sphinitsa Monastery",
        "seat": "Agkathia",
        "address": ["Ι. Μ. Αγίου Αθανασίου Σφηνίτσης, Αγκαθιά Ημαθίας, Τ.Κ. 590 31, Μελίκη"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-agiou-athanasiou-sfinitsis/"],
    },
    {
        "local": "παρεκκλήσιο πρός τιμήν τοῦ Ἁγίου μεγαλομάρτυρος καί ἰαματικοῦ Παντελεήμονος",
        "name": "Great Martyr and Healer Panteleimon Monastic Chapel at Saint Athanasius of Sphinitsa Monastery",
        "seat": "Agkathia",
        "address": ["Ι. Μ. Αγίου Αθανασίου Σφηνίτσης, Αγκαθιά Ημαθίας, Τ.Κ. 590 31, Μελίκη"],
        "rank": "Monastic Chapel",
        "sources": ["https://imverias.gr/iera-moni-agiou-athanasiou-sfinitsis/"],
    },
]


SPECIAL_RECORDS = [
    {
        "local": "Πανελλήνιον Ἱερόν Προσκύνημα «Παναγία Σουμελᾶ»",
        "name": "Pan-Hellenic Holy Pilgrimage of Panagia Soumela",
        "seat": "Kastania, Beroia",
        "address": ["Προσκύνημα Παναγίας Σουμελά, Καστανιά Ημαθίας, Τ.Θ. 125 Τ.Κ. 591 00, Βέροια"],
        "rank": "Pilgrimage Church",
        "phones": ["2331088139", "2331088137"],
        "emails": ["info@panagiasoumela.gr", "psumela@otenet.gr"],
        "site": "https://www.panagiasoumela.gr/",
        "sources": [
            PATRIARCHATE_PAGE,
            "https://imverias.gr/iera-moni-panagias-soumela/",
            "https://www.panagiasoumela.gr/",
        ],
    },
    {
        "local": "ἰδιωτικό Ἱερό Ναό τῆς Ἁγίας Τριάδος",
        "name": "Holy Trinity Private Church of the Pelekan Sisterhood",
        "seat": "Komnenio, Beroia",
        "address": ["Αδελφότητα Αγίας Τριάδος Πέλεκαν, Κομνήνιο Ημαθίας, Τ.Κ. 591 00, Βέροια"],
        "rank": "Private Church",
        "phones": ["2331044034", "2331044036"],
        "sources": ["https://imverias.gr/adelfotita-pelekan/"],
    },
]


INSTITUTIONAL_RECORDS = r'''
Beroia|Νοσοκομείο Βεροίας|Ιερός Ναός Αγίου Λουκά|Saint Luke Institutional Church at Beroia Hospital
Naoussa|Νοσοκομείο Ναούσης|Ιερός Ναός Αγίας Τριάδος|Holy Trinity Institutional Church at Naoussa Hospital
Beroia|Γηροκομείο Βεροίας|Ιερός Ναός Υψώσεως του Τιμίου Σταυρού|Exaltation of the Holy Cross Institutional Church at the Beroia Nursing Home
Naoussa|Γηροκομείο Ναούσης|Ιερός Ναός Αγίων Ιωακείμ και Άννης|Saints Joachim and Anna Institutional Church at the Naoussa Nursing Home
Naoussa|Φιλόπτωχος Αδελφότητα Ναούσης|Ιερός Ναός Υπαπαντής του Κυρίου|Presentation of the Lord Institutional Church at the Naoussa Philoptochos Brotherhood
Beroia|Β΄ Σ. Σ. Βέροια|Ιερός Ναός Αγίου Γεωργίου, Β΄ Σ. Σ. Βέροια|Saint George Institutional Church at B Corps in Beroia
Alexandria|3ο Τάγμα Αεροπορίας Στρατού, Αλεξάνδρεια|Ιερός Ναός Προφήτου Ηλιού, 3ου Τάγματος Αεροπορίας Στρατού, Αλεξάνδρεια|Prophet Elijah Institutional Church at the 3rd Army Aviation Battalion in Alexandria
Platy|315 Μονάδα Τεχνικού, Πλατύ|Ιερός Ναός Αγίου Νικολάου, 315 Μονάδα Τεχνικού, Πλατύ|Saint Nicholas Institutional Church at the 315th Technical Unit in Platy
Varvares, Beroia|172 Μ.Π.Π., Βαρβάρες Βεροίας|Ιερός Ναός Αγίας Βαρβάρας, 172 Μ.Π.Π., Βαρβάρες Βεροίας|Saint Barbara Institutional Church at the 172nd MPP in Varvares, Beroia
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if ord(char) < 128)
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (value or "body")[:100].rstrip("-")


def parse_lines(block, count):
    result = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        values = [value.strip() for value in line.split("|")]
        if len(values) != count:
            raise ValueError("invalid Beroia source row: %s" % line)
        result.append(values)
    return result


def make_name(dedication, rank, seat, parent_name=None):
    if rank in {"Cemetery Church", "Country Church"}:
        return "%s %s in %s" % (dedication, rank, seat)
    if rank in {"Chapel", "Shrine", "Historic Monastic Church"}:
        return "%s %s at %s in %s" % (
            dedication, rank, parent_name, seat
        )
    return "%s %s in %s" % (dedication, rank, seat)


def build_rows():
    rows = []
    index = 0
    for group in SOURCE_GROUPS:
        parent_name = None
        parent_seat = None
        parent_address = None
        for raw in group["rows"].splitlines():
            line = raw.strip()
            if not line:
                continue
            values = [value.strip() for value in line.split("|")]
            marker = values[0]
            if marker == "M":
                if len(values) != 7:
                    raise ValueError("invalid main body row: %s" % line)
                _, seat, address_el, local, dedication, rank, phone = values
                name = make_name(dedication, rank, seat)
                parent_name = dedication
                parent_seat = seat
                parent_address = address_el
            elif marker == "C":
                if len(values) != 4:
                    raise ValueError("invalid subordinate body row: %s" % line)
                if parent_name is None:
                    raise ValueError("orphan chapel in %s" % group["key"])
                _, local, dedication, rank = values
                seat = parent_seat
                address_el = parent_address
                phone = ""
                name = make_name(dedication, rank, seat, parent_name)
            else:
                raise ValueError("unknown Beroia record marker %s" % marker)
            index += 1
            kind = "monastery" if "Monastic" in rank else "parish"
            item = {
                "id": "gr-ep-beroia-%03d-%s" % (index, slug(name)),
                "parent": PARENT,
                "kind": kind,
                "rank": rank,
                "name": name,
                "local": local,
                "seat": seat,
                "country": "GR",
                "address": [address_el],
                "sources": [group["url"]],
                "source_modified": group["modified"],
            }
            if phone:
                item["phones"] = [phone]
                item["contact_sources"] = [group["url"]]
                item["contact_checked"] = CHECKED
            rows.append(item)

    for record in MONASTIC_RECORDS + MONASTIC_CHURCHES:
        index += 1
        item = {
            "id": "gr-ep-beroia-%03d-%s" % (index, slug(record["name"])),
            "parent": PARENT,
            "kind": "monastery",
            "rank": record["rank"],
            "name": record["name"],
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "sources": list(record["sources"]),
        }
        for key in ("phones", "emails", "site"):
            if record.get(key):
                item[key] = (
                    list(record[key]) if isinstance(record[key], list)
                    else record[key]
                )
        if any(item.get(key) for key in ("phones", "emails")):
            item["contact_sources"] = list(record["sources"])
            item["contact_checked"] = CHECKED
        rows.append(item)

    for record in SPECIAL_RECORDS:
        index += 1
        item = {
            "id": "gr-ep-beroia-%03d-%s" % (index, slug(record["name"])),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": record["name"],
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "sources": list(record["sources"]),
        }
        for key in ("phones", "emails", "site"):
            if record.get(key):
                item[key] = (
                    list(record[key]) if isinstance(record[key], list)
                    else record[key]
                )
        if any(item.get(key) for key in ("phones", "emails")):
            item["contact_sources"] = list(record["sources"])
            item["contact_checked"] = CHECKED
        rows.append(item)

    for seat, address_el, local, name in parse_lines(
            INSTITUTIONAL_RECORDS, 4):
        index += 1
        rows.append({
            "id": "gr-ep-beroia-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Institutional Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address_el],
            "sources": [INSTITUTIONAL_PAGE],
            "source_modified": "2026-10-06T20:30:20",
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 362
EXPECTED_OWNER_COUNTS = {PARENT: 362}
EXPECTED_KINDS = {"monastery": 22, "parish": 340}
EXPECTED_RANKS = {
    "Cemetery Church": 24,
    "Chapel": 183,
    "Country Church": 8,
    "Historic Monastic Church": 1,
    "Institutional Church": 9,
    "Metropolitan Cathedral": 3,
    "Monastery": 8,
    "Monastery under Re-establishment": 3,
    "Monastic Chapel": 9,
    "Monastic Church": 1,
    "Parish Church": 108,
    "Pilgrimage Church": 2,
    "Private Church": 1,
    "Shrine": 2,
}
EXPECTED_CONTACT_BODIES = 73
EXPECTED_PHONE_BODIES = 71
EXPECTED_PHONE_VALUES = 74
EXPECTED_EMAIL_BODIES = 3
EXPECTED_EMAIL_VALUES = 4
EXPECTED_SITE_BODIES = 5
EXPECTED_ADDRESS_BODIES = 362
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


COMPETENT_HOSTS = {
    "apotomi.gr",
    "ec-patr.org",
    "imkallipetras.gr",
    "improdromounaousas.gr",
    "imverias.gr",
    "moutsiali.gr",
    "panagiasoumela.gr",
    "www.apotomi.gr",
    "www.imkallipetras.gr",
    "www.improdromounaousas.gr",
    "www.imverias.gr",
    "www.moutsiali.gr",
    "www.panagiasoumela.gr",
}


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
        source_hosts = {urlparse(value).netloc.removeprefix("www.")
                        for value in sources}
        site_host = urlparse(item["site"]).netloc.removeprefix("www.")
        if site_host not in source_hosts:
            raise ValueError("%s body-owned site lacks provenance"
                             % item.get("id"))
    return item


def validate_rows():
    cleaned = [clean(row) for row in ROWS]
    if len(cleaned) != EXPECTED_TOTAL:
        raise ValueError("Beroia total drifted: %d" % len(cleaned))
    ids = [row["id"] for row in cleaned]
    if len(ids) != len(set(ids)):
        raise ValueError("Beroia ids collide")
    for row in cleaned:
        row_id = row["id"]
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("invalid id: %s" % row_id)
        if row.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has an unknown parent" % row_id)
        if row.get("country") != "GR":
            raise ValueError("%s has the wrong country" % row_id)
        for field in ("name", "local", "rank", "seat"):
            if not row.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        if row.get("checked") != CHECKED:
            raise ValueError("%s carries an unexpected checked date" % row_id)
        if row.get("address") in (None, [], [""]):
            raise ValueError("%s lacks an official locality or address" % row_id)
        for email in row.get("emails") or []:
            if not EMAIL_RE.fullmatch(email):
                raise ValueError("%s has invalid email %s" % (row_id, email))
        for phone in row.get("phones") or []:
            if not re.fullmatch(r"[0-9]+", phone):
                raise ValueError("%s has invalid phone %s" % (row_id, phone))
        for value in walk_strings(row):
            if FORBIDDEN_PUNCTUATION.search(value):
                raise ValueError("%s carries forbidden punctuation" % row_id)
    owner_counts = Counter(row["parent"] for row in cleaned)
    kind_counts = Counter(row["kind"] for row in cleaned)
    rank_counts = Counter(row["rank"] for row in cleaned)
    if dict(owner_counts) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Beroia owner counts drifted")
    if dict(kind_counts) != EXPECTED_KINDS:
        raise ValueError("Beroia kind counts drifted")
    if dict(rank_counts) != EXPECTED_RANKS:
        raise ValueError("Beroia rank counts drifted")
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
        raise ValueError("Beroia contact metrics drifted: %r" % metrics)
    identity_keys = [
        (unicase(row["name"]), unicase(row["seat"])) for row in cleaned
    ]
    if len(identity_keys) != len(set(identity_keys)):
        raise ValueError("Beroia English identities collide")
    if set(ENGLISH_NAMES) != set(ids):
        raise ValueError("Beroia English-name coverage drifted")
    return cleaned


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Beroia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Beroia candidate ledger date drifted")
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
        raise ValueError("Beroia ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Beroia ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Beroia ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Beroia ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Beroia ledger has duplicate candidate ids")
    for value in walk_strings(ledger):
        if FORBIDDEN_PUNCTUATION.search(value):
            raise ValueError("Beroia ledger carries forbidden punctuation")
    return ledger


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
    urls = {PATRIARCHATE_PAGE, INSTITUTIONAL_PAGE}
    for group in SOURCE_GROUPS:
        urls.add(group["url"])
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
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = value.replace("\u00a0", " ")
    value = re.sub(
        r"(?<=[\u0370-\u03ff\u1f00-\u1fff])-\s+"
        r"(?=[\u0370-\u03ff\u1f00-\u1fff])",
        "",
        value,
    )
    value = unicodedata.normalize("NFC", value)
    return re.sub(r"\s+", " ", value).strip().casefold()


def check_live_sources():
    failures = []
    source_texts = {}
    for url in all_source_urls():
        try:
            request = Request(url, headers={
                "User-Agent": "Mozilla/5.0 Plithos directory source audit",
            })
            with urlopen(request, timeout=30) as response:
                if response.status >= 400:
                    failures.append((url, "HTTP %s" % response.status))
                    continue
                content_type = response.headers.get("Content-Type", "").lower()
                if "html" not in content_type:
                    failures.append((url, "unexpected content type %s" % content_type))
                    continue
                source_texts[url] = normalize_source_text(
                    response.read().decode("utf-8", "replace")
                )
        except Exception as exc:
            failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join("%s [%s]" % pair for pair in failures)
        raise ValueError("live Beroia source check failed: %s" % rendered)
    exact_failures = []
    for row in ROWS:
        local = normalize_source_text(row["local"])
        if not any(local in source_texts.get(url, "")
                   for url in row["sources"]):
            exact_failures.append((row["id"], row["local"]))
    if exact_failures:
        raise ValueError(
            "live Beroia exact-local-name check failed: %r"
            % exact_failures
        )
    modified_failures = []
    for group in SOURCE_GROUPS:
        slug_value = urlparse(group["url"]).path.strip("/")
        api_url = (
            "https://imverias.gr/wp-json/wp/v2/posts?slug="
            + quote(slug_value)
        )
        try:
            request = Request(api_url, headers={
                "User-Agent": "Mozilla/5.0 Plithos directory source audit",
            })
            with urlopen(request, timeout=30) as response:
                payload = json.load(response)
            observed = payload[0].get("modified") if payload else None
            if observed != group["modified"]:
                modified_failures.append(
                    (group["key"], group["modified"], observed)
                )
        except Exception as exc:
            modified_failures.append(
                (group["key"], group["modified"], str(exc))
            )
    if modified_failures:
        raise ValueError(
            "live Beroia regional modified-date check failed: %r"
            % modified_failures
        )


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
    sys.exit(main())
