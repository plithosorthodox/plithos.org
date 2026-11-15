#!/usr/bin/env python3
"""Validate exact named Zihna and Nevrokopion bodies.

    python tools/directory_zihna_country.py --check
    python tools/directory_zihna_country.py --dump
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
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "zihna_country.json"
)
PARENT = "ep-zihna"
REGULATION_PAGE = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-zixnon-neyrokopioy/"
)


PARISH_ROWS = r'''
ΝΕΑ ΖΙΧΝΗ|Nea Zichni|Αγίου Γεωργίου|Saint George
ΑΓ. ΧΡΙΣΤΟΦΟΡΟΣ|Agios Christophoros|Αγίου Χαραλάμπους|Saint Charalambos
ΑΓΡΙΑΝΗ|Agriani|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΑΝΑΣΤΑΣΙΑ|Anastasia|Αγίας Αναστασίας|Saint Anastasia
ΓΑΖΩΡΟΣ|Gazoros|Αγίου Παντελεήμονος|Saint Panteleimon
ΔΑΦΝΟΥΔΙ|Dafnoudi|Αγίου Αθανασίου|Saint Athanasius
ΔΗΜΗΤΡΑ|Dimitra|Αγίου Γεωργίου|Saint George
ΔΟΜΙΡΟΣ|Domiross|Αγίου Γεωργίου|Saint George
ΘΟΛΟΣ|Tholos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΜΕΣΟΡΡΑΧΗ|Mesorrachi|Αγίου Αθανασίου|Saint Athanasius
ΜΥΡΙΝΗ|Myrini|Αγίου Γεωργίου|Saint George
ΝΕΑ ΠΕΤΡΑ|Nea Petra|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΠΕΘΕΛΙΝΟΣ|Pethelinos|Αγίου Νικολάου|Saint Nicholas
ΣΦΕΛΙΝΟΣ|Sfelinos|Αγίας Τριάδος|Holy Trinity
ΤΟΥΜΠΑ|Toumba|Αγίου Γεωργίου|Saint George
ΑΛΙΣΤΡΑΤΗ|Alistrati|Αγίου Αθανασίου|Saint Athanasius
ΑΓΙΟΧΩΡΙ|Agiochori|Αγίου Γεωργίου|Saint George
ΑΓΓΙΣΤΑ|Angista|Τιμίου Προδρόμου|Saint John the Forerunner
Σ.Σ. ΑΓΓΙΣΤΑΣ|Angista Railway Station|Τιμίου Σταυρού|Holy Cross
ΗΛΙΟΚΩΜΗ|Iliokomi|Ζωοδόχου Πηγής|Life-Giving Spring
ΚΟΡΜΙΣΤΑ|Kormista|Προφήτου Ηλιού|Prophet Elijah
ΚΡΗΝΙΔΑ|Krinida|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΛΕΥΚΟΘΕΑ|Lefkothea|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Σ.Σ. ΛΕΥΚΟΘΕΑΣ|Lefkothea Railway Station|Αγίου Γεωργίου|Saint George
ΜΑΝΔΗΛΙΟΝ|Mandilion|Αγίας Κυριακής|Saint Kyriaki
Ν. ΜΠΑΦΡΑ|Nea Bafra|Μεταμορφώσεως Σωτήρος|Transfiguration of the Savior
ΣΚΟΠΙΑ|Skopia|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΣΥΜΒΟΛΗ|Symvoli|Αγίου Αθανασίου|Saint Athanasius
ΔΡΑΒΗΣΚΟΣ|Draviskos|Αγίου Αθανασίου|Saint Athanasius
ΔΡΑΒΗΣΚΟΣ|Draviskos|Μεταμορφώσεως Σωτήρος|Transfiguration of the Savior
ΑΜΦΙΠΟΛΙΣ|Amphipolis|Αγ. Αποστόλου Παύλου|Apostle Paul
ΜΑΥΡΟΛΟΦΟΣ|Mavrolofos|Αγίων Αναργύρων|Holy Unmercenaries
ΜΕΣΟΛΑΚΚΙΑ|Mesolakkia|Αγίου Αθανασίου|Saint Athanasius
Ν. ΜΕΣΟΛΑΚΚΙΑ|Nea Mesolakkia|Αγίων Τριών Ιεραρχών|Three Hierarchs
ΜΙΚΡΟΝ ΣΟΥΛΙΟΝ|Mikron Soulion|Αγίου Γεωργίου|Saint George
ΜΥΡΚΙΝΟΣ|Myrkinos|Παναγίας Βλαχερνών|Panagia Blachernae
ΝΕΑ ΦΥΛΗ|Nea Fyli|Αγίου Δημητρίου|Saint Demetrius
ΠΑΛΑΙΟΚΩΜΗ|Palaiokomi|Τιμίου Σταυρού|Holy Cross
ΠΑΛΑΙΟΚΩΜΗ|Palaiokomi|Αγίου Γεωργίου|Saint George
ΠΡΩΤΗ|Proti|Αγίας Παρασκευής|Saint Paraskevi
ΡΟΔΟΛΙΒΟΣ|Rodolivos|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΡΟΔΟΛΙΒΟΣ|Rodolivos|Παμμεγίστων Ταξιαρχών|Holy Archangels
Κ. ΝΕΥΡΟΚΟΠΙΟΝ|Kato Nevrokopi|Αγίου Δημητρίου|Saint Demetrius
ΑΧΛΑΔΙΑ|Achladia|Αγίου Χαραλάμπους|Saint Charalambos
ΑΧΛΑΔΟΜΗΛΙΑ|Achladomilia|Αγίου Γεωργίου|Saint George
ΒΑΘΥΤΟΠΟΣ|Vathytopos|Αγίου Νικολάου|Saint Nicholas
ΔΑΣΩΤΟΝ|Dasoto|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΔΕΛΤΑ|Delta|Αγίου Γεωργίου|Saint George
ΕΞΟΧΗ|Exochi|Αγίου Αθανασίου|Saint Athanasius
ΚΑΤΑΦΥΤΟΝ|Katafyto|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
Κ. ΒΡΟΝΤΟΥ|Kato Vrontou|Αγίων Θεοδώρων|Holy Theodore Martyrs
ΛΕΥΚΟΓΕΙΑ|Lefkogeia|Τιμίου Προδρόμου|Saint John the Forerunner
ΜΙΚΡΟΚΛΕΙΣΟΥΡΑ|Mikrokleisoura|Αγίου Γεωργίου|Saint George
ΜΙΚΡΟΜΗΛΙΑ|Mikromilia|Αγίου Παντελεήμονος|Saint Panteleimon
ΟΧΥΡΟΝ|Ochyro|Αγίου Δημητρίου|Saint Demetrius
ΠΑΓΟΝΕΡΙΟΝ|Pagoneri|Εισοδίων Θεοτόκου|Entry of the Theotokos
ΠΕΡΑΣΜΑ|Perasma|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΠΕΡΙΘΩΡΙΟΝ|Perithorio|Αγίου Νικολάου|Saint Nicholas
ΠΟΤΑΜΟΙ|Potamoi|Αγίων Κωνσταντίνου και Ελένης|Saints Constantine and Helen
ΧΡΥΣΟΚΕΦΑΛΟΣ|Chrysokefalos|Γεννήσεως Θεοτόκου|Nativity of the Theotokos
ΑΝΘΟΧΩΡΙΟΝ|Anthochori|Αγίου Γεωργίου|Saint George
ΓΡΑΜΜΕΝΗ|Grammene|Γεννήσεως Θεοτόκου|Nativity of the Theotokos
ΚΑΛΗ ΒΡΥΣΗ|Kali Vrysi|Αγίου Νικολάου|Saint Nicholas
ΚΑΛΛΙΘΕΑ|Kallithea|Αγίου Αθανασίου|Saint Athanasius
ΜΙΚΡΟΠΟΛΙΣ|Mikropolis|Ευαγγελισμού Θεοτόκου|Annunciation of the Theotokos
ΜΙΚΡΟΠΟΛΙΣ|Mikropolis|Τιμίου Σταυρού|Holy Cross
ΠΑΝΟΡΑΜΑ|Panorama|Κοιμήσεως Θεοτόκου|Dormition of the Theotokos
ΠΕΡΙΧΩΡΑ|Perichora|Αγίου Δημητρίου|Saint Demetrius
ΧΑΡΙΤΩΜΕΝΗ|Charitomeni|Αγίου Γεωργίου|Saint George
'''


MONASTERY_ROWS = [
    ("Ἁγίας Τριάδος Τούμπας", "Holy Trinity", "Toumba",
     "2321071668"),
    ("Ἁγίας Κυριακῆς Ἀλιστράτης", "Saint Kyriaki", "Alistrati",
     "2324031499"),
    ("Ἁγίας Παρασκευῆς Δομίρου", "Saint Paraskevi", "Domiros",
     "2324071362"),
    ("Ἁγίου Μηνᾶ Περιχώρας", "Saint Menas", "Perichora",
     "23240-31519"),
    ("Ἀναλήψεως Χριστοῦ Πρώτης", "Ascension of Christ", "Proti",
     "2324061249"),
]


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
    return "%s of %s, %s" % (rank, dedication, seat)


def build_rows():
    rows = []
    index = 0
    parish_lines = PARISH_ROWS.strip().splitlines()
    if len(parish_lines) != 69:
        raise ValueError("expected 69 regulated Zihna parishes")
    for raw in parish_lines:
        local_seat, seat, local_dedication, dedication = raw.split("|", 3)
        rank = "Parish Church"
        name = make_name(dedication, rank, seat)
        index += 1
        rows.append({
            "id": "gr-ep-zihna-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (local_dedication, local_seat),
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [REGULATION_PAGE],
        })
    for local, dedication, seat, phone in MONASTERY_ROWS:
        rank = "Monastery"
        name = make_name(dedication, rank, seat)
        index += 1
        rows.append({
            "id": "gr-ep-zihna-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "phones": [phone],
            "sources": [PATRIARCHATE_PAGE],
            "contact_sources": [PATRIARCHATE_PAGE],
            "contact_checked": CHECKED,
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 74
EXPECTED_OWNER_COUNTS = {PARENT: 74}
EXPECTED_KINDS = {"monastery": 5, "parish": 69}
EXPECTED_RANKS = {"Monastery": 5, "Parish Church": 69}
EXPECTED_CONTACT_BODIES = 5
EXPECTED_PHONE_BODIES = 5
EXPECTED_PHONE_VALUES = 5
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 74
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
    allowed = {"ecclesiagreece.gr", "www.ecclesiagreece.gr",
               "ec-patr.org", "www.ec-patr.org"}
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
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Zihna candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Zihna candidate ledger date drifted")
    expected_summary = {
        PARENT: 74,
        "total": 74,
        "parish_kind_rows": 69,
        "monastery_kind_rows": 5,
        "contact_bodies": 5,
        "phone_bodies": 5,
        "public_phone_values": 5,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 74,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Zihna ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Zihna ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Zihna ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not x or not re.fullmatch(r"[a-z0-9-]+", x)
           for x in candidate_ids):
        raise ValueError("Zihna ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Zihna ledger has forbidden punctuation")
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
        raise ValueError("Zihna English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Zihna rank totals drifted")
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Zihna kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Zihna parent totals drifted")
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
        raise ValueError("Zihna contact coverage drifted: %r" % (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Zihna: 74 exact bodies; 69 parishes and 5 monasteries")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Zihna: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
