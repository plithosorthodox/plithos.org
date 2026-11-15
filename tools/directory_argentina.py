#!/usr/bin/env python3
"""Validated current Eastern Orthodox directory fragments for Argentina.

Only bodies named by a competent current Church source are emitted. Historical,
construction-only, administrative, and search-discovered bodies remain in the
companion candidate ledger.

    python tools/directory_argentina.py --check
    python tools/directory_argentina.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "argentina.json"

EP_BUENOS_AIRES = (
    "https://ec-patr.org/entities/iera-mitropoli-mpoyenos-aires/"
)
ANTIOCH_PARISHES = "https://iglesiaortodoxa.ar/parroquias"
ANTIOCH_DIRECTORY = (
    "https://www.antiochpatriarchate.org/images/pages/"
    "dalil-2025-final2024-12-18-12-31-19.pdf"
)
SERBIAN_DIRECTORY = (
    "https://www.iglesiaortodoxaserbiasca.org/_files/ugd/"
    "e8757a_bcd3fd85dc81441196589a1b3065f8bd.pdf"
)
SERBIAN_DIOCESE = "https://www.iglesiaortodoxaserbiasca.org/diocesis"
MOSCOW_ROSTER = "https://southamerica.cerkov.ru/xramy-eparxii/"
MOSCOW_DIOCESE = "https://patriarchia.ru/org/141"
ROCOR_DIRECTORY = "https://directory.synod.com/listings/"
ROCOR_DIOCESE = "https://iglesiarusa.info/"
EP_UKRAINIANS = (
    "https://ec-patr.org/entities/orthodoksoi-oykranoi-stis-ipa/"
)
UOCUSA_SOBOR = "https://www.uocofusa.org/news_250908_1"
ROMANIAN_DIRECTORY = (
    "https://www.mitropolia.us/index.php/en/structure/parish-directory"
)
ROMANIAN_ALMANAC = "https://www.mitropolia.us/pdf/2025.05.15-almanah.pdf"


def body(row_id, parent, name, local, rank, sources, address=None,
         site=None, kind="parish"):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "AR",
        "checked": CHECKED,
        "sources": sources,
    }
    if address:
        row["address"] = address
    if site:
        row["site"] = site
    return row


EP_GREEK_ROWS = [
    body(
        "ar-ep-buenos-aires-dormition-cathedral", "ep-buenos-aires",
        "Cathedral of the Dormition of the Theotokos in Buenos Aires",
        "Ἱερός Καθεδρικός Ναός Κοιμήσεως τῆς Θεοτόκου",
        "Cathedral Parish", [EP_BUENOS_AIRES],
        ["Julián Álvarez 1030", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-buenos-aires-saint-nicholas", "ep-buenos-aires",
        "Saint Nicholas Church in Buenos Aires",
        "Ἱερός Ναός Ἁγίου Νικολάου", "Church", [EP_BUENOS_AIRES],
        ["Avenida Rabanal 1418", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-remedios-escalada-archangel-michael", "ep-buenos-aires",
        "Archangel Michael Church in Remedios de Escalada",
        "Ἱερός Ναός τοῦ Ταξιάρχου Μιχαήλ", "Church", [EP_BUENOS_AIRES],
        ["Azopardo 150", "Remedios de Escalada, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-olivos-holy-spirit", "ep-buenos-aires",
        "Holy Spirit Church in Olivos", "Ἱερός Ναός τοῦ Ἁγίου Πνεύματος",
        "Church", [EP_BUENOS_AIRES],
        ["Avellaneda 3255", "Olivos, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-berisso-constantine-helen", "ep-buenos-aires",
        "Saints Constantine and Helen Church in Berisso",
        "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης", "Church",
        [EP_BUENOS_AIRES],
        ["Domingo Liveratto 4202", "Berisso, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-mar-del-plata-saint-george", "ep-buenos-aires",
        "Saint George Church in Mar del Plata", "Ἱερός Ναός Ἁγίου Γεωργίου",
        "Church", [EP_BUENOS_AIRES],
        ["Falucho 4456", "Mar del Plata, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-cordoba-john-forerunner", "ep-buenos-aires",
        "Saint John the Forerunner Church in Córdoba",
        "Ἱερός Ναός τοῦ Τιμίου Προδρόμου", "Church", [EP_BUENOS_AIRES],
        ["Santa Rosa 1130", "Córdoba, Argentina"],
    ),
    body(
        "ar-ep-comodoro-rivadavia-saint-nicholas", "ep-buenos-aires",
        "Saint Nicholas Church in Comodoro Rivadavia",
        "Ἱερός Ναός Ἁγίου Νικολάου", "Church", [EP_BUENOS_AIRES],
        ["Italia 722", "Comodoro Rivadavia, Chubut, Argentina"],
    ),
    body(
        "ar-ep-rosario-saint-nicholas", "ep-buenos-aires",
        "Saint Nicholas Church in Rosario", "Ἱερός Ναός Ἁγίου Νικολάου",
        "Church", [EP_BUENOS_AIRES],
        ["Salta 1756", "Rosario, Santa Fe, Argentina"],
    ),
    body(
        "ar-ep-buenos-aires-saint-eleutherius-chapel", "ep-buenos-aires",
        "Metropolitan Chapel of Saint Eleutherius in Buenos Aires",
        "Μητροπολιτικόν Παρεκκλήσιον τοῦ Ἁγίου Ἐλευθερίου", "Chapel",
        [EP_BUENOS_AIRES],
        ["Avenida Figueroa Alcorta 3187", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-buenos-aires-saint-spyridon-chapel", "ep-buenos-aires",
        "Saint Spyridon Chapel in Buenos Aires Province",
        "Ἱερόν Παρεκκλήσιον τοῦ Ἁγίου Σπυρίδωνος", "Chapel",
        [EP_BUENOS_AIRES],
        [
            "Campo de Deportes y Recreación Olimpia",
            "Ruta 8, kilometer 33 1/2, Buenos Aires Province, Argentina",
        ],
    ),
    body(
        "ar-ep-esteban-echeverria-saint-nectarios-chapel",
        "ep-buenos-aires", "Saint Nectarios Chapel in Esteban Echeverría",
        "Ἱερόν Παρεκκλήσιον τοῦ Ἁγίου Νεκταρίου", "Chapel",
        [EP_BUENOS_AIRES],
        [
            "Panelinion, Perú 1815, Barrio 9 de Abril",
            "Esteban Echeverría, Buenos Aires, Argentina",
        ],
    ),
    body(
        "ar-ep-buenos-aires-john-chrysostom-chapel", "ep-buenos-aires",
        "Saint John Chrysostom Chapel of the Cathedral in Buenos Aires",
        "Ἱερόν Παρεκκλήσιον τοῦ Ἁγίου Ἰωάννου Χρυσοστόμου", "Chapel",
        [EP_BUENOS_AIRES],
        ["Julián Álvarez 1040", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-ep-buenos-aires-holy-cross-chapel", "ep-buenos-aires",
        "Holy Cross Chapel in the Metropolitan Offices in Buenos Aires",
        "Ἱερόν Παρεκκλήσιον τοῦ Τιμίου Σταυροῦ", "Chapel",
        [EP_BUENOS_AIRES],
    ),
]


ANTIOCH_ROWS = [
    body(
        "ar-an-buenos-aires-saint-george-cathedral", "an-buenos-aires",
        "Saint George Cathedral in Buenos Aires", "Catedral San Jorge",
        "Cathedral Parish", [ANTIOCH_PARISHES, ANTIOCH_DIRECTORY],
        ["Scalabrini Ortiz 1261", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-an-cordoba-saint-george", "an-buenos-aires",
        "Saint George Parish in Córdoba", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES], ["Avenida Maipú 66", "Córdoba, Argentina"],
    ),
    body(
        "ar-an-mendoza-saint-george", "an-buenos-aires",
        "Saint George Parish in Mendoza", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES], ["Mitre 1823", "Mendoza, Argentina"],
    ),
    body(
        "ar-an-tucuman-dormition-theotokos", "an-buenos-aires",
        "Dormition of the Most Holy Theotokos Parish in San Miguel de Tucumán",
        "Parroquia Asunción de María Santísima", "Parish",
        [ANTIOCH_PARISHES],
        ["Batalla de Maipú 567", "San Miguel de Tucumán, Argentina"],
    ),
    body(
        "ar-an-salta-saint-george", "an-buenos-aires",
        "Saint George Parish in Salta", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES], ["Pellegrini 250", "Salta, Argentina"],
    ),
    body(
        "ar-an-rosario-saint-george", "an-buenos-aires",
        "Saint George Parish in Rosario", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES], ["Italia 1145", "Rosario, Santa Fe, Argentina"],
    ),
    body(
        "ar-an-santiago-estero-saint-george", "an-buenos-aires",
        "Saint George Parish in Santiago del Estero", "Parroquia San Jorge",
        "Parish", [ANTIOCH_PARISHES],
        ["Absalón Rojas 363", "Santiago del Estero, Argentina"],
    ),
    body(
        "ar-an-pergamino-saint-george", "an-buenos-aires",
        "Saint George Parish in Pergamino", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES],
        ["Monteagudo 240", "Pergamino, Buenos Aires, Argentina"],
    ),
    body(
        "ar-an-junin-saint-george", "an-buenos-aires",
        "Saint George Parish in Junín", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES], ["Alsina 282", "Junín, Buenos Aires, Argentina"],
    ),
    body(
        "ar-an-esperanza-saint-george", "an-buenos-aires",
        "Saint George Parish in Esperanza", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES],
        ["9 de Julio 1824", "Esperanza, Santa Fe, Argentina"],
    ),
    body(
        "ar-an-santa-fe-saint-elijah", "an-buenos-aires",
        "Saint Elijah Parish in Santa Fe", "Parroquia San Elías", "Parish",
        [ANTIOCH_PARISHES], ["Alvear 3720", "Santa Fe, Argentina"],
    ),
    body(
        "ar-an-reconquista-saint-george", "an-buenos-aires",
        "Saint George Parish in Reconquista", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES], ["General Obligado 329", "Reconquista, Santa Fe, Argentina"],
    ),
    body(
        "ar-an-tartagal-saint-elijah", "an-buenos-aires",
        "Saint Elijah Parish in Tartagal", "Parroquia San Elías", "Parish",
        [ANTIOCH_PARISHES], ["Cornejo 209", "Tartagal, Salta, Argentina"],
    ),
    body(
        "ar-an-las-talitas-saint-george", "an-buenos-aires",
        "Saint George Parish in Las Talitas", "Parroquia San Jorge", "Parish",
        [ANTIOCH_PARISHES],
        ["Calle 3 at Calle 12, Villa Mariano Moreno", "Las Talitas, Tucumán, Argentina"],
    ),
]


SERBIAN_ROWS = [
    body(
        "ar-sr-buenos-aires-nativity-cathedral", "sr-buenos-aires",
        "Cathedral of the Nativity of the Virgin in Buenos Aires",
        "Catedral de la Natividad de la Virgen", "Cathedral Parish",
        [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["15 de Noviembre de 1889 1536", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-sr-buenos-aires-saint-sava-monastery", "sr-buenos-aires",
        "Saint Sava Monastery in Buenos Aires", "Monasterio San Sava",
        "Monastery", [SERBIAN_DIRECTORY, SERBIAN_DIOCESE],
        ["Perú 1656", "Buenos Aires, Argentina"], kind="monastery",
    ),
    body(
        "ar-sr-machagai-saint-nicholas", "sr-buenos-aires",
        "Saint Nicholas Parish in Machagai", "Parroquia San Nicolás",
        "Parish", [SERBIAN_DIRECTORY],
        ["Adelina Roig Flores s/n", "Machagai, Chaco, Argentina"],
    ),
    body(
        "ar-sr-resistencia-holy-trinity", "sr-buenos-aires",
        "Holy Trinity Parish in Resistencia", "Parroquia de la Santa Trinidad",
        "Parish", [SERBIAN_DIRECTORY],
        ["Nikola Tesla s/n", "Resistencia, Chaco, Argentina"],
    ),
    body(
        "ar-sr-venado-tuerto-archangel-michael", "sr-buenos-aires",
        "Archangel Michael Parish in Venado Tuerto",
        "Parroquia San Miguel Arcángel", "Parish", [SERBIAN_DIRECTORY],
        ["P. José I. Maxwell 964", "Venado Tuerto, Santa Fe, Argentina"],
    ),
    body(
        "ar-sr-general-madariaga-peter-njegos", "sr-buenos-aires",
        "Saint Peter II Njegoš Parish in General Juan Madariaga",
        "Parroquia San Pedro II Njegos", "Parish", [SERBIAN_DIRECTORY],
        [
            "Avenida Buenos Aires 2279",
            "General Juan Madariaga, Buenos Aires, Argentina",
        ],
    ),
    body(
        "ar-sr-las-grutas-saint-paraskeva", "sr-buenos-aires",
        "Saint Paraskeva Mission in Las Grutas", "Misión Santa Paraskeva",
        "Mission", [SERBIAN_DIRECTORY],
        ["Punta Delgado 1150", "Las Grutas, Río Negro, Argentina"],
    ),
]


MOSCOW_ROWS = [
    body(
        "ar-ru-buenos-aires-annunciation-cathedral",
        "ru-argentina-and-south-america",
        "Annunciation Cathedral in Buenos Aires",
        "Благовещенский кафедральный собор Буэнос-Айреса",
        "Cathedral Parish", [MOSCOW_ROSTER, MOSCOW_DIOCESE],
        ["Bulnes 1743", "Buenos Aires, Argentina"],
    ),
    body(
        "ar-ru-lanus-all-saints-russia", "ru-argentina-and-south-america",
        "Church of All Saints Who Shone Forth in the Russian Land in Lanús Oeste",
        "Храм всех святых в земле Российской просиявших в провинции Лянус-Оэсте",
        "Church", [MOSCOW_ROSTER],
        ["Estados Unidos 3686", "Lanús Oeste, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ru-san-martin-job-pochaev", "ru-argentina-and-south-america",
        "Saint Job of Pochaev Church in San Martín",
        "Храм преподобного Иова Почаевского в городе Сан-Мартин",
        "Church", [MOSCOW_ROSTER],
        ["Ballester 2989", "San Martín, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ru-mar-del-plata-royal-passion-bearers",
        "ru-argentina-and-south-america",
        "Holy Royal Passion-Bearers Church in Mar del Plata",
        "Храм Царственных Страстотерпцев в городе Мар-дель-Плата",
        "Church", [MOSCOW_ROSTER],
        ["Borthaburu 5007 at Astor Piazzolla", "Mar del Plata, Buenos Aires, Argentina"],
    ),
    body(
        "ar-ru-obera-holy-trinity", "ru-argentina-and-south-america",
        "Holy Trinity Church in Oberá", "Храм Святой Троицы в городе Оберá",
        "Church", [MOSCOW_ROSTER],
        ["Taruma 43", "Oberá, Misiones, Argentina"],
    ),
    body(
        "ar-ru-ameghino-entrance-theotokos", "ru-argentina-and-south-america",
        "Entrance of the Theotokos Parish in Ameghino",
        "Приход Введения во Храм Пресвятой Богородицы в Амегино",
        "Parish", [MOSCOW_ROSTER],
        ["Ameghino, Los Helechos District", "Misiones, Argentina"],
    ),
    body(
        "ar-ru-bajo-troncho-dormition", "ru-argentina-and-south-america",
        "Dormition of the Theotokos Parish in Bajo Troncho",
        "Приход Успения Пресвятой Богородицы в Бахо Трончо",
        "Parish", [MOSCOW_ROSTER],
        ["Colonia Bajo Troncho, Los Helechos", "Misiones, Argentina"],
    ),
    body(
        "ar-ru-gobernador-lopez-all-saints-russia",
        "ru-argentina-and-south-america",
        "Parish of All Saints Who Shone Forth in the Russian Land in Gobernador López",
        "Приход всех святых в земле Российской просиявших в Гобернадор Лопес",
        "Parish", [MOSCOW_ROSTER],
        ["Gobernador López, Guaraní District", "Misiones, Argentina"],
    ),
    body(
        "ar-ru-picada-yapeyu-resurrection", "ru-argentina-and-south-america",
        "Resurrection of Christ Parish in Picada Yapeyú",
        "Приход Воскресения Христова в Пикадо Жапежу", "Parish",
        [MOSCOW_ROSTER], ["Picada Yapeyú", "Misiones, Argentina"],
    ),
    body(
        "ar-ru-gobernador-lanusse-saint-nicholas",
        "ru-argentina-and-south-america",
        "Saint Nicholas Church in Gobernador Lanusse",
        "Храм святителя Николая чудотворца в Гобернадор Лянус",
        "Church", [MOSCOW_ROSTER],
        ["Colonia Gobernador Lanusse, Wanda", "Misiones, Argentina"],
    ),
]


def rocor(row_id, name, local, rank, detail, address=None):
    return body(
        row_id, "ru-south-america-rocor", name, local, rank,
        [ROCOR_DIRECTORY, detail], address=address, site=detail,
    )


ROCOR_ROWS = [
    rocor(
        "ar-rocor-la-bolsa-saint-nicholas-chapel",
        "Saint Nicholas Russian Orthodox Chapel in La Bolsa",
        "Capilla Orthodoxa Rusa San Nicolas", "Chapel",
        "https://directory.synod.com/listing/10/capilla-orthodoxa-rusa-san-nicolas/",
        ["Villa El Descanso", "La Bolsa, Córdoba 5189, Argentina"],
    ),
    rocor(
        "ar-rocor-buenos-aires-resurrection-cathedral",
        "Russian Orthodox Cathedral of the Resurrection in Buenos Aires",
        "Catedral Ortodoxa Rusa de la Resurreccion", "Cathedral Parish",
        "https://directory.synod.com/listing/7/catedral-ortodoxa-rusa-de-la-resurreccion/",
        ["Núñez 3541", "Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-san-isidro-buenos-aires-demetrios",
        "Church of the Great Martyr Demetrios in San Isidro, Buenos Aires",
        "Church of the Great-Martyr Demetrios", "Church",
        "https://directory.synod.com/listing/5/church-of-the-great-martyr-demetrios/",
    ),
    rocor(
        "ar-rocor-temperley-protection-theotokos",
        "Russian Orthodox Church of the Protection of the Virgin in Temperley",
        "Iglesia Ortodoxa Rusa de la Virgen del Amparo", "Church",
        "https://directory.synod.com/listing/3/iglesia-ortodoxa-rusa-de-la-virgen-del-amraro/",
        ["Anchorena 665", "Temperley, Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-tres-capones-protection-theotokos",
        "Russian Orthodox Church of the Protection of the Virgin in Tres Capones",
        "Iglesia Ortodoxa Rusa de la Virgen del Amparo", "Church",
        "https://directory.synod.com/listing/12/iglesia-ortodoxa-rusa-de-la-virgen-del-amraro/",
        ["Lote Agrícola 52", "Tres Capones, Misiones, Argentina"],
    ),
    rocor(
        "ar-rocor-quilmes-saint-hermogenes",
        "Russian Orthodox Church of Saint Hermogenes in Quilmes",
        "Iglesia Ortodoxa Rusa de San Germogen", "Church",
        "https://directory.synod.com/listing/1/iglesia-ortodoxa-rusa-de-san-germogen/",
        ["Vélez Sarsfield at Lavalleja", "Quilmes, Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-villa-ballester-saint-vladimir",
        "Russian Orthodox Church of Saint Vladimir in Villa Ballester",
        "Iglesia Ortodoxa Rusa de San Vladimiro", "Church",
        "https://directory.synod.com/listing/6/iglesia-ortodoxa-rusa-de-san-vladimiro/",
        ["San Martín 344", "Villa Ballester, Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-ituzaingo-all-saints-russia",
        "Russian Orthodox Church of All Saints of Russia in Ituzaingó",
        "Iglesia Ortodoxa Rusa de Todos los Santos de Rusia", "Church",
        "https://directory.synod.com/listing/4/iglesia-ortodoxa-rusa-de-todos-los-santos-de-rusia/",
        ["Malabia 1253, Villa Ariza", "Ituzaingó, Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-villa-ballester-saint-sergius",
        "Saint Sergius Russian Orthodox Church in Villa Ballester",
        "Iglesia Ortodoxa Rusa San Sergio", "Church",
        "https://directory.synod.com/listing/2/iglesia-ortodoxa-rusa-san-sergio/",
        ["San Vladimir 2045", "Villa Ballester, Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-obera-elevation-cross", "Elevation of the Cross Church in Oberá",
        "Elevation of the Cross Church", "Church",
        "https://directory.synod.com/listing/11/elevation-of-the-cross-church/",
    ),
    rocor(
        "ar-rocor-buenos-aires-holy-trinity-cathedral",
        "Holy Trinity Cathedral in Buenos Aires", "Holy Trinity Cathedral",
        "Cathedral Parish",
        "https://directory.synod.com/listing/8/holy-trinity-cathedral/",
        ["Brasil 315", "Buenos Aires, Argentina"],
    ),
    rocor(
        "ar-rocor-san-isidro-misiones-demetrios",
        "Church of the Great Martyr Demetrios of Thessalonica in San Isidro, Misiones",
        "Iglesia del Gran Mártir Demetrio de Tesalónica", "Church",
        "https://directory.synod.com/listing/13/iglesia-de-san-velmucho-demetrio-de-tesala-nica/",
    ),
]


UKRAINIAN_ROWS = [
    body(
        "ar-ep-ukrainian-buenos-aires-protection-cathedral",
        "ep-ukrainian-south-america",
        "Protection of the Mother of God Cathedral in Buenos Aires",
        "Catedral Protecion de La Madre de Dios", "Cathedral Parish",
        [EP_UKRAINIANS, UOCUSA_SOBOR],
    ),
    body(
        "ar-ep-ukrainian-villa-caraza-resurrection",
        "ep-ukrainian-south-america",
        "Resurrection of the Lord Parish in Villa Caraza",
        "Ressurrecion del Senhor", "Parish",
        [EP_UKRAINIANS, UOCUSA_SOBOR],
    ),
    body(
        "ar-ep-ukrainian-berisso-holy-trinity",
        "ep-ukrainian-south-america", "Holy Trinity Parish in Berisso",
        "Santíssima Trinidad", "Parish", [EP_UKRAINIANS, UOCUSA_SOBOR],
    ),
    body(
        "ar-ep-ukrainian-san-bernardo-holy-trinity",
        "ep-ukrainian-south-america", "Holy Trinity Parish in San Bernardo",
        "SS. Trinidad", "Parish", [EP_UKRAINIANS, UOCUSA_SOBOR],
    ),
    body(
        "ar-ep-ukrainian-la-tigra-saint-george",
        "ep-ukrainian-south-america", "Saint George Parish in La Tigra",
        "San Jorge", "Parish", [EP_UKRAINIANS, UOCUSA_SOBOR],
    ),
    body(
        "ar-ep-ukrainian-las-brenas-protection",
        "ep-ukrainian-south-america",
        "Protection of the Mother of God Parish in Las Breñas",
        "Protecion de La Madre de Dios", "Parish",
        [EP_UKRAINIANS, UOCUSA_SOBOR],
    ),
]


ROMANIAN_ROWS = [
    body(
        "ar-ro-buenos-aires-apostle-andrew", "romanian-americas",
        "Saint Apostle Andrew Romanian Orthodox Mission in Buenos Aires",
        "Saint Apostle Andrew Romanian Orthodox Mission, Buenos Aires, Argentina",
        "Mission",
        [ROMANIAN_DIRECTORY, ROMANIAN_ALMANAC],
    ),
]


ROWS = {
    "ep-buenos-aires": EP_GREEK_ROWS,
    "an-buenos-aires": ANTIOCH_ROWS,
    "sr-buenos-aires": SERBIAN_ROWS,
    "ru-argentina-and-south-america": MOSCOW_ROWS,
    "ru-south-america-rocor": ROCOR_ROWS,
    "ep-ukrainian-south-america": UKRAINIAN_ROWS,
    "romanian-americas": ROMANIAN_ROWS,
}

CONSTANTINOPLE_ROWS = [
    body(
        "ep-ukrainian-south-america", "constantinople",
        "Ukrainian Orthodox Eparchy of South America",
        "Ukrainian Orthodox Eparchy of South America", "Eparchy",
        [EP_UKRAINIANS, UOCUSA_SOBOR], kind="diocese",
    ),
]

EXPECTED = {
    "ep-buenos-aires": 14,
    "an-buenos-aires": 14,
    "sr-buenos-aires": 7,
    "ru-argentina-and-south-america": 10,
    "ru-south-america-rocor": 12,
    "ep-ukrainian-south-america": 6,
    "romanian-americas": 1,
}
CONSTANTINOPLE_EXPECTED = 1
ALLOWED_KINDS = {"parish", "monastery", "diocese"}
ALLOWED_RANKS = {
    "Cathedral Parish", "Parish", "Church", "Chapel", "Mission",
    "Monastery", "Eparchy",
}

ENGLISH_NAMES = {
    row["id"]: row["name"]
    for row in sum(ROWS.values(), []) + CONSTANTINOPLE_ROWS
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
        if row.get("country") != "AR":
            raise ValueError("%s is outside Argentina" % row_id)
        if row.get("kind") not in ALLOWED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if row.get("rank") not in ALLOWED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        name = row.get("name", "")
        local = row.get("local", "")
        if not name or not local:
            raise ValueError("%s lacks a usable local or English name" % row_id)
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
    all_seen = {"constantinople"}
    all_names = {}
    spine = validate_rows(
        CONSTANTINOPLE_ROWS, "constantinople", all_seen, all_names,
    )
    if len(spine) != CONSTANTINOPLE_EXPECTED:
        raise ValueError("Constantinople spine count changed: %d" % len(spine))
    payloads = {}
    for parent, source_rows in ROWS.items():
        rows = validate_rows(source_rows, parent, all_seen, all_names)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "AR",
            "rows": rows,
        }
    row_ids = {
        row["id"] for payload in payloads.values() for row in payload["rows"]
    } | {row["id"] for row in spine}
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != 65:
        raise ValueError("Argentina English name map is out of sync")
    if sum(len(payload["rows"]) for payload in payloads.values()) != 64:
        raise ValueError("Argentina branch total must remain 64")
    return payloads, spine


def build():
    return build_all()[0]


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "AR":
        raise ValueError("Argentina candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Argentina candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if (summary.get("worship_bodies") != 64 or
            summary.get("total_rows_including_eparchy") != 65):
        raise ValueError("Argentina candidate ledger totals are out of sync")
    required_lists = ("candidates", "exclusions", "official_jurisdiction_audit")
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Argentina candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "AR":
            raise ValueError("%s is outside Argentina" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Argentina candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Argentina ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Argentina ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Argentina candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads, spine = build_all()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Argentina: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(
            {
                "branches": payloads,
                "constantinople_spine_rows": spine,
            },
            ensure_ascii=False, indent=2, sort_keys=True,
        ))
    else:
        print(
            "Argentina: 64 verified worship bodies across 7 branches plus "
            "1 Constantinople eparchy row"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
