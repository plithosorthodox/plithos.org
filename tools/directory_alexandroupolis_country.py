#!/usr/bin/env python3
"""Validate exact named Alexandroupolis bodies from first-party rosters.

This module stays independent of the shared directory aggregator until its
country tranche is integrated.

    python tools/directory_alexandroupolis_country.py --check
    python tools/directory_alexandroupolis_country.py --dump
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
    ROOT / "tools" / "directory_candidates"
    / "alexandroupolis_country.json"
)

ROWS = json.loads(r'''[
  {
    "id": "gr-ep-alexandroupolis-001-metropolitan-and-cathedral-church-of-saint-nicholas-in-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Cathedral",
    "name": "Metropolitan and Cathedral Church of Saint Nicholas in Alexandroupolis",
    "local": "Ιερός Μητροπολιτικός & Καθεδρικός Ναός Αγίου Νικολάου Αλεξανδρουπόλεως",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/1_80.html"
    ],
    "address": [
      "Πλατεία Μητροπόλεως",
      "Τ.Κ. 68132 Αλεξανδρούπολη"
    ],
    "emails": [
      "snc@otenet.gr"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/1_80.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-002-saint-eleutherius-parish-church-in-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Eleutherius Parish Church in Alexandroupolis",
    "local": "Ιερός Ναός Αγίου Ελευθερίου Αλεξανδρουπόλεως",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1970/10/blog-post_21.html"
    ],
    "address": [
      "Υψηλάντου 4",
      "Τ.Κ. 68132, Αλεξανδρούπολη"
    ],
    "emails": [
      "snteleftherios@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1970/10/blog-post_21.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-003-saint-kyriaki-parish-church-in-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Kyriaki Parish Church in Alexandroupolis",
    "local": "Ιερός Ναός Αγίας Κυριακής Αλεξανδρουπόλεως",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/blog-post_21.html"
    ],
    "address": [
      "Πλαταιών και Αμφιπόλεως",
      "Τ.Κ. 68131 Αλεξανδρούπολη"
    ],
    "phones": [
      "25510-28819"
    ],
    "emails": [
      "i.n.agiaskiriakis@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/blog-post_21.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-004-transfiguration-of-the-savior-parish-church-in-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Transfiguration of the Savior Parish Church in Alexandroupolis",
    "local": "Ιερός Ναός Μεταμορφώσεως Σωτήρος Αλεξανδρουπόλεως",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1987/10/blog-post.html"
    ],
    "address": [
      "Κονδύλη 16",
      "Τ.Κ. 68132 Αλεξανδρούπολη"
    ],
    "emails": [
      "metamorfosialexandroupoli@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1987/10/blog-post.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-005-saint-nectarius-parish-church-in-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Nectarius Parish Church in Alexandroupolis",
    "local": "Ιερός Ναός Αγίου Νεκταρίου Αλεξανδρουπόλεως",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1986/10/blog-post.html",
      "https://nektariosimalex.blogspot.com/"
    ],
    "address": [
      "Ρόδου 86",
      "Τ.Κ. 68133 Αλεξανδρούπολη"
    ],
    "phones": [
      "25510-23686"
    ],
    "emails": [
      "agiosnektariosalexpolis@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1986/10/blog-post.html"
    ],
    "contact_checked": "2026-11-15",
    "site": "https://nektariosimalex.blogspot.com/"
  },
  {
    "id": "gr-ep-alexandroupolis-006-saint-basil-parish-church-in-kallithea-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Basil Parish Church in Kallithea, Alexandroupolis",
    "local": "Ιερός Ναός Αγίου Βασιλείου Καλλιθέας Αλεξανδρουπόλεως",
    "seat": "Kallithea, Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1985/10/blog-post.html"
    ],
    "address": [
      "Κουταβού & Χατζοπούλου",
      "Τ.Κ. 68131 Καλλιθέα Αλεξανδρούπολης"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-007-apostle-andrew-parish-church-in-nea-ergatika-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Apostle Andrew Parish Church in Nea Ergatika, Alexandroupolis",
    "local": "Ιερός Ναός Αγίου αποστόλου Ανδρέα Ν. Εργατικών Αλεξανδρουπόλεως",
    "seat": "Nea Ergatika, Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1984/10/blog-post.html"
    ],
    "address": [
      "Λεωφ. Μάκρης",
      "Τ.Κ. 68100 Ν. Εργατικά Αλεξανδρούπολης"
    ],
    "emails": [
      "agios.andreas@yahoo.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1984/10/blog-post.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-008-holy-unmercenaries-shrine-in-alexandroupolis-at-the-former-ioakeimeio-ho",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Shrine",
    "name": "Holy Unmercenaries Shrine in Alexandroupolis at the former Ioakeimeio Home for the Aged",
    "local": "Ιερός Προσκυνηματικός Ναός Αγίων Αναργύρων Αλεξανδρουπόλεως (παλαιού Ιωακειμείου Γηροκομείου)",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1983/10/blog-post.html"
    ],
    "address": [
      "Βελισσαρίου 18, (παλαιό Ιωακείμειο Γηροκομείο)",
      "Τ.Κ. 68131 Αλεξανδρούπολη"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-009-saint-catherine-chapel-in-alexandroupolis-at-the-former-hospital",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Chapel",
    "name": "Saint Catherine Chapel in Alexandroupolis at the former hospital",
    "local": "Ιερό Παρεκκλήσιο Αγίας Αικατερίνης Αλεξανδρουπόλεως (Παλαιού Νοσοκομείου)",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1983/10/blog-post_21.html"
    ],
    "address": [
      "Δήμητρας 19 (Παλαιό Νοσοκομείο)",
      "Τ.Κ. 68131 Αλεξανδρούπολη"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-010-panagia-strategissa-church-in-alexandroupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Church",
    "name": "Panagia Strategissa Church in Alexandroupolis",
    "local": "Ιερός Ναός Παναγίας Στρατηγίσσης",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1982/10/blog-post.html"
    ],
    "address": [
      "Περιφερειακή Οδός ( Δίπλα στο Στρατόπεδο ΖΗΣΗ)"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-011-saint-george-parish-church-in-nea-chili",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Nea Chili",
    "local": "Ιερός Ναός Αγίου Γεωργίου Νέας Χηλής",
    "seat": "Nea Chili",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1981/10/blog-post.html"
    ],
    "address": [
      "Τ.Κ. 68100 Νέα Χηλή Αλεξανδρουπόλεως"
    ],
    "emails": [
      "agiosgeorgiosneaschilis@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1981/10/blog-post.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-012-saint-marina-shrine-and-saint-george-parish-church-in-maistros",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Shrine",
    "name": "Saint Marina Shrine and Saint George Parish Church in Maistros",
    "local": "Ιερός Προσκυνηματικός Ναός Αγίας Μαρίνης Μαΐστρου (Ενοριακός Ι.Ν. Αγίου Γεωργίου)",
    "seat": "Maistros",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1980/10/blog-post.html"
    ],
    "address": [
      "Τ.Κ. 68100 Μαΐστρος Αλεξανδρουπόλεως"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-013-saint-panteleimon-parish-church-in-palagia",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Panteleimon Parish Church in Palagia",
    "local": "Ιερός Ναός Αγίου Παντελεήμονος Παλαγίας",
    "seat": "Palagia",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1979/10/blog-post.html"
    ],
    "address": [
      "Παλαγία",
      "Τ.Κ. 68100 Αλεξανδρούπολη"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-014-saint-george-parish-church-in-potamos",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Potamos",
    "local": "Ιερός Ναός Αγίου Γεωργίου Ποταμού",
    "seat": "Potamos",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_75.html"
    ],
    "address": [
      "Ποταμός",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-015-saint-george-parish-church-in-elaionas-makri",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Elaionas, Makri",
    "local": "Ιερός Ναός Αγίου Γεωργίου Ελαιώνα Μάκρης",
    "seat": "Elaionas, Makri",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_50.html"
    ],
    "address": [
      "Ελαιώνας Μάκρης",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-016-saint-demetrius-parish-church-in-iana",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Demetrius Parish Church in Iana",
    "local": "Ιερός Ναός Αγίου Δημητρίου Ιάνας",
    "seat": "Iana",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_95.html"
    ],
    "address": [
      "Ιάνα",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-017-saint-demetrius-parish-church-in-dikella",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Demetrius Parish Church in Dikella",
    "local": "Ιερός Ναός Αγίου Δημητρίου Δικέλλων",
    "seat": "Dikella",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_22.html"
    ],
    "address": [
      "Τ.Κ. 68100 Δίκελλα"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-018-dormition-of-the-theotokos-parish-church-in-apalos",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Dormition of the Theotokos Parish Church in Apalos",
    "local": "Ιερός Ναός Κοιμήσεως Θεοτόκου Απαλού",
    "seat": "Apalos",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post.html"
    ],
    "address": [
      "Τ.Κ. 68100 Απαλός"
    ],
    "phones": [
      "2551045087"
    ],
    "emails": [
      "enoriaapalou@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-019-saint-anastasia-pharmakolytria-parish-church-in-makri",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Anastasia Pharmakolytria Parish Church in Makri",
    "local": "Ιερός Ναός Αγίας Αναστασίας Φαρμακολυτρίας Μάκρης",
    "seat": "Makri",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_21.html"
    ],
    "address": [
      "Τ.Κ. 68100 Μάκρη"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-020-dormition-of-the-theotokos-parish-church-in-aisymi",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Dormition of the Theotokos Parish Church in Aisymi",
    "local": "Ιερός Ναός Κοιμήσεως Θεοτόκου Αισύμης",
    "seat": "Aisymi",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_19.html"
    ],
    "address": [
      "Αισύμη",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-021-saint-charalambos-parish-church-in-avantas",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Charalambos Parish Church in Avantas",
    "local": "Ιερός ΝαόςΑγίου Χαραλάμπους Άβαντα",
    "seat": "Avantas",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_13.html"
    ],
    "address": [
      "Άβαντας",
      "Τ.Κ. 68100"
    ],
    "phones": [
      "2551091409"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_13.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-022-saints-constantine-and-helen-parish-church-in-loutros-traianoupolis",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saints Constantine and Helen Parish Church in Loutros, Traianoupolis",
    "local": "Ιερός Ναός Αγίων Κωνσταντίνου και Ελένης Λουτρών Τραϊανουπόλεως",
    "seat": "Loutros, Traianoupolis",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/blog-post_29.html"
    ],
    "address": [
      "Λουτρός",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-023-nativity-of-the-theotokos-parish-church-in-antheia",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Nativity of the Theotokos Parish Church in Antheia",
    "local": "Ιερός Ναός Γενεσίου της Θεοτόκου Άνθειας",
    "seat": "Antheia",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/2.html"
    ],
    "address": [
      "Άνθεια",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-024-saint-barbara-parish-church-in-amfitriti",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Barbara Parish Church in Amfitriti",
    "local": "Ιερός Ναός Αγίας Βαρβάρας Αμφιτρίτης",
    "seat": "Amfitriti",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_28.html"
    ],
    "address": [
      "Αμφιτρίτη",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-025-holy-trinity-parish-church-in-doriko",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Holy Trinity Parish Church in Doriko",
    "local": "Ιερός Ναός Αγίας Τριάδος Δωρικού",
    "seat": "Doriko",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_90.html"
    ],
    "address": [
      "Δωρικό",
      "Τ.Κ. 68100"
    ],
    "phones": [
      "2551051348"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_90.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-026-saint-athanasius-parish-church-in-aristino",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Athanasius Parish Church in Aristino",
    "local": "Ιερός Ναός Αγίου Αθανασίου Αριστήνου",
    "seat": "Aristino",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_35.html"
    ],
    "address": [
      "Αρίστηνο",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-027-saint-george-parish-church-in-pefka",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Pefka",
    "local": "Ιερός Ναός Αγίου Γεωργίου Πεύκων",
    "seat": "Pefka",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_16.html"
    ],
    "address": [
      "Πεύκα",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-028-transfiguration-of-the-savior-parish-church-in-aetochori",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Transfiguration of the Savior Parish Church in Aetochori",
    "local": "Ιερός Ναός Μεταμορφώσεως Σωτήρος Αετοχωρίου",
    "seat": "Aetochori",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_78.html"
    ],
    "address": [
      "Τ.Κ. 68100 Αετοχώρι"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-029-saint-george-parish-church-in-agnantia",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Agnantia",
    "local": "Ιερός Ναός Αγίου Γεωργίου Αγνάντιας",
    "seat": "Agnantia",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_20.html"
    ],
    "address": [
      "Αγνάντια",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-030-panagia-kosmosoteira-parish-church-in-feres",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Panagia Kosmosoteira Parish Church in Feres",
    "local": "Ιερός Ναός Παναγίας Κοσμοσώτειρας Φερών",
    "seat": "Feres",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/3.html"
    ],
    "address": [
      "Τ.Κ. 68500 Φέρες"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-031-saint-nicholas-parish-church-in-feres",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Nicholas Parish Church in Feres",
    "local": "Ιερός Ναός Αγίου Νικολάου Φερών",
    "seat": "Feres",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1988/10/blog-post.html"
    ],
    "address": [
      "Φέρρες",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-032-saint-alexander-parish-church-in-feres",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Alexander Parish Church in Feres",
    "local": "Ιερός Ναός Αγίου Αλεξάνδρου Φερών",
    "seat": "Feres",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/blog-post_20.html"
    ],
    "address": [
      "Φέρρες",
      "Τ.Κ. 68500"
    ],
    "emails": [
      "inagioualexandrouf@gmail.com"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/blog-post_20.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-033-saint-athanasius-parish-church-in-pylaia",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Athanasius Parish Church in Pylaia",
    "local": "Ιερός Ναός Αγίου Αθανασίου Πυλαίας",
    "seat": "Pylaia",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_25.html"
    ],
    "address": [
      "Πυλαία",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-034-saint-demetrius-parish-church-in-doriskos",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Demetrius Parish Church in Doriskos",
    "local": "Ιερός Ναός Αγίου Δημητρίου Δορίσκου",
    "seat": "Doriskos",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_23.html"
    ],
    "address": [
      "Δορίσκος",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-035-dormition-of-the-theotokos-parish-church-in-monastiraki",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Dormition of the Theotokos Parish Church in Monastiraki",
    "local": "Ιερός Ναός Κοιμήσεως Θεοτόκου Μοναστηρακίου",
    "seat": "Monastiraki",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_47.html"
    ],
    "address": [
      "Μοναστηράκι",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-036-prophet-elijah-parish-church-in-melia",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Prophet Elijah Parish Church in Melia",
    "local": "Ιερός Ναός Προφήτη Ηλία Μελίας",
    "seat": "Melia",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_34.html"
    ],
    "address": [
      "Μελία",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-037-saint-george-parish-church-in-koila",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Koila",
    "local": "Ιερός Ναός Αγίου Γεωργίου Κοίλων",
    "seat": "Koila",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_3.html"
    ],
    "address": [
      "Κοίλα",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-038-exaltation-of-the-precious-cross-parish-church-in-kavysos",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Exaltation of the Precious Cross Parish Church in Kavysos",
    "local": "Ιερός Ναός Υψώσεως Τιμίου Σταυρού Καβησού",
    "seat": "Kavysos",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_84.html"
    ],
    "address": [
      "Καβησός",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-039-saint-athanasius-parish-church-in-itea",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Athanasius Parish Church in Itea",
    "local": "Ιερός Ναός Αγίου Αθανασίου Ιτέας",
    "seat": "Itea",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_14.html"
    ],
    "address": [
      "Ιτέα",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-040-holy-archangels-parish-church-in-gemisti",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Holy Archangels Parish Church in Gemisti",
    "local": "Ιερός Ναός Παμμεγίστων Ταξιαρχών Γεμιστής",
    "seat": "Gemisti",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_1.html"
    ],
    "address": [
      "Γεμιστή",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-041-saint-john-the-forerunner-parish-church-in-vrysoula",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint John the Forerunner Parish Church in Vrysoula",
    "local": "Ιερός Ναός Αγίου Ιωάννου Προδρόμου Βρυσούλας",
    "seat": "Vrysoula",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_30.html"
    ],
    "address": [
      "Βρυσούλα",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-042-holy-unmercenaries-parish-church-in-poros",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Holy Unmercenaries Parish Church in Poros",
    "local": "Ιερός Ναός Αγίων Αναργύρων Πόρου",
    "seat": "Poros",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_86.html"
    ],
    "address": [
      "Πόρος",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-043-saint-demetrius-parish-church-in-peplos",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Demetrius Parish Church in Peplos",
    "local": "Ιερός Ναός Αγίου Δημητρίου Πέπλου",
    "seat": "Peplos",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_42.html"
    ],
    "address": [
      "Πέπλος",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-044-saints-constantine-and-helen-parish-church-in-ardanio",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saints Constantine and Helen Parish Church in Ardanio",
    "local": "Ιερός Ναός Αγίου Κωνσταντίνου και Ελένης Αρδανίου",
    "seat": "Ardanio",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_27.html"
    ],
    "address": [
      "Αρδάνιο",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-045-saint-john-the-forerunner-parish-church-in-kipoi",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint John the Forerunner Parish Church in Kipoi",
    "local": "Ιερός Ναός Αγίου Ιωάννου Προδρόμου Κήπων",
    "seat": "Kipoi",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1970/01/blog-post.html"
    ],
    "address": [
      "Κήποι",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-046-saint-nectarius-parish-church-in-tycheri",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Nectarius Parish Church in Tycheri",
    "local": "Ιερός Ναός Αγίου Νεκταρίου Τυχερού",
    "seat": "Tycheri",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_8.html"
    ],
    "address": [
      "Τυχερό",
      "Τ.Κ. 68003"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-047-saint-john-the-forerunner-parish-church-in-tycheri",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint John the Forerunner Parish Church in Tycheri",
    "local": "Ιερός Ναός Αγίου Ιωάννου Προδρόμου Τυχερού",
    "seat": "Tycheri",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_99.html"
    ],
    "address": [
      "Τυχερό",
      "Τ.Κ. 68003"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-048-saint-paraskevi-parish-church-in-lagyna",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Paraskevi Parish Church in Lagyna",
    "local": "Ιερός Ναός Αγίας Παρασκευής Λαγηνών",
    "seat": "Lagyna",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_57.html"
    ],
    "address": [
      "Λαγηνά",
      "Τ.Κ. 68400"
    ],
    "phones": [
      "2551061023"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_57.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-049-saint-demetrius-parish-church-in-thymaria",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Demetrius Parish Church in Thymaria",
    "local": "Ιερός Ναός Αγίου Δημητρίου Θυμαριάς",
    "seat": "Thymaria",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_5.html"
    ],
    "address": [
      "Θυμαριά",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-050-nativity-of-the-theotokos-parish-church-in-nipsa",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Nativity of the Theotokos Parish Church in Nipsa",
    "local": "Ιερός Ναός Γεννέσιου Θεοτόκου Νίψας",
    "seat": "Nipsa",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_73.html"
    ],
    "address": [
      "Νίψα",
      "Τ.Κ. 68100"
    ],
    "phones": [
      "2551051503"
    ],
    "contact_sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_73.html"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-051-saint-demetrius-parish-church-in-lyra",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Demetrius Parish Church in Lyra",
    "local": "Ιερός Ναός Αγίου Δημητρίου Λύρας",
    "seat": "Lyra",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_87.html"
    ],
    "address": [
      "Λύρα",
      "Τ.Κ. 68100"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-052-dormition-of-the-theotokos-parish-church-in-lykofi",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Dormition of the Theotokos Parish Church in Lykofi",
    "local": "Ιερός Ναός Κοιμήσεως Θεοτόκου Λυκόφης",
    "seat": "Lykofi",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_18.html"
    ],
    "address": [
      "Λυκόφη",
      "Τ.Κ. 68400"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-053-saint-nicholas-parish-church-in-trifylli",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Nicholas Parish Church in Trifylli",
    "local": "Ιερός Ναός Αγίου Νικολάου Τριφύλλι",
    "seat": "Trifylli",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_29.html"
    ],
    "address": [
      "Τριφύλλι",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-054-saint-paraskevi-parish-church-in-provatonas",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Paraskevi Parish Church in Provatonas",
    "local": "Ιερός Ναός Αγίας Παρασκεύης Προβατώνα",
    "seat": "Provatonas",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_15.html"
    ],
    "address": [
      "Προβατώνας",
      "Τ.Κ. 68400"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-055-nativity-of-the-theotokos-parish-church-in-lefkimi",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Nativity of the Theotokos Parish Church in Lefkimi",
    "local": "Ιερός Ναός Γεννεσίου Θεοτόκου Λευκίμης",
    "seat": "Lefkimi",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/4.html"
    ],
    "address": [
      "Λευκίμη",
      "Τ.Κ. 68400"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-056-saint-nicholas-parish-church-in-fylakto",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Nicholas Parish Church in Fylakto",
    "local": "Ιερός Ναός Αγίου Νικολάου Φυλακτού",
    "seat": "Fylakto",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_74.html"
    ],
    "address": [
      "Φυλακτό",
      "Τ.Κ. 68400"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-057-saint-george-parish-church-in-tavri",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint George Parish Church in Tavri",
    "local": "Ιερός Ναός Αγίου Γεωργίου Ταύρης",
    "seat": "Tavri",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_89.html"
    ],
    "address": [
      "Ταύρη",
      "Τ.Κ. 68500"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-058-dormition-of-the-theotokos-parish-church-in-chora-samothrace",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Dormition of the Theotokos Parish Church in Chora, Samothrace",
    "local": "Ιερός Ναός Κοιμήσεως Θεοτόκου Χώρας Σαμοθράκης",
    "seat": "Chora, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/2015/10/5.html"
    ],
    "address": [
      "Χώρα Σαμοθράκης",
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-059-dormition-of-the-theotokos-parish-church-in-kamariotissa-samothrace",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Dormition of the Theotokos Parish Church in Kamariotissa, Samothrace",
    "local": "Ιερός Ναός Κοιμήσεως Θεοτόκου Καμαριώτισσας Σαμοθράκης",
    "seat": "Kamariotissa, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1979/01/blog-post_22.html"
    ],
    "address": [
      "Καμαριώτισσα Σαμοθράκης",
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-060-annunciation-of-the-theotokos-parish-church-in-xiropotamos-samothrace",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Annunciation of the Theotokos Parish Church in Xiropotamos, Samothrace",
    "local": "Ιερός Ναός Ευαγγελισμού Θεοτόκου Ξηροποτάμου Σαμοθράκης",
    "seat": "Xiropotamos, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_9.html"
    ],
    "address": [
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-061-saint-john-the-forerunner-parish-church-in-loutra-samothrace",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint John the Forerunner Parish Church in Loutra, Samothrace",
    "local": "Ιερός Ναός Αγίου Ιωάννου Προδρόμου Λουτρών Σαμοθράκης",
    "seat": "Loutra, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/10/blog-post_92.html"
    ],
    "address": [
      "Λουτρά Σαμοθράκης",
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-062-saint-modestus-parish-church-in-alonia-samothrace",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Saint Modestus Parish Church in Alonia, Samothrace",
    "local": "Ιερός Ναός Αγίου Μοδέστου Αλωνίων Σαμοθράκης",
    "seat": "Alonia, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1978/01/blog-post.html"
    ],
    "address": [
      "Αλώνια",
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-063-nativity-of-the-theotokos-parish-church-in-lakkoma-samothrace",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Nativity of the Theotokos Parish Church in Lakkoma, Samothrace",
    "local": "Ιερός Ναός Γενεσίου της Θεοτόκου Λακκώματος Σαμοθράκης",
    "seat": "Lakkoma, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1977/01/blog-post.html"
    ],
    "address": [
      "Λάκκωμα Σαμοθράκης",
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-064-entry-of-the-theotokos-into-the-temple-parish-church-in-profitis-ilias-s",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Parish Church",
    "name": "Entry of the Theotokos into the Temple Parish Church in Profitis Ilias, Samothrace",
    "local": "Ιερός Ναός Εισοδίων της Θεοτόκου Προφήτου Ηλία Σαμοθράκης",
    "seat": "Profitis Ilias, Samothrace",
    "country": "GR",
    "sources": [
      "https://imalexandroupolis.blogspot.com/1976/01/blog-post.html"
    ],
    "address": [
      "Προφήτης Ηλίας Σαμοθράκης",
      "Τ.Κ. 68002"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-shrine-glykeria-loutra",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Shrine",
    "name": "Saint Glykeria Shrine at Loutra, Traianoupolis",
    "local": "Ἱερόν Προσκύνημα Ἁγίας Γλυκερίας, Λουτρά Τραϊανουπόλεως",
    "seat": "Loutra, Traianoupolis",
    "country": "GR",
    "sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-shrine-cyprian-national-road",
    "parent": "ep-alexandroupolis",
    "kind": "parish",
    "rank": "Shrine",
    "name": "Saint Cyprian Shrine on the Alexandroupolis to Komotini National Road",
    "local": "Ἱερόν Προσκύνημα Ἁγίου Κυπριανοῦ, 9ο χιλιομ. Ἐθνικῆς ὁδοῦ Ἀλεξανδρουπόλεως - Κομοτηνῆς",
    "seat": "Alexandroupolis",
    "country": "GR",
    "sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-monastery-john-theologian-aetochori",
    "parent": "ep-alexandroupolis",
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Monastery of Saint John the Theologian in Aetochori",
    "local": "Ἱερά Μονή Ἁγίου Ἰωάννου Θεολόγου Ἀετοχωρίου Ἀλεξανδρουπόλεως",
    "seat": "Aetochori",
    "country": "GR",
    "sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ]
  },
  {
    "id": "gr-ep-alexandroupolis-monastery-athanasius-alonia",
    "parent": "ep-alexandroupolis",
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Monastery of Saint Athanasius in Alonia, Samothrace",
    "local": "Ἱερά Μονή Ἁγίου Ἀθανασίου Ἁλωνίων Σαμοθράκης",
    "seat": "Alonia, Samothrace",
    "country": "GR",
    "sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ],
    "phones": [
      "+30-25510-41952"
    ],
    "emails": [
      "metsamo@yahoo.gr"
    ],
    "contact_sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ],
    "contact_checked": "2026-11-15"
  },
  {
    "id": "gr-ep-alexandroupolis-monastery-panagia-evrou-makri",
    "parent": "ep-alexandroupolis",
    "kind": "monastery",
    "rank": "Monastery",
    "name": "Panagia of Evros Monastery of the Dormition of the Theotokos in Makri",
    "local": "Ἱερά Μονή Κοιμήσεως τῆς Θεοτόκου «Ἡ Παναγία τοῦ Ἕβρου», Μάκρη Ἀλεξανδρουπόλεως",
    "seat": "Makri",
    "country": "GR",
    "sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ],
    "phones": [
      "+30-25510-71263"
    ],
    "contact_sources": [
      "https://ec-patr.org/entities/iera-mitropoli-aleksandroypoleos/"
    ],
    "contact_checked": "2026-11-15"
  }
]''')

PHONE_BY_SOURCE = json.loads(r'''{
  "https://imalexandroupolis.blogspot.com/1970/01/blog-post.html": [
    "25550-31120"
  ],
  "https://imalexandroupolis.blogspot.com/1970/10/blog-post_21.html": [
    "25510-26601"
  ],
  "https://imalexandroupolis.blogspot.com/1977/01/blog-post.html": [
    "25510-95390"
  ],
  "https://imalexandroupolis.blogspot.com/1978/01/blog-post.html": [
    "25510-41266"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post.html": [
    "2551045087"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_13.html": [
    "2551091409"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_15.html": [
    "25550-42264"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_21.html": [
    "25510-71717"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_22.html": [
    "2551096364"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_27.html": [
    "2551024530"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_35.html": [
    "2551051550"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_57.html": [
    "2551061023"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_73.html": [
    "2551051503"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_8.html": [
    "25550-41851"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_90.html": [
    "2551051348"
  ],
  "https://imalexandroupolis.blogspot.com/1978/10/blog-post_99.html": [
    "25550-41570"
  ],
  "https://imalexandroupolis.blogspot.com/1979/01/blog-post_22.html": [
    "25510-41880"
  ],
  "https://imalexandroupolis.blogspot.com/1979/10/blog-post.html": [
    "25510-36910"
  ],
  "https://imalexandroupolis.blogspot.com/1980/10/blog-post.html": [
    "25510-26073"
  ],
  "https://imalexandroupolis.blogspot.com/1981/10/blog-post.html": [
    "25510-39743"
  ],
  "https://imalexandroupolis.blogspot.com/1983/10/blog-post.html": [
    "25510-33711"
  ],
  "https://imalexandroupolis.blogspot.com/1983/10/blog-post_21.html": [
    "25510-22217"
  ],
  "https://imalexandroupolis.blogspot.com/1984/10/blog-post.html": [
    "25510-81280"
  ],
  "https://imalexandroupolis.blogspot.com/1985/10/blog-post.html": [
    "25510-33053"
  ],
  "https://imalexandroupolis.blogspot.com/1986/10/blog-post.html": [
    "25510-23686"
  ],
  "https://imalexandroupolis.blogspot.com/1987/10/blog-post.html": [
    "25510-25644"
  ],
  "https://imalexandroupolis.blogspot.com/1988/10/blog-post.html": [
    "25550-22428"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/1_80.html": [
    "25510-26693"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/2.html": [
    "25510-51104"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/3.html": [
    "25550-22227"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/5.html": [
    "25510-41373"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/blog-post_20.html": [
    "25550-24004"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/blog-post_21.html": [
    "25510-28819"
  ],
  "https://imalexandroupolis.blogspot.com/2015/10/blog-post_29.html": [
    "25510-61121"
  ]
}''')
for _row in ROWS:
    _source = (_row.get("sources") or [None])[0]
    if _source in PHONE_BY_SOURCE:
        _row["phones"] = list(PHONE_BY_SOURCE[_source])
        _row["contact_sources"] = [_source]
        _row["contact_checked"] = CHECKED
    if _source == "https://imalexandroupolis.blogspot.com/1978/01/blog-post.html":
        _phone_source = "https://www.xo.gr/profile/profile-911336870/el/"
        _row["sources"].append(_phone_source)
        _row["contact_sources"].append(_phone_source)

ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 69
EXPECTED_OWNER_COUNTS = {"ep-alexandroupolis": 69}
EXPECTED_KINDS = {
    "monastery": 3,
    "parish": 66,
}
EXPECTED_RANKS = {
  "Cathedral": 1,
  "Chapel": 1,
  "Church": 1,
  "Monastery": 3,
  "Parish Church": 59,
  "Shrine": 4
}
EXPECTED_CONTACT_BODIES = 36
EXPECTED_PHONE_BODIES = 36
EXPECTED_PHONE_VALUES = 36
EXPECTED_EMAIL_BODIES = 10
EXPECTED_EMAIL_VALUES = 10
EXPECTED_SITE_BODIES = 1
EXPECTED_ADDRESS_BODIES = 64
EXISTING_PARENTS = set(EXPECTED_OWNER_COUNTS)
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
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("%s has an invalid URL: %s" % (label, value))
    if parsed.netloc not in {
            "ec-patr.org", "imalex.gr",
            "imalexandroupolis.blogspot.com",
            "nektariosimalex.blogspot.com", "www.xo.gr"}:
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
                raise ValueError(
                    "%s contact source is outside identity sources"
                    % item.get("id")
                )
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date"
                             % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
        if item["site"] not in sources:
            raise ValueError("%s body-owned site lacks provenance"
                             % item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Alexandroupolis candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Alexandroupolis candidate ledger date drifted")
    expected_summary = {
  "ep-alexandroupolis": 69,
  "total": 69,
  "parish_kind_rows": 66,
  "monastery_kind_rows": 3,
  "contact_bodies": 36,
  "phone_bodies": 36,
  "public_phone_values": 36,
  "email_bodies": 10,
  "public_email_values": 10,
  "body_owned_sites": 1,
  "address_bodies": 64
}
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Alexandroupolis ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Alexandroupolis ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Alexandroupolis ledger item has invalid sources"
                )
            for source_url in sources:
                validate_url(
                    source_url, entry.get("candidate_id") or key
                )
    candidate_ids = [
        entry.get("candidate_id") for entry in ledger["candidates"]
    ]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Alexandroupolis ledger has invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Alexandroupolis ledger has duplicate candidate ids")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError(
            "Alexandroupolis candidate ledger has forbidden punctuation"
        )
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
        if not any("\u0370" <= char <= "\u03ff"
                   for char in item["local"]):
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
        raise ValueError("Alexandroupolis English name coverage drifted")
    expected_seats = {
        item["seat"] for item in result if item.get("seat")
    }
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Alexandroupolis English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Alexandroupolis parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Alexandroupolis kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Alexandroupolis rank totals drifted")
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
        raise ValueError("Alexandroupolis contact coverage drifted: %r"
                         % (coverage,))
    validate_ledger()
    return {
        "ep-alexandroupolis": {
            "v": 1,
            "parent": "ep-alexandroupolis",
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
            "Alexandroupolis: %d exact named bodies; %d carry current "
            "institutional contact data" %
            (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES)
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Alexandroupolis: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
