#!/usr/bin/env python3
"""Current official worship-body roster for the Metropolis of Thessaloniki.

This module is intentionally standalone. It publishes only bodies named by
the current official metropolis roster and records unresolved aggregate gaps
in the adjacent candidate ledger.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse


CHECKED = "2026-11-15"
PARENT = "ep-thessaloniki"
PARISH_ROSTER = "https://imth.gr/about/"
CHAPEL_ROSTER = (
    "https://imth.gr/παρεκκλήσια-ιεράς-μητροπόλεως/")
EP_AGGREGATE = (
    "https://ec-patr.org/entities/iera-mitropoli-thessalonikis/")
CANDIDATE_LEDGER = (
    Path(__file__).with_name("directory_candidates") /
    "thessaloniki_country.json")


def profile(path):
    return "https://imth.gr/%s/" % path


# id suffix, English name, source name, rank, address, phones, emails,
# body-owned site, official profile path
PRIMARY_CHURCHES = [
    ("001", "Metropolitan Church of Saint Gregory Palamas",
     "Μητροπολιτικός Ιερός Ναός αγίου Γρηγορίου του Παλαμά",
     "Metropolitan Church", "οδ. Αγίας Σοφίας 6\n546 22 Θεσσαλονίκη",
     ["2310-271.520"], ["agiosgregoriospalamas@gmail.com"],
     "https://neoiagp.gr/",
     "μητροπολιτικός-ιερός-ναός-αγίου-γρηγ"),
    ("002", "Pilgrimage Church of Saint Demetrius, Patron of Thessaloniki",
     "Προσκυνηματικός Iερός Ναός αγίου Δημητρίου του Πολιούχου",
     "Pilgrimage Church", "οδ. Αγ. Δημητρίου 83\n546 33 Θεσσαλονίκη",
     ["2310-270.008"],
     ["inadthes@yahoo.gr", "agdimitriosthes@gmail.com"],
     "https://www.agdimitriosthes.gr/",
     "προσκυνηματικός-ἱερός-ναός-ἁγίου-δη"),
    ("003", "Cathedral Church of the Wisdom of God",
     "Καθεδρικός Ιερός Ναός της του Θεού Σοφίας", "Cathedral",
     "Πλ. Αγ. Σοφίας\n546 22 Θεσσαλονίκη",
     ["2310-274.413", "2310-270.253"],
     ["agiasofiathess@gmail.com"], None,
     "καθεδρικός-ἱερός-ναός-τῆς-τοῦ-θεοῦ-σ"),
    ("004", "Pilgrimage Church of Saints Cyril and Methodius",
     "Προσκυνηματικός Ιερός Ναός αγίων Κυρίλλου και Μεθοδίου",
     "Pilgrimage Church", "οδ. Στρατ. Καλλιδοπούλου 2\n546 42 Θεσσαλονίκη",
     ["2310-827.444"], ["cyrmethnaos@gmail.com"], None,
     "προσκυνηματικός-ἱερός-ναός-ἁγίων-κυ"),
    ("005", "Pilgrimage Church of Saint George, the Rotunda",
     "Προσκυνηματικός Iερός Ναός αγίου Γεωργίου (Ροτόντα)",
     "Pilgrimage Church", "Πλ. Αγ. Γεωργίου\n546 35 Θεσσαλονίκη",
     [], [], None, "προσκυνηματικός-ἱερός-ναός-ἁγίου-γε"),
    ("006", "Byzantine Church of Saint Catherine",
     "Βυζαντινός Ιερός Ναός αγίας Αικατερίνης", "Byzantine Church",
     "οδ. Ηούς και Σαχτούρη\n546 32 Θεσσαλονίκη",
     ["2310-225.580"], ["vizadini.ag.aikaterini@gmail.com"], None,
     "βυζαντινός-ἱερός-ναός-ἁγίας-αἰκατερ"),
    ("007", "Parish Church of Saint Anastasia in Kifisia",
     "Ενοριακός Ιερός Ναός αγίας Αναστασίας Κηφισιάς", "Parish Church",
     "οδ. Κηφισίας - Μ. Αλεξάνδρου\n542 48 Θεσσαλονίκη",
     ["2310-447.444"], ["inaganastasias@gmail.com"],
     "https://www.farmakolytria.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίας-ἀναστασ"),
    ("008", "Parish Church of Saint Barbara in Ano Toumba",
     "Ενοριακός Ιερός Ναός αγίας Βαρβάρας Άνω Τούμπας", "Parish Church",
     "οδ. Γρηγ. Λαμπράκη 106\n543 51 Θεσσαλονίκη",
     ["2310-911.212"], ["agvar1@yahoo.gr", "inagvarthess@gmail.com"],
     "https://www.inagvarvaras.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίας-βαρβάρα"),
    ("009", "Parish Church of Saint Kyriaki in Charilaou",
     "Ενοριακός Ιερός Ναός αγίας Κυριακής Χαριλάου", "Parish Church",
     "οδ. Αμφοτερού\n542 50 Θεσσαλονίκη",
     ["2310-303.216"], ["agiaskyriakis@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίας-κυριακής"),
    ("010", "Parish Church of Saint Marina in Ano Toumba",
     "Ενοριακός Ιερός Ναός αγίας Μαρίνης Άνω Τούμπας", "Parish Church",
     "Πλ. Αγ. Μαρίνης\n543 51 Θεσσαλονίκη",
     ["2310-913.530"], ["inagmarinisthess@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίας-μαρίνης"),
    ("011", "Parish Church of the Holy Trinity",
     "Ενοριακός Ιερός Ναός αγίας Τριάδος", "Parish Church",
     "οδ. Αγ. Τριάδος 22\n546 40 Θεσσαλονίκη",
     ["2310-831.831"], ["inagiastriados22@gmail.com"],
     "https://inagiastriados.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίας-τριάδος"),
    ("012", "Parish Church of the Holy Unmercenaries in the Acropolis",
     "Ενοριακός Ιερός Ναός αγίων Αναργύρων (Ακροπόλεως)",
     "Parish Church", "Πλ. Αγ. Αναργύρων\n546 34 Θεσσαλονίκη",
     ["2310-209.159"], ["i.n.ag.anargyrwn@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίων-ἀναργύρ"),
    ("013", "Byzantine Parish Church of the Twelve Apostles",
     "Βυζαντινός Ενοριακός Ιερός Ναός αγίων Δώδεκα Αποστόλων",
     "Parish Church", "Πλ. Αγ. Αποστόλων\n546 30 Θεσσαλονίκη",
     ["2310-537.915"],
     ["ierosnaosagiondodekaapostolon@yahoo.com", "inagiwnapostolwn@gmail.com"],
     None, "βυζαντινός-ἐνοριακός-ἱερός-ναός-ἁγί"),
    ("014", "Parish Church of Saints Constantine and Helen",
     "Ενοριακός Ιερός Ναός αγίων Κωνσταντίνου & Ελένης",
     "Parish Church", "Πλ. Ιπποδρομίου\n546 21 Θεσσαλονίκη",
     ["2310-262.329"], ["naosagiouKonstantinou@outlook.com.gr"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίων-κων-νου"),
    ("015", "Parish Church of Saint Athanasius",
     "Ενοριακός Ιερός Ναός αγίου Αθανασίου", "Parish Church",
     "Εγνατία 87\n546 35 Θεσσαλονίκη",
     ["2310-229.473"], ["agiouathanasiou@yahoo.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίου-ἀθανασί"),
    ("016", "Parish Church of Saint Basil in Nea Elvetia",
     "Ενοριακός Ιερός Ναός αγίου Βασιλείου Ν. Ελβετίας",
     "Parish Church", "οδ. Καθ. Ευρυγένη 19\n542 49 Θεσσαλονίκη",
     [], ["i.n.agiouvasiliou.neaselvetias@gmail.com"],
     "https://enavasi.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίου-βασιλείο"),
    ("017", "Parish Church of Saint George in Panorama",
     "Ενοριακός Ιερός Ναός αγίου Γεωργίου (Πανοράματος)",
     "Parish Church", "Πλ. Αγ. Γεωργίου\n552 36 Πανόραμα",
     ["2310-341.059"], ["ag.georgiospanoramatos@yahoo.com"],
     "https://agiosgeorgiospanoramatos.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίου-γεωργίου"),
    ("018", "Parish Church of Saint Eleftherios in Depot",
     "Ενοριακός Ιερός Ναός αγίου Ελευθερίου (Ντεπώ)", "Parish Church",
     "Πλ. Αγ. Ελευθερίου\n546 55 Θεσσαλονίκη",
     ["2310-411.540"], ["agioseleftherios@yahoo.gr"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίου-ἐλευθερ"),
    ("019", "Parish Church of Saint Therapon in Kato Toumba",
     "Ενοριακός Ιερός Ναός αγίου Θεράποντος (Κάτω Τούμπας)",
     "Parish Church", "οδ. Αρτάκης 1\n544 54 Θεσσαλονίκη",
     ["2310-912.151"], ["therapon1950@yahoo.gr"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίου-θεράποντ"),
    ("020", "Parish Church of Saint John Chrysostom",
     "Ενοριακός Ιερός Ναός αγίου Ιωάννου του Χρυσοστόμου",
     "Parish Church", "οδ. Περδίκα 55\n546 39 Θεσσαλονίκη",
     ["2310-832.080"], ["inaixthes@gmail.com"],
     "https://inaixthes.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίου-ἰωάννο"),
    ("021", "Parish Church of Saint Menas",
     "Ενοριακός Ιερός Ναός αγίου Μηνά", "Parish Church",
     "οδ. Ίωνος Δραγούμη 10\n546 23 Θεσσαλονίκη",
     ["2310-272.700"], ["inagiosminas@gmail.com"],
     "https://agiosminas.gr/", "ἐνοριακός-ἱερός-ναός-ἁγίου-μηνᾶ"),
    ("022", "Parish Church of Saint Nicholas in Charilaou",
     "Ενοριακός Ιερός Ναός αγίου Νικολάου (Χαριλάου)",
     "Parish Church", "Οδ. Γυμν. Μυσιρλή 34\n542 50 Θεσσαλονίκη",
     ["2310-306.886"], ["naosagnik@gmail.com", "agnikolaos0612@gmail.com"],
     None, "ἐνοριακός-ἱερός-ναός-ἁγίου-νικολάου"),
    ("023", "Parish Church of Saint Panteleimon in Panorama",
     "Ενοριακός Ιερός Ναός αγίου Παντελεήμονος (Πανοράματος)",
     "Parish Church", "οδ. Ιω. Φαρμάκη 27\n552 36 Πανόραμα",
     ["2310-345.675"], ["ag.panteleimon.panoramatos@gmail.com"],
     "https://inap-panorama.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίου-παντελεή"),
    ("024", "Parish Church of Saint Paul",
     "Ενοριακός Ιερός Ναός αγίου Παύλου", "Parish Church",
     "Λεωφόρος ΟΧΙ 16\n554 38 Αγ. Παύλος",
     ["2310-214.714"], ["inapavlou@outlook.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίου-παύλου"),
    ("025", "Parish Church of Saint Spyridon in Triandria",
     "Ενοριακός Ιερός Ναός αγίου Σπυρίδωνος (Τριανδρίας)",
     "Parish Church", "Πλ. αγ. Σπυρίδωνος\n555 37 Θεσσαλονίκη",
     ["2310-914.760"], ["Agiosspyridontriandrias@hotmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίου-σπυρίδων"),
    ("026", "Parish Church of Saints Phanourios and John the Baptist",
     "Ενοριακός Ιερός Ναός αγίων Φανουρίου - Τιμίου Προδρόμου",
     "Parish Church", "οδ. Ιωαννίνων 130\n546 39 Θεσσαλονίκη",
     ["2310-912.274"], ["agiosfantprod@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἁγίων-φανουρίο"),
    ("027", "Parish Church of Saint Photios",
     "Ενοριακός Ιερός Ναός αγίου Φωτίου", "Parish Church",
     "οδ. Λασκαράτου κ' Μαρίας Κάλλας\n546 46 Θεσσαλονίκη",
     ["2310-414.460"], ["info@agiosfotios.gr"],
     "https://www.agiosfotios.gr/",
     "ἐνοριακός-ἱερός-ναός-ἁγίου-φωτίου-π"),
    ("028", "Parish Church of Saint Christopher",
     "Ενοριακός Ιερός Ναός αγίου Χριστοφόρου", "Parish Church",
     "Οδ. Αθ. Σταγειρίτη 123\n543 52 Θεσσαλονίκη",
     ["2310-934.502"], ["agiosxristoforospylaias@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-χριστοφόρου"),
    ("029", "Parish Church of the Ascension of the Lord",
     "Ενοριακός Ιερός Ναός Αναλήψεως του Κυρίου", "Parish Church",
     "οδ. Αναλήψεως 6\n546 43 Θεσσαλονίκη",
     ["2310-830.306"], ["naosanalipsi@yahoo.com"], None,
     "ἐνοριακός-ἱερός-ναός-ἀναλήψεως-τοῦ"),
    ("030", "Parish Church of the Dormition of the Theotokos in the Forty Churches",
     "Ενοριακός Ιερός Ναός Κοιμήσεως της Θεοτόκου (40 Εκκλησιών)",
     "Parish Church", "Πλ. Πετρίδου\n546 36 Θεσσαλονίκη",
     ["2310-206.672"], ["inkoim40ek@gmail.com"],
     "https://panagia40ek.gr/",
     "ἐνοριακός-ἱερός-ναός-κοιμήσεως-τῆς-θ"),
    ("031", "Parish Church of the Transfiguration of the Saviour",
     "Ενοριακός Ιερός Ναός Μεταμορφώσεως του Σωτήρος",
     "Parish Church", "οδ. Δελφών και Μιαούλη\n546 42 Θεσσαλονίκη",
     ["2310-828.989"], [], "https://inmetamorfoseos.gr/",
     "ἐνοριακός-ἱερός-ναός-μεταμορφώσεως"),
    ("032", "Parish Church of Nea Panagia",
     "Ενοριακός Ιερός Ναός Νέας Παναγίας", "Parish Church",
     "οδ. Δημ. Γούναρη 8\n546 21 Θεσσαλονίκη",
     ["2310-274.040"], ["neapanagia@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-νέας-παναγίας"),
    ("033", "Parish Church of Venerable Xenia in Charilaou",
     "Ενοριακός Ιερός Ναός οσίας Ξένης (Χαριλάου)", "Parish Church",
     "οδ. Μαρασλή 74\n542 49 Θεσσαλονίκη",
     ["2310-300.448"], ["inosiaxeni@gmail.com"],
     "https://osiaxeni.gr/",
     "ἐνοριακός-ἱερός-ναός-ὁσίας-ξένης-χα"),
    ("034", "Byzantine Parish Church of Panagia Acheiropoietos",
     "Βυζαντινός Ενοριακός Ιερός Ναός Παναγίας της Αχειροποιήτου",
     "Parish Church", "οδ. Αγ. Σοφίας 56\n546 35 Θεσσαλονίκη",
     ["2310-227.369"], ["acheiropoiitos@gmail.com"], None,
     "βυζαντινός-ἐνοριακός-ἱερός-ναός-παν"),
    ("035", "Parish Church of Panagia Dexia",
     "Ενοριακός Ιερός Ναός Παναγίας της Δεξιάς", "Parish Church",
     "οδ. Εγνατία 123-125\n546 35 Θεσσαλονίκη",
     ["2310-209.753"], ["inpanagiadexia@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-παναγίας-τῆς-δε"),
    ("036", "Parish Church of Panagia Evangelistria",
     "Ενοριακός Ιερός Ναός Παναγίας της Ευαγγελιστρίας",
     "Parish Church", "οδ. Αγ. Δημητρίου 159\n546 34 Θεσσαλονίκη",
     ["2310-207.507"], ["panagia.euaggelistria@outlook.com"], None,
     "ἐνοριακός-ἱερός-ναός-παναγίας-τῆς-ε"),
    ("037", "Parish Church of Panagia Laodigitria",
     "Ενοριακός Ιερός Ναός Παναγίας της Λαοδηγητρίας",
     "Parish Church", "οδ. Ιουλιανού 50\n546 34 Θεσσαλονίκη",
     ["2310-210.159"], ["laodigitria@outlook.com"],
     "https://laodhghtria.blogspot.com/",
     "ἐνοριακός-ἱερός-ναός-παναγίας-τῆς-λα"),
    ("038", "Parish Church of Panagia Faneromeni in Kallithea",
     "Ενοριακός Ιερός Ναός Παναγίας της Φανερωμένης Καλλιθέας",
     "Parish Church", "οδ. Αρκαδιουπόλεως 20\n546 32 Θεσσαλονίκη",
     ["2310-512.278"], ["inpanfan@yahoo.gr"],
     "https://ierosnaospanagiasfaneromenis.blogspot.com/",
     "ἐνοριακός-ἱερός-ναός-παναγίας-τῆς-φα"),
    ("039", "Byzantine Parish Church of Panagia Chalkeon",
     "Βυζαντινός Ενοριακός Ιερός Ναός Παναγίας των Χαλκέων",
     "Parish Church", "οδ. Χαλκέων 2\n546 24 Θεσσαλονίκη",
     ["2310-272.910"], ["panagiachalkeon@gmail.com"], None,
     "βυζαντινός-ἐνοριακός-ἱερός-ναός-παν-2"),
    ("040", "Parish Church of the Nativity of the Theotokos, Panagouda",
     "Ενοριακός Ιερός Ναός Γενεσίου της Θεοτόκου (Παναγούδα)",
     "Parish Church", "οδ. Εγνατία 138\n546 22 Θεσσαλονίκη",
     ["2310-223.009"], ["ierosnaospanagoudas@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-γενεσίου-τῆς-θε"),
    ("041", "Byzantine Parish Church of Prophet Elijah in the City",
     "Βυζαντινός Ενοριακός Ιερός Ναός αγίου Προφήτου Ηλιού Πόλεως",
     "Parish Church", "οδ. Προφήτου Ηλία 20\n546 33 Θεσσαλονίκη",
     ["2310-273.790"], ["profitis.ilias.poleos.thess@gmail.com"], None,
     "βυζαντινός-ἐνοριακός-ἱερός-ναός-προ"),
    ("042", "Parish Church of Prophet Elijah in Pylaia",
     "Ενοριακός Ιερός Ναός αγίου Προφήτου Ηλιού Πυλαίας",
     "Parish Church", "Λεωφ. Προφήτου Ηλία 109-111\n555 35 Πυλαία",
     ["2310-300.934"],
     ["prophet.ilias.pylaias@gmail.com",
      "grammateia.profityiliapylaias@gmail.com"],
     None, "ἐνοριακός-ἱερός-ναός-ἁγίου-προφήτο"),
    ("043", "Byzantine Church of the Holy Archangels in the Acropolis",
     "Βυζαντικός Ιερός Ναός Παμμεγίστων Ταξιαρχών Ακροπόλεως",
     "Byzantine Church", "οδ. Θεοτοκοπούλου 40\n546 34 Θεσσαλονίκη",
     ["2310-209.546"], ["taxiarxesanopoli@gmail.com"], None,
     "βυζαντικός-ἱερός-ναός-παμμεγίστων-τ"),
    ("044", "Parish Church of Saint John the Baptist, the Catacomb",
     "Eνοριακός Iερός Ναός Τιμίου Προδρόμου (κατακόμβη)",
     "Parish Church", "Πλ. Aγίας Σοφίας\n546 22 Θεσσαλονίκη",
     ["2310-238.984"], ["ag.ioanniskatakomvi@gmail.com"], None,
     "ἑνοριακός-ἱερός-ναός-τιμίου-προδρόμ"),
    ("045", "Parish Church of the Three Holy Hierarchs in Voulgari",
     "Ενοριακός Ιερός Ναός αγίων Τριών Ιεραρχών (Βούλγαρη)",
     "Parish Church", "οδ. Στρωμνίτσης 59\n542 48 Θεσσαλονίκη",
     ["2310-305.422"], ["in3ierarxon@gmail.com"],
     "https://treisierarxesthessaloniki.blogspot.com/",
     "ἐνοριακός-ἱερός-ναός-ἁγίων-τριῶν-ἱε"),
    ("046", "Parish Church of the Meeting of the Lord",
     "Ενοριακός Ιερός Ναός Υπαπαντής του Χριστού", "Parish Church",
     "οδ. Εγνατία 148\n546 21 Θεσσαλονίκη",
     ["2310-278.514"], ["inipapantistouchristou@gmail.com"], None,
     "ἐνοριακός-ἱερός-ναός-ὑπαπαντῆς-τοῦ"),
]


# id suffix, English name, source name, rank, address, phones, profile path,
# optional additional competent source
MONASTIC_BODIES = [
    ("001", "Holy Monastery of the Dormition of the Theotokos",
     "Ιερά Μονή Κοιμήσεως της Θεοτόκου", "Monastery",
     "Τ.Κ.: 552 01 Πανόραμα Θεσ/νίκης", ["2310-341.102"],
     "ιερά-μονή-κοιμήσεως-της-θεοτόκου", None),
    ("002", "Holy Monastery of Venerable Theodora",
     "Ιερά Μονή Οσίας Θεοδώρας", "Monastery",
     "Ἑρμοῦ 34\n546 23 Θεσσαλονίκη", ["2310-220.020"],
     "ιερά-μονή-οσίας-θεοδώρας", EP_AGGREGATE),
    ("003", "Holy Hesychasterion of the Nativity of the Theotokos",
     "Ιερό Ησυχαστήριο Γενεσίου της Θεοτόκου", "Hesychasterion",
     "Αναπαύσεως 18\n552 00 Πανόραμα Θεσ/νίκης", ["2310-343.901"],
     "ιερό-ησυχαστήριο-γενεσίου-της-θεοτόκ", None),
    ("004", "Holy Hesychasterion of the Holy Trinity",
     "Ιερό Ησυχαστήριο Αγίας Τριάδος", "Hesychasterion",
     "Οδός Αναπαύσεως 36\nΠανόραμα, 552 36\nΘεσσαλονίκη",
     ["2310-343.454"], "ιερό-ησυχαστήριο-αγίας-τριάδος", None),
]


def seat_from_address(address):
    if "Θέρμη" in address:
        return "Thermi"
    if "Πυλαία" in address:
        return "Pylaia"
    if "Πανόραμα" in address:
        return "Panorama"
    if "Αγ. Παύλος" in address:
        return "Agios Pavlos"
    return "Thessaloniki"


def primary_row(item):
    suffix, name, local, rank, address, phones, emails, site, path = item
    source = profile(path)
    row = {
        "id": "gr-thessaloniki-church-%s" % suffix,
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat_from_address(address),
        "country": "GR",
        "address": address,
        "sources": [PARISH_ROSTER, source] + ([site] if site else []),
        "checked": CHECKED,
    }
    if phones:
        row["phones"] = phones
    if emails:
        row["emails"] = emails
    if site:
        row["site"] = site
    if phones or emails or site:
        row["contact_sources"] = [source] + ([site] if site else [])
        row["contact_checked"] = CHECKED
    return row


def monastic_row(item):
    suffix, name, local, rank, address, phones, path, extra = item
    source = profile(path)
    sources = [source]
    if extra:
        sources.append(extra)
    return {
        "id": "gr-thessaloniki-monastery-%s" % suffix,
        "parent": PARENT,
        "kind": "monastery",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat_from_address(address),
        "country": "GR",
        "address": address,
        "phones": phones,
        "sources": sources,
        "checked": CHECKED,
        "contact_sources": [extra or source],
        "contact_checked": CHECKED,
    }


ROWS = [primary_row(item) for item in PRIMARY_CHURCHES]
ROWS.extend(monastic_row(item) for item in MONASTIC_BODIES)


# id suffix, English name, source name, rank, parish-parent suffix or None,
# address, phones
CHAPELS = [
    ("001", "Apostle Paul Chapel in the Metropolitan Residence",
     "Aπόστολος Παύλος (εντός Μητροπολιτικού Οίκου)",
     "Metropolitan Chapel", None, None, []),
    ("002", "Saint Catherine Chapel on the Hill of the Constantinopolitans",
     "Αγ. Αικατερίνα (λόφου Κωνσταντινουπολιτών)",
     "Metropolitan Chapel", None, None, []),
    ("003", "Saints Silas and Timothy Chapel",
     "Αγ. Σίλας και Τιμόθεος (Τέρμα οδ. Πανεπιστημίου)",
     "Metropolitan Chapel", None, "Τέρμα οδ. Πανεπιστημίου", []),
    ("004", "Exaltation of the Precious Cross Chapel",
     "Ύψωσις Τιμίου Σταυρού (Νυμφών 8 - 555 35 Πυλαία)",
     "Metropolitan Chapel", None, "Νυμφών 8\n555 35 Πυλαία", []),
    ("005", "Saint Anysia Chapel", "Αγ. Ανυσία", "Parish Chapel", "046",
     "Γ' Σεπτεμβρίου & Γρηγορίου Λαμπράκη\n546 36 Θεσσαλονίκη",
     ["2310-278.514"]),
    ("006", "Saint Glykeria Chapel", "Αγ. Γλυκερία", "Parish Chapel",
     "028", "Γ. Σεφέρη & Κ. Βάρναλη\n555 34 Κωνσταντινουπολίτικα Πυλαίας",
     ["2310-934.502"]),
    ("007", "Saint Euphrosyne Chapel", "Αγ. Ευφροσύνη", "Parish Chapel",
     "019", "Γρ. Λαμπράκη 186\n543 52 Θεσσαλονίκη",
     ["2310-912.151"]),
    ("008", "Saint Solomoni Chapel", "Αγ. Σολομονή", "Parish Chapel",
     "011", "Βασιλίσσης Όλγας - Παρασκευοπούλου\n546 40 Θεσσαλονίκη",
     ["2310-831.831"]),
    ("009", "Saint Photini Chapel", "Αγ. Φωτεινή", "Parish Chapel", "046",
     "Γ' Σεπτεμβρίου & Γρηγορίου Λαμπράκη\n546 36 Θεσσαλονίκη",
     ["2310-278.514"]),
    ("010", "Saints Agape, Irene, and Chionia Chapel",
     "Αγ. Αγάπη, Ειρήνη και Χιονία", "Parish Chapel", "038",
     "Τριών Μαρτύρων 4\n546 32 Θεσσαλονίκη", ["2310-512.278"]),
    ("011", "Three Holy Hierarchs Chapel", "Αγ. Τρείς Ιεράρχες",
     "Parish Chapel", "029", "Δελφών 131\n542 48 Θεσσαλονίκη",
     ["2310-305.422"]),
    ("012", "Saint Basil of Kedrinos Hill Chapel",
     "Αγ. Βασίλειος Κεδρηνού Λόφου", "Parish Chapel", "012",
     "Πάρκο Δάσους\n546 34 Θεσσαλονίκη", ["2310-109.159"]),
    ("013", "Saint Eleftherios Chapel", "Αγ. Ελευθέριος",
     "Parish Chapel", "012", "Πρώην Φυλακές Επταπυργίου\n546 34 Θεσσαλονίκη",
     ["2310-209.159"]),
    ("014", "Saint John the Baptist Chapel", "Αγ. Ιωάννης ο Πρόδρομος",
     "Parish Chapel", "020", "Παπάφη 33\n546 38 Θεσσαλονίκη",
     ["2310-832.080"]),
    ("015", "Saint Nestor Chapel", "Αγ. Νέστωρ", "Parish Chapel", "030",
     "Αγ. Δημητρίου 159\n546 34 Θεσσαλονίκη", ["2310-247.044"]),
    ("016", "Transfiguration of the Saviour Chapel",
     "Μεταμόρφωσις του Σωτήρος", "Parish Chapel", "040",
     "Εγνατία 140\n546 22 Θεσσαλονίκη", ["2310-223.009"]),
    ("017", "Venerable Xenia and Saint Nektarios Chapel",
     "Οσ. Ξένη - Αγ. Νεκτάριος", "Parish Chapel", "033",
     "Παπαναστασίου 127\n542 50 Θεσσαλονίκη", ["2310-301.065"]),
    ("018", "Saint Paraskevi Chapel", "Αγ. Παρασκευή", "Parish Chapel",
     "035", "Επισκόπου Κίτρους Νικολάου 6\n546 34 Θεσσαλονίκη",
     ["2310-209.753"]),
    ("019", "All Saints of Thessaloniki Chapel at the Saint Gregory Palamas Foundation",
     "Αγ. Πάντες οι εν Θεσ/νίκη (Εκπαιδευτικού & Πολιτιστικού Ιδρύματος Αγ. Γρηγόριος ο Παλαμάς)",
     "Institution Chapel", None, "Νικ. Πλαστήρα 65\n542 50 Θεσσαλονίκη",
     ["2310-306.886"]),
    ("020", "Saint John the Baptist Chapel at the Second Child Asylum Complex",
     "Αγ. Ιωάννης ο Πρόδρομος (Β' Συγκροτήματος Ασύλου του Παιδιού)",
     "Institution Chapel", None, "Στ. Καζαντζίδη 30\n555 35 Πυλαία",
     ["2310-472.702"]),
    ("021", "Saint Nektarios Chapel at the Chariseio Nursing Home",
     "Αγ. Νεκτάριος (Χαρισείου Γηροκομείου Θεσσαλονίκης)",
     "Institution Chapel", None,
     "Κισσού 3 και Δημητρίου Χαρίση\n543 52 Θεσσαλονίκη",
     ["2310-913.310"]),
    ("022", "Saint Stylianos Chapel at the First Child Asylum Complex",
     "Αγ. Στυλιανός (Α' Συγκροτήματος Ασύλου του Παιδιού)",
     "Institution Chapel", None, "Εγνατία 129\n546 38 Θεσσαλονίκη",
     ["2310-270.165"]),
    ("023", "Saint Stylianos Chapel at the Thessaloniki Municipal Nursery",
     "Αγ. Στυλιανός (Βρεφοκομείου Δήμου Θεσσαλονίκης)",
     "Institution Chapel", None, "28ης Οκτωβρίου 99\n546 42 Θεσσαλονίκη",
     ["2310-941.777", "2310-929.600"]),
    ("024", "Transfiguration of the Saviour Chapel at the School for the Blind",
     "Μεταμόρφωσις του Σωτήρος (Κ.Ε.Α.Τ. Σχολής Τυφλών)",
     "Institution Chapel", None, "Βασιλίσσης Όλγας 32\n546 41 Θεσσαλονίκη",
     ["2310-830.095"]),
    ("025", "Saint John Chrysostom Chapel at the American Farm School",
     "Αγ. Ιωάννης ο Χρυσόστομος (Αμερικανικής Γεωργικής Σχολής)",
     "Institution Chapel", None, "Μαρίνου Αντύπα 54\n570 01 Θέρμη",
     ["2310-492.700"]),
    ("026", "Apostle Paul Chapel at Malakopi Cemetery",
     "Αγ. Απόστολος Παύλος (Κοιμητήρια Μαλακοπής)",
     "Cemetery Chapel", None, "Κισσού 1\n543 52 Θεσσαλονίκη",
     ["2310-912.356"]),
    ("027", "Resurrection of the Lord Chapel at the New Cemeteries",
     "Ανάστασις του Κυρίου (Νέα Κοιμητήρια)", "Cemetery Chapel", None,
     "Στ. Καζαντζίδη 28\n555 35 Πυλαία", ["693 23 23 23 4"]),
    ("028", "Holy Theodores Chapel at Pylaia Cemetery",
     "Αγ. Θεόδωροι (Κοιμητήρια Πυλαίας)", "Cemetery Chapel", None,
     "Λεωφ. Πυλαίας - Πανοράματος", ["2310-300.934"]),
    ("029", "Holy Trinity Chapel at Panorama Cemetery",
     "Αγ. Τριάς (Κοιμητήρια Πανοράματος)", "Cemetery Chapel", None,
     "Αναπαύσεως 10\n552 36 Πανόραμα", ["2310-341.059"]),
    ("030", "Protection of the Theotokos Church at Georgios Gennimatas General Hospital",
     "Αγ. Σκέπη (Γ.Ν.Θ. Γεώργιος Γεννηματάς)", "Hospital Church", None,
     "Πανεπιστημίου\n546 36 Θεσσαλονίκη", ["2310-211.211"]),
    ("031", "Saint Demetrius Church at Saint Demetrius General Hospital",
     "Αγ. Δημήτριος (Γ.Ν.Θ. Αγ. Δημήτριος)", "Hospital Church", None,
     "Επταπύργιον\n540 02 Θεσσαλονίκη", ["2310-203.874"]),
    ("032", "Saint Luke Church at AHEPA University General Hospital",
     "Αγ. Λουκάς (Πανεπιστημιακού Γ.Ν.Θ. ΑΧΕΠΑ)", "Hospital Church",
     None, "Στίλπ. Κυριακίδη 1\n546 36 Θεσσαλονίκη", ["2310-993.111"]),
    ("033", "Saint Panteleimon Church at Theageneio Anticancer Hospital",
     "Αγ. Παντελεήμων (Θεαγενείου Αντικαρκινικού Ν.Θ.)",
     "Hospital Church", None, "Αλ. Συμεωνίδη 2\n546 39 Θεσσαλονίκη",
     ["2310-829.912"]),
    ("034", "Saint Panteleimon Church at Hippokrateio General Hospital",
     "Αγ. Παντελεήμων (Γ.Ν.Θ. Ιπποκράτειο)", "Hospital Church", None,
     "Κωνσταντινουπόλεως 49\n546 42 Θεσσαλονίκη", ["2310-892.807"]),
    ("035", "Saints Constantine and Helen Military Parish at the Third Army Corps",
     "Αγ. Κων/νος & Ελένη Γ' Σώματος Στρατού", "Military Parish", None,
     "Λεωφόρος Στρατού\n546 39 Θεσσαλονίκη", ["2310-893.174"]),
    ("036", "Saint Demetrius Military Parish at the Military School of Corps Officers",
     "Αγ. Δημήτριος Στρατιωτικής Σχολής Αξιωματικών Σωμάτων",
     "Military Parish", None,
     "Προέκτασις Εγνατίας έναντι πρώην 424 Στρατιωτικού Νοσοκομείου\n546 39 Θεσσαλονίκη",
     ["2310-962.000"]),
    ("037", "Saint George Military Parish at the Supreme Joint War School",
     "Αγ. Γεώργιος Ανωτάτης Διακλαδικής Σχολής Πολέμου",
     "Military Parish", None, "Λεωφ. Γεωργικής Σχολής 29\n555 35 Πυλαία",
     ["2310-472.603"]),
    ("038", "Three Holy Hierarchs Church at the Aristotle University Student Residences",
     "Αγ. Τρείς Ιεράρχαι (Φοιτητικών Εστιών Α.Π.Θ.)",
     "University Church", None,
     "Α' Φοιτητική Εστία Θεσσαλονίκης\nΣτίλπ. Κυριακίδη 17\n546 36 Θεσσαλονίκη",
     ["698 77 10 55 4"]),
    ("039", "Saint Basil Church at the Apostle Paul Schools",
     "Αγ. Βασίλειος (Εκπαιδευτηρίων Ο Απόστολος Παύλος)",
     "School Church", None, "Κέννεντυ 119\n555 35 Πυλαία",
     ["2310-321.110"]),
]


def chapel_row(item):
    suffix, name, local, rank, parish_suffix, address, phones = item
    parent = (
        "gr-thessaloniki-church-%s" % parish_suffix
        if parish_suffix else PARENT)
    row = {
        "id": "gr-thessaloniki-chapel-%s" % suffix,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat_from_address(address or ""),
        "country": "GR",
        "sources": [CHAPEL_ROSTER],
        "checked": CHECKED,
    }
    if address:
        row["address"] = address
    if phones:
        row["phones"] = phones
        row["contact_sources"] = [CHAPEL_ROSTER]
        row["contact_checked"] = CHECKED
    return row


ROWS.extend(chapel_row(item) for item in CHAPELS)
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_COUNT = 89
EXPECTED_RANKS = {
    "Byzantine Church": 2,
    "Cathedral": 1,
    "Cemetery Chapel": 4,
    "Hesychasterion": 2,
    "Hospital Church": 5,
    "Institution Chapel": 7,
    "Metropolitan Chapel": 4,
    "Metropolitan Church": 1,
    "Military Parish": 3,
    "Monastery": 2,
    "Parish Chapel": 14,
    "Parish Church": 39,
    "Pilgrimage Church": 3,
    "School Church": 1,
    "University Church": 1,
}
EXPECTED_KINDS = {"monastery": 4, "parish": 85}
EXPECTED_PARENT_COUNTS = {
    PARENT: 75,
    "gr-thessaloniki-church-011": 1,
    "gr-thessaloniki-church-012": 2,
    "gr-thessaloniki-church-019": 1,
    "gr-thessaloniki-church-020": 1,
    "gr-thessaloniki-church-028": 1,
    "gr-thessaloniki-church-029": 1,
    "gr-thessaloniki-church-030": 1,
    "gr-thessaloniki-church-033": 1,
    "gr-thessaloniki-church-035": 1,
    "gr-thessaloniki-church-038": 1,
    "gr-thessaloniki-church-040": 1,
    "gr-thessaloniki-church-046": 2,
}
EXPECTED_ADDRESS_BODIES = 87
EXPECTED_CONTACT_BODIES = 84
EXPECTED_PHONE_BODIES = 83
EXPECTED_EMAIL_BODIES = 44
EXPECTED_SITE_BODIES = 17
ALLOWED_KINDS = set(EXPECTED_KINDS)
ALLOWED_RANKS = set(EXPECTED_RANKS)
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2018\u2019\u201c\u201d\ufffd]")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            for text in walk_strings(item):
                yield text
    elif isinstance(value, dict):
        for item in value.values():
            for text in walk_strings(item):
                yield text


def unicase(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value.casefold()).strip()


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s is not a current HTTPS URL: %s" %
                         (label, value))


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s lacks bounded official provenance" % row.get("id"))
    for source_url in sources:
        validate_url(source_url, row.get("id"))
        if (urlparse(source_url).netloc not in {"imth.gr", "ec-patr.org"} and
                source_url != row.get("site")):
            raise ValueError("%s carries a non-competent identity source" %
                             row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    contact_sources = list(row.get("contact_sources") or [])
    has_contacts = bool(
        row.get("phones") or row.get("emails") or row.get("site"))
    if has_contacts and not contact_sources:
        raise ValueError("%s lacks contact provenance" % row.get("id"))
    if contact_sources:
        if len(contact_sources) > 3:
            raise ValueError("%s carries too many contact sources" % row.get("id"))
        for source_url in contact_sources:
            validate_url(source_url, row.get("id"))
            if source_url not in sources:
                raise ValueError("%s has contact provenance outside its sources" %
                                 row.get("id"))
        if row.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks the current contact check date" %
                             row.get("id"))
    if row.get("site"):
        validate_url(row["site"], row.get("id"))
    return row


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if (ledger.get("v") != 1 or ledger.get("countries") != ["GR"] or
            ledger.get("parent") != PARENT):
        raise ValueError("Thessaloniki candidate ledger metadata drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        "principal_churches": 46,
        "monasteries": 2,
        "hesychasteria": 2,
        "named_chapels_and_other_worship_bodies": 39,
        "total": EXPECTED_COUNT,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Thessaloniki candidate ledger %s drifted" % key)
    candidate_ids = {
        item.get("candidate_id") for item in ledger.get("candidates") or []
    }
    if candidate_ids != {
            "gr-thessaloniki-aggregate-roster-reconciliation",
            "gr-thessaloniki-monastic-worship-bodies",
            "gr-thessaloniki-search-and-map-leads"}:
        raise ValueError("Thessaloniki candidate holdings drifted")
    return ledger


def build():
    result = []
    seen = {PARENT}
    ids = set()
    signatures = set()
    rank_counts = Counter()
    kind_counts = Counter()
    parent_counts = Counter()
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in ids or row_id == PARENT:
            raise ValueError("duplicate or missing id: %s" % row_id)
        parent = row.get("parent")
        if parent not in seen:
            raise ValueError("%s precedes or lacks its parent %s" %
                             (row_id, parent))
        if row.get("country") != "GR":
            raise ValueError("%s carries the wrong country" % row_id)
        if row.get("kind") not in ALLOWED_KINDS:
            raise ValueError("%s carries an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s carries an unsupported rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks an English or Greek name" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in row["local"]):
            raise ValueError("%s lacks its Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(row)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for email in row.get("emails") or []:
            if not EMAIL_RE.match(email):
                raise ValueError("%s carries an invalid email" % row_id)
        for phone in row.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        signature = (
            parent, row.get("rank"), unicase(row.get("local")),
            unicase(row.get("address")))
        if signature in signatures:
            raise ValueError("%s duplicates another body" % row_id)
        signatures.add(signature)
        ids.add(row_id)
        seen.add(row_id)
        rank_counts[row["rank"]] += 1
        kind_counts[row["kind"]] += 1
        parent_counts[parent] += 1
        result.append(row)
    if len(result) != EXPECTED_COUNT:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_COUNT, len(result)))
    if set(ENGLISH_NAMES) != ids:
        raise ValueError("Thessaloniki English name coverage drifted")
    seats = {row["seat"] for row in result if row.get("seat")}
    if set(ENGLISH_SEATS) != seats:
        raise ValueError("Thessaloniki English seat coverage drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Thessaloniki rank counts drifted: %r" % rank_counts)
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Thessaloniki kind counts drifted: %r" % kind_counts)
    if dict(sorted(parent_counts.items())) != EXPECTED_PARENT_COUNTS:
        raise ValueError("Thessaloniki parent counts drifted: %r" % parent_counts)
    addresses = sum(bool(row.get("address")) for row in result)
    contacts = sum(
        bool(row.get("phones") or row.get("emails") or row.get("site"))
        for row in result)
    phones = sum(bool(row.get("phones")) for row in result)
    emails = sum(bool(row.get("emails")) for row in result)
    sites = sum(bool(row.get("site")) for row in result)
    if (addresses, contacts, phones, emails, sites) != (
            EXPECTED_ADDRESS_BODIES, EXPECTED_CONTACT_BODIES,
            EXPECTED_PHONE_BODIES, EXPECTED_EMAIL_BODIES,
            EXPECTED_SITE_BODIES):
        raise ValueError("Thessaloniki contact coverage drifted")
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
    if args.check or not args.dump:
        print(
            "Thessaloniki: %d officially named bodies; 46 principal "
            "churches, 4 monastic bodies, and 39 named chapels or "
            "other worship bodies; %d carry current official contact data" %
            (EXPECTED_COUNT, EXPECTED_CONTACT_BODIES)
        )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
