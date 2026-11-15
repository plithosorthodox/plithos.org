#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Egypt.

The current first-party records of the Patriarchate of Alexandria, the
Church of Sinai, and the Moscow Patriarchate establish the bodies below.
The existing autonomous Church, patriarchal, metropolitan, and eparchial
rows are not duplicated here.

    python tools/directory_egypt.py --check
    python tools/directory_egypt.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "egypt.json"
CHECKED = "2026-11-15"

AX_COMMISSIONS = (
    "https://www.patriarchateofalexandria.com/to-patriarcheio/"
    "dioikitiki-organosi/patriarchikes-epitropeies/"
)
AX_SAVVAS = (
    "https://www.patriarchateofalexandria.com/the-patriarchate/"
    "patriarchiki-moni-osioy-savva/?lang=en"
)
AX_GEORGE = (
    "https://www.patriarchateofalexandria.com/the-patriarchate/"
    "patriarchiki-moni-agioy-georgioy/?lang=en"
)
AX_NICHOLAS_WOMEN = (
    "https://www.patriarchateofalexandria.com/"
    "idrysi-gynaikeias-ieras-patriarchikis-monis-kai-monachiki-koyra-dyo-"
    "neon-monazoyson/"
)
AX_NEW_CAPITAL = (
    "https://www.patriarchateofalexandria.com/"
    "o-patriarchis-theodoros-v-chtizei-to-ayrio-toy-patriarcheioy-stin-aigypto/"
)
AX_PELUSIUM = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-mitropoli-piloysioy/"
)
AX_PORT_SAID = (
    "https://www.patriarchateofalexandria.com/"
    "patriarchiki-theia-leitoyrgia-stin-kathedra-tis-i-mitropoleos-piloysioy/"
)
AX_PORT_SAID_CURRENT = (
    "https://www.patriarchateofalexandria.com/"
    "enthronisi-toy-sev-mitropolitoy-piloysioy-k-nifonos-ypo-tis-athm/"
)

SINAI_CAIRO_EN = (
    "https://www.sinaimonastery.com/index.php/en/description/"
    "shrines-dependencies/cairo-dependency"
)
SINAI_CAIRO_EL = (
    "https://www.sinaimonastery.com/index.php/el/"
    "%CF%80%CE%B5%CF%81%CE%B9%CE%B3%CF%81%CE%B1%CF%86%CE%B7/"
    "%CE%BC%CE%B5%CF%84%CE%BF%CF%87%CE%B9%CE%B1-%CE%BA%CE%B1%CE%B9-"
    "%CE%BA%CE%B1%CE%B8%CE%B9%CF%83%CE%BC%CE%B1%CF%84%CE%B1/"
    "%CE%BC%CE%B5%CF%84%CE%BF%CF%87%CE%B9-%CF%84%CE%BF%CF%85-"
    "%CE%BA%CE%B1%CF%8A%CF%81%CE%BF%CF%85"
)
SINAI_RAITHO_EN = (
    "https://www.sinaimonastery.com/st-catherine/index.php/en/description/"
    "shrines-dependencies/raitho-el-tur"
)
SINAI_RAITHO_EL = (
    "https://www.sinaimonastery.com/index.php/el/"
    "%CF%80%CE%B5%CF%81%CE%B9%CE%B3%CF%81%CE%B1%CF%86%CE%B7/"
    "%CE%BC%CE%B5%CF%84%CE%BF%CF%87%CE%B9%CE%B1-%CE%BA%CE%B1%CE%B9-"
    "%CE%BA%CE%B1%CE%B8%CE%B9%CF%83%CE%BC%CE%B1%CF%84%CE%B1/"
    "%CF%81%CE%B1%CF%8A%CE%B8%CF%89"
)
SINAI_PHARAN_EN = (
    "https://www.sinaimonastery.com/index.php/en/description/"
    "shrines-dependencies/pharan"
)
SINAI_PHARAN_EL = (
    "https://www.sinaimonastery.com/index.php/el/"
    "%CF%80%CE%B5%CF%81%CE%B9%CE%B3%CF%81%CE%B1%CF%86%CE%B7/"
    "%CE%BC%CE%B5%CF%84%CE%BF%CF%87%CE%B9%CE%B1-%CE%BA%CE%B1%CE%B9-"
    "%CE%BA%CE%B1%CE%B8%CE%B9%CF%83%CE%BC%CE%B1%CF%84%CE%B1/"
    "%CF%86%CE%B1%CF%81%CE%B1%CE%BD"
)
SINAI_TARFA_EN = (
    "https://sinaimonastery.com/index.php/en/description/"
    "shrines-dependencies/tarfa"
)
SINAI_TARFA_EL = (
    "https://sinaimonastery.com/st-catherine/index.php/el/"
    "%CF%80%CE%B5%CF%81%CE%B9%CE%B3%CF%81%CE%B1%CF%86%CE%B7/"
    "%CE%BC%CE%B5%CF%84%CE%BF%CF%87%CE%B9%CE%B1-%CE%BA%CE%B1%CE%B9-"
    "%CE%BA%CE%B1%CE%B8%CE%B9%CF%83%CE%BC%CE%B1%CF%84%CE%B1/"
    "%CF%84%CE%B1%CF%81%CF%86%CE%B1"
)

RU_EGYPT = "https://exarchate-africa.ru/dioceses_cat/egipet/"
RU_CAIRO = "https://exarchate-africa.ru/dioceses/prihod-v-kaire/"
RU_CAIRO_CURRENT = (
    "https://exarchate-africa.ru/novosti/"
    "v-den-pamyati-prepodobnogo-sergiya-radonezhskogo-mitropolit-konstantin-"
    "vozglavil-prestolnye-torzhestva-v-kaire/"
)
RU_GIZA = "https://exarchate-africa.ru/dioceses/hram-sv-vmch-miny/"
RU_GIZA_DECR = "https://mospat.ru/en/news/90331/"
RU_HURGHADA = "https://exarchate-africa.ru/dioceses/prihod-v-hurgade/"
RU_HURGHADA_CURRENT = (
    "https://exarchate-africa.ru/novosti/"
    "vikarij-patriarshego-ekzarhata-afriki-episkop-evfimij-sovershil-liturgiyu-"
    "na-prihode-svyatyh-zhen-mironosicz-v-hurgade/"
)
RU_MADINA = (
    "https://exarchate-africa.ru/dioceses/"
    "prihod-prp-serafima-sarovskogo-v-pos-madina/"
)
RU_MADINA_CURRENT = (
    "https://exarchate-africa.ru/novosti/"
    "prestolnyj-prazdnik-otmetili-na-prihode-prepodobnogo-serafima-sarovskogo-"
    "v-poselke-madina-egipet/"
)
RU_EL_DABAA = (
    "https://exarchate-africa.ru/novosti/"
    "episkop-luhoviczkij-evfimij-sovershil-pervuyu-liturgiyu-v-hrame-vseh-"
    "svyatyh-v-zemle-egipetskoj-prosiyavshih-v-g-el-dabaa-egipet/"
)
RU_EL_DABAA_CONSECRATION = (
    "https://exarchate-africa.ru/en/news/"
    "the-chairman-of-the-decr-attended-the-minor-consecration-of-a-church-at-"
    "the-construction-site-of-the-el-dabaa-nuclear-power-plant-in-egypt/"
)


def body(row_id, parent, name, local, seat, rank, sources,
         kind="parish", address=None):
    return {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "EG",
        "address": address,
        "sources": sources,
    }


AX_ROWS = [
    body(
        "eg-ax-alexandria-savvas-monastery", "alexandria",
        "Patriarchal Monastery of Saint Savvas the Sanctified in Alexandria",
        "Ιερά Πατριαρχική Μονή Οσίου Σάββα του Ηγιασμένου Αλεξανδρείας",
        "Alexandria", "Patriarchal Monastery", [AX_COMMISSIONS, AX_SAVVAS],
        kind="monastery",
    ),
    body(
        "eg-ax-alexandria-savvas-patriarchal-church",
        "eg-ax-alexandria-savvas-monastery",
        "Patriarchal Church of Saint Savvas the Sanctified at Saint Savvas Monastery",
        "Ιερός Πατριαρχικός Ναός Οσίου Σάββα του Ηγιασμένου",
        "Alexandria", "Patriarchal Church", [AX_COMMISSIONS, AX_SAVVAS],
    ),
    body(
        "eg-ax-alexandria-annunciation", "alexandria",
        "Church of the Annunciation of the Theotokos in Alexandria",
        "Ιερός Ναός Ευαγγελισμού της Θεοτόκου", "Alexandria", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-nicholas-womens-monastery", "alexandria",
        "Women's Patriarchal Monastery of Saint Nicholas in Ibrahimiya",
        "Ιερά Μονή Αγίου Νικολάου Ιμβραημίας",
        "Alexandria", "Patriarchal Monastery",
        [AX_COMMISSIONS, AX_NICHOLAS_WOMEN], kind="monastery",
    ),
    body(
        "eg-ax-alexandria-dormition-arabic-community", "alexandria",
        "Church of the Dormition of the Theotokos of the Arabic-speaking Community",
        "Ιερός Ναός Κοιμήσεως της Θεοτόκου", "Alexandria", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-archangels", "alexandria",
        "Church of the Holy Archangels in Alexandria",
        "Ιερός Ναός Παμμεγίστων Ταξιαρχών", "Alexandria", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-sidi-bishr-paraskevi", "alexandria",
        "Patriarchal Church of Saint Paraskevi in Sidi Bishr",
        "Ιερός Πατριαρχικός Ναός Αγίας Παρασκευής Σίντι Μπίσρ",
        "Sidi Bishr", "Patriarchal Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-anthony-arabic-community", "alexandria",
        "Church of Saint Anthony of the Arabic-speaking Community",
        "Ιερός Ναός Αγίου Αντωνίου", "Alexandria", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-aboukir-unmercenaries", "alexandria",
        "Patriarchal Church of the Holy Unmercenaries in Aboukir",
        "Ιερός Πατριαρχικός Ναός Αγίων Αναργύρων Αμπουκίρ",
        "Aboukir", "Patriarchal Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-george-retirement-home", "alexandria",
        "Church of Saint George in the Antoniades-Kaniskereios Retirement Home",
        "Ιερός Ναός Αγίου Γεωργίου",
        "Alexandria", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-catherine-consulate", "alexandria",
        "Church of Saint Catherine in the Consulate General of Greece in Alexandria",
        "Ιερός Ναός Αγίας Αικατερίνης εντός του Γενικού Ελληνικού Προξενείου Αλεξανδρείας",
        "Alexandria", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-john-forerunner-hospital", "alexandria",
        "Church of Saint John the Forerunner in the Kotsikeion Hospital",
        "Ιερός Ναός Τιμίου Προδρόμου",
        "Alexandria", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-dormition-greek-cemetery", "alexandria",
        "Church of the Dormition of the Theotokos in the Greek Community Cemetery",
        "Ιερός Ναός Κοιμήσεως της Θεοτόκου εντός του Κοιμητηρίου της Ελληνικής Κοινότητας Αλεξανδρείας",
        "Alexandria", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-joseph-arimathea-cemetery", "alexandria",
        "Church of Joseph of Arimathea in the Arabic-speaking Community Cemetery",
        "Ιερός Ναός Ιωσήφ του από Αριμαθαίας εντός του Κοιμητηρίου της Κοινότητας Αραβοφώνων",
        "Alexandria", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-holy-theodores-chapel", "alexandria",
        "Chapel of the Holy Theodores in the Patriarchal Mansion",
        "Ιερό Παρεκκλήσιο Αγίων Θεοδώρων",
        "Alexandria", "Chapel", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-alexandria-mark-nectarios-chapel",
        "eg-ax-alexandria-savvas-monastery",
        "Chapel of Saint Mark the Evangelist and Saint Nectarios at Saint Savvas Monastery",
        "Ιερό Παρεκκλήσιο Αποστόλου και Ευαγγελιστού Μάρκου και Αγίου Νεκταρίου εντός της Ιεράς Πατριαρχικής Μονής Αγίου Σάββα",
        "Alexandria", "Chapel", [AX_COMMISSIONS, AX_SAVVAS],
    ),
    body(
        "eg-ax-cairo-nicholas-monastery", "alexandria",
        "Patriarchal Monastery of Saint Nicholas in Cairo",
        "Ιερά Πατριαρχική Μονή Αγίου Νικολάου Καΐρου", "Cairo",
        "Patriarchal Monastery", [AX_COMMISSIONS], kind="monastery",
    ),
    body(
        "eg-ax-cairo-nicholas-patriarchal-church",
        "eg-ax-cairo-nicholas-monastery",
        "Patriarchal Church of Saint Nicholas at Saint Nicholas Monastery",
        "Ιερός Πατριαρχικός Ναός του Αγίου Νικολάου",
        "Cairo", "Patriarchal Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-cairo-constantine-helen", "alexandria",
        "Church of Saints Constantine and Helen in Cairo",
        "Ιερός Ναός των Αγίων Κωνσταντίνου και Ελένης", "Cairo", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-cairo-michael-gabriel", "alexandria",
        "Church of the Archangels Michael and Gabriel in Cairo",
        "Ιερός Ναός των Αρχαγγέλων Μιχαήλ και Γαβριήλ", "Cairo", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-cairo-unmercenaries", "alexandria",
        "Patriarchal Church of the Holy Unmercenaries in Cairo",
        "Ιερός Πατριαρχικός Ναός των Αγίων Αναργύρων", "Cairo",
        "Patriarchal Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-heliopolis-flight-egypt-cathedral", "alexandria",
        "Cathedral of the Theotokos in Heliopolis, the Flight into Egypt",
        "Ιερός Καθεδρικός Ναός Θεοτόκου εν Ηλιουπόλει (Η φυγή εις Αίγυπτον)",
        "Heliopolis", "Cathedral", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-helwan-spyridon", "alexandria",
        "Patriarchal Church of Saint Spyridon in Helwan",
        "Ιερός Πατριαρχικός Ναός του Αγίου Σπυρίδωνος",
        "Helwan", "Patriarchal Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-zeitoun-demetrius", "alexandria",
        "Church of Saint Demetrius in Zeitoun",
        "Ιερός Ναός του Αγίου Δημητρίου", "Zeitoun", "Church",
        [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-cairo-nicholas-arabic-retirement-home", "alexandria",
        "Church of Saint Nicholas in the Arabic-speaking Community Retirement Home",
        "Ιερός Ναός Αγίου Νικολάου εντός του Γηροκομείου της Ελληνορθοδόξου Κοινότητος των Αραβοφώνων Καΐρου",
        "Cairo", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-cairo-panteleimon-hospital", "alexandria",
        "Church of Saint Panteleimon in the Greek Community Hospital",
        "Ιερός Ναός του Αγίου Παντελεήμονος",
        "Cairo", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-heliopolis-entry-theotokos-orphanage", "alexandria",
        "Church of the Entry of the Theotokos in the Spetseropouleion Orphanage",
        "Ιερός Ναός των Εισοδίων της Θεοτόκου",
        "Heliopolis", "Church", [AX_COMMISSIONS],
    ),
    body(
        "eg-ax-old-cairo-george-monastery", "alexandria",
        "Patriarchal Monastery of Saint George in Old Cairo",
        "Ιερά Πατριαρχική Μονή Αγίου Γεωργίου Παλαιού Καΐρου",
        "Old Cairo", "Patriarchal Monastery", [AX_COMMISSIONS, AX_GEORGE],
        kind="monastery",
    ),
    body(
        "eg-ax-old-cairo-dormition-monastery-cemetery",
        "eg-ax-old-cairo-george-monastery",
        "Church of the Dormition of the Theotokos in the Cemetery of Saint George Monastery",
        "Ιερός Ναός της Κοιμήσεως της Θεοτόκου",
        "Old Cairo", "Church", [AX_COMMISSIONS, AX_GEORGE],
    ),
    body(
        "eg-ax-new-capital-john-merciful-construction", "alexandria",
        "Church of Saint John the Merciful in the New Administrative Capital",
        "Ιερού Ναού του Αγίου Ιωάννου του Ελεήμονος, Πατριάρχου Αλεξανδρείας",
        "New Administrative Capital", "Church Under Construction",
        [AX_NEW_CAPITAL],
    ),
]

PELUSIUM_ROWS = [
    body(
        "eg-ax-port-said-transfiguration-cathedral", "ax-pelusium",
        "Cathedral of the Transfiguration of the Saviour in Port Said",
        "Ιερό Καθεδρικό Ναό Μεταμορφώσεως του Σωτήρος",
        "Port Said", "Cathedral",
        [AX_PELUSIUM, AX_PORT_SAID, AX_PORT_SAID_CURRENT],
    ),
]

SINAI_ROWS = [
    body(
        "eg-sinai-cairo-dependency", "sinai",
        "Cairo Dependency", "ΜΕΤΟΧΙ ΤΟΥ ΚΑΪΡΟΥ",
        "Cairo", "Dependency", [SINAI_CAIRO_EL, SINAI_CAIRO_EN],
        kind="monastery",
    ),
    body(
        "eg-sinai-cairo-catherine-chapel", "eg-sinai-cairo-dependency",
        "Chapel of Saint Catherine at the Cairo Dependency",
        "Ναὸς τῆς ἁγίας Αἰκατερίνης", "Cairo", "Chapel",
        [SINAI_CAIRO_EL, SINAI_CAIRO_EN],
    ),
    body(
        "eg-sinai-raitho-george-dependency", "sinai",
        "Sinai Dependency of Saint George at Raitho",
        "Τὸ Μετόχι τοῦ ἁγίου Γεωργίου",
        "Raitho", "Dependency", [SINAI_RAITHO_EL, SINAI_RAITHO_EN],
        kind="monastery",
    ),
    body(
        "eg-sinai-pharan-womens-hermitage", "sinai",
        "Women's Hermitage of Pharan",
        "Τὸ γυναικεῖο ἡσυχαστήριο τῆς Φαράν",
        "Pharan", "Hermitage", [SINAI_PHARAN_EL, SINAI_PHARAN_EN],
        kind="monastery",
    ),
    body(
        "eg-sinai-pharan-prophet-moses-church",
        "eg-sinai-pharan-womens-hermitage",
        "Church of the Prophet Moses at the Women's Hermitage of Pharan",
        "Ὁ Ναὸς τοῦ προφήτου Μωυσέως τοῦ Ἡσυχαστηρίου τῆς Φαράν",
        "Pharan", "Church", [SINAI_PHARAN_EL, SINAI_PHARAN_EN],
    ),
    body(
        "eg-sinai-tarfa-hermitage", "sinai",
        "Hermitage of Tarfa", "τὸ ἡσυχαστήριο τῆς Τάρφας",
        "Tarfa", "Hermitage", [SINAI_TARFA_EL, SINAI_TARFA_EN],
        kind="monastery",
    ),
]

RUSSIAN_ROWS = [
    body(
        "eg-ru-cairo-sergius", "ru-north-africa",
        "Parish of Saint Sergius of Radonezh in Cairo",
        "Приход прп. Сергия Радонежского", "Cairo", "Parish",
        [RU_EGYPT, RU_CAIRO, RU_CAIRO_CURRENT],
        address=[
            "г. Каир, район Замалек",
            "ул. Мохаммед Мазхар Паша, д. 35",
        ],
    ),
    body(
        "eg-ru-giza-parish", "ru-north-africa",
        "Parish in Giza", "Приход в Гизе", "Giza", "Parish",
        [RU_EGYPT, RU_GIZA, RU_GIZA_DECR],
    ),
    body(
        "eg-ru-hurghada-myrrhbearers", "ru-north-africa",
        "Parish of the Holy Myrrh-bearing Women in Hurghada",
        "Приход в Хургаде", "Hurghada", "Parish",
        [RU_EGYPT, RU_HURGHADA, RU_HURGHADA_CURRENT],
    ),
    body(
        "eg-ru-madina-seraphim", "ru-north-africa",
        "Parish of Saint Seraphim of Sarov in Madina",
        "Приход прп. Серафима Саровского в пос. Мадина",
        "Madina", "Parish", [RU_EGYPT, RU_MADINA, RU_MADINA_CURRENT],
        address=[
            "19А, Сан Сити (Мадина)",
            "Эль-Дабаа, провинция Матрух, 5004440",
        ],
    ),
    body(
        "eg-ru-el-dabaa-all-egypt-saints", "ru-north-africa",
        "Church of All Saints Who Shone Forth in the Land of Egypt in El Dabaa",
        "Храм Всех святых, в земле Египетской просиявших",
        "El Dabaa", "Church", [RU_EL_DABAA, RU_EL_DABAA_CONSECRATION],
    ),
]

ROWS = {
    "alexandria": AX_ROWS,
    "ax-pelusium": PELUSIUM_ROWS,
    "sinai": SINAI_ROWS,
    "ru-north-africa": RUSSIAN_ROWS,
}
EXPECTED = {
    "alexandria": 30,
    "ax-pelusium": 1,
    "sinai": 6,
    "ru-north-africa": 5,
}
EXPECTED_TOTAL = 42
ALLOWED_KINDS = {"parish", "monastery"}
ALLOWED_RANKS = {
    "Parish", "Church", "Patriarchal Church", "Cathedral", "Chapel",
    "Patriarchal Monastery", "Dependency", "Hermitage",
    "Church Under Construction",
}
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for rows in ROWS.values()
    for item in rows
}
ENGLISH_SEATS = {
    item["seat"]: item["seat"]
    for rows in ROWS.values()
    for item in rows
}


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % item.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    return item


def build():
    payloads = {}
    seen = set(ROWS)
    names = {}
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" % (
                    row_id, item.get("parent"),
                ))
            if item.get("country") != "EG":
                raise ValueError("%s is outside Egypt" % row_id)
            if item.get("kind") not in ALLOWED_KINDS:
                raise ValueError("%s has an unsupported kind" % row_id)
            if item.get("rank") not in ALLOWED_RANKS:
                raise ValueError("%s has an unsupported rank" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a usable local or English name" % row_id)
            name_key = item["name"].casefold()
            if name_key in names:
                raise ValueError("duplicate reader-facing name: %s and %s" % (
                    names[name_key], row_id,
                ))
            if item.get("address") and (
                    not isinstance(item["address"], list) or
                    not all(isinstance(line, str) for line in item["address"])):
                raise ValueError("%s has an invalid address" % row_id)
            rendered = json.dumps(item, ensure_ascii=False)
            if any(mark in rendered for mark in (
                    "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
                    "\u201c", "\u201d")):
                raise ValueError("%s has forbidden punctuation or encoding" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            names[name_key] = row_id
            rows.append(item)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s count changed: %d" % (parent, len(rows)))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "EG",
            "rows": rows,
        }
    row_ids = {
        item["id"] for payload in payloads.values() for item in payload["rows"]
    }
    if set(ENGLISH_NAMES) != row_ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Egypt English name map is out of sync")
    if sum(len(payload["rows"]) for payload in payloads.values()) != EXPECTED_TOTAL:
        raise ValueError("Egypt branch total must remain %d" % EXPECTED_TOTAL)
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "EG":
        raise ValueError("Egypt candidate ledger has the wrong schema or country")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Egypt candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if (summary.get("new_subordinate_bodies") != EXPECTED_TOTAL or
            summary.get("alexandria") != 30 or
            summary.get("ax-pelusium") != 1 or
            summary.get("sinai") != 6 or
            summary.get("ru-north-africa") != 5):
        raise ValueError("Egypt candidate ledger totals are out of sync")
    required_lists = (
        "candidates", "reconciliation", "exclusions",
        "official_jurisdiction_audit",
    )
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Egypt candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "EG":
            raise ValueError("%s is outside Egypt" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Egypt candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Egypt ledger item must cite one to three sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Egypt ledger item carries a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\ufffd", "\u2018", "\u2019",
            "\u201c", "\u201d")):
        raise ValueError("Egypt candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Egypt: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Egypt: 42 current officially named subordinate bodies across "
            "4 existing parent branches"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
