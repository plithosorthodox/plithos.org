#!/usr/bin/env python3
"""Validate exact named Neapolis and Stavroupolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_neapolis_stavroupolis_country.py --check
    python tools/directory_neapolis_stavroupolis_country.py --check-live
    python tools/directory_neapolis_stavroupolis_country.py --dump
"""

import argparse
from collections import Counter
import html
from http.client import IncompleteRead
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "ep-neapolis-stavroupolis"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" /
    "neapolis_stavroupolis_country.json"
)

LOCAL_DIRECTORY = "https://imnst.gr/enories/"
LOCAL_REST = (
    "https://imnst.gr/wp-json/wp/v2/product?per_page=100&orderby=id&"
    "order=asc&status=publish"
)
LOCAL_CATEGORY_REST = (
    "https://imnst.gr/wp-json/wp/v2/product_cat?per_page=100"
)
OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_january.pdf"
)
TRANSCRIPTION = (
    "https://www.e-nomothesia.gr/inner.php/kat-ekklesia-thriskeia/"
    "kanonismoi-ieras-sunodou/"
    "kanonismos-ieras-sunodou-5509-2684-2019.html?print=1"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-neapoleos-"
    "stayroypoleos/"
)


# product id|kind|rank|English name|Greek local name|English seat|address|
# phones|emails|site|detail slug or @query|legal roster row
PRIMARY_SOURCE = r'''
8421|parish|Metropolitan Parish Church|Metropolitan Parish Church of Saint George, Neapoli|Ιερός Μητροπολιτικός Ναός Αγίου Γεωργίου Νεαπόλεως|Neapoli|Παν. Τσαλδάρη 12, Τ.Κ. 567 28, Νεάπολη|2310 613 060,2310 613 020|AgGeorgiosNeap@imnst.gr||agios-georgios|1
8422|parish|Cathedral Parish Church|Cathedral Parish Church of Saint John the Forerunner, Neapoli|Ιερός Καθεδρικός Ναός Τιμίου Προδρόμου Νεαπόλεως|Neapoli|Μητροπόλεως 13, Τ.Κ. 567 28, Νεάπολη|2310 617 565|timiosprodromosneapolis@yahoo.gr||timios-prodromos|1
8423|parish|Parish Church|Parish Church of Saint Athanasius, Evosmos|Ιερός Ναός Αγίου Αθανασίου Ευόσμου|Evosmos|Εύοσμος|2310 763 354|AgAthanEyosmou@imnst.gr|https://www.katakomvi.gr/|agios-athanasios|1
8424|parish|Parish Church|Parish Church of Saint Athanasius, Nea Magnisia|Ιερός Ναός Αγίου Αθανασίου Νέας Μαγνησίας|Nea Magnisia|Παύλου Κουντουριώτη 11, Τ.Κ. 570 08, Νέα Μαγνησία|2310 781 551,2310 784 409|AgAthanMagn@imnst.gr||agios-athanasios-2|1
8425|parish|Parish Church|Parish Church of Saint Athanasius, Palaiokastro|Ιερός Ναός Αγίου Αθανασίου Παλαιοκάστρου|Palaiokastro|Ηρώων 1, Τ.Κ. 570 13, Παλαιόκαστρο|2310697148|AgAthanPalaiok@imnst.gr|https://inaap.wordpress.com/|agios-athanasios-3|1
8426|parish|Parish Church|Parish Church of the Resurrection of the Lord, Ampelokipoi|Ιερός Ναός Αναστάσεως του Κυρίου Αμπελοκήπων|Ampelokipoi|Πρώην Στρατόπεδο Μεγάλου Αλεξάνδρου, Τ.Κ. 561 22, Αμπελόκηποι|2310 735 944|AnastasiAmpel@imnst.gr||anastasis-tou-kyriou|1
8427|parish|Parish Church|Parish Church of the Holy Apostles, Pefka|Ιερός Ναός Αγίων Αποστόλων Πεύκων|Pefka|Τ.Κ. 570 10, Πεύκα|2310 674 700|AgApostoloi@imnst.gr||agioi-apostoloi|1
8428|parish|Parish Church|Parish Church of Saint Barbara, Stavroupoli|Ιερός Ναός Αγίας Βαρβάρας Σταυρουπόλεως|Stavroupoli|Λαγκαδά 162, Τ.Κ. 564 29, Σταυρούπολη|6972 082 974|info@naosagiasbarbaras.gr|https://naosagiasbarbaras.gr/|agia-varvara|1
8429|parish|Parish Church|Parish Church of Saint Basil and Saints Constantine and Helen, Sykies|Ιερός Ναός Αγίου Βασιλείου και Αγίων Κωνσταντίνου και Ελένης Συκεών|Sykies|Δαβάκη 24, Τ.Κ. 566 25, Συκιές|2310 615 300|AgBasileios@imnst.gr||agios-vasileios|1
8430|parish|Parish Church|Parish Church of Saint George, Asvestochori|Ιερός Ναός Αγίου Γεωργίου Ασβεστοχωρίου|Asvestochori|Τ.Κ. 570 10, Ασβεστοχώρι|2310 357 202|eneaagas@yahoo.gr|https://agiosgeorgiosasvestohori.gr/|agios-georgios-2|1
8431|parish|Parish Church|Parish Church of Saint George, Eleftherio|Ιερός Ναός Αγίου Γεωργίου Ελευθερίου|Eleftherio|Πλατεία Αγίου Γεωργίου, Τ.Κ. 563 34, Ελευθέριο Κορδελιού|2310 761 473|AgGeorgiosEleyth@imnst.gr||agios-georgios-3|1
8432|parish|Parish Church|Parish Church of Saint George, Nea Efkarpia|Ιερός Ναός Αγίου Γεωργίου Νέας Ευκαρπίας|Nea Efkarpia|Αγίου Γεωργίου 28, Τ.Κ. 564 29, Νέα Ευκαρπία|2310 680 901|AgGeorgiosEykar@imnst.gr||agios-georgios-4|1
8433|parish|Parish Church|Parish Church of Saint George, Kalochori|Ιερός Ναός Αγίου Γεωργίου Καλοχωρίου|Kalochori|Πλατεία Αγίου Γεωργίου, Τ.Κ. 570 09, Καλοχώρι|2310 753 944|aggeorgioskalox@imnst.gr|https://aggeorgioskalox.wixsite.com/home|agios-georgios-5|1
8434|parish|Parish Church|Parish Church of Saint George, Filyro|Ιερός Ναός Αγίου Γεωργίου Φιλύρου|Filyro|Κύπρου 1, Τ.Κ. 570 10, Φίλυρο|2310 677 139|AgGeorgiosFil@imnst.gr||agios-georgios-6|1
8435|parish|Parish Church|Parish Church of Saint George, Chortiatis|Ιερός Ναός Αγίου Γεωργίου Χορτιάτη|Chortiatis|Παναγίας Χορταϊτίσσης 67, Τ.Κ. 580 10, Χορτιάτης|2310 349 286,2310 349 644|AgGeorgiosHort@imnst.gr||agios-georgios-7|1
8436|parish|Parish Church|Parish Church of Saint Demetrius, Diavata|Ιερός Ναός Αγίου Δημητρίου Διαβατών|Diavata|Αγίου Γεωργίου 26, Τ.Κ. 570 08, Διαβατά|2310 781 796|agiosdimitriosdiavaton@gmail.com||agios-dimitrios|1
8437|parish|Parish Church|Parish Church of Saint Demetrius and the Exaltation of the Holy Cross, Sykies|Ιερός Ναός Αγίου Δημητρίου και Υψώσεως Τιμίου Σταυρού Συκεών|Sykies|Αγίου Δημητρίου 28, Τ.Κ. 566 25, Συκιές|2310 611 811|AgDimitriosSikies@imnst.gr||agios-dimitrios-2|1
8438|parish|Parish Church|Parish Church of Venerable Irene Chrysovalantou, Nea Efkarpia|Ιερός Ναός Οσίας Ειρήνης Χρυσοβαλάντου Νέας Ευκαρπίας|Nea Efkarpia|Ανοίξεως και Κρήνης, Συνοικισμός Μακεδονία, Τ.Κ. 564 29, Νέα Ευκαρπία|2310 689 404|osiaeirini@gmail.com,AgEiriniXrysob@imnst.gr||agia-eirini-chrysovalantou|1
8439|parish|Parish Church|Parish Church of Saint Eleftherios, Stavroupoli|Ιερός Ναός Αγίου Ελευθερίου Σταυρουπόλεως|Stavroupoli|Λαγκαδά 176, Τ.Κ. 564 29, Σταυρούπολη|2310 655 710|AgEleytherios@imnst.gr||agios-eleftherios|1
8440|parish|Parish Church|Parish Church of the Life-Giving Spring, Ampelokipoi|Ιερός Ναός Ζωοδόχου Πηγής Αμπελοκήπων|Ampelokipoi|Ζωοδόχου Πηγής 65, Τ.Κ. 561 21, Αμπελόκηποι|2310 733 260,2310 730 698,2310 720 355|ZwodoxosPigi@imnst.gr||zoodochos-pigi|1
8441|parish|Parish Church|Parish Church of the Ascension of the Lord, Polichni|Ιερός Ναός Θείας Αναλήψεως του Κυρίου Πολίχνης|Polichni|Αναλήψεως 1, Τ.Κ. 565 33, Πολίχνη|2310 655 741|i.n.theiasanalhps.pol1990@gmail.com||theia-analipsis|1
8442|parish|Parish Church|Parish Church of the Holy Theodore Martyrs, Sykies|Ιερός Ναός Αγίων Θεοδώρων Συκεών|Sykies|Καυκάσου 98, Τ.Κ. 566 25, Συκιές|2310 622 071|AgTheodoroi@imnst.gr|https://stratilates.gr/|agioi-theodoroi|1
8443|parish|Parish Church|Parish Church of the Holy Ancestors Joachim and Anna, Anthokipoi|Ιερός Ναός Αγίων Θεοπατόρων Ιωακείμ και Άννης Ανθοκήπων|Anthokipoi|Χατζηδάκη 4, Τ.Κ. 564 29, Ανθόκηποι Νέας Ευκαρπίας|2310 808 550|intheopatoron@gmail.com|https://intheopatoron.blogspot.com/|agioi-theopatores-ioakeim-anna|1
8444|parish|Parish Church|Parish Church of Saint John the Theologian, Meteora|Ιερός Ναός Αγίου Ιωάννου του Θεολόγου Μετεώρων|Meteora|Αγίου Ιωάννου Θεολόγου 38, Τ.Κ. 565 32, Μετέωρα|2310 614 256|AgIoanTheol@imnst.gr||agios-ioannis-o-theologos|1
8445|parish|Parish Church|Parish Church of Saint Joseph the Betrothed and Saint Photini, Evosmos|Ιερός Ναός Αγίου Ιωσήφ του Μνήστορος και Αγίας Φωτεινής Ευόσμου|Evosmos|Πετμεζά 1, Τ.Κ. 564 31, Εύοσμος|2310 600 835|agiosif@imnst.gr||agios-iosif-o-mnistor|1
8446|parish|Parish Church|Parish Church of Saint Kosmas the Aetolian, Evosmos|Ιερός Ναός Αγίου Κοσμά του Αιτωλού Ευόσμου|Evosmos|Δαβάκη 69, Τ.Κ. 562 24, Εύοσμος|2310 764 380|AgKosmas@imnst.gr||agios-kosmas-o-aitolos|1
8447|parish|Parish Church|Parish Church of the Dormition of the Theotokos, Pentalofos|Ιερός Ναός Κοιμήσεως της Θεοτόκου Πενταλόφου|Pentalofos|Τ.Κ. 545 32, Πεντάλοφος|2310 787 126|KoimisiPental@imnst.gr||koimiseos-theotokou|1
8448|parish|Parish Church|Parish Church of the Dormition of the Theotokos, Pefka|Ιερός Ναός Κοιμήσεως της Θεοτόκου Πεύκων|Pefka|Μικράς Ασίας 43, Τ.Κ. 570 10, Πεύκα|2310 673 402,6937 068 436|KoimisiPeyka@imnst.gr||koimiseos-theotokou-2|1
8449|parish|Parish Church|Parish Church of the Dormition of the Theotokos, Sindos|Ιερός Ναός Κοιμήσεως Θεοτόκου Σίνδου|Sindos|Τ.Κ. 574 00, Σίνδος|2310 798 155|KoimisiSindou@imnst.gr||koimiseos-theotokou-3|1
8450|parish|Parish Church|Parish Church of the Dormition of the Theotokos, Oraiokastro|Ιερός Ναός Κοιμήσεως της Θεοτόκου Ωραιοκάστρου|Oraiokastro|Βασιλέως Γεωργίου 2, Τ.Κ. 570 13, Ωραιόκαστρο|2310 696 296|KoimisiOraiok@imnst.gr||koimiseos-theotokou-4|1
8451|parish|Parish Church|Parish Church of Saints Constantine and Helen, Ilioupoli|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Ηλιουπόλεως|Ilioupoli|Κ. Κωνσταντινίδη 26, Τ.Κ. 564 31, Ηλιούπολη|2310 650 069|agkonsteleni@imnst.gr||agion-konstantinou-elenis|1
8452|parish|Parish Church|Parish Church of Saints Cyril and Methodius, Nea Politeia|Ιερός Ναός Αγίων Κυρίλλου και Μεθοδίου Νέας Πολιτείας Ευόσμου|Nea Politeia|Ολυμπιάδος και 3ης Σεπτεμβρίου, Τ.Κ. 562 24, Νέα Πολιτεία Ευόσμου|2310 558 208|kurmeth@inkme.gr||agios-kyrillos-methodios|1
8453|parish|Parish Church|Parish Church of Saint Luke the Evangelist, Stavroupoli|Ιερός Ναός Αγίου Ευαγγελιστού Λουκά Σταυρουπόλεως|Stavroupoli|Μπουμπουλίνας 90, Τ.Κ. 564 30, Σταυρούπολη|2310 652 461|AgLoukas@imnst.gr||agios-loukas|1
8454|parish|Parish Church|Parish Church of the Transfiguration of the Savior, Neo Kordelio|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Νέου Κορδελιού|Neo Kordelio|Ανδρέα Παπανδρέου 72, Τ.Κ. 563 34, Νέο Κορδελιό|2310 763 730|metamorfosi@imnst.gr||metamorfoseos-tou-sotiros|1
8455|parish|Parish Church|Parish Church of Saint Nektarios, Menemeni|Ιερός Ναός Αγίου Νεκταρίου Μενεμένης|Menemeni|Κοιμήσεως Θεοτόκου 1, Τ.Κ. 546 28, Μενεμένη|2310 762 776|AgNektarios@imnst.gr||agios-nektarios|1
8456|parish|Parish Church|Parish Church of Saint Nicholas, Xirokrini|Ιερός Ναός Αγίου Νικολάου Ξηροκρήνης|Xirokrini|Γρηγορίου Κολωνιάρη 42, Τ.Κ. 546 29, Ξηροκρήνη|2310 514 876|AgNikolKsir@imnst.gr||agios-nikolaos|1
8457|parish|Parish Church|Parish Church of Saint Nicholas, Neochorouda|Ιερός Ναός Αγίου Νικολάου Νεοχωρούδας|Neochorouda|Τ.Κ. 545 00, Νεοχωρούδα|2310787321|kourtenlis@yahoo.gr,stelioskatsifos@gmail.com||agios-nikolaos-2|1
8458|parish|Parish Church|Parish Church of All Saints, Thessaloniki|Ιερός Ναός Αγίων Πάντων Θεσσαλονίκης|Thessaloniki|Μοναστηρίου 28, Τ.Κ. 546 27, Ξηροκρήνη Θεσσαλονίκης|2310 513 977|inapthes@gmail.com||agion-panton|1
8459|parish|Parish Church|Parish Church of Saint Panteleimon, Ampelokipoi|Ιερός Ναός Αγίου Παντελεήμονος Αμπελοκήπων|Ampelokipoi|Φιλιππουπόλεως 20, Τ.Κ. 561 23, Αμπελόκηποι|2310 738 400,2310 737 403|agpantelampel@imnst.gr||agios-panteleimon|1
8460|parish|Parish Church|Parish Church of Saint Panteleimon, Nea Magnisia|Ιερός Ναός Αγίου Παντελεήμονος Νέας Μαγνησίας|Nea Magnisia|25ης Μαρτίου 36, Τ.Κ. 570 08, Νέα Μαγνησία|2310 781 592|agpantelmagn@imnst.gr||agios-panteleimon-2|1
8461|parish|Parish Church|Parish Church of Saint Panteleimon, Polichni|Ιερός Ναός Αγίου Παντελεήμονος Πολίχνης|Polichni|Σταδίου 1, Τ.Κ. 565 33, Πολίχνη|2310 654 062|AgPantelPol@imnst.gr||agios-panteleimon-3|1
8462|parish|Parish Church|Parish Church of Saint Paraskevi, Menemeni|Ιερός Ναός Αγίας Παρασκευής Μενεμένης|Menemeni|Αιμιλιανού 1, Τ.Κ. 546 28, Μενεμένη|2310 736 767|AgParaskMen@imnst.gr||agia-paraskevi|1
8463|parish|Parish Church|Parish Church of Saint Paraskevi, Xirokrini|Ιερός Ναός Αγίας Παρασκευής Ξηροκρήνης|Xirokrini|Λαγκαδά 99, Τ.Κ. 561 93, Ξηροκρήνη|2310 747 303|AgParaskKsir@imnst.gr||agia-paraskevi-2|1
8464|parish|Parish Church|Parish Church of Saint Polycarp, Menemeni|Ιερός Ναός Αγίου Πολυκάρπου Μενεμένης|Menemeni|Τέρμα Μοναστηρίου και Αγαμέμνονος, Τ.Κ. 546 21|6937 363 695|charpantidis1982@gmail.com|http://inagiospolykarpos.gr/|agios-polykarpos|1
8465|parish|Parish Church|Parish Church of Prophet Elijah, Ilioupoli|Ιερός Ναός Προφήτου Ηλιού Ηλιουπόλεως|Ilioupoli|Ευριπίδου 1, Τ.Κ. 564 31, Ηλιούπολη|2310 650 482|profitisiliasilioupolis@gmail.com||profitis-ilias|1
8466|parish|Parish Church|Parish Church of Saints Raphael, Nicholas and Irene, Ano Meteora|Ιερός Ναός Αγίων Ραφαήλ, Νικολάου και Ειρήνης Άνω Μετεώρων|Ano Meteora|Αρχή Κηφισιάς, Τ.Κ. 565 32, Άνω Μετέωρα|2310 632 396|AgRafail@imnst.gr||agioi-rafail-nikolaos-eirini|1
8467|parish|Parish Church|Parish Church of Saint Spyridon, Nikopoli|Ιερός Ναός Αγίου Σπυρίδωνος Νικόπολης Σταυρουπόλεως|Nikopoli|Άρη Βελουχιώτη 5, Τ.Κ. 564 30, Νικόπολη Σταυρουπόλεως|2310 688 268|Agspiridon@imnst.gr||agios-spyridon|1
8468|parish|Parish Church|Parish Church of Saint Seraphim of Sarov, Efxeinoupoli|Ιερός Ναός Αγίου Σεραφείμ του Σάρωφ Ευξεινουπόλεως|Efxeinoupoli|Ιασωνίδου 2, Τ.Κ. 564 29, Ευξεινούπολη|2310 685 997|agserafeim@imnst.gr||agios-serafeim-sarof|1
8469|parish|Parish Church|Parish Church of Saint Stephen, Exochi|Ιερός Ναός Αγίου Στεφάνου Εξοχής|Exochi|Αγίου Στεφάνου 19, Τ.Κ. 570 10, Εξοχή Θεσσαλονίκης|2310 359 014|AgStefanos@imnst.gr||agios-stefanos|1
8470|parish|Parish Church|Parish Church of Saints Charalambos and Christopher, Sykies|Ιερός Ναός Αγίου Χαραλάμπους και Αγίου Χριστοφόρου Συκεών|Sykies|Επταπυργίου 93, Τ.Κ. 566 25, Συκιές|2310 213 866|agharalsikies@imnst.gr||agios-charalabos|1
8471|parish|Parish Church|Parish Church of the Three Hierarchs, Evosmos|Ιερός Ναός Αγίων Τριών Ιεραρχών Ευόσμου|Evosmos|Βόλβης και Τριών Ιεραρχών, Τ.Κ. 562 24, Εύοσμος|2310 708 802,2310 704 736|treisierarxesevosmou@gmail.com||trion-ierarchon|1
8472|parish|Parish Church|Parish Church of the Exaltation of the Holy Cross, Dialogi|Ιερός Ναός Υψώσεως του Τιμίου Σταυρού Διαλογής Νέου Κορδελιού|Dialogi|Τιμίου Σταυρού 1, Τ.Κ. 546 28, Διαλογή Νέου Κορδελιού|2310 762 177|TimiosStaurosDial@imnst.gr||ypsoseos-timou-stavrou|1
8473|parish|Parish Church|Parish Church of the Exaltation of the Holy Cross, Oraiokastro|Ιερός Ναός Υψώσεως του Τιμίου Σταυρού Ωραιοκάστρου|Oraiokastro|Τ.Κ. 570 13, Ωραιόκαστρο|2310 697 286|TimiosStaurosOraiok@imnst.gr||ypsoseos-timou-stavrou-2|1
8484|parish|Parish Church|Parish Church of the Annunciation of the Theotokos, Evosmos|Ιερός Ναός Αγίου Αθανασίου και Ευαγγελισμού της Θεοτόκου Ευόσμου|Evosmos|Εύοσμος|2310 761 325,2310 706 777|AgAthanEyosmou@imnst.gr,info@katakomvi.gr|https://www.katakomvi.gr/|evangelismos-tis-theotokou|1
8474|parish|Station Church|Station Church of Saint Philip the Deacon, Thessaloniki|Ιερός Ναός Αγίου Αποστόλου Φιλίππου του Διακόνου|Thessaloniki Railway Station|Μοναστηρίου 21, Τ.Κ. 546 27, Θεσσαλονίκη|2310 511 715|||agios-filippos|
8475|parish|Chapel|Chapel of Saint Kyriaki, Menemeni|Παρεκκλήσιο Αγίας Κυριακής Βοσπόρου|Menemeni|Μπουμπουλίνας 28, Μενεμένη||||agia-kyriaki|
8476|parish|Hospital Chapel|Hospital Chapel of the Nativity of the Theotokos, Exochi|Ιερό Παρεκκλήσιο Γενεσίου της Θεοτόκου Νοσοκομείου Παπανικολάου Εξοχής|Exochi|Νοσοκομείο Παπανικολάου, Τ.Κ. 566 01, Εξοχή|6933 173 798|||genesio-theotokou|
8477|parish|Chapel|Chapel of the Holy Trinity, Pefka|Παρεκκλήσιο Αγίας Τριάδος Πεύκων|Pefka|Αγίας Τριάδος 51, Τ.Κ. 570 10, Πεύκα||||agios-georgios-8|
8478|parish|Holy Water Chapel|Holy Water Chapel of Saint John the Forerunner, Nea Efkarpia|Αγίασμα Τιμίου Προδρόμου Νέας Ευκαρπίας|Nea Efkarpia|Αγίου Ιωάννου, Τ.Κ. 564 29, Νέα Ευκαρπία|2310 681 098|||agios-georgios-9|
8479|parish|Institutional Chapel|Institutional Chapel of Saint Panteleimon, Stavroupoli|Ιερό Παρεκκλήσιο Αγίου Παντελεήμονος Ιδρύματος Κοινωνικής Πρόνοιας|Stavroupoli|Οδός Λαγκαδά, Σταυρούπολη|2313 320 063|||agios-panteleimon-4|
8480|parish|Institutional Church|Institutional Church of the Holy Unmercenaries, Nea Efkarpia|Ιερός Ναός Αγίων Αναργύρων Θεραπευτηρίου Χρόνιων Παθήσεων|Nea Efkarpia|7ο χλμ. Οδού Λαγκαδά, Τ.Κ. 564 29, Θεσσαλονίκη||||agion-anargyron|
8481|parish|Cemetery Church|Cemetery Church of the Holy Archangels, Evosmos|Κοιμητηριακός Ναός Παμμεγίστων Ταξιαρχών Ευόσμου|Evosmos|Αναπαύσεως 1, Τ.Κ. 562 24, Εύοσμος|6972 177 764||https://koimitiriaevosmou.gr/|pammegiston-taxiarchon|
8482|parish|University Chapel|University Chapel of the Three Hierarchs, Sindos|Ιερό Παρεκκλήσιο Τριών Ιεραρχών ΔΙΠΑΕ Σίνδου|Sindos|ΔΙΠΑΕ, Τ.Θ. 14561, Τ.Κ. 541 01, Σίνδος|2310 791 101|||trion-ierarchon-2|
8483|parish|Metropolitan Chapel|Metropolitan Chapel of Saint Demetrius, Polichni|Ιερό Μητροπολιτικό Παρεκκλήσιο Αγίου Δημητρίου|Polichni|Πρώην Στρατόπεδο Καρατάσου, Πολίχνη|2310 222 201|||agios-dimitrios-3|
13049|parish|Chapel|Chapel of Saint John the Russian, Sykies|Ιερό Παρεκκλήσιο Αγίου Ιωάννου του Ρώσου|Sykies|Καυκάσου 97, Τ.Κ. 566 25, Συκιές||||@13049|
13053|parish|Port Chapel|Port Chapel of Saint Nicholas, Thessaloniki|Ιερό Παρεκκλήσιο Αγίου Νικολάου Λιμένος Θεσσαλονίκης|Port of Thessaloniki|Λιμένας Θεσσαλονίκης||||@13053|
13113|parish|Holy Water Chapel|Holy Water Chapel of Saint Paraskevi, Palaiokastro|Ιερό Παρεκκλήσιο Αγίας Παρασκευής Παλαιοκάστρου|Palaiokastro|Παλαιόκαστρο||||@13113|
13056|monastery|Monastery|Nativity of the Theotokos Panagia Gorgoepikoos Monastery, Ionia|Ιερά Μονή Γενεσίου της Θεοτόκου Παναγίας Γοργοεπηκόου Ιωνίας|Ionia|Πίσω από τη ΣΙΔΕΝΟΡ, Τ.Κ. 570 08, Τ.Θ. 1626|2310 722 020|impanagias@yahoo.gr||@13056|
13059|monastery|Monastery|Transfiguration of the Savior Monastery, Chortiatis|Ιερά Μονή Μεταμορφώσεως του Σωτήρος Χορτιάτη|Chortiatis|Τ.Κ. 580 10, Χορτιάτης|2310 349 388|||@13059|
13062|monastery|Monastery|Holy Trinity Monastery, Nea Efkarpia|Ιερά Μονή Αγίας Τριάδος Νέας Ευκαρπίας|Nea Efkarpia|Τ.Κ. 564 29, Νέα Ευκαρπία|2310 680 975|||@13062|
'''


# source product id|key|rank|English name|Greek local name|English seat|
# Greek address or exact placement|live markers
DEPENDENT_SOURCE = r'''
8421|james-brother-lord|Chapel|Chapel of Saint James the Brother of the Lord, Neapoli|Παρεκκλήσιο Αγίου Ιακώβου του Αδελφοθέου|Neapoli|Εντός του Ιερού Μητροπολιτικού Ναού Αγίου Γεωργίου Νεαπόλεως|Άγιο Ιάκωβο τον Αδελφόθεο
8423|archangels-ossuary|Chapel|Chapel of the Holy Archangels and Ossuary, Evosmos|Παρεκκλήσιο των Ταξιαρχών με το οστεοφυλάκιο|Evosmos|Πρώην Κοιμητήρια Ευόσμου|Παρεκκλήσιο των Ταξιαρχών
8424|tryphon|Chapel|Chapel of Saint Tryphon, Nea Magnisia|Παρεκκλήσιο Αγίου Τρύφωνος|Nea Magnisia|Εξωτερικό περιστύλιο του Ιερού Ναού Αγίου Αθανασίου Νέας Μαγνησίας|Παρεκκλήσιο του Αγίου Τρύφωνος
8431|catherine|Chapel|Chapel of Saint Catherine, Eleftherio|Παρεκκλήσιο Αγίας Αικατερίνης|Eleftherio|Πρόναος του Ιερού Ναού Αγίου Γεωργίου Ελευθερίου|Παρεκκλήσιο της Αγίας Αικατερίνης
8431|three-hierarchs|Chapel|Chapel of the Three Hierarchs, Eleftherio|Παρεκκλήσιο Τριών Ιεραρχών|Eleftherio|Βόρεια πλευρά του Ιερού Ναού Αγίου Γεωργίου Ελευθερίου|Παρεκκλήσιο των Τριών Ιεραρχών
8431|photini|Chapel|Chapel of Saint Photini the Samaritan, Eleftherio|Παρεκκλήσιο Αγίας Φωτεινής της Σαμαρείτιδος|Eleftherio|Κατακόμβη του Ιερού Ναού Αγίου Γεωργίου Ελευθερίου|Αγία Φωτεινή τη Σαμαρείτιδα
8432|anastasia-roman|Chapel|Chapel of Saint Anastasia the Roman, Nea Efkarpia|Παρεκκλήσιο Αγίας Αναστασίας της Ρωμαίας|Nea Efkarpia|Κατακόμβη του Ιερού Ναού Αγίου Γεωργίου Νέας Ευκαρπίας|Αγίας Αναστασίας της Ρωμαίας
8432|john-chrysostom|Chapel|Chapel of Saint John Chrysostom, Nea Efkarpia|Παρεκκλήσιο Ιερού Χρυσοστόμου|Nea Efkarpia|Αριστερό κλίτος του Ιερού Ναού Αγίου Γεωργίου Νέας Ευκαρπίας|Ιερού Χρυσοστόμου
8432|peter-paul|Chapel|Chapel of Saints Peter and Paul, Nea Efkarpia|Παρεκκλήσιο Αγίων Αποστόλων Πέτρου και Παύλου|Nea Efkarpia|Νέα Ευκαρπία|Αγίων Αποστόλων Πέτρου και Παύλου
8432|constantine-helen|Chapel|Chapel of Saints Constantine and Helen, Nea Efkarpia|Παρεκκλήσιο Αγίων Κωνσταντίνου και Ελένης|Nea Efkarpia|Νέα Ευκαρπία|Αγίων Κωνσταντίνου και Ελένης
8434|nikanor-forest|Country Chapel|Country Chapel of Saint Nikanor, Filyro Forest|Παρεκκλήσιο Αγίου Νικάνορος|Filyro|Δάσος Φιλύρου|Αγίου Νικάνορος
8434|lazarus-old-cemetery|Cemetery Chapel|Chapel of Saint Lazarus, Old Cemetery of Filyro|Παρεκκλήσιο Αγίου Λαζάρου|Filyro|Παλαιά κοιμητήρια Φιλύρου|Αγίου Λαζάρου
8434|prophet-elijah-hill|Country Chapel|Country Chapel of Prophet Elijah, Filyro Hill|Παρεκκλήσιο Προφήτου Ηλιού|Filyro|Λόφος Φιλύρου|Προφήτη Ηλία
8434|febronia-new-cemetery|Cemetery Chapel|Chapel of Saint Febronia, New Cemetery of Filyro|Παρεκκλήσιο Αγίας Φεβρωνίας|Filyro|Νέα κοιμητήρια Φιλύρου|Αγίας Φεβρωνίας
8436|old-saint-demetrius|Historic Worship Church|Old Church of Saint Demetrius, Diavata|Παλαιός Ιερός Ναός Αγίου Δημητρίου Διαβατών|Diavata|Αγίου Γεωργίου 26, Τ.Κ. 570 08, Διαβατά|σε πλήρη λειτουργία
8436|nicholas-new-cemetery|Cemetery Chapel|Chapel of Saint Nicholas, New Cemetery of Diavata|Παρεκκλήσιο Αγίου Νικολάου|Diavata|Νέα Κοιμητήρια Διαβατών, Υψώματα Διαβατών|Παρεκκλήσιο αφιερωμένο στον Άγιο Νικόλαο
8436|paraskevi-papavasileiou|Chapel|Chapel of Saint Paraskevi, Former Papavasileiou Camp|Παρεκκλήσιο Αγίας Παρασκευής|Diavata|Πρώην Στρατόπεδο Παπαβασιλείου, Διαβατά|Παρεκκλήσι της Αγίας Παρασκευής
8437|alexander|Chapel|Chapel of Saint Alexander, Sykies|Παρεκκλήσιο Αγίου Αλεξάνδρου|Sykies|Εντός του Ιερού Ναού Αγίου Δημητρίου και Υψώσεως Τιμίου Σταυρού Συκεών|παρεκκλήσιο του Αγίου Αλεξάνδρου
8438|menas|Chapel|Chapel of Saint Menas, Nea Efkarpia|Παρεκκλήσιο Αγίου Μηνά|Nea Efkarpia|Ενορία Οσίας Ειρήνης Χρυσοβαλάντου Νέας Ευκαρπίας|Αγίου Μηνά
8438|paraskevi|Chapel|Chapel of Saint Paraskevi, Nea Efkarpia|Παρεκκλήσιο Αγίας Παρασκευής|Nea Efkarpia|Ενορία Οσίας Ειρήνης Χρυσοβαλάντου Νέας Ευκαρπίας|Αγίας Παρασκευής
8438|athanasius|Chapel|Chapel of Saint Athanasius, Nea Efkarpia|Παρεκκλήσιο Αγίου Αθανασίου|Nea Efkarpia|Ενορία Οσίας Ειρήνης Χρυσοβαλάντου Νέας Ευκαρπίας|Αγίου Αθανασίου
8439|nestor|Chapel|Chapel of Saint Nestor, Stavroupoli|Παρεκκλήσιο Αγίου Νέστορος|Stavroupoli|Πνευματικό Κέντρο Κιβωτός, Σταυρούπολη|παρεκκλήσι του Αγίου Νέστορος
8440|euphemia-holy-water|Holy Water Chapel|Holy Water Chapel of Saint Euphemia, Ampelokipoi|Αγίασμα Αγίας Μεγαλομάρτυρος Ευφημίας|Ampelokipoi|Ιερός Ναός Ζωοδόχου Πηγής Αμπελοκήπων|Αγίας Μεγαλομάρτυρος Ευφημίας
8442|panteleimon|Chapel|Chapel of Saint Panteleimon, Sykies|Παρεκκλήσιο Αγίου Παντελεήμονος|Sykies|Εντός του Ιερού Ναού Αγίων Θεοδώρων Συκεών|εσωτερικό του Αγίου Παντελεήμονος
8443|forerunner|Chapel|Chapel of Saint John the Forerunner, Anthokipoi|Παρεκκλήσιο Τιμίου Προδρόμου|Anthokipoi|Ιερός Ναός Αγίων Θεοπατόρων Ιωακείμ και Άννης Ανθοκήπων|Παρεκκλήσι του Τιμίου Προδρόμου
8447|prophet-elijah-historic|Historic Worship Church|Historic Chapel of Prophet Elijah, Pentalofos|Ιστορικό Παρεκκλήσιο Προφήτου Ηλιού|Pentalofos|Πεντάλοφος|Προφήτη Ηλία: Ιστορικό
8447|george-athanasius|Chapel|Chapel of Saint George and Saint Athanasius the Athonite, Pentalofos|Παρεκκλήσιο Αγίου Γεωργίου και Αγίου Αθανασίου του Αθωνίτου|Pentalofos|Πεντάλοφος|Αγίου Γεωργίου και Αγίου Αθανασίου
8447|prophet-elijah-holy-water|Holy Water Chapel|Holy Water Chapel of Prophet Elijah, Pentalofos|Αγίασμα Προφήτου Ηλιού|Pentalofos|Πεντάλοφος|Προφήτη Ηλία (Αγίασμα)
8447|lazarus-cemetery|Cemetery Chapel|Cemetery Chapel of Saint Lazarus, Pentalofos|Κοιμητηριακό Παρεκκλήσιο Αγίου Λαζάρου|Pentalofos|Κοιμητήρια Πενταλόφου|Αγίου Λαζάρου (Κοιμητηριακό)
8448|phanourios|Chapel|Chapel of Saint Phanourios, Pefka|Παρεκκλήσιο Αγίου Φανουρίου|Pefka|Λεωφόρος Παπανικολάου, Πεύκα|Αγίου Φανουρίου
8448|george|Chapel|Chapel of Saint George, Pefka|Παρεκκλήσιο Αγίου Γεωργίου|Pefka|Έμπροσθεν του Ιερού Ναού Κοιμήσεως της Θεοτόκου Πεύκων|Αγίου Γεωργίου
8448|holy-cross|Chapel|Chapel of the Holy Cross, Pefka|Παρεκκλήσιο Τιμίου Σταυρού|Pefka|Ισαύρων και Σμύρνης, Πεύκα|Τιμίου Σταυρού
8449|raphael-nicholas-irene|Chapel|Chapel of Saints Raphael, Nicholas and Irene, Sindos|Παρεκκλήσιο Αγίων Ραφαήλ, Νικολάου και Ειρήνης|Sindos|Σίνδος|Αγίων Ραφαήλ, Νικολάου και Ειρήνης
8451|barnabas|Chapel|Chapel of Apostle Barnabas, Ilioupoli|Παρεκκλήσιο Αποστόλου Βαρνάβα|Ilioupoli|Εντός του Ιερού Ναού Αγίων Κωνσταντίνου και Ελένης Ηλιουπόλεως|Αποστόλου Βαρνάβα
8451|maximus-confessor|Chapel|Chapel of Saint Maximus the Confessor, Ilioupoli|Παρεκκλήσιο Αγίου Μαξίμου του Ομολογητού|Ilioupoli|Εντός του Ιερού Ναού Αγίων Κωνσταντίνου και Ελένης Ηλιουπόλεως|Αγίου Μαξίμου του Ομολογητού
8453|nektarios|Chapel|Chapel of Saint Nektarios of Pentapolis, Stavroupoli|Παρεκκλήσιο Αγίου Νεκταρίου Επισκόπου Πενταπόλεως|Stavroupoli|Εντός του Ιερού Ναού Αγίου Λουκά Σταυρουπόλεως|Αγίου Νεκταρίου Επισκόπου Πενταπόλεως
8454|irene-chrysovalantou|Chapel|Chapel of Venerable Irene Chrysovalantou, Neo Kordelio|Παρεκκλήσιο Αγίας Ειρήνης Χρυσοβαλάντου|Neo Kordelio|Εντός του Ιερού Ναού Μεταμορφώσεως του Σωτήρος Νέου Κορδελιού|Αγίας Ειρήνης Χρυσοβαλάντου
8457|paraskevi-holy-water|Holy Water Chapel|Holy Water Chapel of Saint Paraskevi, Neochorouda|Αγίασμα Αγίας Παρασκευής|Neochorouda|Νεοχωρούδα|Αγίας Παρασκευής (Αγίασμα)
8457|george|Chapel|Chapel of Saint George, Neochorouda|Παρεκκλήσιο Αγίου Γεωργίου|Neochorouda|Νεοχωρούδα|του Αγίου Γεωργίου
8457|demetrius|Chapel|Chapel of Saint Demetrius, Neochorouda|Παρεκκλήσιο Αγίου Δημητρίου|Neochorouda|Νεοχωρούδα|του Αγίου Δημητρίου
8458|tryphon|Chapel|Chapel of Saint Tryphon, Thessaloniki|Παρεκκλήσιο Αγίου Τρύφωνος|Thessaloniki|Εντός του Ιερού Βήματος του Ιερού Ναού Αγίων Πάντων Θεσσαλονίκης|παρεκκλήσιο αφιερωμένο στον Άγιο Τρύφωνα
8460|arsenios-cappadocian|Chapel|Chapel of Saint Arsenios the Cappadocian, Nea Magnisia|Παρεκκλήσιο Αγίου Αρσενίου του Καππαδόκη|Nea Magnisia|Ιερός Ναός Αγίου Παντελεήμονος Νέας Μαγνησίας|Άγιο Αρσένιο τον Καππαδόκη
8460|matrona-nicholas|Chapel|Chapel of Saint Matrona the Blind and Saint Nicholas of Magnisia|Παρεκκλήσιο Αγίας Ματρώνας της Αόμματης και Αγίου Νικολάου του εν Μαγνησία|Nea Magnisia|Ιερός Ναός Αγίου Παντελεήμονος Νέας Μαγνησίας|Αγία Ματρώνα την Αόμματο
8461|entry-theotokos|Chapel|Chapel of the Entry of the Theotokos, Polichni|Παρεκκλήσιο Εισοδίων της Θεοτόκου|Polichni|Εντός του Ιερού Ναού Αγίου Παντελεήμονος Πολίχνης|Εισοδίων της Θεοτόκου
8461|cyril-methodius|Chapel|Chapel of Saints Cyril and Methodius, Polichni|Παρεκκλήσιο Αγίων Κυρίλλου και Μεθοδίου|Polichni|Εντός του Ιερού Ναού Αγίου Παντελεήμονος Πολίχνης|Αγίων Κυρίλλου και Μεθοδίου
8461|kyriaki|Chapel|Chapel of Saint Kyriaki, Polichni|Παρεκκλήσιο Αγίας Κυριακής|Polichni|Εντός του Ιερού Ναού Αγίου Παντελεήμονος Πολίχνης|Αγίας Κυριακής
8465|stylianos|Chapel|Chapel of Saint Stylianos, Ilioupoli|Παρεκκλήσιο Αγίου Στυλιανού|Ilioupoli|Περιβάλλων χώρος του Ιερού Ναού Προφήτου Ηλιού Ηλιουπόλεως|Αγίου Στυλιανού
8465|demetrius|Chapel|Chapel of Saint Demetrius, Ilioupoli|Παρεκκλήσιο Αγίου Δημητρίου|Ilioupoli|Περιβάλλων χώρος του Ιερού Ναού Προφήτου Ηλιού Ηλιουπόλεως|Αγίου Δημητρίου
8471|mothers-three-hierarchs|Chapel|Chapel of the Mothers of the Three Hierarchs, Evosmos|Παρεκκλήσιο Μητέρων των Τριών Ιεραρχών Εμμέλειας, Νόννας και Ανθούσας|Evosmos|Ιερός Ναός Τριών Ιεραρχών Ευόσμου|Μητέρων των Τριών Ιεραρχών
8471|demetrius|Chapel|Chapel of Saint Demetrius, Evosmos|Παρεκκλήσιο Αγίου Δημητρίου|Evosmos|Εξωτερικά του Ιερού Ναού Τριών Ιεραρχών Ευόσμου|του Αγίου Δημητρίου (εξωτερικά)
8471|barnabas|Chapel|Chapel of Saint Barnabas, Evosmos|Παρεκκλήσιο Αγίου Βαρνάβα|Evosmos|Πνευματικό Κέντρο Βασιλειάδα, Εύοσμος|του Αγίου Βαρνάβα
8472|ephraim-nea-makri|Chapel|Chapel of Saint Ephraim of Nea Makri, Dialogi|Παρεκκλήσιο Αγίου Εφραίμ Νέας Μάκρης|Dialogi|Ενορία Υψώσεως του Τιμίου Σταυρού Διαλογής|Παρεκκλήσιο του Αγίου Εφραίμ Νέας Μάκρης
8472|kyriakos-anna|Chapel|Chapel of Hieromartyr Kyriakos and his Mother Anna, Dialogi|Παρεκκλήσιο Αγίου Ιερομάρτυρος Κυριακού και της μητρός αυτού Άννης|Dialogi|Ενορία Υψώσεως του Τιμίου Σταυρού Διαλογής|Παρεκκλήσιο του Αγίου Ιερομάρτυρος Κυριακού
8473|galini|Chapel|Chapel of Saint Galini, Oraiokastro|Παρεκκλήσιο Αγίας Γαλήνης|Oraiokastro|Υπόγειο του Ιερού Ναού Υψώσεως του Τιμίου Σταυρού Ωραιοκάστρου|παρεκκλήσιο της Αγίας Γαλήνης
8484|constantine-helen|Chapel|Chapel of Saints Constantine and Helen, Evosmos|Παρεκκλήσιο Αγίων Κωνσταντίνου και Ελένης|Evosmos|Εντός του Ιερού Ναού Ευαγγελισμού της Θεοτόκου Ευόσμου|Αγίων Κωνσταντίνου και Ελένης
8484|dionysius-metrophanes|Chapel|Chapel of Venerable Dionysius the Orator and Metrophanes, Evosmos|Παρεκκλήσιο Οσίων Διονυσίου του Ρήτορος και Μητροφάνους|Evosmos|Εντός του Ιερού Ναού Ευαγγελισμού της Θεοτόκου Ευόσμου|Οσίων Διονυσίου του Ρήτορος και Μητροφάνους
8484|david-thessaloniki|Chapel|Chapel of Venerable David of Thessaloniki, Evosmos|Παρεκκλήσιο Οσίου Δαυίδ του εν Θεσσαλονίκη|Evosmos|Εντός του Ιερού Ναού Ευαγγελισμού της Θεοτόκου Ευόσμου|Οσίου Δαυίδ του εν Θεσσαλονίκη
'''


def split_values(value, separator=","):
    return [item.strip() for item in value.split(separator) if item.strip()]


def detail_url(product_id, token):
    if token.startswith("@"):
        return "https://imnst.gr/?post_type=product&p=%s" % product_id
    return "https://imnst.gr/naos/%s/" % token


def primary_rows():
    rows = []
    markers = {}
    legal_ids = set()
    for number, raw in enumerate(
            (line for line in PRIMARY_SOURCE.splitlines() if line.strip()), 1):
        parts = raw.split("|")
        if len(parts) != 12:
            raise ValueError("invalid primary source row: %s" % raw)
        (product_id, kind, rank, name, local, seat, address, phones_text,
         emails_text, site, token, legal) = parts
        product_id = int(product_id)
        source = detail_url(product_id, token)
        row_id = "gr-ep-neapolis-stavroupolis-%03d-%s" % (
            number, re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")
        )
        item = {
            "id": row_id,
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": [source],
            "detail": source,
            "source_product_id": product_id,
        }
        if legal:
            item["sources"].append(OFFICIAL_PDF)
            item["legal_roster"] = True
            legal_ids.add(product_id)
        phones = split_values(phones_text)
        emails = split_values(emails_text)
        if phones:
            item["phones"] = phones
        if emails:
            item["emails"] = emails
        if site:
            item["site"] = site
        if phones or emails or site:
            item["contact_sources"] = [source]
            item["contact_checked"] = CHECKED
        rows.append(item)
        local_parts = [part.strip() for part in re.split(r"[, ]+", local)
                       if len(part.strip()) > 5]
        marker_overrides = {
            8425: ["ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ", "ΠΑΛΑΙΟΚΑΣΤΡΟ"],
            8457: ["ΑΓΙΟΣ ΝΙΚΟΛΑΟΣ", "ΝΕΟΧΩΡΟΥΔΑ"],
        }
        markers[row_id] = marker_overrides.get(
            product_id, local_parts[-2:] or [local]
        )
    if len(rows) != 70:
        raise ValueError("expected 70 live primary detail records")
    if len(legal_ids) != 54:
        raise ValueError("expected 54 legal parish records")
    return rows, markers, legal_ids


def dependent_rows(start_number, primary_by_product):
    rows = []
    markers = {}
    for offset, raw in enumerate(
            (line for line in DEPENDENT_SOURCE.splitlines() if line.strip())):
        parts = raw.split("|")
        if len(parts) != 8:
            raise ValueError("invalid dependent source row: %s" % raw)
        (product_text, key, rank, name, local, seat, address,
         marker_text) = parts
        product_id = int(product_text)
        parent_row = primary_by_product[product_id]
        source = parent_row["detail"]
        row_id = "gr-ep-neapolis-stavroupolis-%03d-%s" % (
            start_number + offset, key
        )
        rows.append({
            "id": row_id,
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": [source],
            "detail": source,
            "source_product_id": product_id,
            "dependent_worship_space": True,
        })
        markers[row_id] = [marker_text]
    if len(rows) != 57:
        raise ValueError("expected 57 exact dependent worship spaces")
    return rows, markers


PRIMARY_ROWS, PRIMARY_MARKERS, LEGAL_PRODUCT_IDS = primary_rows()
PRIMARY_BY_PRODUCT = {row["source_product_id"]: row for row in PRIMARY_ROWS}
DEPENDENT_ROWS, DEPENDENT_MARKERS = dependent_rows(
    len(PRIMARY_ROWS) + 1, PRIMARY_BY_PRODUCT
)
ROWS = PRIMARY_ROWS + DEPENDENT_ROWS
LIVE_MARKERS = dict(PRIMARY_MARKERS)
LIVE_MARKERS.update(DEPENDENT_MARKERS)

ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 127
EXPECTED_OWNER_COUNTS = {PARENT: 127}
EXPECTED_KINDS = {"monastery": 3, "parish": 124}
EXPECTED_PRIMARY_PRODUCTS = 70
EXPECTED_LEGAL_PARISHES = 54
EXPECTED_DEPENDENT_ROWS = 57
EXPECTED_CONTACT_BODIES = 64
EXPECTED_PHONE_BODIES = 64
EXPECTED_PHONE_VALUES = 73
EXPECTED_EMAIL_BODIES = 55
EXPECTED_EMAIL_VALUES = 58
EXPECTED_SITE_BODIES = 10
EXPECTED_ADDRESS_BODIES = 127
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
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value.casefold()).strip()


def validate_url(value, label):
    parsed = urlparse(value)
    allowed_hosts = {
        "imnst.gr", "www.imnst.gr", "ec-patr.org",
        "ecclesiagreece.gr", "www.ecclesiagreece.gr",
        "www.e-nomothesia.gr", "www.katakomvi.gr",
        "inaap.wordpress.com", "naosagiasbarbaras.gr",
        "agiosgeorgiosasvestohori.gr",
        "aggeorgioskalox.wixsite.com", "stratilates.gr",
        "intheopatoron.blogspot.com", "inagiospolykarpos.gr",
        "koimitiriaevosmou.gr",
    }
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in allowed_hosts:
        raise ValueError("%s carries an unreviewed source: %s"
                         % (label, value))
    if parsed.scheme == "http" and parsed.netloc != "inagiospolykarpos.gr":
        raise ValueError("%s has an avoidable insecure URL: %s"
                         % (label, value))


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
    has_contact = bool(
        item.get("phones") or item.get("emails") or item.get("site")
    )
    if has_contact and not contact_sources:
        raise ValueError("%s lacks contact provenance" % item.get("id"))
    if contact_sources:
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError("%s contact source is outside identity sources"
                                 % item.get("id"))
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date"
                             % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Neapolis and Stavroupolis ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Neapolis and Stavroupolis ledger date drifted")
    expected_summary = {
        PARENT: 127,
        "total": 127,
        "live_primary_detail_records": 70,
        "regulated_parish_rows": 54,
        "exact_dependent_worship_rows": 57,
        "parish_kind_rows": 124,
        "monastery_kind_rows": 3,
        "contact_bodies": 64,
        "phone_bodies": 64,
        "public_phone_values": 73,
        "email_bodies": 55,
        "public_email_values": 58,
        "body_owned_sites": 10,
        "address_bodies": 127,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Neapolis and Stavroupolis ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 4:
                raise ValueError("ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("candidate ledger has forbidden punctuation")
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
        if not item.get("rank") or not item.get("name"):
            raise ValueError("%s lacks rank or English name" % row_id)
        if not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks Greek name or seat" % row_id)
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
        signature = (parent, unicase(item["local"]), unicase(item["address"][0]))
        if signature in signatures:
            raise ValueError("%s duplicates %s after normalization"
                             % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d"
                         % (EXPECTED_TOTAL, len(result)))
    if len(PRIMARY_ROWS) != EXPECTED_PRIMARY_PRODUCTS:
        raise ValueError("primary product count drifted")
    if len(LEGAL_PRODUCT_IDS) != EXPECTED_LEGAL_PARISHES:
        raise ValueError("legal parish count drifted")
    if len(DEPENDENT_ROWS) != EXPECTED_DEPENDENT_ROWS:
        raise ValueError("dependent worship count drifted")
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("kind totals drifted")
    if sum(rank_counts.values()) != EXPECTED_TOTAL:
        raise ValueError("rank totals drifted")
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
        raise ValueError("contact coverage drifted: %r" % (coverage,))
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
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def normalize_source_blob(value):
    value = html.unescape(value).replace("\u00a0", " ")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_json(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=60) as response:
        content_type = response.headers.get("Content-Type", "").lower()
        if response.status >= 400 or "json" not in content_type:
            raise ValueError("unexpected response for %s: %s %s" % (
                url, response.status, content_type
            ))
        return json.loads(response.read().decode("utf-8"))


def fetch_blob(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=60) as response:
        if response.status >= 400:
            raise ValueError("HTTP %s for %s" % (response.status, url))
        try:
            blob = response.read()
        except IncompleteRead as exc:
            blob = exc.partial
        return response.headers, blob


def check_live_sources():
    products = fetch_json(LOCAL_REST)
    product_ids = {int(product["id"]) for product in products}
    expected_ids = {row["source_product_id"] for row in PRIMARY_ROWS}
    if len(products) != 70 or product_ids != expected_ids:
        raise ValueError("live Metropolis product roster drifted")
    by_id = {int(product["id"]): product for product in products}
    categories = fetch_json(LOCAL_CATEGORY_REST)
    category_counts = {int(item["id"]): int(item["count"])
                       for item in categories}
    if category_counts.get(219) != 3 or category_counts.get(220) != 13:
        raise ValueError("live monastery or chapel category total drifted")
    top_parish_categories = {155, 157, 159, 161, 163, 166, 169, 186}
    parish_products = {
        int(product["id"]) for product in products
        if top_parish_categories.intersection(product.get("product_cat") or [])
    }
    if len(parish_products) != 54 or parish_products != LEGAL_PRODUCT_IDS:
        raise ValueError("live 54-row parish category roster drifted")
    marker_failures = []
    contact_failures = []
    for row in ROWS:
        product = by_id[row["source_product_id"]]
        raw = json.dumps(product, ensure_ascii=False)
        text = normalize_source_text(raw)
        blob = normalize_source_blob(raw)
        missing = [
            marker for marker in LIVE_MARKERS[row["id"]]
            if normalize_source_text(marker) not in text
        ]
        if missing:
            marker_failures.append((row["id"], missing))
        for field in ("phones", "emails"):
            for value in row.get(field) or []:
                if normalize_source_blob(value) not in blob:
                    contact_failures.append((row["id"], field, value))
    if marker_failures:
        raise ValueError("live exact-source marker check failed: %r"
                         % marker_failures)
    if contact_failures:
        raise ValueError("live contact marker check failed: %r"
                         % contact_failures)
    ep_headers, ep_blob = fetch_blob(PATRIARCHATE_PAGE)
    if "html" not in ep_headers.get("Content-Type", "").lower():
        raise ValueError("Patriarchate page returned non-HTML content")
    ep_text = normalize_source_text(ep_blob.decode("utf-8", "replace"))
    for marker in ("ενοριακοι ναοι : 53", "παρεκκλησια: 36",
                   "εξωκκλησια: 12", "ιδιωτικοι ναοι: 5",
                   "2310-722.020", "2310-349.388", "2310-680.975"):
        if normalize_source_text(marker) not in ep_text:
            raise ValueError("Patriarchate marker missing: %s" % marker)
    pdf_headers, pdf_blob = fetch_blob(OFFICIAL_PDF)
    if not pdf_blob.startswith(b"%PDF") or len(pdf_blob) < 1000000:
        raise ValueError("Church of Greece legal PDF is not live")
    pdf_type = pdf_headers.get("Content-Type", "").lower()
    if "pdf" not in pdf_type and "octet-stream" not in pdf_type:
        raise ValueError("legal source returned unexpected content type")
    for site in sorted({row.get("site") for row in ROWS if row.get("site")}):
        site_headers, site_blob = fetch_blob(site)
        site_type = site_headers.get("Content-Type", "").lower()
        if "html" not in site_type or len(site_blob) < 100:
            raise ValueError("body-associated site is not live: %s" % site)


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
    elif args.check_live:
        print("Neapolis and Stavroupolis directory sources: OK "
              "(%d bodies, %d contact bodies)" % (
                  EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES
              ))
    else:
        print("Neapolis and Stavroupolis directory: OK "
              "(%d bodies, %d primary records, %d dependent spaces)" % (
                  EXPECTED_TOTAL, EXPECTED_PRIMARY_PRODUCTS,
                  EXPECTED_DEPENDENT_ROWS
              ))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
