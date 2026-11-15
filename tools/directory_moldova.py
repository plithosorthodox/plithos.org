#!/usr/bin/env python3
"""Current Orthodox directory branches sourced for the Republic of Moldova."""

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


CHECKED = "2026-11-15"
COUNTRY = "MD"
LEDGER = Path(__file__).with_name("directory_candidates") / "moldova.json"
OUT = Path(__file__).resolve().parent.parent / "data" / "directory"

# Root register additions and stable IDs for reparenting existing dioceses.
STRUCTURE_ROWS = json.loads(r'''[
  {
    "id": "ro-bessarabia",
    "within": "romania",
    "kind": "autonomous",
    "name": "Metropolis of Bessarabia and Exarchate of the Lands",
    "local": "Mitropolia Basarabiei, autonomă şi de stil vechi şi Exarhat al Plaiurilor",
    "rank": "Metropolis",
    "seat": "Chișinău",
    "country": "MD",
    "order": 8,
    "address": [
      "str. 31 August 1989, nr. 161, Chișinău"
    ],
    "site": "https://mitropoliabasarabiei.md/",
    "standing": "On 19 December 1992 the Romanian Orthodox Church recognized the restored Metropolis of Bessarabia as autonomous within the Romanian Patriarchate by a patriarchal and synodal act.",
    "standing_source": "https://mitropoliabasarabiei.md/istoric/",
    "sources": [
      "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/mitropolii/mitropolia-basarabiei-autonoma-si-de-stil-vechi-si-exarhat-al-plaiurilor/",
      "https://mitropoliabasarabiei.md/istoric/",
      "https://mitropoliabasarabiei.md/"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ru-orhei-vicar",
    "parent": "moldova",
    "kind": "seat",
    "rank": "Episcopal See",
    "name": "Vicar Bishopric of Orhei",
    "local": "Episcop de Orhei, Vicar mitropolitan",
    "seat": "Orhei",
    "country": "MD",
    "sources": [
      "https://mitropolia.md/sfanta-liturghie-si-slujba-prohodului-preotesei-maria-bulat-savarsite-la-orhei/",
      "https://mitropolia.md/eparhii/"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ru-capriana-vicar",
    "parent": "moldova",
    "kind": "seat",
    "rank": "Episcopal See",
    "name": "Vicar Bishopric of Căpriana",
    "local": "Episcop de Căpriana, Vicar mitropolitan",
    "seat": "Căpriana",
    "country": "MD",
    "sources": [
      "https://mitropolia.md/sfanta-liturghie-si-slujba-prohodului-preotesei-maria-bulat-savarsite-la-orhei/",
      "https://mitropolia.md/eparhii/"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ru-ceadir-lunga-vicar",
    "parent": "ru-cahul",
    "kind": "seat",
    "rank": "Episcopal See",
    "name": "Vicar Bishopric of Ceadîr-Lunga",
    "local": "Episcop de Ceadîr-Lunga, Vicar al Episcopiei de Cahul și Comrat",
    "seat": "Ceadîr-Lunga",
    "country": "MD",
    "sources": [
      "https://mitropolia.md/sfanta-liturghie-si-slujba-prohodului-preotesei-maria-bulat-savarsite-la-orhei/",
      "https://mitropolia.md/eparhii/"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ru-donduseni-vicar",
    "parent": "ru-edinet",
    "kind": "seat",
    "rank": "Episcopal See",
    "name": "Vicar Bishopric of Dondușeni",
    "local": "Episcop de Dondușeni, Vicar al Episcopiei de Edineț și Briceni",
    "seat": "Dondușeni",
    "country": "MD",
    "sources": [
      "https://mitropolia.md/sfanta-liturghie-si-slujba-prohodului-preotesei-maria-bulat-savarsite-la-orhei/",
      "https://mitropolia.md/eparhii/"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ro-bogdania-vicar",
    "parent": "ro-chisinau",
    "kind": "seat",
    "rank": "Episcopal See",
    "name": "Vicar Bishopric of Bogdania",
    "local": "Episcop-vicar al Arhiepiscopiei Chișinăului",
    "seat": "Chișinău",
    "country": "MD",
    "sources": [
      "https://mitropoliabasarabiei.md/ierarhii-mitropoliei-basarabiei-prezenti-la-proclamarea-canonizarii/",
      "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/mitropolii/mitropolia-basarabiei-autonoma-si-de-stil-vechi-si-exarhat-al-plaiurilor/"
    ],
    "checked": "2026-11-15"
  }
]''')
PARENT_CHANGES = dict.fromkeys(
    ("ro-chisinau", "ro-balti", "ro-south-bessarabia"), "ro-bessarabia"
)

# These bodies are geographically outside Moldova and retain their own country.
EXTERNAL_ROWS = json.loads(r'''[
  {
    "id": "ru-moscow-moldova-representation",
    "parent": "moldova",
    "kind": "monastery",
    "rank": "Metochion",
    "name": "Moldovan Orthodox Church Representation at Holy Trinity in Konkovo, Moscow",
    "local": "Представительство Кишиневско-Молдавской Митрополии при Храме Живоначальной Троицы в Конькове",
    "dedication": "Живоначальной Троицы",
    "seat": "Moscow",
    "country": "RU",
    "address": [
      "117437, Москва, ул.Профсоюзная, 116 (м. Коньково)"
    ],
    "site": "https://trinitykonkovo.ru/",
    "founded": [
      "Официальное представительство Кишиневско-Молдавской митрополии в Москве учреждено распоряжением Святейшего Патриарха Московского и всея Руси Кирилла 1 сентября 2015 года"
    ],
    "sources": [
      "https://trinitykonkovo.ru/o-hrame",
      "https://trinitykonkovo.ru/kontakty",
      "https://trinitykonkovo.ru/raspisanie-bogosluzheniya"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ua-ro-basarabia-hagi-curda-peter-paul",
    "parent": "ro-south-bessarabia",
    "kind": "parish",
    "rank": "Parish",
    "name": "Parish of the Holy Apostles Peter and Paul in Hagi-Curda",
    "local": "parohia „Sfinții Apostoli Petru și Pavel” Hagi-Curda",
    "dedication": "Sfinții Apostoli Petru și Pavel",
    "seat": "Hagi-Curda",
    "country": "UA",
    "sources": [
      "https://www.episcopiabasarabieidesud.md/articol/346"
    ],
    "checked": "2026-11-15"
  },
  {
    "id": "ua-ro-basarabia-reni-andrew",
    "parent": "ro-south-bessarabia",
    "kind": "parish",
    "rank": "Parish",
    "name": "Parish of Saint Andrew the Apostle in Reni",
    "local": "parohia „Sfântul Apostol Andrei” Reni",
    "dedication": "Sfântul Apostol Andrei",
    "seat": "Reni",
    "country": "UA",
    "sources": [
      "https://www.episcopiabasarabieidesud.md/articol/346"
    ],
    "checked": "2026-11-15"
  }
]''')

MONASTIC_RANKS = {"Monastery", "Skete", "Metochion"}
EXPECTED = {"moldova":53,"ro-balti":11,"ro-chisinau":99,"ro-south-bessarabia":50,"ru-balti":19,"ru-cahul":14,"ru-edinet":137,"ru-soroca":205,"ru-tiraspol":114,"ru-ungheni":159}

# Named deaneries from the dioceses' current administrative lists.
DEANERIES = (
    ("md-bom-chisinau-deanery", "moldova", "Chișinău Deanery", "PROTOPOPIATUL mun. CHIȘINĂU", "MD", "Chișinău", "MD-2004, str. București 119, mun. Chișinău", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-straseni-deanery", "moldova", "Strășeni Deanery", "PROTOPOPIATUL STRĂȘENI", "MD", "Căpriana", "MD-3712, com. Căpriana, r. Strășeni", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-orhei-deanery", "moldova", "Orhei Deanery", "PROTOPOPIATUL ORHEI", "MD", "Lucășeuca", "MD-3545, s. Lucășeuca, r. Orhei", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-ialoveni-deanery", "moldova", "Ialoveni Deanery", "PROTOPOPIATUL IALOVENI", "MD", "", "", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-anenii-noi-deanery", "moldova", "Anenii Noi Deanery", "PROTOPOPIATUL ANENII NOI", "MD", "", "", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-criuleni-and-dubasari-deanery", "moldova", "Criuleni and Dubăsari Deanery", "PROTOPOPIATUL CRIULENI ȘI DUBĂSARI", "MD", "Zăicana", "s. Zăicana, r. Criuleni", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-telenesti-deanery", "moldova", "Telenești Deanery", "PROTOPOPIATUL TELENEȘTI", "MD", "Sărătenii Vechi", "MD-5830, s. Sărătenii Vechi, r. Telenești", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-rezina-deanery", "moldova", "Rezina Deanery", "PROTOPOPIATUL REZINA", "MD", "Rezina", "MD-5412, str. 27 august 21, or. Rezina", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-causeni-deanery", "moldova", "Căușeni Deanery", "PROTOPOPIATUL CĂUȘENI", "MD", "Căușeni", "MD-4304, bd. M. Eminescu 4, or. Căușeni", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-soldanesti-deanery", "moldova", "Șoldănești Deanery", "PROTOPOPIATUL ȘOLDĂNEȘTI", "MD", "Șipca", "MD-7216, s. Șipca, r. Șoldănești", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-stefan-voda-deanery", "moldova", "Ștefan Vodă Deanery", "PROTOPOPIATUL ȘTEFAN VODĂ", "MD", "Olănești", "MD-4226, s. Olănești, r. Ștefan Vodă", ["https://mitropolia.md/protopopiate/"]),
    ("md-bom-balti-deanery", "ru-balti", "Bălți Deanery", "Blagocinia Bălţi", "MD", "", "", ["https://ephbalti.md/parohiile"]),
    ("md-bom-falesti-i-deanery", "ru-balti", "Fălești I Deanery", "Blagocinia Făleşti 1", "MD", "", "", ["https://ephbalti.md/parohiile"]),
    ("md-bom-falesti-ii-deanery", "ru-balti", "Fălești II Deanery", "Blagocinia Făleşti 2", "MD", "", "", ["https://ephbalti.md/parohiile"]),
    ("md-bom-glodeni-deanery", "ru-balti", "Glodeni Deanery", "Blagocinia Glodeni", "MD", "", "", ["https://ephbalti.md/parohiile"]),
    ("md-bom-singerei-deanery", "ru-balti", "Sîngerei Deanery", "Blagocinia Sîngerei", "MD", "", "", ["https://ephbalti.md/parohiile"]),
    ("md-bom-cahul-deanery", "ru-cahul", "Cahul Deanery", "Protopopiatul Cahul", "MD", "Cahul", "or. Cahul, str. L. Tolstoi, 1", ["https://episcopiasud.md/ro/protopopiate/"]),
    ("md-bom-gagauzia-deanery", "ru-cahul", "Gagauzia Deanery", "Protopopiatul UTA Gagauzia", "MD", "Ceadîr-Lunga", "MD-6100, str. Okteabrskaia 20, or. Ceadîr-Lunga, UTAG", ["https://episcopiasud.md/ro/protopopiate/"]),
    ("md-bom-cantemir-deanery", "ru-cahul", "Cantemir Deanery", "Protopopiatul Cantemir", "MD", "Cîrpești", "MD-7319, s. Cîrpești, r. Cantemir", ["https://episcopiasud.md/ro/protopopiate/"]),
    ("md-bom-cimislia-deanery", "ru-cahul", "Cimișlia Deanery", "Protopopiatul Cimişlia", "MD", "Sagaidac", "s. Sagaidac, r. Cimișlia", ["https://episcopiasud.md/ro/protopopiate/"]),
    ("md-bom-basarabeasca-deanery", "ru-cahul", "Basarabeasca Deanery", "Protopopiatul Basarabeasca", "MD", "Abaclia", "s. Abaclia, r.Basarabeasca", ["https://episcopiasud.md/ro/protopopiate/"]),
    ("md-bom-leova-deanery", "ru-cahul", "Leova Deanery", "Protopopiatul Leova", "MD", "Covurlui", "s. Covurlui, r. Leova", ["https://episcopiasud.md/ro/protopopiate/"]),
    ("md-bom-edinet-sector-i-deanery", "ru-edinet", "Edineț Sector I Deanery", "Blagocinia Edineț sector I", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-edinet-sector-i-2/"]),
    ("md-bom-edinet-sector-ii-deanery", "ru-edinet", "Edineț Sector II Deanery", "Blagocinia Edineț sector II", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-edinet-sector-ii/"]),
    ("md-bom-edinet-sector-iii-deanery", "ru-edinet", "Edineț Sector III Deanery", "Blagocinia Edineț sector III", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-edinet-sector-iii/"]),
    ("md-bom-briceni-sector-i-deanery", "ru-edinet", "Briceni Sector I Deanery", "Blagocinia Briceni sector I", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-briceni-sector-i/"]),
    ("md-bom-briceni-sector-ii-deanery", "ru-edinet", "Briceni Sector II Deanery", "Blagocinia Briceni sector II", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-briceni-sector-ii/"]),
    ("md-bom-ocnita-sector-i-deanery", "ru-edinet", "Ocnița Sector I Deanery", "Blagocinia Ocnița sector I", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-ocnita-sector-i/"]),
    ("md-bom-ocnita-sector-ii-deanery", "ru-edinet", "Ocnița Sector II Deanery", "Blagocinia Ocnița sector II", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-ocnita-sector-ii/"]),
    ("md-bom-donduseni-sector-i-deanery", "ru-edinet", "Dondușeni Sector I Deanery", "Blagocinia Dondușeni sector I", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-donduseni-sector-i/"]),
    ("md-bom-donduseni-sector-ii-deanery", "ru-edinet", "Dondușeni Sector II Deanery", "Blagocinia Dondușeni sector II", "MD", "", "", ["https://eparhia-edinet.md/blagocinii/","https://eparhia-edinet.md/portfolio/blagocinia-donduseni-sector-ii/"]),
    ("md-bom-soroca-deanery", "ru-soroca", "Soroca Deanery", "Protopopiatul Soroca", "MD", "", "", ["https://eparhiasoroca.md/protopopiate/","https://eparhiasoroca.md/protopopiate/soroca/"]),
    ("md-bom-drochia-deanery", "ru-soroca", "Drochia Deanery", "Protopopiatul Drochia", "MD", "", "", ["https://eparhiasoroca.md/protopopiate/","https://eparhiasoroca.md/protopopiate/drochia/"]),
    ("md-bom-floresti-deanery", "ru-soroca", "Florești Deanery", "Protopopiatul Florești", "MD", "", "", ["https://eparhiasoroca.md/protopopiate/","https://eparhiasoroca.md/protopopiate/floresti/"]),
    ("md-bom-riscani-deanery", "ru-soroca", "Rîșcani Deanery", "Protopopiatul Rîșcani", "MD", "", "", ["https://eparhiasoroca.md/protopopiate/","https://eparhiasoroca.md/protopopiate/riscani/"]),
    ("md-bom-central-deanery", "ru-tiraspol", "Central Deanery", "Центральное благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=246"]),
    ("md-bom-bender-deanery", "ru-tiraspol", "Bender Deanery", "Бендерское благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=247"]),
    ("md-bom-tiraspol-dubasari-deanery", "ru-tiraspol", "Dubăsari Deanery", "Дубоссарское благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=248"]),
    ("md-bom-slobozia-deanery", "ru-tiraspol", "Slobozia Deanery", "Слободзейское благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=249"]),
    ("md-bom-grigoriopol-deanery", "ru-tiraspol", "Grigoriopol Deanery", "Григориопольское благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=250"]),
    ("md-bom-ribnita-deanery", "ru-tiraspol", "Rîbnița Deanery", "Рыбницкое благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=251"]),
    ("md-bom-camenca-deanery", "ru-tiraspol", "Camenca Deanery", "Каменское благочиние", "MD", "", "", ["https://diocese-tiras.org/page.php?id=13","https://diocese-tiras.org/page.php?id=252"]),
    ("md-bom-ungheni-deanery", "ru-ungheni", "Ungheni Deanery", "Protopopiatul Ungheni", "MD", "", "", ["https://episcopia-ungheni.md/ro/protopopiate/"]),
    ("md-bom-nisporeni-deanery", "ru-ungheni", "Nisporeni Deanery", "Protopopiatul Nisporeni", "MD", "", "", ["https://episcopia-ungheni.md/ro/protopopiate/"]),
    ("md-bom-calarasi-deanery", "ru-ungheni", "Călărași Deanery", "Protopopiatul Călărași", "MD", "", "", ["https://episcopia-ungheni.md/ro/protopopiate/"]),
    ("md-bom-hincesti-deanery", "ru-ungheni", "Hîncești Deanery", "Protopopiatul Hîncești", "MD", "", "", ["https://episcopia-ungheni.md/ro/protopopiate/"]),
    ("md-basarabia-chisinau-deanery", "ro-chisinau", "Chișinău Deanery", "Protopopiatul Chișinău", "MD", "", "", ["https://mitropoliabasarabiei.md/protopopiate/"]),
    ("md-basarabia-ungheni-deanery", "ro-chisinau", "Ungheni Deanery", "Protopopiatul Ungheni", "MD", "", "", ["https://mitropoliabasarabiei.md/protopopiate/"]),
    ("md-basarabia-calarasi-deanery", "ro-chisinau", "Călărași Deanery", "Protopopiatul Călărași", "MD", "", "", ["https://mitropoliabasarabiei.md/protopopiate/"]),
    ("md-basarabia-hancesti-deanery", "ro-chisinau", "Hâncești Deanery", "Protopopiatul Hâncești", "MD", "", "", ["https://mitropoliabasarabiei.md/protopopiate/"]),
    ("md-basarabia-orhei-deanery", "ro-chisinau", "Orhei Deanery", "Protopopiatul Orhei", "MD", "", "", ["https://mitropoliabasarabiei.md/protopopiate/"]),
    ("md-basarabia-criuleni-and-dubasari-deanery", "ro-chisinau", "Criuleni and Dubăsari Deanery", "Protopopiatul Criuleni și Dubăsari", "MD", "", "", ["https://mitropoliabasarabiei.md/protopopiate/"]),
    ("md-basarabia-balti-balti-deanery", "ro-balti", "Bălți Deanery", "protopopiatul Bălţi", "MD", "", "", ["https://episcopia.md/ro/node/144","https://episcopia.md/ro/node/1374"]),
    ("md-basarabia-balti-falesti-deanery", "ro-balti", "Fălești Deanery", "protopopiatul Făleşti", "MD", "", "", ["https://episcopia.md/ro/node/144"]),
    ("md-basarabia-balti-soroca-and-floresti-deanery", "ro-balti", "Soroca and Florești Deanery", "protopopiatul Soroca şi Floreşti", "MD", "", "", ["https://episcopia.md/ro/node/144"]),
    ("md-basarabia-balti-edinet-and-donduseni-deanery", "ro-balti", "Edineț and Dondușeni Deanery", "Protopopul de Edineț și Dondușeni", "MD", "", "", ["https://episcopia.md/ro/node/144","https://episcopia.md/ro/node/1263"]),
    ("md-basarabia-sud-stefan-voda-deanery", "ro-south-bessarabia", "Ștefan Vodă Deanery", "Protopopiatul Ștefan Vodă", "MD", "", "", ["https://www.episcopiabasarabieidesud.md/","https://www.episcopiabasarabieidesud.md/manastiri/5/protopopiatul_Ștefan_vodă"]),
    ("md-basarabia-sud-causeni-deanery", "ro-south-bessarabia", "Căușeni Deanery", "Protopopiatul Căușeni", "MD", "", "", ["https://www.episcopiabasarabieidesud.md/","https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni"]),
    ("md-basarabia-sud-cimislia-deanery", "ro-south-bessarabia", "Cimișlia Deanery", "Protopopiatul Cimișlia", "MD", "", "", ["https://www.episcopiabasarabieidesud.md/","https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia"]),
    ("md-basarabia-sud-cantemirului-and-tigheciului-deanery", "ro-south-bessarabia", "Cantemirului and Tigheciului Deanery", "Protopopiatul Cantemirului și Tigheciului", "MD", "", "", ["https://www.episcopiabasarabieidesud.md/","https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului"]),
    ("md-basarabia-sud-cahul-deanery", "ro-south-bessarabia", "Cahul Deanery", "Protopopiatul Cahul", "MD", "", "", ["https://www.episcopiabasarabieidesud.md/","https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul"]),
    ("md-basarabia-sud-ismail-deanery", "ro-south-bessarabia", "Ismail Deanery", "Protopopiatul Ismail", "UA", "Ismail", "", ["https://www.episcopiabasarabieidesud.md/","https://www.episcopiabasarabieidesud.md/articol/346"]),
)

DETAILS = json.loads(r'''{
  "md-bom-chisinau-cathedral-transfiguration-of-the-lord": {
    "site": "https://csf.md/",
    "sources": [
      "https://csf.md/program-liturgic/"
    ],
    "services": [
      "● În zilele de Duminică şi sărbători:",
      "9⁰⁰ ▬ Sfânta şi Dumnezeiasca Liturghie."
    ],
    "languages": [
      "română",
      "slavă"
    ]
  },
  "md-bom-chisinau-church-meeting-of-the-lord": {
    "site": "https://biserica-usm.md/",
    "sources": [
      "https://biserica-usm.md/contacte/"
    ]
  },
  "md-bom-chisinau-church-saint-spyridon-of-trimythous": {
    "site": "https://biserica-spiridon.info/",
    "sources": [
      "https://biserica-spiridon.info/program/"
    ],
    "address": [
      "Chișinău, Spitalul de Urgență, str. Toma Ciorba 1"
    ],
    "services": [
      "Duminică, ora 8.00 - Rugăciunile dimineții, Ceasurile III și VI, ora 8.45 - Sfânta Liturghie; 10.45 - Tedeum; Predica."
    ]
  },
  "md-bom-curchi-monastery-nativity-of-the-mother-of-god": {
    "site": "https://manastireacurchi.md/",
    "sources": [
      "https://manastireacurchi.md/program-liturgic/"
    ],
    "services": [
      "Sâmbătă seara și in ajunul sarbătorilor:",
      "17.00- Privegherea",
      "Duminică şi sărbătorile:",
      "09.00 Sfînta și dumnezeiasca liturghie"
    ],
    "languages": [
      "română",
      "rusă"
    ]
  },
  "md-bom-chisinau-monastery-saint-theodore-the-recruit": {
    "site": "https://ciuflea.md/",
    "sources": [
      "https://ciuflea.md/programul-slujbelor/"
    ],
    "services": [
      "Sfânta Liturghie - zilnic, la ora 9:00",
      "Vecernia şi Utrenia - zilnic, la ora 17:00"
    ]
  },
  "md-bom-hagimus-monastery-saints-martha-and-mary-the-myrrhbearers": {
    "site": "https://martamaria.md/ro",
    "sources": [
      "https://martamaria.md/ro/program-liturgic"
    ],
    "services": [
      "DUMINICI ȘI SĂRBĂTORI",
      "6.00 Ceasurile 3, 6. Sf.Liturghie (în bis.Sf.Ștefan)",
      "8.00 Acatistul. Ceasurile 3, 6. Sf.Liturghie"
    ]
  },
  "md-bom-saharna-monastery-holy-trinity": {
    "site": "https://manastirea-saharna.md/",
    "sources": [
      "https://manastirea-saharna.md/programul-sfintelor-slujbe/"
    ],
    "services": [
      "17.00 Privegherea duminicală"
    ]
  },
  "md-bom-tiganesti-monastery-dormition-of-the-mother-of-god": {
    "site": "https://www.manastirea-tiganesti.md/",
    "sources": [
      "https://www.manastirea-tiganesti.md/contacte/"
    ]
  },
  "md-bom-suruceni-monastery-saint-george-the-great-martyr": {
    "site": "https://manastireasuruceni.md/",
    "sources": [
      "https://manastireasuruceni.md/contacte"
    ]
  },
  "md-bom-ungheni-varzaresti-monastery-nativity-of-the-mother-of-god": {
    "site": "https://varzaresti.md/",
    "sources": [
      "https://varzaresti.md/?page_id=25"
    ],
    "services": [
      "Sâmbătă, Duminică și de sărbători:",
      "08:45 Ceasurile III,VI și Sfânta Liturghie;",
      "16:00 Ceasul IX, Vecernia, Utrenia și ceasul I."
    ]
  },
  "md-bom-tiraspol-tiraspol-cathedral-nativity-of-christ": {
    "site": "https://sobor-tiraspol.com/",
    "sources": [
      "https://sobor-tiraspol.com/contacts.html"
    ]
  },
  "md-bom-edinet-calaraseuca-monastery-dormition-of-the-mother-of-god": {
    "site": "https://calarasovca.blogspot.com/",
    "sources": [
      "https://eparhia-edinet.md/portfolio/manastirea-adormirea-maicii-domnului-din-s-calaraseuca-r-ocnita/"
    ]
  },
  "md-basarabia-balti-lipnic-archangels": {
    "founded": [
      "Biserica din Lipnic a fost construită în anul 1863."
    ]
  },
  "md-basarabia-balti-rautel-dormition": {
    "founded": [
      "Temelia pentru biserica din Răuțel s-a pus în luna decembrie 1935."
    ]
  },
  "md-basarabia-balti-sangerei-theodora": {
    "founded": [
      "în data de 04 iunie 2023, a fost organizată parohia „Sfânta Cuvioasă Teodora de la Sihla” din or. Sângerei"
    ]
  }
}''')

# Each entry holds the official roster and any body-specific corroboration.
SOURCES = (
    ["https://mitropolia.md/resurse-ortodoxe/"],
    ["https://mitropolia.md/manastiri/"],
    ["https://mitropolia.md/protopopiate/"],
    ["https://mitropolia.md/liturghie-arhiereasca-si-slujba-de-sfintire-in-parohia-inaltarea-domnului-din-chirianca/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-oficiat-sfanta-liturghie-si-o-hirotonie-in-diacon-la-catedrala-mitropolitana/"],
    ["https://mitropolia.md/inaltpreasfintitul-mitropolit-vladimir-a-oferit-distinctii-la-resedinta-mitropolitana-din-chisinau/"],
    ["https://mitropolia.md/resurse-ortodoxe/","https://octavianmosin.md/contacte/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-oficiat-sfanta-liturghie-la-hramul-bisericii-sf-m-mc-dimitrie-din-sectorul-botanica-al-capitalei/"],
    ["https://mitropolia.md/preasfintitul-siluan-episcopul-orheiului-s-a-aflat-in-mijlocul-credinciosilor-parohiei-sfantul-apostol-si-evanghelist-ioan-teologul-din-municipiul-chisinau/"],
    ["https://episcopiasud.md/ro/ips-arhiepiscop-anatolie-a-coliturghisit-la-hramul-manastirii-invierea-domnului-din-incinta-cimitirului-sfantul-lazar-doina/"],
    ["https://mitropolia.md/eveniment-caritabil-pentru-membrii-asociatiei-orbilor-la-parohia-sf-cuv-dimitrie-cel-nou-din-chisinau/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-oficiat-sfanta-liturghie-in-biserica-sf-m-mc-dimitrie-din-coropceni-raionul-telenesti/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-vizitat-rezervatia-cultural-naturala-cuconestii-vechi-si-schitul-stavropighial-sf-arhanghel-mihail-si-sf-sofian/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-lliturghisit-in-parohia-nasterea-maicii-domnului-din-satul-ghermanesti-raionul-telenesti/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-liturghisit-in-parohia-acoperamantul-maicii-domnului-din-orasul-ialoveni/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-sfintit-pictura-bisericii-sfintii-parinti-ioachim-si-ana-a-schitului-odaia/"],
    ["https://mitropolia.md/sfanta-liturghie-si-slujba-prohodului-preotesei-maria-bulat-savarsite-la-orhei/"],
    ["https://mitropolia.md/inaltpreasfintitul-mitropolit-vladimir-a-liturghisit-la-hramul-bisericii-sfantul-apostol-si-evanghelist-ioan-teologul-din-peresecina/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-oficiat-randuiala-sfintirii-paraclisului-sfantul-ierarh-nicolae-din-singera/"],
    ["https://mitropolia.md/mitropolitul-vladimir-a-oficiat-dumnezeiasca-liturghie-in-biserica-sfantul-ierarh-nicolae-din-orasul-straseni/"],
    ["https://mitropolia.md/biserica-cu-hramul-acoperamantul-maicii-domnului-din-s-vatici-r-orhei-si-a-serbat-hramul/"],
    ["https://mitropolia.md/manastiri/","https://mitropolia.md/mitropolitul-vladimir-a-vizitat-manastirea-stavropighiala-nasterea-domnului-din-zabriceni-raionul-edinet/"],
    ["https://episcopia.md/ro/node/1395"],
    ["https://episcopia.md/ro/node/1385"],
    ["https://mitropoliabasarabiei.md/hram-la-manastirea-chirilovca/","https://mitropoliabasarabiei.md/mitropolitul-antonie-la-manastirea-chirilovca/"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1","https://mitropoliabasarabiei.md/mitropolitul-antonie-in-parohia-sfintii-trei-ierarhi/"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1","https://mitropoliabasarabiei.md/mitropolitul-antonie-a-vizitat-protopopiatul-criuleni/"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1","https://mitropoliabasarabiei.md/hramul-parohiei-crasnoarmeiscoe/"],
    ["https://mitropoliabasarabiei.md/hramul-paraclisului-din-dereneu/"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1","https://mitropoliabasarabiei.md/mitropolitul-basarabiei-in-mijlocul-credinciosilor-din-ialoveni-in-duminica-vindecarii-orbului/"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1","https://mitropoliabasarabiei.md/bucurie-duhovniceasca-in-stefan-voda-ips-petru-a-oficiat-sfanta-liturghie-in-parohia-sf-mucenite-vera-nadejda-liubov-si-sofia-din-ip-capsuna/"],
    ["https://mitropoliabasarabiei.md/lista-parohiilor-din-arhiepiscopia-chisinaului/","https://www.google.com/maps/d/kml?mid=1dRTCjaMV-W3j9-MxWwAZ7uZr8p-tU-o&forcekml=1","https://mitropoliabasarabiei.md/mitropolitul-antonie-alaturi-de-copii/"],
    ["https://mitropoliabasarabiei.md/hramul-parohiei-varvareuca/"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/8"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/5/protopopiatul_Ștefan_vodă","https://www.episcopiabasarabieidesud.md/manastiri/detalii/54"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/16"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia","https://www.episcopiabasarabieidesud.md/manastiri/detalii/49"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/30"],
    ["https://www.episcopiabasarabieidesud.md/articol/346","https://www.episcopiabasarabieidesud.md/articol/323"],
    ["https://www.episcopiabasarabieidesud.md/manastiri","https://www.episcopiabasarabieidesud.md/manastiri/detalii/2","https://www.episcopiabasarabieidesud.md/istoric"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/34"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/12"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/20"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/43"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/42"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/41"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia","https://www.episcopiabasarabieidesud.md/manastiri/detalii/46"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/15"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/29"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia","https://www.episcopiabasarabieidesud.md/manastiri/detalii/45"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia","https://www.episcopiabasarabieidesud.md/manastiri/detalii/50"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/23"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/36"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/6"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/39"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/17"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/5/protopopiatul_Ștefan_vodă","https://www.episcopiabasarabieidesud.md/manastiri/detalii/25"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/22"],
    ["https://www.episcopiabasarabieidesud.md/manastiri","https://www.episcopiabasarabieidesud.md/manastiri/detalii/55"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/35"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/26"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/31"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/37"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/27"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia","https://www.episcopiabasarabieidesud.md/manastiri/detalii/48"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/3/protopopiatul_cimișlia","https://www.episcopiabasarabieidesud.md/manastiri/detalii/47"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/11"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/40"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/21"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/13"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/5/protopopiatul_Ștefan_vodă","https://www.episcopiabasarabieidesud.md/manastiri/detalii/53"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/33"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/28"],
    ["https://www.episcopiabasarabieidesud.md/manastiri","https://www.episcopiabasarabieidesud.md/manastiri/detalii/1","https://www.episcopiabasarabieidesud.md/"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/14"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/32"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/5/protopopiatul_Ștefan_vodă","https://www.episcopiabasarabieidesud.md/manastiri/detalii/24"],
    ["https://www.episcopiabasarabieidesud.md/manastiri","https://www.episcopiabasarabieidesud.md/manastiri/detalii/3"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/18"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/2/protopopiatul_cantemirului_și_tigheciului","https://www.episcopiabasarabieidesud.md/manastiri/detalii/38"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/44"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/4/protopopiatul_căușeni","https://www.episcopiabasarabieidesud.md/manastiri/detalii/52"],
    ["https://www.episcopiabasarabieidesud.md/manastiri/1/protopopiatul_cahul","https://www.episcopiabasarabieidesud.md/manastiri/detalii/7"],
    ["https://ephbalti.md/balti/ips-marchel-alaturi-de-ierarhi-si-credinciosi-in-rugaciune-in-catedrala-sf-ier-nicolae.2025.12.07"],
    ["https://ephbalti.md/catedrala/sarbatoarea-sf-cuv-marchel-marcata-cu-evlavie-in-catedrala-din-balti-2.2026.01.11"],
    ["https://ephbalti.md/balti/la-hramul-bisericii-sf-app-petru-si-pavel-din-balti.2026.07.13"],
    ["https://ephbalti.md/glodeni/sarbatoare-de-aleasa-bucurie-duhovniceasca-la-parohia-sfintii-arhangheli-mihail-si-gavriil-din-satul-cobani-raionul-glodeni.2025.07.31"],
    ["https://ephbalti.md/falesti/ips-marchel-a-oficiat-sfanta-liturghie-in-biserica-cuvioasa-parascheva-din-satul-doltu.2026.10.17"],
    ["https://ephbalti.md/sangerei/adunarea-preotilor-blagociniei-singerei-la-biserica-sfantul-ierarh-nicolae-din-flamanzeni.2026.08.13"],
    ["https://ephbalti.md/cv"],
    ["https://episcopiasud.md/ro/ips-arhiepiscop-anatolie-a-condus-dumnezeiasca-liturghie-in-duminica-floriilor-la-catedrala-episcopala-sf-arh-mihail-si-gavriil-din-or-cahul/"],
    ["https://episcopiasud.md/ro/manastiri/manastiri/"],
    ["https://mitropolia.md/manastiri/","https://episcopiasud.md/ro/manastiri/manastiri/"],
    ["https://episcopiasud.md/ro/soborul-sfantului-prooroc-ioan-botezatorul-sarbatorit-in-rugaciune-la-catedrala-episcopala-din-comrat/"],
    ["https://episcopiasud.md/ro/inaltpreasfintitul-arhiepiscop-anatolie-a-liturghisit-la-hramul-bisericii-sfanta-treime-din-congaz/"],
    ["https://episcopiasud.md/ro/liturghie-arhiereasca-in-parohia-sf-m-mc-gheorghe-din-satul-porumbrei-raionul-cimislia/"],
    ["https://episcopiasud.md/ro/ips-arhiepiscop-anatolie-si-ps-episcop-nicolae-au-liturghisit-la-hramul-catedralei-episcopale-din-or-taraclia/"],
    ["https://eparhia-edinet.md/parohii/"],
    ["https://eparhia-edinet.md/parohii/","https://eparhia-edinet.md/portfolio/blagocinia-edinet-sector-iii/"],
    ["https://mitropolia.md/manastiri/","https://mitropolia.md/deciziile-sinodului-bisericii-ortodoxe-din-moldova/"],
    ["https://eparhiasoroca.md/protopopiate/floresti/parohii/"],
    ["https://eparhiasoroca.md/protopopiate/soroca/parohii/"],
    ["https://eparhiasoroca.md/protopopiate/riscani/parohii/"],
    ["https://eparhiasoroca.md/protopopiate/drochia/parohii/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-sfintele-mucenite-vera-nadejda-liubovi-si-mama-lor-sofia-din-s-cainarii-vechi-r-soroca/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-acoperamantul-maicii-domnului-din-s-cosauti-r-soroca/"],
    ["https://eparhiasoroca.md/protopopiate/drochia/parohii/","https://eparhiasoroca.md/protopopiate/drochia/parohii/catedrala-episcopala-adormirea-maicii-domnului-din-orasul-drochia/"],
    ["https://eparhiasoroca.md/protopopiate/drochia/parohii/","https://eparhiasoroca.md/protopopiate/drochia/parohii/parohia-sfantul-ierarh-nicolae-din-orasul-drochia/"],
    ["https://eparhiasoroca.md/protopopiate/drochia/parohii/","https://eparhiasoroca.md/parohia-sfantul-cuvios-serafim-de-sarov-din-orasul-drochia/"],
    ["https://eparhiasoroca.md/protopopiate/soroca/parohii/","https://eparhiasoroca.md/protopopiate/soroca/parohii/parohia-sfantul-ierarh-nicolae-din-satul-holosnita-raionul-soroca/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-icoana-maicii-domnului-bucuria-tuturor-scarbitilor-din-satul-inundeni-raionul-soroca/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-inaltarea-domnului-din-s-japca-r-floresti/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-sfintii-parinti-ioachim-si-ana-din-s-miciurin-r-drochia/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-sfantul-prooroc-ilie-din-s-nicoreni-r-drochia/"],
    ["https://eparhiasoroca.md/protopopiate/soroca/parohii/","https://eparhiasoroca.md/protopopiate/soroca/parohii/catedrala-episcopala-adormirea-maicii-domnului-din-municipiul-soroca/"],
    ["https://eparhiasoroca.md/protopopiate/soroca/parohii/","https://eparhiasoroca.md/protopopiate/soroca/parohii/parohia-sfantul-mare-mucenic-dimitrie-din-municipiul-soroca/"],
    ["https://eparhiasoroca.md/protopopiate/soroca/parohii/","https://eparhiasoroca.md/protopopiate/soroca/parohii/parohia-sfantul-cuvios-serafim-de-sarov-si-sfintii-apostoli-petru-si-pavel-din-municipiul-soroca/"],
    ["https://eparhiasoroca.md/protopopiate/soroca/parohii/","https://eparhiasoroca.md/protopopiate/soroca/parohii/parohia-sfantul-mare-mucenic-teodor-stratilat-din-municipiul-soroca/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-sfintii-arhangheli-mihail-si-gavriil-din-s-stirceni-r-floresti/"],
    ["https://eparhiasoroca.md/manastiri/","https://eparhiasoroca.md/manastiri/manastirea-sfantul-ioan-gura-de-aur-din-s-suri-r-drochia/"],
    ["https://diocese-tiras.org/page.php?id=251"],
    ["https://diocese-tiras.org/page.php?id=247"],
    ["https://diocese-tiras.org/page.php?id=253"],
    ["https://diocese-tiras.org/page.php?id=249"],
    ["https://diocese-tiras.org/page.php?id=250"],
    ["https://diocese-tiras.org/page.php?id=246"],
    ["https://diocese-tiras.org/page.php?id=248"],
    ["https://diocese-tiras.org/page.php?id=252"],
    ["https://episcopia-ungheni.md/ro/bisericile-din-cadrul-protopopiatului-ungheni/"],
    ["https://episcopia-ungheni.md/ro/bisericile-din-cadrul-protopopiatului-calarasi/"],
    ["https://episcopia-ungheni.md/ro/bisericile-din-cadrul-protopopiatului-nisporeni/"],
    ["https://episcopia-ungheni.md/ro/bisericile-din-cadrul-protopopiatului-hincesti/"],
    ["https://episcopia-ungheni.md/ro/bisericile-din-cadrul-protopopiatului-nisporeni/","https://mitropolia.md/deciziile-sinodului-bisericii-ortodoxe-din-moldova/"],
    ["https://mitropolia.md/manastiri/","https://mitropolia.md/mitropolitul-vladimir-a-adresat-un-mesaj-de-felicitare-arhimandritului-paisie-staretul-manastirii-noul-neamt/"],
    ["https://mitropolia.md/manastiri/","https://sitevechi.mitropolia.md/ips-mitropolit-vladimir-a-condus-sfanta-liturghie-in-ziua-proclamarii-oficiale-a-icoanei-maicii-domnului-de-la-manastirea-zloti/","https://episcopiasud.md/ro/episcopul-anatolie-de-cahul-si-comrat-sa-zidim-biserica-prin-jertfa-fiecaruia/"],
    ["https://mitropoliabasarabiei.md/duminica-ortodoxiei-prilej-de-comuniune-euharistica-si-bucurie-duhovniceasca-la-manastirea-sf-ap-andrei-din-durlesti/","https://mitropoliabasarabiei.md/zi-istorica-pentru-mitropolia-basarabiei-sarbatoarea-sfantului-apostol-andrei-si-proclamarea-anului-omagial-2026/"],
    ["https://mitropoliabasarabiei.md/ips-parinte-mitropolit-petru-al-basarabiei-in-vizita-pastorala-la-parohia-romaneasca-sfintii-martiri-brancoveni-din-soroca/","https://mitropoliabasarabiei.md/sfintii-martiri-brancoveni-cinstiti-prin-sfanta-liturghie-arhiereasca-cetatea-sorocii/"],
    ["https://episcopia.md/ro/node/1228","https://episcopia.md/ro/node/112"],
    ["https://episcopia.md/ro/node/1301","https://episcopia.md/ro/node/1230"],
    ["https://episcopia.md/ro/node/1253"],
    ["https://episcopia.md/ro/node/1263"],
    ["https://episcopia.md/ro/node/1283"],
    ["https://episcopia.md/ro/node/1284"],
    ["https://episcopia.md/ro/node/1236"],
    ["https://episcopia.md/ro/node/1259","https://mitropoliabasarabiei.md/hramul-parohiei-varvareuca/"],
    ["https://ephbalti.md/administratia/consiliul-eparhial","https://ephbalti.md/parohiile"],
    ["https://ephbalti.md/administratia/consiliul-eparhial"],
    ["https://ephbalti.md/administratia/consiliul-eparhial"],
    ["https://ephbalti.md/administratia/consiliul-eparhial"],
    ["https://ephbalti.md/administratia/consiliul-eparhial"],
    ["https://ephbalti.md/administratia/consiliul-eparhial"],
)

# ID, rank, English display name, published local name, seat, dedication,
# published address, and index into SOURCES.
RECORDS = {
    "moldova": (
        ("md-bom-chitcani-noul-neamt", "Monastery", "Ascension of the Lord Monastery of Noul Neamț in Chițcani", "Mănăstirea „Înălţarea Domnului”, Noul Neamţ", "Chițcani", "Înălţarea Domnului", "MD-5714, com. Chiţcani, r. Slobozia", 134),
        ("md-bom-anenii-noi-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Anenii Noi", "Biserica „Sf. Mare Mucenic Dimitrie” - Anenii Noi", "Anenii Noi", "Sf. Mare Mucenic Dimitrie", "", 0),
        ("md-bom-banestii-noi-skete-protection-of-the-mother-of-god", "Skete", "Protection of the Mother of God Skete in Băneștii Noi", "Schitul „Acoperământul Maicii Domnului”, Băneștii Noi", "Băneștii Noi", "Acoperământul Maicii Domnului", "MD-5811, s. Băneștii Noi, r. Telenești", 1),
        ("md-bom-butuceni-skete-dormition-of-the-mother-of-god", "Skete", "Dormition of the Mother of God Skete in Butuceni", "Schitul „Adormirea Maicii Domnului”, Butuceni", "Butuceni", "Adormirea Maicii Domnului", "MD-3552, s. Butuceni, r. Orhei", 1),
        ("md-bom-capriana-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Căpriana", "Mănăstirea „Adormirea Maicii Domnului”, Căpriana", "Căpriana", "Adormirea Maicii Domnului", "MD-3712, com. Căpriana, r. Străşeni", 1),
        ("md-bom-causeni-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Căușeni", "Biserica „Sf. Ap. Petru și Pavel”", "Căușeni", "Sf. Ap. Petru și Pavel", "MD-4304, bd. M. Eminescu 4, or. Căușeni", 2),
        ("md-bom-chirianca-parish-ascension-of-the-lord", "Parish", "Ascension of the Lord Parish in Chirianca", "Parohia „Înălțarea Domnului” din Chirianca", "Chirianca", "Înălțarea Domnului", "", 3),
        ("md-bom-chisinau-cathedral-nativity-of-christ", "Cathedral", "Nativity of Christ Cathedral in Chișinău", "Catedrala Mitropolitană „Nașterea Domnului”", "Chișinău", "Nașterea Domnului", "", 4),
        ("md-bom-chisinau-cathedral-transfiguration-of-the-lord", "Cathedral", "Transfiguration of the Lord Cathedral in Chișinău", "Catedrala „Schimbarea la Față” - Chișinău", "Chișinău", "Schimbarea la Față", "", 0),
        ("md-bom-chisinau-chapel-all-saints", "Chapel", "All Saints Chapel in Chișinău", "paraclisul mitropolitan cu hramul în cinstea ”Tuturor Sfinților”", "Chișinău", "Tuturor Sfinților", "", 5),
        ("md-bom-chisinau-church-meeting-of-the-lord", "Church", "Meeting of the Lord Church in Chișinău", "Biserica „Întâmpinarea Domnului” - Chișinău", "Chișinău", "Întâmpinarea Domnului", "mun. Chişinău, str. M. Kogălniceanu, nr. 67 (în spatele blocului II)", 6),
        ("md-bom-chisinau-church-prophet-elijah", "Church", "Prophet Elijah Church in Chișinău", "Biserica „Sf. Pr. Ilie”", "Chișinău", "Sf. Pr. Ilie", "Str. Mircea cel Bătrân 20, mun. Chișinău", 2),
        ("md-bom-chisinau-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Chișinău", "biserica „Sf. M. Mc. Dimitrie” din sectorul Botanica al capitalei", "Chișinău", "Sf. M. Mc. Dimitrie", "bd. Traian 3/1, mun. Chișinău", 7),
        ("md-bom-chisinau-church-saint-john-the-new-of-suceava", "Church", "Saint John the New of Suceava Church in Chișinău", "Biserica „Sf. Ioan cel Nou de la Suceava” - Chișinău", "Chișinău", "Sf. Ioan cel Nou de la Suceava", "", 0),
        ("md-bom-chisinau-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Chișinău", "parohiei „Sfântul Apostol și Evanghelist Ioan Teologul” din municipiul Chișinău", "Chișinău", "Sfântul Apostol și Evanghelist Ioan Teologul", "", 8),
        ("md-bom-chisinau-church-saint-spyridon-of-trimythous", "Church", "Saint Spyridon of Trimythous Church in Chișinău", "Biserica „Sf. Ierarh Spiridon al Trimitundei” - Chișinău", "Chișinău", "Sf. Ierarh Spiridon al Trimitundei", "", 0),
        ("md-bom-chisinau-monastery-resurrection-of-the-lord", "Monastery", "Resurrection of the Lord Monastery in Chișinău", "Mănăstirea „Învierea Domnului” din incinta cimitirului „Sf. Lazăr”", "Chișinău", "Învierea Domnului", "", 9),
        ("md-bom-chisinau-monastery-saint-theodore-the-recruit", "Monastery", "Saint Theodore the Recruit Monastery in Chișinău", "Mănăstirea „Sf. M. Mc. Teodor Tiron”, Chișinău", "Chișinău", "Sf. M. Mc. Teodor Tiron", "MD-2001, str. Ciuflea 12, mun. Chișinău, mănăstirea „Sf. M. Mc. Teodor Tiron”", 1),
        ("md-bom-chisinau-parish-saint-demetrius-the-new", "Parish", "Saint Demetrius the New Parish in Chișinău", "parohia „Sf. Cuv. Dimitrie cel Nou” din Chișinău", "Chișinău", "Sf. Cuv. Dimitrie cel Nou", "", 10),
        ("md-bom-chistelnita-monastery-holy-archangels-michael-and-gabriel", "Monastery", "Holy Archangels Michael and Gabriel Monastery in Chiştelniţa", "Mănăstirea „Sf. Arh. Mihail și Gavriil”, Chiştelniţa", "Chiştelniţa", "Sf. Arh. Mihail și Gavriil", "MD-5815, com. Chiştelniţa, r. Teleneşti", 1),
        ("md-bom-chitcani-skete-saints-vincent-and-dorimedont", "Skete", "Saints Vincent and Dorimedont Skete in Chițcani", "Schitul „Sf. Mcc. Vichentie și Dorimedont”, Chițcani", "Chițcani", "Sf. Mcc. Vichentie și Dorimedont", "MD-5714, s. Chițcani, r. Slobozia", 1),
        ("md-bom-colonita-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Colonița", "Biserica „Nașterea Maicii Domnului” - Colonița, mun. Chișinău", "Colonița", "Nașterea Maicii Domnului", "", 0),
        ("md-bom-condrita-monastery-saint-nicholas", "Monastery", "Saint Nicholas Monastery in Condriţa", "Mănăstirea „Sf. Irh. Nicolae”, Condriţa", "Condriţa", "Sf. Irh. Nicolae", "MD-2083, s. Condriţa, mun. Chișinău", 1),
        ("md-bom-coropceni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Coropceni", "Biserica „Sf. M. Mc. Dimitrie” din Coropceni", "Coropceni", "Sf. M. Mc. Dimitrie", "", 11),
        ("md-bom-cuconestii-vechi-skete-archangel-michael-and-saint-sofian", "Skete", "Archangel Michael and Saint Sofian Skete in Cuconeștii Vechi", "Schitul Stavropighial „Sf. Arhanghel Mihail și Sf. Sofian”", "Cuconeștii Vechi", "Sf. Arhanghel Mihail și Sf. Sofian", "", 12),
        ("md-bom-curchi-monastery-nativity-of-the-mother-of-god", "Monastery", "Nativity of the Mother of God Monastery in Curchi", "Mănăstirea „Naşterea Maicii Domnului”, Curchi", "Curchi", "Naşterea Maicii Domnului", "MD-3524, s. Curchi, r. Orhei", 1),
        ("md-bom-cuselauca-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Cușelăuca", "Mănăstirea “Adormirea Maicii Domnului”, Cușelăuca", "Cușelăuca", "Adormirea Maicii Domnului", "MD-7216, s. Cușelăuca, r. Șoldănești", 1),
        ("md-bom-dobrusa-monastery-saint-nicholas", "Monastery", "Saint Nicholas Monastery in Dobruşa", "Mănăstirea „Sf. Irh. Nicolae”, Dobruşa", "Dobruşa", "Sf. Irh. Nicolae", "MD-7219, s. Dobruşa, r. Şoldăneşti", 1),
        ("md-bom-durlesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Durlești", "Biserica „Sf. Arhanghel Mihail și Gavriil”", "Durlești", "Sf. Arhanghel Mihail și Gavriil", "MD-2003, mun. Chișinău, or. Durlești, str. Mateevici 8", 2),
        ("md-bom-floreni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Floreni", "Biserica „Acoperământul Maicii Domnului” - s. Floreni, r. Anenii Noi", "Floreni", "Acoperământul Maicii Domnului", "", 0),
        ("md-bom-ghermanesti-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Ghermănești", "Parohia „Nașterea Maicii Domnului” din satul Ghermănești", "Ghermănești", "Nașterea Maicii Domnului", "", 13),
        ("md-bom-hagimus-monastery-saints-martha-and-mary-the-myrrhbearers", "Monastery", "Saints Martha and Mary the Myrrhbearers Monastery in Hagimus", "Mănăstirea „Sf. Mironosite Marta și Maria”, Hagimus", "Hagimus", "Sf. Mironosite Marta și Maria", "MD-4319, c. Hagimus, r. Căuşeni", 1),
        ("md-bom-horesti-monastery-saint-prince-vladimir", "Monastery", "Saint Prince Vladimir Monastery in Horeşti", "Mănăstirea „Sf. Cneaz Vladimir”, Horeşti", "Horeşti", "Sf. Cneaz Vladimir", "MD-5911, com. Horeşti, r. Ialoveni", 1),
        ("md-bom-ialoveni-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Ialoveni", "parohia „Acoperământul Maicii Domnului” din orașul Ialoveni", "Ialoveni", "Acoperământul Maicii Domnului", "", 14),
        ("md-bom-lucaseuca-church-holy-trinity", "Church", "Holy Trinity Church in Lucașeuca", "Biserica „Sfânta Treime” - s. Lucașeuca, r. Orhei", "Lucașeuca", "Sfânta Treime", "", 0),
        ("md-bom-mereni-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Mereni", "Biserica „Sf. Arhangheli Mihail și Gavriil” - Mereni, r. Anenii Noi", "Mereni", "Sf. Arhangheli Mihail și Gavriil", "", 0),
        ("md-bom-odaia-church-saints-joachim-and-anna", "Church", "Saints Joachim and Anna Church in Odaia", "bisericii „Sfinții Părinți Ioachim și Ana” a schitului Odaia", "Odaia", "Sfinții Părinți Ioachim și Ana", "", 15),
        ("md-bom-odaia-skete-schitului-odaia", "Skete", "Odaia Skete", "schitului Odaia", "Odaia", "", "", 15),
        ("md-bom-olanesti-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Olănești", "Biserica „Sf. Cuv. Parascheva”", "Olănești", "Sf. Cuv. Parascheva", "MD-4226, s. Olănești, r. Ștefan Vodă", 2),
        ("md-bom-orhei-cathedral-saint-nicholas", "Cathedral", "Saint Nicholas Cathedral in Orhei", "Soborul „Sfântul Ierarh Nicolae” din orașul Orhei", "Orhei", "Sfântul Ierarh Nicolae", "", 16),
        ("md-bom-peresecina-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Peresecina", "bisericii „Sfântul Apostol și Evanghelist Ioan Teologul” din Peresecina", "Peresecina", "Sfântul Apostol și Evanghelist Ioan Teologul", "", 17),
        ("md-bom-rezina-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Rezina", "Biserica „Acoperământul Maicii Domnului”", "Rezina", "Acoperământul Maicii Domnului", "MD-5412, str. 27 august 21, or. Rezina", 2),
        ("md-bom-saharna-monastery-holy-trinity", "Monastery", "Holy Trinity Monastery in Saharna", "Mănăstirea „Sf. Treime”, Saharna", "Saharna", "Sf. Treime", "MD-5431, s. Saharna, r. Rezina", 1),
        ("md-bom-sangera-chapel-saint-nicholas", "Chapel", "Saint Nicholas Chapel in Sîngera", "paraclisului „Sfântul Ierarh Nicolae” din Sîngera", "Sîngera", "Sfântul Ierarh Nicolae", "", 18),
        ("md-bom-sipca-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Șipca", "Biserica „Acoperământul Maicii Domnului”", "Șipca", "Acoperământul Maicii Domnului", "MD-7216, s. Șipca, r. Șoldănești", 2),
        ("md-bom-sireti-monastery-saint-james-the-persian", "Monastery", "Saint James the Persian Monastery in Sireţi", "Mănăstirea „Sf. M. Mc. Iacob Persul”, Sireţi", "Sireţi", "Sf. M. Mc. Iacob Persul", "MD-3731, com. Sireţi, r. Străşeni", 1),
        ("md-bom-straseni-church-saint-nicholas", "Church", "Saint Nicholas Church in Strășeni", "biserica „Sfântul Ierarh Nicolae” din orașul Strășeni", "Strășeni", "Sfântul Ierarh Nicolae", "", 19),
        ("md-bom-suruceni-monastery-saint-george-the-great-martyr", "Monastery", "Saint George the Great Martyr Monastery in Suruceni", "Mănăstirea „Sf. M. Mc. Gheorghe”, Suruceni", "Suruceni", "Sf. M. Mc. Gheorghe", "MD-6827, com. Suruceni, r. Ialoveni", 1),
        ("md-bom-tapova-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Ţîpova", "Mănăstirea „Adormirea Maicii Domnului”, Ţîpova", "Ţîpova", "Adormirea Maicii Domnului", "MD-5421, s. Ţîpova, r. Rezina", 1),
        ("md-bom-tiganesti-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Ţigăneşti", "Mănăstirea „Adormirea Maicii Domnului”, Ţigăneşti", "Ţigăneşti", "Adormirea Maicii Domnului", "MD-3734, com. Ţigăneşti, r. Străşeni", 1),
        ("md-bom-vatici-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Vatici", "Biserica cu hramul „Acoperământul Maicii Domnului” din s. Vatici", "Vatici", "Acoperământul Maicii Domnului", "", 20),
        ("md-bom-zabriceni-monastery-nativity-of-christ", "Monastery", "Nativity of Christ Monastery in Zăbriceni", "Mănăstirea Stavropighială „Naşterea Domnului”, Zăbriceni", "Zăbriceni", "Naşterea Domnului", "MD-4646, s. Zăbriceni, r. Edineţ", 21),
        ("md-bom-zaicana-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Zăicana", "Biserica „Nașterea Maicii Domnului”", "Zăicana", "Nașterea Maicii Domnului", "s. Zăicana, r. Criuleni", 2),
    ),
    "ro-balti": (
        ("md-basarabia-balti-burlanesti-demetrius", "Parish", "Parish of Saint Demetrius the Myrrh-Streamer in Burlănești", "Parohia Ortodoxă Română „Sfântul Mare Mucenic Dimitrie, Izvorâtorul de Mir” din satul Burlănești", "Burlănești", "Sfântul Mare Mucenic Dimitrie, Izvorâtorul de Mir", "", 138),
        ("md-basarabia-balti-volovita-john", "Parish", "Parish of Saint John the New of Suceava in Volovița", "biserica „Sfântul Mare Mucenic Ioan cel Nou de la Suceava” din Voloviţa", "Volovița", "Sfântul Mare Mucenic Ioan cel Nou de la Suceava", "", 139),
        ("md-basarabia-balti-lipnic-archangels", "Parish", "Parish of the Holy Archangels Michael and Gabriel in Lipnic", "biserica „Sfinţii Arhangheli Mihail şi Gavriil” din satul Lipnic", "Lipnic", "Sfinţii Arhangheli Mihail şi Gavriil", "", 140),
        ("md-basarabia-balti-garbova-dormition", "Parish", "Dormition of the Mother of God Parish in Gârbova", "biserica „Adormirea Maicii Domnului ” din localitatea Gârbova", "Gârbova", "Adormirea Maicii Domnului", "", 141),
        ("md-basarabia-balti-glodeni-john-baptist", "Parish", "Saint John the Baptist Parish in Glodeni", "Parohia „Sfântul Prooroc Ioan Botezătorul” din orașul Glodeni", "Glodeni", "Sfântul Prooroc Ioan Botezătorul", "", 142),
        ("md-basarabia-balti-rautel-dormition", "Parish", "Dormition of the Mother of God Parish in Răuțel", "Parohia „Adormirea Maicii Domnului” din satul Răuțel", "Răuțel", "Adormirea Maicii Domnului", "", 143),
        ("md-basarabia-balti-sangerei-theodora", "Parish", "Saint Theodora of Sihla Parish in Sângerei", "parohia „Sfânta Cuvioasă Teodora de la Sihla” din or. Sângerei", "Sângerei", "Sfânta Cuvioasă Teodora de la Sihla", "", 144),
        ("md-basarabia-balti-varvareuca-sergius", "Parish", "Saint Sergius of Radonezh Parish in Vărvăreuca", "Comunitatea „Sfântul Serghie de Radonej” din Vărvăreuca", "Vărvăreuca", "Sfântul Serghie de Radonej", "", 145),
        ("md-basarabia-balti-balti-chapel-paraclisul-episcopal-din-municipiul-balti", "Chapel", "Episcopal Chapel in Bălți", "Paraclisul Episcopal din municipiul Bălți", "Bălți", "", "", 22),
        ("md-basarabia-balti-balti-church-nativity-of-christ", "Church", "Nativity of Christ Church in Bălţi", "biserica „Naşterea Domnului şi Mântuitorului nostru Iisus Hristos” din oraşul Bălţi", "Bălţi", "Naşterea Domnului şi Mântuitorului nostru Iisus Hristos", "", 23),
        ("md-basarabia-balti-chirilovca-monastery-nativity-of-the-mother-of-god-and-saint-george", "Monastery", "Nativity of the Mother of God and Saint George Monastery in Chirilovca", "Mănăstirea „Nașterea Maicii Domnului” și „Sfântul Mare Mucenic Gheorghe” din satul Chirilovca", "Chirilovca", "Nașterea Maicii Domnului” și „Sfântul Mare Mucenic Gheorghe", "", 24),
    ),
    "ro-chisinau": (
        ("md-basarabia-chisinau-durlesti-monastery-andrew", "Monastery", "Monastery of Saint Andrew the Apostle in Durlești", "Mănăstirea „Sfântul Apostol Andrei” din or. Durlești", "Durlești", "Sfântul Apostol Andrei", "", 136),
        ("md-basarabia-chisinau-soroca-brancoveanu-parish", "Parish", "Parish of the Brâncoveanu Martyrs in Soroca", "Parohia românească „Sfinții Martiri Brâncoveni” din Soroca", "Soroca", "Sfinții Martiri Brâncoveni", "", 137),
        ("md-basarabia-chisinau-alexeevca-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Alexeevca", "Biserica „Adormirea Maicii Domnului” - Alexeevca", "Alexeevca", "Adormirea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-bahu-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Bahu", "Biserica „Sf. M. Mc. Dimitrie” - Bahu", "Bahu", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-balabanesti-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Bălăbănești", "Biserica „Nașterea Maicii Domnului” - Bălăbănești", "Bălăbănești", "Nașterea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-boghenii-vechi-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Boghenii Vechi", "Biserica „Sf. Arh. Mihail și Gavriil” - Boghenii Vechi", "Boghenii Vechi", "Sf. Arh. Mihail și Gavriil", "", 25),
        ("md-basarabia-chisinau-bozieni-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Bozieni", "Biserica „Sf. Cuv. Parascheva” - Bozieni", "Bozieni", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-bubuieci-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Bubuieci", "Biserica „Acoperământul Maicii Domnului” - Bubuieci", "Bubuieci", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-calarasi-church-holy-trinity", "Church", "Holy Trinity Church in Călărași", "Biserica „Sfânta Treime” - Călărași", "Călărași", "Sfânta Treime", "", 25),
        ("md-basarabia-chisinau-calarasi-church-saint-john-the-merciful", "Church", "Saint John the Merciful Church in Călărași", "Biserica „Sf. Ioan cel Milostiv” - Călărași", "Călărași", "Sf. Ioan cel Milostiv", "", 25),
        ("md-basarabia-chisinau-calarasi-church-saint-nicholas", "Church", "Saint Nicholas Church in Călărași", "Biserica „Sf. Ier. Nicolae” (fosta Alexandru Nevski) - Călărași", "Călărași", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-calarasi-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Călărași", "Biserica „Sf. Cuv. Parascheva” - Călărași", "Călărași", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-calarasi-monastery-the-brancoveanu-martyrs", "Monastery", "The Brâncoveanu Martyrs Monastery in Călărași", "Mănăstirea „Sf. Martiri Brâncoveni” - Călărași", "Călărași", "Sf. Martiri Brâncoveni", "", 25),
        ("md-basarabia-chisinau-camencea-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Camencea", "Biserica „Sf. M. Mc. Gheorghe” - Camencea", "Camencea", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-carpineni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Cărpineni", "Biserica „Sf. M. Mc. Gheorghe” - Cărpineni", "Cărpineni", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-cetireni-church-saint-nicholas", "Church", "Saint Nicholas Church in Cetireni", "Biserica „Sf. Ier. Nicolae” - Cetireni", "Cetireni", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-chisinau-chapel-saint-john-the-theologian", "Chapel", "Saint John the Theologian Chapel in Chișinău", "Paraclisul Mitropolitan „Sf. Ioan Teologul” - Chișinău", "Chișinău", "Sf. Ioan Teologul", "", 25),
        ("md-basarabia-chisinau-chisinau-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Chișinău", "Biserica „Sf. Apostoli Petru și Pavel” - Chișinău", "Chișinău", "Sf. Apostoli Petru și Pavel", "", 25),
        ("md-basarabia-chisinau-chisinau-church-holy-archangels-michael-and-gabriel-and-saint-valerius", "Church", "Holy Archangels Michael and Gabriel and Saint Valerius Church in Chișinău", "Biserica „Sf. Arh. Mihail și Gavriil și Sf. Mc. Valerie” - Chișinău", "Chișinău", "Sf. Arh. Mihail și Gavriil și Sf. Mc. Valerie", "", 25),
        ("md-basarabia-chisinau-chisinau-church-holy-trinity", "Church", "Holy Trinity Church in Chișinău", "Biserica „Sf. Treime” (Liceul Prometeu) - Chișinău", "Chișinău", "Sf. Treime", "", 25),
        ("md-basarabia-chisinau-chisinau-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Chișinău", "Biserica „Sf. M. Mc. Gheorghe” - Chișinău", "Chișinău", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-chisinau-church-saint-gregory-palamas", "Church", "Saint Gregory Palamas Church in Chișinău", "Biserica „Sf. Ier. Grigorie Palama” - Chișinău", "Chișinău", "Sf. Ier. Grigorie Palama", "", 25),
        ("md-basarabia-chisinau-chisinau-church-saint-john-jacob-the-chozebite", "Church", "Saint John Jacob the Chozebite Church in Chișinău", "Biserica „Sf. Ioan Iacob Hozevitul” - Chișinău", "Chișinău", "Sf. Ioan Iacob Hozevitul", "", 25),
        ("md-basarabia-chisinau-chisinau-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Chișinău", "Biserica „Sf. Cuv. Parascheva” - Chișinău", "Chișinău", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-chisinau-church-saints-george-and-stylianos", "Church", "Saints George and Stylianos Church in Chișinău", "Biserica „Sf. M. Mc. Gheorghe și Sf. Cuv. Stelian” - Chișinău", "Chișinău", "Sf. M. Mc. Gheorghe și Sf. Cuv. Stelian", "", 25),
        ("md-basarabia-chisinau-chisinau-church-saints-spyridon-and-seraphim-of-sarov", "Church", "Saints Spyridon and Seraphim of Sarov Church in Chișinău", "Biserica „Sf. Ier. Spiridon și Sf. Serafim de Sarov” - Chișinău", "Chișinău", "Sf. Ier. Spiridon și Sf. Serafim de Sarov", "", 25),
        ("md-basarabia-chisinau-chisinau-church-three-holy-hierarchs", "Church", "Three Holy Hierarchs Church in Chișinău", "Biserica „Sf. Trei Ierarhi” - Chișinău", "Chișinău", "Sf. Trei Ierarhi", "", 26),
        ("md-basarabia-chisinau-cimiseni-church-saints-constantine-and-helen", "Church", "Saints Constantine and Helen Church in Cimișeni", "Biserica „Sf. Împ. Constantin și Elena” - Cimișeni", "Cimișeni", "Sf. Împ. Constantin și Elena", "", 27),
        ("md-basarabia-chisinau-ciorescu-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Ciorescu", "Biserica „Sf. Cuv. Parascheva” - Ciorescu", "Ciorescu", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-codru-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Codru", "Biserica „Adormirea Maicii Domnului” - Codru", "Codru", "Adormirea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-codru-church-the-brancoveanu-martyrs", "Church", "The Brâncoveanu Martyrs Church in Codru", "Biserica „Sf. Martiri Brâncoveni” - Codru", "Codru", "Sf. Martiri Brâncoveni", "", 25),
        ("md-basarabia-chisinau-cornesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Cornești", "Biserica „Sf. Arh. Mihail și Gavriil” - sat. Cornești", "Cornești", "Sf. Arh. Mihail și Gavriil", "", 25),
        ("md-basarabia-chisinau-cornesti-church-saint-arsenios-the-great", "Church", "Saint Arsenios the Great Church in Cornești", "Biserica „Sf. Arsenie cel Mare” - Cornești", "Cornești", "Sf. Arsenie cel Mare", "", 25),
        ("md-basarabia-chisinau-cornesti-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Cornești", "Biserica „Sf. M. Mc. Gheorghe” - Cornești", "Cornești", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-cornova-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Cornova", "Biserica „Sf. M. Mc. Gheorghe” - Cornova", "Cornova", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-coseni-church-holy-trinity", "Church", "Holy Trinity Church in Coșeni", "Biserica „Sf. Treime” - Coșeni", "Coșeni", "Sf. Treime", "", 25),
        ("md-basarabia-chisinau-costesti-church-three-holy-hierarchs", "Church", "Three Holy Hierarchs Church in Costești", "Biserica „Sf. Trei Ierarhi” - Costești", "Costești", "Sf. Trei Ierarhi", "", 25),
        ("md-basarabia-chisinau-costuleni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Costuleni", "Biserica „Sf. M. Mc. Dimitrie\" - Costuleni", "Costuleni", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-costuleni-skete-saints-adrian-and-natalia", "Skete", "Saints Adrian and Natalia Skete in Costuleni", "Schitul „Sf. M. Mc. Adrian și Natalia” - Costuleni", "Costuleni", "Sf. M. Mc. Adrian și Natalia", "", 25),
        ("md-basarabia-chisinau-crasnoarmeiscoe-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Crasnoarmeiscoe", "Biserica „Sf. M. Mc. Dimitrie” - Crasnoarmeiscoe", "Crasnoarmeiscoe", "Sf. M. Mc. Dimitrie", "", 28),
        ("md-basarabia-chisinau-cricova-church-saint-alexander-of-svir", "Church", "Saint Alexander of Svir Church in Cricova", "Biserica „Sf. Alexandru din Svir” - Cricova", "Cricova", "Sf. Alexandru din Svir", "", 25),
        ("md-basarabia-chisinau-dereneu-chapel-saint-nectarius", "Chapel", "Saint Nectarius Chapel in Dereneu", "Paraclisului „Sfântul Ierarh Nectarie” din Dereneu", "Dereneu", "Sfântul Ierarh Nectarie", "", 29),
        ("md-basarabia-chisinau-dereneu-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Dereneu", "Biserica „Adormirea Maicii Domnului” - Dereneu", "Dereneu", "Adormirea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-draguseni-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Drăgușeni", "Biserica „Sf. Arh. Mihail și Gavriil” - Drăgușeni", "Drăgușeni", "Sf. Arh. Mihail și Gavriil", "", 25),
        ("md-basarabia-chisinau-drujba-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Drujba", "Biserica „Sf. M. Mc. Gheorghe” - Drujba", "Drujba", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-dubasarii-vechi-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Dubăsarii Vechi", "Biserica „Sf. Arh. Mihail și Gavriil” - Dubăsarii Vechi", "Dubăsarii Vechi", "Sf. Arh. Mihail și Gavriil", "", 25),
        ("md-basarabia-chisinau-elizavetovca-church-saints-luke-of-crimea-and-dionysius-of-cetatea-alba-and-ismail", "Church", "Saints Luke of Crimea and Dionysius of Cetatea Albă and Ismail Church in Elizavetovca", "Biserica „Sf. Ier. Luca al Crimeii și Sf. Ier. Dionisie al Cetății Albe-Ismail” - Elizavetovca", "Elizavetovca", "Sf. Ier. Luca al Crimeii și Sf. Ier. Dionisie al Cetății Albe-Ismail", "", 25),
        ("md-basarabia-chisinau-floreni-church-saint-seraphim-of-sarov", "Church", "Saint Seraphim of Sarov Church in Floreni", "Biserica „Sf. Cuv. Serafim de Sarov” - Floreni", "Floreni", "Sf. Cuv. Serafim de Sarov", "", 25),
        ("md-basarabia-chisinau-floritoaia-veche-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Florițoaia Veche", "Biserica „Sf. M. Mc. Dimitrie” - Florițoaia Veche", "Florițoaia Veche", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-ghidighici-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Ghidighici", "Biserica „Acoperământul Maicii Domnului” - Ghidighici", "Ghidighici", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-ghiduleni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Ghiduleni", "Biserica „Sf. M. Mc. Dimitrie” - Ghiduleni", "Ghiduleni", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-ghiliceni-church-saints-constantine-and-helen", "Church", "Saints Constantine and Helen Church in Ghiliceni", "Biserica „Sf. Împ. Constantin și Elena” - Ghiliceni", "Ghiliceni", "Sf. Împ. Constantin și Elena", "", 25),
        ("md-basarabia-chisinau-hancesti-church-synaxis-of-the-holy-voivodes", "Church", "Synaxis of the Holy Voivodes Church in Hâncești", "Biserica „Soborul Sfinților Mari Voievozi” - Hâncești", "Hâncești", "Soborul Sfinților Mari Voievozi", "", 25),
        ("md-basarabia-chisinau-hristoforovca-monastery-saint-paraskeva", "Monastery", "Saint Paraskeva Monastery in Hristoforovca", "Mănăstirea „Sf. Cuv. Parascheva” - Hristoforovca", "Hristoforovca", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-humulesti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Humulești", "Biserica „Acoperământul Maicii Domnului” - Humulești", "Humulești", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-ialoveni-church-the-brancoveanu-martyrs", "Church", "The Brâncoveanu Martyrs Church in Ialoveni", "Biserica „Sf. Martiri Brâncoveni” - Ialoveni", "Ialoveni", "Sf. Martiri Brâncoveni", "", 30),
        ("md-basarabia-chisinau-inesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Inești", "Biserica „Sf. Arh. Mihail și Gavriil” - Inești", "Inești", "Sf. Arh. Mihail și Gavriil", "", 25),
        ("md-basarabia-chisinau-ip-capsuna-church-saints-faith-hope-love-and-their-mother-sophia", "Church", "Saints Faith, Hope, Love and their mother Sophia Church in IP Căpșuna", "Biserica „Sf. Mc. Vera, Nadejda, Liubovi și mama lor, Sofia” - IP Căpșuna", "IP Căpșuna", "Sf. Mc. Vera, Nadejda, Liubovi și mama lor, Sofia", "", 31),
        ("md-basarabia-chisinau-isnovat-church-saint-nicholas", "Church", "Saint Nicholas Church in Ișnovăț", "Biserica „Sf. Ier. Nicolae” - Ișnovăț", "Ișnovăț", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-jeloboc-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Jeloboc", "Biserica „Sf. Cuv. Parascheva” - Jeloboc", "Jeloboc", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-magdacesti-church-saint-nicholas", "Church", "Saint Nicholas Church in Măgdăcești", "Biserica „Sf. Ier. Nicolae” - Măgdăcești", "Măgdăcești", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-malaiestii-noi-church-saint-demetrius", "Church", "Saint Demetrius Church in Mălăieștii Noi", "Biserica „Sf. Mc. Dimitrie” - Mălăieștii Noi", "Mălăieștii Noi", "Sf. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-mardareuca-church-archangel-michael", "Church", "Archangel Michael Church in Mărdăreuca", "Biserica „Sf. Arh. Mihail” - Mărdăreuca", "Mărdăreuca", "Sf. Arh. Mihail", "", 25),
        ("md-basarabia-chisinau-medeleni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Medeleni", "Biserica „Sf. M. Mc. Gheorghe” - Medeleni", "Medeleni", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-miclesti-church-saint-spyridon-of-trimythous", "Church", "Saint Spyridon of Trimythous Church in Miclești", "Biserica „Sf. Ier. Spiridon” - Miclești", "Miclești", "Sf. Ier. Spiridon", "", 25),
        ("md-basarabia-chisinau-mihalasa-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Mihalașa", "Biserica „Nașterea Maicii Domnului” - Mihalașa", "Mihalașa", "Nașterea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-morenii-vechi-church-holy-trinity", "Church", "Holy Trinity Church in Morenii Vechi", "Biserica „Sfânta Treime” - Morenii Vechi", "Morenii Vechi", "Sfânta Treime", "", 25),
        ("md-basarabia-chisinau-napadeni-church-saint-nicholas", "Church", "Saint Nicholas Church in Năpădeni", "Biserica „Sf. Ier. Nicolae” - Năpădeni", "Năpădeni", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-novaia-nicolaevca-skete-saint-nicholas", "Skete", "Saint Nicholas Skete in Novaia Nicolaevca", "Schitul „Sf. Ier. Nicolae” - Novaia Nicolaevca", "Novaia Nicolaevca", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-orhei-church-saint-basil-of-poiana-marului", "Church", "Saint Basil of Poiana Mărului Church in Orhei", "Biserica „Sf. Vasile de la Poiana Mărului” - Orhei", "Orhei", "Sf. Vasile de la Poiana Mărului", "", 25),
        ("md-basarabia-chisinau-orhei-church-saint-varlaam-metropolitan-of-moldavia", "Church", "Saint Varlaam, Metropolitan of Moldavia Church in Orhei", "Biserica „Sf. Ier. Varlaam, Mitropolitul Moldovei” - Orhei", "Orhei", "Sf. Ier. Varlaam, Mitropolitul Moldovei", "", 25),
        ("md-basarabia-chisinau-peresecina-church-saint-nicholas", "Church", "Saint Nicholas Church in Peresecina", "Biserica „Sf. Ier. Nicolae” - Peresecina", "Peresecina", "Sf. Ier. Nicolae", "", 32),
        ("md-basarabia-chisinau-peticeni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Peticeni", "Biserica „Sf. M. Mc. Dimitrie” - Peticeni", "Peticeni", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-pocsesti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Pocșești", "Biserica „Acoperământul Maicii Domnului” - Pocșești", "Pocșești", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-pojareni-church-saint-nicholas", "Church", "Saint Nicholas Church in Pojăreni", "Biserica „Sf. Ierarh Nicolae” - Pojăreni", "Pojăreni", "Sf. Ierarh Nicolae", "", 25),
        ("md-basarabia-chisinau-radenii-vechi-church-holy-trinity", "Church", "Holy Trinity Church in Rădenii Vechi", "Biserica „Sf. Treime” - Rădenii Vechi", "Rădenii Vechi", "Sf. Treime", "", 25),
        ("md-basarabia-chisinau-ratus-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Ratuș", "Biserica „Sf. Cuv. Parascheva” - Ratuș", "Ratuș", "Sf. Cuv. Parascheva", "", 25),
        ("md-basarabia-chisinau-rezina-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Rezina", "Biserica „Înălțarea Domnului” - Rezina", "Rezina", "Înălțarea Domnului", "", 25),
        ("md-basarabia-chisinau-rezina-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Rezina", "Biserica „Sf. M. Mc. Gheorghe” - Rezina", "Rezina", "Sf. M. Mc. Gheorghe", "", 25),
        ("md-basarabia-chisinau-romanovca-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Romanovca", "Biserica „Acoperământul Maicii Domnului” - Romanovca", "Romanovca", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-roscani-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Roșcani", "Biserica „Sf. M. Mc. Dimitrie” - Roșcani", "Roșcani", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-sadova-church-saint-nicholas", "Church", "Saint Nicholas Church in Sadova", "Biserica „Sf. Ier. Nicolae” - Sadova", "Sadova", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-saseni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Săseni", "Biserica „Acoperământul Maicii Domnului” - Săseni", "Săseni", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-sculeni-church-annunciation", "Church", "Annunciation Church in Sculeni", "Biserica „Buna Vestire” - Sculeni", "Sculeni", "Buna Vestire", "", 25),
        ("md-basarabia-chisinau-sinesti-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Sinești", "Biserica „Nașterea Maicii Domnului” - Sinești", "Sinești", "Nașterea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-stauceni-church-saints-john-the-new-of-suceava-and-katherine", "Church", "Saints John the New of Suceava and Katherine Church in Stăuceni", "Biserica „Sf. Ioan cel Nou de la Suceava și Sf. M. Ecaterina” - Stăuceni", "Stăuceni", "Sf. Ioan cel Nou de la Suceava și Sf. M. Ecaterina", "", 25),
        ("md-basarabia-chisinau-stolniceni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Stolniceni", "Biserica „Acoperământul Maicii Domnului” - Stolniceni", "Stolniceni", "Acoperământul Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-stolniceni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Stolniceni", "Biserica „Sf. M. Mc. Dimitrie” - Stolniceni", "Stolniceni", "Sf. M. Mc. Dimitrie", "", 25),
        ("md-basarabia-chisinau-straseni-church-saint-andrew-the-apostle", "Church", "Saint Andrew the Apostle Church in Strășeni", "Biserica „Sf. Ap. Andrei” - or. Strășeni", "Strășeni", "Sf. Ap. Andrei", "", 25),
        ("md-basarabia-chisinau-taghira-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Țîghira", "Biserica „Acoperământul Maici Domnului” - Țîghira", "Țîghira", "Acoperământul Maici Domnului", "", 25),
        ("md-basarabia-chisinau-telenesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Telenești", "Biserica „Adormirea Maicii Domnului” - Telenești", "Telenești", "Adormirea Maicii Domnului", "", 25),
        ("md-basarabia-chisinau-tescureni-monastery-prophet-elijah", "Monastery", "Prophet Elijah Monastery in Teșcureni", "Mănăstirea „Sf. Prooroc Ilie Tesviteanul\" - Teșcureni", "Teșcureni", "Sf. Prooroc Ilie Tesviteanul", "", 25),
        ("md-basarabia-chisinau-ulmu-monastery-saint-theodora-of-sihla", "Monastery", "Saint Theodora of Sihla Monastery in Ulmu", "Mănăstirea „Sf. Cuv. Teodora de la Sihla\" - Ulmu", "Ulmu", "Sf. Cuv. Teodora de la Sihla", "", 25),
        ("md-basarabia-chisinau-ungheni-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Ungheni", "Biserica „Înălțarea Domnului” - Ungheni", "Ungheni", "Înălțarea Domnului", "", 25),
        ("md-basarabia-chisinau-ungheni-church-saint-andrew-the-apostle", "Church", "Saint Andrew the Apostle Church in Ungheni", "Biserica „Sf. Apostol Andrei” - Ungheni", "Ungheni", "Sf. Apostol Andrei", "", 25),
        ("md-basarabia-chisinau-ungheni-church-saint-joseph-the-merciful", "Church", "Saint Joseph the Merciful Church in Ungheni", "Biserica „Sf. Ier. Iosif cel Milostiv” - Ungheni", "Ungheni", "Sf. Ier. Iosif cel Milostiv", "", 25),
        ("md-basarabia-chisinau-ungheni-church-saint-nicholas", "Church", "Saint Nicholas Church in Ungheni", "Biserica „Sf. Ier. Nicolae” - Ungheni", "Ungheni", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-vadul-leca-church-saint-nicholas", "Church", "Saint Nicholas Church in Vadul-Leca", "Biserica „Sf. Ier. Nicolae” - Vadul-Leca", "Vadul-Leca", "Sf. Ier. Nicolae", "", 25),
        ("md-basarabia-chisinau-valcinet-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Vălcineț", "Biserica „Acoperământul Maicii Domnului” - Vălcineț", "Vălcineț", "Acoperământul Maicii Domnului", "", 25),
    ),
    "ro-south-bessarabia": (
        ("md-basarabia-sud-alexandru-ioan-cuza-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Alexandru Ioan Cuza", "Parohia Sf. Ier. Nicolae - Alexandru Ioan Cuza", "Alexandru Ioan Cuza", "Sf. Ier. Nicolae", "", 34),
        ("md-basarabia-sud-antonesti-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Antonești", "Parohia Sf. Ier. Nicolae - Antonești", "Antonești", "Sf. Ier. Nicolae", "", 35),
        ("md-basarabia-sud-badicul-moldovenesc-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Badicul Moldovenesc", "Parohia Sf. Arhangheli Mihail și Gavriil - Badicul Moldovenesc", "Badicul Moldovenesc", "Sf. Arhangheli Mihail și Gavriil", "", 36),
        ("md-basarabia-sud-batar-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Batîr", "Parohia Sfinții Arhangheli Mihail și Gavriil - Batîr", "Batîr", "Sfinții Arhangheli Mihail și Gavriil", "", 37),
        ("md-basarabia-sud-baurci-moldoveni-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Baurci Moldoveni", "Parohia Sf. Cuv. Parascheva - Baurci Moldoveni", "Baurci Moldoveni", "Sf. Cuv. Parascheva", "", 38),
        ("md-basarabia-sud-cahul-cathedral-dionysius", "Cathedral", "Cathedral of Saint Dionysius in Cahul", "Catedrala Sfântul Ierarh Dionisie", "Cahul", "Sfântul Ierarh Dionisie", "", 39),
        ("md-basarabia-sud-cahul-chapel-resurrection-of-the-lord", "Chapel", "Resurrection of the Lord Chapel in Cahul", "Paraclisul \"Învierea Domnului\" - Centrul Eparhial Cahul", "Cahul", "Învierea Domnului", "str. B.P Hasdeu 11A", 40),
        ("md-basarabia-sud-cahul-parish-saint-demetrius", "Parish", "Saint Demetrius Parish in Cahul", "Parohia Sf. Dumitru - Cahul", "Cahul", "Sf. Dumitru", "", 41),
        ("md-basarabia-sud-cahul-parish-saint-panteleimon", "Parish", "Saint Panteleimon Parish in Cahul", "Parohia Sf. M. Mc. Pantelimon - Cahul", "Cahul", "Sf. M. Mc. Pantelimon", "", 42),
        ("md-basarabia-sud-cania-parish-sunday-of-all-romanian-saints", "Parish", "Sunday of All Romanian Saints Parish in Cania", "Parohia Duminica Tuturor Sfinților Români, Cania", "Cania", "Duminica Tuturor Sfinților Români", "", 43),
        ("md-basarabia-sud-causeni-parish-nativity-of-saint-john-the-baptist", "Parish", "Nativity of Saint John the Baptist Parish in Căușeni", "Parohia Nașterea Sfântului Proroc Ioan Botezătorul - Căușeni", "Căușeni", "Nașterea Sfântului Proroc Ioan Botezătorul", "", 44),
        ("md-basarabia-sud-causeni-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Căușeni", "Parohia Acoperământul Maicii Domnului - Căușeni", "Căușeni", "Acoperământul Maicii Domnului", "", 45),
        ("md-basarabia-sud-causeni-parish-the-brancoveanu-martyrs", "Parish", "The Brâncoveanu Martyrs Parish in Căușeni", "Parohia Sfinții Martiri Brâncoveni - Căușeni", "Căușeni", "Sfinții Martiri Brâncoveni", "", 46),
        ("md-basarabia-sud-cenac-parish-translation-of-the-relics-of-saint-nicholas", "Parish", "Translation of the Relics of Saint Nicholas Parish in Cenac", "Parohia Aducerea moaștelor Sf. Ier. Nicolae - Cenac", "Cenac", "Aducerea moaștelor Sf. Ier. Nicolae", "", 47),
        ("md-basarabia-sud-chioselia-mare-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Chioselia Mare", "Parohia Sf. Cuv. Parascheva - Chioselia Mare", "Chioselia Mare", "Sf. Cuv. Parascheva", "", 48),
        ("md-basarabia-sud-chircani-parish-prophet-elijah", "Parish", "Prophet Elijah Parish in Chircani", "Parohia Sf. Proroc Ilie - Chircani", "Chircani", "Sf. Proroc Ilie", "", 49),
        ("md-basarabia-sud-cimislia-parish-saints-nicholas-and-eudocia", "Parish", "Saints Nicholas and Eudocia Parish in Cimișlia", "Parohia Sf. Ier. Nicolae și Sf. Cuv Mc. Evdochia - Cimișlia", "Cimișlia", "Sf. Ier. Nicolae și Sf. Cuv Mc. Evdochia", "", 50),
        ("md-basarabia-sud-ciucur-mingir-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Ciucur Mingir", "Parohia Sfinții Arhangheli Mihail și Gavriil - Ciucur Mingir", "Ciucur Mingir", "Sfinții Arhangheli Mihail și Gavriil", "", 51),
        ("md-basarabia-sud-coscalia-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Coșcalia", "Parohia Sfinții Arhangheli Mihail și Gavriil - Coșcalia", "Coșcalia", "Sfinții Arhangheli Mihail și Gavriil", "", 52),
        ("md-basarabia-sud-cotihana-parish-saint-george-the-great-martyr", "Parish", "Saint George the Great Martyr Parish in Cotihana", "Parohia Sf. M. Mc. Gheorghe - Cotihana", "Cotihana", "Sf. M. Mc. Gheorghe", "", 53),
        ("md-basarabia-sud-cucoara-parish-dormition-of-the-mother-of-god-and-saint-andrei-saguna", "Parish", "Dormition of the Mother of God and Saint Andrei Șaguna Parish in Cucoara", "Parohia Adormirea Maicii Domnului și Sfântul Ierarh Andrei Șaguna - Cucoara", "Cucoara", "Adormirea Maicii Domnului și Sfântul Ierarh Andrei Șaguna", "", 54),
        ("md-basarabia-sud-cupcui-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Cupcui", "Parohia Sf. Ier. Nicolae - Cupcui", "Cupcui", "Sf. Ier. Nicolae", "", 55),
        ("md-basarabia-sud-doina-parish-saint-panteleimon", "Parish", "Saint Panteleimon Parish in Doina", "Parohia Sf. M. Mc. Pantelimon - Doina", "Doina", "Sf. M. Mc. Pantelimon", "", 56),
        ("md-basarabia-sud-festelita-parish-saint-john-the-new-of-suceava", "Parish", "Saint John the New of Suceava Parish in Feștelița", "Parohia Sf. Ioan cel Nou de la Suceava - Feștelița", "Feștelița", "Sf. Ioan cel Nou de la Suceava", "", 57),
        ("md-basarabia-sud-filipeni-parish-saints-constantine-and-helen", "Parish", "Saints Constantine and Helen Parish in Filipeni", "Parohia Sfinții Împărați Constantin și Elena, Filipeni", "Filipeni", "Sfinții Împărați Constantin și Elena", "", 58),
        ("md-basarabia-sud-gavanoasa-monastery-descent-of-the-holy-spirit", "Monastery", "Descent of the Holy Spirit Monastery in Găvănoasa", "Mănăstirea \"Pogorârea Sfântului Duh\" - Găvănoasa", "Găvănoasa", "Pogorârea Sfântului Duh", "", 59),
        ("md-basarabia-sud-gavanoasa-parish-saints-constantine-and-helen", "Parish", "Saints Constantine and Helen Parish in Găvănoasa", "Parohia Sf. Împ. Constantin și Elena - Găvănoasa", "Găvănoasa", "Sf. Împ. Constantin și Elena", "", 60),
        ("md-basarabia-sud-ghioltosu-parish-saints-joachim-anna-and-irodion-of-lainici", "Parish", "Saints Joachim, Anna and Irodion of Lainici Parish in Ghioltosu", "Parohia Sfinții Părinți Ioachim și Ana și Sf. Cuv. Irodion de la Lainici - Ghioltosu", "Ghioltosu", "Sfinții Părinți Ioachim și Ana și Sf. Cuv. Irodion de la Lainici", "", 61),
        ("md-basarabia-sud-giurgiulesti-parish-resurrection-of-the-lord-and-saint-george", "Parish", "Resurrection of the Lord and Saint George Parish in Giurgiulești", "Parohia Învierea Domnului și Sf. M. Mc. Gheorghe - Giurgiulești", "Giurgiulești", "Învierea Domnului și Sf. M. Mc. Gheorghe", "", 62),
        ("md-basarabia-sud-gotesti-parish-saint-demetrius-the-new", "Parish", "Saint Demetrius the New Parish in Gotești", "Parohia Sf. Cuv. Dimitrie cel Nou - Gotești", "Gotești", "Sf. Cuv. Dimitrie cel Nou", "", 63),
        ("md-basarabia-sud-hagimus-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Hagimus", "Parohia Nașterea Maicii Domnului - Hagimus", "Hagimus", "Nașterea Maicii Domnului", "", 64),
        ("md-basarabia-sud-ialpujeni-parish-translation-of-the-relics-of-saint-nicholas", "Parish", "Translation of the Relics of Saint Nicholas Parish in Ialpujeni", "Parohia Aducerea Moaștelor Sf. Ier, Nicolae - Ialpujeni", "Ialpujeni", "Aducerea Moaștelor Sf. Ier, Nicolae", "", 65),
        ("md-basarabia-sud-javgur-parish-saints-joachim-and-anna", "Parish", "Saints Joachim and Anna Parish in Javgur", "Parohia Sfinții Părinți Ioachim și Ana - Javgur", "Javgur", "Sfinții Părinți Ioachim și Ana", "", 66),
        ("md-basarabia-sud-larga-noua-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Larga Nouă", "Parohia Sf. Ier. Nicolae - Larga Nouă", "Larga Nouă", "Sf. Ier. Nicolae", "", 67),
        ("md-basarabia-sud-leova-i-parish-saint-john-the-baptist", "Parish", "Saint John the Baptist Parish in Leova I", "Parohia Sf. Ioan Botezătorul - Leova I", "Leova I", "Sf. Ioan Botezătorul", "", 68),
        ("md-basarabia-sud-leova-ii-parish-saint-luke-of-crimea", "Parish", "Saint Luke of Crimea Parish in Leova II", "Parohia Sf. Ier, Luca al Crimeei, Leova II", "Leova II", "Sf. Ier, Luca al Crimeei", "", 69),
        ("md-basarabia-sud-manta-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Manta", "Parohia Sf. Arhangheli Mihail și Gavriil - Manta", "Manta", "Sf. Arhangheli Mihail și Gavriil", "", 70),
        ("md-basarabia-sud-palanca-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Palanca", "Parohia Nașterea Maicii Domnului - Palanca", "Palanca", "Nașterea Maicii Domnului", "", 71),
        ("md-basarabia-sud-pascani-parish-life-giving-spring", "Parish", "Life-Giving Spring Parish in Pașcani", "Parohia Izvorul Tămăduirii - Pașcani", "Pașcani", "Izvorul Tămăduirii", "", 72),
        ("md-basarabia-sud-porumbesti-parish-descent-of-the-holy-spirit", "Parish", "Descent of the Holy Spirit Parish in Porumbești", "Parohia Pogorârea Sfântului Duh - Porumbești", "Porumbești", "Pogorârea Sfântului Duh", "", 73),
        ("md-basarabia-sud-rosu-monastery-holy-trinity", "Monastery", "Holy Trinity Monastery in Roșu", "Mănăstirea \"Sfânta Treime\" Roșu", "Roșu", "Sfânta Treime", "", 74),
        ("md-basarabia-sud-rosu-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Roșu", "Parohia Sf. M. Mc Dimitrie - Roșu", "Roșu", "Sf. M. Mc Dimitrie", "", 75),
        ("md-basarabia-sud-slobozia-mare-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Slobozia Mare", "Parohia Sf. Arhangheli Mihail și Gavriil - Slobozia Mare", "Slobozia Mare", "Sf. Arhangheli Mihail și Gavriil", "", 76),
        ("md-basarabia-sud-stefan-voda-parish-saint-stephen-the-great", "Parish", "Saint Stephen the Great Parish in Ștefan Vodă", "Parohia Binecredinciosul Voievod Ștefan cel Mare și Sfânt - Ștefan Vodă", "Ștefan Vodă", "Binecredinciosul Voievod Ștefan cel Mare și Sfânt", "", 77),
        ("md-basarabia-sud-stoianovca-monastery-ascension-of-the-lord", "Monastery", "Ascension of the Lord Monastery in Stoianovca", "Mănăstirea Eroilor cu hramul \"Înălțarea Domnului\" Stoianovca", "Stoianovca", "Înălțarea Domnului", "", 78),
        ("md-basarabia-sud-taraclia-de-salcie-parish-saint-george-the-great-martyr", "Parish", "Saint George the Great Martyr Parish in Taraclia de Salcie", "Parohia Sf. M. Mc. Gheorghe - Taraclia de Salcie", "Taraclia de Salcie", "Sf. M. Mc. Gheorghe", "", 79),
        ("md-basarabia-sud-toceni-parish-prophet-elijah", "Parish", "Prophet Elijah Parish in Toceni", "Parohia Sf. Proroc Ilie - Toceni", "Toceni", "Sf. Proroc Ilie", "", 80),
        ("md-basarabia-sud-ucrainca-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Ucrainca", "Parohia Nașterea Maicii Domnului - Ucrainca", "Ucrainca", "Nașterea Maicii Domnului", "", 81),
        ("md-basarabia-sud-ursoaia-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Ursoaia", "Parohia Sf. Ier. Nicolae - Ursoaia", "Ursoaia", "Sf. Ier. Nicolae", "", 82),
        ("md-basarabia-sud-vadul-lui-isac-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Vadul lui Isac", "Parohia Sf. Arhangheli Mihail și Gavriil - Vadul lui Isac", "Vadul lui Isac", "Sf. Arhangheli Mihail și Gavriil", "", 83),
    ),
    "ru-balti": (
        ("md-bom-balti-balti-paraskeva", "Church", "Saint Paraskeva Church in Bălți", "biserica «Cuv.Parascheva»", "Bălți", "Cuv.Parascheva", "", 146),
        ("md-bom-balti-singerei-archangels", "Church", "Holy Archangels Michael and Gabriel Church in Sîngerei", "bisericii «Sf.Arh.Mihail şi Gavriil», or.Sîngerei", "Sîngerei", "Sf.Arh.Mihail şi Gavriil", "", 147),
        ("md-bom-balti-singerei-george", "Church", "Saint George the Great Martyr Church in Sîngerei", "bisericii «Sf.M.Mc.Gheorghe», or.Sîngerei", "Sîngerei", "Sf.M.Mc.Gheorghe", "", 148),
        ("md-bom-balti-balti-mina", "Church", "Saint Menas Church in Bălți", "Sf. M. Mc. Mina", "Bălți", "Sf. M. Mc. Mina", "", 149),
        ("md-bom-balti-balti-trinity", "Church", "Holy Trinity Church in Bălți", "Sf. Treime", "Bălți", "Sf. Treime", "", 150),
        ("md-bom-balti-balti-panteleimon", "Church", "Saint Panteleimon Church in Bălți", "Sf. Pantelimon", "Bălți", "Sf. Pantelimon", "", 151),
        ("md-bom-balti-balti-cathedral-saint-nicholas", "Cathedral", "Saint Nicholas Cathedral in Bălți", "catedrala „Sf.Ier.Nicolae” din Bălți", "Bălți", "Sf.Ier.Nicolae", "", 84),
        ("md-bom-balti-balti-cathedral-saints-constantine-and-helen", "Cathedral", "Saints Constantine and Helen Cathedral in Bălți", "Catedrala episcopală „Sfinții Împărați Constantin și Elena”", "Bălți", "Sfinții Împărați Constantin și Elena", "", 85),
        ("md-bom-balti-balti-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Bălți", "bisericii „Sf. Ap. Petru și Pavel” din Bălți", "Bălți", "Sf. Ap. Petru și Pavel", "", 86),
        ("md-bom-balti-bocancea-monastery-apostles-peter-and-paul", "Monastery", "Apostles Peter and Paul Monastery in Bocancea", "Mănăstirea „Sf. Ap. Petru şi Pavel”, Bocancea", "Bocancea", "Sf. Ap. Petru şi Pavel", "MD-6224 s. Bocancea-Schit, r. Sîngerei", 1),
        ("md-bom-balti-calinesti-skete-protection-of-the-mother-of-god", "Skete", "Protection of the Mother of God Skete in Călineşti", "Schitul “Acoprerământul Maicii Domnului”, Călineşti", "Călineşti", "Acoprerământul Maicii Domnului", "MD-5913 com. Călineşti, r. Făleşti", 1),
        ("md-bom-balti-coada-iazului-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Coada Iazului", "Mănăstirea “Adormirea Maicii Domnului”, Coada Iazului", "Coada Iazului", "Adormirea Maicii Domnului", "MD-6214, s. Coada Iazului, r. Sângerei", 1),
        ("md-bom-balti-cobani-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Cobani", "parohia „Sf.Arh.Mihail și Gavriil” din satul Cobani", "Cobani", "Sf.Arh.Mihail și Gavriil", "", 87),
        ("md-bom-balti-doltu-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Doltu", "biserica „Cuvioasa Parascheva” din satul Doltu", "Doltu", "Cuvioasa Parascheva", "", 88),
        ("md-bom-balti-flamanzeni-church-saint-nicholas", "Church", "Saint Nicholas Church in Flămânzeni", "Biserica „Sfântul Ierarh Nicolae” din Flămânzeni", "Flămânzeni", "Sfântul Ierarh Nicolae", "", 89),
        ("md-bom-balti-glingeni-monastery-holy-trinity", "Monastery", "Holy Trinity Monastery in Glingeni", "Mănăstirea “Sf. Treime”, Glingeni", "Glingeni", "Sf. Treime", "MD-5924, s. Glingeni, r. Făleşti", 1),
        ("md-bom-balti-izvoare-skete-saint-demetrius-the-great-martyr", "Skete", "Saint Demetrius the Great Martyr Skete in Izvoare", "Schitul “Sf. M. Mc. Dimitrie”, Izvoare", "Izvoare", "Sf. M. Mc. Dimitrie", "MD-5931, s. Izvoare, r. Făleşti", 1),
        ("md-bom-balti-rediul-de-jos-skete-saint-prince-vladimir", "Skete", "Saint Prince Vladimir Skete in Rediul de Jos", "Schitul “Sf. Cn. Vladimir”, Rediul de Jos", "Rediul de Jos", "Sf. Cn. Vladimir", "MD-5911, s. Rediul de Jos, r. Făleşti", 1),
        ("md-bom-balti-ustia-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Ustia", "bisericii „Sfinții Arhangheli Mihail și Gavriil” din satul Ustia", "Ustia", "Sfinții Arhangheli Mihail și Gavriil", "", 90),
    ),
    "ru-cahul": (
        ("md-bom-cahul-zloti-monastery-george", "Monastery", "Saint George the Great Martyr Monastery in Zloți", "Mănăstirea „Sf. M. Mc. Gheorghe”, Zloţi", "Zloți", "Sf. M. Mc. Gheorghe", "MD-7718, s. Zloţi, r. Cimișlia", 135),
        ("md-bom-cahul-basarabeasca-church-saint-nicholas", "Church", "Saint Nicholas Church in Basarabeasca", "Biserica „Sf. Ierarh Nicolae” - Basarabeasca", "Basarabeasca", "Sf. Ierarh Nicolae", "", 0),
        ("md-bom-cahul-cahul-cathedral-holy-archangels-michael-and-gabriel", "Cathedral", "Holy Archangels Michael and Gabriel Cathedral in Cahul", "catedrala episcopală ”Sf. Arh. Mihail și Gavriil” din or. Cahul", "Cahul", "Sf. Arh. Mihail și Gavriil", "or. Cahul, str. L. Tolstoi, 1", 91),
        ("md-bom-cahul-cahul-monastery-saint-prince-vladimir", "Monastery", "Saint Prince Vladimir Monastery in Cahul", "Mănăstirea „Sfântul Cneaz Vladimir”", "Cahul", "Sfântul Cneaz Vladimir", "MD-3900, str. Tolstoi 1, or. Cahul", 92),
        ("md-bom-cahul-ceadar-lunga-monastery-saint-demetrius-the-great-martyr", "Monastery", "Saint Demetrius the Great Martyr Monastery in Ceadîr-Lunga", "Mănăstirea „Sfântul Mare Mucenic Dimitrie”", "Ceadîr-Lunga", "Sfântul Mare Mucenic Dimitrie", "MD-6100, or. Ceadîr-Lunga, UTAG", 92),
        ("md-bom-cahul-cociulia-monastery-protection-of-the-mother-of-god", "Monastery", "Protection of the Mother of God Monastery in Cociulia", "Mănăstirea „Acoperământul Maicii Domnului”, Cociulia", "Cociulia", "Acoperământul Maicii Domnului", "MD-7321, com. Cociulia, r. Cantemir", 93),
        ("md-bom-cahul-comrat-cathedral-saint-john-the-baptist", "Cathedral", "Saint John the Baptist Cathedral in Comrat", "Catedrala Episcopală „Sf. Ioan Botezătorul” din orașul Comrat", "Comrat", "Sf. Ioan Botezătorul", "", 94),
        ("md-bom-cahul-comrat-monastery-iveron-icon-of-the-mother-of-god", "Monastery", "Iveron Icon of the Mother of God Monastery in Comrat", "Mănăstirea „Icoana MaiciiDomnului Iverskaia”", "Comrat", "Icoana MaiciiDomnului Iverskaia", "MD-3801, or. Comrat", 92),
        ("md-bom-cahul-congaz-church-holy-trinity", "Church", "Holy Trinity Church in Congaz", "Biserica „Sfânta Treime” din Congaz", "Congaz", "Sfânta Treime", "", 95),
        ("md-bom-cahul-copceac-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Copceac", "Biserica „Adormirea Maicii Domnului” - Copceac, r. Ceadâr-Lunga", "Copceac", "Adormirea Maicii Domnului", "", 0),
        ("md-bom-cahul-porumbrei-parish-saint-george-the-great-martyr", "Parish", "Saint George the Great Martyr Parish in Porumbrei", "parohia „Sf. M. Mc. Gheorghe” din satul Porumbrei", "Porumbrei", "Sf. M. Mc. Gheorghe", "", 96),
        ("md-bom-cahul-sadaclia-monastery-saint-nicholas", "Monastery", "Saint Nicholas Monastery in Sadaclia", "Mănăstirea „Sfântul Ierarh Nicolae”", "Sadaclia", "Sfântul Ierarh Nicolae", "MD-6717, com. Sadaclia, r. Basarabeasca", 92),
        ("md-bom-cahul-taraclia-cathedral-catedrala-episcopala-din-or-taraclia", "Cathedral", "Saint George the Great Martyr Cathedral in Taraclia", "Catedralei Episcopale „Sf. M. Mc. Gheorghe” din or. Taraclia", "Taraclia", "Sf. M. Mc. Gheorghe", "", 97),
        ("md-bom-cahul-taraclia-monastery-nativity-of-the-mother-of-god", "Monastery", "Nativity of the Mother of God Monastery in Taraclia", "Mănăstirea „Nașterea Maicii Domnului”", "Taraclia", "Nașterea Maicii Domnului", "MD-7400, or. Taraclia", 92),
    ),
    "ru-edinet": (
        ("md-bom-edinet-alexandreni-church-holy-archangels", "Church", "Holy Archangels Church in Alexăndreni", "ALEXĂNDRENI - “Sf. Arhangheli”", "Alexăndreni", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-alexeevca-church-saint-alexis-metropolitan-of-moscow", "Church", "Saint Alexis, Metropolitan of Moscow Church in Alexeevca", "ALEXEEVCA - “Sf. Alexei Mitrop. Moscovei”", "Alexeevca", "Sf. Alexei Mitrop. Moscovei", "", 98),
        ("md-bom-edinet-arionesti-church-saint-nicholas", "Church", "Saint Nicholas Church in Arioneşti", "ARIONEŞTI - “Sf. Nicolae”", "Arioneşti", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-badragii-noi-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Bădragii Noi", "BĂDRAGII NOI - “Cuv. Parascheva”", "Bădragii Noi", "Cuv. Parascheva", "", 98),
        ("md-bom-edinet-badragii-vechi-church-saint-george", "Church", "Saint George Church in Bădragii Vechi", "BĂDRAGII VECHI - “Sf. Gheorghe”", "Bădragii Vechi", "Sf. Gheorghe", "", 98),
        ("md-bom-edinet-balasanesti-church-three-holy-hierarchs", "Church", "Three Holy Hierarchs Church in Balasîneşti", "BALASÎNEŞTI - “Sf. Trei Ierarhi”", "Balasîneşti", "Sf. Trei Ierarhi", "", 98),
        ("md-bom-edinet-balcauti-church-holy-archangels", "Church", "Holy Archangels Church in Balcauţi", "BALCAUŢI - “Sf. Arhangheli”", "Balcauţi", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-baraboi-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Baraboi", "BARABOI - “N. M. D.”", "Baraboi", "N. M. D.", "", 98),
        ("md-bom-edinet-baraboi-church-three-holy-hierarchs", "Church", "Three Holy Hierarchs Church in Baraboi", "BARABOI - „Sf. Trei Ierarhi”", "Baraboi", "Sf. Trei Ierarhi", "", 98),
        ("md-bom-edinet-barnova-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Bîrnova", "BÎRNOVA - “N. M. D.”", "Bîrnova", "N. M. D.", "", 98),
        ("md-bom-edinet-beleavinta-church-saint-nicholas", "Church", "Saint Nicholas Church in Beleavinţî", "BELEAVINŢÎ - “Sf. Nicolae”", "Beleavinţî", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-berezovca-church-saint-demetrius", "Church", "Saint Demetrius Church in Berezovca", "BEREZOVCA - “Sf. Dumitru”", "Berezovca", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-berlinta-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Berlinţî", "BERLINŢÎ - “Ac. M. D.”", "Berlinţî", "Ac. M. D.", "", 98),
        ("md-bom-edinet-bezeda-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Bezeda", "BEZEDA - “Ad. M. D.”", "Bezeda", "Ad. M. D.", "", 98),
        ("md-bom-edinet-blesteni-church-holy-trinity", "Church", "Holy Trinity Church in Bleşteni", "BLEŞTENI - “Sf. Treime”", "Bleşteni", "Sf. Treime", "", 98),
        ("md-bom-edinet-bogdanesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Bogdănești", "BOGDĂNEȘTI - “Ad. M. D.”", "Bogdănești", "Ad. M. D.", "", 98),
        ("md-bom-edinet-boroseni-chapel-nativity-of-the-mother-of-god", "Chapel", "Nativity of the Mother of God Chapel in Boroseni", "BOROSENI (paraclis) - “N. M. D.”", "Boroseni", "N. M. D.", "", 98),
        ("md-bom-edinet-braicau-church-saint-nicholas", "Church", "Saint Nicholas Church in Braicău", "BRAICĂU - “Sf. Nicolae”", "Braicău", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-bratuseni-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Brătuşeni", "BRĂTUŞENI - “Sf. Petru şi Pavel”", "Brătuşeni", "Sf. Petru şi Pavel", "", 98),
        ("md-bom-edinet-bratuseni-noi-church-saint-alexander-nevsky", "Church", "Saint Alexander Nevsky Church in Brătuşeni Noi", "BRĂTUŞENI NOI - “Sf. Kneaz Alexandru Nevski”", "Brătuşeni Noi", "Sf. Kneaz Alexandru Nevski", "", 98),
        ("md-bom-edinet-briceni-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Briceni", "BRICENI - “N. M. D.”", "Briceni", "N. M. D.", "", 98),
        ("md-bom-edinet-briceni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Briceni", "BRICENI - “Ac. M. D.”", "Briceni", "Ac. M. D.", "", 98),
        ("md-bom-edinet-briceni-church-saint-basil-the-great", "Church", "Saint Basil the Great Church in Briceni", "BRICENI - “Sf. Vasile cel Mare”", "Briceni", "Sf. Vasile cel Mare", "", 98),
        ("md-bom-edinet-briceni-church-saint-nicholas", "Church", "Saint Nicholas Church in Briceni", "Briceni - “Sf. Nicolae”", "Briceni", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-briceni-church-saint-simeon-the-stylite", "Church", "Saint Simeon the Stylite Church in Briceni", "Briceni - “Sf. Simeon Stîlpnicul”", "Briceni", "Sf. Simeon Stîlpnicul", "", 98),
        ("md-bom-edinet-briceni-monastery-resurrection-of-the-lord", "Monastery", "Resurrection of the Lord Monastery in Briceni", "Mănăstirea “Învierea Domnului”, or. Briceni", "Briceni", "Învierea Domnului", "MD, 4701 or. Briceni, str. Mănastirii 1", 1),
        ("md-bom-edinet-bulboaca-church-saint-nicholas", "Church", "Saint Nicholas Church in Bulboaca", "BULBOACA - “Sf. Nicolae”", "Bulboaca", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-calaraseuca-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Călărăşeuca", "Mănăstirea „Adormirea Maicii Domnului„, Călărăşeuca", "Călărăşeuca", "Adormirea Maicii Domnului", "MD-7114, loc. Călărășeuca, r-nul Ocnița", 1),
        ("md-bom-edinet-calarasovca-church-saint-nicholas", "Church", "Saint Nicholas Church in Calaraşovca", "CALARAŞOVCA - “Sf. Nicolae”", "Calaraşovca", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-caracusenii-noi-church-holy-trinity", "Church", "Holy Trinity Church in Caracuşenii Noi", "CARACUŞENII NOI - “Sf. Treime”", "Caracuşenii Noi", "Sf. Treime", "", 98),
        ("md-bom-edinet-caracusenii-vechi-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Caracușenii Vechi", "CARACUȘENII VECHI - “Ad. M. D.”", "Caracușenii Vechi", "Ad. M. D.", "", 98),
        ("md-bom-edinet-cepeliuti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Cepeliuţi", "CEPELIUŢI - “Ac. M. D.”", "Cepeliuţi", "Ac. M. D.", "", 98),
        ("md-bom-edinet-cernoleuca-church-dormition-and-annunciation", "Church", "Nativity of the Mother of God and Annunciation Church in Cernoleuca", "CERNOLEUCA - “N. M. D.” / ”Buna-Vestire”", "Cernoleuca", "N. M. D.” / ”Buna-Vestire", "", 98),
        ("md-bom-edinet-chetrosica-noua-church-saint-nicholas", "Church", "Saint Nicholas Church in Chetroşica Nouă", "CHETROŞICA NOUĂ - “Sf. Nicolae”", "Chetroşica Nouă", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-chetrosica-veche-parish-parohia-chetrosica-veche", "Parish", "Parish in Chetroşica Veche", "parohia Chetroșica Veche", "Chetroşica Veche", "", "", 99),
        ("md-bom-edinet-chiurt-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Chiurt", "Chiurt - “Înălţarea Domnului”", "Chiurt", "Înălţarea Domnului", "", 98),
        ("md-bom-edinet-clocusna-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Clocuşna", "CLOCUŞNA - “Sf. Ioan Teologul”", "Clocuşna", "Sf. Ioan Teologul", "", 98),
        ("md-bom-edinet-codreni-church-saint-demetrius", "Church", "Saint Demetrius Church in Codreni", "CODRENI - “Sf. Dumitru”", "Codreni", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-codreni-church-saint-nicholas", "Church", "Saint Nicholas Church in Codreni", "CODRENI - “Sf. Nicolae”", "Codreni", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-colicauti-church-saint-gregory-the-theologian", "Church", "Saint Gregory the Theologian Church in Colicăuţi", "COLICĂUŢI - “Sf. Grigore Teologul”", "Colicăuţi", "Sf. Grigore Teologul", "", 98),
        ("md-bom-edinet-constantinovca-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Constantinovca", "CONSTANTINOVCA - “Ad. M. D.”", "Constantinovca", "Ad. M. D.", "", 98),
        ("md-bom-edinet-corbu-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Corbu", "CORBU - “Cuv. Parascvheva”", "Corbu", "Cuv. Parascvheva", "", 98),
        ("md-bom-edinet-corestauti-church-saint-basil", "Church", "Saint Basil Church in Corestăuţi", "CORESTĂUŢI - “Sf. Vasile”", "Corestăuţi", "Sf. Vasile", "", 98),
        ("md-bom-edinet-corjauti-church-holy-archangels", "Church", "Holy Archangels Church in Corjăuţi", "CORJĂUŢI - “Sf. Arhangheli”", "Corjăuţi", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-corpaci-church-saint-john-chrysostom", "Church", "Saint John Chrysostom Church in Corpaci", "CORPACI - „Sf. Ioan Gură de Aur”", "Corpaci", "Sf. Ioan Gură de Aur", "", 98),
        ("md-bom-edinet-coteala-church-saint-demetrius", "Church", "Saint Demetrius Church in Coteala", "COTEALA - “Sf. Dumitru”", "Coteala", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-cotiujeni-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Cotiujeni", "COTIUJENI - “Naşterea M. D.”", "Cotiujeni", "Naşterea M. D.", "", 98),
        ("md-bom-edinet-criscauti-church-saints-constantine-and-helen", "Church", "Saints Constantine and Helen Church in Crişcăuţi", "CRIŞCĂUŢI - „Sf. Împ.C-tin şi Elena”", "Crişcăuţi", "Sf. Împ.C-tin şi Elena", "", 98),
        ("md-bom-edinet-criva-church-holy-archangels", "Church", "Holy Archangels Church in Criva", "CRIVA - “Sf. Arhangheli”", "Criva", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-cuconesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Cuconeşti", "CUCONEŞTI - “Ad. M. D.”", "Cuconeşti", "Ad. M. D.", "", 98),
        ("md-bom-edinet-cupcini-church-holy-trinity", "Church", "Holy Trinity Church in Cupcini", "CUPCINI - “Sf. Treime”", "Cupcini", "Sf. Treime", "", 98),
        ("md-bom-edinet-cupcini-church-saint-demetrius", "Church", "Saint Demetrius Church in Cupcini", "CUPCINI - “Sf. Dumitru”", "Cupcini", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-dangeni-church-holy-archangels", "Church", "Holy Archangels Church in Dîngeni", "DÎNGENI - “Sf. Arhangheli”", "Dîngeni", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-donduseni-church-saint-nicholas", "Church", "Saint Nicholas Church in Donduşeni", "DONDUŞENI - “Sf. Nicolae”", "Donduşeni", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-drepcauti-church-saint-nicholas", "Church", "Saint Nicholas Church in Drepcăuţi", "DREPCĂUŢI - “Sf. Nicolae”", "Drepcăuţi", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-druta-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Druţă", "DRUŢĂ - “Ad. M. D.”", "Druţă", "Ad. M. D.", "", 98),
        ("md-bom-edinet-duruitoarea-noua-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Duruitoarea Nouă", "DURUITOAREA NOUĂ - “Înălţarea Domnului”", "Duruitoarea Nouă", "Înălţarea Domnului", "", 98),
        ("md-bom-edinet-edinet-cathedral-saint-basil-the-great", "Cathedral", "Saint Basil the Great Cathedral in Edineţ", "EDINEŢ - “Sf. Vasile cel Mare”", "Edineţ", "Sf. Vasile cel Mare", "", 98),
        ("md-bom-edinet-edinet-church-saint-panteleimon", "Church", "Saint Panteleimon Church in Edineţ", "EDINEŢ - “Sf. M. Mc. Panteleimon”", "Edineţ", "Sf. M. Mc. Panteleimon", "", 98),
        ("md-bom-edinet-edinet-church-saints-sergius-and-bacchus", "Church", "Saints Sergius and Bacchus Church in Edineţ", "EDINEŢ - “Sf. Mc .Serghie şi Vah”", "Edineţ", "Sf. Mc .Serghie şi Vah", "", 98),
        ("md-bom-edinet-edinet-church-three-holy-hierarchs", "Church", "Three Holy Hierarchs Church in Edineţ", "EDINEŢ - “Sf. Trei Ierarhi”", "Edineţ", "Sf. Trei Ierarhi", "", 98),
        ("md-bom-edinet-elizavetovca-church-saint-demetrius", "Church", "Saint Demetrius Church in Elizavetovca", "ELIZAVETOVCA - “Sf. Dumitru”", "Elizavetovca", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-fantana-alba-church-saint-nicholas", "Church", "Saint Nicholas Church in Fîntîna Albă", "FÎNTÎNA ALBĂ - “Sf. Nicolae”", "Fîntîna Albă", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-frasin-church-holy-archangels", "Church", "Holy Archangels Church in Frasin", "FRASIN - “Sf. Arhangheli”", "Frasin", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-frunza-church-holy-archangels", "Church", "Holy Archangels Church in Frunza", "FRUNZA - “Sf. Arhangheli”", "Frunza", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-gaspar-church-holy-archangels", "Church", "Holy Archangels Church in Gaşpar", "GAŞPAR - “Sf. Arhangheli”", "Gaşpar", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-ghincauti-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Ghincăuţi", "GHINCĂUŢI - “Sf. App. Petru și Pavel”", "Ghincăuţi", "Sf. App. Petru și Pavel", "", 98),
        ("md-bom-edinet-ghincauti-church-holy-archangels", "Church", "Holy Archangels Church in Ghincăuţi", "GHINCĂUŢI - “Sf. Arhangheli”", "Ghincăuţi", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-goleni-church-saint-nicholas", "Church", "Saint Nicholas Church in Goleni", "GOLENI - “Sf. Nicolae”", "Goleni", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-gordinesti-noi-chapel-holy-trinity", "Chapel", "Holy Trinity Chapel in Gordineşti Noi", "GORDINEŞTI NOI (paraclis) - “Sf. Treime”", "Gordineşti Noi", "Sf. Treime", "", 98),
        ("md-bom-edinet-gordinesti-vechi-church-holy-archangels", "Church", "Holy Archangels Church in Gordineşti Vechi", "GORDINEŞTI Vechi - “Sf. Arhangheli”", "Gordineşti Vechi", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-grimancauti-church-holy-trinity", "Church", "Holy Trinity Church in Grimăncăuţi", "GRIMĂNCĂUŢI - “Sf. Treime”", "Grimăncăuţi", "Sf. Treime", "", 98),
        ("md-bom-edinet-grinauti-moldova-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Grinăuţi-moldova", "GRINĂUŢI-MOLDOVA - “Ac. M. D.”", "Grinăuţi-moldova", "Ac. M. D.", "", 98),
        ("md-bom-edinet-grinauti-moldova-church-saint-nicholas", "Church", "Saint Nicholas Church in Grinăuţi-moldova", "GRINĂUŢI-MOLDOVA - “Sf. Nicolae”", "Grinăuţi-moldova", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-groznita-church-prophet-elijah", "Church", "Prophet Elijah Church in Groznița", "GROZNIȚA - “Sf. Prooroc Ilie”", "Groznița", "Sf. Prooroc Ilie", "", 98),
        ("md-bom-edinet-hadarauti-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Hădărăuţi", "HĂDĂRĂUŢI - “Înălţarea Domnului”", "Hădărăuţi", "Înălţarea Domnului", "", 98),
        ("md-bom-edinet-hadarauti-church-holy-trinity", "Church", "Holy Trinity Church in Hădărăuţi", "HĂDĂRĂUŢI - “Sf. Treime”", "Hădărăuţi", "Sf. Treime", "", 98),
        ("md-bom-edinet-hancauti-church-saint-demetrius", "Church", "Saint Demetrius Church in Hancăuţi", "HANCĂUŢI - “Sf. Dumitru”", "Hancăuţi", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-hlinoaia-church-saint-nicholas", "Church", "Saint Nicholas Church in Hlinoaia", "HLINOAIA - “Sf. Nicolae”", "Hlinoaia", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-holahora-de-sus-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Holahora De Sus", "HOLAHORA DE SUS - “Ac. M. D.”", "Holahora De Sus", "Ac. M. D.", "", 98),
        ("md-bom-edinet-horodiste-church-holy-trinity", "Church", "Holy Trinity Church in Horodişte", "HORODIŞTE - “Sf. Treime”", "Horodişte", "Sf. Treime", "", 98),
        ("md-bom-edinet-horodiste-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Horodiște", "HORODIȘTE - „Acoperemîntul M. D.”", "Horodiște", "Acoperemîntul M. D.", "", 98),
        ("md-bom-edinet-larga-church-holy-trinity", "Church", "Holy Trinity Church in Larga", "LARGA - “Sf. Treime”", "Larga", "Sf. Treime", "", 98),
        ("md-bom-edinet-lencauti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Lencăuţi", "LENCĂUŢI - “Ac. M. D.”", "Lencăuţi", "Ac. M. D.", "", 98),
        ("md-bom-edinet-lipcani-church-saint-katherine", "Church", "Saint Katherine Church in Lipcani", "LIPCANI - “Sf. Ecaterina”", "Lipcani", "Sf. Ecaterina", "", 98),
        ("md-bom-edinet-lipcani-church-saint-stephen-the-great", "Church", "Saint Stephen the Great Church in Lipcani", "LIPCANI (penitenciar) - “Sf. Ștefan cel Mare”", "Lipcani", "Sf. Ștefan cel Mare", "", 98),
        ("md-bom-edinet-marcauti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Mărcăuţi", "MĂRCĂUŢI - “Ad. M. D.”", "Mărcăuţi", "Ad. M. D.", "", 98),
        ("md-bom-edinet-medveja-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Medveja", "MEDVEJA - “Înălţarea Domnului”", "Medveja", "Înălţarea Domnului", "", 98),
        ("md-bom-edinet-mereseuca-church-exaltation-of-the-holy-cross", "Church", "Exaltation of the Holy Cross Church in Mereşeuca", "MEREŞEUCA - “Înălţarea Sf. Cruci”", "Mereşeuca", "Înălţarea Sf. Cruci", "", 98),
        ("md-bom-edinet-mihaileni-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Mihăileni", "mihăileni - “Adormirea Maicii Domnului”", "Mihăileni", "Adormirea Maicii Domnului", "", 98),
        ("md-bom-edinet-mihalaseni-church-holy-archangels", "Church", "Holy Archangels Church in Mihălăşeni", "MIHĂLĂŞENI - “Sf. Arhangheli”", "Mihălăşeni", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-mosana-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Moşana", "MOŞANA - “Ac. M. D.”", "Moşana", "Ac. M. D.", "", 98),
        ("md-bom-edinet-naslavcea-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Naslavcea", "NASLAVCEA - “Ad. M. D.”", "Naslavcea", "Ad. M. D.", "", 98),
        ("md-bom-edinet-ocnita-church-holy-archangels", "Church", "Holy Archangels Church in Ocniţa", "OCNIŢA - “Sf. Arhangheli”", "Ocniţa", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-onesti-church-saint-nicholas", "Church", "Saint Nicholas Church in Oneşti", "ONEŞTI - “Sf. Nicolae”", "Oneşti", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-or-ocnita-church-saint-george", "Church", "Saint George Church in Or. Ocniţa", "or. OCNIŢA - “Sf. Gheorghe”", "Or. Ocniţa", "Sf. Gheorghe", "", 98),
        ("md-bom-edinet-otaci-church-holy-archangels", "Church", "Holy Archangels Church in Otaci", "OTACI - “Sf. Arhangheli”", "Otaci", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-paladea-church-holy-archangels", "Church", "Holy Archangels Church in Paladea", "PAladea - “Sf. Arhangheli”", "Paladea", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-parcova-church-holy-archangels", "Church", "Holy Archangels Church in Parcova", "PARCOVA - “Sf. Arhangheli”", "Parcova", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-paustova-church-entry-of-the-mother-of-god-into-the-temple", "Church", "Entry of the Mother of God into the Temple Church in Paustova", "PAUSTOVA - “Intrarea M. D. în bis.”", "Paustova", "Intrarea M. D. în bis.", "", 98),
        ("md-bom-edinet-paustova-church-saint-sergius", "Church", "Saint Sergius Church in Paustova", "PAUSTOVA - “Cuv. Serghie”", "Paustova", "Cuv. Serghie", "", 98),
        ("md-bom-edinet-pererita-church-saint-demetrius", "Church", "Saint Demetrius Church in Pererita", "PERERITA - “Sf. Dumitru”", "Pererita", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-pererita-church-saint-john-chrysostom", "Church", "Saint John Chrysostom Church in Pererita", "PERERITA - “Sf. Ioan Gură de Aur”", "Pererita", "Sf. Ioan Gură de Aur", "", 98),
        ("md-bom-edinet-pivniceni-church-saint-demetrius", "Church", "Saint Demetrius Church in Pivniceni", "PIVNICENI - “Sf. Dumitru”", "Pivniceni", "Sf. Dumitru", "", 98),
        ("md-bom-edinet-plop-church-holy-archangels", "Church", "Holy Archangels Church in Plop", "PLOP - “Sf. Arhangheli”", "Plop", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-pocimbauti-church-holy-archangels", "Church", "Holy Archangels Church in Pocimbăuţi", "POCIMBĂUŢI - “Sf. Arhangheli”", "Pocimbăuţi", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-pociumbeni-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Pociumbeni", "POCIUMBENI - “Cuv. Parascheva”", "Pociumbeni", "Cuv. Parascheva", "", 98),
        ("md-bom-edinet-poiana-chapel-prophet-elijah", "Chapel", "Prophet Elijah Chapel in Poiana", "POIANA (paraclis) - “Sf. Pr. Ilie”", "Poiana", "Sf. Pr. Ilie", "", 98),
        ("md-bom-edinet-rediul-mare-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Rediul Mare", "REDIUL MARE - “N. M. D.”", "Rediul Mare", "N. M. D.", "", 98),
        ("md-bom-edinet-rotunda-church-holy-archangels", "Church", "Holy Archangels Church in Rotunda", "ROTUNDA - “Sf. Arhangheli”", "Rotunda", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-rudi-monastery-holy-trinity", "Monastery", "Holy Trinity Monastery in Rudi", "Mănăstirea „Sf. Treime„, Rudi", "Rudi", "Sf. Treime", "MD, 5133, s. Rudi, r. Soroca", 100),
        ("md-bom-edinet-rujnita-church-holy-trinity", "Church", "Holy Trinity Church in Rujniţa", "RUJNIŢA - “Sf. Treime”", "Rujniţa", "Sf. Treime", "", 98),
        ("md-bom-edinet-ruseni-church-saint-nicholas", "Church", "Saint Nicholas Church in Ruseni", "RUSENI - “Sf. Nicolae”", "Ruseni", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-sauca-church-saint-nicholas", "Church", "Saint Nicholas Church in Sauca", "SAUCA - “Sf. Nicolae”", "Sauca", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-scaieni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Scăieni", "SCĂIENI - “Ac. M. D.”", "Scăieni", "Ac. M. D.", "", 98),
        ("md-bom-edinet-sirauti-church-saint-nicholas", "Church", "Saint Nicholas Church in Şirăuţi", "ŞIRĂUŢI - “Sf. Nicolae”", "Şirăuţi", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-slobozia-sirauti-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Slobozia Şirăuţi", "SLOBOZIA ŞIRĂUŢI - “N. M. D.”", "Slobozia Şirăuţi", "N. M. D.", "", 98),
        ("md-bom-edinet-sofrancani-church-saint-george", "Church", "Saint George Church in Şofrîncani", "ŞOFRÎNCANI - “Sf. Gheorghe”", "Şofrîncani", "Sf. Gheorghe", "", 98),
        ("md-bom-edinet-stolniceni-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Stolniceni", "STOLNICENI - “Nașterea. M. D.”", "Stolniceni", "Nașterea. M. D.", "", 98),
        ("md-bom-edinet-sudarca-church-holy-archangels", "Church", "Holy Archangels Church in Sudarca", "SUDARCA - “Sf. Arhangheli”", "Sudarca", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-tabani-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Tabani", "TABANI - “N. M. D.”", "Tabani", "N. M. D.", "", 98),
        ("md-bom-edinet-tarnova-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Tîrnova", "TÎRNOVA - “Ad. M. D.”", "Tîrnova", "Ad. M. D.", "", 98),
        ("md-bom-edinet-tarnova-church-holy-archangels", "Church", "Holy Archangels Church in Tîrnova", "TÎRNOVA - “Sf. Arhangheli”", "Tîrnova", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-tarnova-church-holy-trinity", "Church", "Holy Trinity Church in Tîrnova", "TÎRNOVA - “Sf. Treime”", "Tîrnova", "Sf. Treime", "", 98),
        ("md-bom-edinet-taul-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Ţaul", "ŢAUL - “Ad. M. D.”", "Ţaul", "Ad. M. D.", "", 98),
        ("md-bom-edinet-teleseuca-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Teleşeuca", "TELEŞEUCA - „N. M. D.”", "Teleşeuca", "N. M. D.", "", 98),
        ("md-bom-edinet-terebna-church-saint-nicholas", "Church", "Saint Nicholas Church in Terebna", "TEREBNA - “Sf. Nicolae”", "Terebna", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-tetcani-church-holy-trinity", "Church", "Holy Trinity Church in Tețcani", "TEȚCANI - “Sf. Treime”", "Tețcani", "Sf. Treime", "", 98),
        ("md-bom-edinet-trebisauti-church-holy-archangels", "Church", "Holy Archangels Church in Trebisăuţi", "TREBISĂUŢI - “Sf. Arhangheli”", "Trebisăuţi", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-trestieni-church-holy-archangels", "Church", "Holy Archangels Church in Trestieni", "TRESTIENI - “Sf. Arhangheli”", "Trestieni", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-trinca-church-holy-archangels", "Church", "Holy Archangels Church in Trinca", "TRINCA - “Sf. Arhangheli”", "Trinca", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-unguri-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Unguri", "UNGURI - “N. M. D.”", "Unguri", "N. M. D.", "", 98),
        ("md-bom-edinet-varatec-church-saint-nicholas", "Church", "Saint Nicholas Church in Văratec", "VĂRATEC - “Sf. Nicolae”", "Văratec", "Sf. Nicolae", "", 98),
        ("md-bom-edinet-verejeni-church-holy-archangels", "Church", "Holy Archangels Church in Verejeni", "VEREJENI - “Sf. Arhangheli”", "Verejeni", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-viisoara-church-holy-archangels", "Church", "Holy Archangels Church in Viişoara", "VIIŞOARA - “Sf. Arhangheli”", "Viişoara", "Sf. Arhangheli", "", 98),
        ("md-bom-edinet-volcinet-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Volcineţ", "VOLCINEŢ - “N. M. D.”", "Volcineţ", "N. M. D.", "", 98),
        ("md-bom-edinet-zaicani-church-holy-trinity", "Church", "Holy Trinity Church in Zăicani", "ZĂICANI - “Sf. Treime”", "Zăicani", "Sf. Treime", "", 98),
    ),
    "ru-soroca": (
        ("md-bom-soroca-alexandrovca-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Alexandrovca", "Parohia „Adormirea Maicii Domnului”, satul Alexandrovca", "Alexandrovca", "Adormirea Maicii Domnului", "", 101),
        ("md-bom-soroca-alexandru-cel-bun-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Alexandru cel Bun", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Alexandru cel Bun", "Alexandru cel Bun", "Sfântul Mare Mucenic Dimitrie", "", 102),
        ("md-bom-soroca-alexeevca-parish-kazan-icon-of-the-mother-of-god", "Parish", "Kazan Icon of the Mother of God Parish in Alexeevca", "Parohia „Icoana Maicii Domnului de la Kazani”, satul Alexeevca", "Alexeevca", "Icoana Maicii Domnului de la Kazani", "", 101),
        ("md-bom-soroca-alunis-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Aluniș", "Parohia „Adormirea Maicii Domnului”, satul Aluniș", "Aluniș", "Adormirea Maicii Domnului", "", 103),
        ("md-bom-soroca-antoneuca-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Antoneuca", "Parohia „Nașterea Maicii Domnului”, satul Antoneuca", "Antoneuca", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-badiceni-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Bădiceni", "Parohia „Adormirea Maicii Domnului”, satul Bădiceni", "Bădiceni", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-bahrinesti-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Băhrinești", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Băhrinești", "Băhrinești", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-balanu-nou-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Balanu-Nou", "Parohia „Nașterea Maicii Domnului”, satul Balanu-Nou", "Balanu-Nou", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-balinti-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Balinți", "Parohia „Acoperământul Maicii Domnului”, satul Balinți", "Balinți", "Acoperământul Maicii Domnului", "", 102),
        ("md-bom-soroca-baroncea-noua-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Baroncea Nouă", "Parohia „Sfânta Cuvioasa Parascheva”, satul Baroncea Nouă", "Baroncea Nouă", "Sfânta Cuvioasa Parascheva", "", 104),
        ("md-bom-soroca-baroncea-parish-holy-trinity", "Parish", "Holy Trinity Parish in Baroncea", "Parohia „Sfânta Treime”, satul Baroncea", "Baroncea", "Sfânta Treime", "", 104),
        ("md-bom-soroca-baxani-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Băxani", "Parohia „Nașterea Maicii Domnului”, satul Băxani", "Băxani", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-bobulesti-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Bobulești", "Parohia „Nașterea Maicii Domnului”, satul Bobulești", "Bobulești", "Nașterea Maicii Domnului", "", 101),
        ("md-bom-soroca-borosenii-noi-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Borosenii Noi", "Parohia „Sfânta Cuvioasa Parascheva”, satul Borosenii Noi", "Borosenii Noi", "Sfânta Cuvioasa Parascheva", "", 103),
        ("md-bom-soroca-braniste-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Braniște", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Braniște", "Braniște", "Sfinții Arhangheli Mihail și Gavriil", "", 103),
        ("md-bom-soroca-bulboci-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Bulboci", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Bulboci", "Bulboci", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-bulbocii-noi-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Bulbocii Noi", "Parohia „Acoperământul Maicii Domnului”, satul Bulbocii Noi", "Bulbocii Noi", "Acoperământul Maicii Domnului", "", 102),
        ("md-bom-soroca-bursuc-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Bursuc", "Parohia „Sfânta Cuvioasa Parascheva”, satul Bursuc", "Bursuc", "Sfânta Cuvioasa Parascheva", "", 101),
        ("md-bom-soroca-cainarii-vechi-monastery-saints-faith-hope-love-and-their-mother-sophia", "Monastery", "Saints Faith, Hope, Love and their mother Sophia Monastery in Căinarii Vechi", "Mănăstirea „Sfintele Mucenițe Vera, Nadejda, Liubovi și mama lor Sofia” din s. Căinarii Vechi, r. Soroca", "Căinarii Vechi", "Sfintele Mucenițe Vera, Nadejda, Liubovi și mama lor Sofia", "", 105),
        ("md-bom-soroca-cainarii-vechi-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Căinarii Vechi", "Parohia „Nașterea Maicii Domnului”, satul Căinarii Vechi", "Căinarii Vechi", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-capresti-parish-saints-constantine-and-helen", "Parish", "Saints Constantine and Helen Parish in Căprești", "Parohia „Sfinții Împărați Constantin și Elena”, satul Căprești", "Căprești", "Sfinții Împărați Constantin și Elena", "", 101),
        ("md-bom-soroca-casunca-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Cașunca", "Parohia „Sfânta Cuvioasa Parascheva”, satul Cașunca", "Cașunca", "Sfânta Cuvioasa Parascheva", "", 101),
        ("md-bom-soroca-cenusa-parish-miracle-of-the-archangel-michael", "Parish", "Miracle of the Archangel Michael Parish in Cenușa", "Parohia „Minunea Sfântului Arhanghel Mihail”, satul Cenușa", "Cenușa", "Minunea Sfântului Arhanghel Mihail", "", 101),
        ("md-bom-soroca-cerlina-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Cerlina", "Parohia „Adormirea Maicii Domnului”, satul Cerlina", "Cerlina", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-cernita-parish-saints-cosmas-and-damian", "Parish", "Saints Cosmas and Damian Parish in Cernița", "Parohia „Sfinții Mucenici Cosma și Damian”, satul Cernița", "Cernița", "Sfinții Mucenici Cosma și Damian", "", 101),
        ("md-bom-soroca-chetrosu-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Chetrosu", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Chetrosu", "Chetrosu", "Sfinții Arhangheli Mihail și Gavriil", "", 104),
        ("md-bom-soroca-ciripcau-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Ciripcău", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Ciripcău", "Ciripcău", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-ciubara-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Ciubara", "Parohia „Sfântul Apostol și Evanghelist Ioan Teologul”, satul Ciubara", "Ciubara", "Sfântul Apostol și Evanghelist Ioan Teologul", "", 103),
        ("md-bom-soroca-ciutulesti-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Ciutulești", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Ciutulești", "Ciutulești", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-corlateni-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Corlăteni", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Corlăteni", "Corlăteni", "Sfinții Arhangheli Mihail și Gavriil", "", 103),
        ("md-bom-soroca-cosauti-monastery-protection-of-the-mother-of-god", "Monastery", "Protection of the Mother of God Monastery in Cosăuți", "Mănăstirea „Acoperământul Maicii Domnului” din s. Cosăuți, r. Soroca", "Cosăuți", "Acoperământul Maicii Domnului", "", 106),
        ("md-bom-soroca-cosauti-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Cosăuți", "Parohia „Nașterea Maicii Domnului”, satul Cosăuți", "Cosăuți", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-cosernita-parish-three-holy-hierarchs", "Parish", "Three Holy Hierarchs Parish in Coșernița", "Parohia „Sfinții Trei Ierarhi”, satul Coșernița", "Coșernița", "Sfinții Trei Ierarhi", "", 101),
        ("md-bom-soroca-costesti-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Costești", "Parohia „Nașterea Maicii Domnului”, orașul Costești", "Costești", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-cotova-parish-holy-trinity", "Parish", "Holy Trinity Parish in Cotova", "Parohia „Sfânta Treime”, satul Cotova", "Cotova", "Sfânta Treime", "", 104),
        ("md-bom-soroca-cotova-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Cotova", "Parohia „Acoperământul Maicii Domnului”, satul Cotova", "Cotova", "Acoperământul Maicii Domnului", "", 104),
        ("md-bom-soroca-cremenciug-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Cremenciug", "Parohia „Sfântul Ioan Teologul”, satul Cremenciug", "Cremenciug", "Sfântul Ioan Teologul", "", 102),
        ("md-bom-soroca-cucuieti-parish-holy-trinity", "Parish", "Holy Trinity Parish in Cucuieți", "Parohia „Sfânta Treime”, satul Cucuieți", "Cucuieți", "Sfânta Treime", "", 103),
        ("md-bom-soroca-cuhurestii-de-jos-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Cuhureștii de Jos", "Parohia „Acoperământul Maicii Domnului”, satul Cuhureștii de Jos", "Cuhureștii de Jos", "Acoperământul Maicii Domnului", "", 101),
        ("md-bom-soroca-cuhurestii-de-sus-parish-holy-trinity", "Parish", "Holy Trinity Parish in Cuhureștii de Sus", "Parohia „Sfânta Treime”, satul Cuhureștii de Sus", "Cuhureștii de Sus", "Sfânta Treime", "", 101),
        ("md-bom-soroca-curesnita-noua-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Cureșnița Nouă", "Parohia „Sfântul Ioan Teologul”, satul Cureșnița Nouă", "Cureșnița Nouă", "Sfântul Ioan Teologul", "", 102),
        ("md-bom-soroca-curesnita-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Cureșnița", "Parohia „Nașterea Maicii Domnului”, satul Cureșnița", "Cureșnița", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-darcauti-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Dărcăuți", "Parohia „Sfântul Ierarh Nicolae”, satul Dărcăuți", "Dărcăuți", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-domulgeni-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Domulgeni", "Parohia „Sfântul Ierarh Nicolae”, satul Domulgeni", "Domulgeni", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-drochia-cathedral-dormition-of-the-mother-of-god", "Cathedral", "Dormition of the Mother of God Cathedral in Drochia", "Catedrala episcopală „Adormirea Maicii Domnului”, orașul Drochia", "Drochia", "Adormirea Maicii Domnului", "", 107),
        ("md-bom-soroca-drochia-parish-apostles-peter-and-paul", "Parish", "Apostles Peter and Paul Parish in Drochia", "Parohia „Sfinții Apostoli Petru și Pavel”, orașul Drochia", "Drochia", "Sfinții Apostoli Petru și Pavel", "", 104),
        ("md-bom-soroca-drochia-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Drochia", "Parohia „Adormirea Maicii Domnului”, satul Drochia", "Drochia", "Adormirea Maicii Domnului", "", 104),
        ("md-bom-soroca-drochia-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Drochia", "Parohia „Sfântul Ierarh Nicolae”, orașul Drochia", "Drochia", "Sfântul Ierarh Nicolae", "", 108),
        ("md-bom-soroca-drochia-parish-saint-seraphim-of-sarov", "Parish", "Saint Seraphim of Sarov Parish in Drochia", "Parohia „Sfântul Cuvios Serafim de Sarov”, orașul Drochia", "Drochia", "Sfântul Cuvios Serafim de Sarov", "", 109),
        ("md-bom-soroca-dubna-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Dubna", "Parohia „Adormirea Maicii Domnului”, satul Dubna", "Dubna", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-dumbraveni-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Dumbrăveni", "Parohia „Sfântul Ierarh Nicolae”, satul Dumbrăveni", "Dumbrăveni", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-dumitreni-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Dumitreni", "Parohia „Adormirea Maicii Domnului”, satul Dumitreni", "Dumitreni", "Adormirea Maicii Domnului", "", 101),
        ("md-bom-soroca-duruitoarea-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Duruitoarea", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Duruitoarea", "Duruitoarea", "Sfinții Arhangheli Mihail și Gavriil", "", 103),
        ("md-bom-soroca-egoreni-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Egoreni", "Parohia „Nașterea Maicii Domnului”, satul Egoreni", "Egoreni", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-fantanita-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Fîntînița", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Fîntînița", "Fîntînița", "Sfinții Arhangheli Mihail și Gavriil", "", 104),
        ("md-bom-soroca-floresti-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Florești", "Parohia „Acoperământul Maicii Domnului”, orașul Florești", "Florești", "Acoperământul Maicii Domnului", "", 101),
        ("md-bom-soroca-floresti-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Florești", "Parohia „Sfântul Mare Mucenic Dimitrie”, orașul Florești", "Florești", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-floresti-parish-saint-mitrophan", "Parish", "Saint Mitrophan Parish in Florești", "Parohia „Sfântul Ierarh Mitrofan”, orașul Florești", "Florești", "Sfântul Ierarh Mitrofan", "", 101),
        ("md-bom-soroca-floresti-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Florești", "Parohia „Sfântul Ierarh Nicolae”, orașul Florești", "Florești", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-frumusica-parish-miracle-of-the-archangel-michael", "Parish", "Miracle of the Archangel Michael Parish in Frumușica", "Parohia „Minunea Sfântului Arhanghel Mihail”, satul Frumușica", "Frumușica", "Minunea Sfântului Arhanghel Mihail", "", 101),
        ("md-bom-soroca-galaseni-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Gălășeni", "Parohia „Nașterea Maicii Domnului”, satul Gălășeni", "Gălășeni", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-ghindesti-parish-saint-spyridon-of-trimythous", "Parish", "Saint Spyridon of Trimythous Parish in Ghindești", "Parohia „Sfântul Ierarh Spiridon”, satul Ghindești", "Ghindești", "Sfântul Ierarh Spiridon", "", 101),
        ("md-bom-soroca-gribova-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Gribova", "Parohia „Sfântul Ierarh Nicolae”, satul Gribova", "Gribova", "Sfântul Ierarh Nicolae", "", 104),
        ("md-bom-soroca-grigorauca-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Grigorăuca", "Parohia „Adormirea Maicii Domnului”, satul Grigorăuca", "Grigorăuca", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-grinauti-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Grinăuți", "Parohia „Nașterea Maicii Domnului”, satul Grinăuți", "Grinăuți", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-gura-cainarului-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Gura Căinarului", "Parohia „Sfânta Cuvioasa Parascheva”, satul Gura Căinarului", "Gura Căinarului", "Sfânta Cuvioasa Parascheva", "", 101),
        ("md-bom-soroca-gura-camencei-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Gura Camencei", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Gura Camencei", "Gura Camencei", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-gvozdova-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Gvozdova", "Parohia „Sfântul Ierarh Nicolae”, satul Gvozdova", "Gvozdova", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-hartop-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Hîrtop", "Parohia „Nașterea Maicii Domnului”, satul Hîrtop", "Hîrtop", "Nașterea Maicii Domnului", "", 101),
        ("md-bom-soroca-hasnasenii-mari-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Hăsnășenii Mari", "Parohia „Nașterea Maicii Domnului”, satul Hăsnășenii Mari", "Hăsnășenii Mari", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-hasnasenii-mari-parish-pochaev-icon-of-the-mother-of-god", "Parish", "Pochaev Icon of the Mother of God Parish in Hăsnășenii Mari", "Parohia „Icoana Maicii Domnului de la Poceaev”, satul Hăsnășenii Mari", "Hăsnășenii Mari", "Icoana Maicii Domnului de la Poceaev", "", 104),
        ("md-bom-soroca-hasnasenii-noi-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Hăsnășenii Noi", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Hăsnășenii Noi", "Hăsnășenii Noi", "Sfântul Mare Mucenic Dimitrie", "", 104),
        ("md-bom-soroca-hiliuti-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Hiliuți", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Hiliuți", "Hiliuți", "Sfinții Arhangheli Mihail și Gavriil", "", 103),
        ("md-bom-soroca-holosnita-noua-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Holoșnița Nouă", "Parohia „Sfântul Apostol Ioan Teologul”, satul Holoșnița Nouă", "Holoșnița Nouă", "Sfântul Apostol Ioan Teologul", "", 104),
        ("md-bom-soroca-holosnita-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Holoșnița", "Parohia „Sfântul Ierarh Nicolae”, satul Holoșnița", "Holoșnița", "Sfântul Ierarh Nicolae", "", 110),
        ("md-bom-soroca-hristici-parish-holy-trinity", "Parish", "Holy Trinity Parish in Hristici", "Parohia „Sfânta Treime”, satul Hristici", "Hristici", "Sfânta Treime", "", 102),
        ("md-bom-soroca-iarova-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Iarova", "Parohia „Acoperământul Maicii Domnului”, satul Iarova", "Iarova", "Acoperământul Maicii Domnului", "", 102),
        ("md-bom-soroca-iliciovca-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Iliciovca", "Biserica „Adormirea Maicii Domnului”, satul Iliciovca", "Iliciovca", "Adormirea Maicii Domnului", "", 104),
        ("md-bom-soroca-iliciovca-parish-saint-simeon-the-stylite", "Parish", "Saint Simeon the Stylite Parish in Iliciovca", "Parohia „Sfântul Cuvios Simeon Stâlpnicul”, satul Iliciovca", "Iliciovca", "Sfântul Cuvios Simeon Stâlpnicul", "", 101),
        ("md-bom-soroca-inundeni-monastery-joy-of-all-who-sorrow-icon-of-the-mother-of-god", "Monastery", "Joy of All Who Sorrow Icon of the Mother of God Monastery in Inundeni", "Mănăstirea „Icoana Maicii Domnului Bucuria Tuturor Scârbiților” din s. Inundeni, r. Soroca", "Inundeni", "Icoana Maicii Domnului Bucuria Tuturor Scârbiților", "", 111),
        ("md-bom-soroca-inundeni-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Inundeni", "Parohia „Sfânta Cuvioasa Parascheva” satul Inundeni", "Inundeni", "Sfânta Cuvioasa Parascheva", "", 102),
        ("md-bom-soroca-ion-voda-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Ion Vodă", "Parohia „Adormirea Maicii Domnului”, satul Ion Vodă", "Ion Vodă", "Adormirea Maicii Domnului", "", 101),
        ("md-bom-soroca-iorjnita-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Iorjnița", "Parohia „Sfânta Cuvioasa Parascheva”, satul Iorjnița", "Iorjnița", "Sfânta Cuvioasa Parascheva", "", 102),
        ("md-bom-soroca-izvoare-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Izvoare", "Parohia „Sfânta Cuvioasa Parascheva”, satul Izvoare", "Izvoare", "Sfânta Cuvioasa Parascheva", "", 101),
        ("md-bom-soroca-japca-monastery-ascension-of-the-lord", "Monastery", "Ascension of the Lord Monastery in Japca", "Mănăstirea „Înălțarea Domnului” din s. Japca, r. Florești", "Japca", "Înălțarea Domnului", "", 112),
        ("md-bom-soroca-japca-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Japca", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Japca", "Japca", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-lunga-parish-saints-constantine-and-helen", "Parish", "Saints Constantine and Helen Parish in Lunga", "Parohia „Sfinții Împărați Constantin și Elena”, satul Lunga", "Lunga", "Sfinții Împărați Constantin și Elena", "", 101),
        ("md-bom-soroca-macareuca-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Măcăreuca", "Parohia „Adormirea Maicii Domnului”, satul Măcăreuca", "Măcăreuca", "Adormirea Maicii Domnului", "", 104),
        ("md-bom-soroca-maiscoe-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Maiscoe", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Maiscoe", "Maiscoe", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-malaiesti-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Mălăiești", "Parohia „Adormirea Maicii Domnului”, satul Mălăiești", "Mălăiești", "Adormirea Maicii Domnului", "", 103),
        ("md-bom-soroca-malcauti-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Mălcăuți", "Parohia „Nașterea Maicii Domnului”, satul Mălcăuți", "Mălcăuți", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-malinovscoe-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Malinovscoe", "Parohia „Acoperământul Maicii Domnului”, satul Malinovscoe", "Malinovscoe", "Acoperământul Maicii Domnului", "", 103),
        ("md-bom-soroca-mandac-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Mîndîc", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Mîndîc", "Mîndîc", "Sfinții Arhangheli Mihail și Gavriil", "", 104),
        ("md-bom-soroca-maramonovca-parish-holy-trinity", "Parish", "Holy Trinity Parish in Maramonovca", "Parohia „Sfânta Treime”, satul Maramonovca", "Maramonovca", "Sfânta Treime", "", 104),
        ("md-bom-soroca-marculesti-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Mărculești", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Mărculești", "Mărculești", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-marculesti-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Mărculești", "Parohia „Sfântul Ierarh Nicolae”, orașul Mărculești", "Mărculești", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-miciurin-monastery-saints-joachim-and-anna", "Monastery", "Saints Joachim and Anna Monastery in Miciurin", "Mănăstirea „Sfinții Părinți Ioachim și Ana” din s. Miciurin, r. Drochia", "Miciurin", "Sfinții Părinți Ioachim și Ana", "", 113),
        ("md-bom-soroca-miciurin-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Miciurin", "Parohia „Acoperământul Maicii Domnului”, satul Miciurin", "Miciurin", "Acoperământul Maicii Domnului", "", 104),
        ("md-bom-soroca-mihaileni-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Mihăileni", "Parohia „Acoperământul Maicii Domnului”, satul Mihăileni", "Mihăileni", "Acoperământul Maicii Domnului", "", 103),
        ("md-bom-soroca-mihailenii-noi-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Mihăilenii Noi", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Mihăilenii Noi", "Mihăilenii Noi", "Sfinții Arhangheli Mihail și Gavriil", "", 103),
        ("md-bom-soroca-mihailovca-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Mihailovca", "Parohia „Acoperământul Maicii Domnului”, satul Mihailovca", "Mihailovca", "Acoperământul Maicii Domnului", "", 101),
        ("md-bom-soroca-moara-de-piatra-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Moara de Piatră", "Parohia „Adormirea Maicii Domnului”, satul Moara de Piatră", "Moara de Piatră", "Adormirea Maicii Domnului", "", 104),
        ("md-bom-soroca-moseni-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Moșeni", "Parohia „Sfânta Cuvioasa Parascheva”, satul Moșeni", "Moșeni", "Sfânta Cuvioasa Parascheva", "", 103),
        ("md-bom-soroca-napadova-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Napadova", "Parohia „Sfântul Ierarh Nicolae”, satul Napadova", "Napadova", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-nicolaevca-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Nicolaevca", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Nicolaevca", "Nicolaevca", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-nicolaieni-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Nicolăieni", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Nicolăieni", "Nicolăieni", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-nicoreni-monastery-prophet-elijah", "Monastery", "Prophet Elijah Monastery in Nicoreni", "Mănăstirea „Sfântul Prooroc Ilie” din s. Nicoreni, r. Drochia", "Nicoreni", "Sfântul Prooroc Ilie", "", 114),
        ("md-bom-soroca-nicoreni-parish-holy-trinity", "Parish", "Holy Trinity Parish in Nicoreni", "Parohia „Sfânta Treime”, satul Nicoreni", "Nicoreni", "Sfânta Treime", "", 104),
        ("md-bom-soroca-nihoreni-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Nihoreni", "Parohia „Nașterea Maicii Domnului”, satul Nihoreni", "Nihoreni", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-nimereuca-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Nimereuca", "Parohia „Adormirea Maicii Domnului”, satul Nimereuca", "Nimereuca", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-niorcani-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Niorcani", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Niorcani", "Niorcani", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-ochiul-alb-parish-saint-stephen-the-protomartyr", "Parish", "Saint Stephen the Protomartyr Parish in Ochiul Alb", "Parohia „Sfântul Întâiul Mucenic Arhidiacon Ștefan”, satul Ochiul Alb", "Ochiul Alb", "Sfântul Întâiul Mucenic Arhidiacon Ștefan", "", 104),
        ("md-bom-soroca-oclanda-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Oclanda", "Parohia „Nașterea Maicii Domnului” satul Oclanda", "Oclanda", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-ocolina-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Ocolina", "Parohia „Sfântul Ierarh Nicolae” satul Ocolina", "Ocolina", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-palanca-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Palanca", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Palanca", "Palanca", "Sfinții Arhangheli Mihail și Gavriil", "", 104),
        ("md-bom-soroca-parcani-parish-miracle-of-the-archangel-michael", "Parish", "Miracle of the Archangel Michael Parish in Parcani", "Parohia „Minunea Sfântului Arhanghel Mihail”, satul Parcani", "Parcani", "Minunea Sfântului Arhanghel Mihail", "", 102),
        ("md-bom-soroca-parjota-parish-all-saints", "Parish", "All Saints Parish in Pîrjota", "Parohia „Tuturor Sfinților”, satul Pîrjota", "Pîrjota", "Tuturor Sfinților", "", 103),
        ("md-bom-soroca-parlita-parish-holy-trinity", "Parish", "Holy Trinity Parish in Pîrlița", "Parohia „Sfânta Treime”, satul Pîrlița", "Pîrlița", "Sfânta Treime", "", 102),
        ("md-bom-soroca-pelinia-parish-prophet-elijah", "Parish", "Prophet Elijah Parish in Pelinia", "Parohia „Sfântul Prooroc Ilie”, satul Pelinia", "Pelinia", "Sfântul Prooroc Ilie", "", 104),
        ("md-bom-soroca-pelinia-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Pelinia", "Parohia „Acoperământul Maicii Domnului”, satul Pelinia", "Pelinia", "Acoperământul Maicii Domnului", "", 104),
        ("md-bom-soroca-pelinia-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Pelinia", "Parohia „Sfântul Ierarh Nicolae”, satul Pelinia", "Pelinia", "Sfântul Ierarh Nicolae", "", 104),
        ("md-bom-soroca-pervomaisc-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Pervomaisc", "Parohia „Acoperământul Maicii Domnului”, satul Pervomaisc", "Pervomaisc", "Acoperământul Maicii Domnului", "", 104),
        ("md-bom-soroca-petreni-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Petreni", "Parohia „Nașterea Maicii Domnului”, satul Petreni", "Petreni", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-petruseni-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Petrușeni", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Petrușeni", "Petrușeni", "Sfinții Arhangheli Mihail și Gavriil", "", 103),
        ("md-bom-soroca-poiana-cunicei-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Poiana-Cunicei", "Parohia „Adormirea Maicii Domnului”, satul Poiana-Cunicei", "Poiana-Cunicei", "Adormirea Maicii Domnului", "", 101),
        ("md-bom-soroca-popestii-de-jos-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Popeștii de Jos", "Parohia „Nașterea Maicii Domnului”, satul Popeștii de Jos", "Popeștii de Jos", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-popestii-de-sus-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Popeștii de Sus", "Parohia „Nașterea Maicii Domnului”, satul Popeștii de Sus", "Popeștii de Sus", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-prajila-parish-holy-trinity", "Parish", "Holy Trinity Parish in Prajila", "Parohia „Sfânta Treime”, satul Prajila", "Prajila", "Sfânta Treime", "", 101),
        ("md-bom-soroca-prodanesti-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Prodănești", "Parohia „Sfântul Apostol Ioan Teologul”, satul Prodănești", "Prodănești", "Sfântul Apostol Ioan Teologul", "", 101),
        ("md-bom-soroca-putinesti-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Putinești", "Parohia „Sfântul Ierarh Nicolae”, satul Putinești", "Putinești", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-racaria-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Răcăria", "Parohia „Nașterea Maicii Domnului”, satul Răcăria", "Răcăria", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-racovat-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Racovăț", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Racovăț", "Racovăț", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-racovat-parish-prophet-elijah", "Parish", "Prophet Elijah Parish in Racovăț", "Parohia „Sfântul Prooroc Ilie”, satul Racovăț", "Racovăț", "Sfântul Prooroc Ilie", "", 102),
        ("md-bom-soroca-radulenii-vechi-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Rădulenii Vechi", "Parohia „Sfântul Ierarh Nicolae” satul Rădulenii Vechi", "Rădulenii Vechi", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-rascani-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Rîșcani", "Parohia „Adormirea Maicii Domnului”, orașul Rîșcani", "Rîșcani", "Adormirea Maicii Domnului", "", 103),
        ("md-bom-soroca-rascani-parish-saint-panteleimon", "Parish", "Saint Panteleimon Parish in Rîșcani", "Parohia „Sfântul Mare Mucenic Pantelimon”, orașul Rîșcani", "Rîșcani", "Sfântul Mare Mucenic Pantelimon", "", 103),
        ("md-bom-soroca-rascani-parish-saints-constantine-and-helen", "Parish", "Saints Constantine and Helen Parish in Rîșcani", "Parohia „Sfinții Împărați Constantin și Elena”, orașul Rîșcani", "Rîșcani", "Sfinții Împărați Constantin și Elena", "", 103),
        ("md-bom-soroca-recea-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Recea", "Parohia „Nașterea Maicii Domnului”, satul Recea", "Recea", "Nașterea Maicii Domnului", "", 103),
        ("md-bom-soroca-redi-ceresnovat-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Redi-Cereșnovăț", "Parohia „Adormirea Maicii Domnului”, satul Redi-Cereșnovăț", "Redi-Cereșnovăț", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-regina-maria-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Regina Maria", "Parohia „Nașterea Maicii Domnului”, satul Regina Maria", "Regina Maria", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-rosietici-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Roșietici", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Roșietici", "Roșietici", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-rosieticii-vechi-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Roșieticii Vechi", "Parohia „Acoperământul Maicii Domnului”, satul Roșieticii Vechi", "Roșieticii Vechi", "Acoperământul Maicii Domnului", "", 101),
        ("md-bom-soroca-rublenita-noua-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Rublenița Nouă", "Parohia „Acoperământul Maicii Domnului”, satul Rublenița Nouă", "Rublenița Nouă", "Acoperământul Maicii Domnului", "", 102),
        ("md-bom-soroca-rublenita-parish-miracle-of-the-archangel-michael", "Parish", "Miracle of the Archangel Michael Parish in Rublenița", "Parohia „Minunea Sfântului Arhanghel Mihail”, satul Rublenița", "Rublenița", "Minunea Sfântului Arhanghel Mihail", "", 102),
        ("md-bom-soroca-rublenita-parish-saint-george-the-great-martyr", "Parish", "Saint George the Great Martyr Parish in Rublenița", "Parohia „Sfântul Mare Mucenic Gheorghe”, satul Rublenița", "Rublenița", "Sfântul Mare Mucenic Gheorghe", "", 102),
        ("md-bom-soroca-rudi-parish-holy-trinity", "Parish", "Holy Trinity Parish in Rudi", "Parohia „Sfânta Treime”, satul Rudi", "Rudi", "Sfânta Treime", "", 102),
        ("md-bom-soroca-salvirii-noi-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Șalvirii Noi", "Parohia „Nașterea Maicii Domnului”, satul Șalvirii Noi", "Șalvirii Noi", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-salvirii-vechi-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Șalvirii Vechi", "Parohia „Nașterea Maicii Domnului”, satul Șalvirii Vechi", "Șalvirii Vechi", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-sanatauca-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Sănătăuca", "Parohia „Adormirea Maicii Domnului”, satul Sănătăuca", "Sănătăuca", "Adormirea Maicii Domnului", "", 101),
        ("md-bom-soroca-sangureni-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Sîngureni", "Parohia „Sfânta Cuvioasa Parascheva”, satul Sîngureni", "Sîngureni", "Sfânta Cuvioasa Parascheva", "", 103),
        ("md-bom-soroca-saptebani-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Șaptebani", "Parohia „Acoperământul Maicii Domnului”, satul Șaptebani", "Șaptebani", "Acoperământul Maicii Domnului", "", 103),
        ("md-bom-soroca-schineni-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Schineni", "Parohia „Sfântul Ierarh Nicolae”, satul Schineni", "Schineni", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-septelici-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Șeptelici", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Șeptelici", "Șeptelici", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-serbesti-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Serbești", "Parohia „Sfânta Cuvioasa Parascheva”, satul Serbești", "Serbești", "Sfânta Cuvioasa Parascheva", "", 101),
        ("md-bom-soroca-sevirova-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Sevirova", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Sevirova", "Sevirova", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-slanina-parish-ascension-of-the-lord", "Parish", "Ascension of the Lord Parish in Slănina", "Parohia „Înălțarea Domnului”, satul Slănina", "Slănina", "Înălțarea Domnului", "", 104),
        ("md-bom-soroca-slobozia-cremene-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Slobozia-Cremene", "Parohia „Nașterea Maicii Domnului”, satul Slobozia-Cremene", "Slobozia-Cremene", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-slobozia-noua-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Slobozia Nouă", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Slobozia Nouă", "Slobozia Nouă", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-slobozia-varancau-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Slobozia-Vărăncău", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Slobozia-Vărăncău", "Slobozia-Vărăncău", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-sobari-parish-holy-trinity", "Parish", "Holy Trinity Parish in Sobari", "Parohia „Sfânta Treime”, satul Sobari", "Sobari", "Sfânta Treime", "", 102),
        ("md-bom-soroca-sofia-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Sofia", "Parohia „Adormirea Maicii Domnului”, satul Sofia", "Sofia", "Adormirea Maicii Domnului", "", 104),
        ("md-bom-soroca-sofia-parish-holy-trinity", "Parish", "Holy Trinity Parish in Sofia", "Parohia „Sfânta Treime”, satul Sofia", "Sofia", "Sfânta Treime", "", 104),
        ("md-bom-soroca-solcani-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Șolcani", "Parohia „Sfântul Ierarh Nicolae”, satul Șolcani", "Șolcani", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-solonet-parish-miracle-of-the-archangel-michael", "Parish", "Miracle of the Archangel Michael Parish in Soloneț", "Parohia „Minunea Sfântului Arhanghel Mihail”, satul Soloneț", "Soloneț", "Minunea Sfântului Arhanghel Mihail", "", 102),
        ("md-bom-soroca-soroca-cathedral-dormition-of-the-mother-of-god", "Cathedral", "Dormition of the Mother of God Cathedral in Soroca", "Catedrala episcopală „Adormirea Maicii Domnului”, municipiul Soroca", "Soroca", "Adormirea Maicii Domnului", "", 115),
        ("md-bom-soroca-soroca-chapel-three-holy-hierarchs", "Chapel", "Three Holy Hierarchs Chapel in Soroca", "Capela „Sfinții Trei Ierarhi”, penitenciarul nr. 6 - Soroca", "Soroca", "Sfinții Trei Ierarhi", "", 102),
        ("md-bom-soroca-soroca-parish-holy-trinity", "Parish", "Holy Trinity Parish in Soroca", "Parohia „Sfânta Treime”, municipiul Soroca", "Soroca", "Sfânta Treime", "", 102),
        ("md-bom-soroca-soroca-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Soroca", "Parohia „Sfântul Mare Mucenic Dimitrie”, municipiul Soroca", "Soroca", "Sfântul Mare Mucenic Dimitrie", "", 116),
        ("md-bom-soroca-soroca-parish-saint-seraphim-of-sarov-and-the-apostles-peter-and-paul", "Parish", "Saint Seraphim of Sarov and the Apostles Peter and Paul Parish in Soroca", "Parohia „Sfântul Cuvios Serafim de Sarov și Sfinții Apostoli Petru și Pavel”, municipiul Soroca", "Soroca", "Sfântul Cuvios Serafim de Sarov și Sfinții Apostoli Petru și Pavel", "", 117),
        ("md-bom-soroca-soroca-parish-saint-sergius-of-radonezh", "Parish", "Saint Sergius of Radonezh Parish in Soroca", "Parohia „Sfântul Cuvios Serghie de Radonej”, municipiul Soroca", "Soroca", "Sfântul Cuvios Serghie de Radonej", "", 102),
        ("md-bom-soroca-soroca-parish-saint-theodore-stratelates", "Parish", "Saint Theodore Stratelates Parish in Soroca", "Parohia „Sfântul Mare Mucenic Teodor Stratilat”, municipiul Soroca", "Soroca", "Sfântul Mare Mucenic Teodor Stratilat", "", 118),
        ("md-bom-soroca-starceni-monastery-holy-archangels-michael-and-gabriel", "Monastery", "Holy Archangels Michael and Gabriel Monastery in Stîrceni", "Mănăstirea „Sfinții Arhangheli Mihail și Gavriil” din s. Stîrceni, r. Florești", "Stîrceni", "Sfinții Arhangheli Mihail și Gavriil", "", 119),
        ("md-bom-soroca-stoicani-parish-saint-panteleimon", "Parish", "Saint Panteleimon Parish in Stoicani", "Parohia „Sfântul Mare Mucenic Pantelimon”, satul Stoicani", "Stoicani", "Sfântul Mare Mucenic Pantelimon", "", 102),
        ("md-bom-soroca-suri-monastery-saint-john-chrysostom", "Monastery", "Saint John Chrysostom Monastery in Șuri", "Mănăstirea „Sfântul Ioan Gură de Aur” din s. Șuri, r. Drochia", "Șuri", "Sfântul Ioan Gură de Aur", "", 120),
        ("md-bom-soroca-suri-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Șuri", "Parohia „Nașterea Maicii Domnului”, satul Șuri", "Șuri", "Nașterea Maicii Domnului", "", 104),
        ("md-bom-soroca-surii-noi-parish-apostles-peter-and-paul", "Parish", "Apostles Peter and Paul Parish in Șurii Noi", "Parohia „Sfinții Apostoli Petru și Pavel”, satul Șurii Noi", "Șurii Noi", "Sfinții Apostoli Petru și Pavel", "", 104),
        ("md-bom-soroca-sverdiac-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Sverdiac", "Parohia „Sfântul Apostol și Evanghelist Ioan Teologul”, satul Sverdiac", "Sverdiac", "Sfântul Apostol și Evanghelist Ioan Teologul", "", 103),
        ("md-bom-soroca-tara-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Țîra", "Parohia „Adormirea Maicii Domnului”, satul Țîra", "Țîra", "Adormirea Maicii Domnului", "", 101),
        ("md-bom-soroca-targul-vertiujeni-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Tîrgul-Vertiujeni", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Tîrgul-Vertiujeni", "Tîrgul-Vertiujeni", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-tarigrad-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Țarigrad", "Parohia „Acoperământul Maicii Domnului”, satul Țarigrad", "Țarigrad", "Acoperământul Maicii Domnului", "", 104),
        ("md-bom-soroca-tarigrad-parish-saint-alexander-nevsky", "Parish", "Saint Alexander Nevsky Parish in Țarigrad", "Parohia „Sfântul Alexandru Nevski”, satul Țarigrad", "Țarigrad", "Sfântul Alexandru Nevski", "", 104),
        ("md-bom-soroca-tatarauca-noua-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Tătărăuca Nouă", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Tătărăuca Nouă", "Tătărăuca Nouă", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-tatarauca-veche-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Tătărăuca Veche", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Tătărăuca Veche", "Tătărăuca Veche", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-temeleuti-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Temeleuți", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Temeleuți", "Temeleuți", "Sfinții Arhangheli Mihail și Gavriil", "", 101),
        ("md-bom-soroca-tepilova-parish-saint-george-the-great-martyr", "Parish", "Saint George the Great Martyr Parish in Țepilova", "Parohia „Sfântul Mare Mucenic Gheorghe”, satul Țepilova", "Țepilova", "Sfântul Mare Mucenic Gheorghe", "", 102),
        ("md-bom-soroca-tipordei-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Țipordei", "Parohia „Sfântul Ierarh Nicolae”, satul Țipordei", "Țipordei", "Sfântul Ierarh Nicolae", "", 101),
        ("md-bom-soroca-trifanesti-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Trifănești", "Parohia „Acoperământul Maicii Domnului”, satul Trifănești", "Trifănești", "Acoperământul Maicii Domnului", "", 101),
        ("md-bom-soroca-trifauti-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Trifăuți", "Parohia „Acoperământul Maicii Domnului”, satul Trifăuți", "Trifăuți", "Acoperământul Maicii Domnului", "", 102),
        ("md-bom-soroca-usurei-parish-saint-alexander-nevsky", "Parish", "Saint Alexander Nevsky Parish in Ușurei", "Parohia „Sfântul Cneaz Alexandru Nevski”, satul Ușurei", "Ușurei", "Sfântul Cneaz Alexandru Nevski", "", 103),
        ("md-bom-soroca-vadeni-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Vădeni", "Parohia „ Sfântul Ierarh Nicolae”, satul Vădeni", "Vădeni", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-varancau-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Vărăncău", "Parohia „Adormirea Maicii Domnului”, satul Vărăncău", "Vărăncău", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-varvareuca-parish-miracle-of-the-archangel-michael", "Parish", "Miracle of the Archangel Michael Parish in Vărvăreuca", "Parohia „Minunea Sfântului Arhanghel Mihail”, satul Vărvăreuca", "Vărvăreuca", "Minunea Sfântului Arhanghel Mihail", "", 101),
        ("md-bom-soroca-vascauti-parish-saint-demetrius-the-great-martyr", "Parish", "Saint Demetrius the Great Martyr Parish in Văscăuți", "Parohia „Sfântul Mare Mucenic Dimitrie”, satul Văscăuți", "Văscăuți", "Sfântul Mare Mucenic Dimitrie", "", 101),
        ("md-bom-soroca-vasilcau-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Vasilcău", "Biserica „Adormirea Maicii Domnului”, satul Vasilcău", "Vasilcău", "Adormirea Maicii Domnului", "", 102),
        ("md-bom-soroca-vasilcau-parish-saint-paraskeva", "Parish", "Saint Paraskeva Parish in Vasilcău", "Parohia „Sfânta Cuvioasa Parascheva”, satul Vasilcău", "Vasilcău", "Sfânta Cuvioasa Parascheva", "", 102),
        ("md-bom-soroca-vasiliuti-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Vasiliuți", "Parohia „Acoperământul Maicii Domnului”, satul Vasiliuți", "Vasiliuți", "Acoperământul Maicii Domnului", "", 103),
        ("md-bom-soroca-vertiujeni-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Vertiujeni", "Parohia „Acoperământul Maicii Domnului”, satul Vertiujeni", "Vertiujeni", "Acoperământul Maicii Domnului", "", 101),
        ("md-bom-soroca-visoca-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Visoca", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Visoca", "Visoca", "Sfinții Arhangheli Mihail și Gavriil", "", 102),
        ("md-bom-soroca-voloave-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Voloave", "Parohia „Sfântul Ierarh Nicolae”, satul Voloave", "Voloave", "Sfântul Ierarh Nicolae", "", 102),
        ("md-bom-soroca-volovita-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Volovița", "Parohia „Nașterea Maicii Domnului”, satul Volovița", "Volovița", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-zaluceni-parish-holy-trinity", "Parish", "Holy Trinity Parish in Zăluceni", "Parohia „Sfânta Treime”, satul Zăluceni", "Zăluceni", "Sfânta Treime", "", 101),
        ("md-bom-soroca-zarojeni-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Zarojeni", "Parohia „Nașterea Maicii Domnului”, satul Zarojeni", "Zarojeni", "Nașterea Maicii Domnului", "", 101),
        ("md-bom-soroca-zastanca-parish-apostles-peter-and-paul", "Parish", "Apostles Peter and Paul Parish in Zastînca", "Parohia „Sfinții Apostoli Petru și Pavel”, satul Zastînca", "Zastînca", "Sfinții Apostoli Petru și Pavel", "", 102),
        ("md-bom-soroca-zastanca-parish-nativity-of-the-mother-of-god", "Parish", "Nativity of the Mother of God Parish in Zastînca", "Parohia „Nașterea Maicii Domnului”, satul Zastînca", "Zastînca", "Nașterea Maicii Domnului", "", 102),
        ("md-bom-soroca-zgurita-parish-holy-archangels-michael-and-gabriel", "Parish", "Holy Archangels Michael and Gabriel Parish in Zgurița", "Parohia „Sfinții Arhangheli Mihail și Gavriil”, satul Zgurița", "Zgurița", "Sfinții Arhangheli Mihail și Gavriil", "", 104),
    ),
    "ru-tiraspol": (
        ("md-bom-tiraspol-belochi-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Belochi", "Храм Успения Пресвятой Богородицы", "Белочи", "Успения Пресвятой Богородицы", "с. Белочи, ул. Родина, 26а.", 121),
        ("md-bom-tiraspol-bendery-cathedral-transfiguration-of-the-lord", "Cathedral", "Transfiguration of the Lord Cathedral in Bendery", "Собор Преображения Господня", "Бендеры", "Преображения Господня", "г. Бендеры, ул. Советская, 31.", 122),
        ("md-bom-tiraspol-bendery-chapel-holy-image-of-christ-not-made-by-hands", "Chapel", "Holy Image of Christ Not Made by Hands Chapel in Bendery", "Храм-часовня в честь Образа Спаса Нерукотворного", "Бендеры", "Образа Спаса Нерукотворного", "г. Бендеры, Военно-исторический мемориальный комплекс.", 122),
        ("md-bom-tiraspol-bendery-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Bendery", "Храм Рождества Пресвятой Богородицы", "Бендеры", "Рождества Пресвятой Богородицы", "г. Бендеры, с. Гыска, ул. Ленина, 168.", 122),
        ("md-bom-tiraspol-bendery-church-saint-alexander-nevsky", "Church", "Saint Alexander Nevsky Church in Bendery", "Храм св. блгв. кн. Александра Невского", "Бендеры", "св. блгв. кн. Александра Невского", "г. Бендеры, ул. Панина, 2 (Бендерская крепость).", 122),
        ("md-bom-tiraspol-bendery-church-saint-george-the-victory-bearer", "Church", "Saint George the Victory-Bearer Church in Bendery", "Храм св. вмч. Георгия Победоносца", "Бендеры", "св. вмч. Георгия Победоносца", "г. Бендеры, ул. Космонавтов, 17а.", 122),
        ("md-bom-tiraspol-bendery-church-saints-joachim-and-anna", "Church", "Saints Joachim and Anna Church in Bendery", "Храм прав. Богоотец Иоакима и Анны", "Бендеры", "прав. Богоотец Иоакима и Анны", "г. Бендеры, ул. Ермакова, 22.", 122),
        ("md-bom-tiraspol-bendery-church-sign-icon-of-the-mother-of-god", "Church", "Sign Icon of the Mother of God Church in Bendery", "Храм в честь иконы Божией Матери «Знамение»", "Бендеры", "иконы Божией Матери «Знамение»", "г. Бендеры, ул. Текстильщиков, 6.", 122),
        ("md-bom-tiraspol-bendery-monastery-saints-peter-and-paul", "Monastery", "Saints Peter and Paul Monastery in Bendery", "Женский монастырь в честь свв. первоверховных апп. Петра и Павла", "Бендеры", "свв. первоверховных апп. Петра и Павла", "г. Бендеры, ул. Комсомольская, 44.", 123),
        ("md-bom-tiraspol-bendery-parish-resurrection-of-christ", "Parish", "Resurrection of Christ Parish in Bendery", "Приход Воскресения Христова", "Бендеры", "Воскресения Христова", "г. Бендеры, ул. Интернационалистов, 3.", 122),
        ("md-bom-tiraspol-bendery-parish-saint-andrew-the-fool-for-christ", "Parish", "Saint Andrew the Fool for Christ Parish in Bendery", "Приход блж. Андрея, Христа ради юродивого", "Бендеры", "блж. Андрея, Христа ради юродивого", "г. Бендеры, с. Протягайловка, пер. Первомайский, 6.", 122),
        ("md-bom-tiraspol-bendery-parish-saint-sergius-of-radonezh", "Parish", "Saint Sergius of Radonezh Parish in Bendery", "Приход прп. Сергия Радонежского", "Бендеры", "прп. Сергия Радонежского", "г. Бендеры, ул. 40 лет Победы, 3.", 122),
        ("md-bom-tiraspol-bendery-parish-saint-tikhon-of-moscow", "Parish", "Saint Tikhon of Moscow Parish in Bendery", "Приход свт. Тихона, патриарха Московского и всея России", "Бендеры", "свт. Тихона, патриарха Московского и всея России", "г. Бендеры.", 122),
        ("md-bom-tiraspol-blizhnii-khutor-church-saint-seraphim-of-sarov", "Church", "Saint Seraphim of Sarov Church in Blizhniy Khutor", "Архиерейское подворье прп. Серафима Саровского", "Ближний Хутор", "прп. Серафима Саровского", "с. Ближний Хутор, ул. Ленина, 52.", 124),
        ("md-bom-tiraspol-bolshoi-molokish-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Bolshoy Molokish", "Храм Успения Пресвятой Богородицы", "Большой Молокиш", "Успения Пресвятой Богородицы", "с. Большой Молокиш, пер. Лесной, 3.", 121),
        ("md-bom-tiraspol-butor-parish-archangel-michael", "Parish", "Archangel Michael Parish in Butor", "Приход Архангела Михаила", "Бутор", "Архангела Михаила", "с. Бутор, ул. Ленина, 65.", 125),
        ("md-bom-tiraspol-chobruchi-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Chobruchi", "Храм Покрова Пресвятой Богородицы", "Чобручи", "Покрова Пресвятой Богородицы", "с. Чобручи, ул. Мира, 33а.", 124),
        ("md-bom-tiraspol-delakeu-parish-archangel-michael", "Parish", "Archangel Michael Parish in Delakeu", "Приход Архангела Михаила", "Делакеу", "Архангела Михаила", "с. Делакеу, ул. Мичурина, 55.", 125),
        ("md-bom-tiraspol-dnestrovsk-church-saints-cyril-and-methodius", "Church", "Saints Cyril and Methodius Church in Dnestrovsk", "Храм свв. равноапп. Кирилла и Мефодия", "Днестровск", "свв. равноапп. Кирилла и Мефодия", "г. Днестровск, ул. Строителей, 47/2.", 126),
        ("md-bom-tiraspol-dnestrovsk-parish-prophet-elijah", "Parish", "Prophet Elijah Parish in Dnestrovsk", "Приход пророка Божия Илии", "Днестровск", "пророка Божия Илии", "г. Днестровск.", 126),
        ("md-bom-tiraspol-doibany-church-miracle-of-the-archangel-michael-at-chonae", "Church", "Miracle of the Archangel Michael at Chonae Church in Doybany", "Храм чуда Архангела Михаила в Хонех", "Дойбаны", "чуда Архангела Михаила в Хонех", "с. Дойбаны.", 127),
        ("md-bom-tiraspol-dubossary-cathedral-all-saints", "Cathedral", "All Saints Cathedral in Dubossary", "Кафедральный собор Всех святых", "Дубоссары", "Всех святых", "г. Дубоссары, ул. Ворошилова, 23.", 127),
        ("md-bom-tiraspol-dubossary-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Dubossary", "Храм Успения Пресвятой Богородицы", "Дубоссары", "Успения Пресвятой Богородицы", "г. Дубоссары, ул. Школьная, 10 (м-н Коржево).", 127),
        ("md-bom-tiraspol-dubossary-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Dubossary", "Приход Покрова Пресвятой Богородицы", "Дубоссары", "Покрова Пресвятой Богородицы", "г. Дубоссары, ул. Свердлова, 207 (м-н Лунга).", 127),
        ("md-bom-tiraspol-dubovo-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Dubovo", "Храм Рождества Пресвятой Богородицы", "Дубово", "Рождества Пресвятой Богородицы", "с. Дубово.", 127),
        ("md-bom-tiraspol-dzerzhinskoe-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Dzerzhinskoe", "Приход Покрова Пресвятой Богородицы", "Дзержинское", "Покрова Пресвятой Богородицы", "с. Дзержинское, ул. Кутузова, 28/3.", 127),
        ("md-bom-tiraspol-erzhovo-parish-saint-demetrius-of-thessalonica", "Parish", "Saint Demetrius of Thessalonica Parish in Erzhovo", "Приход св. вмч. Димитрия Солунского", "Ержово", "св. вмч. Димитрия Солунского", "с. Ержово, ул. Ленина, 154а.", 121),
        ("md-bom-tiraspol-frunze-church-community-kazan-icon-of-the-mother-of-god", "Church Community", "Kazan Icon of the Mother of God Church Community in Frunze", "Община Казанской иконы Божией Матери", "Фрунзе", "Казанской иконы Божией Матери", "с. Фрунзе, ул. Советская, 4а.", 124),
        ("md-bom-tiraspol-garaba-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Garaba", "Храм Покрова Пресвятой Богородицы", "Гараба", "Покрова Пресвятой Богородицы", "с. Гараба, ул. Зеленая, 108а.", 121),
        ("md-bom-tiraspol-gidirim-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Gidirim", "Храм Покрова Пресвятой Богородицы", "Гидирим", "Покрова Пресвятой Богородицы", "с. Гидирим, ул. Кирова, 70.", 121),
        ("md-bom-tiraspol-glinoe-church-community-prophet-elijah", "Church Community", "Prophet Elijah Church Community in Glinoe", "Община св. пророка Божия Илии", "Глиное", "св. пророка Божия Илии", "п. Глиное, ул. Гагарина, 63.", 125),
        ("md-bom-tiraspol-glinoe-house-church-saint-nicholas", "House Church", "Saint Nicholas House Church in Glinoe", "Домовая церковь свт. Николая Чудотворца", "Глиное", "свт. Николая Чудотворца", "п. Глиное, УИН №1, ул. Микояна, 60.", 125),
        ("md-bom-tiraspol-glinoe-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Glinoe", "Приход ап. и ев. Иоанна Богослова", "Глиное", "ап. и ев. Иоанна Богослова", "с. Глиное, ул. Мира, 122.", 124),
        ("md-bom-tiraspol-goyan-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Goyan", "Приход св. ап. Иоанна Богослова", "Гоян", "св. ап. Иоанна Богослова", "с. Гоян.", 127),
        ("md-bom-tiraspol-grigoriopol-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Grigoriopol", "Храм Вознесения Господня", "Григориополь", "Вознесения Господня", "г. Григориополь, ул. Шевченко, 11.", 125),
        ("md-bom-tiraspol-grigoriopol-church-community-saint-gregory-the-illuminator", "Church Community", "Saint Gregory the Illuminator Church Community in Grigoriopol", "Община сщмч. Григория еп., просветителя Великой Армении", "Григориополь", "сщмч. Григория еп., просветителя Великой Армении", "г. Григориополь, ул. Карла Маркса.", 125),
        ("md-bom-tiraspol-grigoriopol-house-church-saints-cosmas-and-damian", "House Church", "Saints Cosmas and Damian House Church in Grigoriopol", "Домовая церковь бессребреников Космы и Дамиана", "Григориополь", "бессребреников Космы и Дамиана", "г. Григориополь, Григориопольская центральная районная больница, ул. Урицкого, 130.", 125),
        ("md-bom-tiraspol-grigoriopol-parish-archangel-michael", "Parish", "Archangel Michael Parish in Grigoriopol", "Приход Архангела Михаила", "Григориополь", "Архангела Михаила", "г. Григориополь, с. Красная Горка, ул. Молодежная, 27.", 125),
        ("md-bom-tiraspol-grushka-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Grushka", "Приход Покрова Пресвятой Богородицы", "Грушка", "Покрова Пресвятой Богородицы", "с. Грушка.", 128),
        ("md-bom-tiraspol-kalagur-monastery-saint-john-the-baptist", "Monastery", "Saint John the Baptist Monastery in Kalagur", "Мужской монастырь в честь Пророка, Предтечи и Крестителя Господня Иоанна", "Калагур", "Пророка, Предтечи и Крестителя Господня Иоанна", "Рыбницкий район, урочище Калагур.", 123),
        ("md-bom-tiraspol-kamenka-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Kamenka", "Храм Успения Пресвятой Богородицы", "Каменка", "Успения Пресвятой Богородицы", "г. Каменка, ул. Кирова, 159г.", 128),
        ("md-bom-tiraspol-karagash-church-kazan-icon-of-the-mother-of-god", "Church", "Kazan Icon of the Mother of God Church in Karagash", "Храм Казанской иконы Божией Матери", "Карагаш", "Казанской иконы Божией Матери", "с. Карагаш, ул. Днестровская, 116а.", 124),
        ("md-bom-tiraspol-karmanovo-church-kazan-icon-of-the-mother-of-god", "Church", "Kazan Icon of the Mother of God Church in Karmanovo", "Храм Казанской иконы Божией Матери", "Карманово", "Казанской иконы Божией Матери", "п. Карманово, ул. Октябрьская, 65.", 125),
        ("md-bom-tiraspol-katerinovka-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Katerinovka", "Храм Вознесения Господня", "Катериновка", "Вознесения Господня", "с. Катериновка, ул. Горького, 1.", 128),
        ("md-bom-tiraspol-khrustovaya-church-archangel-michael", "Church", "Archangel Michael Church in Khrustovaya", "Храм Архангела Михаила", "Хрустовая", "Архангела Михаила", "с. Хрустовая.", 128),
        ("md-bom-tiraspol-kolbasna-church-archangel-michael", "Church", "Archangel Michael Church in Kolbasna", "Храм Архангела Михаила", "Колбасна", "Архангела Михаила", "с. Колбасна, ул. Приовражная, 1а.", 121),
        ("md-bom-tiraspol-kolosovo-church-jerusalem-icon-of-the-mother-of-god", "Church", "Jerusalem Icon of the Mother of God Church in Kolosovo", "Храм Иерусалимской иконы Божией Матери", "Колосово", "Иерусалимской иконы Божией Матери", "п. Колосово, ул. Октябрьская, 3.", 125),
        ("md-bom-tiraspol-konstantinovka-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Konstantinovka", "Приход Покрова Пресвятой Богородицы", "Константиновка", "Покрова Пресвятой Богородицы", "с. Константиновка, ул. Карла Маркса, 14а.", 124),
        ("md-bom-tiraspol-korotnoe-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Korotnoe", "Храм Покрова Пресвятой Богородицы", "Коротное", "Покрова Пресвятой Богородицы", "с. Коротное, ул. Фрунзе, 46.", 124),
        ("md-bom-tiraspol-krasnenkoe-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Krasnenkoe", "Приход Успения Пресвятой Богородицы", "Красненькое", "Успения Пресвятой Богородицы", "с. Красненькое, ул. Школьная, 2.", 121),
        ("md-bom-tiraspol-krasnoe-parish-holy-trinity", "Parish", "Holy Trinity Parish in Krasnoe", "Приход Святой Троицы", "Красное", "Святой Троицы", "п. Красное, ул. 40 лет Октября, 11.", 124),
        ("md-bom-tiraspol-krasnogorka-parish-saint-alexander-nevsky", "Parish", "Saint Alexander Nevsky Parish in Krasnogorka", "Приход св. блгв. кн. Александра Невского", "Красногорка", "св. блгв. кн. Александра Невского", "с. Красногорка, ул. Ворошилова, 30а.", 125),
        ("md-bom-tiraspol-krasnyi-oktyabr-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Krasnyy Oktyabr", "Приход Покрова Пресвятой Богородицы", "Красный Октябрь", "Покрова Пресвятой Богородицы", "с. Красный Октябрь.", 128),
        ("md-bom-tiraspol-krasnyi-vinogradar-church-saint-demetrius-of-thessalonica", "Church", "Saint Demetrius of Thessalonica Church in Krasnyy Vinogradar", "Храм св. вмч. Димитрия Солунского", "Красный Виноградарь", "св. вмч. Димитрия Солунского", "с. Красный Виноградарь.", 127),
        ("md-bom-tiraspol-kremenchug-church-saints-faith-hope-love-and-their-mother-sophia", "Church", "Saints Faith, Hope, Love and their mother Sophia Church in Kremenchug", "Архиерейское подворье свв. мцц. Веры, Надежды, Любови и матери их Софии", "Кременчуг", "свв. мцц. Веры, Надежды, Любови и матери их Софии", "с. Кременчуг, ул. Ленина, 41.", 126),
        ("md-bom-tiraspol-malaeshty-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Malaeshty", "Храм Покрова Пресвятой Богородицы", "Малаешты", "Покрова Пресвятой Богородицы", "с. Малаешты, ул. Ленина, 40.", 125),
        ("md-bom-tiraspol-mayak-parish-saint-demetrius-of-thessalonica", "Parish", "Saint Demetrius of Thessalonica Parish in Mayak", "Приход вмч. Димитрия Солунского", "Маяк", "вмч. Димитрия Солунского", "п. Маяк, ул. Мира, 24.", 125),
        ("md-bom-tiraspol-mokra-church-miracle-of-the-archangel-michael-at-chonae", "Church", "Miracle of the Archangel Michael at Chonae Church in Mokra", "Храм чуда Архистратига Михаила в Хонех", "Мокра", "чуда Архистратига Михаила в Хонех", "с. Мокра.", 121),
        ("md-bom-tiraspol-nezavertailovka-parish-dormition-of-the-mother-of-god", "Parish", "Dormition of the Mother of God Parish in Nezavertaylovka", "Приход Успения Пресвятой Богородицы", "Незавертайловка", "Успения Пресвятой Богородицы", "с. Незавертайловка, ул. Жукова, 37.", 124),
        ("md-bom-tiraspol-novo-komissarovka-parish-conception-of-saint-john-the-baptist", "Parish", "Conception of Saint John the Baptist Parish in Novo-Komissarovka", "Приход Зачатия Иоанна Крестителя", "Ново-Комиссаровка", "Зачатия Иоанна Крестителя", "с. Ново-Комиссаровка, ул. Мира, 5.", 127),
        ("md-bom-tiraspol-oknitsa-church-saint-demetrius-of-thessalonica", "Church", "Saint Demetrius of Thessalonica Church in Oknitsa", "Храм св. вмч. Димитрия Солунского", "Окница", "св. вмч. Димитрия Солунского", "с. Окница, ул. Шевченко.", 128),
        ("md-bom-tiraspol-parkany-church-archangel-michael", "Church", "Archangel Michael Church in Parkany", "Храм Архангела Михаила", "Парканы", "Архангела Михаила", "с. Парканы, ул. Благоева, 10.", 124),
        ("md-bom-tiraspol-pgt-pervomaisk-church-miracle-of-the-archangel-michael-at-chonae", "Church", "Miracle of the Archangel Michael at Chonae Church in Pgt Pervomaysk", "Храм чуда Архистратига Михаила в Хонех", "пгт Первомайск", "чуда Архистратига Михаила в Хонех", "пгт Первомайск, ул. Ленина, 105.", 124),
        ("md-bom-tiraspol-plot-church-archangel-michael", "Church", "Archangel Michael Church in Plot", "Храм Архангела Михаила", "Плоть", "Архангела Михаила", "с. Плоть.", 121),
        ("md-bom-tiraspol-podoimitsa-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Podoymitsa", "Храм Рождества Пресвятой Богородицы", "Подоймица", "Рождества Пресвятой Богородицы", "с. Подоймица, ул. Фрунзе.", 128),
        ("md-bom-tiraspol-popenki-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Popenki", "Храм св. ап. Иоанна Богослова", "Попенки", "св. ап. Иоанна Богослова", "с. Попенки, ул. Ленина, 135.", 121),
        ("md-bom-tiraspol-rashkov-church-holy-trinity", "Church", "Holy Trinity Church in Rashkov", "Храм Святой Троицы", "Рашков", "Святой Троицы", "с. Рашков.", 128),
        ("md-bom-tiraspol-rogi-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Rogi", "Архиерейское подворье Покрова Пресвятой Богородицы", "Роги", "Покрова Пресвятой Богородицы", "с. Роги, ул. Днестровская, 57а.", 127),
        ("md-bom-tiraspol-rybnitsa-cathedral-archangel-michael", "Cathedral", "Archangel Michael Cathedral in Rybnitsa", "Собор Архангела Михаила", "Рыбница", "Архангела Михаила", "г. Рыбница, ул. Кирова, 77.", 121),
        ("md-bom-tiraspol-rybnitsa-church-saint-lazarus-the-four-days-dead", "Church", "Saint Lazarus the Four Days Dead Church in Rybnitsa", "Храм прав. Лазаря Четверодневного, еп. Китийского", "Рыбница", "прав. Лазаря Четверодневного, еп. Китийского", "г. Рыбница, городское кладбище.", 121),
        ("md-bom-tiraspol-rybnitsa-house-church-saint-alexander-nevsky", "House Church", "Saint Alexander Nevsky House Church in Rybnitsa", "Домовая церковь св. блгв. кн. Александра Невского", "Рыбница", "св. блгв. кн. Александра Невского", "г. Рыбница, территория 3-й отдельной мотострелковой бригады Министерства обороны ПМР.", 121),
        ("md-bom-tiraspol-rybnitsa-house-church-saint-luke-of-simferopol", "House Church", "Saint Luke of Simferopol House Church in Rybnitsa", "Домовая церковь свт. исп. Луки, архиеп. Симферопольского", "Рыбница", "свт. исп. Луки, архиеп. Симферопольского", "г. Рыбница, Рыбницкая центральная районная больница, ул. Грибоедова, 3.", 121),
        ("md-bom-tiraspol-rybnitsa-parish-entry-of-the-mother-of-god-into-the-temple", "Parish", "Entry of the Mother of God into the Temple Parish in Rybnitsa", "Приход Введения во храм Пресвятой Богородицы", "Рыбница", "Введения во храм Пресвятой Богородицы", "г. Рыбница, ул. Матросова, 12.", 121),
        ("md-bom-tiraspol-severinovka-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Severinovka", "Приход Покрова Пресвятой Богородицы", "Севериновка", "Покрова Пресвятой Богородицы", "с. Севериновка, пер. Вершигоры, 53.", 128),
        ("md-bom-tiraspol-shipka-church-kazan-icon-of-the-mother-of-god", "Church", "Kazan Icon of the Mother of God Church in Shipka", "Храм Казанской иконы Божией Матери", "Шипка", "Казанской иконы Божией Матери", "с. Шипка, ул. Ленина, 107.", 125),
        ("md-bom-tiraspol-sloboda-rashkovo-parish-protection-of-the-mother-of-god", "Parish", "Protection of the Mother of God Parish in Sloboda-Rashkovo", "Приход Покрова Пресвятой Богородицы", "Слобода-Рашково", "Покрова Пресвятой Богородицы", "с. Слобода-Рашково.", 128),
        ("md-bom-tiraspol-slobodzeya-church-archangel-michael", "Church", "Archangel Michael Church in Slobodzeya", "Храм Архангела Михаила", "Слободзея", "Архангела Михаила", "г. Слободзея, ул. Микояна, 17.", 124),
        ("md-bom-tiraspol-slobodzeya-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Slobodzeya", "Храм Успения Пресвятой Богородицы", "Слободзея", "Успения Пресвятой Богородицы", "г. Слободзея, ул. Пушкина, 92.", 124),
        ("md-bom-tiraspol-slobodzeya-house-church-saint-panteleimon", "House Church", "Saint Panteleimon House Church in Slobodzeya", "Домовая церковь св. вмч. Пантелеимона", "Слободзея", "св. вмч. Пантелеимона", "Слободзейская центральная районная больница, г. Слободзея, пер. Больничный, 1.", 124),
        ("md-bom-tiraspol-speya-parish-saint-nicholas", "Parish", "Saint Nicholas Parish in Speya", "Приход свт. Николая Чудотворца", "Спея", "свт. Николая Чудотворца", "с. Спея, ул. Островского, 11.", 125),
        ("md-bom-tiraspol-stroentsy-church-archangel-michael", "Church", "Archangel Michael Church in Stroentsy", "Архиерейское подворье Архангела Михаила", "Строенцы", "Архангела Михаила", "с. Строенцы, ул. Полевая, 7.", 121),
        ("md-bom-tiraspol-sukleya-church-saint-demetrius-of-thessalonica", "Church", "Saint Demetrius of Thessalonica Church in Sukleya", "Храм св. вмч. Димитрия Солунского", "Суклея", "св. вмч. Димитрия Солунского", "с. Суклея, ул. Гагарина, 90б.", 124),
        ("md-bom-tiraspol-tashlyk-church-saint-george-the-victory-bearer", "Church", "Saint George the Victory-Bearer Church in Tashlyk", "Храм вмч. Георгия Победоносца", "Ташлык", "вмч. Георгия Победоносца", "с. Ташлык, ул. Якира, 29а.", 125),
        ("md-bom-tiraspol-ternovka-church-saint-paraskeva-of-serbia", "Church", "Saint Paraskeva of Serbia Church in Ternovka", "Храм прп. Параскевы Сербской", "Терновка", "прп. Параскевы Сербской", "с. Терновка, ул. Ленина, 41г.", 124),
        ("md-bom-tiraspol-tiraspol-cathedral-nativity-of-christ", "Cathedral", "Nativity of Christ Cathedral in Tiraspol", "Кафедральный собор Рождества Христова", "Тирасполь", "Рождества Христова", "г. Тирасполь, ул. Карла Маркса, 81.", 126),
        ("md-bom-tiraspol-tiraspol-church-annunciation", "Church", "Annunciation Church in Tiraspol", "Храм Благовещения Пресвятой Богородицы", "Тирасполь", "Благовещения Пресвятой Богородицы", "г. Тирасполь, ул. Партизанская, 77а.", 126),
        ("md-bom-tiraspol-tiraspol-church-exaltation-of-the-holy-cross", "Church", "Exaltation of the Holy Cross Church in Tiraspol", "Храм Воздвижения Креста Господня", "Тирасполь", "Воздвижения Креста Господня", "г. Тирасполь, ул. Украинская, 4а.", 126),
        ("md-bom-tiraspol-tiraspol-church-new-martyrs-and-confessors-of-the-russian-church", "Church", "New Martyrs and Confessors of the Russian Church Church in Tiraspol", "Храм новомучеников и исповедников Церкви Русской", "Тирасполь", "новомучеников и исповедников Церкви Русской", "г. Тирасполь, ул. Федько, территория Тираспольской крепости (бастион «Святой Владимир»).", 126),
        ("md-bom-tiraspol-tiraspol-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Tiraspol", "Храм Покрова Пресвятой Богородицы", "Тирасполь", "Покрова Пресвятой Богородицы", "г. Тирасполь, ул. Кутузова, 201.", 126),
        ("md-bom-tiraspol-tiraspol-church-saint-andrew-the-first-called", "Church", "Saint Andrew the First-Called Church in Tiraspol", "Архиерейское подворье св. ап. Андрея Первозванного", "Тирасполь", "св. ап. Андрея Первозванного", "г. Тирасполь, ул. Карла Либкнехта, 159.", 126),
        ("md-bom-tiraspol-tiraspol-church-saint-nicholas", "Church", "Saint Nicholas Church in Tiraspol", "Храм свт. Николая Чудотворца", "Тирасполь", "свт. Николая Чудотворца", "г. Тирасполь, пер. Горплавни, 3.", 126),
        ("md-bom-tiraspol-tiraspol-church-saint-yaroslav-the-wise", "Church", "Saint Yaroslav the Wise Church in Tiraspol", "Храм св. блгв. кн. Ярослава Мудрого", "Тирасполь", "св. блгв. кн. Ярослава Мудрого", "г. Тирасполь, кладбище Новое.", 126),
        ("md-bom-tiraspol-tiraspol-house-church-assuage-my-sorrow-icon-of-the-mother-of-god", "House Church", "Assuage My Sorrow Icon of the Mother of God House Church in Tiraspol", "Домовая церковь иконы Божией Матери «Утоли моя печали»", "Тирасполь", "иконы Божией Матери «Утоли моя печали»", "г. Тирасполь, Школа закрытого типа при Республиканском учебно-воспитательном комплексе им. А. С. Макаренко, ул. Заречная, 46.", 126),
        ("md-bom-tiraspol-tiraspol-house-church-holy-royal-martyrs", "House Church", "Holy Royal Martyrs House Church in Tiraspol", "Домовая церковь святых Царственных мучеников", "Тирасполь", "святых Царственных мучеников", "г. Тирасполь, УИН №2, Гребеницкий проезд, 18.", 126),
        ("md-bom-tiraspol-tiraspol-house-church-joy-of-all-who-sorrow-icon-of-the-mother-of-god", "House Church", "Joy of All Who Sorrow Icon of the Mother of God House Church in Tiraspol", "Домовая церковь иконы Божией Матери «Всех скорбящих Радость»", "Тирасполь", "иконы Божией Матери «Всех скорбящих Радость»", "г. Тирасполь, Республиканская клиническая больница, ул. Мира, 33.", 126),
        ("md-bom-tiraspol-tiraspol-house-church-saint-tatiana", "House Church", "Saint Tatiana House Church in Tiraspol", "Домовая церковь св. мц. Татианы", "Тирасполь", "св. мц. Татианы", "г. Тирасполь, ПГУ им. Т. Г. Шевченко, бульвар Гагарина.", 126),
        ("md-bom-tiraspol-tiraspol-house-church-saint-xenia-of-petersburg", "House Church", "Saint Xenia of Petersburg House Church in Tiraspol", "Домовая церковь блж. Ксении Петербургской", "Тирасполь", "блж. Ксении Петербургской", "г. Тирасполь, УИН №3, ул. Сергея Лазо, 7.", 126),
        ("md-bom-tiraspol-tiraspol-monastery-entry-of-the-mother-of-god-and-saint-pachomius", "Monastery", "Entry of the Mother of God and Saint Pachomius Monastery in Tiraspol", "Свято-Введенско-Пахомиев женский монастырь", "Тирасполь", "Свято-Введенско-Пахомиев женский монастырь", "г. Тирасполь, ул. Ленина, 43.", 123),
        ("md-bom-tiraspol-tiraspol-parish-archangel-michael", "Parish", "Archangel Michael Parish in Tiraspol", "Приход Архангела Михаила", "Тирасполь", "Архангела Михаила", "г. Тирасполь, Военный институт МО ПМР, ул. Шевченко, 64а.", 126),
        ("md-bom-tiraspol-tiraspol-parish-saint-matrona-of-moscow", "Parish", "Saint Matrona of Moscow Parish in Tiraspol", "Приход блж. Матроны Московской", "Тирасполь", "блж. Матроны Московской", "г. Тирасполь, микрорайон Октябрьский, ул. Милева.", 126),
        ("md-bom-tiraspol-tiraspol-parish-saint-sabbas-stratelates", "Parish", "Saint Sabbas Stratelates Parish in Tiraspol", "Приход св. мч. Саввы Стратилата", "Тирасполь", "св. мч. Саввы Стратилата", "г. Тирасполь, Республиканский госпиталь инвалидов Великой Отечественной войны, ул. Юности, 33.", 126),
        ("md-bom-tiraspol-tiraspol-parish-transfiguration-of-the-lord", "Parish", "Transfiguration of the Lord Parish in Tiraspol", "Приход Преображения Господня", "Тирасполь", "Преображения Господня", "г. Тирасполь, пос. Новотираспольский, ул. Ленина.", 126),
        ("md-bom-tiraspol-tokmazeya-church-miracle-of-the-archangel-michael-at-chonae", "Church", "Miracle of the Archangel Michael at Chonae Church in Tokmazeya", "Храм чуда Архистратига Михаила в Хонех", "Токмазея", "чуда Архистратига Михаила в Хонех", "с. Токмазея, ул. Ленина, 126.", 125),
        ("md-bom-tiraspol-tsybulevka-parish-archangel-michael", "Parish", "Archangel Michael Parish in Tsybulyovka", "Приход Архангела Михаила", "Цыбулёвка", "Архангела Михаила", "с. Цыбулёвка, ул. Школьная, 3.", 127),
        ("md-bom-tiraspol-ulma-church-community-multiplier-of-wheat-icon-of-the-mother-of-god", "Church Community", "Multiplier of Wheat Icon of the Mother of God Church Community in Ulma", "Община в честь иконы Божией Матери «Спорительница хлебов»", "Ульма", "иконы Божией Матери «Спорительница хлебов»", "с. Ульма.", 121),
        ("md-bom-tiraspol-vadul-turkului-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Vadul-Turkuluy", "Храм Рождества Пресвятой Богородицы", "Вадул-Туркулуй", "Рождества Пресвятой Богородицы", "с. Вадул-Туркулуй, 1-й пер. Артюхова, 4.", 121),
        ("md-bom-tiraspol-valya-adynka-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Valya-Adynka", "Храм Покрова Пресвятой Богородицы", "Валя-Адынка", "Покрова Пресвятой Богородицы", "с. Валя-Адынка, ул. Заречная, 37.", 128),
        ("md-bom-tiraspol-vasilevka-church-life-giving-spring-icon-of-the-mother-of-god", "Church", "Life-Giving Spring Icon of the Mother of God Church in Vasilevka", "Храм в честь иконы Божией Матери «Живоносный источник»", "Васильевка", "иконы Божией Матери «Живоносный источник»", "с. Васильевка.", 121),
        ("md-bom-tiraspol-vinogradnoe-church-saint-demetrius-of-thessalonica", "Church", "Saint Demetrius of Thessalonica Church in Vinogradnoe", "Храм св. вмч. Димитрия Солунского", "Виноградное", "св. вмч. Димитрия Солунского", "с. Виноградное, ул. Ленина, 14.", 125),
        ("md-bom-tiraspol-vladimirovka-parish-saint-john-the-theologian", "Parish", "Saint John the Theologian Parish in Vladimirovka", "Приход ап. и ев. Иоанна Богослова", "Владимировка", "ап. и ев. Иоанна Богослова", "с. Владимировка, ул. Комсомольская, 16а.", 124),
        ("md-bom-tiraspol-voronkovo-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Voronkovo", "Храм Успения Пресвятой Богородицы", "Воронково", "Успения Пресвятой Богородицы", "с. Воронково, ул. Овражная, 10.", 121),
        ("md-bom-tiraspol-vykhvatintsy-church-saint-demetrius-of-thessalonica", "Church", "Saint Demetrius of Thessalonica Church in Vykhvatintsy", "Храм св. вмч. Димитрия Солунского", "Выхватинцы", "св. вмч. Димитрия Солунского", "с. Выхватинцы.", 121),
        ("md-bom-tiraspol-zhura-parish-archangel-michael", "Parish", "Archangel Michael Parish in Zhura", "Приход Архангела Михаила", "Жура", "Архангела Михаила", "с. Жура, ул. Советская, 1.", 121),
        ("md-bom-tiraspol-zozulyany-church-saint-paraskeva-of-serbia", "Church", "Saint Paraskeva of Serbia Church in Zozulyany", "Храм прп. Параскевы Сербской", "Зозуляны", "прп. Параскевы Сербской", "с. Зозуляны.", 121),
    ),
    "ru-ungheni": (
        ("md-bom-ungheni-agronomovca-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Agronomovca", "Biserica „Sf. Ap. Ioan Teologul” din satul Agronomovca", "Agronomovca", "Sf. Ap. Ioan Teologul", "", 129),
        ("md-bom-ungheni-bahmut-church-saint-nicholas", "Church", "Saint Nicholas Church in Bahmut", "Biserica „Sf. Irh. Nicolae” din satul Bahmut", "Bahmut", "Sf. Irh. Nicolae", "", 130),
        ("md-bom-ungheni-balanesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Bălănești", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Bălănești", "Bălănești", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-balauresti-church-saint-nicholas", "Church", "Saint Nicholas Church in Bălăurești", "Biserica „Sf. Irh. Nicolae” din satul Bălăurești", "Bălăurești", "Sf. Irh. Nicolae", "", 131),
        ("md-bom-ungheni-balceana-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Bălceana", "Biserica „Înălțarea Domnului” din satul Bălceana", "Bălceana", "Înălțarea Domnului", "", 132),
        ("md-bom-ungheni-barboieni-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Bărboieni", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Bărboieni", "Bărboieni", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-blindesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Blindești", "Biserica „Adormirea Maicii Domnului” din satul Blindești", "Blindești", "Adormirea Maicii Domnului", "", 129),
        ("md-bom-ungheni-boghiceni-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Boghiceni", "Biserica „Sf. Ap. Petru și Pavel” din satul Boghiceni", "Boghiceni", "Sf. Ap. Petru și Pavel", "", 132),
        ("md-bom-ungheni-bolduresti-church-saint-nicholas", "Church", "Saint Nicholas Church in Boldurești", "Biserica „Sf. Irh. Nicolae” din satul Boldurești", "Boldurești", "Sf. Irh. Nicolae", "", 131),
        ("md-bom-ungheni-boltun-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Bolțun", "Biserica „Acoperământul Maicii Domnului” din satul Bolțun", "Bolțun", "Acoperământul Maicii Domnului", "", 131),
        ("md-bom-ungheni-bratuleni-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Brătuleni", "Biserica „ Ap. Petru și Pavel” din satul Brătuleni", "Brătuleni", "Ap. Petru și Pavel", "", 131),
        ("md-bom-ungheni-bravicea-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Bravicea", "Biserica „Sf. M. Mc. Gheorghe” din satul Bravicea", "Bravicea", "Sf. M. Mc. Gheorghe", "", 130),
        ("md-bom-ungheni-buciumeni-church-all-saints", "Church", "All Saints Church in Buciumeni", "Biserica „Tuturor Sfinților” din satul Buciumeni", "Buciumeni", "Tuturor Sfinților", "", 129),
        ("md-bom-ungheni-buda-church-holy-trinity", "Church", "Holy Trinity Church in Buda", "Biserica „Sf. Treime” din satul Buda", "Buda", "Sf. Treime", "", 130),
        ("md-bom-ungheni-bujor-church-biserica-sf-arh-mihail-si-mihail-din-satul-bujor", "Church", "Church in Bujor", "Biserica „Sf. Arh. Mihail și Mihail” din satul Bujor", "Bujor", "", "", 132),
        ("md-bom-ungheni-bumbata-church-saint-nicholas", "Church", "Saint Nicholas Church in Bumbăta", "Biserica „Sf. Irh. Nicolae” din satul Bumbăta", "Bumbăta", "Sf. Irh. Nicolae", "", 129),
        ("md-bom-ungheni-busila-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Bușila", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Bușila", "Bușila", "Sf. Arh. Mihail și Gavriil", "", 129),
        ("md-bom-ungheni-buteni-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Buțeni", "Biserica „Nașterea Maicii Domnului” din satul Buțeni", "Buțeni", "Nașterea Maicii Domnului", "", 132),
        ("md-bom-ungheni-buteni-church-saint-nicholas", "Church", "Saint Nicholas Church in Buțeni", "Biserica „Sf. Irh. Nicolae” din satul Buțeni", "Buțeni", "Sf. Irh. Nicolae", "", 132),
        ("md-bom-ungheni-buzduganii-de-jos-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Buzduganii de Jos", "Biserica „Nașterea Maicii Domnului” din satul Buzduganii de Jos", "Buzduganii de Jos", "Nașterea Maicii Domnului", "", 129),
        ("md-bom-ungheni-buzduganii-sus-chapel-saint-paraskeva", "Chapel", "Saint Paraskeva Chapel in Buzduganii Sus", "Paraclisul „Sf. Cuv. Parascheva” din satul Buzduganii Sus", "Buzduganii Sus", "Sf. Cuv. Parascheva", "", 129),
        ("md-bom-ungheni-cabaiesti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Căbăiești", "Biserica „Acoperământul Maicii Domnului” din satul Căbăiești", "Căbăiești", "Acoperământul Maicii Domnului", "", 130),
        ("md-bom-ungheni-calarasi-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Călărași", "Biserica „Sf. Ap. Petru și Pavel” din orașul Călărași", "Călărași", "Sf. Ap. Petru și Pavel", "", 130),
        ("md-bom-ungheni-calarasi-church-quick-to-hear-icon-of-the-mother-of-god", "Church", "Quick to Hear Icon of the Mother of God Church in Călăraşi", "Biserica „Icoana Maicii „Grabnică Ascultătoare”” din oraşul Călăraşi", "Călăraşi", "Icoana Maicii „Grabnică Ascultătoare”", "", 130),
        ("md-bom-ungheni-calimanesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Călimănești", "Biserica „Adormirea Maicii Domnului” din satul Călimănești", "Călimănești", "Adormirea Maicii Domnului", "", 131),
        ("md-bom-ungheni-calmatui-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Călmățui", "Biserica „Înălțarea Domnului” din satul Călmățui", "Călmățui", "Înălțarea Domnului", "", 132),
        ("md-bom-ungheni-calmatui-church-saint-prince-vladimir", "Church", "Saint Prince Vladimir Church in Călmățui", "Biserica „Sf. Cneaz Vladimir” din satul Călmățui", "Călmățui", "Sf. Cneaz Vladimir", "", 132),
        ("md-bom-ungheni-caracui-church-saint-nicholas", "Church", "Saint Nicholas Church in Caracui", "Biserica „Sf. Irh. Nicolae” din satul Caracui", "Caracui", "Sf. Irh. Nicolae", "", 132),
        ("md-bom-ungheni-carnesti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Cîrnești", "Biserica „Acoperământul Maicii Domnului” din satul Cîrnești", "Cîrnești", "Acoperământul Maicii Domnului", "", 131),
        ("md-bom-ungheni-carpineni-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Cărpineni", "Biserica „Înălțarea Domnului” din satul Cărpineni", "Cărpineni", "Înălțarea Domnului", "", 132),
        ("md-bom-ungheni-carpineni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Cărpineni", "Biserica „Sf. M. Mc. Gheorghe” din satul Cărpineni", "Cărpineni", "Sf. M. Mc. Gheorghe", "", 132),
        ("md-bom-ungheni-carpineni-church-saint-john-the-baptist", "Church", "Saint John the Baptist Church in Cărpineni", "Biserica „Sf. Ioan Botezătorul” din satul Cărpineni", "Cărpineni", "Sf. Ioan Botezătorul", "", 132),
        ("md-bom-ungheni-chirileni-church-saint-nicholas", "Church", "Saint Nicholas Church in Chirileni", "Biserica „Sf. Irh. Nicolae” din satul Chirileni", "Chirileni", "Sf. Irh. Nicolae", "", 129),
        ("md-bom-ungheni-cioara-church-prophet-elijah", "Church", "Prophet Elijah Church in Cioara", "Biserica „Sf. Proroc Ilie” din satul Cioara", "Cioara", "Sf. Proroc Ilie", "", 132),
        ("md-bom-ungheni-cioresti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Ciorești", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Ciorești", "Ciorești", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-cioropcani-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Cioropcani", "Biserica „Sf. Ap. Ioan Teologul” din satul Cioropcani", "Cioropcani", "Sf. Ap. Ioan Teologul", "", 129),
        ("md-bom-ungheni-ciuciuleni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Ciuciuleni", "Biserica „Sf. M. Mc. Gheorghe” din satul Ciuciuleni", "Ciuciuleni", "Sf. M. Mc. Gheorghe", "", 132),
        ("md-bom-ungheni-ciuciuleni-church-saint-nicholas", "Church", "Saint Nicholas Church in Ciuciuleni", "Biserica „Sf. Irh. Nicolae” din satul Ciuciuleni", "Ciuciuleni", "Sf. Irh. Nicolae", "", 132),
        ("md-bom-ungheni-ciutesti-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Ciutești", "Biserica „Înălțarea Domnului” din satul Ciutești", "Ciutești", "Înălțarea Domnului", "", 131),
        ("md-bom-ungheni-condratesti-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Condrătești", "Biserica „Acoperământul Maicii Domnului” din satul Condrătești", "Condrătești", "Acoperământul Maicii Domnului", "", 129),
        ("md-bom-ungheni-cornesti-church-saint-matthew-the-apostle", "Church", "Saint Matthew the Apostle Church in Cornești", "Biserica „Sf. Ap. Matei” din orașul Cornești", "Cornești", "Sf. Ap. Matei", "", 129),
        ("md-bom-ungheni-cotul-morii-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Cotul Morii", "Biserica „Nașterea Maicii Domnului” din satul Cotul Morii", "Cotul Morii", "Nașterea Maicii Domnului", "", 132),
        ("md-bom-ungheni-cristesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Cristești", "Biserica „Adormirea Maicii Domnului” din satul Cristești", "Cristești", "Adormirea Maicii Domnului", "", 131),
        ("md-bom-ungheni-dahnovici-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Dahnovici", "Biserica „Sf. M. Mc. Gheorghe” din satul Dahnovici", "Dahnovici", "Sf. M. Mc. Gheorghe", "", 132),
        ("md-bom-ungheni-dancu-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Dancu", "Biserica „Sf. M. Mc. Gheorghe” din satul Dancu", "Dancu", "Sf. M. Mc. Gheorghe", "", 132),
        ("md-bom-ungheni-dereneu-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Dereneu", "Biserica „Adormirea Maicii Domnului” din satul Dereneu", "Dereneu", "Adormirea Maicii Domnului", "", 130),
        ("md-bom-ungheni-dragusenii-noi-church-saint-nicholas", "Church", "Saint Nicholas Church in Drăgușenii Noi", "Biserica „Sf. Irh. Nicolae” din satul Drăgușenii Noi", "Drăgușenii Noi", "Sf. Irh. Nicolae", "", 132),
        ("md-bom-ungheni-drojdieni-church-joy-of-all-who-sorrow-icon-of-the-mother-of-god", "Church", "Joy of All Who Sorrow Icon of the Mother of God Church in Drojdieni", "Biserica „Icoana Maicii Domnului „Bucuria Tuturor Scârbiților”” din satul Drojdieni", "Drojdieni", "Icoana Maicii Domnului „Bucuria Tuturor Scârbiților”", "", 131),
        ("md-bom-ungheni-drujba-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Drujba", "Biserica „Sf. M. Mc. Dumitru” din satul Drujba", "Drujba", "Sf. M. Mc. Dumitru", "", 129),
        ("md-bom-ungheni-farladeni-church-saint-theodore-stratelates", "Church", "Saint Theodore Stratelates Church in Fîrlădeni", "Biserica „Sf. M. Mc. Teodor Stratilat” din satul Fîrlădeni", "Fîrlădeni", "Sf. M. Mc. Teodor Stratilat", "", 132),
        ("md-bom-ungheni-floresti-church-three-holy-hierarchs", "Church", "Three Holy Hierarchs Church in Florești", "Biserica „Sf. Trei Ierarhi” din satul Florești", "Florești", "Sf. Trei Ierarhi", "", 129),
        ("md-bom-ungheni-frasinesti-church-saint-nicholas", "Church", "Saint Nicholas Church in Frăsinești", "Biserica „Sf. Irh. Nicolae” din satul Frăsinești", "Frăsinești", "Sf. Irh. Nicolae", "", 129),
        ("md-bom-ungheni-frumoasa-monastery-holy-trinity", "Monastery", "Holy Trinity Monastery in Frumoasa", "Mănăstirea „Sf. Treime„, Frumoasa", "Frumoasa", "Sf. Treime", "MD-4419, s. Frumoasa, r. Călărași", 1),
        ("md-bom-ungheni-fundul-galbenei-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Fundul Galbenei", "Biserica „Sf. Ap. Ioan Teologul” din satul Fundul Galbenei", "Fundul Galbenei", "Sf. Ap. Ioan Teologul", "", 132),
        ("md-bom-ungheni-gaureni-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Găureni", "Biserica „Adormirea Maicii Domnului” din satul Găureni", "Găureni", "Adormirea Maicii Domnului", "", 131),
        ("md-bom-ungheni-gherman-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Gherman", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Gherman", "Gherman", "Sf. Arh. Mihail și Gavriil", "", 129),
        ("md-bom-ungheni-graseni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Grăseni", "Biserica „Acoperământul Maicii Domnului” din satul Grăseni", "Grăseni", "Acoperământul Maicii Domnului", "", 129),
        ("md-bom-ungheni-grozasca-church-saint-basil-the-great", "Church", "Saint Basil the Great Church in Grozasca", "Biserica „Sf. Irh. Vasile cel Mare” din satul Grozasca", "Grozasca", "Sf. Irh. Vasile cel Mare", "", 129),
        ("md-bom-ungheni-grozesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Grozești", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Grozești", "Grozești", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-hancesti-church-saint-nicholas", "Church", "Saint Nicholas Church in Hîncești", "Biserica „Sf. Irh. Nicolae” din municipiul Hîncești", "Hîncești", "Sf. Irh. Nicolae", "", 132),
        ("md-bom-ungheni-hancu-monastery-saint-paraskeva", "Monastery", "Saint Paraskeva Monastery in Hîncu", "Mănăstirea „Sf. Cuv. Parascheva„, Hîncu", "Hîncu", "Sf. Cuv. Parascheva", "MD-6442, s. Bursuc, r. Nisporeni", 1),
        ("md-bom-ungheni-harbovat-monastery-dormition-of-the-mother-of-god", "Monastery", "Dormition of the Mother of God Monastery in Hîrbovăţ", "Mănăstirea „Adormirea Maicii Domnului”, Hîrbovăţ", "Hîrbovăţ", "Adormirea Maicii Domnului", "MD-4422, s. Hîrbovăţ, r. Călăraşi", 1),
        ("md-bom-ungheni-harcesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Hîrcești", "Biserica „Adormirea Maicii Domnului” din satul Hîrcești", "Hîrcești", "Adormirea Maicii Domnului", "", 129),
        ("md-bom-ungheni-harjauca-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Hîrjauca", "Biserica „Sf. Ap. Petru și Pavel” din satul Hîrjauca", "Hîrjauca", "Sf. Ap. Petru și Pavel", "", 130),
        ("md-bom-ungheni-harjauca-monastery-ascension-of-the-lord", "Monastery", "Ascension of the Lord Monastery in Hîrjauca", "Mănăstirea „Înălţarea Domnului”, Hîrjauca", "Hîrjauca", "Înălţarea Domnului", "MD-4421, com. Hîrjauca, r. Călăraşi", 1),
        ("md-bom-ungheni-hirova-church-saint-nicholas", "Church", "Saint Nicholas Church in Hirova", "Biserica „Sf. Irh. Nicolae” din satul Hirova", "Hirova", "Sf. Irh. Nicolae", "", 130),
        ("md-bom-ungheni-hoginesti-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Hoginești", "Biserica „Sf. Cuv. Parascheva” din satul Hoginești", "Hoginești", "Sf. Cuv. Parascheva", "", 130),
        ("md-bom-ungheni-horjesti-church-saint-gregory-the-theologian", "Church", "Saint Gregory the Theologian Church in Horjești", "Biserica „Sf. Irh. Grigore Teologul” din satul Horjești", "Horjești", "Sf. Irh. Grigore Teologul", "", 132),
        ("md-bom-ungheni-horodca-church-kazan-icon-of-the-mother-of-god", "Church", "Kazan Icon of the Mother of God Church in Horodca", "Biserica „Icoana Maicii Domnului din Kazani” din satul Horodca", "Horodca", "Icoana Maicii Domnului din Kazani", "", 132),
        ("md-bom-ungheni-horodiste-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Horodiște", "Biserica „Sf. Cuv. Parascheva” din satul Horodiște", "Horodiște", "Sf. Cuv. Parascheva", "", 130),
        ("md-bom-ungheni-isaicani-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Isăicani", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Isăicani", "Isăicani", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-iurceni-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Iurceni", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Iurceni", "Iurceni", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-ivanovca-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Ivanovca", "Biserica „Acoperământul Maicii Domnului” din satul Ivanovca", "Ivanovca", "Acoperământul Maicii Domnului", "", 132),
        ("md-bom-ungheni-lapusna-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Lăpușna", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Lăpușna", "Lăpușna", "Sf. Arh. Mihail și Gavriil", "", 132),
        ("md-bom-ungheni-leuseni-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Leușeni", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Leușeni", "Leușeni", "Sf. Arh. Mihail și Gavriil", "", 132),
        ("md-bom-ungheni-loganesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Logănești", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Logănești", "Logănești", "Sf. Arh. Mihail și Gavriil", "", 132),
        ("md-bom-ungheni-macaresti-church-saint-gregory-the-theologian", "Church", "Saint Gregory the Theologian Church in Măcărești", "Biserica „Sf. Irh. Grigore Teologul” din satul Măcărești", "Măcărești", "Sf. Irh. Grigore Teologul", "", 129),
        ("md-bom-ungheni-magurele-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Măgurele", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Măgurele", "Măgurele", "Sf. Arh. Mihail și Gavriil", "", 129),
        ("md-bom-ungheni-mandra-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Mîndra", "Biserica „Sf. M. Mc. Dumitru” din satul Mîndra", "Mîndra", "Sf. M. Mc. Dumitru", "", 130),
        ("md-bom-ungheni-manzatesti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Mînzătești", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Mînzătești", "Mînzătești", "Sf. Arh. Mihail și Gavriil", "", 129),
        ("md-bom-ungheni-marinici-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Marinici", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Marinici", "Marinici", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-meleseni-church-ascension-of-the-lord", "Church", "Ascension of the Lord Church in Meleșeni", "Biserica „Înălțarea Domnului” din satul Meleșeni", "Meleșeni", "Înălțarea Domnului", "", 130),
        ("md-bom-ungheni-mereseni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Mereșeni", "Biserica „Sf. M. Mc. Dumitru” din satul Mereșeni", "Mereșeni", "Sf. M. Mc. Dumitru", "", 132),
        ("md-bom-ungheni-milesti-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Milești", "Biserica „Sf. M. Mc. Gheorghe” din satul Milești", "Milești", "Sf. M. Mc. Gheorghe", "", 131),
        ("md-bom-ungheni-mingir-church-saint-nicholas", "Church", "Saint Nicholas Church in Mingir", "Biserica „Sf. Irh. Nicolae” din satul Mingir", "Mingir", "Sf. Irh. Nicolae", "", 132),
        ("md-bom-ungheni-miresti-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Mirești", "Biserica „Sf. Cuv. Parascheva” din satul Mirești", "Mirești", "Sf. Cuv. Parascheva", "", 132),
        ("md-bom-ungheni-morenii-noi-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Morenii Noi", "Biserica „Sf. M. Mc. Dumitru” din satul Morenii Noi", "Morenii Noi", "Sf. M. Mc. Dumitru", "", 129),
        ("md-bom-ungheni-morenii-vechi-church-holy-trinity", "Church", "Holy Trinity Church in Morenii Vechi", "Biserica „Sf. Treime” din satul Morenii Vechi", "Morenii Vechi", "Sf. Treime", "", 129),
        ("md-bom-ungheni-negurenii-vechi-church-holy-trinity", "Church", "Holy Trinity Church in Negurenii Vechi", "Biserica „Sf. Treime” din satul Negurenii Vechi", "Negurenii Vechi", "Sf. Treime", "", 129),
        ("md-bom-ungheni-nemteni-church-saint-john-chrysostom", "Church", "Saint John Chrysostom Church in Nemțeni", "Biserica „Sf. Irh. Ioan Gură de Aur” din satul Nemțeni", "Nemțeni", "Sf. Irh. Ioan Gură de Aur", "", 132),
        ("md-bom-ungheni-niscani-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Nișcani", "Biserica „Sf. Cuv. Parascheva” din satul Nișcani", "Nișcani", "Sf. Cuv. Parascheva", "", 130),
        ("md-bom-ungheni-nisporeni-cathedral-holy-archangels-michael-and-gabriel", "Cathedral", "Holy Archangels Michael and Gabriel Cathedral in Nisporeni", "Catedrala „Sf. Arh. Mihail și Gavriil” din orașul Nisporeni", "Nisporeni", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-nisporeni-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Nisporeni", "Biserica „Adormirea Maicii Domnului” din orașul Nisporeni", "Nisporeni", "Adormirea Maicii Domnului", "", 131),
        ("md-bom-ungheni-nisporeni-church-icon-of-the-mother-of-god-assuage-my-sorrow", "Church", "Icon of the Mother of God Assuage My Sorrow Church in Nisporeni", "Biserica „Icoana Maicii Domnului „Potolește Întristarea Mea” din orașul Nisporeni", "Nisporeni", "Icoana Maicii Domnului „Potolește Întristarea Mea", "", 131),
        ("md-bom-ungheni-novaci-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Novaci", "Biserica „Sf. M. Mc. Gheorghe” din satul Novaci", "Novaci", "Sf. M. Mc. Gheorghe", "", 130),
        ("md-bom-ungheni-obileni-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Obileni", "Biserica „Acoperământul Maicii Domnului” din satul Obileni", "Obileni", "Acoperământul Maicii Domnului", "", 132),
        ("md-bom-ungheni-onesti-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Onești", "Biserica „Sf. M. Mc. Dumitru” din satul Onești", "Onești", "Sf. M. Mc. Dumitru", "", 132),
        ("md-bom-ungheni-oniscani-church-miracle-of-the-archangel-michael", "Church", "Miracle of the Archangel Michael Church in Onișcani", "Biserica „Minunea Sf. Arh. Mihail” din satul Onișcani", "Onișcani", "Minunea Sf. Arh. Mihail", "", 130),
        ("md-bom-ungheni-palanca-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Palanca", "Biserica „Acoperământul Maicii Domnului” din satul Palanca", "Palanca", "Acoperământul Maicii Domnului", "", 130),
        ("md-bom-ungheni-parcani-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Parcani", "Biserica „Nașterea Maicii Domnului” din satul Parcani", "Parcani", "Nașterea Maicii Domnului", "", 130),
        ("md-bom-ungheni-parjolteni-church-saint-nicholas", "Church", "Saint Nicholas Church in Pîrjolteni", "Biserica „Sf. Irh. Nicolae” din satul Pîrjolteni", "Pîrjolteni", "Sf. Irh. Nicolae", "", 130),
        ("md-bom-ungheni-parlita-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Pîrlița", "Biserica „Sf. M. Mc. Dumitru” din satul Pîrlița", "Pîrlița", "Sf. M. Mc. Dumitru", "", 129),
        ("md-bom-ungheni-parlita-church-saint-john-the-baptist", "Church", "Saint John the Baptist Church in Pîrlița", "Biserica „Sf. Ioan Botezătorul” din satul Pîrlița", "Pîrlița", "Sf. Ioan Botezătorul", "", 129),
        ("md-bom-ungheni-paruceni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Păruceni", "Biserica „Sf. M. Mc. Gheorghe” din satul Păruceni", "Păruceni", "Sf. M. Mc. Gheorghe", "", 131),
        ("md-bom-ungheni-pascani-church-prophet-elijah", "Church", "Prophet Elijah Church in Pașcani", "Biserica „Sf. Proroc Ilie” din satul Pașcani", "Pașcani", "Sf. Proroc Ilie", "", 132),
        ("md-bom-ungheni-paulesti-church-saint-nicholas", "Church", "Saint Nicholas Church in Păulești", "Biserica „Sf. Irh. Nicolae” din satul Păulești", "Păulești", "Sf. Irh. Nicolae", "", 130),
        ("md-bom-ungheni-pereni-church-transfiguration-of-the-lord", "Church", "Transfiguration of the Lord Church in Pereni", "Biserica „Schimbarea la Față a Domnului” din satul Pereni", "Pereni", "Schimbarea la Față a Domnului", "", 132),
        ("md-bom-ungheni-peticeni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Peticeni", "Biserica „Sf. M. Mc. Dumitru” din satul Peticeni", "Peticeni", "Sf. M. Mc. Dumitru", "", 130),
        ("md-bom-ungheni-petresti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Petrești", "Biserica „Adormirea Maicii Domnului” din satul Petrești", "Petrești", "Adormirea Maicii Domnului", "", 129),
        ("md-bom-ungheni-pitusca-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Pitușca", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Pitușca", "Pitușca", "Sf. Arh. Mihail și Gavriil", "", 130),
        ("md-bom-ungheni-poganesti-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Pogănești", "Biserica „Adormirea Maicii Domnului” din satul Pogănești", "Pogănești", "Adormirea Maicii Domnului", "", 132),
        ("md-bom-ungheni-raciula-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Răciula", "Biserica „Sf. M. Mc. Dumitru” din satul Răciula", "Răciula", "Sf. M. Mc. Dumitru", "", 130),
        ("md-bom-ungheni-raciula-monastery-nativity-of-the-mother-of-god", "Monastery", "Nativity of the Mother of God Monastery in Răciula", "Mănăstirea „Nașterii Maicii Domnului„, Răciula", "Răciula", "Nașterii Maicii Domnului", "MD-4434, s. Răciula, r. Călărași", 1),
        ("md-bom-ungheni-radeni-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Rădeni", "Biserica „Adormirea Maicii Domnului” din satul Rădeni", "Rădeni", "Adormirea Maicii Domnului", "", 130),
        ("md-bom-ungheni-rezina-church-prophet-elijah", "Church", "Prophet Elijah Church in Rezina", "Biserica „Sf. Proroc Ilie” din satul Rezina", "Rezina", "Sf. Proroc Ilie", "", 129),
        ("md-bom-ungheni-rusca-church-saint-sergius-of-radonezh", "Church", "Saint Sergius of Radonezh Church in Rusca", "Biserica „Sf. Cuv. Serghie de Radonej” (incinta Penitenciarului de femei) din satul Rusca", "Rusca", "Sf. Cuv. Serghie de Radonej", "", 132),
        ("md-bom-ungheni-sarata-galbena-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Sărata-Galbenă", "Biserica „Sf. Cuv. Parascheva” din satul Sărata-Galbenă", "Sărata-Galbenă", "Sf. Cuv. Parascheva", "", 132),
        ("md-bom-ungheni-sculeni-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Sculeni", "Biserica „Nașterea Maicii Domnului” din satul Sculeni", "Sculeni", "Nașterea Maicii Domnului", "", 129),
        ("md-bom-ungheni-sculeni-church-saint-nicholas", "Church", "Saint Nicholas Church in Sculeni", "Biserica „Sf. Irh. Nicolae” din satul Sculeni", "Sculeni", "Sf. Irh. Nicolae", "", 129),
        ("md-bom-ungheni-seliste-church-descent-of-the-holy-spirit", "Church", "Descent of the Holy Spirit Church in Seliște", "Biserica „Pogorârea Sfântului Duh” din satul Seliște", "Seliște", "Pogorârea Sfântului Duh", "", 131),
        ("md-bom-ungheni-selistea-noua-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Seliștea Nouă", "Biserica „Acoperământul Maicii Domnului” din satul Seliștea Nouă", "Seliștea Nouă", "Acoperământul Maicii Domnului", "", 130),
        ("md-bom-ungheni-semeni-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Semeni", "Biserica „Sf. M. Mc. Dumitru” din satul Semeni", "Semeni", "Sf. M. Mc. Dumitru", "", 129),
        ("md-bom-ungheni-sipoteni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Şipoteni", "Biserica „Sf. M. Mc. Gheorghe” din satul Şipoteni", "Şipoteni", "Sf. M. Mc. Gheorghe", "", 132),
        ("md-bom-ungheni-sipoteni-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Sipoteni", "Biserica „Sf. Cuv. Parascheva” din satul Sipoteni", "Sipoteni", "Sf. Cuv. Parascheva", "", 130),
        ("md-bom-ungheni-sipoteni-church-saint-stephen-the-protomartyr", "Church", "Saint Stephen the Protomartyr Church in Sipoteni", "Biserica „Sf. Arhidiacon Ștefan” din satul Sipoteni", "Sipoteni", "Sf. Arhidiacon Ștefan", "", 130),
        ("md-bom-ungheni-siscani-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Șișcani", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Șișcani", "Șișcani", "Sf. Arh. Mihail și Gavriil", "", 131),
        ("md-bom-ungheni-slobozia-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Slobozia", "Biserica „Sf. M. Mc. Dumitru” din s. Slobozia", "Slobozia", "Sf. M. Mc. Dumitru", "", 130),
        ("md-bom-ungheni-sofia-church-saint-john-the-theologian", "Church", "Saint John the Theologian Church in Sofia", "Biserica „Sf. Ap. Ioan Teologul” din satul Sofia", "Sofia", "Sf. Ap. Ioan Teologul", "", 132),
        ("md-bom-ungheni-soltanesti-church-holy-trinity", "Church", "Holy Trinity Church in Soltănești", "Biserica „Sf. Treime” din satul Soltănești", "Soltănești", "Sf. Treime", "", 131),
        ("md-bom-ungheni-temeleuti-church-saint-mary-magdalene", "Church", "Saint Mary Magdalene Church in Temeleuți", "Biserica „Sf. Maria Magdalena” din satul Temeleuți", "Temeleuți", "Sf. Maria Magdalena", "", 130),
        ("md-bom-ungheni-tescureni-church-all-saints", "Church", "All Saints Church in Teșcureni", "Biserica „Tuturor Sfinților” din satul Teșcureni", "Teșcureni", "Tuturor Sfinților", "", 129),
        ("md-bom-ungheni-tibirica-church-saint-nicholas", "Church", "Saint Nicholas Church in Țibirica", "Biserica „Sf. Irh. Nicolae” din satul Țibirica", "Țibirica", "Sf. Irh. Nicolae", "", 130),
        ("md-bom-ungheni-todiresti-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Todirești", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Todirești", "Todirești", "Sf. Arh. Mihail și Gavriil", "", 129),
        ("md-bom-ungheni-tuzara-church-saint-demetrius-the-great-martyr", "Church", "Saint Demetrius the Great Martyr Church in Tuzara", "Biserica „Sf. M. Mc. Dumitru” din satul Tuzara", "Tuzara", "Sf. M. Mc. Dumitru", "", 130),
        ("md-bom-ungheni-ungheni-cathedral-saint-alexander-nevsky", "Cathedral", "Saint Alexander Nevsky Cathedral in Ungheni", "Catedrala Episcopală „Sf. Bn. Cneaz Alexandru Nevski” din municipiul Ungheni", "Ungheni", "Sf. Bn. Cneaz Alexandru Nevski", "", 129),
        ("md-bom-ungheni-ungheni-church-annunciation", "Church", "Annunciation Church in Ungheni", "Biserica „Buna Vestire” din municipiul Ungheni", "Ungheni", "Buna Vestire", "", 129),
        ("md-bom-ungheni-ungheni-church-meeting-of-the-lord", "Church", "Meeting of the Lord Church in Ungheni", "Biserica „Întâmpinarea Domnului” din municipiul Ungheni", "Ungheni", "Întâmpinarea Domnului", "", 129),
        ("md-bom-ungheni-ungheni-church-nativity-of-the-mother-of-god", "Church", "Nativity of the Mother of God Church in Ungheni", "Biserica „Nașterea Maicii Domnului” (cartierul Ungheni-Deal) din municipiul Ungheni", "Ungheni", "Nașterea Maicii Domnului", "", 129),
        ("md-bom-ungheni-ungheni-church-protection-of-the-lord", "Church", "Protection of the Lord Church in Ungheni", "Biserica „Acoperământul Domnului” din municipiul Ungheni", "Ungheni", "Acoperământul Domnului", "", 129),
        ("md-bom-ungheni-ungheni-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Ungheni", "Biserica „Sf. M. Mc. Gheorghe” (cartierul Berești) din municipiul Ungheni", "Ungheni", "Sf. M. Mc. Gheorghe", "", 129),
        ("md-bom-ungheni-ungheni-church-saint-luke-the-apostle", "Church", "Saint Luke the Apostle Church in Ungheni", "Biserica „Sf. Ap. Luca” din municipiul Ungheni", "Ungheni", "Sf. Ap. Luca", "", 129),
        ("md-bom-ungheni-ungheni-monastery-saint-george-the-great-martyr", "Monastery", "Saint George the Great Martyr Monastery in Ungheni", "Mănăstirea „Sf. Mare Mucenic Gheorghe„, Ungheni", "Ungheni", "Sf. Mare Mucenic Gheorghe", "MD-3600, str. Gr. Ureche 3, or. Ungheni", 1),
        ("md-bom-ungheni-untesti-church-all-saints", "Church", "All Saints Church in Unțești", "Biserica „Tuturor Sfinților” din satul Unțești", "Unțești", "Tuturor Sfinților", "", 129),
        ("md-bom-ungheni-valcinet-church-saint-nicholas", "Church", "Saint Nicholas Church in Vălcineț", "Biserica „Sf. Irh. Nicolae” din satul Vălcineț", "Vălcineț", "Sf. Irh. Nicolae", "", 130),
        ("md-bom-ungheni-valea-mare-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Valea Mare", "Biserica „Acoperământul Maicii Domnului” din satul Valea Mare", "Valea Mare", "Acoperământul Maicii Domnului", "", 129),
        ("md-bom-ungheni-valea-trestieni-church-dormition-of-the-mother-of-god", "Church", "Dormition of the Mother of God Church in Valea-Trestieni", "Biserica „Adormirea Maicii Domnului” din satul Valea-Trestieni", "Valea-Trestieni", "Adormirea Maicii Domnului", "", 131),
        ("md-bom-ungheni-vanatori-church-saint-nicholas", "Church", "Saint Nicholas Church in Vînători", "Biserica „Sf. Irh. Nicolae” din satul Vînători", "Vînători", "Sf. Irh. Nicolae", "", 131),
        ("md-bom-ungheni-varzaresti-monastery-nativity-of-the-mother-of-god", "Monastery", "Nativity of the Mother of God Monastery in Vărzărești", "Mănăstirea „Nașterea Maicii Domnului”, Vărzărești", "Vărzărești", "Nașterea Maicii Domnului", "MD- 6439, com. Vărzărești, r. Nisporeni", 1),
        ("md-bom-ungheni-varzaresti-skete-saint-ambrose-of-optina", "Skete", "Saint Ambrose of Optina Skete in Vărzărești", "Schitul de călugărițe „Sfântul Cuvios Ambrozie de la Optina”", "Vărzărești", "Sfântul Cuvios Ambrozie de la Optina", "", 133),
        ("md-bom-ungheni-varzarestii-noi-church-miracle-of-the-archangel-michael", "Church", "Miracle of the Archangel Michael Church in Vărzăreștii Noi", "Biserica „Minunea Sf. Arh. Mihail” din satul Vărzăreștii Noi", "Vărzăreștii Noi", "Minunea Sf. Arh. Mihail", "", 130),
        ("md-bom-ungheni-vatamaneasa-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Vătămăneasa", "Biserica „Sf. Arh. Mihail și Gavriil” din satul Vătămăneasa", "Vătămăneasa", "Sf. Arh. Mihail și Gavriil", "", 130),
        ("md-bom-ungheni-veverita-monastery-joy-of-all-who-sorrow-icon-of-the-mother-of-god", "Monastery", "Joy of All Who Sorrow Icon of the Mother of God Monastery in Veveriţa", "Mănăstirea „Maica Domnului tuturor scârbiţilor”, Veveriţa", "Veveriţa", "Maica Domnului tuturor scârbiţilor", "MD-3631, s. Veveriţa, r. Ungheni", 1),
        ("md-bom-ungheni-voinescu-church-holy-archangels-michael-and-gabriel", "Church", "Holy Archangels Michael and Gabriel Church in Voinescu", "Biserica „Sf. Arh. Mihail şi Gavriil” din satul Voinescu", "Voinescu", "Sf. Arh. Mihail şi Gavriil", "", 132),
        ("md-bom-ungheni-voinescu-church-protection-of-the-mother-of-god", "Church", "Protection of the Mother of God Church in Voinescu", "Biserica „Acoperământul Maicii Domnului” din satul Voinescu", "Voinescu", "Acoperământul Maicii Domnului", "", 132),
        ("md-bom-ungheni-vulcanesti-church-apostles-peter-and-paul", "Church", "Apostles Peter and Paul Church in Vulcănești", "Biserica „Sf. Ap. Petru și Pavel” din satul Vulcănești", "Vulcănești", "Sf. Ap. Petru și Pavel", "", 131),
        ("md-bom-ungheni-vulpesti-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Vulpești", "Biserica „Sf. M. Mc. Gheorghe” din satul Vulpești", "Vulpești", "Sf. M. Mc. Gheorghe", "", 129),
        ("md-bom-ungheni-zagarancea-church-saint-paraskeva", "Church", "Saint Paraskeva Church in Zagarancea", "Biserica „Sf. Cuv. Parascheva” din satul Zagarancea", "Zagarancea", "Sf. Cuv. Parascheva", "", 129),
        ("md-bom-ungheni-zazulenii-vechi-church-saint-george-the-great-martyr", "Church", "Saint George the Great Martyr Church in Zăzulenii Vechi", "Biserica „Sf. M. Mc. Gheorghe” din satul Zăzulenii Vechi", "Zăzulenii Vechi", "Sf. M. Mc. Gheorghe", "", 129),
        ("md-bom-ungheni-zberoaia-church-saint-nicholas", "Church", "Saint Nicholas Church in Zberoaia", "Biserica „Sf. Irh. Nicolae” din satul Zberoaia", "Zberoaia", "Sf. Irh. Nicolae", "", 131),
    ),
}


def structural_rows():
    rows = list(STRUCTURE_ROWS)
    for row_id, parent, name, local, country, seat, address, sources in DEANERIES:
        row = {
            "id": row_id, "parent": parent, "kind": "diocese",
            "rank": "Deanery", "name": name, "local": local, "country": country,
            "sources": sources, "checked": CHECKED,
        }
        if seat:
            row["seat"] = seat
        if address:
            row["address"] = [address]
        rows.append(row)
    return rows


ENGLISH_NAMES = {
    row["id"]: row["name"]
    for row in (*structural_rows(), *EXTERNAL_ROWS)
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for row in (*structural_rows(), *EXTERNAL_ROWS)
    if row.get("seat")
}
for _records in RECORDS.values():
    for (_row_id, _rank, _name, _local, _seat, _dedication,
         _address, _source) in _records:
        ENGLISH_NAMES[_row_id] = _name
        if _seat:
            ENGLISH_SEATS[_seat] = _seat
del _records, _row_id, _rank, _name, _local, _seat, _dedication, _address, _source


def valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def check_row(row, seen):
    row_id = row["id"]
    if row_id in seen:
        raise ValueError(f"duplicate Moldova row: {row_id}")
    if not row.get("local") or not row.get("name"):
        raise ValueError(f"missing name: {row_id}")
    urls = row["sources"]
    if not 1 <= len(urls) <= 3 or any(not valid_url(url) for url in urls):
        raise ValueError(f"invalid sources: {row_id}")
    if row.get("site") and not valid_url(row["site"]):
        raise ValueError(f"invalid site: {row_id}")
    seen.add(row_id)


def build():
    seen = set(RECORDS)
    for row in (*structural_rows(), *EXTERNAL_ROWS):
        check_row(row, seen)
    payloads = {}
    for parent, records in RECORDS.items():
        rows = []
        for row_id, rank, name, local, seat, dedication, address, source in records:
            urls = SOURCES[source]
            row = {
                "id": row_id, "parent": parent, "country": COUNTRY,
                "kind": "monastery" if rank in MONASTIC_RANKS else "parish",
                "rank": rank, "name": name, "local": local, "checked": CHECKED,
                "sources": list(urls), "cite": list(urls),
            }
            if seat:
                row["seat"] = seat
            if dedication:
                row["dedication"] = dedication
            if address:
                row["address"] = [address]
            details = DETAILS.get(row_id, {})
            extra_sources = details.get("sources", [])
            row.update({key: value for key, value in details.items() if key != "sources"})
            row["sources"] = list(dict.fromkeys([*urls, *extra_sources]))
            row["cite"] = list(row["sources"])
            check_row(row, seen)
            rows.append(row)
        payloads[parent] = {"v": 1, "parent": parent, "country": COUNTRY, "rows": rows}
    counts = {parent: len(payload["rows"]) for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError(f"Moldova branch counts changed: {counts}")
    return payloads


def manifest(payloads=None):
    return {
        parent: {"url": f"/data/directory/{parent}.v1.json",
                 "count": len(payload["rows"]), "country": COUNTRY}
        for parent, payload in (payloads or build()).items()
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in payloads.items():
        (OUT / f"{parent}.v1.json").write_bytes(encoded(payload))


def problems(payloads):
    errors = []
    for parent, payload in payloads.items():
        path = OUT / f"{parent}.v1.json"
        if not path.is_file():
            errors.append(f"missing {path.name}")
        elif path.read_bytes() != encoded(payload):
            errors.append(f"stale {path.name}")
    return errors


def check_ledger(payloads):
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    counts = {parent: len(payload["rows"]) for parent, payload in payloads.items()}
    if (ledger["v"] != 1 or ledger["checked"] != CHECKED
            or ledger["countries"] != [COUNTRY]
            or ledger["published_summary"] != {**counts, "total": sum(counts.values())}
            or ledger["structure_ids"] != [row["id"] for row in structural_rows()]
            or ledger["external_ids"] != [row["id"] for row in EXTERNAL_ROWS]):
        raise ValueError("Moldova candidate ledger differs from the inventory")
    seen = set()
    for entry in ledger["candidates"]:
        key = entry["candidate_id"]
        if (key in seen or not entry["reason"] or not entry["status"]
                or not entry["name"] or not entry["sources"]
                or any(not valid_url(url) for url in entry["sources"])):
            raise ValueError(f"invalid Moldova candidate: {key}")
        seen.add(key)
    return len(seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    candidate_count = check_ledger(payloads)
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
    else:
        counts = Counter(row["kind"] for payload in payloads.values() for row in payload["rows"])
        print(f"Moldova: {sum(counts.values())} local rows across {len(payloads)} branches, "
              f"{len(structural_rows())} structural rows, {len(EXTERNAL_ROWS)} external bodies, "
              f"{candidate_count} candidate records")
        print(dict(sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
