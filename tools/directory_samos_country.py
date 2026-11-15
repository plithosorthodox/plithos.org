#!/usr/bin/env python3
"""Validate exact named Samos and Ikaria bodies from official sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_samos_country.py --check
    python tools/directory_samos_country.py --dump
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "samos_country.json"
)
PARENT = "ep-samos"
SAMOS_ROSTER = (
    "https://www.imsamou.gr/index.php/el/mitropoli/"
    "ieroi-naoi-kai-mones/ieroi-naoi-samou"
)
IKARIA_ROSTER = (
    "https://www.imsamou.gr/index.php/el/mitropoli/"
    "ieroi-naoi-kai-mones/ieroi-naoi-ikarias"
)
MONASTERY_PAGE = (
    "https://www.imsamou.gr/index.php/el/mitropoli/ieres-mones"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-samoy-ikarias/"
)


# local dedication | local seat | archiepiscopal region | postal code
SAMOS_ROWS = r'''
ΑΓ.ΓΕΩΡΓΙΟΥ|ΠΑΛΑΙΟΚΑΣΤΡΟ|ΣΑΜΟΥ|83100
ΑΓ.ΘΕΟΔΩΡΟΥ|ΣΑΜΟΣ|ΣΑΜΟΥ|83100
ΑΓ.ΙΩΑΝ.ΘΕΟΛΟΓΟΥ|ΒΟΥΡΛΙΩΤΕΣ|ΣΑΜΟΥ|83100
ΑΓ.ΝΙΚΟΛΑΟΥ|ΑΥΛΑΚΙΑ|ΣΑΜΟΥ|83200
ΑΓ.ΝΙΚΟΛΑΟΥ|ΚΟΚΚΑΡΙ|ΣΑΜΟΥ|83100
ΑΓ.ΝΙΚΟΛΑΟΥ|ΣΑΜΟΣ|ΣΑΜΟΥ|83100
ΑΓ.ΣΠΥΡΙΔΩΝΟΣ|ΣΑΜΟΣ|ΣΑΜΟΥ|83100
ΑΓ.ΧΑΡΑΛΑΜΠΟΥΣ|ΣΑΜΟΣ|ΣΑΜΟΥ|83100
ΓΕΝ.ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ|ΑΓ.ΚΩΝ/ΝΟΣ|ΣΑΜΟΥ|83200
ΕΙΣ.ΘΕΟΤΟΚΟΥ|ΒΑΘΥ|ΣΑΜΟΥ|83100
ΖΩΟΔ.ΠΗΓΗΣ|ΜΑΝΩΛΑΤΕΣ|ΣΑΜΟΥ|83200
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΒΑΘΥ|ΣΑΜΟΥ|83100
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΒΟΥΡΛΙΩΤΕΣ|ΣΑΜΟΥ|83100
ΜΕΤΑΜ.ΣΩΤΗΡΟΣ|ΒΑΘΥ|ΣΑΜΟΥ|83100
ΠΡΟΦ.ΗΛΙΑ|ΣΤΑΥΡΙΝΗΔΕΣ|ΣΑΜΟΥ|83200
ΣΥΛ.ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ|ΑΜΠΕΛΟΣ|ΣΑΜΟΥ|83200
ΑΓ.ΓΕΩΡΓΙΟΥ|ΜΑΥΡΑΤΖΑΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΑΓ.ΔΗΜΗΤΡΙΟΥ|ΜΥΤΙΛΗΝΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83101
ΑΓ.ΔΗΜΗΤΡΙΟΥ|ΠΑΝΔΡΟΣΟ|ΠΥΘΑΓΟΡΕΙΟΥ|83104
ΑΓ.ΝΙΚΟΛΑΟΥ|ΜΥΤΙΛΗΝΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83101
ΑΓ.ΠΑΝΤΕΛΕΗΜΟΝΟΣ|ΚΟΥΜΑΡΑΔΑΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83104
ΑΓ.ΤΡΙΑΔΟΣ|ΠΑΓΩΝΔΑΣ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΑΠΟΣ.ΠΑΥΛΟΥ|ΗΡΑΙΟΝ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΓΕΝ.ΧΡΙΣΤΟΥ|ΠΑΓΩΝΔΑΣ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΖΩΟΔ.ΠΗΓΗΣ|ΜΕΣΟΓΕΙΟΝ|ΠΥΘΑΓΟΡΕΙΟΥ|83104
ΖΩΟΔ.ΠΗΓΗΣ|ΜΥΛΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΜΥΤΙΛΗΝΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83101
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΠΥΡΓΟΣ|ΠΥΘΑΓΟΡΕΙΟΥ|83104
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΧΩΡΑ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΜΕΤΑΜ.ΣΩΤΗΡΟΣ|ΠΥΘΑΓΟΡΕΙΟ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΟΣ.ΑΝΤΩΝΙΟΥ|ΜΥΤΙΛΗΝΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83101
ΟΣ.ΜΑΤΡΩΝΗΣ|ΜΥΤΙΛΗΝΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83101
ΟΣ.ΠΑΡΑΣΚΕΥΗΣ|ΧΩΡΑ|ΠΥΘΑΓΟΡΕΙΟΥ|83103
ΤΑΞ/ΧΟΥ ΜΙΧΑΗΛ|ΣΠΑΘΑΡΑΙΟΙ|ΠΥΘΑΓΟΡΕΙΟΥ|83104
ΑΓ.ΓΕΩΡΓΙΟΥ|ΚΑΛΛΙΘΕΑ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΑΓ.ΓΕΩΡΓΙΟΥ|ΣΚΟΥΡΕΙΚΑ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83104
ΑΓ.ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ|ΔΡΑΚΑΙΟΙ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΑΓ.ΝΙΚΟΛΑΟΥ|ΚΟΥΜΕΙΚΑ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83104
ΑΓ.ΝΙΚΟΛΑΟΥ|ΟΡΜ.ΜΑΡΑΘΟΚΑΜΠΟΥ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΑΓ.ΤΡΙΑΔΟΣ|ΜΑΡΑΘΟΚΑΜΠΟΣ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΟΣ.ΑΝΤΩΝΙΟΥ|ΜΑΡΑΘΟΚΑΜΠΟΣ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΟΣ.ΠΑΡΑΣΚΕΥΗΣ|ΜΑΡΑΘΟΚΑΜΠΟΣ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΠΡΟΦ.ΗΛΙΑ|ΜΑΡΑΘΟΚΑΜΠΟΣ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83102
ΤΑΞ/ΧΟΥ ΜΙΧΑΗΛ|ΝΕΟΧΩΡΙΟΝ|ΜΑΡΑΘΟΚΑΜΠΟΥ|83104
ΑΓ.ΑΘΑΝΑΣΙΟΥ|ΥΔΡΟΥΣΑ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΓΕΩΡΓΙΟΥ|ΠΛΑΤΑΝΟΣ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΘΕΟΔΩΡΩΝ|ΑΓ.ΘΕΟΔΩΡΟΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΙΩΑΝ.ΘΕΟΛΟΓΟΥ|ΝΙΚΟΛΟΥΔΕΣ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΛΕΚΚΑ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΙΩΑΝ.ΧΡΥΣΟΣΤΟΜΟΥ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΝΙΚΟΛΑΟΥ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΑΓ.ΠΑΝΤΕΛΕΗΜΟΝΟΣ|ΤΣΟΥΡΛΑΙΟΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΓΕΝ.ΘΕΟΤΟΚΟΥ|ΚΟΝΤΕΙΚΑ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΓΕΝ.ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΓΕΝ.ΧΡΙΣΤΟΥ|ΠΑΛ.ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΕΙΣ.ΘΕΟΤΟΚΟΥ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΕΥΑΓΓ.ΘΕΟΤΟΚΟΥ|ΚΟΣΜΑΔΑΙΟΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΖΩΟΔ.ΠΗΓΗΣ|ΣΟΥΡΡΗΔΕΣ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΚΑΣΤΑΝΙΑ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΚΟΝΤΑΚΕΙΚΑ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΟΣ.ΜΑΤΡΩΝΗΣ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΟΣ.ΠΑΡΑΣΚΕΥΗΣ|ΣΑΚΟΥΛΕΙΚΑ|ΚΑΡΛΟΒΑΣΟΥ|83200
ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ|ΚΑΡΛΟΒΑΣΙ|ΚΑΡΛΟΒΑΣΟΥ|83200
'''


IKARIA_ROWS = r'''
ΑΓ.ΑΝΑΡΓΥΡΩΝ|ΘΕΡΜΑ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΓΕΩΡΓΙΟΥ|ΑΜΑΛΟ|ΑΓ.ΚΗΡΥΚΟΥ|83301
ΑΓ.ΓΡΗΓΟΡΙΟΥ|ΓΛΑΡΕΔΕΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΔΗΜΗΤΡΙΟΥ|ΚΑΤΑΦΥΓΙΟ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΜΑΥΡΑΤΟ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΜΑΥΡΙΚΑΤΟ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΙΩΑΝ.ΧΡΥΣΟΣΤΟΜΟΥ|ΧΡΥΣΟΣΤΟΜΟ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΝΙΚΟΛΑΟΥ|ΑΓ.ΚΗΡΥΚΟΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΝΙΚΟΛΑΟΥ|ΚΑΡΚΙΝΑΓΡΙ|ΑΓ.ΚΗΡΥΚΟΥ|83301
ΑΓ.ΝΙΚΟΛΑΟΥ|ΜΑΓΓΑΝΙΤΗΣ|ΑΓ.ΚΗΡΥΚΟΥ|83301
ΑΓ.ΠΑΝΤΕΛΕΗΜΟΝΟΣ|ΑΓ.ΚΗΡΥΚΟΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΓΕΝ.ΘΕΟΤΟΚΟΥ|ΠΛΑΓΙΑ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΕΥΑΓΓ.ΘΕΟΤΟΚΟΥ|ΚΟΥΝΤΟΥΜΑΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΑΓ.ΚΗΡΥΚΟΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΜΟΝΟΚΑΜΠΙ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΜΕΤΑΜ.ΣΩΤΗΡΟΣ|ΓΛΑΡΕΔΕΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΟΣ.ΜΑΤΡΩΝΗΣ|ΠΕΡΔΙΚΙ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΤΑΞΙΑΡΧΩΝ|ΞΥΛΟΣΥΡΤΗΣ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΤΑΞΙΑΡΧΩΝ|ΠΛΩΜΑΡΙ|ΑΓ.ΚΗΡΥΚΟΥ|83300
ΑΓ.ΑΝΑΡΓΥΡΩΝ|ΚΑΡΑΒΟΣΤΑΜΟ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΕΙΡΗΝΗΣ|ΚΑΜΠΟΣ ΦΡΑΝΤΑΤΟΥ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΔΑΦΝΗ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΚΑΡΑΒΟΣΤΑΜΟ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΚΕΡΑΜΕ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΚΩΝ/ΝΟΥ|ΑΥΛΑΚΙ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΜΑΡΙΝΑΣ|ΑΡΕΘΟΥΣΑ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΧΑΡΑΛΑΜΠΟΥΣ|ΕΥΔΗΛΟΣ|ΕΥΔΗΛΟΥ|83302
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΑΚΑΜΑΤΡΑ|ΕΥΔΗΛΟΥ|83302
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΚΟΣΣΟΙΚΙΑ|ΕΥΔΗΛΟΥ|83302
ΚΟΙΜ.ΘΕΟΤΟΚΟΥ|ΣΤΥΛΙΟ|ΕΥΔΗΛΟΥ|83302
ΟΣ.ΠΑΡΑΣΚΕΥΗΣ|ΠΕΤΡΟΠΟΥΛΙ|ΕΥΔΗΛΟΥ|83302
ΑΓ.ΔΗΜΗΤΡΙΟΥ|ΡΑΧΕΣ|ΡΑΧΩΝ|83301
ΑΓ.ΕΙΡΗΝΗΣ|ΚΟΥΝΙΑΔΟΙ|ΡΑΧΩΝ|83301
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΜΑΝΔΡΙΑ|ΡΑΧΩΝ|83301
ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ|ΠΡΟΕΣΠΕΡΑ|ΡΑΧΩΝ|83301
ΑΓ.ΝΙΚΟΛΑΟΥ|ΑΡΜΕΝΙΣΤΗΣ|ΡΑΧΩΝ|83301
ΑΓ.ΝΙΚΟΛΑΟΥ|ΓΙΑΛΙΣΚΑΡΙ|ΡΑΧΩΝ|83301
ΑΓ.ΠΟΛΥΚΑΡΠΟΥ|ΑΓ.ΠΟΛΥΚΑΡΠΟΣ|ΡΑΧΩΝ|83301
ΑΓ.ΤΡΙΑΔΟΣ|ΡΑΧΕΣ|ΡΑΧΩΝ|83301
ΜΕΤΑΜ.ΣΩΤΗΡΟΣ|ΡΑΧΕΣ|ΡΑΧΩΝ|83301
ΜΕΤΑΜ.ΣΩΤΗΡΟΣ|ΦΡΑΝΤΑΤΟ|ΡΑΧΩΝ|83302
ΠΡΟΦ.ΔΑΝΙΗΛ|ΜΑΡΑΘΟ|ΡΑΧΩΝ|83302
ΠΡΟΦ.ΗΛΙΑ|ΒΡΑΚΑΔΕΣ|ΡΑΧΩΝ|83301
ΠΡΟΦ.ΗΛΙΑ|ΠΗΓΗ|ΡΑΧΩΝ|83302
ΠΡΟΦ.ΗΛΙΑ|ΡΑΧΕΣ|ΡΑΧΩΝ|83301
ΑΓ.ΓΕΩΡΓΙΟΥ|ΘΥΜΑΙΝΑ|ΦΟΥΡΝΩΝ|83400
ΑΓ.ΝΙΚΟΛΑΟΥ|ΦΟΥΡΝΟΙ|ΦΟΥΡΝΩΝ|83400
ΖΩΟΔ.ΠΗΓΗΣ|ΧΡΥΣΟΜΗΛΙΑ|ΦΟΥΡΝΩΝ|83400
'''


DEDICATIONS = {
    "ΑΓ.ΑΘΑΝΑΣΙΟΥ": "Saint Athanasius",
    "ΑΓ.ΑΝΑΡΓΥΡΩΝ": "Holy Unmercenaries",
    "ΑΓ.ΓΕΩΡΓΙΟΥ": "Saint George",
    "ΑΓ.ΓΡΗΓΟΡΙΟΥ": "Saint Gregory",
    "ΑΓ.ΔΗΜΗΤΡΙΟΥ": "Saint Demetrius",
    "ΑΓ.ΕΙΡΗΝΗΣ": "Saint Irene",
    "ΑΓ.ΘΕΟΔΩΡΟΥ": "Saint Theodore",
    "ΑΓ.ΘΕΟΔΩΡΩΝ": "Saints Theodore",
    "ΑΓ.ΙΩΑΝ.ΘΕΟΛΟΓΟΥ": "Saint John the Theologian",
    "ΑΓ.ΙΩΑΝ.ΠΡΟΔΡΟΜΟΥ": "Saint John the Forerunner",
    "ΑΓ.ΙΩΑΝ.ΧΡΥΣΟΣΤΟΜΟΥ": "Saint John Chrysostom",
    "ΑΓ.ΚΩΝ/ΝΟΥ": "Saint Constantine",
    "ΑΓ.ΚΩΝ/ΝΟΥ & ΕΛΕΝΗΣ": "Saints Constantine and Helen",
    "ΑΓ.ΜΑΡΙΝΑΣ": "Saint Marina",
    "ΑΓ.ΝΙΚΟΛΑΟΥ": "Saint Nicholas",
    "ΑΓ.ΠΑΝΤΕΛΕΗΜΟΝΟΣ": "Saint Panteleimon",
    "ΑΓ.ΠΟΛΥΚΑΡΠΟΥ": "Saint Polycarp",
    "ΑΓ.ΣΠΥΡΙΔΩΝΟΣ": "Saint Spyridon",
    "ΑΓ.ΤΡΙΑΔΟΣ": "Holy Trinity",
    "ΑΓ.ΧΑΡΑΛΑΜΠΟΥΣ": "Saint Charalambos",
    "ΑΠΟΣ.ΠΑΥΛΟΥ": "Apostle Paul",
    "ΓΕΝ.ΘΕΟΤΟΚΟΥ": "Nativity of the Theotokos",
    "ΓΕΝ.ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ": "Nativity of Saint John the Forerunner",
    "ΓΕΝ.ΧΡΙΣΤΟΥ": "Nativity of Christ",
    "ΕΙΣ.ΘΕΟΤΟΚΟΥ": "Entry of the Theotokos",
    "ΕΥΑΓΓ.ΘΕΟΤΟΚΟΥ": "Annunciation of the Theotokos",
    "ΖΩΟΔ.ΠΗΓΗΣ": "Life-Giving Spring",
    "ΚΟΙΜ.ΘΕΟΤΟΚΟΥ": "Dormition of the Theotokos",
    "ΜΕΤΑΜ.ΣΩΤΗΡΟΣ": "Transfiguration of the Savior",
    "ΟΣ.ΑΝΤΩΝΙΟΥ": "Saint Anthony",
    "ΟΣ.ΜΑΤΡΩΝΗΣ": "Saint Matrona",
    "ΟΣ.ΠΑΡΑΣΚΕΥΗΣ": "Saint Paraskevi",
    "ΠΡΟΦ.ΔΑΝΙΗΛ": "Prophet Daniel",
    "ΠΡΟΦ.ΗΛΙΑ": "Prophet Elijah",
    "ΣΥΛ.ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ": "Synaxis of Saint John the Forerunner",
    "ΤΑΞ/ΧΟΥ ΜΙΧΑΗΛ": "Archangel Michael",
    "ΤΑΞΙΑΡΧΩΝ": "Holy Archangels",
    "ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ": "Holy Cross",
}


SEAT_NAMES = {
    "ΑΓ.ΘΕΟΔΩΡΟΙ": "Agioi Theodoroi",
    "ΑΓ.ΚΗΡΥΚΟΣ": "Agios Kirykos",
    "ΑΓ.ΚΩΝ/ΝΟΣ": "Agios Konstantinos",
    "ΑΓ.ΠΟΛΥΚΑΡΠΟΣ": "Agios Polykarpos",
    "ΑΚΑΜΑΤΡΑ": "Akamatra",
    "ΑΜΑΛΟ": "Amalo",
    "ΑΜΠΕΛΟΣ": "Ambelos",
    "ΑΡΕΘΟΥΣΑ": "Arethousa",
    "ΑΡΜΕΝΙΣΤΗΣ": "Armenistis",
    "ΑΥΛΑΚΙ": "Avlaki",
    "ΑΥΛΑΚΙΑ": "Avlakia",
    "ΒΑΘΥ": "Vathy",
    "ΒΟΥΡΛΙΩΤΕΣ": "Vourliotes",
    "ΒΡΑΚΑΔΕΣ": "Vrakades",
    "ΓΙΑΛΙΣΚΑΡΙ": "Gialiskari",
    "ΓΛΑΡΕΔΕΣ": "Glaredes",
    "ΔΑΦΝΗ": "Dafni",
    "ΔΡΑΚΑΙΟΙ": "Drakaioi",
    "ΕΥΔΗΛΟΣ": "Evdilos",
    "ΗΡΑΙΟΝ": "Heraion",
    "ΘΕΡΜΑ": "Therma",
    "ΘΥΜΑΙΝΑ": "Thymaina",
    "ΚΑΛΛΙΘΕΑ": "Kallithea",
    "ΚΑΜΠΟΣ ΦΡΑΝΤΑΤΟΥ": "Kampos Frantatou",
    "ΚΑΡΑΒΟΣΤΑΜΟ": "Karavostamo",
    "ΚΑΡΚΙΝΑΓΡΙ": "Karkinagri",
    "ΚΑΡΛΟΒΑΣΙ": "Karlovasi",
    "ΚΑΣΤΑΝΙΑ": "Kastania",
    "ΚΑΤΑΦΥΓΙΟ": "Katafygio",
    "ΚΕΡΑΜΕ": "Kerame",
    "ΚΟΚΚΑΡΙ": "Kokkari",
    "ΚΟΝΤΑΚΕΙΚΑ": "Kontakeika",
    "ΚΟΝΤΕΙΚΑ": "Konteika",
    "ΚΟΣΜΑΔΑΙΟΙ": "Kosmadaioi",
    "ΚΟΣΣΟΙΚΙΑ": "Kossoikia",
    "ΚΟΥΜΑΡΑΔΑΙΟΙ": "Koumaradaioi",
    "ΚΟΥΜΕΙΚΑ": "Koumeika",
    "ΚΟΥΝΙΑΔΟΙ": "Kouniadoi",
    "ΚΟΥΝΤΟΥΜΑΣ": "Kountoumas",
    "ΛΕΚΚΑ": "Lekka",
    "ΜΑΓΓΑΝΙΤΗΣ": "Manganitis",
    "ΜΑΝΔΡΙΑ": "Mandria",
    "ΜΑΝΩΛΑΤΕΣ": "Manolates",
    "ΜΑΡΑΘΟ": "Maratho",
    "ΜΑΡΑΘΟΚΑΜΠΟΣ": "Marathokampos",
    "ΜΑΥΡΑΤΖΑΙΟΙ": "Mavratzai",
    "ΜΑΥΡΑΤΟ": "Mavrato",
    "ΜΑΥΡΙΚΑΤΟ": "Mavrikato",
    "ΜΕΣΟΓΕΙΟΝ": "Mesogeion",
    "ΜΟΝΟΚΑΜΠΙ": "Monokampi",
    "ΜΥΛΟΙ": "Myloi",
    "ΜΥΤΙΛΗΝΙΟΙ": "Mytilinioi",
    "ΝΕΟΧΩΡΙΟΝ": "Neochorion",
    "ΝΙΚΟΛΟΥΔΕΣ": "Nikoloudes",
    "ΞΥΛΟΣΥΡΤΗΣ": "Xylosyrtis",
    "ΟΡΜ.ΜΑΡΑΘΟΚΑΜΠΟΥ": "Ormos Marathokampou",
    "ΠΑΓΩΝΔΑΣ": "Pagondas",
    "ΠΑΛ.ΚΑΡΛΟΒΑΣΙ": "Palaio Karlovasi",
    "ΠΑΛΑΙΟΚΑΣΤΡΟ": "Palaiokastro",
    "ΠΑΝΔΡΟΣΟ": "Pandrosos",
    "ΠΕΡΔΙΚΙ": "Perdiki",
    "ΠΕΤΡΟΠΟΥΛΙ": "Petropouli",
    "ΠΗΓΗ": "Pigi",
    "ΠΛΑΓΙΑ": "Plagia",
    "ΠΛΑΤΑΝΟΣ": "Platanos",
    "ΠΛΩΜΑΡΙ": "Plomari",
    "ΠΡΟΕΣΠΕΡΑ": "Proespera",
    "ΠΥΘΑΓΟΡΕΙΟ": "Pythagoreio",
    "ΠΥΡΓΟΣ": "Pyrgos",
    "ΡΑΧΕΣ": "Raches",
    "ΣΑΚΟΥΛΕΙΚΑ": "Sakouleika",
    "ΣΑΜΟΣ": "Samos",
    "ΣΚΟΥΡΕΙΚΑ": "Skoureika",
    "ΣΟΥΡΡΗΔΕΣ": "Sourrides",
    "ΣΠΑΘΑΡΑΙΟΙ": "Spatharaioi",
    "ΣΤΑΥΡΙΝΗΔΕΣ": "Stavrinides",
    "ΣΤΥΛΙΟ": "Stylio",
    "ΤΣΟΥΡΛΑΙΟΙ": "Tsourlaioi",
    "ΥΔΡΟΥΣΑ": "Hydrousa",
    "ΦΟΥΡΝΟΙ": "Fournoi",
    "ΦΡΑΝΤΑΤΟ": "Frantato",
    "ΧΡΥΣΟΜΗΛΙΑ": "Chrysomilia",
    "ΧΡΥΣΟΣΤΟΜΟ": "Chrysostomo",
    "ΧΩΡΑ": "Chora",
}


# local | dedication | seat | Greek seat | rank | phones | founded
MONASTIC_ROWS = r'''
Τιμίου Σταυροῦ Μαυρατζαῖοι|Holy Cross|Mavratzai|Μαυρατζαῖοι|Patriarchal and Stavropegic Monastery|22730-37.798|ἔτος ἱδρύσεως 1592.
Μεγάλης Παναγίας Κουμαραδαῖοι|Megali Panagia|Koumaradaioi|Κουμαραδαῖοι|Patriarchal and Stavropegic Monastery|22730-41.249|ἔτος ἱδρύσεως 1586.
Παναγίας Βροντιανῆς (Βουρλιῶτες)|Panagia Vrontiani|Vourliotes|Βουρλιῶτες|Patriarchal and Stavropegic Monastery|22730-93.255|ἔτος ἱδρύσεως 1566.
Προφήτου Ἠλιού Καρλοβασίου|Prophet Elijah|Karlovasi|Καρλοβασίου|Monastery|22730- 89355|ἔτος ἱδρύσεως 1625.
Ἁγίας Ζώνης Βλαμαρῆς|Holy Belt|Vlamari|Βλαμαρῆς|Patriarchal and Stavropegic Monastery|22730-27.587|ἔτος ἱδρύσεως 1695.
Ἁγίας Τριάδος Μυτιληνιῶν|Holy Trinity|Mytilinioi|Μυτιληνιῶν|Monastery|22730-51.339|ἔτος ἱδρύσεως 1824.;;ἔτος ἱδρύσεως 1820,
Ζωοδόχου Πηγῆς Κότσικα|Life-Giving Spring|Kotsika|Κότσικα|Monastery||ἔτος ἱδρύσεως 1730.
Παναγίας Σπηλιανῆς (Πυθαγόρειον)|Panagia Spiliani|Pythagoreio|Πυθαγόρειον|Monastery|22730-61.361|
Ζωοδόχου Πηγῆς Σάμου|Life-Giving Spring|Samos|Σάμου|Patriarchal and Stavropegic Monastery|22730-27.582|ἔτος ἱδρύσεως 1866.
Ἁγίου Ἰωάννου Θεολόγου Παλαιοῦ Καρλοβασίου|Saint John the Theologian|Palaio Karlovasi|Παλαιοῦ Καρλοβασίου|Monastery|22730-32.219|ἔτος ἱδρύσεως 1823.
Ζωοδόχου Πηγῆς Κακοπέρατου|Life-Giving Spring|Kakoperato|Κακοπέρατο|Monastery||
Κοιμήσεως Θεοτόκου Μαραθοκάμπου|Dormition of the Theotokos|Marathokampos|Μαραθοκάμπου|Monastery||ἔτος ἱδρύσεως 1887.
Εὐαγγελισμοῦ Θεοτόκου Λευκάδος|Annunciation of the Theotokos|Lefkada|Λευκάδος|Monastery|22750-22.549|1775
Ζωοδόχου Πηγῆς Γλαρέδων|Life-Giving Spring|Glaredes|Γλαρέδων|Monastery||1890
Εὐαγγελισμοῦ Θεοτόκου Μαβριάνου|Annunciation of the Theotokos|Mavriano|Μαβριάνου|Monastery||18ος αἰ.
Ὁσίας Θεοκτίστης Πηγῆς Φραντάτου|Venerable Theoktiste|Pigi Frantatou|Πηγῆς Φραντάτου|Monastery||1688
Εὐαγγελισμοῦ Θεοτόκου Μοντέ|Annunciation of the Theotokos|Monte|Μοντέ|Monastery|22750-41.254|1460
Μονή Τιμίου Προδρόμου|Saint John the Forerunner|Fournoi|Φούρνων|Monastery||
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "body"


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def make_name(dedication, rank, seat):
    return "%s of %s, %s" % (rank, dedication, seat)


def build_rows():
    rows = []
    regions = Counter()
    index = 0
    roster_groups = (
        (SAMOS_ROWS, SAMOS_ROSTER, 64),
        (IKARIA_ROWS, IKARIA_ROSTER, 48),
    )
    roster_dedications = set()
    roster_seats = set()
    for raw_rows, source, expected in roster_groups:
        lines = raw_rows.strip().splitlines()
        if len(lines) != expected:
            raise ValueError("expected %d roster rows at %s" % (
                expected, source))
        for raw in lines:
            local_dedication, greek_seat, region, postal = raw.split("|", 3)
            if not re.fullmatch(r"\d{5}", postal):
                raise ValueError("invalid postal code in %s" % raw)
            if local_dedication not in DEDICATIONS:
                raise ValueError("unmapped dedication: %s" % local_dedication)
            if greek_seat not in SEAT_NAMES:
                raise ValueError("unmapped seat: %s" % greek_seat)
            dedication = DEDICATIONS[local_dedication]
            seat = SEAT_NAMES[greek_seat]
            rank = "Parish Church"
            name = make_name(dedication, rank, seat)
            index += 1
            rows.append({
                "id": "gr-ep-samos-%03d-%s" % (index, slug(name)),
                "parent": PARENT,
                "kind": "parish",
                "rank": rank,
                "name": name,
                "local": "%s, %s" % (local_dedication, greek_seat),
                "seat": seat,
                "country": "GR",
                "address": [greek_seat, "Τ.Κ. %s" % postal],
                "sources": [source],
            })
            regions[region] += 1
            roster_dedications.add(local_dedication)
            roster_seats.add(greek_seat)
    if roster_dedications != set(DEDICATIONS):
        raise ValueError("dedication map coverage drifted")
    if roster_seats != set(SEAT_NAMES):
        raise ValueError("seat map coverage drifted")
    expected_regions = {
        "ΑΓ.ΚΗΡΥΚΟΥ": 19,
        "ΕΥΔΗΛΟΥ": 12,
        "ΚΑΡΛΟΒΑΣΟΥ": 20,
        "ΜΑΡΑΘΟΚΑΜΠΟΥ": 10,
        "ΠΥΘΑΓΟΡΕΙΟΥ": 18,
        "ΡΑΧΩΝ": 14,
        "ΣΑΜΟΥ": 16,
        "ΦΟΥΡΝΩΝ": 3,
    }
    if dict(sorted(regions.items())) != expected_regions:
        raise ValueError("archiepiscopal region counts drifted")
    monastic_lines = MONASTIC_ROWS.strip().splitlines()
    if len(monastic_lines) != 18:
        raise ValueError("expected 18 exact named monastic institutions")
    for raw in monastic_lines:
        (local, dedication, seat, greek_seat, rank, phones,
         founded) = raw.split("|", 6)
        index += 1
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-samos-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [greek_seat],
            "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
        }
        if phones:
            item["phones"] = phones.split(",")
            item["contact_sources"] = [MONASTERY_PAGE]
            item["contact_checked"] = CHECKED
        if founded:
            item["founded"] = founded.split(";;")
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 130
EXPECTED_OWNER_COUNTS = {PARENT: 130}
EXPECTED_KINDS = {"monastery": 18, "parish": 112}
EXPECTED_RANKS = {
    "Monastery": 13,
    "Parish Church": 112,
    "Patriarchal and Stavropegic Monastery": 5,
}
EXPECTED_CONTACT_BODIES = 11
EXPECTED_PHONE_BODIES = 11
EXPECTED_PHONE_VALUES = 11
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 130
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
        "www.imsamou.gr", "imsamou.gr", "ec-patr.org", "www.ec-patr.org",
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
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Samos candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Samos candidate ledger date drifted")
    expected_summary = {
        PARENT: 130,
        "total": 130,
        "parish_kind_rows": 112,
        "monastery_kind_rows": 18,
        "contact_bodies": 11,
        "phone_bodies": 11,
        "public_phone_values": 11,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 130,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Samos ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Samos ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Samos ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Samos ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Samos ledger has duplicate candidate ids")
    if FORBIDDEN_PUNCTUATION.search(
            json.dumps(ledger, ensure_ascii=False)):
        raise ValueError("Samos ledger has forbidden punctuation")
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
            raise ValueError("%s lacks name, local name, or seat" % row_id)
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
            raise ValueError("%s duplicates %s after normalization" % (
                row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (
            EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Samos English name coverage drifted")
    if set(ENGLISH_SEATS) != {
            item["seat"] for item in result if item.get("seat")}:
        raise ValueError("Samos English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Samos parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Samos kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Samos rank totals drifted: %r" %
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
        raise ValueError("Samos contact coverage drifted: %r" % (coverage,))
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Samos and Ikaria: %d exact named bodies; %d carry current "
            "public contact paths" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Samos and Ikaria: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
