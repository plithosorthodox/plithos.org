#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Palestine.

The current Jerusalem Patriarchate rosters are reconciled with current
Moscow, ROCOR, and Romanian Holy Land directories. Historical sites,
aggregate references, and affiliation-unclear discoveries remain in the
country candidate ledger.

    python tools/directory_palestine.py --check
    python tools/directory_palestine.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "palestine.json"

JP_OUTSIDE = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "holy-monasteries-and-hegoumeneia-abbots-quarters-outside-jerusalem/"
)
JP_WEST_BANK = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "churches-in-the-west-bank/"
)
JP_EXTERNAL = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "russian-speaking-community-parishes/"
)
JP_SHRINES = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "all-holy-pilgrimage-sites/"
)
JP_COMMITTEES = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "patriarchal-management-committees/"
)
JP_GAZA_2026 = (
    "https://ar.jerusalem-patriarchate.info/wp-content/uploads/2026/02/"
    "arabic_2026.pdf"
)
JP_BURQIN = (
    "https://en.jerusalem-patriarchate.info/articles-speeches/"
    "the-church-of-the-ten-lepers-in-the-town-of-burqin/"
)
JP_NISF_JUBEIL = (
    "https://en.jerusalem-patriarchate.info/projects/"
    "st-george-church-consecrated-in-nisf-ijbil/"
)
JP_SEBASTIA = (
    "https://en.jerusalem-patriarchate.info/liturgic-life/"
    "the-commemoration-of-the-beheading-of-st-john-the-forerunner-at-the-patriarchate/"
)
JP_JOHN_BAPTIST = (
    "https://en.jerusalem-patriarchate.info/announcements/"
    "the-h-monastery-of-st-john-the-baptist-in-the-jordan-river-is-reopened/"
)
ROCOR_CONTACTS = "https://missionrocor.ru/contacts"
MP_CHAPELS = "https://rusdm.ru/chapel/"
MP_HISTORY = "https://rusdm.ru/history/392"
RO_EXTERNAL = (
    "https://patriarhia.ro/en/organization-of-the-romanian-orthodox-church/"
    "external-representations-and-communities/"
)


def body(row_id, parent, name, seat, rank="Church", kind="parish",
         sources=None, local=None, **extra):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "seat": seat,
        "country": "PS",
        "sources": sources or [JP_WEST_BANK],
    }
    if local:
        row["local"] = local
    row.update(extra)
    if row.get("emails") or row.get("phones"):
        row.setdefault("contact_sources", list(row["sources"][:1]))
        row.setdefault("contact_checked", CHECKED)
    return row


JERUSALEM_ROWS = [
    body("ps-je-bethlehem-nativity", "jerusalem",
         "Holy Bethlehem and the Church of the Nativity", "Bethlehem",
         "Shrine", sources=[JP_SHRINES],
         address=["Greek Orthodox Convent", "P.O. Box 52", "Bethlehem"],
         phones=["02/2742440", "02/2748049"],
         emails=["orthodox_nativity_church@yahoo.com"]),
    body("ps-je-saint-savvas-lavra", "jerusalem",
         "Holy Lavra of Saint Savvas the Sanctified", "Judean Desert",
         "Lavra", "monastery", [JP_OUTSIDE],
         address=["Holy Lavra of St. Savvas", "P.O. Box 19824",
                  "Jerusalem 91199"], phones=["+972-2-2762915"],
         emails=["imas.jer@yandex.com"]),
    body("ps-je-saint-george-hozevite", "jerusalem",
         "Holy Monastery of Saint George the Hozevite", "Wadi Qelt",
         "Monastery", "monastery", [JP_OUTSIDE],
         address=["P.O. Box 31388", "Jerusalem 91001", "Israel"],
         phones=["00972/547/306557"]),
    body("ps-je-mount-temptation", "jerusalem",
         "Holy Monastery of Mount Sarantario of Temptation", "Jericho",
         "Monastery", "monastery", [JP_OUTSIDE],
         address=["Greek Orthodox Convent", "P.O. Box 21", "Jericho"],
         phones=["02/2322827"]),
    body("ps-je-bethany-martha-maria", "jerusalem",
         "Holy Monastery of Martha and Maria in Bethany", "Bethany",
         "Monastery", "monastery", [JP_OUTSIDE],
         address=["Greek Orthodox Convent", "P.O. Box 19121", "Jerusalem"],
         phones=["+972-2-2799708"]),
    body("ps-je-abba-gerasimos", "jerusalem",
         "Holy Monastery of Abba Gerasimos of the Jordan", "Jericho",
         "Monastery", "monastery", [JP_OUTSIDE],
         address=["Greek Orthodox Convent", "P.O. Box 35", "Jericho"],
         phones=["02/9943038"]),
    body("ps-je-abba-theodosius", "jerusalem",
         "Holy Monastery of Abba Theodosius the Cenobiarch", "Ubeidiya",
         "Monastery", "monastery", [JP_OUTSIDE],
         address=["Greek Orthodox Convent", "P.O. Box 1102",
                  "Jerusalem 91010", "Israel"],
         phones=["02/2761223", "0512/081144"]),
    body("ps-je-jacobs-well", "jerusalem",
         "Holy Monastery of Jacob's Well in Samaria", "Nablus",
         "Monastery", "monastery", [JP_OUTSIDE]),
    body("ps-je-prophet-elisha", "jerusalem",
         "Holy Monastery of the Prophet Elisha of Jericho", "Jericho",
         "Monastery", "monastery", [JP_OUTSIDE],
         address=["Greek Orthodox Convent", "P.O. Box 89", "Jericho"],
         phones=["02/2322433", "0507/375139"]),
    body("ps-je-shepherds-beit-sahour", "jerusalem",
         "Holy Monastery of the Shepherds in Beit Sahour", "Beit Sahour",
         "Monastery", "monastery", [JP_OUTSIDE],
         phones=["02/2773135", "0522/810522"]),
    body("ps-je-beit-jala-al-khader-saint-george", "jerusalem",
         "Holy Monastery of Saint George in Beit Jala, Al-Khader",
         "Al-Khader", "Monastery", "monastery", [JP_OUTSIDE],
         phones=["02/2743233", "0528/658828", "0544/598201"]),
    body("ps-je-jordan-john-baptist", "jerusalem",
         "Holy Monastery of Saint John the Baptist on the Jordan River",
         "Jordan River", "Monastery", "monastery",
         [JP_OUTSIDE, JP_JOHN_BAPTIST], phones=["00972 543158798"]),
    body("ps-je-jordan-theophany", "jerusalem",
         "Holy Patriarchal Monastery of the Theophany", "Jordan River",
         "Patriarchal Monastery", "monastery", [JP_OUTSIDE],
         phones=["+972/79/6831809"]),
    body("ps-je-ramallah-transfiguration", "jerusalem",
         "Church of the Transfiguration of the Saviour in Ramallah",
         "Ramallah", sources=[JP_OUTSIDE],
         address=["Greek Orthodox Convent", "P.O. Box 307", "Ramallah"],
         phones=["02/2964684", "0599/805586", "02/29656618"]),
    body("ps-je-ramallah-saint-stephen", "jerusalem",
         "Holy Monastery of the First Martyr and Archdeacon Stephen in Ramallah",
         "Ramallah", "Monastery", "monastery", [JP_OUTSIDE],
         phones=["0599/805586"]),
    body("ps-je-ain-farah-saint-chariton", "jerusalem",
         "Lavra of Saint Chariton at Ain Farah", "Ain Farah", "Lavra",
         "monastery", [JP_OUTSIDE]),

    body("ps-je-beit-sahour-forefathers", "jerusalem",
         "Holy Church of the Forefathers in Beit Sahour", "Beit Sahour",
         sources=[JP_WEST_BANK], phones=["02/2773081"]),
    body("ps-je-birzeit-saint-george", "jerusalem",
         "Holy Church of Saint George in Birzeit", "Birzeit",
         sources=[JP_WEST_BANK]),
    body("ps-je-jifna-saint-george", "jerusalem",
         "Holy Church of Saint George in Jifna", "Jifna",
         sources=[JP_WEST_BANK], phones=["02/2818359", "0599/392383"]),
    body("ps-je-taybeh-saint-george", "jerusalem",
         "Holy Church of Saint George in Taybeh", "Taybeh",
         sources=[JP_WEST_BANK], phones=["02/2898282", "0599/127867"]),
    body("ps-je-ain-arik-dormition", "jerusalem",
         "Holy Church of the Dormition of the Theotokos in Ain Arik",
         "Ain Arik", sources=[JP_WEST_BANK],
         phones=["02/2905013", "0599/732993"]),
    body("ps-je-aboud-dormition", "jerusalem",
         "Holy Church of the Dormition of the Theotokos in Aboud", "Aboud",
         sources=[JP_WEST_BANK], phones=["02/2972043", "0597/952779"],
         emails=["orthodox.aboud@gmail.com"]),
    body("ps-je-tulkarm-saint-george", "jerusalem",
         "Holy Church of Saint George in Tulkarm", "Tulkarm",
         sources=[JP_WEST_BANK]),
    body("ps-je-zababdeh-saint-george", "jerusalem",
         "Holy Church of Saint George in Zababdeh", "Zababdeh",
         sources=[JP_WEST_BANK], phones=["04/2510215"]),
    body("ps-je-tubas-holy-trinity", "jerusalem",
         "Holy Trinity Church in Tubas", "Tubas", sources=[JP_WEST_BANK],
         phones=["0599/270699"]),

    body("ps-je-beit-jala-nativity-theotokos", "jerusalem",
         "Holy Church of the Nativity of the Theotokos in Beit Jala",
         "Beit Jala", sources=[JP_EXTERNAL], phones=["02/2743178"]),
    body("ps-je-beit-jala-saint-nicholas", "jerusalem",
         "Holy Church of Saint Nicholas in Beit Jala", "Beit Jala",
         sources=[JP_EXTERNAL], phones=["02/2743178"]),
    body("ps-je-beit-jala-archangel-michael", "jerusalem",
         "Holy Church of Archangel Michael in Beit Jala", "Beit Jala",
         sources=[JP_EXTERNAL], phones=["02/2743178"]),
    body("ps-je-rafidia-annunciation", "jerusalem",
         "Holy Church of the Annunciation of the Theotokos in Rafidia",
         "Rafidia", sources=[JP_EXTERNAL]),
    body("ps-je-rafidia-saint-moses", "jerusalem",
         "Holy Church of Saint Moses the Ethiopian in Rafidia", "Rafidia",
         sources=[JP_EXTERNAL]),
    body("ps-je-nablus-saint-demetrios", "jerusalem",
         "Holy Church of Saint Demetrios in Nablus", "Nablus",
         sources=[JP_EXTERNAL]),
    body("ps-je-burqin-saint-george", "jerusalem",
         "Holy Church of Saint George and the Shrine of the Ten Lepers in Burqin",
         "Burqin", "Shrine", sources=[JP_EXTERNAL, JP_BURQIN],
         phones=["0569/397582"]),
    body("ps-je-nisf-jubeil-saint-george", "jerusalem",
         "Holy Church of Saint George in Nisf Jubeil", "Nisf Jubeil",
         sources=[JP_EXTERNAL, JP_NISF_JUBEIL]),
    body("ps-je-sebastia-saint-john-baptist", "jerusalem",
         "Holy Church of Saint John the Baptist in Sebastia", "Sebastia",
         "Shrine", sources=[JP_SEBASTIA]),
]


GAZA_ROWS = [
    body("ps-je-gaza-saint-porphyrios", "je-gaza",
         "Holy Monastery of Saint Porphyrios in Gaza", "Gaza City",
         "Monastery", "monastery", [JP_COMMITTEES, JP_GAZA_2026],
         address=["Greek Orthodox Convent", "Old City, Zeitoun Quarter",
                  "Church Street", "Gaza"],
         phones=["+970/591/81080", "+972/503/073223", "08/2818019",
                 "08/2818021"], emails=["churchorthodox@yahoo.com"],
         contact_sources=[JP_COMMITTEES, JP_GAZA_2026]),
]


ROCOR_ROWS = [
    body("ps-rocor-bethany-resurrection-sisterhood",
         "ru-jerusalem-mission-rocor",
         "Bethany Sisterhood of the Lord's Resurrection", "Bethany",
         "Sisterhood", "monastery", [ROCOR_CONTACTS],
         local="Вифания, Община Воскресения Христова",
         address=["P.O. Box 20607", "Jerusalem 91205", "Israel"],
         site="https://bethany-community.org/", phones=["+972 (2) 279 0316"],
         emails=["bethany.school.girls@gmail.com"]),
    body("ps-rocor-wadi-faran-saint-chariton",
         "ru-jerusalem-mission-rocor",
         "Monastery of Saint Chariton in Wadi Faran", "Wadi Faran",
         "Monastery", "monastery", [ROCOR_CONTACTS],
         local="Фара. Монастырь преподобного Харитона Исповедника",
         phones=["+972 52 539 9075"]),
]


ROWS = {
    "jerusalem": JERUSALEM_ROWS,
    "je-gaza": GAZA_ROWS,
    "ru-jerusalem-mission-rocor": ROCOR_ROWS,
}


DIRECT_RUSSIA_ROWS = [
    body("ps-mp-hebron-forefathers", "ru-jerusalem-mission-mp",
         "Metochion of the Holy Forefathers in Hebron", "Hebron",
         "Metochion", sources=[MP_CHAPELS, MP_HISTORY],
         local="Подворье в честь святых Праотцев в Хевроне",
         address=["Al-Jalada Str. (Am Maabad Str.)", "Khalla al-Magarib",
                  "Hebron", "Palestine"], phones=["050-902-26-42"]),
    body("ps-mp-jericho-zacchaeus", "ru-jerusalem-mission-mp",
         "Metochion of the Apostle Zacchaeus in Jericho", "Jericho",
         "Metochion", sources=[MP_CHAPELS, MP_HISTORY],
         local="Подворье в честь апостола Закхея в Иерихоне",
         address=["Yadr El Ballad", "Jericho", "Palestine"],
         phones=["02-232-45-50", "052-385-98-64", "056-909-50-48"]),
]


DIRECT_ROMANIA_ROWS = [
    body("ps-ro-jericho-establishment", "romania",
         "Romanian Establishment in Jericho", "Jericho", "Settlement",
         sources=[RO_EXTERNAL], local="Aşezământul Românesc din Ierihon",
         address=["47-49 Kamal Nasser Str", "Jericho", "Palestine",
                  "Via Israel"], site="https://www.jerusalem.ro/",
         phones=["009.722.232.46.21"], emails=["evgheniast@yahoo.com"]),
]


EXPECTED = {
    "jerusalem": 34,
    "je-gaza": 1,
    "ru-jerusalem-mission-rocor": 2,
}
EXPECTED_TOTAL = 40
ALL_SOURCE_ROWS = (
    JERUSALEM_ROWS + GAZA_ROWS + ROCOR_ROWS + DIRECT_RUSSIA_ROWS +
    DIRECT_ROMANIA_ROWS
)
LOCAL_NAMES = {
    "ps-je-bethlehem-nativity": "كنيسة المهد في بيت لحم",
    "ps-je-ramallah-transfiguration": "دير تجلّي المخلّص في رام الله",
    "ps-je-beit-sahour-forefathers": "كنيسة الأجداد في بيت ساحور",
    "ps-je-birzeit-saint-george": "كنيسة القدّيس جيورجيوس في بيرزيت",
    "ps-je-jifna-saint-george": "كنيسة القدّيس جيورجيوس في جفنا",
    "ps-je-taybeh-saint-george": "كنيسة القديس جيورجيوس في الطيبة",
    "ps-je-ain-arik-dormition": "كنيسة رقاد والدة الإله في عين عريك",
    "ps-je-aboud-dormition": "كنيسة رقاد والدة الإله في عابود",
    "ps-je-tulkarm-saint-george": "كنيسة القدّيس جيورجيوس في طولكرم",
    "ps-je-zababdeh-saint-george": "كنيسة القدّيس جيورجيوس في الزبابدة",
    "ps-je-tubas-holy-trinity": "كنيسة الثالوث الأقدس في طوباس",
    "ps-je-beit-jala-nativity-theotokos":
        "كنيسة ميلاد والدة الإله في بيت جالا",
    "ps-je-beit-jala-saint-nicholas":
        "كنيسة القديس نيقولاوس في بيت جالا",
    "ps-je-beit-jala-archangel-michael":
        "كنيسة رئيس الملائكة ميخائيل في بيت جالا",
    "ps-je-rafidia-annunciation": "كنيسة بشارة والدة الإله في رفيديا",
    "ps-je-rafidia-saint-moses": "كنيسة البار موسى الحبشي في رفيديا",
    "ps-je-nablus-saint-demetrios":
        "الكنيسة المقدسة للقديس ديميتريوس في نابلس",
    "ps-je-burqin-saint-george":
        "كنيسة القديس جورجيوس وشفاء العشرة البرص في برقين",
    "ps-je-nisf-jubeil-saint-george":
        "كنيسة القديس جورجيوس في نصف اجبيل",
    "ps-je-sebastia-saint-john-baptist":
        "كنيسة القديس يوحنّا المعمدان في سبسطية",
}
for row in ALL_SOURCE_ROWS:
    if row["id"] in LOCAL_NAMES:
        row["local"] = LOCAL_NAMES[row["id"]]
        if JP_GAZA_2026 not in row["sources"]:
            row["sources"].append(JP_GAZA_2026)
ENGLISH_NAMES = {row["id"]: row["name"] for row in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ALL_SOURCE_ROWS}
CONTACTS = {
    row["id"]: {
        "emails": list(row.get("emails") or []),
        "phones": list(row.get("phones") or []),
        "contact_sources": list(row.get("contact_sources") or []),
    }
    for row in ALL_SOURCE_ROWS
}


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
    for key in ("address", "emails", "phones", "contact_sources"):
        if row.get(key) and (not isinstance(row[key], list) or not all(
                isinstance(value, str) and value.strip()
                for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    if bool(row.get("emails") or row.get("phones")) != bool(
            row.get("contact_sources")):
        raise ValueError("%s contact provenance is out of sync" % row.get("id"))
    if row.get("contact_sources") and (
            len(row["contact_sources"]) > 3 or not all(
                url.startswith("https://") for url in row["contact_sources"])):
        raise ValueError("%s has invalid contact sources" % row.get("id"))
    if row.get("contact_sources") and row.get("contact_checked") != CHECKED:
        raise ValueError("%s has a stale contact check date" % row.get("id"))
    if row.get("site") and not row["site"].startswith("https://"):
        raise ValueError("%s has a non-HTTPS body site" % row.get("id"))
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    return row


def validate_rows(source_rows, root_parent, seen, external_parents=None):
    rows = []
    branch_seen = {root_parent} | set(external_parents or [])
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") not in branch_seen:
            raise ValueError("%s hangs off unknown parent %r" %
                             (row_id, row.get("parent")))
        if row.get("country") != "PS":
            raise ValueError("%s is outside Palestine" % row_id)
        if row.get("kind") not in {"diocese", "parish", "monastery"}:
            raise ValueError("%s has an unsupported kind" % row_id)
        if not row.get("name") or not row.get("seat"):
            raise ValueError("%s lacks a usable English name or seat" % row_id)
        seen.add(row_id)
        branch_seen.add(row_id)
        rows.append(row)
    return rows


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = validate_rows(source_rows, parent, seen)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "PS",
            "rows": rows,
        }
    validate_rows(DIRECT_RUSSIA_ROWS, "russia", seen,
                  {"ru-jerusalem-mission-mp"})
    validate_rows(DIRECT_ROMANIA_ROWS, "romania", seen)
    row_ids = {row["id"] for row in ALL_SOURCE_ROWS}
    if set(ENGLISH_NAMES) != row_ids or set(CONTACTS) != row_ids:
        raise ValueError("Palestine English name or contact map is out of sync")
    if len(row_ids) != EXPECTED_TOTAL:
        raise ValueError("Palestine must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if sum(EXPECTED.values()) + len(DIRECT_RUSSIA_ROWS) + \
            len(DIRECT_ROMANIA_ROWS) != EXPECTED_TOTAL:
        raise ValueError("Palestine branch total is out of sync")
    if sum(bool(item["emails"] or item["phones"])
           for item in CONTACTS.values()) != 31:
        raise ValueError("Palestine contact-bearing row total is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "PS":
        raise ValueError("Palestine candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Palestine candidate ledger check date is out of sync")
    expected = dict(EXPECTED)
    expected.update({"russia": 2, "romania": 1, "total": EXPECTED_TOTAL})
    if ledger.get("published_summary") != expected:
        raise ValueError("Palestine candidate ledger totals are out of sync")
    for key in ("candidates", "reconciliation", "official_jurisdiction_audit",
                "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Palestine candidate ledger lacks %s" % key)
    classes = {item.get("classification") for item in ledger["candidates"]}
    required = {"unnamed", "aggregate-only", "historical", "uncertain",
                "noncanonical", "affiliation-unclear"}
    if not required.issubset(classes):
        raise ValueError("Palestine candidate ledger lacks required lead classes")
    for section in ("candidates", "reconciliation",
                    "official_jurisdiction_audit", "exclusions"):
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or not all(
                    isinstance(url, str) and url.startswith("https://")
                    for url in sources):
                raise ValueError("Palestine ledger has invalid %s sources" %
                                 section)
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("Palestine candidate ledger has forbidden punctuation")
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
        print("directory Palestine: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Palestine: 40 current bodies under five canonical branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
