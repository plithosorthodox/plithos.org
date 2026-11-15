#!/usr/bin/env python3
"""Australia parish-scale contributions to shared directory branches.

Every published body is documented by its own canonical jurisdiction. Search
engines and map listings were used only for discovery. This module does not
write shared payloads because most parent branches also contain other country
contributions.

    python tools/directory_australia.py --check
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIRECTORY_INDEX = ROOT / "data" / "directory.v1.json"
DATA_FILE = ROOT / "tools" / "directory_australia_data.json"
CHECKED = "2026-11-14"

ROWS_BY_PARENT = {}


def add(parent, suffix, name, rank="Parish", kind="parish", local=None,
        address=None, site=None, sources=None, dedication=None):
    row = dict(
        id="au-%s-%s" % (parent, suffix), parent=parent, kind=kind,
        rank=rank, english=name, local=local or name, country="AU",
        dedication=dedication or name, site=site,
        sources=list(sources or ([site] if site else [])),
    )
    if address:
        row["address"] = [address]
    ROWS_BY_PARENT.setdefault(parent, []).append(row)


def load_greek_rows():
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    church_index = (
        "https://greekorthodox.org.au/wp-json/wp/v2/"
        "churches_locations?per_page=100"
    )
    monastery_index = (
        "https://greekorthodox.org.au/wp-json/wp/v2/monasteries?"
        "per_page=100&_fields=id,slug,link,title,monasteries_locations"
    )
    for slug, name, rank, kind, address in data["greek_specs"]:
        stem = "monasteries" if kind == "monastery" else "churches"
        site = "https://greekorthodox.org.au/%s/%s/" % (stem, slug)
        add(
            "ep-australia", slug, name, rank=rank, kind=kind,
            address=address or None, site=site,
            sources=[site, monastery_index if kind == "monastery"
                     else church_index],
        )


load_greek_rows()


ANTIOCH_INDEX = (
    "https://www.antiochian.org.au/portfolio_category/"
    "australian-parishes/"
)
ANTIOCH_SPECS = [
    ("holy-cross-melbourne", "Holy Cross Mission in Melbourne North", "Mission"),
    ("st-george-cathedral-redfern", "Saint George Cathedral in Redfern", "Cathedral"),
    ("st-nicholas-punchbowl", "Saint Nicholas Church in Punchbowl", "Parish"),
    ("st-mary-mays-hill", "Saint Mary Church in Mays Hill", "Parish"),
    ("sts-michael-and-gabriel-ryde", "Saints Michael and Gabriel Church in Ryde", "Parish"),
    ("st-marys-mount-pritchard", "Saint Mary Church in Mount Pritchard", "Parish"),
    ("sts-peter-and-paul-doonside", "Saints Peter and Paul Church in Doonside", "Parish"),
    ("st-elias-wollongong", "Saint Elias Church in Wollongong", "Parish"),
    ("st-michael-kirrawee", "Saint Michael Church in Kirrawee", "Parish"),
    ("st-john-the-baptist-croydon-park", "Saint John the Baptist Church in Croydon Park", "Parish"),
    ("st-nicholas-bankstown", "Saint Nicholas Church in Bankstown", "Parish"),
    ("st-nicholas-east-melbourne", "Saint Nicholas Church in East Melbourne", "Parish"),
    ("st-george-thornbury", "Saint George Church in Thornbury", "Parish"),
    ("st-paul-dandenong", "Saint Paul Church in Dandenong", "Parish"),
    ("st-mary-yarraville", "Saint Mary Church in Yarraville", "Parish"),
    ("st-elias-west-croydon", "Saint Elias Church in West Croydon", "Parish"),
    ("st-paul-woolloongabba", "Saint Paul Church in Woolloongabba", "Parish"),
]
for slug, name, rank in ANTIOCH_SPECS:
    site = "https://www.antiochian.org.au/avada_portfolio/%s/" % slug
    add("an-australia", slug, name, rank=rank, site=site,
        sources=[ANTIOCH_INDEX, site])
goulburn = (
    "https://www.antiochian.org.au/avada_portfolio/"
    "st-michaels-antiochian-village-and-st-anna-monastery-goulburn/"
)
add("an-australia", "goulburn-saint-michael-monastery",
    "Saint Michael Monastery in Goulburn", rank="Monastery",
    kind="monastery", address="13 Kenmore Street, Goulburn NSW 2580",
    site=goulburn, sources=[ANTIOCH_INDEX, goulburn])
add("an-australia", "goulburn-saint-anna-chapel",
    "Saint Anna Chapel in Goulburn", rank="Chapel",
    address="13 Kenmore Street, Goulburn NSW 2580",
    site=goulburn, sources=[ANTIOCH_INDEX, goulburn])


ROMANIAN_API = "https://roeanz.com.au/api/parish"
ROMANIAN_SPECS = [
    ("life-giving-spring-monastery-melton-west", "The Life-Giving Spring Monastery - Diocesan Residence", "Mănăstirea Izvorul Tămăduirii - resedinţă eparhială", "Monastery", "monastery", "103 Porteous Road, Melton West VIC 3337", "manastirea-izvorul-tamaduirii-resedinta-eparhiala"),
    ("melbourne-holy-apostles", "The Romanian Orthodox Church of the Holy Apostles Peter and Paul in Melbourne", "Biserica Ortodoxă Română Sfinţii Apostoli Petru si Pavel - Melbourne", "Parish", "parish", "61-63 Queensberry Street, Carlton VIC 3053", "biserica-ortodoxa-romana-sfintii-apostoli-petru-si-pavel-melbourne"),
    ("sydney-saint-mary", "Saint Mary Church in Sydney", "Biserica Sfânta Maria - Sydney", "Parish", "parish", "64 Linthorn Avenue, Croydon Park NSW 2133", "biserica-sfanta-maria-sydney"),
    ("adelaide-saint-nicholas", "Saint Nicholas Church in Adelaide", "Biserica Sfântul Nicolae - Adelaide", "Parish", "parish", "9 Gilbert Street, Ovingham SA 5082", "biserica-sfantul-nicolae-adelaide"),
    ("brisbane-saint-demetrius", "Saint Demetrius Church in Brisbane", "Biserica Sfântul Dumitru - Brisbane", "Parish", "parish", "37 Brisbane Road, Riverview QLD", "biserica-sfantul-dumitru-brisbane"),
    ("sydney-saint-john-baptist", "Saint John the Baptist Church in Sydney", "Biserica Sfântul Ioan Botezătorul - Sydney", "Parish", "parish", "699 George Street, South Windsor NSW 2761", "biserica-sfantul-ioan-botezatorul-sydney"),
    ("perth-holy-trinity", "Holy Trinity Church in Perth", "Biserica Sfânta Treime - Perth", "Parish", "parish", "Koondoola Plaza, 8/34 Burbridge Avenue, Koondoola WA 6064", "biserica-sfanta-treime-perth"),
    ("sydney-saint-gregory-theologian", "Saint Gregory the Theologian Church in Sydney", "Biserica Sfântul Grigorie Teologul - Sydney", "Parish", "parish", "1803A Pittwater Road, Mona Vale NSW 2103", "biserica-sfantul-grigorie-teologul-sydney"),
    ("sydney-holy-brancoveanu-martyrs", "Holy Brâncoveanu Martyrs Church in Sydney", "Biserica Sfinţii Martiri Brâncoveni - Sydney", "Parish", "parish", "82 Canterbury Road, Glenfield NSW 2167", "biserica-sfintii-martiri-brancoveni-sydney"),
    ("dandenong-saint-thomas", "Saint Thomas the Apostle Church in Dandenong", "Biserica Sfântul Apostol Toma - Dandenong Victoria", "Parish", "parish", "57 Fox Road, Narre Warren North VIC 3804", "biserica-sfantul-apostol-toma-dandenong-victoria"),
    ("newcastle-saint-andrew", "Saint Andrew the Apostle Church in Newcastle", "Biserica Sfântul Apostol Andrei - Newcastle", "Parish", "parish", "3 Irving Street, Wallsend NSW 2287", "biserica-sfantul-apostol-andrei-newcastle"),
    ("brisbane-saint-philip", "Saint Philip the Apostle Church in Brisbane", "Biserica Sfântul Apostol Filip - Brisbane", "Parish", "parish", "10 Tansey Street, Beenleigh QLD", "biserica-sfantul-apostol-filip-brisbane"),
    ("cairns-saint-spyridon", "Saint Spyridon Church in Cairns", "Biserica Sfântul Spiridon - Cairns", "Parish", "parish", None, "biserica-sfantul-spiridon-cairns"),
    ("bayswater-saint-philothea", "Saint Philothea of Argeș Church in Bayswater", "Biserica Sfânta Filofteia de la Argeş - Bayswater Victoria", "Parish", "parish", "72 Highfield Road, Canterbury VIC", "biserica-sfanta-filofteia-de-la-arges-bayswater-victoria"),
    ("canberra-three-hierarchs", "Three Holy Hierarchs Church in Canberra", "Biserica Sfinţii Trei Ierarhi - Canberra", "Parish", "parish", None, "biserica-sfintii-trei-ierarhi-canberra"),
]
for suffix, name, local, rank, kind, address, slug in ROMANIAN_SPECS:
    site = "https://roeanz.com.au/parohia/%s" % slug
    add("ro-australia-nz", suffix, name, rank=rank, kind=kind,
        local=local, address=address, site=site,
        sources=[ROMANIAN_API, site])


MOC_DANZ_INDEX = "https://www.mocdanz.org.au/wp-json/wp/v2/pages?per_page=100"
MOC_DANZ_SPECS = [
    ("sutherland-holy-trinity", "Holy Trinity Church in Sutherland", "МПЦ Света Троица - Сатерланд", "moc-holy-trinity-sutherland", "Parish"),
    ("brisbane-dormition", "Dormition of the Most Holy Theotokos Church in Brisbane", "МПЦ Успение на Пресвета Богородица - Бризбен", "moc-assumption-of-the-virgin-mary-brisbane", "Parish"),
    ("adelaide-theotokos-cathedral", "Cathedral of the Most Holy Theotokos in Adelaide", "МПЦ Собор на Пресвета Богородица - Аделаид", "%d0%9c%d0%9f%d0%a6-%d0%a1%d0%be%d0%b1%d0%be%d1%80-%d0%bd%d0%b0-%d0%9f%d1%80%d0%b5%d1%81%d0%b2%d0%b5%d1%82%d0%b0-%d0%91%d0%be%d0%b3%d0%be%d1%80%d0%be%d0%b4%d0%b8%d1%86%d0%b0-%d0%90%d0%b4%d0%b5%d0%bb", "Cathedral"),
    ("footscray-prophet-elijah", "Prophet Elijah Church in Footscray", "МПЦ Свети Пророк Илија - Футскрај", "%d0%bc%d0%bf%d1%86-%d1%81%d0%b2%d0%b5%d1%82%d0%b8-%d0%bf%d1%80%d0%be%d1%80%d0%be%d0%ba-%d0%b8%d0%bb%d0%b8%d1%98%d0%b0-%d1%84%d1%83%d1%82%d1%81%d0%ba%d1%80%d0%b0%d1%98", "Parish"),
    ("preston-saint-nicholas", "Saint Nicholas Church in Preston", "МПЦ Свети Никола - Престон", "moc-saint-nicholas-preston", "Parish"),
    ("perth-saint-nicholas", "Saint Nicholas Church in Perth", "МПЦ Свети Никола - Перт", "moc-saint-nicholas-perth", "Parish"),
    ("mill-park-saint-petka", "Saint Petka Church in Mill Park", "МПЦ Света Петка - Мил Парк", "%d0%9c%d0%9f%d0%a6-%d0%a1%d0%b2%d0%b5%d1%82%d0%b0-%d0%9f%d0%b5%d1%82%d0%ba%d0%b0-%d0%9c%d0%b8%d0%bb-%d0%9f%d0%b0%d1%80%d0%ba", "Parish"),
    ("werribee-saint-zlata", "Saint Zlata of Meglen Church in Werribee", "МПЦ Света Злата Мегленска - Вереби", "%d0%9c%d0%9f%d0%a6-%d0%a1%d0%b2%d0%b5%d1%82%d0%b0-%d0%97%d0%bb%d0%b0%d1%82%d0%b0-%d0%9c%d0%b5%d0%b3%d0%bb%d0%b5%d0%bd%d1%81%d0%ba%d0%b0-%d0%92%d0%b5%d1%80%d0%b5%d0%b1%d0%b8", "Parish"),
    ("liverpool-theotokos-prechista", "Most Holy Theotokos Prechista Church in Liverpool", "МПЦ Света Богородица - Пречиста - Ливерпул", "%d0%bc%d0%bf%d1%86-%d1%81%d0%b2%d0%b5%d1%82%d0%b0-%d0%b1%d0%be%d0%b3%d0%be%d1%80%d0%be%d0%b4%d0%b8%d1%86%d0%b0-%d0%bf%d1%80%d0%b5%d1%87%d0%b8%d1%81%d1%82%d0%b0-%d0%bb%d0%b8%d0%b2%d0%b5%d1%80%d0%bf", "Parish"),
    ("sydenham-nativity-cathedral", "Nativity of the Virgin Mary Cathedral in Sydenham", "MOC Nativity of the Virgin Mary Mother of God - Cathedral Church, Sydenham", "%d1%80%d0%b0%d1%93%d0%b0%d1%9a%d0%b5-%d0%bd%d0%b0-%d0%bf%d1%80%d0%b5%d1%81%d0%b2%d0%b5%d1%82%d0%b0-%d0%b1%d0%be%d0%b3%d0%be%d1%80%d0%be%d0%b4%d0%b8%d1%86%d0%b0-%d1%81%d0%be%d0%b1o%d1%80%d0%bd%d0%b0", "Cathedral"),
    ("port-kembla-saint-clement", "Saint Clement of Ohrid Church in Port Kembla", "MПЦ Свети Климент Охридски - Порт Кембла", "m%d0%bf%d1%86-%d1%81%d0%b2%d0%b5%d1%82%d0%b8-%d0%ba%d0%bb%d0%b8%d0%bc%d0%b5%d0%bd%d1%82-%d0%be%d1%85%d1%80%d0%b8%d0%b4%d1%81%d0%ba%d0%b8-%d0%bf%d0%be%d1%80%d1%82-%d0%ba%d0%b5%d0%bc%d0%b1%d0%bb%d0%b0", "Parish"),
    ("springvale-saint-demetrius", "Saint Demetrius of Thessalonica Church in Springvale", "MПЦ Свети Димитриј Солунски - Спрингваeл", "sveti-dimitrij-sprinvajl", "Parish"),
]
for suffix, name, local, slug, rank in MOC_DANZ_SPECS:
    site = (
        "https://www.mocdanz.org.au/%d1%86%d1%80%d0%ba%d0%b2%d0%b8/"
        + slug + "/"
    )
    add("mk-australia-nz", suffix, name, rank=rank, local=local,
        site=site, sources=[MOC_DANZ_INDEX, site])
for suffix, name, local, slug in [
    ("kembla-grange-saint-parasceva", "Saint Parasceva Monastery in Kembla Grange", "Манастир Света Петка - Кембла Гранџ", "monastery-st-parasceva-kembla-grange"),
    ("rocklyn-saint-naum", "Saint Naum of Ohrid Monastery in Rocklyn", "Манастир Свети Наум Охридски - Роклин", "monastery-st-naum-ohridski-rocklyn"),
    ("donnybrook-saint-prohor", "Saint Prohor of Pčinja Monastery in Donnybrook", "Манастир Свети Прохор Пчински - Донибрук", "monastery-st-prohor-pchinski-donnybrook"),
]:
    site = (
        "https://www.mocdanz.org.au/"
        "%d0%9c%d0%90%d0%9d%d0%90%d0%a1%d0%a2%d0%98%d0%a0%d0%98/"
        + slug + "/"
    )
    add("mk-australia-nz", suffix, name, rank="Monastery", kind="monastery",
        local=local, site=site, sources=[MOC_DANZ_INDEX, site])


MOC_SYDNEY = "https://www.macedonianorthodoxdiocese.org.au/crkvi-i-manastiri/"
for suffix, name, local, rank, kind in [
    ("sydenham-dormition", "Dormition of the Most Holy Theotokos Church in Sydenham", "Црква 'Успение на Пресвета Богородица' - Сиденхам", "Parish", "parish"),
    ("epping-saint-george-theotokos", "Saint George and Most Holy Theotokos Church in Epping", "Црква 'Свети Ѓорѓи и Пресвета Богородица' - Епинг", "Parish", "parish"),
    ("kinglake-saint-clement-monastery", "Saint Clement of Ohrid Monastery in Kinglake", "Манастир 'Свети Климент Охридски' - Кинглејк", "Monastery", "monastery"),
    ("geelong-saint-john", "Saint John the Baptist Church in Geelong", "Црква 'Свети Јован Крстител' - Џилонг", "Parish", "parish"),
    ("cabramatta-saint-nicholas", "Saint Nicholas Church in Cabramatta", "Црква 'Свети Никола' - Кабрамата", "Parish", "parish"),
    ("wollongong-saint-demetrius", "Saint Demetrius Church in Wollongong", "Црква 'Свети Димитриј' - Волонгонг", "Parish", "parish"),
    ("canberra-saint-clement", "Saint Clement of Ohrid Church in Canberra", "Црква 'Свети Климент Охридски' - Канбера", "Parish", "parish"),
    ("queanbeyan-saint-elijah", "Saint Elijah Church in Queanbeyan", "Црква 'Свети Илија' - Квинбијан", "Parish", "parish"),
    ("perth-saint-nicholas", "Saint Nicholas Church in Perth", "Црква 'Свети Никола' - Перт", "Parish", "parish"),
    ("adelaide-saint-naum", "Saint Naum of Ohrid Church in Adelaide", "Црква 'Свети Наум Охридски' - Аделаид", "Parish", "parish"),
    ("gold-coast-saint-nedela", "Saint Nedela Church on the Gold Coast", "Црква 'Света Недела' - Голд Кост", "Parish", "parish"),
    ("rockdale-saint-petka", "Saint Petka Church in Rockdale", "Црква 'Света Петка' - Рокдејл", "Parish", "parish"),
]:
    add("mk-australia-sydney", suffix, name, rank=rank, kind=kind,
        local=local, site=MOC_SYDNEY, sources=[MOC_SYDNEY])


BULGARIAN_INDEX = "https://www.bulgariandiocese.org/parishdirectory"
for suffix, name, address in [
    ("adelaide-saint-petka", "Saint Petka Bulgarian Eastern Orthodox Church in Adelaide", "Adelaide, South Australia"),
    ("melbourne-saints-cyril-methodius", "Saints Cyril and Methody Bulgarian Eastern Orthodox Cathedral in Melbourne", "Melbourne, Victoria"),
]:
    add("bulgarian-usa", suffix, name,
        rank="Cathedral" if "Cathedral" in name else "Parish",
        address=address, site=BULGARIAN_INDEX,
        sources=["https://bg-patriarshia.bg/statute", BULGARIAN_INDEX])


UKRAINIAN_EP = "https://www.uocofausandnz.org/parishes"
for suffix, name, local, address in [
    ("canberra-saint-nicholas", "Saint Nicholas the Wonderworker Ukrainian Orthodox Parish in Canberra", "Парафія св. Миколая Чудотворця", "6 McKay Gardens, Turner ACT"),
    ("strathfield-protection", "Protection of the Most Holy Theotokos Ukrainian Orthodox Parish in Strathfield", "Парафія Покрови Пресвятої Богородиці", "Arthur Road and Mitchell Road, Strathfield West NSW"),
    ("granville-saint-athanasius", "Saint Athanasius Ukrainian Orthodox Parish in Granville", "Парафія св. Афанасія", "53 William Street, Granville NSW"),
    ("essendon-protection", "Protection of the Most Holy Theotokos Ukrainian Orthodox Parish in Essendon", "Парафія Покрови Пресвятої Богородиці", "91 Buckley Street, Essendon VIC"),
    ("balaclava-dormition", "Dormition of the Most Holy Theotokos Ukrainian Orthodox Parish in Balaclava", "Парафія Успіння Пресвятої Богородиці", "17 Camden Street, Balaclava VIC"),
    ("geelong-nativity", "Nativity of the Most Holy Theotokos Ukrainian Orthodox Parish in Geelong", "Парафія Різдва Пресвятої Богородиці", "14 Alder Crescent, Bell Park VIC"),
    ("perth-saint-nicholas", "Saint Nicholas Ukrainian Orthodox Parish in Perth", "Парафія св. Миколая Чудотворця", "2A Ferguson Street, Maylands WA"),
    ("brisbane-holy-trinity", "Holy Trinity Ukrainian Orthodox Parish in Brisbane", "Парафія св. Трійці Брізбен", "6 Wilkie Street, Yeerongpilly QLD"),
    ("brisbane-saint-nicholas", "Saint Nicholas the Wonderworker Ukrainian Orthodox Parish in Brisbane", "Парафія св. Миколая Чудотворця", "60 Vallely Street, Annerley QLD"),
    ("adelaide-saint-andrew", "Saint Andrew the First-Called Ukrainian Orthodox Parish in Adelaide", "Св. Ап. Андрія Первозванного", "420 Torrens Road, Kilkenny SA"),
]:
    add("ep-australia", "ukrainian-%s" % suffix, name, local=local,
        address=address, site=UKRAINIAN_EP, sources=[UKRAINIAN_EP])


OCU_INDEX = "https://www.uockp.net/parishes"
for suffix, name, local, address, site in [
    ("banksia-saint-savvas", "Saint Savvas of Kalymnos Ukrainian Orthodox Parish in Banksia", "SAINT SAVVAS OF KALYMNOS - BANKSIA", "316 Princes Highway, Banksia NSW 2216", "https://www.stsavvaskalymnos.org/"),
    ("blacktown-transfiguration", "Transfiguration of Our Lord Ukrainian Orthodox Parish in Blacktown", "TRANSFIGURATION OF OUR LORD - BLACKTOWN & DISTRICTS", "35A Kildare Road, Blacktown NSW 2148", OCU_INDEX),
    ("newcastle-saint-basil", "Saint Basil the Great Ukrainian Orthodox Parish in Newcastle", "SAINT BASIL THE GREAT - NEWCASTLE & DISTRICTS", "34 Morgan Street, Islington NSW 2296", None),
    ("adelaide-saint-michael", "Saint Michael the Archangel Ukrainian Orthodox Church in Croydon", "Українська Православна Церква св. Михаїла", "427 Port Road, Croydon SA 5008", OCU_INDEX),
    ("brisbane-saint-andrew", "Saint Andrew Ukrainian Orthodox Church in Brisbane", "Українська Православна Церква св. Андрія", "36 Primrose Street, Sherwood QLD 4075", OCU_INDEX),
]:
    add("ukraine-ocu", suffix, name, local=local, address=address,
        site=site if site and site != OCU_INDEX else None,
        sources=[OCU_INDEX, site] if site and site != OCU_INDEX
        else [OCU_INDEX])


MOSCOW_NEWS = "https://mospat.ru/en/news/94144/"
MOSCOW_SITE = "https://holy-trinity.org.au/"
add("russia", "moscow-oakleigh-holy-trinity",
    "Holy Trinity Parish of the Moscow Patriarchate in Oakleigh",
    local="Свято-Троицкий приход Русской Православной Церкви в Окли",
    address="4 Park Road, Oakleigh VIC 3166", site=MOSCOW_SITE,
    sources=[MOSCOW_NEWS, "https://holy-trinity.org.au/kontakty/"])
add("russia", "moscow-frankston-community",
    "Russian Orthodox Community in Frankston", rank="Community",
    local="Православная община района Frankston",
    address="103 Ashleigh Avenue, Frankston VIC 3199",
    site="https://holy-trinity.org.au/pravoslavnaya-obshhina-rajona-frankston-shtat-victoria/",
    sources=[MOSCOW_NEWS, "https://holy-trinity.org.au/pravoslavnaya-obshhina-rajona-frankston-shtat-victoria/"])
add("russia", "moscow-ballarat-community",
    "Russian Orthodox Community in Ballarat", rank="Community",
    local="Православная община г. Балларат",
    site="https://holy-trinity.org.au/ballarat/",
    sources=[MOSCOW_NEWS, "https://holy-trinity.org.au/ballarat/"])


SERBIAN_SPECS = [
    ("nsw-liverpool-saint-luke", "Saint Luke the Apostle Serbian Orthodox Church in Liverpool", "st-luke-the-apostle-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-peats-ridge-serbian-saints", "Synaxis of the Serbian Saints Orthodox Church in Peats Ridge", "synaxis-of-the-serbian-saints-orthodox-church", "Parish", "parish"),
    ("nsw-lightning-ridge-saint-george", "Saint George Serbian Orthodox Church in Lightning Ridge", "st-george-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-moree-saints-simeon-anna", "Saints Simeon and Anna Serbian Orthodox Parish in Moree", "sts-simeon-and-ana-serbian-orthodox-parish", "Parish", "parish"),
    ("act-mawson-entrance-theotokos", "Entrance of the Most Holy Theotokos Serbian Orthodox Parish in Mawson", "entrance-of-the-most-holy-theotokos-serbian-orthodox-parish", "Parish", "parish"),
    ("nsw-dapto-saint-john-baptist", "Saint John the Baptist Serbian Orthodox Church in Dapto", "st-john-the-baptist-serbian-orthodox-church-2", "Parish", "parish"),
    ("nsw-wollongong-saint-john-baptist", "Saint John the Baptist Serbian Orthodox Church in Wollongong", "st-john-the-baptist-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-plumpton-saint-stephen", "Saint Stephen the Archdeacon Serbian Orthodox Church in Plumpton", "st-stephen-the-archdeacon-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-broadmeadow-saint-naum", "Saint Naum of Ohrid Serbian Orthodox Church in Broadmeadow", "st-naum-of-ohrid-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-homebush-saint-michael", "Saint Michael the Archangel Serbian Orthodox Church in Homebush", "st-michael-the-archangel-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-homebush-west-saint-sava", "Saint Sava Serbian Orthodox Church in Homebush West", "st-sava-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-blacktown-saint-nicholas", "Saint Nicholas Serbian Orthodox Church in Blacktown", "st-nicholas-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-ingleside-saint-sava", "Saint Sava Serbian Orthodox Pro-Cathedral in Ingleside", "st-sava-serbian-orthodox-pro-cathedral", "Pro-Cathedral", "parish"),
    ("nsw-cabramatta-saint-george", "Saint George Serbian Orthodox Cathedral in Cabramatta", "st-george-serbian-orthodox-church-cathedral", "Cathedral", "parish"),
    ("nsw-alexandria-saint-lazarus", "Saint Lazarus Serbian Orthodox Co-Cathedral in Alexandria", "st-lazarus-serbian-orthodox-parish", "Co-Cathedral", "parish"),
    ("act-farrer-saint-sava", "Saint Sava Serbian Orthodox Church in Farrer", "st-sava-serbian-orthodox-church-2", "Parish", "parish"),
    ("act-forrest-saint-george", "Saint George Serbian Orthodox Church in Forrest", "st-george-serbian-orthodox-church-parish", "Parish", "parish"),
    ("vic-langwarrin-saint-basil", "Saint Basil of Ostrog Serbian Orthodox Church in Langwarrin", "st-basil-of-ostrog-serbian-orthodox-church", "Parish", "parish"),
    ("vic-wendouree-saints-ignatius-aidan", "Saint Ignatius of Antioch and Saint Aidan of Lindisfarne Orthodox Church in Wendouree", "st-ignatius-of-antioch-and-st-aidan-of-lindisfarne-orthodox-church", "Parish", "parish"),
    ("vic-brunswick-holy-trinity-cathedral", "Holy Trinity Serbian Orthodox Cathedral in Brunswick East", "holy-trinity-serbian-orthodox-cathedral", "Cathedral", "parish"),
    ("vic-carrum-downs-saint-steven", "Saint Steven of Dechani Serbian Orthodox Parish in Carrum Downs", "st-steven-of-dechani-serbian-orthodox-parish", "Parish", "parish"),
    ("vic-hamlyn-heights-saint-nicholas", "Saint Nicholas Serbian Orthodox Church in Hamlyn Heights", "st-nicholas-serbian-orthodox-church-2", "Parish", "parish"),
    ("vic-greensborough-saint-sava", "Saint Sava Serbian Orthodox Church in Greensborough", "st-sava-serbian-orthodox-church-3", "Parish", "parish"),
    ("vic-keysborough-saint-stephen", "Saint Stephen the Archdeacon Serbian Orthodox Church in Keysborough", "st-stephen-the-archdeacon-serbian-orthodox-church-2", "Parish", "parish"),
    ("vic-rockbank-saint-petka", "Saint Petka Serbian Orthodox Church in Rockbank", "st-petka-serbian-orthodox-church", "Parish", "parish"),
    ("vic-saint-albans-saint-george", "Saint George Serbian Orthodox Church in Saint Albans", "st-george-serbian-orthodox-church-2", "Parish", "parish"),
    ("vic-wodonga-saints-peter-paul", "Saints Peter and Paul Serbian Orthodox Church in Wodonga", "sts-peter-and-paul-serbian-orthodox-church", "Parish", "parish"),
    ("vic-yallourn-holy-trinity", "Holy Trinity Serbian Orthodox Church in Yallourn North", "holy-trinity-serbian-orthodox-church", "Parish", "parish"),
    ("nt-darwin-saint-sava", "Saint Sava Serbian Orthodox Church in Darwin", "st-sava-serbian-orthodox-church-5", "Parish", "parish"),
    ("qld-woolloongabba-saint-nicholas", "Saint Nicholas Serbian Orthodox Church in Woolloongabba", "st-nicholas-serbian-orthodox-church-4", "Parish", "parish"),
    ("qld-arundel-dormition", "Dormition of the Most Holy Theotokos Serbian Orthodox Church in Arundel", "dormition-of-the-most-holy-theotokos-serbian-orthodox-church", "Parish", "parish"),
    ("qld-sunnybank-saint-nicholas", "Saint Nicholas Serbian Orthodox Parish in Sunnybank", "st-nicholas-serbian-orthodox-parish", "Parish", "parish"),
    ("qld-cairns-saint-elijah", "Saint Elijah the Prophet Serbian Orthodox Parish in Cairns", "st-elijah-the-prophet-serbian-orthodox-parish", "Parish", "parish"),
    ("qld-wacol-saint-nicholas", "Saint Nicholas Serbian Orthodox Church in Wacol", "st-nicholas-serbian-orthodox-church-3", "Parish", "parish"),
    ("tas-lenah-valley-holy-cross", "Holy Cross Serbian Orthodox Parish in Lenah Valley", "holy-cross-serbian-orthodox-parish", "Parish", "parish"),
    ("wa-perth-holy-trinity", "Holy Trinity Serbian Orthodox Church in Perth", "holy-trinity-serbian-orthodox-church-2", "Parish", "parish"),
    ("wa-highgate-saint-sava", "Saint Sava Serbian Orthodox Church in Highgate", "st-sava-serbian-orthodox-church-6", "Parish", "parish"),
    ("wa-waterford-saint-basil-parish", "Saint Basil of Ostrog Serbian Orthodox Parish in Waterford", "st-basil-of-ostrog-serbian-orthodox-church-2", "Parish", "parish"),
    ("wa-rockingham-saint-basil", "Saint Basil of Ostrog Serbian Orthodox Church in Rockingham", "st-basil-of-ostrog-serbian-orthodox-church-3", "Parish", "parish"),
    ("sa-hindmarsh-saint-sava-parish", "Saint Sava Serbian Orthodox Parish in Hindmarsh", "st-sava-serbian-orthodox-parish", "Parish", "parish"),
    ("sa-woodville-saint-sava", "Saint Sava Serbian Orthodox Church in Woodville Park", "st-sava-serbian-orthodox-church-4", "Parish", "parish"),
    ("sa-coober-pedy-saint-elijah", "Saint Elijah the Prophet Serbian Orthodox Church in Coober Pedy", "st-elijah-the-prophet-serbian-orthodox-church", "Parish", "parish"),
    ("nsw-wallaroo-new-kalenich", "Saint Sava New Kalenich Serbian Orthodox Monastery in Wallaroo", "st-sava-new-kalenich-serbian-orthodox-monastery", "Monastery", "monastery"),
    ("nsw-tallong-protection-monastery", "Protection of the Most Holy Theotokos Serbian Orthodox Monastery in Tallong", "tallong-protection-of-the-most-holy-theotokos-serbian-orthodox-monastery", "Monastery", "monastery"),
    ("vic-elaine-saint-sava-monastery", "Saint Sava Monastery in Elaine", "st-sava-monastery-elaine", "Monastery", "monastery"),
    ("sa-inglewood-nativity-skete", "Nativity of the Most Holy Theotokos Skete in Inglewood", "nativity-of-the-most-holy-theotokos-skete-inglewood", "Skete", "monastery"),
]
for suffix, name, slug, rank, kind in SERBIAN_SPECS:
    section = "monastery" if kind == "monastery" else "parish"
    site = "https://soc.org.au/%s/%s/" % (section, slug)
    add("sr-australia-new-zealand", suffix, name, rank=rank, kind=kind,
        site=site, sources=[site])


ROCOR_INDEX = "https://directory.synod.com/listings/"
ROCOR_SPECS = [
    (15, "saint-john-forerunner-canberra", "Saint John the Forerunner Church in Canberra", "Parish", "parish", "Canberra ACT"),
    (16, "saints-peter-paul-strathfield", "Saints Peter and Paul Orthodox Cathedral in Strathfield", "Cathedral", "parish", "Strathfield NSW"),
    (17, "holy-dormition-wollongong", "Holy Dormition Community in Wollongong", "Community", "parish", "Wollongong NSW"),
    (18, "holy-trinity-croydon", "Holy Trinity Monastery in Croydon", "Monastery", "monastery", "Croydon NSW"),
    (19, "saint-nicholas-wallsend", "Saint Nicholas Church in Wallsend", "Parish", "parish", "Wallsend NSW"),
    (20, "saint-panteleimon-west-gosford", "Saint Panteleimon Church in West Gosford", "Parish", "parish", "West Gosford NSW"),
    (21, "presentation-convent-bungarby", "Presentation of the Mother of God Convent in Bungarby", "Convent", "monastery", "Bungarby NSW"),
    (22, "saint-john-baptist-skete-kentlyn", "Saint John the Baptist Skete in Kentlyn", "Skete", "monastery", "Kentlyn NSW"),
    (23, "intercession-cabramatta", "Intercession of the Holy Virgin Church in Cabramatta", "Parish", "parish", "Cabramatta NSW"),
    (230, "christ-saviour-rockdale", "Christ the Saviour Church in Rockdale", "Parish", "parish", "Rockdale NSW"),
    (24, "saint-george-carlton", "Saint George Church in Carlton", "Parish", "parish", "Carlton NSW"),
    (25, "saint-nicholas-fairfield", "Saint Nicholas Church in Fairfield", "Parish", "parish", "Fairfield NSW"),
    (26, "blessed-xenia-tweed-heads", "Blessed Xenia of Petersburg Church in Tweed Heads South", "Parish", "parish", "Tweed Heads South NSW"),
    (27, "our-lady-kazan-convent-kentlyn", "Our Lady of Kazan Convent in Kentlyn", "Convent", "monastery", "Kentlyn NSW"),
    (28, "all-russian-saints-croydon", "All Russian Saints Church in Croydon", "Parish", "parish", "Croydon NSW"),
    (29, "saint-vladimir-centennial-park", "Saint Vladimir Church in Centennial Park", "Parish", "parish", "Centennial Park NSW"),
    (30, "holy-transfiguration-bombala", "Holy Transfiguration Monastery in Bombala", "Monastery", "monastery", "Bombala NSW"),
    (31, "archangel-michael-marrickville", "Archangel Michael Monastery in Marrickville", "Monastery", "monastery", "Marrickville NSW"),
    (33, "holy-dormition-sisterhood-st-marys", "Holy Dormition Sisterhood in Saint Marys", "Sisterhood", "monastery", "Saint Marys NSW"),
    (34, "our-lady-vladimir-rocklea", "Our Lady of Vladimir Church in Rocklea", "Parish", "parish", "Rocklea QLD"),
    (35, "saint-nicholas-cathedral-kangaroo-point", "Saint Nicholas Cathedral in Kangaroo Point", "Cathedral", "parish", "Kangaroo Point QLD"),
    (36, "saint-seraphim-woolloongabba", "Saint Seraphim Church in Woolloongabba", "Parish", "parish", "Woolloongabba QLD"),
    (37, "holy-annunciation-woolloongabba", "Holy Annunciation Church in Woolloongabba", "Parish", "parish", "Woolloongabba QLD"),
    (39, "prophet-elias-monarto", "Prophet Elias Monastery in Monarto", "Monastery", "monastery", "Monarto SA"),
    (40, "saint-nicholas-wayville", "Saint Nicholas Church in Wayville", "Parish", "parish", "Wayville SA"),
    (41, "saint-patrick-elizabeth-grove", "Saint Patrick Mission in Elizabeth Grove", "Mission", "parish", "Elizabeth Grove SA"),
    (42, "saints-elizabeth-barbara-happy-valley", "Saints Elizabeth and Barbara Church in Happy Valley", "Parish", "parish", "Happy Valley SA"),
    (43, "exaltation-holy-cross-lenah-valley", "Exaltation of the Holy Cross Church in Lenah Valley", "Parish", "parish", "Lenah Valley TAS"),
    (44, "holy-trinity-lonnavale", "Holy Trinity Church in Lonnavale", "Parish", "parish", "Lonnavale TAS"),
    (45, "holy-fathers-warrnambool", "Holy Fathers Community in Warrnambool", "Community", "parish", "Warrnambool VIC"),
    (46, "our-lady-dormition-dandenong", "Dormition of Our Lady Church in Dandenong", "Parish", "parish", "Dandenong VIC"),
    (47, "joy-all-who-sorrow-bell-park", "Joy of All Who Sorrow Church in Bell Park", "Parish", "parish", "Bell Park VIC"),
    (48, "holy-virgin-protection-east-brunswick", "Holy Virgin Protection Cathedral in East Brunswick", "Cathedral", "parish", "East Brunswick VIC"),
    (49, "holy-ascension-keilor-east", "Holy Ascension Mission in Keilor East", "Mission", "parish", "Keilor East VIC"),
    (50, "saint-john-kronstadt-dandenong", "Saint John of Kronstadt Chapel in Dandenong", "Chapel", "parish", "Dandenong VIC"),
    (51, "saints-peter-paul-bayswater", "Saints Peter and Paul Church in Bayswater", "Parish", "parish", "Bayswater WA"),
    (607, "archangel-michael-blacktown", "Archangel Michael Church in Blacktown", "Parish", "parish", "Blacktown NSW"),
]
for number, suffix, name, rank, kind, address in ROCOR_SPECS:
    site = "https://directory.synod.com/listing/%d/%s/" % (number, suffix)
    add("ru-australia-and-new-zealand-rocor", suffix, name,
        rank=rank, kind=kind, address=address, site=site,
        sources=[ROCOR_INDEX, site])


ENGLISH_NAMES = {
    row["id"]: row["english"]
    for rows in ROWS_BY_PARENT.values()
    for row in rows
}


EXPECTED_COUNTS = {
    "ep-australia": 150,
    "an-australia": 19,
    "sr-australia-new-zealand": 46,
    "ro-australia-nz": 15,
    "mk-australia-nz": 15,
    "mk-australia-sydney": 12,
    "ru-australia-and-new-zealand-rocor": 37,
    "bulgarian-usa": 2,
    "ukraine-ocu": 5,
    "russia": 3,
}

SHARED_PAYLOAD_PARENTS = set(EXPECTED_COUNTS)

AUDITED_JURISDICTIONS_WITH_NO_PUBLISHED_AUSTRALIAN_BODY = {
    "alexandria": "https://www.patriarchateofalexandria.com/",
    "jerusalem": "https://en.jerusalem-patriarchate.info/",
    "cyprus": "https://churchofcyprus.org.cy/",
    "greece": "https://www.ecclesia.gr/",
    "albania": "https://orthodoxalbania.org/2020/en/",
    "poland": "https://www.orthodox.pl/administracja/",
    "czech-slovakia": "https://www.pp-eparchie.cz/",
    "oca": "https://www.oca.org/parishes",
    "finland": "https://ort.fi/en/parishes/",
    "estonia-eaok": "https://www.eoc.ee/parishes/",
    "estonia-ekok": "https://orthodox.ee/",
    "japan": "https://www.orthodoxjapan.jp/",
    "ukraine-uoc": "https://church.ua/",
}


def clean(row):
    out = {key: value for key, value in row.items()
           if value not in (None, "", [])}
    out["name"] = out.pop("english")
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("site") and not out["site"].startswith("http"):
        raise ValueError("%s carries a non-URL site" % out.get("id"))
    for value in out.values():
        texts = value if isinstance(value, list) else [value]
        for text in texts:
            if isinstance(text, str) and ("\u2013" in text or "\u2014" in text):
                raise ValueError("%s carries a forbidden long dash" % out.get("id"))
    return out


def build():
    public = json.loads(DIRECTORY_INDEX.read_text(encoding="utf-8"))
    public_ids = {row.get("id") for row in public.get("rows", [])}
    missing_parents = set(ROWS_BY_PARENT) - public_ids
    if missing_parents:
        raise ValueError("unknown parent ids: %s" %
                         ", ".join(sorted(missing_parents)))
    if set(ROWS_BY_PARENT) != set(EXPECTED_COUNTS):
        raise ValueError("parent assertions do not match source groups")

    contributions = {}
    seen = set()
    english_names = {}
    for parent, source_rows in ROWS_BY_PARENT.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen or row_id in public_ids:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if row.get("parent") != parent or row.get("country") != "AU":
                raise ValueError("%s is grouped incorrectly" % row_id)
            if row.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("rank") or not row.get("local"):
                raise ValueError("%s lacks its rank or local name" % row_id)
            if not row.get("dedication") or not row.get("name"):
                raise ValueError("%s lacks an English name or dedication" % row_id)
            english_names[row_id] = row["name"]
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED_COUNTS[parent]:
            raise ValueError("%s must contribute %d rows, found %d" %
                             (parent, EXPECTED_COUNTS[parent], len(rows)))
        contributions[parent] = rows

    if (len(english_names) != len(seen) or set(english_names) != seen or
            ENGLISH_NAMES != english_names):
        raise ValueError("English name coverage differs from row coverage")
    if sum(len(rows) for rows in contributions.values()) != 304:
        raise ValueError("Australia must contribute exactly 304 rows")
    return contributions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        contributions = build()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Australia: %s" % exc, file=sys.stderr)
        return 1
    counts = ", ".join(
        "%s=%d" % (parent, len(rows))
        for parent, rows in contributions.items()
    )
    print("Australia directory contributions: 304 rows (%s)" % counts)
    print("Audited canonical roots without a published Australian body: %d" %
          len(AUDITED_JURISDICTIONS_WITH_NO_PUBLISHED_AUSTRALIAN_BODY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
