#!/usr/bin/env python3
"""Validate exact current Church of Crete bodies from first-party rosters.

This tranche remains independent of the shared directory aggregator. It emits
later-integration payloads for the Archdiocese of Crete and all eight
metropolises of the Church of Crete. Only exact bodies named by current
competent Church sources are published. Aggregate-only bodies and dissolved
institutions stay in the companion candidate ledger.

    python tools/directory_crete_country.py --check
    python tools/directory_crete_country.py --dump
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "crete_country.json"
)

# The exact ordered source transcription is plain UTF-8 JSON in the
# companion research ledger. The module validates and consumes it directly
# so provenance remains inspectable without decoding an opaque payload.
PARENT_BY_BLOB = {
    "crete": "ep-crete",
    "gortyne": "ep-gortyne",
    "rethymne": "ep-rethymne",
    "kydonia": "ep-kydonia",
    "lampe": "ep-lampe",
    "hierapytne": "ep-hierapytne",
    "petra": "ep-petra",
    "kisamos": "ep-kisamos",
    "arkalochorion": "ep-arkalochorion",
}

EXPECTED_PARENTS = {
    "ep-crete": 167,
    "ep-gortyne": 124,
    "ep-rethymne": 120,
    "ep-kydonia": 129,
    "ep-lampe": 84,
    "ep-hierapytne": 102,
    "ep-petra": 104,
    "ep-kisamos": 83,
    "ep-arkalochorion": 98,
}
EXPECTED_RANKS = {
    "Parish Church": 861,
    "Chapel": 21,
    "Monastery": 72,
    "Hesychasterion": 9,
    "Monastic Dependency": 27,
    "Parish Monastery": 10,
    "Pilgrimage Church": 11,
}
EXPECTED_KINDS = {"parish": 893, "monastery": 118}
EXPECTED_TOTAL = 1011

COMPETENT_HOSTS = {
    "ec-patr.org",
    "www.iak.gr",
    "www.imga.gr",
    "imka.gr",
    "www.imis.gr",
    "www.impeh.gr",
    "imks.gr",
    "www.imakb.gr",
}
BODY_SITE_HOSTS = {
    "enoriaagiougeorgiou.blogspot.com",
    "evaggelistria.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_source_transcription():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    source = ledger.get("source_transcription") or {}
    if source.get("format") != "plain UTF-8 JSON in official roster order":
        raise ValueError("Crete source transcription format drifted")
    by_roster = source.get("by_roster")
    if not isinstance(by_roster, dict) or set(by_roster) != set(PARENT_BY_BLOB):
        raise ValueError("Crete source transcription roster coverage drifted")
    return by_roster


def clean_space(value):
    value = (value or "").replace("\u00ad", "")
    value = value.replace("\u2013", " - ").replace("\u2014", " - ")
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(value.split()).strip(" ,.;")


def folded(value):
    value = clean_space(value)
    return "".join(
        char for char in unicodedata.normalize("NFD", value).upper()
        if unicodedata.category(char) not in {"Mn", "Sk"}
    ).replace("Ϲ", "Σ").replace("ς", "Σ")


GREEK_DIGRAPHS = (
    ("ΟΥ", "ou"), ("ΑΙ", "ai"), ("ΕΙ", "ei"), ("ΟΙ", "oi"),
    ("ΑΥ", "av"), ("ΕΥ", "ev"), ("ΓΓ", "ng"), ("ΓΚ", "gk"),
    ("ΜΠ", "b"), ("ΝΤ", "nt"), ("ΤΣ", "ts"), ("ΤΖ", "tz"),
)
GREEK_LETTERS = {
    "Α": "a", "Β": "v", "Γ": "g", "Δ": "d", "Ε": "e",
    "Ζ": "z", "Η": "i", "Θ": "th", "Ι": "i", "Κ": "k",
    "Λ": "l", "Μ": "m", "Ν": "n", "Ξ": "x", "Ο": "o",
    "Π": "p", "Ρ": "r", "Σ": "s", "Τ": "t", "Υ": "y",
    "Φ": "f", "Χ": "ch", "Ψ": "ps", "Ω": "o",
}


def transliterate(value):
    source = folded(value)
    for greek, latin in GREEK_DIGRAPHS:
        source = source.replace(greek, "{%s}" % latin)
    out = []
    pos = 0
    while pos < len(source):
        if source[pos] == "{" and "}" in source[pos:]:
            end = source.index("}", pos)
            out.append(source[pos + 1:end])
            pos = end + 1
            continue
        out.append(GREEK_LETTERS.get(source[pos], source[pos].lower()))
        pos += 1
    text = clean_space("".join(out))
    words = []
    for word in text.split(" "):
        parts = [part[:1].upper() + part[1:] for part in word.split("-")]
        words.append("-".join(parts))
    return " ".join(words)


def english_seat(value):
    value = clean_space(value or "Κρήτη")
    text = transliterate(value)
    overrides = {
        "Kriti": "Crete",
        "Siteia": "Sitia",
        "Rethymnon": "Rethymno",
        "Chanion": "Chania",
        "Irakleion": "Heraklion",
    }
    return overrides.get(text, text)


TITLE_MARKERS = (
    ("Iera Patriarchiki Kai Stavropigiaki Koinoviaki Moni",
     "Patriarchal and Stavropegic Monastery"),
    ("Iera Patriarchiki Kai Stavropigiaki Moni",
     "Patriarchal and Stavropegic Monastery"),
    ("Patriarchiki Kai Stavropigiaki Moni",
     "Patriarchal and Stavropegic Monastery"),
    ("Stavropigiaki Iera Moni", "Stavropegic Monastery"),
    ("Iera Gynaikeia Koinoviaki Moni", "Cenobitic Convent"),
    ("Iera Koinoviaki Moni", "Cenobitic Monastery"),
    ("Gynaikeion Isychastirion", "Hesychasterion"),
    ("Ieros Mitropolitikos Naos", "Metropolitan Church"),
    ("I. Mitropolitikos N.", "Metropolitan Church"),
    ("I. Mitropolitikos Naos", "Metropolitan Church"),
    ("Ieros Kathedrikos Naos", "Cathedral"),
    ("I. Kathedrikos N.", "Cathedral"),
    ("I. Kathedrikos Naos", "Cathedral"),
    ("Ieros Proskynimatikos Naos", "Pilgrimage Church"),
    ("Iero Proskynima", "Pilgrimage Church"),
    ("Ieres Mones", "Monasteries"),
    ("Iera Moni", "Monastery"),
    ("Ieron Isychastirion", "Hesychasterion"),
    ("Iero Isychastirio", "Hesychasterion"),
    ("Isychastirion", "Hesychasterion"),
    ("Ieros Naos", "Church"),
    ("I. Naos", "Church"),
    ("I. N.", "Church"),
    ("I N.", "Church"),
    ("Enoria", "Parish Church"),
    ("Metochi", "Monastic Dependency"),
)

# The keys are the normalized romanization emitted by transliterate().
# Longest-prefix matching keeps place names separate from the dedication and
# makes every English title reproducible from the first-party Greek roster.
DEDICATIONS = {
    "Yperagias Theotokou \"axion Estin\"":
        "the Most Holy Theotokos, Axion Estin",
    "Anastaseos Tou Kyriou Kai Axion Esti":
        "the Resurrection of the Lord and Axion Estin",
    "Metamorfosis Tou Sotiros Kai Agios Spyridon":
        "the Transfiguration of the Savior and Saint Spyridon",
    "Metamorfos.eos Tou Sotiros": "the Transfiguration of the Savior",
    "Metamorfosis Tou Kyriou": "the Transfiguration of the Lord",
    "Ypsoseos Timiou Stavrou": "the Exaltation of the Precious Cross",
    "Theias Metamorfoseos": "the Holy Transfiguration",
    "Ypapantis Tou Sotiros": "the Meeting of the Lord",
    "Ypapantis Tou Kyriou": "the Meeting of the Lord",
    "Tou Sotiros Christou": "Christ the Savior",
    "Agiou Panteleimonos Kainas-Agion Panton":
        "Saint Panteleimon and All Saints",
    "Agiou Rafail Kai Ton Syn Avtoi":
        "Saint Raphael and his companions",
    "Panagias Akrotirianis Kai Ioannou Tou Theologou":
        "Panagia Akrotiriani and Saint John the Theologian",
    "Ton Taxiarchon Michail Kai Gavriil":
        "the Archangels Michael and Gabriel",
    "Ton Agion Antoniou Kai Varvaras":
        "Saints Anthony and Barbara",
    "Isapostolon Konstantinou Kai Elenis":
        "Saints Constantine and Helen, Equals-to-the-Apostles",
    "Agion Apostolon Petrou Kai Pavlou":
        "the Holy Apostles Peter and Paul",
    "Agion Petrou Kai Pavlou":
        "Saints Peter and Paul",
    "Agion Konstantinou Kai Elenis":
        "Saints Constantine and Helen",
    "Agiou Konstantinou Kai Elenis":
        "Saints Constantine and Helen",
    "Agion Athanasiou Kai Kyrillou":
        "Saints Athanasius and Cyril",
    "Agiou Athanasiou Kai Kyrillou":
        "Saints Athanasius and Cyril",
    "Agion Kirykou Kai Ioulittis":
        "Saints Cyricus and Julitta",
    "Ag. Kon/nos & Eleni":
        "Saints Constantine and Helen",
    "Apostolos Pavlos Kai Agios Georgios":
        "the Apostle Paul and Saint George",
    "Evangelismou Tis Theotokou":
        "the Annunciation of the Theotokos",
    "Evangelismou Tais Theotokou":
        "the Annunciation of the Theotokos",
    "Evangelismou Theotokou":
        "the Annunciation of the Theotokos",
    "Evang. Theotokou": "the Annunciation of the Theotokos",
    "Evag. Theotokou": "the Annunciation of the Theotokos",
    "Koimiseos Tis Theotokou": "the Dormition of the Theotokos",
    "Koimiseos Theotokou": "the Dormition of the Theotokos",
    "Koimisis Tis Theotokou": "the Dormition of the Theotokos",
    "Koimisis Theotokou": "the Dormition of the Theotokos",
    "Koim. Theotokou": "the Dormition of the Theotokos",
    "Eisodion Tis Theotokou": "the Presentation of the Theotokos",
    "Eisodion Theotokou": "the Presentation of the Theotokos",
    "Eisodia Tis Theotokou": "the Presentation of the Theotokos",
    "Eisodia Theotokou": "the Presentation of the Theotokos",
    "Eis. Theotokou": "the Presentation of the Theotokos",
    "Genesiou Tis Theotokou": "the Nativity of the Theotokos",
    "Genesiou Theotokou": "the Nativity of the Theotokos",
    "Genesion Tis Theotokou": "the Nativity of the Theotokos",
    "Genesion Theotokou": "the Nativity of the Theotokos",
    "Genethliou Tis Theotokou": "the Nativity of the Theotokos",
    "Genethliou Theotokou": "the Nativity of the Theotokos",
    "Gen. Theotokou": "the Nativity of the Theotokos",
    "Genesio Theotokou": "the Nativity of the Theotokos",
    "Metamorfoseos Tou Sotiros": "the Transfiguration of the Savior",
    "Metamorfoseos Sotiros": "the Transfiguration of the Savior",
    "Metamorfosis Tou Sotiros": "the Transfiguration of the Savior",
    "Metamorfosis Sotiros": "the Transfiguration of the Savior",
    "Metam. Sotiros": "the Transfiguration of the Savior",
    "Met. Sotiros": "the Transfiguration of the Savior",
    "Metamorfoseos": "the Transfiguration of the Lord",
    "Analipseos Tou Sotiros": "the Ascension of the Lord",
    "Analipsis Tou Sotiros": "the Ascension of the Lord",
    "Analipsis Kyriou": "the Ascension of the Lord",
    "Analipsis Sotiros": "the Ascension of the Lord",
    "Anal. Sotiros": "the Ascension of the Lord",
    "Analipseos": "the Ascension of the Lord",
    "Anastasis Kyriou": "the Resurrection of the Lord",
    "Anastaseos Tou Kyriou": "the Resurrection of the Lord",
    "Yp. Sotiros": "the Meeting of the Lord",
    "Zoodochou Pigis": "the Life-giving Spring",
    "Tis Tou Theou Sofias": "the Holy Wisdom of God",
    "Agias Triados": "the Holy Trinity",
    "Agia Triada": "the Holy Trinity",
    "Agia Trias": "the Holy Trinity",
    "Ag. Triados": "the Holy Trinity",
    "Ag. Trias": "the Holy Trinity",
    "Timiou Stavrou": "the Precious Cross",
    "Tim. Stavrou": "the Precious Cross",
    "Timiou Prodromou": "Saint John the Forerunner",
    "Tim. Prodromou": "Saint John the Forerunner",
    "Agias Zonis": "the Holy Belt of the Theotokos",
    "Agia Skepi": "the Protection of the Theotokos",
    "Agiou Pnevmatos": "the Holy Spirit",
    "Ag. Pnevmatos": "the Holy Spirit",
    "Agion Apostolon": "the Holy Apostles",
    "Agioi Apostoloi": "the Holy Apostles",
    "Ag. Apostolon": "the Holy Apostles",
    "Ag. Apostoloi": "the Holy Apostles",
    "Agion Anargyron": "the Holy Unmercenaries",
    "Agioi Anargyroi": "the Holy Unmercenaries",
    "Agion Panton": "All Saints",
    "Agioi Pantes": "All Saints",
    "Ag. Panton": "All Saints",
    "Ag. Pantes": "All Saints",
    "Agion Tessarakonta Martyron": "the Forty Martyrs",
    "Agion Tessarakonta": "the Forty Martyrs",
    "Agion Tessaron Martyron": "the Four Martyrs",
    "Agion 4 Martyron": "the Four Martyrs",
    "Agion Deka Martyron": "the Ten Martyrs of Crete",
    "Ag. Deka": "the Ten Martyrs of Crete",
    "Agion Theodoron": "Saints Theodore",
    "Agioi Theodoroi": "Saints Theodore",
    "Ag. Pateres": "the Holy Fathers",
    "Archistratigon": "the Archangels",
    "Taxiarchon": "the Archangels",
    "Michail Archangelou": "the Archangel Michael",
    "Archangelou Michail": "the Archangel Michael",
    "Michail Archangelos": "the Archangel Michael",
    "Profitou Iliou": "the Prophet Elias",
    "Prof. Iliou": "the Prophet Elias",
    "Apostolou Pavlou": "the Apostle Paul",
    "Apostolou Thoma": "the Apostle Thomas",
    "Arch. Michail": "the Archangel Michael",
    "Apostolos Pavlos": "the Apostle Paul",
    "Apostolos Titos": "the Apostle Titus",
    "Evangelistis Loukas": "the Evangelist Luke",
    "Osiou Theodosiou Tou Koinoviarchou":
        "Venerable Theodosius the Cenobiarch",
    "Osias Eirinis Tis Chrysovalantou":
        "Venerable Irene of Chrysovalantou",
    "Osia Eirini Chrysovalantou":
        "Venerable Irene of Chrysovalantou",
    "Osias Pelagias": "Venerable Pelagia",
    "Odigitria": "Panagia Hodegetria",
    "Kyrias Ton Angelon": "Our Lady of the Angels",
    "Kera Eleousa": "Panagia Eleousa",
    "Genesiou Tou Prodromou": "the Nativity of Saint John the Forerunner",
    "Agia Moni": "Agia Moni",
    "Agioi Evtychianoi": "Saints Eutychianoi",
    "Evangelistrias": "Panagia Evangelistria",
    "Theologou": "Saint John the Theologian",
    "Asomaton": "the Holy Bodiless Powers",
    "Theogennitoros": "the Theotokos",
    "Keras Kardiotissas": "Panagia Kera Kardiotissa",
    "Synaxeos Ton Archangelon": "the Synaxis of the Archangels",
    "Treis Ierarchai": "the Three Holy Hierarchs",
    "Timios Prodromos": "Saint John the Forerunner",
    "Timios Stavros": "the Precious Cross",
    "Zoodochos Pigi": "the Life-giving Spring",
    "Profitis Ilias": "the Prophet Elias",
    "Myrtidiotissa": "Panagia Myrtidiotissa",
    "Ag. Kon/nou": "Saint Constantine",
    "Ai Kyr Giannis": "Saint John",
}

PANAGIA_FORMS = {
    "Akrotirianis": "Akrotiriani",
    "Charakianis": "Charakiani",
    "Chrysoskalitissis": "Chrysoskalitissa",
    "Eleousis": "Eleousa",
    "Elevtherotrias": "Eleftherotria",
    "Exakoustis": "Exakousti",
    "Faneromenis": "Faneromeni",
    "Kardiotissas": "Kardiotissa",
    "Keras": "Kera",
    "Odigitrias": "Hodegetria",
    "Thymianis": "Thymiani",
    "Vryomenou": "Vryomeni",
}

SAINT_FORMS = {
    "Andreou Ierosolymitou, Archiepiskopou Kritis":
        "Andrew of Jerusalem, Archbishop of Crete",
    "Ioannou Tou Prodromou": "John the Forerunner",
    "Ioannou Tou Eleimonos": "John the Merciful",
    "Ioannou Tou Theologou": "John the Theologian",
    "Ioannou Theologou": "John the Theologian",
    "Ioannis O Theologos": "John the Theologian",
    "Ioannis Theologos": "John the Theologian",
    "Ioannis O Rigologos": "John Rigologos",
    "Ioan. Theologos": "John the Theologian",
    "Io. Chrysost": "John Chrysostom",
    "Ioannou Chrysostomou": "John Chrysostom",
    "Ioannou Prodromou": "John the Forerunner",
    "Konstantinou": "Constantine",
    "Georgiou": "George",
    "Georgios": "George",
    "Nikolaou": "Nicholas",
    "Nikolaos": "Nicholas",
    "Ioannou": "John",
    "Ioannis": "John",
    "Dimitriou": "Demetrius",
    "Dimitrios": "Demetrius",
    "Panteleimonos": "Panteleimon",
    "Panteleimon": "Panteleimon",
    "Antoniou": "Anthony",
    "Antonios": "Anthony",
    "Charalabous": "Charalambos",
    "Charalabos": "Charalambos",
    "Paraskevis": "Paraskevi",
    "Paraskevi": "Paraskevi",
    "Paraskies": "Paraskevi",
    "Marinis": "Marina",
    "Marinas": "Marina",
    "Marina": "Marina",
    "Annis": "Anna",
    "Anna": "Anna",
    "Aikaterinis": "Catherine",
    "Aikaterini": "Catherine",
    "Varvaras": "Barbara",
    "Varvara": "Barbara",
    "Elevtheriou": "Eleftherius",
    "Elevtherios": "Eleftherius",
    "Stylianou": "Stylianos",
    "Stefanou": "Stephen",
    "Stefanos": "Stephen",
    "Fanouriou": "Phanourios",
    "Fanourios": "Phanourios",
    "Mina": "Minas",
    "Kyrillou": "Cyril",
    "Kyrillos": "Cyril",
    "Vasileiou": "Basil",
    "Vasileios": "Basil",
    "Nektariou": "Nectarius",
    "Nektarios": "Nectarius",
    "Spyridonos": "Spyridon",
    "Spyridon": "Spyridon",
    "Rafail": "Raphael",
    "Titou": "Titus",
    "Titos": "Titus",
    "Dionysiou": "Dionysius",
    "Christoforou": "Christopher",
    "Christoforos": "Christopher",
    "Mamantos": "Mamas",
    "Mamas": "Mamas",
    "Mama": "Mamas",
    "Andreou": "Andrew",
    "Andreas": "Andrew",
    "Andrea": "Andrew",
    "Anastasias": "Anastasia",
    "Eirinis": "Irene",
    "Eirini": "Irene",
    "Thomas": "Thomas",
    "Thoma": "Thomas",
    "Athanasiou": "Athanasius",
    "Pelagias": "Pelagia",
    "Pelagia": "Pelagia",
    "Sofias": "Sophia",
    "Sofia": "Sophia",
    "Foteinis": "Photini",
    "Foteini": "Photini",
    "Fotia": "Photini",
    "Amvrosiou": "Ambrose",
    "Pavlou": "Paul",
    "Pavlos": "Paul",
    "Louka": "Luke",
    "Gerasimou": "Gerasimus",
    "Magdalinis": "Mary Magdalene",
    "Kyriakis": "Kyriake",
    "Kyriaki": "Kyriake",
    "Tryfonos": "Tryphon",
    "Evstathiou": "Eustathius",
    "Nikita": "Niketas",
    "Nikitas": "Niketas",
    "Myronos": "Myron",
    "Myron": "Myron",
    "Vlasiou": "Blaise",
    "Vlasios": "Blaise",
    "Sila": "Silas",
    "Silas": "Silas",
    "Evmeniou": "Eumenius",
    "Evgeniou": "Eugene",
    "Kyprianou": "Cyprian",
    "Theodoroi": "Theodore",
    "Theodoron": "Theodore",
    "Alexandros": "Alexander",
    "Petros": "Peter",
    "Nikita": "Niketas",
    "Nikitou": "Niketas",
    "Makrinas": "Macrina",
}

HONORIFICS = {
    "Agiou": "Saint",
    "Agias": "Saint",
    "Agios": "Saint",
    "Agia": "Saint",
    "Ag.": "Saint",
    "Osiou": "Venerable",
    "Osias": "Venerable",
    "Osia": "Venerable",
}

LOCATION_REPLACEMENTS = (
    ("Enorias Agiou Georgiou Porou Irakleiou",
     "the Parish of Saint George in Poros, Heraklion"),
    ("Enorias Zoodochou Pigis Chrysopigis",
     "the Parish of the Life-giving Spring in Chrysopigi"),
    ("Tis Ieras Monis Agkarathou", "the Monastery of Agarathos"),
    ("Agiou Stefanou Xiropotamou", "Agios Stefanos, Xiropotamos"),
    ("Agias Marinas Kydonias", "Agia Marina, Kydonia"),
    ("Psathis Agiou Ioannou Ierapetras",
     "Psathi, Agios Ioannis, Ierapetra"),
    ("Loulou, Panagias, Aletrouvariou Kydonias",
     "Loulos, Panagia, Aletrouvari, Kydonia"),
    ("Exopoleos K' Kalamitsi Amygdalou Apokoronou",
     "Exopoli and Kalamitsi Amygdali, Apokoronas"),
    ("A G. Ioannis", "Agios Ioannis"),
    ("Kok. Pyrgos", "Kokkinos Pyrgos"),
    ("Ag. Deka", "Agioi Deka"),
    ("Ag. Kyrillos", "Agios Kyrillos"),
    ("Vas. Anogeia", "Vasilika Anogeia"),
    ("Ag. Varvara", "Agia Varvara"),
    ("Ag. Thomas", "Agios Thomas"),
    ("Meg. Vrysi", "Megali Vrysi"),
    ("Frantz. Metochia", "Frantzeskiana Metochia"),
    ("N. Choras Chanion", "Nea Chora, Chania"),
    ("Kok. Metochiou Chanion", "Kokkino Metochi, Chania"),
    ("Ag. Pantes", "Agioi Pantes"),
    ("K. Palaiokastro", "Kato Palaiokastro"),
    ("P. Roumata", "Palaia Roumata"),
    ("Ag. Paraskies", "Agies Paraskies"),
    ("Ag. Paraskevi", "Agia Paraskevi"),
    ("S.e.a.p", "S.E.A.P."),
    ("11is M.k.v", "11th M.K.B."),
    ("51 M.e", "51st M.E."),
    ("Arkadiou", "Arkadi"),
    ("Arsaniou", "Arsani"),
    ("Atalis Bali", "Atali, Bali"),
    ("Diskouriou", "Diskouri"),
    ("Roustikon", "Roustika"),
    ("Vrontision", "Vrontisi"),
    ("Vosakou", "Vosakos"),
    ("Zarou", "Zaros"),
    ("Anopoleos", "Anopolis"),
    ("Apteron", "Aptera"),
    ("Archiepiskopikou Oikimatos", "the archiepiscopal residence"),
    ("Mitropolitikou Naou Agiou Mina Irakleiou",
     "the Metropolitan Church of Saint Minas in Heraklion"),
    ("Panepistimiakou Genikou Nosokomeiou",
     "the University General Hospital"),
    ("Pagkritiou Venizeleiou Nosokomeiou",
     "Pankritio Venizeleio Hospital"),
    ("Neou Koimitiriou Irakleiou", "the New Cemetery in Heraklion"),
    ("Monados Frontidos Ilikiomenon", "the elder-care unit"),
    ("Oikismou Aeroporias Gournon", "the Air Force settlement at Gournes"),
    ("Fylakon Neas Alikarnassou", "Nea Alikarnassos Prison"),
    ("Nisou Ntias", "Dia Island"),
    ("Irakleiou", "Heraklion"),
    ("Chanion", "Chania"),
    ("Rethymnis", "Rethymno"),
    ("Rethymnou", "Rethymno"),
    ("Ierapetras", "Ierapetra"),
    ("Siteias", "Sitia"),
    ("Apokoronou", "Apokoronas"),
    ("Kydonias", "Kydonia"),
)

RESIDUAL_DEDICATION_RE = re.compile(
    r"\b(?:Agiou|Agias|Agion|Agios|Agia|Agioi|Ag\.|Osiou|Osias|Osia|"
    r"Theotokou|Sotiros|Taxiarchon|Archistratigon|Profitou|Pnevmatos|"
    r"Koim(?:iseos|isis)?|Eisodion|Eisodia|Evangelismou|Evang\.|Evag\.|"
    r"Genesiou|Genesion|Genethliou|Metamorfoseos|Metamorfosis|Metam\.|"
    r"Timiou|Zoodochou|Apostolou|Apostolos|Evangelistis)\b"
)
RESIDUAL_ENGLISH_TOKEN_RE = re.compile(
    r"\b(?:Ieros|Iera|Iero|Naos|Naou|Moni|Monis|Patriarchiki|"
    r"Stavropigiaki|Proskynima|Enoria|Enorias|Presv|Exypiretei|"
    r"Archim|Ierom|Episkopou|Archiepiskopou|Martyros|Martyron|"
    r"Neomartyros|Megalomartyros|Ieromartyros|Osiomartyros|"
    r"Thaumatourgou|Theologou|Evangelistou|Prodromou|Vaptistou|"
    r"Archangelou|Stylitou|Koinoviarchou|Myrovlitou|Isapostolou|"
    r"Isapostolon|Theoforou|Omologitou|Vasileos|Vasileon|"
    r"Apostolou|Apostolon|Diakonou|Presvyterou|Patriarchou|"
    r"Pateron|Ierarchon|Ierosolymitou)\b",
    re.IGNORECASE,
)
RESIDUAL_ENGLISH_EXCEPTIONS = {
    "gr-ep-crete-097-moni-ieros-naos-agias-paraskevis": {"Moni"},
}
PARENTHETICAL_NAME_EXCEPTIONS = {
    "gr-ep-gortyne-122-treis-ierarchai-lousoudiou-iosif-filagri",
}

EXACT_ENGLISH_NAMES = {
    "Ieros Naos Agiou Kyrillou Episkopou Gortynis - Filotheis "
    "Irakleiou":
        "Church of Saint Cyril, Bishop of Gortyna, in Filothei, "
        "Heraklion",
    "Agia Moni Sarakina Mournion":
        "Monastic Dependency of the Holy Monastery of Sarakina in Mournies",
    "Agia Moni Viannou": "Holy Monastery of Viannos",
    "Agia Moni Agiou Antoniou Arvis":
        "Monastery of Saint Anthony in Arvi",
    "Ieros Naos Agiou Dimitriou (limenos)":
        "Church of Saint Demetrius at the Harbor",
    "Ieros Naos Agiou Ioannou (chostos)":
        "Church of Saint John in Chostos",
    "Ieros Naos Eisodion Tis Theotokou (mitropolitikos)":
        "Metropolitan Church of the Presentation of the Theotokos",
    "Ieros Naos Agiou Konstantinou Kai Elenis (nea Chora) Chanion":
        "Church of Saints Constantine and Helen in Nea Chora, Chania",
    "Ieros Naos Agiou Nektariou Chanion (pachiana)":
        "Church of Saint Nectarius in Pachiana, Chania",
    "Ieros Naos Agiou Nikolaou Chanion (splantzia)":
        "Church of Saint Nicholas in Splantzia, Chania",
    "Ieros Naos Agiou Panteleimonos Kainas-Agion Panton Apokoronou "
    "Kai Ieros Naos Agiou Fanouriou (ethnikis Odou)":
        "Parish Churches of Saint Panteleimon in Kaina, All Saints in "
        "Apokoronas, and Saint Phanourios on the National Road",
    "Iero Proskynima Agiou Rafail Tis Ieras Mitropoleos Kydonias Kai "
    "Apokoronou, 18o Chiliometro Chanion Rethymnou":
        "Pilgrimage Church of Saint Raphael at the 18th km of the "
        "Chania-Rethymno Road",
    "Gavdos (nisos) - Ag. Trias":
        "Church of the Holy Trinity on Gavdos",
    "Odigitria Patriarchiki Kai Stavropigiaki":
        "Patriarchal and Stavropegic Monastery of Panagia Hodegetria",
    "Ieros Proskynimatikos Naos Agion Anargyron Nosokomeiou Agiou "
    "Nikolaou":
        "Pilgrimage Church of the Holy Unmercenaries at Agios Nikolaos "
        "Hospital",
    "Ieros Proskynimatikos Naos Agiou Panteleimonos Nisou Spinalogkas":
        "Pilgrimage Church of Saint Panteleimon on Spinalonga",
    "Iera Moni Genethliou Tis Theotokou Tis Vigliotissas":
        "Monastery of the Nativity of the Theotokos at Vigliotissa",
    "Treis Ierarchai Lousoudiou Iosif Filagri":
        "Monastic Dependency of the Three Holy Hierarchs at Lousoudi "
        "(Joseph Philagris)",
    "Kardiotissa": "Kardiotissa Monastic Dependency",
    "Arkalochori - I. Mitropolitikos Naos Agiou Andreou Ierosolymitou, "
    "Archiepiskopou Kritis":
        "Metropolitan Church of Saint Andrew of Jerusalem, Archbishop "
        "of Crete, in Arkalochori",
    "Ano Viannos - Michail Archangelou - Michail Archangelou":
        "Church of the Archangel Michael in Ano Viannos",
    "Ieros Naos Evangelismou Tis Theotokou Panagias Stavroforon":
        "Church of the Annunciation of the Theotokos, Panagia Stavroforon",
    "Ieros Naos Koimiseos Tis Theotokou Panagias Kamarianis":
        "Church of the Dormition of the Theotokos, Panagia Kamariani",
}


def split_prefix(value, prefix):
    if value == prefix:
        return ""
    if value.startswith(prefix):
        boundary = value[len(prefix):len(prefix) + 1]
        if boundary in {" ", "-", ",", ".", "("}:
            return value[len(prefix):].strip(" -,.")
    return None


def dedication_prefix(value):
    value = clean_space(value).replace("«", '"').replace("»", '"')
    for source in sorted(DEDICATIONS, key=len, reverse=True):
        remainder = split_prefix(value, source)
        if remainder is not None:
            return DEDICATIONS[source], remainder
    for honorific in sorted(HONORIFICS, key=len, reverse=True):
        remainder = split_prefix(value, honorific)
        if remainder is None:
            continue
        for source in sorted(SAINT_FORMS, key=len, reverse=True):
            tail = split_prefix(remainder, source)
            if tail is not None:
                return "%s %s" % (
                    HONORIFICS[honorific], SAINT_FORMS[source]
                ), tail
    if value.startswith("Panagia "):
        words = value.split(" ")
        epithet = PANAGIA_FORMS.get(words[1], words[1])
        return "Panagia %s" % epithet, " ".join(words[2:])
    if value == "Panagias":
        return "the Theotokos", ""
    if value.startswith("Panagias "):
        words = value.split(" ")
        epithet = PANAGIA_FORMS.get(words[1], words[1])
        return "Panagia %s" % epithet, " ".join(words[2:])
    return "", value


def find_dedication(value, prefer_after_separator=False):
    candidates = []
    for pos in range(len(value)):
        if pos and value[pos - 1] not in " -,.":
            continue
        dedication, remainder = dedication_prefix(value[pos:])
        if not dedication:
            continue
        consumed = len(value[pos:]) - len(remainder)
        separator = bool(re.search(r"-\s*$", value[:pos]))
        candidates.append((separator, consumed, pos, dedication, remainder))
    if not candidates:
        return "", value, ""
    separated = [item for item in candidates if item[0]]
    if prefer_after_separator and separated:
        separator, consumed, pos, dedication, remainder = max(
            separated, key=lambda item: (item[2], item[1])
        )
    else:
        separator, consumed, pos, dedication, remainder = min(
            candidates, key=lambda item: (item[2], -item[1])
        )
    before = value[:pos].strip(" -,.")
    return dedication, remainder, before


def title_allowed(title, rank):
    if title in {
        "Church", "Metropolitan Church", "Cathedral", "Parish Church",
    }:
        return rank == "Parish Church"
    if title == "Pilgrimage Church":
        return rank in {"Parish Church", "Pilgrimage Church"}
    if title in {
        "Monastery", "Monasteries", "Cenobitic Monastery",
        "Cenobitic Convent", "Stavropegic Monastery",
        "Patriarchal and Stavropegic Monastery",
    }:
        return rank in {"Monastery", "Parish Monastery"}
    if title == "Hesychasterion":
        return rank == "Hesychasterion"
    if title == "Monastic Dependency":
        return rank == "Monastic Dependency"
    return False


def title_position(value, source):
    for match in re.finditer(re.escape(source), value):
        start, end = match.span()
        if start and value[start - 1].isalnum():
            continue
        if end < len(value) and value[end].isalnum():
            continue
        return start
    return -1


def english_location(value):
    value = clean_space(value).replace("«", '"').replace("»", '"')
    value = re.sub(r"\s*-\s*", ", ", value).strip(" ,")
    for source, target in LOCATION_REPLACEMENTS:
        value = value.replace(source, target)
    return clean_space(value)


def english_name(local, rank):
    text = transliterate(local).replace("«", '"').replace("»", '"')
    if text in EXACT_ENGLISH_NAMES:
        return EXACT_ENGLISH_NAMES[text]
    markers = []
    for source, target in TITLE_MARKERS:
        if not title_allowed(target, rank):
            continue
        start = title_position(text, source)
        if start >= 0:
            markers.append((start, source, target))
    if markers:
        start, source, title = sorted(markers)[0]
        before = text[:start].strip(" -,.")
        after = text[start + len(source):].strip(" -,.")
    else:
        before = ""
        after = text
        title = {
            "Parish Church": "Church",
            "Chapel": "Chapel",
            "Monastery": "Monastery",
            "Hesychasterion": "Hesychasterion",
            "Monastic Dependency": "Monastic Dependency",
            "Parish Monastery": "Parish Monastery",
            "Pilgrimage Church": "Pilgrimage Church",
        }[rank]
    dedication, after, inner_before = find_dedication(
        after, prefer_after_separator=not markers
    )
    if inner_before:
        before = " ".join(value for value in (before, inner_before) if value)
    if not dedication:
        subject = english_location(after)
        result = clean_space("%s of %s" % (title, subject))
        if before:
            result += " in " + english_location(before)
        return clean_space(result)
    locations = [english_location(value) for value in (before, after)
                 if english_location(value)]
    result = "%s of %s" % (title, dedication)
    if locations:
        result += " in " + ", ".join(locations)
    return clean_space(result)


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if ord(char) < 128)
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:64].rstrip("-") or "body"


def validate_url(value, label, body_site=False):
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    allowed = BODY_SITE_HOSTS if body_site else COMPETENT_HOSTS
    if parsed.netloc not in allowed:
        raise ValueError("%s carries an unapproved host: %s" % (label, value))


LOCAL_SOURCE_FIXES = {
    "Β ῶροι - Ἱ. Ν. Εἰσ. Θεοτόκου. Μιχαήλ Τζαγκαράκης":
        "Βῶροι - Ἱ. Ν. Εἰσ. Θεοτόκου",
    "Ἱερός Ναός Ἁγίας Τριάδος Τσιβαρᾶ Ἀποκορώνου, : Τήν Ἐνορία "
    "ἐξυπηρετεῖ ὁ Πρεσβ. Νεραντζάκης Δημήτριος (ΔΕ)":
        "Ἱερός Ναός Ἁγίας Τριάδος Τσιβαρᾶ Ἀποκορώνου",
    "Καλό Χωριό Μεραμβέλλου - Ενορία Αγίου Χαραλάμπους. T.K.721 00":
        "Καλό Χωριό Μεραμβέλλου - Ενορία Αγίου Χαραλάμπους",
}


def source_rows():
    rows = []
    parent_ordinals = Counter()
    source = load_source_transcription()
    for blob_name in PARENT_BY_BLOB:
        expected_parent = PARENT_BY_BLOB[blob_name]
        for raw in source[blob_name]:
            parent = raw["p"]
            rank = raw["r"]
            local = clean_space(raw["l"])
            if parent != expected_parent:
                raise ValueError("%s blob carries parent %s" %
                                 (blob_name, parent))
            parent_ordinals[parent] += 1
            ordinal = parent_ordinals[parent]
            seat_source = raw.get("t")
            if parent == "ep-petra" and ordinal in {1, 2}:
                seat_source = "Νεάπολις"
            elif parent == "ep-petra" and 23 <= ordinal <= 28:
                seat_source = "Ἅγιος Νικόλαος"
            row_id = "gr-%s-%03d-%s" % (
                parent,
                ordinal,
                slug(transliterate(local)),
            )
            sources = [clean_space(value) for value in raw["u"]]
            site = clean_space(raw.get("w"))
            if site and site not in sources:
                sources.append(site)
            source_only = [value for value in sources if value != site]
            item = {
                "id": row_id,
                "parent": parent,
                "kind": (
                    "monastery"
                    if rank in {
                        "Monastery", "Hesychasterion",
                        "Monastic Dependency", "Parish Monastery",
                    }
                    else "parish"
                ),
                "rank": rank,
                "name": english_name(local, rank),
                "local": local,
                "seat": english_seat(seat_source or "Κρήτη"),
                "country": "GR",
                "sources": sources,
                "cite": list(sources),
                "checked": CHECKED,
            }
            phones = [clean_space(value) for value in raw.get("ph") or []]
            emails = [clean_space(value).lower()
                      for value in raw.get("em") or []]
            if phones:
                item["phones"] = phones
            if emails:
                item["emails"] = emails
            if phones or emails:
                item["contact_sources"] = source_only
                item["contact_checked"] = CHECKED
            if site:
                item["site"] = site
            rows.append(item)
    return rows


ROWS = source_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            for text in walk_strings(item):
                yield text
    elif isinstance(value, dict):
        for item in value.values():
            for text in walk_strings(item):
                yield text


def contact_summary(rows):
    return {
        "contact_bodies": sum(bool(
            row.get("phones") or row.get("emails") or row.get("site")
        ) for row in rows),
        "phone_bodies": sum(bool(row.get("phones")) for row in rows),
        "public_phone_values": sum(
            len(row.get("phones") or []) for row in rows
        ),
        "email_bodies": sum(bool(row.get("emails")) for row in rows),
        "public_email_values": sum(
            len(row.get("emails") or []) for row in rows
        ),
        "body_owned_sites": sum(bool(row.get("site")) for row in rows),
    }


def published_summary(rows):
    parents = Counter(row["parent"] for row in rows)
    ranks = Counter(row["rank"] for row in rows)
    summary = {
        "total": len(rows),
        "parents": dict(sorted(parents.items())),
        "ranks": dict(sorted(ranks.items())),
    }
    summary.update(contact_summary(rows))
    return summary


def validate_ledger(rows):
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Crete candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Crete candidate ledger check date drifted")
    if ledger.get("published_summary") != published_summary(rows):
        raise ValueError("Crete candidate ledger summary drifted")
    for key in ("source_boundaries", "completeness", "held_limitations"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Crete candidate ledger lacks %s" % key)
        for entry in entries:
            for source_url in entry.get("sources") or []:
                validate_url(source_url, key)
    source = ledger.get("source_transcription") or {}
    if source.get("format") != "plain UTF-8 JSON in official roster order":
        raise ValueError("Crete ledger source format drifted")
    if set(source.get("keys") or {}) != {
        "p", "r", "l", "t", "u", "ph", "em", "w",
    }:
        raise ValueError("Crete ledger source key legend drifted")
    by_roster = source.get("by_roster") or {}
    if set(by_roster) != set(PARENT_BY_BLOB):
        raise ValueError("Crete ledger source roster coverage drifted")
    for roster, source_entries in by_roster.items():
        parent = PARENT_BY_BLOB[roster]
        if len(source_entries) != EXPECTED_PARENTS[parent]:
            raise ValueError("%s source transcription count drifted" % roster)
        for source_entry in source_entries:
            if source_entry.get("p") != parent:
                raise ValueError("%s source transcription parent drifted" % roster)
            if not all(source_entry.get(key) for key in ("r", "l", "u")):
                raise ValueError("%s source transcription is incomplete" % roster)
            for source_url in source_entry["u"]:
                validate_url(source_url, roster)
    boundaries = ledger.get("transcription_boundaries") or []
    boundary_map = {
        item.get("original"): item.get("published_local")
        for item in boundaries
    }
    if boundary_map != LOCAL_SOURCE_FIXES or any(
            not item.get("reason") for item in boundaries):
        raise ValueError("Crete transcription boundary record drifted")
    documented_exceptions = {
        item.get("id"): {item.get("term")}
        for item in ledger.get("english_name_exceptions") or []
        if item.get("reason")
    }
    if documented_exceptions != RESIDUAL_ENGLISH_EXCEPTIONS:
        raise ValueError("Crete English-name exception record drifted")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Crete candidate ledger has forbidden punctuation")
    return ledger


def build():
    ids = set()
    parent_counts = Counter()
    rank_counts = Counter()
    kind_counts = Counter()
    signatures = {}
    for item in ROWS:
        row_id = item["id"]
        if row_id in ids:
            raise ValueError("duplicate id: %s" % row_id)
        ids.add(row_id)
        parent_counts[item["parent"]] += 1
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        if item.get("country") != "GR":
            raise ValueError("%s carries the wrong country" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks a name, local name, or seat" % row_id)
        dedication_segment = re.split(
            r"\s+(?:in|at|on)\s+", item["name"], maxsplit=1
        )[0]
        if RESIDUAL_DEDICATION_RE.search(dedication_segment):
            raise ValueError(
                "%s carries an untranslated English dedication: %s" %
                (row_id, item["name"])
            )
        residual_tokens = {
            match.group(0)
            for match in RESIDUAL_ENGLISH_TOKEN_RE.finditer(item["name"])
        }
        allowed_tokens = RESIDUAL_ENGLISH_EXCEPTIONS.get(row_id, set())
        if {value.casefold() for value in residual_tokens} - {
                value.casefold() for value in allowed_tokens}:
            raise ValueError(
                "%s carries residual roster language: %s" %
                (row_id, item["name"])
            )
        if (("(" in item["name"] or ")" in item["name"]) and
                row_id not in PARENTHETICAL_NAME_EXCEPTIONS):
            raise ValueError(
                "%s carries an unreviewed parenthetical name: %s" %
                (row_id, item["name"])
            )
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for source_url in item.get("sources") or []:
            validate_url(
                source_url,
                row_id,
                body_site=source_url == item.get("site"),
            )
        if item.get("site") and item["site"] not in item["sources"]:
            raise ValueError("%s body-owned site lacks provenance" % row_id)
        if item.get("phones") or item.get("emails"):
            if item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks a current contact check" % row_id)
            if not item.get("contact_sources"):
                raise ValueError("%s lacks contact provenance" % row_id)
            for source_url in item["contact_sources"]:
                validate_url(source_url, row_id)
                if source_url not in item["sources"]:
                    raise ValueError(
                        "%s contact source is outside identity sources" %
                        row_id
                    )
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 10 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.match(email):
                raise ValueError("%s carries an invalid email" % row_id)
        signature = (
            item["parent"], folded(item["local"]), folded(item["seat"])
        )
        if signature in signatures:
            raise ValueError("%s duplicates %s" %
                             (row_id, signatures[signature]))
        signatures[signature] = row_id
    if len(ROWS) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(ROWS)))
    if dict(sorted(parent_counts.items())) != EXPECTED_PARENTS:
        raise ValueError("Crete parent totals drifted: %r" % parent_counts)
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Crete rank totals drifted: %r" % rank_counts)
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Crete kind totals drifted: %r" % kind_counts)
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Crete English name coverage drifted")
    expected_seats = {item["seat"] for item in ROWS if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Crete English seat coverage drifted")
    validate_ledger(ROWS)
    grouped = {parent: [] for parent in EXPECTED_PARENTS}
    for item in ROWS:
        grouped[item["parent"]].append(dict(item))
    return {
        parent: {
            "v": 1,
            "parent": parent,
            "country": "GR",
            "rows": grouped[parent],
        }
        for parent in sorted(grouped)
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("directory_crete_country: %s" % error, file=sys.stderr)
        return 1
    if args.dump:
        json.dump(payloads, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        summary = published_summary(ROWS)
        print(
            "directory_crete_country: ok "
            "(%d rows, %d parents, %d contact bodies, "
            "%d phone values, %d email values, %d body-owned sites)" %
            (
                summary["total"],
                len(summary["parents"]),
                summary["contact_bodies"],
                summary["public_phone_values"],
                summary["public_email_values"],
                summary["body_owned_sites"],
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
