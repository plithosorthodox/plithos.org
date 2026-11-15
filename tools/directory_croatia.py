#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Croatia.

The official-source union preserves every confirmed overlapping jurisdiction
and keeps unclear or historical cases in the separate Croatia candidate file.

    python tools/directory_croatia.py --check
    python tools/directory_croatia.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-15"

ZAGREB_CONTACTS = "https://mitropolija-zagrebacka.org/kontakti/"
ZAGREB_SERVICES = "https://mitropolija-zagrebacka.org/raspored-bogosluzenja/"
GORNJI_ADDRESS = "https://www.eparhija-gornjokarlovacka.hr/adresar/"
GORNJI_GOMIRJE = "https://www.eparhija-gornjokarlovacka.hr/manastir-gomirje/"
GORNJI_KOMOGOVINA = "https://www.eparhija-gornjokarlovacka.hr/manastir-komogovina/"
GORNJI_MEDAK = "https://www.eparhija-gornjokarlovacka.hr/manastir-medak/"
GORNJI_GORICA = "https://www.eparhija-gornjokarlovacka.hr/manastir-gorica/"
DALMATIA_ADDRESS = "https://www.eparhija-dalmatinska.hr/Adresar-c.htm"
OSIJEK_ADDRESS = "https://eparhijaosecka.hr/?A=G&G=66"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
MACEDONIAN_DIRECTORY = "https://mpee.mk/category/juzno-evropsko-namesnistvo-2"
ROMANIAN_EXTERNAL = (
    "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
    "reprezentante-si-comunitati-externe/"
)


def row(row_id, parent, name, local, sources, rank="Parish", kind="parish",
        address=None, site=None, services=None, founded=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "HR",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    if services:
        value["services"] = services
    if founded:
        value["founded"] = founded
    return value


def rows_from_table(parent, source, entries):
    rows = []
    for row_id, name, local, address in entries:
        rows.append(row(
            row_id, parent, name, local, [source],
            address=list(address) if address else None,
        ))
    return rows


BULGARIAN_ROWS = [
    row(
        "hr-bg-zagreb-seven-saints", "bg-western-central-europe",
        "Holy Seven Saints Bulgarian Orthodox Church Community in Zagreb",
        "БПЦО Св. Седмочисленици",
        [BULGARIAN_DIRECTORY], rank="Church Community",
        address=["Zdihovska 67", "10000 Zagreb, Croatia"],
    ),
]


MACEDONIAN_ROWS = [
    row(
        "hr-mk-zagreb-zlata-maglenska", "mk-europe",
        "Saint Zlata of Meglen Macedonian Orthodox Church Community in Zagreb",
        "МПЦО Св. Злата Мегленска, Загреб, Хрватска",
        [MACEDONIAN_DIRECTORY], rank="Church Community",
    ),
    row(
        "hr-mk-pula-joachim-osogovo", "mk-europe",
        "Saint Joachim of Osogovo Macedonian Orthodox Church Community in Pula",
        "МПЦО Свети Јоаким Осоговски, Пула",
        [MACEDONIAN_DIRECTORY], rank="Church Community",
    ),
    row(
        "hr-mk-rijeka-constantine-helen", "mk-europe",
        "Saints Constantine and Helen Macedonian Orthodox Church Community in Rijeka",
        "МПЦО Свети Цар Константин и Царица Елена, Ријека",
        [MACEDONIAN_DIRECTORY], rank="Church Community",
        address=["Matačićeva 5", "51000 Rijeka, Croatia"],
    ),
]


ROMANIAN_ROWS = [
    row(
        "hr-ro-zagreb-community", "romania",
        "Romanian Orthodox Community in Zagreb",
        "Comunitatea Ortodoxă Română din Zagreb",
        [ROMANIAN_EXTERNAL], rank="Church Community",
        address=["Voćarska cesta", "10000 Zagreb, Croatia"],
    ),
]


ZAGREB_ROWS = [
    row(
        "hr-sr-zagreb-transfiguration", "sr-zagreb-ljubljana",
        "Transfiguration Cathedral in Zagreb",
        "Саборни храм Преображења Господњег у Загребу",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Cathedral",
        address=["Ilica 7", "10000 Zagreb, Croatia"],
    ),
    row(
        "hr-sr-varazdin-george", "sr-zagreb-ljubljana",
        "Saint George Serbian Orthodox Church in Varaždin",
        "Храм Светог великомученика Георгија у Вараждину",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Petra Preradovića 19", "48000 Varaždin, Croatia"],
    ),
    row(
        "hr-sr-veliki-poganac-george", "sr-zagreb-ljubljana",
        "Saint George Serbian Orthodox Church in Veliki Poganac",
        "Храм Светог великомученика Георгија у Великом Поганцу",
        [ZAGREB_CONTACTS], rank="Church",
        address=["Veliki Poganac 36", "48312 Rasinja, Croatia"],
    ),
    row(
        "hr-sr-koprivnica-trinity", "sr-zagreb-ljubljana",
        "Holy Trinity Serbian Orthodox Church in Koprivnica",
        "Храм Свете Тројице у Копривници",
        [ZAGREB_CONTACTS], rank="Church",
        address=["Frankopanska 9", "48000 Koprivnica, Croatia"],
    ),
    row(
        "hr-sr-krizevci-sava", "sr-zagreb-ljubljana",
        "Saint Sava Serbian Orthodox Church in Križevci",
        "Храм Светог Саве у Крижевцима",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
    ),
    row(
        "hr-sr-sisak-paraskeva", "sr-zagreb-ljubljana",
        "Saint Paraskeva Serbian Orthodox Church in Sisak",
        "Храм Преподобне мати Параскеве у Сиску",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Franje Lovrića 4", "44000 Sisak, Croatia"],
    ),
    row(
        "hr-sr-bjelovar-trinity", "sr-zagreb-ljubljana",
        "Holy Trinity Serbian Orthodox Church in Bjelovar",
        "Храм Свете Тројице у Бјеловару",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Ante Trumbića 2", "43000 Bjelovar, Croatia"],
    ),
    row(
        "hr-sr-velika-pisanica-lazarus", "sr-zagreb-ljubljana",
        "Saint Lazarus the Four Days Dead Serbian Orthodox Church in Velika Pisanica",
        "Храм Светог четвородневног Лазара у Великој Писаници",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Hrvatskih Mučenika 4", "43271 Velika Pisanica, Croatia"],
    ),
    row(
        "hr-sr-narta-george", "sr-zagreb-ljubljana",
        "Saint George Serbian Orthodox Church in Narta",
        "Храм Светог великомученика Георгија у Нарти",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Narta 333", "43247 Narta, Croatia"],
    ),
    row(
        "hr-sr-grubisno-polje-george", "sr-zagreb-ljubljana",
        "Saint George Serbian Orthodox Church in Grubišno Polje",
        "Храм Светог великомученика Георгија у Грубишном Пољу",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Nikole Šubića Zrinjskog 23", "43290 Grubišno Polje, Croatia"],
    ),
    row(
        "hr-sr-stupovaca-demetrius", "sr-zagreb-ljubljana",
        "Saint Demetrius the Myrrh-Streamer Serbian Orthodox Church in Stupovača",
        "Храм Светог великомученика Димитрија Мироточивог у Ступовачи",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Stupovača Selska 120", "44320 Kutina, Croatia"],
    ),
    row(
        "hr-sr-velika-brsljanica-translation-nicholas", "sr-zagreb-ljubljana",
        "Translation of the Relics of Saint Nicholas Serbian Orthodox Church in Velika Bršljanica",
        "Храм Преноса моштију Светог Николаја у Великој Бршљаници",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Church",
        address=["Velika Bršljanica 44", "43282 Veliko Vukovje, Croatia"],
    ),
    row(
        "hr-sr-lepavina-monastery", "sr-zagreb-ljubljana",
        "Lepavina Monastery",
        "Манастир Лепавина",
        [ZAGREB_CONTACTS], rank="Monastery", kind="monastery",
        address=["48306 Sokolovac, Croatia"],
    ),
    row(
        "hr-sr-zagreb-paraskeva-monastery", "sr-zagreb-ljubljana",
        "Saint Paraskeva Monastery in Zagreb",
        "Манастир Свете Петке у Загребу",
        [ZAGREB_CONTACTS, ZAGREB_SERVICES], rank="Monastery", kind="monastery",
        address=["Sveti Duh 122", "10000 Zagreb, Croatia"],
    ),
    row(
        "hr-sr-zagreb-sava-school-chapel", "sr-zagreb-ljubljana",
        "Saint Sava Chapel at the Kantakuzina Katarina Branković Gymnasium in Zagreb",
        "Капела Светог Саве у Гимназији Кантакузина Катарина Бранковић",
        [ZAGREB_SERVICES], rank="Chapel",
        address=["Sveti Duh 122", "10000 Zagreb, Croatia"],
        services=["Matins and Vespers are served daily. Divine Liturgy is served on Saturdays."],
    ),
    row(
        "hr-sr-zagreb-mirogoj-peter-paul", "sr-zagreb-ljubljana",
        "Saints Peter and Paul Chapel at Mirogoj Cemetery in Zagreb",
        "Капела Светих апостола Петра и Павла на гробљу Мирогој",
        [ZAGREB_SERVICES], rank="Chapel",
        address=["Mirogoj Cemetery", "Zagreb, Croatia"],
        services=["Divine Liturgy is served on the first Saturday of each month and on memorial Saturdays."],
    ),
    row(
        "hr-sr-vojakovac-worship", "sr-zagreb-ljubljana",
        "Serbian Orthodox Recurring Worship Site in Vojakovac",
        "Богослужбено мјесто у Војаковцу",
        [ZAGREB_SERVICES], rank="Recurring Worship Site",
        address=["Vojakovac, Croatia"],
        services=["Divine Liturgy is served on the first Sunday of each month."],
    ),
    row(
        "hr-sr-pavljani-peter-paul", "sr-zagreb-ljubljana",
        "Saints Peter and Paul Serbian Orthodox Church in Pavljani",
        "Храм Светих апостола Петра и Павла у Пављанима",
        [ZAGREB_SERVICES], rank="Recurring Worship Site",
        address=["Pavljani, Croatia"],
        services=["Divine Liturgy is served on the last Sunday of each month."],
    ),
]


GORNJI_PARISHES = [
    ("hr-sr-gk-glina", "Serbian Orthodox Parish in Glina", "СПЦО и Управа парохије у Глини", ("Hrvatska 20", "44400 Glina, Croatia")),
    ("hr-sr-gk-dvor", "Serbian Orthodox Parish in Dvor", "СПЦО и Управа парохије у Двору", ("Mile Blaževića Čađe 46", "44440 Dvor, Croatia")),
    ("hr-sr-gk-karlovac-first", "First Serbian Orthodox Parish in Karlovac", "Прва парохија карловачка", ("Miroslava Krleže 15", "47000 Karlovac, Croatia")),
    ("hr-sr-gk-karlovac-second", "Second Serbian Orthodox Parish in Karlovac", "Друга парохија карловачка", ("Tina Ujevića 5", "47000 Karlovac, Croatia")),
    ("hr-sr-gk-karlovac-third", "Third Serbian Orthodox Parish in Karlovac", "Трећа парохија карловачка", ("Izidora Kršnjavog 10c", "47000 Karlovac, Croatia")),
    ("hr-sr-gk-karlovac-fourth", "Fourth Serbian Orthodox Parish in Karlovac", "Четврта парохија карловачка", ("Ambroza Vranicanija 6", "47000 Karlovac, Croatia")),
    ("hr-sr-gk-kolaric", "Serbian Orthodox Parish in Kolarić", "СПЦО и Управа парохије у Коларићу", ("Kolarić 67", "47220 Vojnić, Croatia")),
    ("hr-sr-gk-kostajnica", "Serbian Orthodox Parish in Kostajnica", "СПЦО и Управа парохије у Костајници", ("Davorina Trstenjaka 5", "44430 Kostajnica, Croatia")),
    ("hr-sr-gk-petrinja", "Serbian Orthodox Parish in Petrinja", "СПЦО и Управа парохије у Петрињи", ("Vladimira Nazora 13", "44250 Petrinja, Croatia")),
    ("hr-sr-gk-topusko", "Serbian Orthodox Parish in Topusko", "СПЦО и Управа парохије у Топуском", ("Prilaz G. Draškovića 2/a", "44415 Topusko, Croatia")),
    ("hr-sr-gk-gospic-smiljan", "Serbian Orthodox Parish of Gospić and Smiljan", "СПЦО и Управа парохије Госпићко-смиљанске", ("Specijalne jedinice policije 16", "53000 Gospić, Croatia")),
    ("hr-sr-gk-gracac", "Serbian Orthodox Parish in Gračac", "СПЦО и Управа парохије у Грачацу", ("K. Stepinca 82", "23440 Gračac, Croatia")),
    ("hr-sr-gk-donji-lapac", "Serbian Orthodox Parish in Donji Lapac", "СПЦО и Управа парохије у Доњем Лапцу", ("Maršala Tita 11", "53250 Donji Lapac, Croatia")),
    ("hr-sr-gk-dreznica", "Serbian Orthodox Parish in Drežnica", "СПЦО и Управа парохије у Дрежници", ("Centar bb", "47313 Drežnica, Croatia")),
    ("hr-sr-gk-korenica", "Serbian Orthodox Parish in Korenica", "СПЦО и Управа парохије у Кореници", ("IX gardijske brigade 26", "53230 Korenica, Croatia")),
    ("hr-sr-gk-ogulin", "Serbian Orthodox Parish in Ogulin", "СПЦО и Управа парохије у Огулину", ("B. Frankopana 16", "47300 Ogulin, Croatia")),
    ("hr-sr-gk-otocac", "Serbian Orthodox Parish in Otočac", "СПЦО и Управа парохије у Оточцу", ("dr Franje Tuđmana 5", "53220 Otočac, Croatia")),
    ("hr-sr-gk-plaski", "Serbian Orthodox Parish in Plaški", "СПЦО и Управа парохије у Плашком", ("I Gardijske brigade I/a", "47304 Plaški, Croatia")),
    ("hr-sr-gk-pula-peroj", "Serbian Orthodox Parish of Pula and Peroj", "СПЦО и Управа парохије Пулско-перојске", ("Peroj 19", "52215 Vodnjan, Croatia")),
    ("hr-sr-gk-rijeka-first", "First Serbian Orthodox Parish in Rijeka", "Прва парохија ријечка", ("Ivana Zajca 24/I", "51000 Rijeka, Croatia")),
    ("hr-sr-gk-rijeka-second", "Second Serbian Orthodox Parish in Rijeka", "Друга парохија ријечка", ("Ivana Zajca 24/III", "51000 Rijeka, Croatia")),
    ("hr-sr-gk-srpske-moravice", "Serbian Orthodox Parish in Srpske Moravice", "СПЦО и Управа парохије у Српским Моравицама", ("Dokmanovići 10", "51325 Moravice, Croatia")),
]


GORNJI_ROWS = rows_from_table(
    "sr-gornji-karlovac", GORNJI_ADDRESS, GORNJI_PARISHES,
) + [
    row(
        "hr-sr-gk-gomirje-monastery", "sr-gornji-karlovac",
        "Gomirje Monastery", "Манастир Гомирје",
        [GORNJI_GOMIRJE, GORNJI_ADDRESS], rank="Monastery", kind="monastery",
        address=["Ribnjak 23", "51327 Gomirje, Croatia"],
    ),
    row(
        "hr-sr-gk-komogovina-monastery", "sr-gornji-karlovac",
        "Komogovina Monastery", "Манастир Комоговина",
        [GORNJI_KOMOGOVINA], rank="Monastery", kind="monastery",
        address=["Svetoga Roka bb", "Komogovina", "44430 Donji Kukuruzari, Croatia"],
    ),
    row(
        "hr-sr-gk-medak-monastery", "sr-gornji-karlovac",
        "Medak Monastery", "Манастир Медак",
        [GORNJI_MEDAK], rank="Monastery", kind="monastery",
        address=["Medak", "53205 Gospić, Croatia"],
        founded=["The monastery was re-established by diocesan decision on 6 September 2006."],
    ),
    row(
        "hr-sr-gk-gorica-monastery", "sr-gornji-karlovac",
        "Gorica Monastery in Donji Budački", "Манастир Горица у Доњем Будачком",
        [GORNJI_GORICA, GORNJI_ADDRESS], rank="Monastery", kind="monastery",
        address=["Donji Budački 6", "47242 Krnjak, Croatia"],
    ),
]


DALMATIA_PARISHES = [
    ("hr-sr-da-split-first", "First Serbian Orthodox Parish in Split", "СПЦО и Управа прве парохије у Сплиту", ("Obrov 6", "21000 Split, Croatia")),
    ("hr-sr-da-split-second", "Second Serbian Orthodox Parish in Split", "СПЦО и Управа друге парохије у Сплиту", ("Obrov 6", "21000 Split, Croatia")),
    ("hr-sr-da-sibenik-second", "Second Serbian Orthodox Parish in Šibenik", "СПЦО и Управа друге парохије у Шибенику", ("Tina Ujevića 12", "22000 Šibenik, Croatia")),
    ("hr-sr-da-zadar-first", "First Serbian Orthodox Parish in Zadar", "СПЦО и Управа прве парохије у Задру", ()),
    ("hr-sr-da-zadar-second", "Second Serbian Orthodox Parish in Zadar", "СПЦО и Управа друге парохије у Задру", ()),
    ("hr-sr-da-knin-first", "First Serbian Orthodox Parish in Knin", "Прва парохија книнска", ("Rendićeva 12", "22300 Knin, Croatia")),
    ("hr-sr-da-knin-second", "Second Serbian Orthodox Parish in Knin", "Друга парохија книнска", ("Mokro Polje, Centar 2", "22300 Knin, Croatia")),
    ("hr-sr-da-knin-third", "Third Serbian Orthodox Parish in Knin", "Трећа парохија книнска", ("Zvonimirova 60", "22300 Knin, Croatia")),
    ("hr-sr-da-benkovac", "Serbian Orthodox Parish in Benkovac", "СПЦО и Управа парохије у Бенковцу", ("Kralja Dmitra Zvonimira 42b", "23420 Benkovac, Croatia")),
    ("hr-sr-da-drnis", "Serbian Orthodox Parish in Drniš", "СПЦО и Управа парохије у Дрнишу", ("Rogoznička 1a", "22000 Šibenik, Croatia")),
    ("hr-sr-da-imotski", "Serbian Orthodox Parish in Imotski", "СПЦО и Управа парохије у Имотском", ("Glavina Donja 488", "21260 Imotski, Croatia")),
    ("hr-sr-da-obrovac", "Serbian Orthodox Parish in Obrovac", "СПЦО и Управа парохије у Обровцу", ("Stjepana Radića 10", "23450 Obrovac, Croatia")),
    ("hr-sr-da-djevrske", "Serbian Orthodox Parish in Đevrske", "СПЦО и Управа парохије у Ђеврскама", ("Đevrske Centar 122", "Croatia")),
    ("hr-sr-da-skradin", "Serbian Orthodox Parish in Skradin", "СПЦО и Управа парохије у Скрадину", ("Franje Tuđmana 16", "22222 Skradin, Croatia")),
    ("hr-sr-da-kistanje", "Serbian Orthodox Parish in Kistanje", "СПЦО и Управа парохије у Кистањама", ("Trg Petra Preradovića 19", "22305 Kistanje, Croatia")),
    ("hr-sr-da-ravni-kotari", "Serbian Orthodox Parish of Ravni Kotari", "СПЦО и Управа парохије Равних Котара", ("Smilčić 49", "23424 Smilčić, Croatia")),
    ("hr-sr-da-biocic", "Serbian Orthodox Parish in Biočić", "СПЦО и Управа парохије у Биочићу", ("Biočić", "22320 Drniš, Croatia")),
    ("hr-sr-da-markovac", "Serbian Orthodox Parish in Markovac", "СПЦО и Управа парохије у Марковцу", ("Riđane centar 77", "22300 Knin, Croatia")),
    ("hr-sr-da-padjene", "Serbian Orthodox Parish in Pađene", "СПЦО и Управа парохије у Пађенама", ("Mokro Polje, Centar 2", "22300 Knin, Croatia")),
    ("hr-sr-da-vrlika", "Serbian Orthodox Parish in Vrlika", "СПЦО и Управа парохије у Врлици", ("Put Vrančića 1", "21236 Vrlika, Croatia")),
]


DALMATIA_ROWS = rows_from_table(
    "sr-dalmatia", DALMATIA_ADDRESS, DALMATIA_PARISHES,
) + [
    row("hr-sr-da-krupa-monastery", "sr-dalmatia", "Krupa Monastery", "Манастир Крупа", [DALMATIA_ADDRESS], rank="Monastery", kind="monastery", address=["23450 Obrovac, Croatia"]),
    row("hr-sr-da-krka-monastery", "sr-dalmatia", "Krka Monastery", "Манастир Крка", [DALMATIA_ADDRESS], rank="Monastery", kind="monastery", address=["Nikole Tesle 45", "22305 Kistanje, Croatia"]),
    row("hr-sr-da-dragovic-monastery", "sr-dalmatia", "Dragović Monastery", "Манастир Драговић", [DALMATIA_ADDRESS], rank="Monastery", kind="monastery", address=["Koljani", "21236 Vrlika, Croatia"]),
    row("hr-sr-da-lazarica-monastery", "sr-dalmatia", "Lazarica Monastery", "Манастир Лазарица", [DALMATIA_ADDRESS], rank="Monastery", kind="monastery", address=["Zvjerinac", "22312 Kosovo, Croatia"]),
    row("hr-sr-da-saint-nedjelja-monastery", "sr-dalmatia", "Saint Nedjelja Monastery", "Манастир Света Недјеља", [DALMATIA_ADDRESS], rank="Monastery", kind="monastery", address=["Oćestovo bb", "22300 Knin, Croatia"]),
]


OSIJEK_PARISHES = [
    ("hr-sr-ob-beli-manastir", "Saint Michael the Archangel Serbian Orthodox Parish in Beli Manastir", "Беломанастирска парохија при храму Светог архангела Михаила", ("Vladana Desnice 74", "31300 Beli Manastir, Croatia")),
    ("hr-sr-ob-bolman", "Saints Peter and Paul Serbian Orthodox Parish in Bolman", "Болманска парохија при храму Светих апостола Петра и Павла", ("Miladina Popovića 2", "31323 Bolman, Croatia")),
    ("hr-sr-ob-darda", "Saint Michael the Archangel Serbian Orthodox Parish in Darda", "Дарђанска парохија при храму Светог архангела Михаила", ("135. baranjske brigade 20", "31326 Darda, Croatia")),
    ("hr-sr-ob-jagodnjak", "Saint Nicholas Serbian Orthodox Parish in Jagodnjak", "Јагодњачка парохија при храму Светог оца Николаја", ("Zmaj Jove Jovanovića 27", "31324 Jagodnjak, Croatia")),
    ("hr-sr-ob-karanac", "Saint Stefan Štiljanović Serbian Orthodox Parish in Karanac", "Караначка парохија при храму Светог Стефана Штиљановића", ("Nikole Tesle 2", "31315 Karanac, Croatia")),
    ("hr-sr-ob-knezevi-vinogradi", "Entrance of the Theotokos Serbian Orthodox Parish in Kneževi Vinogradi", "Кнежевовиноградска парохија при храму Ваведења Пресвете Богородице", ("Glavna 112", "31309 Kneževi Vinogradi, Croatia")),
    ("hr-sr-ob-popovac", "Entrance of the Theotokos Serbian Orthodox Parish in Popovac", "Поповачка парохија при храму Ваведења Пресвете Богородице", ("V. Nazora 49", "31303 Popovac, Croatia")),
    ("hr-sr-ob-ugljese", "Prophet Elijah Serbian Orthodox Parish in Uglješ", "Угљешка парохија при храму Светог пророка Илије", ("Baranjska 15", "31326 Uglješ, Croatia")),
    ("hr-sr-ob-bobota", "Saint George Serbian Orthodox Parish in Bobota", "Боботска парохија при храму Светог великомученика Георгија", ("Mitrovićeva 33", "32225 Bobota, Croatia")),
    ("hr-sr-ob-borovo-first", "First Serbian Orthodox Parish at the Translation of Saint Stephen Church in Borovo", "Прва парохија боровска при храму Преноса моштију Светог архиђакона Стефана", ("Trg palih boraca 13", "32227 Borovo, Croatia")),
    ("hr-sr-ob-borovo-second", "Second Serbian Orthodox Parish at the Translation of Saint Stephen Church in Borovo", "Друга парохија боровска при храму Преноса моштију Светог архиђакона Стефана", ("Trg palih boraca 13", "32227 Borovo, Croatia")),
    ("hr-sr-ob-borovo-naselje-first", "First Saint Stefan Dečanski Serbian Orthodox Parish in Borovo Naselje", "Прва парохија боровонасељска при храму Светог краља Стефана Дечанског", ("Vile Velebita 164", "32010 Vukovar, Croatia")),
    ("hr-sr-ob-borovo-naselje-second", "Second Saint Stefan Dečanski Serbian Orthodox Parish in Borovo Naselje", "Друга парохија боровонасељска при храму Светог краља Стефана Дечанског", ("Vile Velebita 164", "32010 Vukovar, Croatia")),
    ("hr-sr-ob-brsadin", "Archangel Gabriel Serbian Orthodox Parish in Bršadin", "Бршадинска парохија при храму Светог архангела Гаврила", ("Vase Đurđevića 31", "32222 Bršadin, Croatia")),
    ("hr-sr-ob-vera", "Annunciation Serbian Orthodox Parish in Vera", "Веранска парохија при храму Благовештења Пресвете Богородице", ("Miloša Obilića 3", "32224 Trpinja, Croatia")),
    ("hr-sr-ob-marinci", "Saint George Serbian Orthodox Parish in Marinci", "Мариначка парохија при храму Светог великомученика Георгија", ("Bana Jelačića bb", "32221 Marinci, Croatia")),
    ("hr-sr-ob-pacetin", "Saint Nicholas Serbian Orthodox Parish in Pačetin", "Пачетинска парохија при храму Светог оца Николаја", ("Crnogoraca 14", "32222 Pačetin, Croatia")),
    ("hr-sr-ob-trpinja", "Ascension Serbian Orthodox Parish in Trpinja", "Трпињска парохија при храму Вазнесења Господњег", ("Velika 2", "32224 Trpinja, Croatia")),
    ("hr-sr-ob-vinkovci", "Descent of the Holy Spirit Serbian Orthodox Parish in Vinkovci", "Винковачка парохија при храму Силаска Светог Духа на апостоле", ("Istarska 1", "32100 Vinkovci, Croatia")),
    ("hr-sr-ob-vukovar-first", "First Serbian Orthodox Parish at Saint Nicholas Cathedral in Vukovar", "Прва парохија вуковарска при Саборном храму Светог оца Николаја", ("Europske unije 7a", "32000 Vukovar, Croatia")),
    ("hr-sr-ob-vukovar-second", "Second Serbian Orthodox Parish at Saint Paraskeva Church in Vukovar", "Друга парохија вуковарска при храму Преподобне мати Параскеве", ("Europske unije 7a", "32000 Vukovar, Croatia")),
    ("hr-sr-ob-gornji-petrovci", "Ascension Serbian Orthodox Parish in Gornji Petrovci", "Горњопетровачка парохија при храму Вазнесења Господњег", ("Grabik 1", "32229 Petrovci, Croatia")),
    ("hr-sr-ob-mirkovci", "Translation of Saint Nicholas Serbian Orthodox Parish in Mirkovci", "Мирковачка парохија при храму Преноса моштију Светог оца Николаја", ("Trg Nikole Tesle 3", "32240 Mirkovci, Croatia")),
    ("hr-sr-ob-negoslavci", "Dormition Serbian Orthodox Parish in Negoslavci", "Негославачка парохија при храму Успенија Пресвете Богородице", ("Vukovarska 3", "32239 Negoslavci, Croatia")),
    ("hr-sr-ob-orolik", "Saints Peter and Paul Serbian Orthodox Parish in Orolik", "Ороличка парохија при храму Светих апостола Петра и Павла", ()),
    ("hr-sr-ob-sotin", "Translation of Saint Nicholas Serbian Orthodox Parish in Sotin", "Сотинска парохија при храму Преноса моштију Светог оца Николаја", ("dr Franje Tuđmana 44", "32232 Sotin, Croatia")),
    ("hr-sr-ob-sremske-laze", "Nativity of the Theotokos Serbian Orthodox Parish in Sremske Laze", "Сремсколашка парохија при храму Рођења Пресвете Богородице", ("Branislava Nušića 3", "32242 Slakovci, Croatia")),
    ("hr-sr-ob-sremski-cakovci", "Entrance of the Theotokos Serbian Orthodox Parish in Sremski Čakovci", "Сремскочаковачка парохија при храму Ваведења Пресвете Богородице", ("K. Zvonimira 1", "32238 Sremski Čakovci, Croatia")),
    ("hr-sr-ob-bijelo-brdo", "Translation of Saint Nicholas Serbian Orthodox Parish in Bijelo Brdo", "Бјелобрдска парохија при храму Преноса моштију Светог оца Николаја", ("Školski trg 23", "31204 Bijelo Brdo, Croatia")),
    ("hr-sr-ob-budimci", "Ascension Serbian Orthodox Parish in Budimci", "Будимачка парохија при храму Вазнесења Господњег", ("J. Bana Jelačića 169", "31432 Budimci, Croatia")),
    ("hr-sr-ob-valpovo", "Saint George Serbian Orthodox Chapel Parish in Valpovo", "Валповачка парохија при капели Светог великомученика Георгија", ("Osječka 21", "31550 Valpovo, Croatia")),
    ("hr-sr-ob-gabos", "Nativity of the Theotokos Serbian Orthodox Parish in Gaboš", "Габошка парохија при храму Рођења Пресвете Богородице", ("J. J. Zmaja 3", "32212 Gaboš, Croatia")),
    ("hr-sr-ob-dalj-first", "First Saint Demetrius Serbian Orthodox Parish in Dalj", "Прва парохија даљска при храму Светог великомученика Димитрија", ("Bana Josipa Jelačića 3", "31226 Dalj, Croatia")),
    ("hr-sr-ob-dalj-second", "Second Saint Demetrius Serbian Orthodox Parish in Dalj", "Друга парохија даљска при храму Светог великомученика Димитрија", ("Bana Josipa Jelačića 3", "31226 Dalj, Croatia")),
    ("hr-sr-ob-dopsin", "Saints Peter and Paul Serbian Orthodox Parish in Dopsin", "Допсинска парохија при храму Светих апостола Петра и Павла", ("J. J. Strossmayera 68", "31404 Vladislavci, Croatia")),
    ("hr-sr-ob-erdut", "Archangel Gabriel Serbian Orthodox Parish in Erdut", "Ердутска парохија при храму Светог архангела Гаврила", ("I. Bakića 45", "31206 Erdut, Croatia")),
    ("hr-sr-ob-markusica", "Descent of the Holy Spirit Serbian Orthodox Parish in Markušica", "Маркушичка парохија при храму Силаска Светог Духа на апостоле", ("Save Popovića 27", "32213 Markušica, Croatia")),
    ("hr-sr-ob-osijek", "Dormition Serbian Orthodox Parish in Osijek", "Осјечка парохија при храму Успења Пресвете Богородице", ("Crkvena 15", "31000 Osijek, Croatia")),
    ("hr-sr-ob-ostrovo", "Nativity of Saint John the Baptist Serbian Orthodox Parish in Ostrovo", "Островска парохија при храму Рођења Светог Јована Крститеља", ("N. Demonje 22", "32214 Tordinci, Croatia")),
    ("hr-sr-ob-petrova-slatina", "Nativity of the Theotokos Serbian Orthodox Parish in Petrova Slatina", "Петровослатинска парохија при храму Рођења Пресвете Богородице", ("Kordunaška 78", "31215 Petrova Slatina, Croatia")),
    ("hr-sr-ob-silas", "Prophet Elijah Serbian Orthodox Parish in Silaš", "Силашка парохија при храму Светог пророка Илије", ("Srednja 7A", "31214 Silaš, Croatia")),
    ("hr-sr-ob-tenja", "Translation of Saint Nicholas Serbian Orthodox Parish in Tenja", "Тењска парохија при храму Преноса моштију Светог оца Николаја", ("Vlatka Mačeka 27", "31207 Tenja, Croatia")),
    ("hr-sr-ob-cepin", "Saint Michael the Archangel Serbian Orthodox Parish in Čepin", "Чепинска парохија при храму Светог архангела Михаила", ("K. Zvonimira 227", "31431 Čepin, Croatia")),
]


OSIJEK_ROWS = rows_from_table(
    "sr-osijek-baranja", OSIJEK_ADDRESS, OSIJEK_PARISHES,
) + [
    row("hr-sr-ob-beli-manastir-cemetery-chapel", "hr-sr-ob-beli-manastir", "Serbian Orthodox Cemetery Chapel in Beli Manastir", "Капела на гробљу у Белом Манастиру", [OSIJEK_ADDRESS], rank="Chapel", address=["Beli Manastir, Croatia"]),
    row("hr-sr-ob-jagodnjak-nectarios", "hr-sr-ob-jagodnjak", "Saint Nectarios Serbian Orthodox Church in Jagodnjak", "Храм Светог Нектарија Егинског Чудотворца у Јагодњаку", [OSIJEK_ADDRESS], rank="Church Under Construction", address=["Jagodnjak, Croatia"]),
    row("hr-sr-ob-karanac-anne-site", "hr-sr-ob-karanac", "Dormition of Saint Anne Serbian Orthodox Church Site near Karanac", "Црквиште Успенија Свете Ане у планини код Каранца", [OSIJEK_ADDRESS], rank="Church Site", address=["near Karanac, Croatia"]),
    row("hr-sr-ob-knezevi-vinogradi-john-site", "hr-sr-ob-knezevi-vinogradi", "Beheading of Saint John the Baptist Serbian Orthodox Church Site near Kneževi Vinogradi", "Црквиште Усековања главе Светог Јована Крститеља у планини код Кнежевих Винограда", [OSIJEK_ADDRESS], rank="Church Site", address=["near Kneževi Vinogradi, Croatia"]),
    row("hr-sr-ob-marinci-paraskeva-chapel", "hr-sr-ob-marinci", "Saint Paraskeva Chapel between Marinci and Petrovci", "Капела Свете Петке између Маринаца и Петроваца", [OSIJEK_ADDRESS], rank="Chapel", address=["between Marinci and Petrovci, Croatia"]),
    row("hr-sr-ob-mirkovci-panteleimon-chapel", "hr-sr-ob-mirkovci", "Saint Panteleimon Chapel at the Mirkovci Spring", "Капела Светог Пантелејмона на мирковачкој водици", [OSIJEK_ADDRESS], rank="Chapel", address=["Mirkovci, Croatia"]),
    row("hr-sr-ob-negoslavci-john-chapel", "hr-sr-ob-negoslavci", "Nativity of Saint John the Baptist Cemetery Chapel in Negoslavci", "Капела Рођења Светог Јована Претече на гробљу у Негославцима", [OSIJEK_ADDRESS], rank="Chapel", address=["Negoslavci, Croatia"]),
    row("hr-sr-ob-opatovac-george", "hr-sr-ob-sotin", "Saint George Serbian Orthodox Church in Opatovac", "Храм Светог великомученика Георгија у Опатовцу", [OSIJEK_ADDRESS], rank="Church", address=["Opatovac, Croatia"]),
    row("hr-sr-ob-mohovo-ascension", "hr-sr-ob-sotin", "Ascension Serbian Orthodox Church in Mohovo", "Храм Вазнесења Господњег у Мохову", [OSIJEK_ADDRESS], rank="Church", address=["Mohovo, Croatia"]),
    row("hr-sr-ob-sarengrad-michael", "hr-sr-ob-sotin", "Archangel Michael Serbian Orthodox Church in Šarengrad", "Храм Светог архангела Михаила у Шаренграду", [OSIJEK_ADDRESS], rank="Church", address=["Šarengrad, Croatia"]),
    row("hr-sr-ob-sarvas-john", "hr-sr-ob-bijelo-brdo", "Nativity of Saint John the Baptist Serbian Orthodox Church in Sarvaš", "Храм Рођења Светог Јована Крститеља у Сарвашу", [OSIJEK_ADDRESS], rank="Church", address=["Sarvaš, Croatia"]),
    row("hr-sr-ob-paucje-george", "hr-sr-ob-budimci", "Saint George Serbian Orthodox Church in Paučje", "Храм Светог великомученика Георгија у Паучју", [OSIJEK_ADDRESS], rank="Church", address=["Paučje, Croatia"]),
    row("hr-sr-ob-cepinski-martinci-george", "hr-sr-ob-budimci", "Saint George Serbian Orthodox Church in Čepinski Martinci", "Храм Светог великомученика Георгија у Чепинским Мартинцима", [OSIJEK_ADDRESS], rank="Church", address=["Čepinski Martinci, Croatia"]),
    row("hr-sr-ob-bijela-loza-nativity", "hr-sr-ob-budimci", "Nativity of the Theotokos Serbian Orthodox Church in Bijela Loza", "Храм Рођења Пресвете Богородице у Бијелој Лози", [OSIJEK_ADDRESS], rank="Church", address=["Bijela Loza, Croatia"]),
    row("hr-sr-ob-poganovci-elijah", "hr-sr-ob-budimci", "Prophet Elijah Serbian Orthodox Church in Poganovci", "Храм Светог пророка Илије у Погановцима", [OSIJEK_ADDRESS], rank="Church", address=["Poganovci, Croatia"]),
    row("hr-sr-ob-babjak-transfiguration", "hr-sr-ob-budimci", "Transfiguration Serbian Orthodox Prayer House in Babjak", "Молитвени дом Преображења Господњег у Бабјаку", [OSIJEK_ADDRESS], rank="Prayer House", address=["Babjak, Croatia"]),
    row("hr-sr-ob-bracevci-demetrius", "hr-sr-ob-dopsin", "Saint Demetrius Serbian Orthodox Church in Bračevci", "Храм Светог великомученика Димитрија у Брачевцима", [OSIJEK_ADDRESS], rank="Church", address=["Bračevci, Croatia"]),
    row("hr-sr-ob-slobodna-vlast-holy-spirit", "hr-sr-ob-dopsin", "Descent of the Holy Spirit Serbian Orthodox Church in Slobodna Vlast", "Храм Силаска Светог Духа на апостоле у Слободној Власти", [OSIJEK_ADDRESS], rank="Church", address=["Slobodna Vlast, Croatia"]),
    row("hr-sr-ob-breznica-cyriacus", "hr-sr-ob-dopsin", "Saint Cyriacus the Anchorite Chapel in Breznica", "Капела Преподобног Киријака Отшелника у Брезници", [OSIJEK_ADDRESS], rank="Chapel", address=["Breznica, Croatia"]),
    row("hr-sr-ob-osijek-lower-town-nicholas", "hr-sr-ob-osijek", "Translation of Saint Nicholas Chapel at Lower Town Cemetery in Osijek", "Капела Преноса моштију Светог оца Николаја на Доњоградском гробљу у Осијеку", [OSIJEK_ADDRESS], rank="Chapel", address=["Lower Town Cemetery", "Osijek, Croatia"]),
    row("hr-sr-ob-osijek-anino-john", "hr-sr-ob-osijek", "Nativity of Saint John the Baptist Chapel at Anino Cemetery in Osijek", "Капела Рођења Светог Јована Крститеља на Анином гробљу у Осијеку", [OSIJEK_ADDRESS], rank="Chapel", address=["Anino Cemetery", "Osijek, Croatia"]),
    row("hr-sr-ob-petrova-slatina-basil", "hr-sr-ob-petrova-slatina", "Saint Basil of Ostrog Chapel in Petrova Slatina", "Капела Светог Василија Острошког у Петровој Слатини", [OSIJEK_ADDRESS], rank="Chapel", address=["Petrova Slatina, Croatia"]),
    row("hr-sr-ob-dalj-mountain-monastery", "sr-osijek-baranja", "Dormition of the Theotokos Monastery at Dalj Mountain", "Манастир Успења Пресвете Богородице на Даљској планини", [OSIJEK_ADDRESS], rank="Monastery", kind="monastery", address=["31205 Aljmaš, Croatia"]),
]


ROWS = {
    "bg-western-central-europe": BULGARIAN_ROWS,
    "mk-europe": MACEDONIAN_ROWS,
    "romania": ROMANIAN_ROWS,
    "sr-dalmatia": DALMATIA_ROWS,
    "sr-gornji-karlovac": GORNJI_ROWS,
    "sr-osijek-baranja": OSIJEK_ROWS,
    "sr-zagreb-ljubljana": ZAGREB_ROWS,
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "bg-western-central-europe": 1,
    "mk-europe": 3,
    "romania": 1,
    "sr-dalmatia": 25,
    "sr-gornji-karlovac": 26,
    "sr-osijek-baranja": 66,
    "sr-zagreb-ljubljana": 18,
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
    for key in ("address", "services", "founded"):
        if out.get(key) and (not isinstance(out[key], list) or
                             not all(isinstance(item, str)
                                     for item in out[key])):
            raise ValueError("%s has invalid %s" % (out.get("id"), key))
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
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if not item.get("local"):
                raise ValueError("%s has no local name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "HR",
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Croatia counts changed: %r" % counts)
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
        print("directory Croatia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Croatia: 140 verified bodies across 7 canonical parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
