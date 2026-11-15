#!/usr/bin/env python3
"""Validated current Eastern Orthodox directory fragments for Mexico.

Only bodies named by a competent current Church source are emitted. Historical,
count-only, map-only, and independently claimed bodies remain in the companion
candidate ledger.

    python tools/directory_mexico.py --check
    python tools/directory_mexico.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "mexico.json"

OCA_PARISHES = "https://www.oca.org/parishes/mexico"
OCA_DIOCESE = "https://www.oca.org/dioceses/diocese-of-mexico"
OCA_LOCAL = "https://www.ocamexico.org/parish.html"
EP_MEXICO = "https://ec-patr.org/entities/iera-mitropoli-meksikoy/"
ANTIOCH_MEXICO = (
    "https://iglesiaortodoxa.org.mx/informacion/arquidiocesis/"
    "parroquias/mexico/"
)
ANTIOCH_CLERGY = (
    "https://iglesiaortodoxa.org.mx/informacion/arquidiocesis/el-clero/"
)
ANTIOCH_SAINT_GEORGE = ANTIOCH_MEXICO + "catedral-de-san-jorge/"
ANTIOCH_SAINT_ANTHONY = ANTIOCH_MEXICO + "monasterio-de-san-antonio-el-grande/"
ANTIOCH_PETER_PAUL = ANTIOCH_MEXICO + "iglesia-de-san-pedro-y-san-pablo/"
ANTIOCH_MERIDA = ANTIOCH_MEXICO + "merida/"
ANTIOCH_TIJUANA = "https://www.iglesiaortodoxa.org.mx/Categorias/Tijuana"
NATIVITY_ROSARITO = "https://www.projectmexico.org/save-the-date-consecration"
MOSCOW_PARISHES = "https://mospatusa.com/parishdirectory.html"
MOSCOW_WEST = "https://ruschurchusa.org/en/zapadnye-shtaty/"
MOSCOW_BODY = "https://patriarchia.ru/org/286"
ROCOR_MONASTERY = (
    "https://directory.synod.com/listing/223/"
    "sacrosanto-monasterio-de-la-santisima-trinidad/"
)
ROCOR_WEST = "https://wadiocese.org/mexico_city"
ROMANIAN_DIRECTORY = (
    "https://www.mitropolia.us/index.php/ro/structura/director-parohii"
)
ROMANIAN_MISSION = (
    "https://www.mitropolia.us/index.php/ro/structure/parish-directory/"
    "1558-misiunea-ortodoxa-romana-sf-ier-iosif-marturisitorul-din-"
    "maramures-cancun-mexic"
)


def body(row_id, parent, name, local, rank, seat, sources, address=None,
         site=None, kind="parish"):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "MX",
        "sources": sources,
    }
    if address:
        row["address"] = address
    if site:
        row["site"] = site
    return row


OCA_ROWS = [
    body(
        "mx-oca-colima-nicholas-myra", "oca-mexico",
        "Saint Nicholas of Myra Orthodox Chapel in Colima",
        "Capilla Ortodoxa de San Nicolás de Mira", "Chapel", "Colima, Colima",
        [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-mexico-city-ascension-cathedral", "oca-mexico",
        "Cathedral of the Ascension of the Lord in Mexico City",
        "Catedral de la Ascensión del Señor", "Cathedral Parish",
        "Mexico City", [OCA_PARISHES, OCA_DIOCESE],
    ),
    body(
        "mx-oca-mexico-city-ascension-monastic-community", "oca-mexico",
        "Monastic Community of the Cathedral of the Ascension in Mexico City",
        "Comunidad Monástica de la Catedral de la Ascensión del Señor",
        "Monastic Community", "Mexico City", [OCA_PARISHES, OCA_LOCAL],
        kind="monastery",
    ),
    body(
        "mx-oca-nezahualcoyotl-holy-trinity-monastic-community", "oca-mexico",
        "Most Holy Trinity Monastic Community in Nezahualcóyotl",
        "Comunidad Monástica de la Santísima Trinidad", "Monastic Community",
        "Nezahualcóyotl, State of Mexico", [OCA_PARISHES, OCA_LOCAL],
        kind="monastery",
    ),
    body(
        "mx-oca-los-reyes-archangel-michael-hermitage", "oca-mexico",
        "Archangel Michael Hermitage in Los Reyes",
        "Eremitorio de San Miguel Arcangel", "Hermitage",
        "Los Reyes, Michoacán", [OCA_PARISHES, OCA_LOCAL], kind="monastery",
    ),
    body(
        "mx-oca-tijuana-andrew-apostle", "oca-mexico",
        "Saint Andrew the Apostle Mission Station in Tijuana",
        "Estación Misionera de San Andrés Apóstol", "Mission Station",
        "Tijuana, Baja California", [OCA_PARISHES, OCA_LOCAL],
        site="https://sandresmexico.org/",
    ),
    body(
        "mx-oca-torreon-mark-evangelist", "oca-mexico",
        "Saint Mark the Evangelist Mission Station in Torreón",
        "Estación Misionera de San Marcos Evangelista", "Mission Station",
        "Torreón, Coahuila", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-san-andres-cholula-archangel-michael", "oca-mexico",
        "Archangel Michael Mission Station in San Andrés Cholula",
        "Estación Misionera de San Miguel Arcángel", "Mission Station",
        "San Andrés Cholula, Puebla", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-tlalnepantla-seraphim-sarov", "oca-mexico",
        "Saint Seraphim of Sarov Mission Station in Tlalnepantla",
        "Estación Misionera de San Serafin de Sarov", "Mission Station",
        "Tlalnepantla de Baz, State of Mexico", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-chihuahua-mark-ephesus", "oca-mexico",
        "Saint Mark of Ephesus Mission Station in Chihuahua",
        "Estación Misionera San Marcos de Éfeso", "Mission Station",
        "Chihuahua, Chihuahua", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-xochistlahuaca-twelve-apostles", "oca-mexico",
        "Holy Twelve Apostles Mission in Xochistlahuaca",
        "Misión de los Santos Doce Apóstoles", "Mission",
        "Xochistlahuaca, Guerrero", [OCA_PARISHES],
    ),
    body(
        "mx-oca-mexico-city-john-baptist", "oca-mexico",
        "Saint John the Baptist Mission in Mexico City",
        "Misión de San Juan el Bautista", "Mission", "Mexico City",
        [OCA_PARISHES],
    ),
    body(
        "mx-oca-guadalupe-protection-theotokos", "oca-mexico",
        "Protection of the Most Holy Theotokos Orthodox Mission in Guadalupe",
        "Misión Ortodoxa de la Protección de la Santísima Theotokos y Siempre Virgen María",
        "Mission", "Guadalupe, Nuevo León", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-ixhuatlan-holy-cross", "oca-mexico",
        "Holy Cross Orthodox Mission in Ixhuatlán de Madero",
        "Misión Ortodoxa de la Santa Cruz", "Mission",
        "Ixhuatlán de Madero, Veracruz", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-guanajuato-holy-trinity", "oca-mexico",
        "Most Holy Trinity Orthodox Mission in Guanajuato",
        "Misión Ortodoxa de la Santísima Trinidad", "Mission",
        "Guanajuato, Guanajuato", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-guadalajara-herman-alaska", "oca-mexico",
        "Saint Herman of Alaska Orthodox Mission Station in Guadalajara",
        "Misión Ortodoxa de San Germán de Alaska - Estación Misionera",
        "Mission Station", "Guadalajara, Jalisco", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-nezahualcoyotl-holy-trinity", "oca-mexico",
        "Most Holy Trinity Parish in Nezahualcóyotl",
        "Parroquia de la Santísima Trinidad", "Parish",
        "Nezahualcóyotl, State of Mexico", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-ecatepec-holy-cross", "oca-mexico",
        "Holy Cross Orthodox Parish in Ecatepec",
        "Parroquia Ortodoxa de la Santa Cruz", "Parish",
        "Ecatepec, State of Mexico", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-chalco-transfiguration", "oca-mexico",
        "Transfiguration of the Lord Orthodox Parish in Chalco",
        "Parroquia Ortodoxa de la Transfiguración del Señor", "Parish",
        "Chalco de Díaz Covarrubias, State of Mexico", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-huehuetla-stephen", "oca-mexico",
        "Saint Stephen Orthodox Parish in Huehuetla",
        "Parroquia Ortodoxa de San Esteban", "Parish", "Huehuetla, Hidalgo",
        [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-mazatan-herman-alaska", "oca-mexico",
        "Saint Herman of Alaska Orthodox Parish in Mazatán",
        "Parroquia Ortodoxa de San Germán de Alaska", "Parish",
        "Mazatán, Chiapas", [OCA_PARISHES, OCA_LOCAL],
    ),
    body(
        "mx-oca-tultepec-james-lesser", "oca-mexico",
        "Apostle James the Less Mission Station in Tultepec",
        "Estación Misionera del Apostol Santiago el Menor", "Mission Station",
        "Tultepec, State of Mexico", [OCA_LOCAL],
    ),
    body(
        "mx-oca-queretaro-peter-paul", "oca-mexico",
        "Saints Peter and Paul Mission Station in Querétaro",
        "Estación Misionera de San Pedro y San Pablo", "Mission Station",
        "Querétaro, Querétaro", [OCA_LOCAL],
    ),
    body(
        "mx-oca-ojuelos-nativity-lord", "oca-mexico",
        "Nativity of Our Lord Orthodox Mission in Ojuelos",
        "Misión Ortodoxa de la Natividad de Nuestro Señor", "Mission",
        "Ojuelos, Jalisco", [OCA_LOCAL],
    ),
    body(
        "mx-oca-zapote-bravo-community", "oca-mexico",
        "Orthodox Community of Zapote Bravo",
        "Comunidad Ortodoxa de Zapote Bravo", "Community",
        "Zapote Bravo, Veracruz", [OCA_LOCAL],
    ),
    body(
        "mx-oca-cruz-blanca-community", "oca-mexico",
        "Orthodox Community of Cruz Blanca",
        "Comunidad Ortodoxa de Cruz Blanca", "Community",
        "Cruz Blanca, Veracruz", [OCA_LOCAL],
    ),
    body(
        "mx-oca-leon-benedict-nursia", "oca-mexico",
        "Saint Benedict of Nursia Mission Station in León",
        "Estación Misionera de San Benito de Nursia", "Mission Station",
        "León, Guanajuato", [OCA_LOCAL],
    ),
]


EP_ROWS = [
    body(
        "mx-ep-naucalpan-holy-wisdom-cathedral", "ep-mexico",
        "Metropolitan Cathedral of the Wisdom of God in Naucalpan",
        "Ἱερός Μητροπολιτικός Ναός τῆς τοῦ Θεοῦ Σοφίας ἐν Μεξικῷ",
        "Cathedral Parish", "Naucalpan de Juárez, State of Mexico", [EP_MEXICO],
        ["Calle Agua Caliente s/n at Saratoga, Colonia Lomas-Hipódromo",
         "Naucalpan de Juárez, State of Mexico 53900, Mexico"],
    ),
    body(
        "mx-ep-guadalajara-greek-orthodox", "ep-mexico",
        "Greek Orthodox Church in Guadalajara",
        "Ἑλληνική Ὀρθόδοξος Ἐκκλησία ἐν Γουδαλαχάρᾳ", "Church",
        "Guadalajara, Jalisco", [EP_MEXICO],
        ["Calle Madero 807, Sector Juárez", "Guadalajara, Jalisco 44100, Mexico"],
    ),
    body(
        "mx-ep-uruapan-apostle-timothy", "ep-mexico",
        "Greek Orthodox Church of Apostle Timothy in Uruapan",
        "Ἑλληνική Ὀρθόδοξος Ἐκκλησία ἐν Οὐρουάπαν-Μιτσοακάν", "Church",
        "Uruapan, Michoacán", [EP_MEXICO],
        ["Constitución 112, Colonia Centro", "Uruapan, Michoacán 60000, Mexico"],
    ),
    body(
        "mx-ep-toluca-dormition-private-chapel", "ep-mexico",
        "Dormition of the Theotokos Private Chapel in Toluca",
        "Ἱερόν Παρεκκλήσιον Κοιμήσεως τῆς Θεοτόκου ἐν Τολούκᾳ",
        "Private Chapel", "Toluca, State of Mexico", [EP_MEXICO],
    ),
    body(
        "mx-ep-san-salvador-el-verde-entrance-theotokos-monastery", "ep-mexico",
        "Entrance of the Theotokos into the Temple Monastery in San Salvador El Verde",
        "Sagrado Monasterio de Entrada de Theotokos en el Templo", "Monastery",
        "San Salvador El Verde, Puebla", [EP_MEXICO],
        ["Calle Francisco I. Madero 33, San Andrés Hueyacatitla",
         "San Salvador El Verde, Puebla 74130, Mexico"], kind="monastery",
    ),
    body(
        "mx-ep-san-salvador-el-verde-prophet-elijah-monastery", "ep-mexico",
        "Prophet Elijah Monastery in San Salvador El Verde",
        "Sagrado Monasterio del Profeta Elías", "Monastery",
        "San Salvador El Verde, Puebla", [EP_MEXICO],
        ["Calle Francisco I. Madero 33, San Andrés Hueyacatitla",
         "San Salvador El Verde, Puebla 74130, Mexico"], kind="monastery",
    ),
    body(
        "mx-ep-tziscao-presentation-lord", "ep-mexico",
        "Presentation of the Lord Orthodox Parish in Tziscao",
        "Parroquia Ortodoxa La Presentación del Señor", "Parish",
        "Tziscao, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-el-horizonte-ephrem-syrian", "ep-mexico",
        "Saint Ephrem the Syrian Orthodox Community in El Horizonte",
        "Iglesia Ortodoxa San Efrén el Sirio", "Community",
        "El Horizonte, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-san-lorenzo-joseph-betrothed", "ep-mexico",
        "Saint Joseph the Betrothed Orthodox Community in San Lorenzo",
        "Iglesia Ortodoxa San José el Prometido", "Community",
        "San Lorenzo, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-rancheria-la-victoria-photini", "ep-mexico",
        "Saint Photini Orthodox Community in Ranchería La Victoria",
        "Iglesia Ortodoxa Santa Fotiní", "Community",
        "Ranchería La Victoria, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-tierra-libertad-cosmas-damian", "ep-mexico",
        "Saints Cosmas and Damian Orthodox Community in Tierra y Libertad",
        "Iglesia Ortodoxa Santos Cosmes y Damián", "Community",
        "Tierra y Libertad, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-nuevo-mundo-theophany", "ep-mexico",
        "Theophany of the Lord Orthodox Community in Nuevo Mundo",
        "Iglesia Ortodoxa La Teofanía del Señor", "Community",
        "Nuevo Mundo, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-badenia-nativity-christ", "ep-mexico",
        "Nativity of Our Lord Jesus Christ Orthodox Community in Badenia",
        "Iglesia Ortodoxa La Natividad de nuestro Señor Jesús Cristo",
        "Community", "Badenia, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-san-vicente-conception-theotokos", "ep-mexico",
        "Conception of the Most Holy Theotokos by Saint Anna Community in San Vicente",
        "La Concepción de la Santísima Virgen María en Santa Ana", "Community",
        "San Vicente, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-santa-rosa-ascension", "ep-mexico",
        "Ascension of the Lord Orthodox Community in Santa Rosa",
        "Iglesia Ortodoxa La Ascensión del Señor", "Community",
        "Santa Rosa, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-la-gloria-constantine-helen", "ep-mexico",
        "Saints Constantine and Helen Orthodox Community in La Gloria",
        "Iglesia Ortodoxa San Constantino y Santa Elena", "Community",
        "La Gloria, Las Margaritas, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-amparo-agua-tinta-nativity-theotokos", "ep-mexico",
        "Nativity of the Theotokos Orthodox Community in Amparo Agua Tinta",
        "Iglesia Ortodoxa La Natividad de La Teotokos", "Community",
        "Amparo Agua Tinta, Las Margaritas, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-cuauhtemoc-victor-damascus", "ep-mexico",
        "Martyr Victor of Damascus Orthodox Community in Cuauhtémoc",
        "Iglesia Ortodoxa Santo Mártir Víctor en Damasco", "Community",
        "Cuauhtémoc, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-santa-rosa-oriente-simeon-anna", "ep-mexico",
        "Righteous Simeon and Anna the Prophetess Orthodox Community in Santa Rosa El Oriente",
        "Iglesia Ortodoxa El Santo y Justo Simeón y Ana la Profetisa",
        "Community", "Santa Rosa El Oriente, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-rancheria-el-mirador-julian-egina", "ep-mexico",
        "Saint Julian the Deacon of Aegina Orthodox Community in Ranchería El Mirador",
        "Iglesia Ortodoxa San Julián el Diácono de Egina", "Community",
        "Ranchería El Mirador, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-san-luis-george", "ep-mexico",
        "Saint George Orthodox Community in San Luis",
        "Iglesia Ortodoxa San Jorge", "Community",
        "San Luis, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-esmeralda-cipreses-sophia", "ep-mexico",
        "Saint Sophia Orthodox Community in La Esmeralda de los Cipreses",
        "Iglesia Ortodoxa Santa Sofia", "Community",
        "La Esmeralda de los Cipreses, Las Margaritas, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-san-caralampio-charalambos", "ep-mexico",
        "Saint Charalambos Orthodox Community in San Caralampio",
        "Iglesia Ortodoxa San Caralampio", "Community",
        "San Caralampio, La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-la-trinitaria-holy-trinity", "ep-mexico",
        "Holy Trinity Orthodox Community in La Trinitaria",
        "Iglesia Ortodoxa La Santísima Trinidad", "Community",
        "La Trinitaria, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-colonia-candelaria-prophet-samuel", "ep-mexico",
        "Prophet Samuel Orthodox Community in Colonia Candelaria",
        "Iglesia Ortodoxa Profeta Samuel", "Community",
        "Colonia Candelaria, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-playa-azul-transfiguration", "ep-mexico",
        "Transfiguration of the Lord Orthodox Community in Playa Azul",
        "Iglesia Ortodoxa La Transfiguración del Señor", "Community",
        "Playa Azul, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-nuevo-progreso-antimus-nicomedia", "ep-mexico",
        "Hieromartyr Antimus of Nicomedia Orthodox Community in Nuevo Progreso",
        "Iglesia Ortodoxa Santo Mártir Antimo, obispo de Nicomedia", "Community",
        "Nuevo Progreso, La Independencia, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-cacahoatan-christ-deliverer", "ep-mexico",
        "Christ the Deliverer Parish in Cacahoatán",
        "Ἐνορία Χριστοῦ Ἐλευθερωτοῦ ἐν Κακαχοατάν", "Parish",
        "Cacahoatán, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-bellavista-apostle-matthias", "ep-mexico",
        "Apostle Matthias Orthodox Parish Church in Bellavista",
        "Parroquia Ortodoxa Apóstol San Matías", "Parish Church",
        "Bellavista, Cacahoatán, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-guatimoc-apostle-philip", "ep-mexico",
        "Apostle Philip Orthodox Community in Guatimoc",
        "Iglesia Ortodoxa San Felipe Apóstol", "Community",
        "Guatimoc, Cacahoatán, Chiapas", [EP_MEXICO],
    ),
    body(
        "mx-ep-aldea-cinco-mayo-apostle-paul", "ep-mexico",
        "Apostle Paul Orthodox Community in Aldea 5 de Mayo",
        "Iglesia Ortodoxa San Pablo", "Community",
        "Aldea 5 de Mayo, Cacahoatán, Chiapas", [EP_MEXICO],
    ),
]


ANTIOCH_ROWS = [
    body(
        "mx-an-mexico-city-saint-george-cathedral", "an-mexico",
        "Saint George Cathedral in Mexico City", "Catedral de San Jorge",
        "Cathedral Parish", "Mexico City", [ANTIOCH_MEXICO, ANTIOCH_SAINT_GEORGE],
        ["Tuxpan 30, Colonia Roma Sur", "Mexico City 06700, Mexico"],
    ),
    body(
        "mx-an-jilotepec-anthony-great-monastery", "an-mexico",
        "Saint Anthony the Great Monastery in Jilotepec",
        "Monasterio de San Antonio el Grande", "Monastery",
        "Jilotepec, State of Mexico", [ANTIOCH_MEXICO, ANTIOCH_SAINT_ANTHONY],
        ["Rancho Los Duraznos, kilometer 2, Comunidad El Xhitey",
         "Jilotepec, State of Mexico 54270, Mexico"], kind="monastery",
    ),
    body(
        "mx-an-huixquilucan-peter-paul-cathedral", "an-mexico",
        "Saints Peter and Paul Cathedral in Huixquilucan",
        "Catedral de San Pedro y San Pablo", "Cathedral Parish",
        "Huixquilucan, State of Mexico", [ANTIOCH_MEXICO, ANTIOCH_PETER_PAUL],
        ["Fraccionamiento Bosque Real, Lot 5, Block 2",
         "Huixquilucan, State of Mexico 52774, Mexico"],
    ),
    body(
        "mx-an-merida-dormition-mother-god", "an-mexico",
        "Dormition of the Mother of God Church in Mérida",
        "Iglesia de la Dormición de la Madre de Dios", "Church",
        "Mérida, Yucatán", [ANTIOCH_MEXICO, ANTIOCH_MERIDA],
        ["Calle 7 B at 18, Santa Gertrudis Copó", "Mérida, Yucatán 97305, Mexico"],
    ),
    body(
        "mx-an-tijuana-innocent-chapel", "an-mexico",
        "Saint Innocent Orthodox Chapel in Tijuana",
        "Capilla de San Inocencio", "Chapel", "Tijuana, Baja California",
        [ANTIOCH_CLERGY, ANTIOCH_TIJUANA],
        ["Orfanato San Inocencio, Del Rocío 354, Aztlán",
         "Tijuana, Baja California 22710, Mexico"],
        site="https://www.projectmexico.org/",
    ),
    body(
        "mx-an-rosarito-nativity-theotokos", "an-mexico",
        "Nativity of the Theotokos Church in Rosarito",
        "Iglesia de la Natividad de la Virgen", "Church",
        "Rosarito, Baja California", [ANTIOCH_CLERGY, NATIVITY_ROSARITO],
        site="https://www.projectmexico.org/",
    ),
]


MOSCOW_ROWS = [
    body(
        "mx-mp-tlalnepantla-protection-theotokos", "mp-parishes-usa",
        "Protection of the Mother of God Church in Tlalnepantla",
        "Покровский храм в Мехико", "Church",
        "Tlalnepantla de Baz, State of Mexico",
        [MOSCOW_PARISHES, MOSCOW_WEST, MOSCOW_BODY],
        ["Avenida Barrios 350, Los Reyes Iztacala",
         "Tlalnepantla de Baz, State of Mexico, Mexico"],
    ),
]


ROCOR_ROWS = [
    body(
        "mx-rocor-mexico-city-holy-trinity-monastery",
        "ru-western-america-rocor", "Holy Trinity Monastery in Mexico City",
        "Sacrosanto Monasterio de la Santisima Trinidad", "Monastery",
        "Mexico City", [ROCOR_MONASTERY, ROCOR_WEST],
        ["Río Danubio 42, Colonia Cuauhtémoc", "Mexico City 06500, Mexico"],
        site="https://www.pravoslavie.mx/", kind="monastery",
    ),
]


ROMANIAN_ROWS = [
    body(
        "mx-ro-cancun-joseph-confessor-maramures", "romanian-americas",
        "Saint Joseph the Confessor of Maramureș Romanian Orthodox Mission in Cancún",
        "Misiunea Ortodoxă Română Sf. Ier. Iosif Mărturisitorul din Maramureș",
        "Mission", "Cancún, Quintana Roo", [ROMANIAN_DIRECTORY, ROMANIAN_MISSION],
        ["Santuario Maria Desatadora de Nudos, Avenida 145 S/N, M1, Lots 01-05, SM 320",
         "Benito Juárez, Cancún, Quintana Roo 77536, Mexico"],
    ),
]


ROWS = {
    "oca-mexico": OCA_ROWS,
    "ep-mexico": EP_ROWS,
    "an-mexico": ANTIOCH_ROWS,
    "mp-parishes-usa": MOSCOW_ROWS,
    "ru-western-america-rocor": ROCOR_ROWS,
    "romanian-americas": ROMANIAN_ROWS,
}

EXPECTED = {
    "oca-mexico": 27,
    "ep-mexico": 31,
    "an-mexico": 6,
    "mp-parishes-usa": 1,
    "ru-western-america-rocor": 1,
    "romanian-americas": 1,
}

ALLOWED_KINDS = {"parish", "monastery"}
ALLOWED_RANKS = {
    "Cathedral Parish", "Parish", "Parish Church", "Church", "Chapel",
    "Private Chapel", "Mission", "Mission Station", "Community",
    "Monastery", "Monastic Community", "Hermitage",
}

ENGLISH_NAMES = {
    row["id"]: row["name"] for row in sum(ROWS.values(), [])
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in sum(ROWS.values(), [])
}


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if row.get("site") and not row["site"].startswith("https://"):
        raise ValueError("%s carries a non-HTTPS site" % row.get("id"))
    return row


def validate_rows(source_rows, parent, all_seen, all_names):
    rows = []
    for source in source_rows:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in all_seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != parent:
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if row.get("country") != "MX":
            raise ValueError("%s is outside Mexico" % row_id)
        if row.get("kind") not in ALLOWED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        name = row.get("name", "")
        local = row.get("local", "")
        seat = row.get("seat", "")
        if not name or not local or not seat:
            raise ValueError("%s lacks a usable name, local name, or seat" % row_id)
        if name[:1].islower() or "  " in name or name.endswith(" -"):
            raise ValueError("%s has malformed English text" % row_id)
        key = name.casefold()
        if key in all_names:
            raise ValueError("duplicate reader-facing name: %s and %s" % (
                all_names[key], row_id,
            ))
        if row.get("address") and (
                not isinstance(row["address"], list) or
                not all(isinstance(value, str) for value in row["address"])):
            raise ValueError("%s has an invalid address" % row_id)
        rendered = json.dumps(row, ensure_ascii=False)
        if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
            raise ValueError("%s has forbidden punctuation or encoding" % row_id)
        all_seen.add(row_id)
        all_names[key] = row_id
        rows.append(row)
    return rows


def build_all():
    all_seen = set()
    all_names = {}
    payloads = {}
    for parent, source_rows in ROWS.items():
        rows = validate_rows(source_rows, parent, all_seen, all_names)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "MX",
            "rows": rows,
        }
    row_ids = {
        row["id"] for payload in payloads.values() for row in payload["rows"]
    }
    seats = {
        row["seat"] for payload in payloads.values() for row in payload["rows"]
    }
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 67:
        raise ValueError("Mexico English name map is out of sync")
    if set(ENGLISH_SEATS) != seats:
        raise ValueError("Mexico English seat map is out of sync")
    if sum(len(payload["rows"]) for payload in payloads.values()) != 67:
        raise ValueError("Mexico branch total must remain 67")
    return payloads


def build():
    return build_all()


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "MX":
        raise ValueError("Mexico candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Mexico candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("worship_bodies") != 67:
        raise ValueError("Mexico candidate ledger total is out of sync")
    required_lists = ("candidates", "exclusions", "official_jurisdiction_audit")
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Mexico candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "MX":
            raise ValueError("%s is outside Mexico" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Mexico candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Mexico ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Mexico ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Mexico candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build_all()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Mexico: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(
            {"branches": payloads}, ensure_ascii=False, indent=2, sort_keys=True,
        ))
    else:
        print("Mexico: 67 verified worship bodies across 6 branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
