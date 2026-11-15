#!/usr/bin/env python3
"""Build the exact current Ilion, Petroupolis and Acharnai body roster."""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PARENT = "gr-ilion"
CHECKED = "2026-11-15"
HERE = Path(__file__).resolve().parent
CANDIDATE_LEDGER = HERE / "directory_candidates" / "ilion_country.json"

BASE = "https://imiliou.gr"
PARISH_URL = BASE + "/category/typos-naoy/enoriakoi-ieroi-naoi"
PILGRIMAGE_URL = BASE + "/category/typos-naoy/proskynimatikoi-ieroi-naoi"
METROPOLITAN_CHAPEL_URL = BASE + "/category/typos-naoy/mitropolitika-parekklisia"
PARISH_CHAPEL_URL = BASE + "/category/typos-naoy/enoriaka-parekklisia"
INSTITUTION_CHAPEL_URL = BASE + "/category/typos-naoy/parekklisia-idrymaton"
CEMETERY_CHAPEL_URL = BASE + "/category/typos-naoy/parekklisia-koimitirion"
MONASTERY_URL = BASE + "/ieres-mones"
STRUCTURE_URL = BASE + "/content/domi"
LEGAL_URL = "https://ecclesiagreece.gr/greek/press/ekklisia/2019_ioulios.pdf"
PROFILE_URL = "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/iliou-petroupoleos-kai-acharnon"

RAW = json.loads(r"""
[
  {
    "rank": "Parish Church",
    "title": "Ευαγγελισμός της Θεοτόκου Ιλίου (Μητροπολιτικός)",
    "detail": "https://imiliou.gr/naos/ilion/content/eyaggelismos-tis-theotokoy-ilioy-mitropolitikos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "phones": [
      "+30 210-261-3009",
      "+30 210-263-9260"
    ],
    "address": [
      "Πριάμου 123",
      "131 22 Ίλιον"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Παναγίας Γοργοεπηκόου Ζεφυρίου (Γρηγορούσα)",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/panagias-gorgoepikooy-zefyrioy-grigoroysa",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "grigorousa@imiliou.gr"
    ],
    "address": [
      "Μιαούλη 1",
      "134 51 Ζεφύρι"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Προφήτη Ηλία Αχαρνών",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/profiti-ilia-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "pr.ilias-ah@imiliou.gr"
    ],
    "address": [
      "Βωμού Αρτέμιδος 92",
      "136 75 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Παρασκευής Αχαρνών",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agias-paraskeyis-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.paraskevi-ah@imiliou.gr"
    ],
    "address": [
      "Αγίας Παρασκευής 4-8",
      "136 74 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Τριάδας Θρακομακεδόνων",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agias-triadas-thrakomakedonon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.triada-th@imiliou.gr"
    ],
    "address": [
      "Μεγάλου Αλεξάνδρου 181",
      "136 76 Θρακομακεδόνες"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Παντελεήμονος Κρυονερίου",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agioy-panteleimona-kryonerioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.panteleimon@imiliou.gr"
    ],
    "address": [
      "Παραδείσου 3",
      "145 68 Κρυονέρι"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Κωνσταντίνου και Ελένης Άνω Αχαρνών (Μεγάλα Σχίνα)",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agion-konstantinoy-kai-elenis-ano-axarnon-megala-sxina",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.konstantinos-aa@imiliou.gr"
    ],
    "address": [
      "Μόλας 134",
      "136 72 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Κυρίλλου και Μεθοδίου Ολυμπιακού Χωρίου",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agion-kyrilloy-kai-methodioy-olympiakoy-xorioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.kyrillosmethodios@imiliou.gr"
    ],
    "address": [
      "Κωνσταντίνου Κεντέρη",
      "136 72 Ολυμπιακό χωριό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Άννης Αχαρνών",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agias-annis-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.anna@imiliou.gr"
    ],
    "address": [
      "Νίκου Σταυρίδη 4",
      "13675 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Κοιμήσεως Θεοτόκου Αχαρνών",
    "detail": "https://imiliou.gr/naos/axarnon/content/koimiseos-theotokoy-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "koimisis.theotokou-ah@imiliou.gr"
    ],
    "address": [
      "Μαραθώνος 1",
      "136 71 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Τριάδας Καματερού",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agias-triadas-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.triada-ka@imiliou.gr"
    ],
    "address": [
      "Πλατεία Αγίας Τριάδος 3",
      "134 51 Καματερό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Νικολάου Ιλίου",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agioy-nikolaoy-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.nikolaos@imiliou.gr"
    ],
    "address": [
      "Πλατεία Αγίου Νικολάου",
      "134 51 Καματερό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Κοιμήσεως Θεοτόκου Φυλής (Χασιά)",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/koimiseos-theotokoy-fylis-xasia",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "koimisis.theotokou-fy@imiliou.gr"
    ],
    "address": [
      "133 45 Φυλή"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Τριάδας Πετρουπόλεως",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agias-triadas-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.triada-pe@imiliou.gr"
    ],
    "address": [
      "Σουλίου 167",
      "132 31 Πετρούπολη"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Κοιμήσεως Θεοτόκου Πετρουπόλεως",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/koimiseos-theotokoy-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "koimisis.theotokou-pe@imiliou.gr"
    ],
    "address": [
      "Πίνδου 60",
      "132 31 Πετρούπολη"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Γεωργίου Ζωφριάς",
    "detail": "https://imiliou.gr/naos/ano-liosia/content/agioy-georgioy-ano-liosion-zofrias",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.georgios-al@imiliou.gr"
    ],
    "address": [
      "Ισοκράτους 17",
      "133 44 Άνω Λιόσια"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Αποστόλων (Ρέθι) Αχαρνών",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agion-apostolon-rethi-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.antonios@imiliou.gr"
    ],
    "address": [
      "Αγίου Ιωάννου Ρώσου 1",
      "136 74 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Γεωργίου Αχαρνών",
    "detail": "https://imiliou.gr/naos/axarnon/content/agioy-georgioy-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.georgios-ah@imiliou.gr"
    ],
    "address": [
      "Κατσανδρή 8 (πλατεία Αγίου Γεωργίου)",
      "136 73 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Τρύφωνα Καματερού",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agioy-tryfona-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.tryfon@imiliou.gr"
    ],
    "address": [
      "Ζαγορίου 74",
      "13451 Καματερό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Παμμεγίστων Ταξιαρχών Αχαρνών",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/pammegiston-taksiarxon-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "taxiarches@imiliou.gr"
    ],
    "address": [
      "Λεωφ. Ιωνίας και Αγίων Ταξιαρχών",
      "13671 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Στυλιανού Ζεφυρίου",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agioy-stylianoy-zefyrioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.stylianos@imiliou.gr"
    ],
    "address": [
      "Δράκου Κόγκα και Μπουμπουλίνας",
      "13451 Ζεφύρι"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Σπυρίδωνος Καματερού",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/agioy-spyridonos-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.spyridon@imiliou.gr"
    ],
    "address": [
      "Καποδιστρίου 1",
      "134 51 Καματερό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Προφήτη Ηλία Πετρουπόλεως",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/profiti-ilia-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "pr.ilias-pe@imiliou.gr"
    ],
    "address": [
      "Υψηλάντου 39 - 41",
      "132 31 Πετρούπολη"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Μυροφόρων και Νικόδημου Αγίων Αναργύρων",
    "detail": "https://imiliou.gr/index.php/naos/agioi-anargyroi-anakasa/content/agion-myroforon-kai-nikodimoy-agion-anargyron",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.myrofores@imiliou.gr"
    ],
    "address": [
      "Λεωφ. Κωνσταντινουπόλεως 518",
      "135 62 Άγιοι Ανάργυροι"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Μεταμορφώσεως του Σωτήρος Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/ano-liosia/content/metamorfoseos-toy-sotiros-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "metamorfosis@imiliou.gr"
    ],
    "address": [
      "Μεταμόρφωσης Σωτήρος 1",
      "133 44 Άνω Λιόσια"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Κωνσταντίνου και Ελένης Κάτω Αχαρνών (Λυκότρυπα)",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/agion-konstantinoy-kai-elenis-kato-axarnon-lykotrypa",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.konstantinos-ka@imiliou.gr"
    ],
    "address": [
      "Αγίων Κωνσταντίνου και Ελένης 42",
      "136 71 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Κοιμήσεως Θεοτόκου (Παλατιανής) Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/ilioy/content/koimiseos-theotokoy-palatianis-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "address": [
      "Παύλου Μελά 10",
      "131 21 ​Ίλιον"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Κοιμήσεως Θεοτόκου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/koimiseos-theotokoy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "koimisis.theotokou-af@imiliou.gr"
    ],
    "address": [
      "Αγ. Τριάδας 6",
      "190 14 Αφίδνες"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Ιωάννου του Θεολόγου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/ano-liosia/content/agioy-ioannoy-toy-theologoy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.ioannis@imiliou.gr"
    ],
    "address": [
      "Αγίου Ιωάννη 1",
      "133 42 Άνω Λιόσια"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Γεννήσεως Χριστού Καματερού",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/genniseos-xristoy-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "gennisis.christou@imiliou.gr"
    ],
    "address": [
      "Ανοίξεως 20",
      "134 51 Καματερό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Δημητρίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/naos/axarnon/content/agioy-dimitrioy-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.dimitrios-ah@imiliou.gr"
    ],
    "address": [
      "Λεωφ. Δημοκρατίας 109",
      "136 75 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Δημητρίου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/ano-liosia/content/agioy-dimitrioy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.dimitrios-al@imiliou.gr"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Βλασίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/naos/axarnon/content/agioy-blasioy-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.vlasios@imiliou.gr"
    ],
    "address": [
      "Φιλαδελφείας 1 (κεντρική πλατεία Αχαρνών)",
      "136 73 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Αποστόλων Πέτρου και Παύλου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/agion-apostolon-petroy-kai-payloy-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ap.petrospavlos-ah@imiliou.gr"
    ],
    "address": [
      "Αγίου Πέτρου 11",
      "136 74 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Αντωνίου και Ανδρέου Αυλώνα",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/agion-antonioy-kai-andreoy-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.antonios@imiliou.gr"
    ],
    "address": [
      "Αγίου Αντωνίου",
      "190 11 Αυλώνας"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Διονυσίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/naos/axarnon/content/agioy-dionysioy-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.dionysios-ah@imiliou.gr"
    ],
    "address": [
      "Αγίου Διονυσίου 37",
      "136 74 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Ζωοδόχου Πηγής Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/ilioy/content/zoodoxoy-pigis-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "address": [
      "Αγίων Θεοδώρων 6",
      "131 21 Ίλιον"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Διονυσίου Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/ilioy/content/agioy-dionysioy-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "address": [
      "Αετόπετρας 23",
      "131 22 Ίλιον"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Βαρβάρας Ιλίου",
    "detail": "https://imiliou.gr/index.php/aviliou",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Ίλιον",
    "phones": [
      "+30 210-261-0455"
    ],
    "emails": [
      "ag.varvara@imiliou.gr"
    ],
    "address": [
      ""
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Δημητρίου Πετρουπόλεως",
    "detail": "https://imiliou.gr/naos/enoriakoi-ieroi-naoi/content/agioy-dimitrioy-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.dimitrios-pe@imiliou.gr"
    ],
    "address": [
      "Δωδεκανήσου 85",
      "132 31 Πετρούπολη"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αποστόλων Πέτρου και Παύλου Βαρυμπόμπης",
    "detail": "https://imiliou.gr/index.php/naos/enoriakoi-ieroi-naoi/content/apostolon-petroy-kai-payloy-barympompis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ap.petrospavlos-va@imiliou.gr"
    ],
    "address": [
      "Αγίου Αντωνίου 1",
      "136 72 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίου Γεωργίου Καματερού",
    "detail": "https://imiliou.gr/index.php/naos/kamatero/content/agios-georgios-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "phones": [
      "+30 210-231-8977",
      "+30 210-238-8235"
    ],
    "emails": [
      "ag.georgios-ka@imiliou.gr"
    ],
    "address": [
      "Αγίου Γεωργίου 4",
      "134 51 Καματερό"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Ευαγγελισμός της Θεοτόκου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/ano-liosia/content/eyaggelismos-tis-theotokoy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "evangelismos-al@imiliou.gr"
    ],
    "address": [
      "Θεσσαλίας και Λαρίσης",
      "133 41 Άνω Λιόσια"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίας Αικατερίνης Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/ilion/content/agia-aikaterini-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "address": [
      "Αριστείδου και Αγίας Αικατερίνης",
      "131 22 Ίλιον"
    ]
  },
  {
    "rank": "Parish Church",
    "title": "Αγίων Κωνσταντίνου και Ελένης Άνω Λιοσίων",
    "detail": "https://imiliou.gr/agion-konstantinoy-kai-elenis-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriakoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "phones": [
      "+30 210-247-2113",
      "+30 210-247-2946"
    ],
    "emails": [
      "ag.konstantinos-al@imiliou.gr"
    ],
    "address": [
      "Αχαρνών 53",
      "133 41 Άνω Λιόσια"
    ]
  },
  {
    "rank": "Pilgrimage Church",
    "title": "Προσκυνηματικός Ναός Αγίου Νεκταρίου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/ano-liosia/content/proskynimatikos-naos-agioy-nektarioy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/proskynimatikoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.nektarios@imiliou.gr"
    ],
    "address": [
      "Αγίου Νεκταρίου 7",
      "133 41 Άνω Λιόσια"
    ]
  },
  {
    "rank": "Pilgrimage Church",
    "title": "Προσκυνηματικός Ναός Παναγίας Σουμελά",
    "detail": "https://imiliou.gr/naos/axarnes/content/panagias-soymela",
    "category": "https://imiliou.gr/category/typos-naoy/proskynimatikoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "soumela@imiliou.gr"
    ],
    "address": [
      "Ελ. Βενιζέλου 73",
      "136 74 Αχαρνές"
    ]
  },
  {
    "rank": "Pilgrimage Church",
    "title": "Προσκυνηματικός Ναός Αγίας Παρασκευής Ανάκασας",
    "detail": "https://imiliou.gr/naos/agioi-anargyroi-anakasa/content/proskynimatikos-naos-agias-paraskeyis-anakasas",
    "category": "https://imiliou.gr/category/typos-naoy/proskynimatikoi-ieroi-naoi",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "emails": [
      "ag.paraskevi-an@imiliou.gr"
    ],
    "address": [
      "Γεωργίου Παπανδρέου 175",
      "135 62 Άγιοι Ανάργυροι"
    ]
  },
  {
    "rank": "Metropolitan Chapel",
    "title": "Αγίου Νικολάου Περιστεριών Σαλαμίνας",
    "detail": "https://imiliou.gr/agioy-nikolaoy-peristerion-salaminas",
    "category": "https://imiliou.gr/category/typos-naoy/mitropolitika-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Προφήτη Ηλία Αχαρνών",
    "detail": "https://imiliou.gr/parekklisi-profiti-ilia-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Μαρίνας Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-agias-marinas-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Σοφίας Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-agias-sofias-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Προσκυνητάρι Αγίας Παρασκευής, Αφιδνών",
    "detail": "https://imiliou.gr/proskynitari-agias-paraskeyis-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Προσκυνητάρι Αγίου Μερκουρίου",
    "detail": "https://imiliou.gr/proskynitari-agioy-merkoyrioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Ζωοδόχου Πηγής Αχαρνών",
    "detail": "https://imiliou.gr/parekklisi-zoodohoy-pigis-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Αθανασίου Πετρουπόλεως",
    "detail": "https://imiliou.gr/parekklisi-agioy-athanasioy-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Γεωργίου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-agioy-georgioy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Παναγίτσας - Ζωοδόχου Πηγής - Εισοδίων της Θεοτόκου Βαρυμπόμπης",
    "detail": "https://imiliou.gr/parekklisi-panagitsas-zoodohoy-pigis-eisodion-tis-theotokoy-barympompis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "address": [
      "Τύμβου Σοφοκλέους",
      "136 77 Αχαρνές"
    ]
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Αποστόλων Πέτρου και Παύλου Αχαρνών (Παλαιός Ναός)",
    "detail": "https://imiliou.gr/parekklisi-agion-apostolon-petroy-kai-payloy-aharnon-palaios-naos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Ταξιαρχών Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agion-taxiarhon-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Ιωάννου του Προδρόμου Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agioy-ioannoy-toy-prodromoy-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Σπυρίδωνος Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agioy-spyridonos-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Αθανασίου Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agioy-athanasioy-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Κυριακής Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agias-kyriakis-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Παρασκευής Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agias-paraskeyis-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Μαρίνας Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agias-marinas-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Γεωργίου Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-agioy-georgioy-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Εισοδίων της Θεοτόκου Παναγίτσας Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-eisodion-tis-theotokoy-panagitsas-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Κοιμήσεως Θεοτόκου Αυλώνα",
    "detail": "https://imiliou.gr/parekklisi-koimiseos-theotokoy-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Κυριακής Βαρυμπόμπης",
    "detail": "https://imiliou.gr/index.php/parekklisi-agias-kyriakis-barympompis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νεκταρίου Καματερού",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-nektarioy-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Παμμεγίστων Ταξιαρχών Καματερού",
    "detail": "https://imiliou.gr/index.php/parekklisi-pammegiston-taxiarhon-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Πέτρου θέση Μόλα Πάρνηθα",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-petroy-thesi-mola-parnitha",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Ελευθερίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-eleytherioy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Τριάδας Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agias-triadas-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Φανουρίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-fanoyrioy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Παντελεήμονος Κρυονερίου (Παλαιός Ναός)",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-panteleimonos-kryonerioy-palaios-naos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νικολάου Κρυονερίου",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-nikolaoy-kryonerioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Εισοδίων της Θεοτόκου Κρυονερίου",
    "detail": "https://imiliou.gr/index.php/parekklisi-eisodion-tis-theotokoy-kryonerioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Δημητρίου Κρυονερίου",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-dimitrioy-kryonerioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Μαύρας και Αγίου Τιμοθέου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agias-mayras-kai-agioy-timotheoy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Ιωάννου του Προδρόμου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-ioannoy-toy-prodromoy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Θεοδώρων Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agion-theodoron-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Αθανασίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-athanasioy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Παρασκευής Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agias-paraskeyis-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Πάντων Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agion-panton-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Χαραλάμπους Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-haralampoys-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Δημητρίου Αυλώνα",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-dimitrioy-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Κωνσταντίνου και Ελένης Αυλώνα",
    "detail": "https://imiliou.gr/index.php/parekklisi-agion-konstantinoy-kai-elenis-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Κοιμήσεως Θεοτόκου Φυλής (Παλαιός Ναός)",
    "detail": "https://imiliou.gr/parekklisi-koimiseos-theotokoy-fylis-palaios-naos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Παρασκευής Φυλής (Αρχαία Πηγή)",
    "detail": "https://imiliou.gr/parekklisi-agias-paraskeyis-fylis-arhaia-pigi",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Παρασκευής Φυλής (Πλατεία)",
    "detail": "https://imiliou.gr/parekklisi-agias-paraskeyis-fylis-plateia",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Προφήτη Ηλία Φυλής (Δεξαμενή)",
    "detail": "https://imiliou.gr/index.php/parekklisi-profiti-ilia-fylis-dexameni",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νικολάου Φυλής",
    "detail": "https://imiliou.gr/parekklisi-agioy-nikolaoy-fylis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νικολάου Νεομάρτυρος Φυλής (Κοκκινόχωμα)",
    "detail": "https://imiliou.gr/parekklisi-agioy-nikolaoy-neomartyros-fylis-kokkinohoma",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Γεωργίου Φυλής (Κοκκινόχωμα)",
    "detail": "https://imiliou.gr/parekklisi-agioy-georgioy-fylis-kokkinohoma",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Κυριακής Φυλής",
    "detail": "https://imiliou.gr/parekklisi-agias-kyriakis-fylis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Αθανασίου Φυλής",
    "detail": "https://imiliou.gr/parekklisi-agioy-athanasioy-fylis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Άννης Φυλής",
    "detail": "https://imiliou.gr/parekklisi-agias-annis-fylis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Άγιου Πέτρου, Φυλής.",
    "detail": "https://imiliou.gr/parekklisi-agioy-petroy-fylis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Δημητρίου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-agioy-dimitrioy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Οσίου Δαυίδ του εν Ευβοίας Ιλίου",
    "detail": "https://imiliou.gr/index.php/parekklisi-osioy-dayid-toy-en-eyboias-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Τριάδας Βαρυμπόμπης",
    "detail": "https://imiliou.gr/index.php/parekklisi-agias-triadas-barympompis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Ιωάννου Θεολόγου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-ioannoy-theologoy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Δημητρίου Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-dimitrioy-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Λεωνίδα Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-leonida-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Σπυρίδωνος Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-spyridonos-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Κωνσταντίνου και Ελένης Αχαρνών",
    "detail": "https://imiliou.gr/index.php/parekklisi-agion-konstantinoy-kai-elenis-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Εισοδίων της Θεοτόκου (Φοβερά Προστασία) Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-eisodion-tis-theotokoy-fobera-prostasia-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Χριστοφόρου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-agioy-hristoforoy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Παναγή Μπασιά Άνω Λιοσίων",
    "detail": "https://imiliou.gr/parekklisi-agioy-panagi-mpasia-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Γεωργίου Βουρδουμπά Θρακομακεδόνων",
    "detail": "https://imiliou.gr/index.php/parekklisi-agioy-georgioy-boyrdoympa-thrakomakedonon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Φανουρίου (Ιπποκράτειος πολιτεία) Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-fanoyrioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Φανουρίου Αφιδνών (Κεντρικού Ναού)",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-fanoyrioy-afidnon-kentrikoy-naoy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Τεσσαράκοντα Μαρτύρων Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agion-tessarakonta-martyron-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Άννας Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-annas-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Εισοδίων Θεοτόκου Κηπουπόλεως",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/eisodion-theotokoy-kipoypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Ευαγγελισμός της Θεοτόκου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/enoriaka-parekklisia/content/parekklisi-eyaggelismoy-tis-theotokoy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αποτομή Κεφαλής Ιωάννου του Προδρόμου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-apotomis-kefalis-ioannoy-prodromoy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Μεταμορφώσεως του Σωτήρος Αχαρνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-metamorfoseos-toy-sotiros-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα",
    "address": [
      "Λεωφ. Κωνσταντίνου Καραμανλή & Φιλοκτήτου 4, ΛΑΘΕΑ, 136 72 Αχαρναί."
    ]
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νικολάου Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-nikolaoy-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Προφήτη Ηλία Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-profiti-ilia-kamateroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Γλυκερίας Πετρουπόλεως",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-glykerias-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Φανουρίου Πετρουπόλεως",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-fanoyrioy-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Προφήτη Ηλία Ιλίου (Πάρκο Τρίτση)",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-profiti-ilia-parko-tritsi-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Μερκουρίου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-merkoyrioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Ζωοδόχου Πηγής Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-zoodoxoy-pigis-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Ειρήνης Χρυσοβαλάντου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-eirinis-xrysobalantoy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Προφήτη Ηλία Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-profiti-ilia-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Υψώσεως Τιμίου Σταυρού Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-ypsoseos-timioy-stayroy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Μεταμόρφωση του Σωτήρος Αυλώνα",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-metamorfosi-toy-sotiros-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Τριάδας Αυλώνα",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-triadas-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νικολάου Νεομάρτυρος εξ Ιωαννίνων Αυλώνα",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-nikolaoy-neomartyros-eks-ioanninon-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Λουκά Αρχιεπισκόπου Συμφερουπόλεως Άνω Λιοσίων",
    "detail": "https://imiliou.gr/naos/enoriaka-parekklisia/content/parekklisi-agioy-loyka-arxiepiskopoy-symferoypoleos-toy-iatroy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Οσίου Μελετίου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-meletioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Μεταμορφώσεως του Σωτήρος Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-metamorfoseos-toy-sotiros-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Αναργύρων Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agion-anargyron-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Παρασκευής Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-paraskeyis-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Νικολάου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-nikolaoy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Μαρίνας Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-marinas-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Θεοδώρων Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agion-theodoron-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Γεωργίου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-georgioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Βλασίου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-blasioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Τριάδας Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-triadas-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Σώζοντος Καταυλισμού ΚΑΠΩΤΑ Αχαρνών",
    "detail": "https://imiliou.gr/index.php/naos/axarnes/content/agioy-sozontos-kataylismoy-kapota-axarnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Αθανασίου Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-athanasioy-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίας Παρασκευής Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agias-paraskeyis-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίου Αντωνίου Βαρυμπόμπης",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agioy-antonioy-barympompis",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Parish Chapel",
    "title": "Παρεκκλήσι Αγίων Ραφαήλ, Νικολάου και Ειρήνης Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/enoriaka-parekklisia/content/parekklisi-agion-rafail-nikolaoy-kai-eirinis-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/enoriaka-parekklisia",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Institutional Chapel",
    "title": "Παρεκκλήσι Αποστόλου Παύλου Εθνικού Ιδρύματος Νεότητας Ιλίου",
    "detail": "https://imiliou.gr/parekklisi-apostoloy-payloy-ethnikoy-idrymatos-neotitas-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-idrymaton",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Institutional Chapel",
    "title": "Παρεκκλήσι Αγίας Αικατερίνης Κέντρου Βρεφών \"ΜΗΤΕΡΑ\" Ιλίου",
    "detail": "https://imiliou.gr/naos/ilioy/content/parekklisi-agias-aikaterinis-kentroy-brefon-mitera-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-idrymaton",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Institutional Chapel",
    "title": "Παρεκκλήσι Ζωοδόχου Πηγής Εθνικού Κέντρου Αποκατάστασης Ιλίου",
    "detail": "https://imiliou.gr/naos/ilioy/content/parekklisi-zoodoxoy-pigis-ethnikoy-kentroy-apokatastasis-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-idrymaton",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Ευαγγελισμού της Θεοτόκου (Παλαιό) Αχαρνών",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-eyaggelismoy-tis-theotokoy-palaio-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αναστάσεως του Λαζάρου Άνω Λιοσίων",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-anastaseos-toy-lazaroy-ano-liosion",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αγίου Παντελεήμονος (Νέο) Αχαρνών",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-agioy-panteleimonos-neo-aharnon",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αναλήψεως Αυλώνα",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-analipseos-aylona",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αγίων Ταξιαρχών Κρυονερίου",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-agion-taxiarhon-kryonerioy",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αγίου Ιωάννου Θεολόγου Φυλής",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-agioy-ioannoy-theologoy-fylis",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αγίου Ιωάννου Θεολόγου Φυλής (Νέος Ναός)",
    "detail": "https://imiliou.gr/index.php/koimitiriako-parekklisi-agioy-ioannoy-theologoy-fylis-neos-naos",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Παρεκκλήσιο Αγίου Θωμά Πετρουπόλεως",
    "detail": "https://imiliou.gr/index.php/parekklisio-agioy-thoma-petroypoleos",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αγίων Θεοδώρων Ιλίου",
    "detail": "https://imiliou.gr/index.php/naos/ilioy/content/mitropolitiko-parekklisi-koimitiriakos-naos-agion-theodoron-ilioy",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Cemetery Chapel",
    "title": "Κοιμητηριακό Παρεκκλήσι Αγίας Κυριακής Αφιδνών",
    "detail": "https://imiliou.gr/index.php/naos/afidnes/content/koimitiriako-parekklisi-agias-kyriakis-afidnon",
    "category": "https://imiliou.gr/category/typos-naoy/parekklisia-koimitirion",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Hesychasterion",
    "title": "Ιερό Ησυχαστήριο Παναγία η Ιεροσολυμίτισσα",
    "detail": "https://imiliou.gr/iero-isyhastirio-panagia-i-ierosolymitissa",
    "category": "https://imiliou.gr/ieres-mones",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Monastery",
    "title": "Ιερά Μονή Γενεσίου της Θεοτόκου Ντάρδιζας",
    "detail": "https://imiliou.gr/iera-moni-genesioy-tis-theotokoy-ntardizas",
    "category": "https://imiliou.gr/ieres-mones",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Monastery",
    "title": "Ιερά Μονή Νέου Στουδίου Αυλώνος",
    "detail": "https://imiliou.gr/iera-moni-neoy-stoydioy-aylonos",
    "category": "https://imiliou.gr/ieres-mones",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Monastery",
    "title": "Ιερά Μονή Αγίου Παντελεήμονος Πετρουπόλεως",
    "detail": "https://imiliou.gr/iera-moni-agioy-panteleimonos-petroypoleos",
    "category": "https://imiliou.gr/ieres-mones",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  },
  {
    "rank": "Monastery",
    "title": "Ιερά Μονή Κοιμήσεως Θεοτόκου Κλειστών",
    "detail": "https://imiliou.gr/iera-moni-koimiseos-theotokoy-kleiston",
    "category": "https://imiliou.gr/ieres-mones",
    "seat_local": "Άγιοι Ανάργυροι-Ανάκασα"
  }
]
""")

CONTACT_OVERRIDES = json.loads(r"""
{
  "Ευαγγελισμός της Θεοτόκου Ιλίου (Μητροπολιτικός)": {
    "phones": [
      "+30 210-261-3009",
      "+30 210-263-9260"
    ],
    "emails": [
      "evangelismos-il@imiliou.gr"
    ]
  },
  "Παναγίας Γοργοεπηκόου Ζεφυρίου (Γρηγορούσα)": {
    "phones": [
      "+30 210-231-0668"
    ],
    "emails": [
      "grigorousa@imiliou.gr"
    ]
  },
  "Προφήτη Ηλία Αχαρνών": {
    "phones": [
      "+30 213-090-8990"
    ],
    "emails": [
      "pr.ilias-ah@imiliou.gr"
    ]
  },
  "Αγίας Παρασκευής Αχαρνών": {
    "phones": [
      "+30 210-244-3920"
    ],
    "emails": [
      "ag.paraskevi-ah@imiliou.gr"
    ]
  },
  "Αγίας Τριάδας Θρακομακεδόνων": {
    "phones": [
      "+30 210-243-1376"
    ],
    "emails": [
      "ag.triada-th@imiliou.gr"
    ]
  },
  "Αγίου Παντελεήμονος Κρυονερίου": {
    "phones": [
      "+30 210-816-1311"
    ],
    "emails": [
      "ag.panteleimon@imiliou.gr"
    ]
  },
  "Αγίων Κωνσταντίνου και Ελένης Άνω Αχαρνών (Μεγάλα Σχίνα)": {
    "phones": [
      "+30 210-244-0477"
    ],
    "emails": [
      "ag.konstantinos-aa@imiliou.gr"
    ]
  },
  "Αγίων Κυρίλλου και Μεθοδίου Ολυμπιακού Χωρίου": {
    "phones": [
      "+30 210-244-0772"
    ],
    "emails": [
      "ag.kyrillosmethodios@imiliou.gr"
    ]
  },
  "Αγίας Άννης Αχαρνών": {
    "phones": [
      "+30 210-231-2686"
    ],
    "emails": [
      "ag.anna@imiliou.gr"
    ]
  },
  "Κοιμήσεως Θεοτόκου Αχαρνών": {
    "phones": [
      "+30 210-246-1213"
    ],
    "emails": [
      "koimisis.theotokou-ah@imiliou.gr"
    ]
  },
  "Αγίας Τριάδας Καματερού": {
    "phones": [
      "+30 210-231-6377"
    ],
    "emails": [
      "ag.triada-ka@imiliou.gr"
    ]
  },
  "Αγίου Νικολάου Ιλίου": {
    "phones": [
      "+30 210-232-0645"
    ],
    "emails": [
      "ag.nikolaos@imiliou.gr"
    ]
  },
  "Κοιμήσεως Θεοτόκου Φυλής (Χασιά)": {
    "phones": [
      "+30 210-241-1019"
    ],
    "emails": [
      "koimisis.theotokou-fy@imiliou.gr"
    ]
  },
  "Αγίας Τριάδας Πετρουπόλεως": {
    "phones": [
      "+30 210-501-3108"
    ],
    "emails": [
      "ag.triada-pe@imiliou.gr"
    ]
  },
  "Κοιμήσεως Θεοτόκου Πετρουπόλεως": {
    "phones": [
      "+30 210-501-6163"
    ],
    "emails": [
      "koimisis.theotokou-pe@imiliou.gr"
    ]
  },
  "Αγίου Γεωργίου Ζωφριάς": {
    "phones": [
      "+30 693-713-0308"
    ],
    "emails": [
      "ag.georgios-al@imiliou.gr"
    ]
  },
  "Αγίων Αποστόλων (Ρέθι) Αχαρνών": {
    "phones": [
      "+30 210-246-4306"
    ],
    "emails": [
      "ag.antonios@imiliou.gr"
    ]
  },
  "Αγίου Γεωργίου Αχαρνών": {
    "phones": [
      "+30 210-246-9823"
    ],
    "emails": [
      "ag.georgios-ah@imiliou.gr"
    ]
  },
  "Αγίου Τρύφωνα Καματερού": {
    "phones": [
      "+30 210-231-1610"
    ],
    "emails": [
      "ag.tryfon@imiliou.gr"
    ]
  },
  "Παμμεγίστων Ταξιαρχών Αχαρνών": {
    "phones": [
      "+30 210-246-4655"
    ],
    "emails": [
      "taxiarches@imiliou.gr"
    ]
  },
  "Αγίου Στυλιανού Ζεφυρίου": {
    "phones": [
      "+30 210-247-0273"
    ],
    "emails": [
      "ag.stylianos@imiliou.gr"
    ]
  },
  "Αγίου Σπυρίδωνος Καματερού": {
    "phones": [
      "+30 210-231-2973"
    ],
    "emails": [
      "ag.spyridon@imiliou.gr"
    ]
  },
  "Προφήτη Ηλία Πετρουπόλεως": {
    "phones": [
      "+30 210-502-7850"
    ],
    "emails": [
      "pr.ilias-pe@imiliou.gr"
    ]
  },
  "Αγίων Μυροφόρων και Νικόδημου Αγίων Αναργύρων": {
    "phones": [
      "+30 210-238-5901"
    ],
    "emails": [
      "ag.myrofores@imiliou.gr"
    ]
  },
  "Μεταμορφώσεως του Σωτήρος Άνω Λιοσίων": {
    "phones": [
      "+30 210-247-3355"
    ],
    "emails": [
      "metamorfosis@imiliou.gr"
    ]
  },
  "Αγίων Κωνσταντίνου και Ελένης Κάτω Αχαρνών (Λυκότρυπα)": {
    "phones": [
      "+30 210-231-6550"
    ],
    "emails": [
      "ag.konstantinos-ka@imiliou.gr"
    ]
  },
  "Κοιμήσεως Θεοτόκου (Παλατιανής) Ιλίου": {
    "phones": [
      "+30 210-261-4336"
    ],
    "emails": [
      "palatiani@imiliou.gr"
    ]
  },
  "Κοιμήσεως Θεοτόκου Αφιδνών": {
    "phones": [
      "+30 229-502-2329"
    ],
    "emails": [
      "koimisis.theotokou-af@imiliou.gr"
    ]
  },
  "Αγίου Ιωάννου του Θεολόγου Άνω Λιοσίων": {
    "phones": [
      "+30 210-247-2896"
    ],
    "emails": [
      "ag.ioannis@imiliou.gr"
    ]
  },
  "Γεννήσεως Χριστού Καματερού": {
    "phones": [
      "+30 210-238-8108"
    ],
    "emails": [
      "gennisis.christou@imiliou.gr"
    ]
  },
  "Αγίου Δημητρίου Αχαρνών": {
    "phones": [
      "+30 210-246-2249"
    ],
    "emails": [
      "ag.dimitrios-ah@imiliou.gr"
    ]
  },
  "Αγίου Δημητρίου Άνω Λιοσίων": {
    "phones": [
      "+30 210-247-1059"
    ],
    "emails": [
      "ag.dimitrios-al@imiliou.gr"
    ]
  },
  "Αγίου Βλασίου Αχαρνών": {
    "phones": [
      "+30 210-246-9187"
    ],
    "emails": [
      "ag.vlasios@imiliou.gr"
    ]
  },
  "Αγίων Αποστόλων Πέτρου και Παύλου Αχαρνών": {
    "phones": [
      "+30 210-246-6316"
    ],
    "emails": [
      "ap.petrospavlos-ah@imiliou.gr"
    ]
  },
  "Αγίων Αντωνίου και Ανδρέου Αυλώνα": {
    "phones": [
      "+30 229-504-1350"
    ],
    "emails": [
      "ag.antonios@imiliou.gr"
    ]
  },
  "Αγίου Διονυσίου Αχαρνών": {
    "phones": [
      "+30 210-246-3144"
    ],
    "emails": [
      "ag.dionysios-ah@imiliou.gr"
    ]
  },
  "Ζωοδόχου Πηγής Ιλίου": {
    "phones": [
      "+30 210-573-0324"
    ],
    "emails": [
      "zoodochos.pigi@imiliou.gr"
    ]
  },
  "Αγίου Διονυσίου Ιλίου": {
    "phones": [
      "+30 210-263-4025"
    ],
    "emails": [
      "ag.dionysios-il@imiliou.gr"
    ]
  },
  "Αγίας Βαρβάρας Ιλίου": {
    "phones": [
      "+30 210-261-0455"
    ],
    "emails": [
      "ag.varvara@imiliou.gr"
    ]
  },
  "Αγίου Δημητρίου Πετρουπόλεως": {
    "phones": [
      "+30 210-501-2027"
    ],
    "emails": [
      "ag.dimitrios-pe@imiliou.gr"
    ]
  },
  "Αποστόλων Πέτρου και Παύλου Βαρυμπόμπης": {
    "phones": [
      "+30 210-816-9590"
    ],
    "emails": [
      "ap.petrospavlos-va@imiliou.gr"
    ]
  },
  "Αγίου Γεωργίου Καματερού": {
    "phones": [
      "+30 210-231-8977",
      "+30 210-238-8235"
    ],
    "emails": [
      "ag.georgios-ka@imiliou.gr"
    ]
  },
  "Ευαγγελισμός της Θεοτόκου Άνω Λιοσίων": {
    "phones": [
      "+30 210-247-1156"
    ],
    "emails": [
      "evangelismos-al@imiliou.gr"
    ]
  },
  "Αγίας Αικατερίνης Ιλίου": {
    "phones": [
      "+30 210-263-4188"
    ],
    "emails": [
      "ag.aikaterini@imiliou.gr"
    ]
  },
  "Αγίων Κωνσταντίνου και Ελένης Άνω Λιοσίων": {
    "phones": [
      "+30 210-247-2113",
      "+30 210-247-2946"
    ],
    "emails": [
      "ag.konstantinos-al@imiliou.gr"
    ]
  },
  "Προσκυνηματικός Ναός Αγίου Νεκταρίου Άνω Λιοσίων": {
    "phones": [
      "+30 210-248-6621"
    ],
    "emails": [
      "ag.nektarios@imiliou.gr"
    ]
  },
  "Προσκυνηματικός Ναός Παναγίας Σουμελά": {
    "phones": [
      "+30 210-244-5825"
    ],
    "emails": [
      "soumela@imiliou.gr"
    ]
  },
  "Προσκυνηματικός Ναός Αγίας Παρασκευής Ανάκασας": {
    "phones": [
      "+30 210-261-4186"
    ],
    "emails": [
      "ag.paraskevi-an@imiliou.gr"
    ]
  },
  "Παρεκκλήσι Αγίου Αντωνίου Βαρυμπόμπης": {
    "phones": [
      "+30 210-816-9590"
    ],
    "emails": []
  },
  "Παρεκκλήσι Ζωοδόχου Πηγής Εθνικού Κέντρου Αποκατάστασης Ιλίου": {
    "phones": [
      "+30 697-712-8844"
    ],
    "emails": []
  },
  "Ιερό Ησυχαστήριο Παναγία η Ιεροσολυμίτισσα": {
    "phones": [
      "+30 210-244-5141"
    ],
    "emails": []
  },
  "Ιερά Μονή Γενεσίου της Θεοτόκου Ντάρδιζας": {
    "phones": [
      "+30 210-246-0956"
    ],
    "emails": []
  },
  "Ιερά Μονή Νέου Στουδίου Αυλώνος": {
    "phones": [
      "+30 229-530-0972"
    ],
    "emails": []
  },
  "Ιερά Μονή Αγίου Παντελεήμονος Πετρουπόλεως": {
    "phones": [
      "+30 210-501-3639"
    ],
    "emails": []
  },
  "Ιερά Μονή Κοιμήσεως Θεοτόκου Κλειστών": {
    "phones": [
      "+30 210-241-1314"
    ],
    "emails": []
  }
}
""")

ALLOWED_HOSTS = {
    "imiliou.gr", "www.imiliou.gr", "ecclesiagreece.gr", "www.ecclesiagreece.gr",
}
FORBIDDEN_PUNCTUATION = re.compile(r"[\u2013\u2014\u2015\u2018\u2019\u201c\u201d\ufffd]")
CLERGY_TERMS = re.compile(
    r"\b(?:Αρχιμανδρίτης|Πρωτοπρεσβύτερος|Πρεσβύτερος|Διάκονος|Ηγουμένη|Μοναχή)\b",
    re.IGNORECASE,
)

TRANSLIT = str.maketrans({
    "Α":"A","Β":"V","Γ":"G","Δ":"D","Ε":"E","Ζ":"Z","Η":"I","Θ":"Th","Ι":"I",
    "Κ":"K","Λ":"L","Μ":"M","Ν":"N","Ξ":"X","Ο":"O","Π":"P","Ρ":"R","Σ":"S",
    "Τ":"T","Υ":"Y","Φ":"F","Χ":"Ch","Ψ":"Ps","Ω":"O",
    "α":"a","β":"v","γ":"g","δ":"d","ε":"e","ζ":"z","η":"i","θ":"th","ι":"i",
    "κ":"k","λ":"l","μ":"m","ν":"n","ξ":"x","ο":"o","π":"p","ρ":"r","σ":"s",
    "ς":"s","τ":"t","υ":"y","φ":"f","χ":"ch","ψ":"ps","ω":"o",
})
PHRASES = (
    ("Μεταμορφώσεως του Σωτήρος", "Transfiguration of the Savior"),
    ("Αποστόλων Πέτρου και Παύλου", "Apostles Peter and Paul"),
    ("Αγίων Κωνσταντίνου και Ελένης", "Saints Constantine and Helen"),
    ("Αγίων Κυρίλλου και Μεθοδίου", "Saints Cyril and Methodius"),
    ("Κοιμήσεως της Θεοτόκου", "Dormition of the Theotokos"),
    ("Κοιμήσεως Θεοτόκου", "Dormition of the Theotokos"),
    ("Γενεσίου της Θεοτόκου", "Nativity of the Theotokos"),
    ("Ευαγγελισμός της Θεοτόκου", "Annunciation of the Theotokos"),
    ("Ευαγγελισμού της Θεοτόκου", "Annunciation of the Theotokos"),
    ("Ζωοδόχου Πηγής", "Life-giving Spring"),
    ("Αναστάσεως του Λαζάρου", "Raising of Lazarus"),
    ("Παμμεγίστων Ταξιαρχών", "Holy Archangels"),
    ("Προφήτη Ηλία", "Prophet Elias"),
    ("Αγίας Τριάδας", "Holy Trinity"),
    ("Αγία Τριάδα", "Holy Trinity"),
    ("Αγίου", "Saint"),
    ("Αγίας", "Saint"),
    ("Αγίων", "Saints"),
    ("Αγιοι", "Saints"),
    ("Παναγίας", "Panagia"),
)
PREFIXES = (
    "Κοιμητηριακό Παρεκκλήσι ", "Κοιμητηριακό Παρεκκλήσιο ",
    "Προσκυνηματικός Ναός ", "Ιερός Προσκυνηματικός Ναός ",
    "Παρεκκλήσι ", "Παρεκκλήσιο ", "Ιερό Ησυχαστήριο ", "Ιερά Μονή ",
)


def romanize(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value.translate(TRANSLIT)).strip()


def english_name(local, rank):
    value = local
    for prefix in PREFIXES:
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    for source, target in PHRASES:
        value = value.replace(source, target)
    value = romanize(value)
    labels = {
        "Parish Church": "Parish Church",
        "Pilgrimage Church": "Pilgrimage Church",
        "Metropolitan Chapel": "Metropolitan Chapel",
        "Parish Chapel": "Parish Chapel",
        "Institutional Chapel": "Institutional Chapel",
        "Cemetery Chapel": "Cemetery Chapel",
        "Monastery": "Monastery",
        "Hesychasterion": "Hesychasterion",
    }
    return "%s %s" % (value, labels[rank])


def slug(value):
    value = romanize(value).casefold()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "body"


def make_rows():
    rows = []
    for index, raw in enumerate(RAW, 1):
        rank = raw["rank"]
        local = raw["title"]
        seat = romanize(raw["seat_local"])
        item = {
            "id": "gr-ilion-%03d-%s" % (index, slug(local)),
            "parent": PARENT,
            "kind": "monastery" if rank in ("Monastery", "Hesychasterion") else "parish",
            "rank": rank,
            "name": english_name(local, rank),
            "local": local,
            "seat": seat,
            "country": "GR",
            "sources": list(dict.fromkeys((raw["detail"], raw["category"]))),
        }
        if raw.get("address"):
            item["address"] = list(raw["address"]) + ["Ελλάδα"]
        contacts = CONTACT_OVERRIDES.get(local) or {}
        if contacts.get("phones"):
            item["phones"] = list(contacts["phones"])
        if contacts.get("emails"):
            item["emails"] = list(contacts["emails"])
        if item.get("phones") or item.get("emails"):
            item["contact_sources"] = [raw["detail"]]
            item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


ROWS = make_rows()
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}

EXPECTED_TOTAL = 167
EXPECTED_OWNER_COUNTS = {PARENT: 167}
EXPECTED_KINDS = {"monastery": 5, "parish": 162}
EXPECTED_RANKS = {
    "Cemetery Chapel": 10,
    "Hesychasterion": 1,
    "Institutional Chapel": 3,
    "Metropolitan Chapel": 1,
    "Monastery": 4,
    "Parish Chapel": 100,
    "Parish Church": 45,
    "Pilgrimage Church": 3,
}
EXPECTED_COVERAGE = (55, 55, 58, 48, 48, 0, 49)
EXISTING_PARENTS = {PARENT}


def validate_url(value, label):
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc.casefold() not in ALLOWED_HOSTS:
        raise ValueError("%s carries a non-competent source: %s" % (label, value))


def clean(source):
    item = {key: value for key, value in source.items() if value not in (None, "", [])}
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must carry one to three sources" % item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    contact_sources = list(item.get("contact_sources") or [])
    if item.get("phones") or item.get("emails") or item.get("site"):
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks exact current contact provenance" % item.get("id"))
    for source_url in contact_sources:
        validate_url(source_url, item.get("id"))
    return item


def coverage_tuple(rows):
    return (
        sum(bool(item.get("phones") or item.get("emails") or item.get("site")) for item in rows),
        sum(bool(item.get("phones")) for item in rows),
        sum(len(item.get("phones") or []) for item in rows),
        sum(bool(item.get("emails")) for item in rows),
        sum(len(item.get("emails") or []) for item in rows),
        sum(bool(item.get("site")) for item in rows),
        sum(bool(item.get("address")) for item in rows),
    )


def validate_ledger(expected_coverage=None):
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Ilion candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Ilion candidate ledger date drifted")
    summary = ledger.get("published_summary") or {}
    expected = {
        PARENT: EXPECTED_TOTAL,
        "total": EXPECTED_TOTAL,
        "current_parishes": 45,
        "current_pilgrimages": 3,
        "current_metropolitan_chapels": 1,
        "current_parish_chapels": 100,
        "current_institutional_chapels": 3,
        "current_cemetery_chapels": 10,
        "current_monasteries_and_hesychasteria": 5,
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise ValueError("Ilion ledger summary drifted at %s" % key)
    if expected_coverage:
        coverage_keys = (
            "contact_bodies", "phone_bodies", "public_phone_values",
            "email_bodies", "public_email_values", "body_owned_sites", "address_bodies",
        )
        if tuple(summary.get(key) for key in coverage_keys) != expected_coverage:
            raise ValueError("Ilion ledger contact summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Ilion ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Ilion ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or entry.get("id") or key)
    candidate_ids = [entry.get("candidate_id") for entry in ledger["candidates"]]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Ilion candidate IDs repeat")
    return ledger


def build():
    ids = set()
    signatures = {}
    owner_counts = Counter()
    kind_counts = Counter()
    rank_counts = Counter()
    result = []
    for source in ROWS:
        item = clean(source)
        row_id = item["id"]
        if row_id in ids:
            raise ValueError("duplicate Ilion ID: %s" % row_id)
        if item.get("parent") not in EXISTING_PARENTS:
            raise ValueError("%s has unknown parent" % row_id)
        if item.get("country") != "GR":
            raise ValueError("%s has wrong country" % row_id)
        if item.get("kind") not in ("parish", "monastery"):
            raise ValueError("%s has invalid kind" % row_id)
        for field in ("name", "local", "seat", "rank"):
            if not item.get(field):
                raise ValueError("%s lacks %s" % (row_id, field))
        rendered = json.dumps(item, ensure_ascii=False)
        if FORBIDDEN_PUNCTUATION.search(rendered):
            raise ValueError("%s carries forbidden punctuation" % row_id)
        if CLERGY_TERMS.search(rendered):
            raise ValueError("%s carries a clergy name or title" % row_id)
        signature = unicodedata.normalize(
            "NFKC", "%s|%s|%s" % (item["local"], item["seat"], item["rank"])
        ).casefold()
        signature = re.sub(r"\s+", " ", signature).strip()
        if signature in signatures:
            raise ValueError("%s duplicates %s" % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        owner_counts[item["parent"]] += 1
        kind_counts[item["kind"]] += 1
        rank_counts[item["rank"]] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Ilion English name coverage drifted")
    if set(ENGLISH_SEATS) != {item["seat"] for item in result}:
        raise ValueError("Ilion English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Ilion parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Ilion kind totals drifted: %r" % dict(kind_counts))
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Ilion rank totals drifted: %r" % dict(rank_counts))
    coverage = coverage_tuple(result)
    if coverage != EXPECTED_COVERAGE:
        raise ValueError("Ilion contact coverage drifted: %r" % (coverage,))
    validate_ledger(coverage)
    return {PARENT: {"v": 1, "parent": PARENT, "country": "GR", "rows": result}}


def normalize_source_text(value):
    value = html.unescape(re.sub(r"<[^>]+>", " ", value))
    value = value.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch_live_source(url, allow_access_control=False):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8",
        "Connection": "close",
    })
    try:
        with urlopen(request, timeout=60) as response:
            content_type = response.headers.get("Content-Type", "").lower()
            payload = response.read()
    except HTTPError as exc:
        if allow_access_control and exc.code in (403, 429, 520):
            return None
        raise
    if "pdf" in content_type or url.endswith(".pdf"):
        if not payload.startswith(b"%PDF") or len(payload) < 1000000:
            raise ValueError("invalid legal PDF payload")
        return None
    if "html" not in content_type:
        raise ValueError("unexpected content type %s" % content_type)
    return payload.decode("utf-8", "replace")


def listing_titles(payload):
    values = re.findall(
        r'<h2[^>]*>\s*<a\s+href="[^"]+"[^>]*>\s*(?:<span>)?([\s\S]*?)(?:</span>)?\s*</a>\s*</h2>',
        payload, re.IGNORECASE,
    )
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip() for value in values]


def live_category_count(url, pages):
    titles = []
    for page in range(pages):
        payload = fetch_live_source(url if page == 0 else url + "?page=" + str(page))
        titles.extend(listing_titles(payload))
    return titles


def check_markers(url, markers):
    payload = fetch_live_source(url, allow_access_control=True)
    if payload is None:
        return
    text = normalize_source_text(payload)
    for marker in markers:
        if normalize_source_text(marker) not in text:
            raise ValueError("live Ilion marker failed at %s: %s" % (url, marker))


def check_live_sources():
    specifications = (
        (PARISH_URL, 3, 45),
        (PILGRIMAGE_URL, 1, 3),
        (METROPOLITAN_CHAPEL_URL, 1, 1),
        (PARISH_CHAPEL_URL, 6, 102),
        (INSTITUTION_CHAPEL_URL, 1, 3),
        (CEMETERY_CHAPEL_URL, 1, 10),
        (MONASTERY_URL, 1, 5),
    )
    live = {}
    for url, pages, expected in specifications:
        titles = live_category_count(url, pages)
        if len(titles) != expected:
            raise ValueError("live Ilion count drifted at %s: %d" % (url, len(titles)))
        live[url] = titles
    if live[PARISH_CHAPEL_URL].count("Παρεκκλήσι Αγίας Σοφίας Άνω Λιοσίων") != 2:
        raise ValueError("live Ilion duplicate chapel reconciliation drifted")
    if not any("δε λειτουργείται-είναι ερείπια" in title for title in live[PARISH_CHAPEL_URL]):
        raise ValueError("live Ilion non-operating ruin marker drifted")
    check_markers(STRUCTURE_URL, (
        "Ενοριακοί Ναοί: 47", "Προσκυνηματικοί ναοί: 3",
        "Μητροπολιτικά Παρεκκλήσια: 6", "Ενοριακά Παρεκκλήσια: 94",
        "Παρεκκλήσια Ιδρυμάτων: 6", "Κοιμητηριακοί Ναοί: 9",
    ))
    check_markers(PROFILE_URL, ("Ιλίου", "Πετρουπόλεως", "Αχαρνών"))
    fetch_live_source(LEGAL_URL)
    build()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-live", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check_live:
        check_live_sources()
        print("Ilion live authoritative source check passed: %d exact bodies" % EXPECTED_TOTAL)
    elif args.check:
        print("Ilion check passed: %d exact bodies" % EXPECTED_TOTAL)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
