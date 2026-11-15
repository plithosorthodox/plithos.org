#!/usr/bin/env python3
"""Validated directory fragments for canonical Eastern Orthodox bodies in Norway.

The parent jurisdictions also carry rows from other countries. This module
therefore emits Norway-only fragments for later merging and never writes a
shared payload.

    python tools/directory_norway.py --check
    python tools/directory_norway.py --dump
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-14"

EP_PARISHES = "https://gomos.se/en/about-the-metropolis/parishes/"
RO_PARISHES = (
    "https://episcopiascandinavia.se/"
    "parohiile-ortodoxe-romanesti-din-regatul-norvegiei/"
)
RO_MAP = (
    "https://episcopiascandinavia.se/wp-content/uploads/2026/10/"
    "3.-MOBIL_harta_parohii_Scandinavia_v3.html"
)
MP_NORWAY = "https://www.ortodoks.no/"
MP_DEANERY = "https://patriarchia.ru/article/105460"
MP_OSLO = "https://www.ortodoks.no/oslo"
MP_STAVANGER = "https://www.ortodoks.no/stavanger"
MP_TRONDHEIM = "https://www.ortodoks.no/trondheim"
MP_ARENDAL = "https://www.ortodoks.no/arendal"
MP_SVALBARD = "https://www.ortodoks.no/svalbard"
MP_KIRKENES = "https://www.ortodoks.no/kirkenes"
ARCH_ANNUNCIATION = (
    "https://archeveche.eu/en/lieux/parish-of-the-annunciation/"
)
ARCH_HALLVARD = "https://archeveche.eu/lieux/paroisse-saint-hallvard/"
SERBIAN_BASIL = "https://www.vasilijeostroski.com/"
SERBIAN_PARISHES = "https://www.vasilijeostroski.com/parohije/"
SERBIAN_OSLO = "https://www.vasilijeostroski.com/oslo/"
SERBIAN_PORSGRUNN = "https://www.vasilijeostroski.com/porsgrunn/"
SERBIAN_BRUMUNDDAL = "https://www.vasilijeostroski.com/brumunddal/"
SERBIAN_BERGEN = "https://www.vasilijeostroski.com/bergen/"
SERBIAN_TRONDHEIM = "https://www.vasilijeostroski.com/trondheim/"
SERBIAN_SARPSBORG = "https://www.vasilijeostroski.com/sarpsborg/"
SERBIAN_TONSBERG = "https://www.vasilijeostroski.com/tonsberg-2/"
SERBIAN_DRAMMEN = "https://www.vasilijeostroski.com/dramen/"
SERBIAN_MO_I_RANA = "https://www.vasilijeostroski.com/mo-i-rana/"
SERBIAN_ALESUND = "https://www.vasilijeostroski.com/olesund/"
SERBIAN_BERGEN_CENTRAL = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/"
    "16540.osvestan-novi-srpski-pravoslavni-hram-u-bergenu.html"
)
SERBIAN_BRUMUNDDAL_CENTRAL = (
    "https://spc.rs/sr/news/aktuelno/16578.-osvestan-hram-sabora-"
    "srpskih-svetitelja-u-brumundalu.html"
)
SERBIAN_DEMETRIUS = "https://www.svetidimitrije.no/"
SERBIAN_NICHOLAS = "https://www.ortodokskirke.no/"
SERBIAN_ASSOCIATIONS = "https://www.ortodokskirke.no/kirkeforeninger"
SERBIAN_CONTACTS = "https://www.ortodokskirke.no/kontakt"
SERBIAN_SKETE = "https://www.ortodokskirke.no/hellige-trifon-skita"
BULGARIAN_DIRECTORY = "https://bg-patriarshia.bg/west-eu-diocese-temples"
MACEDONIAN_PARISH = "https://www.svpetka.no/"
MACEDONIAN_GOVERNMENT = (
    "https://minisel.gov.mk/%D0%B4%D1%83%D1%85%D0%BE%D0%B2%D0%BD%D0%B0-"
    "%D1%82%D1%80%D0%B8%D0%B1%D0%B8%D0%BD%D0%B0-%D0%B8-"
    "%D0%BF%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%87%D0%BD%D0%BE-"
    "%D0%BE%D0%B4%D0%B1%D0%B5%D0%BB%D0%B5%D0%B6%D1%83/"
)
UOC_NORWAY = "https://ukrortodoks.no/menigheter"
UOC_HOME = "https://ukrortodoks.no/"
UOC_SARPSBORG = "https://ukrortodoks.no/sarpsborg"
UOC_FAERDER = "https://ukrortodoks.no/faerder"
UOC_DRAMMEN = "https://ukrortodoks.no/drammen"
UOC_VISIT = (
    "https://vzcz.church.ua/2026/08/20/"
    "jepiskop-veniamin-vidvidav-parafiji-upc-v-krajinax-skandinaviji/"
)
UOC_SANDNES = (
    "https://vzcz.church.ua/2023/04/20/"
    "zakordonni-parafiji-upc-vidsvyatkuvali-svoje-pershe-svyato-pasxi/"
)
UOC_SANDNES_REGISTER = (
    "https://virksomhet.brreg.no/nb/oppslag/underenheter/934273311"
)
OCU_MISSION = (
    "https://www.pomisna.info/uk/document-post/"
    "dokumenty-zasidannya-svyashhennogo-synodu-18-zhovtnya-2022-r/"
)
OCU_NORWAY_ASSOCIATION = (
    "https://virksomhet.brreg.no/nb/oppslag/enheter/933229475"
)
OCU_NORWAY_CHAPLAINCY = (
    "https://virksomhet.brreg.no/nb/oppslag/enheter/931236830"
)
OCU_HOLY_VOLODYMYR = (
    "https://virksomhet.brreg.no/nb/oppslag/enheter/936057209"
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
        "country": "NO",
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
            "no-ep-oslo-annunciation", "ep-sweden",
            "Annunciation Greek Orthodox Metropolitan Church in Oslo",
            "Den gresk-ortodokse metropolitankirken Maria Bebudelse i Oslo",
            [EP_PARISHES], rank="Metropolitan Church",
            address=["Thor Olsens gate 9", "0177 Oslo, Norway"],
        ),
        row(
            "no-ep-stavanger-saint-nectarios", "ep-sweden",
            "St Nectarios Greek Orthodox Parish in Stavanger",
            "Den gresk-ortodokse menigheten Hellige Nektarios i Stavanger",
            [EP_PARISHES],
        ),
        row(
            "no-ep-bergen-chrysostom-smyrna", "ep-sweden",
            "St Chrysostom of Smyrna Greek Orthodox Parish in Bergen",
            "Den gresk-ortodokse menigheten Hellige Krysostomos av Smyrna i Bergen",
            [EP_PARISHES],
        ),
        row(
            "no-ep-trondheim-saint-gerasimos", "ep-sweden",
            "St Gerasimos of Cephalonia Greek Orthodox Parish in Trondheim",
            "Den gresk-ortodokse menigheten Hellige Gerasimos av Kefallinia i Trondheim",
            [EP_PARISHES],
        ),
        row(
            "no-ep-bo-saint-olav", "ep-sweden",
            "St Olav Parish in Bo, Telemark",
            "Den ortodokse misjonen til den hellige kong Olav",
            [EP_PARISHES],
            address=["Kyrkjevegen 78", "3800 Bo i Telemark, Norway"],
        ),
    ],
    "ro-northern-europe": [
        row(
            "no-ro-svalbard-seraphim-antipa-mission", "ro-northern-europe",
            "Mission of Saints Seraphim of Sarov and Antipa of Calapodesti in Svalbard",
            "Misiunea Sfinții Cuvioși Serafim de Sarov și Antipa de la Calapodești",
            [RO_PARISHES, RO_MAP], rank="Mission",
        ),
        row(
            "no-ro-alesund-nursing-icon-myrrhbearers-niculitel", "ro-northern-europe",
            "Parish of the Nursing Theotokos Icon of Tibles, the Myrrhbearers Mary and Martha, and the Martyrs of Niculitel in Alesund",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea\" de la Țibleș, Sfintele Mironosițe Maria și Marta și Sfinţii Mucenici Zotic, Atal, Camasie şi Filip de la Niculiţel",
            [RO_PARISHES, RO_MAP],
            address=["Kirkegata 33A", "Alesund, Norway"],
        ),
        row(
            "no-ro-bergen-theotokos-icons-martyrs", "ro-northern-europe",
            "Parish of the Theotokos Icons Receiver of Strangers and Nursing Mother of Tibles, and the Martyrs Philothea, Tatiana, and Sunniva in Bergen",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Primitoarea streinilor\" și \"Alăptătoarea de la Țibleș\", Sfintele Muceniţe Filofteia, Tatiana şi Suniva",
            [RO_PARISHES, RO_MAP],
            address=["Brattholmen 35", "5350 Bergen, Norway"],
            site="https://www.parohiabergen.no",
        ),
        row(
            "no-ro-bergen-saints-macarius-episcopal-chapel",
            "no-ro-bergen-theotokos-icons-martyrs",
            "Episcopal Chapel of the Synaxis of the Saints Macarius in Bergen",
            "Paraclisul Episcopal Soborul Sfinților Macarie",
            [RO_PARISHES, RO_MAP], rank="Episcopal Chapel",
        ),
        row(
            "no-ro-flekkefjord-alypius-nicon-stylianos-mission", "ro-northern-europe",
            "Mission of Saints Alypius the Stylite, Nicon the Preacher of Repentance, and Stylianos in Flekkefjord",
            "Misiunea Sfinții Cuvioși Alipie Stâlpnicul, Nicon propovăduitorul pocăinței şi Stelian, Ocrotitorul copiilor",
            [RO_PARISHES, RO_MAP], rank="Mission",
        ),
        row(
            "no-ro-forde-ascension", "ro-northern-europe",
            "Parish of the Ascension of the Lord in Forde",
            "Parohia Înălţarea Domnului",
            [RO_PARISHES, RO_MAP],
            address=["Forde Bedehus", "Elstervegen 2A", "6809 Forde, Norway"],
        ),
        row(
            "no-ro-fredrikstad-theotokos-martyrs", "ro-northern-europe",
            "Parish of the Nursing Theotokos Icon of Tibles and the Martyrs Niketas, Sava, Theodore, and John in Fredrikstad",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Alăptătoarea de la Țibleș\", Sfinții Mucenici Nichita, Sava, Teodor și Ioan",
            [RO_PARISHES, RO_MAP],
            address=["Ostre Gravlund kapell", "Gamlebyveien 1", "1632 Gamle Fredrikstad, Norway"],
        ),
        row(
            "no-ro-haugesund-all-blessed-icon-macarius", "ro-northern-europe",
            "Parish of the All-Blessed Theotokos Icon of Haugesund and Saints Macarius the Great and Macarius of Alexandria",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Cea de toți fericită\" de la Haugesund și Sfinții Cuvioși Macarie cel Mare și Macarie Alexandrinul",
            [RO_PARISHES, RO_MAP],
            address=["Tittelsnesvegen 346", "5514 Haugesund, Norway"],
        ),
        row(
            "no-ro-hamar-gregory-palamas-filial", "ro-northern-europe",
            "Filial of St Gregory Palamas in Hamar",
            "Filia Sfântul Ierarh Grigorie Palama, Arhiepiscopul Tesalonicului, cu Soborul Sfinților Grigorie",
            [RO_PARISHES, RO_MAP], rank="Filial",
        ),
        row(
            "no-ro-kirkenes-lapland-saints-mission", "ro-northern-europe",
            "Mission of Saints Tryphon, Jonah, Theodoret, Barlaam, and Porphyrios in Kirkenes",
            "Misiunea Sfinții Cuvioși Trifon cu Sfințitul Mucenic Iona de la Pecenga, Teodoret de la Kola, Varlaam de la Keret şi Porfirie Kavsokalivitul",
            [RO_PARISHES, RO_MAP], rank="Mission",
        ),
        row(
            "no-ro-kristiansand-theotokos-mina-macarius", "ro-northern-europe",
            "Parish of the Theotokos Icons Orans and Nursing Mother of Tibles, St Menas, and St Macarius the Roman in Kristiansand",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Oranta-Rugătoarea, a Semnului\" și \"Alăptătoarea de la Țibleș\", Sfântul Mare Mucenic Mina şi Sfântul Cuvios Macarie Romanul",
            [RO_PARISHES, RO_MAP],
            address=["Songdalsvegen 342", "4645 Nodeland, Norway"],
            site="https://parohia-kristiansand.org",
        ),
        row(
            "no-ro-mo-i-rana-first-council-fathers-filial", "ro-northern-europe",
            "Filial of the Holy Fathers of the First Ecumenical Council in Mo i Rana",
            "Filia Sfinții Ierarhi Macarie al Ierusalimului, Nicolae al Mirelor Lichiei, Spiridon al Trimitundei, Ipatie al Gangrei dimpreună cu ceilalți Sfinți Părinți de la Sinodul I Ecumenic de la Niceea",
            [RO_PARISHES, RO_MAP], rank="Filial",
        ),
        row(
            "no-ro-molde-procopius-epictetus-astion-sunniva", "ro-northern-europe",
            "Parish of the Martyrs Procopius, Theodosia, Epictetus, Astion, and Sunniva in Molde",
            "Parohia Sfinții Mari Mucenici Procopie cu mama, Teodosia, Epictet Preotul și Astion Monahul, Sfânta Muceniță Suniva cu cei dimpreună pătimitori cu ea",
            [RO_PARISHES, RO_MAP],
        ),
        row(
            "no-ro-myre-demetrius-nicholas-filial", "ro-northern-europe",
            "Filial of St Demetrius and St Nicholas in Myre",
            "Filia Sfântul Mare Mucenic Dimitrie Izvorâtorul de Mir, Sfântul Ierarh Nicolae al Mirelor Lichiei cu Soborul Sfinților Izvorâtori de Mir",
            [RO_PARISHES, RO_MAP], rank="Filial",
        ),
        row(
            "no-ro-narvik-george-theodoret-filial", "ro-northern-europe",
            "Filial of Saints George the Pilgrim and Theodoret of Kola in Narvik",
            "Filia Sfinții Cuvioși Gheorghe Pelerinul de la Văratec și Teodoret de la Kola, Luminătorul Laponiei",
            [RO_PARISHES, RO_MAP], rank="Filial",
        ),
        row(
            "no-ro-oslo-resurrection-theotokos-martyrs", "ro-northern-europe",
            "Parish of the Resurrection, the Quick to Hear Theotokos Icon, and the Martyrs John the Wallachian and Hallvard in Oslo",
            "Parohia Învierea Domnului, Cinstirea Icoanei Maicii Domnului \"Grabnic Ascultătoarea\" de la Oslo şi Sfinţii Mucenici Ioan Valahul şi Halvard Norvegianul",
            [RO_PARISHES, RO_MAP],
            address=["Voksen kapell", "Jarbakken 7", "0767 Oslo, Norway"],
            site="https://www.parohiaoslo.net",
        ),
        row(
            "no-ro-oslo-nursing-icon-episcopal-chapel",
            "no-ro-oslo-resurrection-theotokos-martyrs",
            "Episcopal Chapel of the Nursing Theotokos Icon of Tibles in Oslo",
            "Paraclisul Episcopal Cinstirea Icoanei Maicii Domnului \"Alăptătoarea\" de la Țibleș",
            [RO_PARISHES, RO_MAP], rank="Episcopal Chapel",
        ),
        row(
            "no-ro-skjervoy-leontie-iacob-pahomie-filial", "ro-northern-europe",
            "Filial of Saints Leontie of Radauti, Iacob of Putna, and Pahomie of Gledin in Skjervoy",
            "Filia Sfinții Arhieroschimonahi Leontie de la Rădăuți, Iacob Putneanul și Pahomie de la Gledinul Bistriței",
            [RO_PARISHES, RO_MAP], rank="Filial",
        ),
        row(
            "no-ro-stavanger-theotokos-annunciation-calnic-swithun", "ro-northern-europe",
            "Parish of the Lady of the Fjords and Nursing Theotokos Icons, the Annunciation, St Calinic, and St Swithun in Stavanger",
            "Parohia Cinstirea Icoanelor Maicii Domnului \"Stăpâna Fiordurilor\" și \"Alăptătoarea de la Țibleș\", Buna Vestire şi Sfinţii Ierarhi Calinic de la Cernica şi Svitun cel Smerit",
            [RO_PARISHES, RO_MAP],
            address=["Stefanuskyrkja", "Tarnveien 4", "4365 Narbo, Norway"],
            site="https://www.parohiastavanger.no",
        ),
        row(
            "no-ro-stord-john-climacus-mission", "ro-northern-europe",
            "Mission of St John Climacus in Stord",
            "Misiunea Sfântul Cuvios Ioan Scărarul",
            [RO_PARISHES, RO_MAP], rank="Mission",
        ),
        row(
            "no-ro-tromso-shepherdess-icon-saints", "ro-northern-europe",
            "Parish of the Shepherdess Theotokos Icon, St Sisoes, and the Roman Martyrs in Tromso",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Păstorița\" de la Tromsø, Sfântul Cuvios Sisoe cel Mare şi Sfinții Mucenici Marius, Marta, Audifaciu, Avacum și Lucia",
            [RO_PARISHES, RO_MAP],
            address=["Tromso gravlunds kapell", "Kirkegardsvegen 1", "Tromso, Norway"],
        ),
        row(
            "no-ro-trondheim-theotokos-voivodes-olav", "ro-northern-europe",
            "Parish of the Theotokos Icon Enlighten Our Darkness, the Holy Voivodes Stephen and Neagoe, and King Olav in Trondheim",
            "Parohia Cinstirea Icoanei Maicii Domnului \"Luminează întunericul sufletelor noastre\" de la Trondheim, Sfinţii Voievozi Ştefan cel Mare, Neagoe Basarab şi Regele Martir Olav",
            [RO_PARISHES, RO_MAP],
            address=["Stavne Kapell", "Osloveien 155D", "7019 Trondheim, Norway"],
        ),
    ],
    "russia": [
        row(
            "no-mp-deanery", "russia",
            "Deanery of Parishes of the Moscow Patriarchate in Norway",
            "Prosti for Moskva-patriarkatets menigheter i Norge",
            [MP_DEANERY, MP_NORWAY], rank="Deanery", kind="diocese",
            site=MP_NORWAY,
        ),
        row(
            "no-mp-oslo-saint-olga", "no-mp-deanery",
            "St Olga Parish in Oslo", "Hellige Olga menighet",
            [MP_OSLO, MP_NORWAY], address=["Akersveien 33", "0177 Oslo, Norway"],
            site=MP_OSLO,
        ),
        row(
            "no-mp-oslo-our-saviour-church", "no-mp-oslo-saint-olga",
            "Our Saviour Orthodox Church", "Vår Frelsers ortodokse kirke",
            [MP_OSLO], rank="Church", address=["Akersveien 33", "0177 Oslo, Norway"],
            site=MP_OSLO,
        ),
        row(
            "no-mp-stavanger-saint-irina", "no-mp-deanery",
            "St Irina Parish in Stavanger", "Hellige Irina menighet",
            [MP_STAVANGER, MP_NORWAY],
            address=["Kleppemarka 33", "4352 Kleppe, Norway"],
            site=MP_STAVANGER,
        ),
        row(
            "no-mp-bryne-line-bedehus", "no-mp-stavanger-saint-irina",
            "Line Bedehus Worship Site in Bryne", "Line Bedehus",
            [MP_STAVANGER], rank="Worship Site",
            address=["Hauglandsvegen 100", "Bryne, Norway"],
        ),
        row(
            "no-mp-karmoy-nordbo-bedehus", "no-mp-stavanger-saint-irina",
            "Nordbo Bedehus Worship Site in Karmoy", "Nordbø bedehus",
            [MP_STAVANGER], rank="Worship Site",
            address=["Bovegen 33", "4260 Torvastad, Norway"],
        ),
        row(
            "no-mp-trondheim-saint-anna", "no-mp-deanery",
            "St Anna Parish in Trondheim", "Hellige Anna menighet",
            [MP_TRONDHEIM, MP_NORWAY], site="https://ortodokstrondheim.wordpress.com",
        ),
        row(
            "no-mp-trondheim-bakke-church", "no-mp-trondheim-saint-anna",
            "Bakke Church Worship Site", "Bakke kirke",
            [MP_TRONDHEIM], rank="Worship Site",
            address=["Innherresveien 3", "Trondheim, Norway"],
        ),
        row(
            "no-mp-stiklestad-saint-olav-chapel", "no-mp-trondheim-saint-anna",
            "St Olav Orthodox Chapel at Stiklestad", "Hellige Olav ortodokse kapell",
            [MP_TRONDHEIM], rank="Chapel",
            address=["Stiklestad National Cultural Centre", "Stiklestad, Norway"],
        ),
        row(
            "no-mp-arendal-parish-group", "no-mp-deanery",
            "Orthodox Parish Group in Arendal", "Menighetsgruppe i Arendal",
            [MP_ARENDAL, MP_NORWAY], rank="Parish Group", site=MP_ARENDAL,
        ),
        row(
            "no-mp-arendal-transfiguration-house-chapel", "no-mp-arendal-parish-group",
            "Transfiguration House Chapel", "Kristi forklarelses huskapel",
            [MP_ARENDAL], rank="House Chapel",
        ),
        row(
            "no-mp-svalbard-community", "no-mp-deanery",
            "Russian Orthodox Community on Svalbard", "Menigheten på Svalbard",
            [MP_SVALBARD, MP_NORWAY], rank="Parish Community", site=MP_SVALBARD,
        ),
        row(
            "no-mp-barentsburg-dormition-house-church", "no-mp-svalbard-community",
            "Dormition House Church in Barentsburg", "Uspenie huskirke i Barentsburg",
            [MP_SVALBARD], rank="House Church",
            address=["Barentsburg Cultural Centre", "Barentsburg, Svalbard, Norway"],
        ),
        row(
            "no-mp-barentsburg-operafjellet-memorial-chapel", "no-mp-svalbard-community",
            "Operafjellet Air Disaster Memorial Chapel in Barentsburg",
            "Ortodoks minnekapell for flyulykken ved Operafjellet",
            [MP_SVALBARD], rank="Memorial Chapel",
            address=["Barentsburg, Svalbard, Norway"],
        ),
    ],
    "ru-murmansk": [
        row(
            "no-mp-kirkenes-saint-tryphon", "ru-murmansk",
            "St Tryphon Parish in Kirkenes", "Hellige Trifon menighet",
            [MP_KIRKENES, MP_NORWAY],
            address=["Hans Vaeggersvei 5", "9900 Kirkenes, Norway"],
            site="https://trifon-kirkenes.cerkov.ru",
        ),
    ],
    "ru-archdiocese-western-europe": [
        row(
            "no-russian-archdiocese-bergen-annunciation",
            "ru-archdiocese-western-europe",
            "Parish of the Annunciation in Bergen",
            "Hellige Jomfru Marias Bebudelse Ortodokse Menighet",
            [ARCH_ANNUNCIATION],
            address=["Kringsjaveien 28", "5162 Laksevag, Norway"],
            site="https://helligebebudelsen.com",
        ),
        row(
            "no-russian-archdiocese-oslo-saint-hallvard",
            "ru-archdiocese-western-europe",
            "St Hallvard Parish in Oslo", "Hellige Hallvard ortodokse menighet",
            [ARCH_HALLVARD], address=["Myrerveien 4", "0494 Oslo, Norway"],
            site="https://www.helligehallvard.no",
        ),
    ],
    "sr-scandinavia": [
        row(
            "no-sr-saint-basil-ostrog-community", "sr-scandinavia",
            "Church Community of St Basil of Ostrog in Norway",
            "Црквена општина Свети Василије Острошки",
            [SERBIAN_BASIL, SERBIAN_PARISHES], rank="Church Community",
            address=["Frognerveien 47", "0266 Oslo, Norway"], site=SERBIAN_BASIL,
        ),
        row(
            "no-sr-saint-basil-first-parish", "no-sr-saint-basil-ostrog-community",
            "First Parish of the Church Community of St Basil of Ostrog",
            "Прва парохија", [SERBIAN_PARISHES],
        ),
        row(
            "no-sr-saint-basil-second-parish", "no-sr-saint-basil-ostrog-community",
            "Second Parish of the Church Community of St Basil of Ostrog",
            "Друга парохија", [SERBIAN_PARISHES],
        ),
        row(
            "no-sr-saint-basil-third-parish", "no-sr-saint-basil-ostrog-community",
            "Third Parish of the Church Community of St Basil of Ostrog",
            "Трећа парохија", [SERBIAN_PARISHES],
        ),
        row(
            "no-sr-oslo-saint-basil-ostrog-church", "no-sr-saint-basil-ostrog-community",
            "Church of St Basil of Ostrog in Oslo", "Црква Светог Василија Острошког",
            [SERBIAN_OSLO, SERBIAN_BASIL], rank="Church",
            address=["Frognerveien 47", "0266 Oslo, Norway"], site=SERBIAN_OSLO,
        ),
        row(
            "no-sr-porsgrunn-cyril-methodius-church", "no-sr-saint-basil-second-parish",
            "Church of Saints Cyril and Methodius in Porsgrunn",
            "Црква Светог Ћирила и Методија", [SERBIAN_PORSGRUNN, SERBIAN_BASIL],
            rank="Church", address=["Winthersgate 10", "3921 Porsgrunn, Norway"],
            site=SERBIAN_PORSGRUNN,
        ),
        row(
            "no-sr-brumunddal-serbian-saints-church", "no-sr-saint-basil-first-parish",
            "Church of the Synaxis of Serbian Saints in Brumunddal",
            "Храм Сабора српских светитеља у Брумундалу",
            [SERBIAN_BRUMUNDDAL, SERBIAN_BRUMUNDDAL_CENTRAL], rank="Church",
            address=["Solheimvegen 89", "2384 Brumunddal, Norway"],
            site=SERBIAN_BRUMUNDDAL,
        ),
        row(
            "no-sr-bergen-myrrhbearers-church", "no-sr-saint-basil-third-parish",
            "Church of the Holy Myrrhbearers in Bergen",
            "Храм Светих жена мироносица у Бергену",
            [SERBIAN_BERGEN, SERBIAN_BERGEN_CENTRAL], rank="Church",
            site=SERBIAN_BERGEN,
        ),
        row(
            "no-sr-trondheim-service-point", "no-sr-saint-basil-third-parish",
            "Serbian Orthodox Service Point at Ilen Parish House in Trondheim",
            "Богослужбено место у Ilen menighetshus у Трондхајму",
            [SERBIAN_TRONDHEIM, SERBIAN_BASIL], rank="Service Point",
            address=["Ilen menighetshus", "Ilevollen 15", "7018 Trondheim, Norway"],
            site=SERBIAN_TRONDHEIM,
        ),
        row(
            "no-sr-sarpsborg-soli-church-service-point", "no-sr-saint-basil-first-parish",
            "Serbian Orthodox Service Point at Soli Church in Sarpsborg",
            "Богослужбено место у Soli kirke у Сарпсборгу",
            [SERBIAN_SARPSBORG, SERBIAN_BASIL], rank="Service Point",
            address=["Soli kirke", "Desiderias vei 200", "1719 Greaker, Norway"],
            site=SERBIAN_SARPSBORG,
        ),
        row(
            "no-sr-tonsberg-torod-church-service-point", "no-sr-saint-basil-second-parish",
            "Serbian Orthodox Service Point at Torod Church in Tonsberg",
            "Богослужбено место у Torød kirke у Тонсбергу",
            [SERBIAN_TONSBERG, SERBIAN_BASIL], rank="Service Point",
            address=["Torod kirke", "3135 Torod, Norway"],
            site=SERBIAN_TONSBERG,
        ),
        row(
            "no-sr-drammen-service-point", "no-sr-saint-basil-second-parish",
            "Serbian Orthodox Service Point in Drammen",
            "Богослужбено место у Драмену",
            [SERBIAN_DRAMMEN, SERBIAN_BASIL], rank="Service Point",
            address=["Solsvingen 90", "3034 Drammen, Norway"],
            site=SERBIAN_DRAMMEN,
        ),
        row(
            "no-sr-mo-i-rana-selfors-church-service-point", "no-sr-saint-basil-third-parish",
            "Serbian Orthodox Service Point at Selfors Church in Mo i Rana",
            "Богослужбено место у Selfors Kirke у Мо и Рани",
            [SERBIAN_MO_I_RANA, SERBIAN_BASIL], rank="Service Point",
            address=["Selfors Kirke", "Mo i Rana, Norway"],
            site=SERBIAN_MO_I_RANA,
        ),
        row(
            "no-sr-alesund-service-point", "no-sr-saint-basil-third-parish",
            "Serbian Orthodox Service Point in Alesund",
            "Богослужбено место у Олесунду",
            [SERBIAN_ALESUND, SERBIAN_BASIL], rank="Service Point",
            site=SERBIAN_ALESUND,
        ),
        row(
            "no-sr-kristiansand-saint-demetrius", "sr-scandinavia",
            "Parish and Church of St Demetrius of Thessaloniki in Kristiansand",
            "Парохија Светог Димитрија Солунског у Кристијансанду",
            [SERBIAN_DEMETRIUS],
            address=["Tinnheiveien 17", "4629 Kristiansand, Norway"],
            site=SERBIAN_DEMETRIUS,
        ),
        row(
            "no-sr-algard-constantine-helen-church", "no-sr-kristiansand-saint-demetrius",
            "Church of Saints Constantine and Helen in Algard",
            "Црква Светог цара Константина и царице Јелене у Олгорду",
            [SERBIAN_DEMETRIUS], rank="Church", site=SERBIAN_DEMETRIUS,
        ),
        row(
            "no-sr-holy-nicholas-parish", "sr-scandinavia",
            "Holy Nicholas Parish of the Orthodox Church in Norway",
            "Den ortodokse kirke i Norge - Hellige Nikolai menighet",
            [SERBIAN_NICHOLAS, SERBIAN_ASSOCIATIONS],
            address=["Tvetenveien 13", "0661 Oslo, Norway"], site=SERBIAN_NICHOLAS,
        ),
        row(
            "no-sr-nicholas-oslo-association", "no-sr-holy-nicholas-parish",
            "Oslo Church Association", "Oslo Kirkeforening",
            [SERBIAN_ASSOCIATIONS], rank="Church Association",
            address=["Tvetenveien 13", "0661 Oslo, Norway"],
        ),
        row(
            "no-sr-nicholas-bergen-association", "no-sr-holy-nicholas-parish",
            "Bergen Church Association", "Bergen Kirkeforening",
            [SERBIAN_ASSOCIATIONS, SERBIAN_CONTACTS], rank="Church Association",
            address=["Repslagergaten 17", "Skuteviken, Bergen, Norway"],
            site="https://www.ortodoksibergen.no",
        ),
        row(
            "no-sr-nicholas-rogaland-transfiguration-association", "no-sr-holy-nicholas-parish",
            "Transfiguration Church Association in Rogaland", "Kristi Forklarelse i Rogaland",
            [SERBIAN_ASSOCIATIONS, SERBIAN_CONTACTS], rank="Church Association",
            site="http://ortodoksstavanger.no/",
        ),
        row(
            "no-sr-sandnes-saint-elizabeth-chapel",
            "no-sr-nicholas-rogaland-transfiguration-association",
            "Holy Martyr Elizabeth Chapel in Sandnes", "Hellige Martyr Elisabeths kapell",
            [SERBIAN_ASSOCIATIONS, SERBIAN_CONTACTS], rank="Chapel",
            address=["Daleveien 3", "Sandnes, Norway"],
        ),
        row(
            "no-sr-nicholas-neiden-association", "no-sr-holy-nicholas-parish",
            "Neiden Church Association", "Neiden Kirkeforening",
            [SERBIAN_ASSOCIATIONS, SERBIAN_CONTACTS], rank="Church Association",
        ),
        row(
            "no-sr-neiden-saint-george-chapel", "no-sr-nicholas-neiden-association",
            "St George Orthodox Chapel in Neiden", "St. Georgs ortodokse kapell i Neiden",
            [SERBIAN_ASSOCIATIONS, SERBIAN_CONTACTS], rank="Chapel",
            address=["Neiden, Norway"],
        ),
        row(
            "no-sr-bodo-presentation-community", "no-sr-holy-nicholas-parish",
            "Presentation of Christ in the Temple Community in Bodo",
            "Kristi Frembærelse i Tempelet i Bodø",
            [SERBIAN_CONTACTS], rank="Parish Community",
        ),
        row(
            "no-sr-johnsegarden", "no-sr-holy-nicholas-parish",
            "Johnsegarden in Sogn og Fjordane", "Johnsegarden i Sogn og Fjordane",
            [SERBIAN_CONTACTS], rank="Parish Community",
            address=["6977 Bygstad, Norway"],
        ),
        row(
            "no-sr-helgoya-saint-john-theologian-chapel", "no-sr-johnsegarden",
            "Holy Apostle John the Theologian Chapel at Helgoya Cemetery",
            "Hellige apostel Johannes Teologens kapell",
            [SERBIAN_CONTACTS], rank="Chapel",
            address=["Helgoya kirkegard", "Norway"],
        ),
        row(
            "no-sr-hurdal-holy-tryphon-skete", "no-sr-holy-nicholas-parish",
            "Holy Tryphon Skete in Hurdal", "Hellige Trifon Skita",
            [SERBIAN_SKETE, SERBIAN_ASSOCIATIONS], rank="Skete", kind="monastery",
            address=["Hurdal, Norway"], site=SERBIAN_SKETE,
        ),
        row(
            "no-sr-hurdal-life-giving-trinity-church", "no-sr-hurdal-holy-tryphon-skete",
            "Church of the Life-Giving Trinity in Memory of St Tryphon of Pechenga",
            "Kirken til den levendegjørende Treenighet og minne om Hellige Trifon av Petsjenga",
            [SERBIAN_SKETE], rank="Church", kind="parish",
        ),
        row(
            "no-sr-hurdal-saint-seraphim-forest-chapel", "no-sr-hurdal-holy-tryphon-skete",
            "St Seraphim of Sarov Forest Chapel", "Hellige Serafim av Sarovs skogskapell",
            [SERBIAN_SKETE], rank="Chapel", kind="parish",
        ),
    ],
    "bg-western-central-europe": [
        row(
            "no-bg-oslo-cyril-methodius", "bg-western-central-europe",
            "Bulgarian Orthodox Church Community of Saints Cyril and Methodius in Oslo",
            "БПЦО \"Св. Кирил и Методий\" - гр. Осло",
            [BULGARIAN_DIRECTORY], rank="Church Community",
            address=["Enebakkveien 168", "0680 Oslo, Norway"],
        ),
    ],
    "mk-europe": [
        row(
            "no-mk-oslo-saint-petka", "mk-europe",
            "Macedonian Orthodox Church Community of Venerable Paraskeva, St Petka, in Oslo",
            "Македонска православна црковна општина Преподобна Параскева - Света Петка во Осло",
            [MACEDONIAN_PARISH, MACEDONIAN_GOVERNMENT], rank="Church Community",
            site=MACEDONIAN_PARISH,
        ),
    ],
    "ukraine-uoc": [
        row(
            "no-uoc-scandinavian-deanery", "ukraine-uoc",
            "Scandinavian Deanery of the Western European Vicariate",
            "Skandinavisk prosti i det vesteuropeiske vikariatet",
            [UOC_HOME, UOC_NORWAY], rank="Deanery", kind="diocese", site=UOC_HOME,
        ),
        row(
            "no-uoc-sarpsborg-saint-basil", "no-uoc-scandinavian-deanery",
            "Parish of St Basil the Great in Sarpsborg",
            "Menigheten Den hellige Basilios den Store i Sarpsborg",
            [UOC_SARPSBORG, UOC_NORWAY],
            address=["Tuneveien 43", "1710 Sarpsborg, Norway"], site=UOC_SARPSBORG,
        ),
        row(
            "no-uoc-faerder-protection", "no-uoc-scandinavian-deanery",
            "Parish of the Protection of the Mother of God in Faerder",
            "Menigheten Guds Mors Beskyttelse i Færder",
            [UOC_FAERDER, UOC_NORWAY],
            address=["Kirkeveien 192", "3140 Notteroy, Norway"], site=UOC_FAERDER,
        ),
        row(
            "no-uoc-drammen-saint-nectarios", "no-uoc-scandinavian-deanery",
            "Parish of St Nectarios of Aegina in Drammen",
            "Menigheten Den hellige Nektarios av Egina i Drammen",
            [UOC_DRAMMEN, UOC_NORWAY],
            address=["Tordenskiolds gate 58A", "3044 Drammen, Norway"], site=UOC_DRAMMEN,
        ),
        row(
            "no-uoc-sandnes-saint-nicholas", "ukraine-uoc",
            "Parish of St Nicholas the Wonderworker in Sandnes",
            "Den hellige Nikolai undergjørerens menighet i Sandnes",
            [UOC_NORWAY, UOC_SANDNES, UOC_SANDNES_REGISTER],
            address=["Telthusveien 1", "4319 Sandnes, Norway"],
        ),
        row(
            "no-uoc-kvinesdal-community", "ukraine-uoc",
            "Ukrainian Orthodox Parish in Kvinesdal",
            "Den ukrainske ortodokse menigheten i Kvinesdal",
            [UOC_NORWAY], address=["Nesgata 1", "4480 Kvinesdal, Norway"],
        ),
        row(
            "no-uoc-kristiansand-holy-trinity", "ukraine-uoc",
            "Holy Trinity Parish in Kristiansand",
            "Свято-Троїцька парафія УПЦ у Крістіансанні",
            [UOC_VISIT, UOC_NORWAY],
        ),
        row(
            "no-uoc-oslo-saint-olav", "ukraine-uoc",
            "Parish of St Olav in Oslo",
            "Парафія УПЦ на честь святого Олафа в Осло",
            [UOC_VISIT, UOC_NORWAY],
            address=["Gamlebyen kapell", "Ekebergveien 4", "0192 Oslo, Norway"],
        ),
    ],
    "ukraine-ocu": [
        row(
            "no-ocu-norway-association", "ukraine-ocu",
            "Orthodox Church of Ukraine in Norway Association",
            "Ukrainas ortodokse kyrkje i Noreg",
            [OCU_NORWAY_ASSOCIATION, OCU_MISSION], rank="Church Association",
        ),
        row(
            "no-ocu-chaplain-mission", "ukraine-ocu",
            "OCU Chaplain Mission in Norway",
            "Ukrainas ortodokse kyrkje (PTSU) - Kapellanmisjonen i Noreg",
            [OCU_NORWAY_CHAPLAINCY, OCU_MISSION], rank="Chaplain Mission",
        ),
        row(
            "no-ocu-holy-volodymyr-oslo-fredrikstad", "no-ocu-chaplain-mission",
            "Holy Volodymyr Ukrainian Orthodox Community in Oslo and Fredrikstad",
            "Hl. Volodymyr - det ukrainsk-ortodokse kirkesamfunnet i Oslo og Fredrikstad",
            [OCU_HOLY_VOLODYMYR, OCU_MISSION], rank="Parish Community",
        ),
    ],
}


SHARED_MULTI_COUNTRY_PARENTS = frozenset(ROWS)

ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}

EXPECTED = {
    "bg-western-central-europe": 1,
    "ep-sweden": 5,
    "mk-europe": 1,
    "ro-northern-europe": 22,
    "ru-archdiocese-western-europe": 2,
    "ru-murmansk": 1,
    "russia": 14,
    "sr-scandinavia": 29,
    "ukraine-uoc": 8,
    "ukraine-ocu": 3,
}

AUDITED_NO_ROWS = {
    "alexandria": "https://www.patriarchateofalexandria.com/archdioceses/?lang=en",
    "albania": "https://orthodoxalbania.org/2026/en/church-organization-2026/",
    "antioch": "https://antiochpatriarchate.org/en/page/3011/",
    "cyprus": "https://churchofcyprus.org.cy/diikitiki_diathrosi",
    "czech-slovak": "https://orthodox.sk/schematizmus/pravoslavna-eparchia/",
    "estonia": "https://www.eoc.ee/fr/eglise-orthodoxe-destonie/structure/",
    "finland": "https://ort.fi/en/finnish-orthodox-church/",
    "georgia": "https://patriarchate.ge/",
    "greece": "https://www.ecclesia.gr/",
    "japan": "https://www.orthodoxjapan.jp/",
    "jerusalem": "https://en.jerusalem-patriarchate.info/administrative-structure/holy-bishoprics/",
    "oca": "https://www.oca.org/parishes/search",
    "poland": "https://www.orthodox.pl/administracja/",
    "ru-great-britain-and-western-europe-rocor": "https://orthodox-europe.org/wp-content/uploads/2025/12/2026-Diocese-of-GB-and-W-Europe-Directory-PDF.pdf",
    "sinai": "https://www.sinaimonastery.com/index.php/en/",
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
    allowed_kinds = {"diocese", "monastery", "parish"}
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
            if item.get("country") != "NO":
                raise ValueError("%s is outside Norway" % row_id)
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
            "country": "NO",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Norway parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != sum(EXPECTED.values()):
        raise ValueError("Norway English name coverage changed")
    if SHARED_MULTI_COUNTRY_PARENTS != frozenset(EXPECTED):
        raise ValueError("Norway shared parent coverage changed")
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
        if parent not in base_ids:
            errors.append("missing directory parent: %s" % parent)
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Norway row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": "NO",
            "merge_required": True,
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
        errors = repository_problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Norway: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Norway branches: %d bodies under %d shared parents" %
          (sum(EXPECTED.values()), len(EXPECTED)))
    for parent, entry in manifest(payloads).items():
        print("%s: %d" % (parent, entry["count"]))
    print("additional canonical jurisdictions audited without Norway rows: %d" %
          len(AUDITED_NO_ROWS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
