#!/usr/bin/env python3
"""Validate exact current Karpenision bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_karpenision_country.py --check
    python tools/directory_karpenision_country.py --check-live
    python tools/directory_karpenision_country.py --dump
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
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "karpenision_country.json"
)
PARENT = "gr-karpenision"
METROPOLIS_HOME = "https://imkarpenisiou.gr/cms/"
ROSTER_PAGE = (
    "https://imkarpenisiou.gr/cms/"
    "%CE%B9%CE%B5%CF%81%CE%B5%CE%B9%CF%83-"
    "%CF%84%CE%B7%CE%BB%CE%B5%CF%86%CF%89%CE%BD%CE%B1/"
)
ACTIVE_MONASTERIES_PAGE = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%bc%ce%bf%ce%bd%ce%b1%cf%83%cf%84%ce%ae%cf%81%ce%b9%ce%b1-"
    "%ce%b5%ce%bd%ce%b5%cf%81%ce%b3%ce%b5%ce%af%ce%b1/"
)
FORMER_MONASTERIES_PAGE = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%bc%ce%bf%ce%bd%ce%b1%cf%83%cf%84%ce%ae%cf%81%ce%b9%ce%b1-"
    "%ce%b5%ce%bd%ce%b5%cf%81%ce%b3%ce%b5%ce%af%ce%b1-2/"
)
PILGRIMAGE_MAP_PAGE = (
    "https://imkarpenisiou.gr/cms/"
    "%cf%80%cf%81%ce%bf%cf%83%ce%ba%cf%85%ce%bd%ce%b7%ce%bc%ce%b1%"
    "cf%84%ce%b9%ce%ba%cf%8c%cf%82-%cf%87%ce%ac%cf%81%cf%84%ce%b7%"
    "cf%82/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/karpenesiou"
)
LEGAL_PAGE = (
    "https://www.e-nomothesia.gr/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-ekklesias-738-854-2019.html"
)
LEGAL_PDF = (
    "https://ia37rg02wpsa01.blob.core.windows.net/fek/02/2019/"
    "20190202148.pdf"
)

CATHEDRAL_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%cf%83%cf%85%ce%bd%cf%84%ce%b7%cf%81%ce%b7%cf%83%ce%b7-"
    "%cf%84%ce%bf%ce%b9%cf%87%ce%bf%ce%b3%cf%81%ce%b1%cf%86%ce%b9%"
    "cf%89%ce%bd-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%"
    "ce%b9%cf%84%ce%b9%ce%ba/"
)
CEMETERY_ARCHANGEL_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%cf%80%cf%81%ce%bf%ce%b3%cf%81%ce%b1%ce%bc%ce%bc%ce%b1-"
    "%ce%bb%ce%b5%ce%b9%cf%84%ce%bf%cf%85%cf%81%ce%b3%ce%b9%ce%b1%"
    "cf%83-%ce%ba%ce%bf%ce%b9%ce%bc%ce%b7%cf%84%ce%b7%cf%81%ce%b9%"
    "ce%b1%ce%ba%ce%bf%cf%85/"
)
IAKOVOS_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%b5%ce%b3%ce%ba%ce%b1%ce%af%ce%bd%ce%b9%ce%b1-"
    "%ce%b9%ce%b5%cf%81%ce%bf%cf%8d-%ce%bd%ce%b1%ce%bf%cf%8d-"
    "%ce%bf%cf%83%ce%af%ce%bf%cf%85-%ce%b9%ce%b1%ce%ba%cf%8e%ce%b2%"
    "ce%bf%cf%85/"
)
NICHOLAS_KARPENISIOT_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%b5%ce%bf%cf%81%cf%84%ce%b7-"
    "%cf%80%ce%bf%ce%bb%ce%b9%ce%bf%cf%85%cf%87%ce%bf%cf%85-"
    "%cf%80%ce%bf%ce%bb%ce%b5%cf%89%cf%83-"
    "%ce%ba%ce%b1%cf%81%cf%80%ce%b5%ce%bd%ce%b7%cf%83%ce%b9%ce%bf%"
    "cf%85/"
)
OLD_CEMETERY_GEORGE_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%bf%ce%bd%ce%bf%ce%bc%ce%b1%cf%83%cf%84%ce%b7%cf%81%ce%b9%"
    "ce%b1-%cf%83%ce%b5%ce%b2%ce%b1%cf%83%ce%bc%ce%b9%cf%89%cf%84%"
    "ce%b1%cf%84%ce%bf%cf%85-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%"
    "ce%bf%ce%bb-2/"
)
SABBAS_CHAPEL_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%b9%ce%b5%cf%81%ce%b1-"
    "%ce%b1%ce%b3%cf%81%cf%85%cf%80%ce%bd%ce%b9%ce%b1-"
    "%ce%b3%ce%b9%ce%b1-%cf%84%ce%b7%ce%bd-"
    "%ce%b5%ce%bf%cf%81%cf%84%ce%b7-%cf%84%ce%bf%cf%85-"
    "%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%83/"
)
KOUMASIA_POST = (
    "https://imkarpenisiou.gr/cms/"
    "%ce%b1%cf%81%cf%87%ce%b9%ce%b5%cf%81%ce%b1%cf%84%ce%b9%ce%ba%"
    "ce%b7-%ce%b8%ce%b5%ce%b9%ce%b1-"
    "%ce%bb%ce%b5%ce%b9%cf%84%ce%bf%cf%85%cf%81%ce%b3%ce%b9%ce%b1-"
    "%cf%84%ce%bf-%cf%83%ce%b1%ce%b2%ce%b2%ce%b1/"
)


# English seat | English dedication | current Greek seat |
# current Greek dedication | current body-associated phones
#
# The official Gazette carries 97 exact parish rows. The current first-party
# roster carries 96 of them and omits Roska. It supplies the phones retained
# below. The current roster also gives Holy Trinity for the Domianoi parish,
# which supersedes the older Dormition dedication in the Gazette roster.
PARISH_ROWS = r'''
Karpenisi|Holy Trinity|ΚΑΡΠΕΝΗΣΙ|ΑΓΙΑ ΤΡΙΑΣ|6946824740,6975605186,2237022215
Karpenisi|Nativity of the Theotokos|ΚΑΡΠΕΝΗΣΙ|ΓΕΝΝΗΣΙΣ ΘΕΟΤΟΚΟΥ|6974555689,2237025387
Karpenisi|Prophet Elijah|ΚΑΡΠΕΝΗΣΙ|ΠΡΟΦΗΤΗΣ ΗΛΙΑΣ|6984756296,2237024491
Karpenisi|Saint Paraskevi|ΚΑΡΠΕΝΗΣΙ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6974114208,2237080206
Karpenisi|Saints of Evrytania|ΚΑΡΠΕΝΗΣΙ|ΕΥΡΥΤΑΝΩΝ ΑΓΙΩΝ|6974466853,2237024688
Agia Triada|Holy Trinity|ΑΓΙΑ ΤΡΙΑΔΑ|ΑΓΙΑ ΤΡΙΑΣ|
Agios Charalambos|Saint Charalambos|ΑΓΙΟΣ ΧΑΡΑΛΑΜΠΟΣ|ΑΓΙΟΣ ΧΑΡΑΛΑΜΠΟΣ|2237096096
Agios Dimitrios|Saint Demetrius|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|
Agios Nikolaos|Saint Nicholas|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6978778616,2237021087
Agrafa|Saint Demetrius|ΑΓΡΑΦΑ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6981618894,2237023040
Alestia-Ftelia|Dormition of the Theotokos|ΑΛΕΣΤΙΑ-ΦΤΕΛΙΑ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|
Ampliani|Saint Paraskevi|ΑΜΠΛΙΑΝΗ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|
Anatoliki Fragkista|Holy Apostles|ΑΝΑΤΟΛΙΚΗ ΦΡΑΓΚΙΣΤΑ|ΑΓΙΟΙ ΑΠΟΣΤΟΛΟΙ|
Aniada|Saint Nicholas|ΑΝΙΑΔΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6942527865
Ano Raptopoulo|Saint Paraskevi|ΑΝΩ ΡΑΠΤΟΠΟΥΛΟΝ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|
Aspropyrgos|Saint Nicholas|ΑΣΠΡΟΠΥΡΓΟΣ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|2237021297,2237080763
Valaora|Dormition of the Theotokos|ΒΑΛΑΩΡΑ|ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|6978888837
Velota|Saint Barbara|ΒΕΛΩΤΑ|ΑΓΙΑ ΒΑΡΒΑΡΑ|
Viniani|Holy Apostles|ΒΙΝΙΑΝΗ|ΑΓΙΟΙ ΑΠΟΣΤΟΛΟΙ|6978404797,2237031306
Voulpi|Dormition of the Theotokos|ΒΟΥΛΠΗ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|6994349096
Voutyro|Saint Paraskevi|ΒΟΥΤΥΡΟΝ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6978374838,2237025954
Vrangiana|Saint George|ΒΡΑΓΓΙΑΝΑ|ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|6977820734
Vracha|Saint Nicholas|ΒΡΑΧΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6971816040
Gorianades|Holy Trinity|ΓΟΡΙΑΝΑΔΕΣ|ΑΓΙΑ ΤΡΙΑΣ|6977590511,2237080667
Granitsa|New Martyr Michael|ΓΡΑΝΙΤΣΑ|ΝΕΟΜΑΡΤΥΣ ΜΙΧΑΗΛ|6906632503
Dafni|Transfiguration of the Savior|ΔΑΦΝΗ|ΜΕΤΑΜΟΡΦΩΣΙΣ ΣΩΤΗΡΟΣ|6934929015
Dafnoula|Saint Demetrius|ΔΑΦΝΟΥΛΑ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6970879500,2237061696
Domianoi|Holy Trinity|ΔΟΜΙΑΝΟΙ|ΑΓΙΑ ΤΡΙΑΣ|2237096096
Domnista|Saint Athanasius|ΔΟΜΝΙΣΤΑ|ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|6983300401
Dytiki Fragkista|Nativity of the Theotokos|ΔΥΤ.ΦΡΑΓΚΙΣΤΑ|ΓΕΝΝΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|6974060595
Epiniana|Saint George|ΕΠΑΙΝΙΑΝΑ|ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|
Episkopi|Dormition of the Theotokos|ΕΠΙΣΚΟΠΗ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|6975726763
Esochoria|Dormition of the Theotokos|ΕΣΩΧΩΡΙΑ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|
Itea|Saint Paraskevi|ΙΤΕΑ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6972869530,2237061510
Kalesmeno|Conception of Saint John the Forerunner|ΚΑΛΕΣΜΕΝΟΝ|ΣΥΛΛ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|6974466874,2237024628
Karytsa|Saint Demetrius|ΚΑΡΥΤΣΑ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6974541546,2237041241
Kastanea|Saint Nicholas|ΚΑΣΤΑΝΕΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6942527865
Kastanoula|Saint Barbara|ΚΑΣΤΑΝΟΥΛΑ|ΑΓΙΑ ΒΑΡΒΑΡΑ|
Katavothra|Saint Demetrius|ΚΑΤΑΒΟΘΡΑ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|
Kato Raptopoulo|Dormition of the Theotokos|ΚΑΤΩ ΡΑΠΤΟΠΟΥΛΟΝ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|6974895399,6972591038
Kato Potamia|Saint Nicholas|ΚΑΤΩ ΠΟΤΑΜΙΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6970207607,2237061064
Kedra|Nativity of Christ|ΚΕΔΡΑ|ΓΕΝΝΗΣΙΣ ΤΟΥ ΧΡΙΣΤΟΥ|6981653051,2237097167
Kerasochori|Saint Paraskevi|ΚΕΡΑΣΟΧΩΡΙΟΝ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6978404797,2237031306
Klavsi|Saint Demetrius|ΚΛΑΥΣΕΙΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6982942046
Koritsa|Saint Nicholas|ΚΟΡΙΤΣΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|
Koryschades|Saint Athanasius|ΚΟΡΥΣΧΑΔΕΣ|ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|2237021297,2237080763
Krenti|Conception of Saint John the Forerunner|ΚΡΕΝΤΗ|ΣΥΛΛ.ΠΡΟΔΡΟΜΟΥ|
Krikello|Saint Nicholas|ΚΡΙΚΕΛΛΟΝ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6943149460
Lepiana|Holy Unmercenaries|ΛΕΠΙΑΝΑ|ΑΓΙΟΙ ΑΝΑΡΓΥΡΟΙ|6907217986
Limeri|Saint Barbara|ΛΗΜΕΡΙΟΝ|ΑΓΙΑ ΒΑΡΒΑΡΑ|6907217986
Lithochori|Saint Demetrius|ΛΙΘΟΧΩΡΙΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6976285947
Longitsi|Nativity of the Theotokos|ΛΟΓΓΙΤΣΙΟΝ|ΓΕΝΕΣΙΟΝ ΘΕΟΤΟΚΟΥ|6989868648,2641098440
Marathea|Saint Athanasius|ΜΑΡΑΘΕΑ|ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|6974466874,2237024628
Marathos|Holy Archangels|ΜΑΡΑΘΟΣ|ΑΓΙΟΙ ΤΑΞΙΑΡΧΑΙ|6978404797,2237031306
Mavrommata|Dormition of the Theotokos|ΜΑΥΡΟΜΜΑΤΑ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|
Megalo Chorio|Saint Paraskevi|ΜΕΓΑΛΟ ΧΩΡΙΟΝ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6974541546,2237041241
Mesokomi|Dormition of the Theotokos|ΜΕΣΟΚΩΜΗ|ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|6983300401
Mesochori|Holy Archangels|ΜΕΣΟΧΩΡΙΟΝ|ΑΓΙΟΙ ΤΑΞΙΑΡΧΑΙ|6971816040
Mikro Chorio|Transfiguration of the Savior|ΜΙΚΡΟ ΧΩΡΙΟΝ|ΜΕΤΑΜ.ΣΩΤΗΡΟΣ|6985696867
Monastiraki|Saint Demetrius|ΜΟΝΑΣΤΗΡΑΚΙΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6973066922,2231062137
Mouzilo|Dormition of the Theotokos|ΜΟΥΖΗΛΟΝ|ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|6978374838,2237025954
Myriki-Kallithea|Saint George|ΜΥΡΙΚΗ-ΚΑΛΛΙΘΕΑ|ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|6982942046
Neo Argyri|Holy Unmercenaries|ΝΕΟΝ ΑΡΓΥΡΙΟΝ|ΑΓΙΟΙ ΑΝΑΡΓΥΡΟΙ|6972153598,2237061740
Nostimo|Transfiguration of the Savior|ΝΟΣΤΙΜΟΝ|ΜΕΤΑΜΟΡΦΩΣΙΣ ΣΩΤΗΡΟΣ|6976524200
Palaiokatouna|Dormition of the Theotokos|ΠΑΛΑΙΟΚΑΤΟΥΝΑ|ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|6972312887
Palaiochori|Saint Demetrius|ΠΑΛΑΙΟΧΩΡΙΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6989868648,2641098440
Paparousi|Saint Paraskevi|ΠΑΠΑΡΟΥΣΙΟΝ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6973066922,2231062137
Pavlopoulo|Saint Demetrius|ΠΑΥΛΟΠΟΥΛΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6979711101,2237021093
Petralona|Holy Trinity|ΠΕΤΡΑΛΩΝΑ|ΑΓΙΑ ΤΡΙΑΣ|2237096096
Platanos|Saint Nicholas|ΠΛΑΤΑΝΟΣ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|
Prasia|Transfiguration of the Savior|ΠΡΑΣΙΑ|ΜΕΤΑΜΟΡΦΩΣΙΣ ΣΩΤΗΡΟΣ|6972591038
Prodromos|Saint John the Forerunner|ΠΡΟΔΡΟΜΟΣ|ΑΓΙΟΣ ΙΩΑΝ. ΠΡΟΔΡΟΜΟΣ|
Proussos|Saint Nicholas|ΠΡΟΥΣΟΣ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|2237021297,2237080763
Roska|Saint Paraskevi|ΡΩΣΚΑ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|
Sella|Holy Apostles Peter and Paul|ΣΕΛΛΑ|ΑΓΙΟΙ ΑΠ.ΠΕΤΡΟΣ-ΠΑΥΛΟΣ|6907551962
Sivista|Saint Marina|ΣΙΒΙΣΤΑ|ΑΓΙΑ ΜΑΡΙΝΑ|6978516841,2237095736
Skopia|Saint Nicholas|ΣΚΟΠΙΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6979605834
Stavloi|Saint Nicholas|ΣΤΑΥΛΟΙ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6906632503
Stenoma|Saint Paraskevi|ΣΤΕΝΩΜΑ|ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|6979711101,2237021093
Stavrochori|Saint Nicholas|ΣΤΑΥΡΟΧΩΡΙΟΝ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|
Stefanio|Dormition of the Theotokos|ΣΤΕΦΑΝΙΟΝ|ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|
Stournara|Saint Athanasius|ΣΤΟΥΡΝΑΡΑ|ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|
Syngkrelo|Saint Nicholas|ΣΥΓΚΡΕΛΟΝ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6978374838,2237025954
Topoliana|Saint George|ΤΟΠΟΛΙΑΝΑ|ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|6975794880
Tornos|Holy Trinity|ΤΟΡΝΟΣ|ΑΓΙΑ ΤΡΙΑΣ|
Tridendro|Saint Demetrius|ΤΡΙΔΕΝΔΡΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|
Tripotamos|Saint Demetrius|ΤΡΙΠΟΤΑΜΟΣ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6907551962
Trovato|Saint Demetrius|ΤΡΟΒΑΤΟΝ|ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|6978535338
Tsouka Palaiokatouna|Saint Constantine|ΤΣΟΥΚΑ ΠΑΛ/ΝΑΣ|ΑΓΙΟΣ ΚΩΝΣΤΑΝΤΙΝΟΣ|
Feidakia|Nativity of the Theotokos|ΦΕΙΔΑΚΙΑ|ΓΕΝΝΕΣΕΩΣ ΘΕΟΤΟΚΟΥ|6975726763
Fourna|Transfiguration of the Savior|ΦΟΥΡΝΑΣ|ΜΕΤΑΜΟΡΦΩΣΙΣ ΣΩΤΗΡΟΣ|6977365044
Fousiana|Dormition of the Theotokos|ΦΟΥΣΙΑΝΑ|ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|6976285947,2237097326
Chelidona-Agia Vlacherna|Saint George|ΧΕΛΙΔΟΝΑ-ΑΓ.ΒΛΑΧΕΡΝΑ|ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|6974541546,2237041241
Chochlia|Saint Nicholas|ΧΟΧΛΙΑ|ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|6980004492,2237096096
Chrysova|Saint Constantine|ΧΡΥΣΟΒΑ|ΑΓΙΟΣ ΚΩΝΣΤΑΝΤΙΝΟΣ|6978516841,2237095736
Chryso|Dormition of the Theotokos|ΧΡΥΣΩ|ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ|6979870474
Psiana|Nativity of the Theotokos|ΨΙΑΝΑ|ΓΕΝΕΣΕΩΣ ΘΕΟΤΟΚΟΥ|6974541546,2237041241
'''


# English seat | English dedication | Greek seat | Greek local name | rank |
# phones | body detail page | identity/contact source
MONASTIC_ROWS = r'''
Domianoi|Dormition of the Theotokos|Δομιανοί|Ιερά Μονή Κοιμήσεως της Θεοτόκου Δομιανών|Monastery||https://imkarpenisiou.gr/cms/koimdomianoi/|https://imkarpenisiou.gr/cms/koimdomianoi/
Proussos|Panagia Prousiotissa|Προυσός|Ιερά Μονή Παναγίας Προυσιώτισσας|Monastery|6946866770,6949110350,2237080705|https://imkarpenisiou.gr/cms/braxa-2/|https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/karpenesiou
Vracha|Transfiguration of the Savior|Βράχα|Ιερά Μονή Μεταμορφώσεως του Σωτήρος Βράχας|Monastery||https://imkarpenisiou.gr/cms/braxa/|https://imkarpenisiou.gr/cms/braxa/
Tatarnis|Panagia Tatarnis|Τατάρνη|Ιερά Πατριαρχική και Σταυροπηγιακή Μονή Παναγίας Τατάρνης|Monastery|6970093838,6979605834,2237095400|https://imkarpenisiou.gr/cms/pantarn/|https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/karpenesiou
Epiniana|Nativity of the Theotokos|Επινιανά|Ιερά Μονή Γεννήσεως της Θεοτόκου Στάνας Επινιανών|Monastery||https://imkarpenisiou.gr/cms/braxa-2-2-2-2/|https://imkarpenisiou.gr/cms/braxa-2-2-2-2/
Neo Mikro Chorio|Venerable Mary of Egypt|Νέο Μικρό Χωριό|Μετόχι Οσίας Μαρίας της Αιγυπτίας Ιεράς Μονής Τατάρνης|Metochion|2237041322|https://imkarpenisiou.gr/cms/braxa-2-2-2/|https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/karpenesiou
Karpenisi|Saint Nectarios|Καρπενήσι|Μετόχι Αγίου Νεκταρίου Ιεράς Μονής Τατάρνης|Metochion|2237022979,2237022621|https://imkarpenisiou.gr/cms/braxa-2-2/|https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/karpenesiou
Tripotamos|Saint Sabbas|Τριπόταμος|Ιερό Κάθισμα Αγίου Σάββα Τριποτάμου|Monastic Dependency|||https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/karpenesiou
Koumasia|Panagia Koumasion|Κουμάσια|Μετόχι Παναγίας Κουμασίων Ιεράς Μονής Προυσού|Metochion|||https://imkarpenisiou.gr/cms/%ce%b1%cf%81%cf%87%ce%b9%ce%b5%cf%81%ce%b1%cf%84%ce%b9%ce%ba%ce%b7-%ce%b8%ce%b5%ce%b9%ce%b1-%ce%bb%ce%b5%ce%b9%cf%84%ce%bf%cf%85%cf%81%ce%b3%ce%b9%ce%b1-%cf%84%ce%bf-%cf%83%ce%b1%ce%b2%ce%b2%ce%b1/
'''


# English seat | English dedication | Greek seat | Greek local name | rank |
# phones | current first-party post
OTHER_CURRENT_ROWS = r'''
Karpenisi|Archangel Michael|Καρπενήσι|Κοιμητηριακός Ιερός Ναός Αρχαγγέλου Μιχαήλ Καρπενησίου|Cemetery Church|6972267840|https://imkarpenisiou.gr/cms/%cf%80%cf%81%ce%bf%ce%b3%cf%81%ce%b1%ce%bc%ce%bc%ce%b1-%ce%bb%ce%b5%ce%b9%cf%84%ce%bf%cf%85%cf%81%ce%b3%ce%b9%ce%b1%cf%83-%ce%ba%ce%bf%ce%b9%ce%bc%ce%b7%cf%84%ce%b7%cf%81%ce%b9%ce%b1%ce%ba%ce%bf%cf%85/
Karpenisi Episcopal Residence|Venerable Iakovos Tsalikis|Επισκοπείο Καρπενησίου|Μητροπολιτικό Παρεκκλήσιο Οσίου Ιακώβου του Τσαλίκη|Metropolitan Chapel||https://imkarpenisiou.gr/cms/%ce%b5%ce%b3%ce%ba%ce%b1%ce%af%ce%bd%ce%b9%ce%b1-%ce%b9%ce%b5%cf%81%ce%bf%cf%8d-%ce%bd%ce%b1%ce%bf%cf%8d-%ce%bf%cf%83%ce%af%ce%bf%cf%85-%ce%b9%ce%b1%ce%ba%cf%8e%ce%b2%ce%bf%cf%85/
Karpenisi|Saint Nicholas the Karpenisiot|Καρπενήσι|Παρεκκλήσιο Αγίου Νικολάου του Καρπενησιώτου|Chapel||https://imkarpenisiou.gr/cms/%ce%b5%ce%bf%cf%81%cf%84%ce%b7-%cf%80%ce%bf%ce%bb%ce%b9%ce%bf%cf%85%cf%87%ce%bf%cf%85-%cf%80%ce%bf%ce%bb%ce%b5%cf%89%cf%83-%ce%ba%ce%b1%cf%81%cf%80%ce%b5%ce%bd%ce%b7%cf%83%ce%b9%ce%bf%cf%85/
Karpenisi Old Cemetery|Saint George|Παλαιό Κοιμητήριο Καρπενησίου|Ιερός Ναός Αγίου Γεωργίου στο παλαιό κοιμητήριο Καρπενησίου|Cemetery Church||https://imkarpenisiou.gr/cms/%ce%bf%ce%bd%ce%bf%ce%bc%ce%b1%cf%83%cf%84%ce%b7%cf%81%ce%b9%ce%b1-%cf%83%ce%b5%ce%b2%ce%b1%cf%83%ce%bc%ce%b9%cf%89%cf%84%ce%b1%cf%84%ce%bf%cf%85-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb-2/
Karpenisi|Saint Sabbas the Sanctified|Καρπενήσι|Παρεκκλήσιο Αγίου Σάββα του Ηγιασμένου|Chapel||https://imkarpenisiou.gr/cms/%ce%b9%ce%b5%cf%81%ce%b1-%ce%b1%ce%b3%cf%81%cf%85%cf%80%ce%bd%ce%b9%ce%b1-%ce%b3%ce%b9%ce%b1-%cf%84%ce%b7%ce%bd-%ce%b5%ce%bf%cf%81%cf%84%ce%b7-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%83/
'''


def parse_table(raw, width, label):
    rows = []
    for line_number, line in enumerate(raw.strip().splitlines(), 1):
        fields = [value.strip() for value in line.split("|")]
        if len(fields) != width:
            raise ValueError(
                "%s row %d has %d fields" % (label, line_number, len(fields))
            )
        rows.append(tuple(fields))
    return rows


def unicase(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"[^a-z0-9α-ω]+", "", value.casefold())


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if ord(char) < 128)
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "body"


def phone(value):
    digits = "".join(re.findall(r"\d", value))
    if len(digits) != 10:
        raise ValueError("invalid Greek phone %s" % value)
    return "+30-" + digits


def make_name(dedication, rank, seat):
    return "%s %s at %s" % (dedication, rank, seat)


PARISH_PARSED = parse_table(PARISH_ROWS, 5, "parish")
MONASTIC_PARSED = parse_table(MONASTIC_ROWS, 8, "monastic")
OTHER_PARSED = parse_table(OTHER_CURRENT_ROWS, 7, "other current body")


def build_rows():
    rows = []
    if len(PARISH_PARSED) != 97:
        raise ValueError("official legal parish source must have 97 rows")
    for seat, dedication, seat_local, dedication_local, raw_phones in \
            PARISH_PARSED:
        rank = "Cathedral" if (
            seat == "Karpenisi" and dedication == "Holy Trinity"
        ) else "Parish Church"
        name = make_name(dedication, rank, seat)
        sources = [ROSTER_PAGE, LEGAL_PAGE, LEGAL_PDF]
        if seat == "Roska":
            sources = [LEGAL_PAGE, LEGAL_PDF]
        if rank == "Cathedral":
            sources = [ROSTER_PAGE, LEGAL_PDF, CATHEDRAL_POST]
        item = {
            "id": "gr-karpenision-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s %s %s" % (
                "Μητροπολιτικός Ιερός Ναός" if rank == "Cathedral"
                else "Ιερός Ναός",
                dedication_local,
                seat_local,
            ),
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "sources": sources,
        }
        if raw_phones:
            item["phones"] = [phone(value) for value in raw_phones.split(",")]
            item["contact_sources"] = [ROSTER_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)

    for fields in MONASTIC_PARSED:
        (seat, dedication, seat_local, local, rank, raw_phones, site,
         identity_source) = fields
        name = make_name(dedication, rank, seat)
        if seat in {"Proussos", "Tatarnis"}:
            sources = [site, ROSTER_PAGE, CHURCH_OF_GREECE_PAGE]
        else:
            sources = [identity_source]
            if site and site not in sources:
                sources.insert(0, site)
            if rank in {"Monastery", "Metochion"} and \
                    ACTIVE_MONASTERIES_PAGE not in sources and \
                    len(sources) < 3:
                sources.append(ACTIVE_MONASTERIES_PAGE)
        item = {
            "id": "gr-karpenision-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "sources": sources,
        }
        if site:
            item["site"] = site
        if raw_phones:
            item["phones"] = [phone(value) for value in raw_phones.split(",")]
            contact_sources = []
            if seat in {"Proussos", "Tatarnis"}:
                contact_sources.extend([ROSTER_PAGE, CHURCH_OF_GREECE_PAGE])
            else:
                contact_sources.append(CHURCH_OF_GREECE_PAGE)
            item["contact_sources"] = contact_sources
            for contact_source in contact_sources:
                if contact_source not in item["sources"]:
                    if len(item["sources"]) >= 3:
                        raise ValueError("too many identity sources for %s" % name)
                    item["sources"].append(contact_source)
            item["contact_checked"] = CHECKED
        rows.append(item)

    for fields in OTHER_PARSED:
        (seat, dedication, seat_local, local, rank, raw_phones,
         source) = fields
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-karpenision-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "sources": [source],
        }
        if dedication == "Saint Sabbas the Sanctified":
            item["address"] = ["Καραπιπέρη 22", "Καρπενήσι"]
        if raw_phones:
            item["phones"] = [phone(value) for value in raw_phones.split(",")]
            item["contact_sources"] = [source]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 111
EXPECTED_OWNER_COUNTS = {PARENT: 111}
EXPECTED_KINDS = {"monastery": 9, "parish": 102}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Church": 2,
    "Chapel": 2,
    "Metochion": 3,
    "Metropolitan Chapel": 1,
    "Monastery": 5,
    "Monastic Dependency": 1,
    "Parish Church": 96,
}
EXPECTED_CONTACT_BODIES = 82
EXPECTED_PHONE_BODIES = 79
EXPECTED_PHONE_VALUES = 124
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 7
EXPECTED_ADDRESS_BODIES = 111
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
        "imkarpenisiou.gr", "www.imkarpenisiou.gr",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
        "e-nomothesia.gr", "www.e-nomothesia.gr",
        "ia37rg02wpsa01.blob.core.windows.net",
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
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s site lacks source provenance" % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Karpenision candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Karpenision candidate ledger date drifted")
    expected_summary = {
        PARENT: 111,
        "total": 111,
        "exact_current_parishes": 97,
        "exact_current_monasteries": 5,
        "exact_current_monastic_dependencies": 4,
        "exact_current_other_churches_and_chapels": 5,
        "parish_kind_rows": 102,
        "monastery_kind_rows": 9,
        "contact_bodies": 82,
        "phone_bodies": 79,
        "public_phone_values": 124,
        "email_bodies": 0,
        "public_email_values": 0,
        "official_detail_sites": 7,
        "address_bodies": 111,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Karpenision candidate ledger summary drifted")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 5:
        raise ValueError("Karpenision candidate ledger lacks held leads")
    for key in ("candidates", "source_reconciliations", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Karpenision ledger lacks %s" % key)
        for entry in ledger[key]:
            for source_url in entry.get("sources") or []:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Karpenision ledger has an invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Karpenision ledger repeats a candidate id")
    if FORBIDDEN_PUNCTUATION.search(
            json.dumps(ledger, ensure_ascii=False)):
        raise ValueError("Karpenision ledger has forbidden punctuation")


def build():
    result = []
    ids = set()
    signatures = {}
    owner_counts = Counter()
    kind_counts = Counter()
    rank_counts = Counter()
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
        for field in ("kind", "rank", "name", "local", "seat"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        if any(re.search(r"(^|\s)π\.", text)
               for text in walk_strings(item)):
            raise ValueError("%s exposes a clergy name marker" % row_id)
        for email_value in item.get("emails") or []:
            if not EMAIL_RE.match(email_value):
                raise ValueError("%s carries an invalid email" % row_id)
        for phone_value in item.get("phones") or []:
            if not re.match(r"^\+30-\d{10}$", phone_value):
                raise ValueError("%s carries an invalid phone" % row_id)
        if len(set(item.get("phones") or [])) != len(item.get("phones") or []):
            raise ValueError("%s repeats a public phone" % row_id)
        signature = (parent, unicase(item["local"]), unicase(item["seat"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s after normalization" % (
                row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[parent] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (
            EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Karpenision English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Karpenision English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Karpenision parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Karpenision kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Karpenision rank totals drifted: %r" %
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
        raise ValueError("Karpenision contact coverage drifted: %r" %
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


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    value = value.replace("\u2013", "-").replace("\u2014", "-")
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
            response.geturl(),
        )


def assert_html_markers(url, markers, label):
    content_type, payload, unused = fetch_source(url)
    if "html" not in content_type:
        raise ValueError("%s returned a non-HTML response" % label)
    text = normalize_source_text(payload.decode("utf-8", "replace"))
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("%s source marker drifted: %s" % (label, marker))


def parse_live_roster(payload):
    text = payload.decode("utf-8", "replace")
    match = re.search(
        r"<h3[^>]*>\s*Ιεροί Ναοί και Εφημέριοι\s*</h3>\s*"
        r"<p[^>]*>(.*?)</p>",
        text,
        re.I | re.S,
    )
    if not match:
        raise ValueError("current roster body could not be located")
    segment = re.sub(r"<br\s*/?>", "\n", match.group(1), flags=re.I)
    segment = html.unescape(re.sub(r"<[^>]+>", "", segment))
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in segment.splitlines()
        if re.sub(r"\s+", " ", line).strip()
    ]
    records = []
    clergy_lines = []
    current = None
    for line in lines:
        numbers = re.findall(r"(?<!\d)(\d{10})(?!\d)", line)
        body = line
        if "π." in body:
            clergy_lines.append(body)
            body = body.split("π.", 1)[0]
        body = re.sub(r"(?<!\d)\d{10}(?!\d)", "", body).strip()
        if body:
            if current is None:
                current = [body, None, []]
            elif current[1] is None:
                current[1] = body
            else:
                records.append(current)
                current = [body, None, []]
        if numbers:
            if current is None:
                raise ValueError("phone appeared before a roster body")
            current[2].extend(numbers)
    if current:
        records.append(current)
    return records, clergy_lines


def validate_live_roster(payload):
    records, clergy_lines = parse_live_roster(payload)
    if len(records) != 100:
        raise ValueError("current roster expected 100 raw rows, found %d" %
                         len(records))
    parish_records = [
        row for row in records
        if "ΙΕΡΑ ΜΟΝΗ" not in row[0] and "ΙΕΡΑ ΜΟΝΗ" not in row[1]
    ]
    monastic_records = [row for row in records if row not in parish_records]
    if len(parish_records) != 96 or len(monastic_records) != 4:
        raise ValueError("current roster parish/monastic shape drifted")
    live = {
        (unicase(row[0]), unicase(row[1])): tuple(row[2])
        for row in parish_records
    }
    expected = {
        (unicase(seat_local), unicase(dedication_local)):
            tuple(raw_phones.split(",") if raw_phones else [])
        for seat, dedication, seat_local, dedication_local, raw_phones
        in PARISH_PARSED if seat != "Roska"
    }
    if live != expected:
        missing = sorted(set(expected) - set(live))
        extra = sorted(set(live) - set(expected))
        raise ValueError(
            "current roster reconciliation drifted: missing %r extra %r" %
            (missing, extra)
        )
    combined = {"Proussos": set(), "Tatarnis": set()}
    for seat, dedication, numbers in monastic_records:
        key = "Tatarnis" if "ΤΑΤΑΡΝΗΣ" in seat else "Proussos"
        combined[key].update(numbers)
    if combined != {
        "Proussos": {"6946866770", "6949110350"},
        "Tatarnis": {"6970093838", "6979605834", "2237095400"},
    }:
        raise ValueError("current monastic contact roster drifted")
    published = normalize_source_text(json.dumps(ROWS, ensure_ascii=False))
    for line in clergy_lines:
        personal = line.split("π.", 1)[1]
        personal = re.sub(r"\d", "", personal).strip(" .&")
        if len(personal) > 5 and normalize_source_text(personal) in published:
            raise ValueError("a clergy name leaked into published rows")


LIVE_DETAIL_MARKERS = {
    "https://imkarpenisiou.gr/cms/koimdomianoi/": (
        "Ιερή Μονή Κοιμήσεως Της Θεοτόκου Δομιανοί",
    ),
    "https://imkarpenisiou.gr/cms/braxa-2/": (
        "Ιερή Μονή Παναγίας Προυσιώτισσας", "Προυσός",
    ),
    "https://imkarpenisiou.gr/cms/braxa/": (
        "Ιερή Μονή Μεταμόρφωσης Του Σωτήρα", "Βράχα",
    ),
    "https://imkarpenisiou.gr/cms/pantarn/": (
        "Ιερά Μονή Παναγίας Ταρτάνας",
    ),
    "https://imkarpenisiou.gr/cms/braxa-2-2-2-2/": (
        "Μονή Γέννησης Της Θεοτόκου", "Επινιανών",
    ),
    "https://imkarpenisiou.gr/cms/braxa-2-2-2/": (
        "Μετόχι Οσίας Μαρίας της Αιγύπτιας", "Νέο Μικρό Χωριό",
    ),
    "https://imkarpenisiou.gr/cms/braxa-2-2/": (
        "Μετόχι Αγίου Νεκταρίου", "Καρπενήσι",
    ),
}

LIVE_POST_MARKERS = {
    CATHEDRAL_POST: (
        "Μητροπολιτικού Ναού Αγίας Τριάδος", "Καρπενησίου",
    ),
    CEMETERY_ARCHANGEL_POST: (
        "κοιμητηριακό ναό του Αρχαγγέλου Μιχαήλ", "6972267840",
    ),
    IAKOVOS_POST: (
        "παρεκκλησίου του Οσίου Ιακώβου του Τσαλίκη", "Επισκοπείου",
    ),
    NICHOLAS_KARPENISIOT_POST: (
        "Άγιος Νικόλαος ο παντοπώλης", "ομώνυμο παρεκκλήσι",
    ),
    OLD_CEMETERY_GEORGE_POST: (
        "Ιερό Ναό Αγίου Γεωργίου", "παλαιό κοιμητήριο",
    ),
    SABBAS_CHAPEL_POST: (
        "Αγίου Σάββα του Ηγιασμένου", "Καραπιπέρη 22",
    ),
    KOUMASIA_POST: (
        "Ιερό Ναό Παναγίας Κουμασίων", "μετόχι της Ιεράς Μονής Προυσού",
    ),
}


def check_marker_pair(pair):
    url, markers = pair
    assert_html_markers(url, markers, "current body source")
    return url


def check_live_sources():
    assert_html_markers(
        METROPOLIS_HOME,
        ("Ιερά Μητρόπολις Καρπενησίου", "ΙΕΡΕΙΣ & ΤΗΛΕΦΩΝΑ"),
        "Metropolis home",
    )
    content_type, payload, unused = fetch_source(ROSTER_PAGE)
    if "html" not in content_type:
        raise ValueError("current roster returned a non-HTML response")
    validate_live_roster(payload)
    assert_html_markers(
        ACTIVE_MONASTERIES_PAGE,
        (
            "Μοναστήρια Ενεργεία",
            "Ι.Μ. Κοιμήσεως Θεοτόκου Δομιανοί",
            "Ι.Μ. Παναγίας Προυσιώτισσας",
            "Ι.Μ. Μεταμόρφωσης Σωτήρος Βράχα",
            "Ι.Μ. Παναγίας Ταρτάνας",
            "Ι.Μ. Γέννησης Θεοτόκου Επινιανά",
            "Μετόχι Οσίας Μαρίας Αιγύπτιας",
            "Μετόχι Αγίου Νεκταρίου",
        ),
        "active monastery roster",
    )
    assert_html_markers(
        CHURCH_OF_GREECE_PAGE,
        (
            "Ανδρικές μονές",
            "Προυσού", "22370-80705",
            "Τατάρνης", "22370-95400",
            "Αγ. Νεκταρίου Καρπενησίου", "22370-22979", "22621",
            "Οσίας Μαρίας Αιγυπτίας", "22370-41322",
            "Ι. Κάθισμα Αγ. Σάββα Τριποτάμου",
        ),
        "Church of Greece profile",
    )
    assert_html_markers(
        LEGAL_PAGE,
        ("738/854/2019", "ΦΕΚ 2148/Β/7-6-2019", "Καρπενησίου"),
        "legal roster page",
    )
    content_type, payload, unused = fetch_source(LEGAL_PDF)
    if not payload.startswith(b"%PDF"):
        raise ValueError("official legal roster is not a valid PDF")
    if len(payload) < 100000:
        raise ValueError("official legal roster PDF is unexpectedly small")
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(check_marker_pair, LIVE_DETAIL_MARKERS.items()))
        list(executor.map(check_marker_pair, LIVE_POST_MARKERS.items()))


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
            "Karpenision: %d exact current bodies; %d carry public "
            "body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Karpenision: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
