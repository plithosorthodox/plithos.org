#!/usr/bin/env python3
"""Validate exact named Peristerion Metropolis worship bodies.

This module stays independent of the shared directory aggregator until its
regional tranche is integrated.

    python tools/directory_peristerion_country.py --check
    python tools/directory_peristerion_country.py --check-live
    python tools/directory_peristerion_country.py --dump
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree


CHECKED = "2026-11-15"
PARENT = "gr-peristerion"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "peristerion_country.json"
)

SITEMAP = "https://imperisteriou.gr/church-sitemap.xml"
ARCHIVE_ROOT = "https://imperisteriou.gr/church/"
OFFICIAL_PDF = (
    "https://ecclesiagreece.gr/greek/press/ekklisia/2019_noembrios.pdf"
)
CHURCH_OF_GREECE_PAGE = (
    "https://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/"
    "metropoleis/peristeriou"
)
GREGORY_FOUNDATION = (
    "https://imperisteriou.gr/%cf%84%ce%bf%cf%80%ce%bf%ce%b8%ce%ad%cf%84%ce%b7%cf%83%ce%b7-"
    "%ce%b8%ce%b5%ce%bc%ce%ad%ce%bb%ce%b9%ce%bf%cf%85-%ce%bb%ce%af%ce%b8%ce%bf%cf%85-"
    "%ce%b3%ce%b9%ce%b1-%cf%84%ce%b7-%ce%bc%ce%bf%ce%bd%ce%ae/"
)

BODY_SITES = {
    "ANNUNCIATION": "https://evaggelistriaperisteri.blogspot.com/",
    "OLD_ARCHANGELS": "https://www.ptaxiarchisper.com/",
    "PAUL": "https://www.inagioupavlou.gr/",
    "HIEROTHEOS": "https://agiosierotheosperisteri.gr/",
}


# These are the 34 exact body pages in the official sitemap, in sitemap order.
# The archive root is intentionally excluded from this tuple.
SITEMAP_PAGE_TEXT = r'''
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b9%cf%89%ce%b1%ce%bd%ce%bd%ce%bf%cf%85-%cf%84%ce%bf%cf%85-%ce%b8%ce%b5%ce%bf%ce%bb%ce%bf%ce%b3%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b9%cf%89%ce%b1%ce%bd%ce%bd%ce%bf%cf%85-%cf%84%ce%bf%cf%85-%cf%87%cf%81%cf%85%cf%83%ce%bf%cf%83%cf%84%ce%bf/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%84%ce%b9%ce%bc%ce%b9%ce%bf%cf%85-%cf%80%cf%81%ce%bf%ce%b4%cf%81%ce%bf%ce%bc%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%83%cf%84%cf%85%ce%bb%ce%b9%ce%b1%ce%bd%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b3%ce%b5%cf%89%cf%81%ce%b3%ce%b9%ce%bf%cf%85-%ce%ba%ce%b7%cf%80%ce%bf%cf%85%cf%80%ce%bf%ce%bb%ce%b5%cf%89/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%ba%cf%85%cf%80%cf%81%ce%b9%ce%b1%ce%bd%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%ce%b1%ce%bd%ce%bd%ce%b7%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%80%ce%b1%ce%bd%cf%84%ce%b5%ce%bb%ce%b5%ce%b7%ce%bc%ce%bf%ce%bd%ce%bf%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%cf%8c%cf%82-%ce%bd%ce%b1%cf%8c%cf%82-%ce%b1%ce%b3%ce%af%cf%89%ce%bd-%ce%ba%cf%89%ce%bd%cf%83%cf%84%ce%b1%ce%bd%cf%84%ce%af%ce%bd%ce%bf%cf%85-%ce%ba%ce%b1%ce%b9-%ce%b5%ce%bb%ce%ad/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%ce%b1%ce%bd%ce%b1%cf%83%cf%84%ce%b1%cf%83%ce%b9%ce%b1%cf%83-%cf%84%ce%b7%cf%83-%cf%80%ce%b1%cf%84%cf%81%ce%b9/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%80%ce%b1%cf%85%ce%bb%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%cf%80%ce%b1%cf%81%ce%b1%cf%83%ce%ba%ce%b5%cf%85%ce%b7%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%cf%84%cf%81%ce%b9%ce%b1%ce%b4%ce%bf%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%80%ce%b1%ce%bc%ce%bc%ce%b5%ce%b3%ce%b9%cf%83%cf%84%cf%89%ce%bd-%cf%84%ce%b1%ce%be%ce%b9%ce%b1%cf%81%cf%87%cf%89%ce%bd-%cf%80%ce%b1%ce%bb/
https://imperisteriou.gr/church/%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%cf%89%ce%bd-%cf%81%ce%b1%cf%86%ce%b1%ce%b7%ce%bb-%ce%bd%ce%b9%ce%ba%ce%bf%ce%bb%ce%b1%ce%bf%cf%85-%ce%b5%ce%b9%cf%81%ce%b7%ce%bd/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%cf%89%ce%bd-%ce%b1%ce%bd%ce%b1%cf%81%ce%b3%cf%85%cf%81%cf%89%ce%bd/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%80%ce%b1%ce%bd%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%ce%b1%ce%be%ce%b9%ce%bf%ce%bd-%ce%b5%cf%83%cf%84%ce%b9/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%ac-%ce%bc%ce%bf%ce%bd%ce%ae-%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%ce%b3%cf%81%ce%b7%ce%b3%ce%bf%cf%81%ce%af%ce%bf%cf%85-%ce%b8%ce%b5%ce%bf%ce%bb%cf%8c%ce%b3%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%ba%ce%bf%ce%b9%ce%bc%ce%b7%cf%84%ce%b7%cf%81%ce%b9%ce%b1%ce%ba%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%bb%ce%b1%ce%b6%ce%b1%cf%81%ce%bf%cf%85/
https://imperisteriou.gr/church/naos-1/
https://imperisteriou.gr/church/%ce%ba%ce%b1%ce%b8%ce%b5%ce%b4%cf%81%ce%b9%ce%ba%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%80%ce%b1%ce%bc%ce%bc%ce%b5%ce%b3%ce%b9%cf%83%cf%84%cf%89%ce%bd-%cf%84%ce%b1%ce%be%ce%b9%ce%b1%cf%81%cf%87/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%cf%89%ce%bd-%ce%b8%ce%b5%ce%bf%ce%b4%cf%89%cf%81%cf%89%ce%bd/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b1%ce%b8%ce%b1%ce%bd%ce%b1%cf%83%ce%b9%ce%bf%cf%85-%ce%bf%cf%83%ce%b9%ce%b1%cf%83-%ce%b5%cf%85%ce%b3%ce%b5/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b9%ce%b5%cf%81%ce%bf%ce%b8%ce%b5%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%ce%bc%ce%b1%cf%81%ce%b9%ce%bd%ce%b7%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%bd%ce%b9%ce%ba%ce%bf%ce%bb%ce%b1%ce%bf%cf%85-%cf%87%cf%89%cf%83%cf%84%ce%bf%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%bd%ce%b5%ce%ba%cf%84%ce%b1%cf%81%ce%b9%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%cf%86%ce%b1%ce%bd%ce%bf%cf%85%cf%81%ce%b9%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b3%ce%b5%cf%89%cf%81%ce%b3%ce%b9%ce%bf%cf%85-%ce%bd%ce%b5%ce%b1%cf%83-%ce%b6%cf%89%ce%b7%cf%83/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%ce%b1%ce%b3%ce%b9%ce%bf%cf%85-%ce%b5%ce%bb%ce%b5%cf%85%ce%b8%ce%b5%cf%81%ce%b9%ce%bf%cf%85/
https://imperisteriou.gr/church/%cf%85%cf%88%cf%89%cf%83%ce%b9%cf%83-%cf%84%ce%b9%ce%bc%ce%b9%ce%bf%cf%85-%cf%83%cf%84%ce%b1%cf%85%cf%81%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%bf%cf%83-%ce%bd%ce%b1%ce%bf%cf%83-%cf%85%cf%80%ce%b1%cf%80%ce%b1%ce%bd%cf%84%ce%b7%cf%83-%cf%84%ce%bf%cf%85-%ce%ba%cf%85%cf%81%ce%b9%ce%bf%cf%85/
https://imperisteriou.gr/church/%ce%b9%ce%b5%cf%81%ce%b1-%ce%bc%ce%bf%ce%bd%ce%b7-%cf%80%ce%b1%ce%bd%ce%b1%ce%b3%ce%b9%ce%b1%cf%83-%cf%86%ce%bf%ce%b9%ce%bd%ce%b9%ce%ba%ce%b9%cf%89%cf%84%ce%b9%cf%83%cf%83%ce%b1%cf%83/
https://imperisteriou.gr/church/naos-2/
'''
PAGE_URLS = tuple(SITEMAP_PAGE_TEXT.strip().splitlines())


# page|key|kind|rank|English name|Greek local name|English seat|Greek address|
# phones|emails|site token|legal roster|markers
ROW_SOURCE = r'''
1|john-theologian|parish|Parish Church|Saint John the Theologian Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΤΟΥ ΘΕΟΛΟΓΟΥ|Peristeri|Αγ. Ιωάννου Θεολόγου & Λευκωσίας, 12133, Περιστέρι|2105712789|agioannistheologos@imperisteriou.gr||1|ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΤΟΥ ΘΕΟΛΟΓΟΥ
2|john-chrysostom-episcopal|parish|Metropolitan Chapel|Saint John Chrysostom Metropolitan Chapel at the episcopal residence, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΙΩΑΝΝΟΥ ΤΟΥ ΧΡΥΣΟΣΤΟΜΟΥ (ΕΠΙΣΚΟΠΕΙΟ)|Peristeri|Χαλκοκονδύλη 29 & Εθν. Αντιστάσεως, 12135 Περιστέρι||||0|ΙΩΑΝΝΟΥ ΤΟΥ ΧΡΥΣΟΣΤΟΜΟΥ;ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
3|john-forerunner|parish|Church|Saint John the Forerunner Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ|Nea Sepolia, Peristeri|Κωνσταντινουπόλεως & Σολωμού, Ν. Σεπόλια, Περιστέρι||||0|ΝΑΟΣ ΤΙΜΙΟΥ ΠΡΟΔΡΟΜΟΥ;Εξυπηρετείται απο
4|stylianos|parish|Parish Chapel|Saint Stylianos Parish Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΣΤΥΛΙΑΝΟΥ|Chryssoupoli, Peristeri|Κριεζώτου 34, 12137, Χρυσούπολις, Περιστέρι||||0|ΝΑΟΣ ΑΓΙΟΥ ΣΤΥΛΙΑΝΟΥ;ΕΝΟΡΙΑΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
5|george-kipoupoli|parish|Metropolitan Chapel|Saint George Metropolitan Chapel, Kipoupoli|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ (ΚΗΠΟΥΠΟΛΕΩΣ)|Kipoupoli, Peristeri|Πλ. Αγ. Γεωργίου, 12137 Κηπούπολις, Περιστέρι|2105016110|ag.georgekp@gmail.com||0|ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ (ΚΗΠΟΥΠΟΛΕΩΣ);ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
6|cyprian-justina|parish|Metropolitan Pilgrimage Chapel|Saints Cyprian and Justina Metropolitan Pilgrimage Chapel, Kipoupoli|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΚΥΠΡΙΑΝΟΥ|Kipoupoli, Peristeri|Κήπων & Ρόδων, 12137 Κηπούπολις, Περιστέρι|2105015729|agios.kyprianos.peristeri@gmail.com||0|ΝΑΟΣ ΑΓΙΟΥ ΚΥΠΡΙΑΝΟΥ;Ιερό Προσκύνημα των Αγίων Κυπριανού και Ιουστίνης
7|anna|parish|Parish Church|Saint Anna Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΑΝΝΗΣ|Peristeri|Σαλώνων & Αγίου Πολυκάρπου, 12136, Περιστέρι|2105711390|aganna@imperisteriou.gr||0|ΝΑΟΣ ΑΓΙΑΣ ΑΝΝΗΣ;ανυψώθηκε σε ενορία
8|panteleimon|parish|Parish Chapel|Saint Panteleimon Parish Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΠΑΝΤΕΛΕΗΜΟΝΟΣ|Lofos Axiomatikon, Peristeri|Καρύστου & Ανακρέοντος, Άνω Λόφος Αξιωματικών, Περιστέρι|2105810588|agpant@imperisteriou.gr||0|ΝΑΟΣ ΑΓΙΟΥ ΠΑΝΤΕΛΕΗΜΟΝΟΣ;Ενοριακό Παρεκκλήσιο
9|constantine-helen|parish|Parish Church|Saints Constantine and Helen Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ|Chorafa, Peristeri|Οδός Πεύκων, 12137, Χωράφα, Περιστέρι|2105010312|||1|ΑΓΙΩΝ ΚΩΝΣΤΑΝΤΙΝΟΥ ΚΑΙ ΕΛΕΝΗΣ
10|anastasia-patrician|parish|Parish Church|Saint Anastasia the Patrician Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΑΝΑΣΤΑΣΙΑΣ ΤΗΣ ΠΑΤΡΙΚΙΑΣ|Peristeri|Αγ. Αναστασίας & Μαυρογένους, 12136, Περιστέρι|2105719239,2105777060|aganastasia@imperisteriou.gr||1|ΑΓΙΑΣ ΑΝΑΣΤΑΣΙΑΣ ΤΗΣ ΠΑΤΡΙΚΙΑΣ
11|apostle-paul|parish|Parish Church|Apostle Paul Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΠΑΥΛΟΥ|Nea Sepolia, Peristeri|Κωνσταντινουπόλεως & Ζακύνθου 2, 12133 Περιστέρι|2105716449|agpaulos@imperisteriou.gr|PAUL|1|ΝΑΟΣ ΑΓΙΟΥ ΠΑΥΛΟΥ
12|paraskevi|parish|Metropolitan Chapel|Saint Paraskevi Metropolitan Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ|Nea Sepolia, Peristeri|Αγίας Παρασκευής & Λάδωνος 15, 12132, Ν. Σεπόλια, Περιστέρι|2105774641|pspiridonvou6@gmail.com||0|ΝΑΟΣ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ;ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙ
13|holy-trinity|parish|Parish Church|Holy Trinity Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ|Peristeri|Ναούσης 111 & Αλκίμου, 12137, Περιστέρι|2105740700|agtriada@imperisteriou.gr||1|ΝΑΟΣ ΑΓΙΑΣ ΤΡΙΑΔΟΣ
14|old-archangels|parish|Parish Church|Holy Archangels Parish Church, Peristeri (Old)|ΙΕΡΟΣ ΝΑΟΣ ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ (ΠΑΛΑΙΟΣ)|Peristeri|Σοφοκλή Βενιζέλου 47, 12131 Περιστέρι|2105712325|palaiostaxiarxis@imperisteriou.gr|OLD_ARCHANGELS|1|ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ (ΠΑΛΑΙΟΣ)
15|raphael-nicholas-irene|parish|Parish Chapel|Saints Raphael, Nicholas and Irene Parish Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΡΑΦΑΗΛ ΝΙΚΟΛΑΟΥ & ΕΙΡΗΝΗΣ|Nea Sepolia, Peristeri|Χαλκίδος 26, Ν. Σεπόλια, 2133, Περιστέρι|2105745412|||0|ΑΓΙΩΝ ΡΑΦΑΗΛ ΝΙΚΟΛΑΟΥ;ΕΝΟΡΙΑΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
16|unmercenaries|parish|Metropolitan Chapel|Holy Unmercenaries Metropolitan Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ|Peristeri|Ζαλοκώστα 24, 12132 Περιστέρι|2105723424|dorotheosgr@yahoo.gr||0|ΝΑΟΣ ΑΓΙΩΝ ΑΝΑΡΓΥΡΩΝ;ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
17|axion-estin|parish|Parish Chapel|Axion Estin Theotokos Parish Chapel, Egaleo|ΙΕΡΟΣ ΝΑΟΣ ΠΑΝΑΓΙΑΣ ΑΞΙΟΝ ΕΣΤΙ|Egaleo|Δάβακη 7, 12242, Αιγάλεω|2105312145|axionestiperisteri@gmail.com||0|ΠΑΝΑΓΙΑΣ ΑΞΙΟΝ ΕΣΤΙ;ΕΝΟΡΙΑΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
18|gregory-theologian-monastery|monastery|Monastery|Saint Gregory the Theologian Monastery, Kipoupoli|Ιερά Μονή Αγίου Γρηγορίου Θεολόγου|Kipoupoli, Peristeri|||||0|Μονή Αγίου Γρηγορίου Θεολόγου
19|lazarus-cemetery|parish|Cemetery Church|Saint Lazarus Cemetery Church, Peristeri|ΚΟΙΜΗΤΗΡΙΑΚΟΣ ΝΑΟΣ ΑΓΙΟΥ ΛΑΖΑΡΟΥ|Peristeri|Αναπαύσεως, 12135, Περιστέρι|2105739306,2105712098|aglazaros@imperisteriou.gr||0|ΚΟΙΜΗΤΗΡΙΑΚΟΣ ΝΑΟΣ ΑΓΙΟΥ ΛΑΖΑΡΟΥ
20|annunciation|parish|Metropolitan Church|Annunciation of the Theotokos Metropolitan Church, Peristeri|ΜΗΤΡΟΠΟΛΙΤΙΚΟΣ ΝΑΟΣ ΕΥΑΓΓΕΛΙΣΤΡΙΑΣ|Peristeri|Παναγή Τσαλδάρη 53-55, Πλατεία Δημαρχείου, 12134 Περιστέρι|2105711633|evaggelistria@imperisteriou.gr|ANNUNCIATION|1|ΜΗΤΡΟΠΟΛΙΤΙΚΟΣ ΝΑΟΣ ΕΥΑΓΓΕΛΙΣΤΡΙΑΣ
21|archangels-cathedral|parish|Cathedral|Holy Archangels Cathedral, Peristeri|ΚΑΘΕΔΡΙΚΟΣ ΝΑΟΣ ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ|Peristeri|Β. Αλεξάνδρου & Μεσολογγίου, 12134 Περιστέρι|2105719226|kathedrikos@imperisteriou.gr||1|ΚΑΘΕΔΡΙΚΟΣ ΝΑΟΣ ΠΑΜΜΕΓΙΣΤΩΝ ΤΑΞΙΑΡΧΩΝ
22|holy-theodores|parish|Metropolitan Chapel|Holy Theodore Martyrs Metropolitan Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΩΝ ΘΕΟΔΩΡΩΝ|Peristeri|Κρυστάλη 47 & Προκοπίου, 12131 Περιστέρι|2105712325|i.n.ag.theodoron.ap.andrea@gmail.com||0|ΝΑΟΣ ΑΓΙΩΝ ΘΕΟΔΩΡΩΝ;ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
23|athanasius-eugenia|parish|Parish Church|Saint Athanasius and Venerable Eugenia Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ - ΟΣΙΑΣ ΕΥΓΕΝΙΑΣ|Peristeri|Φλωρίνης 14, 12133 Περιστέρι|2105713093|agathanasios@imperisteriou.gr||0|ΑΓΙΟΥ ΑΘΑΝΑΣΙΟΥ;ΟΣΙΑΣ ΕΥΓΕΝΙΑΣ;νεότερη ενορία
24|hierotheos|parish|Parish Church|Saint Hierotheos Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΙΕΡΟΘΕΟΥ|Peristeri|Κυκλαμίνων 2 & Σικάγου, 12137 Περιστέρι|2105719200,2105785556|agierotheos@imperisteriou.gr,in.ierotheou.peristeri@gmail.com|HIEROTHEOS|1|ΝΑΟΣ ΑΓΙΟΥ ΙΕΡΟΘΕΟΥ
25|marina|parish|Parish Church|Saint Marina Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΑΣ ΜΑΡΙΝΗΣ|Anthoupoli, Peristeri|Πλ. Αγ. Μαρίνης, 12135 Ανθούπολη, Περιστέρι|2105777508,2105777765|agmarina@imperisteriou.gr||1|ΝΑΟΣ ΑΓΙΑΣ ΜΑΡΙΝΗΣ
26|nicholas-chostos|parish|Metropolitan Chapel|Saint Nicholas Chostos Metropolitan Chapel, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ (ΧΩΣΤΟΣ)|Peristeri|Λεωφόρος Κηφισού 38, 10442 Περιστέρι|2105149028|||0|ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ (ΧΩΣΤΟΣ);ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
27|nectarios|parish|Parish Church|Saint Nectarios Parish Church, Kipoupoli|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΝΕΚΤΑΡΙΟΥ|Kipoupoli, Peristeri|Μακρυγιάννη 145, 13231 Κηπούπολις, Περιστέρι|2105026229|ag.nektariosper@gmail.com||1|ΝΑΟΣ ΑΓΙΟΥ ΝΕΚΤΑΡΙΟΥ
28|phanourios|parish|Metropolitan Chapel|Saint Phanourios Metropolitan Chapel, Anthoupoli|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΦΑΝΟΥΡΙΟΥ|Anthoupoli, Peristeri|Αντ. Τρίτση 6, 12135 Ανθούπολη, Περιστέρι|2105759970|ag.phanourios.per@gmail.com||0|ΝΑΟΣ ΑΓΙΟΥ ΦΑΝΟΥΡΙΟΥ;ΜΗΤΡΟΠΟΛΙΤΙΚΟ ΠΑΡΕΚΚΛΗΣΙΟ
29|george-nea-zoi|parish|Parish Church|Saint George Parish Church, Nea Zoi|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ (ΝΕΑΣ ΖΩΗΣ)|Nea Zoi, Peristeri|Πελοπίδα 205 & Πεισιστράτου 24, 12137, Ν. Ζωή, Περιστέρι|2105713578|ag.georgiou.peristeri@gmail.com||1|ΑΓΙΟΥ ΓΕΩΡΓΙΟΥ (ΝΕΑΣ ΖΩΗΣ)
30|eleftherios|parish|Parish Church|Saint Eleftherios Parish Church, Nea Zoi|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΕΛΕΥΘΕΡΙΟΥ|Nea Zoi, Peristeri|Αγ. Ελευθερίου & Κοσμά Αιτωλού, 12137, Ν. Ζωή, Περιστέρι|2105715477|ageleftherios@imperisteriou.gr||1|ΝΑΟΣ ΑΓΙΟΥ ΕΛΕΥΘΕΡΙΟΥ
31|exaltation-cross|parish|Parish Church|Exaltation of the Holy Cross Parish Church, Peristeri|ΥΨΩΣΙΣ ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ|Peristeri|Αγ. Βασιλείου και Ηφαίστου 1, 12135 Περιστέρι|2105722850|tstauros@imperisteriou.gr||0|ΥΨΩΣΙΣ ΤΙΜΙΟΥ ΣΤΑΥΡΟΥ
32|meeting-lord|parish|Parish Church|Meeting of the Lord Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΥΠΑΠΑΝΤΗΣ ΤΟΥ ΚΥΡΙΟΥ|Lofos Axiomatikon, Peristeri|Μεσσηνίας & Ελπίδος, 12132, Λόφος Αξιωματικών, Περιστέρι|2105726041|ipapanti@imperisteriou.gr||0|ΥΠΑΠΑΝΤΗΣ ΤΟΥ ΚΥΡΙΟΥ;ανυψώθηκε σε ενορία
33|phoinikiotissa-monastery|monastery|Monastery|Panagia Phoinikiotissa Monastery, Peristeri|ΙΕΡΑ ΜΟΝΗ ΠΑΝΑΓΙΑΣ ΦΟΙΝΙΚΙΩΤΙΣΣΑΣ|Peristeri|Διασταύρωσις Τεμπών & Μιλήτου, Περιστέρι|2105769333,2105382356|i.moni.panagias.foinik@gmail.com||0|ΜΟΝΗ ΠΑΝΑΓΙΑΣ ΦΟΙΝΙΚΙΩΤΙΣΣΑΣ
34|anthony|parish|Parish Church|Saint Anthony Parish Church, Peristeri|ΙΕΡΟΣ ΝΑΟΣ ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ (ΠΟΛΙΟΥΧΟΣ)|Peristeri|Εθν. Μακαρίου & Κουντουριώτου 2, 12132 Περιστέρι|2105712705,2105712605|agantonios@imperisteriou.gr||1|ΑΓΙΟΥ ΑΝΤΩΝΙΟΥ (ΠΟΛΙΟΥΧΟΣ)
'''


# page|key|English name|Greek local name|English seat|Greek address|markers
EMBEDDED_SOURCE = r'''
1|parthenius-chapel|Saint Parthenius Parish Chapel at Saint John the Theologian Parish, Peristeri|Παρεκκλήσιο Αγίου Παρθενίου Ιερού Ναού Αγίου Ιωάννου του Θεολόγου|Peristeri|Αγ. Ιωάννου Θεολόγου & Λευκωσίας, 12133, Περιστέρι|παρεκκλήσιο του Αγίου Παρθενίου
14|patapios-chapel|Venerable Patapios Parish Chapel at the Old Holy Archangels Parish, Peristeri|Παρεκκλήσιο Οσίου Παταπίου Ιερού Ναού Παμμεγίστων Ταξιαρχών (Παλαιού)|Peristeri|Σοφοκλή Βενιζέλου 47, 12131 Περιστέρι|λειτουργεί παρεκκλήσιο του Οσίου Παταπίου
11|menas-chapel|Great Martyr Menas Parish Chapel at Apostle Paul Parish, Peristeri|Παρεκκλήσιο Αγίου Μεγαλομάρτυρος Μηνά Ιερού Ναού Αγίου Παύλου|Nea Sepolia, Peristeri|Κωνσταντινουπόλεως & Ζακύνθου 2, 12133 Περιστέρι|υπογείου παρεκκλησίου;Αγίου Μεγαλομάρτυρος Μηνά
30|unmercenaries-chapel|Holy Unmercenaries Parish Chapel at Saint Eleftherios Parish, Peristeri|Παρεκκλήσιο Αγίων Αναργύρων Ιερού Ναού Αγίου Ελευθερίου|Nea Zoi, Peristeri|Αγ. Ελευθερίου & Κοσμά Αιτωλού, 12137, Ν. Ζωή, Περιστέρι|λειτουργεί παρεκκλήσιο των Αγίων Αναργύρων
'''


def split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def split_markers(value):
    return [item.strip() for item in value.split(";") if item.strip()]


def unicase(value):
    value = unicodedata.normalize("NFD", value).casefold()
    return "".join(
        char for char in value if unicodedata.category(char) != "Mn"
    )


def build_rows():
    rows = []
    lines = ROW_SOURCE.strip().splitlines()
    if len(PAGE_URLS) != 34 or len(lines) != 34:
        raise ValueError("expected 34 current Peristerion body pages")
    seen_pages = set()
    for number, raw in enumerate(lines, 1):
        (page_number, key, kind, rank, name, local, seat, address, phones,
         emails, site_token, legal, markers) = raw.split("|", 12)
        page_index = int(page_number)
        page_url = PAGE_URLS[page_index - 1]
        if page_index != number or page_url in seen_pages:
            raise ValueError("Peristerion sitemap row order drifted")
        seen_pages.add(page_url)
        sources = [page_url]
        if legal == "1":
            sources.append(OFFICIAL_PDF)
        if site_token:
            sources.append(BODY_SITES[site_token])
        if key == "gregory-theologian-monastery":
            sources.append(GREGORY_FOUNDATION)
        row = {
            "id": "gr-peristerion-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "sources": sources,
            "dedicated_page": page_url,
            "live_markers": split_markers(markers),
        }
        if address:
            row["address"] = [address, "Greece"]
        if phones:
            row["phones"] = split_values(phones)
        if emails:
            row["emails"] = split_values(emails)
        if site_token:
            row["site"] = BODY_SITES[site_token]
        if row.get("phones") or row.get("emails") or row.get("site"):
            row["contact_sources"] = [page_url]
            if site_token:
                row["contact_sources"].append(BODY_SITES[site_token])
            row["contact_checked"] = CHECKED
        rows.append(row)

    for number, raw in enumerate(EMBEDDED_SOURCE.strip().splitlines(), 35):
        (page_number, key, name, local, seat, address, markers) = raw.split(
            "|", 6
        )
        page_url = PAGE_URLS[int(page_number) - 1]
        rows.append({
            "id": "gr-peristerion-%03d-%s" % (number, key),
            "parent": PARENT,
            "kind": "parish",
            "rank": "Parish Chapel",
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address, "Greece"],
            "sources": [page_url],
            "live_markers": split_markers(markers),
        })
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {
    row["seat"]: row["seat"] for row in ROWS if row.get("seat")
}

EXPECTED_TOTAL = 38
EXPECTED_OWNER_COUNTS = {PARENT: 38}
EXPECTED_KINDS = {"monastery": 2, "parish": 36}
EXPECTED_RANKS = {
    "Cathedral": 1,
    "Cemetery Church": 1,
    "Church": 1,
    "Metropolitan Chapel": 7,
    "Metropolitan Church": 1,
    "Metropolitan Pilgrimage Chapel": 1,
    "Monastery": 2,
    "Parish Chapel": 8,
    "Parish Church": 16,
}
EXPECTED_CONTACT_BODIES = 30
EXPECTED_PHONE_BODIES = 30
EXPECTED_PHONE_VALUES = 36
EXPECTED_EMAIL_BODIES = 27
EXPECTED_EMAIL_VALUES = 28
EXPECTED_SITE_BODIES = 4
EXPECTED_ADDRESS_BODIES = 37
EXISTING_PARENTS = {PARENT}
ALLOWED_HOSTS = {
    "imperisteriou.gr",
    "www.imperisteriou.gr",
    "ecclesiagreece.gr",
    "www.ecclesiagreece.gr",
    "evaggelistriaperisteri.blogspot.com",
    "ptaxiarchisper.com",
    "www.ptaxiarchisper.com",
    "inagioupavlou.gr",
    "www.inagioupavlou.gr",
    "agiosierotheosperisteri.gr",
    "www.agiosierotheosperisteri.gr",
}
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
    if len(sources) != len(set(sources)):
        raise ValueError("%s repeats an identity source" % item.get("id"))
    for source_url in sources:
        validate_url(source_url, item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)

    contact_sources = list(item.get("contact_sources") or [])
    has_contact = bool(
        item.get("phones") or item.get("emails") or item.get("site")
    )
    has_contact_metadata = bool(
        contact_sources or item.get("contact_checked")
    )
    if has_contact != has_contact_metadata:
        raise ValueError("%s has mismatched contact metadata" % item.get("id"))
    if has_contact:
        if not contact_sources or item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks current contact provenance" % item.get("id"))
        for source_url in contact_sources:
            validate_url(source_url, item.get("id"))
            if source_url not in sources:
                raise ValueError("contact source is outside identity sources")
    elif "contact_sources" in item or "contact_checked" in item:
        raise ValueError("%s has metadata without contacts" % item.get("id"))

    site = item.get("site")
    if site:
        validate_url(site, item.get("id"))
        source_hosts = {urlparse(value).netloc for value in sources}
        if urlparse(site).netloc not in source_hosts:
            raise ValueError("%s site host lacks an identity source" % item.get("id"))
    item.pop("live_markers", None)
    item.pop("dedicated_page", None)
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Peristerion candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Peristerion candidate ledger date drifted")
    expected_summary = {
        PARENT: 38,
        "total": 38,
        "dedicated_official_body_pages": 34,
        "current_embedded_chapel_rows": 4,
        "regulated_parish_rows": 14,
        "current_parish_body_pages": 18,
        "parish_kind_rows": 36,
        "monastery_kind_rows": 2,
        "exact_chapel_rows": 16,
        "cemetery_rows": 1,
        "contact_bodies": 30,
        "phone_bodies": 30,
        "public_phone_or_fax_values": 36,
        "email_bodies": 27,
        "public_email_values": 28,
        "body_owned_sites": 4,
        "address_bodies": 37,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Peristerion ledger summary drifted")
    for key in ("candidates", "source_reconciliations",
                "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Peristerion ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 4:
                raise ValueError("Peristerion ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    candidate_ids = [x.get("candidate_id") for x in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Peristerion ledger has invalid candidate id")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Peristerion ledger has forbidden punctuation")
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
        raise ValueError("Peristerion English name coverage drifted")
    if dict(sorted(ranks.items())) != EXPECTED_RANKS:
        raise ValueError("Peristerion rank totals drifted: %r" % dict(ranks))
    if dict(sorted(kinds.items())) != EXPECTED_KINDS:
        raise ValueError("Peristerion kind totals drifted")
    if dict(sorted(owners.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Peristerion parent totals drifted")
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
        raise ValueError("Peristerion contact coverage drifted: %r" %
                         (coverage,))
    validate_ledger()
    return {PARENT: {"v": 1, "parent": PARENT,
                     "country": "GR", "rows": result}}


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 Plithos directory source audit",
        "Accept": "text/html,application/xhtml+xml,application/pdf,application/xml,text/xml",
        "Accept-Encoding": "identity",
    })
    with urlopen(request, timeout=60) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    return payload, content_type


def normalized_page(payload):
    text = payload.decode("utf-8", "replace")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return unicase(re.sub(r"\s+", " ", text))


def compact_digits(value):
    return re.sub(r"\D", "", value)


def check_live_sources():
    required = {SITEMAP, OFFICIAL_PDF, CHURCH_OF_GREECE_PAGE}
    required.update(url for row in ROWS for url in row.get("sources", []))
    cache = {}
    errors = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch, url): url for url in required}
        for future in as_completed(futures):
            url = futures[future]
            try:
                payload, content_type = future.result()
                if url == OFFICIAL_PDF:
                    if not payload.startswith(b"%PDF") and "pdf" not in content_type:
                        raise ValueError("source is not a PDF")
                    cache[url] = payload
                elif url == SITEMAP:
                    if "xml" not in content_type and not payload.lstrip().startswith(b"<?xml"):
                        raise ValueError("source is not XML")
                    cache[url] = payload
                else:
                    if ("html" not in content_type and
                            not payload.lstrip().startswith(b"<")):
                        raise ValueError("source is not HTML")
                    cache[url] = normalized_page(payload)
            except Exception as exc:
                errors.append("%s failed: %s" % (url, exc))
    if errors:
        raise ValueError("; ".join(sorted(errors)))

    root = ElementTree.fromstring(cache[SITEMAP])
    live_locations = []
    for url_node in root.findall("./{*}url"):
        node = url_node.find("./{*}loc")
        if node is not None and node.text and node.text.strip():
            live_locations.append(node.text.strip())
    if len(live_locations) != 35 or live_locations[0] != ARCHIVE_ROOT:
        raise ValueError("Peristerion sitemap no longer has one root and 34 pages")
    if tuple(live_locations[1:]) != PAGE_URLS:
        raise ValueError("Peristerion sitemap body order or membership drifted")
    dedicated = tuple(
        row["dedicated_page"] for row in ROWS if row.get("dedicated_page")
    )
    if dedicated != PAGE_URLS:
        raise ValueError("Peristerion dedicated-page reconciliation drifted")

    if unicase("ΠΕΡΙΣΤΕΡΙΟΥ") not in cache[CHURCH_OF_GREECE_PAGE]:
        raise ValueError("Church of Greece parent profile lacks Peristerion marker")
    if unicase("Κηπούπολης") not in cache[GREGORY_FOUNDATION]:
        raise ValueError("Saint Gregory foundation source lacks Kipoupoli marker")

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
    print("Peristerion live sources: %d URLs checked" % len(required))


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
        print("Peristerion: 38 exact bodies; 34 current body pages and "
              "4 exact current embedded chapels")
        print("Contacts: 30 bodies; 36 phones or faxes; 28 emails; "
              "4 live body sites")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Peristerion: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
