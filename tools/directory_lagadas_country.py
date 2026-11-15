#!/usr/bin/env python3
"""Validate exact named Lagadas bodies from current first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_lagadas_country.py --check
    python tools/directory_lagadas_country.py --dump
    python tools/directory_lagadas_country.py --check-live
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
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "lagadas_country.json"
)
PARENT = "ep-lagadas"
ROSTER_PAGE = (
    "https://www.imlagada.gr/"
    "%CE%95%CE%BD%CE%BF%CF%81%CE%AF%CE%B5%CF%82.aspx"
)
MONASTERY_PAGE = (
    "https://www.imlagada.gr/"
    "%CE%9C%CE%BF%CE%BD%CE%AD%CF%82.aspx"
)
CHAPEL_PAGE = "https://www.imlagada.gr/default.aspx?catid=81"
PILGRIMAGE_PAGE = "https://www.imlagada.gr/default.aspx?catid=234"
INSTITUTIONAL_PAGE = "https://www.imlagada.gr/default.aspx?catid=235"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-lagkada-litis-rentinis/"
)


PARISH_GROUPS = [
    {
        "key": "lagadas",
        "url": "https://www.imlagada.gr/default.aspx?pageid=53",
        "rows": r'''
Ι.Ν.Ἁγίας Παρασκευής|Saint Paraskevi|Lagadas|Λαγκαδᾶς|572 00|23940 22313|Metropolitan Cathedral
Ι.Ν. Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos|Lagadas|Λαγκαδᾶς|572 00|23940 22582|Parish Church
Ι.Ν.Ἁγ. Παντελεήμονος|Saint Panteleimon|Lagadas|Λαγκαδᾶς|572 00||Parish Church
Ι.Ν. Μεταμ. Σωτήρος|Transfiguration of the Savior|Lagadas|Λαγκαδᾶς|572 00||Parish Church
Ι.Ν. Κοιμήσεως τῆς Θεοτόκου|Dormition of the Theotokos|Perivolaki|Περιβολάκιον|572 00|23940 23639|Parish Church
Ι.Ν. Ἁγ. Νεκταρίου|Saint Nectarios|Kavallari|Καβαλλάριον|572 00|6972636115|Parish Church
Ι.Ν. Ἁγ. Ἀθανασίου|Saint Athanasius|Kavallari|Καβαλάρι|572 00|6972636115|Parish Church
Ι.Ν. Ἁγ. Ἀθανασίου|Saint Athanasius|Irakleio|Ἡράκλειον|572 00|23940 25305|Parish Church
''',
    },
    {
        "key": "assyros",
        "url": "https://www.imlagada.gr/default.aspx?pageid=56",
        "rows": r'''
Ι.Ν. Αγίου Κωνσταντίνου & Ελένης Ἀσσήρου|Saints Constantine and Helen|Assyros|Άσσηρος|572 00|23940 61647|Parish Church
Ι.Ν. Προφήτου Ἡλιοῦ Άσσήρου|Prophet Elijah|Assyros|Άσσηρος|572 00||Parish Church
Ι.Ν. Αγ. Γεωργίου Ξυλουπόλεως|Saint George|Xylopoli|Ξυλόπολις|570 17|23940 93244|Parish Church
Ι.Ν. Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Krithea|Κριθέα|572 00|23940 54029|Parish Church
Ι.Ν. Αγ. Γεωργίου Ἐξαμηλίου|Saint George|Examilio|Εξαμἠλιον|572 00||Parish Church
Ι.Ν. Προφήτου Ηλιού Νικοπόλεως|Prophet Elijah|Nikopoli|Νικόπολις|||Parish Church
Ι.Ν. Αγ. Γεωργίου Μαυροράχης|Saint George|Mavrorachi|Μαυροράχη|570 17||Parish Church
''',
    },
    {
        "key": "kolchiko",
        "url": "https://www.imlagada.gr/default.aspx?pageid=2646",
        "rows": r'''
Ι.Ν. Αγ. Κυριακής Κολχικού|Saint Kyriaki|Kolchiko|Κολχικόν|||Parish Church
Ι.Ν. Αγ. Παρασκευής Κολχικού|Saint Paraskevi|Kolchiko|Κολχικόν|572 00|23940 41429|Parish Church
Ι.Ν. Αγ. Αθανασίου Σχολαρίου|Saint Athanasius|Scholari|Σχολάρι|572 00|6976 719448|Parish Church
Ι.Ν. Μεταμορφώσεως του Σωτήρος Δρακοντίου|Transfiguration of the Savior|Drakontio|Δρακόντιο|572 00|6947150453|Parish Church
Ι.Ν. Αγ. Αθανασίου Εὐαγγελισμού|Saint Athanasius|Evangelismos|Ευαγγελισμός|572 00|23940 55161|Parish Church
Ι.Ν. Αγίου Δημητρίου Ἀναλήψεως|Saint Demetrius|Analipsi|Ανάληψη|572 00|6974 994028|Parish Church
Ι.Ν. Αγίου Δημητρίου Χρυσαυγής|Saint Demetrius|Chrysavgi|Χρυσαυγή|57200|23940 22350|Parish Church
''',
    },
    {
        "key": "lagyna",
        "url": "https://www.imlagada.gr/default.aspx?pageid=57",
        "rows": r'''
Ι.Ν. Αγίου Νικολάου Λαγυνών|Saint Nicholas|Lagyna|Λαγυνά|572 00|23940 71036|Parish Church
Ι.Ν. Αγ.Νικολάου, Ραφαήλ και Ειρήνης Λαγυνών|Saints Nicholas, Raphael, and Irene|Lagyna|Λαγυνά|572 00||Parish Church
Ι.Ν. Αγ. Παντελεήμονος Λαγκαδικίων|Saint Panteleimon|Lagkadikia|Λαγκαδίκια|570 20|23930 23311|Parish Church
Ι.Ν. Αγ.Γεωργίου Αγ. Βασιλείου|Saint George|Agios Vasileios|Άγιος Βασίλειος|572 00|23940 51125|Parish Church
Ι.Ν. Κοιμήσεως Θεοτόκου Αγ. Βασιλείου|Dormition of the Theotokos|Agios Vasileios|Άγιος Βασίλειος|572 00||Parish Church
Ι.Ν. Αγ. Παρασκευής Νικομηδινού|Saint Paraskevi|Nikomidino|Νικομηδινό|570 20|23930 23095|Parish Church
Ι.Ν. Αγ. Γεωργίου Στίβου|Saint George|Stivos|Στίβος|570 20|23930 22236|Parish Church
Ι.Ν. Κοιμήσεως της Θεοτόκου Βασιλουδίου|Dormition of the Theotokos|Vasiloudi|Βασιλούδιον|570 12|6977 876878|Parish Church
Ι.Ν. Αγ. Γεωργίου Γερακαρούς|Saint George|Gerakarou|Γερακαρού|572 00|2310 601719|Parish Church
Ι.Ν. Γεν. Θεοτόκου Γερακαρούς|Nativity of the Theotokos|Gerakarou|Γερακαρού|572 00||Parish Church
''',
    },
    {
        "key": "liti",
        "url": "https://www.imlagada.gr/default.aspx?pageid=58",
        "rows": r'''
Ι.Ν. Αγ. Αθανασίου|Saint Athanasius|Liti|Λητή|570 18|23940 73208,6974429588|Parish Church
Ι.Ν. Ζωοδόχου Πηγής|Life-Giving Spring|Liti|Λητή|570 18||Parish Church
Ι.Ν. Αγ. Γεωργίου|Saint George|Liti|Λητή|570 18|2310 649859|Parish Church
Ι.Ν. Αγ.Γεωργίου|Saint George|Melissochori|Μελισσοχώρι|570 18|23940 32701|Parish Church
Ι.Ν. Αγ. Γρηγορίου Παλαμά|Saint Gregory Palamas|Melissochori|Μελισσοχώρι|572 00||Parish Church
Ι.Ν. Αγ. Τρύφων (Κοιμ.)|Saint Tryphon|Melissochori|Μελισσοχώρι|572 00||Cemetery Church
Ι.Ν. Αναλήψεως του Σωτήρος|Ascension of the Savior|Mesaio|Μεσαίον|545 00|23940 22234|Parish Church
Ι.Ν. Αγ.Γεωργίου & Αγ. Νεκταρίου|Saints George and Nectarios|Monolofos|Μονόλοφος|545 00|2310 786338|Parish Church
Ι.Ν. Ζωοδόχου Πηγής|Life-Giving Spring|Petroto|Πετρωτόν|545 00|6975 910442|Parish Church
Ι.Ν. Κοιμήσεως της Θεοτόκου / Αγ. Τριάδος|Dormition of the Theotokos and Holy Trinity|Drymos|Δρυμός|572 00|23940 31337|Parish Church
''',
    },
    {
        "key": "ossa",
        "url": "https://www.imlagada.gr/default.aspx?pageid=70",
        "rows": r'''
Ι.Ν. Γεννήσεως της Θεοτόκου|Nativity of the Theotokos|Pente Vryses|Πέντε βρύσες|572 00|23940 56242|Parish Church
Ι.Ν. Υψώσεως Τιμίου Σταυρού|Exaltation of the Holy Cross|Lofiskos|Λοφίσκος|570 02|23950 51157|Parish Church
Ι.Ν. Αγ. Κυράνα / Ταξιαρχών|Saint Kyranna and the Holy Archangels|Ossa|Όσσα|572 00|6972093103|Parish Church
Ι.Ν. Αγ. Δημητρίου|Saint Demetrius|Polydendri|Πολυδένδριον|572 00|23940 56397|Parish Church
Ι.Ν. Παμμεγίστων Ταξιαρχών|Holy Archangels|Ossa|Όσσα|572 00||Pilgrimage Church
Ι.Ν. Αγ. Γεωργίου|Saint George|Vertiskos|Βερτίσκος|570 17|23940 94028|Parish Church
Ι.Ν. Αγ. Αθανασίου|Saint Athanasius|Galini|Γαλήνη|572 00|23940 91187|Parish Church
Ι.Ν.Γεννήσεως της Θεοτόκου|Nativity of the Theotokos|Areti|Αρετή|572 00|23950 51044|Parish Church
Ι.Ν. Αγ. Αθανασίου|Saint Athanasius|Chorouda|Χωρούδα|570 17|23940 22234|Parish Church
''',
    },
    {
        "key": "rentini",
        "url": "https://www.imlagada.gr/default.aspx?pageid=90",
        "rows": r'''
Ι.Ν. Ζωοδόχου Πηγής|Life-Giving Spring|Rentini|Ρεντίνα|570 14|2310 825630|Parish Church
Ι.Ν. Αγ. Δημητρίου|Saint Demetrius|Nymfopetra|Νυμφόπετρα|572 00|6945 240178|Parish Church
Ι.Ν. Προφήτη Ηλία|Prophet Elijah|Profitis|Προφήτης|572 00|6936 599432|Parish Church
Ι.Ν. Αγ. Κωνσταντίνου & Ελένης|Saints Constantine and Helen|Vagiochori|Βαΐοχώρι|570 16|6984 591661|Parish Church
Ι.Ν. Αγ. Παντελεήμονα|Saint Panteleimon|Vamvakia|Βαμβακιά|570 14|6936 989664|Parish Church
Ι.Ν. Αποστόλου Θωμά|Apostle Thomas|Megali Volvi|Βόλβη Μεγάλη|570 16|6949 473353|Parish Church
Ι.Ν. Αγ. Παρασκευής|Saint Paraskevi|Mikri Volvi|Βόλβη Μικρά|570 14||Parish Church
Ι.Ν. Κοιμήσεως της Θεοτόκου|Dormition of the Theotokos|Mikrokomi|Μικροκώμη|572 00||Parish Church
''',
    },
    {
        "key": "sochos",
        "url": "https://www.imlagada.gr/default.aspx?pageid=91",
        "rows": r'''
Ι.Ν. Ἅγ. Γεωργίου / Κοιμήσεως της Θεοτόκου|Saint George and the Dormition of the Theotokos|Sochos|Σοχός|572 00|23950 22284|Parish Church
Ι.Ν. Ζωοδόχου Πηγής|Life-Giving Spring|Ano Askos|Ασκός Άνω|570 18||Pilgrimage Church
Ι.Ν. Αγ. Νικολάου|Saint Nicholas|Kato Askos|Ασκός Κάτω|570 18|23950 61119|Parish Church
Ι.Ν. Αγ. Νικολάου|Saint Nicholas|Avgi|Αυγή|570 02||Parish Church
Ι.Ν. Κοιμ. Θεοτόκου|Dormition of the Theotokos|Kryoneri|Κρυονέριον|570 02|23950 51453|Parish Church
''',
    },
]


EXTRA_ROWS = [
    {
        "local": "Ἀποστόλου Παύλου καί Ἁγ. Κυρίλλου καί Μεθοδίου Δερβενίου",
        "dedication": "Apostle Paul and Saints Cyril and Methodius",
        "seat": "Derveni",
        "rank": "Pilgrimage Church",
        "sources": [PATRIARCHATE_PAGE],
    },
    {
        "local": "Παναγίας Χρυσοκεφάλου Πέντε Βρύσεων",
        "dedication": "Panagia Chrysokephalos",
        "seat": "Pente Vryses",
        "rank": "Pilgrimage Church",
        "sources": [PATRIARCHATE_PAGE],
    },
    {
        "local": "Ἁγίου Λαζάρου Εὐαγγελισμοῦ",
        "dedication": "Saint Lazarus",
        "seat": "Evangelismos",
        "rank": "Pilgrimage Church",
        "sources": [PATRIARCHATE_PAGE],
    },
    {
        "local": "Ἁγ. Εἰρήνης Χρυσοβαλάντου Ρεντίνης",
        "dedication": "Saint Irene Chrysovalantou",
        "seat": "Rentini",
        "rank": "Pilgrimage Church",
        "sources": [PILGRIMAGE_PAGE, PATRIARCHATE_PAGE],
    },
    {
        "local": "Παναγίας Περπατούσης Ἡρακλείου",
        "dedication": "Panagia Perpatousa",
        "seat": "Irakleio",
        "rank": "Pilgrimage Church",
        "sources": [PILGRIMAGE_PAGE, PATRIARCHATE_PAGE],
    },
    {
        "local": "Ἁγίου Πορφυρίου Ἡρακλείου",
        "dedication": "Saint Porphyrios",
        "seat": "Irakleio",
        "rank": "Pilgrimage Church",
        "sources": [PATRIARCHATE_PAGE],
    },
    {
        "local": (
            "Ι.Ν. Θεοφανείων, Τιμίου Προδρόμου καί Ἁγίας "
            "Ἀναστασίας τῆς Φαρμακολυτρίας"
        ),
        "dedication": (
            "Theophany, Saint John the Forerunner, and Saint Anastasia "
            "the Deliverer from Potions"
        ),
        "seat": "Lagadas",
        "rank": "Pilgrimage and Institutional Church",
        "sources": [INSTITUTIONAL_PAGE, PATRIARCHATE_PAGE],
    },
    {
        "local": "Ι.Ν. Ἁγίου Χαραλάμπους Μελισσοχωρίου",
        "dedication": "Saint Charalambos",
        "seat": "Melissochori",
        "rank": "Institutional Church",
        "sources": [INSTITUTIONAL_PAGE],
    },
    {
        "local": "Ι.Ν. Ζωοδόχου Πηγῆς Χρυσαυγῆς",
        "dedication": "Life-Giving Spring",
        "seat": "Chrysavgi",
        "rank": "Institutional Church",
        "sources": [INSTITUTIONAL_PAGE],
    },
]


MONASTIC_ROWS = r'''
Ανδρώα Ιερά Μονή Αγ. Τριάδος Πέντε Βρύσεων|Holy Trinity|Pente Vryses|Monastery|23940 56494
Ανδρώα Ιερά Μονή Μεταμορφώσεως του Σωτήρος Σοχού|Transfiguration of the Savior|Sochos|Monastery|23950 22343
Ανδρώα Ιερά Μονή Μεγάλου Βασιλείου|Saint Basil the Great|Agios Vasileios|Monastery|23940 51372
Γυναικεία Ιερά Μονή Αγίου Θεοδώρου Γαβρά|Saint Theodore Gabras|Lagadas Metropolis|Monastery|
Γυναικεία Ιερά Μονή Εισοδίων Θεοτόκου Όσσης|Entry of the Theotokos|Ossa|Monastery|
Γυναικεία Ιερά Μονή Παναγίας Θεοσκεπάστου|Panagia Theoskepastos|Sochos|Metochion|23950 23288
Γυναικεία Ιερά Μονή Αγ. Νεκταρίου|Saint Nectarios|Melissochori|Metochion|
Ησυχαστήριο Ανδρώο "Ο Παντοκράτωρ"|Christ Pantocrator|Melissochori|Hermitage|23940 32215
Ησυχαστήριο Ανδρώο Αγίων Αρχαγγέλων - Βασιλουδίου|Holy Archangels|Vasiloudi|Hermitage|23930 61380
Ησυχαστήριο Αγ. Αποστόλλων και Ισαποστόλων Κυρίλλου και Μεθοδίου - Ασκού|Holy Apostles and Saints Cyril and Methodius|Askos|Hermitage|
Ησυχαστήριο Αγ. Λουκά - Όσσης|Saint Luke|Ossa|Hermitage|
Η Ανάστασις του Χριστού - Εμμαούς|Resurrection of Christ, Emmaus|Agios Vasileios|Hermitage|23940 26350
Αγίου Αθανασίου & Αγίας Κυράννης Γαλήνης|Saints Athanasius and Kyranna|Galini|Hermitage|
Άξιον Εστί|Axion Estin|Mesaio|Hermitage|
Ἀγίου Ραφαήλ Σοχοῦ|Saint Raphael|Sochos|Hermitage|
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "body"


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"[^a-z0-9α-ω]+", "", value)


def make_name(dedication, rank, seat):
    return "%s of %s, %s" % (rank, dedication, seat)


def build_rows():
    rows = []
    index = 0
    for group in PARISH_GROUPS:
        for raw in group["rows"].strip().splitlines():
            (local, dedication, seat, greek_seat, postal_code, phones,
             rank) = raw.split("|", 6)
            index += 1
            name = make_name(dedication, rank, seat)
            address = [greek_seat]
            if postal_code:
                address.append(postal_code)
            address.append("Greece")
            item = {
                "id": "gr-ep-lagadas-%03d-%s" % (index, slug(name)),
                "parent": PARENT,
                "kind": "parish",
                "rank": rank,
                "name": name,
                "local": local,
                "seat": seat,
                "country": "GR",
                "address": address,
                "sources": [group["url"]],
            }
            if phones:
                item["phones"] = phones.split(",")
                item["contact_sources"] = [group["url"]]
                item["contact_checked"] = CHECKED
            rows.append(item)
    for record in EXTRA_ROWS:
        index += 1
        name = make_name(
            record["dedication"], record["rank"], record["seat"]
        )
        rows.append({
            "id": "gr-ep-lagadas-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": record["rank"],
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": [record["seat"], "Greece"],
            "sources": list(record["sources"]),
        })
    for raw in MONASTIC_ROWS.strip().splitlines():
        local, dedication, seat, rank, phone = raw.split("|", 4)
        index += 1
        name = make_name(dedication, rank, seat)
        item = {
            "id": "gr-ep-lagadas-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [MONASTERY_PAGE],
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [MONASTERY_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 88
EXPECTED_OWNER_COUNTS = {PARENT: 88}
EXPECTED_KINDS = {"monastery": 15, "parish": 73}
EXPECTED_RANKS = {
    "Cemetery Church": 1,
    "Hermitage": 8,
    "Institutional Church": 2,
    "Metochion": 2,
    "Metropolitan Cathedral": 1,
    "Monastery": 5,
    "Parish Church": 60,
    "Pilgrimage Church": 8,
    "Pilgrimage and Institutional Church": 1,
}
EXPECTED_CONTACT_BODIES = 53
EXPECTED_PHONE_BODIES = 53
EXPECTED_PHONE_VALUES = 54
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 88
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
    allowed = {"www.imlagada.gr", "ec-patr.org", "www.ec-patr.org"}
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
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Lagadas candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Lagadas candidate ledger date drifted")
    expected_summary = {
        PARENT: 88,
        "total": 88,
        "parish_kind_rows": 73,
        "monastery_kind_rows": 15,
        "contact_bodies": 53,
        "phone_bodies": 53,
        "public_phone_values": 54,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 88,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Lagadas ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Lagadas ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Lagadas ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Lagadas ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Lagadas ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Lagadas ledger has forbidden punctuation")
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
        raise ValueError("Lagadas English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Lagadas English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Lagadas parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Lagadas kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Lagadas rank totals drifted: %r" %
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
        raise ValueError("Lagadas contact coverage drifted: %r"
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


def fetch_text(url):
    request = Request(url, headers={"User-Agent": "Plithos directory audit"})
    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get_content_type()
        if response.status != 200 or content_type != "text/html":
            raise ValueError("unexpected live response for %s" % url)
        raw = response.read().decode("utf-8", "replace")
    raw = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    text = re.sub(r"(?s)<[^>]+>", " ", raw)
    return html.unescape(text)


def check_live():
    source_text = {}
    urls = {
        ROSTER_PAGE, MONASTERY_PAGE, CHAPEL_PAGE, PILGRIMAGE_PAGE,
        INSTITUTIONAL_PAGE, PATRIARCHATE_PAGE,
    }
    urls.update(group["url"] for group in PARISH_GROUPS)
    for url in sorted(urls):
        source_text[url] = fetch_text(url)
    if "ΥΠΟ ΚΑΤΑΣΚΕΥΗ" not in source_text[CHAPEL_PAGE]:
        raise ValueError("Lagadas chapel-page status changed")
    for group in PARISH_GROUPS:
        normalized_page = unicase(source_text[group["url"]])
        for raw in group["rows"].strip().splitlines():
            local, _dedication, _seat, greek_seat, _postal, _phones, _rank = (
                raw.split("|", 6)
            )
            if unicase(local) not in normalized_page:
                raise ValueError("live Lagadas parish marker drifted: %s" % local)
            if unicase(greek_seat) not in normalized_page:
                raise ValueError("live Lagadas seat marker drifted: %s" % greek_seat)
            for phone in (_phones.split(",") if _phones else []):
                if unicase(phone) not in normalized_page:
                    raise ValueError(
                        "live Lagadas phone marker drifted: %s" % phone
                    )
    for record in EXTRA_ROWS:
        if not any(
            unicase(record["local"]) in unicase(source_text[url])
            for url in record["sources"]
        ):
            raise ValueError("live Lagadas supplement drifted: %s"
                             % record["local"])
    normalized_monasteries = unicase(source_text[MONASTERY_PAGE])
    for raw in MONASTIC_ROWS.strip().splitlines():
        local, _dedication, _seat, _rank, phone = raw.split("|", 4)
        if unicase(local) not in normalized_monasteries:
            raise ValueError("live Lagadas monastery marker drifted: %s" % local)
        if phone and unicase(phone) not in normalized_monasteries:
            raise ValueError("live Lagadas monastery phone drifted: %s" % phone)
    return len(urls)


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    elif args.check_live:
        count = check_live()
        print("Lagadas live sources: %d first-party pages verified" % count)
    else:
        print(
            "Lagadas: %d exact named bodies; %d carry current public "
            "contact paths" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Lagadas: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
