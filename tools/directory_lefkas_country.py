#!/usr/bin/env python3
"""Validate exact current Lefkas and Ithaca worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_lefkas_country.py --check
    python tools/directory_lefkas_country.py --check-live
    python tools/directory_lefkas_country.py --dump
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
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-lefkas"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "lefkas_country.json"
)
REGULATION_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
SPYRIDON_ACT = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2017_aprilios.pdf"
)
PRIESTS = "https://imli.gr/priests/"
MANAGEMENT = "https://imli.gr/management/"
PROFILE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "leukados-kai-ithakes"
)
EVANGELISTRIA_HOME = "https://e-evaggelistria.gr/"
EVANGELISTRIA_CONTACT = "https://e-evaggelistria.gr/epikoinonia/"
SAINT_NICHOLAS_SITE = "https://agiosnikolaoslefkadas.gr/"
VISSARION_CURRENT = (
    "https://imli.gr/uncategorized/o-%cf%80%ce%b1%ce%bd%ce%b7%ce%b3%cf%85%"
    "cf%81%ce%b9%ce%ba%cf%8c%cf%82-%ce%b1%cf%81%cf%87%ce%b9%ce%b5%cf%81%"
    "ce%b1%cf%84%ce%b9%ce%ba%cf%8c%cf%82-%ce%b5%cf%83%cf%80%ce%b5%cf%81%"
    "ce%b9%ce%bd%cf%8c%cf%82-18/"
)
EUTYCHIOS_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%"
    "ce%bc%ce%bc%ce%b1-%ce%b9%ce%b5%cf%81%ce%ac%cf%82-%cf%80%ce%b1%ce%bd%"
    "ce%b7%ce%b3%cf%8d%cf%81%ce%b5%cf%89%cf%82-%ce%b9%ce%b5%cf%81%ce%bf%"
    "cf%8d-%ce%bc%ce%b7%cf%84-5/"
)
SAINT_LUKE_CURRENT = (
    "https://imli.gr/uncategorized/%ce%bf-%cf%80%ce%b1%ce%bd%ce%b7%ce%b3%"
    "cf%85%cf%81%ce%b9%ce%ba%cf%8c%cf%82-%ce%b5%cf%83%cf%80%ce%b5%cf%81%"
    "ce%b9%ce%bd%cf%8c%cf%82-%cf%84%ce%b7%cf%82-%ce%bc%ce%bd%ce%ae%ce%bc%"
    "ce%b7%cf%82-%cf%84%ce%bf-5/"
)
HYPOMONE_CURRENT = (
    "https://imli.gr/uncategorized/%ce%bf-%cf%80%ce%b1%ce%bd%ce%b7%ce%b3%"
    "cf%85%cf%81%ce%b9%ce%ba%cf%8c%cf%82-%ce%b1%cf%81%cf%87%ce%b9%ce%b5%"
    "cf%81%ce%b1%cf%84%ce%b9%ce%ba%cf%8c%cf%82-%ce%b5%cf%83%cf%80%ce%b5%"
    "cf%81%ce%b9%ce%bd%cf%8c-45/"
)
ELEFTHERIOS_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%"
    "ce%bc%ce%bc%ce%b1-%ce%b5%ce%bf%cf%81%cf%84%ce%b1%cf%83%ce%bc%ce%bf%"
    "cf%8d-%ce%b9%ce%b5%cf%81%ce%bf%cf%8d-%cf%80%ce%b1%cf%81%ce%b5%ce%ba%"
    "ce%ba%ce%bb%ce%b7%cf%83-5/"
)
PROPHET_ELIJAH_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%cf%83%ce%ba%ce%bb%"
    "ce%b7%cf%83%ce%b7-%ce%b8%cf%85%cf%81%ce%b1%ce%bd%ce%bf%ce%b9%ce%be%"
    "ce%af%cf%89%ce%bd-%ce%b9%ce%b5%cf%81%ce%bf%cf%8d-%cf%80%ce%b1%cf%81%"
    "ce%b5%ce%ba%ce%ba%ce%bb/"
)
SAINT_NICHOLAS_REMA_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%"
    "ce%bc%ce%bc%ce%b1-%ce%b9%ce%b5%cf%81%ce%ac%cf%82-%cf%80%ce%b1%ce%bd%"
    "ce%b7%ce%b3%cf%8d%cf%81%ce%b5%cf%89%cf%82-%ce%b9%ce%b5%cf%81%ce%bf%"
    "cf%8d-%cf%80%ce%b1%cf%81-3/"
)
ARCHANGEL_CEMETERY_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%"
    "ce%bc%ce%bc%ce%b1-%ce%bc-%ce%b5%ce%b2%ce%b4%ce%bf%ce%bc%ce%ac%ce%b4%"
    "ce%bf%cf%82-%ce%b9%ce%b5%cf%81%ce%bf%cf%8d-%ce%ba%ce%bf%ce%b9%ce%bc%"
    "ce%b7%cf%84%ce%b7%cf%81-2/"
)
MEGANISI_CEMETERY_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%"
    "ce%bc%ce%bc%ce%b1-%ce%b9%ce%b5%cf%81%ce%ac%cf%82-%cf%80%ce%b1%ce%bd%"
    "ce%b7%ce%b3%cf%8d%cf%81%ce%b5%cf%89%cf%82-%ce%b9%ce%b5%cf%81%ce%bf%"
    "cf%8d-%ce%ba%ce%bf%ce%b9-6/"
)
TSOUKALADES_CEMETERY_CURRENT = (
    "https://imli.gr/uncategorized/%cf%80%cf%81%cf%8c%ce%b3%cf%81%ce%b1%"
    "ce%bc%ce%bc%ce%b1-%ce%b9%ce%b5%cf%81%ce%ac%cf%82-%cf%80%ce%b1%ce%bd%"
    "ce%b7%ce%b3%cf%8d%cf%81%ce%b5%cf%89%cf%82-%ce%b9%ce%b5%cf%81%ce%bf%"
    "cf%8d-%ce%ba%ce%bf%ce%b9-4/"
)

# Legal district | English seat | postcode | exact legal identity |
# English dedication | current body-associated public phones.
PARISH_SOURCE = r'''
Lefkada|Lefkada|31100|ΛΕΥΚΑΣ - ΕΥΑΓΓΕΛΙΣΤΡΙΑ|the Annunciation of the Theotokos|2645023246,2645023876,2645022415
Lefkada|Lefkada|31100|ΛΕΥΚΑΣ - ΑΓΙΟΙ ΑΝΑΡΓΥΡΟΙ|Holy Unmercenaries|2645023458,6974152365
Lefkada|Lefkada|31100|ΛΕΥΚΑΣ - ΑΓΙΟΣ ΜΗΝΑΣ|Saints Minas, Victor, and Vincent|2645024945,6944260430,2645023105
Lefkada|Lefkada|31100|ΛΕΥΚΑΣ - ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|Saint Nicholas|2645025410,2645024200
Lefkada|Lefkada|31100|ΛΕΥΚΑΣ - ΓΕΝΕΣΙΟΝ ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos|2645023608,6944140052
Lefkada|Agios Nikitas|31080|ΑΓΙΟΣ ΝΙΚΗΤΑΣ - ΑΓΙΟΣ ΝΙΚΗΤΑΣ|Saint Nikitas|2645025947
Lefkada|Alexandros|31080|ΑΛΕΞΑΝΔΡΟΣ - ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ|Saint Spyridon|2645026496
Lefkada|Apolpaina|31100|ΑΠΟΛΠΑΙΝΑ - ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|Saint Athanasius|2645025221
Lefkada|Kalamitsi|31080|ΚΑΛΑΜΙΤΣΙΟΝ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|6976290811
Lefkada|Kalligoni|31100|ΚΑΛΛΙΓΟΝΙΟΝ - ΑΓΙΑ ΤΡΙΑΣ|Holy Trinity|2645025221
Lefkada|Karyotes|31100|ΚΑΡΥΩΤΑΙ - ΤΑΞΙΑΡΧΑΙ|Holy Archangels|2645026255
Lefkada|Katouna|31100|ΚΑΤΟΥΝΑ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2645071924,2645025763
Lefkada|Nikiana|31100|ΝΙΚΙΑΝΑ - ΜΕΤΑΜΟΡΦΩΣΙΣ ΣΩΤΗΡΟΣ|the Transfiguration of the Savior|2645026496
Lefkada|Tsoukalades|31100|ΤΣΟΥΚΑΛΑΔΕΣ - ΕΙΣΟΔΙΑ ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos|2645025947
Lefkada|Fryni|31100|ΦΡΥΝΙΟΝ - ΑΓΙΟΙ ΑΠΟΣΤΟΛΟΙ|Holy Apostles|2645026255
Lefkada|Episkopi, Kalamos|31081|ΕΠΙΣΚΟΠΗ ΚΑΛΑΜΟΥ - ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|Saint George|6944140052
Lefkada|Kalamos|31081|ΚΑΛΑΜΟΣ - ΑΓΙΑ ΤΡΙΑΣ|Holy Trinity|6984764754
Lefkada|Kastos|31081|ΚΑΣΤΟΣ - ΤΙΜΙΟΣ ΠΡΟΔΡΟΜΟΣ|Saint John the Forerunner|6972818079
Ithaca|Anogi, Ithaca|28301|ΑΝΩΓΗ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2674031555,2674031663
Ithaca|Vathy, Ithaca|28300|ΒΑΘΥ - ΕΙΣΟΔΙΑ ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos|2674033738
Ithaca|Vathy, Ithaca|28300|ΒΑΘΥ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2674032906,2674032066
Ithaca|Vathy, Ithaca|28300|ΒΑΘΥ - ΤΑΞΙΑΡΧΑΙ|Holy Archangels|2674033112
Ithaca|Exogi, Ithaca|28301|ΕΞΩΓΗ - ΑΓΙΑ ΜΑΡΙΝΑ|Saint Marina|6976769899
Ithaca|Kioni, Ithaca|28301|ΚΙΟΝΙΟΝ - ΤΙΜΙΟΣ ΠΡΟΔΡΟΜΟΣ|Saint John the Forerunner|2674031555,2674031663
Ithaca|Lefki, Ithaca|28301|ΛΕΥΚΗ - ΕΙΣΟΔΙΑ ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos|2674033738
Ithaca|Perachori, Ithaca|28300|ΠΕΡΑΧΩΡΙΟΝ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2674033112
Ithaca|Platreithias, Ithaca|28301|ΠΛΑΤΡΕΙΘΙΑΣ - ΤΑΞΙΑΡΧΑΙ|Holy Archangels|2674031663
Ithaca|Stavros, Ithaca|28301|ΣΤΑΥΡΟΣ - ΜΕΤΑΜΟΡΦΩΣΙΣ ΣΩΤΗΡΟΣ|the Transfiguration of the Savior|6976769899
Nydri|Alatro|31084|ΑΛΑΤΡΟΝ - ΥΠΑΠΑΝΤΗ ΚΥΡΙΟΥ|the Presentation of the Lord|2645095087
Nydri|Vafkeri|31080|ΒΑΥΚΕΡΗ - ΑΓΙΟΣ ΙΩΑΝΝΗΣ ΧΡΥΣΟΣΤΟΜΟΣ|Saint John Chrysostom|6981892413,6977153119
Nydri|Vlycho|31084|ΒΛΥΧΟΝ - ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ|Saint Spyridon|2645095228
Nydri|Katochori|31084|ΚΑΤΩΧΩΡΙΟΝ - ΑΓΙΟΣ ΔΗΜΗΤΡΙΟΣ|Saint Demetrius|6947334233
Nydri|Neochori|31084|ΝΕΟΧΩΡΙΟΝ - ΕΙΣΟΔΙΑ ΘΕΟΤΟΚΟΥ|the Entrance of the Theotokos|2645092264
Nydri|Nydri|31084|ΝΥΔΡΙΟΝ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|6972740216
Nydri|Perigiali|31084|ΠΕΡΙΓΙΑΛΙΟΝ - ΕΥΑΓΓΕΛΙΣΤΡΙΑ|the Annunciation of the Theotokos|6972370262
Nydri|Platystoma|31080|ΠΛΑΤΥΣΤΟΜΑ - ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|Saint Paraskevi|6977153119
Nydri|Poros|31082|ΠΟΡΟΣ - ΑΓΙΑ ΜΑΡΙΝΑ|Saint Marina|2645095646
Nydri|Fterno|31082|ΦΤΕΡΝΟΝ - ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|Saint Nicholas|6937334233
Nydri|Charadiatika|31084|ΧΑΡΑΔΙΑΤΙΚΑ - ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|Saint Nicholas|2645095087
Nydri|Vathy, Meganisi|31083|ΒΑΘΥ ΜΕΓΑΝΗΣΙΟΥ - ΑΓΙΟΣ ΒΗΣΣΑΡΙΩΝ|Saint Vissarion|2645023077
Nydri|Katomeri, Meganisi|31083|ΚΑΤΩΜΕΡΙΟΝ ΜΕΓΑΝΗΣΙΟΥ - ΑΓΙΟΙ ΑΠΟΣΤΟΛΟΙ|Holy Apostles|2645051070,2645023077
Nydri|Spartochori, Meganisi|31083|ΣΠΑΡΤΟΧΩΡΙΟΝ ΜΕΓΑΝΗΣΙΟΥ - ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|Saint George|2645051727
Vasiliki|Agios Ilias|31082|ΑΓΙΟΣ ΗΛΙΑΣ - ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|Saint Athanasius|2645071261
Vasiliki|Vasiliki|31082|ΒΑΣΙΛΙΚΗ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2645031283,6944362454
Vasiliki|Vournikas|31082|ΒΟΥΡΝΙΚΑΣ - ΑΓΙΟΣ ΣΤΕΦΑΝΟΣ|Saint Stephen|2645071261
Vasiliki|Evgiros|31082|ΕΥΓΗΡΟΣ - ΑΓΙΟΣ ΒΑΣΙΛΕΙΟΣ|Saint Basil|2645031048,6944362454
Vasiliki|Kontaraina|31082|ΚΟΝΤΑΡΑΙΝΑ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2645025763
Vasiliki|Marantochori|31082|ΜΑΡΑΝΤΟΧΩΡΙΟΝ - ΤΑΞΙΑΡΧΑΙ|Holy Archangels|2645095646
Vasiliki|Syvros|31082|ΣΥΒΡΟΣ - ΓΕΝΕΣΙΟΝ ΘΕΟΤΟΚΟΥ|the Nativity of the Theotokos|2645071261
Agios Petros|Agios Petros|31082|ΑΓΙΟΣ ΠΕΤΡΟΣ - ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ|Saint Athanasius|2645033403
Agios Petros|Agios Petros|31082|ΑΓΙΟΣ ΠΕΤΡΟΣ - ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ ΣΤΟ ΡΟΥΠΑΚΙ|Saint George at Roupaki|2645033403
Agios Petros|Athani|31082|ΑΘΑΝΙΟΝ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2645033151
Agios Petros|Dragano|31082|ΔΡΑΓΑΝΟΝ - ΥΠΑΠΑΝΤΗ ΚΥΡΙΟΥ|the Presentation of the Lord|2645033151
Agios Petros|Komilio|31082|ΚΟΜΗΛΙΟΝ - ΚΟΙΜΗΣΙΣ ΘΕΟΤΟΚΟΥ|the Dormition of the Theotokos|2645033418
Agios Petros|Nikolis|31082|ΝΙΚΟΛΗΣ - ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|Saint George|6976413465
Agios Petros|Chortata|31082|ΧΟΡΤΑΤΑ - ΑΓΙΟΣ ΙΩΑΝΝΗΣ|Saint John|6976290811
Karya|Asprogerakata|31080|ΑΣΠΡΟΓΕΡΑΚΑΤΑ - ΑΓΙΟΣ ΙΩΑΝΝΗΣ ΧΡΥΣΟΣΤΟΜΟΣ|Saint John Chrysostom|2645041325
Karya|Drymon|31080|ΔΡΥΜΩΝ - ΑΓΙΟΣ ΙΩΑΝΝΗΣ ΧΡΥΣΟΣΤΟΜΟΣ|Saint John Chrysostom|6938510564
Karya|Englouvi|31080|ΕΓΚΛΟΥΒΗ - ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|Saint George|2645041325
Karya|Exantheia|31080|ΕΞΑΝΘΕΙΑ - ΑΓΙΟΣ ΣΤΕΦΑΝΟΣ|Saint Stephen|2645099307,2645033418
Karya|Kavallos|31080|ΚΑΒΑΛΛΟΣ - ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ|Saint Nicholas|6976413465
Karya|Karya|31080|ΚΑΡΥΑ - ΑΓΙΑ ΠΑΡΑΣΚΕΥΗ|Saint Paraskevi|6972282301
Karya|Karya|31080|ΚΑΡΥΑ - ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ|Saint Spyridon|2645041115,6938510564
Karya|Lazarata|31080|ΛΑΖΑΡΑΤΑ - ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ|Saint Spyridon|2645061284
Karya|Pigadisanoi|31080|ΠΗΓΑΔΗΣΑΝΟΙ - ΑΓΙΟΙ ΑΝΑΡΓΥΡΟΙ|Holy Unmercenaries|2645041325
Karya|Pinakochori|31080|ΠΙΝΑΚΟΧΩΡΙΟΝ - ΑΓΙΟΣ ΓΕΩΡΓΙΟΣ|Saint George|2645061284
Karya|Spanochori|31080|ΣΠΑΝΟΧΩΡΙΟΝ - ΤΑΞΙΑΡΧΑΙ|Holy Archangels|6932412700,6977153119
'''

# Exact current identity | rank | English name | seat | address parts |
# phones | faxes | emails | identity sources | contact sources.
MONASTERY_SOURCE = r'''
Ἱερά Μονή Ὑπεραγίας Θεοτόκου Πεφανερωμένης Λευκάδος|Monastery|Monastery of the Most Holy Theotokos Pephaneromeni, Lefkada|Lefkada|Monastery of Pephaneromeni;31100;Lefkada;Greece|2645021305|2645021405|fanerome5@otenet.gr|management,profile|management
Ἱερά Μονή Ὑπεραγίας Θεοτόκου Καθαρῶν Ἰθάκης|Monastery|Monastery of the Most Holy Theotokos Katharon, Ithaca|Kathara, Ithaca|Kathara;28300;Ithaca;Greece|2674033460,6979687938,2674031247|||management,profile|management,profile
Ἱερά Μονή Ἁγίου Ἰωάννου Προδρόμου στό Λιβάδι Καρυᾶς|Monastery|Monastery of Saint John the Forerunner at Livadi, Karya|Karya|Livadi;Karya;31080;Lefkada;Greece|6981892413|||management|management
Ἱερά Μονή Ἁγίου Γεωργίου Σκάρων Ἀλεξάνδρου Λευκάδος|Monastery|Monastery of Saint George at Skaroi, Alexandros|Alexandros|Skaroi;Alexandros;31080;Lefkada;Greece|6972818079|||management|management
Ἱερά Μονή Ἁγίου Νικολάου Ἱρᾶς Λευκάδος|Monastery|Monastery of Saint Nicholas of Ira, Lefkada|Ira, Lefkada|Ira;Athani;31082;Lefkada;Greece|2645039108,6981892413|2645039108||management,profile|management
Ἡσυχαστήριον Ἁγίων Πατέρων Ἀλεξάνδρου|Hesychasterion|Hesychasterion of the Holy Fathers, Alexandros|Alexandros|Nikiana;31100;Lefkada;Greece|2645061284,6988501227,6984764754|||management,profile|management
'''

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imli.gr",
    "www.imli.gr",
    "e-evaggelistria.gr",
    "www.e-evaggelistria.gr",
    "agiosnikolaoslefkadas.gr",
    "www.agiosnikolaoslefkadas.gr",
}
EXPECTED_TOTAL = 84
EXPECTED_LEGAL_REGION_COUNTS = {
    "Agios Petros": 7,
    "Ithaca": 10,
    "Karya": 11,
    "Lefkada": 18,
    "Nydri": 14,
    "Vasiliki": 7,
}
EXPECTED_KINDS = {"monastery": 6, "parish": 78}
EXPECTED_RANKS = {
    "Cemetery Church": 3,
    "Chapel": 3,
    "Hesychasterion": 1,
    "Institutional Chapel": 2,
    "Metropolitan Chapel": 1,
    "Metropolitan Church": 2,
    "Monastery": 5,
    "Parish Church": 65,
    "Pilgrimage Church": 2,
}
EXPECTED_PHONE_BODIES = 74
EXPECTED_PHONE_VALUES = 98
EXPECTED_FAX_BODIES = 2
EXPECTED_FAX_VALUES = 2
EXPECTED_EMAIL_BODIES = 1
EXPECTED_EMAIL_VALUES = 1
EXPECTED_SITE_BODIES = 2
EXPECTED_CONTACT_BODIES = 74


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


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
        raise ValueError("%s has an unsupported URL: %s" % (label, value))


def source_urls(value):
    mapping = {"management": MANAGEMENT, "profile": PROFILE}
    return [mapping[item] for item in value.split(",") if item]


def build_rows():
    rows = []
    legal_regions = Counter()
    parish_lines = PARISH_SOURCE.strip().splitlines()
    if len(parish_lines) != 67:
        raise ValueError("expected 67 legal parish source rows")
    for number, raw in enumerate(parish_lines, 1):
        region, seat, postcode, local, dedication, raw_phones = raw.split(
            "|", 5
        )
        legal_regions[region] += 1
        rank = "Metropolitan Church" if number in (1, 20) else "Parish Church"
        sources = [REGULATION_PDF, PRIESTS]
        contact_sources = [PRIESTS]
        address = [seat, postcode, "Greece"]
        site = None
        if number == 1:
            sources.append(EVANGELISTRIA_CONTACT)
            contact_sources.append(EVANGELISTRIA_CONTACT)
            address = [
                "Napoleontos Zampeliou and Mitropoleos",
                "31100",
                "Lefkada",
                "Greece",
            ]
            site = EVANGELISTRIA_HOME
        elif number == 4:
            sources.append(SAINT_NICHOLAS_SITE)
            contact_sources.append(SAINT_NICHOLAS_SITE)
            address = [
                "Kalkani K.",
                "Old Town",
                "31100",
                "Lefkada",
                "Greece",
            ]
            site = SAINT_NICHOLAS_SITE
        row = {
            "id": "gr-lefkas-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s of %s, %s" % (rank, dedication, seat),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": address,
            "phones": raw_phones.split(","),
            "sources": sources,
            "checked": CHECKED,
            "contact_sources": contact_sources,
            "contact_checked": CHECKED,
        }
        if site:
            row["site"] = site
        rows.append(row)
    if dict(sorted(legal_regions.items())) != EXPECTED_LEGAL_REGION_COUNTS:
        raise ValueError("legal district totals drifted: %r" % legal_regions)

    for number, raw in enumerate(MONASTERY_SOURCE.strip().splitlines(), 68):
        (
            local, rank, name, seat, raw_address, raw_phones, raw_faxes,
            raw_emails, raw_sources, raw_contact_sources,
        ) = raw.split("|", 9)
        row = {
            "id": "gr-lefkas-%03d" % number,
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": raw_address.split(";"),
            "phones": raw_phones.split(",") if raw_phones else [],
            "faxes": raw_faxes.split(",") if raw_faxes else [],
            "emails": raw_emails.split(",") if raw_emails else [],
            "sources": source_urls(raw_sources),
            "checked": CHECKED,
            "contact_sources": source_urls(raw_contact_sources),
            "contact_checked": CHECKED,
        }
        rows.append(row)

    rows.extend([
        {
            "id": "gr-lefkas-074",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": "Pilgrimage Church of Saint Vissarion, Lefkada",
            "local": "ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙΟΥ ΒΗΣΣΑΡΙΩΝΟΣ ΛΕΥΚΑΔΟΣ",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Agia Kara", "Lefkada", "Greece"],
            "phones": ["2645024945", "6944260430"],
            "sources": [REGULATION_PDF, PRIESTS, VISSARION_CURRENT],
            "checked": CHECKED,
            "contact_sources": [PRIESTS],
            "contact_checked": CHECKED,
        },
        {
            "id": "gr-lefkas-075",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": "Pilgrimage Church of Saint Spyridon, Lefkada",
            "local": "ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙΟΥ ΣΠΥΡΙΔΩΝΟΣ ΛΕΥΚΑΔΟΣ",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Near the central square", "Lefkada", "Greece"],
            "sources": [REGULATION_PDF, SPYRIDON_ACT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-076",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Metropolitan Chapel",
            "name": "Metropolitan Chapel of Saint Eutychios, Lefkada",
            "local": "Ιερό Μητροπολιτικό Παρεκκλήσιο Αγίου Ευτυχίου Λευκάδος",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Lefkada", "Greece"],
            "sources": [EUTYCHIOS_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-077",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Institutional Chapel",
            "name": "Hospital Chapel of Saint Luke of Simferopol, Lefkada",
            "local": "Ιερό Παρεκκλήσιο Αγίου Λουκά Νοσοκομείου Λευκάδος",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Lefkada General Hospital", "Lefkada", "Greece"],
            "sources": [SAINT_LUKE_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-078",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Chapel",
            "name": "Chapel of Saint Hypomone, Lefkada",
            "local": "Ιερό Παρεκκλήσιο Αγίας Υπομονής Λευκάδος",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Lefkada", "Greece"],
            "sources": [HYPOMONE_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-079",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Institutional Chapel",
            "name": "Chapel of Saint Eleftherios at the Former Hospital, Lefkada",
            "local": "Ιερό Παρεκκλήσιο Αγίου Ελευθερίου πρώην Νοσοκομείου Λευκάδος",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Former Lefkada Hospital", "Lefkada", "Greece"],
            "sources": [ELEFTHERIOS_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-080",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Chapel",
            "name": "Chapel of Prophet Elijah, Katomeri, Meganisi",
            "local": "Ιερό Παρεκκλήσιο Προφήτου Ηλιού Κατωμερίου Μεγανησίου",
            "seat": "Katomeri, Meganisi",
            "country": "GR",
            "address": ["Katomeri", "Meganisi", "Greece"],
            "sources": [PROPHET_ELIJAH_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-081",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Chapel",
            "name": "Chapel of Saint Nicholas at Rema, Karyotes",
            "local": "Ιερό Παρεκκλήσιο Αγίου Νικολάου στο Ρέμα Καρυωτών Λευκάδος",
            "seat": "Karyotes",
            "country": "GR",
            "address": ["Rema", "Karyotes", "Lefkada", "Greece"],
            "sources": [SAINT_NICHOLAS_REMA_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-082",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Cemetery Church",
            "name": "Cemetery Church of Archangel Michael, Lefkada",
            "local": "Ιερός Κοιμητηριακός Ναός Ταξιάρχου Μιχαήλ Λευκάδος",
            "seat": "Lefkada",
            "country": "GR",
            "address": ["Lefkada Cemetery", "Lefkada", "Greece"],
            "sources": [ARCHANGEL_CEMETERY_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-083",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Cemetery Church",
            "name": (
                "Cemetery Church of Saints Constantine and Helen, "
                "Vathy and Katomeri, Meganisi"
            ),
            "local": (
                "Ιερός Κοιμητηριακός Ναός Αγίων Κωνσταντίνου και Ελένης "
                "Βαθέος και Κατωμερίου Μεγανησίου"
            ),
            "seat": "Vathy and Katomeri, Meganisi",
            "country": "GR",
            "address": ["Meganisi", "Greece"],
            "sources": [MEGANISI_CEMETERY_CURRENT],
            "checked": CHECKED,
        },
        {
            "id": "gr-lefkas-084",
            "parent": PARENT,
            "kind": "parish",
            "rank": "Cemetery Church",
            "name": "Cemetery Church of Saint Charalampus, Tsoukalades",
            "local": "Ιερός Κοιμητηριακός Ναός Αγίου Χαραλάμπους Τσουκαλάδων Λευκάδος",
            "seat": "Tsoukalades",
            "country": "GR",
            "address": ["Tsoukalades Cemetery", "Lefkada", "Greece"],
            "sources": [TSOUKALADES_CEMETERY_CURRENT],
            "checked": CHECKED,
        },
    ])
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


LIVE_CHECKS = {
    PRIESTS: {
        "Εὐαγγελίστρια (Μητροπολιτικός)",
        "Κοίμησις Θεοτόκου",
        "Ταξιάρχαι",
        "Ἅγ. Ἰω. Χρυσόστομος",
        "6932412700",
    },
    MANAGEMENT: {
        "Ἐνοριακοί Ναοί: 67",
        "Παρεκκλήσια: 74",
        "Ἐξωκκλήσια: 180",
        "Ναοί Κοιμητηρίων: 36",
        "Προσκυνηματικοί Ναοί: 2",
        "Ὑπεραγίας Θεοτόκου Πεφανερωμένης",
        "Ἡσυχαστήριον Ἁγ. Πατέρων",
        "Διαλελυμμέναι Ἱεραί Μοναί",
    },
    PROFILE: {
        "Φανερωμένης",
        "Υπεραγίας Θεοτόκου Καθαρών",
        "26740-31247",
        "Αγίων Πατέρων Αλεξάνδρου",
    },
    EVANGELISTRIA_HOME: {
        "Ενορία Ευαγγελίστριας Λευκάδας",
    },
    EVANGELISTRIA_CONTACT: {
        "Ιερός Μητροπολιτικός Ναός Ευαγγελίστριας Λευκάδος",
        "Ναπολέοντος Ζαμπελίου",
        "26450.22415",
    },
    SAINT_NICHOLAS_SITE: {
        "Ιερός Ναός Αγίου Νικολάου Λευκάδας",
        "Καλκάνη Κ. Παλαιά Πόλη",
        "2645025410",
    },
    VISSARION_CURRENT: {
        "Ιερό Προσκυνηματικό Ναό του Αγίου Βησσαρίωνος",
        "Αγία Κάρα",
        "14 Σεπτεμβρίου 2026",
    },
    EUTYCHIOS_CURRENT: {
        "Ιερού Μητροπολιτικού Παρεκκλησίου Αγίου Ευτυχίου",
    },
    SAINT_LUKE_CURRENT: {
        "Ιερό Παρεκκλήσιο του Νοσοκομείου Λευκάδος",
        "Αγίου Λουκά",
    },
    HYPOMONE_CURRENT: {
        "Ιερό Παρεκκλήσιο",
        "Αγίας Υπομονής",
        "πόλη της Λευκάδος",
    },
    ELEFTHERIOS_CURRENT: {
        "Παρεκκλησίου Αγίου Ελευθερίου",
        "πρώην Νοσοκομείου Λευκάδος",
    },
    PROPHET_ELIJAH_CURRENT: {
        "Ιερού Παρεκκλησίου Προφήτου Ηλιού Κατωμερίου Μεγανησίου",
        "16 Αυγούστου 2026",
    },
    SAINT_NICHOLAS_REMA_CURRENT: {
        "Ιερού Παρεκκλησίου Αγίου Νικολάου",
        "Καρυωτών Λευκάδος",
    },
    ARCHANGEL_CEMETERY_CURRENT: {
        "Ιερού Κοιμητηριακού Ναού Ταξιάρχου Μιχαήλ Λευκάδος",
    },
    MEGANISI_CEMETERY_CURRENT: {
        "Ιερού Κοιμητηριακού Ναού Αγίων Κωνσταντίνου και Ελένης",
        "Βαθέος και Κατωμερίου Μεγανησίου",
    },
    TSOUKALADES_CEMETERY_CURRENT: {
        "Ιερού Κοιμητηριακού Ναού Αγίου Χαραλάμπους",
        "Τσουκαλάδων Λευκάδος",
    },
}


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Lefkas candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Lefkas candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "regulated_parish_rows": 67,
        "current_monastic_rows": 6,
        "regulated_pilgrimage_rows": 2,
        "current_exact_chapel_rows": 6,
        "current_exact_cemetery_rows": 3,
        "parish_kind_rows": 78,
        "monastery_kind_rows": 6,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "fax_bodies": EXPECTED_FAX_BODIES,
        "public_fax_values": EXPECTED_FAX_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_TOTAL,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Lefkas ledger summary drifted")
    for key in (
            "candidates", "source_reconciliations",
            "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Lefkas ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Lefkas ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    for source in ROWS:
        item = {
            key: value for key, value in source.items()
            if value not in (None, "", [])
        }
        row_id = item.get("id")
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") != PARENT or item.get("country") != "GR":
            raise ValueError("%s has the wrong parent or country" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(value)
               for value in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        sources = list(item.get("sources") or [])
        if not sources or len(sources) > 3:
            raise ValueError("%s lacks valid sources" % row_id)
        for source_url in sources:
            validate_url(source_url, row_id)
        item["sources"] = sources
        item["cite"] = list(sources)
        contact_sources = list(item.get("contact_sources") or [])
        has_contact = bool(
            item.get("phones") or item.get("faxes") or
            item.get("emails") or item.get("site")
        )
        if has_contact:
            if not contact_sources or item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            for phone in (item.get("phones") or []) + (item.get("faxes") or []):
                if not re.fullmatch(r"[26]\d{9}", phone):
                    raise ValueError("%s carries an invalid phone or fax" % row_id)
            for email in item.get("emails") or []:
                if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
                    raise ValueError("%s carries an invalid email" % row_id)
            if item.get("site"):
                validate_url(item["site"], row_id)
            for source_url in contact_sources:
                validate_url(source_url, row_id)
                if source_url not in sources:
                    raise ValueError("contact source is outside identity sources")
        elif contact_sources or "contact_checked" in item:
            raise ValueError(
                "%s carries contact provenance without contact data" % row_id
            )
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Lefkas English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Lefkas rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Lefkas kind totals drifted: %r" % dict(kinds))
    phone_bodies = sum(bool(item.get("phones")) for item in result)
    phone_values = sum(len(item.get("phones") or []) for item in result)
    fax_bodies = sum(bool(item.get("faxes")) for item in result)
    fax_values = sum(len(item.get("faxes") or []) for item in result)
    email_bodies = sum(bool(item.get("emails")) for item in result)
    email_values = sum(len(item.get("emails") or []) for item in result)
    site_bodies = sum(bool(item.get("site")) for item in result)
    contact_bodies = sum(bool(
        item.get("phones") or item.get("faxes") or
        item.get("emails") or item.get("site")
    ) for item in result)
    if (phone_bodies, phone_values) != (
            EXPECTED_PHONE_BODIES, EXPECTED_PHONE_VALUES):
        raise ValueError("Lefkas phone coverage drifted")
    if (fax_bodies, fax_values) != (
            EXPECTED_FAX_BODIES, EXPECTED_FAX_VALUES):
        raise ValueError("Lefkas fax coverage drifted")
    if (email_bodies, email_values, site_bodies, contact_bodies) != (
            EXPECTED_EMAIL_BODIES, EXPECTED_EMAIL_VALUES,
            EXPECTED_SITE_BODIES, EXPECTED_CONTACT_BODIES):
        raise ValueError("Lefkas contact coverage drifted")
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    }
    if url in (REGULATION_PDF, SPYRIDON_ACT):
        headers["Range"] = "bytes=0-4095"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=90) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return unicase(" ".join(text.split()))


def check_live():
    checks = dict(LIVE_CHECKS)
    checks[REGULATION_PDF] = set()
    checks[SPYRIDON_ACT] = set()

    def one(item):
        url, markers = item
        payload, content_type = fetch(url)
        if url in (REGULATION_PDF, SPYRIDON_ACT):
            if "pdf" not in content_type and not payload.startswith(b"%PDF"):
                raise ValueError("Lefkas legal source is not a PDF: %s" % url)
            return url
        if "html" not in content_type:
            raise ValueError("non-HTML Lefkas source: %s" % url)
        page = normalized_page(payload)
        missing = [marker for marker in markers
                   if unicase(" ".join(marker.split())) not in page]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        return url

    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(one, checks.items()))
    return len(checks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        data = build()
        if args.check_live:
            checked = check_live()
            print("Lefkas live checks passed for %d source pages" % checked)
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Lefkas checks passed: %d bodies, %d phone bodies, "
                "%d email bodies, %d body sites" % (
                    len(rows),
                    sum(bool(item.get("phones")) for item in rows),
                    sum(bool(item.get("emails")) for item in rows),
                    sum(bool(item.get("site")) for item in rows),
                )
            )
    except Exception as exc:
        print("Lefkas check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
