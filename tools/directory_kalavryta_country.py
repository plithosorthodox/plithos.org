#!/usr/bin/env python3
"""Validate exact current Kalavryta and Aigialeia worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_kalavryta_country.py --check
    python tools/directory_kalavryta_country.py --check-live
    python tools/directory_kalavryta_country.py --dump
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
PARENT = "gr-kalavryta"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "kalavryta_country.json"
)

REGION_PAGE = "https://www.imkalaig.gr/arxieratikes-perifereies"
CHURCH_INDEX = "https://www.imkalaig.gr/ieroi-naoi"
CHURCH_PAGE_2 = (
    "https://www.imkalaig.gr/?section=2161&page1463=1&language=el_GR"
)
MONASTERY_INDEX = "https://www.imkalaig.gr/ieres-mones"
PILGRIMAGE_INDEX = "https://www.imkalaig.gr/proskinimata"
CALENDAR_PDF = (
    "https://www.imkalaig.gr/managed_images/imerologio-eortologio-2026.pdf"
)
REGULATION_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "kalabryton-kai-aigialeias"
)


def detail_url(section, item_id):
    return (
        "https://www.imkalaig.gr/?section=%s&language=el_GR&"
        "itemid1494=%s&detail1494=1" % (section, item_id)
    )


def church_url(item_id):
    return detail_url(2161, item_id)


def monastery_url(item_id):
    return detail_url(2162, item_id)


def pilgrimage_url(item_id):
    return detail_url(2528, item_id)


# Current archieratical region | settlement | current first-party dedication.
# These are the 164 exact rows on the live regional roster.
PARISH_SOURCE = r'''
Aigeira|Αιγείρα|Ι.Ν. Αγ. Παντελεήμονος
Aigeira|Αιγές|Ι.Ν. Αγ. Δημητρίου
Aigeira|Αμπελόκηποι|Ι.Ν. Αγ. Αναργύρων
Aigeira|Βελλά|Ι.Ν. Κοιμήσεως Θεοτόκου
Aigeira|Εξοχή|Ι.Ν. Αγ. Νικολάου
Aigeira|Μάρμαρα|Ι.Ν. Αγ. Σπυρίδωνος
Aigeira|Μοναστήριο|Ι.Ν. Κοιμήσεως Θεοτόκου
Aigeira|Όαση|Ι.Ν. Αγ. Ανδρέου
Aigeira|Περιθώριο|Ι.Ν. Αγ. Βλασίου
Aigeira|Σελιάνα|Ι.Ν. Κοιμήσεως Θεοτόκου
Aigeira|Συνεβρό|Ι.Ν. Κοιμήσεως Θεοτόκου
Aigeira|Χρυσάνθιο|Ι.Ν. Αγ. Αποστόλων
Akrata|Ακράτα|Ι.Ν. Αγ. Χαραλάμπους
Akrata|Παραλία Πλατάνου|Ι.Ν. Ζωοδόχου Πηγής
Akrata|Αγία Βαρβάρα|Ι.Ν. Αγ. Γεωργίου
Akrata|Άμπελος|Ι.Ν. Αγ. Ανδρέου
Akrata|Βαλιμή|Ι.Ν. Κοιμήσεως Θεοτόκου
Akrata|Βούτσιμο|Ι.Ν. Αγ. Χαραλάμπους
Akrata|Ζαρούχλα|Ι.Ν. Αγ. Τριάδος
Akrata|Καλαμιάς|Ι.Ν. Υπαπαντής Χριστού
Akrata|Κράθιο|Ι.Ν. Μεταμορφώσεως Σωτήρος
Akrata|Μεσορούγιο|Ι.Ν. Αγ. Θεοδώρων
Akrata|Περιστέρα|Ι.Ν. Τιμίου Προδρόμου
Akrata|Πορρωβίτσα|Ι.Ν. Τριών Ιεραρχών
Akrata|Πύργος|Ι.Ν. Αγ. Γεωργίου
Akrata|Πλάτανος|Ι.Ν. Αγ. Ανδρέου
Akrata|Σιλιβενιώτικα|Ι.Ν. Αγ. Νικολάου
Aroania|Αγρίδιο|Ι.Ν. Τιμίας Ζώνης
Aroania|Αλέσταινα|Ι.Ν. Αγ. Γεωργίου
Aroania|Αμυγδαλιά|Ι.Ν. Αγ. Νικολάου
Aroania|Ανάστασις|Ι.Ν. Αγ. Δημητρίου
Aroania|Αροανία|Ι.Ν. Ευαγγελισμού
Aroania|Αροανία|Ι.Ν. Αγ. Γεωργίου
Aroania|Βεσίνιο|Ι.Ν. Κοιμήσεως Θεοτόκου
Aroania|Δάφνη|Ι.Ν. Αγ. Τριάδος
Aroania|Δάφνη|Ι.Ν. Αγ. Χαραλάμπους
Aroania|Δεσινό|Ι.Ν. Αγ. Γεωργίου
Aroania|Δεχούνιο|Ι.Ν. Αγ. Γεωργίου
Aroania|Καμενιάνοι|Ι.Ν. Αγ. Αθανασίου
Aroania|Κερασιά|Ι.Ν. Αγ. Δημητρίου
Aroania|Λειβάρτζιο|Ι.Ν. Αγ. Γεωργίου
Aroania|Λεχούριο|Ι.Ν. Εισοδίων Θεοτόκου
Aroania|Νάσια|Ι.Ν. Αγ. Δημητρίου
Aroania|Πάος|Ι.Ν. Αγ. Θεοδώρων
Aroania|Πεύκο|Ι.Ν. Κοιμήσεως Θεοτόκου
Aroania|Πλάκα|Ι.Ν. Τιμίου Προδρόμου
Aroania|Σειρές|Ι.Ν. Αναλήψεως Χριστού
Aroania|Σειρές|Ι.Ν. Αγ. Βασιλείου
Aroania|Σκοτάνη|Ι.Ν. Αγ. Δημητρίου
Aroania|Χόβολη|Ι.Ν. Αγ. Τριάδος
Aroania|Ψωφίδα|Ι.Ν. Κοιμήσεως Θεοτόκου
Vostitsa|Αίγιο|Καθεδρικός Ι.Ν. Κοιμήσεως Θεοτόκου (Παναγία Φανερωμένη)
Vostitsa|Αίγιο|Ι.Ν. Παμμεγίστων Ταξιαρχών
Vostitsa|Αίγιο|Ι.Ν. Εισοδίων Θεοτόκου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Ανδρέου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Κων/νου-Ελένης & Θεοπρ. Άννης
Vostitsa|Αίγιο|Ι.Ν. Αγ. Ιωάννου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Αλεξίου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Λεοντίου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Αθανασίου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Αποστόλων Πέτρου & Παύλου
Vostitsa|Αίγιο|Ι.Ν. Αγ. Μαρίνης
Vostitsa|Άγιος Ανδρέας Πτέρης|Ι.Ν. Αγ. Ανδρέου
Vostitsa|Αραχωβίτικα (Βουλωμένο)|Ι.Ν. Μεταμορφώσεως του Σωτήρος
Vostitsa|Αχλαδιάς|Ι.Ν. Αγ. Ανδρέου
Vostitsa|Βαλιμίτικα|Ι.Ν. Αγ. Βασιλείου
Vostitsa|Δάφνες|Ι.Ν. Αγ. Γεωργίου
Vostitsa|Διγιελιώτικα|Ι.Ν. Αγ. Ανδρέου
Vostitsa|Κουλούρα|Ι.Ν. Υπαπαντής του Χριστού
Vostitsa|Κούμαρης|Ι.Ν. Αγ. Ιωάννου
Vostitsa|Κουνινά|Ι.Ν. Αγ. Αθανασίου
Vostitsa|Μαυρίκι|Ι.Ν. Αγ. Νικολάου
Vostitsa|Μελίσσια|Ι.Ν. Αγ. Γεωργίου
Vostitsa|Παρασκευή|Ι.Ν. Αγ. Παρασκευής
Vostitsa|Σέλισσα|Ι.Ν. Αγ. Βασιλείου
Vostitsa|Σελινούντας|Ι.Ν. Κοιμήσεως Θεοτόκου
Vostitsa|Τέμενη|Ι.Ν. Αγ. Γεωργίου
Vostitsa|Χατζή|Ι.Ν. Αγ. Ανδρέου
Diakopto|Διακοπτό|Ι.Ν. Αγ. Τρύφωνος
Diakopto|Άνω Διακοπτό|Ι.Ν. Αγ. Νικολάου
Diakopto|Ελαιώνας|Ι.Ν. Αγ. Βασιλείου
Diakopto|Ελίκη|Ι.Ν. Αγ. Αθανασίου
Diakopto|Ζαχλωρίτικα|Ι.Ν. Αγ. Χαραλάμπους
Diakopto|Καθολικό|Ι.Ν. Κοιμήσεως Θεοτόκου
Diakopto|Κερνίτσα|Ι.Ν. Αγ. Αναργύρων
Diakopto|Κερύνεια|Ι.Ν. Αγ. Νικολάου
Diakopto|Ν. Κερύνεια|Ι.Ν. Παμμ. Ταξιαρχών & Αγ. Αναστασίας
Diakopto|Λόφος-Καλυβίτης|Ι.Ν. Αγ. Γεωργίου
Diakopto|Μαμουσιά|Ι.Ν. Κοιμήσεως Θεοτόκου
Diakopto|Νικολέϊκα|Ι.Ν. Αγ. Βαρβάρας
Diakopto|Ριζόμυλος|Ι.Ν. Κοιμήσεως Θεοτόκου
Diakopto|Ροδιά|Ι.Ν. Αγ. Νικολάου
Diakopto|Τράπεζα|Ι.Ν. Εισοδίων Θεοτόκου
Kalavryta|Καλάβρυτα|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Βάλτσα|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Βιλιβίνα|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Άνω Βλασία|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Κάτω Βλασία|Ι.Ν. Αγ. Βλασίου
Kalavryta|Γουμένισσα|Ι.Ν. Αγ. Γεωργίου
Kalavryta|Δουμενά|Ι.Ν. Αγ. Σπυρίδωνος
Kalavryta|Δροσάτο|Ι.Ν. Αγ. Νικολάου
Kalavryta|Κάτω Ζαχλωρού|Ι.Ν. Εισοδίων Θεοτόκου
Kalavryta|Καλλιφώνιο|Ι.Ν. Αγ. Ιωάννου Χρυσοστόμου
Kalavryta|Κάνδαλος|Ι.Ν. Αγ. Ιωάννου Χρυσοστόμου
Kalavryta|Καρούσιο|Ι.Ν. Αγ. Δημητρίου
Kalavryta|Κερπινή|Ι.Ν. Τιμίου Προδρόμου
Kalavryta|Κέρτεζη|Ι.Ν. Γεννέσεως Θεοτόκου
Kalavryta|Κορφές|Ι.Ν. Γεννέσεως Θεοτόκου
Kalavryta|Κούτελη|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Κραστικοί|Ι.Ν. Αγ. Δημητρίου
Kalavryta|Κρυονέρι|Ι.Ν. Αγ. Παρασκευής
Kalavryta|Λαγοβούνιο|Ι.Ν. Αγ. Γεωργίου
Kalavryta|Λαπαναγοί|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Λαπάτα|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Λεύκα|Ι.Ν. Αγ. Νικολάου
Kalavryta|Λουσικό|Ι.Ν. Αγ. Τριάδος
Kalavryta|Άνω Λουσοί|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Κάτω Λουσοί|Ι.Ν. Αγ. Βασιλείου
Kalavryta|Μάνεσι|Ι.Ν. Αγ. Νικολάου
Kalavryta|Μέγας Ποντιάς|Ι.Ν. Αγ. Νικολάου
Kalavryta|Μικρός Ποντιάς|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Μπούμπουκας|Ι.Ν. Τιμίου Προδρόμου
Kalavryta|Πετσάκοι|Ι.Ν. Αγ. Νικολάου
Kalavryta|Πλατανιώτισσα|Ι.Ν. Μεταμορφώσεως Σωτήρος
Kalavryta|Πριόλιθος|Ι.Ν. Αγ. Ανδρέου
Kalavryta|Προφήτης Ηλίας|Ι.Ν. Κοιμήσεως Θεοτόκου
Kalavryta|Ρωγοί|Ι.Ν. Αγ. Βαρβάρας
Kalavryta|Σιγούνιο|Ι.Ν. Τιμίου Προδρόμου
Kalavryta|Σκεπαστό|Ι.Ν. Αγ. Ανδρέου
Kalavryta|Τρεχλό|Ι.Ν. Αγ. Γεωργίου
Kalavryta|Τρίκορφο|Ι.Ν. Αγ. Βαρβάρας
Kalavryta|Χαλανδρίτσα|Ι.Ν. Αγ. Βασιλείου
Kleitoria|Άγιος Νικόλαος|Ι. Ν. Αγ. Νικολάου
Kleitoria|Άρμπουνας|Ι. Ν. Αγ. Αθανασίου
Kleitoria|Γλάστρα|Ι. Ν. Αγ. Γεωργίου
Kleitoria|Δρυμός|Ι. Ν. Αγ. 40 Μαρτύρων
Kleitoria|Καλλιθέα|Ι. Ν. Παμμ. Ταξιαρχών
Kleitoria|Καλύβια Δρυμού|Ι. Ν. Μεταμορφώσεως Σωτήρος
Kleitoria|Καλύβια Φιλίων|Ι. Ν. Ζωοδόχου Πηγής
Kleitoria|Καστέλι|Ι. Ν. Αγ. Γεωργίου
Kleitoria|Καστριά|Ι. Ν. Κοιμήσεως Θεοτόκου
Kleitoria|Άνω Κλειτορία|Ι. Ν. Γεννέσεως Θεοτόκου
Kleitoria|Κλειτορία|Ι. Ν. Αγ. Δημητρίου
Kleitoria|Κλείτωρ|Ι. Ν. Αγ. Νικολάου
Kleitoria|Κρυνόφυτα|Ι. Ν. Αγ. Θεοδώρων
Kleitoria|Λευκάσιο|Ι. Ν. Αγ. Δημητρίου
Kleitoria|Λυκούρια|Ι. Ν. Αγ. Γεωργίου
Kleitoria|Παγκράτι|Ι. Ν. Αγ. Ιωάννου Θεολόγου
Kleitoria|Πλανήτερον|Ι. Ν. Αγ. Νικολάου
Kleitoria|Τουρλάδα|Ι. Ν. Αγ. Ανδρέου
Kleitoria|Φίλια|Ι. Ν. Κοιμήσεως Θεοτόκου
Sympoliteia|Άβυθος|Ι.Ν. Παμμ. Ταξιαρχών
Sympoliteia|Άγιος Κωνσταντίνος|Ι.Ν. Αγ. Κωνσταντίνου
Sympoliteia|Γκραίκα|Ι.Ν. Αγ. Μαρίνης
Sympoliteia|Γρηγόρι|Ι.Ν. Αγίου Γρηγορίου
Sympoliteia|Δημητρόπουλο|Ι.Ν. Τιμίου Προδρόμου
Sympoliteia|Κρήνη|Ι.Ν. Κοιμήσεως Θεοτόκου
Sympoliteia|Λόγγος|Ι.Ν. Αγ. Δημητρίου
Sympoliteia|Νεραντζιές|Ι.Ν. Αγ. Δημητρίου
Sympoliteia|Πανόραμα|Ι.Ν. Αγ. Παντελεήμονος
Sympoliteia|Ροδοδάφνη|Ι.Ν. Αγ. Σπυρίδωνος
Sympoliteia|Άγιος Γεώργιος Ροδοδάφνης|Ι.Ν. Αγ. Γεωργίου
Sympoliteia|Σελιανίτικα|Ι.Ν. Αγ. Βασιλείου
Sympoliteia|Τούμπα|Ι.Ν. Αγ. Δημητρίου
'''


# Settlement | regional dedication | detail id | public phones | public email |
# exact street address when the body publishes one | current detail title.
# Central Metropolis contacts repeated in the page chrome are not body contacts.
PARISH_CONTACT_SOURCE = r'''
Αιγείρα|Ι.Ν. Αγ. Παντελεήμονος|3704|6978951086|||Ιερός Ναός Αγίου Παντελεήμονος Αιγείρας
Αιγές|Ι.Ν. Αγ. Δημητρίου|2669|6974962294|||Ιερός Ναός Αγίου Δημητρίου Αιγών (Λαμπινού)
Αμπελόκηποι|Ι.Ν. Αγ. Αναργύρων|2446|6977873501,2696034303|||Ιερός Ναός Αγίων Αναργύρων Αμπελοκήπων Αιγείρας
Μάρμαρα|Ι.Ν. Αγ. Σπυρίδωνος|2480|2696031560|pathrpanaqiotis@qmail.com||Ιερός Ναός Αγίου Σπυριδωνος Μαρμαρων Αιγειρας
Μοναστήριο|Ι.Ν. Κοιμήσεως Θεοτόκου|3620|6974962294|||Ιερός Ναός Κοιμήσεως Της Θεοτόκου Μοναστηρίου
Χρυσάνθιο|Ι.Ν. Αγ. Αποστόλων|3614|6938020475|||Ιερός Ναός Αγίων Αποστόλων Πέτρου και Παύλου Χρυσανθίου
Ακράτα|Ι.Ν. Αγ. Χαραλάμπους|3477|2696022574||Ιερός Ναός Αγίου Χαραλάμπους, Ακράτα, 25006|Ιερός Ναός Αγίου Χαραλάμπους Ακράτας
Παραλία Πλατάνου|Ι.Ν. Ζωοδόχου Πηγής|3674|6977971590|||Ιερός Ναός Ζωοδόχου Πηγής Παραλίας Πλατάνου
Άμπελος|Ι.Ν. Αγ. Ανδρέου|3841|6973471657|||Ιερός Ναός Αγίου Ανδρέου Αμπέλου
Δάφνη|Ι.Ν. Αγ. Τριάδος|3525|6972272026|||Ιερός Ναός Αγίας Τριάδος Δάφνης
Δάφνη|Ι.Ν. Αγ. Χαραλάμπους|3524|6972272026|||Ιερός Ναός Αγίου Χαραλάμπους Δάφνης
Ψωφίδα|Ι.Ν. Κοιμήσεως Θεοτόκου|2574|2692051490|||Ιερός Ναός Κοιμήσεως Της Θεοτόκου Ψωφίδας
Αίγιο|Καθεδρικός Ι.Ν. Κοιμήσεως Θεοτόκου (Παναγία Φανερωμένη)|2464|6945947680,2691022322||Μητροπόλεως & Παναγοπούλου, Αίγιο|Ιερός Ναός Κοιμήσεως Της Θεοτόκου (Φανερωμένη Αιγίου)
Αίγιο|Ι.Ν. Παμμεγίστων Ταξιαρχών|2474|6981049257,2691022325||Ταξιαρχών και Ελίκης, Αίγιο|Ιερός Ναός Παμμεγίστων Ταξιαρχών Αιγίου
Αίγιο|Ι.Ν. Εισοδίων Θεοτόκου|2460|2691028979||Εισοδίων και Δωδεκανήσου|Ιερός Ναός Εισοδίων Της Θεοτόκου Αιγίου
Αίγιο|Ι.Ν. Αγ. Ανδρέου|2447|6945917621,2691027700||Αγίου Ανδρέου 6, Αίγιο|Ιερός Ναός Αγίου Ανδρέου Αιγίου
Αίγιο|Ι.Ν. Αγ. Κων/νου-Ελένης & Θεοπρ. Άννης|2468|2691028665||Συνοικισμός Νικολάου Πλαστήρα, Αίγιο|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης και Θεοπρομήτορος Άννης Αιγίου
Αίγιο|Ι.Ν. Αγ. Ιωάννου|2462|2691028581||Αγίου Ιωάννου 13, Αίγιο|Ιερός Ναός Αγίου Ιωάννη Προδρόμου Καλλιθέας Αιγίου
Αίγιο|Ι.Ν. Αγ. Αλεξίου|2445|6931008551,2691026018|||Ιερός Ναός Αγίου Αλεξίου Σταφιδαλώνων Αιγίου
Αίγιο|Ι.Ν. Αγ. Λεοντίου|2600|6972599265||Οδός Σκρα, Αίγιο (Περιοχή Παγοποιείου)|Ιερός Ναός Οσίου Λεοντίου Αιγίου
Αίγιο|Ι.Ν. Αγ. Αθανασίου|2442|2691020493|||Ιερός Ναός Αγίου Αθανασίου Αιγίου
Αίγιο|Ι.Ν. Αγ. Αποστόλων Πέτρου & Παύλου|2479|2691025521||Αγίας Τριάδος και Παρασκευής, Οικισμός Μεσσηνέζη, Αίγιο|Ιερός Ναός Αγίων Πρωτοκορυφαίων Αποστόλων Πέτρου και Παύλου
Αίγιο|Ι.Ν. Αγ. Μαρίνης|2470|6946823703,2691029312||25100 Πάροδος Μενελάου, Μυρτιά Αιγιαλείας|Ιερός Ναός Αγίας Μαρίνας Μυρτιάς Αιγίου
Αραχωβίτικα (Βουλωμένο)|Ι.Ν. Μεταμορφώσεως του Σωτήρος|3725|6971650754|inms.sotira@gmail.com||Ιερός Ναός Μεταμορφώσεως του Σωτήρος οικισμού Σωτήρα Αιγίου
Βαλιμίτικα|Ι.Ν. Αγ. Βασιλείου|2452|6973745118||Βαλιμήτικα Αιγιαλείας|Ιερός Ναός Αγίου Βασιλείου Βαλιμιτίκων
Διγιελιώτικα|Ι.Ν. Αγ. Ανδρέου|2449|2691051501||25100 Διγελιώτικα Αιγιαλείας|Ιερός Ναός Αγίου Ανδρέα Διγελιωτίκων
Κουλούρα|Ι.Ν. Υπαπαντής του Χριστού|2486|2691029421||Ιεράς Μονής Ταξιαρχών και Ανδρέα Λόντου, Κουλούρα Αιγίου|Ιερός Ναός Υπαπαντής Του Χριστού Κουλούρας
Κούμαρης|Ι.Ν. Αγ. Ιωάννου|4000|2691027651|||Ιερός Ναός Αγίου Ιωάννου Προδρόμου Κούμαρη
Κουνινά|Ι.Ν. Αγ. Αθανασίου|2444|6995703211||Κουνινά Αιγιαλείας|Ιερός Ναός Αγίου Αθανασίου Κουνινάς
Σέλισσα|Ι.Ν. Αγ. Βασιλείου|3734|6976745330|||Ιερός Ναός Αγίου Βασιλείου Κ. Πτέρης
Διακοπτό|Ι.Ν. Αγ. Τρύφωνος|2485|6984487159,2691041485||Διακοπτό Αιγιαλείας|Ιερός Ναός Αγίου Τρύφωνος Διακοπτού
Ελαιώνας|Ι.Ν. Αγ. Βασιλείου|2453|2691042852||Ελαιώνας Αιγιαλείας|Ιερός Ναός Αγίου Βασιλείου Ελαιώνος
Ελίκη|Ι.Ν. Αγ. Αθανασίου|2443|2691082590||Ελίκη Αιγιαλείας|Ιερός Ναός Αγίου Αθανασίου Ελίκης
Ζαχλωρίτικα|Ι.Ν. Αγ. Χαραλάμπους|2487|6974913977|||Ιερός Ναός Αγίου Χαραλάμπους Ζαχλωριτίκων
Ν. Κερύνεια|Ι.Ν. Παμμ. Ταξιαρχών & Αγ. Αναστασίας|2475|6906859321|||Ιερός Ναός Παμμεγίστων Ταξιαρχών και Αγίας Αναστασίας
Λόφος-Καλυβίτης|Ι.Ν. Αγ. Γεωργίου|2455|2691097266||Λόφος-Καλυβίτη Αιγιαλείας|Ιερός Ναός Αγίου Γεωργίου Λόφου
Μαμουσιά|Ι.Ν. Κοιμήσεως Θεοτόκου|3663|6980695672|||Ιερός Ναός Κοιμήσεως της Θεοτόκου Μαμουσιάς
Νικολέϊκα|Ι.Ν. Αγ. Βαρβάρας|2451|6972844128,2691081625|papaioannis1@yahoo.gr|Νικολαίικα Αιγιαλείας, Τ.Κ. 25100|Ιερός Ναός Αγίας Βαρβάρας Νικολαιίκων
Ριζόμυλος|Ι.Ν. Κοιμήσεως Θεοτόκου|2465|2691082585,6944373232|arathan2005@yahoo.gr||Ιερός Ναός Κοιμήσεως Της Θεοτόκου Ριζομύλου
Ροδιά|Ι.Ν. Αγ. Νικολάου|2472|6981445796,2691082501||Ροδιά Αιγιαλείας|Ιερός Ναός Αγίου Νικολάου Ροδιάς
Τράπεζα|Ι.Ν. Εισοδίων Θεοτόκου|2461|6934217602||Τράπεζα Αιγιαλείας|Ιερός Ναός Εισοδίων Της Θεοτόκου Αιγίου Τραπέζης Αιγιαλείας
Καλάβρυτα|Ι.Ν. Κοιμήσεως Θεοτόκου|2552|2692022204|inkoimiseowtheotokoukalavriton@gmail.com||Μητροπολιτικός Ιερός Ναός Κοιμήσεως Της Θεοτόκου Καλαβρύτων
Κλειτορία|Ι. Ν. Αγ. Δημητρίου|2625|2692031326|||Ιερός Ναός Αγίου Δημητρίου Κλειτορίας
Άβυθος|Ι.Ν. Παμμ. Ταξιαρχών|2473|2691071718||Άβυθος Αιγιαλείας|Ιερός Ναός Παμμεγίστων Ταξιαρχών Αβύθου
Δημητρόπουλο|Ι.Ν. Τιμίου Προδρόμου|2482|6992269794|||Ιερός Ναός Αγίου Τιμίου Προδρόμου Δημητρόπουλου
Λόγγος|Ι.Ν. Αγ. Δημητρίου|2457|6936860825,2691073559||Λόγγος Αιγιαλείας|Ιερός Ναός Αγίου Δημητρίου Λόγγου
Νεραντζιές|Ι.Ν. Αγ. Δημητρίου|2458|2691072896||Νεραντζιές Αιγιαλείας|Ιερός Ναός Αγίου Δημητρίου Νεραντζιών
Πανόραμα|Ι.Ν. Αγ. Παντελεήμονος|2476|2691073397||Πανόραμα Αιγιαλείας|Ιερός Ναός Αγίου Παντελεήμονος Πανοράματος
Ροδοδάφνη|Ι.Ν. Αγ. Σπυρίδωνος|2481|2691071221||Ροδοδάφνη Αιγιαλείας|Ιερός Ναός Αγίου Σπυρίδωνος Ροδοδάφνης
Άγιος Γεώργιος Ροδοδάφνης|Ι.Ν. Αγ. Γεωργίου|2672|6976016528|||Ιερός Ναός Αγίου Γεωργίου Ροδοδάφνης
Σελιανίτικα|Ι.Ν. Αγ. Βασιλείου|2454|6978036436||Επί της Παλαιάς Εθνικής Οδού εντός των Σελιανιτίκων. Είσοδος από την οδό Αγίου Βασιλείου|Ιερός Ναός Αγίου Βασιλείου Σελιανιτίκων
'''


# kind | rank | English name | current Greek title | seat | detail id |
# phones | emails | address | live marker.
EXTRA_CHURCH_SOURCE = r'''
parish|Country Church|Country Church of the Ascension of the Savior (Rouvaliotissa)|Ιερός Ναός Αναλήψεως του Σωτήρος (Ρουβαλιώτισσα)|Rouvaliotissa|4138||||Rouvaliotissa|Αναλήψεως του Σωτήρος
parish|Country Church|Country Church of the Prophet Elijah in Koumari|Ιερός Ναός Προφήτη Ηλία Κούμαρη|Koumari|4112||||Koumari|Προφήτη Ηλία Κούμαρη
parish|Country Church|Country Church of Saints Constantine and Helen in Longos|Ιερός Ναός Αγίων Κωνσταντίνου & Ελένης Λόγγου|Longos|2685|6936860825|||Longos|Αγίων Κωνσταντίνου & Ελένης Λόγγου
parish|Country Church|Country Church of the Transfiguration of the Savior in Rodia|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Ροδιάς|Rodia|4011||||Rodia|Μεταμορφώσεως του Σωτήρος Ροδιάς
parish|Country Church|Country Church of Saint Nicholas in Vergouvitsa|Ιερός Ναός Αγίου Νικολάου Βεργουβίτσας|Vergouvitsa|3781||||Vergouvitsa|Αγίου Νικολάου Βεργουβίτσας
parish|Chapel|Chapel of the Holy Unmercenaries in Aigio|Ιερός Ναός Αγίων Αναργύρων Αιγίου|Aigio|3864||||Aigio|Αγίων Αναργύρων Αιγίου
parish|Chapel|Chapel of Saint Kyriaki in Aigio|Ιερός Ναός Αγίας Κυριακής - Παρεκκλήσιο Ιερού Ναού Αγίου Αθανασίου Αιγίου|Aigio|2466|||οδός Αγίας Κυριακής, Αίγιο|Αγίας Κυριακής
parish|Chapel|Chapel of Saint Luke of Simferopol and Saint Phanourios in Avythos|Ιερός Ναός Αγίου Ιεράρχου Λουκά επισκόπου Συμφερουπόλεως & Αγίου Φανουρίου - Άβυθος|Avythos|2601||||Avythos|Αγίου Ιεράρχου Λουκά
parish|Chapel|Chapel of the Transfiguration of the Savior in Dervenio|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Δερβενίου Αιγιαλείας|Dervenio|3664|6980695672|||Dervenio|Μεταμορφώσεως του Σωτήρος Δερβενίου
parish|Chapel|Chapel of Saint Nicholas in Alyki, Aigio|Ιερός Ναός Αγίου Νικολάου Αλυκής Αιγίου (Παρεκκλήσιο Φανερωμένης)|Aigio|3080||||Alyki, Aigio|Αγίου Νικολάου Αλυκής
parish|Chapel|Chapel of Saint Paraskevi in Aigio|Ιερός Ναός Αγίας Παρασκευής Αιγίου (Παρεκκλήσιο Ιερού Ναού Αγίου Αθανασίου Αιγίου)|Aigio|2478|||25 100 Άγιος Αθανάσιος Αιγίου|Αγίας Παρασκευής Αιγίου
parish|Chapel|Chapel of the Holy Trinity of Panagia Faneromeni in Aigio|Ιερός Ναός Αγίας Τριάδος Αιγίου (Παρεκκλήσιο Ιερού Μητροπολιτικού Ναού Παναγίας Φανερωμένης)|Aigio|2484|2691021528||Μητροπόλεως 1-3, 25100 Αίγιο|Αγίας Τριάδος Αιγίου
parish|Festal Church|Festal Church of Saint Basil in Seliana|Ιερός Ναός Αγίου Βασιλείου Σελιάνας|Seliana|2575||||Seliana|Αγίου Βασιλείου Σελιάνας
parish|Festal Church|Festal Church of Saint George in Mertidi|Ιερός Ναός Αγίου Γεωργίου - Μερτίδι|Mertidi|2614||||Mertidi|Αγίου Γεωργίου
parish|Festal Church|Festal Church of Saints Constantine and Helen in Seliana|Ιερός Ναός Αγίων Κωνσταντίνου & Ελένης Σελιάνας|Seliana|2557||||Seliana|Αγίων Κωνσταντίνου & Ελένης Σελιάνας
parish|Festal Church|Festal Church of Saint Nicholas of Vounena in Voulomeno|Ιερός Ναός Αγίου Νικολάου του "Εν Βουνένοις" (Άγιος Νικολάκης) - Βουλωμένο Αιγίου|Voulomeno, Aigio|3047||||Voulomeno, Aigio|Αγίου Νικολάου του "Εν Βουνένοις"
parish|Festal Church|Byzantine Festal Church of Saint Nicholas in Mavriki|Βυζαντινός Ναός Αγίου Νικολάου Ταξιαρχών Αιγιαλείας (Μαυρίκι)|Mavriki|2661||||Mavriki|Βυζαντινός Ναός Αγίου Νικολάου
parish|Festal Church|Festal Church of the New Martyr Paul in Aroania|Ιερός Ναός Αγίου Νεομάρτυρος Παύλου - Αροανία (Σοποτό)|Aroania|3460||||Aroania|Αγίου Νεομάρτυρος Παύλου
parish|Cemetery Church|Cemetery Church of Saint George in Longos|Ιερός Κοιμητηριακός Ναός Αγίου Γεωργίου Λόγγου|Longos|2671||||Longos|Αγίου Γεωργίου Λόγγου
parish|Cemetery Church|Cemetery Church of Saint Panteleimon in Selianitika|Ιερός Κοιμητηριακός Ναός Αγίου Παντελεήμονος Σελιανιτίκων|Selianitika|2477||||Selianitika|Αγίου Παντελεήμονος Σελιανιτίκων
parish|Cemetery Church|Church of All Saints at Aigio Cemetery|Ιερός Ναός Αγίων Πάντων Κοιμητηρίου Αιγίου|Aigio|3483|2691060683||Κοιμητήριο Αιγίου|Αγίων Πάντων Κοιμητηρίου Αιγίου
parish|Cemetery Church|Cemetery Church of All Saints in Rododafni|Ιερός Κοιμητηριακός Ναός Αγίων Πάντων Ροδοδάφνης|Rododafni|3915||||Rododafni|Αγίων Πάντων Ροδοδάφνης
parish|Hospital Church|Hospital Church of Saint Luke the Apostle and Evangelist in Aigio|Ιερός Ναός Αγίου Αποστόλου και Ευαγγελιστού Λουκά Νοσοκομείου Αιγίου|Aigio|2593|||Γενικό Νοσοκομείο Αιγίου|Αγίου Αποστόλου και Ευαγγελιστού Λουκά
monastery|Monastery Church|Katholikon of the Dormition at Agia Lavra Monastery|Ιερός Ναός Κοιμήσεως Της Θεοτόκου Αγίας Λαύρας (Καθολικό)|Agia Lavra|2674||||Agia Lavra|Ιερός Ναός Κοιμήσεως Της Θεοτόκου Αγίας Λαύρας (Καθολικό)
'''


PILGRIMAGE_SOURCE = r'''
Pilgrimage Church of Panagia Trypiti|Παναγία Τρυπητή|Aigio|2529|2691029333,2691022323||Ιερό Προσκύνημα Παναγίας Τρυπητής (Ζωοδόχου Πηγής), Τ.Κ. 25100, Αίγιο
Pilgrimage Church of Panagia Plataniotissa|Πλατανιώτισσα|Plataniotissa|2530|2692023129,6945448995||Plataniotissa
'''


# Current first-party directory detail plus the current 2026 calendar roster.
# Saint Athanasius at Filia is emitted once as the metochion the calendar also
# identifies, not again as a second exact body.
MONASTERY_SOURCE = r'''
Monastery|Monastery of the Holy Apostles in Seliana-Perithorio|Ιερά Μονή Αγίων Αποστόλων Σελιάνα - Περιθώρι|Seliana-Perithorio|2504|2696039110||
Monastery|Monastery of the Annunciation in Daphne|Ιερά Μονή Ευαγγελιστρίας Δάφνης|Daphne|3462|||
Monastery|Monastery of the Holy Theodores in Aroania|Ιερά Μονή Αγίων Θεοδώρων Αροανίας|Aroania|2505|2692061244||
Monastery|Monastery of Saint John the Theologian in Verino|Ιερά Μονή Αγίου Ιωάννου του Θεολόγου Βερίνου|Verino|2500|2691094248,2691094349,2691094129||
Monastery|Monastery of Agia Lavra|Ιερά Μονή Αγίας Λαύρας|Agia Lavra|2498|2692022363|agialavra1821@gmail.com|https://agialavra.gr/
Monastery|Makellaria Monastery|Ιερά Μονή Μακελλαριάς|Makellaria|2503|2692084485,2692024219|info@moni-makellarias.gr|https://www.moni-makellarias.gr
Monastery|Great Cave Monastery|Ιερά Μονή Μεγάλου Σπηλαίου|Mega Spilaio|2497|2692022401,2692023130,2692023035||
Monastery|Monastery of Saint Nicholas in Vlasia|Ιερά Μονή Αγίου Νικολάου Βλασίας|Vlasia|2506|2692041248||
Monastery|Monastery of the Chief Commanders in Aigialeia|Ιερά Μονή Παμμεγίστων Ταξιαρχών|Aigialeia|2499|2691056300,2691056515||
Monastery|Monastery of the Holy Trinity in Akrata|Ιερά Μονή Αγίας Τριάδος Ακράτας|Akrata|2501|2696022567,6974481813|info@monastiriaka-ergoxeira.gr|https://monastiriakrata.gr/
Monastery|Monastery of the Holy Trinity in Voura|Ιερά Μονή Αγίας Τριάδος Βουρών (Τράπεζας Διακοπτού)|Voura, Diakopto|2502|2692041247||
'''

MONASTERY_ADDRESSES = {
    "2500": (
        "ΙΕΡΑ ΜΟΝΗ ΑΓ. ΙΩΑΝΝΟΥ ΤΟΥ ΘΕΟΛΟΓΟΥ, "
        "25100, ΒΕΡΙΝΟ ΑΙΓΙΑΛΕΙΑΣ"
    ),
    "2497": "IEPA MONH MEΓAΛOY ΣΠHΛAIOY 25001, KAΛABPYTA",
    "2498": "Καλάβρυτα, Καλάβρυτα, 25001, ΑΧΑΪΑΣ",
    "2499": "Ι.Μ. Παμμεγίστων Ταξιαρχών, 25100 Μελίσσια Αιγιαλείας",
    "2501": "Ακράτα, Αχαΐα, 25006",
    "2502": "25003 ΤΡΑΠΕΖΑ, ΔΙΑΚΟΠΤΟ",
    "2503": "Ιερά Μονή Μακελαριάς, Δήμος Καλαβρύτων, 250 01",
}


# Current exact metochia in Greece from the 2026 Metropolis calendar.
METOCHION_SOURCE = r'''
Metochion of Saint Alexios in Patras, of Agia Lavra Monastery|Μετόχιο Αγίου Αλεξίου εν Πάτραις Ιεράς Μονής Αγίας Λαύρας|Patras||
Metochion of Saint Athanasius in Filia, of Agia Lavra Monastery|Μετόχιο Αγίου Αθανασίου εν Φιλίοις Ιεράς Μονής Αγίας Λαύρας|Filia|2692036397|
Metochion of Saint George Basta in Lechaina, of Agia Lavra Monastery|Μετόχιο Αγίου Γεωργίου Μπάστα εν Λεχαινοίς Ιεράς Μονής Αγίας Λαύρας|Lechaina||
Metochion of Saint Nicholas in Amaliada, of the Holy Theodores Monastery|Μετόχιο Αγίου Νικολάου εν Αμαλιάδι Ιεράς Μονής Αγίων Θεοδώρων|Amaliada||
Metochion of the Dormition in Prosilio, of the Chief Commanders Monastery|Μετόχιο Κοιμήσεως Θεοτόκου εν Προσηλίω Αιγιαλείας Ιεράς Μονής Παμμεγίστων Ταξιαρχών|Prosilio, Aigialeia||
Metochion of Saint Mary Magdalene in Rafina, of Great Cave Monastery|Μετόχιο Αγίας Μαγδαληνής Ραφίνας Αττικής Ιεράς Μονής Μεγάλου Σπηλαίου|Rafina||
'''


DEDICATION_RULES = (
    ("Παμμ. Ταξιαρχών & Αγ. Αναστασίας",
     "the Chief Commanders and Saint Anastasia"),
    ("Αγ. Κων/νου-Ελένης & Θεοπρ. Άννης",
     "Saints Constantine and Helen and Saint Anna"),
    ("Αγ. Αποστόλων Πέτρου & Παύλου",
     "the Holy Apostles Peter and Paul"),
    ("Καθεδρικός Ι.Ν. Κοιμήσεως Θεοτόκου",
     "the Dormition of the Theotokos"),
    ("Κοιμήσεως Θεοτόκου", "the Dormition of the Theotokos"),
    ("Γεννέσεως Θεοτόκου", "the Nativity of the Theotokos"),
    ("Εισοδίων Θεοτόκου", "the Entrance of the Theotokos"),
    ("Ευαγγελισμού", "the Annunciation"),
    ("Ζωοδόχου Πηγής", "the Life-giving Spring"),
    ("Υπαπαντής του Χριστού", "the Presentation of Christ"),
    ("Υπαπαντής Χριστού", "the Presentation of Christ"),
    ("Μεταμορφώσεως του Σωτήρος", "the Transfiguration of the Savior"),
    ("Μεταμορφώσεως Σωτήρος", "the Transfiguration of the Savior"),
    ("Αναλήψεως Χριστού", "the Ascension of Christ"),
    ("Τιμίας Ζώνης", "the Holy Belt of the Theotokos"),
    ("Τιμίου Προδρόμου", "Saint John the Forerunner"),
    ("Παμμεγίστων Ταξιαρχών", "the Chief Commanders"),
    ("Παμμ. Ταξιαρχών", "the Chief Commanders"),
    ("Τριών Ιεραρχών", "the Three Hierarchs"),
    ("Αγ. 40 Μαρτύρων", "the Forty Martyrs"),
    ("Αγ. Αναργύρων", "the Holy Unmercenaries"),
    ("Αγ. Αποστόλων", "the Holy Apostles"),
    ("Αγ. Θεοδώρων", "the Holy Theodores"),
    ("Αγ. Τριάδος", "the Holy Trinity"),
    ("Αγ. Αθανασίου", "Saint Athanasius"),
    ("Αγ. Αλεξίου", "Saint Alexios"),
    ("Αγ. Ανδρέου", "Saint Andrew"),
    ("Αγ. Βαρβάρας", "Saint Barbara"),
    ("Αγ. Βασιλείου", "Saint Basil"),
    ("Αγ. Βλασίου", "Saint Blaise"),
    ("Αγ. Γεωργίου", "Saint George"),
    ("Αγ. Δημητρίου", "Saint Demetrius"),
    ("Αγ. Ιωάννου Θεολόγου", "Saint John the Theologian"),
    ("Αγ. Ιωάννου Χρυσοστόμου", "Saint John Chrysostom"),
    ("Αγ. Ιωάννου", "Saint John"),
    ("Αγ. Κωνσταντίνου", "Saint Constantine"),
    ("Αγ. Λεοντίου", "Saint Leontios"),
    ("Αγ. Μαρίνης", "Saint Marina"),
    ("Αγ. Νικολάου", "Saint Nicholas"),
    ("Αγ. Παντελεήμονος", "Saint Panteleimon"),
    ("Αγ. Παρασκευής", "Saint Paraskevi"),
    ("Αγ. Σπυρίδωνος", "Saint Spyridon"),
    ("Αγ. Τρύφωνος", "Saint Tryphon"),
    ("Αγ. Χαραλάμπους", "Saint Charalambos"),
    ("Αγίου Γρηγορίου", "Saint Gregory"),
)

SEAT_OVERRIDES = {
    "Αίγιο": "Aigio",
    "Αιγείρα": "Aigeira",
    "Ακράτα": "Akrata",
    "Αροανία": "Aroania",
    "Διακοπτό": "Diakopto",
    "Καλάβρυτα": "Kalavryta",
    "Κλειτορία": "Kleitoria",
    "Πλατανιώτισσα": "Plataniotissa",
    "Ροδοδάφνη": "Rododafni",
    "Σελιανίτικα": "Selianitika",
}

GREEK_TO_LATIN = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}

FORBIDDEN_PUNCTUATION = re.compile("[\u2013\u2014]")
ALLOWED_HOSTS = {
    "www.imkalaig.gr", "imkalaig.gr",
    "ecclesiagreece.gr", "www.ecclesiagreece.gr",
    "agialavra.gr", "www.agialavra.gr",
    "www.moni-makellarias.gr", "moni-makellarias.gr",
    "monastiriakrata.gr", "www.monastiriakrata.gr",
}

EXPECTED_REGION_COUNTS = {
    "Aigeira": 12,
    "Akrata": 15,
    "Aroania": 24,
    "Vostitsa": 27,
    "Diakopto": 15,
    "Kalavryta": 39,
    "Kleitoria": 19,
    "Sympoliteia": 13,
}
EXPECTED_TOTAL = 207
EXPECTED_KINDS = {"monastery": 18, "parish": 189}
EXPECTED_RANKS = {
    "Cathedral Parish Church": 1,
    "Cemetery Church": 4,
    "Chapel": 7,
    "Country Church": 5,
    "Festal Church": 6,
    "Hospital Church": 1,
    "Metropolitan Parish Church": 1,
    "Monastery": 11,
    "Monastery Church": 1,
    "Monastery Metochion": 6,
    "Parish Church": 162,
    "Pilgrimage Church": 2,
}
EXPECTED_CONTACT_BODIES = 68
EXPECTED_PHONE_BODIES = 68
EXPECTED_PHONE_VALUES = 88
EXPECTED_EMAIL_BODIES = 8
EXPECTED_EMAIL_VALUES = 8
EXPECTED_SITE_BODIES = 3
EXPECTED_FAX_VALUES = {
    "2691094129",
    "2692023035",
    "2691056515",
}


def unicase(value):
    value = unicodedata.normalize("NFD", value)
    return "".join(
        char for char in value.casefold()
        if unicodedata.category(char) != "Mn"
    )


def transliterate(value):
    value = unicodedata.normalize("NFD", value)
    output = []
    for char in value:
        if unicodedata.category(char) == "Mn":
            continue
        lower = char.lower()
        if lower in GREEK_TO_LATIN:
            text = GREEK_TO_LATIN[lower]
            if char.isupper():
                text = text[:1].upper() + text[1:]
            output.append(text)
        else:
            output.append(char)
    return "".join(output)


def english_seat(value):
    if value in SEAT_OVERRIDES:
        return SEAT_OVERRIDES[value]
    return transliterate(value)


def dedication_name(value):
    compact = " ".join(value.split())
    for source, english in DEDICATION_RULES:
        if source in compact:
            return english
    cleaned = re.sub(r"^(?:Καθεδρικός )?Ι\.\s*Ν\.\s*", "", compact)
    return transliterate(cleaned)


def parse_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_parishes():
    records = []
    counts = Counter()
    seen = set()
    for raw in PARISH_SOURCE.strip().splitlines():
        region, seat, local = raw.split("|", 2)
        key = (seat, local)
        if key in seen:
            raise ValueError("duplicate current regional parish: %r" % (key,))
        seen.add(key)
        counts[region] += 1
        records.append((region, seat, local))
    if dict(counts) != EXPECTED_REGION_COUNTS:
        raise ValueError("Kalavryta regional totals drifted: %r" % dict(counts))
    if len(records) != 164:
        raise ValueError("expected 164 current regional rows")
    return records


def parse_parish_contacts():
    contacts = {}
    for raw in PARISH_CONTACT_SOURCE.strip().splitlines():
        fields = raw.split("|", 6)
        if len(fields) != 7:
            raise ValueError("invalid Kalavryta parish contact row")
        seat, local, item_id, phones, emails, address, marker = fields
        key = (seat, local)
        if key in contacts:
            raise ValueError("duplicate Kalavryta parish contact: %r" % (key,))
        contacts[key] = {
            "url": church_url(item_id),
            "phones": parse_values(phones),
            "emails": parse_values(emails),
            "address": address,
            "marker": marker,
        }
    parish_keys = {(seat, local) for _, seat, local in parse_parishes()}
    if not set(contacts).issubset(parish_keys):
        raise ValueError("parish contacts do not reconcile to the live roster")
    return contacts


def add_contact(row, phones, emails, site, contact_sources):
    if phones:
        row["phones"] = phones
    if emails:
        row["emails"] = emails
    if site:
        row["site"] = site
    if phones or emails or site:
        row["contact_sources"] = list(dict.fromkeys(contact_sources))
        row["contact_checked"] = CHECKED


def build_rows():
    rows = []
    live_checks = defaultdict(set)
    contacts = parse_parish_contacts()

    for number, (region, seat, local) in enumerate(parse_parishes(), 1):
        key = (seat, local)
        contact = contacts.get(key)
        sources = [REGION_PAGE, REGULATION_PDF]
        address = seat
        if contact:
            sources.insert(1, contact["url"])
            live_checks[contact["url"]].add(contact["marker"])
            if contact["address"]:
                address = contact["address"]
        rank = "Parish Church"
        if local.startswith("Καθεδρικός"):
            rank = "Cathedral Parish Church"
        elif seat == "Καλάβρυτα" and local == "Ι.Ν. Κοιμήσεως Θεοτόκου":
            rank = "Metropolitan Parish Church"
        name = "%s of %s in %s" % (
            rank,
            dedication_name(local),
            english_seat(seat),
        )
        row = {
            "id": "gr-kalavryta-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s - %s" % (seat, local),
            "seat": english_seat(seat),
            "country": "GR",
            "address": [address, "Greece"],
            "sources": sources,
            "checked": CHECKED,
        }
        live_checks[REGION_PAGE].update((seat, local))
        if contact:
            add_contact(
                row,
                contact["phones"],
                contact["emails"],
                "",
                [contact["url"]],
            )
        rows.append(row)

    next_id = 165
    for raw in EXTRA_CHURCH_SOURCE.strip().splitlines():
        fields = raw.split("|")
        # Several source rows spell out a seat-level fallback address after an
        # intentionally empty address slot. Normalize that harmless extra slot
        # before unpacking the fixed body schema.
        if len(fields) == 11 and not fields[8]:
            del fields[8]
        if len(fields) != 10:
            raise ValueError("invalid Kalavryta extra church row")
        (kind, rank, name, local, seat, item_id, phones, emails,
         address, marker) = fields
        url = church_url(item_id)
        index = CHURCH_PAGE_2 if item_id == "2484" else CHURCH_INDEX
        row = {
            "id": "gr-kalavryta-%03d" % next_id,
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address or seat, "Greece"],
            "sources": [index, url],
            "checked": CHECKED,
        }
        parsed_phones = parse_values(phones)
        parsed_emails = parse_values(emails)
        add_contact(row, parsed_phones, parsed_emails, "", [url])
        live_checks[url].add(marker)
        rows.append(row)
        next_id += 1

    for raw in PILGRIMAGE_SOURCE.strip().splitlines():
        name, local, seat, item_id, phones, emails, address = raw.split("|", 6)
        url = pilgrimage_url(item_id)
        row = {
            "id": "gr-kalavryta-%03d" % next_id,
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address or seat, "Greece"],
            "sources": [PILGRIMAGE_INDEX, url, REGULATION_PDF],
            "checked": CHECKED,
        }
        add_contact(
            row, parse_values(phones), parse_values(emails), "", [url]
        )
        live_checks[url].add(local)
        rows.append(row)
        next_id += 1

    for raw in MONASTERY_SOURCE.strip().splitlines():
        rank, name, local, seat, item_id, phones, emails, site = raw.split("|", 7)
        url = monastery_url(item_id)
        sources = [MONASTERY_INDEX, url, CALENDAR_PDF]
        if site:
            sources = [url, CALENDAR_PDF, site]
        row = {
            "id": "gr-kalavryta-%03d" % next_id,
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [MONASTERY_ADDRESSES.get(item_id, seat), "Greece"],
            "sources": sources,
            "checked": CHECKED,
        }
        contact_sources = [url]
        if item_id == "2503":
            contact_sources.append(CALENDAR_PDF)
        if site:
            contact_sources.append(site)
            live_checks[site].update(parse_values(emails))
        add_contact(
            row, parse_values(phones), parse_values(emails), site,
            contact_sources,
        )
        live_checks[url].add(local)
        rows.append(row)
        next_id += 1

    for raw in METOCHION_SOURCE.strip().splitlines():
        name, local, seat, phones, emails = raw.split("|", 4)
        row = {
            "id": "gr-kalavryta-%03d" % next_id,
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery Metochion",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [CALENDAR_PDF],
            "checked": CHECKED,
        }
        add_contact(
            row, parse_values(phones), parse_values(emails), "",
            [CALENDAR_PDF],
        )
        rows.append(row)
        next_id += 1

    if next_id != EXPECTED_TOTAL + 1:
        raise ValueError("Kalavryta body numbering drifted")
    return rows, live_checks


ROWS, LIVE_CHECKS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS if row.get("seat")}


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
    if parsed.scheme != "https" or parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Kalavryta candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kalavryta candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_regional_parish_rows": 164,
        "regulated_parish_rows": 163,
        "regulated_pilgrimage_rows": 2,
        "published_pilgrimage_rows": 2,
        "current_exact_extra_church_rows": 24,
        "current_calendar_active_monastery_identities": 12,
        "published_monastery_rank_rows": 11,
        "current_greek_metochion_rows": 6,
        "parish_kind_rows": 189,
        "monastery_kind_rows": 18,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "public_fax_values": len(EXPECTED_FAX_VALUES),
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_TOTAL,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Kalavryta ledger summary drifted")
    for key in (
            "candidates", "source_reconciliations",
            "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Kalavryta ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kalavryta ledger item has invalid sources")
            for source_url in sources:
                validate_url(
                    source_url, entry.get("candidate_id") or key
                )
    if any(FORBIDDEN_PUNCTUATION.search(value)
           for value in walk_strings(ledger)):
        raise ValueError("Kalavryta ledger contains forbidden punctuation")
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    forbidden_central_values = {
        "2691021776", "2691021777",
        "grammateia.imka@gmail.com", "imkaigial@gmail.com",
    }
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
        if any("\u0370" <= char <= "\u03ff" for char in item["name"]):
            raise ValueError("%s lacks a complete English name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(value)
               for value in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        sources = list(item.get("sources") or [])
        if not sources or len(sources) > 3 or len(sources) != len(set(sources)):
            raise ValueError("%s lacks valid sources" % row_id)
        for source_url in sources:
            validate_url(source_url, row_id)
        item["sources"] = sources
        item["cite"] = list(sources)
        phones = list(item.get("phones") or [])
        emails = list(item.get("emails") or [])
        site = item.get("site")
        contact_sources = list(item.get("contact_sources") or [])
        has_contact = bool(phones or emails or site)
        if has_contact:
            if not contact_sources or item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            if len(contact_sources) != len(set(contact_sources)):
                raise ValueError("%s repeats contact sources" % row_id)
            for phone in phones:
                if not re.fullmatch(r"[26]\d{9}", phone):
                    raise ValueError("%s carries an invalid phone" % row_id)
            for email in emails:
                if not re.fullmatch(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                        email):
                    raise ValueError("%s carries an invalid email" % row_id)
            for source_url in contact_sources:
                validate_url(source_url, row_id)
                if source_url not in sources:
                    raise ValueError("contact source is outside identity sources")
            if site:
                validate_url(site, row_id)
                if urlparse(site).netloc in {
                        "www.imkalaig.gr", "imkalaig.gr",
                        "www.ecclesiagreece.gr", "ecclesiagreece.gr"}:
                    raise ValueError("%s carries a parent site as body site" % row_id)
        elif contact_sources or "contact_checked" in item:
            raise ValueError(
                "%s carries contact provenance without contact data" % row_id
            )
        if forbidden_central_values.intersection(phones + emails):
            raise ValueError("%s inherited a central Metropolis contact" % row_id)
        if not item.get("address"):
            raise ValueError("%s lacks an address" % row_id)
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        result.append(item)

    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Kalavryta English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Kalavryta rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Kalavryta kind totals drifted: %r" % dict(kinds))
    metrics = (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site"))
            for item in result),
        sum(bool(item.get("phones")) for item in result),
        sum(len(item.get("phones") or []) for item in result),
        sum(bool(item.get("emails")) for item in result),
        sum(len(item.get("emails") or []) for item in result),
        sum(bool(item.get("site")) for item in result),
    )
    expected_metrics = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
    )
    if metrics != expected_metrics:
        raise ValueError("Kalavryta contact coverage drifted: %r" % (metrics,))
    all_phones = {
        phone for item in result for phone in item.get("phones") or []
    }
    if not EXPECTED_FAX_VALUES.issubset(all_phones):
        raise ValueError("Kalavryta public fax coverage drifted")
    current_keys = {
        (item["seat"], item["local"])
        for item in result[:164]
    }
    if not any("Βελλά" in local and "Κοιμήσεως" in local
               for _, local in current_keys):
        raise ValueError("current Vella parish split is missing")
    if not any("Μάρμαρα" in local and "Σπυρίδωνος" in local
               for _, local in current_keys):
        raise ValueError("current Marmara parish split is missing")
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
    }


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    }
    is_pdf = url in {CALENDAR_PDF, REGULATION_PDF}
    if is_pdf:
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=90) as response:
        payload = response.read(4096) if is_pdf else response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return unicase(" ".join(text.split()))


def check_live():
    checks = {url: set(markers) for url, markers in LIVE_CHECKS.items()}
    checks.setdefault(REGION_PAGE, set()).add("Αρχιερατικές Περιφέρειες")
    checks[CHURCH_INDEX] = {"ΙΕΡΟΙ ΝΑΟΙ"}
    checks[CHURCH_PAGE_2] = {"ΙΕΡΟΙ ΝΑΟΙ"}
    checks[MONASTERY_INDEX] = {"ΙΕΡΕΣ ΜΟΝΕΣ"}
    checks[PILGRIMAGE_INDEX] = {"ΙΕΡΑ ΠΡΟΣΚΥΝΗΜΑΤΑ"}
    checks[CHURCH_OF_GREECE_PAGE] = {"Καλαβρύτων και Αιγιαλείας"}
    checks[REGULATION_PDF] = set()
    checks[CALENDAR_PDF] = set()

    def one(item):
        url, markers = item
        payload, content_type = fetch(url)
        if url in {CALENDAR_PDF, REGULATION_PDF}:
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("Kalavryta source is not a PDF: %s" % url)
            return url
        if "html" not in content_type:
            raise ValueError("non-HTML Kalavryta source: %s" % url)
        page = normalized_page(payload)
        missing = [
            marker for marker in markers
            if unicase(" ".join(marker.split())) not in page
        ]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        return url

    with ThreadPoolExecutor(max_workers=16) as executor:
        list(executor.map(one, checks.items()))
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
            print("Kalavryta live checks passed for %d source pages" % checked)
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Kalavryta checks passed: %d bodies, %d phone bodies, "
                "%d public phone values, %d fax values, %d email bodies, "
                "%d body sites" % (
                    len(rows),
                    sum(bool(item.get("phones")) for item in rows),
                    sum(len(item.get("phones") or []) for item in rows),
                    len(EXPECTED_FAX_VALUES),
                    sum(bool(item.get("emails")) for item in rows),
                    sum(bool(item.get("site")) for item in rows),
                )
            )
    except Exception as exc:
        print("Kalavryta check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
