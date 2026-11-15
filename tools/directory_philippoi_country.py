#!/usr/bin/env python3
"""Validate exact named Philippoi, Neapolis and Thasos bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_philippoi_country.py --check
    python tools/directory_philippoi_country.py --check-live
    python tools/directory_philippoi_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "philippoi_country.json"
)
PARENT = "ep-philippoi"
METROPOLIS_PAGE = "https://imfnth.gr/"
KAVALA_ROSTER_PAGE = (
    "https://imfnth.gr/mitropoli/topiki-agiologia/"
    "2014-12-09-17-35-17/arxieratiki-epitropeia.html"
)
MONASTERY_PAGE = (
    "https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones.html"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-filippon-neapoleos-thasoy/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/philippon-neapoleos-kai-thasou"
)
LEGAL_PDF_2017 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2017_iounios.pdf"
)
LEGAL_PDF_2019 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/"
    "2019_avgoustos_septembrios.pdf"
)
LEGAL_PDF_2020 = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2020_martios.pdf"
)


# Greek seat | English seat | Greek dedication | English dedication
#
# The first 93 rows reproduce the complete 2019 legal parish table. The
# Zarkadia row is confirmed by the official 2017 recognition because the
# searchable rendering of the 2019 table omits that one printed row. The
# final Chryssochorion row is the exact addition made by the 2020 amendment.
PARISH_ROWS = r'''
Καβάλα|Kavala|Αγίου Αθανασίου|Saint Athanasius
Καβάλα|Kavala|Αγίων Αναργύρων|Holy Unmercenaries
Καβάλα|Kavala|Αγίας Βαρβάρας|Saint Barbara
Καβάλα|Kavala|Αγίου Γεωργίου|Saint George
Καβάλα|Kavala|Αγίας Ειρήνης|Saint Irene
Καβάλα|Kavala|Αγίου Λουκά|Saint Luke
Καβάλα|Kavala|Αγίου Νικολάου|Saint Nicholas
Καβάλα|Kavala|Αγίου Παύλου|Saint Paul
Καβάλα|Kavala|Αγίας Παρασκευής|Saint Paraskevi
Καβάλα|Kavala|Αγίου Τρύφωνος|Saint Tryphon
Καβάλα|Kavala|Αγίας Τριάδος|Holy Trinity
Καβάλα|Kavala|Αγίας Φωτεινής|Saint Photini
Καβάλα|Kavala|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Καβάλα|Kavala|Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior
Καβάλα|Kavala|Προφήτου Ηλιού|Prophet Elijah
Καβάλα|Kavala|Τιμίου Προδρόμου|Saint John the Forerunner
Καβάλα|Kavala|Υψώσεως Τιμίου Σταυρού|Exaltation of the Holy Cross
Αβραμυλιά|Avramylia|Παμμεγίστων Ταξιαρχών|Holy Archangels
Αγίασμα|Agiasma|Αγίου Γεωργίου|Saint George
Άγιος Κοσμάς|Agios Kosmas|Αγίου Παντελεήμονος|Saint Panteleimon
Αμισιανά|Amisiana|Αγίων Μυροφόρων|Holy Myrrhbearers
Αμυγδαλεών|Amygdaleonas|Αγίου Γεωργίου|Saint George
Σταυρός Αμυγδαλεώνος|Stavros, Amygdaleonas|Τιμίου Σταυρού|Holy Cross
Βουνοχώριον|Vounochori|Αγίου Δημητρίου|Saint Demetrius
Γέροντας|Gerontas|Αγίου Ιωάννου|Saint John
Γραβούνα|Gravouna|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Δάτον|Dato|Αγίου Παντελεήμονος|Saint Panteleimon
Διαλεκτόν|Dialekto|Ευαγγελισμού Θεοτόκου|Annunciation of the Theotokos
Διπόταμος|Dipotamos|Αγίου Γεωργίου|Saint George
Δύσβατον|Dysvato|Αγίου Γεωργίου|Saint George
Ελαφοχώριον|Elafochori|Αγίου Δημητρίου|Saint Demetrius
Ερατεινόν|Erateino|Γενεσίου Θεοτόκου|Nativity of the Theotokos
Ζαρκαδιά|Zarkadia|Ζωοδόχου Πηγής|Life-Giving Spring
Ζυγός|Zygos|Αγίου Αποστόλου Θωμά|Holy Apostle Thomas
Προσφυγικός Συνοικισμός Ζυγού|Refugee Settlement, Zygos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Θάσος|Thasos|Αγίου Νικολάου|Saint Nicholas
Θάσος|Thasos|Αγίας Τριάδος και Αγίου Βασιλείου|Holy Trinity and Saint Basil
Θεολόγος Θάσου|Theologos, Thasos|Αγίου Δημητρίου|Saint Demetrius
Θεολόγος Θάσου|Theologos, Thasos|Αγίας Παρασκευής|Saint Paraskevi
Καλλιράχη Θάσου|Kallirachi, Thasos|Αγίου Δημητρίου|Saint Demetrius
Σκάλα Καλλιράχης Θάσου|Skala Kallirachis, Thasos|Αγίου Νικολάου|Saint Nicholas
Κεραμωτή|Keramoti|Αγίου Νικολάου|Saint Nicholas
Κεχρόκαμπος|Kechrokampos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Κοκκινόχωμα|Kokkinochoma|Αγίου Δημητρίου|Saint Demetrius
Κορυφές|Koryfes|Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior
Κρανοχώριον|Kranochori|Αγίου Δημητρίου|Saint Demetrius
Κρηνίδες|Krinides|Αγίου Γεωργίου|Saint George
Κρηνίδες|Krinides|Αγίου Χριστοφόρου|Saint Christopher
Κρυονέριον|Kryoneri|Αγίας Τριάδος|Holy Trinity
Λεκάνη|Lekani|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen
Λεύκη|Lefki|Αγίου Γεωργίου|Saint George
Λιμενάρια Θάσου|Limenaria, Thasos|Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior
Καλύβια Λιμεναρίων Θάσου|Kalyvia Limenarion, Thasos|Αγίου Γεωργίου|Saint George
Λιμνιά|Limnia|Αγίου Γεωργίου|Saint George
Λυδία|Lydia|Τιμίου Προδρόμου|Saint John the Forerunner
Λυκόστομον|Lykostomo|Αγίου Γεωργίου|Saint George
Μακρυχώριον|Makrychori|Υψώσεως Τιμίου Σταυρού|Exaltation of the Holy Cross
Μαριές Θάσου|Maries, Thasos|Παμμεγίστων Ταξιαρχών|Holy Archangels
Σκάλα Μαριών Θάσου|Skala Marion, Thasos|Τιμίου Προδρόμου|Saint John the Forerunner
Μοναστηράκιον|Monastiraki|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Νέα Καρβάλη|Nea Karvali|Αγίου Γρηγορίου|Saint Gregory the Theologian
Νέα Καρυά|Nea Karya|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Νέα Κώμη|Nea Komi|Αγίας Τριάδος|Holy Trinity
Νέος Ξεριάς|Neos Xerias|Αγίου Γεωργίου|Saint George
Παλαιά Καβάλα|Palaia Kavala|Παναγίας Οδηγητρίας|Panagia Hodegetria
Παληόν|Palio|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Παναγία Θάσου|Panagia, Thasos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Παράδεισος|Paradeisos|Αγίου Ιωάννου|Saint John
Πέρνη|Perni|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen
Πετροπηγή|Petropigi|Αγίου Γεωργίου|Saint George
Πηγές|Piges|Αγίου Δημητρίου|Saint Demetrius
Πλαταμών|Platamon|Προφήτου Ηλιού|Prophet Elijah
Πολύνερον|Polynero|Αγίου Γεωργίου|Saint George
Πολύστυλον|Polystylo|Αγίας Τριάδος και Αγίων Πέντε Μαρτύρων|Holy Trinity and Five Martyrs
Ποντολίβαδον|Pontolivado|Γενεσίου Θεοτόκου|Nativity of the Theotokos
Ποταμιά Θάσου|Potamia, Thasos|Εισοδίων Θεοτόκου|Entry of the Theotokos
Ποτός Θάσου|Potos, Thasos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Πρίνος Θάσου|Prinos, Thasos|Αγίου Νικολάου|Saint Nicholas
Πρίνος Θάσου|Prinos, Thasos|Τιμίου Προδρόμου|Saint John the Forerunner
Ραχώνιον Θάσου|Rachoni, Thasos|Αγίου Γεωργίου|Saint George
Ραχώνιον Θάσου|Rachoni, Thasos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Σκοπός|Skopos|Αγίου Δημητρίου|Saint Demetrius
Στεγνόν|Stegno|Αγίου Παντελεήμονος|Saint Panteleimon
Στενωπός|Stenopos|Αγίου Γεωργίου|Saint George
Σωτήρ Θάσου|Sotiras, Thasos|Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior
Σκάλα Σωτήρος Θάσου|Skala Sotiros, Thasos|Προφήτου Ηλιού|Prophet Elijah
Φίλιπποι|Philippoi|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Χαϊδευτόν|Chaidefto|Γενεσίου Θεοτόκου|Nativity of the Theotokos
Χαλκερόν|Chalkero|Ζωοδόχου Πηγής|Life-Giving Spring
Χρυσούπολις|Chrysoupoli|Αγίου Αθανασίου|Saint Athanasius
Χρυσούπολις|Chrysoupoli|Αγίου Γεωργίου|Saint George
Χρυσούπολις|Chrysoupoli|Αγίου Δημητρίου|Saint Demetrius
Χρυσούπολις|Chrysoupoli|Αγίου Παντελεήμονος|Saint Panteleimon
Χρυσοχώριον|Chryssochorio|Αγίου Γεωργίου|Saint George
'''


KAVALA_BASE = (
    "https://imfnth.gr/mitropoli/topiki-agiologia/"
    "2014-12-09-17-35-17/arxieratiki-epitropeia/"
)


# dedication | address | phone | postal code | detail-page suffix
KAVALA_CONTACTS = r'''
Αγίου Αθανασίου|Αγίου Αθανασίου 109|2510222330|65201|120-agio-athanasiou.html
Αγίων Αναργύρων|Αγίων Αναργύρων 6|2510226533|65403|119-agioi-anargiroi.html
Αγίας Βαρβάρας|Κολοκοτρώνη 64|2510223292|65201|114-agia-varvara.html
Αγίου Γεωργίου|Περδίκα 1|2510224398|65302|121-agios-georgios.html
Αγίας Ειρήνης|Θεμιστοκλή Κορνάρου 6|2510246538|65404|115-agia-eirinis.html
Αγίου Νικολάου|Αγίου Νικολάου 1|2510224527|65302|123-agiou-nikolaou.html
Αγίου Παύλου|Ιωακείμ Σγουρού 1|2510222113|65302|113-apotolou-paulou.html
Αγίας Παρασκευής|Χρυσοστόμου Σμύρνης|2510243820|65403|116-agia-paraskeui.html
Αγίου Τρύφωνος|Περιγιάλι 76|2510230492|65201|125-agiou-trifonos.html
Αγίας Τριάδος|Αμερικανικού Ερυθρού Σταυρού|2510221878|65201|117-agia-triados.html
Αγίας Φωτεινής|Ευξείνου Πόντου και Ανατολικής Ρωμυλίας|2510243408|65404|118-agia-foteini.html
Κοιμήσεως Θεοτόκου|Θεοδώρου Πουλίδου 69|2510222159|65201|126-theotokou.html
Μεταμορφώσεως του Σωτήρος|Φιλαδελφείας και Αρκαδίου|2510241000|65404|127-naos-metamorfoseos.html
Προφήτου Ηλιού|Παρθενώνος 3|2510223823|65302|128-profitilia.html
Τιμίου Προδρόμου|Ελευθερίου Βενιζέλου|2510223177|65403|102-timiou-prodromou.html
Υψώσεως Τιμίου Σταυρού|Σαππαίων 2|2510226213|65201|129-timios-stauros.html
'''


# local | dedication | seat | phone | address | detail page
MONASTIC_ROWS = r'''
Ιερά Μονή Αγίου Αποστόλου Σίλα|Holy Apostle Silas|Kavala|2510242511|Ιερά Μονή Αγίου Αποστόλου Σίλα, Καβάλα 65500|https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/130-apostolou-sila.html
Ιερά Μονή Κοιμήσεως της Θεοτόκου Μαριών Θάσου|Dormition of the Theotokos|Maries, Thasos|2593051394|Μαριές Θάσου|https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/101-iera-moni.html
Ιερά Μονή Μεταμορφώσεως του Σωτήρος|Transfiguration of the Savior|Nikites|2591054236|Νικητές Καβάλας|
Ιερά Μονή Αγίου Παντελεήμονος|Saint Panteleimon|Prinos, Thasos|2593071235|Πρίνος Θάσου|
'''


# local | dedication | seat | phone | address | detail page
PILGRIMAGE_ROWS = r'''
Ιερό Προσκύνημα Αγίου Γρηγορίου του Θεολόγου|Saint Gregory the Theologian|Nea Karvali|2510316232|Νέα Καρβάλη 64006|https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/132-agiou-grigoriou.html
Ιερό Προσκύνημα Αγίου Νεκταρίου|Saint Nektarios|Aspri Ammos|2510832885|Άσπρη Άμμος Καβάλας|
Ιερό Προσκύνημα και Βαπτιστήριο Αγίας Λυδίας της Φιλιππησίας|Saint Lydia of Philippi|Ancient Philippoi|2510516944|Λυδία Καβάλας 64003|https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/131-ludias.html
'''


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


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def contact_map():
    result = {}
    for raw in KAVALA_CONTACTS.strip().splitlines():
        dedication, address, phone, postal, suffix = raw.split("|", 4)
        result[dedication] = {
            "address": [address, "Καβάλα %s" % postal],
            "phones": [phone],
            "site": KAVALA_BASE + suffix,
        }
    if len(result) != 16:
        raise ValueError("expected 16 current Kavala contact pages")
    return result


def build_rows():
    rows = []
    contacts = contact_map()
    parish_lines = PARISH_ROWS.strip().splitlines()
    if len(parish_lines) != 94:
        raise ValueError("expected 94 exact current parish rows")
    signatures = set()
    for index, raw in enumerate(parish_lines, 1):
        seat_local, seat, dedication_local, dedication = raw.split("|", 3)
        signature = (seat_local, dedication_local)
        if signature in signatures:
            raise ValueError("duplicate source parish row: %r" % (signature,))
        signatures.add(signature)
        rank = "Parish Church"
        if seat_local == "Καβάλα" and dedication_local == "Αγίου Παύλου":
            rank = "Cathedral"
        elif (seat_local == "Καβάλα" and
              dedication_local == "Τιμίου Προδρόμου"):
            rank = "Metropolitan Church"
        name = make_name(dedication, rank, seat)
        sources = [LEGAL_PDF_2019, PATRIARCHATE_PAGE]
        if seat_local == "Ζαρκαδιά":
            sources = [LEGAL_PDF_2017, LEGAL_PDF_2019,
                       PATRIARCHATE_PAGE]
        elif seat_local == "Χρυσοχώριον":
            sources = [LEGAL_PDF_2020, PATRIARCHATE_PAGE]
        item = {
            "id": "gr-ep-philippoi-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (dedication_local, seat_local),
            "seat": seat,
            "country": "GR",
            "address": [seat_local],
            "sources": sources,
        }
        if seat_local == "Καβάλα" and dedication_local in contacts:
            detail = contacts[dedication_local]
            item.update(detail)
            item["sources"] = [LEGAL_PDF_2019, PATRIARCHATE_PAGE,
                               detail["site"]]
            item["contact_sources"] = [detail["site"]]
            item["contact_checked"] = CHECKED
        rows.append(item)

    for raw in MONASTIC_ROWS.strip().splitlines():
        local, dedication, seat, phone, address, detail = raw.split("|", 5)
        name = make_name(dedication, "Monastery", seat)
        sources = [PATRIARCHATE_PAGE, CHURCH_OF_GREECE_PAGE]
        if detail:
            sources.append(detail)
        item = {
            "id": "gr-ep-philippoi-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address],
            "phones": [phone],
            "sources": sources,
            "contact_sources": [PATRIARCHATE_PAGE],
            "contact_checked": CHECKED,
        }
        if detail:
            item["site"] = detail
        rows.append(item)

    for raw in PILGRIMAGE_ROWS.strip().splitlines():
        local, dedication, seat, phone, address, detail = raw.split("|", 5)
        name = make_name(dedication, "Pilgrimage Church", seat)
        sources = [PATRIARCHATE_PAGE]
        if detail:
            sources.append(detail)
        item = {
            "id": "gr-ep-philippoi-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address],
            "phones": [phone],
            "sources": sources,
            "contact_sources": [PATRIARCHATE_PAGE],
            "contact_checked": CHECKED,
        }
        if detail:
            item["site"] = detail
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 101
EXPECTED_OWNER_COUNTS = {PARENT: 101}
EXPECTED_KINDS = {"monastery": 4, "parish": 97}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Metropolitan Church": 1,
    "Monastery": 4,
    "Parish Church": 92,
    "Pilgrimage Church": 3,
}
EXPECTED_CONTACT_BODIES = 23
EXPECTED_PHONE_BODIES = 23
EXPECTED_PHONE_VALUES = 23
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 20
EXPECTED_ADDRESS_BODIES = 101
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
    allowed = {
        "imfnth.gr", "www.imfnth.gr", "ec-patr.org", "www.ec-patr.org",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
    }
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
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError("contact source is outside identity sources")
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s site lacks source provenance" % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Philippoi candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Philippoi candidate ledger date drifted")
    expected_summary = {
        PARENT: 101,
        "total": 101,
        "exact_current_parishes": 94,
        "exact_current_monasteries": 4,
        "exact_current_pilgrimages": 3,
        "parish_kind_rows": 97,
        "monastery_kind_rows": 4,
        "contact_bodies": 23,
        "phone_bodies": 23,
        "public_phone_values": 23,
        "email_bodies": 0,
        "public_email_values": 0,
        "official_detail_sites": 20,
        "address_bodies": 101,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Philippoi candidate ledger summary drifted")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 3:
        raise ValueError("Philippoi candidate ledger lacks held leads")


def build():
    result = []
    ids = set()
    signatures = {}
    owner_counts = Counter()
    kind_counts = Counter()
    rank_counts = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        parent = item.get("parent")
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing Philippoi row id")
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s lacks the GR country code" % row_id)
        for field in ("kind", "rank", "name", "local", "seat"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
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
            raise ValueError("%s duplicates %s after normalization" % (
                row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[parent] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (
            EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Philippoi English name coverage drifted")
    if set(ENGLISH_SEATS) != {
            item["seat"] for item in result if item.get("seat")}:
        raise ValueError("Philippoi English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Philippoi parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Philippoi kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Philippoi rank totals drifted: %r" %
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
        raise ValueError("Philippoi contact coverage drifted: %r" %
                         (coverage,))
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


def fetch_source(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=60) as response:
        if response.status >= 400:
            raise ValueError("%s returned HTTP %s" % (url, response.status))
        return (
            response.headers.get("Content-Type", "").lower(),
            response.read(),
        )


def assert_html_markers(url, markers, label):
    content_type, payload = fetch_source(url)
    if "html" not in content_type:
        raise ValueError("%s returned a non-HTML response" % label)
    text = normalize_source_text(payload.decode("utf-8", "replace"))
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("%s source marker drifted: %s" % (label, marker))


def check_live_sources():
    assert_html_markers(PATRIARCHATE_PAGE, (
        "Ἐνοριακοί Ναοί : 94",
        "Παρεκκλήσια-Ἐξωκκλήσια 72",
        "Ναοί Κοιμητηρίων 8",
        "Μοναστηριακοί Ναοί: 4",
        "Ἀποστόλου Σίλα Καβάλας",
        "2510-242.511",
        "Κοιμ. Θεοτόκου Μαριῶν Θάσου",
        "25930-51394",
        "Μεταμορφώσεως Σωτῆρος Νικητῶν",
        "25910-54236",
        "Ἁγίου Παντελεήμονος Πρίνου Θάσου",
        "25930-71235",
        "Ἁγ. Γρηγορίου τοῦ Θεολόγου Νέας Καρβάλης",
        "2510-316.232",
        "Ἁγίου Νεκταρίου Ἄσπρης Ἄμμου",
        "2510-832.885",
        "Ναός-Βαπτιστήριον Ἁγίας Λυδίας",
        "2510-516.944",
    ), "Patriarchate profile")
    assert_html_markers(CHURCH_OF_GREECE_PAGE, (
        "Αγ. Σίλα Καβάλας",
        "Μεταμορφώσεως Σωτήρος Νικητών",
        "Αγ. Παντελεήμονος Θάσου",
        "25930-71235",
    ), "Church of Greece profile")
    assert_html_markers(METROPOLIS_PAGE, (
        "ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΛΟΥΚΑ ΚΑΒΑΛΑΣ",
        "ΙΕΡΟΣ ΚΑΘΕΔΡΙΚΟΣ ΝΑΟΣ ΑΠΟΣΤΟΛΟΥ ΠΑΥΛΟΥ",
    ), "current Metropolis site")
    assert_html_markers(MONASTERY_PAGE, (
        "ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΑΠΟΣΤΟΛΟΥ ΣΙΛΑ",
        "ΙΕΡΑ ΜΟΝΗ ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΜΑΡΙΩΝ ΘΑΣΟΥ",
        "ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙΑΣ ΛΥΔΙΑΣ",
        "ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙOY ΓΡΗΓΟΡΙΟΥ",
    ), "current monastery and pilgrimage page")
    for url, markers, label in (
        ("https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/"
         "130-apostolou-sila.html",
         ("ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΑΠΟΣΤΟΛΟΥ ΣΙΛΑ", "2510242511", "65500"),
         "Apostle Silas monastery"),
        ("https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/"
         "101-iera-moni.html",
         ("ΙΕΡΑ ΜΟΝΗ ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΜΑΡΙΩΝ ΘΑΣΟΥ",
          "2593051394"),
         "Dormition monastery at Maries"),
        ("https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/"
         "132-agiou-grigoriou.html",
         ("ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙOY ΓΡΗΓΟΡΙΟΥ", "2510316232", "64006"),
         "Saint Gregory pilgrimage"),
        ("https://imfnth.gr/mitropoli/topiki-agiologia/ieres-mones/"
         "131-ludias.html",
         ("ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙΑΣ ΛΥΔΙΑΣ", "2510516944", "64003"),
         "Saint Lydia pilgrimage"),
    ):
        assert_html_markers(url, markers, label)
    for raw in KAVALA_CONTACTS.strip().splitlines():
        dedication, address, phone, postal, suffix = raw.split("|", 4)
        live_address = "Αρκαδίου" if suffix == (
            "127-naos-metamorfoseos.html") else address
        assert_html_markers(KAVALA_BASE + suffix, (
            live_address, phone, postal,
        ), "Kavala parish %s" % dedication)
    for url, markers, label in (
        (LEGAL_PDF_2017, (), "2017 legal recognition"),
        (LEGAL_PDF_2019, (), "2019 legal roster"),
        (LEGAL_PDF_2020, (), "2020 legal amendment"),
    ):
        content_type, payload = fetch_source(url)
        if "pdf" not in content_type or not payload.startswith(b"%PDF"):
            raise ValueError("%s is not a valid PDF" % label)


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
            "Philippoi: %d exact named bodies; %d carry current public "
            "body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Philippoi: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
