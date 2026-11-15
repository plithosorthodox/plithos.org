#!/usr/bin/env python3
"""Build the exact current Florina, Prespes and Eordaia body roster."""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PARENT = "ep-phlorina"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "phlorina_country.json"

LOCAL_BASE = "https://imflorinas.gr"
LOCAL_PARISH_URL = LOCAL_BASE + "/enories/"
LOCAL_MONASTERY_URL = LOCAL_BASE + "/mones/"
LOCAL_CLERGY_URL = LOCAL_BASE + "/klhrikoi/"
LOCAL_CLERGY_PAGE_2 = LOCAL_BASE + "/klhrikoi/page/2/"
EP_URL = "https://ec-patr.org/entities/iera-mitropoli-florinis-prespon-eordaias/"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2019_decembrios.pdf"

PARISH_SOURCE = r"""
Florina|Florina|Φλώρινα|Saint Panteleimon|Αγίου Παντελεήμονος|Metropolitan Cathedral
Florina|Florina|Φλώρινα|Saint George|Αγίου Γεωργίου|Parish Church
Florina|Florina|Φλώρινα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
Florina|Florina|Φλώρινα|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Florina|Φλώρινα|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Florina|Agia Paraskevi|Αγία Παρασκευή|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
Florina|Agios Vartholomaios|Άγιος Βαρθολομαίος|Saint Bartholomew|Αγίου Βαρθολομαίου|Parish Church
Florina|Akritas|Ακρίτας|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Alona|Άλωνα|Saint Athanasius|Αγίου Αθανασίου|Parish Church
Florina|Ammochori|Αμμοχώρι|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Ano Kalliniki|Άνω Καλλινίκη|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Ano Kleines|Άνω Κλεινές|Holy Trinity|Αγίας Τριάδος|Parish Church
Florina|Ano Ydrousa|Άνω Υδρούσα|Saint Gregory the Theologian|Αγίου Γρηγορίου του Θεολόγου|Parish Church
Florina|Armenochori|Αρμενοχώρι|Venerable Naum|Οσίου Ναούμ|Parish Church
Florina|Atrapos|Ατραπός|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Achlada|Αχλάδα|Saint Spyridon|Αγίου Σπυρίδωνος|Parish Church
Florina|Vevi|Βεύη|Saint George|Αγίου Γεωργίου|Parish Church
Florina|Drosopigi|Δροσοπηγή|Holy Trinity|Αγίας Τριάδος|Parish Church
Florina|Ethniko|Εθνικό|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Itea|Ιτέα|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church
Florina|Kato Kalliniki|Κάτω Καλλινίκη|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Florina|Kato Kleines|Κάτω Κλεινές|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church
Florina|Kladorrachi|Κλαδορράχη|Saint Procopius|Αγίου Προκοπίου|Parish Church
Florina|Kolchiki|Κολχική|Saints Theodore|Αγίων Θεοδώρων|Parish Church
Florina|Kratero|Κρατερό|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Leptokaryai|Λεπτοκαρυές|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου|Parish Church
Florina|Lofoi|Λόφοι|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church
Florina|Marina|Μαρίνα|Saint Marina|Αγίας Μαρίνης|Parish Church
Florina|Meliti|Μελίτη|Saint Irene|Αγίας Ειρήνης|Parish Church
Florina|Mesokampos|Μεσόκαμπος|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church
Florina|Mesonisi|Μεσονήσι|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Mesochori|Μεσοχώρι|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Neos Kafkasos|Νέος Καύκασος|Saint George|Αγίου Γεωργίου|Parish Church
Florina|Neochoraki|Νεοχωράκι|Saint Athanasius|Αγίου Αθανασίου|Parish Church
Florina|Niki|Νίκη|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church
Florina|Palaistre|Παλαίστρα|Saint John the Theologian|Αγίου Ιωάννου του Θεολόγου|Parish Church
Florina|Papagiannis|Παπαγιάννης|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Parori|Παρόρι|Saints Cyricus and Julitta|Αγίων Κηρύκου και Ιουλίττης|Parish Church
Florina|Perasma|Πέρασμα|Holy Unmercenaries|Αγίων Αναργύρων|Parish Church
Florina|Polyplatanos|Πολυπλάτανος|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Polypotamos|Πολυπόταμος|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Proti|Πρώτη|Saint George|Αγίου Γεωργίου|Parish Church
Florina|S.S. Vevis|Σ.Σ. Βεύης|Saint Ignatius the God-bearer|Αγίου Ιγνατίου του Θεοφόρου|Parish Church
Florina|Sitaria|Σιταριά|Saint Athanasius|Αγίου Αθανασίου|Parish Church
Florina|Skopia|Σκοπιά|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Skopos|Σκοπός|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Florina|Triantafyllia|Τριανταφυλλιά|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
Florina|Trivouno|Τρίβουνο|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Tripotamos|Τριπόταμος|Saint George|Αγίου Γεωργίου|Parish Church
Florina|Tropaiouchos|Τροπαιούχος|Saint George|Αγίου Γεωργίου|Parish Church
Florina|Ydrousa|Υδρούσα|Saint Nicholas|Αγίου Νικολάου|Parish Church
Florina|Flampouro|Φλάμπουρο|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Prespes|Agios Achilleios|Άγιος Αχίλλειος|Saint Achilleios|Αγίου Αχιλλείου|Parish Church
Prespes|Agios Germanos|Άγιος Γερμανός|Saint Germanos|Αγίου Γερμανού|Parish Church
Prespes|Vrontero|Βροντερό|Saint Nicholas|Αγίου Νικολάου|Parish Church
Prespes|Kallithea|Καλλιθέα|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
Prespes|Karyes|Καρυές|Ascension of the Lord|Αναλήψεως του Κυρίου|Parish Church
Prespes|Laimos|Λαιμός|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
Prespes|Lefkon|Λευκώνας|Saint Andrew|Αγίου Ανδρέου|Parish Church
Prespes|Pisoderi|Πισοδέρι|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
Prespes|Mikrolimni|Μικρολίμνη|Saint Athanasius|Αγίου Αθανασίου|Parish Church
Prespes|Platy|Πλατύ|Saint George|Αγίου Γεωργίου|Parish Church
Prespes|Psarades|Ψαράδες|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Amyntaio|Amyntaio|Αμύνταιο|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church
Amyntaio|Amyntaio|Αμύνταιο|Ascension of the Lord|Αναλήψεως του Κυρίου|Parish Church
Amyntaio|Amyntaio|Αμύνταιο|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church
Amyntaio|Agios Athanasios|Άγιος Αθανάσιος|Saint Athanasius|Αγίου Αθανασίου|Parish Church
Amyntaio|Agios Panteleimon|Άγιος Παντελεήμονας|Saint Panteleimon|Αγίου Παντελεήμονος|Parish Church
Amyntaio|Anargyroi|Ανάργυροι|Holy Unmercenaries|Αγίων Αναργύρων|Parish Church
Amyntaio|Antigonos|Αντίγονος|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Amyntaio|Agios Grammatikos|Άγιος Γραμματικός|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Amyntaio|Vegora|Βεγόρα|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Amyntaio|Zervi|Ζέρβη|Apostle Thomas|Αποστόλου Θωμά|Parish Church
Amyntaio|Kato Grammatikos|Κάτω Γραμματικός|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Amyntaio|Kelli|Κέλλη|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Amyntaio|Kleidi|Κλειδί|Holy Apostles|Αγίων Αποστόλων|Parish Church
Amyntaio|Levaia|Λεβαία|Saint George|Αγίου Γεωργίου|Parish Church
Amyntaio|Maniaki|Μανιάκι|Saint Charalambos|Αγίου Χαραλάμπους|Parish Church
Amyntaio|Xanthogeia|Ξανθόγεια|Prophet Elijah|Προφήτου Ηλιού|Parish Church
Amyntaio|Xino Nero|Ξινό Νερό|Saint George|Αγίου Γεωργίου|Parish Church
Amyntaio|Pelargos|Πέλαργος|Ascension of the Lord|Αναλήψεως του Κυρίου|Parish Church
Amyntaio|Peraia|Περαία|Saints Theodore|Αγίων Θεοδώρων|Parish Church
Amyntaio|Petres|Πέτρες|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Parish Church
Amyntaio|Rodon|Ροδώνας|Saint Nicholas|Αγίου Νικολάου|Parish Church
Amyntaio|Fanos|Φανός|Saint John the Hut-Dweller|Αγίου Ιωάννου του Καλυβίτου|Parish Church
Amyntaio|Farangi|Φαράγγι|Saint Anthony|Αγίου Αντωνίου|Parish Church
Amyntaio|Filotas|Φιλώτας|Saint Basil|Αγίου Βασιλείου|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Holy Trinity|Αγίας Τριάδος|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Holy Protection of the Theotokos|Αγίας Σκέπης|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Saint John the Forerunner|Αγίου Ιωάννου του Προδρόμου|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Holy New Martyrs|Αγίων Νεομαρτύρων|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Saint Nicholas of Kardia|Αγίου Νικολάου Καρδιάς|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Saint Stephen and Venerable Paraskevi of Epivat|Αγίου Στεφάνου και Οσίας Παρασκευής της Επιβατινής|Parish Church
Eordaia|Ptolemaida|Πτολεμαΐδα|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church
Eordaia|Agios Christoforos|Άγιος Χριστόφορος|Saint Christopher|Αγίου Χριστοφόρου|Parish Church
Eordaia|Anarrache|Αναρράχη|Saint George|Αγίου Γεωργίου|Parish Church
Eordaia|Anatoliko|Ανατολικό|Exaltation of the Precious Cross|Υψώσεως του Τιμίου Σταυρού|Parish Church
Eordaia|Ardassa|Άρδασσα|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Parish Church
Eordaia|Asvestopetra|Ασβεστόπετρα|Saint George|Αγίου Γεωργίου|Parish Church
Eordaia|Galateia|Γαλάτεια|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Eordaia|Drosero|Δροσερό|All Saints|Αγίων Πάντων|Parish Church
Eordaia|Ermakia|Ερμάκια|Saint Athanasius|Αγίου Αθανασίου|Parish Church
Eordaia|Emporio|Εμπόριο|Saint Menas|Αγίου Μηνά|Parish Church
Eordaia|Karyochori|Καρυοχώρι|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Eordaia|Komanos|Κόμανος|Saint John Chrysostom|Αγίου Ιωάννου Χρυσοστόμου|Parish Church
Eordaia|Komnina|Κομνηνά|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Parish Church
Eordaia|Kryovrysi|Κρυόβρυση|Saint Mark of Ephesus|Αγίου Μάρκου του Ευγενικού|Parish Church
Eordaia|Mavropigi|Μαυροπηγή|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Eordaia|Mesovouno|Μεσόβουνο|Saints George and James the Brother of the Lord|Αγίων Γεωργίου και Ιακώβου του Αδελφοθέου|Parish Church
Eordaia|Milochori|Μηλοχώρι|Saint Thecla|Αγίας Θέκλας|Parish Church
Eordaia|Palaia Ampelia|Παλαιά Αμπέλια|Archangels Michael and Gabriel|Αρχαγγέλων Μιχαήλ και Γαβριήλ|Parish Church
Eordaia|Olympiada|Ολυμπιάδα|Saint Nicholas|Αγίου Νικολάου|Parish Church
Eordaia|Pentavrysso|Πεντάβρυσο|Saint Photius|Αγίου Φωτίου|Parish Church
Eordaia|Perdikkas|Περδίκκας|Ascension of the Lord|Αναλήψεως του Κυρίου|Parish Church
Eordaia|Proastio|Προάστιο|Saint Demetrius|Αγίου Δημητρίου|Parish Church
Eordaia|Pteleonas|Πτελεώνας|Evangelist Matthew|Ευαγγελιστού Ματθαίου|Parish Church
Eordaia|Pyrgoi|Πύργοι|Archangels Michael and Gabriel|Αρχαγγέλων Μιχαήλ και Γαβριήλ|Parish Church
Eordaia|Spilia|Σπηλιά|Saint George|Αγίου Γεωργίου|Parish Church
Eordaia|Foufas|Φούφας|Saint Paraskevi|Αγίας Παρασκευής|Parish Church
"""


PARISH_CONTACTS = {
    ("Florina", "Saint Panteleimon"): (["+30 23850-28223", "+30 23850-23817", "+30 6979689890"], [LOCAL_BASE + "/enories/ieros-naos-agiou-panteleimonos-florina/", LOCAL_CLERGY_PAGE_2]),
    ("Florina", "Saint George"): (["+30 23850-22595"], [LOCAL_BASE + "/enories/ieros-naos-agiou-georgiou-florina/"]),
    ("Florina", "Saint Paraskevi"): (["+30 6971540459"], [LOCAL_BASE + "/enories/ieros-naos-agias-paraskevis-florina/"]),
    ("Florina", "Saint Nicholas"): (["+30 23850-22595"], [LOCAL_BASE + "/enories/ieros-naos-agiou-nikolaou-florina/"]),
    ("Florina", "Saint Demetrius"): (["+30 23850-26203", "+30 6937166925"], [LOCAL_BASE + "/enories/ieros-naos-agiou-dimitriou-florina/", LOCAL_CLERGY_URL]),
    ("Ano Ydrousa", "Saint Gregory the Theologian"): (["+30 6944712184"], [LOCAL_BASE + "/enories/ano-ydrousa/"]),
    ("Atrapos", "Dormition of the Theotokos"): (["+30 23850-30476"], [LOCAL_BASE + "/enories/atrapos/"]),
    ("Achlada", "Saint Spyridon"): (["+30 23850-37819"], [LOCAL_BASE + "/enories/achlada/"]),
    ("Vevi", "Saint George"): (["+30 23850-41259"], [LOCAL_BASE + "/enories/vevi/"]),
    ("Ethniko", "Dormition of the Theotokos"): (["+30 23850-92668"], [LOCAL_BASE + "/enories/ethnikon/"]),
    ("Itea", "Nativity of the Theotokos"): (["+30 23850-41010"], [LOCAL_BASE + "/enories/itea/"]),
    ("Kato Kleines", "Nativity of the Theotokos"): (["+30 23850-92778", "+30 6978543651"], [LOCAL_BASE + "/enories/kato-kleinai/", LOCAL_CLERGY_URL]),
    ("Kladorrachi", "Saint Procopius"): (["+30 23850-35040"], [LOCAL_BASE + "/enories/kladorrachi/"]),
    ("Lofoi", "Saints Constantine and Helen"): (["+30 23850-41259"], [LOCAL_BASE + "/enories/lofoi-2/"]),
    ("Marina", "Saint Marina"): (["+30 23850-92628"], [LOCAL_BASE + "/enories/marina/"]),
    ("Meliti", "Saint Irene"): (["+30 23850-37146"], [LOCAL_BASE + "/enories/meliti/"]),
    ("Mesokampos", "Saint Panteleimon"): (["+30 6975980255"], [LOCAL_BASE + "/enories/mesokabos/"]),
    ("Mesonisi", "Dormition of the Theotokos"): (["+30 6945821690"], [LOCAL_BASE + "/enories/mesonisi/"]),
    ("Neos Kafkasos", "Saint George"): (["+30 23850-92628"], [LOCAL_BASE + "/enories/neos-kafkasos/"]),
    ("Neochoraki", "Saint Athanasius"): (["+30 23850-37294"], [LOCAL_BASE + "/enories/neochorakion/"]),
    ("Palaistre", "Saint John the Theologian"): (["+30 23850-41567"], [LOCAL_BASE + "/enories/palaistra/"]),
    ("Parori", "Saints Cyricus and Julitta"): (["+30 6982329727"], [LOCAL_BASE + "/enories/parori/"]),
    ("Perasma", "Holy Unmercenaries"): (["+30 6976832859"], [LOCAL_BASE + "/enories/perasma/"]),
    ("Polyplatanos", "Dormition of the Theotokos"): (["+30 23850-46815", "+30 6988262145"], [LOCAL_BASE + "/enories/polyplatanos/", LOCAL_CLERGY_URL]),
    ("Proti", "Saint George"): (["+30 23850-46815"], [LOCAL_BASE + "/enories/proti/"]),
    ("S.S. Vevis", "Saint Ignatius the God-bearer"): (["+30 23850-36187"], [LOCAL_BASE + "/enories/s-s-vevis/"]),
    ("Sitaria", "Saint Athanasius"): (["+30 23850-42015"], [LOCAL_BASE + "/enories/sitaria/"]),
    ("Skopia", "Dormition of the Theotokos"): (["+30 23850-41793"], [LOCAL_BASE + "/enories/skopia/"]),
    ("Skopos", "Dormition of the Theotokos"): (["+30 23850-37819"], [LOCAL_BASE + "/enories/skopos/"]),
    ("Triantafyllia", "Saint Paraskevi"): (["+30 23850-30476"], [LOCAL_BASE + "/enories/triantafyllia/"]),
    ("Tropaiouchos", "Saint George"): (["+30 6985835039"], [LOCAL_CLERGY_URL]),
    ("Leptokaryai", "Nativity of the Theotokos"): (["+30 6974656953"], [LOCAL_CLERGY_URL]),
    ("Armenochori", "Venerable Naum"): (["+30 6945821690"], [LOCAL_CLERGY_URL]),
    ("Polypotamos", "Dormition of the Theotokos"): (["+30 23850-30476"], [LOCAL_CLERGY_URL]),
    ("Agios Achilleios", "Saint Achilleios"): (["+30 6907512420"], [LOCAL_BASE + "/enories/agios-achilleios/"]),
    ("Agios Germanos", "Saint Germanos"): (["+30 6937246737"], [LOCAL_BASE + "/enories/agios-germanos/"]),
    ("Vrontero", "Saint Nicholas"): (["+30 6946922591"], [LOCAL_BASE + "/enories/vrontero/"]),
    ("Kallithea", "Saint Paraskevi"): (["+30 6937246737"], [LOCAL_BASE + "/enories/kallithea/"]),
    ("Laimos", "Saint Paraskevi"): (["+30 23850-35099"], [LOCAL_BASE + "/enories/laimos/"]),
    ("Psarades", "Dormition of the Theotokos"): (["+30 6937246737"], [LOCAL_CLERGY_PAGE_2]),
    ("Ydrousa", "Saint Nicholas"): (["+30 6944712184"], [LOCAL_BASE + "/enories/ydrousa/"]),
    ("Flampouro", "Dormition of the Theotokos"): (["+30 23850-23884"], [LOCAL_BASE + "/enories/flabouro/"]),
    ("Anargyroi", "Holy Unmercenaries"): (["+30 23860-41080"], [LOCAL_BASE + "/enories/anargyroi/"]),
    ("Antigonos", "Dormition of the Theotokos"): (["+30 6981632790"], [LOCAL_BASE + "/enories/antigonos/"]),
    ("Amyntaio", "Saints Constantine and Helen"): (["+30 23860-23839"], [LOCAL_BASE + "/enories/ieros-naos-agiou-kostantinou-kai-elenis/"]),
    ("Agios Panteleimon", "Saint Panteleimon"): (["+30 6983723278"], [LOCAL_BASE + "/enories/ag-panteleimonas/"]),
    ("Zervi", "Apostle Thomas"): (["+30 23810-27700"], [LOCAL_BASE + "/enories/zervi-pellas/"]),
    ("Kelli", "Dormition of the Theotokos"): (["+30 23850-92383"], [LOCAL_BASE + "/enories/kelli/"]),
    ("Maniaki", "Saint Charalambos"): (["+30 23860-24060"], [LOCAL_BASE + "/enories/maniaki/"]),
    ("Xino Nero", "Saint George"): (["+30 23850-35099"], [LOCAL_BASE + "/enories/xino-nero/"]),
    ("Peraia", "Saints Theodore"): (["+30 23810-20213"], [LOCAL_BASE + "/enories/peraia-pellas/"]),
    ("Fanos", "Saint John the Hut-Dweller"): (["+30 23860-41080"], [LOCAL_BASE + "/enories/fanos/"]),
    ("Filotas", "Saint Basil"): (["+30 6994494931"], [LOCAL_BASE + "/enories/filotas/"]),
    ("Petres", "Saints Peter and Paul"): (["+30 23860-22947"], [LOCAL_BASE + "/enories/petres/"]),
    ("Vegora", "Dormition of the Theotokos"): (["+30 23860-81414"], [LOCAL_CLERGY_URL]),
    ("Agios Athanasios", "Saint Athanasius"): (["+30 6937141738"], [LOCAL_CLERGY_PAGE_2]),
    ("Ptolemaida", "Holy Trinity"): (["+30 24630-28553"], [LOCAL_BASE + "/enories/ieros-naos-agias-triados-ptolemaida/"]),
    ("Ptolemaida", "Holy Protection of the Theotokos"): (["+30 24630-23773", "+30 24630-24257"], [LOCAL_BASE + "/enories/ieros-naos-agias-skepis-ptolemaida/", LOCAL_CLERGY_PAGE_2]),
    ("Ptolemaida", "Saint John the Forerunner"): (["+30 24630-26969"], [LOCAL_BASE + "/enories/ieros-naos-agiou-ioannou-ptolemaida/"]),
    ("Ptolemaida", "Saint Stephen and Venerable Paraskevi of Epivat"): (["+30 24630-24800"], [LOCAL_BASE + "/enories/ieros-naos-ag-stefanou-ptolemaida/"]),
    ("Ptolemaida", "Transfiguration of the Savior"): (["+30 6987034038"], [LOCAL_CLERGY_URL]),
    ("Anatoliko", "Exaltation of the Precious Cross"): (["+30 24630-31591"], [LOCAL_BASE + "/enories/anatoliko/"]),
    ("Ardassa", "Transfiguration of the Savior"): (["+30 6974934542"], [LOCAL_BASE + "/enories/ardassa/"]),
    ("Galateia", "Dormition of the Theotokos"): (["+30 6982007148"], [LOCAL_BASE + "/enories/galateia/"]),
    ("Emporio", "Saint Menas"): (["+30 24630-61151"], [LOCAL_BASE + "/enories/emporio/", LOCAL_CLERGY_PAGE_2]),
    ("Komnina", "Dormition of the Theotokos"): (["+30 6944644563"], [LOCAL_BASE + "/enories/komnina/"]),
    ("Mavropigi", "Saint Demetrius"): (["+30 24630-54619"], [LOCAL_BASE + "/enories/mavropigi/"]),
    ("Kryovrysi", "Saint Mark of Ephesus"): (["+30 6944844421"], [LOCAL_BASE + "/enories/kryovrisi/"]),
    ("Milochori", "Saint Thecla"): (["+30 6975560093"], [LOCAL_BASE + "/enories/milochori/", LOCAL_CLERGY_PAGE_2]),
    ("Olympiada", "Saint Nicholas"): (["+30 6982007148"], [LOCAL_BASE + "/enories/olympiada/"]),
    ("Proastio", "Saint Demetrius"): (["+30 6971668994"], [LOCAL_BASE + "/enories/proastio/", LOCAL_CLERGY_PAGE_2]),
    ("Pyrgoi", "Archangels Michael and Gabriel"): (["+30 6982829658"], [LOCAL_CLERGY_PAGE_2]),
    ("Foufas", "Saint Paraskevi"): (["+30 24630-29628"], [LOCAL_BASE + "/enories/foufas/"]),
    ("Xanthogeia", "Prophet Elijah"): (["+30 23810-27700"], [LOCAL_BASE + "/enories/xanthogeia/"]),
    ("Mesochori", "Dormition of the Theotokos"): (["+30 6987026171"], [LOCAL_CLERGY_PAGE_2]),
    ("Drosopigi", "Holy Trinity"): (["+30 6972304119"], [LOCAL_CLERGY_PAGE_2]),
    ("Ano Kalliniki", "Saint Nicholas"): (["+30 6948949712"], [LOCAL_BASE + "/enories/ano-kalliniki/"]),
    ("Agia Paraskevi", "Saint Paraskevi"): (["+30 23850-35040"], [LOCAL_BASE + "/enories/agia-paraskevi/"]),
    ("Ammochori", "Saint Nicholas"): (["+30 23850-41587"], [LOCAL_BASE + "/enories/ammochorion/"]),
    ("Agios Vartholomaios", "Saint Bartholomew"): (["+30 23850-36187"], [LOCAL_BASE + "/enories/ieros-naos-agiou-vartholomaiou/"]),
    ("Papagiannis", "Saint Nicholas"): (["+30 23850-41347"], [LOCAL_BASE + "/enories/papagiannis/"]),
    ("Tripotamos", "Saint George"): (["+30 23850-41781"], [LOCAL_BASE + "/enories/tripotamos/"]),
    ("Amyntaio", "Ascension of the Lord"): (["+30 6977981403"], [LOCAL_BASE + "/enories/analipsi-amyntaio/"]),
}


ADDITIONAL_SOURCE = [
    ("nicholas-agia-paraskevi", "Saint Nicholas Church in Agia Paraskevi", "Ιερός Ναός Αγίου Νικολάου Αγίας Παρασκευής", "Agia Paraskevi", "Αγία Παρασκευή", "Church", ["+30 23850-35040"], "https://imflorinas.gr/enories/agia-paraskevi-2/"),
    ("george-alona", "Saint George Church in Alona", "Ιερός Ναός Αγίου Γεωργίου Αλώνας", "Alona", "Άλωνα", "Church", [], "https://imflorinas.gr/enories/alona-2/"),
    ("george-ammochori", "Saint George Church in Ammochori", "Ιερός Ναός Αγίου Γεωργίου Αμμοχωρίου", "Ammochori", "Αμμοχώρι", "Church", ["+30 23850-41587"], "https://imflorinas.gr/enories/ammochori-2/"),
    ("elijah-ano-kalliniki", "Prophet Elijah Church in Ano Kalliniki", "Ιερός Ναός Προφήτου Ηλιού Άνω Καλλινίκης", "Ano Kalliniki", "Άνω Καλλινίκη", "Church", ["+30 6948949712"], "https://imflorinas.gr/enories/kalliniki-2/"),
    ("nicodemus-papagiannis", "Saint Nicodemus Church in Papagiannis", "Ιερός Ναός Αγίου Νικοδήμου Παπαγιάννη", "Papagiannis", "Παπαγιάννης", "Church", ["+30 23850-41347"], "https://imflorinas.gr/enories/papagiannis-2/"),
    ("kosmas-sitaria", "Saint Kosmas the Aetolian Church in Sitaria", "Ιερός Ναός Αγίου Κοσμά του Αιτωλού Σιταριάς", "Sitaria", "Σιταριά", "Church", ["+30 23850-42015"], "https://imflorinas.gr/enories/ieros-naos-agiou-kosma/"),
    ("dormition-ermakia", "Dormition of the Theotokos Church in Ermakia", "Ιερός Ναός Κοιμήσεως της Θεοτόκου Ερμακιάς", "Ermakia", "Ερμάκια", "Church", [], "https://imflorinas.gr/enories/ermakia-2/"),
    ("catherine-ss-ioannidis", "Saint Catherine Church at S.S. Ioannidis", "Ιερός Ναός Αγίας Αικατερίνης Σ.Σ. Ιωαννίδη", "S.S. Ioannidis", "Σ.Σ. Ιωαννίδη", "Church", [], "https://imflorinas.gr/iera-panigyris-ierou-naou-agias-aikaterinis-s-s-ioannidi/"),
    ("elijah-meliti", "Prophet Elijah Church in Meliti", "Ιερός Ναός Προφήτου Ηλιού Μελίτης", "Meliti", "Μελίτη", "Church", [], "https://imflorinas.gr/panigyrizei-o-ieros-naos-tou-profiti-ilia-stin-enoria-melitis-florinas/"),
]


PARISH_CHAPELS = [
    {
        "key": "dormition-ptolemaida-chapel", "rank": "Parish Chapel",
        "name": "Dormition of the Theotokos Parish Chapel in Ptolemaida",
        "local": "Ενοριακό Παρεκκλήσιο Κοιμήσεως της Θεοτόκου Πτολεμαΐδας",
        "seat": "Ptolemaida", "local_seat": "Θέση Κουρί, 502 00 Πτολεμαΐδα",
        "phones": ["+30 6944844421", "+30 24630-22366"],
        "source": "https://imflorinas.gr/enories/parekklisio-koimiseos-tis-theotokou/",
    },
    {
        "key": "paraskevi-amyntaio-chapel", "rank": "Parish Chapel",
        "name": "Saint Paraskevi Parish Chapel in Amyntaio",
        "local": "Ενοριακό Παρεκκλήσιο Αγίας Παρασκευής Αμυνταίου",
        "seat": "Amyntaio", "local_seat": "Κωνσταντίνου Ιωάννου, 532 00 Αμύνταιο",
        "phones": ["+30 23860-22256"],
        "source": "https://imflorinas.gr/enories/parekklisio-agias-paraskevis/",
    },
    {
        "key": "menas-florina-chapel", "rank": "Parish Chapel",
        "name": "Saint Menas Parish Chapel in Florina",
        "local": "Ενοριακό Παρεκκλήσιο Αγίου Μηνά Ενορίας Αγίου Νικολάου Φλωρίνης",
        "seat": "Florina", "local_seat": "Φλώρινα",
        "source": "https://imflorinas.gr/panigyris-ierou-parekklisiou-agiou-mina-enorias-agiou-nikolaou-florinis/",
    },
    {
        "key": "nectarios-anatoliko-chapel", "rank": "Parish Chapel",
        "name": "Saint Nectarios Chapel in Anatoliko",
        "local": "Ιερό Παρεκκλήσιο Αγίου Νεκταρίου Ανατολικού Εορδαίας",
        "seat": "Anatoliko", "local_seat": "Ανατολικό Εορδαίας",
        "source": "https://imflorinas.gr/panigyrizei-to-iero-parekklisio-agiou-nektariou-sto-anatoliko-eordaias/",
    },
    {
        "key": "solomoni-cathedral-chapel", "rank": "Cathedral Chapel",
        "name": "Saint Solomoni Chapel at the Saint Panteleimon Metropolitan Cathedral",
        "local": "Παρεκκλήσιο Αγίας Σολομονής Ιερού Μητροπολιτικού Ναού Αγίου Παντελεήμονος",
        "seat": "Florina", "local_seat": "Φλώρινα",
        "source": "https://imflorinas.gr/wp-content/uploads/2026/01/%CE%A3%CE%A4%CE%91%CE%93%CE%9F%CE%9D%CE%95%CE%A3-%CE%A0%CE%99%CE%A3%CE%A4%CE%95%CE%A9%CE%A3-low-res.pdf",
    },
    {
        "key": "athanasius-cathedral-chapel", "rank": "Cathedral Chapel",
        "name": "Saint Athanasius Chapel at the Saint Panteleimon Metropolitan Cathedral",
        "local": "Παρεκκλήσιο Αγίου Αθανασίου Ιερού Μητροπολιτικού Ναού Αγίου Παντελεήμονος",
        "seat": "Florina", "local_seat": "Φλώρινα",
        "source": "https://imflorinas.gr/wp-content/uploads/2026/01/%CE%A3%CE%A4%CE%91%CE%93%CE%9F%CE%9D%CE%95%CE%A3-%CE%A0%CE%99%CE%A3%CE%A4%CE%95%CE%A9%CE%A3-low-res.pdf",
    },
]


MONASTERIES = [
    ("dormition-kladorrachi", "Dormition of the Theotokos Monastery", "Ιερά Μονή Κοιμήσεως της Θεοτόκου", "Kladorrachi", "Κλαδορράχη 531 00, Φλώρινα", ["+30 6976608119"], [], "https://imflorinas.gr/mones/i-m-koimiseos-tis-theotokou-kladorrachi/"),
    ("paraskevi-milochori", "Saint Paraskevi Monastery", "Ιερά Μονή Αγίας Παρασκευής", "Milochori", "Μηλοχώρι 500 05, Εορδαία", ["+30 6988922655"], [], "https://imflorinas.gr/mones/i-m-agias-paraskevi-milochori/"),
    ("mark-proti", "Saint Mark the Evangelist Monastery", "Ιερά Μονή Αγίου Μάρκου του Ευαγγελιστού", "Proti", "Πρώτη 531 00, Φλώρινα", ["+30 23850-37944"], ["moniagioumarkou@gmail.com"], "https://imflorinas.gr/mones/i-m-agiou-markou-proti/"),
    ("augustine-florina", "Saint Augustine of Hippo Monastery", "Ιερά Μονή Αγίου Αυγουστίνου Ιππώνος", "Florina", "Κούλη Στερίκα 23, 531 00 Φλώρινα", ["+30 23850-28610"], ["imaaflo@yahoo.gr"], "https://imflorinas.gr/mones/i-m-agiou-avgoustinou-florina/"),
    ("panteleimon-euboula", "Saints Panteleimon and Euboula Monastery", "Ιερά Μονή Αγίων Παντελεήμονος και Ευβούλης", "Agios Panteleimon", "Άγιος Παντελεήμονας 532 00, Αμύνταιο", ["+30 23860-61130"], ["i.m.ag.pan.ev@gmail.com"], "https://imflorinas.gr/mones/i-m-agiwn-panteleimona-kai-evvoulis-amyntaio/"),
    ("gregory-palamas-antigonos", "Saint Gregory Palamas Monastery", "Ιερά Μονή Αγίου Γρηγορίου του Παλαμά", "Antigonos", "Αντίγονος 530 70, Αμύνταιο", ["+30 6974934540"], [], "https://imflorinas.gr/mones/i-m-agiou-grigoriou-tou-palama-antigono/"),
    ("kosmas-ardassa", "Saint Kosmas the Aetolian Monastery", "Ιερά Μονή Αγίου Κοσμά του Αιτωλού", "Ardassa", "Άρδασσα 502 00, Εορδαία", ["+30 6988922655", "+30 6974934542"], [], "https://imflorinas.gr/mones/i-m-agiou-kosma-tou-aitolou-ardassa/"),
    ("ascension-vartholomaios", "Ascension of the Lord Monastery", "Ιερά Μονή Αναλήψεως του Κυρίου", "Agios Vartholomaios", "Άγιος Βαρθολομαίος 531 00, Φλώρινα", ["+30 6989177583"], [], "https://imflorinas.gr/mones/iera-moni-analipseos-tou-kyriou/"),
]


MONASTERY_CHAPELS = [
    ("david-kladorrachi", "Venerable David the Elder Monastery Chapel", "Παρεκκλήσιο Οσίου Δαυίδ του Γέροντος", "Kladorrachi", "Κλαδορράχη 531 00, Φλώρινα", MONASTERIES[0][7]),
    ("nectarios-kladorrachi", "Saint Nectarios of Pentapolis Monastery Chapel", "Παρεκκλήσιο Αγίου Νεκταρίου Πενταπόλεως", "Kladorrachi", "Κλαδορράχη 531 00, Φλώρινα", MONASTERIES[0][7]),
    ("kyriaki-milochori", "Saint Kyriaki Monastery Chapel", "Παρεκκλήσιο Αγίας Κυριακής", "Milochori", "Μηλοχώρι 500 05, Εορδαία", MONASTERIES[1][7]),
    ("ignatius-milochori", "Saint Ignatius the God-bearer Monastery Chapel", "Παρεκκλήσιο Αγίου Ιγνατίου του Θεοφόρου", "Milochori", "Μηλοχώρι 500 05, Εορδαία", MONASTERIES[1][7]),
    ("nectarios-milochori", "Saint Nectarios Monastery Chapel", "Παρεκκλήσιο Αγίου Νεκταρίου", "Milochori", "Μηλοχώρι 500 05, Εορδαία", MONASTERIES[1][7]),
    ("life-giving-spring-milochori", "Life-giving Spring Monastery Chapel", "Παρεκκλήσιο Ζωοδόχου Πηγής", "Milochori", "Μηλοχώρι 500 05, Εορδαία", MONASTERIES[1][7]),
    ("entrance-theotokos-proti", "Entrance of the Theotokos Monastery Chapel", "Παρεκκλήσιο Εισοδίων της Θεοτόκου", "Proti", "Πρώτη 531 00, Φλώρινα", MONASTERIES[2][7]),
    ("catherine-proti", "Saint Catherine Monastery Chapel", "Παρεκκλήσιο Αγίας Αικατερίνης", "Proti", "Πρώτη 531 00, Φλώρινα", MONASTERIES[2][7]),
    ("engyetria-florina", "Panagia Engyetria Monastery Chapel", "Παρεκκλήσιο Παναγίας της Εγγυήτριας", "Florina", "Κούλη Στερίκα 23, 531 00 Φλώρινα", MONASTERIES[3][7]),
    ("monica-florina", "Saint Monica Monastery Chapel", "Παρεκκλήσιο Αγίας Μόνικας", "Florina", "Κούλη Στερίκα 23, 531 00 Φλώρινα", MONASTERIES[3][7]),
    ("raphael-antigonos", "Saints Raphael, Nicholas and Irene Monastery Chapel", "Παρεκκλήσιο Αγίων Ραφαήλ, Νικολάου και Ειρήνης", "Antigonos", "Αντίγονος 530 70, Αμύνταιο", MONASTERIES[5][7]),
    ("silouan-ardassa", "Saint Silouan the Athonite Monastery Chapel", "Παρεκκλήσιο Αγίου Σιλουανού του Αθωνίτου", "Ardassa", "Άρδασσα 502 00, Εορδαία", MONASTERIES[6][7]),
    ("eustathius-ardassa", "Saint Eustathius Monastery Chapel", "Παρεκκλήσιο Αγίου Ευσταθίου", "Ardassa", "Άρδασσα 502 00, Εορδαία", MONASTERIES[6][7]),
    ("raphael-ardassa", "Saints Raphael, Nicholas and Irene Monastery Chapel", "Παρεκκλήσιο Αγίων Ραφαήλ, Νικολάου και Ειρήνης", "Ardassa", "Άρδασσα 502 00, Εορδαία", MONASTERIES[6][7]),
]


ALLOWED_HOSTS = {
    "imflorinas.gr", "www.imflorinas.gr", "ec-patr.org",
    "ecclesiagreece.gr", "www.ecclesiagreece.gr",
}
FORBIDDEN_PUNCTUATION = re.compile("[\u2013\u2014]")


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "body"


def parse_parishes():
    rows = []
    for line in PARISH_SOURCE.strip().splitlines():
        district, seat, local_seat, dedication, local_dedication, rank = line.split("|")
        row_id = "gr-ep-phlorina-%03d-%s" % (
            len(rows) + 1, slug(seat + "-" + dedication),
        )
        source = {
            "id": row_id, "parent": PARENT, "kind": "parish", "rank": rank,
            "name": "%s %s in %s" % (dedication, rank, seat),
            "local": "Ιερός Ναός %s %s" % (local_dedication, local_seat),
            "seat": seat, "country": "GR",
            "address": [local_seat, district, "Ελλάδα"],
            "sources": [LEGAL_URL, LOCAL_PARISH_URL],
        }
        contact = PARISH_CONTACTS.get((seat, dedication))
        if contact:
            source["phones"] = list(contact[0])
            source["contact_sources"] = list(contact[1])
            source["contact_checked"] = CHECKED
        rows.append(source)
    return rows


def build_rows():
    rows = parse_parishes()
    for key, name, local, seat, local_seat, rank, phones, source_url in ADDITIONAL_SOURCE:
        item = {
            "id": "gr-ep-phlorina-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "parish", "rank": rank,
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [local_seat, "Ελλάδα"], "sources": [source_url],
        }
        if phones:
            item["phones"] = list(phones)
            item["contact_sources"] = [source_url]
            item["contact_checked"] = CHECKED
        rows.append(item)
    for source in PARISH_CHAPELS:
        item = {
            "id": "gr-ep-phlorina-%03d-%s" % (len(rows) + 1, source["key"]),
            "parent": PARENT, "kind": "parish", "rank": source["rank"],
            "name": source["name"], "local": source["local"],
            "seat": source["seat"], "country": "GR",
            "address": [source["local_seat"], "Ελλάδα"],
            "sources": [source["source"]],
        }
        if source.get("phones"):
            item["phones"] = list(source["phones"])
            item["contact_sources"] = [source["source"]]
            item["contact_checked"] = CHECKED
        rows.append(item)
    for key, name, local, seat, local_address, phones, emails, source_url in MONASTERIES:
        item = {
            "id": "gr-ep-phlorina-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "monastery", "rank": "Monastery",
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [local_address, "Ελλάδα"],
            "phones": list(phones), "sources": [source_url, EP_URL],
            "contact_sources": [source_url, EP_URL], "contact_checked": CHECKED,
        }
        if emails:
            item["emails"] = list(emails)
        rows.append(item)
    for key, name, local, seat, local_address, source_url in MONASTERY_CHAPELS:
        rows.append({
            "id": "gr-ep-phlorina-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "monastery", "rank": "Monastery Chapel",
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [local_address, "Ελλάδα"], "sources": [source_url],
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 156
EXPECTED_OWNER_COUNTS = {PARENT: 156}
EXPECTED_KINDS = {"monastery": 22, "parish": 134}
EXPECTED_RANKS = {
    "Cathedral Chapel": 2,
    "Church": 9,
    "Metropolitan Cathedral": 1,
    "Monastery": 8,
    "Monastery Chapel": 14,
    "Parish Chapel": 4,
    "Parish Church": 118,
}
EXISTING_PARENTS = {PARENT}


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s carries a non-competent source: %s" % (label, value))


def clean(source):
    item = {key: value for key, value in source.items() if value not in (None, "", [])}
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
    return item


def coverage_tuple(rows):
    return (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site")) for item in rows),
        sum(bool(item.get("phones")) for item in rows),
        sum(len(item.get("phones") or []) for item in rows),
        sum(bool(item.get("emails")) for item in rows),
        sum(len(item.get("emails") or []) for item in rows),
        sum(bool(item.get("site")) for item in rows),
        sum(bool(item.get("address")) for item in rows),
    )


def validate_ledger(expected_coverage=None):
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Florina candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Florina candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "legal_named_parish_rows": 119,
        "current_directory_additional_churches": 7,
        "other_current_exact_churches": 2,
        "exact_non_monastic_chapels": 6,
        "current_monasteries": 8,
        "exact_monastery_chapels": 14,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Florina ledger summary drifted at %s" % key)
    if expected_coverage:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites",
            "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Florina ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Florina ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Florina ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Florina candidate IDs repeat")
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
            raise ValueError("duplicate Florina ID: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has wrong country" % row_id)
        if item.get("kind") not in ("parish", "monastery"):
            raise ValueError("%s has invalid kind" % row_id)
        for field in ("name", "local", "seat", "rank"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        rendered = json.dumps(item, ensure_ascii=False)
        if FORBIDDEN_PUNCTUATION.search(rendered):
            raise ValueError("%s carries forbidden punctuation" % row_id)
        signature = unicodedata.normalize(
            "NFKC", "%s|%s|%s" % (item["local"], item["seat"], item["rank"])
        ).casefold()
        signature = re.sub(r"\s+", " ", signature).strip()
        if signature in signatures:
            raise ValueError("%s duplicates %s" % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[item["parent"]] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Florina English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Florina English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Florina parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Florina kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Florina rank totals drifted: %r" % dict(rank_counts))
    coverage = coverage_tuple(result)
    validate_ledger(coverage)
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_live_source(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=45) as response:
        content_type = response.headers.get("Content-Type", "").lower()
        payload = response.read()
        if "pdf" in content_type or url.endswith(".pdf"):
            if not payload.startswith(b"%PDF") or len(payload) < 100000:
                raise ValueError("invalid PDF payload")
            return None
        if "html" not in content_type:
            raise ValueError("unexpected content type %s" % content_type)
        return payload.decode("utf-8", "replace")


def check_live_sources():
    ep_payload = fetch_live_source(EP_URL)
    fetch_live_source(LEGAL_URL)
    ep_text = normalize_source_text(ep_payload)
    for marker in (
            "Ενοριακοί Ναοί: 119", "Παρεκκλήσια: 80", "Εξωκκλήσια: 120",
            "Ιδρυματικοί Ναοί: 18", "Μοναστηριακοί Ναοί: 7",
            "6976.608.119", "moniagioumarkou@gmail.com",
            "i.m.ag.pan.ev@gmail.com", "6989.177.583"):
        if normalize_source_text(marker) not in ep_text:
            raise ValueError("live Florina Patriarchate marker failed: %s" % marker)
    try:
        fetch_live_source(LOCAL_PARISH_URL)
    except HTTPError as exc:
        if exc.code != 403:
            raise
    build()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        check_live_sources()
        print("Florina live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Florina check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
