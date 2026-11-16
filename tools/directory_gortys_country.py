#!/usr/bin/env python3
"""Build the exact current Gortys and Megalopolis subordinate body roster."""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PARENT = "gr-gortys"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "gortys_country.json"
SHARED_GREECE = HERE / "directory_greece_country.py"

BASE = "https://imgortmeg.gr"
WP_API = BASE + "/wp-json/wp/v2"
ADMIN_URL = BASE + "/dioikisi/"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2020_martios.pdf"
PROFILE_URL = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "gortynos-kai-megalopoleos"
)

REGIONS = {
    "Dimitsana": (2289, 22, BASE + "/arxieratiki-periferia-dimitsanis/"),
    "Lagkadia": (2905, 9, BASE + "/arxieratiki-perifereia-lagadiwn/"),
    "Vytina": (2913, 8, BASE + "/arxieratiki-periferia-bitinis/"),
    "Valtetsiniko": (2926, 8, BASE + "/arxieratiki-periferia-baltesinikou/"),
    "Kontovazaina": (2931, 9, BASE + "/arxieratiki-periferia-kontovazainas/"),
    "Tropaia": (2936, 26, BASE + "/arxieratiki-periferia-stayrodromioy-tropaiwn/"),
    "Velimachi": (3107, 7, BASE + "/arxieratiki-periferia-velimaxiou/"),
    "Megalopolis": (3122, 36, BASE + "/arxieratiki-periferia-megaloupolews/"),
    "Eastern Falaisia": (3144, 16, BASE + "/arxieratiki-periferia-anatolikis-falaisias/"),
    "Western Falaisia": (3150, 10, BASE + "/arxieratiki-periferia-dytikis-falaisias/"),
    "Karytaina": (3171, 17, BASE + "/arxieratiki-periferia-karutainas/"),
}


# Region | exact current table identity | seat | exact public phone values.
PARISH_DATA = r"""
Dimitsana|Δημητσάνα - Aγ. Κυριακή|Δημητσάνα|+30 697-167-5803
Dimitsana|Δημητσάνα - Ἅγ. Χαράλαμπος|Δημητσάνα|+30 697-167-5803
Dimitsana|Αράχωβα - Ἅγ. Γεώργιος|Αράχωβα|+30 693-226-6401
Dimitsana|Βλόγγος - Ἅγ. Γεώργιος|Βλόγγος|+30 697-167-5803
Dimitsana|Ελληνικό - Προφ. Ηλίας|Ελληνικό|+30 697-229-6924
Dimitsana|Ζάτουνα - Κοίμ. Θεοτόκου|Ζάτουνα|+30 699-347-7338
Dimitsana|Ζυγοβίστιον - Μεταμ. Σωτήρος|Ζυγοβίστιον|+30 697-643-6165
Dimitsana|Κακουρέϊκα - Ἅγ. Βασίλειος|Κακουρέϊκα|+30 690-627-5212
Dimitsana|Κοκορά - Προφήτης Ηλίας|Κοκορά|+30 693-226-6401
Dimitsana|Λυκούρεση - Ζωοδ. Πηγή|Λυκούρεση|+30 694-097-7528
Dimitsana|Λυσσαρέα - Ἅγ. Νικόλαος|Λυσσαρέα|+30 694-481-2344
Dimitsana|Μάρκου - Τίμιος Πρόδρομος|Μάρκου|+30 697-438-9081
Dimitsana|Μελισσόπετρα - Ἅγ. Αθανάσιος|Μελισσόπετρα|+30 699-347-7388
Dimitsana|Παλαιοχώριον - Ἅγ. Απόστολοι|Παλαιοχώριον|+30 27950-31273
Dimitsana|Παλούμπα - Ἅγ. Γεώργιος|Παλούμπα|+30 697-757-1361
Dimitsana|Παναγιά - Ἅγ. Νικόλαος|Παναγιά|+30 694-481-2344
Dimitsana|Ράφτη - Ἅγ. Δημήτριος|Ράφτη|+30 693-226-6401
Dimitsana|Ριζοσπηλιά - Ἅγ. Νικόλαος|Ριζοσπηλιά|+30 699-347-7338
Dimitsana|Σαρακίνιον Ηρ. - Κοιμ. Θεοτόκου|Σαρακίνιον Ηρ.|+30 693-685-8221
Dimitsana|Σέρβου - Κοιμ. Θεοτόκου|Σέρβου|+30 699-474-9018
Dimitsana|Στεμνίτσα - Ἅγ. Γεώργιος|Στεμνίτσα|+30 698-164-2306
Dimitsana|Στεμνίτσα - Αγ. Παρασκευή|Στεμνίτσα|+30 698-164-2306
Lagkadia|Αετορράχη - Μετ. Σωτήρος|Αετορράχη|+30 697-280-8311
Lagkadia|Λαγκάδια - Παμ. Ταξιάρχαι|Λαγκάδια|+30 694-446-2610
Lagkadia|Λαγκάδια - Τίμ. Πρόδρομος|Λαγκάδια|+30 697-482-5099
Lagkadia|Λαγκάδια - Άγ. Άπόστολοι|Λαγκάδια|+30 694-446-2610
Lagkadia|Λευκοχώριον - Άγ. Δημήτριος|Λευκοχώριον|+30 698-475-0738
Lagkadia|Ράδου - Κοιμ. Θεοτόκου|Ράδου|+30 697-327-9780
Lagkadia|Σβόρνα - Αγ. Μαρίνα|Σβόρνα|+30 697-327-9780
Lagkadia|Τουθόα - Άγ. Παρασκευή|Τουθόα|+30 697-908-3953
Lagkadia|Φτεριά - Άγ. Γεώργιος|Φτεριά|+30 697-328-3467
Vytina|Ἀγρίδιον - Ἁγ. Τριάς|Ἀγρίδιον|+30 690-717-8785
Vytina|Βυτίνα - Άγ. Τρύφων|Βυτίνα|+30 697-298-7035
Vytina|Ελάτη - Κοιμ. Θεοτόκου|Ελάτη|+30 697-167-5803
Vytina|Καμενίτσα - Άγ. Γεώργιος|Καμενίτσα|+30 694-946-4195
Vytina|Νυμφασία - Ἁγ. Τριάς|Νυμφασία|+30 697-428-5040
Vytina|Παναγίτσα - Ἀνάληψις Κυρίου|Παναγίτσα|+30 697-202-9176
Vytina|Πράσινο - Άγ. Κωνσταντίνος|Πράσινο|+30 699-323-8496
Vytina|Πυργάκι - Τίμιος Πρόδρομος|Πυργάκι|+30 698-143-9129
Valtetsiniko|Ἀμυγδαλέα - Κοιμ. Θεοτόκου|Ἀμυγδαλέα|+30 699-323-8496
Valtetsiniko|Βαλτεσινίκον - Ἅγ. Γεώργιος|Βαλτεσινίκον|+30 699-701-0771
Valtetsiniko|Βαλτεσινίκον - Ἅγ. Θεόδωροι|Βαλτεσινίκον|+30 699-701-0771
Valtetsiniko|Δρακοβούνιον - Ἅγ. Γεώργιος|Δρακοβούνιον|+30 690-717-8785
Valtetsiniko|Θεόκτιστον - Ἅγ. Θεόδωροι|Θεόκτιστον|+30 698-594-2833
Valtetsiniko|Κερπινή - Ἁγ. Τριάς|Κερπινή|+30 690-717-8785
Valtetsiniko|Λάστα - Ἅγ. Γεώργιος|Λάστα|+30 697-482-5099
Valtetsiniko|Μαγούλιανα - Τίμ. Πρόδρομος|Μαγούλιανα|+30 698-745-8920
Kontovazaina|Βάχλια - Ἅγ. Βασίλειος|Βάχλια|+30 697-455-2077
Kontovazaina|Βάχλια - Ἁγ. Μαρίνα|Βάχλια|+30 697-455-2077
Kontovazaina|Δήμητρα - Ἅγ. Νικόλαος|Δήμητρα|+30 697-600-7359
Kontovazaina|Κοντοβάζαινα - Ἅγ. Γεώργιος|Κοντοβάζαινα|+30 698-825-9638
Kontovazaina|Κοντοβάζαινα - Ἅγ. Δημήτριος|Κοντοβάζαινα|+30 698-825-9638
Kontovazaina|Κοντοβάζαινα - Ἁγ. Τριάς|Κοντοβάζαινα|+30 698-825-9638
Kontovazaina|Μουριά - Ἅγ. Γεώργιος|Μουριά|+30 699-323-8496
Kontovazaina|Ξηροκαρύταινα - Τίμ. Πρόδρομος|Ξηροκαρύταινα|+30 699-323-8496
Kontovazaina|Πουρναριά - Ἁγ. Τριάς|Πουρναριά|+30 694-481-2344
Tropaia|Ἅγιος Ἰωάννης - Ἅγ. Ἀθανάσιος|Ἅγιος Ἰωάννης|+30 690-627-5212
Tropaia|Ἁγιονέριον - Ἅγ. Γεώργιος|Ἁγιονέριον|+30 694-481-2344
Tropaia|Βυζίκιον - Ἅγ. Νικόλαος|Βυζίκιον|+30 697-280-8311
Tropaia|Δάφνη - Ἅγ. Χαράλαμπος|Δάφνη|+30 697-908-3953
Tropaia|Δόξα - Ἅγ. Νικόλαος|Δόξα|+30 697-328-3467
Tropaia|Καλλιάνιον - Ἅγ. Γεώργιος|Καλλιάνιον|+30 695-588-5433
Tropaia|Καπελίτσα - Γεν. Θεοτόκου|Καπελίτσα|+30 697-834-9567
Tropaia|Καστράκι - Ἅγ. Δημήτριος|Καστράκι|+30 695-588-5433
Tropaia|Λειβαδάκι - Ἅγ. Νικόλαος|Λειβαδάκι|+30 697-834-9567
Tropaia|Λιοδώρα - Ἅγ. Νικόλαος|Λιοδώρα|+30 698-055-3662
Tropaia|Λουτρά Ἡραίας - Τίμ. Πρόδρομος|Λουτρά Ἡραίας|+30 698-055-3662
Tropaia|Λώτι - Ἅγ. Χαράλαμπος|Λώτι|+30 698-055-3662
Tropaia|Μπουλιάρι - Ἁγ. Ἄννα|Μπουλιάρι|+30 697-328-3467
Tropaia|Νεοχώριον - Ἁγ. Τριάς|Νεοχώριον|+30 697-757-1361
Tropaia|Ὄχθια - Ἅγ. Γεώργιος|Ὄχθια|+30 697-280-8311
Tropaia|Περδικονέριον - Ἅγ. Δημήτριος|Περδικονέριον|+30 699-323-8496
Tropaia|Πυρρί - Γεν. Θεοτόκου|Πυρρί|+30 698-169-5660
Tropaia|Ράχες - Ἁγ. Τριάς|Ράχες|+30 698-825-9638
Tropaia|Σπάθαρι - Ἅγ. Δημήτριος|Σπάθαρι|+30 698-169-5660
Tropaia|Σταυροδρόμιον - Κοιμ. Θεοτόκου|Σταυροδρόμιον|+30 698-475-0738
Tropaia|Τουμπίτσιον - Ἅγ. Ἀθανάσιος|Τουμπίτσιον|+30 698-825-9638
Tropaia|Τριποταμιά - Εὐαγγ. Θεοτόκου|Τριποταμιά|+30 697-834-9567
Tropaia|Τρόπαια - Ἅγ. Γεώργιος|Τρόπαια|+30 697-280-8311
Tropaia|Τρόποια - Κοιμ. Θεοτόκου|Τρόποια|+30 697-280-8311
Tropaia|Χρυσοχώριον - Ἅγ. Γεώργιος|Χρυσοχώριον|+30 27970-24528
Tropaia|Χώρα - Ἅγ. Ἀθανάσιος|Χώρα|+30 698-169-5660
Velimachi|Απόσκια Βελημαχίου - Αγ. Τριάς|Απόσκια Βελημαχίου|+30 693-431-2403
Velimachi|Βελημάχιον - Κοιμ. Θεοτόκου|Βελημάχιον|+30 693-431-2403
Velimachi|Βούτσιον - Αγ. Παρασκευή|Βούτσιον|+30 698-475-0738
Velimachi|Βυδιάκι - Ἅγ. Δημήτριος|Βυδιάκι|+30 697-738-8633
Velimachi|Καρδαρίτσιον - Ἅγ. Νικόλαος|Καρδαρίτσιον|+30 693-431-2403
Velimachi|Μοναστηράκιον - Κοίμ. Θεοτόκου|Μοναστηράκιον|+30 698-475-0738
Velimachi|Παραλλογγοί - Τιμ. Ζώνη|Παραλλογγοί|+30 698-247-9210
Megalopolis|Μεγαλόπολις - Ἅγ. Νικόλαος|Μεγαλόπολις|+30 697-474-6465,+30 694-276-8761,+30 694-698-4706
Megalopolis|Μεγαλόπολις - Ἅγ. Κωνσταντίνος|Μεγαλόπολις|+30 697-490-3969,+30 693-325-1842
Megalopolis|Μεγαλόπολις - Κοιμ. Θεοτόκου Ψαθίου|Μεγαλόπολις|+30 697-512-4481
Megalopolis|Ἀνθοχώριον - Εἰσ. Θεοτόκου|Ἀνθοχώριον|+30 698-703-5317
Megalopolis|Βάγκου - Κοιμ. Θεοτόκου|Βάγκου|+30 694-560-6114
Megalopolis|Βάστα - Κοιμ. Θεοτόκου|Βάστα|+30 695-906-4807
Megalopolis|Βρυσούλες - Κοιμ. Θεοτόκου|Βρυσούλες|+30 698-703-0208
Megalopolis|Γέφυρα - Ἅγ. Γεώργιος|Γέφυρα|+30 694-560-6114
Megalopolis|Ἐκκλησούλα - Ἅγ. Νικόλαος|Ἐκκλησούλα|+30 697-792-5612
Megalopolis|Θωκνία - Εὐαγγ. Θεοτόκου|Θωκνία|+30 694-276-8761
Megalopolis|Ίσαρι - Άγ. Νικόλαος|Ίσαρι|+30 695-906-4807
Megalopolis|Καλύβια Καρυών - Άγ. Γεώργιος|Καλύβια Καρυών|+30 697-819-7546
Megalopolis|Καράτουλα - Άγ. Γεώργιος|Καράτουλα|+30 694-560-6114
Megalopolis|Καρυαί Άνω - Γεν. Θεοτόκου|Καρυαί Άνω|+30 694-745-8764
Megalopolis|Κασταναχώριον - Κοιμ. Θεοτόκου|Κασταναχώριον|+30 694-745-8764
Megalopolis|Λύκαιον - Γεν. Θεοτόκου|Λύκαιον|+30 694-745-8764
Megalopolis|Λυκόσουρα - Κοίμ. Θεοτόκου|Λυκόσουρα|+30 697-819-7546
Megalopolis|Μακρύσιον - Ἅγ. Δημήτριος|Μακρύσιον|+30 27910-27003
Megalopolis|Μαλλωτά - Εὐαγγ. Θεοτόκου|Μαλλωτά|+30 698-703-0208
Megalopolis|Μαραθούσα - Ἅγ. Νικόλαος|Μαραθούσα|+30 27910-27003
Megalopolis|Νεοχώριον - Γεν. Θεοτόκου|Νεοχώριον|+30 697-618-9881
Megalopolis|Ὀρέστιον - Ἅγ. Γεώργιος|Ὀρέστιον|+30 693-685-8221
Megalopolis|Παλιομοίρι - Ἅγ. Νικόλαος|Παλιομοίρι|+30 694-560-6114
Megalopolis|Παραδείσια - Άγ. Δημήτριος|Παραδείσια|+30 697-935-3709
Megalopolis|Περιβόλια - Γεν. Θεοτόκου|Περιβόλια|+30 697-935-3709
Megalopolis|Πετροβούνι - Γεν. Θεοτόκου|Πετροβούνι|+30 695-906-4807
Megalopolis|Πλάκα - Γεν. Θεοτόκου|Πλάκα|+30 693-685-8221
Megalopolis|Ραψωμάτι - Κοιμ. Θεοτόκου|Ραψωμάτι|+30 698-703-0208
Megalopolis|Σούλιον - Άγ. Νικόλαος|Σούλιον|+30 697-512-4481
Megalopolis|Σούλου - Ἅγ. Γεώργιος|Σούλου|+30 694-445-9236
Megalopolis|Τρίλοφος - Τίμ. Πρόδρομος|Τρίλοφος|+30 694-445-9236
Megalopolis|Τριπόταμος - Ἅγ. Δημήτριος|Τριπόταμος|+30 697-474-6465
Megalopolis|Χειράδες - Αγ. Παρασκευή|Χειράδες|+30 697-512-4481
Megalopolis|Χράνοι - Κοίμ. Θεοτόκου|Χράνοι|+30 697-618-9881
Megalopolis|Χρούσα - Άγ. Γεώργιος|Χρούσα|+30 695-906-4807
Megalopolis|Χωρέμιον - Ἅγ. Γεώργιος|Χωρέμιον|+30 697-819-7546
Eastern Falaisia|Αναβρυττός - Ἅγ. Δημήτριος|Αναβρυττός|+30 693-325-1842
Eastern Falaisia|Ανεμοδούριον - Ἅγ. Χαράλαμπος|Ανεμοδούριον|+30 698-703-0208
Eastern Falaisia|Βελιγοστή - Μεταμόρφωση Σωτήρος|Βελιγοστή|+30 697-427-6454
Eastern Falaisia|Βουτσαρά - Αγ. Τριάς|Βουτσαρά|+30 697-847-7574
Eastern Falaisia|Γραικού - Κοιμ. Θεοτόκου|Γραικού|+30 693-325-1842
Eastern Falaisia|Ελληνίτσα - Υπαπ. Σωτήρος|Ελληνίτσα|+30 26230-96050
Eastern Falaisia|Καμαρίτσα - Παμμ.Ταξιάρχαι|Καμαρίτσα|+30 695-847-7574
Eastern Falaisia|Κοτσιρίδιον - Ἅγ. Δημήτριος|Κοτσιρίδιον|+30 695-847-7574
Eastern Falaisia|Λεοντάριον - Ἅγ. Απόστολοι|Λεοντάριον|+30 697-847-7574
Eastern Falaisia|Πετρίνα - Κοιμ. Θεοτόκου|Πετρίνα|+30 694-445-9236
Eastern Falaisia|Ποταμιά - Ἅγ. Ιωάννης Θεολόγος|Ποταμιά|+30 697-967-3563
Eastern Falaisia|Ρούτσι - Ἅγ. Σπυρίδων|Ρούτσι|+30 693-325-1842
Eastern Falaisia|Σκορτσινού - Παμμ. Ταξιάρχαι|Σκορτσινού|+30 694-445-9236
Eastern Falaisia|Σουλάριον - Ἅγ. Αθανάσιος|Σουλάριον|+30 697-490-3969
Eastern Falaisia|Σπανέϊκα - Ἅγ. Αθανάσιος|Σπανέϊκα|+30 697-935-3709
Eastern Falaisia|Φαλαισία - Ἅγ. Νικόλαος|Φαλαισία|+30 697-967-3563
Western Falaisia|Άκοβος - Ἅγ. Νικόλαος|Άκοβος|+30 697-928-2114
Western Falaisia|Γιαννέϊκα - Αγ. Τριάς|Γιαννέϊκα|+30 697-928-2114
Western Falaisia|Γιαννέϊκα Άνω - Αγ. Παρασκευή|Γιαννέϊκα Άνω|+30 697-475-9146
Western Falaisia|Γούπατα - Κοιμ. Θεοτόκου|Γούπατα|+30 697-928-2114
Western Falaisia|Δυρράχιον - Εισ. Θεοτόκου|Δυρράχιον|+30 697-475-9146
Western Falaisia|Καμάρα - Ἅγ. Γεώργιος|Καμάρα|+30 697-856-4725
Western Falaisia|Καμποχώριον - Κοιμ. Θεοτόκου|Καμποχώριον|+30 697-856-4725
Western Falaisia|Λεπτίνιον - Ἅγ. Δημήτριος|Λεπτίνιον|+30 697-819-7546
Western Falaisia|Νεοχώριον Φαλαισ. - Γεν. Θεοτόκου|Νεοχώριον Φαλαισ.|+30 697-475-9146
Western Falaisia|Τουρκολέκα - Κοιμ. Θεοτόκου|Τουρκολέκα|+30 697-427-6454
Karytaina|Ἀτσίχωλος - Ἅγ. Ἀθανάσιος|Ἀτσίχωλος|+30 697-438-9081
Karytaina|Βλαχόραφτη - Αγ. Τριάς|Βλαχόραφτη|+30 697-438-9081
Karytaina|Ζώνη - Ἅγ. Δημήτριος|Ζώνη|+30 697-792-5612
Karytaina|Ίσιωμα Καρυών - Ἅγ. Δημήτριος|Ίσιωμα Καρυών|+30 697-819-7546
Karytaina|Καρβουνάρι - Ἅγ. Νικόλαος|Καρβουνάρι|+30 697-229-6924
Karytaina|Καρύταινα - Εὐαγγ. Θεοτόκου|Καρύταινα|+30 694-355-0907
Karytaina|Κατσίμπαλι -Τίμ. Πρόδρομος|Κατσίμπαλι|+30 694-355-0907
Karytaina|Κουρουνιού - Ἅγ. Γεώργιος|Κουρουνιού|+30 694-481-2344
Karytaina|Κρυονέρι - Ἅγ. Θεόδωρος|Κρυονέρι|+30 697-438-9081
Karytaina|Κυπαρίσσια - Ἅγ. Νικόλαος|Κυπαρίσσια|+30 694-276-8761
Karytaina|Κωτίλιον Άνω - Ἅγ. Δημήτριος|Κωτίλιον Άνω|+30 27910-26011
Karytaina|Μαυριά - Άγ. Δημήτριος|Μαυριά|+30 694-445-9236
Karytaina|Παλαιόκαστρον - Εὐαγγ. Θεοτόκου|Παλαιόκαστρον|+30 693-685-8221
Karytaina|Παλαμάριον - Κοιμ. Θεοτόκου|Παλαμάριον|+30 697-229-6924
Karytaina|Παύλια - Ἅγ. Κωνσταντίνος|Παύλια|+30 694-560-6114
Karytaina|Σύρνα - Εὐαγγ. Θεοτόκου|Σύρνα|+30 694-560-6114
Karytaina|Ψάρι - Ζωοδόχος Πηγή|Ψάρι|+30 697-229-6924
"""


# Group | exact current heading | seat | exact public phone | page ID.
MONASTERY_DATA = r"""
men|Ιερά Μονή Γεν. Θεοτόκου Αιμυαλών, Δημητσάνης|Δημητσάνα|+30 27950-31273|9409
men|Ιερά Μονή Κοιμήσεως Θεοτόκου Βελτεσινίκου|Βαλτεσινίκον|+30 27950-82308|9409
men|Ιερά Μονή Κοιμήσεως Θεοτόκου Κολοκοτρώνη Εκκλησούλας|Ἐκκλησούλα|+30 695-847-7574|9409
men|Ιερά Μονή Κοιμήσεως Θεοτόκου Φιλοσόφου, Δημητσάνης|Δημητσάνα|+30 27950-81447|9409
men|Ιερά Μονή Αγίας Παρασκευής, Βάχλιας|Βάχλια|+30 27977-70750|9409
men|Ιερά Μονή Τιμίου Προδρόμου, Στεμνίτσης|Στεμνίτσα|+30 27950-81385|9409
women|ΙΕΡΑ ΜΟΝΗ ΑΚΟΒΑΣ|Ἄκοβα||9461
women|ΙΕΡΑ ΜΟΝΗ ΑΜΠΕΛΑΚΙΟΥ|Πετρίνα|+30 27910-26600|9461
women|ΙΕΡΑ ΜΟΝΗ ΚΑΛΑΜΙΟΥ|Ἀτσίχωλος|+30 27950-81520|9461
women|ΙΕΡΑ ΜΟΝΗ ΚΕΡΝΙΤΣΗΣ|Νυμφασία|+30 27950-22337|9461
women|ΙΕΡΑ ΜΟΝΗ ΚΛΕΙΒΩΚΑΣ|Κοντοβάζαινα|+30 27970-23811|9461
women|ΙΕΡΑ ΜΟΝΗ ΜΑΚΡΥΣΙΟΥ|Μακρύσι|+30 27910-22216|9461
women|ΙΕΡΑ ΜΟΝΗ ΜΠΟΥΡΑ|Μπούρα|+30 27910-26400|9461
"""


METOCHION_DATA = r"""
Ἁγ. Ἀποστόλων Ζυγοβιστίου Ἱ.Μ. Αἰμυαλῶν|Ζυγοβίστιον
Ἁγ. Θεοδώρων Πυργακίου Ἱ.Μ. Κερνίτσης|Πυργάκι
"""

PILGRIMAGE_LOCAL = "Ιερό Προσκύνημα Αγίας Οσιομάρτυρος Θεοδώρας της εν Βάστα Μεγαλοπόλεως"
PILGRIMAGE_SEAT = "Βάστα Μεγαλοπόλεως"

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
CLERGY_TERMS = re.compile(
    r"\b(?:Ἀρχιμανδρίτης|Αρχιμανδρίτης|Ἀρχιμ|Αρχιμ|Πρωτοπρεσβύτερος|"
    r"Πρωτοπρ|Πρεσβύτερος|Διάκονος|Ἡγούμενος|Ηγούμενος|Ἡγουμένη|"
    r"Ηγουμένη|Μοναχός|Μοναχή)\b",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"^\+30 (?:\d{3}-\d{3}-\d{4}|\d{5}-\d{5})$")

TRANSLIT = str.maketrans({
    "Α":"A","Β":"V","Γ":"G","Δ":"D","Ε":"E","Ζ":"Z","Η":"I","Θ":"Th","Ι":"I",
    "Κ":"K","Λ":"L","Μ":"M","Ν":"N","Ξ":"X","Ο":"O","Π":"P","Ρ":"R","Σ":"S",
    "Τ":"T","Υ":"Y","Φ":"F","Χ":"Ch","Ψ":"Ps","Ω":"O",
    "α":"a","β":"v","γ":"g","δ":"d","ε":"e","ζ":"z","η":"i","θ":"th","ι":"i",
    "κ":"k","λ":"l","μ":"m","ν":"n","ξ":"x","ο":"o","π":"p","ρ":"r","σ":"s",
    "ς":"s","τ":"t","υ":"y","φ":"f","χ":"ch","ψ":"ps","ω":"o",
})

RANK_LABELS = {
    "Parish Church": "Parish Church",
    "Pilgrimage Church": "Pilgrimage Church",
    "Monastery": "Monastery",
    "Metochion": "Metochion",
}

ROW_ALLOWED_HOSTS = {
    "imgortmeg.gr", "www.imgortmeg.gr", "ecclesiagreece.gr", "www.ecclesiagreece.gr",
}
LEDGER_ALLOWED_HOSTS = ROW_ALLOWED_HOSTS | {"iaath.gr", "www.iaath.gr"}


def parse_pipe_rows(block, expected):
    rows = []
    for number, line in enumerate(block.strip().splitlines(), 1):
        fields = [value.strip() for value in line.split("|")]
        if len(fields) != expected:
            raise ValueError(
                "raw row %d has %d fields, expected %d" % (number, len(fields), expected)
            )
        rows.append(fields)
    return rows


def romanize(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value.translate(TRANSLIT)).strip()


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", romanize(value).casefold()).strip("-") or "body"


def english_name(local, seat, rank):
    title = romanize(local)
    seat_name = romanize(seat)
    if seat_name.casefold() not in title.casefold():
        title += ", " + seat_name
    return "%s %s" % (title, RANK_LABELS[rank])


def page_source(page_id):
    return BASE + "/?page_id=" + str(page_id)


def post_source(post_id):
    return BASE + "/?p=" + str(post_id)


def make_row(rank, local, seat, phones, sources, contact_sources):
    item = {
        "parent": PARENT,
        "kind": "monastery" if rank in ("Monastery", "Metochion") else "parish",
        "rank": rank,
        "name": english_name(local, seat, rank),
        "local": local,
        "seat": romanize(seat),
        "country": "GR",
        "sources": list(dict.fromkeys(sources)),
    }
    if phones:
        item["phones"] = [value.strip() for value in phones.split(",") if value.strip()]
    if item.get("phones") or item.get("emails") or item.get("site"):
        item["contact_sources"] = list(dict.fromkeys(contact_sources))
        item["contact_checked"] = CHECKED
    return item


def make_rows():
    rows = []
    region_counts = Counter()
    for region, local, seat, phones in parse_pipe_rows(PARISH_DATA, 4):
        if region not in REGIONS:
            raise ValueError("unknown parish region: %s" % region)
        region_counts[region] += 1
        page_url = REGIONS[region][2]
        rows.append(make_row(
            "Parish Church", local, seat, phones,
            [page_url, LEGAL_URL], [page_url],
        ))
    expected_regions = {key: value[1] for key, value in REGIONS.items()}
    if dict(region_counts) != expected_regions:
        raise ValueError("parish regional totals drifted: %r" % dict(region_counts))

    group_counts = Counter()
    for group, local, seat, phone, page_id in parse_pipe_rows(MONASTERY_DATA, 5):
        if group not in ("men", "women") or page_id not in ("9409", "9461"):
            raise ValueError("invalid monastery source row")
        group_counts[group] += 1
        source = page_source(page_id)
        rows.append(make_row(
            "Monastery", local, seat, phone,
            [source, ADMIN_URL], [source] if phone else [],
        ))
    if group_counts != Counter({"women": 7, "men": 6}):
        raise ValueError("monastery grouping drifted: %r" % dict(group_counts))

    metochia = parse_pipe_rows(METOCHION_DATA, 2)
    if len(metochia) != 2:
        raise ValueError("metochion count drifted")
    for local, seat in metochia:
        rows.append(make_row(
            "Metochion", local, seat, "",
            [page_source(9477), ADMIN_URL], [],
        ))

    rows.append(make_row(
        "Pilgrimage Church", PILGRIMAGE_LOCAL, PILGRIMAGE_SEAT, "",
        [post_source(10141), post_source(10178), LEGAL_URL], [],
    ))

    for index, item in enumerate(rows, 1):
        item["id"] = "gr-gortys-%03d-%s" % (
            index, slug(item["local"] + " " + item["seat"]),
        )
    return rows


ROWS = make_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 184
EXPECTED_INTEGRATED_TOTAL = 185
EXPECTED_OWNER_COUNTS = {PARENT: 184}
EXPECTED_KINDS = {"monastery": 15, "parish": 169}
EXPECTED_RANKS = {
    "Metochion": 2,
    "Monastery": 13,
    "Parish Church": 168,
    "Pilgrimage Church": 1,
}
EXPECTED_COVERAGE = (180, 180, 183, 0, 0, 0, 0)
EXISTING_PARENTS = {PARENT}


def validate_url(value, label, allowed_hosts=ROW_ALLOWED_HOSTS):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc.casefold() not in allowed_hosts:
        raise ValueError("%s carries an unaudited source: %s" % (label, value))


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
    has_contact = bool(item.get("phones") or item.get("emails") or item.get("site"))
    if has_contact:
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks exact current contact provenance" % item.get("id"))
    elif contact_sources or item.get("contact_checked"):
        raise ValueError(
            "%s carries contact audit metadata without a phone, email, or site" % item.get("id")
        )
    if len(contact_sources) > 3:
        raise ValueError("%s carries too many contact sources" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
    for phone in item.get("phones") or []:
        if not PHONE_RE.fullmatch(phone):
            raise ValueError("%s carries malformed phone %s" % (item.get("id"), phone))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] in sources:
            raise ValueError("%s mixes its direct site with higher-level sources" % item.get("id"))
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
    text = CANDIDATE_LEDGER.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        raise ValueError("Gortys candidate ledger lacks a final newline")
    if FORBIDDEN_PUNCTUATION.search(text):
        raise ValueError("Gortys candidate ledger carries forbidden punctuation")
    ledger = json.loads(text)
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Gortys candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Gortys candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "module_rows": EXPECTED_TOTAL,
        "existing_external_rows": 1,
        "integrated_total": EXPECTED_INTEGRATED_TOTAL,
        "current_parishes": 168,
        "current_pilgrimages": 1,
        "current_monasteries": 13,
        "current_male_monasteries": 6,
        "current_female_monasteries": 7,
        "current_metochia": 2,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Gortys ledger summary drifted at %s" % key)
    if expected_coverage:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites", "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Gortys ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Gortys ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Gortys ledger item has invalid sources")
            for source_url in sources:
                validate_url(
                    source_url,
                    entry.get("candidate_id") or entry.get("id") or key,
                    LEDGER_ALLOWED_HOSTS,
                )
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Gortys candidate IDs repeat")
    return ledger


def validate_external_chapel():
    text = SHARED_GREECE.read_text(encoding="utf-8")
    if text.count('"parent":"gr-gortys"') != 1:
        raise ValueError("existing Athens-assigned gr-gortys row drifted")
    if "gr-athens-chapel-148-saint-constantine-and-helen-filopappoy" not in text:
        raise ValueError("existing Athens-assigned Gortys chapel is missing")


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
            raise ValueError("duplicate Gortys ID: %s" % row_id)
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
        if CLERGY_TERMS.search(rendered):
            raise ValueError("%s carries a clergy name or title" % row_id)
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
        raise ValueError("Gortys English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Gortys English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Gortys parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Gortys kind totals drifted: %r" % dict(kind_counts))
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Gortys rank totals drifted: %r" % dict(rank_counts))
    coverage = coverage_tuple(result)
    if coverage != EXPECTED_COVERAGE:
        raise ValueError("Gortys contact coverage drifted: %r" % (coverage,))
    validate_external_chapel()
    validate_ledger(coverage)
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_live(url, expect_json=False):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "application/json,text/html,application/pdf;q=0.9,*/*;q=0.8",
        "Connection": "close",
    })
    error = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=60) as response:
                content_type = response.headers.get("Content-Type", "").lower()
                payload = response.read()
            if expect_json:
                if "json" not in content_type:
                    raise ValueError("unexpected JSON content type at %s" % url)
                return json.loads(payload.decode("utf-8"))
            return content_type, payload
        except (HTTPError, URLError, TimeoutError) as exc:
            error = exc
            if attempt < 2:
                time.sleep(1 + attempt)
    raise error


def extract_live_table(rendered):
    rows = []
    pattern = r'<tr[^>]*data-entry="[^"]+"[^>]*>(.*?)(?:</tr>|</tbody>)'
    for match in re.finditer(pattern, rendered, re.IGNORECASE | re.DOTALL):
        cells = re.findall(
            r'<span class="uael-table__text-inner">(.*?)</span>',
            match.group(1), re.IGNORECASE | re.DOTALL,
        )
        if len(cells) < 2:
            continue
        values = []
        for cell in cells:
            value = re.sub(r"<br\s*/?>", " ", cell, flags=re.IGNORECASE)
            value = html.unescape(re.sub(r"<[^>]+>", " ", value))
            values.append(re.sub(r"\s+", " ", value).strip())
        rows.append((values[0], values[1]))
    return rows


def phone_digits(value):
    return re.sub(r"\D", "", value)[-10:]


def check_markers(payload, markers, label):
    text = normalize_source_text(payload)
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("live Gortys marker failed at %s: %s" % (label, marker))


def check_live_sources():
    expected_by_region = {}
    for region, local, _seat, phones in parse_pipe_rows(PARISH_DATA, 4):
        expected_by_region.setdefault(region, {})[normalize_source_text(local)] = [
            phone_digits(value) for value in phones.split(",") if value.strip()
        ]
    for region, (page_id, expected_count, _url) in REGIONS.items():
        page = fetch_live(WP_API + "/pages/" + str(page_id), expect_json=True)
        live_rows = extract_live_table(page["content"]["rendered"])
        if len(live_rows) != expected_count:
            raise ValueError("live %s parish count drifted: %d" % (region, len(live_rows)))
        live = {}
        for title, phone_text in live_rows:
            key = normalize_source_text(title)
            matches = re.findall(
                r"(?<!\d)(?:\d{4}\s*\d{3}\s*\d{3}|\d{5}[-\s]?\d{5})(?!\d)",
                phone_text,
            )
            live[key] = [phone_digits(value) for value in matches]
        if set(live) != set(expected_by_region[region]):
            raise ValueError("live %s parish identities drifted" % region)
        for title, phones in expected_by_region[region].items():
            if live[title] != phones:
                raise ValueError("live %s parish phones drifted at %s" % (region, title))

    for page_id, group, expected_count in ((9409, "men", 6), (9461, "women", 7)):
        page = fetch_live(WP_API + "/pages/" + str(page_id), expect_json=True)
        markers = [
            row[1] for row in parse_pipe_rows(MONASTERY_DATA, 5)
            if row[0] == group and row[4] == str(page_id)
        ]
        if len(markers) != expected_count:
            raise ValueError("monastery marker count drifted")
        check_markers(page["content"]["rendered"], markers, "page %d" % page_id)

    metochia = fetch_live(WP_API + "/pages/9477", expect_json=True)
    check_markers(
        metochia["content"]["rendered"],
        [row[0] for row in parse_pipe_rows(METOCHION_DATA, 2)],
        "page 9477",
    )
    dissolved = fetch_live(WP_API + "/pages/9471", expect_json=True)
    check_markers(dissolved["content"]["rendered"], (
        "ΙΕΡΑ ΜΟΝΗ ΖΩΟΔΟΧΟΥ ΠΗΓΗΣ ΣΤΕΜΝΙΤΣΑΣ",
        "ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΣΤΕΜΝΙΤΣΑΣ",
        "ΙΕΡΑ ΜΟΝΗ ΙΣΙΩΜΑΤΟΣ ΚΑΡΥΩΝ",
        "ΙΕΡΑ ΜΟΝΗ ΑΓ. ΘΕΟΔΩΡΩΝ ΠΥΡΓΑΚΙΟΥ",
        "ΙΕΡΑ ΜΟΝΗ ΤΗΣ ΠΑΝΑΓΙΑΣ ΣΤΟ ΚΡΑΜΠΟΒΟ",
        "ΙΕΡΑ ΜΟΝΗ ΡΕΚΙΤΣΑΣ",
        "ΙΕΡΑ ΜΟΝΗ ΑΓ.ΝΙΚΟΛΑΟΥ ΒΑΛΤΕΣΙΝΙΚΟΥ",
        "ΙΕΡΑ ΜΟΝΗ ΑΓΙΑΣ ΣΟΛΟΜΟΝΗΣ",
        "ΙΕΡΑ ΜΟΝΗ ΑΓ. ΝΙΚΟΛΑΟΥ ΧΟΥΝΤΑΛΟΥ",
        "Ἀσκητήριο Ἁγίου Νίκωνος",
        "Ασκητηριο Αναληψεως Καμενιτσα",
    ), "page 9471")

    for post_id in (10141, 10178):
        post = fetch_live(WP_API + "/posts/" + str(post_id), expect_json=True)
        check_markers(
            post["title"]["rendered"] + " " + post["content"]["rendered"],
            ("Αγίας", "Θεοδώρας", "Βάστα", "Ιερό Προσκύνημα"),
            "post %d" % post_id,
        )

    admin = fetch_live(WP_API + "/pages/2260", expect_json=True)
    check_markers(admin["content"]["rendered"], (
        "Ἐνοριακοί 161", "Παρεκκλήσια 100", "Ἐξωκκλήσια 518",
        "Κοιμητηρίων 146", "Μοναστηριακοί 20",
    ), "administration page")
    content_type, profile = fetch_live(PROFILE_URL)
    if "html" not in content_type:
        raise ValueError("unexpected Church of Greece profile content type")
    check_markers(profile.decode("utf-8", "replace"), ("Γόρτυνος", "Μεγαλοπόλεως"), "profile")
    content_type, legal = fetch_live(LEGAL_URL)
    if "pdf" not in content_type or not legal.startswith(b"%PDF") or len(legal) < 4000000:
        raise ValueError("invalid Church of Greece legal PDF")
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
        print("Gortys live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Gortys check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
