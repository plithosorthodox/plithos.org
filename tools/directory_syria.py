#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Syria.

The current first-party records of the Patriarchates of Antioch, Moscow,
and Romania establish the bodies below. Existing Syrian Antiochian
archdiocesan parent rows are not duplicated here.

    python tools/directory_syria.py --check
    python tools/directory_syria.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "syria.json"
CHECKED = "2026-11-15"

DAMASCUS_ROSTER_EN = (
    "https://www.antiochpatriarchate.org/en/category/"
    "churches-of-damascus-and-rural-damascus/105/"
)
DAMASCUS_ROSTER_AR = (
    "https://www.antiochpatriarchate.org/ar/category/"
    "%D9%83%D9%86%D8%A7%D8%A6%D8%B3-%D8%AF%D9%85%D8%B4%D9%82-"
    "%D9%88%D8%B1%D9%8A%D9%81%D9%87%D8%A7/105/"
)
DWEILAA = "https://www.antiochpatriarchate.org/ar/page/2959/"
MARIAMITE_CURRENT = "https://antiochpatriarchate.org/en/page/3040/"
ANTIOCH_MONASTERIES = "https://antiochpatriarchate.org/en/category/38/"
SAYDNAYA_OUR_LADY = "https://www.antiochpatriarchate.org/en/page/146/"
SAYDNAYA_SAINT_GEORGE = "https://www.antiochpatriarchate.org/en/page/144/"
SAYDNAYA_CHERUBIM = "https://antiochpatriarchate.org/en/page/143/"
MAALULA_SAINT_THECLA = "https://www.antiochpatriarchate.org/en/page/149/"
AL_HOMEYRA = "https://antiochpatriarchate.org/en/page/145/"
RUSSIA_REPRESENTATION = "https://representation-damascus.org/"
RUSSIA_CURRENT = "https://mospat.ru/en/news/94542/"
ROMANIA_EXTERNAL = (
    "https://patriarhia.ro/en/organization-of-the-romanian-orthodox-church/"
    "external-representations-and-communities/"
)


def body(row_id, parent, name, local, seat, rank, sources,
         kind="parish", address=None, phones=None, emails=None, site=None,
         contact_sources=None):
    item = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "SY",
        "address": address,
        "sources": sources,
        "site": site,
    }
    phone_values = list(phones or [])
    email_values = list(emails or [])
    if phone_values or email_values:
        item.update({
            "emails": email_values,
            "phones": phone_values,
            "contact_sources": list(contact_sources or sources),
            "contact_checked": CHECKED,
        })
    return item


def damascus_church(slug, name, local, seat, location, phones=None,
                     parent="antioch", sources=None, rank="Church"):
    source_values = list(sources or [DAMASCUS_ROSTER_EN, DAMASCUS_ROSTER_AR])
    return body(
        "sy-an-%s" % slug,
        parent,
        name,
        local,
        seat,
        rank,
        source_values,
        address=[location, "Syria"],
        phones=phones,
        contact_sources=[DAMASCUS_ROSTER_AR] if phones else None,
    )


ANTIOCH_MONASTERY_ROWS = [
    body(
        "sy-an-our-lady-saydnaya-monastery",
        "antioch",
        "Our Lady of Saydnaya Patriarchal Monastery",
        "دير سيّدة صيدنايا البطريركيّ",
        "Saydnaya",
        "Patriarchal Monastery",
        [SAYDNAYA_OUR_LADY, ANTIOCH_MONASTERIES],
        kind="monastery",
        address=["Our Lady of Saydnaya Patriarchal Monastery",
                 "Saydnaya, Syria"],
        phones=[
            "+963 11 595 1 900",
            "+963 11 595 0 547",
            "+963 11 595 1 648",
        ],
        contact_sources=[SAYDNAYA_OUR_LADY],
    ),
    body(
        "sy-an-saint-george-saydnaya-monastery",
        "sy-an-our-lady-saydnaya-monastery",
        "Saint George Saydnaya Patriarchal Monastery",
        "دير القدّيس جاورجيوس - صيدنايا البطريركيّ",
        "Saydnaya",
        "Patriarchal Monastery",
        [SAYDNAYA_SAINT_GEORGE, ANTIOCH_MONASTERIES],
        kind="monastery",
        address=["St George Monastery", "P.O. Box 22458",
                 "Saydnaya, Syria"],
        phones=["+963 11 595 0 646", "+963 11 595 5 882"],
        contact_sources=[SAYDNAYA_SAINT_GEORGE],
    ),
    body(
        "sy-an-cherubim-saydnaya-monastery",
        "antioch",
        "Cherubim Saydnaya Patriarchal Monastery",
        "دير الشاروبيم - صيدنايا البطريركيّ",
        "Saydnaya",
        "Patriarchal Monastery",
        [SAYDNAYA_CHERUBIM, ANTIOCH_MONASTERIES],
        kind="monastery",
        address=["St George Monastery", "P.O. Box 22458",
                 "Saydnaya, Syria"],
        phones=["+963 11 595 3 377"],
        contact_sources=[SAYDNAYA_CHERUBIM],
    ),
    body(
        "sy-an-saint-thecla-maalula-monastery",
        "antioch",
        "Saint Thecla Ma'lula Patriarchal Monastery",
        "دير مار تقلا - معلولا البطريركيّ",
        "Ma'lula",
        "Patriarchal Monastery",
        [MAALULA_SAINT_THECLA, ANTIOCH_MONASTERIES],
        kind="monastery",
        address=["St Thecla Ma'lula Patriarchal Monastery",
                 "Ma'lula, Syria"],
        phones=["+963 11 777 0 003"],
        contact_sources=[MAALULA_SAINT_THECLA],
    ),
    body(
        "sy-an-saint-george-al-homeyra-monastery",
        "antioch",
        "Saint George Al-Homeyra Patriarchal Monastery",
        "دير القدّيس جاورجيوس - الحميراء البطريركيّ",
        "Al-Mechtaye",
        "Patriarchal Monastery",
        [AL_HOMEYRA, ANTIOCH_MONASTERIES],
        kind="monastery",
        address=["St Georges Al-Homeyra Patriarchal Monastery",
                 "Al-Mechtaye, Talkalakh, Syria"],
        phones=["+963 31 773 0 113", "+963 31 773 1 101"],
        contact_sources=[AL_HOMEYRA],
    ),
]


DAMASCUS_ROWS = [
    damascus_church(
        "damascus-mariamite", "Mariamite Cathedral",
        "الكاتدرائية المريمية", "Damascus",
        "Bab Touma - Tale' al-Feda, Damascus", ["00963 11 5413392"],
        sources=[DAMASCUS_ROSTER_EN, MARIAMITE_CURRENT],
        rank="Cathedral",
    ),
    damascus_church(
        "damascus-holy-cross", "Holy Cross Church",
        "كنيسة الصليب", "Damascus", "Qassaa, Damascus",
        ["00963 11 5427752"],
    ),
    damascus_church(
        "damascus-saint-elias-tabale", "Saint Elias Church in Tabale",
        "كنيسة مار الياس، الطبالة", "Damascus", "Tabale, Damascus",
        ["00963 11 4728868"],
    ),
    damascus_church(
        "damascus-saint-george-east-tijara",
        "Saint George Church in East Tijara",
        "كنيسة القديس جاورجيوس، شرق التجارة", "Damascus",
        "East Tijara, Damascus", ["00963 11 2236324"],
    ),
    damascus_church(
        "damascus-annunciation-barze", "Annunciation Church in Barze",
        "كنيسة سيدة البشارة، مساكن برزة", "Damascus",
        "Masaken Barze - Mousbak Al-Sone', Damascus",
    ),
    damascus_church(
        "damascus-archangel-michael-cornish-tijara",
        "Archangel Michael Church in Cornish Tijara",
        "كنيسة رئيس الملائكة مخائيل، كورنيش التجارة", "Damascus",
        "Cornish Tijara, Damascus", ["00963 11 4447126"],
    ),
    damascus_church(
        "jaramana-saint-anthony-great",
        "Saint Anthony the Great Church in Jaramana",
        "كنيسة القديس أنطونيوس الكبير، جرمانا", "Jaramana",
        "Jaramana - Al-Baladiyeh", ["00963 11 5615002"],
    ),
    damascus_church(
        "damascus-saint-nicholas-mazze", "Saint Nicholas Church in Mazze",
        "كنيسة القديس نيقولاوس، المزة", "Damascus", "Mazze, Damascus",
        ["00963 11 6663915"],
    ),
    damascus_church(
        "damascus-saint-dimitri-salhiyeh",
        "Saint Dimitri Church in Salhiyeh",
        "كنيسة القديس ديمتريوس، الصالحية", "Damascus",
        "Salhiyeh - Sebki, Damascus", ["00963 11 3331617"],
    ),
    damascus_church(
        "damascus-saint-ignatius-abou-remaneh",
        "Saint Ignatius Church in Abou Remaneh",
        "كنيسة القديس اغناطيوس، أبو رمانة", "Damascus",
        "Abou Remaneh, Damascus",
        ["00963 11 3735718", "00963 11 3737893"],
    ),
    damascus_church(
        "damascus-saint-ananias-midan", "Saint Ananias Church in Midan",
        "كنيسة القديس حنانيا، الميدان", "Damascus", "Midan, Damascus",
        ["00963 11 8881528"],
    ),
    damascus_church(
        "damascus-saints-peter-paul-dummar",
        "Saints Peter and Paul Church in Dummar",
        "كنيسة القديسين بطرس وبولس، مشروع دمر", "Damascus",
        "Mashrou' Dummar, Damascus", ["00963 11 3111553"],
    ),
    damascus_church(
        "damascus-saint-john-bab-touma",
        "Saint John of Damascus Church in Bab Touma",
        "كنيسة القديس يوحنا الدمشقي، باب توما", "Damascus",
        "Bab Touma - Sefel Al-Tale, Damascus",
    ),
    damascus_church(
        "damascus-saint-george-vault",
        "Saint George Church at the Vault in Damascus",
        "كنيسة القديس جاورجيوس المدفن", "Damascus",
        "Opposite Bab Kissan, Damascus", ["00963 11 4730090"],
    ),
]


RURAL_DAMASCUS_ROWS = [
    damascus_church(
        "jdeidet-artouz-saint-george", "Saint George Church in Jdeidet Artouz",
        "كنيسة القديس جاورجيوس، جديدة عرطوز", "Jdeidet Artouz",
        "Jdeidet Artouz, Rural Damascus", ["00963 11 6810848"],
    ),
    damascus_church(
        "qatana-saint-elias", "Saint Elias Church in Qatana",
        "كنيسة النبي الياس، قطنا", "Qatana", "Qatana, Rural Damascus",
        ["00963 11 6820196"],
    ),
    damascus_church(
        "sahnaya-saint-elias", "Saint Elias Church in Sahnaya",
        "كنيسة النبي الياس، صحنايا", "Sahnaya", "Sahnaya, Rural Damascus",
        ["00963 11 6710679"],
    ),
    damascus_church(
        "hine-saint-elias", "Saint Elias Church in Hine",
        "كنيسة النبي الياس، حينه", "Hine", "Hine, Rural Damascus",
        ["00963 11 6880918"],
    ),
    damascus_church(
        "erne-saint-george", "Saint George Church in Erne",
        "كنيسة القديس جاورجيوس، عرنة", "Erne", "Erne, Rural Damascus",
    ),
    damascus_church(
        "ain-al-shara-saint-george", "Saint George Church in Ain Al-Sha'ra",
        "كنيسة القديس جاورجيوس، عين الشعرة", "Ain Al-Sha'ra",
        "Ain Al-Sha'ra, Rural Damascus",
    ),
    damascus_church(
        "bludan-saint-george", "Saint George Church in Bludan",
        "كنيسة القديس جاورجيوس، بلودان", "Bludan", "Bludan, Rural Damascus",
    ),
    damascus_church(
        "deir-atiyeh-dormition", "Dormition of Our Lady Church in Deir 'Atiyeh",
        "كنيسة رقاد السيدة، دير عطية", "Deir 'Atiyeh",
        "Deir 'Atiyeh, Rural Damascus",
    ),
    damascus_church(
        "saydnaya-nativity-our-lady",
        "Nativity of Our Lady Church at the Monastery and Parish of Saydnaya",
        "كنيسة ميلاد السيدة، الدير ورعية صيدنايا", "Saydnaya",
        "Monastery and Parish of Saydnaya",
        parent="sy-an-our-lady-saydnaya-monastery",
    ),
    damascus_church(
        "maaret-saydnaya-saint-elias",
        "Saint Elias Church in Ma'aret Saydnaya",
        "كنيسة النبي الياس، معرة صيدنايا", "Ma'aret Saydnaya",
        "Ma'aret Saydnaya, Rural Damascus", ["00963 11 5953312"],
    ),
    damascus_church(
        "maarouneh-saint-elias", "Saint Elias Church in Ma'rouneh",
        "كنيسة النبي الياس، معرونة", "Ma'rouneh",
        "Ma'rouneh, Rural Damascus", ["00963 11 5907731"],
    ),
    damascus_church(
        "maalula-saint-elias", "Saint Elias Church in Ma'lula",
        "كنيسة النبي الياس، معلولا", "Ma'lula", "Ma'lula, Rural Damascus",
    ),
    damascus_church(
        "zabadani-dormition", "Dormition of Our Lady Church in Zabadani",
        "كنيسة رقاد السيدة، الزبداني", "Zabadani",
        "Zabadani, Rural Damascus",
    ),
    damascus_church(
        "daraya-saint-thecla", "Saint Thecla Church in Daraya",
        "كنيسة القديسة تقلا، داريا", "Daraya", "Daraya, Rural Damascus",
    ),
    damascus_church(
        "harasta-saint-elias", "Saint Elias Church in Harasta",
        "كنيسة النبي الياس، حرستا", "Harasta", "Harasta, Rural Damascus",
    ),
    damascus_church(
        "erbin-saint-george", "Saint George Church in Erbin",
        "كنيسة القديس جاورجيوس، عربين", "Erbin", "Erbin, Rural Damascus",
    ),
    damascus_church(
        "adra-annunciation", "Annunciation Church in Adra Industrial City",
        "كنيسة سيدة البشارة، مدينة عدرا العمالية", "Adra Industrial City",
        "Adra Industrial City, Rural Damascus",
    ),
]


OTHER_ANTIOCH_ROWS = [
    damascus_church(
        "dweilaa-saint-elias", "Saint Elias Church in Dweilaa",
        "كنيسة مار إلياس، الدويلعة", "Dweilaa", "Dweilaa, Damascus",
        sources=[DWEILAA],
    ),
]


DIRECT_ANTIOCH_ROWS = (
    ANTIOCH_MONASTERY_ROWS + DAMASCUS_ROWS +
    RURAL_DAMASCUS_ROWS + OTHER_ANTIOCH_ROWS
)

DIRECT_RUSSIA_ROWS = [
    body(
        "sy-ru-damascus-saint-ignatius-representation",
        "russia",
        "Church of Saint Ignatius the God-Bearer at the Representation of the Russian Orthodox Church in Damascus",
        "Храм священномученика Игнатия Богоносца при Представительстве Русской Православной Церкви в Дамаске",
        "Damascus",
        "Metochion",
        [RUSSIA_REPRESENTATION, RUSSIA_CURRENT],
        address=[
            "2709, СИРИЯ, г. Дамаск, р-н Малки, ул. Мухамеда аль Бизима, 15",
        ],
        emails=["podvorie-damascus@yandex.ru"],
        site=RUSSIA_REPRESENTATION,
        contact_sources=[RUSSIA_REPRESENTATION],
    ),
]

DIRECT_ROMANIA_ROWS = [
    body(
        "sy-ro-damascus-community",
        "romania",
        "Romanian Orthodox Community in Syria",
        "Comunitatea Ortodoxă Română din Siria",
        "Damascus",
        "Community",
        [ROMANIA_EXTERNAL],
        phones=["+40-742.013.538"],
        emails=["gheorghecostea@yahoo.com"],
        site="https://bordamascsiria.wordpress.com/",
        contact_sources=[ROMANIA_EXTERNAL],
    ),
]


ROWS = {
    "antioch": DIRECT_ANTIOCH_ROWS,
    "russia": DIRECT_RUSSIA_ROWS,
    "romania": DIRECT_ROMANIA_ROWS,
}
EXPECTED = {"antioch": 37, "russia": 1, "romania": 1}
EXPECTED_TOTAL = 39
ALLOWED_KINDS = {"parish", "monastery"}
ALLOWED_RANKS = {
    "Church", "Cathedral", "Patriarchal Monastery", "Metochion", "Community",
}
ALL_SOURCE_ROWS = [
    item for parent_rows in ROWS.values() for item in parent_rows
]
ENGLISH_NAMES = {item["id"]: item["name"] for item in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ALL_SOURCE_ROWS}
CONTACTS = {
    item["id"]: {
        "emails": list(item.get("emails") or []),
        "phones": list(item.get("phones") or []),
        "contact_sources": list(item.get("contact_sources") or []),
    }
    for item in ALL_SOURCE_ROWS
}


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % item.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    return item


def _validate_row(item, seen, branch_seen, names):
    row_id = item.get("id")
    if not row_id or row_id in seen:
        raise ValueError("duplicate or missing id: %s" % row_id)
    if not re.fullmatch(r"[a-z0-9-]+", row_id):
        raise ValueError("%s is not a stable ASCII id" % row_id)
    if item.get("parent") not in branch_seen:
        raise ValueError("%s hangs off an unknown parent: %s" % (
            row_id, item.get("parent"),
        ))
    if item.get("country") != "SY":
        raise ValueError("%s is outside Syria" % row_id)
    if item.get("kind") not in ALLOWED_KINDS:
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if not item.get("name") or not item.get("local") or not item.get("seat"):
        raise ValueError("%s lacks a usable name or seat" % row_id)
    name_key = item["name"].casefold()
    if name_key in names:
        raise ValueError("duplicate reader-facing name: %s and %s" % (
            names[name_key], row_id,
        ))
    if item.get("address") and (
            not isinstance(item["address"], list) or
            not all(isinstance(line, str) and line.strip()
                    for line in item["address"])):
        raise ValueError("%s has an invalid address" % row_id)
    if item.get("site") and not item["site"].startswith("https://"):
        raise ValueError("%s has a non-HTTPS site" % row_id)
    rendered = json.dumps(item, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("%s has forbidden punctuation or encoding" % row_id)
    seen.add(row_id)
    branch_seen.add(row_id)
    names[name_key] = row_id


def build():
    payloads = {}
    seen = set(ROWS)
    names = {}
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            _validate_row(item, seen, branch_seen, names)
            rows.append(item)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "SY",
            "rows": rows,
        }

    row_ids = {item["id"] for item in ALL_SOURCE_ROWS}
    if set(ENGLISH_NAMES) != row_ids or len(row_ids) != EXPECTED_TOTAL:
        raise ValueError("Syria English name map is out of sync")
    if set(CONTACTS) != row_ids:
        raise ValueError("Syria contact map is out of sync")
    for row_id, contact in CONTACTS.items():
        if set(contact) != {"emails", "phones", "contact_sources"}:
            raise ValueError("%s contact map has the wrong fields" % row_id)
        has_contacts = bool(contact["emails"] or contact["phones"])
        if has_contacts != bool(contact["contact_sources"]):
            raise ValueError("%s contact provenance is out of sync" % row_id)
        if len(contact["contact_sources"]) > 3 or not all(
                str(url).startswith("https://")
                for url in contact["contact_sources"]):
            raise ValueError("%s contact map has invalid sources" % row_id)
        if not all(isinstance(value, str) and value.strip()
                   for key in ("emails", "phones")
                   for value in contact[key]):
            raise ValueError("%s contact map has an empty value" % row_id)
    if sum(bool(value["emails"] or value["phones"])
           for value in CONTACTS.values()) != 25:
        raise ValueError("Syria contact-bearing row total is out of sync")
    if sum(len(value["emails"]) for value in CONTACTS.values()) != 2:
        raise ValueError("Syria email total is out of sync")
    if sum(len(value["phones"]) for value in CONTACTS.values()) != 29:
        raise ValueError("Syria phone total is out of sync")
    if sum(EXPECTED.values()) != EXPECTED_TOTAL:
        raise ValueError("Syria branch total must remain %d" % EXPECTED_TOTAL)
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "SY":
        raise ValueError("Syria candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Syria candidate ledger check date is out of sync")
    expected_summary = {
        "antioch": 37,
        "russia": 1,
        "romania": 1,
        "total": EXPECTED_TOTAL,
        "canonical_jurisdictions_represented": 3,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Syria candidate ledger totals are out of sync")
    required_lists = (
        "candidates", "reconciliation", "exclusions",
        "official_jurisdiction_audit",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Syria candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "SY":
            raise ValueError("%s is outside Syria" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Syria candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Syria ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Syria ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("Syria candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Syria: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Syria: 39 current officially named bodies across "
            "3 canonical jurisdictions"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
