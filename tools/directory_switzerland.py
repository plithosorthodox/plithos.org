#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Switzerland.

The official-source union preserves overlapping canonical structures without
preferring one jurisdiction. This module emits Switzerland-only fragments for
later merging and never writes a shared payload.

    python tools/directory_switzerland.py --check
    python tools/directory_switzerland.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

EP_DIRECTORY = "https://ec-patr.org/entities/iera-mitropoli-elvetias/"
EP_CENTRE = "https://centreorthodoxe.org/eglise-saint-paul/"
EP_FRIBOURG = "https://orthodoxie.ch/p/fribourg-protection/"
EP_CHAVORNAY = "https://orthodoxie.ch/p/chavornay/"
EP_SWISS_DIRECTORY = "https://orthodoxie.ch/de/deutsch/verzeichnis/"

ROMANIAN_PARISHES = "https://www.mitropolia.eu/ro/site/172/"
ROMANIAN_MONASTERIES = "https://www.mitropolia.eu/ro/site/351/"

ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)

SERBIAN_EPARChY = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/"
    "14168.bratski-sastanak-svestenstva-eparhije-svajcarske.html"
)
SERBIAN_WEST = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/"
    "16295.episkop-andrej-posetio-parohije-u-zapadnoj-svajcarskoj.html"
)
SERBIAN_BASEL = "https://www.spc.rs/sr/news/16906.slava-parohije-svih-svetih-u-bazelu.html"
SERBIAN_BERN = (
    "https://spc.rs/sr/news/14094.vladika-andrej-sveti-kirilo-i-metodije-"
    "%E2%80%93-primer-misionarske-revnosti%2C-molitvene-istrajnosti-i-"
    "ljubavi-prema-crkvi.html"
)
SERBIAN_ST_GALLEN = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/"
    "13890.vladika-andrej-vera-je-zivi-odnos-sa-vaskrslim-hristom-"
    "ispunjen-ljubavlju%2C-nadom-i-poverenjem.html"
)
SERBIAN_ZURICH = (
    "https://www.spc.rs/sr/news/iz-zivota-crkve/-/"
    "14694.cirih-dvadeset-godina-parohije-uspenja-presvete-bogorodice.html"
)

MOSCOW_SWITZERLAND = "https://www.egliserusse.eu/Paroisses-et-communautes-en-Suisse_r30.html"
MOSCOW_PLACES = "https://www.egliserusse.eu/Lieux-de-culte_r2.html"
MOSCOW_EXARCHATE = "https://patriarchia.ru/church/orgs/exarchates/org/543"
MOSCOW_ROVEREDO = "https://eparchia.patriarchia.ru/article/123116"
MOSCOW_MELIDE = "https://eparchia.patriarchia.ru/article/123462"
MOSCOW_ZURICH = "https://patriarchia.ru/en/document/120725"
MOSCOW_SAINT_MAURICE = (
    "https://www.egliserusse.eu/La-chapelle-Saint-Jacques-appartenant-a-l-"
    "abbaye-Saint-Maurice-canton-suisse-du-Valais-a-ete-transmise-au-"
    "diocese-de_a1654.html"
)

BULGARIAN_GENEVA = (
    "https://bg-patriarshia.bg/news/"
    "praznik-na-balgarskata-tsarkovna-obshtina-rozhdestvo-bogorod"
)
BULGARIAN_ZURICH = (
    "https://bg-patriarshia.bg/news/"
    "most-na-vyarata-balgarskata-pravoslavna-tsarkovna-obshtina-v"
)
BULGARIAN_ZURICH_VISIT = (
    "https://bg-patriarshia.bg/news/"
    "arhiereyska-sv-liturgia-na-chetvartata-nedelya-ot-velikia-po"
)

MACEDONIAN_DIRECTORY = "https://mpee.mk/category/juzno-evropsko-namesnistvo-2"
MACEDONIAN_COUNT = "https://mpee.mk/?page=9"

UOC_SWITZERLAND = (
    "https://uoc-news.church/2023/05/03/"
    "keruyuchij-parafiyami-upc-zakordonom-vidvidav-ukrajinski-"
    "cerkovni-gromadi-u-shvejcariji/"
)
UOC_ZURICH = (
    "https://uoc-news.church/2023/12/29/"
    "keruyuchij-zaxidnojevropejskim-vikariatstvom-vidvidav-"
    "parafiji-u-shvejcariji-nimechchini-ta-portugaliji/"
)
GEORGIAN_SYNOD = "https://patriarchate.ge/sinodi/members/all"
GEORGIAN_DIOCESE = "https://www.facebook.com/weudiocese.georgia"
GEORGIAN_HISTORY = (
    "https://orthodoxcanada.ca/"
    "Patriarch_Ilia_II_%28Ghudushauri-Shiolashvili%29"
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
        "country": "CH",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


SPINE_ROW_PROPOSALS = {
    "ge-western-europe": {
        "id": "ge-western-europe",
        "parent": "georgia",
        "kind": "diocese",
        "rank": "Eparchy",
        "name": "Eparchy of Western Europe",
        "local": "დასავლეთ ევროპის ეპარქია",
        "seat": "Paris",
        "country": "FR",
        "site": GEORGIAN_DIOCESE,
        "sources": [GEORGIAN_SYNOD, GEORGIAN_DIOCESE, GEORGIAN_HISTORY],
        "cite": [GEORGIAN_SYNOD, GEORGIAN_DIOCESE, GEORGIAN_HISTORY],
        "checked": CHECKED,
    },
}


ROWS = {
    "ep-switzerland": [
        row(
            "ch-ep-chambesy-apostle-paul", "ep-switzerland",
            "Holy Apostle Paul Parish in Chambesy",
            "Ἐνορία Ἀποστόλου Παύλου Γενεύης",
            [EP_DIRECTORY, EP_CENTRE],
            address=["Chemin des Cornillons 12", "1292 Chambésy GE"],
            site=EP_CENTRE,
        ),
        row(
            "ch-ep-chambesy-catherine-trinity", "ep-switzerland",
            "Saint Catherine and Holy Trinity Parish in Chambesy",
            "Ἐνορία Ἁγίας Αἰκατερίνης-Ἁγίας Τριάδος Γενεύης",
            [EP_DIRECTORY],
            address=["Chemin des Cornillons 12", "1292 Chambésy GE"],
            site="https://www.saintecatherine.ch/",
        ),
        row(
            "ch-ep-chene-bourg-john-forerunner", "ep-switzerland",
            "Nativity of Saint John the Forerunner Romanian-Speaking Parish in Chene-Bourg",
            "Ἐνορία Γενεσίου Τιμίου Προδρόμου Γενεύης",
            [EP_DIRECTORY],
            address=["Chemin du Bois des Arts 43-45", "1225 Chêne-Bourg"],
        ),
        row(
            "ch-ep-lausanne-saint-gerasimos", "ep-switzerland",
            "Saint Gerasimos Parish in Lausanne",
            "Ἐνορία Ἁγίου Γερασίμου Λωζάννης",
            [EP_DIRECTORY], address=["Avenue Florimont 2", "1006 Lausanne"],
        ),
        row(
            "ch-ep-fribourg-protection-silouan", "ep-switzerland",
            "Protection of the Mother of God and Saint Silouan the Athonite Parish in Fribourg",
            "Paroisse de la Protection de la Mère de Dieu et de Saint Silouane l'Athonite",
            [EP_DIRECTORY, EP_FRIBOURG],
            address=["Rue du Botzet 2", "1700 Fribourg"],
        ),
        row(
            "ch-ep-chavornay-nativity-theotokos", "ep-switzerland",
            "Nativity of the Mother of God Parish in Chavornay",
            "Paroisse de la Nativité de la Mère de Dieu",
            [EP_DIRECTORY, EP_CHAVORNAY],
            address=["Chemin de la Ville 2", "1373 Chavornay"],
            site="https://nativitedelamerededieu.ch/",
        ),
        row(
            "ch-ep-bern-presentation-theotokos", "ep-switzerland",
            "Presentation of the Mother of God Parish in Bern",
            "Ἐνορία Εἰσοδίων τῆς Θεοτόκου Βέρνης",
            [EP_DIRECTORY],
            address=["Inselspital chapels", "3010 Bern"],
        ),
        row(
            "ch-ep-zurich-saint-demetrios", "ep-switzerland",
            "Saint Demetrios Parish in Zurich",
            "Ἐνορία Ἁγίου Δημητρίου Ζυρίχης",
            [EP_DIRECTORY], address=["Rousseaustrasse 17", "8037 Zürich"],
        ),
        row(
            "ch-ep-st-gallen-constantine-helen", "ep-switzerland",
            "Saints Constantine and Helen Parish of Eastern Switzerland and Liechtenstein in St Gallen",
            "Ἐνορία Ἁγίων Κωνσταντίνου καί Ἑλένης Ἀνατολικῆς Ἑλβετίας καί Πριγκηπάτου τοῦ Liechtenstein",
            [EP_DIRECTORY], address=["Feldlistrasse 18", "9000 St Gallen"],
        ),
        row(
            "ch-ep-munchenstein-holy-wisdom", "ep-switzerland",
            "Holy Wisdom Parish of Basel and Northwestern Switzerland in Munchenstein",
            "Ἐνορία τῆς τοῦ Θεοῦ Σοφίας Βασιλείας-Βορειοδυτικῆς Ἑλβετίας",
            [EP_DIRECTORY], address=["Gladiolenstrasse 2", "4142 Münchenstein"],
            site="https://www.agiasofia.ch/",
        ),
        row(
            "ch-ep-olten-saint-george", "ep-switzerland",
            "Saint George Parish in Olten", "Ἐνορία Ἁγίου Γεωργίου Olten",
            [EP_DIRECTORY], address=["Kapuzinerkloster", "4600 Olten"],
        ),
        row(
            "ch-ep-magenwil-nativity-calinic-paisios", "ep-switzerland",
            "Nativity of the Mother of God, Saint Calinic of Cernica, and Saint Paisios Parish in Magenwil",
            "Ἐνορία Γενεσίου τῆς Θεοτόκου, Ἁγίου Καλλινίκου Τσερνίκας καί Ὁσίου Παϊσίου τοῦ Ἁγιορείτου",
            [EP_DIRECTORY, EP_SWISS_DIRECTORY],
            address=["Hauptstrasse 26", "5506 Mägenwil"],
            site="http://www.bisericaortodoxabaden.ch/",
        ),
        row(
            "ch-ep-bissone-theophany-nektarios", "ep-switzerland",
            "Theophany and Saint Nektarios Parish of Ticino in Bissone",
            "Ἐνορία τῶν Ἐπιφανείων καί τοῦ Ἁγίου Νεκταρίου Τιτσίνου",
            [EP_DIRECTORY],
            address=["Piazza Francesco Borromini 1-3", "6816 Bissone"],
            site="https://comunita-ellenica.ch/it/parrocchia/",
        ),
        row(
            "ch-ep-massagno-theophany-nektarios", "ch-ep-bissone-theophany-nektarios",
            "Theophany and Saint Nektarios Parish Winter Worship Site in Massagno",
            "Luogo di culto invernale della Parrocchia dell'Epifania e di San Nectario",
            [EP_DIRECTORY, "https://comunita-ellenica.ch/it/parrocchia/"],
            rank="Worship Site",
            address=["Chiesa Sant'Antonio di Gerso", "Via Selva", "6900 Massagno"],
            site="https://comunita-ellenica.ch/it/parrocchia/",
        ),
    ],
    "ro-western-europe": [
        row("ch-ro-reinach-andrew", "ro-western-europe",
            "Saint Andrew the Apostle Romanian Orthodox Parish in Reinach",
            "Parohia Sf. Apostol Andrei", [ROMANIAN_PARISHES],
            address=["Stockackerstrasse 36", "4153 Reinach"],
            site="https://biserica-basel.ch/"),
        row("ch-ro-turgi-peter-paul-athanasius", "ro-western-europe",
            "Saints Peter and Paul and Saint Athanasius the Great Romanian Orthodox Parish in Turgi",
            "Parohia Sfinții Apostoli Petru și Pavel și Sfântul Atanasie cel Mare",
            [ROMANIAN_PARISHES], address=["Weichlenstrasse", "5300 Turgi"],
            site="https://bisericabaden.ch/"),
        row("ch-ro-bern-george-mary-arsenie", "ro-western-europe",
            "Saint George, Saint Mary of Egypt, and Saint Arsenie of Prislop Romanian Orthodox Parish in Bern",
            "Parohia Sf. Mare Mucenic Gheorghe, Sf. Cuv. Maria Egipteanca, Sf. Cuv. Mart. Arsenie de la Prislop",
            [ROMANIAN_PARISHES], address=["Kastellweg 7", "3004 Bern"],
            site="https://biserica-ortodoxa-berna.ch/"),
        row("ch-ro-chur-parascheva", "ro-western-europe",
            "Saint Paraskeva Romanian Orthodox Parish in Chur",
            "Parohia Cuvioasa Parascheva", [ROMANIAN_PARISHES],
            address=["Priesterseminar St. Luzi", "Alte Schanfiggerstrasse 7", "7000 Chur"],
            site="http://www.biserica-romana-gr.ch/"),
        row("ch-ro-fribourg-demetrios-new", "ro-western-europe",
            "Saint Demetrios the New Romanian Orthodox Parish in Fribourg",
            "Parohia Sf. Dimitrie cel Nou", [ROMANIAN_PARISHES],
            site="https://www.biserica-fribourg.ch/"),
        row("ch-ro-grand-lancy-john-baptist", "ro-western-europe",
            "Saint John the Baptist Romanian Orthodox Parish in Grand-Lancy",
            "Parohia Sf. Ioan Botezătorul", [ROMANIAN_PARISHES],
            address=["Eglise de la Trinité", "Avenue Eugène-Lance 4", "1212 Grand-Lancy"],
            site="https://www.biserica.ch/"),
        row("ch-ro-chambesy-resurrection", "ro-western-europe",
            "Resurrection of the Lord Romanian Orthodox Parish in Chambesy",
            "Parohia Învierea Domnului", [ROMANIAN_PARISHES],
            address=["Chemin de Chambésy 37", "1292 Chambésy"],
            site="http://www.biserica-geneva.ch/"),
        row("ch-ro-lausanne-all-romanian-swiss-saints", "ro-western-europe",
            "All Romanian and Swiss Saints Romanian Orthodox Parish in Lausanne",
            "Parohia Tuturor Sfinților Români și Elvețieni", [ROMANIAN_PARISHES],
            address=["Avenue de la Harpe 2-B", "1007 Lausanne"],
            site="https://www.biserica.ch/"),
        row("ch-ro-lugano-john-suceava", "ro-western-europe",
            "Saint John the New of Suceava Romanian Orthodox Parish in Lugano",
            "Parohia Sf. Ioan cel Nou de la Suceava", [ROMANIAN_PARISHES],
            address=["Via Madonnetta 13", "6900 Lugano"], site="https://ortodossi.ch/"),
        row("ch-ro-horw-nativity-theotokos", "ro-western-europe",
            "Nativity of the Mother of God Romanian Orthodox Parish in Horw",
            "Parohia Nașterea Maicii Domnului", [ROMANIAN_PARISHES],
            address=["Bodenmattstrasse 2", "6048 Horw"],
            site="https://www.biserica-luzern.ch/"),
        row("ch-ro-corcelles-trinity-nektarios", "ro-western-europe",
            "Holy Trinity and Saint Nektarios of Aegina Romanian Orthodox Parish in Corcelles",
            "Parohia Sf. Treime și Sf. Nectarie de Eghina", [ROMANIAN_PARISHES],
            address=["Grande Rue 13", "2035 Corcelles"],
            site="https://eglise-orthodoxe-neuchatel.ch/"),
        row("ch-ro-saviese-george-maurice-theodora-patapios", "ro-western-europe",
            "Saints George, Maurice, Theodora, and Patapios Romanian Orthodox Parish in Saviese",
            "Parohia Sf. Gheorghe - Sf. Mauritiu - Sf. Teodora și Sf. Patapie",
            [ROMANIAN_PARISHES], address=["Rue de la Chapelle 5", "1965 Savièse"],
            site="http://www.orthodoxievalais.net/"),
        row("ch-ro-saviese-saint-antoine", "ch-ro-saviese-george-maurice-theodora-patapios",
            "Saint George, Saint Maurice, Saint Theodora, and Saint Patapios Parish Worship Site at Saint Antoine Chapel",
            "Loc de slujire al Parohiei Sf. Gheorghe - Sf. Mauritiu - Sf. Teodora și Sf. Patapie la Chapelle Saint Antoine",
            [ROMANIAN_PARISHES], rank="Worship Site",
            address=["Chapelle Saint Antoine", "Route d'Oucon 31", "1965 Savièse"],
            site="http://www.orthodoxievalais.net/"),
        row("ch-ro-st-gallen-anthony", "ro-western-europe",
            "Saint Anthony the Great Romanian Orthodox Parish in St Gallen",
            "Parohia Sf. Antonie cel Mare", [ROMANIAN_PARISHES],
            address=["Bildstrasse 2a", "9015 St Gallen"],
            site="https://biserica-stgallen.ch/"),
        row("ch-ro-winterthur-dormition", "ro-western-europe",
            "Dormition of the Mother of God Romanian Orthodox Parish in Winterthur",
            "Parohia Adormirea Maicii Domnului", [ROMANIAN_PARISHES],
            address=["Tellstrasse 11A", "8400 Winterthur"],
            site="https://parohia-winterthur.ch/"),
        row("ch-ro-zurich-saint-nicholas", "ro-western-europe",
            "Saint Nicholas Romanian Orthodox Parish in Zurich",
            "Parohia Sf. Nicolae", [ROMANIAN_PARISHES],
            address=["Wehntalerstrasse 451", "8046 Zürich"],
            site="https://www.bor-zh.ch/"),
        row("ch-ro-les-sciernes-protection-monastery", "ro-western-europe",
            "Protection of the Mother of God Monastery in Les Sciernes d'Albeuve",
            "Mănăstirea Sfântului Acoperământ al Născătoarei-de-Dumnezeu",
            [ROMANIAN_MONASTERIES], rank="Monastery", kind="monastery",
            address=["Route de la Gare 39", "1669 Les Sciernes d'Albeuve"],
            site="http://monasteresuisse.mitropolia.eu/"),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row("ch-rocor-basel-nicholas", "ru-great-britain-and-western-europe-rocor",
            "Saint Nicholas Church in Basel", "Церковь Святителя Николая",
            [ROCOR_DIRECTORY], rank="Church",
            address=["Amerbachstrasse 72", "4057 Basel"],
            site="https://www.russische-kirche-basel.com/"),
        row("ch-rocor-bern-holy-trinity", "ru-great-britain-and-western-europe-rocor",
            "Holy Trinity Church in Bern", "Храм Святой Троицы",
            [ROCOR_DIRECTORY], rank="Church",
            address=["Postgasse 62", "3011 Bern"], site="https://russischekirchebern.ch/"),
        row("ch-rocor-vevey-saint-barbara", "ru-great-britain-and-western-europe-rocor",
            "Saint Barbara Church in Vevey", "Храм святой великомученицы Варвары",
            [ROCOR_DIRECTORY], rank="Church",
            address=["Rue des Communaux 12", "1800 Vevey"]),
        row("ch-rocor-geneva-exaltation-cathedral", "ru-great-britain-and-western-europe-rocor",
            "Exaltation of the Holy Cross Cathedral in Geneva",
            "Крестовоздвиженский кафедральный собор", [ROCOR_DIRECTORY],
            rank="Cathedral", address=["Rue Rodolphe-Toepffer 9", "1206 Genève"],
            site="https://www.eglise-russe.ch/"),
        row("ch-rocor-leysin-panteleimon", "ru-great-britain-and-western-europe-rocor",
            "Saint Panteleimon Church in Leysin", "Храм святого великомученика Пантелеимона",
            [ROCOR_DIRECTORY], rank="Church",
            address=["Maison Riant-Val", "1854 Leysin"]),
        row("ch-rocor-lucerne-theodosius", "ru-great-britain-and-western-europe-rocor",
            "Saint Theodosius the Great of the Kiev Caves Mission in Lucerne",
            "Миссия преподобного Феодосия Великого Киево-Печерского",
            [ROCOR_DIRECTORY], rank="Mission",
            address=["Museggstrasse 15", "6004 Luzern"], site="https://cerkov.ch/"),
        row("ch-rocor-st-gallen-all-swiss-saints", "ru-great-britain-and-western-europe-rocor",
            "All Saints of Switzerland Mission in St Gallen",
            "Миссия Всех Швейцарских Святых", [ROCOR_DIRECTORY], rank="Mission",
            address=["St Barbara Chapel", "Zürcherstrasse 436", "9015 St Gallen"],
            site="https://sites.google.com/view/orthodoxe-mission-ch"),
        row("ch-rocor-frauenfeld-all-swiss-saints", "ch-rocor-st-gallen-all-swiss-saints",
            "All Saints of Switzerland Mission Worship Site in Frauenfeld",
            "Миссия Всех Швейцарских Святых во Фрауэнфельде",
            [ROCOR_DIRECTORY], rank="Worship Site",
            address=["St Anna Chapel, Friedhof Oberkirche", "Oberkirchstrasse 66", "8500 Frauenfeld"],
            site="https://sites.google.com/view/orthodoxe-mission-ch"),
        row("ch-rocor-schaffhausen-all-swiss-saints", "ch-rocor-st-gallen-all-swiss-saints",
            "All Saints of Switzerland Mission Worship Site in Schaffhausen",
            "Миссия Всех Швейцарских Святых в Шаффхаузене",
            [ROCOR_DIRECTORY], rank="Worship Site",
            address=["St Anna Chapel", "Baumgartenstrasse 12", "8200 Schaffhausen"],
            site="https://sites.google.com/view/orthodoxe-mission-ch"),
        row("ch-rocor-fribourg-nicholas", "ru-great-britain-and-western-europe-rocor",
            "Saint Nicholas the Wonderworker Mission in Fribourg",
            "Миссия святителя Николая Чудотворца", [ROCOR_DIRECTORY], rank="Mission",
            address=["Convict Salesianum", "Avenue du Moléson 21", "1700 Fribourg"]),
        row("ch-rocor-zurich-protection", "ru-great-britain-and-western-europe-rocor",
            "Protection of the Mother of God Church in Zurich",
            "Храм Покрова Пресвятой Богородицы", [ROCOR_DIRECTORY], rank="Church",
            address=["Haldenbachstrasse 2", "8006 Zürich"], site="https://www.pokrov.ch/"),
    ],
    "sr-switzerland": [
        row("ch-sr-basel-all-saints", "sr-switzerland",
            "Synaxis of All Saints Serbian Orthodox Parish in Basel",
            "Српска православна црквена општина и парохија Свих Светих у Базелу",
            [SERBIAN_BASEL], address=["Mühlenberg 11", "4051 Basel"],
            site="http://spc-basel.ch/"),
        row("ch-sr-belp-cyril-methodius", "sr-switzerland",
            "Saints Cyril and Methodius Serbian Orthodox Parish in Belp",
            "Парохија Светих равноапостолних Кирила и Методија у Берну",
            [SERBIAN_BERN], address=["Aemmenmattstrasse 12", "3123 Belp"],
            site="http://www.spcobern.ch/"),
        row("ch-sr-solothurn-cyril-methodius", "ch-sr-belp-cyril-methodius",
            "Saints Cyril and Methodius Parish Worship Site in Solothurn",
            "Богослужбено место Српске православне црквене општине Берн у Золотурну",
            [SERBIAN_BERN, EP_SWISS_DIRECTORY], rank="Worship Site",
            address=["Franziskanerkirche", "Barfüssergasse 26", "4500 Solothurn"]),
        row("ch-sr-chancy-andrew", "sr-switzerland",
            "Saint Andrew the First-Called Serbian Orthodox Parish in Chancy",
            "Парохија Светог Андреја Првозваног у Женеви", [SERBIAN_WEST],
            address=["Route de Bellegarde 69", "1284 Chancy"], site="https://fr.spczeneva.com/"),
        row("ch-sr-perlen-nativity-theotokos", "sr-switzerland",
            "Nativity of the Mother of God Serbian Orthodox Parish in Perlen",
            "Парохија Рођења Пресвете Богородице", [SERBIAN_EPARChY, EP_SWISS_DIRECTORY],
            address=["Dorfstrasse 2", "6035 Perlen"], site="http://spcoluzern.ch/"),
        row("ch-sr-st-gallen-simon-monk", "sr-switzerland",
            "Venerable Simon the Monk Serbian Orthodox Parish in St Gallen",
            "Парохија Преподобног Симона Монаха у Санкт Галену", [SERBIAN_ST_GALLEN],
            address=["Langgasse 161", "9008 St Gallen"], site="https://www.spc-sg.ch/"),
        row("ch-sr-chippis-community", "sr-switzerland",
            "Serbian Orthodox Church Community in Chippis",
            "Српска православна црквена општина у Сијеру", [SERBIAN_EPARChY, EP_SWISS_DIRECTORY],
            rank="Church Community", address=["Rue Saint-Urbain 7", "3965 Chippis"]),
        row("ch-sr-lausanne-three-hierarchs", "sr-switzerland",
            "Three Holy Hierarchs Serbian Orthodox Parish in Lausanne",
            "Парохија Света Три Јерарха у Лозани", [SERBIAN_WEST],
            address=["Route de Berne 230", "1066 Epalinges"]),
        row("ch-sr-lausanne-maire-gregory", "sr-switzerland",
            "Saint Maire and Saint Gregory Palamas Orthodox Parish in Lausanne",
            "Paroisse orthodoxe Saint Maire et Saint Grégoire Palamas",
            [SERBIAN_WEST, "https://orthodoxie.ch/p/lausanne-paroisse-saint-maire/"],
            address=["Avenue Louis Vulliemin 16", "1005 Lausanne"]),
        row("ch-sr-lugano-ticino", "sr-switzerland",
            "Serbian Orthodox Church Community of Ticino in Lugano",
            "Comunità ecclesiale ortodossa serba del Canton Ticino",
            [SERBIAN_EPARChY, "https://orthodoxie.ch/it/italiano/parrocchie/comunita-ortodossa-serba-ticino/"],
            rank="Church Community", address=["Chiesa di San Rocco", "Piazza San Rocco", "6900 Lugano"],
            ),
        row("ch-sr-bellinzona-ticino", "ch-sr-lugano-ticino",
            "Serbian Orthodox Church Community of Ticino Worship Site in Bellinzona",
            "Luogo di culto della Comunità ecclesiale ortodossa serba del Canton Ticino a Bellinzona",
            [SERBIAN_EPARChY, "https://orthodoxie.ch/it/italiano/parrocchie/comunita-ortodossa-serba-ticino/"],
            rank="Worship Site", address=["Chiesa Madonna della Neve", "Via Sasso Corbaro", "6500 Bellinzona"],
            ),
        row("ch-sr-zurich-dormition", "sr-switzerland",
            "Dormition of the Mother of God Serbian Orthodox Parish in Zurich",
            "Парохија Успења Пресвете Богородице у Цириху", [SERBIAN_ZURICH],
            address=["Glattstegweg 91", "8051 Zürich"], site="https://www.pravoslavnacrkva.ch/"),
        row("ch-sr-zurich-holy-trinity", "sr-switzerland",
            "Holy Trinity Serbian Orthodox Parish in Zurich",
            "Парохија Свете Тројице у Цириху", [SERBIAN_ZURICH, EP_SWISS_DIRECTORY],
            address=["Elisabethenstrasse 20", "8004 Zürich"]),
    ],
    "ru-korsun": [
        row("ch-ru-zurich-resurrection", "ru-korsun",
            "Resurrection of Christ Parish in Zurich", "Приход Воскресения Христова в Цюрихе",
            [MOSCOW_SWITZERLAND, MOSCOW_ZURICH],
            address=["Narzissenstrasse 10", "8006 Zürich"], site="http://www.pravoslavie.ch/"),
        row("ch-ru-lausanne-all-swiss-saints", "ru-korsun",
            "All Saints of Helvetia Orthodox Community in Lausanne",
            "Communauté orthodoxe de Tous les Saints Helvétiques",
            [MOSCOW_SWITZERLAND, "https://www.egliserusse.eu/Le-Metropolite-Nestor-visite-les-nouvelles-communautes-en-Haute-Savoie-et-a-Lausanne_a2067.html"],
            rank="Community", site="https://www.saints-helvetes-orthodoxes.ch/"),
        row("ch-ru-sion-theodore-ame", "ru-korsun",
            "Saint Theodore and Saint Ame Orthodox Chapel in Sion",
            "Chapelle orthodoxe Saint-Théodore-et-Saint-Amé",
            [MOSCOW_SWITZERLAND], rank="Chapel",
            address=["Rue du Grand-Pont 8", "1950 Sion"], site="https://www.orthodox.ch/"),
        row("ch-ru-saint-maurice-saint-james", "ru-korsun",
            "Saint James of the Pilgrims Orthodox Chapel in Saint-Maurice",
            "Chapelle Saint-Jacques-des-Pèlerins", [MOSCOW_SAINT_MAURICE],
            rank="Chapel", address=["Avenue du Simplon 9", "1890 Saint-Maurice"]),
        row("ch-ru-melide-protection", "ru-korsun",
            "Protection of the Mother of God Parish in Melide",
            "Приход Покрова Пресвятой Богородицы в Мелиде",
            [MOSCOW_MELIDE], address=["Via al Doyro 24", "6815 Melide"]),
        row("ch-ru-dompierre-holy-trinity", "ru-korsun",
            "Holy Trinity Monastery in Dompierre", "Монастырь Пресвятой Троицы в Домпьер",
            [MOSCOW_PLACES], rank="Monastery", kind="monastery",
            address=["Route de Lucens 15", "1682 Dompierre"]),
        row("ch-ru-roveredo-holy-cross", "ru-korsun",
            "Holy Cross Monastery in Roveredo", "Крестовоздвиженский мужской монастырь в Ровередо",
            [MOSCOW_PLACES, MOSCOW_ROVEREDO], rank="Monastery", kind="monastery",
            address=["Eremo Santa Croce", "6957 Roveredo"]),
    ],
    "russia": [
        row("ch-ru-geneva-nativity-stavropegion", "russia",
            "Nativity of the Mother of God Church in Geneva",
            "Храм Рождества Пресвятой Богородицы в Женеве",
            [MOSCOW_EXARCHATE], rank="Patriarchal Stavropegion",
            address=["Avenue Jean-Martin 11", "1224 Chêne-Bougeries"]),
    ],
    "bg-western-central-europe": [
        row("ch-bg-geneva-nativity-theotokos", "bg-western-central-europe",
            "Nativity of the Mother of God Bulgarian Orthodox Church Community in Geneva",
            "Българска православна църковна общност „Рождество Богородично“",
            [BULGARIAN_GENEVA], rank="Church Community",
            address=["Temple de la Madeleine", "Rue Toutes-Ames", "1204 Geneva"]),
        row("ch-bg-zurich-saint-george", "bg-western-central-europe",
            "Saint George the Victorious Bulgarian Orthodox Church Community in Zurich",
            "БПЦО „Св. Георги Победоносец“ - Цюрих",
            [BULGARIAN_ZURICH, BULGARIAN_ZURICH_VISIT], rank="Church Community",
            address=["Maria-Hilf Kirche", "Leimbachstrasse 64", "8041 Zürich"]),
    ],
    "ge-western-europe": [
        row("ch-ge-bern-saint-nino", "ge-western-europe",
            "Saint Nino Georgian Orthodox Parish in Bern",
            "წმ. ნინოს სახელობის სამრევლო ბერნში",
            [GEORGIAN_SYNOD, GEORGIAN_DIOCESE,
             "https://orthodoxie.ch/de/deutsch/verzeichnis/bern-georgisch-orthodoxe-gemeinde-der-heiligen-nino/"],
            address=["Rathausgasse 2", "3011 Bern"], site=GEORGIAN_DIOCESE),
        row("ch-ge-zurich-saint-nino", "ge-western-europe",
            "Saint Nino Georgian Orthodox Parish in Zurich",
            "ციურიხის წმ. ნინოს სახელობის სამრევლო",
            [GEORGIAN_SYNOD, GEORGIAN_DIOCESE,
             "https://orthodoxie.ch/de/deutsch/verzeichnis/zuerich-georgisch-orthodoxe-gemeinde-der-heiligen-nino/"],
            address=["Glattstegweg 91", "8051 Zürich"], site=GEORGIAN_DIOCESE),
    ],
    "mk-europe": [
        row("ch-mk-lausanne-all-macedonian-saints", "mk-europe",
            "Synaxis of All Macedonian Saints Macedonian Orthodox Church Community in Lausanne",
            "МПЦО „Собор на сите македонски светители“ - Лозана",
            [MACEDONIAN_DIRECTORY, MACEDONIAN_COUNT], rank="Church Community",
            address=["Chemin de l'Eglise 13", "1026 Denges"], site="https://mpc-lausanne.ch/"),
        row("ch-mk-triengen-saint-naum", "mk-europe",
            "Saint Naum of Ohrid Macedonian Orthodox Church Community in Triengen",
            "МПЦО „Свети Наум Охридски“ - Триенген",
            [MACEDONIAN_DIRECTORY, MACEDONIAN_COUNT], rank="Church Community",
            address=["Gislerstrasse 9", "6234 Triengen"], site="http://mpc-triengen.ch/"),
        row("ch-mk-locarno-theotokos", "mk-europe",
            "Most Holy Mother of God Macedonian Orthodox Church Community in Locarno",
            "МПЦО „Пресвета Богородица“ - Локарно",
            [MACEDONIAN_DIRECTORY, MACEDONIAN_COUNT], rank="Church Community"),
    ],
    "ukraine-uoc": [
        row("ch-uoc-bern-myrrhbearers", "ukraine-uoc",
            "Holy Myrrh-Bearing Women Ukrainian Orthodox Parish in Bern",
            "Парафія на честь святих Жон-Мироносиць у Берні",
            [UOC_SWITZERLAND, "https://www.ukraine-orthodox.ch/en/"],
            site="https://www.ukraine-orthodox.ch/"),
        row("ch-uoc-biel-myrrhbearers", "ch-uoc-bern-myrrhbearers",
            "Holy Myrrh-Bearing Women Parish Worship Site in Biel",
            "Богослужбове місце парафії святих Жон-Мироносиць у Білі",
            ["https://www.ukraine-orthodox.ch/en/"], rank="Worship Site"),
        row("ch-uoc-thun-myrrhbearers", "ch-uoc-bern-myrrhbearers",
            "Holy Myrrh-Bearing Women Parish Worship Site in Thun",
            "Богослужбове місце парафії святих Жон-Мироносиць у Туні",
            ["https://www.ukraine-orthodox.ch/en/"], rank="Worship Site"),
        row("ch-uoc-fribourg-myrrhbearers", "ch-uoc-bern-myrrhbearers",
            "Holy Myrrh-Bearing Women Parish Worship Site in Fribourg",
            "Богослужбове місце парафії святих Жон-Мироносиць у Фрібурі",
            ["https://www.ukraine-orthodox.ch/en/"], rank="Worship Site"),
        row("ch-uoc-wallisellen-andrew", "ukraine-uoc",
            "Saint Andrew the First-Called Ukrainian Orthodox Parish in Wallisellen",
            "Парафія на честь святого апостола Андрія Первозванного у Цюриху",
            [UOC_ZURICH, "https://www.ukrhram.com/"],
            address=["Zentralstrasse 10", "8304 Wallisellen"], site="https://www.ukrhram.com/"),
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "bg-western-central-europe": 2,
    "ep-switzerland": 14,
    "ge-western-europe": 2,
    "mk-europe": 3,
    "ro-western-europe": 17,
    "ru-great-britain-and-western-europe-rocor": 11,
    "ru-korsun": 7,
    "russia": 1,
    "sr-switzerland": 13,
    "ukraine-uoc": 5,
}


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
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") not in ("parish", "monastery"):
                raise ValueError("%s has unsupported kind: %s" %
                                 (row_id, item.get("kind")))
            if item.get("country") != "CH":
                raise ValueError("%s is outside Switzerland" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            serialized = json.dumps(item, ensure_ascii=False)
            if "\u2013" in serialized or "\u2014" in serialized:
                raise ValueError("%s contains a long dash" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "CH",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Switzerland parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 75:
        raise ValueError("Switzerland English name coverage changed")
    return payloads


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = []
    for parent in payloads:
        if parent not in base_ids and parent not in SPINE_ROW_PROPOSALS:
            errors.append("missing directory parent: %s" % parent)
    for proposal_id, proposal in SPINE_ROW_PROPOSALS.items():
        if proposal_id in base_ids:
            existing = next(item for item in directory.get("rows", [])
                            if item.get("id") == proposal_id)
            compared = ("parent", "kind", "rank", "name", "local", "seat",
                        "country", "site", "sources")
            if any(existing.get(key) != proposal.get(key)
                   for key in compared):
                errors.append("published directory parent differs: %s" %
                              proposal_id)
        if proposal.get("parent") not in base_ids:
            errors.append("proposed directory parent has missing root: %s" %
                          proposal.get("parent"))
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Switzerland row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": ["CH"],
        }
        for parent, payload in sorted(payloads.items())
    }


def export(payloads=None):
    """Return the shared-parent proposal and Switzerland branch fragments."""
    return {
        "spine_row_proposals": [
            dict(SPINE_ROW_PROPOSALS[key])
            for key in sorted(SPINE_ROW_PROPOSALS)
        ],
        "branches": payloads or build(),
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        errors = repository_problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Switzerland: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(export(payloads), ensure_ascii=False, indent=2))
        return 0
    print("Switzerland branches: 75 bodies and worship sites under 10 canonical parents")
    print("spine proposal: ge-western-europe under georgia")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
