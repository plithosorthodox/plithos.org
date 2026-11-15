#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Israel.

The module reconciles the Jerusalem Patriarchate's current administrative
rosters with the current Moscow, ROCOR, and Romanian Holy Land directories.
It publishes separately named churches, monasteries, chapels, shrines, and
recurring language congregations, while recording duplicate and uncertain
discoveries in the country candidate ledger.

    python tools/directory_israel.py --check
    python tools/directory_israel.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "israel.json"

JP_JERUSALEM = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "holy-monasteries-and-churches-in-jerusalem/"
)
JP_OUTSIDE = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "holy-monasteries-and-hegoumeneia-abbots-quarters-outside-jerusalem/"
)
JP_METROPOLIS = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "holy-bishoprics/"
)
JP_EXTERNAL = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "russian-speaking-community-parishes/"
)
JP_COMMUNITIES = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "churches-in-the-west-bank/"
)
JP_SHRINES = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "all-holy-pilgrimage-sites/"
)
JP_COMMITTEES = (
    "https://en.jerusalem-patriarchate.info/administrative-structure/"
    "patriarchal-management-committees/"
)
ROCOR_CONTACTS = "https://missionrocor.ru/contacts"
MP_CHAPELS = "https://rusdm.ru/chapel/"
MP_CONTACT = "https://rusdm.ru/contact/"
MP_HISTORY = "https://rusdm.ru/history/392"
RO_EXTERNAL = (
    "https://patriarhia.ro/en/organization-of-the-romanian-orthodox-church/"
    "external-representations-and-communities/"
)
JP_ARABIC_2026 = (
    "https://ar.jerusalem-patriarchate.info/wp-content/uploads/2026/02/"
    "arabic_2026.pdf"
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
        "country": "IL",
        "sources": sources or [JP_JERUSALEM],
    }
    if local:
        row["local"] = local
    row.update(extra)
    if row.get("emails") or row.get("phones"):
        row.setdefault("contact_sources", list(row["sources"][:1]))
        row.setdefault("contact_checked", CHECKED)
    return row


JERUSALEM_ROWS = [
    body("il-je-central-constantine-helen", "jerusalem",
         "Central Monastery of Saints Constantine and Helen", "Jerusalem",
         "Monastery", "monastery"),
    body("il-je-little-galilee", "jerusalem",
         "Holy Monastery of Little Galilee on the Mount of Olives",
         "Jerusalem", "Monastery", "monastery",
         phones=["+972-545359387"]),
    body("il-je-little-galilee-men-of-galilee", "il-je-little-galilee",
         "Church of the Men of Galilee", "Jerusalem", "Church"),
    body("il-je-little-galilee-annunciation-dormition",
         "il-je-little-galilee",
         "Church of the Annunciation of the Dormition of the Theotokos",
         "Jerusalem", "Church"),
    body("il-je-saint-charalambos", "jerusalem",
         "Holy Monastery of Saint Charalambos", "Jerusalem", "Monastery",
         "monastery", phones=["+972-529395513"]),
    body("il-je-forerunner-old-city", "jerusalem",
         "Holy Monastery of the Forerunner", "Jerusalem", "Monastery",
         "monastery", phones=["+972-545670625"]),
    body("il-je-archangels-old-city", "jerusalem",
         "Holy Monastery of the Archangels", "Jerusalem", "Monastery",
         "monastery"),
    body("il-je-saint-nikolaos", "jerusalem",
         "Holy Monastery of Saint Nikolaos", "Jerusalem", "Monastery",
         "monastery", phones=["0546/6112486"]),
    body("il-je-saints-theodores", "jerusalem",
         "Holy Monastery of Saints Theodores", "Jerusalem", "Monastery",
         "monastery", phones=["0547/152770"]),
    body("il-je-saint-george-jewish-quarter", "jerusalem",
         "Holy Monastery of Saint George at the Jewish Quarter",
         "Jerusalem", "Monastery", "monastery",
         phones=["00972/547503198"]),
    body("il-je-saint-george-hospital", "jerusalem",
         "Holy Monastery of Saint George of the Hospital", "Jerusalem",
         "Monastery", "monastery", phones=["+972-2-6277176"]),
    body("il-je-saint-basil", "jerusalem",
         "Holy Monastery of Saint Basil", "Jerusalem", "Monastery",
         "monastery", phones=["0544/282390"]),
    body("il-je-saint-catherine", "jerusalem",
         "Holy Monastery of Saint Catherine", "Jerusalem", "Monastery",
         "monastery", phones=["+972-544-263240"],
         emails=["fr.stefanosjerusalem@gmail.com"]),
    body("il-je-saint-spyridon", "jerusalem",
         "Holy Monastery of Saint Spyridon", "Jerusalem", "Monastery",
         "monastery", phones=["0549/350350"]),
    body("il-je-saint-nicodemus", "jerusalem",
         "Holy Monastery of Saint Nicodemus", "Jerusalem", "Monastery",
         "monastery", phones=["02/6492378", "0543/509060"]),
    body("il-je-praetorium", "jerusalem",
         "Holy Monastery of the Praetorium", "Jerusalem", "Monastery",
         "monastery", phones=["0549/752426"]),
    body("il-je-saint-anna", "jerusalem",
         "Holy Monastery of Saint Anna", "Jerusalem", "Monastery",
         "monastery", phones=["+972-544-628103"]),
    body("il-je-panteleimon-cyril", "jerusalem",
         "Holy Monastery of Saint Panteleimon and Saint Cyril of Jerusalem",
         "Jerusalem", "Monastery", "monastery",
         phones=["+972-2-6280684"]),
    body("il-je-holy-sion", "jerusalem",
         "Holy Monastery of Holy Sion", "Jerusalem", "Monastery",
         "monastery"),
    body("il-je-ascension", "jerusalem",
         "Holy Monastery of the Ascension", "Jerusalem", "Monastery",
         "monastery", phones=["+972-528-128087"],
         emails=["monanalipsi.holyland@gmail.com"]),
    body("il-je-holy-cross", "jerusalem",
         "Holy Monastery of the Holy Cross", "Jerusalem", "Monastery",
         "monastery", phones=["00972-547487664", "0543217107"],
         emails=["theholycrossmonastery@gmail.com"],
         address=["P.O. Box 14083", "Jerusalem 9114002", "Israel"]),
    body("il-je-saint-simeon-katamon", "jerusalem",
         "Holy Monastery of Saint Simeon in Katamon", "Jerusalem",
         "Monastery", "monastery", phones=["02/6790477", "0544/988542"],
         emails=["parthenios27@gmail.com"]),
    body("il-je-prophet-elijah", "jerusalem",
         "Holy Monastery of Prophet Elijah", "Jerusalem", "Monastery",
         "monastery", phones=["0528/128087"],
         address=["Greek Orthodox Convent", "P.O. Box 876",
                  "Jerusalem 9100801", "Israel"]),
    body("il-je-john-baptist-ein-karem", "jerusalem",
         "Holy Monastery of Saint John the Baptist in Ein Karem",
         "Jerusalem", "Monastery", "monastery",
         phones=["02/6436297", "0544/865063"],
         address=["P.O. Box 14223", "Jerusalem 91141", "Israel"]),
    body("il-je-saint-onoufrios", "jerusalem",
         "Holy Monastery of Saint Onoufrios", "Jerusalem", "Monastery",
         "monastery", phones=["+972-505-315530"]),
    body("il-je-saint-stephen", "jerusalem",
         "Holy Monastery of Saint Stephen", "Jerusalem", "Monastery",
         "monastery", phones=["0586/112017", "02/6288092"]),
    body("il-je-beitphage", "jerusalem",
         "Holy Monastery of Beitphage", "Jerusalem", "Monastery",
         "monastery", phones=["0542/076941", "0542/421175"],
         address=["Greek Orthodox Convent", "P.O. Box 20697", "Jerusalem"]),
    body("il-je-saint-modestos", "jerusalem",
         "Holy Monastery of Saint Modestos", "Jerusalem", "Monastery",
         "monastery", phones=["00972 545695084"]),
    body("il-je-abraham", "jerusalem",
         "Holy Monastery of Abraham", "Jerusalem", "Monastery",
         "monastery"),
    body("il-je-megali-panaghia", "jerusalem",
         "Holy Monastery of Megali Panaghia", "Jerusalem", "Monastery",
         "monastery", phones=["0546/026930"]),
    body("il-je-saint-euthymios", "jerusalem",
         "Holy Monastery of Saint Euthymios", "Jerusalem", "Monastery",
         "monastery", phones=["0544/305968"]),
    body("il-je-panaghia-sayda-naya", "jerusalem",
         "Holy Monastery of Panaghia Sayda Naya", "Jerusalem", "Monastery",
         "monastery", phones=["+972-544-364157"]),
    body("il-je-central-saint-demetrios", "il-je-central-constantine-helen",
         "Chapel of Saint Demetrios", "Jerusalem", "Chapel"),
    body("il-je-central-saint-thecla", "il-je-central-constantine-helen",
         "Chapel of Saint Thecla", "Jerusalem", "Chapel"),
    body("il-je-saint-james-cathedral", "jerusalem",
         "Cathedral of Saint James the Brother of God", "Jerusalem",
         "Cathedral", phones=["+972-2-6284185", "02/6289954"]),
    body("il-je-saint-james-myrrh-bearers",
         "il-je-saint-james-cathedral",
         "Chapel of the Myrrh-bearing Women", "Jerusalem", "Chapel"),
    body("il-je-saint-james-forty-martyrs",
         "il-je-saint-james-cathedral",
         "Chapel of the Holy Forty Martyrs", "Jerusalem", "Chapel"),

    body("il-je-holy-sepulchre", "jerusalem",
         "Church of the Holy Sepulchre", "Jerusalem", "Shrine",
         sources=[JP_SHRINES], phones=["02/6284202"],
         address=["Church of the Holy Sepulchre", "P.O. Box 14367",
                  "Jerusalem"]),
    body("il-je-holy-gethsemane", "jerusalem", "Holy Gethsemane",
         "Jerusalem", "Shrine", sources=[JP_SHRINES],
         phones=["+972/548/802421"]),

    body("il-je-tiberias-twelve-apostles", "jerusalem",
         "Holy Monastery of the Twelve Apostles in Tiberias", "Tiberias",
         "Monastery", "monastery", [JP_OUTSIDE], phones=["04/6720042"]),
    body("il-je-mount-tabor", "jerusalem",
         "Holy Monastery of Mount Tabor", "Mount Tabor", "Monastery",
         "monastery", [JP_OUTSIDE], phones=["0504931632"],
         address=["Greek Orthodox Convent", "P.O. Box 2100",
                  "Nazareth 16000"]),
    body("il-je-cana", "jerusalem", "Holy Monastery of Cana, Galilee",
         "Cana", "Monastery", "monastery", [JP_OUTSIDE]),
    body("il-je-capernaum-holy-apostles", "jerusalem",
         "Holy Monastery of the Holy Apostles in Capernaum", "Capernaum",
         "Monastery", "monastery", [JP_OUTSIDE],
         phones=["04/6722282"], emails=["capernaoum1@gmail.com"],
         address=["Greek Orthodox Convent", "P.O. Box 385", "Tiberias"]),
    body("il-je-lod-saint-george", "jerusalem",
         "Holy Monastery of Saint George in Lod", "Lod", "Monastery",
         "monastery", [JP_OUTSIDE], phones=["08/9222023"],
         address=["Greek Orthodox Convent", "P.O. Box 230", "Lod"]),
    body("il-je-ramle-saint-george", "jerusalem",
         "Holy Monastery of Saint George in Ramle", "Ramle", "Monastery",
         "monastery", [JP_OUTSIDE], phones=["08/9221174", "0544/484786"],
         emails=["nifonmitsoulis@yahoo.com"],
         address=["Greek Orthodox Convent", "Kehilat Detroit Street 2",
                  "P.O. Box 38", "7100 Ramle"]),
    body("il-je-qasr-el-mutran-holy-cross", "jerusalem",
         "Holy Monastery of the Holy Cross in Qasr El-Mutran", "Nazareth",
         "Monastery", "monastery", [JP_OUTSIDE], phones=["0522/413348"]),

    body("il-je-haifa-forerunner", "jerusalem",
         "Holy Church of the Forerunner in Haifa", "Haifa", "Church",
         sources=[JP_EXTERNAL], phones=["0509/368317"]),
    body("il-je-haifa-prophet-elias", "jerusalem",
         "Holy Church of Prophet Elias in Haifa", "Haifa", "Church",
         sources=[JP_EXTERNAL], phones=["0509/368317"]),

    body("il-je-russian-community-jerusalem", "jerusalem",
         "Russian-speaking Community Parish in Jerusalem", "Jerusalem",
         "Parish", sources=[JP_COMMUNITIES],
         phones=["02/6436297", "0544/700965"]),
    body("il-je-russian-community-haifa", "jerusalem",
         "Russian-speaking Community Parish in Haifa", "Haifa", "Parish",
         sources=[JP_COMMUNITIES], phones=["0545/826855"]),
    body("il-je-russian-community-tiberias", "jerusalem",
         "Russian-speaking Community Parish in Tiberias", "Tiberias",
         "Parish", sources=[JP_COMMUNITIES], phones=["04/6720042"]),
    body("il-je-russian-community-capernaum", "jerusalem",
         "Russian-speaking Community Parish in Capernaum", "Capernaum",
         "Parish", sources=[JP_COMMUNITIES],
         phones=["04/6722282", "0544/671747"]),
    body("il-je-russian-community-beersheba", "jerusalem",
         "House of Prayer of Patriarch Abraham in Beersheba", "Beersheba",
         "Prayer House", sources=[JP_COMMUNITIES], phones=["0587/971943"],
         address=["Ha Manof 4", "Beersheba"]),
    body("il-je-russian-community-ashdod-ashkelon", "jerusalem",
         "House of Prayer of the Holy Apostle Philip the Deacon in Ashdod and Ashkelon",
         "Ashdod", "Prayer House", sources=[JP_COMMUNITIES],
         phones=["0544/479499"],
         address=["Ha Kalanit Street 9", "Apartment 16", "4th floor",
                  "Ashdod"]),
]


PTOLEMAIS_ROWS = [
    body("il-je-ptolemais-saint-george", "je-ptolemais",
         "Holy Metropolitan Church of Saint George", "Acre", "Cathedral",
         sources=[JP_METROPOLIS], phones=["04/9811519"]),
    body("il-je-beane-saint-barbara", "je-ptolemais",
         "Church of Saint Barbara in Beane", "Beane", sources=[JP_METROPOLIS],
         phones=["0546/205776"]),
    body("il-je-zdeideh-saint-patrick", "je-ptolemais",
         "Church of Saint Patrick in Zdeideh", "Zdeideh",
         sources=[JP_METROPOLIS], phones=["04/9866917", "0546/887144"]),
    body("il-je-maker-prophet-elias", "je-ptolemais",
         "Church of Prophet Elias in Maker", "Maker", sources=[JP_METROPOLIS],
         phones=["0509/603603", "04/9964401"]),
    body("il-je-tarshiha-prophet-elias", "je-ptolemais",
         "Church of Prophet Elias in Tarshiha", "Tarshiha",
         sources=[JP_METROPOLIS], phones=["04/9974087", "0543/476265"]),
    body("il-je-ibillin-saint-george", "je-ptolemais",
         "Church of Saint George in I'billin", "I'billin",
         sources=[JP_METROPOLIS], phones=["0522/338811"]),
    body("il-je-kafr-samia-constantine-helen", "je-ptolemais",
         "Church of Saints Constantine and Helen in Kafr Sami'a",
         "Kafr Sami'a", sources=[JP_METROPOLIS], phones=["0522/433464"]),
    body("il-je-pekiin-old-saint-george", "je-ptolemais",
         "Church of Saint George in Old Peki'in", "Peki'in",
         sources=[JP_METROPOLIS], phones=["0544/787193"]),
    body("il-je-pekiin-new-saint-george", "je-ptolemais",
         "Church of Saint George in New Peki'in", "Peki'in",
         sources=[JP_METROPOLIS], phones=["0587/003001"],
         emails=["nektarios.farah@gmail.com"]),
    body("il-je-kafr-yasif-saint-george", "je-ptolemais",
         "Church of Saint George in Kafr Yasif", "Kafr Yasif",
         sources=[JP_METROPOLIS], phones=["0543/109023", "0544/319697"]),
    body("il-je-sakhnin-saint-george", "je-ptolemais",
         "Church of Saint George in Sakhnin", "Sakhnin",
         sources=[JP_METROPOLIS], phones=["0524/701510"]),
    body("il-je-sakhnin-nativity-theotokos", "je-ptolemais",
         "Church of the Nativity of the Theotokos in Sakhnin", "Sakhnin",
         sources=[JP_METROPOLIS], phones=["0524/701510"]),
    body("il-je-rameh-saint-george", "je-ptolemais",
         "Church of Saint George in Rameh", "Rameh", sources=[JP_METROPOLIS],
         phones=["0509/589534", "0527/297260"]),
    body("il-je-shefa-amr-constantine-helen", "je-ptolemais",
         "Church of Saints Constantine and Helen in Shefa-Amr", "Shefa-Amr",
         sources=[JP_METROPOLIS], phones=["0506/961292", "04/9500893"]),
    body("il-je-abu-snan-saint-george", "je-ptolemais",
         "Church of Saint George in Abu Snan", "Abu Snan",
         sources=[JP_METROPOLIS], phones=["0545/359985"]),
    body("il-je-saab-saint-george", "je-ptolemais",
         "Holy Church of Saint George in Sa'ab", "Sa'ab",
         sources=[JP_METROPOLIS]),
    body("il-je-russian-community-acre", "je-ptolemais",
         "Russian-speaking Community Parish in Acre", "Acre", "Parish",
         sources=[JP_COMMUNITIES]),
]


NAZARETH_ROWS = [
    body("il-je-nazareth-annunciation", "je-nazareth",
         "Venerating Church of the Annunciation of the Theotokos", "Nazareth",
         "Shrine", sources=[JP_METROPOLIS],
         phones=["04/6569349", "04/6456463"]),
    body("il-je-nazareth-saint-george", "je-nazareth",
         "Metropolitan Church of Saint George", "Nazareth", "Cathedral",
         sources=[JP_METROPOLIS], phones=["04/6021533"]),
    body("il-je-eilaboun-saint-george", "je-nazareth",
         "Church of Saint George in Eilaboun", "Eilaboun",
         sources=[JP_METROPOLIS], phones=["0506/543983"]),
    body("il-je-turaan-saint-george", "je-nazareth",
         "Church of Saint George in Turaan", "Turaan", sources=[JP_METROPOLIS],
         phones=["0544/491629"]),
    body("il-je-yafat-nasra-saint-george", "je-nazareth",
         "Church of Saint George in Yafat Nasra", "Yafat Nasra",
         sources=[JP_METROPOLIS], phones=["0526/733398"]),
    body("il-je-reineh-saint-george", "je-nazareth",
         "Church of Saint George in Reineh", "Reineh", sources=[JP_METROPOLIS],
         phones=["0543/180480"]),
    body("il-je-migdal-haemek-saint-nicholas", "je-nazareth",
         "Church of Saint Nicholas in Migdal HaEmek", "Migdal HaEmek",
         sources=[JP_METROPOLIS], phones=["0506/514775"]),
    body("il-je-maalul-ascension-prophet-elias", "je-nazareth",
         "Church of the Ascension and Prophet Elias in Maalul", "Maalul",
         sources=[JP_METROPOLIS], phones=["0522/413348"]),
    body("il-je-russian-community-nazareth", "je-nazareth",
         "Russian-speaking Community Parish in Nazareth", "Nazareth",
         "Parish", sources=[JP_COMMUNITIES],
         phones=["04/6021533", "0542/250366"]),
    body("il-je-russian-community-migdal-haemek", "je-nazareth",
         "Russian-speaking Community Parish in Migdal HaEmek",
         "Migdal HaEmek", "Parish", sources=[JP_COMMUNITIES],
         phones=["04/6021533", "0506/514775"]),
]


JAFFA_ROWS = [
    body("il-je-jaffa-archangels", "je-jaffa",
         "Holy Monastery of the Archangels in Jaffa", "Jaffa", "Monastery",
         "monastery", [JP_COMMITTEES], phones=["03/6823451"],
         address=["Greek Orthodox Convent", "Nativ Hamazalot 8",
                  "Jaffa 68021"]),
    body("il-je-jaffa-saint-george", "je-jaffa",
         "Holy Church of Saint George in Jaffa", "Jaffa", sources=[JP_COMMITTEES],
         phones=["0523/187618"]),
    body("il-je-jaffa-saint-tabitha", "je-jaffa",
         "Holy Church of Saint Tabitha in Jaffa", "Jaffa",
         sources=[JP_COMMITTEES], phones=["0507/644218"]),
    body("il-je-russian-community-jaffa", "je-jaffa",
         "Russian-speaking Community Parish in Jaffa", "Jaffa", "Parish",
         sources=[JP_COMMUNITIES, JP_COMMITTEES], phones=["0507/644218"]),
    body("il-je-romanian-community-jaffa", "je-jaffa",
         "Romanian-speaking Community Parish in Jaffa", "Jaffa", "Parish",
         sources=[JP_COMMUNITIES, JP_COMMITTEES], phones=["0527/748482"]),
]


ROCOR_ROWS = [
    body("il-rocor-mount-olives-ascension", "ru-jerusalem-mission-rocor",
         "Convent of the Ascension of Our Lord on the Mount of Olives",
         "Jerusalem", "Convent", "monastery", [ROCOR_CONTACTS],
         local="Спасо-Вознесенский женский монастырь на г. Елеонской",
         address=["P.O. Box 19229", "Jerusalem 91191", "Israel"],
         site="https://eleonmonastery.com/", phones=["+972 (2) 628 4373"],
         emails=["eleon.monastery@outlook.com"]),
    body("il-rocor-gethsemane-mary-magdalene",
         "ru-jerusalem-mission-rocor",
         "Convent of Saint Mary Magdalene in Gethsemane", "Jerusalem",
         "Convent", "monastery", [ROCOR_CONTACTS],
         local="Женская обитель св. Марии Магдалины в Гефсиманском саду",
         address=["P.O. Box 19238", "Jerusalem 91191", "Israel"],
         phones=["+972 54 694 7510"],
         emails=["mmconventoffice@gmail.com"]),
    body("il-rocor-alexander-nevsky-excavations",
         "ru-jerusalem-mission-rocor",
         "Saint Alexander Nevsky Church at the Excavations", "Jerusalem",
         "Church", sources=[ROCOR_CONTACTS],
         local="Храм святого благоверного князя Александра Невского Раскопки",
         address=["Dabbagah St. 25", "P.O. Box 20164", "Jerusalem 91200",
                  "Israel"], phones=["+972 (2) 628 3088"],
         emails=["rocorrem@gmail.com"]),
    body("il-rocor-tomb-of-prophets", "ru-jerusalem-mission-rocor",
         "Tomb of the Prophets", "Jerusalem", "Shrine",
         sources=[ROCOR_CONTACTS], local="Гробница пророков",
         address=["Dabbagah St. 25", "P.O. Box 20164", "Jerusalem 91200",
                  "Israel"], phones=["+972 (2) 628 3088"],
         emails=["rocorrem@gmail.com"]),
]


ROWS = {
    "jerusalem": JERUSALEM_ROWS,
    "je-ptolemais": PTOLEMAIS_ROWS,
    "je-nazareth": NAZARETH_ROWS,
    "je-jaffa": JAFFA_ROWS,
    "ru-jerusalem-mission-rocor": ROCOR_ROWS,
}


DIRECT_RUSSIA_ROWS = [
    body("ru-jerusalem-mission-mp", "russia",
         "Russian Ecclesiastical Mission in Jerusalem (Moscow Patriarchate)",
         "Jerusalem", "Mission", "diocese", [MP_CONTACT, MP_HISTORY],
         local="Русская духовная миссия в Иерусалиме",
         address=["Russian Compound", "6 Heshin Street", "P.O. Box 1042",
                  "Jerusalem 9100902", "Israel"], site="https://rusdm.ru/",
         phones=["+972 2 625-25-65"], emails=["missia.jerusalem@gmail.com"]),
    body("il-mp-holy-trinity-cathedral", "ru-jerusalem-mission-mp",
         "Holy Trinity Cathedral at the Russian Compound", "Jerusalem",
         "Cathedral", sources=[MP_CHAPELS, MP_HISTORY],
         local="Троицкий собор в Иерусалиме",
         address=["Holy Trinity Cathedral", "Russian Compound",
                  "Moskva Square", "Jerusalem", "Israel"],
         phones=["02-625-25-65"]),
    body("il-mp-saint-alexandra", "ru-jerusalem-mission-mp",
         "Church of Saint Alexandra the Martyr at the Russian Compound",
         "Jerusalem", "Church", sources=[MP_HISTORY],
         local="Храм святой мученицы царицы Александры на Русском Подворье в Иерусалиме"),
    body("il-mp-gorny-convent", "ru-jerusalem-mission-mp",
         "Gorny Convent in Ein Karem", "Jerusalem", "Convent", "monastery",
         [MP_CHAPELS, MP_HISTORY],
         local="Горненский женский монастырь в Эйн-Кареме",
         address=["Gornenskiy Convent", "P.O. Box 1699",
                  "Jerusalem 9100902", "Israel"],
         phones=["02-641-28-87"]),
    body("il-mp-jaffa-peter-tabitha", "ru-jerusalem-mission-mp",
         "Metochion of Saints Peter and Tabitha in Jaffa", "Jaffa",
         "Metochion", sources=[MP_CHAPELS, MP_HISTORY],
         local="Подворье в честь апостола Петра и праведной Тавифы в Яффе",
         address=["Russian Church", "157 Herzl St.", "Tel-Aviv", "Israel"],
         phones=["058-695-13-52"]),
    body("il-mp-haifa-prophet-elijah", "ru-jerusalem-mission-mp",
         "Metochion of Prophet Elijah in Haifa", "Haifa", "Metochion",
         sources=[MP_CHAPELS, MP_HISTORY],
         local="Подворье в честь пророка Илии в Хайфе",
         address=["Russian Church", "6 Ha-Hursha St.", "Haifa", "Israel"],
         phones=["04-833-01-90", "052-846-41-81"]),
    body("il-mp-magdala-mary-magdalene", "ru-jerusalem-mission-mp",
         "Metochion of Saint Mary Magdalene in Magdala", "Magdala",
         "Metochion", sources=[MP_CHAPELS, MP_HISTORY],
         local="Подворье в честь равноапостольной Марии Магдалины в Магдале",
         address=["Gan ha-Rusim", "3 km north of Tiberias", "Israel"],
         phones=["052-809-16-01"]),
]


DIRECT_ROMANIA_ROWS = [
    body("il-ro-jerusalem-establishment", "romania",
         "Romanian Establishment in Jerusalem", "Jerusalem", "Settlement",
         sources=[RO_EXTERNAL], local="Așezământul Românesc din Ierusalim",
         address=["46 Shivtei Israel St.", "95105 Jerusalem", "Israel"],
         site="https://www.jerusalem.ro/", phones=["009.722.626.30.34"],
         emails=["bisericaro_jerusalem@yahoo.com"]),
]


EXPECTED = {
    "jerusalem": 54,
    "je-ptolemais": 17,
    "je-nazareth": 10,
    "je-jaffa": 5,
    "ru-jerusalem-mission-rocor": 4,
}
EXPECTED_TOTAL = 98
ALL_SOURCE_ROWS = (
    JERUSALEM_ROWS + PTOLEMAIS_ROWS + NAZARETH_ROWS + JAFFA_ROWS +
    ROCOR_ROWS + DIRECT_RUSSIA_ROWS + DIRECT_ROMANIA_ROWS
)
LOCAL_NAMES = {
    "il-je-little-galilee-men-of-galilee": "كنيسة الرجال الجليليّين",
    "il-je-little-galilee-annunciation-dormition":
        "كنيسة بشارة رقاد الفائقة القداسة والدة الإله",
    "il-je-central-saint-demetrios": "كنيسة القديس ديميتريوس",
    "il-je-central-saint-thecla": "كنيسة القديسة ثقلا",
    "il-je-saint-james-cathedral": "كاتدرائية القديس يعقوب أخو الربّ",
    "il-je-saint-james-myrrh-bearers": "كنيسة حاملات الطيب",
    "il-je-saint-james-forty-martyrs": "كنيسة الأربعين شهيداً",
    "il-je-holy-sepulchre": "كنيسة القيامة",
    "il-je-holy-gethsemane": "كنيسة الجسثمانية",
    "il-je-haifa-forerunner": "كنيسة القديس يوحنّا المعمدان في حيفا",
    "il-je-haifa-prophet-elias": "كنيسة النبي إيليا في حيفا",
    "il-je-russian-community-jerusalem":
        "الرعية الناطقة باللغة الروسية في أورشليم",
    "il-je-russian-community-haifa":
        "الرعية الناطقة باللغة الروسية في حيفا",
    "il-je-russian-community-tiberias":
        "الرعية الناطقة باللغة الروسية في طبريا",
    "il-je-russian-community-capernaum":
        "الرعية الناطقة باللغة الروسية في كفرناحوم",
    "il-je-russian-community-beersheba":
        "بيت مصلّى البطريرك أبراهام في بئر السبع",
    "il-je-russian-community-ashdod-ashkelon":
        "مصلَّى الرسول فيليبوس الشماس في أشدود وأشكلون",
    "il-je-ptolemais-saint-george":
        "كنيسة القديس جيورجيوس المتروبوليتيّة",
    "il-je-beane-saint-barbara": "كنيسة القديسة بربارة في البعنة",
    "il-je-zdeideh-saint-patrick": "كنيسة القديس باتريكيوس في الجديدة",
    "il-je-maker-prophet-elias": "كنيسة النبي إيليا في المكر",
    "il-je-tarshiha-prophet-elias": "كنيسة النبي إيليا في ترشيحا",
    "il-je-ibillin-saint-george": "كنيسة القديس جيورجيوس في عبلين",
    "il-je-kafr-samia-constantine-helen":
        "كنيسة القديسَين قسطنطين وهلانة في كفر سميع",
    "il-je-pekiin-old-saint-george":
        "كنيسة القديس جيورجيوس في البقيعة القديمة",
    "il-je-pekiin-new-saint-george":
        "كنيسة القديس جيورجيوس في البقيعة الجديدة",
    "il-je-kafr-yasif-saint-george":
        "كنيسة القديس جيورجيوس في كفر ياسيف",
    "il-je-sakhnin-saint-george": "كنيسة القديس جيورجيوس في سخنين",
    "il-je-sakhnin-nativity-theotokos":
        "كنيسة ميلاد والدة الإله في سخنين",
    "il-je-rameh-saint-george": "كنيسة القديس جيورجيوس في الرامة",
    "il-je-shefa-amr-constantine-helen":
        "كنيسة القديسَين قسطنطين وهيلانة في شفاعمرو",
    "il-je-abu-snan-saint-george": "كنيسة القديس جيورجيوس في أبو سنان",
    "il-je-saab-saint-george": "كنيسة القديس جيورجيوس في شعب",
    "il-je-russian-community-acre":
        "الرعية الناطقة باللغة الروسية في عكا",
    "il-je-nazareth-annunciation": "مزار كنيسة بشارة والدة الإله",
    "il-je-nazareth-saint-george":
        "كنيسة ميتروبوليتيّة القدّيس جيورجيوس",
    "il-je-eilaboun-saint-george": "كنيسة القديس جيورجيوس في عيلبون",
    "il-je-turaan-saint-george": "كنيسة القديس جيورجيوس في طرعان",
    "il-je-yafat-nasra-saint-george":
        "كنيسة القديس جيورجيوس القديمة في يافة الناصرة",
    "il-je-reineh-saint-george": "كنيسة القديس جيورجيوس في الرينة",
    "il-je-migdal-haemek-saint-nicholas":
        "كنيسة القديس نيقولاوس في المجيدل",
    "il-je-maalul-ascension-prophet-elias":
        "كنيسة الصعود والنبي إيليا في معلول",
    "il-je-russian-community-nazareth":
        "الرعية الناطقة باللغة الروسية في الناصرة",
    "il-je-russian-community-migdal-haemek":
        "الرعية الناطقة باللغة الروسية في المجيدل",
    "il-je-jaffa-saint-george": "كنيسة القديس جوارجيوس في يافا",
    "il-je-jaffa-saint-tabitha": "كنيسة القديسة طابيثا في يافا",
    "il-je-russian-community-jaffa":
        "الرعية الناطقة باللغة الروسية في يافا",
    "il-je-romanian-community-jaffa":
        "الرعية الناطقة باللغة الرومانيّة في يافا",
}
for row in ALL_SOURCE_ROWS:
    if row["id"] in LOCAL_NAMES:
        row["local"] = LOCAL_NAMES[row["id"]]
        if JP_ARABIC_2026 not in row["sources"]:
            row["sources"].append(JP_ARABIC_2026)
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
        if row.get("country") != "IL":
            raise ValueError("%s is outside Israel" % row_id)
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
            "country": "IL",
            "rows": rows,
        }
    validate_rows(DIRECT_RUSSIA_ROWS, "russia", seen)
    validate_rows(DIRECT_ROMANIA_ROWS, "romania", seen)
    row_ids = {row["id"] for row in ALL_SOURCE_ROWS}
    if set(ENGLISH_NAMES) != row_ids or set(CONTACTS) != row_ids:
        raise ValueError("Israel English name or contact map is out of sync")
    if len(row_ids) != EXPECTED_TOTAL:
        raise ValueError("Israel must publish exactly %d rows" % EXPECTED_TOTAL)
    if sum(EXPECTED.values()) + len(DIRECT_RUSSIA_ROWS) + \
            len(DIRECT_ROMANIA_ROWS) != EXPECTED_TOTAL:
        raise ValueError("Israel branch total is out of sync")
    if sum(bool(item["emails"] or item["phones"])
           for item in CONTACTS.values()) != 84:
        raise ValueError("Israel contact-bearing row total is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "IL":
        raise ValueError("Israel candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Israel candidate ledger check date is out of sync")
    expected = dict(EXPECTED)
    expected.update({"russia": 7, "romania": 1, "total": EXPECTED_TOTAL})
    if ledger.get("published_summary") != expected:
        raise ValueError("Israel candidate ledger totals are out of sync")
    for key in ("candidates", "reconciliation", "official_jurisdiction_audit",
                "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Israel candidate ledger lacks %s" % key)
    classes = {item.get("classification") for item in ledger["candidates"]}
    required = {"unnamed", "aggregate-only", "historical", "uncertain",
                "noncanonical", "affiliation-unclear"}
    if not required.issubset(classes):
        raise ValueError("Israel candidate ledger lacks required lead classes")
    for section in ("candidates", "reconciliation",
                    "official_jurisdiction_audit", "exclusions"):
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or not all(
                    isinstance(url, str) and url.startswith("https://")
                    for url in sources):
                raise ValueError("Israel ledger has invalid %s sources" %
                                 section)
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("Israel candidate ledger has forbidden punctuation")
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
        print("directory Israel: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Israel: 98 current bodies under seven canonical branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
