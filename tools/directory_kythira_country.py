#!/usr/bin/env python3
"""Build the exact current Kythira and Antikythira body roster."""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PARENT = "gr-kythira"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "kythira_country.json"

LOCAL_BASE = "https://www.imkythiron.gr"
ROSTER_URL = LOCAL_BASE + "/index.php/el/organosis-dioikisis-leitourgia-i-mitr-kythiron-antikythiron"
MONUMENTS_URL = LOCAL_BASE + "/index.php/el/ekklisiastika-mnimeia/perispoudasta-ekklisiastika-mnimeia-2"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2019_februarios.pdf"
RENAME_URL = "https://www.ecclesia.gr/greek/press/ekklisia/2019_decembrios.pdf"
PROGRAM_BASE = LOCAL_BASE + "/index.php/el/eidiseis/programmata-sevasmiotatou-mitropoliti/"
JAN_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-a-15nthimeron-ianouariou-2026"
JAN_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-v-15nthimeron-ianouariou-2026"
FEB_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-a-15nthimeron-fevrouariou-2026"
FEB_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-v-15nthimeron-fevrouariou-2027"
MAR_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-a-15nthimeron-martiou-2027"
MAR_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-v-15nthimeron-martiou-2026"
APR_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-a-15nthimeron-apriliou-2026"
APR_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-v-15nthimeron-apriliou-2026"
MAY_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-a-15nthimeron-maiou-2026"
MAY_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-v-15nthimeron-maiou-2026"
JUN_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-a-15nthimeron-iouniou-2026"
JUN_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-b-15nthimeron-iouniou-2026"
JULY = PROGRAM_BASE + "programma-sev-mitr-kythiron-ioulios-2026"
AUGUST = PROGRAM_BASE + "programma-sev-mitr-kythiron-avgoustos-2026"
SEPTEMBER = PROGRAM_BASE + "programma-sev-mitr-kythiron-antikythiron-serafeim-septemvrios-2026"
OCT_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-antikythiron-serafeim-v-15nthimeron-oktovriou-2026"
NOV_A = PROGRAM_BASE + "programma-sev-mitr-kythiron-antikythiron-serafeim-a-15nthimeron-noemvriou-2026"
NOV_B = PROGRAM_BASE + "programma-sev-mitr-kythiron-antikythiron-serafeim-v-15nthimeron-noemvriou-2026"
FORTY_LITURGIES_URL = LOCAL_BASE + "/images/stories/pdf/2026/programma_sarantaleitourgou_16-31.10.2026.pdf"


PARISH_SOURCE = r"""
Chora|Χώρα|Crucified Christ|Ἐσταυρωμένου Χριστοῦ|Metropolitan Cathedral|+30 6984805577
Agios Ilias|Ἅγιος Ἠλίας|Prophet Elijah|Προφήτου Ἠλιού|Parish Church|+30 27360-31015
Agia Pelagia|Ἁγία Πελαγία|Venerable Pelagia|Ὁσίας Πελαγίας|Parish Church|+30 6972096996
Alexandrades|Ἀλεξανδράδες|Holy Trinity|Ἁγίας Τριάδος|Parish Church|+30 6938366731
Aloizianika|Ἀλοϊζιάνικα|Saint Basil|Ἁγίου Βασιλείου|Parish Church|+30 27360-33483
Aroniadika|Ἀρωνιάδικα|Transfiguration of Christ|Μεταμορφώσεως τοῦ Χριστοῦ|Parish Church|+30 27360-33231
Avlemon|Αὐλέμων|Saint Nicholas|Ἁγίου Νικολάου|Parish Church|+30 6977616194
Viaradika|Βιαράδικα|Entrance of the Theotokos|Εἰσοδίων τῆς Θεοτόκου|Parish Church|+30 6945147286
Drymon|Δρυμών|Saint Marina|Ἁγίας Μαρίνης|Parish Church|+30 6977695632
Kalamos|Κάλαμος|Saint Nikitas|Ἁγίου Νικήτα|Parish Church|+30 27360-33183
Kalisperianika|Καλησπεριάνικα|Saint George|Ἁγίου Γεωργίου|Parish Church|+30 27360-33856
Kalokairines|Καλοκαιρινές|Saint Spyridon|Ἁγίου Σπυρίδωνος|Parish Church|+30 6938366731
Karavas|Καραβᾶς|Saint Charalambos|Ἁγίου Χαραλάμπους|Parish Church|+30 27360-33548
Karvounades|Καρβουνᾶδες|Saint George|Ἁγίου Γεωργίου|Parish Church|+30 6938366731
Kastrisianika|Καστρισιάνικα|Saint Anthony|Ἁγίου Ἀντωνίου|Parish Church|+30 6945147286
Katouni|Κατούνι|Saint Irene|Ἁγίας Εἰρήνης|Parish Church|+30 6938366731
Kato Leivadi|Κάτω Λειβάδι|Ascension of the Savior|Ἀναλήψεως τοῦ Σωτῆρος|Parish Church|+30 27360-31015;+30 6977695632
Keramoto|Κεραμωτό|Transfiguration of Christ|Μεταμορφώσεως τοῦ Χριστοῦ|Parish Church|+30 6938366731
Leivadi|Λειβάδι|Dormition of the Theotokos|Κοιμήσεως τῆς Θεοτόκου|Parish Church|+30 6977695632;+30 27360-31015
Mitata|Μητᾶτα|Holy Trinity|Ἁγίας Τριάδος|Parish Church|+30 6977616194
Logothetianika|Λογοθετιάνικα|Saint Menas|Ἁγίου Μηνᾶ|Parish Church|+30 27360-33548
Mylopotamos|Μυλοπόταμος|Saint Charalambos|Ἁγίου Χαραλάμπους|Parish Church|+30 27360-33673
Pitsinianika|Πιτσινιάνικα|Crucified Christ|Ἐσταυρωμένου Χριστοῦ|Parish Church|+30 27360-33856
Potamos|Ποταμός|Life-giving Spring|Ζωοδόχου Πηγῆς|Parish Church|+30 6994327599
Pourkon|Ποῦρκον|Saint Elesa|Ἁγίας Ἐλέσης|Parish Church|+30 27360-33856
Strapodi|Στραπόδι|Saint John the Forerunner|Τιμίου Προδρόμου|Parish Church|+30 6984805577
Fatsadika|Φατσάδικα|Holy Unmercenaries|Ἁγίων Ἀναργύρων|Parish Church|+30 27360-31015
Fratsia|Φράτσια|Dormition of the Theotokos and Saint Charalambos|Κοιμήσεως τῆς Θεοτόκου καί Ἁγίου Χαραλάμπους|Parish Church|+30 6977292317
Frilingkianika|Φριλιγκιάνικα|Entrance of the Theotokos|Εἰσοδίων τῆς Θεοτόκου|Parish Church|+30 6945147286
Antikythira|Ἀντικύθηρα|Saint Myron|Ἁγίου Μύρωνος|Parish Church|
"""


PILGRIMAGES = [
    ("myrtidiotissa", "Panagia Myrtidiotissa Pilgrimage", "Ἱερόν Προσκύνημα Παναγίας Μυρτιδιωτίσσης", "Myrtidia", "Μυρτίδια Κυθήρων", ["+30 27360-31184"]),
    ("agia-moni", "Agia Moni Pilgrimage", "Ἱερόν Προσκύνημα Ἁγίας Μόνης", "Agia Moni", "Ἁγία Μόνη Κυθήρων", ["+30 27360-31184", "+30 6977616194"]),
    ("panagia-despoina", "Panagia Despoina Pilgrimage in Karavas", "Ἱερόν Προσκύνημα Παναγίας Δέσποινας Καραβᾶ", "Karavas", "Καραβᾶς Κυθήρων", ["+30 27360-33548"]),
    ("unmercenaries-xeroulaki", "Holy Unmercenaries Pilgrimage at Xeroulaki", "Ἱερόν Προσκύνημα Ἁγίων Ἀναργύρων Ξερουλάκι", "Xeroulaki", "Ξερουλάκι Κυθήρων", ["+30 27360-31015"]),
]


MONASTERY = (
    "theodore", "Venerable Theodore Monastery", "Ἱερά Μονή Ὁσίου Θεοδώρου",
    "Kythira", "Κύθηρα", ["+30 27360-33673"],
)


ADDITIONAL_SOURCE = [
    ("peter-araioi", "Holy Apostle Peter Church in Araioi", "Ἱερός Ναός Ἁγίου Ἀποστόλου Πέτρου Ἀραίων", "Araioi", "Ἄραιοι Κυθήρων", "Church", "parish", ROSTER_URL),
    ("demetrius-pourkon", "Saint Demetrius Church in Pourkon", "Ἱερός Ναός Ἁγίου Δημητρίου Πούρκου", "Pourkon", "Ποῦρκον Κυθήρων", "Church", "parish", ROSTER_URL),
    ("andrew-ano-leivadi", "Holy Apostle Andrew Church in Ano Leivadi", "Ἱερός Ναός Ἁγίου Ἀποστόλου Ἀνδρέου τοῦ Πρωτοκλήτου Ἄνω Λιβαδίου", "Ano Leivadi", "Ἄνω Λειβάδι Κυθήρων", "Church", "parish", NOV_B),
    ("unmercenaries-frilingkianika", "Holy Unmercenaries Church in Frilingkianika", "Ἱερός Ναός Ἁγίων Ἀναργύρων Φριλιγκιανίκων", "Frilingkianika", "Φριλιγκιάνικα Κυθήρων", "Church", "parish", JULY),
    ("nikon-potamos", "Saint Nikon Church in Potamos", "Ἱερός Ναός Ἁγίου Νίκωνος Ποταμοῦ", "Potamos", "Ποταμός Κυθήρων", "Church", "parish", ROSTER_URL),
    ("anthony-drymon", "Saint Anthony Church in Drymon", "Ἱερός Ναός Ἁγίου Ἀντωνίου Δρυμῶνος", "Drymon", "Δρυμών Κυθήρων", "Church", "parish", JAN_B),
    ("athanasius-pitsinades", "Saint Athanasius Church in Pitsinades", "Ἱερός Ναός Ἁγίου Ἀθανασίου Πιτσινάδων", "Pitsinades", "Πιτσινάδες Κυθήρων", "Church", "parish", JAN_B),
    ("eustathius-stathianika", "Saint Eustathius Church in Stathianika", "Ἱερός Ναός Ἁγίου Εὐσταθίου Σταθιανίκων", "Stathianika", "Σταθιάνικα Κυθήρων", "Church", "parish", JAN_B),
    ("three-hierarchs-chora", "Three Hierarchs Chapel in Chora", "Ἱερόν Παρεκκλήσιον Ἁγίων Τριῶν Ἱεραρχῶν Χώρας", "Chora", "Χώρα Κυθήρων", "Chapel", "parish", JAN_B),
    ("panagia-kera-leivadi", "Panagia Kera Church in Leivadi", "Ἱερός Ναός Παναγίας Κερᾶς Λιβαδίου", "Leivadi", "Λειβάδι Κυθήρων", "Church", "parish", FEB_A),
    ("meeting-kaki-melissa", "Meeting of the Lord Chapel at Kaki Melissa", "Ἱερόν Παρεκκλήσιον Ὑπαπαντῆς τοῦ Χριστοῦ Κακῆς Μέλισσας", "Kaki Melissa", "Κακή Μέλισσα Κυθήρων", "Chapel", "parish", FEB_A),
    ("blaise-kastrisianika", "Saint Blaise Chapel in Kastrisianika", "Ἱερόν Παρεκκλήσιον Ἁγίου Βλασίου Καστρισιανίκων", "Kastrisianika", "Καστρισιάνικα Κυθήρων", "Chapel", "parish", FEB_A),
    ("leo-alexandrades", "Saint Leo Pope of Rome Chapel in Alexandrades", "Ἱερόν Παρεκκλήσιον Ἁγίου Λέοντος Πάπα Ρώμης Ἀλεξανδράδων", "Alexandrades", "Ἀλεξανδράδες Κυθήρων", "Chapel", "parish", FEB_B),
    ("charalambos-potamos-antikythira", "Saint Charalambos Church in Potamos, Antikythira", "Ἱερός Ναός Ἁγίου Χαραλάμπους Ποταμοῦ Ἀντικυθήρων", "Potamos, Antikythira", "Ποταμός Ἀντικυθήρων", "Church", "parish", FEB_B),
    ("constantine-helen-pateriana", "Saints Constantine and Helen Church in Pateriana, Antikythira", "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης Πατεριανῶν Ἀντικυθήρων", "Pateriana, Antikythira", "Πατεριανά Ἀντικυθήρων", "Church", "parish", FEB_B),
    ("ilariotissa-potamos", "Panagia Ilariotissa Church in Potamos", "Ἱερός Ναός Παναγίας Ἱλαριωτίσσης Ποταμοῦ", "Potamos", "Ποταμός Κυθήρων", "Church", "parish", MAR_A),
    ("eleousa-fratsia", "Panagia Eleousa Church in Fratsia", "Ἱερός Ναός Παναγίας Ἐλεούσης Φρατσίων", "Fratsia", "Φράτσια Κυθήρων", "Church", "parish", MAR_A),
    ("menas-diakofti", "Saint Menas Church in Diakofti", "Ἱερός Ναός Ἁγίου Μηνᾶ Διακοφτίου", "Diakofti", "Διακόφτι Κυθήρων", "Church", "parish", MAR_B),
    ("george-antikythira", "Saint George Church in Antikythira", "Ἱερός Ναός Ἁγίου Γεωργίου Ἀντικυθήρων", "Antikythira", "Ἀντικύθηρα", "Church", "parish", MAR_B),
    ("constantine-antikythira", "Saint Constantine Church in Antikythira", "Ἱερός Ναός Ἁγίου Κωνσταντίνου Ἀντικυθήρων", "Antikythira", "Ἀντικύθηρα", "Church", "parish", MAR_B),
    ("nicholas-antikythira", "Saint Nicholas Church in Antikythira", "Ἱερός Ναός Ἁγίου Νικολάου Ἀντικυθήρων", "Antikythira", "Ἀντικύθηρα", "Church", "parish", MAR_B),
    ("entrance-kontolianika", "Entrance of the Theotokos Church in Kontolianika", "Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Κοντολιανίκων", "Kontolianika", "Κοντολιάνικα Κυθήρων", "Church", "parish", APR_A),
    ("kontelatous-ano-leivadi", "Panagia Kontelatous Church in Ano Leivadi", "Ἱερός Ναός Παναγίας Κοντελετοῦς Ἄνω Λιβαδίου", "Ano Leivadi", "Ἄνω Λειβάδι Κυθήρων", "Church", "parish", APR_A),
    ("george-mitata", "Saint George Church in Mitata", "Ἱερός Ναός Ἁγίου Γεωργίου Μητάτων", "Mitata", "Μητᾶτα Κυθήρων", "Church", "parish", APR_A),
    ("john-theologian-chora", "Saint John the Theologian Church in Chora", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Χώρας", "Chora", "Χώρα Κυθήρων", "Church", "parish", MAY_A),
    ("john-theologian-leivadi", "Saint John the Theologian Church in Leivadi", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Λιβαδίου", "Leivadi", "Λειβάδι Κυθήρων", "Church", "parish", MAY_A),
    ("nicholas-alones-fratsia", "Saint Nicholas Chapel at Alones in Fratsia", "Ἱερόν Παρεκκλήσιον Ἁγίου Νικολάου Ἁλῶνες Φρατσίων", "Alones, Fratsia", "Ἁλῶνες Φρατσίων Κυθήρων", "Chapel", "parish", MAY_B),
    ("constantine-helen-ano-leivadi", "Saints Constantine and Helen Chapel in Ano Leivadi", "Ἱερόν Παρεκκλήσιον Ἁγίων Κωνσταντίνου καί Ἑλένης Ἄνω Λιβαδίου", "Ano Leivadi", "Ἄνω Λειβάδι Κυθήρων", "Chapel", "parish", JULY),
    ("constantine-potamos", "Saint Constantine Church in Potamos", "Ἱερός Ναός Ἁγίου Κωνσταντίνου Ποταμοῦ", "Potamos", "Ποταμός Κυθήρων", "Church", "parish", MAY_B),
    ("john-alexandrades", "Saint John Church in Alexandrades", "Ἱερός Ναός Ἁγίου Ἰωάννου Ἀλεξανδράδων", "Alexandrades", "Ἀλεξανδράδες Κυθήρων", "Church", "parish", MAY_B),
    ("myrtidiotissa-castle", "Panagia Myrtidiotissa Church at the Castle of Chora", "Ἱερός Ναός Παναγίας Μυρτιδιωτίσσης Κάστρου Χώρας", "Castle of Chora", "Κάστρο Χώρας Κυθήρων", "Church", "parish", MAY_B),
    ("hodegetria-kalamos", "Panagia Hodegetria Church in Kalamos", "Ἱερός Ναός Παναγίας Ὁδηγητρίας Καλάμου", "Kalamos", "Κάλαμος Κυθήρων", "Church", "parish", MAY_B),
    ("trinity-logothetianika", "Holy Trinity Church in Logothetianika", "Ἱερός Ναός Ἁγίας Τριάδος Λογοθετιανίκων", "Logothetianika", "Λογοθετιάνικα Κυθήρων", "Church", "parish", MAY_B),
    ("trinity-frilingkianika", "Holy Trinity Church in Frilingkianika", "Ἱερός Ναός Ἁγίας Τριάδος Φριλιγκιανίκων", "Frilingkianika", "Φριλιγκιάνικα Κυθήρων", "Church", "parish", JUN_A),
    ("trinity-araioi", "Holy Trinity Church in Araioi", "Ἱερός Ναός Ἁγίας Τριάδος Ἀραίων", "Araioi", "Ἄραιοι Κυθήρων", "Church", "parish", JUN_A),
    ("all-saints-goudianika", "All Saints Church in Goudianika", "Ἱερός Ναός Ἁγίων Πάντων Γουδιανίκων", "Goudianika", "Γουδιάνικα Κυθήρων", "Church", "parish", JUN_A),
    ("eleousa-chora", "Panagia Eleousa Church in Chora", "Ἱερός Ναός Παναγίας Ἐλεούσης Χώρας", "Chora", "Χώρα Κυθήρων", "Church", "parish", JUN_A),
    ("theodore-karvounades", "Saint Theodore Church in Karvounades", "Ἱερός Ναός Ἁγίου Θεοδώρου Καρβουνάδων", "Karvounades", "Καρβουνᾶδες Κυθήρων", "Church", "parish", JUN_B),
    ("forerunner-ntourianika", "Saint John the Forerunner Church in Ntourianika", "Ἱερός Ναός Ἁγίου Ἰωάννου Προδρόμου Ντουριανίκων", "Ntourianika", "Ντουριάνικα Κυθήρων", "Church", "parish", JUN_B),
    ("raphael-antikythira", "Saints Raphael, Nicholas and Irene with Venerable Athanasius the Athonite Chapel in Antikythira", "Ἱερόν Παρεκκλήσιον Ἁγίων Ραφαήλ, Νικολάου καί Εἰρήνης καί Ὁσίου Ἀθανασίου τοῦ Ἀθωνίτου Ἀντικυθήρων", "Antikythira", "Ἀντικύθηρα", "Chapel", "parish", JULY),
    ("procopius-karavas", "Saint Procopius Chapel in Karavas", "Ἱερόν Παρεκκλήσιον Ἁγίου Προκοπίου Καραβᾶ", "Karavas", "Καραβᾶς Κυθήρων", "Chapel", "parish", JULY),
    ("elijah-potamos", "Prophet Elijah Chapel in Potamos", "Ἱερόν Παρεκκλήσιον Προφήτου Ἠλιού Ποταμοῦ", "Potamos", "Ποταμός Κυθήρων", "Chapel", "parish", JULY),
    ("eleftherios-dokana", "Saint Eleftherios Church in Dokana", "Ἱερός Ναός Ἁγίου Ἐλευθερίου Δοκάνων", "Dokana", "Δόκανα Κυθήρων", "Church", "parish", AUGUST),
    ("patricia-karavas", "Saint Patricia Church in Karavas", "Ἱερός Ναός Ἁγίας Πατρικίας Καραβᾶ", "Karavas", "Καραβᾶς Κυθήρων", "Church", "parish", AUGUST),
    ("spyridon-kapsali", "Saint Spyridon Church in Kapsali", "Ἱερός Ναός Ἁγίου Σπυρίδωνος Καψαλίου", "Kapsali", "Καψάλι Κυθήρων", "Church", "parish", AUGUST),
    ("paraskevi-viaradika", "Saint Paraskevi Church in Viaradika", "Ἱερός Ναός Ἁγίας Παρασκευῆς Βιαραδίκων", "Viaradika", "Βιαράδικα Κυθήρων", "Church", "parish", AUGUST),
    ("basil-christoforianika", "Saint Basil Church in Christoforianika", "Ἱερός Ναός Ἁγίου Βασιλείου Χριστοφοριανίκων", "Christoforianika", "Χριστοφοριάνικα Κυθήρων", "Church", "parish", AUGUST),
    ("john-gerakari", "Saint John Church in Gerakari", "Ἱερός Ναός Ἁγίου Ἰωάννου Γερακαρίου", "Gerakari", "Γερακάρι Κυθήρων", "Church", "parish", AUGUST),
    ("john-cliff-kapsali", "Saint John at the Cliff Church in Kapsali", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ ἐν Κρημνῷ Καψαλίου", "Kapsali", "Καψάλι Κυθήρων", "Church", "parish", AUGUST),
    ("mamas-logothetianika", "Saint Mamas Chapel in Logothetianika", "Ἱερόν Παρεκκλήσιον Ἁγίου Μάμαντος Λογοθετιανίκων", "Logothetianika", "Λογοθετιάνικα Κυθήρων", "Chapel", "parish", SEPTEMBER),
    ("mamas-katouni", "Saint Mamas Chapel in Katouni", "Ἱερόν Παρεκκλήσιον Ἁγίου Μάμαντος Κατουνίου", "Katouni", "Κατούνι Κυθήρων", "Chapel", "parish", SEPTEMBER),
    ("sozon-mylopotamos", "Saint Sozon Church in Mylopotamos", "Ἱερός Ναός Ἁγίου Σώζοντος Μυλοποτάμου", "Mylopotamos", "Μυλοπόταμος Κυθήρων", "Church", "parish", SEPTEMBER),
    ("nativity-katafygadi", "Nativity of the Theotokos Church at Katafygadi in Pourkon", "Ἱερός Ναός Γενεσίου τῆς Θεοτόκου Καταφυγάδι Πούρκου", "Katafygadi, Pourkon", "Καταφυγάδι Πούρκου Κυθήρων", "Church", "parish", SEPTEMBER),
    ("nativity-kakopetri", "Nativity of the Theotokos Monastery at Kakopetri", "Ἱερά Μονή Γενεσίου τῆς Θεοτόκου Κακοπέτρι", "Kakopetri", "Κακοπέτρι Κυθήρων", "Monastery", "monastery", SEPTEMBER),
    ("manolitissa-fratsia", "Panagia Manolitissa Church in Fratsia", "Ἱερός Ναός Παναγίας Μανωλίτισσας Φρατσίων", "Fratsia", "Φράτσια Κυθήρων", "Church", "parish", SEPTEMBER),
    ("sophia-cave-kalamos", "Saint Sophia Cave Church at Spilies in Kalamos", "Σπηλαιώδης Ἱερός Ναός Ἁγίας Σοφίας Σπηλιές Καλάμου", "Spilies, Kalamos", "Σπηλιές Καλάμου Κυθήρων", "Cave Church", "parish", SEPTEMBER),
    ("forerunner-agriolies", "Saint John the Forerunner Monydrion at Agriolies", "Ἱερόν Μονύδριον Τιμίου Προδρόμου Ἀγριολιές", "Agriolies", "Ἀγριολιές Κυθήρων", "Monydrion", "monastery", SEPTEMBER),
    ("luke-manitochori", "Evangelist Luke Chapel in Manitochori", "Ἱερόν Παρεκκλήσιον Εὐαγγελιστοῦ Λουκᾶ Μανιτοχωρίου", "Manitochori", "Μανιτοχώρι Κυθήρων", "Chapel", "parish", OCT_B),
    ("gerasimus-potamos", "Venerable Gerasimus Chapel in Potamos", "Ἱερόν Παρεκκλήσιον Ὁσίου Γερασίμου Ποταμοῦ", "Potamos", "Ποταμός Κυθήρων", "Chapel", "parish", OCT_B),
    ("artemius-ano-strapodi", "Saint Artemius Chapel in Ano Strapodi", "Ἱερόν Παρεκκλήσιον Ἁγίου Ἀρτεμίου Ἄνω Στραποδίου", "Ano Strapodi", "Ἄνω Στραπόδι Κυθήρων", "Chapel", "parish", OCT_B),
    ("james-mesa-vourgo", "Saint James the Brother of the Lord Chapel in Mesa Vourgo", "Ἱερόν Παρεκκλήσιον Ἁγίου Ἰακώβου τοῦ Ἀδελφοθέου Μέσα Βούργου", "Mesa Vourgo", "Μέσα Βούργο Χώρας Κυθήρων", "Chapel", "parish", OCT_B),
    ("anna-chora", "Saint Anna Church in Chora", "Ἱερός Ναός Ἁγίας Ἄννης Χώρας", "Chora", "Χώρα Κυθήρων", "Church", "parish", OCT_B),
    ("demetrius-logothetianika", "Saint Demetrius Church in Logothetianika", "Ἱερός Ναός Ἁγίου Δημητρίου Λογοθετιανίκων", "Logothetianika", "Λογοθετιάνικα Κυθήρων", "Church", "parish", OCT_B),
    ("anastasia-chora", "Saint Anastasia Chapel in Chora", "Ἱερόν Παρεκκλήσιον Ἁγίας Ἀναστασίας Χώρας", "Chora", "Χώρα Κυθήρων", "Chapel", "parish", OCT_B),
    ("archangels-cemetery-karavas", "Holy Archangels Cemetery Church in Karavas", "Κοιμητηριακός Ἱερός Ναός Ἁγίων Ταξιαρχῶν Καραβᾶ", "Karavas", "Καραβᾶς Κυθήρων", "Cemetery Church", "parish", NOV_A),
    ("archangels-travasarianika", "Holy Archangels Church in Travasarianika", "Ἱερός Ναός Παμμεγίστων Ταξιαρχῶν Τραβασαριανίκων", "Travasarianika", "Τραβασαριάνικα Κυθήρων", "Church", "parish", NOV_A),
    ("menas-aroniadika", "Saint Menas Chapel in Aroniadika", "Ἱερόν Παρεκκλήσιον Ἁγίου Μηνᾶ Ἀρωνιαδίκων", "Aroniadika", "Ἀρωνιάδικα Κυθήρων", "Chapel", "parish", NOV_A),
    ("andrew-tsikalaria", "Saint Andrew Church in Tsikalaria", "Ἱερός Ναός Ἁγίου Ἀνδρέου Τσικαλαρίας", "Tsikalaria", "Τσικαλαριά Κυθήρων", "Church", "parish", NOV_B),
    ("george-ano-leivadi", "Saint George Church in Ano Leivadi", "Ἱερός Ναός Ἁγίου Γεωργίου Ἄνω Λιβαδίου", "Ano Leivadi", "Ἄνω Λειβάδι Κυθήρων", "Church", "parish", JAN_B),
    ("pantokrator-castle", "Pantokrator Church at the Castle of Chora", "Ἱερός Ναός Παντοκράτορος Κάστρου Χώρας", "Castle of Chora", "Κάστρο Χώρας Κυθήρων", "Church", "parish", FORTY_LITURGIES_URL),
    ("holy-trinity-myrtidia", "Holy Trinity Monastery Chapel at Myrtidia", "Ναΐδιον Ἁγίας Τριάδος Μυρτιδίων", "Myrtidia", "Μυρτίδια Κυθήρων", "Monastery Chapel", "monastery", MONUMENTS_URL),
]


ALLOWED_HOSTS = {
    "www.imkythiron.gr", "imkythiron.gr", "ecclesiagreece.gr", "www.ecclesiagreece.gr",
    "ecclesia.gr", "www.ecclesia.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]")


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "body"


def parse_parishes():
    rows = []
    for line in PARISH_SOURCE.strip().splitlines():
        seat, local_seat, dedication, local_dedication, rank, phone_text = line.split("|")
        item = {
            "id": "gr-kythira-%03d-%s" % (len(rows) + 1, slug(seat + "-" + dedication)),
            "parent": PARENT, "kind": "parish", "rank": rank,
            "name": "%s %s in %s" % (dedication, rank, seat),
            "local": "Ἱερός Ναός %s %s" % (local_dedication, local_seat),
            "seat": seat, "country": "GR", "address": [local_seat, "Ελλάδα"],
            "sources": [ROSTER_URL, LEGAL_URL],
        }
        phones = [value for value in phone_text.split(";") if value]
        if phones:
            item["phones"] = phones
            item["contact_sources"] = [ROSTER_URL]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


def build_rows():
    rows = parse_parishes()
    for key, name, local, seat, local_seat, phones in PILGRIMAGES:
        rows.append({
            "id": "gr-kythira-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": "parish", "rank": "Pilgrimage",
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [local_seat, "Ελλάδα"], "phones": list(phones),
            "sources": [ROSTER_URL, LEGAL_URL], "contact_sources": [ROSTER_URL],
            "contact_checked": CHECKED,
        })
    key, name, local, seat, local_seat, phones = MONASTERY
    rows.append({
        "id": "gr-kythira-%03d-%s" % (len(rows) + 1, key),
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": name, "local": local, "seat": seat, "country": "GR",
        "address": [local_seat, "Ελλάδα"], "phones": list(phones),
        "sources": [ROSTER_URL], "contact_sources": [ROSTER_URL],
        "contact_checked": CHECKED,
    })
    for key, name, local, seat, local_seat, rank, kind, source_url in ADDITIONAL_SOURCE:
        rows.append({
            "id": "gr-kythira-%03d-%s" % (len(rows) + 1, key),
            "parent": PARENT, "kind": kind, "rank": rank,
            "name": name, "local": local, "seat": seat, "country": "GR",
            "address": [local_seat, "Ελλάδα"], "sources": [source_url],
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 106
EXPECTED_OWNER_COUNTS = {PARENT: 106}
EXPECTED_KINDS = {"monastery": 4, "parish": 102}
EXPECTED_RANKS = {
    "Cave Church": 1,
    "Cemetery Church": 1,
    "Chapel": 17,
    "Church": 49,
    "Metropolitan Cathedral": 1,
    "Monastery": 2,
    "Monastery Chapel": 1,
    "Monydrion": 1,
    "Parish Church": 29,
    "Pilgrimage": 4,
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
        raise ValueError("Kythira candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kythira candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_parishes": 30,
        "current_pilgrimages": 4,
        "current_roster_monasteries": 1,
        "other_exact_current_bodies": 71,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Kythira ledger summary drifted at %s" % key)
    if expected_coverage:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites",
            "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Kythira ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Kythira ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kythira ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Kythira candidate IDs repeat")
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
            raise ValueError("duplicate Kythira ID: %s" % row_id)
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
        raise ValueError("Kythira English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Kythira English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Kythira parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Kythira kind totals drifted: %r" % dict(kind_counts))
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Kythira rank totals drifted: %r" % dict(rank_counts))
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
            if not payload.startswith(b"%PDF") or len(payload) < 50000:
                raise ValueError("invalid PDF payload")
            return None
        if "html" not in content_type:
            raise ValueError("unexpected content type %s" % content_type)
        return payload.decode("utf-8", "replace")


def check_markers(url, markers):
    payload = fetch_live_source(url)
    text = normalize_source_text(payload)
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("live Kythira marker failed at %s: %s" % (url, marker))


def check_live_sources():
    check_markers(ROSTER_URL, (
        "Ἐνοριακοί Ναοί 30", "Παρεκκλήσια 300", "Ναοί Κοιμητηρίων 30",
        "Μοναστηριακοί Ναοί 5", "Κοίμησις Θεοτόκου", "Ἅγιος Χαράλαμπος",
        "Ἅγιος Βασίλειος", "Εἰσόδια Θεοτόκου", "6977.292.317",
        "Παναγία Δέσποινα", "Ξερουλάκι", "Ὁσιου Θεοδώρου",
    ))
    check_markers(SEPTEMBER, (
        "Γενεσίου τῆς Θεοτόκου (Κακοπέτρι)",
        "Ἱερόν Μονύδριον Τιμίου Προδρόμου", "Ἁγίου Μάμαντος Κατουνίου",
    ))
    check_markers(OCT_B, (
        "Εὐαγγελιστοῦ Λουκᾶ Μανιτοχωρίου", "Ἁγίου Ἀρτεμίου",
        "Ἁγίου Ἰακώβου Ἀδελφοθέου", "Ἁγίας Ἀναστασίας",
    ))
    check_markers(NOV_A, (
        "Κοιμητηριακόν Ναόν Ἁγίων Ταξιαρχῶν Καραβᾶ",
        "Παμμεγίστων Ταξιαρχῶν Τραβασαριανίκων", "Ἁγίου Μηνᾶ Ἀρωνιαδίκων",
    ))
    fetch_live_source(LEGAL_URL)
    fetch_live_source(RENAME_URL)
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
        print("Kythira live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Kythira check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
