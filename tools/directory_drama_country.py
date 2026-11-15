#!/usr/bin/env python3
"""Validate exact named Drama bodies from current first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_drama_country.py --check
    python tools/directory_drama_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "drama_country.json"
)
PARENT = "ep-drama"
PATRIARCHATE_PAGE = "https://ec-patr.org/entities/iera-mitropoli-dramas/"
ROSTER_PAGE = "http://www.imdramas.gr/Ενορίες-Εφημέριοι/"
FEAST_PDF = (
    "http://www.imdramas.gr/files/"
    "eortazontes-ieroi-naoi-mitropolis-dramas.pdf"
)
HISTORIC_PAGE = "http://www.imdramas.gr/Ἱστορικοί-Ναοί-Μουσείο/"
ARCHANGELS_NEWS = (
    "http://www.imdramas.gr/n/12197/"
    "ΠΑΝΗΓΥΡΙΣ-ΒΥΖΑΝΤΙΝΟΥ-ΠΑΡΕΚΚΛΗΣΙΟΥ-ΠΑΜΜΕΓΙΣΤΩΝ-ΤΑΞΙΑΡΧΩΝ"
)

REGION_SOURCES = {
    "drama": (
        "http://www.imdramas.gr/Ενορίες-Εφημέριοι/Περιφέρεια/10/"
        "Α!-ΑΡΧΙΕΡΑΤΙΚΗ-ΠΕΡΙΦΕΡΕΙΑ-ΔΡΑΜΑΣ"
    ),
    "doxato": (
        "http://www.imdramas.gr/Ενορίες-Εφημέριοι/Περιφέρεια/20/"
        "Β!-ΑΡΧΙΕΡΑΤΙΚΗ-ΠΕΡΙΦΕΡΕΙΑ-ΔΟΞΑΤΟΥ"
    ),
    "nikiforos": (
        "http://www.imdramas.gr/Ενορίες-Εφημέριοι/Περιφέρεια/30/"
        "Γ!-ΑΡΧΙΕΡΑΤΙΚΗ-ΠΕΡΙΦΕΡΕΙΑ-ΝΙΚΗΦΟΡΟΥ-"
    ),
    "paranesti": (
        "http://www.imdramas.gr/Ενορίες-Εφημέριοι/Περιφέρεια/40/"
        "Δ!-ΑΡΧΙΕΡΑΤΙΚΗ-ΠΕΡΙΦΕΡΕΙΑ-ΠΑΡΑΝΕΣΤΙΟΥ-"
    ),
    "prosotsani": (
        "http://www.imdramas.gr/Ενορίες-Εφημέριοι/Περιφέρεια/50/"
        "Ε!-ΑΡΧΙΕΡΑΤΙΚΗ-ΠΕΡΙΦΕΡΕΙΑ-ΠΡΟΣΟΤΣΑΝΗΣ-"
    ),
}


RECORD_GROUPS = [
    {
        "source": REGION_SOURCES["drama"],
        "rows": r'''
Drama|Δράμα|Εἰσόδια τῆς Θεοτόκου (Μητροπολιτικός)|Entry of the Theotokos|25210-32042|Metropolitan Cathedral
Panorama, Drama|Πανόραμα Δράμας|Ἁγ. Ραφαήλ, Νικόλαος καί Εἰρήνη|Saints Raphael, Nicholas, and Irene|25210-28077|Parish Church
Drama|Δράμα|Ἁγ. Ἀνάργυροι.|Holy Unmercenaries|25210-37548|Parish Church
Drama|Δράμα|Ἁγ. Δώδεκα Ἀπόστολοι|Twelve Holy Apostles|25210-38176|Parish Church
Drama|Δράμα|Ἁγ. Εἰρήνη|Saint Irene|25210-39435|Parish Church
Drama|Δράμα|Ἁγ. Κωνσταντῖνος καί Ἑλένη|Saints Constantine and Helen|25210-30182|Parish Church
Drama|Δράμα|Ἁγ. Νικόλαος|Saint Nicholas|25210-32934|Parish Church
Drama|Δράμα|Ἁγ. Παντελεήμων|Saint Panteleimon|25210-33107|Parish Church
Drama|Δράμα|Ἁγ. Σοφία|Saint Sophia|25210-34986|Historic Church
Drama|Δράμα|Ἁγ. Τριάς|Holy Trinity|25210-21197|Parish Church
Drama|Δράμα|Ἁγ. Χρυσόστομος|Hieromartyr Chrysostom of Drama and Smyrna|25210-45005|Parish Church
Drama|Δράμα|Εὐαγγελισμοῦ τῆς Θεοτόκου|Annunciation of the Theotokos|25210-24693|Parish Church
Drama|Δράμα|Προφήτης Ἠλίας|Prophet Elijah|25210-23505|Parish Church
Drama|Δράμα|Ἁγ. Πάντες (Α΄ Κοιμητήρια)|All Saints| |Cemetery Church
Proastio, Drama|Εργατικές κατοικίες Προαστίου Δράμας|Ἁγ. Σάββα|Saint Sabbas| |Parish Church
Mikrochorio|Μικροχώριον|Μικροχώριον - Αγ. Τριάς|Holy Trinity| |Parish Church
Ampelakia|Ἀμπελάκια|Ἀμπελάκια - Ἁγ. Πέτρος καί Παῦλος|Apostles Peter and Paul|25210-96918|Parish Church
Koudounia|Κουδούνια|Κουδούνια - Ἁγ. Γεώργιος - Ἁγ.Δικαίου Λαζάρου|Saint George and Saint Righteous Lazarus|25210-96592|Parish Church
Mavrovatos|Μαυρόβατος|Μαυρόβατος - Αγ. Νικόλαος|Saint Nicholas|25210-83381|Parish Church
Nea Amisos|Νέα Ἀμισός|Νέα Ἀμισός - Ἁγ. Γεώργιος|Saint George| |Parish Church
Nea Sevasteia|Νέα Σεβάστεια|Νέα Σεβάστεια - Ύψωση Τιμίου Σταυρού|Exaltation of the Holy Cross| |Parish Church
Xiropotamos|Ξηροπόταμος|Ξηροπόταμος - Ἁγ. Γεώργιος|Saint George|25210-92387|Parish Church
Drama|Δράμα|Αγ. Βαρβάρα|Saint Barbara| |Church
Dendrakia|Δενδράκια|Δενδράκια - Ἁγ. Νικόλαος|Saint Nicholas| |Parish Church
Argyroupolis|Ἀργυρούπολις|Ἀργυρούπολις - Ἁγ. Ἰωάννης|Saint John the Forerunner| |Parish Church
Kallikarpos|Καλλίκαρπος|Καλλίκαρπος - Κοιμ. Θεοτόκου|Dormition of the Theotokos| |Parish Church
Livadero|Λιβαδερόν|Λιβαδερόν - Αγ. Δημήτριος|Saint Demetrius| |Parish Church
Papades|Παπάδες|Παπάδες - Αγ. Γεώργιος|Saint George| |Parish Church
Sidironero|Σιδηρόνερον|Σιδηρόνερον - Αγ. Γεώργιος|Saint George| |Parish Church
Skaloti|Σκαλωτή|Σκαλωτή - Προφήτης Ηλίας|Prophet Elijah| |Parish Church
Kalos Agros|Καλός Ἀγρός|Καλός Ἀγρός - Κοίμησις Θεοτόκου|Dormition of the Theotokos|25210-96587|Parish Church
Mavrolefki|Μαυρολεύκη|Μαυρολεύκη - Αγ. Παντελεήμων|Saint Panteleimon|25210-93693|Parish Church
Mylopotamos|Μυλοπόταμος|Μυλοπόταμος - Αγ. Δημήτριος|Saint Demetrius| |Parish Church
Nikotsaras|Νικοτσάρας|Νικοτσάρας - Ἁγ. Παρασκευή|Saint Paraskevi| |Parish Church
Sitagroi|Σιταγροί|Σιταγροί - Αγ. Γεώργιος|Saint George|25210-95607|Parish Church
Fotolivos|Φωτολίβος|Φωτολίβος - Αγ. Ανάργυροι|Holy Unmercenaries| |Parish Church
Fotolivos|Φωτολίβος|Φωτολίβος - Αγ. Γεώργιος|Saint George| |Parish Church
Vathylakkos|Βαθύλαξ|Βαθύλαξ - Κοίμησις τῆς Θεοτόκου|Dormition of the Theotokos| |Parish Church
Kallifytos|Καλλίφυτος|Καλλίφυτος - Αγ. Παντελεήμων|Saint Panteleimon| |Parish Church
Makryplagio|Μακρυπλάγιον|Μακρυπλάγιον - Κοίμ. Θεοτόκου|Dormition of the Theotokos|25210-45016|Parish Church
Monastiraki|Μοναστηράκιον|Μοναστηράκιον - Αγ. Γεώργιος|Saint George| |Parish Church
Taxiarches|Ταξιάρχαι|Ταξιάρχαι - Γενέθλιο της Θεοτόκου|Nativity of the Theotokos| |Parish Church
Choristi|Χωριστή|Χωριστή - Εισόδια της Θεοτόκου|Entry of the Theotokos| |Parish Church
''',
    },
    {
        "source": REGION_SOURCES["doxato"],
        "rows": r'''
Doxato|Δοξάτον|Δοξάτον - Άγιος Αθανάσιος|Saint Athanasius| |Parish Church
Agios Athanasios|Άγιος Αθανάσιος|Αγ. Αθανάσιος- Αγ. Παρασκεύη|Saint Paraskevi| |Parish Church
Agora|Αγορά|Αγορά - Κοιμ. Θεοτόκου|Dormition of the Theotokos| |Parish Church
Aigeiros|Αίγειρος|Αίγειρος - Αγ. Γεώργιος|Saint George| |Parish Church
Vathysphilo|Βαθύσπηλον|Βαθύσπηλον - Ευαγγ. Θεοτόκου|Annunciation of the Theotokos| |Parish Church
Evrypedo|Ευρύπεδον|Ευρύπεδον - Γενν. Θεοτόκου|Nativity of the Theotokos| |Parish Church
Ano Kefalari|Άνω Κεφαλάριον|Κεφαλάριον 'Ανω - Αγ. Κωνσταντίνος και Ελένη|Saints Constantine and Helen| |Parish Church
Kato Kefalari|Κάτω Κεφαλάριον|Κεφαλάριον Κάτω - Ευαγγ. Θεοτόκου|Annunciation of the Theotokos| |Parish Church
Kyrgia|Κύργια|Κύργια Άγιος Δημήτριος - Άγιος Γεώργιος|Saints Demetrius and George| |Parish Church
Peristeria|Περιστεριά|Περιστεριά, Κοιμ. Θεοτόκου|Dormition of the Theotokos| |Parish Church
Pigadia|Πηγάδια|Πηγάδια - Τρεις Ιεράρχαι|Three Holy Hierarchs| |Parish Church
Ypsilo|Υψηλόν|Υψηλόν - Αναλ. Σωτήρος|Ascension of the Savior| |Parish Church
Vathychorio|Βαθυχώριον|Βαθυχώριον - Αγ.Νικόλαος|Saint Nicholas| |Parish Church
Agia Paraskevi|Αγία Παρασκευή|Αγία Παρασκευή - Αγ. Παρασκευή|Saint Paraskevi| |Parish Church
Kalampaki|Καλαμπάκιον|Καλαμπάκιον - Αγ. Γεώργιος|Saint George| |Parish Church
Kalamonas|Καλαμώνας|Καλαμώνας - Ευαγγ. Θεοτόκου|Annunciation of the Theotokos| |Parish Church
Nerofraktis|Νεροφράκτης|Νεροφράκτης - Αγ. Δημήτριος|Saint Demetrius| |Parish Church
Ftelia|Φτελιά|Φτελιά - Αγ. Ταξιάρχαι|Holy Archangels| |Parish Church
''',
    },
    {
        "source": REGION_SOURCES["nikiforos"],
        "rows": r'''
Adriani|Αδριανή|Αδριανή - Αγ. Νικόλαος|Saint Nicholas| |Parish Church
Marmaria|Μαρμαριά|Μαρμαριά - Υψ. Τιμίου Σταυρού|Exaltation of the Holy Cross| |Parish Church
Mavrokordato|Μαυροκορδάτον|Μαυροκορδάτον - Αγ. Γεώργιος|Saint George| |Parish Church
Mikrolivado|Μικρολίβαδον|Μικρολίβαδον - Αγ. Πέτρος - Παύλος|Apostles Peter and Paul| |Parish Church
Nikiforos|Νικηφόρος|Νικηφόρος - Αγ. Γεώργιος|Saint George| |Parish Church
Paliampela|Παλιάμπελα|Παλιάμπελα - Αγ. Κωνσταντίνος και Ελένη|Saints Constantine and Helen| |Parish Church
Platania|Πλατανιά|Πλατανιά - Ζωοδόχος Πηγή|Life-Giving Spring| |Parish Church
Platanovrysi|Πλατανόβρυση|Πλατανόβρυση - Αγ. Γεώργιος|Saint George| |Parish Church
Prinolofos|Πρινόλοφος|Πρινόλοφος - Αγ. Θεόδωροι|Holy Theodore Martyrs| |Parish Church
Ptelea|Πτελέα|Πτελέα - Αγ. Δημήτριος|Saint Demetrius| |Parish Church
Pyxari|Πυξάριον|Πυξάριον - Αγ. Γεώργιος|Saint George| |Parish Church
Teichos|Τείχος|Τείχος - Αγ. Γεώργιος|Saint George| |Parish Church
Terpsithea|Τερψιθέα|Τερψιθέα - Αγ. Παντελεήμων|Saint Panteleimon| |Parish Church
Ypsili Rachi|Υψηλή Ράχη|Υψηλή Ράχη - Κοιμ. Θεοτόκου|Dormition of the Theotokos| |Parish Church
Chamokerasa|Χαμοκέρασα|Χαμοκέρασα - Αγ. Γεώργιος|Saint George| |Parish Church
''',
    },
    {
        "source": REGION_SOURCES["paranesti"],
        "rows": r'''
Aidonokastro|Αηδονόκαστρον|Αηδονόκαστρον - Αγ. Γεώργιος|Saint George| |Parish Church
Dipotama|Διπόταμα|Διπόταμα - Αγ. Νικόλαος|Saint Nicholas| |Parish Church
Ano Tholos|Άνω Θόλος|Θόλος 'Ανω - Αγ. Γεώργιος|Saint George| |Parish Church
Kato Tholos|Κάτω Θόλος|Θόλος Κάτω - Γενέθλιο της Θεοτόκου|Nativity of the Theotokos| |Parish Church
Kapnofyto|Καπνόφυτον|Καπνόφυτον - Αγ. Δημήτριος|Saint Demetrius| |Parish Church
Karpoforo|Καρποφόρον|Καρποφόρον - Αγ. Μηνάς|Saint Menas| |Parish Church
Krini|Κρήνη|Κρήνη - Αγ. Πέτρος και Παύλος|Apostles Peter and Paul| |Parish Church
Mesochori|Μεσοχωρίον|Μεσοχωρίον - Κοιμ. της Θεοτόκου|Dormition of the Theotokos| |Parish Church
Mikrochorio, Paranesti|Μικροχώριον Παρανεστίου|Μικροχώριον - Αγ. Πέτρος και Παύλος|Apostles Peter and Paul| |Parish Church
Xagnanto|Ξάγναντον|Ξάγναντον - Αγ. Τριάς|Holy Trinity| |Parish Church
Perivlepto|Περίβλεπτον|Περίβλεπτον - Αγ. Δημήτριος|Saint Demetrius| |Parish Church
Polyneri|Πολυνέριον|Πολυνέριον - Μεταμόρφ. Σωτήρος|Transfiguration of the Savior| |Parish Church
Polysyko|Πολύσυκον|Πολύσυκον - Αγ. Παντελεήμων|Saint Panteleimon| |Parish Church
Prasinada|Πρασινάδα|Πρασινάδα - Αγ. Γεώργιος|Saint George| |Parish Church
Sterna|Στέρνα|Στέρνα - Αγ. Παντελεήμων|Saint Panteleimon| |Parish Church
Temenos|Τέμενος|Τέμενος - Προφήτης Ηλίας|Prophet Elijah| |Parish Church
Paranesti|Παρανέστιον|Παρανέστιον- Άγ.Κων/νος και Ελένη|Saints Constantine and Helen| |Parish Church
''',
    },
    {
        "source": REGION_SOURCES["prosotsani"],
        "rows": r'''
Angitis|Ἀγγίτης|Ἀγγίτης - Ἁγ. Πέτρος καί Παῦλος|Apostles Peter and Paul| |Parish Church
Volakas|Βώλαξ|Βώλαξ - Προφήτης Ἠλίας|Prophet Elijah| |Parish Church
Granitis|Γρανίτης|Γρανίτης - Ἁγ. Ταξιάρχαι|Holy Archangels| |Parish Church
Kokkinoia|Κοκκινόγεια|Κοκκινόγεια - Ἁγ. Γεώργιος|Saint George| |Parish Church
Petrousa|Πετροῦσα|Πετροῦσα - Ἁγ. Ἀθανάσιος|Saint Athanasius| |Parish Church
Piges|Πηγαί|Πηγαί - Προφήτης Ἠλίας|Prophet Elijah| |Parish Church
Prosotsani|Προσοτσάνη|Προσοτσάνη - Ἁγ. Τριάς|Holy Trinity| |Parish Church
Prosotsani|Προσοτσάνη|Προσοτσάνη-Εἰσόδια Θεοτόκου|Entry of the Theotokos| |Parish Church
Pyrgoi|Πύργοι|Πύργοι - Μεταμόρφωση Σωτῆρος|Transfiguration of the Savior| |Parish Church
Stavros|Σταυρός|Σταυρός - Ἁγ. Φανούριος|Saint Phanourios| |Parish Church
Megalokampos|Μεγαλόκαμπος|Μεγαλόκαμπος - Ἁγ. Κωνσταντῖνος καί Ἑλένη|Saints Constantine and Helen| |Parish Church
Mikrokampos|Μικρόκαμπος|Μικρόκαμπος - Προφήτης Ἠλίας|Prophet Elijah| |Parish Church
''',
    },
]

ARKADIKOS_SPLIT = [
    {
        "seat": "Arkadikos",
        "address": ["Ἀρκαδικός"],
        "local": "Ἱερός Ναός Ἁγίου Παντελεήμονος Ἀρκαδικοῦ Δράμας",
        "dedication": "Saint Panteleimon",
        "rank": "Church",
        "phones": ["25210-32057"],
    },
    {
        "seat": "Arkadikos",
        "address": ["Ἀρκαδικός"],
        "local": "Ἱερός Ναός Ἁγίου Εὐγενίου τοῦ Τραπεζουντίου Ἀρκαδικοῦ Δράμας",
        "dedication": "Saint Eugene of Trebizond",
        "rank": "Parish Church",
        "phones": ["25210-32057"],
    },
]
ARKADIKOS_DETAIL = (
    "http://www.imdramas.gr/Ενορίες-Εφημέριοι/Ναός/43/"
    "Ἀρκαδικός-Ἁγ-Παντελεήμων,-ἉγΕὐγενίου-τοῦ-Τραπεζουντίου"
)

FEAST_ROWS = r'''
Kalampaki|Καλαμπάκιον|Ι.Ν. Αγίου Αθανασίου Καλαμπακίου|Saint Athanasius|Church
Vounoplagia|Βουνοπλαγιά|Ι.Ν. Αγίου Πολυκάρπου Βουνοπλαγιάς|Saint Polycarp|Church
Kallifytos|Καλλίφυτος|Ι.Ν. Ζωοδόχου Πηγής Καλλιφύτου|Life-Giving Spring|Church
Ftelia|Φτελιά|Ι.Ν. Αγίου Γεωργίου Φτελιάς|Saint George|Church
Adriani|Αδριανή|Ι.Ν. Αγίου Ιωάννου Θεολόγου Αδριανής|Saint John the Theologian|Church
Xiropotamos|Ξηροπόταμος|Ι.Ν. Αγίων Πέτρου και Παύλου Ξηροποτάμου|Apostles Peter and Paul|Church
Paranesti|Παρανέστιον|Ι.Ν. Αγίων Πέτρου και Παύλου Παρανεστίου|Apostles Peter and Paul|Church
Doxato|Δοξάτον|Ι.Ν. Αγίας Κυριακής Δοξάτου|Saint Kyriaki|Church
Choristi|Χωριστή|Ι.Ν. Αγίας Κυριακής Χωριστής|Saint Kyriaki|Church
Choristi|Χωριστή|Ι.Ν. Οσίου Παϊσίου Χωριστής|Saint Paisios|Church
Kalos Agros|Καλός Ἀγρός|Ι.Ν. Ευαγγελισμού Θεοτόκου Καλού Αγρού|Annunciation of the Theotokos|Church
Kyrgia|Κύργια|Ι.Ν. Αγίας Μακρίνης Κυργίων|Saint Macrina|Church
Prosotsani|Προσοτσάνη|Ι.Ν. Προφήτη Ηλιού Προσοτσάνης|Prophet Elijah|Church
Fotolivos|Φωτολίβος|Ι.Ν. Προφήτη Ηλιού Φωτολίβους|Prophet Elijah|Church
Ano Kefalari|Άνω Κεφαλάριον|Ι.Ν. Αγίου Παντελεήμονος Άνω Κεφαλαρίου|Saint Panteleimon|Church
Psilokastro|Ψηλόκαστρον|Ι.Ν. Μεταμορφώσεως Ψηλοκάστρου|Transfiguration of the Savior|Church
Platania|Πλατανιά|Ι.Ν. Τιμίου Προδρόμου Πλατανιάς|Saint John the Forerunner|Church
Koudounia|Κουδούνια|Ι.Ν. Αγίου Δαυίδ Μεγάλου Κομνηνού Κουδουνίων|Saint David Grand Komnenos|Church
Mikrokampos|Μικρόκαμπος|Ι.Ν. Αγίας Ελένης της εκ Σινώπης Μικροκάμπου|Saint Helen of Sinope|Church
Prosotsani|Προσοτσάνη|Ι.Ν. Ταξιαρχών Προσοτσάνης|Holy Archangels|Church
Psilokastro|Ψηλόκαστρον|Ι.Ν. Αγίου Νεκταρίου Ψηλοκάστρου|Saint Nectarius|Church
Choristi|Χωριστή|Ι.Ν. Οσίου Αρσενίου Χωριστής|Saint Arsenios|Church
Petrousa|Πετροῦσα|Ι.Ν. Εισοδίων της Θεοτόκου Πετρούσης|Entry of the Theotokos|Church
Doxato|Δοξάτον|Ι.Ν. Αγίας Αικατερίνης Δοξάτου|Saint Catherine|Church
Gyros|Γύρος|Ι.Ν. Αγίας Αικατερίνης Γύρου|Saint Catherine|Church
'''

MONASTIC_ROWS = [
    {
        "seat": "Nea Kromni, Drama",
        "address": ["Τέρμα Ευξείνου Πόντου", "661 00 Νέα Κρώμνη Δράμας"],
        "local": "Ιερά Λαυρεντιανή Μονή Μεταμορφώσεως του Σωτήρος - Νέα Σουμελά",
        "dedication": "Laurentian Transfiguration of the Savior - New Soumela",
        "rank": "Monastery",
        "sources": [
            "http://www.imdramas.gr/n/1451/Λαυρεντιανή-Νέα-Σουμελᾶ",
            PATRIARCHATE_PAGE,
        ],
    },
    {
        "seat": "Mount Pangaion",
        "address": ["620 56 Σ.Σ. Αγγίστης Σερρών"],
        "local": "Ιερά Πατριαρχική και Σταυροπηγιακή Μονή Παναγίας Εικοσιφοινίσσης",
        "dedication": "Panagia Eikosifoinissa Patriarchal and Stauropegial",
        "rank": "Monastery",
        "phones": ["2510-516581"],
        "sources": [
            "http://www.imdramas.gr/n/1453/Παναγίας-Εικοσιφοινίσσης",
            PATRIARCHATE_PAGE,
        ],
        "contact_sources": [PATRIARCHATE_PAGE],
    },
    {
        "seat": "Taxiarches, Drama",
        "address": ["661 00 Ταξιάρχαι Δράμας"],
        "local": "Ιερά Μονή Αναλήψεως του Σωτήρος - Σίψα",
        "dedication": "Ascension of the Savior - Sipsa",
        "rank": "Monastery",
        "phones": ["25210-45023"],
        "sources": [
            "http://www.imdramas.gr/n/1452/Αναλήψεως-Σίψα",
            PATRIARCHATE_PAGE,
        ],
        "contact_sources": [
            "http://www.imdramas.gr/n/1452/Αναλήψεως-Σίψα"
        ],
    },
    {
        "seat": "Prasinada, Drama",
        "address": ["Πρασινάδα Δράμας", "Τ.Κ. 66035"],
        "local": "Ιερά Μονή Μεταμορφώσεως του Σωτήρος Πρασινάδας Παρανεστίου",
        "dedication": "Transfiguration of the Savior at Prasinada",
        "rank": "Monastery under Re-establishment",
        "phones": ["25247-70014"],
        "emails": ["immespr@gmail.com"],
        "site": "https://immsdramas.gr/",
        "sources": [
            "http://www.imdramas.gr/n/10336/Μεταμορφώσεως-του-Σωτήρος-Πρασινάδος",
            "https://immsdramas.gr/",
            "https://immsdramas.gr/?page_id=591",
        ],
        "contact_sources": ["https://immsdramas.gr/?page_id=591"],
    },
    {
        "seat": "Serres",
        "address": ["Σέρρες"],
        "local": "Παναγία ἡ Ἡλιόκαλλη ἐν Σέρραις",
        "dedication": "Panagia Iliokalli",
        "rank": "Metochion",
        "sources": [PATRIARCHATE_PAGE],
    },
    {
        "seat": "Thasos",
        "address": ["Θάσος"],
        "local": "Μεταμορφώσεως τοῦ Σωτῆρος Θάσου",
        "dedication": "Transfiguration of the Savior",
        "rank": "Metochion",
        "sources": [PATRIARCHATE_PAGE],
    },
]


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:72]


def parse_lines(block, columns):
    result = []
    for line in block.strip().splitlines():
        values = [value.strip() for value in line.split("|")]
        if len(values) != len(columns):
            raise ValueError("invalid Drama source row: %s" % line)
        result.append(dict(zip(columns, values)))
    return result


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def build_rows():
    rows = []
    index = 0
    columns = ("seat", "address_el", "local", "dedication", "phone", "rank")
    for group in RECORD_GROUPS:
        for record in parse_lines(group["rows"], columns):
            index += 1
            item = {
                "id": "gr-ep-drama-%03d-%s" % (
                    index,
                    slug(make_name(record["dedication"],
                                   record["rank"], record["seat"])),
                ),
                "parent": PARENT,
                "kind": "parish",
                "rank": record["rank"],
                "name": make_name(record["dedication"], record["rank"],
                                  record["seat"]),
                "local": record["local"],
                "seat": record["seat"],
                "country": "GR",
                "address": [record["address_el"]],
                "sources": [group["source"]],
            }
            if record["phone"]:
                item["phones"] = [record["phone"]]
                item["contact_sources"] = [group["source"]]
                item["contact_checked"] = CHECKED
            rows.append(item)
    for record in ARKADIKOS_SPLIT:
        index += 1
        item = {
            "id": "gr-ep-drama-%03d-%s" % (
                index,
                slug(make_name(record["dedication"],
                               record["rank"], record["seat"])),
            ),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": make_name(record["dedication"], record["rank"],
                              record["seat"]),
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "phones": list(record["phones"]),
            "sources": [REGION_SOURCES["drama"], ARKADIKOS_DETAIL, FEAST_PDF],
            "contact_sources": [REGION_SOURCES["drama"]],
            "contact_checked": CHECKED,
        }
        rows.append(item)
    feast_columns = ("seat", "address_el", "local", "dedication", "rank")
    for record in parse_lines(FEAST_ROWS, feast_columns):
        index += 1
        name = make_name(record["dedication"], record["rank"], record["seat"])
        rows.append({
            "id": "gr-ep-drama-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": [record["address_el"]],
            "sources": [FEAST_PDF],
        })
    index += 1
    chapel_name = "Holy Archangels Byzantine Chapel in Drama"
    rows.append({
        "id": "gr-ep-drama-%03d-%s" % (index, slug(chapel_name)),
        "parent": PARENT,
        "kind": "parish",
        "rank": "Chapel",
        "name": chapel_name,
        "local": "Βυζαντινό Παρεκκλήσιο Παμμεγίστων Ταξιαρχών Δράμας",
        "seat": "Drama",
        "country": "GR",
        "address": ["Δράμα"],
        "sources": [HISTORIC_PAGE, ARCHANGELS_NEWS],
    })
    for record in MONASTIC_ROWS:
        index += 1
        name = make_name(record["dedication"], record["rank"], record["seat"])
        item = {
            "id": "gr-ep-drama-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": record["rank"],
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": list(record["address"]),
            "sources": list(record["sources"]),
        }
        for key in ("phones", "emails", "site", "contact_sources"):
            if record.get(key):
                item[key] = (list(record[key]) if isinstance(record[key], list)
                             else record[key])
        if item.get("contact_sources"):
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 139
EXPECTED_OWNER_COUNTS = {PARENT: 139}
EXPECTED_KINDS = {"monastery": 6, "parish": 133}
EXPECTED_RANKS = {
    "Cemetery Church": 1,
    "Chapel": 1,
    "Church": 27,
    "Historic Church": 1,
    "Metochion": 2,
    "Metropolitan Cathedral": 1,
    "Monastery": 3,
    "Monastery under Re-establishment": 1,
    "Parish Church": 102,
}
EXPECTED_CONTACT_BODIES = 26
EXPECTED_PHONE_BODIES = 26
EXPECTED_PHONE_VALUES = 26
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 139
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
    if not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    allowed = {
        "ec-patr.org": {"https"},
        "immsdramas.gr": {"https"},
        "www.imdramas.gr": {"http"},
    }
    if parsed.netloc not in allowed or parsed.scheme not in allowed[parsed.netloc]:
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
        if item["site"] not in sources:
            raise ValueError("%s body-owned site lacks provenance"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Drama candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Drama candidate ledger date drifted")
    expected_summary = {
        PARENT: 139,
        "total": 139,
        "parish_kind_rows": 133,
        "monastery_kind_rows": 6,
        "contact_bodies": 26,
        "phone_bodies": 26,
        "public_phone_values": 26,
        "email_bodies": 1,
        "public_email_values": 1,
        "body_owned_sites": 1,
        "address_bodies": 139,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Drama ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Drama ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Drama ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Drama ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Drama ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Drama candidate ledger has forbidden punctuation")
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
        signature = (parent, unicase(item["local"]))
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
        raise ValueError("Drama English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Drama English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Drama parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Drama kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Drama rank totals drifted: %r" %
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
        raise ValueError("Drama contact coverage drifted: %r" % (coverage,))
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
            "Drama: %d exact named bodies; %d carry current institutional "
            "contact data" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Drama: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
