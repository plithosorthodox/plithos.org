#!/usr/bin/env python3
"""Validate exact named Ioannina bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_ioannina_country.py --check
    python tools/directory_ioannina_country.py --check-live
    python tools/directory_ioannina_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CHECKED = "2026-11-15"
PARENT = "ep-ioannina"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "ioannina_country.json"
)

LOCAL_BASE = "https://imioanninon.gr"
LOCAL_DIRECTORY_URL = LOCAL_BASE + "/enories-efimerioi/"
LOCAL_MONASTERIES_URL = LOCAL_BASE + "/ieres-mones/"
LOCAL_REGIONS_URL = LOCAL_BASE + "/arxieratikes-perifereies/"
EP_URL = "https://ec-patr.org/entities/iera-mitropoli-ioanninon/"
COG_URL = (
    "https://ecclesiagreece.gr/ecclesiajoomla/index.php/en/dioceses/"
    "holy-metropolis-of-ioannina"
)
LEGAL_URL = (
    "https://www.ecclesiagreece.gr/greek/press/ekklisia/"
    "material/1996_11_16.pdf"
)
LOCAL_LEGAL_URL = LOCAL_BASE + "/wp-content/uploads/2023/10/apof_042.pdf"
PAISIOS_CURRENT_URL = (
    LOCAL_BASE + "/epikairotita/"
    "%CE%B7-%CE%B5%CE%BF%CF%81%CF%84%CE%B7-%CF%84%CE%BF%CF%85-"
    "%CE%B1%CE%B3%CE%B9%CE%BF%CF%85-%CF%80%CE%B1%CF%8A%CF%83%CE%B9%CE%BF%CF%85-"
    "%CF%84%CE%BF%CF%85-%CE%B1%CE%B3%CE%B9%CE%BF%CF%81%CE%B5%CE%B9%CF%84-2/"
)


# Exact source order from the current Metropolis directory. Fields are:
# Greek directory title, phone cell, email cell, region, optional detail page.
DIRECTORY_SOURCE = r"""
Αβγό - Αγ. Δημήτριος|6932376441|enoriaavgo@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Αγία Αναστασία - Αγία Αναστασία|6945514835|mororospetra@yahoo.gr|ΣΤ΄ Δωδώνης|
Αγία Τριάδα - Αγία Παρασκευή|6973861933|-|Ζ΄ Ξηροβουνίου|
Άγιος Ανδρέας - Αγ. Ανδρέας|6979212177|-|ΣΤ΄ Δωδώνης|
Αγ. Ιωάννης - Αγ. Ιωάννης ὁ Θεολόγος|6977494624|ag.ioannistheologos26@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/ieros-naos-agiou-ioannou-enorias/
Άγιος Ιωάννης «Μπονίλα» - Αγ. Ιωάννης|2651022206|ini.agios.ioannis.anatolis@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/parekklhsio-agiou-ioannou/
Αγία Μαρίνα - Αγία Μαρίνα|2651025949|agiamarina_ioa@yahoo.gr|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/ieros-naos-agias-marinhs/
Άγιος Μηνάς - Γέννηση της Θεοτόκου|6984421270|lefteris.pexomatis@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Άγιος Νικόλαος - Άγιος Νικόλαος|6942708928|agiosnikolaosdodonis@gmail.com|ΣΤ΄ Δωδώνης|
Άγιος Νικόλαος «Αγοράς» - Αγ. Νικόλαος|2651027659|inagiounikolaouagoras@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/ieros-naos-agiou-nikolaou-agoras/
Άγιος Νικόλαος «Κοπάνων» - Αγ. Νικόλαος|2651022234|agiosnikolaos2@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/agios-nikolaos-kopanvn/
Άγιος Σεραφείμ - Άγιοι Απόστολοι|2651074189|agioiapostoloi.ioa@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/agios-serafeim-agioi-apostoloi/
Αετόπετρα - Αγ. Παρασκευή|6948099688|lamroskolokas@gmail.com|Δ΄ Καλαμά|
Αετορράχη - Αγ. Γεώργιος|6970596195|-|Ι΄ Κατσανοχωρίων|
Αλεποχώρι Μπότσαρη - Κοίμηση της Θεοτόκου|6978032162|dimitrisiama@gmail.com|Ε΄ Λάκκας Σουλίου|
Αμπελιά - Αγ. Νικόλαος|6976700398|-|Β΄ Λεκανοπεδίου Ιωαννίνων|
Αμφιθέα - Αγ. Ανάργυροι|6940981938|enoriaamfitheas@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ανάργυροι - Κοίμηση της Θεοτόκου|6975872366|nikostsitses48@gmail.com|Η΄ Γραμμενοχωρίων|
Ανατολή - Της Του Θεού Σοφίας|6938884409|agiasophiaan@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/anatoli-ths-tou-theou-sofias/
Ανατολική - Αγ. Δημήτριος|6978492378|b3klouras@hotmail.com|ΙΑ΄ Συρράκου|
Ανήλιο - Αγ. Παρασκευή|6947664890|dimitrisvar77@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Ανθοχώρι Δωδώνης - Κοίμηση της Θεοτόκου|6940185717|-|ΣΤ΄ Δωδώνης|
Ανθοχώρι Μετσόβου - Αγ. Παρασκευή|6970796674|giannismetsios@yahoo.gr|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Ανθρακίτης - Κοίμηση της Θεοτόκου|6940090012|kladis.g@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Άνω Βίτσα - Παμμ. Ταξιαρχών|6984332264|xristosklad@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Άνω Λαψίστα - Αγ. Νικόλαος|6944514179|ag.nik.lapsista@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Άνω Μουσιωτίτσα - Αγ. Γεώργιος|6986535229|-|Ζ΄ Ξηροβουνίου|
Άνω Πεδινά - Αγ. Δημήτριος|6984332264|xristosklad@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|https://imioanninon.gr/ano-pedina-ag-dhmhtrios/
Ανώγειο - Αγ. Νικόλαος|6981786884|konsfrin@hotmail.gr|Ζ΄ Ξηροβουνίου|
Άρδοση - Αγ. Παρασκευή|6948380697|lamprosgeorgokitsios@gmail.com|Ε΄ Λάκκας Σουλίου|
Αρίστη - Κοίμηση της Θεοτόκου|6984421270|enoriaaristis@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Αρτοπούλα - Αγ. Γεώργιος|6945514835|mororospetra@yahoo.gr|ΣΤ΄ Δωδώνης|https://imioanninon.gr/artopoula-ag-georgios/
Αρχιμανδρείο - Κοίμηση της Θεοτόκου|2651073331|inarchim@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/arximandreio-koimhsh-ths-theotokou/
Ασβεστοχώρι - Αγ. Δημήτριος|6975872366|agdimitriosasv@gmail.com|Η΄ Γραμμενοχωρίων|
Ασπράγγελοι - Αγ. Νικόλαος|6942228828|inagnaspraggelon@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Ασπροχώρι - Κοίμηση της Θεοτόκου|6945514835|koimhshstheotokouasproxoriou@gmail.com|ΣΤ΄ Δωδώνης|
Ασφάκα - Αγ. Παρασκευή|6972109310|kostakitsisbasilis@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/asfaka-ag-paraskeyh/
Αχλαδέα - Κοίμηση της Θεοτόκου|6947525824|-|Ε΄ Λάκκας Σουλίου|
Βαγενήτι - Αγ. Γεώργιος|6986515112|kosmaspylis@yahoo.gr|Η΄ Γραμμενοχωρίων|
Βαθύπεδο - Κοίμηση της Θεοτόκου|6906150683|dimitrios.peristeris@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Βαλανιδιά - Αγ. Νικόλαος|6942708928|demetriosraptes33@gmail.com|ΣΤ΄ Δωδώνης|
Βαπτιστής - Αγ. Ιωάννης|6948804411|xristoxaris@gmail.com|ΙΑ΄ Συρράκου|https://imioanninon.gr/baptistis-ag-ioannis/
Βαρλαάμ - Αγ. Νικόλαος|6973861933|-|Ζ΄ Ξηροβουνίου|
Βαρυάδες - Γέννηση της Θεοτόκου|6973291647|-|Ζ΄ Ξηροβουνίου|https://imioanninon.gr/baruades-gennisi-tis-theotokou/
Βασιλική - Αγ. Τρύφων|6982217980|koutsogiannakis68@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/basiliki-ag-trufvn/
Βασιλόπουλο - Αγ. Απόστολοι|6974485443|tsekos.swtiris@gmail.com|Δ΄ Καλαμά|
Βατατάδες - Αγ. Νικόλαος|6955447504|pathrth@gmail.com|Δ΄ Καλαμά|
Βλαχάτανος - Αγ. Γεώργιος|6955447504|pathrth@gmail.com|Δ΄ Καλαμά|
Βοτονόσι - Μεταμόρφωση του Σωτήρος|6970796674|inmsvotonosiou@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Βουλιάσα - Γέννηση της Θεοτόκου|6972318904|-|Ζ΄ Ξηροβουνίου|
Βουνοπλαγιά - Αγ. Δημήτριος|6945828171|evounoplagia_agdim@outlook.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/bounoplagia-ag-dimitrios/
Βουτσαράς - Αγ. Δημήτριος|6940747902|-|Θ΄ Ραδοβιζίου|
Βραδέτο - Γέννηση της Θεοτόκου|6944817631|kaxiras.nikolaos@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Βρυσοχώρι - Αγ. Χαράλαμπος|6974319994|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Βωβούσα - Αγ. Γεώργιος|6943464362|pvntinos87@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Γαβρισιοί - Αγ. Παρασκευή|6951822201|paterhd5@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/gavrisioi-ag-paraskeuh/
Γεωργάνοι - Κοίμηση της Θεοτόκου|6976359456|georgiosego8@gmail.com|Ε΄ Λάκκας Σουλίου|
Γηροκομείο - Αγ. Κων/νος και Ελένης|2651073331|inkonstantinouelenis@gmail.com|Α΄ Πόλεως Ιωαννίνων|
Γκρίμποβο - Αγ. Αθανάσιος|6984160844|spapatheodorou80@yahoo.com|Θ΄ Ραδοβιζίου|
Γορίτσα - Αγ. Δημήτριος|6976700398|-|Β΄ Λεκανοπεδίου Ιωαννίνων|
Γουργιάνιστα - Αγ. Παρασκευή|6984160844|spapatheodorou80@yahoo.com|Θ΄ Ραδοβιζίου|
Γραμμένο - Παμμ. Ταξιαρχῶν|6977697708|ingrammenou@gmail.com|Η΄ Γραμμενοχωρίων|
Γρανιτσοπούλα - Αγ. Κυριακή|6945880125|-|Δ΄ Καλαμά|
Γρεβενήτι - Κοίμηση της Θεοτόκου|6947664890|inkthgrevenitiou@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Δαφνούλα - Πρ. Ηλίας|6976074006|chrisioan59@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Δαφνόφυτο - Αγ. Κυριακή|6983661800|alexpap272@gmail.com|Δ΄ Καλαμά|
Δαφνωτή - Αγ. Νικόλαος|6971742652|-|Ι΄ Κατσανοχωρίων|
Δελβινακόπουλο - Αγ. Μηνάς|6971612449|katerina_zikou@yahoo.gr|Δ΄ Καλαμά|
Δεμάτι - Αγ. Νικόλαος|6937084166|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Δερβίζιανα - Αγ. Νικόλαος|6976359456|georgiosego8@gmail.com|Ε΄ Λάκκας Σουλίου|
Δεσποτικό - Αγ. Τριάδα|6974485443|tsekos.swtiris@gmail.com|Δ΄ Καλαμά|
Δίκορφο - Αγ. Μηνάς|6940090012|kladis.g@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Δίλοφο - Κοίμηση της Θεοτόκου|6937453515|steftiog@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Διπόταμος - Κοίμηση της Θεοτόκου|6946483508|lefterisgrigor25@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Δόλιανη - Κοίμηση της Θεοτόκου|6932847945|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Δομολεσσά - Αγ. Νικόλαος|6976803888|-|Θ΄ Ραδοβιζίου|
Δραγοψά - Αγ. Νικόλαος|6974141366|pgkostakitsis@gmail.com|ΣΤ΄ Δωδώνης|
Δραμεσιοί - Αγ. Ανάργυροι|6974141366|pgkostakitsis@gmail.com|ΣΤ΄ Δωδώνης|
Δροσοχώρι - Αγ. Παντελεήμων|6977403251|metrogiannesd@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Δωδώνη - Αγ. Θεόδωρος|6974141366|pgDodoni@gmail.com|ΣΤ΄ Δωδώνης|
Εκκλησοχώρι - Αγ. Αθανάσιος|6971612449|-|Δ΄ Καλαμά|
Ελάτη - Αγ. Γεώργιος|6942228828|jap.papadimitriou@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Ελατοχώρι - Αγ. Γεώργιος|6943464362|pvntinos87@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Έλαφος - Γέννηση της Θεοτόκου|6948380697|lamprosgeorgokitsios@gmail.com|Ε΄ Λάκκας Σουλίου|
Ελαφότοπος - Αγ. Νικόλαος|6944809615|hrisosilias@yahoo.gr|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Ελεούσα - Κοίμηση της Θεοτόκου|2651063704|koim.theo.eleousas@hotmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ελευθεροχώρι - Αγ. Γεώργιος|6940185717|-|ΣΤ΄ Δωδώνης|
Ελληνικό - Αγία Τριάδα|6973219422|-|Ι΄ Κατσανοχωρίων|
Επισκοπικό - Κοίμηση της Θεοτόκου|6948209005|enoriaepiskopikou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ζίτσα - Αγ. Νικόλαος|6983661800|agnikzitsas@gmail.com|Δ΄ Καλαμά|
Ζωοδόχος - Αγ. Παρασκευή|6945706708|enoriazwodoxou@outlook.com|Η΄ Γραμμενοχωρίων|
Ζωτικό - Κοίμηση της Θεοτόκου|6947784065|-|ΣΤ΄ Δωδώνης|
Ηλιόκαλη - Αγ. Παρασκευή|6976074006|chrisioan59@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ηλιοχώρι - Αγ. Νικόλαος|6974319994|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Θεριακήσι - Αγ. Γεώργιος|6973291647|-|Ζ΄ Ξηροβουνίου|
Ιερομνήμη - Αγ. Τριάδα|6973802375|konstantinosgiannakos95@gmail.com|Δ΄ Καλαμά|
Ιτέα - Αγ. Παρασκευή|6937084166|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Καβαλλάρι - Αγία Τριάδα|6939504652|giannessioules6@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Καλέντζι - Γέννηση της Θεοτόκου|6976295858|-|Ι΄ Κατσανοχωρίων|
Καλλιθέα Σίτσαινα - Αγ. Παρασκευή|6937084166|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Καλοχώρι - Κοίμηση της Θεοτόκου|6996954554|-|Θ΄ Ραδοβιζίου|
Καλπάκι - Αγ. Σκέπη|6939584186|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Καλωτάς - Μεταμόρφωση του Σωτήρος|6942228828|jap.papadimitriou@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Καπέσοβο - Αγ. Νικόλαος|6944817631|kaxiras.nikolaos@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Καρδαμίτσια - Προφήτης Ηλίας|6932240440|proph.ilias@hotmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/kardamitsia-profitis-hlias/
Καρίτσα - Κοίμηση της Θεοτόκου|6996556818|-|Δ΄ Καλαμά|
Καρυές Ζαγορίου - Αγ. Παρασκευή|6937084166|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Καστανώνας - Αγ. Ανάργυροι|6943464362|pvntinos87@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Καστρίτσα - Αγ. Γεώργιος|6944771880|-|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/kastritsa-ag-georgios/
Κάστρο Ἰωαννίνων - Άγιοι Ανάργυροι|6989228404|ag.anargyroi.kastrou@gmail.com|Α΄ Πόλεως Ιωαννίνων|
Καταμάχη - Γέννηση του Προδρόμου|6942708928|demetriosraptes33@gmail.com|ΣΤ΄ Δωδώνης|
Καταρράκτης - Αγ. Γεώργιος|6955447504|pathrth@gmail.com|Δ΄ Καλαμά|
Κατσικάς - Κοίμηση της Θεοτόκου|6945735162|enoriakatsika@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/katsikas-koimhsh-ths-theotokou/
Κάτω Βίτσα - Κοίμηση της Θεοτόκου|6984332264|envitsa@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Κάτω Λαψίστα - Αγ. Γεώργιος|6972109310|A.GeorgiosK.Lapsista@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Κάτω Λίππα - Μεταμόρφωση του Σωτήρος|6948380697|lamprosgeorgokitsios@gmail.com|Ε΄ Λάκκας Σουλίου|
Κάτω Μουσιωτίτσα - Αγ. Νικόλαος|6948889642|ioannismpoutzias@gmail.com|Ζ΄ Ξηροβουνίου|
Κάτω Πεδινά - Αγ. Αθανάσιος|6984332264|xristosklad@hotmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|https://imioanninon.gr/katv-pedina-ag-athanasios/
Κερασέα - Αγ. Παρασκευή|6984160844|spapatheodorou80@yahoo.com|Θ΄ Ραδοβιζίου|
Κηπίνα - Αγ. Νικόλαος|6976046234|klearchossakkas@gmail.com|ΙΑ΄ Συρράκου|
Κήποι - Αγ. Νικόλαος|6940350435|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Κλεισούρα - Παμμ. Ταξιαρχών|6981786884|konsfrin@hotmail.gr|Ζ΄ Ξηροβουνίου|
Κληματιά - Αγ. Δημήτριος|6996556818|-|Δ΄ Καλαμά|
Κοκκινόχωμα - Αγ. Γεώργιος|6971612449|katerina_zikou@yahoo.gr|Δ΄ Καλαμά|
Κοντινοί Καραδήμα - Μεταμόρφωση του Σωτήρος|6977403251|metrogiannesd@gmail.com|ΙΑ΄ Συρράκου|
Κόντσικα - Αγ. Γεώργιος|6975872366|agiosgeorgioskontsikas@gmail.com|Η΄ Γραμμενοχωρίων|
Κοπάνη - Κοίμηση της Θεοτόκου|6930477370|-|Ζ΄ Ξηροβουνίου|https://imioanninon.gr/kopani-koimisi-ths-theotokou/
Κορύτιανη - Αγ. Συμεών|6944820617|k_siontis@yahoo.gr|Ι΄ Κατσανοχωρίων|
Κοσμηρά - Aγ. Παρασκευή|6979124404|-|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/kosmira-ag-paraskeuh/
Κουκλέσι - Αγ. Νικόλαος|6981786884|konsfrin@hotmail.gr|Ζ΄ Ξηροβουνίου|
Κουκούλι - Κοίμηση της Θεοτόκου|6944817631|kaxiras.nikolaos@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Κουμαριά - Κοίμηση της Θεοτόκου|6982983961|-|ΣΤ΄ Δωδώνης|
Κούρεντα - Αγ. Γεώργιος|6940747902|-|Θ΄ Ραδοβιζίου|
Κουτσελιό - Κοίμηση της Θεοτόκου|6932379192|pater.georgiossioulas@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Κρανούλα - Αγ. Παρασκευή|6908278208|agparaskevikranoula@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/kranoula-ag-paraskeyh/
Κράψη - Αγ. Νικόλαος|6978492378|b3klouras@hotmail.com|ΙΑ΄ Συρράκου|
Κρύα Λυκοτρίχι - Αγ. Ιωάννης|6972540041|enoriakryaslykotrixiou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/krua-lykotrixi-ag-ioannis/
Κρυόβρυση - Παμμ. ταξιαρχών|6972109310|kostakitsisbasilis@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/kryovrysi-pamm-taxiarxvn/
Κρυφοβό - Γέννηση της Θεοτόκου|6973291647|-|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/kryfobo-gennisi-ths-theotokou/
Κωστάνιανη - Παμμ. Ταξιαρχών|6978327749|-|ΣΤ΄ Δωδώνης|
Λάϊστα - Παμμ. Ταξιαρχών|6974319994|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Λάλιζα - Αγ. Παρασκευή|6976803888|-|Θ΄ Ραδοβιζίου|
Λεπτοκαρυά - Αγ. Νικόλαος|6984421270|lefteris.pexomatis@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Λευκοθέα - Αγ. Απόστολοι|6971612449|katerina_zikou@yahoo.gr|Δ΄ Καλαμά|
Λιγκιάδες - Αγ. Γεώργιος|6982217980|koutsogiannakis68@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Λιγοψά - Αγ. Νικόλαος|6983661800|alexpap272@gmail.com|Δ΄ Καλαμά|
Λίθινο - Αγ. Κων/νος & Ελένη|6974485443|tsekos.swtiris@gmail.com|Δ΄ Καλαμά|
Λίππα - Αγ. Γεώργιος|6948804411|xristoxaris@gmail.com|ΣΤ΄ Δωδώνης|
Λογγάδες - Κοίμηση της Θεοτόκου|6978103219|ierosnaoskoim.theotokouloggadon@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Λοζιανά Διχούνι - Αγ. Κυριακή|6982152472|agiakiriakiloziana@gmail.com|Θ΄ Ραδοβιζίου|
Λοφίσκος - Κοίμηση της Θεοτόκου|6977697708|george.papp3@gmail.com|Η΄ Γραμμενοχωρίων|
Λύγγος - Κοίμηση της Θεοτόκου|6976784679|vasileiospeppas1970@gmail.com|Η΄ Γραμμενοχωρίων|
Μαζαράκι - Αγ. Νικόλαος|6973802375|agiosnikolaosmazarakiou@gmail.com|Δ΄ Καλαμά|
Μάζια - Μεταμόρφωση του Σωτήρος|6984274819|papatsodoulos61@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Μακρίνο - Αγ. Νικόλαος|26560315436988527499|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μανασσής - Αγ. Γεώργιος|6940090012|inaggeorgioumanassi@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|https://imioanninon.gr/manassis-ag-georgios/
Μαντείο - Αγ. Δημήτριος|6976700398|-|ΣΤ΄ Δωδώνης|
Μανωλιάσα - Αγ. Γεώργιος|6976700398|-|Β΄ Λεκανοπεδίου Ιωαννίνων|
Μάρμαρα - Αγ. Νικόλαος|6930771100|agiosnikolaosmarmaron@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/marmara-ag-nikolaou/
Μεγάλη Γότιστα - Αγ. Απόστολοι|6906150683|dimitrios.peristeris@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μεγάλο Γαρδίκι - Αγ. Νικόλαος|6972547580|spirosmastoras02@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Μεγάλο Περιστέρι - Κοίμηση της Θεοτόκου|6906150683|dimitrios.peristeris@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μελιά - Εισόδια της Θεοτόκου|6930477370|-|Ζ΄ Ξηροβουνίου|https://imioanninon.gr/melia-eisodia-tis-theotokou/
Μελιγγοί - Κοίμηση της Θεοτόκου|6944361731|steliossimpas@hotmail.com|ΣΤ΄ Δωδώνης|
Μεσοβούνι - Κοίμηση της Θεοτόκου|6972412917|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Μεταμόρφωση - Αγ. Κοσμάς|6976775590|-|Β΄ Λεκανοπεδίου Ιωαννίνων|
Μέτσοβο - Αγ. Παρασκευή|6932318461|Inapmet@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μέτσοβο - Αγ. Δημήτριος|6941415981|inagdime@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μηλιά - Κοίμηση της Θεοτόκου|6977742561|kimisimileas@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μηλιωτάδες - Γέννηση της Θεοτόκου|6937084166|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μητροπολιτικός Ναός - Άγιος Αθανάσιος|2651027632|mitropolitikos_ioa@yahoo.gr|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/mhtropolitikos-naos-ag-athanasioy/
Μικρή Γότιστα - Αγ. Νικόλαος|6906150683|dimitrios.peristeris@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μικρό Περιστέρι - Κοίμηση της Θεοτόκου|6979817827|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μιχαλίτσι - Αγ. Νικόλαος|6948804411|xristoxaris@gmail.com|ΙΑ΄ Συρράκου|
Μονοδένδρι - Αγ. Αθανάσιος|6944809615|enoriamonodendriou@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Μονολίθι - Αγ. Τριάδα|6974852368|-|Ι΄ Κατσανοχωρίων|
Μουζακαίοι - Αγ. Γεώργιος|6977518269|-|ΙΑ΄ Συρράκου|
Μουκοβίνα - Αγ. Αθανάσιος|6978032162|dimitrisiama@gmail.com|Ε΄ Λάκκας Σουλίου|
Μπαλντούμα - Αγ. Νικόλαος|6979817827|-|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Μπαουσιοί - Κοίμηση της Θεοτόκου|6945514835|mororospetra@yahoo.gr|ΣΤ΄ Δωδώνης|
Μπάφρα - Αγ. Παρασκευή|6946901570|enoriaagiasparaskevismpafras@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/bafra-ag-paraskeyh/
Μπεστιά - Εισόδια της Θεοτόκου|6947525824|-|Ε΄ Λάκκας Σουλίου|
Μπιζάνι - Αγ. Γεώργιος|6932376441|lakasgian@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/bizani-ag-georgios/
Μυροδάφνη - Κοίμηση της Θεοτόκου|6946591562|-|Ζ΄ Ξηροβουνίου|
Νεγάδες - Αγ. Γεώργιος|6946483508|lefterisgrigor25@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|https://imioanninon.gr/negades-ag-georgios/
Νεγράδες - Κοίμηση της Θεοτόκου|6939584186|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Νεοκαισάρεια - Αγ. Βασίλειος|6942680957|inavneok@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/neokaisareia-ag-basileios/
Νεοχώρι - Αγ. Γεώργιος|6972547580|ag.georgios.neoxori@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Νεοχωρόπουλο - Αγ. Σπυρίδων|6973743242|agspyridvnneochoropoulou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/neoxvropoulo-ag-spuridvn/
Νήσος - Κοίμηση της Θεοτόκου|6984094932|enoriakoimisewsnisou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Νίστορα Πάτερο - Αγ. Νικόλαος|6946798815|-|Ι΄ Κατσανοχωρίων|
Οίκος Νεομάρτυρος Αγίου Γεωργίου|2651024539|-|Α΄ Πόλεως Ιωαννίνων|
Παλαιοχώρι Μπότσαρη - Γενέθλιον του Προδρόμου|6932361917|-|Ε΄ Λάκκας Σουλίου|
Παλαιοχώρι Συρράκου - Γέννηση της Θεοτόκου|6976046234|klearchossakkas@gmail.com|ΙΑ΄ Συρράκου|
Παλιουρή - Γενέθλιο του Προδρόμου|6975858762|-|Δ΄ Καλαμά|
Πάπιγκο - Αγ. Βλάσιος|6972412917|-|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Παρδαλίτσα - Αγ. Θεόδωροι|6947784065|-|ΣΤ΄ Δωδώνης|
Πεδινή - Κοίμηση της Θεοτόκου|6986626525|ieros.naos.pedinis@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/penteli-drosia-ag-kvnstantinos-kai-eleni/
Πεντέλη Δροσιά - Αγ. Κων/νος και Ελένη|6949645275|inpentelisdrosias@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/%CF%80%CE%B5%CE%BD%CF%84%CE%AD%CE%BB%CE%B7-%CE%B4%CF%81%CE%BF%CF%83%CE%B9%CE%AC-%CE%B1%CE%B3-%CE%BA%CF%89%CE%BD-%CE%BD%CE%BF%CF%82-%CE%BA%CE%B1%CE%B9-%CE%B5%CE%BB%CE%AD%CE%BD%CE%B7/
Πεντόλακκος - Άγιοι Θεόδωροι|6973291647|-|Ζ΄ Ξηροβουνίου|
Πέραμα - Αγ. Χαράλαμπος|6936712251|agharalabos@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Περάτη - Προφ. Ηλίας|6975872366|nikostsitses48@gmail.com|Η΄ Γραμμενοχωρίων|
Πέρδικα - Αγ. Παρασκευή|6946591562|-|Ζ΄ Ξηροβουνίου|
Περίβλεπτος - Αγ. Παρασκευή|6980388344|mikearxalos29@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Περίβλεπτος - Κοίμηση της Θεοτόκου|2651041617|inperivleptou@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/perivleptos-koimisi-ths-theotokoy/
Πεστά - Κοίμηση της Θεοτόκου|6973861933|-|Ζ΄ Ξηροβουνίου|
Πετούσι - Κοίμηση της Θεοτόκου|6942708928|demetriosraptes33@gmail.com|ΣΤ΄ Δωδώνης|
Πέτρα - Αγ. Νικόλαος|6906150683|agnikolaospetras@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Πετράλωνα - Αγ. Παρασκευή|6986515112|kosmaspylis@yahoo.gr|Η΄ Γραμμενοχωρίων|
Πετροβούνι - Παμμ. Ταξιαρχών|6976046234|klearchossakkas@gmail.com|ΙΑ΄ Συρράκου|
Πετσάλι - Γέννηση της Θεοτόκου|6984274819|ingennesseostheotokoupetsaliou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/petsali-gennisi-tis-theotokou/
Πηγάδια - Αγ. Παρασκευή|6974852368|-|Ι΄ Κατσανοχωρίων|
Πλαίσια - Κοίμηση της Θεοτόκου|6976295858|-|Ι΄ Κατσανοχωρίων|
Πλατάνια - Αγ. Νικόλαος|6974141366|pgkostakitsis@gmail.com|ΣΤ΄ Δωδώνης|
Πλατανιά Γερακάρι - Προφ. Ηλίας|6985854369|giannistzitzi@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Πλατανούσα - Κοίμηση της Θεοτόκου|6974852368|-|Ι΄ Κατσανοχωρίων|
Πολύγυρος - Αγ. Κυριακή|6976784679|poligirosbasiliospep@gmail.com|Η΄ Γραμμενοχωρίων|
Πολύλοφος - Απ. Πέτρος|6976784679|vasileiospeppas1970@gmail.com|Η΄ Γραμμενοχωρίων|
Πολυστάφυλλο - Αγ. Γεώργιος|6978032162|dimitrisiama@gmail.com|Ε΄ Λάκκας Σουλίου|
Ποτιστικά - Αγ. Νικόλαος|6976046234|klearchossakkas@gmail.com|ΙΑ΄ Συρράκου|
Προσήλιο - Αγ. Βλάσιος|6976046234|klearchossakkas@gmail.com|ΙΑ΄ Συρράκου|
Προσκυνηματικός Ναός Νεομάρτυρος Αγ. Γεωργίου|2651020407|ipn.agiougeorgiou@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/proskinimatikos-naos-neomartyros/
Πρωτόπαππας - Αγ. Νικόλαος|6944514179|ziakas72@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ραβένια - Κοίμηση της Θεοτόκου|6948209005|vafeaspetros@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ραδοβίζι - Αγ. Τριάδα|6996954554|-|Θ΄ Ραδοβιζίου|
Ράϊκο - Αγ. Παρασκευή|6948099688|lamroskolokas@gmail.com|Δ΄ Καλαμά|
Ραψαίοι - Γέννηση της Θεοτόκου|6942951145|-|Ζ΄ Ξηροβουνίου|
Ριάχοβο - Αγ. Τριάδα|-|-|Δ΄ Καλαμά|
Ριζό - Τρείς Ιεράρχες|6945880125|-|Δ΄ Καλαμά|
Ροδοτόπι - Αγ. Τριάδα|6972547580|agiatriadarodotopiou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Ρωμανό - Γέννηση της Θεοτόκου|6947525824|-|Ε΄ Λάκκας Σουλίου|
Σεισμόπληκτα - Απόστολος Παύλος|6948356769|agpavlosseismoplhkta@gmail.com|Α΄ Πόλεως Ιωαννίνων|https://imioanninon.gr/seismoplikta-apostolos-paulos/
Σέλτσανα - Αγ. Γεώργιος|6984160844|spapatheodorou80@yahoo.com|Θ΄ Ραδοβιζίου|
Σενίκο - Αγ. Παρασκευή|6976803888|-|Θ΄ Ραδοβιζίου|
Σερβιανά - Παμμ. Ταξιαρχών|6978314199|taksiarxes@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|https://imioanninon.gr/serviana-pamm-taxiarxvn/
Σιστρούνι - Αγ. Βασιλείου|6976359456|georgiosego8@gmail.com|Ε΄ Λάκκας Σουλίου|https://imioanninon.gr/sistrouni-ag-basileiou/
Σκαμνέλι - Αγ. Απόστολοι|6944817631|kaxiras.nikolaos@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Σκλίβανη - Αγ. Γεώργιος|6974630725|tzamanos@yahoo.com|Ζ΄ Ξηροβουνίου|
Σκούπα - Κοίμηση της Θεοτόκου|6971742652|-|Ι΄ Κατσανοχωρίων|
Σμυρτιά - Αγ. Νικόλαος|6981786884|inagiounikolaousmyrtias@gmail.com|Ε΄ Λάκκας Σουλίου|
Σουλόπουλο - Αγ. Γεώργιος|6975858762|-|Δ΄ Καλαμά|
Σταυράκι - Αγ. Κων/νος & Ελένη|6937453515|enoriastayrakiou@gmail.com|Β΄ Λεκανοπεδίου Ιωαννίνων|
Συρράκο - Αγ. Νικόλαος|6976046234|klearchossakkas@gmail.com|ΙΑ΄ Συρράκου|
Τέρροβο - Κοίμηση της Θεοτόκου|6942951145|-|Ζ΄ Ξηροβουνίου|
Τρίστενο - Αγ. Γεώργιος|6937444025|ag.gewrgios.tristenou@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Τσεπέλοβο - Αγ. Νικόλαος|6944817631|ag.nikolaos.tsepelovou@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Φανερωμένη - Αγ. Τριάδα|6971742652|-|Ι΄ Κατσανοχωρίων|
Φλαμπουράρι - Αγ. Νικόλαος|6943464362|pvntinos87@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Φορτόσι - Εισόδια της Θεοτόκου|6977154791|-|Ι΄ Κατσανοχωρίων|
Φραγκάδες - Αγ. Δημήτριος|6984421270|lefteris.pexomatis@gmail.com|ΙΒ΄ Κεντρικού & Δυτ. Ζαγορίου|
Φωτεινό - Αγ. Νικόλαος|6948099688|lamroskolokas@gmail.com|Δ΄ Καλαμά|
Χαροκόπι - Εισόδια της Θεοτόκου|6981394339|-|ΙΑ΄ Συρράκου|
Χίνκα - Κοίμηση της Θεοτόκου|6996954554|-|Θ΄ Ραδοβιζίου|
Χουλιαράδες - Αγ. Παρασκευή|6948804411|enories.vtzoumerkwn@gmail.com|ΙΑ΄ Συρράκου|
Χρυσοβίτσα - Κοίμηση της Θεοτόκου|6937444025|inkoim.chrysov@gmail.com|Γ΄ Μετσόβου - Ανατ. Ζαγορίου|
Ψήνα - Κοίμηση της Θεοτόκου|6945514835|mororospetra@yahoo.gr|ΣΤ΄ Δωδώνης|
"""


# Exact current bodies disclosed by the directory's own body detail pages.
# Fields are key, English seat, Greek seat, English name, Greek source name,
# rank, and source-page slug.
EXTRA_SOURCE = r"""
old-john-theologian-bisdonaki|Agios Ioannis|Άγιος Ιωάννης Μπισδουνάκι|Old Church of Saint John the Theologian|Παλαιός Ιερός Ναός Αγίου Ιωάννου του Θεολόγου|Historic Church|ieros-naos-agiou-ioannou-enorias
nectarios-bonila|Anatoli|Ανατολή|Saint Nectarios Chapel at Bonila|Ιερό Παρεκκλήσιο Αγίου Νεκταρίου Αιγίνης στον Άγιο Ιωάννη Μπονίλα|Chapel|parekklhsio-agiou-ioannou
john-new-martyr-agia-marina|Ioannina|Ιωάννινα|Saint John the New Martyr Chapel at Saint Marina|Ναΐδριο Νεομάρτυρος Αγίου Ιωάννου του εξ Ιωαννίνων στην Αγία Μαρίνα|Chapel|ieros-naos-agias-marinhs
eleutherius-nicholas-market|Ioannina|Ιωάννινα|Saint Eleutherius Chapel at Saint Nicholas of the Market|Παρεκκλήσιο Αγίου Ελευθερίου στον Ιερό Ναό Αγίου Νικολάου Αγοράς|Chapel|ieros-naos-agiou-nikolaou-agoras
sophia-faith-hope-love-anatoli|Anatoli|Ανατολή|Saint Sophia, Faith, Hope, and Love Church in Anatoli|Ιερός Ναός Αγίας Σοφίας και των Αγίων Πίστεως, Ελπίδος και Αγάπης Ανατολής|Church|anatoli-ths-tou-theou-sofias
george-new-martyr-anatoli|Anatoli|Ανατολή|Saint George and New Martyr George Chapel in Anatoli|Παρεκκλήσιο Αγίου Γεωργίου και Νεομάρτυρος Αγίου Γεωργίου Ανατολής|Chapel|anatoli-ths-tou-theou-sofias
panagia-soumela-anatoli|Anatoli|Ανατολή|Panagia Soumela Chapel in Anatoli|Παρεκκλήσιο Παναγίας Σουμελά Ανατολής|Chapel|anatoli-ths-tou-theou-sofias
paraskevi-ano-pedina|Ano Pedina|Άνω Πεδινά|Saint Paraskevi Monastic Church in Ano Pedina|Ναός Μονής Αγίας Παρασκευής Άνω Πεδινών|Monastic Church|ano-pedina-ag-dhmhtrios
kosmas-artopoula|Artopoula|Αρτοπούλα|Saint Kosmas Chapel in Artopoula|Παρεκκλήσιο Αγίου Κοσμά Αρτοπούλας|Chapel|artopoula-ag-georgios
marina-artopoula|Artopoula|Αρτοπούλα|Saint Marina Chapel in Artopoula|Παρεκκλήσιο Αγίας Μαρίνας Αρτοπούλας|Chapel|artopoula-ag-georgios
demetrius-ntouska-artopoula|Artopoula|Αρτοπούλα|Saint Demetrius Chapel at Ntouska in Artopoula|Παρεκκλήσιο Αγίου Δημητρίου στη Ντούσκα Αρτοπούλας|Chapel|artopoula-ag-georgios
prophet-elijah-artopoula|Artopoula|Αρτοπούλα|Prophet Elijah Chapel in Artopoula|Παρεκκλήσιο Προφήτη Ηλία Αρτοπούλας|Chapel|artopoula-ag-georgios
apostles-artopoula|Artopoula|Αρτοπούλα|Holy Apostles Chapel in Artopoula|Παρεκκλήσιο Αγίων Αποστόλων Αρτοπούλας|Chapel|artopoula-ag-georgios
paraskevi-artopoula|Artopoula|Αρτοπούλα|Saint Paraskevi Chapel in Artopoula|Παρεκκλήσιο Αγίας Παρασκευής Αρτοπούλας|Chapel|artopoula-ag-georgios
dormition-artopoula|Artopoula|Αρτοπούλα|Dormition of the Theotokos Chapel at Panagia in Artopoula|Ιερός Ναός Κοιμήσεως της Θεοτόκου Παναγίας Αρτοπούλας|Chapel|artopoula-ag-georgios
john-riganas-artopoula|Artopoula|Αρτοπούλα|Saint John Riganas Chapel in Artopoula|Παρεκκλήσιο Αγίου Ιωάννου του Ριγανά Αρτοπούλας|Chapel|artopoula-ag-georgios
nicholas-baptisti|Baptisti|Βαπτιστής|Saint Nicholas Chapel in Baptisti|Παρεκκλήσιο Αγίου Νικολάου Βαπτιστή|Chapel|baptistis-ag-ioannis
prophet-elijah-baptisti|Baptisti|Βαπτιστής|Prophet Elijah Chapel in Baptisti|Παρεκκλήσιο Προφήτη Ηλία Βαπτιστή|Chapel|baptistis-ag-ioannis
catherine-baptisti|Baptisti|Βαπτιστής|Saint Catherine Chapel in Baptisti|Παρεκκλήσιο Αγίας Αικατερίνης Βαπτιστή|Chapel|baptistis-ag-ioannis
holy-trinity-baptisti-chouliarades|Baptisti and Chouliarades|Βαπτιστής και Χουλιαράδες|Holy Trinity Chapel near Baptisti and Chouliarades|Παρεκκλήσιο Αγίας Τριάδας Βαπτιστή και Χουλιαράδων|Chapel|baptistis-ag-ioannis
holy-theodores-varyades|Varyades|Βαρυάδες|Holy Theodore Martyrs Chapel in Varyades|Παρεκκλήσιο Αγίων Θεοδώρων Βαρυάδων|Chapel|baruades-gennisi-tis-theotokou
george-varyades|Varyades|Βαρυάδες|Saint George Country Church in Varyades|Ιερός Ναός Αγίου Γεωργίου Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
apostles-varyades|Varyades|Βαρυάδες|Holy Apostles Country Church in Varyades|Ιερός Ναός Αγίων Αποστόλων Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
nicholas-varyades|Varyades|Βαρυάδες|Saint Nicholas Country Church in Varyades|Ιερός Ναός Αγίου Νικολάου Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
kyriaki-varyades|Varyades|Βαρυάδες|Saint Kyriaki Country Church in Varyades|Ιερός Ναός Αγίας Κυριακής Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
constantine-helen-varyades|Varyades|Βαρυάδες|Saints Constantine and Helen Country Church in Varyades|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
demetrius-varyades|Varyades|Βαρυάδες|Saint Demetrius Country Church in Varyades|Ιερός Ναός Αγίου Δημητρίου Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
kosmas-varyades|Varyades|Βαρυάδες|Saint Kosmas Country Church in Varyades|Ιερός Ναός Αγίου Κοσμά Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
prophet-elijah-varyades|Varyades|Βαρυάδες|Prophet Elijah Country Church in Varyades|Ιερός Ναός Προφήτη Ηλία Βαρυάδων|Country Church|baruades-gennisi-tis-theotokou
phaneromeni-vounoplagia|Vounoplagia|Βουνοπλαγιά|Panagia Phaneromeni Chapel in Vounoplagia|Παρεκκλήσιο Παναγίας Φανερωμένης Γεννήσεως της Θεοτόκου Βουνοπλαγιάς|Chapel|bounoplagia-ag-dimitrios
athanasius-vounoplagia|Vounoplagia|Βουνοπλαγιά|Saint Athanasius Chapel in Vounoplagia|Παρεκκλήσιο Αγίου Αθανασίου Βουνοπλαγιάς|Chapel|bounoplagia-ag-dimitrios
athanasius-gavrisioi|Gavrisioi|Γαβρισιοί|Saint Athanasius Chapel in Gavrisioi|Παρεκκλήσιο Αγίου Αθανασίου Γαβρισιών|Chapel|gavrisioi-ag-paraskeuh
marina-gavrisioi|Gavrisioi|Γαβρισιοί|Saint Marina Chapel in Gavrisioi|Παρεκκλήσιο Αγίας Μαρίνας Γαβρισιών|Chapel|gavrisioi-ag-paraskeuh
constantine-helen-katsikas|Katsikas|Κατσικάς|Saints Constantine and Helen Church in Katsikas|Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Κατσικάς|Church|katsikas-koimhsh-ths-theotokou
archangels-katsikas|Katsikas|Κατσικάς|Holy Archangels Church in Katsikas|Ιερός Ναός Παμμεγίστων Ταξιαρχών Κατσικάς|Church|katsikas-koimhsh-ths-theotokou
apostles-katsikas|Katsikas|Κατσικάς|Holy Apostles Church in Katsikas|Ιερός Ναός Αγίων Αποστόλων Κατσικάς|Church|katsikas-koimhsh-ths-theotokou
paraskevi-katsikas|Katsikas|Κατσικάς|Saint Paraskevi Guild Church in Katsikas|Συντεχνιακός Ναός Αγίας Παρασκευής Κατσικάς|Guild Church|katsikas-koimhsh-ths-theotokou
george-kato-pedina|Kato Pedina|Κάτω Πεδινά|Saint George Chapel at Saint Athanasius in Kato Pedina|Παρεκκλήσιο Αγίου Γεωργίου Κάτω Πεδινών|Chapel|katv-pedina-ag-athanasios
archangels-kato-pedina|Kato Pedina|Κάτω Πεδινά|Holy Archangels Church in Kato Pedina|Ιερός Ναός Ταξιαρχών Κάτω Πεδινών|Church|katv-pedina-ag-athanasios
nicholas-kato-pedina|Kato Pedina|Κάτω Πεδινά|Saint Nicholas Church in Kato Pedina|Ιερός Ναός Αγίου Νικολάου Κάτω Πεδινών|Church|katv-pedina-ag-athanasios
barbara-kato-pedina|Kato Pedina|Κάτω Πεδινά|Saint Barbara Church in Kato Pedina|Ιερός Ναός Αγίας Βαρβάρας Κάτω Πεδινών|Church|katv-pedina-ag-athanasios
nicholas-kopani|Kopani|Κοπάνη|Saint Nicholas Chapel in Kopani|Παρεκκλήσιο Αγίου Νικολάου Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
menas-kopani|Kopani|Κοπάνη|Saint Menas Chapel in Kopani|Παρεκκλήσιο Αγίου Μηνά Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
george-kopani|Kopani|Κοπάνη|Saint George Chapel in Kopani|Παρεκκλήσιο Αγίου Γεωργίου Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
paraskevi-kopani|Kopani|Κοπάνη|Saint Paraskevi Chapel in Kopani|Παρεκκλήσιο Αγίας Παρασκευής Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
nectarios-kopani|Kopani|Κοπάνη|Saint Nectarios Chapel in Kopani|Παρεκκλήσιο Αγίου Νεκταρίου Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
george-spartitsi-kopani|Kopani|Κοπάνη|Saint George Chapel at Spartitsi in Kopani|Παρεκκλήσιο Αγίου Γεωργίου Σπαρτίτσι Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
theodore-palaiochori-kopani|Kopani|Κοπάνη|Saint Theodore Chapel at Palaiochori Olytsika|Παρεκκλήσιο Αγίου Θεοδώρου Παλαιοχωρίου Ολύτσικα Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
athanasius-palaiochori-kopani|Kopani|Κοπάνη|Saint Athanasius Chapel at Palaiochori Olytsika|Παρεκκλήσιο Αγίου Αθανασίου Παλαιοχωρίου Ολύτσικα Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
demetrius-palaiochori-kopani|Kopani|Κοπάνη|Saint Demetrius Chapel at Palaiochori Olytsika|Παρεκκλήσιο Αγίου Δημητρίου Παλαιοχωρίου Ολύτσικα Κοπάνης|Chapel|kopani-koimisi-ths-theotokou
george-kosmira|Kosmira|Κοσμηρά|Saint George Chapel in Kosmira|Παρεκκλήσιο Αγίου Γεωργίου Κοσμηράς|Chapel|kosmira-ag-paraskeuh
dormition-kosmira|Kosmira|Κοσμηρά|Dormition of the Theotokos Chapel in Kosmira|Παρεκκλήσιο Κοιμήσεως της Θεοτόκου Κοσμηράς|Chapel|kosmira-ag-paraskeuh
demetrius-kosmira|Kosmira|Κοσμηρά|Saint Demetrius Chapel in Kosmira|Παρεκκλήσιο Αγίου Δημητρίου Κοσμηράς|Chapel|kosmira-ag-paraskeuh
savvas-kosmira|Kosmira|Κοσμηρά|Saint Savvas Chapel in Kosmira|Παρεκκλήσιο Αγίου Σάββα Κοσμηράς|Chapel|kosmira-ag-paraskeuh
nicholas-kosmira|Kosmira|Κοσμηρά|Saint Nicholas Chapel in Kosmira|Παρεκκλήσιο Αγίου Νικολάου Κοσμηράς|Chapel|kosmira-ag-paraskeuh
nicholas-kranoula|Kranoula|Κρανούλα|Saint Nicholas Chapel in Kranoula|Παρεκκλήσιο Αγίου Νικολάου Κρανούλας|Chapel|kranoula-ag-paraskeyh
apostles-kranoula|Kranoula|Κρανούλα|Holy Apostles Chapel in Kranoula|Παρεκκλήσιο Αγίων Αποστόλων Κρανούλας|Chapel|kranoula-ag-paraskeyh
paraskevi-kryfovo|Kryfovo|Κρυφοβό|Saint Paraskevi Church in Kryfovo|Ιερός Ναός Αγίας Παρασκευής Κρυφοβού|Church|kryfobo-gennisi-ths-theotokou
nicholas-kryfovo|Kryfovo|Κρυφοβό|Saint Nicholas Church in Kryfovo|Ιερός Ναός Αγίου Νικολάου Κρυφοβού|Church|kryfobo-gennisi-ths-theotokou
niketas-kryfovo|Kryfovo|Κρυφοβό|Saint Niketas Church in Kryfovo|Ιερός Ναός Αγίου Νικήτα Κρυφοβού|Church|kryfobo-gennisi-ths-theotokou
demetrius-kryfovo|Kryfovo|Κρυφοβό|Saint Demetrius Church in Kryfovo|Ιερός Ναός Αγίου Δημητρίου Κρυφοβού|Church|kryfobo-gennisi-ths-theotokou
athanasius-nicholas-maura-manassis|Manassis|Μανασσής|Saints Athanasius, Nicholas, and Maura Chapel in Manassis|Παρεκκλήσιο Αγίων Αθανασίου, Νικολάου και Μαύρας Μανασσή|Chapel|manassis-ag-georgios
christopher-manassis|Manassis|Μανασσής|Saint Christopher Chapel in Manassis|Παρεκκλήσιο Αγίου Χριστοφόρου Μανασσή|Chapel|manassis-ag-georgios
paraskevi-marmara|Marmara|Μάρμαρα|Saint Paraskevi Church at the Former Monastery in Marmara|Ιερός Ναός Αγίας Παρασκευής πρώην Μονής Μαρμάρων|Monastic Church|marmara-ag-nikolaou
nicholas-melia|Melia|Μελιά|Saint Nicholas Church in Melia|Ιερός Ναός Αγίου Νικολάου Μελιάς|Church|melia-eisodia-tis-theotokou
theodore-tyro-melia|Melia|Μελιά|Saint Theodore Tyro Country Church in Melia|Ιερός Ναός Αγίου Θεοδώρου του Τήρωνος Μελιάς|Country Church|melia-eisodia-tis-theotokou
paraskevi-melia|Melia|Μελιά|Saint Paraskevi Country Church in Melia|Ιερός Ναός Αγίας Παρασκευής Μελιάς|Country Church|melia-eisodia-tis-theotokou
nativity-theotokos-langiotissa|Langiotissa|Λαγγιώτισσα|Nativity of the Theotokos Church in Langiotissa|Ιερός Ναός Γεννήσεως της Θεοτόκου Λαγγιώτισσας|Church|melia-eisodia-tis-theotokou
marina-langiotissa|Langiotissa|Λαγγιώτισσα|Saint Marina Church in Langiotissa|Ιερός Ναός Αγίας Μαρίνας Λαγγιώτισσας|Church|melia-eisodia-tis-theotokou
athanasius-langiotissa|Langiotissa|Λαγγιώτισσα|Saint Athanasius Country Church in Langiotissa|Ιερός Ναός Αγίου Αθανασίου Λαγγιώτισσας|Country Church|melia-eisodia-tis-theotokou
life-giving-spring-bizani|Bizani|Μπιζάνι|Life-giving Spring Church in Bizani|Ιερός Ναός Ζωοδόχου Πηγής Μπιζανίου|Church|bizani-ag-georgios
paraskevi-bizani|Bizani|Μπιζάνι|Saint Paraskevi Church in Bizani|Ιερός Ναός Αγίας Παρασκευής Μπιζανίου|Church|bizani-ag-georgios
nicholas-bizani|Bizani|Μπιζάνι|Saint Nicholas Church in Bizani|Ιερός Ναός Αγίου Νικολάου Μπιζανίου|Church|bizani-ag-georgios
nicholas-koloniati|Koloniati|Κολωνιάτι|Saint Nicholas Church in Koloniati|Ιερός Ναός Αγίου Νικολάου Κολωνιατίου|Church|bizani-ag-georgios
prophet-elijah-koloniati|Koloniati|Κολωνιάτι|Prophet Elijah Chapel in Koloniati|Ιερός Ναός Προφήτη Ηλία Κολωνιατίου|Chapel|bizani-ag-georgios
archangels-neokaisareia|Neokaisareia|Νεοκαισάρεια|Holy Archangels Cemetery Church in Neokaisareia|Κοιμητηριακός Ναός Συνάξεως Παμμεγίστων Ταξιαρχών Νεοκαισάρειας|Cemetery Church|neokaisareia-ag-basileios
old-spyridon-trinity-neochoropoulo|Neochoropoulo|Νεοχωρόπουλο|Old Church of Saint Spyridon and the Holy Trinity in Neochoropoulo|Παλαιός Ιερός Ναός Αγίου Σπυρίδωνος και Αγίας Τριάδος Νεοχωροπούλου|Historic Church|neoxvropoulo-ag-spuridvn
kosmas-perivleptos|Ioannina|Ιωάννινα|Saint Kosmas the Aetolian Chapel of Perivleptos|Ιερό Παρεκκλήσιο Αγίου Κοσμά του Αιτωλού Ενορίας Περιβλέπτου|Chapel|perivleptos-koimisi-ths-theotokoy
tabitha-perivleptos|Ioannina|Ιωάννινα|Saint Tabitha Cemetery Chapel of Perivleptos|Ιερό Παρεκκλήσιο Αγίας Ταβιθάς Ενορίας Περιβλέπτου|Cemetery Chapel|perivleptos-koimisi-ths-theotokoy
spyridon-perivleptos|Ioannina|Ιωάννινα|Saint Spyridon Chapel of Perivleptos|Ιερό Παρεκκλήσιο Αγίου Σπυρίδωνος Ενορίας Περιβλέπτου|Chapel|perivleptos-koimisi-ths-theotokoy
sophia-daughters-child-protection|Ioannina|Ιωάννινα|Saint Sophia, Faith, Hope, and Love Institutional Chapel|Ιερό Παρεκκλήσιο Αγίας Σοφίας και των Αγίων Πίστεως, Ελπίδος και Αγάπης στο Κέντρο Προστασίας του Παιδιού|Institutional Chapel|perivleptos-koimisi-ths-theotokoy
panteleimon-gianniotiko-saloni|Ioannina|Ιωάννινα|Saint Panteleimon Chapel at Gianniotiko Saloni|Ιερό Παρεκκλήσιο Αγίου Παντελεήμονος στο Γιαννιώτικο Σαλόνι|Institutional Chapel|perivleptos-koimisi-ths-theotokoy
george-university-dourouti|Ioannina|Ιωάννινα|Saint George University Church at Dourouti|Πανεπιστημιακός Ναός Αγίου Γεωργίου Ιεράς Μονής Περιστεράς Δουρούτης|Institutional Church|perivleptos-koimisi-ths-theotokoy
nicholas-petsali|Petsali|Πετσάλι|Saint Nicholas Church in Petsali|Ιερός Ναός Αγίου Νικολάου Πετσαλίου|Church|petsali-gennisi-tis-theotokou
raphael-nicholas-irene-seismoplikta|Seismoplikta|Σεισμόπληκτα|Saints Raphael, Nicholas, and Irene Chapel at Apostle Paul|Παρεκκλήσιο Αγίων Ραφαήλ, Νικολάου και Ειρήνης στον Ιερό Ναό Αποστόλου Παύλου Σεισμοπλήκτων|Chapel|seismoplikta-apostolos-paulos
cyprian-justina-seismoplikta|Seismoplikta|Σεισμόπληκτα|Saints Cyprian and Justina Chapel at Apostle Paul|Παρεκκλήσιο Αγίων Κυπριανού και Ιουστίνης στον Ιερό Ναό Αποστόλου Παύλου Σεισμοπλήκτων|Chapel|seismoplikta-apostolos-paulos
nativity-theotokos-serviana|Serviana|Σερβιανά|Nativity of the Theotokos Church in Serviana|Ιερός Ναός Γεννήσεως της Θεοτόκου Σερβιανών|Church|serviana-pamm-taxiarxvn
nicholas-molyvadia|Molyvadia|Μολυβαδιά|Saint Nicholas Church in Molyvadia|Ιερός Ναός Αγίου Νικολάου Μολυβαδιάς|Church|serviana-pamm-taxiarxvn
dormition-serviana|Serviana|Σερβιανά|Dormition of the Theotokos Cemetery Church in Serviana|Κοιμητηριακός Ναός Κοιμήσεως της Θεοτόκου Σερβιανών|Cemetery Church|serviana-pamm-taxiarxvn
paraskevi-serviana|Serviana|Σερβιανά|Saint Paraskevi Chapel in Serviana|Ιερός Ναός Αγίας Παρασκευής Σερβιανών|Chapel|serviana-pamm-taxiarxvn
transfiguration-serviana|Serviana|Σερβιανά|Transfiguration of the Savior Chapel in Serviana|Ιερός Ναός Μεταμορφώσεως του Σωτήρος Σερβιανών|Chapel|serviana-pamm-taxiarxvn
george-sistrouni|Sistrouni|Σιστρούνι|Saint George Country Church in Sistrouni|Ιερός Ναός Αγίου Γεωργίου Σιστρουνίου|Country Church|sistrouni-ag-basileiou
john-sistrouni|Sistrouni|Σιστρούνι|Saint John Country Church in Sistrouni|Ιερός Ναός Αγίου Ιωάννου Σιστρουνίου|Country Church|sistrouni-ag-basileiou
nicholas-sistrouni|Sistrouni|Σιστρούνι|Saint Nicholas Country Church in Sistrouni|Ιερός Ναός Αγίου Νικολάου Σιστρουνίου|Country Church|sistrouni-ag-basileiou
barbara-sistrouni|Sistrouni|Σιστρούνι|Saint Barbara Country Church in Sistrouni|Ιερός Ναός Αγίας Βαρβάρας Σιστρουνίου|Country Church|sistrouni-ag-basileiou
paraskevi-sistrouni|Sistrouni|Σιστρούνι|Saint Paraskevi Country Church in Sistrouni|Ιερός Ναός Αγίας Παρασκευής Σιστρουνίου|Country Church|sistrouni-ag-basileiou
ascension-sistrouni|Sistrouni|Σιστρούνι|Ascension of the Lord Country Church in Sistrouni|Ιερός Ναός Αναλήψεως Σιστρουνίου|Country Church|sistrouni-ag-basileiou
athanasius-sistrouni|Sistrouni|Σιστρούνι|Saint Athanasius Country Church in Sistrouni|Ιερός Ναός Αγίου Αθανασίου Σιστρουνίου|Country Church|sistrouni-ag-basileiou
spyridon-sistrouni|Sistrouni|Σιστρούνι|Saint Spyridon Country Church in Sistrouni|Ιερός Ναός Αγίου Σπυρίδωνος Σιστρουνίου|Country Church|sistrouni-ag-basileiou
prophet-elijah-sistrouni|Sistrouni|Σιστρούνι|Prophet Elijah Country Church in Sistrouni|Ιερός Ναός Προφήτη Ηλία Σιστρουνίου|Country Church|sistrouni-ag-basileiou
"""


# Current Metropolis monastery index. Fields are key, English seat, Greek
# seat, English name, Greek source name, rank, and optional contact key.
MONASTIC_SOURCE = r"""
eleousa|Island of Ioannina|Νήσος Ιωαννίνων|Eleousa Monastery on the Island of Ioannina|Ιερά Μονή Ελεούσης Νήσου|Monastery|eleousa
vella|Vella|Βελλά|Vella Monastery|Ιερά Μονή Βελλάς|Monastery|vella
votsa|Votsa|Βοτσά|Votsa Monastery|Ιερά Μονή Βοτσάς|Monastery|votsa
romanou|Romanou|Ρωμανό|Romanou Monastery|Ιερά Μονή Ρωμανού|Monastery|
paliouri|Paliouri|Παλιουρή|Paliouri Monastery|Ιερά Μονή Παλιουρής|Monastery|paliouri
dourachani|Dourachani|Δουραχάνη|Dourachani Monastery|Ιερά Μονή Δουραχάνης|Monastery|dourachani
tsouka|Tsouka|Τσούκα|Tsouka Monastery|Ιερά Μονή Τσούκας|Monastery|tsouka
stoupaina|Stoupaina|Στούπαινα|Pantanassa Perivleptos Monastery of Stoupaina|Ιερά Μονή Περιβλέπτου Παντανάσσης Στούπαινας|Monastery|stoupaina
kastritsa|Kastritsa|Καστρίτσα|Kastritsa Monastery|Ιερά Μονή Καστρίτσης|Monastery|kastritsa
evangelistria|Ano Pedina|Άνω Πεδινά|Evangelistria Monastery in Ano Pedina|Ιερά Μονή Ευαγγελίστριας Άνω Πεδινών|Monastery|
panteleimon-island|Island of Ioannina|Νήσος Ιωαννίνων|Saint Panteleimon Dependency on the Island of Ioannina|Μετόχιο Αγίου Παντελεήμονος Νήσου|Monastic Dependency|
nicholas-philanthropenon|Island of Ioannina|Νήσος Ιωαννίνων|Saint Nicholas Philanthropenon Dependency|Μετόχιο Αγίου Νικολάου Φιλανθρωπηνών|Monastic Dependency|
nicholas-diliou|Island of Ioannina|Νήσος Ιωαννίνων|Saint Nicholas Diliou or Stratigopoulou Dependency|Μετόχιο Αγίου Νικολάου Ντίλιου ή Στρατηγοπούλου|Monastic Dependency|
john-forerunner-island|Island of Ioannina|Νήσος Ιωαννίνων|Saint John the Forerunner Dependency on the Island of Ioannina|Μετόχιο Αγίου Ιωάννου Προδρόμου Νήσου|Monastic Dependency|
transfiguration-island|Island of Ioannina|Νήσος Ιωαννίνων|Transfiguration of the Savior Dependency on the Island of Ioannina|Μετόχιο Μεταμορφώσεως του Σωτήρος Νήσου|Monastic Dependency|
prophet-elijah-island|Island of Ioannina|Νήσος Ιωαννίνων|Prophet Elijah Dependency on the Island of Ioannina|Μετόχιο Προφήτου Ηλιού Νήσου|Monastic Dependency|
john-rogovou|Tsepelovo|Τσεπέλοβο|Saint John Rogovou Dependency|Μετόχιο Αγίου Ιωάννου Ρογκοβού|Monastic Dependency|
nativity-theotokos-asprangeloi|Asprangeloi|Ασπράγγελοι|Nativity of the Theotokos Dependency in Asprangeloi|Μετόχιο Γεννήσεως της Θεοτόκου Ασπραγγέλων|Monastic Dependency|
dormition-pateron|Pateron|Πάτερο|Dormition of the Theotokos Dependency in Pateron|Μετόχιο Κοιμήσεως της Θεοτόκου Πατέρων|Monastic Dependency|
life-giving-spring-spilaiotissa|Aristi|Αρίστη|Life-giving Spring Spilaiotissa Dependency in Aristi|Μετόχιο Ζωοδόχου Πηγής Σπηλαιωτίσσης Αρίστης|Monastic Dependency|
nicholas-metsovo|Metsovo|Μέτσοβο|Saint Nicholas Dependency in Metsovo|Μετόχιο Αγίου Νικολάου Μετσόβου|Monastic Dependency|nicholas-metsovo
life-giving-spring-anthochori|Anthochori|Ανθοχώρι|Life-giving Spring Dependency in Anthochori|Μετόχιο Ζωοδόχου Πηγής Ανθοχωρίου|Monastic Dependency|
paraskevi-monodendri|Monodendri|Μονοδένδρι|Saint Paraskevi Dependency in Monodendri|Μετόχιο Αγίας Παρασκευής Μονοδενδρίου|Monastic Dependency|
prophet-elijah-vitsa|Vitsa|Βίτσα|Prophet Elijah Dependency in Vitsa|Μετόχιο Προφήτου Ηλιού Βίτσης|Monastic Dependency|
dormition-metsovo|Metsovo|Μέτσοβο|Dormition of the Theotokos Dependency in Metsovo|Μετόχιο Κοιμήσεως της Θεοτόκου Μετσόβου|Monastic Dependency|
demetrius-dichouni|Dichouni|Διχούνι|Saint Demetrius Dependency in Dichouni|Μετόχιο Αγίου Δημητρίου Διχουνίου|Monastic Dependency|
nativity-theotokos-sistrouni|Sistrouni|Σιστρούνι|Nativity of the Theotokos Dependency in Sistrouni|Μετόχιο Γεννήσεως της Θεοτόκου Σιστρουνίου|Monastic Dependency|
nativity-theotokos-katamachi|Katamachi|Καταμάχη|Nativity of the Theotokos Dependency in Katamachi|Μετόχιο Γενεθλίου της Θεοτόκου Καταμάχης|Monastic Dependency|
paraskevi-valanidia|Valanidia|Βαλανιδιά|Saint Paraskevi Dependency in Valanidia|Μετόχιο Αγίας Παρασκευής Βαλανιδιάς|Monastic Dependency|
apostles-messiana|Messiana|Μεσσιανά|Holy Apostles Dependency in Messiana|Μετόχιο Αγίων Αποστόλων Μεσσιανών|Monastic Dependency|
prophet-elijah-zitsa|Zitsa|Ζίτσα|Prophet Elijah Dependency in Zitsa|Μετόχιο Προφήτου Ηλιού Ζίτσης|Monastic Dependency|
entrance-theotokos-angelomachos|Kourenta|Κούρεντα|Entrance of the Theotokos Angelomachos Dependency in Kourenta|Μετόχιο Εισοδίων της Θεοτόκου Αγγελομάχου Κουρέντων|Monastic Dependency|
pardastani-ekklisiochori|Ekklisiochori|Εκκλησιοχώρι|Pardastani Dependency in Ekklisiochori|Μετόχιο Παρδάστανης Εκκλησιοχωρίου|Monastic Dependency|
nicholas-tzora|Mount Tzora|Όρος Τζόρα|Saint Nicholas of the Mountain Dependency at Tzora|Μετόχιο Αγίου Νικολάου Όρους Τζόρας|Monastic Dependency|nicholas-tzora
dormition-kipina|Kipina|Κηπίνα|Dormition of the Theotokos Dependency in Kipina|Μετόχιο Κοιμήσεως της Θεοτόκου Κηπίνας|Monastic Dependency|
dormition-krapsi|Krapsi|Κράψη|Dormition of the Theotokos Dependency in Krapsi|Μετόχιο Κοιμήσεως της Θεοτόκου Κράψης|Monastic Dependency|
dormition-iliokali|Iliokali|Ηλιόκαλη|Dormition of the Theotokos Dependency in Iliokali|Μετόχιο Κοιμήσεως της Θεοτόκου Ηλιόκαλης|Monastic Dependency|
"""


DEDICATIONS = {
    "Αγ. Δημήτριος": "Saint Demetrius",
    "Αγία Αναστασία": "Saint Anastasia",
    "Αγία Μαρίνα": "Saint Marina",
    "Αγία Παρασκευή": "Saint Paraskevi",
    "Αγ. Ανδρέας": "Saint Andrew",
    "Αγ. Αθανάσιος": "Saint Athanasius",
    "Άγιος Αθανάσιος": "Saint Athanasius",
    "Αγ. Ιωάννης ὁ Θεολόγος": "Saint John the Theologian",
    "Αγ. Ιωάννης": "Saint John",
    "Γέννηση της Θεοτόκου": "Nativity of the Theotokos",
    "Άγιος Νικόλαος": "Saint Nicholas",
    "Αγ. Νικόλαος": "Saint Nicholas",
    "Άγιοι Απόστολοι": "Holy Apostles",
    "Αγ. Απόστολοι": "Holy Apostles",
    "Αγ. Παρασκευή": "Saint Paraskevi",
    "Κοίμηση της Θεοτόκου": "Dormition of the Theotokos",
    "Της Του Θεού Σοφίας": "Wisdom of God",
    "Παμμ. Ταξιαρχών": "Holy Archangels",
    "Παμμ. Ταξιαρχῶν": "Holy Archangels",
    "Παμμ. ταξιαρχών": "Holy Archangels",
    "Αγ. Τριάδα": "Holy Trinity",
    "Αγία Τριάδα": "Holy Trinity",
    "Αγ. Τρύφων": "Saint Tryphon",
    "Μεταμόρφωση του Σωτήρος": "Transfiguration of the Savior",
    "Αγ. Χαράλαμπος": "Saint Charalambos",
    "Αγ. Γεώργιος": "Saint George",
    "Πρ. Ηλίας": "Prophet Elijah",
    "Προφ. Ηλίας": "Prophet Elijah",
    "Προφήτης Ηλίας": "Prophet Elijah",
    "Αγ. Ανάργυροι": "Holy Unmercenaries",
    "Άγιοι Ανάργυροι": "Holy Unmercenaries",
    "Αγ. Μηνάς": "Saint Menas",
    "Αγ. Παντελεήμων": "Saint Panteleimon",
    "Αγ. Θεόδωρος": "Saint Theodore",
    "Αγ. Κυριακή": "Saint Kyriaki",
    "Εισόδια της Θεοτόκου": "Entrance of the Theotokos",
    "Αγ. Σκέπη": "Protection of the Theotokos",
    "Αγ. Κοσμάς": "Saint Kosmas",
    "Γέννηση του Προδρόμου": "Nativity of Saint John the Forerunner",
    "Γενέθλιον του Προδρόμου": "Nativity of Saint John the Forerunner",
    "Γενέθλιο του Προδρόμου": "Nativity of Saint John the Forerunner",
    "Αγ. Συμεών": "Saint Symeon",
    "Aγ. Παρασκευή": "Saint Paraskevi",
    "Αγ. Κων/νος & Ελένη": "Saints Constantine and Helen",
    "Αγ. Κων/νος και Ελένη": "Saints Constantine and Helen",
    "Αγ. Κων/νος και Ελένης": "Saints Constantine and Helen",
    "Αγ. Βλάσιος": "Saint Blaise",
    "Αγ. Θεόδωροι": "Holy Theodore Martyrs",
    "Άγιοι Θεόδωροι": "Holy Theodore Martyrs",
    "Αγ. Βασίλειος": "Saint Basil",
    "Αγ. Βασιλείου": "Saint Basil",
    "Αγ. Σπυρίδων": "Saint Spyridon",
    "Απ. Πέτρος": "Apostle Peter",
    "Τρείς Ιεράρχες": "Three Holy Hierarchs",
    "Απόστολος Παύλος": "Apostle Paul",
}


SEAT_OVERRIDES = {
    "Αγ. Ιωάννης": ("Agios Ioannis", "Άγιος Ιωάννης"),
    "Άγιος Ιωάννης «Μπονίλα»": ("Anatoli", "Ανατολή"),
    "Αγία Μαρίνα": ("Ioannina", "Ιωάννινα"),
    "Άγιος Νικόλαος «Αγοράς»": ("Ioannina", "Ιωάννινα"),
    "Άγιος Νικόλαος «Κοπάνων»": ("Ioannina", "Ιωάννινα"),
    "Άγιος Σεραφείμ": ("Ioannina", "Ιωάννινα"),
    "Αρχιμανδρείο": ("Ioannina", "Ιωάννινα"),
    "Γηροκομείο": ("Ioannina", "Ιωάννινα"),
    "Καρδαμίτσια": ("Ioannina", "Ιωάννινα"),
    "Μητροπολιτικός Ναός": ("Ioannina", "Ιωάννινα"),
    "Σεισμόπληκτα": ("Ioannina", "Ιωάννινα"),
}


DETAIL_CONTACTS = {
    "Άγιος Νικόλαος «Κοπάνων» - Αγ. Νικόλαος": {
        "phones": ["+30 2651079195"],
        "site": "https://eiskopanous.blogspot.com/",
    },
    "Άνω Πεδινά - Αγ. Δημήτριος": {
        "phones": ["+30 6955837173"],
    },
    "Αρχιμανδρείο - Κοίμηση της Θεοτόκου": {
        "phones": ["+30 2651027647"],
        "address": ["Παντελεήμονος Μητροπολίτου Αργυροκάστρου", "45333 Ιωάννινα", "Ελλάδα"],
    },
    "Βαρυάδες - Γέννηση της Θεοτόκου": {
        "phones": ["+30 6945461044"],
    },
    "Βασιλική - Αγ. Τρύφων": {
        "phones": ["+30 6946712386"],
    },
    "Γαβρισιοί - Αγ. Παρασκευή": {
        "phones": ["+30 6909475886"],
    },
    "Καρδαμίτσια - Προφήτης Ηλίας": {
        "phones": ["+30 2651073331", "+30 2651027647"],
    },
    "Καστρίτσα - Αγ. Γεώργιος": {
        "phones": ["+30 2651055714"],
    },
    "Κατσικάς - Κοίμηση της Θεοτόκου": {
        "phones": ["+30 2651094187"],
    },
    "Κάτω Πεδινά - Αγ. Αθανάσιος": {
        "phones": ["+30 6955837173"],
    },
    "Κρύα Λυκοτρίχι - Αγ. Ιωάννης": {
        "phones": ["+30 2651022671", "+30 6947694489"],
    },
    "Μανασσής - Αγ. Γεώργιος": {
        "phones": ["+30 6986755303"],
    },
    "Μπάφρα - Αγ. Παρασκευή": {
        "emails": ["enoriampafras@yahoo.com"],
    },
    "Νεγάδες - Αγ. Γεώργιος": {
        "phones": ["+30 6948308313"],
    },
    "Προσκυνηματικός Ναός Νεομάρτυρος Αγ. Γεωργίου": {
        "emails": ["evtsogas@yahoo.gr"],
        "address": ["Πλατεία Πάργης", "45221 Ιωάννινα", "Ελλάδα"],
    },
    "Σεισμόπληκτα - Απόστολος Παύλος": {
        "phones": ["+30 2651045182"],
        "emails": ["inagpavlouseism@gmail.com"],
        "address": ["Πλατεία Αγίου Παύλου", "45500 Σεισμόπληκτα Ιωάννινα", "Ελλάδα"],
    },
}


DETAIL_ADDRESSES = {
    "Αγ. Ιωάννης - Αγ. Ιωάννης ὁ Θεολόγος": ["Άγιος Ιωάννης Μπισδουνάκι", "45500 Ιωάννινα", "Ελλάδα"],
    "Άγιος Ιωάννης «Μπονίλα» - Αγ. Ιωάννης": ["Λεωφόρος Ιωαννίνων 2", "45333 Ανατολή Ιωαννίνων", "Ελλάδα"],
    "Αγία Μαρίνα - Αγία Μαρίνα": ["Αγίας Μαρίνης 34", "45221 Ιωάννινα", "Ελλάδα"],
    "Άγιος Νικόλαος «Αγοράς» - Αγ. Νικόλαος": ["Χατζηκώστα 21", "45444 Ιωάννινα", "Ελλάδα"],
    "Άγιος Σεραφείμ - Άγιοι Απόστολοι": ["Δημολίτσα Πατατούκου 13", "45333 Ιωάννινα", "Ελλάδα"],
    "Ανατολή - Της Του Θεού Σοφίας": ["Προφήτη Ηλία 13 και Παναγίας Σουμελά 17", "45333 Ανατολή Ιωαννίνων", "Ελλάδα"],
    "Μητροπολιτικός Ναός - Άγιος Αθανάσιος": ["Μητροπόλεως 1", "45221 Ιωάννινα", "Ελλάδα"],
}


BODY_SITES = {
    "Αγία Μαρίνα - Αγία Μαρίνα": "https://agiamarina-ioa.blogspot.com/",
}


MONASTIC_CONTACTS = {
    "eleousa": {
        "phones": ["+30 2651081974", "+30 6907910348", "+30 6980379154", "+30 2651081819"],
        "detail": LOCAL_BASE + "/eleousis-nhsou/",
    },
    "vella": {"phones": ["+30 2653041286"]},
    "votsa": {
        "phones": ["+30 6947664890"],
        "emails": ["info@im-votsas.gr"],
        "site": "https://im-votsas.gr/",
    },
    "paliouri": {
        "phones": ["+30 2658061464"],
        "emails": ["impaliouris@gmail.com"],
        "detail": LOCAL_BASE + "/iera-monh-palioyris/",
    },
    "dourachani": {"phones": ["+30 2651052247"]},
    "tsouka": {"phones": ["+30 2651089223"]},
    "stoupaina": {
        "phones": ["+30 6980388344", "+30 2658770194"],
        "detail": LOCAL_BASE + "/i-monh-stoupainas/",
    },
    "kastritsa": {
        "phones": ["+30 6955583070", "+30 2651052258"],
        "emails": ["imkastritsis@gmail.com"],
        "detail": LOCAL_BASE + "/iera-moni-kastritsas/",
    },
    "nicholas-metsovo": {
        "phones": ["+30 6947664890"],
        "emails": ["info@im-votsas.gr"],
        "site": "https://im-votsas.gr/",
    },
    "nicholas-tzora": {"phones": ["+30 6970468028"]},
}


EP_MONASTIC_OMISSIONS = {
    "pardastani-ekklisiochori",
    "dormition-krapsi",
}


FORBIDDEN_PUNCTUATION = re.compile(
    r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]"
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_HOSTS = {
    "imioanninon.gr", "www.imioanninon.gr", "ec-patr.org",
    "ecclesiagreece.gr", "www.ecclesiagreece.gr", "im-votsas.gr",
    "www.im-votsas.gr", "agiamarina-ioa.blogspot.com",
    "eiskopanous.blogspot.com",
}


def article(slug):
    return LOCAL_BASE + "/" + slug.strip("/") + "/"


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


def transliterate(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    pairs = (
        ("αι", "ai"), ("ει", "ei"), ("οι", "oi"), ("ου", "ou"),
        ("Αι", "Ai"), ("Ει", "Ei"), ("Οι", "Oi"), ("Ου", "Ou"),
        ("γκ", "gk"), ("Γκ", "Gk"), ("μπ", "b"), ("Μπ", "B"),
        ("ντ", "nt"), ("Ντ", "Nt"), ("τσ", "ts"), ("Τσ", "Ts"),
        ("τζ", "tz"), ("Τζ", "Tz"),
    )
    for source, target in pairs:
        value = value.replace(source, target)
    mapping = {
        "Α": "A", "Β": "V", "Γ": "G", "Δ": "D", "Ε": "E",
        "Ζ": "Z", "Η": "I", "Θ": "Th", "Ι": "I", "Κ": "K",
        "Λ": "L", "Μ": "M", "Ν": "N", "Ξ": "X", "Ο": "O",
        "Π": "P", "Ρ": "R", "Σ": "S", "Τ": "T", "Υ": "Y",
        "Φ": "F", "Χ": "Ch", "Ψ": "Ps", "Ω": "O",
        "α": "a", "β": "v", "γ": "g", "δ": "d", "ε": "e",
        "ζ": "z", "η": "i", "θ": "th", "ι": "i", "κ": "k",
        "λ": "l", "μ": "m", "ν": "n", "ξ": "x", "ο": "o",
        "π": "p", "ρ": "r", "σ": "s", "ς": "s", "τ": "t",
        "υ": "y", "φ": "f", "χ": "ch", "ψ": "ps", "ω": "o",
    }
    return "".join(mapping.get(char, char) for char in value)


def slugify(value):
    value = transliterate(value).lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "body"


def normalize_phone(value):
    digits = re.sub(r"\D", "", value or "")
    if not digits:
        return []
    if len(digits) == 20:
        chunks = [digits[:10], digits[10:]]
    elif len(digits) == 10:
        chunks = [digits]
    else:
        raise ValueError("unexpected Ioannina phone cell: %s" % value)
    return ["+30 " + chunk for chunk in chunks]


def unique(values):
    result = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def parse_directory_source():
    rows = []
    for raw in (line for line in DIRECTORY_SOURCE.splitlines()
                if line.strip()):
        parts = raw.split("|")
        if len(parts) != 5:
            raise ValueError("invalid Ioannina directory row: %s" % raw)
        title, phone, email, region, detail = parts
        rows.append({
            "title": title,
            "phone_cell": phone,
            "email_cell": email,
            "region": region,
            "detail": detail,
        })
    if len(rows) != 256:
        raise ValueError("expected 256 current directory rows")
    return rows


def parse_extra_source():
    rows = []
    for raw in (line for line in EXTRA_SOURCE.splitlines() if line.strip()):
        parts = raw.split("|")
        if len(parts) != 7:
            raise ValueError("invalid Ioannina detail row: %s" % raw)
        key, seat, local_seat, name, local, rank, slug = parts
        rows.append({
            "key": key, "seat": seat, "local_seat": local_seat,
            "name": name, "local": local, "rank": rank,
            "source": article(slug),
        })
    if len(rows) != 100:
        raise ValueError("expected 100 current detail bodies")
    return rows


def parse_monastic_source():
    rows = []
    for raw in (line for line in MONASTIC_SOURCE.splitlines()
                if line.strip()):
        parts = raw.split("|")
        if len(parts) != 7:
            raise ValueError("invalid Ioannina monastic row: %s" % raw)
        key, seat, local_seat, name, local, rank, contact_key = parts
        rows.append({
            "key": key, "seat": seat, "local_seat": local_seat,
            "name": name, "local": local, "rank": rank,
            "contact_key": contact_key,
        })
    if len(rows) != 37:
        raise ValueError("expected 37 current monastic bodies")
    return rows


def directory_rank(title):
    if title == "Μητροπολιτικός Ναός - Άγιος Αθανάσιος":
        return "Metropolitan Cathedral"
    if title == "Προσκυνηματικός Ναός Νεομάρτυρος Αγ. Γεωργίου":
        return "Pilgrimage Church"
    if title == "Οίκος Νεομάρτυρος Αγίου Γεωργίου":
        return "Memorial House"
    if title.startswith("Γηροκομείο -"):
        return "Institutional Church"
    if title.startswith(("Άγιος Ιωάννης «Μπονίλα» -",
                         "Άγιος Σεραφείμ -", "Καρδαμίτσια -")):
        return "Chapel"
    return "Parish Church"


def directory_identity(source):
    title = source["title"]
    rank = directory_rank(title)
    if title == "Οίκος Νεομάρτυρος Αγίου Γεωργίου":
        return (
            "House of New Martyr Saint George", title,
            "Ioannina", "Ιωάννινα", rank,
        )
    if title == "Προσκυνηματικός Ναός Νεομάρτυρος Αγ. Γεωργίου":
        return (
            "New Martyr Saint George Pilgrimage Church in Ioannina",
            title, "Ioannina", "Ιωάννινα", rank,
        )
    if " - " not in title:
        raise ValueError("unparsed Ioannina directory title: %s" % title)
    local_seat, local_dedication = title.split(" - ", 1)
    if local_dedication not in DEDICATIONS:
        raise ValueError("unknown Ioannina dedication: %s" % local_dedication)
    dedication = DEDICATIONS[local_dedication]
    seat, display_local_seat = SEAT_OVERRIDES.get(
        local_seat, (transliterate(local_seat), local_seat)
    )
    if rank == "Metropolitan Cathedral":
        name = dedication + " Metropolitan Cathedral in Ioannina"
    elif rank == "Institutional Church":
        name = dedication + " Institutional Church at the Ioannina Elderly Home"
    elif rank == "Chapel":
        name = dedication + " Chapel in " + seat
    else:
        name = dedication + " Parish Church in " + seat
    return name, title, seat, display_local_seat, rank


def add_directory_rows(rows):
    for source in parse_directory_source():
        number = len(rows) + 1
        name, local, seat, local_seat, rank = directory_identity(source)
        title = source["title"]
        detail = source["detail"]
        if title in {
                "Πεδινή - Κοίμηση της Θεοτόκου",
                "Πεντέλη Δροσιά - Αγ. Κων/νος και Ελένη"}:
            detail = ""
        sources = [LOCAL_DIRECTORY_URL]
        if detail:
            sources.append(detail)
        phones = normalize_phone(source["phone_cell"])
        emails = [] if source["email_cell"] == "-" else [source["email_cell"]]
        extra = DETAIL_CONTACTS.get(title, {})
        phones = unique(phones + list(extra.get("phones") or []))
        emails = unique(emails + list(extra.get("emails") or []))
        site = BODY_SITES.get(title) or extra.get("site")
        if site:
            sources.append(site)
        address = (
            extra.get("address") or DETAIL_ADDRESSES.get(title) or
            [local_seat, "Ιωάννινα, Ελλάδα"]
        )
        item = {
            "id": "gr-ep-ioannina-%03d-%s" % (
                number, slugify(seat + " " + name)
            ),
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": list(address),
            "region": source["region"],
            "sources": unique(sources),
        }
        if phones:
            item["phones"] = phones
        if emails:
            item["emails"] = emails
        if site:
            item["site"] = site
        if phones or emails or site:
            item["contact_sources"] = [LOCAL_DIRECTORY_URL]
            if extra and detail:
                item["contact_sources"].append(detail)
            if site:
                item["contact_sources"].append(site)
            item["contact_sources"] = unique(item["contact_sources"])
            item["contact_checked"] = CHECKED
        rows.append(item)


def add_extra_rows(rows):
    for source in parse_extra_source():
        number = len(rows) + 1
        rows.append({
            "id": "gr-ep-ioannina-%03d-%s" % (number, source["key"]),
            "parent": PARENT,
            "kind": "parish",
            "rank": source["rank"],
            "name": source["name"],
            "local": source["local"],
            "seat": source["seat"],
            "country": "GR",
            "address": [source["local_seat"], "Ιωάννινα, Ελλάδα"],
            "sources": [source["source"]],
        })


def add_monastic_rows(rows):
    for source in parse_monastic_source():
        number = len(rows) + 1
        sources = [LOCAL_MONASTERIES_URL]
        contact = MONASTIC_CONTACTS.get(source["contact_key"], {})
        if contact.get("detail"):
            sources.append(contact["detail"])
        if source["key"] not in EP_MONASTIC_OMISSIONS:
            sources.append(EP_URL)
        if contact.get("site"):
            sources.append(contact["site"])
        item = {
            "id": "gr-ep-ioannina-%03d-%s" % (number, source["key"]),
            "parent": PARENT,
            "kind": "monastery",
            "rank": source["rank"],
            "name": source["name"],
            "local": source["local"],
            "seat": source["seat"],
            "country": "GR",
            "address": [source["local_seat"], "Ιωάννινα, Ελλάδα"],
            "sources": unique(sources),
        }
        for key in ("phones", "emails"):
            if contact.get(key):
                item[key] = list(contact[key])
        if contact.get("site"):
            item["site"] = contact["site"]
        if any(contact.get(key) for key in ("phones", "emails", "site")):
            item["contact_sources"] = unique(sources)
            item["contact_checked"] = CHECKED
        rows.append(item)


def create_rows():
    rows = []
    add_directory_rows(rows)
    add_extra_rows(rows)
    add_monastic_rows(rows)
    rows.append({
        "id": "gr-ep-ioannina-394-paisios-kiapha-ioannina",
        "parent": PARENT,
        "kind": "parish",
        "rank": "Metropolitan Chapel",
        "name": "Saint Paisios the Hagiorite Metropolitan Chapel in Kiapha, Ioannina",
        "local": "Ιερός Ναός Αγίου Παϊσίου του Αγιορείτου Κιάφας πόλεως Ιωαννίνων",
        "seat": "Ioannina",
        "country": "GR",
        "address": ["Κιάφα", "Ιωάννινα, Ελλάδα"],
        "sources": [EP_URL, PAISIOS_CURRENT_URL],
    })
    return rows


ROWS = create_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 394
EXPECTED_OWNER_COUNTS = {PARENT: 394}
EXPECTED_KINDS = {"monastery": 37, "parish": 357}
EXPECTED_RANKS = {
    "Cemetery Chapel": 1,
    "Cemetery Church": 2,
    "Chapel": 51,
    "Church": 21,
    "Country Church": 20,
    "Guild Church": 1,
    "Historic Church": 2,
    "Institutional Chapel": 2,
    "Institutional Church": 2,
    "Memorial House": 1,
    "Metropolitan Cathedral": 1,
    "Metropolitan Chapel": 1,
    "Monastic Church": 2,
    "Monastic Dependency": 27,
    "Monastery": 10,
    "Parish Church": 249,
    "Pilgrimage Church": 1,
}
EXPECTED_CONTACT_BODIES = 265
EXPECTED_PHONE_BODIES = 265
EXPECTED_PHONE_VALUES = 287
EXPECTED_EMAIL_BODIES = 179
EXPECTED_EMAIL_VALUES = 182
EXPECTED_SITE_BODIES = 4
EXPECTED_ADDRESS_BODIES = 394
EXISTING_PARENTS = {PARENT}


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in ALLOWED_HOSTS:
        raise ValueError("%s carries a non-competent source: %s" % (label, value))


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
                raise ValueError("%s contact source lacks identity provenance" % item.get("id"))
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
        raise ValueError("Ioannina candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Ioannina candidate ledger date drifted")
    expected_summary = {
        PARENT: 394,
        "total": 394,
        "current_directory_rows": 256,
        "detail_page_bodies": 100,
        "current_monasteries": 10,
        "current_monastic_dependencies": 27,
        "current_reported_bodies": 1,
        "parish_kind_rows": 357,
        "monastery_kind_rows": 37,
        "contact_bodies": 265,
        "phone_bodies": 265,
        "public_phone_values": 287,
        "email_bodies": 179,
        "public_email_values": 182,
        "body_owned_sites": 4,
        "address_bodies": 394,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Ioannina ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Ioannina ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Ioannina ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Ioannina ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Ioannina ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Ioannina candidate ledger has forbidden punctuation")
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
        signature = (parent, unicase(item["local"]), unicase(item["seat"]))
        if signature in signatures:
            raise ValueError("%s duplicates %s after Greek normalization" % (
                row_id, signatures[signature]
            ))
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Ioannina English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Ioannina English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Ioannina parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Ioannina kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Ioannina rank totals drifted: %r" % dict(sorted(rank_counts.items())))
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
        EXPECTED_CONTACT_BODIES, EXPECTED_PHONE_BODIES,
        EXPECTED_PHONE_VALUES, EXPECTED_EMAIL_BODIES,
        EXPECTED_EMAIL_VALUES, EXPECTED_SITE_BODIES,
        EXPECTED_ADDRESS_BODIES,
    )
    if coverage != expected_coverage:
        raise ValueError("Ioannina contact coverage drifted: %r" % (coverage,))
    validate_ledger()
    return {
        PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}
    }


class DirectoryTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = {"text": [], "links": []}
        elif tag == "a" and self.cell is not None:
            self.cell["links"].append(values.get("href", ""))

    def handle_data(self, data):
        if self.cell is not None:
            self.cell["text"].append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.cell["text"] = " ".join(
                "".join(self.cell["text"]).split()
            )
            self.row.append(self.cell)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ")
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", value).strip().casefold()


def all_source_urls():
    values = {
        LOCAL_DIRECTORY_URL, LOCAL_MONASTERIES_URL, LOCAL_REGIONS_URL,
        EP_URL, COG_URL, LEGAL_URL, LOCAL_LEGAL_URL, PAISIOS_CURRENT_URL,
    }
    for row in ROWS:
        values.update(row.get("sources") or [])
        values.update(row.get("contact_sources") or [])
        if row.get("site"):
            values.add(row["site"])
    ledger = validate_ledger()
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        for entry in ledger[key]:
            values.update(entry.get("sources") or [])
    return sorted(values)


def fetch_live_source(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Connection": "close",
    })
    with urlopen(request, timeout=45) as response:
        if response.status >= 400:
            raise ValueError("HTTP %s" % response.status)
        content_type = response.headers.get("Content-Type", "").lower()
        payload = response.read()
        if "pdf" in content_type or url.endswith(".pdf"):
            if not payload.startswith(b"%PDF") or len(payload) < 20000:
                raise ValueError("invalid PDF payload")
            return None
        if "html" not in content_type:
            raise ValueError("unexpected content type %s" % content_type)
        return payload.decode("utf-8", "replace")


def parse_live_directory(payload):
    parser = DirectoryTableParser()
    parser.feed(payload)
    parsed = []
    for cells in parser.rows:
        if len(cells) != 5:
            continue
        title = cells[0]["text"].replace("\u2013", "-")
        if title == "Ενορία - Ναός":
            continue
        parsed.append({
            "title": title,
            "phone_cell": cells[2]["text"].replace("\u2013", "-"),
            "email_cell": cells[3]["text"].replace("\u2013", "-"),
            "region": cells[4]["text"].replace("\u2013", "-"),
            "detail": cells[0]["links"][0] if cells[0]["links"] else "",
        })
    return parsed


def check_live_sources():
    failures = []
    source_payloads = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(fetch_live_source, url): url
            for url in all_source_urls()
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                source_payloads[url] = future.result()
            except Exception as exc:
                failures.append((url, str(exc)))
    if failures:
        rendered = "; ".join("%s [%s]" % pair for pair in sorted(failures))
        raise ValueError("live Ioannina source check failed: %s" % rendered)

    live_directory = parse_live_directory(source_payloads[LOCAL_DIRECTORY_URL])
    expected_directory = parse_directory_source()
    if live_directory != expected_directory:
        raise ValueError(
            "live Ioannina directory drifted: expected %d rows, found %d"
            % (len(expected_directory), len(live_directory))
        )

    monastery_text = normalize_source_text(source_payloads[LOCAL_MONASTERIES_URL])
    for marker in (
            "Ελεούσης Νήσου", "Βελλᾶς", "Βοτσᾶς", "Ρωμανοῦ",
            "Παλιουρῆς", "Δουραχάνης", "Τσούκας",
            "Περιβλέπτου Παντανάσσης", "Καστρίτσης", "Εὐαγγελίστριας",
            "Ἁγίου Παντελεήμονος", "Ἁγίου Νικολάου Φιλανθρωπηνῶν",
            "Παρδάστανης Ἐκκλησιοχωρίου", "Κοιμήσεως τῆς Θεοτόκου Κράψης"):
        if normalize_source_text(marker) not in monastery_text:
            raise ValueError("live Ioannina monastery marker failed: %s" % marker)

    ep_text = normalize_source_text(source_payloads[EP_URL])
    for marker in ("249", "Ἱεραὶ Μοναί", "Ἁγίου Παϊσίου"):
        if normalize_source_text(marker) not in ep_text:
            raise ValueError("live Ioannina Patriarchate marker failed: %s" % marker)

    paisios_text = normalize_source_text(source_payloads[PAISIOS_CURRENT_URL])
    for marker in ("Οσίου Παϊσίου", "Κιάφας", "Ιωαννίνων"):
        if normalize_source_text(marker) not in paisios_text:
            raise ValueError("live Ioannina Saint Paisios marker failed: %s" % marker)

    contact_failures = []
    normalized = {
        url: normalize_source_text(payload or "")
        for url, payload in source_payloads.items()
    }
    for row in ROWS:
        contact_sources = row.get("contact_sources") or []
        for phone in row.get("phones") or []:
            digits = re.sub(r"\D", "", phone)
            source_digits = [
                re.sub(r"\D", "", normalized.get(url, ""))
                for url in contact_sources
            ]
            if not any(digits[-10:] in value for value in source_digits):
                contact_failures.append((row["id"], phone))
        for email in row.get("emails") or []:
            if not any(
                    email.casefold() in normalized.get(url, "") or
                    email.casefold() in (source_payloads.get(url) or "").casefold()
                       for url in contact_sources):
                contact_failures.append((row["id"], email))
    if contact_failures:
        raise ValueError("live Ioannina contact marker failed: %r" % contact_failures)


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        check_live_sources()
        print("Ioannina live source check passed: 394 exact bodies")
    elif args.dump:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print("Ioannina check passed: 394 exact bodies")


if __name__ == "__main__":
    main()
