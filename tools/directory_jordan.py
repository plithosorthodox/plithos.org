#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Jordan.

The live Jordan Metropolis roster is reconciled with the Jerusalem
Patriarchate's East Bank roster and its 2025 official calendar. The union
keeps current parish churches, monasteries, and named shrines while removing
duplicate spellings of the same body.

    python tools/directory_jordan.py --check
    python tools/directory_jordan.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "jordan.json"
LOCAL_ROSTER = (
    "https://orthodoxjordan.org/"
    "%D8%A7%D9%84%D9%83%D9%86%D8%A7%D8%A6%D8%B3/"
)
PATRIARCHATE_ROSTER = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "churches-in-the-east-bank-jordan/"
)
CALENDAR_2025 = (
    "https://ar.jerusalem-patriarchate.info/wp-content/uploads/2025/03/"
    "ARABIC_CALENDAR_OF_PATRIARCHATE-2025_R.pdf"
)


def body(row_id, name, local, seat, rank="Church", kind="parish",
         sources=None):
    return {
        "id": row_id,
        "parent": "je-amman",
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "JO",
        "sources": sources or [LOCAL_ROSTER, PATRIARCHATE_ROSTER],
    }


CURRENT = [LOCAL_ROSTER, PATRIARCHATE_ROSTER]
CALENDAR_ONLY = [PATRIARCHATE_ROSTER, CALENDAR_2025]

ROWS = {
    "je-amman": [
        body("jo-amman-swaifyeh-saint-nectarios",
             "Monastery of Saint Nectarios in Swaifyeh",
             "كنيسة دير القديس نكتاريوس الصويفية - عمان", "Amman",
             "Monastery", "monastery", [LOCAL_ROSTER]),
        body("jo-amman-swaifyeh-presentation-cathedral",
             "Cathedral of the Presentation of the Lord in Swaifyeh",
             "كاتدرائية دخول السيد الى الهيكل الصويفية - عمان", "Amman",
             "Cathedral"),
        body("jo-amman-abdali-annunciation-cathedral",
             "Cathedral of the Annunciation of the Theotokos in Abdali",
             "كاتدرائية البشارة العبدلي - عمان", "Amman", "Cathedral"),
        body("jo-amman-downtown-transfiguration",
             "Church of the Transfiguration of the Saviour in Downtown Amman",
             "كنيسة المخلص وسط البلد - عمان", "Amman"),
        body("jo-amman-khalda-ascension",
             "Church of the Ascension of the Lord in Khalda",
             "كنيسة الصعود الإلهي خلدا - عمان", "Amman"),
        body("jo-amman-abu-nseir-elias-barbara",
             "Church of Prophet Elias and Saint Barbara in Abu Nseir",
             "كنيسة النبي إيليا والقديسة بربارة ابو نصير - عمان", "Amman"),
        body("jo-amman-jabal-al-taj-nativity-theotokos",
             "Church of the Nativity of the Theotokos in Jabal al-Taj",
             "كنيسة ميلاد السيدة العذارء جبل التاج - عمان", "Amman"),
        body("jo-amman-jabal-al-hashmi-saint-george",
             "Church of Saint George in Jabal al-Hashmi",
             "كنيسة القديس جاورجيوس جبل الهاشمي - عمان", "Amman"),
        body("jo-amman-marka-saint-nicholas",
             "Church of Saint Nicholas in Marka",
             "كنيسة القديس نيقولاوس ماركا - عمان", "Amman"),
        body("jo-amman-marj-al-hamam-constantine-helen",
             "Church of Saints Constantine and Helen in Marj al-Hamam",
             "كنيسة القديسين قسطنطين وهيلانه مرج الحمام - عمان", "Amman"),

        body("jo-fuheis-saint-george-monastery",
             "Monastery of Saint George in Fuheis",
             "كنيسة دير القديس جاورجيوس الفحيص - البلقاء", "Fuheis",
             "Monastery", "monastery"),
        body("jo-fuheis-saint-james",
             "Church of Saint James the Brother of the Lord in Fuheis",
             "كنيسة القديس يعقوب أخو الرب الفحيص - البلقاء", "Fuheis"),
        body("jo-mahis-saint-george-shrine",
             "Shrine of Saint George in Mahis",
             "مزار القديس جيرجيوس في ماحص", "Mahis", "Shrine", "parish",
             CALENDAR_ONLY),
        body("jo-fuheis-ancient-saint-george",
             "Ancient Church of Saint George in Fuheis",
             "كنيسة القديس جاورجيوس الأثرية الفحيص - البلقاء", "Fuheis"),
        body("jo-salt-dormition-monastery",
             "Dormition Monastery in Salt",
             "كنيسة دير رقاد السيدة العذارء السلط - البلقاء", "Salt",
             "Monastery", "monastery"),
        body("jo-salt-ancient-saint-george",
             "Ancient Church of Saint George in Salt",
             "كنيسة القديس جاورجيوس الأثرية السلط - البلقاء", "Salt"),
        body("jo-salt-sarah-ancient-transfiguration",
             "Ancient Church of the Transfiguration in Sarah, Salt",
             "كنيسة التجلي الأثرية (سارة) السلط - البلقاء", "Salt"),
        body("jo-rmeimin-dormition",
             "Church of the Dormition of the Theotokos in Rmeimin",
             "كنيسة رقاد والدة الإله ارميمين - البلقاء", "Rmeimin"),
        body("jo-safout-saint-george",
             "Church of Saint George in Safout",
             "كنيسة القديس جاورجيوس صافوط - البلقاء", "Safout"),

        body("jo-zarqa-saint-george-monastery",
             "Monastery of Saint George in Zarqa",
             "كنيسة دير القديس جاورجيوس الزرقاء", "Zarqa",
             "Monastery", "monastery"),
        body("jo-irbid-saint-george-monastery",
             "Monastery of Saint George in Irbid",
             "كنيسة دير القديس جاورجيوس اربد", "Irbid",
             "Monastery", "monastery"),
        body("jo-al-husn-saint-george",
             "Church of Saint George in Al-Husn",
             "كنيسة القديس جاورجيوس الحصن - اربد", "Al-Husn"),
        body("jo-al-sarih-saint-nicholas",
             "Church of Saint Nicholas in Al-Sarih",
             "كنيسة القديس نيقولاوس الصريح - اربد", "Al-Sarih"),
        body("jo-shatana-saint-george",
             "Church of Saint George in Shatana",
             "كنيسة القديس جاورجيوس شطنا - اربد", "Shatana"),

        body("jo-ajloun-saint-george-monastery",
             "Monastery of Saint George in Ajloun",
             "كنيسة دير القديس جاورجيوس عجلون", "Ajloun",
             "Monastery", "monastery"),
        body("jo-ajloun-holy-spirit",
             "Church of the Holy Spirit in Ajloun",
             "كنيسة الروح القدس عجلون", "Ajloun"),
        body("jo-listib-prophet-elias-shrine",
             "Shrine of Prophet Elias in Listib",
             "مزار النبي إيليا (مار الياس) حيث الموقع الأثري في الستب",
             "Listib", "Shrine", "parish", CALENDAR_ONLY),
        body("jo-anjara-saint-george",
             "Church of Saint George in Anjara",
             "كنيسة القديس جاورجيوس عنجرة - عجلون", "Anjara"),
        body("jo-wahadneh-prophet-elias",
             "Church of Prophet Elias in Wahadneh",
             "كنيسة النبي ايليا الوهادنة - عجلون", "Wahadneh"),

        body("jo-mafraq-dormition",
             "Church of the Dormition of the Theotokos in Mafraq",
             "كنيسة رقاد والدة الإله المفرق", "Mafraq"),
        body("jo-jerash-saint-george",
             "Church of Saint George in Jerash",
             "كنيسة القديس جاورجيوس جرش", "Jerash"),
        body("jo-souf-saint-george-shrine",
             "Shrine of Saint George in Souf",
             "مزار القديس جورجيوس في سوف", "Souf", "Shrine", "parish",
             CALENDAR_ONLY),

        body("jo-madaba-map-saint-george-monastery",
             "Saint George Map Church and Monastery in Madaba",
             "كنيسة دير القديس جاورجيوس (الخارطة) البلد - مأدبا", "Madaba",
             "Monastery", "monastery"),
        body("jo-madaba-hanina-dormition",
             "Church of the Dormition of the Theotokos in Hanina",
             "كنيسة رقاد والدة الإله حنينا - مأدبا", "Madaba"),
        body("jo-main-saint-john-baptist",
             "Shrine of Saint John the Baptist in Ma'in",
             "مزار القديس يوحنا المعمدان في ماعين", "Ma'in", "Shrine",
             "parish", CALENDAR_ONLY),

        body("jo-karak-saint-george-monastery",
             "Monastery of Saint George in Karak",
             "كنيسة دير القديس جاورجيوس الكرك", "Karak",
             "Monastery", "monastery"),
        body("jo-ader-saint-george",
             "Church of Saint George in Ader",
             "كنيسة القديس جاورجيوس أدر - الكرك", "Ader"),
        body("jo-hamoud-saint-george",
             "Church of Saint George in Hamoud",
             "كنيسة القديس جاورجيوس الحمود - الكرك", "Hamoud"),
        body("jo-rabbah-saint-george",
             "Church of Saint George in Rabbah",
             "كنيسة القديس جاورجيوس الربة - الكرك", "Rabbah"),
        body("jo-ader-prophet-elias",
             "Church of Prophet Elias in Ader",
             "كنيسة مار إلياس أدر -الكرك", "Ader", sources=[LOCAL_ROSTER]),
        body("jo-aqaba-saint-nicholas-monastery",
             "Monastery of Saint Nicholas in Aqaba",
             "كنيسة دير القديس نيقولاوس العقبة", "Aqaba",
             "Monastery", "monastery"),

        body("jo-dibin-three-hierarchs",
             "Church of the Three Holy Hierarchs in Dibin",
             "كنيسة الأقمار الثلاث دبين-جرش", "Dibin", sources=[LOCAL_ROSTER]),
        body("jo-dibin-life-giving-spring-monastery",
             "Monastery of the Theotokos of the Life-Giving Spring in Dibin",
             "دير السيدة العذراء ينبوع الحياة دبين- جرش", "Dibin",
             "Monastery", "monastery", [LOCAL_ROSTER]),
        body("jo-al-maghtas-theophany-monastery",
             "Patriarchal Monastery of the Theophany at Al-Maghtas",
             "دير الظهور الإلهي البطريركي المغطس", "Al-Maghtas",
             "Patriarchal Monastery", "monastery", [LOCAL_ROSTER]),
        body("jo-taybeh-saint-george-shrine",
             "Shrine of Saint George in Taybeh",
             "مزار القديس جيورجيوس في الطيبة", "Taybeh", "Shrine", "parish",
             CALENDAR_ONLY),
        body("jo-kufran-saint-george-shrine",
             "Shrine of Saint George in Kufran",
             "مزار القديس جيورجيوس في كفرعان", "Kufran", "Shrine", "parish",
             CALENDAR_ONLY),
    ],
}

DIRECT_RUSSIA_ROWS = [
    {
        "id": "jo-ru-baptism-site-metochion",
        "parent": "russia",
        "kind": "parish",
        "rank": "Metochion",
        "name": "Russian Ecclesiastical Mission Metochion at the Site of the Baptism of the Lord",
        "local": "Подворье Русской Духовной Миссии на месте Крещения Господня в Иордании",
        "seat": "Al-Maghtas",
        "country": "JO",
        "checked": CHECKED,
        "sources": [
            "https://rusdm.ru/gps/",
            "https://rusdm.ru/hotels/322",
            "https://mospat.ru/en/news/92066/",
        ],
    },
]

EXPECTED = {"je-amman": 46}
EXPECTED_TOTAL = 47
ALL_SOURCE_ROWS = ROWS["je-amman"] + DIRECT_RUSSIA_ROWS
ENGLISH_NAMES = {row["id"]: row["name"] for row in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ALL_SOURCE_ROWS}


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    return row


def build():
    payloads = {}
    seen = set(ROWS)
    total = 0
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if row.get("parent") != parent or row.get("country") != "JO":
                raise ValueError("%s hangs outside Jordan" % row_id)
            if row.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        total += len(rows)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "JO",
            "rows": rows,
        }
    direct = []
    for source in DIRECT_RUSSIA_ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing direct id: %s" % row_id)
        if row.get("parent") != "russia" or row.get("country") != "JO":
            raise ValueError("%s hangs outside Jordan" % row_id)
        seen.add(row_id)
        direct.append(row)
    if total + len(direct) != EXPECTED_TOTAL:
        raise ValueError("Jordan must publish exactly %d rows" % EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Jordan English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "JO":
        raise ValueError("Jordan candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Jordan candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("je-amman") != 46 or summary.get("russia") != 1 or \
            summary.get("total") != EXPECTED_TOTAL:
        raise ValueError("Jordan candidate ledger totals are out of sync")
    for key in ("candidates", "reconciliation", "official_jurisdiction_audit",
                "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Jordan candidate ledger lacks %s" % key)
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("Jordan candidate ledger has forbidden punctuation")
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
        print("directory Jordan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Jordan: 47 current bodies under two canonical parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
