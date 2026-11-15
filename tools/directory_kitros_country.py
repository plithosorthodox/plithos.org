#!/usr/bin/env python3
"""Validate exact named Kitros bodies from first-party sources.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_kitros_country.py --check
    python tools/directory_kitros_country.py --check-live
    python tools/directory_kitros_country.py --dump
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import ssl
import sys
import unicodedata
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "ep-kitros"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "kitros_country.json"
)


def imkitros_path(value):
    return "https://imkitrous.gr/" + quote(value, safe="/")


def monument(value):
    return imkitros_path("monuments/%s/" % value)


REGION_A = imkitros_path(
    "μητρόπολη/αρχιερατικές-περιφέρειες/"
    "α-αρχιερατική-περιφέρεια-κατερίνης/"
)
REGION_B = imkitros_path(
    "μητρόπολη/αρχιερατικές-περιφέρειες/"
    "β-αρχιερατική-περιφέρεια-κατερίνης/"
)
REGION_C = imkitros_path(
    "μητρόπολη/αρχιερατικές-περιφέρειες/"
    "γ-αρχιερατική-περιφέρεια-κατερίνης/"
)
REGION_D = imkitros_path(
    "μητρόπολη/αρχιερατικές-περιφέρειες/"
    "δ-αρχιερατική-περιφέρεια-κατερίνης/"
)
SERVICES_URL = imkitros_path("μητρόπολη/υπηρεσίες/")
MONASTERIES_URL = imkitros_path("μητρόπολη/ιερές-μονές/")
MONUMENTS_URL = imkitros_path("θρησκευτικά-μνημεία/")
EP_URL = "https://ec-patr.org/entities/iera-mitropoli-kitroys/"
ANNA_SITE = "https://www.agiaanna.net/"
ANNA_CONTACT = "https://www.agiaanna.net/Contact.aspx"
DIONYSIUS_SITE = "https://imado.gr/"
EPHRAIM_SITE = "http://imociosefraimsyr.gr/"
EPHRAIM_CONTACT = "http://imociosefraimsyr.gr/contact.html"
EPHRAIM_BODY = "http://imociosefraimsyr.gr/peribalon.html"
SAINT_SOPHIA_POST = imkitros_path(
    "πανηγύρισε-ο-ιερός-ναός-αγίας-σοφίας-τ/"
)

SOURCES = {
    "A": REGION_A,
    "B": REGION_B,
    "C": REGION_C,
    "D": REGION_D,
    "SERVICES": SERVICES_URL,
    "MONASTERIES": MONASTERIES_URL,
    "MONUMENTS": MONUMENTS_URL,
    "EP": EP_URL,
    "ANNA_SITE": ANNA_SITE,
    "ANNA_CONTACT": ANNA_CONTACT,
    "DIONYSIUS_SITE": DIONYSIUS_SITE,
    "EPHRAIM_SITE": EPHRAIM_SITE,
    "EPHRAIM_CONTACT": EPHRAIM_CONTACT,
    "EPHRAIM_BODY": EPHRAIM_BODY,
    "SAINT_SOPHIA": SAINT_SOPHIA_POST,
    "M_KARYES_NICHOLAS": monument("άγιος-νικόλαος-καρυές"),
    "M_PAISIOS": monument("ιερός-ναός-αγίου-παϊσίου"),
    "M_AGIA_KORI": monument("αγία-κόρη-βροντούς"),
    "M_TRINITY_VRONTOU": monument("αγία-τριάδα-βροντούς"),
    "M_KOSMAS": monument("άγιος-κοσμάς-ο-αιτωλός"),
    "M_DEMETRIUS_DION": monument("άγιος-δημήτριος-δίου"),
    "M_ATHANASIUS_AIGINIO": monument("άγιος-αθανάσιος-αιγινίου"),
    "M_PARASKEVI": monument("αγία-παρασκευή"),
    "M_PETRA": monument("μονή-παναγίας-πέτρας"),
    "M_MAKRYRACHI": monument("ιερά-μονή-παναγίας-μακρυράχης"),
    "M_DIONYSIUS": monument(
        "ιερά-μονή-αγίου-διονυσίου-εν-ολύμπω-νέ"
    ),
    "M_EPHRAIM": monument("ιερά-μονή-οσίου-εφραίμ"),
    "M_PROPHET_ELIJAH": monument("μοναστήρι-προφήτη-ηλία"),
    "M_GEORGE_RITINI": monument("ιερά-μονή-αγίου-γεωργίου-ρητίνης"),
    "M_GEORGE_KORINOS": monument("ιερά-μονή-αγίου-γεωργίου-κορινού"),
    "M_ATHANASIUS_KOLINDROS": monument(
        "ιερά-μονή-αγίου-αθανασίου-κολινδρού"
    ),
    "M_JOACHIM_ANNA": monument(
        "μοναστήρι-θεοπατόρων-ιωακείμ-και-άνν"
    ),
}


# region|key|English seat|Greek seat|English dedication|Greek dedication|
# rank|phones|emails|site|source tokens
REGIONAL_SOURCE = r"""
A|katerini-ascension|Katerini|Κατερίνη Πιερίας|Divine Ascension|Θείας Αναλήψεως|Cathedral|23510 23700|||A
A|katerini-anna|Katerini|Κατερίνη Πιερίας|Saint Anna|Αγίας Άννης|Parish Church|23510 26207|info@agiaanna.net|https://www.agiaanna.net/|A,ANNA_SITE,ANNA_CONTACT
A|katerini-paraskevi|Katerini|Κατερίνη Πιερίας|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|23510 20563|||A
A|katerini-holy-trinity|Katerini|Κατερίνη Πιερίας|Holy Trinity|Αγίας Τριάδος|Parish Church|23510 24197|||A
A|katerini-kosmas|Katerini|Κατερίνη Πιερίας|Saint Kosmas the Aetolian|Αγίου Κοσμά του Αιτωλού|Parish Church|23510 30462|||A
A|katerini-sabbas|Katerini|Κατερίνη Πιερίας|Saint Sabbas|Αγίου Σάββα|Parish Church|23510 29401|||A
A|katerini-cross-meeting|Katerini|Κατερίνη Πιερίας|Holy Cross and Meeting of the Lord|Τιμίου Σταυρού και Υπαπαντής του Κυρίου|Parish Church|2351021526|||A
A|katerini-charalambos|Katerini|Κατερίνη Πιερίας|Saint Charalambos|Αγίου Χαραλάμπους|Parish Church|23510 20150|||A
A|katerini-pantanassa-nativity|Katerini|Κατερίνη Πιερίας|Pantanassa and Nativity of the Theotokos|Παντανάσσης Γενέσιον της Θεοτόκου|Parish Church|23510 29868|||A
A|katerini-christopher-euthymius|Katerini|Κατερίνη Πιερίας|Saints Christopher and Euthymius|Αγίου Χριστοφόρου και Ευθυμίου|Parish Church|23510 22461|||A
A|olympiaki-akti-procopius|Olympiaki Akti|Ολυμπιακή Ακτή Πιερίας|Saint Procopius|Αγίου Προκοπίου|Parish Church|23510 61369|||A
A|katerini-cemetery-catherine|Katerini|Κατερίνη Πιερίας|Saint Catherine|Αγίας Αικατερίνης|Cemetery Church|23510 28113|||A
A|katerini-cemetery-lazarus|Katerini|Κατερίνη Πιερίας|Saint Lazarus|Αγίου Λαζάρου|Cemetery Church|23510 28113|||A
A|katerini-hospital-therapon|Katerini|Κατερίνη Πιερίας|Saint Therapon|Αγίου Θεράποντος|Hospital Church|23510 23104|||A
A|svoronos-anthony|Svoronos|Σβορώνος Πιερίας|Saint Anthony|Αγίου Αντωνίου|Parish Church|23510 30214|||A
A|kallithea-nicholas|Kallithea|Καλλιθέα Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|23510 61195|||A
A|paralia-katerinis-photini|Paralia Katerinis|Παραλία Κατερίνης, Πιερία|Saint Photini|Αγίας Φωτεινής|Parish Church|23510 61442|||A
A|peristasi-george|Peristasi|Περίσταση Κατερίνης, Πιερία|Saint George|Αγίου Γεωργίου|Parish Church|23510 21064|||A
A|katerini-meletios|Katerini|Κατερίνη, Πιερία|Saint Meletios|Αγίου Μελετίου|Parish Church|6993233975|||A
A|korinos-panteleimon|Korinos|Κορινός Πιερίας|Saint Panteleimon|Αγίου Παντελεήμωνος|Parish Church|23510 42049,23510 42250|||A
A|korinos-twelve-apostles|Korinos|Κορινός Πιερίας|Twelve Apostles|Δώδεκα Αποστόλων|Parish Church|23510 42049,23510 42250|||A
A|chrani-irene|Chrani|Χράνη Πιερίας|Saint Irene|Αγίας Ειρήνης|Parish Church|23510 91173|||A
A|ano-agios-ioannis-prophet-elijah|Ano Agios Ioannis|Άνω Άγιος Ιωάννης Πιερίας|Prophet Elijah|Προφήτη Ηλία|Parish Church|23510 92393|||A
A|kato-agios-ioannis-forerunner|Kato Agios Ioannis|Κάτω Άγιος Ιωάννης Πιερίας|Saint John the Forerunner|Αγίου Ιωάννου Προδρόμου|Parish Church|23510 91283|||A
A|koukkos-demetrius|Koukkos|Κούκκος Πιερίας|Saint Demetrius|Αγίου Δημητρίου|Parish Church|23510 71733|||A
A|sevasti-nicholas|Sevasti|Σεβαστή Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|6977518015|||A
A|nea-trapezounta-life-giving-spring|Nea Trapezounta|Νέα Τραπεζούντα Πιερίας|Life-Giving Spring|Ζωοδόχου Πηγής|Parish Church|23510 91633|||A
A|palaio-keramidi-archangels|Palaio Keramidi|Παλαιό Κεραμίδιον Πιερίας|Holy Archangels|Παμμεγίστων Ταξιαρχών|Parish Church|2351092685|||A
A|neo-keramidi-unmercenaries|Neo Keramidi|Νέο Κεραμίδιον Πιερίας|Holy Unmercenaries|Αγίων Αναργύρων|Parish Church|23510 31420|||A
A|trilofos-george|Trilofos|Τρίλοφος Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|2351095286|||A
A|ganochora-nicholas|Ganochora|Γανόχωρα Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|2351081260|||A
A|neokaisareia-demetrius|Neokaisareia|Νεοκαισάρεια Πιερίας|Saint Demetrius|Αγίου Δημητρίου|Parish Church|23510 35067|||A
A|aronas-prophet-elijah|Aronas|Αρωνάς Πιερίας|Prophet Elijah|Προφήτη Ηλία|Parish Church|2351036355|||A
B|agios-dimitrios-demetrius|Agios Dimitrios|Άγιος Δημήτριος Πιερίας|Saint Demetrius|Αγίου Δημητρίου|Parish Church|23510 84309|||B
B|petra-george|Petra|Πέτρα Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|23510 82715|||B
B|foteina-nicholas|Foteina|Φωτεινά Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|23510 81770|||B
B|lofos-george|Lofos|Λόφος Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|23510 98302|||B
B|rachi-luke|Rachi|Ράχη Πιερίας|Saint Luke|Αγίου Λουκά|Parish Church|23510 98302|||B
B|kato-milia-demetrius|Kato Milia|Κάτω Μηλιά Πιερίας|Saint Demetrius|Αγίου Δημητρίου|Parish Church|23510 81787|||B
B|mesea-milia-eustathius|Mesea Milia|Μέση Μηλιά Πιερίας|Saint Eustathius|Αγίου Ευσταθίου|Parish Church|23510 81352|||B
B|karyes-barbara|Karyes|Καρυαί Πιερίας|Saint Barbara|Αγίας Βαρβάρας|Parish Church|23510 81527|||B
B|vrya-stephen|Vrya|Βρύα Πιερίας|Saint Stephen|Αγίου Στεφάνου|Parish Church|23510 82010|||B
B|ritini-holy-trinity|Ritini|Ρητίνη Πιερίας|Holy Trinity|Αγίας Τριάδος|Parish Church|23510 82516|||B
B|elatochori-constantine-helen|Elatochori|Ελατοχώρι Πιερίας|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|23510 82118|||B
B|moschochori-dormition|Moschochori|Μοσχοχώριον Πιερίας|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|23510 98258|||B
B|exochi-all-saints|Exochi|Εξοχή Πιερίας|All Saints|Αγίων Πάντων|Parish Church|23510 95475|||B
B|elafos-dormition|Elafos|Έλαφος Πιερίας|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|23510 95111|||B
B|toxo-dormition|Toxo|Τόξο Πιερίας|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|23510 95440|||B
B|katalonia-prophet-elijah|Katalonia|Καταλώνια Πιερίας|Prophet Elijah|Προφήτη Ηλία|Parish Church|23510 95259|||B
B|lagorrachi-anna|Lagorrachi|Λαγορράχη Πιερίας|Saint Anna|Αγίας Άννης|Parish Church|23510 93248|||B
B|moschopotamos-george|Moschopotamos|Μοσχοπόταμος Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|23510 93260|||B
C|litochoro-nicholas|Litochoro|Λιτόχωρο Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|23520 81941|||C
C|litochoro-demetrius|Litochoro|Λιτόχωρο Πιερίας|Saint Demetrius|Αγίου Δημητρίου|Parish Church|23520 81777|||C
C|litochoro-george|Litochoro|Λιτόχωρο Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|6958731729|||C
C|leptokarya-nicholas|Leptokarya|Λεπτοκαρυά Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|23520 31229|||C
C|platamonas-transfiguration|Platamonas|Πλαταμώνας Πιερίας|Transfiguration of the Savior|Μεταμορφώσεως Σωτήρος|Parish Church|23520 41270|||C
C|panteleimon-eleftherios|Panteleimon|Παντελεήμων Πιερίας|Saint Eleftherios|Αγίου Ελευθερίου|Parish Church|23520 44647|||C
C|poroi-marina|Poroi|Πόρροι Πιερίας|Saint Marina|Αγίας Μαρίνης|Parish Church|23520 44647|||C
C|skotina-george|Skotina|Σκοτίνα Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|23520 91265|||C
C|vrontou-nicholas|Vrontou|Βροντού Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|23510 55522|||C
C|karitsa-demetrius|Karitsa|Καρίτσα Πιερίας|Saint Demetrius|Αγίου Δημητρίου|Parish Church|23510 53378|||C
C|agios-spyridon-spyridon|Agios Spyridon|Άγιος Σπυρίδων Πιερίας|Saint Spyridon|Αγίου Σπυρίδωνος|Parish Church|23510 55212|||C
C|dion-paraskevi|Dion|Δίον Πιερίας|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|23510 53639|||C
C|kontariotissa-paraskevi|Kontariotissa|Κονταριώτισσα Πιερίας|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|23510 51712|||C
C|kontariotissa-thomas|Kontariotissa|Κονταριώτισσα Πιερίας|Saint Thomas|Αγίου Θωμά|Parish Church|23510 51734|||C
C|nea-ephesus-three-hierarchs|Nea Ephesus|Νέα Έφεσος Πιερίας|Three Hierarchs|Τριών Ιεραρχών|Parish Church|23510 51275|||C
C|nea-ephesus-john-theologian|Nea Ephesus|Νέα Έφεσος Πιερίας|Saint John the Theologian|Αγίου Ιωάννου Θεολόγου|Parish Church|23510 51239|||C
D|aiginio-andrew|Aiginio|Αιγίνιο Πιερίας|Saint Andrew|Αγίου Ανδρέα|Parish Church|23530 22304|||D
D|aiginio-dormition|Aiginio|Αιγίνιο Πιερίας|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|23530 22427|||D
D|megali-gefyra-george|Megali Gefyra|Μ. Γέφυρα Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|6973165760|||D
D|katachas-menas|Katachas|Καταχάς Πιερίας|Saint Menas|Αγίου Μηνά|Parish Church|23530 22881|||D
D|kolindros-george|Kolindros|Κολινδρός Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|23530 31269|||D
D|kolindros-theodora|Kolindros|Κολινδρός Πιερίας|Saint Theodora|Αγίας Θεοδώρας|Parish Church|23530 31272|||D
D|paliampela-dormition|Paliampela|Παλιάμπελα Πιερίας|Dormition of the Theotokos|Κοιμήσεως Θεοτόκου|Parish Church|23530 31770|||D
D|kastanea-athanasius|Kastanea|Καστανέα Πιερίας|Saint Athanasius|Αγίου Αθανασίου|Parish Church||||D
D|livadi-nicholas|Livadi|Λιβάδι Πιερίας|Saint Nicholas|Αγίου Νικολάου|Parish Church|23530 32304|||D
D|rhyakia-prophet-elijah|Rhyakia|Ρυάκια Πιερίας|Prophet Elijah|Προφήτη Ηλία|Parish Church|23510 95316|||D
D|makrygialos-george|Makrygialos|Μακρύγιαλος Πιερίας|Saint George|Αγίου Γεωργίου|Parish Church|23530 42324|||D
D|methoni-paul|Methoni|Μεθώνη Πιερίας|Apostle Paul|Αποστόλου Παύλου|Parish Church|23530 51098|||D
D|nea-agathoupoli-dormition|Nea Agathoupoli|Αγαθούπολις, Νέα Πιερίας|Dormition of the Theotokos|Κοίμησης Θεοτόκου|Parish Church|23530 51604|||D
D|palaio-eleftherochori-paraskevi|Palaio Eleftherochori|Παλιό Ελευθεροχώρι Πιερίας|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|23530 51870|||D
D|alonia-panteleimon|Alonia|Αλώνια Πιερίας|Saint Panteleimon|Αγίου Παντελεήμωνος|Parish Church|23510 71461|||D
D|mikri-milia-gerasimos|Mikri Milia|Μικρή Μηλιά Πιερίας|Saint Gerasimos|Αγίου Γερασίμου|Parish Church|23510 31260|||D
D|palaiostani-paraskevi|Palaiostani|Παλαιοστάνη Πιερίας|Saint Paraskevi|Αγίας Παρασκευής|Parish Church|23510 83351|||D
D|kitros-constantine-helen|Kitros|Κίτρος Πιερίας|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Parish Church|23510 71111|||D
"""


# key|kind|rank|English name|Greek local name|English seat|address|phones|
# emails|site|source tokens|contact source tokens|live markers
OTHER_SOURCE = r"""
petra-entry-monastery|monastery|Monastery|Patriarchal and Stavropegic Monastery of the Entry of the Theotokos at Petra Olympus|Ιερά Πατριαρχική και Σταυροπηγιακή Μονή Εισοδίων της Θεοτόκου Πέτρας Ολύμπου|Petra Olympus|Πέτρα Ολύμπου|6972.276.754|||EP,M_PETRA,MONASTERIES|EP|Μονή Εισοδίων της Θεοτόκου Πέτρας;6972.276.754
dionysius-olympus-monastery|monastery|Monastery|Patriarchal and Stavropegic Monastery of Saint Dionysius on Olympus|Ιερά Πατριαρχική και Σταυροπηγιακή Μονή Αγίου Διονυσίου εν Ολύμπω|Litochoro|Λιτόχωρο Πιερίας|23520-81220,23520-84220|m@imado.gr,info@imado.gr|https://imado.gr/|EP,MONASTERIES,DIONYSIUS_SITE|EP,MONASTERIES,DIONYSIUS_SITE|Μονή Αγίου Διονυσίου;23520-81220
alexander-pydna-monastery|monastery|Monastery under Foundation|Saint Alexander at Pydna Monastery near Kitros|Ιερά Μονή Αγίου Αλεξάνδρου του εν Πύδνη παρά το Κίτρος|Kitros|Πύδνα, πλησίον Κίτρους|6948.005479|||EP|EP|Μονή Αγίου Αλεξάνδρου;6948.005479
makryrachi-monastery|monastery|Monastery|Patriarchal and Stavropegic Monastery of Panagia Makryrachi|Ιερά Πατριαρχική και Σταυροπηγιακή Μονή Παναγίας Μακρυρράχης|Makryrachi|Μακρυρράχη Πιερίας|23510-83372|||EP,MONASTERIES,M_MAKRYRACHI|EP,MONASTERIES|Μονή Παναγίας Μακρυρράχης;23510-83372
ephraim-syrian-monastery|monastery|Monastery|Coenobitic Monastery of Venerable Ephraim the Syrian|Ιερά Κοινοβιακή Μονή Οσίου Εφραίμ του Σύρου|Kontariotissa|Κονταριώτισσα, Τ.Κ. 60100 Κατερίνης|23510 - 51591|info@imociosefraimsyr.gr|http://imociosefraimsyr.gr/|EP,EPHRAIM_CONTACT,EPHRAIM_BODY|EP,EPHRAIM_CONTACT|Μονή Οσίου Εφραίμ;23510 - 51591
athanasius-kolindros-monastery|monastery|Monastery|Coenobitic Monastery of Saint Athanasius near Kolindros|Ιερά Κοινοβιακή Μονή Αγίου Αθανασίου|Kolindros|Πλησίον Κολινδρού Πιερίας|23530-31122|||EP,MONASTERIES,M_ATHANASIUS_KOLINDROS|EP,MONASTERIES|Μονή Αγίου Αθανασίου;23530-31122
george-korinos-hermitage|monastery|Hermitage|Saint George Hermitage in Korinos|Ησυχαστήριο Αγίου Γεωργίου Κορινού|Korinos|Κορινός Πιερίας|23510-41287|||EP,MONASTERIES,M_GEORGE_KORINOS|EP,MONASTERIES|Ησυχαστήριον Αγίου Γεωργίου;23510-41287
joachim-anna-kolindros-monastery|monastery|Monastery under Foundation|Holy Ancestors Joachim and Anna Monastery near Kolindros|Ιερά Μονή Αγίων Θεοπατόρων Ιωακείμ και Άννης|Kolindros|Δύο χιλιόμετρα προ Κολινδρού Πιερίας|6949234119|||EP,MONASTERIES,M_JOACHIM_ANNA|EP,MONASTERIES|Μονή των Αγίων Θεοπατόρων Ιωακείμ και Άννης;6949234119
george-ritini-monastery|monastery|Monastery|Saint George Monastery in Ritini|Ιερά Μονή Αγίου Γεωργίου Ρητίνης|Ritini|Ρητίνη Πιερίας|694 9221787,6946.057.706|||EP,MONASTERIES,M_GEORGE_RITINI|EP,MONASTERIES|Μονή Αγίου Γεωργίου Ρητίνης
solomone-litochoro-metochion|monastery|Metochion|Saint Solomone Metochion of Saint Dionysius Monastery in Litochoro|Μετόχιο Ιεράς Μονής Αγίου Διονυσίου, Αγίας Σολομονής|Litochoro|Λιτόχωρο Πιερίας||||EP||Μετόχιον Ιεράς Μονής Αγίου Διονυσίου;Αγίας Σολομονής
prophet-elijah-livadi-metochion|monastery|Metochion|Prophet Elijah Metochion of Gregoriou Monastery at Livadi Kolindros|Μετόχιο Ιεράς Μονής Οσίου Γρηγορίου Αγίου Όρους, Προφήτου Ηλιού|Livadi|Λιβάδι Κολινδρού Πιερίας|23530-32309|||MONASTERIES,M_PROPHET_ELIJAH|MONASTERIES|Μετόχιον Ι. Μονής Προφήτου Ηλιού;23530-32309
old-dionysius-holy-trinity|monastery|Historic Monastery Church|Holy Trinity Church at the Old Monastery of Saint Dionysius on Olympus|Ιερός Ναός Αγίας Τριάδος Παλαιάς Ιεράς Μονής Αγίου Διονυσίου εν Ολύμπω|Litochoro|Φαράγγι Ενιπέα, Λιτόχωρο Πιερίας|2352100006|||EP,M_DIONYSIUS|EP|Παλαιά Μονή;αγίας Τριάδος
saint-sophia-institutional-church|parish|Institutional Church|Saint Sophia Church at the Metropolis Ecclesiastical Institutions Complex|Ιερός Ναός Αγίας Σοφίας του Συγκροτήματος Εκκλησιαστικών Ιδρυμάτων|Svoronos|Προσήλιο Κατερίνης, Σβορώνος Πιερίας||||SAINT_SOPHIA||Ιερό Ναό Αγίας Σοφίας;Συγκρότημα Εκκλησιαστικών Ιδρυμάτων
karyes-nicholas-chapel|parish|Chapel|Saint Nicholas Chapel in Karyes|Παρεκκλήσιο Αγίου Νικολάου Καρυών|Karyes|Καρυαί Πιερίας||||M_KARYES_NICHOLAS||μέχρι σήμερα αποτελεί παρεκκλήσιο;αγίας Βαρβάρας
nea-ephesus-paisios-pilgrimage|parish|Pilgrimage Church|Saint Paisios the Athonite Pilgrimage Church in Nea Ephesus|Προσκυνηματικός Ιερός Ναός Αγίου Παϊσίου Νέας Εφέσου|Nea Ephesus|Νέα Έφεσος Πιερίας||||M_PAISIOS||Ιερός Ναός του Αγίου Παϊσίου;προσκυνηματικός ναός
vrontou-agia-kori-shrine|parish|Shrine|Agia Kori Shrine near Vrontou|Προσκύνημα Αγίας Κόρης Βροντούς|Vrontou|Έξι χιλιόμετρα δυτικά Βροντούς Πιερίας||||M_AGIA_KORI||Σήμερα το προσκύνημα της αγίας Κόρης;Βροντού
vrontou-holy-trinity-country-church|parish|Country and Pilgrimage Church|Holy Trinity Country and Pilgrimage Church near Vrontou|Εξωκλήσι και Προσκύνημα Αγίας Τριάδος Βροντούς|Vrontou|Τέσσερα χιλιόμετρα από Βροντού Πιερίας||||M_TRINITY_VRONTOU||Σήμερα αποτελεί εξωκλήσι;προσκυνηματικό τόπο
ano-milia-kosmas-pilgrimage|parish|Pilgrimage Church|Saint Kosmas the Aetolian Pilgrimage Church in Ano Milia|Προσκύνημα Αγίου Κοσμά του Αιτωλού Άνω Μηλιάς|Ano Milia|Άνω Μηλιά Πιερίας||||M_KOSMAS||Το προσκύνημα του αγίου Κοσμά;κτίστηκε ναός
dion-demetrius-country-church|parish|Country Church|Saint Demetrius Country Church in Dion|Εξωκλήσι Αγίου Δημητρίου Δίου|Dion|Δίον Πιερίας||||M_DEMETRIUS_DION||αποτελεί εξωκλήσι της σημερινής ενορίας;Δίον
aiginio-athanasius-worship-church|parish|Historic Worship Church|Saint Athanasius Historic Worship Church in Aiginio|Ιερός Ναός Αγίου Αθανασίου Αιγινίου|Aiginio|Αιγίνιο Πιερίας||||M_ATHANASIUS_AIGINIO||παραχώρησε στη δημόσια λατρεία;Αιγινίου
ano-milia-paraskevi-church|parish|Church|Saint Paraskevi Church in Ano Milia|Ιερός Ναός Αγίας Παρασκευής Άνω Μηλιάς|Ano Milia|Άνω Μηλιά Πιερίας||||M_PARASKEVI||Ιερός Ναός της αγίας Παρασκευής;επαναλειτούργησε
makryrachi-dormition-katholikon|monastery|Monastery Church|Dormition of the Theotokos Katholikon at Panagia Makryrachi Monastery|Καθολικό Κοιμήσεως της Θεοτόκου Ιεράς Μονής Παναγίας Μακρυρράχης|Makryrachi|Ιερά Μονή Παναγίας Μακρυρράχης, Μακρυρράχη Πιερίας||||M_MAKRYRACHI||σημερινό καθολικό;Κοίμηση της Θεοτόκου
petra-entry-katholikon|monastery|Monastery Church|Entry of the Theotokos Church at Petra Olympus Monastery|Ιερός Ναός Εισοδίων της Θεοτόκου Ιεράς Μονής Πέτρας Ολύμπου|Petra Olympus|Ιερά Μονή Πέτρας Ολύμπου||||EP,M_PETRA||Μονή Εισοδίων της Θεοτόκου Πέτρας;σημερινός ναός
ephraim-panagia-monastery-church|monastery|Monastery Church|Panagia Monastery Church near Venerable Ephraim Monastery|Μοναστηριακός Ναός Παναγίας|Kontariotissa|Πλησίον Ιεράς Μονής Οσίου Εφραίμ, Κονταριώτισσα||||EPHRAIM_BODY||Παναγία;Μοναστηριακός Ναός
ephraim-life-giving-spring-katholikon|monastery|Monastery Church|Life-Giving Spring and Venerable Ephraim Katholikon|Καθολικό Ζωοδόχου Πηγής και Οσίου Εφραίμ του Σύρου|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||M_EPHRAIM,EPHRAIM_BODY||Καθολικόν;Ζωοδόχου Πηγής;Εφραίμ του Σύρου
ephraim-underground-church|monastery|Monastery Church|Forerunner and New Martyrs Raphael, Nicholas and Irene Underground Church|Υπόγειος Ναός Τιμίου Προδρόμου και Αγίων Ραφαήλ, Νικολάου και Ειρήνης|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||M_EPHRAIM,EPHRAIM_BODY||υπόγειος ναός;Τιμίου Προδρόμου;Ραφαήλ
ephraim-catherine-chapel|monastery|Monastery Chapel|Saint Catherine Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίας Αικατερίνης|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλησίων;Αικατερίνης της Πανσόφου
ephraim-porphyrios-chapel|monastery|Monastery Chapel|Venerable Porphyrios Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίου Πορφυρίου του Καυσοκαλυβίτου|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλησίων;Πορφυρίου του Καυσοκαλυβίτου
ephraim-nativity-theotokos-chapel|monastery|Monastery Chapel|Nativity of the Theotokos Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Γενεθλίου της Υπεραγίας Θεοτόκου|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλήσια του Γενεθλίου;Υπεραγίας Θεοτόκου
ephraim-irene-chrysovalantou-chapel|monastery|Monastery Chapel|Venerable Irene Chrysovalantou Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίας Ειρήνης Χρυσοβαλάντου|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλήσιον;Ειρήνης Χρυσοβαλάντου
ephraim-holy-apostles-chapel|monastery|Monastery Chapel|Holy Apostles Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίων Αποστόλων|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλήσιον Αγίων Αποστόλων
ephraim-dionysius-areopagite-chapel|monastery|Monastery Chapel|Saint Dionysius the Areopagite Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίου Διονυσίου του Αρεοπαγίτου|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλήσιον του Αγίου Διονυσίου του;Αρεοπαγίτου
ephraim-thekla-chapel|monastery|Monastery Chapel|Saint Thekla Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίας Πρωτομάρτυρος και Ισαποστόλου Θέκλης|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλήσιον της Αγίας;Θέκλης
ephraim-portaitissa-chapel|monastery|Monastery Chapel|Panagia Portaitissa Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Παναγίας Πορταΐτισσας|Kontariotissa|Είσοδος Ιεράς Μονής Οσίου Εφραίμ, Κονταριώτισσα||||EPHRAIM_BODY||Παναγίαν Πορταϊτισσαν;Παρεκκλήσιον
ephraim-paraskevi-chapel|monastery|Monastery Chapel|Saint Paraskevi Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίας Παρασκευής|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Αγ. Παρθενομάρτυρος Παρασκευής;Παρεκκλήσια
ephraim-david-euboea-chapel|monastery|Monastery Chapel|Venerable David of Euboea Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίου Δαυΐδ του εν Ευβοία|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Παρεκκλήσιον;Οσίου Δαβίδ του εν Ευβοία
ephraim-sisoe-chapel|monastery|Monastery Chapel|Venerable Sisoe Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίου Σισώη|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Οσίου Σισώη;Παρεκκλήσια
ephraim-archangels-cemetery-church|monastery|Monastery Cemetery Church|Holy Archangels Cemetery Church at Venerable Ephraim Monastery|Κοιμητηριακός Ναός Αγίων Αρχαγγέλων|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Αγίων Αρχαγγέλων;Κοιμητηριακός Ναός
ephraim-prophet-elijah-kathisma|monastery|Monastic Kathisma|Prophet Elijah Kathisma at Venerable Ephraim Monastery|Κάθισμα Προφήτου Ηλιού|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Κάθισμα εις τιμήν του Προφήτου Ηλιού
ephraim-menas-chapel|monastery|Monastery Chapel|Saint Menas Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίου Μηνά|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Άγιος Μεγαλομάρτυς;Μηνάς;Παρεκκλήσια
ephraim-john-merciful-chapel|monastery|Monastery Chapel|Saint John the Merciful Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίου Ιωάννου του Ελεήμονος|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Ιωάννης;Ελεήμων;Παρεκκλήσια
ephraim-seraphim-sarov-chapel|monastery|Monastery Chapel|Venerable Seraphim of Sarov Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίου Σεραφείμ του Σαρώφ|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Σεραφείμ;του Σαρώφ;Παρεκκλήσια
ephraim-john-kalyvites-chapel|monastery|Monastery Chapel|Venerable John Kalyvites Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίου Ιωάννου του Καλυβίτου|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Ιωάννης;ο Καλυβίτης;Παρεκκλήσια
ephraim-hypomone-chapel|monastery|Monastery Chapel|Venerable Hypomone Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Οσίας Υπομονής|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Αγ. Υπομονή;Παρεκκλήσια
ephraim-luke-crimea-chapel|monastery|Monastery Chapel|Saint Luke of Crimea Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίου Λουκά Κριμαίας|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Αγ. Λουκάς;Κριμαίας;Παρεκκλήσια
ephraim-barbara-chapel|monastery|Monastery Chapel|Saint Barbara Chapel at Venerable Ephraim Monastery|Παρεκκλήσιο Αγίας Βαρβάρας|Kontariotissa|Ιερά Μονή Οσίου Εφραίμ του Σύρου, Κονταριώτισσα||||EPHRAIM_BODY||Μεγαλομάρτυς;Βαρβάρα;Παρεκκλήσια
joachim-anna-anna-church|monastery|Monastery Church|Saint Anna Church at the Holy Ancestors Monastery|Ιερός Ναός Αγίας Άννας Ιεράς Μονής Αγίων Θεοπατόρων|Kolindros|Ιερά Μονή Αγίων Θεοπατόρων, Κολινδρός||||M_JOACHIM_ANNA||Ναός της αγίας Άννας;σημερινό μοναστηριακό συγκρότημα
joachim-anna-irene-church|monastery|Monastery Church|Saint Irene Chrysovalantou Church at the Holy Ancestors Monastery|Ιερός Ναός Αγίας Ειρήνης Χρυσοβαλάντου Ιεράς Μονής Αγίων Θεοπατόρων|Kolindros|Ιερά Μονή Αγίων Θεοπατόρων, Κολινδρός||||M_JOACHIM_ANNA||δεύτερο ναό;αγίας Ειρήνης της Χρυσοβαλάντου
george-korinos-katholikon|monastery|Monastery Church|Saint George Katholikon at the Korinos Hermitage|Καθολικό Αγίου Γεωργίου Ησυχαστηρίου Κορινού|Korinos|Ησυχαστήριο Αγίου Γεωργίου, Κορινός||||M_GEORGE_KORINOS||Καθολικό της;αγίου Γεωργίου Κορινού
george-korinos-nektarios-chapel|monastery|Monastery Chapel|Saint Nektarios Chapel at the Korinos Hermitage|Παρεκκλήσιο Αγίου Νεκταρίου Ησυχαστηρίου Κορινού|Korinos|Ησυχαστήριο Αγίου Γεωργίου, Κορινός||||M_GEORGE_KORINOS||δύο παρεκκλήσια;Αγίου Νεκταρίου
george-korinos-phanourios-chapel|monastery|Monastery Chapel|Saint Phanourios Chapel at the Korinos Hermitage|Παρεκκλήσιο Αγίου Φανουρίου Ησυχαστηρίου Κορινού|Korinos|Ησυχαστήριο Αγίου Γεωργίου, Κορινός||||M_GEORGE_KORINOS||δύο παρεκκλήσια;Αγίου Φανουρίου
prophet-elijah-metochion-church|monastery|Monastery Church|Prophet Elijah Church at the Livadi Metochion|Ιερός Ναός Προφήτου Ηλιού Μετοχίου Ιεράς Μονής Οσίου Γρηγορίου|Livadi|Μετόχιο Ιεράς Μονής Οσίου Γρηγορίου, Λιβάδι Κολινδρού||||M_PROPHET_ELIJAH||μοναστήρι του προφήτη Ηλία;Ο ναός
george-ritini-katholikon|monastery|Monastery Church|Saint George Katholikon at Ritini Monastery|Καθολικό Αγίου Γεωργίου Ιεράς Μονής Ρητίνης|Ritini|Ιερά Μονή Αγίου Γεωργίου, Ρητίνη||||M_GEORGE_RITINI||καθολικό της Μονής;αγίου Γεωργίου
athanasius-kolindros-katholikon|monastery|Monastery Church|Saint Athanasius Katholikon at Kolindros Monastery|Καθολικό Αγίου Αθανασίου Ιεράς Μονής Κολινδρού|Kolindros|Ιερά Μονή Αγίου Αθανασίου, Κολινδρός||||M_ATHANASIUS_KOLINDROS||παρέμεινε μόνο το Καθολικό;νέας Μονής
"""


def split_values(value, separator=","):
    return [part.strip() for part in value.split(separator) if part.strip()]


def source_values(tokens):
    values = []
    for token in split_values(tokens):
        if token not in SOURCES:
            raise ValueError("unknown Kitros source token: %s" % token)
        values.append(SOURCES[token])
    return values


def parse_regional_rows():
    rows = []
    markers = {}
    for number, raw in enumerate(
            (line for line in REGIONAL_SOURCE.splitlines() if line.strip()), 1):
        parts = raw.split("|")
        if len(parts) != 11:
            raise ValueError("invalid Kitros regional source row: %s" % raw)
        (region, key, seat, seat_local, dedication, dedication_local, rank,
         phones_text, emails_text, site, source_tokens) = parts
        row_id = "gr-ep-kitros-%03d-%s" % (number, key)
        if rank == "Cathedral":
            name = "%s Cathedral in %s" % (dedication, seat)
            local = "Ιερός Καθεδρικός Ναός %s" % dedication_local
        elif rank == "Cemetery Church":
            name = "%s Cemetery Church in %s" % (dedication, seat)
            ordinal = "Α'" if "catherine" in key else "Β'"
            local = "Ιερός Ναός %s (%s Κοιμητήριο)" % (
                dedication_local, ordinal
            )
        elif rank == "Hospital Church":
            name = "%s Hospital Church in %s" % (dedication, seat)
            local = (
                "Ιερός Ναός %s (παλαιό Νοσοκομείο Κατερίνης)"
                % dedication_local
            )
        else:
            name = "%s Parish Church in %s" % (dedication, seat)
            local = "Ιερός Ναός %s, %s" % (
                dedication_local, seat_local
            )
        sources = source_values(source_tokens)
        item = {
            "id": row_id,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "sources": sources,
        }
        phones = split_values(phones_text)
        emails = split_values(emails_text)
        if phones:
            item["phones"] = phones
        if emails:
            item["emails"] = emails
        if site:
            item["site"] = site
        if phones or emails or site:
            item["contact_sources"] = sources
            item["contact_checked"] = CHECKED
        rows.append(item)
        marker_dedication = dedication_local
        for prefix in ("Αγίου ", "Αγίας "):
            if marker_dedication.startswith(prefix):
                marker_dedication = marker_dedication[len(prefix):]
                break
        markers[row_id] = [seat_local, marker_dedication]
        if region not in {"A", "B", "C", "D"}:
            raise ValueError("invalid Kitros region: %s" % region)
    return rows, markers


def parse_other_rows(start_number):
    rows = []
    markers = {}
    for offset, raw in enumerate(
            (line for line in OTHER_SOURCE.splitlines() if line.strip())):
        parts = raw.split("|")
        if len(parts) != 13:
            raise ValueError("invalid Kitros other source row: %s" % raw)
        (key, kind, rank, name, local, seat, address, phones_text,
         emails_text, site, source_tokens, contact_tokens,
         marker_text) = parts
        row_id = "gr-ep-kitros-%03d-%s" % (start_number + offset, key)
        item = {
            "id": row_id,
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address],
            "sources": source_values(source_tokens),
        }
        phones = split_values(phones_text)
        emails = split_values(emails_text)
        if phones:
            item["phones"] = phones
        if emails:
            item["emails"] = emails
        if site:
            item["site"] = site
        contact_sources = source_values(contact_tokens)
        if contact_sources:
            item["contact_sources"] = contact_sources
            item["contact_checked"] = CHECKED
        rows.append(item)
        markers[row_id] = split_values(marker_text, ";")
    return rows, markers


REGIONAL_ROWS, REGIONAL_MARKERS = parse_regional_rows()
OTHER_ROWS, OTHER_MARKERS = parse_other_rows(len(REGIONAL_ROWS) + 1)
ROWS = REGIONAL_ROWS + OTHER_ROWS
LIVE_MARKERS = dict(REGIONAL_MARKERS)
LIVE_MARKERS.update(OTHER_MARKERS)

ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 139
EXPECTED_OWNER_COUNTS = {PARENT: 139}
EXPECTED_KINDS = {"monastery": 45, "parish": 94}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Church": 2,
    "Chapel": 1,
    "Church": 1,
    "Country and Pilgrimage Church": 1,
    "Country Church": 1,
    "Hermitage": 1,
    "Historic Monastery Church": 1,
    "Historic Worship Church": 1,
    "Hospital Church": 1,
    "Institutional Church": 1,
    "Metochion": 2,
    "Monastery": 6,
    "Monastery Cemetery Church": 1,
    "Monastery Chapel": 20,
    "Monastery Church": 11,
    "Monastery under Foundation": 2,
    "Monastic Kathisma": 1,
    "Parish Church": 81,
    "Pilgrimage Church": 2,
    "Shrine": 1,
}
EXPECTED_CONTACT_BODIES = 95
EXPECTED_PHONE_BODIES = 95
EXPECTED_PHONE_VALUES = 99
EXPECTED_EMAIL_BODIES = 3
EXPECTED_EMAIL_VALUES = 4
EXPECTED_SITE_BODIES = 3
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
    allowed_hosts = {
        "imkitrous.gr", "ec-patr.org", "www.agiaanna.net",
        "imado.gr", "imociosefraimsyr.gr",
    }
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in allowed_hosts:
        raise ValueError("%s carries a non-competent source: %s"
                         % (label, value))
    if parsed.scheme == "http" and parsed.netloc != "imociosefraimsyr.gr":
        raise ValueError("%s has an avoidable insecure URL: %s"
                         % (label, value))


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
    has_contact = bool(
        item.get("phones") or item.get("emails") or item.get("site")
    )
    if has_contact and not contact_sources:
        raise ValueError("%s lacks contact provenance" % item.get("id"))
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
        site_host = urlparse(item["site"]).netloc
        if not any(urlparse(value).netloc == site_host for value in sources):
            raise ValueError("%s body-owned site lacks provenance"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Kitros candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kitros candidate ledger date drifted")
    expected_summary = {
        PARENT: 139,
        "total": 139,
        "displayed_regional_church_rows": 85,
        "regional_parish_church_rows": 81,
        "parish_kind_rows": 94,
        "monastery_kind_rows": 45,
        "contact_bodies": 95,
        "phone_bodies": 95,
        "public_phone_values": 99,
        "email_bodies": 3,
        "public_email_values": 4,
        "body_owned_sites": 3,
        "address_bodies": 139,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Kitros ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Kitros ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kitros ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Kitros ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Kitros ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Kitros candidate ledger has forbidden punctuation")
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
        raise ValueError("Kitros English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Kitros English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Kitros parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Kitros kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Kitros rank totals drifted: %r"
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
        raise ValueError("Kitros contact coverage drifted: %r" % (coverage,))
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
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def normalize_source_blob(value):
    value = html.unescape(value).replace("\u00a0", " ")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def all_source_urls():
    values = set()
    for row in ROWS:
        values.update(row.get("sources") or [])
        values.update(row.get("contact_sources") or [])
        if row.get("site"):
            values.add(row["site"])
    ledger = validate_ledger()
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        for entry in ledger[key]:
            values.update(entry.get("sources") or [])
    return sorted(values)


def check_live_sources():
    failures = []
    source_texts = {}
    source_blobs = {}
    for url in all_source_urls():
        try:
            request = Request(url, headers={
                "User-Agent": "Mozilla/5.0 Plithos directory source audit",
                "Connection": "close",
            })
            context = ssl._create_unverified_context() if (
                urlparse(url).netloc == "imociosefraimsyr.gr"
            ) else None
            with urlopen(request, timeout=45, context=context) as response:
                if response.status >= 400:
                    failures.append((url, "HTTP %s" % response.status))
                    continue
                content_type = response.headers.get("Content-Type", "").lower()
                if "html" not in content_type:
                    failures.append((url, "unexpected content type %s"
                                     % content_type))
                    continue
                raw = response.read().decode("utf-8", "replace")
                source_texts[url] = normalize_source_text(raw)
                source_blobs[url] = normalize_source_blob(raw)
        except Exception as exc:
            failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join("%s [%s]" % pair for pair in failures)
        raise ValueError("live Kitros source check failed: %s" % rendered)
    marker_failures = []
    for row in ROWS:
        missing = []
        for marker in LIVE_MARKERS[row["id"]]:
            normalized = normalize_source_text(marker)
            if not any(normalized in source_texts.get(url, "")
                       for url in row["sources"]):
                missing.append(marker)
        if missing:
            marker_failures.append((row["id"], missing))
    if marker_failures:
        raise ValueError(
            "live Kitros exact-source marker check failed: %r"
            % marker_failures
        )
    contact_failures = []
    for row in ROWS:
        for field in ("phones", "emails"):
            for value in row.get(field) or []:
                normalized = normalize_source_blob(value)
                if not any(
                    normalized in source_blobs.get(url, "")
                    for url in row.get("contact_sources") or []
                ):
                    contact_failures.append((row["id"], field, value))
    if contact_failures:
        raise ValueError(
            "live Kitros contact marker check failed: %r"
            % contact_failures
        )


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
            "Kitros: %d exact named bodies; %d carry current public "
            "body-associated contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Kitros: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
