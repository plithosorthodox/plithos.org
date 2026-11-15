#!/usr/bin/env python3
"""Validate exact named Elassona bodies from current first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_elassona_country.py --check
    python tools/directory_elassona_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "elassona_country.json"
)
PARENT = "ep-elassona"
ROSTER_PAGE = (
    "https://imelassonos.gr/"
    "%E1%BC%90%CE%BD%CE%BF%CF%81%CE%B9%CE%B1%CE%BA%CE%BF%CE%AF-"
    "%E1%BC%B1%CE%B5%CF%81%CE%BF%E1%BD%B6-"
    "%CE%BD%CE%B1%CE%BF%E1%BD%B6/"
)
ADMIN_PAGE = (
    "https://imelassonos.gr/"
    "%CE%B4%CE%B9%CE%BF%CE%AF%CE%BA%CE%B7%CF%83%CE%B7/"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-elassonos/"
)
REGULATION_PAGE = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/"
    "2019_aprilios.pdf"
)


PARISH_ROWS = r'''
Ελασσών Μητροπολιτικός|Elasson|Άγιος Δημήτριος|Saint Demetrius|24930 23611|Metropolitan Cathedral
Ελασσών - Βαρόσι|Elasson, Varosi|Εισόδια της Θεοτόκου|Entry of the Theotokos|24930 22723|Parish Church
Ελασσών|Elasson|Άγιος Σπυρίδων|Saint Spyridon|24930 23272|Parish Church
Ελασσών|Elasson|Άγιος Αρσένιος|Saint Arsenios|24930 24020;24930 24463|Parish Church
Αγιονέριον|Agioneri|Αγίες Σοφία, Πίστη και Ελπίδα|Saints Sophia, Faith, and Hope||Parish Church
Αετοράχη|Aetorachi|Άγιοι Ανάργυροι|Holy Unmercenaries||Parish Church
Άκρη|Akri|Μεταμόρφωση του Σωτήρος|Transfiguration of the Savior||Parish Church
Αμούριον|Amouri|Αγία Παρασκευή|Saint Paraskevi||Parish Church
Αμπέλια|Ampelia|Άγιοι Πάντες|All Saints|24920 81191|Parish Church
Ανάληψις|Analipsi|Άγιος Χαράλαμπος|Saint Charalambos|24930 24653|Parish Church
Ασπρόχωμα|Asprochoma|Άγιος Γεώργιος|Saint George||Parish Church
Άζωρος|Azoros|Άγιος Γεώργιος|Saint George|24930 82250|Parish Church
Βαλανίδα|Valanida|Αγία Τριάς|Holy Trinity||Parish Church
Βερδικούσια|Verdikousia|Προφήτης Ηλίας|Prophet Elijah||Parish Church
Βλαχογιάννιον|Vlachogianni|Αγία Τριάς|Holy Trinity|24920 91107|Parish Church
Γαλανόβρυση|Galanovrysi|Άγιος Γεώργιος|Saint George|24930 23518|Parish Church
Γεράνεια|Geraneia|Αγία Τριάς|Holy Trinity|24930 94241|Parish Church
Γήλοφος|Gilofos|Άγιος Δημήτριος|Saint Demetrius||Parish Church
Γιαννωτά|Giannota|Άγιος Νικόλαος|Saint Nicholas|24930 62279|Parish Church
Δαμάσιον|Damasio|Άγιος Νικόλαος|Saint Nicholas|24920 66204|Parish Church
Δασοχώριον|Dasochori|Άγιοι Απόστολοι|Holy Apostles|24920 32023|Parish Church
Δεσκάτη|Deskati|Άγιος Κωνσταντίνος|Saint Constantine|24620 32705|Parish Church
Δεσκάτη|Deskati|Άγιος Αθανάσιος|Saint Athanasius|24620 32109|Parish Church
Δολίχη|Dolichi|Μεταμόρφωση του Σωτήρος|Transfiguration of the Savior|24930 92335|Parish Church
Δομένικον|Domeniko|Παμμέγιστοι Ταξιάρχες|Holy Archangels|24930 87020|Parish Church
Δρυμός|Drymos|Προφήτης Ηλίας|Prophet Elijah||Parish Church
Ευαγγελισμός|Evangelismos|Ευαγγελισμός της Θεοτόκου|Annunciation of the Theotokos|24930 83057|Parish Church
Καλλιθέα|Kallithea|Άγιος Γεώργιος|Saint George|24930 61107|Parish Church
Καλύβια|Kalyvia|Άγιος Γεώργιος|Saint George||Parish Church
Καρυά|Karya|Άγιος Νικόλαος|Saint Nicholas|23520 91045|Parish Church
Κεφαλόβρυσον|Kefalovryso|Άγιος Δημήτριος|Saint Demetrius|24930 95403|Parish Church
Κλεισούρα|Kleisoura|Πέτρου και Παύλου|Saints Peter and Paul|24930 95479|Parish Church
Κοκκινόγειον|Kokkinogeio|Άγιος Αντώνιος|Saint Anthony|24930 61267|Parish Church
Κοκκινοπηλός|Kokkinopilos|Αγία Παρασκευή|Saint Paraskevi||Parish Church
Κρανέα|Kranea|Άγιος Δημήτριος|Saint Demetrius|24930 51498|Parish Church
Κρυόβρυση|Kryovrysi|Άγιος Δημήτριος|Saint Demetrius||Parish Church
Λιβάδιον|Livadi|Κοίμησις της Θεοτόκου|Dormition of the Theotokos|24930 41146|Parish Church
Λιβάδιον|Livadi|Άγιος Κωνσταντίνος|Saint Constantine|24930 41576|Parish Church
Λιβάδιον|Livadi|Άγιοι Ανάργυροι|Holy Unmercenaries|24930 41736|Parish Church
Λουτρόν|Loutro|Άγιος Νικόλαος|Saint Nicholas|24930 51447|Parish Church
Λόφος|Lofos|Άγιος Νικόλαος|Saint Nicholas|24930 61130|Parish Church
Λυκούδιον|Lykoudi|Αγία Παρασκευή|Saint Paraskevi||Parish Church
Μαγούλα|Magoula|Άγιος Γεώργιος|Saint George||Parish Church
Μέγα Ελευθεροχώριον|Mega Eleftherochori|Άγιος Νικόλαος|Saint Nicholas||Parish Church
Μεσοχώριον|Mesochori|Άγιος Δημήτριος|Saint Demetrius|24920 91106|Parish Church
Μηλέα|Milea|Άγιος Αθανάσιος|Saint Athanasius|24930 94296|Parish Church
Μικρόν Ελευθεροχώριον|Mikro Eleftherochori|Αγία Παρασκευή|Saint Paraskevi|24930 61513|Parish Church
Ολυμπιάδα|Olympiada|Άγιος Γεώργιος|Saint George|24930 23024|Parish Church
Παλαιόκαστρον|Palaiokastro|Άγιος Νικόλαος|Saint Nicholas||Parish Church
Παρασκευή|Paraskevi|Άγιος Ιωάννης ο Χρυσόστομος|Saint John Chrysostom|24620 32019|Parish Church
Πραιτώριον|Praitorio|Άγιος Νικόλαος|Saint Nicholas|24930 83380|Parish Church
Πύθιον|Pythio|Τίμιος Πρόδρομος|Saint John the Forerunner|24930 92009|Parish Church
Σαραντάπορον|Sarantaporo|Αγία Μαρίνα|Saint Marina|24930 93290|Parish Church
Συκαμινέα|Sykaminea|Αγία Τριάς|Holy Trinity||Parish Church
Συκέα|Sykea|Άγιος Δημήτριος|Saint Demetrius|24930 83481|Parish Church
Σταφανόβουνον|Stefanovouno|Άγιος Κωνσταντίνος|Saint Constantine|2493024327|Parish Church
Τσαριτσάνη|Tsaritsani|Κοίμησις της Θεοτόκου|Dormition of the Theotokos|24930 81625|Parish Church
Τσαριτσάνη|Tsaritsani|Άγιος Νικόλαος|Saint Nicholas|24930 81303|Parish Church
Τσαπουρνιά|Tsapournia|Κοίμησις της Θεοτόκου|Dormition of the Theotokos|24930 62450|Parish Church
Φαρμάκη|Farmaki|Άγιος Δημήτριος|Saint Demetrius||Parish Church
Φλάμπουρον|Flampouro|Αγία Τριάς|Holy Trinity||Parish Church
'''


MONASTERY_ROWS = [
    {
        "local": "Πατριαρχική και Σταυροπηγιακή Μονή Αγίας Τριάδος Σπαρμού Ολύμπου",
        "dedication": "Holy Trinity Sparmos of Olympus",
        "seat": "Sparmos, Olympus",
        "rank": "Patriarchal and Stavropegic Monastery",
        "phones": ["24930 61811"],
    },
    {
        "local": "Ιερά Μονή Αγίου Δημητρίου Βαλέτσικο Τσαριτσάνης",
        "dedication": "Saint Demetrius Valetsiko",
        "seat": "Tsaritsani",
        "rank": "Monastery",
    },
    {
        "local": "Πατριαρχική και Σταυροπηγιακή Μονή Παναγίας Ολυμπιωτίσσης",
        "dedication": "Panagia Olympiotissa",
        "seat": "Elasson",
        "rank": "Patriarchal and Stavropegic Monastery",
        "phones": ["24930 22480"],
    },
    {
        "local": "Ιερά Μονή Αναλήψεως του Σωτήρος Αναλήψεως Συκέας",
        "dedication": "Ascension of the Savior",
        "seat": "Analipsi, Sykea",
        "rank": "Monastery",
        "phones": ["24930 83076"],
    },
    {
        "local": "Ιερά Μονή Αγίας Τριάδος Λιβαδίου",
        "dedication": "Holy Trinity",
        "seat": "Livadi",
        "rank": "Monastery",
        "phones": ["24930 41810"],
    },
    {
        "local": "Πατριαρχική και Σταυροπηγιακή Μονή Γενεσίου της Θεοτόκου Κανάλων Καρυάς",
        "dedication": "Nativity of the Theotokos Kanalon",
        "seat": "Karya",
        "rank": "Patriarchal and Stavropegic Monastery",
        "phones": ["24930 91250"],
    },
    {
        "local": "Ιερά Μονή Μεταμορφώσεως του Σωτήρος Δασοχωρίου και Δεσκάτης",
        "dedication": "Transfiguration of the Savior",
        "seat": "Dasochori, Deskati",
        "rank": "Monastery",
        "phones": ["24620 31286"],
    },
    {
        "local": "Ιερά Μονή Μεταμορφώσεως του Σωτήρος Παλαιοκαρυάς",
        "dedication": "Transfiguration of the Savior Palaiokarya",
        "seat": "Kranea",
        "rank": "Monastery",
    },
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
    if len(parish_lines) != 61:
        raise ValueError("expected 61 current Elassona parish rows")
    for raw in parish_lines:
        local_seat, seat, local_dedication, dedication, phones, rank = (
            raw.split("|", 5)
        )
        name = make_name(dedication, rank, seat)
        index += 1
        row = {
            "id": "gr-ep-elassona-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s, %s" % (local_dedication, local_seat),
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [ROSTER_PAGE],
        }
        if phones:
            row["phones"] = phones.split(";")
            row["contact_sources"] = [ROSTER_PAGE]
            row["contact_checked"] = CHECKED
        rows.append(row)
    for source in MONASTERY_ROWS:
        rank = source["rank"]
        name = make_name(source["dedication"], rank, source["seat"])
        index += 1
        row = {
            "id": "gr-ep-elassona-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": source["local"],
            "seat": source["seat"],
            "country": "GR",
            "address": [source["seat"], "Greece"],
            "sources": [PATRIARCHATE_PAGE],
        }
        if source.get("phones"):
            row["phones"] = list(source["phones"])
            row["contact_sources"] = [PATRIARCHATE_PAGE]
            row["contact_checked"] = CHECKED
        rows.append(row)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


EXPECTED_TOTAL = 69
EXPECTED_OWNER_COUNTS = {PARENT: 69}
EXPECTED_KINDS = {"monastery": 8, "parish": 61}
EXPECTED_RANKS = {
    "Metropolitan Cathedral": 1,
    "Monastery": 5,
    "Parish Church": 60,
    "Patriarchal and Stavropegic Monastery": 3,
}
EXPECTED_CONTACT_BODIES = 48
EXPECTED_PHONE_BODIES = 48
EXPECTED_PHONE_VALUES = 49
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 69
EXISTING_PARENTS = {PARENT}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
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
    allowed = {
        "imelassonos.gr", "www.imelassonos.gr",
        "ec-patr.org", "www.ec-patr.org",
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
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Elassona candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Elassona candidate ledger date drifted")
    expected_summary = {
        PARENT: 69,
        "total": 69,
        "parish_kind_rows": 61,
        "monastery_kind_rows": 8,
        "contact_bodies": 48,
        "phone_bodies": 48,
        "public_phone_values": 49,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 69,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Elassona ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Elassona ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Elassona ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not x or not re.fullmatch(r"[a-z0-9-]+", x)
           for x in candidate_ids):
        raise ValueError("Elassona ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Elassona ledger has forbidden punctuation")
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
        raise ValueError("Elassona English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Elassona rank totals drifted")
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Elassona kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Elassona parent totals drifted")
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
        raise ValueError("Elassona contact coverage drifted: %r" % (coverage,))
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
        print("Elassona: 69 exact bodies; 61 parishes and 8 monasteries")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Elassona: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
