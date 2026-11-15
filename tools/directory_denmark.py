#!/usr/bin/env python3
"""Directory rows for Denmark.

The rows are grouped by parent IDs already present in the directory spine.
Several parents also cover other countries, so this module validates and
exports Denmark's contribution without writing shared branch payloads.

    python tools/directory_denmark.py --check
    python tools/directory_denmark.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-14"

EP_SWEDEN = "https://gomos.se/en/about-the-metropolis/parishes/"
ROMANIAN_DENMARK = (
    "https://episcopiascandinavia.se/"
    "parohiile-ortodoxe-romanesti-din-regatul-danemarcei/"
)
ROMANIAN_COPENHAGEN = "https://www.parohiaortodoxacopenhaga.dk/"
DANISH_ORTHODOX = "https://ortodoks.dk/om-menigheden/about-the-parish"
SERBIAN_DENMARK = "https://www.svetigeorgije.dk/crkva/"
SERBIAN_COPENHAGEN = "https://www.svetigeorgije.dk/"
SERBIAN_SILKEBORG = "https://svetidimitrije.dk/"
ROCOR_COPENHAGEN = (
    "https://directory.synod.com/listing/103/"
    "kirche-d-hl-alexander-nevskij/"
)
ROCOR_AARHUS = (
    "https://directory.synod.com/listing/104/"
    "den-hellige-bispemartyr-klements-menighed/"
)
ROCOR_AARHUS_CONTACT = "https://klementskirke.dk/kontakter/"
MOSCOW_DENMARK = "https://ortodoxy.dk/beta/US/site/about"
MOSCOW_COPENHAGEN = "https://ortodoxy.dk/beta/RU/news/show?id=1050"
MOSCOW_FREDERICIA = "https://ortodoxy.dk/beta/RU/news/show?id=1040"
MOSCOW_NYKOBING_FALSTER = "https://ortodoxy.dk/beta/RU/news/show?id=1026"
MACEDONIAN_DENMARK = "https://mpee.mk/category/k-o-p-e-n-x-a-g-e-n"
UOC_DENMARK = "https://orthodoxua.dk/about-2/"
UOC_CENTRAL = (
    "https://uoc-news.church/2024/02/20/"
    "keruyuchij-zaxidnojevropejskim-vikariatstvom-upc-vidvidav-daniyu/"
)
OCU_CENTRAL = (
    "https://www.pomisna.info/en/news/"
    "mytropolyt-epifanij-zustrivsya-z-generalnym-sekretarem-rady-tserkov-daniyi/"
)
OCU_DENMARK = "https://www.pcuvdanii.com/"


def row(row_id, parent, name, local, address, sources,
        rank="Parish", kind="parish", site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "DK",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


ROWS = {
    "ep-sweden": [
        row(
            "dk-ep-roskilde-saint-george-ioannina", "ep-sweden",
            "Saint George of Ioannina Greek Orthodox Parish in Roskilde",
            "St. George of Ioannina Greek Orthodox Parish in Roskilde",
            ["Katolsk Apostolisk kirke", "Toldbodgade 7",
             "4000 Roskilde"],
            [EP_SWEDEN],
        ),
    ],
    "ro-northern-europe": [
        row(
            "dk-ro-aalborg-entry-theotokos", "ro-northern-europe",
            "Entry of the Mother of God and Saints Pachomius and John Parish in Aalborg",
            "Parohia Intrarea în Biserică a Maicii Domnului și Sfinții Ierarhi Pahomie de la Gledinul Bistriței și Ioan de la Râșca și Secu, Episcopii Romanului",
            ["Vinkelvej 9", "9830 Tårs"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-aabenraa-nursing-theotokos", "ro-northern-europe",
            "Nursing Mother Icon and Saints Stelian, Alypius, and Nikon Parish in Aabenraa",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Cuvioși Stelian Paflagonul, Alipie Stâlpnicul și Nicon propovăduitorul pocăinței",
            ["Vestergarde 5", "Bolderslev", "6360"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-aarhus-theotokos-parascheva", "ro-northern-europe",
            "Lady of Jutland Icon and Saints Parascheva, Theodora, and Anna Parish in Aarhus",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Stăpâna Iutlandei\" de la Aarhus, Izvorul Tămăduirii și Sfintele Cuvioase Parascheva de la Iași, Teodora de la Sihla și Ana Vikinga de Novgorod",
            ["Vitten kirke", "Vittenvej 63", "8382 Hinnerup"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-grindsted-saint-john", "ro-northern-europe",
            "Sacrificial Love and Nursing Mother Icons and Saint John the Evangelist Parish in Grindsted",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Iubirea Jertfelnică\" și \"Alăptătoarea de la Țibleș\" și Sfântul Apostol și Evanghelist Ioan",
            ["Lovlundvej 21", "7190 Billund-Grindsted"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-billund-saint-elijah-filial", "dk-ro-grindsted-saint-john",
            "Saint Elijah the Tishbite Filial Parish in Billund",
            "Filia Sfântul Proroc Ilie Tesviteanul", [],
            [ROMANIAN_DENMARK], rank="Filial Parish",
        ),
        row(
            "dk-ro-copenhagen-nativity-theotokos", "ro-northern-europe",
            "Nativity of the Mother of God and Saints Gregory, Nicodemus, Macarius, and Mary Parish in Copenhagen",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Arătătoarea Căii\" și \"Alăptătoarea de la Țibleș\", Nașterea Maicii Domnului, Sfinții Cuvioși Grigorie Decapolitul și Nicodim cel Sfințit de la Tismana, Macarie Mărturisitorul și Maria Egipteanca",
            ["Kollegievej 2", "2920 Charlottenlund Gentofte",
             "Copenhagen"],
            [ROMANIAN_DENMARK, ROMANIAN_COPENHAGEN],
            site=ROMANIAN_COPENHAGEN,
        ),
        row(
            "dk-ro-bornholm-saint-marina-mission",
            "dk-ro-copenhagen-nativity-theotokos",
            "Saint Marina Mission on Bornholm",
            "Misiunea din Insula Bornholm Sfânta Mare Muceniță Marina", [],
            [ROMANIAN_DENMARK], rank="Mission",
        ),
        row(
            "dk-ro-copenhagen-danish-protection", "ro-northern-europe",
            "Danish Orthodox Parish of the Protection of the Mother of God",
            "Gudsmoders Beskyttelses Menighed",
            ["Dag Hammarskjölds Allé 1A, kld.", "2100 København Ø"],
            [ROMANIAN_DENMARK, DANISH_ORTHODOX], site="https://ortodoks.dk/",
        ),
        row(
            "dk-ro-aarhus-danish-protection-filial",
            "dk-ro-copenhagen-danish-protection",
            "Aarhus Filial Parish of the Danish Orthodox Protection Parish",
            "Filia Aarhus", [], [ROMANIAN_DENMARK, DANISH_ORTHODOX],
            rank="Filial Parish",
        ),
        row(
            "dk-ro-esbjerg-healer-icon", "ro-northern-europe",
            "Healer and Nursing Mother Icons and Saints Irene and Ephraim Parish in Esbjerg",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Vindecătoarea\" și \"Alăptătoarea de la Țibleș\", Sfânta Mare Muceniță Irina și Sfântul Cuvios Mucenic Efrem cel Nou",
            ["Jernbanegade 4", "6753 Agerbæk"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-fredericia-middelfart-nursing-theotokos", "ro-northern-europe",
            "Nursing Mother Icon and Saints Paisius and Cleopa Parish in Fredericia-Middelfart",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Cuvioși Paisie și Cleopa de la Sihăstria",
            ["Erritsø Bygade 87", "7000 Fredericia"],
            [ROMANIAN_DENMARK, "https://www.ortodoks-fredericia-middelfart.dk/"],
            site="https://www.ortodoks-fredericia-middelfart.dk/",
        ),
        row(
            "dk-ro-haderslev-nursing-theotokos", "ro-northern-europe",
            "Nursing Mother Icon and Saints Macarius, Autbert, and Vitmar Parish in Haderslev",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Cuvioși Macarie Protopsaltul de la București, Autbert și Vitmar",
            ["Laurids Skaus Gade 26", "6100 Haderslev"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-helsingor-nursing-theotokos", "ro-northern-europe",
            "Nursing Mother Icon and Saints Philothea and Elisabeth Parish in Helsingor",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfintele Cuvioase Filofteia și Elisabeta de la Pasărea",
            [], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-herning-ikast-saint-john", "ro-northern-europe",
            "Increase of Mind and Nursing Mother Icons and Saint John the Baptist Parish in Herning-Ikast",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Sporirea Minții\" și \"Alăptătoarea de la Țibleș\", Nașterea Sfântului Proroc Ioan Botezătorul și Sfântul Mucenic Ioan cel Nou de la Suceava",
            ["Bygaden 9", "7430 Ikast"],
            [ROMANIAN_DENMARK, "https://www.parohiaortodoxaromana-herning.dk/"],
            site="https://www.parohiaortodoxaromana-herning.dk/",
        ),
        row(
            "dk-ro-holstebro-theotokos-saint-nicholas", "ro-northern-europe",
            "Bearer of Him Who Bears All and Nursing Mother Icons Parish in Holstebro",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Purtătoarea Celui Ce poartă toate\" de la Holstebro și \"Alăptătoarea de la Țibleș\", Aducerea moaștelor Sfântului Ierarh Nicolae, Sfântul Proroc Isaia și Sfântul Mucenic Hristofor",
            ["Viborgvej 10B", "7500 Holstebro"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-horsens-myrrhbearers", "ro-northern-europe",
            "Myrrh-Bearer Icon and Holy Myrrh-Bearing Women Parish in Horsens",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Purtătoarea de mir\" de la Horsens și Sfintele Femei Mironosițe",
            ["Landevejen 6", "8350 Hundslund"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-jelling-hedensted-saints-macarius-gopon", "ro-northern-europe",
            "Nursing Mother Icon and Saints Macarius and Gopon Parish in Jelling-Hedensted",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Ierarhi Macarie, Episcopul Ierusalimului, și Gopon Mărturisitorul de la Jelling, Luminătorul Iutlandei",
            [], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-kollund-willibrord-willehad-mission", "ro-northern-europe",
            "Saints Willibrord and Willehad Mission in Kollund",
            "Misiunea Sfinții Ierarhi Vilibrord și Vilehad, Apostolii frizilor și danezilor",
            [], [ROMANIAN_DENMARK], rank="Mission",
        ),
        row(
            "dk-ro-nykobing-falster-saint-panteleimon", "ro-northern-europe",
            "Consolation of the Sorrowful Icon and Saint Panteleimon Parish in Nykobing Falster",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Mângâierea celor întristați\" de la Nykøbing Falster și Sfântul Mare Mucenic și Tămăduitor Pantelimon",
            ["Kirkegaardsvej 2", "4800 Nykøbing Falster"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-nykobing-mors-saint-tryphon", "ro-northern-europe",
            "Icon of the Holy Passion and Saints Tryphon, Perpetua, and Felicitas Parish in Nykobing Mors",
            "Parohia Cinstirea Icoanei Maicii Domnului \"a Sfintelor Pătimiri\" de la Nykøbing Mors, Sfântul Mucenic Trifon și Sfintele Mucenițe Perpetua și Felicitas",
            ["Råghøj 43", "7900 Nykøbing Mors"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-odense-transfiguration", "ro-northern-europe",
            "Lady of Funen Icon, Transfiguration, and Saints Demetrius and John Jacob Parish in Odense",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Stăpâna Insulei Funen\" de la Odense, Schimbarea la Față și Sfinții Cuvioși Dimitrie cel Nou din Basarabi și Ioan Iacob de la Neamț",
            ["Solgårdsvej 40", "5210 Odense NV"],
            [ROMANIAN_DENMARK, "https://www.ortodoks-odense.dk/"],
            site="https://www.ortodoks-odense.dk/",
        ),
        row(
            "dk-ro-svendborg-prophets-moses-elijah-filial",
            "dk-ro-odense-transfiguration",
            "Holy Prophets Moses and Elijah Filial Parish in Svendborg",
            "Parohia Sfinții Proroci Moise și Ilie Tesviteanul", [],
            [ROMANIAN_DENMARK], rank="Filial Parish",
        ),
        row(
            "dk-ro-ribe-liafdag-odinkar-mission", "ro-northern-europe",
            "Saints Liafdag and Odinkar the Younger Mission in Ribe",
            "Misiunea Sfântul Sfințit Mucenic Liafdag și Sfântul Ierarh Odincar cel Tânăr, Episcopi de Ribe",
            [], [ROMANIAN_DENMARK], rank="Mission",
        ),
        row(
            "dk-ro-ringkobing-skjern-irodion-theodgar", "ro-northern-europe",
            "Nursing Mother Icon and Saints Irodion and Theodgar Parish in Ringkobing-Skjern",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Cuvioși Irodion de la Lainici și Teodgar cel Sfințit de la Vestervig",
            ["Tarmvej 106", "6880 Tarm"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-roskilde-saint-ansgar", "ro-northern-europe",
            "Soothe Our Sorrows Icon, Romanian Saints, and Saint Ansgar Parish in Roskilde",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Potolește întristările noastre\" de la Roskilde, Sfinții Români și Sfântul Ierarh Ansgar și toți Luminătorii Nordului",
            ["Jernbanevej 57", "4340 Tølløse"],
            [ROMANIAN_DENMARK, "https://www.ortodoks-roskilde.dk/"],
            site="https://www.ortodoks-roskilde.dk/",
        ),
        row(
            "dk-ro-sonderborg-theophany", "ro-northern-europe",
            "Harbor of the Storm-Tossed Icon, Theophany, and Saints John Cassian and Germanus Parish in Sonderborg",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Limanul celor înviforați\" de la Sønderborg, Botezul Domnului și Sfinții Cuvioși Ioan Casian și Gherman din Dobrogea",
            ["Christianskirken", "Ringgade 102", "6400 Sønderborg"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-skagen-joseph-job", "ro-northern-europe",
            "Helper of the Humble Icon and Saints Joseph and Job Parish in Skagen",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Ajutătoarea celor smeriți\" de la Skagen și Sfinții și Drepții Iosif cel Preafrumos și Iov, mult răbdătorul",
            ["Vestre Strandvej 24", "9990 Skagen"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-tonder-burning-bush", "ro-northern-europe",
            "Burning Bush Icon and Saints Catherine and Mercurius Parish in Tonder",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Rugul Aprins\" de la Tønder, Sfânta Mare Muceniță Ecaterina și Sfântul Mare Mucenic Mercurie",
            ["Ribe Landevej 41", "6270 Tønder"], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-vejen-nursing-theotokos", "ro-northern-europe",
            "Nursing Mother Icon and Saints Macarius and Mary of Egypt Parish in Vejen",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\" și Sfinții Cuvioși Macarie Mărturisitorul, Egumenul Pelechitului, și Maria Egipteanca",
            [], [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-vejen-danish-odinkar-mission", "ro-northern-europe",
            "Danish Orthodox Mission of Saints Odinkar the Elder, Asa, and Odinkar the Younger in Vejen",
            "Misiunea Ortodoxă Daneză Sfântul Ierarh Odincar cel Bătrân, Episcop de Skara și Odense, Sfânta Cuvioasă Asa cea Desculță de la Bremen și Sfântul Ierarh Odincar cel Tânăr, Episcop de Ribe",
            [], [ROMANIAN_DENMARK], rank="Mission",
        ),
        row(
            "dk-ro-vejle-kolding-saints-niphon-macarius", "ro-northern-europe",
            "Joy of All Who Sorrow and Nursing Mother Icons Parish in Vejle-Kolding",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Bucuria tuturor celor necăjiți\" și \"Alăptătoarea de la Țibleș\", Sfântul Ierarh Nifon al Constanțianei și Sfinții Cuvioși Macarie cel Mare și Macarie Alexandrinul",
            ["Langelinie 78", "7100 Vejle"],
            [ROMANIAN_DENMARK],
        ),
        row(
            "dk-ro-vestervig-saint-theodgar-mission", "ro-northern-europe",
            "Saint Theodgar Mission in Vestervig",
            "Misiunea Sfântul Cuvios Teodgar cel Sfințit de la Vestervig, Luminătorul Peninsulei Iutlanda",
            [], [ROMANIAN_DENMARK], rank="Mission",
        ),
        row(
            "dk-ro-viborg-presentation", "ro-northern-europe",
            "Consoler Icon, Presentation of the Lord, and Saints Joseph and George Parish in Viborg",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Mângâietoarea\" de la Viborg, Întâmpinarea Domnului, Sfinții Cuvioși Iosif de la Văratec și Gheorghe de la Cernica și Căldărușani",
            ["Tingvej 3", "8832 Ulbjerg"], [ROMANIAN_DENMARK],
        ),
    ],
    "sr-scandinavia": [
        row(
            "dk-serbian-copenhagen-saint-george", "sr-scandinavia",
            "Serbian Orthodox Parish of Saint George in Copenhagen",
            "Парохија Светог Великомученика Георгија у Копенхагену",
            ["Tranehavevej 21", "2450 København SV"],
            [SERBIAN_DENMARK, SERBIAN_COPENHAGEN],
            site=SERBIAN_COPENHAGEN,
        ),
        row(
            "dk-serbian-silkeborg-saint-demetrius", "sr-scandinavia",
            "Serbian Orthodox Church of Saint Demetrius in Silkeborg",
            "Српска Православна Црква Свети Димитрије",
            ["Grauballe Gudenåvej 25", "8600 Silkeborg"],
            [SERBIAN_DENMARK, SERBIAN_SILKEBORG], site=SERBIAN_SILKEBORG,
        ),
        row(
            "dk-serbian-odense-saint-john-mission", "sr-scandinavia",
            "Serbian Orthodox Mission at Saint John's Church in Odense",
            "Српска православна мисија у Санкт Ханс Кирке",
            [],
            [SERBIAN_DENMARK], rank="Mission",
        ),
    ],
    "ru-germany-rocor": [
        row(
            "dk-rocor-copenhagen-saint-alexander-nevsky", "ru-germany-rocor",
            "Saint Alexander Nevsky Church in Copenhagen",
            "Церковь святого благоверного князя Александра Невского",
            ["Bredgade 53", "1260 København K"], [ROCOR_COPENHAGEN],
            site="https://ruskirke.dk/",
        ),
        row(
            "dk-rocor-aarhus-saint-clement", "ru-germany-rocor",
            "Holy Hieromartyr Clement of Rome Parish in Aarhus",
            "Den Hellige Bispemartyr Klements Menighed",
            ["Tabor", "Vølundsvej 8", "8230 Åbyhøj"],
            [ROCOR_AARHUS, ROCOR_AARHUS_CONTACT],
            site="https://klementskirke.dk/",
        ),
    ],
    "russia": [
        row(
            "dk-russia-copenhagen-saint-alexander-nevsky", "russia",
            "Parish of Saint Alexander Nevsky in Copenhagen",
            "Приход святого благоверного князя Александра Невского в Копенгагене",
            ["Tranehavevej 21", "2450 København SV"],
            [MOSCOW_DENMARK, MOSCOW_COPENHAGEN],
            site="https://ortodoxy.dk/",
        ),
        row(
            "dk-russia-hobro-saint-nicholas", "russia",
            "Church of Saint Nicholas in Hobro",
            "Храм святителя Николая Чудотворца в Хобро",
            ["Onsildgade 1", "9500 Hobro"], [MOSCOW_DENMARK],
            site="https://ortodoxy.dk/",
        ),
        row(
            "dk-russia-baagoe-royal-martyrs", "russia",
            "Church of the Holy Royal Passion-Bearers of Russia on Baagoe",
            "Храм святых Царственных страстотерпцев на острове Баагё",
            ["Prinsehøjsvej 35", "5160 Baagø", "Assens"],
            [MOSCOW_DENMARK], site="https://ortodoxy.dk/",
        ),
        row(
            "dk-russia-fredericia-worship-site", "russia",
            "Moscow Patriarchate Worship Site in Fredericia",
            "Место богослужений Русской Православной Церкви во Фредерисии",
            ["Sjællandsgade 48", "7000 Fredericia"],
            [MOSCOW_FREDERICIA], rank="Worship Site",
            site="https://ortodoxy.dk/",
        ),
        row(
            "dk-russia-nykobing-falster-worship-site", "russia",
            "Moscow Patriarchate Worship Site in Nykobing Falster",
            "Место богослужений Русской Православной Церкви в Нюкёбинге-Фальстере",
            ["Lindeskovkirken", "Grønsundsvej 32",
             "4800 Nykøbing Falster"],
            [MOSCOW_NYKOBING_FALSTER], rank="Worship Site",
            site="https://ortodoxy.dk/",
        ),
    ],
    "mk-europe": [
        row(
            "dk-macedonian-copenhagen-saint-clement", "mk-europe",
            "Saint Clement of Ohrid Macedonian Orthodox Church Community in Copenhagen",
            "МПЦО Свети Климент Охридски Копенхаген",
            ["Nitives 17", "2000 Frederiksberg"], [MACEDONIAN_DENMARK],
            rank="Church Community",
        ),
    ],
    "ukraine-uoc": [
        row(
            "dk-uoc-holstebro-protection", "ukraine-uoc",
            "Parish of the Protection of the Most Holy Theotokos in Holstebro",
            "Парафія Покрови Пресвятої Богородиці в Хольстебро",
            ["Danmarksgade 23", "7500 Holstebro"],
            [UOC_DENMARK, UOC_CENTRAL], site="https://orthodoxua.dk/",
        ),
        row(
            "dk-uoc-bramming-saint-nicholas", "ukraine-uoc",
            "Parish of Saint Nicholas in Bramming",
            "Парафія святителя Миколая Чудотворця в Браммінгу",
            ["N. A. Jørgensens Plads 2", "6740 Bramming"],
            [UOC_DENMARK, UOC_CENTRAL], site="https://orthodoxua.dk/",
        ),
        row(
            "dk-uoc-roskilde-pochaev-icon", "ukraine-uoc",
            "Parish of the Pochaev Icon of the Mother of God in Roskilde",
            "Парафія Почаївської ікони Божої Матері в Роскілле",
            ["Kurhusvænge 3", "4000 Roskilde"],
            [UOC_DENMARK, UOC_CENTRAL], site="https://orthodoxua.dk/",
        ),
    ],
    "ukraine-ocu": [
        row(
            "dk-ocu-copenhagen-community", "ukraine-ocu",
            "Ukrainian Orthodox Community in Copenhagen",
            "Українська православна громада в Копенгагені", [],
            [OCU_CENTRAL, OCU_DENMARK], rank="Community",
            site=OCU_DENMARK,
        ),
        row(
            "dk-ocu-ferslev-community", "ukraine-ocu",
            "Ukrainian Orthodox Community in Ferslev",
            "Українська православна громада у Ферслеві", [],
            [OCU_CENTRAL, OCU_DENMARK], rank="Community",
            site=OCU_DENMARK,
        ),
        row(
            "dk-ocu-kolding-community", "ukraine-ocu",
            "Ukrainian Orthodox Community in Kolding",
            "Українська православна громада в Колдінгу", [],
            [OCU_CENTRAL, OCU_DENMARK], rank="Community",
            site=OCU_DENMARK,
        ),
        row(
            "dk-ocu-gram-community", "ukraine-ocu",
            "Ukrainian Orthodox Community in Gram",
            "Українська православна громада в Грамі", [],
            [OCU_CENTRAL, OCU_DENMARK], rank="Community",
            site=OCU_DENMARK,
        ),
        row(
            "dk-ocu-haderslev-community", "ukraine-ocu",
            "Ukrainian Orthodox Community in Haderslev",
            "Українська православна громада в Гадерслеві", [],
            [OCU_CENTRAL, OCU_DENMARK], rank="Community",
            site=OCU_DENMARK,
        ),
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "ep-sweden": 1,
    "mk-europe": 1,
    "ro-northern-europe": 33,
    "ru-germany-rocor": 2,
    "russia": 5,
    "sr-scandinavia": 3,
    "ukraine-ocu": 5,
    "ukraine-uoc": 3,
}


# Convenience exports for aggregators that merge direct local-church rows.
DIRECT_RUSSIA_ROWS = ROWS["russia"]


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
    allowed_kinds = {"parish", "monastery"}
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
            if item.get("kind") not in allowed_kinds:
                raise ValueError("%s has unsupported kind: %s" %
                                 (row_id, item.get("kind")))
            if item.get("country") != "DK":
                raise ValueError("%s is outside Denmark" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "DK",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Denmark parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 53:
        raise ValueError("Denmark English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": ["DK"],
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
        print("directory Denmark: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Denmark branches: 53 rows")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
