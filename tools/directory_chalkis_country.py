#!/usr/bin/env python3
"""Validate exact current Metropolis of Chalkis bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_chalkis_country.py --check
    python tools/directory_chalkis_country.py --check-live
    python tools/directory_chalkis_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "chalkis_country.json"
)
PARENT = "gr-chalkis"
ROSTER_TEMPLATE = (
    "https://imchalkidos.gr/Site/wSite/"
    "pListChurch.asp?Lang=1&PageRecID=25171&Rec=%d"
)
ROSTER_URLS = {rec: ROSTER_TEMPLATE % rec for rec in range(46, 56)}
CHURCH_OF_GREECE_PAGE = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/chalkidos"
)
CHURCH_OF_GREECE_AGGREGATE = (
    "https://www.ecclesiagreece.gr/greek/holysynod/commitees/"
    "relations/thesmiko_plaisio_paideias.pdf"
)
LEGAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/"
    "2019_februarios.pdf"
)


# Current source rows retained after omitting five non-worship institutions,
# one planned church, and one duplicate orphanage chapel row. The columns are
# regional source number, settlement, exact current title, and exact phone
# display. Clergy names occupy a separate source column and are not retained.
RAW_ROWS = r"""
46|Χαλκίδα|Μητροπολιτικός Ιερός Ναός Αγίου Δημητρίου|22210. 23279
46|Χαλκίδα|Ιερός Ναός Αγίου Στεφάνου|22210. 77611
46|Χαλκίδα|Ιερός Ναός Αγίων Τιμοθέου Ευρίπου και Νικολάου του Πλανά (Εκκλησ. Μουσείου)|
46|Χαλκίδα|Ιερός Ναός Αγίας Παρασκευής Πολιούχου Χαλκίδος|22210. 22112 . 25579
46|Χαλκίδα|Ιερός Ναός Αγίου Φανουρίου|
46|Χαλκίδα|Ιερός Ναός Αγίου Ελευθερίου (1ου Δημοτικού Σχολείου)|
46|Χαλκίδα|Ιερός Ναός Αγίων Αναργύρων|22210. 43996
46|Χαλκίδα|Ιερός Ναός Ευαγγελισμού της Θεοτόκου Κανήθου|22210. 24550 . 28820
46|Χαλκίδα|Ιερός Ναός Ευβοέων Αγίων|22210. 84600
46|Χαλκίδα|Ιερός Ναός Αγίου Ιωάννου|22210. 24440
46|Χαλκίδα|Ιερός Ναός Αγίας Φωτεινής|
46|Χαλκίδα|Ιερός Ναός Παναγίας των Βλαχερνών|
46|Χαλκίδα|Ιερός Ναός Αγίας Μαρίνας|22210. 80698
46|Χαλκίδα|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης|22210. 87731
46|Χαλκίδα|Ιερός Ναός Αγίου Νεκταρίου|22210. 82682
46|Χαλκίδα|Ιερός Ναός Αγίου Νικολάου|22210. 24815 . 76649
46|Χαλκίδα|Ιερός Ναός Παναγίας Οδηγήτριας (Μέσα Παναγίτσα)|22210. 29619
46|Χαλκίδα|Προφήτη Ηλία Κάστρου Χαλκίδος|22210. 79329
46|Χαλκίδα|Οσίου Δαβίδ (Α΄ Γυμνασίου - Λυκείου)|
46|Χαλκίδα|Παναγίας Λαγκαδιώτισσας|
46|Χαλκίδα|Ιερός Ναός Αγίων Πέτρου και Παύλου|22210. 74824
46|Χαλκίδα|Ιερός Ναός Αγίου Σπυρίδωνος|22210. 88120
46|Χαλκίδα|Ιερός Ναός Παμμεγίστων Ταξιαρχών|22210. 24828
46|Χαλκίδα|Ιερός Ναός Ζωοδόχου Πηγής Ορφανοτροφείου|22210. 84585
46|Χαλκίδα|Ιερός Ναός Αγίου Παντελεήμονος Γηροκομείου|22210. 26452 . 25400
46|Χαλκίδα|Ιερός Ναός Αγίας Βαρβάρας (Μητροπολιτικό παρεκκλήσιο)|22210. 23474
46|Χαλκίδα|Ιερός Ναός Αγίου Ελευθερίου Φυλακών Χαλκίδος|
46|Άγ. Νικόλαος Μπούρτζι|Ιερός Ναός Αγίου Νικολάου|22210. 53601
46|Αμάρυνθος|Ιερός Ναός Ευαγγελισμού της Θεοτόκου|22290. 36330
46|Αμάρυνθος|Ιερός Ναός Αγίου Ιωάννου|22290. 36393
46|Νέα Αρτάκη|Ιερός Ναός Αγίων Αποστόλων|
46|Αφράτι|Ιερός Ναός Κοιμήσεως Θεοτόκου|22210. 53848
46|Άνω Βάθεια|Ιερός Ναός Αγίου Νικολάου|22290. 38990
46|Βασιλικό|Ιερός Ναός Κοιμήσεως Θεοτόκου|22210. 52821
46|Βασιλικό|Ιερός Ναός Οσίου Ιωάννου Ρώσου|22210. 53387
46|Βατώντας|Ιερός Ναός Αγίου Γεωργίου|2.221.042.584
46|Γυμνού|Ιερός Ναός Κοιμήσεως Θεοτόκου|22290. 91444
46|Δοκός Χαλκίδος|Ιερός Ναός Κοιμήσεως Θεοτόκου|22210. 92257
46|Δοκός Χαλκίδος|Ιερός Ναός Αγίας Ελεούσης|22210. 92007
46|Ερέτρια|Ιερός Ναός Αγίου Νικολάου|22290. 62311
46|Ερέτρια|Ιερός Ναός Παναγίας Παραβουνιώτισσας|22290. 65222
46|Ερέτρια|Ιερός Ναός Παναγίας Ελεούσα (Μαλακώντα)|22290. 68933
46|Ερέτρια|Ιερός Ναός Αγίου Ανδρέου - (Μαλακώντα)|
46|Καλλιθέα|Ιερός Ναός Αγίας Παρασκευής|22290. 91989
46|Νέα Λάμψακος|Ιερός Ναός Αγίου Τρύφωνος|22210. 80318
46|Μύτικας|Ιερός Ναός Αγίου Αθανασίου|22210. 52675
46|Μύτικας|Ιερός Ναός Αγίου Ιωάννου Προδρόμου|22210. 52524
46|Σέττα|Ιερός Ναός Αγίας Παρασκευής|22290. 91586
46|Φύλλα|Ιερός Ναός Εισοδίων Θεοτόκου|22210. 53943
46|Χαλκίδα|Ιερός Ναός Αγίας Σοφίας (Ξηρόβρυση)|22210. 94697
46|Χαλκίδα|Ιερός Ναός Κοιμητηρίου Ανάσταση Λαζάρου|22210. 44667
46|Μύτικας|Ιερός Ναός Ευαγγελισμού της Θεοτόκου|22210. 54157
46|Χαλκίδα|Ιερό Παρακκλήσιο Οσίου Ιακώβου του ''με συγχωρείτε''|
46|Νέα Αρτάκη|Ιερό Προσκύνημα Παναγίας της Φανερωμένης|
46|Φύλλα|Ιερά Μονή Αγίου Αρμά|22210.50777
46|Άνω Βάθεια|Ιερά Μόνη Αγίου Νικολάου Άνω Βάθειας|22290.36070
47|Άτταλη|Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|22280. 91243
47|Αγία Σοφία|Ιερός Ναός Αγίου Νικολάου|
47|Καμαρίτσα|Ιερός Ναός Αγίας Τριάδος|22280. 32750
47|Καστέλλα|Ιερός Ναός Ευαγγελισμού της Θεοτόκου|22280. 24948
47|Κοντοδεσπότι|Ιερός Ναός Κοιμήσεως Θεοτόκου|22280. 91255
47|Κυπαρίσσι|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22280. 91277
47|Μακρυκάπα|Ιερός Ναός Αγίας Παρασκευής|22280. 71448
47|Μακρυμάλλη|Ιερός Ναός Οσίου Ιωάννου του Ρώσου|22280. 24803
47|Μύλοι|Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|22280. 22178
47|Νεροτριβιά|Ιερός Ναός Αγίου Κωνσταντίνου|22280. 31845
47|Παγώντας|Ιερός Ναός Αγίας Παρασκευής|22280. 25137
47|Πολιτικά|Ιερός Ναός Αγίας Παρασκευής|22280. 31621
47|Σταυρός|Σταυρός|22280. 91202
47|Τριάδα|Ιερός Ναός Αγίου Σπυρίδωνος|22287. 71007
47|Ψαχνά|Ιερός Ναός Αγίου Νικολάου|22280. 23658
47|Ψαχνά|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22280. 22118
47|Ψαχνά|Ιερός Ναός Μεταμορφώσεως του Σωτήρος|22280. 23496
47|Μαρκάτες|Ιερός Ναός Ευαγγελισμού της Θεοτόκου|
47|Ψαχνά|Ιερό Ησυχαστήριο Παναγίας Γοργοϋπηκόου Ψαχνών|22280.22743
47|Ψαχνά|Ιερά Μονή Αγίου Ιωάννη Καλυβίτη|22280.22180
47|Μακρυμάλλη|Ιερά Μονή Κοιμήσεως της Θεοτόκου|22280.22790
47|Πολιτικά|Ιερά Μονή Παναγίας Περιβλέπτου Πολιτικών|22280.31088
48|Άγιος Αθανάσιος|Ιερός Ναός Αγίου Κωνσταντίνου|22280. 71017
48|Αμφιθέα|Ιερός Ναός Κοιμήσεως Θεοτόκου|22280. 71976
48|Βούνοι|Ιερός Ναός Αγίου Γεωργίου|22280. 51203
48|Γλυφάδα|Ιερός Ναός Αγίου Ιωάννου Θεολόγου|22280. 92276
48|Θεολόγος|Ιερός Ναός Αγίου Ιωάννου|22210. 95186
48|Καθενοί|Ιερός Ναός Αγίου Ιωάννου Προδρόμου|22280. 51007
48|Καμπιά|Ιερός Ναός Αγίου Νικολάου|
48|Κοτσίκια|Ιερός Ναός Προφήτου Ηλιού|
48|Κούτουρλο|Ιερός Ναός Αγίου Δημητρίου|
48|Λάμαρη|Ιερός Ναός Αγίων Ταξιαρχών|22280. 25041
48|Λούτσα|Ιερός Ναός Γενέσεως Θεοτόκου|
48|Μετόχι Δίρφυος|Ιερός Ναός Αγίου Ιωάννου|22280. 25204
48|Μίστρος|Ιερός Ναός Αγίου Δημητρίου|
48|Πάλιουρας|Ιερός Ναός Αγίου Νικολάου|22280. 71649
48|Πισσώνας|Ιερός Ναός Αγίου Γεωργίου|22280. 51028
48|Πούρνος|Ιερός Ναός Αγίας Τριάδος|22210. 78965
48|Άνω Στενή|Ιερός Ναός Κοιμήσεως Θεοτόκου|22280. 51128, 51232
48|Κάτω Στενή|Ιερός Ναός Αγίας Τριάδος|22280. 51516
48|Στρόπωνες|Ιερός Ναός Αγίας Τριάδος|22280. 25028
48|Μαυρόπουλο|Ι. Ν. Αγίας Τριάδος Μαυρόπουλο|
48|Χιλιαδού|Ι.Ν.Παναγίας Χιλιαδούς, Μετόχιον Ι. Μονής Μακρυμάλλη Ψαχνών|
48|Πάλιουρας|Ιερά Μονή Παναγίας Μυρτιδιωτίσσης Πάλιουρα|22280.71113
49|Άγιος Γεώργιος Ιστιαίας|Ιερός Ναός Αγίου Γεωργίου|22260. 53494
49|Αγριοβοτάνι|Ιερός Ναός Αγίων Αναργύρων|22260. 53183
49|Αγδίνες|Ιερός Ναός Αγίου Ιωάννου Θεολόγου|22260. 55680
49|Αρτεμήσιο|Ιερός Ναός Αγίου Δημητρίου|22260. 41926
49|Ασμήνιο|Ιερός Ναός Αγίου Νικολάου|22260. 41075
49|Αυγαριά|Ιερός Ναός Αγίας Παρασκευής|
49|Βασιλικά|Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|22260. 43256
49|Βουτά|Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|22260. 81079
49|Γαλατσώνα|Ιερός Ναός Αγίου Ιωάννου του Προδρόμου|
49|Γαλατσάδες|Ιερός Ναός Αγίου Αθανασίου|
49|Γερακιού|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22260. 54537
49|Γούβες|Ιερός Ναός Αγίου Παντελεήμονος|22260. 42066
49|Ελληνικά|Ιερός Ναός Αγίου Χαραλάμπους|22260. 42412
49|Ιστιαία|Ιερός Ναός Αγίου Αθανασίου|22260. 54586
49|Ιστιαία|Ιερός Ναός Ευαγγελισμού της Θεοτόκου|22260. 52163
49|Ιστιαία|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22260. 52406
49|Καμάρια|Ιερός Ναός Αγίων Αναργύρων|22260. 54723
49|Καμματριάδες|Ιερός Ναός Αγίου Παντελεήμονος|
49|Καστανιώτισσα|Ιερός Ναός Αγίου Αγίας Παρασκευής|
49|Κοκκινομηλιά|Ιερός Ναός Αγίων Ταξιαρχών|22260. 55574
49|Κρυονερίτης|Ιερός Ναός Αγίου Γεωργίου|22260. 81189
49|Μηλιές|Ιερός Ναός Αγίας Παρασκευής|22260. 91277
49|Μονοκαρυά|Ιερός Ναός Αγίου Δημητρίου|22260. 81073
49|Νεοχώρι Ιστιαίας|Ιερός Ναός Αγίου Νικολάου|22260. 54483
49|Πευκί|Ιερός Ναός Αγίων Θεοδώρων|22260. 40316
49|Νέος Πύργος|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22260. 72433
49|Σίμια|Ιερός Ναός Αγίας Τριάδος|
49|Συνασσός|Ιερός Ναός Αγίου Νικολάου|22260. 54945
49|Ταξιάρχης Ιστιαίας|Ιερός Ναός Αγίου Ταξιάρχου|22260. 71020
49|Ωρεοί|Ιερός Ναός Μεταμορφώσεως του Σωτήρος|22260. 72530
49|Ιστιαία|Ιερός Ναός Αγίας Μαρίας Μαγδαληνής|
49|Ήλια|Ιερά Μονή Αγίου Γεωργίου Ήλιων|22260.22384
50|Άγιος Αιδηψού|Ιερός Ναός Αγίου Γεωργίου|22260. 31087
50|Άγιος Γεώργιος Λιχάδος|Ιερός Ναός Αγίου Γεωργίου|22260. 33178
50|Αιδηψός|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22260. 22754, 22260. 22754
50|Γιάλτρα|Ιερός Ναός Αγίου Νικολάου|22260. 32363
50|Ήλια|Ιερός Ναός Αγίου Ιωάννου Θεολόγου|22260. 60647
50|Λιχάδα|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22260. 33007
50|Λουτρά Αιδηψού|Ιερός Ναός Αγίων Αναργύρων|22260. 22254 . 23700 .
50|Λουτρά Αιδηψού|Ιερός Ναός Αγίου Παντελεήμονος|22260. 60056
50|Πολύλοφος|Ιερός Ναός Αγίου Ιωάννου Προδρόμου|
51|Δαμιά|Ιερός Ναός Γεννήσεως της Θεοτόκου|22270 71297
51|Δάφνη|Ιερός Ναός Αγίου Δημητρίου|22270. 97134
51|Κεχριές|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22270. 93292
51|Κούλουρος|Ιερός Ναός Γεννήσεως της Θεοτόκου|
51|Κουρκουλοί|Ιερός Ναός Αγίας Παρασκευής|22270. 92535
51|Λίμνη|Ιερός Ναός Γεννήσεως της Θεοτόκου|22270. 31171
51|Ροβιές|Ιερός Ναός Αγίου Δημητρίου|22270. 71216
51|Σκεπαστή|Ιερός Ναός Αγίου Νικολάου|22270. 92069
51|Χρόνια|Ιερός Ναός Αγίων Αναργύρων|
51|Φαράκλα|Ι.Ν. Αγίου Γεωργίου|
51|Καλαμούδι|Ιερός Ναός Κοιμήσεως της Θεοτόκου|
51|Λίμνη|Ιερά Μονή Αγίου Νικολάου Γαλατάκη Λίμνης|22270.31489
51|Λίμνη|Ιερά Μονή Οσίου Δαυίδ Γέροντος|22270.71297 και 22270.71143
51|Ροβιές|Ιερό Μετόχιο Οσίας Ειρήνης Χρυσοβαλλάντου|22270.71215
52|Βλαχιά|Ιερός Ναός Αγίας Τριάδος|22270. 91155
52|Δαφνούσα|Ιερός Ναός Αγίου Αθανασίου|
52|Κήρυνθος|Ιερός Ναός Αγίου Γεωργίου|22270. 22381
52|Αγίου Δημητρίου Μετοχίου Κηρέως|Αγίου Δημητρίου Μετοχίου Κηρέως|22270. 93221
52|Μαντούδι|Ιερός Ναός Αγίου Ιωάννου Θεολόγου|22270. 22100
52|Προκόπι|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης|22270. 41450
52|Πήλι|Ιερός Ναός Αγίου Γεωργίου|22270. 91015
52|Σπαθάρι|Ιερός Ναός Αγίου Δημητρίου|22270. 94252
52|Τσούκα|Ιερός Ναός Ζωοδόχου Πηγής|
52|Προκόπι|Ιερό Προσκύνημα του Οσίου Ιωάννου του Ρώσσου|
53|Αγία Άννα|Ιερός Ναός Γενεθλίου της Θεοτόκου|22270. 61406
53|Παραλία Αγίας Άννας|Ιερός Ναός Αποτομής Τιμίου Προδρόμου|
53|Αμέλαντες|Ιερός Ναός Τιμίας Ζώνης|
53|Αχλάδι|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22270. 97134
53|Κεράμεια|Ιερός Ναός Ευαγγελισμού της Θεοτόκου|22270. 51182
53|Κερασιά|Ιερός Ναός Αγίας Τριάδος|22270. 71517
53|Κοτσικιά|Ιερός Ναός Αγίου Ιωάννου|
53|Παπάδες|Ιερός Ναός Κοιμήσεως της Θεοτόκου|22270. 61412
53|Στροφυλιά|Ιερός Ναός Αγίας Τριάδος|22270. 32390
54|Σκιάθος|Ιερός Ναός Γενεθλίου της Θεοτόκου|24270. 23180
54|Σκιάθος|Ιερός Ναός Τριών Ιεραρχών|24270. 22530
54|Σκιάθος|Ιερά Μονή Ευαγγελισμού της Θεοτόκου|24270. 22012
55|Αλόννησος|Ιερός Ναός Αγίου Νικολάου|24240 65041
55|Γλώσσα Σκοπέλου|Ιερός Ναός Κοιμήσεως της Θεοτόκου|24240. 34250
55|Κλήμα Σκοπέλου|Ιερός Ναός Αγίων Αναργύρων|24240. 33330
55|Λουτράκι Σκοπέλου|Ιερός Ναός Αγίου Νικολάου|
55|Πατητήρι - Αλόννησος|Πατητήρι - Αλόννησος|24240. 65041
55|Σκόπελος|Ιερός Ναός Αγίου Παντελεήμονος|24240. 22184
55|Σκόπελος|Ιερός Ναός Γεννήσεως του Χριστού|24240. 22171
55|Σκόπελος|Ιερός Ναός Κοιμήσεως της Θεοτόκου|24240. 23187
55|Σκόπελος|Ιερός Ναός Παναγίας Φανερωμένης|24240. 24370
55|Σκόπελος|Ιερά Μονή Αγίου Ρηγίνου|24240.22395
55|Σκόπελος|Ιερά Μονή Τιμίου Προδρόμου|24240.22395
55|Σκόπελος|Ιερά Μονή Ευαγγελισμού της Θεοτόκου|24240.22394
"""

EXCLUDED_LIVE_TITLES = {
    "Ιερός Ναός Νέου Νοσοκομείου Χαλκίδος - υπό ανέγερση",
    "Ιερός Ναός Ζωοδόχυ Πηγής (Ορφανοτροφείο Αρρένων)",
    "Γραφεία Ιεράς Μητροπόλεως Χαλκίδος",
    "Πολιτιστικό και Πνευματικό Κέντρο Ιεράς Μητροπόλεως Χαλκίδος",
    "Εκκλησιαστικό Γηροκομείο Χαλκίδος",
    "Ορφανοτροφείο Χαλκίδος",
    "Βησσαριώνειο Εκκλησιαστικό Γηροκομείο Ιστιαίας",
}


# These 25 current exact churches are outside the regulation's 145 parish
# rows. They remain publishable current worship bodies, but are not silently
# promoted to legal parishes.
NON_PARISH_CURRENT = {
    ("Χαλκίδα", "Ιερός Ναός Αγίου Στεφάνου"),
    ("Χαλκίδα", "Ιερός Ναός Αγίων Τιμοθέου Ευρίπου και Νικολάου του Πλανά (Εκκλησ. Μουσείου)"),
    ("Χαλκίδα", "Ιερός Ναός Αγίου Φανουρίου"),
    ("Χαλκίδα", "Ιερός Ναός Αγίου Ελευθερίου (1ου Δημοτικού Σχολείου)"),
    ("Χαλκίδα", "Ιερός Ναός Αγίας Φωτεινής"),
    ("Χαλκίδα", "Ιερός Ναός Παναγίας των Βλαχερνών"),
    ("Χαλκίδα", "Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης"),
    ("Χαλκίδα", "Ιερός Ναός Παναγίας Οδηγήτριας (Μέσα Παναγίτσα)"),
    ("Χαλκίδα", "Προφήτη Ηλία Κάστρου Χαλκίδος"),
    ("Χαλκίδα", "Οσίου Δαβίδ (Α΄ Γυμνασίου - Λυκείου)"),
    ("Χαλκίδα", "Παναγίας Λαγκαδιώτισσας"),
    ("Χαλκίδα", "Ιερός Ναός Ζωοδόχου Πηγής Ορφανοτροφείου"),
    ("Χαλκίδα", "Ιερός Ναός Αγίου Παντελεήμονος Γηροκομείου"),
    ("Χαλκίδα", "Ιερός Ναός Αγίας Βαρβάρας (Μητροπολιτικό παρεκκλήσιο)"),
    ("Χαλκίδα", "Ιερός Ναός Αγίου Ελευθερίου Φυλακών Χαλκίδος"),
    ("Δοκός Χαλκίδος", "Ιερός Ναός Αγίας Ελεούσης"),
    ("Ερέτρια", "Ιερός Ναός Αγίου Ανδρέου - (Μαλακώντα)"),
    ("Μύτικας", "Ιερός Ναός Αγίου Αθανασίου"),
    ("Χαλκίδα", "Ιερός Ναός Κοιμητηρίου Ανάσταση Λαζάρου"),
    ("Μαρκάτες", "Ιερός Ναός Ευαγγελισμού της Θεοτόκου"),
    ("Μαυρόπουλο", "Ι. Ν. Αγίας Τριάδος Μαυρόπουλο"),
    ("Ιστιαία", "Ιερός Ναός Αγίας Μαρίας Μαγδαληνής"),
    ("Καλαμούδι", "Ιερός Ναός Κοιμήσεως της Θεοτόκου"),
    ("Φαράκλα", "Ι.Ν. Αγίου Γεωργίου"),
    ("Παραλία Αγίας Άννας", "Ιερός Ναός Αποτομής Τιμίου Προδρόμου"),
}


DETAILS = {
    ("Λίμνη", "Ιερά Μονή Οσίου Δαυίδ Γέροντος"): {
        "rec": 30, "page_rec": 6, "address": "340 05 Ροβιές Ευβοίας",
    },
    ("Φύλλα", "Ιερά Μονή Αγίου Αρμά"): {
        "rec": 31, "page_rec": 7, "address": "341 00 Φύλλα Χαλκίδος",
    },
    ("Σκιάθος", "Ιερά Μονή Ευαγγελισμού της Θεοτόκου"): {
        "rec": 32, "page_rec": 8, "address": "370 02 Σκιάθος",
        "emails": ["info@monievaggelistrias.gr"],
    },
    ("Λίμνη", "Ιερά Μονή Αγίου Νικολάου Γαλατάκη Λίμνης"): {
        "rec": 33, "page_rec": 9, "address": "340 05 Λίμνη",
    },
    ("Ήλια", "Ιερά Μονή Αγίου Γεωργίου Ήλιων"): {
        "rec": 34, "page_rec": 10, "address": "343 00 Ήλια Λουτρών Αιδηψού",
    },
    ("Άνω Βάθεια", "Ιερά Μόνη Αγίου Νικολάου Άνω Βάθειας"): {
        "rec": 35, "page_rec": 11, "address": "340 06 Άνω Βάθεια",
    },
    ("Μακρυμάλλη", "Ιερά Μονή Κοιμήσεως της Θεοτόκου"): {
        "rec": 36, "page_rec": 12, "address": "344 00 Ψαχνά Ευβοίας",
    },
    ("Σκόπελος", "Ιερά Μονή Τιμίου Προδρόμου"): {
        "rec": 37, "page_rec": 13, "address": "370 03 Σκόπελος",
    },
    ("Πολιτικά", "Ιερά Μονή Παναγίας Περιβλέπτου Πολιτικών"): {
        "rec": 38, "page_rec": 14, "address": "344 00 Πολιτικά Ευβοίας",
    },
    ("Ψαχνά", "Ιερά Μονή Αγίου Ιωάννη Καλυβίτη"): {
        "rec": 39, "page_rec": 15, "address": "344 00 Ψαχνά",
        "site": "https://www.kalivitis.gr/",
    },
    ("Σκόπελος", "Ιερά Μονή Ευαγγελισμού της Θεοτόκου"): {
        "rec": 40, "page_rec": 16, "address": "370 03 Σκόπελος",
    },
    ("Πάλιουρας", "Ιερά Μονή Παναγίας Μυρτιδιωτίσσης Πάλιουρα"): {
        "rec": 41, "page_rec": 17, "address": "340 18 Πάλιουρα Διρφύων",
    },
    ("Ψαχνά", "Ιερό Ησυχαστήριο Παναγίας Γοργοϋπηκόου Ψαχνών"): {
        "rec": 42, "page_rec": 18, "address": "344 00 Ψαχνά Ευβοίας",
    },
    ("Ροβιές", "Ιερό Μετόχιο Οσίας Ειρήνης Χρυσοβαλλάντου"): {
        "rec": 43, "page_rec": 19, "address": "340 05 Ροβιές Ευβοίας",
    },
    ("Προκόπι", "Ιερό Προσκύνημα του Οσίου Ιωάννου του Ρώσσου"): {
        "rec": 44, "page_rec": 20, "address": "340 04 Νέον Προκόπιον",
        "phones": ["2227041209", "2227041462", "2221025008"],
        "site": "https://oir.gr/",
    },
    ("Νέα Αρτάκη", "Ιερό Προσκύνημα Παναγίας της Φανερωμένης"): {
        "rec": 45, "page_rec": 21, "address": "346 00 Νέα Αρτάκη",
        "phones": ["2221042811", "2221042120"],
    },
}
for detail in DETAILS.values():
    detail["detail_page"] = (
        "https://imchalkidos.gr/Site/wSite/"
        "PageUser.asp?Lang=1&Rec=%d&PageRecID=%d"
        % (detail["rec"], detail["page_rec"])
    )
    detail.setdefault("site", detail["detail_page"])


DEDICATION_RULES = (
    ("Αγίων Τιμοθέου Ευρίπου και Νικολάου του Πλανά",
     "Saints Timothy of Euripos and Nicholas Planas"),
    ("Αγίων Κωνσταντίνου και Ελένης", "Saints Constantine and Helen"),
    ("Αγίων Πέτρου και Παύλου", "Saints Peter and Paul"),
    ("Αγίων Αναργύρων", "Holy Unmercenaries"),
    ("Αγίων Αποστόλων", "Holy Apostles"),
    ("Αγίων Θεοδώρων", "Holy Theodores"),
    ("Αγίων Ταξιαρχών", "Holy Archangels"),
    ("Παμμεγίστων Ταξιαρχών", "Holy Archangels"),
    ("Αγίου Ταξιάρχου", "Holy Archangels"),
    ("Ευβοέων Αγίων", "Saints of Euboea"),
    ("Αποτομής Τιμίου Προδρόμου", "Beheading of Saint John the Forerunner"),
    ("Τριών Ιεραρχών", "Three Holy Hierarchs"),
    ("Γεννήσεως του Χριστού", "Nativity of Christ"),
    ("Αγίας Μαρίας Μαγδαληνής", "Saint Mary Magdalene"),
    ("Αγίας Παρασκευής", "Saint Paraskevi"),
    ("Αγίου Αγίας Παρασκευής", "Saint Paraskevi"),
    ("Αγίας Βαρβάρας", "Saint Barbara"),
    ("Αγίας Ελεούσης", "Theotokos Eleousa"),
    ("Αγίας Μαρίνας", "Saint Marina"),
    ("Αγίας Σοφίας", "Saint Sophia"),
    ("Αγίας Τριάδος", "Holy Trinity"),
    ("Αγίας Φωτεινής", "Saint Photini"),
    ("Αγίου Αθανασίου", "Saint Athanasius"),
    ("Αγίου Ανδρέου", "Saint Andrew"),
    ("Αγίου Γεωργίου", "Saint George"),
    ("Αγίου Δημητρίου", "Saint Demetrius"),
    ("Αγίου Ελευθερίου", "Saint Eleftherios"),
    ("Αγίου Ιωάννου Θεολόγου", "Saint John the Theologian"),
    ("Αγίου Ιωάννου του Προδρόμου", "Saint John the Forerunner"),
    ("Αγίου Ιωάννου Προδρόμου", "Saint John the Forerunner"),
    ("Αγίου Ιωάννου του Ρώσσου", "Venerable John the Russian"),
    ("Αγίου Ιωάννου Ρώσου", "Venerable John the Russian"),
    ("Αγίου Ιωάννη Καλυβίτη", "Venerable John Kalyvites"),
    ("Αγίου Ιωάννου", "Saint John"),
    ("Αγίου Κωνσταντίνου", "Saint Constantine"),
    ("Αγίου Νεκταρίου", "Saint Nectarios"),
    ("Αγίου Νικολάου", "Saint Nicholas"),
    ("Αγίου Παντελεήμονος", "Saint Panteleimon"),
    ("Αγίου Ρηγίνου", "Saint Reginos"),
    ("Αγίου Σπυρίδωνος", "Saint Spyridon"),
    ("Αγίου Στεφάνου", "Saint Stephen"),
    ("Αγίου Τρύφωνος", "Saint Tryphon"),
    ("Αγίου Φανουρίου", "Saint Fanourios"),
    ("Αγίου Χαραλάμπους", "Saint Charalambos"),
    ("Αγίου Αρμά", "Saint George"),
    ("Οσίου Δαυίδ", "Venerable David the Elder"),
    ("Οσίου Δαβίδ", "Venerable David the Elder"),
    ("Οσίου Ιακώβου", "Venerable Iakovos Tsalikis"),
    ("Οσίου Ιωάννου του Ρώσσου", "Venerable John the Russian"),
    ("Οσίου Ιωάννου του Ρώσου", "Venerable John the Russian"),
    ("Οσίου Ιωάννου Ρώσου", "Venerable John the Russian"),
    ("Οσίας Ειρήνης Χρυσοβαλλάντου", "Venerable Irene Chrysovalantou"),
    ("Παναγίας Γοργοϋπηκόου", "Theotokos Gorgoepikoos"),
    ("Παναγίας Μυρτιδιωτίσσης", "Theotokos Myrtidiotissa"),
    ("Παναγίας Περιβλέπτου", "Theotokos Perivleptos"),
    ("Παναγίας Παραβουνιώτισσας", "Theotokos Paravouniotissa"),
    ("Παναγίας Φανερωμένης", "Theotokos Faneromeni"),
    ("Παναγίας της Φανερωμένης", "Theotokos Faneromeni"),
    ("Παναγίας Οδηγήτριας", "Theotokos Hodegetria"),
    ("Παναγίας των Βλαχερνών", "Theotokos of Blachernae"),
    ("Παναγίας Λαγκαδιώτισσας", "Theotokos Lagkadiotissa"),
    ("Παναγίας Ελεούσα", "Theotokos Eleousa"),
    ("Παναγίας Χιλιαδούς", "Theotokos of Chiliadou"),
    ("Ευαγγελισμού της Θεοτόκου", "Annunciation of the Theotokos"),
    ("Γενεθλίου της Θεοτόκου", "Nativity of the Theotokos"),
    ("Γενέσεως Θεοτόκου", "Nativity of the Theotokos"),
    ("Γεννήσεως της Θεοτόκου", "Nativity of the Theotokos"),
    ("Κοιμήσεως της Θεοτόκου", "Dormition of the Theotokos"),
    ("Κοιμήσεως Θεοτόκου", "Dormition of the Theotokos"),
    ("Εισοδίων Θεοτόκου", "Entrance of the Theotokos into the Temple"),
    ("Ζωοδόχου Πηγής", "Life-Giving Spring"),
    ("Μεταμορφώσεως του Σωτήρος", "Transfiguration of the Savior"),
    ("Προφήτου Ηλιού", "Prophet Elijah"),
    ("Προφήτη Ηλία", "Prophet Elijah"),
    ("Τιμίας Ζώνης", "Holy Belt of the Theotokos"),
    ("Τιμίου Προδρόμου", "Saint John the Forerunner"),
    ("Ανάσταση Λαζάρου", "Raising of Lazarus"),
)


GREEK = dict(zip(
    "αβγδεζηθικλμνξοπρστυφχψω",
    ("a", "v", "g", "d", "e", "z", "i", "th", "i", "k", "l", "m",
     "n", "x", "o", "p", "r", "s", "t", "y", "f", "ch", "ps", "o")
))
AREA_PREFIXES = {
    "22210", "22260", "22270", "22280", "22287", "22290",
    "24240", "24270",
}


def parse_table(raw, width, label):
    rows = []
    for line_number, line in enumerate(raw.strip().splitlines(), 1):
        fields = [value.strip() for value in line.split("|")]
        if len(fields) != width:
            raise ValueError("%s row %d has %d fields" % (
                label, line_number, len(fields)))
        rows.append(fields)
    return rows


def unicase(value):
    value = unicodedata.normalize("NFD", value.casefold())
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def transliterate(value):
    value = unicase(value)
    for source, target in (
        ("γγ", "ng"), ("γκ", "gk"), ("μπ", "mp"), ("ντ", "nt"),
        ("ου", "ou"), ("αι", "ai"), ("ει", "ei"), ("οι", "oi"),
        ("τσ", "ts"), ("τζ", "tz"),
    ):
        value = value.replace(source, target)
    value = "".join(GREEK.get(char, char) for char in value)
    value = re.sub(r"\s+", " ", value).strip().title()
    value = value.replace("Mpourtzi", "Bourtzi")
    return value.replace("Ag. Nikolaos", "Agios Nikolaos")


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "body"


def dedication_for(local_title):
    if local_title == "Σταυρός":
        return "Saint Demetrius"
    if local_title == "Πατητήρι - Αλόννησος":
        return "Saint Paraskevi"
    for needle, dedication in DEDICATION_RULES:
        if needle in local_title:
            return dedication
    raise ValueError("missing English dedication for %s" % local_title)


def parse_phones(raw):
    if not raw:
        return []
    groups = re.findall(r"\d+", raw)
    if not groups:
        return []
    if not any(len(value) == 5 for value in groups):
        joined = "".join(groups)
        if len(joined) == 10:
            return [joined]
        raise ValueError("unparsed phone display %r" % raw)
    prefix = None
    values = []
    for value in groups:
        if len(value) != 5:
            raise ValueError("unparsed phone group %r in %r" % (value, raw))
        if value in AREA_PREFIXES:
            prefix = value
            continue
        if prefix is None:
            raise ValueError("phone tail without prefix in %r" % raw)
        values.append(prefix + value)
    return list(dict.fromkeys(values))


def rank_for(seat_local, local_title):
    if local_title.startswith("Ιερό Ησυχαστήριο"):
        return "Hermitage"
    if (local_title.startswith("Ιερό Μετόχιο") or
            "Μετόχιον Ι. Μονής" in local_title):
        return "Metochion"
    if local_title.startswith(("Ιερά Μονή", "Ιερά Μόνη")):
        return "Monastery"
    if local_title.startswith("Ιερό Προσκύνημα"):
        return "Pilgrimage Church"
    if local_title.startswith("Ιερό Παρακκλήσιο"):
        return "Chapel"
    if local_title.startswith("Μητροπολιτικός"):
        return "Metropolitan Church"
    if (seat_local, local_title) not in NON_PARISH_CURRENT:
        return "Parish Church"
    if "Εκκλησ. Μουσείου" in local_title:
        return "Museum Church"
    if "Σχολείου" in local_title or "Γυμνασίου" in local_title:
        return "School Chapel"
    if "Ορφανοτροφείου" in local_title:
        return "Orphanage Chapel"
    if "Γηροκομείου" in local_title:
        return "Nursing Home Chapel"
    if "Μητροπολιτικό παρεκκλήσιο" in local_title:
        return "Metropolitan Chapel"
    if "Φυλακών" in local_title:
        return "Prison Chapel"
    if "Κοιμητηρίου" in local_title:
        return "Cemetery Church"
    return "Church"


def build_rows():
    parsed = parse_table(RAW_ROWS, 4, "current roster")
    if len(parsed) != 189:
        raise ValueError("current retained roster must have 189 rows")
    rows = []
    for index, (rec_text, seat_local, local_title, raw_phone) in enumerate(
            parsed, 1):
        rec = int(rec_text)
        source = ROSTER_URLS[rec]
        rank = rank_for(seat_local, local_title)
        dedication = dedication_for(local_title)
        seat = transliterate(seat_local)
        if seat_local == "Αγίου Δημητρίου Μετοχίου Κηρέως":
            seat = "Metochi Kireos"
        name = "%s %s in %s" % (dedication, rank, seat)
        kind = "monastery" if rank in (
            "Monastery", "Hermitage", "Metochion"
        ) else "parish"
        item = {
            "id": "gr-chalkis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (local_title, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat_local, "Greece"],
            "sources": [source],
        }
        if rank in ("Parish Church", "Metropolitan Church"):
            item["sources"].append(LEGAL_PDF)
        phones = parse_phones(raw_phone)
        detail = DETAILS.get((seat_local, local_title))
        if detail:
            item["sources"].append(detail["detail_page"])
            item["address"] = [detail["address"], "Greece"]
            phones.extend(detail.get("phones", []))
            phones = list(dict.fromkeys(phones))
            if detail.get("emails"):
                item["emails"] = list(detail["emails"])
            item["site"] = detail["site"]
        if phones:
            item["phones"] = ["+30-" + value for value in phones]
        if phones or item.get("emails"):
            item["contact_sources"] = [source]
            if detail:
                item["contact_sources"].append(detail["detail_page"])
            item["contact_checked"] = CHECKED
        rows.append(item)
    if sum(row["rank"] in ("Parish Church", "Metropolitan Church")
           for row in rows) != 145:
        raise ValueError("legal parish reconciliation must total 145")
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}
EXPECTED_TOTAL = 189
EXPECTED_OWNER_COUNTS = {PARENT: 189}
EXPECTED_KINDS = {"monastery": 16, "parish": 173}
EXPECTED_RANKS = {
    "Cemetery Church": 1,
    "Chapel": 1,
    "Church": 17,
    "Hermitage": 1,
    "Metochion": 2,
    "Metropolitan Chapel": 1,
    "Metropolitan Church": 1,
    "Monastery": 13,
    "Museum Church": 1,
    "Nursing Home Chapel": 1,
    "Orphanage Chapel": 1,
    "Parish Church": 144,
    "Pilgrimage Church": 2,
    "Prison Chapel": 1,
    "School Chapel": 2,
}
EXPECTED_CONTACT_BODIES = 151
EXPECTED_PHONE_BODIES = 151
EXPECTED_PHONE_VALUES = 161
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 16
EXPECTED_ADDRESS_BODIES = 189
EXISTING_PARENTS = {PARENT}
FORBIDDEN_PUNCTUATION = re.compile("[\u2013\u2014]")
PHONE_RE = re.compile(r"^\+30-\d{10}$")


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()
                if item not in (None, "", [], {})}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from walk_strings(item)


def expected_summary():
    return {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "exact_current_source_rows": 196,
        "exact_published_current_bodies": 189,
        "exact_legal_parishes": 145,
        "exact_current_other_churches_and_chapels": 26,
        "exact_current_pilgrimages": 2,
        "exact_current_monastic_bodies": 16,
        "parish_kind_rows": 173,
        "monastery_kind_rows": 16,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_or_official_detail_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
    }


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Chalkis candidate ledger identity drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Chalkis candidate ledger date drifted")
    if ledger.get("published_summary") != expected_summary():
        raise ValueError("Chalkis ledger summary drifted")
    if not ledger.get("candidates") or not ledger.get("source_reconciliations"):
        raise ValueError("Chalkis ledger lacks audit evidence")
    if any(FORBIDDEN_PUNCTUATION.search(text)
           for text in walk_strings(ledger)):
        raise ValueError("Chalkis ledger contains forbidden punctuation")
    return ledger


def validate():
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
        if not row_id or row_id in ids or row_id in EXISTING_PARENTS:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s lacks parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s carries the wrong country" % row_id)
        for field in ("kind", "rank", "name", "local", "seat"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        if any(re.search(
                r"(^|\s)(π\.|Αρχιμ\.|Πρωτοπρ\.|Ηγούμενος|Ηγουμένη)",
                text)
               for text in walk_strings(item)):
            raise ValueError("%s exposes a clergy marker" % row_id)
        phones = item.get("phones") or []
        if len(phones) != len(set(phones)):
            raise ValueError("%s repeats a phone" % row_id)
        for phone in phones:
            if not PHONE_RE.fullmatch(phone):
                raise ValueError("%s has malformed phone %s" % (row_id, phone))
        emails = item.get("emails") or []
        if len(emails) != len(set(emails)):
            raise ValueError("%s repeats an email" % row_id)
        if (phones or emails) and (
                item.get("contact_checked") != CHECKED or
                not item.get("contact_sources")):
            raise ValueError("%s lacks contact provenance" % row_id)
        signature = (
            item["parent"], item["kind"], unicase(item["name"]),
            unicase(item["seat"])
        )
        if signature in signatures:
            raise ValueError(
                "duplicate body signature: %s and %s"
                % (signatures[signature], row_id)
            )
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[parent] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (
            EXPECTED_TOTAL, len(result)))
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Chalkis parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Chalkis kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Chalkis rank totals drifted: %r" % (
            dict(sorted(rank_counts.items())),))
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
        raise ValueError(
            "Chalkis contact coverage drifted: %r != %r"
            % (coverage, expected_coverage)
        )
    validate_ledger()
    return result


def build():
    result = validate()
    for item in result:
        item.setdefault("checked", CHECKED)
        item.setdefault("cite", list(item.get("sources") or []))
    if set(ENGLISH_NAMES) != {row["id"] for row in result}:
        raise ValueError("Chalkis English name coverage drifted")
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
    }


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag == "td" and self.row is not None:
            self.cell = []
        elif tag == "br" and self.cell is not None:
            self.cell.append(" ")

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None


def fetch(url):
    request = Request(url, headers={"User-Agent": "Plithos directory audit"})
    with urlopen(request, timeout=45) as response:
        content_type = (response.headers.get("Content-Type") or "").lower()
        body = response.read()
        status = getattr(response, "status", 200)
    if status != 200:
        raise ValueError("%s returned HTTP %s" % (url, status))
    return body, content_type


def fetch_roster(rec):
    url = ROSTER_URLS[rec]
    body, content_type = fetch(url)
    if "html" not in content_type:
        raise ValueError("%s did not return HTML" % url)
    parser = TableParser()
    parser.feed(body.decode("utf-8", "replace"))
    rows = []
    for cells in parser.rows:
        if len(cells) >= 4 and cells[0] != "ΕΔΡΑ":
            rows.append((
                str(rec),
                cells[0].replace("\u2013", "-"),
                cells[1].replace("\u2013", "-"),
                cells[2].replace("\u2013", "-"),
            ))
    return rows


def check_live():
    with ThreadPoolExecutor(max_workers=8) as executor:
        source_groups = list(executor.map(fetch_roster, range(46, 56)))
    source_rows = [row for group in source_groups for row in group]
    if len(source_rows) != 196:
        raise ValueError("current official roster returned %d rows" %
                         len(source_rows))
    held = [row for row in source_rows if row[2] in EXCLUDED_LIVE_TITLES]
    if len(held) != 7:
        raise ValueError("current official held-row set drifted")
    retained = [row for row in source_rows
                if row[2] not in EXCLUDED_LIVE_TITLES]
    embedded = [tuple(row) for row in parse_table(
        RAW_ROWS, 4, "embedded current roster"
    )]
    if retained != embedded:
        raise ValueError("embedded current roster drifted from first party")
    detail_urls = [detail["detail_page"] for detail in DETAILS.values()]
    with ThreadPoolExecutor(max_workers=8) as executor:
        detail_results = list(executor.map(fetch, detail_urls))
    for url, (body, content_type) in zip(detail_urls, detail_results):
        if "html" not in content_type or len(body) < 5000:
            raise ValueError("%s failed current detail validation" % url)
    body, content_type = fetch(CHURCH_OF_GREECE_PAGE)
    page_text = html.unescape(body.decode("utf-8", "replace"))
    profile_tokens = (
        "Χαλκίδος", "Ανδρικές Μονές", "Γυναικείες Μονές",
        "Οσίου Δαβίδ Γέροντος", "Οσίας Ειρήνης Χρυσοβαλάντου",
    )
    if ("html" not in content_type or
            not all(token in page_text for token in profile_tokens)):
        raise ValueError("Church of Greece Chalkis profile drifted")
    for url in (LEGAL_PDF, CHURCH_OF_GREECE_AGGREGATE):
        body, content_type = fetch(url)
        if "pdf" not in content_type or len(body) < 100000:
            raise ValueError("%s failed official PDF validation" % url)
    return {
        "current_source_rows": len(source_rows),
        "retained_current_bodies": len(retained),
        "official_detail_pages": len(detail_urls),
        "held_or_merged_rows": len(held),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    if args.check:
        rows = validate()
        print(
            "Chalkis directory check passed: %d bodies, %d phone bodies, "
            "%d phone values, %d email bodies, %d official sites"
            % (
                len(rows),
                sum(bool(row.get("phones")) for row in rows),
                sum(len(row.get("phones") or []) for row in rows),
                sum(bool(row.get("emails")) for row in rows),
                sum(bool(row.get("site")) for row in rows),
            )
        )
    if args.check_live:
        print(json.dumps(check_live(), ensure_ascii=False, sort_keys=True))
    if args.dump:
        print(json.dumps(
            {
                "rows": [clean(row) for row in ROWS],
                "summary": {
                    "total": len(ROWS),
                    "kinds": dict(sorted(Counter(
                        row["kind"] for row in ROWS
                    ).items())),
                    "ranks": dict(sorted(Counter(
                        row["rank"] for row in ROWS
                    ).items())),
                    "contact_bodies": sum(bool(
                        row.get("phones") or row.get("emails") or
                        row.get("site")
                    ) for row in ROWS),
                    "phone_bodies": sum(bool(row.get("phones"))
                                       for row in ROWS),
                    "phone_values": sum(len(row.get("phones") or [])
                                        for row in ROWS),
                    "email_bodies": sum(bool(row.get("emails"))
                                       for row in ROWS),
                    "email_values": sum(len(row.get("emails") or [])
                                        for row in ROWS),
                    "site_bodies": sum(bool(row.get("site"))
                                      for row in ROWS),
                },
            },
            ensure_ascii=False, indent=2, sort_keys=True
        ))
    if not (args.check or args.check_live or args.dump):
        parser.print_help()


if __name__ == "__main__":
    main()
