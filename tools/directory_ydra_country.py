#!/usr/bin/env python3
"""Validate the current exact Ydra, Spetsai, and Aigina roster.

This module stays independent of the shared directory aggregator until its
jurisdictional tranche is integrated.

    python tools/directory_ydra_country.py --check
    python tools/directory_ydra_country.py --check-live
    python tools/directory_ydra_country.py --dump
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
from urllib.parse import quote, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-ydra"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "ydra_country.json"
)

SOURCE_URLS = {
    "legal": "https://api.et.gr/apiFEK/2/2019/1513/pdf",
    "profile": (
        "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
        "metropoleis/ydras-spetson-kai-aigines"
    ),
    "admin": "https://imhydra.gr/dioikitiko-prosopiko",
    "districts": "https://imhydra.gr/arxieratikes-epitropies",
    "visitor": "https://imhydra.gr/plirofories-gia-ton-episkepti",
    "nectarius": "https://imhydra.gr/agios-nektarios",
    "palaiochora": (
        "https://imhydra.gr/"
        "mesaioniki-kastropolitia-palaia-chora-aigina"
    ),
    "hydra": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "MONES_YDRAS_GR-1.pdf"
    ),
    "methana": (
        "https://imhydra.gr/wp-content/uploads/2021/03/"
        "2021_ΙΣΤΟΣΕΛΙΔΑ_ΑΡΧΙΕΡΑΤΙΚΗ-ΕΠΙΤΡΟΠΕΙΑ-ΜΕΘΑΝΩΝ_1.pdf"
    ),
    "aig_synaxis": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΝΟΡΙΑ-ΑΙΓΙΝΙΤΩΝ-ΑΓΙΩΝ-2013.pdf"
    ),
    "pacheia": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "Ενορία-Παχειάς-Ράχης-Αίγινας.pdf"
    ),
    "aig_cathedral": (
        "https://imhydra.gr/wp-content/uploads/2021/04/Μητροπολη.pdf"
    ),
    "erm_arch": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΡΜΙΟΝΗ-Ι.Ν.-ΤΑΞΙΑΡΧΩΝ-_ΙΣΤΟΡΙΚΟ-ΕΝΟΡΙΑΚΟΥ-ΝΑΟΥ-"
        "ΠΑΜΜ.-ΤΑΞΙΑΡΧΩΝ-ΕΡΜΙΟΝΗΣ.pdf"
    ),
    "erm_dorm": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΡΜΙΟΝΗ_ΕΝΟΡΙΑΚΟΣ-ΝΑΟΣ-ΚΟΙΜΗΣΕΩΣ-ΘΕΟΤΟΚΟΥ.pdf"
    ),
    "thermisia": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΡΜΙΟΝΗ_ΕΝΟΡΙΑ-Ι.Ν.-ΕΥΑΓΓΕΛΙΣΜΟΥ-ΤΗΣ-ΘΕΟΤΟΚΟΥ-"
        "ΘΕΡΜΗΣΙΑΣ.pdf"
    ),
    "erm_mon": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΡΜΙΟΝΗ_Ι.Μ.-ΑΓΙΩΝ-ΑΝΑΡΓΥΡΩΝ.pdf"
    ),
    "iliokastro": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΡΜΙΟΝΗ_Ι.Ν.-ΑΓΙΩΝ-ΑΠΟΣΤΟΛΩΝ-ΗΛΙΟΚΑΣΤΡΟΥ.pdf"
    ),
    "poros_church": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΑΓ-ΓΕΩΡΓΙΟΣ-Copy.pdf"
    ),
    "skapeti": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΝΟΡΙΑ-ΕΥΑΓΓΕΛΙΣΜΟΥ-ΘΕΟΤΟΚΟΥ-ΣΚΑΠΕΤΙΟΥ-Νεο.pdf"
    ),
    "taktik": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΕΝΟΡΙΑ-ΙΕΡΟΥ-ΝΑΟΥ-ΖΩΟΔΟΧΟΥ-ΠΗΓΗΣ-"
        "ΤΑΚΤΙΚΟΥΠΟΛΕΩΣ-ΤΡΟΙΖΗΝΙΑΣ.pdf"
    ),
    "poros_mon": (
        "https://imhydra.gr/wp-content/uploads/2021/04/"
        "ΙΜΖΩΟΔΟΧΟΥ-ΠΗΓΗΣ-ΙΣΤΟΡΙΚΟ_2020.pdf"
    ),
    "kranidi_all": (
        "https://imhydra.gr/wp-content/uploads/2022/02/"
        "ΑΡΧΙΕΡΑΤΙΚΗ-ΕΠΙΤΡΟΠΕΙΑ-ΚΡΑΝΙΔΙΟΥ.pdf"
    ),
    "kato": (
        "https://imhydra.gr/wp-content/uploads/2021/06/"
        "Ξωκλήσια-Κάτω-Παναγία_Κρανίδι-1.pdf"
    ),
    "pano": (
        "https://imhydra.gr/wp-content/uploads/2021/06/"
        "Ξωκλήσια-Πάνω-Παναγία_Κρανίδι.pdf"
    ),
    "imna": "https://imna.gr/",
    "prodromos": "https://prodromos-kranidiou.gr/",
}

# key | parent key | kind | rank | English name | Greek source name | seat |
# address parts | phones | faxes | emails | direct body site |
# identity source keys | contact source keys
CORE_SOURCE = r'''
parish-hydra-dormition||parish|Cathedral|Cathedral of the Dormition of the Theotokos in Hydra|Ιερός Καθεδρικός Ναός Κοιμήσεως της Θεοτόκου Ύδρας|Hydra|Ύδρα;18040;Greece|2298054071||||legal,hydra|hydra
parish-hydra-barbara||parish|Parish Church|Parish Church of Saint Barbara in Hydra|Ενορία Αγίας Βαρβάρας Ύδρας|Hydra|Ύδρα;Greece|||||legal,admin|
parish-hydra-demetrius||parish|Parish Church|Parish Church of Saint Demetrius in Hydra|Ενορία Αγίου Δημητρίου Ύδρας|Hydra|Ύδρα;Greece|||||legal,admin|
parish-hydra-meeting||parish|Parish Church|Parish Church of the Meeting of Christ in Hydra|Ιερός Ιστορικός Ενοριακός Ναός Υπαπαντής του Χριστού Ύδρας|Hydra|Ύδρα;18040;Greece|2298052553,2298052207 ext. 2||ipapanti.hydra@gmail.com||legal,hydra|hydra
parish-hydra-forerunner||parish|Parish Church|Parish Church of Saint John the Forerunner in Hydra|Ενορία Τιμίου Προδρόμου Ύδρας|Hydra|Ύδρα;Greece|||||legal,admin|
parish-spetses-nicholas||parish|Parish Church|Parish Church of Saint Nicholas in Spetses|Ενορία Αγίου Νικολάου Σπετσών|Spetses|Σπέτσες;Greece|||||legal,admin|
parish-spetses-anthony||parish|Parish Church|Parish Church of Saint Anthony in Spetses|Ενορία Αγίου Αντωνίου Σπετσών|Spetses|Σπέτσες;Greece|||||legal,admin|
parish-spetses-ascension||parish|Parish Church|Parish Church of the Ascension of Christ in Spetses|Ενορία Αναλήψεως Χριστού Σπετσών|Spetses|Σπέτσες;Greece|||||legal,admin|
parish-spetses-forerunner||parish|Parish Church|Parish Church of Saint John the Forerunner in Spetses|Ενορία Τιμίου Προδρόμου Σπετσών|Spetses|Σπέτσες;Greece|||||legal,admin|
parish-ermioni-archangels||parish|Parish Church|Parish Church of the Holy Archangels in Ermioni|Ενοριακός Ναός Παμμεγίστων Ταξιαρχών Ερμιόνης|Ermioni|Ερμιόνη;21051;Greece|||||legal,erm_arch|
parish-ermioni-dormition||parish|Parish Church|Parish Church of the Dormition of the Theotokos in Ermioni|Ενοριακός Ναός Κοιμήσεως της Θεοτόκου Ερμιόνης|Ermioni|Ερμιόνη;21051;Greece|2754031045,2754031924,6972664449||pdampe@gmail.com||legal,erm_dorm|erm_dorm
parish-thermisia-annunciation||parish|Parish Church|Parish Church of the Annunciation of the Theotokos in Thermisia|Ενορία Ευαγγελισμού της Θεοτόκου Θερμησίας|Thermisia|Ερμιόνη Αργολίδας;21051;Greece|2754031839,6976133826||p.dauid@gmail.com||legal,thermisia|thermisia
parish-kranidi-forerunner||parish|Metropolitan Church|Metropolitan Church of Saint John the Forerunner in Kranidi|Ιερός Μητροπολιτικός Ναός Τιμίου Προδρόμου Κρανιδίου|Kranidi|Μητροπόλεως 1;21300 Κρανίδι;Greece|2754022049,6975464287|2754400773|pchristoforos2@gmail.com|https://prodromos-kranidiou.gr/|legal,kranidi_all,prodromos|kranidi_all,prodromos
parish-kranidi-entrance||parish|Parish Church|Parish Church of the Entrance of the Theotokos in Kranidi|Ενορία Ιερού Ναού Εισοδίων Θεοτόκου Κάτω Παναγία Κρανιδίου|Kranidi|Κρανίδι Αργολίδας;21300;Greece|2754021204|2754022512|||legal,kato|kato
parish-kranidi-transfiguration||parish|Parish Church|Parish Church of the Transfiguration of the Savior in Kranidi|Ενορία Μεταμορφώσεως του Σωτήρος Κρανιδίου|Kranidi|Κρανίδι;Greece|||||legal,admin|
parish-kranidi-synaxis||parish|Parish Church|Parish Church of the Synaxis of the Theotokos in Kranidi|Ενορία Ιερού Ναού Συνάξεως Θεοτόκου Πάνω Παναγία Κρανιδίου|Kranidi|Κρανίδι Αργολίδας;21300;Greece|2754021922,2754022421||||legal,pano|pano
parish-koilada-annunciation||parish|Parish Church|Parish Church of the Annunciation of the Theotokos in Koilada|Ενορία Ευαγγελισμού της Θεοτόκου Κοιλάδας|Koilada|Κοιλάδα;Greece|||||legal,admin|
parish-porto-cheli-annunciation||parish|Parish Church|Parish Church of the Annunciation of the Theotokos in Porto Cheli|Ενορία Ευαγγελισμού της Θεοτόκου Πορτοχελίου|Porto Cheli|Πόρτο Χέλι;Greece|||||legal,admin|
parish-didyma-nicholas||parish|Parish Church|Parish Church of Saint Nicholas in Didyma|Ενορία Αγίου Νικολάου Διδύμων|Didyma|Δίδυμα;Greece|||||legal,admin|
parish-fournoi-archangels||parish|Parish Church|Parish Church of the Holy Archangels in Fournoi|Ενορία Παμμεγίστων Ταξιαρχών Φούρνων|Fournoi|Φούρνοι;Greece|||||legal,admin|
parish-iliokastro-apostles||parish|Parish Church|Parish Church of the Holy Apostles in Iliokastro|Ενορία Αγίων Αποστόλων Ηλιοκάστρου|Iliokastro|Ηλιόκαστρο;Greece|2754021841||||legal,iliokastro|iliokastro
parish-poros-annunciation||parish|Parish Church|Parish Church of the Annunciation of the Theotokos in Poros|Ενορία Ευαγγελισμού της Θεοτόκου Πόρου|Poros|Πόρος;Greece|||||legal,admin|
parish-poros-george||parish|Metropolitan Church|Metropolitan Church of Saint George in Poros|Ιερός Μητροπολιτικός Ναός Αγίου Γεωργίου Πόρου|Poros|Πόρος;Greece|||||legal,poros_church|
parish-poros-constantine-helen||parish|Parish Church|Parish Church of Saints Constantine and Helen in Poros|Ενορία Αγίων Κωνσταντίνου και Ελένης Πόρου|Poros|Πόρος;Greece|||||legal,admin|
parish-galatas-nicholas||parish|Parish Church|Parish Church of Saint Nicholas in Galatas|Ενορία Αγίου Νικολάου Γαλατά|Galatas|Γαλατάς;Greece|||||legal,admin|
parish-galatas-anna||parish|Parish Church|Parish Church of Saint Anna in Galatas|Ενορία Αγίας Άννας Γαλατά|Galatas|Γαλατάς;Greece|||||legal,admin|
parish-troizina-chrysostom||parish|Parish Church|Parish Church of Saint John Chrysostom in Troizina|Ενορία Αγίου Ιωάννου του Χρυσοστόμου Τροιζήνας|Troizina|Τροιζήνα;Greece|||||legal,admin|
parish-skapeti-annunciation||parish|Parish Church|Parish Church of the Annunciation of the Theotokos in Skapeti|Ενορία Ευαγγελισμού της Θεοτόκου Σκαπετίου|Skapeti|Σκαπέτι Τροιζηνίας;Greece|6948618826||pgegal@gmail.com||legal,skapeti|skapeti
parish-taktikoupolis-life-giving-spring||parish|Parish Church|Parish Church of the Life-Giving Spring in Taktikoupolis|Ενορία Ιερού Ναού Ζωοδόχου Πηγής Τακτικουπόλεως Τροιζηνίας|Taktikoupolis|Τακτικούπολη Τροιζηνίας;18020;Greece|2298036036,2298036056,6977946677||||legal,taktik|taktik
parish-ano-fanari-athanasius||parish|Parish Church|Parish Church of Saint Athanasius in Ano Fanari|Ενορία Αγίου Αθανασίου Άνω Φαναρίου|Ano Fanari|Άνω Φανάρι;Greece|||||legal,admin|
parish-kato-fanari-charalambos||parish|Parish Church|Parish Church of Saint Charalambos in Kato Fanari|Ενορία Αγίου Χαραλάμπους Κάτω Φαναρίου|Kato Fanari|Κάτω Φανάρι;Greece|||||legal,admin|
parish-tracheia-athanasius||parish|Parish Church|Parish Church of Saint Athanasius in Tracheia|Ενορία Αγίου Αθανασίου Τραχειάς|Tracheia|Τραχειά;Greece|||||legal,admin|
parish-methana-trinity||parish|Metropolitan Church|Metropolitan Church of the Holy Trinity in Methana|Ενορία Μητροπολιτικού Ναού Αγίας Τριάδος Μεθάνων|Methana|Λουτρόπολη Μεθάνων;18030;Greece|2298092180,6973354967||arxieratiame8anon@gmail.com||legal,methana|methana
parish-megalochori-meeting||parish|Parish Church|Parish Church of the Meeting of Christ in Megalochori, Methana|Ενορία Ιερού Ναού Υπαπαντής Χριστού Μεγαλοχωρίου Μεθάνων|Megalochori|Βαθύ Μεγαλοχωρίου Μεθάνων;18030;Greece|6977354340||||legal,methana|methana
parish-kounoupitsa-entrance||parish|Parish Church|Parish Church of the Entrance of the Theotokos in Kounoupitsa, Methana|Ενορία Ιερού Ναού Εισοδίων Θεοτόκου Κουνουπίτσας Μεθάνων|Kounoupitsa|Κουνουπίτσα Μεθάνων;18030;Greece|2298092085,6978998580||||legal,methana|methana
parish-kypseli-anthony||parish|Parish Church|Parish Church of Saint Anthony in Kypseli, Methana|Ενορία Ιερού Ναού Αγίου Αντωνίου Κυψέλης Μεθάνων|Kypseli, Methana|Κυψέλη Μεθάνων;Greece|2298092180,6973354967||arxieratiame8anon@gmail.com||legal,methana|methana
parish-palaia-loutra-dormition||parish|Parish Church|Parish Church of the Dormition of the Theotokos in Palaia Loutra, Methana|Ενορία Ιερού Ναού Κοιμήσεως Θεοτόκου Παλαιών Λουτρών Μεθάνων|Palaia Loutra|Παλαιά Λουτρά Μεθάνων;Greece|2298092085,6978998580||||legal,methana|methana
parish-aegina-dormition||parish|Metropolitan Church|Metropolitan Church of the Dormition of the Theotokos and Saint Dionysius in Aegina|Ιερός Μητροπολιτικός Ναός Κοιμήσεως της Θεοτόκου και Αγίου Διονυσίου Αιγίνης|Aegina|Μητροπόλεως;18010 Αίγινα;Greece|2297022654||emgiann@gmail.com|https://imna.gr/|legal,aig_cathedral,imna|imna
parish-aegina-nicholas||parish|Parish Church|Parish Church of Saint Nicholas in Aegina|Ενορία Αγίου Νικολάου Αιγίνης|Aegina|Αίγινα;Greece|||||legal,admin|
parish-aegina-entrance||parish|Parish Church|Parish Church of the Entrance of the Theotokos in Aegina|Ενορία Εισοδίων της Θεοτόκου Αιγίνης|Aegina|Αίγινα;Greece|||||legal,admin|
parish-aegina-synaxis||parish|Parish Church|Parish Church of the Synaxis of the Saints of Aegina|Ενορία Συνάξεως των Αιγινητών Αγίων|Livadi, Aegina|Λιβάδι Αίγινας;Greece|||||legal,aig_synaxis|
parish-asomatoi-archangels||parish|Parish Church|Parish Church of the Holy Archangels in Asomatoi, Aegina|Ενορία Παμμεγίστων Ταξιαρχών Ασωμάτων Αιγίνης|Asomatoi, Aegina|Ασώματοι Αίγινας;Greece|||||legal,admin|
parish-kypseli-aegina-annunciation||parish|Parish Church|Parish Church of the Annunciation of the Theotokos in Kypseli, Aegina|Ενορία Ευαγγελισμού της Θεοτόκου Κυψέλης Αιγίνης|Kypseli, Aegina|Κυψέλη Αίγινας;Greece|||||legal,admin|
parish-perdika-dormition||parish|Parish Church|Parish Church of the Dormition of the Theotokos in Perdika|Ενορία Κοιμήσεως της Θεοτόκου Πέρδικας|Perdika, Aegina|Πέρδικα Αίγινας;Greece|||||legal,admin|
parish-mesagros-dormition||parish|Parish Church|Parish Church of the Dormition of the Theotokos in Mesagros|Ενορία Κοιμήσεως της Θεοτόκου Μεσαγρού|Mesagros, Aegina|Μεσαγρός Αίγινας;Greece|||||legal,admin|
parish-pacheia-rachi||parish|Parish Church|Parish Church of the Holy Archangels and Saint Dionysius in Pacheia Rachi|Ενορία Παμμεγίστων Ταξιαρχών Αγίου Διονυσίου Παχειάς Ράχης Αίγινας|Pacheia Rachi, Aegina|Παχειά Ράχη Αίγινας;Greece|||||legal,pacheia|
parish-vathy-trinity||parish|Parish Church|Parish Church of the Holy Trinity in Vathy, Aegina|Ενορία Αγίας Τριάδος Βαθέος Αιγίνης|Vathy, Aegina|Βαθύ Αίγινας;Greece|||||legal,admin|
parish-agia-marina-transfiguration||parish|Parish Church|Parish Church of the Transfiguration of the Savior in Agia Marina, Aegina|Ενορία Μεταμορφώσεως του Σωτήρος Αγίας Μαρίνας Αιγίνης|Agia Marina, Aegina|Αγία Μαρίνα Αίγινας;Greece|||||legal,admin|
parish-agioi-crispus||parish|Parish Church|Parish Church of Apostle Crispus in Agioi, Aegina|Ενορία Αποστόλου Κρίσπου Αγίων Αιγίνης|Agioi, Aegina|Άγιοι Αίγινας;Greece|||||legal,admin|
parish-marathonas-barbara||parish|Parish Church|Parish Church of Saint Barbara in Marathonas, Aegina|Ενορία Αγίας Βαρβάρας Μαραθώνα Αιγίνης|Marathonas, Aegina|Μαραθώνας Αίγινας;Greece|||||legal,admin|
parish-anitsaion-dormition||parish|Parish Church|Parish Church of the Dormition of the Theotokos in Anitsaion|Ενορία Κοιμήσεως της Θεοτόκου Ανιτσαίου|Anitsaion, Aegina|Ανιτσαίο Αίγινας;Greece|||||legal,admin|
parish-agistri-life-giving-spring||parish|Parish Church|Parish Church of the Life-Giving Spring in Agistri|Ενορία Ζωοδόχου Πηγής Αγκιστρίου|Agistri|Αγκίστρι;Greece|||||legal,admin|
pilgrimage-aegina-myrtidiotissa||parish|Pilgrimage Church|Pilgrimage Church of Panagia Myrtidiotissa in Aegina|Ιερό Προσκύνημα Παναγίας Μυρτιδιώτισσας Αιγίνης|Aegina|Αίγινα;Greece|||||legal|
monastery-poros-life-giving-spring||monastery|Monastery|Monastery of the Life-Giving Spring of Kalavria in Poros|Ιερά Μονή Ζωοδόχου Πηγής Καλαυρίας Πόρου|Poros|Πόρος;Greece|2298022926||||profile,poros_mon|profile
monastery-hydra-prophet-elijah||monastery|Monastery|Monastery of Prophet Elijah in Hydra|Ιερά Μονή Προφήτου Ηλιού Ύδρας|Hydra|Ύδρα;Greece|2298052540||||profile,hydra|profile,hydra
monastic-house-hydra-trinity||monastery|Monastic House|Monastic House of Patristic Ministry of the Holy Trinity in Hydra|Μοναστικός Οίκος Πατερικής Διακονίας Αγίας Τριάδος Ύδρας|Hydra|Ύδρα;Greece|2298052553||||profile,hydra|profile,hydra
monastery-aegina-chrysoleontissa||monastery|Monastery|Monastery of the Dormition of the Theotokos Chrysoleontissa in Aegina|Ιερά Μονή Κοιμήσεως Θεοτόκου Χρυσολεοντίσσης Αιγίνης|Aegina|Αίγινα;Greece|2297062100||||profile|profile
monastery-ermioni-unmercenaries||monastery|Monastery|Monastery of the Holy Unmercenaries in Ermioni|Ιερά Μονή Αγίων Αναργύρων Ερμιόνης|Ermioni|Ερμιόνη;Greece|2754031280||||profile,erm_mon|profile,erm_mon
monastery-spetses-all-saints||monastery|Monastery|Monastery of All Saints in Spetses|Ιερά Μονή Αγίων Πάντων Σπετσών|Spetses|Σπέτσες;Greece|2298072300||||profile|profile
monastery-hydra-eupraxia||monastery|Monastery|Monastery of Saint Eupraxia of Dokos in Hydra|Ιερά Μονή Αγίας Ευπραξίας Δοκού Ύδρας|Hydra|Ύδρα;Greece|2298052484||||profile,hydra|profile,hydra
monastery-hydra-nativity-zourva||monastery|Monastery|Monastery of the Nativity of the Theotokos of Zourva in Hydra|Ιερά Μονή Γενεσίου Θεοτόκου Ζούρβας Ύδρας|Hydra|Ζούρβα Ύδρας;Greece|2298052344||||profile,hydra|profile,hydra
monastery-hydra-matrona||monastery|Monastery|Monastery of Saint Matrona in Hydra|Ιερά Μονή Αγίας Ματρώνας Ύδρας|Hydra|Ύδρα;Greece|2298052552||||profile,hydra|profile,hydra
monastery-hydra-nicholas||monastery|Monastery|Monastery of Saint Nicholas in Hydra|Ιερά Μονή Αγίου Νικολάου Ύδρας|Hydra|Ύδρα;Greece|2298052551||||profile,hydra|profile,hydra
monastery-aegina-eleftherotria||monastery|Monastery|Monastery of Panagia Eleftherotria in Aegina|Ιερά Μονή Παναγίας Ελευθερώτριας Αιγίνης|Aegina|Αίγινα;Greece|2297052182||||profile|profile
hermitage-troizina-kecharitomene||monastery|Hermitage|Hermitage of the Kecharitomene Theotokos in Troizina|Ιερό Ησυχαστήριο Κεχαριτωμένης Θεοτόκου Τροιζήνας|Troizina|Τροιζήνα;Greece|2298035320||||profile|profile
hermitage-aegina-trinity-nectarius||monastery|Hermitage|Hermitage of the Holy Trinity and Saint Nectarius in Aegina|Ιερό Ησυχαστήριο Αγίας Τριάδος και Αγίου Νεκταρίου Αιγίνης|Aegina|Ιερά Μονή Αγίου Νεκταρίου Αγίας Τριάδος;18010 Αίγινα;Greece|2297053800||||profile|profile
hermitage-aegina-catherine||monastery|Hermitage|Hermitage of Saint Catherine in Aegina|Ιερό Ησυχαστήριο Αγίας Αικατερίνης Αιγίνης|Aegina|Αίγινα;Greece|2297053813||||profile|profile
hermitage-aegina-menas||monastery|Hermitage|Hermitage of Saint Menas in Aegina|Ιερό Ησυχαστήριο Αγίου Μηνά Αιγίνης|Aegina|Αίγινα;Greece|||||profile|
hermitage-aegina-nativity-christopher||monastery|Hermitage|Hermitage of the Nativity of the Theotokos and Saint Christopher in Aegina|Ιερό Ησυχαστήριο Γεννήσεως Θεοτόκου και Αγίου Χριστοφόρου Αιγίνης|Aegina|Αίγινα;Greece|2297022292||||profile|profile
hermitage-aegina-anastasia||monastery|Hermitage|Hermitage of Saint Anastasia Pharmacolytria in Aegina|Ιερό Ησυχαστήριο Αγίας Αναστασίας Φαρμακολυτρίας Αιγίνης|Aegina|Αίγινα;Greece|2297022080||||profile|profile
hermitage-hydra-photini-elizabeth||monastery|Hermitage|Hermitage of Saints Photini and Elizabeth in Hydra|Ιερό Ησυχαστήριο Αγίων Φωτεινής και Ελισάβετ Ύδρας|Hydra|Ύδρα;Greece|2298052209||||profile,hydra|profile,hydra
hermitage-kranidi-pantanassa||monastery|Hermitage|Hermitage of Panagia Pantanassa in Kranidi|Ιερό Ησυχαστήριο Παναγίας Παντανάσσης Κρανιδίου|Kranidi|Κρανίδι;Greece|2754021426||||profile|profile
hermitage-kranidi-anna||monastery|Hermitage|Hermitage of Saint Anna in Kranidi|Ιερό Ησυχαστήριο Αγίας Άννης Κρανιδίου|Kranidi|Λόφος Αγίας Άννας Κρανιδίου;Greece|2754021450||||profile,kato|profile
hermitage-souvala-demetrius||monastery|Hermitage|Hermitage of Saint Demetrius in Souvala, Aegina|Ιερό Ησυχαστήριο Αγίου Δημητρίου Σουβάλας Αιγίνης|Souvala, Aegina|Σουβάλα Αίγινας;Greece|||||profile|
'''

HYDRA_METHANA_SOURCE = r'''
chapel-hydra-nativity|parish-hydra-meeting|parish|Parish Chapel|Parish Chapel of the Nativity of Christ in Hydra|Ιερός Ναός Γεννήσεως του Χριστού Οικονόμου Ύδρας|Hydra|Ύδρα;Greece|||||hydra|
chapel-hydra-all-saints|parish-hydra-meeting|parish|Parish Chapel|Parish Chapel of All Saints in Hydra|Ιερός Ναός Αγίων Πάντων Ύδρας|Hydra|Ύδρα;Greece|||||hydra|
church-hydra-constantine||parish|Church|Church of New Martyr Saint Constantine of Hydra|Ιερός Ναός Νεομάρτυρος Αγίου Κωνσταντίνου του Υδραίου|Hydra|Κιάφα Ύδρας;Greece|2298052829||||hydra|hydra
chapel-methana-charalambos|parish-methana-trinity|parish|Parish Chapel|Parish Chapel of Saint Charalambos in Vromolimni, Methana|Ιερός πρώην Μητροπολιτικός Ναός Αγίου Χαραλάμπους Βρωμολίμνης Μεθάνων|Vromolimni, Methana|Βρωμολίμνη Μεθάνων;Greece|||||methana|
chapel-methana-unmercenaries|parish-methana-trinity|parish|Parish Chapel|Parish Chapel of the Holy Unmercenaries in Loutra, Methana|Ιερός Ναός Αγίων Αναργύρων Λουτροπόλεως Μεθάνων|Loutra, Methana|Λουτρόπολη Μεθάνων;Greece|||||methana|
chapel-methana-paraskevi|parish-methana-trinity|parish|Parish Chapel|Parish Chapel of Saint Paraskevi in Loutra, Methana|Ιερός Ναός Αγίας Παρασκευής Λουτροπόλεως Μεθάνων|Loutra, Methana|Λουτρόπολη Μεθάνων;Greece|||||methana|
chapel-methana-nicholas|parish-methana-trinity|parish|Parish Chapel|Parish Chapel of Saint Nicholas in Loutra, Methana|Ιερός Ναός Αγίου Νικολάου Λουτροπόλεως Μεθάνων|Loutra, Methana|Λουτρόπολη Μεθάνων;Greece|||||methana|
cemetery-methana-george|parish-methana-trinity|parish|Cemetery Church|Cemetery Church of Saint George in Dritsaika, Methana|Ιερός Ναός Αγίου Γεωργίου Κοιμητηριακός Δριτσαΐκων Μεθάνων|Dritsaika, Methana|Δριτσαΐκα Μεθάνων;Greece|||||methana|
chapel-methana-maura|parish-methana-trinity|parish|Parish Chapel|Parish Chapel of Saint Maura in Dritsaika, Methana|Ιερός Ναός Αγίας Μαύρας Δριτσαΐκων Μεθάνων|Dritsaika, Methana|Δριτσαΐκα Μεθάνων;Greece|||||methana|
country-methana-constantine-helen|parish-methana-trinity|parish|Country Church|Country Church of Saints Constantine and Helen in Loutra, Methana|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Λουτροπόλεως Μεθάνων|Loutra, Methana|Λουτρόπολη Μεθάνων;Greece|||||methana|
country-methana-panteleimon|parish-methana-trinity|parish|Country Church|Country Church of Saint Panteleimon in Dritsaika, Methana|Ιερός Ναός Αγίου Παντελεήμονος Δριτσαΐκων Μεθάνων|Dritsaika, Methana|Δριτσαΐκα Μεθάνων;Greece|||||methana|
chapel-kypseli-entrance-hodegetria|parish-kypseli-anthony|parish|Parish Chapel|Parish Chapel of the Entrance of the Theotokos and Panagia Hodegetria in Kypseli, Methana|Ιερός Ναός Εισοδίων της Θεοτόκου και Παναγίας Οδηγήτριας Κυψέλης Μεθάνων|Kypseli, Methana|Κυψέλη Μεθάνων;Greece|||||methana|
chapel-kypseli-archangels|parish-kypseli-anthony|parish|Parish Chapel|Parish Chapel of the Holy Archangels in Kypseli, Methana|Ιερός Ναός Ταξιαρχών Κυψέλης Μεθάνων|Kypseli, Methana|Κυψέλη Μεθάνων;Greece|||||methana|
cemetery-kypseli-forerunner|parish-kypseli-anthony|parish|Cemetery Church|Cemetery Church of Saint John the Forerunner in Kypseli, Methana|Ιερός Ναός Αγίου Ιωάννου Προδρόμου Κοιμητηριακός Κυψέλης Μεθάνων|Kypseli, Methana|Κυψέλη Μεθάνων;Greece|||||methana|
country-kypseli-athanasius|parish-kypseli-anthony|parish|Country Church|Country Church of Saint Athanasius in Stravologgos, Methana|Ιερό Εξωκκλήσιο Αγίου Αθανασίου Στραβολόγγου Κυψέλης Μεθάνων|Stravologgos, Methana|Στραβολόγγος Κυψέλης Μεθάνων;Greece|||||methana|
chapel-megalochori-ephraims|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of Venerable Ephraim the Syrian and Saint Ephraim of Nea Makri in Megalochori, Methana|Ιερός Ναός Οσίου Εφραίμ του Σύρου και Αγίου Εφραίμ Νέας Μάκρης|Megalochori, Methana|Μεγαλοχώρι Μεθάνων;Greece|||||methana|
cemetery-megalochori-demetrius|parish-megalochori-meeting|parish|Cemetery Church|Cemetery Church of Saint Demetrius in Megalochori, Methana|Ιερός Ναός Αγίου Δημητρίου Κοιμητηριακός Μεγαλοχωρίου Μεθάνων|Megalochori, Methana|Μεγαλοχώρι Μεθάνων;Greece|||||methana|
chapel-megalopotami-unmercenaries|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of the Holy Unmercenaries in Megalopotami, Methana|Ιερός Ναός Αγίων Αναργύρων Μεγαλοποταμίου Μεγαλοχωρίου Μεθάνων|Megalopotami, Methana|Μεγαλοπόταμι Μεθάνων;Greece|||||methana|
chapel-vathy-spyridon|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of Saint Spyridon in Vathy, Methana|Ιερός Ναός Αγίου Σπυρίδωνος Βαθέος Μεγαλοχωρίου Μεθάνων|Vathy, Methana|Βαθύ Μεθάνων;Greece|||||methana|
chapel-kameni-chora-forerunner|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of the Beheading of Saint John the Forerunner in Kameni Chora, Methana|Ιερός Ναός Αποκεφαλισμού Αγίου Ιωάννου Προδρόμου Καμένης Χώρας Μεθάνων|Kameni Chora, Methana|Καμένη Χώρα Μεθάνων;Greece|||||methana|
chapel-vathy-george|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of Saint George in Vathy, Methana|Ιερός Ναός Αγίου Γεωργίου Βαθέος Μεγαλοχωρίου Μεθάνων|Vathy, Methana|Βαθύ Μεθάνων;Greece|||||methana|
chapel-vathy-eleousa|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of Panagia Eleousa in Vathy, Methana|Ιερός Ναός Παναγίας Ελεούσας Βαθέος Μεγαλοχωρίου Μεθάνων|Vathy, Methana|Βαθύ Μεθάνων;Greece|||||methana|
chapel-vathy-palaiokastro-nicholas|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of Saint Nicholas at Palaiokastro in Vathy, Methana|Ιερός Ναός Αγίου Νικολάου Παλαιοκάστρου Βαθέος Μεγαλοχωρίου Μεθάνων|Palaiokastro, Vathy|Παλαιόκαστρο Βαθέος Μεθάνων;Greece|||||methana|
chapel-megalochori-four-saints|parish-megalochori-meeting|parish|Parish Chapel|Parish Chapel of Saints Niketas, Athanasius, Arsenios of Cappadocia, and Kosmas of Aetolia in Megalochori, Methana|Ιερός Ναός Αγίων Νικήτα, Αθανασίου του Μεγάλου, Αρσενίου του Καππαδόκου και Κοσμά του Αιτωλού|Megalochori, Methana|Μεγαλοχώρι Μεθάνων;Greece|||||methana|
country-steno-nativity|parish-megalochori-meeting|parish|Country Church|Country Church of the Nativity of the Theotokos in Steno, Methana|Ιερός Ναός Γενεσίου της Θεοτόκου Στενού Μεθάνων|Steno, Methana|Στενό Μεθάνων;Greece|||||methana|
country-steno-eleutherius|parish-megalochori-meeting|parish|Country Church|Country Church of Saint Eleutherius in Steno, Methana|Ιερός Ναός Αγίου Ελευθερίου Στενού Μεθάνων|Steno, Methana|Στενό Μεθάνων;Greece|||||methana|
country-steno-maura|parish-megalochori-meeting|parish|Country Church|Country Church of Saint Maura in Steno, Methana|Ιερός Ναός Αγίας Μαύρας Στενού Μεγαλοχωρίου Μεθάνων|Steno, Methana|Στενό Μεθάνων;Greece|||||methana|
country-sterna-transfiguration|parish-megalochori-meeting|parish|Country Church|Country Church of the Transfiguration of the Savior at Old Sterna, Methana|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Παλαιάς Στέρνας Μεθάνων|Old Sterna, Methana|Παλαιά Στέρνα Μεθάνων;Greece|||||methana|
country-kameni-chora-andrew|parish-megalochori-meeting|parish|Country Church|Country Church of Saint Andrew in Kameni Chora, Methana|Ιερός Ναός Αγίου Ανδρέου Καμένης Χώρας Μεγαλοχωρίου Μεθάνων|Kameni Chora, Methana|Καμένη Χώρα Μεθάνων;Greece|||||methana|
country-kameni-chora-krasopanagia|parish-megalochori-meeting|parish|Country Church|Country Church of Krasopanagia in Kameni Chora, Methana|Ιερός Ναός Κρασοπαναγιάς Καμένης Χώρας Μεγαλοχωρίου Μεθάνων|Kameni Chora, Methana|Καμένη Χώρα Μεθάνων;Greece|||||methana|
country-megalopotami-chrysostom|parish-megalochori-meeting|parish|Country Church|Country Church of Saint John Chrysostom in Megalopotami, Methana|Ιερός Ναός Αγίου Ιωάννου Χρυσοστόμου Μεγαλοποταμίου Μεγαλοχωρίου Μεθάνων|Megalopotami, Methana|Μεγαλοπόταμι Μεθάνων;Greece|||||methana|
country-megalopotami-marina|parish-megalochori-meeting|parish|Country Church|Country Church of Saint Marina in Megalopotami, Methana|Ιερός Ναός Αγίας Μαρίνας Μεγαλοποταμίου Μεγαλοχωρίου Μεθάνων|Megalopotami, Methana|Μεγαλοπόταμι Μεθάνων;Greece|||||methana|
country-vathy-prophet-elijah|parish-megalochori-meeting|parish|Country Church|Country Church of Prophet Elijah in Vathy, Methana|Ιερός Ναός Προφήτου Ηλιού Βαθέος Μεγαλοχωρίου Μεθάνων|Vathy, Methana|Βαθύ Μεθάνων;Greece|||||methana|
country-megalochori-forerunner|parish-megalochori-meeting|parish|Country Church|Country Church of Saint John the Forerunner in Megalochori, Methana|Ιερός Ναός Αγίου Ιωάννου Προδρόμου Μεγαλοχωρίου Μεθάνων|Megalochori, Methana|Μεγαλοχώρι Μεθάνων;Greece|||||methana|
chapel-kounoupitsa-george|parish-kounoupitsa-entrance|parish|Parish Chapel|Parish Chapel of Saint George in Agios Georgios, Methana|Ιερός Ναός Αγίου Γεωργίου Κουνουπίτσας Μεθάνων|Agios Georgios, Methana|Άγιος Γεώργιος Μεθάνων;Greece|||||methana|
cemetery-kounoupitsa-archangels|parish-kounoupitsa-entrance|parish|Cemetery Church|Cemetery Church of the Holy Archangels in Kounoupitsa, Methana|Ιερός Ναός Ταξιαρχών Κοιμητηριακός Κουνουπίτσας Μεθάνων|Kounoupitsa, Methana|Κουνουπίτσα Μεθάνων;Greece|||||methana|
chapel-kounoupitsa-transfiguration|parish-kounoupitsa-entrance|parish|Parish Chapel|Parish Chapel of the Transfiguration of the Savior in Kounoupitsa, Methana|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Κουνουπίτσας Μεθάνων|Kounoupitsa, Methana|Κουνουπίτσα Μεθάνων;Greece|||||methana|
pilgrimage-kounoupitsa-barbara|parish-kounoupitsa-entrance|parish|Pilgrimage Church|Pilgrimage Church of Saint Barbara in Kounoupitsa, Methana|Ιερό Προσκύνημα Αγίας Βαρβάρας Κουνουπίτσας Μεθάνων|Kounoupitsa, Methana|Κουνουπίτσα Μεθάνων;Greece|||||methana|
country-kounoupitsa-theologian|parish-kounoupitsa-entrance|parish|Country Church|Country Church of Saint John the Theologian in Kounoupitsa, Methana|Ιερός Ναός Αγίου Ιωάννου Θεολόγου Κουνουπίτσας Μεθάνων|Kounoupitsa, Methana|Κουνουπίτσα Μεθάνων;Greece|||||methana|
country-kounoupitsa-demetrius|parish-kounoupitsa-entrance|parish|Country Church|Country Church of Saint Demetrius in Kounoupitsa, Methana|Ιερός Ναός Αγίου Δημητρίου Κουνουπίτσας Μεθάνων|Kounoupitsa, Methana|Κουνουπίτσα Μεθάνων;Greece|||||methana|
chapel-makrylongos-annunciation|parish-palaia-loutra-dormition|parish|Parish Chapel|Parish Chapel of the Annunciation of the Theotokos in Makrylongos, Methana|Ιερός Ναός Ευαγγελισμού της Θεοτόκου Μακρυλόγγου Μεθάνων|Makrylongos, Methana|Μακρύλογγος Μεθάνων;Greece|||||methana|
chapel-agioi-theodoroi-all-saints-demetrius|parish-palaia-loutra-dormition|parish|Parish Chapel|Parish Chapel of All Saints and Saint Demetrius in Agioi Theodoroi, Methana|Ιερός Ναός Αγίων Πάντων και Αγίου Δημητρίου Αγίων Θεοδώρων Μεθάνων|Agioi Theodoroi, Methana|Άγιοι Θεόδωροι Μεθάνων;Greece|||||methana|
chapel-palaia-loutra-nicholas|parish-palaia-loutra-dormition|parish|Parish Chapel|Parish Chapel of Saint Nicholas in Palaia Loutra, Methana|Ιερός Ναός Αγίου Νικολάου Παλαιών Λουτρών Μεθάνων|Palaia Loutra, Methana|Παλαιά Λουτρά Μεθάνων;Greece|||||methana|
cemetery-makrylongos-panagia|parish-palaia-loutra-dormition|parish|Cemetery Church|Cemetery Church of Panagia in Makrylongos, Methana|Ιερός Ναός Παναγίας Μακρυλόγγου Κοιμητηριακός Μεθάνων|Makrylongos, Methana|Μακρύλογγος Μεθάνων;Greece|||||methana|
country-makrylongos-prophet-elijah|parish-palaia-loutra-dormition|parish|Country Church|Country Church of Prophet Elijah in Makrylongos, Methana|Ιερός Ναός Προφήτου Ηλιού Μακρυλόγγου Μεθάνων|Makrylongos, Methana|Μακρύλογγος Μεθάνων;Greece|||||methana|
country-makrylongos-constantine-helen|parish-palaia-loutra-dormition|parish|Country Church|Country Church of Saints Constantine and Helen in Makrylongos, Methana|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Μακρυλόγγου Μεθάνων|Makrylongos, Methana|Μακρύλογγος Μεθάνων;Greece|||||methana|
country-agioi-theodoroi-theodore|parish-palaia-loutra-dormition|parish|Country Church|Country Church of Saint Theodore Stratelates in Agioi Theodoroi, Methana|Ιερός Ναός Αγίου Θεοδώρου Στρατηλάτου Αγίων Θεοδώρων Μεθάνων|Agioi Theodoroi, Methana|Άγιοι Θεόδωροι Μεθάνων;Greece|||||methana|
country-agioi-theodoroi-life-giving-spring|parish-palaia-loutra-dormition|parish|Country Church|Country Church of the Life-Giving Spring in Agioi Theodoroi, Methana|Ιερός Ναός Ζωοδόχου Πηγής Αγίων Θεοδώρων Μεθάνων|Agioi Theodoroi, Methana|Άγιοι Θεόδωροι Μεθάνων;Greece|||||methana|
'''

TROIZINIA_AEGINA_ERMIONI_SOURCE = r'''
chapel-poros-annunciation|parish-poros-george|parish|Parish Chapel|Parish Chapel of the Annunciation of the Theotokos in Saint George Square, Poros|Ιερός Ναός Ευαγγελιστρίας στην πλατεία Αγίου Γεωργίου Πόρου|Poros|Πλατεία Αγίου Γεωργίου Πόρου;Greece|||||poros_church|
chapel-poros-meeting|parish-poros-george|parish|Parish Chapel|Parish Chapel of the Meeting of the Lord in the Poros Market|Ιερός Ναός Υπαπαντής του Κυρίου στην αγορά Πόρου|Poros|Αγορά Πόρου;Greece|||||poros_church|
chapel-poros-transfiguration|parish-poros-george|parish|Parish Chapel|Parish Chapel of the Transfiguration of the Savior in Poros|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Πόρου|Poros|Πόρος;Greece|||||poros_church|
chapel-poros-entrance|parish-poros-george|parish|Parish Chapel|Parish Chapel of the Entrance of the Theotokos in Poros|Ιερός Ναός Εισοδίων της Θεοτόκου Πόρου|Poros|Πόρος;Greece|||||poros_church|
chapel-poros-demetrius|parish-poros-george|parish|Parish Chapel|Parish Chapel of Saint Demetrius in Poros|Ιερός Ναός Αγίου Δημητρίου Πόρου|Poros|Πόρος;Greece|||||poros_church|
chapel-poros-phanourios|parish-poros-george|parish|Parish Chapel|Parish Chapel of Saint Phanourios in Poros|Ιερός Ναός Αγίου Φανουρίου Πόρου|Poros|Πόρος;Greece|||||poros_church|
chapel-neorio-george|parish-poros-george|parish|Parish Chapel|Parish Chapel of Saint George in Neorio, Poros|Ιερός Ναός Αγίου Γεωργίου Νεωρίου Πόρου|Neorio, Poros|Νεώριο Πόρου;Greece|||||poros_church|
chapel-lemonodasos-panteleimon|parish-poros-george|parish|Parish Chapel|Parish Chapel of Saint Panteleimon in Lemonodasos|Ιερός Ναός Αγίου Παντελεήμονος Λεμονοδάσους|Lemonodasos|Λεμονοδάσος;Greece|||||poros_church|
chapel-poros-marina|parish-poros-george|parish|Parish Chapel|Parish Chapel of Saint Marina in Poros|Ιερός Ναός Αγίας Μαρίνας Πόρου|Poros|Πόρος;Greece|||||poros_church|
private-lemonodasos-seraphim|parish-poros-george|parish|Private Chapel|Private Chapel of Saint Seraphim in Lemonodasos|Ιδιωτικός Ιερός Ναός Αγίου Σεραφείμ Λεμονοδάσους|Lemonodasos|Λεμονοδάσος;Greece|||||poros_church|
private-foussa-nectarius|parish-poros-george|parish|Private Chapel|Private Chapel of Saint Nectarius in Foussa|Ιδιωτικός Ιερός Ναός Αγίου Νεκταρίου Φούσσας|Foussa|Φούσσα;Greece|||||poros_church|
private-foussa-theologian|parish-poros-george|parish|Private Chapel|Private Chapel of Saint John the Theologian in Foussa|Ιδιωτικός Ιερός Ναός Αγίου Ιωάννου Θεολόγου Φούσσας|Foussa|Φούσσα;Greece|||||poros_church|
chapel-kalloni-nativity-luke|parish-skapeti-annunciation|parish|Parish Chapel|Parish Chapel of the Nativity of the Theotokos and Saint Luke the Physician in Kalloni|Ιερός Ναός Γενεσίου της Θεοτόκου και Αγίου Λουκά του Ιατρού Καλλονής|Kalloni|Καλλονή Τροιζηνίας;Greece|2298031360||||skapeti|skapeti
chapel-aegina-synaxis-thomas|parish-aegina-synaxis|parish|Parish Chapel|Parish Chapel of Saint Thomas in Livadi, Aegina|Ιερός Ναός Αγίου Θωμά στο προαύλιο της ενορίας Αιγινητών Αγίων|Livadi, Aegina|Λιβάδι Αίγινας;Greece|||||aig_synaxis|
chapel-ladiano-unmercenaries|parish-aegina-synaxis|parish|Parish Chapel|Parish Chapel of the Holy Unmercenaries in Ladiano, Aegina|Ιερός Ναός Αγίων Αναργύρων Λαδιανού Αιγίνης|Ladiano, Aegina|Λαδιανό Αίγινας;Greece|||||aig_synaxis|
chapel-plakakia-trinity|parish-aegina-synaxis|parish|Parish Chapel|Parish Chapel of the Holy Trinity in Plakakia, Aegina|Ιερός Ναός Αγίας Τριάδος Πλακακίων Αιγίνης|Plakakia, Aegina|Πλακάκια Αίγινας;Greece|||||aig_synaxis|
chapel-chloe-nicholas|parish-aegina-synaxis|parish|Parish Chapel|Parish Chapel of Saint Nicholas in Chloe, Aegina|Ιερός Ναός Αγίου Νικολάου Χλόης Αιγίνης|Chloe, Aegina|Χλόη Αίγινας;Greece|||||aig_synaxis|
chapel-ellanion-archangel|parish-pacheia-rachi|parish|Parish Chapel|Parish Chapel of the Holy Archangel at Sfyrichtres on Mount Ellanion|Ιερός Ναός Παμμεγίστου Ταξιάρχου στις Σφυρίχτρες Ελλανίου Όρους|Mount Ellanion, Aegina|Σφυρίχτρες Ελλανίου Όρους Αίγινας;Greece|||||pacheia|
cemetery-pacheia-mesosporitissa|parish-pacheia-rachi|parish|Cemetery Church|Cemetery Church of the Entrance of the Theotokos Mesosporitissa near Pacheia Rachi|Ιερός Ναός Εισοδίων της Θεοτόκου Μεσοσπορίτισσας Κοιμητηρίου Παχειάς Ράχης|Pacheia Rachi, Aegina|Οδός προς Ανιτσαίο Αίγινας;Greece|||||pacheia|
chapel-ellanion-meeting|parish-pacheia-rachi|parish|Parish Chapel|Parish Chapel of the Meeting of the Savior on Mount Ellanion|Ιερός Ναός Υπαπαντής του Σωτήρος Ελλανίου Όρους|Mount Ellanion, Aegina|Ελλάνιο Όρος Αίγινας;Greece|||||pacheia|
cemetery-tzikides-demetrius|parish-pacheia-rachi|parish|Cemetery Church|Cemetery Church of Saint Demetrius in Tzikides, Aegina|Ιερός Ναός Αγίου Δημητρίου Κοιμητηρίου Τζίκηδων Αιγίνης|Tzikides, Aegina|Τζίκηδες Αίγινας;Greece|||||pacheia|
chapel-pacheia-julius-julian|parish-pacheia-rachi|parish|Parish Chapel|Parish Chapel of Saints Julius and Julian in Pacheia Rachi|Παρεκκλήσιο Αγίων Ιουλίου και Ιουλιανού Παχειάς Ράχης Αίγινας|Pacheia Rachi, Aegina|Παλαιός Ιερός Ναός Παμμεγίστων Ταξιαρχών;Παχειά Ράχη Αίγινας;Greece|||||pacheia|
chapel-aegina-cathedral-tatiana|parish-aegina-dormition|parish|Parish Chapel|Parish Chapel of Saint Tatiana at the Aegina Metropolitan Church|Παρεκκλήσιο Αγίας Τατιανής Ιερού Μητροπολιτικού Ναού Αιγίνης|Aegina|Μητροπόλεως;18010 Αίγινα;Greece|||||aig_cathedral|
cemetery-ermioni-michael-kyriaki-all-saints|parish-ermioni-archangels|parish|Cemetery Church|New Cemetery Church of Archangel Michael, Saint Kyriaki, and All Saints in Ermioni|Ιερός Ναός Αρχαγγέλου Μιχαήλ, Αγίας Κυριακής και Αγίων Πάντων Νέου Κοιμητηρίου Ερμιόνης|Ermioni|Νέο Κοιμητήριο Ερμιόνης;Greece|||||erm_arch|
cemetery-ermioni-andrew|parish-ermioni-archangels|parish|Cemetery Church|Old Cemetery Church of Saint Andrew in Ermioni|Ιερός Ναός Αγίου Ανδρέου Παλαιού Κοιμητηρίου Ερμιόνης|Ermioni|Παλαιό Κοιμητήριο Ερμιόνης;Greece|||||erm_arch|
chapel-kasidiari-life-giving-spring|parish-ermioni-archangels|parish|Parish Chapel|Parish Chapel of the Life-Giving Spring in Kasidiari, Ermioni|Ιερός Ναός Ζωοδόχου Πηγής Κασιδιαρίου Ερμιόνης|Kasidiari, Ermioni|Κασιδιάρι Ερμιόνης;Greece|||||erm_arch|
chapel-ermioni-tryphon|parish-ermioni-archangels|parish|Parish Chapel|Parish Chapel of Saint Tryphon on the Ermioni Plain|Ιερός Ναός Αγίου Τρύφωνος Κάμπου Ερμιόνης|Ermioni|Κάμπος Ερμιόνης;Greece|||||erm_arch|
chapel-ermioni-apostles|parish-ermioni-archangels|parish|Parish Chapel|Parish Chapel of the Holy Apostles outside Ermioni|Ιερός Ναός Αγίων Αποστόλων εκτός Ερμιόνης|Ermioni|Ερμιόνη;Greece|||||erm_arch|
chapel-ermionida-forerunner|parish-ermioni-archangels|parish|Parish Chapel|Parish Chapel of Saint John the Forerunner on the Ermionida Gulf|Ιερός Ναός Αγίου Ιωάννου Προδρόμου Κόλπου Ερμιονίδας|Ermionida Gulf|Κόλπος Ερμιονίδας;Greece|||||erm_arch|
chapel-petrothalassa-timothy-maura|parish-ermioni-archangels|parish|Parish Chapel|Parish Chapel of Saints Timothy and Maura in Petrothalassa|Ιερός Ναός Αγίων Τιμοθέου και Μαύρας Πετροθάλασσας|Petrothalassa|Πετροθάλασσα Ερμιονίδας;Greece|||||erm_arch|
chapel-ermioni-cyrus-john|parish-ermioni-archangels|parish|Parish Chapel|Parish Chapel of Holy Unmercenaries Cyrus and John on the Ermioni Plain|Ιερός Ναός Αγίων Αναργύρων Κύρου και Ιωάννου Κάμπου Ερμιόνης|Ermioni|Κάμπος Ερμιόνης;Greece|||||erm_arch|
chapel-ermioni-athanasius|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Athanasius in Ermioni|Ιερός Ναός Αγίου Αθανασίου Ερμιόνης|Ermioni|Ερμιόνη;Greece|||||erm_dorm|
chapel-dardiza-charalambos|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Charalambos in Dardiza|Ιερός Ναός Αγίου Χαραλάμπους Δαρδίζας|Dardiza|Δαρδίζα Ερμιονίδας;Greece|||||erm_dorm|
chapel-portizes-platytera|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Platytera ton Ouranon in Portizes|Ιερός Ναός Πλατυτέρας των Ουρανών Πορτιζών|Portizes|Πορτίζες Ερμιονίδας;Greece|||||erm_dorm|
chapel-ermioni-george|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint George on the Ermioni Plain|Ιερός Ναός Αγίου Γεωργίου Κάμπου Ερμιόνης|Ermioni|Κάμπος Ερμιόνης;Greece|||||erm_dorm|
chapel-ermioni-john-russian-david|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint John the Russian and Venerable David the Elder in Ermioni|Ιερός Ναός Αγίου Ιωάννου του Ρώσου και Οσίου Δαυίδ του Γέροντος Ερμιόνης|Ermioni|Ερμιόνη;Greece|||||erm_dorm|
chapel-krothi-gerasimos|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Gerasimos in Krothi|Ιερός Ναός Αγίου Γερασίμου Κρόθης|Krothi|Κρόθη Ερμιόνης;Greece|||||erm_dorm|
chapel-avlonos-prophet-elijah|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Prophet Elijah in Avlonos|Ιερός Ναός Προφήτου Ηλιού Αυλώνος|Avlonos|Αυλώνος Ερμιονίδας;Greece|||||erm_dorm|
cemetery-dardiza-nativity|parish-ermioni-dormition|parish|Cemetery Church|Cemetery Church of the Nativity of the Theotokos in Dardiza|Ιερός Ναός Γενεσίου της Θεοτόκου Κοιμητηρίου Δαρδίζας|Dardiza|Κοιμητήριο Δαρδίζας;Greece|||||erm_dorm|
chapel-petrothalassa-demetrius|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Demetrius in Petrothalassa|Ιερός Ναός Αγίου Δημητρίου Πετροθάλασσας|Petrothalassa|Πετροθάλασσα Ερμιονίδας;Greece|||||erm_dorm|
chapel-krothi-menas|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Menas in Krothi|Ιερός Ναός Αγίου Μηνά Κρόθης|Krothi|Κρόθη Ερμιόνης;Greece|||||erm_dorm|
chapel-ermioni-catherine|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Catherine in Ermioni|Ιερός Ναός Αγίας Αικατερίνης Ερμιόνης|Ermioni|Ερμιόνη;Greece|||||erm_dorm|
chapel-kapari-ephraim|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Ephraim in Kapari|Ιερός Ναός Αγίου Εφραίμ Καπαρίου|Kapari|Καπάρι Ερμιονίδας;Greece|||||erm_dorm|
chapel-avlonos-paraskevi|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Paraskevi in Avlonos|Ιερός Ναός Αγίας Παρασκευής Αυλώνος|Avlonos|Αυλώνος Ερμιονίδας;Greece|||||erm_dorm|
chapel-ermioni-life-giving-spring|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of the Life-Giving Spring in Ermioni|Ιερός Ναός Ζωοδόχου Πηγής Ερμιόνης|Ermioni|Ερμιόνη;Greece|||||erm_dorm|
chapel-ermioni-nicholas-vounenois|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Nicholas en Vounenois in Ermioni|Ιερός Ναός Αγίου Νικολάου εν Βουνένοις Ερμιόνης|Ermioni|Ερμιόνη;Greece|||||erm_dorm|
chapel-bisti-nicholas|parish-ermioni-dormition|parish|Parish Chapel|Parish Chapel of Saint Nicholas in Bisti|Ιερός Ναός Αγίου Νικολάου Μπιστίου|Bisti, Ermioni|Μπίστι Ερμιόνης;Greece|||||erm_dorm|
cemetery-sambariza-unfading-rose|parish-thermisia-annunciation|parish|Cemetery Church|Cemetery Church of the Unfading Rose in Sambariza|Ιερός Ναός Ρόδον το Αμάραντον Κοιμητηρίου Σαμπάριζας|Sambariza|Σαμπάριζα Θερμησίας;Greece|||||thermisia|
cemetery-thermisia-george|parish-thermisia-annunciation|parish|Cemetery Church|Cemetery Church of Saint George in Thermisia|Ιερός Ναός Αγίου Γεωργίου Κοιμητηρίου Θερμησίας|Thermisia|Κοιμητήριο Θερμησίας;Greece|||||thermisia|
chapel-thermisia-phanourios|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of Saint Phanourios in Thermisia|Ιερός Ναός Αγίου Φανουρίου Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
chapel-thermisia-nectarius|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of Saint Nectarius in Thermisia|Ιερός Ναός Αγίου Νεκταρίου Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
chapel-thermisia-constantine-helen|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of Saints Constantine and Helen in Thermisia|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
chapel-thermisia-archangels|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of the Holy Archangels in Thermisia|Ιερός Ναός Παμμεγίστων Ταξιαρχών Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
chapel-plepi-blaise|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of Saint Blaise in Plepi|Ιερός Ναός Αγίου Βλασίου Πλεπίου|Plepi|Πλέπι Ερμιονίδας;Greece|||||thermisia|
chapel-thermisia-unmercenaries|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of the Holy Unmercenaries in Thermisia|Ιερός Ναός Αγίων Αναργύρων Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
chapel-thermisia-demetrius|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of Saint Demetrius in Thermisia|Ιερός Ναός Αγίου Δημητρίου Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
chapel-thermisia-andrew|parish-thermisia-annunciation|parish|Parish Chapel|Parish Chapel of Saint Andrew in Thermisia|Ιερός Ναός Αγίου Ανδρέου Θερμησίας|Thermisia|Θερμησία;Greece|||||thermisia|
monastery-chapel-ermioni-eupraxia|monastery-ermioni-unmercenaries|monastery|Monastery Chapel|Monastery Chapel of Saint Eupraxia in Ermioni|Παρεκκλήσιο Αγίας Ευπραξίας Ιεράς Μονής Αγίων Αναργύρων Ερμιόνης|Ermioni|Ιερά Μονή Αγίων Αναργύρων Ερμιόνης;Greece|||||erm_mon|
monastery-chapel-mouzaki-elijah|monastery-ermioni-unmercenaries|monastery|Monastery Chapel|Monastery Chapel of Prophet Elijah on Mount Mouzaki|Ιερός Ναός Προφήτου Ηλιού Όρους Μουζακίου Κουβέρτας|Mount Mouzaki|Όρος Μουζάκι Κουβέρτα;Greece|||||erm_mon|
monastery-chapel-ermioni-cyril-methodius|monastery-ermioni-unmercenaries|monastery|Monastery Chapel|Monastery Chapel of Saints Cyril and Methodius in Ermioni|Παρεκκλήσιο Αγίων Κυρίλλου και Μεθοδίου Ιεράς Μονής Αγίων Αναργύρων Ερμιόνης|Ermioni|Ιερά Μονή Αγίων Αναργύρων Ερμιόνης;Greece|||||erm_mon|
monastery-chapel-ermioni-isidore|monastery-ermioni-unmercenaries|monastery|Monastery Chapel|Monastery Chapel of Saint Isidore in Ermioni|Ιερός Ναός Αγίου Ισιδώρου Ιεράς Μονής Αγίων Αναργύρων Ερμιόνης|Ermioni|Ιερά Μονή Αγίων Αναργύρων Ερμιόνης;Greece|||||erm_mon|
chapel-iliokastro-nicholas-planas|parish-iliokastro-apostles|parish|Parish Chapel|Parish Chapel of Saint Nicholas Planas beneath the Holy Apostles Church in Iliokastro|Υπόγειος Ιερός Ναός Αγίου Νικολάου του Πλανά Ηλιοκάστρου|Iliokastro|Ιερός Ναός Αγίων Αποστόλων Ηλιοκάστρου;Greece|||||iliokastro|
cemetery-iliokastro-george|parish-iliokastro-apostles|parish|Cemetery Church|Cemetery Church of Saint George in Iliokastro|Ιερός Ναός Αγίου Γεωργίου Κοιμητηρίου Ηλιοκάστρου|Iliokastro|Κοιμητήριο Ηλιοκάστρου;Greece|||||iliokastro|
chapel-iliokastro-paraskevi|parish-iliokastro-apostles|parish|Parish Chapel|Parish Chapel of Saint Paraskevi in Iliokastro|Ιερός Ναός Αγίας Παρασκευής Ηλιοκάστρου|Iliokastro|Ηλιόκαστρο;Greece|||||iliokastro|
chapel-loukaiti-archangels|parish-iliokastro-apostles|parish|Parish Chapel|Parish Chapel of the Holy Archangels in Loukaiti|Ιερός Ναός Παμμεγίστων Ταξιαρχών Λουκαϊτίου|Loukaiti|Λουκαΐτι Ερμιονίδας;Greece|||||iliokastro|
cemetery-loukaiti-eleutherius|parish-iliokastro-apostles|parish|Cemetery Church|Cemetery Church of Saint Eleutherius in Loukaiti|Ιερός Ναός Αγίου Ελευθερίου Κοιμητηρίου Λουκαϊτίου|Loukaiti|Κοιμητήριο Λουκαϊτίου;Greece|||||iliokastro|
monastery-chapel-aegina-nectarius|hermitage-aegina-trinity-nectarius|monastery|Monastery Chapel|Monastery Chapel of Saint Nectarius at the Holy Trinity Hermitage in Aegina|Παρεκκλήσιο Αγίου Νεκταρίου Ιεράς Μονής Αγίας Τριάδος Αιγίνης|Aegina|Ιερά Μονή Αγίας Τριάδος Αίγινας;Greece|||||nectarius|
monastery-chapel-aegina-archangels|hermitage-aegina-trinity-nectarius|monastery|Monastery Chapel|Monastery Chapel of the Holy Archangels at the tomb of Saint Nectarius in Aegina|Παρεκκλήσιο Ταξιαρχών επί του τάφου Αγίου Νεκταρίου Αιγίνης|Aegina|Ιερά Μονή Αγίας Τριάδος Αίγινας;Greece|||||nectarius|
monastery-church-aegina-nectarius|hermitage-aegina-trinity-nectarius|monastery|Monastery Church|Monastery Church of Saint Nectarius in Aegina|Νέος Ιερός Ναός Αγίου Νεκταρίου Αιγίνης|Aegina|Ιερά Μονή Αγίας Τριάδος Αίγινας;Greece|||||nectarius|
'''

KRANIDI_SOURCE = r'''
chapel-kranidi-basil|parish-kranidi-forerunner|parish|Parish Chapel|Parish Chapel of Saint Basil the Great in Kranidi|Παρεκκλήσιο Αγίου Βασιλείου του Μεγάλου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||kranidi_all|
country-oureza-elisha|parish-kranidi-forerunner|parish|Country Church|Country Church of Prophet Elisha in Oureza|Ιερός Ναός Προφήτου Ελισσαίου Ούρεζας|Oureza|Ούρεζα Κρανιδίου;Greece|||||kranidi_all|
country-kranidi-george|parish-kranidi-forerunner|parish|Country Church|Country Church of Saint George in Kranidi|Ιερός Ναός Αγίου Γεωργίου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||kranidi_all|
country-loutra-andrew|parish-kranidi-forerunner|parish|Country Church|Country Church of Saint Andrew in Loutra, Kranidi|Ιερός Ναός Αγίου Ανδρέου Λουτρών Κρανιδίου|Loutra, Kranidi|Λουτρά Κρανιδίου;Greece|||||kranidi_all|
country-kranidi-kyriaki|parish-kranidi-forerunner|parish|Country Church|Country Church of Saint Kyriaki on the Kranidi to Nafplio Road|Ιερός Ναός Αγίας Κυριακής στην οδό Κρανιδίου Ναυπλίου|Kranidi|Οδός Κρανιδίου Ναυπλίου;Greece|||||kranidi_all|
country-kranidi-athanasius|parish-kranidi-forerunner|parish|Country Church|Country Church of Saint Athanasius toward Koilada|Ιερός Ναός Αγίου Αθανασίου προς Κοιλάδα Κρανιδίου|Kranidi|Οδός Κρανιδίου προς Κοιλάδα;Greece|||||kranidi_all|
country-golemi-theodora|parish-kranidi-forerunner|parish|Country Church|Country Church of Saint Theodora in Golemi|Ιερός Ναός Αγίας Θεοδώρας Γκολεμίου|Golemi|Γκολέμι Κρανιδίου;Greece|||||kranidi_all|
country-milindra-prophet-elijah|parish-kranidi-forerunner|parish|Country Church|Country Church of Prophet Elijah on Milindra Hill|Ιερός Ναός Προφήτου Ηλιού λόφου Μηλίνδρας|Milindra Hill|Λόφος Μηλίνδρας Κρανιδίου;Greece|||||kranidi_all|
private-kranidi-irene-chrysovalantou|parish-kranidi-forerunner|parish|Private Chapel|Private Chapel of Saint Irene Chrysovalantou in Kranidi|Ιδιωτικός Ιερός Ναός Αγίας Ειρήνης Χρυσοβαλάντου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||kranidi_all|
cemetery-kranidi-archangels|parish-kranidi-entrance|parish|Cemetery Church|Cemetery Church of the Holy Archangels in Kranidi|Ιερός Ναός Παμμεγίστων Ταξιαρχών Κοιμητηρίου Κρανιδίου|Kranidi|Κοιμητήριο Κρανιδίου;Greece|||||kato|
country-kranidi-holy-girdle|parish-kranidi-entrance|parish|Country Church|Country Church of the Holy Girdle in Kranidi|Ιερός Ναός Αγίας Ζώνης Κρανιδίου|Kranidi|Κρανίδι;Greece|||||kato|
country-thyni-nicholas|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Nicholas in Thyni|Ιερός Ναός Αγίου Νικολάου Θυνί|Thyni|Θυνί Κρανιδίου;Greece|||||kato|
country-doroufi-spyridon|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Spyridon in Doroufi|Ιερός Ναός Αγίου Σπυρίδωνος Δορουφίου|Doroufi|Δορούφι Κρανιδίου;Greece|||||kato|
country-villa-panteleimon|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Panteleimon in Villa|Ιερός Ναός Αγίου Παντελεήμονος Βίλλας|Villa, Kranidi|Βίλλα Κρανιδίου;Greece|||||kato|
country-golemi-chrysostom|parish-kranidi-entrance|parish|Country Church|Country Church of Saint John Chrysostom in Golemi|Ιερός Ναός Αγίου Ιωάννου Χρυσοστόμου Γκολεμίου|Golemi|Γκολέμι Κρανιδίου;Greece|||||kato|
country-kranidi-prophet-elijah|parish-kranidi-entrance|parish|Country Church|Country Church of Prophet Elijah near Saint Anna Hill|Ιερός Ναός Προφήτου Ηλιού νοτιοδυτικά λόφου Αγίας Άννας Κρανιδίου|Kranidi|Λόφος Αγίας Άννας Κρανιδίου;Greece|||||kato|
country-oureza-constantine-helen|parish-kranidi-entrance|parish|Country Church|Country Church of Saints Constantine and Helen in Oureza|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Ούρεζας|Oureza|Ούρεζα Κρανιδίου;Greece|||||kato|
country-oureza-george|parish-kranidi-entrance|parish|Country Church|Country Church of Saint George in Oureza|Ιερός Ναός Αγίου Γεωργίου Ούρεζας|Oureza|Ούρεζα Κρανιδίου;Greece|||||kato|
country-koilada-paraskevi|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Paraskevi near Koilada|Ιερός Ναός Αγίας Παρασκευής πλησίον Κοιλάδας|Koilada|Πλησίον Κοιλάδας Αργολίδας;Greece|||||kato|
country-delpera-demetrius|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Demetrius in Delpera|Ιερός Ναός Αγίου Δημητρίου Δελπέρας|Delpera|Δελπέρα Κρανιδίου;Greece|||||kato|
country-taxiarchis-trinity|parish-kranidi-entrance|parish|Country Church|Country Church of the Holy Trinity at Taxiarchis Mill|Ιερός Ναός Αγίας Τριάδος Ταξιάρχη Μύλου Τσουρούτη|Taxiarchis, Kranidi|Ταξιάρχης Μύλος Τσουρούτη Κρανιδίου;Greece|||||kato|
country-chapel-taxiarchis-all-saints|country-taxiarchis-trinity|parish|Country Chapel|Country Chapel of All Saints at the Holy Trinity Church in Taxiarchis|Παρεκκλήσιο Αγίων Πάντων Ιερού Ναού Αγίας Τριάδος Ταξιάρχη|Taxiarchis, Kranidi|Ταξιάρχης Μύλος Τσουρούτη Κρανιδίου;Greece|||||kato|
country-pyrgos-nicholas|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Nicholas in Pyrgos|Ιερός Ναός Αγίου Νικολάου Πύργου|Pyrgos, Kranidi|Πύργος Κρανιδίου;Greece|||||kato|
country-katsifoni-nectarius|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Nectarius in Katsifoni|Ιερός Ναός Αγίου Νεκταρίου Κατσιφωνίου|Katsifoni|Κατσιφώνι Κρανιδίου;Greece|||||kato|
country-lefka-myrtidiotissa|parish-kranidi-entrance|parish|Country Church|Country Church of Panagia Myrtidiotissa in Lefka|Ιερός Ναός Παναγίας Μυρτιδιώτισσας Λεύκας|Lefka, Kranidi|Λεύκα Κρανιδίου;Greece|||||kato|
country-kranidi-anthony|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Anthony in Kranidi|Ιερός Ναός Αγίου Αντωνίου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||kato|
country-golemi-sozon|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Sozon in Golemi|Ιερός Ναός Αγίου Σώζοντος Γκολεμίου|Golemi|Γκολέμι Κρανιδίου;Greece|||||kato|
country-doroufi-ascension|parish-kranidi-entrance|parish|Country Church|Country Church of the Ascension in Doroufi|Ιερός Ναός Αναλήψεως Δορουφίου|Doroufi|Δορούφι Κρανιδίου;Greece|||||kato|
country-saint-anna-hill-epiphanius|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Epiphanius on Saint Anna Hill|Ιερός Ναός Αγίου Επιφανίου λόφου Αγίας Άννας Κρανιδίου|Saint Anna Hill, Kranidi|Λόφος Αγίας Άννας Κρανιδίου;Greece|||||kato|
country-oureza-paraskevi|parish-kranidi-entrance|parish|Country Church|Country Church of Saint Paraskevi in Oureza|Ιερός Ναός Αγίας Παρασκευής Ούρεζας|Oureza|Ούρεζα Κρανιδίου;Greece|||||kato|
chapel-bardounia-george|parish-kranidi-synaxis|parish|Parish Chapel|Parish Chapel of Saint George in Bardounia, Kranidi|Ιερός Ναός Αγίου Γεωργίου Μπαρδουνίων Κρανιδίου|Bardounia, Kranidi|Μπαρδούνια Κρανιδίου;Greece|||||pano|
country-kranidi-pano-prophet-elijah|parish-kranidi-synaxis|parish|Country Church|Country Church of Prophet Elijah under the Synaxis Parish in Kranidi|Ιερός Ναός Προφήτου Ηλιού Ενορίας Συνάξεως Θεοτόκου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||pano|
country-kranidi-pano-andrew|parish-kranidi-synaxis|parish|Country Church|Country Church of Saint Andrew under the Synaxis Parish in Kranidi|Ιερός Ναός Αγίου Ανδρέου Ενορίας Συνάξεως Θεοτόκου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||pano|
country-kranidi-pano-panteleimon|parish-kranidi-synaxis|parish|Country Church|Country Church of Saint Panteleimon under the Synaxis Parish in Kranidi|Ιερός Ναός Αγίου Παντελεήμονος Ενορίας Συνάξεως Θεοτόκου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||pano|
country-kranidi-pano-marina|parish-kranidi-synaxis|parish|Country Church|Country Church of Saint Marina under the Synaxis Parish in Kranidi|Ιερός Ναός Αγίας Μαρίνας Ενορίας Συνάξεως Θεοτόκου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||pano|
country-kranidi-pano-theologian|parish-kranidi-synaxis|parish|Country Church|Country Church of Saint John the Theologian under the Synaxis Parish in Kranidi|Ιερός Ναός Αγίου Ιωάννου Θεολόγου Ενορίας Συνάξεως Θεοτόκου Κρανιδίου|Kranidi|Κρανίδι;Greece|||||pano|
country-flamboura-archangel|parish-kranidi-synaxis|parish|Country Church|Country Church of the Archangel in Flamboura|Ιερός Ναός Ταξιάρχου Φλαμπούρας|Flamboura|Φλαμπούρα Κρανιδίου;Greece|||||pano|
'''

EXPECTED_TOTAL = 228
EXPECTED_CORE = 74
EXPECTED_DEPENDENCIES = 154
EXPECTED_KINDS = {"monastery": 28, "parish": 200}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Church": 15,
    "Church": 1,
    "Country Chapel": 1,
    "Country Church": 51,
    "Hermitage": 10,
    "Metropolitan Church": 4,
    "Monastery": 10,
    "Monastery Chapel": 6,
    "Monastery Church": 1,
    "Monastic House": 1,
    "Parish Chapel": 74,
    "Parish Church": 47,
    "Pilgrimage Church": 2,
    "Private Chapel": 4,
}
EXPECTED_CONTACTS = {
    "address_bodies": 228,
    "contact_bodies": 37,
    "phone_bodies": 37,
    "public_phone_values": 49,
    "fax_bodies": 2,
    "public_fax_values": 2,
    "email_bodies": 8,
    "public_email_values": 8,
    "body_owned_sites": 2,
}
ALLOWED_HOSTS = {
    "api.et.gr",
    "ecclesiagreece.gr",
    "imhydra.gr",
    "www.imhydra.gr",
    "imna.gr",
    "www.imna.gr",
    "prodromos-kranidiou.gr",
    "www.prodromos-kranidiou.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2018\u2019\u201c\u201d\ufffd]"
)
GREEK_RE = re.compile(r"[\u0370-\u03ff]")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

LIVE_MARKERS = {
    SOURCE_URLS["profile"]: ("Ανδρικές μονές", "Γυναικεία ησυχαστήρια"),
    SOURCE_URLS["admin"]: ("Ενοριακοί Ναοί: 52", "Εξωκκλήσια: 754"),
    SOURCE_URLS["districts"]: ("Αρχιερατεία Ύδρας", "Αρχιερατεία Κρανιδίου"),
    SOURCE_URLS["visitor"]: ("Πληροφορίες για τον επισκέπτη",),
    SOURCE_URLS["nectarius"]: ("Άγιος Νεκτάριος", "παρεκκλήσιον"),
    SOURCE_URLS["palaiochora"]: ("Μεσαιωνική Καστροπολιτεία",),
    SOURCE_URLS["imna"]: ("Ιερός Μητροπολιτικός Ναός", "2297022654"),
    SOURCE_URLS["prodromos"]: ("ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΚΡΑΝΙΔΙΟΥ", "2754022049"),
}


def parse_list(value, delimiter=","):
    return [item.strip() for item in value.split(delimiter) if item.strip()]


def parse_sources(value, row_key):
    keys = parse_list(value)
    unknown = [key for key in keys if key not in SOURCE_URLS]
    if unknown:
        raise ValueError("%s has unknown source keys: %r" % (row_key, unknown))
    return [SOURCE_URLS[key] for key in keys]


def parse_rows():
    rows = []
    blocks = (
        CORE_SOURCE,
        HYDRA_METHANA_SOURCE,
        TROIZINIA_AEGINA_ERMIONI_SOURCE,
        KRANIDI_SOURCE,
    )
    for block in blocks:
        for raw in block.strip().splitlines():
            fields = raw.split("|")
            if len(fields) != 14:
                raise ValueError(
                    "source row has %d fields instead of 14: %s" %
                    (len(fields), raw[:80])
                )
            (key, parent_key, kind, rank, name, local, seat, address,
             phones, faxes, emails, site, sources, contact_sources) = fields
            row_id = "%s-%s" % (PARENT, key)
            row = {
                "id": row_id,
                "parent": (
                    "%s-%s" % (PARENT, parent_key)
                    if parent_key else PARENT
                ),
                "kind": kind,
                "rank": rank,
                "name": name,
                "local": local,
                "seat": seat,
                "country": "GR",
                "address": parse_list(address, ";"),
                "sources": parse_sources(sources, key),
                "checked": CHECKED,
            }
            for field, value in (
                    ("phones", phones),
                    ("faxes", faxes),
                    ("emails", emails)):
                parsed = parse_list(value)
                if parsed:
                    row[field] = parsed
            if site:
                row["site"] = site
            parsed_contact_sources = parse_sources(contact_sources, key)
            if parsed_contact_sources:
                row["contact_sources"] = parsed_contact_sources
                row["contact_checked"] = CHECKED
            rows.append(row)
    return rows


ROWS = parse_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)


def unicase(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value.casefold()).strip()


def validate_url(value, label):
    parsed = urlparse(value)
    if (parsed.scheme != "https" or not parsed.netloc or
            parsed.netloc not in ALLOWED_HOSTS):
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


def validate_phone(value, label):
    main = value.split(" ext. ", 1)[0]
    digits = re.sub(r"\D", "", main)
    if len(digits) != 10 or digits[0] not in "26":
        raise ValueError("%s carries an invalid public number: %s" %
                         (label, value))
    if " ext. " in value and not re.fullmatch(r".* ext\. \d+", value):
        raise ValueError("%s carries a malformed extension: %s" %
                         (label, value))


def coverage(rows):
    return {
        "address_bodies": sum(bool(row.get("address")) for row in rows),
        "contact_bodies": sum(bool(
            row.get("phones") or row.get("faxes") or row.get("emails") or
            row.get("site")
        ) for row in rows),
        "phone_bodies": sum(bool(row.get("phones")) for row in rows),
        "public_phone_values": sum(
            len(row.get("phones") or []) for row in rows
        ),
        "fax_bodies": sum(bool(row.get("faxes")) for row in rows),
        "public_fax_values": sum(
            len(row.get("faxes") or []) for row in rows
        ),
        "email_bodies": sum(bool(row.get("emails")) for row in rows),
        "public_email_values": sum(
            len(row.get("emails") or []) for row in rows
        ),
        "body_owned_sites": sum(bool(row.get("site")) for row in rows),
    }


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if (ledger.get("v") != 1 or ledger.get("countries") != ["GR"] or
            ledger.get("parent") != PARENT or
            ledger.get("checked") != CHECKED):
        raise ValueError("Ydra candidate ledger metadata drifted")
    expected_summary = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_parish_rows": 52,
        "legal_parish_rows": 53,
        "legal_pilgrimage_rows": 1,
        "current_monastic_rows": 21,
        "exact_named_dependency_rows": EXPECTED_DEPENDENCIES,
        "parish_kind_rows": EXPECTED_KINDS["parish"],
        "monastery_kind_rows": EXPECTED_KINDS["monastery"],
        **EXPECTED_CONTACTS,
        "rank_counts": EXPECTED_RANKS,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Ydra ledger summary drifted")
    expected_candidates = {
        "gr-ydra-legal-current-parish-reconciliation",
        "gr-ydra-unnamed-chapel-aggregate",
        "gr-ydra-spetses-roster-gap",
        "gr-ydra-contact-conflicts",
        "gr-ydra-monastic-rank-reconciliations",
        "gr-ydra-historic-and-dissolved-bodies",
        "gr-ydra-search-and-map-leads",
    }
    candidates = {
        item.get("candidate_id"): item
        for item in ledger.get("candidates") or []
    }
    if set(candidates) != expected_candidates:
        raise ValueError("Ydra candidate holdings drifted")
    if any(FORBIDDEN_PUNCTUATION.search(text)
           for text in walk_strings(ledger)):
        raise ValueError("Ydra candidate ledger contains forbidden punctuation")
    for group in ("candidates", "source_reconciliations",
                  "official_parent_audit", "exclusions"):
        entries = ledger.get(group)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Ydra ledger lacks %s" % group)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 4:
                raise ValueError("Ydra ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or group)
    return ledger


def build():
    if len(CORE_SOURCE.strip().splitlines()) != EXPECTED_CORE:
        raise ValueError("Ydra core roster count drifted")
    if sum(len(block.strip().splitlines()) for block in (
            HYDRA_METHANA_SOURCE,
            TROIZINIA_AEGINA_ERMIONI_SOURCE,
            KRANIDI_SOURCE)) != EXPECTED_DEPENDENCIES:
        raise ValueError("Ydra dependency roster count drifted")
    result = []
    ids = set()
    seen = {PARENT}
    signatures = set()
    ranks = Counter()
    kinds = Counter()
    for source in ROWS:
        row = {
            key: value for key, value in source.items()
            if value not in (None, "", [])
        }
        row_id = row.get("id")
        if not row_id or row_id in ids or row_id == PARENT:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if row.get("parent") not in seen:
            raise ValueError(
                "%s precedes or lacks parent %s" %
                (row_id, row.get("parent"))
            )
        if (row.get("country") != "GR" or
                row.get("kind") not in EXPECTED_KINDS or
                row.get("rank") not in EXPECTED_RANKS):
            raise ValueError("%s has invalid country, kind, or rank" % row_id)
        if not row.get("name") or not row.get("local") or not row.get("seat"):
            raise ValueError("%s lacks its name, local name, or seat" % row_id)
        if GREEK_RE.search(row["name"]) or not GREEK_RE.search(row["local"]):
            raise ValueError("%s lacks a complete English or Greek name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(row)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        sources = list(row.get("sources") or [])
        if not sources or len(sources) > 3:
            raise ValueError("%s lacks bounded official provenance" % row_id)
        for source_url in sources:
            validate_url(source_url, row_id)
        row["sources"] = sources
        row["cite"] = list(sources)
        contact_sources = list(row.get("contact_sources") or [])
        has_contact = bool(
            row.get("phones") or row.get("faxes") or row.get("emails") or
            row.get("site")
        )
        if has_contact:
            if not contact_sources or row.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            if (len(contact_sources) > 3 or
                    any(value not in sources for value in contact_sources)):
                raise ValueError("%s has invalid contact provenance" % row_id)
        elif contact_sources or "contact_checked" in row:
            raise ValueError(
                "%s carries contact provenance without contact data" % row_id
            )
        for value in (row.get("phones") or []) + (row.get("faxes") or []):
            validate_phone(value, row_id)
        for email_value in row.get("emails") or []:
            if not EMAIL_RE.fullmatch(email_value):
                raise ValueError("%s carries an invalid email" % row_id)
        if row.get("site"):
            validate_url(row["site"], row_id)
            if row["site"] not in sources:
                raise ValueError("%s has an unproven direct site" % row_id)
        signature = (
            row.get("parent"), row.get("rank"), unicase(row.get("local")),
            unicase(" ".join(row.get("address") or [])),
        )
        if signature in signatures:
            raise ValueError("%s duplicates another body" % row_id)
        signatures.add(signature)
        ids.add(row_id)
        seen.add(row_id)
        ranks[row["rank"]] += 1
        kinds[row["kind"]] += 1
        result.append(row)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or any(
            ENGLISH_NAMES[row["id"]] != row["name"] for row in result):
        raise ValueError("Ydra English name coverage drifted")
    if set(ENGLISH_SEATS) != {
            row["seat"] for row in result if row.get("seat")}:
        raise ValueError("Ydra English seat coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Ydra rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Ydra kind totals drifted: %r" % dict(kinds))
    actual_contacts = coverage(result)
    if actual_contacts != EXPECTED_CONTACTS:
        raise ValueError("Ydra contact coverage drifted: %r" % actual_contacts)
    validate_ledger()
    return {PARENT: {
        "v": 1,
        "parent": PARENT,
        "country": "GR",
        "rows": result,
    }}


def ascii_url(value):
    parts = urlsplit(value)
    return urlunsplit((
        parts.scheme,
        parts.netloc,
        quote(parts.path, safe="/%"),
        quote(parts.query, safe="=&%"),
        "",
    ))


def fetch(value):
    is_pdf = value.endswith(".pdf") or value == SOURCE_URLS["legal"]
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": (
            "application/pdf" if is_pdf else
            "text/html,application/xhtml+xml"
        ),
        "Accept-Encoding": "identity",
    }
    if is_pdf:
        headers["Range"] = "bytes=0-8191"
    request = Request(ascii_url(value), headers=headers)
    with urlopen(request, timeout=45) as response:
        payload = response.read(8192 if is_pdf else 2000000)
        content_type = response.headers.get("Content-Type", "").lower()
        status = getattr(response, "status", 200)
    return payload, content_type, status


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return unicase(" ".join(text.split()))


def check_live():
    checks = set(SOURCE_URLS.values())

    def one(value):
        try:
            payload, content_type, status = fetch(value)
        except OSError as exc:
            raise ValueError(
                "source fetch failed for %s: %s" % (value, exc)
            ) from exc
        if status < 200 or status >= 400:
            raise ValueError("source returned HTTP %s: %s" % (status, value))
        is_pdf = value.endswith(".pdf") or value == SOURCE_URLS["legal"]
        if is_pdf:
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("source is not a PDF: %s" % value)
            return value
        if "html" not in content_type:
            raise ValueError("source is not HTML: %s" % value)
        page = normalized_page(payload)
        missing = [
            marker for marker in LIVE_MARKERS.get(value, ())
            if unicase(marker) not in page
        ]
        if missing:
            raise ValueError("%s lacks markers: %r" % (value, missing))
        return value

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(one, sorted(checks)))
    return len(checks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        checked = check_live()
        print("Ydra live checks passed for %d official URLs" % checked)
    if args.dump:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.check or not args.check_live:
        rows = data[PARENT]["rows"]
        contacts = coverage(rows)
        print(
            "Ydra checks passed: %d bodies, 52 current parishes, "
            "21 monastic bodies, %d exact named dependencies, "
            "%d contact bodies" % (
                len(rows), EXPECTED_DEPENDENCIES,
                contacts["contact_bodies"],
            )
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Ydra: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
