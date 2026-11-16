#!/usr/bin/env python3
"""Audited current subordinate bodies of the Metropolis of Kifisia."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
from pathlib import Path
import re
import shutil
import ssl
import subprocess
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PARENT = "gr-kifisia"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "kifisia_country.json"

PROFILE_URL = "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/kephisias-amarousiou-oropou-kai-marathonos"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2015_october.pdf"
STRUCTURE_URL = "https://www.imkifissias.gr/index.php?Itemid=470&id=73&option=com_content&view=article"
REGION_INDEX_URL = "https://www.imkifissias.gr/index.php/ieroi-naoi"
MEN_MONASTERIES_URL = "https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai"
WOMEN_MONASTERIES_URL = "https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai"

REGIONS = {
    "a": {
        "admin": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/75-arxieratiki-perifereia-kifisias",
        "listing": "https://www.imkifissias.gr/index.php/ieroi-naoi/85-ero-nao-a-rxieratik-s-perifereias-kifisi-s",
        "count": 21,
    },
    "b": {
        "admin": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/76-arxieratiki-perifereia-ekalis",
        "listing": "https://www.imkifissias.gr/index.php/ieroi-naoi/86-ero-nao-v-rxieratik-s-perifereias-kalis",
        "count": 16,
    },
    "c": {
        "admin": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/77-arxieratiki-perifereia-amarousiou",
        "listing": "https://www.imkifissias.gr/index.php/ieroi-naoi/87-ero-nao-g-rxieratik-s-perifereias-marousiou",
        "count": 17,
    },
    "d": {
        "admin": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/78-arxieratiki-perifereia-metamorfosis",
        "listing": "https://www.imkifissias.gr/index.php/ieroi-naoi/88-ero-nao-d-rxieratik-s-perifereias-metamorfosis",
        "count": 8,
    },
    "e": {
        "admin": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/79-arxieratiki-perifereia-n-makris-kai-marathonos",
        "listing": "https://www.imkifissias.gr/index.php/ieroi-naoi/89-ero-nao-e-rxieratik-s-perifereias-n-makris",
        "count": 11,
    },
    "f": {
        "admin": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/80-arxieratiki-perifereia-kapandritiou-kai-oropou",
        "listing": "https://www.imkifissias.gr/index.php/ieroi-naoi/90-ero-nao-st-rxieratik-s-perifereias-ropo",
        "count": 36,
    },
}

CATEGORY_URLS = {
    "Pilgrimage Church": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/81-proskynimatikoi-ieroi-naoi",
    "Metropolitan Chapel": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/82-mitropolitika-parekklisia",
    "Parish Chapel": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/83-enoriaka-parekklisia",
    "Institutional Chapel": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/84-parekklisia-idrymaton",
    "Cemetery Chapel": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/85-parekklisia-koimitirion",
    "Armed Forces Chapel": "https://www.imkifissias.gr/index.php/iera-mitropolis/dioikisi/arxieratikes-perifereies/86-parekklisia-enoplon-dynameon",
}

PARISH_DATA = r"""
a|Ἅγιος Δημήτριος Κηφισιᾶς (Μητροπολιτικός - Καθεδρικός)|Κηφισιά|Πλατεῖα Ἁγίου Δημητρίου;145 62 Κηφισιά|+30 210-801-3195,+30 210-801-3909|||
a|Ἁγία Ἄννα Κηφισιᾶς|Κηφισιά|Τέρμα Σαρανταπόρου;145 63 Κηφισιά|+30 210-801-1018|||
a|Ἅγιος Γεώργιος Κηφισιᾶς|Κηφισιά|Τατοΐου 28;145 61 Κηφισιά|+30 210-807-1050,+30 210-807-8297||http://agiosgeorgioskifisias.blogspot.com/?m=1|
a|Ὑπαπαντή τοῦ Κυρίου, Ἅγιοι Ἀνάργυροι καὶ Ἅγιος Λουκᾶς Ἀδαμῶν|Κηφισιά|Πελοποννήσου καὶ Φιγαλείας;145 64 Κηφισιά|+30 210-625-3741|||
a|Ἅγιος Νεκτάριος Κάτω Κηφισιᾶς|Κηφισιά|1ης Μαΐου καὶ Ἀραβοσιτᾶ;145 61 Κηφισιά|+30 210-801-6585|||
a|Ἅγιοι Πέτρος καὶ Παῦλος καὶ Ἅγιος Νεκτάριος Ἄνω Κηφισιᾶς|Κηφισιά|25ης Μαρτίου καὶ Ἁγίου Νεκταρίου 10;145 62 Κηφισιά|+30 210-808-4100|||
a|Ἁγία Τριάς Νέας Κηφισιᾶς|Κηφισιά|Παυσιλίπου 1;145 62 Κηφισιά|+30 210-807-6521,+30 210-807-9341||http://agiatriadaneakifisia.blogspot.com/?m=1|
a|Μεταμόρφωσις τοῦ Σωτῆρος Κεφαλαρίου Κηφισιᾶς|Κηφισιά|Πλατεία Κεφαλαρίου, Τέρμα Κολοκοτρώνη;145 62 Κηφισιά|+30 210-801-1133|||
a|Ἅγιος Γεώργιος Μελισσίων|Μελίσσια|17ης Νοεμβρίου 12;151 27 Μελίσσια|+30 210-804-3330|||
a|Ἁγία Μαρίνα Μελισσίων|Μελίσσια|Ἱπποκράτους καὶ Πηγῆς Ἀφροδίτης 2;151 27 Μελίσσια|+30 210-804-5266|||
a|Ζωοδόχος Πηγή Μελισσίων|Μελίσσια|Δημοκρατίας 10;151 27 Μελίσσια|+30 210-804-1665||http://zoodoxosmelission.blogspot.com/?m=1|
b|Κοίμησις Θεοτόκου Ἁγίου Στεφάνου|Ἅγιος Στέφανος|Κοιμήσεως Θεοτόκου 11;145 65 Ἅγιος Στέφανος|+30 210-814-1919|grammateia@agios-stefanos.gr|http://www.agios-stefanos.gr/|
b|Κοίμησις Θεοτόκου Ἀνοίξεως|Ἄνοιξη|Κανάρη 9;145 69 Ἄνοιξη|+30 210-621-8910||https://www.panagitsa-anixi.gr/|
b|Ἅγιος Γεώργιος καὶ Ἅγιος Διονύσιος Διονύσου|Διόνυσος|Ἁγίου Γεωργίου 1;145 76 Διόνυσος|+30 210-815-0818,+30 210-815-0556,+30 210-621-0481|||
b|Ἅγιος Δημήτριος Δροσιᾶς|Δροσιά|Ἐθνάρχου Μακαρίου;145 72 Δροσιά|+30 210-813-5685|||
b|Κοίμησις Θεοτόκου καὶ Ἁγία Μαρίνα Ἐκάλης|Ἐκάλη|Θησέως 54;145 78 Ἐκάλη|+30 210-813-1201,+30 210-622-8242|agiamarinaekalis@gmail.com|https://agiamarinaekalis.gr/|
b|Ἁγία Τριάς Ἐκάλης|Ἐκάλη|Δημητρίου Λαμπράκη 2;145 78 Ἐκάλη|+30 210-813-7325,+30 210-625-2471|||
b|Εὐαγγελισμός Θεοτόκου Νέας Ἐρυθραίας|Νέα Ἐρυθραία|Ἁγίου Φανουρίου 3;146 71 Νέα Ἐρυθραία|+30 210-620-4340,+30 210-800-0196|Evaggelistriaerythreas@gmail.com||
b|Ἁγία Ματρώνα Νέας Ἐρυθραίας|Νέα Ἐρυθραία|Ἠλία Βενέζη καὶ Σπύρου Λούη;146 71 Νέα Ἐρυθραία|+30 210-800-1309||https://agia-matrona.gr/|
b|Προφήτης Ἠλίας Ροδοπόλεως|Ροδόπολη|Προφήτη Ἠλία;165 74 Ροδόπολη|+30 210-621-9655,+30 210-621-9744|info@enoriarodopolis.gr|https://enoriarodopolis.gr/|
b|Κοίμησις Θεοτόκου Σταμάτας|Σταμάτα|Πλατεῖα Σταμάτας;145 75 Σταμάτα|+30 210-621-9911,+30 210-621-5509|||
c|Ἅγιοι Ἀνάργυροι Ἀμαρουσίου|Ἀμαρούσιον|Ἁγίων Ἀναργύρων καὶ Μεγάλου Ἀλεξάνδρου;151 22 Ἀμαρούσιον|+30 210-802-8561,+30 210-612-0492|||
c|Ἅγιοι Ἀπόστολοι Ἀμαρουσίου|Ἀμαρούσιον|Θεσσαλίας 10;141 21 Ἀμαρούσιον|+30 210-271-6783,+30 210-271-6782|ag.apostoloi.ps@gmail.com||
c|Ἅγιος Ἐλευθέριος Ἀμαρουσίου|Ἀμαρούσιον|Ἁγίου Ἀθανασίου καὶ Ἁγίου Ἐλευθερίου;151 25 Ἀμαρούσιον|+30 210-619-6388|||
c|Ἅγιος Θωμᾶς Ἀμαρουσίου|Ἀμαρούσιον|Ἁγίου Θωμᾶ 25;151 24 Ἀμαρούσιον|+30 210-619-8460|||
c|Ἅγιος Κοσμᾶς ὁ Αἰτωλός Ἀμαρουσίου|Ἀμαρούσιον|Μαραθωνομάχων καὶ Βυζαντίου 14;151 24 Ἀμαρούσιον|+30 210-619-9116,+30 210-619-9858||https://www.inagioskosmas.gr/|
c|Ἅγιος Νικόλαος Ἀμαρουσίου|Ἀμαρούσιον|Ἐλευθερίου Βενιζέλου καὶ Ἁγίου Νικολάου;151 22 Ἀμαρούσιον|+30 210-802-8011|||
c|Ὑπαπαντή τοῦ Σωτῆρος Ἀμαρουσίου|Ἀμαρούσιον|Πάρκο Νεαπόλεως καὶ Ἐλευθερίας;151 23 Ἀμαρούσιον|+30 210-685-4122,+30 210-682-5264|||
c|Κοίμησις Θεοτόκου Ἀμαρουσίου|Ἀμαρούσιον|Μητροπόλεως καὶ Κοιμήσεως Θεοτόκου;151 24 Ἀμαρούσιον|+30 210-802-8211,+30 210-802-9606|grammateia@panagia-amarousiou.gr|https://panagia-amarousiou.gr/|
c|Παναγία Βλαχερνῶν Ἀμαρουσίου|Ἀμαρούσιον|Λεωφόρος Κηφισίας 40;151 24 Ἀμαρούσιον|+30 210-619-8828|invlaherna@yahoo.gr,naos@inpv.gr|https://inpv.gr/|
d|Ἅγιοι Ἀπόστολοι Πέτρου καὶ Παύλου Πεύκης|Πεύκη|Νικολάου Πλαστήρα καὶ Πατριάρχου Γρηγορίου Ε΄;151 21 Πεύκη|+30 210-802-7738|agioi.apostoloi@gmail.com|https://www.agioiapostoloi.gr/|
d|Ἅγιος Παντελεήμων Πεύκης|Πεύκη|Ἁγίου Παντελεήμονος 9;151 21 Πεύκη|+30 210-612-3532,+30 210-612-3577|||
d|Ἁγία Βαρβάρα Μεταμορφώσεως|Μεταμόρφωσις|Πλατεῖα Ἁγίας Βαρβάρας 1;144 52 Μεταμόρφωσις|+30 210-281-4063|ieros.naos.ag.varvaras.met@gmail.com|https://agiavarvaramet.gr/|
d|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη Μεταμορφώσεως|Μεταμόρφωσις|Γεωργίου Παπανδρέου 66Α;144 51 Μεταμόρφωσις|+30 210-282-8985,+30 210-282-8926|||
d|Μεταμόρφωσις τοῦ Σωτῆρος Μεταμορφώσεως|Μεταμόρφωσις|Χλόης καὶ Ὀδυσσέως;144 52 Μεταμόρφωσις|+30 210-285-0060,+30 210-281-6706|iknmsm@gmail.com,info@inmm.gr|http://inmm.gr/|
d|Προφήτης Ἠλίας Μεταμορφώσεως|Μεταμόρφωσις|Προφήτου Ἠλιοὺ καὶ Παναθηναίων 22;144 51 Μεταμόρφωσις|+30 210-281-7533|||
d|Ἁγία Βαρβάρα Λυκοβρύσεως|Λυκόβρυσις|Σοφοκλῆ Βενιζέλου 23;141 23 Λυκόβρυσις|+30 210-281-6007,+30 210-284-6211|||
d|Ζωοδόχος Πηγή Λυκοβρύσεως|Λυκόβρυσις|Γεωργίου Ἀργύρη καὶ Μενέλαου Λουντέμη;141 23 Λυκόβρυσις|+30 210-281-5574,+30 210-281-5578|||
e|Κοίμησις Θεοτόκου Ἄνω Σουλίου|Ἄνω Σούλι|190 07 Μαραθών|+30 22940-66333|||
e|Ἅγιος Γεώργιος Γραμματικοῦ|Γραμματικόν|Ἁγίου Γεωργίου 16;190 07 Μαραθών|+30 22940-61213|||
e|Μεταμόρφωσις τοῦ Σωτῆρος Καλετζίου|Καλέτζι|190 07 Μαραθών|+30 22940-69299,+30 22940-61069|||
e|Ἅγιος Μόδεστος Κάτω Σουλίου|Κάτω Σούλι|Ἁγίου Μοδέστου 8;190 07 Μαραθών|+30 22940-63396,+30 22940-94001|||
e|Ἅγιος Ἰωάννης ὁ Πρόδρομος Μαραθῶνος|Μαραθών|Πλατεῖα Ἡρώων;190 07 Μαραθών|+30 22940-66333|||
e|Ἅγιος Παντελεήμων Παραλίας Μαραθῶνος|Παραλία Μαραθῶνος|Ἁγίου Παντελεήμονος 1;190 07 Μαραθών|+30 22940-55582,+30 22940-61069|||
e|Κοίμησις Θεοτόκου Ματίου|Μάτι|Κύπρου καὶ Κοιμήσεως Θεοτόκου;190 05 Νέα Μάκρη|+30 22940-34414,+30 22940-34415|inktheotokou.mati@gmail.com|http://www.koimisi-theotokou-mati.gr|https://www.imkifissias.gr/index.php?Itemid=1170&catid=89&id=228&option=com_content&view=article
e|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη Νέας Μάκρης|Νέα Μάκρη|Λεωφόρος Μαραθῶνος;190 05 Νέα Μάκρη|+30 22940-94001,+30 22940-99579,+30 697-791-3295|||https://imkifissias.gr/index.php/ieroi-naoi/89-ero-nao-e-rxieratik-s-perifereias-n-makris/219-eros-naos-giou-konstantinou-kai-lenis-n-makris
e|Ἁγία Μαρίνα Νέας Μάκρης|Νέα Μάκρη|Λεωφόρος Μαραθῶνος;190 05 Νέα Μάκρη|+30 22940-95622|||
e|Προφήτης Ἠλίας Ἀνατολῆς Νέας Μάκρης|Ἀνατολή Νέας Μάκρης|190 05 Νέα Μάκρη|+30 22940-90355|||
e|Ἅγιος Ἰωάννης ὁ Πρόδρομος Νέου Βουτζᾶ|Νέος Βουτζᾶς|Ἁγίου Ἰωάννου 15 καὶ Μεγάλου Ἀλεξάνδρου;190 05 Νέος Βουτζᾶς|+30 22940-77941|||
f|Ἅγιοι Ἀπόστολοι Πέτρος καὶ Παῦλος Βαρνάβα|Βαρνάβας|190 14 Βαρνάβας|+30 22950-97367|||
f|Ἅγιοι Ἀπόστολοι Παραλίας Καλάμου|Παραλία Καλάμου|190 17 Κάλαμος|+30 22950-82618|||
f|Κοίμησις Θεοτόκου Καλάμου|Κάλαμος|190 17 Κάλαμος|+30 22950-62709|||
f|Ἁγία Παρασκευή Καπανδριτίου|Καπανδρίτι|190 14 Καπανδρίτι|+30 22950-53108,+30 22950-53889|||
f|Ἁγία Παρασκευή Μαλακάσας|Μαλακάσα|190 11 Μαλακάσα|+30 22950-98498,+30 22950-98458||https://aparaskevimal.gr/|
f|Ἅγιος Ἀθανάσιος Μαρκοπούλου Ὠρωποῦ|Μαρκόπουλο Ὠρωποῦ|190 15 Ὠρωπός|+30 22950-33501|||
f|Παμμέγιστοι Ταξιάρχαι καὶ Ἅγιος Δημήτριος Μηλεσίου|Μήλεσι|190 15 Ὠρωπός|+30 22950-98270,+30 22950-92270|||https://imkifissias.gr/index.php/ieroi-naoi/90-ero-nao-st-rxieratik-s-perifereias-ropo/319-er-s-na-s-pammegiston-taksiarx-n-ka-giou-dimitriou-milesi-ropo
f|Ἅγιος Δημήτριος Πολυδενδρίου|Πολυδένδρι|190 14 Πολυδένδρι|+30 22950-52700|||
f|Κοίμησις Θεοτόκου Νέων Παλατίων|Νέα Παλάτια|190 15 Ὠρωπός|+30 22950-31886,+30 22950-35567|||
f|Κοίμησις Θεοτόκου Νέας Πολιτείας|Νέα Πολιτεία Ὠρωποῦ|190 15 Ὠρωπός|+30 22950-34407|||
f|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη Συκαμίνου|Συκάμινον|190 15 Ὠρωπός|+30 22950-73431,+30 22950-73430|||
f|Εὐαγγελισμός Θεοτόκου Χαλκουτσίου|Χαλκούτσι|190 15 Ὠρωπός|+30 22950-71988|||
f|Ἁγία Μαρίνα Ὠρωποῦ|Ὠρωπός|190 15 Ὠρωπός|+30 22950-36331,+30 22950-36341,+30 22950-62709|||https://www.imkifissias.gr/index.php/ieroi-naoi/90-ero-nao-st-rxieratik-s-perifereias-ropo/310-eros-naos-koimiseos-theotokou-ropo
f|Ἅγιος Ἀνδρέας Σκάλας Ὠρωποῦ|Σκάλα Ὠρωποῦ|190 15 Ὠρωπός|+30 22950-32386,+30 694-609-5085,+30 698-106-2126||https://agios-andreas.gr/|
"""

CATEGORY_DATA = r"""
Pilgrimage Church|Ἱερὸ Προσκύνημα καὶ Καθίδρυμα Παναγία ἡ Ἐλευθερώτρια|Κοκκιναρᾶς Κηφισιᾶς|Ἀρεταίου;145 63 Κηφισιά|+30 210-801-4620,+30 210-801-4611,+30 694-464-2746|panagia@eleftherotria.gr|https://www.eleftherotria.gr/index.html
Metropolitan Chapel|Ἀπόστολος Ἰάκωβος ὁ Ἀδελφόθεος|Κηφισιά|145 10 Κηφισιά||||
Metropolitan Chapel|Προφήτης Ἠλίας Ἐπισκοπείου|Κηφισιά|145 10 Κηφισιά||||
Metropolitan Chapel|Παναγία Νερατζιώτισσα|Ἀμαρούσιον|151 24 Ἀμαρούσιον|+30 210-802-8784|||
Metropolitan Chapel|Ἅγιοι Τιμόθεος καὶ Μαύρα Νέας Ἐρυθραίας|Νέα Ἐρυθραία|Ἁγίας Μαύρας 3;146 71 Νέα Ἐρυθραία|+30 210-813-7315|||
Metropolitan Chapel|Ζωοδόχος Πηγή Ψαλιδίου Ἀμαρουσίου|Ἀμαρούσιον|Χαλκιδικῆς 12;151 21 Ἀμαρούσιον|+30 210-614-2774|||
Metropolitan Chapel|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη καὶ Ὅσιος Παΐσιος Νέων Παλατίων Ὠρωποῦ|Νέα Παλάτια|Κάμπος Νέων Παλατίων;190 15 Ὠρωπός|+30 697-778-2984,+30 22950-32386,+30 694-609-5085|||https://www.imkifissias.gr/index.php/ieroi-naoi/90-ero-nao-st-rxieratik-s-perifereias-ropo/2858-parekklision-ag-kwnstantinou-kai-elenis
Metropolitan Chapel|Ἅγιος Διονύσιος Διονύσου|Διόνυσος|Ἀττάλου 38;145 76 Διόνυσος|+30 210-815-0556|||
Parish Chapel|Ἅγιοι Ἀνάργυροι Χαλκουτσίου|Χαλκούτσι|||||
Parish Chapel|Ἅγιοι Ἀσώματοι Ἀμαρουσίου (Ταξιάρχαι)|Ἀμαρούσιον|||||
Parish Chapel|Ἅγιοι Ἀνάργυροι Λόφου Νυμφῶν Ἁγίου Στεφάνου|Ἅγιος Στέφανος|||||
Parish Chapel|Ἅγιος Ἀθανάσιος Ἀμαρουσίου|Ἀμαρούσιον|||||
Parish Chapel|Ἅγιος Γεώργιος Κοκκιναρᾶ|Κοκκιναρᾶς Κηφισιᾶς|||||
Parish Chapel|Ἅγιος Γεώργιος Ἐκάλης|Ἐκάλη|||||
Parish Chapel|Ἅγιος Γεώργιος ὁ Χιοπολίτης Διονύσου|Διόνυσος|||||
Parish Chapel|Γέννησις τῆς Θεοτόκου Ἐκάλης|Ἐκάλη|||||
Parish Chapel|Γέννησις τῆς Θεοτόκου Συκαμίνου|Συκάμινον|||||
Parish Chapel|Ἅγιος Δημήτριος Πευκοφύτου|Πευκόφυτο Ἁγίου Στεφάνου|||||
Parish Chapel|Ἅγιος Ἰωάννης Πέλικα Ἀμαρουσίου|Ἀμαρούσιον|||||
Parish Chapel|Ἁγία Κυριακή Κηφισιᾶς|Κηφισιά|||||
Parish Chapel|Ἁγία Κυριακή Καλάμου|Κάλαμος|||||
Parish Chapel|Ἁγία Κυριακή Νέας Μάκρης|Νέα Μάκρη|||||
Parish Chapel|Ἁγία Μαρκέλλα Κηφισιᾶς|Κηφισιά|||||
Parish Chapel|Ἁγία Μαρίνα Παραλίας Καλάμου|Παραλία Καλάμου|||||
Parish Chapel|Μεταμόρφωσις τοῦ Σωτῆρος καὶ Ἅγιος Νικόλαος Παραλίας Μαρκοπούλου|Παραλία Μαρκοπούλου|||||
Parish Chapel|Ἁγία Παρασκευή Κηφισιᾶς|Κηφισιά|||||
Parish Chapel|Ἅγιοι Θεόδωροι Ἀνοίξεως|Ἄνοιξη|||||
Parish Chapel|Ἅγιος Στέφανος Δήμου Μεταμορφώσεως|Μεταμόρφωσις|||||
Parish Chapel|Ἅγιος Τιμόθεος Ἐπίσκοπος Εὐρίπου Καλάμου|Κάλαμος|||||
Parish Chapel|Ἅγιος Τιμόθεος Ἐπίσκοπος Προικονήσου Νέων Παλατίων Ὠρωποῦ|Νέα Παλάτια|||||
Parish Chapel|Ἅγιος Φανούριος Παραλίας Μαρκοπούλου|Παραλία Μαρκοπούλου|||||
Parish Chapel|Κοίμησις Θεοτόκου (Παναγίτσα) Κηφισιᾶς|Κηφισιά||+30 210-801-4168|||
Parish Chapel|Ἅγιοι Τεσσαράκοντα Μάρτυρες Κηφισιᾶς|Κηφισιά|||||
Parish Chapel|Παναγία Ξυδοῦς (Γέννησις Θεοτόκου) Κηφισιᾶς|Κηφισιά|||||
Parish Chapel|Παναγία Χελιδονοῦς (Ζωοδόχος Πηγή) Κηφισιᾶς|Κηφισιά|||||
Parish Chapel|Ζωοδόχος Πηγή Νέου Λεβισίου Μαρκοπούλου|Νέο Λεβίσι Μαρκοπούλου|||||
Parish Chapel|Μεταμόρφωσις τοῦ Σωτῆρος Σταμάτας|Σταμάτα|||||
Parish Chapel|Παλαιὰ Μεταμόρφωσις τοῦ Σωτῆρος Κεφαλαρίου Κηφισιᾶς|Κεφαλάρι Κηφισιᾶς|||||
Parish Chapel|Ἅγιοι Ραφαήλ, Νικόλαος καὶ Εἰρήνη Κεφαλαρίου Κηφισιᾶς|Κεφαλάρι Κηφισιᾶς|||||
Parish Chapel|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη καὶ Ἁγία Εἰρήνη Πολιτείας|Πολιτεία Κηφισιᾶς|||||
Parish Chapel|Ἁγία Ἄννα Δήμου Μεταμορφώσεως|Μεταμόρφωσις|||||
Parish Chapel|Ἁγία Παρασκευή Δήμου Μεταμορφώσεως|Μεταμόρφωσις||+30 210-280-1024|||http://inmm.gr/
Institutional Chapel|Μεταμόρφωσις τοῦ Σωτῆρος Ἀνωτάτης Ἐκκλησιαστικῆς Ἀκαδημίας|Κηφισιά|145 61 Κηφισιά||||
Institutional Chapel|Ἅγιος Βασίλειος Σικιαριδείου Ἱδρύματος|Μελίσσια|151 27 Μελίσσια||||
Institutional Chapel|Ἁγία Ἄννα Ὀρφανοτροφείου|Νέα Κηφισιά|145 64 Νέα Κηφισιά||||
Institutional Chapel|Ἅγιος Νεκτάριος ΠΟΕ|Ἐκάλη|145 65 Ἐκάλη||||
Institutional Chapel|Κοίμησις Θεοτόκου Κατασκηνώσεων Δήμου Ἀθηναίων Ἁγίου Ἀνδρέου|Νέα Μάκρη|190 05 Νέα Μάκρη||||
Institutional Chapel|Ἅγιος Γεώργιος Ὀρφανοτροφείου Βουλιαγμένης|Ἀμαρούσιον|151 24 Ἀμαρούσιον||||
Institutional Chapel|Εἴσοδος Θεοτόκου Ἀμαλιείου Ὀρφανοτροφείου|Ἀμαρούσιον|151 24 Ἀμαρούσιον||||
Institutional Chapel|Ἅγιος Παντελεήμων Φίλων Ἀστυνομίας|Ἐκάλη|145 65 Ἐκάλη||||
Institutional Chapel|Ἅγιος Παῦλος Νοσοκομείου ΚΑΤ|Κηφισιά|145 10 Κηφισιά||||
Institutional Chapel|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη Σισμανογλείου|Μελίσσια|151 25 Μελίσσια||||
Institutional Chapel|Ἁγία Τριάς Σχολῶν Μαθητείας ΔΕΗ|Ἄνοιξη|145 65 Ἄνοιξη||||
Institutional Chapel|Ἅγιος Κωνσταντῖνος Νοσοκομείου Ὑγεία|Ἀμαρούσιον|151 22 Ἀμαρούσιον||||
Institutional Chapel|Κοίμησις Θεοτόκου Πέμπτης Παιδικῆς Κατασκηνώσεως Ἁγίου Ἀνδρέου|Νέα Μάκρη|190 05 Νέα Μάκρη||||
Cemetery Chapel|Ἅγιος Ἀνδρέας Κοιμητηρίου Ὠρωποῦ|Ὠρωπός|190 15 Ὠρωπός||||
Cemetery Chapel|Ἁγία Βαρβάρα Κοιμητηρίου Ἁγίου Στεφάνου|Ἅγιος Στέφανος|145 65 Ἅγιος Στέφανος||||
Cemetery Chapel|Ἅγιος Γεώργιος Κοιμητηρίου Ἀμαρουσίου|Ἀμαρούσιον|151 24 Ἀμαρούσιον|+30 210-802-0951|||
Cemetery Chapel|Ἅγιοι Θεόδωροι Κοιμητηρίου Μεταμορφώσεως|Μεταμόρφωσις|144 53 Μεταμόρφωσις|+30 210-279-0955|||
Cemetery Chapel|Ἅγιος Νικόλαος Κοιμητηρίου Μαρκοπούλου|Μαρκόπουλο Ὠρωποῦ|190 15 Ὠρωπός||||
Cemetery Chapel|Ἁγία Παρασκευή Κοιμητηρίου Νέας Ἐρυθραίας|Νέα Ἐρυθραία|146 71 Νέα Ἐρυθραία||||
Cemetery Chapel|Ἅγιος Τρύφων Κοιμητηρίου Κηφισιᾶς|Κηφισιά|154 62 Κηφισιά|+30 210-801-5281|||
Cemetery Chapel|Παμμέγιστοι Ταξιάρχαι Κοιμητηρίου Διονύσου|Διόνυσος|145 76 Διόνυσος||||
Cemetery Chapel|Παμμέγιστοι Ταξιάρχαι Κοιμητηρίου Μελισσίων|Μελίσσια|151 27 Μελίσσια||||
Cemetery Chapel|Παμμέγιστοι Ταξιάρχαι Κοιμητηρίου Νέας Μάκρης|Νέα Μάκρη|190 05 Νέα Μάκρη||||
Cemetery Chapel|Παμμέγιστοι Ταξιάρχαι Κοιμητηρίου Χαλκουτσίου|Χαλκούτσι|190 15 Ὠρωπός||||
Cemetery Chapel|Κοίμησις Θεοτόκου Κοιμητηρίου Μαραθῶνος|Μαραθών|190 07 Μαραθών||||
Cemetery Chapel|Μεταμόρφωσις τοῦ Σωτῆρος Κοιμητηρίου Κάτω Σουλίου|Κάτω Σούλι|190 07 Μαραθών||||
Cemetery Chapel|Τίμιος Πρόδρομος Κοιμητηρίου Γραμματικοῦ|Γραμματικόν|190 07 Μαραθών||||
Armed Forces Chapel|Ἅγιος Νεκτάριος 651 ΤΑΞΥΛΠ|Ἅγιος Στέφανος|||||
Armed Forces Chapel|Ἁγία Βαρβάρα Πυροβολικοῦ Καπανδριτίου|Καπανδρίτι|||||
Armed Forces Chapel|Ἁγία Βαρβάρα 4ης ΤΥΛ Μαλακάσας|Μαλακάσα|||||
Armed Forces Chapel|Ἅγιος Ἀνδρέας Ἀεροπορίας Ἁγίου Ἀνδρέου|Νέα Μάκρη|||||
Armed Forces Chapel|Κοίμησις Θεοτόκου Ἀστυνομίας Ἁγίου Ἀνδρέου|Νέα Μάκρη|||||
Armed Forces Chapel|Ἁγία Παρασκευή Ἀστυνομίας Ἁγίου Ἀνδρέου|Νέα Μάκρη|||||
Armed Forces Chapel|Προφήτης Ἠλίας Βάσεως Ἑλικοπτέρων Ναυτικοῦ Μαραθῶνος|Μαραθών|||||
"""

EXTRA_CHAPEL_DATA = r"""
a|Ἅγιος Νικόλαος Κηφισιᾶς|Κηφισιά
b|Νέος Ἱερὸς Ναὸς Κοιμήσεως Θεοτόκου "Ἄξιόν Ἐστι"|Σταμάτα
b|Ἅγιος Φανούριος Σταμάτας|Σταμάτα
b|Ἁγία Παρασκευή Σταμάτας|Σταμάτα
b|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη Σταμάτας|Σταμάτα
b|Προφήτης Ἠλίας Σταμάτας|Σταμάτα
c|Ἅγιοι Θεόδωροι Ἀμαρουσίου|Ἀμαρούσιον
c|Ἅγιος Βλάσιος Ἀμαρουσίου|Ἀμαρούσιον
c|Ἅγιος Νικόλαος Ἀμαρουσίου Παρεκκλήσιο|Ἀμαρούσιον
c|Ἅγιος Φανούριος Ἀμαρουσίου|Ἀμαρούσιον
e|Ἅγιος Ἀθανάσιος Γραμματικοῦ|Γραμματικόν
e|Ἁγία Τριάς Γραμματικοῦ|Γραμματικόν
e|Ἁγία Μαρίνα Γραμματικοῦ|Γραμματικόν
e|Προφήτης Ἠλίας Γραμματικοῦ|Γραμματικόν
e|Μεταμόρφωσις τοῦ Σωτῆρος Γραμματικοῦ|Γραμματικόν
e|Ἅγιος Σπυρίδων Γραμματικοῦ|Γραμματικόν
e|Ἅγιος Ἰωάννης ὁ Χρυσόστομος Γραμματικοῦ|Γραμματικόν
e|Ἁγία Παρασκευή καὶ Ἁγία Κυριακή Γραμματικοῦ|Γραμματικόν
e|Κοίμησις Θεοτόκου Γραμματικοῦ|Γραμματικόν
e|Ἅγιοι Θεόδωροι Γραμματικοῦ|Γραμματικόν
f|Ἁγία Τριάς Καλάμου|Κάλαμος
f|Ἅγιος Δημήτριος Καλάμου|Κάλαμος
f|Προφήτης Ἠλίας Καλάμου|Κάλαμος
f|Ἁγία Παρασκευή Καλάμου|Κάλαμος
f|Ἁγία Ἄννα Καλάμου|Κάλαμος
f|Ἁγία Σοφία Καλάμου|Κάλαμος
f|Ἅγιος Ἀθανάσιος Καλάμου|Κάλαμος
f|Ἅγιος Ἀντώνιος Καλάμου|Κάλαμος
f|Ἅγιος Ἰωάννης ὁ Θεολόγος Καλάμου|Κάλαμος
f|Ἅγιος Νικόλαος Καλάμου|Κάλαμος
f|Ἅγιος Πέτρος Καλάμου|Κάλαμος
f|Παμμέγιστοι Ταξιάρχαι Καλάμου|Κάλαμος
f|Ἀνάληψις τοῦ Κυρίου Καλάμου|Κάλαμος
f|Ἅγιοι Ἀνάργυροι Κοσμᾶς καὶ Δαμιανὸς Καλάμου|Κάλαμος
f|Ἅγιος Γεώργιος Καλάμου|Κάλαμος
f|Εἴσοδος Θεοτόκου Καλάμου|Κάλαμος
f|Ἅγιοι Κωνσταντῖνος καὶ Ἑλένη Καλάμου|Κάλαμος
f|Ἁγία Βαρβάρα Καλάμου|Κάλαμος
f|Ἅγιος Στυλιανὸς Καλάμου|Κάλαμος
"""

MONASTERY_DATA = r"""
Monastery|Ἱερὰ Μονὴ Ἁγίας Τριάδος Σχοινιᾶ Μαραθῶνος|Σχοινιᾶς Μαραθῶνος|190 07 Μαραθών|+30 22940-63287|||https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai/321-er-mon-gias-triados|men
Monastery|Ἱερὰ Μονὴ Εἰσοδίων τῆς Θεοτόκου - Ἁγίας Φιλοθέης Ἀμαρουσίου|Ἀμαρούσιον|||||https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai/4185-iera-moni-eisodion-tis-theotokou-agias-filotheis-amarousiou|men
Monastery|Ἱερὰ Μονὴ Ὁσίου Ἰωάννου τοῦ Δαμασκηνοῦ Ὠρωποῦ|Σαραντάρι Σκάλας Ὠρωποῦ|Σαραντάρι, Σκάλα Ὠρωποῦ|+30 210-822-0542|thruthtarget@gmail.com||https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai/4184-iera-moni-osiou-ioannou-tou-damaskinoy-oropoy|men
Monastery|Ἱερὰ Μονὴ Παρακλήτου|Ὠρωπός|190 15 Ὠρωπός|+30 22950-32475,+30 22950-31600||https://www.imparaklitou.gr/|https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai/323-era-moni-paraklitou|men
Hesychasterion|Ἱερὸν Ἡσυχαστήριον Ἁγίου Νεκταρίου Μαλακάσας|Μαλακάσα||+30 22950-98363|||https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai/641-eron-syxastirion-g-nektariou-malakasis|men
Hesychasterion|Ἱερὸν Ἡσυχαστήριον Ἁγίου Ραφαήλ Ἄνω Σουλίου Μαραθῶνος|Ἄνω Σούλι Μαραθῶνος||+30 22940-61151,+30 694-435-9953|p.rafael@agiosrafael.gr|https://agiosrafael.gr/index.php/el/|https://www.imkifissias.gr/index.php/i-monai/androai-ierai-monai/4183-ieron-isyxastirion-ag-rafail-ano-souliou-marathonos|men
Monastery|Ἱερὰ Μονὴ Ἁγίας Τριάδος Ματίου Ἀττικῆς|Μάτι Ἀττικῆς|190 09 Μάτι Ἀττικῆς|+30 22940-79240,+30 22940-79241,+30 22940-79242,+30 22940-79243||http://lyreioidryma.gr/|https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/335-era-moni-gias-triados-mati-ttik-s|women
Monastery|Ἱερὰ Μονὴ Ἁγίας Φιλοθέης Ἐκάλης|Ἐκάλη|145 78 Ἐκάλη|+30 210-813-6369,+30 210-813-6094||https://www.imaf.gr/|https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/338-era-moni-gias-filotheis-kalis|women
Monastery|Ἱερὰ Μονὴ Ἁγίου Θεοδοσίου τοῦ Κοινοβιάρχου|Ἅγιος Στέφανος|145 65 Ἅγιος Στέφανος|+30 210-814-0445,+30 210-621-9697|i.m.agioutheodosiou@gmail.com||https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/332-era-moni-giou-theodosiou-to-koinoviarxou|women
Monastery|Ἱερὰ Μονὴ Ἁγίου Παντελεήμονος Ραπεντώσης Διονύσου|Διόνυσος|145 65 Διόνυσος|+30 210-621-2318|i.m.agpanteleimonosdionysou@gmail.com||https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/330-era-moni-giou-panteleimonos-rapentosis-dionysou|women
Monastery|Ἱερὰ Μονὴ Εἰσοδίων Θεοτόκου Μαρκοπούλου Ὠρωποῦ|Μαρκόπουλο Ὠρωποῦ|190 15 Ὠρωπός|+30 22950-32501|||https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/337-era-moni-e-sodi-n-theotokou-markopoulou-ropo|women
Monastery|Ἱερὰ Μονὴ Εὐαγγελισμοῦ τῆς Θεοτόκου καὶ Ἁγίου Ἐφραίμ|Νέα Μάκρη|190 05 Νέα Μάκρη|+30 22940-91202,+30 22940-50128|im_evagelismou_AgiouEfraim@yahoo.gr||https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/339-era-moni-e-aggelismo-t-s-theotokou-kai-giou-fraim|women
Monastery|Ἱερὰ Μονὴ Ἁγίας Σκέπης τῆς Ὑπεραγίας Θεοτόκου|Δροσιά|145 72 Δροσιά|+30 210-813-4653|imagiaskepsis@gmail.com||https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/325-era-moni-t-s-gias-skepis-t-s-peragias-theotokou|women
Hesychasterion|Ἱερὸν Γυναικεῖον Ἡσυχαστήριον "Παναγία Φανερωμένη"|Μπάλα Ροδοπόλεως|145 65 Μπάλα Ροδοπόλεως|+30 210-621-0760|||https://www.imkifissias.gr/index.php/i-monai/gynaikeiai-ierai-monai/326-eron-gynaike-on-syxastirion-panagia-faneromeni|women
"""

PILGRIMAGE_DETAIL_URL = "https://www.imkifissias.gr/index.php/ieroi-naoi/85-ero-nao-a-rxieratik-s-perifereias-kifisi-s/4674-iero-proskynima-panagias-eleftherotrias-kokkinara-kifisias"

ALLOWED_HOSTS = {
    "www.imkifissias.gr", "imkifissias.gr",
    "www.ecclesiagreece.gr", "ecclesiagreece.gr", "www.ecclesia.gr", "ecclesia.gr",
    "www.eleftherotria.gr", "eleftherotria.gr",
    "agiatriadaneakifisia.blogspot.com", "zoodoxosmelission.blogspot.com",
    "agiosgeorgioskifisias.blogspot.com", "agiamarinaekalis.gr", "www.agiamarinaekalis.gr",
    "agia-matrona.gr", "www.agia-matrona.gr", "agios-stefanos.gr", "www.agios-stefanos.gr",
    "panagitsa-anixi.gr", "www.panagitsa-anixi.gr", "enoriarodopolis.gr", "www.enoriarodopolis.gr",
    "panagia-amarousiou.gr", "www.panagia-amarousiou.gr", "inpv.gr", "www.inpv.gr",
    "inagioskosmas.gr", "www.inagioskosmas.gr", "agioiapostoloi.gr", "www.agioiapostoloi.gr",
    "inmm.gr", "www.inmm.gr", "agiavarvaramet.gr", "www.agiavarvaramet.gr",
    "koimisi-theotokou-mati.gr", "www.koimisi-theotokou-mati.gr",
    "agios-andreas.gr", "www.agios-andreas.gr", "aparaskevimal.gr", "www.aparaskevimal.gr",
    "imparaklitou.gr", "www.imparaklitou.gr", "agiosrafael.gr", "www.agiosrafael.gr",
    "imaf.gr", "www.imaf.gr", "lyreioidryma.gr", "www.lyreioidryma.gr",
    "agiamarinamelission.gr", "www.agiamarinamelission.gr",
    "agiospanteleimonas-pefkis.gr", "www.agiospanteleimonas-pefkis.gr",
    "agapostoloi.gr", "www.agapostoloi.gr",
}

FORBIDDEN_PUNCTUATION = re.compile(r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]")
CLERGY_TERMS = re.compile(
    r"\b(?:Ἀρχιμανδρίτης|Αρχιμανδρίτης|Πρωτοπρεσβύτερος|Πρεσβύτερος|Διάκονος|"
    r"Ἡγούμενος|Ηγούμενος|Ἡγουμένη|Ηγουμένη|Μοναχός|Μοναχή)\b",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"^\+30 (?:210-\d{3}-\d{4}|229\d0-\d{5}|69\d-\d{3}-\d{4})$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

TRANSLIT = str.maketrans({
    "Α":"A","Β":"V","Γ":"G","Δ":"D","Ε":"E","Ζ":"Z","Η":"I","Θ":"Th","Ι":"I",
    "Κ":"K","Λ":"L","Μ":"M","Ν":"N","Ξ":"X","Ο":"O","Π":"P","Ρ":"R","Σ":"S",
    "Τ":"T","Υ":"Y","Φ":"F","Χ":"Ch","Ψ":"Ps","Ω":"O",
    "α":"a","β":"v","γ":"g","δ":"d","ε":"e","ζ":"z","η":"i","θ":"th","ι":"i",
    "κ":"k","λ":"l","μ":"m","ν":"n","ξ":"x","ο":"o","π":"p","ρ":"r","σ":"s",
    "ς":"s","τ":"t","υ":"y","φ":"f","χ":"ch","ψ":"ps","ω":"o",
})

RANK_LABELS = {
    "Parish Church": "Parish Church",
    "Pilgrimage Church": "Pilgrimage Church",
    "Metropolitan Chapel": "Metropolitan Chapel",
    "Parish Chapel": "Parish Chapel",
    "Institutional Chapel": "Institutional Chapel",
    "Cemetery Chapel": "Cemetery Chapel",
    "Armed Forces Chapel": "Armed Forces Chapel",
    "Monastery": "Monastery",
    "Hesychasterion": "Hesychasterion",
}


def parse_pipe_rows(block, minimum):
    rows = []
    for number, line in enumerate(block.strip().splitlines(), 1):
        fields = [value.strip() for value in line.split("|")]
        if len(fields) < minimum:
            raise ValueError("raw row %d has %d fields, expected at least %d" % (number, len(fields), minimum))
        rows.append(fields)
    return rows


def split_values(value, delimiter=","):
    return [part.strip() for part in value.split(delimiter) if part.strip()]


def romanize(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value.translate(TRANSLIT)).strip()


def english_name(local, rank):
    value = romanize(local)
    prefixes = (
        "Ieros Naos ", "Iera Moni ", "Ieron Isychastirion ",
        "Ieron Gynaikeion Isychastirion ", "Neos Ieros Naos ",
    )
    for prefix in prefixes:
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    return "%s %s" % (value, RANK_LABELS[rank])


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", romanize(value).casefold()).strip("-") or "body"


def row_from_fields(rank, local, seat_local, address, phones, emails, site, sources, contact_sources):
    item = {
        "parent": PARENT,
        "kind": "monastery" if rank in ("Monastery", "Hesychasterion") else "parish",
        "rank": rank,
        "name": english_name(local, rank),
        "local": local,
        "seat": romanize(seat_local),
        "country": "GR",
        "sources": list(dict.fromkeys(sources)),
    }
    if address:
        parts = split_values(address, ";")
        if parts and parts[-1] != "Ελλάδα":
            parts.append("Ελλάδα")
        item["address"] = parts
    if phones:
        item["phones"] = split_values(phones)
    if emails:
        item["emails"] = split_values(emails)
    if site:
        item["site"] = site
    if item.get("phones") or item.get("emails") or item.get("site"):
        item["contact_sources"] = list(dict.fromkeys(contact_sources))
        item["contact_checked"] = CHECKED
    return item


def make_rows():
    rows = []
    parish_rows = parse_pipe_rows(PARISH_DATA, 8)
    if len(parish_rows) != 63:
        raise ValueError("parish source table drifted: %d" % len(parish_rows))
    for region, local, seat, address, phones, emails, site, detail, *extra in parish_rows:
        if extra or region not in REGIONS:
            raise ValueError("invalid parish source row")
        sources = [REGIONS[region]["admin"], REGIONS[region]["listing"], LEGAL_URL]
        contact_sources = [REGIONS[region]["admin"]]
        if detail:
            sources[1] = detail
            contact_sources.append(detail)
        if site:
            contact_sources.append(site)
        rows.append(row_from_fields(
            "Parish Church", local, seat, address, phones, emails, site, sources, contact_sources
        ))

    category_rows = parse_pipe_rows(CATEGORY_DATA, 7)
    if len(category_rows) != 76:
        raise ValueError("category source table drifted: %d" % len(category_rows))
    for fields in category_rows:
        fields += [""] * (8 - len(fields))
        rank, local, seat, address, phones, emails, site, detail = fields[:8]
        if rank not in CATEGORY_URLS:
            raise ValueError("unknown current category rank: %s" % rank)
        sources = [CATEGORY_URLS[rank]]
        contact_sources = [CATEGORY_URLS[rank]]
        if rank == "Pilgrimage Church":
            sources.extend([REGIONS["a"]["listing"], PILGRIMAGE_DETAIL_URL])
            contact_sources.append(PILGRIMAGE_DETAIL_URL)
        if detail:
            sources.append(detail)
            contact_sources.append(detail)
        if site:
            contact_sources.append(site)
        rows.append(row_from_fields(
            rank, local, seat, address, phones, emails, site, sources, contact_sources
        ))

    extra_rows = parse_pipe_rows(EXTRA_CHAPEL_DATA, 3)
    if len(extra_rows) != 39:
        raise ValueError("linked chapel source table drifted: %d" % len(extra_rows))
    for region, local, seat, *extra in extra_rows:
        if extra or region not in REGIONS:
            raise ValueError("invalid linked chapel source row")
        rows.append(row_from_fields(
            "Parish Chapel", local, seat, "", "", "", "",
            [REGIONS[region]["listing"]], [],
        ))

    monastery_rows = parse_pipe_rows(MONASTERY_DATA, 9)
    if len(monastery_rows) != 14:
        raise ValueError("monastery source table drifted: %d" % len(monastery_rows))
    for rank, local, seat, address, phones, emails, site, detail, group, *extra in monastery_rows:
        if extra or group not in ("men", "women"):
            raise ValueError("invalid monastery source row")
        listing = MEN_MONASTERIES_URL if group == "men" else WOMEN_MONASTERIES_URL
        sources = [detail, listing, PROFILE_URL]
        contact_sources = [detail, PROFILE_URL]
        if site:
            contact_sources.append(site)
        rows.append(row_from_fields(
            rank, local, seat, address, phones, emails, site, sources, contact_sources
        ))

    for index, item in enumerate(rows, 1):
        item["id"] = "gr-kifisia-%03d-%s" % (index, slug(item["local"]))
    return rows


ROWS = make_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 192
EXPECTED_OWNER_COUNTS = {PARENT: 192}
EXPECTED_KINDS = {"monastery": 14, "parish": 178}
EXPECTED_RANKS = {
    "Armed Forces Chapel": 7,
    "Cemetery Chapel": 14,
    "Hesychasterion": 3,
    "Institutional Chapel": 13,
    "Metropolitan Chapel": 7,
    "Monastery": 11,
    "Parish Chapel": 73,
    "Parish Church": 63,
    "Pilgrimage Church": 1,
}
EXPECTED_COVERAGE = (87, 87, 134, 18, 20, 22, 109)
EXISTING_PARENTS = {PARENT}


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc.casefold() not in ALLOWED_HOSTS:
        raise ValueError("%s carries a non-competent or unaudited source: %s" % (label, value))


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
    has_contact = bool(item.get("phones") or item.get("emails") or item.get("site"))
    if has_contact:
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks exact current contact provenance" % item.get("id"))
    elif contact_sources or item.get("contact_checked"):
        raise ValueError("%s carries contact audit metadata without a phone, email, or site" % item.get("id"))
    if len(contact_sources) > 3:
        raise ValueError("%s carries too many contact sources" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
    for phone in item.get("phones") or []:
        if not PHONE_RE.fullmatch(phone):
            raise ValueError("%s carries malformed phone %s" % (item.get("id"), phone))
    for email in item.get("emails") or []:
        if not EMAIL_RE.fullmatch(email):
            raise ValueError("%s carries malformed email %s" % (item.get("id"), email))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if any(host in item["site"].casefold() for host in ("facebook.", "youtube.", "maps.")):
            raise ValueError("%s classifies a social or map URL as a direct body site" % item.get("id"))
        if item["site"] in sources:
            raise ValueError("%s mixes its direct body site with higher-level roster sources" % item.get("id"))
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
        raise ValueError("Kifisia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kifisia candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_named_parishes": 63,
        "current_pilgrimages": 1,
        "current_metropolitan_chapels": 7,
        "current_parish_chapels": 73,
        "current_institutional_chapels": 13,
        "current_cemetery_chapels": 14,
        "current_armed_forces_chapels": 7,
        "current_monasteries_and_hesychasteria": 14,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Kifisia ledger summary drifted at %s" % key)
    if expected_coverage is not None:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites", "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Kifisia ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Kifisia ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kifisia ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or entry.get("id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Kifisia candidate IDs repeat")
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
            raise ValueError("duplicate Kifisia ID: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has wrong country" % row_id)
        if item.get("kind") not in ("parish", "monastery"):
            raise ValueError("%s has invalid kind" % row_id)
        if item.get("rank") not in RANK_LABELS:
            raise ValueError("%s has invalid rank" % row_id)
        for field in ("name", "local", "seat", "rank"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        rendered = json.dumps(item, ensure_ascii=False)
        if FORBIDDEN_PUNCTUATION.search(rendered):
            raise ValueError("%s carries forbidden punctuation" % row_id)
        if CLERGY_TERMS.search(rendered):
            raise ValueError("%s carries a clergy or monastic personal title" % row_id)
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
        raise ValueError("Kifisia English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Kifisia English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Kifisia parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Kifisia kind totals drifted: %r" % dict(kind_counts))
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Kifisia rank totals drifted: %r" % dict(rank_counts))
    coverage = coverage_tuple(result)
    if EXPECTED_COVERAGE is not None and coverage != EXPECTED_COVERAGE:
        raise ValueError("Kifisia contact coverage drifted: %r" % (coverage,))
    validate_ledger(coverage)
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_live_source(url, body_site=False):
    request_url = url.replace("https://www.imkifissias.gr", "https://imkifissias.gr")
    curl = shutil.which("curl")
    if curl:
        last_error = None
        curl_timeout = "45" if body_site else "25"
        process_timeout = 50 if body_site else 30
        for attempt in range(3):
            command = [
                curl, "--location", "--silent", "--show-error", "--compressed",
                "--max-time", curl_timeout, "--user-agent", "Mozilla/5.0 Plithos directory source audit",
                "--write-out", "\n__PLITHOS_STATUS__%{http_code}\n__PLITHOS_TYPE__%{content_type}",
            ]
            if urlparse(request_url).netloc.casefold() in (
                "koimisi-theotokou-mati.gr", "www.koimisi-theotokou-mati.gr"
            ):
                command.append("--insecure")
            command.append(request_url)
            completed = subprocess.run(
                command, capture_output=True, timeout=process_timeout
            )
            marker = b"\n__PLITHOS_STATUS__"
            if completed.returncode == 0 and marker in completed.stdout:
                payload, trailer = completed.stdout.rsplit(marker, 1)
                status_text, content_type = trailer.split(b"\n__PLITHOS_TYPE__", 1)
                status = int(status_text.decode("ascii"))
                content_type = content_type.decode("ascii", "replace").casefold()
                if body_site and status in (403, 429):
                    return None
                if status < 200 or status >= 400:
                    last_error = "HTTP %d" % status
                elif url.casefold().endswith(".pdf") or "pdf" in content_type:
                    if not payload.startswith(b"%PDF") or len(payload) < 100000:
                        raise ValueError("invalid legal PDF payload at %s" % url)
                    return None
                elif not any(token in content_type for token in ("html", "text", "xml", "rss", "atom")):
                    raise ValueError("unexpected content type at %s: %s" % (url, content_type))
                else:
                    return payload.decode("utf-8", "replace")
            else:
                last_error = completed.stderr.decode("utf-8", "replace").strip() or (
                    "curl exit %d" % completed.returncode
                )
            if attempt < 2:
                time.sleep(2 + attempt * 2)
        raise ValueError("live URL failed at %s: %s" % (url, last_error))

    request = Request(request_url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8",
        "Connection": "close",
    })
    last_error = None
    for attempt in range(3):
        try:
            try:
                response = urlopen(request, timeout=20)
            except URLError as exc:
                if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
                    raise
                response = urlopen(request, timeout=20, context=ssl._create_unverified_context())
            with response:
                content_type = response.headers.get("Content-Type", "").lower()
                payload = response.read()
            if url.casefold().endswith(".pdf") or "pdf" in content_type:
                if not payload.startswith(b"%PDF") or len(payload) < 100000:
                    raise ValueError("invalid legal PDF payload at %s" % url)
                return None
            if not any(token in content_type for token in ("html", "text", "xml", "rss", "atom")):
                raise ValueError("unexpected content type at %s: %s" % (url, content_type))
            return payload.decode("utf-8", "replace")
        except HTTPError as exc:
            if body_site and exc.code in (403, 429):
                return None
            last_error = exc
            if exc.code not in (429, 500, 502, 503, 504):
                raise
        except (URLError, TimeoutError) as exc:
            last_error = exc
        if attempt < 2:
            time.sleep(2 + attempt * 2)
    raise ValueError("live URL failed at %s: %s" % (url, last_error))


def listing_titles(payload, url):
    path = urlparse(url).path.rstrip("/")
    found = []
    for href, title in re.findall(
        r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', payload, re.IGNORECASE
    ):
        href = html.unescape(href)
        if not re.search(re.escape(path) + r"/\d+-", href):
            continue
        title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", title))).strip()
        if title:
            found.append((href, title))
    return list(dict.fromkeys(found))


def live_feed_titles(url):
    titles = []
    for start in range(0, 100, 10):
        separator = "&" if "?" in url else "?"
        payload = fetch_live_source(
            "%s%sformat=feed&type=rss&start=%d" % (url, separator, start)
        )
        batch = re.findall(r"<item>[\s\S]*?<title>([\s\S]*?)</title>", payload, re.IGNORECASE)
        batch = [
            re.sub(r"\s+", " ", html.unescape(re.sub(r"<!\[CDATA\[|\]\]>", "", title))).strip()
            for title in batch
        ]
        titles.extend(batch)
        if len(batch) < 10:
            break
    return titles


def check_markers(payload, url, markers):
    text = normalize_source_text(payload)
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("live Kifisia marker failed at %s: %s" % (url, marker))


def check_live_sources():
    listing_specs = [(value["listing"], value["count"]) for value in REGIONS.values()]
    listing_specs.extend(((MEN_MONASTERIES_URL, 6), (WOMEN_MONASTERIES_URL, 8)))
    for url, expected in listing_specs:
        titles = live_feed_titles(url)
        if len(titles) != expected:
            raise ValueError("live Kifisia listing count drifted at %s: %d" % (url, len(titles)))

    admin_markers = {
        REGIONS["a"]["admin"]: ("Ἅγ. Δημήτριος Κηφισιᾶς", "Ζωοδ.Πηγή Mελισσίων"),
        REGIONS["b"]["admin"]: ("Kοιμ. Θεοτόκου Ἅγ. Στεφάνου", "Κοίμ. Θεοτόκου Σταμάτας"),
        REGIONS["c"]["admin"]: ("Ἅγ. Ἀνάργυροι Ἀμαρουσίου", "Παναγία Βλαχερνῶν Ἀμαρουσίου"),
        REGIONS["d"]["admin"]: ("Ἅγ. Απόστολοι Πεύκης", "Ζωοδ. Πηγή Λυκοβρύσεως"),
        REGIONS["e"]["admin"]: ("Κοίμ. Θεοτόκου", "Ἁγ. Ἰωάννης Πρόδρομος"),
        REGIONS["f"]["admin"]: ("Ἅγ. Ἀποστ. Πέτρου & Παύλου", "Ἁγ. Ἀνδρέας"),
    }
    for url, markers in admin_markers.items():
        check_markers(fetch_live_source(url), url, markers)

    category_markers = {
        CATEGORY_URLS["Pilgrimage Church"]: ("Παναγία Ἐλευθερώτρια",),
        CATEGORY_URLS["Metropolitan Chapel"]: ("Ἀποστόλου Ἰακώβου", "Ὁσίου Παϊσίου"),
        CATEGORY_URLS["Parish Chapel"]: ("Ἁγ. Ἀναργύρων Χαλκουτσίου", "Ἁγ. Παρασκευῆς Δ. Μεταμορφώσεως"),
        CATEGORY_URLS["Institutional Chapel"]: ("Ἀνωτάτης Ἐκκλ. Ἀκαδημίας", "Θεραπευτηρίου", "Ὑγεία"),
        CATEGORY_URLS["Cemetery Chapel"]: ("Ἅγ. Ἀνδρέας Ὠρωποῦ", "Τιμίου Προδρόμου Γραμματικοῦ"),
        CATEGORY_URLS["Armed Forces Chapel"]: ("651", "Βάση Ἑλικοπτέρων"),
    }
    for url, markers in category_markers.items():
        check_markers(fetch_live_source(url), url, markers)

    check_markers(fetch_live_source(STRUCTURE_URL), STRUCTURE_URL, (
        "Ἐνοριακοί 64", "Κοιμητηρίων 11", "Μοναστηριακοί 10",
    ))
    check_markers(fetch_live_source(PROFILE_URL), PROFILE_URL, (
        "Κηφισίας, Αμαρουσίου, Ωρωπού και Μαραθώνος",
        "Ανδρικές Ιερές Μονές", "Γυναικείο Ιερό Ησυχαστήριο",
    ))
    fetch_live_source(LEGAL_URL)

    site_urls = sorted({item["site"] for item in ROWS if item.get("site")})
    failures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_live_source, url, True): url for url in site_urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as exc:
                failures.append("%s: %s" % (url, exc))
    if failures:
        raise ValueError("direct body site live checks failed: " + "; ".join(failures))
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
        print("Kifisia live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Kifisia check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
