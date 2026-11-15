#!/usr/bin/env python3
"""Current officially named canonical Orthodox bodies in the Philippines.

The Moscow Patriarchate's exarchal map supplies the national baseline. The
current diocesan clergy roster and recent diocesan worship records reconcile
renamed bodies and add active parishes, missions, and communities that the map
does not yet show. The Ecumenical Patriarchate, Antiochian, and ROCOR
contributions are supported by their own current official directories and
records. Overlapping canonical jurisdictions remain separate parent branches.

    python tools/directory_philippines.py --check
    python tools/directory_philippines.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

MP_MAP = "https://exarchate.asia/en/karta-prihodov/"
MP_CLERGY = "https://phvieparchy.org/en/priesthood/"
MP_DIOCESE = "https://phvieparchy.org/en/eparchy/"

SINILOAN = "https://phvieparchy.org/en/parish-news/krestovozdvizhenie-3/"
POLOMOLOK = "https://phvieparchy.org/en/parish-news/prestolnyj-prazdnik-v-polomoloke-2/"
LAWIGUE = "https://phvieparchy.org/en/parish-news/liturgiya-v-lavige-tajabas/"
MANUKAN = "https://phvieparchy.org/en/parish-news/liturgiya-v-zamboange-2/"
LAKE_SEBU = "https://phvieparchy.org/en/parish-news/den-svyatogo-georgiya/"
PANGLAO = "https://phvieparchy.org/en/parish-news/liturgiya-na-o-panglao/"
PANGASINAN = "https://phvieparchy.org/en/parish-news/liturgiya-v-pangasinane-2/"
CAMARINES = "https://phvieparchy.org/en/parish-news/liturgiya-v-severnom-kamarines/"
CEBU = "https://phvieparchy.org/en/parish-news/liturgiya-v-sebu-3/"
BALILAY = "https://phvieparchy.org/en/parish-news/prestolnyj-prazdnik-v-alabele/"

EP_ROSTER = "https://ec-patr.org/entities/iera-mitropoli-xongk-kongk/"
EP_CLERGY = "https://omhksea.org/metropolis-of-hong-kong/clergy"
EP_HOLY_TRINITY = "https://omhksea.org/archives/14107"
ANTIOCH_MISSION = (
    "https://www.antiochian.org.au/2024/01/"
    "nativity-2023-at-the-nativity-of-the-theotokos-sta-maria-bulacan/"
)
ANTIOCH_ROSTER = (
    "https://antiochpatriarchate.org/en/category/"
    "%D8%A3%D8%B3%D8%AA%D8%B1%D8%A7%D9%84%D9%8A%D8%A7-"
    "%D9%86%D9%8A%D9%88%D8%B2%D9%8A%D9%84%D9%86%D8%AF%D8%A7-"
    "%D9%88%D8%A7%D9%84%D9%81%D9%8A%D9%84%D8%A8-%D9%8A%D9%86/66/"
)
ROCOR_DIRECTORY = (
    "https://directory.synod.com/listing/611/"
    "orthodox-community-of-st-nikolai/"
)

PARENT = "ru-philippines-and-vietnam"
EP_PARENT = "ep-hongkong"
ANTIOCH_PARENT = "an-australia"
ROCOR_PARENT = "ru-australia-and-new-zealand-rocor"
ROWS = []


def add(slug, name, local, dedication=None, rank="Parish", address=None,
        sources=None):
    row = {
        "id": "ph-" + slug,
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "PH",
        "sources": list(sources or [MP_MAP]),
    }
    if dedication:
        row["dedication"] = dedication
    if address:
        row["address"] = list(address)
    ROWS.append(row)


def add_other(row_id, parent, name, local, kind="parish", rank="Parish",
              dedication=None, address=None, sources=None):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "PH",
        "sources": list(sources or []),
    }
    if dedication:
        row["dedication"] = dedication
    if address:
        row["address"] = list(address)
    ROWS.append(row)


add(
    "ru-balilay-saint-isidore",
    "Saint Isidore of Chios Parish in Balilay",
    "Saint Isidore of Chios Parish, Balilay",
    dedication="Saint Isidore of Chios",
    sources=[MP_MAP, MP_CLERGY, BALILAY],
)
add(
    "ru-magulo-prophet-elijah",
    "Prophet Elijah Parish in Magulo",
    "Приход святого Илии Пророка в Магуле",
    dedication="The Holy Prophet Elijah",
    address=["Malungon, Sarangani, Philippines"],
)
add(
    "ru-lambayong-saint-ignatius",
    "Saint Ignatius the God-Bearer Parish in Lambayong",
    "Приход святителя Игнатия Богоносца в Ламбайонге",
    dedication="Saint Ignatius the God-Bearer",
    address=["Lambayong, Sultan Kudarat, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-tampakan-saint-catherine",
    "Saint Catherine Parish in Tampakan",
    "Приход святой Екатерины в Тампакане",
    dedication="Saint Catherine",
)
add(
    "ru-alabel-isidore-rostov",
    "Blessed Isidore of Rostov Parish in Alabel",
    "Приход блаженного Исидора Ростовского",
    dedication="Blessed Isidore of Rostov",
    address=["Alabel, Sarangani, Philippines"],
    sources=[MP_MAP, MP_CLERGY, BALILAY],
)
add(
    "ru-maitum-passion-icon",
    "Passion Icon of the Mother of God Community in Maitum",
    "Приход Страстной иконы Богородицы в Маитуме",
    dedication="The Passion Icon of the Mother of God",
    rank="Community",
    address=["Maitum, Sarangani, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-kayupo-saint-nicholas",
    "Saint Nicholas the Wonderworker Parish in Kayupo",
    "Приход святителя Николая в Каюпу",
    dedication="Saint Nicholas the Wonderworker",
    address=["Kayupo, Kiamba, Sarangani, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-kiamba-saint-john-shanghai",
    "Saint John of Shanghai and San Francisco Community in Kiamba",
    "Приход святителя Иоанна Шанхайского в Киамбе",
    dedication="Saint John of Shanghai and San Francisco",
    rank="Community",
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-general-santos-resurrection",
    "Resurrection of Christ Parish in General Santos",
    "Приход Воскресения Господня в Генерал Сантосе",
    dedication="The Resurrection of Christ",
    address=["Villa Dona Consuelo, General Santos, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-surigao-saint-george",
    "Saint George the Victory-Bearer Parish in Surigao",
    "Приход великомученика Георгия Победоносца в Суригао, Минданао",
    dedication="Saint George the Victory-Bearer",
)
add(
    "ru-palo-saint-nicholas-serbia",
    "Saint Nicholas of Serbia Parish in Palo",
    "Приход святителя Николая Сербского в Пало, Лейте",
    dedication="Saint Nicholas of Serbia",
    address=["Palo, Leyte, Philippines"],
)
add(
    "ru-jp-laurel-saint-vincent",
    "Saint Vincent of Lerins Parish in J.P. Laurel",
    "Приход святого Викентия Лиринского в Дж.П.Лауреле",
    dedication="Saint Vincent of Lerins",
)
add(
    "ru-banate-dormition",
    "Dormition of the Most Holy Theotokos Parish in Banate",
    "Приход Успения Богородицы в Банате",
    dedication="The Dormition of the Most Holy Theotokos",
    address=["Banate, Sarangani, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-kinabalan-saint-thomas",
    "Holy Apostle Thomas Parish in Kinabalan",
    "Приход святого апостола Фомы в Кинабалане",
    dedication="The Holy Apostle Thomas",
    address=["Kinabalan, Santa Maria, Davao Occidental, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-kiblawan-archangel-michael",
    "Archangel Michael Parish in Kiblawan",
    "Приход архангела Михаила в Киблаване",
    dedication="The Archangel Michael",
    address=["Kiblawan, Santa Maria, Davao Occidental, Philippines"],
)
add(
    "ru-talas-theophany",
    "Holy Theophany Parish in Talas",
    "Приход Богоявления в Таласе",
    dedication="The Holy Theophany of the Lord",
    address=["Talas, Santa Maria, Davao Occidental, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-mamakao-nativity-theotokos",
    "Nativity of the Most Holy Theotokos Parish in Mamakao",
    "Приход Рождества Богородицы в Санта Мария - Мамакао",
    dedication="The Nativity of the Most Holy Theotokos",
    address=["Mamakao, Santa Maria, Davao Occidental, Philippines"],
)
add(
    "ru-kapehan-saint-john-shanghai",
    "Saint John of Shanghai and San Francisco Parish in Santa Maria",
    "Приход святителя Иоанна Шанхайского в Санта Мария - Капехан",
    dedication="Saint John of Shanghai and San Francisco",
    address=["Sitio Jassie, Kapehan, Santa Maria, Davao Occidental 8011, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-santo-nino-saint-luke",
    "Holy Apostle Luke Community in Santo Nino",
    "Приход святого Луки в Санто Ниньо",
    dedication="The Holy Apostle and Evangelist Luke",
    rank="Community",
    address=["Santo Nino, Arakan, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-malibatuan-saint-anna",
    "Saint Anna, Ancestor of God Parish in Malibatuan",
    "Приход святой Анны в Малибатуане",
    dedication="Saint Anna, Ancestor of God",
    address=["Malibatuan, Arakan, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-little-baguio-saint-helena",
    "Saint Helena Equal-to-the-Apostles Parish in Little Baguio",
    "Приход святой равноапостольной Елены в Литтл Багио",
    dedication="Saint Helena Equal-to-the-Apostles",
    address=["Little Baguio, Arakan, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-mahongkog-archangel-michael",
    "Saint Michael the Archangel Parish in Mahongkog",
    "Приход архангела Михаила в Махонгоке",
    dedication="The Archangel Michael",
    address=["Mahongkog, Magpet, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-makalangot-saint-seraphim",
    "Saint Seraphim of Sarov Parish in Makalangot",
    "Приход преподобного Серафима Саровского в Макаланготе",
    dedication="Saint Seraphim of Sarov",
    address=["Makalangot, Arakan, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-salasang-peter-paul",
    "Holy Apostles Peter and Paul Parish in Salasang",
    "Приход святых апостолов Петра и Павла в Саласане",
    dedication="The Holy Apostles Peter and Paul",
    address=["Salasang, Arakan, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-arakan-nativity-theotokos",
    "Nativity of the Most Holy Theotokos Parish in Arakan",
    "Приход Рождества Богородицы в Аракане",
    dedication="The Nativity of the Most Holy Theotokos",
    address=["Arakan, North Cotabato, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-davao-saint-matrona",
    "Blessed Matrona of Moscow Parish and Missionary Center in Davao",
    "Приход Блаженной Матроны Московской в Давао",
    dedication="Blessed Matrona of Moscow",
    rank="Missionary Center",
    address=["8 Voyager Street, Davao City 8000, Philippines"],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-tagaytay-christ-savior",
    "Christ the Savior Parish in Tagaytay",
    "Храм Христа Спасителя в Тагайтайе",
    dedication="The Nativity of Christ",
    address=[
        "Barangay Patutong Malaki South",
        "Mendez-Tagaytay Road, Tagaytay City 4120, Philippines",
    ],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-manila-iveron",
    "Iveron Icon of the Mother of God Parish in Manila",
    "Приход Иверской иконы Богородицы в Маниле",
    dedication="The Iveron Icon of the Mother of God",
    address=[
        "35 Guam, Better Living Subdivision",
        "Barangay Don Bosco, Paranaque, Metro Manila 1711, Philippines",
    ],
    sources=[MP_MAP, MP_CLERGY],
)
add(
    "ru-cebu-holy-spirit",
    "Holy Spirit Parish in Cebu City",
    "Parish of the Holy Spirit in Cebu City",
    dedication="The Holy Spirit",
    sources=[MP_MAP, CEBU],
)
add(
    "ru-boracay-holy-trinity",
    "Holy Trinity Parish on Boracay",
    "Приход Святой Троицы на о.Боракай",
    dedication="The Holy Trinity",
)

# Current diocesan bodies which the exarchal map does not yet display.
add(
    "ru-siniloan-exaltation-cross",
    "Exaltation of the Holy Cross Parish in Siniloan",
    "Holy Cross Parish, Siniloan",
    dedication="The Exaltation of the Holy and Life-Giving Cross",
    address=["Siniloan, Laguna, Philippines"],
    sources=[MP_CLERGY, SINILOAN],
)
add(
    "ru-polomolok-protection",
    "Protection of the Most Holy Theotokos Parish in Polomolok",
    "Protection of the Most Holy Theotokos Parish, Polomolok",
    dedication="The Protection of the Most Holy Theotokos",
    address=["Polomolok, South Cotabato, Philippines"],
    sources=[MP_CLERGY, POLOMOLOK],
)
add(
    "ru-lawigue-saint-seraphim",
    "Saint Seraphim of Sarov Mission in Lawigue",
    "Mission of St. Seraphim of Sarov in Lawigue",
    dedication="Saint Seraphim of Sarov",
    rank="Mission",
    address=["Lawigue, Tayabas, Quezon, Philippines"],
    sources=[MP_CLERGY, LAWIGUE],
)
add(
    "ru-manukan-saint-nicholas",
    "Saint Nicholas the Wonderworker Parish in Manukan",
    "Saint Nicholas the Wonderworker Parish, Manukan",
    dedication="Saint Nicholas the Wonderworker",
    address=["Disakan, Manukan, Zamboanga del Norte, Philippines"],
    sources=[MP_CLERGY, MANUKAN],
)
add(
    "ru-lake-sebu-saint-george",
    "Saint George the Victory-Bearer Parish in Lake Sebu",
    "Saint George the Victorious Parish, Lake Sebu",
    dedication="Saint George the Victory-Bearer",
    address=["Lake Sebu, South Cotabato, Philippines"],
    sources=[MP_CLERGY, LAKE_SEBU],
)
add(
    "ru-panglao-quick-to-hear",
    "Quick to Hear Icon of the Mother of God Parish on Panglao",
    "Church of the Icon of the Mother of God Quick to Hear in Panglao",
    dedication="The Quick to Hear Icon of the Mother of God",
    address=["Panglao, Bohol, Philippines"],
    sources=[PANGLAO],
)
add(
    "ru-pangasinan-community",
    "Orthodox Community in Pangasinan",
    "Orthodox community in Pangasinan",
    rank="Community",
    address=["Pangasinan, Philippines"],
    sources=[PANGASINAN],
)
add(
    "ru-daet-camarines-norte-mission",
    "Orthodox Mission in Daet, Camarines Norte",
    "Orthodox community in Camarines Norte",
    rank="Mission",
    address=["Daet, Camarines Norte, Philippines"],
    sources=[CAMARINES],
)

# Ecumenical Patriarchate bodies named by the central Patriarchate roster and
# reconciled against the current Metropolis clergy roster.
add_other(
    "ph-ep-paranaque-annunciation-cathedral",
    EP_PARENT,
    "Cathedral of the Annunciation of the Theotokos in Paranaque",
    "Καθεδρικός Ναός Εὐαγγελισμοῦ Θεοτόκου",
    rank="Cathedral Parish",
    dedication="The Annunciation of the Theotokos",
    address=[
        "36 Filipinas Avenue",
        "United Paranaque Subdivision 5, Sucat",
        "Paranaque City, Metro Manila 1703, Philippines",
    ],
    sources=[EP_ROSTER, EP_CLERGY],
)
add_other(
    "ph-ep-los-banos-holy-trinity",
    EP_PARENT,
    "Holy Trinity Orthodox Church in Los Banos",
    "Ἱερός Ναός Ἁγίας Τριάδος",
    dedication="The Holy Trinity",
    address=[
        "Sitio Sampaguita, San Antonio",
        "Los Banos, Laguna, Philippines",
    ],
    sources=[EP_ROSTER, EP_CLERGY, EP_HOLY_TRINITY],
)
add_other(
    "ph-ep-cataingan-nativity-theotokos",
    EP_PARENT,
    "Church of the Nativity of the Theotokos in Cataingan",
    "Ἱερός Ναός Γενεσίου τῆς Θεοτόκου",
    dedication="The Nativity of the Theotokos",
    address=["Bajada, Cataingan 5405, Masbate, Philippines"],
    sources=[EP_ROSTER, EP_CLERGY],
)
add_other(
    "ph-ep-sorala-resurrection",
    EP_PARENT,
    "Chapel of the Resurrection of the Lord in Sorala",
    "Παρεκκλήσιον Ἀναστάσεως Κυρίου",
    rank="Chapel",
    dedication="The Resurrection of the Lord",
    address=["Sorala, South Cotabato, Mindanao, Philippines"],
    sources=[EP_ROSTER, EP_CLERGY],
)
add_other(
    "ph-ep-gubat-saint-eleftherios",
    EP_PARENT,
    "Chapel of Saint Eleftherios in Gubat",
    "Παρεκκλήσιον Ἁγίου Ἐλευθερίου",
    rank="Chapel",
    dedication="Hieromartyr Eleftherios",
    address=["Gubat, Sorsogon City, Sorsogon, Bicol, Philippines"],
    sources=[EP_ROSTER, EP_CLERGY],
)
add_other(
    "ph-ep-cataingan-nativity-monastery",
    EP_PARENT,
    "Monastery of the Nativity of the Theotokos in Cataingan",
    "Ἱερά Μονή Γενεσίου Θεοτόκου",
    kind="monastery",
    rank="Monastery",
    dedication="The Nativity of the Theotokos",
    address=["Bajada, Cataingan 5405, Masbate, Philippines"],
    sources=[EP_ROSTER, EP_CLERGY],
)

# Other current official canonical rosters.
add_other(
    "ph-antioch-santa-maria-nativity-theotokos",
    ANTIOCH_PARENT,
    "Nativity of the Theotokos Mission in Santa Maria",
    "Mission of the Nativity of the Theotokos, Sta. Maria Bulacan",
    rank="Mission",
    dedication="The Nativity of the Theotokos",
    address=["Santa Maria, Bulacan, Philippines"],
    sources=[ANTIOCH_MISSION, ANTIOCH_ROSTER],
)
add_other(
    "ph-rocor-manila-saint-nikolai",
    ROCOR_PARENT,
    "Orthodox Community of Saint Nikolai",
    "Orthodox Community of Saint Nikolai",
    rank="Community",
    dedication="Saint Nikolai",
    address=["Manila, Philippines"],
    sources=[ROCOR_DIRECTORY],
)


ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {}
EXPECTED = {
    PARENT: 38,
    EP_PARENT: 6,
    ANTIOCH_PARENT: 1,
    ROCOR_PARENT: 1,
}
EXPECTED_RANKS = {
    "Parish", "Cathedral Parish", "Chapel", "Community", "Mission",
    "Missionary Center", "Monastery",
}
FORBIDDEN_FIELDS = {
    "contact", "contacts", "email", "phone", "telephone", "clergy",
    "priest", "rector", "abbot", "abbess",
}
FORBIDDEN_PUNCTUATION = (
    "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d", "\ufffd",
)


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if len(sources) != len(set(sources)):
        raise ValueError("%s repeats a source" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in FORBIDDEN_PUNCTUATION):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    return row


def semantic_key(value):
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def build():
    rows = {parent: [] for parent in EXPECTED}
    seen_ids = set()
    seen_names = {}
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen_ids:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") not in EXPECTED or row.get("country") != "PH":
            raise ValueError("%s is grouped outside the Philippines" % row_id)
        if (row.get("kind") not in {"parish", "monastery"}
                or row.get("rank") not in EXPECTED_RANKS):
            raise ValueError("%s has an unsupported kind or rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable official identity" % row_id)
        if FORBIDDEN_FIELDS.intersection(row):
            raise ValueError("%s carries contact or personnel prose" % row_id)
        for key in ("address", "sources", "cite"):
            if row.get(key) and (not isinstance(row[key], list) or
                                 not all(isinstance(value, str)
                                         for value in row[key])):
                raise ValueError("%s has invalid %s" % (row_id, key))
        name_key = semantic_key(row["name"])
        if name_key in seen_names:
            raise ValueError("semantic duplicate: %s and %s" %
                             (seen_names[name_key], row_id))
        seen_names[name_key] = row_id
        seen_ids.add(row_id)
        rows[row["parent"]].append(row)
    for parent, expected in EXPECTED.items():
        if len(rows[parent]) != expected:
            raise ValueError(
                "Philippines must publish exactly %d rows under %s" %
                (expected, parent))
    if set(ENGLISH_NAMES) != seen_ids:
        raise ValueError("Philippines English name map is out of sync")
    return {
        parent: {
            "v": 1,
            "parent": parent,
            "country": "PH",
            "rows": parent_rows,
        }
        for parent, parent_rows in rows.items()
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Philippines: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Philippines: 46 current bodies across 4 canonical branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
