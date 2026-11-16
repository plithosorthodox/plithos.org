#!/usr/bin/env python3
"""Validate exact current Kerkyra worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_kerkyra_country.py --check
    python tools/directory_kerkyra_country.py --check-live
    python tools/directory_kerkyra_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import html
import json
from pathlib import Path
import re
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-kerkyra"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "kerkyra_country.json"
)
OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_noembrios.pdf"
)
NAV_PAGE = "https://imcorfu.gr/naoi-ieres-mones/"
OFFICES_PAGE = "https://imcorfu.gr/grafeia/"
CHURCH_API = "https://imcorfu.gr/wp-json/wp/v2/ieroi-naoi?per_page=100"
MONASTERY_API = "https://imcorfu.gr/wp-json/wp/v2/monastiria?per_page=100"
PILGRIMAGE_API = (
    "https://imcorfu.gr/wp-json/wp/v2/iera-proskynimata?per_page=100"
)

CATHEDRAL_DETAIL = (
    "https://imcorfu.gr/iera-proskynimata/"
    "ieros-mitropolitikos-naos-kerkyras/"
)
SAINT_JOHN_DETAIL = (
    "https://imcorfu.gr/ieroi-naoi/"
    "ieros-naos-tou-agiou-ioannou-prodromou-poleos-kerkyras/"
)
ALL_SAINTS_DETAIL = (
    "https://imcorfu.gr/ieroi-naoi/ieros-naos-agion-panton-poleos/"
)
KASSOPITRA_DETAIL = (
    "https://imcorfu.gr/ieroi-naoi/"
    "ieros-naos-panagias-kassopitras-kassiopi/"
)
SAINT_SPYRIDON_DETAIL = (
    "https://imcorfu.gr/iera-proskynimata/"
    "iero-proskynima-agiou-spyridona/"
)
VELLIANITON_DETAIL = (
    "https://imcorfu.gr/monastiria/"
    "panagia-vellianiton-sto-nisaki-gaios-paxon/"
)
ALL_SAINTS_SITE = "https://apantes.gr/"

# Legal region | English seat | legal Greek identity | English dedication.
# The sequence is the numbered sequence in the 2019 Church of Greece table.
PARISH_SOURCE = r'''
A|Corfu|Ὑ.Θ. Σπηλαιωτίσσης Ἁγίου Βλασίου καί Ἁγίας Θεοδώρας τῆς Αὐγούστης (Μητροπολιτικός)|Panagia Spilaiotissa, Saint Blaise, and Saint Theodora the Augusta
A|Corfu|Ἁγίου Ἀντωνίου|Saint Anthony
A|Corfu|Ὑ.Θ. Φανερωμένης τῶν Στερεωτῶν|Panagia Phaneromene of the Stereotai
A|Corfu|Ἁγίου Ἰωάννου τοῦ Προδρόμου|Saint John the Forerunner
A|Corfu|Ἁγίων Πάντων|All Saints
A|Corfu|Ἁγίου Βασιλείου|Saint Basil
A|Corfu|Ἁγίου Ἐλευθερίου καί Ὑ.Θ. Μανδρακιωτίσσης|Saint Eleftherius and Panagia Mandrakiotissa
A|Corfu|Ἁγίου Νικολάου Γερόντων|Saint Nicholas of the Elders
A|Corfu|Ἁγίας Παρασκευῆς|Saint Paraskevi
A|Corfu|Ἁγίας Σοφίας|Saint Sophia
A|Corfu|Ἁγίου Σπυρίδωνος Σαρόκου|Saint Spyridon at Saroko
A|Pagrateika, Corfu|Ἁγίου Ἀπολλοδώρου Περιοχῆς Παγκρατεί̈κων|Saint Apollodorus in Pagrateika
A|Garitsa, Corfu|Ἁγίας Τριάδος Γαρίτσας|Holy Trinity in Garitsa
A|Garitsa, Corfu|Ὑ.Θ. Βλαχερνῶν Γαρίτσας|Panagia Blachernae in Garitsa
A|Anemomylos, Corfu|Ἁγίων Τριῶν Μαρτύρων Ἀνεμομύλου|Three Holy Martyrs at Anemomylos
A|Kanoni|Ἀναλήψεως Κανονίου|the Ascension of the Lord
A|Mandouki|Ἁγίου Γεωργίου Μανδουκίου|Saint George at Mandouki
A|Mandouki|Ἁγίου Ἰωάννου Λάζου Μανδουκίου|Saint John Lazos at Mandouki
A|Koulines|Ἁγίων Κων/νου, Ἑλένης καί Ἁγίας Κερκύρας Κουλίνας|Saints Constantine and Helen and Saint Kerkyra at Koulines
A|Mamali|Ὑ.Θ. Κοιμήσεως Μαμάλων|the Dormition of the Theotokos at Mamali
A|Alepou|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
A|Gouvia|Ἁγίων Πάντων|All Saints
A|Evropouli|Παντοκράτορος|Christ Pantocrator
A|Kanali|Ἁγίου Σπυρίδωνος|Saint Spyridon
A|Kanali|Ἁγίου Νικολάου|Saint Nicholas
A|Kontokali|Ἁγίας Τριάδος|Holy Trinity
A|Kyra Chrysikou|Ἁγίου Σπυρίδωνος|Saint Spyridon
A|Potamos|Ἁγίου Βαρβάρου|Saint Barbarus
A|Potamos|Ὑ.Θ. Ἐλεούσης|Panagia Eleousa
A|Potamos|Ἁγίου Νικολάου Ἀλυκῶν|Saint Nicholas at Alykes
A|Temploni|Ὑ.Θ. Σπαρμιωτίσσης|Panagia Sparmiotissa
B|Agios Ioannis|Ἁγίου Ἰωάννου τοῦ Προδρόμου|Saint John the Forerunner
B|Afra|Ὑ.Θ. Λαμποβίτισσης|Panagia Lampovitissa
B|Vatos|Ἁγίου Νικολάου|Saint Nicholas
B|Giannades|Ἁγίου Νικολάου|Saint Nicholas
B|Kanakades|Ἁγίας Αἰκατερίνης|Saint Catherine
B|Karoumatika|Ἁγίας Τριάδος|Holy Trinity
B|Kompitsi|Ἁγίων Ἀποστόλων|Holy Apostles
B|Kokkini|Ἁγίων Κων/νου καί Ἑλένης|Saints Constantine and Helen
B|Marmaro|Ἁγίας Μαρίνας|Saint Marina
B|Pelekas|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
B|Sinarades|Ἁγίου Νικολάου|Saint Nicholas
B|Sinarades|Ὑ.Θ. Παντανάσσης|Panagia Pantanassa
C|Agioi Deka|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
C|Agios Prokopios|Ἁγίας Τριάδος|Holy Trinity
C|Varipatades|Ἁγίας Παρασκευῆς καί Ἁγίου Σπυρίδωνος|Saint Paraskevi and Saint Spyridon
C|Viros|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
C|Ano Garouna|Ὑ.Θ. Ἐλεούσης|Panagia Eleousa
C|Kato Garouna|Ἁγίου Νικολάου|Saint Nicholas
C|Gastouri|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
C|Kamara|Ὑ.Θ. Βλαχερνῶν|Panagia Blachernae
C|Kalafationes|Προφήτου Ἠλιού καί Ὑ.Θ. Ἐλεούσης|Prophet Elijah and Panagia Eleousa
C|Kastellanoi Meses|Ὑπαπαντῆς τοῦ Κυρίου|the Meeting of the Lord
C|Kynopiastes|Ὑ.Θ. Ἐλεούσης|Panagia Eleousa
C|Kouramades|Ἁγίου Ἰωάννου τοῦ Καλυβίτου|Saint John the Calybite
C|Benitses|Ἁγίου Νικολάου|Saint Nicholas
C|Stavros|Ὑ.Θ. Ἀγνάντων|Panagia Agnanton
C|Tsarou|Ὑ.Θ. Εὐαγγελιστρίας|the Annunciation of the Theotokos
C|Chrysiida|Ἁγίας Κυριακῆς|Saint Kyriaki
D|Agios Dimitrios|Ἁγίου Δημητρίου|Saint Demetrius
D|Agios Matthaios|Ἁγίου Ματθαίου|Saint Matthew
D|Agios Matthaios|Ἁγίας Παρασκευῆς|Saint Paraskevi
D|Vragkaniotika|Ἁγίας Παρασκευῆς|Saint Paraskevi
D|Vouniatades|Ἁγίου Ἰωάννου τοῦ Προδρόμου|Saint John the Forerunner
D|Episkopiana|Παμμεγίστων Ταξιαρχῶν|Holy Archangels
D|Linia|Ἁγίων Ἑπτά Μαρτύρων τῶν ἐν Κερκύρᾳ Μαρτυρησάντων|the Seven Martyrs of Kerkyra
D|Mesongi|Ἁγίου Νεκταρίου|Saint Nectarius
D|Moraitika|Κοιμήσεως τῆς Θεοτόκου|the Dormition of the Theotokos
D|Ano Pavliana|Ἁγίου Δημητρίου|Saint Demetrius
D|Kato Pavliana|Ἁγίας Τριάδος|Holy Trinity
D|Pentati|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
D|Spilaio|Γενεσίου Ὑ. Θεοτόκου|the Nativity of the Theotokos
D|Strongyli|Ἁγίων Πάντων|All Saints
D|Chlomotiana|Ὑ.Θ. Κασσιοπίας|Panagia Kassopitra
D|Chlomos|Ὑ.Θ. Ζωοδόχου Πηγῆς|the Life-Giving Spring
E|Agios Nikolaos|Ἁγίου Νικολάου|Saint Nicholas
E|Argyrades|Ἁγίου Ἰωάννου τοῦ Προδρόμου|Saint John the Forerunner
E|Vasilatika|Ἁγίου Σπυρίδωνος|Saint Spyridon
E|Korakades|Κοιμήσεως τῆς Ὑ. Θεοτόκου|the Dormition of the Theotokos
E|Kouspades|Ἁγίου Ἀθανασίου|Saint Athanasius
E|Marathias|Ὑ.Θ. Λαμποβίτισσης|Panagia Lampovitissa
E|Neochoraki|Ἁγίου Νικολάου|Saint Nicholas
E|Petriti|Ἁγίας Κερκύρας|Saint Kerkyra
E|Perivoli|Ἁγίου Θεοδώρου τοῦ Στρατηλάτου|Saint Theodore Stratelates
ST|Vitalades|Ἁγίων Ἀποστόλων|Holy Apostles
ST|Dragotina|Ταξιαρχῶν|Holy Archangels
ST|Kavos|Ἁγίου Προκοπίου|Saint Procopius
ST|Kritika|Ἁγίου Σπυρίδωνος|Saint Spyridon
ST|Anaplades, Lefkimmi|Ἁγίων Ἀναργύρων Ἀναπλάδων|Holy Unmercenaries at Anaplades
ST|Rigglades, Lefkimmi|Ἁγίου Ἀρσενίου Ριγγλάδων|Saint Arsenius at Rigglades
ST|Lefkimmi|Ἁγίων Θεοδώρων|Holy Theodores
ST|Lefkimmi|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
ST|Melikia, Lefkimmi|Ὑ.Θ. Λαμποβίτισσης Μελικίων|Panagia Lampovitissa at Melikia
ST|Potamio, Lefkimmi|Ὑ.Θ. Εὐαγγελιστρίας Ποταμίου|the Annunciation of the Theotokos at Potamio
ST|Neochori|Ἁγίας Τριάδος|Holy Trinity
ST|Palaiochori|Ἁγίου Γεωργίου|Saint George
ST|Spartera|Ἁγίας Μαρίνης|Saint Marina
Z|Agios Markos|Ὑ.Θ. Λαμποβίτισσης|Panagia Lampovitissa
Z|Ano Korakiana|Ἁγίου Ἀθανασίου|Saint Athanasius
Z|Ano Korakiana|Ἁγίου Γεωργίου|Saint George
Z|Ano Korakiana|Ἁγίου Νικολάου|Saint Nicholas
Z|Kato Korakiana|Ἁγίου Νικολάου|Saint Nicholas
Z|Kato Korakiana|Ὑ.Θ. Ζωοδόχου Πηγῆς|the Life-Giving Spring
Z|Gazatika, Kato Korakiana|Ἁγίου Δημητρίου Γαζατίκων|Saint Demetrius at Gazatika
Z|Zygos|Ἁγίας Ἀγάθης|Saint Agatha
Z|Spartylas|Ἁγίου Σπυρίδωνος|Saint Spyridon
Z|Sgourades|Ὑ.Θ. Εὐαγγελιστρίας|the Annunciation of the Theotokos
Z|Sokraki|Ὑ.Θ. Περιβολιωτίσσης|Panagia Perivoliotissa
H|Aleimmatades|Ἁγίου Νικολάου|Saint Nicholas
H|Vistonas|Ἁγίου Χριστοφόρου|Saint Christopher
H|Gardelades|Ὑ.Θ. Ἐλεούσης|Panagia Eleousa
H|Doukades|Ὑ. Θεοτόκου Μεσοχωριτίσσης|Panagia Mesochoritissa
H|Krini|Ἁγίου Νικολάου|Saint Nicholas
H|Liapades|Ἁγίας Ἀναστασίας τῆς Φαρμακολυτρίας|Saint Anastasia Pharmakolytria
H|Lakones|Ἁγίου Νικολάου|Saint Nicholas
H|Makrades|Παντοκράτορος|Christ Pantocrator
H|Skripero|Ἁγίου Στεφάνου|Saint Stephen
TH|Gimari|Ἁγίων Κων/νου καί Ἑλένης|Saints Constantine and Helen
TH|Kassiopi|Ὑ.Θ. Κασσιοπίας|Panagia Kassopitra
TH|Nisaki|Ἁγίων Πάντων|All Saints
TH|Sinies|Ἁγίας Βαρβάρας|Saint Barbara
I|Agios Panteleimon|Ἁγίου Παντελεήμονος|Saint Panteleimon
I|Acharavi|Ἁγίου Χαραλάμπους|Saint Charalampus
I|Episkepsi|Ὑ.Θ. Ὁδηγητρίας καί Ἁγίου Βασιλείου|Panagia Hodegetria and Saint Basil
I|Klimatia|Ἁγίου Γεωργίου|Saint George
I|Loutses|Ἁγίου Ἀθανασίου καί Ἁγίου Ἰακώβου|Saint Athanasius and Saint James
I|Lafki|Ἁγίας Παρασκευῆς|Saint Paraskevi
I|Nymfes|Ἁγίων Κων/νου καί Ἑλένης|Saints Constantine and Helen
I|Nymfes|Ἁγίου Νικολάου|Saint Nicholas
I|Kyprianades|Ἁγίου Βασιλείου|Saint Basil
I|Xanthates|Ἁγίας Κυριακῆς|Saint Kyriaki
I|Peritheia|Ἁγίων Θεοδώρων|Holy Theodores
I|Petaleia|Ἁγίου Νικολάου|Saint Nicholas
I|Roda|Ἁγίου Γεωργίου|Saint George
I|Strinylas|Ἁγίας Παρασκευῆς|Saint Paraskevi
I|Sfakera|Ὑ.Θ. Εἰσοδίων|the Entrance of the Theotokos
IA|Agios Athanasios|Ταξιαρχῶν|Holy Archangels
IA|Agros|Ἁγίου Βασιλείου|Saint Basil
IA|Arkadades|Ὑ.Θ. Ἀρκαδιωτίσσης|Panagia Arkadiotissa
IA|Armenades|Ἁγίων Ἀποστόλων|Holy Apostles
IA|Aspiotades|Ὑ.Θ. Βλαχερνῶν|Panagia Blachernae
IA|Afionas|Ἁγίου Ἰωάννου τοῦ Προδρόμου|Saint John the Forerunner
IA|Vatonies|Ἁγίων Ἀποστόλων|Holy Apostles
IA|Dafni|Ὑ.Θ. Εἰσοδίων|the Entrance of the Theotokos
IA|Drosato|Ἁγίου Νικολάου|Saint Nicholas
IA|Kavvadades|Ἁγίου Σπυρίδωνος|Saint Spyridon
IA|Kastellanoi Gyrou|Ἁγίου Νικολάου|Saint Nicholas
IA|Messaria and Kopsocheilades|Ὑ.Θ. Καρουσιωτίσσης καί Ἁγίου Νικολάου|Panagia Karousiotissa and Saint Nicholas
IA|Pagoi|Ἁγίου Ἰωάννου καί Ἁγίων Θεοδώρων|Saint John and the Holy Theodores
IA|Prinylas|Ἁγίου Νικολάου|Saint Nicholas
IA|Rachtades|Ἁγίας Βαρβάρας|Saint Barbara
IA|Chorepiskopoi|Ὑ.Θ. Κουκαμιωτίσσης|Panagia Koukamiotissa
ES|Agioi Douloi|Ἁγίων Θεοδώρων|Holy Theodores
ES|Agrafoi|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
ES|Antipernoi|Ἁγίας Τριάδος|Holy Trinity
ES|Arillas|Ἀναλήψεως τοῦ Σωτῆρος|the Ascension of the Savior
ES|Avliotes|Ταξιαρχῶν|Holy Archangels
ES|Avliotes|Ὑ.Θ. Ὁδηγητρίας|Panagia Hodegetria
ES|Valaneio|Ἁγίου Ἀρσενίου|Saint Arsenius
ES|Velonades|Ἁγίας Τριάδος|Holy Trinity
ES|Ereikoussa|Ἁγίου Νικολάου|Saint Nicholas
ES|Kavallouri|Ὑ.Θ. Εἰσοδίων|the Entrance of the Theotokos
ES|Karousades|Ἁγίου Γεωργίου|Saint George
ES|Karousades|Ἁγίου Νικολάου τῶν Ξένων|Saint Nicholas of the Strangers
ES|Kounavades|Ἁγίας Παρασκευῆς|Saint Paraskevi
ES|Livadi Velonadon|Ἁγίου Σπυρίδωνος|Saint Spyridon
ES|Magoulades|Ἁγίων Θεοδώρων|Holy Theodores
ES|Mathraki|Ἁγίου Νικολάου|Saint Nicholas
ES|Othonoi|Ἁγίας Τριάδος|Holy Trinity
ES|Peroulades|Ἁγίου Νικολάου|Saint Nicholas
ES|Sidari|Ἁγίου Νικολάου|Saint Nicholas
PX|Velianitatika, Paxoi|Ἁγίου Γεωργίου|Saint George
PX|Vlachobogdanatika, Paxoi|Προφήτου Ἠλιού καί Ὑ.Θ. Εἰσοδίων|Prophet Elijah and the Entrance of the Theotokos
PX|Gaios, Paxoi|Ἁγίας Τριάδος|Holy Trinity
PX|Lakka, Paxoi|Ἁγίου Ἀνδρέου|Saint Andrew
PX|Lakka, Paxoi|Ὑπαπαντῆς τοῦ Κυρίου|the Meeting of the Lord
PX|Longos, Paxoi|Ἀναλήψεως τοῦ Κυρίου|the Ascension of the Lord
PX|Magazia, Paxoi|Ἁγίου Σπυρίδωνος|Saint Spyridon
PX|Fountana, Paxoi|Ὑ.Θ. Βλαχερνῶν|Panagia Blachernae
'''

# Legal Greek identity | English name | English seat | optional current detail.
PILGRIMAGE_SOURCE = r'''
Ἁγίου καί Θαυματουργοῦ Σπυρίδωνος|Pilgrimage Church of Saint Spyridon the Wonderworker, Corfu|Corfu|https://imcorfu.gr/iera-proskynimata/iero-proskynima-agiou-spyridona/
Ἁγίων Ἰάσονος καί Σωσιπάτρου|Pilgrimage Church of Saints Jason and Sosipater, Corfu|Corfu|
Ἁγίου Χαραλάμπους|Pilgrimage Church of Saint Charalampus, Paxoi|Paxoi|
Ὑ.Θ. Βελλιανιτῶν|Pilgrimage Church of Panagia Vellianiton, Gaios, Paxoi|Vellianiton Islet, Gaios, Paxoi|https://imcorfu.gr/monastiria/panagia-vellianiton-sto-nisaki-gaios-paxon/
'''

# Rank | current Greek title | English name | English seat | detail page.
# Panagia Vellianiton is not repeated here because the legal pilgrimage row
# and its current detail page establish that it is the same current body.
MONASTERY_SOURCE = r'''
Hermitage|Ἱερό Ἡσυχαστήριο Παντοκράτορος Καμαρέλας|Hermitage of Christ Pantocrator at Kamarela|Kamarela, Agioi Douloi|https://imcorfu.gr/monastiria/iero-isychastirio-pantokratoros-kamarelas/
Hermitage|Ἱερό Ἡσυχαστήριο τῆς Ἁγίας Παρασκευῆς Κοινοπιαστῶν|Hermitage of Saint Paraskevi at Kynopiastes|Kynopiastes|https://imcorfu.gr/monastiria/iero-isychastirio-tis-agias-paraskevis-koinopiaston/
Monastery|Ἱερά Μονή Ἁγίας Παρασκευῆς Μακράδων|Monastery of Saint Paraskevi at Makrades|Makrades|https://imcorfu.gr/monastiria/iera-moni-%E1%BC%81gias-paraskevis-makradon/
Monastery|Ἱερά Μονή Ἁγίας Παρασκευῆς Σγουράδων|Monastery of Saint Paraskevi at Sgourades|Sgourades|https://imcorfu.gr/monastiria/%E1%BC%B1er%E1%BD%B0-mon%E1%BD%B4-%E1%BC%81gias-paraskev%E1%BF%86s-sgouradon/
Monastery|Ἱερά Μονή τῆς Ὑπεραγίας Θεοτόκου Χαμηλῆς Μαγουλάδων|Monastery of Panagia Chamili at Magoulades|Chamili, Magoulades|https://imcorfu.gr/monastiria/iera-moni-t%E1%BF%86s-%E1%BD%91peragias-theotokou-chamil%E1%BF%86s-magouladon/
Monastery|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Κυρᾶς τῶν Ἀγγέλων|Monastery of Panagia Kyra ton Angelon|Lefkimmi|https://imcorfu.gr/monastiria/%E1%BC%B1era-moni-%E1%BD%91peragias-theotokou-kyr%E1%BE%B6s-t%E1%BF%B6n-%E1%BC%80ngelon/
Monastery|Ἱερά Μονή Ἁγίου Δημητρίου Ἁγίων Δούλων|Monastery of Saint Demetrius at Agioi Douloi|Agioi Douloi|https://imcorfu.gr/monastiria/iera-moni-agiou-dimitriou-agion-doulon/
Monastery|Ἱερά Μονή τοῦ Παντοκράτορος, Ἁγίου Ἀθανασίου|Monastery of Christ Pantocrator at Agios Athanasios|Agios Athanasios|https://imcorfu.gr/monastiria/iera-moni-tou-pantokratoros-agiou-athanasiou/
Monastery|Ἱερά Μονή τῶν Ἁγίων Θεοδώρων Στρατιᾶς|Monastery of the Holy Theodores at Stratia|Stratia, Garitsa, Corfu|https://imcorfu.gr/monastiria/iera-moni-ton-agion-theodoron-stratias/
Monastery|Ἱερά Μονή τῆς Ἁγίας Εὐφημίας|Monastery of Saint Euphemia|Mon Repos, Corfu|https://imcorfu.gr/monastiria/iera-moni-tis-agias-effimias/
Monastery|Ἱερά Μονή Ὑψηλοῦ Παντοκράτορος|Monastery of the Most High Pantocrator|Mount Pantokrator|https://imcorfu.gr/monastiria/iera-moni-ypsilou-pantokratoros/
Monastery|Ἱερά Μονή Ἁγίας Τριάδος Κληματιᾶς|Monastery of the Holy Trinity at Klimatia|Klimatia|https://imcorfu.gr/monastiria/iera-moni-agias-triados-klimatias/
Monastery|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Βλαχερνῶν Σκριπεροῦ|Monastery of Panagia Blachernae at Skripero|Skripero|https://imcorfu.gr/monastiria/iera-moni-yperagias-theotokou-vlachernon-skriperou/
Monastery|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Κασσωπίτρας|Monastery of Panagia Kassopitra at Figareto|Figareto, Kanoni|https://imcorfu.gr/monastiria/iera-moni-yperagias-theotokou-kassopitras/
Monastery|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Μυρτιδιωτίσσης|Monastery of Panagia Myrtiotissa|Myrtiotissa, Vatos|https://imcorfu.gr/monastiria/iera-moni-yperagias-theotokou-myrtidiotissis/
Monastery|Ἱερά Μονή Ἁγίων Θεοδώρων Καμάρας|Monastery of the Holy Theodores at Kamara|Kamara|https://imcorfu.gr/monastiria/iera-moni-agion-theodoron-kamaras/
Monastery|Ἱερά Μονή Ἁγίας Κυριακῆς Κουραμάδων|Monastery of Saint Kyriaki at Kouramades|Kouramades|https://imcorfu.gr/monastiria/iera-moni-agias-kyriakis-kouramadon/
Monastery|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Ὑψηλῆς Μαγουλάδων|Monastery of Panagia Ypsili at Magoulades|Ypsili, Magoulades|https://imcorfu.gr/monastiria/iera-moni-yperagias-theotokou-ypsilis-magouladon/
Monastery|Ἱερά Μονή Εὐαγγελιστρίας Εὐρωπούλων|Monastery of the Annunciation at Evropouli|Evropouli|https://imcorfu.gr/monastiria/iera-moni-evangelistrias-evropoulon/
Monastery|Ὑπεραγία Θεοτόκος Παλαιοκαστρίτσας|Monastery of Panagia at Palaiokastritsa|Palaiokastritsa|https://imcorfu.gr/monastiria/yperagia-theotokos-palaiokastritsas/
Monastery|Ἱερά Μονή Ὑπεραγίας Θεοτόκου Πλατυτέρας|Monastery of Panagia Platytera|Platytera, Corfu|https://imcorfu.gr/monastiria/%E1%BC%B1era-moni-%E1%BD%91peragias-theotokou-platyteras/
'''

REGION_COUNTS = {
    "A": 31,
    "B": 12,
    "C": 16,
    "D": 16,
    "E": 9,
    "ST": 13,
    "Z": 11,
    "H": 9,
    "TH": 4,
    "I": 15,
    "IA": 16,
    "ES": 19,
    "PX": 8,
}

CHURCH_DETAIL_URLS = {
    SAINT_JOHN_DETAIL,
    ALL_SAINTS_DETAIL,
    KASSOPITRA_DETAIL,
}
PILGRIMAGE_DETAIL_URLS = {
    SAINT_SPYRIDON_DETAIL,
    CATHEDRAL_DETAIL,
}
MONASTERY_DETAIL_URLS = {
    VELLIANITON_DETAIL,
    *[
        line.rsplit("|", 1)[1]
        for line in MONASTERY_SOURCE.strip().splitlines()
    ],
}
CURRENT_DETAIL_URLS = (
    CHURCH_DETAIL_URLS | PILGRIMAGE_DETAIL_URLS | MONASTERY_DETAIL_URLS
)

FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
ALLOWED_HOSTS = {
    "apantes.gr",
    "www.apantes.gr",
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "imcorfu.gr",
    "www.imcorfu.gr",
}
EXPECTED_TOTAL = 204
EXPECTED_KINDS = {"monastery": 21, "parish": 183}
EXPECTED_RANKS = {
    "Hermitage": 2,
    "Metropolitan Cathedral": 1,
    "Monastery": 19,
    "Parish Church": 178,
    "Pilgrimage Church": 4,
}
EXPECTED_PHONE_BODIES = 1
EXPECTED_PHONE_VALUES = 3
EXPECTED_SITE_BODIES = 1


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def canonical_url(value):
    parsed = urlparse(value)
    path = unquote(parsed.path).rstrip("/") + "/"
    return "%s://%s%s" % (parsed.scheme, parsed.netloc.lower(), path)


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
    if parsed.scheme != "https" or parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


def parish_sources(number):
    if number == 1:
        return [OFFICIAL_PDF, CATHEDRAL_DETAIL, PILGRIMAGE_API]
    if number == 4:
        return [OFFICIAL_PDF, SAINT_JOHN_DETAIL, CHURCH_API]
    if number == 5:
        return [OFFICIAL_PDF, ALL_SAINTS_DETAIL, ALL_SAINTS_SITE]
    if number == 119:
        return [OFFICIAL_PDF, KASSOPITRA_DETAIL, CHURCH_API]
    return [OFFICIAL_PDF]


def parish_address(number, seat):
    if number == 1:
        return ["Mitropoleos Street, Corfu", "Greece"]
    if number == 5:
        return ["Agion Panton Street, Corfu", "Greece"]
    return [seat, "Greece"]


def build_rows():
    if (
            len(CHURCH_DETAIL_URLS),
            len(MONASTERY_DETAIL_URLS),
            len(PILGRIMAGE_DETAIL_URLS),
            len(CURRENT_DETAIL_URLS),
    ) != (3, 22, 2, 27):
        raise ValueError("current WordPress roster totals drifted")
    rows = []
    region_counts = Counter()
    parish_lines = PARISH_SOURCE.strip().splitlines()
    if len(parish_lines) != 179:
        raise ValueError("expected 179 legal parish source rows")
    for number, raw in enumerate(parish_lines, 1):
        region, seat, local, dedication = raw.split("|", 3)
        region_counts[region] += 1
        rank = "Metropolitan Cathedral" if number == 1 else "Parish Church"
        row = {
            "id": "gr-kerkyra-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": "%s of %s, %s" % (rank, dedication, seat),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": parish_address(number, seat),
            "sources": parish_sources(number),
            "checked": CHECKED,
        }
        if number == 4:
            row["phones"] = ["2661039316", "2661039356", "6944183655"]
            row["contact_sources"] = [SAINT_JOHN_DETAIL]
            row["contact_checked"] = CHECKED
        elif number == 5:
            row["site"] = ALL_SAINTS_SITE
        rows.append(row)
    if dict(region_counts) != REGION_COUNTS:
        raise ValueError("legal parish region totals drifted: %r" % region_counts)

    for number, raw in enumerate(PILGRIMAGE_SOURCE.strip().splitlines(), 180):
        local, name, seat, detail = raw.split("|", 3)
        sources = [OFFICIAL_PDF]
        if detail:
            sources.extend([
                detail,
                MONASTERY_API if detail == VELLIANITON_DETAIL
                else PILGRIMAGE_API,
            ])
        rows.append({
            "id": "gr-kerkyra-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": sources,
            "checked": CHECKED,
        })

    for number, raw in enumerate(MONASTERY_SOURCE.strip().splitlines(), 184):
        rank, local, name, seat, detail = raw.split("|", 4)
        rows.append({
            "id": "gr-kerkyra-%03d" % number,
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat, "Greece"],
            "sources": [MONASTERY_API, detail],
            "checked": CHECKED,
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Kerkyra candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Kerkyra candidate ledger date drifted")
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "regulated_parish_rows": 179,
        "regulated_pilgrimage_rows": 4,
        "current_monastery_pages": 22,
        "overlapping_monastery_pages": 1,
        "additional_monastic_rows": 21,
        "parish_kind_rows": 183,
        "monastery_kind_rows": 21,
        "contact_bodies": 1,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_TOTAL,
    }
    if ledger.get("published_summary") != expected:
        raise ValueError("Kerkyra ledger summary drifted")
    for key in (
            "candidates", "source_reconciliations",
            "official_parent_audit", "exclusions"):
        entries = ledger.get(key)
        if not isinstance(entries, list) or not entries:
            raise ValueError("Kerkyra ledger lacks %s" % key)
        for entry in entries:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Kerkyra ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    return ledger


def build():
    ids = set()
    ranks = Counter()
    kinds = Counter()
    result = []
    for source in ROWS:
        item = {
            key: value for key, value in source.items()
            if value not in (None, "", [])
        }
        row_id = item.get("id")
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") != PARENT or item.get("country") != "GR":
            raise ValueError("%s has the wrong parent or country" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(value)
               for value in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        sources = list(item.get("sources") or [])
        if not sources or len(sources) > 3:
            raise ValueError("%s lacks valid sources" % row_id)
        for source_url in sources:
            validate_url(source_url, row_id)
        item["sources"] = sources
        item["cite"] = list(sources)
        contact_sources = list(item.get("contact_sources") or [])
        has_contact = bool(item.get("phones") or item.get("emails"))
        if item.get("site"):
            validate_url(item["site"], row_id)
        if has_contact:
            if not contact_sources or item.get("contact_checked") != CHECKED:
                raise ValueError("%s lacks current contact provenance" % row_id)
            for phone in item.get("phones") or []:
                if not re.fullmatch(r"[26]\d{9}", phone):
                    raise ValueError("%s carries an invalid phone" % row_id)
            for source_url in contact_sources:
                validate_url(source_url, row_id)
                if source_url not in sources:
                    raise ValueError("contact source is outside identity sources")
        elif contact_sources or "contact_checked" in item:
            raise ValueError(
                "%s carries contact provenance without contact data" % row_id
            )
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Kerkyra English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Kerkyra rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Kerkyra kind totals drifted: %r" % dict(kinds))
    phone_bodies = sum(bool(item.get("phones")) for item in result)
    phone_values = sum(len(item.get("phones") or []) for item in result)
    site_bodies = sum(bool(item.get("site")) for item in result)
    contact_bodies = sum(bool(
        item.get("phones") or item.get("emails")
    ) for item in result)
    if (phone_bodies, phone_values, site_bodies, contact_bodies) != (
            EXPECTED_PHONE_BODIES, EXPECTED_PHONE_VALUES,
            EXPECTED_SITE_BODIES, 1):
        raise ValueError("Kerkyra contact coverage drifted")
    validate_ledger()
    return {PARENT: {
        "v": 1,
        "parent": PARENT,
        "country": "GR",
        "rows": result,
    }}


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "application/json,text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    }
    if url == OFFICIAL_PDF:
        headers["Range"] = "bytes=0-4095"
    last_error = None
    for attempt in range(3):
        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=30) as response:
                payload = response.read()
                content_type = response.headers.get("Content-Type", "").lower()
            return payload, content_type
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2)
    raise last_error


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    return unicase(" ".join(text.split()))


def check_api(url, expected_links):
    payload, content_type = fetch(url)
    if "json" not in content_type:
        raise ValueError("non-JSON Kerkyra API source: %s" % url)
    records = json.loads(payload.decode("utf-8"))
    if not isinstance(records, list):
        raise ValueError("Kerkyra API did not return a list: %s" % url)
    links = set()
    for record in records:
        link = record.get("link")
        title = html.unescape((record.get("title") or {}).get("rendered", ""))
        if not link or not title.strip():
            raise ValueError("Kerkyra API returned an incomplete record")
        links.add(canonical_url(link))
    expected = {canonical_url(value) for value in expected_links}
    if links != expected:
        raise ValueError(
            "Kerkyra API roster drifted at %s: expected %d, found %d" %
            (url, len(expected), len(links))
        )
    return url


def check_navigation(payload):
    text = payload.decode("utf-8", "replace")
    links = set()
    for match in re.finditer(r'''href=["']([^"']+)["']''', text):
        value = html.unescape(match.group(1))
        if re.match(
                r"^https://imcorfu[.]gr/"
                r"(?:ieroi-naoi|monastiria|iera-proskynimata)/",
                value):
            links.add(canonical_url(value))
    expected = {canonical_url(value) for value in CURRENT_DETAIL_URLS}
    if links != expected:
        raise ValueError(
            "Kerkyra navigation roster drifted: expected %d, found %d" %
            (len(expected), len(links))
        )


def check_live():
    api_checks = {
        CHURCH_API: CHURCH_DETAIL_URLS,
        MONASTERY_API: MONASTERY_DETAIL_URLS,
        PILGRIMAGE_API: PILGRIMAGE_DETAIL_URLS,
    }
    html_checks = {
        NAV_PAGE: {"Ναοί & Ιερές Μονές", "Παναγία Βελλιανιτών"},
        OFFICES_PAGE: {"Ἐνοριακοὶ Ναοὶ 179", "Ἱερὰ Προσκυνήματα 4"},
        SAINT_JOHN_DETAIL: {"26610 39316", "26610 39356", "6944 183655"},
        ALL_SAINTS_DETAIL: {"apantes.gr", "Ο Ναός έγινε ενοριακός το 2014"},
        ALL_SAINTS_SITE: {"Άγιοι Πάντες", "Κέρκυρα"},
    }

    api_fallbacks = []

    def one_api(item):
        try:
            return check_api(*item)
        except HTTPError as exc:
            if exc.code == 520:
                return item[0], exc.code
            raise

    def one_html(item):
        url, markers = item
        payload, content_type = fetch(url)
        if "html" not in content_type:
            raise ValueError("non-HTML Kerkyra source: %s" % url)
        page = normalized_page(payload)
        missing = [marker for marker in markers
                   if unicase(" ".join(marker.split())) not in page]
        if missing:
            raise ValueError("%s lacks markers: %r" % (url, missing[:3]))
        if url == NAV_PAGE:
            check_navigation(payload)
        return url

    with ThreadPoolExecutor(max_workers=8) as executor:
        api_results = list(executor.map(one_api, api_checks.items()))
        list(executor.map(one_html, html_checks.items()))
    api_fallbacks = [item for item in api_results if isinstance(item, tuple)]
    payload, content_type = fetch(OFFICIAL_PDF)
    if "pdf" not in content_type and not payload.startswith(b"%PDF"):
        raise ValueError("Kerkyra regulation is not a PDF")
    checked = len(api_checks) - len(api_fallbacks) + len(html_checks) + 1
    return checked, api_fallbacks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-live", action="store_true")
    parser.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        data = build()
        if args.check_live:
            checked, api_fallbacks = check_live()
            if api_fallbacks:
                print(
                    "Kerkyra live roster checks passed on %d source surfaces; "
                    "%d API endpoints returned HTTP 520 and were covered by "
                    "the exact 27-link navigation roster" %
                    (checked, len(api_fallbacks))
                )
            else:
                print(
                    "Kerkyra live checks passed for %d source surfaces" %
                    checked
                )
        if args.dump:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        elif args.check or not args.check_live:
            rows = data[PARENT]["rows"]
            print(
                "Kerkyra checks passed: %d bodies, %d contact bodies, "
                "%d public phone values, %d body sites" % (
                    len(rows),
                    sum(bool(
                        item.get("phones") or item.get("emails")
                    ) for item in rows),
                    sum(len(item.get("phones") or []) for item in rows),
                    sum(bool(item.get("site")) for item in rows),
                )
            )
    except Exception as exc:
        print("Kerkyra check failed: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
