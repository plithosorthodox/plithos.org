#!/usr/bin/env python3
"""Validate exact current Polyane and Kilkis bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_polyane_country.py --check
    python tools/directory_polyane_country.py --check-live
    python tools/directory_polyane_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "polyane_country.json"
)
PARENT = "ep-polyane"
ROSTER_PAGE = "https://www.impk.gr/enories/"
ROSTER_REST = "https://www.impk.gr/wp-json/wp/v2/pages/1103"
ADMIN_PAGE = "https://www.impk.gr/dioikisi/dioikitiki-domi/"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-polyanis-kilkisioy/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "polyanes-kai-kilkisiou"
)
LEGAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_noembrios.pdf"
)
LEGAL_HTML = (
    "https://www.e-nomothesia.gr/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-ekklesias-4161-2125-2019.html"
)
YEARBOOK_PDF = (
    "https://www.impk.gr/wp-content/uploads/2025/01/"
    "POLYANHS-TSEPHS-2025-%CE%99%CE%9D%CE%A4%CE%95%CE%A1%CE%9D%CE%95%CE%A4.pdf"
)
SAINT_GEORGE_MONASTERY_PAGE = (
    "https://www.impk.gr/i-iera-moni-agiou-georgiou-lofou-kilkis/"
)
TRANSFIGURATION_SITE = "https://metamorfosikilkis.gr/"


# seat | dedication | current IMPK post id, blank for yearbook-only parishes
PARISH_ROWS = r'''
Kilkis|Transfiguration of the Savior|1096
Kilkis|Fifteen Martyrs|1211
Kilkis|Holy Unmercenaries|1146
Kilkis|Saint Basil and Saint Nicholas|1214
Kilkis|Saint Demetrius|1212
Kilkis|Saint Therapon|1216
Kilkis|Dormition of the Theotokos|1213
Kilkis|Exaltation of the Holy Cross|1215
Rodona|Holy Trinity|1234
Myriofyto|Ascension of the Lord|1233
Mouries|Saints Constantine and Helen|1232
Kritika|Saint Demetrius|1230
Koryfi|Saint Panteleimon|1229
Kalliroi|Saint Irene|1228
Kavalari|Saint Panteleimon|1227
Drosato|Dormition of the Theotokos|1226
Doirani|Prophet Elijah|1225
Amaranta|Saint John the Forerunner|1224
Chorygi|Saint George|1252
Cherso|Saints Constantine and Helen|1251
Plagia|Saint John the Forerunner|1250
Metalliko|Saint George|1249
Megali Sterna|Exaltation of the Holy Cross|1248
Megali Vrysi|Saints Demetrius and Nicholas|1247
Koromilia|Prophet Elijah|1246
Kastanies|Dormition of the Theotokos|1245
Kallindria|Saint Demetrius|1244
Iliolousto|Saint George|1243
Pikrolimni|Saint John the Forerunner|1264
Xylokeratia|Saint George|1263
Mikrokampos|Saint Athanasius|1262
Messiano|Ascension of the Lord|1261
Leventochori|Saints Constantine and Helen|1260
Dafnochori|Saint Demetrius|1259
Palaio Gynaikokastro|Saint Charalambos|1258
Neo Gynaikokastro|Saint George|1257
Kato Apostoloi|Saint George|1256
Ano Apostoloi|Dormition of the Theotokos and Saint Nectarios|1255
Chimadio|Exaltation of the Holy Cross|1276
Petrades|Saint Barbara|1275
Palatiano|Transfiguration of the Savior|1274
Mylochori|Prophet Elijah|1273
Monolithi|Exaltation of the Holy Cross|1272
Mavroplagia|Saints Constantine and Helen|1271
Kentriko|Dormition of the Theotokos|1270
Gavra|Saints Peter and Paul|1269
Antigoneia|Saint George|1268
Koiladi|Saint Demetrius|1267
Fyska|Prophet Elijah|1287
Spourgitis|Saints Constantine and Helen|1286
Xirovrysi|Dormition of the Theotokos|1285
Kato Theodoraki|Holy Trinity|1284
Ano Theodoraki|Saint George|1283
Zacharato|Saints Constantine and Helen|1282
Divouno|Saints Peter and Paul|1281
Gerakario|Saint George|1280
Efkarpia|Nativity of the Theotokos|1279
Vathi|Panagia Faneromeni|1278
Chrysopetra|Saint Athanasius|1305
Fanari|Holy Archangels|1304
Pyrgoto|Saint George|1303
Peristeri|Saint Demetrius|1302
Pedino|Dormition of the Theotokos|1301
Panteleimon|Exaltation of the Holy Cross|1300
Mandres|Saint Demetrius|1299
Leipsydrio|Prophet Elijah|1298
Laodikino|Saint George|1297
Kristoni|Saint Paraskevi|1296
Stefania|Saints Constantine and Helen|1319
Rizana|Prophet Elijah|1318
Melanthio|Saint Demetrius|1317
Lefkochori|Saint Athanasius|1316
Koronouda|Exaltation of the Holy Cross|1315
Karteres|Saint George|1314
Isoma|Saint Athanasius|1313
Theodosia|Meeting of the Lord|1312
Eptalofos|Dormition of the Theotokos|1311
Elliniko|Saint Nicholas|1310
Sevasto|Holy Trinity|1333
Kato Potamia|Saints Peter and Paul|1332
Ano Potamia|Exaltation of the Holy Cross|1331
Pontokerasia|Saint John the Forerunner|1330
Parochthio|Saint John the Forerunner|1329
Metaxochori|Saint Demetrius|1328
Melisourgeio|Saint George|1327
Kokkinia|Saint Demetrius|1326
Dipotamos|Saint Anthony|1325
Argyroupoli|Saints Constantine and Helen and Saint Barbara|1324
Xirochori|Saints Constantine and Helen|1344
Nea Filadelfia|Saint Panteleimon|1343
Nea Mesimvria|Dormition of the Theotokos|1342
Nea Mesimvria|Saint Athanasius|1341
Vathylakkos|Saint John the Theologian|1340
Anchialos|Saint George|1339
Anthofyto|Saints Constantine and Helen|1338
Palaio Agioneri|Saint George|1337
Neo Agioneri|Saint Basil and Saint Panteleimon|1336
Agios Athanasios|Life-Giving Spring|1335
Agios Charalambos|Saint Charalambos|
Agia Kyriaki|Saint Demetrius|
Agia Paraskevi|Saint Paraskevi|
Agios Antonios|Saint Anthony|
Agios Markos|Dormition of the Theotokos|
Akritas|Saint George|
Akropotamia|Dormition of the Theotokos|
Anavryto|Saint George|
Vaptistis|Saint John the Forerunner|
Vafeiochori|Nativity of the Theotokos|
Gallikos|Saint Panteleimon|
Dorkada|Saint Demetrius|
Eleftherochori|Saint John the Forerunner|
Kampanis|Saint Athanasius|
Kolchida|Saint Fanourios|
Mavroneri|Saint Charalambos|
Nea Santa|Transfiguration of the Savior|
Perinthos|Exaltation of the Holy Cross|
Plagiochori|Saint Demetrius|
Mouries Railway Station (Mikrovrysi)|Exaltation of the Holy Cross|
Stavrochori|Saint Athanasius and Nativity of the Theotokos|
Terpyllos|Saint Panteleimon|
'''


# IMPK post id | URL slug | exact current Greek title | displayed address |
# body email. The final six rows are metropolitan chapels, not parishes.
WEB_ROWS = r'''
1096|metamorfosis-tou-sotiros-mitropolitikos|Μεταμόρφωσις του Σωτήρος (Μητροπολιτικός)|Βενιζέλου Ελευθερίου 2, Κιλκίς, 61100|
1211|pentekaideka-martyres-poliouchoi|Πεντεκαίδεκα Μάρτυρες (Πολιούχοι Κιλκίς)|Παπαλουκά - Ελ. Βενιζέλου|dekapentemartires@gmail.com
1146|agion-anargyron-g΄-ergatikes-katoikies-kilkis|Αγίων Αναργύρων|Γ΄ Εργατικές Κατοικίες Κιλκίς|
1214|agios-vasileios-agios-nikolaos|Άγιος Βασίλειος & Άγιος Νικόλαος|Περιοχή ΟΑΕΔ (Πλησίον 12ου Νηπιαγωγείου)|
1212|agios-dimitrios|Άγιος Δημήτριος|Αγ. Δημητρίου 2|
1216|agios-therapon|Άγιος Θεράποντας|Αρχή Νικολάου Αγγελίδη (Περιφερειακός)|
1213|koimisis-tis-theotokou|Κοίμησις της Θεοτόκου|Τέρμα Περικλέους|
1215|ypsosis-timiou-stavrou|Ύψωσις Τιμίου Σταυρού|Α' Εργατικές Κατοικίες|
1234|agia-triada|Αγία Τριάδα Ροδώνας||
1233|analipsis-tou-kyriou|Ανάληψις του Κυρίου Μυριοφύτου||
1232|agioi-kon-nos-eleni|Αγιοι Κων/νος - Ελένη Μουριών||
1230|agios-dimitrios-2|Άγιος Δημήτριος Κρητικών||
1229|agios-panteleimon-2|Άγιος Παντελεήμων Κορυφής||
1228|agia-eirini|Αγία Ειρήνη Καλλιρόης||
1227|agios-panteleimon|Άγιος Παντελεήμων Καβαλαρίου||
1226|koimisis-tis-theotokou-2|Κοίμησις της Θεοτόκου Δροσάτου||
1225|profitis-ilias|Προφήτης Ηλίας Δοϊράνης||
1224|ag-ioannis-prodromos|Αγ. Ιωάννης Πρόδρομος Αμαράντων||
1252|agios-georgios-4|Άγιος Γεώργιος Χωρυγίου||
1251|agioi-kon-nos-eleni-2|Άγιοι Κων/νος & Ελένη Χέρσου||
1250|agios-ioannis-prodromos-2|Άγιος Ιωάννης Πρόδρομος Πλαγιάς||
1249|agios-georgios-3|Άγιος Γεώργιος Μεταλλικού||
1248|ypsosis-timiou-stavrou-3|Ύψωσις Τιμίου Σταυρού Μ. Στέρνας||
1247|agios-dimitrios-agios-nikolaos|Άγιος Δημήτριος & Άγιος Νικόλαος Μ. Βρύσης||
1246|profitis-ilias-2|Προφήτης Ηλίας Κορομηλιάς||
1245|koimisis-tis-theotokou-3|Κοίμησις της Θεοτόκου Καστανιών||
1244|agios-dimitrios-4|Άγιος Δημήτριος Καλλίνδριας||
1243|agios-georgios-2|Άγιος Γεώργιος Ηλιόλουστου||
1264|agios-ioannis-prodromos-3|Άγιος Ιωάννης Πρόδρομος Πικρολίμνης||
1263|agios-georgios-7|Άγιος Γεώργιος Ξυλοκερατιάς||
1262|agios-athanasios|Άγιος Αθανάσιος Μικροκάμπου||
1261|analipsis-tou-kyriou-2|Ανάληψις του Κυρίου Μεσσιανού||
1260|agioi-kon-nos-eleni-3|Άγιοι Κων/νος & Ελένη Λεβεντοχωρίου||
1259|agios-dimitrios-5|Άγιος Δημήτριος Δαφνοχωρίου||
1258|agios-charalabos-3|Άγιος Χαράλαμπος Π. Γυναικοκάστρου||
1257|agios-georgios-6|Άγιος Γεώργιος Ν. Γυναικοκάστρου||
1256|agios-georgios-5|Άγιος Γεώργιος Κ. Αποστόλων||
1255|koimiseos-tis-theotokou-agios-nektarios|Άγιος Νεκτάριος Άνω Αποστόλων||
1276|yps-timiou-stavrou-2|Ύψ. Τιμίου Σταυρού Χειμαδιού||
1275|agia-varvara|Αγία Βαρβάρα Πετράδων||
1274|metamorfosis-tou-sotiros|Μεταμόρφωσις του Σωτήρος Παλατιανού||
1273|profitis-ilias-3|Προφήτης Ηλίας Μυλοχωρίου||
1272|yps-timiou-stavrou|Ύψ. Τιμίου Σταυρού Μονολιθίου||
1271|ag-kon-nos-eleni|Άγ. Κων/νος & Ελένη Μαυροπλαγιάς||
1270|koim-tis-theotokou|Κοίμ. της Θεοτόκου Κεντρικού||
1269|ag-petros-pavlos|Άγ. Πέτρος & Παύλος Γάβρας||
1268|agios-georgios-8|Άγιος Γεώργιος Αντιγόνειας||
1267|agios-dimitrios-6|Άγιος Δημήτριος Κοιλαδίου||
1287|profitis-ilias-4|Προφήτης Ηλίας Φύσκας||
1286|ag-kon-nos-eleni-2|Άγ. Κων/νος & Ελένη Σπουργίτη||
1285|koimisis-tis-theototou|Κοίμησις της Θεοτόκου Ξηρόβρυσης||
1284|agia-triada-2|Αγία Τριάδα Κ. Θεοδωρακίων||
1283|agios-georgios-10|Άγιος Γεώργιος Άνω Θεοδωρακίων||
1282|agioi-kon-nos-eleni-zacharatou|Άγιοι Κων/νος & Ελένη Ζαχαράτου||
1281|ag-petros-pavlos-2|Άγ. Πέτρος & Παύλος Δίβουνου||
1280|agios-georgios-9|Άγιος Γεώργιος Γερακαριού||
1279|genniseos-tis-theotokou-2|Γεννήσεως της Θεοτόκου Ευκαρπίας||inefkarpias@gmail.com
1278|panagia-faneromeni|Παναγία Φανερωμένη Βάθης||
1305|agios-athanasios-3|Άγιος Αθανάσιος Χρυσόπετρας||
1304|pammegiston-taxiarchon|Παμμεγίστων Ταξιαρχών Φαναρίου||
1303|agios-georgios-12|Άγιος Γεώργιος Πυργωτού||
1302|agios-dimitrios-8|Άγιος Δημήτριος Περιστερίου||
1301|koimisis-tis-theotokou-5|Κοίμησις της Θεοτόκου Πεδινού||
1300|ypsosis-timiou-stavrou-4|Ύψωσις Τιμίου Σταυρού Παντελεήμονος||
1299|agios-dimitrios-7|Άγιος Δημήτριος Μανδρών||
1298|profitis-ilias-5|Προφήτης Ηλίας Λειψυδρίου||
1297|agios-georgios-11|Άγιος Γεώργιος Λαοδικηνού||
1296|agia-paraskevi-2|Αγία Παρασκευή Κρηστώνης||
1319|agioi-kon-nos-kai-eleni|Άγιοι Κων/νος και Ελένη Στεφανιών||
1318|profitis-ilias-6|Προφήτης Ηλίας Ριζανών||
1317|agios-dimitrios-10|Άγιος Δημήτριος Μελανθίου||
1316|agios-athanasios-5|Άγιος Αθανάσιος Λευκοχωρίου||
1315|yps-timiou-stavrou-3|Ύψ. Τιμίου Σταυρού Κορωνούδας||
1314|agios-georgios-14|Άγιος Γεώργιος Καρτερών||
1313|agios-athanasios-4|Άγιος Αθανάσιος Ισώματος||
1312|ypapanti-tou-kyriou|Υπαπαντή του Κυρίου Θεοδοσίων||
1311|koim-tis-theotokou-2|Κοίμ. της Θεοτόκου Επταλόφου||
1310|agios-nikolaos|Άγιος Νικόλαος Ελληνικού||
1333|agia-trias|Αγία Τριάς Σεβαστού||
1332|agioi-petros-pavlos|Άγιοι Πέτρος & Παύλος Κ. Ποταμιάς||
1331|ypsosis-timiou-stavrou-5|Ύψωσις Τιμίου Σταυρού Α. Ποταμιάς||
1330|agios-ioannis-prodromos-5|Άγιος Ιωάννης Πρόδρομος Ποντοκερασιάς||
1329|agios-ioannis-prodromos-4|Άγιος Ιωάννης Πρόδρομος Παροχθίου||
1328|agios-dimitrios-12|Άγιος Δημήτριος Μεταξοχωρίου||
1327|agios-georgios-15|Άγιος Γεώργιος Μελισουργειού||
1326|agios-dimitrios-11|Άγιος Δημήτριος Κοκκινιάς||
1325|agios-antonios-2|Άγιος Αντώνιος Διποτάμου||
1324|agioi-kon-nos-eleni-kai-agia-varvara|Άγιοι Κων/νος & Ελένη και Αγία Βαρβάρα Αργυρουπόλεως||
1344|agioi-kon-nos-eleni-6|Άγιοι Κων/νος & Ελένη Ξηροχωρίου Θεσ/νίκης||
1343|agios-panteleimon-5|Άγιος Παντελεήμων Ν. Φιλαδέλφειας Θεσ/νίκης||
1342|koimisis-tis-theotokou-6|Κοίμησις της Θεοτόκου Ν. Μεσήμβριας Θεσ/νίκης||
1341|agios-athanasios-6|Άγιος Αθανάσιος Ν. Μεσήμβριας Θεσ/νίκης||
1340|agios-ioannis-theologos|Άγιος Ιωάννης Θεολόγος Βαθυλάκκου Θεσ/νίκης||
1339|agios-georgios-16|Άγιος Γεώργιος Αγχιάλου Θεσ/νίκης||
1338|agioi-kon-nos-eleni-5|Άγιοι Κων/νος & Ελένη Ανθοφύτου||
1337|palaioagios-georgios|Άγιος Γεώργιος Π. Αγιονερίου||
1336|agios-vasileios-agios-panteleimon|Άγιος Βασίλειος & Άγιος Παντελεήμων Ν. Αγιονερίου||
1335|zoodochou-pigis|Ζωοδόχου Πηγής Αγίου Αθανασίου Θεσ/νίκης||
1147|agias-triados-argyroupoleos|Αγίας Τριάδος (Αργυρουπόλεως)||
1145|agion-rafail-nikolaou-eirinis-str-fylakio-ag-georgiou-lofou-kilkis|Αγίων Ραφαήλ, Νικολάου & Ειρήνης (Στρ. Φυλάκιο Αγ. Γεωργίου Λόφου Κιλκίς)||
1144|agiou-efstathiou-proin-stratopedo-dogani|Αγίου Ευσταθίου (Πρώην Στρατόπεδο Δογάνη)||
1143|agiou-amvrosiou-mitropolitiko-megaro|Αγίου Αμβροσίου (Μητροπολιτικό Μέγαρο)||
1142|taxiarchon-kai-agiou-fanouriou-archaiologiko-mouseio|Ταξιαρχών και Αγίου Φανουρίου (Αρχαιολογικό Μουσείο)||
1141|profitis-ilias-periochi-salats-kilkis|Προφήτης Ηλίας (περιοχή Σαλάτς Κιλκίς)||
'''


# Exact Greek local labels for the current legal/yearbook parishes that do not
# have current IMPK detail pages.
YEARBOOK_ONLY_LOCALS = r'''
Agios Charalambos|Saint Charalambos|Άγιος Χαράλαμπος Αγίου Χαραλάμπους
Agia Kyriaki|Saint Demetrius|Άγιος Δημήτριος Αγίας Κυριακής
Agia Paraskevi|Saint Paraskevi|Αγία Παρασκευή Αγίας Παρασκευής
Agios Antonios|Saint Anthony|Άγιος Αντώνιος Αγίου Αντωνίου
Agios Markos|Dormition of the Theotokos|Κοίμησις της Θεοτόκου Αγίου Μάρκου
Akritas|Saint George|Άγιος Γεώργιος Ακρίτα
Akropotamia|Dormition of the Theotokos|Κοίμησις της Θεοτόκου Ακροποταμιάς
Anavryto|Saint George|Άγιος Γεώργιος Αναβρυτού
Vaptistis|Saint John the Forerunner|Άγιος Ιωάννης Πρόδρομος Βαπτιστή
Vafeiochori|Nativity of the Theotokos|Γεννήσεως της Θεοτόκου Βαφειοχωρίου
Gallikos|Saint Panteleimon|Άγιος Παντελεήμων Γαλλικού
Dorkada|Saint Demetrius|Άγιος Δημήτριος Δορκάδας
Eleftherochori|Saint John the Forerunner|Άγιος Ιωάννης Πρόδρομος Ελευθεροχωρίου
Kampanis|Saint Athanasius|Άγιος Αθανάσιος Καμπάνη
Kolchida|Saint Fanourios|Άγιος Φανούριος Κολχίδας
Mavroneri|Saint Charalambos|Άγιος Χαράλαμπος Μαυρονερίου
Nea Santa|Transfiguration of the Savior|Μεταμόρφωσις του Σωτήρος Νέας Σάντας
Perinthos|Exaltation of the Holy Cross|Ύψωσις Τιμίου Σταυρού Περίνθου
Plagiochori|Saint Demetrius|Άγιος Δημήτριος Πλαγιοχωρίου
Mouries Railway Station (Mikrovrysi)|Exaltation of the Holy Cross|Ύψωσις Τιμίου Σταυρού Σιδηροδρομικού Σταθμού Μουριών (Μικρόβρυση)
Stavrochori|Saint Athanasius and Nativity of the Theotokos|Άγιος Αθανάσιος και Γεννήσεως της Θεοτόκου Σταυροχωρίου
Terpyllos|Saint Panteleimon|Άγιος Παντελεήμων Τερπύλλου
'''


# seat | dedication | complete current public phone union in the 2025
# Metropolis yearbook. Every row is tied to one exact parish body.
YEARBOOK_PHONE_ROWS = r'''
Kilkis|Transfiguration of the Savior|2341022475,2341026165,2341501316,6974151359,6945335705,6974672026,6977534156,6986292305
Kilkis|Fifteen Martyrs|2341022784,2341028635,6977575576,6976697074,6944888183
Kilkis|Saint Demetrius|2341022576,6946359086,6972079043,6946223699
Kilkis|Dormition of the Theotokos|2341029076,6978099754,6946779223,6906717855
Kilkis|Saint Basil and Saint Nicholas|6998377827
Kilkis|Exaltation of the Holy Cross|2341026869,2341020651,6948835609,6955171002
Kilkis|Saint Therapon|2341024380,6973309062
Kilkis|Holy Unmercenaries|2341020993,6976353699
Mouries Railway Station (Mikrovrysi)|Exaltation of the Holy Cross|2341031601,6976428718
Agia Paraskevi|Saint Paraskevi|2341032342,6987767873
Agios Charalambos|Saint Charalambos|2341032342,6987767873
Akritas|Saint George|6979584779
Amaranta|Saint John the Forerunner|6979584779
Doirani|Prophet Elijah|2341103488,6985717105
Drosato|Dormition of the Theotokos|2341031674,2341097137,6934849239
Kavalari|Saint Panteleimon|2341031601,6976428718
Kalliroi|Saint Irene|6987331124
Koryfi|Saint Panteleimon|2341097853,6932288368
Kritika|Saint Demetrius|2341097853,6932288368
Mouries|Saints Constantine and Helen|2341103488,6985717105
Myriofyto|Ascension of the Lord|2341032342,6987331124
Rodona|Holy Trinity|6976428718
Stavrochori|Saint Athanasius and Nativity of the Theotokos|2341071961,2341051510,6974452495
Agia Kyriaki|Saint Demetrius|2341065437,6944936691
Vaptistis|Saint John the Forerunner|2341071708,6940575910
Vafeiochori|Nativity of the Theotokos|2341102017,6978235457
Eleftherochori|Saint John the Forerunner|6983646300
Iliolousto|Saint George|6983646300
Kallindria|Saint Demetrius|6986519443
Kastanies|Dormition of the Theotokos|2341026636,6978510734
Koromilia|Prophet Elijah|2341071795,6983611780
Megali Vrysi|Saints Demetrius and Nicholas|2341026636,6974085004
Megali Sterna|Exaltation of the Holy Cross|6986519443
Metalliko|Saint George|2341071795,6983611780
Plagia|Saint John the Forerunner|6944936691
Cherso|Saints Constantine and Helen|2341051894,6909682200
Chorygi|Saint George|6909617111
Mavroneri|Saint Charalambos|2341091333,6936812093
Ano Apostoloi|Dormition of the Theotokos and Saint Nectarios|6972230654
Kato Apostoloi|Saint George|2341094261,2341094160,6939786436
Neo Gynaikokastro|Saint George|2331095367,6972168671
Palaio Gynaikokastro|Saint Charalambos|6972230654
Dafnochori|Saint Demetrius|2310856060,6978349646
Leventochori|Saints Constantine and Helen|6975202810
Messiano|Ascension of the Lord|2310856060,6978349646
Mikrokampos|Saint Athanasius|6976713919
Xylokeratia|Saint George|2341091026,6980123390
Pikrolimni|Saint John the Forerunner|2341091026,6980123390
Koiladi|Saint Demetrius|2341086141,6974175743
Antigoneia|Saint George|6945824139
Gavra|Saints Peter and Paul|2341088445,6985861786
Kentriko|Dormition of the Theotokos|2341088445,6985861786
Mavroplagia|Saints Constantine and Helen|2341088445,6985861786
Monolithi|Exaltation of the Holy Cross|2341086043,6942438842
Mylochori|Prophet Elijah|6945824139
Palatiano|Transfiguration of the Savior|2341075885,6972428880
Petrades|Saint Barbara|2341088445,6985861786
Chimadio|Exaltation of the Holy Cross|2341020709,6977724466
Vathi|Panagia Faneromeni|2341070684,6981853167
Efkarpia|Nativity of the Theotokos|2341075885,6972428880
Gerakario|Saint George|2341086043,6942438842
Divouno|Saints Peter and Paul|2341027423,6977043121
Zacharato|Saints Constantine and Helen|2341103501,6972378386
Ano Theodoraki|Saint George|6971843500
Kato Theodoraki|Holy Trinity|6971843500
Xirovrysi|Dormition of the Theotokos|2341103501,6972378386
Spourgitis|Saints Constantine and Helen|2310541626,6972192792,6937961911
Fyska|Prophet Elijah|2310541626,6972192792,6937961911
Nea Santa|Transfiguration of the Savior|2341064988,2341064115,6982440430
Akropotamia|Dormition of the Theotokos|2310327578,6979216960
Gallikos|Saint Panteleimon|2310766901,6936431498
Kampanis|Saint Athanasius|2341041033,2341029907,6972227100
Kolchida|Saint Fanourios|6975202810
Kristoni|Saint Paraskevi|2341026022,6953037894
Laodikino|Saint George|2310327578,6979216960
Leipsydrio|Prophet Elijah|2310747922,6988817209
Mandres|Saint Demetrius|6996629368,6945961241
Panteleimon|Exaltation of the Holy Cross|6932354648
Pedino|Dormition of the Theotokos|2392029942,6974219723
Peristeri|Saint Demetrius|2310739530,6936849546
Pyrgoto|Saint George|2310747922,6988817209
Fanari|Holy Archangels|6934620154
Chrysopetra|Saint Athanasius|6934620154
Perinthos|Exaltation of the Holy Cross|2310766901,6936431498
Dorkada|Saint Demetrius|2310605429,6974254042
Anavryto|Saint George|2341025437,6942027119
Elliniko|Saint Nicholas|2341020310,6981881583
Eptalofos|Dormition of the Theotokos|6981841789
Theodosia|Meeting of the Lord|6974084987
Isoma|Saint Athanasius|6974645451
Karteres|Saint George|6981619290
Koronouda|Exaltation of the Holy Cross|2341062385,6945187947
Lefkochori|Saint Athanasius|6981619290
Melanthio|Saint Demetrius|2394033351,6976306360
Rizana|Prophet Elijah|6974084987
Stefania|Saints Constantine and Helen|6974645451
Terpyllos|Saint Panteleimon|6977044917
Agios Antonios|Saint Anthony|6934599312
Agios Markos|Dormition of the Theotokos|6934599312
Argyroupoli|Saints Constantine and Helen and Saint Barbara|2341024287,6977554924
Dipotamos|Saint Anthony|2341020709,6977724466
Kokkinia|Saint Demetrius|6993085821
Melisourgeio|Saint George|6993085821
Metaxochori|Saint Demetrius|2341025437,6942027119
Parochthio|Saint John the Forerunner|2341027656
Pontokerasia|Saint John the Forerunner|2341027656
Ano Potamia|Exaltation of the Holy Cross|6948671289
Kato Potamia|Saints Peter and Paul|6948671289
Sevasto|Holy Trinity|6945187947
Plagiochori|Saint Demetrius|6977724466
Agios Athanasios|Life-Giving Spring|2310701226,2310702386,2391054069,6977875644,6977767989
Neo Agioneri|Saint Basil and Saint Panteleimon|2341093887,2310702331,2310701114,6973994243
Palaio Agioneri|Saint George|2341093793,2310786117,6979203332
Anthofyto|Saints Constantine and Helen|2341093386,6942685508
Anchialos|Saint George|2310603925,6933231119
Vathylakkos|Saint John the Theologian|2310719308,6970042568,6977491282,6977607631
Nea Mesimvria|Saint Athanasius|2310713171,2310713884,6944851483
Nea Mesimvria|Dormition of the Theotokos|2310713174,6981812024
Nea Filadelfia|Saint Panteleimon|2310786021,2310222447,6976792700
Xirochori|Saints Constantine and Helen|6937145526
'''


# seat | dedication | exact Greek label | public phone union
SETTLEMENT_CHAPELS = r'''
Neos Myriofyto|Life-Giving Spring|Ζωοδόχος Πηγή Νέου Μυριοφύτου|2341032342,6987331124
Iliophoto (Brozeika)|Transfiguration of the Savior|Μεταμόρφωσις του Σωτήρος Ηλιοφώτου (Μπροζέικα)|6986519443
Kyriakeika|Dormition of the Theotokos|Κοίμησις της Θεοτόκου Κυριακέικων|2341071708,6940575910
Michalitsi|Resurrection of the Lord|Ανάστασις του Κυρίου Μιχαλιτσίου|6986519443
Soultougianeika|Saint Athanasius|Άγιος Αθανάσιος Σουλτουγιαννέικων|6986519443
Kotyli|Saints Constantine and Helen|Άγιοι Κωνσταντίνος και Ελένη Κοτύλης|2341102017,6978235457
Valtoudi|Holy Trinity|Αγία Τριάδα Βαλτουδίου|2341102017,6978235457
Kalo Livadi|Saint Eleftherios|Άγιος Ελευθέριος Καλού Λιβαδίου|2341075885,6972428880
Tripotamos|Saint George|Άγιος Γεώργιος Τριποτάμου|2341088445,6985861786
Bakaiika|Saint Christopher|Άγιος Χριστόφορος Μπακαίικων|2341091026,6980123390
'''

INSTITUTIONAL_CHURCHES = r'''
Kilkis General Hospital|Saints Constantine and Helen|Άγιοι Κωνσταντίνος και Ελένη, Νοσοκομείο Κιλκίς|2341038400,6936812093
Kilkis care home|Saint Charalambos|Άγιος Χαράλαμπος, Γηροκομείο Κιλκίς|2341022294,2341022576
'''

MONASTIC_ROWS = r'''
Lofos Kilkis|Saint George|Ιερά Μονή Αγίου Γεωργίου Λόφου Κιλκίς|6974151359,2341022740|https://www.impk.gr/i-iera-moni-agiou-georgiou-lofou-kilkis/
Spanos Kilkis|Saint Nectarios|Ιερά Μονή Αγίου Νεκταρίου Σπανού Κιλκίς|6946359086,2341070577|
'''

# English dedication | English seat | exact Greek label. The first six rows
# have current detail pages in WEB_ROWS; the seventh is yearbook-only.
METROPOLITAN_CHAPELS = r'''
Holy Trinity|Argyroupoli|Αγία Τριάδα Αργυρουπόλεως|1147
Saints Raphael, Nicholas, and Irene|Saint George Hill military post, Kilkis|Άγιοι Ραφαήλ, Νικόλαος και Ειρήνη, Στρατιωτικό Φυλάκιο Αγίου Γεωργίου Λόφου Κιλκίς|1145
Saint Eustathios|former Doganis camp, Kilkis|Άγιος Ευστάθιος, πρώην Στρατόπεδο Δογάνη|1144
Saint Ambrose|Metropolitan Hall, Kilkis|Άγιος Αμβρόσιος, Μητροπολιτικό Μέγαρο Κιλκίς|1143
Holy Archangels and Saint Fanourios|Archaeological Museum, Kilkis|Ταξιάρχες και Άγιος Φανούριος, Αρχαιολογικό Μουσείο Κιλκίς|1142
Prophet Elijah|Salats area, Kilkis|Προφήτης Ηλίας, περιοχή Σαλάτς Κιλκίς|1141
Saints Paisios of Mount Athos and Eugene of Trebizond|LAF Kilkis|Άγιοι Παΐσιος ο Αγιορείτης και Ευγένιος Τραπεζούντιος, ΛΑΦ Κιλκίς|
'''


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode(
        "ascii", "ignore"
    ).decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "body"


def phone(value):
    digits = re.sub(r"\D", "", value)
    if len(digits) != 10:
        raise ValueError("unexpected Greek phone: %r" % value)
    return "+30-" + digits


def parse_table(raw, width, label):
    result = []
    for line in raw.strip().splitlines():
        fields = [field.strip() for field in line.split("|")]
        if len(fields) != width:
            raise ValueError("%s row has %d fields: %r" % (
                label, len(fields), line))
        result.append(fields)
    return result


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def web_map():
    result = {}
    for post_id, path, local, address, email_value in parse_table(
            WEB_ROWS, 5, "current web roster"):
        if post_id in result:
            raise ValueError("duplicate current web post id %s" % post_id)
        detail = "https://www.impk.gr/enoria/%s/" % path
        result[post_id] = {
            "detail": detail,
            "local": local,
            "address": address,
            "emails": [email_value] if email_value else [],
        }
    if len(result) != 104:
        raise ValueError("expected 104 current web bodies, found %d" %
                         len(result))
    return result


def yearbook_phone_map():
    result = {}
    for seat, dedication, phone_values in parse_table(
            YEARBOOK_PHONE_ROWS, 3, "yearbook parish phone"):
        key = (seat, dedication)
        if key in result:
            raise ValueError("duplicate yearbook parish contact %r" % (key,))
        result[key] = [phone(value) for value in phone_values.split(",")]
    if len(result) != 120:
        raise ValueError("expected 120 yearbook parish contacts, found %d" %
                         len(result))
    return result


def yearbook_local_map():
    result = {}
    for seat, dedication, local in parse_table(
            YEARBOOK_ONLY_LOCALS, 3, "yearbook-only local"):
        key = (seat, dedication)
        if key in result:
            raise ValueError("duplicate yearbook-only local %r" % (key,))
        result[key] = local
    if len(result) != 22:
        raise ValueError("expected 22 yearbook-only local labels")
    return result


def build_rows():
    rows = []
    web = web_map()
    phone_rows = yearbook_phone_map()
    yearbook_locals = yearbook_local_map()
    parishes = parse_table(PARISH_ROWS, 3, "parish")
    if len(parishes) != 120:
        raise ValueError("expected 120 exact current parishes")
    parish_keys = {(seat, dedication) for seat, dedication, unused in parishes}
    if len(parish_keys) != 120 or set(phone_rows) != parish_keys:
        raise ValueError("yearbook parish identities and contacts diverged")
    post_ids = {post_id for unused, unused2, post_id in parishes if post_id}
    chapel_ids = {"1141", "1142", "1143", "1144", "1145", "1147"}
    if len(post_ids) != 98 or set(web) != post_ids | chapel_ids:
        raise ValueError("current web roster identity reconciliation drifted")
    blank_keys = {
        (seat, dedication) for seat, dedication, post_id in parishes
        if not post_id
    }
    if blank_keys != set(yearbook_locals):
        raise ValueError("yearbook-only local coverage drifted")

    for index, (seat, dedication, post_id) in enumerate(parishes, 1):
        key = (seat, dedication)
        detail = web.get(post_id)
        local = detail["local"] if detail else yearbook_locals[key]
        rank = "Parish Church"
        if key == ("Kilkis", "Transfiguration of the Savior"):
            rank = "Metropolitan Cathedral"
        name = make_name(dedication, rank, seat)
        sources = [YEARBOOK_PDF]
        if key == ("Kilkis", "Holy Unmercenaries"):
            sources.append(ADMIN_PAGE)
        else:
            sources.append(LEGAL_PDF)
        item = {
            "id": "gr-ep-polyane-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [detail["address"] if detail and
                        detail["address"] else seat],
            "phones": phone_rows[key],
            "sources": sources,
            "contact_sources": [YEARBOOK_PDF],
            "contact_checked": CHECKED,
        }
        if detail and post_id != "1096":
            sources.append(detail["detail"])
            item["site"] = detail["detail"]
            if detail["emails"]:
                item["emails"] = detail["emails"]
                item["contact_sources"].append(detail["detail"])
        if post_id == "1096":
            item["site"] = TRANSFIGURATION_SITE
            item["emails"] = ["metamorfosikilkis@gmail.com"]
            sources.append(TRANSFIGURATION_SITE)
            item["contact_sources"].append(TRANSFIGURATION_SITE)
        rows.append(item)

    for dedication, seat, local, post_id in parse_table(
            METROPOLITAN_CHAPELS, 4, "metropolitan chapel"):
        name = make_name(dedication, "Metropolitan Chapel", seat)
        sources = [YEARBOOK_PDF]
        item = {
            "id": "gr-ep-polyane-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Metropolitan Chapel",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": sources,
        }
        if post_id:
            detail = web[post_id]["detail"]
            sources.append(detail)
            item["site"] = detail
        rows.append(item)

    for seat, dedication, local, phone_values in parse_table(
            SETTLEMENT_CHAPELS, 4, "settlement chapel"):
        name = make_name(dedication, "Settlement Chapel", seat)
        rows.append({
            "id": "gr-ep-polyane-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Settlement Chapel",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "phones": [phone(value) for value in phone_values.split(",")],
            "sources": [YEARBOOK_PDF],
            "contact_sources": [YEARBOOK_PDF],
            "contact_checked": CHECKED,
        })

    for seat, dedication, local, phone_values in parse_table(
            INSTITUTIONAL_CHURCHES, 4, "institutional church"):
        name = make_name(dedication, "Institutional Church", seat)
        rows.append({
            "id": "gr-ep-polyane-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Institutional Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "phones": [phone(value) for value in phone_values.split(",")],
            "sources": [YEARBOOK_PDF],
            "contact_sources": [YEARBOOK_PDF],
            "contact_checked": CHECKED,
        })

    for seat, dedication, local, phone_values, detail in parse_table(
            MONASTIC_ROWS, 5, "monastery"):
        name = make_name(dedication, "Monastery", seat)
        sources = [YEARBOOK_PDF, ADMIN_PAGE]
        item = {
            "id": "gr-ep-polyane-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Monastery",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "phones": [phone(value) for value in phone_values.split(",")],
            "sources": sources,
            "contact_sources": [YEARBOOK_PDF, ADMIN_PAGE],
            "contact_checked": CHECKED,
        }
        if detail:
            sources.append(detail)
            item["site"] = detail
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 141
EXPECTED_OWNER_COUNTS = {PARENT: 141}
EXPECTED_KINDS = {"monastery": 2, "parish": 139}
EXPECTED_RANKS = {
    "Institutional Church": 2,
    "Metropolitan Cathedral": 1,
    "Metropolitan Chapel": 7,
    "Monastery": 2,
    "Parish Church": 119,
    "Settlement Chapel": 10,
}
EXPECTED_CONTACT_BODIES = 140
EXPECTED_PHONE_BODIES = 134
EXPECTED_PHONE_VALUES = 255
EXPECTED_EMAIL_BODIES = 3
EXPECTED_EMAIL_VALUES = 3
EXPECTED_SITE_BODIES = 105
EXPECTED_ADDRESS_BODIES = 141
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


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def validate_url(value, label):
    parsed = urlparse(value)
    allowed = {
        "www.impk.gr", "impk.gr", "ec-patr.org", "www.ec-patr.org",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
        "www.e-nomothesia.gr", "e-nomothesia.gr",
        "metamorfosikilkis.gr", "www.metamorfosikilkis.gr",
    }
    if parsed.scheme != "https" or parsed.netloc not in allowed:
        raise ValueError("%s has a non-competent URL: %s" % (label, value))


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 4:
        raise ValueError("%s must carry one to four sources" %
                         item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    contact_sources = list(item.get("contact_sources") or [])
    if contact_sources:
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError("contact source is outside identity sources")
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check" %
                             item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s site lacks source provenance" %
                             item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Polyane candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Polyane candidate ledger date drifted")
    expected_summary = {
        PARENT: 141,
        "total": 141,
        "exact_current_parishes": 120,
        "exact_current_metropolitan_chapels": 7,
        "exact_current_settlement_chapels": 10,
        "exact_current_institutional_churches": 2,
        "exact_current_monasteries": 2,
        "parish_kind_rows": 139,
        "monastery_kind_rows": 2,
        "contact_bodies": 140,
        "phone_bodies": 134,
        "public_phone_values": 255,
        "email_bodies": 3,
        "public_email_values": 3,
        "official_detail_sites": 105,
        "address_bodies": 141,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Polyane candidate ledger summary drifted")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 6:
        raise ValueError("Polyane candidate ledger lacks held leads")


def build():
    result = []
    ids = set()
    signatures = {}
    owner_counts = Counter()
    kind_counts = Counter()
    rank_counts = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        parent = item.get("parent")
        if not row_id or row_id in ids:
            raise ValueError("duplicate or missing Polyane row id")
        if parent not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent %s" % (row_id, parent))
        if item.get("country") != "GR":
            raise ValueError("%s lacks the GR country code" % row_id)
        for field in ("kind", "rank", "name", "local", "seat"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for email_value in item.get("emails") or []:
            if not EMAIL_RE.match(email_value):
                raise ValueError("%s carries an invalid email" % row_id)
        for phone_value in item.get("phones") or []:
            if not re.match(r"^\+30-\d{10}$", phone_value):
                raise ValueError("%s carries an invalid phone" % row_id)
        if len(set(item.get("phones") or [])) != len(item.get("phones") or []):
            raise ValueError("%s repeats a public phone" % row_id)
        signature = (parent, unicase(item["local"]), unicase(item["seat"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s after normalization" % (
                row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[parent] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (
            EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Polyane English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Polyane English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Polyane parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Polyane kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Polyane rank totals drifted: %r" %
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
        raise ValueError("Polyane contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {
        PARENT: {
            "v": 1,
            "parent": PARENT,
            "country": "GR",
            "rows": result,
        }
    }


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    value = re.sub(r"(?<=[\u0370-\u03ff])\s+(?=[\u0370-\u03ff])", "",
                   value)
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_source(url):
    safe_url = quote(url, safe=":/?=&%")
    request = Request(safe_url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=60) as response:
        if response.status >= 400:
            raise ValueError("%s returned HTTP %s" % (url, response.status))
        return (
            response.headers.get("Content-Type", "").lower(),
            response.read(),
        )


def assert_html_markers(url, markers, label):
    content_type, payload = fetch_source(url)
    if "html" not in content_type:
        raise ValueError("%s returned a non-HTML response" % label)
    text = normalize_source_text(payload.decode("utf-8", "replace"))
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("%s source marker drifted: %s" % (label, marker))


def check_detail_page(item):
    content_type, payload = fetch_source(item["detail"])
    if "html" not in content_type or len(payload) < 5000:
        raise ValueError("current body detail failed: %s" % item["detail"])
    text = normalize_source_text(payload.decode("utf-8", "replace"))
    if normalize_source_text(item["local"].split("(", 1)[0].strip()) not in text:
        raise ValueError("current body title drifted: %s" % item["detail"])
    return item["detail"], text


def check_live_sources():
    content_type, payload = fetch_source(ROSTER_REST)
    if "json" not in content_type:
        raise ValueError("current roster REST response is not JSON")
    page = json.loads(payload.decode("utf-8"))
    rendered = page.get("content", {}).get("rendered", "")
    live_ids = set(re.findall(r'<article class="[^"]*\bpost-(\d+)\b',
                              rendered))
    web = web_map()
    if live_ids != set(web) or len(live_ids) != 104:
        raise ValueError("current IMPK roster no longer exposes 104 bodies")
    roster_text = normalize_source_text(rendered)
    for item in web.values():
        if normalize_source_text(item["local"]) not in roster_text:
            raise ValueError("current IMPK title drifted: %s" % item["local"])
        if item["address"] and normalize_source_text(
                item["address"]) not in roster_text:
            raise ValueError("current IMPK address drifted: %s" %
                             item["address"])
    with ThreadPoolExecutor(max_workers=12) as executor:
        detail_text = dict(executor.map(check_detail_page, web.values()))
    for item in web.values():
        for email_value in item["emails"]:
            if (email_value.casefold() not in roster_text and
                    email_value.casefold() not in detail_text[item["detail"]]):
                raise ValueError("current body email drifted: %s" %
                                 item["detail"])

    assert_html_markers(ADMIN_PAGE, (
        "Ενοριακοί Ιεροί Ναοί: 120",
        "Παρεκκλήσια : 65",
        "Ε ξωκκλήσια : 42",
        "Ιεροί Ναοί Κοιμητηρίων: 22",
        "Αγίου Γεωργίου Λόφου Κιλκίς",
        "23410 22.740",
        "Αγίου Νεκταρίου Σπανού Κιλκίς",
        "23410 70.577",
        "Παναγίας Οὐρανοφερούσης Κρουσσίων (ὑπό σύστασιν)",
    ), "current Metropolis administration")
    assert_html_markers(PATRIARCHATE_PAGE, (
        "Ἐνοριακοί Ἱεροί Ναοί: 119",
        "Παρεκκλήσια: 65",
        "Ἐξωκκλήσια: 42",
        "Ἱεροί Ναοί Κοιμητηρίων: 22",
        "Μοναστηριακοί Ναοί: 3",
        "Ἁγίου Γεωργίου Λόφου Κιλκίς",
        "Ἁγίου Νεκταρίου Σπανοῦ Κιλκίς",
    ), "Patriarchate profile")
    assert_html_markers(LEGAL_HTML, (
        "Συνολικός αριθμός Ενοριών: 119",
        "Χωρύγι",
        "Άγιος Γεώργιος",
    ), "2019 legal roster")
    assert_html_markers(CHURCH_OF_GREECE_PAGE, (
        "Πολυανής και Κιλκισίου",
        "Κιλκίς",
    ), "Church of Greece profile")
    assert_html_markers(SAINT_GEORGE_MONASTERY_PAGE, (
        "Ιερά Μονή Αγίου Γεωργίου Λόφου Κιλκίς",
    ), "Saint George monastery")
    assert_html_markers(TRANSFIGURATION_SITE, (
        "metamorfosikilkis@gmail.com",
        "23410 - 22475",
    ), "Transfiguration cathedral site")
    for url, label, minimum in (
        (LEGAL_PDF, "2019 official legal PDF", 100000),
        (YEARBOOK_PDF, "2025 official yearbook PDF", 500000),
    ):
        pdf_type, pdf_payload = fetch_source(url)
        if ("pdf" not in pdf_type or not pdf_payload.startswith(b"%PDF") or
                len(pdf_payload) < minimum):
            raise ValueError("%s is not a valid current PDF" % label)


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    payloads = build()
    if args.check_live:
        check_live_sources()
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Polyane and Kilkis: %d exact named bodies; %d carry current "
            "public body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Polyane: %s" % exc, file=sys.stderr)
        raise SystemExit(1)

