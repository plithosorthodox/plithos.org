#!/usr/bin/env python3
"""Validate exact current Paramythia, Filiates, Giromeri and Parga bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_paramythia_country.py --check
    python tools/directory_paramythia_country.py --check-live
    python tools/directory_paramythia_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "paramythia_country.json"
)
PARENT = "ep-paramythia"
ROSTER_PAGE = "https://imparamythias.gr/acategories/show/enories-290"
MONASTERIES_PAGE = "https://imparamythias.gr/pages/ieres-mones"
ADMIN_PAGE = "https://imparamythias.gr/articles/show/dioikhsis-40"
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/"
    "iera-mitropoli-paramythias-filiaton-giromerioy/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/paramythias-philiaton-geromeriou-kai-pargas"
)
LEGAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_octobrios.pdf"
)
GIROMERI_SITE = "https://www.monigiromeriou.gr/"


# Greek seat | source dedication | source row title | postal code |
# current detail path | body-associated public phones
#
# The current Metropolis page has 150 unique parish detail paths. Its two
# featured Paramythia rows repeat bodies in the complete table; their extra
# public routes are merged into the same exact bodies below. Monastery rows
# embedded in that category are handled separately from the current monastery
# and Patriarchate profiles.
PARISH_ROWS = r'''
Αγιά|Αγ. Παρασκευή|Αγιά|48060|/articles/show/agia-138|6936283660
Αγία Κυριακή Πάργας|Αγ. Κυριακή|Αγία Κυριακή Πάργας|48060|/articles/show/agia-kuriakh-pargas-106|
Αγία Κυριακή Σουλίου|Αγ. Κυριακή|Αγία Κυριακή Σουλίου|46200|/articles/show/agia-kuriakh-souliou-popobo-51|
Αγία Μαρίνα|Κοιμ. Θεοτόκου|Αγία Μαρίνα|46100|/articles/show/agia-marina-94|6944725228
Άγιοι Πάντες|Άγ. Πάντες|Άγιοι Πάντες|46300|/articles/show/agioi-pantes-130|
Άγιος Βλάσιος|Άγ. Αθανάσιος|Άγιος Βλάσιος|46100|/articles/show/agios-blasios-118|6948035246
Άγιος Γεώργιος Ηγ.|Άγ. Γεώργιος|Άγιος Γεώργιος Ηγουμενίτσας|46100|/articles/show/agios-georgios-hgoumenitsas-rizianh-120|
Άγιος Νικόλαος Φιλ.|Άγ. Γεώργιος|Άγιος Νικόλαος Ι.Ν. Αγίου Γεωργίου|46300|/articles/show/agios-nikolaos-agios-georgios-144|2664022407
Άγιος Νικόλαος Φιλ.|Άγ. Νικόλαος|Άγιος Νικόλαος Ι.Ν. Αγίου Νικολάου|46300|/articles/show/agios-nikolaos-agios-nikolaos-145|
Αγορά|Μεταμόρφ. Σωτῆρος|Αγορά|46200|/articles/show/agora-69|
Αετός|Άγ. Νικόλαος|Αετός|46300|/articles/show/aetos-143|6945382714
Αμπελιά|Κοιμ. Θεοτόκου|Αμπελιά|46200|/articles/show/ampelia-91|6937982870
Αμπελών|Άγ. Νικόλαος|Αμπελώνας|46300|/articles/show/ampelonas-131|6977833988
Αναβρυτός|Άγ. Απόστολοι|Αναβρυτός|46300|/articles/show/anabrutos-146|
Ανθούσα|Άγ. Ιωάννης|Ανθούσα|48060|/articles/show/anthousa-139|
Αργυρότοπος|Κοιμ. Θεοτόκου|Αργυρότοπος|46100|/articles/show/argurotopos-110|6949365687
Ασπροκκλήσιον|Άγ. Γεώργιος|Ασπροκκλήσι|46300|/articles/show/asprokklhsi-124|
Αυλότοπος|Αγ. Κυριακή|Αυλότοπος|46031|/articles/show/aulotopos-140|
Αχερουσία|Μεταμ. Σωτήρος|Αχερουσία|48062|/articles/show/axerousia-77|
Αχλαδέα|Κοιμ. Θεοτόκου|Αχλαδιά|46300|/articles/show/axladia-147|
Βαβούρι|Κοιμ. Θεοτόκου|Βαβούρι|46300|/articles/show/babouri-134|
Βασιλικόν|Ζωοδ. Πηγή|Βασιλικό|46100|/articles/show/basiliko-148|
Βερενίκη|Κοιμ. Θεοτόκου|Βερενίκη|44017|/articles/show/berenikh-52|6938420720
Βουβοπόταμος|Άγ. Δημήτριος|Βουβοπόταμος|48062|/articles/show/boubopotamos-73|6978234355
Βροσύνα|Άγ. Γεώργιος|Βροσύνα|44017|/articles/show/brosuna-149|
Βρυσέλλα|Άγ. Απόστολοι|Βρυσέλλα|46300|/articles/show/brusella-150|6950206293
Βρυσούλα|Αγ. Νικόλαος|Βρυσούλα|46300|/articles/show/brusoula-151|
Γαρδίκι Σουλίου|Αγ. Κυριακή, (Άγ. Νεκταρίος)|Γαρδίκι|46031|/articles/show/gardiki-48|6945162817
Άγιος Γεώργιος Φιλ.|Αγ. Παρασκευή|Γαρδίκι Φιλιατών|44017|/articles/show/agios-georgios-filiaton-gardiki-137|
Γηρομέριον|Εισ. Θεοτόκου|Γηρομέρι|46300|/articles/show/ghromeri-152|
Γκρίκα|Αγ. Δονάτος|Γκρίκα|46200|/articles/show/gkrika-89|
Γλυκή|Αγ. Ιωάννης Πρόδρομος|Γλυκή|46031|/articles/show/glukh-47|6976678273
Γολά|Κοιμ. Θεοτόκου|Γολά|46300|/articles/show/gola-153|
Γραικοχώρι|Ἁγία Τριάς|Γραικοχώρι|46100|/articles/show/graikoxori-113|6944246067
Γρανίτσα|Παμμ.Ταξιάρχαι|Γρανίτσα|44017|/articles/show/granitsa-53|6945003112
Δάφνη|Άγ. Παντελεήμων|Δάφνη|46300|/articles/show/dafnh-154|
Δοβλά Ιωαννίνων|Άγ. Νικόλαος|Δοβλά|44017|/articles/show/dobla-155|
Δράμεση|Άγ. Γεώργιος|Δράμεση|46100|/articles/show/dramesh-156|6983634570
Ελαία|Άγ. Δημήτριος|Ελαία|46300|/articles/show/elaia-125|2664023621
Ελευθέριον|Άγ. Αθανάσιος|Ελευθέρι|48060|/articles/show/eleutheri-157|6940537030
Ζάλογγον Άνω|Άγ. Νικόλαος|Ζάλογγο Άνω|44017|/articles/show/zaloggo-ano-158|2658051868
Ζάλογγον Κάτω|Άγ. Νικόλαος|Ζάλογγο Κάτω|44017|/articles/show/zaloggo-kato-159|2658051814
Ζερβοχώρι|Άγ. Νικόλαος|Ζερβοχώρι|46200|/articles/show/zerboxori-68|
Ηγουμενίτσα|Ευαγγελ. Θεοτόκου|Ηγουμενίτσα I.N.Ευαγ.Θεοτόκου|46100|/articles/show/hgoumenitsa-euag-theotokou-42|2665022376,6971738647,6973806644
Ηγουμενίτσα|Άγ. Παντελεήμων|Ηγουμενίτσα Ι.Ν. Αγίου Παντελεήμονα (Κοιμητήριο)|46100|/articles/show/hgoumenitsa-i-n-agiou-pantelehmona-koimhthrio-114|6976773879
Θέμελον|Άγ. Νικόλαος|Θέμελο|48062|/articles/show/themelo-103|
Καλλιθέα Σουλίου|Άγ. Γεώργιος|Καλλιθέα Σουλίου|46200|/articles/show/kallithea-souliou-82|
Καλλιθέα Φιλιατών|Κοιμ. Θεοτόκου|Καλλιθέα Φιλιατών|44017|/articles/show/kallithea-filiaton-160|
Καμίνιον|Μεταμ. Σωτῆρος|Καμίνι|46200|/articles/show/kamini-67|6974654766
Καμίτσιανη|Αγ. Γεώργιος|Καμίτσιανη|46300|/articles/show/kamitsianh-132|6972315041
Καναλλάκι|Κοιμ. Θεοτόκου|Καναλάκι|48062|/articles/show/kanalaki-46|2684022641
Καρβουνάρι|Άγ. Γεώργιος|Καρβουνάρι|46200|/articles/show/karbounari-64|
Καρτέρι|Άγ. Νικόλαος|Καρτέρι|46030|/articles/show/karteri-161|
Καρυώτι|Αγία Τριάς|Καρυώτι|46200|/articles/show/karuoti-61|
Καστρί Ηγουμ.|Άγ. Γεώργιος|Καστρί Ηγουμενίτσας|46100|/articles/show/kastri-hgoumenitsas-117|2665028356
Καστρί Πρεβ.|Άγ. Χαράλαμπος|Καστρί Πρεβέζης|48062|/articles/show/kastri-prebezhs-97|6981835141
Καταβόθρα|Άγ. Κων/νος καί Ἐλένη|Καταβόθρα|46030|/articles/show/katabothra-162|6948042541
Κεραμίτσα|Άγ. Δημήτριος|Κεραμίτσα|46300|/articles/show/keramitsa-96|6944670781
Κερασοχώρι|Αγ. Παρασκευή|Κερασοχώρι|46300|/articles/show/kerasoxori-129|
Κεστρίνη|Αγ. Μηνάς|Κεστρίνη|46100|/articles/show/kestrinh-60|6979105040
Κεφαλοχώρι|Γεν. Προδρόμου|Κεφαλοχώρι|44017|/articles/show/kefaloxori-163|6989126132
Κλεισούρα|Άγ. Γεώργιος|Κλεισούρα|48062|/articles/show/kleisoura-74|
Κοκκινιά|Γεν. Θεοτόκου|Κοκκινιά|46300|/articles/show/kokkinia-164|6933245977
Κοκκινολιθάριον|Άγ. Απόστολοι|Κοκκινολιθάρι|46300|/articles/show/kokkinolithari-165|
Κορύτιανη|Κοιμ. Θεοτόκου|Κορύτιανη|46100|/articles/show/korutianh-166|
Κορώνη|Κοιμ. Θεοτόκου|Κορώνη|48062|/articles/show/koronh-100|6946860035
Κορωνόπουλον|Αγία Τριάς|Κορωνόπολυλο|48062|/articles/show/koronopolulo-99|6949207566
Κουκουλιοί|Κοιμ. Θεοτόκου|Κουκουλιοί|46031|/articles/show/koukoulioi-142|
Κουρεμάδι|Κοιμ. Θεοτόκου|Κουρεμάδι|44017|/articles/show/kouremadi-135|
Κρυόβρυση|Άγ. Αθανάσιος|Κρυόβρυση|46100|/articles/show/kruobrush-167|
Κρυονέρι|Γέννησις Θεοτόκου|Κρυονέρι|46300|/articles/show/kruoneri-168|
Κρυσταλλοπηγή|Άγ. Κοσμάς|Κρυσταλλοπηγή|46200|/articles/show/krustallophgh-80|
Κυπάρισσος|Άγ. Ἰωάννης|Κυπάρισσος|46300|/articles/show/kuparissos-169|
Κυρά Παναγιά|Άγ. Νικόλαος|Κυρά Παναγιά|46200|/articles/show/kura-panagia-63|
Κυψέλη|Άγ. Νικόλαος|Κυψέλη|48062|/articles/show/kupselh-101|6944791265
Λαδοχώρι|Άγ. Γεώργιος|Λαδοχώρι|46100|/articles/show/ladoxori-170|6947689330
Λάκκα Ηγουμ.|Άγ. Γεώργιος|Λάκκα|46100|/articles/show/lakka-171|
Λειβαδάρι|Προφ. Ηλίας|Λειβαδάρι|48060|/articles/show/leibadari-172|
Λεπτοκαρυά|Αγ. Μαρίνα|Λεπτοκαρυά|44017|/articles/show/leptokarua-54|6945335630
Λιά|Αγία Τριάς|Λιά|46300|/articles/show/lia-133|
Λίστα|Άγ. Προκόπιος|Λίστα|44017|/articles/show/lista-136|
Μαζαρακιά|Άγ. Αθανάσιος|Μαζαρακιά|46030|/articles/show/mazarakia-93|6947883095
Μαλουνι|Κοιμ. Θεοτόκου|Μαλούνι|46300|/articles/show/malouni-173|
Μαργαρίτι|Άγ. Βασίλειος|Μαργαρίτι|46030|/articles/show/margariti-112|6983031840
Μαυρονέρι|Άγ. Κοσμάς|Μαυρονέρι|46300|/articles/show/mauroneri-174|
Μαυρούδι|Άγ. Γεώργιος|Μαυρούδι|46100|/articles/show/mauroudi-116|6978850003
Μεσοβούνι|Άγ. Δημήτριος|Μεσοβούνι|46030|/articles/show/mesobouni-92|
Μεσοπόταμος|Άγιος Ίωάννης Πρόδρομος|Μεσοπόταμος|48062|/articles/show/mesopotamos-44|
Μηλέα|Γεν. Θεοτόκου|Μηλέα|44017|/articles/show/mhlea-175|
Μόρφιον|Άγ. Μηνάς|Μόρφι|48060|/articles/show/morfi-104|6940608032
Μουζακαίικα|Άγ. Νικόλαος|Μουζακαίικα|48062|/articles/show/mouzakaiika-75|6906114487
Νάρκισσος|Άγ. Λουκάς|Νάρκισσος|48062|/articles/show/20.606353-76|6945702289
Νέα Σελεύκεια|Άγ. Γεώργιος, Άγ. Ιωάννης|Νέα Σελεύκεια|46100|/articles/show/nea-seleukeia-115|6946485053
Νεοχωριον|Αγ. Παρασκευή|Νεοχώρι|46200|/articles/show/neoxori-81|6943436209
Νεράϊδα|Άγ. Κων/νος καί Ἐλένη|Νεράιδα|46200|/articles/show/neraida-menina-85|
Νεροχωρι|Αγ. Παρασκευή|Νεροχώρι|46300|/articles/show/neroxori-176|6974837415
Ξέχωρον Άνω|Άγ. Δημήτριος|Ξέχωρο Άνω|46300|/articles/show/xexoro-ano-177|
Ξέχωρον Κάτω|Άγ. Γεώργιος|Ξέχωρο Κάτω|46300|/articles/show/xexoro-kato-178|
Ξηρόλοφος|Άγ. Γεώργιος|Ξηρόλοφος|46200|/articles/show/xhrolofos-62|6946479505
Παγκράτιον|Άγ. Ιωάννης|Παγκράτι|46200|/articles/show/pagkrati-78|6982466646
Παλαιόκαστρον|Άγ. Χριστόφορος|Παλαιόκαστρο|46030|/articles/show/palaiokastro-179|
Παλαιοκκλήσι|Κοιμ. Θεοτόκου|Παλαιοκκλήσι|46300|/articles/show/palaiokklhsi-180|
Παλαιοχώρι Άγ. Πάντων -|Γεν. Θεοτόκου|Παλαιοχώρι Αγίων Πάντων|46300|/articles/show/palaioxori-agion-panton-182|
Παλαιοχώρι Σκάλας|Άγ. Δημήτριος|Παλαιοχώρι Σκάλας|46300|/articles/show/palaioxori-skalas-181|6977725099
Παλαμπάς|Άγ. Γεώργιος|Παλαμπάς|46300|/articles/show/palampas-57|
Παραμυθιά|Ἅγ. Δονᾶτος(Καθεδρι. )|Παραμυθιά I.N.Αγίου Δονάτου|46200|/articles/show/paramuthia-7|2666022262,2666022264,6931566674,6974606918,6977044377
Παραμυθιά|Άγ. Νικόλαος- Άγ. Αναστάσιος εκ Παραμυθίας|Παραμυθιά I.N.Αγίου Νικολάου||/articles/show/agios-nikolaos-paramuthias-41|2666023219,6940909079,6947687584
Παραπόταμος|Άγ. Μηνάς|Παραπόταμος|46300|/articles/show/parapotamos-119|6906646055
Πάργα|Άγ. Νικόλαος|Πάργα|48060|/articles/show/parga-43|2684031216
Πέντε Εκκλησιές|Άγ. Νικόλαος|Πέντε Εκκλησιές|46200|/articles/show/pente-ekklhsies-183|6948954315
Πέρδικα|Άγ. Γεώργιος|Πέρδικα|46030|/articles/show/perdika-107|6972424875
Πετροβίτσα|Κοιμ. Θεοτόκου|Πετροβίτσα|46200|/articles/show/petrobitsa-86|
Πηγαδούλια|Κοιμ. Θεοτόκου|Πηγαδούλια|46300|/articles/show/phgadoulia-184|
Πλαίσιον|Προφ. Ηλίας|Πλαίσιο|46300|/articles/show/plaisio-128|
Πλακωτή|Άγ. Γεώργιος|Πλακωτή|46200|/articles/show/plakoth-87|
Πλάτανος|Αγ. Μαρίνα|Πλάτανος|46300|/articles/show/platanos-185|
Πλαταριᾶ|Παμμ. Ταξιάρχαι|Πλαταριά|46100|/articles/show/plataria-109|6946819705
Πολύδροσον|Άγ. Δημήτριος|Πολύδροσο|44017|/articles/show/poludroso-88|6932391413
Πολύδωρον|Κοιμ. Θεοτόκου|Πολύδωρο|44017|/articles/show/poludoro-186|
Πολυνέρι|Άγ. Κων/νος καί Ἐλένη|Πολυνέρι|46100|/articles/show/poluneri-111|
Ποταμιά Σουλίου|Παμμ. Ταξιάρχαι|Ποταμιά Σουλίου|46031|/articles/show/potamia-souliou-72|
Ποταμιά Φιλιατών|Γεν. Θεοτόκου|Ποταμιά Φιλιατών|46300|/articles/show/potamia-filiaton-187|
Προδρόμι|Άγ. Μηνάς|Προδρόμι|46200|/articles/show/prodromi-66|6977270842
Ραβενή|Κοιμ. Θεοτόκου|Ραβενή|44017|/articles/show/rabenh-95|6979205758
Ράγιον|Αγ. Παρασκευή, Αγ.Κοσμάς|Ράγιο|46100|/articles/show/ragio-121|6994001796
Ραχούλι|Άγ. Νικόλαος|Ραχούλι|46200|/articles/show/raxouli-199|
Ριζόν|Κοιμ. Θεοτόκου|Ριζό|46300|/articles/show/rizo-188|
Σαγιάδα|Άγ. Γεώργιος|Σαγιάδα|46300|/articles/show/sagiada-58|6972162882
Σαλονίκι|Άγ. Νικόλαος|Σαλονίκι|46200|/articles/show/saloniki-84|
Σαμονίδα|Ευαγγ. Θεοτόκου|Σαμονίδα|46031|/articles/show/samonida-49|
Σεβαστόν|Άγ. Αρσένιος|Σεβαστό|46200|/articles/show/sebasto-79|
Σίδερη|Άγ. Ιωάννης|Σίδερη|46300|/articles/show/siderh-189|
Σκάνδαλον|Άγ. Γεώργιος|Σκάνδαλο|46200|/articles/show/skandalo-70|
Σκορπιώνα|Κοιμ. Θεοτόκου|Σκορπιώνα|46100|/articles/show/skorpiona-190|6945300744
Σμέρτον|Άγ. Σπυρίδων|Σμέρτο|46300|/articles/show/smertos-123|6972408175
Σπαθαραίοι|Ἀγία Τριάς|Σπαθαραίοι|48060|/articles/show/spatharaioi-105|
Σταυροχώρι|Μεταμ. Σωτῆρος|Σταυροχώρι|48062|/articles/show/stauroxori-98|6949175836
Σύβοτα|Άγ. Νικόλαος|Σύβοτα|46100|/articles/show/subota-108|6909434650
Τρικόρυφον|Άγ. Κων/νος καί Ἐλένη|Τρικόρυφο|46300|/articles/show/trikorufo-191|
Τσαγγάρι|Άγ. Δημήτριος|Τσαγγάρι|46031|/articles/show/tsaggari-141|
Τσαμαντάς|Κοιμ. Θεοτόκου|Τσαμαντάς|46300|/articles/show/tsamantas-56|
Φανερωμένη|Κοιμ. Θεοτόκου|Φανερωμένη|46300|/articles/show/faneromenh-126|
Φασκομηλιά|Μεταμ. Σωτῆρος|Φασκομηλιά|46100|/articles/show/faskomhlia-192|6938357160
Φιλιάται|Αγία Τριάς, Αγ. Δημήτριος|Φιλιάτες|46300|/articles/show/filiates-59|6944462544,6976503924
Φοινίκι|Μεταμ. Σωτήρος|Φοινίκι|46300|/articles/show/foiniki-193|2664024301
Φροσύνη|Άγ. Βλάσιος|Φροσύνη|46031|/articles/show/frosunh-50|6983234471
Χαραυγή|Κοιμ. Θεοτόκου|Χαραυγή|44017|/articles/show/xaraugh-194|
Χόϊκα|Άγ. Νικόλαος|Χόικα|46200|/articles/show/xoika-71|
Χρυσαυγή|Άγ. Νικόλαος|Χρυσαυγή|46200|/articles/show/xrusaugh-65|6942877272
Ψάκκα|Αγ. Βαρβάρα|Ψάκκα|46200|/articles/show/psakka-90|6947178405
'''


# Source dedication spellings normalize to these forty-six exact meanings.
DEDICATION_EN = {
    "αγ. αθανασιοσ": "Saint Athanasius",
    "αγ. αποστολοι": "Holy Apostles",
    "αγ. αρσενιοσ": "Saint Arsenios",
    "αγ. βαρβαρα": "Saint Barbara",
    "αγ. βασιλειοσ": "Saint Basil",
    "αγ. βλασιοσ": "Saint Blaise",
    "αγ. γεωργιοσ": "Saint George",
    "αγ. γεωργιοσ, αγ. ιωαννησ": "Saints George and John",
    "αγ. δημητριοσ": "Saint Demetrius",
    "αγ. δονατοσ": "Saint Donatos",
    "αγ. δονατοσ(καθεδρι. )": "Saint Donatos",
    "αγ. ιωαννησ": "Saint John",
    "αγ. ιωαννησ προδρομοσ": "Saint John the Forerunner",
    "αγ. κοσμασ": "Saint Kosmas",
    "αγ. κυριακη": "Saint Kyriake",
    "αγ. κυριακη, (αγ. νεκταριοσ)": "Saint Kyriake and Saint Nectarios",
    "αγ. κων/νοσ και ελενη": "Saints Constantine and Helen",
    "αγ. λουκασ": "Saint Luke",
    "αγ. μαρινα": "Saint Marina",
    "αγ. μηνασ": "Saint Minas",
    "αγ. νικολαοσ": "Saint Nicholas",
    "αγ. νικολαοσ- αγ. αναστασιοσ εκ παραμυθιασ": (
        "Saint Nicholas and Saint Anastasios of Paramythia"
    ),
    "αγ. παντελεημων": "Saint Panteleimon",
    "αγ. παντεσ": "All Saints",
    "αγ. παρασκευη": "Saint Paraskevi",
    "αγ. παρασκευη, αγ.κοσμασ": "Saint Paraskevi and Saint Kosmas",
    "αγ. προκοπιοσ": "Saint Prokopios",
    "αγ. σπυριδων": "Saint Spyridon",
    "αγ. χαραλαμποσ": "Saint Charalambos",
    "αγ. χριστοφοροσ": "Saint Christopher",
    "αγια τριασ": "Holy Trinity",
    "αγια τριασ, αγ. δημητριοσ": "Holy Trinity and Saint Demetrius",
    "αγιοσ ιωαννησ προδρομοσ": "Saint John the Forerunner",
    "γεν. θεοτοκου": "Nativity of the Theotokos",
    "γεν. προδρομου": "Nativity of Saint John the Forerunner",
    "γεννησισ θεοτοκου": "Nativity of the Theotokos",
    "εισ. θεοτοκου": "Entrance of the Theotokos into the Temple",
    "ευαγγ. θεοτοκου": "Annunciation of the Theotokos",
    "ευαγγελ. θεοτοκου": "Annunciation of the Theotokos",
    "ζωοδ. πηγη": "Life-Giving Spring",
    "κοιμ. θεοτοκου": "Dormition of the Theotokos",
    "μεταμ. σωτηροσ": "Transfiguration of the Savior",
    "μεταμορφ. σωτηροσ": "Transfiguration of the Savior",
    "παμμ. ταξιαρχαι": "Holy Archangels",
    "παμμ.ταξιαρχαι": "Holy Archangels",
    "προφ. ηλιασ": "Prophet Elijah",
}


SEAT_EN = {
    "Άγιος Γεώργιος Ηγ.": "Agios Georgios, Igoumenitsa",
    "Άγιος Γεώργιος Φιλ.": "Agios Georgios, Filiates",
    "Άγιος Νικόλαος Φιλ.": "Agios Nikolaos, Filiates",
    "Καστρί Ηγουμ.": "Kastri, Igoumenitsa",
    "Καστρί Πρεβ.": "Kastri, Preveza",
    "Λάκκα Ηγουμ.": "Lakka, Igoumenitsa",
    "Παλαιοχώρι Άγ. Πάντων -": "Palaiochori Agion Panton",
    "Φιλιάται": "Filiates",
}


# seat | dedication | exact local label | rank | phone values | address | site
MONASTIC_ROWS = r'''
Paganion|Dormition of the Theotokos|Ιερά Μονή Κοιμήσεως της Θεοτόκου Παγανιών|Monastery|2666031244|Kallithea Souliou 46200|
Giromeri|Dormition of the Theotokos|Πατριαρχική και Σταυροπηγιακή Ιερά Μονή Κοιμήσεως της Θεοτόκου Γηρομερίου|Patriarchal and Stavropegic Monastery|2664022407|Giromeri, Filiates 46300|https://www.monigiromeriou.gr/
Ragi|Dormition of the Theotokos|Ιερά Μονή Κοιμήσεως της Θεοτόκου Ραγίου|Monastery|2665028510|Ragi, Igoumenitsa 46100|
Pounta|Saint Paraskevi|Ιερά Μονή Αγίας Παρασκευής Πούντας|Monastery|2684022159,2684024151|Pounta, Kanallaki 48062|
'''


# seat | dedication | exact local label | governing monastery seat
DEPENDENCY_ROWS = r'''
Chrysavgi (Velliani)|Nativity of Saint John the Forerunner|Γενέθλιον Τιμίου Προδρόμου Χρυσαυγής (Βέλλιανης)|Paganion
Michla|Nativity of the Theotokos|Γενέθλιον Θεοτόκου Μίχλας|Paganion
Plakoti|Transfiguration of the Savior|Μεταμόρφωσις Σωτήρος Πλακωτής|Paganion
Kokkinolithari|Saint Minas|Άγιος Μηνάς Κοκκινολιθαρίου|Giromeri
Vavouri|Saint Athanasius|Άγιος Αθανάσιος Βαβουρίου|Giromeri
Lykou|Saint Marina|Αγία Μαρίνα Λύκου|Giromeri
Agioi Pantes|Dormition of the Theotokos|Κοίμησις Θεοτόκου Αγίων Πάντων|Giromeri
'''


# seat | dedication | exact local label
PILGRIMAGE_ROWS = r'''
Perdika|Saint Athanasius|Προσκυνηματικός Ναός Ἁγίου Ἀθανασίου Πέρδικας
Agionysio|Life-Giving Spring|Προσκυνηματικός Ναός Ζωοδόχου Πηγῆς Ἁγιονησίου
'''


GREEK_ROMAN = {
    "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
    "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
    "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
    "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
    "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
}


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


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


def romanize(value):
    if value in SEAT_EN:
        return SEAT_EN[value]
    value = unicase(value)
    for source, replacement in (
            ("γγ", "ng"), ("ου", "ou"), ("αι", "ai"),
            ("ει", "ei"), ("οι", "oi"), ("αυ", "av"),
            ("ευ", "ev")):
        value = value.replace(source, replacement)
    value = "".join(GREEK_ROMAN.get(char, char) for char in value)
    value = re.sub(r"\s+", " ", value).strip(" -")
    return " ".join(part[:1].upper() + part[1:] for part in value.split(" "))


def make_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def parish_static_rows():
    rows = parse_table(PARISH_ROWS, 6, "current parish roster")
    if len(rows) != 150:
        raise ValueError("expected 150 exact current parish rows")
    paths = [row[4] for row in rows]
    if len(set(paths)) != 150:
        raise ValueError("current parish detail paths are not unique")
    return rows


def build_rows():
    rows = []
    for index, fields in enumerate(parish_static_rows(), 1):
        seat_local, dedication_local, row_title, postal, path, phones = fields
        dedication_key = unicase(dedication_local)
        if dedication_key not in DEDICATION_EN:
            raise ValueError("unmapped parish dedication: %s" % dedication_local)
        dedication = DEDICATION_EN[dedication_key]
        seat = romanize(seat_local)
        rank = "Parish Church"
        if path == "/articles/show/paramuthia-7":
            rank = "Cathedral"
        elif path == (
                "/articles/show/"
                "hgoumenitsa-i-n-agiou-pantelehmona-koimhthrio-114"):
            rank = "Cemetery Church"
        name = make_name(dedication, rank, seat)
        detail = "https://imparamythias.gr" + path
        address = seat + ((" " + postal) if postal else "")
        item = {
            "id": "gr-ep-paramythia-%03d-%s" % (index, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": "%s - %s" % (row_title, dedication_local),
            "seat": seat,
            "country": "GR",
            "address": [address],
            "site": detail,
            "sources": [ROSTER_PAGE, detail, LEGAL_PDF],
        }
        if phones:
            item["phones"] = [phone(value) for value in phones.split(",")]
            item["contact_sources"] = [ROSTER_PAGE]
            item["contact_checked"] = CHECKED
        rows.append(item)

    for seat, dedication, local, rank, phones, address, site in parse_table(
            MONASTIC_ROWS, 7, "current monastery"):
        name = make_name(dedication, rank, seat)
        sources = [MONASTERIES_PAGE, PATRIARCHATE_PAGE]
        item = {
            "id": "gr-ep-paramythia-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address],
            "phones": [phone(value) for value in phones.split(",")],
            "sources": sources,
            "contact_sources": [MONASTERIES_PAGE],
            "contact_checked": CHECKED,
        }
        if site:
            sources.append(site)
            item["site"] = site
        rows.append(item)

    for seat, dedication, local, governing_seat in parse_table(
            DEPENDENCY_ROWS, 4, "current dependency"):
        name = "%s Metochion of %s Monastery in %s" % (
            dedication, governing_seat, seat
        )
        rows.append({
            "id": "gr-ep-paramythia-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "monastery",
            "rank": "Metochion",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": [MONASTERIES_PAGE, PATRIARCHATE_PAGE],
        })

    for seat, dedication, local in parse_table(
            PILGRIMAGE_ROWS, 3, "current pilgrimage"):
        name = make_name(dedication, "Pilgrimage Church", seat)
        sources = [PATRIARCHATE_PAGE]
        if seat == "Agionysio":
            sources.append(MONASTERIES_PAGE)
        rows.append({
            "id": "gr-ep-paramythia-%03d-%s" % (len(rows) + 1, slug(name)),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Pilgrimage Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [seat],
            "sources": sources,
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 163
EXPECTED_OWNER_COUNTS = {PARENT: 163}
EXPECTED_KINDS = {"monastery": 11, "parish": 152}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Church": 1,
    "Metochion": 7,
    "Monastery": 3,
    "Parish Church": 148,
    "Patriarchal and Stavropegic Monastery": 1,
    "Pilgrimage Church": 2,
}
EXPECTED_CONTACT_BODIES = 154
EXPECTED_PHONE_BODIES = 75
EXPECTED_PHONE_VALUES = 85
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 151
EXPECTED_ADDRESS_BODIES = 163
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
    allowed = {
        "imparamythias.gr", "www.imparamythias.gr",
        "ec-patr.org", "www.ec-patr.org",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
        "monigiromeriou.gr", "www.monigiromeriou.gr",
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
    if not sources or len(sources) > 3:
        raise ValueError("%s must carry one to three sources" % item.get("id"))
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
            raise ValueError("%s lacks a current contact check" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s site lacks source provenance" % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Paramythia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Paramythia candidate ledger date drifted")
    expected_summary = {
        PARENT: 163,
        "total": 163,
        "exact_current_parishes": 150,
        "exact_current_monasteries": 4,
        "exact_current_metochia": 7,
        "exact_current_pilgrimage_churches": 2,
        "parish_kind_rows": 152,
        "monastery_kind_rows": 11,
        "contact_bodies": 154,
        "phone_bodies": 75,
        "public_phone_values": 85,
        "email_bodies": 0,
        "public_email_values": 0,
        "official_detail_sites": 151,
        "address_bodies": 163,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Paramythia candidate ledger summary drifted")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 6:
        raise ValueError("Paramythia candidate ledger lacks held leads")


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
            raise ValueError("duplicate or missing Paramythia row id")
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
        raise ValueError("Paramythia English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Paramythia English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Paramythia parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Paramythia kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Paramythia rank totals drifted: %r" %
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
        raise ValueError("Paramythia contact coverage drifted: %r" %
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
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_source(url):
    request = Request(url, headers={
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


def decode_html(payload, content_type):
    match = re.search(r"charset=([^;\s]+)", content_type)
    encoding = match.group(1).strip("\"'") if match else "utf-8"
    try:
        return payload.decode(encoding, "replace")
    except LookupError:
        return payload.decode("utf-8", "replace")


def assert_html_markers(url, markers, label):
    content_type, payload = fetch_source(url)
    if "html" not in content_type:
        raise ValueError("%s returned a non-HTML response" % label)
    text = normalize_source_text(decode_html(payload, content_type))
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("%s source marker drifted: %s" % (label, marker))


class RosterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row = []
        elif self.row is not None and tag == "td":
            self.cell = {"text": [], "links": []}
            self.row.append(self.cell)
        elif self.cell is not None and tag == "a":
            self.cell["links"].append(attrs.get("href", ""))
        elif self.cell is not None and tag == "br":
            self.cell["text"].append(" ")

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "td":
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
            self.cell = None


def live_roster(payload):
    parser = RosterParser()
    parser.feed(payload.decode("utf-8", "replace"))
    result = {}
    body_rows = 0
    for cells in parser.rows:
        if len(cells) < 3:
            continue
        title = re.sub(r"\s+", " ", "".join(cells[1]["text"])).strip()
        detail = re.sub(r"\s+", " ", "".join(cells[2]["text"])).strip()
        links = [
            value for value in cells[1]["links"] + cells[2]["links"]
            if "/articles/show/" in value
        ]
        if not title or not links or title.startswith("Ιερά Μονή"):
            continue
        body_rows += 1
        path = urlparse(links[0]).path
        item = result.setdefault(path, {"texts": [], "phones": set()})
        item["texts"].append(title + " " + detail)
        for value in re.findall(
                r"(?<!\d)(?:2\d{4}(?:[- .]?\d){5}|"
                r"6\d{2}(?:[- .]?\d){7})(?!\d)", detail):
            digits = "".join(re.findall(r"\d", value))
            if len(digits) == 10:
                item["phones"].add(digits)
    if body_rows != 152 or len(result) != 150:
        raise ValueError(
            "current roster no longer has 152 rows and 150 unique parishes"
        )
    result["/articles/show/paramuthia-7"]["phones"].add("2666022262")
    return result


def check_detail_page(fields):
    unused, unused2, row_title, unused3, path, unused4 = fields
    url = "https://imparamythias.gr" + path
    content_type, payload = fetch_source(url)
    if "html" not in content_type or len(payload) < 5000:
        raise ValueError("current parish detail failed: %s" % url)
    text = normalize_source_text(decode_html(payload, content_type))
    if normalize_source_text(row_title) not in text:
        raise ValueError("current parish title drifted: %s" % url)
    return url


def check_live_sources():
    content_type, payload = fetch_source(ROSTER_PAGE)
    if "html" not in content_type:
        raise ValueError("current parish roster returned a non-HTML response")
    live = live_roster(payload)
    static = parish_static_rows()
    static_paths = {row[4] for row in static}
    if set(live) != static_paths:
        raise ValueError("current parish detail path set drifted")
    for seat_local, dedication, row_title, postal, path, phones in static:
        live_text = normalize_source_text(" ".join(live[path]["texts"]))
        for marker in (row_title, dedication):
            if normalize_source_text(marker) not in live_text:
                raise ValueError("current roster identity drifted: %s" % path)
        if postal and postal not in re.sub(r"\D", "", " ".join(
                live[path]["texts"])):
            raise ValueError("current roster postal code drifted: %s" % path)
        expected_phones = set(phones.split(",")) if phones else set()
        if live[path]["phones"] != expected_phones:
            raise ValueError("current roster phone union drifted: %s" % path)
    with ThreadPoolExecutor(max_workers=12) as executor:
        list(executor.map(check_detail_page, static))

    assert_html_markers(ADMIN_PAGE, (
        "Ἐνοριακοὶ Ναοὶ 150",
        "Ἐξωκκλήσια 380",
        "Παρεκκλήσια 354",
        "Ναοὶ Κοιμητηρίων 50",
        "Μοναστηριακοὶ Ναοὶ 8",
    ), "current Metropolis administration")
    assert_html_markers(MONASTERIES_PAGE, (
        "ΙΕΡΑ ΜΟΝΗ ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΠΑΓΑΝΙΩΝ",
        "26660-31244",
        "Γενέθλιον Τιμίου Προδρόμου Χρυσαυγῆς",
        "Γενέθλιον Θεοτόκου Μίχλας",
        "Μεταμόρφωσις Σωτῆρος Πλακωτῆς",
        "ΙΕΡΑ ΜΟΝΗ ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΓΗΡΟΜΕΡΙΟΥ",
        "26640-22407",
        "Ἅγ. Μηνᾶς Κοκκινολιθαρίου",
        "Ἅγ. Ἀθανάσιος Βαβουρίου",
        "Ἅγ. Μαρίνα Λύκου",
        "Κοιμ. Θεοτόκου Ἁγίων Πάντων",
        "ΙΕΡΑ ΜΟΝΗ ΚΟΙΜΗΣΕΩΣ ΤΗΣ ΘΕΟΤΟΚΟΥ ΡΑΓΙΟΥ",
        "26650-28510",
        "ΙΕΡΑ ΜΟΝΗ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΠΟΥΝΤΑΣ",
        "26840-22159, 24151",
        "Ζωοδόχου Πηγῆς Ἁγιονησίου",
    ), "current Metropolis monastery profile")
    assert_html_markers(PATRIARCHATE_PAGE, (
        "Ἐνοριακοί Ναοί 150",
        "Ἐξωκκλήσια 380",
        "Παρεκκλήσια 354",
        "Ναοί Κοιμητηρίων 50",
        "Μοναστηριακοί Ναοί 8",
        "Κοιμήσεως τῆς Θεοτόκου Παγανιῶν",
        "Πατριαρχική καί Σταυροπηγιακή Μονή Κοιμήσεως τῆς Θεοτόκου",
        "Κοιμήσεως τῆς Θεοτόκου Ραγίου",
        "Ἁγίας Παρασκευῆς Πούντας",
        "Γενέθλιον τοῦ Τιμίου Προδρόμου Χρυσαυγῆς",
        "Ἅγιος Μηνᾶς Κοκκινολιθαρίου",
        "Ἅγιος Ἀθανάσιος Βαβουρίου",
        "Ἁγία Μαρίνα Λύκου",
        "Κοίμησις τῆς Θεοτόκου Ἁγίων Πάντων",
        "Ἁγίου Ἀθανασίου Πέρδικας",
        "Ζωοδόχου Πηγῆς Ἁγιονησίου",
    ), "Patriarchate profile")
    assert_html_markers(CHURCH_OF_GREECE_PAGE, (
        "Παραμυθίας, Φιλιατών, Γηρομερίου και Πάργας",
        "Κοιμ. Θεοτόκου Παγανιών",
        "Κοιμ. Θεοτόκου Γηρομερίου",
    ), "Church of Greece profile")
    assert_html_markers(GIROMERI_SITE, (
        "Holy Monastery of Giromeri",
    ), "Giromeri monastery site")
    pdf_type, pdf_payload = fetch_source(LEGAL_PDF)
    if ("pdf" not in pdf_type or not pdf_payload.startswith(b"%PDF") or
            len(pdf_payload) < 4000000):
        raise ValueError("2019 official legal PDF is not a valid roster PDF")


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
            "Paramythia, Filiates, Giromeri and Parga: %d exact named "
            "bodies; %d carry current public body-associated phone routes" %
            (EXPECTED_TOTAL, EXPECTED_PHONE_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Paramythia: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
