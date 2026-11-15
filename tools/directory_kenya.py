#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Kenya.

The current Alexandrian register establishes four Kenyan eparchies. The
official Eldoret diocesan roster supplies sixty-three exact worship-body
names, and the Nairobi cathedral supplies its own current record. The Russian
Church's current South African Diocese reports 136 Kenyan parishes across ten
deaneries; current official activity records identify eighty of those bodies
exactly. Aggregate-only and conflicting records remain in the companion
candidate ledger.

    python tools/directory_kenya.py --check
    python tools/directory_kenya.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_NAIROBI = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-nairobi/?lang=en"
)
NAIROBI_CATHEDRAL = "https://stsanargyroike.org/metropolis-of-nairobi/"
ELDORET_ROSTER = "https://eldometropolis.org/parishes-clergy/"
AX_ELDORET = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-diocese-of-nieri-and-mount-kenya/?lang=en"
)
RU_DIOCESE = (
    "https://exarchate-africa.ru/en/dioceses_cat/south-african-diocese/"
)
RU_VISIT = (
    "https://exarchate-africa.ru/en/news/"
    "the-archpastoral-visit-of-the-patriarchal-exarch-of-africa-to-"
    "kenya-has-come-to-an-end/"
)
RU_MERU_GREGORY = (
    "https://exarchate-africa.ru/en/news/"
    "the-patriarchal-exarch-of-africa-celebrated-the-liturgy-at-the-"
    "parish-of-st-gregory-the-theologian-in-the-kenyan-deanery-of-mero/"
)
RU_MERU_JAMES = (
    "https://exarchate-africa.ru/en/news/"
    "metropolitan-konstantin-performed-the-rite-of-laying-the-foundation-"
    "stone-for-the-church-of-st-james-the-apostle-and-administered-the-"
    "sacrament-of-baptism-in-the-kenyan-deanery-of-meru/"
)
RU_NAIROBI = (
    "https://exarchate-africa.ru/en/news/"
    "on-the-11th-sunday-after-pentecost-metropolitan-konstantin-"
    "celebrated-the-liturgy-at-the-parish-of-the-great-martyr-"
    "panteleimon-in-the-capital-of-kenya/"
)
RU_NAIVASHA = (
    "https://exarchate-africa.ru/en/news/"
    "the-patriarchal-exarch-of-africa-celebrated-the-liturgy-at-the-"
    "life-giving-trinity-parish-in-naivasha-kenya/"
)
RU_LUGARI = (
    "https://exarchate-africa.ru/en/news/"
    "the-patriarchal-exarch-of-africa-visited-parishes-in-the-lugari-"
    "deanery-in-kenya/"
)
RU_VIHIGA = (
    "https://exarchate-africa.ru/en/news/"
    "metropolitan-konstantin-consecrated-a-church-dedicated-to-saints-"
    "cosmas-and-damian-the-holy-unmercenaries-in-kenya-and-celebrated-"
    "the-liturgy-there/"
)
RU_KAKAMEGA = (
    "https://exarchate-africa.ru/en/news/"
    "on-the-feast-of-the-transfiguration-of-the-lord-metropolitan-"
    "konstantin-celebrated-the-liturgy-at-the-st-panteleimon-parish-in-"
    "the-village-of-ebuyangu-kenya/"
)
RU_MIGORI = (
    "https://exarchate-africa.ru/en/news/"
    "metropolitan-konstantin-consecrated-a-church-dedicated-to-st-"
    "athanasius-the-great-in-the-village-of-nyabigege-kenya/"
)
RU_MIGORI_MEETING = (
    "https://exarchate-africa.ru/en/news/"
    "the-patriarchal-exarch-of-africa-held-a-meeting-of-the-migori-"
    "deanery-kenya/"
)
RU_HOMA_BAY = (
    "https://exarchate-africa.ru/en/news/"
    "metropolitan-konstantin-celebrated-the-liturgy-at-the-parish-of-"
    "st-mark-the-apostle-in-the-homabay-deanery-kenya/"
)
RU_NYERI = (
    "https://exarchate-africa.ru/en/news/"
    "the-patriarchal-exarch-of-africa-metropolitan-constantine-has-"
    "begun-his-visit-to-kenya/"
)
RU_MBOLOLO = (
    "https://exarchate-africa.ru/novosti/"
    "v-s-mbololo-keniya-osvyashhen-novyj-uchastok-pod-stroitelstvo-"
    "hrama-prepodobnogo-pimena-velikogo/"
)


def body(row_id, parent, name, local, seat, rank, sources, address=None,
         site=None, founded=None):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "country": "KE",
        "sources": sources,
    }
    if seat:
        row["seat"] = seat
    if address:
        row["address"] = address
    if site:
        row["site"] = site
    if founded:
        row["founded"] = founded
    return row


NAIROBI_ROWS = [
    body(
        "ke-ax-nairobi-anargyroi-cathedral",
        "ax-nairobi",
        "Patriarchal Cathedral of Sts Anargyroi Greek Orthodox Church",
        "Patriarchal Cathedral of Sts Anargyroi Greek Orthodox Church",
        "Nairobi",
        "Cathedral",
        [NAIROBI_CATHEDRAL, AX_NAIROBI],
        ["6 Valley Rd", "Nairobi, Kenya"],
        "https://stsanargyroike.org/",
        ["Our parish was founded in 1953."],
    ),
]


# Exact current roster labels. Most carry their locality in the label itself.
# The locality-free and grouped labels remain locality-free rather than being
# expanded from copied template fields on their individual pages.
ELDORET_LIST = [
    ("archangel-michael-community", "Archangel Michael Community", None,
     "Community"),
    ("archangels-michael-and-gabriel-kabasgei",
     "Archangels Michael And Gabriel Kabasgei", "Kabasgei", "Parish"),
    ("holy-announciation-kisarich", "Holy Announciation Kisarich",
     "Kisarich", "Parish"),
    ("holy-apostles-eldoret-town", "Holy Apostles Eldoret Town", "Eldoret",
     "Parish"),
    ("holy-ascension-kapkoros", "Holy Ascension Kapkoros", "Kapkoros",
     "Parish"),
    ("holy-cross-chepkakwen", "Holy Cross Chepkakwen", "Chepkakwen",
     "Parish"),
    ("holy-dormition-chepchori", "Holy Dormition Chepchori", "Chepchori",
     "Parish"),
    ("holy-resurrection-koromait", "Holy Resurrection Koromait", "Koromait",
     "Parish"),
    ("holy-resurrection-serem", "Holy Resurrection Serem", "Serem",
     "Parish"),
    ("holy-transfiguration-kipchekwen", "Holy Transfiguration Kipchekwen",
     "Kipchekwen", "Parish"),
    ("holy-trinity-sarura", "Holy Trinity Sarura", "Sarura", "Parish"),
    ("st-andreas-chemelil", "St. Andreas Chemelil", "Chemelil", "Parish"),
    ("st-andrews-community", "St.Andrews Community", None, "Community"),
    ("st-anne-chepkor", "St.Anne Chepkor", "Chepkor", "Parish"),
    ("st-anthimos-enego", "St. Anthimos Enego", "Enego", "Parish"),
    ("st-anthony-kapkechui", "St. Anthony Kapkechui", "Kapkechui",
     "Parish"),
    ("st-athanasios-bomet", "St. Athanasios Bomet", "Bomet", "Parish"),
    ("st-athanasios-chepsaita", "St. Athanasios Chepsaita", "Chepsaita",
     "Parish"),
    ("st-barnabas-nyinyira", "St. Barnabas Nyinyira", "Nyinyira",
     "Parish"),
    ("st-basil-chepkenduon", "St. Basil Chepkenduon", "Chepkenduon",
     "Parish"),
    ("st-catherine-and-photini-napetit", "St. Catherine And Photini Napetit",
     "Napetit", "Parish"),
    ("st-cyril-and-methodios-kamobon", "St. Cyril And Methodios Kamobon",
     "Kamobon", "Parish"),
    ("st-dionysios-kemeloi", "St. Dionysios Kemeloi", "Kemeloi", "Parish"),
    ("st-ephraim-mubare", "St. Ephraim Mubare", "Mubare", "Parish"),
    ("st-george-and-cosmas-kitaor", "St. George And Cosmas Kitaor", "Kitaor",
     "Parish"),
    ("st-george-community", "St.George Community", None, "Community"),
    ("st-george-kamogoywo", "St. George Kamogoywo", "Kamogoywo", "Parish"),
    ("st-hellen-and-constantine-chemogong",
     "St. Hellen And Constantine Chemogong'", "Chemogong'", "Parish"),
    ("st-hellen-and-constantine-kereri",
     "St. Hellen And Constantine Kereri", "Kereri", "Parish"),
    ("st-herman-of-alaska-ngechepcha", "St. Herman Of Alaska Ng'echepcha",
     "Ng'echepcha", "Parish"),
    ("st-irine-chemase", "St. Irine Chemase", "Chemase", "Parish"),
    ("st-irine-kamaitgok", "St. Irine Kamaitgok", "Kamaitgok", "Parish"),
    ("st-james-chemonoi", "St. James Chemonoi", "Chemonoi", "Parish"),
    ("st-john-the-baptist-lodwar", "St. John The Baptist Lodwar", "Lodwar",
     "Parish"),
    ("st-john-the-baptist-siginwai", "St. John The Baptist Siginwai",
     "Siginwai", "Parish"),
    ("st-katherine-kamasia", "St. Katherine Kamasia", "Kamasia", "Parish"),
    ("st-kyriaki-chepkiwis", "St. Kyriaki Chepkiwis", "Chepkiwis", "Parish"),
    ("st-luke-chepterit", "St. Luke Chepterit", "Chepterit", "Parish"),
    ("st-marina-kiboine", "St. Marina Kiboine", "Kiboine", "Parish"),
    ("st-mark-cathedral-kapsabet", "St. Mark Cathedral Kapsabet", "Kapsabet",
     "Cathedral"),
    ("st-mark-nakuutan", "St. Mark Nakuutan", "Nakuutan", "Parish"),
    ("st-marys-kaborok", "St. Marys Kaborok", "Kaborok", "Parish"),
    ("st-marys-st-george-st-andrew-communities",
     "St. Marys /St. George/St.Andrew Communities", None, "Parish Group"),
    ("st-nektarios-chebugundi", "St. Nektarios Chebugundi", "Chebugundi",
     "Parish"),
    ("st-nektarios-lemook", "St. Nektarios Lemook", "Lemook", "Parish"),
    ("st-nicholas-kiptaruswo", "St. Nicholas Kiptaruswo", "Kiptaruswo",
     "Parish"),
    ("st-nicholas-lokichar", "St.Nicholas Lokichar", "Lokichar", "Parish"),
    ("st-nicodemus-kamarich", "St. Nicodemus Kamarich", "Kamarich",
     "Parish"),
    ("st-nina-kesengei", "St. Nina Kesengei", "Kesengei", "Parish"),
    ("st-paisios-iboe", "St. Paisios Iboe", "Iboe", "Parish"),
    ("st-paisios-the-athonite-lebelen", "St. Paisios The Athonite Lebelen",
     "Lebelen", "Parish"),
    ("st-panteleimon-kenyor", "St. Panteleimon Kenyor", "Kenyor", "Parish"),
    ("st-paul-community", "St. Paul Community", None, "Community"),
    ("st-paul-kobos", "St. Paul Kobos", "Kobos", "Parish"),
    ("st-peter-and-paul-chebarus", "St. Peter And Paul Chebarus", "Chebarus",
     "Parish"),
    ("st-peter-loupwala", "St. Peter Loupwala", "Loupwala", "Parish"),
    ("st-peters", "St. Peters", None, "Parish"),
    ("st-peters-kapkechui", "St. Peters Kapkechui", "Kapkechui", "Parish"),
    ("st-sarvas-chepkuny", "St. Sarvas Chepkuny", "Chepkuny", "Parish"),
    ("st-stephen-chemororoch", "St. Stephen Chemororoch", "Chemororoch",
     "Parish"),
    ("st-styllianos-morongiot", "St. Styllianos Morong'iot", "Morong'iot",
     "Parish"),
    ("virgin-mary-ratinwet", "Virgin Mary Ratinwet", "Ratinwet", "Parish"),
    ("virgin-mary-students-chapel",
     "Virgin Mary - Bishop Makarios Secondary Chapel", None, "Chapel"),
]


def eldoret_rows():
    rows = []
    for slug, name, seat, rank in ELDORET_LIST:
        detail = "https://eldometropolis.org/branch/%s/" % slug
        rows.append(body(
            "ke-ax-eldoret-%s" % slug,
            "ax-eldoret",
            name,
            name,
            seat,
            rank,
            [ELDORET_ROSTER, detail, AX_ELDORET],
        ))
    return rows


def ru(row_id, name, seat, sources, rank="Parish"):
    # Official English records supply the default local form. Exact Russian
    # forms from Russian-only records replace it below.
    return body(
        "ke-ru-%s" % row_id,
        "ru-south-africa",
        name,
        name,
        seat,
        rank,
        sources,
    )


RU_ROWS = [
    # The nine exact contact parishes in the current 136-parish roster.
    ru("buyangu-nectarios", "Parish of St. Nectarios of Aegina", "Buyangu",
       [RU_DIOCESE, RU_VIHIGA]),
    ru("mbololo-pimen", "Parish of St. Pimen the Great", "Mbololo",
       [RU_DIOCESE, RU_MBOLOLO]),
    ru("gombe-andrew", "Parish of the Apostle Andrew", "Gombe",
       [RU_DIOCESE]),
    ru("kipkaren-james", "Parish of the Apostle James", "Kipkaren",
       [RU_DIOCESE]),
    ru("mworoga-tikhon",
       "Parish of St. Tikhon, Patriarch of Moscow and All Russia", "Mworoga",
       [RU_DIOCESE]),
    ru("oyani-alexander-nevsky",
       "Parish of the Holy Right-Believing Prince Alexander Nevsky", "Oyani",
       [RU_DIOCESE, RU_MIGORI]),
    ru("tilolwo-constantine-helena",
       "Parish of the Equal-to-the-Apostles Constantine and Helena", "Tilolwo",
       [RU_DIOCESE, RU_VISIT]),
    ru("gitima-sophia", "Parish of the Martyr Sophia", "Gitima",
       [RU_DIOCESE, RU_NYERI]),
    ru("malunge-macarius-kalyazin", "Parish of St. Macarius of Kalyazin",
       "Malunge", [RU_DIOCESE]),

    # Exact bodies named during the current August 2026 Kenya visitation.
    ru("ngarendare-gregory", "Parish of St. Gregory the Theologian",
       "Ngarendare", [RU_VISIT, RU_MERU_GREGORY]),
    ru("gitongo-john-nativity",
       "Parish of the Nativity of St. John the Forerunner", "Gitongo",
       [RU_VISIT, RU_MERU_GREGORY]),
    ru("kiambogo-nicholas", "Parish of St. Nicholas the Wonderworker",
       "Kiambogo", [RU_VISIT, RU_MERU_GREGORY]),
    ru("igembe-james-alphaeus",
       "Parish of the Apostle James the Son of Alphaeus", "Igembe",
       [RU_VISIT, RU_MERU_JAMES]),
    ru("antuamvuo-athanasius", "Parish of St. Athanasius the Great",
       "Antuamvuo", [RU_VISIT, RU_MERU_JAMES]),
    ru("naivasha-trinity", "Life-Giving Trinity Parish", "Naivasha",
       [RU_VISIT, RU_NAIVASHA]),
    ru("nyabini-nectarios", "Parish of St. Nektarios of Aegina", "Nyabini",
       [RU_VISIT, RU_NAIVASHA]),
    ru("mutonyora-mary-egypt", "Parish of the Venerable Mary of Egypt",
       "Mutonyora", [RU_VISIT, RU_NAIVASHA]),
    ru("nairobi-panteleimon",
       "Parish of the Great Martyr and Healer Panteleimon", "Nairobi",
       [RU_VISIT, RU_NAIROBI]),
    ru("ngamba-george", "Parish of St. George the Victorious", "Ngamba",
       [RU_VISIT, RU_NAIROBI]),
    ru("baringo-john-alexander",
       "Parish of St. John the Forerunner and Hieromartyr Alexander Parusnikov",
       "Nginian", [RU_VISIT, RU_LUGARI]),
    ru("marakusi-paul", "Parish of the Apostle Paul", "Marakusi",
       [RU_VISIT, RU_LUGARI]),
    ru("mulovol-cosmas-damian",
       "Church of Saints Cosmas and Damian, Martyrs of Rome", "Mulovol",
       [RU_VISIT, RU_VIHIGA], rank="Church"),
    ru("kapsayon-cyprian", "Parish of St. Cyprian of Carthage", "Kapsayon",
       [RU_VISIT,
        "https://exarchate-africa.ru/donations/"
        "postroim-hram-v-chest-svyatitelya-kipriana-karfagenskogo-v-kenii/"]),
    ru("kapasianga-elijah", "Parish of the Prophet Elijah", "Kapasianga",
       [RU_VISIT, RU_VIHIGA]),
    ru("ebuyangu-panteleimon",
       "Parish of the Great Martyr and Healer Panteleimon", "Ebuyangu",
       [RU_VISIT, RU_KAKAMEGA]),
    ru("essaba-john-kalita", "Parish of the Righteous Prince John Kalita",
       "Essaba", [RU_VISIT, RU_KAKAMEGA]),
    ru("ramula-mary-egypt", "Parish of St. Mary of Egypt", "Ramula",
       [RU_VISIT, RU_KAKAMEGA]),
    ru("ketim-peter", "Parish of the Apostle Peter", "Ketim", [RU_VISIT]),
    ru("kisarich-james-zebedee",
       "Parish of St. James the Son of Zebedee", "Kisarich", [RU_VISIT]),
    ru("chemelil-zosima", "Parish of St. Zosima of Solovki", "Chemelil",
       [RU_VISIT]),
    ru("nyabigege-athanasius", "Parish of St. Athanasius the Great",
       "Nyabigege", [RU_VISIT, RU_MIGORI]),
    ru("manyatta-john-baptist", "Parish of St. John the Baptist", "Manyatta",
       [RU_VISIT, RU_MIGORI]),
    ru("bvare-philotheus", "Parish of the Martyr Philotheus of Samosata",
       "Bvare", [RU_VISIT, RU_MIGORI_MEETING]),
    ru("sanjweru-mark", "Parish of the Apostle Mark", "Sanjweru",
       [RU_VISIT, RU_HOMA_BAY]),
    ru("kibwer-barnabas", "Parish of the Apostle Barnabas", "Kibwer",
       [RU_VISIT, RU_HOMA_BAY]),
    ru("godkeyo-nectarios", "Parish of St. Nektarios of Aegina", "Godkeyo",
       [RU_VISIT, RU_HOMA_BAY]),

    # Other exact bodies with direct official activity in 2026.
    ru("nairobi-sergius", "Parish of St. Sergius of Radonezh", "Nairobi", [
        "https://exarchate-africa.ru/novosti/"
        "sovershena-liturgiya-na-novom-prihode-v-chest-prepodobnogo-sergiya-"
        "radonezhskogo-v-stolicze-kenii/"
    ]),
    ru("maseno-irene", "Parish of the Great Martyr Irene", "Maseno", [
        "https://exarchate-africa.ru/en/news/"
        "father-alexander-otoli-rector-of-the-parishes-of-the-great-martyr-"
        "irene-and-the-first-martyr-stephen-in-the-kakamega-deanery-in-"
        "kenya-has-passed-away/"
    ]),
    ru("ebaya-stephen", "Parish of the First Martyr and Archdeacon Stephen",
       "Ebaya", [
        "https://exarchate-africa.ru/en/news/"
        "father-alexander-otoli-rector-of-the-parishes-of-the-great-martyr-"
        "irene-and-the-first-martyr-stephen-in-the-kakamega-deanery-in-"
        "kenya-has-passed-away/"
    ]),
    ru("nyamilu-basil", "Parish of St. Basil the Great", "Nyamilu", [
        "https://exarchate-africa.ru/novosti/"
        "postroeno-novoe-uchebnoe-zdanie-v-obrazovatelnom-czentre-"
        "svyatitelya-vasiliya-velikogo-v-kenii/"
    ]),
    ru("tumaini-john-shanghai", "Parish of St. John of Shanghai", "Tumaini",
       ["https://exarchate-africa.ru/novosti/"
        "v-blagochinii-nieri-keniya-osvyashhen-novyj-zemelnyj-uchastok-pod-"
        "prihodskuyu-fermu/"]),
    ru("kahuho-nicholas", "Church of St. Nicholas the Wonderworker", "Kahuho",
       ["https://exarchate-africa.ru/novosti/"
        "pashalnye-torzhestva-i-tainstvo-kreshheniya-sostoyalis-na-"
        "nikolskom-prihode-v-kenijskom-blagochinii-nieri/"], rank="Church"),
    ru("kinangop-joseph", "Parish of St. Joseph the Betrothed", "Kinangop", [
        "https://exarchate-africa.ru/en/news/"
        "easter-celebrations-and-charity-events-held-in-the-central-"
        "deanery-of-kenya/"
    ]),
    ru("ndenderu-gerasimos", "Parish of St. Gerasimos of the Jordan",
       "Ndenderu", ["https://exarchate-africa.ru/novosti/"
        "v-czentralnom-blagochinii-kenii-provedeno-sobranie-molodezhnogo-"
        "aktiva-i-pedagogov-voskresnyh-shkol/"]),
    ru("panpaper-community", "Orthodox Community in Panpaper", "Panpaper", [
        "https://exarchate-africa.ru/novosti/"
        "sovershena-pervaya-liturgiya-v-novoj-obshhine-v-s-panpejper-na-"
        "zapade-kenii/"
    ], rank="Community"),
    ru("mlimani-demetrius",
       "Church of the Great Martyr Demetrius of Thessaloniki", "Mlimani", [
        "https://exarchate-africa.ru/novosti/"
        "ierej-georgij-maksimov-sovershil-poezdku-v-keniyu/"
    ], rank="Church"),
    ru("indagalasia-vladimir",
       "Parish of the Equal-to-the-Apostles Prince Vladimir", "Indagalasia", [
        "https://exarchate-africa.ru/novosti/"
        "v-blagochinii-kakamega-keniya-sostoyalos-obshhee-sobranie-"
        "duhovenstva/"
    ]),
    ru("bukura-mark", "Parish of the Apostle Mark", "Bukura", [
        "https://exarchate-africa.ru/novosti/"
        "na-prihode-apostola-marka-v-kenijskom-blagochinii-kakamega-"
        "sostoyalos-obshhee-sobranie-duhovenstva/"
    ]),

    # Exact official bodies confirmed by direct activity in 2024 or 2025.
    ru("zimmerman-catherine", "Parish of the Great Martyr Catherine",
       "Zimmerman", ["https://exarchate-africa.ru/novosti/"
        "patriarshij-ekzarh-afriki-sovershil-liturgiyu-na-prihode-"
        "velikomucheniczy-ekateriny-v-prigorode-stoliczy-kenii/"]),
    ru("kikuyu-george", "Parish of the Great Martyr George the Victory-Bearer",
       "Kikuyu", ["https://exarchate-africa.ru/en/news/"
        "the-rector-of-the-parish-of-the-great-martyr-george-the-victory-"
        "bearer-in-the-central-deanery-of-kenya-priest-ephraim-kimani-has-"
        "reposed-in-the-lord/"]),
    ru("limuru-lazarus", "Parish of St. Lazarus", "Limuru", [
        "https://exarchate-africa.ru/en/news/"
        "patriarchal-exarch-of-africa-visits-central-deanery-parishes-in-"
        "kenya/"
    ]),
    ru("munzasti-moses-black", "Parish of St. Moses the Black", "Munzasti", [
        "https://exarchate-africa.ru/novosti/"
        "v-blagochinii-vihiga-keniya-zavershilsya-dvuhdnevnyj-obuchayushhij-"
        "seminar-dlya-miryan/"
    ]),
    ru("kaptendje-vladimir",
       "Parish of the Equal-to-the-Apostles Prince Vladimir", "Kaptendje", [
        "https://exarchate-africa.ru/novosti/"
        "v-den-poprazdnstva-preobrazheniya-gospodnya-mitropolit-konstantin-"
        "sovershil-liturgiyu-v-blagochinii-vihiga-keniya/"
    ]),
    ru("siyakuti-james-brother",
       "Parish of the Apostle James, Brother of the Lord", "Siyakuti", [
        "https://exarchate-africa.ru/novosti/"
        "zavershilas-poezdka-patriarshego-ekzarha-afriki-v-keniyu-2/"
    ]),
    ru("siala-gerasimos", "Parish of St. Gerasimos of the Jordan", "Siala", [
        "https://exarchate-africa.ru/en/news/"
        "the-rector-of-the-parish-of-st-gerasimos-of-the-jordan-in-kenya-"
        "priest-charles-otieno-has-departed-unto-the-lord/"
    ]),
    ru("sio-port-paul", "Parish of the Apostle Paul", "Sio Port", [
        "https://exarchate-africa.ru/novosti/"
        "sostoyalos-sobranie-duhovenstva-na-prihode-apostola-pavla-v-"
        "blagochinii-kakamega-keniya/"
    ]),
    ru("bukura-george", "Parish of the Great Martyr George the Victory-Bearer",
       "Bukura", [
        "https://exarchate-africa.ru/en/news/"
        "metropolitan-konstantin-of-zaraysk-consecrates-a-church-in-kenyan-"
        "village-of-bukura/",
        "https://exarchate-africa.ru/novosti/"
        "priobreten-uchastok-zemli-dlya-prihoda-velikomuchenika-georgiya-"
        "pobedonoscza-v-blagochinii-kakamega-keniya/"
    ]),
    ru("ugundja-anastasia",
       "Parish of the Great Martyr Anastasia the Deliverer from Potions",
       "Ugundja", ["https://exarchate-africa.ru/novosti/"
        "zavershilas-poezdka-patriarshego-ekzarha-afriki-v-keniyu-2/"]),
    ru("lugari-dormition", "Parish of the Dormition of the Most Holy Theotokos",
       "Lugari", ["https://exarchate-africa.ru/novosti/"
        "patriarshij-ekzarh-afriki-posetil-prihody-blagochiniya-lugari-"
        "keniya/"]),
    ru("kaluli-entrance-theotokos",
       "Parish of the Entrance of the Most Holy Theotokos into the Temple",
       "Kaluli", ["https://exarchate-africa.ru/novosti/"
        "zavershilas-poezdka-patriarshego-ekzarha-afriki-v-keniyu-2/"]),
    ru("kirindine-mark", "Parish of the Apostle Mark", "Kirindine", [
        "https://exarchate-africa.ru/novosti/"
        "zavershilas-poezdka-patriarshego-ekzarha-afriki-v-keniyu-2/"
    ]),
    ru("kaongo-archangel-michael",
       "Church of the Archangel Michael and the Other Bodiless Powers",
       "Kaongo", ["https://exarchate-africa.ru/novosti/"
        "zavershilas-poezdka-patriarshego-ekzarha-afriki-v-keniyu-2/"],
       rank="Church Under Construction"),
    ru("kairune-theotokos", "Parish of the Most Holy Theotokos", "Kairune", [
        "https://exarchate-africa.ru/novosti/"
        "v-novogodnyuyu-noch-sovershena-liturgiya-na-prihode-presvyatoj-"
        "bogorodiczy-v-blagochinii-meru-keniya/"
    ]),
    ru("giti-macarius", "Parish of St. Macarius", "Giti", [
        "https://exarchate-africa.ru/novosti/"
        "v-pyatniczu-pervoj-sedmiczy-velikogo-posta-v-blagochinii-meru-"
        "keniya-sovershena-liturgiya-prezhdeosvyashhennyh-darov/"
    ]),
    ru("michiamikuru-john-theologian", "Church of the Apostle John the Theologian",
       "Michiamikuru", ["https://exarchate-africa.ru/en/news/"
        "a-new-temporary-church-built-for-the-growing-orthodox-community-in-"
        "the-kenyan-village-of-michiamikuru/"], rank="Church"),
    ru("mikinduri-john-climacus", "Parish of St. John Climacus", "Mikinduri", [
        "https://exarchate-africa.ru/novosti/"
        "v-nedelyu-vseh-svyatyh-v-voskresnyh-shkolah-v-kenijskom-meru-"
        "proshli-zanyatiya-dlya-detej-i-podrostkov/"
    ]),
    ru("aito-james", "Parish of the Apostle James", "Aito", [
        "https://exarchate-africa.ru/novosti/"
        "sostoyalos-ocherednoe-sobranie-duhovenstva-blagochiniya-meru/"
    ]),
    ru("migori-gregory", "Parish of St. Gregory the Theologian", "Migori", [
        "https://exarchate-africa.ru/novosti/"
        "otoshel-ko-gospodu-nastoyatel-prihoda-svyatitelya-grigoriya-"
        "bogoslova-v-g-migori-keniya-ierej-timofej-opino/"
    ]),
    ru("kamaichkok-irene", "Parish of the Great Martyr Irene", "Kamaichkok", [
        "https://exarchate-africa.ru/novosti/"
        "na-prihode-velikomucheniczy-ekateriny-v-blagochinii-nandi-keniya-"
        "kreshheny-semero-mestnyh-zhitelej/"
    ]),
    ru("matara-catherine", "Parish of the Great Martyr Catherine", "Matara", [
        "https://exarchate-africa.ru/novosti/"
        "na-prihode-velikomucheniczy-ekateriny-v-blagochinii-nandi-keniya-"
        "kreshheny-semero-mestnyh-zhitelej/"
    ]),
    ru("chemobo-stylianos", "Parish of St. Stylianos of Paphlagonia", "Chemobo",
       ["https://exarchate-africa.ru/novosti/"
        "na-prihode-velikomucheniczy-ekateriny-v-blagochinii-nandi-keniya-"
        "kreshheny-semero-mestnyh-zhitelej/"]),
    ru("kibora-luke", "Parish of the Apostle Luke", "Kibora", [
        "https://exarchate-africa.ru/novosti/"
        "sostoyalis-prosvetitelskie-besedy-na-prihode-apostola-luki-v-"
        "kenijskom-blagochinii-nandi/"
    ]),
    ru("sokosik-seraphim", "Parish of St. Seraphim of Sarov", "Sokosik", [
        "https://exarchate-africa.ru/novosti/"
        "priobreten-tent-dlya-prihoda-prepodobnogo-serafima-v-s-sokosik-"
        "keniya/"
    ]),
    ru("serem-vladimir", "Parish of the Equal-to-the-Apostles Prince Vladimir",
       "Serem", ["https://exarchate-africa.ru/novosti/"
        "v-kenijskom-blagochinii-nandi-sostoyalsya-seminar-dlya-"
        "pravoslavnyh-zhenshhin/"]),
    ru("kapsagawat-dormition",
       "Parish of the Dormition of the Most Holy Theotokos", "Kapsagawat", [
        "https://exarchate-africa.ru/novosti/"
        "v-prazdnik-vvedeniya-vo-hram-presvyatoj-bogorodiczy-v-"
        "blagochinii-nandi-keniya-soborno-sovershena-bozhestvennaya-"
        "liturgiya/"
    ]),
    ru("taunet-andrew", "Church of the Apostle Andrew", "Taunet", [
        "https://exarchate-africa.ru/novosti/"
        "duhovno-prosvetitelskij-czentr-apostola-marka-patriarshego-"
        "ekzarhata-afriki-provel-ryad-obrazovatelnyh-meropriyatij-v-"
        "blagochinii-nandi-keniya/"
    ], rank="Church"),
    ru("kirondio-olga",
       "Parish of the Equal-to-the-Apostles Grand Princess Olga", "Kirondio", [
        "https://exarchate-africa.ru/novosti/"
        "v-kenijskom-blagochinii-nandi-sostoyalis-liturgiya-i-sobranie-"
        "soyuza-pravoslavnyh-materej/"
    ]),
    ru("kiamuiru-tryphon", "Parish of the Martyr Tryphon", "Kiamuiru", [
        "https://exarchate-africa.ru/novosti/"
        "na-prihode-muchenika-trifona-v-blagochinii-nieri-keniya-"
        "priobreten-tent-dlya-bogosluzhenij/"
    ]),
    ru("kigoto-maximus", "Parish of St. Maximus the Confessor", "Kigoto", [
        "https://exarchate-africa.ru/novosti/"
        "v-prazdnik-uspeniya-presvyatoj-bogorodiczy-patriarshij-ekzarh-"
        "afriki-sovershil-liturgiyu-v-g-nakuru-keniya/",
        "https://exarchate-africa.ru/novosti/"
        "prazdnik-svetlogo-hristova-voskreseniya-otmetili-na-prihode-sv-"
        "maksima-v-kenii/"
    ]),
    ru("ochiro-macarius-great", "Parish of St. Macarius the Great", "Ochiro", [
        "https://exarchate-africa.ru/novosti/"
        "v-prazdnik-uspeniya-presvyatoj-bogorodiczy-patriarshij-ekzarh-"
        "afriki-sovershil-liturgiyu-v-g-nakuru-keniya/",
        "https://exarchate-africa.ru/novosti/"
        "20-zhitelej-okruga-homa-bej-keniya-prinyali-svyatoe-kreshhenie/"
    ]),
]


# The official Russian pages use inflected forms in prose. These local labels
# preserve their terminology while normalizing the body name to nominative
# case, as elsewhere in the directory.
RU_LOCAL = {
    "ke-ru-nairobi-sergius":
        "Приход в честь преподобного Сергия Радонежского",
    "ke-ru-nyamilu-basil": "Приход святителя Василия Великого",
    "ke-ru-tumaini-john-shanghai":
        "Приход святителя Иоанна Шанхайского",
    "ke-ru-kahuho-nicholas": "Храм святителя Николая Чудотворца",
    "ke-ru-ndenderu-gerasimos":
        "Приход преподобного Герасима Иорданского",
    "ke-ru-panpaper-community": "Община в с. Панпейпер",
    "ke-ru-mlimani-demetrius":
        "Храм великомученика Димитрия Солунского",
    "ke-ru-indagalasia-vladimir":
        "Приход равноапостольного князя Владимира",
    "ke-ru-bukura-mark": "Приход апостола Марка",
    "ke-ru-zimmerman-catherine":
        "Приход великомученицы Екатерины",
    "ke-ru-munzasti-moses-black": "Приход преподобного Моисея Мурина",
    "ke-ru-kaptendje-vladimir":
        "Приход равноапостольного князя Владимира",
    "ke-ru-siyakuti-james-brother":
        "Приход апостола Иакова, брата Господня",
    "ke-ru-sio-port-paul": "Приход апостола Павла",
    "ke-ru-ugundja-anastasia":
        "Приход великомученицы Анастасии Узорешительницы",
    "ke-ru-lugari-dormition":
        "Приход Успения Пресвятой Богородицы",
    "ke-ru-kaluli-entrance-theotokos":
        "Приход в честь праздника Введения во храм Пресвятой Богородицы",
    "ke-ru-kirindine-mark": "Приход апостола Марка",
    "ke-ru-kaongo-archangel-michael":
        "Храм Архистратига Божия Михаила и прочих Небесных Сил бесплотных",
    "ke-ru-kairune-theotokos": "Приход Пресвятой Богородицы",
    "ke-ru-giti-macarius": "Приход святого Макария",
    "ke-ru-mikinduri-john-climacus":
        "Приход преподобного Иоанна Лествичника",
    "ke-ru-aito-james": "Приход апостола Иакова",
    "ke-ru-migori-gregory": "Приход святителя Григория Богослова",
    "ke-ru-kamaichkok-irene": "Приход великомученицы Ирины",
    "ke-ru-matara-catherine": "Приход великомученицы Екатерины",
    "ke-ru-chemobo-stylianos":
        "Приход преподобного Стилиана Пафлагонского",
    "ke-ru-kibora-luke": "Приход апостола Луки",
    "ke-ru-sokosik-seraphim":
        "Приход преподобного Серафима Саровского",
    "ke-ru-serem-vladimir": "Приход равноапостольного Владимира",
    "ke-ru-kapsagawat-dormition":
        "Приход Успения Пресвятой Богородицы",
    "ke-ru-taunet-andrew": "Храм апостола Андрея",
    "ke-ru-kirondio-olga":
        "Приход святой равноапостольной великой княгини Ольги",
    "ke-ru-kiamuiru-tryphon": "Приход в честь мученика Трифона",
    "ke-ru-kigoto-maximus":
        "Приход преподобного Максима Исповедника",
    "ke-ru-ochiro-macarius-great":
        "Приход преподобного Макария Великого",
}
RUSSIAN_ONLY_ROWS = {
    row["id"] for row in RU_ROWS
    if not any("/en/" in url for url in row["sources"])
}
if set(RU_LOCAL) != RUSSIAN_ONLY_ROWS:
    raise ValueError("Russian local-name map is out of sync")
for ru_row in RU_ROWS:
    if ru_row["id"] in RU_LOCAL:
        ru_row["local"] = RU_LOCAL[ru_row["id"]]


ROWS = {
    "ax-nairobi": NAIROBI_ROWS,
    "ax-kisumu": [],
    "ax-nieri": [],
    "ax-eldoret": eldoret_rows(),
    "ru-south-africa": RU_ROWS,
}
EXPECTED = {
    "ax-nairobi": 1,
    "ax-kisumu": 0,
    "ax-nieri": 0,
    "ax-eldoret": 63,
    "ru-south-africa": 80,
}
EXPECTED_TOTAL = 144
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in ROWS.values()
    for row in rows
    if row.get("seat")
}


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    for forbidden in ("bishop", "priest", "clergy", "phone", "email"):
        if forbidden in row:
            raise ValueError("%s carries forbidden personnel or contact data" %
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
            if row.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if row.get("country") != "KE":
                raise ValueError("%s is outside Kenya" % row_id)
            if row.get("kind") != "parish":
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
            "country": "KE",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Kenya must publish exactly %d rows" % EXPECTED_TOTAL)
    if len(ELDORET_LIST) != 63:
        raise ValueError("the current Eldoret roster must contain 63 labels")
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Kenya English name map is out of sync")
    return payloads


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Kenya: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Kenya: 144 current officially named bodies under 5 existing "
          "Alexandrian and Russian diocesan parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
