#!/usr/bin/env python3
"""Validate exact current Fthiotis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_fthiotis_country.py --check
    python tools/directory_fthiotis_country.py --check-live
    python tools/directory_fthiotis_country.py --dump
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
PARENT = "gr-fthiotis"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "fthiotis_country.json"
)
OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
REGION_INDEX = "https://www.imfth.gr/taxonomy-basic-page/term/36"
MONASTERY_INDEX = "https://www.imfth.gr/taxonomy-basic-page/term/37"
CHAPEL_PAGE = "https://www.imfth.gr/content/mitropolitika-parekklisia"

REGION_DEFAULTS = {
    1: "Lamia",
    2: "Thermopylae and Roditsa",
    3: "Ypati",
    4: "Lianokladi",
    5: "Amfikleia",
    6: "Atalanti",
    7: "Opountia and Malessina",
    8: "Domokos and Xyniada",
    9: "Thavmakos and Neo Monastiri",
    10: "Mendenitsa and Kamena Vourla",
    11: "Makrakomi and Tymfristos",
    12: "Spercheiada and Gardiki",
    13: "Stylida",
    14: "Pelasgia",
}

PARISH_NAME_OVERRIDES = {
    2: "Parish Church of Saint Athanasius in Galaneika, Lamia",
    3: "Parish Church of the Holy Apostles in Pangrati, Lamia",
    5: "Parish Church of Saint George in Kalyvia, Lamia",
    6: "Parish Church of Saint George in Nea Ambliani, Lamia",
    9: "Parish Church of Saint Constantine in Nea Magnisia, Lamia",
    12: "Parish Church of Saint Paraskevi in Nea Ambliani, Lamia",
    15: "Parish Church of Saint Nectarius in Neapoli, Lamia",
    16: "Parish Church of Saint Cosmas in the Workers' Housing, Nea Magnisia",
    17: "Parish Church of Saint Nicholas in Nea Vracha, Lamia",
    18: "Parish Church of the Dormition of the Theotokos in Nea Evrytania, Lamia",
    19: "Parish Church of the Entrance of the Theotokos in Stavros, Lamia",
    20: "Parish Church of Saint Basil at Lianokladi Station",
    21: "Parish Church of the Dormition of the Theotokos at Lamia Cemetery",
    23: "Parish Church of Saint Paraskevi at Agia Paraskevi Sfageion",
}

# Region number | current identity and contact source | current Greek listing |
# current body-associated public phones
PARISH_SOURCE = r'''
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Λαμία-Εὐαγγ. Θεοτόκου 23.151(Καθερδικός)|2231023151,2231062248,2231052426
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Ἀθανάσιος Γαλανέικων 27.115|2231027115,2231030078,2231021620
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Ἀπόστολοι Παγκρατίου 23.114|2231023114,2231061190
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἁγ. Βαρβάρα 33.798|2231033798,2231038996,2231022380,2231024934
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Γεώργιος Καλυβίων 51.839|2231051839,2231052866,2231034856
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Γεώργιος 43.466|2231043466
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Δημήτριος 24.294|2231024294,2231029351,2231101670
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Θεόδωροι 24.771|2231024771,2231052065
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Κων/νος Ν. Μαγνησίας 26.954|2231026954,2231039681
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Λουκᾶς (Πολιοῦχος)36.252|2231036252
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Νικόλαος 22.568|2231022568,2231043904,2231023231,2231037514
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἁγ. Παρασκευή Ν. Ἄμπλιανης 24.961|2231024961,2231053493
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Παναγία Δέσποινα 22.211|2231022211,2231094140,2231038946,6984762699
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἁγ. Σοφία 38.708|2231038708
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Νεκτάριος (Νεαπόλεως) 28170|2231028170
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Κοσμᾶς Ἐργ. Κατοικίαι 67.316|2231067316
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Ἅγ. Νικόλαος Ν. Βράχα 61.325|2231061325,2231061645
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Κοίμ. Θεοτόκου Ν. Εὐρυτανίας 69.131|2231069131
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Εἰσ. Θεοτόκου Σταυροῦ 61.214|2231061214,2231026673
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Λιανοκλάδιον Στ.-Ἅγ. Βασίλειος 62.252|2231062252,2231033267
1|https://www.imfth.gr/content/arhieratiki-perifereia-lamias|Κοίμηση Θεοτόκου (Κοιμητήριον) 34.730|2231034730
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Ροδίτσα - Ἅγ. Ἀθανάσιος 26.546|2231026546,2231039332
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Ἁγ. Παρασκ. Φθιώτ.-Ἁγ. Παρασκευή 33275|2231033275,2231045094
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Ἀλεπόσπιτα - Ἅγ. Γεώργιος|6977935731
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Ἀνθήλη - Ἅγ. Νικόλαος 93.561|2231093561,2231093145
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Βαρδάτες - Ἅγ. Νικόλαος|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Βουνά Δύο - Ἁγ. Αἰκατερίνη|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Γοργοπόταμος - Ζωοδ. Πηγή|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Δαμάστα - Κοίμ. Θεοτόκου|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Δέλφινον - Ἅγ. Ἀθανάσιος|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Ἐλευθεροχώριον - Ἁγ. Παρασκευή|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Ἠράκλεια - Ἅγ. Δημήτριος|2231301583
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Θερμοπῦλαι - Ἅγ. Ἰωάννης|2231022462
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Κόμμα - Ἅγ. Ἀθανάσιος|2231030034
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Κουμαρίτσιον - Ἁγ. Παρασκευή|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Κρίκελλον Νέον - Ἅγ. Κων/νος|2231026214
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Κωσταλέξιον-Ἅγ. Ἀθανάσιος 96.242|2231096242,2231096027
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Μεγάλη Βρύση-Ἅγ. Γεώργιος|2231046418
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Μοσχοχώριον - Ἁγ. Παρασκευή|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Οἴτη - Ἅγ. Ἀθανάσιος|
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Παύλιανη - Ἅγ. Ἀθανάσιος|2235024764
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Σκαμνός - Ἅγ. Κωνσταντῖνος|2231092474
2|https://www.imfth.gr/content/v-arhieratiki-perifereia-thermopylon-roditsis|Φραντζή - Ἅγ. Γεώργιος|2231038980
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Ὑπάτη - Ἅγ. Νικόλαος|2231098238
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Ἅγ. Γεώργιος 95.218|2231095218
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Ὑπάτης Λουτρά-Ἅγ. Κων/νος 59.115|2231059115,6971702838
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Ἀμαλώτα - Ἅγ. Γεώργιος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Ἀργυροχώριον-Ἅγ.Δημήτριος|2231051281
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Βασιλικά Ὑπάτης - Ἅγ. Δημήτριος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Δάφνη - Ἅγ. Ἀπόστολοι|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Καπνοχώριον - Ἅγ. Νικόλαος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Καρυά Ὑπάτης - Ἅγ. Χαράλαμπος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Καστανιά - Ἅγ.Ἀθανάσιος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Κομποτάδες - Ἁγ. Παρασκευή|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Λαδικοῦ - Ἅγ. Ἰωάννης|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Λυχνός - Ἅγ. Γεώργιος|2231095218
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Μεξιάτες - Ἅγ. Παντελεήμων|2231059454
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Μεσοχώριον Ὑπάτης -Ἅγ. Νικόλαος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Νεοχώριον Ὑπάτης - Ἅγ. Νικόλαος .|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Περιστέριον - Ἅγ. Γεώργιος|
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Πύργος Ὑπάτης-Κοίμ.Θεοτόκου|2236044334
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Ροδωνιά - Κοίμ. Θεοτόκου|2231061073
3|https://www.imfth.gr/content/g-arhieratiki-perifereia-ypatis|Συκᾶ - Ἅγ. Νικόλαος|2231094530
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Λιανοκλάδιον-Ἅγ. Γεώργιος 79.590|2231079590,2231079334
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Ἀγρηλιά - Ἅγ. Γεώργιος|
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Ἀμούριον - Ἅγ. Δημήτριος|2231031537
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Δίβρη - Ἁγ. Βαρβάρα|
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Ζηλευτόν - Ἅγ. Νικόλαος|
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Καλαμάκιον - Ἅγ. Νικόλαος|
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Λυγαριά - Ἅγ. Ἀθανάσιος|2231052670
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Μοσχοκαρυά - Ἅγ. Νικόλαος|2236023192
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Στύρφακα - Ἅγ. Γεώργιος|2231079895
4|https://www.imfth.gr/content/d-arhieratiki-perifereia-lianokladioy|Τρίλοφον - Ἅγ. Ἀθανάσιος|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ἀμφίκλεια - Ἅγ. Δημήτριος|2234022757
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ἅγ. Βλάσιος|2234022800
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Εἰσ. Θεοτόκου 22.702|2234022702,2234023459
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ἀνθοχώριον - Ἅγ. Δημήτριος|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ἁγ. Μαρίνα Λοκρίδ.-Κοίμ. Θεοτόκου|2234071064
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ἁγ. Παρασκευή - Ἁγ. Παρασκευή|2234049376
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Βασιλικά Λοκρίδος - Ἅγ. Ἀθανάσιος|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Δρυμαία - Ἅγ. Ἰωάννης|2234031470
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ἐλάτεια - Ἅγ. Δημήτριος|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Κουμπουριανά - Ἅγ. Εὐστάθιος|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Λευκοχώριον - Ἅγ. Γεώργιος|2234031621
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Μόδιον - Ἅγ. Νικόλαος|2234049977
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Ξυλικοί - Ἁγ. Παρασκευή|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Παναγίτσα - Ἅγ. Ἀθανάσιος|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Παρόριον - Ἅγ. Θεόδωροι|
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Προφ. Ἠλίας - Ἅγ. Νικόλαος|2261061390
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Στεφανιάς - Ἁγ. Τριάς|2234031838
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Τιθορέα - Κοίμ. Θεοτόκου|2234071581
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Τιθορέα Κάτω-Ἅγ.Δημήτριος 49.047|2234049047,2234049349
5|https://www.imfth.gr/content/e-arhieratiki-perifereia-amfikleias|Τιθρώνιο - Κοίμ. Θεοτόκου|
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Ἀταλάντη - Ἅγ. Θεόδωροι 22.485|2233022485,2233022978
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Μεταμ. Σωτῆρος 22.389|2233022389,2233023257
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Ἀρκίτσα - Ἅγ. Γεώργιος|2233091064
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Γουλέμιον - Ἁγ. Παρασκευή|
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Ἔξαρχος - Ἅγ. Γεώργιος|2233095380
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Ζέλιον - Ἅγ. Σεραφείμ 71481|2233071481,2233071207
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Καλαπόδιον - Εὐαγγ. Θεοτόκου|
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Κυρτώνη - Ἅγ. Γεώργιος|2233094322
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Κυπαρίσσιον - Εἰσoδ. Θεοτόκου|
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Λιβανάται-Ἅγ.Γεώργιος 31104|2233031104,2233091479
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Λιβανάται (παρ.) - Ἁγ. Κυριακή 32.465|2233032465,2233031212
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Μεγαπλάτανος - Ἅγ. Βασίλειος|2233023303
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Σφάκα - Ἅγ. Δημήτριος 2234031233|2234031233,2233031632
6|https://www.imfth.gr/content/st-arhieratiki-perifereia-atalantis|Τραγάνα - Ἅγ. Νικόλαος 94.401|2233094401
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Μαρτῖνον - Παμμ. Ταξιάρχαι 61.750|2233061750,2233092256,2233061310
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Θεολόγος - Ἅγ. Ἰωάνν|2233093325
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Λάρυμνα - Εὐαγγ. Θεοτόκου|
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Μάζιον - Ἅγ. Ἰωάννης|
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Μαλεσσίνα-Ἅγ.Κωνσταντῖνος|2233051294,2233051879
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Ἁγία Τριάς|
7|https://www.imfth.gr/content/z-arhieratiki-perifereia-opoyntion-malessinis|Προσκυνᾶς - Ἅγ. Γεώργιος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Δομοκός - Ἁγ. Παρασκευή 22.012|2232022012,2232022409
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ἁγ. Κυριακή 22.922|2232022922,2232023213
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ἅγ. Γεώργιος Δομοκ.-Ἅγ. Νικόλαος|2232041502
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ἅγ. Στέφανος - Ἁγ. Μαρίνα|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ἄνω Ἀγόριανη - Ἁγ. Παρασκευή|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ἀνάβρα Ἁλμυροῦ - Ἅγ. Δημήτριος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ἀχλαδιά - Κοίμ. Θεοτόκου|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Βούζιον - Ἅγ. Γεώργιος|2232092050
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Γερακλῆ - Ἅγ. Γεώργιος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Καρυά Δομοκοῦ - Ἅγ. Δημήτριος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Κορομηλιά - Προφ. Ἠλίας|2232051194
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Λεῦκα Δομοκοῦ - Ἅγ. Ἀνάργυροι|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Μακρολείβαδον - Ἅγ. Γεώργιος|2232041551
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Μάκρυση Νέα - Ἅγ. Πέτρος & Παῦλος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Μακρυρράχη - Ἅγ. Νικόλαος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Μαντασιά - Ἅγ. Γεώργιος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Μελιταία - Ἅγ. Νικόλαος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Μεταλλεῖα - Ἁγ. Βαρβάρα|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Νεοχώριον Δομοκοῦ-Ἅγ.Ἀνάργυροι|2231069153
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ξυνιάς - Κοίμ. Θεοτόκου 51.203|2232051203
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Ὀμβριακή - Ἅγ. Γεώργιος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Παλαμᾶς - Ἅγ. Ἀθανάσιος|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Παναγιά - Κοίμ. Θεοτόκου|2232031581
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Περιβόλιον Δομοκοῦ-Ἅγ.Κων/νος|2232093448
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Πετρωτόν - Ἁγ. Παρασκευή 95.228|2232095228,2232095214
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Πολυδένδριον - Ἅγ. Ἰωάννης|
8|https://www.imfth.gr/content/i-arhieratiki-perifereia-domokoy-xyniados|Φιλιαδῶν - Ἅγ. Γεώργιος|2232041384
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Βελεσσιῶτες-Ἁγ.Παρασκευή 22.504|2232022504,2232022715
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Ἀγραπηδιά - Κοίμ. Θεοτόκου|6977682020
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Βαρδαλῆ - Ἅγ. Γεώργιος|
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Γαβράκια - Ζωοδ. Πηγή|
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Ἐκκάρα - Ἅγ. Παντελεήμων 94.455|2232094455,2232071528
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Θαυμακός - Ἅγ. Νικόλαος|
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Μοναστήριον Νέον - Ἅγ. Γεώργιος|2232022088
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Πουρνάριον - Ἁγ. Παρασκευή 2491300631|2491300631
9|https://www.imfth.gr/content/th-arhieratiki-perifereia-thaymakoy-neoy-monastirioy|Σοφιάδες - Ἅγ. Ἰωάννης 2443081466|2443081466
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Καμένα Βοῦρλα-Ἅγ.Παντελεήμων 22.464|2235022464,2235022209
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ἁγ. Τριάς - Ἁγ. Τριάς|
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ἅγ. Κωνσταντῖνος-Ἅγ.Κων/νος 31.147|2235031147,2235033214
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ἅγ. Σεραφείμ - Ἅγ. Σεραφείμ|2235041093
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ἅγ. Χαράλαμπος - Ἅγ. Χαράλαμπος|
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ἄγναντη - Ἅγ. Ἀθανάσιος|2235022209
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ἀνάβρα Λοκρίδος - Προφ. Ἠλίας|
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Καινούριον - Κοίμ. Θεοτόκου 41.841|2235041841,2235041890
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Καλλίδρομος - Ἅγ. Κωνσταντῖνος|2235022265
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Καραβίδια - Γεν. Θεοτόκου|
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Καρυά Λοκρίδος - Ἁγ. Τριάς|2235032689
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Κόμνηνα - Ἅγ. Ἰωάννης|2235041105
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Λογγός - Ἅγ. Γεώργιος|2235032408
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Μενδενίτσα - Ἅγ. Γεώργιος|
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Μῶλος - Εἰσ. Θεοτόκου 52.455|2235052455,2235051572
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Ρεγγίνιον - Μεταμ. Σωτῆρος|2235061257
10|https://www.imfth.gr/content/i-arhieratiki-perifereia-mendenitsis-kamenon-voyrlon|Σκάρφεια - Ἅγ. Ἰωάν. Πρόδρομος|2235041253
10|https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf|Χάρμα-Κθάρα - Ἅγ. Ἰωάννης|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Μακρακώμη - Ἁγ. Τριάς 23.860|2236023860,2236022041
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Ἅγ. Γεώργιος 23.296|2236023296
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Ἅγ. Γεώργιος Τυμφρ. - Ἅγ. Γεώργιος|2236031300
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Ἀρχάνιον - Ἅγ. Ἀθανάσιος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Ἀσβέστιον - Γεν. Θεοτόκου|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Βίτωλη - Ζωοδ. Πηγή|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Γιαννιτσοῦ Νέα - Ἅγ. Ἰωάννης|2236031008
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Γιαννιτσοῦ Παλαιά - Ἅγ. Ἰωάννης|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Γραμμένη - Ἅγ. Νικόλαος|2236051081
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Δίκαστρον - Ἅγ. Γεώργιος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Καστρί - Ἅγ. Γεώργιος 51562|2236051562,2236051287
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Κάψη Μεγάλη - Ἁγ. Τριάς|2236031976
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Κάψη Μεσαία - Ἅγ. Δημήτριος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Λυτόσελον - Ἅγ. Γεώργιος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Μάκρη - Ἅγ. Ἀθανάσιος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Μαυρίλλον -Ἅγ. Δημήτριος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Μερκάς - Ἅγ. Παρασκευή|2236031942
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Μεσοχώριον (Πάπα) - Ἅγ. Νικόλαος|2236023631
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Νεοχωράκιον - Ἅγ. Κων/νος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Νεοχώριον Τυμφρ. - Κοίμ. Θεοτόκου|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Παλαιόκαστρον - Κοίμ. Θεοτόκου|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Περίβλεπτον - Κοίμ. Θεοτόκου|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Πιτσιωτά - Παμμ. Ταξιάρχαι|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Πλατύστομον - Ἁγ. Παρασκευή|2236023078
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Πτελέα - Ἅγ. Νικόλαος|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Ροβολιάριον - Ἅγ. Ἀπόστολοι|
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Τσούκα - Ἅγ. Γεώργιος|2236023134
11|https://www.imfth.gr/content/ia-arhieratiki-perifereia-makrakomis-tymfristoy|Τυμφρηστός - Ἅγ. Ἀθαν. 91341|2236091341,6995191878
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Σπερχειάς - Ἅγ. Νικόλαος 44.311|2236044311,2236043009
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Ἅγ. Δημήτριος 44.024|2236044024,2236044937
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Ἁγ. Παρασκευή 44.360|2236044360,2236044928
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Ἀνατολή - Ἅγ. Νικόλαος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Ἀργύρια - Ἅγ. Νικόλαος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Ἅγ. Σώστης - Ἅγ. Νικόλαος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Γαρδίκιον - Κοίμ. Θεοτόκου|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Δίλοφον - Ἅγ. Νικόλαος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Καλλιθέα Ἄνω - Ἅγ. Ἀθανάσιος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Καλλιθέα Κάτω - Ἅγ. Γεώργιος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Καμπιά - Ἅγ. Κων/νος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Κανάλλια - Ἅγ. Ἀθανάσιος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Κλωνίον - Ἅγ. Νικόλαος|2236022218
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Κολοκυθιᾶ - Κοίμ. Θεοτόκου|2236045124
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Κουτσούφλιανη - Ἅγ. Ἀπόστολοι|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Κυριακοχώριον - Ἅγ. Νικόλαος|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Λευκάδα Σπερχ. - Ἅγ. Νικόλαος|2236092708
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Μάρμαρα - Παμμ. Ταξιάρχαι|2236024929
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Μεσοποταμία - Ἅγ. Νικόλαος|2236044750
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Νικολίτσιον - Κοίμ. Θεοτόκου|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Παλαιοβράχα - Κοίμ. Θεοτόκου|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Παλαιοχώριον - Προφ. Ἠλίας|
12|https://www.imfth.gr/content/iv-arhieratiki-perifereia-sperheiados-gardikioy|Περιβόλιον Ὀμιλαίων - Γενέσ.Θεοτόκου|
12|https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf|Πίτσιον - Ἅγ. Ἀπόστολοι|
12|https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf|Πλάτανος - Ἅγ. Ἰωάννης|
12|https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf|Πουγκάκια - Κοίμ. Θεοτόκου|
12|https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf|Φτέρη - Ἅγ. Γεώργιος|
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Στυλίς - Ἅγ. Ἀθανάσιος 22.450|2238022450,2238023441,2238022416
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Ἁγ. Αἰκατερίνη 22.397|2238022397,6934649790
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Μεταμ. Σωτῆρος - Μαρίνι|
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Ἁγ. Μαρίνα Φθιώτ.-Ἁγ.Μαρίνα|2238041624
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Ἄνυδρον - Ἅγ. Δημήτριος|2238041631
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Αὐλάκιον - Ἅγ. Βλάσιος 22.957|2238022957,2238022270
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Ἀχινός - Ἁγ. Αἰκατερίνη 41.237|2238041237,2238031450
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Καραβόμυλος - Ἅγ. Ἀνάργυροι|2238041483
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Κουβέλλα - Ἅγ. Ἰωάννης|
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Λιμογάρδιον - Ἁγ. Εἰρήνη|
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Λογγίτσιον - Μεταμ. Σωτῆρος|
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Νεράιδα - Ἁγ. Παρασκευή|2238023414
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Παλαιοκερασιά - Μεταμ. Σωτῆρος|2238024577
13|https://www.imfth.gr/content/ig-arhieratiki-perifereia-stylidos|Παλαιοχώριον - Ἅγ. Γεώργιος|
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Πελασγία - Ἅγ. Ἀπόστολοι 51.000|2238051000,2238071355
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Ἀχλάδιον - Ἅγ. Παντελεήμων|2238031160
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Βαθύκοιλον - Κοίμ. Θεοτόκου|2238031727
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Γλύφα - Ἅγ. Ἀνάργυροι|2238061264
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Κυπαρισσών - Ἅγ. Ἰωάννης|
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Μῦλοι - Ἅγ. Ἀθανάσιος|2238051390
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Ράχες - Ἅγ. Χαράλαμπος 32.069|2238032069,2238031484
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Ράχες Παραλία-Ἅγ.Γρηγόριος|
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Σπαρτιά Ἄνω - Κοίμ. Θεοτόκου|
14|https://www.imfth.gr/content/id-arhieratiki-perifereia-pelasgias|Σπαρτιά Νέα - Ὅσ. Σεραφείμ|2238071330
'''

# Current official monastery title | current first-party detail page |
# English seat
MONASTERY_SOURCE = r'''
Κοιμήσεως τῆς Θεοτόκου Ἀγάθωνος|https://www.imfth.gr/content/koimiseos-tes-theotokoy-agathonos|Agathon
Μεταμορφώσεως του Σωτῆρος Καμένων Βούρλων|https://www.imfth.gr/content/metamorfoseos-toy-soteros-kamenon-voyrlon|Kamena Vourla
Γενεσίου τῆς Θεοτόκου Δαμάστας|https://www.imfth.gr/content/genesioy-tes-theotokoy-damastas|Damasta
Γενεσίου τῆς Θεοτόκου Δαδίου Ἀμφικλείας|https://www.imfth.gr/content/genesioy-tes-theotokoy-dadioy-amfikleias|Dadi, Amfikleia
Ἁγίου Γεωργίου Μαλεσσίνης|https://www.imfth.gr/content/agioy-georgioy-malessinis|Malessina
Μεταμορφώσεως του Σωτῆρος Λιβανατῶν|https://www.imfth.gr/content/metamorfoseos-toy-soteros-livanaton|Livanates
Ἁγίου Γεωργίου Μύλων|https://www.imfth.gr/content/agioy-georgioy-mylon|Myloi
Κοιμήσεως της Θεοτόκου Ἁγίας Μαρίνης Λοκρίδος|https://www.imfth.gr/content/koimiseos-tis-theotokoy-agias-marinis-lokridos|Agia Marina, Lokrida
Ἁγίας Παρασκευῆς Σπαρτιᾶς|https://www.imfth.gr/content/agias-paraskeyes-spartias|Spartia
Ἁγίων Ἀναργύρων Ἀταλάντης|https://www.imfth.gr/content/agion-anargyron-atalantis|Atalanti
Ἁγίας Τριάδος Μελιταίας|https://www.imfth.gr/content/agias-triados-melitaias|Melitaia
Ἁγίου Ἀθανασίου Ὀμβριακῆς|https://www.imfth.gr/content/agioy-athanasioy-omvriakes|Omvriaki
Ἁγίου Βλασίου Στυλίδος|https://www.imfth.gr/content/agioy-vlasioy-stylidos|Stylida
Παναγίας Φανερωμένης Ξυνιάδος|https://www.imfth.gr/content/panagias-faneromenis-xyniados|Xyniada
Γενεσίου τῆς Θεοτόκου Ἀντινίτσης|https://www.imfth.gr/content/genesioy-tes-theotokoy-antinitsis|Antinitsa
Ἁγίου Γεωργίου Νεράιδας Στυλίδος|https://www.imfth.gr/content/agioy-georgioy-neraidas-stylidos|Neraida, Stylida
Ἅγίου Νικολάου Δίβρης|https://www.imfth.gr/content/agioy-nikolaoy-divris|Divri
Ἁγίας Τριάδος Τραγάνας|https://www.imfth.gr/content/agias-triados-traganas|Tragana
Προφήτου Ἠλιού Ζελίου|https://www.imfth.gr/content/profitoy-elioy-zelioy|Zelio
'''

# Current first-party title | English name | English seat | source location |
# body-associated public phones. The page publishes responsible clergy, but
# their names and role labels are deliberately not retained here.
CHAPEL_SOURCE = r'''
Εὐαγγελιστρίας Μητροπολιτικοῦ Μεγάρου|Annunciation of the Theotokos Metropolitan Chapel at the Metropolitan Residence, Lamia|Lamia|Metropolitan Residence, Lamia|
Ἁγίου Ἐφραίμ Πνευματικοῦ Διοικητικοῦ Κέντρου|Saint Ephraim Metropolitan Chapel at the Spiritual and Administrative Center, Lamia|Lamia|Spiritual and Administrative Center, Lamia|2232050553
Ἁγίου Παντελεήμονος Γηροκομείου Λαμίας|Saint Panteleimon Metropolitan Chapel at the Care Home, Lamia|Lamia|Care Home, Lamia|2231022043
Ἁγίου Ἀθανασίου Γηροκομείου Σπερχειάδος|Saint Athanasius Metropolitan Chapel at the Care Home, Spercheiada|Spercheiada|Care Home, Spercheiada|2236043200
Ἁγίας Αἰκατερίνης Κατασκηνώσεων στό Καινούριο Καμένων Βούρλων|Saint Catherine Metropolitan Chapel at the Camps, Kainourio, Kamena Vourla|Kainourio, Kamena Vourla|Camps, Kainourio, Kamena Vourla|2235041375
Ἁγίας Ζώνης Κέδρου|Holy Cincture Metropolitan Chapel, Kedros|Kedros|Kedros|
Ἁγίου Φιλίππου Σιδ. Σταθμοῦ Λιανοκλαδίου|Saint Philip Metropolitan Chapel at Lianokladi Railway Station|Lianokladi|Lianokladi Railway Station|
Ἁγίου Παϊσίου Μακρακώμης|Saint Paisios Metropolitan Chapel, Makrakomi|Makrakomi|Makrakomi|
Ἁγίας Ἐρμιόνης Γηροκομείου Στυλίδος|Saint Hermione Metropolitan Chapel at the Care Home, Stylida|Stylida|Care Home, Stylida|
'''

TRANSLITERATION = str.maketrans({
    "Α": "A", "Β": "V", "Γ": "G", "Δ": "D", "Ε": "E", "Ζ": "Z",
    "Η": "I", "Θ": "Th", "Ι": "I", "Κ": "K", "Λ": "L", "Μ": "M",
    "Ν": "N", "Ξ": "X", "Ο": "O", "Π": "P", "Ρ": "R", "Σ": "S",
    "Τ": "T", "Υ": "Y", "Φ": "F", "Χ": "Ch", "Ψ": "Ps", "Ω": "O",
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e", "ζ": "z",
    "η": "i", "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m",
    "ν": "n", "ξ": "x", "ο": "o", "π": "p", "ρ": "r", "ς": "s",
    "σ": "s", "τ": "t", "υ": "y", "φ": "f", "χ": "ch",
    "ψ": "ps", "ω": "o",
})

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imfth.gr",
    "www.imfth.gr",
}
EXPECTED_TOTAL = 276
EXPECTED_KINDS = {"monastery": 19, "parish": 257}
EXPECTED_RANKS = {
    "Metropolitan Cathedral": 1,
    "Metropolitan Chapel": 9,
    "Monastery": 19,
    "Parish Church": 246,
    "Pilgrimage Church": 1,
}
EXPECTED_PHONE_BODIES = 144
EXPECTED_PHONE_VALUES = 207


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def transliterate(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    for greek, latin in (
            ("ΟΥ", "OU"), ("ου", "ou"), ("ΑΙ", "AI"), ("αι", "ai"),
            ("ΕΙ", "EI"), ("ει", "ei"), ("ΟΙ", "OI"), ("οι", "oi"),
            ("ΜΠ", "B"), ("μπ", "b"), ("ΝΤ", "D"), ("ντ", "d"),
            ("ΓΚ", "G"), ("γκ", "g"), ("ΤΣ", "TS"), ("τσ", "ts"),
            ("ΤΖ", "TZ"), ("τζ", "tz")):
        value = value.replace(greek, latin)
    value = value.translate(TRANSLITERATION)
    value = re.sub(r"[^A-Za-z0-9]+", " ", value).strip()
    return " ".join(word.capitalize() for word in value.split()) or "Fthiotis"


def normalize_greek(value):
    return re.sub(r"[^A-ZΑ-Ω]+", " ", unicase(value).upper()).strip()


def strip_phone_text(value):
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = re.sub(r"\s*(?:\d{2}\.\d{3}|\d{5})(?:\([^)]*\))?.*$", "", value)
    return " ".join(value.strip(" .").split())


def looks_like_dedication(value):
    normalized = normalize_greek(value)
    starts = (
        "ΑΓ ", "ΑΓΙ", "ΟΣ ", "ΚΟΙΜ", "ΕΙΣ", "ΕΥΑΓΓ",
        "ΓΕΝ", "ΜΕΤΑΜ", "ΖΩΟΔ", "ΠΑΜΜ", "ΠΑΝΑΓΙΑ",
        "ΠΡΟΦ",
    )
    return normalized.startswith(starts)


def dedication_name(value):
    normalized = normalize_greek(value)
    rules = (
        (("ΠΕΤΡ", "ΠΑΥΛ"), "Saints Peter and Paul"),
        (("ΙΩΑΝ", "ΠΡΟΔΡ"), "Saint John the Forerunner"),
        (("ΚΟΙΜ", "ΘΕΟΤΟΚ"), "the Dormition of the Theotokos"),
        (("ΕΥΑΓΓ", "ΘΕΟΤΟΚ"), "the Annunciation of the Theotokos"),
        (("ΕΙΣ", "ΘΕΟΤΟΚ"), "the Entrance of the Theotokos"),
        (("ΓΕΝ", "ΘΕΟΤΟΚ"), "the Nativity of the Theotokos"),
        (("ΜΕΤΑΜ", "ΣΩΤ"), "the Transfiguration of the Savior"),
        (("ΖΩΟΔ", "ΠΗΓ"), "the Life-Giving Spring"),
        (("ΠΑΜΜ", "ΤΑΞ"), "Holy Archangels"),
        (("ΑΝΑΡΓΥΡ",), "Holy Unmercenaries"),
        (("ΑΠΟΣΤΟΛ",), "Holy Apostles"),
        (("ΤΡΙΑ",), "Holy Trinity"),
        (("ΠΡΟΦ", "ΗΛΙ"), "Prophet Elijah"),
        (("ΠΑΡΑΣΚΕΥ",), "Saint Paraskevi"),
        (("ΠΑΝΤΕΛΕ",), "Saint Panteleimon"),
        (("ΧΑΡΑΛΑΜΠ",), "Saint Charalampus"),
        (("ΑΘΑΝ",), "Saint Athanasius"),
        (("ΔΗΜΗΤΡ",), "Saint Demetrius"),
        (("ΓΕΩΡΓ",), "Saint George"),
        (("ΝΙΚΟΛΑ",), "Saint Nicholas"),
        (("ΚΩΝ", "ΝΟΣ"), "Saint Constantine"),
        (("ΚΩΝΣΤΑΝΤ",), "Saint Constantine"),
        (("ΑΙΚΑΤΕΡ",), "Saint Catherine"),
        (("ΒΑΡΒΑΡ",), "Saint Barbara"),
        (("ΙΩΑΝ",), "Saint John"),
        (("ΒΛΑΣΙ",), "Saint Blaise"),
        (("ΕΥΣΤΑΘ",), "Saint Eustathius"),
        (("ΚΥΡΙΑΚ",), "Saint Kyriaki"),
        (("ΜΑΡΙΝ",), "Saint Marina"),
        (("ΣΟΦΙ",), "Saint Sophia"),
        (("ΕΙΡΗΝ",), "Saint Irene"),
        (("ΒΑΣΙΛΕΙ",), "Saint Basil"),
        (("ΓΡΗΓΟΡ",), "Saint Gregory"),
        (("ΛΟΥΚ",), "Saint Luke"),
        (("ΝΕΚΤΑΡ",), "Saint Nectarius"),
        (("ΚΟΣΜ",), "Saint Cosmas"),
        (("ΘΕΟΔΩΡ",), "Holy Theodores"),
        (("ΣΤΕΦΑΝ",), "Saint Stephen"),
        (("ΟΣ", "ΣΕΡΑΦΕΙΜ"), "Venerable Seraphim"),
        (("ΣΕΡΑΦΕΙΜ",), "Saint Seraphim"),
        (("ΠΑΝΑΓΙΑ", "ΔΕΣΠΟΙΝ"), "Panagia Despoina"),
        (("ΠΑΝΑΓΙΑ", "ΦΑΝΕΡΩΜ"), "Panagia Phaneromene"),
    )
    for required, english in rules:
        if all(token in normalized for token in required):
            return english
    return transliterate(value)


def parish_parts(region, local):
    local = strip_phone_text(local)
    if "-" not in local:
        return REGION_DEFAULTS[region], dedication_name(local), local
    left, right = [value.strip() for value in local.rsplit("-", 1)]
    if looks_like_dedication(left) and not looks_like_dedication(right):
        left, right = right, left
    return transliterate(left), dedication_name(right), local


def parse_phones(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def build_rows():
    rows = []
    live_checks = defaultdict(set)
    parish_lines = PARISH_SOURCE.strip().splitlines()
    if len(parish_lines) != 247:
        raise ValueError("expected 247 parish source rows")
    for number, raw in enumerate(parish_lines, 1):
        region_text, source_url, raw_local, phone_text = raw.split("|", 3)
        region = int(region_text)
        seat, dedication, local = parish_parts(region, raw_local)
        rank = "Metropolitan Cathedral" if number == 1 else "Parish Church"
        sources = [OFFICIAL_PDF]
        if source_url != OFFICIAL_PDF:
            sources.append(source_url)
            live_checks[source_url].add(local)
        row = {
            "id": "gr-fthiotis-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": PARISH_NAME_OVERRIDES.get(
                number,
                "%s of %s, %s" % (
                    "Metropolitan Cathedral" if number == 1 else "Parish Church",
                    dedication,
                    seat,
                ),
            ),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": sources,
            "checked": CHECKED,
        }
        phones = parse_phones(phone_text)
        if phones:
            row["phones"] = phones
            row["contact_sources"] = [source_url]
            row["contact_checked"] = CHECKED
        rows.append(row)

    for offset, raw in enumerate(MONASTERY_SOURCE.strip().splitlines(), 248):
        local, source_url, seat = raw.split("|", 2)
        dedication = dedication_name(local)
        live_checks[source_url].add(local)
        rows.append({
            "id": "gr-fthiotis-%03d" % offset,
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": "Monastery of %s, %s" % (dedication, seat),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [MONASTERY_INDEX, source_url],
            "checked": CHECKED,
        })

    rows.append({
        "id": "gr-fthiotis-267",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Pilgrimage Church",
        "name": "Pilgrimage Church of Panagia Prousiotissa, Vardates",
        "local": "Ιερός Προσκυνηματικός Ναός Παναγίας Προυσιωτίσσης Βαρδατών",
        "seat": "Vardates",
        "country": "GR",
        "address": ["Vardates", "Greece"],
        "sources": [OFFICIAL_PDF],
        "checked": CHECKED,
    })

    for number, raw in enumerate(CHAPEL_SOURCE.strip().splitlines(), 268):
        local, name, seat, address, phone_text = raw.split("|", 4)
        live_checks[CHAPEL_PAGE].add(local)
        row = {
            "id": "gr-fthiotis-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": "Metropolitan Chapel",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": [CHAPEL_PAGE],
            "checked": CHECKED,
        }
        phones = parse_phones(phone_text)
        if phones:
            row["phones"] = phones
            row["contact_sources"] = [CHAPEL_PAGE]
            row["contact_checked"] = CHECKED
        rows.append(row)
    return rows, live_checks


ROWS, LIVE_CHECKS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


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
        raise ValueError("Fthiotis candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Fthiotis candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "regulated_parish_rows": 247,
        "regulated_pilgrimage_rows": 1,
        "active_monastery_rows": 19,
        "current_metropolitan_chapel_rows": 9,
        "parish_kind_rows": 257,
        "monastery_kind_rows": 19,
        "contact_bodies": EXPECTED_PHONE_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": EXPECTED_TOTAL,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Fthiotis ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Fthiotis ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Fthiotis ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    for source in ROWS:
        item = {key: value for key, value in source.items()
                if value not in (None, "", [])}
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
                if not re.fullmatch(r"[26]\d{9}", phone):
                    raise ValueError("%s carries an invalid phone" % row_id)
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
        raise ValueError("Fthiotis English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Fthiotis rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Fthiotis kind totals drifted: %r" % dict(kinds))
    phone_bodies = sum(bool(item.get("phones")) for item in result)
    phone_values = sum(len(item.get("phones") or []) for item in result)
    if (phone_bodies, phone_values) != (
            EXPECTED_PHONE_BODIES, EXPECTED_PHONE_VALUES):
        raise ValueError("Fthiotis contact coverage drifted")
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    }
    if url == OFFICIAL_PDF:
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=90) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return unicase(" ".join(text.split()))


def check_live():
    checks = dict(LIVE_CHECKS)
    checks[REGION_INDEX] = {"Αρχιερατικές Περιφέρειες"}
    checks[MONASTERY_INDEX] = {"Ιερές Μονές", "Σύνολο : 21"}
    checks[OFFICIAL_PDF] = set()

    def one(item):
        url, markers = item
        payload, content_type = fetch(url)
        if url == OFFICIAL_PDF:
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("Fthiotis regulation is not a PDF")
            return url
        if "html" not in content_type:
            raise ValueError("non-HTML Fthiotis source: %s" % url)
        page = normalized_page(payload)
        missing = [marker for marker in markers
                   if unicase(" ".join(marker.split())) not in page]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        return url

    with ThreadPoolExecutor(max_workers=10) as executor:
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
            print("Fthiotis live checks passed for %d source pages" % checked)
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Fthiotis checks passed: %d bodies, %d phone bodies, "
                "%d public phone values" % (
                    len(rows),
                    sum(bool(item.get("phones")) for item in rows),
                    sum(len(item.get("phones") or []) for item in rows),
                )
            )
    except Exception as exc:
        print("Fthiotis check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
