#!/usr/bin/env python3
"""Validated directory fragments for canonical Eastern Orthodox bodies in the Netherlands.

The parent jurisdictions also carry rows from other countries. This module
therefore emits Netherlands-only fragments for later merging and never writes
a shared payload.

    python tools/directory_netherlands.py --check
    python tools/directory_netherlands.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

EP_PARISHES = (
    "https://orthodoxia.be/nl/parochies/%CE%B9n-nederland/"
)
EP_PARISHES_ALL = "https://orthodoxia.be/nl/parochies/"
EP_MONASTERIES = "https://orthodoxia.be/nl/parochies/40326-2/"
EP_NETHERLANDS = (
    "https://orthodoxekerk.net/parochies/oecumenisch-patriarchaat/"
)
EP_KAMPEN = (
    "https://orthodoxia.be/nl/2024/01/13/"
    "eerste-goddelijke-liturgie-in-kampen-noord-holland/"
)
EP_ELIAS = (
    "https://orthodoxia.be/nl/enoria/"
    "heilige-profeet-elias-klooster-nl-5454-hg/"
)
EP_ASTEN = (
    "https://orthodoxia.be/fr/enoria/"
    "monastere-de-la-nativite-de-la-mere-de-dieu-asten/"
)
EP_HAGUE_MONASTERY = (
    "https://orthodoxia.be/nl/2023/07/03/"
    "patroonsfeest-van-het-klooster-van-de-heilige-johannes-de-doper-"
    "in-den-haag/"
)
EP_BREDA = "https://www.orthodoxekerkbreda.nl/"
EP_MAASTRICHT_GIRDLE = (
    "https://orthodoxia.be/nl/2026/03/10/"
    "eerste-goddelijke-liturgie-in-de-nieuw-opgerichte-parochie-van-de-"
    "heilige-gordel-van-de-moeder-gods-in-maastricht-nederland/"
)
SAINT_SERVATIUS_CONTACT = (
    "https://www.sintservaas.nl/index.php/footer/parochie/Contact_2"
)

ANTIOCH_UTRECHT = "https://rum-orthodox.de/gemeinden/utrecht/"
ANTIOCH_ENSCHEDE = "https://rum-orthodox.de/gemeinden/enschede/"

MOSCOW_PARISHES = (
    "https://russian-diocese.nl/parochies/lijst-van-parochies/"
)
MOSCOW_AMERSFOORT = "https://www.orthodox-amersfoort.nl/"
MOSCOW_SKETE = "https://www.orthodox-amersfoort.nl/page-6/"

ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
ROCOR_NETHERLANDS = (
    "https://orthodoxekerk.net/parochies/russ-orth-kerk-in-het-buitenland/"
)

RUSSIAN_TRADITION = (
    "https://archeveche.eu/en/lieu_type/deanery-of-the-benelux/"
)
RUSSIAN_TRADITION_DEVENTER = (
    "https://archeveche.eu/en/lieux/"
    "parish-of-the-holy-apostles-peter-and-paul/"
)
RUSSIAN_TRADITION_MAASTRICHT = (
    "https://archeveche.eu/de/lieux/"
    "gemeinde-des-heiligen-johannes-chrysostomus-und-des-heiligen-"
    "servatius-de/"
)
RUSSIAN_TRADITION_BONIFACE = (
    "https://archeveche.eu/en/lieux/"
    "saint-boniface-and-saint-xenia-community-of-saint-petersburg/"
)

SERBIAN_BENELUX = "https://dioceseserbe.org/beneluks/"
SERBIAN_OVERVIEW = "https://dioceseserbe.org/eparhija/"
SERBIAN_NETHERLANDS = (
    "https://orthodoxekerk.net/parochies/servisch-orthodoxe-kerk/"
)

ROMANIAN_NETHERLANDS = "https://www.mitropolia.eu/fr/site/177/"
ROMANIAN_OKIN = (
    "https://orthodoxekerk.net/parochies/patriarchaat-van-roemenie/"
)

BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
BULGARIAN_NETHERLANDS = (
    "https://orthodoxekerk.net/parochies/patriarchaat-van-bulgarije/"
)

GEORGIAN_NETHERLANDS = (
    "https://orthodoxekerk.net/parochies/patriarchaat-van-georgie/"
)
GEORGIAN_AALSMEER_HOST = (
    "https://aalsmeer.oudkatholiek.nl/kerkdiensten/"
)
ORTHODOX_BENELUX_MAP = "https://orthodoxconnect.be/kerkkaart"

MACEDONIAN_HOME = "https://www.svetistefan.nl/nl/"
MACEDONIAN_ABOUT = "https://www.svetistefan.nl/nl/over-ons/"
MACEDONIAN_EPARCIES = "https://www.m-p-c.org/?page_id=17"

UOC_PARISH = "https://thetransfiguration.church/"
UOC_SCHEDULE = "https://thetransfiguration.church/rozklad-podij/"
UOC_FOUNDING = (
    "https://uoc-news.church/2023/01/06/"
    "u-kelni-ta-roterdami-vidkrito-novi-gromadi-upc/"
)
UOC_VICARIATE = (
    "https://news.church.ua/2026/02/09/"
    "pro-sluzhinnya-zaxidnojevropejskogo-vikariatstva-"
    "ukrajinskoji-pravoslavnoji-cerkvi/"
)


def row(row_id, parent, name, local, sources, rank="Parish", kind="parish",
        address=None, site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "NL",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


ROWS = {
    "ep-belgium": [
        row(
            "nl-ep-rotterdam-saint-nicholas-cathedral", "ep-belgium",
            "St Nicholas Cathedral in Rotterdam",
            "Kathedraal van de Heilige Nikolaas",
            [EP_PARISHES, EP_NETHERLANDS], rank="Cathedral",
            address=["Westzeedijk 333", "3015 AA Rotterdam, Netherlands"],
        ),
        row(
            "nl-ep-amsterdam-saint-nicholas-myra", "ep-belgium",
            "St Nicholas of Myra Parish in Amsterdam",
            "Parochie van de Heilige Nikolaas van Myra",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Lijnbaansgracht 47-48", "1015 GR Amsterdam, Netherlands"],
            site="https://orthodox-amsterdam.nl",
        ),
        row(
            "nl-ep-zaandam-saint-catherine", "ep-belgium",
            "St Catherine Parish in Zaandam",
            "Parochie van de Heilige Katerina",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Botenmakersstraat 114", "1506 TH Zaandam, Netherlands"],
        ),
        row(
            "nl-ep-alkmaar-nativity-theotokos-adalbert", "ep-belgium",
            "Nativity of the Mother of God and St Adalbert Parish in Alkmaar",
            "Parochie van de Geboorte van de Moeder Gods en van de Heilige Adalbert",
            [EP_PARISHES, EP_PARISHES_ALL],
            site="https://orthodox-alkmaar.nl",
        ),
        row(
            "nl-ep-hague-james-paraskeva", "ep-belgium",
            "St James the Greater and St Paraskeva of Epivata Parish in The Hague",
            "Parochie van de Heilige Apostel Jacobus de Meerdere en de Heilige Paraskeva van Epivata",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Juffrouw Idastraat 13", "2513 BE Den Haag, Netherlands"],
            site="http://www.orthodoxdenhaag.nl",
        ),
        row(
            "nl-ep-utrecht-annunciation", "ep-belgium",
            "Annunciation of the Mother of God Parish in Utrecht",
            "Parochie van de Verkondiging aan de Moeder Gods",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Springweg 89", "3511 VL Utrecht, Netherlands"],
            site="https://utrecht-orthodox.nl",
        ),
        row(
            "nl-ep-voorthuizen-faneromeni", "ep-belgium",
            "Faneromeni Icon of the Mother of God Parish in Voorthuizen",
            "Parochie van de Moeder Gods Faneromeni",
            [EP_PARISHES],
        ),
        row(
            "nl-ep-gorinchem-maximos-confessor", "ep-belgium",
            "St Maximos the Confessor Parish in Gorinchem",
            "Parochie van de Heilige Maximos de Belijder",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Stalkaarsen 19", "4205 PG Gorinchem, Netherlands"],
            site="https://orthodox-gorinchem.blogspot.com",
        ),
        row(
            "nl-ep-tilburg-saint-porphyrios", "ep-belgium",
            "St Porphyrios Parish in Tilburg",
            "Orthodoxe Parochie van de Heilige Porfyrios",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Abdij Koningshoeven", "Eindhovenseweg 3",
                     "5056 RP Berkel-Enschot, Netherlands"],
            site="https://www.orthodoxtilburg.nl",
        ),
        row(
            "nl-ep-eindhoven-saint-nectarios", "ep-belgium",
            "St Nectarios of Aegina Parish in Eindhoven",
            "Parochie van de Heilige Nektarios van Egina",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Hoogstraat 301A", "5654 NB Eindhoven, Netherlands"],
            site="https://www.orthodox-eindhoven.nl",
        ),
        row(
            "nl-ep-venlo-faneromeni", "ep-belgium",
            "Faneromeni Icon of the Mother of God Parish in Venlo",
            "Parochie van de Moeder Gods Faneromeni",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Grote Kerkstraat 26", "5911 CH Venlo, Netherlands"],
        ),
        row(
            "nl-ep-maastricht-holy-girdle-theotokos", "ep-belgium",
            "Holy Girdle of the Mother of God Parish in Maastricht",
            "Parochie van de Heilige Gordel van de Moeder Gods",
            [EP_MAASTRICHT_GIRDLE, SAINT_SERVATIUS_CONTACT,
             ORTHODOX_BENELUX_MAP],
            address=["Basiliek van Sint Servaas", "Keizer Karelplein 3",
                     "6211 TC Maastricht, Netherlands"],
        ),
        row(
            "nl-ep-breda-myrrhbearers", "ep-belgium",
            "Holy Myrrhbearers Parish in Breda",
            "Orthodoxe Parochie van de Heilige Myrondraagsters",
            [EP_PARISHES_ALL, EP_NETHERLANDS, EP_BREDA],
            address=["Kerkhofkapel", "Vogelenzanglaan 21",
                     "Breda-Ginneken, Netherlands"],
            site=EP_BREDA,
        ),
        row(
            "nl-ep-nijmegen-saint-theophano", "ep-belgium",
            "St Theophano Parish in Nijmegen",
            "Parochie van de Heilige Theofano",
            [EP_PARISHES, EP_NETHERLANDS],
            address=["Byzantijnse Kapel", "Dobbelmannweg 3",
                     "6531 KT Nijmegen, Netherlands"],
            site="https://www.orthodoxe-parochie-nijmegen.nl",
        ),
        row(
            "nl-ep-zwolle-anthony-theodosius", "ep-belgium",
            "Saints Anthony and Theodosius of the Kiev Caves Community in Zwolle",
            "Gemeenschap van de Heiligen Antonius en Theodosius van Kiev-Pechersk",
            [EP_PARISHES], rank="Community",
        ),
        row(
            "nl-ep-kampen-saint-boniface", "ep-belgium",
            "St Boniface Community in Kampen",
            "Gemeenschap van de Heilige Bonifatius",
            [EP_PARISHES, EP_PARISHES_ALL, EP_KAMPEN], rank="Community",
            site="https://www.orthodoxkampen.nl",
        ),
        row(
            "nl-ep-assen-community", "ep-belgium",
            "Orthodox Community in Assen",
            "Gemeenschap van Assen (Drenthe)",
            [EP_PARISHES], rank="Community",
        ),
        row(
            "nl-ep-asten-nativity-theotokos-monastery", "ep-belgium",
            "Nativity of the Mother of God Monastery in Asten",
            "Klooster van de Geboorte van de Moeder Gods",
            [EP_MONASTERIES, EP_ASTEN, EP_NETHERLANDS],
            rank="Monastery", kind="monastery",
            address=["Gruttoweg 7", "5725 RT Heusden-Asten, Netherlands"],
            site="https://www.orthodoxasten.nl",
        ),
        row(
            "nl-ep-sint-hubert-prophet-elias-monastery", "ep-belgium",
            "Holy Prophet Elias Monastery in Sint Hubert",
            "Klooster van de Heilige Profeet Elias",
            [EP_MONASTERIES, EP_ELIAS, EP_NETHERLANDS],
            rank="Monastery", kind="monastery",
            address=["Nimrod 15", "5454 HG Sint Hubert, Netherlands"],
            site="https://www.eliasklooster.nl",
        ),
        row(
            "nl-ep-hague-john-forerunner-monastery", "ep-belgium",
            "Nativity of St John the Forerunner Monastery in The Hague",
            "Klooster van de Geboorte van de Heilige Johannes de Voorloper",
            [EP_MONASTERIES, EP_HAGUE_MONASTERY, EP_NETHERLANDS],
            rank="Monastery", kind="monastery",
            address=["Dr. Kuyperstraat 2", "2514 BB Den Haag, Netherlands"],
            site="https://www.johannesdevoorloper.nl",
        ),
    ],
    "an-germany": [
        row(
            "nl-antioch-de-bilt-mother-of-god", "an-germany",
            "Mother of God Parish in De Bilt",
            "Gemeente Moeder Gods Parochie",
            [ANTIOCH_UTRECHT],
            address=["Kerklaan 31", "3731 EE De Bilt, Netherlands"],
        ),
        row(
            "nl-antioch-enschede-anthony-great", "an-germany",
            "St Anthony the Great Parish in Enschede",
            "Gemeente Antonius de Grote Parochie",
            [ANTIOCH_ENSCHEDE],
            address=["Vlierstraat 93", "7544 GG Enschede, Netherlands"],
        ),
    ],
    "ru-hague-and-the-netherlands": [
        row(
            "nl-mp-rotterdam-alexander-nevsky", "ru-hague-and-the-netherlands",
            "St Alexander Nevsky Parish in Rotterdam",
            "Parochie van de Heilige rechtgelovige grootvorst Alexander Nevskij",
            [MOSCOW_PARISHES],
            address=["Schiedamsesingel 220", "3012 BA Rotterdam, Netherlands"],
            site="https://www.ruskerk.nl",
        ),
        row(
            "nl-mp-amsterdam-sergius-radonezh", "ru-hague-and-the-netherlands",
            "St Sergius of Radonezh Parish in Amsterdam",
            "Parochie van de Heilige Sergius van Radonezj",
            [MOSCOW_PARISHES],
            address=["Veluwelaan 22", "1079 RA Amsterdam, Netherlands"],
            site="https://www.ruskerkamsterdam.nl",
        ),
        row(
            "nl-mp-hague-mary-magdalene", "ru-hague-and-the-netherlands",
            "St Mary Magdalene Parish in The Hague",
            "Parochie van de Heilige Maria Magdalena",
            [MOSCOW_PARISHES],
            address=["Obrechtstraat 9", "2517 VL Den Haag, Netherlands"],
            site="https://www.ruskerkdenhaag.nl",
        ),
        row(
            "nl-mp-amersfoort-cornelius-centurion", "ru-hague-and-the-netherlands",
            "St Cornelius the Centurion Parish in Amersfoort",
            "Parochie van de Heilige Cornelius de Honderdman",
            [MOSCOW_PARISHES, MOSCOW_AMERSFOORT],
            address=["Matthias Withoosstraat 34",
                     "3812 ST Amersfoort, Netherlands"],
            site=MOSCOW_AMERSFOORT,
        ),
        row(
            "nl-mp-amersfoort-holy-cross-skete",
            "nl-mp-amersfoort-cornelius-centurion",
            "Holy Cross Women's Skete in Amersfoort",
            "Orthodoxe Vrouwenklooster van het Heilig Kruis",
            [MOSCOW_SKETE, ORTHODOX_BENELUX_MAP],
            rank="Skete", kind="monastery",
            address=["Matthias Withoosstraat 34",
                     "3812 ST Amersfoort, Netherlands"],
            site=MOSCOW_SKETE,
        ),
        row(
            "nl-mp-groningen-transfiguration", "ru-hague-and-the-netherlands",
            "Holy Transfiguration Parish in Groningen",
            "Parochie van de Heilige Transfiguratie",
            [MOSCOW_PARISHES],
            address=["Ganzevoortsingel 2", "9711 AL Groningen, Netherlands"],
        ),
        row(
            "nl-mp-nijmegen-saint-tikhon", "ru-hague-and-the-netherlands",
            "St Tikhon, Patriarch of Moscow, Parish in Nijmegen",
            "Parochie van de Heilige Tichon Patriarch van Moskou",
            [MOSCOW_PARISHES],
            address=["Byzantijnse Kapel", "Dobbelmanweg 3",
                     "6531 KT Nijmegen, Netherlands"],
            site="https://www.orthodox-nijmegen.nl",
        ),
        row(
            "nl-mp-zwolle-archangel-michael", "ru-hague-and-the-netherlands",
            "Archangel Michael Parish in Zwolle",
            "Parochie van de Heilige Aartsengel Michael",
            [MOSCOW_PARISHES],
            address=["Theodorahof 20", "8011 AA Zwolle, Netherlands"],
            site="https://www.orthodoxekerkzwolle.nl",
        ),
        row(
            "nl-mp-leeuwarden-john-baptist", "ru-hague-and-the-netherlands",
            "St John the Baptist Parish in Leeuwarden",
            "Parochie van Heilige Johannes de Doper",
            [MOSCOW_PARISHES],
            address=["De Hooidollen 17", "8918 HV Leeuwarden, Netherlands"],
            site="https://www.orthodoxekerkleeuwarden.nl",
        ),
        row(
            "nl-mp-hemelum-saint-nicholas-monastery", "ru-hague-and-the-netherlands",
            "St Nicholas of Myra Monastery in Hemelum",
            "Klooster van de Heilige Nikolaas van Myra",
            [MOSCOW_PARISHES], rank="Monastery", kind="monastery",
            address=["Buorren 18", "8584 VC Hemelum, Netherlands"],
            site="https://www.kloosterhemelum.nl",
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "nl-rocor-aalsmeer-mary-egypt",
            "ru-great-britain-and-western-europe-rocor",
            "St Mary of Egypt Parish in Aalsmeer",
            "Heilige Maria van Egypte",
            [ROCOR_DIRECTORY, ROCOR_NETHERLANDS],
            address=["Oud-Katholieke Kerk", "Oosteinderweg 394",
                     "1432 BG Aalsmeer, Netherlands"],
            site="https://www.hmvekerk.nl",
        ),
        row(
            "nl-rocor-arnhem-protection-theotokos",
            "ru-great-britain-and-western-europe-rocor",
            "Protection of the Mother of God Parish in Arnhem",
            "Parochie Moeder Gods Bescherming",
            [ROCOR_DIRECTORY, ROCOR_NETHERLANDS],
            address=["Amsterdamseweg 96", "6814 GG Arnhem, Netherlands"],
        ),
        row(
            "nl-rocor-maastricht-apostle-thomas-mission",
            "ru-great-britain-and-western-europe-rocor",
            "Holy Apostle Thomas Mission in Maastricht",
            "Missie van de H. Apostel Thomas",
            [ROCOR_DIRECTORY, ROCOR_NETHERLANDS], rank="Mission",
            address=["Einsteinstraat 60", "6227 BZ Maastricht, Netherlands"],
        ),
    ],
    "ru-archdiocese-western-europe": [
        row(
            "nl-russian-tradition-deventer-peter-paul",
            "ru-archdiocese-western-europe",
            "Holy Apostles Peter and Paul Parish in Deventer",
            "Parish of the Holy Apostles Peter and Paul",
            [RUSSIAN_TRADITION, RUSSIAN_TRADITION_DEVENTER],
            address=["Korte Assenstraat 13", "7411 JP Deventer, Netherlands"],
        ),
        row(
            "nl-russian-tradition-maastricht-john-servatius",
            "ru-archdiocese-western-europe",
            "St John Chrysostom and St Servatius Parish in Maastricht",
            "Parish of Saint John Chrysostom and Saint Servatius",
            [RUSSIAN_TRADITION, RUSSIAN_TRADITION_MAASTRICHT],
            address=["St. Maartenslaan 37", "6221 AW Maastricht, Netherlands"],
        ),
        row(
            "nl-russian-tradition-deventer-boniface-xenia-community",
            "ru-archdiocese-western-europe",
            "St Boniface and St Xenia of St Petersburg Community in Deventer",
            "Saint Boniface and Saint Xenia Community of Saint Petersburg",
            [RUSSIAN_TRADITION, RUSSIAN_TRADITION_BONIFACE],
            rank="Community",
            address=["Metzelaarplein 3", "7416 BV Deventer, Netherlands"],
        ),
    ],
    "sr-western-europe": [
        row(
            "nl-serbian-rotterdam-holy-trinity", "sr-western-europe",
            "Holy Trinity Parish in Rotterdam",
            "Парохија Свете Тројице",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Lede 121", "3075 HH Rotterdam, Netherlands"],
            site="https://www.svetatrojicaroterdam.com/",
        ),
        row(
            "nl-serbian-zaandam-saint-nicholas", "sr-western-europe",
            "St Nicholas Parish in Zaandam",
            "Парохија Светог Николе",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Stationsstraat 13", "1506 DA Zaandam, Netherlands"],
            site="https://www.svetinikolaamsterdam.com/",
        ),
        row(
            "nl-serbian-emmer-compascuum-nativity-theotokos",
            "sr-western-europe",
            "Nativity of the Most Holy Theotokos Parish in Emmer-Compascuum",
            "Парохија Рођења Пресвете Богородице",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Middenweg Oostzijde 5",
                     "7881 XG Emmer-Compascuum, Netherlands"],
        ),
        row(
            "nl-serbian-zeist-simeon-myrrhstreaming", "sr-western-europe",
            "St Simeon the Myrrh-Streaming Parish in Zeist",
            "Парохија Светог Симеона Мироточивог",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Woudenbergseweg 38", "3701 BC Zeist, Netherlands"],
            site="https://www.svetisimeonutrecht.com/",
        ),
        row(
            "nl-serbian-ritthem-john-theologian", "sr-western-europe",
            "St John the Theologian Parish in Ritthem",
            "Парохија Светог Јован Богослова",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Weverstraat 9", "4389 TR Ritthem, Netherlands"],
        ),
        row(
            "nl-serbian-breda-nectarios-aegina", "sr-western-europe",
            "St Nectarios of Aegina Parish in Breda",
            "Парохија Светог Нектарија Егинског",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Mattheuskerk", "Steendorpstraat 4",
                     "4826 EP Breda, Netherlands"],
            site="https://www.svetinektarijeeginski.com/",
        ),
        row(
            "nl-serbian-breda-saint-anna-chapel",
            "nl-serbian-breda-nectarios-aegina",
            "St Anna Chapel in Breda", "Sint Annakapel",
            [SERBIAN_BENELUX], rank="Chapel",
            address=["Heusdenhoutseweg 34", "4817 NC Breda, Netherlands"],
        ),
        row(
            "nl-serbian-helmond-saint-demetrius", "sr-western-europe",
            "St Demetrius Parish in Helmond",
            "Парохија Светог Димитрија",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Hornestraat 1", "5707 TM Helmond, Netherlands"],
        ),
        row(
            "nl-serbian-haalderen-saint-sava", "sr-western-europe",
            "St Sava Parish in Haalderen", "Парохија Светог Саве",
            [SERBIAN_BENELUX, SERBIAN_NETHERLANDS],
            address=["Van der Mondeweg 24", "6685 BP Haalderen, Netherlands"],
            site="https://www.spc-nijmegen.nl/",
        ),
        row(
            "nl-serbian-enschede-protection-theotokos", "sr-western-europe",
            "Protection of the Most Holy Theotokos Parish in Enschede",
            "Парохија Покрова Пресвете Богородице",
            [SERBIAN_OVERVIEW, SERBIAN_NETHERLANDS],
            address=["Johanneskerk", "Twekkelerweg 110",
                     "7547 RN Enschede, Netherlands"],
        ),
    ],
    "ro-western-europe": [
        row(
            "nl-ro-heemstede-john-chrysostom", "ro-western-europe",
            "St John Chrysostom Parish in Heemstede",
            "Parohia Sf. Ioan Gură de Aur",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Valkerburgerplein 20", "2103 AT Heemstede, Netherlands"],
        ),
        row(
            "nl-ro-rucphen-martin-ephraim", "ro-western-europe",
            "St Martin of Tours and St Ephraim the New Parish in Rucphen",
            "Parohia Sf. Ierarh Martin de Tours și Sf. Cuv. și Mart. Efrem cel Nou",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Sint-Martinuskerk", "Raadhuisstraat 3",
                     "4715 CB Rucphen, Netherlands"],
        ),
        row(
            "nl-ro-megen-basil-ludger", "ro-western-europe",
            "St Basil the Great and St Ludger Parish in Megen",
            "Parohia Sf. Vasile cel Mare și Sf. Ludger",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Schoolstraat 1", "5366 AT Megen, Netherlands"],
        ),
        row(
            "nl-ro-berkel-enschot-parascheva", "ro-western-europe",
            "St Paraskeva of Iasi Parish in Berkel-Enschot",
            "Parohia Sf. Cuvioasă Parascheva de la Iași",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Sint Willibrordstraat 1",
                     "5056 HS Berkel-Enschot, Netherlands"],
        ),
        row(
            "nl-ro-s-heer-abtskerke-anastasia", "ro-western-europe",
            "St Anastasia Parish in 's-Heer Abtskerke",
            "Parohia Sf. Mare Mucenică Anastasia",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Kerkring 1", "4444 AB 's-Heer Abtskerke, Netherlands"],
            site="https://www.bisericazeeland.nl/",
        ),
        row(
            "nl-ro-middelbert-john-evangelist", "ro-western-europe",
            "St John the Apostle and Evangelist Parish in Middelbert",
            "Parohia Sf. Apostol și Evanghelist Ioan",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Middelberterweg 13", "9723 ET Middelbert, Netherlands"],
            site="https://www.bisericagroningen.nl/",
        ),
        row(
            "nl-ro-schiedam-gregory-maria-brancoveanu",
            "ro-western-europe",
            "St Gregory the Theologian and St Maria Brancoveanu Parish in Schiedam",
            "Parohia Sf. Grigorie Teologul și Sfânta Doamnă Maria Brâncoveanu",
            [ROMANIAN_NETHERLANDS, ROMANIAN_OKIN],
            address=["Vlaardingerdijk 48", "3117 EW Schiedam, Netherlands"],
        ),
    ],
    "bg-western-central-europe": [
        row(
            "nl-bg-hague-paisius-archangels", "bg-western-central-europe",
            "St Paisius of Hilendar and Holy Archangels Michael and Gabriel Parish in The Hague",
            "БПЦО Св. преподобни Паисий Хилендарски и Св. Архангели Михаил и Гавраил",
            [BULGARIAN_DIRECTORY, BULGARIAN_NETHERLANDS,
             "https://www.bgorthodoxekerk.nl/"],
            address=["Bakkerstraat 57A", "2513 TJ Den Haag, Netherlands"],
            site="https://www.bgorthodoxekerk.nl/",
        ),
    ],
    "ge-belgium-holland": [
        row(
            "nl-ge-aalsmeer-exaltation-cross", "ge-belgium-holland",
            "Exaltation of the Holy Cross Parish in Aalsmeer",
            "Parochie Verheerlijking van het Kruis",
            [GEORGIAN_NETHERLANDS, GEORGIAN_AALSMEER_HOST,
             ORTHODOX_BENELUX_MAP],
            address=["Oosteinderweg 394", "1432 BG Aalsmeer, Netherlands"],
        ),
        row(
            "nl-ge-hague-john-baptist", "ge-belgium-holland",
            "St John the Baptist Parish in The Hague",
            "Parochie van de Heilige Johannes de Doper",
            [GEORGIAN_NETHERLANDS, ORTHODOX_BENELUX_MAP],
            address=["Bakkerstraat 57A", "2513 TJ Den Haag, Netherlands"],
        ),
    ],
    "mk-europe": [
        row(
            "nl-macedonian-rossum-saint-stephen", "mk-europe",
            "St Stephen Macedonian Orthodox Church Community in Rossum",
            "МПЦ ОА Свети Стефан",
            [MACEDONIAN_HOME, MACEDONIAN_ABOUT, MACEDONIAN_EPARCIES],
            rank="Church Community",
            address=["H.C. de Jonghweg 2", "5328 JD Rossum, Netherlands"],
            site=MACEDONIAN_HOME,
        ),
    ],
    "ukraine-uoc": [
        row(
            "nl-uoc-rotterdam-transfiguration", "ukraine-uoc",
            "Transfiguration of the Lord Parish in Rotterdam",
            "Свято-Преображенська парафія міста Роттердам",
            [UOC_PARISH, UOC_FOUNDING, UOC_VICARIATE],
            address=["Andreaskerk", "Heer Vrankestraat 51",
                     "3036 LB Rotterdam, Netherlands"],
            site=UOC_PARISH,
        ),
        row(
            "nl-uoc-vlaardingen-hoflaankerk-worship-site",
            "nl-uoc-rotterdam-transfiguration",
            "Hoflaankerk Worship Site in Vlaardingen",
            "Remonstrantse Kerk Hoflaankerk",
            [UOC_PARISH, UOC_SCHEDULE], rank="Worship Site",
            address=["Hoflaan 39", "3134 AB Vlaardingen, Netherlands"],
        ),
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "an-germany": 2,
    "bg-western-central-europe": 1,
    "ep-belgium": 20,
    "ge-belgium-holland": 2,
    "mk-europe": 1,
    "ro-western-europe": 7,
    "ru-archdiocese-western-europe": 3,
    "ru-great-britain-and-western-europe-rocor": 3,
    "ru-hague-and-the-netherlands": 10,
    "sr-western-europe": 10,
    "ukraine-uoc": 2,
}


PROHIBITED_PUNCTUATION = {"\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d"}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def clean(source):
    out = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("address") and (not isinstance(out["address"], list) or
                               not all(isinstance(line, str)
                                       for line in out["address"])):
        raise ValueError("%s has an invalid address" % out.get("id"))
    return out


def build():
    spine = json.loads((ROOT / "data" / "directory.v1.json").read_text(
        encoding="utf-8"))
    spine_ids = {item["id"] for item in spine["rows"]}
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"parish", "monastery"}
    for parent, source_rows in ROWS.items():
        if parent not in spine_ids:
            raise ValueError("unknown directory spine parent: %s" % parent)
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen or row_id in spine_ids:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not row_id.startswith("nl-"):
                raise ValueError("%s lacks the Netherlands id prefix" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") not in allowed_kinds:
                raise ValueError("%s has unsupported kind: %s" %
                                 (row_id, item.get("kind")))
            if item.get("country") != "NL":
                raise ValueError("%s is outside the Netherlands" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            for value in strings(item):
                marks = PROHIBITED_PUNCTUATION.intersection(value)
                if marks:
                    raise ValueError("%s carries prohibited punctuation: %r" %
                                     (row_id, sorted(marks)))
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "NL",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Netherlands parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 61:
        raise ValueError("Netherlands English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": ["NL"],
        }
        for parent, payload in sorted(payloads.items())
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
        print("directory Netherlands: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Netherlands branches: 61 rows")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
