#!/usr/bin/env python3
"""Validate exact current Aitolia and Acarnania bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_aitolia_country.py --check
    python tools/directory_aitolia_country.py --check-live
    python tools/directory_aitolia_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "aitolia_country.json"
)
PARENT = "gr-aitolia"
ROSTER_PAGE = (
    "https://imaa.gr/"
    "%CE%B9%CE%B5%CF%81%CE%BF%CE%B9-%CE%BD%CE%B1%CE%BF%CE%B9-"
    "%CE%BA%CE%B1%CE%B9-%CE%B5%CF%86%CE%B7%CE%BC%CE%B5%CF%81%"
    "CE%B9%CE%BF%CE%B9/"
)
MONASTERIES_PAGE = (
    "https://imaa.gr/"
    "%CE%B9%CE%B5%CF%81%CE%B1%CE%B9-%CE%BC%CE%BF%CE%BD%CE%B1%CE%B9/"
)
MONASTERIES_PDF = (
    "https://imaa.gr/wp-content/uploads/2025/06/"
    "MONASTHRIA-AITOLOAKARNANIAS.pdf"
)
CHURCH_OF_GREECE_PAGE = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/aitolias"
)
CHURCH_OF_GREECE_AGGREGATE = (
    "https://www.ecclesiagreece.gr/greek/holysynod/commitees/relations/"
    "thesmiko_plaisio_paideias.pdf"
)
LEGAL_PAGE = (
    "https://www.e-nomothesia.gr/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-ekklesias-1378-758-2019.html"
)
LEGAL_PDF = (
    "https://ia37rg02wpsa01.blob.core.windows.net/fek/02/2019/"
    "20190201599.pdf"
)


# Current Greek seat | postal code | current Greek dedication |
# body-specific phone displayed in the current official table.
#
# The source has 215 body rows across ten regional tables. A blank seat in
# the rendered source continues the preceding settlement; that continuation
# is resolved here. The one malformed nine-digit Amfilochia value is retained
# only for live reconciliation and held from publication in the ledger.
PARISH_ROWS = r'''
Μεσολόγγι|30200|Ἅγιος Σπυρίδων (Μητροπολιτικός)|2631022414
Μεσολόγγι|30200|Ἁγία Παρασκευῆ|2631022342
Μεσολόγγι|30200|Ἅγιος Ἀθανάσιος|2631023560
Μεσολόγγι|30200|Ἅγιος Παντελεήμων|2631022324
Μεσολόγγι|30200|Ἀπόστολος Παῦλος|2631023988
Ἀγγελόκαστρον|30400|Ἅγ. Ἀπόστολοι|2641093303
Ἅγιος Γεώργιος|30014|Προφ. Ἠλίας|6943021104
Ἅγιος Ἠλίας|30400|Κοίμ. Θεοτόκου|
Ἅγιος Θωμᾶς|30200|Ἀπόστ. Θωμᾶς|2631026316
Ἀγριλιά|30200|Μεταμόρφωσις Σωτῆρος|6983759470
Αἰτωλικόν|30400|Κοίμησις Θεοτόκου|2632022433
Αἰτωλικόν|30400|Παμμέγιστοι Ταξιάρχαι|2632022294
Αἰτωλικόν|30400|Ἅγιος Νεκτάριος|
Γαλατᾶς|30014|Γενέσιον Θεοτόκου|2631041005
Γουριά|30001|Ἅγιος Νικόλαος|2632031171
Ἑλληνικά|30200|Ἅγιος Ἰωάννης|
Εὐηνοχώριον|30014|Ἅγιος Χαράλαμπος|2631039343
Κατοχή|30007|Ἅγιος Δημήτριος|2632091348
Κεφαλόβρυσον|30400|Ἅγιος Γεράσιμος|2632022377
Κουδούνιον|30014|Κοίμησις Θεοτόκου|
Κουτσοχέριον|30014|Ζωοδόχος Πηγή|
Λεσίνιον|30001|Εἰσόδια Θεοτόκου|6978174602
Μαγούλα|30001|Ἅγ. Συμεών Στυλίτης|6945313483
Μᾶστρος|30001|Ἅγιος Νικόλαος|2632081271
Μούσουρα|30200|Ἁγία Παρασκευή|6983759470
Νεοχώριον|30001|Ἅγ. Ἰωάννης Θεολόγος|2632091342
Νεοχώριον|30001|Εὐαγγελισμός Θεοτόκου|2632092002
Πεντάλοφον|30001|Μεταμόρφωσις Σωτῆρος|6986674700
Περιθώριον|30014|Ἁγία Βαρβάρα|6983902322
Ρέτσινα|30200|Κοίμησις Θεοτόκου|6986744114
Σταμνά|30400|Ἅγιος Νικόλαος|6977018497
Σταμνᾶς Λουτρά|30400|Ἁγία Τριάς|6974065368
Στρογγυλοβούνιον|30001|Ζωοδόχος Πηγή|6977479531
Φραγκουλέικα|30400|Ἅγιος Αντώνιος|6936719706
Χρυσοβέργιον|30400|Ἅγ. Διονύσιος Ἀρεοπαγίτης|2641055713
Ἀγρίνιον|30131|Ζωοδόχος Πηγή (Μητροπολιτικός)|2641024665
Ἀγρίνιον|30132|Ἁγία Βαρβάρα|2641044839
Ἀγρίνιον|30027|Ἁγία Παρασκευή|2641026181
Ἀγρίνιον|30132|Ἁγία Τριάς|2641022562
Ἀγρίνιον|30100|Ἅγιος Ἀντώνιος|2641034409
Ἀγρίνιον|30132|Ἅγιος Γεώργιος|2641022871
Ἀγρίνιον|30133|Ἅγιος Γρηγόριος Θεολόγος|2641046046
Ἀγρίνιον|30131|Ἅγιος Δημήτριος|2641022824
Ἀγρίνιον|30027|Ἅγιος Κωνσταντῖνος καί Ἑλένη|2641022552
Ἀγρίνιον|30133|Ἅγιος Χριστοφόρος (Πολιοῦχος)|2641022698
Ἀγρίνιον|30133|Ἀπόστολος Θωμᾶς|2641029865
Ἀβώρανη Νέα|30011|Εὐαγγελισμός Θεοτόκου|
Ἁγία Βαρβάρα|30010|Ἅγιος Νικόλαος|2641025199
Ἁγία Παρασκευή|30100|Ἅγιος Δημήτριος|
Ἅγιος Νικόλαος Τριχωνίδος|30100|Ἅγιος Νικόλαος|2641058338
Γιαννούζιον|30100|Ἅγιος Ἀθανάσιος|2641058256
Γουριώτισσα|30100|Ἅγιος Δημήτριος|6983131145
Διαμαντέικα|30100|Ἅγιοι Ἀπόστολοι|2641050396
Δοκίμιον|30100|Γενέσιον Προδρόμου|2641024660
Ἐλαιόφυτον|30100|Ἅγιος Βασίλειος|2641025371
Καλύβια|30100|Ἅγιος Νικόλαος|2641095272
Καμαρούλα|30100|Ἅγιος Γεώργιος|2641044530
Καστράκιον|30100|Ἁγία Κυριακή|6980550611
Κερασέα|30100|Ἅγιος Ἀθανάσιος|
Κλεισορρεύματα|30400|Ἅγιος Ἀλέξιος|2641097467
Κυψέλη (Σφήνα)|30100|Ἅγιος Παντελεήμων|2641071170
Λεπενοῦ|30100|Ἅγιος Γεώργιος|2641092359
Λυσιμαχία|30400|Ἁγία Παρασκευή|6984744519
Ματσούκιον|30100|Ἅγιος Γεώργιος|2641047834
Μεγάλη Χώρα|30100|Ἀπόστολος Παῦλος|2641026133
Νεάπολις|30100|Ἅγιος Δημήτριος|2641091269
Ὄχθια|30100|Εὐαγγελισμός Θεοτόκου|6984047343
Παλαιομάνινα|30001|Ἅγ. Κων/νος κ Ἑλένη|2632041477
Παναιτώλιον|30003|Ἁγία Παρασκευή|6974522966
Παναιτώλιον|30003|Ἁγία Τριάδα|2641051226
Προσήλια|30010|Ἁγία Παρασκευή|
Πύργιον|30100|Ἅγιος Ἀθανάσιος|2641025511
Ρίγανη|30001|Ἅγιος Δημήτριος|
Σιτόμενα|30010|Κοίμησις Θεοτόκου|
Σκουτερά|30100|Ἅγιος Νικόλαος|2641042253
Σκουτεσιάδα|30100|Ἅγιος Νικόλαος|6936584642
Σπολάιτα|30100|Κοίμησις Θεοτόκου|2641091309
Στρᾶτος|30100|Ἅγιος Νικόλαος|2641071325
Ἀμφιλοχία|30500|Ἅγιος Ἀθανάσιος|264202334
Ἀμφιλοχία|30500|Ἁγία Παρασκευή|2642023121
Ἁγία Τριάδα Βάλτου|30500|Ἁγία Τριάς|
Ἀμπελάκιον|30500|Ἅγιοι Θεόδωροι|6983943308
Ἀνοιξιάτικον|30500|Ἅγιος Ἀθανάσιος|6978670866
Ἀριάδα|30500|Ἅγιος Ἀθανάσιος|
Βαρετάδα|30500|Ἅγιος Δημήτριος|2647031951
Κάμπος Ἀμπελακίου|30500|Ἅγιος Νεκτάριος|6976514652
Κεχρινιά|30500|Ἅγιος Βησσαρίων|6974353739
Κομποθέκλα|30500|Ἅγιος Νικόλαος ἐν Βουνένοις|2642081353
Λουτρόν|30500|Ἅγιος Νικόλαος|6981094844
Μενίδιον|30016|Ἀπόστολος Παῦλος|2681067611
Μπούκα|30500|Ἅγιος Σπυρίδων|6977966366
Πτελέα|30500|Ἅγιος Γεώργιος|
Σαρδήνια|30500|Ἁγία Τριάς|
Σπᾶρτον|30500|Ἅγιος Ἀθανάσιος|6945715203
Στᾶνος|30500|Ἅγιος Δημήτριος|2642041275
Συκούλα|47040|Ἅγιος Δημήτριος|2681088507
Φλωριάδα|47040|Ἁγία Τριάς|2681077548
Ἀστακός|30006|Ἅγιος Νικόλαος|2646041230
Ἀγράμπελον|30006|Παμμέγιστοι Ταξιάρχαι|6977352229
Βασιλόπουλον|30006|Ἅγιος Γεώργιος|6907775521
Βλιζιανά|30003|Ἅγιος Νικόλαος|
Καραϊσκάκης|30006|Ἅγιος Ἀθανάσιος|6973414923
Μαχαιρᾱς|30009|Ἅγιος Γεώργιος|6983699702
Μπαμπίνη|30009|Ἅγιος Νικόλαος|
Πρόδρομος|30006|Ἅγιος Ἰωάννης|6977352229
Σκουρτοῦ|30009|Ἅγιος Δημήτριος|
Φυτεῖαι|30009|Ἅγιος Ἰωάννης ὁ Θεολόγος|2646022021
Χρυσοβίτσα|30006|Ἅγιος Γεώργιος|
Βόνιτσα|30002|Ἅγιος Σπυρίδων|2643022451
Ἅγ. Νικόλαος Βονίτσης|30002|Ἅγ. Νικόλαος ὁ ἐν Βουνένοις|2643081297
Δρυμός|30002|Ἅγιος Δημήτριος|6974094565
Θύρρειον|30002|Κοίμησις Θεοτόκου|6976178071
Μοναστηράκιον|30013|Ἅγιος Ἰωάννης ὁ Θεολόγος|2643031130
Πάλαιρος|30012|Ἁγία Παρασκευή|2643041230
Παληάμπελα|30002|Ἅγιος Ἀθανάσιος|6986278914
Περατιά|30002|Γενέσιον Προδρόμου|6980382213
Πλαγιά|30002|Ἅγιος Δημήτριος|6940535444
Πογωνιά|30002|Παναγία Φανερωμένη|
Σκλάβαινα|30012|Ἅγιος Βλάσιος ὁ Ἀκαρνᾶν|
Θέρμον|30008|Κοίμησις Θεοτόκου|2644022409
Θέρμον|30008|Ἅγιος Δημήτριος|2644023040
Ἀβαρῖκος|30008|Ἁγία Παρασκευή|6973352682
Ἁγία Σοφία|30008|Κοίμησις Θεοτόκου|2644051203
Ἅγιος Θεόδωρος|30008|Κοίμησις Θεοτόκου|
Ἀετόπετρα|30008|Ἅγιος Νικόλαος|
Ἀμβρακιά|30008|Παμμέγιστοι Ταξιάρχαι|
Ἀνάληψις|30008|Ἅγιος Νικόλαος|6938947686
Ἀργυροπηγάδιον|30008|Ἅγιος Δημήτριος|
Δρυμών|30008|Ἅγιος Γεώργιος|2644051497
Καλλιθέα|30008|Ἁγία Παρασκευή|
Καλούδιον|30008|Ἁγία Παρασκευή|6972015099
Κάμπος Ἀναλήψεως|30008|Ἅγιος Γεώργιος|
Κοκκινόβρυσις|30008|Μεταμόρφωσις Σωτῆρος|
Κόνισκα|30008|Ἅγιος Νικόλαος|2644023852
Κρυονέριον|30010|Ἁγία Τριάς|
Λαμπίριον|30008|Ἅγιος Δημήτριος|
Λευκόν|30008|Ἅγιος Γεώργιος|
Μάνδρα|30008|Ἁγία Παρασκευή|
Μεγαδένδρον|30008|Εἰσόδια Θεοτόκου|
Νεροχώριον|30008|Ἅγιος Ἀθανάσιος|
Πάμφιον|30008|Ἅγιος Ἰωάννης|2635031520
Πετροχώριον|30008|Ἅγιος Δημήτριος|6974088254
Σιταράλωνα|30008|Ἅγιος Παντελεήμων|2635031641
Σπαρτιᾶς|30008|Ἁγία Τριάς|2644061398
Στριγανιά|30008|Ἁγία Παρασκευή|
Ταξιάρχης|30008|Κοίμησις Θεοτόκου|
Χαλίκιον|30008|Μεταμόρφωσις Σωτήρος|
Χρυσοβίτσα Ἄνω|30008|Ἅγιος Γεώργιος|
Χρυσοβίτσα Κάτω|30008|Ἅγιος Νικόλαος|2644023471
Ἀγρίδιον|30017|Ἅγιοι Θεόδωροι|
Ἀλευράδα|30018|Ἅγιος Γεώργιος|6986633224
Ἀμοργιανοί|30018|Γενέσιον Θεοτόκου|2641033373
Ἀρωνιάδα|30017|Ἀπόστολος Θωμᾶς|
Αὐλάκιον|30017|Ἅγιος Κωνστ/νος καί Ἑλένη|
Βαλμάδα|47040|Ἅγιος Δημήτριος|
Βρουβιανά|30017|Κοίμησις Θεοτόκου|
Γιαννόπουλοι|30018|Ἅγιος Γεώργιος|2647051326
Ἐμπεσός|30017|Μεταμόρφωσις Σωτῆρος|2642051894
Θεριακήσιον|47040|Παμμέγιστοι Ταξιάρχαι|
Θύαμος|30017|Ἅγιοι Ἀνάργυροι|6982792151
Μαλεσιάδα|30018|Ἅγιος Κωνσταντῖνος|6944645999
Μπαμπαλιόν|30018|Κοίμησις Θεοτόκου|
Πατιόπουλον|30017|Ἅγιος Γεώργιος|
Πετρώνα|30018|Κοίμησις Θεοτόκου|
Περδικάκιον|30017|Κοίμησις Θεοτόκου|2647031620
Ρουπακιά|30017|Ἁγία Παρασκευή|
Σταθᾶς|30017|Κοίμησις Θεοτόκου|2647031354
Τρίκλινον|30017|Μεταμόρφωσις Σωτῆρος|
Χαλκιόπουλοι|30017|Γενέσιον Προδρόμου|6942835601
Κατούνα|30004|Ἅγιος Ἀθανάσιος|2646031758
Ἅγ. Νικόλαος Κατούνης|30004|Ἅγ. Νικόδημος Ἁγιορείτης|
Ἀετός|30004|Ἅγιος Σπυρίδων|
Ἀρχοντοχώριον|30019|Ἅγιος Σπυρίδων|6998020359
Βάρνακας|30019|Ἅγιος Γεράσιμος|
Κανδήλα Ἄνω|30019|Ἅγιος Ἀνδρέας|
Κανδήλα Κάτω|30019|Ζωοδόχος Πηγή|2646051529
Κομπωτή|30004|Ἅγιος Ἱερόθεος|
Κωνωπίνα|30004|Εἰσόδια Θεοτόκου|2641047768
Μύτικας|30019|Ἅγιος Νικόλαος|6955405546
Παναγούλα|30019|Κοίμησις Θεοτόκου|
Παπαδᾶτον|30009|Ἅγιος Νικόλαος|2641029827
Τρῦφος|30004|Ἅγιος Νικόλαος|
Ἅγιος Ἀνδρέας|30015|Ἅγιος Ἀνδρέας|6942668145
Ἄκρες|30015|Ἅγιος Δημήτριος|
Γαβαλοῦ|30015|Ἁγία Φωτεινή Σαμαρείτις|2635042742
Γραμματικοῦ|30015|Ἀπόστολος Φίλιππος|2635041376
Δαφνιᾶς|30015|Ἅγιος Ἰωάννης|6907168038
Ζευγαράκι Ἄνω|30011|Ἅγιος Δημήτριος|6948615386
Ζευγαράκι Κάτω|30011|Ἅγιοι Ἀπόστολοι|6934270372
Κεράσοβο Ἄνω|30011|Κοίμησις Θεοτόκου|6951595363
Κεράσοβο Κάτω|30011|Ἅγιος Ἰωάννης Χρυσόστομος|6936712238
Κουρτελέικα|30015|Ἅγιος Κωνστ/νος καί Ἑλένη|6972150386
Μακρυνοῦ Ἄνω|30015|Ἅγιος Ἀθανάσιος|6946125041
Μακρυνοῦ Κάτω|30015|Ἅγιος Λουκᾶς|
Ματαράγκα|30011|Ἅγιος Γεώργιος|2635022536
Μεσάριστα|30015|Ἅγιος Νικόλαος|2641044620
Παλαιοχώριον (Καψωράχη)|30015|Εὐαγγελιστής Μᾶρκος|
Παπαδάτες|30011|Ἅγιος Κωνστ/νος καί Ἑλένη|2635022355
Ποταμούλα|30015|Ἅγιος Νικόλαος|
Τριχώνιον|30015|Ἅγία Παρασκευή|6975771559
Παραβόλα|30010|Ἅγιος Δημήτριος|2641061401
Ἀφρᾶτον|30010|Ἅγιος Ἐλευθέριος|
Βαρειά|30010|Ἅγιος Κωνστ/νος καί Ἑλένη|6945851109
Βλοχός Ἄνω|30010|Ἅγιος Νικόλαος|
Καινούριον|30005|Ἅγιος Δημήτριος|2641061407
Καινούριον|30005|Ἅγιος Νικόλαος|2641061254
Κυραβγένα|30010|Ἁγία Τριάς|6949085902
Μυρτιά Ἄνω|30008|Ἅγιος Ἰωάννης Θεολόγος|2641050260
Μυρτιά Κάτω|30008|Προφήτης Ἠλίας|6974119765
Νερομάνα|30010|Κοίμησις Θεοτόκου|2644061056
Παληοκαρυά|30010|Ἅγιος Δημήτριος|2641061906
Παντάνασσα|30010|Εἰσόδια Θεοτόκου|6973977286
Περιστέριον|30010|Κοίμησις Θεοτόκου|6949912637
Πλατανιᾶς|30010|Κοίμησις Θεοτόκου|6949912637
Τραγάνα|30010|Παμμέγιστοι Ταξιάρχαι|2641050130
'''


DEDICATIONS = {
    "αγ. αποστολοι": "Holy Apostles",
    "αγ. διονυσιος αρεοπαγιτης": "Saint Dionysius the Areopagite",
    "αγ. ιωαννης θεολογος": "Saint John the Theologian",
    "αγ. κων/νος κ ελενη": "Saints Constantine and Helen",
    "αγ. νικοδημος αγιορειτης": "Saint Nikodemos the Hagiorite",
    "αγ. νικολαος ο εν βουνενοις": "Saint Nicholas of Vounena",
    "αγ. συμεων στυλιτης": "Saint Symeon the Stylite",
    "αγια βαρβαρα": "Saint Barbara",
    "αγια κυριακη": "Saint Kyriaki",
    "αγια παρασκευη": "Saint Paraskevi",
    "αγια τριαδα": "Holy Trinity",
    "αγια τριας": "Holy Trinity",
    "αγια φωτεινη σαμαρειτις": "Saint Photini the Samaritan Woman",
    "αγιοι αναργυροι": "Holy Unmercenaries",
    "αγιοι αποστολοι": "Holy Apostles",
    "αγιοι θεοδωροι": "Holy Theodores",
    "αγιος αθανασιος": "Saint Athanasius",
    "αγιος αλεξιος": "Saint Alexios",
    "αγιος ανδρεας": "Saint Andrew",
    "αγιος αντωνιος": "Saint Anthony",
    "αγιος βασιλειος": "Saint Basil",
    "αγιος βησσαριων": "Saint Bessarion",
    "αγιος βλασιος ο ακαρναν": "Saint Blasios the Acarnanian",
    "αγιος γερασιμος": "Saint Gerasimos",
    "αγιος γεωργιος": "Saint George",
    "αγιος γρηγοριος θεολογος": "Saint Gregory the Theologian",
    "αγιος δημητριος": "Saint Demetrius",
    "αγιος ελευθεριος": "Saint Eleftherios",
    "αγιος ιεροθεος": "Saint Hierotheos",
    "αγιος ιωαννης": "Saint John",
    "αγιος ιωαννης θεολογος": "Saint John the Theologian",
    "αγιος ιωαννης ο θεολογος": "Saint John the Theologian",
    "αγιος ιωαννης χρυσοστομος": "Saint John Chrysostom",
    "αγιος κωνστ/νος και ελενη": "Saints Constantine and Helen",
    "αγιος κωνσταντινος": "Saint Constantine",
    "αγιος κωνσταντινος και ελενη": "Saints Constantine and Helen",
    "αγιος λουκας": "Saint Luke",
    "αγιος νεκταριος": "Saint Nectarios",
    "αγιος νικολαος": "Saint Nicholas",
    "αγιος νικολαος εν βουνενοις": "Saint Nicholas of Vounena",
    "αγιος παντελεημων": "Saint Panteleimon",
    "αγιος σπυριδων": "Saint Spyridon",
    "αγιος σπυριδων (μητροπολιτικος)": "Saint Spyridon",
    "αγιος χαραλαμπος": "Saint Charalambos",
    "αγιος χριστοφορος (πολιουχος)": "Saint Christopher",
    "αποστ. θωμας": "Apostle Thomas",
    "αποστολος θωμας": "Apostle Thomas",
    "αποστολος παυλος": "Apostle Paul",
    "αποστολος φιλιππος": "Apostle Philip",
    "γενεσιον θεοτοκου": "Nativity of the Theotokos",
    "γενεσιον προδρομου": "Nativity of Saint John the Forerunner",
    "εισοδια θεοτοκου": "Entrance of the Theotokos into the Temple",
    "ευαγγελισμος θεοτοκου": "Annunciation of the Theotokos",
    "ευαγγελιστης μαρκος": "Evangelist Mark",
    "ζωοδοχος πηγη": "Life-Giving Spring",
    "ζωοδοχος πηγη (μητροπολιτικος)": "Life-Giving Spring",
    "κοιμ. θεοτοκου": "Dormition of the Theotokos",
    "κοιμησις θεοτοκου": "Dormition of the Theotokos",
    "μεταμορφωσις σωτηρος": "Transfiguration of the Savior",
    "παμμεγιστοι ταξιαρχαι": "Holy Archangels",
    "παναγια φανερωμενη": "Panagia Faneromeni",
    "προφ. ηλιας": "Prophet Elijah",
    "προφητης ηλιας": "Prophet Elijah",
}


# English dedication | English seat | Greek local title | rank | phones
MONASTIC_ROWS = r'''
Entrance of the Theotokos into the Temple|Myrtia, Thermo|Ἱερά Μονή Εἰσοδίων τῆς Θεοτόκου Μυρτιᾶς Θέρμου|Monastery|2644051497
Panagia Lesiniotissa|Lesinio|Ἱερά Μονή Παναγίας Λεσινιωτίσσης|Monastery|6985574857,6949015576
Saint Paraskevi|Sardinia, Amfilochia|Ἱερά Μονή Ἁγίας Παρασκευῆς Σαρδινίων Ἀμφιλοχίας|Monastery|6981094844
Panagia Eleoussa|Kleisoura, Messolonghi|Ἱερά Μονή Παναγίας Ἐλεούσης Κλεισούρας Μεσολογγίου|Monastery|2632022386
Nativity of the Theotokos|Romvi, Akarnania|Ἱερά Μονή Γενεσίου τῆς Θεοτόκου Ρόμβου Ἀκαρνανίας|Monastery|2643022814
Dormition of the Theotokos|Vlochos, Paravola|Ἱερά Μονή Κοιμήσεως τῆς Θεοτόκου Βλοχοῦ Παραβόλας|Monastery|2641025199
Saint Paraskevi|Mandra, Thermo|Ἱερά Μονή Ἁγίας Παρασκευῆς Μάνδρας Θέρμου|Monastery|2644024195,6946761587
Dormition of the Theotokos|Varetada|Ἱερά Μονή Κοιμήσεως τῆς Θεοτόκου Βαρετάδας|Monastery|6986633224
Ascension of Saint John the Forerunner|Dervekista, Thermo|Ἱερά Μονή Τιμίου Προδρόμου Ἀναλήψεως Δερβεκίστης Θέρμου|Monastery|2644100000,2644031200
Nativity of the Theotokos|Katerinou, Makryneia|Ἱερά Μονή Γενεσίου τῆς Θεοτόκου Κατερινοῦς Μακρυνείας|Monastery|2635041244
Saint Nicholas|Katouna, Xiromero|Ἱερά Μονή Ἁγίου Νικολάου Κατούνης Ξηρομέρου|Monastery|6983905944
Saint George|Ellinika, Messolonghi|Ἱερά Μονή Ἁγίου Γεωργίου Ἑλληνικῶν Μεσολογγίου|Monastery|2631025923
Dormition of the Theotokos|Ligovitsi, Fyteies|Ἱερά Μονή Κοιμήσεως τῆς Θεοτόκου Λιγοβιτσίου Φυτειῶν|Monastery|2646093300
Transfiguration of the Savior Pantokrator|Angelokastro|Ἱερά Μονή Μεταμορφώσεως τοῦ Σωτῆρος Παντοκράτορος Ἀγγελοκάστρου|Monastery|2641093220
Nativity of the Theotokos|Retha, Amfilochia|Ἱερά Μονή Γενεσίου τῆς Θεοτόκου Ρέθα Ἀμφιλοχίας|Monastery|2642051800,6944211509
Saint Demetrius|Palairos|Ἱερά Μονή Ἁγίου Δημητρίου Παλαίρου|Monastery|2643041427
Saint Symeon|Messolonghi|Ἱερά Μονή Ἁγίου Συμεών Μεσολογγίου|Monastery|2631022515
Saint Demetrius|Drymos, Vonitsa|Ἱερά Μονή Ἁγίου Δημητρίου Δρυμοῦ Βονίτσης|Monastery|2643091230
Deposition of the Holy Belt of the Theotokos|Lykourissa, Skoutera|Ἱερά Μονή Καταθέσεως Τιμίας Ζώνης Ὑπεραγίας Θεοτόκου Λυκουρίσσης Σκουτερᾶς|Monastery|2641042410
Saint Kosmas of Aitolia|Thermo|Ἱερά Μονή Ἁγίου Κοσμᾶ τοῦ Αἰτωλοῦ|Monastery|2644024050
Annunciation of the Theotokos|Paravola|Ἱερά Μονή Εὐαγγελισμοῦ τῆς Θεοτόκου Παραβόλας|Monastery|2641062692
Transfiguration of the Savior|Tsoukalades, Paravola|Ἱερόν Ἡσυχαστήριον Μεταμορφώσεως τοῦ Σωτῆρος Τσουκαλάδων Παραβόλας|Hermitage|2641062052
'''


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "body"


GREEK = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}


def transliterate(value):
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


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def parse_table(raw, width, label):
    result = []
    for index, line in enumerate(raw.strip().splitlines(), 1):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != width:
            raise ValueError("%s row %d has %d fields" % (
                label, index, len(parts)))
        result.append(parts)
    return result


DEDICATIONS = {unicase(key): value for key, value in DEDICATIONS.items()}
PARISH_PARSED = parse_table(PARISH_ROWS, 4, "parish")
MONASTIC_PARSED = parse_table(MONASTIC_ROWS, 5, "monastic")


def build_rows():
    rows = []
    malformed = []
    for index, (seat_local, postal, dedication_local,
                raw_phone) in enumerate(PARISH_PARSED, 1):
        key = unicase(dedication_local)
        dedication = DEDICATIONS.get(key)
        if not dedication:
            raise ValueError("missing English dedication for parish row %d" %
                             index)
        seat = transliterate(seat_local)
        rank = (
            "Metropolitan Church"
            if "μητροπολιτικ" in key else "Parish Church"
        )
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-aitolia-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (dedication_local, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat_local, "Τ.Κ. %s" % postal],
            "sources": [ROSTER_PAGE, LEGAL_PDF],
        }
        if raw_phone:
            if len(raw_phone) == 10:
                item["phones"] = ["+30-" + raw_phone]
                item["contact_sources"] = [ROSTER_PAGE]
                item["contact_checked"] = CHECKED
            else:
                malformed.append((seat_local, dedication_local, raw_phone))
        rows.append(item)
    if malformed != [("Ἀμφιλοχία", "Ἅγιος Ἀθανάσιος", "264202334")]:
        raise ValueError("unexpected malformed official phone values")

    for raw in MONASTIC_PARSED:
        dedication, seat, local, rank, raw_phones = raw
        index = len(rows) + 1
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-aitolia-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "phones": ["+30-" + value for value in raw_phones.split(",")],
            "sources": [MONASTERIES_PAGE, MONASTERIES_PDF],
            "contact_sources": [MONASTERIES_PAGE, MONASTERIES_PDF],
            "contact_checked": CHECKED,
        }
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}


EXPECTED_TOTAL = 237
EXPECTED_OWNER_COUNTS = {PARENT: 237}
EXPECTED_KINDS = {"monastery": 22, "parish": 215}
EXPECTED_RANKS = {
    "Hermitage": 1,
    "Metropolitan Church": 2,
    "Monastery": 21,
    "Parish Church": 213,
}
EXPECTED_CONTACT_BODIES = 174
EXPECTED_PHONE_BODIES = 174
EXPECTED_PHONE_VALUES = 178
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 237
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
        "imaa.gr", "www.imaa.gr",
        "e-nomothesia.gr", "www.e-nomothesia.gr",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
        "ia37rg02wpsa01.blob.core.windows.net",
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
        raise ValueError("Aitolia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Aitolia candidate ledger date drifted")
    expected_summary = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "exact_current_parish_rows": 215,
        "exact_current_monastic_rows": 22,
        "parish_kind_rows": 215,
        "monastery_kind_rows": 22,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Aitolia ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Aitolia ledger lacks %s" % key)
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        for entry in ledger[key]:
            if any(FORBIDDEN_PUNCTUATION.search(text)
                   for text in walk_strings(entry)):
                raise ValueError("Aitolia ledger contains forbidden punctuation")
            for source_url in entry.get("sources") or []:
                validate_url(source_url, entry.get("candidate_id") or key)


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
        if re.search(r"\b(Ηγούμενος|Ηγουμένη|Αρχιμ|Πρωτοπρ)\b",
                     item["local"], re.I):
            raise ValueError("%s exposes a clergy marker" % row_id)
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
        raise ValueError("Aitolia English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Aitolia English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Aitolia parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Aitolia kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Aitolia rank totals drifted: %r" %
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
        raise ValueError("Aitolia contact coverage drifted: %r" %
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
    with urlopen(request, timeout=90) as response:
        if response.status >= 400:
            raise ValueError("%s returned HTTP %s" % (url, response.status))
        return (
            response.headers.get("Content-Type", "").lower(),
            response.read(),
            response.geturl(),
        )


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.depth += 1
            if self.depth == 1:
                self.table = []
        elif self.depth == 1 and tag == "tr":
            self.row = []
        elif self.depth == 1 and tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif self.depth == 1 and tag == "br" and self.cell is not None:
            self.cell.append(" ")

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if (self.depth == 1 and tag in ("td", "th") and
                self.cell is not None):
            value = html.unescape("".join(self.cell))
            self.row.append(re.sub(r"\s+", " ", value).strip())
            self.cell = None
        elif self.depth == 1 and tag == "tr" and self.row is not None:
            if any(self.row):
                self.table.append(self.row)
            self.row = None
        elif tag == "table":
            if self.depth == 1:
                self.tables.append(self.table)
                self.table = None
            self.depth -= 1


def parse_live_roster(payload):
    parser = TableParser()
    parser.feed(payload.decode("utf-8", "replace"))
    if len(parser.tables) != 10:
        raise ValueError("current roster expected ten regional tables")
    records = []
    current_seat = ""
    for table in parser.tables:
        for cells in table:
            if len(cells) != 4 or "Τ.Κ." in cells[0]:
                continue
            source = cells[0].replace("\u2013", " - ").replace(
                "\u2014", " - ")
            source = re.sub(r"\s+", " ", source).strip()
            match = re.match(
                r"^(.*?)\s*-?\s*(\d{5})\s*-?\s*(.+)$", source
            )
            if not match:
                raise ValueError("unparsed current parish row: %s" % cells[0])
            seat, postal, dedication = match.groups()
            seat = seat.strip(" -")
            if seat:
                current_seat = seat
            if not current_seat:
                raise ValueError("current roster begins with a continued seat")
            phone_digits = re.sub(r"\D", "", cells[1])
            records.append((
                current_seat, postal, dedication.strip(" -"), phone_digits
            ))
    return records


def assert_html_markers(url, markers, label):
    content_type, payload, unused = fetch_source(url)
    if "html" not in content_type:
        raise ValueError("%s returned a non-HTML response" % label)
    text = normalize_source_text(payload.decode("utf-8", "replace"))
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("%s source marker drifted: %s" % (label, marker))


def check_live_sources():
    content_type, payload, unused = fetch_source(ROSTER_PAGE)
    if "html" not in content_type:
        raise ValueError("current roster returned a non-HTML response")
    live = parse_live_roster(payload)
    expected = [tuple(row) for row in PARISH_PARSED]
    if live != expected:
        missing = sorted(set(expected) - set(live))
        extra = sorted(set(live) - set(expected))
        raise ValueError(
            "current parish reconciliation drifted: missing %r extra %r" %
            (missing[:5], extra[:5])
        )
    assert_html_markers(
        MONASTERIES_PAGE,
        (
            "Παναγίας Ἐλεούσης Κλεισούρας Μεσολογγίου",
            "Παναγίας Λεσινιωτίσσης", "6949015576",
            "Ἁγίας Παρασκευῆς Μάνδρας Θέρμου",
            "Γενεσίου τῆς Θεοτόκου Κατερινοῦς Γαβαλοῦς",
            "Ἁγίου Νικολάου Κατούνης Ξηρομέρου", "6983905944",
            "Ἱερόν Ἡσυχαστήριον Μεταμορφώσεως τοῦ Σωτῆρος",
        ),
        "current monastery roster",
    )
    content_type, monastery_pdf, unused = fetch_source(MONASTERIES_PDF)
    if not monastery_pdf.startswith(b"%PDF") or len(monastery_pdf) < 30000000:
        raise ValueError("official 2025 monastery guide is not the expected PDF")
    assert_html_markers(
        CHURCH_OF_GREECE_PAGE,
        ("Αἰτωλίας καί Ἀκαρνανίας", "Δαμασκηνός", "imaa.gr"),
        "Church of Greece profile",
    )
    assert_html_markers(
        LEGAL_PAGE,
        ("1378/758/2019", "ΦΕΚ 1599/Β/10-5-2019",
         "Αιτωλίας και Ακαρνανίας"),
        "legal roster page",
    )
    content_type, legal_pdf, unused = fetch_source(LEGAL_PDF)
    if not legal_pdf.startswith(b"%PDF") or len(legal_pdf) < 200000:
        raise ValueError("official legal roster is not the expected PDF")
    content_type, aggregate_pdf, unused = fetch_source(
        CHURCH_OF_GREECE_AGGREGATE
    )
    if not aggregate_pdf.startswith(b"%PDF") or len(aggregate_pdf) < 100000:
        raise ValueError("Church of Greece aggregate is not the expected PDF")


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
            "Aitolia and Acarnania: %d exact current bodies; %d carry "
            "public body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Aitolia: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
