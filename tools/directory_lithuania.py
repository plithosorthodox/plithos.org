#!/usr/bin/env python3
"""The parish-scale Lithuania branches of the Churches directory.

The Patriarchal Exarchate publishes its worshipping communities through its
service finder. The Lithuanian Orthodox Archdiocese publishes the churches
and monasteries served by its clergy through its official clergy register.

    python tools/directory_lithuania.py --check
    python tools/directory_lithuania.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-14"
EP_SERVICES = "https://www.obl.lt/en-gb/pamaldu-paieska"
EP_PARISHES = "https://www.obl.lt/en-gb/parapijos"
MP_CLERGY = "https://www.orthodoxy.lt/duxovenstvo"
MP_COMMUNITIES = (
    "https://www.orthodoxy.lt/novosti/"
    "jau-36-lietuvos-staciatikiu-baznycios-bendruomenes-kreipesi-i-seima"
)
MP_HOLY_SPIRIT = (
    "https://www.orthodoxy.lt/lt/vilniaus-sv-dvasios-vienuolynas"
)
MP_MAGDALENE = (
    "https://www.orthodoxy.lt/lt/marijos-magdalietes-vienuolynas"
)


EP_ROWS = [
    dict(id="lt-ep-vilnius-andrew-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of the Holy Apostle Andrew in Vilnius",
         local="Vilniaus Šv. apaštalo Andriejaus parapija", country="LT",
         dedication="Šv. apaštalas Andriejus",
         address=["Antakalnio g. 10", "Vilnius"],
         services=[
             "Pirmadieniais-ketvirtadieniais 18:00 - Dieviškoji Liturgija ukrainiečių kalba.",
             "Penktadieniais 18:30 - Dieviškoji Liturgija graikų kalba.",
             "Šeštadieniais ir sekmadieniais 9:00 - Dieviškoji Liturgija ukrainiečių kalba.",
         ],
         languages=["ukrainiečių", "graikų"],
         sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-vilnius-trinity-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of the Holy Trinity in Vilnius",
         local="Vilniaus Švč. Trejybės parapija", country="LT",
         dedication="Švč. Trejybė", address=["Verkių g. 70", "Vilnius"],
         site="https://www.trejybe.lt/",
         services=[
             "8:40 - liturginės valandos, išpažintis.",
             "9:00 - Dieviškoji Liturgija lietuvių kalba.",
         ],
         languages=["lietuvių"], sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-vilnius-nicholas-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of Saint Nicholas in Vilnius",
         local="Vilniaus Šv. Mikalojaus parapija", country="LT",
         dedication="Šv. Mikalojus", address=["Lukiškių skg. 6", "Vilnius"],
         services=[
             "9:00 - Dieviškoji Liturgija bažnytine slavų kalba.",
         ],
         languages=["bažnytinė slavų"],
         sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-vilnius-annunciation-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of the Annunciation of the Mother of God in Vilnius",
         local="Vilniaus Švč. Dievo Gimdytojos Apreiškimo parapija",
         country="LT", dedication="Švč. Dievo Gimdytojos Apreiškimas",
         address=["Bokšto g. 4", "Vilnius"],
         services=[
             "9:00 - Dieviškoji Liturgija bažnytine slavų kalba.",
             "10:30 - Dieviškoji Liturgija baltarusių kalba.",
         ],
         languages=["bažnytinė slavų", "baltarusių"],
         sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-kaunas-resurrection-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of the Resurrection of Christ in Kaunas",
         local="Kauno Kristaus Prisikėlimo parapija", country="LT",
         dedication="Kristaus Prisikėlimas",
         address=["Aukštaičių g. 6", "Kaunas"],
         services=[
             "10:00 - Dieviškoji Liturgija ukrainiečių kalba.",
             "12:30 - Dieviškoji Liturgija lietuvių kalba.",
         ],
         languages=["ukrainiečių", "lietuvių"],
         sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-klaipeda-george-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of Saint George in Klaipėda",
         local="Klaipėdos Šv. Jurgio parapija", country="LT",
         dedication="Šv. Jurgis", address=["Herkaus Manto g. 84", "Klaipėda"],
         services=[
             "10:00 - Dieviškoji Liturgija bažnytine slavų kalba.",
         ],
         languages=["bažnytinė slavų"],
         sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-siauliai-george-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of Saint George in Šiauliai",
         local="Šiaulių Šv. Jurgio parapija", country="LT",
         dedication="Šv. Jurgis", address=["Kražių g. 17", "Šiauliai"],
         services=[
             "Kiekvieną pirmą mėnesio šeštadienį: 11:30 - Dieviškoji Liturgija ukrainiečių kalba.",
         ],
         languages=["ukrainiečių"], sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-alytus-bruno-chapel", parent="ep-lithuania",
         kind="parish", rank="Chapel",
         name="Chapel of Saint Bruno of Querfurt in Alytus",
         local="Šv. Brunono Kverfurtiečio koplyčia", country="LT",
         dedication="Šv. Brunonas Kverfurtietis",
         address=["Kalnėnų g. 2A", "Alytus"],
         services=[
             "Kiekvieną trečią mėnesio šeštadienį: 11:30 - Dieviškoji Liturgija ukrainiečių kalba.",
         ],
         languages=["ukrainiečių"], sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-taurage-nativity-parish", parent="ep-lithuania",
         kind="parish", rank="Parish",
         name="Parish of the Nativity of Christ in Tauragė",
         local="Tauragės Kristaus Gimimo parapija", country="LT",
         dedication="Kristaus Gimimas", address=["Gintaro g. 32", "Tauragė"],
         services=[
             "Šeštadieniais, bet ne kiekvieną savaitę, 10:00 - Dieviškoji Liturgija bažnytine slavų kalba.",
         ],
         languages=["bažnytinė slavų"],
         sources=[EP_PARISHES, EP_SERVICES]),
    dict(id="lt-ep-anyksciai-mission", parent="ep-lithuania",
         kind="parish", rank="Mission",
         name="Orthodox Worshipping Community in Anykščiai",
         local="Ortodoksų pamaldos Anykščiuose", country="LT",
         address=[
             "A. Baranausko ir A. Vienuolio-Žukausko memorialinio muziejaus patalpos",
             "A. Vienuolio g. 2",
             "Anykščiai",
         ],
         services=[
             "Pamaldos: šiuo metu pamaldos ukrainiečių kalba vyksta tik didžiųjų švenčių metu.",
         ],
         languages=["ukrainiečių"], sources=[EP_PARISHES]),
]


MP_PARISHES = [
    ("lt-mp-vilnius-dormition-cathedral",
     "Cathedral Parish of the Dormition of the Mother of God in Vilnius",
     "Пречистенский кафедральный собор, г. Вильнюс",
     "Успение Пресвятой Богородицы"),
    ("lt-mp-vilnius-paraskeva-parish",
     "Parish of Saint Paraskeva in Vilnius",
     "Пятницкий храм, г. Вильнюс", "святая Параскева Пятница"),
    ("lt-mp-trakai-nativity-theotokos-parish",
     "Parish of the Nativity of the Mother of God in Trakai",
     "храм Рождества Богородицы, г. Тракай", "Рождество Богородицы"),
    ("lt-mp-semeliskes-nicholas-parish",
     "Parish of Saint Nicholas in Semeliškės",
     "Свято-Никольский храм, дер. Семелишкес Электренского р-на",
     "святитель Николай"),
    ("lt-mp-vievis-dormition-parish",
     "Parish of the Dormition of the Mother of God in Vievis",
     "Успенский храм, г. Вевис", "Успение Божией Матери"),
    ("lt-mp-palanga-iveron-parish",
     "Parish of the Iveron Icon of the Mother of God in Palanga",
     "Иверский храм, г. Паланга", "Иверская икона Божией Матери"),
    ("lt-mp-kaunatava-sorrowful-icon-parish",
     "Parish of the Joy of All Who Sorrow Icon in Kaunatava",
     "Скорбященский храм, с. Каунатава",
     "икона Божией Матери «Всех скорбящих Радость»"),
    ("lt-mp-vieksniai-sergius-parish",
     "Parish of Saint Sergius of Radonezh in Viekšniai",
     "храм в честь прп. Сергия Радонежского, с. Векшняй",
     "прп. Сергий Радонежский"),
    ("lt-mp-vilnius-nicholas-parish",
     "Parish of Saint Nicholas in Vilnius",
     "храм в честь Перенесения мощей святителя Николая Чудотворца, г. Вильнюс",
     "Перенесение мощей святителя Николая Чудотворца"),
    ("lt-mp-vilnius-sign-icon-parish",
     "Parish of the Sign Icon of the Mother of God in Vilnius",
     "храм в честь иконы Божией Матери «Знамение», г. Вильнюс",
     "икона Божией Матери «Знамение»"),
    ("lt-mp-druskininkai-sorrowful-icon-parish",
     "Parish of the Joy of All Who Sorrow Icon in Druskininkai",
     "Скорбященский храм, г. Друскининкай",
     "икона Божией Матери «Всех скорбящих Радость»"),
    ("lt-mp-alytus-protection-parish",
     "Parish of the Protection of the Mother of God in Alytus",
     "Покровский приход, г. Алитус", "Покров Пресвятой Богородицы"),
    ("lt-mp-vilnius-euphrosyne-parish",
     "Parish of Saint Euphrosyne of Polotsk in Vilnius",
     "храм во имя преподобной Евфросинии Полоцкой, г. Вильнюс",
     "преподобная Евфросиния Полоцкая"),
    ("lt-mp-mikniskes-sorrowful-icon-parish",
     "Parish of the Joy of All Who Sorrow Icon in Mikniškės",
     "Скорбященский храм, дер. Микнишкес (Михново) Шальчининского р-на",
     "икона Божией Матери «Всех скорбящих Радость»"),
    ("lt-mp-siauliai-peter-paul-parish",
     "Parish of the Holy Apostles Peter and Paul in Šiauliai",
     "храм в честь святых первоверховных апостолов Петра и Павла, г. Шауляй",
     "святые первоверховные апостолы Петр и Павел"),
    ("lt-mp-tytuvenai-kazan-icon-parish",
     "Parish of the Kazan Icon of the Mother of God in Tytuvėnai",
     "храм в честь иконы Божией матери «Казанская», г. Титувенай",
     "икона Божией Матери «Казанская»"),
    ("lt-mp-taurage-vilnius-martyrs-parish",
     "Parish of the Vilnius Martyrs in Tauragė",
     "храм Виленских мчч., г. Таураге", "Виленские мученики"),
    ("lt-mp-kaunas-annunciation-cathedral",
     "Cathedral Parish of the Annunciation of the Mother of God in Kaunas",
     "собор в честь Благовещения Пресвятой Богородицы, г. Каунас",
     "Благовещение Пресвятой Богородицы"),
    ("lt-mp-kedainiai-transfiguration-parish",
     "Parish of the Transfiguration of the Lord in Kėdainiai",
     "храм в честь Преображения Господня, г. Кедайняй",
     "Преображение Господне"),
    ("lt-mp-raseiniai-trinity-parish",
     "Parish of the Life-Giving Trinity in Raseiniai",
     "храм во Имя Животворящей Троицы, г. Расейняй",
     "Животворящая Троица"),
    ("lt-mp-uzusaliai-alexander-nevsky-parish",
     "Parish of Saint Alexander Nevsky in Užusaliai",
     "храм во имя святого благоверного князя Александра Невского, с. Ужусаляй",
     "святой благоверный князь Александр Невский"),
    ("lt-mp-ukmerge-resurrection-parish",
     "Parish of the Resurrection of Christ in Ukmergė",
     "храм Воскресения Христова, г. Укмерге", "Воскресение Христово"),
    ("lt-mp-jonava-resurrection-parish",
     "Parish of the Resurrection of Christ in Jonava",
     "храм Воскресения Христова, г. Йонава", "Воскресение Христово"),
    ("lt-mp-vilnius-peter-paul-parish",
     "Parish of the Holy Apostles Peter and Paul in Vilnius",
     "Петропавловский храм, г. Вильнюс",
     "святые первоверховные апостолы Петр и Павел"),
    ("lt-mp-vilnius-archangel-michael-parish",
     "Parish of the Archangel Michael in Vilnius",
     "Михайловский храм, г. Вильнюс", "Архангел Михаил"),
    ("lt-mp-inturke-protection-parish",
     "Parish of the Protection of the Mother of God in Inturkė",
     "Покровский храм, дер. Интуркес Молетского р-на",
     "Покров Пресвятой Богородицы"),
    ("lt-mp-vilnius-constantine-michael-parish",
     "Parish of Saints Constantine and Michael in Vilnius",
     "Константино-Михайловский храм, г. Вильнюс",
     "святые Константин и Михаил"),
    ("lt-mp-bukiskis-nativity-parish",
     "Parish of the Nativity of Christ in Bukiškis",
     "храм Рождества Христова, д. Букишкис", "Рождество Христово"),
    ("lt-mp-visaginas-presentation-panteleimon-parish",
     "Parish of the Presentation of the Mother of God and Saint Panteleimon in Visaginas",
     "Введено-Пантелеимоновский храм, г. Висагинас",
     "Введение во храм Пресвятой Богородицы и святой Пантелеимон"),
    ("lt-mp-vilnius-catherine-parish",
     "Parish of Saint Catherine in Vilnius",
     "Екатерининский храм, г. Вильнюс", "святая Екатерина"),
    ("lt-mp-raguva-nativity-theotokos-parish",
     "Parish of the Nativity of the Mother of God in Raguva",
     "храм Рождества Богородицы, г. Рагува Паневежского р-на",
     "Рождество Богородицы"),
    ("lt-mp-rudamina-nicholas-parish",
     "Parish of Saint Nicholas in Rudamina",
     "Никольский храм, г. Рудамина Вильнюсского р-на",
     "святитель Николай"),
    ("lt-mp-pabrade-sergius-parish",
     "Parish of Saint Sergius of Radonezh in Pabradė",
     "храм прп. Сергия Радонежского, г. Пабраде",
     "прп. Сергий Радонежский"),
    ("lt-mp-klaipeda-faith-hope-love-sophia-parish",
     "Parish of the Martyrs Faith, Hope, Love, and Sophia in Klaipėda",
     "храм свв. мцц. Веры, Надежды, Любови и матери их Софии, г. Клайпеда",
     "святые мученицы Вера, Надежда, Любовь и матерь их София"),
    ("lt-mp-marijampole-trinity-parish",
     "Parish of the Holy Trinity in Marijampolė",
     "храм в честь Святой Троицы, г. Мариямполе", "Святая Троица"),
    ("lt-mp-kybartai-alexander-nevsky-parish",
     "Parish of Saint Alexander Nevsky in Kybartai",
     "храм во имя святого благоверного князя Александра Невского, г. Кибартай",
     "святой благоверный князь Александр Невский"),
    ("lt-mp-kruonis-protection-parish",
     "Parish of the Protection of the Mother of God in Kruonis",
     "храм в честь Покрова Пресвятой Богородицы, г. Круонис",
     "Покров Пресвятой Богородицы"),
    ("lt-mp-klaipeda-all-russian-saints-parish",
     "Parish of All Saints Who Shone Forth in the Russian Land in Klaipėda",
     "храм Всех святых, в земле Русской просиявших, г. Клайпеда",
     "Все святые, в земле Русской просиявшие"),
    ("lt-mp-telsiai-nicholas-parish",
     "Parish of Saint Nicholas in Telšiai",
     "Никольский храм, г. Тельшяй", "святитель Николай"),
    ("lt-mp-kolainiai-dormition-parish",
     "Parish of the Dormition of the Mother of God in Kolainiai",
     "храм в честь Успения Божией Матери, г. Колайняй",
     "Успение Божией Матери"),
    ("lt-mp-klaipeda-protection-nicholas-parish",
     "Parish of the Protection of the Mother of God and Saint Nicholas in Klaipėda",
     "Покрово-Никольский храм, г. Клайпеда",
     "Покров Пресвятой Богородицы и святитель Николай"),
    ("lt-mp-salcininkai-tikhon-parish",
     "Parish of Saint Tikhon in Šalčininkai",
     "храм свт. Тихона, г. Шальчининкай", "святитель Тихон"),
    ("lt-mp-panevezys-resurrection-parish",
     "Parish of the Resurrection of the Lord in Panevėžys",
     "храм в честь Воскресения Господня, г. Паневежис",
     "Воскресение Господне"),
    ("lt-mp-gegabrasta-nicholas-parish",
     "Parish of Saint Nicholas in Gegabrasta",
     "Никольский храм дер. Гегабраста Пасвальского р-на",
     "святитель Николай"),
    ("lt-mp-lebeniskiai-nicander-parish",
     "Parish of Saint Nicander in Lebeniškiai",
     "Никандровский храм дер. Лебенишкес Биржайского р-на",
     "святой Никандр"),
    ("lt-mp-anyksciai-alexander-nevsky-parish",
     "Parish of Saint Alexander Nevsky in Anykščiai",
     "храм св. Александра Невского, г. Аникщяй",
     "святой Александр Невский"),
    ("lt-mp-rokiskis-alexander-nevsky-parish",
     "Parish of Saint Alexander Nevsky in Rokiškis",
     "храм Александра Невского, г. Рокишкис", "Александр Невский"),
    ("lt-mp-zarasai-all-saints-parish",
     "Parish of All Saints in Zarasai",
     "Всехсвятский храм, г. Зарасай", "Все святые"),
    ("lt-mp-visaginas-john-baptist-parish",
     "Parish of the Nativity of Saint John the Baptist in Visaginas",
     "храм Рождества Иоанна Крестителя, г. Висагинас",
     "Рождество Иоанна Крестителя"),
    ("lt-mp-mazeikiai-dormition-parish",
     "Parish of the Dormition of the Mother of God in Mažeikiai",
     "Успенский храм, г. Мажейкяй", "Успение Божией Матери"),
    ("lt-mp-geisiskes-george-parish",
     "Parish of Saint George in Geisiškės",
     "Георгиевский храм дер. Гейсишкес Вильнюсского р-на",
     "святой Георгий"),
    ("lt-mp-utena-ascension-parish",
     "Parish of the Ascension of the Lord in Utena",
     "Вознесенский храм, г. Утена", "Вознесение Господне"),
    ("lt-mp-uzpaliai-nicholas-parish",
     "Parish of Saint Nicholas in Užpaliai",
     "Никольский храм, г. Ужпаляй", "святитель Николай"),
    ("lt-mp-svencionys-trinity-parish",
     "Parish of the Holy Trinity in Švenčionys",
     "Свято-Троицкий храм, г. Швенченис", "Святая Троица"),
]


MP_CONFIRMED_PARISH_IDS = {
    "lt-mp-vilnius-dormition-cathedral",
    "lt-mp-vilnius-paraskeva-parish",
    "lt-mp-vilnius-nicholas-parish",
    "lt-mp-vilnius-sign-icon-parish",
    "lt-mp-vilnius-archangel-michael-parish",
    "lt-mp-vilnius-constantine-michael-parish",
    "lt-mp-vilnius-catherine-parish",
    "lt-mp-vilnius-euphrosyne-parish",
    "lt-mp-vilnius-peter-paul-parish",
    "lt-mp-trakai-nativity-theotokos-parish",
    "lt-mp-pabrade-sergius-parish",
    "lt-mp-palanga-iveron-parish",
    "lt-mp-taurage-vilnius-martyrs-parish",
    "lt-mp-bukiskis-nativity-parish",
    "lt-mp-vievis-dormition-parish",
    "lt-mp-rudamina-nicholas-parish",
    "lt-mp-mikniskes-sorrowful-icon-parish",
    "lt-mp-salcininkai-tikhon-parish",
    "lt-mp-kaunas-annunciation-cathedral",
    "lt-mp-kedainiai-transfiguration-parish",
    "lt-mp-siauliai-peter-paul-parish",
    "lt-mp-ukmerge-resurrection-parish",
    "lt-mp-marijampole-trinity-parish",
    "lt-mp-mazeikiai-dormition-parish",
    "lt-mp-utena-ascension-parish",
    "lt-mp-panevezys-resurrection-parish",
    "lt-mp-anyksciai-alexander-nevsky-parish",
    "lt-mp-rokiskis-alexander-nevsky-parish",
    "lt-mp-svencionys-trinity-parish",
    "lt-mp-klaipeda-all-russian-saints-parish",
    "lt-mp-klaipeda-protection-nicholas-parish",
    "lt-mp-klaipeda-faith-hope-love-sophia-parish",
    "lt-mp-visaginas-presentation-panteleimon-parish",
    "lt-mp-visaginas-john-baptist-parish",
}


def mp_rows():
    rows = []
    for work_id, name, local, dedication in MP_PARISHES:
        sources = [MP_CLERGY]
        if work_id in MP_CONFIRMED_PARISH_IDS:
            sources.append(MP_COMMUNITIES)
        rows.append(dict(
            id=work_id, parent="ru-vilnius", kind="parish",
            rank=("Parish" if work_id in MP_CONFIRMED_PARISH_IDS
                  else "Church"),
            name=name, local=local, dedication=dedication, country="LT",
            sources=sources,
        ))
    rows.extend([
        dict(id="lt-mp-vilnius-holy-spirit-monastery",
             parent="ru-vilnius", kind="monastery", rank="Monastery",
             name="Holy Spirit Monastery in Vilnius",
             local="Свято-Духов мужской монастырь, г. Вильнюс",
             dedication="Сошествие Святого Духа на апостолов", country="LT",
             sources=[MP_CLERGY, MP_HOLY_SPIRIT, MP_COMMUNITIES]),
        dict(id="lt-mp-vilnius-mary-magdalene-monastery",
             parent="ru-vilnius", kind="monastery", rank="Monastery",
             name="Saint Mary Magdalene Convent in Vilnius",
             local="Марие-Магдалининский женский монастырь, г. Вильнюс",
             dedication="святая равноапостольная Мария Магдалина",
             country="LT",
             sources=[MP_CLERGY, MP_MAGDALENE, MP_COMMUNITIES]),
    ])
    return rows


ROWS = {
    "ep-lithuania": EP_ROWS,
    "ru-vilnius": mp_rows(),
}


def clean(row):
    out = {key: value for key, value in row.items()
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
    if out.get("languages") and (not isinstance(out["languages"], list) or
                                 not all(isinstance(word, str)
                                         for word in out["languages"])):
        raise ValueError("%s has invalid worship languages" % out.get("id"))
    if out.get("services") and (not isinstance(out["services"], list) or
                                not all(isinstance(line, str)
                                        for line in out["services"])):
        raise ValueError("%s has invalid service times" % out.get("id"))
    if out.get("founded") and (not isinstance(out["founded"], list) or
                               not all(isinstance(line, str)
                                       for line in out["founded"])):
        raise ValueError("%s has invalid history text" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"parish", "monastery"}
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            row = clean(source)
            work_id = row.get("id")
            if not work_id or work_id in seen:
                raise ValueError("duplicate or missing id: %s" % work_id)
            if row.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (work_id, row.get("parent")))
            if row.get("kind") not in allowed_kinds:
                raise ValueError("%s has unsupported kind: %s" %
                                 (work_id, row.get("kind")))
            if row.get("kind") == "parish" and not row.get("local"):
                raise ValueError("%s is a parish without its own name" % work_id)
            if row.get("country") != "LT":
                raise ValueError("%s is outside Lithuania" % work_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a name" % work_id)
            if row.get("site") and not row["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % work_id)
            seen.add(work_id)
            branch_seen.add(work_id)
            rows.append(row)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "LT",
            "rows": rows,
        }
    if len(payloads["ep-lithuania"]["rows"]) != 10:
        raise ValueError("Lithuanian Exarchate must publish exactly 10 rows")
    if len(payloads["ru-vilnius"]["rows"]) != 56:
        raise ValueError("Vilnius Diocese must publish exactly 56 rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
        }
        for parent, payload in sorted(payloads.items())
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    expected = set()
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        expected.add(path.name)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    if OUT.exists():
        for path in OUT.glob("*lithuania*.v1.json"):
            if path.name not in expected:
                errors.append("unexpected %s" % path.relative_to(ROOT))
        for path in OUT.glob("ru-vilnius*.v1.json"):
            if path.name not in expected:
                errors.append("unexpected %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Lithuania: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Lithuania branches: 2 parents, 42 parishes, 20 churches, "
          "1 chapel, 1 mission, 2 monasteries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
