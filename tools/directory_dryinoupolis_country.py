#!/usr/bin/env python3
"""Validate exact named Dryinoupolis bodies from first-party sources.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_dryinoupolis_country.py --check
    python tools/directory_dryinoupolis_country.py --dump
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
    ROOT / "tools" / "directory_candidates" / "dryinoupolis_country.json"
)
PARENT = "ep-dryinoupolis"
PARISH_PAGES = (
    "https://www.imdpk.gr/enories/enories-1",
    "https://www.imdpk.gr/enories/enories-1/page:2",
    "https://www.imdpk.gr/enories/enories-1/page:3",
    "https://www.imdpk.gr/enories/enories-1/page:4",
)
CHURCH_PAGE = (
    "https://www.imdpk.gr/enories/mitropolitikoi-ieroi-naoi-2"
)
DELVINAKI_PAGE = (
    "https://www.imdpk.gr/enories/naoi-kai-eksoklisia-sto-delvinaki-4"
)
KONITSA_PAGE = (
    "https://www.imdpk.gr/enories/naoi-kai-eksoklisia-stin-konitsa-5"
)
MONASTERY_PAGE = "https://www.imdpk.gr/enories/ieres-mones-3"
SAINT_KOSMAS_PAGE = (
    "https://www.imdpk.gr/enories/ieros-naos-agiou-kosma-aitolou-6"
)


PARISH_HEADINGS = [
  "Ἐνορία τοῦ Καθεδρικοῦ Μητροπολιτικοῦ Ἱεροῦ Ναοῦ Κοιμήσεως τῆς Θεοτόκου Δελβινακίου",
  "Ἐνορία τοῦ Μητροπολιτικοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου Ἄνω Κονίτσης",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Κωνσταντίνου καί Ἑλένης Κάτω Κονίτσης",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ἁγία Βαρβάρα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ἅγιος Κοσμᾶς",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Δημητρίου χωρίου Ἁγία Μαρίνα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ἁγία Παρασκευή",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ἀετομηλίτσα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἀθανασίου χωρίου Ἀετόπετρα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Ἀποστόλων χωρίου Ἀηδονοχώριον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Ἀμάραντος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἰωάννου τοῦ Θεολόγου χωρίου Ἄνω Παρακάλαμος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ἄνω Ραβένια",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ἀργυροχώριον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ἀρετή",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ἅρματα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ἀσημοχώριον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ὑπαπαντῆς τοῦ Χριστοῦ χωρίου Βασιλικόν",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Βήσσανη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Βούρμπιανη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Βραστοβά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Βροντισμενη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Ταξιαρχῶν χωρίου Γανναδιό",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Γεροπλάτανος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Γοργοποτάμου",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Δημητρίου χωρίου Δημόκορη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Δίστρατον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Γεννήσεως Θεοτόκου χωρίου Δολιανά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Δολόν",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Παρασκευῆς χωρίου Δροσοπηγή",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Δρυμάδες",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ἐλεύθερον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ἐξοχή",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ηλιορράχη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Καβάσιλα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Δημητρίου χωρίου Κακόλακκος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Καλλιθέα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Τριάδος χωρίου Καλόβρυση",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Καστάνιανη (πρώην Καστανέα)",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Τριάδος χωρίου Καστάνιανη (πρώην Καστανή)",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Γεννήσεως Θεοτόκου χωρίου Κάτω Λάβδανη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Εὐαγγελισμοῦ τῆς Θεοτόκου χωρίου Κάτω Μερόπης",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Παντελεήμονος χωρίου Κάτω Παρακάλαμος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Γεννήσεως τῆς Θεοτόκου χωρίου Κάτω Ραβένια",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Κεράσοβον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Κεφαλόβρυσον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Κλειδωνιά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Γεννήσεως τῆς Θεοτόκου χωρίου Κουκλιοί",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἀθανασίου χωρίου Κρυονέριον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Κτίσματα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Δημητρίου χωρίου Λάβδανη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Λαγκάδα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Λίμνη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Ταξιαρχῶν χωρίου Λυκόρραχη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Μάζιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Προφήτου Ηλιού χωρίου Μαυροβούνιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Εὐαγγελισμοῦ τῆς Θεοτόκου χωρίου Μαυρονόρος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Παρασκευῆς χωρίου Μαυρόπουλον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Μελισσόπετρα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Γεννήσεως τῆς Θεοτόκου χωρίου Μερόπη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Μόλιστα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Ἀποστόλων χωρίου Μολυβδοσκέπαστον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἀθανασίου χωρίου Μοναστήριον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Μαρίνης χωρίου Νικάνωρ",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ξηρόβαλτον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Οξυά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Παρασκευῆς χωρίου Ὀρεινόν",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Πάδες",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Παλαιόπυργος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Παρασκευῆς χωρίου Παλαιοσέλιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἐισοδίων τῆς Θεοτόκου χωρίου Περιστέριον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Πηγή",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Δημητρίου χωρίου Πλαγιά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Πληκάτιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Ποντικάτες",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Ταξιαρχῶν χωρίου Πουρνιά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Παρασκευῆς χωρίου Πυξαριά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Πύργος",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Πυρσόγιαννη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Πωγωνιανής",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Ρεπετίστη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἐισοδίων τῆς Θεοτόκου χωρίου Ρουψιά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἀθανασίου χωρίου Σιταριά",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Σταυροδρόμιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἐισοδίων τῆς Θεοτόκου χωρίου Σταυροσκιάδιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Στρατίνιστα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίων Ταξιαρχῶν χωρίου Τεριάχιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Τράπεζα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Κοιμήσεως Θεοτόκου χωρίου Φαράγγιον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Φούρκα",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Δημητρίου χωρίου Xαραυγή",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἀθανασίου χωρίου Χιονιᾶδες",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Ἀθανασίου χωρίου Χρυσόδουλη",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίας Τριάδος χωρίου Χρυσορράχης",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Νικολάου χωρίου Ψηλόκαστρον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Γεννήσεως τῆς Θεοτόκου χωρίου Ωραιόκαστρον",
  "Ἐνορία τοῦ Ἱεροῦ Ναοῦ Ἁγίου Γεωργίου χωρίου Ζάβροχον"
]

PARISH_SEATS = r"""
Delvinaki
Ano Konitsa
Kato Konitsa
Agia Varvara
Agios Kosmas
Agia Marina
Agia Paraskevi
Aetomilitsa
Aetopetra
Aidonochori
Amarantos
Ano Parakalamos
Ano Ravenia
Argyrochorio
Areti
Armata
Asimochorio
Vasiliko
Vissani
Vourmpiani
Vrastova
Vrontismeni
Gannadio
Geroplatanos
Gorgopotamos
Dimokori
Distrato
Doliana
Dolo
Drosopigi
Drymades
Elefthero
Exochi
Iliorrachi
Kavasila
Kakolakkos
Kallithea
Kalovrysi
Kastaniani
Kastaniani
Kato Lavdani
Kato Meropi
Kato Parakalamos
Kato Ravenia
Kerasovo
Kefalovryso
Kleidonia
Kouklioi
Kryoneri
Ktismata
Lavdani
Lagkada
Limni
Lykorrachi
Mazio
Mavrovouni
Mavronoros
Mavropoulo
Melissopetra
Meropi
Molista
Molyvdoskepasto
Monastiri
Nikanor
Xirovalto
Oxya
Oreino
Pades
Palaiopyrgos
Palaioselio
Peristeri
Pigi
Plagia
Plikati
Pontikates
Pournia
Pyxaria
Pyrgos
Pyrsogianni
Pogoniani
Repetisti
Roupsia
Sitaria
Stavrodromi
Stavroskiadi
Stratinista
Teriachi
Trapeza
Farangi
Fourka
Charavgi
Chioniades
Chrysodouli
Chrysorrachi
Psilokastro
Oraiokastro
Zavrocho
""".strip().splitlines()


DEDICATION_PATTERNS = (
    ("Κοιμησεως της Θεοτοκου", "Dormition of the Theotokos"),
    ("Κοιμησεως Θεοτοκου", "Dormition of the Theotokos"),
    ("Αγιου Νικολαου", "Saint Nicholas"),
    ("Αγιων Κωνσταντινου και Ελενης", "Saints Constantine and Helen"),
    ("Αγιου Δημητριου", "Saint Demetrius"),
    ("Αγιου Αθανασιου", "Saint Athanasius"),
    ("Αγιων Αποστολων", "Holy Apostles"),
    ("Αγιου Γεωργιου", "Saint George"),
    ("Αγιου Ιωαννου του Θεολογου", "Saint John the Theologian"),
    ("Υπαπαντης του Χριστου", "Meeting of Christ"),
    ("Αγιων Ταξιαρχων", "Holy Archangels"),
    ("Γεννησεως της Θεοτοκου", "Nativity of the Theotokos"),
    ("Γεννησεως Θεοτοκου", "Nativity of the Theotokos"),
    ("Αγιας Παρασκευης", "Saint Paraskevi"),
    ("Αγιας Τριαδος", "Holy Trinity"),
    ("Ευαγγελισμου της Θεοτοκου", "Annunciation of the Theotokos"),
    ("Αγιου Παντελεημονος", "Saint Panteleimon"),
    ("Προφητου Ηλιου", "Prophet Elijah"),
    ("Εισοδιων της Θεοτοκου", "Entry of the Theotokos"),
    ("Αγιας Μαρινης", "Saint Marina"),
)


ADDITIONAL_ROWS = [
    ("Ἱερός Ναός Ἁγίου Ἀθανασίου", "Saint Athanasius", "Delvinaki", "Church", DELVINAKI_PAGE),
    ("Ἱερός Ναός Ἁγίων Θεοδώρων", "Holy Theodore Martyrs", "Delvinaki", "Church", DELVINAKI_PAGE),
    ("Ἱερός Ναός Ἁγίων Ταξιαρχῶν", "Holy Archangels", "Delvinaki", "Church", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Δημητρίου", "Saint Demetrius", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Μηνᾶ", "Saint Menas", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Γεωργίου", "Saint George", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίων Κωνσταντίνου καί Ἑλένης", "Saints Constantine and Helen", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Γρηγορίου τοῦ Θεολόγου", "Saint Gregory the Theologian", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Προφήτου Ἠλία", "Prophet Elijah", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Ἰωάννου τοῦ Προδρόμου", "Saint John the Forerunner", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίας Παρασκευῆς", "Saint Paraskevi", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Μεταμορφώσεως τοῦ Σωτήρος", "Transfiguration of the Savior", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίας Ἀναστασίας", "Saint Anastasia", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Σπυρίδωνος", "Saint Spyridon", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Παναγίας τῆς Μπολιάνιτσας", "Panagia Bolianitsa", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Παντελεήμονος", "Saint Panteleimon", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίου Νεκταρίου", "Saint Nectarius", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίας Τριάδος", "Holy Trinity", "Delvinaki", "Country Chapel", DELVINAKI_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Παναγίας", "Dormition of the Theotokos", "Konitsa", "Country Chapel", KONITSA_PAGE),
    ("Ἱερόν Παρεκκλήσιον Ἁγίου Νεομάρτυρα Γεωργίου τοῦ ἐξ Ἰωαννίνων", "Saint George the New Martyr of Ioannina", "Konitsa", "Private Chapel", KONITSA_PAGE),
    ("Ἱερός Ναός Ἁγίων Ἀποστόλων", "Holy Apostles", "Konitsa", "Church", KONITSA_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίας Βαρβάρας", "Saint Barbara", "Konitsa", "Country Chapel", KONITSA_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Κόκκινης Παναγιᾶς", "Life-Giving Spring", "Konitsa", "Country Chapel", KONITSA_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίας Παρασκευής", "Saint Paraskevi", "Konitsa", "Country Chapel", KONITSA_PAGE),
    ("Ἱερόν Ἐξωκκλήσιον Ἁγίας Τριάδος", "Holy Trinity", "Konitsa", "Country Chapel", KONITSA_PAGE),
    ("Ἱερόν Παρεκκλήσιον Ἁγίου Ἀρσενίου τοῦ Καππαδόκου, Ὁσίου Παϊσίου τοῦ Ἁγιορείτου καί Ἀναλήψεως τοῦ Κυρίου", "Saints Arsenios of Cappadocia and Paisios the Athonite and the Ascension", "Konitsa", "Chapel", KONITSA_PAGE),
]


MONASTIC_ROWS = [
    {
        "local": "Ἱερά Μονή Παναγίας τῆς Μολυβδοσκεπάστου",
        "dedication": "Panagia Molyvdoskepastos",
        "seat": "Molyvdoskepasto",
        "phone": "26550-24175",
    },
    {
        "local": "Ἱερά Μονή Παναγίας Στομίου",
        "dedication": "Panagia Stomio",
        "seat": "Konitsa",
        "phone": "26550-23067",
    },
    {
        "local": "Ἱερά Μονή Εἰσοδίων τῆς Θεοτόκου Μολίστης",
        "dedication": "Entry of the Theotokos",
        "seat": "Molista",
        "phone": "26550-24175",
    },
    {
        "local": "Ἱερά Γυναικεία Κοινοβιακή Μονή Ὑψώσεως τοῦ Τιμίου Σταυροῦ",
        "dedication": "Exaltation of the Holy Cross",
        "seat": "Kallithea",
        "phone": "",
    },
]


def slug(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:96]


def unicase(value):
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value.casefold()).strip()


def dedication_from_heading(heading):
    normalized = unicase(heading)
    matches = []
    for greek, english in DEDICATION_PATTERNS:
        if unicase(greek) in normalized:
            matches.append(english)
    matches = list(dict.fromkeys(matches))
    if len(matches) != 1:
        raise ValueError("could not resolve parish dedication: %s" % heading)
    return matches[0]


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def build_rows():
    if len(PARISH_HEADINGS) != 97 or len(PARISH_SEATS) != 97:
        raise ValueError("Dryinoupolis parish source alignment drifted")
    rows = []
    index = 0
    for offset, (heading, seat) in enumerate(
            zip(PARISH_HEADINGS, PARISH_SEATS)):
        index += 1
        if offset == 0:
            rank = "Metropolitan Cathedral"
        elif offset == 1:
            rank = "Metropolitan Church"
        else:
            rank = "Parish Church"
        dedication = dedication_from_heading(heading)
        name = make_name(dedication, rank, seat)
        page = PARISH_PAGES[min(offset // 30, 3)]
        sources = [page]
        phone = ""
        if offset == 0:
            sources.append(CHURCH_PAGE)
            phone = "26570-22192"
        elif offset == 1:
            sources.append(CHURCH_PAGE)
            phone = "26550-22290"
        item = {
            "id": "gr-ep-dryinoupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": heading,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": sources,
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [CHURCH_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)
    for local, dedication, seat, rank, source in ADDITIONAL_ROWS:
        index += 1
        name = make_name(dedication, rank, seat)
        rows.append({
            "id": "gr-ep-dryinoupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": [source],
        })
    index += 1
    dedication = "Saint Kosmas the Aetolian"
    rank = "Pilgrimage Church"
    seat = "Konitsa"
    name = make_name(dedication, rank, seat)
    rows.append({
        "id": "gr-ep-dryinoupolis-%03d-%s" % (index, slug(name)),
        "parent": PARENT,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": "Προσκυνηματικός Ἱερός Ναός Ἁγίου Κοσμᾶ τοῦ Αἰτωλοῦ",
        "seat": seat,
        "country": "GR",
        "address": [seat],
        "phones": ["26550-22605"],
        "sources": [CHURCH_PAGE, SAINT_KOSMAS_PAGE],
        "contact_sources": [CHURCH_PAGE, SAINT_KOSMAS_PAGE],
        "contact_checked": CHECKED,
    })
    for record in MONASTIC_ROWS:
        index += 1
        rank = "Monastery"
        name = make_name(record["dedication"], rank, record["seat"])
        item = {
            "id": "gr-ep-dryinoupolis-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": record["local"],
            "seat": record["seat"],
            "country": "GR",
            "address": [record["seat"]],
            "sources": [MONASTERY_PAGE],
        }
        if record["phone"]:
            item["phones"] = [record["phone"]]
            item["contact_sources"] = [MONASTERY_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 128
EXPECTED_OWNER_COUNTS = {PARENT: 128}
EXPECTED_KINDS = {"monastery": 4, "parish": 124}
EXPECTED_RANKS = {
    "Chapel": 1,
    "Church": 4,
    "Country Chapel": 20,
    "Metropolitan Cathedral": 1,
    "Metropolitan Church": 1,
    "Monastery": 4,
    "Parish Church": 95,
    "Pilgrimage Church": 1,
    "Private Chapel": 1,
}
EXPECTED_CONTACT_BODIES = 6
EXPECTED_PHONE_BODIES = 6
EXPECTED_PHONE_VALUES = 6
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 128
EXISTING_PARENTS = {PARENT}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc != "www.imdpk.gr":
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


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
                raise ValueError(
                    "%s contact source is outside identity sources"
                    % item.get("id")
                )
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Dryinoupolis candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Dryinoupolis candidate ledger date drifted")
    expected_summary = {
        PARENT: 128,
        "total": 128,
        "parish_kind_rows": 124,
        "monastery_kind_rows": 4,
        "contact_bodies": 6,
        "phone_bodies": 6,
        "public_phone_values": 6,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 128,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Dryinoupolis ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Dryinoupolis ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Dryinoupolis ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Dryinoupolis ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Dryinoupolis ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Dryinoupolis ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
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
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s lacks parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s carries the wrong country" % row_id)
        if item.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s carries an unsupported kind" % row_id)
        if item.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s carries an unsupported rank" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError(
                "%s lacks an English name, Greek name, or seat" % row_id
            )
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
        signature = (parent, unicase(item["local"]), unicase(item["seat"]))
        if signature in signatures:
            raise ValueError(
                "%s duplicates %s after Greek normalization"
                % (row_id, signatures[signature])
            )
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d"
                         % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Dryinoupolis English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Dryinoupolis English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Dryinoupolis parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Dryinoupolis kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Dryinoupolis rank totals drifted: %r" %
                         dict(sorted(rank_counts.items())))
    coverage = (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site"))
            for item in result),
        sum(bool(item.get("phones")) for item in result),
        sum(len(item.get("phones") or []) for item in result),
        sum(bool(item.get("emails")) for item in result),
        sum(len(item.get("emails") or []) for item in result),
        sum(bool(item.get("site")) for item in result),
        sum(bool(item.get("address")) for item in result),
    )
    expected_coverage = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected_coverage:
        raise ValueError("Dryinoupolis contact coverage drifted: %r"
                         % (coverage,))
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
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
            "Dryinoupolis: %d exact named bodies; %d carry current "
            "institutional contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Dryinoupolis: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
