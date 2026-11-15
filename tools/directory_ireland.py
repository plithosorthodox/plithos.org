#!/usr/bin/env python3
"""Directory rows for the Republic of Ireland and Northern Ireland.

The rows are grouped by the parent IDs already used by the directory spine.
Several of those parents also cover Great Britain, Iceland or continental
Europe, so this module deliberately does not write branch payload files. Its
validated payloads are intended to be merged with the other country modules
before publication.

    python tools/directory_ireland.py --check
    python tools/directory_ireland.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-14"
EP_IRELAND = "https://ec-patr.org/entities/iera-mitropolis-irlandias/"
EP_THYATEIRA = (
    "https://ec-patr.org/entities/"
    "iera-arxiepiskopi-thyateiron-megalis-vretanias/"
)
ANTIOCH = "https://www.antiochian-orthodox.com/parish-directory"
SOUROZH = "https://www.sourozh.org/parishes-eng"
ROCOR = (
    "https://orthodox-europe.org/wp-content/uploads/2025/12/"
    "2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf"
)
SERBIAN_DIOCESE = "https://eparhija.uk/en/diocese/"
SERBIAN_PARISHES = "https://eparhija.uk/parohije/"
SERBIAN_CORK = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/16282."
    "republika-irska-episkop-nektarije-posetio-kork-i-dablin.html"
)
ROMANIAN_IRELAND = "https://www.eorii.com/?p=parohii"
ROMANIAN_MONASTERY = "https://eorii.com/mitropolitul-bartolomeu-anania?p=manastiri"
ROMANIAN_NI = "https://roarch.org.uk/ro/parohii-in-irlanda-de-nord/"
UOC_CENTRAL = "https://vzcz.church.ua/2023/07/17/pershij-rik-prisutnosti-upc-v-irlandiji/"
UOC_DUBLIN = "https://www.uocdublin.org/nasha-parafiya"
UOC_LETTERKENNY = (
    "https://news.church.ua/2023/11/22/"
    "v-irlandskomu-misti-letterkenni-vidznachili-pershe-prestolne-svyato/"
)


def row(row_id, parent, name, local, country, address, sources,
        rank="Parish", kind="parish", site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": country,
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


ROWS = {
    "ep-ireland": [
        row(
            "ie-ep-dublin-annunciation-cathedral", "ep-ireland",
            "Orthodox Cathedral of the Annunciation of the Theotokos",
            "Ιερός Καθεδρικός Ναός Ευαγγελισμού της Θεοτόκου", "IE",
            ["46 Arbour Hill", "Dublin 7", "D07 C958"],
            [EP_IRELAND], rank="Cathedral Parish",
            site="https://orthodoxireland.ie/",
        ),
        row(
            "ie-ep-cork-saint-nicholas", "ep-ireland",
            "Orthodox Parish and Community of Saint Nicholas",
            "Ορθόδοξος Ενορία και Κοινότης Αγίου Νικολάου", "IE", [],
            [EP_IRELAND],
        ),
        row(
            "ie-ep-dublin-ukrainian-protection", "ep-ireland",
            "Ukrainian Orthodox Parish of the Protection of the Most Holy Theotokos in Dublin",
            "Українська православна парафія в Дубліні на честь Покрова Пресвятої Богородиці",
            "IE",
            ["St John the Baptist Church of Ireland", "Church Avenue",
             "Grace Park Road", "Drumcondra, Dublin 9", "D09 VE04"],
            [EP_IRELAND, "https://uop.ie/about-us/", "https://uop.ie/contact/"],
            site="https://uop.ie/",
        ),
    ],
    "ep-thyateira": [
        row(
            "gb-ni-ep-belfast-community", "ep-thyateira",
            "Greek Orthodox Community of Belfast",
            "Ελληνορθόδοξος Κοινότης Belfast", "GB", [],
            [EP_THYATEIRA], rank="Community",
        ),
    ],
    "an-british-isles": [
        row(
            "gb-ni-antioch-belfast-saint-ignatius", "an-british-isles",
            "Saint Ignatius of Antioch Orthodox Church",
            "Saint Ignatius of Antioch Orthodox Church", "GB",
            ["Cullen Memorial Hall", "Donegall Road Methodist Church",
             "381 Donegall Road", "Belfast", "BT12 6GR"],
            [ANTIOCH], site="https://saintignatiusbelfast.org/",
        ),
        row(
            "ie-antioch-dublin-three-patrons", "an-british-isles",
            "Three Patrons of Ireland Orthodox Church",
            "Three Patrons of Ireland Orthodox Church", "IE",
            ["7 Grange Terrace", "Deansgrange, Blackrock", "Dublin"],
            [ANTIOCH],
        ),
    ],
    "ru-sourozh": [
        row(
            "gb-ni-sourozh-belfast-saint-finnian", "ru-sourozh",
            "Parish of Saint Finnian of Clonard",
            "Parish of Saint Finnian of Clonard", "GB",
            ["St George Church", "105 High Street", "Belfast", "BT1 2AG"],
            [SOUROZH],
        ),
        row(
            "gb-ni-sourozh-newry-community", "ru-sourozh",
            "Newry Diocesan Community", "Newry Diocesan Community", "GB",
            ["Hall for All", "33 Downshire Road", "Newry", "BT34 1EE"],
            [SOUROZH], rank="Diocesan Community",
        ),
        row(
            "ie-sourozh-athlone-holy-theophany", "ru-sourozh",
            "Parish of Holy Theophany", "Parish of Holy Theophany", "IE",
            ["Drum Community Centre", "Summerhill, Crannagh",
             "Athlone, County Roscommon", "N37 T298"], [SOUROZH],
        ),
        row(
            "ie-sourozh-castlebar-saint-tikhon", "ru-sourozh",
            "Diocesan Community of Saint Tikhon, Patriarch of Moscow and All Russia",
            "Diocesan Community of Saint Tikhon, Patriarch of Moscow and All Russia",
            "IE", ["The Monastery", "3 Upper Chapel Street, Garryduff",
                   "Castlebar", "F23 D295"], [SOUROZH],
            rank="Diocesan Community",
        ),
        row(
            "ie-sourozh-cork-holy-trinity", "ru-sourozh",
            "Parish of the Holy Trinity and Pentecost",
            "Parish of the Holy Trinity and Pentecost", "IE",
            ["St Peter's Church of Ireland", "Church Hill, Carrigrohane",
             "Cork", "T12 TX89"], [SOUROZH],
        ),
        row(
            "ie-sourozh-drogheda-entry-theotokos", "ru-sourozh",
            "Parish of the Entrance into the Temple of the Most Holy Theotokos",
            "Parish of the Entrance into the Temple of the Most Holy Theotokos",
            "IE", ["St Peter's Church of Ireland", "Peter's Hill",
                   "Drogheda, County Louth"], [SOUROZH],
        ),
        row(
            "ie-sourozh-galway-saint-nicholas", "ru-sourozh",
            "Parish of Saint Nicholas the Wonderworker",
            "Parish of Saint Nicholas the Wonderworker", "IE",
            ["Ballinfoyle Castlegar Neighbourhood Centre", "Galway",
             "H91 PN50"], [SOUROZH],
        ),
        row(
            "ie-sourozh-letterkenny-kazan-icon", "ru-sourozh",
            "Diocesan Community of the Kazan Icon of the Mother of God",
            "Diocesan Community of the Kazan Icon of the Mother of God", "IE",
            ["IOSAS Centre", "Derryvane, Muff", "County Donegal"], [SOUROZH],
            rank="Diocesan Community",
        ),
        row(
            "ie-sourozh-limerick-saint-john", "ru-sourozh",
            "Parish of Saint John the Theologian",
            "Parish of Saint John the Theologian", "IE",
            ["Unit E, The Gables", "Ballysimon Road, Spital-Land",
             "Limerick", "V94 NW82"], [SOUROZH],
        ),
        row(
            "ie-sourozh-navan-dormition", "ru-sourozh",
            "Diocesan Community of the Dormition of the Mother of God",
            "Diocesan Community of the Dormition of the Mother of God", "IE",
            ["St Mary's Church", "Church Hill, Townparks",
             "Navan, County Meath", "C15 K662"], [SOUROZH],
            rank="Diocesan Community",
        ),
        row(
            "ie-sourozh-sligo-saint-attracta", "ru-sourozh",
            "Diocesan Community of Saint Attracta",
            "Diocesan Community of Saint Attracta", "IE",
            ["St Anne's Church", "Cranmore Road", "Sligo", "F91 C3YT"],
            [SOUROZH], rank="Diocesan Community",
        ),
        row(
            "ie-sourozh-tralee-saint-brendan", "ru-sourozh",
            "Diocesan Community of Saint Brendan the Navigator",
            "Diocesan Community of Saint Brendan the Navigator", "IE",
            ["Church of the Immaculate Conception", "Rathass", "Tralee",
             "V92 DX62"], [SOUROZH], rank="Diocesan Community",
        ),
        row(
            "ie-sourozh-waterford-saint-patrick", "ru-sourozh",
            "Parish of Saint Patrick of Ireland",
            "Parish of Saint Patrick of Ireland", "IE",
            ["Manor Saint John Centre", "Saint Paul's Boxing Club, first floor",
             "Lisduggan", "Waterford", "X91 XW80"], [SOUROZH],
        ),
        row(
            "ie-sourozh-wexford-community", "ru-sourozh",
            "Wexford Diocesan Community", "Wexford Diocesan Community", "IE",
            ["Church of the Immaculate Conception",
             "Rowe Street Upper, Townparks", "Wexford", "Y35 KX66"],
            [SOUROZH], rank="Diocesan Community",
        ),
    ],
    "russia": [
        row(
            "ie-russia-dublin-peter-paul-metochion", "russia",
            "Holy Apostles Peter and Paul Patriarchal Metochion in Dublin",
            "Храм святых апостолов Петра и Павла в Дублине, Патриаршее подворье",
            "IE", ["Harold's Cross Road", "Dublin", "D6W WA48"],
            [SOUROZH,
             "https://www.sourozh.org/maineng/2019/2/21/on-the-sunday-of-the-publican-and-the-pharisee-his-grace-bis.html",
             "https://stpeterstpaul.net/"],
            rank="Patriarchal Metochion", site="https://stpeterstpaul.net/",
        ),
    ],
    "ru-great-britain-and-western-europe-rocor": [
        row(
            "ie-rocor-stradbally-saint-colman", "ru-great-britain-and-western-europe-rocor",
            "Saint Colman's Orthodox Church",
            "Храм св. Колмана Огавалъского", "IE",
            ["The Abbeyleix Road", "1 km from Stradbally", "County Laois"],
            [ROCOR], site="https://www.st-colman-church.com/",
        ),
        row(
            "ie-rocor-clifden-saint-patrick", "ru-great-britain-and-western-europe-rocor",
            "Mission of Saint Patrick of Ireland",
            "Миссия Святаго Патрика Ирландскаго", "IE",
            ["Atticlough", "Clifden, County Galway", "H71 W285"], [ROCOR],
            rank="Mission", site="https://www.orthodoxpatrick.ie/",
        ),
        row(
            "gb-ni-rocor-belfast-saint-john", "ru-great-britain-and-western-europe-rocor",
            "Parish of Saint John the Wonderworker of Shanghai",
            "Приходъ св. Іоанна Шанхайскаго чуд.", "GB",
            ["Lower Hall, Moravian Church", "1 University Road", "Belfast",
             "BT7 1NA"], [ROCOR],
            site="https://www.stjohnofshanghaibelfast.org/",
        ),
    ],
    "sr-britain-scandinavia": [
        row(
            "ie-serbian-dublin-saint-george", "sr-britain-scandinavia",
            "Serbian Orthodox Parish and Church Community of Saint George in Ireland",
            "Парохија Српске Православне Цркве у Републици Ирској, Црквена општина Светог Георгија",
            "IE", ["Artane Oratory of the Resurrection", "Kilmore Road",
                   "Beaumont, Dublin"],
            [SERBIAN_DIOCESE, "https://www.spcireland.org/en/o-nama/"],
            site="https://www.spcireland.org/",
        ),
        row(
            "ie-serbian-cork-faith-hope-love-sophia", "sr-britain-scandinavia",
            "Parish of the Holy Martyrs Faith, Hope, Love and Their Mother Sophia in Cork",
            "Парохија Светих мученица Вере, Наде, Љубави и мати им Софије у Корку",
            "IE", ["114 Knockfree Avenue", "Churchfield, Cork", "T23 W08N"],
            [SERBIAN_PARISHES, SERBIAN_CORK],
        ),
    ],
    "ro-ireland-iceland": [
        row(
            "ie-ro-dublin-holy-cross-cathedral", "ro-ireland-iceland",
            "Episcopal Cathedral Parish of the Exaltation of the Holy Cross",
            "Parohia Înălțarea Sfintei Cruci", "IE",
            ["Romanian Orthodox Church", "Leeson Park, Ballsbridge",
             "Dublin 6", "D06 E542"], [ROMANIAN_IRELAND],
            rank="Cathedral Parish",
        ),
        row(
            "ie-ro-dublin-saint-john-diocesan-centre", "ro-ireland-iceland",
            "Saint John the Baptist Diocesan Centre",
            "Centrul Eparhial Sfântul Ioan Botezătorul", "IE",
            ["Drimnagh Castle", "Long Mile Road", "Dublin 12", "D12 RP3F"],
            [ROMANIAN_IRELAND], rank="Diocesan Centre",
        ),
        row(
            "ie-ro-dublin-saint-george-columba", "ro-ireland-iceland",
            "Parish of Saint George the Great Martyr and Saint Columba",
            "Parohia Sfântul Mare Mucenic Gheorghe și Sfântul Columba", "IE",
            ["Saint Mary of the Servants", "Blakestown Way", "Dublin 15",
             "D15 RC42"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-dublin-annunciation-romanian-saints", "ro-ireland-iceland",
            "Parish of the Annunciation and the Sunday of Romanian Saints",
            "Parohia Buna Vestire și Duminica Sfinților Români", "IE",
            ["52B Western Way", "Broadstone", "Dublin 7", "D07 FA38"],
            [ROMANIAN_IRELAND], site="https://bisericasfintiiromani.com/",
        ),
        row(
            "ie-ro-dublin-all-saints-dionysius", "ro-ireland-iceland",
            "Parish of the Sunday of All Saints and Saint Dionysius Erhan",
            "Parohia Duminică Tuturor Sfinților și Sfântul Ierarh Dionisie Erhan",
            "IE", ["Dublin 5"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-dublin-saint-brendan-joseph", "ro-ireland-iceland",
            "Parish of Saint Brendan and Saint Joseph the New of Partoș",
            "Parohia Sfântul Brendan și Sfântul Iosif cel Nou de la Partoș", "IE",
            ["7 Mount Street Crescent", "Dublin 2", "D02 HC65"],
            [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-balbriggan-entry-dometius", "ro-ireland-iceland",
            "Parish of the Entry of the Mother of God and Saint Dometius the Merciful of Râmeț",
            "Parohia Intrarea Maicii Domnului în biserică și Sfântul Dometie cel milostiv de la Râmeț",
            "IE", ["Church Street", "Balbriggan", "K32 PW52"],
            [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-cork-callinicus-patrick", "ro-ireland-iceland",
            "Parish of Saint Callinicus of Cernica and Saint Patrick",
            "Parohia Sfântul Ierarh Calinic de la Cernica și Sfântul Patrick", "IE",
            ["Cork Road", "Passage West, County Cork"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-galway-nicholas-brigid", "ro-ireland-iceland",
            "Parish of Saint Nicholas and Saint Brigid of Kildare",
            "Parohia Sfântul Nicolae și Sfânta Brighita de la Kildare", "IE",
            ["St Mary's College Chapel", "St Mary's Road", "Galway",
             "H91 H7F8"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-kildare-pentecost-colman", "ro-ireland-iceland",
            "Parish of the Descent of the Holy Spirit and Saint Colman",
            "Parohia Pogorârea Sfântului Duh și Sfântul Colman", "IE",
            ["4 Moorefield Road", "Moorfield, Newbridge", "W12 HN15"],
            [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-kilkenny-arsenie-canice", "ro-ireland-iceland",
            "Parish of Venerable Confessor Arsenie of Prislop and Saint Canice",
            "Parohia Sfântul Cuvios Mărturisitor Arsenie de la Prislop și Sfântul Canice",
            "IE", ["Kilkenny"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-limerick-three-hierarchs-munchin", "ro-ireland-iceland",
            "Parish of the Three Holy Hierarchs and Saint Munchin",
            "Parohia Sfinții Trei Ierarhi, Vasile cel Mare, Grigorie Teologul și Ioan Gură de Aur, și Sfântul Munchin",
            "IE", ["St Saviour's Dominican Church", "Dominic Street",
                   "Limerick", "V94 X2AA"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-longford-nativity-saint-mel", "ro-ireland-iceland",
            "Parish of the Nativity of the Mother of God and Saint Mel of Ardagh",
            "Parohia Nașterea Maicii Domnului și Sfântul Ierarh Mel de Ardagh",
            "IE", ["Methodist Church", "Battery Road", "Abbeycartron",
                   "Longford"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-monasterevin-saint-evin-paraskeva", "ro-ireland-iceland",
            "Parish of Saint Evin of Munster and Saint Paraskeva of Iași",
            "Parohia Sfântul Cuvios Evin din Munster și Sfânta Cuvioasă Parascheva de la Iași",
            "IE", ["Monasterevin Council Hall", "Main Street",
                   "Monasterevin, County Kildare"], [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-navan-protection-saint-erc", "ro-ireland-iceland",
            "Parish of the Protection of the Mother of God and Saint Erc",
            "Parohia Acoperământul Maicii Domnului și Sfântul Erc", "IE",
            ["Fair Green, Townparks", "Navan", "C15 X0A3"],
            [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-nenagh-limerick-filial", "ie-ro-limerick-three-hierarchs-munchin",
            "Nenagh Filial Parish", "Filie a Parohiei Limerick", "IE",
            ["Chapel of Nenagh Hospital", "Tyone, Nenagh",
             "County Tipperary", "E45 PT86"], [ROMANIAN_IRELAND],
            rank="Filial Parish",
        ),
        row(
            "ie-ro-newcastle-west-mission", "ro-ireland-iceland",
            "Newcastle West Mission", "Misiunea din Newcastle West", "IE",
            ["Appletown Church", "Appletown, Feohanagh", "County Limerick",
             "V42 KX99"], [ROMANIAN_IRELAND], rank="Mission",
        ),
        row(
            "ie-ro-waterford-thomas-sunday-kevin", "ro-ireland-iceland",
            "Parish of Thomas Sunday and Saint Kevin of Glendalough",
            "Parohia Duminica Tomii și Sfântul Kevin de Glendalough", "IE",
            ["Church Road", "Lisduggan, Waterford", "X91 EY92"],
            [ROMANIAN_IRELAND],
        ),
        row(
            "ie-ro-ard-ciaran-life-giving-spring", "ro-ireland-iceland",
            "Life-Giving Spring Monastery",
            "Mănăstirea Izvorul Tămăduirii", "IE",
            ["Ard Ciaran", "Raghrabeg, County Westmeath", "N37 Y153"],
            [ROMANIAN_MONASTERY], kind="monastery", rank="Monastery",
            site="https://orthodoxmonasteryireland.ie/",
        ),
    ],
    "ro-great-britain": [
        row(
            "gb-ni-ro-ballymena-saint-john", "ro-great-britain",
            "Parish of Saint John the Apostle and Evangelist",
            "Parohia Sfântul Apostol și Evanghelist Ioan", "GB",
            ["All Saints", "4 Broughshane Road", "Ballymena", "BT43 7DX"],
            [ROMANIAN_NI],
        ),
        row(
            "gb-ni-ro-belfast-entry-theotokos", "ro-great-britain",
            "Parish of the Entry of the Mother of God into the Church",
            "Parohia Intrarea în Biserică a Maicii Domnului", "GB",
            ["St Paul's Church", "125 Falls Road", "Belfast", "BT12 6AB"],
            [ROMANIAN_NI], site="https://www.ocni.org.uk/",
        ),
    ],
    "ukraine-uoc": [
        row(
            "ie-uoc-dublin-protection", "ukraine-uoc",
            "Parish of the Protection of the Most Holy Theotokos in Dublin",
            "Парафія Покрови Пресвятої Богородиці у м. Дублін", "IE",
            ["Farranboley", "Dublin, County Dublin", "D14 VP11"],
            [UOC_DUBLIN, "https://vzcz.church.ua/2023/11/13/33805/"],
            site="https://www.uocdublin.org/",
        ),
        row(
            "ie-uoc-letterkenny-archangel-michael", "ukraine-uoc",
            "Parish of the Archangel Michael and the Other Bodiless Powers",
            "Парафія Української Православної Церкви на честь Архістратига Божого Михаїла та інших Небесних Сил безплотних",
            "IE", ["St Eunan's Cathedral", "Sentry Hill Road",
                   "Letterkenny, County Donegal"],
            [UOC_CENTRAL, UOC_LETTERKENNY],
        ),
        row(
            "ie-uoc-killarney-community", "ukraine-uoc",
            "Ukrainian Orthodox Church Community in Killarney",
            "Громада УПЦ у Кілларні", "IE",
            ["St Mary's Church", "Killarney, County Kerry"], [UOC_CENTRAL],
            rank="Community",
        ),
        row(
            "ie-uoc-navan-community", "ukraine-uoc",
            "Ukrainian Orthodox Church Community in Navan",
            "Громада УПЦ у Навані", "IE",
            ["St Anne's Chapel", "Fair Green, Dillonsland", "Navan",
             "County Meath", "C15 X0A3"], [UOC_CENTRAL], rank="Community",
        ),
        row(
            "ie-uoc-galway-community", "ukraine-uoc",
            "Ukrainian Orthodox Church Community in Galway",
            "Громада УПЦ у Голвеї", "IE",
            ["Church of the Resurrection", "Galway"], [UOC_CENTRAL],
            rank="Community",
        ),
    ],
}


# Exported for tools/directory_names/en.py. The source rows already carry the
# directory's English display names, so keeping this map derived prevents the
# catalogue label and the row label from drifting apart.
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "an-british-isles": 2,
    "ep-ireland": 3,
    "ep-thyateira": 1,
    "ro-great-britain": 2,
    "ro-ireland-iceland": 19,
    "ru-great-britain-and-western-europe-rocor": 3,
    "ru-sourozh": 14,
    "russia": 1,
    "sr-britain-scandinavia": 2,
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
    allowed_kinds = {"parish", "monastery"}
    country_counts = {"IE": 0, "GB": 0}
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
            if item.get("country") not in country_counts:
                raise ValueError("%s is outside Ireland and Northern Ireland" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            if item.get("site") and not item["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            country_counts[item["country"]] += 1
            rows.append(item)
        countries = sorted({item["country"] for item in rows})
        payload = {"v": 1, "parent": parent, "rows": rows}
        if len(countries) == 1:
            payload["country"] = countries[0]
        else:
            payload["countries"] = countries
        payloads[parent] = payload
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Ireland parent counts changed: %r" % actual)
    if country_counts != {"IE": 45, "GB": 7}:
        raise ValueError("Ireland country counts changed: %r" % country_counts)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 52:
        raise ValueError("Ireland English name coverage changed")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    answer = {}
    for parent, payload in sorted(payloads.items()):
        countries = payload.get("countries") or [payload["country"]]
        answer[parent] = {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "countries": countries,
        }
    return answer


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Ireland: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Ireland branches: 52 rows, 45 in IE, 7 in GB Northern Ireland")
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
