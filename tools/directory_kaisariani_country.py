#!/usr/bin/env python3
"""Validate exact named Kaisariani Metropolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_kaisariani_country.py --check
    python tools/directory_kaisariani_country.py --check-live
    python tools/directory_kaisariani_country.py --dump
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
PARENT = "gr-kaisariani"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "kaisariani_country.json"
)

OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/kaisarianes-byronos-kai-ymettou"
)
HOME = "https://imkby.gr/"
DIRECTORY = HOME + "ieroi-naoi"
MONASTERIES = HOME + "ieres-mones"
NICHOLAS_CONTACT = "https://in-agiosnikolaos.gr/?page_id=2"
TRINITY_CONTACT = "https://www.agiatriadavyrona.gr/contact/"
KAREAS_CONTACT = "https://www.imaik.gr/?page_id=949"

SOURCE_URLS = {
    "COG": CHURCH_OF_GREECE_PAGE,
    "NICHOLAS": NICHOLAS_CONTACT,
    "TRINITY": TRINITY_CONTACT,
    "KAREAS": KAREAS_CONTACT,
}

BODY_SITES = {
    "NICHOLAS": "https://in-agiosnikolaos.gr/",
    "TRINITY": "https://www.agiatriadavyrona.gr/",
    "KAREAS": "https://www.imaik.gr/",
}


# key|rank|English name|Greek local name|English seat|Greek address|
# phones|emails|site token|extra source tokens|contact source tokens|markers
MAIN_SOURCE = r'''
saint-nicholas|Metropolitan Church|Metropolitan Church of Saint Nicholas, Kaisariani|Μητροπολιτικός Ιερός Ναός Αγίου Νικολάου Καισαριανής|Kaisariani|Κιουπεκτσόγλου 1, 16121 Καισαριανή|2107213522,7221203,2107229320,2107236204|ag.nikolaos.kaisarianis@gmail.com|NICHOLAS|NICHOLAS|NICHOLAS|Ἁγίου Νικολάου;210 7213 522;7221 203
dormition-theotokos|Parish Church|Parish Church of the Dormition of the Theotokos, Kaisariani|Ιερός Ναός Κοιμήσεως της Θεοτόκου Καισαριανής|Kaisariani|Εθνάρχου Μακαρίου 1, 16121 Καισαριανή|2107213811,2107213802,2107213848|||COG|COG|Κοιμήσεως τῆς Θεοτόκου;210 7213 811
three-hierarchs|Parish Church|Parish Church of the Holy Three Hierarchs, Kaisariani|Ιερός Ναός Τριών Ιεραρχών Καισαριανής|Kaisariani|Τριών Ιεραρχών 18, 16122 Καισαριανή|2107222557,2107220931||||||Τριῶν Ἱεραρχῶν;210 7222 557
holy-trinity|Cathedral|Cathedral of the Holy Trinity, Vyron|Καθεδρικός Ιερός Ναός Αγίας Τριάδος Βύρωνος|Vyron|Κορυτσάς 1 και Κωνσταντιλιέρη, 16231 Βύρων|2107660859,2130291680,2107653461|agia_triada@hotmail.gr|TRINITY|COG,TRINITY|COG,TRINITY|Ἁγίας Τριάδος;210 7660 859;Καθεδρικός Ιερός Ναός
saint-demetrius|Parish Church|Parish Church of Saint Demetrius of Nea Elvetia, Vyron|Ιερός Ναός Αγίου Δημητρίου Νέας Ελβετίας Βύρωνος|Nea Elvetia, Vyron|Αγίου Δημητρίου 36, 16231 Βύρων|2107660943,2107660351||||||Ἁγίου Δημητρίου;210 7660 943
transfiguration|Parish Church|Parish Church of the Transfiguration of the Savior, Vyron|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Βύρωνος|Vyron|Μεταμορφώσεως 1, 16232 Βύρων|2107624200,2107624282,2107669369|||COG|COG|Μεταμορφώσεως Σωτῆρος;210 7624 200
annunciation-photini|Parish Church|Parish Church of the Annunciation of the Theotokos and Saint Photini, Ymittos|Ιερός Ναός Ευαγγελισμού της Θεοτόκου και Αγίας Φωτεινής Υμηττού|Ymittos|Ευαγγελιστρίας 1, 17237 Υμηττός|2109701580,2109734311,2109760334||||||Ευαγγελισμού της Θεοτόκου και Αγίας Φωτεινής;210 9701 580
peter-paul|Parish Church|Parish Church of the Holy Apostles Peter and Paul, Ymittos|Ιερός Ναός Αγίων Αποστόλων Πέτρου και Παύλου Υμηττού|Ymittos|Πλατεία Υμηττού, 17237 Υμηττός|2107629670,2107623525|||COG|COG|Ἁγίων Ἀποστόλων Πέτρου;210 7629 670
saint-george-kareas|Parish Church|Parish Church of Saint George, Kareas|Ιερός Ναός Αγίου Γεωργίου Καρέα|Kareas|16233 Καρέας, Βύρων|2107651595,2107658225,2107651023,2107651008|||COG|COG|Ἁγίου Γεωργίου Καρέα;210 7651 595
apostle-paul-prousiotissa|Pilgrimage Church|Pilgrimage Church of Apostle Paul and Panagia Prousiotissa, Kareas|Ιερός Προσκυνηματικός Ναός Αποστόλου Παύλου και Παναγίας Προυσιωτίσσης|Kareas|Λεωφόρος Κατεχάκη και Αλίμου, Καρέας|2109763310||||||Ἀποστόλου Παύλου;210-9763310
'''


# key|kind|rank|English name|Greek local name|English seat|Greek address|
# phones|emails|site token|source tokens|contact source tokens|markers
OTHER_SOURCE = r'''
john-theologian-chapel|parish|Metropolitan Chapel|Saint John the Theologian Metropolitan Chapel, Vyron|Ιερό Μητροπολιτικό Παρεκκλήσιο Αγίου Ιωάννου Θεολόγου|Vyron|Νέας Εφέσου 15, 16231 Βύρων||||DIRECTORY||Ἁγίου Ἰωάννου Θεολόγου;Νέας Ἐφέσου 15
barbara-chapel|parish|Parish Chapel|Saint Barbara Chapel of Holy Trinity Parish, Vyron|Παρεκκλήσιο Αγίας Βαρβάρας Ιερού Ναού Αγίας Τριάδος Βύρωνος|Vyron|Αγίας Βαρβάρας 4, 16232 Βύρων||||DIRECTORY||Ἁγίας Βαρβάρας;Ἁγ. Βαρβάρας 4
lazarus-chapel|parish|Parish Chapel|Saint Lazarus Chapel of Holy Trinity Parish, Vyron|Παρεκκλήσιο Αγίου Λαζάρου Ιερού Ναού Αγίας Τριάδος Βύρωνος|Vyron|Πλατεία Αγίου Λαζάρου, 16231 Βύρων||||DIRECTORY||Ἁγίου Λαζάρου;Πλατεία Ἁγίου Λαζάρου
paraskevi-chapel|parish|Parish Chapel|Saint Paraskevi Chapel of the Holy Three Hierarchs Parish, Kaisariani|Παρεκκλήσιο Αγίας Παρασκευής Ιερού Ναού Τριών Ιεραρχών Καισαριανής|Kaisariani|Παραδείσου και Κασαμπά, 16122 Καισαριανή||||DIRECTORY||Ἁγίας Παρασκευῆς;Παραδείσου
annunciation-chapel|parish|Parish Chapel|Annunciation of the Theotokos Chapel of the Transfiguration Parish, Vyron|Παρεκκλήσιο Ευαγγελισμού της Θεοτόκου Ιερού Ναού Μεταμορφώσεως Σωτήρος Βύρωνος|Vyron|Μεταμορφώσεως 47, 16232 Βύρων||||DIRECTORY||Εὐαγγελισμοῦ τῆς Θεοτόκου;Μεταμορφώσεως 47
constantine-helen-chapel|parish|Parish Chapel|Saints Constantine and Helen Chapel of Saint Demetrius Parish, Kareas|Παρεκκλήσιο Αγίων Κωνσταντίνου και Ελένης Ιερού Ναού Αγίου Δημητρίου Βύρωνος|Kareas|Σταματοπούλου, 16233 Καρέας||||DIRECTORY||Ἁγίων Κωνσταντίνου;Σταματοπούλου
entrance-life-giving-spring|monastery|Monastery|Entrance of the Theotokos and Life-Giving Spring Monastery, Vyron|Ιερά Μονή Εισοδίων της Θεοτόκου και Ζωοδόχου Πηγής Βύρωνος|Vyron|Απόλλωνος 2, 16233 Βύρων, Αττική|7650765|||MONASTERIES,COG|COG|Εἰσοδίων τῆς Θεοτόκου;Ἀπόλλωνος 2
john-forerunner-kareas|monastery|Monastery|Saint John the Forerunner Monastery, Kareas|Ιερά Μονή Αγίου Ιωάννου Προδρόμου Καρέα|Kareas|Καρέας, 16233 Βύρων, Αττική|2107652746,2107666506|imaik@imaik.gr|KAREAS|MONASTERIES,COG,KAREAS|COG,KAREAS|Ἱερὰ Μονὴ Ἁγ. Ἰωάννου Προδρόμου (Καρέα);Τηλ.: +210 76 52 746
john-forerunner-kaisariani|monastery|Monastery|Saint John the Forerunner Monastery, Kaisariani|Ιερά Μονή Αγίου Ιωάννου Προδρόμου Καισαριανής|Kaisariani|Μονή Καισαριανής, Υμηττός, Αττική|7224167|||MONASTERIES,COG|COG|Ἱερὰ Μονὴ Ἁγ. Ἰωάννου Προδρόμου (Καισαριανῆς);7224167
'''


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def source_values(value):
    values = []
    for token in split_values(value):
        if token == "DIRECTORY":
            values.append(DIRECTORY)
        elif token == "MONASTERIES":
            values.append(MONASTERIES)
        else:
            values.append(SOURCE_URLS[token])
    return values


def build_rows():
    rows = []
    main_lines = MAIN_SOURCE.strip().splitlines()
    if len(main_lines) != 10:
        raise ValueError("expected ten current main worship bodies")
    for number, raw in enumerate(main_lines, 1):
        (key, rank, name, local, seat, address, phones, emails,
         site_token, extra_tokens, contact_tokens, markers) = raw.split(
            "|", 11
        )
        sources = [DIRECTORY, OFFICIAL_PDF]
        sources.extend(source_values(extra_tokens))
        if key == "holy-trinity":
            sources.remove(OFFICIAL_PDF)
        contact_sources = [DIRECTORY]
        contact_sources.extend(source_values(contact_tokens))
        row = {
            "id": "gr-kaisariani-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": list(dict.fromkeys(sources)),
            "contact_sources": list(dict.fromkeys(contact_sources)),
            "contact_checked": CHECKED,
            "live_markers": split_values(
                markers.lstrip("|").replace(";", ",")
            ),
        }
        if phones:
            row["phones"] = split_values(phones)
        if emails:
            row["emails"] = split_values(emails)
        if site_token:
            row["site"] = BODY_SITES[site_token]
        rows.append(row)

    for number, raw in enumerate(OTHER_SOURCE.strip().splitlines(), 11):
        (key, kind, rank, name, local, seat, address, phones, emails,
         site_token, source_tokens, contact_tokens, markers) = raw.split(
            "|", 12
        )
        sources = source_values(source_tokens)
        row = {
            "id": "gr-kaisariani-%03d-%s" % (number, key),
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
            row["contact_sources"] = source_values(contact_tokens)
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

EXPECTED_TOTAL = 19
EXPECTED_OWNER_COUNTS = {PARENT: 19}
EXPECTED_KINDS = {"monastery": 3, "parish": 16}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Metropolitan Chapel": 1,
    "Metropolitan Church": 1,
    "Monastery": 3,
    "Parish Chapel": 5,
    "Parish Church": 7,
    "Pilgrimage Church": 1,
}
EXPECTED_CONTACT_BODIES = 13
EXPECTED_PHONE_BODIES = 13
EXPECTED_PHONE_VALUES = 31
EXPECTED_EMAIL_BODIES = 3
EXPECTED_EMAIL_VALUES = 3
EXPECTED_SITE_BODIES = 3
EXPECTED_ADDRESS_BODIES = 19
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imkby.gr",
    "www.imkby.gr",
    "in-agiosnikolaos.gr",
    "www.in-agiosnikolaos.gr",
    "agiatriadavyrona.gr",
    "www.agiatriadavyrona.gr",
    "imaik.gr",
    "www.imaik.gr",
    "monipetraki.gr",
    "www.monipetraki.gr",
    "evaggelismostheotokou.gr",
    "www.evaggelismostheotokou.gr",
    "agiosgeorgioskarea.gr",
    "www.agiosgeorgioskarea.gr",
    "appauloskarea.blogspot.com",
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
    item.pop("live_markers", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Kaisariani candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kaisariani candidate ledger date drifted")
    expected_summary = {
        PARENT: 19,
        "total": 19,
        "regulated_parish_rows": 9,
        "regulated_pilgrimage_rows": 1,
        "parish_kind_rows": 16,
        "monastery_kind_rows": 3,
        "exact_chapel_rows": 6,
        "contact_bodies": 13,
        "phone_bodies": 13,
        "public_phone_values": 31,
        "email_bodies": 3,
        "public_email_values": 3,
        "body_owned_sites": 3,
        "address_bodies": 19,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Kaisariani ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Kaisariani ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 4:
                raise ValueError("Kaisariani ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Kaisariani ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Kaisariani ledger has forbidden punctuation")
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
        raise ValueError("Kaisariani English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Kaisariani rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Kaisariani kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Kaisariani parent totals drifted")
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
        raise ValueError("Kaisariani contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
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
    required = {HOME, DIRECTORY, MONASTERIES, CHURCH_OF_GREECE_PAGE,
                OFFICIAL_PDF}
    required.update(url for row in ROWS for url in row.get("sources", []))
    cache = {}
    for url in sorted(required):
        payload, content_type = fetch(url)
        if url.lower().endswith(".pdf"):
            if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                raise ValueError("live source is not a PDF: %s" % url)
            cache[url] = payload
            continue
        if "html" not in content_type and not payload.lstrip().startswith(b"<"):
            raise ValueError("live source is not HTML: %s" % url)
        cache[url] = normalized_page(payload)

    directory_page = cache[DIRECTORY]
    for marker in ("Δέκα ἐνοριακοί ναοί", "6 Παρεκκλήσια",
                   "Ἀποστόλου Παύλου", "Ἁγίου Ἰωάννου Θεολόγου"):
        if unicase(marker) not in directory_page:
            raise ValueError("Kaisariani directory lacks marker: %s" % marker)
    monastery_page = cache[MONASTERIES]
    for marker in ("Τρία μοναστήρια", "Εἰσοδίων τῆς Θεοτόκου",
                   "Προδρόμου (Καρέα)", "Προδρόμου (Καισαριανῆς)"):
        if unicase(marker) not in monastery_page:
            raise ValueError("Kaisariani monastery page lacks marker: %s" % marker)

    for row in ROWS:
        pages = " ".join(
            cache[url] for url in row["sources"]
            if isinstance(cache[url], str)
        )
        digit_pages = compact_digits(pages)
        for marker in row.get("live_markers") or []:
            marker_digits = compact_digits(marker)
            if marker_digits and len(marker_digits) >= 7:
                if marker_digits not in digit_pages:
                    raise ValueError("%s lacks live marker %s" %
                                     (row["id"], marker))
            elif unicase(marker) not in pages:
                raise ValueError("%s lacks live marker %s" %
                                 (row["id"], marker))
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digit_pages:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
        for email in row.get("emails") or []:
            if unicase(email) not in pages:
                raise ValueError("%s lacks live email %s" %
                                 (row["id"], email))
    print("Kaisariani live sources: %d URLs checked" % len(required))


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
        print("Kaisariani: 19 exact bodies; 9 regulated parishes, "
              "1 regulated pilgrimage church, 6 exact chapels, and "
              "3 current local monasteries")
        print("Contacts: 13 bodies; 31 phones; 3 emails; 3 live body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Kaisariani: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
