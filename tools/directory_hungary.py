#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Hungary.

The official-source union preserves overlapping jurisdictions and separately
listed bodies at shared addresses. It does not decide property claims.

    python tools/directory_hungary.py --check
    python tools/directory_hungary.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-15"

SERBIAN_BUDA = (
    "https://www.serbdiocese.hu/eparhija/parohije/"
    "arhijerejsko-namesnishtvo-budimsko/"
)
SERBIAN_MOHACS = (
    "https://www.serbdiocese.hu/eparhija/parohije/"
    "arhijerejsko-namesnistvo-mohacko/"
)
SERBIAN_SZEGED = (
    "https://www.serbdiocese.hu/eparhija/parohije/"
    "arhijerejsko-namesnishtvo-segedinsko/"
)
SERBIAN_KOVIN = (
    "https://www.serbdiocese.hu/eparhija/manastiri/manastir-srpski-kovin/"
)
SERBIAN_GRABOVAC = (
    "https://www.serbdiocese.hu/eparhija/manastiri/manastir-grabovac/"
)

RUSSIAN_DIRECTORY = "https://magyarortodox.hu/?page_id=36"
RUSSIAN_DIRECTORY_HU = "https://magyarortodox.com/templomaink/"

EP_ORGANISATIONS = (
    "https://patriarchatus.hu/szervezeti-felepitesunk-elerhetosegeink/"
)
EP_MAP = (
    "https://wien.metropolisvonaustria.at/de/metropolis-de/"
    "pfarreien-de/landkarte-mit-den-pfarreien"
)
EP_EXARCHATE = (
    "https://patriarchatus.hu/exarchatus/"
    "konstantinapolyi-egyetemes-patriarchatus-magyarorszagi-"
    "orthodox-exarchatusa/"
)

BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"

ROMANIAN_DIOCESE = (
    "https://patriarhia.ro/en/dioceses/romanian-orthodox-diocese-of-hungary/"
)
ROMANIAN_COUNT = (
    "https://arhiva.patriarhia.ro/"
    "comunitaile-bisericesti-externe-in-anul-2023-2871.html"
)
ROMANIAN_FACTBOX = (
    "https://basilica.ro/factbox-ortodoxia-romaneasca-in-ungaria/"
)
ROMANIAN_ROSTER = (
    "https://bibliotecaromaneasca-hu.ro/biserici-romanesti-in-ungaria/"
)
ROMANIAN_SILUAN = (
    "https://patriarhia.ro/sfantul-sinod/"
    "siluan-episcopul-ortodox-roman-al-ungariei/"
)

UOC_BUDAPEST = (
    "https://uoc-news.church/2026/08/21/"
    "ijerarxi-upc-vidvidali-ukrajinski-parafiji-u-shveciji-norvegiji-ta-"
    "ugorshhini/"
)
UOC_RAJKA = (
    "https://vzcz.church.ua/2026/09/19/"
    "jepiskop-veniamin-vidvidav-parafiji-upc-v-avstriji-ta-ugorshhini/"
)


def row(row_id, parent, name, local, sources, rank="Parish", kind="parish",
        address=None, site=None, founded=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "HU",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    if founded:
        value["founded"] = founded
    return value


def rows_from_specs(parent, source, prefix, specs):
    answer = []
    for spec in specs:
        slug, name, local, rank, address = spec
        answer.append(row(
            "hu-%s-%s" % (prefix, slug), parent, name, local, [source],
            rank=rank, kind="monastery" if rank == "Monastery" else "parish",
            address=address,
        ))
    return answer


SERBIAN_BUDA_SPECS = [
    ("racalmas-ascension", "Ascension of the Lord Serbian Orthodox Church in Rácalmás",
     "Храм Вазнесења Господњег у Аљмашу", "Church", ["Rác köz", "2459 Rácalmás, Hungary"]),
    ("szazhalombatta-nativity", "Nativity of the Theotokos Serbian Orthodox Church in Százhalombatta",
     "Храм Рођења Пресвете Богородице у Бати", "Church", ["Szent László út 94", "2440 Százhalombatta, Hungary"]),
    ("budapest-george", "Holy Great Martyr George Serbian Orthodox Church in Budapest",
     "Храм Светог Великомученика Георгија у Будимпешти", "Church", ["Szerb utca 33", "Budapest, Hungary"]),
    ("dunaujvaros-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Dunaújváros",
     "Храм Преноса моштију Светог Николаја у Дунапантелији", "Church", ["Táltos u. 7", "2400 Dunaújváros, Hungary"]),
    ("dunafoldvar-trinity", "Holy Trinity Serbian Orthodox Church in Dunaföldvár",
     "Храм Свете Тројице у Дунафелдвару", "Church", ["Kossuth Lajos utca 7", "7020 Dunaföldvár, Hungary"]),
    ("gyor-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Győr",
     "Храм Преноса моштију Светог Николаја у Ђуру", "Church", ["Bálint Mihály u. 54", "Győr, Hungary"]),
    ("budakalasz-gabriel", "Holy Archangel Gabriel Serbian Orthodox Church in Budakalász",
     "Храм Светог Архангела Гаврила у Калазу", "Church", ["Kálvária u. 4", "2011 Budakalász, Hungary"]),
    ("lorev-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Lórév",
     "Храм Преноса моштију Светог Николаја у Ловри", "Church", ["Csarnojevity Arzen utca 114/A", "2309 Lórév, Hungary"]),
    ("eger-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Eger",
     "Храм Преноса моштију Светог Николаја у Јегри", "Church", ["Vitkovits Mihály u.", "Eger, Hungary"]),
    ("pomaz-george", "Holy Great Martyr George Serbian Orthodox Church in Pomáz",
     "Храм Светог Великомученика Георгија у Помазу", "Church", ["Szerb utca 8", "Pomáz, Hungary"]),
    ("szentendre-dormition-cathedral", "Dormition of the Theotokos Serbian Orthodox Cathedral in Szentendre",
     "Саборни храм Успења Пресвете Богородице у Сентандреји", "Cathedral", ["Pátriárka u. 5", "2000 Szentendre, Hungary"]),
    ("szentendre-michael", "Holy Archangel Michael Serbian Orthodox Church in Szentendre",
     "Храм Светог Архангела Михаила у Сентандреји", "Church", ["Kossuth Lajos u.", "Szentendre, Hungary"]),
    ("szentendre-annunciation", "Annunciation of the Theotokos Serbian Orthodox Church in Szentendre",
     "Храм Благовести Пресвете Богородице у Сентандреји", "Church", ["Fő tér", "Szentendre, Hungary"]),
    ("szentendre-transfiguration", "Transfiguration of the Lord Serbian Orthodox Church in Szentendre",
     "Храм Преображења Господњег у Сентандреји", "Church", ["Bogdányi u. 42", "Szentendre, Hungary"]),
    ("szekesfehervar-john-baptist", "Nativity of St John the Baptist Serbian Orthodox Church in Székesfehérvár",
     "Храм Рођења Светог Јована Крститеља у Стоном Београду", "Church", ["Rác utca 17", "Székesfehérvár, Hungary"]),
    ("csobanka-gabriel", "Holy Archangel Gabriel Serbian Orthodox Church in Csobánka",
     "Храм Светог Архангела Гаврила у Чобанцу", "Church", ["Vörösvári út 1", "Csobánka, Hungary"]),
    ("szigetcsep-stephen-decani", "St Stephen of Dečani Serbian Orthodox Church in Szigetcsép",
     "Храм Светог Краља Стефана Дечанског у Чипу", "Church", ["Fő u. 120", "2317 Szigetcsép, Hungary"]),
]


SERBIAN_MOHACS_SPECS = [
    ("baja-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Baja",
     "Храм Преноса моштију Светог Николаја у Баји", "Church", ["Miklós utca 4", "6500 Baja, Hungary"]),
    ("beremend-ascension", "Ascension of Christ Serbian Orthodox Church in Beremend",
     "Храм Вазнесења Христовог у Бремену", "Church", ["Kossuth Lajos u. 64", "Beremend, Hungary"]),
    ("villany-dormition", "Dormition of the Theotokos Serbian Orthodox Church in Villány",
     "Храм Успења Пресвете Богородице у Вилању", "Church", ["Móra Ferenc u. 1", "Villány, Hungary"]),
    ("ilocska-paraskeva", "St Paraskeva Serbian Orthodox Church in Ilocska",
     "Храм Преподобне Мајке Параскеве у Илочцу", "Church", ["Ilocska, Hungary"]),
    ("lippo-john-baptist", "Nativity of St John the Baptist Serbian Orthodox Church in Lippó",
     "Храм Рођења Светог Јована Крститеља у Липови", "Church", ["Lippó, Hungary"]),
    ("magyarboly-luke", "Holy Apostle and Evangelist Luke Serbian Orthodox Church in Magyarbóly",
     "Храм Светог апостола и еванђелиста Луке у Мађарбоји", "Church", ["Kossuth Lajos u. 42", "Magyarbóly, Hungary"]),
    ("majs-paraskeva", "St Paraskeva Serbian Orthodox Church in Majs",
     "Храм Преподобне Мајке Параскеве у Мајшу", "Church", ["Majs, Hungary"]),
    ("medina-trinity", "Holy Trinity Serbian Orthodox Church in Medina",
     "Храм Свете Тројице у Медини", "Church", ["Kossuth Lajos u. 13", "Medina, Hungary"]),
    ("mohacs-trinity", "Holy Trinity Serbian Orthodox Church in Mohács",
     "Храм Свете Тројице у Мохачу", "Church", ["Korsós u. 2", "Mohács, Hungary"]),
    ("mohacs-constantine-helena", "Sts Constantine and Helena Serbian Orthodox Cemetery Chapel in Mohács",
     "Гробљанска капела Светих цара Константина и царице Јелене у Мохачу", "Cemetery Chapel", ["Mohács, Hungary"]),
    ("pecs-andronicus-junia", "Holy Apostles Andronicus and Junia Serbian Orthodox Church in Pécs",
     "Храм Светих апостола Андроника и Јуније у Печују", "Church", ["Zrínyi Miklós u. 15", "7621 Pécs, Hungary"]),
    ("erdosmecske-demetrios", "Holy Great Martyr Demetrios Serbian Orthodox Church in Erdősmecske",
     "Храм Светог Великомученика Димитрија у Рацмечки", "Church", ["Erdősmecske, Hungary"]),
    ("hercegszanto-nativity", "Nativity of the Theotokos Serbian Orthodox Church in Hercegszántó",
     "Храм Рођења Пресвете Богородице у Сантову", "Church", ["Alkotmány tér 3", "Hercegszántó, Hungary"]),
    ("dunaszekcso-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Dunaszekcső",
     "Храм Преноса моштију Светог Николаја у Сечују", "Church", ["Május 1. tér", "Dunaszekcső, Hungary"]),
    ("sarok-demetrios", "Holy Great Martyr Demetrios Serbian Orthodox Church in Sárok",
     "Храм Светог Великомученика Димитрија у Шароку", "Church", ["Sárok, Hungary"]),
    ("siklos-demetrios", "Holy Great Martyr Demetrios Serbian Orthodox Church in Siklós",
     "Храм Светог Великомученика Димитрија у Шиклошу", "Church", ["Táncsics u. 2", "Siklós, Hungary"]),
    ("somberek-george", "Holy Great Martyr George Serbian Orthodox Church in Somberek",
     "Храм Светог Великомученика Георгија у Шумберку", "Church", ["Somberek, Hungary"]),
]


SERBIAN_MOHACS_PARISHES = [
    ("alsonana", "Alsónána", "Доња Нана"),
    ("vemend", "Véménd", "Вемен"),
    ("gorcsonydoboka", "Görcsönydoboka", "Рац Гарчин"),
    ("szalka", "Szálka", "Салка"),
    ("bataszek", "Bátaszék", "Батосек"),
    ("borjad", "Borjád", "Борјад"),
    ("nagybudmer", "Nagybudmér", "Велики Будмир"),
    ("ivandarda", "Ivándárda", "Ивандарда"),
    ("lanycsok", "Lánycsók", "Ланчук"),
    ("liptod", "Liptód", "Литоба"),
    ("pecsvarad", "Pécsvárad", "Печварад"),
    ("pocsa", "Pócsa", "Поча"),
    ("egyhaskozar", "Egyházaskozár", "Рацкозар"),
    ("hidas", "Hidas", "Рацхидош"),
    ("szigetvar", "Szigetvár", "Сигетвар"),
    ("hercegtottos", "Hercegtöttös", "Титош"),
]


SERBIAN_SZEGED_SPECS = [
    ("battonya-nativity", "Nativity of the Theotokos Serbian Orthodox Church in Battonya",
     "Храм Рођења Пресвете Богородице у Батањи", "Church", ["Battonya, Hungary"]),
    ("hodmezovasarhely-nativity", "Nativity of the Theotokos Serbian Orthodox Church in Hódmezővásárhely",
     "Храм Рођења Пресвете Богородице у Вашархељу", "Church", ["Dr. Rapcsák András utca 7", "6800 Hódmezővásárhely, Hungary"]),
    ("hodmezovasarhely-constantine-helena", "Sts Constantine and Helena Serbian Orthodox Cemetery Chapel in Hódmezővásárhely",
     "Гробљанска капела Светих цара Константина и царице Јелене у Вашархељу", "Cemetery Chapel", ["Hódmezővásárhely, Hungary"]),
    ("deszk-transfiguration", "Transfiguration of the Lord Serbian Orthodox Church in Deszk",
     "Храм Преображења Господњег у Дески", "Church", ["Széchenyi István utca 39", "6772 Deszk, Hungary"]),
    ("ujszentivan-dormition", "Dormition of the Theotokos Serbian Orthodox Church in Újszentiván",
     "Храм Успења Пресвете Богородице у Новом Сентивану", "Church", ["Felszabadulás utca 1", "6754 Újszentiván, Hungary"]),
    ("szeged-nicholas", "Translation of the Relics of St Nicholas Serbian Orthodox Church in Szeged",
     "Храм Преноса моштију Светог Николаја у Сегедину", "Church", ["Somogyi u. 3", "Szeged, Hungary"]),
    ("szoreg-nativity", "Nativity of the Theotokos Serbian Orthodox Church in Szőreg",
     "Храм Рођења Пресвете Богородице у Сиригу", "Church", ["Szőreg, Hungary"]),
    ("magyarcsanad-george", "Holy Great Martyr George Serbian Orthodox Church in Magyarcsanád",
     "Храм Светог Великомученика Георгија у Чанаду", "Church", ["Fő u. 49", "Magyarcsanád, Hungary"]),
]


SERBIAN_ROWS = (
    rows_from_specs("sr-buda", SERBIAN_BUDA, "sr", SERBIAN_BUDA_SPECS) +
    rows_from_specs("sr-buda", SERBIAN_MOHACS, "sr", SERBIAN_MOHACS_SPECS) +
    [row(
        "hu-sr-%s-parish" % slug, "sr-buda",
        "Serbian Orthodox Parish in %s" % town,
        "Српска православна парохија %s" % local,
        [SERBIAN_MOHACS], address=[town + ", Hungary"],
    ) for slug, town, local in SERBIAN_MOHACS_PARISHES] +
    rows_from_specs("sr-buda", SERBIAN_SZEGED, "sr", SERBIAN_SZEGED_SPECS) +
    [
        row("hu-sr-rackeve-kovin-monastery", "sr-buda",
            "Serbian Kovin Monastery in Ráckeve", "Манастир Српски Ковин",
            [SERBIAN_KOVIN], rank="Monastery", kind="monastery",
            address=["Ráckeve, Hungary"]),
        row("hu-sr-graboc-monastery", "sr-buda",
            "Grábóc Serbian Orthodox Monastery", "Манастир Грабовац",
            [SERBIAN_GRABOVAC], rank="Monastery", kind="monastery",
            address=["Grábóc, Hungary"]),
    ]
)


RUSSIAN_SPECS = [
    ("budapest-dormition", "Dormition of the Theotokos Hungarian Orthodox Cathedral",
     "Nagyboldogasszony magyar ortodox székesegyház", "Cathedral", ["Petőfi tér 2", "1052 Budapest, Hungary"]),
    ("budapest-holy-trinity", "Holy Trinity Russian Orthodox Parish in Budapest",
     "Szent Háromság orosz ortodox egyházközség", "Parish", ["Petőfi tér 2", "1052 Budapest, Hungary"]),
    ("budapest-sergius", "St Sergius of Radonezh Russian Orthodox Church in Budapest",
     "Radonyezsi Szent Szergij orosz ortodox templom", "Church", ["Lendvay u. 26", "1062 Budapest, Hungary"]),
    ("urom-alexandra", "Holy Martyr Alexandra Russian Orthodox Church in Üröm",
     "Szent Alexandra vértanú templom", "Church", ["Patak u. 6", "2096 Üröm, Hungary"]),
    ("miskolc-trinity", "Holy Trinity Hungarian Orthodox Church in Miskolc",
     "Szent Háromság magyar ortodox templom", "Church", ["Deák tér 7", "3525 Miskolc, Hungary"]),
    ("debrecen-trinity", "Holy Trinity Hungarian Orthodox Church in Debrecen",
     "Szent Háromság magyar ortodox templom", "Church", ["Késmárk u. 7/c", "4029 Debrecen, Hungary"]),
    ("nyiregyhaza-george", "Holy Great Martyr George Hungarian Orthodox Church in Nyíregyháza",
     "Szent György nagyvértanú magyar ortodox templom", "Church", ["Széchenyi tér 5", "4400 Nyíregyháza, Hungary"]),
    ("szeged-george", "Holy Great Martyr George Hungarian Orthodox Church in Szeged",
     "Szent György nagyvértanú magyar ortodox templom", "Church", ["Kazinczy u. 7", "6720 Szeged, Hungary"]),
    ("gyongyos-nicholas", "St Nicholas Hungarian Orthodox Church in Gyöngyös",
     "Szent Miklós magyar ortodox templom", "Church", ["Vachott Sándor u. 12", "3200 Gyöngyös, Hungary"]),
    ("tokaj-nicholas", "St Nicholas Hungarian Orthodox Church in Tokaj",
     "Szent Miklós magyar ortodox templom", "Church", ["Bethlen Gábor u. 15", "3910 Tokaj, Hungary"]),
    ("heviz-life-giving-spring", "Life-Giving Spring Icon Russian Orthodox Church in Hévíz",
     "Az Életet adó forrás ikonja orosz ortodox templom", "Church", ["Ady Endre utca 15", "8380 Hévíz, Hungary"]),
]

RUSSIAN_ROWS = rows_from_specs(
    "ru-budapest-and-hungary", RUSSIAN_DIRECTORY_HU, "ru", RUSSIAN_SPECS)


EP_SPECS = [
    ("budapest-three-hierarchs", "Church of the Three Holy Hierarchs in Budapest",
     "A Három Szent Főpap temploma", "Church", ["Múzeum utca 11", "1088 Budapest, Hungary"]),
    ("budapest-dormition", "Dormition of the Theotokos Church in Budapest",
     "Nagyboldogasszony templom", "Church", ["Petőfi tér 2", "1052 Budapest, Hungary"]),
    ("budapest-piroska", "St Piroska Chapel in Budapest",
     "Árpád-házi Szent Piroska kápolna", "Chapel", ["II. János Pál pápa tér 19", "1081 Budapest, Hungary"]),
    ("budapest-hierotheos-stephen", "Sts Hierotheos and Stephen Parish in Budapest",
     "Szent Hierotheosz és Szent István Görögkeleti Egyházközség", "Parish", ["Váci utca 55", "1056 Budapest, Hungary"]),
    ("budapest-annunciation-ukrainian", "Ukrainian-speaking Annunciation of the Theotokos Orthodox Community in Budapest",
     "A Legszentebb Istenszülő Szűz Mária Örömhírvétele Ukrán Ortodox Közösség", "Community", None),
    ("beloiannisz-demetrios", "St Demetrios and Sts Constantine and Helena Greek Orthodox Church in Beloiannisz",
     "Szent Demeter, Szent Konstantin és Szent Ilona görögkeleti templom", "Church", ["Szent Konstantin park 1", "2455 Beloiannisz, Hungary"]),
    ("szentes-nicholas", "St Nicholas Greek Orthodox Church in Szentes",
     "Szent Miklós Görögkeleti Egyházközség", "Church", ["Kossuth Lajos utca 4", "6600 Szentes, Hungary"]),
    ("kecskemet-trinity", "Holy Trinity Greek Orthodox Church in Kecskemét",
     "Szentháromság görögkeleti templom", "Church", ["Széchenyi tér 9", "6000 Kecskemét, Hungary"]),
    ("karcag-george", "St George Greek Orthodox Church in Karcag",
     "Szent György görögkeleti templom", "Church", ["Horváth Ferenc utca 2", "5300 Karcag, Hungary"]),
    ("szigetszentmiklos-nicholas", "St Nicholas Greek Orthodox Parish in Szigetszentmiklós",
     "Szent Miklós Görögkeleti Egyházközség", "Parish", ["Eklézsia utca 6", "2310 Szigetszentmiklós, Hungary"]),
    ("alfold-parish-group", "Great Plain Greek Orthodox Parish Group",
     "Alföldi Görögkeleti Parochia", "Parish Group", None),
]

EP_ROWS = rows_from_specs("ep-austria", EP_MAP, "ep", EP_SPECS)
for item in EP_ROWS:
    item["sources"] = [EP_ORGANISATIONS, EP_MAP, EP_EXARCHATE]


BULGARIAN_ROWS = [
    row("hu-bg-budapest-cyril-methodius", "bg-western-central-europe",
        "Sts Cyril and Methodius Bulgarian Orthodox Cathedral in Budapest",
        "Катедрален храм Св. св. Кирил и Методий",
        [BULGARIAN_DIRECTORY], rank="Cathedral",
        address=["Vágóhíd utca 15", "1097 Budapest, Hungary"]),
    row("hu-bg-budapest-tryphon", "bg-western-central-europe",
        "Holy Martyr Tryphon Bulgarian Orthodox Chapel in Budapest",
        "Параклис Св. мъченик Трифон",
        [BULGARIAN_DIRECTORY], rank="Chapel",
        address=["Vágóhíd utca 15", "1097 Budapest, Hungary"]),
    row("hu-bg-pecs-john-rila", "bg-western-central-europe",
        "St John of Rila Bulgarian Orthodox Chapel in Pécs",
        "Параклис Св. Йоан Рилски в Пейч",
        [BULGARIAN_DIRECTORY], rank="Chapel",
        address=["Pécs, Hungary"]),
]


ROMANIAN_SPECS = [
    ("elek-nicholas", "St Nicholas Romanian Orthodox Chapel in Elek",
     "Capela ortodoxă română Sfântul Nicolae din Aletea", "Chapel", ["Lökösházi u. 40", "5742 Elek, Hungary"]),
    ("korosszegapati-nicholas", "St Nicholas Romanian Orthodox Church in Körösszegapáti",
     "Biserica ortodoxă română Sfântul Nicolae din Apateu", "Church", ["Kossuth u. 17", "Körösszegapáti, Hungary"]),
    ("battonya-george", "St George Romanian Orthodox Church in Battonya",
     "Biserica ortodoxă română Sfântul Gheorghe din Bătania", "Church", ["Hunyadi u. 42", "Battonya, Hungary"]),
    ("bekes-nativity", "Nativity of the Theotokos Romanian Orthodox Church in Békés",
     "Biserica ortodoxă română Nașterea Maicii Domnului din Bichiș", "Church", ["Kossuth u. 5", "Békés, Hungary"]),
    ("bekescsaba-nicholas", "St Nicholas Romanian Orthodox Church in Békéscsaba",
     "Biserica ortodoxă română Sfântul Nicolae din Bichișciaba", "Church", ["Bartók Béla út 51-53", "Békéscsaba, Hungary"]),
    ("budapest-john-baptist", "St John the Baptist Romanian Orthodox Church in Budapest",
     "Biserica ortodoxă română Sfântul Ioan Botezătorul din Budapesta", "Church", ["Holló u. 8", "1075 Budapest, Hungary"]),
    ("magyarcsanad-ascension", "Ascension of the Lord Romanian Orthodox Church in Magyarcsanád",
     "Biserica ortodoxă română Înălțarea Domnului din Cenadul Unguresc", "Church", ["Templom tér", "Magyarcsanád, Hungary"]),
    ("ketegyhaza-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Kétegyháza",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Chitighaz", "Church", ["Fő tér", "Kétegyháza, Hungary"]),
    ("csorvas-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Csorvás",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Ciorvaș", "Church", ["Szabadság tér", "Csorvás, Hungary"]),
    ("sarkadkeresztur-annunciation", "Annunciation Romanian Orthodox Chapel in Sarkadkeresztúr",
     "Capela ortodoxă română Bunavestire din Crâstor", "Chapel", ["Gárdonyi u. 3", "Sarkadkeresztúr, Hungary"]),
    ("darvas-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Darvas",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Darvaș", "Church", ["Rákóczi u. 71", "Darvas, Hungary"]),
    ("zsaka-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Zsáka",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Jaca", "Church", ["Kossuth u. 15", "Zsáka, Hungary"]),
    ("gyula-nicholas-cathedral", "St Nicholas Romanian Orthodox Cathedral in Gyula",
     "Catedrala Episcopală Ortodoxă Română Sfântul Nicolae din Jula", "Cathedral", ["Szent Miklós park 2", "5700 Gyula, Hungary"]),
    ("gyula-paraskeva", "St Paraskeva Romanian Orthodox Church in Gyula",
     "Biserica ortodoxă română Sfânta Cuvioasă Parascheva din Jula Mică", "Church", ["Jász Lukács u. 9", "Gyula, Hungary"]),
    ("mehkerek-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Méhkerék",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Micherechi", "Church", ["Kossuth u. 77", "Méhkerék, Hungary"]),
    ("pusztaottlaka-ascension", "Ascension of the Lord Romanian Orthodox Church in Pusztaottlaka",
     "Biserica ortodoxă română Înălțarea Domnului din Otlaca-Pustă", "Church", ["Kossuth u. 15-17", "Pusztaottlaka, Hungary"]),
    ("mezopeterd-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Mezőpeterd",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Peterd", "Church", ["Petőfi u. 50", "Mezőpeterd, Hungary"]),
    ("korosszakal-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Körösszakál",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Săcal", "Church", ["Templom u. 16", "Körösszakál, Hungary"]),
    ("szeged-annunciation-silouan", "Annunciation and St Silouan the Athonite Romanian Orthodox Chapel in Szeged",
     "Capela ortodoxă română Bunavestire și Sfântul Cuvios Siluan Athonitul din Seghedin", "Chapel", ["Szent-Györgyi Albert u. 16-24", "Szeged, Hungary"]),
    ("vekert-archangels", "Holy Archangels Michael and Gabriel Romanian Orthodox Church in Vekerd",
     "Biserica ortodoxă română Sfinții Arhangheli Mihail și Gavriil din Vecherd", "Church", ["Kossuth u. 7", "Vekerd, Hungary"]),
]

ROMANIAN_ROWS = rows_from_specs(
    "ro-hungary", ROMANIAN_ROSTER, "ro", ROMANIAN_SPECS)
for item in ROMANIAN_ROWS:
    item["sources"] = [ROMANIAN_DIOCESE, ROMANIAN_FACTBOX, ROMANIAN_ROSTER]
ROMANIAN_ROWS.extend([
    row("hu-ro-budapest-john-baptist-monastic", "ro-hungary",
        "St John the Baptist Romanian Orthodox Monastic Establishment in Budapest",
        "Așezământul Monahal Sfântul Ioan Botezătorul din Budapesta",
        [ROMANIAN_COUNT, ROMANIAN_ROSTER], rank="Monastery", kind="monastery",
        address=["Holló u. 8", "1075 Budapest, Hungary"]),
    row("hu-ro-korosszakal-dormition-monastery", "ro-hungary",
        "Dormition of the Theotokos Romanian Orthodox Monastery in Körösszakál",
        "Mănăstirea Adormirea Maicii Domnului din Săcal",
        [ROMANIAN_COUNT, ROMANIAN_SILUAN], rank="Monastery", kind="monastery",
        address=["Körösszakál, Hungary"]),
])


UOC_ROWS = [
    row("hu-uoc-budapest-stephen", "ukraine-uoc",
        "St Stephen I, King of Hungary Ukrainian Orthodox Parish in Budapest",
        "Парафія святого праведного Стефана І, короля Угорщини, у Будапешті",
        [UOC_BUDAPEST]),
    row("hu-uoc-rajka-mission", "ukraine-uoc",
        "Ukrainian Orthodox Mission Centre in Rajka",
        "Місіонерський осередок Української Православної Церкви в Райці",
        [UOC_RAJKA], rank="Mission", address=["Rajka, Hungary"]),
]


ROWS = {
    "bg-western-central-europe": BULGARIAN_ROWS,
    "ep-austria": EP_ROWS,
    "ro-hungary": ROMANIAN_ROWS,
    "ru-budapest-and-hungary": RUSSIAN_ROWS,
    "sr-buda": SERBIAN_ROWS,
    "ukraine-uoc": UOC_ROWS,
}

EXPECTED = {
    "bg-western-central-europe": 3,
    "ep-austria": 11,
    "ro-hungary": 22,
    "ru-budapest-and-hungary": 11,
    "sr-buda": 60,
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
    if out.get("address") and (not isinstance(out["address"], list) or
                               not all(isinstance(item, str)
                                       for item in out["address"])):
        raise ValueError("%s has invalid address" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") != parent:
                raise ValueError("%s has wrong parent" % row_id)
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if not item.get("local"):
                raise ValueError("%s has no local name" % row_id)
            seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "HU",
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Hungary counts changed: %r" % counts)
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
        print("directory Hungary: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
        return 0
    print("Hungary: 109 verified bodies across 6 canonical parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
