# -*- coding: utf-8 -*-
"""Exact named bodies of the Metropolis of Larisa and Tyrnavos.

The current parish roster is the Metropolis's 8 June 2022 allocation of its
seven archieratical regions. The current monastery page supplies the five
monasteries it presently describes and the pilgrimage church at Tempe. The
Metropolis's 2021 official handbook supplies its named chapels and fixed
institutional monastery contacts. Current 2026 notices confirm newer or
otherwise separately identifiable bodies. Personal clergy contacts are not
published here.
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


PARENT = "gr-larisa"
CHECKED = "2026-11-15"
CANDIDATE_LEDGER = (
    Path(__file__).resolve().parent
    / "directory_candidates"
    / "larisa_country.json"
)

HOME = "https://imlarisis.gr/"
PARISH_ROSTER = (
    "https://imlarisis.gr/home/imlt/"
    "%CE%B1%CF%81%CF%87%CE%B9%CE%B5%CF%81%CE%B1%CF%84%CE%B9%CE%BA%CE%B5%CF%83-"
    "%CF%80%CE%B5%CF%81%CE%B9%CF%86%CE%B5%CF%81%CE%B5%CE%B9%CE%B5%CF%83-"
    "%CE%B5%CE%BD%CE%BF%CF%81%CE%B9%CE%B5%CF%83/"
)
MONASTERY_PAGE = (
    "https://imlarisis.gr/home/imlt/"
    "%CE%B9%CE%B5%CF%81%CE%B5%CF%82-%CE%BC%CE%BF%CE%BD%CE%B5%CF%82/"
)
HANDBOOK = "https://imlarisis.gr/wp-content/uploads/2020/12/Egkolpio2021.pdf"
ALL_SAINTS_PAGE = "https://imlarisis.gr/prog-imagpanton/"
NECTARIOS_NIKAIA_PAGE = "https://imlarisis.gr/prog-agiou-nektariou-nikaia-2026/"
NECTARIOS_LARISA_PAGE = "https://imlarisis.gr/prog-agiou-nektariou-larisa-2026/"
CHRYSOSTOM_PAGE = (
    "https://imlarisis.gr/"
    "i-eorti-tou-ag-ioannou-chrisostomou-terpsithea-2026/"
)
OLD_CEMETERY_PAGE = (
    "https://imlarisis.gr/prog-pammegiston-taksiarxon-larisis-2026/"
)
CHURCH_OF_GREECE_PAGE = (
    "http://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
    "larises-kai-tyrnabou"
)


# local|English dedication|Greek locality|English locality|rank
PARISH_ROWS = r'''
Ἱ. Ν. Ἁγίου Ἀχιλλίου (Μητροπολιτικός) Λαρίσης|Saint Achillius|Λαρίσης|Larissa|Metropolitan Cathedral
Ἱ. Ν. Ἁγίου Ἀθανασίου Λαρίσης|Saint Athanasius|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Λαρίσης|Saint George|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Δημητρίου Λαρίσης|Saint Demetrius|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ζωοδόχου Πηγῆς Λαρίσης|Life-giving Spring|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίων Κωνσταντίνου καίἙλένης Λαρίσης|Saints Constantine and Helen|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίων Τεσσαράκοντα Μαρτύρων Λαρίσης|Forty Holy Martyrs|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Χαραλάμπους Λαρίσης|Saint Charalambos|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. τῆςτοῦ Θεοῦ Σοφίας Λαρίσης|Wisdom of God|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Γιάννουλης|Saint George|Γιάννουλης|Giannouli|Parish Church
Ἱ. Ν. Ἁγίων Δώδεκα Ἀποστόλων Γιάννουλης|Holy Twelve Apostles|Γιάννουλης|Giannouli|Parish Church
Ἱ. Ν. Γενεσίου Θεοτόκου Ἐλευθερίου|Nativity of the Theotokos|Ἐλευθερίου|Eleftherio|Parish Church
Ἱ. Ν. ἉγίουἈθανασίου Κουλουρίου|Saint Athanasius|Κουλουρίου|Koulouri|Parish Church
Ἱ. Ν. ἉγίουἈθανασίου Ὀμορφοχωρίου|Saint Athanasius|Ὀμορφοχωρίου|Omorfochori|Parish Church
Ἱ. Ν. Ἁγίου Νικολάου Λαρίσης|Saint Nicholas|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου ἐξ Ἰωαννίνων Λαρίσης|Saint George of Ioannina|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίων Θεοδώρων Λαρίσης|Holy Theodores|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Θωμᾶ Λαρίσης|Saint Thomas|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. ἉγίωνΠέτρου καί Παύλου Λαρίσης|Saints Peter and Paul|Λαρίσης|Larissa|Parish Church
Ἱ Ν. Ἁγίας Τριάδος Λαρίσης|Holy Trinity|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἀναλήψεως Σωτῆρος Λαρίσης|Ascension of the Savior|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Παμμεγίστων Ταξιαρχῶν Λαρίσης|Holy Archangels|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Προφήτου Ἠλιοῦ Λαρίσης|Prophet Elijah|Λαρίσης|Larissa|Parish Church
Ἱ. Ν. Ἁγίου Νικολάου Ἀμυγδαλέας|Saint Nicholas|Ἀμυγδαλέας|Amygdalea|Parish Church
Ἱ. Ν. ἉγίουΒησσαρίωνος Ἐλευθερῶν|Saint Bessarion|Ἐλευθερῶν|Eleftheres|Parish Church
Ἱ. Ν. Ἁγίου Σπυρίδωνος Κοιλάδος|Saint Spyridon|Κοιλάδος|Koilada|Parish Church
Ἱ. Ν. Ἁγίου Νικολάου Κουτσοχέρου|Saint Nicholas|Κουτσοχέρου|Koutsochero|Parish Church
Ἱ. Ν. ἉγίουΒασιλείου Μάνδρας|Saint Basil|Μάνδρας|Mandra|Parish Church
Ἱ. Ν. Ἁγίου Βησσαρίωνος Ραχούλας|Saint Bessarion|Ραχούλας|Rachoula|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Τερψιθέας|Saint Athanasius|Τερψιθέας|Terpsithea|Parish Church
Ἱ. Ν. Παναγίας Φανερωμένης (Μητροπολιτικός) Τυρνάβου|Panagia Phaneromene|Τυρνάβου|Tyrnavos|Metropolitan Cathedral
Ἱ. Ν. Ἁγίου Γεωργίου Τυρνάβου|Saint George|Τυρνάβου|Tyrnavos|Parish Church
Ἱ. Ν. Ἁγίου Δημητρίου Τυρνάβου|Saint Demetrius|Τυρνάβου|Tyrnavos|Parish Church
Ἱ. Ν. Τιμίου Προδρόμου Τυρνάβου|Saint John the Forerunner|Τυρνάβου|Tyrnavos|Parish Church
Ἱ. Ν. Κοιμήσεως Θεοτόκου Ἀμπελῶνος|Dormition of the Theotokos|Ἀμπελῶνος|Ampelonas|Parish Church
Ἱ. Ν. Ἁγίων Κωνσταντίνου καί Ἑλένης Ἀμπελῶνος|Saints Constantine and Helen|Ἀμπελῶνος|Ampelonas|Parish Church
Ἱ. Ν. Ζωοδόχου Πηγῆς Ἀργυροπουλίου|Life-giving Spring|Ἀργυροπουλίου|Argyropouli|Parish Church
Ἱ. Ν. Ἁγίων Κωνσταντίνου καί Ἑλένης Βρυοτόπου|Saints Constantine and Helen|Βρυοτόπου|Vryotopos|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Γυρτώνης|Saint Athanasius|Γυρτώνης|Gyrtoni|Parish Church
Ἱ. Ν. Ἁγίου Χαραλάμπους Δασοχωρίου|Saint Charalambos|Δασοχωρίου|Dasochori|Parish Church
Ἱ. Ν. Ἁγίου Δημητρίου Δελερίων|Saint Demetrius|Δελερίων|Deleria|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Δένδρων|Saint Athanasius|Δένδρων|Dendra|Parish Church
Ἱ. Ν. Ἁγίου Χαραλάμπους Πλατανουλίων|Saint Charalambos|Πλατανουλίων|Platanoulia|Parish Church
Ἱ. Ν. Εὐαγγελισμοῦ Θεοτόκου Ροδιᾶς|Annunciation of the Theotokos|Ροδιᾶς|Rodia|Parish Church
Ἱ. Ν. Ἁγίων Κωνσταντίνου καί Ἑλένης Φαλάνης|Saints Constantine and Helen|Φαλάνης|Falani|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ἀρμενίου|Saint Athanasius|Ἀρμενίου|Armenio|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ἀγναντερῆς|Saint Athanasius|Ἀγναντερῆς|Agnanteri|Parish Church
Ἱ. Ν. Ζωοδόχου Πηγῆς Ἀναγεννήσεως|Life-giving Spring|Ἀναγεννήσεως|Anagennisi|Parish Church
Ἱ. Ν. Ἁγίου Ἀχιλλίου Ἀχιλλείου|Saint Achillius|Ἀχιλλείου|Achillio|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Γαλήνης|Saint Athanasius|Γαλήνης|Galini|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Γλαύκης|Saint Athanasius|Γλαύκης|Glafki|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Κυψέλης-Κιλελέρ|Saint George|Κυψέλης-Κιλελέρ|Kypseli-Kileler|Parish Church
Ἱ. Ν. Κοιμήσεως Θεοτόκου Λοφίσκου|Dormition of the Theotokos|Λοφίσκου|Lofiskos|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Μεγάλου Μοναστηρίου|Saint Athanasius|Μεγάλου Μοναστηρίου|Megalo Monastiri|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Μελίας|Saint Athanasius|Μελίας|Melia|Parish Church
Ἱ. Ν. Ζωοδόχου Πηγῆς Μέλισσας|Life-giving Spring|Μέλισσας|Melissa|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Μοδέστου|Saint Athanasius|Μοδέστου|Modestos|Parish Church
Ἱ. Ν. Ἁγίου Χαραλάμπους Νίκης|Saint Charalambos|Νίκης|Niki|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Ναμάτων|Saint George|Ναμάτων|Namaton|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Νέου Περιβολίου|Saint George|Νέου Περιβολίου|Neo Perivoli|Parish Church
Ἱ. Ν. Ἁγίου Χαραλάμπους Πλατυκάμπου|Saint Charalambos|Πλατυκάμπου|Platykampos|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ριζομύλου|Saint Athanasius|Ριζομύλου|Rizomylos|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Στεφανοβικείου|Saint Athanasius|Στεφανοβικείου|Stefanovikio|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Σωτηρίου|Saint Athanasius|Σωτηρίου|Sotirio|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Χάλκης|Saint Athanasius|Χάλκης|Chalki|Parish Church
Ἱ. Ν. Ἁγίας Παρασκευῆς Ἀμπελακίων|Saint Paraskevi|Ἀμπελακίων|Ampelakia|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ἀμπελακίων|Saint Athanasius|Ἀμπελακίων|Ampelakia|Parish Church
Ἱ. Ν. Γενεσίου Θεοτόκου Αἰγάνης|Nativity of the Theotokos|Αἰγάνης|Aigani|Parish Church
Ἱ. Ν. Εὐαγγελισμοῦ Θεοτόκου Εὐαγγελισμοῦ|Annunciation of the Theotokos|Εὐαγγελισμοῦ|Evangelismos|Parish Church
Ἱ. Ν. Ἁγίου Νικολάου Ἰτέας|Saint Nicholas|Ἰτέας|Itea|Parish Church
Ἱ. Ν. Παμμεγίστων Ταξιαρχῶν Καρίτσας|Holy Archangels|Καρίτσας|Karitsa|Parish Church
Ἱ. Ν. Μεταμορφώσεως Σωτῆρος Κουλούρας|Transfiguration of the Savior|Κουλούρας|Kouloura|Parish Church
Ἱ. Ν. Παμμεγίστων Ταξιαρχῶν Κρανιᾶς|Holy Archangels|Κρανιᾶς|Krania|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ὁμολίου|Saint Athanasius|Ὁμολίου|Omolio|Parish Church
Ἱ. Ν. Ἁγίων Κωνσταντίνου καί Ἑλένης Παλαιοπύργου|Saints Constantine and Helen|Παλαιοπύργου|Palaiopyrgos|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Πυργετοῦ|Saint George|Πυργετοῦ|Pyrgetos|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ραψάνης|Saint Athanasius|Ραψάνης|Rapsani|Parish Church
Ἱ. Ν. Κοιμήσεως Θεοτόκου Ραψάνης|Dormition of the Theotokos|Ραψάνης|Rapsani|Parish Church
Ἱ. Ν. Ἁγίου Νικολάου Στομίου|Saint Nicholas|Στομίου|Stomio|Parish Church
Ἱ. Ν. Ἁγίας Τριάδος Τεμπῶν|Holy Trinity|Τεμπῶν|Tempe|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Νικαίας|Saint George|Νικαίας|Nikaia|Parish Church
Ἱ. Ν. Ἁγίας Παρασκευῆς Ἁγίας Παρασκευῆς|Saint Paraskevi|Ἁγίας Παρασκευῆς|Agia Paraskevi|Parish Church
Ἱ. Ν. Ἁγίων Ἀναργύρων Ἁγίων Ἀναργύρων|Holy Unmercenaries|Ἁγίων Ἀναργύρων|Agioi Anargyroi|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Ἁγίου Γεωργίου|Saint George|Ἁγίου Γεωργίου|Agios Georgios|Parish Church
Ἱ. Ν. Ἁγίου Δημητρίου Ἀργυρομύλων|Saint Demetrius|Ἀργυρομύλων|Argyromyloi|Parish Church
Ἱ. Ν. Ἁγίου Βησσαρίωνος Διλόφου|Saint Bessarion|Διλόφου|Dilofos|Parish Church
Ἱ. Ν. Ἁγίου Βησσαρίωνος Δοξαρᾶ|Saint Bessarion|Δοξαρᾶ|Doxaras|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ζαππείου|Saint Athanasius|Ζαππείου|Zappeio|Parish Church
Ἱ. Ν. Ἁγίου Ἀχιλλίου Καλοῦ Νεροῦ|Saint Achillius|Καλοῦ Νεροῦ|Kalo Nero|Parish Church
Ἱ. Ν. Ἁγίου Κωνσταντίνου καί Ἑλένης Κάμπου|Saints Constantine and Helen|Κάμπου|Kampos|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Κραννῶνος|Saint Athanasius|Κραννῶνος|Krannonas|Parish Church
Ἱ. Ν. Ἁγίου Χαραλάμπους Κυπαρισσίου|Saint Charalambos|Κυπαρισσίου|Kyparissio|Parish Church
Ἱ. Ν. Μεταμορφώσεως Σωτῆρος Κυπαρίσσου|Transfiguration of the Savior|Κυπαρίσσου|Kyparissos|Parish Church
Ἱ. Ν. Ἁγίας Παρασκευῆς Λουτροῦ|Saint Paraskevi|Λουτροῦ|Loutro|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Μαυροβουνίου|Saint Athanasius|Μαυροβουνίου|Mavrovouni|Parish Church
Ἱ. Ν. Κοιμήσεως Θεοτόκου Μεσορράχης|Dormition of the Theotokos|Μεσορράχης|Mesorrachi|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Μοσχοχωρίου|Saint George|Μοσχοχωρίου|Moschochori|Parish Church
Ἱ. Ν. Ἁγίου Σπυρίδωνος Μύρων|Saint Spyridon|Μύρων|Myra|Parish Church
Ἱ. Ν. Κοιμήσεως Θεοτόκου Νέων Καρυῶν|Dormition of the Theotokos|Νέων Καρυῶν|Nea Karya|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Νέας Λεύκης|Saint George|Νέας Λεύκης|Nea Lefki|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Σοφοῦ|Saint George|Σοφοῦ|Sofo|Parish Church
Ἱ. Ν. Ἁγίου Νικολάου Χαρᾶς|Saint Nicholas|Χαρᾶς|Chara|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ψυχικοῦ|Saint Athanasius|Ψυχικοῦ|Psychiko|Parish Church
Ἱ. Ν. Ἁγίων Κωνσταντίνου καί Ἑλένης Συκουρίου|Saints Constantine and Helen|Συκουρίου|Sykourio|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Γόννων|Saint George|Γόννων|Gonnoi|Parish Church
Ἱ. Ν. Ἁγίας Παρασκευῆς Γόννων|Saint Paraskevi|Γόννων|Gonnoi|Parish Church
Ἱ. Ν. Ἁγίου Ἀθανασίου Ἐλαίας|Saint Athanasius|Ἐλαίας|Elaia|Parish Church
Ἱ. Ν. Ζωοδόχου Πηγῆς Ἐλάτειας|Life-giving Spring|Ἐλάτειας|Elateia|Parish Church
Ἱ. Ν. Ἁγίων Δώδεκα Ἀποστόλων Καλλιπεύκης|Holy Twelve Apostles|Καλλιπεύκης|Kallipefki|Parish Church
Ἱ. Ν. Τιμίου Προδρόμου Καλοχωρίου|Saint John the Forerunner|Καλοχωρίου|Kalochori|Parish Church
Ἱ. Ν. Τιμίου Προδρόμου Κυψελοχωρίου|Saint John the Forerunner|Κυψελοχωρίου|Kypselochori|Parish Church
Ἱ. Ν. Ἁγίου Θωμᾶ Μακρυχωρίου|Saint Thomas|Μακρυχωρίου|Makrychori|Parish Church
Ἱ. Ν. Ἁγίου Δημητρίου Μελισσοχωρίου|Saint Demetrius|Μελισσοχωρίου|Melissochori|Parish Church
Ἱ. Ν. Ἁγίου Δημητρίου Νέσσωνος|Saint Demetrius|Νέσσωνος|Nesson|Parish Church
Ἱ. Ν. Ἁγίου Ἀντωνίου Ὄσσης|Saint Anthony|Ὄσσης|Ossa|Parish Church
Ἱ. Ν. Τιμίου Προδρόμου Παραποτάμου|Saint John the Forerunner|Παραποτάμου|Parapotamos|Parish Church
Ἱ. Ν. Ἁγίου Βασιλείου Πουρναρίου|Saint Basil|Πουρναρίου|Pournari|Parish Church
Ἱ. Ν. Γενεσίου Θεοτόκου Σπηλιᾶς|Nativity of the Theotokos|Σπηλιᾶς|Spilia|Parish Church
Ἱ. Ν. Ἁγίου Γεωργίου Χειμαδίου|Saint George|Χειμαδίου|Cheimadio|Parish Church
'''


SITE_CONTACTS = {
    "Ἱ. Ν. Ἁγίου Ἀχιλλίου (Μητροπολιτικός) Λαρίσης": {
        "site": "https://www.inaa.gr/",
        "phones": ["2410-537159"],
        "emails": ["inaagr@gmail.com"],
        "address": ["Ιερός Μητροπολιτικός Ναός Αγίου Αχιλλίου", "41221 Λάρισα"],
        "source": "https://www.inaa.gr/%CE%B5%CF%80%CE%B9%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CE%BD%CE%AF%CE%B1-%CE%B9%CE%BD%CE%B1%CE%B1/",
    },
    "Ἱ. Ν. Ἁγίου Νικολάου Λαρίσης": {
        "site": "https://www.inagiounikolaoularisis.gr/",
        "phones": ["2410-623438"],
        "emails": ["info@inagiounikolaoularisis.gr"],
        "address": ["Ηπείρου 52", "41222 Λάρισα"],
        "source": "https://www.inagiounikolaoularisis.gr/contact",
    },
    "Ἱ. Ν. Ζωοδόχου Πηγῆς Λαρίσης": {
        "site": "https://www.panagialarisis.gr/",
        "phones": ["2410-532350"],
        "emails": ["panagialarisis@yahoo.gr"],
        "address": ["Χρυσοστόμου και Αγίου Βησσαρίωνος", "Λάρισα"],
        "source": "https://www.panagialarisis.gr/",
    },
    "Ἱ. Ν. Ἁγίου Γεωργίου Γιάννουλης": {
        "site": "http://inaggeorgiou.blogspot.com/",
        "phones": ["2410-591654"],
        "emails": ["ag.georgios.giannoulis@gmail.com"],
        "source": "http://inaggeorgiou.blogspot.com/",
    },
    "Ἱ. Ν. Ἁγίου Γεωργίου Λαρίσης": {
        "site": "https://galilea.gr/",
        "phones": ["+30-2410-280569"],
        "emails": ["info@galilea.gr"],
        "source": "https://galilea.gr/",
    },
    "Ἱ. Ν. ἉγίωνΠέτρου καί Παύλου Λαρίσης": {
        "site": "http://inpetroukpaulou.blogspot.com/",
        "phones": ["2410-614114"],
        "emails": ["inpetroukpaulou@gmail.com"],
        "source": "http://inpetroukpaulou.blogspot.com/",
    },
    "Ἱ. Ν. Ἁγίων Κωνσταντίνου καίἙλένης Λαρίσης": {
        "site": "http://ierosnaoskonstantinou-elenislarisas.blogspot.com/",
        "source": "http://ierosnaoskonstantinou-elenislarisas.blogspot.com/",
    },
    "Ἱ. Ν. Προφήτου Ἠλιοῦ Λαρίσης": {
        "site": "https://profitis-ilias-larisas.blogspot.com/",
        "phones": ["2410-623439"],
        "emails": ["profitis.ilias.larisas@gmail.com"],
        "source": "https://profitis-ilias-larisas.blogspot.com/",
    },
    "Ἱ. Ν. τῆςτοῦ Θεοῦ Σοφίας Λαρίσης": {
        "site": "https://www.inagiasofialarisas.gr/",
        "phones": ["2410-550093"],
        "emails": ["agiasofialarisas@gmail.com"],
        "address": ["Τέρμα Φλωρίνης - Λεωφόρος Καραμανλή", "Χαραυγή - Λάρισα", "41448"],
        "source": "https://www.inagiasofialarisas.gr/",
    },
    "Ἱ. Ν. Ἁγίων Δώδεκα Ἀποστόλων Γιάννουλης": {
        "site": "https://inag12apostolon.wordpress.com/",
        "phones": ["2410-593209"],
        "address": ["Εργατικές Κατοικίες Γιάννουλης", "41500"],
        "source": "https://inag12apostolon.wordpress.com/%CE%B5%CF%80%CE%B9%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CE%BD%CE%B9%CE%B1/",
    },
}


ADDITIONAL_ROWS = [
    # Metropolitan chapels in the official 2021 handbook.
    ("Ἅγ. Βησσαρίων", "Saint Bessarion Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Στυλιανός", "Saint Stylianos Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Λουκᾶς Παν. Νοσοκομείου Λαρίσης", "Saint Luke Chapel at Larissa University Hospital", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Μεταμόρφωσις Σωτῆρος Κόκκινου Νεροῦ", "Transfiguration of the Savior Chapel at Kokkino Nero", "Kokkino Nero", "Κόκκινο Νερό", "Chapel", "parish", [HANDBOOK]),
    # Parish chapels.
    ("Ἅγ. Ἀθανάσιος", "Saint Athanasius Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἁγία Αἰκατερίνη", "Saint Catherine Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK, HOME]),
    ("Ἅγ. Ἀντώνιος", "Saint Anthony Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Ἐλευθέριος", "Saint Eleftherios Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἁγ. Μαρίνα", "Saint Marina Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Νεκτάριος", "Saint Nectarios Chapel on Eretrias Street in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK, NECTARIOS_LARISA_PAGE]),
    ("Ἅγ. Παντελεήμων", "Saint Panteleimon Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Τρύφων", "Saint Tryphon Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Μετ. Σωτῆρος", "Transfiguration of the Savior Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἁγ. Εἰρήνης Χρυσοβαλάντου", "Saint Irene Chrysovalantou Chapel in Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Κοιμητηριακός Ἱερός Ναός Ἀναστάσεως Λαζάρου", "Resurrection of Lazarus Cemetery Church in Larissa", "Larissa", "Λάρισα", "Cemetery Church", "parish", [HANDBOOK]),
    # Institution chapels.
    ("Ἁγ. Αἰκατερίνη Γηροκομείου Λαρίσης", "Saint Catherine Chapel at the Larissa Home for the Aged", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Ἀνάργυροι Γεν. Νοσοκομείου Λαρίσης", "Holy Unmercenaries Chapel at Larissa General Hospital", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Παναγίας Γλυκοφιλούσης Γεν. Νοσοκομείου Λαρίσης", "Panagia Glykophilousa Chapel at Larissa General Hospital", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἁγ. Τριῶν Ἱεραρχῶν Τ.Ε.Ι. Λαρίσης", "Three Holy Hierarchs Chapel at the Technological Institute of Larissa", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    # Military chapels, each named by the official handbook.
    ("Μετ. Σωτῆρος 1ης Στρατιᾶς", "Transfiguration of the Savior Chapel of the First Army", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Κοιμ. Θεοτόκου 110 Π.Μ.", "Dormition of the Theotokos Chapel of the 110th Combat Wing", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἁγ. Βαρβάρα Στρατ. Μπουγᾶ", "Saint Barbara Chapel at Bouga Army Camp", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Ὅσ. Δαμιανός ΔΑΚ, Ἐλευθέριον", "Venerable Damian Chapel at DAK Eleftherio", "Eleftherio", "Ἐλευθέριο", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Νικόλαος 303 Π.Ε.Β.", "Saint Nicholas Chapel of the 303rd PEB", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Μετ. Σωτῆρος 307 ΤΣΥΑΥ, Στεφανοβίκειον", "Transfiguration of the Savior Chapel of the 307th TSYAY", "Stefanovikio", "Στεφανοβίκειο", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγιος Ἐφραίμ Μ.ΑΦ.Κ.", "Saint Ephraim Chapel at MAFK", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    ("Προφ. Ἠλίας 1ης ΤΑΞΑΣ, Στεφανοβίκειον", "Prophet Elijah Chapel of the First Army Aviation Brigade", "Stefanovikio", "Στεφανοβίκειο", "Chapel", "parish", [HANDBOOK]),
    ("Ἅγ. Ραφαήλ 856 Α/Κ στρ. Μακρῆ", "Saint Raphael Chapel at Makris Army Camp", "Larissa", "Λάρισα", "Chapel", "parish", [HANDBOOK]),
    # Bodies identified by current official notices.
    ("Ιερό Παρεκκλήσιο Αγίου Νεκταρίου Νικαίας", "Saint Nectarios Chapel in Nikaia", "Nikaia", "Νίκαια", "Chapel", "parish", [NECTARIOS_NIKAIA_PAGE]),
    ("Παρεκκλήσιο του Αγίου Ιωάννου του Χρυσοστόμου Τερψιθέας", "Saint John Chrysostom Chapel in Terpsithea", "Terpsithea", "Τερψιθέα", "Chapel", "parish", [CHRYSOSTOM_PAGE]),
    ("Ιερός Ναός Παμμεγίστων Ταξιαρχών Λαρίσης (παλαιό Κοιμητήριο)", "Holy Archangels Church at the Old Cemetery in Larissa", "Larissa", "Λάρισα", "Cemetery Church", "parish", [OLD_CEMETERY_PAGE]),
    # Current monasteries and the pilgrimage church.
    ("ΙΕΡΑ ΜΟΝΗ ΠΑΝΑΓΙΑΣ ΓΛΥΚΟΦΙΛΟΥΣΑΣ ΡΑΨΑΝΗΣ", "Panagia Glykophilousa Monastery at Rapsani", "Rapsani", "Ραψάνη", "Monastery", "monastery", [MONASTERY_PAGE, HANDBOOK]),
    ("ΙΕΡΑ ΜΟΝΗ ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΤΟΥ ΣΩΤΗΡΟΣ ΡΑΨΑΝΗΣ", "Transfiguration of the Savior Monastery at Rapsani", "Rapsani", "Ραψάνη", "Monastery", "monastery", [MONASTERY_PAGE, HANDBOOK]),
    ("ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΡΑΦΑΗΛ ΠΥΡΓΕΤΟΥ", "Saints Raphael, Nicholas, and Irene Monastery at Pyrgetos", "Pyrgetos", "Πυργετός", "Monastery", "monastery", [MONASTERY_PAGE]),
    ("ΙΕΡΑ ΜΟΝΗ ΚΟΜΝΗΝΕΙΟΥ ΣΤΟΜΙΟΥ ΛΑΡΙΣΑΣ", "Komnenion Dormition of the Theotokos and Saint Demetrius Monastery at Stomio", "Stomio", "Στόμιο", "Monastery", "monastery", [MONASTERY_PAGE, HANDBOOK]),
    ("ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΝΙΚΟΔΗΜΟΥ ΑΓΙΟΡΕΙΤΟΥ", "Saint Nikodemos the Hagiorite Monastery near Pyrgetos", "Pyrgetos", "Πυργετός", "Monastery", "monastery", [MONASTERY_PAGE, HANDBOOK]),
    ("υπό σύσταση Ιερά Μονή Αγίων Πάντων Αμυγδαλέας", "All Saints Monastery under Establishment at Amygdalea", "Amygdalea", "Ἀμυγδαλέα", "Monastery under Establishment", "monastery", [ALL_SAINTS_PAGE]),
    ("ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΤΕΜΠΩΝ", "Saint Paraskevi Pilgrimage Church at Tempe", "Tempe", "Τέμπη", "Pilgrimage Church", "parish", [MONASTERY_PAGE, HANDBOOK]),
]


ADDITIONAL_CONTACTS = {
    "Ἁγία Αἰκατερίνη": {
        "site": "http://www.agia-aikaterini-larissis.com/",
        "source": HOME,
    },
    "ΙΕΡΑ ΜΟΝΗ ΠΑΝΑΓΙΑΣ ΓΛΥΚΟΦΙΛΟΥΣΑΣ ΡΑΨΑΝΗΣ": {
        "phones": ["24950-61010"], "source": HANDBOOK,
    },
    "ΙΕΡΑ ΜΟΝΗ ΜΕΤΑΜΟΡΦΩΣΕΩΣ ΤΟΥ ΣΩΤΗΡΟΣ ΡΑΨΑΝΗΣ": {
        "phones": ["24950-61170"], "source": HANDBOOK,
    },
    "ΙΕΡΑ ΜΟΝΗ ΚΟΜΝΗΝΕΙΟΥ ΣΤΟΜΙΟΥ ΛΑΡΙΣΑΣ": {
        "phones": ["24950-91220"], "source": HANDBOOK,
    },
    "ΙΕΡΑ ΜΟΝΗ ΑΓΙΟΥ ΝΙΚΟΔΗΜΟΥ ΑΓΙΟΡΕΙΤΟΥ": {
        "phones": ["24957-70004"], "source": HANDBOOK,
    },
    "ΙΕΡΟ ΠΡΟΣΚΥΝΗΜΑ ΑΓΙΑΣ ΠΑΡΑΣΚΕΥΗΣ ΤΕΜΠΩΝ": {
        "phones": ["24950-93294"], "source": HANDBOOK,
    },
}


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:72]


def parse_parishes():
    rows = []
    for line in PARISH_ROWS.strip().splitlines():
        values = [value.strip() for value in line.split("|")]
        if len(values) != 5:
            raise ValueError("invalid Larisa parish row: %s" % line)
        local, dedication, address_el, seat, rank = values
        name = "%s %s in %s" % (dedication, rank, seat)
        item = {
            "parent": PARENT,
            "kind": "parish",
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address_el],
            "sources": [PARISH_ROSTER],
        }
        contact = SITE_CONTACTS.get(local)
        if contact:
            item["site"] = contact["site"]
            for key in ("phones", "emails", "address"):
                if contact.get(key):
                    item[key] = list(contact[key])
            item["sources"].extend([HOME, contact["source"]])
            if contact.get("phones") or contact.get("emails"):
                item["contact_sources"] = [contact["source"]]
                item["contact_checked"] = CHECKED
        rows.append(item)
    return rows


def build_rows():
    rows = parse_parishes()
    for local, name, seat, address_el, rank, kind, sources in ADDITIONAL_ROWS:
        item = {
            "parent": PARENT,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "seat": seat,
            "country": "GR",
            "address": [address_el],
            "sources": list(sources),
        }
        contact = ADDITIONAL_CONTACTS.get(local)
        if contact:
            if contact.get("site"):
                item["site"] = contact["site"]
            if contact.get("phones"):
                item["phones"] = list(contact["phones"])
            if contact["source"] not in item["sources"]:
                item["sources"].append(contact["source"])
            if contact.get("phones") or contact.get("emails"):
                item["contact_sources"] = [contact["source"]]
                item["contact_checked"] = CHECKED
        rows.append(item)
    for index, item in enumerate(rows, 1):
        item["id"] = "gr-larisa-%03d-%s" % (index, slug(item["name"]))
    return rows


ROWS = build_rows()
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in ROWS}

EXPECTED_TOTAL = 157
EXPECTED_OWNER_COUNTS = {PARENT: 157}
EXPECTED_KINDS = {"monastery": 6, "parish": 151}
EXPECTED_RANKS = {
    "Cemetery Church": 2,
    "Chapel": 29,
    "Metropolitan Cathedral": 2,
    "Monastery": 5,
    "Monastery under Establishment": 1,
    "Parish Church": 117,
    "Pilgrimage Church": 1,
}
EXPECTED_CONTACT_BODIES = 16
EXPECTED_PHONE_BODIES = 14
EXPECTED_PHONE_VALUES = 14
EXPECTED_EMAIL_BODIES = 8
EXPECTED_EMAIL_VALUES = 8
EXPECTED_SITE_BODIES = 11
EXPECTED_ADDRESS_BODIES = 157
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
        if value not in (None, "", [])
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
                raise ValueError("%s contact source is outside identity sources" % item.get("id"))
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s lacks a current contact check date" % item.get("id"))
    if item.get("site"):
        validate_url(item["site"], item.get("id"))
    return item


def validate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("countries") != ["GR"]:
        raise ValueError("Larisa candidate ledger metadata drifted")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Larisa candidate ledger date drifted")
    expected_summary = {
        PARENT: 157,
        "total": 157,
        "parish_kind_rows": 151,
        "monastery_kind_rows": 6,
        "contact_bodies": 16,
        "phone_bodies": 14,
        "public_phone_values": 14,
        "email_bodies": 8,
        "public_email_values": 8,
        "body_owned_sites": 11,
        "address_bodies": 157,
    }
    if ledger.get("published_summary") != expected_summary:
        raise ValueError("Larisa ledger summary drifted")
    for key in ("candidates", "source_reconciliations", "official_parent_audit", "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Larisa ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Larisa ledger item has invalid sources")
            for source_url in sources:
                validate_url(source_url, entry.get("candidate_id") or key)
    rendered = json.dumps(ledger, ensure_ascii=False)
    if FORBIDDEN_PUNCTUATION.search(rendered):
        raise ValueError("Larisa candidate ledger has forbidden punctuation")
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
            raise ValueError("%s duplicates %s after Greek normalization" % (row_id, signatures[signature]))
        signatures[signature] = row_id
        ids.add(row_id)
        rank_counts[item["rank"]] += 1
        kind_counts[item["kind"]] += 1
        owner_counts[parent] += 1
        result.append(item)
    if len(result) != EXPECTED_TOTAL:
        raise ValueError("expected %d bodies, found %d" % (EXPECTED_TOTAL, len(result)))
    if set(ENGLISH_NAMES) != ids or len(ENGLISH_NAMES) != EXPECTED_TOTAL:
        raise ValueError("Larisa English name coverage drifted")
    expected_seats = {item["seat"] for item in result if item.get("seat")}
    if set(ENGLISH_SEATS) != expected_seats:
        raise ValueError("Larisa English seat coverage drifted")
    if dict(sorted(owner_counts.items())) != EXPECTED_OWNER_COUNTS:
        raise ValueError("Larisa parent totals drifted")
    if dict(sorted(kind_counts.items())) != EXPECTED_KINDS:
        raise ValueError("Larisa kind totals drifted")
    if dict(sorted(rank_counts.items())) != EXPECTED_RANKS:
        raise ValueError("Larisa rank totals drifted: %r" % dict(sorted(rank_counts.items())))
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
        raise ValueError("Larisa contact coverage drifted: %r" % (coverage,))
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
        print("Larisa and Tyrnavos: %d exact named bodies; %d carry current institutional contact data" % (EXPECTED_TOTAL, EXPECTED_CONTACT_BODIES))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory Larisa: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
