#!/usr/bin/env python3
"""Validate exact current bodies named by Dodecanese Church rosters.

This tranche is intentionally independent of the shared directory aggregator.
It emits later-integration payloads for the five Dodecanese metropolises and
the Patriarchal Exarchate of Patmos. Only current first-party Church rosters
control publication. Aggregate-only chapels and historical bodies stay in the
candidate ledger.

    python tools/directory_dodecanese_country.py --check
    python tools/directory_dodecanese_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "dodecanese_country.json"
)

SOURCES = {
    "ep-rhodes": "https://ec-patr.org/entities/iera-mitropoli-rodoy/",
    "ep-kos": "https://ec-patr.org/entities/iera-mitropoli-kooy-nisyroy/",
    "ep-leros": (
        "https://ec-patr.org/entities/"
        "iera-mitropoli-leroy-kalymnoy-astypalaias/"
    ),
    "ep-karpathos": (
        "https://ec-patr.org/entities/iera-mitropoli-karpathoy-kasoy/"
    ),
    "ep-syme": "https://ec-patr.org/entities/iera-mitropoli-symis/",
    "ep-patmos": (
        "https://ec-patr.org/entities/patriarxiki-eksarxia-patmoy/"
    ),
}

RHODES_DISTRICT_SOURCES = {
    "Rhodes": "https://www.imr.gr/article/9/enories-d-d-rodoy",
    "Ialysos": "https://www.imr.gr/article/37/enories-d-d-ialysoy",
    "Petaloudes": "https://www.imr.gr/article/38/enories-d-d-petaloydwn",
    "Kamiros": "https://www.imr.gr/article/39/enories-d-d-kameiroy",
    "Attavyros": "https://www.imr.gr/article/40/enories-d-d-attabyroy",
    "South Rhodes": (
        "https://www.imr.gr/article/41/enories-d-d-notias-rodoy"
    ),
    "Lindos": "https://www.imr.gr/article/42/enories-d-d-lindiwn",
    "Archangelos": "https://www.imr.gr/article/43/enories-d-d-arxaggeloy",
    "Afantou": "https://www.imr.gr/article/44/enories-d-d-afantoy",
    "Kallithea": "https://www.imr.gr/article/45/enories-d-d-kallitheas",
}
RHODES_CHAPEL_SOURCE = "https://www.imr.gr/article/46/parekklhsia-idrymatwn"
RHODES_MONASTERY_SOURCES = {
    "men": "https://www.imr.gr/list/19",
    "women": "https://www.imr.gr/list/36",
    "english": "https://www.imr.gr/list/58/monasteries",
}


def row(row_id, parent, name, local, seat, rank, kind, source,
        phones=None, emails=None, site=None, extra_sources=None,
        address=None):
    sources = [source] + list(extra_sources or [])
    if site and site not in sources:
        sources.append(site)
    item = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "GR",
        "sources": sources,
    }
    if address:
        item["address"] = list(address)
    if phones:
        item["phones"] = list(phones)
    if emails:
        item["emails"] = list(emails)
    if phones or emails:
        item["contact_sources"] = list(extra_sources or [source])[:3]
        item["contact_checked"] = CHECKED
    if site:
        item["site"] = site
    return item


ROWS = []


def add_group(parent, prefix, source, entries, extra_source=None):
    for entry in entries:
        values = list(entry) + [None] * (11 - len(entry))
        (slug, name, local, seat, rank, kind, phones, emails, site,
         extra_sources, address) = values[:11]
        if extra_sources is None and extra_source:
            extra_sources = [extra_source]
        ROWS.append(row(
            "%s-%s" % (prefix, slug), parent, name, local, seat,
            rank, kind, source, phones, emails, site, extra_sources, address,
        ))


# Body rosters follow below. A source line that names current personnel is
# never copied as a body contact. Only numbers printed as the institution's
# own telephone, office line, or explicit contact line are carried.

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("rhodes-presentation", "Metropolitan Church of the Presentation of the Theotokos in Rhodes", "Μητροπολιτικός Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Ρόδου", "Rhodes", "Metropolitan Church", "parish", ["22410 21447"]),
    ("rhodes-annunciation", "Cathedral of the Annunciation of the Theotokos in Rhodes", "Καθεδρικός Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου Ρόδου", "Rhodes", "Cathedral", "parish", ["22410 77916"]),
    ("rhodes-anastasia", "Church of Saint Anastasia Pharmacolytria in Rhodes", "Ἱερός Ναός Ἁγίας Ἀναστασίας Φαρμακολυτρίας Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 33676"]),
    ("rhodes-protection-euthymius", "Church of the Protection of the Theotokos and Saint Euthymius in Rhodes", "Ἱερός Ναός Ἁγίας Σκέπης καί Ἁγίου Εὐθυμίου Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 43495"]),
    ("rhodes-unmercenaries", "Church of the Holy Unmercenaries in Rhodes", "Ἱερός Ναός Ἁγίων Ἀναργύρων Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 24725"]),
    ("rhodes-apostles", "Church of the Holy Apostles in Rhodes", "Ἱερός Ναός Ἁγίων Ἀποστόλων Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 67407"]),
    ("rhodes-george-upper", "Upper Church of Saint George in Rhodes", "Ἱερός Ναός Ἁγίου Γεωργίου Ἄνω Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 33675"]),
    ("rhodes-george-lower", "Lower Church of Saint George in Rhodes", "Ἱερός Ναός Ἁγίου Γεωργίου Κάτω Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 20886"]),
    ("rhodes-demetrius-old-cemetery", "Church of Saint Demetrius at the Old Cemetery in Rhodes", "Ἱερός Ναός Ἁγίου Δημητρίου παλαιοῦ Κοιμητηρίου Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 20615"]),
    ("rhodes-demetrius-rodini", "Church of Saint Demetrius in Rodini", "Ἱερός Ναός Ἁγίου Δημητρίου Ροδινίου", "Rhodes", "Parish Church", "parish", ["22410 33349"]),
    ("rhodes-john-forerunner", "Church of Saint John the Forerunner in Rhodes", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Προδρόμου Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 21965"]),
    ("rhodes-nicholas", "Church of Saint Nicholas in Rhodes", "Ἱερός Ναός Ἁγίου Νικολάου Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 29407"]),
    ("rhodes-panteleimon", "Church of Saint Panteleimon in Rhodes", "Ἱερός Ναός Ἁγίου Παντελεήμονος Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 21499"]),
    ("rhodes-phanourios", "Church of Saint Phanourios in Rhodes", "Ἱερός Ναός Ἁγίου Φανουρίου Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 32966"]),
    ("rhodes-christopher", "Church of Saint Christopher in Rhodes", "Ἱερός Ναός Ἁγίου Χριστοφόρου Ρόδου", "Rhodes", "Parish Church", "parish"),
    ("rhodes-ascension", "Church of the Ascension of the Lord in Rhodes", "Ἱερός Ναός Ἀναλήψεως τοῦ Κυρίου Ρόδου", "Rhodes", "Parish Church", "parish", ["22410 65061"]),
    ("rhodes-neochori-presentation", "Church of the Presentation of the Theotokos in Neochori", "Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Νεοχωρίου", "Rhodes", "Parish Church", "parish", ["22410 38190"]),
], RHODES_DISTRICT_SOURCES["Rhodes"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("ialysos-dormition", "Church of the Dormition of the Theotokos in Ialysos", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ἰαλυσοῦ", "Ialysos", "Parish Church", "parish"),
    ("ixia-transfiguration", "Church of the Transfiguration of the Savior in Ixia", "Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος Ἰξιᾶς", "Ixia", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Ialysos"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("damatria-john-theologian", "Church of Saint John the Theologian in Damatria", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Δαματριᾶς", "Damatria", "Parish Church", "parish"),
    ("theologos-spyridon", "Church of Saint Spyridon in Theologos", "Ἱερός Ναός Ἁγίου Σπυρίδωνος Θεολόγου", "Theologos", "Parish Church", "parish"),
    ("kremasti-dormition", "Church of the Dormition of the Theotokos in Kremasti", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Κρεμαστῆς", "Kremasti", "Parish Church", "parish"),
    ("maritsa-archangel-michael", "Church of the Archangel Michael in Maritsa", "Ἱερός Ναός Ταξιάρχου Μιχαήλ Μαριτσῶν", "Maritsa", "Parish Church", "parish"),
    ("paradeisi-nicholas", "Church of Saint Nicholas in Paradeisi", "Ἱερός Ναός Ἁγίου Νικολάου Παραδεισίου", "Paradeisi", "Parish Church", "parish"),
    ("pastida-nicholas", "Church of Saint Nicholas in Pastida", "Ἱερός Ναός Ἁγίου Νικολάου Παστίδας", "Pastida", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Petaloudes"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("apollona-cross", "Church of the Exaltation of the Precious Cross in Apollona", "Ἱερός Ναός Τιμίου Σταυροῦ Ἀπόλλωνα", "Apollona", "Parish Church", "parish"),
    ("dimylia-forty-martyrs", "Church of the Forty Martyrs in Dimylia", "Ἱερός Ναός Ἁγίων Τεσσαράκοντα Μαρτύρων Διμυλιᾶς", "Dimylia", "Parish Church", "parish"),
    ("eleousa-charalambos", "Church of Saint Charalambos in Eleousa", "Ἱερός Ναός Ἁγίου Χαραλάμπους Ἐλεούσης", "Eleousa", "Parish Church", "parish"),
    ("kalavarda-catherine", "Church of Saint Catherine in Kalavarda", "Ἱερός Ναός Ἁγίας Αἰκατερίνης Καλαβάρδας", "Kalavarda", "Parish Church", "parish"),
    ("platania-george", "Church of Saint George in Platania", "Ἱερός Ναός Ἁγίου Γεωργίου Πλατανίων", "Platania", "Parish Church", "parish"),
    ("salakos-dormition", "Church of the Dormition of the Theotokos in Salakos", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Σαλάκου", "Salakos", "Parish Church", "parish"),
    ("soroni-luke", "Church of the Evangelist Luke in Soroni", "Ἱερός Ναός Εὐαγγελιστοῦ Λουκᾶ Σορωνῆς", "Soroni", "Parish Church", "parish"),
    ("fanes-john-forerunner", "Church of Saint John the Forerunner in Fanes", "Ἱερός Ναός Ἁγίου Ἰωάννου Προδρόμου Φανῶν", "Fanes", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Kamiros"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("embonas-dormition", "Church of the Dormition of the Theotokos in Embonas", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ἔμπωνα", "Embonas", "Parish Church", "parish"),
    ("agios-isidoros-isidore", "Church of Saint Isidore in Agios Isidoros", "Ἱερός Ναός Ἁγίου Ἰσιδώρου", "Agios Isidoros", "Parish Church", "parish"),
    ("kritinia-george", "Church of Saint George in Kritinia", "Ἱερός Ναός Ἁγίου Γεωργίου Κρητηνίας", "Kritinia", "Parish Church", "parish"),
    ("mandriko-holy-trinity", "Church of the Holy Trinity in Mandriko", "Ἱερός Ναός Ἁγίας Τριάδος Μανδρικοῦ", "Mandriko", "Parish Church", "parish"),
    ("monolithos-thomas", "Church of the Apostle Thomas in Monolithos", "Ἱερός Ναός Ἀποστόλου Θωμᾶ Μονολίθου", "Monolithos", "Parish Church", "parish"),
    ("siana-panteleimon", "Church of Saint Panteleimon in Siana", "Ἱερός Ναός Ἁγίου Παντελεήμονος Σιάνων", "Siana", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Attavyros"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("apolakkia-marina", "Church of Saint Marina in Apolakkia", "Ἱερός Ναός Ἁγίας Μαρίνης Ἀπολακκιᾶς", "Apolakkia", "Parish Church", "parish"),
    ("arnitha-george", "Church of Saint George in Arnitha", "Ἱερός Ναός Ἁγίου Γεωργίου Ἀρνίθας", "Arnitha", "Parish Church", "parish"),
    ("asklipio-dormition", "Church of the Dormition of the Theotokos in Asklipio", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ἀσκληπειοῦ", "Asklipio", "Parish Church", "parish"),
    ("vati-john-theologian", "Church of Saint John the Theologian in Vati", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Βατίου", "Vati", "Parish Church", "parish"),
    ("gennadi-john-theologian", "Church of the Evangelist John the Theologian in Gennadi", "Ἱερός Ναός Εὐαγγελιστοῦ Ἰωάννου τοῦ Θεολόγου Γενναδίου", "Gennadi", "Parish Church", "parish"),
    ("istrios-mercurius", "Church of Saint Mercurius in Istrios", "Ἱερός Ναός Ἁγίου Μερκουρίου Ἰστρίου", "Istrios", "Parish Church", "parish"),
    ("kattavia-paraskevi", "Church of Saint Paraskevi in Kattavia", "Ἱερός Ναός Ἁγίας Παρασκευῆς Κατταβιᾶς", "Kattavia", "Parish Church", "parish"),
    ("lachania-george", "Church of Saint George in Lachania", "Ἱερός Ναός Ἁγίου Γεωργίου Λαχανιᾶς", "Lachania", "Parish Church", "parish"),
    ("mesanagros-archangels", "Church of the Archangels in Mesanagros", "Ἱερός Ναός Ταξιαρχῶν Μεσαναγροῦ", "Mesanagros", "Parish Church", "parish"),
    ("profylia-nativity", "Church of the Nativity of the Theotokos in Profylia", "Ἱερός Ναός Γενεσίου τῆς Θεοτόκου Προφυλίων", "Profylia", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["South Rhodes"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("laerma-george", "Church of Saint George in Laerma", "Ἱερός Ναός Ἁγίου Γεωργίου Λαέρμων", "Laerma", "Parish Church", "parish"),
    ("lardos-archangel-michael", "Church of the Archangel Michael in Lardos", "Ἱερός Ναός Ἀρχιστρατήγου Μιχαήλ Λάρδου", "Lardos", "Parish Church", "parish"),
    ("lindos-dormition", "Church of the Dormition of the Theotokos in Lindos", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Λίνδου", "Lindos", "Parish Church", "parish"),
    ("kalathos-archangel-michael", "Church of the Archangel Michael in Kalathos", "Ἱερός Ναός Ταξιάρχου Μιχαήλ Καλάθου", "Kalathos", "Parish Church", "parish"),
    ("pylona-gerasimus", "Church of Saint Gerasimus in Pylona", "Ἱερός Ναός Ἁγίου Γερασίμου Πυλώνας", "Pylona", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Lindos"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("archangelos-archangel-michael", "Church of the Archangel Michael in Archangelos", "Ἱερός Ναός Ἀρχαγγέλου Μιχαήλ Ἀρχαγγέλου", "Archangelos", "Parish Church", "parish"),
    ("malona-george", "Church of Saint George in Malona", "Ἱερός Ναός Ἁγίου Γεωργίου Μαλώνας", "Malona", "Parish Church", "parish"),
    ("massari-presentation", "Church of the Presentation of the Theotokos in Massari", "Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Μασσάρων", "Massari", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Archangelos"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("archipolis-demetrius", "Church of Saint Demetrius in Archipolis", "Ἱερός Ναός Ἁγίου Δημητρίου Ἀρχιπόλεως", "Archipolis", "Parish Church", "parish"),
    ("afantou-dormition", "Church of the Dormition of the Theotokos in Afantou", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ἀφάντου", "Afantou", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Afantou"])

add_group("ep-rhodes", "gr-ep-rhodes", SOURCES["ep-rhodes"], [
    ("kalythies-transfiguration", "Church of the Transfiguration of the Savior in Kalythies", "Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος Καλυθιῶν", "Kalythies", "Parish Church", "parish"),
    ("koskinou-presentation", "Church of the Presentation of the Theotokos in Koskinou", "Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Κοσκινοῦ", "Koskinou", "Parish Church", "parish"),
    ("faliraki-nectarius", "Church of Saint Nectarius in Faliraki", "Ἱερός Ναός Ἁγίου Νεκταρίου Φαληρακίου", "Faliraki", "Parish Church", "parish"),
    ("psinthos-nativity", "Church of the Nativity of the Theotokos in Psinthos", "Ἱερός Ναός Γενεσίου τῆς Θεοτόκου Ψίνθου", "Psinthos", "Parish Church", "parish"),
], RHODES_DISTRICT_SOURCES["Kallithea"])

add_group("ep-rhodes", "gr-ep-rhodes-chapel", SOURCES["ep-rhodes"], [
    ("archangels-municipal-cemetery", "Chapel of the Archangels at the Rhodes Municipal Cemetery", "Παρεκκλήσιον Παμμεγίστων Ταξιαρχῶν Δημοτικοῦ Κοιμητηρίου Ρόδου", "Rhodes", "Cemetery Chapel", "parish"),
    ("irene-female-reform-school", "Chapel of Saint Irene at the Rhodes Female Reform School", "Παρεκκλήσιον Ἁγίας Εἰρήνης Κ.Π.Μ. Θηλέων Ρόδου", "Rhodes", "Institutional Chapel", "parish"),
    ("nectarius-male-reform-school", "Chapel of Saint Nectarius at the Rhodes Male Reform School", "Παρεκκλήσιον Ἁγίου Νεκταρίου Κ.Π.Μ. Ἀρρένων Ρόδου", "Rhodes", "Institutional Chapel", "parish"),
    ("catherine-former-hospital", "Chapel of Saint Catherine at the Former Rhodes General Hospital", "Παρεκκλήσιον Ἁγίας Αἰκατερίνης πρώην Γενικοῦ Νοσοκομείου Ρόδου", "Rhodes", "Hospital Chapel", "parish"),
    ("irene-aegean-university", "Chapel of Saint Irene at the University of the Aegean", "Παρεκκλήσιον Ἁγίας Εἰρήνης Πανεπιστημίου Αἰγαίου", "Rhodes", "Institutional Chapel", "parish"),
    ("tryphon-afantou", "Chapel of Saint Tryphon in Afantou", "Παρεκκλήσιον Ἁγίου Τρύφωνος Ἀφάντου Ρόδου", "Afantou", "Chapel", "parish", ["22410-56.221"]),
    ("catherine-hospital", "Chapel of Saint Catherine at Rhodes General Hospital", "Παρεκκλήσιον Ἁγίας Αἰκατερίνης Γενικοῦ Νοσοκομείου Ρόδου", "Rhodes", "Hospital Chapel", "parish"),
    ("archangels-vrykous-brotherhood", "Chapel of the Archangels of the Vrykous Brotherhood of Olympos", "Παρεκκλήσιον Παμμεγίστων Ταξιαρχῶν Ἀδελφότητος Ὀλυμπιτῶν Ρόδου «Ἡ Βρυκούς»", "Rhodes", "Brotherhood Chapel", "parish"),
], RHODES_CHAPEL_SOURCE)

add_group("ep-rhodes", "gr-ep-rhodes-monastery", SOURCES["ep-rhodes"], [
    ("archangel-michael-tharri", "Monastery of the Archangel Michael at Tharri", "Ἱερά Μονή Ταξιάρχου Μιχαήλ Θαρρίου", "Laerma", "Monastery", "monastery", ["22440-61.460", "22440-61.467"], None, None, [RHODES_MONASTERY_SOURCES["men"], RHODES_MONASTERY_SOURCES["english"]]),
    ("nativity-theotokos-skiadi", "Monastery of the Nativity of the Theotokos at Skiadi", "Ἱερά Μονή Γενεσίου Θεοτόκου Σκιαδίου", "Mesanagros", "Monastery", "monastery", ["22440-46006"], None, None, [RHODES_MONASTERY_SOURCES["men"], RHODES_MONASTERY_SOURCES["english"]]),
    ("theotokos-faneromeni-ixia", "Monastery of the Theotokos Faneromeni in Ixia", "Ἱερά Μονή Ὑπεραγίας Θεοτόκου Φανερωμένης Ἰξιᾶς", "Ixia", "Monastery", "monastery", None, None, None, [RHODES_MONASTERY_SOURCES["men"], RHODES_MONASTERY_SOURCES["english"]]),
    ("john-theologian-artamitis", "Monastery of Saint John the Theologian at Artamitis", "Ἱερά Μονή Ἁγίου Ἰωάννου τοῦ Θεολόγου Ἀρταμίτου", "Agios Isidoros", "Monastery", "monastery", None, None, None, [RHODES_MONASTERY_SOURCES["men"], RHODES_MONASTERY_SOURCES["english"]]),
    ("theotokos-paramythia", "Monastery of the Theotokos Paramythia", "Ἱερά Μονή Ὑπεραγίας Θεοτόκου Παραμυθίας", "Afantou", "Monastery", "monastery", ["22410-52.199"], None, None, [RHODES_MONASTERY_SOURCES["men"], RHODES_MONASTERY_SOURCES["english"]]),
    ("dormition-ypseni", "Monastery of the Dormition of the Theotokos at Ypseni", "Ἱερά Μονή Κοιμήσεως Θεοτόκου τοῦ Ὕψους Ὑψενῆς", "Lardos", "Convent", "monastery", ["22440-44.245"], None, None, [RHODES_MONASTERY_SOURCES["women"], RHODES_MONASTERY_SOURCES["english"]]),
    ("nectarius-kryoneri", "Monastery of Saint Nectarius at Kryoneri", "Ἱερά Μονή Ἁγίου Νεκταρίου Κρυονερίου", "Archipolis", "Convent", "monastery", ["22460-98180"], None, None, [RHODES_MONASTERY_SOURCES["women"], RHODES_MONASTERY_SOURCES["english"]]),
    ("theotokos-pantanassa-soroni", "Monastery of the Theotokos Pantanassa at Soroni", "Ἱερά Μονή Ὑπεραγίας Θεοτόκου Παντανάσσης Σορωνῆς", "Soroni", "Convent", "monastery", ["22410-42.188"], None, None, [RHODES_MONASTERY_SOURCES["women"], RHODES_MONASTERY_SOURCES["english"]]),
    ("life-giving-spring-filerimos", "Monastery of the Life-giving Spring at Filerimos", "Ἱερά Μονή Ζωοδόχου Πηγῆς Φιλερήμου", "Ialysos", "Monastery", "monastery", ["22410-44.555"]),
    ("archangel-michael-kamyri", "Monastery of the Archangel Michael at Kamyri", "Ἱερά Μονή Ἀρχαγγέλου Μιχαήλ Καμυρί", "Massari", "Monastery", "monastery"),
    ("theotokos-eleousa-koskinisti", "Monastery of the Theotokos Eleousa at Koskinisti", "Ἱερά Μονή Ὑπεραγίας Θεοτόκου Ἐλεούσης Κοσκινιστῆς", "Eleousa", "Monastery", "monastery"),
    ("nativity-theotokos-amartos", "Monastery of the Nativity of the Theotokos at Amartos", "Ἱερά Μονή Γενεσίου τῆς Θεοτόκου Ἀμάρτου", "Kritinia", "Monastery", "monastery"),
    ("prophet-amos-kalythies", "Monastery of the Prophet Amos in Kalythies", "Ἱερά Μονή Προφήτου Ἀμώς Καλυθιῶν", "Kalythies", "Monastery", "monastery"),
    ("philemon-arnitha", "Monastery of Saint Philemon in Arnitha", "Ἱερά Μονή Ἁγίου Φιλήμονος Ἀρνίθας", "Arnitha", "Monastery", "monastery"),
    ("theotokos-tsambika", "Monastery of the Theotokos Tsambika in Archangelos", "Ἱερά Μονή Ὑπεραγίας Θεοτόκου Τσαμπίκας Ἀρχαγγέλου", "Archangelos", "Monastery", "monastery"),
    ("theotokos-eleousa-kalythies", "Monastery of the Theotokos Eleousa in Kalythies", "Ἱερά Μονή Ὑπεραγίας Θεοτόκου Ἐλεούσης Καλυθιῶν", "Kalythies", "Monastery", "monastery"),
    ("dormition-kalopetra", "Monastery of the Dormition of the Theotokos at Kalopetra", "Ἱερά Μονή Κοιμήσεως Θεοτόκου Καλόπετρας", "Theologos", "Monastery", "monastery"),
    ("life-giving-spring-plimmiri", "Monastery of the Life-giving Spring at Plimmiri", "Ἱερά Μονή Ζωοδόχου Πηγῆς Πλημμυρίου", "Plimmiri", "Monastery", "monastery"),
    ("george-lachania", "Monastery of Saint George in Lachania", "Ἱερά Μονή Ἁγίου Γεωργίου Λαχανιᾶς", "Lachania", "Monastery", "monastery"),
    ("prophet-elias", "Monastery of the Prophet Elias in Rhodes", "Ἱερά Μονή Προφήτου Ἠλιού Ρόδου", "Rhodes", "Monastery", "monastery"),
])

add_group("ep-kos", "gr-ep-kos", SOURCES["ep-kos"], [
    ("kos-nicholas-metropolitan", "Metropolitan Church of Saint Nicholas in Kos", "Ἱερός Μητροπολιτικός Ναός Ἁγίου Νικολάου Κῶ", "Kos", "Metropolitan Church", "parish", ["22420-22383"], None, None, None, ["Κοραῆ 10, Κῶς"]),
    ("kos-paraskevi-cathedral", "Cathedral of Saint Paraskevi in Kos", "Ἱερός Καθεδρικός Ναός Ἁγίας Παρασκευῆς Κῶ", "Kos", "Cathedral", "parish", ["22420-28213"], None, None, None, ["Ἀλεξάνδρου Ὑψηλάντου 20, Κῶς"]),
    ("kos-paul", "Church of Saint Paul in Kos", "Ἱερός Ναός Ἁγίου Παύλου πόλεως Κῶ", "Kos", "Parish Church", "parish", ["22420-28620"], None, None, None, ["Θεμιστοκλέους 22, Κῶς"]),
    ("platani-athanasius-gabriel", "Church of Saint Athanasius and the Archangel Gabriel in Platani", "Ἱερός Ναός Ἁγίου Ἀθανασίου καί Ἀρχαγγέλου Γαβριήλ Πλατανίου", "Platani", "Parish Church", "parish", ["22420-30355"], None, None, None, ["Πλατάνι, Κῶς"]),
    ("paradeisi-all-saints", "Church of All Saints in Paradeisi", "Ἱερός Ναός Ἁγίων Πάντων Παραδεισίου", "Paradeisi", "Parish Church", "parish", ["22420-24537"], None, None, None, ["Παραδείσι, Κῶς"]),
    ("nea-alikarnassos-george", "Church of Saint George in Nea Alikarnassos", "Ἱερός Ναός Ἁγίου Γεωργίου Νέας Ἁλικαρνασσοῦ", "Nea Alikarnassos", "Parish Church", "parish"),
    ("zipari-ascension", "Church of the Ascension of the Lord in Zipari", "Ἱερός Ναός Θείας Ἀναλήψεως Ζηπαρίου", "Zipari", "Parish Church", "parish", ["22420-68240"], None, None, None, ["Ζηπάρι, Κῶς"]),
    ("asfendiou-annunciation", "Church of the Annunciation of the Theotokos in Asfendiou", "Ἱερός Ναός Εὐαγγελισμοῦ Θεοτόκου Ἀσφενδιοῦ", "Asfendiou", "Parish Church", "parish"),
    ("asfendiou-bodiless-powers", "Church of the Holy Bodiless Powers in Asfendiou", "Ἱερός Ναός Ἀσωμάτων Ἀσφενδιοῦ", "Asfendiou", "Parish Church", "parish", ["6948518430"], None, None, None, ["Ἀσφενδιοῦ, Κῶς"]),
    ("zia-dormition", "Church of the Dormition of the Theotokos in Zia", "Ἱερός Ναός Κοιμήσεως Θεοτόκου Ζιᾶς", "Zia", "Parish Church", "parish"),
    ("lagoudi-nativity", "Church of the Nativity of the Theotokos in Lagoudi", "Ἱερός Ναός Γενεσίου Θεοτόκου Λαγουδίου", "Lagoudi", "Parish Church", "parish"),
    ("linopoti-paul", "Church of Saint Paul in Linopoti", "Ἱερός Ναός Ἁγίου Παύλου Λινοποτίου", "Linopoti", "Parish Church", "parish"),
    ("chaichoutes-demetrius", "Church of Saint Demetrius in Chaichoutes", "Ἱερός Ναός Ἁγίου Δημητρίου Χαϊχουτῶν", "Chaichoutes", "Parish Church", "parish"),
    ("pyli-nicholas", "Church of Saint Nicholas in Pyli", "Ἱερός Ναός Ἁγίου Νικολάου Πυλίου", "Pyli", "Parish Church", "parish"),
    ("pyli-george", "Church of Saint George in Pyli", "Ἱερός Ναός Ἁγίου Γεωργίου Πυλίου", "Pyli", "Parish Church", "parish", ["22420-41584"], None, None, None, ["Πυλί, Κῶς"]),
    ("amaniou-presentation", "Church of the Presentation of the Theotokos in Amaniou", "Ἱερός Ναός Εἰσοδίων Θεοτόκου Ἀμανιοῦ", "Amaniou", "Parish Church", "parish", ["22420-41687"], None, None, None, ["Ἀμανιοῦ, Κῶς"]),
    ("antimachia-holy-trinity", "Church of the Holy Trinity in Antimachia", "Ἱερός Ναός Ἁγίας Τριάδος Ἀντιμαχείας", "Antimachia", "Parish Church", "parish", ["22420-51177"], None, None, None, ["Ἀντιμάχεια, Κῶς"]),
    ("antimachia-dormition", "Church of the Dormition of the Theotokos in Antimachia", "Ἱερός Ναός Κοιμήσεως Θεοτόκου Ἀντιμαχείας", "Antimachia", "Parish Church", "parish", ["22420-51065"], None, None, None, ["Ἀντιμάχεια, Κῶς"]),
    ("antimachia-apostles", "Church of the Holy Apostles in Antimachia", "Ἱερός Ναός Ἁγίων Ἀποστόλων Ἀντιμαχείας", "Antimachia", "Parish Church", "parish", ["22420-51515"], None, None, None, ["Ἀντιμάχεια, Κῶς"]),
    ("mastichari-annunciation", "Church of the Annunciation of the Theotokos in Mastichari", "Ἱερός Ναός Εὐαγγελισμοῦ Θεοτόκου Μαστιχαρίου", "Mastichari", "Parish Church", "parish"),
    ("kardamaina-nativity", "Church of the Nativity of the Theotokos in Kardamaina", "Ἱερός Ναός Γενεσίου Θεοτόκου Καρδαμαίνης", "Kardamaina", "Parish Church", "parish", ["22420-91380"], None, None, None, ["Καρδάμαινα, Κῶς"]),
    ("kefalos-presentation", "Church of the Presentation of the Theotokos in Kefalos", "Ἱερός Ναός Εἰσοδίων Θεοτόκου Κεφάλου", "Kefalos", "Parish Church", "parish"),
    ("nisyros-potamitissa-metropolitan", "Metropolitan Church of the Nativity of the Theotokos Potamitissa", "Ἱερός Μητροπολιτικός Ναός Γενεσίου Θεοτόκου Ποταμητίσσης", "Mandraki, Nisyros", "Metropolitan Church", "parish", ["22420-31253"], None, None, None, ["Μανδράκι, Νίσυρος 85303"]),
    ("nisyros-emporeios-nativity", "Church of the Nativity of the Theotokos in Emporeios", "Ἱερός Ναός Γενεσίου Θεοτόκου Ἐμπορειοῦ", "Emporeios, Nisyros", "Parish Church", "parish"),
    ("nisyros-nikia-presentation", "Church of the Presentation of the Theotokos in Nikia", "Ἱερός Ναός Εἰσοδίων Θεοτόκου Νικιῶν", "Nikia, Nisyros", "Parish Church", "parish"),
    ("nisyros-paloi-apostles", "Church of the Holy Apostles in Paloi", "Ἱερός Ναός Ἁγίων Ἀποστόλων Πάλων", "Paloi, Nisyros", "Parish Church", "parish"),
])

add_group("gr-ep-kos-kos-paul", "gr-ep-kos-chapel", SOURCES["ep-kos"], [
    ("panagia-faneromeni", "Chapel of Panagia Faneromeni in Kos", "Ἱερόν Παρεκκλήσιον Παναγίας Φανερωμένης Κῶ", "Kos", "Chapel", "parish", None, None, None, None, ["Μπουμπουλίνας καί Μανδηλαρᾶ 33, Κῶς"]),
])

add_group("gr-ep-kos-linopoti-paul", "gr-ep-kos-chapel", SOURCES["ep-kos"], [
    ("john-chrysostom-baptistery", "Baptistery of Saint John Chrysostom in Linopoti", "Ἱερός Ναός Ἁγίου Ἰωάννου Χρυσοστόμου Βαπτιστήριον", "Linopoti", "Baptistery", "parish"),
])

add_group("ep-kos", "gr-ep-kos-shrine", SOURCES["ep-kos"], [
    ("nisyros-niketas", "Pilgrimage Church of Saint Niketas of Nisyros", "Ἱερός Προσκυνηματικός Ναός Ἁγίου Νικήτα Νισυρίου", "Mandraki, Nisyros", "Pilgrimage Church", "parish"),
    ("nisyros-panteleimon-avlaki", "Pilgrimage Church of Saint Panteleimon at Avlaki", "Ἱερός Προσκυνηματικός Ναός Ἁγίου Παντελεήμονος Αὐλακίου", "Nikia, Nisyros", "Pilgrimage Church", "parish", ["22420-31253"], None, None, None, ["Νικιά, Νίσυρος 85303"]),
    ("giali-john-forerunner", "Church of Saint John the Forerunner on Giali", "Ἱερός Ναός Ἁγίου Ἰωάννου Προδρόμου νήσου Γυαλί", "Giali", "Church", "parish", ["22420-31280"]),
    ("agios-antonios-anthony", "Country Chapel of Saint Anthony on Agios Antonios", "Ἱερόν Ἐξωκκλήσιον Ἁγίου Ἀντωνίου νήσου Ἁγίου Ἀντωνίου", "Agios Antonios", "Country Chapel", "parish"),
])

add_group("ep-kos", "gr-ep-kos-monastery", SOURCES["ep-kos"], [
    ("panagia-kastrianon-palaio-pyli", "Monastery of Panagia Kastrianon at Palaio Pyli", "Ἱερά Μονή Παναγίας Καστριανῶν Παλαιοῦ Πυλίου", "Palaio Pyli", "Monastery", "monastery"),
    ("forerunner-thymiano-kefalos", "Metropolitan Monastery of Saint John the Forerunner at Thymiano, Kefalos", "Ἱερά Μητροπολιτική Μονή Τιμίου Προδρόμου Θυμιανοῦ Κεφάλου", "Kefalos", "Metropolitan Monastery", "monastery"),
    ("nectarius", "Monastery of Saint Nectarius in Kos", "Ἱερά Μονή Ἁγίου Νεκταρίου Κῶ", "Kos", "Convent", "monastery", ["22420-22453"]),
    ("fovea-prostasia-menas", "Monastery of the Fovea Prostasia and Saint Menas", "Ἱερά Μονή Φοβερᾶς Προστασίας καί Ἁγίου Μηνᾶ", "Kos", "Monastery", "monastery"),
    ("melou-vourrina", "Monastery of Venerable Melou at Vourrina", "Ἱερά Μονή Ὁσίας Μελοῦς ἐν Βουρρίνῃ τῆς Κῶ", "Vourrina, Kos", "Monastery", "monastery"),
    ("dodecanese-saints", "Monastery of the Saints of the Dodecanese and of the Metropolis of Kos and Nisyros", "Ἱερά Μονή τῶν ἐν Δωδεκανήσῳ Ἁγίων καί τῶν ἐν τῇ Ἱερᾷ Μητροπόλει Κώου καί Νισύρου διαλαμψάντων", "Kos", "Monastery", "monastery"),
    ("irene-therma", "Monastery of Saint Irene at Therma", "Ἱερά Μονή Ἁγίας Εἰρήνης Θερμῶν", "Therma, Kos", "Monastery", "monastery"),
    ("prophet-zechariah", "Monastery of the Prophet Zechariah in Kos", "Ἱερά Μονή Προφήτου Ζαχαρίου", "Kos", "Monastery", "monastery"),
    ("christ-savior-dikaios", "Monastery of Christ the Savior on Mount Dikaios", "Ἱερά Μονή Σωτῆρος Χριστοῦ ὄρους Δικαίου", "Mount Dikaios, Kos", "Monastery", "monastery"),
    ("john-theologian-dikaios", "Monastery of Saint John the Theologian on Mount Dikaios", "Ἱερά Μονή Ἁγίου Ἰωάννου Θεολόγου ὄρους Δικαίου", "Mount Dikaios, Kos", "Monastery", "monastery"),
    ("prophet-elias-skenourion", "Monastery of the Prophet Elias at Skenourion Kathisma", "Ἱερά Μονή Προφήτου Ἠλιού Σκηνούριον Κάθισμα", "Kos", "Monastery", "monastery"),
    ("life-giving-spring-monagri", "Monastery of Panagia the Life-giving Spring at Monagri", "Ἱερά Μονή Παναγίας Ζωοδόχου Πηγῆς εἰς τό Μονάγρι", "Monagri, Kos", "Monastery", "monastery"),
    ("nisyros-panagia-spiliani", "Monastery of Panagia Spiliani on Nisyros", "Ἱερά Μονή Παναγίας Σπηλιανῆς Νισύρου", "Mandraki, Nisyros", "Monastery", "monastery", ["22420-31125"], None, None, None, ["Μανδράκι, Νίσυρος 85303"]),
    ("nisyros-panagia-kyra-emporeios", "Monastery of Panagia Kyra in Emporeios", "Ἱερά Μονή Παναγίας Κυρᾶς Ἐμπορειοῦ", "Emporeios, Nisyros", "Monastery", "monastery", ["22420-31432"], None, None, None, ["Ἐμπορειός, Νίσυρος 85303"]),
    ("nisyros-john-theologian-nikia", "Monastery of Saint John the Theologian in Nikia", "Ἱερά Μονή Ἁγίου Ἰωάννου Θεολόγου Νικιῶν", "Nikia, Nisyros", "Monastery", "monastery", ["22420-31253"], None, None, None, ["Νικιά, Νίσυρος 85303"]),
    ("nisyros-precious-cross-argos", "Monastery of the Precious Cross at Argos", "Ἱερά Μονή Τιμίου Σταυροῦ Ἄργους", "Mandraki, Nisyros", "Monastery", "monastery", ["22420-31253"], None, None, None, ["Μανδράκι, Νίσυρος 85303"]),
    ("nisyros-annunciation-mandraki", "Monastery of the Annunciation of the Theotokos in Mandraki", "Ἱερά Μονή Εὐαγγελισμοῦ Θεοτόκου Μανδρακίου", "Mandraki, Nisyros", "Monastery", "monastery", ["22420-31253"], None, None, None, ["Μανδράκι, Νίσυρος 85303"]),
])

add_group("ep-leros", "gr-ep-leros", SOURCES["ep-leros"], [
    ("leros-annunciation-metropolitan", "Metropolitan Church of the Annunciation of the Theotokos on Leros", "Ἱερός Μητροπολιτικός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου Λέρου", "Leros", "Metropolitan Church", "parish"),
    ("leros-marina", "Church of Saint Marina on Leros", "Ἱερός Ναός Ἁγίας Μαρίνης Λέρου", "Leros", "Parish Church", "parish"),
    ("leros-transfiguration", "Church of the Transfiguration of Christ the Savior on Leros", "Ἱερός Ναός Θείας Μεταμορφώσεως Σωτῆρος Χριστοῦ Λέρου", "Leros", "Parish Church", "parish"),
    ("leros-forty-martyrs", "Church of the Forty Martyrs on Leros", "Ἱερός Ναός Ἁγίων Τεσσαράκοντα Μαρτύρων Λέρου", "Leros", "Parish Church", "parish"),
    ("lakki-nicholas-cathedral", "Cathedral of Saint Nicholas in Lakki", "Καθεδρικός Ἱερός Ναός Ἁγίου Νικολάου Λακκίου", "Lakki, Leros", "Cathedral", "parish"),
    ("leros-irene-chrysovalantou", "Church of Venerable Irene Chrysovalantou on Leros", "Ἱερός Ναός Ὁσίας Εἰρήνης Χρυσοβαλάντου Λέρου", "Leros", "Parish Church", "parish"),
    ("leros-phanourios", "Church of Saint Phanourios on Leros", "Ἱερός Ναός Ἁγίου Φανουρίου Λέρου", "Leros", "Parish Church", "parish"),
    ("kalymnos-transfiguration-metropolitan", "Metropolitan Church of the Transfiguration of Christ the Savior on Kalymnos", "Ἱερός Μητροπολιτικός Ναός Θείας Μεταμορφώσεως Σωτῆρος Χριστοῦ Καλύμνου", "Kalymnos", "Metropolitan Church", "parish"),
    ("chora-kecharitomene-cathedral", "Cathedral of Panagia Kecharitomene in Chora", "Ἱερός Καθεδρικός Ναός Παναγίας Κεχαριτωμένης Χώρας", "Chora, Kalymnos", "Cathedral", "parish"),
    ("kalymnos-stephen", "Church of Saint Stephen on Kalymnos", "Ἱερός Ναός Ἁγίου Στεφάνου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-nicholas", "Church of Saint Nicholas on Kalymnos", "Ἱερός Ναός Ἁγίου Νικολάου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-life-giving-spring", "Church of the Life-giving Spring on Kalymnos", "Ἱερός Ναός Ζωοδόχου Πηγῆς Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-basil", "Church of Saint Basil on Kalymnos", "Ἱερός Ναός Ἁγίου Βασιλείου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-meeting", "Church of the Meeting of the Lord on Kalymnos", "Ἱερός Ναός Ὑπαπαντῆς τοῦ Κυρίου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-holy-trinity", "Church of the Holy Trinity on Kalymnos", "Ἱερός Ναός Ἁγίας Τριάδος Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-mamas", "Church of Saint Mamas on Kalymnos", "Ἱερός Ναός Ἁγίου Μάμαντος Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-annunciation", "Church of the Annunciation of the Theotokos on Kalymnos", "Ἱερός Ναός Εὐαγγελιστρίας Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-resurrection", "Church of the Resurrection on Kalymnos", "Ἱερός Ναός Ἀναστάσεως Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-john-theologian", "Church of Saint John the Theologian on Kalymnos", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-athanasius", "Church of Saint Athanasius on Kalymnos", "Ἱερός Ναός Ἁγίου Ἀθανασίου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-forerunner", "Church of Saint John the Forerunner on Kalymnos", "Ἱερός Ναός Τιμίου Προδρόμου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-charalambos", "Church of Saint Charalambos on Kalymnos", "Ἱερός Ναός Ἁγίου Χαραλάμπους Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-george", "Church of Saint George on Kalymnos", "Ἱερός Ναός Ἁγίου Γεωργίου Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("kalymnos-archangel-michael", "Church of the Archangel Michael on Kalymnos", "Ἱερός Ναός Ἀρχαγγέλου Μιχαήλ Καλύμνου", "Kalymnos", "Parish Church", "parish"),
    ("arginonta-dormition", "Church of the Dormition of the Theotokos in Arginonta", "Ἱερός Ναός Κοιμήσεως Θεοτόκου Ἀργινώντα", "Arginonta, Kalymnos", "Parish Church", "parish"),
    ("myrties-presentation", "Church of the Presentation of the Theotokos in Myrties", "Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Μυρτιῶν", "Myrties, Kalymnos", "Parish Church", "parish"),
    ("argos-george", "Church of Saint George in Argos", "Ἱερός Ναός Ἁγίου Γεωργίου Ἄργους", "Argos, Kalymnos", "Parish Church", "parish"),
    ("vothynoi-dormition", "Church of the Dormition of the Theotokos in Vothynoi", "Ἱερός Ναός Κοιμήσεως Θεοτόκου Βοθύνων", "Vothynoi, Kalymnos", "Parish Church", "parish"),
    ("vathy-theodore", "Church of Saint Theodore in Vathy", "Ἱερός Ναός Ἁγίου Θεοδώρου Βαθέος", "Vathy, Kalymnos", "Parish Church", "parish"),
    ("vathy-holy-trinity", "Church of the Holy Trinity in Vathy", "Ἱερός Ναός Ἁγίας Τριάδος Βαθέος", "Vathy, Kalymnos", "Parish Church", "parish"),
    ("telendos-life-giving-spring", "Church of the Life-giving Spring on Telendos", "Ἱερός Ναός Ζωοδόχου Πηγῆς νήσου Τελένδου", "Telendos", "Parish Church", "parish"),
    ("pserimos-dormition", "Church of the Dormition of the Theotokos on Pserimos", "Ἱερός Ναός Κοιμήσεως Θεοτόκου νήσου Ψερίμου", "Pserimos", "Parish Church", "parish"),
    ("flaska-paul", "Church of the Apostle Paul at Flaska", "Ἱερός Ναός Ἀποστόλου Παύλου Φλασκᾶ", "Flaska, Kalymnos", "Parish Church", "parish"),
    ("astypalaia-portaitissa-metropolitan", "Metropolitan Church of Panagia Portaitissa on Astypalaia", "Ἱερός Μητροπολιτικός Ναός Παναγίας Πορταϊτίσσης", "Chora, Astypalaia", "Metropolitan Church", "parish"),
    ("pera-gialos-nicholas", "Church of Saint Nicholas in Pera Gialos", "Ἱερός Ναός Ἁγίου Νικολάου Πέρα Γυαλοῦ", "Pera Gialos, Astypalaia", "Parish Church", "parish"),
    ("maltezana-demetrius", "Church of Saint Demetrius in Maltezana", "Ἱερός Ναός Ἁγίου Δημητρίου Μαλτεζάνας", "Maltezana, Astypalaia", "Parish Church", "parish"),
    ("astypalaia-megali-panagia", "Church of Megali Panagia on Astypalaia", "Ἱερός Ναός Μεγάλης Παναγιᾶς Ἀστυπαλαίας", "Astypalaia", "Parish Church", "parish"),
    ("chora-george", "Church of Saint George in Chora", "Ἱερός Ναός Ἁγίου Γεωργίου Χώρας", "Chora, Astypalaia", "Parish Church", "parish"),
    ("chora-castle-annunciation", "Church of Panagia of the Castle, the Annunciation of the Theotokos", "Ἱερός Ναός Παναγίας Κάστρου Εὐαγγελισμοῦ τῆς Θεοτόκου", "Chora, Astypalaia", "Parish Church", "parish"),
])

add_group("ep-leros", "gr-ep-leros-monastery", SOURCES["ep-leros"], [
    ("panagia-castle-leros", "Monastery of Panagia of the Castle on Leros", "Ἱερά Μονή Παναγίας Κάστρου Λέρου", "Leros", "Monastery", "monastery"),
    ("holy-angels-leros", "Monastery of the Holy Angels on Leros", "Ἱερά Μονή Ἁγίων Ἀγγέλων Λέρου", "Agios Petros, Leros", "Convent", "monastery"),
    ("panteleimon-kalymnos", "Monastery of Saint Panteleimon on Kalymnos", "Ἱερά Μονή Ἁγίου Παντελεήμονος Καλύμνου", "Kalymnos", "Monastery", "monastery"),
    ("annunciation-argos", "Monastery of the Annunciation in Argos", "Ἱερά Μονή Εὐαγγελιστρίας Ἄργους", "Argos, Kalymnos", "Convent", "monastery"),
    ("catherine-vothynoi", "Monastery of Saint Catherine in Vothynoi", "Ἱερά Μονή Ἁγίας Αἰκατερίνης Βοθύνων", "Vothynoi, Kalymnos", "Convent", "monastery"),
    ("all-saints-kalymnos", "Monastery of All Saints on Kalymnos", "Ἱερά Μονή Ἁγίων Πάντων Καλύμνου", "Kalymnos", "Convent", "monastery"),
    ("ascension-kalymnos", "Monastery of the Ascension of the Lord on Kalymnos", "Ἱερά Μονή Ἀναλήψεως Κυρίου Καλύμνου", "Kalymnos", "Convent", "monastery", ["22430-29479"]),
    ("panagia-eleousa-rotsos", "Monastery of Panagia Eleousa at Rotsos", "Ἱερά Μονή Παναγίας Ἐλεούσης Ρότσου", "Rotsos, Kalymnos", "Convent", "monastery"),
])

add_group("ep-leros", "gr-ep-leros-hesychasterion", SOURCES["ep-leros"], [
    ("matrona-kioura", "Hesychasterion of Saint Matrona at Kioura", "Ἱερόν Ἡσυχαστήριον Ἁγίας Ματρώνης Κιουρᾶς", "Kioura, Leros", "Hesychasterion in Formation", "monastery"),
    ("precious-cross-kantouni", "Hesychasterion of the Precious Cross at Kantouni", "Ἱερόν Ἡσυχαστήριον Τιμίου Σταυροῦ Καντουνίου", "Kantouni, Kalymnos", "Hesychasterion", "monastery"),
    ("cyprian-vothynoi", "Hesychasterion of Saint Cyprian in Vothynoi", "Ἱερόν Ἡσυχαστήριον Ἁγίου Κυπριανοῦ Βοθύνων", "Vothynoi, Kalymnos", "Hesychasterion", "monastery"),
    ("holy-trinity-chali", "Hesychasterion of the Holy Trinity at Chali", "Ἱερόν Ἡσυχαστήριον Ἁγίας Τριάδος Χαλῆς", "Chali, Kalymnos", "Hesychasterion", "monastery"),
    ("macrina-vathy", "Hesychasterion of Saint Macrina in Vathy", "Ἱερόν Ἡσυχαστήριον Ἁγίας Μακρίνης Βαθέος Καλύμνου", "Vathy, Kalymnos", "Hesychasterion", "monastery"),
    ("panagia-flevariotissa", "Monastery of Panagia Flevariotissa on Astypalaia", "Ἱερά Μονή Παναγίας Φλεβαριωτίσσης", "Astypalaia", "Monastery", "monastery"),
    ("precious-cross-nera", "Hesychasterion of the Precious Cross on Nera", "Ἱερόν Ἡσυχαστήριον Τιμίου Σταυροῦ βραχονησίδος Νερά", "Nera", "Hesychasterion", "monastery"),
    ("nicholas-plati", "Hesychasterion of Saint Nicholas on Plati", "Ἱερόν Ἡσυχαστήριον Ἁγίου Νικολάου βραχονησίδος Πλάτη", "Plati", "Hesychasterion", "monastery"),
    ("nicholas-kalolimnos", "Hesychasterion of Saint Nicholas on Kalolimnos", "Ἱερόν Ἡσυχαστήριον Ἁγίου Νικολάου βραχονησίδος Καλόλιμνος", "Kalolimnos", "Hesychasterion", "monastery"),
])

add_group("gr-ep-leros-monastery-catherine-vothynoi", "gr-ep-leros-metochion", SOURCES["ep-leros"], [
    ("andrew", "Metochion of Saint Andrew", "Μετόχιον Ἁγίου Ἀνδρέα", "Kalymnos", "Metochion", "monastery"),
])
add_group("gr-ep-leros-monastery-all-saints-kalymnos", "gr-ep-leros-metochion", SOURCES["ep-leros"], [
    ("nectarius", "Metochion of Saint Nectarius", "Μετόχιον Ἁγίου Νεκταρίου", "Kalymnos", "Metochion", "monastery", ["22430-28424"]),
])
add_group("gr-ep-leros-monastery-annunciation-argos", "gr-ep-leros-metochion", SOURCES["ep-leros"], [
    ("paraskevi", "Metochion of Saint Paraskevi", "Μετόχιον Ἁγίας Παρασκευῆς", "Kalymnos", "Metochion", "monastery"),
])
add_group("gr-ep-leros-monastery-panagia-eleousa-rotsos", "gr-ep-leros-metochion", SOURCES["ep-leros"], [
    ("holy-trinity-chali", "Metochion of the Holy Trinity at Chali", "Μετόχιον Ἁγίας Τριάδος Χαλῆς", "Chali, Kalymnos", "Metochion", "monastery"),
    ("macrina-kampi", "Metochion of Saint Macrina at Kampi", "Μετόχιον Ἁγίας Μακρίνης Καμπί", "Kampi, Kalymnos", "Metochion", "monastery"),
])
add_group("gr-ep-leros-kalymnos-nicholas", "gr-ep-leros-metochion", SOURCES["ep-leros"], [
    ("george-pezoules", "Metochion of Saint George at Pezoules", "Μετόχιον Ἁγίου Γεωργίου Πεζούλες", "Pezoules, Kalymnos", "Metochion", "monastery"),
])

add_group("ep-karpathos", "gr-ep-karpathos", SOURCES["ep-karpathos"], [
    ("aperi-dormition-metropolitan", "Metropolitan Church of the Dormition of the Theotokos in Aperi", "Μητροπολιτικός Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ἀπερίου", "Aperi, Karpathos", "Metropolitan Church", "parish"),
    ("aperi-transfiguration", "Church of the Transfiguration of the Savior in Aperi", "Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος Ἀπερίου", "Aperi, Karpathos", "Parish Church", "parish"),
    ("aperi-john-forerunner", "Church of Saint John the Forerunner in Aperi", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Προδρόμου Ἀπερίου", "Aperi, Karpathos", "Parish Church", "parish"),
    ("karpathos-annunciation", "Church of the Annunciation of the Theotokos in Karpathos", "Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου Καρπάθου", "Karpathos", "Parish Church", "parish"),
    ("karpathos-apostles", "Church of the Holy Apostles in Karpathos", "Ἱερός Ναός Ἁγίων Ἀποστόλων Καρπάθου", "Karpathos", "Parish Church", "parish"),
    ("arkasa-meeting", "Church of the Meeting of the Savior in Arkasa", "Ἱερός Ναός Ὑπαπαντῆς τοῦ Σωτῆρος Ἀρκάσας", "Arkasa, Karpathos", "Parish Church", "parish"),
    ("volada-nativity", "Church of the Nativity of the Theotokos in Volada", "Ἱερός Ναός Γενεσίου τῆς Θεοτόκου Βωλάδας", "Volada, Karpathos", "Parish Church", "parish"),
    ("diafani-life-giving-spring", "Church of the Life-giving Spring in Diafani", "Ἱερός Ναός Ζωοδόχου Πηγῆς Διαφανίου", "Diafani, Karpathos", "Parish Church", "parish"),
    ("menetes-dormition", "Church of the Dormition of the Theotokos in Menetes", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Μενετῶν", "Menetes, Karpathos", "Parish Church", "parish"),
    ("mesochori-nativity", "Church of the Nativity of the Theotokos in Mesochori", "Ἱερός Ναός Γενεσίου τῆς Θεοτόκου Μεσοχωρίου", "Mesochori, Karpathos", "Parish Church", "parish"),
    ("othos-transfiguration", "Church of the Transfiguration of the Savior in Othos", "Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος Ὄθους", "Othos, Karpathos", "Parish Church", "parish"),
    ("olympos-dormition", "Church of the Dormition of the Theotokos in Olympos", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ὀλύμπου", "Olympos, Karpathos", "Parish Church", "parish"),
    ("pyles-dormition", "Church of the Dormition of the Theotokos in Pyles", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Πυλῶν", "Pyles, Karpathos", "Parish Church", "parish"),
    ("spoa-george", "Church of Saint George in Spoa", "Ἱερός Ναός Ἁγίου Γεωργίου Σπόων", "Spoa, Karpathos", "Parish Church", "parish"),
    ("kasos-spyridon", "Church of Saint Spyridon on Kasos", "Ἱερός Ναός Ἁγίου Σπυρίδωνος Κάσου", "Kasos", "Parish Church", "parish"),
    ("kasos-demetrius", "Church of Saint Demetrius on Kasos", "Ἱερός Ναός Ἁγίου Δημητρίου Κάσου", "Kasos", "Parish Church", "parish"),
    ("kasos-marina", "Church of Saint Marina on Kasos", "Ἱερός Ναός Ἁγίας Μαρίνης Κάσου", "Kasos", "Parish Church", "parish"),
    ("kasos-precious-cross", "Church of the Precious Cross on Kasos", "Ἱερός Ναός Τιμίου Σταυροῦ Κάσου", "Kasos", "Parish Church", "parish"),
    ("kasos-dormition", "Church of the Dormition of the Theotokos on Kasos", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Κάσου", "Kasos", "Parish Church", "parish"),
    ("kasos-holy-trinity", "Church of the Holy Trinity on Kasos", "Ἱερός Ναός Ἁγίας Τριάδος Κάσου", "Kasos", "Parish Church", "parish"),
])

add_group("ep-karpathos", "gr-ep-karpathos-monastery", SOURCES["ep-karpathos"], [
    ("george-vasson", "Patriarchal and Stavropegic Monastery of Saint George at Vasson", "Πατριαρχική καί Σταυροπηγιακή Μονή Ἁγίου Γεωργίου Βασσῶν", "Karpathos", "Patriarchal and Stavropegic Monastery", "monastery"),
    ("george-chadion-kasos", "Monastery of Saint George at Chadion on Kasos", "Ἱερά Μονή Ἁγίου Γεωργίου Χαδιῶν Κάσου", "Kasos", "Monastery", "monastery"),
    ("mamas-kasos", "Monastery of Saint Mamas on Kasos", "Ἱερά Μονή Ἁγίου Μάμαντος Κάσου", "Kasos", "Monastery", "monastery"),
    ("panagia-myrtonos-aperi", "Hesychasterion of Panagia Myrtonos in Aperi", "Ἡσυχαστήριον Παναγίας Μυρτῶνος Ἀπερείου Καρπάθου", "Aperi, Karpathos", "Hesychasterion", "monastery"),
])

add_group("ep-karpathos", "gr-ep-karpathos-shrine", SOURCES["ep-karpathos"], [
    ("nectarius", "Shrine of Saint Nectarius on Karpathos", "Ἱερόν Προσκύνημα Ἁγίου Νεκταρίου Καρπάθου", "Karpathos", "Shrine", "parish"),
    ("kyriaki", "Shrine of Saint Kyriaki on Karpathos", "Ἱερόν Προσκύνημα Ἁγίας Κυριακῆς Καρπάθου", "Karpathos", "Shrine", "parish"),
    ("panagia-larniotissa", "Shrine of Panagia Larniotissa on Karpathos", "Ἱερόν Προσκύνημα Παναγίας Λαρνιωτίσσης Καρπάθου", "Karpathos", "Shrine", "parish"),
    ("john-vrykountos", "Shrine of Saint John at Vrykountos", "Ἱερόν Προσκύνημα Ἁγίου Ἰωάννου Βρυκοῦντος", "Vrykountos, Karpathos", "Shrine", "parish"),
])

add_group("ep-syme", "gr-ep-syme", SOURCES["ep-syme"], [
    ("syme-john-forerunner-metropolitan", "Metropolitan Church of Saint John the Forerunner on Syme", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Προδρόμου Σύμης", "Syme", "Metropolitan Church", "parish"),
    ("syme-megali-panagia-castle", "Church of Megali Panagia of the Castle on Syme", "Ἱερός Ναός Μεγάλης Παναγίας Κάστρου Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-demetrius", "Church of Saint Demetrius on Syme", "Ἱερός Ναός Ἁγίου Δημητρίου Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-precious-cross", "Church of the Precious Cross on Syme", "Ἱερός Ναός Τιμίου Σταυροῦ Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-kecharitomene", "Church of Panagia Kecharitomene on Syme", "Ἱερός Ναός Κεχαριτωμένης Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-athanasius", "Church of Saint Athanasius on Syme", "Ἱερός Ναός Ἁγίου Ἀθανασίου Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-george-upper-chora", "Church of Saint George in Upper Chora on Syme", "Ἱερός Ναός Ἁγίου Γεωργίου Ἄνω Χώρας Σύμης", "Ano Chora, Syme", "Parish Church", "parish"),
    ("syme-panteleimon", "Church of Saint Panteleimon on Syme", "Ἱερός Ναός Ἁγίου Παντελεήμονος Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-nicholas", "Church of Saint Nicholas on Syme", "Ἱερός Ναός Ἁγίου Νικολάου Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-eleftherius", "Church of Saint Eleftherius on Syme", "Ἱερός Ναός Ἁγίου Ἐλευθερίου Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-holy-trinity", "Church of the Holy Trinity on Syme", "Ἱερός Ναός Ἁγίας Τριάδος Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-annunciation", "Church of the Annunciation of the Theotokos on Syme", "Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-presentation-eleimonitria", "Church of the Presentation of the Theotokos Eleimonitria on Syme", "Ἱερός Ναός Εἰσοδίων Θεοτόκου Ἐλεημονητρίας Σύμης", "Syme", "Parish Church", "parish"),
    ("syme-george-pedio", "Church of Saint George at Pedio on Syme", "Ἱερός Ναός Ἁγίου Γεωργίου Πεδίου Σύμης", "Pedio, Syme", "Parish Church", "parish"),
    ("tilos-megalo-chorio-archangel", "Metropolitan Church of the Archangel in Megalo Chorio", "Ἱερός Ναός Ταξιάρχου Μεγάλου Χωριοῦ Τήλου", "Megalo Chorio, Tilos", "Metropolitan Church", "parish"),
    ("tilos-livadia-nicholas", "Church of Saint Nicholas in Livadia", "Ἱερός Ναός Ἁγίου Νικολάου Λιβαδίων Τήλου", "Livadia, Tilos", "Parish Church", "parish"),
    ("chalki-nicholas", "Church of Saint Nicholas on Chalki", "Ἱερός Ναός Ἁγίου Νικολάου Χάλκης", "Chalki", "Parish Church", "parish"),
    ("chalki-palaio-chorio-dormition", "Church of the Dormition of the Theotokos in Palaio Chorio", "Ἱερός Ναός Κοιμήσεως Θεοτόκου Παλαιοῦ Χωριοῦ Χάλκης", "Palaio Chorio, Chalki", "Parish Church", "parish"),
    ("megisti-constantine-helen", "Church of Saints Constantine and Helen on Megisti", "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης Μεγίστης", "Megisti", "Parish Church", "parish"),
    ("megisti-george-pigadi", "Church of Saint George at Pigadi on Megisti", "Ἱερός Ναός Ἁγίου Γεωργίου Πηγαδιοῦ Μεγίστης", "Pigadi, Megisti", "Parish Church", "parish"),
])

add_group("ep-syme", "gr-ep-syme-monastery", SOURCES["ep-syme"], [
    ("archangel-michael-roukouniotis", "Patriarchal and Stavropegic Monastery of the Archangel Michael Roukouniotis", "Ἱερά Πατριαρχική καί Σταυροπηγιακή Μονή Ταξιάρχου Μιχαήλ τοῦ Ρουκουνιώτου Σύμης", "Syme", "Patriarchal and Stavropegic Monastery", "monastery", ["22460 71233"]),
    ("archangel-michael-panormitis", "Monastery of the Archangel Michael Panormitis", "Ἱερά Μονή Ταξιάρχου Μιχαήλ τοῦ Πανορμίτου Σύμης", "Panormitis, Syme", "Monastery", "monastery", ["22460 71581"], ["impanormitou@gmail.com"], "https://www.panormitisymis.gr/"),
    ("panteleimon-tilos", "Monastery of Saint Panteleimon on Tilos", "Ἱερά Μονή Ἁγίου Παντελεήμονος Τήλου", "Tilos", "Monastery", "monastery", ["22420 31676"]),
    ("john-forerunner-chalki", "Monastery of Saint John the Forerunner on Chalki", "Ἱερά Μονή Ἁγίου Ἰωάννου Προδρόμου Χάλκης", "Chalki", "Monastery", "monastery"),
    ("george-vouno-megisti", "Monastery of Saint George of the Mountain on Megisti", "Ἱερά Μονή Ἁγίου Γεωργίου Βουνοῦ Μεγίστης", "Megisti", "Monastery", "monastery"),
    ("prophet-elias-megisti", "Monastery of the Prophet Elias on Megisti", "Ἱερά Μονή Προφήτου Ἠλιού Μεγίστης", "Megisti", "Monastery", "monastery"),
])

add_group("ep-patmos", "gr-ep-patmos", SOURCES["ep-patmos"], [
    ("chora-megali-panagia-cathedral", "Cathedral of Megali Panagia in Chora", "Ἱερός Ναός Μεγάλης Παναγίας Χώρας Πάτμου", "Chora, Patmos", "Cathedral", "parish"),
    ("chora-panagia-cemetery", "Church of Panagia at the Chora Cemetery", "Ἱερός Ναός Παναγίας Κοιμητηρίων Χώρας Πάτμου", "Chora, Patmos", "Cemetery Church", "parish"),
    ("chora-meeting", "Church of the Meeting of the Lord in Chora", "Ἱερός Ναός Ὑπαπαντῆς τοῦ Κυρίου Χώρας Πάτμου", "Chora, Patmos", "Parish Church", "parish"),
    ("skala-john-forerunner", "Church of Saint John the Forerunner in Skala", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Προδρόμου Σκάλας Πάτμου", "Skala, Patmos", "Parish Church", "parish"),
    ("skala-nicholas", "Church of Saint Nicholas in Skala", "Ἱερός Ναός Ἁγίου Νικολάου Σκάλας Πάτμου", "Skala, Patmos", "Parish Church", "parish"),
    ("netia-thomas", "Church of the Apostle Thomas in Netia", "Ἱερός Ναός Ἀποστόλου Θωμᾶ Νετιᾶς Πάτμου", "Netia, Patmos", "Parish Church", "parish"),
    ("kampos-annunciation", "Church of the Annunciation of the Theotokos in Kampos", "Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου Κάμπου Πάτμου", "Kampos, Patmos", "Parish Church", "parish"),
    ("lipsoi-john-theologian", "Church of Saint John the Theologian on Lipsoi", "Ἱερός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Λειψῶν", "Lipsoi", "Parish Church", "parish"),
    ("agathonisi-george", "Church of Saint George on Agathonisi", "Ἱερός Ναός Ἁγίου Γεωργίου Ἀγαθονησίου", "Agathonisi", "Parish Church", "parish"),
    ("arkioi-transfiguration", "Church of the Transfiguration of the Savior on Arkioi", "Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος Ἀρκιῶν", "Arkioi", "Parish Church", "parish"),
])

add_group("ep-patmos", "gr-ep-patmos-monastery", SOURCES["ep-patmos"], [
    ("john-theologian", "Royal, Patriarchal and Stavropegic Monastery of Saint John the Theologian and Evangelist", "Ἱερά Βασιλική Πατριαρχική Σταυροπηγιακή καί Κοινοβιακή Μονή Ἁγίου Ἰωάννου τοῦ Θεολόγου καί Εὐαγγελιστοῦ", "Chora, Patmos", "Royal, Patriarchal and Stavropegic Monastery", "monastery", ["22470-20800"], ["grammateia@patmosmonastery.gr"], "https://www.patmosmonastery.gr/", None, ["Τ.Θ. 25, Τ.Κ. 855 00 Πάτμος"]),
    ("holy-of-holies", "Monastery of the Holy of Holies", "Ἱερά Μονή Ἅγια τῶν Ἁγίων", "Patmos", "Convent", "monastery", ["22470-31030"]),
    ("life-giving-spring", "Monastery of the Life-giving Spring", "Ἱερά Μονή Ζωοδόχου Πηγῆς", "Patmos", "Convent", "monastery", ["22470-31256", "22470-32056"]),
    ("annunciation-mother-beloved", "Hesychasterion of the Annunciation, Mother of the Beloved", "Ἱερόν Γυναικεῖον Ἡσυχαστήριον Εὐαγγελισμός Μητρός Ἠγαπημένου", "Patmos", "Hesychasterion", "monastery", ["22470-31276", "22470-31336"]),
])

add_group("gr-ep-patmos-monastery-life-giving-spring", "gr-ep-patmos-dependency", SOURCES["ep-patmos"], [
    ("dormition-livadi-kalogeron", "Hesychasterion of the Dormition of the Theotokos at Livadi ton Kalogeron", "Ἱερόν Ἡσυχαστήριον Κοιμήσεως τῆς Θεοτόκου Λειβαδίου τῶν Καλογήρων", "Livadi ton Kalogeron, Patmos", "Hesychasterion", "monastery"),
])

add_group("gr-ep-patmos-monastery-annunciation-mother-beloved", "gr-ep-patmos-dependency", SOURCES["ep-patmos"], [
    ("christ-argyra", "Kathisma of Christ at Argyra", "Ἱερόν Κάθισμα τοῦ Χριστοῦ τῆς Ἀργυρῆς", "Argyra, Patmos", "Kathisma", "monastery"),
    ("joseph-betrothed-kouvari", "Dependency of Saint Joseph the Betrothed at Kouvari", "Ἐξάρτημα Ἁγίου Ἰωσήφ τοῦ Μνήστορος ἐν Κουβαρίῳ", "Kouvari, Patmos", "Monastery Dependency", "monastery"),
])

add_group("gr-ep-patmos-monastery-john-theologian", "gr-ep-patmos-shrine", SOURCES["ep-patmos"], [
    ("cave-apocalypse", "Sacred Cave of the Apocalypse", "Ἱερά Ἀποκάλυψις", "Patmos", "Shrine", "parish", ["22470-31234"]),
])

add_group("gr-ep-patmos-monastery-john-theologian", "gr-ep-patmos-hermitage", SOURCES["ep-patmos"], [
    ("unmercenaries-kipoi", "Hermitage of the Holy Unmercenaries at Kipoi", "Ἱερόν Ἡσυχαστήριον Ἁγίων Ἀναργύρων Κήπων", "Kipoi, Patmos", "Hermitage", "monastery"),
    ("dormition-lipsoi-upper", "Hermitage of the Dormition of the Theotokos on Upper Lipsoi", "Ἱερόν Ἡσυχαστήριον Κοιμήσεως τῆς Θεοτόκου Λειψῶν ἄνω", "Lipsoi", "Hermitage", "monastery"),
    ("paraskevi-kavos", "Hermitage of Saint Paraskevi at Kavos", "Ἱερόν Ἡσυχαστήριον Ἁγίας Παρασκευῆς Κάβου", "Kavos, Patmos", "Hermitage", "monastery"),
    ("panagia-koumana", "Hermitage of Panagia Koumana", "Ἱερόν Ἡσυχαστήριον Παναγίας τῆς Κουμάνας", "Patmos", "Hermitage", "monastery"),
    ("all-saints-apollo", "Hermitage of All Saints at Apollo", "Ἱερόν Ἡσυχαστήριον Ἁγίων Πάντων Ἀπολλώ", "Apollo, Patmos", "Hermitage", "monastery"),
    ("panagia-pantanassa-arkioi", "Hermitage of Panagia Pantanassa on Arkioi", "Ἱερόν Ἡσυχαστήριον Παναγίας Παντανάσσης Ἀρκιῶν", "Arkioi", "Hermitage", "monastery"),
    ("nectarius-loukakia", "Hermitage of Saint Nectarius at Loukakia", "Ἱερόν Ἡσυχαστήριον Ἁγίου Νεκταρίου Λουκακίων", "Loukakia, Patmos", "Hermitage", "monastery", ["22470-32833"]),
    ("irene-skala", "Hermitage of Saint Irene in Skala", "Ἱερόν Ἡσυχαστήριον Ἁγίας Εἰρήνης Σκάλας", "Skala, Patmos", "Hermitage", "monastery"),
])

add_group("gr-ep-patmos-monastery-john-theologian", "gr-ep-patmos-kathisma", SOURCES["ep-patmos"], [
    ("bodiless-powers", "Kathisma of the Holy Bodiless Powers", "Ἱερόν Κάθισμα Ἀσωμάτων", "Patmos", "Kathisma", "monastery"),
    ("panteleimon-chiliomodi", "Kathisma of Saint Panteleimon at Chiliomodi", "Ἱερόν Κάθισμα Ἁγίου Παντελεήμονος Χιλιομοδίου", "Chiliomodi, Patmos", "Kathisma", "monastery"),
    ("christodoulos-alykes", "Kathisma of Venerable Christodoulos at Alykes", "Ἱερόν Κάθισμα Ὁσίου Χριστοδούλου Ἁλυκῶν", "Alykes, Patmos", "Kathisma", "monastery"),
    ("panagia-harou-lipsoi", "Kathisma of Panagia tou Harou on Lipsoi", "Ἱερόν Κάθισμα Παναγίας τοῦ Χάρου Λειψῶν", "Lipsoi", "Kathisma", "monastery"),
    ("george-avlaki", "Kathisma of Saint George at Avlaki", "Ἱερόν Κάθισμα Ἁγίου Γεωργίου τοῦ Αὐλακιοῦ", "Avlaki, Patmos", "Kathisma", "monastery"),
    ("panagia-mandalaki", "Kathisma of Panagia tou Mandalaki", "Ἱερόν Κάθισμα Παναγίας τοῦ Μανδαλάκη", "Patmos", "Kathisma", "monastery"),
    ("panagia-kykkou", "Kathisma of Panagia tou Kykkou", "Ἱερόν Κάθισμα Παναγίας τοῦ Κύκκου", "Patmos", "Kathisma", "monastery"),
    ("panagia-grava", "Kathisma of Panagia tou Grava", "Ἱερόν Κάθισμα Παναγίας τοῦ Γραβᾶ", "Patmos", "Kathisma", "monastery"),
    ("prophet-elias", "Kathisma of the Prophet Elias", "Ἱερόν Κάθισμα Προφήτου Ἠλιού", "Patmos", "Kathisma", "monastery"),
    ("dormition-lipsoi-lower", "Kathisma of the Dormition of the Theotokos on Lower Lipsoi", "Ἱερόν Κάθισμα Κοιμήσεως τῆς Θεοτόκου Λειψῶν κάτω", "Lipsoi", "Kathisma", "monastery"),
    ("transfiguration-axion-estin-kalamoti", "Kathisma of the Transfiguration and Axion Estin at Kalamoti", "Ἱερόν Κάθισμα Μεταμορφώσεως καί Ἄξιον Ἐστίν Καλαμωτῆς", "Kalamoti, Patmos", "Kathisma", "monastery"),
])

add_group("gr-ep-patmos-monastery-john-theologian", "gr-ep-patmos-monastic-church", SOURCES["ep-patmos"], [
    ("panagia-diasozousa-chora", "Monastic Church of Panagia Diasozousa in Chora", "Μοναστηριακός Ναός Παναγίας τῆς Διασώζουσας Χώρας", "Chora, Patmos", "Monastery Church", "parish"),
    ("phokas-skala", "Monastic Church of Saint Phokas in Skala", "Μοναστηριακός Ναός Ἁγίου Φωκᾶ Σκάλας", "Skala, Patmos", "Monastery Church", "parish"),
    ("basil-chora", "Monastic Church of Saint Basil in Chora", "Μοναστηριακός Ναός Ἁγίου Βασιλείου Χώρας", "Chora, Patmos", "Monastery Church", "parish"),
    ("george-aporthianoi-chora", "Monastic Church of Saint George ton Aporthianon in Chora", "Μοναστηριακός Ναός Ἁγίου Γεωργίου τῶν Ἀπορθιανῶν Χώρας", "Chora, Patmos", "Monastery Church", "parish"),
    ("john-theologian-skala-baptistery", "Baptistery of Saint John the Theologian in Skala", "Μοναστηριακός Ναός Ἁγίου Ἰωάννου τοῦ Θεολόγου Σκάλας Βαπτιστήριον", "Skala, Patmos", "Baptistery", "parish"),
    ("john-forerunner-chora", "Monastic Church of Saint John the Forerunner in Chora", "Μοναστηριακός Ναός Ἁγίου Ἰωάννου τοῦ Προδρόμου Χώρας", "Chora, Patmos", "Monastery Church", "parish"),
    ("george-loza-chora", "Monastic Church of Saint George of Loza in Chora", "Μοναστηριακός Ναός Ἁγίου Γεωργίου τῆς Λόζας Χώρας", "Chora, Patmos", "Monastery Church", "parish"),
    ("nicholas-koudounas", "Monastic Church of Saint Nicholas Koudounas", "Μοναστηριακός Ναός Ἁγίου Νικολάου τοῦ Κουδουνᾶ", "Patmos", "Monastery Church", "parish"),
    ("demetrius-chora", "Monastic Church of Saint Demetrius in Chora", "Μοναστηριακός Ναός Ἁγίου Δημητρίου Χώρας", "Chora, Patmos", "Monastery Church", "parish"),
])

add_group("gr-ep-patmos-monastery-john-theologian", "gr-ep-patmos-metochion", SOURCES["ep-patmos"], [
    ("john-theologian-lakki-leros", "Metochion of Saint John the Theologian in Lakki, Leros", "Ἱερόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Θεολόγου ἐν Λακκίῳ Λέρου", "Lakki, Leros", "Metochion", "monastery"),
    ("holy-apostles-kalymnos", "Metochion of the Holy Apostles on Kalymnos", "Ἱερόν Μετόχιον Ἁγίων Ἀποστόλων ἐν Καλύμνῳ", "Kalymnos", "Metochion", "monastery"),
    ("john-theologian-aptera-crete", "Metochion of Saint John the Theologian at Aptera, Crete", "Ἱερόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Θεολόγου ἐν Ἀπτέραις Κρήτης", "Aptera, Crete", "Metochion", "monastery"),
    ("transfiguration-photodotis-naxos", "Metochion of the Transfiguration of the Lord at Photodotis on Naxos", "Ἱερόν Μετόχιον τῆς τοῦ Κυρίου Μεταμορφώσεως Φωτοδότου ἐν Νάξῳ", "Naxos", "Metochion", "monastery"),
    ("john-theologian-chora-amorgos", "Metochion of Saint John the Theologian in Chora, Amorgos", "Ἱερόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Θεολόγου ἐν Χώρᾳ Ἀμοργοῦ", "Chora, Amorgos", "Metochion", "monastery"),
    ("john-theologian-heraion-samos", "Metochion of Saint John the Theologian at Heraion, Samos", "Ἱερόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Θεολόγου ἐν Ἡραίῳ Σάμου", "Heraion, Samos", "Metochion", "monastery"),
    ("john-theologian-thera", "Metochion of Saint John the Theologian on Thera", "Ἱερόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Θεολόγου ἐν Θήρᾳ", "Thera", "Metochion", "monastery"),
    ("john-theologian-siderianos-milos", "Metochion of Saint John the Theologian Siderianos on Milos", "Ἱερόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Θεολόγου Σιδεριανοῦ ἐν Μήλῳ", "Milos", "Metochion", "monastery"),
    ("george-penteli-athens", "Metochion of Saint George at Penteli, Athens", "Ἱερόν Μετόχιον Ἁγίου Γεωργίου ἐν Πεντέλῃ Ἀθηνῶν", "Penteli, Athens", "Metochion", "monastery"),
])


ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 311
EXPECTED_OWNER_COUNTS = {
    "ep-rhodes": 91,
    "ep-kos": 49,
    "ep-leros": 62,
    "ep-karpathos": 28,
    "ep-syme": 26,
    "ep-patmos": 55,
}
EXPECTED_KINDS = {"monastery": 105, "parish": 206}
EXPECTED_RANKS = {
    "Baptistery": 2,
    "Brotherhood Chapel": 1,
    "Cathedral": 5,
    "Cemetery Chapel": 1,
    "Cemetery Church": 1,
    "Chapel": 2,
    "Church": 1,
    "Convent": 12,
    "Country Chapel": 1,
    "Hermitage": 8,
    "Hesychasterion": 10,
    "Hesychasterion in Formation": 1,
    "Hospital Chapel": 2,
    "Institutional Chapel": 3,
    "Kathisma": 12,
    "Metochion": 15,
    "Metropolitan Church": 9,
    "Metropolitan Monastery": 1,
    "Monastery": 42,
    "Monastery Church": 8,
    "Monastery Dependency": 1,
    "Parish Church": 163,
    "Patriarchal and Stavropegic Monastery": 2,
    "Pilgrimage Church": 2,
    "Royal, Patriarchal and Stavropegic Monastery": 1,
    "Shrine": 5,
}
EXPECTED_CONTACT_BODIES = 57
EXPECTED_PHONE_BODIES = 57
EXPECTED_PHONE_VALUES = 60
EXPECTED_EMAIL_BODIES = 2
EXPECTED_EMAIL_VALUES = 2
EXPECTED_SITE_BODIES = 2
EXISTING_PARENTS = set(EXPECTED_OWNER_COUNTS)
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


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


def unicase(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value.casefold()).strip()


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in {
            "ec-patr.org", "www.imr.gr", "www.panormitisymis.gr",
            "www.patmosmonastery.gr"}:
        raise ValueError("%s carries a non-competent source: %s" %
                         (label, value))


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must carry one to three sources" % item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    contact_sources = list(item.get("contact_sources") or [])
    if contact_sources:
        if len(contact_sources) > 3:
            raise ValueError("%s has too many contact sources" % item.get("id"))
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError("%s contact source is outside identity sources" %
                                 item.get("id"))
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date" %
                             item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s body-owned site lacks provenance" %
                             item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Dodecanese candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Dodecanese candidate ledger check date drifted")
    summary = ledger.get("published_summary") or {}
    expected_summary = dict(EXPECTED_OWNER_COUNTS)
    expected_summary.update({
        "total": EXPECTED_TOTAL,
        "parish_kind_rows": EXPECTED_KINDS["parish"],
        "monastery_kind_rows": EXPECTED_KINDS["monastery"],
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
    })
    if summary != expected_summary:
        raise ValueError("Dodecanese candidate ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Dodecanese candidate ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Dodecanese ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Dodecanese ledger has an invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Dodecanese ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Dodecanese candidate ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
    seen = set(EXISTING_PARENTS)
    owners = {parent: parent for parent in EXISTING_PARENTS}
    signatures = {}
    rank_counts = Counter()
    kind_counts = Counter()
    owner_counts = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        parent = item.get("parent")
        if not row_id or row_id in ids or row_id in EXISTING_PARENTS:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if parent not in seen:
            raise ValueError("%s precedes or lacks parent %s" %
                             (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s carries the wrong country" % row_id)
        if item.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s carries an unsupported kind" % row_id)
        if item.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s carries an unsupported rank" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks an English name, Greek name, or seat" %
                             row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.match(email):
                raise ValueError("%s carries an invalid email" % row_id)
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        signature = (parent, unicase(item["local"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s after Greek normalization" %
                             (row_id, signatures[signature]))
        signatures[signature] = row_id
        owner = owners[parent]
        owners[row_id] = owner
        seen.add(row_id)
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[owner] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Dodecanese English name coverage drifted")
    expected_seats = {
        item["seat"] for item in result if item.get("seat")
    }
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Dodecanese English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Dodecanese parent totals drifted: %r" % owner_counts)
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Dodecanese kind totals drifted: %r" % kind_counts)
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Dodecanese rank totals drifted: %r" % rank_counts)
    coverage = (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site"))
            for item in result),
        sum(bool(item.get("phones")) for item in result),
        sum(len(item.get("phones") or []) for item in result),
        sum(bool(item.get("emails")) for item in result),
        sum(len(item.get("emails") or []) for item in result),
        sum(bool(item.get("site")) for item in result),
    )
    if coverage != (
            EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
            EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
            EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES):
        raise ValueError("Dodecanese contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    grouped = {parent: [] for parent in EXISTING_PARENTS}
    for item in result:
        grouped[owners[item["id"]]].append(item)
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
    payloads = build()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Dodecanese: %d exact current named bodies across %d official "
            "parents; %d bodies carry current institutional contact data" %
            (EXPECTED_TOTAL, len(EXPECTED_OWNER_COUNTS),
             EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Dodecanese: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
