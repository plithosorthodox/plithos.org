#!/usr/bin/env python3
"""Validate exact named Ilia and Oleni Metropolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_ilia_country.py --check
    python tools/directory_ilia_country.py --check-live
    python tools/directory_ilia_country.py --dump
"""

import argparse
from collections import Counter
import concurrent.futures
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "gr-ilia"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "ilia_country.json"

BASE = "https://www.imilias.gr"
LEGAL = "https://ecclesiagreece.gr/greek/press/ekklisia/2019_iounios.pdf"
PILGRIMAGE_LEGAL = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2010_ioulios.pdf"
)
CHURCH_OF_GREECE = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/eleias-kai-olenes"
)
MALE_MONASTERIES = BASE + "/mones/antrikes-mones"
FEMALE_MONASTERIES = BASE + "/mones/gynaikies-mones"
HESYCHASTERIA = BASE + "/mones/isixasthria-proskinimata"
HISTORY = BASE + "/istorika-stoiheia-ieras-mitropoleos-ileias"

# detail path|Greek seat|Greek dedication|English name|English seat|address|phones
PARISH_SOURCE = r'''
/enories-amaliada/108-agios-athanasios|ΣΚΛΗΒΑ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Skliva|Skliva|ΣΚΛΗΒΑ 27069|2622031808
/enories-amaliada/92-agios-andreas|ΔΑΦΝΙΩΤΙΣΣΑ|Άγιος Ανδρέας|Saint Andrew Parish Church, Dafniotissa|Dafniotissa|ΔΑΦΝΙΩΤΙΣΣΑ 27069|2622094307
/enories-amaliada/76-agios-dionisios|ΠΕΤΡΟΥΛΕΣ|Άγιος Διονύσιος|Saint Dionysius Parish Church, Petroules|Petroules|ΠΕΤΡΟΥΛΕΣ 27200|2622029125
/enories-amaliada/18-agios-georgios-amaliada|ΑΜΑΛΙΑΔΑ|Άγιος Γεώργιος|Saint George Parish Church, Amaliada|Amaliada|Τρικούπη 5, Αμαλιάδα 272 00 27200|2622028977
/enories-amaliada/107-agios-nikolaos|ΣΙΜΟΠΟΥΛΟΝ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Simopoulon|Simopoulon|ΣΙΜΟΠΟΥΛΟΝ 27069|2622024414
/enories-amaliada/91-koimisi-theotokoy|ΒΟΥΛΙΑΓΜΕΝΗ|Κοίμησις της Θεοτόκου|Dormition of the Theotokos Parish Church, Vouliagmeni|Vouliagmeni|ΒΟΥΛΙΑΓΜΕΝΗ 27069 27069|2622031368
/enories-amaliada/75-agia-marina|ΠΕΡΙΣΤΕΡΙ|Αγία Μαρίνα|Saint Marina Parish Church, Peristeri|Peristeri|ΠΕΡΙΣΤΕΡΙ 27200|2622025300
/enories-amaliada/17-agia-anna-amaliada|ΑΜΑΛΙΑΔΑ|Αγία Άννα|Saint Anna Parish Church, Amaliada|Amaliada|27200|6937095992
/enories-amaliada/106-eisodia-theotokoy|ΡΟΔΙΑ|Εισόδια Θεοτόκου|Entrance of the Theotokos into the Temple Parish Church, Rodia|Rodia|ΡΟΔΙΑ 27069|2622093256
/enories-amaliada/90-agios-konstantinos|ΒΕΛΑΝΙΔΙΟΝ|Άγιος Κωνσταντίνος|Saint Constantine Parish Church, Velanidion|Velanidion|ΒΕΛΑΝΙΔΙ 27069|2623035329
/enories-amaliada/74-agios-georgios|ΠΑΛΑΙΟΧΩΡΙ|Άγιος Γεώργιος|Saint George Parish Church, Palaiochori|Palaiochori|ΠΑΛΑΙΟΧΩΡΙ 27200|6932586446
/enories-amaliada/16-agios-athanasios-amaliada|ΑΜΑΛΙΑΔΑ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Amaliada|Amaliada|Καποδιστρίου 27200|2622028647
/enories-amaliada/105-agios-nikolaos|ΟΙΝΟΗ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Oinoi|Oinoi|ΟΙΝΟΗ 27069|
/enories-amaliada/89-agios-xaralampow|ΑΥΓΗ|Άγιος Χαράλαμπος|Saint Charalambos Parish Church, Avgi|Avgi|ΑΥΓΗ ΑΜΑΛΙΑΔΑ 27069|2622028756
/enories-amaliada/73-agia-paraskeui|ΡΟΒΙΑΤΑ|Αγία Παρασκευή|Saint Paraskevi Parish Church, Roviata|Roviata|ΡΟΒΙΑΤΑ 27200|2623032189
/enories-amaliada/104-koim-theotokou|ΞΕΝΙΕΣ|Κοιμ. Θεοτόκου|Dormition of the Theotokos Parish Church, Xenies|Xenies|ΞΕΝΙΕΣ 27052|
/enories-amaliada/88-koimisi-theotokoy|ΑΠΙΔΟΥΛΑ|Κοίμησις της Θεοτόκου|Dormition of the Theotokos Parish Church, Apidoula|Apidoula|ΑΠΙΔΟΥΛΑ ΑΜΑΛΙΑΔΑ 27069|2622026748
/enories-amaliada/72-koimisi-theotokou|ΜΑΡΑΘΙΑ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Marathia|Marathia|ΜΑΡΑΘΕΑ 27200|2622061024
/enories-amaliada/103-agios-geogrios|ΛΟΥΚΑ|Άγιος Γεώργιος|Saint George Parish Church, Louka|Louka|ΛΟΥΚΑΣ 27069|2622093219
/enories-amaliada/87-agios-nikoloas|ΑΝΘΩΝΑΣ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Anthonas|Anthonas|ΑΝΘΩΝ 27069|2622031047
/enories-amaliada/71-analipsi-sotiros|ΛΑΒΔΕΪΚΑ|Ανάληψη Σωτήρος|Ascension of the Savior Parish Church, Lavdeika|Lavdeika|ΛΑΒΔΕΪΚΑ 27200|2622029875
/enories-amaliada/102-agios-nikolaos|ΛΑΤΤΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Latta|Latta|ΛΑΤΑΣ 27069|2622094279
/enories-amaliada/86-agios-ioannis|ΑΚΡΟΠΟΤΑΜΙΑ|Άγιος Ιωάννης|Saint John Parish Church, Akropotamia|Akropotamia|ΑΚΡΟΠΟΤΑΜΙΑ 27069|2622093391
/enories-amaliada/70-agios-ioannis|ΚΑΡΔΑΜΑΣ|Άγιος Ιωάννης Θεολόγος|Saint John the Theologian Parish Church, Kardamas|Kardamas|ΚΑΡΔΑΜΑΣ 27200|2622023623
/enories-amaliada/101-agios-spiridon|ΛΑΓΑΝΑΣ|Άγιος Σπυριδων|Saint Spyridon Parish Church, Laganas|Laganas|ΛΑΓΑΝΑΣ 27069|
/enories-amaliada/85-gennesio-theotokoy|ΑΓΡΑΠΙΔΟΧΩΡΙ|Γεννέσιο της Θεοτόκου|Nativity of the Theotokos Parish Church, Agrapidochori|Agrapidochori|ΑΓΡΑΠΙΔΟΧΩΡΙΟΝ 27069|6976599883
/enories-amaliada/69-agioi-theodori|ΖΕΡΟ|Άγιοι Θεόδωροι|Holy Theodores Parish Church, Zero|Zero|ΑΝΑΛΗΨΙΣ 27200|2610346619
/enories-amaliada/100-agios-ioannis|ΚΡΥΟΝΕΡΙ|Άγιος Ιωάννης|Saint John Parish Church, Kryoneri|Kryoneri|ΚΡΥΟΝΕΡΟΝ 27069|2622094052
/enories-amaliada/84-agios-nikoloas|ΑΓΝΑΝΤΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Agnada|Agnada|ΑΓΝΑΝΤΑ 27069 27069|2622023795
/enories-amaliada/68-agios-georgios|ΔΟΥΝΕΪΚΑ|Άγιος Γεώργιος|Saint George Parish Church, Douneika|Douneika|ΔΟΥΝΑΙΙΚΑ 27200|2622029027
/enories-amaliada/99-agios-nikolaos|ΚΕΡΑΜΙΔΙΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Keramidia|Keramidia|ΚΕΡΑΜΙΔΙΑ 27069|2622031833
/enories-amaliada/83-agios-andreas|ΑΓΙΑ ΤΡΙΑΔΑ|Άγιος Ανδρέας|Saint Andrew Parish Church, Agia Triada|Agia Triada|Αγία Τριάδα 27069 27069|2622031681
/enories-amaliada/67-agia-triada|ΓΕΡΑΚΙ|Αγία Τριάδα|Holy Trinity Parish Church, Geraki|Geraki|ΓΕΡΑΚΙ 27200|2622023674
/enories-andravida-kilini-lexaina/135-agios-dimitrios|ΜΠΟΡΣΙ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Borsi|Borsi|27052|2623061583
/enories-andravida-kilini-lexaina/33-pammegiston-taksiarxon-lexaina|ΑΝΔΡΑΒΙΔΑ|Παμμεγίστων Ταξιαρχών|Holy Archangels Parish Church, Andravida|Andravida|27051|2623054573
/enories-andravida-kilini-lexaina/134-agios-trifonas|ΜΕΛΙΣΣΑ|Άγιος Τρύφων|Saint Tryphon Parish Church, Melissa|Melissa|Μέλισσα 27053|
/enories-andravida-kilini-lexaina/32-agios-konstantinos-lexaina|ΑΝΔΡΑΒΙΔΑ|Άγιος Κωνσταντίνος|Saint Constantine Parish Church, Andravida|Andravida|27051|2623054660
/enories-andravida-kilini-lexaina/133-agioi-theodoroi|ΛΕΧΑΙΝΑ|Άγιοι Θεόδωροι|Holy Theodores Parish Church, Lechaina|Lechaina|27053|
/enories-andravida-kilini-lexaina/132-eisodia-theotokoy|ΛΕΧΑΙΝΑ|Εισόδια της θεοτόκου|Entrance of the Theotokos into the Temple Parish Church, Lechaina|Lechaina|Δ.Δ. ΛΕΧΑΙΝΩΝ 27053|2623024202
/enories-andravida-kilini-lexaina/131-agios-dimitrios|ΛΕΧΑΙΝΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Lechaina|Lechaina|27053|2623023723
/enories-andravida-kilini-lexaina/130-agios-athanasios|ΛΕΥΚΟΧΩΡΙ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Levkochori|Levkochori|27053|2623041668
/enories-andravida-kilini-lexaina/129-koimisi-theotokoy|ΚΑΤΩ ΠΑΝΑΓΙΑ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Kato Panagia|Kato Panagia|27068|2623092528
/enories-andravida-kilini-lexaina/128-agios-dionysios|ΚΥΛΛΗΝΗ|Άγιος Διονὐσιος|Saint Dionysius Parish Church, Kyllini|Kyllini|ΚΥΛΛΗΝΗ 27068|2623041762
/enories-andravida-kilini-lexaina/127-panagia-pantanassa|ΚΟΥΡΤΕΣΙ|Παναγία Παντάνασσα|Panagia Pantanassa Parish Church, Kourtesi|Kourtesi|Δ.Δ. ΚΟΥΡΤΕΣΙΟΥ 27052|2623061583
/enories-andravida-kilini-lexaina/142-agios-nikolaos|ΤΡΑΓΑΝΟ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Tragano|Tragano|27057|2623033078
/enories-andravida-kilini-lexaina/126-agios-georgios|ΑΝΩ ΚΟΥΡΤΕΣΙ|Άγιος Γεώργιος|Saint George Parish Church, Ano Kourtesi|Ano Kourtesi|Δ.Δ. ΚΟΥΡΤΕΣΙΟΥ 27052|2610330624
/enories-andravida-kilini-lexaina/141-agia-kiriaki|ΣΤΡΟΥΣΙ|Αγία Κυριακή|Saint Kyriaki Parish Church, Strousi|Strousi|27053|2623022797
/enories-andravida-kilini-lexaina/125-koimisi-theotokoy|ΚΑΣΤΡΟ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Kastro|Kastro|27050|2623094515
/enories-andravida-kilini-lexaina/140-euaggelismos-theotokou|ΣΤΑΦΙΔΟΚΑΜΠΟΣ|Ευαγγελισμός Της Θεοτόκου|Annunciation of the Theotokos Parish Church, Stafidokabos|Stafidokabos|27053|2623055060
/enories-andravida-kilini-lexaina/124-agios-dimitrios|ΚΑΡΔΙΑΚΑΥΤΙ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Kardiakavti|Kardiakavti|27050|2623042242
/enories-andravida-kilini-lexaina/139-agios-nikolaos|ΣΙΜΙΖΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Simiza|Simiza|27052|2623061596
/enories-andravida-kilini-lexaina/123-agios-nikolaos|ΔΗΜΗΤΡΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Dimitra|Dimitra|27050|2623042489
/enories-andravida-kilini-lexaina/138-agios-georgios|ΟΛΓΑ-ΜΑΡΚΟΠΟΥΛΟΥ|Άγιος Γεώργιος|Saint George Parish Church, Olga Markopoulou|Olga Markopoulou|27053|2623061293
/enories-andravida-kilini-lexaina/122-agioi-apostoloi|ΒΥΤΙΝΕΪΚΑ ΚΥΛΛΗΝΗΣ|Άγιοι Απόστολοι|Holy Apostles Parish Church, Vytineika Kyllinis|Vytineika Kyllinis|27068|
/enories-andravida-kilini-lexaina/137-agios-georgios|ΝΕΟΧΩΡΙ|Άγιος Γεώργιος|Saint George Parish Church, Neochori|Neochori|27053|2623055198
/enories-andravida-kilini-lexaina/121-agios-georgios|ΒΡΑΧΝΕΪΚΑ|Άγιος Γεώργιος|Saint George Parish Church, Vrachneika|Vrachneika|27053|
/enories-andravida-kilini-lexaina/136-agios-nikolaos|ΜΥΡΣΙΝΗ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Myrsini|Myrsini|27053|2623023825
/enories-arx-olimpias/187-koimisi-theotokou|ΜΑΓΕΙΡΑ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Mageira|Mageira|ΜΑΓΕΙΡΑΣ 27065|6983027907
/enories-arx-olimpias/186-agios-nikolaos|ΛΟΥΒΡΟ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Louvro|Louvro|ΛΟΥΒΡΟ 27065|2624071452
/enories-arx-olimpias/185-agios-dimitrios|ΛΙΝΑΡΙΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Linaria|Linaria|ΛΙΝΑΡΙΑ 27065 27065|6976349741
/enories-arx-olimpias/184-agios-dimitrios|ΚΟΣΚΙΝΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Koskina|Koskina|ΚΟΣΚΙΝΑΣ 27065 27065|2624031656
/enories-arx-olimpias/183-agios-athanasios|ΚΛΑΔΕΟ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Kladeo|Kladeo|ΚΛΑΔΕΟ 27065|2624022093
/enories-arx-olimpias/182-agios-georgios|ΚΑΜΕΝΑ|Άγιος Γεώργιος|Saint George Parish Church, Kamena|Kamena|ΚΑΜΕΝΑ 27065|
/enories-arx-olimpias/181-agios-nikolaos|ΒΑΣΙΛΑΚΙ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Vasilaki|Vasilaki|ΒΑΣΙΛΑΚΙ 27065 27065|2624071070
/enories-arx-olimpias/180-agios-georgios|ΑΣΠΡΑ ΣΠΙΤΙΑ|Άγιος Γεώργιος|Saint George Parish Church, Aspra Spitia|Aspra Spitia|ΑΣΠΡΑ ΣΠΙΤΙΑ 27065 27065|2624071182
/enories-arx-olimpias/179-koimisi-theotokou|ΑΡΧΑΙΑ ΟΛΥΜΠΙΑ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Archaia Olybia|Archaia Olybia|27065|2624041824
/enories-arx-olimpias/193-agios-xaralampos|ΦΛΩΚΑ|Άγιος Χαράλαμπος|Saint Charalambos Parish Church, Floka|Floka|ΦΛΩΚΑΣ 27065|2624022772
/enories-arx-olimpias/192-metamorfosi-sotiros|ΥΨΗΛΟΝ|Μεταμόρφωσι Του Σωτήρος|Transfiguration of the Savior Parish Church, Ypsilon|Ypsilon|ΥΨΗΛΟΝ 27065|
/enories-arx-olimpias/191-agios-georgios|ΠΕΥΚΑΙ (ΒΥΛΙΖΑ)|Άγιος Γεώργιος|Saint George Parish Church, Pevkai Vyliza|Pevkai Vyliza|ΠΕΥΚΑΙ 27065|2624023384
/enories-arx-olimpias/190-agia-marina|ΞΗΡΟΚΑΜΠΟΣ|Αγία Μαρίνα|Saint Marina Parish Church, Xirokabos|Xirokabos|ΞΗΡΟΚΑΜΠΟΣ 27065|2624071378
/enories-arx-olimpias/189-agios-basileios|ΜΟΥΡΙΑ|Άγιος Βασίλειος|Saint Basil Parish Church, Mouria|Mouria|ΜΟΥΡΙΑ 27065|2621025018
/enories-arx-olimpias/188-agios-georgios|ΜΙΡΑΚΑ|Άγιος Γεώργιος|Saint George Parish Church, Miraka|Miraka|ΜΙΡΑΚΑ 27065 27065|2624041026
/enories-gastouni-vartholomio/116-prof-ilia|ΜΑΧΟΣ|Προφ. Ηλία|Prophet Elijah Parish Church, Machos|Machos|ΜΑΧΟΣ 27050|2623042208
/enories-gastouni-vartholomio/115-agios-geogrios|ΛΥΓΙΑ|Άγιος Γεώργιος|Saint George Parish Church, Lygia|Lygia|ΛΥΓΙΑ 27050|2623096258
/enories-gastouni-vartholomio/114-zoodoxoy-pigis|ΚΑΛΥΒΙΑ-ΗΛΙΔΟΣ|Ζωοδόχου Πηγής|Life-Giving Spring Parish Church, Kalyvia Ilidos|Kalyvia Ilidos|ΗΛΙΔΑ 27300|2622041509
/enories-gastouni-vartholomio/113-agios-ioannis|ΚΑΛΥΒΙΑ-ΒΑΡΘΟΛΟΜΙΟΥ|Άγιος Ιωάννης|Saint John Parish Church, Kalyvia Vartholomiou|Kalyvia Vartholomiou|ΚΑΛΥΒΙΑ 27050|2623041137
/enories-gastouni-vartholomio/112-agios-geogrios|ΚΑΒΑΣΙΛΑ|Άγιος Γεώργιος|Saint George Parish Church, Kavasila|Kavasila|ΚΑΒΑΣΙΛΑ 27300|2623032493
/enories-gastouni-vartholomio/111-agia-marina|ΓΛΥΦΑ|Αγία Μαρίνα|Saint Marina Parish Church, Glyfa|Glyfa|ΓΛΥΦΑ 27050|
/enories-gastouni-vartholomio/31-koimisi-theotokou-gastouni|ΓΑΣΤΟΥΝΗ|Κοίμησις της Θεοτόκου|Dormition of the Theotokos Parish Church, Gastouni|Gastouni|27300|2623035055
/enories-gastouni-vartholomio/30-agios-konstantinos-gastouni|ΓΑΣΤΟΥΝΗ|Άγιος Κωνσταντίνος|Saint Constantine Parish Church, Gastouni|Gastouni|27300|2623035627
/enories-gastouni-vartholomio/29-agios-nikolaos-gastouni|ΓΑΣΤΟΥΝΗ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Gastouni|Gastouni|27300|2623032318
/enories-gastouni-vartholomio/28-pammegiston-taksiarxon-brana|ΒΡΑΝΑΣ|Παμμεγίστων Ταξιαρχών|Holy Archangels Parish Church, Vranas|Vranas|Βρανάς 27050|2623042256
/enories-gastouni-vartholomio/27-agios-ioannis-vartholomio|ΒΑΡΘΟΛΟΜΙΟ|Άγιος Ιωάννης|Saint John Parish Church, Vartholomio|Vartholomio|27050|2623041776
/enories-gastouni-vartholomio/26-koimiseos-theotokou-vartholomio|ΒΑΡΘΟΛΟΜΙΟ|Κοίμησις της Θεοτόκου|Dormition of the Theotokos Parish Church, Vartholomio|Vartholomio|27050|2623042652
/enories-gastouni-vartholomio/25-agios-dimitrios-avgeio|ΑΥΓΕΙΟ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Avgeio|Avgeio|Αυγείον 27300|2622026224
/enories-gastouni-vartholomio/119-agia-paraskeyi|ΚΟΡΟΙΒΟΣ|Αγία Παρασκευή|Saint Paraskevi Parish Church, Koroivos|Koroivos|ΚΟΡΟΙΒΟΣ 27300|6982078920
/enories-gastouni-vartholomio/24-agios-dimitrios-agia-maura|ΑΓ. ΜΑΥΡΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Ag Mavra|Ag Mavra|Αγία Μαύρα 27300|2623035365
/enories-gastouni-vartholomio/118-agia-maura|ΡΟΥΠΑΚΙ|Αγία Μαύρα|Saint Maura Parish Church, Roupaki|Roupaki|ΡΟΥΠΑΚΙΟΝ 27300|2623033122
/enories-gastouni-vartholomio/117-agios-panteleimon|ΠΑΛΑΙΟΠΟΛΙΣ|Άγιος Παντελεήμων|Saint Panteleimon Parish Church, Palaiopolis|Palaiopolis|ΠΑΛΑΙΟΠΟΛΗ 27300|6977955180
/enories-lampeias-lasionos-folois/210-agia-marina|ΛΑΜΠΕΙΑ|Αγία Μαρίνα|Saint Marina Parish Church, Labeia|Labeia|27063|2692082352
/enories-lampeias-lasionos-folois/194-agia-kiriaki|ΑΓΙΑ ΚΥΡΙΑΚΗ|Αγία Κυριακή|Saint Kyriaki Parish Church, Agia Kyriaki|Agia Kyriaki|ΑΓΙΑ ΚΥΡΙΑΚΗ 27063|2624061904
/enories-lampeias-lasionos-folois/209-agio-nikolaos|ΛΑΜΠΕΙΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Labeia|Labeia|27063|2692082350
/enories-lampeias-lasionos-folois/208-agia-triada|ΝΕΡΑΪΔΑ|Αγία Τριάδα|Holy Trinity Parish Church, Neraida|Neraida|ΝΕΡΑΪΔΑ|2624057418
/enories-lampeias-lasionos-folois/207-gennesio-theotokou|ΝΕΜΟΥΤΑ|Γεννέσιο της Θεοτόκου|Nativity of the Theotokos Parish Church, Nemouta|Nemouta|ΝΕΜΟΥΤΑ 27066|
/enories-lampeias-lasionos-folois/206-agios-ioannis|ΜΗΛΙΕΣ|Άγιος Ιωάννης ο Θεολόγος|Saint John the Theologian Parish Church, Milies|Milies|27066|2624041157
/enories-lampeias-lasionos-folois/205-geni-theotokou|ΚΡΥΟΝΕΡΙ|Γεν. Θεοτόκου|Nativity of the Theotokos Parish Church, Kryoneri|Kryoneri|ΚΡΥΟΝΕΡΙΟΝ 27066|2624051174
/enories-lampeias-lasionos-folois/204-agio-nikolaos|ΚΡΥΟΒΡΥΣΗ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Kryovrysi|Kryovrysi|ΚΡΥΟΒΡΥΣΗ 27063|2621026971
/enories-lampeias-lasionos-folois/220-koim-theotokou|ΠΕΡΣΑΙΝΑ|Κοιμ. Θεοτόκου|Dormition of the Theotokos Parish Church, Persaina|Persaina|ΠΕΡΣΑΙΝΑ 27066|2624061181
/enories-lampeias-lasionos-folois/203-koimisi-theotokou|ΚΟΥΜΑΝΙ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Koumani|Koumani|ΚΟΥΜΑΝΙ 27063|2624061395
/enories-lampeias-lasionos-folois/219-kon-elenh|ΛΑΛΑΣ|Άγιοι Κωνσταντίνος και Ελένη|Saints Constantine and Helen Parish Church, Lalas|Lalas|27066|2624041238
/enories-lampeias-lasionos-folois/202-agios-georgios|ΚΑΚΟΤΑΡΙ|Άγιος Γεώργιος|Saint George Parish Church, Kakotari|Kakotari|ΚΑΚΟΤΑΡΙΟΝ 27063|2624061612
/enories-lampeias-lasionos-folois/217-koimisi-theotokou|ΦΟΛΟΗ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Foloi|Foloi|ΦΟΛΟΗ 27066|
/enories-lampeias-lasionos-folois/201-agios-georgios|ΖΑΧΑΡΕΪΚΑ|Άγιος Γεώργιος|Saint George Parish Church, Zachareika|Zachareika|ΚΑΚΟΤΑΡΙΟ 27063|
/enories-lampeias-lasionos-folois/216-agio-nikolaos|ΛΑΣΔΙΚΑΣ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Lasdikas|Lasdikas|27066|2624041710
/enories-lampeias-lasionos-folois/200-agios-nikolaos|ΔΟΥΚΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Douka|Douka|ΔΟΥΚΑΣ 27066|2624041507
/enories-lampeias-lasionos-folois/215-agios-dimitrios|ΠΟΘΟΥ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Pothou|Pothou|27066|2624041710
/enories-lampeias-lasionos-folois/199-agios-ioannis|ΑΧΛΑΔΙΝΗ|Άγιος Ιωάννης|Saint John Parish Church, Achladini|Achladini|ΑΧΛΑΔΙΝΗ 27066|2624041755
/enories-lampeias-lasionos-folois/214-koimisi-theotokou|ΠΕΥΚΗ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Pevki|Pevki|ΠΕΥΚΗ 27064 27064|2624061169
/enories-lampeias-lasionos-folois/198-agios-georgios|ΑΣΤΡΑ|Άγιος Γεώργιος|Saint George Parish Church, Astra|Astra|ΑΣΤΡΑ 27063|2692082391
/enories-lampeias-lasionos-folois/213-analipsi-sotiros|ΠΑΝΟΠΟΥΛΟ|Ανάληψη Σωτήρος|Ascension of the Savior Parish Church, Panopoulo|Panopoulo|ΠΑΝΟΠΟΥΛΟΣ 27063|
/enories-lampeias-lasionos-folois/197-agios-konstantinos|ΑΝΔΡΩΝΙ|Άγιος Κωσταντίνος|Saint Constantine Parish Church, Androni|Androni|ΑΝΔΡΩΝΙ 27063|2622032019
/enories-lampeias-lasionos-folois/212-agioi-theodoroi|ΟΡΕΙΝΗ|Άγιοι Θεόδωροι|Holy Theodores Parish Church, Oreini|Oreini|ΟΡΕΙΝΗ 27063|2624081019
/enories-lampeias-lasionos-folois/196-agios-georgios|ΑΜΥΓΔΑΛΗ|Άγιος Γεώργιος|Saint George Parish Church, Amygdali|Amygdali|ΑΜΥΓΔΑΛΗ|2610322076
/enories-olenis/174-koimisi-theotokou|ΣΤΡΕΦΙ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Strefi|Strefi|ΣΤΡΕΦΙ|6972789736
/enories-olenis/158-agios-dimitrios|ΑΡΒΑΝΙΤΗ|Άγιος Δημητριος|Saint Demetrius Parish Church, Arvaniti|Arvaniti|ΑΡΒΑΝΙΤΙΟΝ 27064|2621061766
/enories-olenis/173-agios-nikolaos|ΣΟΠΙ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Sopi|Sopi|ΣΟΠΙΟΝ 27064|2621026801
/enories-olenis/157-prof-ilia|ΑΓΙΑ ΑΝΝΑ|Προφήτη Ηλία|Prophet Elijah Parish Church, Agia Anna|Agia Anna|ΑΓΙΑ ΑΝΝΑ 27064|2624041137
/enories-olenis/172-agios-athanasios|ΣΜΙΛΑ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Smila|Smila|27060|
/enories-olenis/38-agios-georgios|ΛΑΤΖΟΪΟΝ|Άγιος Γεώργιος Αγ. Γεωργίου Λαντζοϊου|Saint George at Agios Georgios Lantzoio Parish Church, Latzoion|Latzoion|ΛΑΤΖΟΪΟΝ 27064|2621069155
/enories-olenis/171-agios-dimitrios|ΠΟΥΡΝΑΡΙ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Pournari|Pournari|27060|2624031543
/enories-olenis/170-agios-ioannis|ΠΛΑΤΑΝΟΣ|Άγιος Ιωάννης|Saint John Parish Church, Platanos|Platanos|ΠΛΑΤΑΝΟΣ 27065|2621035358
/enories-olenis/169-agios-basileios|ΠΕΛΟΠΙΟ|Άγιος Βασίλειος|Saint Basil Parish Church, Pelopio|Pelopio|27060|2624071111
/enories-olenis/168-prof-ilia|ΜΟΥΖΑΚΙ|Προφήτη Ηλία|Prophet Elijah Parish Church, Mouzaki|Mouzaki|ΜΟΥΖΑΚΙ 27064|2624061696
/enories-olenis/167-zoodoxou-pigis|ΜΑΓΟΥΛΑ|Ζωοδόχου Πηγής|Life-Giving Spring Parish Church, Magoula|Magoula|ΜΑΓΟΥΛΑ 27064|2621071369
/enories-olenis/166-agios-dimitrios|ΛΑΤΖΟΪΟΝ|Άγιος Δημητριος|Saint Demetrius Parish Church, Latzoion|Latzoion|ΛΑΤΖΟΙΟΝ 27060|2621026114
/enories-olenis/165-agios-nikolaos|ΛΑΝΘΙ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Lanthi|Lanthi|ΛΑΝΘΙΟΝ 27064|
/enories-olenis/164-prof-ilia|ΚΟΥΤΣΟΧΕΡΑ|Προφήτη Ηλία|Prophet Elijah Parish Church, Koutsochera|Koutsochera|ΚΟΥΤΣΟΧΕΡΑ 27064|2624031139
/enories-olenis/163-agios-basileios|ΚΛΕΙΝΔΙΑ|Άγιος Βασίλειος|Saint Basil Parish Church, Kleindia|Kleindia|ΚΛΕΙΝΔΙΑ 27064|2621093266
/enories-olenis/178-agios-nikolaos|ΩΛΕΝΑ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Olena|Olena|Ωλένη 27064|2621061793
/enories-olenis/162-agia-paraskeui|ΚΑΥΚΑΝΙΑ|Αγία Παρασκευή|Saint Paraskevi Parish Church, Kavkania|Kavkania|ΚΑΥΚΩΝΙΑ 27060|2624031491
/enories-olenis/177-agios-basileios|ΧΕΛΙΔΟΝΙ|Άγιος Βασίλειος|Saint Basil Parish Church, Chelidoni|Chelidoni|ΧΕΛΙΔΟΝΙ 27064|2624051210
/enories-olenis/161-agios-dimitrios|ΚΑΡΑΤΟΥΛΑ|Άγιος Δημητριος|Saint Demetrius Parish Church, Karatoula|Karatoula|ΚΑΡΑΤΟΥΛΑΣ 27064|2622031020
/enories-olenis/176-agios-konstantinos|ΧΕΙΜΑΔΙΟ|Άγιος Κωσταντίνος|Saint Constantine Parish Church, Cheimadio|Cheimadio|ΧΕΙΜΑΔΙΟΝ 27064|6981050558
/enories-olenis/160-koimisi-theotokou|ΗΡΑΚΛΕΙΑ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Irakleia|Irakleia|ΗΡΑΚΛΕΙΑ 27060|2624032060
/enories-olenis/175-agios-dimitrios|ΧΑΡΙΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Charia|Charia|ΧΑΡΙΑ 27064|2621051274
/enories-olenis/159-agia-paraskeui|ΓΟΥΜΕΡΟ|Αγία Παρασκευή|Saint Paraskevi Parish Church, Goumero|Goumero|ΓΟΥΜΕΡΟ 27064|2621061627
/enories-pyrgou/63-agios-spiridon|ΣΚΟΥΡΟΧΩΡΙ|Άγιος Σπυρίδων|Saint Spyridon Parish Church, Skourochori|Skourochori|ΣΚΟΥΡΟΧΩΡΙΟΝ 27100|2621096363
/enories-pyrgou/47-agios-nikolaos|ΚΑΤΑΚΩΛΟ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Katakolo|Katakolo|ΚΑΤΑΚΩΛΟ 27067|2621041220
/enories-pyrgou/8-agios-eleftherios-pirgos|ΠΥΡΓΟΣ|Άγιος Ελευθέριος|Saint Eleutherius Parish Church, Pyrgos|Pyrgos|Αγίου Γεωργίου 27100|2621032334
/enories-pyrgou/62-koim-theotokoy|ΣΚΑΦΙΔΙΑ|Κοίμ. Θεοτόκου|Dormition of the Theotokos Parish Church, Skafidia|Skafidia|ΣΚΑΦΙΔΙΑ 27100|2621023172
/enories-pyrgou/46-agios-dimitrios|ΚΑΛΑΚΕΪΚΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Kalakeika|Kalakeika|ΚΑΛΑΚΑΙΙΚΑ 27100|2621035260
/enories-pyrgou/7-agios-panteleimon-pirgos|ΠΥΡΓΟΣ|Άγιος Παντελεήμων|Saint Panteleimon Parish Church, Pyrgos|Pyrgos|Κολιρίου 27100|2621033789
/enories-pyrgou/61-agios-georgios|ΣΑΛΜΩΝΙ|Άγιος Γεώργιος|Saint George Parish Church, Salmoni|Salmoni|ΣΑΛΜΩΝΗ|2621069133
/enories-pyrgou/45-agios-athanasiosxrist|ΚΑΒΑΣΙΛΑΚΙΑ|Αγίου Αθανασίου Χριστιανουπόλεως|Saint Athanasius of Christianoupolis Parish Church, Kavasilakia|Kavasilakia|ΚΑΒΑΣΙΛΑΚΙΑ-ΠΥΡΓΟΣ ΠΥΡΓΟΣ 27100|2621051165
/enories-pyrgou/6-agios-spiridinas-pirgos|ΠΥΡΓΟΣ|Άγιος Σπυρίδωνας|Saint Spyridon Parish Church, Pyrgos|Pyrgos|Αγίου Σπυρίδωνος 48, Πύργος 271 00 Πύργος 27100|2621022014
/enories-pyrgou/60-agios-georgios|ΠΡΑΣΙΝΟ|Άγιος Γεώργιος|Saint George Parish Church, Prasino|Prasino|ΠΡΑΣΙΝΟ 27100|2621051342
/enories-pyrgou/44-koim-theotokoy|ΕΛΑΙΩΝΑΣ|Κοιμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Elaionas|Elaionas|ΕΛΑΙΩΝΑΣ 27100|2621095492
/enories-pyrgou/5-agia-triada-pirgos|ΠΥΡΓΟΣ|Αγία Τριάδα|Holy Trinity Parish Church, Pyrgos|Pyrgos|Πατρών 27100|2621036515
/enories-pyrgou/59-agios-athanasios|ΠΑΛΑΙΟΒΑΡΒΑΣΑΙΝΑ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Palaiovarvasaina|Palaiovarvasaina|ΠΑΛΑΙΟΒΑΡΒΑΣΑΙΝΑ 27100|
/enories-pyrgou/43-agios-georgios|ΓΡΑΝΙΤΣΕΪΚΑ|Άγιος Γεώργιος|Saint George Parish Church, Granitseika|Granitseika|ΓΡΑΝΙΤΣΕΪΚΑ 27100|2621033426
/enories-pyrgou/4-agia-kiriaki-pirgos|ΠΥΡΓΟΣ|Αγία Κυριακή|Saint Kyriaki Parish Church, Pyrgos|Pyrgos|Αγ. Κυριακής 27100|2621022349
/enories-pyrgou/58-agios-spiridon|ΞΥΛΟΚΕΡΑ|Άγιος Σπυρίδων|Saint Spyridon Parish Church, Xylokera|Xylokera|ΞΥΛΟΚΕΡΑ 27100|
/enories-pyrgou/42-agios-trifonas|ΒΥΤΙΝΕΪΚΑ|Άγιος Τρύφωνας|Saint Tryphon Parish Church, Vytineika|Vytineika|ΒΥΤΙΝΕΪΚΑ 27100|2624051232
/enories-pyrgou/3-2010-09-16-19-55-11|ΠΥΡΓΟΣ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Pyrgos|Pyrgos|Αγ. Αθανασίου 27100|2621022218
/enories-pyrgou/57-agios-athanasios|ΜΥΡΤΙΑ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Myrtia|Myrtia|ΜΥΡΤΙΑ 27100|2621031459
/enories-pyrgou/41-agios-athanasios|ΒΟΥΝΑΡΓΟ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Vounargo|Vounargo|ΒΟΥΝΑΡΓΟΝ 27100|2621051171
/enories-pyrgou/2-2010-09-16-19-49-32|ΠΥΡΓΟΣ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Pyrgos|Pyrgos|Πλατεία Καράγιωργα ΗΛΕΙΑ 27100|2621023609
/enories-pyrgou/56-agia-triada|ΛΕΒΕΝΤΟΧΩΡΙ|Αγία Τριάδα|Holy Trinity Parish Church, Levedochori|Levedochori|ΛΕΒΕΝΤΟΧΩΡΙΟΝ 27100|
/enories-pyrgou/40-agios-athanasios|ΒΑΡΒΑΣΑΙΝΑ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Varvasaina|Varvasaina|ΒΑΡΒΑΣΑΙΝΑ 27100|2621028970
/enories-pyrgou/55-agios-spiridon|ΛΑΣΤΕΙΚΑ|Άγιος Σπυρίδων|Saint Spyridon Parish Church, Lasteika|Lasteika|ΛΑΣΤΑΙΙΚΑ 27100|
/enories-pyrgou/39-agia-triada|ΒΡΟΧΙΤΣΑ|Αγία Τριάδα|Holy Trinity Parish Church, Vrochitsa|Vrochitsa|ΒΡΟΧΙΤΣΑ 27100|2621051180
/enories-pyrgou/54-agios-nikolaos|ΛΑΜΠΕΤΙ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Labeti|Labeti|ΛΑΜΠΕΤΙΟΝ 27100|2621774063
/enories-pyrgou/15-agios-nikolaos-alpoxori|ΑΛΠΟΧΩΡΙ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Alpochori|Alpochori|Αλποχώρι 27100|2621054650
/enories-pyrgou/53-prof-ilia|ΚΟΥΖΟΥΛΙ|Προφ. Ηλία|Prophet Elijah Parish Church, Kouzouli|Kouzouli|ΚΟΥΖΟΥΛΙΟΝ 27100|2621034843
/enories-pyrgou/14-agios-georgios-ampelonas|ΑΜΠΕΛΩΝΑΣ|Άγιος Γεώργιος|Saint George Parish Church, Abelonas|Abelonas|Αμπελώνας 27100|2621095695
/enories-pyrgou/52-agios-georgios|ΚΟΡΥΦΗ|Άγιος Γεώργιος|Saint George Parish Church, Koryfi|Koryfi|ΚΟΡΥΦΗ 27100|6972072401
/enories-pyrgou/13-agioi-apostoloi-pirgou|ΑΓΙΟΙ ΑΠΟΣΤΟΛΟΙ|Άγιοι Απόστολοι|Holy Apostles Parish Church, Agioi Apostoloi|Agioi Apostoloi|Άγιοι Απόστολοι 27100|2621051165
/enories-varda/145-agios-nikolaos|ΚΑΠΕΛΕΤΟ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Kapeleto|Kapeleto|Σ.Σ. ΒΑΡΑΔΑΣ 27052|2623072159
/enories-varda/144-agios-athanasios|ΚΑΓΚΑΔΙ|Άγιος Αθανάσιος|Saint Athanasius Parish Church, Kagkadi|Kagkadi|25200|2693099010
/enories-varda/143-pam-taxiarxon|ΘΑΝΑΣΟΥΛΕΪΚΑ|Παμμεγίστων Ταξιαρχών|Holy Archangels Parish Church, Thanasouleika|Thanasouleika|27052|
/enories-varda/37-agios-konstantinos|ΒΟΥΠΡΑΣΙΟ|Άγιος Κωνσταντίνος|Saint Constantine Parish Church, Vouprasio|Vouprasio|ΒΟΥΠΡΑΣΙΟ Σ.Σ. ΒΑΡΔΑΣ 27052|2623099610
/enories-varda/36-agia-triada|ΒΑΡΔΑ|Αγία Τριάδα|Holy Trinity Parish Church, Varda|Varda|Σ.Σ. ΒΑΡΔΑΣ 27052|2623071528
/enories-varda/156-koimisi-theotokou|ΨΑΡΙ|Κοίμησις Θεοτόκου|Dormition of the Theotokos Parish Church, Psari|Psari|Σ.Σ. ΒΑΡΔΑΣ 27052|2623071740
/enories-varda/35-agios-dimitrios|ΑΕΤΟΡΡΑΧΗ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Aetorrachi|Aetorrachi|ΑΕΤΟΡΡΑΧΗ Σ.Σ. ΒΑΡΔΑΣ 27052|2623061010
/enories-varda/155-agios-konstantinos|ΣΥΡΜΠΑΝΙ|Άγιος Κωνσταντινος|Saint Constantine Parish Church, Syrbani|Syrbani|Σ.Σ. ΒΑΡΔΑΣ 27052|2623073154
/enories-varda/34-agioi-apostoloi|ΑΓ. ΚΩΝΣΤΑΝΤΙΝΟΣ ΣΠΑΤΑ|Άγιοι Απόστολοι|Holy Apostles Parish Church, Ag Konstadinos Spata|Ag Konstadinos Spata|ΑΓ. ΚΩΝΣΤΑΝΤΙΝΟΣ ΣΠΑΤΑ Σ.Σ. ΒΑΡΔΑΣ 27052|2693099265
/enories-varda/154-pamm-taxiarxon|ΝΗΣΙΟΝ|Παμμεγίστων Ταξιαρχών|Holy Archangels Parish Church, Nision|Nision|Σ.Σ. ΒΑΡΔΑΣ 27052|2623073427
/enories-varda/153-agios-nikolaos|ΜΕΤΟΧΙ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Metochi|Metochi|Σ.Σ. ΒΑΡΔΑΣ 27052|2610524827
/enories-varda/152-agios-dimitrios|ΝΕΑΠΟΛΙΣ|Άγιος Γεώργιος|Saint George Parish Church, Neapolis|Neapolis|Σ.Σ. ΒΑΡΔΑΣ 27052|2623072159
/enories-varda/151-agios-dimitrios|ΜΑΤΑΡΑΓΚΑ|Άγιος Δημήτριος|Saint Demetrius Parish Church, Mataragka|Mataragka|25200|2610342359
/enories-varda/150-agios-georgios|ΝΕΑ ΜΑΝΩΛΑΔΑ|Άγιος Γεώργιος|Saint George Parish Church, Nea Manolada|Nea Manolada|Σ.Σ. ΒΑΡΔΑΣ 27052|2623072104
/enories-varda/149-agios-petros|ΝΕΑ ΜΑΝΩΛΑΔΑ|Άγιος Πέτρος|Saint Peter Parish Church, Nea Manolada|Nea Manolada|Σ.Σ. ΒΑΡΔΑΣ 27052|2623072452
/enories-varda/148-pam-taxiarxon|ΠΑΛΑΙΑ ΜΑΝΩΛΑΔΑ|Παμμεγίστων Ταξιαρχών|Holy Archangels Parish Church, Palaia Manolada|Palaia Manolada|Σ.Σ. ΒΑΡΔΑΣ 27052|6974509388
/enories-varda/147-agios-georgios|ΛΑΠΠΑ|Άγιος Γεώργιος|Saint George Parish Church, Lappa|Lappa|Σ.Σ. ΒΑΡΔΑΣ 27052|2623073680
/enories-varda/146-agios-nikolaos|ΚΡΕΜΜΥΔΙΟΝ|Άγιος Νικόλαος|Saint Nicholas Parish Church, Kremmydion|Kremmydion|Σ.Σ. ΒΑΡΑΔΑΣ 27052|2623071930
'''


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def parish_rows():
    rows = []
    listing_sources = {
        "/enories-lampeias-lasionos-folois/196-agios-georgios":
            BASE + "/enories-lampeias-lasionos-folois",
        "/enories-olenis/174-koimisi-theotokou":
            BASE + "/enories-olenis",
    }
    lines = PARISH_SOURCE.strip().splitlines()
    if len(lines) != 185:
        raise ValueError("expected 185 current parish detail rows")
    for number, raw in enumerate(lines, 1):
        href, seat_local, local, name, seat, address, phones = raw.split("|", 6)
        source = BASE + href
        sources = [source]
        if href in listing_sources:
            sources.append(listing_sources[href])
        sources.append(LEGAL)
        row = {
            "id": "gr-ilia-%03d" % number,
            "parent": PARENT,
            "kind": "parish",
            "rank": "Parish Church",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": sources,
            "live_markers": [local, seat_local],
        }
        if phones:
            row["phones"] = split_values(phones)
            row["contact_sources"] = [source]
            row["contact_checked"] = CHECKED
            row["live_markers"].extend(row["phones"])
        rows.append(row)
    return rows


MONASTIC_ROWS = [
    {
        "id": "gr-ilia-186-panagia-poretsou",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Panagia Poretsou Monastery",
        "local": "Ιερά Μονή Παναγίας Πορετσού",
        "seat": "Agrampela", "country": "GR",
        "address": ["Agrampela, Ilia", "Greece"],
        "sources": [BASE + "/187-iera-moni-poretsou", MALE_MONASTERIES],
        "live_markers": ["Ιερά Μονή Πορετσού", "Αγραμπέλων"],
    },
    {
        "id": "gr-ilia-187-chrysopigi-divri",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Chrysopigi Monastery in Divri",
        "local": "Ιερά Μονή Χρυσοπηγής Δίβρης",
        "seat": "Lampeia", "country": "GR",
        "address": ["Ano Divri, Lampeia, Ilia", "Greece"],
        "phones": ["2624-81263"],
        "sources": [BASE + "/123-moni-xrisopigis-divri",
                    MALE_MONASTERIES, CHURCH_OF_GREECE],
        "contact_sources": [CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Χρυσοπηγής Δίβρης", "2624-81263"],
    },
    {
        "id": "gr-ilia-188-panagia-eleousa-lygia",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Panagia Eleousa Monastery in Lygia",
        "local": "Ιερά Μονή Παναγίας Ελεούσης Λυγιάς",
        "seat": "Lygia", "country": "GR",
        "address": ["Lygia, Ilia", "Greece"],
        "phones": ["6974884238"],
        "sources": [BASE + "/98-moni-eleousa-ligia", FEMALE_MONASTERIES],
        "contact_sources": [BASE + "/98-moni-eleousa-ligia"],
        "contact_checked": CHECKED,
        "live_markers": ["Παναγίας Ελεούσης Λυγιάς", "6974884238"],
    },
    {
        "id": "gr-ilia-189-panagia-kremasti",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Dormition of the Theotokos Kremasti Monastery",
        "local": "Ιερά Μονή Κοιμήσεως Θεοτόκου Κρεμαστής",
        "seat": "Lanti", "country": "GR",
        "address": ["Near Lanti and Lampeti, Ilia", "Greece"],
        "phones": ["26210-25303"],
        "sources": [BASE + "/121-moni-panagia-kremasti",
                    FEMALE_MONASTERIES, CHURCH_OF_GREECE],
        "contact_sources": [BASE + "/121-moni-panagia-kremasti",
                            CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Παναγίας Κρεμαστής", "26210-25303"],
    },
    {
        "id": "gr-ilia-190-saint-nicholas-fragkapidima",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Saint Nicholas Fragkapidima Monastery",
        "local": "Ιερά Μονή Αγίου Νικολάου Φραγκαπηδήματος",
        "seat": "Vounargo", "country": "GR",
        "address": ["Vounargo, Ilia", "Greece"],
        "phones": ["26210-51312"],
        "sources": [BASE + "/95-monastiri-fragapidima",
                    FEMALE_MONASTERIES, CHURCH_OF_GREECE],
        "contact_sources": [BASE + "/95-monastiri-fragapidima",
                            CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Αγ. Νικολάου Φραγκαπηδήματος", "26210-51312"],
    },
    {
        "id": "gr-ilia-191-panagia-skafidia",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Dormition of the Theotokos Skafidia Monastery",
        "local": "Ιερά Μονή Κοιμήσεως Θεοτόκου Σκαφιδιάς",
        "seat": "Skafidia", "country": "GR",
        "address": ["Skafidia, Ilia", "Greece"],
        "phones": ["2621055088", "6972495980", "2621-94273"],
        "sources": [BASE + "/87-moni-skafidia",
                    FEMALE_MONASTERIES, CHURCH_OF_GREECE],
        "contact_sources": [BASE + "/87-moni-skafidia",
                            CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Μονή Σκαφιδιάς", "2621055088",
                         "6972495980", "2621-94273"],
    },
    {
        "id": "gr-ilia-192-panagia-vlaherna",
        "parent": PARENT, "kind": "monastery", "rank": "Monastery",
        "name": "Panagia Vlaherna Monastery in Kato Panagia",
        "local": "Ιερά Μονή Παναγίας Βλαχέρνας",
        "seat": "Kato Panagia", "country": "GR",
        "address": ["Kato Panagia, Kyllini, Ilia", "Greece"],
        "sources": [BASE + "/186-panagia-vlaxerna", HESYCHASTERIA],
        "live_markers": ["Παναγίας της Βλαχέρνας", "Κάτω Παναγιάς"],
    },
    {
        "id": "gr-ilia-193-saint-nicholas-spata",
        "parent": PARENT, "kind": "parish", "rank": "Pilgrimage Church",
        "name": "Saint Nicholas at Spata Pilgrimage Church",
        "local": "Ιερό Προσκύνημα Αγίου Νικολάου Σπάτων",
        "seat": "Spata", "country": "GR",
        "address": ["Near Spata, Achaia", "Greece"],
        "phones": ["26930-99.265"],
        "sources": [BASE + "/185-agios-nikolaos-spata",
                    PILGRIMAGE_LEGAL, CHURCH_OF_GREECE],
        "contact_sources": [CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Αγίου Νικολάου", "Σπάτα", "26930-99.265"],
    },
    {
        "id": "gr-ilia-194-saint-george-lampeti",
        "parent": PARENT, "kind": "monastery", "rank": "Hesychasterion",
        "name": "Saint George Lampeti Hesychasterion",
        "local": "Ιερό Ησυχαστήριο Αγίου Γεωργίου Λαμπετίου",
        "seat": "Lampeti", "country": "GR",
        "address": ["Lampeti, Pyrgos, Ilia", "Greece"],
        "sources": [BASE + "/253-moni-agiou-georgiou-lampetiou",
                    HESYCHASTERIA],
        "live_markers": ["Ησυχαστήριο του Αγίου Γεωργίου Λαμπετίου"],
    },
    {
        "id": "gr-ilia-195-prophet-elijah-amaliada",
        "parent": PARENT, "kind": "monastery", "rank": "Hesychasterion",
        "name": "Prophet Elijah Hesychasterion in Amaliada",
        "local": "Γυναικείο Ησυχαστήριο Προφήτου Ηλιού Αμαλιάδος",
        "seat": "Amaliada", "country": "GR",
        "address": ["Amaliada, Ilia", "Greece"],
        "phones": ["2622-28442"],
        "sources": [BASE + "/151-eorti-profiti-ilia", CHURCH_OF_GREECE],
        "contact_sources": [CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Μονή Αμαλιάδος", "2622-28442"],
    },
    {
        "id": "gr-ilia-196-saint-demetrius-amaliada",
        "parent": PARENT, "kind": "monastery", "rank": "Hesychasterion",
        "name": "Saint Demetrius Hesychasterion in Amaliada",
        "local": "Γυναικείο Ησυχαστήριο Αγίου Δημητρίου Αμαλιάδος",
        "seat": "Amaliada", "country": "GR",
        "address": ["Amaliada, Ilia", "Greece"],
        "phones": ["2622-28961"],
        "sources": [BASE + "/162-eorti-agiou-dimitriou-myrovlitou",
                    CHURCH_OF_GREECE],
        "contact_sources": [CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Μονή Αμαλιάδας", "2622-28961"],
    },
    {
        "id": "gr-ilia-197-ascension-zerou",
        "parent": PARENT, "kind": "monastery", "rank": "Hesychasterion",
        "name": "Ascension of the Savior Zerou Hesychasterion",
        "local": "Γυναικείο Ησυχαστήριο Αναλήψεως του Σωτήρος Ζερού",
        "seat": "Zerou", "country": "GR",
        "address": ["Zerou, Amaliada, Ilia", "Greece"],
        "phones": ["2622-28150"],
        "sources": [BASE + "/174-eorti-analipseos", CHURCH_OF_GREECE],
        "contact_sources": [CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Αναλήψεως Ζερού", "2622-28150"],
    },
    {
        "id": "gr-ilia-198-saint-athanasius-ampelokampos",
        "parent": PARENT, "kind": "monastery", "rank": "Hesychasterion",
        "name": "Saint Athanasius Ampelokampos Hesychasterion",
        "local": "Γυναικείο Ησυχαστήριο Αγίου Αθανασίου Αμπελοκάμπου",
        "seat": "Ampelokampos", "country": "GR",
        "address": ["Ampelokampos, Ilia", "Greece"],
        "phones": ["2622-61280"],
        "sources": [BASE + "/139-eorti-agiou-athanasiou",
                    CHURCH_OF_GREECE],
        "contact_sources": [CHURCH_OF_GREECE],
        "contact_checked": CHECKED,
        "live_markers": ["Μονή Αμπελοκάμπου", "2622-61280"],
    },
]


ROWS = parish_rows() + MONASTIC_ROWS
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 198
EXPECTED_OWNER_COUNTS = {PARENT: 198}
EXPECTED_KINDS = {"monastery": 12, "parish": 186}
EXPECTED_RANKS = {
    "Hesychasterion": 5,
    "Monastery": 7,
    "Parish Church": 185,
    "Pilgrimage Church": 1,
}
EXPECTED_CONTACT_BODIES = 174
EXPECTED_PHONE_BODIES = 174
EXPECTED_PHONE_VALUES = 176
EXPECTED_EMAIL_BODIES = 0
EXPECTED_EMAIL_VALUES = 0
EXPECTED_SITE_BODIES = 0
EXPECTED_ADDRESS_BODIES = 198
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "ecclesiagreece.gr", "www.ecclesiagreece.gr",
    "imilias.gr", "www.imilias.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


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
    if item.get("phones") or item.get("emails"):
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks current contact provenance" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
        if source_url not in sources:
            raise ValueError("contact source is outside identity sources")
    item.pop("live_markers", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Ilia candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Ilia candidate ledger date drifted")
    expected_summary = {
        PARENT: 198,
        "total": 198,
        "current_named_parish_rows": 185,
        "regulated_pilgrimage_rows": 1,
        "monastery_rows": 7,
        "hesychasterion_rows": 5,
        "contact_bodies": 174,
        "phone_bodies": 174,
        "public_phone_values": 176,
        "email_bodies": 0,
        "public_email_values": 0,
        "body_owned_sites": 0,
        "address_bodies": 198,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Ilia ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Ilia ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Ilia ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Ilia ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Ilia ledger has forbidden punctuation")
    return ledger


def build():
    result = []
    ids = set()
    signatures = {}
    ranks = Counter()
    kinds = Counter()
    owners = Counter()
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in ids or row_id in EXISTING_PARENTS:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has the wrong parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has the wrong country" % row_id)
        if item.get("kind") not in EXPECTED_KINDS:
            raise ValueError("%s has an unsupported kind" % row_id)
        if item.get("rank") not in EXPECTED_RANKS:
            raise ValueError("%s has an unsupported rank" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks name or seat data" % row_id)
        if not any("\u0370" <= char <= "\u03ff" for char in item["local"]):
            raise ValueError("%s lacks a Greek source name" % row_id)
        if any(FORBIDDEN_PUNCTUATION.search(text)
               for text in walk_strings(item)):
            raise ValueError("%s contains forbidden punctuation" % row_id)
        for phone in item.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            if len(digits) < 7 or len(digits) > 15:
                raise ValueError("%s carries an invalid phone" % row_id)
        for email in item.get("emails") or []:
            if not EMAIL_RE.fullmatch(email):
                raise ValueError("%s carries an invalid email" % row_id)
        signature = (item["parent"], unicase(item["local"]),
                     unicase(item["seat"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s" %
                             (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        ranks[item["rank"]] += 1
        kinds[item["kind"]] += 1
        owners[item["parent"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" %
                         (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Ilia English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Ilia rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Ilia kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Ilia parent totals drifted")
    coverage = (
        sum(bool(x.get("phones") or x.get("emails") or x.get("site"))
            for x in result),
        sum(bool(x.get("phones")) for x in result),
        sum(len(x.get("phones") or []) for x in result),
        sum(bool(x.get("emails")) for x in result),
        sum(len(x.get("emails") or []) for x in result),
        sum(bool(x.get("site")) for x in result),
        sum(bool(x.get("address")) for x in result),
    )
    expected = (
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected:
        raise ValueError("Ilia contact coverage drifted: %r" % (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf",
        "Accept-Encoding": "identity",
    })
    with urlopen(request, timeout=60) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return url, payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", unicase(text))


def compact_digits(value):
    return re.sub(r"\D", "", value)


def check_live_sources():
    required = {url for row in ROWS for url in row.get("sources", [])}
    cache = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        futures = [pool.submit(fetch, url) for url in sorted(required)]
        for future in concurrent.futures.as_completed(futures):
            url, payload, content_type = future.result()
            if url.lower().endswith(".pdf"):
                if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                    raise ValueError("live source is not a PDF: %s" % url)
                cache[url] = payload
            else:
                if ("html" not in content_type and
                        not payload.lstrip().startswith(b"<")):
                    raise ValueError("live source is not HTML: %s" % url)
                cache[url] = normalized_page(payload)
    for row in ROWS:
        pages = " ".join(
            cache[url] for url in row["sources"]
            if isinstance(cache[url], str)
        )
        digit_pages = compact_digits(pages)
        for marker in row.get("live_markers") or []:
            marker_digits = compact_digits(marker)
            if marker_digits and len(marker_digits) >= 7:
                if marker_digits not in digit_pages:
                    raise ValueError("%s lacks live marker %s" %
                                     (row["id"], marker))
            elif unicase(marker) not in pages:
                raise ValueError("%s lacks live marker %s" %
                                 (row["id"], marker))
        for phone in row.get("phones") or []:
            if compact_digits(phone) not in digit_pages:
                raise ValueError("%s lacks live phone %s" %
                                 (row["id"], phone))
        for email in row.get("emails") or []:
            if unicase(email) not in pages:
                raise ValueError("%s lacks live email %s" %
                                 (row["id"], email))
    print("Ilia live sources: %d URLs checked" % len(required))


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
    elif args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print("Ilia: 198 exact bodies; 185 current named parishes, "
              "1 regulated pilgrimage church, 7 monasteries, and "
              "5 hesychasteria")
        print("Contacts: 174 bodies; 176 phones; no emails; "
              "no independent body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Ilia: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
