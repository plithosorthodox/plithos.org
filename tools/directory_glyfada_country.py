#!/usr/bin/env python3
"""Validate exact named Glyfada Metropolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_glyfada_country.py --check
    python tools/directory_glyfada_country.py --check-live
    python tools/directory_glyfada_country.py --dump
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-glyfada"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "glyfada_country.json"
)

OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_decembrios.pdf"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/glyphadas"
)
HOME = "https://www.imglyfadas.gr/"
DIRECTORY = "https://www.imglyfadas.gr/index.php/enories"
DIRECTORY_PAGE_2 = DIRECTORY + "?start=17"
DETAIL_ROOT = "https://www.imglyfadas.gr/index.php/enories/item/"


def detail(value):
    return DETAIL_ROOT + value


NICHOLAS_CONTACT = "https://agiosnikolaosglyfadas.gr/contact/"
PANTELEIMON_SITE = "https://agiospan.gr/"
PAUL_SITE = "https://enoriapavloudimitriou.blogspot.com/"
PAUL_APRIL = "https://enoriapavloudimitriou.blogspot.com/2026/04/"
PAUL_JULY = "https://enoriapavloudimitriou.blogspot.com/2026/07/"
TRYFON_SITE = "https://agiostryfon.gr/"
TRINITY_ELLINIKO_CONTACT = (
    "https://agiatriadaellhnikou.gr/"
    "%ce%b5%cf%80%ce%b9%ce%ba%ce%bf%ce%b9%ce%bd%cf%89%ce%bd%ce%af%ce%b1/"
)
KOIMISI_VOULA_SITE = "https://koimisi.blogspot.com/"
EISODIA_VARI_SITE = "https://eisodiavaris.gr/"
VARKIZA_CONTACT = (
    "https://www.koimisitheotokouvarkizas.gr/"
    "%CE%B5%CE%BE%CE%BF%CE%BC%CE%BF%CE%BB%CF%8C%CE%B3%CE%B7%CF%83%CE%B7"
)
IMANG_SITE = "https://imang.gr/"
CHRYSOSTOM_CURRENT_PDF = (
    "https://agiosnikolaosglyfadas.gr/download.php?"
    "fgr=issues%2Fissues_0015_2038_1_gr.pdf"
)

BODY_SOURCES = {
    "NICHOLAS": NICHOLAS_CONTACT,
    "PANTELEIMON": PANTELEIMON_SITE,
    "PAUL": PAUL_SITE,
    "TRYFON": TRYFON_SITE,
    "TRINITY_ELLINIKO": TRINITY_ELLINIKO_CONTACT,
    "KOIMISI_VOULA": KOIMISI_VOULA_SITE,
    "EISODIA_VARI": EISODIA_VARI_SITE,
    "VARKIZA": VARKIZA_CONTACT,
    "IMANG": IMANG_SITE,
}

BODY_SITES = {
    "NICHOLAS": "https://agiosnikolaosglyfadas.gr/",
    "PANTELEIMON": PANTELEIMON_SITE,
    "PAUL": PAUL_SITE,
    "TRYFON": TRYFON_SITE,
    "TRINITY_ELLINIKO": "https://agiatriadaellhnikou.gr/",
    "KOIMISI_VOULA": KOIMISI_VOULA_SITE,
    "EISODIA_VARI": EISODIA_VARI_SITE,
    "VARKIZA": "https://www.koimisitheotokouvarkizas.gr/",
    "IMANG": IMANG_SITE,
}


# key|rank|English dedication|Greek local name|English seat|Greek address|
# phones|emails|site token|detail path|live markers
PARISH_SOURCE = r'''
constantine-helen|Metropolitan Church|Saints Constantine and Helen|Ἱερός Μητροπολιτικός Ναός Ἁγίων Κωνσταντίνου και Ἑλένης Γλυφάδας|Glyfada|Λ. Ποσειδῶνος καί Σ. Καράγιωργα, Γλυφάδα Τ.Κ. 166 75|2108943405|inkonelengl@gmail.com||571-eros-mitropolitikos-naos-gion-konstantinou-lenis-glyfadas|Ἁγίων Κωνσταντίνου;210.89.43.405
nicholas|Parish Church|Saint Nicholas|Ἱερός Ναός Ἁγίου Νικολάου Γλυφάδας|Glyfada|Ἀρτέμιδος καί Ζαμάνου, Γλυφάδα Τ.Κ. 166 74|2108949167,2108944398|info@agiosnikolaosglyfadas.gr|NICHOLAS|572-eros-naos-giou-nikolaou-glyfadas|Ἁγίου Νικολάου;210.89.49.167
panteleimon|Parish Church|Saint Panteleimon|Ἱερός Ναός Ἁγίου Παντελεήμονος Γλυφάδας|Glyfada|Κ. Καραμανλῆ 4, Γλυφάδα Τ.Κ. 166 75|2109626443,6977357795|sgiospgl@gmail.com|PANTELEIMON|573-eros-naos-giou-panteleimonos-glyfadas|Ἁγίου Παντελεήμονος;210.96.26.443
paul-demetrius|Parish Church|Saints Paul and Demetrius|Ἱερός Ναός Ἁγίων Παύλου και Δημητρίου Γλυφάδας|Glyfada|Κυνουρίας καί Μυστρᾶ 100, Αἴγλη Γλυφάδας Τ.Κ. 165 61|2109614974|agiospavlos2022@gmail.com|PAUL|778-eros-naos-gion-paylou-dimitriou-glyfadas|Ἁγίων Παύλου;210.96.14.974
holy-trinity-glyfada|Cathedral|Holy Trinity|Καθεδρικός Ἱερός Ναός Ἁγίας Τριάδος Γλυφάδας|Glyfada|Ἀρετῆς καί Ἁγ. Τριάδος, Γλυφάδα Τ.Κ. 166 74|2109621150|agia.triada.glyfadas@gmail.com||576-kathedrikos-eros-naos-gias-triados-glyfadas?print=1&tmpl=component|Ἁγίας Τριάδος;210.96.21.150
tryphon|Parish Church|Saint Tryphon|Ἱερός Ναός Ἁγίου Τρύφωνος Τερψιθέας Γλυφάδας|Terpsithea, Glyfada|Ἀρχιπελάγους καί Γ. Γεννηματᾶ, Γλυφάδα Τ.Κ. 165 62|2109611211|agiostryfonglyfadas@gmail.com,agiostryfon.secretary@gmail.com|TRYFON|577-eros-naos-giou-tryfonos-terpsitheas-glyfadas|Ἁγίου Τρύφωνος;210.96.11.211
entrance-theotokos|Parish Church|Entrance of the Theotokos|Ἱερός Ναός Εἰσοδίων Θεοτόκου Τερψιθέας Γλυφάδας|Terpsithea, Glyfada|Πλατ. Καραϊσκάκη, Γλυφάδα Τ.Κ. 165 62|2109612373|eisodiaglyfada@gmail.com||574-eros-naos-e-sodion-theotokou-g-fanouriou-terpsitheas-glyfadas|Εἰσοδίων Θεοτόκου;210.96.12.373
dormition-dikigorika|Parish Church|Dormition of the Theotokos at Dikigorika|Ἱερός Ναός Κοιμήσεως Θεοτόκου Δικηγορικῶν Γλυφάδας|Dikigorika, Glyfada|Ροντήρη καί Ἀρτεμισίου, Γλυφάδα Τ.Κ. 166 75|2109680397|koimdikigorika@protonmail.com||579-eros-naos-koimiseos-theotokou-dikigorik-n-glyfadas|Κοιμήσεως Θεοτόκου;210.96.80.397
dormition-evryali|Parish Church|Dormition of the Theotokos at Evryali|Ἱερός Ναός Κοιμήσεως Θεοτόκου Εὐρυάλης Γλυφάδας|Evryali, Glyfada|Ὁδ. Σοφίας Βέμπω καί Ἰάσωνος, Ἄνω Γλυφάδα Τ.Κ. 165 61|2109621723|inpanagitsakarapanou@gmail.com||578-eros-naos-koimiseos-theotokou-e-ryalis-glyfadas|Κοιμήσεως Θεοτόκου;210.96.21.723
transfiguration|Parish Church|Transfiguration of the Savior|Ἱερός Ναός Μεταμορφώσεως Σωτῆρος Ἑλληνικοῦ|Elliniko|Λεωφ. Ἰασωνίδου καί Χρυσάνθου Τραπεζοῦντος, Ἑλληνικό Τ.Κ. 166 77|2109618624|in.metamorfosis.sotiros.ell@gmail.com||580-eros-naos-metamorfoseos-sot-ros-lliniko|Μεταμορφώσεως Σωτῆρος;210.96.18.624
holy-trinity-elliniko|Parish Church|Holy Trinity|Ἱερός Ναός Ἁγίας Τριάδος Ἑλληνικοῦ|Elliniko|Πλατ. Ἁγ. Τριάδος, Ἑλληνικό Τ.Κ. 167 77|2109628949,2109624989|agiatriadaellinikou@gmail.com|TRINITY_ELLINIKO|581-eros-naos-gias-triados-lliniko|Ἁγίας Τριάδος;210.96.28.949
paraskevi-elliniko|Parish Church|Saint Paraskevi|Ἱερός Ναός Ἁγίας Παρασκευῆς Ἑλληνικοῦ|Elliniko|Ὁδός Ἀεροπορίας, Ἁμαξοστάσιον Ἑλληνικοῦ, Τ.Κ. 167 77|2109926641|agiasparaskeuesierosnaos@gmail.com||582-eros-naos-gias-paraskev-s-lliniko|Ἁγίας Παρασκευῆς;210.99.26.641
dormition-voula|Parish Church|Dormition of the Theotokos|Ἱερός Ναός Κοιμήσεως Θεοτόκου Βούλας|Voula|Βασιλέως Παύλου 2, Βούλα Τ.Κ. 166 73|2108958128|koimisivoul@yahoo.gr|KOIMISI_VOULA|583-eros-naos-koimiseos-theotokou-voylas|Κοιμήσεως Θεοτόκου;210.89.58.128
john-forerunner-voula|Parish Church|Saint John the Forerunner|Ἱερός Ναός Ἁγίου Ἰωάννου Βούλας|Voula|Ἁγ. Ἰωάννου καί Βασ. Παύλου, Βούλα Τ.Κ. 166 73|2108958756|agioannisvoulas@gmail.com||567-eros-naos-giou-oannou-voylas|Ἁγίου Ἰωάννου;210.89.58.756
nektarios-voula|Parish Church|Saint Nektarios|Ἱερός Ναός Ἁγίου Νεκταρίου Πανοράματος Βούλας|Panorama, Voula|Πλατ. Ἄλσους, Βούλα Τ.Κ. 166 73|2108954921|agiosnektariosvoulas@gmail.com||506-eros-naos-giou-nektariou-panoramatos-voylas|Ἁγίου Νεκταρίου;210.89.54.921
panagia-faneromeni|Parish Church|Panagia Faneromeni|Ἱερός Ναός Ὑπεραγίας Θεοτόκου Φανερωμένης Βουλιαγμένης|Vouliagmeni|Λεωφόρος Ἀθηνᾶς καί Αἰόλου 1, Βουλιαγμένη Τ.Κ. 166 71|2108964068|infaneromenisvoulnis@gmail.com||584-eros-naos-peragias-theotokou-faneromenis-vouliagmenis|Θεοτόκου;210.89.64.068
entrance-vari|Parish Church|Entrance of the Theotokos|Ἱερός Ναός Εἰσοδίων Θεοτόκου Βάρης|Vari|Πλατ. Ἡρώων, Βάρη 2 Τ.Κ. 166 72|2108971895|eisodiavaris@gmail.com|EISODIA_VARI|568-eros-naos-e-sodion-theotokou-varis|Εἰσοδίων Θεοτόκου;210.89.71.895
peter-paul-vari|Parish Church|Saints Peter and Paul|Ἱερός Ναός Ἁγίων Ἀποστόλων Πέτρου και Παύλου Διλόφου Βάρης|Dilofo, Vari|Πανός 9, Δίλοφο Βάρης Τ.Κ. 166 72|2108950216|inpetroupavlouvaris@gmail.com||566-eros-naos-gion-postolon-petrou-paylou-dilofou-varis|Πέτρου;210.89.50.216
dormition-varkiza|Parish Church|Dormition of the Theotokos|Ἱερός Ναός Κοιμήσεως Θεοτόκου Βαρκίζης|Varkiza|Ἥρας 10 καί Ὠκεανίδων, Βάρκιζα Τ.Κ. 166 72|2108972460,6944065733|koimisitheotokouvarkizas@gmail.com|VARKIZA|653-eros-naos-koimiseos-theotokou-varkizis|Κοιμήσεως Θεοτόκου;210.89.72.460
prophet-elijah-vari|Parish Church|Prophet Elijah|Ἱερός Ναός Προφήτου Ἠλιοῦ Κόρμπι Βάρης|Korbi, Vari|Προφήτου Ἠλιοῦ 7 καί Θεσσαλονίκης 1, Κόρμπι Βάρης Τ.Κ. 166 72|2109655370|profhthshliaskormpivaris@gmail.com||569-eros-naos-profitou-lio-kormpi-varis|Προφήτου Ἠλιοῦ;210.96.55.370
'''


# key|kind|rank|English name|Greek local name|English seat|Greek address|
# phones|emails|site token|source tokens|live markers
OTHER_SOURCE = r'''
life-giving-spring|monastery|Monastery|Life-Giving Spring Monastery of the Most Holy Theotokos, Glyfada|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Ζωοδόχου Πηγῆς Γλυφάδας|Ano Glyfada|Παπαφλέσσα 37, Πυρνάρι, Ἄνω Γλυφάδα Τ.Κ. 166 74|2172183595|prwtosygkellos.imgl@gmail.com||ZOODOCHOS|Ζωοδόχου Πηγῆς;217.218.3595
trinity-nektarios-monastery|monastery|Monastery|Holy Trinity and Saint Nektarios Monastery, Terpsithea|Ἱερά Μονή Ἁγίας Τριάδος καί Ἁγίου Νεκταρίου Τερψιθέας Γλυφάδας|Terpsithea, Glyfada|Ἥβης 109 καί Ἁγίου Νεκταρίου 330, Ἄνω Γλυφάδα Τ.Κ. 165 62|2109622239|imagnektariou@gmail.com|IMANG|TRINITY_MONASTERY,IMANG|Ἁγίας Τριάδος;210.96.22.239
rose-unfading-hermitage|monastery|Hermitage|Rose of the Unfading Flower and Saint Spyridon Hermitage, Glyfada|Ἱερό Ἡσυχαστήριο Ὑπεραγίας Θεοτόκου Ρόδου τοῦ Ἀμάραντου καί Ἁγίου Σπυρίδωνος Γλυφάδας|Glyfada|Γλυφάδα||||HERMITAGE|Ρόδου τοῦ Ἀμάραντου
holy-sophia-vari|parish|Metropolitan Chapel|Saint Sophia Metropolitan Chapel, Cheroma, Vari|Ἱερό Μητροπολιτικό Παρεκκλήσιο Ἁγίας Σοφίας Χερώματος Βάρης|Cheroma, Vari|Χέρωμα Βάρης Τ.Κ. 166 72|6986989039|||HOLY_SOPHIA,HOME|Ἁγίας Σοφίας;6986.989.039
panteleimon-hospital|parish|Hospital Chapel|Saint Panteleimon Chapel, Asklipieio Hospital of Voula|Παρεκκλήσιο Ἁγίου Παντελεήμονος Ἀσκληπιείου Νοσοκομείου Βούλας|Voula|Ὁδ. Βασ. Παύλου 1, Βούλα Τ.Κ. 166 01|213.21.63.324-5|||DORMITION_VOULA,HOME|Ἁγίου Παντελεήμονος;213.21.63.324-5
stylianos-recovery-center|parish|Institutional Chapel|Saint Stylianos Chapel, Children's Recovery and Rehabilitation Center, Voula|Παρεκκλήσιο Ἁγίου Στυλιανοῦ Κέντρου Ἀποκαταστάσεως καί Ἀποθεραπείας Παίδων Βούλας|Voula|Κέντρο Ἀποκαταστάσεως καί Ἀποθεραπείας Παίδων, πρώην Π.Ι.Κ.Π.Α., Βούλα||||DORMITION_VOULA|Ἁγίου Στυλιανοῦ;Κέντρου Ἀποκαταστάσεως
nektarios-panteleimon-chapel|parish|Parish Chapel|Saint Nektarios Chapel at Saint Panteleimon Parish, Glyfada|Παρεκκλήσιο Ἁγίου Νεκταρίου Ἱεροῦ Ναοῦ Ἁγίου Παντελεήμονος Γλυφάδας|Glyfada|Κ. Καραμανλῆ 4, Γλυφάδα Τ.Κ. 166 75||||PANTELEIMON_DETAIL|παρεκκλησίου τοῦ Ἁγίου Νεκταρίου
paraskevi-irene-chapel|parish|Parish Chapel|Saints Paraskevi and Irene Chapel at Evryali, Glyfada|Παρεκκλήσιο Ἁγίων Παρασκευῆς καί Εἰρήνης Εὐρυάλης Γλυφάδας|Evryali, Glyfada|Ὁδ. Σοφίας Βέμπω καί Ἰάσωνος, Ἄνω Γλυφάδα Τ.Κ. 165 61||||EVRYALI_DETAIL|Παρεκκλήσιο τῶν Ἁγίων Παρασκευῆς καί Εἰρήνης
nikodemos-monastery-chapel|monastery|Monastery Chapel|Saint Nikodemos of the Holy Mountain Chapel|Παρεκκλήσιο Ἁγίου Νικοδήμου τοῦ Ἁγιορείτου|Terpsithea, Glyfada|Ἥβης 109 καί Ἁγίου Νεκταρίου 330, Ἄνω Γλυφάδα Τ.Κ. 165 62||||TRINITY_MONASTERY|Παρεκκλήσιο;Ἁγίου Νικοδήμου
catherine-dilofo-chapel|parish|Parish Chapel|Saint Catherine Chapel, Dilofo, Vari|Παρεκκλήσιο Ἁγίας Αἰκατερίνης Διλόφου Βάρης|Dilofo, Vari|Δίλοφο Βάρης||||PETER_PAUL_DETAIL|σημερινό Παρεκκλήσιο Αγίας Αικατερίνης
phanourios-chapel|parish|Parish Chapel|Saint Phanourios Chapel, Terpsithea, Glyfada|Ἱερός Ναός Ἁγίου Μεγαλομάρτυρος Φανουρίου Τερψιθέας Γλυφάδας|Terpsithea, Glyfada|Πλατ. Καραϊσκάκη, Γλυφάδα Τ.Κ. 165 62||||ENTRANCE_GLYFADA_DETAIL|ὑπόγειος Ἱερός Ναός;Ἁγίου Μεγαλομάρτυρος Φανουρίου
john-chrysostom-chapel|parish|Parish Chapel|Saint John Chrysostom Chapel at Saint Nicholas Parish, Glyfada|Ἱερό Παρεκκλήσιο Ἁγίου Ἰωάννου Χρυσοστόμου Ἱεροῦ Ναοῦ Ἁγίου Νικολάου Γλυφάδας|Glyfada|Κάτω ἀπό τόν Ἱερό Ναό Ἁγίου Νικολάου, εἴσοδος ἀπό ὁδό Φοίβης, Γλυφάδα||||CHRYSOSTOM_CURRENT|Παρεκκλήσιο;Χρυσοστόμου;Φοίβης
prophet-elijah-chapel|parish|Parish Chapel|Prophet Elijah Chapel of Saints Paul and Demetrius Parish, Glyfada|Ἱερό Παρεκκλήσιο Προφήτου Ἠλιοῦ Ἐνορίας Ἁγίων Παύλου καί Δημητρίου Ἄνω Γλυφάδας|Glyfada|Πρόποδες Ὑμηττοῦ, Γλυφάδα||||PAUL_JULY|Παρεκκλησίου τοῦ Προφήτου Ηλιού;πρόποδες του Υμηττού
raphael-nicholas-irene-chapel|parish|Parish Chapel|Saints Raphael, Nicholas and Irene Chapel, Glyfada|Παρεκκλήσιο Ἁγίων Ραφαήλ, Νικολάου καί Εἰρήνης Γλυφάδας|Glyfada|Τριπόλεως 92, Γλυφάδα||||PAUL_APRIL|Αγίων Ραφαήλ;Τριπόλεως 92
'''

OTHER_URLS = {
    "ZOODOCHOS": detail(
        "594-iera-moni-iperagias-theotoku-zoodoxu-pigis-glifadas"
    ),
    "TRINITY_MONASTERY": detail(
        "600-era-moni-gias-triados-giou-nektariou-terpsitheas-glyfadas"
    ),
    "HERMITAGE": detail(
        "601-ero-syxastirio-peragias-theotokou-rodou-to-marantou-"
        "giou-spyridonos-glyfadas"
    ),
    "HOLY_SOPHIA": detail(
        "565-ero-mitr-parekklisio-gias-sofias-xeromatos-varis"
    ),
    "DORMITION_VOULA": detail(
        "583-eros-naos-koimiseos-theotokou-voylas"
    ),
    "PANTELEIMON_DETAIL": detail(
        "573-eros-naos-giou-panteleimonos-glyfadas"
    ),
    "EVRYALI_DETAIL": detail(
        "578-eros-naos-koimiseos-theotokou-e-ryalis-glyfadas"
    ),
    "PETER_PAUL_DETAIL": detail(
        "566-eros-naos-gion-postolon-petrou-paylou-dilofou-varis"
    ),
    "ENTRANCE_GLYFADA_DETAIL": detail(
        "574-eros-naos-e-sodion-theotokou-g-fanouriou-"
        "terpsitheas-glyfadas"
    ),
    "CHRYSOSTOM_CURRENT": CHRYSOSTOM_CURRENT_PDF,
    "PAUL_JULY": PAUL_JULY,
    "PAUL_APRIL": PAUL_APRIL,
    "IMANG": IMANG_SITE,
    "HOME": HOME,
}


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "body"


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def build_rows():
    rows = []
    parish_lines = PARISH_SOURCE.strip().splitlines()
    if len(parish_lines) != 20:
        raise ValueError("expected 20 regulated Glyfada parishes")
    for number, raw in enumerate(parish_lines, 1):
        (key, rank, dedication, local, seat, address, phones, emails,
         site_token, detail_path, markers) = raw.split("|", 10)
        detail_url = detail(detail_path)
        sources = [detail_url, OFFICIAL_PDF]
        contact_sources = [detail_url]
        site = ""
        if site_token:
            body_source = BODY_SOURCES[site_token]
            sources.append(body_source)
            site = BODY_SITES[site_token]
            if site_token in {
                "NICHOLAS", "PANTELEIMON", "TRYFON",
                "TRINITY_ELLINIKO", "VARKIZA",
            }:
                contact_sources.append(body_source)
        name = "%s of %s, %s" % (rank, dedication, seat)
        row = {
            "id": "gr-glyfada-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": sources,
            "contact_sources": contact_sources,
            "contact_checked": CHECKED,
            "legal_markers": [dedication, seat],
            "live_markers": split_values(markers.replace(";", ",")),
        }
        if phones:
            row["phones"] = split_values(phones)
        if emails:
            row["emails"] = split_values(emails)
        if site:
            row["site"] = site
        rows.append(row)

    for offset, raw in enumerate(OTHER_SOURCE.strip().splitlines(), 21):
        (key, kind, rank, name, local, seat, address, phones, emails,
         site_token, source_tokens, markers) = raw.split("|", 11)
        sources = [OTHER_URLS[token.strip()]
                   for token in source_tokens.split(",") if token.strip()]
        row = {
            "id": "gr-glyfada-%03d-%s" % (offset, key),
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": sources,
            "live_markers": split_values(markers.replace(";", ",")),
        }
        if phones:
            row["phones"] = split_values(phones)
        if emails:
            row["emails"] = split_values(emails)
        if phones or emails:
            row["contact_sources"] = list(sources)
            row["contact_checked"] = CHECKED
        if site_token:
            row["site"] = BODY_SITES[site_token]
        rows.append(row)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 34
EXPECTED_OWNER_COUNTS = {PARENT: 34}
EXPECTED_KINDS = {"monastery": 4, "parish": 30}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Hermitage": 1,
    "Hospital Chapel": 1,
    "Institutional Chapel": 1,
    "Metropolitan Chapel": 1,
    "Metropolitan Church": 1,
    "Monastery": 2,
    "Monastery Chapel": 1,
    "Parish Chapel": 7,
    "Parish Church": 18,
}
EXPECTED_CONTACT_BODIES = 24
EXPECTED_PHONE_BODIES = 24
EXPECTED_PHONE_VALUES = 28
EXPECTED_EMAIL_BODIES = 22
EXPECTED_EMAIL_VALUES = 23
EXPECTED_SITE_BODIES = 9
EXPECTED_ADDRESS_BODIES = 34
EXISTING_PARENTS = {PARENT}
BINARY_ONLY_LIVE_IDS = {
    "gr-glyfada-032-john-chrysostom-chapel",
}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imglyfadas.gr",
    "www.imglyfadas.gr",
    "agiosnikolaosglyfadas.gr",
    "www.agiosnikolaosglyfadas.gr",
    "agiospan.gr",
    "www.agiospan.gr",
    "enoriapavloudimitriou.blogspot.com",
    "agiostryfon.gr",
    "www.agiostryfon.gr",
    "agiatriadaellhnikou.gr",
    "www.agiatriadaellhnikou.gr",
    "koimisi.blogspot.com",
    "eisodiavaris.gr",
    "www.eisodiavaris.gr",
    "koimisitheotokouvarkizas.gr",
    "www.koimisitheotokouvarkizas.gr",
    "imang.gr",
    "www.imang.gr",
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


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc not in ALLOWED_HOSTS:
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
    if item.get("phones") or item.get("emails"):
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks current contact provenance" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
        if source_url not in sources:
            raise ValueError("contact source is outside identity sources")
    site = item.get("site")
    if site:
        validate_url(site, item.get("id"))
        source_hosts = {urlparse(value).netloc for value in sources}
        if urlparse(site).netloc not in source_hosts:
            raise ValueError("%s site host lacks an identity source" % item.get("id"))
    item.pop("legal_markers", None)
    item.pop("live_markers", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Glyfada candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Glyfada candidate ledger date drifted")
    expected_summary = {
        PARENT: 34,
        "total": 34,
        "regulated_parish_rows": 20,
        "parish_kind_rows": 30,
        "monastery_kind_rows": 4,
        "contact_bodies": 24,
        "phone_bodies": 24,
        "public_phone_values": 28,
        "email_bodies": 22,
        "public_email_values": 23,
        "body_owned_sites": 9,
        "address_bodies": 34,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Glyfada ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Glyfada ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Glyfada ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Glyfada ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Glyfada ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
    signatures = {}
    ranks = Counter()
    kinds = Counter()
    owners = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in ids or row_id in EXISTING_PARENTS:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has the wrong parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has the wrong country" % row_id)
        if item.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if item.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.fullmatch(email):
                raise ValueError("%s carries an invalid email" % row_id)
        signature = (item["parent"], unicase(item["local"]),
                     unicase(item["seat"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s" %
                             (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        owners[item["parent"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Glyfada English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Glyfada rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Glyfada kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Glyfada parent totals drifted")
    coverage = (
        sum(bool(x.get("phones") or x.get("emails") or x.get("site"))
            for x in result),
        sum(bool(x.get("phones")) for x in result),
        sum(len(x.get("phones") or []) for x in result),
        sum(bool(x.get("emails")) for x in result),
        sum(len(x.get("emails") or []) for x in result),
        sum(bool(x.get("site")) for x in result),
        sum(bool(x.get("address")) for x in result),
    )
    expected = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected:
        raise ValueError("Glyfada contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf,"
                  "text/javascript,application/javascript",
    })
    with urlopen(request, timeout=60) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = unicase(text)
    return re.sub(r"\s+", " ", text)


def compact_digits(value):
    return re.sub(r"\D", "", value)


def check_live_sources():
    required = {HOME, DIRECTORY, DIRECTORY_PAGE_2,
                CHURCH_OF_GREECE_PAGE, OFFICIAL_PDF}
    required.update(url for row in ROWS for url in row.get("sources", []))
    cache = {}
    for url in sorted(required):
        payload, content_type = fetch(url)
        if url == CHRYSOSTOM_CURRENT_PDF or url.lower().endswith(".pdf"):
            if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                raise ValueError("live source is not a PDF: %s" % url)
            cache[url] = payload
            continue
        if "html" not in content_type and not payload.lstrip().startswith(b"<"):
            raise ValueError("live source is not HTML: %s" % url)
        if url == TRYFON_SITE:
            match = re.search(rb'src=["\']([^"\']+\.js)["\']', payload)
            if not match:
                raise ValueError("Saint Tryphon site lacks its public bundle")
            script_url = urljoin(url, match.group(1).decode("utf-8"))
            script_payload, unused_type = fetch(script_url)
            payload += b" " + script_payload
        cache[url] = normalized_page(payload)

    home = cache[HOME]
    for marker in ("ἔχει 20 Ἐνορίες", "Ἁγ. Σοφίας",
                   "Ἁγ. Παντελεήμονος", "Ζωοδόχου Πηγῆς"):
        if unicase(marker) not in home:
            raise ValueError("Glyfada home page lacks marker: %s" % marker)
    directory_pages = cache[DIRECTORY] + " " + cache[DIRECTORY_PAGE_2]
    for row in ROWS[:24]:
        marker = row["live_markers"][0]
        if unicase(marker) not in directory_pages and row["id"] not in {
            "gr-glyfada-021-life-giving-spring",
            "gr-glyfada-022-trinity-nektarios-monastery",
            "gr-glyfada-023-rose-unfading-hermitage",
        }:
            raise ValueError("directory lacks current body marker: %s" % marker)

    for row in ROWS:
        pages = " ".join(
            cache[url] for url in row["sources"]
            if isinstance(cache[url], str)
        )
        if not pages and row["id"] in BINARY_ONLY_LIVE_IDS:
            continue
        digit_pages = compact_digits(pages)
        for marker in row.get("live_markers") or []:
            if unicase(marker) not in pages:
                raise ValueError("%s lacks live marker %s" %
                                 (row["id"], marker))
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digit_pages:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
        for email in row.get("emails") or []:
            local_part, domain = email.lower().split("@", 1)
            if (unicase(local_part) not in pages or
                    unicase(domain.split(".", 1)[0]) not in pages):
                raise ValueError("%s lacks live email %s" %
                                 (row["id"], email))
    print("Glyfada live sources: %d URLs checked" % len(required))


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
    elif args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Glyfada: 34 exact bodies; 20 regulated parishes, "
              "3 monastic institutions, and 11 exact chapels or "
              "dependent worship bodies")
        print("Contacts: 24 bodies; 28 phones; 23 emails; 9 body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Glyfada: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
