#!/usr/bin/env python3
"""Validate exact current Nikopolis and Preveza bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_nikopolis_country.py --check
    python tools/directory_nikopolis_country.py --check-live
    python tools/directory_nikopolis_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "nikopolis_country.json"
)
PARENT = "ep-nikopolis"
METROPOLIS_HOME = "https://www.imnp.gr/"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-nikopoleos-prevezis/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/nikopoleos-kai-prebezes"
)
LEGAL_PAGE = (
    "https://www.e-nomothesia.gr/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-ekklesias-388-642-2019.html"
)
LEGAL_PDF = (
    "https://ia37rg02wpsa01.blob.core.windows.net/fek/02/2019/"
    "20190201436.pdf"
)
PROPHET_ELIJAH_SITE = "https://impiprevezis.gr/"
SAINT_VISSARION_SITE = "https://agios-vissarionas.gr/"
ZALONGO_CONTACT_PDF = (
    "https://www.culture.gov.gr/DocLib/"
    "%CE%91%CE%A0%CE%9F%CE%A6%CE%91%CE%A3%CE%97%20%CE%99_%20"
    "%CE%9C_%20%CE%96%CE%B1%CE%9B%CE%9F%CE%93%CE%93%CE%9F%CE%A5.pdf"
)


# English seat | English dedication | Greek seat | Greek dedication
#
# These 131 rows reproduce the exact parish bodies in Regulation 388/642/2019
# and reconcile to the current Patriarchate aggregate of 131 parish churches.
PARISH_ROWS = r'''
Preveza|Saint Catherine|Πρέβεζα|Αγία Αικατερίνη
Preveza|Saint Anna|Πρέβεζα|Αγία Άννα
Preveza|Saint Basil|Πρέβεζα|Άγιος Βασίλειος
Preveza|Saint Irene of Elaion|Πρέβεζα|Αγία Ειρήνη Ελαιώνος
Preveza|Saint John Chrysostom|Πρέβεζα|Άγιος Ιωάννης Χρυσόστομος
Preveza|Saints Constantine and Helen|Πρέβεζα|Άγιοι Κωνσταντίνος και Ελένη
Preveza|Saint Nectarios|Πρέβεζα|Άγιος Νεκτάριος
Preveza|Saint Nicholas|Πρέβεζα|Άγιος Νικόλαος
Preveza|Dormition of the Theotokos|Πρέβεζα|Κοίμηση της Θεοτόκου
Preveza|Saint Charalambos|Πρέβεζα|Άγιος Χαράλαμπος
Preveza|Transfiguration of the Savior Pantokrator|Πρέβεζα|Μεταμόρφωση του Σωτήρος Παντοκράτορος
Agios Thomas|Saint Thomas|Άγιος Θωμάς|Άγιος Θωμάς
Agia Triada Neochoriou|Holy Trinity|Αγία Τριάδα Νεοχωρίου|Αγία Τριάδα
Michalitsi|Dormition of the Theotokos|Μιχαλίτσι|Κοίμηση της Θεοτόκου
Mytikas|Holy Archangels|Μύτικας|Παμμέγιστοι Ταξιάρχες
Nikopolis|Holy Apostle Paul|Νικόπολη|Άγιος Απόστολος Παύλος
Flampoura|Saints Constantine and Helen|Φλάμπουρα|Άγιοι Κωνσταντίνος και Ελένη
Aedonia|Saint John|Αηδόνια|Άγιος Ιωάννης
Ammoudia|Dormition of the Theotokos|Αμμουδιά|Κοίμηση της Θεοτόκου
Ano Despotiko|Saint Paraskevi|Άνω Δεσποτικό|Αγία Παρασκευή
Ano Skafidoti|Nativity of the Theotokos|Άνω Σκαφιδωτή|Γέννηση της Θεοτόκου
Archangelos|Saint Athanasius|Αρχάγγελος|Άγιος Αθανάσιος
Valanidorrachi|Saint Athanasius|Βαλανιδορράχη|Άγιος Αθανάσιος
Valanidoussa|Saint Marina|Βαλανιδούσσα|Αγία Μαρίνα
Vrachos|Saint Kyriake|Βράχος|Αγία Κυριακή
Ekklisies|Saint Nicholas|Εκκλησιές|Άγιος Νικόλαος
Kamarina|Saint Basil|Καμαρίνα|Άγιος Βασίλειος
Kanali|Saint Paraskevi|Κανάλι|Αγία Παρασκευή
Kastrosykia|Saint George|Καστροσυκιά|Άγιος Γεώργιος
Kato Despotiko|Saint George|Κάτω Δεσποτικό|Άγιος Γεώργιος
Kato Skafidoti|Holy Trinity|Κάτω Σκαφιδωτή|Αγία Τριάδα
Koryfoula|Saint George|Κορυφούλα|Άγιος Γεώργιος
Koukoulio|Holy Apostles|Κουκούλιο|Άγιοι Απόστολοι
Kryopigi|Saint Blaise|Κρυοπηγή|Άγιος Βλάσιος
Loutsa|Saint George|Λούτσα|Άγιος Γεώργιος
Lygia|Saint Thomas|Λυγιά|Άγιος Θωμάς
Megadendro|Saint Constantine|Μεγάδενδρο|Άγιος Κωνσταντίνος
Myrsini|Nativity of the Theotokos|Μυρσίνη|Γέννηση της Θεοτόκου
Nea Sampsous|Holy Trinity|Νέα Σαμψούς|Αγία Τριάδα
Nea Sinope|Saint Nicholas|Νέα Σινώπη|Άγιος Νικόλαος
Riza|Holy Unmercenaries|Ριζά|Άγιοι Ανάργυροι
Skepasto|Saint George|Σκεπαστό|Άγιος Γεώργιος
Tsouknida|Saint George|Τσουκνίδα|Άγιος Γεώργιος
Chimadio|Saint Nicholas|Χειμαδιό|Άγιος Νικόλαος
Chochla|Saint Constantine|Χόχλα|Άγιος Κωνσταντίνος
Agia Paraskevi|Saint Paraskevi|Αγία Παρασκευή|Αγία Παρασκευή
Akropotamia|Dormition of the Theotokos|Ακροποταμιά|Κοίμηση της Θεοτόκου
Aneza|Saint Nicholas|Ανέζα|Άγιος Νικόλαος
Anthotopos|Life-Giving Spring|Ανθότοπος|Ζωοδόχος Πηγή
Apomero|Saint Kyriake|Απόμερο|Αγία Κυριακή
Vigla|Saint Nicholas|Βίγλα|Άγιος Νικόλαος
Vlacherna|Deposition of the Precious Robe of the Theotokos|Βλαχέρνα|Κατάθεση της Τιμίας Εσθήτος της Θεοτόκου
Gavria|Dormition of the Theotokos|Γαβριά|Κοίμηση της Θεοτόκου
Grammenitsa|Saint Demetrius|Γραμμενίτσα|Άγιος Δημήτριος
Grimpovo|Saint Athanasius|Γρίμποβο|Άγιος Αθανάσιος
Dryon|Holy Apostles|Δρυών|Άγιοι Απόστολοι
Eleousa|Dormition of the Theotokos|Ελεούσα|Κοίμηση της Θεοτόκου
Kalovatos|Nativity of the Theotokos|Καλοβάτος|Γέννηση της Θεοτόκου
Kalovatos|Saint Panteleimon|Καλοβάτος|Άγιος Παντελεήμων
Kalogeriko|Saint Paraskevi|Καλογερικό|Αγία Παρασκευή
Keramatai|Holy Trinity|Κεραμάτες|Αγία Τριάδα
Kirkizatai|Saint Nicholas|Κιρκιζάτες|Άγιος Νικόλαος
Kolomodia|Nativity of the Theotokos|Κολομόδια|Γέννηση της Θεοτόκου
Korfovouni|Saint George|Κορφοβούνι|Άγιος Γεώργιος
Koronisia|Nativity of the Theotokos|Κορωνησία|Γέννηση της Θεοτόκου
Kostakioi|Saint George|Κωστακιοί|Άγιος Γεώργιος
Mytikas, Arta|Saint Paraskevi|Μύτικας Άρτας|Αγία Παρασκευή
Neochori|Saint Demetrius|Νεοχώρι|Άγιος Δημήτριος
Pachykalamos|Nativity of the Theotokos|Παχύκαλαμος|Γέννηση της Θεοτόκου
Pistiana|Nativity of the Theotokos|Πιστιανά|Γέννηση της Θεοτόκου
Plisioi|Saint Demetrius|Πλησιοί|Άγιος Δημήτριος
Polydroso|Saint Athanasius|Πολύδροσο|Άγιος Αθανάσιος
Rachi|Saint George|Ράχη|Άγιος Γεώργιος
Rokka|Saint Nicholas|Ρόκκα|Άγιος Νικόλαος
Filothei, Chalkiades|Saints Constantine and Helen|Φιλοθέη Χαλκιάδων|Άγιοι Κωνσταντίνος και Ελένη
Kalamia|Life-Giving Spring, Panagia Hodegetria|Καλαμιά|Ζωοδόχος Πηγή, Παναγία Οδηγήτρια
Chanopoulo|Nativity of the Theotokos|Χανόπουλο|Γέννηση της Θεοτόκου
Psathotopi|Saint Blaise|Ψαθοτόπι|Άγιος Βλάσιος
Ano Kotsanopoulo|Saint Paraskevi|Άνω Κοτσανόπουλο|Αγία Παρασκευή
Ano Rachi|Nativity of Saint John the Forerunner|Άνω Ράχη|Γέννηση του Τιμίου Προδρόμου
Ano Revmatia|Saint George|Άνω Ρευματιά|Άγιος Γεώργιος
Assos|Saint George|Άσσος|Άγιος Γεώργιος
Vrysoula|Dormition of the Theotokos|Βρυσούλα|Κοίμηση της Θεοτόκου
Galatas|Dormition of the Theotokos|Γαλατάς|Κοίμηση της Θεοτόκου
Galini|Saint George|Γαλήνη|Άγιος Γεώργιος
Elaia|Saint Athanasius|Ελαία|Άγιος Αθανάσιος
Zervo|Saint Demetrius|Ζερβό|Άγιος Δημήτριος
Thesprotiko|Saint George|Θεσπρωτικό|Άγιος Γεώργιος
Thesprotiko|Nativity of the Theotokos|Θεσπρωτικό|Γέννηση της Θεοτόκου
Kato Kotsanopoulo|Saint George|Κάτω Κοτσανόπουλο|Άγιος Γεώργιος
Kato Revmatia|Dormition of the Theotokos|Κάτω Ρευματιά|Κοίμηση της Θεοτόκου
Kerasovo|Saint Constantine|Κεράσοβο|Άγιος Κωνσταντίνος
Kranea|Saint Demetrius|Κρανέα|Άγιος Δημήτριος
Louros|Dormition of the Theotokos|Λούρος|Κοίμηση της Θεοτόκου
Meliana|Dormition of the Theotokos|Μελιανά|Κοίμηση της Θεοτόκου
Nikolitsi|Dormition of the Theotokos|Νικολίτσι|Κοίμηση της Θεοτόκου
Papadatai|Holy Trinity, Faneromeni|Παπαδάτες|Αγία Τριάδα, Φανερωμένη
Polyvryso|Saint Panteleimon|Πολύβρυσο|Άγιος Παντελεήμων
Rizovouni|Saint Nicholas|Ριζοβούνι|Άγιος Νικόλαος
Seriziana|Dormition of the Theotokos|Σερίζιανα|Κοίμηση της Θεοτόκου
Skiadas|Saint Paraskevi|Σκιαδάς|Αγία Παρασκευή
Stefani|Saint Athanasius|Στεφάνη|Άγιος Αθανάσιος
Neo Sfinoto|Saint Nicholas|Νέο Σφηνωτό|Άγιος Νικόλαος
Trikastro|Dormition of the Theotokos|Τρίκαστρο|Κοίμηση της Θεοτόκου
Tyrgia|Life-Giving Spring|Τυργιά|Ζωοδόχος Πηγή
Oropos|Saint Demetrius|Ωρωπός|Άγιος Δημήτριος
Agios Georgios|Saint George|Άγιος Γεώργιος|Άγιος Γεώργιος
Agios Spyridon|Saint Spyridon|Άγιος Σπυρίδων|Άγιος Σπυρίδων
Ampelia, Arta|Saint Paraskevi|Αμπέλια Άρτας|Αγία Παρασκευή
Ammotopos|Saint George|Αμμότοπος|Άγιος Γεώργιος
Ano Drymon and Drymon|Saint Christopher|Άνω Δρυμών και Δρυμών|Άγιος Χριστόφορος
Vathy Gorgomylou|Holy Archangels|Βαθύ Γοργομύλου|Παμμέγιστοι Ταξιάρχες
Voulista|Saint George|Βούλιστα|Άγιος Γεώργιος
Gorgomylos|Saint George|Γοργόμυλος|Άγιος Γεώργιος
Gymnotopos|Saint Kyriake|Γυμνότοπος|Αγία Κυριακή
Dryofyto|Saint Nicholas|Δρυόφυτο|Άγιος Νικόλαος
Iliovounia|Saint Constantine|Ηλιοβούνια|Άγιος Κωνσταντίνος
Kampi|Saints Constantine and Helen|Καμπή|Άγιοι Κωνσταντίνος και Ελένη
Kerasona|Holy Apostle Paul|Κερασώνα|Άγιος Απόστολος Παύλος
Nea Kerasous|Transfiguration of the Savior|Νέα Κερασούς|Μεταμόρφωση του Σωτήρος
Neos Gorgomylos|Life-Giving Spring|Νέος Γοργόμυλος|Ζωοδόχος Πηγή
Pantanassa|Dormition of the Theotokos|Παντάνασσα|Κοίμηση της Θεοτόκου
Panagia|Dormition of the Theotokos|Παναγία|Κοίμηση της Θεοτόκου
Petra|Saint Kyriake|Πέτρα|Αγία Κυριακή
Rodavgi|Saint Paraskevi|Ροδαυγή|Αγία Παρασκευή
Romia|Saint John|Ρωμιά|Άγιος Ιωάννης
Soumesi|Holy Trinity|Σουμέσι|Αγία Τριάδα
Strongyli|Saint Catherine|Στρογγυλή|Αγία Αικατερίνη
Tsagkaropoulo|Saint Nicholas|Τσαγκαρόπουλο|Άγιος Νικόλαος
Philippiada|Saint Vissarion|Φιλιππιάδα|Άγιος Βησσαρίων
Philippiada|Dormition of the Theotokos|Φιλιππιάδα|Κοίμηση της Θεοτόκου
'''


# English seat | English dedication | Greek seat | Greek local name
PILGRIMAGE_ROWS = r'''
Kanali|Panagia Kanaliotissa|Κανάλι|Ιερό Προσκύνημα Παναγίας Καναλιώτισσας
Preveza|Saint Paraskevi|Πρέβεζα|Ιερό Προσκύνημα Αγίας Παρασκευής
Lithari|Holy Apostle Paul|Λιθάρι|Ιερό Προσκύνημα Αγίου Αποστόλου Παύλου
'''


# English seat | English dedication | Greek seat | Greek local name |
# phones | emails | body-owned site
MONASTIC_ROWS = r'''
Iliovounia|Prophet Elijah|Ηλιοβούνια|Ιερά Μονή Προφήτου Ηλιού Ηλιοβουνίων|2682051161,2682051172,2682052144||https://impiprevezis.gr/
Lekatsa|Holy Trinity|Λεκατσά|Ιερά Μονή Αγίας Τριάδος Λεκατσά|2682100353||
Zalongo|Saint Demetrius|Ζάλογγο|Ιερά Μονή Αγίου Δημητρίου Ζαλόγγου|2682051320|agdimzal@gmail.com|
Kerasona|Panagia Faneromeni|Κερασώνα|Ιερά Μονή Παναγίας Φανερωμένης Κερασώνος|2683091294||
'''


# English seat | English dedication | Greek seat | Greek local name | rank |
# exact current first-party source
OTHER_CURRENT_ROWS = r'''
Archangelos|Saint Marina|Αρχάγγελος|Ιερό Παρεκκλήσιο Αγίας Μαρίνας Αρχαγγέλου|Chapel|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b5%ce%b3%ce%ba%ce%b1%ce%b9%ce%bd%ce%b9%ce%b1-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%b1%cf%82-%ce%bc%ce%b1%cf%81%ce%b9%ce%bd%ce%b7%cf%82/
Polydroso|Saints Vissarion and John Chrysostom|Πολύδροσο|Κοιμητηριακό Ιερό Παρεκκλήσιο Αγίων Βησσαρίωνος και Ιωάννου του Χρυσοστόμου|Cemetery Chapel|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%b9%ce%be%ce%b9%ce%b1%ce%ba%ce%bf%ce%b9%ce%bc%ce%b7%cf%84%ce%b7%cf%81%ce%b9%ce%b1%ce%ba%ce%bf%cf%85-%ce%b9%ce%b5%cf%81%ce%bf%cf%85-%cf%80%ce%b1%cf%81%ce%b5%ce%ba/
Margarona|Nativity of the Theotokos|Μαργαρώνα|Ιερό Παρεκκλήσιο Γενεσίου της Θεοτόκου Μαργαρώνας|Chapel|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b5%ce%bf%cf%81%cf%84%ce%b1%ce%b6%ce%b5%ce%b9-%cf%84%ce%bf-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf-%cf%84%ce%b7%cf%83-%ce%bc%ce%b1%cf%81%ce%b3%ce%b1%cf%81%cf%89%ce%bd/
Psathotopi|Saint Nectarios|Ψαθοτόπι|Ιερό Παρεκκλήσιο Αγίου Νεκταρίου Ψαθοτοπίου|Chapel|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%b9%ce%be%ce%b9%ce%b1-%ce%b9%ce%b5%cf%81%ce%bf%cf%85-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85/
Ekklisies|Saint Theodore Stratelates|Εκκλησιές|Ιερό Παρεκκλήσιο Αγίου Θεοδώρου του Στρατηλάτου Εκκλησιών|Chapel|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b5%ce%b3%ce%ba%ce%b1%ce%b9%ce%bd%ce%b9%ce%b1-%ce%b9%ce%b5%cf%81%ce%bf%cf%85-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%ce%ba%ce%bb%ce%b7%cf%83%ce%b9%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b5%ce%bd/
Elaion Workers Housing, Preveza|Saint Demetrius the Myrrh-streamer|Εργατικές Κατοικίες Ελαιώνος Πρεβέζης|Ιερός Ναός Αγίου Δημητρίου του Μυροβλήτου|Church|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%b9%ce%be%ce%b9%ce%b1-%ce%b9-%ce%bd%ce%b1%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b4%ce%b7%ce%bc%ce%b7%cf%84%cf%81%ce%b9%ce%bf%cf%85-%cf%84%ce%bf%cf%85/
Filothei, Chalkiades|Saint Kosmas of Aetolia|Φιλοθέη Χαλκιάδων|Κοιμητηριακό Ιερό Παρεκκλήσιο Αγίου Κοσμά του Αιτωλού|Cemetery Chapel|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b5%ce%b3%ce%ba%ce%b1%ce%b9%ce%bd%ce%b9%ce%b1-%ce%ba%ce%bf%ce%b9%ce%bc%ce%b7%cf%84%ce%b7%cf%81%ce%b9%ce%b1%ce%ba%ce%bf%cf%85-%ce%b9%ce%b5%cf%81%ce%bf%cf%85-%ce%bd%ce%b1%ce%bf%cf%85-%ce%b1%ce%b3/
Kato Kotsanopoulo|Saint Nectarios|Κάτω Κοτσανόπουλο|Ιερός Ναός Αγίου Νεκταρίου Κάτω Κοτσανόπουλου|Church|https://www.imnp.gr/%ce%bd%ce%ad%ce%b1/%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%b9%ce%be%ce%b9%ce%b1-%ce%b9%ce%b5%cf%81%ce%bf%cf%85-%ce%bd%ce%b1%ce%bf%cf%85-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%bd%ce%b5%ce%ba%cf%84%ce%b1%cf%81%ce%b9%ce%bf/
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


def build_rows():
    rows = []
    parish_rows = parse_table(PARISH_ROWS, 4, "parish")
    if len(parish_rows) != 131:
        raise ValueError("legal parish source must contain exactly 131 rows")
    for seat, dedication, seat_local, dedication_local in parish_rows:
        rank = "Cathedral" if (
            seat == "Preveza" and dedication == "Saint Charalambos"
        ) else "Parish Church"
        name = make_name(dedication, rank, seat)
        local_rank = "Μητροπολιτικός Ιερός Ναός" if rank == "Cathedral" \
            else "Ιερός Ναός"
        item = {
            "id": "gr-ep-nikopolis-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s %s %s" % (local_rank, dedication_local, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": [LEGAL_PAGE, LEGAL_PDF, PATRIARCHATE_PAGE],
        }
        if seat == "Philippiada" and dedication == "Saint Vissarion":
            item["site"] = SAINT_VISSARION_SITE
            item["sources"] = [LEGAL_PAGE, LEGAL_PDF, SAINT_VISSARION_SITE]
        rows.append(item)

    for seat, dedication, seat_local, local in parse_table(
            PILGRIMAGE_ROWS, 4, "pilgrimage"):
        name = make_name(dedication, "Pilgrimage Church", seat)
        sources = [PATRIARCHATE_PAGE]
        if seat != "Lithari":
            sources = [LEGAL_PAGE, LEGAL_PDF]
        rows.append({
            "id": "gr-ep-nikopolis-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": sources,
        })

    for fields in parse_table(MONASTIC_ROWS, 7, "monastery"):
        seat, dedication, seat_local, local, raw_phones, raw_emails, site = fields
        name = make_name(dedication, "Monastery", seat)
        sources = [PATRIARCHATE_PAGE]
        contact_sources = [PATRIARCHATE_PAGE]
        if site:
            sources.append(site)
            contact_sources.append(site)
        if raw_emails:
            sources.append(ZALONGO_CONTACT_PDF)
            contact_sources.append(ZALONGO_CONTACT_PDF)
        item = {
            "id": "gr-ep-nikopolis-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "phones": [phone(value) for value in raw_phones.split(",")],
            "sources": sources,
            "contact_sources": contact_sources,
            "contact_checked": CHECKED,
        }
        if raw_emails:
            item["emails"] = raw_emails.split(",")
        if site:
            item["site"] = site
        if seat == "Iliovounia":
            item["address"] = ["P.O. Box 138", "48100 Preveza"]
        rows.append(item)

    for seat, dedication, seat_local, local, rank, source in parse_table(
            OTHER_CURRENT_ROWS, 6, "other current body"):
        name = make_name(dedication, rank, seat)
        rows.append({
            "id": "gr-ep-nikopolis-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": [source],
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 146
EXPECTED_OWNER_COUNTS = {PARENT: 146}
EXPECTED_KINDS = {"monastery": 4, "parish": 142}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Chapel": 2,
    "Chapel": 4,
    "Church": 2,
    "Monastery": 4,
    "Parish Church": 130,
    "Pilgrimage Church": 3,
}
EXPECTED_CONTACT_BODIES = 5
EXPECTED_PHONE_BODIES = 4
EXPECTED_PHONE_VALUES = 6
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 2
EXPECTED_ADDRESS_BODIES = 146
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
        "www.imnp.gr", "imnp.gr",
        "ec-patr.org", "www.ec-patr.org",
        "www.ecclesiagreece.gr", "ecclesiagreece.gr",
        "www.e-nomothesia.gr", "e-nomothesia.gr",
        "ia37rg02wpsa01.blob.core.windows.net",
        "impiprevezis.gr", "www.impiprevezis.gr",
        "agios-vissarionas.gr", "www.agios-vissarionas.gr",
        "www.culture.gov.gr", "culture.gov.gr",
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
        raise ValueError("Nikopolis candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Nikopolis candidate ledger date drifted")
    expected_summary = {
        PARENT: 146,
        "total": 146,
        "exact_current_parishes": 131,
        "exact_current_pilgrimage_churches": 3,
        "exact_current_monasteries": 4,
        "exact_current_other_churches_and_chapels": 8,
        "parish_kind_rows": 142,
        "monastery_kind_rows": 4,
        "contact_bodies": 5,
        "phone_bodies": 4,
        "public_phone_values": 6,
        "email_bodies": 1,
        "public_email_values": 1,
        "official_detail_sites": 2,
        "address_bodies": 146,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Nikopolis candidate ledger summary drifted")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 5:
        raise ValueError("Nikopolis candidate ledger lacks held leads")


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
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing Nikopolis row id")
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s lacks the GR country code" % row_id)
        for field in ("kind", "rank", "name", "local", "seat"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
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
        raise ValueError("Nikopolis English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Nikopolis English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Nikopolis parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Nikopolis kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Nikopolis rank totals drifted: %r" %
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
        raise ValueError("Nikopolis contact coverage drifted: %r" %
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


OTHER_CURRENT_PARSED = parse_table(
    OTHER_CURRENT_ROWS, 6, "other current body"
)
LIVE_MARKERS_BY_SEAT = {
    "Archangelos": ("Μαρίνης Αρχαγγέλου Πρεβέζης", "Εγκαίνια"),
    "Polydroso": ("Αγίων Βησσαρίωνος", "Πολύδροσο Άρτας"),
    "Margarona": ("ΓΕΝΕΣΙΟΥ ΤΗΣ ΘΕΟΤΟΚΟΥ", "ΜΑΡΓΑΡΩΝΑΣ"),
    "Psathotopi": ("Αγίου Νεκταρίου", "Ψαθοτόπι Άρτης"),
    "Ekklisies": ("Θεοδώρου του Στρατηλάτου", "Εκκλησιών Πρεβέζης"),
    "Elaion Workers Housing, Preveza": (
        "Αγίου Δημητρίου του Μυροβλήτου", "Ελαιώνος Πρεβέζης"
    ),
    "Filothei, Chalkiades": (
        "Αγίου Κοσμά του Αιτωλού", "Φιλοθέη (Χαλκιάδες) Άρτας"
    ),
    "Kato Kotsanopoulo": (
        "Αγίου Νεκταρίου", "Κάτω Κοτσανόπουλου Λούρου"
    ),
}
LIVE_POST_MARKERS = {
    row[5]: LIVE_MARKERS_BY_SEAT[row[0]] for row in OTHER_CURRENT_PARSED
}


def check_post(pair):
    url, markers = pair
    assert_html_markers(url, markers, "current body post")
    return url


def check_live_sources():
    assert_html_markers(
        METROPOLIS_HOME,
        ("ΙΕΡΑ ΜΗΤΡΟΠΟΛΙΣ ΝΙΚΟΠΟΛΕΩΣ", "Ανακοινώσεις"),
        "Metropolis home",
    )
    assert_html_markers(
        PATRIARCHATE_PAGE,
        (
            "Ἐνοριακοί Ναοί 131",
            "Προφ. Ἠλιού Ἠλιοβουνίων",
            "Ἁγίας Τριάδος Λεκατσᾶ",
            "Ἁγ. Δημητρίου Ζαλόγγου",
            "Παναγίας Φανερωμένης Κερασῶνος",
            "προσκύνημα Ἁγίου Παύλου",
        ),
        "Patriarchate profile",
    )
    assert_html_markers(
        CHURCH_OF_GREECE_PAGE,
        (
            "Προφήτου Ηλιού, Ηλιοβουνίων",
            "Αγίας Τριάδος Λεκατσά",
            "Αγ. Δημητρίου Ζαλόγγου",
            "Αγίας Τριάδος Παπαδάτων",
        ),
        "Church of Greece profile",
    )
    assert_html_markers(
        LEGAL_PAGE,
        (
            "388/642/2019",
            "ΦΕΚ 1436/Β/24-4-2019",
            "ΙΕΡΑΣ ΜΗΤΡΟΠΟΛΕΩΣ ΝΙΚΟΠΟΛΕΩΣ ΚΑΙ ΠΡΕΒΕΖΗΣ",
        ),
        "legal roster page",
    )
    content_type, payload, unused = fetch_source(LEGAL_PDF)
    if not payload.startswith(b"%PDF"):
        raise ValueError("official legal roster is not a valid PDF")
    if len(payload) < 100000:
        raise ValueError("official legal roster PDF is unexpectedly small")
    assert_html_markers(
        PROPHET_ELIJAH_SITE,
        ("ΙΕΡΑ ΜΟΝΗ ΠΡΟΦΗΤΟΥ ΗΛΙΟΥ", "26820-51161", "51172", "52144"),
        "Prophet Elijah body site",
    )
    assert_html_markers(
        SAINT_VISSARION_SITE,
        ("Ενορίας Αγίου Βησσαρίωνος Φιλιππιάδος", "Επικοινωνία"),
        "Saint Vissarion body site",
    )
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(check_post, LIVE_POST_MARKERS.items()))


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
            "Nikopolis: %d exact current bodies; %d carry public "
            "body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Nikopolis: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
