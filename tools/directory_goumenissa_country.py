#!/usr/bin/env python3
"""Validate exact named Goumenissa bodies from first-party sources.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_goumenissa_country.py --check
    python tools/directory_goumenissa_country.py --check-live
    python tools/directory_goumenissa_country.py --dump
"""

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


CHECKED = "2026-11-15"
PARENT = "ep-goumenissa"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates"
    / "goumenissa_country.json"
)

ROSTER_URL = "https://www.imgap.gr/file1/dhioik.html"
MONASTERIES_URL = "https://www.imgap.gr/file1/mones.html"
PANAGIA_PDF_URL = "https://www.imgap.gr/file1/PanagiaGoumenissa.pdf"
RAPHAEL_LEGACY_URL = "https://www.imgap.gr/file1/imagraf.html"
ANYDROS_URL = "https://www.imgap.gr/file1/anydhro.html"
EP_URL = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-goymenissis-aksioypoleos-polykastrou/"
)
COG_URL = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/goumenisses-axioupoleos-kai-polykastrou"
)
RAPHAEL_SITE = "https://www.moni-agiou-rafail.gr/"
RAPHAEL_CONTACT_URL = (
    "https://www.moni-agiou-rafail.gr/en/contact-en"
)
RAPHAEL_CHAPELS_URL = (
    "https://www.moni-agiou-rafail.gr/the-monastery/"
    "parekklisia-ksenones-topothesia"
)
RAPHAEL_SERVICES_URL = (
    "https://www.moni-agiou-rafail.gr/9-general/"
    "78-leitourgiko-programma"
)


# key|English seat|Greek seat|postal code|English dedication|Greek dedication|
# exact displayed source phrase|fixed phone printed on the church line
PARISH_SOURCE = r"""
goumenissa-george|Goumenissa|Γουμένισσα|613 00|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|23430-41298
axioupoli-demetrius|Axioupoli|Αξιούπολη|614 00|Saint Demetrius|Αγίου Δημητρίου|Ι. Ναός Αγ. Δημητρίου|23430-32540
axioupoli-axion-estin|Axioupoli|Αξιούπολη|614 00|Panagia Axion Estin|Παναγίας Άξιον Εστίν|Ι. Ναός Παναγίας Άξιον Εστίν|23430-31955
polykastro-holy-trinity|Polykastro|Πολύκαστρο|612 00|Holy Trinity|Αγίας Τριάδος|Ι. Ναός Αγ. Τριάδος|23430-22227
polykastro-athanasius|Polykastro|Πολύκαστρο|612 00|Saint Athanasius|Αγίου Αθανασίου|Ι. Ναός Αγ. Αθανασίου|23430-24498
agios-petros-peter-paul|Agios Petros|Άγιος Πέτρος|610 07|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Ι. Ναός Αγ. Πέτρου & Παύλου|
akropotamos-dormition|Akropotamos|Ακροπόταμος|570 11|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ναός Κοιμήσεως της Θεοτόκου|2310-711520
axiochori-transfiguration|Axiochori|Αξιοχώρι|612 00|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Ι. Ναός Μεταμορφώσεως του Σωτήρος|23430-95459
aspros-john-theologian|Aspros|Άσπρος|612 00|Saint John the Theologian|Αγίου Ιωάννου Θεολόγου|Ι. Ναός Αγ. Ιωάννου Θεολόγου|23430-95495
valtotopi-constantine|Valtotopi|Βαλτοτόπι|614 00|Saint Constantine|Αγίου Κωνσταντίνου|Ι. Ναοί Αγ. Κωνσταντίνου & Υψώσεως Τιμίου Σταυρού|
valtotopi-exaltation-cross|Valtotopi|Βαλτοτόπι|614 00|Exaltation of the Holy Cross|Υψώσεως Τιμίου Σταυρού|Ι. Ναοί Αγ. Κωνσταντίνου & Υψώσεως Τιμίου Σταυρού|
gerakona-archangels|Gerakona|Γερακώνα|613 00|Holy Archangels|Αγίων Αρχαγγέλων|Ι. Ναός Αγ. Αρχαγγέλων|
gefyra-rheumatokratoussa|Gefyra|Γέφυρα|570 11|Panagia Rheumatokratoussa|Παναγίας Ρευματοκρατούσης|Ι. Ναός Παναγίας Ρευματοκρατούσης|2310-715442
kato-gefyra-george|Kato Gefyra|Κάτω Γέφυρα|570 11|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|2310-716098
gorgopi-nicholas|Gorgopi|Γοργόπη|614 00|Saint Nicholas|Αγίου Νικολάου|Ι. Ναός Αγ. Νικολάου|23430-32003
griva-athanasius|Griva|Γρίβα|613 00|Saint Athanasius|Αγίου Αθανασίου|Ι. Ναός Αγ. Αθανασίου|23430-43111
doganis-demetrius|Doganis|Δογάνης|614 00|Saint Demetrius|Αγίου Δημητρίου|Ι. Ναός Αγ. Δημητρίου|
eidomeni-nativity-theotokos|Eidomeni|Ειδομένη|614 00|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Ι. Ναός Γενεσίου της Θεοτόκου|
eiriniko-paraskevi|Eiriniko|Ειρηνικό|612 00|Saint Paraskevi|Αγίας Παρασκευής|Ι. Ναός Αγ. Παρασκευής|
evzoni-dormition|Evzoni|Εύζωνοι|612 00|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ναός Κοιμήσεως της Θεοτόκου|23430-51005
evropos-george|Evropos|Εύρωπος|610 07|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|23430-61237
kampochori-george|Kampochori|Καμποχώρι|614 00|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|
karpi-athanasius|Karpi|Κάρπη|613 00|Saint Athanasius|Αγίου Αθανασίου|Ι. Ναός Αγ. Αθανασίου|23430-43381
kastanas-george|Kastanas|Καστανάς|570 11|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|2310-711255
kastaneri-paraskevi|Kastaneri|Καστανερή|613 00|Saint Paraskevi|Αγίας Παρασκευής|Ι. Ναός Αγ. Παρασκευής|
korona-holy-apostles|Korona|Κορώνα|612 00|Holy Apostles Peter and Paul|Αγίων Αποστόλων Πέτρου και Παύλου|Ι. Ναός Αγ. Αποστόλων Πέτρου και Παύλου|
koupa-dormition|Koupa|Κούπα|614 00|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ναός Κοιμήσεως της Θεοτόκου|23430-91250
livadia-nicholas|Livadia|Λιβάδια|614 00|Saint Nicholas|Αγίου Νικολάου|Ι. Ναός Αγ. Νικολάου|
limnotopos-george|Limnotopos|Λιμνότοπος|612 00|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|
mesia-constantine-helen|Mesia|Μεσιά|610 07|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι. Ναός Αγ. Κωνσταντίνου και Ελένης|
metamorfosi-transfiguration|Metamorfosi|Μεταμόρφωση|612 00|Transfiguration of the Savior|Μεταμορφώσεως του Σωτήρος|Ι. Ναός Μεταμορφώσεως του Σωτήρος|
mikro-dasos-archangels|Mikro Dasos|Μικρό Δάσος|612 00|All-Holy Archangels|Παμμεγίστων Ταξιαρχών|Ι. Ναός Παμμεγίστων Ταξιαρχών|23430-51303
nea-kavala-paraskevi|Nea Kavala|Νέα Καβάλα|612 00|Saint Paraskevi|Αγίας Παρασκευής|Ι. Ναός Αγ. Παρασκευής|
omalo-nativity-theotokos|Omalo|Ομαλό|613 00|Nativity of the Theotokos|Γενεσίου της Θεοτόκου|Ι. Ναός Γενεσίου της Θεοτόκου|
pentalofos-peter-paul|Pentalofos|Πεντάλοφος|613 00|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Ι. Ναός Αγ. Πέτρου και Παύλου|
pefkodasos-george|Pefkodasos|Πευκόδασος|612 00|Saint George|Αγίου Γεωργίου|Ι. Ναός Αγ. Γεωργίου|23430-23113
pigi-prophet-elijah|Pigi|Πηγή|614 00|Prophet Elijah|Προφήτου Ηλιού|Ι. Ναός Προφήτου Ηλιού|
plagia-paraskevi|Plagia|Πλάγια|614 00|Saint Paraskevi|Αγίας Παρασκευής|Ι. Ναός Αγ. Παρασκευής|23430-91270
platania-constantine-helen|Platania|Πλατανιά|612 00|Saints Constantine and Helen|Αγίων Κωνσταντίνου και Ελένης|Ι. Ναός Αγ. Κωνσταντίνου και Ελένης|23430-92404
polypetro-demetrius|Polypetro|Πολύπετρο|610 07|Saint Demetrius|Αγίου Δημητρίου|Ι. Ναός Αγ. Δημητρίου|23430-62395
pontoirakleia-prophet-elijah|Pontoirakleia|Ποντοηράκλεια|612 00|Prophet Elijah|Προφήτου Ηλιού|Ι. Ναός Προφήτου Ηλιού|23430-92052
prochoma-exaltation-cross|Prochoma|Πρόχωμα|570 11|Exaltation of the Holy Cross|Υψώσεως Τιμίου Σταυρού|Ι. Ναός Υψώσεως Τιμίου Σταυρού|2310-711923
rizia-dormition|Rizia|Ρίζια|614 00|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ναός Κοιμήσεως της Θεοτόκου|23430-71537,23430-71107
sitaria-dormition|Sitaria|Σιταριά|612 00|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ναός Κοιμήσεως της Θεοτόκου|
skra-demetrius|Skra|Σκρά|614 00|Saint Demetrius|Αγίου Δημητρίου|Ι. Ναός Αγ. Δημητρίου|23430-25128
stathis-peter-paul|Stathis|Στάθης|614 00|Saints Peter and Paul|Αγίων Πέτρου και Παύλου|Ι. Ναός Αγ. Πέτρου και Παύλου|23430-32291
toumba-athanasius|Toumba|Τούμπα|614 00|Saint Athanasius|Αγίου Αθανασίου|Ι. Ναοί Αγ. Αθανασίου & Κοιμ. Θεοτόκου|23430-71710
toumba-dormition|Toumba|Τούμπα|614 00|Dormition of the Theotokos|Κοιμήσεως της Θεοτόκου|Ι. Ναοί Αγ. Αθανασίου & Κοιμ. Θεοτόκου|23430-71710
fanos-john-forerunner|Fanos|Φανός|614 00|Saint John the Forerunner|Αγίου Ιωάννου Προδρόμου|Ι. Ναός Αγ. Ιωάννου Προδρόμου|
filyria-life-giving-spring|Filyria|Φιλυριά|613 00|Life-Giving Spring|Ζωοδόχου Πηγής|Ι. Ναοί Ζωοδόχου Πηγής & Αγ. Κυριακής|
filyria-kyriaki|Filyria|Φιλυριά|613 00|Saint Kyriaki|Αγίας Κυριακής|Ι. Ναοί Ζωοδόχου Πηγής & Αγ. Κυριακής|
chamilo-exaltation-cross|Chamilo|Χαμηλό|614 00|Exaltation of the Holy Cross|Υψώσεως Τιμίου Σταυρού|Ι. Ναός Υψώσεως Τιμίου Σταυρού|
"""


# The official roster groups each church with its assigned clergy contacts.
# These are public directory routes associated with the church. They are not
# all represented as church office lines, and no clergy name is copied.
PUBLIC_ASSOCIATED_PHONES = json.loads(r'''{
  "goumenissa-george": ["23430-41298", "6976837126", "23430-41259", "6945676138", "6979867991", "6972206307"],
  "axioupoli-demetrius": ["23430-32540", "23430-32710", "6937148808", "6982565256"],
  "axioupoli-axion-estin": ["23430-31955", "23430-32710", "6937148808", "6982565256"],
  "polykastro-holy-trinity": ["23430-22227", "23437-70009", "6982337441", "6944761853", "6942087268", "6989092619"],
  "polykastro-athanasius": ["23430-24498", "23430-23719", "6948133495"],
  "agios-petros-peter-paul": ["6946482417"],
  "akropotamos-dormition": ["2310-711520", "6999711711"],
  "axiochori-transfiguration": ["23430-95459", "23410-61009", "6976418962"],
  "aspros-john-theologian": ["23430-95495", "23430-95412", "6932546930"],
  "valtotopi-constantine": ["6985924568"],
  "valtotopi-exaltation-cross": ["6985924568"],
  "gerakona-archangels": ["6937149770"],
  "gefyra-rheumatokratoussa": ["2310-715442", "2310-715763", "6947290408"],
  "kato-gefyra-george": ["2310-716098", "6932652812"],
  "gorgopi-nicholas": ["23430-32003", "23430-32212", "6972849552"],
  "griva-athanasius": ["23430-43111", "6972370196"],
  "doganis-demetrius": ["6984388753"],
  "eidomeni-nativity-theotokos": ["6944837649"],
  "eiriniko-paraskevi": ["23411-02811", "6981710601"],
  "evzoni-dormition": ["23430-51005", "6974435508"],
  "evropos-george": ["23430-61237", "23430-61039", "6945499603", "6996844502"],
  "kampochori-george": ["23430-42231"],
  "karpi-athanasius": ["23430-43381", "2310-609382", "6933356891"],
  "kastanas-george": ["2310-711255", "6936400470"],
  "kastaneri-paraskevi": ["6972364813"],
  "korona-holy-apostles": ["23411-02811", "6981710601"],
  "koupa-dormition": ["23430-91250", "6946833773"],
  "livadia-nicholas": ["23430-24486", "6946522727"],
  "limnotopos-george": ["6947427262"],
  "mesia-constantine-helen": ["2310-760554", "6971729618"],
  "metamorfosi-transfiguration": ["23430-24486", "6946522727"],
  "mikro-dasos-archangels": ["23430-51303", "6940829055"],
  "nea-kavala-paraskevi": ["23410-42208", "6981818693"],
  "omalo-nativity-theotokos": ["6972582568"],
  "pentalofos-peter-paul": ["6972259091"],
  "pefkodasos-george": ["23430-23113", "6947569209"],
  "pigi-prophet-elijah": ["6979928374"],
  "plagia-paraskevi": ["23430-91270", "23430-91158", "6974646979"],
  "platania-constantine-helen": ["23430-92404", "23430-32533", "6939543772"],
  "polypetro-demetrius": ["23430-62395", "6947759343"],
  "pontoirakleia-prophet-elijah": ["23430-92052", "6983449108"],
  "prochoma-exaltation-cross": ["2310-711923", "6977493617"],
  "rizia-dormition": ["23430-71537", "23430-71107", "6974641086", "6970854250"],
  "sitaria-dormition": ["6949070168"],
  "skra-demetrius": ["23430-25128", "23430-32705", "6979602774"],
  "stathis-peter-paul": ["23430-32291", "23430-32317", "6974708695"],
  "toumba-athanasius": ["23430-71710", "23430-23278", "6974248235"],
  "toumba-dormition": ["23430-71710", "23430-23278", "6974248235"],
  "fanos-john-forerunner": ["6942087204"],
  "filyria-life-giving-spring": ["23910-91454", "6937768349"],
  "filyria-kyriaki": ["23910-91454", "6937768349"],
  "chamilo-exaltation-cross": ["6946037940"]
}''')


def parse_parishes():
    rows = []
    markers = {}
    for number, raw in enumerate(
            (line for line in PARISH_SOURCE.splitlines() if line.strip()), 1):
        parts = raw.split("|")
        if len(parts) != 8:
            raise ValueError("invalid Goumenissa parish source row: %s" % raw)
        (key, seat, seat_local, postal, dedication, dedication_local,
         source_phrase, phones_text) = parts
        row_id = "gr-ep-goumenissa-%03d-%s" % (number, key)
        item = {
            "id": row_id,
            "parent": PARENT,
            "kind": "parish",
            "rank": "Parish Church",
            "name": "%s Parish Church in %s" % (dedication, seat),
            "local": "Ιερός Ναός %s, %s" % (
                dedication_local, seat_local
            ),
            "seat": seat,
            "country": "GR",
            "address": ["%s, Τ.Κ. %s" % (seat_local, postal)],
            "sources": [ROSTER_URL],
        }
        body_line_phones = [
            value for value in phones_text.split(",") if value
        ]
        phones = list(PUBLIC_ASSOCIATED_PHONES.get(key) or [])
        if not phones or any(value not in phones for value in body_line_phones):
            raise ValueError(
                "%s loses a body-line phone or directory contact" % key
            )
        if phones:
            item["phones"] = phones
            item["contact_sources"] = [ROSTER_URL]
            item["contact_checked"] = CHECKED
        rows.append(item)
        markers[row_id] = [seat_local, source_phrase]
    return rows, markers


ROWS, LIVE_MARKERS = parse_parishes()


def add_row(item, markers):
    ROWS.append(item)
    LIVE_MARKERS[item["id"]] = markers


add_row({
    "id": "gr-ep-goumenissa-053-panagia-goumenissa-monastery",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Panagia Goumenissa Monastery",
    "local": "Ιερά Μονή Παναγίας Γουμένισσης",
    "seat": "Goumenissa",
    "country": "GR",
    "address": ["613 00 Γουμένισσα"],
    "phones": ["23430-43333", "6984388753"],
    "sources": [PANAGIA_PDF_URL, EP_URL, COG_URL],
    "contact_sources": [EP_URL, COG_URL],
    "contact_checked": CHECKED,
}, ["Ιερά Μονή Παναγίας Γουμενίσσης"])

add_row({
    "id": "gr-ep-goumenissa-054-saints-raphael-nicholas-irene-monastery",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Holy Monastery of Saints Raphael, Nicholas and Irene",
    "local": "Ιερά Μονή Αγίων Ραφαήλ, Νικολάου και Ειρήνης",
    "seat": "Griva",
    "country": "GR",
    "address": ["Γρίβα, 613 00 Γουμένισσα"],
    "phones": ["23430-42231", "23430-20270"],
    "emails": ["agiosrafailgriva@gmail.com"],
    "site": RAPHAEL_SITE,
    "sources": [EP_URL, RAPHAEL_SITE, RAPHAEL_CONTACT_URL],
    "contact_sources": [EP_URL, RAPHAEL_CONTACT_URL],
    "contact_checked": CHECKED,
}, ["Holy Monastery of Saints Raphael, Nicholas and Irene"])

add_row({
    "id": "gr-ep-goumenissa-055-saint-george-panagia-paramythia-hermitage",
    "parent": PARENT,
    "kind": "monastery",
    "rank": "Hermitage",
    "name": "Saint George and Panagia Paramythia Hermitage at Anydros",
    "local": "Ιερό Ησυχαστήριο Αγίου Γεωργίου και Παναγίας Παραμυθίας Ανύδρου",
    "seat": "Anydros",
    "country": "GR",
    "address": ["Τ.Θ. 179, 581 00 Γιαννιτσά"],
    "phones": ["23820-29899", "6987960848"],
    "sources": [ANYDROS_URL, EP_URL, COG_URL],
    "contact_sources": [EP_URL, COG_URL],
    "contact_checked": CHECKED,
}, ["Ησυχαστήριον Αγίου Γεωργίου Ανύδρου"])

RAPHAEL_ADDRESS = ["Γρίβα, 613 00 Γουμένισσα"]
ANYDROS_ADDRESS = ["Τ.Θ. 179, 581 00 Γιαννιτσά"]

for suffix, name, local, rank, markers in [
    (
        "saints-raphael-nicholas-irene-monastic-church",
        "Saints Raphael, Nicholas and Irene Monastic Church",
        "Καθολικό Αγίων Ραφαήλ, Νικολάου και Ειρήνης",
        "Monastic Church",
        ["Το Καθολικό", "Ναός", "Αγίων Ραφαήλ, Νικολάου και Ειρήνης"],
    ),
    (
        "myrrhbearers-burial-attendants-chapel",
        "Myrrhbearers and Burial Attendants of the Lord Monastery Chapel",
        "Παρεκκλήσιο Μυροφόρων και Κηδευτών του Κυρίου",
        "Monastery Chapel",
        ["παρεκκλήσι", "Μυροφόρων και των Κηδευτών του Κυρίου"],
    ),
    (
        "basil-the-great-chapel",
        "Saint Basil the Great Monastery Chapel",
        "Παρεκκλήσιο Μεγάλου Βασιλείου",
        "Monastery Chapel",
        ["παρεκκλήσι του Μεγάλου Βασιλείου"],
    ),
    (
        "apostles-peter-paul-chapel",
        "Holy Apostles Peter and Paul Monastery Chapel",
        "Παρεκκλήσιο Αγίων Αποστόλων Πέτρου και Παύλου",
        "Monastery Chapel",
        ["Παρεκκλήσιό τους", "αγίων αποστόλων Πέτρου και Παύλου"],
    ),
    (
        "apostle-andrew-chapel",
        "Apostle Andrew Monastery Chapel",
        "Παρεκκλήσιο Αγίου Αποστόλου Ανδρέου",
        "Monastery Chapel",
        ["Παρεκκλήσιο", "αγίου αποστόλου Ανδρέου"],
    ),
]:
    row_number = len(ROWS) + 1
    add_row({
        "id": "gr-ep-goumenissa-%03d-%s" % (row_number, suffix),
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name + " at the Holy Monastery in Griva",
        "local": local,
        "seat": "Griva",
        "country": "GR",
        "address": list(RAPHAEL_ADDRESS),
        "sources": [RAPHAEL_CHAPELS_URL, RAPHAEL_SERVICES_URL],
    }, markers)

add_row({
    "id": "gr-ep-goumenissa-061-saint-george-monastic-church-anydros",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Monastic Church",
    "name": "Saint George Monastic Church at Anydros Hermitage",
    "local": "Ναός Αγίου Γεωργίου Ανύδρου",
    "seat": "Anydros",
    "country": "GR",
    "address": list(ANYDROS_ADDRESS),
    "sources": [ANYDROS_URL],
}, ["παλαιά εκκλησία", "ναός του Αγίου Γεωργίου"])

add_row({
    "id": "gr-ep-goumenissa-062-panagia-paramythia-katholikon-anydros",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Monastic Church",
    "name": "Panagia Paramythia Katholikon at Anydros Hermitage",
    "local": "Καθολικό Παναγίας Παραμυθίας Ανύδρου",
    "seat": "Anydros",
    "country": "GR",
    "address": list(ANYDROS_ADDRESS),
    "sources": [ANYDROS_URL],
}, ["καθολικό", "Παναγίας Παραμυθίας"])

add_row({
    "id": "gr-ep-goumenissa-063-saint-sabbas-hospital-church-goumenissa",
    "parent": PARENT,
    "kind": "parish",
    "rank": "Hospital Church",
    "name": "Saint Sabbas Hospital Church in Goumenissa",
    "local": "Νοσοκομειακός Ναός Αγίου Σάββα",
    "seat": "Goumenissa",
    "country": "GR",
    "sources": [EP_URL],
}, ["Νοσοκομειακός Ναός Αγίου Σάββα"])


ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 63
EXPECTED_OWNER_COUNTS = {PARENT: 63}
EXPECTED_KINDS = {"monastery": 3, "parish": 60}
EXPECTED_RANKS = {
    "Hermitage": 1,
    "Hospital Church": 1,
    "Monastery": 2,
    "Monastery Chapel": 4,
    "Monastic Church": 3,
    "Parish Church": 52,
}
EXPECTED_CONTACT_BODIES = 55
EXPECTED_PHONE_BODIES = 55
EXPECTED_PHONE_VALUES = 123
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 62
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
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in {
            "www.imgap.gr", "ec-patr.org", "www.ecclesiagreece.gr",
            "www.moni-agiou-rafail.gr"}:
        raise ValueError(
            "%s carries a non-competent source: %s" % (label, value)
        )


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
        if item["site"] not in sources:
            raise ValueError("%s body-owned site lacks provenance"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Goumenissa candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Goumenissa candidate ledger date drifted")
    expected_summary = {
        PARENT: 63,
        "total": 63,
        "displayed_parish_roster_lines": 49,
        "exact_parish_church_bodies": 52,
        "parish_kind_rows": 60,
        "monastery_kind_rows": 3,
        "contact_bodies": 55,
        "phone_bodies": 55,
        "public_phone_values": 123,
        "email_bodies": 1,
        "public_email_values": 1,
        "body_owned_sites": 1,
        "address_bodies": 62,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Goumenissa ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Goumenissa ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Goumenissa ledger item has invalid sources")
            for source_url in sources:
                validate_url(
                    source_url, entry.get("candidate_id") or key
                )
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Goumenissa ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Goumenissa ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Goumenissa candidate ledger has forbidden punctuation")
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
        raise ValueError("Goumenissa English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Goumenissa English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Goumenissa parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Goumenissa kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Goumenissa rank totals drifted: %r"
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
        raise ValueError("Goumenissa contact coverage drifted: %r"
                         % (coverage,))
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
    for url in all_source_urls():
        try:
            request = Request(url, headers={
                "User-Agent": "Mozilla/5.0 Plithos directory source audit",
                "Connection": "close",
            })
            with urlopen(request, timeout=40) as response:
                if response.status >= 400:
                    failures.append((url, "HTTP %s" % response.status))
                    continue
                content_type = response.headers.get("Content-Type", "").lower()
                payload = response.read()
                if "pdf" in content_type:
                    if not payload.startswith(b"%PDF"):
                        failures.append((url, "invalid PDF payload"))
                    continue
                if "html" not in content_type:
                    failures.append((url, "unexpected content type %s" % content_type))
                    continue
                encoding = "windows-1253" if "imgap.gr" in url else "utf-8"
                source_texts[url] = normalize_source_text(
                    payload.decode(encoding, "replace")
                )
        except Exception as exc:
            failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join("%s [%s]" % pair for pair in failures)
        raise ValueError("live Goumenissa source check failed: %s" % rendered)
    marker_failures = []
    for row in ROWS:
        markers = [normalize_source_text(value)
                   for value in LIVE_MARKERS[row["id"]]]
        if not any(
            all(marker in source_texts.get(url, "") for marker in markers)
            for url in row["sources"]
        ):
            marker_failures.append((row["id"], LIVE_MARKERS[row["id"]]))
    if marker_failures:
        raise ValueError(
            "live Goumenissa exact-source marker check failed: %r"
            % marker_failures
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
            "Goumenissa: %d exact named bodies; %d carry current "
            "public body-associated contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Goumenissa: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
