#!/usr/bin/env python3
"""Validate the independently audited Kefallinia worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_kefallinia_country.py --check
    python tools/directory_kefallinia_country.py --check-live
    python tools/directory_kefallinia_country.py --dump
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
PARENT = "gr-kefallinia"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "kefallinia_country.json"
)
LEGAL_PDF = "https://api.et.gr/apiFEK/2/2019/3311/pdf"
AMENDMENT_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2020_noembrios.pdf"
)
OFFICIAL_PROFILE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/kephallenias"
)
CALENDAR_REPORT = (
    "https://voutospress.gr/wp-content/uploads/2024/01/"
    "%CE%A6%CF%81%CE%B1%CE%B3%CE%BA%CE%AC%CF%84%CE%B1-59%CE%BF-"
    "%CF%84%CE%B5%CF%8D%CF%87.-%CE%99%CE%B1%CE%BD.-2024-"
    "%CF%83%CE%B5%CE%BB.-12.pdf"
)
SAINT_GERASIMOS_SITE_LEAD = "https://sfantulgherasim.ro/el/manastirea/"

ALLOWED_HOSTS = {
    "api.et.gr",
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "voutospress.gr",
    "www.voutospress.gr",
    "sfantulgherasim.ro",
}
FORBIDDEN_PUNCTUATION = re.compile(r"[\u2013\u2014]")


# Legal seat | legal dedication. Line order is the order printed in Article 1
# of regulation 2659/1589 in FEK B 3311/29.08.2019. The 2020 amendment
# republishes the same 167 identities and changes the regional headings and
# demographic columns. The combined Argostoli and Spilia source cell is
# resolved into the six Argostoli rows followed by the separately printed
# Spilia row.
PARISH_ROWS = r'''
Αργοστόλι|Ευαγγελισμός της Θεοτόκου Μητροπολ. Ναός
Αργοστόλι|Ταξιάρχαι
Αργοστόλι|Εισόδια της Θεοτόκου- Σισσιωτίσσης
Αργοστόλι|Αγ. Νικόλαος
Αργοστόλι|Αγ. Ελευθέριος
Αργοστόλι|Αγ. Σπυρίδων
Σπήλια|Κοίμησις Θεοτόκου
Αγκών|Κοίμησις Θεοτόκου
Βαλσαμάτα|Ταξιάρχαι
Φραγκάτα|Κοίμησις Θεοτόκου
Δαυγάτα|Αγ. Γεώργιος
Δειλινάτα|Αγ. Ιωάννης Πρόδρομος
Δεμουτσαντάτα|Κοίμησις Θεοτόκου
Επανωχώριον|Αγ. Δημήτριος
Ζόλα|Αγ. Δημήτριος
Ζόλα|Υπαπαντή του Κυρίου
Καρδακάτα|Γενέσιον της Θεοτόκου
Κοντογουράτα|Αγ. Παντελεήμων
Πετρικάτα|Αγ. Γεώργιος
Ρίζα|Κοίμησις Θεοτόκου
Κοκολάτα|Αγ. Παρασκευή
Κομποθεκράτα|Αγ. Νικόλαος
Κουρουκλάτα|Αγ. Ιωάννης Χρυσόστομος
Μηνιές|Γενέσ. Θεοτόκου- Αγ. Στέφανος
Μιχάτα|Αγ. Κυριακή
Νύφιον|Αγ. Ιωάννης Πρόδρομος
Τρωϊαννάτα|Αγ. Δημήτρης
Φαρακλάτα|Αγ. Νικόλαος
Προκοπάτα|Αγ. Κυριακή
Ραζάτα|Αγ. Ιωάννης Θεολόγος
Φάρσα|Αγ. Χριστόφορος
Ληξούριον|Μεταμόρφ. Σωτήρος- Παντοκράτορος
Ληξούριον|Αγ. Γεράσιμος
Ληξούριον|Αγ. Νικόλαος- Λειβαθινάδων
Ληξούριον|Αγ. Νικόλαος -Μηνιατών
Ληξούριον|Κοίμησις Θεοτόκου- Περλιγκάδων
Ληξούριον|Αγ. Σπυρίδων
Ληξούριον|Ταξιάρχαι
Ληξούριον|Αγ. Τριάς
Ληξούριον|Αγ. Χαράλαμπος
Αγ. Δημήτριος|Αγ. Δημήτριος
Αγ. Θέκλα|Αγ. Θέκλα
Βόβυκες|Αγ. Δημήτριος
Αθέρας|Ευαγγ. Θεοτόκου- Αγ. Παρασκευή
Βλιχάτα|Αγ. Δημήτριος
Βουνί|Αγ. Δημήτριος
Δαμουλιανάτα|Κοίμησις Θεοτόκου
Δελλαπορτάτα|Γενέσιον Θεοτόκου
Καλλάτα|Αγ. Δημήτριος
Καμιναράτα|Προφήτης Ηλίας
Κοντογενάδα|Αγ. Ιωάννης Θεολόγος
Κουβαλάτα|Γενέσιον Θεοτόκου
Λιβάδι|Αγ. Διονύσιος
Λουκεράτα|Αγ. Παντελεήμων
Μαντζαβινάτα|Αγ. Σοφία
Μιχαλιτσάτα|Αγ. Μαρίνα
Μονοπολάτα|Αγ. Παρασκευή
Δεματορά|Εισόδια Θεοτόκου
Παρισάτα|Κοίμησις Θεοτόκου
Ρίφιον|Αγ. Νικόλαος
Σκηνέας|Εισόδια Θεοτόκου
Σουλλάροι|Αγ. Νικόλαος
Φαβατάτα|Αγ. Ιωάννης Πρόδρομος
Μαντουκάτα|Ταξιάρχαι
Χαβδάτα|Άγιοι Απόστολοι
Χαβριάτα|Κοίμησις Θεοτόκου
Σάμη|Κοίμησις Θεοτόκου
Γριζάτα|Μεταμόρφωσις Σωτήρος
Ζερβάτα|Αγ. Ιωάννης Πρόδρομος
Καταποδάτα|Αγ. Σπυρίδων
Διγαλέτο (Πυργί)|Κοίμησις Θεοτόκου
Τσακαρισιάνο|Αγ. Παρασκευή
Χαράκτιον|Άγιοι Πάντες
Καραβόμυλος|Αγ. Ιωάννης Πρόδρομος
Κουλουράτα|Προφήτης Ηλίας
Πουλάτα|Αγ. Παντελεήμων
Χαλιωτάτα|Αγ. Νικόλαος
Άσσος|Αγ. Νικόλαος (Αγ. Γεώργιος-Υ.Θ.)
Αντυπάτα|Ανάστασις του Κυρίου
Βαρύ|Αγ. Στέφανος
Βασιλικάδες|Αγ. Σπυρίδων
Βιγκλί|Αγ. Σπυρίδων
Δεφαρανάτα|Αγ. Λάζαρος
Καρυά|Κοίμησις Θεοτόκου
Κοκολάτα|Αγ. Νικόλαος
Κομιτάτα|Κοίμησις Θεοτόκου
Κονιδαράτα|Αγ. Γεράσιμος
Κοθρέας|Κοίμησις Θεοτόκου
Μαρκουλάτα|Γενέσιον Αγ. Ιωάννου του Προδρόμου
Μεσοβούνια|Αγ. Παρασκευή
Ματσουκάτα|Υπαπαντή του Κυρίου
Νεοχώριον|Αγ. Σπυρίδων
Πλαγιά|Ζωοδόχος Πηγή
Τουλιάτα|Εισόδια Θεοτόκου
Τσελεντάτα|Αγ. Γεράσιμος
Φισκάρδον|Γενέσιον Θεοτόκου
Χαλικερή|Κοίμησις Θεοτόκου
Αγία Ευφημία|Αγ. Ευφημία
Δρακοπουλάτα|Αγ. Μηνάς
Φερεντινάτα|Μεταμόρφωσις Σωτήρος
Δενδρινάτα|Αγ. Κωνσταντίνος
Διβαράτα|Αγ. Νικόλαος
Δρακάτα|Ζωοδόχος Πηγή
Λεκατσάτα|Ευαγγελισμός Θεοτόκου
Άνω Μεριά|Υπαπαντή του Κυρίου
Καρουσάτα (Αντυπάτα)|Ευαγγελισμός Θεοτόκου
Λογαράτα|Αγ. Ανάργυροι
Λουκάτα|Αγ. Ιωάννης Θεολόγος
Μπεκατωράτα|Κοίμησις Θεοτόκου
Ποταμιανάτα|Αγ. Γεώργιος
Μακρυώτικα|Αγ. Δημήτριος
Πνευματικάτα|Αγ. Γεράσιμος
Βασιλοπουλάτα|Ανάληψις του Κυρίου
Αγ. Ειρήνη|Αγ. Ειρήνη
Αγ. Ειρήνη|Αγ. Στέφανος
Αγ. Ειρήνη|Εισόδια Θεοτόκου
Αγ. Νικόλαος|Άγιοι Τεσσαράκοντα
Μοναστηράκιον|Υπ. Θεοτόκου Μυρτιδιωτίσσης
Ξενόπουλον|Αγ. Κυριακή
Ανδρεολάτα|Αγ. Ιωάννης Θεολόγος
Καπανδρίτι|Κοίμησις Θεοτόκου
Αργίνια|Κοίμησις Θεοτόκου
Ατσουπάδες|Αγ. Παρασκευή
Βαλεριάνο|Αγ. Απόστολοι
Θηράμονα|Αγ. Ιωάννης Θεολόγος
Θηράμονα|Αγ. Δημήτριος
Καμπιτσάτα|Αγ. Προκόπιος
Κατελειός|Ταξιάρχαι
Κολαΐτη|Αγ. Μαρίνα
Μαυράτα|Κοίμησις Θεοτόκου
Μαρκόπουλο|Κοίμησις Θεοτόκου
Πάστρα|Κοίμησις Θεοτόκου Γραβαλιωτίσσης
Πόρος|Μεταμόρφωσις Σωτήρος
Αννινάτα|Υπ. Θεοτόκου-Βλαχερνών
Ασπρογέρακας|Αγ. Παρασκευή
Ρατζακλί|Αγ. Ιωάννης Πρόδρομος
Σκάλα|Αγ. Γεράσιμος
Σπαθίον|Προφήτης Ηλίας
Τζαννάτα|Γενεσ. Αγ. Ιωάννου Προδρόμου
Αφραγιάς|Αγ. Ευπραξία
Βλαχάτα|Αγ. Μαρίνα
Δοριζάτα|Κοίμησις Θεοτόκου
Καλλιγάτα|Κοίμησις Θεοτόκου
Καλλιγάτα|Μεταμόρφωσις Σωτήρος
Κουρκουμελάτα|Εισόδια της Θεοτόκου
Μεταξάτα|Αγ. Παρασκευή
Ντομάτα|Εισόδια Θεοτόκου
Καραβάδος|Αγ. Κωνσταντίνου και Ελένης
Περατάτα|Κοίμησις Θεοτόκου
Τραυλιάτα|Μεταμόρφωσις Σωτήρος
Κάστρο|Ευαγγελισμός Θεοτόκου
Κεραμειές|Αγ. Νικόλαος
Σπαρτιά|Κοίμησις Θεοτόκου
Κλείσματα|Αγ. Σπυρίδων
Κοριάννα|Κοίμησις Θεοτόκου
Κουντουράτα|Αγ. Νικόλαος
Λακύθρα|Αγ. Άννα
Λακύθρα|Κοίμοισις Θεοτόκου - Μεσσών
Λακύθρα|Κοίμησις Θεοτόκου- Γαρδελιωτίσσης
Φωκάτα|Αγ. Ιωάννης Πρόδρομος
Λουρδάτα|Ευαγγελισμός Θεοτόκου
Μουσάτα|Αγ. Νικόλαος
Ποριαράτα|Αγ. Σπυρίδων-Αγ. Ακυλίνα
Πεσσάδες|Ευαγγελισμός Θεοτόκου
Σβορωνάτα|Αγ. Νικόλαος
Σαρλάτα|Αγ. Ιωάννης Θεολόγος
Σιμωτάτα|Κοίμησις Θεοτόκου
'''


DEDICATIONS = {
    "Άγιοι Απόστολοι": "the Holy Apostles",
    "Άγιοι Πάντες": "All Saints",
    "Άγιοι Τεσσαράκοντα": "the Forty Holy Martyrs",
    "Αγ. Άννα": "Saint Anna",
    "Αγ. Ανάργυροι": "the Holy Unmercenaries",
    "Αγ. Απόστολοι": "the Holy Apostles",
    "Αγ. Γεράσιμος": "Saint Gerasimos",
    "Αγ. Γεώργιος": "Saint George",
    "Αγ. Δημήτρης": "Saint Demetrius",
    "Αγ. Δημήτριος": "Saint Demetrius",
    "Αγ. Διονύσιος": "Saint Dionysius",
    "Αγ. Ειρήνη": "Saint Irene",
    "Αγ. Ελευθέριος": "Saint Eleftherios",
    "Αγ. Ευπραξία": "Saint Eupraxia",
    "Αγ. Ευφημία": "Saint Euphemia",
    "Αγ. Θέκλα": "Saint Thekla",
    "Αγ. Ιωάννης Θεολόγος": "Saint John the Theologian",
    "Αγ. Ιωάννης Πρόδρομος": "Saint John the Forerunner",
    "Αγ. Ιωάννης Χρυσόστομος": "Saint John Chrysostom",
    "Αγ. Κυριακή": "Saint Kyriaki",
    "Αγ. Κωνσταντίνος": "Saint Constantine",
    "Αγ. Κωνσταντίνου και Ελένης": "Saints Constantine and Helen",
    "Αγ. Λάζαρος": "Saint Lazarus",
    "Αγ. Μαρίνα": "Saint Marina",
    "Αγ. Μηνάς": "Saint Menas",
    "Αγ. Νικόλαος": "Saint Nicholas",
    "Αγ. Νικόλαος (Αγ. Γεώργιος-Υ.Θ.)": (
        "Saint Nicholas with Saint George and the Theotokos"
    ),
    "Αγ. Νικόλαος -Μηνιατών": "Saint Nicholas of Miniates",
    "Αγ. Νικόλαος- Λειβαθινάδων": "Saint Nicholas of Livathinatoi",
    "Αγ. Παντελεήμων": "Saint Panteleimon",
    "Αγ. Παρασκευή": "Saint Paraskevi",
    "Αγ. Προκόπιος": "Saint Procopius",
    "Αγ. Σοφία": "Saint Sophia",
    "Αγ. Σπυρίδων": "Saint Spyridon",
    "Αγ. Σπυρίδων-Αγ. Ακυλίνα": "Saints Spyridon and Aquilina",
    "Αγ. Στέφανος": "Saint Stephen",
    "Αγ. Τριάς": "the Holy Trinity",
    "Αγ. Χαράλαμπος": "Saint Charalambos",
    "Αγ. Χριστόφορος": "Saint Christopher",
    "Ανάληψις του Κυρίου": "the Ascension of the Lord",
    "Ανάστασις του Κυρίου": "the Resurrection of the Lord",
    "Γενέσ. Θεοτόκου- Αγ. Στέφανος": (
        "the Nativity of the Theotokos and Saint Stephen"
    ),
    "Γενέσιον Αγ. Ιωάννου του Προδρόμου": (
        "the Nativity of Saint John the Forerunner"
    ),
    "Γενέσιον Θεοτόκου": "the Nativity of the Theotokos",
    "Γενέσιον της Θεοτόκου": "the Nativity of the Theotokos",
    "Γενεσ. Αγ. Ιωάννου Προδρόμου": (
        "the Nativity of Saint John the Forerunner"
    ),
    "Εισόδια Θεοτόκου": "the Entrance of the Theotokos",
    "Εισόδια της Θεοτόκου": "the Entrance of the Theotokos",
    "Εισόδια της Θεοτόκου- Σισσιωτίσσης": (
        "the Entrance of the Theotokos at Sissiotissa"
    ),
    "Ευαγγ. Θεοτόκου- Αγ. Παρασκευή": (
        "the Annunciation of the Theotokos and Saint Paraskevi"
    ),
    "Ευαγγελισμός Θεοτόκου": "the Annunciation of the Theotokos",
    "Ευαγγελισμός της Θεοτόκου Μητροπολ. Ναός": (
        "the Annunciation of the Theotokos"
    ),
    "Ζωοδόχος Πηγή": "the Life-Giving Spring",
    "Κοίμησις Θεοτόκου": "the Dormition of the Theotokos",
    "Κοίμησις Θεοτόκου Γραβαλιωτίσσης": (
        "the Dormition of the Theotokos at Gravaliotissa"
    ),
    "Κοίμησις Θεοτόκου- Γαρδελιωτίσσης": (
        "the Dormition of the Theotokos at Gardeliotissa"
    ),
    "Κοίμησις Θεοτόκου- Περλιγκάδων": (
        "the Dormition of the Theotokos of Perlingatoi"
    ),
    "Κοίμοισις Θεοτόκου - Μεσσών": (
        "the Dormition of the Theotokos at Messon"
    ),
    "Μεταμόρφ. Σωτήρος- Παντοκράτορος": (
        "the Transfiguration of the Savior and Pantokrator"
    ),
    "Μεταμόρφωσις Σωτήρος": "the Transfiguration of the Savior",
    "Προφήτης Ηλίας": "Prophet Elijah",
    "Ταξιάρχαι": "the Holy Archangels",
    "Υπ. Θεοτόκου Μυρτιδιωτίσσης": "Panagia Myrtidiotissa",
    "Υπ. Θεοτόκου-Βλαχερνών": "Panagia of Blachernae",
    "Υπαπαντή του Κυρίου": "the Meeting of the Lord",
}

SEAT_OVERRIDES = {
    "Αγ. Δημήτριος": "Agios Dimitrios",
    "Αγ. Ειρήνη": "Agia Irini",
    "Αγ. Θέκλα": "Agia Thekla",
    "Αγ. Νικόλαος": "Agios Nikolaos",
    "Διγαλέτο (Πυργί)": "Digaleto (Pyrgi)",
    "Επανωχώριον": "Epanochori",
    "Καρουσάτα (Αντυπάτα)": "Karousata (Antypata)",
    "Ληξούριον": "Lixouri",
    "Μοναστηράκιον": "Monastiraki",
    "Μπεκατωράτα": "Bekatorata",
    "Νεοχώριον": "Neochori",
    "Νύφιον": "Nyfi",
    "Ξενόπουλον": "Xenopoulo",
    "Ρίφιον": "Rifio",
    "Σπαθίον": "Spathi",
    "Φισκάρδον": "Fiskardo",
    "Χαράκτιον": "Charakti",
}

# Greek label | English name | seat | rank | address field or blank |
# comma-separated exact public phones.
MONASTIC_ROWS = r'''
Ιερά Μονή Υπεραγίας Θεοτόκου Άτρου|Panagia of Atros Monastery|Atros|Monastery|Atros, Kefallinia|26740-72297
Ιερά Μονή Υπεραγίας Θεοτόκου Αγριλίων|Panagia of Agrilia Monastery|Agrilia|Monastery|Agrilia, Kefallinia|26710-22089
Ιερά Μονή Υπεραγίας Θεοτόκου Θεμάτων|Panagia of Themata Monastery|Themata|Monastery|Themata, Kefallinia|26710-61292
Ιερά Μονή Υπεραγίας Θεοτόκου Κηπουραίων|Panagia of Kipouraia Monastery|Kipouraia|Monastery|Kipouraia, Kefallinia|26710-95080
Ιερά Μονή Υπεραγίας Θεοτόκου Σισσίων|Panagia of Sissia Monastery|Sissia|Monastery|Sissia, Kefallinia|26710-31217
Ιερά Μονή Αγίου Γερασίμου Ομαλών|Saint Gerasimos Monastery at Omala|Omala|Monastery|Omala, Kefallinia|26710-86205,26710-86385
Ιερά Μονή Αποστόλου Ανδρέα|Apostle Andrew Monastery|Kefallinia|Monastery||26710-69398
Ιερά Μονή Εσταυρωμένου|Estavromenos Monastery|Kefallinia|Monastery||26710-69143
Ιερά Μονή Υπεραγίας Θεοτόκου Κορωνάτου|Panagia of Koronato Monastery|Koronato|Monastery|Koronato, Kefallinia|26710-94361
Μετόχιο Σπηλαίου Αγίου Γερασίμου στη Λάσση Αργοστολίου|Cave of Saint Gerasimos Metochion in Lassi|Lassi|Metochion|Lassi, Argostoli, Kefallinia|26710-2832
Μετόχιο Αγίας Παρασκευής Λεπέδων|Saint Paraskevi Metochion at Lepeda|Lepeda|Metochion|Lepeda, Kefallinia|26710-91690
Μετόχιο Υπεραγίας Θεοτόκου Παλαιοχέρσου|Panagia Palaiochersou Metochion|Palaiochersos|Metochion|Palaiochersos, Kefallinia|
Μετόχιο Ευαγγελιστρίας Βαρδιάνων|Evangelistria of Vardianoi Metochion|Vardianoi|Metochion|Vardianoi, Kefallinia|
'''

REGION_LIMITS = ((31, "A"), (66, "B"), (77, "C"), (97, "D"),
                 (113, "E"), (140, "ST"), (167, "Z"))
EXPECTED_REGION_COUNTS = {
    "A": 31, "B": 35, "C": 11, "D": 20,
    "E": 16, "ST": 27, "Z": 27,
}
EXPECTED_TOTAL = 180
EXPECTED_RANKS = {
    "Metochion": 4,
    "Metropolitan Cathedral": 1,
    "Monastery": 9,
    "Parish Church": 166,
}
EXPECTED_KINDS = {"monastery": 13, "parish": 167}
EXPECTED_PHONE_BODIES = 11
EXPECTED_PHONE_VALUES = 12
EXPECTED_ADDRESS_BODIES = 178


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


GREEK = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}


def transliterate(value):
    if value in SEAT_OVERRIDES:
        return SEAT_OVERRIDES[value]
    value = unicase(value)
    for source, target in (
        ("γγ", "ng"), ("γκ", "gk"), ("μπ", "mp"),
        ("ντ", "nt"), ("ου", "ou"), ("αι", "ai"),
        ("ει", "ei"), ("οι", "oi"), ("τσ", "ts"),
        ("τζ", "tz"),
    ):
        value = value.replace(source, target)
    value = "".join(GREEK.get(char, char) for char in value)
    return re.sub(r"\s+", " ", value).strip().title()


def parse_table(raw, width, label):
    result = []
    for number, line in enumerate(raw.strip().splitlines(), 1):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != width:
            raise ValueError(
                "%s row %d has %d fields" % (label, number, len(parts))
            )
        result.append(parts)
    return result


PARISH_PARSED = parse_table(PARISH_ROWS, 2, "parish")
MONASTIC_PARSED = parse_table(MONASTIC_ROWS, 6, "monastic")
DEDICATIONS = {unicase(key): value for key, value in DEDICATIONS.items()}


def region_for(number):
    for limit, region in REGION_LIMITS:
        if number <= limit:
            return region
    raise ValueError("parish row exceeds legal region limits")


def build_rows():
    if len(PARISH_PARSED) != 167:
        raise ValueError("legal parish transcription must contain 167 rows")
    rows = []
    regions = Counter()
    for number, (seat_local, dedication_local) in enumerate(
            PARISH_PARSED, 1):
        dedication = DEDICATIONS.get(unicase(dedication_local))
        if not dedication:
            raise ValueError(
                "missing English dedication for parish row %d" % number
            )
        seat = transliterate(seat_local)
        rank = "Metropolitan Cathedral" if number == 1 else "Parish Church"
        prefix = "Metropolitan Cathedral of" if number == 1 else \
            "Parish Church of"
        regions[region_for(number)] += 1
        rows.append({
            "id": "gr-kefallinia-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s %s in %s" % (prefix, dedication, seat),
            "local": "%s, %s" % (dedication_local, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat, "Kefallinia", "Greece"],
            "sources": [LEGAL_PDF, AMENDMENT_PDF],
            "checked": CHECKED,
        })
    if dict(regions) != EXPECTED_REGION_COUNTS:
        raise ValueError("legal parish region counts drifted: %r" % regions)

    for local, name, seat, rank, address, phone_text in MONASTIC_PARSED:
        number = len(rows) + 1
        row = {
            "id": "gr-kefallinia-%03d" % number,
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "sources": [OFFICIAL_PROFILE],
            "checked": CHECKED,
        }
        if address:
            row["address"] = [address, "Greece"]
        if phone_text:
            row["phones"] = phone_text.split(",")
            row["contact_sources"] = [OFFICIAL_PROFILE]
            row["contact_checked"] = CHECKED
        rows.append(row)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}


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
        raise ValueError("Kefallinia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kefallinia candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "regulated_parish_rows": 167,
        "current_calendar_reported_parishes": 164,
        "unresolved_parish_aggregate_difference": 3,
        "current_monastery_rows": 9,
        "current_metochion_rows": 4,
        "regulated_pilgrimage_rows": 0,
        "parish_kind_rows": 167,
        "monastery_kind_rows": 13,
        "contact_bodies": EXPECTED_PHONE_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Kefallinia ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Kefallinia ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kefallinia ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    malformed_phones = []
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
            item.get("phones") or item.get("emails") or item.get("site")
        )
        if has_contact:
            if not contact_sources or item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            for phone in item.get("phones") or []:
                if not re.fullmatch(r"\d{5}-\d{4,5}", phone):
                    raise ValueError("%s carries an invalid phone" % row_id)
                if len(re.sub(r"\D", "", phone)) == 9:
                    malformed_phones.append((row_id, phone))
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
    if malformed_phones != [("gr-kefallinia-177", "26710-2832")]:
        raise ValueError("unexpected malformed official phone values")
    if len(result) != EXPECTED_TOTAL:
        raise ValueError(
            "expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result))
        )
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Kefallinia English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Kefallinia rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Kefallinia kind totals drifted: %r" % dict(kinds))
    phone_bodies = sum(bool(item.get("phones")) for item in result)
    phone_values = sum(len(item.get("phones") or []) for item in result)
    address_bodies = sum(bool(item.get("address")) for item in result)
    if (phone_bodies, phone_values) != (
            EXPECTED_PHONE_BODIES, EXPECTED_PHONE_VALUES):
        raise ValueError("Kefallinia contact coverage drifted")
    if address_bodies != EXPECTED_ADDRESS_BODIES:
        raise ValueError("Kefallinia address coverage drifted")
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
    if url in {LEGAL_PDF, AMENDMENT_PDF, CALENDAR_REPORT}:
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=90) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return unicase(" ".join(text.split()))


def check_live():
    profile_markers = {
        "Ανδρικές μονές",
        "Υπεραγίας Θεοτόκου Άτρου",
        "Υπεραγίας Θεοτόκου Αγριλίων",
        "Υπεραγίας Θεοτόκου Θεμάτων",
        "Υπεραγίας Θεοτόκου Κηπουραίων",
        "Υπεραγίας Θεοτόκου Σισσίων",
        "Αγ. Γερασίμου Ομαλών",
        "Απόστολου Ανδρέα",
        "Εσταυρωμένου",
        "Υπ. Θεοτόκου Κορωνάτου",
        "Σπηλαίου Αγ. Γερασίμου στη Λάσση Αργοστολίου",
        "Αγ. Παρασκευής Λεπέδων",
        "Υπεραγίας Θεοτόκου Παλαιοχέρσου",
        "Ευαγγελιστρίας Βαρδιάνων",
        "26740-72297",
        "26710-86205",
        "86385",
        "26710-2832",
        "26710-91690",
    }
    checks = {
        LEGAL_PDF: ("pdf", set()),
        AMENDMENT_PDF: ("pdf", set()),
        CALENDAR_REPORT: ("pdf", set()),
        OFFICIAL_PROFILE: ("html", profile_markers),
        SAINT_GERASIMOS_SITE_LEAD: ("html", {"Μονή", "Ομαλών"}),
    }

    def one(item):
        url, (expected_type, markers) = item
        payload, content_type = fetch(url)
        if expected_type == "pdf":
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("Kefallinia source is not a PDF: %s" % url)
            return url
        if "html" not in content_type:
            raise ValueError("non-HTML Kefallinia source: %s" % url)
        page = normalized_page(payload)
        missing = [
            marker for marker in markers
            if unicase(" ".join(marker.split())) not in page
        ]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        return url

    with ThreadPoolExecutor(max_workers=5) as executor:
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
            print(
                "Kefallinia live checks passed for %d source pages" % checked
            )
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Kefallinia checks passed: %d bodies, %d phone bodies, "
                "%d public phone values" % (
                    len(rows),
                    sum(bool(item.get("phones")) for item in rows),
                    sum(len(item.get("phones") or []) for item in rows),
                )
            )
    except Exception as exc:
        print("Kefallinia check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
