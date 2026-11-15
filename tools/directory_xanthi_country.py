#!/usr/bin/env python3
"""Validate exact named Xanthi bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_xanthi_country.py --check
    python tools/directory_xanthi_country.py --check-live
    python tools/directory_xanthi_country.py --dump
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
PARENT = "ep-xanthi"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "xanthi_country.json"
)

BASE = "https://im-xanthis.gr"
EP_URL = "https://ec-patr.org/entities/iera-mitropoli-ksanthis/"
COG_URL = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/xanthes-kai-peritheoriou"
)
REGULATION_URL = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_january.pdf"
)
LOCAL_ADMIN_URL = BASE + "/dioikisi/"
LOCAL_MONASTERIES_URL = BASE + "/ieres-mones/"
LOCAL_MAP_URL = BASE + "/proskinimatikos-tourismos/"


# key|English seat|Greek seat|English dedication|Greek dedication|rank
#
# The official regulation gives the exact 86-name roster. The current
# Patriarchate and Metropolis profiles independently retain the aggregate at
# 86 parish churches. The source order is preserved by archieratical region:
# Xanthi 20, Abdera 25, Stavroupolis 22, and Topeiros 19.
PARISH_SOURCE = r"""
forerunner-xanthi|Xanthi|Ξάνθη|Saint John the Forerunner|Τιμίου Προδρόμου|Metropolitan Cathedral
anna-xanthi|Xanthi|Ξάνθη|Saint Anna|Αγίας Άννης|Parish Church
twelve-apostles-xanthi|Xanthi|Ξάνθη|Holy Twelve Apostles|Αγίων Δώδεκα Αποστόλων|Parish Church
george-xanthi|Xanthi|Ξάνθη|Saint George|Αγίου Γεωργίου|Parish Church
akathist-hymn-xanthi|Xanthi|Ξάνθη|Akathist Hymn|Ακαθίστου Ύμνου|Parish Church
eleutherius-xanthi|Xanthi|Ξάνθη|Saint Eleutherius|Αγίου Ελευθερίου|Parish Church
theophanes-xanthi|Xanthi|Ξάνθη|Saint Theophanes of Peritheorion|Αγίου Θεοφάνους Περιθεωρίου|Parish Church
cyril-methodius-xanthi|Xanthi|Ξάνθη|Saints Cyril and Methodius|Αγίων Κυρίλλου και Μεθοδίου|Parish Church
constantine-helen-xanthi|Xanthi|Ξάνθη|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church
transfiguration-xanthi|Xanthi|Ξάνθη|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church
nicholas-xanthi|Xanthi|Ξάνθη|Saint Nicholas|Αγίου Νικολάου|Parish Church
raphael-nicholas-irene-xanthi|Xanthi|Ξάνθη|Saints Raphael, Nicholas, and Irene|Αγίων Ραφαήλ, Νικολάου και Ειρήνης|Parish Church
tryphon-xanthi|Xanthi|Ξάνθη|Saint Tryphon|Αγίου Τρύφωνος|Parish Church
archangels-kavaki-xanthi|Xanthi|Ξάνθη|Holy Archangels at Kavaki|Παμμεγίστων Ταξιαρχών Καβακίου|Parish Church
photini-chrysa|Chrysa|Χρύσα|Saint Photini the Samaritan|Αγίας Φωτεινής της Σαμαρείτιδος|Parish Church
life-giving-spring-evmoiron|Evmoiron|Εύμοιρο|Life-giving Spring|Ζωοδόχου Πηγής|Parish Church
demetrius-kimmeria|Kimmeria|Κιμμέρια|Saint Demetrius|Αγίου Δημητρίου|Parish Church
peter-paul-lefki|Lefki|Λεύκη|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Parish Church
savvas-nea-morsini|Nea Morsini|Νέα Μορσίνη|Saint Savvas|Αγίου Σάββα|Parish Church
christopher-petrochori|Petrochori|Πετροχώρι|Saint Christopher|Αγίου Χριστοφόρου|Parish Church
paraskevi-abdera|Abdera|Άβδηρα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
demetrius-afxentio|Afxentio|Αυξέντιο|Saint Demetrius|Αγίου Δημητρίου|Parish Church
gerasimos-vafeika|Vafeika|Βαφέικα|Saint Gerasimos|Αγίου Γερασίμου|Parish Church
life-giving-spring-veloni|Veloni|Βελόνη|Life-giving Spring|Ζωοδόχου Πηγής|Parish Church
presentation-genisea|Genisea|Γενισέα|Presentation of the Lord|Υπαπαντής του Κυρίου|Parish Church
archangels-giona|Giona|Γκιώνα|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church
george-diomideia|Diomideia|Διομήδεια|Saint George|Αγίου Γεωργίου|Parish Church
george-neos-zygos|Neos Zygos|Νέος Ζυγός|Saint George|Αγίου Γεωργίου|Parish Church
life-giving-spring-palaios-zygos|Palaios Zygos|Παλαιός Ζυγός|Life-giving Spring|Ζωοδόχου Πηγής|Parish Church
holy-cross-nea-kessani|Nea Kessani|Νέα Κεσσάνη|Holy Cross|Τιμίου Σταυρού|Parish Church
george-koutso-abdera|Koutso|Κουτσό|Saint George|Αγίου Γεωργίου|Parish Church
george-lefkopetra|Lefkopetra|Λευκόπετρα|Saint George|Αγίου Γεωργίου|Parish Church
constantine-helen-magiko|Magiko|Μαγικό|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church
prophet-elijah-mandra|Mandra|Μάνδρα|Prophet Elijah|Προφήτου Ηλιού|Parish Church
george-myrodato|Myrodato|Μυρωδάτο|Saint George|Αγίου Γεωργίου|Parish Church
holy-girdle-pezoula|Pezoula|Πεζούλα|Holy Girdle of the Theotokos|Τιμίας Ζώνης της Θεοτόκου|Parish Church
peter-paul-peteinos|Peteinos|Πετεινός|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Parish Church
dormition-pigadia|Pigadia|Πηγάδια|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
george-polysitos|Polysitos|Πολύσιτος|Saint George|Αγίου Γεωργίου|Parish Church
transfiguration-porto-lagos|Porto Lagos|Πόρτο Λάγος|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church
unmercenaries-potamia|Potamia|Ποταμιά|Holy Unmercenaries|Αγίων Αναργύρων|Parish Church
charalambos-selino|Selino|Σέλινο|Saint Charalambos|Αγίου Χαραλάμπους|Parish Church
thomas-sounio|Sounio|Σούνιο|Apostle Thomas|Αποστόλου Θωμά|Parish Church
athanasius-syndini|Syndini|Σύνδινη|Saint Athanasius|Αγίου Αθανασίου|Parish Church
panteleimon-feloni|Feloni|Φελώνη|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church
george-dafnonas|Dafnonas|Δαφνώνας|Saint George|Αγίου Γεωργίου|Parish Church
nativity-forerunner-drymia|Drymia|Δρυμιά|Nativity of Saint John the Forerunner|Γενεσίου του Τιμίου Προδρόμου|Parish Church
george-echinos|Echinos|Εχίνος|Saint George|Αγίου Γεωργίου|Parish Church
george-ano-ioniko|Ano Ioniko|Άνω Ιωνικό|Saint George|Αγίου Γεωργίου|Parish Church
dormition-kato-ioniko|Kato Ioniko|Κάτω Ιωνικό|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
george-kallithea|Kallithea|Καλλιθέα|Saint George|Αγίου Γεωργίου|Parish Church
prophet-elijah-kalyva|Kalyva|Καλύβα|Prophet Elijah|Προφήτου Ηλιού|Parish Church
demetrius-ano-karyofyto|Ano Karyofyto|Άνω Καρυόφυτο|Saint Demetrius|Αγίου Δημητρίου|Parish Church
holy-cross-kato-karyofyto|Kato Karyofyto|Κάτω Καρυόφυτο|Holy Cross|Τιμίου Σταυρού|Parish Church
dormition-kastanies|Kastanies|Καστανιές|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
peter-paul-komnina|Komnina|Κομνηνά|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Parish Church
ascension-leivaditis|Leivaditis|Λειβαδίτης|Ascension of the Lord|Αναλήψεως του Κυρίου|Parish Church
life-giving-spring-lykovounio|Lykovounio|Λυκοβούνιο|Life-giving Spring|Ζωοδόχου Πηγής|Parish Church
constantine-helen-lykodromio|Lykodromio|Λυκοδρόμιο|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church
nicholas-margariti|Margariti|Μαργαρίτι|Saint Nicholas|Αγίου Νικολάου|Parish Church
george-myrtousa|Myrtousa|Μυρτούσα|Saint George|Αγίου Γεωργίου|Parish Church
life-giving-spring-neochori|Neochori|Νεοχώρι|Life-giving Spring|Ζωοδόχου Πηγής|Parish Church
george-paschalia|Paschalia|Πασχαλιά|Saint George|Αγίου Γεωργίου|Parish Church
archangels-sidiropetra|Sidiropetra|Σιδηρόπετρα|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church
annunciation-stavroupoli|Stavroupoli|Σταυρούπολη|Annunciation of the Theotokos|Ευαγγελισμού της Θεοτόκου|Parish Church
demetrius-stavrochori|Stavrochori|Σταυροχώρι|Saint Demetrius|Αγίου Δημητρίου|Parish Church
life-giving-spring-chalepi|Chalepi|Χαλέπι|Life-giving Spring|Ζωοδόχου Πηγής|Parish Church
nativity-theotokos-avato|Avato|Άβατο|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Parish Church
athanasius-agios-athanasios|Agios Athanasios|Άγιος Αθανάσιος|Saint Athanasius|Αγίου Αθανασίου|Parish Church
prophet-elijah-nea-amissos|Nea Amissos|Νέα Αμισσός|Prophet Elijah|Προφήτου Ηλιού|Parish Church
panteleimon-galani|Galani|Γαλάνη|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church
euphemia-dasochori|Dasochori|Δασοχώρι|Saint Euphemia|Αγίας Ευφημίας|Parish Church
kyriaki-dekarcho|Dekarcho|Δέκαρχο|Saint Kyriaki|Αγίας Κυριακής|Parish Church
nikodimos-exochi|Exochi|Εξοχή|Saint Nikodimos the Hagiorite|Αγίου Νικοδήμου του Αγιορείτου|Parish Church
forerunner-erasmio|Erasmio|Εράσμιο|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church
ascension-evlalo|Evlalo|Εύλαλο|Ascension of the Lord|Αναλήψεως του Κυρίου|Parish Church
holy-cross-thalassia|Thalassia|Θαλασσιά|Holy Cross|Τιμίου Σταυρού|Parish Church
stylianos-koutso-topeiros|Koutso|Κουτσό|Saint Stylianos|Αγίου Στυλιανού|Parish Church
nectarios-kremasti|Kremasti|Κρεμαστή|Saint Nectarios|Αγίου Νεκταρίου|Parish Church
george-kypseli|Kypseli|Κυψέλη|Saint George|Αγίου Γεωργίου|Parish Church
holy-trinity-mangana|Mangana|Μάγγανα|Holy Trinity|Αγίας Τριάδος|Parish Church
demetrius-melissa|Melissa|Μέλισσα|Saint Demetrius|Αγίου Δημητρίου|Parish Church
george-neo-olvio|Neo Olvio|Νέο Όλβιο|Saint George|Αγίου Γεωργίου|Parish Church
panteleimon-palaio-olvio|Palaio Olvio|Παλαιό Όλβιο|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church
dormition-toxotes|Toxotes|Τοξότες|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
demetrius-tympano|Tympano|Τύμπανο|Saint Demetrius|Αγίου Δημητρίου|Parish Church
"""


def article(path):
    return BASE + path


ARTICLE_URLS = {
    "wisdom": article(
        "/2026/10/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%ba%ce%b1%ce%b8%ce%b5%ce%b4%cf%81%ce%b9%ce%ba%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%84%ce%b7%cf%83-%cf%84%ce%bf%cf%85-%ce%b8%ce%b5%ce%bf%cf%85-%cf%83%ce%bf-14/"
    ),
    "eustathius": article(
        "/2026/09/%ce%b9%ce%b5%cf%81%ce%bf%ce%bd-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%ce%bd-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%bc%ce%b5%ce%b3%ce%b1%ce%bb%ce%bf%ce%bc-3/"
    ),
    "marina-myrodato": article(
        "/2026/07/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%ce%b9%cf%83-%ce%be%ce%b1%ce%bd%ce%b8%ce%b7%cf%83-%ce%ba%ce%b1%ce%b9-%cf%80%ce%b5%cf%81%ce%b9%ce%b8%ce%b5%cf%89%cf%81%ce%b9-77/"
    ),
    "marina-evmoiron": article(
        "/2026/07/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%ce%b9%cf%83-%ce%be%ce%b1%ce%bd%ce%b8%ce%b7%cf%83-%ce%ba%ce%b1%ce%b9-%cf%80%ce%b5%cf%81%ce%b9%ce%b8%ce%b5%cf%89%cf%81%ce%b9-76/"
    ),
    "paisios-cyril": article(
        "/2026/07/%ce%b9%ce%b5%cf%81%cf%8c%ce%bd-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%ae%cf%83%ce%b9%ce%bf%ce%bd-%cf%84%ce%bf%cf%85-%ce%bf%cf%83%ce%af%ce%bf%cf%85-%cf%80%ce%b1%cf%8a%cf%83%ce%af%ce%bf%cf%85-4/"
    ),
    "holy-trinity": article(
        "/2026/06/%ce%b7-%ce%b5%ce%bf%cf%81%cf%84%ce%ae-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%cf%80%ce%bd%ce%b5%cf%8d%ce%bc%ce%b1%cf%84%ce%bf%cf%82-%cf%83%cf%84%ce%bf%ce%bd-%ce%b9%ce%b5%cf%81%cf%8c-%ce%bd/"
    ),
    "ephraim": article(
        "/2026/05/%ce%b9%ce%b5%cf%81%ce%bf%ce%bd-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%ce%bd-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b5%cf%86%cf%81%ce%b1%ce%b9%ce%bc-%cf%84/"
    ),
    "alexander": article(
        "/2025/08/%cf%80%ce%b1%ce%bd%ce%b7%ce%b3%cf%85%cf%81%ce%b9%cf%83-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%cf%85-%ce%b1%ce%b3-%ce%b1%ce%bb%ce%b5%ce%be%ce%b1%ce%bd%ce%b4%cf%81%ce%bf/"
    ),
    "paisios-theophanes": article(
        "/2025/07/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%ce%b9%cf%83-%ce%be%ce%b1%ce%bd%ce%b8%ce%b7%cf%83-%ce%ba%ce%b1%ce%b9-%cf%80%ce%b5%cf%81%ce%b9%ce%b8%ce%b5%cf%89%cf%81%ce%b9-39/"
    ),
    "christopher-george": article(
        "/2024/11/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%af%ce%be%ce%b9%ce%b1-%cf%84%ce%bf%cf%85-%ce%b9%ce%b5%cf%81%ce%bf%cf%8d-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%af%ce%bf%cf%85-%cf%84%cf%89/"
    ),
    "phanourios": article(
        "/2024/08/%ce%b1%cf%80%cf%8c-%cf%84%ce%b7%ce%bd-%ce%b5%ce%bf%cf%81%cf%84%ce%ae-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%ce%bc%ce%b5%ce%b3%ce%b1%ce%bb%ce%bf%ce%bc%ce%ac%cf%81%cf%84%cf%85%cf%81%ce%bf/"
    ),
    "kosmas": article(
        "/2024/08/%ce%b1%cf%80%cf%8c-%cf%84%ce%b7%ce%bd-%ce%b5%ce%bf%cf%81%cf%84%ce%ae-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%ce%ba%ce%bf%cf%83%ce%bc%ce%ac-%cf%84%ce%bf%cf%85-%ce%b1%ce%b9%cf%84%cf%89%ce%bb/"
    ),
    "elijah": article(
        "/2024/07/%ce%b9%ce%b5%cf%81%ce%bf%ce%bd-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%ce%bd-%cf%80%cf%81%ce%bf%cf%86%ce%b7%cf%84%ce%bf%cf%85-%ce%b7%ce%bb%ce%b9%ce%bf%cf%85-%cf%84%ce%bf/"
    ),
    "forty-martyrs": article(
        "/2024/03/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%bf%ce%bd%ce%b7-%cf%80%ce%b1%ce%bd%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%ce%b1%cf%81%cf%87%ce%b1%ce%b3%ce%b3%ce%b5%ce%bb%ce%b9%cf%89%cf%84%ce%b9%cf%83%cf%83%ce%b7%cf%83-10/"
    ),
    "joachim-anna": article(
        "/2025/09/%cf%80%ce%b1%ce%bd%ce%b7%ce%b3%cf%85%cf%81%ce%b9%cf%83-%ce%b9%ce%b5%cf%81%ce%bf%cf%85-%ce%bd%ce%b1%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%cf%89%ce%bd-%ce%b8%ce%b5%ce%bf%cf%80%ce%b1%cf%84%ce%bf%cf%81%cf%89/"
    ),
    "anna-kallithea": article(
        "/2026/07/%ce%b9%ce%b5%cf%81%cf%8c%cf%82-%ce%bd%ce%b1%cf%8c%cf%82-%cf%84%ce%b7%cf%82-%ce%b1%ce%b3%ce%af%ce%b1%cf%82-%ce%ac%ce%bd%ce%bd%ce%b7%cf%82-%cf%83%cf%84%ce%bf%ce%bd-%ce%bf%ce%b9%ce%ba%ce%b9%cf%83%ce%bc-3/"
    ),
    "panteleimon-dafnonas": article(
        "/2025/07/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%ce%b9%cf%83-%ce%be%ce%b1%ce%bd%ce%b8%ce%b7%cf%83-%ce%ba%ce%b1%ce%b9-%cf%80%ce%b5%cf%81%ce%b9%ce%b8%ce%b5%cf%89%cf%81%ce%b9-49/"
    ),
    "spyridon-kosmiti": article(
        "/2025/12/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%83%cf%80%cf%85%cf%81%ce%b9%ce%b4%cf%89%ce%bd%ce%bf%cf%83-%cf%83%cf%84%ce%bf%ce%bd-%ce%bf%ce%b9%ce%ba%ce%b9/"
    ),
    "archangels-stavroupoli": article(
        "/2025/11/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%84%cf%89%ce%bd-%cf%80%ce%b1%ce%bc%ce%bc%ce%b5%ce%b3%ce%b9%cf%83%cf%84%cf%89%ce%bd-%cf%84%ce%b1%ce%be%ce%b9%ce%b1%cf%81%cf%87%cf%89%ce%bd-5/"
    ),
    "polycarp": article(
        "/2024/02/%ce%b9%ce%b5%cf%81%cf%8c%cf%82-%ce%bd%ce%b1%cf%8c%cf%82-%cf%84%ce%bf%cf%85-%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%cf%80%ce%bf%ce%bb%cf%85%ce%ba%ce%ac%cf%81%cf%80%ce%bf%cf%85-%cf%83%cf%84%ce%b7%ce%bd-%ce%bc/"
    ),
    "blaise": article(
        "/2026/02/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b2%ce%bb%ce%b1%cf%83%ce%b9%ce%bf%cf%85-%ce%be%ce%b1%ce%bd%ce%b8%ce%b7%cf%83-%cf%80%ce%b1%ce%bd%ce%b7%ce%b3-3/"
    ),
    "john-theologian-thermes": article(
        "/2024/09/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%b7%cf%84%cf%81%ce%bf%cf%80%ce%bf%ce%bb%ce%b9%cf%83-%ce%be%ce%b1%ce%bd%ce%b8%ce%b7%cf%83-%ce%ba%ce%b1%ce%b9-%cf%80%ce%b5%cf%81%ce%b9%ce%b8%ce%b5%cf%89%cf%81%ce%b9-13/"
    ),
}


def parse_parishes():
    rows = []
    keys = []
    for number, raw in enumerate(
            (line for line in PARISH_SOURCE.splitlines() if line.strip()), 1):
        parts = raw.split("|")
        if len(parts) != 6:
            raise ValueError("invalid Xanthi parish source row: %s" % raw)
        key, seat, seat_local, dedication, dedication_local, rank = parts
        keys.append(key)
        rows.append({
            "id": "gr-ep-xanthi-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s Parish Church in %s" % (dedication, seat),
            "local": "Ιερός Ναός %s, %s" % (dedication_local, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "sources": [REGULATION_URL, EP_URL],
        })
    if len(rows) != 86:
        raise ValueError("expected 86 Xanthi regulation parishes")
    region_boundaries = {
        1: "forerunner-xanthi",
        20: "christopher-petrochori",
        21: "paraskevi-abdera",
        45: "panteleimon-feloni",
        46: "george-dafnonas",
        67: "life-giving-spring-chalepi",
        68: "nativity-theotokos-avato",
        86: "demetrius-tympano",
    }
    if any(keys[position - 1] != key
           for position, key in region_boundaries.items()):
        raise ValueError("Xanthi regulation region boundaries drifted")
    return rows


ROWS = parse_parishes()
LIVE_MARKERS = {}


def add_row(item, markers):
    ROWS.append(item)
    LIVE_MARKERS[item["id"]] = markers


add_row({
    "id": "gr-ep-xanthi-087-wisdom-of-god-pilgrimage-cathedral",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Pilgrimage Cathedral",
    "name": "Wisdom of God Pilgrimage Cathedral in Xanthi",
    "local": "Ιερός Καθεδρικός Ναός της του Θεού Σοφίας Ξάνθης",
    "seat": "Xanthi",
    "country": "GR",
    "address": ["Ξάνθη"],
    "sources": [REGULATION_URL, ARTICLE_URLS["wisdom"]],
}, ["Καθεδρικός Ναός της του Θεού Σοφίας", "Ξάνθης"])


MONASTERIES = [
    (
        "archangeliotissa-monastery", "Xanthi", "Ξάνθη",
        "Monastery of Panagia Archangeliotissa in Xanthi",
        "Ιερά Μονή Παναγίας Αρχαγγελιωτίσσης Ξάνθης",
        ["25410-29799"], ["Παναγίας Αρχαγγελιωτίσσης"],
    ),
    (
        "archangels-ecclesiastical-school-monastery", "Xanthi", "Ξάνθη",
        "Monastery of the Holy Archangels at the Ecclesiastical School of Xanthi",
        "Ιερά Μονή Παμμεγίστων Ταξιαρχών Εκκλησιαστικής Σχολής Ξάνθης",
        ["25410-22362", "25410-29911"],
        ["Παμμεγίστων Ταξιαρχών", "Εκκλησιαστικόν Γυμνάσιον"],
    ),
    (
        "kalamou-monastery", "Xanthi", "Ξάνθη",
        "Monastery of Panagia Kalamou in Xanthi",
        "Ιερά Μονή Παναγίας Καλαμούς Ξάνθης",
        ["25410-29899", "25410-66000"], ["Παναγίας Καλαμούς"],
    ),
    (
        "irene-monastery", "Xanthi", "Ξάνθη",
        "Monastery of Saint Irene the Great Martyr in Xanthi",
        "Ιερά Μονή Αγίας Μεγαλομάρτυρος Ειρήνης Ξάνθης",
        ["25410-25460", "25410-25558"],
        ["Μεγαλομάρτυρος Ειρήνης"],
    ),
]

for offset, record in enumerate(MONASTERIES, 88):
    key, seat, seat_local, name, local, phones, markers = record
    add_row({
        "id": "gr-ep-xanthi-%03d-%s" % (offset, key),
        "parent": PARENT,
        "kind": "monastery",
        "rank": "Monastery",
        "name": name,
        "local": local,
        "seat": seat,
        "country": "GR",
        "address": ["Τ.Κ. 671 00 " + seat_local],
        "phones": phones,
        "sources": [EP_URL, COG_URL, LOCAL_MONASTERIES_URL],
        "contact_sources": [EP_URL],
        "contact_checked": CHECKED,
    }, markers)

add_row({
    "id": "gr-ep-xanthi-092-nativity-theotokos-komnina-dependency",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastic Dependency",
    "name": (
        "Nativity of the Theotokos Monastic Dependency of Panagia Kalamou "
        "in Komnina"
    ),
    "local": (
        "Ιερό Μετόχιο Παναγίας Καλαμούς Γενεσίου της Θεοτόκου Κομνηνών"
    ),
    "seat": "Komnina",
    "country": "GR",
    "address": ["Κομνηνά"],
    "phones": ["6946605741"],
    "sources": [EP_URL],
    "contact_sources": [EP_URL],
    "contact_checked": CHECKED,
}, ["Μετόχιο Παναγίας Καλαμούς", "Γενεσίου της Θεοτόκου Κομνηνών"])


# key|English seat|Greek seat|English name|Greek local name|rank|article key|
# marker one|marker two
EXTRA_SOURCE = r"""
eustathius-selero|Selero|Σέλερο|Saint Eustathius Chapel in Selero|Ιερό Παρεκκλήσιο Αγίου Μεγαλομάρτυρος Ευσταθίου Σελέρου|Chapel|eustathius|Ευσταθίου|Σελέρου
marina-myrodato-beach|Myrodato Beach|Παραλία Μυρωδάτου|Saint Marina Chapel at Myrodato Beach|Ιερό Παρεκκλήσιο Αγίας Μεγαλομάρτυρος Μαρίνης στην παραλία Μυρωδάτου|Chapel|marina-myrodato|Αγίας Μαρίνης|παραλία του Μυρωδάτου
marina-evmoiron-grove|Evmoiron|Άλσος Ευμοίρου|Saint Marina Chapel in Evmoiron Grove|Ιερό Παρεκκλήσιο Αγίας Μεγαλομάρτυρος Μαρίνης στο άλσος Ευμοίρου|Chapel|marina-evmoiron|Αγίας Μαρίνης|άλσος Ευμοίρου
paisios-cyril-methodius|Xanthi|Ξάνθη|Saint Paisios the Hagiorite Chapel at Saints Cyril and Methodius Parish in Xanthi|Ιερό Παρεκκλήσιο Οσίου Παϊσίου του Αγιορείτου του Ιερού Ναού Αγίων Κυρίλλου και Μεθοδίου Ξάνθης|Chapel|paisios-cyril|Παϊσίου|Κυρίλλου και Μεθοδίου
holy-trinity-xanthi|Xanthi|Ξάνθη|Holy Trinity Chapel in Xanthi|Ιερό Παρεκκλήσιο Αγίας Τριάδος Ξάνθης|Chapel|holy-trinity|Παρεκκλήσιο Αγίας Τριάδος|Ξάνθης
ephraim-nea-morsini|Nea Morsini|Νέα Μορσίνη|Saint Ephraim of Nea Makri Chapel at Saint Savvas Parish in Nea Morsini|Ιερό Παρεκκλήσιο Αγίου Εφραίμ της Νέας Μάκρης του Ιερού Ναού Αγίου Σάββα Νέας Μορσίνης|Chapel|ephraim|Εφραίμ της Νέας Μάκρης|Νέα Μορσίνη
alexander-myrodato|Myrodato|Μυρωδάτο|Saint Alexander Chapel in Myrodato|Ιερό Παρεκκλήσιο Αγίου Αλεξάνδρου Μυρωδάτου|Chapel|alexander|Αλεξάνδρου|Μυρωδάτου
paisios-theophanes|Xanthi|Ξάνθη|Saint Paisios the Hagiorite Chapel at Saint Theophanes Parish in Xanthi|Ιερό Παρεκκλήσιο Οσίου Παϊσίου του Ιερού Ναού Αγίου Θεοφάνους Ξάνθης|Chapel|paisios-theophanes|Παϊσίου|Αγίου Θεοφάνους
christopher-george-petrochori|Petrochori|Πετροχώρι|Saints Christopher and George Chapel at Saint Christopher Parish in Petrochori|Ιερό Παρεκκλήσιο Αγίων Χριστοφόρου και Γεωργίου του Τροπαιοφόρου Πετροχωρίου|Chapel|christopher-george|Χριστοφόρου και Αγίου Γεωργίου|Πετροχωρίου
phanourios-erasmio|Erasmio|Εράσμιο|Saint Phanourios Chapel in Erasmio|Ιερό Παρεκκλήσιο Αγίου Φανουρίου Ερασμίου|Chapel|phanourios|Φανουρίου|Ερασμίου
kosmas-mandra|Mandra|Μάνδρα|Saint Kosmas of Aetolia Chapel in Mandra|Ιερό Παρεκκλήσιο Αγίου Κοσμά του Αιτωλού Μάνδρας|Chapel|kosmas|Κοσμά του Αιτωλού|Μάνδρας
prophet-elijah-pigadia|Pigadia|Πηγάδια|Prophet Elijah the Tishbite Chapel in Pigadia|Ιερό Παρεκκλήσιο Προφήτου Ηλιού του Θεσβίτου Πηγαδίων|Chapel|elijah|Προφήτου Ηλιού|Πηγάδια
forty-martyrs-archangeliotissa|Xanthi|Ξάνθη|Forty Martyrs Chapel at Panagia Archangeliotissa Monastery|Ιερό Παρεκκλήσιο Αγίων Τεσσαράκοντα Μαρτύρων της Ιεράς Μονής Παναγίας Αρχαγγελιωτίσσης|Monastic Chapel|forty-martyrs|Τεσσαράκοντα Μαρτύρων|Αρχαγγελιωτίσσης
joachim-anna-thermes|Thermes|Θέρμες|Saints Joachim and Anna Chapel in Thermes|Ιερό Παρεκκλήσιο Αγίων Θεοπατόρων Ιωακείμ και Άννης Θερμών|Chapel|joachim-anna|Ιωακείμ και Άννης|Θέρμες
anna-kallithea|Kallithea|Καλλιθέα|Saint Anna Church in Kallithea|Ιερός Ναός Αγίας Άννης Καλλιθέας|Church|anna-kallithea|Αγίας Άννης|Καλλιθέας
panteleimon-dafnonas|Dafnonas|Δαφνώνας|Saint Panteleimon Church in Dafnonas|Ιερός Ναός Αγίου Παντελεήμονος Δαφνώνος|Church|panteleimon-dafnonas|Παντελεήμονος|Δαφνώνος
spyridon-kosmiti|Kosmiti|Κοσμητή|Saint Spyridon Church in Kosmiti|Ιερός Ναός Αγίου Σπυρίδωνος Κοσμητής|Church|spyridon-kosmiti|Σπυρίδωνος|Κοσμητής
archangels-stavroupoli|Stavroupoli|Σταυρούπολη|Holy Archangels Church in Stavroupoli|Ιερός Ναός Παμμεγίστων Ταξιαρχών Σταυρουπόλεως|Church|archangels-stavroupoli|Παμμεγίστων Ταξιαρχών|Σταυρούπολη
polycarp-elderly-care|Xanthi|Ξάνθη|Saint Polycarp Church at the Saint Panteleimon Elderly Care Unit in Xanthi|Ιερός Ναός Αγίου Πολυκάρπου της Μονάδας Φροντίδας Ηλικιωμένων Ο Άγιος Παντελεήμων|Institutional Church|polycarp|Αγίου Πολυκάρπου|Μονάδα Φροντίδας Ηλικιωμένων
blaise-xanthi|Xanthi|Ξάνθη|Saint Blaise Church in Xanthi|Ιερός Ναός Αγίου Βλασίου Ξάνθης|Historic Church|blaise|Αγίου Βλασίου|Ξάνθης
john-theologian-thermes|Thermes|Θέρμες|Saint John the Theologian Country Church in Thermes|Ιερό Εξωκλήσι Αγίου Ιωάννου του Θεολόγου Θερμών|Country Church|john-theologian-thermes|Ιωάννου του Θεολόγου|Θέρμες
"""

for number, raw in enumerate(
        (line for line in EXTRA_SOURCE.splitlines() if line.strip()), 93):
    parts = raw.split("|")
    if len(parts) != 9:
        raise ValueError("invalid Xanthi exact-body row: %s" % raw)
    (key, seat, seat_local, name, local, rank, article_key,
     marker_one, marker_two) = parts
    add_row({
        "id": "gr-ep-xanthi-%03d-%s" % (number, key),
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "GR",
        "address": [seat_local],
        "sources": [ARTICLE_URLS[article_key]],
    }, [marker_one, marker_two])


ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 113
EXPECTED_OWNER_COUNTS = {PARENT: 113}
EXPECTED_KINDS = {"monastery": 5, "parish": 108}
EXPECTED_RANKS = {
    "Chapel": 13,
    "Church": 4,
    "Country Church": 1,
    "Historic Church": 1,
    "Institutional Church": 1,
    "Metropolitan Cathedral": 1,
    "Monastic Chapel": 1,
    "Monastic Dependency": 1,
    "Monastery": 4,
    "Parish Church": 85,
    "Pilgrimage Cathedral": 1,
}
EXPECTED_CONTACT_BODIES = 5
EXPECTED_PHONE_BODIES = 5
EXPECTED_PHONE_VALUES = 8
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 113
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
            "im-xanthis.gr", "ec-patr.org", "ecclesiagreece.gr",
            "www.ecclesiagreece.gr"}:
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
        raise ValueError("Xanthi candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Xanthi candidate ledger date drifted")
    expected_summary = {
        PARENT: 113,
        "total": 113,
        "current_regulation_parishes": 86,
        "parish_kind_rows": 108,
        "monastery_kind_rows": 5,
        "pilgrimage_cathedrals": 1,
        "monasteries": 4,
        "monastic_dependencies": 1,
        "exact_current_supplemental_bodies": 21,
        "exact_current_chapel_bodies": 14,
        "exact_current_other_churches": 7,
        "contact_bodies": 5,
        "phone_bodies": 5,
        "public_phone_values": 8,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 113,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Xanthi ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Xanthi ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Xanthi ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Xanthi ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Xanthi ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Xanthi candidate ledger has forbidden punctuation")
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
        raise ValueError("Xanthi English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Xanthi English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Xanthi parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Xanthi kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Xanthi rank totals drifted: %r"
                         % dict(sorted(rank_counts.items())))
    exact_chapels = sum(
        item["rank"] in {"Chapel", "Monastic Chapel"}
        for item in result
    )
    if exact_chapels != 14:
        raise ValueError("Xanthi exact chapel total drifted")
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
        raise ValueError("Xanthi contact coverage drifted: %r" % (coverage,))
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
    values = {EP_URL, COG_URL, REGULATION_URL, LOCAL_ADMIN_URL,
              LOCAL_MONASTERIES_URL, LOCAL_MAP_URL}
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
            if not payload.startswith(b"%PDF") or len(payload) < 100000:
                raise ValueError("invalid PDF payload")
            return None
        if "html" not in content_type:
            raise ValueError("unexpected content type %s" % content_type)
        return normalize_source_text(payload.decode("utf-8", "replace"))


def check_live_sources():
    failures = []
    source_texts = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
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
        raise ValueError("live Xanthi source check failed: %s" % rendered)

    ep_text = source_texts.get(EP_URL) or ""
    for marker in (
            "ενοριακοι ναοι: 86", "παρεκκλησια 100",
            "εξωκκλησια 25", "ναοι κοιμητηριων 1",
            "μοναστηριακοι ναοι: 4", "προσκυνηματικοι ναοι: 1"):
        if normalize_source_text(marker) not in ep_text:
            raise ValueError("live Xanthi aggregate marker failed: %s" % marker)

    marker_failures = []
    for row in ROWS:
        raw_markers = LIVE_MARKERS.get(row["id"])
        if not raw_markers:
            continue
        markers = [normalize_source_text(value) for value in raw_markers]
        if not any(
            source_texts.get(url) is not None and
            all(marker in source_texts.get(url, "") for marker in markers)
            for url in row["sources"]
        ):
            marker_failures.append((row["id"], raw_markers))
    if marker_failures:
        raise ValueError(
            "live Xanthi exact-source marker check failed: %r"
            % marker_failures
        )

    contact_failures = []
    for row in ROWS:
        for phone in row.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if not any(
                digits in re.sub(r"\D", "", source_texts.get(url) or "") or
                (
                    digits.startswith("25410") and
                    digits[-5:] in
                    re.sub(r"\D", "", source_texts.get(url) or "")
                )
                for url in row.get("contact_sources") or []
            ):
                contact_failures.append((row["id"], phone))
    if contact_failures:
        raise ValueError(
            "live Xanthi contact marker check failed: %r"
            % contact_failures
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
            "Xanthi: %d exact named bodies; %d carry current public "
            "body-associated contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Xanthi: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
