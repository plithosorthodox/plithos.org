#!/usr/bin/env python3
"""Validate exact named Nea Smyrni Metropolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_nea_smyrni_country.py --check
    python tools/directory_nea_smyrni_country.py --check-live
    python tools/directory_nea_smyrni_country.py --dump
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
PARENT = "gr-nea-smyrni"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "nea_smyrni_country.json"
)

OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2017_iounios.pdf"
)
DIRECTORY_ROOT = "https://www.imns.gr/mitropoli/enories/"

BODY_SOURCES = {
    "SOSTIS": "https://www.sostis.gr/",
    "FOTEINI": "https://agiafoteinins.gr/",
    "ANARGYROI": "https://agioianargyroi.gr/",
    "ALEXANDER": "https://inaapf.gr/",
    "PANAGITSA": "https://koimisifalirou.gr/",
    "KYRIAKI": "https://inak.gr/",
    "BARBARA_FALIRO": "https://inagiasvarvaras.blogspot.com/",
    "SOTIRAS_ALIMOS": "https://sites.google.com/site/sotiras/",
    "THEOMITOROS": "https://theomitoros.gr/",
    "MYRTIDIOTISSA": "https://myrtidiotissa-alimou.gr/",
    "NICHOLAS_ALIMOS": "https://agiosnikolaosalimou.gr/",
    "BARBARA_ARGYRO": "https://agia-varvara-argyroupolis.gr/",
}

BODY_EMAILS = {
    "ANARGYROI": "agioianargyroi@yahoo.com",
    "ALEXANDER": "inaalpf@gmail.com",
    "PANAGITSA": "koimisifalirou@yahoo.gr",
    "KYRIAKI": "mail@inak.gr",
    "BARBARA_FALIRO": "inagiasvarvaras@gmail.com",
    "SOTIRAS_ALIMOS": "sotiras@gmail.com",
    "BARBARA_ARGYRO": "naos@agia-varvara-argyroupolis.gr",
}


# key|kind|rank|English name|Greek local name|English seat|Greek address|
# phones|site token|legal parish|detail path|live markers
ROW_SOURCE = r'''
transfiguration-sostis|parish|Parish Church|Transfiguration of the Savior Parish Church, Saint Sostis|Μεταμόρφωσις Σωτῆρος (Ἅγιος Σώστης)|Athens|Λεωφ. Συγγρού 131, 117 45 Αθήνα|2109335460,2109342620,2109585590,2109344521,2109326193,2114120673|SOSTIS|1|48-enories-dimou-neas-smyrnis/88-metamorfosis-sot-ros-gios-sostis|Μεταμόρφωσις Σωτῆρος;210-93.35.460
photini|parish|Metropolitan Church|Saint Photini Metropolitan Church, Nea Smyrni|Ἁγία Φωτεινή (Μητροπολιτικός Ναός)|Nea Smyrni|Αγίας Φωτεινής, 171 23 Νέα Σμύρνη|2109335892,2109319696,2109016385,2109430651,2109764632,2109948488|FOTEINI|1|48-enories-dimou-neas-smyrnis/89-gia-foteini-mitropolitikos-naos|Ἁγία Φωτεινή;210-93.35.892
charalambos|parish|Parish Church|Saint Charalambos Parish Church at the Iosephogleion, Nea Smyrni|Ἅγιος Χαράλαμπος (Ἰωσηφογλείου)|Nea Smyrni|Λεωφ. Συγγρού 221, 171 22 Νέα Σμύρνη|2109357333||1|48-enories-dimou-neas-smyrnis/90-gios-xaralampos|Ἅγιος Χαράλαμπος;210-93.57.333
paraskevi|parish|Parish Church|Saint Paraskevi Parish Church, Nea Smyrni|Ἁγία Παρασκευή|Nea Smyrni|Ελευθ. Βενιζέλου 135β, 171 23 Νέα Σμύρνη|2109332237,2109315045,2109838732,2109719693,2109019442||1|48-enories-dimou-neas-smyrnis/91-gia-paraskevi|Ἁγία Παρασκευή;210-93.32.237
unmercenaries|parish|Parish Church|Holy Unmercenaries Parish Church, Nea Smyrni|Ἅγιοι Ἀνάργυροι|Nea Smyrni|Αγίων Αναργύρων και Παρασκευοπούλου, 171 22 Νέα Σμύρνη|2109414131,2109414221,2107293400,2114074072,2109316752|ANARGYROI|1|48-enories-dimou-neas-smyrnis/92-gioi-nargyroi|Ἅγιοι Ἀνάργυροι;210-94.14.131
alexander|parish|Parish Church|Saint Alexander Parish Church, Palaio Faliro|Ἅγιος Ἀλέξανδρος|Palaio Faliro|Αλκυόνης και Αγίου Αλεξάνδρου, 17561 Παλαιό Φάληρο|2109815551,2109816933,2108832250,2109854704,2169002495|ALEXANDER|1|49-enories-dimou-palaiou-falirou/93-gios-leksandros|Ἅγιος Ἀλέξανδρος;210-98.15.551
dormition-panagitsa|parish|Parish Church|Dormition of the Theotokos Parish Church, Panagitsa, Palaio Faliro|Κοίμησις Θεοτόκου (Παναγίτσα)|Palaio Faliro|Αχιλλέως 30, 175 62 Παλαιό Φάληρο|2109812234,2109843468,2102691931,2109834935,2109828634,2109215119,2109812859|PANAGITSA|1|49-enories-dimou-palaiou-falirou/94-koimisis-theotokou-panagitsa|Κοίμησις Θεοτόκου;210-98.12.234
kyriaki|parish|Parish Church|Saint Kyriaki Parish Church, Palaio Faliro|Ἁγία Κυριακή|Palaio Faliro|Λεωφ. Αμφιθέας 60, 175 64 Παλαιό Φάληρο|2109419643,2109416425,2109347338,2109405161|KYRIAKI|1|49-enories-dimou-palaiou-falirou/95-gia-kyriaki|Ἁγία Κυριακή;210-94.19.643
barbara-faliro|parish|Parish Church|Saint Barbara Parish Church, Palaio Faliro|Ἁγία Βαρβάρα|Palaio Faliro|Λεωφ. Αγίας Βαρβάρας 110, 175 63 Παλαιό Φάληρο|2109810220,2109852542,2109823774,2109835773|BARBARA_FALIRO|1|49-enories-dimou-palaiou-falirou/96-gia-varvara|Ἁγία Βαρβάρα;210-98.10.220
transfiguration-alimos|parish|Parish Church|Transfiguration of the Savior Parish Church, Alimos|Μεταμόρφωσις Σωτῆρος|Alimos|Νίκης 51 και Μεταμορφώσεως, 174 55 Άλιμος|2109810568,2109833640,2109311491,2102283166|SOTIRAS_ALIMOS|1|50-enories-dimou-alimou/77-metamorfosis-sot-ros|Μεταμόρφωσις Σωτῆρος;210-98.10.568
dormition-upper-kalamaki|parish|Parish Church|Dormition of the Theotokos Parish Church, Upper Kalamaki|Κοίμησις Θεοτόκου Ἄνω Καλαμακίου|Upper Kalamaki, Alimos|Θεομήτορος 21, 174 56 Άλιμος|2109813910,2109884789,2109852096,2109634586|THEOMITOROS|1|50-enories-dimou-alimou/78-koimisis-theotokou-no-kalamakiou|Κοίμησις Θεοτόκου;210-98.13.910
dormition-alimos|parish|Parish Church|Dormition of the Theotokos Parish Church, Alimos|Κοίμησις Θεοτόκου Ἁλίμου|Alimos|Κεφαλληνίας και Ιθάκης, 175 55 Άλιμος|2109825563,2109829461,2109912002||1|50-enories-dimou-alimou/79-koimisis-theotokou-limou|Κοίμησις Θεοτόκου;210-98.25.563
panteleimon-trachones|parish|Parish Church|Saint Panteleimon Parish Church, Trachones|Ἅγιος Παντελεήμων Τραχώνων|Trachones, Alimos|Ρόδου 2, 175 56 Άλιμος|2109910591,2109963351,2109922439,2109615303||1|50-enories-dimou-alimou/80-gios-panteleimon-traxonon|Ἅγιος Παντελεήμων;210-99.10.591
life-giving-spring|parish|Parish Church|Life-Giving Spring Parish Church, Trachones|Ζωοδόχος Πηγή Τραχώνων|Trachones, Alimos|Κουμουνδούρου 94, 174 56 Άλιμος|2109912258,2109960716,2109925583||1|50-enories-dimou-alimou/81-zoodoxos-pigi-traxonon|Ζωοδόχος Πηγή;210-99.12.258
myrtidiotissa|parish|Parish Church|Panagia Myrtidiotissa Parish Church, Alimos|Παναγία Μυρτιδιώτισσα|Alimos|Κυθηρίων 71 και Δήμητρας, 174 56 Άλιμος|2109958357,2109968560,2104950105,2109910668|MYRTIDIOTISSA|1|50-enories-dimou-alimou/82-panagia-myrtidiotissa|Παναγία Μυρτιδιώτισσα;210-99.58.357
nicholas-alimos|parish|Parish Church|Saint Nicholas Parish Church, Alimos|Ἅγιος Νικόλαος|Alimos|Ανδρούτσου και Ταξιαρχών, 174 55 Άλιμος|2109802260,2107717882,6983461149|NICHOLAS_ALIMOS|1|50-enories-dimou-alimou/83-agios-nikolaos|Ἅγιος Νικόλαος;210-98.02.260
barbara-argyroupoli|parish|Parish Church|Saint Barbara Parish Church, Argyroupoli|Ἁγία Βαρβάρα|Argyroupoli|Αγίας Βαρβάρας 20, 164 52 Αργυρούπολη|2109615425,2109644424,2109627048,2107019786,2155103928|BARBARA_ARGYRO|1|51-enories-dimou-argyroupoleos/84-gia-varvara|Ἁγία Βαρβάρα;210-96.15.425
dormition-argyroupoli|parish|Parish Church|Dormition of the Theotokos Parish Church, Argyroupoli|Κοίμησις Θεοτόκου Ἀργυρουπόλεως|Argyroupoli|Ολυμπίας 28, 164 51 Αργυρούπολη|2109913070,2109910280,2109756976,6909605631,2105069169||1|51-enories-dimou-argyroupoleos/85-koimisis-theotokou|Κοίμησις Θεοτόκου;210-99.13.070
holy-trinity-argyroupoli|parish|Parish Church|Holy Trinity Parish Church, Argyroupoli|Ἁγία Τριάς|Argyroupoli|Πλατεία Αγίας Τριάδος, 164 00 Αργυρούπολη|2109917286,2109917301,2109803191,2109833861||1|51-enories-dimou-argyroupoleos/86-gia-trias|Ἁγία Τριάς;210-99.17.286
george-argyroupoli|parish|Parish Church|Saint George Parish Church, Argyroupoli|Ἅγιος Γεώργιος|Argyroupoli|Αγίου Γεωργίου 2, 164 52 Αργυρούπολη|2109916885,2109920033,2109671135||1|51-enories-dimou-argyroupoleos/87-gios-georgios|Ἅγιος Γεώργιος;210-99.16.885
archangels-cemetery|parish|Cemetery Church|Holy Archangels Cemetery Church, Nea Smyrni|Παμμέγιστοι Ταξιάρχες Κοιμητηρίου Νέας Σμύρνης|Nea Smyrni|Κοιμητήριο Νέας Σμύρνης|2109812202|||52-naoi-koimitirion/97-nea-smyrni|Παμμ. Ταξιάρχαι;210-98.12.202
peter-paul-cemetery|parish|Cemetery Church|Saints Peter and Paul Cemetery Church, Palaio Faliro|Ἅγιοι Πέτρος καί Παύλος Κοιμητηρίου Παλαιοῦ Φαλήρου|Palaio Faliro|Κοιμητήριο Παλαιοῦ Φαλήρου|2109811309|||52-naoi-koimitirion/98-palaio-faliro|Άγιος Πέτρος;210-98.11.309
resurrection-cemetery|parish|Cemetery Church|Resurrection of the Lord Cemetery Church, Argyroupoli|Ἀνάστασις τοῦ Κυρίου Κοιμητηρίου Ἀργυρουπόλεως|Argyroupoli|Κοιμητήριο Αργυρουπόλεως|2109612872|||52-naoi-koimitirion/99-a|Ανάστασις του Κυρίου;210-96.12.872
andrew-institution|parish|Institutional Chapel|Saint Andrew Chapel at the Foundation for the Protection of Poor Girls|Ἅγιος Ἀνδρέας (Ἱδρύματος Προστασίας Ἀπόρων Κορασίδων, Ε.Ι.Π.Α.Κ.)|Nea Smyrni|Αγίου Ανδρέου 14, 171 22 Νέα Σμύρνη|2109331667|||53-naoi-parekklision-poy-leitourgoun/100-gios-ndreas|Ἅγιος Ἀνδρέας;210-93.31.667
ascension-pantokrator|parish|Institutional Chapel|Ascension of the Lord Chapel at the Pantokrator Christian Youth Foundation|Ἀνάληψις Κυρίου (Χριστιανικοῦ Ἱδρύματος Νεότητος «Ὁ Παντοκράτωρ»)|Palaio Faliro|Ήβης 43 και Ναϊάδων, 175 61 Παλαιό Φάληρο|2109810400|||53-naoi-parekklision-poy-leitourgoun/101-nalipsis-kyriou-xristianiko-drymatos-neotitos-pantokrator|Ἀνάληψις Κυρίου;210-98.10.400
archangels-zanneio|parish|Institutional Chapel|Holy Archangels Chapel at the Zanneio Orphanage|Παμμέγιστοι Ταξιάρχες (Ζαννείου Ὀρφανοτροφείου)|Palaio Faliro|Διαγόρα 4 και Αγίας Λαύρας 22, 175 63 Παλαιό Φάληρο|2104179114|||53-naoi-parekklision-poy-leitourgoun/102-pamm-taksiarx-n-zanneiou-rfanotrofeiou|Παμμ. Ταξιαρχῶν;210-41.79.114
'''


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def detail(value):
    return DIRECTORY_ROOT + value


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def build_rows():
    rows = []
    lines = ROW_SOURCE.strip().splitlines()
    if len(lines) != 26:
        raise ValueError("expected 26 current Nea Smyrni worship bodies")
    for number, raw in enumerate(lines, 1):
        (key, kind, rank, name, local, seat, address, phones, site_token,
         legal, detail_path, markers) = raw.split("|", 11)
        detail_url = detail(detail_path)
        sources = [detail_url]
        if legal:
            sources.append(OFFICIAL_PDF)
        if site_token:
            sources.append(BODY_SOURCES[site_token])
        row = {
            "id": "gr-nea-smyrni-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "phones": split_values(phones),
            "sources": sources,
            "contact_sources": [detail_url],
            "contact_checked": CHECKED,
            "live_markers": split_values(markers.replace(";", ",")),
        }
        if site_token:
            row["site"] = BODY_SOURCES[site_token]
            if site_token in BODY_EMAILS:
                row["emails"] = [BODY_EMAILS[site_token]]
                row["contact_sources"].append(BODY_SOURCES[site_token])
        rows.append(row)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 26
EXPECTED_OWNER_COUNTS = {PARENT: 26}
EXPECTED_KINDS = {"parish": 26}
EXPECTED_RANKS = {
    "Cemetery Church": 3,
    "Institutional Chapel": 3,
    "Metropolitan Church": 1,
    "Parish Church": 19,
}
EXPECTED_PHONE_VALUES = 91
EXPECTED_EMAIL_VALUES = 7
EXPECTED_SITE_BODIES = 12
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imns.gr",
    "www.imns.gr",
    "sostis.gr",
    "www.sostis.gr",
    "agiafoteinins.gr",
    "www.agiafoteinins.gr",
    "agioianargyroi.gr",
    "www.agioianargyroi.gr",
    "inaapf.gr",
    "www.inaapf.gr",
    "koimisifalirou.gr",
    "www.koimisifalirou.gr",
    "inak.gr",
    "www.inak.gr",
    "inagiasvarvaras.blogspot.com",
    "sites.google.com",
    "theomitoros.gr",
    "www.theomitoros.gr",
    "myrtidiotissa-alimou.gr",
    "www.myrtidiotissa-alimou.gr",
    "agiosnikolaosalimou.gr",
    "www.agiosnikolaosalimou.gr",
    "agia-varvara-argyroupolis.gr",
    "www.agia-varvara-argyroupolis.gr",
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
    if not contact_sources or item.get("contact_checked") != CHECKED:
        raise ValueError("%s lacks current contact provenance" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
        if source_url not in sources:
            raise ValueError("contact source is outside identity sources")
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        source_hosts = {urlparse(value).netloc for value in sources}
        if urlparse(item["site"]).netloc not in source_hosts:
            raise ValueError("%s site host lacks an identity source" % item.get("id"))
    item.pop("live_markers", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Nea Smyrni candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Nea Smyrni candidate ledger date drifted")
    expected_summary = {
        PARENT: 26,
        "total": 26,
        "regulated_parish_rows": 20,
        "cemetery_church_rows": 3,
        "operating_institutional_chapel_rows": 3,
        "contact_bodies": 26,
        "phone_bodies": 26,
        "public_phone_values": 91,
        "email_bodies": 7,
        "public_email_values": 7,
        "body_owned_sites": 12,
        "address_bodies": 26,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Nea Smyrni ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Nea Smyrni ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Nea Smyrni ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Nea Smyrni ledger has forbidden punctuation")
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
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for phone in item.get("phones") or []:
            if not re.fullmatch(r"\d{10}", phone):
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
        raise ValueError("Nea Smyrni English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Nea Smyrni rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Nea Smyrni kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Nea Smyrni parent totals drifted")
    coverage = (
        sum(len(x.get("phones") or []) for x in result),
        sum(len(x.get("emails") or []) for x in result),
        sum(bool(x.get("site")) for x in result),
    )
    if coverage != (EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_VALUES,
                    EXPECTED_SITE_BODIES):
        raise ValueError("Nea Smyrni contact coverage drifted: %r" %
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
    return " ".join(text.split())


def check_live():
    errors = []
    fetched = {}
    for row in ROWS:
        primary = row["sources"][0]
        try:
            if primary not in fetched:
                fetched[primary] = fetch(primary)
            payload, _ = fetched[primary]
            page = normalized_page(payload)
            for marker in row.get("live_markers") or []:
                if unicase(marker) not in unicase(page):
                    errors.append("%s lacks live marker %s" %
                                  (row["id"], marker))
        except Exception as exc:
            errors.append("%s failed: %s" % (primary, exc))
        for source_url in row["sources"][1:]:
            if source_url == OFFICIAL_PDF or source_url in fetched:
                continue
            try:
                fetched[source_url] = fetch(source_url)
            except Exception as exc:
                errors.append("%s failed: %s" % (source_url, exc))
    try:
        payload, content_type = fetch(OFFICIAL_PDF)
        fetched[OFFICIAL_PDF] = (payload, content_type)
        if not payload.startswith(b"%PDF"):
            errors.append("Nea Smyrni legal source is not a PDF")
    except Exception as exc:
        errors.append("%s failed: %s" % (OFFICIAL_PDF, exc))
    for token, email in BODY_EMAILS.items():
        source_url = BODY_SOURCES[token]
        try:
            payload, _ = fetched.get(source_url) or fetch(source_url)
            if email.casefold() not in payload.decode("utf-8", "replace").casefold():
                errors.append("%s lacks live email %s" % (source_url, email))
        except Exception as exc:
            errors.append("%s failed: %s" % (source_url, exc))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Nea Smyrni live sources: %d URLs checked" % len(fetched))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        return check_live()
    if args.dump:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    print(
        "Nea Smyrni: 26 exact bodies; 20 regulated parishes, "
        "3 cemetery churches, and 3 operating institutional chapels"
    )
    print(
        "Contacts: 26 bodies; 91 phone or fax values; "
        "7 emails; 12 live body sites"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
