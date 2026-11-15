#!/usr/bin/env python3
"""Current official worship-body roster for Lemnos and Saint Eustratios.

The current metropolis roster names 37 principal parishes. Its parish pages
name 226 subordinate chapels, and its pilgrimage page names Saint Sozon.
Aggregate-only bodies remain in the adjacent candidate ledger.
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
PARENT = "ep-lemnos"
PARISH_ROSTER = (
    "https://www.imlimnou.gr/index.php/2022-06-26-16-43-19/"
    "2022-06-26-16-45-27"
)
PARISH_PROFILE = PARISH_ROSTER + "?view=article&id=%s&catid=9"
PILGRIMAGE = (
    "https://www.imlimnou.gr/index.php/2022-06-26-16-43-19/"
    "2022-07-23-16-44-34"
)
EP_OVERVIEW = "https://ec-patr.org/entities/iera-mitropoli-limnoy/"
PARENT_SITE = "https://www.imlimnou.gr/"
CANDIDATE_LEDGER = (
    Path(__file__).with_name("directory_candidates") /
    "lemnos_country.json"
)


# Page id, English name, exact source title, English seat, source address,
# institutional phones, institutional email, exact named parish chapels.
PARISHES = [
    (
        "57", "Metropolitan Church of the Holy Trinity in Myrina",
        "Ι. Μ. Ν. Αγ. Τριάδος Μυρίνης", "Myrina", "Μύρινα 814 00",
        ["22540-22109"], "imnagiastriados@gmail.com",
        [
            "Αγ. Λαζάρου Κοιμητηρίου",
            "Αγ. Παρασκευής Ρωμέικου Γιαλού",
            "Γεννήσεως Θεοτόκου Αγοράς",
            "Παμμεγίστων Ταξιαρχών Αγοράς",
        ],
    ),
    (
        "65", "Parish Church of the Holy Unmercenaries in Dafni",
        "Ι. Ν. Αγ. Αναργύρων Δάφνης", "Dafni", "Δάφνη 814 00", [],
        "ag.anargyroi.dafnis@gmail.com",
        [
            "Αγ. Αναργύρων (Θέση Κοντοβράκι)",
            "Αγ. Δημητρίου",
            "Αγ. Ελευθερίου και Χριστοφόρου",
            "Αγ. Κλήμεντος",
            "Αγ. Κυριακής και Σοφίας",
            "Αγ. Παντελεήμονος Χάρακος",
            "Αποτομής Τιμίας Κεφαλής Αγ. Ιωάννου Προδρόμου",
            "Κοιμήσεως Θεοτόκου Χάρακος",
            "Οσίου Αθανασίου του εν Άθω Χάρακος",
            "Προφήτου Ηλιού",
        ],
    ),
    (
        "60", "Parish Church of Saint George in Angariones",
        "Ι. Ν. Αγ. Γεωργίου Αγγαριώνων", "Angariones",
        "Αγγαριώνες 814 00", [], "ag.georgios.aggarionon@gmail.com",
        ["Αγ. Ευστρατίου", "Αγ. Σοφίας"],
    ),
    (
        "63", "Parish Church of Saint George in Atsiki",
        "Ι. Ν. Αγ. Γεωργίου Ατσικής", "Atsiki", "Ατσική 814 01",
        ["22540-31437"], "ag.georgios.atsikis@gmail.com",
        [
            "Αγ. Βλασίου",
            "Αγ. Γεωργίου",
            "Αγ. Γεωργίου Κρηνίδος",
            "Αγ. Γεωργίου (ο Μικρός)",
            "Αγ. Ειρήνης",
            "Αγ. Ερμολάου",
            "Αγ. Ιωάννου",
            "Αγ. Ιωάννου (Θέση Γαïδουρόμαντρες)",
            "Αγ. Κωνσταντίνου",
            "Αγ. Νικολάου",
            "Αγ. Παρασκευής (Θέση Γαïδουρόμαντρες)",
            "Αγ. Σώζοντος (Θέση Λούκι)",
        ],
    ),
    (
        "67", "Parish Church of Saint George in Kallithea",
        "Ι. Ν. Αγ. Γεωργίου Καλλιθέας", "Kallithea",
        "Καλλιθέα 814 00", [], "ag.georgios.kallitheas@gmail.com",
        [
            "Αγ. Αντωνίου",
            "Αγ. Γεωργίου",
            "Αγ. Μελιτινής",
            "Αγ. Φωτίδος",
            "Αγ. Χαραλάμπους",
            "Προφήτου Ηλιού και Αγ. Δημητρίου",
        ],
    ),
    (
        "68", "Parish Church of Saint George in Kalliopi",
        "Ι. Ν. Αγ. Γεωργίου Καλλιόπης", "Kalliopi", "Καλλιόπη 814 01",
        [], "ag.georgios.kalliopis@gmail.com",
        [
            "Αγ. Γεωργίου Κέρους",
            "Αγ. Ιωάννου Κέρους",
            "Αγ. Κυριακής Κέρους",
            "Αγ. Παρασκευής Κέρους",
        ],
    ),
    (
        "71", "Parish Church of Saint George in Kaspakas",
        "Ι. Ν. Αγ. Γεωργίου Κάσπακα", "Kaspakas", "Κάσπακας 814 00",
        [], "ag.georgios.kaspaka@gmail.com",
        [
            "Αγ. Αθανασίου",
            "Αγ. Γεωργίου Ποταμού",
            "Αγ. Θεοδώρων (Θέση Λάζου)",
            "Αγ. Ιωάννου Μούρτζουφλου",
            "Αγ. Ιωάννου (Παραλία Αγίου Ιωάννου)",
            "Αγ. Κυριακής Κεραμιδαριάς",
            "Αγ. Παντελεήμονος (Θέση Πλιτς)",
            "Αγ. Παρασκευής (Θέση Ρους)",
            "Αγ. Σπυρίδωνος Κοιμητηρίου",
            "Αγ. Σπυρίδωνος Ροδανιάς",
            "Αγ. Φανουρίου Παραλίας Αγίου Ιωάννου",
            "Αναλήψεως Χριστού (Θέση Σπλιδ)",
            "Προφήτου Ηλιού Καρβουνόλακα",
        ],
    ),
    (
        "83", "Parish Church of Saint George in Platy",
        "Ι. Ν. Αγ. Γεωργίου Πλατέος", "Platy", "Πλατύ 814 00", [],
        "ag.georgios.plateos@gmail.com",
        [
            "Αγ. Αναργύρων (Είσοδος Πλατέος)",
            "Αγ. Δημητρίου Κοιμητηρίου",
            "Αγ. Κηρύκου και Ιουλίττης Παραλίας Πλατέος",
            "Αγ. Κυριακής Παραλίας Πλατέος",
            "Προφήτου Ηλιού (Προέκταση Παραλίας Πλατέος)",
        ],
    ),
    (
        "86", "Parish Church of Saint George in Repanidi",
        "Ι. Ν. Αγ. Γεωργίου Ρεπανιδίου", "Repanidi", "Ρεπανίδι 814 01",
        [], "ag.georgios.repanidiou@gmail.com",
        [
            "Αγ. Αθανασίου Ανυπάτη",
            "Αγ. Γεωργίου (Μνημειακός Ναός)",
            "Αγ. Γεωργίου Κότσινα",
            "Αγ. Σοφίας Κότσινα",
            "Ζωοδόχου Πηγής Κότσινα",
        ],
    ),
    (
        "73", "Parish Church of Saint Demetrius in Kontias",
        "Ι. Ν. Αγ. Δημητρίου Κοντιά", "Kontias", "Κοντιάς 814 01", [],
        "ag.dimitrios.kontia@gmail.com", [],
    ),
    (
        "74", "Parish Church of Saint Demetrius in Kontopouli",
        "Ι. Ν. Αγ. Δημητρίου Κοντοπουλίου", "Kontopouli",
        "Κοντοπούλι 814 01", ["22540-41820"],
        "inagdimitrioukontopoul@gmail.com",
        [
            "Αγ. Αναστασίας Φαρμακολυτρίας",
            "Αγ. Άννης Σαράβαρης",
            "Αγ. Θεοδώρων Σαράβαρης",
            "Αγ. Κηρύκου Πασάδικων",
            "Αγ. Νεκταρίου",
            "Αγ. Παχωμίου Οικισμού Αγ. Αλεξάνδρου",
            "Αγ. Πολυκάρπου",
            "Αγ. Σπυρίδωνος",
            "Αγ. Τριάδος",
            "Αγ. Φιλοθέης",
        ],
    ),
    (
        "77", "Parish Church of Saint Demetrius in Lychna",
        "Ι. Ν. Αγ. Δημητρίου Λύχνων", "Lychna", "Λύχνα 814 01", [],
        "ag.dimitrios.lyxnon@gmail.com",
        [
            "Αγ. Γεωργίου",
            "Αγ. Θεοδώρων",
            "Αγ. Ιωάννου Προδρόμου",
            "Αγ. Νικολάου",
        ],
    ),
    (
        "62", "Parish Church of Saint Demetrius in Agios Dimitrios",
        "Ι. Ν. Αγ. Δημητρίου Ομωνύμου Δημ. Διαμερίσματος",
        "Agios Dimitrios", "Άγιος Δημήτριος 814 00", [],
        "inagdimlimnou@gmail.com",
        [
            "Αγ. Γεωργίου Κουρουνίου",
            "Αγ. Ιακώβου του εν Ευβοία",
            "Αγ. Κωνσταντίνου και Ελένης",
            "Αγ. Νεκταρίου",
            "Αγ. Οσιομάρτυρος Εφραίμ του Νέου",
            "Αγ. Φανουρίου",
        ],
    ),
    (
        "82", "Parish Church of Saint Demetrius in Plaka",
        "Ι. Ν. Αγ. Δημητρίου Πλάκας", "Plaka", "Πλάκα 814 01", [],
        "ag.dimitrios.plakas@gmail.com",
        [
            "Αγ. Αποστόλων Φάρου",
            "Αγ. Ελένης",
            "Αγ. Ευστρατίου Σπανοχωρίου",
            "Αγ. Ιωάννου Παλαιού Λιμένος",
            "Αγ. Χαραλάμπους",
            "Μεταμορφώσεως Σωτήρος",
        ],
    ),
    (
        "85", "Parish Church of Saint Demetrius in Propouli",
        "Ι. Ν. Αγ. Δημητρίου Προπουλίου", "Propouli", "Προπούλι 814 01",
        [], "ag.dimitrios.propouliou@gmail.com",
        [
            "Αγ. Αικατερίνης",
            "Αγ. Αναργύρων",
            "Αγ. Γεωργίου",
            "Αγ. Ειρήνης Χρυσοβαλάντου",
            "Αγ. Ιωάννου",
            "Αγ. Μάμαντος",
            "Αγ. Νικολάου",
            "Αγ. Παρασκευής",
            "Αγ. Παύλου",
        ],
    ),
    (
        "87", "Parish Church of Saint Demetrius in Roussopouli",
        "Ι. Ν. Αγ. Δημητρίου Ρουσσοπουλίου", "Roussopouli",
        "Ρουσσοπούλι 814 01", [], "ag.dimitrios.roussopouliou@gmail.com",
        [],
    ),
    (
        "89", "Parish Church of Saint Demetrius in Sardes",
        "Ι. Ν. Αγ. Δημητρίου Σαρδών", "Sardes", "Σαρδές 814 00", [],
        "ag.dimitrios.sardon@gmail.com",
        [
            "Αγ. Γεωργίου",
            "Αγ. Κηρύκου και Ιουλίττης",
            "Αγ. Κωνσταντίνου και Ελένης",
            "Αγ. Μαρίνης",
            "Αγ. Παρασκευής",
        ],
    ),
    (
        "92", "Parish Church of Saint John in Fisini",
        "Ι. Ν. Αγ. Ιωάννου Φυσίνης", "Fisini", "Φυσίνη 814 01", [],
        "ag.ioannis.fysinis@gmail.com",
        [
            "Αγ. Αναργύρων",
            "Αγ. Γεωργίου",
            "Αγ. Δημητρίου",
            "Αγ. Νικολάου",
            "Αγ. Ονουφρίου",
            "Κοιμήσεως Θεοτόκου",
            "Προφήτου Ηλιού Κοιμητηρίου",
        ],
    ),
    (
        "76", "Parish Church of Saint Marina in Livadochori",
        "Ι. Ν. Αγ. Μαρίνης Λειβαδοχωρίου", "Livadochori",
        "Λειβαδοχώρι 814 00", [], "ag.marina.leivadochoriou@gmail.com",
        [
            "Αγ. Βαβάρας",
            "Αγ. Βασιλείου",
            "Αγ. Γεωργίου Κοιμητηρίου",
            "Αγ. Δημητρίου Στρατοπέδου «ΥΠΙΛΑΡΧΟΥ ΚΑΡΔΑΜΗΛΑ»",
            "Αγ. Θεοδώρων",
            "Αγ. Κωνσταντίνου και Ελένης",
            "Αγ. Παρασκευής",
            "Αποτομής Τιμίας Κεφαλής Αγ. Ιωάννου Προδρόμου",
        ],
    ),
    (
        "79", "Parish Church of Saint Marina in Nea Koutali",
        "Ι. Ν. Αγ. Μαρίνης Νέας Κούταλης", "Nea Koutali",
        "Νέα Κούταλη 814 00", [], "ag.marina.neaskoutalis@gmail.com",
        [
            "Αγ. Βαρβάρας",
            "Αγ. Νεκταρίου",
            "Αγ. Νικολάου Πούντας",
            "Αγ. Πέτρου και Παύλου",
            "Αγ. Τριάδος",
            "Παναγίας Φανερωμένης",
        ],
    ),
    (
        "72", "Parish Church of Saint Modestus in Katalakko",
        "Ι. Ν. Αγ. Μοδέστου Καταλάκκου", "Katalakko",
        "Κατάλακκο 814 00", [], "ag.modestos.katallakou@gmail.com",
        [
            "Αγ. Αθανασίου Αθωνίτου (Παραλία Γομάτι)",
            "Αγ. Γεωργίου (Θέση Χαρκόπες)",
            "Αγ. Γεωργίου Ράχης",
            "Αγ. Γεωργίου (Παραλία Γομάτι)",
            "Αγ. Δημητρίου",
            "Αγ. Νικολάου (Παραλία Γομάτι)",
            "Αγ. Νεκταρίου",
            "Αγ. Παρασκευής (Παραλία Γομάτι)",
            "Ζωοδόχου Πηγής (Παραλία Γομάτι)",
            "Κοιμήσεως Θεοτόκου",
            "Κοιμήσεως Θεοτόκου (Παραλία Γομάτι)",
        ],
    ),
    (
        "90", "Parish Church of Saint Nicholas in Skandali",
        "Ι. Ν. Αγ. Νικολάου Σκανδάλης", "Skandali", "Σκανδάλη 814 01",
        [], "ag.nikolaos.skandalis@gmail.com",
        [
            "Αγ. Αθανασίου",
            "Αγ. Γεωργίου (Θέση Καμαρωτό)",
            "Αγ. Γεωργίου (Θέση Νενό)",
            "Αγ. Γεωργίου (Θέση Ορφανός)",
            "Αγ. Γρηγορίου",
            "Αγ. Δημητρίου",
            "Αγ. Ειρήνης",
            "Αγ. Κωνσταντίνου και Ελένης",
            "Αγ. Μαρίνης",
            "Αγ. Στεφάνου",
            "Κοιμήσεως Θεοτόκου Κοιμητηρίου",
        ],
    ),
    (
        "59", "Parish Church of Saint Panteleimon in Myrina",
        "Ι. Ν. Αγ. Παντελεήμονος Μυρίνης", "Myrina", "Μύρινα 814 00",
        [], "ag.panteleimon.myrinas@gmail.com",
        [
            "Αγ. Βαρβάρας Ανδρωνίου (Ξενοδοχείο Ελβετικά)",
            "Αγ. Μαρίνης Ανδρωνίου",
            "Αγ. Παρασκευής Ανδρωνίου (Πλησίον Στρατοπέδου «ΝΑΥΑΡΧΟΥ ΚΟΥΝΤΟΥΡΙΩΤΗ»)",
        ],
    ),
    (
        "81", "Parish Church of All Saints in Pedino",
        "Ι. Ν. Αγ. Πάντων Πεδινού", "Pedino", "Πέδινο 814 00", [],
        "ag.pantes.pedinou@gmail.com",
        [
            "Αγ. Ιωάννου Προδρόμου Παλαιού Πεδινού",
            "Αγ. Ειρήνης Χρυσοβαλάντου Παλαιού Πεδινού",
            "Μεταμορφώσεως Σωτήρος Παλαιού Πεδινού",
        ],
    ),
    (
        "66", "Parish Church of Saint Paraskevi in Thanos",
        "Ι. Ν. Αγ. Παρασκευής Θάνους", "Thanos", "Θάνος 814 00", [],
        "ag.paraskevi.thanous@gmail.com",
        [
            "Αγ. Ιωάννου Κάμπου",
            "Αγ. Κωνσταντίνου",
            "Αγ. Παρασκευής Στυβής",
            "Αγ. Παρασκευής Παλαιού Κοιμητηρίου",
            "Αγ. Παύλου",
            "Αγ. Χαραλάμπους Κοιμητηρίου",
            "Παναγίας Κακαβιωτίσσης",
            "Προφήτου Ζαχαρίου Ζεματά",
        ],
    ),
    (
        "70", "Parish Church of Saint Pachomius in Karpasi",
        "Ι. Ν. Αγ. Παχωμίου Καρπασίου", "Karpasi", "Καρπάσι 814 01", [],
        "ag.paxomios.karpasiou@gmail.com",
        ["Αγ. Νικολάου", "Αγ. Χριστοφόρου"],
    ),
    (
        "61", "Parish Church of Saint Sophia in Agia Sofia",
        "Ι. Ν. Αγ. Σοφίας Ομωνύμου Δημ. Διαμερίσματος", "Agia Sofia",
        "Αγία Σοφία 814 01", [], "ag.sofia.ag.sofias@gmail.com",
        [
            "Αγ. Ευστρατίου",
            "Αγ. Μαρίνου",
            "Αγ. Νικολάου",
            "Αγ. Σπυρίδωνος",
            "Εισοδίων Θεοτόκου Παραδεισίου",
        ],
    ),
    (
        "80", "Parish Church of the Nativity of the Theotokos in Panagia",
        "Ι. Ν. Γεννήσεως Θεοτόκου Παναγιάς", "Panagia",
        "Παναγιά 814 01", [], "gen.theotokou.panagias@gmail.com",
        [
            "Αγ. Αναργύρων Παλαιοκάστρου",
            "Αγ. Γεωργίου Μαρμάρου",
            "Αγ. Δημητρίου Κοιμητηρίου",
            "Αγ. Μοδέστου Κορτισώνος",
            "Αγ. Παρασκευής (Θέση Πετσά)",
            "Αγ. Τρύφωνος Μαρμάρου",
            "Κοιμήσεως Θεοτόκου",
            "Παμμεγίστου Ταξιάρχου Μιχαήλ Σπανοχωρίου",
        ],
    ),
    (
        "93", "Parish Church of the Nativity of Christ on Saint Eustratios",
        "Ι. Ν. Γεννήσεως Χριστού Νήσου Αγ. Ευστρατίου",
        "Agios Efstratios", "Άγιος Ευστράτιος 815 00", [],
        "gen.christou.ag.eustratiou@gmail.com", [],
    ),
    (
        "88", "Parish Church of the Nativity of Christ in Romano",
        "Ι. Ν. Γεννήσεως Χριστού Ρωμανού", "Romano", "Ρωμανού 814 01",
        [], "gen.christou.romanou@gmail.com",
        [
            "Αγ. Ανδρέου",
            "Αγ. Ιωάννου Κώμης",
            "Αγ. Κωνσταντίνου και Ελένης",
            "Αγ. Νικολάου",
            "Αγ. Παρασκευής (Θέση Κβάρες)",
            "Αγ. Στεφάνου",
            "Αγ. Φωτίδος",
            "Δεσπότου Χριστού Λίμνης",
            "Κοιμήσεως Θεοτόκου Λειβαδίου",
            "Παναγίας Καματερής Μύτακα",
            "Παναγίας Πάντων Χαράς (Θέση Παναγίδα)",
        ],
    ),
    (
        "64", "Parish Church of the Presentation of the Theotokos in Varos",
        "Ι. Ν. Εισοδίων Θεοτόκου Βάρους", "Varos", "Βάρος 814 01", [],
        "eis.theotokou.varous@gmail.com",
        [
            "Αγ. Γεωργίου",
            "Αγ. Ευστρατίου",
            "Αγ. Κυριακής Μπουρνιά",
            "Αγ. Μαρίνης",
            "Αγ. Νικολάου Μπουρνιά",
            "Αγ. Παρασκευής Καμαρών",
            "Αγ. Χαραλάμπους",
            "Μεταμορφώσεως Σωτήρος",
        ],
    ),
    (
        "84", "Parish Church of the Presentation of the Theotokos in Portianou",
        "Ι. Ν. Εισοδίων Θεοτόκου Πορτιανού", "Portianou",
        "Πορτιανού 814 00", [], "eis.theotokou.portianou@gmail.com",
        [
            "Αγ. Βασιλείου",
            "Αγ. Σπυρίδωνος",
            "Αποτομής Τιμίας Κεφαλής Αγ. Ιωάννου Προδρόμου (Θέση Προφήτης Ηλίας)",
            "Προφήτου Ηλιού",
        ],
    ),
    (
        "78", "Parish Church of the Annunciation of the Theotokos in Moudros",
        "Ι. Ν. Ευαγγελισμού Θεοτόκου Μούδρου", "Moudros",
        "Μύρινα 814 00", ["22540-71975"],
        "evag.theotokou.moudrou@gmail.com",
        [
            "Αγ. Βαρβάρας Αυλώνος",
            "Αγ. Μαρίνης Αυλώνος",
            "Αγ. Ιωάννου Θεολόγου Καλυβίων",
            "Αγ. Παύλου",
            "Αγ. Πέτρου Φαναρακίου",
            "Αγ. Μηνά Χαβούλης",
            "Παμμεγίστων Ταξιαρχών",
        ],
    ),
    (
        "69", "Parish Church of the Dormition of the Theotokos in Kaminia",
        "Ι. Ν. Κοιμήσεως Θεοτόκου Καμινίων", "Kaminia",
        "Καμίνια 814 01", [], "koim.theotokou.kaminion@gmail.com", [],
    ),
    (
        "75", "Parish Church of the Dormition of the Theotokos in Kornos",
        "Ι. Ν. Κοιμήσεως Θεοτόκου Κορνού", "Kornos", "Κορνός 814 00", [],
        "koim.theotokou.kornou@gmail.com",
        [
            "Αγ. Αναργύρων",
            "Αγ. Αναργύρων Κάμπου",
            "Αγ. Ανδρέου",
            "Αγ. Μαρίνης Φράγματος",
            "Αγ. Κυριακής Ψύλλων",
            "Αγ. Παρασκευής",
            "Αγ. Σπυρίδωνος",
            "Αγ. Σώζοντος",
            "Γενεθλίου Θεοτόκου Κάμπου",
            "Προφήτου Ηλιού Θερμών",
            "Τιμίου Προδρόμου",
        ],
    ),
    (
        "58", "Parish Church of the Dormition of the Theotokos in Myrina",
        "Ι. Ν. Κοιμήσεως Θεοτόκου Μυρίνης", "Myrina", "Μύρινα 814 00",
        ["22540-23433"], "koim.theotokou.myrinas@gmail.com",
        [
            "Αγ. Αποστόλων Νοσοκομείου",
            "Αγ. Δημητρίου Κοιμητηρίου",
            "Αγ. Νικολάου Λιμένος",
            "Αγ. Φωτίδος",
            "Αγ. Χαραλάμπους Γηροκομείου",
            "Βραχνής Παναγιάς",
            "Κοιμήσεως Θεοτόκου (Καμένη Παναγιά)",
        ],
    ),
    (
        "91", "Parish Church of the Dormition of the Theotokos in Tsimandria",
        "Ι. Ν. Κοιμήσεως Θεοτόκου Τσιμανδρίων", "Tsimandria",
        "Τσιμάνδρια 814 00", [], "koim.theotokou.tsimandrion@gmail.com",
        [
            "Αγ. Ειρήνης Χρυσοβαλάντου",
            "Αγ. Θεοδώρου",
            "Αγ. Φωτεινής (Θέση Κόμπι)",
            "Αγ. Χαραλάμπους",
            "Γεννήσεως Χριστού",
        ],
    ),
]


# The source abbreviates the Greek titles. English display names expand the
# received dedication while the exact source string remains in local.
DEDICATIONS = {
    "Αποτομής Τιμίας Κεφαλής Αγ. Ιωάννου Προδρόμου":
        "the Beheading of Saint John the Forerunner",
    "Αγ. Οσιομάρτυρος Εφραίμ του Νέου":
        "the Venerable Martyr Ephraim the New",
    "Οσίου Αθανασίου του εν Άθω": "Venerable Athanasius of Athos",
    "Αγ. Αθανασίου Αθωνίτου": "Saint Athanasius the Athonite",
    "Αγ. Αναστασίας Φαρμακολυτρίας":
        "Saint Anastasia Pharmacolytria",
    "Αγ. Ειρήνης Χρυσοβαλάντου": "Saint Irene Chrysovalantou",
    "Αγ. Ελευθερίου και Χριστοφόρου":
        "Saints Eleftherios and Christopher",
    "Αγ. Ιακώβου του εν Ευβοία": "Saint James of Euboea",
    "Αγ. Ιωάννου Θεολόγου": "Saint John the Theologian",
    "Αγ. Ιωάννου Προδρόμου": "Saint John the Forerunner",
    "Αγ. Κηρύκου και Ιουλίττης": "Saints Cyricus and Julitta",
    "Αγ. Κωνσταντίνου και Ελένης": "Saints Constantine and Helen",
    "Αγ. Κυριακής και Σοφίας": "Saints Kyriaki and Sophia",
    "Αγ. Πέτρου και Παύλου": "Saints Peter and Paul",
    "Παμμεγίστου Ταξιάρχου Μιχαήλ": "Archangel Michael",
    "Προφήτου Ηλιού και Αγ. Δημητρίου":
        "Prophet Elijah and Saint Demetrius",
    "Παναγίας Πάντων Χαράς": "the Panagia, Joy of All",
    "Αγ. Αναργύρων": "the Holy Unmercenaries",
    "Αγ. Αποστόλων": "the Holy Apostles",
    "Αγ. Θεοδώρων": "the Holy Theodores",
    "Αγ. Τριάδος": "the Holy Trinity",
    "Αγ. Αθανασίου": "Saint Athanasius",
    "Αγ. Αικατερίνης": "Saint Catherine",
    "Αγ. Ανδρέου": "Saint Andrew",
    "Αγ. Αντωνίου": "Saint Anthony",
    "Αγ. Άννης": "Saint Anna",
    "Αγ. Βαρβάρας": "Saint Barbara",
    "Αγ. Βαβάρας": "Saint Barbara",
    "Αγ. Βασιλείου": "Saint Basil",
    "Αγ. Βλασίου": "Saint Blaise",
    "Αγ. Γεωργίου": "Saint George",
    "Αγ. Γρηγορίου": "Saint Gregory",
    "Αγ. Δημητρίου": "Saint Demetrius",
    "Αγ. Ειρήνης": "Saint Irene",
    "Αγ. Ελένης": "Saint Helen",
    "Αγ. Ερμολάου": "Saint Hermolaus",
    "Αγ. Ευστρατίου": "Saint Eustratios",
    "Αγ. Θεοδώρου": "Saint Theodore",
    "Αγ. Ιωάννου": "Saint John",
    "Αγ. Κλήμεντος": "Saint Clement",
    "Αγ. Κωνσταντίνου": "Saint Constantine",
    "Αγ. Κηρύκου": "Saint Cyricus",
    "Αγ. Κυριακής": "Saint Kyriaki",
    "Αγ. Λαζάρου": "Saint Lazarus",
    "Αγ. Μάμαντος": "Saint Mamas",
    "Αγ. Μαρίνης": "Saint Marina",
    "Αγ. Μαρίνου": "Saint Marinus",
    "Αγ. Μελιτινής": "Saint Melitini",
    "Αγ. Μηνά": "Saint Menas",
    "Αγ. Μοδέστου": "Saint Modestus",
    "Αγ. Νεκταρίου": "Saint Nektarios",
    "Αγ. Νικολάου": "Saint Nicholas",
    "Αγ. Ονουφρίου": "Saint Onuphrius",
    "Αγ. Παντελεήμονος": "Saint Panteleimon",
    "Αγ. Παρασκευής": "Saint Paraskevi",
    "Αγ. Παύλου": "Saint Paul",
    "Αγ. Παχωμίου": "Saint Pachomius",
    "Αγ. Πέτρου": "Saint Peter",
    "Αγ. Πολυκάρπου": "Saint Polycarp",
    "Αγ. Σοφίας": "Saint Sophia",
    "Αγ. Σπυρίδωνος": "Saint Spyridon",
    "Αγ. Στεφάνου": "Saint Stephen",
    "Αγ. Σώζοντος": "Saint Sozon",
    "Αγ. Τρύφωνος": "Saint Tryphon",
    "Αγ. Φανουρίου": "Saint Phanourios",
    "Αγ. Φιλοθέης": "Saint Philothei",
    "Αγ. Φωτεινής": "Saint Photini",
    "Αγ. Φωτίδος": "Saint Photida",
    "Αγ. Χαραλάμπους": "Saint Charalambos",
    "Αγ. Χριστοφόρου": "Saint Christopher",
    "Αναλήψεως Χριστού": "the Ascension of Christ",
    "Βραχνής Παναγιάς": "Panagia Vrachni",
    "Γενεθλίου Θεοτόκου": "the Nativity of the Theotokos",
    "Γεννήσεως Θεοτόκου": "the Nativity of the Theotokos",
    "Γεννήσεως Χριστού": "the Nativity of Christ",
    "Δεσπότου Χριστού": "Christ the Master",
    "Εισοδίων Θεοτόκου": "the Presentation of the Theotokos",
    "Ζωοδόχου Πηγής": "the Life-Giving Spring",
    "Κοιμήσεως Θεοτόκου": "the Dormition of the Theotokos",
    "Μεταμορφώσεως Σωτήρος": "the Transfiguration of the Savior",
    "Παμμεγίστων Ταξιαρχών": "the Holy Archangels",
    "Παναγίας Κακαβιωτίσσης": "Panagia Kakaviotissa",
    "Παναγίας Φανερωμένης": "Panagia Faneromeni",
    "Παναγίας Καματερής": "Panagia Kamateri",
    "Προφήτου Ηλιού": "Prophet Elijah",
    "Προφήτου Ζαχαρίου": "Prophet Zachariah",
    "Τιμίου Προδρόμου": "the Honorable Forerunner",
}

QUALIFIER_TERMS = {
    "Παλαιού Κοιμητηρίου": "Old Cemetery",
    "Παλαιού Λιμένος": "Old Harbor",
    "Πλησίον Στρατοπέδου": "Near Military Camp",
    "Προέκταση Παραλίας": "Beyond Beach",
    "Παραλία Αγίου Ιωάννου": "Saint John Beach",
    "Μνημειακός Ναός": "Monumental Church",
    "Αγ. Αλεξάνδρου": "Saint Alexander",
    "Προφήτης Ηλίας": "Prophet Elijah",
    "Κοιμητηρίου": "Cemetery",
    "Νοσοκομείου": "Hospital",
    "Γηροκομείου": "Nursing Home",
    "Στρατοπέδου": "Military Camp",
    "Οικισμού": "Settlement",
    "Παραλίας": "Beach",
    "Παραλία": "Beach",
    "Αγοράς": "Market",
    "Λιμένος": "Harbor",
    "Φράγματος": "Dam",
    "Είσοδος": "Entrance",
    "Ξενοδοχείο": "Hotel",
    "Θέση": "Site",
    "ο Μικρός": "the Small",
    "και": "and",
}

GREEK_TRANSLITERATION = {
    "Α": "A", "Β": "V", "Γ": "G", "Δ": "D", "Ε": "E",
    "Ζ": "Z", "Η": "I", "Θ": "Th", "Ι": "I", "Κ": "K",
    "Λ": "L", "Μ": "M", "Ν": "N", "Ξ": "X", "Ο": "O",
    "Π": "P", "Ρ": "R", "Σ": "S", "Τ": "T", "Υ": "U",
    "Φ": "F", "Χ": "Ch", "Ψ": "Ps", "Ω": "O",
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "u", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}


def transliterate(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn")
    return "".join(GREEK_TRANSLITERATION.get(char, char) for char in value)


def chapel_english(local):
    for greek in sorted(DEDICATIONS, key=len, reverse=True):
        if local == greek or local.startswith(greek + " ") or local.startswith(
                greek + " ("):
            qualifier = local[len(greek):].strip()
            qualifier = qualifier.replace("«", "").replace("»", "")
            qualifier = qualifier.replace("(", " ").replace(")", " ")
            for source, target in sorted(
                    QUALIFIER_TERMS.items(), key=lambda item: len(item[0]),
                    reverse=True):
                qualifier = re.sub(
                    r"(?<!\w)%s(?!\w)" % re.escape(source), target,
                    qualifier)
            qualifier = re.sub(
                r"\s+", " ", transliterate(qualifier)).strip().title()
            name = "Parish Chapel of %s" % DEDICATIONS[greek]
            if qualifier:
                name += " - %s" % qualifier
            return name
    raise ValueError("untranslated Lemnos chapel title: %s" % local)


PARISH_CHAPEL_COUNTS = {
    "57": 4,
    "65": 10,
    "60": 2,
    "63": 12,
    "67": 6,
    "68": 4,
    "71": 13,
    "83": 5,
    "86": 5,
    "73": 0,
    "74": 10,
    "77": 4,
    "62": 6,
    "82": 6,
    "85": 9,
    "87": 0,
    "89": 5,
    "92": 7,
    "76": 8,
    "79": 6,
    "72": 11,
    "90": 11,
    "59": 3,
    "81": 3,
    "66": 8,
    "70": 2,
    "61": 5,
    "80": 8,
    "93": 0,
    "88": 11,
    "64": 8,
    "84": 4,
    "78": 7,
    "69": 0,
    "75": 11,
    "58": 7,
    "91": 5,
}


def parish_row(entry):
    (page_id, name, local, seat, address, phones, email,
     unused_chapels) = entry
    profile = PARISH_PROFILE % page_id
    row = {
        "id": "gr-lemnos-parish-%s" % page_id,
        "parent": PARENT,
        "kind": "parish",
        "rank": "Metropolitan Church" if page_id == "57" else
                "Parish Church",
        "name": name,
        "local": local,
        "seat": seat,
        "country": "GR",
        "address": address,
        "emails": [email],
        "sources": [PARISH_ROSTER, profile],
        "contact_sources": [profile],
        "contact_checked": CHECKED,
        "checked": CHECKED,
    }
    if phones:
        row["phones"] = list(phones)
    return row


def chapel_row(page_id, index, seat, local):
    return {
        "id": "gr-lemnos-chapel-%s-%03d" % (page_id, index),
        "parent": "gr-lemnos-parish-%s" % page_id,
        "kind": "parish",
        "rank": "Parish Chapel",
        "name": chapel_english(local),
        "local": local,
        "seat": seat,
        "country": "GR",
        "sources": [PARISH_PROFILE % page_id],
        "checked": CHECKED,
    }


ROWS = []
for parish in PARISHES:
    page_id, unused_name, unused_local, seat = parish[:4]
    chapels = parish[7]
    ROWS.append(parish_row(parish))
    ROWS.extend(
        chapel_row(page_id, index, seat, local)
        for index, local in enumerate(chapels, 1)
    )

ROWS.append({
    "id": "gr-lemnos-pilgrimage-saint-sozon",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Pilgrimage Church",
    "name": "Holy Pilgrimage of Saint Sozon",
    "local": "Ιερό Προσκύνημα Αγίου Σώζοντος",
    "seat": "Fisini",
    "country": "GR",
    "address": "814 01 Φυσίνη",
    "sources": [PILGRIMAGE],
    "checked": CHECKED,
})

ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_COUNT = 264
EXPECTED_RANKS = {
    "Metropolitan Church": 1,
    "Parish Chapel": 226,
    "Parish Church": 36,
    "Pilgrimage Church": 1,
}
EXPECTED_KINDS = {"parish": EXPECTED_COUNT}
EXPECTED_ADDRESS_BODIES = 38
EXPECTED_CONTACT_BODIES = 37
EXPECTED_PHONE_BODIES = 5
EXPECTED_EMAIL_BODIES = 37
EXPECTED_SITE_BODIES = 0
EXPECTED_PARENT_COUNTS = {PARENT: 38}
EXPECTED_PARENT_COUNTS.update({
    "gr-lemnos-parish-%s" % page_id: count
    for page_id, count in PARISH_CHAPEL_COUNTS.items() if count
})

ALLOWED_KINDS = set(EXPECTED_KINDS)
ALLOWED_RANKS = set(EXPECTED_RANKS)
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2018\u2019\u201c\u201d\ufffd]")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
GREEK_RE = re.compile(r"[\u0370-\u03ff]")


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
        if urlparse(source_url).netloc not in {
                "www.imlimnou.gr", "imlimnou.gr", "ec-patr.org"}:
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
                raise ValueError(
                    "%s has contact provenance outside its sources" %
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
            ledger.get("parent") != PARENT or
            ledger.get("checked") != CHECKED):
        raise ValueError("Lemnos candidate ledger metadata drifted")
    if ledger.get("higher_level_site") != PARENT_SITE:
        raise ValueError("Lemnos higher-level site record drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        "principal_parishes": 37,
        "named_parish_chapels": 226,
        "pilgrimage_churches": 1,
        "total": EXPECTED_COUNT,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Lemnos candidate ledger %s drifted" % key)
    candidate_ids = {
        item.get("candidate_id") for item in ledger.get("candidates") or []
    }
    if candidate_ids != {
            "gr-lemnos-aggregate-country-chapels",
            "gr-lemnos-moudros-address",
            "gr-lemnos-pilgrimage-contact",
            "gr-lemnos-search-and-map-leads"}:
        raise ValueError("Lemnos candidate holdings drifted")
    return ledger


def build():
    validate_url(PARENT_SITE, "Lemnos higher-level site")
    parish_ids = {item[0] for item in PARISHES}
    if len(PARISHES) != 37 or parish_ids != set(PARISH_CHAPEL_COUNTS):
        raise ValueError("Lemnos principal parish roster drifted")
    actual_chapel_counts = {
        item[0]: len(item[7]) for item in PARISHES
    }
    if actual_chapel_counts != PARISH_CHAPEL_COUNTS:
        raise ValueError("Lemnos named parish chapel counts drifted")
    if sum(actual_chapel_counts.values()) != 226:
        raise ValueError("Lemnos named parish chapel total drifted")

    result = []
    ids = set()
    seen = {PARENT}
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
        if not row.get("name") or not row.get("local") or not row.get("seat"):
            raise ValueError("%s lacks its name, local name, or seat" % row_id)
        if GREEK_RE.search(row["name"]):
            raise ValueError("%s lacks a complete English name" % row_id)
        if not GREEK_RE.search(row["local"]):
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
            if digits.startswith("69"):
                raise ValueError("%s carries an excluded clergy mobile" % row_id)
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
    if set(ENGLISH_NAMES) != ids or any(
            ENGLISH_NAMES[row["id"]] != row["name"] for row in result):
        raise ValueError("Lemnos English name coverage drifted")
    seats = {row["seat"] for row in result if row.get("seat")}
    if set(ENGLISH_SEATS) != seats or any(
            ENGLISH_SEATS[seat] != seat for seat in seats):
        raise ValueError("Lemnos English seat coverage drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Lemnos rank counts drifted: %r" % rank_counts)
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Lemnos kind counts drifted: %r" % kind_counts)
    if dict(sorted(parent_counts.items())) != dict(
            sorted(EXPECTED_PARENT_COUNTS.items())):
        raise ValueError("Lemnos parent counts drifted: %r" % parent_counts)

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
        raise ValueError("Lemnos contact coverage drifted")
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
            "Lemnos: %d officially named bodies; 37 principal parishes, "
            "226 parish chapels, and 1 pilgrimage church; %d carry "
            "current official institutional contact data" %
            (EXPECTED_COUNT, EXPECTED_CONTACT_BODIES)
        )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
