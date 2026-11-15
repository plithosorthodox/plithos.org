# -*- coding: utf-8 -*-
"""Exact named bodies of the Metropolis of Serres and Nigrita.

The Metropolis publishes 126 numbered church profiles. Their numbering
resolves exactly into 118 parish profiles, six chapel profiles, and two
cemetery church profiles. The current monastery page and the Ecumenical
Patriarchate's current yearbook supply five active monasteries and the exact
named monastic dependencies. The former Holy Spirit monastery is retained as
a historic monastery church, not counted as an active monastery. Personal
clergy mobile numbers are not published here.
"""

from __future__ import print_function

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse


PARENT = "ep-serres"
CHECKED = "2026-11-15"
CANDIDATE_LEDGER = (
    Path(__file__).resolve().parent
    / "directory_candidates"
    / "serres_country.json"
)

HOME = "https://www.imsn.gr/"
CHURCH_CATEGORY = "https://www.imsn.gr/category/mitropoli/naoi/"
CHURCH_API = (
    "https://www.imsn.gr/wp-json/wp/v2/posts?categories=28&per_page=100&page=1"
)
MONASTERY_PAGE = (
    "https://www.imsn.gr/"
    "%CE%B9%CE%B5%CF%81%CE%AD%CF%82-%CE%BC%CE%BF%CE%BD%CE%AD%CF%82/"
)
ADMINISTRATION_PAGE = (
    "https://www.imsn.gr/"
    "%CE%B4%CE%B9%CE%BF%CE%B9%CE%BA%CE%B7%CF%83%CE%B7/"
)
PATRIARCHATE_PAGE = (
    "https://ec-patr.org/entities/iera-mitropoli-serron-nigritis/"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "serron-kai-nigrites"
)
NIGRITA_SITE = "https://ecclesia-nigrita.gr/"
NIGRITA_CONTACT = "https://ecclesia-nigrita.gr/m-epikoinwnia"


# number|post id|exact profile title|English seat|Greek address|phone|postal code
PROFILE_ROWS = r'''
001|642|IΕΡΟΣ ΜΗΤΡΟΠΟΛΙΤΙΚΟΣ ΝΑΟΣ ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ|Serres|Σέρρες, Πλ. Ταξιαρχῶν. Τ.Κ. 62122|23210-22755|
002|651|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Σαρανταπόρου 44. Τ.Κ. 62122|23210-39798|
003|655|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ ΣΕΡΡΩΝ|Serres|Σέρρες, Δ. Μαρούλη & Ἀναπαύσεως. Τ.Κ. 62122|23210-25810|
004|658|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΑΝΤΩΝΙΟΥ ΚΑΙ ΜΑΡΙΝΗΣ ΣΕΡΡΩΝ|Serres|Ἐθν. Ἀντιστάσεως & Ἁγίου Ἀντωνίου|23210-23078|
005|663|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Ἐμμ. Παπᾶ 18, Τ.Κ. 62121|23210-23721|
006|668|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΘΕΟΛΟΓΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Ἁγίου Ἰωάννου Θεολόγου 1|23210-25445|
007|672|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΗΤΑ ΤΟΥ ΝΕΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Χ. Τρικούπη 71. Τ.Κ. 62125|23210-39381|
008|677|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΠΑΝΤΕΛΕΗΜΟΝΟΣ ΣΕΡΡΩΝ|Serres|Σέρρες, Ἁγίου Παντελεήμονος & Ἀν. Χρυσάφη, Τ.Κ. 62122|23210-65222|
009|684|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΣΑΡΑΝΤΑ ΜΑΡΤΥΡΩΝ ΣΕΡΡΩΝ|Serres|Σέρρες, Μ. Μπότσαρη 70-77, Τ.Κ. 62124|23210-23718|
010|686|ΙΕΡΟΣ ΝΑΟΣ ΕΙΣΟΔΙΩΝ ΘΕΟΤΟΚΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Μπιζανίου 3, Τ.Κ. 62125|23210-35900|
011|691|ΙΕΡΟΣ ΝΑΟΣ ΕΥΑΓΓΕΛΙΣΤΡΙΑΣ ΣΕΡΡΩΝ|Serres|Σέρρες, Παρ. Τουρλεντέ. Τ.Κ. 62125|23210-45876|
012|694|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Κ. Ἀλεξανδρίδη 10 & Θεσσαλονίκης, Τ.Κ. 62123|23210-56967|
013|697|ΙΕΡΟΣ ΝΑΟΣ ΠΡΟΦΗΤΟΥ ΗΛΙΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Προφ. Ἠλιού 13. Τ.Κ. 62124|23210-24296|
014|2566|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΣΠΥΡΙΔΩΝΟΣ ΣΕΡΡΩΝ|Serres|Σέρρες, Εὐστ. Ἀνθοπούλου & Μονῆς Τιμίου Προδρόμου, Τ.Κ. 62125||
015|704|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Γ. Παπανδρέου 19, Τ.Κ. 62124|23210-23889|
016|707|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΘΕΟΔΩΡΩΝ ΣΕΡΡΩΝ|Serres|Σέρρες|23210-21465|
017|712|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ Α΄ ΚΟΙΜΗΤΗΡΙΟΥ ΣΕΡΡΩΝ|Serres|Α΄ Κοιμητήριο Σερρών|23210-62574|
018|715|ΙΕΡΟΣ ΝΑΟΣ ΖΩΟΔΟΧΟΥ ΠΗΓΗΣ Β' ΚΟΙΜΗΤΗΡΙΟΥ ΣΕΡΡΩΝ|Serres|Β' Κοιμητήριο Σερρών|23210-46577|
019|721|ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΟΥ ΘΕΡΑΠΟΝΤΟΣ ΣΕΡΡΩΝ|Serres|Σέρρες, Καισαρείας 19|23210-23889|
020|725|ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΟΥ ΣΥΜΕΩΝ|Serres|Τέρμα Λ. Παπαπαύλου, Σέρρες|23210-65222|
021|728|ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΩΝ ΔΩΔΕΚΑ ΑΠΟΣΤΟΛΩΝ ΚΑΙ ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΤΟΥ ΚΥΡΙΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Τέρμα Ἐξοχῶν|23210-22755|
022|730|ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΩΝ ΙΩΑΝΝΟΥ ΤΟΥ ΣΕΡΡΑΙΟΥ ΚΑΙ ΛΟΥΚΑ ΤΟΥ ΙΑΤΡΟΥ ΣΕΡΡΩΝ|Serres|Σέρρες, Ἐλ. Βενιζέλου 143||
023|732|ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΩΝ ΜΗΝΑ ΚΑΙ ΚΥΡΙΑΚΗΣ ΣΕΡΡΩΝ|Serres|Ἀκροπόλεως & Εὐθ. Ἀδάμ, Σέρρες||
024|735|ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΝΑΛΗΨΕΩΣ ΤΟΥ ΚΥΡΙΟΥ ΣΕΡΡΩΝ|Serres|Λαμψάκου 810, Σέρρες|23210-22755|
025|739|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ ΔΗΜ. ΔΙΑΜΕΡΙΣΜΑΤΟΣ ΑΓΙΑΣ ΕΛΕΝΗΣ|Agia Eleni|Αγία Ελένη|23210-27712|62100
026|742|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΑΓΙΟΥ ΙΩΑΝΝΟΥ|Agios Ioannis|Άγιος Ιωάννης|23210-59302|
027|746|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΑΓΙΟΥ ΠΝΕΥΜΑΤΟΣ|Agio Pneuma|Άγιο Πνεύμα|23210-91206|62051
028|750|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΑΔΕΛΦΙΚΟΥ|Adelfiko|Αδελφικό|23210-54255|62049
029|753|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΑΝΑΓΕΝΝΗΣΕΩΣ|Anagennisi|Αναγέννηση|23210-78167|62400
030|756|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΒΑΛΤΟΤΟΠΙΟΥ|Valtotopi|Βαλτοτόπι|23210-31797|62100
031|759|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ ΒΑΜΒΑΚΙΑΣ|Vamvakia|Βαμβακιά|23210-81169|62400
032|762|ΙΕΡΟΣ ΝΑΟΣ ΖΩΟΔΟΧΟΥ ΠΗΓΗΣ ΒΑΜΒΑΚΟΥΣΑΣ|Vamvakousa|Βαμβακούσα|23210-41395|62100
033|765|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΑΝΩ ΒΡΟΝΤΟΥΣ|Ano Vrontou|Άνω Βροντού|23210-85280|62100
034|768|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΕΛΑΙΩΝΟΣ|Elaionas|Ελαιώνας|23210-92330|62100
035|776|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΕΜΜ. ΠΑΠΠΑ|Emmanouil Pappas|Εμμανουήλ Παππάς|23210-91968|62048
036|779|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΕΠΤΑΜΥΛΩΝ|Eptamyloi|Επτάμυλοι|23210-93065|62100
037|785|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΕΥΑΓΓΕΛΙΣΤΡΙΑΣ|Evangelistria|Ευαγγελίστρια||57017
038|787|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΑΛΩΝ ΔΕΝΔΡΩΝ|Kala Dendra|Καλά Δένδρα||62100
039|789|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΝΩ ΚΑΜΗΛΑΣ|Ano Kamila|Άνω Καμήλα|23210-88768|62100
040|791|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΑΤΩ ΚΑΜΗΛΑΣ|Kato Kamila|Κάτω Καμήλα|23210-38356|62100
041|793|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΑΡΠΕΡΗΣ|Karperi|Καρπερή|23210-81746|62400
042|807|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΚΕΦΑΛΟΧΩΡΙΟΥ|Kefalochori|Κεφαλοχώρι|23220-63325|57017
043|811|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΚΟΥΒΟΥΚΛΙΩΝ|Kouvouklia|Κουβούκλια|23210-41658|62100
044|814|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΚΡΙΝΟΥ|Krinos|Κρίνος|23210-63495|62100
045|817|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΚΟΥΜΑΡΙΑΣ|Koumaria|Κουμαριά|23210-59862|62100
046|820|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΠΑΝΤΕΛΕΗΜΟΝΟΣ ΚΩΝΣΤΑΝΤΙΝΑΤΟΥ|Konstantinato|Κωνσταντινάτο|23210-42946|62100
047|823|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΛΑΧΑΝΑ|Lachanas|Λαχανάς|23940-93071|57017
048|826|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΛΕΥΚΩΝΑ|Lefkonas|Λευκώνας|23210-38140|62100
049|829|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΚΑΤΩ ΛΕΥΚΩΝΟΣ|Kato Lefkonas|Κάτω Λευκώνας||62100
050|832|ΙΕΡΟΣ ΝΑΟΣ ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ ΜΕΛΕΝΙΚΙΤΣΙΟΥ|Melenikitsi|Μελενικίτσι|23210-88150|62300
051|835|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΜΕΣΟΚΩΜΗΣ|Mesokomi|Μεσοκώμη|23210-32049|62100
052|839|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΜΕΤΑΛΛΩΝ|Metalla|Μέταλλα||
053|842|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΜΕΤΟΧΙΟΥ|Metochi|Μετόχι|23210-46653|62100
054|845|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΑΝΩ ΜΗΤΡΟΥΣΙΟΥ|Ano Mitrousi|Άνω Μητρούσι|23210-75313|62100
055|848|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΑΤΩ ΜΗΤΡΟΥΣΙΟΥ|Kato Mitrousi|Κάτω Μητρούσι||62100
056|851|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΜΟΝΟΒΡΥΣΕΩΣ|Monovrysi|Μονόβρυση|23210-39215|62100
057|855|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ ΜΟΝΟΚΚΛΗΣΙΑΣ|Monokklisia|Μονοκκλησιά|23210-46027|62100
058|858|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΕΚΤΑΡΙΟΥ ΝΕΟΧΩΡΙΟΥ|Neochori|Νεοχώρι|23211-21287|62100
059|861|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΞΗΡΟΤΟΠΟΥ|Xirotopos|Ξηρότοπος|23210-56346|62100
060|864|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ ΟΙΝΟΥΣΑΣ|Oinoussa|Οινούσσα|23210-50743|62100
061|870|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΑΝΩ ΟΡΕΙΝΗΣ|Ano Oreini|Άνω Ορεινή||62100
062|873|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΜΑΡΙΝΑΣ ΚΑΤΩ ΟΡΕΙΝΗΣ|Kato Oreini|Κάτω Ορεινή|2321-321256|62100
063|878|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΠΑΛΑΙΟΚΑΣΤΡΟΥ|Palaiokastro|Παλαιόκαστρο|23210-86034|62300
064|882|ΙΕΡΟΣ ΝΑΟΣ ΓΕΝΝΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΠΑΡΑΛΙΜΝΙΟΥ|Paralimnio|Παραλίμνιο|23210-36004|62100
065|885|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΠΕΝΤΑΠΟΛΕΩΣ|Pentapoli|Πεντάπολη|23210-92814|62048
066|891|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΠΕΠΟΝΙΑΣ|Peponia|Πεπόνια|23210-41445|62100
067|895|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΠΡΟΒΑΤΑ|Provatas|Προβατάς||62100
068|899|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΝΕΟΥ ΣΚΟΠΟΥ|Neo Skopos|Νέος Σκοπός|23210-32601|62044
069|902|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΣΚΟΤΟΥΣΗΣ|Skotoussa|Σκοτούσσα|23210-81235|62100
070|905|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΣΚΟΥΤΑΡΕΩΣ|Skoutari|Σκούταρι|23210-41887|62100
071|908|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΝΕΟΥ ΣΟΥΛΙΟΥ|Neo Souli|Νέο Σούλι|23210-92986|62100
072|911|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ ΣΤΡΥΜΟΝΙΚΟΥ|Strymoniko|Στρυμονικό|23210-86020|62054
073|914|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ ΣΥΚΙΑΣ|Sykia|Συκιά|23210-54994|
074|917|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΤΥΡΟΛΟΗΣ|Tyroloi|Τυρολόη|23210-71834|62100
075|920|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ ΧΙΟΝΟΧΩΡΙΟΥ|Chionochori|Χιονοχώρι||62100
076|923|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΧΡΙΣΤΟΥ|Christos|Χριστός|23210-78370|
077|928|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΧΡΥΣΟΥ|Chryso|Χρυσό|23210-42658|62046
078|931|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΘΕΟΛΟΓΟΥ ΨΥΧΙΚΟΥ|Psychiko|Ψυχικό|23210-32479|62100
079|1017|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΝΙΓΡΙΤΗΣ|Nigrita|Νιγρίτα|23220-22507|62200
080|1020|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΝΙΓΡΙΤΗΣ|Nigrita|Νιγρίτα|23220-22270|62200
081|1023|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΔΗΜ. ΔΙΑΜΕΡΙΣΜΑΤΟΣ|Agia Paraskevi|Αγία Παρασκευή|23220-41223|62200
082|1027|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΔΗΜΟΤΙΚΟΥ ΔΙΑΜΕΡΙΣΜΑΤΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ|Agios Dimitrios|Άγιος Δημήτριος|23220-35531|
083|1032|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΑΗΔΟΝΟΧΩΡΙΟΥ|Aidonochori|Αηδονοχώρι|23220-31317|62049
084|1037|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΑΜΠΕΛΩΝ|Ampeloi|Άμπελοι|23220-63300|62054
085|1041|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΝΘΗΣ|Anthi|Ανθή|23220-24405|62200
086|1046|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ ΑΧΙΝΟΥ|Achinos|Αχινός|23220-31472|62200
087|1050|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΒΑΡΙΚΟΥ|Variko|Βαρικό|23210-88367|62054
088|1062|ΙΕΡΟΣ ΝΑΟΣ ΠΡΟΦΗΤΗ ΗΛΙΑ ΒΕΡΓΗΣ|Vergi|Βέργη|2322-110044|62200
089|1066|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΔΑΦΝΗΣ|Dafni|Δάφνη|23220-51994|62200
090|1069|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΔΗΜΗΤΡΙΤΣΙΟΥ|Dimitritsi|Δημητρίτσι|23220-61620|62200
091|1073|ΙΕΡΟΣ ΝΑΟΣ ΜΕΓΑΛΩΝ ΤΑΞΙΑΡΧΩΝ ΕΥΚΑΡΠΙΑΣ|Efkarpia|Ευκαρπία|23210-88844|62049
092|1076|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ ΖΕΡΒΟΧΩΡΙΟΥ|Zervochori|Ζερβοχώρι|23220-51811|62200
093|1079|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΘΕΡΜΩΝ|Therma|Θερμά||62200
094|1082|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ ΙΒΗΡΩΝ|Iviron|Ίβηρα|23210-35568|62049
095|1085|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ ΚΑΣΤΑΝΟΧΩΡΙΟΥ|Kastanochori|Καστανοχώρι|23220-31135|62200
096|1089|ΙΕΡΟΣ ΝΑΟΣ ΜΕΓΑΛΩΝ ΤΑΞΙΑΡΧΩΝ ΚΑΣΤΡΙΟΥ|Kastri|Καστρί||
097|1092|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΛΑΓΚΑΔΙΟΥ|Lagkadi|Λαγκάδι|23220-51984|62200
098|1098|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΛΕΥΚΟΤΟΠΟΥ|Lefkotopos|Λευκότοπος|23220-52022|62200
099|1101|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΛΙΒΑΔΟΧΩΡΙΟΥ|Livadochori|Λιβαδοχώρι|23220-63560|62054
100|1104|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ ΛΥΓΑΡΙΑΣ|Lygaria|Λυγαριά|23220-25773|
101|1107|ΙΕΡΟΣ ΝΑΟΣ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΜΑΥΡΟΘΑΛΑΣΣΑΣ|Mavrothalassa|Μαυροθάλασσα|23220-35544|62049
102|1110|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΝΙΚΟΚΛΕΙΑΣ|Nikokleia|Νικόκλεια|23220-41039|62200
103|1113|ΙΕΡΟΣ ΝΑΟΣ ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΤΟΥ ΚΥΡΙΟΥ ΟΡΕΣΚΕΙΑΣ|Oreskeia|Ορέσκεια||62200
104|1127|ΙΕΡΟΣ ΝΑΟΣ ΓΕΝΝΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΠΑΤΡΙΚΙΟΥ|Patriki|Πατρίκι||62200
105|1130|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΠΥΡΓΟΥ|Pyrgos|Πύργος||62049
106|1135|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΔΩΔΕΚΑ ΑΠΟΣΤΟΛΩΝ ΣΗΣΑΜΙΑΣ|Sisamia|Σησαμιά|23220-41339|62200
107|1138|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΣΙΤΟΧΩΡΙΟΥ|Sitochori|Σιτοχώρι|23220-24875|62200
108|1141|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΤΕΡΠΝΗΣ|Terpni|Τερπνή|23220-23142|62200
109|1145|ΙΕΡΟΣ ΝΑΟΣ ΤΡΙΩΝ ΙΕΡΑΡΧΩΝ ΤΕΡΠΝΗΣ|Terpni|Τερπνή|23220-22043|62200
110|1151|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ ΤΡΑΓΙΛΟΥ|Tragilos|Τράγιλος|23220-31135|62049
111|1154|ΙΕΡΟΣ ΝΑΟΣ ΓΕΝΝΗΣΕΩΣ ΘΕΟΚΟΤΟΥ ΤΡΙΑΝΤΑΦΥΛΛΙΑΣ|Triantafyllia|Τριανταφυλλιά|23220-61831|62054
112|1157|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΦΛΑΜΠΟΥΡΟΥ|Flambouro|Φλάμπουρο|23220-64281|62200
113|1160|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΧΟΥΜΝΙΚΟΥ|Choumniko|Χουμνικό||62200
114|1195|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΑΣΠΡΟΒΑΛΤΑΣ|Asprovalta|Ασπροβάλτα|23970-22405|57021
115|1199|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΒΡΑΣΝΩΝ|Vrasna|Βρασνά|23970-23569|57021
116|1203|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ ΝΕΩΝ ΒΡΑΣΝΩΝ|Nea Vrasna|Νέα Βρασνά|23970-24363|57021
117|1206|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ ΝΕΩΝ ΚΕΡΔΥΛΙΩΝ|Nea Kerdylia|Νέα Κερδύλια|23220-32301|62052
118|1212|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΠΑΝΤΕΛΕΗΜΟΝΟΣ ΑΝΟΙΞΙΑΣ|Anoixia|Ανοιξιά|23950-91268|57016
119|1219|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΑΡΕΘΟΥΣΑΣ|Arethousa|Αρέθουσα||57002
120|1225|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΛΕΥΚΟΥΔΑΣ|Lefkouda|Λευκούδα||57002
121|1229|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ ΛΙΜΝΗΣ|Limni|Λίμνη|23950-71108|57002
122|1239|ΙΕΡΟΣ ΝΑΟΣ ΓΕΝΝΗΣΕΩΣ ΘΕΟΤΟΚΟΥ ΜΑΡΟΥΔΑΣ|Mavrouda|Μαυρούδα|23950-71262|57002
123|1242|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΞΗΡΟΠΟΤΑΜΟΥ|Xiropotamos|Ξηροπόταμος|23950-91319|57016
124|1248|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΣΚΕΠΑΣΤΟΥ|Skepasto|Σκεπαστό||57016
125|1251|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΦΙΛΑΔΕΛΦΙΟΥ|Filadelfio|Φιλαδέλφιο|23950-91213|57016
126|1254|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ ΣΤΕΦΑΝΙΝΩΝ|Stefanina|Στεφανινά|23950-41609|57002
'''


# Longest and most specific source phrases come first.
DEDICATION_RULES = [
    ("ΑΓΙΩΝ ΔΩΔΕΚΑ ΑΠΟΣΤΟΛΩΝ ΚΑΙ ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΤΟΥ ΚΥΡΙΟΥ", "Holy Twelve Apostles and Transfiguration of the Lord"),
    ("ΑΓΙΩΝ ΙΩΑΝΝΟΥ ΤΟΥ ΣΕΡΡΑΙΟΥ ΚΑΙ ΛΟΥΚΑ ΤΟΥ ΙΑΤΡΟΥ", "Saints John of Serres and Luke the Surgeon"),
    ("ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ", "Saints Constantine and Helen"),
    ("ΑΓΙΩΝ ΑΝΤΩΝΙΟΥ ΚΑΙ ΜΑΡΙΝΗΣ", "Saints Anthony and Marina"),
    ("ΑΓΙΩΝ ΜΗΝΑ ΚΑΙ ΚΥΡΙΑΚΗΣ", "Saints Menas and Kyriake"),
    ("ΑΓΙΩΝ ΣΑΡΑΝΤΑ ΜΑΡΤΥΡΩΝ", "Forty Holy Martyrs"),
    ("ΑΓΙΩΝ ΔΩΔΕΚΑ ΑΠΟΣΤΟΛΩΝ", "Holy Twelve Apostles"),
    ("ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ", "Holy Archangels"),
    ("ΜΕΓΑΛΩΝ ΤΑΞΙΑΡΧΩΝ", "Holy Archangels"),
    ("ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ", "Holy Unmercenaries"),
    ("ΑΓΙΩΝ ΘΕΟΔΩΡΩΝ", "Holy Theodores"),
    ("ΤΡΙΩΝ ΙΕΡΑΡΧΩΝ", "Three Holy Hierarchs"),
    ("ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΘΕΟΛΟΓΟΥ", "Saint John the Theologian"),
    ("ΑΓΙΟΥ ΝΙΚΗΤΑ ΤΟΥ ΝΕΟΥ", "Saint Niketas the New"),
    ("ΑΓΙΟΥ ΠΑΝΤΕΛΕΗΜΟΝΟΣ", "Saint Panteleimon"),
    ("ΕΙΣΟΔΙΩΝ ΘΕΟΤΟΚΟΥ", "Entry of the Theotokos into the Temple"),
    ("ΕΥΑΓΓΕΛΙΣΤΡΙΑΣ", "Annunciation of the Theotokos"),
    ("ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ", "Dormition of the Theotokos"),
    ("ΠΡΟΦΗΤΟΥ ΗΛΙΟΥ", "Prophet Elijah"),
    ("ΠΡΟΦΗΤΗ ΗΛΙΑ", "Prophet Elijah"),
    ("ΑΓΙΟΥ ΣΠΥΡΙΔΩΝΟΣ", "Saint Spyridon"),
    ("ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ", "Holy Cross"),
    ("ΑΓΙΟΥ ΘΕΡΑΠΟΝΤΟΣ", "Saint Therapon"),
    ("ΑΝΑΛΗΨΕΩΣ ΤΟΥ ΚΥΡΙΟΥ", "Ascension of the Lord"),
    ("ΖΩΟΔΟΧΟΥ ΠΗΓΗΣ", "Life-giving Spring"),
    ("ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ", "Saint Paraskevi"),
    ("ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ", "Saint Athanasius"),
    ("ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ", "Saint George"),
    ("ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ", "Saint Anthony"),
    ("ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ", "Saint Nicholas"),
    ("ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ", "Saint John the Forerunner"),
    ("ΑΓΙΟΥ ΔΗΜΗΤΡΙΟΥ", "Saint Demetrius"),
    ("ΑΓΙΟΥ ΝΕΚΤΑΡΙΟΥ", "Saint Nectarios"),
    ("ΑΓΙΑΣ ΤΡΙΑΔΟΣ", "Holy Trinity"),
    ("ΑΓΙΑΣ ΜΑΡΙΝΑΣ", "Saint Marina"),
    ("ΓΕΝΝΗΣΕΩΣ ΘΕΟΤΟΚΟΥ", "Nativity of the Theotokos"),
    ("ΓΕΝΝΗΣΕΩΣ ΘΕΟΚΟΤΟΥ", "Nativity of the Theotokos"),
    ("ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΤΟΥ ΚΥΡΙΟΥ", "Transfiguration of the Lord"),
]


MONASTIC_ROWS = [
    {
        "local": "ΙΕΡΑ ΜΟΝΗ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ ΣΕΡΡΩΝ",
        "name": "Saint John the Forerunner Monastery near Serres",
        "seat": "Serres",
        "address": ["Ἱερά Μονή Τιμίου Προδρόμου Σερρῶν", "Τ.Κ. 62100"],
        "rank": "Monastery",
        "phones": ["23210-74623"],
        "sources": [
            "https://www.imsn.gr/wp-json/wp/v2/posts/941",
            MONASTERY_PAGE,
            PATRIARCHATE_PAGE,
        ],
    },
    {
        "local": "ΙΕΡΑ ΜΟΝΗ ΥΨΩΣΕΩΣ ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ ΑΓΙΟΥ ΠΝΕΥΜΑΤΟΣ",
        "name": "Exaltation of the Holy Cross Monastery at Agio Pneuma",
        "seat": "Agio Pneuma",
        "address": ["Ἱερά Μονή Ὑψώσεως Τιμίου Σταυροῦ", "Τ.Κ. 62051, Ἅγιον Πνεῦμα Σερρῶν"],
        "rank": "Monastery",
        "phones": ["23210-91353"],
        "sources": [
            "https://www.imsn.gr/wp-json/wp/v2/posts/951",
            MONASTERY_PAGE,
            PATRIARCHATE_PAGE,
        ],
    },
    {
        "local": "ΙΕΡΑ ΜΟΝΗ ΠΡΟΦΗΤΟΥ ΗΛΙΟΥ ΑΓΙΟΥ ΠΝΕΥΜΑΤΟΣ",
        "name": "Prophet Elijah Monastery at Agio Pneuma",
        "seat": "Agio Pneuma",
        "address": ["Ἱερά Μονή Προφήτου Ἠλιού", "Τ.Κ. 62051, Ἅγιον Πνεῦμα Σερρῶν"],
        "rank": "Monastery",
        "phones": ["23210-91360"],
        "sources": [
            "https://www.imsn.gr/wp-json/wp/v2/posts/957",
            MONASTERY_PAGE,
            PATRIARCHATE_PAGE,
        ],
    },
    {
        "local": "ΙΕΡΑ ΜΟΝΗ ΚΟΙΜΗΣΕΩΣ ΘΕΟΤΟΚΟΥ «ΒΥΣΣΙΑΝΗΣ»",
        "name": "Dormition of the Theotokos Vyssiani Monastery near Serres",
        "seat": "Serres",
        "address": ["Ἱερά Μονή Κοιμήσεως Θεοτόκου «Βύσσιανης»", "Τ.Κ. 62100, Σέρρες"],
        "rank": "Monastery",
        "phones": ["23210-62502"],
        "sources": [
            "https://www.imsn.gr/wp-json/wp/v2/posts/963",
            MONASTERY_PAGE,
            PATRIARCHATE_PAGE,
        ],
    },
    {
        "local": "ΙΕΡΑ ΑΝΔΡΩΑ ΜΟΝΗ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΣΕΡΡΩΝ",
        "name": "Saint Paraskevi Monastery in Serres",
        "seat": "Serres",
        "address": ["Ἴων. Δραγούμη καί Ἁγίου Ἀντωνίου", "Τ.Κ. 62122, Σέρρες"],
        "rank": "Monastery",
        "phones": ["23210-22480"],
        "sources": [
            "https://www.imsn.gr/wp-json/wp/v2/posts/969",
            MONASTERY_PAGE,
            PATRIARCHATE_PAGE,
        ],
    },
    {
        "local": "ΜΟΝΥΔΡΙΟ ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΤΟΥ ΠΡΟΔΡΟΜΟΥ",
        "name": "Saint John the Forerunner Metochion (Prodromoudi) in Serres",
        "seat": "Serres",
        "address": ["Παλαιό Κονάκι, Σέρρες"],
        "rank": "Metochion",
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
    },
    {
        "local": "ΜΟΝΥΔΡΙΟ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ ΚΡΥΟΝΕΡΙΤΟΥ",
        "name": "Saint George Kryoneritis Metochion near Serres",
        "seat": "Serres",
        "address": ["Ὁδός Σερρῶν-Ἁγίου Ἰωάννου, Σέρρες"],
        "rank": "Metochion",
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
    },
    {
        "local": "ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΠΑΝΑΓΙΑΣ ΜΥΡΤΙΔΙΩΤΙΣΣΑΣ",
        "name": "Panagia Myrtidiotissa Monastery Chapel at Agio Pneuma",
        "seat": "Agio Pneuma",
        "address": ["Ἱερά Μονή Προφήτου Ἠλιού", "Τ.Κ. 62051, Ἅγιον Πνεῦμα Σερρῶν"],
        "rank": "Monastery Chapel",
        "sources": [MONASTERY_PAGE],
    },
    {
        "local": "ΙΕΡΟ ΚΟΙΜΗΤΗΡΙΑΚΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΡΧΑΓΓΕΛΟΥ ΜΙΧΑΗΛ",
        "name": "Archangel Michael Cemetery Chapel at Prophet Elijah Monastery",
        "seat": "Agio Pneuma",
        "address": ["Ἱερά Μονή Προφήτου Ἠλιού", "Τ.Κ. 62051, Ἅγιον Πνεῦμα Σερρῶν"],
        "rank": "Monastery Chapel",
        "sources": [MONASTERY_PAGE],
    },
    {
        "local": "ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΠΑΝΑΓΙΑΣ",
        "name": "Panagia Monastery Chapel at Vyssiani Monastery",
        "seat": "Serres",
        "address": ["Ἱερά Μονή Κοιμήσεως Θεοτόκου «Βύσσιανης»", "Τ.Κ. 62100, Σέρρες"],
        "rank": "Monastery Chapel",
        "sources": [MONASTERY_PAGE],
    },
    {
        "local": "ΙΕΡΟ ΠΑΡΕΚΚΛΗΣΙΟ ΑΓΙΟΥ ΧΑΡΑΛΑΜΠΟΥΣ",
        "name": "Saint Charalambos Monastery Chapel at Vyssiani Monastery",
        "seat": "Serres",
        "address": ["Ἱερά Μονή Κοιμήσεως Θεοτόκου «Βύσσιανης»", "Τ.Κ. 62100, Σέρρες"],
        "rank": "Monastery Chapel",
        "sources": [MONASTERY_PAGE],
    },
    {
        "local": "ΙΕΡΟ ΝΑΫΔΡΙΟ ΖΩΟΔΟΧΟΥ ΠΗΓΗΣ",
        "name": "Life-giving Spring Monastery Chapel in Serres",
        "seat": "Serres",
        "address": ["Ἴων. Δραγούμη καί Ἁγίου Ἀντωνίου", "Τ.Κ. 62122, Σέρρες"],
        "rank": "Monastery Chapel",
        "sources": [MONASTERY_PAGE],
    },
    {
        "local": "ΙΕΡΟ ΜΕΤΟΧΙΟ ΑΓΙΟΥ ΝΕΟΜΑΡΤΥΡΟΣ ΕΦΡΑΙΜ ΕΠΤΑΜΥΛΩΝ",
        "name": "New Martyr Ephraim Metochion at Eptamyloi",
        "seat": "Eptamyloi",
        "address": ["Ἐπτάμυλοι Σερρῶν"],
        "rank": "Metochion",
        "phones": ["23210-56967"],
        "sources": [MONASTERY_PAGE, PATRIARCHATE_PAGE],
    },
    {
        "local": "ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΠΝΕΥΜΑΤΟΣ ΟΜΩΝΥΜΟΥ ΧΩΡΙΟΥ",
        "name": "Holy Spirit Historic Monastery Church at Agio Pneuma",
        "seat": "Agio Pneuma",
        "address": ["Ἅγιον Πνεῦμα Σερρῶν"],
        "rank": "Historic Monastery Church",
        "sources": [
            "https://www.imsn.gr/wp-json/wp/v2/posts/976",
            MONASTERY_PAGE,
        ],
    },
]


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:72]


def profile_rank(number):
    if number == 1:
        return "Metropolitan Cathedral"
    if number == 16:
        return "Cathedral and Pilgrimage Church"
    if number in (17, 18):
        return "Cemetery Church"
    if number == 20:
        return "Metochion Chapel"
    if 19 <= number <= 24:
        return "Chapel"
    return "Parish Church"


def profile_dedication(number, local):
    if number == 20:
        return "Saints Simeon the Stylite and Simeon the God-receiver"
    for source_phrase, english in DEDICATION_RULES:
        if source_phrase in local:
            return english
    raise ValueError("no English dedication for profile %03d" % number)


def profile_name(dedication, rank, seat):
    return "%s %s in %s" % (dedication, rank, seat)


def parse_profiles():
    rows = []
    for line in PROFILE_ROWS.strip().splitlines():
        values = [value.strip() for value in line.split("|")]
        if len(values) != 7:
            raise ValueError("invalid Serres profile row: %s" % line)
        number_text, post_id_text, local, seat, address_el, phone, postal = values
        number = int(number_text)
        post_id = int(post_id_text)
        rank = profile_rank(number)
        dedication = profile_dedication(number, local)
        source = "https://www.imsn.gr/wp-json/wp/v2/posts/%d" % post_id
        address = [address_el]
        if postal:
            address.append("Τ.Κ. %s" % postal)
        item = {
            "id": "gr-ep-serres-%03d-%s" % (
                number, slug(profile_name(dedication, rank, seat))
            ),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": profile_name(dedication, rank, seat),
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": address,
            "sources": [source],
            "_profile_number": number,
            "_source_post_id": post_id,
        }
        if phone:
            item["phones"] = [phone]
            item["contact_sources"] = [source]
            item["contact_checked"] = CHECKED
        if number == 16:
            item["sources"].append(PATRIARCHATE_PAGE)
        if number == 79:
            item["site"] = NIGRITA_SITE
            item["sources"].extend([NIGRITA_SITE, NIGRITA_CONTACT])
            item["contact_sources"] = [source, NIGRITA_CONTACT]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


def build_rows():
    rows = parse_profiles()
    for index, source in enumerate(MONASTIC_ROWS, 127):
        item = {
            "id": "gr-ep-serres-%03d-%s" % (index, slug(source["name"])),
            "parent": PARENT,
            "kind": "monastery",
            "rank": source["rank"],
            "name": source["name"],
            "local": source["local"],
            "seat": source["seat"],
            "country": "GR",
            "address": list(source["address"]),
            "sources": list(source["sources"]),
        }
        if source.get("phones"):
            item["phones"] = list(source["phones"])
            item["contact_sources"] = [source["sources"][0]]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 140
EXPECTED_OWNER_COUNTS = {PARENT: 140}
EXPECTED_KINDS = {"monastery": 14, "parish": 126}
EXPECTED_RANKS = {
    "Cathedral and Pilgrimage Church": 1,
    "Cemetery Church": 2,
    "Chapel": 5,
    "Historic Monastery Church": 1,
    "Metochion": 3,
    "Metochion Chapel": 1,
    "Metropolitan Cathedral": 1,
    "Monastery": 5,
    "Monastery Chapel": 5,
    "Parish Church": 116,
}
EXPECTED_CONTACT_BODIES = 112
EXPECTED_PHONE_BODIES = 112
EXPECTED_PHONE_VALUES = 112
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 140
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
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))


def clean(source):
    item = {
        key: value for key, value in source.items()
        if not key.startswith("_") and value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(dict.fromkeys(item.get("sources") or []))
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
                raise ValueError(
                    "%s contact source is outside identity sources"
                    % item.get("id")
                )
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s body-owned site lacks provenance" % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Serres candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Serres candidate ledger date drifted")
    expected_summary = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "numbered_profile_rows": 126,
        "numbered_parish_profiles": 118,
        "numbered_chapel_profiles": 6,
        "numbered_cemetery_profiles": 2,
        "parish_kind_rows": EXPECTED_KINDS["parish"],
        "monastery_kind_rows": EXPECTED_KINDS["monastery"],
        "active_monasteries": 5,
        "named_monastic_metochia_and_chapels": 9,
        "historic_monastery_churches": 1,
        "contact_bodies": EXPECTED_CONTACT_BODIES,
        "phone_bodies": EXPECTED_PHONE_BODIES,
        "public_phone_values": EXPECTED_PHONE_VALUES,
        "email_bodies": EXPECTED_EMAIL_BODIES,
        "public_email_values": EXPECTED_EMAIL_VALUES,
        "body_owned_sites": EXPECTED_SITE_BODIES,
        "address_bodies": EXPECTED_ADDRESS_BODIES,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Serres ledger summary drifted")
    for key in (
        "candidates", "source_reconciliations",
        "official_parent_audit", "exclusions",
    ):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Serres ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Serres ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if any(
        not value or not re.fullmatch(r"[a-z0-9-]+", value)
        for value in candidate_ids
    ):
        raise ValueError("Serres ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Serres ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Serres candidate ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
    signatures = {}
    rank_counts = Counter()
    kind_counts = Counter()
    owner_counts = Counter()
    profile_numbers = []
    post_ids = []
    for source in ROWS:
        if source.get("_profile_number"):
            profile_numbers.append(source["_profile_number"])
            post_ids.append(source["_source_post_id"])
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
            raise ValueError("%s lacks an English name, Greek name, or seat" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text) for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.match(email):
                raise ValueError("%s carries an invalid email" % row_id)
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
            if digits.startswith("69"):
                raise ValueError("%s carries an excluded mobile phone" % row_id)
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
    if profile_numbers != list(range(1, 127)):
        raise ValueError("Serres numbered profile sequence drifted")
    if len(post_ids) != len(set(post_ids)):
        raise ValueError("Serres profile post ids are not unique")
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Serres English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Serres English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Serres parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Serres kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Serres rank totals drifted: %r" % dict(sorted(rank_counts.items())))
    coverage = (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site")) for item in result),
        sum(bool(item.get("phones")) for item in result),
        sum(len(item.get("phones") or []) for item in result),
        sum(bool(item.get("emails")) for item in result),
        sum(len(item.get("emails") or []) for item in result),
        sum(bool(item.get("site")) for item in result),
        sum(bool(item.get("address")) for item in result),
    )
    expected_coverage = (
        EXPECTED_CONTACT_BODIES,
        EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES,
        EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES,
        EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected_coverage:
        raise ValueError("Serres contact coverage drifted: %r" % (coverage,))
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
        print(json.dumps(payloads, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            "Serres and Nigrita: %d exact named bodies; %d carry current institutional contact data"
            % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Serres: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
