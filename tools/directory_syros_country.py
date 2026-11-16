#!/usr/bin/env python3
"""Validate exact current worship bodies of the Holy Metropolis of Syros.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_syros_country.py --check
    python tools/directory_syros_country.py --check-live
    python tools/directory_syros_country.py --dump
"""

import argparse
from collections import Counter, defaultdict
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
PARENT = "gr-syros"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "syros_country.json"
)
REGULATION_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/"
    "2020_septembrios.pdf"
)
PROFILE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/syrou-tenou-androu-keas-kai-melou"
)

ISLAND_PAGES = {
    "Syros": "https://www.imsyrou.gr/index.php/el/nisia/nisos-syros",
    "Tinos": "https://www.imsyrou.gr/index.php/el/nisia/iera-nisos-tinos",
    "Andros": "https://www.imsyrou.gr/index.php/el/nisia/nisos-andros",
    "Mykonos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-mykonos",
    "Kea": "https://www.imsyrou.gr/index.php/el/nisia/nisos-kea",
    "Kythnos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-kythnos",
    "Serifos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-serifos",
    "Sifnos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-sifnos",
    "Milos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-milos",
    "Kimolos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-kimolos",
    "Folegandros": (
        "https://www.imsyrou.gr/index.php/el/nisia/nisos-folegandros"
    ),
    "Sikinos": "https://www.imsyrou.gr/index.php/el/nisia/nisos-sikinos",
}

ATHANASIUS = (
    "https://www.imsyrou.gr/index.php/el/?view=article&"
    "id=3237:2010-08-29-14-54-58&catid=162"
)
HOLY_TRINITY_METOCHION = (
    "https://www.imsyrou.gr/index.php/el/?view=article&"
    "id=3240:2010-08-29-15-06-28&catid=162"
)
SAINT_DEMETRIUS = (
    "https://www.imsyrou.gr/index.php/el/?view=article&"
    "id=3246:2010-08-29-15-39-56&catid=162"
)
SAINT_SPYRIDON = (
    "https://www.imsyrou.gr/index.php/el/?view=article&"
    "id=3254:2010-08-29-16-08-43&catid=162"
)
PARKIA = (
    "https://www.imsyrou.gr/index.php/el/?view=article&"
    "id=3284:ieros-naos-tou-agiou-ioannou-tis-parkias&catid=166"
)
SAINT_IRENE_CURRENT = (
    "https://www.imsyrou.gr/index.php/el/eidiseis-ieras-mitropoleos/"
    "eidiseis/arxeio-eidiseon-2025/"
    "arxieratikos-esperinos-stin-iera-moni-agias-eirinis-"
    "sta-apoikia-tis-androu"
)
SAINT_IRENE_SITE = "https://ierosnaosagiaseirinisandrou.gr/"
SAINT_IRENE_CONTACT = (
    "https://ierosnaosagiaseirinisandrou.gr/en/contact/"
)
PANACHRANTOU_SITE = "https://panachrantouandros.com/"
PANACHRANTOU_CONTACT = (
    "https://panachrantouandros.com/"
    "%CE%B5%CF%80%CE%B9%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CE%BD%CE%AF%CE%B1/"
)
KAPOULIS_DISSOLVED = (
    "https://www.imsyrou.gr/index.php/el/?view=article&"
    "id=3297:genesiplakes&catid=167"
)

SOURCE_KEYS = {
    "regulation": REGULATION_PDF,
    "profile": PROFILE,
    "syros": ISLAND_PAGES["Syros"],
    "tinos": ISLAND_PAGES["Tinos"],
    "andros": ISLAND_PAGES["Andros"],
    "mykonos": ISLAND_PAGES["Mykonos"],
    "kea": ISLAND_PAGES["Kea"],
    "kythnos": ISLAND_PAGES["Kythnos"],
    "serifos": ISLAND_PAGES["Serifos"],
    "sifnos": ISLAND_PAGES["Sifnos"],
    "milos": ISLAND_PAGES["Milos"],
    "kimolos": ISLAND_PAGES["Kimolos"],
    "folegandros": ISLAND_PAGES["Folegandros"],
    "sikinos": ISLAND_PAGES["Sikinos"],
    "panachrantou": PANACHRANTOU_CONTACT,
    "irene_current": SAINT_IRENE_CURRENT,
    "irene_contact": SAINT_IRENE_CONTACT,
}

ISLAND_LOCAL = {
    "Syros": "Σύρου",
    "Tinos": "Τήνου",
    "Andros": "Άνδρου",
    "Mykonos": "Μυκόνου",
    "Kea": "Κέας",
    "Kythnos": "Κύθνου",
    "Serifos": "Σερίφου",
    "Sifnos": "Σίφνου",
    "Milos": "Μήλου",
    "Kimolos": "Κιμώλου",
    "Folegandros": "Φολεγάνδρου",
    "Sikinos": "Σικίνου",
}

# Island | English seat | Greek legal seat | Greek legal dedication |
# English dedication | rank | current public body phones | direct body site |
# exact current island-page row.
PARISH_SOURCE = r'''
Syros|Ermoupoli|Ερμούπολις|Μεταμορφώσεως του Σωτήρος|the Transfiguration of the Savior|Metropolitan Church|2281082467||1
Syros|Ermoupoli|Ερμούπολις|Αναστάσεως Χριστού|the Resurrection of Christ|Parish Church|2281082998||1
Syros|Ermoupoli|Ερμούπολις|Αγίου Γεωργίου (Κοιμητηριακός)|Saint George|Cemetery Parish Church|2281082635||1
Syros|Ermoupoli|Ερμούπολις|Αγίου Κωνσταντίνου|Saint Constantine|Parish Church|2281080600||1
Syros|Ermoupoli|Ερμούπολις|Αγίου Νικολάου (Πολιούχος)|Saint Nicholas the Patron|Parish Church|2281082623,2281082537||1
Syros|Ermoupoli|Ερμούπολις|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2281082204,2281088964||1
Syros|Ermoupoli|Ερμούπολις|Ταξιαρχών|the Holy Archangels|Parish Church|2281080780||1
Syros|Ermoupoli|Ερμούπολις|Αγίου Νικολάου των Πτωχών|Saint Nicholas of the Poor|Parish Church|||1
Syros|Episkopeion|Επισκοπείον|Προφήτου Ηλιού|Prophet Elijah|Parish Church|2281081406||1
Syros|Manna|Μάννα|Αγίων Αναργύρων|the Holy Unmercenaries|Parish Church|2281080702||1
Syros|Parakopi|Παρακοπή|Τιμίου Σταυρού|the Holy Cross|Parish Church|2281042645||1
Syros|Poseidonia|Ποσειδωνία|Τιμίου Προδρόμου|Saint John the Forerunner|Parish Church|2281042206||1
Syros|Chroussa|Χρούσσα|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Parish Church|2281062216||1
Tinos|Tinos|Τήνος|Παμμεγίστων Ταξιαρχών|the Holy Archangels|Metropolitan Church|2283022861||1
Tinos|Tinos|Τήνος|Αγίου Νικολάου και Αγίου Ελευθερίου|Saint Nicholas and Saint Eleftherios|Parish Church|2283022108,2283022400||1
Tinos|Tinos|Τήνος|Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2283023336||1
Tinos|Tinos|Τήνος|Τριών Ιεραρχών και Αγίου Ιωάννου|the Three Holy Hierarchs and Saint John|Parish Church|2283023679||1
Tinos|Arnados|Αρνάδος|Αναλήψεως του Κυρίου|the Ascension of the Lord|Parish Church|2283031000||1
Tinos|Dyo Choria|Δύο Χωρία|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2283025020||1
Tinos|Kardiani|Καρδιανή|Αγίας Τριάδος|the Holy Trinity|Parish Church|||1
Tinos|Ktikados|Κτικάδος|Υπαπαντής του Κυρίου|the Presentation of the Lord|Parish Church|2283022156||1
Tinos|Marlas and Mamados|Μαρλάς και Μαμάδος|Αγίων Αναργύρων Μαρλά και Μεταμορφώσεως του Σωτήρος Μαμάδου|the Holy Unmercenaries at Marlas and the Transfiguration of the Savior at Mamados|Parish Church|||1
Tinos|Mountados|Μουντάδος|Αγίου Ιωάννου|Saint John|Parish Church|2283024977||1
Tinos|Plateia|Πλατεία|Γενεθλίου της Θεοτόκου|the Nativity of the Theotokos|Parish Church|2283022559||1
Tinos|Pyrgos|Πύργος|Αγίου Νικολάου|Saint Nicholas|Parish Church|2283025325||1
Tinos|Pyrgos|Πύργος|Αγίου Δημητρίου|Saint Demetrius|Parish Church|2283031209||1
Tinos|Sklavochorion|Σκλαβοχώριον|Αγίας Τριάδος|the Holy Trinity|Parish Church|||1
Tinos|Triantaros|Τριαντάρος|Αγίων Αποστόλων|the Holy Apostles|Parish Church|2283041357||1
Tinos|Tripotamos|Τριπόταμος|Εισοδίων της Θεοτόκου|the Entrance of the Theotokos|Parish Church|2283022083||1
Tinos|Ysternia|Υστέρνια|Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2283031100||1
Tinos|Falatados|Φαλατάδος|Αγίας Τριάδος|the Holy Trinity|Parish Church|2283041347||1
Tinos|Hatzirados|Χατζηράδος|Αγίας Τριάδος|the Holy Trinity|Parish Church|2283022233||1
Tinos|Steni|Στενή|Αγίου Αντωνίου|Saint Anthony|Parish Church|2283041990||1
Andros|Andros|Άνδρος|Αγίου Γεωργίου|Saint George|Metropolitan Church|2282023223||1
Andros|Andros|Άνδρος|Παναγίας Θεοσκεπάστου|Panagia Theoskepasti|Parish Church|2282041980,2282022433|https://www.theoskepasti.gr|1
Andros|Andros|Άνδρος|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2282051370||1
Andros|Aladinou|Αλαδινού|Αγίας Τριάδος|the Holy Trinity|Parish Church|2282051402,2282024074||1
Andros|Apoikia|Αποίκια|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Parish Church|||1
Andros|Apoikia|Αποίκια|Κοιμήσεως Θεοτόκου Κατασύρτη|the Dormition of the Theotokos at Katasyritis|Parish Church|2282022190,2282022603||1
Andros|Vrachnou|Βραχνού|Αγίου Δημητρίου|Saint Demetrius|Parish Church|||1
Andros|Vourkoti|Βουρκωτή|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2282024532,2282023800||1
Andros|Zaganiarion|Ζαγανιάριον|Αγίου Νικολάου|Saint Nicholas|Parish Church|||1
Andros|Koureleion|Κουρέλιον|Αγίου Νικολάου|Saint Nicholas|Parish Church|||1
Andros|Lamyra|Λάμυρα|Μεταμορφώσεως του Σωτήρος|the Transfiguration of the Savior|Parish Church|||1
Andros|Livadia|Λιβάδια|Αγίου Κωνσταντίνου|Saint Constantine|Parish Church|2282022611,2282024955||1
Andros|Menites|Μενήτες|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2282051630||1
Andros|Mesathourion|Μεσαθούριον|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|||1
Andros|Mesaria|Μεσαριά|Αγίου Νικολάου|Saint Nicholas|Parish Church|||1
Andros|Pitrofos|Πιτροφός|Αγίου Παντελεήμονος|Saint Panteleimon|Parish Church|2282051141||1
Andros|Pitrofos|Πιτροφός|Τιμίου Σταυρού|the Holy Cross|Parish Church|||1
Andros|Sassa|Σάσσα|Αγίου Σάββα|Saint Sabbas|Parish Church|||1
Andros|Stenies|Στενιές|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2282023963,2282023089||1
Andros|Stenies|Στενιές|Αγίου Γεωργίου|Saint George|Parish Church|||1
Andros|Stratouriai|Στρατουργιαί|Αγίου Παντελεήμονος|Saint Panteleimon|Parish Church|||1
Andros|Synetion|Συνέτιον|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|||1
Andros|Ypsilou|Υψηλού|Ταξιαρχών|the Holy Archangels|Parish Church|||1
Andros|Fallika|Φάλλικα|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Parish Church|2282051131||1
Andros|Ormos Korthiou|Όρμος Κορθίου|Αγίου Νικολάου|Saint Nicholas|Parish Church|2282061193||1
Andros|Agia Marina|Αγία Μαρίνα|Αγίας Μαρίνης|Saint Marina|Parish Church|||1
Andros|Alamania|Αλαμανιά|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Parish Church|||1
Andros|Aidonia|Αηδόνια|Αγίων Πάντων|All Saints|Parish Church|2282061919||1
Andros|Amonakliou|Αμονακλίου|Αγίου Παντελεήμονος|Saint Panteleimon|Parish Church|2282024594||1
Andros|Ano Korthion|Άνω Κόρθιον|Αγίου Γεωργίου|Saint George|Parish Church|||1
Andros|Aypatia|Αϋπάτια|Αγίας Άννης|Saint Anna|Parish Church|||1
Andros|Exo Vounion|Βούνιον Έξω|Αγίας Παρασκευής|Saint Paraskevi|Parish Church|||1
Andros|Mesa Vounion|Βούνιον Μέσα|Εισοδίων Θεοτόκου|the Entrance of the Theotokos|Parish Church|||1
Andros|Giannisaion|Γιαννησαίον|Εισοδίων Θεοτόκου|the Entrance of the Theotokos|Parish Church|2282061670||1
Andros|Episkopeion|Επισκοπείον|Ζωοδόχου Πηγής|the Life-giving Spring|Parish Church|||1
Andros|Kapparia|Καππαριά|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2282061580||1
Andros|Kochylou|Κοχύλου|Αγίου Γεωργίου|Saint George|Parish Church|||1
Andros|Lardia|Λαρδιά|Μεταμορφώσεως του Σωτήρος|the Transfiguration of the Savior|Parish Church|||1
Andros|Morakaion|Μωρακαίων|Γεννήσεως του Χριστού|the Nativity of Christ|Parish Church|||1
Andros|Piso Meria|Πίσω Μεριά|Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2282062165||1
Andros|Rogon|Ρωγών|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|||1
Andros|Chonai|Χώναι|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Parish Church|||1
Andros|Batsi|Μπατσίον|Αγίου Φιλίππου|Saint Philip|Parish Church|2282071880,2282041449||1
Andros|Agios Petros|Άγιος Πέτρος|Αγίου Πέτρου|Saint Peter|Parish Church|||1
Andros|Ammolochos|Αμμόλοχος|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|||1
Andros|Ano Gavrion|Άνω Γαύριον|Αγίας Σοφίας|Saint Sophia|Parish Church|||1
Andros|Aprovatos|Απρόβατος|Αγίου Δημητρίου|Saint Demetrius|Parish Church|2282051496||1
Andros|Aprovatos|Απρόβατος|Αγίου Αντωνίου|Saint Anthony|Parish Church|||1
Andros|Arni, Mpaleoi|Άρνη, Μπαλέοι|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|||1
Andros|Arni, Panochori|Άρνη, Πανωχώρι|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|||1
Andros|Varydion|Βαρύδιον|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2282072381||1
Andros|Vitalion|Βιτάλιον|Αγίας Σοφίας|Saint Sophia|Parish Church|||1
Andros|Gavrion|Γαύριον|Αγίου Νικολάου|Saint Nicholas|Parish Church|2282071111||1
Andros|Gides|Γίδες|Αγίου Νικολάου|Saint Nicholas|Parish Church|||1
Andros|Kalyvarion|Καλυβάριον|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Parish Church|||1
Andros|Katakoilos|Κατάκοιλος|Αγίου Ιωάννου Θεολόγου|Saint John the Theologian|Parish Church|2282042377||1
Andros|Mermygkies|Μερμυγκιές|Αγίας Μαρίνης|Saint Marina|Parish Church|||1
Andros|Palaiopoli|Παλαιόπολη|Αγίου Ιωάννου|Saint John|Parish Church|2282041588||1
Andros|Remata|Ρέματα|Ευαγγελιστρίας|the Annunciation of the Theotokos|Parish Church|||1
Andros|Sidontas|Σιδόντας|Αγίου Αντωνίου|Saint Anthony|Parish Church|||1
Andros|Fellos|Φελλός|Ευαγγελιστρίας|the Annunciation of the Theotokos|Parish Church|2282071497||1
Andros|Chartes|Χάρτες|Αγίας Μαύρας|Saint Mavra|Parish Church|||0
Mykonos|Mykonos|Μύκονος|Ζωοδόχου Πηγής|the Life-giving Spring|Metropolitan Church|2289026013,2289025282||1
Mykonos|Mykonos|Μύκονος|Αγίας Κυριακής|Saint Kyriaki|Parish Church|||1
Mykonos|Mykonos|Μύκονος|Παναχράντου|Panachrantos|Parish Church|2289024223||1
Mykonos|Ano Mera|Άνω Μερά|Αγίου Γεωργίου|Saint George|Parish Church|||1
Kea|Kea|Κέα|Ευαγγελισμού της Θεοτόκου|the Annunciation of the Theotokos|Metropolitan Church|2288022266||1
Kea|Kea|Κέα|Αγίου Δημητρίου|Saint Demetrius|Parish Church|2288022094||1
Kea|Kea|Κέα|Μεταμορφώσεως Σωτήρος|the Transfiguration of the Savior|Parish Church|2288022295||1
Kea|Korissia|Κορησσία|Αγίας Τριάδος|the Holy Trinity|Parish Church|2288021392||1
Kythnos|Dryopis|Δρυοπίς|Αγίων Αποστόλων|the Holy Apostles|Metropolitan Church|2281032155,2281032235,2281032828||1
Kythnos|Chora|Χώρα|Αγίας Τριάδος|the Holy Trinity|Parish Church|||1
Kythnos|Chora|Χώρα|Αγίου Ιωάννου Θεολόγου|Saint John the Theologian|Parish Church|2281031275||1
Serifos|Serifos|Σέριφος|Αγίου Αθανασίου|Saint Athanasius|Metropolitan Church|2281051221||1
Serifos|Megalo Livadi|Μεγάλο Λιβάδιον|Αγίου Νικολάου|Saint Nicholas|Parish Church|||1
Serifos|Tria Choria|Τρία Χωρία|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2281051027||1
Serifos|Chora|Χώρα|Ευαγγελιστρίας|the Annunciation of the Theotokos|Parish Church|2281052547||1
Serifos|Kotala|Κούταλα|Αγίας Θεοδώρας|Saint Theodora|Parish Church|||0
Sifnos|Apollonia|Απολλωνία|Αγίου Σπυρίδωνος|Saint Spyridon|Metropolitan Church|2284031937||1
Sifnos|Artemon|Αρτεμών|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2284032032||1
Sifnos|Artemon|Αρτεμών|Ταξιάρχου|the Holy Archangel|Parish Church|2284031856||1
Sifnos|Exambela|Εξάμπελα|Αγίου Νικολάου|Saint Nicholas|Parish Church|2284033698||1
Sifnos|Kastron|Κάστρον|Αγίας Ελεούσης|Panagia Eleousa|Parish Church|2284033676||1
Sifnos|Katavati|Καταβατή|Αγίου Γεωργίου|Saint George|Parish Church|2284032168||1
Sifnos|Ano Petali|Άνω Πετάλι|Αγίου Ιωάννου|Saint John|Parish Church|||1
Sifnos|Kato Petali|Κάτω Πετάλι|Ζωοδόχου Πηγής|the Life-giving Spring|Parish Church|2284033338||1
Milos|Adamas|Αδάμας|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2287022279||1
Milos|Zefyria|Ζεφυρία|Κοιμήσεως Θεοτόκου|the Dormition of the Theotokos|Parish Church|2287031205||1
Milos|Plaka|Πλάκα|Γενεσίου Θεοτόκου|the Nativity of the Theotokos|Metropolitan Church|2287021180||1
Milos|Plakes|Πλάκες|Αγίου Χαραλάμπους|Saint Charalampus|Parish Church|||1
Milos|Triovasalos|Τριοβάσαλον|Αγίου Σπυρίδωνος|Saint Spyridon|Parish Church|2287021505||1
Milos|Pera Triovasalos|Πέραν Τριοβασάλου|Αγίου Γεωργίου|Saint George|Parish Church|||1
Milos|Trypiti|Τρυπητή|Αγίου Νικολάου|Saint Nicholas|Parish Church|2287021676||1
Milos|Pollonia|Πολλώνια|Αγίας Παρασκευής|Saint Paraskevi|Parish Church|2287041344||1
Kimolos|Kimolos|Κίμωλος|Εισοδίων Θεοτόκου|the Entrance of the Theotokos|Metropolitan Church|2287051028||1
Folegandros|Ano Meria|Άνω Μεριά|Αγίου Γεωργίου|Saint George|Parish Church|2286041326||1
Folegandros|Chora|Χώρα|Αγίου Νικολάου|Saint Nicholas|Metropolitan Church|2286041324||1
Sikinos|Sikinos|Σίκινος|Τιμίου Σταυρού|the Holy Cross|Metropolitan Church|2286051267||1
Sikinos|Sikinos|Σίκινος|Αγίου Βασιλείου|Saint Basil|Parish Church|2286051026||1
'''

# Greek current identity | English name | seat | island | address parts |
# phones | emails | body site | identity source keys | contact source keys.
MONASTERY_SOURCE = r'''
Ιερά Μονή Παναγίας Παναχράντου και Αγίου Παντελεήμονος Άνδρου|Monastery of Panagia Panachrantou and Saint Panteleimon, Andros|Fallika|Andros|Fallika;84500;Andros;Greece|2282051090|impanahrantou@gmail.com|https://panachrantouandros.com/|profile,panachrantou|profile,panachrantou
Ιερά Μονή Αγίου Νικολάου του εν Βουνένοις Άνδρου|Monastery of Saint Nicholas of Vounena, Andros|Andros|Andros|Andros;Greece|2282022190|||profile|profile
Ιερά Μονή Αγίας Μαρίνας Άνδρου|Monastery of Saint Marina, Andros|Andros|Andros|Andros;Greece|2282024074|||profile|profile
Ιερά Μονή Θεοτόκου Βρύσεως Σίφνου|Monastery of the Theotokos at Vrysi, Sifnos|Vrysi|Sifnos|Vrysi;Sifnos;Greece|2284031937|||profile,sifnos|profile,sifnos
Ιερά Μονή Παμμεγίστων Ταξιαρχών Σερίφου|Monastery of the Holy Archangels, Serifos|Serifos|Serifos|Serifos;Greece|2281051027|||profile,serifos|profile,serifos
Ιερά Μονή Παναγίας Τουρλιανής Μυκόνου|Monastery of Panagia Tourliani, Mykonos|Ano Mera|Mykonos|Ano Mera;84600;Mykonos;Greece|2289071249|||profile,mykonos|profile,mykonos
Ιερά Μονή Αγίου Ιωάννου Ταλάντων Σύρου|Monastery of Saint John at Talanta, Syros|Talanta|Syros|Talanta;84100;Syros;Greece|2281088655|||profile|profile
Ιερά Μονή Κοιμήσεως Θεοτόκου Κεχροβουνίου Τήνου|Monastery of the Dormition of the Theotokos at Kechrovouni, Tinos|Kechrovouni|Tinos|Kechrovouni;84200;Tinos;Greece|2283041218|||profile|profile
Ιερά Μονή Ζωοδόχου Πηγής Αγίας Άνδρου|Monastery of the Life-giving Spring, Agia, Andros|Agia|Andros|Agia;Andros;Greece|2282072459|||profile|profile
Ιερά Μονή Αγίας Βαρβάρας Σύρου|Monastery of Saint Barbara, Syros|Kini|Syros|Kini;84100;Syros;Greece|2281071250|||profile,syros|profile,syros
Ιερά Μονή Κοιμήσεως Θεοτόκου Παλαιοκάστρου Μυκόνου|Monastery of the Dormition of the Theotokos at Palaiokastro, Mykonos|Ano Mera|Mykonos|Palaiokastro;Ano Mera;84600;Mykonos;Greece||||profile,mykonos|
Ιερά Μονή Παναγίας Χρυσοπηγής Σικίνου|Monastery of Panagia Chrysopigi, Sikinos|Sikinos|Sikinos|Sikinos;Greece||||profile|
'''

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imsyrou.gr",
    "www.imsyrou.gr",
    "theoskepasti.gr",
    "www.theoskepasti.gr",
    "panachrantouandros.com",
    "www.panachrantouandros.com",
    "ierosnaosagiaseirinisandrou.gr",
    "www.ierosnaosagiaseirinisandrou.gr",
    "panagiatinou.gr",
    "www.panagiatinou.gr",
}

EXPECTED_TOTAL = 154
EXPECTED_LEGAL_ISLAND_COUNTS = {
    "Andros": 62,
    "Folegandros": 2,
    "Kea": 4,
    "Kimolos": 1,
    "Kythnos": 3,
    "Milos": 8,
    "Mykonos": 4,
    "Serifos": 5,
    "Sifnos": 8,
    "Sikinos": 2,
    "Syros": 13,
    "Tinos": 20,
}
EXPECTED_KINDS = {"monastery": 12, "parish": 142}
EXPECTED_RANKS = {
    "Cemetery Parish Church": 1,
    "Church": 1,
    "Country Chapel": 1,
    "Dependent Church": 2,
    "Former Monastery Church": 1,
    "Metropolitan Church": 12,
    "Monastery": 12,
    "Monastic Metochion": 1,
    "Parish Church": 119,
    "Pilgrimage Church": 4,
}
EXPECTED_PHONE_BODIES = 93
EXPECTED_PHONE_VALUES = 107
EXPECTED_EMAIL_BODIES = 2
EXPECTED_EMAIL_VALUES = 2
EXPECTED_SITE_BODIES = 3
EXPECTED_CONTACT_BODIES = 93
EXPECTED_LIVE_SOURCES = 23


def unicase(value):
    value = unicodedata.normalize("NFD", value)
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    ).casefold()


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(key)
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("%s carries a non-HTTP URL" % label)
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("%s carries an unapproved host: %s" %
                         (label, parsed.hostname))


def source_urls(raw):
    if not raw:
        return []
    return [SOURCE_KEYS[key] for key in raw.split(",")]


def build_rows():
    rows = []
    legal_counts = defaultdict(int)
    for number, raw in enumerate(PARISH_SOURCE.strip().splitlines(), 1):
        (
            island, seat, seat_local, dedication_local, dedication,
            rank, raw_phones, site, current,
        ) = raw.split("|", 8)
        legal_counts[island] += 1
        local = "%s - %s" % (seat_local, dedication_local)
        if rank == "Metropolitan Church":
            local += " (Μητροπολιτικός)"
        sources = [REGULATION_PDF]
        if current == "1":
            sources.append(ISLAND_PAGES[island])
        phones = raw_phones.split(",") if raw_phones else []
        row = {
            "id": "gr-syros-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s of %s in %s, %s" %
                    (rank, dedication, seat, island),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, island, "Greece"],
            "sources": sources,
            "checked": CHECKED,
        }
        if phones:
            row["phones"] = phones
            row["contact_sources"] = [ISLAND_PAGES[island]]
            row["contact_checked"] = CHECKED
        if site:
            row["site"] = site
            row["contact_sources"] = [ISLAND_PAGES[island]]
            row["contact_checked"] = CHECKED
        rows.append(row)
    if dict(sorted(legal_counts.items())) != EXPECTED_LEGAL_ISLAND_COUNTS:
        raise ValueError("legal island totals drifted: %r" % legal_counts)

    pilgrimages = [
        (
            "Pilgrimage Church of Panagia Thalassini and Saint Anthony "
            "at Megas Gialos, Syros",
            "Ιερό Προσκύνημα Παναγίας Θαλασσινής και Αγίου Αντωνίου "
            "Μεγάλου Γιαλού Σύρου",
            "Megas Gialos", ["Megas Gialos", "Syros", "Greece"],
        ),
        (
            "Pilgrimage Church of Panagia Kanala, Kythnos",
            "Ιερό Προσκύνημα Παναγίας Κανάλας Κύθνου",
            "Kanala", ["Kanala", "Kythnos", "Greece"],
        ),
        (
            "Pilgrimage Church of Panagia Vounou, Sifnos",
            "Ιερό Προσκύνημα Παναγίας Βουνού Σίφνου",
            "Vouno", ["Vouno", "Sifnos", "Greece"],
        ),
        (
            "Pilgrimage Church of the Catacombs of Milos",
            "Ιερό Προσκύνημα Κατακομβών Νήσου Μήλου",
            "Milos Catacombs", ["Catacombs", "Milos", "Greece"],
        ),
    ]
    for number, (name, local, seat, address) in enumerate(pilgrimages, 133):
        rows.append({
            "id": "gr-syros-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": address,
            "sources": [REGULATION_PDF],
            "checked": CHECKED,
        })

    for number, raw in enumerate(MONASTERY_SOURCE.strip().splitlines(), 137):
        (
            local, name, seat, island, raw_address, raw_phones,
            raw_emails, site, raw_sources, raw_contact_sources,
        ) = raw.split("|", 9)
        row = {
            "id": "gr-syros-%03d" % number,
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": raw_address.split(";"),
            "sources": source_urls(raw_sources),
            "checked": CHECKED,
        }
        if raw_phones:
            row["phones"] = raw_phones.split(",")
        if raw_emails:
            row["emails"] = raw_emails.split(",")
        if site:
            row["site"] = site
        contact_sources = source_urls(raw_contact_sources)
        if contact_sources:
            row["contact_sources"] = contact_sources
            row["contact_checked"] = CHECKED
        rows.append(row)

    rows.extend([
        {
            "id": "gr-syros-149",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Country Chapel",
            "name": (
                "Country Chapel of Saint Athanasius at Pigi, Ano Syros"
            ),
            "local": "Εξωκκλήσιο Αγίου Αθανασίου στην Πηγή Άνω Σύρου",
            "seat": "Pigi, Ano Syros",
            "country": "GR",
            "address": ["Pigi", "Ano Syros", "Syros", "Greece"],
            "sources": [ISLAND_PAGES["Syros"], ATHANASIUS],
            "checked": CHECKED,
        },
        {
            "id": "gr-syros-150",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Monastic Metochion",
            "name": (
                "Holy Trinity Metochion of the Monastery of Saint John "
                "at Talanta, Ano Syros"
            ),
            "local": (
                "Μετόχιο Αγίας Τριάδος Άνω Σύρου της Ιεράς Μονής "
                "Αγίου Ιωάννου Ταλάντων"
            ),
            "seat": "Ano Syros",
            "country": "GR",
            "address": ["Ano Syros", "Syros", "Greece"],
            "sources": [ISLAND_PAGES["Syros"], HOLY_TRINITY_METOCHION],
            "checked": CHECKED,
        },
        {
            "id": "gr-syros-151",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Dependent Church",
            "name": (
                "Dependent Church of Saint Demetrius at Vaporia, "
                "Ermoupoli"
            ),
            "local": (
                "Ιερός Ναός Αγίου Δημητρίου Βαπορίων, υπαγόμενος στην "
                "Ενορία Αγίου Νικολάου"
            ),
            "seat": "Vaporia, Ermoupoli",
            "country": "GR",
            "address": ["Vaporia", "Ermoupoli", "Syros", "Greece"],
            "sources": [ISLAND_PAGES["Syros"], SAINT_DEMETRIUS],
            "checked": CHECKED,
        },
        {
            "id": "gr-syros-152",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Church",
            "name": "Church of Saint Spyridon in Chroussa, Syros",
            "local": "Ιερός Ναός Αγίου Σπυρίδωνος Χρουσσών Σύρου",
            "seat": "Chroussa",
            "country": "GR",
            "address": ["Chroussa", "Syros", "Greece"],
            "sources": [ISLAND_PAGES["Syros"], SAINT_SPYRIDON],
            "checked": CHECKED,
        },
        {
            "id": "gr-syros-153",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Dependent Church",
            "name": (
                "Dependent Church of Saint John the Forerunner at Parkia, "
                "Mykonos"
            ),
            "local": (
                "Ιερός Ναός Αγίου Ιωάννου του Προδρόμου της Παρκιάς "
                "Μυκόνου"
            ),
            "seat": "Parkia, Mykonos",
            "country": "GR",
            "address": ["Parkia", "Mykonos", "Greece"],
            "sources": [ISLAND_PAGES["Mykonos"], PARKIA],
            "checked": CHECKED,
        },
        {
            "id": "gr-syros-154",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Former Monastery Church",
            "name": (
                "Former Monastery Church of Saint Irene and Venerable "
                "Irene Chrysovalantou in Apoikia, Andros"
            ),
            "local": (
                "Ιερός Ναός Αγίας Μεγαλομάρτυρος Ειρήνης και Οσίας "
                "Ειρήνης Χρυσοβαλάντου Αποικίων Άνδρου"
            ),
            "seat": "Apoikia",
            "country": "GR",
            "address": [
                "Moni Agias Eirinis", "Apoikia", "84500", "Andros",
                "Greece",
            ],
            "phones": ["6942957661", "6976493470"],
            "emails": ["info@ierosnaosagiaseirinisandrou.gr"],
            "site": SAINT_IRENE_SITE,
            "sources": [SAINT_IRENE_CURRENT, SAINT_IRENE_CONTACT],
            "checked": CHECKED,
            "contact_sources": [SAINT_IRENE_CONTACT],
            "contact_checked": CHECKED,
        },
    ])
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

LIVE_CHECKS = {
    ISLAND_PAGES["Syros"]: {
        "Μεταμόρφωσις του Σωτήρος",
        "Αγ. Νικόλαος των",
        "Αγ. Σπυρίδωνας",
        "22810",
    },
    ISLAND_PAGES["Tinos"]: {
        "Ταξιάρχες",
        "Μαρλά",
        "Υστέρνια",
        "22830",
    },
    ISLAND_PAGES["Andros"]: {
        "Παναγίας Θεοσκεπάστου",
        "Ευαγγελισμός Θεοτόκου",
        "Φελλός",
        "71497",
    },
    ISLAND_PAGES["Mykonos"]: {
        "Ιερός Ναός του Αγίου Ιωάννου της Παρκιάς",
        "Θεοτόκου Τουρλιανής",
        "71249",
    },
    ISLAND_PAGES["Kea"]: {
        "Ευαγγελισμός Θεοτόκου",
        "Κορησσία",
        "21392",
    },
    ISLAND_PAGES["Kythnos"]: {
        "Αγ. Άννα",
        "Αγ. Ιωάννης",
        "32828",
    },
    ISLAND_PAGES["Serifos"]: {
        "Αγ. Αθανάσιος",
        "Ιερά Μονή Παμμεγίστων Ταξιαρχών",
        "51027",
    },
    ISLAND_PAGES["Sifnos"]: {
        "Αγ. Σπυρίδων",
        "Ιερά Μονή Θεοτόκου",
        "31937",
    },
    ISLAND_PAGES["Milos"]: {
        "Κοίμηση Θεοτόκου",
        "Πολώνια",
        "41344",
    },
    ISLAND_PAGES["Kimolos"]: {"Εισ. Θεοτόκου", "51028"},
    ISLAND_PAGES["Folegandros"]: {"Άνω Μεριά", "41326", "41324"},
    ISLAND_PAGES["Sikinos"]: {"Τιμ. Σταυρός", "51026"},
    PROFILE: {
        "Παναχράντου Άνδρου",
        "Αγ. Νικολάου Άνδρου",
        "Αγ. Γεωργίου του Καπούλη",
        "Χρυσοπηγής Σικίνου",
        "22820-51090",
    },
    ATHANASIUS: {"εξωκκλήσι του Αγίου Αθανασίου"},
    HOLY_TRINITY_METOCHION: {"Μετόχι της Μονής Ταλάντων Σύρου"},
    SAINT_DEMETRIUS: {"Υπάγεται στην ενορία του Αγίου Νικολάου"},
    SAINT_SPYRIDON: {"πευκόφυτο θέρετρο των Χρουσσών"},
    PARKIA: {"ήρθε στην πνευματική δικαιοδοσία"},
    SAINT_IRENE_CURRENT: {
        "Ιεράς Μονής Αγίας Ειρήνης Αποικίων Άνδρου",
    },
    SAINT_IRENE_CONTACT: {
        "697 6493470",
        "info@ierosnaosagiaseirinisandrou.gr",
    },
    PANACHRANTOU_CONTACT: {
        "2282051090",
        "impanahrantou@gmail.com",
    },
    KAPOULIS_DISSOLVED: {
        "διαλυθέντα μοναστήρια της Αγίας Μαρίνας και του Αγίου "
        "Γεωργίου του Καπούλη",
    },
}


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Syros candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Syros candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "regulated_parish_rows": 132,
        "regulated_pilgrimage_rows": 4,
        "current_monastic_rows": 12,
        "current_island_page_extra_rows": 5,
        "current_former_monastery_church_rows": 1,
        "parish_kind_rows": 142,
        "monastery_kind_rows": 12,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "fax_bodies": 0,
        "public_fax_values": 0,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_TOTAL,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Syros ledger summary drifted")
    for key in (
            "candidates", "source_reconciliations",
            "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Syros ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Syros ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    for source in ROWS:
        item = {
            key: value for key, value in source.items()
            if value not in (None, "", [])
        }
        row_id = item.get("id")
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") != PARENT or item.get("country") != "GR":
            raise ValueError("%s has the wrong parent or country" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(value)
               for value in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        sources = list(item.get("sources") or [])
        if not sources or len(sources) > 3:
            raise ValueError("%s lacks valid sources" % row_id)
        for source_url in sources:
            validate_url(source_url, row_id)
        item["sources"] = sources
        item["cite"] = list(sources)
        contact_sources = list(item.get("contact_sources") or [])
        has_contact = bool(
            item.get("phones") or item.get("faxes") or
            item.get("emails") or item.get("site")
        )
        if has_contact:
            if not contact_sources or item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            for phone in (item.get("phones") or []) + (item.get("faxes") or []):
                if not re.fullmatch(r"[26]\d{9}", phone):
                    raise ValueError("%s carries an invalid phone or fax" % row_id)
            for email in item.get("emails") or []:
                if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                    raise ValueError("%s carries an invalid email" % row_id)
            if item.get("site"):
                validate_url(item["site"], row_id)
            for source_url in contact_sources:
                validate_url(source_url, row_id)
                if source_url not in sources:
                    raise ValueError("contact source is outside identity sources")
        elif contact_sources or "contact_checked" in item:
            raise ValueError(
                "%s carries contact provenance without contact data" % row_id
            )
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Syros English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Syros rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Syros kind totals drifted: %r" % dict(kinds))
    phone_bodies = sum(bool(item.get("phones")) for item in result)
    phone_values = sum(len(item.get("phones") or []) for item in result)
    fax_bodies = sum(bool(item.get("faxes")) for item in result)
    fax_values = sum(len(item.get("faxes") or []) for item in result)
    email_bodies = sum(bool(item.get("emails")) for item in result)
    email_values = sum(len(item.get("emails") or []) for item in result)
    site_bodies = sum(bool(item.get("site")) for item in result)
    contact_bodies = sum(bool(
        item.get("phones") or item.get("faxes") or
        item.get("emails") or item.get("site")
    ) for item in result)
    if (phone_bodies, phone_values) != (
            EXPECTED_PHONE_BODIES, EXPECTED_PHONE_VALUES):
        raise ValueError(
            "Syros phone coverage drifted: %r" %
            ((phone_bodies, phone_values),)
        )
    if (fax_bodies, fax_values) != (0, 0):
        raise ValueError("Syros fax coverage drifted")
    if (email_bodies, email_values, site_bodies, contact_bodies) != (
            EXPECTED_EMAIL_BODIES, EXPECTED_EMAIL_VALUES,
            EXPECTED_SITE_BODIES, EXPECTED_CONTACT_BODIES):
        raise ValueError(
            "Syros contact coverage drifted: %r" %
            ((email_bodies, email_values, site_bodies, contact_bodies),)
        )
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    }
    if url == REGULATION_PDF:
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=90) as response:
        payload = response.read(4096 if url == REGULATION_PDF else -1)
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return unicase(" ".join(text.split()))


def check_live():
    checks = dict(LIVE_CHECKS)
    checks[REGULATION_PDF] = set()

    def one(item):
        url, markers = item
        payload, content_type = fetch(url)
        if url == REGULATION_PDF:
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("Syros legal source is not a PDF")
            return url
        if "html" not in content_type:
            raise ValueError("non-HTML Syros source: %s" % url)
        page = normalized_page(payload)
        missing = [marker for marker in markers
                   if unicase(" ".join(marker.split())) not in page]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        return url

    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(one, checks.items()))
    if len(checks) != EXPECTED_LIVE_SOURCES:
        raise ValueError("Syros live source count drifted")
    return len(checks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        data = build()
        if args.check_live:
            checked = check_live()
            print("Syros live checks passed for %d source pages" % checked)
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Syros checks passed: %d bodies, %d phone bodies, "
                "%d email bodies, %d body sites" % (
                    len(rows),
                    sum(bool(item.get("phones")) for item in rows),
                    sum(bool(item.get("emails")) for item in rows),
                    sum(bool(item.get("site")) for item in rows),
                )
            )
    except Exception as exc:
        print("Syros check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
