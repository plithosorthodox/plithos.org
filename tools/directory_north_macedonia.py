#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in North Macedonia.

The current official-source union follows the Macedonian Orthodox Church after
the 2023 reception of the former Orthodox Ohrid Archbishopric. It preserves the
three resulting eparchies that are absent from the older shared spine and does
not duplicate the former Serbian structure as a current jurisdiction.

    python tools/directory_north_macedonia.py --check
    python tools/directory_north_macedonia.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-15"

MOC_2023 = "https://www.m-p-c.org/?p=3933"
MOC_2026 = "https://www.m-p-c.org/?p=4168"
MOC_MONASTERIES = "https://www.m-p-c.org/?page_id=121"
TIVERIOPOL_VODOCHA = (
    "https://www.tiveriopol.mk/"
    "%D0%BC%D0%B0%D0%BD%D0%B0%D1%81%D1%82%D0%B8%D1%80-"
    "%D1%81%D0%B2-%D0%BB%D0%B5%D0%BE%D0%BD%D1%82%D0%B8%D1%98-"
    "%D0%B2%D0%BE%D0%B4%D0%BE%D1%87%D0%B0/"
)

SKOPJE_CHURCHES = (
    "https://mpc-spe.mk/skopskaeparhija/crkvi-vo-eparhijata/"
)
SKOPJE_MONASTERIES = "https://mpc-spe.mk/skopskaeparhija/manastiri/"

DKE_TEMPLES_1 = "https://dke.org.mk/hramovi-i-manastiri/hramovi/"
DKE_TEMPLES_2 = (
    "https://dke.org.mk/hramovi-i-manastiri/hramovi/?query-15-page=2"
)
DKE_MONASTERIES_1 = "https://dke.org.mk/hramovi-i-manastiri/manastiri/"
DKE_MONASTERIES_2 = (
    "https://dke.org.mk/hramovi-i-manastiri/manastiri/?query-15-page=2"
)
DKE_CONTACT = "https://dke.org.mk/kontakt/"

KOE_ROSTER = "https://koe.mk/eparhija/"
TGE_ROSTER = "https://tge.mk/eparhija/all"

BREGALNICA_DEANERIES = (
    "https://www.bregalnickaeparhija.org.mk/?page_id=63"
)
BREGALNICA_STIP = "https://www.bregalnickaeparhija.org.mk/?page_id=332"
BREGALNICA_KOCANI = "https://www.bregalnickaeparhija.org.mk/?page_id=336"
BREGALNICA_VINICA = "https://www.bregalnickaeparhija.org.mk/?page_id=343"
BREGALNICA_RADOVIS = "https://www.bregalnickaeparhija.org.mk/?page_id=348"
BREGALNICA_MONASTERIES = (
    "https://www.bregalnickaeparhija.org.mk/?page_id=161"
)
BREGALNICA_NEWS_2 = (
    "https://novostibregalnickaeparhija.wordpress.com/?page_id=6138"
)
BREGALNICA_NEWS_3 = (
    "https://novostibregalnickaeparhija.wordpress.com/?page_id=8291"
)
BREGALNICA_NEWS_5 = (
    "https://novostibregalnickaeparhija.wordpress.com/?page_id=13591"
)

PPPE_BITOLA = (
    "https://www.pppe.mk/bitolsko-namesnistvo/soboren-hram-sv-dimitrij/"
)
SPC_BITOLA = (
    "https://spc.rs/sr/news/patrijarh/-/11287."
    "patrijarh-porfirije-i-arhiepiskop-stefan-bogosluzili-u-bitolju.html"
)

KRUSHDEM_ORGANIZATION = "https://krushdem.org/organizacija/"
KRUSHDEM_PARISHES = "https://krushdem.org/organizacija/parohii/"
KRUSHDEM_TEMPLES = "https://krushdem.org/organizacija/hramovi/"
KRUSHDEM_MONASTERIES = "https://krushdem.org/organizacija/manastiri/"

DELJADROVO_ENTHRONEMENT = (
    "https://bigorski.org.mk/vesti/svet/"
    "vostolichen-noviot-episkop-deljadrovsko-ilindenski-g-joakim/"
)

DELCHEVO_HOME = "https://www.dkeparhija.eu.mk/"
DELCHEVO_CLERGY = (
    "https://www.dkeparhija.eu.mk/index.php/parohii/"
    "parohiski-svestenici-vo-delcevo"
)
KAMENICA_CLERGY = (
    "https://www.dkeparhija.eu.mk/index.php/parohii/"
    "parohiski-svestenici-vo-makedonska-kamenica"
)
DELCHEVO_MONASTERY = (
    "https://www.dkeparhija.eu.mk/index.php/manstir-balaklija-delcevo"
)

POVARDARIE_CATEGORY = (
    "https://www.povardarska-eparhija.org.mk/pe/index.php?"
    "option=com_content&task=category&sectionid=8&id=20&Itemid=46"
)


def povardarie_article(article_id, item_id=55):
    return (
        "https://www.povardarska-eparhija.org.mk/pe/index.php?"
        "option=com_content&task=view&id=%s&Itemid=%s" %
        (article_id, item_id)
    )


POVARDARIE_GEVGELIJA = povardarie_article(34, 46)
POVARDARIE_VELES = povardarie_article(35, 46)
POVARDARIE_KAVADARCI = povardarie_article(36, 46)


def row(row_id, parent, name, local, rank, kind="parish", sources=None,
        address=None, site=None, founded=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "MK",
        "sources": list(sources or []),
    }
    if address:
        value["address"] = list(address)
    if site:
        value["site"] = site
    if founded:
        value["founded"] = list(founded)
    return value


def table_rows(text, parent, sources):
    rows = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = [field.strip() for field in line.split("|")]
        if len(fields) != 5:
            raise ValueError("invalid table row: %s" % line)
        row_id, name, local, rank, kind = fields
        rows.append(row(row_id, parent, name, local, rank, kind, sources))
    return rows


NEW_EPARCHY_ROWS = [
    row(
        "mk-krusevo-demir-hisar", "macedonia",
        "Eparchy of Krushevo and Demir Hisar",
        "Крушевско-демирхисарска епархија", "Eparchy", "diocese",
        [MOC_2023, MOC_2026, KRUSHDEM_ORGANIZATION],
        address=["Илинденска б.б.", "7550 Крушево, North Macedonia"],
        site="https://krushdem.org/",
        founded=["The eparchy was established in 2023."],
    ),
    row(
        "mk-deljadrovo-ilinden", "macedonia",
        "Eparchy of Deljadrovo and Ilinden",
        "Дељадровско-илинденска епархија", "Eparchy", "diocese",
        [MOC_2023, MOC_2026, DELJADROVO_ENTHRONEMENT],
        founded=["The eparchy was established in 2023."],
    ),
    row(
        "mk-ilinden-constantine-helen", "mk-deljadrovo-ilinden",
        "Saints Constantine and Helen Church in Ilinden",
        "Храм Свети цар Константин и царица Елена, Илинден",
        "Church", "parish",
        [MOC_2023, DELJADROVO_ENTHRONEMENT],
    ),
    row(
        "mk-delchevo-kamenica", "macedonia",
        "Eparchy of Delchevo and Kamenica",
        "Делчевско-каменичка епархија", "Eparchy", "diocese",
        [MOC_2023, MOC_2026, DELCHEVO_HOME],
        site=DELCHEVO_HOME,
        founded=["The eparchy was established in 2023."],
    ),
]


DELCHEVO_ROWS = table_rows(
    """
mk-delchevo-parish|Delchevo Parish|Делчевска парохија|Parish|parish
mk-kamenica-parish|Kamenica Parish|Каменичка парохија|Parish|parish
mk-zvegor-parish|Zvegor Parish|Ѕвегорска парохија|Parish|parish
mk-trbotivishte-parish|Trbotivishte Parish|Трботивишка парохија|Parish|parish
mk-delchevo-theotokos|Dormition of the Most Holy Theotokos Church in Delchevo|Храм Успение на Пресвета Богородица, Делчево|Church|parish
mk-makedonska-kamenica-elijah|Saint Elijah Church in Makedonska Kamenica|Црква Свети Илија, Македонска Каменица|Church|parish
mk-makedonska-kamenica-dormition|Dormition of the Most Holy Theotokos Church in Makedonska Kamenica|Храм Успение на Пресвета Богородица, Македонска Каменица|Church|parish
mk-zvegor-john-baptist|Saint John the Baptist Church in Zvegor|Црква Свети Јован Крстител, село Ѕвегор|Church|parish
mk-delchevo-balaklija-monastery|Holy Theotokos Balaklija and Life-giving Spring Monastery in Delchevo|Манастир Света Богородица Балаклија - Источен петок, Делчево|Monastery|monastery
""",
    "mk-delchevo-kamenica", [DELCHEVO_HOME, DELCHEVO_MONASTERY],
)

# The first three parish rows and their seat churches are all printed on the
# current diocesan home page. The clergy pages independently confirm the
# Delchevo and Makedonska Kamenica assignments.
for item in DELCHEVO_ROWS:
    if item["id"] in {"mk-delchevo-parish", "mk-delchevo-theotokos"}:
        item["sources"] = [DELCHEVO_HOME, DELCHEVO_CLERGY]
    elif item["id"] == "mk-trbotivishte-parish":
        item["sources"] = [DELCHEVO_CLERGY]
    elif item["id"] in {"mk-kamenica-parish", "mk-makedonska-kamenica-elijah"}:
        item["sources"] = [DELCHEVO_HOME, KAMENICA_CLERGY]
    elif item["id"] == "mk-makedonska-kamenica-dormition":
        item["sources"] = [KAMENICA_CLERGY]
    elif item["id"] == "mk-delchevo-balaklija-monastery":
        item["sources"] = [DELCHEVO_HOME, DELCHEVO_MONASTERY]


KRUSHDEM_PARISH_ROWS = table_rows(
    """
mk-krusevo-first-parish|First Parish of Krushevo|Прва Крушевска парохија|Parish|parish
mk-krusevo-second-parish|Second Parish of Krushevo|Втора Крушевска парохија|Parish|parish
mk-sopotnica-parish|Sopotnica Parish|Сопотничка парохија|Parish|parish
mk-buchin-parish|Buchin Parish|Бучинска парохија|Parish|parish
mk-demir-hisar-parish|Demir Hisar Parish|Демирхисарска парохија|Parish|parish
mk-slepche-parish|Slepche Parish|Слепчанска парохија|Parish|parish
mk-krivogashtani-first-parish|First Parish of Krivogashtani|Прва Кривогаштанска парохија|Parish|parish
mk-krivogashtani-second-parish|Second Parish of Krivogashtani|Втора Кривогаштанска парохија|Parish|parish
""",
    "mk-krusevo-demir-hisar", [KRUSHDEM_PARISHES],
)


KRUSHDEM_CHURCH_ROWS = table_rows(
    """
mk-krusevo-nicholas-cathedral|Saint Nicholas Cathedral in Krushevo|Храм Свети Никола - катедрален храм, Крушево|Cathedral|parish
mk-krusevo-nativity-john|Nativity of Saint John the Baptist Church in Krushevo|Храм Рождество на Свети Јован Крстител, Крушево|Church|parish
mk-krusevo-holy-trinity|Holy Trinity Church in Krushevo|Храм Света Троица, Крушево|Church|parish
mk-krusevo-paraskeva-romana-chapel|Venerable Martyr Paraskeva of Rome Chapel in Krushevo|Параклис Преподобна маченичка Параскева Римјанка, Крушево|Chapel|parish
mk-ostrilci-george|Saint George the Great Martyr Church in Ostrilci|Храм Свети великомаченик Георгиј, село Острилци|Church|parish
mk-aldanci-elijah|Holy Prophet Elijah Church in Aldanci|Храм Свети пророк Илија, село Алданци|Church|parish
mk-birino-elijah|Holy Prophet Elijah Church in Birino|Храм Свети пророк Илија, село Бирино|Church|parish
mk-krusevo-dormition|Dormition of the Most Holy Theotokos Church in Krushevo|Храм Успение на Пресвета Богородица, Крушево|Church|parish
mk-pusta-reka-nicholas|Saint Nicholas Church in Pusta Reka|Храм Свети Никола, село Пуста Река|Church|parish
mk-gorno-divjaci-demetrius|Saint Demetrius the Great Martyr Church in Gorno Divjaci|Храм Свети великомаченик Димитриј, село Горно Дивјаци|Church|parish
mk-dolno-divjaci-nicholas|Saint Nicholas Church in Dolno Divjaci|Храм Свети Никола, село Долно Дивјаци|Church|parish
mk-arilevo-nicholas|Saint Nicholas Church in Arilevo|Храм Свети Никола, село Арилево|Church|parish
mk-selce-paraskeva|Venerable Paraskeva of Epivates Church in Selce|Храм Преподобна Параскева Епиватска, село Селце|Church|parish
mk-belushino-nicholas|Saint Nicholas Church in Belushino|Храм Свети Никола, село Белушино|Church|parish
mk-sopotnica-nicholas|Saint Nicholas Church in Sopotnica|Храм Свети Никола, село Сопотница|Church|parish
mk-zhvan-paraskeva-romana|Martyr Paraskeva of Rome Church in Zhvan|Храм Света маченичка Параскева Римјанка, село Жван|Church|parish
mk-zhvan-demetrius|Saint Demetrius the Great Martyr Church in Zhvan|Храм Свети великомаченик Димитриј, село Жван|Church|parish
mk-zhvan-elijah-chapel|Holy Prophet Elijah Chapel in Zhvan|Параклис Свети пророк Илија, село Жван|Chapel|parish
mk-zhvan-archangel-michael-chapel|Holy Archangel Michael Chapel in Zhvan|Параклис Свети Архангел Михаил, село Жван|Chapel|parish
mk-sloeshtica-dormition|Dormition of the Most Holy Theotokos Church in Sloeshtica|Храм Успение на Пресвета Богородица, село Слоештица|Church|parish
mk-sloeshtica-elijah-nicholas-george|Holy Prophet Elijah, Saint Nicholas, and Saint George Church in Sloeshtica|Храм Свети пророк Илија, Свети Никола и Свети великомаченик Георгиј, село Слоештица|Church|parish
mk-mrenoga-ascension|Ascension of Christ Church in Mrenoga|Храм Вознесение Христово, село Мренога|Church|parish
mk-mrenoga-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Mrenoga|Храм Рождество на Пресвета Богородица, село Мренога|Church|parish
mk-virovo-nicholas|Saint Nicholas Church in Virovo|Храм Свети Никола, село Вирово|Church|parish
mk-bazernik-athanasius|Saint Athanasius the Great Church in Bazernik|Храм Свети Атанасиј Велики, село Базерник|Church|parish
mk-babino-nicholas|Saint Nicholas Church in Babino|Храм Свети Никола, село Бабино|Church|parish
mk-dolenci-dormition|Dormition of the Most Holy Theotokos Church in Dolenci|Храм Успение на Пресвета Богородица, село Доленци|Church|parish
mk-brezovo-george|Saint George the Great Martyr Church in Brezovo|Храм Свети великомаченик Георгиј, село Брезово|Church|parish
mk-golemo-ilino-nicholas|Saint Nicholas Church in Golemo Ilino|Храм Свети Никола, село Големо Илино|Church|parish
mk-malo-ilino-nicholas|Saint Nicholas Church in Malo Ilino|Храм Свети Никола, село Мало Илино|Church|parish
mk-radovo-archangel-michael|Holy Archangel Michael Church in Radovo|Храм Свети Архангел Михаил, село Радово|Church|parish
mk-novo-selo-archangel-michael|Holy Archangel Michael Church in Novo Selo|Храм Свети Архангел Михаил, Ново Село|Church|parish
mk-rastojca-nativity-george|Nativity of the Most Holy Theotokos and Saint George Church in Rastojca|Храм Рождество на Пресвета Богородица и Свети великомаченик Георгиј, село Растојца|Church|parish
mk-rakitnica-demetrius|Saint Demetrius the Great Martyr Church in Rakitnica|Храм Свети великомаченик Димитриј, село Ракитница|Church|parish
mk-kochishta-nicholas|Saint Nicholas Church in Kochishta|Храм Свети Никола, село Кочишта|Church|parish
mk-suvo-grlo-athanasius|Saint Athanasius the Great Church in Suvo Grlo|Храм Свети Атанасиј Велики, село Суво Грло|Church|parish
mk-zheleznec-dormition|Dormition of the Most Holy Theotokos Church in Zheleznec|Храм Успение на Пресвета Богородица, село Железнец|Church|parish
mk-zashle-elijah|Holy Prophet Elijah Church in Zashle|Храм Свети пророк Илија, село Зашле|Church|parish
mk-buchin-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Buchin|Храм Рождество на Пресвета Богородица, село Бучин|Church|parish
mk-vogjani-nicholas|Saint Nicholas Church in Vogjani|Храм Свети Никола, село Воѓани|Church|parish
mk-sveta-panteleimon|Saint Panteleimon the Great Martyr Church in Sveta|Храм Свети великомаченик Пантелејмон, село Света|Church|parish
mk-sveta-peter-paul|Holy Apostles Peter and Paul Church in Sveta|Храм Свети апостоли Петар и Павле, село Света|Church|parish
mk-edinakovci-nicholas|Saint Nicholas Church in Edinakovci|Храм Свети Никола, село Единаковци|Church|parish
mk-demir-hisar-nicholas|Saint Nicholas Church in Demir Hisar|Храм Свети Никола, Демир Хисар|Church|parish
mk-strugovo-athanasius|Saint Athanasius the Great Church in Strugovo|Храм Свети Атанасиј Велики, село Стругово|Church|parish
mk-zagoriche-utovo-nicholas|Saint Nicholas Church serving Zagoriche and Utovo|Храм Свети Никола, села Загориче и Утово|Church|parish
mk-obednik-dormition|Dormition of the Most Holy Theotokos Church in Obednik|Храм Успение на Пресвета Богородица, село Обедник|Church|parish
mk-svinishta-george|Saint George the Great Martyr Church in Svinishta|Храм Свети великомаченик Георгиј, село Свињишта|Church|parish
mk-metimer-nicholas|Saint Nicholas Church in Metimer|Храм Свети Никола, село Метимер|Church|parish
mk-smilevo-george-representative|Saint George the Great Martyr Representative Church in Smilevo|Храм Свети великомаченик Георгиј - репрезентативна црква, село Смилево|Church|parish
mk-smilevo-george-cemetery|Saint George the Great Martyr Cemetery Church in Smilevo|Свети великомаченик Георгиј - гробјанска црква, село Смилево|Cemetery Church|parish
mk-slepche-nicholas|Saint Nicholas Church in Slepche|Храм Свети Никола, село Слепче|Church|parish
mk-vardino-nicholas|Saint Nicholas Church in Vardino|Храм Свети Никола, село Вардино|Church|parish
mk-vardino-constantine-helen|Saints Constantine and Helen Church in Vardino|Храм Свети цареви Константин и Елена, село Вардино|Church|parish
mk-barakovo-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Barakovo|Храм Рождество на Пресвета Богородица, село Бараково|Church|parish
mk-graishte-leontius|Holy Martyr Leontius Church in Graishte|Храм Свети маченик Леонтиј, село Граиште|Church|parish
mk-belche-nicholas|Saint Nicholas Church in Belche|Храм Свети Никола, село Белче|Church|parish
mk-zhurche-dormition|Dormition of the Most Holy Theotokos Church in Zhurche|Храм Успение на Пресвета Богородица, село Журче|Church|parish
mk-sladuevo-elijah|Holy Prophet Elijah Church in Sladuevo|Храм Свети пророк Илија, село Сладуево|Church|parish
mk-pribilci-dormition|Dormition of the Most Holy Theotokos Church in Pribilci|Храм Успение на Пресвета Богородица, село Прибилци|Church|parish
mk-kutretino-suvodol-constantine-helen|Saints Constantine and Helen Church serving Kutretino and Suvodol|Храм Свети цареви Константин и Елена, села Кутретино и Суводол|Church|parish
mk-krivogashtani-nicholas|Saint Nicholas Church in Krivogashtani|Храм Свети Никола, село Кривогаштани|Church|parish
mk-krivogashtani-presentation|Presentation of the Most Holy Theotokos Church in Krivogashtani|Храм Воведение на Пресвета Богородица, село Кривогаштани|Church|parish
mk-sveto-mitrani-ascension|Ascension of Christ Church in Sveto Mitrani|Храм Вознесение Христово, село Свето Митрани|Church|parish
mk-sveto-mitrani-nicholas|Saint Nicholas Church in Sveto Mitrani|Храм Свети Никола, село Свето Митрани|Church|parish
mk-vrboec-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Vrboec|Храм Рождество на Пресвета Богородица, село Врбоец|Church|parish
mk-lokveni-holy-trinity|Holy Trinity Church in Lokveni|Храм Света Троица, село Локвени|Church|parish
mk-podvis-holy-trinity|Holy Trinity Church in Podvis|Храм Света Троица, село Подвис|Church|parish
mk-vrbjani-nicholas|Saint Nicholas Church in Vrbjani|Храм Свети Никола, село Врбјани|Church|parish
mk-krivogashtani-demetrius|Saint Demetrius the Great Martyr Church in Krivogashtani|Храм Свети великомаченик Димитриј, село Кривогаштани|Church|parish
mk-krivogashtani-theodores|Holy Great Martyrs Theodore Tyro and Theodore Stratelates Church in Krivogashtani|Храм Свети великомаченик Теодор Тирон и Свети великомаченик Теодор Стратилат, село Кривогаштани|Church|parish
mk-krusheani-athanasius|Saint Athanasius the Great Church in Krusheani|Храм Свети Атанасиј Велики, село Крушеани|Church|parish
mk-krusheani-nicholas-cemetery|Saint Nicholas Cemetery Church in Krusheani|Храм Свети Никола - гробјанска црква, село Крушеани|Cemetery Church|parish
mk-slavej-elijah|Holy Prophet Elijah Church in Slavej|Храм Свети пророк Илија, село Славеј|Church|parish
mk-godivle-athanasius|Saint Athanasius the Great Church in Godivle|Храм Свети Атанасиј Велики, село Годивле|Church|parish
mk-korenica-nicholas|Saint Nicholas Church in Korenica|Храм Свети Никола, село Кореница|Church|parish
""",
    "mk-krusevo-demir-hisar", [KRUSHDEM_PARISHES],
)


KRUSHDEM_MONASTERY_ROWS = table_rows(
    """
mk-krusevo-ascension-monastery|Ascension of Christ Monastery in Krushevo|Манастир Свето Вознесение Христово, Крушево|Monastery|monastery
mk-krusevo-transfiguration-monastery|Transfiguration of Christ Monastery in Krushevo|Манастир Свето Преображение Христово, Крушево|Monastery|monastery
mk-trstenik-basil-monastery|Saint Basil the Great Monastery in Trstenik|Манастир Свети Василиј Велики, село Трстеник|Monastery|monastery
mk-arilevo-athanasius-monastery|Saint Athanasius the Great Monastery in Arilevo|Манастир Свети Атанасиј Велики, село Арилево|Monastery|monastery
mk-strugovo-anthony-monastery|Saint Anthony Monastery in Strugovo|Манастир Свети Антониј, село Стругово|Monastery|monastery
mk-smilevo-peter-paul-monastery|Holy Apostles Peter and Paul Monastery in Smilevo|Манастир Свети апостоли Петар и Павел, село Смилево|Monastery|monastery
mk-toplica-sloeshtica-nicholas-monastery|Saint Nicholas Monastery at Toplica and Sloeshtica|Манастир Свети Никола, села Топлица и Слоештица|Monastery|monastery
mk-zashle-george-monastery|Saint George the Great Martyr Monastery in Zashle|Манастир Свети великомаченик Георгиј, село Зашле|Monastery|monastery
mk-slepche-life-giving-spring-monastery|Life-giving Spring Monastery in Slepche|Манастир Живоприемен извор, село Слепче|Monastery|monastery
mk-zhurche-elijah-monastery|Holy Prophet Elijah Monastery in Zhurche|Манастир Свети пророк Илија, село Журче|Monastery|monastery
mk-kutretino-suvodol-dormition-monastery|Dormition of the Most Holy Theotokos Monastery at Kutretino and Suvodol|Манастир Успение на Пресвета Богородица, села Кутретино и Суводол|Monastery|monastery
mk-buchin-george-monastery|Saint George the Great Martyr Monastery in Buchin|Манастир Свети великомаченик Георгиј, село Бучин|Monastery|monastery
""",
    "mk-krusevo-demir-hisar", [KRUSHDEM_MONASTERIES],
)


SKOPJE_CHURCH_ROWS = table_rows(
    """
mk-skopje-center-nativity-theotokos|Nativity of the Most Holy Theotokos Church in central Skopje|Рождество на Пресвета Богородица, Центар|Church|parish
mk-skopje-center-demetrius|Saint Demetrius the Great Martyr Church in central Skopje|Свети великомаченик Димитриј, Центар|Church|parish
mk-skopje-avtokomanda-michael|Holy Archangel Michael Church in Avtokomanda|Свети архангел Михаил, Автокоманда|Church|parish
mk-skopje-madzari-savior|Holy Savior Church in Madzari|Свети Спас, Маџари|Church|parish
mk-skopje-chair-george|Saint George the Great Martyr Church in Chair|Свети великомаченик Георгиј, Чаир|Church|parish
mk-skopje-north-nicholas|Saint Nicholas Church in Skopje North|Свети Николај, Скопје Север|Church|parish
mk-butel-nativity-john|Nativity of Saint John the Baptist Church in Butel|Раѓање на свети Јован Крстител, Бутел|Church|parish
mk-vizbegovo-savior|Holy Savior Church in Vizbegovo|Свети Спас, Визбегово|Church|parish
mk-chento-george|Saint George the Great Martyr Church in Chento|Свети великомаченик Георгиј, Ченто|Church|parish
mk-stajkovci-cyril-methodius|Saints Cyril and Methodius Church in Stajkovci|Свети Кирил и Методиј, Стајковци|Church|parish
mk-smiljkovci-kyriake|Saint Kyriake Church in Smiljkovci|Света Недела, Смиљковци|Church|parish
mk-smiljkovci-forty-martyrs|Holy Forty Martyrs of Sebaste Church in Smiljkovci|Свети 40 севастиски маленици, Смиљковци|Church|parish
mk-rashtak-savior|Holy Savior Church in Rashtak|Свети Спас, Раштак|Church|parish
mk-bulachani-john-baptist|Saint John the Baptist Church in Bulachani|Свети Јован Крстител, Булачани|Church|parish
mk-creshevo-savior|Holy Savior Church in Creshevo|Свети Спас, Црешево|Church|parish
mk-viniche-elijah|Holy Prophet Elijah Church in Viniche|Свети Илија, Виниче|Church|parish
mk-gjorche-petrov-peter-paul|Holy Apostles Peter and Paul Church in Gjorche Petrov|Свети апостоли Петар и Павле, Ѓорче Петров|Church|parish
mk-orizari-athanasius|Saint Athanasius Church in Orizari|Свети Атанасиј, Оризари|Church|parish
mk-bardovci-trinity|Holy Trinity Church in Bardovci|Света Троица, Бардовци|Church|parish
mk-radishani-nicholas|Saint Nicholas Church in Radishani|Свети Николај, Радишани|Church|parish
mk-radishani-george|Saint George the Great Martyr Church in Radishani|Свети великомаченик Георгиј, Радишани|Church|parish
mk-radishani-naum|Saint Naum of Ohrid Church in Radishani|Свети Наум Охридски, Радишани|Church|parish
mk-marino-trinity|Holy Trinity Church in Marino|Света Троица, Марино|Church|parish
mk-hotel-belvi-petka-balaklija|Saint Petka and Life-giving Spring Church at Hotel Belvi|Света Петка и Источен петок - Балаклија, хотел Белви|Church|parish
mk-petrovec-george|Saint George the Great Martyr Church in Petrovec|Свети великомаченик Георгиј, Петровец|Church|parish
mk-katlanovo-kyriake|Saint Kyriake Church in Katlanovo|Света Недела, Катланово|Church|parish
mk-letevci-savior|Holy Savior Church in Letevci|Свети Спас, Летевци|Church|parish
mk-bader-athanasius|Saint Athanasius Church in Bader|Свети Атанасиј, Бадер|Church|parish
mk-ognjanci-george|Saint George Church in Ognjanci|Свети Георгиј, Огњанци|Church|parish
mk-blace-george|Saint George Church in Blace|Свети Георгиј, Блаце|Church|parish
mk-katlanovo-nicholas|Saint Nicholas Church in Katlanovo|Свети Николај, Катланово|Church|parish
mk-rzhanichino-trinity|Holy Trinity Church in Rzhanichino|Света Троица, Ржаничино|Church|parish
mk-chojlija-trinity|Holy Trinity Church in Chojlija|Света Троица, Чојлија|Church|parish
mk-kadino-elijah|Holy Prophet Elijah Church in Kadino|Свети Илија, Кадино|Church|parish
mk-bunardzhik-savior|Holy Savior Church in Bunardzhik|Свети Спас, Бунарџик|Church|parish
mk-mralino-theotokos|Church of the Theotokos in Mralino|Света Богородица, Мралино|Church|parish
mk-ajvatovci-tryphon|Saint Tryphon Church in Ajvatovci|Свети Трифун, Ајватовци|Church|parish
mk-jurumleri-peter-paul|Holy Apostles Peter and Paul Church in Jurumleri|Свети Петар и Павле, Јурумлери|Church|parish
mk-trubarevo-george|Saint George Church in Trubarevo|Свети Георгиј, Трубарево|Church|parish
mk-volkovo-athanasius|Saint Athanasius Church in Volkovo|Свети Атанасиј, Волково|Church|parish
mk-mirkovci-petka|Saint Petka Church in Mirkovci|Света Петка, Мирковци|Church|parish
mk-mirkovci-nicholas|Saint Nicholas Church in Mirkovci|Свети Николај, Мирковци|Church|parish
mk-mirkovci-mercury|Saint Mercury Church in Mirkovci|Свети Меркјури, Мирковци|Church|parish
mk-mirkovci-george|Saint George the Great Martyr Church in Mirkovci|Свети великомаченик Георгиј, Мирковци|Church|parish
mk-banjani-george|Saint George Church in Banjani|Свети Георгиј, Бањани|Church|parish
mk-gluvo-nicholas|Saint Nicholas Church in Gluvo|Свети Николај, Глуво|Church|parish
mk-gorno-orizari-petka|Saint Petka Church in Gorno Orizari|Светка Петка, Горно Оризари|Church|parish
mk-chucher-sandevo-trinity|Holy Trinity Church in Chucher Sandevo|Света Троица, Чучер Сандево|Church|parish
mk-brazda-theotokos|Church of the Theotokos in Brazda|Света Богородица, Бразда|Church|parish
mk-kuchevishte-savior|Holy Savior Church in Kuchevishte|Свети Спас, Кучевиште|Church|parish
mk-ljubanci-nicholas|Saint Nicholas Church in Ljubanci|Свети Николај, Љубанци|Church|parish
mk-ljubanci-theotokos|Church of the Theotokos in Ljubanci|Света Богородица, Љубанци|Church|parish
mk-ljuboten-nicholas|Saint Nicholas Church in Ljuboten|Свети Николај, Љуботен|Church|parish
mk-pobozhje-petka|Saint Petka Church in Pobozhje|Света Петка, Побожје|Church|parish
mk-kuchevishte-athanasius|Saint Athanasius Church in Kuchevishte|Свети Атанасиј, Кучевиште|Church|parish
mk-kuchevishte-petka|Saint Petka Church in Kuchevishte|Света Петка, Кучевиште|Church|parish
mk-kuchevishte-kyriake|Saint Kyriake Church in Kuchevishte|Света Недела, Кучевиште|Church|parish
mk-skopje-clement-cathedral|Archiepiscopal Cathedral of Saint Clement of Ohrid in central Skopje|Архиепископски соборен храм Свети Климент Охридски, Центар|Cathedral|parish
mk-kapishtec-john-baptist|Saint John the Baptist Church in Kapishtec|Свети Јован Крстител, Капиштец|Church|parish
mk-crniche-petka|Saint Petka Church in Crniche, Kisela Voda|Света Петка, Црниче, Кисела Вода|Church|parish
mk-sredno-vodno-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Sredno Vodno|Рождество на Пресвета Богородица, Средно Водно|Church|parish
mk-aerodrom-elijah|Holy Prophet Elijah Church in Jane Sandanski, Aerodrom|Свети Илија, Јане Сандански, Аеродром|Church|parish
mk-michurin-three-hierarchs|Holy Three Hierarchs Church in Michurin|Свети Три Ерарси, Мичурин|Church|parish
mk-kisela-voda-george|Saint George Church in Kisela Voda|Свети Георгиј, Кисела Вода|Church|parish
mk-usje-athanasius|Saint Athanasius Church in Usje|Свети Атанасиј, Усје|Church|parish
mk-drachevo-savior|Holy Savior Church in Drachevo|Свети Спас, Драчево|Church|parish
mk-zelenikovo-gabriel|Holy Archangel Gabriel Church in Zelenikovo|Свети архангел Гаврил, Зелениково|Church|parish
mk-zelenikovo-george|Saint George Church in Zelenikovo|Свети Георгиј, Зелениково|Church|parish
mk-pakoshevo-peter-paul|Holy Apostles Peter and Paul Church in Pakoshevo|Свети Петар и Павле, Пакошево|Church|parish
mk-novo-selo-nicholas-skopje|Saint Nicholas Church in Novo Selo|Свети Николај, Ново Село|Church|parish
mk-gradovci-george|Saint George Church in Gradovci|Свети Георгиј, Градовци|Church|parish
mk-oreshani-athanasius|Saint Athanasius Church in Oreshani|Свети Атанасиј, Орешани|Church|parish
mk-morani-theotokos|Church of the Theotokos in Morani|Света Богородица, Морани|Church|parish
mk-taor-elijah|Holy Prophet Elijah Church in Taor, Zelenikovo|Свети Илија, Таор, Зелениково|Church|parish
mk-tri-krushi-petka|Saint Petka Church at Tri Krushi|Света Петка, Три Круши|Church|parish
mk-drachevo-lazarus|Raising of Lazarus Church in Drachevo|Воскресение Лазарево, Драчево|Church|parish
mk-dolno-lisiche-trinity|Holy Trinity Church in Dolno Lisiche|Света Троица, Долно Лисиче|Church|parish
mk-gorno-lisiche-peter-paul|Holy Apostles Peter and Paul Church in Gorno Lisiche|Свети апостоли Петар и Павле, Горно Лисиче|Church|parish
mk-sopishte-mina|Saint Menas Church in Sopishte|Свети Мина, Сопиште|Church|parish
mk-rakotinci-theotokos|Church of the Theotokos in Rakotinci|Света Богородица, Ракотинци|Church|parish
mk-govrlevo-nicholas|Saint Nicholas Church in Govrlevo|Свети Николај, Говрлево|Church|parish
mk-pusta-breznica-nicholas|Saint Nicholas Church in Pusta Breznica|Свети Николај, Пуста Брезница|Church|parish
mk-gorno-sonje-nicholas|Saint Nicholas Church in Gorno Sonje|Свети Николај, Горно Соње|Church|parish
mk-dolno-sonje-savior|Holy Savior Church in Dolno Sonje|Свети Спас, Долно Соње|Church|parish
mk-markova-sushica-nicholas|Saint Nicholas Church in Markova Sushica|Свети Николај, Маркова Сушица|Church|parish
mk-varvara-barbara|Holy Martyr Barbara Church in Varvara|Света маченичка Варвара, Варвара|Church|parish
mk-govrlevo-elijah|Holy Prophet Elijah Church in Govrlevo|Свети Илија, Говрлево|Church|parish
mk-dolno-nerezi-panteleimon|Saint Panteleimon Church in Dolno Nerezi|Свети Пантелејмон, Долно Нрези|Church|parish
mk-ajvatovci-peter-paul-chapel|Holy Apostles Peter and Paul Chapel in Ajvatovci|Параклис Свети Петар и Павле, Ајватовци|Chapel|parish
mk-kuchkovo-tryphon-chapel|Saint Tryphon Chapel in Kuchkovo|Параклис Свети Трифун, Кучково|Chapel|parish
mk-pelenica-mid-pentecost-chapel|Mid-Pentecost Chapel in Pelenica|Параклис Преполовение, Пеленица|Chapel|parish
mk-clinical-center-annunciation-chapel|Annunciation Chapel at the Clinical Center in Skopje|Параклис Свето Благовештение, Клинички центар|Chapel|parish
""",
    "mk-skopje", [SKOPJE_CHURCHES],
)


SKOPJE_MONASTERY_ROWS = table_rows(
    """
mk-skopje-savior-monastery|Holy Savior Monastery in central Skopje|Манастир Свети Спас, Центар|Monastery|monastery
mk-gornjani-nikita-monastery|Saint Nikita Monastery in Gornjani|Манастир Свети Никита, Горњани|Monastery|monastery
mk-kuchkovo-george-monastery|Saint George the Great Martyr Monastery in Kuchkovo|Манастир Свети великомаченик Георгиј, Кучково|Monastery|monastery
mk-ljubanci-nicholas-monastery|Saint Nicholas Monastery in Ljubanci|Манастир Свети Николај, Љубанци|Monastery|monastery
mk-kuchevishte-archangels-monastery|Holy Archangels Michael and Gabriel Monastery in Kuchevishte|Манастир Свети архангели Михаил и Гаврил, Кучевиште|Monastery|monastery
mk-krivi-dol-george-monastery|Saint George the Great Martyr Monastery in Krivi Dol|Манастир Свети великомаченик Георгиј, Криви Дол|Monastery|monastery
mk-mirkovci-chardak-elijah-monastery|Saint Elijah Chardak Monastery in Mirkovci|Манастир Свети Илија Чардак, Мирковци, Чучер Сандево|Monastery|monastery
mk-gornjani-gorni-elijah-monastery|Saint Elijah Gorni Monastery in Gornjani|Манастир Свети Илија Горни, Горњани|Monastery|monastery
mk-banjani-elijah-monastery|Holy Prophet Elijah Monastery in Banjani|Манастир Свети Илија, Бањани|Monastery|monastery
mk-banjani-annunciation-monastery|Annunciation Monastery in Banjani|Манастир Свето Благовештение, Бањани|Monastery|monastery
mk-banjani-dormition-monastery|Dormition of the Most Holy Theotokos Monastery in Banjani|Манастир Успение на Пресвета Богородица, Бањани|Monastery|monastery
mk-ljubanci-john-baptist-monastery|Saint John the Baptist Monastery in Ljubanci|Манастир Свети Јован Крстител, Љубанци|Monastery|monastery
mk-pobozhje-theotokos-monastery|Monastery of the Theotokos in Pobozhje|Манастир Света Богородица, Побожје|Monastery|monastery
mk-gluvo-athanasius-monastery|Saint Athanasius Monastery in Gluvo|Манастир Свети Атанасиј, Глуво|Monastery|monastery
mk-kozhle-theotokos-monastery|Monastery of the Theotokos in Kozhle|Манастир Света Богородица, Кожле|Monastery|monastery
mk-gorno-nerezi-panteleimon-monastery|Saint Panteleimon Monastery in Gorno Nerezi|Манастир Свети Пантелејмон, Горно Нерези|Monastery|monastery
mk-markova-sushica-demetrius-monastery|Saint Demetrius the Great Martyr Monastery in Markova Sushica|Манастир Свети великомаченик Димитриј, Маркова Сушица|Monastery|monastery
mk-matka-dormition-monastery|Dormition of the Most Holy Theotokos Monastery in Matka|Манастир Успение на Пресвета Богородица, Матка|Monastery|monastery
mk-matka-andrew-monastery|Saint Andrew Monastery in Matka|Манастир Свети Андреј, Матка|Monastery|monastery
mk-shishevo-nicholas-monastery|Saint Nicholas Monastery in Shishevo|Манастир Свети Николај, Шишево|Monastery|monastery
""",
    "mk-skopje", [SKOPJE_MONASTERIES],
)


DKE_TEMPLE_ROWS = table_rows(
    """
mk-ohrid-perivlepta|Holy Theotokos Perivlepta Church in Ohrid|Света Богородица Перивлепта, Охрид|Church|parish
mk-ohrid-holy-wisdom-cathedral|Holy Wisdom Cathedral in Ohrid|Света Софија, Охрид|Cathedral|parish
mk-ohrid-nicholas-gerakomija|Saint Nicholas Gerakomija Church in Ohrid|Свети Никола Геракомија, Охрид|Church|parish
mk-ohrid-john-kaneo|Saint John the Theologian Church at Kaneo|Свети Јован Богослов - Канео, Охрид|Church|parish
mk-ohrid-demetrius|Saint Demetrius Church in Ohrid|Свети Димитриј, Охрид|Church|parish
mk-ohrid-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Ohrid|Рождество на Пресвета Богородица, Охрид|Church|parish
mk-ohrid-great-unmercenaries|Great Holy Unmercenaries Cosmas and Damian Church in Ohrid|Големи Свети Врачи - Козма и Дамјан, Охрид|Church|parish
mk-ohrid-nicholas-wonderworker|Saint Nicholas the Wonderworker Church in Ohrid|Свети Никола Чудотворец, Охрид|Church|parish
mk-ohrid-nicholas-dolna-maala|Saint Nicholas Church in Dolna Maala, Ohrid|Свети Никола - Долна Маала, Охрид|Church|parish
mk-ohrid-barbara|Saint Barbara Church in Ohrid|Света Варвара, Охрид|Church|parish
mk-ohrid-theotokos-pandanos|Holy Theotokos Pandanos Church in Ohrid|Света Богородица Панданос, Охрид|Church|parish
mk-ohrid-little-unmercenaries|Little Holy Unmercenaries Cosmas and Damian Church in Ohrid|Мали Свети Врачи - Козма и Дамјан, Охрид|Church|parish
mk-ohrid-nicholas-bolnichki|Saint Nicholas Bolnichki Church in Ohrid|Свети Никола Болнички, Охрид|Church|parish
mk-ohrid-theotokos-bolnichka|Holy Theotokos Bolnichka Church in Ohrid|Света Богородица Болничка, Охрид|Church|parish
mk-ohrid-little-clement|Little Saint Clement of Ohrid Church in Ohrid|Свети Климент Охридски - Мал Свети Климент, Охрид|Church|parish
mk-ohrid-constantine-helen|Saints Constantine and Helen Church in Ohrid|Свети Константин и Елена, Охрид|Church|parish
mk-ohrid-theotokos-chelnica|Holy Theotokos Chelnica Church in Ohrid|Света Богородица - Челница, Охрид|Church|parish
mk-ohrid-kamensko-dormition|Dormition of the Most Holy Theotokos Church at Kamensko, Ohrid|Успение на Пресвета Богородица - Каменско, Охрид|Church|parish
mk-ohrid-george|Saint George the Great Martyr Church in Ohrid|Свети Великомаченик Георгиј, Охрид|Church|parish
mk-ohrid-radojca-trinity|Holy Trinity Church in Radojca Novichikj, Ohrid|Света Троица, населба Радојца Новичиќ, Охрид|Church|parish
mk-velgoshti-panteleimon|Saint Panteleimon Church in Velgoshti|Свети Пантелејмон, Велгошти|Church|parish
mk-peshtani-unmercenaries|Holy Unmercenaries Cosmas and Damian Church in Peshtani|Свети безсребреници Кузман и Дамјан, Пештани|Church|parish
mk-kicevo-peter-paul|Holy Apostles Peter and Paul Church in Kichevo|Свети апостоли Петар и Павле, Кичево|Church|parish
mk-struga-george|Saint George the Great Martyr Church in Struga|Свети великомаченик Ѓорѓи, Струга|Church|parish
mk-vevchani-nicholas|Saint Nicholas Church in Vevchani|Свети Никола, Вевчани|Church|parish
""",
    "mk-debar-kicevo", [DKE_TEMPLES_1, DKE_TEMPLES_2, DKE_CONTACT],
)


DKE_MONASTERY_ROWS = table_rows(
    """
mk-bigorski-john-baptist-monastery|Saint John the Baptist Bigorski Monastery|Манастир Свети Јован Крстител - Бигорски|Monastery|monastery
mk-knezhino-george-monastery|Saint George Monastery in Knezhino, Kichevo|Манастир Свети Георгиј - Кнежино, Кичевско|Monastery|monastery
mk-plaoshnik-clement-panteleimon-monastery|Saints Clement and Panteleimon Monastery at Plaoshnik|Манастир Свети Климент и Пантелејмон - Плаошник|Monastery|monastery
mk-gorni-manastirec-nativity-monastery|Nativity of the Most Holy Theotokos Monastery in Gorni Manastirec|Манастир Рождество на Пресвета Богородица - Горни Манастирец, Македонски Брод|Monastery|monastery
mk-rajchica-george-monastery|Saint George the Victorious Monastery in Rajchica|Манастир Свети Георгиј Победоносец - Рајчица|Monastery|monastery
mk-leshani-all-saints-monastery|All Saints Monastery in Leshani|Манастир Сите Светии - Си Свети - Лешани, Охридско|Monastery|monastery
mk-ohrid-naum-monastery|Saint Naum of Ohrid Monastery in Ohrid|Манастир Свети Наум Охридски - Охрид|Monastery|monastery
mk-ohrid-stephen-monastery|Saint Stephen Monastery in Ohrid|Манастир Свети Стефан - Охрид|Monastery|monastery
mk-ohrid-zaum-theotokos-monastery|Holy Theotokos Zaum Monastery in Ohrid|Манастир Света Богородица Заумска - Охрид|Monastery|monastery
mk-kicevo-prechista-monastery|Holy Theotokos Prechista Monastery in Kichevo|Манастир Света Богородица Пречиста - Кичево|Monastery|monastery
mk-ohrid-erasmus-monastery|Saint Erasmus of Ohrid Monastery in Ohrid|Манастир Свети Еразмо Охридски - Охрид|Monastery|monastery
mk-velgoshti-petka-monastery|Saint Petka Monastery in Velgoshti|Манастир Света Петка - Велгошти, Охридско|Monastery|monastery
mk-gorno-lakocerej-ascension-monastery|Ascension of Christ and Holy Savior Monastery in Gorno Lakocerej|Манастир Вознесение Христово - Свети Спас - Горно Лакочереј, Охридско|Monastery|monastery
""",
    "mk-debar-kicevo", [DKE_MONASTERIES_1, DKE_MONASTERIES_2],
)


KOE_ROWS = table_rows(
    """
mk-koe-kumanovo-kratovo-deanery|Kumanovo and Kratovo Deanery|Кумановско-кратовско архиерејско намесништво|Deanery|diocese
mk-koe-kriva-palanka-deanery|Kriva Palanka Deanery|Кривопаланечко архиерејско намесништво|Deanery|diocese
mk-kumanovo-first-parish|First Parish of Kumanovo|Прва парохија, Куманово|Parish|parish
mk-kumanovo-second-parish|Second Parish of Kumanovo|Втора парохија, Куманово|Parish|parish
mk-kumanovo-third-parish|Third Parish of Kumanovo|Трета парохија, Куманово|Parish|parish
mk-kumanovo-fourth-parish|Fourth Parish of Kumanovo|Четврта парохија, Куманово|Parish|parish
mk-kumanovo-fifth-parish|Fifth Parish of Kumanovo|Петта парохија, Куманово|Parish|parish
mk-kumanovo-sixth-parish|Sixth Parish of Kumanovo|Шеста парохија, Куманово|Parish|parish
mk-kumanovo-seventh-parish|Seventh Parish of Kumanovo|Седма парохија, Куманово|Parish|parish
mk-kumanovo-eighth-parish|Eighth Parish of Kumanovo|Осма парохија, Куманово|Parish|parish
mk-kumanovo-ninth-parish|Ninth Parish of Kumanovo|Деветта парохија, Куманово|Parish|parish
mk-kumanovo-tenth-parish|Tenth Parish of Kumanovo|Десетта парохија, Куманово|Parish|parish
mk-kumanovo-eleventh-parish|Eleventh Parish of Kumanovo|Единаесетта парохија, Куманово|Parish|parish
mk-kumanovo-twelfth-parish|Twelfth Parish of Kumanovo|Дванаесетта парохија, Куманово|Parish|parish
mk-kumanovo-thirteenth-parish|Thirteenth Parish of Kumanovo|Тринаесетта парохија, Куманово|Parish|parish
mk-kumanovo-fourteenth-parish|Fourteenth Parish of Kumanovo|Четиринаесетта парохија, Куманово|Parish|parish
mk-kumanovo-fifteenth-parish|Fifteenth Parish of Kumanovo|Петнаесетта парохија, Куманово|Parish|parish
mk-kumanovo-sixteenth-parish|Sixteenth Parish of Kumanovo|Шеснаесетта парохија, Куманово|Parish|parish
mk-karpino-zheglane-parish|Karpino and Zheglane Parish|Карпинско-жегљанска парохија|Parish|parish
mk-staro-nagorichane-parish|Staro Nagorichane Parish|Старонагоричка парохија|Parish|parish
mk-mlado-nagorichane-parish|Mlado Nagorichane Parish|Младонагоричка парохија|Parish|parish
mk-orashac-parish|Orashac Parish|Орашачка парохија|Parish|parish
mk-tabanovce-parish|Tabanovce Parish|Табановачка парохија|Parish|parish
mk-pchinja-parish|Pchinja Parish|Пчињска парохија|Parish|parish
mk-klechovce-parish|Klechovce Parish|Клечовска парохија|Parish|parish
mk-kumanovo-nicholas-cathedral|Saint Nicholas Metropolitan Cathedral in Kumanovo|Митрополитски соборен храм Свети Никола, Куманово|Cathedral|parish
mk-osogovo-joachim-monastery|Saint Joachim of Osogovo Monastery|Манастир Свети Јоаким Осоговски|Monastery|monastery
mk-karpino-presentation-monastery|Karpino Presentation of the Most Holy Theotokos Monastery|Карпински Воведенски манастир|Monastery|monastery
mk-staro-nagorichane-george-monastery|Saint George the Great Martyr Monastery in Staro Nagorichane|Манастир Свети великомаченик Георгиј - Старо Нагоричане|Monastery|monastery
mk-psacha-nicholas-monastery|Saint Nicholas the Wonderworker Monastery in Psacha|Манастир Свети Николај Чудотворец - Псача|Monastery|monastery
""",
    "mk-kumanovo-osogovo", [KOE_ROSTER],
)


TGE_ROWS = table_rows(
    """
mk-tetovo-petka-kyriake|Saint Petka and Saint Kyriake Church in Tetovo|Црква Свети Петка и Света Недела, Тетово|Church|parish
mk-tetovo-demetrius|Saint Demetrius Church in Tetovo|Црква Свети Димитриј, Тетово|Church|parish
mk-tetovo-theotokos|Church of the Theotokos in Tetovo|Црква Света Богородица, Тетово|Church|parish
mk-tetovo-athanasius|Saint Athanasius Church in Tetovo|Црква Свети Атанасиј, Тетово|Church|parish
mk-gostivar-petka|Saint Petka Church in Gostivar|Црква Света Петка, Гостивар|Church|parish
mk-gostivar-demetrius|Saint Demetrius Church in Gostivar|Црква Свети Димитрија, Гостивар|Church|parish
""",
    "mk-tetovo-gostivar", [TGE_ROSTER],
)


BREGALNICA_ROWS = table_rows(
    """
mk-bregalnica-stip-deanery|Stip Deanery|Штипско архиерејско намесништво|Deanery|diocese
mk-bregalnica-kochani-deanery|Kochani Deanery|Кочанско архиерејско намесништво|Deanery|diocese
mk-bregalnica-radovish-deanery|Radovish Deanery|Радовишко архиерејско намесништво|Deanery|diocese
mk-bregalnica-vinica-deanery|Vinica Deanery|Виничко архиерејско намесништво|Deanery|diocese
mk-krupishte-lakavica-parish|Krupishte and Lakavica Parish|Крупишко-лакавичка парохија|Parish|parish
mk-karbin-parish|Karbin Parish|Карбинска парохија|Parish|parish
mk-orizari-parish-bregalnica|Orizari Parish|Оризари|Parish|parish
mk-obleshevo-parish|Obleshevo Parish|Облешево|Parish|parish
mk-zrnovci-parish|Zrnovci Parish|Зрновци|Parish|parish
mk-sokolarci-spanchevo-parish|Sokolarci and Spanchevo Parish|Соколарци и Спанчево|Parish|parish
mk-grdovci-parish|Grdovci Parish|Грдовци|Parish|parish
mk-injevo-konche-parish|Injevo and Konche Parish|Ињевско-конченска парохија|Parish|parish
mk-voislavci-parish|Voislavci Parish|Воиславска парохија|Parish|parish
mk-podaresh-parish|Podaresh Parish|Подарешка парохија|Parish|parish
mk-stip-nicholas-cathedral|Saint Nicholas Cathedral in Stip|Соборен храм Свети Николај, Штип|Cathedral|parish
mk-stip-clement|Saint Clement of Ohrid Church in Stip|Храм Свети Климент Охридски, Штип|Church|parish
mk-stip-petka|Saint Petka Church in Stip|Храм Света Петка, Штип|Church|parish
mk-novo-selo-dormition-stip|Dormition of the Most Holy Theotokos Church in Novo Selo, Stip|Храм Успение на Пресвета Богородица, Ново Село, Штип|Church|parish
mk-sveti-nikole-lydia|Saint Lydia of Macedonia Church in Sveti Nikole|Храм Света Лидија Македонска, Свети Николе|Church|parish
mk-radovish-elijah|Holy Prophet Elijah Church in Radovish|Храм Свети пророк Илија, Радовиш|Church|parish
""",
    "mk-bregalnica", [BREGALNICA_DEANERIES],
)

for item in BREGALNICA_ROWS:
    if item["id"].startswith("mk-stip-") or item["id"] in {
        "mk-krupishte-lakavica-parish", "mk-karbin-parish",
        "mk-sveti-nikole-lydia", "mk-novo-selo-dormition-stip",
    }:
        item["sources"] = [BREGALNICA_STIP]
    elif item["id"] in {
        "mk-orizari-parish-bregalnica", "mk-obleshevo-parish",
        "mk-zrnovci-parish", "mk-sokolarci-spanchevo-parish",
        "mk-grdovci-parish",
    }:
        item["sources"] = [BREGALNICA_KOCANI]
    elif item["id"] in {
        "mk-injevo-konche-parish", "mk-voislavci-parish",
        "mk-podaresh-parish", "mk-radovish-elijah",
    }:
        item["sources"] = [BREGALNICA_RADOVIS]
    elif item["id"] == "mk-bregalnica-vinica-deanery":
        item["sources"] = [BREGALNICA_VINICA]


STRUMICA_ROWS = table_rows(
    """
mk-strumica-fifteen-martyrs-monastery|Holy Fifteen Hieromartyrs of Tiberiopolis Monastery in Strumica|Манастир Свети Петнаесет Тиверополски свештено-маченици, Струмица|Monastery|monastery
mk-strumica-elijah-monastery|Holy Prophet Elijah Monastery in Strumica|Манастир Свети Илија, Струмица|Monastery|monastery
mk-veljusa-eleusa-monastery|Most Holy Theotokos Eleusa Monastery in Veljusa|Манастир Пресвета Богородица Елеуса, село Вељуса|Monastery|monastery
mk-vodocha-leontius-monastery|Protection of the Most Holy Theotokos and Saint Leontius Monastery in Vodocha|Манастир Покров на Пресвета Богородица и Свети Леонтиј, село Водоча|Monastery|monastery
mk-star-dojran-parthenius-monastery|Saint Parthenius Zograf Monastery in Star Dojran|Манастир Свети Партениј Зографски, Стар Дојран|Monastery|monastery
mk-bansko-forty-martyrs-monastery|Holy Forty Martyrs Monastery in Bansko|Манастир Свети 40 маченици, село Банско|Monastery|monastery
""",
    "mk-strumica", [MOC_MONASTERIES],
)

for item in STRUMICA_ROWS:
    if item["id"] == "mk-vodocha-leontius-monastery":
        item["sources"] = [MOC_MONASTERIES, TIVERIOPOL_VODOCHA]


PRESPA_ROWS = table_rows(
    """
mk-bitola-demetrius-cathedral|Saint Demetrius Cathedral in Bitola|Соборен храм Свети Димитриј, Битола|Cathedral|parish
mk-bitola-cathedral-first-parish|First Parish at Saint Demetrius Cathedral in Bitola|Прва парохија при Соборниот храм Свети Димитриј, Битола|Parish|parish
mk-bitola-cathedral-second-parish|Second Parish at Saint Demetrius Cathedral in Bitola|Втора парохија при Соборниот храм Свети Димитриј, Битола|Parish|parish
mk-bitola-cathedral-third-parish|Third Parish at Saint Demetrius Cathedral in Bitola|Трета парохија при Соборниот храм Свети Димитриј, Битола|Parish|parish
mk-bitola-cathedral-fourth-parish|Fourth Parish at Saint Demetrius Cathedral in Bitola|Четврта парохија при Соборниот храм Свети Димитриј, Битола|Parish|parish
""",
    "mk-prespa-pelagonia", [PPPE_BITOLA, SPC_BITOLA],
)


BREGALNICA_ACTIVE_MONASTERY_ROWS = table_rows(
    """
mk-lesnovo-archangel-michael-gabriel-monastery|Holy Archangel Michael and Saint Gabriel of Lesnovo Monastery in Lesnovo|Манастир Свети Архангел Михаил и Свети Гаврил Лесновски, село Лесново|Monastery|monastery
mk-pantelej-panteleimon-monastery|Saint Panteleimon Monastery in Pantelej, Kochani|Манастир Свети Пантелејмон, село Пантелеј, Кочанско|Monastery|monastery
mk-berovo-archangel-michael-monastery|Holy Archangel Michael Monastery in Berovo|Манастир Свети Архангел Михаил, Берово|Monastery|monastery
mk-oraovica-george-monastery|Saint George the Victorious Monastery in Oraovica|Манастир Свети Ѓорѓи Победоносец, Ораовица, Радовишко|Monastery|monastery
mk-stip-kyriake-monastery|Saint Kyriake Monastery in Stip|Манастир Света Недела, Штип|Monastery|monastery
mk-djurishte-theotokos-monastery|Holy Theotokos Monastery at Djurishte|Манастир Света Богородица, Ѓуриште, Светиниколско|Monastery|monastery
mk-probishtip-elijah-monastery|Holy Prophet Elijah Monastery in Probishtip|Манастир Свети Илија, Пробиштип|Monastery|monastery
mk-zletovo-spyridon-monastery|Saint Spyridon Monastery in Zletovo|Манастир Свети Спиридон, Злетово|Monastery|monastery
""",
    "mk-bregalnica", [MOC_MONASTERIES],
)
for item in BREGALNICA_ACTIVE_MONASTERY_ROWS:
    if item["id"] == "mk-lesnovo-archangel-michael-gabriel-monastery":
        item["sources"] = [MOC_MONASTERIES, "https://www.m-p-c.org/?p=3741"]


BREGALNICA_NEWS_MONASTERY_ROWS = [
    row(
        "mk-orizari-dobra-voda-life-giving-spring-monastery",
        "mk-bregalnica",
        "Life-giving Spring of the Most Holy Theotokos Monastery at "
        "Dobra Voda in Orizari",
        "Манастир Пресвета Богородица - Источен Петок, Балаклија, "
        "Добра Вода, село Оризари, Кочанско",
        "Monastery", "monastery", [BREGALNICA_NEWS_5],
    ),
    row(
        "mk-ponikva-basil-monastery", "mk-bregalnica",
        "Saint Basil the Great Monastery at Ponikva",
        "Манастир Свети Василиј Велики, Пониква, Кочанско",
        "Monastery", "monastery", [BREGALNICA_NEWS_5],
    ),
    row(
        "mk-zletovo-marena-life-giving-spring-monastery",
        "mk-bregalnica",
        "Life-giving Spring of the Most Holy Theotokos Monastery at "
        "Marena in Zletovo",
        "Манастир Пресвета Богородица - Животоносен извор, Марена, "
        "село Злетово",
        "Monastery", "monastery",
        [BREGALNICA_NEWS_3, BREGALNICA_NEWS_2],
    ),
    row(
        "mk-blatec-george-monastery", "mk-bregalnica",
        "Saint George the Great-Martyr Monastery in Blatec",
        "Манастир Свети великомаченик Георгиј, село Блатец, Виничко",
        "Monastery", "monastery", [BREGALNICA_NEWS_5],
    ),
]


PRESPA_ACTIVE_MONASTERY_ROWS = table_rows(
    """
mk-novaci-nativity-theotokos-monastery|Nativity of the Most Holy Theotokos Monastery in Novaci|Манастир Рождество на Пресвета Богородица, село Новаци|Monastery|monastery
mk-zrze-transfiguration-monastery|Transfiguration of Christ Monastery in Zrze|Манастир Преображение Господово, село Зрзе|Monastery|monastery
mk-kurbinovo-george-monastery|Saint George the Victorious Monastery in Kurbinovo|Манастир Свети Ѓорѓи Победоносец, Курбиново, Преспа|Monastery|monastery
mk-slivnica-nativity-theotokos-monastery|Nativity of the Most Holy Theotokos Monastery in Slivnica|Манастир Рождество на Пресвета Богородица, Сливница, Преспа|Monastery|monastery
mk-varosh-nicholas-monastery|Saint Nicholas Monastery in Varosh, Prilep|Манастир Свети Никола, Варош, Прилепско|Monastery|monastery
mk-treskavec-dormition-monastery|Dormition of the Most Holy Theotokos Treskavec Monastery|Манастир Успение на Пресвета Богородица - Трескавец, Прилепско|Monastery|monastery
mk-crnec-peter-paul-monastery|Holy Apostles Peter and Paul Monastery in Crnec|Манастир Свети апостоли Петар и Павле, село Црнеец|Monastery|monastery
""",
    "mk-prespa-pelagonia", [MOC_MONASTERIES],
)
for item in PRESPA_ACTIVE_MONASTERY_ROWS:
    if item["id"] == "mk-crnec-peter-paul-monastery":
        item["sources"] = [
            MOC_MONASTERIES,
            "https://www.pppe.mk/2023/"
            "sveti-apostoli-petar-i-pavle-praznichna-vecherna-"
            "bogosluzhba-vo-manastirot-sveti-apostoli-petar-i-pavle-"
            "vo-tsrneets-2/",
        ]

PRESPA_NEWS_MONASTERY_ROWS = [
    row(
        "mk-mariovo-manastir-nicholas-monastery",
        "mk-prespa-pelagonia",
        "Saint Nicholas Monastery in Manastir, Mariovo",
        "Манастир Свети Никола, село Манастир, Мариово",
        "Monastery", "monastery", [BREGALNICA_NEWS_2],
    ),
]


POVARDARIE_ACTIVE_MONASTERY_ROWS = [
    row(
        "mk-sermenin-elijah-monastery", "mk-povardarie",
        "Holy Prophet Elijah Monastery in Sermenin",
        "Манастир Свети пророк Илија, Серменин",
        "Monastery", "monastery",
        [
            MOC_MONASTERIES,
            "https://www.povardarska-eparhija.org.mk/pe//index.php?"
            "Itemid=32&id=1482&option=com_content&task=view",
        ],
    ),
]


TGE_ACTIVE_MONASTERY_ROWS = [
    row(
        "mk-leshok-athanasius-dormition-monastery", "mk-tetovo-gostivar",
        "Saint Athanasius the Great and Dormition of the Most Holy "
        "Theotokos Leshok Monastery",
        "Лешочки манастир Свети Атанасиј Велики и Успение на "
        "Пресвета Богородица, Лешок",
        "Monastery", "monastery",
        [
            "https://tge.mk/product/prepodobniot-kiril-leshochki",
            "https://tge.mk/vecerna-bogosluzba-vo-lesockiot-manastir-na-"
            "praznikot-uspenie-na-presveta-bogorodica",
        ],
    ),
]


POVARDARIE_HIERARCHY_ROWS = (
    table_rows(
        """
mk-povardarie-gevgelija-deanery|Gevgelija Deanery|Гевгелиско архиерејско намесништво|Deanery|diocese
mk-bogdanci-parish|Bogdanci Parish|Богданска парохија|Parish|parish
mk-negorci-parish|Negorci Parish|Негорска парохија|Parish|parish
mk-valandovo-parish|Valandovo Parish|Валандовска парохија|Parish|parish
mk-miravci-parish|Miravci Parish|Миравска парохија|Parish|parish
mk-pirava-parish|Pirava Parish|Пиравска парохија|Parish|parish
mk-stojakovo-parish|Stojakovo Parish|Стојаковска парохија|Parish|parish
""",
        "mk-povardarie", [POVARDARIE_CATEGORY, POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-povardarie-veles-deanery|Veles Deanery|Велешко архиерејско намесништво|Deanery|diocese
mk-bashino-selo-parish|Bashino Selo Parish|Башиноселска парохија|Parish|parish
mk-karatmanovo-lozovo-parish|Karatmanovo and Lozovo Parish|Каратмановско-лозовска парохија|Parish|parish
mk-gradsko-parish|Gradsko Parish|Градска парохија|Parish|parish
mk-izvor-parish|Izvor Parish|Изворска парохија|Parish|parish
mk-bogomila-parish|Bogomila Parish|Богомилска парохија|Parish|parish
mk-chashka-parish|Chashka Parish|Чашка парохија|Parish|parish
""",
        "mk-povardarie", [POVARDARIE_CATEGORY, POVARDARIE_VELES],
    )
    + table_rows(
        """
mk-povardarie-kavadarci-deanery|Kavadarci Deanery|Кавадаречко архиерејско намесништво|Deanery|diocese
mk-vatasha-parish|Vatasha Parish|Ваташка парохија|Parish|parish
mk-rosoman-parish|Rosoman Parish|Росоманска парохија|Parish|parish
mk-demir-kapija-parish|Demir Kapija Parish|Демиркаписка парохија|Parish|parish
mk-timjanik-parish|Timjanik Parish|Тимјаничка парохија|Parish|parish
mk-marena-parish|Marena Parish|Маренска парохија|Parish|parish
""",
        "mk-povardarie", [POVARDARIE_CATEGORY, POVARDARIE_KAVADARCI],
    )
)


POVARDARIE_GEVGELIJA_ROWS = (
    table_rows(
        """
mk-gevgelija-ascension|Ascension of Christ and Holy Savior Church in Gevgelija|Црква Вознесение Христово - Свети Спас, Гевгелија|Church|parish
mk-gevgelija-cyril-methodius|Saints Cyril and Methodius Church in Gevgelija|Црква Свети Кирил и Методиј, Гевгелија|Church|parish
mk-moin-archangel-michael|Holy Archangel Michael Church in Moin|Црква Свети Архангел Михаил, Моин|Church|parish
mk-mrzenci-constantine-helen|Saints Constantine and Helen Church in Mrzenci|Црква Свети Константин и Елена, Мрзенци|Church|parish
""",
        "mk-povardarie", [povardarie_article(367), POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-negorci-athanasius|Saint Athanasius the Great Church in Negorci|Црква Свети Атанасиј Велики, Негорци|Church|parish
mk-prdejci-petka|Saint Petka Church in Prdejci|Црква Света Петка, Прдејци|Church|parish
mk-smokvica-demetrius|Saint Demetrius Church in Smokvica|Црква Свети Димитриј, Смоквица|Church|parish
mk-kovanec-demetrius|Saint Demetrius Church in Kovanec|Црква Свети Димитриј, Кованец|Church|parish
mk-sermenin-george|Saint George Church in Sermenin|Црква Свети Ѓорѓи, Серменин|Church|parish
""",
        "mk-povardarie", [povardarie_article(365), POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-bogdanci-athanasius|Saint Athanasius Church in Bogdanci|Црква Свети Атанасиј, Богданци|Church|parish
mk-gjavoto-dormition|Dormition of the Most Holy Theotokos Church in Gjavoto|Црква Успение на Пресвета Богородица, Ѓавото|Church|parish
""",
        "mk-povardarie", [povardarie_article(366), POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-valandovo-george-monastery|Saint George Monastery in Valandovo|Манастир Свети Ѓорѓи, Валандово|Monastery|monastery
mk-valandovo-demetrius|Saint Demetrius Church in Valandovo|Црква Свети Димитриј, Валандово|Church|parish
mk-brajkovci-george|Saint George Church in Brajkovci|Црква Свети Ѓорѓи, Брајковци|Church|parish
mk-balinci-demetrius|Saint Demetrius Church in Balinci|Црква Свети Димитриј, Балинци|Church|parish
mk-marvinci-petka|Saint Petka Church in Marvinci|Црква Света Петка, Марвинци|Church|parish
mk-grchishte-archangel-michael|Holy Archangel Michael Church in Grchishte|Црква Свети Архангел Михаил, Грчиште|Church|parish
mk-gradec-demetrius|Saint Demetrius Church in Gradec|Црква Свети Димитриј, Градец|Church|parish
mk-gradec-athanasius-monastery|Saint Athanasius Monastery in Gradec|Манастир Свети Атанасиј, Градец|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(364), POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-miravci-constantine-helen|Saints Constantine and Helen Church in Miravci|Црква Свети Константин и Елена, Миравци|Church|parish
mk-davidovo-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Davidovo|Црква Рождество на Пресвета Богородица, Давидово|Church|parish
mk-petrovo-ascension|Ascension of Christ Church in Petrovo|Црква Вознесение Христово, Петрово|Church|parish
mk-miletkovo-petka|Saint Petka Church in Miletkovo|Црква Света Петка, Милетково|Church|parish
mk-gabrovo-athanasius|Saint Athanasius the Great Church in Gabrovo|Црква Свети Атанасиј Велики, Габрово|Church|parish
mk-davidovo-elijah-monastery|Saint Elijah Monastery in Davidovo|Манастир Свети Илија, Давидово|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(363), POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-pirava-george|Saint George Church in Pirava|Црква Свети Ѓорѓи, Пирава|Church|parish
mk-josifovo-dormition|Dormition of the Most Holy Theotokos Church in Josifovo|Црква Успение на Пресвета Богородица, Јосифово|Church|parish
mk-udovo-athanasius|Saint Athanasius the Great Church in Udovo|Црква Свети Атанасиј Велики, Удово|Church|parish
""",
        "mk-povardarie", [povardarie_article(362), POVARDARIE_GEVGELIJA],
    )
    + table_rows(
        """
mk-stojakovo-kyriake|Saint Kyriake Church in Stojakovo|Црква Света Недела, Стојаково|Church|parish
mk-bogorodica-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Bogorodica|Црква Рождество на Пресвета Богородица, Богородица|Church|parish
""",
        "mk-povardarie", [povardarie_article(361), POVARDARIE_GEVGELIJA],
    )
)


POVARDARIE_VELES_ROWS = (
    table_rows(
        """
mk-veles-panteleimon-cathedral|Holy Great-Martyr Panteleimon Cathedral in Veles|Соборен храм Свети великомаченик Пантелејмон, Велес|Cathedral|parish
mk-veles-panteleimon-demetrius-chapel|Saint Demetrius Chapel in Holy Great-Martyr Panteleimon Cathedral|Параклис Свети Димитриј во Соборниот храм Свети великомаченик Пантелејмон, Велес|Chapel|parish
mk-veles-panteleimon-menas-chapel|Saint Menas Chapel in Holy Great-Martyr Panteleimon Cathedral|Параклис Свети Мина во Соборниот храм Свети великомаченик Пантелејмон, Велес|Chapel|parish
mk-veles-dormition|Dormition of the Most Holy Theotokos Church in Veles|Црква Успение на Пресвета Богородица, Велес|Church|parish
mk-veles-ascension|Ascension of Christ and Holy Savior Church in Veles|Црква Вознесение Христово - Свети Спас, Велес|Church|parish
mk-veles-john-baptist|Saint John the Baptist Church in Veles|Црква Свети Јован Крстител, Велес|Church|parish
mk-veles-cyril-methodius|Saints Cyril and Methodius Church in Veles|Црква Свети Кирил и Методиј, Велес|Church|parish
mk-veles-cosmas-damian-hospital|Saints Cosmas and Damian Hospital Church in Veles|Болнички храм Свети Козма и Дамјан, Велес|Hospital Church|parish
mk-veles-george-chapel|Saint George Chapel in Veles|Параклис Свети Ѓорѓи, Велес|Chapel|parish
mk-veles-gabriel-velika-chapel|Saint Gabriel of Velika Chapel in Veles|Параклис Свети Гаврил Велички, Велес|Chapel|parish
mk-veles-naum-ohrid-chapel|Saint Naum of Ohrid Chapel in Veles|Параклис Свети Наум Охридски, Велес|Chapel|parish
mk-veles-elijah-ridot-monastery|Saint Elijah at Ridot Monastery in Veles|Манастир Свети Илија - Ридот, Велес|Monastery|monastery
mk-veles-demetrius-monastery|Holy Great-Martyr Demetrius Monastery in Veles|Манастир Свети великомаченик Димитриј, Велес|Monastery|monastery
mk-veles-petka|Saint Petka Church in Veles|Црква Света Петка, Велес|Church|parish
mk-veles-nicholas-chapel|Saint Nicholas Chapel in Veles|Параклис Свети Никола, Велес|Chapel|parish
mk-veles-john-chapel|Saint John Chapel in Veles|Параклис Свети Јован, Велес|Chapel|parish
mk-veles-kyriake-chapel|Saint Kyriake Chapel in Veles|Параклис Света Недела, Велес|Chapel|parish
mk-veles-anna-chapel|Saint Anna Chapel in Veles|Параклис Света Ана, Велес|Chapel|parish
mk-otovica-george-victorious|Saint George the Victorious Church in Otovica|Црква Свети Георгиј Победоносец, Отовица|Church|parish
""",
        "mk-povardarie", [povardarie_article(35, 46), povardarie_article(47)],
    )
    + table_rows(
        """
mk-bashino-selo-nicholas|Saint Nicholas Church in Bashino Selo|Црква Свети Никола, Башино Село|Church|parish
mk-karatmanovo-protection-theotokos|Protection of the Most Holy Theotokos Church in Karatmanovo|Црква Покров на Пресвета Богородица, Каратманово|Church|parish
mk-novachani-athanasius|Saint Athanasius Church in Novachani|Црква Свети Атанасиј, Новачани|Church|parish
mk-karabunishte-elijah-monastery|Saint Elijah Monastery in Karabunishte|Манастир Свети Илија, Карабуниште|Monastery|monastery
mk-vetersko-john-baptist-monastery|Saint John the Baptist Monastery in Vetersko|Манастир Свети Јован Крстител, Ветерско|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(382), POVARDARIE_VELES],
    )
    + table_rows(
        """
mk-gradsko-george|Saint George Church in Gradsko|Црква Свети Ѓорѓи, Градско|Church|parish
mk-ulanci-nicholas|Saint Nicholas Church in Ulanci|Црква Свети Никола, Уланци|Church|parish
mk-nogaevci-ascension|Ascension of Christ Church in Nogaevci|Црква Вознесение Христово, Ногаевци|Church|parish
mk-dolno-chichevo-athanasius|Saint Athanasius Church in Dolno Chichevo|Црква Свети Атанасиј, Долно Чичево|Church|parish
mk-podles-trinity|Holy Trinity Church in Podles|Црква Света Троица, Подлес|Church|parish
mk-skachinci-trinity|Holy Trinity Church in Skachinci|Црква Света Троица, Скачинци|Church|parish
mk-svekjani-constantine-helen|Saints Constantine and Helen Church in Svekjani|Црква Свети Константин и Елена, Свеќани|Church|parish
mk-chichevo-archangel-michael-monastery|Holy Archangel Michael Monastery in Chichevo|Манастир Свети Архангел Михаил, Чичево|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(381), POVARDARIE_VELES],
    )
    + table_rows(
        """
mk-bogomila-athanasius|Saint Athanasius Church in Bogomila|Црква Свети Атанасиј, Богомила|Church|parish
mk-oreshe-dormition|Dormition of the Most Holy Theotokos Church in Oreshe|Црква Успение на Пресвета Богородица, Ореше|Church|parish
mk-nezhilovo-stephen|Saint Stephen Church in Nezhilovo|Црква Свети Стефан, Нежилово|Church|parish
mk-teovo-athanasius|Saint Athanasius Church in Teovo|Црква Свети Атанасиј, Теово|Church|parish
mk-martolci-george|Saint George Church in Martolci|Црква Свети Ѓорѓи, Мартолци|Church|parish
mk-papradishte-peter-paul|Saints Peter and Paul Church in Papradishte|Црква Свети Петар и Павле, Папрадиште|Church|parish
mk-omorani-constantine-helen|Saints Constantine and Helen Church in Omorani|Црква Свети Константин и Елена, Оморани|Church|parish
mk-oraov-dol-savior|Holy Savior Church in Oraov Dol|Црква Свети Спас, Ораов Дол|Church|parish
mk-mokreni-nicholas|Saint Nicholas Church in Mokreni|Црква Свети Никола, Мокрени|Church|parish
mk-kapinovo-elijah|Saint Elijah Church in Kapinovo|Црква Свети Илија, Капиново|Church|parish
mk-bogomila-ascension-monastery|Ascension of Christ and Holy Savior Monastery in Bogomila|Манастир Вознесение Христово - Свети Спас, Богомила|Monastery|monastery
mk-oreshe-george-monastery|Saint George Monastery in Oreshe|Манастир Свети Ѓорѓи, Ореше|Monastery|monastery
mk-oreshe-john-monastery|Saint John Monastery in Oreshe|Манастир Свети Јован, Ореше|Monastery|monastery
mk-teovo-archangel-michael-monastery|Holy Archangel Michael Monastery in Teovo|Манастир Свети Архангел Михаил, Теово|Monastery|monastery
mk-mokreni-savior-monastery|Holy Savior Monastery in Mokreni|Манастир Свети Спас, Мокрени|Monastery|monastery
mk-sogle-nativity-theotokos-monastery|Nativity of the Most Holy Theotokos Monastery in Sogle|Манастир Рождество на Пресвета Богородица, Согле|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(380), POVARDARIE_VELES],
    )
    + table_rows(
        """
mk-chashka-clement-ohrid|Saint Clement of Ohrid Church in Chashka|Црква Свети Климент Охридски, Чашка|Church|parish
mk-drenovo-theotokos|Holy Theotokos Church in Drenovo|Црква Света Богородица, Дреново|Church|parish
mk-kriva-krusha-theotokos|Holy Theotokos Church in Kriva Krusha|Црква Света Богородица, Крива Круша|Church|parish
mk-rakovec-nicholas|Saint Nicholas Church in Rakovec|Црква Свети Никола, Раковец|Church|parish
mk-rlevci-ascension|Ascension of Christ Church in R'levci|Црква Вознесение Христово, Р'левци|Church|parish
mk-elovec-resurrection|Resurrection of Christ Church in Elovec|Црква Воскресение Христово, Еловец|Church|parish
mk-slp-elijah|Saint Elijah Church in S'lp|Црква Свети Илија, С'лп|Church|parish
mk-lisiche-elijah-monastery|Saint Elijah Monastery in Lisiche|Манастир Свети Илија, Лисиче|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(379), POVARDARIE_VELES],
    )
)


POVARDARIE_KAVADARCI_ROWS = (
    table_rows(
        """
mk-kavadarci-demetrius-cathedral|Saint Demetrius Cathedral in Kavadarci|Соборен храм Свети Димитриј, Кавадарци|Cathedral|parish
mk-kavadarci-petka|Saint Petka Church in Kavadarci|Црква Света Петка, Кавадарци|Church|parish
mk-negotino-athanasius|Saint Athanasius Church in Negotino|Црква Свети Атанасиј, Неготино|Church|parish
mk-negotino-george-monastery|Saint George Monastery in Negotino|Манастир Свети Ѓорѓи, Неготино|Monastery|monastery
""",
        "mk-povardarie", [POVARDARIE_KAVADARCI, povardarie_article(53)],
    )
    + table_rows(
        """
mk-vatasha-dormition|Dormition of the Most Holy Theotokos Church in Vatasha|Црква Успение на Пресвета Богородица, Ваташа|Church|parish
mk-kumanichevo-demetrius|Saint Demetrius Church in Kumanichevo|Црква Свети Димитриј, Куманичево|Church|parish
mk-mrezhichko-demetrius|Saint Demetrius Church in Mrezhichko|Црква Свети Димитриј, Мрежичко|Church|parish
mk-chemersko-savior|Holy Savior Church in Chemersko|Црква Свети Спас, Чемерско|Church|parish
mk-bohula-athanasius|Saint Athanasius Church in Bohula|Црква Свети Атанасиј, Бохула|Church|parish
mk-konopishte-stephen|Saint Stephen Church in Konopishte|Црква Свети Стефан, Конопиште|Church|parish
mk-grbavec-petka|Saint Petka Church in Grbavec|Црква Света Петка, Грбавец|Church|parish
mk-vatasha-moklishte-nicholas-monastery|Saint Nicholas at Moklishte Monastery in Vatasha|Манастир Свети Никола - Моклиште, Ваташа|Monastery|monastery
mk-boshava-archangel-michael-monastery|Holy Archangel Michael of Boshava Monastery|Манастир Свети Архангел Михаил - Бошавски, Бошава|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(170), POVARDARIE_KAVADARCI],
    )
    + table_rows(
        """
mk-marena-theotokos|Holy Theotokos Church in Marena|Црква Света Богородица, Марена|Church|parish
mk-begnishte-theotokos|Holy Theotokos Church in Begnishte|Црква Света Богородица, Бегниште|Church|parish
mk-brushani-trinity|Holy Trinity Church in Brushani|Црква Света Троица, Брушани|Church|parish
mk-vozarci-theotokos|Holy Theotokos Church in Vozarci|Црква Света Богородица, Возарци|Church|parish
mk-galishte-athanasius|Saint Athanasius Church in Galishte|Црква Свети Атанасиј, Галиште|Church|parish
mk-dobrotino-demetrius|Saint Demetrius Church in Dobrotino|Црква Свети Димитриј, Добротино|Church|parish
mk-kjesendre-demetrius|Saint Demetrius Church in Kjesendre|Црква Свети Димитриј, Ќесендре|Church|parish
mk-resava-archangel-michael|Holy Archangel Michael Church in Resava|Црква Свети Архангел Михаил, Ресава|Church|parish
mk-sopot-athanasius|Saint Athanasius Church in Sopot|Црква Свети Атанасиј, Сопот|Church|parish
mk-sheshkovo-theotokos|Holy Theotokos Church in Sheshkovo|Црква Света Богородица, Шешково|Church|parish
mk-shivec-stephen|Saint Stephen Church in Shivec|Црква Свети Стефан, Шивец|Church|parish
mk-palikura-nicholas|Saint Nicholas Church in Palikura|Црква Свети Никола, Паликура|Church|parish
mk-poloshki-george-monastery|Saint George Poloshki Monastery on Tikvesh Lake|Манастир Свети Ѓорѓи - Полошки, Праведник, Тиквешко Езеро|Monastery|monastery
""",
        "mk-povardarie", [povardarie_article(378), POVARDARIE_KAVADARCI],
    )
    + table_rows(
        """
mk-rosoman-trinity|Holy Trinity Church in Rosoman|Црква Света Троица, Росоман|Church|parish
mk-sirkovo-old-george|Old Saint George Church in Sirkovo|Стара црква Свети Ѓорѓи, Сирково|Church|parish
mk-sirkovo-new-george|New Saint George Church in Sirkovo|Нова црква Свети Ѓорѓи, Сирково|Church|parish
mk-farish-theotokos|Holy Theotokos Church in Farish|Црква Света Богородица, Фариш|Church|parish
""",
        "mk-povardarie", [povardarie_article(375), POVARDARIE_KAVADARCI],
    )
    + table_rows(
        """
mk-demir-kapija-dormition|Dormition of the Most Holy Theotokos Church in Demir Kapija|Црква Успение на Пресвета Богородица, Демир Капија|Church|parish
mk-przhdevo-athanasius|Saint Athanasius Church in Przhdevo|Црква Свети Атанасиј, Прждево|Church|parish
mk-bistrenici-petka|Saint Petka Church in Bistrenici|Црква Света Петка, Бистренци|Church|parish
mk-koreshnica-ascension|Ascension of Christ Church in Koreshnica|Црква Вознесение Христово, Корешница|Church|parish
mk-klisura-nicholas|Saint Nicholas Church in Klisura|Црква Свети Никола, Клисура|Church|parish
mk-chiflik-athanasius|Saint Athanasius Church in Chiflik|Црква Свети Атанасиј, Чифлик|Church|parish
mk-dren-nicholas|Saint Nicholas Church in Dren|Црква Свети Никола, Дрен|Church|parish
mk-koprishnica-george|Saint George Church in Koprishnica|Црква Свети Ѓорѓи, Копришница|Church|parish
mk-barovo-theotokos|Holy Theotokos Church in Barovo|Црква Света Богородица, Барово|Church|parish
mk-veshje-elijah|Saint Elijah Church in Veshje|Црква Свети Илија, Вешје|Church|parish
""",
        "mk-povardarie", [povardarie_article(376), POVARDARIE_KAVADARCI],
    )
    + table_rows(
        """
mk-timjanik-nativity-theotokos|Nativity of the Most Holy Theotokos Church in Timjanik|Црква Рождество на Пресвета Богородица, Тимјаник|Church|parish
mk-pepelishte-elijah|Saint Elijah Church in Pepelishte|Црква Свети Илија, Пепелиште|Church|parish
mk-krivolak-ascension|Ascension of Christ Church in Krivolak|Црква Вознесение Христово, Криволак|Church|parish
mk-dolni-disan-archangel-michael|Holy Archangel Michael Church in Dolni Disan|Црква Свети Архангел Михаил, Долни Дисан|Church|parish
mk-vojshanci-petka|Saint Petka Church in Vojshanci|Црква Света Петка, Војшанци|Church|parish
mk-tremnik-trinity|Holy Trinity Church in Tremnik|Црква Света Троица, Тремник|Church|parish
mk-gorni-disan-jeremiah|Prophet Jeremiah Church in Gorni Disan|Црква Свети Еремија, Горни Дисан|Church|parish
""",
        "mk-povardarie", [povardarie_article(377), POVARDARIE_KAVADARCI],
    )
)


ROWS = {
    "macedonia": (
        NEW_EPARCHY_ROWS + DELCHEVO_ROWS + KRUSHDEM_PARISH_ROWS
        + KRUSHDEM_CHURCH_ROWS + KRUSHDEM_MONASTERY_ROWS
    ),
    "mk-bregalnica": (
        BREGALNICA_ROWS + BREGALNICA_ACTIVE_MONASTERY_ROWS
        + BREGALNICA_NEWS_MONASTERY_ROWS
    ),
    "mk-debar-kicevo": DKE_TEMPLE_ROWS + DKE_MONASTERY_ROWS,
    "mk-kumanovo-osogovo": KOE_ROWS,
    "mk-povardarie": (
        POVARDARIE_HIERARCHY_ROWS + POVARDARIE_GEVGELIJA_ROWS
        + POVARDARIE_VELES_ROWS + POVARDARIE_KAVADARCI_ROWS
        + POVARDARIE_ACTIVE_MONASTERY_ROWS
    ),
    "mk-prespa-pelagonia": (
        PRESPA_ROWS + PRESPA_ACTIVE_MONASTERY_ROWS
        + PRESPA_NEWS_MONASTERY_ROWS
    ),
    "mk-skopje": SKOPJE_CHURCH_ROWS + SKOPJE_MONASTERY_ROWS,
    "mk-strumica": STRUMICA_ROWS,
    "mk-tetovo-gostivar": TGE_ROWS + TGE_ACTIVE_MONASTERY_ROWS,
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "macedonia": 109,
    "mk-bregalnica": 32,
    "mk-debar-kicevo": 38,
    "mk-kumanovo-osogovo": 30,
    "mk-povardarie": 154,
    "mk-prespa-pelagonia": 13,
    "mk-skopje": 112,
    "mk-strumica": 6,
    "mk-tetovo-gostivar": 7,
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
            if item.get("kind") not in {"diocese", "parish", "monastery"}:
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
            "country": "MK",
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("North Macedonia counts changed: %r" % counts)
    if set(ENGLISH_NAMES) != {
            item["id"] for payload in payloads.values()
            for item in payload["rows"]}:
        raise ValueError("English name coverage changed")
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
        print("directory North Macedonia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    total = sum(len(payload["rows"]) for payload in payloads.values())
    print("North Macedonia: %d verified bodies across %d canonical parents" %
          (total, len(payloads)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
