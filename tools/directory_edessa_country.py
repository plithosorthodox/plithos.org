#!/usr/bin/env python3
"""Validate exact named Edessa and Pella bodies from official sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_edessa_country.py --check
    python tools/directory_edessa_country.py --dump
    python tools/directory_edessa_country.py --check-live
"""

import argparse
from collections import Counter
import html
from html.parser import HTMLParser
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
    ROOT / "tools" / "directory_candidates" / "edessa_country.json"
)
PARENT = "ep-edessa"
PARENT_SITE = "https://www.imepa.gr/"
STATISTICS_PAGE = (
    "https://www.imepa.gr/"
    "sigmataualphatauiotasigmatauiotakappa940.html"
)
MONASTERY_PAGE = "https://www.imepa.gr/muomicronnuepsilonsigma.html"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-edessis-pellis/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/edesses-pelles-kai-almopias"
)
CATHEDRAL_PAGE = (
    "https://www.parembasis.gr/index.php/el/menu-teyxos-363/"
    "8792-2026-363-03"
)


SOURCE_GROUPS = [
    {
        "key": "edessa",
        "url": "https://www.imepa.gr/7960delta941sigmasigmaetasigmaf.html",
        "rows": r'''
Edessa|Ἔδεσσα|Ἁγ. Σκέπη|Holy Protection|58200|Metropolitan Cathedral
Edessa|Ἔδεσσα|Ἅγ. Δημήτριος|Saint Demetrius|58200|Parish Church
Edessa|Ἔδεσσα|Ἅγ. Νεκτάριος|Saint Nectarios|58200|Parish Church
Edessa|Ἔδεσσα|Ἅγιοι Πάντες|All Saints|58200|Parish Church
Agia Fotini|Ἁγία Φωτεινή|Ἅγ. Νικόλαος|Saint Nicholas|58200|Parish Church
Agras|Ἄγρας|Ἅγ. Δημήτριος|Saint Demetrius|58200|Parish Church
Arnissa|Ἄρνισσα|Ἁγ. Τριάς|Holy Trinity|58002|Parish Church
Vrytta|Βρυττά|Εἰσ. Θεοτόκου|Entry of the Theotokos|58200|Parish Church
Drosia|Δροσιά|Ἅγ. Νικόλαος|Saint Nicholas|58200|Parish Church
Ekklisiochorion|Ἐκκλησιοχώριον|Τίμ. Πρόδρομος|Holy Forerunner|58200|Parish Church
Kaisariana|Καισαριανά|Ἅγ. Νικόλαος|Saint Nicholas|58200|Parish Church
Karydia|Καρυδιά|Ἅγ. Γεώργιος|Saint George|58200|Parish Church
Kerasia|Κερασιά|Ἅγ. Δημήτριος|Saint Demetrius|58200|Parish Church
Lykoi|Λύκοι|Ἅγ. Γεώργιος|Saint George|58200|Parish Church
Margarita|Μαργαρίτα|Ἅγ. Ἀρχάγγελοι|Holy Archangels|58200|Parish Church
Mesimeri|Μεσημέριον|Ἅγ. Ἀνάργυροι|Holy Unmercenaries|58200|Parish Church
Nisi|Νησίον|Ἅγ. Ἀρχάγγελοι|Holy Archangels|58200|Parish Church
Panagitsa|Παναγίτσα|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58200|Parish Church
Platani|Πλατάνη|Ἁγ. Παρασκευή|Saint Paraskevi|58200|Parish Church
Rizari|Ριζάριον|318 Θεοφ. Πατέρες|318 God-bearing Fathers|58200|Parish Church
Samari|Σαμάριον|Ἅγ. Γεώργιος|Saint George|58200|Parish Church
Sotira|Σωτήρα|Ἁγ. Παρασκευή|Saint Paraskevi|58200|Parish Church
Flamouria|Φλαμουριά|Ἅγ. Ἀθανάσιος|Saint Athanasius|58200|Parish Church
''',
    },
    {
        "key": "aridaia",
        "url": "https://www.imepa.gr/7944rhoiotadeltaalpha943alphasigmaf.html",
        "rows": r'''
Aridaia|Ἀριδαία|Ἅγ. Νίκανδ. & Ἰωαν.|Saints Nicander and John|58400|Parish Church
Aridaia|Ἀριδαία|Ἅγ. Ἀντώνιος|Saint Anthony|58400|Parish Church
Aetochori|Ἀετοχώριον|Ἅγ. Δημήτριος|Saint Demetrius|58003|Parish Church
Aloro|Ἄλωρον|Ἅγ. Νικόλαος|Saint Nicholas|58400|Parish Church
Archangelos|Ἀρχάγγελος|Ἅγ. Νικόλαος|Saint Nicholas|58003|Parish Church
Apsalos|Ἄψαλος|Ἅγ. Ἀθανάσιος|Saint Athanasius|58400|Parish Church
Voreino|Βορεινόν|Ἁγ. Εὐφημία|Saint Euphemia|58400|Parish Church
Garefi|Γαρέφειον|Εὐαγγ. Ματθαῖος|Evangelist Matthew|58400|Parish Church
Dorothea|Δωροθέα|Ἀναλήψεως|Ascension of the Lord|58400|Parish Church
Exaplatanos|Ἑξαπλάτανος|Ἅγ. Γεώργιος|Saint George|58400|Parish Church
Theodoraki|Θεοδωράκιον|Ἀναλ. Σωτῆρος|Ascension of the Savior|58400|Parish Church
Theriopetra|Θηριόπετρα|Ἀπ. Φίλιππος|Apostle Philip|58003|Parish Church
Ida|Ἴδα|Ἅγ. Νικόλαος|Saint Nicholas|58400|Parish Church
Koryfi|Κορυφή|Ἅγ. Ἐπιφάνειος|Saint Epiphanius|58400|Parish Church
Kranea|Κρανέα|Ἅγ. Γεώργιος|Saint George|58003|Parish Church
Konstantia|Κωνσταντία|Ἅγ. Νεκτάριος|Saint Nectarios|58400|Parish Church
Lagkadia|Λαγκαδιά|Ἅγ. Ἀνάργυροι|Holy Unmercenaries|58003|Parish Church
Loutraki|Λουτράκιον|Τίμ. Πρόδρομος|Holy Forerunner|58400|Parish Church
Lykostomo|Λυκόστομον|Ἅγ. Νικόλαος|Saint Nicholas|58400|Parish Church
Megaplatanos|Μεγαπλάτανος|Ἅγ. Εὐστάθιος|Saint Eustathius|58400|Parish Church
Milea|Μηλέα|Γεν. Θεοτόκου|Nativity of the Theotokos|58400|Parish Church
Monastiraki|Μοναστηράκιον|Ζωοδ. Πηγή|Life-Giving Spring|58400|Parish Church
Neochori|Νεοχώριον|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58400|Parish Church
Notia|Νότια|Ἁγ. Σοφία|Saint Sophia|58003|Parish Church
Xifiani|Ξιφιανή|Ἅγ. Πολύκαρπος|Saint Polycarp|58400|Parish Church
Orma|Ὅρμα|Ἅγ. Νικόλαος|Saint Nicholas|68400|Parish Church
Perikleia|Περίκλεια|Ἁγ. Παρασκευή|Saint Paraskevi|58003|Parish Church
Piperia|Πιπεριά|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58003|Parish Church
Polykarpi|Πολυκάρπιον|Εἰσ. Θεοτόκου|Entry of the Theotokos|68400|Parish Church
Prodromos|Πρόδρομος|Εὐαγγ. Μάρκος|Evangelist Mark|58003|Parish Church
Promachoi|Πρόμαχοι|Ἅγ. Δημήτριος|Saint Demetrius|58400|Parish Church
Rizochori|Ριζοχώριον|Ἅγ. Ἰγνάτιος|Saint Ignatius|58400|Parish Church
Sarakenoi|Σαρακηνοί|Ἅγ. Νικόλαος|Saint Nicholas|58400|Parish Church
Sosandra|Σωσάνδρα|Ἅγ. Γεώργιος|Saint George|58400|Parish Church
Tsakoi|Τσάκοι|Ἅγ. Γεώργιος|Saint George|58400|Parish Church
Ydraia|Ὑδραία|Ἅγ. Ἀθανάσιος|Saint Athanasius|58400|Parish Church
Filoteia|Φιλώτεια|Ἅγ. Δημήτριος|Saint Demetrius|58003|Parish Church
Foustani|Φούστανη|Ἅγ. Γεώργιος|Saint George|58003|Parish Church
Chrysi|Χρυσῆ|Κοίμ. Θεοτόκου|Dormition of the Theotokos|68400|Parish Church
''',
    },
    {
        "key": "skydra",
        "url": "https://www.imepa.gr/sigmakappa973deltarhoalphasigmaf.html",
        "rows": r'''
Skydra|Σκύδρα|Ἅγ. Στέφανος|Saint Stephen|58500|Parish Church
Anydro|Ἄνυδρο|Ἅγ. Νικόλαος|Saint Nicholas|58500|Parish Church
Arseni|Ἀρσένι|Ἅγ. Ἰω. Θεολόγου|Saint John the Theologian|58500|Parish Church
Aspro|Ἄσπρο|Κοιμ. Θεοτόκου|Dormition of the Theotokos|58500|Parish Church
Giannakochori|Γιαννακοχῶρι|Ἅγ. Κων/νος & Ἑλ.|Saints Constantine and Helen|59200|Parish Church
Dafni|Δάφνη|Ἅγ. Χαράλαμπος|Saint Charalambos|58500|Parish Church
Episkopi|Ἐπισκοπή|Ἅγ. Ἐλευθέριος|Saint Eleftherios|59200|Parish Church
Kali|Καλή|Τιμ. Σταυρός|Holy Cross|58500|Parish Church
Kallipoli|Καλλίπολη|Ἅγ. Δημήτριος|Saint Demetrius|58500|Parish Church
Kalyvia|Καλύβια|Ἅγ. Μηνᾶς|Saint Menas|58500|Parish Church
Lakka|Λάκκα|Ἅγ. Ἀνδρέας|Saint Andrew|58500|Parish Church
Lefkadia|Λευκάδια|Ἁγ. Παρασκευή|Saint Paraskevi|59200|Parish Church
Lipochori|Λιποχῶρι|Τρεῖς Ἅγιοι|Three Saints|58500|Parish Church
Loutrochori|Λουτροχῶρι|Ἅγ. Πάντες|All Saints|58500|Parish Church
Mandalo|Μάνδαλο|Ἅγ. Γεώργιος|Saint George|58500|Parish Church
Marina|Μαρίνα|Ἁγ. Μαρίνα|Saint Marina|59200|Parish Church
Mavrovouni|Μαυροβούνι|Ἀπ. Πέτρου & Παύλ.|Apostles Peter and Paul|58500|Parish Church
Nea Zoi|Νέα Ζωή|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58500|Parish Church
Petraia|Πετραία|Ἅγ. Γεώργιος|Saint George|58500|Parish Church
Plevroma|Πλεύρωμα|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58500|Parish Church
Polla Nera|Πολλά Νερά|Ἅγ. Δημήτριος|Saint Demetrius|58500|Parish Church
Profitis Ilias|Προφ. Ἠλίας|Προφ. Ἠλίας|Prophet Elijah|58500|Parish Church
Rizo|Ριζό|Μεταμορφώσεως|Transfiguration of the Savior|58500|Parish Church
Rodochori|Ροδοχώριον|Ἅγ. Δημήτριος|Saint Demetrius|59200|Parish Church
Sandalio|Σανδάλιον|Ἀπ. Πέτρου & Παύλ.|Apostles Peter and Paul|58500|Parish Church
Sevasteiana|Σεβαστειανά|Ἅγ. Νικόλαος|Saint Nicholas|58500|Parish Church
Strantza|Στράντζα|Ἅγ. Μυροφόροι|Holy Myrrh-bearers|59200|Parish Church
''',
    },
    {
        "key": "giannitsa",
        "url": (
            "https://www.imepa.gr/"
            "gammaiotaalphanunuiotatausigma8182nu.html"
        ),
        "rows": r'''
Giannitsa|Γιαννιτσά|Κοίμησις Θεοτόκου (Μητρόπολη)|Dormition of the Theotokos|581 00|Metropolitan Church
Giannitsa|Γιαννιτσά|Ἅγ. Γεώργιος|Saint George|581 00|Parish Church
Giannitsa|Γιαννιτσά|Ἅγ. Κων/νος & Ἑλένη|Saints Constantine and Helen|581 00|Parish Church
Giannitsa|Γιαννιτσά|Ἀπ. Πέτρος & Παῦλος|Apostles Peter and Paul|581 00|Parish Church
Giannitsa|Γιαννιτσά|Ἁγία Παρασκευή|Saint Paraskevi|581 00|Parish Church
Agios Georgios|Ἅγ. Γεώργιος|Ἅγ. Δημήτριος|Saint Demetrius|58500|Parish Church
Agios Loukas|Ἅγ. Λουκᾶς|Ἅγ. Λουκᾶς|Saint Luke|58300|Parish Church
Agrosykea|Ἀγροσυκέα|Ἅγ. Ἰωάννης Χρυσόστομος|Saint John Chrysostom|57100|Parish Church
Akrolimni|Ἀκρολίμνη|Ἅγ. Νικόλαος|Saint Nicholas|58300|Parish Church
Ampelies|Ἀμπελιές|Ἅγ. Ἀθανάσιος|Saint Athanasius|58100|Parish Church
Axios|Ἀξός|Ἅγ. Γεώργιος|Saint George|58100|Parish Church
Arabissos|Ἀραβησσός|Μεταμορφώσεως|Transfiguration of the Savior|58100|Parish Church
Archontiko|Ἀρχοντικόν|Ἅγ. Ἀθανάσιος|Saint Athanasius|58100|Parish Church
Asvestario|Ἀσβεσταριό|Ἀναλήψεως|Ascension of the Lord|58100|Parish Church
Achladochori|Ἀχλαδοχώριον|Ἅγ. Μόδεστος|Saint Modestus|58100|Parish Church
Galatades|Γαλατάδες|Ἅγ. Ἀθανάσιος|Saint Athanasius|58100|Parish Church
Gypsochori|Γυψοχώριον|Ἅγ. Ἀθανάσιος|Saint Athanasius|58100|Parish Church
Damiano|Δαμιανόν|Ἅγ. Δημήτριος|Saint Demetrius|58100|Parish Church
Drosero|Δροσερόν|Ἅγ. Κων/νος & Ἑλ.|Saints Constantine and Helen|58100|Parish Church
Dytiko|Δυτικόν|Ἅγ. Κων/νος & Ἑλ.|Saints Constantine and Helen|57100|Parish Church
Eleftherochori|Ἐλευθεροχώριον|Ἅγ. Κοσμᾶς ὁ Αἰτωλ.|Saint Kosmas the Aetolian|58100|Parish Church
Esovalta|Ἐσώβαλτα|Ἁγ. Τριάς|Holy Trinity|58300|Parish Church
Karyotissa|Καρυώτισσα|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58100|Parish Church
Krya Vrysi|Κρύα Βρύση|Γεννήσεως|Nativity|58300|Parish Church
Krya Vrysi|Κρύα Βρύση|Ἁγ. Κυριακή|Saint Kyriake|58300|Parish Church
Leptokarya|Λεπτοκαρυά|Ἅγ. Νικόδημος|Saint Nicodemus|58100|Parish Church
Liparo|Λιπαρόν|Ἅγ. Παῦλος|Saint Paul|58500|Parish Church
Melissi|Μελίσσιον|Ἅγ. Βασίλειος|Saint Basil|68100|Parish Church
Messiano|Μεσσιανόν|Ἅγ. Παντελεήμων|Saint Panteleimon|58100|Parish Church
Nea Pella|Νέα Πέλλα|Μεταμορφώσεως|Transfiguration of the Savior|58100|Parish Church
Neos Mylotopos|Ν. Μυλότοπος|Ἅγ. Γεώργιος|Saint George|58100|Parish Church
Pella|Πέλλα|Ἅγ. Ἀπόστολοι|Holy Apostles|57007|Parish Church
Palaios Mylotopos|Π. Μυλότοπος|Ἁγ. Παρασκευή|Saint Paraskevi|58100|Parish Church
Palaifyto|Παλαίφυτον|Τίμ . Πρόδρομος|Holy Forerunner|58200|Parish Church
Paralimni|Παραλίμνη|Ἅγ. Χαράλαμπος|Saint Charalambos|58100|Parish Church
Pentaplatanos|Πενταπλάτανος|Ἅγ. Ἀρτέμιος & Γερ.|Saints Artemios and Gerasimos|58100|Parish Church
Plagiari|Πλαγιάριον|Γεν. Θεοτόκου|Nativity of the Theotokos|58100|Parish Church
Stavrodromi|Σταυροδρόμιον|Κοίμ. Θεοτόκου|Dormition of the Theotokos|58300|Parish Church
Trifylli|Τριφύλλιον|Ὑπαπαντῆς|Meeting of the Lord|58100|Parish Church
''',
    },
    {
        "key": "koufalia",
        "url": (
            "https://www.imepa.gr/"
            "kappaomicronupsilonphialphalambda943omeganu.html"
        ),
        "rows": r'''
Koufalia|Κουφάλια|Ἅγ. Ἀθανάσιος|Saint Athanasius|57100|Parish Church
Koufalia|Κουφάλια|Ἅγ. Γεώργιος|Saint George|57100|Parish Church
Koufalia|Κουφάλια|Ἅγ. Τρύφων|Saint Tryphon|57100|Parish Church
Athyra|Ἄθυρα|Ἀναλήψεως|Ascension of the Lord|57100|Parish Church
Valtochori|Βαλτοχῶρι|Κοίμ. Θεοτόκου|Dormition of the Theotokos|57007|Parish Church
Eleousa|Ἐλεοῦσα|Ἅγ. Γεώργιος|Saint George|57007|Parish Church
Leivaditsa|Λειβαδίτσα|Ἅγ. Ἀλέξιος|Saint Alexios|57100|Parish Church
Loudias|Λουδίας|Τίμ. Σταυρός|Holy Cross|57007|Parish Church
Mikro Monastiri|Μ. Μοναστήρι|Ἅγ. Δημήτριος|Saint Demetrius|57007|Parish Church
Partheni|Παρθένι|Ἅγ. Γεώργιος|Saint George|57007|Parish Church
Rachona|Ραχώνα|Ἅγ. Γεώργιος|Saint George|57100|Parish Church
Chalkidona|Χαλκηδόνα|Ἅγ. Παντελεήμων|Saint Panteleimon|57007|Parish Church
''',
    },
]


MONASTIC_ROWS = r'''
Aridaia|Ἀρχαγγέλου Μιχαήλ (Ἀριδαίας)|Archangel Michael|23840-73499|Monastery
Marina|Μεταμορφώσεως τοῦ Σωτῆρος (Μαρίνας)|Transfiguration of the Savior|23320-44192|Monastery
Edessa|Προφήτου Ἠλιοῦ (Ἐδέσσης)|Prophet Elijah|23810-29854|Monastery
Giannitsa|Ἁγίας Παρασκευῆς (Γιαννιτσῶν)|Saint Paraskevi||Monastery
Edessa|Ἁγ. Τριάδος Ἐδέσσης|Holy Trinity|23810-22870|Monastery
Mesimeri|Ὑψώσεως Τιμ. Σταυροῦ Μεσημερίου|Exaltation of the Holy Cross|23810-23578|Monastery
Lakka, Giannitsa|Κοιμήσεως Θεοτόκου Λάκκας Γιαννιτσῶν|Dormition of the Theotokos|23810-97357|Monastery
Promachoi, Aridaia|Ἁγίου Ἱλαρίωνος Μογλενῶν, Πρόμαχοι Ἀριδαίας|Saint Hilarion of Moglena|23840-75700|Monastery
Koufalia|Ἡσυχαστήριον Ἁγ. Γρηγορίου Παλαμᾶ Κουφαλίων|Saint Gregory Palamas|23910-51563|Hesychasterion
'''


INSTITUTIONAL_ROWS = r'''
Rodochori, Imathia|Ἱ. Μονή Ἁγίου Γεωργίου Περιστερεώτα (Συλλόγου Ποντίων) εἰς Ροδοχώριον Ἡμαθίας|Saint George Peristereota Institutional Church
Leivaditsa, Pella|Ἁγίας Τριάδος (Συλλόγου Ἀνατολικορωμυλιωτῶν) εἰς Λειβαδίτσαν Πέλλης|Holy Trinity Institutional Church
'''


# The regional tables place public contact numbers in the same visual row as
# each church and its serving clergy. They are retained as church-associated
# contacts without claiming that each number is a church office line.
PARISH_PHONE_ROWS = r'''
edessa|1|88941;23500 (ἐσωτ. 7);27770;22720
edessa|2|27295
edessa|3|23500 (ἐσωτ. 2);23909;29296
edessa|4|82711;29010;27411
edessa|5|51272
edessa|6|92888
edessa|7|31368
edessa|10|21327
edessa|12|20349
edessa|13|92867
edessa|14|82426
edessa|17|92742
edessa|18|34398
edessa|19|29384
edessa|20|91388
edessa|23|21862
aridaia|1|2384024968;23279
aridaia|2|6981176587
aridaia|3|73499
aridaia|4|92029
aridaia|5|73203
aridaia|7|71042
aridaia|10|62094
aridaia|12|62317
aridaia|13|51587
aridaia|15|41742
aridaia|16|23993
aridaia|17|73388
aridaia|18|91266
aridaia|19|91358
aridaia|21|41463
aridaia|24|73064
aridaia|25|21879
aridaia|26|94101
aridaia|27|73335
aridaia|28|24723
aridaia|29|31345
aridaia|30|51507
aridaia|31|75517
aridaia|34|23500
aridaia|35|23500
aridaia|36|6978875422
aridaia|37|41641
aridaia|38|41595
skydra|1|2381081927;2381082713
skydra|2|2381041148
skydra|3|2381071791
skydra|4|61757
skydra|6|2381061993
skydra|7|2332044129
skydra|8|2381041746
skydra|9|2381094485
skydra|11|2381097478
skydra|12|2332041457
skydra|13|2381082632
skydra|15|2381097406
skydra|16|2332044640
skydra|17|2381083253
skydra|19|2381071409
skydra|21|6979131187
skydra|22|2381041723
skydra|23|2381081099
skydra|25|2381094354
skydra|27|2332044192
giannitsa|1|6979665959;20479
giannitsa|2|27794;22714;28448;24341
giannitsa|3|26338
giannitsa|4|21864;21907;23802;83735
giannitsa|5|82426;83206
giannitsa|6|62154
giannitsa|8|63069
giannitsa|9|94525
giannitsa|10|51131
giannitsa|11|99524
giannitsa|14|52027
giannitsa|16|2382.100166
giannitsa|17|23662
giannitsa|19|93160
giannitsa|21|28529
giannitsa|22|41484
giannitsa|23|62400
giannitsa|24|63785
giannitsa|27|41018
giannitsa|28|43081
giannitsa|29|31895
giannitsa|30|31604;6972236355
giannitsa|31|51233
giannitsa|32|32177
giannitsa|33|52392
giannitsa|34|42440
giannitsa|35|6983629942
giannitsa|36|21160
giannitsa|38|71136
giannitsa|39|2381094259
koufalia|1|23910.52822
koufalia|2|2391053705
koufalia|3|2391053528
koufalia|4|2391091318
koufalia|8|2391061412
koufalia|12|2333026263
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_lines(block, columns):
    result = []
    for raw in block.strip().splitlines():
        values = [value.strip() for value in raw.split("|")]
        if len(values) != len(columns):
            raise ValueError("invalid Edessa source row: %s" % raw)
        result.append(dict(zip(columns, values)))
    return result


def parse_phone_rows(block):
    result = {}
    for raw in block.strip().splitlines():
        group, position, values = [value.strip() for value in raw.split("|", 2)]
        key = (group, int(position))
        if key in result:
            raise ValueError("duplicate Edessa phone association: %r" % (key,))
        result[key] = [value.strip() for value in values.split(";")]
    return result


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def build_rows():
    rows = []
    group_counts = {}
    phone_rows = parse_phone_rows(PARISH_PHONE_ROWS)
    columns = (
        "seat", "seat_local", "local", "dedication", "postcode", "rank"
    )
    for group in SOURCE_GROUPS:
        records = parse_lines(group["rows"], columns)
        group_counts[group["key"]] = len(records)
        for position, record in enumerate(records, 1):
            row = {
                "id": "gr-edessa-%s-%s" % (
                    slug(record["seat"]), slug(record["dedication"])
                ),
                "parent": PARENT,
                "kind": "parish",
                "rank": record["rank"],
                "name": make_name(
                    record["dedication"], record["rank"], record["seat"]
                ),
                "local": record["local"],
                "seat": record["seat"],
                "country": "GR",
                "address": "%s, Τ.Κ. %s" % (
                    record["seat_local"], record["postcode"]
                ),
                "sources": [group["url"]],
                "checked": CHECKED,
            }
            if (group["key"] == "edessa" and
                    record["rank"] == "Metropolitan Cathedral"):
                row["sources"].append(CATHEDRAL_PAGE)
            phones = phone_rows.get((group["key"], position), [])
            if phones:
                row["phones"] = phones
                row["contact_sources"] = [group["url"]]
                row["contact_checked"] = CHECKED
            rows.append(row)

    valid_phone_keys = {
        (group["key"], position)
        for group in SOURCE_GROUPS
        for position in range(1, group_counts[group["key"]] + 1)
    }
    if not set(phone_rows).issubset(valid_phone_keys):
        raise ValueError("Edessa phone association is outside a roster")

    columns = ("seat", "local", "dedication", "phone", "rank")
    for record in parse_lines(MONASTIC_ROWS, columns):
        row = {
            "id": "gr-edessa-%s-%s" % (
                slug(record["rank"]), slug(record["dedication"])
            ),
            "parent": PARENT,
            "kind": "monastery",
            "rank": record["rank"],
            "name": make_name(
                record["dedication"], record["rank"], record["seat"]
            ),
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": record["seat"],
            "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
            "checked": CHECKED,
        }
        if record["phone"]:
            row["phones"] = [record["phone"]]
            row["contact_sources"] = [MONASTERY_PAGE, PATRIARCHATE_PAGE]
            row["contact_checked"] = CHECKED
        rows.append(row)

    columns = ("seat", "local", "dedication")
    for record in parse_lines(INSTITUTIONAL_ROWS, columns):
        rows.append({
            "id": "gr-edessa-institutional-%s" % slug(record["dedication"]),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Institutional Church",
            "name": "%s in %s" % (record["dedication"], record["seat"]),
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": record["seat"],
            "sources": [PATRIARCHATE_PAGE],
            "checked": CHECKED,
        })
    return rows, group_counts


ROWS, GROUP_COUNTS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}
EXPECTED_GROUP_COUNTS = {
    "aridaia": 39,
    "edessa": 23,
    "giannitsa": 39,
    "koufalia": 12,
    "skydra": 27,
}
EXPECTED_TOTAL = 151
EXPECTED_OWNER_COUNTS = {PARENT: 151}
EXPECTED_KINDS = {"monastery": 9, "parish": 142}
EXPECTED_RANKS = {
    "Hesychasterion": 1,
    "Institutional Church": 2,
    "Metropolitan Cathedral": 1,
    "Metropolitan Church": 1,
    "Monastery": 8,
    "Parish Church": 138,
}
EXPECTED_PARISH_PHONE_BODIES = 100
EXPECTED_PARISH_PHONE_VALUES = 118
EXPECTED_CONTACT_BODIES = 108
EXPECTED_PHONE_BODIES = 108
EXPECTED_PHONE_VALUES = 126
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 151
EXISTING_PARENTS = {PARENT}
COMPETENT_HOSTS = {
    "www.imepa.gr",
    "imepa.gr",
    "ec-patr.org",
    "www.ecclesiagreece.gr",
    "ecclesiagreece.gr",
    "www.parembasis.gr",
    "parembasis.gr",
}
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
    if parsed.scheme != "https" or parsed.netloc not in COMPETENT_HOSTS:
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
    if (ledger.get("v") != 1 or ledger.get("countries") != ["GR"] or
            ledger.get("parent") != PARENT or
            ledger.get("checked") != CHECKED):
        raise ValueError("Edessa candidate ledger metadata drifted")
    expected_summary = {
        PARENT: 151,
        "total": 151,
        "parish_kind_rows": 142,
        "monastery_kind_rows": 9,
        "contact_bodies": 108,
        "phone_bodies": 108,
        "public_phone_values": 126,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 151,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Edessa ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Edessa ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Edessa ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Edessa ledger has an invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Edessa ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Edessa ledger has forbidden punctuation")
    return ledger


def validate_rows():
    if GROUP_COUNTS != EXPECTED_GROUP_COUNTS:
        raise ValueError("Edessa regional roster counts drifted: %r"
                         % GROUP_COUNTS)
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
            if len(digits) < 5 or len(digits) > 15:
                raise ValueError("%s carries an invalid public phone" % row_id)
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
        raise ValueError("Edessa English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Edessa English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Edessa parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Edessa kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Edessa rank totals drifted: %r"
                         % dict(sorted(rank_counts.items())))
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
        raise ValueError("Edessa contact coverage drifted: %r" % (coverage,))
    parish_rows = [item for item in result if item["rank"] in {
        "Metropolitan Cathedral", "Metropolitan Church", "Parish Church"
    }]
    parish_phone_coverage = (
        sum(bool(item.get("phones")) for item in parish_rows),
        sum(len(item.get("phones") or []) for item in parish_rows),
    )
    if parish_phone_coverage != (
            EXPECTED_PARISH_PHONE_BODIES, EXPECTED_PARISH_PHONE_VALUES):
        raise ValueError("Edessa parish phone coverage drifted: %r"
                         % (parish_phone_coverage,))
    return result


def build():
    rows = validate_rows()
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": rows,
        }
    }


def all_source_urls():
    urls = {
        PARENT_SITE,
        STATISTICS_PAGE,
        MONASTERY_PAGE,
        PATRIARCHATE_PAGE,
        CHURCH_OF_GREECE_PAGE,
        CATHEDRAL_PAGE,
    }
    urls.update(group["url"] for group in SOURCE_GROUPS)
    for row in ROWS:
        urls.update(row.get("sources") or [])
        urls.update(row.get("contact_sources") or [])
    ledger = validate_ledger()
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        for entry in ledger[key]:
            urls.update(entry.get("sources") or [])
    return sorted(urls)


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u200b", " ").replace("\u00a0", " ")
    value = unicase(value)
    return re.sub(r"\s*/\s*", "/", value)


class TableCellParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.cells = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.depth += 1
            self.current = []
        elif self.depth and tag in {"br", "div", "p"}:
            self.current.append("\n")

    def handle_endtag(self, tag):
        if tag == "td" and self.depth:
            self.cells.append("".join(self.current))
            self.current = []
            self.depth -= 1
        elif self.depth and tag in {"div", "p"}:
            self.current.append("\n")

    def handle_data(self, data):
        if self.depth:
            self.current.append(data)


def source_cell_lines(value):
    return [
        " ".join(line.replace("\u200b", "").split())
        for line in value.splitlines()
    ]


def extract_live_phone_rows(body):
    parser = TableCellParser()
    parser.feed(body)
    if len(parser.cells) < 5:
        raise ValueError("official parish table has fewer than five cells")
    cells = parser.cells[-5:]
    dedications = source_cell_lines(cells[1])
    phones = source_cell_lines(cells[4])
    size = max(len(dedications), len(phones))
    dedications += [""] * (size - len(dedications))
    phones += [""] * (size - len(phones))
    starts = [
        index for index, value in enumerate(dedications)
        if value and not value.startswith("(")
    ]
    result = {}
    for position, start in enumerate(starts, 1):
        end = starts[position] if position < len(starts) else size
        values = [value for value in phones[start:end]
                  if value and value != "-"]
        expanded = []
        for value in values:
            if " ἤ " in value:
                expanded.extend(part.strip() for part in value.split(" ἤ "))
            elif " καί " in value:
                expanded.extend(part.strip() for part in value.split(" καί "))
            else:
                expanded.append(value)
        if expanded:
            result[position] = expanded
    return result


def check_live_sources():
    failures = []
    source_texts = {}
    source_bodies = {}
    for url in all_source_urls():
        try:
            request = Request(url, headers={"User-Agent": "Plithos directory audit"})
            with urlopen(request, timeout=30) as response:
                content_type = response.headers.get("content-type", "").lower()
                body = response.read().decode("utf-8", "replace")
                if (response.status != 200 or
                        not any(kind in content_type
                                for kind in ("html", "xml"))):
                    failures.append("%s returned %s %s" % (
                        url, response.status, content_type
                    ))
                    continue
                source_texts[url] = normalize_source_text(body)
                source_bodies[url] = body
        except Exception as exc:
            failures.append("%s failed: %s" % (url, exc))
    for row in ROWS:
        needle = unicase(row["local"])
        if not any(needle in source_texts.get(url, "")
                   for url in row["sources"]):
            failures.append("%s local name is absent from live sources"
                            % row["id"])
        for phone in row.get("phones") or []:
            phone_needle = unicase(phone)
            phone_digits = re.sub(r"\D", "", phone)
            if not any(
                    phone_needle in source_texts.get(url, "") or
                    phone_digits in re.sub(
                        r"\D", "", source_texts.get(url, "")
                    )
                    for url in row.get("contact_sources") or []):
                failures.append("%s phone %s is absent from contact sources"
                                % (row["id"], phone))
    expected_phone_rows = parse_phone_rows(PARISH_PHONE_ROWS)
    for group in SOURCE_GROUPS:
        expected = {
            position: phones
            for (key, position), phones in expected_phone_rows.items()
            if key == group["key"]
        }
        try:
            actual = extract_live_phone_rows(source_bodies[group["url"]])
        except (KeyError, ValueError) as exc:
            failures.append("%s phone table could not be read: %s"
                            % (group["key"], exc))
            continue
        if actual != expected:
            failures.append("%s live phone associations drifted"
                            % group["key"])
    stats = source_texts.get(STATISTICS_PAGE, "")
    for phrase in (
            "ενοριακοι ναοι 140", "παρεκκλησια 40", "εξωκκλησια 71",
            "ιδιωτικοι ναοι 5", "μοναστηριακοι ναοι 10"):
        if phrase not in stats:
            failures.append("statistics source lacks %s" % phrase)
    parent_text = source_texts.get(PATRIARCHATE_PAGE, "")
    for phrase in ("ενοριακοι ναοι: 140", "ιδρυματικοι ναοι"):
        if phrase not in parent_text:
            failures.append("patriarchal source lacks %s" % phrase)
    if failures:
        raise ValueError("live source check failed:\n" + "\n".join(failures))
    return len(source_texts)


def main(argv=None):
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    args = parser.parse_args(argv)
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    elif args.check_live:
        count = check_live_sources()
        print("Edessa: %d official source URLs live" % count)
    else:
        print(
            "Edessa: %d exact named bodies; %d carry current public "
            "contact data" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Edessa: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
