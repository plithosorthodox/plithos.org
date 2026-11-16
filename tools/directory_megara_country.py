#!/usr/bin/env python3
"""Build the exact current Megara and Salamis subordinate body roster."""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PARENT = "gr-megara"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "megara_country.json"

BASE = "https://www.immesa.gr"
WP_API = BASE + "/wp-json/wp/v2"
PARISH_URL = BASE + "/enories/"
CHAPEL_URL = BASE + "/mitropolitika-parekklisia/"
MONASTERY_URL = BASE + "/ieres-mones-metoxia/"
PROFILE_URL = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "megaron-kai-salaminos"
)
ADMIN_PDF = (
    "https://www.ecclesiagreece.gr/greek/Dioceses/repository_for_all/"
    "megaron_dioikisis_new.pdf"
)

# Exact current detail title | seat | address | public phone | detail URL.
PARISH_DATA = r"""
Κοίμησις Θεοτόκου|Μέγαρα|Γεωρ. Μενιδιάτη 54;191 00 Μέγαρα|+30 22960-29537|https://www.immesa.gr/arxieratikes-perifereies/koimisis-theotokoy/
Ἁγ. Παρασκευή|Μέγαρα|191 00 Μέγαρα|+30 22960-28305|https://www.immesa.gr/arxieratikes-perifereies/agia-paraskevi-megaron/
Ἅγ. Δημήτριος|Μέγαρα|191 00 Μέγαρα|+30 22960-29423|https://www.immesa.gr/arxieratikes-perifereies/agios-dimitrios/
Ἅγ. Ἰωάννης Θεολόγος|Μελί Μεγάρων|Μελί Μεγάρων;191 00 Μέγαρα|+30 22960-83779|https://www.immesa.gr/arxieratikes-perifereies/g-oannis-theologos/
Ἅγ. Γεώργιος|Νέα Πέραμος|Νέα Πέραμος;190 06|+30 22960-33565|https://www.immesa.gr/arxieratikes-perifereies/g-georgios/
Ἅγ. Παντελεήμων|Βλυχάδα Νέας Περάμου|Βλυχάδα Νέας Περάμου;190 06|+30 22960-33224|https://www.immesa.gr/arxieratikes-perifereies/agios-panteleimon/
Ἅγιος Γεώργιος|Ἐλευσίς|Παγκάλου 40;192 00 Ἐλευσίς|+30 210-554-6545|https://www.immesa.gr/arxieratikes-perifereies/gios-georgios/
Ἅγ. Ἀπόστολοι|Ἐλευσίς|192 00 Ἐλευσίς|+30 210-554-2729|https://www.immesa.gr/arxieratikes-perifereies/g-postoloi/
Ἅγ. Κων/νος καί Ἑλένη|Ἐλευσίς|Πλ. Ἐθν. Ἀντιστάσεως 20;192 00 Ἐλευσίς|+30 210-554-3490|https://www.immesa.gr/arxieratikes-perifereies/g-kon-nos-kai-leni/
Ζωοδ. Πηγή - Ταξιάρχαι Ἀεροδρομίου|Ἐλευσίς|Κερασούντος 26;192 00 Ἐλευσίς|+30 210-554-9077|https://www.immesa.gr/arxieratikes-perifereies/zood-pigi-taxiarchai-erodromioy/
Ἀναλήψεως Χριστοῦ|Μαγούλα|25ης Μαρτίου 1;190 18 Μαγούλα|+30 210-555-5989|https://www.immesa.gr/arxieratikes-perifereies/nalipseos-christo/
Ἅγ. Δημήτριος|Ἀσπρόπυργος|193 00 Ἀσπρόπυργος|+30 210-557-2774|https://www.immesa.gr/arxieratikes-perifereies/g-dimitrios/
Εὐαγγελισμός τῆς Θεοτόκου|Ἀσπρόπυργος|193 00 Ἀσπρόπυργος|+30 210-557-4816|https://www.immesa.gr/arxieratikes-perifereies/evaggelismos-theotokou/
Ἀνάληψις Χριστοῦ|Παραλία Ἀσπροπύργου|Παραλία Ἀσπροπύργου;193 00|+30 210-557-4354|https://www.immesa.gr/arxieratikes-perifereies/nalipsis-christo/
Ἅγ. Χαράλαμπος (Νεοκτίστων)|Νεόκτιστα Ἀσπροπύργου|Ἁγ. Χαραλάμπους 1;Νεόκτιστα Ἀσπροπύργου;193 00|+30 210-559-1714|https://www.immesa.gr/arxieratikes-perifereies/agios-charalampos/
Ἅγ. Κων/νος καί Ἑλένη|Μάνδρα|196 00 Μάνδρα|+30 210-555-5382|https://www.immesa.gr/arxieratikes-perifereies/agios-konstantinos-eleni/
Ἁγ. Παρασκευῆ (Ἐργατ. Κατοικιῶν)|Μάνδρα|Ἐργατικές Κατοικίες Μάνδρας;196 00|+30 210-554-9017|https://www.immesa.gr/arxieratikes-perifereies/g-paraskey-rgat-katoiki-n/
Μεταμ. Σωτῆρος|Βίλλια|190 12 Βίλλια|+30 22630-22236|https://www.immesa.gr/arxieratikes-perifereies/metamorfosi-villia/
Ζωοδόχος Πηγή|Ἀλεποχώριον|Ἀλεποχώριον;190 12|+30 697-201-6616|https://www.immesa.gr/arxieratikes-perifereies/zoodochos-pigi/
Ἁγ. Τριάς|Οἰνόη|190 12 Οἰνόη|+30 22630-51228|https://www.immesa.gr/arxieratikes-perifereies/agia-trias/
Εὐαγγ. Θεοτόκου|Ἐρυθραί|190 08 Ἐρυθραί|+30 22630-62258|https://www.immesa.gr/arxieratikes-perifereies/euagg-theotokou/
Ἅγ. Μηνᾶς|Σαλαμίς|189 00 Σαλαμίς|+30 210-465-1268|https://www.immesa.gr/arxieratikes-perifereies/g-min-s/
Ἅγ. Ἀνδρέας|Σαλαμίς|189 00 Σαλαμίς|+30 210-465-2035|https://www.immesa.gr/arxieratikes-perifereies/agios-andreas/
Ἅγ. Δημήτριος|Σαλαμίς|189 00 Σαλαμίς|+30 210-465-3972|https://www.immesa.gr/arxieratikes-perifereies/agios-dimitrios-salamina/
Ἅγ. Λαυρέντιος|Σαλαμίς|189 00 Σαλαμίς|+30 210-467-6685|https://www.immesa.gr/arxieratikes-perifereies/agios-lavrentios/
Ἅγ. Νικόλαος|Σαλαμίς|189 00 Σαλαμίς|+30 210-465-3710|https://www.immesa.gr/arxieratikes-perifereies/agios-nikolaos/
Ἁγ. Βαρβάρα|Παλούκια Σαλαμῖνος|Παλούκια Σαλαμῖνος;189 00|+30 210-467-2188|https://www.immesa.gr/arxieratikes-perifereies/agia-varvara/
Κοίμησις Θεοτόκου|Καματερό Σαλαμῖνος|Καματερό Σαλαμῖνος;189 00|+30 210-467-3226|https://www.immesa.gr/arxieratikes-perifereies/koimisis-theotokou-salamina/
Κοίμησις Θεοτόκου|Αἰάντειον Σαλαμῖνος|Αἰάντειον Σαλαμῖνος;189 00|+30 210-466-3200|https://www.immesa.gr/arxieratikes-perifereies/koimisis-theotokou-aianteion/
Εἰσόδια Θεοτόκου|Ἀμπελάκια Σαλαμῖνος|Ἀμπελάκια Σαλαμῖνος;189 00|+30 210-467-3729|https://www.immesa.gr/arxieratikes-perifereies/eisodia-theotokou/
Ἅγ. Νικόλαος - Σεληνίων|Σελήνια Σαλαμῖνος|Σελήνια Σαλαμῖνος;189 02|+30 210-467-1717|https://www.immesa.gr/arxieratikes-perifereies/agios-nikolaos-selinion/
Ἁγ. Ζώνη|Κακή Βίγλα Σαλαμῖνος|Κακή Βίγλα Σαλαμῖνος;189 00|+30 210-466-3312|https://www.immesa.gr/arxieratikes-perifereies/agia-zoni/
"""

# Current section rank | exact body identity | seat | address if expressly printed.
CHAPEL_DATA = r"""
Episcopal Residence Chapel|Ἅγιος Λαυρέντιος Παρεκκλησίου Ἐπισκοπείου Μεγάρων|Μέγαρα|
Metropolitan Chapel|Ἁγία Παρασκευή Αἰαντείου Σαλαμῖνος|Αἰάντειον Σαλαμῖνος|
Metropolitan Chapel|Ἅγιος Φανούριος Αἰαντείου Σαλαμῖνος|Αἰάντειον Σαλαμῖνος|
Metropolitan Chapel|Ἅγιος Γεώργιος Πεύκου Σαλαμῖνος|Πεῦκον Σαλαμῖνος|
Metropolitan Chapel|Γέννησις Χριστοῦ Γυάλας Σαλαμῖνος|Γυάλα Σαλαμῖνος|
Pilgrimage Church|Μεταμόρφωσις Σωτῆρος Βιλλιαρίου Μάνδρας|Βιλλιαρί Μάνδρας|
Hospital Church|Εὐαγγελισμός Θεοτόκου Θριασίου|Θριάσιον|
"""

# Exact current identity | seat | address | public phone | detail URL | group.
MONASTERY_DATA = r"""
Προφήτου Ἠλιού Ἐρυθρῶν|Ἐρυθραί|190 08 Ἐρυθραί|+30 697-215-1111|https://www.immesa.gr/ieres-mones-metoxia/profitis-ilias/|men
Παναγίας Γαλακτοτροφούσης Νέας Δάφνης Μεγάρων|Νέα Δάφνη Μεγάρων|191 00 Μέγαρα|+30 697-886-4643|https://www.immesa.gr/ieres-mones-metoxia/panagias-galaktotrofoysis-n-dafnis-megaron/|men
Ἁγίας Παρασκευῆς Μαζίου Μεγάρων|Μάζι Μεγάρων|191 00 Μέγαρα|+30 22960-51750|https://www.immesa.gr/ieres-mones-metoxia/gias-paraskey-s-mazioy-megaron/|men
Ἁγίου Βλασίου Μεγαρίδος|Μέγαρα|191 00 Μέγαρα|+30 694-728-9062|https://www.immesa.gr/ieres-mones-metoxia/gioy-vlasioy-megaridos/|men
Ἁγίας Τριάδος Μυρινίου Μεγαρίδος|Μυρίνιον Μεγαρίδος|191 00 Μέγαρα|+30 698-003-6105|https://www.immesa.gr/ieres-mones-metoxia/gias-triados-myrinioy-megaridos/|men
Παναγίας Ὁδηγητρίας Βασιλικῶν Σαλαμῖνος|Βασιλικά Σαλαμῖνος|189 00 Σαλαμίνα|+30 698-200-3177|https://www.immesa.gr/ieres-mones-metoxia/%cf%80%ce%b1%ce%bd%ce%b1%ce%b3%ce%af%ce%b1%cf%82-%e1%bd%81%ce%b4%ce%b7%ce%b3%ce%b7%cf%84%cf%81%ce%af%ce%b1%cf%82-%ce%b2%ce%b1%cf%83%ce%b9%ce%bb%ce%b9%ce%ba%e1%bf%b6%ce%bd-%cf%83%ce%b1%ce%bb%ce%b1/|men
Ἁγίου Ἱεροθέου Μεγάρων|Μέγαρα|191 00 Μέγαρα|+30 22960-26599|https://www.immesa.gr/ieres-mones-metoxia/agiou-ierotheou/|women
Ὁσίου Μελετίου Κιθαιρῶνος|Οἰνόη|190 12 Οἰνόη|+30 22630-51240|https://www.immesa.gr/ieres-mones-metoxia/meletiou-kithairionos/|women
Παναγίας Φανερωμένης Σαλαμῖνος|Σαλαμίνα|189 00 Σαλαμίνα|+30 210-468-1861|https://www.immesa.gr/ieres-mones-metoxia/panagias-faneromenis/|women
Ἁγίου Γερασίμου Σαλαμῖνος|Σαλαμίνα|189 00 Σαλαμίνα|+30 697-097-0391|https://www.immesa.gr/ieres-mones-metoxia/agiou-gerasimou/|women
Ἁγίου Ἰωάννου Προδρόμου Μακρυνοῦ Μεγάρων|Μέγαρα|191 00 Μέγαρα|+30 22960-51333|https://www.immesa.gr/ieres-mones-metoxia/agiou-ioannou/|women
Προφήτου Ἠλιού Βιλλίων|Βίλλια|190 12 Βίλλια|+30 217-700-1068|https://www.immesa.gr/ieres-mones-metoxia/profitou-iliou-vilion/|women
Παναγίας Γοργοεπηκόου Μάνδρας|Μάνδρα|196 00 Μάνδρα|+30 690-613-0914|https://www.immesa.gr/ieres-mones-metoxia/panagias-gorgoepikooy-mandras/|women
Ἁγίου Νικολάου Λεμονίων Σαλαμῖνος|Λεμόνια Σαλαμῖνος|189 00 Σαλαμίνα|+30 210-466-2380|https://www.immesa.gr/ieres-mones-metoxia/agiou-nikolaou-lemonion/|women
Παναγίας Εὐαγγελιστρίας καί Ἁγίου Δαυίδ Μάνδρας|Μάνδρα|196 00 Μάνδρα|+30 210-555-6062|https://www.immesa.gr/ieres-mones-metoxia/panagia-evaggelistria/|women
Ἁγίας Αἰκατερίνης Σαλαμῖνος|Σαλαμίνα|Ἁγίας Αἰκατερίνης;189 00 Σαλαμίνα||https://www.immesa.gr/ieres-mones-metoxia/g-a-katerinis-salam-nos/|women
"""

# Exact current dependency | seat | address if expressly printed.
METOCHION_DATA = r"""
Ἅγιος Σάββας, Μετόχιον Ἱερᾶς Μονῆς Παναγίας Γαλακτοτροφούσης|Μέγαρα|
Ὑπεραγία Θεοτόκος, Μετόχιον Ἱερᾶς Μονῆς Ἁγίου Βλασίου|Βλυχάδα Μεγάρων|
Ἁγία Παρασκευή, Μετόχιον Ἱερᾶς Μονῆς Ὁσίου Μελετίου|Ἀθήνα|Αἰόλου 62;Ἀθήνα
Ἁγία Βαρβάρα, Μετόχιον Ἱερᾶς Μονῆς Ἁγίου Ἱεροθέου|Μέγαρα|
Ἅγιος Λουκᾶς, Μετόχιον Ἱερᾶς Μονῆς Ἁγίου Ἱεροθέου|Μέγαρα|
Ἁγία Τριάς, Μετόχιον Ἱερᾶς Μονῆς Παναγίας Φανερωμένης|Βουρκάρι Σαλαμῖνος|
Ἅγιος Γεώργιος, Μετόχιον Ἱερᾶς Μονῆς Παναγίας Φανερωμένης|Ἅγιος Στέφανος Ἀττικῆς|
"""

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
CLERGY_TERMS = re.compile(
    r"\b(?:Ἀρχιμανδρίτης|Αρχιμανδρίτης|Ἀρχιμ|Αρχιμ|Πρωτοπρεσβύτερος|"
    r"Πρωτοπρ|Πρεσβύτερος|Διάκονος|Ἡγούμενος|Ηγούμενος|Ἡγουμένη|"
    r"Ηγουμένη|Μοναχός|Μοναχή)\b",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"^\+30 (?:\d{3}-\d{3}-\d{4}|\d{5}-\d{5})$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

TRANSLIT = str.maketrans({
    "Α":"A","Β":"V","Γ":"G","Δ":"D","Ε":"E","Ζ":"Z","Η":"I","Θ":"Th","Ι":"I",
    "Κ":"K","Λ":"L","Μ":"M","Ν":"N","Ξ":"X","Ο":"O","Π":"P","Ρ":"R","Σ":"S",
    "Τ":"T","Υ":"Y","Φ":"F","Χ":"Ch","Ψ":"Ps","Ω":"O",
    "α":"a","β":"v","γ":"g","δ":"d","ε":"e","ζ":"z","η":"i","θ":"th","ι":"i",
    "κ":"k","λ":"l","μ":"m","ν":"n","ξ":"x","ο":"o","π":"p","ρ":"r","σ":"s",
    "ς":"s","τ":"t","υ":"y","φ":"f","χ":"ch","ψ":"ps","ω":"o",
})

RANK_LABELS = {
    "Parish Church": "Parish Church",
    "Episcopal Residence Chapel": "Episcopal Residence Chapel",
    "Metropolitan Chapel": "Metropolitan Chapel",
    "Pilgrimage Church": "Pilgrimage Church",
    "Hospital Church": "Hospital Church",
    "Monastery": "Monastery",
    "Metochion": "Metochion",
}

ROW_ALLOWED_HOSTS = {
    "www.immesa.gr", "immesa.gr", "www.ecclesiagreece.gr", "ecclesiagreece.gr",
}
LEDGER_ALLOWED_HOSTS = ROW_ALLOWED_HOSTS | {
    "profitisiliaserythron.blogspot.com",
    "attiki.topodigos.gr",
    "salamina.eu",
    "gorgoepikoos.gr",
    "www.iaath.gr",
}


def parse_pipe_rows(block, expected):
    rows = []
    for number, line in enumerate(block.strip().splitlines(), 1):
        fields = [value.strip() for value in line.split("|")]
        if len(fields) != expected:
            raise ValueError(
                "raw row %d has %d fields, expected %d" % (number, len(fields), expected)
            )
        rows.append(fields)
    return rows


def romanize(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value.translate(TRANSLIT)).strip()


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", romanize(value).casefold()).strip("-") or "body"


def english_name(local, seat, rank):
    title = romanize(local)
    seat_name = romanize(seat)
    if seat_name.casefold() not in title.casefold():
        title += ", " + seat_name
    return "%s %s" % (title, RANK_LABELS[rank])


def address_parts(value):
    if not value:
        return []
    parts = [part.strip() for part in value.split(";") if part.strip()]
    if parts[-1] != "Ελλάδα":
        parts.append("Ελλάδα")
    return parts


def make_row(rank, local, seat, address, phones, sources, contact_sources):
    item = {
        "parent": PARENT,
        "kind": "monastery" if rank in ("Monastery", "Metochion") else "parish",
        "rank": rank,
        "name": english_name(local, seat, rank),
        "local": local,
        "seat": romanize(seat),
        "country": "GR",
        "sources": list(dict.fromkeys(sources)),
    }
    if address:
        item["address"] = address_parts(address)
    if phones:
        item["phones"] = [value.strip() for value in phones.split(",") if value.strip()]
    if item.get("phones") or item.get("emails") or item.get("site"):
        item["contact_sources"] = list(dict.fromkeys(contact_sources))
        item["contact_checked"] = CHECKED
    return item


def make_rows():
    rows = []
    parish_rows = parse_pipe_rows(PARISH_DATA, 5)
    if len(parish_rows) != 32:
        raise ValueError("parish source table drifted: %d" % len(parish_rows))
    for local, seat, address, phone, detail in parish_rows:
        rows.append(make_row(
            "Parish Church", local, seat, address, phone,
            [detail, PARISH_URL, ADMIN_PDF], [detail],
        ))

    chapel_rows = parse_pipe_rows(CHAPEL_DATA, 4)
    if len(chapel_rows) != 7:
        raise ValueError("chapel source table drifted: %d" % len(chapel_rows))
    for rank, local, seat, address in chapel_rows:
        if rank not in RANK_LABELS:
            raise ValueError("unknown chapel rank: %s" % rank)
        rows.append(make_row(
            rank, local, seat, address, "", [CHAPEL_URL, ADMIN_PDF], [],
        ))

    monastery_rows = parse_pipe_rows(MONASTERY_DATA, 6)
    if len(monastery_rows) != 16:
        raise ValueError("monastery source table drifted: %d" % len(monastery_rows))
    group_counts = Counter()
    for local, seat, address, phone, detail, group in monastery_rows:
        if group not in ("men", "women"):
            raise ValueError("unknown monastery group: %s" % group)
        group_counts[group] += 1
        rows.append(make_row(
            "Monastery", local, seat, address, phone,
            [detail, MONASTERY_URL, ADMIN_PDF], [detail],
        ))
    if group_counts != Counter({"women": 10, "men": 6}):
        raise ValueError("monastery sex grouping drifted: %r" % dict(group_counts))

    metochion_rows = parse_pipe_rows(METOCHION_DATA, 3)
    if len(metochion_rows) != 7:
        raise ValueError("metochion source table drifted: %d" % len(metochion_rows))
    for local, seat, address in metochion_rows:
        rows.append(make_row(
            "Metochion", local, seat, address, "",
            [MONASTERY_URL, ADMIN_PDF], [],
        ))

    for index, item in enumerate(rows, 1):
        item["id"] = "gr-megara-%03d-%s" % (
            index, slug(item["local"] + " " + item["seat"]),
        )
    return rows


ROWS = make_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 62
EXPECTED_OWNER_COUNTS = {PARENT: 62}
EXPECTED_KINDS = {"monastery": 23, "parish": 39}
EXPECTED_RANKS = {
    "Episcopal Residence Chapel": 1,
    "Hospital Church": 1,
    "Metochion": 7,
    "Metropolitan Chapel": 4,
    "Monastery": 16,
    "Parish Church": 32,
    "Pilgrimage Church": 1,
}
EXPECTED_COVERAGE = (47, 47, 47, 0, 0, 0, 49)
EXISTING_PARENTS = {PARENT}


def validate_url(value, label, allowed_hosts=ROW_ALLOWED_HOSTS):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc.casefold() not in allowed_hosts:
        raise ValueError("%s carries an unaudited source: %s" % (label, value))


def clean(source):
    item = {key: value for key, value in source.items() if value not in (None, "", [])}
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must carry one to three sources" % item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)

    contact_sources = list(item.get("contact_sources") or [])
    has_contact = bool(item.get("phones") or item.get("emails") or item.get("site"))
    if has_contact:
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks exact current contact provenance" % item.get("id"))
    elif contact_sources or item.get("contact_checked"):
        raise ValueError(
            "%s carries contact audit metadata without a phone, email, or site" % item.get("id")
        )
    if len(contact_sources) > 3:
        raise ValueError("%s carries too many contact sources" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
    for phone in item.get("phones") or []:
        if not PHONE_RE.fullmatch(phone):
            raise ValueError("%s carries malformed phone %s" % (item.get("id"), phone))
    for email in item.get("emails") or []:
        if not EMAIL_RE.fullmatch(email):
            raise ValueError("%s carries malformed email %s" % (item.get("id"), email))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] in sources:
            raise ValueError("%s mixes its direct site with higher-level sources" % item.get("id"))
    return item


def coverage_tuple(rows):
    return (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site")) for item in rows),
        sum(bool(item.get("phones")) for item in rows),
        sum(len(item.get("phones") or []) for item in rows),
        sum(bool(item.get("emails")) for item in rows),
        sum(len(item.get("emails") or []) for item in rows),
        sum(bool(item.get("site")) for item in rows),
        sum(bool(item.get("address")) for item in rows),
    )


def validate_ledger(expected_coverage=None):
    text = CANDIDATE_LEDGER.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        raise ValueError("Megara candidate ledger lacks a final newline")
    if FORBIDDEN_PUNCTUATION.search(text):
        raise ValueError("Megara candidate ledger carries forbidden punctuation")
    ledger = json.loads(text)
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Megara candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Megara candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_parishes": 32,
        "current_episcopal_residence_chapels": 1,
        "current_metropolitan_chapels": 4,
        "current_pilgrimages": 1,
        "current_hospital_churches": 1,
        "current_monasteries": 16,
        "current_male_monasteries": 6,
        "current_female_monasteries": 10,
        "current_metochia": 7,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Megara ledger summary drifted at %s" % key)
    if expected_coverage is not None:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites", "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Megara ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Megara candidate ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Megara ledger item has invalid sources")
            for source_url in sources:
                validate_url(
                    source_url,
                    entry.get("candidate_id") or entry.get("id") or key,
                    LEDGER_ALLOWED_HOSTS,
                )
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Megara candidate IDs repeat")
    return ledger


def build():
    ids = set()
    signatures = {}
    owner_counts = Counter()
    kind_counts = Counter()
    rank_counts = Counter()
    result = []
    for source in ROWS:
        item = clean(source)
        row_id = item["id"]
        if row_id in ids:
            raise ValueError("duplicate Megara ID: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has wrong country" % row_id)
        if item.get("kind") not in ("parish", "monastery"):
            raise ValueError("%s has invalid kind" % row_id)
        if item.get("rank") not in RANK_LABELS:
            raise ValueError("%s has invalid rank" % row_id)
        for field in ("name", "local", "seat", "rank"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        rendered = json.dumps(item, ensure_ascii=False)
        if FORBIDDEN_PUNCTUATION.search(rendered):
            raise ValueError("%s carries forbidden punctuation" % row_id)
        if CLERGY_TERMS.search(rendered):
            raise ValueError("%s carries a clergy or monastic personal title" % row_id)
        signature = unicodedata.normalize(
            "NFKC", "%s|%s|%s" % (item["local"], item["seat"], item["rank"])
        ).casefold()
        signature = re.sub(r"\s+", " ", signature).strip()
        if signature in signatures:
            raise ValueError("%s duplicates %s" % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[item["parent"]] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)

    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Megara English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Megara English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Megara parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Megara kind totals drifted: %r" % dict(kind_counts))
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Megara rank totals drifted: %r" % dict(rank_counts))
    coverage = coverage_tuple(result)
    if coverage != EXPECTED_COVERAGE:
        raise ValueError("Megara contact coverage drifted: %r" % (coverage,))
    validate_ledger(coverage)
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_bytes(url, expected=None):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "application/json,text/html,application/pdf;q=0.9,*/*;q=0.8",
        "Connection": "close",
    })
    last_error = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                content_type = response.headers.get("Content-Type", "").casefold()
                payload = response.read()
            if expected and expected not in content_type:
                raise ValueError("unexpected content type at %s: %s" % (url, content_type))
            return payload
        except HTTPError as exc:
            last_error = exc
            if exc.code not in (429, 500, 502, 503, 504):
                raise
        except (URLError, TimeoutError) as exc:
            last_error = exc
        if attempt < 2:
            time.sleep(2 + attempt * 2)
    raise ValueError("live URL failed at %s: %s" % (url, last_error))


def fetch_json(url):
    return json.loads(fetch_bytes(url, "json").decode("utf-8"))


def fetch_text(url):
    return fetch_bytes(url, "html").decode("utf-8", "replace")


def check_markers(payload, url, markers):
    text = normalize_source_text(payload)
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("live Megara marker failed at %s: %s" % (url, marker))


def category_map():
    categories = fetch_json(WP_API + "/categories?per_page=100")
    return {item["slug"]: item for item in categories}


def category_posts(category):
    return fetch_json(
        WP_API + "/posts?per_page=100&categories=%d" % int(category["id"])
    )


def check_live_sources():
    pages = fetch_json(WP_API + "/pages?per_page=100")
    page_ids = {item["id"]: item for item in pages}
    if len(pages) != 12 or not {275, 292, 358}.issubset(page_ids):
        raise ValueError("live Megara page inventory drifted")
    if page_ids[275]["slug"] != "enories":
        raise ValueError("live parish page slug drifted")
    if page_ids[292]["slug"] != "mitropolitika-parekklisia":
        raise ValueError("live chapel page slug drifted")
    if page_ids[358]["slug"] != "ieres-mones-metoxia":
        raise ValueError("live monastery page slug drifted")

    categories = category_map()
    expected_category_counts = {
        "arxieratikes-perifereies": 32,
        "a-arxieratiki-perifereia": 6,
        "b-arxieratiki-perifereia": 9,
        "c-arxieratiki-perifereia": 6,
        "d-archieratiki-perifereia": 11,
        "ieres-mones-metoxia": 16,
        "androai": 6,
        "gynaikeiai": 10,
    }
    for slug_name, count in expected_category_counts.items():
        if slug_name not in categories or categories[slug_name]["count"] != count:
            raise ValueError("live category count drifted at %s" % slug_name)

    parish_posts = category_posts(categories["arxieratikes-perifereies"])
    monastery_posts = category_posts(categories["ieres-mones-metoxia"])
    parish_urls = {fields[4] for fields in parse_pipe_rows(PARISH_DATA, 5)}
    monastery_urls = {fields[4] for fields in parse_pipe_rows(MONASTERY_DATA, 6)}
    if {item["link"] for item in parish_posts} != parish_urls:
        raise ValueError("live parish detail URL inventory drifted")
    if {item["link"] for item in monastery_posts} != monastery_urls:
        raise ValueError("live monastery detail URL inventory drifted")

    parish_page = fetch_json(WP_API + "/pages/275")["content"]["rendered"]
    if len(re.findall(r'<article id="post-\d+"', parish_page)) != 32:
        raise ValueError("live parish card count drifted")
    check_markers(parish_page, PARISH_URL, (
        "Κοίμησις Θεοτόκου", "Ἅγ. Χαράλαμπος (Νεοκτίστων)",
        "Ἅγ. Νικόλαος - Σεληνίων", "Ἁγ. Ζώνη",
    ))

    chapel_page = fetch_json(WP_API + "/pages/292")["content"]["rendered"]
    check_markers(chapel_page, CHAPEL_URL, (
        "Παρεκκλήσιον Ἐπισκοπείου Μεγάρων", "Ἁγ. Λαυρεντίου",
        "Ἁγ. Παρασκευῆς - Αἰαντείου Σαλαμῖνος",
        "Ἁγ. Φανουρίου - Αἰαντείου Σαλαμῖνος",
        "Ἁγ. Γεωργίου - Πεῦκον Σαλαμῖνος",
        "Γεννήσεως Χριστοῦ - Γυάλας Σαλαμῖνος",
        "Μεταμορφώσεως Σωτῆρος - Βιλλιαρί Μάνδρας",
        "Εὐαγγελισμοῦ Θεοτόκου - Θριασίου",
    ))

    monastery_page = fetch_json(WP_API + "/pages/358")["content"]["rendered"]
    check_markers(monastery_page, MONASTERY_URL, (
        "Ἀνδρῷαι", "Γυναικεῖαι", "Παναγίας Ὁδηγητρίας Βασιλικῶν Σαλαμῖνος",
        "Μετόχιον Ἱ. Μονῆς Παναγίας Γαλακτοτροφούσης",
        "Ἁγία Παρασκευή εἰς Ἀθήνας (Αἰόλου 62)",
        "Ἁγία Τριάς εἰς Βουρκάρι", "Ἅγιος Γεώργιος εἰς Ἅγιον Στέφανον Ἀττικῆς",
        "Διαλελυμέναι Ἱ. Μοναί", "Ἁγ. Γεωργίου - Κάστρο Πόρτο Γερμενοῦ",
    ))

    profile = fetch_text(PROFILE_URL)
    check_markers(profile, PROFILE_URL, (
        "Μεγάρων και Σαλαμίνος", "Ἁγίου Λαυρεντίου 1", "www.immesa.gr",
    ))
    pdf = fetch_bytes(ADMIN_PDF, "pdf")
    if not pdf.startswith(b"%PDF") or len(pdf) < 100000:
        raise ValueError("live Church of Greece administrative PDF is invalid")
    build()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        check_live_sources()
        print("Megara live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Megara check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
