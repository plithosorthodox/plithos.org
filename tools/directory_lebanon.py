#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Lebanon.

The current first-party records of the Patriarchate of Antioch and the
Moscow Patriarchate establish the bodies below. The six existing Antiochian
archdiocesan rows in Lebanon are not duplicated here.

    python tools/directory_lebanon.py --check
    python tools/directory_lebanon.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "lebanon.json"
CHECKED = "2026-11-15"

ZAHLE_ROSTER = "https://archzahle.com/archdiocese/parishes/"
ZAHLE_CATHEDRAL = (
    "https://archzahle.com/%D8%B5%D9%84%D8%A7%D8%A9-%D8%A7%D9%84%D8%BA%D8%B1"
    "%D9%88%D8%A8-%D9%81%D9%8A-%D9%83%D8%A7%D8%AA%D8%AF%D8%B1%D8%A7%D8%A6%D9%8A"
    "%D8%A9-%D8%A7%D9%84%D9%82%D8%AF%D9%91%D9%8A%D8%B3-%D9%86%D9%8A%D9%82%D9%88-3/"
)
TRIPOLI_MONASTERIES = "https://archtripoli.org/Archdiocese/Monasteries"
TRIPOLI_PARISHES = "https://archtripoli.org/Archdiocese/Parish"
ANTIOCH_DIRECTORY_POST = "https://antiochpatriarchate.org/wp-json/wp/v2/posts/5342"
ANTIOCH_DIRECTORY = (
    "https://antiochpatriarchate.org/wp-content/uploads/2026/10/Dalil-2025.pdf"
)
BALAMAND = (
    "https://antiochpatriarchate.org/institutions/monasteries/"
    "%d8%af%d9%8a%d8%b1-%d8%b3%d9%8a%d9%91%d8%af%d8%a9-%d8%a7%d9%84%d8%a8"
    "%d9%84%d9%85%d9%86%d8%af-%d8%a7%d9%84%d8%a8%d8%b7%d8%b1%d9%8a%d8%b1"
    "%d9%83%d9%8a%d9%91/"
)
RUSSIA_METOCHION = "https://mospat.ru/en/news/94698/"
RUSSIA_METOCHION_CURRENT = (
    "https://patriarchia.ru/en/article/123715?path=%2Fnews%2Fsynod-orgs"
)
RUSSIA_ANNUNCIATION = "https://mospat.ru/en/news/94701/"
RUSSIA_MOUNT_LEBANON = "https://mospat.ru/en/news/94696/"
TRIPOLI_SAINT_JAMES = (
    "https://archtripoli.org/Archdiocese/Monasteries/Yaacoub-Deddeh"
)


def body(row_id, parent, name, local, seat, rank, sources,
         kind="parish", address=None):
    return {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "LB",
        "address": address,
        "sources": sources,
    }


def beirut_body(number, slug, name, local, seat="Beirut", rank="Church",
                 kind="parish"):
    return body(
        "lb-an-beirut-%s" % slug,
        "an-beirut",
        name,
        local,
        seat,
        rank,
        ["https://quartos.org.lb/Churches/%d" % number],
        kind=kind,
    )


BEIRUT_ROWS = [
    beirut_body(
        1, "saint-george-cathedral", "Saint George Cathedral",
        "كاتدرائيّة القدّيس جاورجيوس", rank="Cathedral",
    ),
    beirut_body(
        2, "entrance-theotokos-monastery",
        "Church of the Holy Monastery of the Presentation of the Theotokos",
        "كنيسة دير دخول السيدة إلى الهيكل، الأشرفيّة",
        rank="Monastery", kind="monastery",
    ),
    beirut_body(
        3, "annunciation-theotokos",
        "Church of the Annunciation of the Theotokos",
        "كنيسة بشارة السّيّدة، الأشرفية",
    ),
    beirut_body(
        4, "dormition-theotokos",
        "Church of the Dormition of the Theotokos",
        "كنيسة نياح السّيّدة، رأس بيروت",
    ),
    beirut_body(
        5, "archangels-michael-gabriel",
        "Church of the Archangels Michael and Gabriel",
        "كنيسة رئيسَيّ الملائكة ميخائيل وجبرائيل، المزرعة",
    ),
    beirut_body(
        6, "prophet-elias-btina-monastery",
        "Church of the Monastery of the Prophet Elias-Btina",
        "كنيسة دير النّبيّ إيلياس-بطينا",
        rank="Monastery", kind="monastery",
    ),
    beirut_body(
        7, "prophet-elias-msaytbeh",
        "Church of the Prophet Elias-Msaytbeh",
        "كنيسة النبيّ إيلياس، المصيطبة",
    ),
    beirut_body(
        8, "saint-nicholas-ashrafieh",
        "Church of Saint Nicholas-Ashrafieh",
        "كنيسة القدّيس نيقولاوس، الأشرفيّة",
    ),
    beirut_body(
        9, "saint-george-souk-el-ghareb-monastery",
        "The Church of the Saint George Monastery-Souk El Ghareb",
        "كنيسة دير القدّيس جاورجيوس، سوق الغرب",
        seat="Souk El Ghareb", rank="Monastery", kind="monastery",
    ),
    beirut_body(
        10, "saint-george-rmeil",
        "Church of Saint George-Rmeil",
        "كنيسة القدّيس جاورجيوس، الرّميل",
    ),
    beirut_body(
        11, "saint-dimitrios-ashrafieh",
        "Church of Saint Dimitrios-Ashrafieh",
        "كنيسة القدّيس ديمتريوس، الأشرفيّة",
    ),
    beirut_body(
        12, "saint-catherine-monastery",
        "Church of the Saint Catherine Monastery",
        "كنيسة دير القدّيسة كاترينا، الأشرفيّة",
        rank="Monastery", kind="monastery",
    ),
    beirut_body(
        14, "saint-john-baptist",
        "Church of Saint John the Baptist",
        "كنيسة القدّيس يوحنّا المعمدان",
    ),
    beirut_body(
        15, "saint-catherine-annunciation-college",
        "Church of Saint Catherine at the Beirut Annunciation College",
        "كنيسة القدّيسة كاترينا في مدرسة البشارة الأرثوذكسيّة",
    ),
    beirut_body(
        16, "saint-george-university-medical-center",
        "Saint George Church at Saint George University Medical Center",
        "كنيسة القدّيس جاورجيوس في مستشفى القدّيس جاورجيوس الجامعيّ",
    ),
    beirut_body(
        17, "saints-anthony-porphyrios",
        "Church of Saints Anthony the Great and Porphyrios",
        "كنيسة البارَّين أنطونيوس الكبير وبورفيريوس الرّائي",
    ),
]


def zahle_body(slug, name, local, seat, rank="Church", sources=None):
    return body(
        "lb-an-zahleh-%s" % slug,
        "an-zahleh",
        name,
        local,
        seat,
        rank,
        sources or [ZAHLE_ROSTER],
    )


ZAHLE_ROWS = [
    zahle_body(
        "saint-nicholas-midan", "Saint Nicholas Cathedral in Midan",
        "القديس نيقولاوس- الميدان", "Zahleh", rank="Cathedral",
        sources=[ZAHLE_ROSTER, ZAHLE_CATHEDRAL],
    ),
    zahle_body(
        "saint-nicholas-gardenia", "Church of Saint Nicholas at Gardenia",
        "القديس نيقولاوس- معمل غاردينيا", "Zahleh",
    ),
    zahle_body(
        "saint-george-deir-el-ghazal",
        "Church of Saint George in Deir El Ghazal",
        "القديس جاورجيوس - دير الغزال", "Deir El Ghazal",
    ),
    zahle_body(
        "saint-andrew-rayak", "Church of Saint Andrew in Rayak",
        "القديس أندراوس- رياق", "Rayak",
    ),
    zahle_body(
        "saint-george-housh-el-omara",
        "Church of Saint George in Housh El Omara",
        "القديس جاورجيوس - حوش الأمراء", "Housh El Omara",
    ),
    zahle_body(
        "nativity-theotokos-qabb-elias",
        "Church of the Nativity of the Theotokos in Qabb Elias",
        "ميلاد السيدة - قب الياس", "Qabb Elias",
    ),
    zahle_body(
        "annunciation-theotokos-chlifa",
        "Church of the Annunciation of the Theotokos in Chlifa",
        "سيدة البشارة- شليفا", "Chlifa",
    ),
    zahle_body(
        "dormition-theotokos-hadath-baalbek",
        "Church of the Dormition of the Theotokos in Hadath Baalbek",
        "رقاد السيدة- حدث بعلبك", "Hadath Baalbek",
    ),
    zahle_body(
        "our-lady-earthquake-zahleh",
        "Church of Our Lady of the Earthquake in Zahleh",
        "سيدة الزلزلة- زحلة", "Zahleh",
    ),
    zahle_body(
        "saint-george-qaraoun", "Church of Saint George in Qaraoun",
        "القديس جاورجيوس - القرعون", "Qaraoun",
    ),
    zahle_body(
        "transfiguration-makseh", "Church of the Transfiguration in Makseh",
        "كنيسة التجلي- مكسه", "Makseh",
    ),
    zahle_body(
        "saint-anthony-maallaqa", "Church of Saint Anthony in Maallaqa",
        "القديس أنطونيوس - المعلقة", "Maallaqa",
    ),
    zahle_body(
        "archangel-michael-ablah", "Church of Archangel Michael in Ablah",
        "رئيس الملائكة ميخائيل- أبلح", "Ablah",
    ),
    zahle_body(
        "our-lady-beit-chama", "Church of Our Lady in Beit Chama",
        "كنيسة السيدة- بيت شاما", "Beit Chama",
    ),
    zahle_body(
        "saint-george-qaa-el-rim", "Church of Saint George in Qaa El Rim",
        "القديس جاورجيوس- قاع الريم", "Qaa El Rim",
    ),
    zahle_body(
        "holy-cross-rayit", "Church of the Holy Cross in Rayit",
        "الصليب- رعيت", "Rayit",
    ),
    zahle_body(
        "saint-george-kafr-zabad",
        "Church of Saint George in Kafr Zabad",
        "القديس جاورجيوس- كفرزبد", "Kafr Zabad",
    ),
    zahle_body(
        "saint-george-talia", "Church of Saint George in Talia",
        "القديس جاورجيوس- طليا", "Talia",
    ),
    zahle_body(
        "prophet-elias-housh-barada",
        "Church of Prophet Elias in Housh Barada",
        "مار الياس- حوش بردى", "Housh Barada",
    ),
    zahle_body(
        "saint-john-baptist-taalabaya",
        "Church of Saint John the Baptist in Taalabaya",
        "النبي يوحنا المعمدان- تعلبايا", "Taalabaya",
    ),
    zahle_body(
        "saint-george-jdita", "Church of Saint George in Jdita",
        "القديس جاورجيوس- جديتا", "Jdita",
    ),
    zahle_body(
        "prophet-elias-niha", "Church of Prophet Elias in Niha",
        "النبي إيليا- نيحا", "Niha",
    ),
    zahle_body(
        "saint-nicholas-terbol", "Church of Saint Nicholas in Terbol",
        "القديس نيقولاوس- تربل", "Terbol",
    ),
    zahle_body(
        "dormition-theotokos-qousaya",
        "Church of the Dormition of the Theotokos in Qousaya",
        "كنيسة رقاد السيدة- قوسايا", "Qousaya",
    ),
    zahle_body(
        "saint-george-baalbek", "Church of Saint George in Baalbek",
        "القديس جاورجيوس- بعلبك", "Baalbek",
    ),
]


def tripoli_body(slug, name, local, seat, rank, kind, sources):
    return body(
        "lb-an-tripoli-%s" % slug,
        "an-tripoli",
        name,
        local,
        seat,
        rank,
        sources,
        kind=kind,
    )


TRIPOLI_ROWS = [
    tripoli_body(
        "saint-dimitrios-kousba-monastery",
        "Monastery of Saint Dimitrios in Kousba",
        "دير القديس ديمتريوس - كوسبا", "Kousba", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "fervent-intercessor-badba-monastery",
        "Monastery of Our Lady, the Fervent Intercessor, in Badba",
        "دير الشفيعة الحارة - بدبا", "Badba", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "saint-james-persian-deddeh-monastery",
        "Monastery of Saint James the Persian in Deddeh",
        "دير القديس يعقوب الفارسي المقطع - دده", "Deddeh", "Monastery",
        "monastery", [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "saint-john-baptist-bshamzin-monastery",
        "Monastery of Saint John the Baptist in Bshamzin",
        "دير القديس يوحنا المعمدان - بشمزين", "Bshamzin", "Monastery",
        "monastery", [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "prophet-elias-kfarqahel-monastery",
        "Monastery of Prophet Elias in Kfarqahel",
        "دير النبي ايليا - كفرقاهل", "Kfarqahel", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "our-lady-natour-monastery", "Monastery of Our Lady of Natour",
        "دير سيدة الناطور", "Anfeh", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "our-lady-bkiftine-monastery", "Monastery of Our Lady of Bkiftine",
        "دير سيدة بكفتين", "Bkiftine", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "saint-george-el-kfour-monastery",
        "Monastery of Saint George in El Kfour",
        "دير مار جرجس - الكفر", "El Kfour", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "saint-john-anfeh-monastery", "Monastery of Saint John in Anfeh",
        "دير مار يوحنا - أنفه", "Anfeh", "Monastery", "monastery",
        [TRIPOLI_MONASTERIES],
    ),
    tripoli_body(
        "our-lady-kousba-shrine", "Shrine of Our Lady in Kousba",
        "مزار السيدة", "Kousba", "Shrine", "parish", [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "prophet-elias-kousba-shrine", "Shrine of Prophet Elias in Kousba",
        "مزار النبي الياس", "Kousba", "Shrine", "parish", [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "martyr-barbara-kousba-shrine", "Shrine of Martyr Barbara in Kousba",
        "مزار الشهيدة بربارة", "Kousba", "Shrine", "parish",
        [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "martyr-george-kousba-shrine", "Shrine of Martyr George in Kousba",
        "مزار الشهيد جاورجيوس", "Kousba", "Shrine", "parish",
        [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "righteous-joseph-kousba-shrine",
        "Shrine of Righteous Joseph the Betrothed in Kousba",
        "مزار البارّ يوسف الخطيب", "Kousba", "Shrine", "parish",
        [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "saint-marina-amyoun-shrine", "Shrine of Saint Marina in Amyoun",
        "مزار القديسة مارينا", "Amyoun", "Shrine", "parish",
        [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "saints-cyprian-justina-basarma-shrine",
        "Shrine of Saints Cyprian and Justina in Basarma",
        "مزار القديسين كبريانوس ويوستينا", "Basarma", "Shrine", "parish",
        [TRIPOLI_PARISHES],
    ),
    tripoli_body(
        "saint-george-cave-el-mina-shrine",
        "Cave Shrine of Saint George in El Mina",
        "مزار مغارة مار جرجس", "El Mina", "Shrine", "parish",
        [TRIPOLI_PARISHES],
    ),
]


DIRECT_ANTIOCH_ROWS = [
    body(
        "lb-an-balamand-patriarchal-monastery",
        "antioch",
        "Our Lady of Balamand Patriarchal Monastery",
        "دير سيّدة البلمند البطريركيّ",
        "Balamand",
        "Patriarchal Monastery",
        [BALAMAND, ANTIOCH_DIRECTORY],
        kind="monastery",
        address=[
            "Our Lady of Balamand Patriarchal Monastery",
            "P.O. Box 100 Tripoli, Lebanon",
        ],
    ),
    body(
        "lb-an-saint-elias-shwayya-patriarchal-monastery",
        "antioch",
        "Saint Elias Shwayya Patriarchal Monastery",
        "دير مار إلياس شويّا البطريركيّ",
        "Shwayya",
        "Patriarchal Monastery",
        [ANTIOCH_DIRECTORY_POST, ANTIOCH_DIRECTORY],
        kind="monastery",
        address=[
            "Saint Elias Shwayya Patriarchal Monastery",
            "Northern Matn, Lebanon",
        ],
    ),
    body(
        "lb-an-our-lady-younes-shrine",
        "lb-an-balamand-patriarchal-monastery",
        "Shrine of Our Lady of Younes in Old Tripoli",
        "مزار سيدة يونس",
        "Tripoli",
        "Shrine",
        [TRIPOLI_PARISHES],
    ),
]

DIRECT_RUSSIA_ROWS = [
    body(
        "lb-ru-bsalim-metochion",
        "russia",
        "Russian Orthodox Church Metochion in Bsalim",
        "Подворье Русской Православной Церкви в Бсалиме",
        "Bsalim",
        "Metochion",
        [RUSSIA_METOCHION, RUSSIA_METOCHION_CURRENT],
    ),
    body(
        "lb-ru-jal-el-dib-annunciation",
        "lb-ru-bsalim-metochion",
        "Church of the Annunciation of the Most Holy Theotokos in Jal El Dib",
        "храм Благовещения Пресвятой Богородицы в Жаль Эль Диб",
        "Jal El Dib",
        "Church",
        [RUSSIA_ANNUNCIATION, RUSSIA_MOUNT_LEBANON],
    ),
]

ROWS = {
    "an-beirut": BEIRUT_ROWS,
    "an-zahleh": ZAHLE_ROWS,
    "an-tripoli": TRIPOLI_ROWS,
}
EXPECTED = {"an-beirut": 16, "an-zahleh": 25, "an-tripoli": 17}
EXPECTED_TOTAL = 63
ALLOWED_KINDS = {"parish", "monastery"}
ALLOWED_RANKS = {
    "Church", "Cathedral", "Monastery", "Shrine",
    "Patriarchal Monastery", "Metochion",
}
ALL_SOURCE_ROWS = (
    BEIRUT_ROWS + ZAHLE_ROWS + TRIPOLI_ROWS +
    DIRECT_ANTIOCH_ROWS + DIRECT_RUSSIA_ROWS
)
ENGLISH_NAMES = {item["id"]: item["name"] for item in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ALL_SOURCE_ROWS}

# Every contact below is the body's public institutional contact as printed by
# a current first-party Church source. Empty values are deliberate.
CONTACTS = {
    item["id"]: {
        "emails": [],
        "phones": [],
        "contact_sources": [],
    }
    for item in ALL_SOURCE_ROWS
}

_CONTACT_UPDATES = {
    "lb-an-beirut-saint-george-cathedral": {"phones": ["01 980 920"]},
    "lb-an-beirut-annunciation-theotokos": {"phones": ["01 339 426"]},
    "lb-an-beirut-dormition-theotokos": {
        "phones": ["01 340 347", "01 341 881"],
    },
    "lb-an-beirut-archangels-michael-gabriel": {
        "phones": ["01 657 857", "01 657 756"],
    },
    "lb-an-beirut-prophet-elias-btina-monastery": {
        "phones": ["01 301 680", "01 701 953"],
    },
    "lb-an-beirut-prophet-elias-msaytbeh": {"phones": ["01 315 662"]},
    "lb-an-beirut-saint-nicholas-ashrafieh": {
        "phones": ["01 216 053", "01 203 308", "01 203 309"],
    },
    "lb-an-beirut-saint-george-souk-el-ghareb-monastery": {
        "phones": ["05 270 135", "05 270 030"],
    },
    "lb-an-beirut-saint-george-rmeil": {"phones": ["01 584 953"]},
    "lb-an-beirut-saint-dimitrios-ashrafieh": {
        "phones": ["01 216 885", "01 334 086"],
    },
    "lb-an-beirut-saint-catherine-monastery": {"phones": ["01 200 239"]},
    "lb-an-beirut-saint-george-university-medical-center": {
        "phones": ["ext: 1287"],
    },
    "lb-an-zahleh-saint-nicholas-midan": {
        "phones": ["08/820527", "08/818630", "03/009609", "03/379808"],
    },
    "lb-an-zahleh-saint-nicholas-gardenia": {
        "phones": ["08/820527", "03/009609"],
    },
    "lb-an-zahleh-saint-george-deir-el-ghazal": {
        "phones": ["03/138265"],
    },
    "lb-an-zahleh-saint-andrew-rayak": {
        "phones": ["08/951127", "03/662892"],
    },
    "lb-an-zahleh-saint-george-housh-el-omara": {
        "phones": ["08/811695", "03/329627", "03/672273"],
    },
    "lb-an-zahleh-nativity-theotokos-qabb-elias": {
        "phones": ["08/501166", "81/310211"],
    },
    "lb-an-zahleh-annunciation-theotokos-chlifa": {
        "phones": ["08/300082", "71/676416"],
    },
    "lb-an-zahleh-dormition-theotokos-hadath-baalbek": {
        "phones": ["08/300082", "71/676416"],
    },
    "lb-an-zahleh-our-lady-earthquake-zahleh": {
        "phones": ["08/817868", "03/321248"],
    },
    "lb-an-zahleh-saint-george-qaraoun": {
        "phones": ["08/801232", "76/827982"],
    },
    "lb-an-zahleh-transfiguration-makseh": {
        "phones": ["08/801232", "76/827982"],
    },
    "lb-an-zahleh-saint-anthony-maallaqa": {
        "phones": ["08/800890", "03/239871"],
    },
    "lb-an-zahleh-archangel-michael-ablah": {
        "phones": ["08/950776", "03/226286"],
    },
    "lb-an-zahleh-our-lady-beit-chama": {
        "phones": ["08/950776", "03/226286"],
    },
    "lb-an-zahleh-saint-george-qaa-el-rim": {
        "phones": ["80/800130", "70/528920"],
    },
    "lb-an-zahleh-holy-cross-rayit": {
        "phones": ["08/800130", "70/528920"],
    },
    "lb-an-zahleh-saint-george-kafr-zabad": {
        "phones": ["08/807932", "70/777173"],
    },
    "lb-an-zahleh-saint-george-talia": {
        "phones": ["08/829599", "03/581847"],
    },
    "lb-an-zahleh-prophet-elias-housh-barada": {
        "phones": ["08/829599", "03/581847"],
    },
    "lb-an-zahleh-saint-john-baptist-taalabaya": {
        "phones": ["08/925533", "03/940157"],
    },
    "lb-an-zahleh-saint-george-jdita": {
        "phones": ["08/925533", "03/940157"],
    },
    "lb-an-zahleh-prophet-elias-niha": {"phones": ["70/865170"]},
    "lb-an-zahleh-saint-nicholas-terbol": {"phones": ["70/865170"]},
    "lb-an-zahleh-dormition-theotokos-qousaya": {
        "phones": ["03/688257"],
    },
    "lb-an-zahleh-saint-george-baalbek": {"phones": ["71/964720"]},
    "lb-an-tripoli-saint-james-persian-deddeh-monastery": {
        "phones": ["405176/ 06"],
    },
    "lb-an-balamand-patriarchal-monastery": {
        "phones": ["00961 6 930311", "00961 76 880886"],
        "emails": ["monastery.balamand@gmail.com"],
    },
    "lb-an-saint-elias-shwayya-patriarchal-monastery": {
        "phones": ["00961 4 390046", "00961 3 349337"],
        "emails": ["costakayal.ck@gmail.com"],
    },
}
for _contact_id, _contact_values in _CONTACT_UPDATES.items():
    CONTACTS[_contact_id].update(_contact_values)

_ROW_BY_ID = {item["id"]: item for item in ALL_SOURCE_ROWS}
for _contact_id, _contact in CONTACTS.items():
    if not (_contact["emails"] or _contact["phones"]):
        continue
    if _contact_id.startswith("lb-an-beirut-"):
        _contact["contact_sources"] = list(_ROW_BY_ID[_contact_id]["sources"][:1])
    elif _contact_id.startswith("lb-an-zahleh-"):
        _contact["contact_sources"] = [ZAHLE_ROSTER]
    elif _contact_id == "lb-an-tripoli-saint-james-persian-deddeh-monastery":
        _contact["contact_sources"] = [TRIPOLI_SAINT_JAMES]
    elif _contact_id == "lb-an-balamand-patriarchal-monastery":
        _contact["contact_sources"] = [BALAMAND, ANTIOCH_DIRECTORY]
    elif _contact_id == "lb-an-saint-elias-shwayya-patriarchal-monastery":
        _contact["contact_sources"] = [ANTIOCH_DIRECTORY]
    else:
        raise ValueError("missing contact source for %s" % _contact_id)
    _ROW_BY_ID[_contact_id].update({
        "emails": list(_contact["emails"]),
        "phones": list(_contact["phones"]),
        "contact_sources": list(_contact["contact_sources"]),
        "contact_checked": CHECKED,
    })


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
    if item.get("country") != "LB":
        raise ValueError("%s is outside Lebanon" % row_id)
    if item.get("kind") not in ALLOWED_KINDS:
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if not item.get("name") or not item.get("local"):
        raise ValueError("%s lacks a usable local or English name" % row_id)
    name_key = item["name"].casefold()
    if name_key in names:
        raise ValueError("duplicate reader-facing name: %s and %s" % (
            names[name_key], row_id,
        ))
    if item.get("address") and (
            not isinstance(item["address"], list) or
            not all(isinstance(line, str) for line in item["address"])):
        raise ValueError("%s has an invalid address" % row_id)
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
            "country": "LB",
            "rows": rows,
        }

    for root_parent, source_rows in (
            ("antioch", DIRECT_ANTIOCH_ROWS),
            ("russia", DIRECT_RUSSIA_ROWS)):
        branch_seen = {root_parent}
        for source in source_rows:
            item = clean(source)
            _validate_row(item, seen, branch_seen, names)

    row_ids = {item["id"] for item in ALL_SOURCE_ROWS}
    if set(ENGLISH_NAMES) != row_ids or len(row_ids) != EXPECTED_TOTAL:
        raise ValueError("Lebanon English name map is out of sync")
    if set(CONTACTS) != row_ids:
        raise ValueError("Lebanon contact map is out of sync")
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
           for value in CONTACTS.values()) != 40:
        raise ValueError("Lebanon contact-bearing row total is out of sync")
    if sum(len(value["emails"]) for value in CONTACTS.values()) != 2:
        raise ValueError("Lebanon email total is out of sync")
    if sum(len(value["phones"]) for value in CONTACTS.values()) != 72:
        raise ValueError("Lebanon phone total is out of sync")
    if sum(EXPECTED.values()) + len(DIRECT_ANTIOCH_ROWS) + \
            len(DIRECT_RUSSIA_ROWS) != EXPECTED_TOTAL:
        raise ValueError("Lebanon branch total must remain %d" % EXPECTED_TOTAL)
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "LB":
        raise ValueError("Lebanon candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Lebanon candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    expected_summary = {
        "an-beirut": 16,
        "an-zahleh": 25,
        "an-tripoli": 17,
        "antioch": 3,
        "russia": 2,
        "total": EXPECTED_TOTAL,
        "canonical_jurisdictions_represented": 2,
    }
    if summary != expected_summary:
        raise ValueError("Lebanon candidate ledger totals are out of sync")
    required_lists = (
        "candidates", "reconciliation", "exclusions",
        "official_jurisdiction_audit",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Lebanon candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "LB":
            raise ValueError("%s is outside Lebanon" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Lebanon candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Lebanon ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Lebanon ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("Lebanon candidate ledger has forbidden punctuation")
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
        print("directory Lebanon: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Lebanon: 63 current officially named bodies across "
            "2 canonical jurisdictions"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
