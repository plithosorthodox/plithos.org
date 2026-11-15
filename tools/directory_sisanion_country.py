#!/usr/bin/env python3
"""Validate exact current Sisanion and Siatista worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_sisanion_country.py --check
    python tools/directory_sisanion_country.py --check-live
    python tools/directory_sisanion_country.py --dump
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
PARENT = "ep-sisanion"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "sisanion_country.json"
)

LOCAL_PARISHES = "https://www.imsiatistis.gr/ataxinomita/enories/"
LOCAL_MONASTERIES = "https://www.imsiatistis.gr/ieres-mones/"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-sisanioy-siatistis/"
)
OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2020_octobrios.pdf"
)
SAINT_MENAS_RECORD = (
    "https://www.ypes.gr/wp-content/uploads/2026/02/"
    "20260224_atnp_evdomadiaio_7.pdf"
)


# Greek seat|English seat|postal code|current Greek dedication|phones|legal row
# LEGAL_DORMITION represents the live table's blank dedication at Spilios.
PARISH_SOURCE = r'''
Σιάτιστα|Siatista|50300|Άγ. Δημήτριος|24650 21465,24650 21933,6947542028,6946839137|1
Σιάτιστα|Siatista|50300|Άγ. Νικόλαος|24650 21472,24650 21183,6974029439|1
Βλάστη|Vlasti|50009|Άγ. Μάρκος|6936974528|1
Γαλατινή|Galatini|50300|Αγ. Παρασκευή|24650 41089|1
Δρυόβουνον|Dryovouno|50003|Άγ. Μηνάς|24650 51091|1
Εράτυρα|Eratyra|50003|Άγ. Γεώργιος|24650 31192|1
Καλονέριον|Kaloneri|50300|Άγ. Παντελεήμων|6974435311|1
Μεταμόρφωσις|Metamorfosis|50100|Άγ. Νικόλαος|24650 91435|1
Μικρόκαστρον|Mikrokastro|50300|Άγ. Νικόλαος|24650 23144|1
Νάματα|Namata|50003|Άγ. Νικόλαος|24650 31570|1
Πελεκάνος|Pelekanos|50003|Κοιμ. Θεοτόκου|6942776204|1
Σισάνιον|Sisanion|50003|Άγ. Δημήτριος|24650 23520|1
Νεάπολις|Neapoli|50001|Άγ. Γεώργιος|24680 22269,24680 22490|1
Αηδονοχώριον|Aidonochori|50001|Άγ. Νικόλαος|6977820241|1
Αλιάκμων|Aliakmon|50001|Αγ. Τριάς|24680 23525|1
Αξιόκαστρον|Axiokastro|50001|Άγ. Αθανάσιος||1
Ασπρούλα|Asproula|50001|Μετ. Σωτήρος|24680 81208|1
Βελανιδιά|Velanidia|50001|Κοιμ. Θεοτόκου|24680 23012|1
Καλλιστράτιον|Kallistrati|50001|Άγ. Γεώργιος||1
Κλήμα|Klima|50001|Άγ. Νικόλαος||1
Κρυονέριον|Kryoneri|50001|Γεν. Χριστού|24680 71044|1
Μελιδόνιον|Melidonio|50001|Εισ. Θεοτόκου||1
Μεσόλογγος|Mesologgos|50001|Κοιμ. Θεοτόκου|24680 21208|1
Μολόχα|Molocha|50001|Άγ. Δημήτριος|24680 23204|1
Παναρέτη|Panareti|50001|Άγ. Αθανάσιος||1
Πεπονιά|Peponia|50001|Αγ. Βαρβάρα|6970860828|1
Περιστέρα|Peristera|50001|Παμμ. Ταξιάρχαι|24680 24680|1
Πλατανιά|Platania|50001|Κοιμ. Θεοτόκου|24680 22453|1
Πολύλακκος|Polylakkos|50001|Άγ. Νικόλαος||1
Πυλώριον|Pylorio|50001|Τιμ. Πρόδρομος||1
Σήμαντρον|Simantro|50001|Άγ. Γεώργιος||1
Στέρνα|Sterna|50001|Άγ. Νικόλαος||1
Τραπεζίτσα|Trapezitsa|50001|Άγ. Γεώργιος|6986089509|1
Χειμερινόν|Cheimerino|50001|Κοιμ. Θεοτόκου||1
Χορηγός|Chorigos|50001|Παμμ. Ταξιάρχαι||1
Τσοτύλιον|Tsotylio|50002|Αγ. Μαρίνα|24680 31444,6983400552,24680 32670|1
Αγίασμα|Agiasma|50002|Άγ. Γεώργιος||1
Αγ. Σωτήρα|Agia Sotira|50002|Άγ. Κων/νος & Ελένη||1
Άγ. Θεόδωροι|Agioi Theodoroi|50002|Αγ. Παρασκευή|24680 32105|1
Άγ. Ανάργυροι|Agioi Anargyroi|50002|Άγ. Ανάργυροι|6942433250|1
Ανθούσα|Anthousa|50002|Άγ. Θωμάς|24680 21560|1
Ανθοχώριον|Anthochori|50002|Άγ. Δημήτριος|24680 31096|1
Απιδέα|Apidea|50002|Άγ. Ανάργυροι|24680 23635|1
Αχλαδιά|Achladia|50002|Άγ. Δημήτριος||1
Βουχωρίνα|Vouchorina|50002|Άγ. Δημήτριος|24680 31127,6972006112|1
Βροντή|Vronti|50002|Άγ. Νικόλαος||1
Δαμασκηνέα|Damaskenea|50002|Κοιμ. Θεοτόκου|24680 32374|1
Δάφνη|Dafni|50002|Άγ. Δημήτριος||1
Διχείμαρρος|Dicheimarros|50002|Άγ. Γεώργιος||1
Δραγασιά|Dragasia|50002|Άγ. Σπυρίδων|24680 23086|1
Ζώνη|Zoni|50002|Άγ. Θεόδωροι||1
Κλεισώρια|Kleisoria|50002|Άγ. Δημήτριος||1
Κοιλάδι|Koiladi|50002|Άγ. Γεώργιος||1
Κορυφή|Koryfi|50002|Άγ. Δημήτριος|6936317677|1
Κριμίνιον|Kriminio|50002|Άγ. Ευστάθιος|6972306515|1
Λευκάδιον|Lefkadio|50002|Άγ. Παύλος||1
Λεύκη|Lefki|50002|Άγ. Νικόλαος||1
Λευκοθέα|Lefkothea|50002|Αγ. Παρασκευή|24650 71231|1
Λικνάδες|Liknades|50002|Αγ. Παρασκευή||1
Λούβρη|Louvri|50002|Κοιμ. Θεοτόκου||1
Λουκόμιον|Loukomio|50002|Γεν. Θεοτόκου||1
Μόρφη|Morfi|50002|Κοιμ. Θεοτόκου||1
Ομαλή|Omali|50002|Παμμ. Ταξιάρχαι|24680 31839|1
Πολυκάστανον|Polykastano|50002|Αγ. Παρασκευή|24680 71044|1
Ροδοχώριον|Rodochori|50002|Αγ. Παρασκευή|6972306515|1
Σταυροδρόμιον|Stavrodromi|50002|Άγ. Γεώργιος||1
Τριάδα|Triada|50002|Αγ. Τριάς||1
Φυτώκιον|Fytokio|50002|Άγ. Παύλος|6973783423|1
Χρυσαυγή|Chrysavgi|50002|Κοιμ. Θεοτόκου|6976317677|1
Πεντάλοφος|Pentalofos|50007|Άγ. Αθανάσιος|24680 31235|1
Αυγερινός|Avgerinos|50008|Κοιμ. Θεοτόκου|24680 21560,6934752805|1
Βυθός|Vythos|50007|Εισ. Θεοτόκου|24680 41140|1
Δασύλλιον|Dasyllio|50007|Άγ. Νικόλαος|24680 41140|1
Δίλοφος|Dilofos|50007|Κοιμ. Θεοτόκου|24680 41140|1
Βογατσικόν|Vogatsiko|52053|Άγ. Απόστολοι|6946797285|1
Ανθηρόν|Anthero|52200|Κοιμ. Θεοτόκου||1
Άγ. Ηλίας|Agios Ilias|52200|Εισ. Θεοτόκου||1
Βέλος|Velos|52200|Προφ. Ηλίας|24670 41887|1
Διαλεκτόν|Dialekto|52200|Άγ. Νικόλαος|6974029439|1
Νόστιμον|Nostimo|52200|Αγ. Τριάς|24670 43548,6953077688|1
Σκαλοχώριον|Skalochori|52200|Γεν. Θεοτόκου||1
Σπήλιος|Spilios|52200|LEGAL_DORMITION||1
Κερασώνα|Kerasona|52200|Κοιμ. Θεοτόκου||
Άγ. Κοσμάς|Agios Kosmas|51100|Άγ. Αθανάσιος||1
Δοτσικόν|Dotsiko|51100|Άγ. Αθανάσιος|24650 21365|1
Καλλονή|Kalloni|51100|Άγ. Νικόλαος|24620 73357|1
Κυπαρίσσιον|Kyparissio|51100|Άγ. Γεώργιος|24620 73363|1
Τρίκορφο|Trikorfo|51100|Άγ. Νικόλαος|24620 73357|1
'''


DEDICATIONS = {
    "Άγ. Δημήτριος": "Saint Demetrius",
    "Άγ. Νικόλαος": "Saint Nicholas",
    "Άγ. Μάρκος": "Saint Mark",
    "Αγ. Παρασκευή": "Saint Paraskevi",
    "Άγ. Μηνάς": "Saint Menas",
    "Άγ. Γεώργιος": "Saint George",
    "Άγ. Παντελεήμων": "Saint Panteleimon",
    "Κοιμ. Θεοτόκου": "Dormition of the Theotokos",
    "Αγ. Τριάς": "Holy Trinity",
    "Μετ. Σωτήρος": "Transfiguration of the Savior",
    "Γεν. Χριστού": "Nativity of Christ",
    "Εισ. Θεοτόκου": "Entry of the Theotokos",
    "Αγ. Βαρβάρα": "Saint Barbara",
    "Παμμ. Ταξιάρχαι": "Holy Archangels",
    "Τιμ. Πρόδρομος": "Saint John the Forerunner",
    "Αγ. Μαρίνα": "Saint Marina",
    "Άγ. Κων/νος & Ελένη": "Saints Constantine and Helen",
    "Άγ. Ανάργυροι": "Holy Unmercenaries",
    "Άγ. Θωμάς": "Saint Thomas",
    "Άγ. Σπυρίδων": "Saint Spyridon",
    "Άγ. Θεόδωροι": "Holy Theodore Martyrs",
    "Άγ. Ευστάθιος": "Saint Eustathius",
    "Άγ. Παύλος": "Apostle Paul",
    "Γεν. Θεοτόκου": "Nativity of the Theotokos",
    "Προφ. Ηλίας": "Prophet Elijah",
    "Άγ. Απόστολοι": "Holy Apostles",
    "Άγ. Αθανάσιος": "Saint Athanasius",
    "LEGAL_DORMITION": "Dormition of the Theotokos",
}


MONASTIC_SOURCE = r'''
holy-trinity-vythos|Holy Trinity Monastery, Vythos|Ιερά Μονή Αγίας Τριάδος Βυθού|Vythos|Βυθός, Τ.Κ. 50007|24680 71004,6978929809|||https://www.imsiatistis.gr/ieres-mones/andrikes/iera-moni-agias-triados-vythou/|D|Αγίας Τριάδος;Βυθού;2468071004;6978929809
transfiguration-dryovouno|Transfiguration of the Savior Monastery, Dryovouno|Ιερά Μονή Μεταμορφώσεως Σωτήρος Δρυοβούνου|Dryovouno|Δρυόβουνο, Τ.Κ. 50003|24680 23086|||https://www.imsiatistis.gr/ieres-mones/andrikes/iera-moni-metamorfoseos-sotiros-dryovounou/|D|Μεταμορφώσεως Σωτήρος;Δρυοβούνου;2468023086
athanasius-eratyra|Saint Athanasius Monastery, Eratyra|Ιερά Μονή Αγίου Αθανασίου Εράτυρας|Eratyra|Εράτυρα, Τ.Κ. 50003|24650 31570|||https://www.imsiatistis.gr/ieres-mones/andrikes/iera-moni-agiou-athanasiou-eratyras/|D|Αγίου Αθανασίου;Εράτυρας;2465031570
paraskevi-pelekanos|Saint Paraskevi Monastery, Pelekanos|Ιερά Μονή Αγίας Παρασκευής Πελεκάνου|Pelekanos|Πελεκάνος, Τ.Κ. 50003||||https://www.imsiatistis.gr/ieres-mones/andrikes/iera-moni-agias-paraskevis-pelekanou/||Αγίας Παρασκευής;Πελεκάνου
panteleimon-vlasti|Saint Panteleimon Monastery, Vlasti|Ιερά Μονή Αγίου Παντελεήμονος Βλάστης|Vlasti|Βλάστη, Τ.Κ. 50009|6998116520|||https://www.imsiatistis.gr/ieres-mones/andrikes/iera-moni-agiou-panteleimonos-vlastis/|EP|Αγίου Παντελεήμονος;Βλάστης;6998116520
dormition-sisanion|Dormition of the Theotokos Monastery, Sisanion|Ιερά Μονή Κοιμήσεως Θεοτόκου Σισανίου|Sisanion|Σισάνιο, Τ.Κ. 50003|24630 92498|||https://www.imsiatistis.gr/ieres-mones/andrikes/iera-moni-koimiseos-theotokou-sisaniou/|D|Κοιμήσεως Θεοτόκου;Σισανίου;2463092498
dormition-mikrokastro|Dormition of the Theotokos Monastery, Mikrokastro|Ιερά Μονή Κοιμήσεως Θεοτόκου Μικροκάστρου|Mikrokastro|Μικρόκαστρο, Τ.Κ. 50300|24650 71307|imp.mikrokastrou@gmail.com||https://www.imsiatistis.gr/ieres-mones/gynaikeies/iera-moni-koimiseos-theotokou-mikrokastrou/|D|Κοιμήσεως Θεοτόκου;Μικροκάστρου;2465071307;imp.mikrokastrou@gmail.com
nativity-dryovouno|Nativity of the Theotokos Monastery, Dryovouno|Ιερά Μονή Γενεθλίου Θεοτόκου Δρυοβούνου|Dryovouno|Δρυόβουνο, Τ.Κ. 50003|6957464137,24650 51410|impanagiasdryovounou@gmail.com|https://www.imgth.gr/|https://www.imsiatistis.gr/ieres-mones/gynaikeies/iera-moni-genethliou-theotokou-dryovounou/|D,EP,S|Γενεθλίου Θεοτόκου;Δρυοβούνου;6957464137;2465051410;impanagiasdryovounou@gmail.com
constantine-helen-vogatsiko|Saints Constantine and Helen Monastery, Vogatsiko|Ιερά Μονή Αγίων Κωνσταντίνου και Ελένης Βογατσικού|Vogatsiko|Βογατσικό, Τ.Κ. 52053|24670 73103|||https://www.imsiatistis.gr/ieres-mones/gynaikeies/iera-moni-agion-kon-nou-kai-elenis-vogatsikou/|D|Κωνσταντίνου;Ελένης;Βογατσικού;2467073103
athanasius-zikovitsi|Saint Athanasius Monastery, Zikovitsi|Ιερά Μονή Αγίου Αθανασίου Ζηκοβίτσης|Zikovitsi|Ζηκοβίτσα|24673 00301|agiosathanasioszik@gmail.com||https://www.imsiatistis.gr/ieres-mones/gynaikeies/iera-moni-agiou-athanasiou-zikovitsis/|D|Αγίου Αθανασίου;Ζηκοβίτσης;2467300301;agiosathanasioszik@gmail.com
saint-menas|Saint Menas the Great Martyr Monastery, Agios Ioannis, Siatista|Ιερά Ανδρώα Κοινοβιακή Μονή Αγίου Μεγαλομάρτυρος Μηνά|Agios Ioannis, Siatista|Περιοχή Άγιος Ιωάννης, Σιάτιστα||||@GAZETTE||Αγίου Μεγαλομάρτυρος Μηνά
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "body"


def unicase(value):
    value = unicodedata.normalize("NFD", value or "").casefold()
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip()


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def compact_digits(value):
    return re.sub(r"\D", "", value)


def parish_rows():
    rows = []
    lines = [line for line in PARISH_SOURCE.splitlines() if line.strip()]
    if len(lines) != 88:
        raise ValueError("expected 88 exact current parish rows")
    legal_count = 0
    for number, raw in enumerate(lines, 1):
        greek_seat, seat, postal, greek_dedication, phones, legal = raw.split(
            "|", 5
        )
        dedication = DEDICATIONS[greek_dedication]
        local_dedication = greek_dedication
        if greek_dedication == "LEGAL_DORMITION":
            local_dedication = "Κοιμ. Θεοτόκου"
        name = "Parish Church of %s, %s" % (dedication, seat)
        sources = [LOCAL_PARISHES]
        if legal:
            sources.append(OFFICIAL_PDF)
            legal_count += 1
        row = {
            "id": "gr-ep-sisanion-%03d-%s" % (number, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Parish Church",
            "name": name,
            "local": "%s, %s" % (local_dedication, greek_seat),
            "seat": seat,
            "country": "GR",
            "address": [greek_seat, "Τ.Κ. %s" % postal, "Greece"],
            "sources": sources,
            "detail": LOCAL_PARISHES,
            "source_seat": greek_seat,
            "source_postal": postal,
            "source_dedication": greek_dedication,
        }
        values = split_values(phones)
        if values:
            row["phones"] = values
            row["contact_sources"] = [LOCAL_PARISHES]
            row["contact_checked"] = CHECKED
        if legal:
            row["legal_roster"] = True
        rows.append(row)
    if legal_count != 87:
        raise ValueError("expected 87 regulated parish rows")
    return rows


def monastic_rows(start_number):
    rows = []
    lines = [line for line in MONASTIC_SOURCE.splitlines() if line.strip()]
    if len(lines) != 11:
        raise ValueError("expected 11 exact current monastic institutions")
    for offset, raw in enumerate(lines):
        parts = raw.split("|", 10)
        if len(parts) != 11:
            raise ValueError("invalid monastic source row: %s" % raw)
        (key, name, local, seat, address, phones, emails, site, detail,
         contact_flags, markers) = parts
        if detail == "@GAZETTE":
            detail = SAINT_MENAS_RECORD
            sources = [SAINT_MENAS_RECORD]
        else:
            sources = [detail, PATRIARCHATE_PAGE]
            if site:
                sources.append(site)
        row = {
            "id": "gr-ep-sisanion-%03d-%s" %
                  (start_number + offset, key),
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": sources,
            "detail": detail,
            "live_markers": [item for item in markers.split(";") if item],
        }
        phone_values = split_values(phones)
        email_values = split_values(emails)
        if phone_values:
            row["phones"] = phone_values
        if email_values:
            row["emails"] = email_values
        if site:
            row["site"] = site
        if phone_values or email_values or site:
            flags = set(split_values(contact_flags))
            contact_sources = []
            if "D" in flags:
                contact_sources.append(detail)
            if "EP" in flags:
                contact_sources.append(PATRIARCHATE_PAGE)
            if "S" in flags:
                contact_sources.append(site)
            row["contact_sources"] = contact_sources
            row["contact_checked"] = CHECKED
        rows.append(row)
    return rows


PARISH_ROWS = parish_rows()
MONASTIC_ROWS = monastic_rows(len(PARISH_ROWS) + 1)
ROWS = PARISH_ROWS + MONASTIC_ROWS
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 99
EXPECTED_OWNER_COUNTS = {PARENT: 99}
EXPECTED_KINDS = {"monastery": 11, "parish": 88}
EXPECTED_RANKS = {"Monastery": 11, "Parish Church": 88}
EXPECTED_CURRENT_SOURCE_RECORDS = 89
EXPECTED_CURRENT_UNIQUE_PARISHES = 88
EXPECTED_LEGAL_PARISHES = 87
EXPECTED_CONTACT_BODIES = 63
EXPECTED_PHONE_BODIES = 63
EXPECTED_PHONE_VALUES = 76
EXPECTED_EMAIL_BODIES = 3
EXPECTED_EMAIL_VALUES = 3
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 99
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "www.imsiatistis.gr",
    "imsiatistis.gr",
    "ec-patr.org",
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "www.ypes.gr",
    "www.imgth.gr",
    "herbal-monastery.com",
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
    has_contact = bool(
        item.get("phones") or item.get("emails") or item.get("site")
    )
    contact_sources = list(item.get("contact_sources") or [])
    if has_contact and not contact_sources:
        raise ValueError("%s lacks contact provenance" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
        if source_url not in sources:
            raise ValueError("%s has contact evidence outside its sources" %
                             item.get("id"))
    if contact_sources and item.get("contact_checked") != CHECKED:
        raise ValueError("%s lacks a current contact check" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
    for key in ("source_seat", "source_postal", "source_dedication",
                "live_markers"):
        item.pop(key, None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Sisanion candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Sisanion candidate ledger date drifted")
    expected_summary = {
        PARENT: 99,
        "total": 99,
        "current_table_source_records": 89,
        "current_unique_parishes": 88,
        "regulated_parish_rows": 87,
        "parish_kind_rows": 88,
        "monastery_kind_rows": 11,
        "contact_bodies": 63,
        "phone_bodies": 63,
        "public_phone_values": 76,
        "email_bodies": 3,
        "public_email_values": 3,
        "body_owned_sites": 1,
        "address_bodies": 99,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Sisanion ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Sisanion ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 4:
                raise ValueError("Sisanion ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Sisanion ledger has an invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Sisanion ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Sisanion ledger has forbidden punctuation")
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
            digits = compact_digits(phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.fullmatch(email):
                raise ValueError("%s carries an invalid email" % row_id)
        signature = (
            item["parent"], unicase(item["local"]),
            unicase(" ".join(item.get("address") or [])),
        )
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
        raise ValueError("Sisanion English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Sisanion English seat coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Sisanion rank totals drifted")
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Sisanion kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Sisanion parent totals drifted")
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
        raise ValueError("Sisanion contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


class TableReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "table":
            self.current_table = {
                "id": values.get("id", ""), "rows": []
            }
            self.tables.append(self.current_table)
        elif tag == "tr" and self.current_table is not None:
            self.current_table["rows"].append([])
        elif (tag in ("td", "th") and self.current_table is not None and
              self.current_table["rows"]):
            self.current_cell = []
        elif tag == "br" and self.current_cell is not None:
            self.current_cell.append(" ")

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.current_cell is not None:
            value = re.sub(r"\s+", " ", " ".join(self.current_cell)).strip()
            self.current_table["rows"][-1].append(value)
            self.current_cell = None
        elif tag == "table":
            self.current_table = None


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Connection": "close",
    })
    with urlopen(request, timeout=60) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", unicase(text))


def live_parish_rows(payload):
    reader = TableReader()
    reader.feed(payload.decode("utf-8", "replace"))
    table_ids = {"tablepress-10", "tablepress-12", "tablepress-13",
                 "tablepress-14", "tablepress-15", "tablepress-16"}
    tables = [table for table in reader.tables if table["id"] in table_ids]
    if {table["id"] for table in tables} != table_ids:
        raise ValueError("live parish page lacks one or more district tables")
    records = []
    for table in tables:
        current = None
        seat_context = ""
        postal_context = ""
        for cells in table["rows"][1:]:
            if len(cells) < 4:
                continue
            greek_seat, postal, dedication, phone_text = cells[:4]
            if greek_seat:
                seat_context = greek_seat
                postal_context = postal
            if dedication:
                current = {
                    "seat": greek_seat or seat_context,
                    "postal": postal or postal_context,
                    "dedication": dedication,
                    "phones": [],
                }
                records.append(current)
            dash_values = ("-", "\u2013", "\u2014")
            if current and phone_text and phone_text not in dash_values:
                digits = re.sub(r"\s+", "", phone_text)
                current["phones"].extend(re.findall(
                    r"(?<!\d)(?:69\d{8}|2\d{9})(?!\d)", digits
                ))
    return records


def parish_live_signature(record):
    dedication = record["dedication"]
    if dedication in ("-", "\u2013", "\u2014"):
        dedication = ""
    return (
        unicase(record["seat"]), record["postal"], unicase(dedication),
        tuple(compact_digits(value) for value in record["phones"]),
    )


def embedded_parish_signature(row):
    dedication = row["source_dedication"]
    if dedication == "LEGAL_DORMITION":
        dedication = ""
    return (
        unicase(row["source_seat"]), row["source_postal"],
        unicase(dedication),
        tuple(compact_digits(value) for value in row.get("phones") or []),
    )


def check_live_sources():
    parish_blob, parish_type = fetch(LOCAL_PARISHES)
    if "html" not in parish_type:
        raise ValueError("live parish directory is not HTML")
    source_records = live_parish_rows(parish_blob)
    if len(source_records) != EXPECTED_CURRENT_SOURCE_RECORDS:
        raise ValueError("live parish source-record count drifted: %d" %
                         len(source_records))
    signatures = [parish_live_signature(row) for row in source_records]
    unique_signatures = list(dict.fromkeys(signatures))
    if len(unique_signatures) != EXPECTED_CURRENT_UNIQUE_PARISHES:
        raise ValueError("live unique parish count drifted: %d" %
                         len(unique_signatures))
    duplicates = [signature for signature, count in Counter(signatures).items()
                  if count > 1]
    if (len(duplicates) != 1 or
            unicase("Μεσόλογγος") not in duplicates[0][0]):
        raise ValueError("live duplicate parish reconciliation drifted")
    expected = [embedded_parish_signature(row) for row in PARISH_ROWS]
    if unique_signatures != expected:
        missing = [value for value in expected if value not in unique_signatures]
        extra = [value for value in unique_signatures if value not in expected]
        raise ValueError("live parish roster drifted: missing=%r extra=%r" %
                         (missing, extra))

    urls = sorted({url for row in MONASTIC_ROWS
                   for url in row.get("sources", [])})
    cache = {}
    for url in urls:
        payload, content_type = fetch(url)
        if url.lower().endswith(".pdf"):
            if not payload.startswith(b"%PDF") or len(payload) < 50000:
                raise ValueError("live government source is not a PDF: %s" % url)
            cache[url] = payload
        else:
            if "html" not in content_type and not payload.lstrip().startswith(b"<"):
                raise ValueError("live source is not HTML: %s" % url)
            cache[url] = normalized_page(payload)

    ep_page = cache[PATRIARCHATE_PAGE]
    for marker in ("ενοριακοι ναοι 87", "παρεκκλησια 130",
                   "εξωκκλησια 60", "ναοι κοιμητηριων 80",
                   "μοναστηριακοι ναοι 9", "στατιστικα στοιχεια 2023"):
        if unicase(marker) not in ep_page:
            raise ValueError("Patriarchate page lacks marker: %s" % marker)

    monastery_blob, monastery_type = fetch(LOCAL_MONASTERIES)
    if "html" not in monastery_type:
        raise ValueError("live monastery roster is not HTML")
    monastery_roster = monastery_blob.decode("utf-8", "replace")
    local_details = [row["detail"] for row in MONASTIC_ROWS
                     if row["detail"] != SAINT_MENAS_RECORD]
    if len(local_details) != 10:
        raise ValueError("expected ten local monastery detail pages")
    for detail in local_details:
        if urlparse(detail).path.rstrip("/") not in monastery_roster:
            raise ValueError("monastery roster lacks detail page: %s" % detail)

    for row in MONASTIC_ROWS[:-1]:
        pages = " ".join(cache[url] for url in row["sources"]
                         if isinstance(cache[url], str))
        digits = compact_digits(pages)
        for marker in row.get("live_markers") or []:
            if marker.isdigit():
                if marker not in digits:
                    raise ValueError("%s lacks live marker %s" %
                                     (row["id"], marker))
            elif unicase(marker) not in pages:
                raise ValueError("%s lacks live marker %s" %
                                 (row["id"], marker))
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digits:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
        for email in row.get("emails") or []:
            if unicase(email) not in pages:
                raise ValueError("%s lacks live email %s" %
                                 (row["id"], email))

    legal_blob, legal_type = fetch(OFFICIAL_PDF)
    if not legal_blob.startswith(b"%PDF") or len(legal_blob) < 1000000:
        raise ValueError("Church of Greece legal roster is not live")
    if "pdf" not in legal_type and "octet-stream" not in legal_type:
        raise ValueError("legal roster returned an unexpected content type")
    menas_blob = cache[SAINT_MENAS_RECORD]
    if not menas_blob.startswith(b"%PDF"):
        raise ValueError("Saint Menas government record is not live")
    print("Sisanion live sources: %d parish records, %d unique parishes, "
          "%d monastic sources checked" %
          (len(source_records), len(unique_signatures), len(urls)))


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
        print("Sisanion: 99 exact bodies; 88 current parishes and "
              "11 monasteries")
        print("Contacts: 63 bodies; 76 phones; 3 emails; 1 body site")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Sisanion: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
