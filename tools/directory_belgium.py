#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Belgium.

The parent jurisdictions also carry rows from other countries. This module
emits Belgium-only fragments for later merging and never writes a shared
payload.

    python tools/directory_belgium.py --check
    python tools/directory_belgium.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

EP_PARISHES = "https://orthodoxia.be/fr/paroisses/"
EP_UKRAINIAN = (
    "https://orthodoxia.be/fr/paroisses/presences-orthodoxes/"
)
EP_UKRAINIAN_PAGE = (
    "https://orthodoxia.be/fr/enoria/paroisse-saint-archange-michel-genk/"
)
MOSCOW_PARISHES = (
    "https://archiepiskopia.be/index.php?content=parishes&lang=fr"
)
ROCOR_DIRECTORY = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
RUSSIAN_TRADITION = "https://archeveche.eu/lieux/"
RUSSIAN_TRADITION_BRUSSELS = (
    "https://archeveche.eu/communique-de-ladministration-diocesaine-"
    "assemblee-generale-ordinaire-de-larcheveche-6-7-novembre-2026/"
)
SERBIAN_BENELUX = "https://dioceseserbe.org/fr/benelux/"
ROMANIAN_BELGIUM = (
    "https://www.mitropolia.eu/fr/site/185/paroisses-de-belgique.htm"
)
ROMANIAN_BELGIUM_DIRECTORY = "https://belgia.biserica.be/862-2/"
ROMANIAN_MONASTERY = "https://manastirea.be/program-liturgic/"
ROMANIAN_PATRIARCHAL_CHAPEL = "https://sfantaparascheva.be/"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
BULGARIAN_ANTWERP = "https://www.izvor.be/bg/church"
GEORGIAN_BENELUX = (
    "https://orthodoxia.be/fr/paroisses/presences-orthodoxes/"
)
GEORGIAN_MAP = "https://www.eklesia.us/georgian-orthodox-churches/"
MACEDONIAN_DIOCESE = "https://mpee.mk/category/za-eparxijata"
MACEDONIAN_BELGIUM = (
    "https://minisel.gov.mk/"
    "%D0%BC%D0%B0%D0%BA%D0%B5%D0%B4%D0%BE%D0%BD%D1%86%D0%B8%D1%82%D0%B5-"
    "%D0%B2%D0%BE-%D0%B1%D1%80%D0%B8%D1%81%D0%B5%D0%BB-"
    "%D1%98%D0%B0-%D0%BF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B8%D1%98%D0%B0-%D1%85/"
)
UOC_BRUSSELS_LOCATIONS = (
    "https://news.church.ua/2022/07/10/"
    "vidbulosya-pershe-bogosluzhinnya-parafiji-ukrajinskoji-"
    "pravoslavnoji-cerkvi-u-bryusseli/"
)
UOC_BRUSSELS_TWO_SITES = (
    "https://news.church.ua/2022/08/12/"
    "v-novostvorenij-parafiji-upc-u-bryusseli-vzhe-zvershili-"
    "dvanadcyat-tajinstv-xreshhennya/"
)
UOC_BRUSSELS_CURRENT = (
    "https://news.church.ua/2026/03/09/"
    "v-bryusseli-tisyachi-viruyuchix-upc-vidsvyatkuvali-prestolne-"
    "svyato-u-den-soboru-usix-prepodobnix-kijevo-pecherskix/"
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
        "country": "BE",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


EP_ROWS = [
    ("be-ep-brussels-holy-archangels-cathedral",
     "Cathedral of the Holy Archangels in Brussels",
     "Cathédrale des Saints Archanges, Bruxelles", "Cathedral"),
    ("be-ep-schaerbeek-saint-marina", "St Marina Parish in Schaerbeek",
     "Paroisse de Sainte Marina, Schaerbeek", "Parish"),
    ("be-ep-schaerbeek-saint-nicholas", "St Nicholas Parish in Schaerbeek",
     "Paroisse de Saint Nicolas, Schaerbeek", "Parish"),
    ("be-ep-schaerbeek-ignatius-theophoros",
     "St Ignatius the God-Bearer Parish in Schaerbeek",
     "Paroisse de Saint Ignace le Théophore, Schaerbeek", "Parish"),
    ("be-ep-ixelles-holy-archangels", "Holy Archangels Parish in Ixelles",
     "Paroisse des Saints Archanges, Ixelles", "Parish"),
    ("be-ep-saint-gilles-silouan-martin",
     "St Silouan the Athonite and St Martin of Tours Parish in Saint-Gilles",
     "Paroisse de Saints Silouane l'Athonite et Martin des Tours, St-Gilles",
     "Parish"),
    ("be-ep-anderlecht-nativity-theotokos",
     "Nativity of the Mother of God Parish in Anderlecht",
     "Paroisse de la Naissance de la Mère de Dieu, Anderlecht", "Parish"),
    ("be-ep-molenbeek-john-baptist", "St John the Baptist Parish in Molenbeek",
     "Paroisse de Saint Jean Baptiste, Molenbeek", "Parish"),
    ("be-ep-lasne-irene-paisios",
     "St Irene the Great Martyr and St Paisios the Athonite Parish in Lasne",
     "Paroisse des Saints Irène la Mégalomartyre et Païsios l'Athonite, Ohain (Lasne)",
     "Parish"),
    ("be-ep-dilbeek-george-alina", "St George and St Alina Parish in Dilbeek",
     "Paroisse des Saints Georges le Tropéophore et Alina, Dilbeek", "Parish"),
    ("be-ep-dilbeek-martin-tours", "St Martin of Tours Parish in Dilbeek",
     "Paroisse de Saint Martin de Tours, Dilbeek", "Parish"),
    ("be-ep-antwerp-annunciation", "Annunciation Parish in Antwerp",
     "Paroisse de l'Annonciation de la Mère de Dieu, Anvers", "Parish"),
    ("be-ep-ekeren-laurence", "St Laurence the Archdeacon Parish in Ekeren",
     "Paroisse de Saint Laurent l'Archidiacre, Ekeren (Anvers)", "Parish"),
    ("be-ep-berchem-sophrony", "St Sophrony the Athonite Parish in Berchem",
     "Paroisse de Saint Sophrony l'Athonite, Berchem (Anvers)", "Parish"),
    ("be-ep-hasselt-three-hierarchs", "Three Holy Hierarchs Parish in Hasselt",
     "Paroisse des Trois Hiérarques, Hasselt", "Parish"),
    ("be-ep-houthalen-dormition-raphael-nicholas-irene",
     "Dormition of the Mother of God and Sts Raphael, Nicholas and Irene Parish in Houthalen",
     "Paroisse de la Dormition de la Mère de Dieu et des Saints Raphaël, Nicolas et Irène, Houthalen",
     "Parish"),
    ("be-ep-beringen-nectarios", "St Nectarios Parish in Beringen",
     "Paroisse de Saint Nectaire, Beringen", "Parish"),
    ("be-ep-maasmechelen-demetrios", "St Demetrios Parish in Maasmechelen",
     "Paroisse de Saint Dimitrios, Maasmechelen", "Parish"),
    ("be-ep-genk-barbara", "St Barbara Parish in Genk",
     "Paroisse de Sainte Barbe, Genk", "Parish"),
    ("be-ep-tongeren-olga", "St Olga Parish in Tongeren",
     "Paroisse de Sainte Olga, Tongeren", "Parish"),
    ("be-ep-peer-meletios", "St Meletios of Antioch Parish in Peer",
     "Paroisse de Saint Meletios d'Antioche, Peer", "Parish"),
    ("be-ep-liege-barbara", "St Barbara Parish in Liège",
     "Paroisse de Sainte Barbe, Liège", "Parish"),
    ("be-ep-eupen-nino", "St Nino Equal-to-the-Apostles Parish in Eupen",
     "Paroisse de Sainte égale aux Apôtres Nino, Eupen", "Parish"),
    ("be-ep-verviers-presentation", "Presentation of Christ Parish in Verviers",
     "Paroisse de la Présentation du Christ au Temple, Verviers", "Parish"),
    ("be-ep-namur-raphael-nicholas-irene",
     "Sts Raphael, Nicholas and Irene Parish in Namur",
     "Paroisse des Saints Raphaël, Nicolas et Irène, Namur", "Parish"),
    ("be-ep-charleroi-barbara", "St Barbara Parish in Charleroi",
     "Paroisse de Sainte Barbe, Charleroi", "Parish"),
    ("be-ep-mons-nectarios", "St Nectarios Parish in Mons",
     "Paroisse de Saint Nectaire, Mons", "Parish"),
    ("be-ep-boussoit-protection-luke",
     "Protection of the Mother of God and St Luke of Simferopol Parish in Boussoit",
     "Paroisse de la Protection de la Mère de Dieu et Saint Luc de Simferopol, Boussoit",
     "Parish"),
    ("be-ep-peronnes-holy-unmercenaries",
     "Holy Unmercenaries Parish in Péronnes-lez-Binche",
     "Paroisse des Saints Anargyres, Péronnes-lez-Binche", "Parish"),
    ("be-ep-tournai-phocas", "St Phocas Parish in Tournai",
     "Paroisse de Saint Phocas, Tournai", "Parish"),
    ("be-ep-bruges-constantine-helen", "Sts Constantine and Helen Parish in Bruges",
     "Paroisse des Saints Constantin et Hélène, Bruges", "Parish"),
    ("be-ep-ostend-cyril-methodius", "Sts Cyril and Methodius Parish in Ostend",
     "Paroisse des Saints Cyrille et Méthode, Ostende", "Parish"),
    ("be-ep-kortrijk-amandus", "St Amand Parish in Kortrijk",
     "Paroisse de Saint Amand, Courtrai", "Parish"),
    ("be-ep-ghent-andrew", "Holy Apostle Andrew Parish in Ghent",
     "Paroisse de Saint Apôtre André, Gand", "Parish"),
]


MOSCOW_ROWS = [
    ("be-mp-brussels-nicholas-cathedral", "St Nicholas the Wonderworker Cathedral in Brussels", "Eglise-cathédrale de Saint Nicolas le Thaumaturge", "Cathedral"),
    ("be-mp-antwerp-nativity-christ", "Nativity of Christ Church in Antwerp", "Eglise de la Nativité du Christ", "Church"),
    ("be-mp-brussels-holy-trinity", "Holy Trinity Church in Brussels", "Eglise de la Sainte Trinité", "Church"),
    ("be-mp-brussels-protection", "Protection of the Mother of God Parish in Brussels", "Paroisse de la Protection de la Sainte Vierge", "Parish"),
    ("be-mp-brussels-saint-anne", "St Anne Church in Brussels", "Eglise de Sainte Anne", "Church"),
    ("be-mp-leuven-matthew", "Holy Apostle Matthew Parish in Leuven", "Paroisse du Saint Apôtre Matthieu", "Parish"),
    ("be-mp-leglise-holy-cross", "Exaltation of the Precious and Life-Giving Cross Church in Léglise", "Église de l'Exaltation de la vénérable et vivifiante Croix", "Church"),
    ("be-mp-liege-life-giving-spring", "Life-Giving Spring Icon of the Mother of God Church in Liège", "Eglise de l'icône de la Mère de Dieu Source de Vie", "Church"),
    ("be-mp-louvain-la-neuve-university-chapel", "Orthodox University Chapel in Louvain-la-Neuve", "Chapelle universitaire orthodoxe", "Chapel"),
    ("be-mp-mechelen-theophany", "Holy Theophany Parish in Mechelen", "Paroisse de la Sainte Epiphanie", "Parish"),
    ("be-mp-mons-archangel-michael", "Holy Archangel Michael Church in Mons", "Eglise du Saint Archange Michel", "Church"),
    ("be-mp-namur-seraphim-sarov", "St Seraphim of Sarov Parish in Namur", "Paroisse de Saint Seraphim de Sarov", "Parish"),
    ("be-mp-ostend-john-theologian", "St John the Theologian Parish in Ostend", "Paroisse de St. Jean le Théologien", "Parish"),
    ("be-mp-pervijze-joy-all-sorrow", "Joy of All Who Sorrow Monastery in Pervijze", "Monastère Orthodoxe de la Mère de Dieu, Consolatrice des affligés", "Monastery"),
    ("be-mp-trazegnies-iveron", "Iveron Mother of God Convent in Trazegnies", "Couvent de la Mère de Dieu d'Iveron (Portaïtissa)", "Monastery"),
    ("be-mp-charleroi-holy-trinity", "Holy Trinity Church in Charleroi", "Eglise de la Sainte Trinité", "Church"),
    ("be-mp-tournai-annunciation", "Annunciation Chapel in Tournai", "Chapelle de l'Annonciation", "Chapel"),
    ("be-mp-kortrijk-nativity-theotokos", "Nativity of the Virgin Mary Church in Kortrijk", "Église de la Nativité de la Vierge Marie", "Church"),
]


MOSCOW_ADDRESSES = {
    "be-mp-brussels-nicholas-cathedral": ["Rue des Chevaliers 29", "B-1050 Bruxelles"],
    "be-mp-antwerp-nativity-christ": ["Loosplaats 2, Sint-Jozefkerk", "B-2018 Antwerpen"],
    "be-mp-brussels-holy-trinity": ["Rue Léon Lepage 35", "1000 Bruxelles"],
    "be-mp-brussels-protection": ["Rue Léon Lepage 33", "1000 Bruxelles"],
    "be-mp-brussels-saint-anne": ["Avenue des Trembles, église Sainte-Anne", "1020 Laeken, Bruxelles"],
    "be-mp-leuven-matthew": ["Tervuursestraat 56, Collegium Latino-Americanum", "B-3000 Leuven"],
    "be-mp-leglise-holy-cross": ["Rue de Luxembourg 76", "B-6860 Léglise"],
    "be-mp-liege-life-giving-spring": ["Rue Ferrer 73", "B-4100 Seraing"],
    "be-mp-louvain-la-neuve-university-chapel": ["Ruelle Saint-Eloi 2", "1348 Louvain-la-Neuve"],
    "be-mp-mechelen-theophany": ["Blaasveldstraat 1", "2830 Willebroek"],
    "be-mp-mons-archangel-michael": ["Place des Martyrs 11-bis", "7000 Mons"],
    "be-mp-namur-seraphim-sarov": ["Avenue de la Vecquée 9", "B-5000 Namur"],
    "be-mp-ostend-john-theologian": ["Sint-Catharinaplein 23", "8400 Oostende"],
    "be-mp-pervijze-joy-all-sorrow": ["Rousdammestraat 1", "8600 Pervijze, Diksmuide"],
    "be-mp-trazegnies-iveron": ["Rue du Caillou 3", "B-6183 Trazegnies"],
    "be-mp-charleroi-holy-trinity": ["Chaussée de Charleroi 436", "B-6080 Montignies-sur-Sambre"],
    "be-mp-tournai-annunciation": ["Rue Albert 33", "B-7540 Kain"],
    "be-mp-kortrijk-nativity-theotokos": ["Hoog Mosscher 69A", "8500 Kortrijk"],
}


ROMANIAN_ROWS = [
    ("be-ro-antwerp-nativity-theotokos", "Nativity of the Mother of God Parish in Antwerp", "Paroisse de la Nativité-de-la-Mère-de-Dieu", "Parish"),
    ("be-ro-arlon-peter-paul", "Holy Apostles Peter and Paul Mission in Arlon", "Mission des Saints Apôtres Pierre et Paul", "Mission"),
    ("be-ro-ath-archangels-nectarios", "Holy Archangels Michael and Gabriel and St Nectarios Parish in Ath", "Paroisse des Saints-Archanges-Michel-et-Gabriel-et-de-Saint Nectaire", "Parish"),
    ("be-ro-brussels-annunciation", "Annunciation Parish in Brussels", "Paroisse de l'Annonciation", "Parish"),
    ("be-ro-brussels-nicholas", "St Nicholas Parish in Brussels", "Paroisse Saint-Nicolas", "Parish"),
    ("be-ro-uccle-peter-paul-gertrude", "Holy Apostles Peter and Paul and St Gertrude of Nivelles Parish in Uccle", "Paroisse des Saints Apôtres Pierre et Paul et Sainte Gertrude de Nivelles", "Parish"),
    ("be-ro-anderlecht-entry-theotokos-gregory", "Entry of the Mother of God and St Gregory Palamas Parish in Anderlecht", "Paroisse de l'Entrée de la Mère de Dieu au Temple et Saint Grégoire Palamas", "Parish"),
    ("be-ro-charleroi-john-romanos", "St John the Wallachian and St Piat the Roman Parish in Charleroi", "Paroisse des Saints Jean le Valaque et Piat le Romain", "Parish"),
    ("be-ro-aalst-andrew-maternus", "Holy Apostle Andrew and St Maternus Parish in Aalst", "Paroisse du Saint-Apôtre-André-et-de-Saint-Materne", "Parish"),
    ("be-ro-hasselt-antipa", "St Antipa the Athonite Mission in Hasselt", "Mission Sf. Antipa Athonitul", "Mission"),
    ("be-ro-hoogstraten-joachim-anna", "Sts Joachim and Anna Parish in Hoogstraten", "Paroisse des Saints Joachim et Anne", "Parish"),
    ("be-ro-huldenberg-all-saints", "All Saints Parish in Huldenberg", "Paroisse de Tous-les-Saints", "Parish"),
    ("be-ro-knokke-holy-apostles", "Holy Apostles Parish in Knokke-Heist", "Paroisse des Saints Apôtres", "Parish"),
    ("be-ro-landen-exaltation-cross", "Exaltation of the Holy Cross Parish in Landen", "Paroisse de l'Exaltation-de-la-Sainte-Croix", "Parish"),
    ("be-ro-liege-holy-spirit-demetrios", "Descent of the Holy Spirit and St Demetrios the New Parish in Liège", "Paroisse de la Descente-du-Saint-Esprit Saint-Dimitri-le-Nouveau-de-Bassarabov", "Parish"),
    ("be-ro-mons-mission", "Romanian Orthodox Mission in Mons", "Mission orthodoxe roumaine de Mons", "Mission"),
    ("be-ro-roeselare-luke", "Holy Apostle and Evangelist Luke Parish in Roeselare", "Paroisse du Saint Apôtre et Evangéliste Luc", "Parish"),
    ("be-ro-sint-niklaas-entry-theotokos-calinic", "Entry of the Mother of God and St Calinic of Edessa Parish in Sint-Niklaas", "Paroisse de l'Entrée de la Mère de Dieu au Temple et St. Calinic Métropolite d'Edesse", "Parish"),
    ("be-ro-stavelot-protection", "Protection of the Mother of God Parish in Stavelot", "Paroisse de la Protection de la Mère de Dieu", "Parish"),
    ("be-ro-turnhout-george", "St George the Great Martyr Parish in Turnhout", "Paroisse du Saint-Mégalomartyr-Georges", "Parish"),
    ("be-ro-warisy-john-baptist", "Nativity of St John the Baptist Parish in Warisy", "Paroisse de la Nativité de Saint Jean Baptiste", "Parish"),
    ("be-ro-brussels-trinity-cosmas-damian", "Holy Trinity and Sts Cosmas and Damian Parish in Brussels", "Paroisse de la Ste Trinité et des sts Côme et Damien", "Parish"),
]


ROMANIAN_ADDRESSES = {
    "be-ro-antwerp-nativity-theotokos": ["Heistraat 319", "2610 Wilrijk, Antwerpen"],
    "be-ro-arlon-peter-paul": ["Église de village, Rue de la Platinerie", "6700 Bonnert, Arlon"],
    "be-ro-ath-archangels-nectarios": ["Chaussée de Mons 263", "7800 Ath"],
    "be-ro-brussels-annunciation": ["Place de la Duchesse de Brabant 24", "1080 Bruxelles"],
    "be-ro-brussels-nicholas": ["Rue des Palais 181-183", "1030 Bruxelles"],
    "be-ro-uccle-peter-paul-gertrude": ["Rue Baron Guillaume Van Hamme 33B", "1180 Uccle"],
    "be-ro-anderlecht-entry-theotokos-gregory": ["Avenue Norbert Gille 67", "1070 Bruxelles"],
    "be-ro-charleroi-john-romanos": ["Rue Emile Gantois 46", "6030 Marchienne-au-Pont"],
    "be-ro-aalst-andrew-maternus": ["Begijnhof 41A", "9300 Aalst"],
    "be-ro-hasselt-antipa": ["Sint-Amandusstraat 4", "3511 Hasselt"],
    "be-ro-hoogstraten-joachim-anna": ["Klinketstraat 2", "2323 Hoogstraten"],
    "be-ro-huldenberg-all-saints": ["Sint-Jansbergsteenweg 44", "3040 Loonbeek, Huldenberg"],
    "be-ro-knokke-holy-apostles": ["Stella Maris, Christianastraat", "8380 Zeebrugge"],
    "be-ro-landen-exaltation-cross": ["Sint Norbertusstraat 64B", "3400 Landen"],
    "be-ro-liege-holy-spirit-demetrios": ["Rue des Airelles 103", "4100 Seraing"],
    "be-ro-roeselare-luke": ["Sint-Eligiuskerk, Kampstraat 1", "8840 Staden"],
    "be-ro-sint-niklaas-entry-theotokos-calinic": ["Heistraat 210", "9100 Sint-Niklaas"],
    "be-ro-stavelot-protection": ["Rue Neuve 24", "4970 Stavelot"],
    "be-ro-turnhout-george": ["Kerkplein 1", "2300 Turnhout"],
    "be-ro-warisy-john-baptist": ["Rue du Monument 25", "6987 Warisy, Rendeux"],
    "be-ro-brussels-trinity-cosmas-damian": ["Rue Paul Spaak 26", "1050 Bruxelles"],
}


ROWS = {
    "ep-belgium": [
        row(item[0], "ep-belgium", item[1], item[2], [EP_PARISHES],
            rank=item[3]) for item in EP_ROWS
    ] + [
        row(
            "be-ep-genk-ukrainian-archangel-michael", "ep-belgium",
            "Holy Archangel Michael Ukrainian Parish in Genk",
            "Paroisse du Saint Archange Michel, Genk",
            [EP_UKRAINIAN, EP_UKRAINIAN_PAGE],
            address=["Hulshagenstraat", "3600 Genk, Belgium"],
        ),
    ],
    "ru-brussels-and-belgium": [
        row(item[0], "ru-brussels-and-belgium", item[1], item[2],
            [MOSCOW_PARISHES], rank=item[3],
            kind="monastery" if item[3] == "Monastery" else "parish",
            address=MOSCOW_ADDRESSES[item[0]])
        for item in MOSCOW_ROWS
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "be-rocor-brussels-saint-job",
            "ru-great-britain-and-western-europe-rocor",
            "St Job Memorial Church in Brussels",
            "Брюссель. Храмъ св. прав. Iова Многострадальнаго, въ память св. Царя-Мученика Николая II, Царской Семьи и всѣхъ въ смуту убіенныхъ",
            [ROCOR_DIRECTORY], rank="Church",
            address=["8, rue du Manoir (av. De Fré)",
                     "B-1180 Bruxelles, Belgique"],
            site="https://www.egliserussememorial.be",
        ),
        row(
            "be-rocor-brussels-resurrection",
            "ru-great-britain-and-western-europe-rocor",
            "Resurrection of Christ Church in Brussels",
            "Брюссель. Храм Воскресения Христова",
            [ROCOR_DIRECTORY], rank="Church",
            address=["42, rue des Drapiers", "B-1050 Bruxelles"],
            site="https://www.pravoslavie.be",
        ),
    ],
    "ru-archdiocese-western-europe": [
        row(
            "be-russian-tradition-brussels-panteleimon-nicholas",
            "ru-archdiocese-western-europe",
            "Sts Panteleimon and Nicholas Church in Brussels",
            "Église Saint Pantéléïmon et Saint Nicolas",
            [RUSSIAN_TRADITION, RUSSIAN_TRADITION_BRUSSELS], rank="Church",
        ),
        row(
            "be-russian-tradition-liege-alexander-seraphim",
            "ru-archdiocese-western-europe",
            "St Alexander Nevsky and St Seraphim of Sarov Church in Liège",
            "Église Saint Alexandre Nevsky et Saint Séraphin de Sarov",
            [RUSSIAN_TRADITION], rank="Church",
            address=["80, rue du Laveu", "B 4000 Liège, Belgique"],
        ),
        row(
            "be-russian-tradition-antwerp-george",
            "ru-archdiocese-western-europe",
            "St George the Trophy-Bearer Parish in Antwerp",
            "Paroisse Saint-Georges-le-Tropéophore",
            [RUSSIAN_TRADITION],
        ),
        row(
            "be-russian-tradition-banneux-protection",
            "ru-archdiocese-western-europe",
            "Protection of the Mother of God Orthodox Chapel in Banneux",
            "Chapelle orthodoxe Notre-Dame-de-toute-Protection à Banneux",
            [RUSSIAN_TRADITION], rank="Chapel",
        ),
    ],
    "sr-western-europe": [
        row("be-sr-brussels-sava", "sr-western-europe",
            "St Sava Parish in Brussels", "Парохија Светог Саве, Брисел",
            [SERBIAN_BENELUX], address=["Rue des Etangs Noirs 110",
                                       "1080 Bruxelles, Belgium"],
            site="https://www.svetisava.be"),
        row("be-sr-brussels-pec-theotokos", "sr-western-europe",
            "Mother of God of Peć Parish in Brussels",
            "Парохија Богородице Пећке Краснице, Брисел",
            [SERBIAN_BENELUX], address=["Rue Gendebien 9",
                                       "1030 Schaerbeek, Belgium"]),
        row("be-sr-antwerp-george", "sr-western-europe",
            "St George Parish in Antwerp", "Парохија Св. Георгија, Антверпен",
            [SERBIAN_BENELUX], address=["Lageweg 121",
                                       "2660 Hoboken (Antwerpen), Belgium"],
            site="https://www.spvz.be"),
        row("be-sr-godsheide-visitation", "sr-western-europe",
            "Visitation of the Mother of God Church in Godsheide",
            "O.-L.-Vr.-Bezoekingkerk, Godsheide", [SERBIAN_BENELUX],
            rank="Church", address=["Kiezelstraat 132a",
                                     "3500 Godsheide, Belgium"]),
        row("be-sr-liege-protection", "sr-western-europe",
            "Protection of the Mother of God Parish in Liège",
            "Paroisse Protection de la Mère de Dieu, Liège",
            [SERBIAN_BENELUX], address=["Chapelle Sainte-Croix",
                                       "rue Hors-Chateau 49",
                                       "4000 Liège, Belgium"]),
        row("be-sr-charleroi-luke", "sr-western-europe",
            "St Luke Parish in Charleroi", "Парохија Светог Луке, Charleroi",
            [SERBIAN_BENELUX]),
    ],
    "ro-western-europe": [
        row(item[0], "ro-western-europe", item[1], item[2],
            [ROMANIAN_BELGIUM], rank=item[3],
            address=ROMANIAN_ADDRESSES.get(item[0])) for item in ROMANIAN_ROWS
    ] + [
        row(
            "be-ro-namur-protection-monastery", "ro-western-europe",
            "Protection of the Mother of God Monastery in Namur",
            "Mănăstirea Acoperământul Maicii Domnului, Namur",
            [ROMANIAN_BELGIUM_DIRECTORY, ROMANIAN_MONASTERY],
            rank="Monastery", kind="monastery",
            address=["Rue Su l'Tîdge 86", "5020 Vedrin, Namur, Belgium"],
            site="https://manastirea.be/",
        ),
    ],
    "romania": [
        row(
            "be-ro-brussels-parascheva-patriarchal-chapel", "romania",
            "St Parascheva Patriarchal Chapel in Brussels",
            "Biserica Sfânta Cuvioasă Parascheva, Paraclis Patriarhal, Bruxelles",
            [ROMANIAN_BELGIUM_DIRECTORY, ROMANIAN_PATRIARCHAL_CHAPEL],
            rank="Patriarchal Chapel",
            address=["Rue de la Charité 41", "1210 Bruxelles, Belgium"],
            site="https://sfantaparascheva.be/",
        ),
    ],
    "bg-western-central-europe": [
        row(
            "be-bg-brussels-clement-ohrid", "bg-western-central-europe",
            "St Clement of Ohrid Bulgarian Orthodox Church Community in Brussels",
            "БПЦО Св. Климент Охридски, Брюксел",
            [BULGARIAN_DIRECTORY], rank="Church Community",
            address=["Rue Victor Hugo 8", "B-1030 Bruxelles, Belgium"],
        ),
        row(
            "be-bg-antwerp-zlata-maglenska", "bg-western-central-europe",
            "St Zlata of Meglen Bulgarian Orthodox Church Community in Antwerp",
            "БПЦО Св. Злата Мъгленска, Антверпен",
            [BULGARIAN_ANTWERP], rank="Church Community",
            address=["Heilige Naam Jezus", "Edenplein 26",
                     "2610 Wilrijk, Belgium"],
        ),
    ],
    "ge-belgium-holland": [
        row(
            "be-ge-brussels-queen-tamar", "ge-belgium-holland",
            "St Queen Tamar Georgian Orthodox Parish in Brussels",
            "წმ. თამარ მეფის სამრევლო", [GEORGIAN_BENELUX, GEORGIAN_MAP],
            address=["Rue Gendebien 9", "1030 Bruxelles, Belgium"],
        ),
        row(
            "be-ge-antwerp-nino", "ge-belgium-holland",
            "St Nino Georgian Orthodox Parish in Antwerp",
            "წმ. ნინოს სახელობის სამრევლო", [GEORGIAN_BENELUX, GEORGIAN_MAP],
            address=["Goedendagstraat 48", "2140 Antwerpen, Belgium"],
        ),
    ],
    "mk-europe": [
        row(
            "be-mk-brussels-elijah-michael", "mk-europe",
            "Holy Prophet Elijah and Archangel Michael Macedonian Orthodox Church Community in Brussels",
            "МПЦО Св. Пророк Илија и Архангел Михаил, Брисел",
            [MACEDONIAN_DIOCESE, MACEDONIAN_BELGIUM],
            rank="Church Community",
            address=["Chapelle pour l'Europe", "Brussels, Belgium"],
        ),
    ],
    "ukraine-uoc": [
        row(
            "be-uoc-brussels-community", "ukraine-uoc",
            "All Venerable Fathers of the Kyiv Caves Ukrainian Orthodox Parish in Brussels",
            "парафія УПЦ на честь Усіх преподобних Києво-Печерських у Брюсселі",
            [UOC_BRUSSELS_TWO_SITES, UOC_BRUSSELS_CURRENT],
            address=["Avenue Norbert Gilles 67",
                     "1070 Anderlecht, Belgium"],
        ),
        row(
            "be-uoc-brussels-community-kraainem-site",
            "be-uoc-brussels-community",
            "Kraainem Worship Site of the All Venerable Fathers of the Kyiv Caves Parish",
            "місце регулярних богослужінь громади Української Православної Церкви в Брюсселі",
            [UOC_BRUSSELS_TWO_SITES, UOC_BRUSSELS_CURRENT],
            rank="Recurring Worship Site",
            address=["Hebronlaan 5", "1950 Kraainem, Belgium"],
        ),
    ],
}


EXPECTED = {
    "bg-western-central-europe": 2,
    "ep-belgium": 35,
    "ge-belgium-holland": 2,
    "mk-europe": 1,
    "ro-western-europe": 23,
    "romania": 1,
    "ru-archdiocese-western-europe": 4,
    "ru-brussels-and-belgium": 18,
    "ru-great-britain-and-western-europe-rocor": 2,
    "sr-western-europe": 6,
    "ukraine-uoc": 2,
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
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
    for field in ("address", "services", "founded", "languages"):
        if (out.get(field) and
                (not isinstance(out[field], list) or
                 not all(isinstance(line, str) for line in out[field]))):
            raise ValueError("%s has invalid %s" % (out.get("id"), field))
    serialized = json.dumps(out, ensure_ascii=False)
    if "\u2013" in serialized or "\u2014" in serialized:
        raise ValueError("%s contains a long dash" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    all_new_ids = {item["id"] for source_rows in ROWS.values()
                   for item in source_rows}
    if len(all_new_ids) != sum(len(items) for items in ROWS.values()):
        raise ValueError("duplicate Belgium source row id")
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        pending = list(source_rows)
        while pending:
            progressed = False
            for source in list(pending):
                item = clean(source)
                if item.get("parent") not in branch_seen:
                    continue
                row_id = item.get("id")
                if not row_id or row_id in seen:
                    raise ValueError("duplicate or missing id: %s" % row_id)
                if item.get("kind") not in {"parish", "monastery"}:
                    raise ValueError("%s has unsupported kind" % row_id)
                if item.get("country") != "BE":
                    raise ValueError("%s is outside Belgium" % row_id)
                if not item.get("name") or not item.get("local"):
                    raise ValueError("%s lacks a name" % row_id)
                if item.get("site") and not item["site"].startswith("http"):
                    raise ValueError("%s carries a non-URL site" % row_id)
                seen.add(row_id)
                branch_seen.add(row_id)
                rows.append(item)
                pending.remove(source)
                progressed = True
            if not progressed:
                raise ValueError("Belgium child rows have unresolved parents")
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "BE",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Belgium parent counts changed: %r" % actual)
    if len(ENGLISH_NAMES) != 96:
        raise ValueError("Belgium English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "BE",
            "merge_required": True,
        }
        for parent, payload in sorted(payloads.items())
    }


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = []
    for parent in payloads:
        if parent not in base_ids:
            errors.append("missing directory parent: %s" % parent)
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Belgium row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


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
        print("directory Belgium: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Belgium branches: 96 rows")
    for parent, count in sorted(EXPECTED.items()):
        print("%s: %d" % (parent, count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
