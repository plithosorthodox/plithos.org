#!/usr/bin/env python3
"""Validate current canonical Eastern Orthodox bodies in Turkey.

This country module is intentionally independent of the directory aggregator.
It emits branch payloads for later integration and checks its own source ledger.
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "turkey.json"

EP_ARCHDIOCESE = (
    "https://ec-patr.org/entities/archiepiskopi-konstantinoypoleos/"
)
EP_CHALCEDON = "https://ec-patr.org/entities/iera-mitropoli-xalkidonas/"
EP_DERKOI = "https://ec-patr.org/entities/iera-mitropoli-derkon/"
EP_PRINCES = "https://ec-patr.org/entities/iera-mitropoli-prigkiponnison/"
EP_PISIDIA = "https://ec-patr.org/entities/iera-mitropoli-pisidias/"
EP_VRYOULA = "https://ec-patr.org/entities/ieara-mitropolis-vruoulon/"
EP_SELYBRIA = "https://ec-patr.org/entities/iera-mitropolis-siluvrias/"
EP_ADRIANOPLE = "https://ec-patr.org/entities/iera-mitropoli-adrianoypoleos/"
EP_SMYRNA = "https://ec-patr.org/entities/iera-mitropoli-smyrnis/"
EP_IMBROS = "https://ec-patr.org/entities/iera-mitropoli-imvroy-tenedoy/"
EP_BURSA = "https://ec-patr.org/entities/iera-mitropoli-proysis/"
EP_GANOS = "https://ec-patr.org/entities/iera-mitropoli-ganou-kai-horas/"
EP_TURKEY = (
    "https://ec-patr.org/en/eparchies-of-the-throne/"
    "metropolitan-sees-in-turkiye/"
)
EP_GEORGIAN = (
    "https://ec-patr.org/en/13/07/15/43/address-of-his-all-holiness-"
    "ecumenical-patriarch-bartholomew-at-the-holy-church-of-saint-george-"
    "edirnekapi-sunday-13-july-2025-duplicate-1/"
)
EP_UKRAINIAN = (
    "https://ec-patr.org/23/02/15/01/address-of-his-all-holiness-"
    "ecumenical-patriarch-bartholomew-to-the-ukrainian-diplomatic-corps-"
    "and-the-local-ukrainian-community-in-istanbul-on-the-third-"
    "anniversary-of-the-russian-inva/"
)

MOSPAT_ROSTER_NOTICE = "https://mospat.ru/ru/news/91280/"
MOSPAT_CURRENT = "https://mospat.ru/en/news/93751/"
MOSPAT_BASE = "https://mospaturk.ru/community/"

ANTIOCH_DIOCESE = (
    "https://www.antiochpatriarchate.org/ar/page/"
    "metropolitan-of-tarsus-adana-and-hatay-gulf-of-alexandria/3004/"
)
ANTIOCH_CATHEDRAL = (
    "https://www.antiochpatriarchate.org/ar/page/"
    "patriarch-john-x-from-the-cathedral-of-the-apostles-peter-and-paul-"
    "in-antioch/3084/"
)
ANTIOCH_ISKENDERUN = "https://www.antiochpatriarchate.org/en/page/3093/"
ANTIOCH_SURIYAH = "https://www.antiochpatriarchate.org/en/page/2577/"
ANTIOCH_MERSIN = "https://www.antiochpatriarchate.org/en/page/2578/"
ANTIOCH_CONTACT = (
    "https://www.antiochpatriarchate.org/ar/category/contact/93/"
)

BULGARIAN_STATUTE = "https://bg-patriarshia.bg/statute"
BULGARIAN_CURRENT = (
    "https://bg-patriarshia.bg/news/"
    "obyava-bptso-v-istanbul-republika-turtsia-obyavyava-priem-na"
)
BULGARIAN_SITES = "https://bg-patriarshia.bg/church-sites"
ROMANIAN_COMMUNITIES = (
    "https://patriarhia.ro/organizarea-bisericii-ortodoxe-romane/"
    "reprezentante-si-comunitati-externe/"
)
ROMANIAN_ISTANBUL = (
    "https://basilica.ro/en/ecumenical-patriarch-romanian-church-"
    "constantinople-martyrs/"
)


def body(row_id, parent, name, local, seat, sources, rank="Church",
         kind="parish", address=None, emails=None, phones=None):
    item = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "TR",
        "sources": list(sources),
    }
    if address:
        item["address"] = list(address)
    if emails:
        item["emails"] = list(emails)
    if phones:
        item["phones"] = list(phones)
    if emails or phones:
        item["contact_sources"] = [sources[0]]
        item["contact_checked"] = CHECKED
    return item


def ep(row_id, parent, name, local, seat, source, rank="Church",
       kind="parish", address=None, emails=None, phones=None,
       extra_sources=None):
    sources = [source] + list(extra_sources or [])
    return body(row_id, parent, name, local, seat, sources, rank, kind,
                address, emails, phones)


CONSTANTINOPLE_CHURCHES = [
    ("tr-ep-constantinople-stavrodromi-presentation",
     "Church of the Presentation of the Theotokos in Stavrodromi",
     "Ἱερός Ναός Εἰσοδίων τῆς Θεοτόκου Σταυροδρομίου", "Istanbul",
     ["Panayia Rum Ortodoks Kilisesi",
      "Emir Nevruz Çıkmazı No. 24, Galatasaray-İstanbul"],
     ["+ 90-212- 244.11.84"]),
    ("tr-ep-constantinople-taksim-holy-trinity",
     "Church of the Holy Trinity in Taksim",
     "Ἱερός Ναός Ἁγίας Τριάδος Ταξείμ", "Istanbul",
     ["Aya Triada Rum Ortodoks Kilisesi",
      "Meşelik Sok. No. 11/1 Taksim / İstanbul"], ["+90-212-244.13.58"]),
    ("tr-ep-constantinople-stavrodromi-constantine-helen",
     "Church of Saints Constantine and Helen in Stavrodromi",
     "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης Σταυροδρομίου",
     "Istanbul", ["Aya Kostantin Rum Ortodoks Kilisesi",
                  "Kalyoncukulluk Cad. No. 176, Beyoğlu /İstanbul"],
     ["+ 90-212-256.86.86"]),
    ("tr-ep-constantinople-sisli-transfiguration-cemetery",
     "Cemetery Church of the Transfiguration in Sisli",
     "Κοιμητηριακός Ἱερός Ναός Θείας Μεταμορφώσεως Σισλῆ", "Istanbul",
     ["Metamorfosis Rum Ortodoks Kilisesi ve Mezarlığı",
      "Şişli / İstanbul"], ["+90-212-248.11.91"]),
    ("tr-ep-constantinople-galata-andrew",
     "Church of Saint Andrew in Galata",
     "Ἱερός Ναός Ἁγίου Ἀνδρέου Γαλατᾶ", "Istanbul",
     ["Aya Αndrea Kilisesi", "Mumhame Cad. No. 39, Karaköy/İstanbul"], []),
    ("tr-ep-constantinople-galata-panteleimon",
     "Church of Saint Panteleimon in Galata",
     "Ἱερός Ναός Ἁγίου Παντελεήμονος Γαλατᾶ", "Istanbul",
     ["Hocatahsin Cad. No. 19, Karaköy/İstanbul"], []),
    ("tr-ep-constantinople-galata-elias",
     "Church of Prophet Elias in Galata",
     "Ἱερός Ναός Προφήτου Ἠλιού Γαλατᾶ", "Istanbul",
     ["Karanlık Fırın Sok. No. 6, Karaköy/ İstanbul"], []),
    ("tr-ep-constantinople-sisli-john-rila",
     "Church of Saint John of Rila in Sisli",
     "Ἱερός Ναός Ἁγίου Ἰωάννου τῆς Ρίλας Σισλῆ", "Istanbul",
     ["Abide-i Hürriyet Cad. No. 70, 34381 Şişli/İstanbul"],
     ["+90-212-248.09.21"]),
    ("tr-ep-constantinople-tatavla-demetrius",
     "Church of Saint Demetrius in Tatavla",
     "Ἱερός Ναός Ἁγίου Δημητρίου Ταταούλων", "Istanbul",
     ["Aya Dimitri Rum Ortodoks Kilisesi",
      "Ateşböceği Sok. No. 66 Kurtuluş/ İstanbul"],
     ["+ 90-212-250.48.73", "250.62.48"]),
    ("tr-ep-constantinople-tatavla-athanasius",
     "Church of Saint Athanasius in Tatavla",
     "Ἱερός Ναός Ἁγίου Ἀθανασίου Ταταούλων", "Istanbul",
     ["Aya Tanaş Rum Ortodoks Kilisesi", "Omuzdaş Sok. Kurtuluş / İstanbul"], []),
    ("tr-ep-constantinople-tatavla-eleftherios-cemetery",
     "Cemetery Church of Saint Eleftherios in Tatavla",
     "Κοιμητηριακός Ἱερός Ναός Ἁγίου Ἐλευθερίου Ταταούλων", "Istanbul",
     ["Aya Lefter Rum Ortodoks Kilisesi",
      "Bayır Sok. No. 1 Kurtuluş/ İstanbul"], ["+90-212- 246.24.61"]),
    ("tr-ep-constantinople-dolapdere-annunciation",
     "Church of the Annunciation of the Theotokos in Dolapdere",
     "Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου", "Istanbul",
     ["Evangelistria Rum Ortodoks Kilisesi",
      "Hacı İlbey Sok. No. 6, Dolapdere / İstanbul"], ["+90-212-250.21.84"]),
    ("tr-ep-constantinople-ferikoy-twelve-apostles",
     "Church of the Twelve Apostles in Ferikoy",
     "Ἱερός Ναός Δώδεκα Ἀποστόλων Φερίκιοϊ", "Istanbul",
     ["Feriköy Oniki Apostol Rum Ortodoks Kilisesi",
      "Avukat Cad No. 41, Feriköy / İstanbul"], ["+90-212- 248.34.89"]),
    ("tr-ep-constantinople-haskoy-paraskevi",
     "Church of Saint Paraskevi in Haskoy",
     "Ἱερός Ναός Ἁγίας Παρασκευῆς Πικριδίου", "Istanbul",
     ["Aya Paraskevi Rum Ortodoks Kilisesi",
      "Bastar Sok. No. 2/1, Hasköy / İstanbul"],
     ["+90-212-250.09.10", "+90-212-250.09.11"]),
    ("tr-ep-constantinople-ferikoy-demetrius-bulgarian-cemetery",
     "Cemetery Church of Saint Demetrius in Ferikoy",
     "Κοιμητηριακός Ἱερός Ναός Ἁγίου Δημητρίου Φερίκιοϊ",
     "Istanbul", ["Feriköy / İstanbul"], []),
    ("tr-ep-constantinople-besiktas-dormition",
     "Church of the Dormition of the Theotokos in Besiktas",
     "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Διπλοκιονίου", "Istanbul",
     ["Meryem Ana Rum Ortodoks Kilisesi",
      "Köyiçi Sok. No. 44, Beşiktaş / İstanbul"], ["+90-212- 261.85.16"]),
    ("tr-ep-constantinople-besiktas-nativity-theotokos",
     "Church of the Nativity of the Theotokos in Besiktas",
     "Ἱερός Ναός Γενεθλίων τῆς Θεοτόκου Παλαιοῦ Μπάνιου",
     "Istanbul", ["Meryem Ana Cihannuma Rum Ortodoks Kilisesi",
                  "Çırağan Cad. No. 49, Beşiktaş / İstanbul"],
     ["+90-212-260.07.02"]),
    ("tr-ep-constantinople-ortakoy-phocas",
     "Church of Saint Phocas in Ortakoy",
     "Ἱερός Ναός Ἁγίου Φωκᾶ Μεσαχώρου", "Istanbul",
     ["Aya Fokas Rum Ortodoks Kilisesi",
      "Muallim Naci Cad. No. 76/1, Ortaköy / İstanbul"], ["+90-212-236.79.02"]),
    ("tr-ep-constantinople-ortakoy-george-cemetery",
     "Cemetery Church of Saint George in Ortakoy",
     "Κοιμητηριακός Ἱερός Ναός Ἁγίου Γεωργίου", "Istanbul",
     ["Aya Yorgi Mezarlığı ve Rum Ortodoks Kilisesi", "Ortaköy"], []),
    ("tr-ep-constantinople-kurucesme-demetrius",
     "Church of Saint Demetrius in Kurucesme",
     "Ἱερός Ναός Ἁγίου Δημητρίου Ξηροκρήνης", "Istanbul",
     ["Kuruçeşme Aya Dimitri Rum Ortodoks Kilisesi",
      "Kırbaş Sok. No. 52, Kuruçeşme / İstanbul"], ["+ 90-212- 257.54.03"]),
    ("tr-ep-constantinople-kurucesme-forerunner",
     "Church of Saint John the Forerunner in Kurucesme",
     "Ἱερός Ναός Ἁγίου Ἰωάννου Προδρόμου Ξηροκρήνης", "Istanbul",
     ["Aya Yani Rum Ortodoks Kilisesi",
      "Kuruçeşme Cad. 14 Kuruçeşme / İstanbul"], []),
    ("tr-ep-constantinople-arnavutkoy-archangels",
     "Church of the Archangels in Arnavutkoy",
     "Ἱερός Ναός Παμμεγίστων Ταξιαρχῶν Μεγάλου Ρεύματος", "Istanbul",
     ["Taksiarhi Rum Ortodoks Kilisesi",
      "Satış Meydanı No. 22, Arnavutköy / İstanbul"], ["+ 90-212- 263.57.44"]),
    ("tr-ep-constantinople-arnavutkoy-elias-cemetery",
     "Cemetery Church of Prophet Elias in Arnavutkoy",
     "Κοιμητηριακός Ἱερός Ναός Προφήτου Ἠλιού Μεγάλου Ρεύματος",
     "Istanbul", ["Profiti İliya Mezarlığı ve Rum Ortodoks Kilisesi",
                  "Korkadir Sok. No. 27 Arnavutköy / İstanbul"], []),
    ("tr-ep-constantinople-bebek-charalambos",
     "Church of Saint Charalambos in Bebek",
     "Ἱερός Ναός Ἁγίου Χαραλάμπους Βεβεκίου", "Istanbul",
     ["Aya Haralambos Rum Ortodoks Kilisesi",
      "İnşirah Sok. No. 15 A, Bebek/ İstanbul"],
     ["+90-212-265.03.19", "263.52.99"]),
    ("tr-ep-constantinople-boyacikoy-annunciation",
     "Church of the Annunciation of the Theotokos in Boyacikoy",
     "Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου Βαφεοχωρίου", "Istanbul",
     ["Panayia Evangelistria Rum Ortodoks Kilisesi",
      "Fırın Sok. No. 7, Boyacıköy / İstanbul"], ["+ 90-212-277.65.19"]),
    ("tr-ep-constantinople-istinye-archangels",
     "Church of the Archangels in Istinye",
     "Ἱερός Ναός Παμμεγίστων Ταξιαρχῶν Σωσθενίου", "Istanbul",
     ["Aya Strati (Taksiarhi) Rum Ortodoks Kilisesi",
      "Çapari Sok. No. 18, İstinye / İstanbul"], ["+ 90-212- 263.68.60"]),
    ("tr-ep-constantinople-yenikoy-nicholas",
     "Church of Saint Nicholas in Yenikoy",
     "Ἱερός Ναός Ἁγίου Νικολάου Νεοχωρίου", "Istanbul",
     ["Aya Nikola Rum Ortodoks Kilisesi",
      "Hamit Vehbi Sok. No. 14, Yeniköy/ İstanbul"], ["+90-212-262.46.38"]),
    ("tr-ep-constantinople-yenikoy-dormition-koumariotissa",
     "Church of the Dormition of the Theotokos Koumariotissa in Yenikoy",
     "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Κουμαριωτίσσης Νεοχωρίου",
     "Istanbul", ["Panayia Rum Ortodoks Kilisesi",
                  "Köybaşı Cad. No. 108, Yeniköy / İstanbul"],
     ["+ 90-212-262.35.74", "262.38.73", "262.38.21"]),
]

CONSTANTINOPLE_CHURCHES.extend([
    ("tr-ep-constantinople-vlanga-theodore",
     "Church of Saints Theodore in Vlanga",
     "Ἱερός Ναός Ἁγίων Θεοδώρων Βλάγκας", "Istanbul",
     ["Aya Todori Rum Ortodoks Kilisesi",
      "Ηayriye Tüccarı Cad. No. 4-6, Büyük Lânga - Aksaray / İstanbul"],
     ["+90-212- 516.78.08"]),
    ("tr-ep-constantinople-kumkapi-kyriaki",
     "Church of Saint Kyriaki in Kumkapi",
     "Ἱερός Ναός Ἁγίας Κυριακῆς Κοντοσκαλίου", "Istanbul",
     ["Aya Kiryaki Rum Ortodoks Kilisesi",
      "Kadırga Limanı Cad. No. 15, Kumkapı / İstanbul"], ["+90-212- 517.18.58"]),
    ("tr-ep-constantinople-kumkapi-panagia-elpis",
     "Church of Panagia Elpis in Kumkapi",
     "Ἱερός Ναός Παναγίας Ἐλπίδος Κοντοσκαλίου", "Istanbul",
     ["Panayia Elpida Rum Ortodoks Kilisesi",
      "Gerdanlık Sok. No. 4, Kumkapı / İstanbul"], ["+90-212-638.81.36"]),
    ("tr-ep-constantinople-kocamustafapasa-menas",
     "Church of Saint Menas in Koca Mustafa Pasa",
     "Ἱερός Ναός Ἁγίου Μηνᾶ Ὑψωμαθείων", "Istanbul",
     ["Aya Mina Rum Ortodoks Kilisesi",
      "Bestekâr Hakkı Sok. No. 1. Koca Mustafa Paşa/ İstanbul"],
     ["+90-212-586.16.50"]),
    ("tr-ep-constantinople-kocamustafapasa-ascension",
     "Church of the Ascension in Koca Mustafa Pasa",
     "Ἱερός Ναός Ἀναλήψεως Ὑψωμαθείων", "Istanbul",
     ["Analipsis Rum Ortodoks Kilisesi",
      "Akıncı Sok. No. 7, Koca Mustafa Paşa/ İstanbul"], ["+90-212-530.31.57"]),
    ("tr-ep-constantinople-kocamustafapasa-nicholas",
     "Church of Saint Nicholas in Koca Mustafa Pasa",
     "Ἱερός Ναός Ἁγίου Νικολάου Ὑψωμαθείων", "Istanbul",
     ["Aya Nikola Rum Ortodoks Kilisesi",
      "Muallim Fevzi Sok. No. 3, Koca Mustafa Paşa/İstanbul"], []),
    ("tr-ep-constantinople-kocamustafapasa-george-kyparissas",
     "Church of Saint George Kyparissas in Koca Mustafa Pasa",
     "Ἱερός Ναός Ἁγίου Γεωργίου Κυπαρισσᾶ Ὑψωμαθείων", "Istanbul",
     ["Aya Yorgi Kiparisa Rum Ortodoks Kilisesi",
      "Org. A. Nafiz Gürman Cad. No. 247, Koca Mustafa Paşa/İstanbul"], []),
    ("tr-ep-constantinople-yedikule-constantine-helen",
     "Church of Saints Constantine and Helen in Yedikule",
     "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης Ὑψωμαθείων",
     "Istanbul", ["Aya Kostantin Rum Ortodoks Kilisesi",
                  "İmrahor İlyas Bey Cad No. 45, Yedikule/İstanbul"],
     ["+ 90-212-586.12.46"]),
    ("tr-ep-constantinople-topkapi-nicholas",
     "Church of Saint Nicholas in Topkapi",
     "Ἱερός Ναός Ἁγίου Νικολάου Τοπκαπίου", "Istanbul",
     ["Aya Nikola Rum Ortodoks Kilisesi",
      "Karatay Sok. No. 1, Topkapı/İstanbul"], ["+90-212-525.03.79"]),
    ("tr-ep-constantinople-altimermer-dormition",
     "Church of the Dormition of the Theotokos in Altimermer",
     "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Ἕξ Μαρμάρων", "Istanbul",
     ["Altı Mermer Panayia Rum Ortodoks Kilisesi",
      "Hekimoğu Ali Paşa Cad.,Yapağı Sok. No. 5, Şehremini/İstanbul"],
     ["+ 90-212-586.47.00"]),
    ("tr-ep-constantinople-belgradkapi-nativity-theotokos",
     "Church of the Nativity of the Theotokos at Belgrad Gate",
     "Ἱερός Ναός Γενεθλίων τῆς Θεοτόκου Πύλης Βελιγραδίου",
     "Istanbul", ["Belgratkapı Panayia Rum Ortodoks Kilisesi",
                  "Hacı Hamza Mektebi Sok. No. 61, Belgratkapı/İstanbul"],
     ["+ 90-212-529.05.20"]),
    ("tr-ep-constantinople-fener-dormition-mouhlion",
     "Church of the Dormition of the Theotokos in Mouhlion",
     "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Μουχλίου", "Istanbul",
     ["Meryem Ana Rum Ortodoks Kilisesi",
      "Tevkii Cafer Mah. Firketeci Sok. No. 5, Fener/Ha1iç/İstanbul"],
     ["+90-212-521.71.39"]),
    ("tr-ep-constantinople-cibali-nicholas",
     "Church of Saint Nicholas in Cibali",
     "Ἱερός Ναός Ἁγίου Νικολάου Τζιβαλίου", "Istanbul",
     ["Cibali Aya Nikola Rum Ortodoks Kilisesi",
      "Abdüllezel Paşa Cad. No. 255, Cibali/İstanbul"], ["+ 90-212-521.26.02"]),
    ("tr-ep-constantinople-fener-george-potiras",
     "Church of Saint George Potiras Antiphonetes in Phanar",
     "Ἱερός Ναός Ἁγίου Γεωργίου Ποτηρᾶ Ἀντιφωνητοῦ", "Istanbul",
     ["Aya Yorgi Potira Rum Ortodoks Kilisesi",
      "Murat Molla Sok. No. 39, Fener/Ha1iç/İstanbul"], []),
    ("tr-ep-constantinople-edirnekapi-george",
     "Church of Saint George at Edirne Gate",
     "Ἱερός Ναός Ἁγίου Γεωργίου Πύλης Ἀδριανουπόλεως", "Istanbul",
     ["Aya Yorgi Rum Ortodoks Kilisesi (Hıdır İlyas)",
      "Hoca Şakir Sok. No. 8, Edirnekapı/İstanbul"],
     ["+90-212-523.23.71", "523.43.28"]),
    ("tr-ep-constantinople-karagumruk-demetrius",
     "Church of Saint Demetrius in Karagumruk",
     "Ἱερός Ναός Ἁγίου Δημητρίου Σαρμασικίου", "Istanbul",
     ["Aya Dimitri Sarmaşık Rum Ortodoks Kilisesi",
      "Profesör Naci Sensağ Cad. No. 93, Karagümrük/İstanbul"], []),
    ("tr-ep-constantinople-balat-archangels",
     "Church of the Archangels in Balat",
     "Ἱερός Ναός Παμμεγίστων Ταξιαρχῶν Βαλατᾶ", "Istanbul",
     ["Aya Strati Rum Ortodoks Kilisesi",
      "Ayan Cad No. 25, Balat/Haliç/ İstanbul"], ["+90-212-631.88.73"]),
    ("tr-ep-constantinople-ayvansaray-dormition-valino",
     "Church of the Dormition of the Theotokos in Valino",
     "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου Βαλινοῦ", "Istanbul",
     ["Panayia Balino Rum Ortodoks Kilisesi",
      "Mahkeme Altı Sok. No. 38, Ayvansaray/Haliç/İstanbul"],
     ["+90- 212-534.56.04"]),
    ("tr-ep-constantinople-ayvansaray-demetrius",
     "Church of Saint Demetrius at Xyloporta",
     "Ἱερός Ναός Ἁγίου Δημητρίου Ξυλοπόρτης", "Istanbul",
     ["Aya Dimitri Rum Ortodoks Kilisesi",
      "Kırk Ambar Sok. No. 12, Ayvansaray/Haliç/İstanbul"],
     ["+90-212-521.35.83"]),
    ("tr-ep-constantinople-blachernae-life-giving-spring",
     "Church of the Life-Giving Spring of the Theotokos at Blachernae",
     "Ἱερός Ναός Ζωοδόχου Πηγῆς Παναγίας Βλαχερνῶν", "Istanbul",
     ["Aya Vlaherna Ayazması ve Panayia Rum Ortodoks Kilisesi",
      "Bostan Sok. No. 47, Ayvansaray/Haliç/İstanbul"], ["+90-212-523.22.94"]),
    ("tr-ep-constantinople-salmatomvruk-panagia-heavens",
     "Church of Panagia of the Heavens in Salmatomvruk",
     "Ἱερός Ναός Παναγίας τῶν Οὐρανῶν Σαλματομβρουκίου", "Istanbul",
     ["Salmatobruk Panayia Rum Ortodoks Kilisesi",
      "Neşter Sok. No. 14, Salmatobruk/Edirnekapı/İstanbul"],
     ["+90-212-533.36.84"]),
    ("tr-ep-constantinople-tekfursaray-panagia-hantzeriotissa",
     "Church of Panagia Hantzeriotissa in Tekfursaray",
     "Ἱερός Ναός Παναγίας Χαντζεριωτίσσης Τεκφούρσαραϊ", "Istanbul",
     ["Tekfursaray Panayia Hançerli Rum Ortodoks Kilisesi",
      "Ulubatlı Hasan Sok. No. 24, Edirnekapı/İstanbul"],
     ["+90-212-525.37.50"]),
    ("tr-ep-constantinople-egrikapi-panagia-souda",
     "Church of Panagia Souda in Egrikapi",
     "Ἱερός Ναός Παναγίας Σούδας Ἐγρίκαπου", "Istanbul",
     ["Panayia Suda Rum Ortodoks Kilisesi",
      "Tandır Sok. No. 3, Eğrikapı/İstanbul"], ["+90-212-521.15.48"]),
    ("tr-ep-constantinople-egrikapi-kyriakos-cemetery",
     "Cemetery Church of Saint Kyriakos in Egrikapi",
     "Κοιμητηριακός Ἱερός Ναός Ἁγίου Κυριακοῦ Ἐγρίκαπου", "Istanbul",
     ["Aya Kiryakos Mezarlığı ve Rum Ortodoks Kilisesi",
      "Savanlar Cad., Eğrikapı/İstanbul"], []),
    ("tr-ep-constantinople-balat-stephen-bulgarian",
     "Church of Saint Stephen in Balat",
     "Ἱερός Ναός Ἁγίου Στεφάνου Βαλατᾶ", "Istanbul",
     ["Mürselpaşa Cad. No. 70, Balat/Fatih/İstanbul"], []),
])

CONSTANTINOPLE_MONASTERIES = [
    ("tr-ep-constantinople-baliki-life-giving-spring",
     "Monastery of the Life-Giving Spring in Balikli",
     "Ἱερά Μονή Ζωοδόχου Πηγῆς Βαλουκλῆ", "Istanbul",
     ["Balıklı Meryem Ana Rum Ortodoks Manastırı",
      "Silivri Kapı Yolu No. 3, Zeytinburnu, İstanbul, Türkiye"],
     ["+90-212-510.42.43"]),
    ("tr-ep-constantinople-halki-holy-trinity",
     "Monastery of the Holy Trinity on Halki",
     "Ἱερά Μονή Ἁγίας Τριάδος Χάλκης", "Halki",
     ["AyaTriada Rum Ortodoks Manastırı Heybeliada",
      "Ümit Tepesi No. 3, 81340 Heybeliada/İstanbul"], ["+90-216-351.85.63"]),
    ("tr-ep-constantinople-halki-spyridon",
     "Monastery of Saint Spyridon on Halki",
     "Ἱερά Μονή Ἁγίου Σπυρίδωνος Χάλκης", "Halki",
     ["Aya Spiridon Rum Ortodoks Manastırı",
      "Heybeliada Arsenios Namı (Terki Dünya)"], ["+90-216-351.89.00"]),
    ("tr-ep-constantinople-halki-transfiguration",
     "Monastery of the Transfiguration on Halki",
     "Ἱερά Μονή Μεταμορφώσεως τοῦ Σωτῆρος Χάλκης", "Halki",
     ["Hristos Rum Ortodoks Manastırı Heybeliada",
      "Bahriye Mevki, İsa Tepesi, Heybeliada/İstanbul"], []),
    ("tr-ep-constantinople-buyukada-transfiguration",
     "Monastery of the Transfiguration on Buyukada",
     "Ἱερά Μονή Μεταμορφώσεως τοῦ Σωτῆρος Πριγκήπου", "Buyukada",
     ["Hristos Rum Ortodoks Manastırı, Büyükada",
      "Büyükada Maden Mevki, İsa Tepesi/İstanbul"], ["+ 90-216- 382.66.37"]),
    ("tr-ep-constantinople-buyukada-nicholas",
     "Monastery of Saint Nicholas on Buyukada",
     "Ἱερά Μονή Ἁγίου Νικολάου Πριγκήπου", "Buyukada",
     ["Aya Nikola Rum Ortodoks Manastırı Büyükada",
      "Büyükada Selvili Batmış Mevkii, Büyükada/İstanbul"],
     ["+90-216-382.61.12"]),
    ("tr-ep-constantinople-buyukada-george-koudounas",
     "Monastery of Saint George Koudounas on Buyukada",
     "Ἱερά Μονή Ἁγίου Γεωργίου Κουδουνᾶ Πριγκήπου", "Buyukada",
     ["Aya Yorgi Kuduna Rum Ortodoks Manastırı Büyükada",
      "Yücetepe Mevkii, Büyükada/İstanbul"], ["+ 90-216-382.39.39"]),
    ("tr-ep-constantinople-burgazada-transfiguration",
     "Monastery of the Transfiguration on Burgazada",
     "Ἱερά Μονή Μεταμορφώσεως τοῦ Σωτῆρος Ἀντιγόνης", "Burgazada",
     ["Hristos Rum Ortodoks Manastırı Burgazada",
      "Tepe Mevkii, Burgazada/İstanbul"], []),
    ("tr-ep-constantinople-burgazada-george-karypis",
     "Monastery of Saint George Karypis on Burgazada",
     "Ἱερά Μονή Ἁγίου Γεωργίου Καρύπη Ἀντιγόνης", "Burgazada",
     ["Aya Yorgi Karipi Rum Ortodoks Manastırı, Burgazada",
      "Gönüllü Cad. Burgazada/İstanbul"], []),
    ("tr-ep-constantinople-kinaliada-transfiguration-convent",
     "Women's Monastery of the Transfiguration on Kinaliada",
     "Γυναικεία Ἱερά Μονή Μεταμορφώσεως τοῦ Σωτῆρος Πρώτης", "Kinaliada",
     ["Hristos Rum Ortodoks Manastırı Kınalıada",
      "Tepe Mah. Μanastır Sok. No. 23, Kınalıada/İstanbul"],
     ["+90-216-381.43.65", "381.43.66"]),
]

CHALCEDON = [
    ep("tr-ep-chalcedon-euphemia-metropolitan", "ep-chalcedon",
       "Metropolitan Church of Saint Euphemia in Chalcedon",
       "Μητροπολιτικός Ἱερός Ναός Ἁγίας Εὐφημίας", "Istanbul",
       EP_CHALCEDON, "Metropolitan Church",
       address=["Yasa Cad. No 27, Kadıköy, İstanbul"],
       phones=["+90-216-336.14.97", "414.66.58"]),
    ep("tr-ep-chalcedon-holy-trinity-cathedral", "ep-chalcedon",
       "Cathedral of the Holy Trinity in Chalcedon",
       "Καθεδρικός Ἱερός Ναός Ἁγίας Τριάδος", "Istanbul", EP_CHALCEDON,
       "Cathedral", address=["Bahariye Cad., Hacı Sükrü Sok. No 17",
                             "Kadıköy, İstanbul"],
       emails=["cathedralchalcedon@gmail.com"], phones=["+90-216-347.10.55"]),
    ep("tr-ep-chalcedon-kalamis-john-chrysostom", "ep-chalcedon",
       "Church of Saint John Chrysostom in Kalamis",
       "Ἱερός Ναός Ἁγίου Ἰωάννου Χρυσοστόμου Καλαμησίων", "Istanbul",
       EP_CHALCEDON, address=["İskele Sok. No 30, Kalamış, İstanbul"],
       phones=["+90-216-348.20.11"]),
    ep("tr-ep-chalcedon-yeldegirmen-george", "ep-chalcedon",
       "Church of Saint George in Yeldegirmen",
       "Ἱερός Ναός Ἁγίου Γεωργίου Γέλδεγιρμεν", "Istanbul", EP_CHALCEDON,
       address=["Karakol Hane Cad. No 60, Yeldeğirmen, İstanbul"],
       phones=["+90-216-336.36.93"]),
    ep("tr-ep-chalcedon-uzuncayir-ignatius-cemetery", "ep-chalcedon",
       "Cemetery Church of Saint Ignatius in Uzun Cayir",
       "Κοιμητηριακός Ἱερός Ναός Ἁγίου Ἰγνατίου Μακροῦ Λειμῶνος",
       "Istanbul", EP_CHALCEDON, "Cemetery Church",
       address=["Hasan Paşa Uzun Çayır Taş Ocak Sok. No 2, İstanbul"],
       phones=["+90-216-428.04.10"]),
    ep("tr-ep-chalcedon-uskudar-elias", "ep-chalcedon",
       "Church of Prophet Elias in Uskudar",
       "Ἱερός Ναός Προφήτου Ἠλιού Χρυσοπόλεως", "Istanbul", EP_CHALCEDON,
       address=["Hacı Murat Sok. No 10, Yenimahalle, Üsküdar, İstanbul"],
       phones=["+90-216-492.81.62", "492.66.52"]),
    ep("tr-ep-chalcedon-kuzguncuk-panteleimon", "ep-chalcedon",
       "Church of Saint Panteleimon in Kuzguncuk",
       "Ἱερός Ναός Ἁγίου Παντελεήμονος Κουσκουντζουκίου", "Istanbul",
       EP_CHALCEDON, address=["İcadiye Cad. No 80, Kuzguncuk, İstanbul"],
       phones=["+90-216-553.07.43"]),
    ep("tr-ep-chalcedon-kuzguncuk-george", "ep-chalcedon",
       "Church of Saint George in Kuzguncuk",
       "Ἱερός Ναός Ἁγίου Γεωργίου Κουσκουντζουκίου", "Istanbul",
       EP_CHALCEDON, address=["İcadiye Cad. No 19, Kuzguncuk, İstanbul"],
       phones=["+90-216-343.22.51"]),
    ep("tr-ep-chalcedon-cengelkoy-george", "ep-chalcedon",
       "Church of Saint George Chrysokeramos in Cengelkoy",
       "Ἱερός Ναός Ἁγίου Γεωργίου Χρυσοκεράμου", "Istanbul", EP_CHALCEDON,
       address=["Tanrıverdi Sok. No 28, Çengelköy, İstanbul"],
       phones=["+90-216-422.03.70"]),
    ep("tr-ep-chalcedon-kandilli-transfiguration", "ep-chalcedon",
       "Church of the Transfiguration in Kandilli",
       "Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος Κανδυλλίου", "Istanbul",
       EP_CHALCEDON, address=["Bahçe Sok. No 6, Kandilli, İstanbul"],
       phones=["+90-216-332.02.38"]),
    ep("tr-ep-chalcedon-pasabahce-constantine-helen", "ep-chalcedon",
       "Church of Saints Constantine and Helen in Pasabahce",
       "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης Πασάμπαχτσε",
       "Istanbul", EP_CHALCEDON,
       address=["Çağatay Sok. No 9, Paşabahçe, İstanbul"]),
    ep("tr-ep-chalcedon-beykoz-paraskevi", "ep-chalcedon",
       "Church of Saint Paraskevi in Beykoz",
       "Ἱερός Ναός Ἁγίας Παρασκευῆς Βεϊκόζ", "Istanbul", EP_CHALCEDON,
       address=["Panayır Sok. No 30, Beykoz, İstanbul"],
       phones=["+90-216-323.98.15"]),
]

DERKOI = [
    ep("tr-ep-derkoi-tarabya-paraskevi-metropolitan", "ep-derkoi",
       "Metropolitan Church of Saint Paraskevi in Tarabya",
       "Ἱερός Mητροπολιτικός Ναός Ἁγίας Παρασκευῆς Θεραπείων",
       "Istanbul", EP_DERKOI, "Metropolitan Church",
       address=["Yeniköy Cad. No. 64-68, 80880 Tarabya, İstanbul"],
       phones=["+90-212-262.00.28"]),
    ep("tr-ep-derkoi-buyukdere-paraskevi", "ep-derkoi",
       "Church of Saint Paraskevi in Buyukdere",
       "Ἱερός Ναός Ἁγίας Παρασκευῆς Βαθυρρύακος", "Istanbul", EP_DERKOI,
       address=["Danişment Sok. No. 5, 80890 Büyükdere, İstanbul"],
       phones=["+90-535-945.78.44"]),
    ep("tr-ep-derkoi-yenimahalle-forerunner", "ep-derkoi",
       "Church of the Nativity of Saint John the Forerunner in Yenimahalle",
       "Ἱερός Ναός Γενεθλίου Ἁγίου Ἰωάννου Προδρόμου Γενῆ Μαχαλλέ",
       "Istanbul", EP_DERKOI,
       address=["İbni Sina Sok. No. 6, 80900 Yeni Mahalle, Sarıyer, İstanbul"],
       phones=["+90-212-242.25.69"]),
    ep("tr-ep-derkoi-bakirkoy-george", "ep-derkoi",
       "Church of Saint George in Bakirkoy",
       "Ἱερός Ναός Ἁγίου Γεωργίου Μακροχωρίου", "Istanbul", EP_DERKOI,
       address=["Ebuziyya Cad. 15, 34720 Bakırköy, İstanbul"],
       phones=["+90-212-571.60.13", "543.95.47"]),
    ep("tr-ep-derkoi-yesilkoy-stephen", "ep-derkoi",
       "Church of Saint Stephen in Yesilkoy",
       "Ἱερός Ναός Ἁγίου Στεφάνου Γεσήλκιοϊ", "Istanbul", EP_DERKOI,
       address=["Mirasyedi Sok. No 9, 348 00 Yeşilköy, İstanbul"],
       phones=["+90-212-542.70.98"]),
    ep("tr-ep-derkoi-bakirkoy-ascension-cemetery", "ep-derkoi",
       "Cemetery Church of the Ascension in Bakirkoy",
       "Κοιμητηριακός Ἱερός Ναός Ἀναλήψεως Μακροχωρίου", "Istanbul",
       EP_DERKOI, "Cemetery Church", phones=["+90.537.407.44.58"]),
    ep("tr-ep-derkoi-buyukdere-george-cemetery", "ep-derkoi",
       "Cemetery Church of Saint George in Buyukdere",
       "Κοιμητηριακός Ἱερός Ναός Ἁγίου Γεωργίου Βαθυρρύακος", "Istanbul",
       EP_DERKOI, "Cemetery Church", phones=["+90.212.271.68.82"]),
    ep("tr-ep-derkoi-tarabya-helen-cemetery", "ep-derkoi",
       "Cemetery Church of Saint Helen in Tarabya",
       "Κοιμητηριακός Ἱερός Ναός Ἁγίας Ἑλένης Θεραπείων", "Istanbul",
       EP_DERKOI, "Cemetery Church", phones=["+90.535.476.71.72"]),
]

PRINCES = [
    ep("tr-ep-princes-buyukada-demetrius-metropolitan", "ep-princes-islands",
       "Metropolitan Church of Saint Demetrius on Buyukada",
       "Μητροπολιτικός Ἱερός Ναός Ἁγίου Δημητρίου Πριγκήπου", "Buyukada",
       EP_PRINCES, "Metropolitan Church", address=["Alacam Sok. No. 15"]),
    ep("tr-ep-princes-buyukada-panagia-eleousa-cathedral",
       "ep-princes-islands", "Cathedral of Panagia Eleousa on Buyukada",
       "Καθεδρικός Ἱερός Ναός Παναγίας Ἐλεούσης Πριγκήπου", "Buyukada",
       EP_PRINCES, "Cathedral", address=["Kıvılcım Sok. No. 3"],
       phones=["+90.537.986.47.34"]),
    ep("tr-ep-princes-buyukada-elias-cemetery", "ep-princes-islands",
       "Cemetery Church of Prophet Elias on Buyukada",
       "Κοιμητηριακός Ἱερός Ναός Προφήτου Ἠλιού Πριγκήπου", "Buyukada",
       EP_PRINCES, "Cemetery Church", address=["Karacebey Mevkii"],
       phones=["+90.536.471.28.59"]),
    ep("tr-ep-princes-buyukada-theodore-chapel", "ep-princes-islands",
       "Chapel of Saints Theodore on Buyukada",
       "Παρεκκλήσιον Ἁγίων Θεοδώρων Πριγκήπου", "Buyukada", EP_PRINCES,
       "Chapel", address=["Yılmaztürk Cad. 25, Maden Mah."],
       phones=["+90.535.523.16.44"]),
    ep("tr-ep-princes-halki-nicholas", "ep-princes-islands",
       "Church of Saint Nicholas on Halki", "Ἱερός Ναός Ἁγίου Νικολάου Χάλκης",
       "Halki", EP_PRINCES, address=["İşgüzar Cad. No. 10"],
       phones=["+90.216.351.05.06", "+90.216.351.94.03", "+90.530.511.43.36"]),
    ep("tr-ep-princes-halki-barbara-cemetery", "ep-princes-islands",
       "Cemetery Church of Saint Barbara on Halki",
       "Κοιμητηριακός Ἱερός Ναός Ἁγίας Βαρβάρας Χάλκης", "Halki",
       EP_PRINCES, "Cemetery Church", address=["Mezarlık Sok. No. 7/9"]),
    ep("tr-ep-princes-burgazada-forerunner", "ep-princes-islands",
       "Church of Saint John the Forerunner on Burgazada",
       "Ἱερός Ναός Ἁγίου Ἰωάννου Προδρόμου Ἀντιγόνης", "Burgazada",
       EP_PRINCES, address=["Takım Ağa Sok. No. 19"],
       phones=["+90.216.381.13.09", "+90.216.381.14.01", "+90.532.612.54.16"]),
    ep("tr-ep-princes-burgazada-elias-cemetery", "ep-princes-islands",
       "Cemetery Church of Prophet Elias on Burgazada",
       "Κοιμητηριακός Ἱερός Ναός Προφήτου Ἠλιού Ἀντιγόνης", "Burgazada",
       EP_PRINCES, "Cemetery Church", address=["İsa Tepesi"],
       phones=["+90.538.414.55.10"]),
    ep("tr-ep-princes-kinaliada-nativity-theotokos", "ep-princes-islands",
       "Church of the Nativity of the Theotokos on Kinaliada",
       "Ἱερός Ναός Γενεθλίων τῆς Θεοτόκου Πρώτης", "Kinaliada", EP_PRINCES,
       address=["Beşiroğlu Sok. No 6"],
       phones=["+90.216.381.41.43", "+90.532.764.64.51"]),
]

PISIDIA = [
    ep("tr-ep-pisidia-antalya-alypius", "ep-pisidia",
       "Church of Saint Alypius the Stylite in Antalya",
       "Ἱερός Ναός Ὁσίου Ἀλυπίου τοῦ Κιονίτου", "Antalya", EP_PISIDIA,
       address=["Kılınçarslan Mah., Yenıkapı Sok. No: 20",
                "07100 Kaleiçi, Muratpaşa-Antalya. Türkiye"]),
    ep("tr-ep-pisidia-alanya-panagia-pisidiotissa", "ep-pisidia",
       "Church of Panagia Pisidiotissa in Alanya",
       "Ἱερός Ναός Παναγίας Πισιδιωτίσσης", "Alanya", EP_PISIDIA,
       address=["Mahmutlar Yukarı Mah., Kılınçarslan Cad. 158-1",
                "07450 Mahmutlar, Alanya-Antalya. Türkiye"]),
    ep("tr-ep-pisidia-side-paul", "ep-pisidia",
       "Church of the Holy Apostle Paul in Side",
       "Ἱερός Ναός Ἁγίου Ἀποστόλου Παύλου", "Side", EP_PISIDIA,
       address=["Sorkun Mah., 8131 Sok.",
                "07600 Sorkun, Manavgat-Antalya. Türkiye"]),
    ep("tr-ep-pisidia-alanya-george-country-chapel", "ep-pisidia",
       "Country Chapel of Saint George near Alanya",
       "Ἐξωκκλήσιον Ἁγίου Γεωργίου", "Alanya", EP_PISIDIA,
       "Wayside Chapel", address=["HİDİRELLEZ KİLİSESİ",
                                  "Hacı Mehmetli, Alanya-Antalya. Türkiye"]),
]

VRYOULA = [
    ep("tr-ep-vryoula-house-chapel", "ep-vryoula",
       "House Chapel of Panagia of Vryoula and New Martyrs Nektarios and Michael",
       "Παρεκκλήσιον Παναγίας Βρυούλων καί Νεομαρτύρων Νεκταρίου καί Μιχαήλ",
       "Urla", EP_VRYOULA, "House Chapel",
       address=["Atatürk Mah., 2224 Sok. No. 13",
                "İskele Urla, İzmir, Türkiye"]),
]

SELYBRIA = [
    ep("tr-ep-selybria-house-chapel", "ep-selybria",
       "House Chapel of Panagia Selybriani and Saint Nektarios",
       "Παρεκκλήσιον Παναγίας Σηλυβριανῆς καί Ἁγίου Νεκταρίου",
       "Silivri", EP_SELYBRIA, "House Chapel",
       address=["Fatih Mah., Ramazan Sezginer Sok. No: 5",
                "34570 Silivri, İstanbul Türkiye"]),
]

ADRIANOPLE = [
    ep("tr-ep-adrianople-edirne-george", "ep-adrianople",
       "Church of Saint George the Great Martyr in Edirne",
       "Ἱερός Ναός Ἁγίου Μεγαλομάρτυρος Γεωργίου", "Edirne",
       EP_ADRIANOPLE, address=["Barutluk Mah., Sv. Georgi Kilisesi Sok. No. 5",
                              "Merkez, Edirne, Türkiye"],
       phones=["+90-284-214.06.48"]),
    ep("tr-ep-adrianople-edirne-constantine-helen", "ep-adrianople",
       "Church of Saints Constantine and Helen in Edirne",
       "Ἱερός Ναός Ἁγίων Κωνσταντίνου καί Ἑλένης", "Edirne",
       EP_ADRIANOPLE, address=["Abdurrahman Mah., Çağlar Sok. No. 14",
                              "Kirişhane, Edirne, Türkiye"],
       phones=["+90-284-214.77.44"], extra_sources=[BULGARIAN_SITES]),
]

SMYRNA = [
    ep("tr-ep-smyrna-dormition-cathedral", "ep-smyrna",
       "Cathedral of the Dormition of the Theotokos in Izmir",
       "Καθεδρικός Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου", "Izmir",
       EP_SMYRNA, "Cathedral",
       address=["AkDeniz, Halit Ziya Blvı No. 67",
                "35210, Konak, İzmir, Türkiye"]),
    ep("tr-ep-smyrna-photini-samaritan", "ep-smyrna",
       "Church of Saint Photini the Samaritan in Izmir",
       "Ἱερός Ναός Ἁγίας Φωτεινῆς τῆς Σαμαρείτιδος", "Izmir", EP_SMYRNA,
       address=["Sezer Doğan Sok. (1374) No: 24/1 Alsancak",
                "35210 Konak/İzmir, Türkiye"]),
]

GANOS = [
    ep("tr-ep-ganos-sarkoy-amphilochios-house-chapel", "ep-ganos-chora",
       "House Chapel of Saint Amphilochios of Patmos in Sarkoy",
       "Παρεκκλήσιον Ἁγίου Ἀμφιλοχίου Πάτμου", "Sarkoy", EP_GANOS,
       "House Chapel", address=["Hoşköy Mah., Tekel Cad. No. 17",
                                "59570 Şarköy-Tekirdağ. Türkiye"]),
    ep("tr-ep-ganos-sarkoy-john-theologian-convent", "ep-ganos-chora",
       "Women's Monastery of Saint John the Theologian in Sarkoy",
       "Γυναικεία Ἱερά Μονή Ἁγίου Ἰωάννου τοῦ Θεολόγου", "Sarkoy",
       EP_GANOS, "Monastery", "monastery"),
]


def ib(row_id, name, local, seat, rank="Church", kind="parish",
       address=None, phones=None, parent="ep-imbros-tenedos"):
    return ep(row_id, parent, name, local, seat, EP_IMBROS, rank, kind,
              address=address, phones=phones)


IMBROS = [
    ib("tr-ep-imbros-cinarli-dormition-metropolitan",
       "Metropolitan Church of the Dormition of the Theotokos in Cinarli",
       "Μητροπολιτικός Ναός Κοιμήσεως τῆς Θεοτόκου", "Gokceada",
       "Metropolitan Church", address=["Çınarlı-Merkez",
       "17760 Gökçeada-Çanakkale"], phones=["+90.286.887.2806"]),
    ib("tr-ep-imbros-cinarli-archangels-frantzi",
       "Chapel of the Archangels at Frantzi",
       "Παρεκκλήσιον Παμμεγίστων Ταξιαρχῶν (Φραντζῆ)", "Gokceada", "Chapel"),
    ib("tr-ep-imbros-cinarli-panagia-taxeidiani",
       "Chapel of Panagia Taxeidiani",
       "Παρεκκλήσιον Παναγίας Ταξειδιανῆς", "Gokceada", "Chapel"),
    ib("tr-ep-imbros-cinarli-unmercenaries",
       "Chapel of the Holy Unmercenaries in Cinarli",
       "Παρεκκλήσιον τῶν Ἁγίων Ἀναργύρων μεθ' Ἁγιάσματος", "Gokceada",
       "Chapel"),
]


def add_wayside(target, prefix, seat, specs):
    for slug, name, local in specs:
        target.append(ib(prefix + slug, name, local, seat, "Wayside Chapel"))


add_wayside(IMBROS, "tr-ep-imbros-cinarli-", "Gokceada", [
    ("presentation-kokkina", "Country Chapel of the Presentation of the Lord at Kokkina",
     "Ἐξωκκλήσιον Ὑπαπαντῆς τοῦ Κυρίου (Θεοτόκου) Κόκκινα"),
    ("dormition", "Country Chapel of the Dormition of the Theotokos near Cinarli",
     "Ἐξωκκλήσιον Κοιμήσεως Θεοτόκου"),
    ("symeon", "Country Chapel of Saint Symeon near Cinarli", "Ἐξωκκλήσιον Ἁγίου Συμεών"),
    ("athanasius", "Country Chapel of Saint Athanasius near Cinarli", "Ἐξωκκλήσιον Ἁγίου Ἀθανασίου"),
    ("constantine-helen", "Country Chapel of Saints Constantine and Helen near Cinarli",
     "Ἐξωκκλήσιον Ἁγίων Κωνσταντίνου καί Ἑλένης"),
    ("nicholas", "Country Chapel of Saint Nicholas near Cinarli", "Ἐξωκκλήσιον Ἁγίου Νικολάου"),
    ("anastasia", "Country Chapel of Saint Anastasia near Cinarli", "Ἐξωκκλήσιον Ἁγίας Ἀναστασίας"),
    ("george", "Country Chapel of Saint George near Cinarli", "Ἐξωκκλήσιον Ἁγίου Γεωργίου"),
    ("demetrius", "Country Chapel of Saint Demetrius near Cinarli", "Ἐξωκκλήσιον Ἁγίου Δημητρίου"),
    ("helen", "Country Chapel of Saint Helen near Cinarli", "Ἐξωκκλήσιον Ἁγίας Ἑλένης"),
    ("christopher", "Country Chapel of Saint Christopher near Cinarli", "Ἐξωκκλήσιον Ἁγίου Χριστοφόρου"),
])

IMBROS.extend([
    ib("tr-ep-imbros-zeytinlikoy-george", "Church of Saint George the Great Martyr in Zeytinlikoy",
       "Ἱερός Ναός τοῦ Ἁγίου Μεγαλομάρτυρος Γεωργίου τοῦ Τροπαιοφόρου",
       "Zeytinlikoy", address=["Zeytinliköy, 17760 Gökçeada-Çanakkale"]),
    ib("tr-ep-imbros-zeytinlikoy-dormition", "Church of the Dormition of the Theotokos in Zeytinlikoy",
       "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου", "Zeytinlikoy"),
    ib("tr-ep-imbros-zeytinlikoy-demetrius", "Chapel of Saint Demetrius in Zeytinlikoy",
       "Παρεκκλήσιον τοῦ Ἁγίου Δημητρίου", "Zeytinlikoy", "Chapel"),
    ib("tr-ep-imbros-zeytinlikoy-charalambos", "Chapel of Saint Charalambos in Zeytinlikoy",
       "Παρεκκλήσιον Ἁγίου Χαραλάμπους", "Zeytinlikoy", "Chapel"),
    ib("tr-ep-imbros-zeytinlikoy-archangels", "Chapel of the Archangels in Zeytinlikoy",
       "Παρεκκλήσιον τῶν Παμμεγίστων Ταξιαρχῶν", "Zeytinlikoy", "Chapel"),
])

DIRECT_METOCHIA = {
    "sinai": [
        ep("tr-sinai-istanbul-forerunner-metochion", "sinai",
           "Sinai Metochion of Saint John the Forerunner in Phanar",
           "Σιναϊτικόν Μετόχιον Ἁγίου Ἰωάννου τοῦ Προδρόμου ἐν Φαναρίῳ",
           "Istanbul", EP_ARCHDIOCESE, "Metochion", "monastery"),
        ep("tr-sinai-imbros-demetrius-metochion", "sinai",
           "Sinai Metochion of Saint Demetrius at Livrochia",
           "Σιναϊτικόν Ἱερόν Μετόχιον Ἁγίου Δημητρίου εἰς Λιβρόχια Ἀγριδίων",
           "Tepekoy", EP_IMBROS, "Metochion", "monastery"),
    ],
    "constantinople": [
        ep("tr-ep-imbros-great-lavra-constantine-helen-metochion",
           "constantinople",
           "Great Lavra Metochion of Saints Constantine and Helen on Imbros",
           "Ἱερόν Μετόχιον Ἁγίων Κωνσταντίνου καί Ἑλένης Ἱερᾶς Μονῆς Μεγίστης Λαύρας",
           "Zeytinlikoy", EP_IMBROS, "Metochion", "monastery"),
        ep("tr-ep-imbros-koutloumousiou-archangels-metochion",
           "constantinople", "Koutloumousiou Metochion of the Archangels on Imbros",
           "Ἱερόν Μετόχιον Παμμεγίστων Ταξιαρχῶν Ἱερᾶς Μονῆς Κουτλουμουσίου",
           "Eskibademli", EP_IMBROS, "Metochion", "monastery"),
        ep("tr-ep-tenedos-iveron-portaitissa-metochion", "constantinople",
           "Iveron Metochion of Panagia Portaitissa on Tenedos",
           "Ἱερόν Μετόχιον Παναγίας Πορταϊτίσσης Ἱερᾶς Μονῆς Ἰβήρων",
           "Bozcaada", EP_IMBROS, "Metochion", "monastery"),
    ],
}


def moscow(row_id, name, local, seat, slug, rank="Community",
           address=None, phones=None):
    page = MOSPAT_BASE + slug + "/"
    return body(row_id, "russia", name, local, seat,
                [page, MOSPAT_ROSTER_NOTICE, MOSPAT_CURRENT], rank,
                "parish", address, phones=phones)


MOSCOW = [
    moscow("tr-ru-istanbul-constantine-helen",
           "Church of Saints Constantine and Helen in Istanbul",
           "Храм святых равноапостольных Константина и Елены в Стамбуле",
           "Istanbul", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-10",
           "Church", ["Rusya Konsolosluğu Büyükdere Mahallesi",
                      "Piyasa Cd. No:69, 34453 Sarıyer/İstanbul"],
           ["+79163227914"]),
    moscow("tr-ru-antalya-parish",
           "Russian Orthodox Church Parish in Antalya",
           "Приход Русской Православной Церкви (Московский Патриархат) в Анталье",
           "Antalya", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-9", "Parish"),
    moscow("tr-ru-alanya-parish", "Russian Orthodox Church Parish in Alanya",
           "Приход Русской Православной Церкви (Московский Патриархат) в Аланье",
           "Alanya", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-8", "Parish",
           phones=["+905411548858", "+905380969229"]),
    moscow("tr-ru-ankara-community", "Russian Orthodox Church Community in Ankara",
           "Община Русской Православной Церкви (Московский Патриархат) в Анкаре",
           "Ankara", "obshhina-russkoj-pravoslavnoj-czerkvi-moskovskij-patriarhat-v-ankare",
           phones=["+79163227914"]),
    moscow("tr-ru-marmaris-community", "Russian Orthodox Church Community in Marmaris",
           "Община Русской Православной Церкви (Московский Патриархат) в Мармарисе",
           "Marmaris", "obshhina-russkoj-pravoslavnoj-czerkvi-moskvoskij-patriarhat-v-marmarise",
           phones=["+905356637235"]),
    moscow("tr-ru-bursa-community", "Russian Orthodox Church Community in Bursa",
           "Община Русской Православной Церкви (Московский Патриархат) в Бурсе",
           "Bursa", "obshhina-russkoj-pravoslavnoj-czerkvi-moskovskij-patriarhat-v-burse",
           phones=["+79163227914"]),
    moscow("tr-ru-kocaeli-community", "Russian Orthodox Church Community in Kocaeli",
           "Община Русской Православной Церкви (Московский Патриархат) в Коджаэли",
           "Kocaeli", "obshhina-russkoj-pravoslavnoj-czerkvi-moskovskij-patriarhat-v-kodzhaeli",
           phones=["+79163227914"]),
    moscow("tr-ru-samsun-community", "Russian Orthodox Church Community in Samsun",
           "Община Русской Православной Церкви (Московский Патриархат) в Самсуне",
           "Samsun", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-3",
           address=["Denizevleri, 212. Sk. no 7",
                    "55200 Atakum/Samsun, Турция"], phones=["+79163227914"]),
    moscow("tr-ru-eskisehir-community", "Russian Orthodox Church Community in Eskisehir",
           "Община Русской Православной Церкви (Московский Патриархат) в Эскишехире",
           "Eskisehir", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-4",
           address=["Mustafa Kemal Paşa, Sümer Sk. No:17",
                    "26120 Tepebaşı/ Eskişehir"], phones=["+79163227914"]),
    moscow("tr-ru-demre-dormition-basilica", "Dormition Basilica Worship Community in Myra",
           "Базилика Успения Божьей Матери в Мирах Ликийских (Демре)",
           "Demre", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-5",
           "Recurring Worship Site", phones=["+905356637235"]),
    moscow("tr-ru-kusadasi-community", "Russian Orthodox Church Community in Kusadasi",
           "Община Русской Православной Церкви (Московский Патриархат) в Кушадасах",
           "Kusadasi", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-6",
           address=["İki Çeşmelik Mah., Süleyman Demirel Bulv.",
                    "No 25/ 1, Kuşadası"], phones=["+79163227914"]),
    moscow("tr-ru-izmir-community", "Russian Orthodox Church Community in Izmir",
           "Община Русской Православной Церкви (Московский Патриархат) в Измире",
           "Izmir", "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-7",
           address=["İzmir, Bostanli Mah. Bestekar Sadi Hoşses Sokak N17 Meral Hanım",
                    "Между метро Nergız и Demir Köprü"], phones=["+79163227914"]),
    moscow("tr-ru-ephesus-basilica-worship", "Basilica Worship Community in Ephesus",
           "Базилика в Эфесе", "Selcuk",
           "hram-russkoj-pravoslavnoj-czerkvi-v-izmire-2", "Recurring Worship Site",
           address=["Музейный комплекс Эфес: Acarlar, Efes Harabeleri, 35920 Selçuk/İzmir",
                    "Могила святого апостола Иоанна Богослова: Atatürk, St. Jean Cd., 35920 Selçuk/İzmir"],
           phones=["+79163227914"]),
    moscow("tr-ru-cappadocia-george-worship", "Church of Saint George Worship Community in Cappadocia",
           "Храм святого Георгия Победоносца в Каппадокии", "Cappadocia",
           "hram-russkoj-pravoslavnoj-czerkvi-v-izmire", "Recurring Worship Site",
           phones=["+90535667235"]),
]

ANTIOCH = [
    body("tr-an-tarsus-adana-hatay", "antioch",
         "Diocese of Tarsus, Adana and Hatay",
         "أبرشية طرسوس وأضنة ولواء الاسكندرون (هاتاي)", "",
         [ANTIOCH_DIOCESE], "Diocese", "diocese"),
    body("tr-an-antakya-peter-paul-cathedral", "antioch",
         "Cathedral of the Apostles Peter and Paul in Antioch",
         "كاتدرائية الرسولين بطرس وبولس في أنطاكية", "Antakya",
         [ANTIOCH_CATHEDRAL, ANTIOCH_CONTACT], "Cathedral",
         phones=["+90 326 213 6496"]),
    body("tr-an-iskenderun-george", "tr-an-tarsus-adana-hatay",
         "Church of Saint George in Iskenderun",
         "كنيسة القديس جاورجيوس في لواء الاسكندرون", "Iskenderun",
         [ANTIOCH_ISKENDERUN], "Church"),
    body("tr-an-hatay-suriyah-george", "tr-an-tarsus-adana-hatay",
         "Church of Saint George in Al-Suriyah",
         "كنيسة القديس جاورجيوس في الصوريّة", "Hatay",
         [ANTIOCH_SURIYAH], "Church"),
    body("tr-an-mersin-archangels", "tr-an-tarsus-adana-hatay",
         "Church of the Archangels Michael and Gabriel in Mersin",
         "كنيسة رئيسي الملائكة ميخائيل وجبرائيل في مرسين", "Mersin",
         [ANTIOCH_MERSIN, ANTIOCH_DIOCESE], "Church"),
]
ANTIOCH[1]["contact_sources"] = [ANTIOCH_CONTACT]

BULGARIAN = [
    body("tr-bg-istanbul-community", "bulgaria",
         "Bulgarian Orthodox Church Community in Istanbul",
         "Българска православна църковна община в Истанбул", "Istanbul",
         [BULGARIAN_CURRENT, BULGARIAN_STATUTE, BULGARIAN_SITES],
         "Church Community"),
]

ROMANIAN = [
    body("tr-ro-istanbul-community", "romania",
         "Romanian Orthodox Community in Turkey",
         "Comunitatea Ortodoxă Română din Turcia", "Istanbul",
         [ROMANIAN_COMMUNITIES, ROMANIAN_ISTANBUL], "Church Community",
         address=["Aya Paraskevi Kilisesi, Kalaycı Bahçe Sok. No. 2",
                  "Piripaşa Mah., Hasköy, Beyoğlu, Istanbul"]),
]


def build_constantinople():
    rows = []
    for row_id, name, local, seat, address, phones in CONSTANTINOPLE_CHURCHES:
        rank = "Cemetery Church" if "cemetery" in row_id else "Church"
        extra = []
        if row_id == "tr-ep-constantinople-edirnekapi-george":
            extra.append(EP_GEORGIAN)
        if row_id in {
                "tr-ep-constantinople-sisli-john-rila",
                "tr-ep-constantinople-ferikoy-demetrius-bulgarian-cemetery",
                "tr-ep-constantinople-balat-stephen-bulgarian"}:
            extra.append(BULGARIAN_SITES)
        if row_id == "tr-ep-constantinople-haskoy-paraskevi":
            extra.append(ROMANIAN_ISTANBUL)
        rows.append(ep(row_id, "ep-constantinople", name, local, seat,
                       EP_ARCHDIOCESE, rank, address=address,
                       phones=phones, extra_sources=extra))
    for row_id, name, local, seat, address, phones in CONSTANTINOPLE_MONASTERIES:
        rows.append(ep(row_id, "ep-constantinople", name, local, seat,
                       EP_ARCHDIOCESE, "Monastery", "monastery",
                       address=address, phones=phones))
    return rows


ROWS = {
    "ep-constantinople": build_constantinople(),
    "ep-chalcedon": CHALCEDON,
    "ep-derkoi": DERKOI,
    "ep-princes-islands": PRINCES,
    "ep-pisidia": PISIDIA,
    "ep-vryoula": VRYOULA,
    "ep-selybria": SELYBRIA,
    "ep-adrianople": ADRIANOPLE,
    "ep-smyrna": SMYRNA,
    "ep-bursa": [],
    "ep-ganos-chora": GANOS,
    "ep-imbros-tenedos": IMBROS,
    "sinai": DIRECT_METOCHIA["sinai"],
    "constantinople": DIRECT_METOCHIA["constantinople"],
    "russia": MOSCOW,
    "antioch": ANTIOCH,
    "bulgaria": BULGARIAN,
    "romania": ROMANIAN,
}

EXPECTED = {
    "ep-constantinople": 63,
    "ep-chalcedon": 12,
    "ep-derkoi": 8,
    "ep-princes-islands": 9,
    "ep-pisidia": 4,
    "ep-vryoula": 1,
    "ep-selybria": 1,
    "ep-adrianople": 2,
    "ep-smyrna": 2,
    "ep-bursa": 0,
    "ep-ganos-chora": 2,
    "ep-imbros-tenedos": 102,
    "sinai": 2,
    "constantinople": 3,
    "russia": 14,
    "antioch": 5,
    "bulgaria": 1,
    "romania": 1,
}
EXPECTED_TOTAL = 232
EXPECTED_CONTACT_ROWS = 92
EXPECTED_EMAIL_ROWS = 1
EXPECTED_PHONE_ROWS = 92
EXPECTED_EMAIL_VALUES = 1
EXPECTED_PHONE_VALUES = 108
ALLOWED_KINDS = {"diocese", "parish", "monastery"}
ALLOWED_RANKS = {
    "Cathedral", "Cemetery Church", "Chapel", "Church",
    "Church Community", "Community", "Diocese", "House Chapel",
    "Metochion", "Metropolitan Church", "Monastery", "Parish",
    "Recurring Worship Site", "Wayside Chapel",
}
ALL_SOURCE_ROWS = [item for rows in ROWS.values() for item in rows]
ENGLISH_NAMES = {item["id"]: item["name"] for item in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {
    item["seat"]: item["seat"] for item in ALL_SOURCE_ROWS
    if item.get("seat")
}


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % item.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    rendered = json.dumps(item, ensure_ascii=False)
    forbidden = ("\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d", "\ufffd")
    if any(mark in rendered for mark in forbidden):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         item.get("id"))
    return item


def validate_row(item, branch_seen):
    row_id = item.get("id")
    if not row_id or not re.fullmatch(r"[a-z0-9-]+", row_id):
        raise ValueError("invalid or missing id: %s" % row_id)
    if item.get("parent") not in branch_seen:
        raise ValueError("%s hangs off an unknown parent" % row_id)
    if item.get("country") != "TR":
        raise ValueError("%s is outside Turkey" % row_id)
    if item.get("kind") not in ALLOWED_KINDS:
        raise ValueError("%s has an unsupported kind" % row_id)
    if item.get("rank") not in ALLOWED_RANKS:
        raise ValueError("%s has an unsupported rank" % row_id)
    if not item.get("name") or not item.get("local"):
        raise ValueError("%s lacks a usable name" % row_id)
    if item.get("site"):
        raise ValueError("%s unexpectedly publishes a body site" % row_id)
    emails = item.get("emails") or []
    phones = item.get("phones") or []
    contact_sources = item.get("contact_sources") or []
    if emails or phones:
        if item.get("contact_checked") != CHECKED:
            raise ValueError("%s has an outdated contact check" % row_id)
        if not contact_sources or len(contact_sources) > 3:
            raise ValueError("%s has invalid contact sources" % row_id)
        if not all(str(url).startswith("https://")
                   for url in contact_sources):
            raise ValueError("%s has a non-HTTPS contact source" % row_id)
        if len(emails) != len(set(emails)) or len(phones) != len(set(phones)):
            raise ValueError("%s has duplicate contact values" % row_id)
        if not all(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value)
                   for value in emails):
            raise ValueError("%s has an invalid public email" % row_id)
        if not all(isinstance(value, str) and value.strip()
                   for value in phones):
            raise ValueError("%s has an invalid public phone" % row_id)
    elif contact_sources or item.get("contact_checked"):
        raise ValueError("%s has contact metadata without contacts" % row_id)


def build():
    payloads = {}
    all_seen = set(ROWS)
    total = 0
    for branch_parent, source_rows in ROWS.items():
        branch_seen = {branch_parent}
        rows = []
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if row_id in all_seen:
                raise ValueError("duplicate id: %s" % row_id)
            validate_row(item, branch_seen)
            all_seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        if len(rows) != EXPECTED[branch_parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (branch_parent, EXPECTED[branch_parent]))
        total += len(rows)
        payloads[branch_parent] = {
            "v": 1,
            "parent": branch_parent,
            "country": "TR",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Turkey must publish exactly %d rows" % EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != all_seen - set(ROWS):
        raise ValueError("Turkey English name map is out of sync")
    contact_rows = [item for item in ALL_SOURCE_ROWS
                    if item.get("emails") or item.get("phones")]
    checks = (
        (len(contact_rows), EXPECTED_CONTACT_ROWS, "contact row"),
        (sum(bool(item.get("emails")) for item in contact_rows),
         EXPECTED_EMAIL_ROWS, "email row"),
        (sum(bool(item.get("phones")) for item in contact_rows),
         EXPECTED_PHONE_ROWS, "phone row"),
        (sum(len(item.get("emails") or []) for item in contact_rows),
         EXPECTED_EMAIL_VALUES, "public email"),
        (sum(len(item.get("phones") or []) for item in contact_rows),
         EXPECTED_PHONE_VALUES, "public phone"),
    )
    for actual, expected, label in checks:
        if actual != expected:
            raise ValueError("Turkey %s total is out of sync" % label)
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "TR":
        raise ValueError("Turkey candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Turkey candidate ledger date is out of sync")
    summary = ledger.get("published_summary") or {}
    for parent, count in EXPECTED.items():
        if summary.get(parent) != count:
            raise ValueError("Turkey ledger count is out of sync for %s" % parent)
    if summary.get("total") != EXPECTED_TOTAL:
        raise ValueError("Turkey ledger total is out of sync")
    for key in ("candidates", "reconciliation", "official_jurisdiction_audit",
                "exclusions"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Turkey candidate ledger lacks %s" % key)
        for entry in ledger[key]:
            sources = entry.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Turkey ledger item has invalid sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Turkey ledger item has a non-HTTPS source")
    candidate_ids = [item.get("candidate_id") for item in ledger["candidates"]]
    if any(not value or not re.fullmatch(r"[a-z0-9-]+", value)
           for value in candidate_ids):
        raise ValueError("Turkey ledger carries an invalid candidate id")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Turkey ledger has duplicate candidate ids")
    required_categories = {
        "affiliation-unclear", "aggregate-only", "historical", "noncanonical",
        "uncertain", "unnamed",
    }
    if {item.get("category") for item in ledger["candidates"]} < required_categories:
        raise ValueError("Turkey ledger lacks one or more required candidate categories")
    rendered = json.dumps(ledger, ensure_ascii=False)
    forbidden = ("\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d", "\ufffd")
    if any(mark in rendered for mark in forbidden):
        raise ValueError("Turkey candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Turkey: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Turkey: %d current named bodies across Constantinople, Moscow, "
            "Antioch, Bulgaria, Romania, and Sinai structures" % EXPECTED_TOTAL
        )
    return 0


add_wayside(IMBROS, "tr-ep-imbros-zeytinlikoy-", "Zeytinlikoy", [
    ("george-poul", "Country Chapel of Saint George at Poul", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Πούλ)"),
    ("george-fterado", "Country Chapel of Saint George at Fterado", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Φτεράδο)"),
    ("panagia-arasiani", "Country Chapel of Panagia Arasiani", "Ἐξωκκλήσιον Παναγίας Ἀρασιανῆς"),
    ("thekla-vrachakia", "Country Chapel of Saint Thekla at Vrachakia", "Ἐξωκκλήσιον Ἁγίας Θέκλας (Βραχάκια)"),
    ("john-vlastologos-kastri", "Country Chapel of Saint John Vlastologos at Kastri",
     "Ἐξωκκλήσιον Ἁγίου Ἰωάννου τοῦ Βλαστολόγου (Καστρί)"),
])

IMBROS.extend([
    ib("tr-ep-imbros-derekoy-marina", "Church of Saint Marina in Derekoy",
       "Ἱερός Ναός Ἁγίας Μαρίνης", "Derekoy",
       address=["Dereköy, 17760 Gökçeada-Çanakkale"]),
    ib("tr-ep-imbros-derekoy-dormition", "Church of the Dormition of the Theotokos in Derekoy",
       "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου", "Derekoy"),
    ib("tr-ep-imbros-derekoy-forerunner", "Chapel of Saint John the Forerunner in Derekoy",
       "Παρεκκλήσιον Τιμίου Προδρόμου", "Derekoy", "Chapel"),
])
add_wayside(IMBROS, "tr-ep-imbros-derekoy-", "Derekoy", [
    ("elias-halaka", "Country Chapel of Prophet Elias at Halaka", "Ἐξωκκλήσιον Προφήτου Ἠλιού (Χάλακα)"),
    ("athanasius-bournia", "Country Chapel of Saint Athanasius at Bournia", "Ἐξωκκλήσιον Ἁγίου Ἀθανασίου (Μπουρνιά)"),
    ("john-theologian", "Country Chapel of Saint John the Theologian near Derekoy",
     "Ἐξωκκλήσιον Ἁγίου Ἰωάννου τοῦ Θεολόγου"),
    ("euthymius", "Country Chapel of Saint Euthymius near Derekoy", "Ἐξωκκλήσιον Ἁγίου Εὐθυμίου"),
    ("george", "Country Chapel of Saint George near Derekoy", "Ἐξωκκλήσιον Ἁγίου Γεωργίου"),
    ("constantine-helen", "Country Chapel of Saints Constantine and Helen near Derekoy",
     "Ἐξωκκλήσιον Ἁγίων Κωνσταντίνου καί Ἑλένης"),
    ("catherine", "Country Chapel of Saint Catherine near Derekoy", "Ἐξωκκλήσιον Ἁγίας Αἰκατερίνης"),
])

IMBROS.extend([
    ib("tr-ep-imbros-tepekoy-annunciation", "Church of the Annunciation of the Theotokos in Tepekoy",
       "Ἱερός Ναός Εὐαγγελισμοῦ τῆς Θεοτόκου", "Tepekoy",
       address=["Tepeköy, 17760 Gökçeada-Çanakkale"]),
    ib("tr-ep-imbros-tepekoy-phanourios", "Chapel of Saint Phanourios in Tepekoy",
       "Παρεκκλήσιον Ἁγίου Φανουρίου", "Tepekoy", "Chapel"),
    ib("tr-ep-imbros-tepekoy-modestus-cemetery", "Cemetery Church of Saint Modestus in Tepekoy",
       "Κοιμητηριακός Ἱερός Ναός Ἁγίου Μοδέστου", "Tepekoy", "Cemetery Church"),
])
add_wayside(IMBROS, "tr-ep-imbros-tepekoy-", "Tepekoy", [
    ("george-apaliri", "Country Chapel of Saint George at Apaliri", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Ἀπαλίρι)"),
    ("archangels-valanari", "Country Chapel of the Archangels at Valanari", "Ἐξωκκλήσιον Παμμεγίστων Ταξιαρχῶν (Βαλανάρι)"),
    ("holy-trinity-hagiado", "Country Chapel of the Holy Trinity at Hagiado", "Ἐξωκκλήσιον Ἁγίας Τριάδος (Χαγιάδο)"),
    ("transfiguration-siomata", "Country Chapel of the Transfiguration at Siomata",
     "Ἐξωκκλήσιον Μεταμορφώσεως τοῦ Σωτῆρος (Σιώματα)"),
    ("eustratius-tagari", "Country Chapel of Saint Eustratius at Tagari", "Ἐξωκκλήσιον Ἁγίου Εὐστρατίου (Ταγάρι)"),
    ("dormition-kastrinado", "Country Chapel of the Dormition at Kastrinado", "Ἐξωκκλήσιον Κοιμήσεως τῆς Θεοτόκου (Καστρινάδο)"),
    ("demetrius-livrochia", "Country Chapel of Saint Demetrius at Livrochia", "Ἐξωκκλήσιον Ἁγίου Δημητρίου (Λιβρόχια)"),
    ("nicholas-mourtari", "Country Chapel of Saint Nicholas at Mourtari", "Ἐξωκκλήσιον Ἁγίου Νικολάου (Μουρτάρι)"),
    ("basil-alipares", "Country Chapel of Saint Basil at Alipares", "Ἐξωκκλήσιον Ἁγίου Βασιλείου (Ἀλιπάρες)"),
    ("demetrius-vigli", "Country Chapel of Saint Demetrius at Vigli", "Ἐξωκκλήσιον Ἁγίου Δημητρίου (Βίγλη)"),
    ("panteleimon-patinado", "Country Chapel of Saint Panteleimon at Patinado", "Ἐξωκκλήσιον Ἁγίου Παντελεήμονος (Πατινάδο)"),
    ("anastasia-klismata", "Country Chapel of Saint Anastasia at Klismata", "Ἐξωκκλήσιον Ἁγίας Ἀναστασίας (Κλίσματα)"),
    ("athanasius-rozado", "Country Chapel of Saint Athanasius at Rozado", "Ἐξωκκλήσιον Ἁγίου Ἀθανασίου (Ροζάδο)"),
    ("arsenius-vat", "Country Chapel of Saint Arsenius at Vat", "Ἐξωκκλήσιον Ἁγίου Ἀρσενίου (Βάτ)"),
    ("george-kourniado", "Country Chapel of Saint George at Kourniado", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Κουρνιάδου)"),
])

IMBROS.extend([
    ib("tr-ep-imbros-eskibademli-dormition", "Church of the Dormition of the Theotokos in Eskibademli",
       "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου", "Eskibademli",
       address=["Eskibademli, 17760 Gökçeada-Çanakkale"],
       phones=["+90.286.887.2806"]),
    ib("tr-ep-imbros-eskibademli-quiricus-julitta", "Chapel of Saints Quiricus and Julitta in Eskibademli",
       "Παρεκκλήσιον Ἁγίων Κηρύκου καί Ἰουλίτης", "Eskibademli", "Chapel"),
])
add_wayside(IMBROS, "tr-ep-imbros-eskibademli-", "Eskibademli", [
    ("eustratius-vrysara", "Country Chapel of Saint Eustratius at Vrysara", "Ἐξωκκλήσιον Ἁγίου Εὐστρατίου (Βρυσάρα)"),
    ("george-fkada", "Country Chapel of Saint George at Fkada", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Φκαδᾶ)"),
    ("andrew-vosko", "Country Chapel of Saint Andrew at Vosko", "Ἐξωκκλήσιον Ἁγίου Ἀνδρέου (Βοσκό)"),
    ("athanasius", "Country Chapel of Saint Athanasius near Eskibademli", "Ἐξωκκλήσιον Ἁγίου Ἀθανασίου"),
    ("panagia-eleousa", "Country Chapel of Panagia Eleousa near Eskibademli", "Ἐξωκκλήσιον Παναγίας τῆς Ἐλεούσης"),
    ("basil", "Country Chapel of Saint Basil near Eskibademli", "Ἐξωκκλήσιον Ἁγίου Βασιλείου"),
    ("panagia-galaktotrophousa-plaka", "Country Chapel of Panagia Galaktotrophousa at Plaka",
     "Ἐξωκκλήσιον Παναγίας τῆς Γαλακτοτροφούσης (Πλάκα)"),
    ("george-petrogourni", "Country Chapel of Saint George at Petrogourni", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Πετρογούρνι)"),
    ("panagia-meintaniotissa", "Country Chapel of Panagia Meintaniotissa", "Ἐξωκκλήσιον Παναγίας τῆς Μεϊντανιωτίσσης"),
    ("nektarios", "Country Chapel of Saint Nektarios near Eskibademli", "Ἐξωκκλήσιον Ἁγίου Νεκταρίου"),
])

IMBROS.extend([
    ib("tr-ep-imbros-yenimahalle-barbara", "Church of Saint Barbara in Yenimahalle",
       "Ἱερός Ναός Ἁγίας Βαρβάρας", "Yenimahalle",
       address=["Yenimahalle Aya Varvara Kilisesi",
                "17760 Gökçeada-Çanakkale"], phones=["+90.286.887.4493"]),
    ib("tr-ep-imbros-yenimahalle-barbara-chapel", "Chapel of Saint Barbara in Yenimahalle",
       "Παρεκκλήσιον Ἁγίας Βαρβάρας μεθ' Ἁγιάσματος", "Yenimahalle", "Chapel"),
])
add_wayside(IMBROS, "tr-ep-imbros-yenimahalle-", "Yenimahalle", [
    ("transfiguration", "Country Chapel of the Transfiguration near Yenimahalle", "Ἐξωκκλήσιον Μεταμορφώσεως τοῦ Σωτῆρος"),
    ("george", "Country Chapel of Saint George near Yenimahalle", "Ἐξωκκλήσιον Ἁγίου Γεωργίου"),
    ("dormition-lazarada", "Country Chapel of the Dormition at Lazarada", "Ἐξωκκλήσιον Κοιμήσεως τῆς Θεοτόκου (Λαζαράδα)"),
    ("archangel-palavado", "Country Chapel of the Archangel at Palavado", "Ἐξωκκλήσιον Ἁγίου Ταξιάρχου (Παλαβάδο)"),
    ("barbara-limni", "Country Chapel of Saint Barbara at Limni", "Ἐξωκκλήσιον Ἁγίας Βαρβάρας (Λημνί)"),
    ("john-kalamia", "Country Chapel of Saint John at Kalamia", "Ἐξωκκλήσιον Ἁγίου Ἰωάννου (Καλάμια)"),
    ("dormition-klivanos", "Country Chapel of the Dormition at Klivanos", "Ἐξωκκλήσιον Κοιμήσεως τῆς Θεοτόκου (Κλίβανος)"),
    ("george-plakia", "Country Chapel of Saint George at Plakia", "Ἐξωκκλήσιον Ἁγίου Γεωργίου (Πλακιά)"),
    ("theodore-samakas", "Country Chapel of Saint Theodore at Samakas", "Ἐξωκκλήσιον Ἁγίου Θεοδώρου (Σάμακας)"),
    ("dormition-damia", "Country Chapel of the Dormition at Damia", "Ἐξωκκλήσιον Κοιμήσεως τῆς Θεοτόκου (Ντάμια)"),
    ("anthony-lamarada", "Country Chapel of Saint Anthony at Lamarada", "Ἐξωκκλήσιον Ἁγίου Ἀντωνίου (Λαμαράδα)"),
    ("all-saints", "Country Chapel of All Saints near Yenimahalle", "Ἐξωκκλήσιον Ἁγίων Πάντων"),
    ("panteleimon", "Country Chapel of Saint Panteleimon near Yenimahalle", "Ἐξωκκλήσιον Ἁγίου Παντελεήμονος"),
    ("anastasia-pharmacolytria", "Country Chapel of Saint Anastasia Pharmacolytria near Yenimahalle",
     "Ἐξωκκλήσιον Ἁγίας Ἀναστασίας τῆς Φαρμακολυτρίας"),
])

IMBROS.extend([
    ib("tr-ep-imbros-kastro-marina", "Church of Saint Marina in Kastro", "Ἱερός Ναός Ἁγίας Μαρίνης", "Gokceada"),
    ib("tr-ep-imbros-kastro-nicholas", "Church of Saint Nicholas in Kastro", "Ἱερός Ναός Ἁγίου Νικολάου", "Gokceada"),
    ib("tr-ep-imbros-kastro-spyridon", "Chapel of Saint Spyridon in Kastro", "Παρεκκλήσιον Ἁγίου Σπυρίδωνος", "Gokceada", "Chapel"),
    ib("tr-ep-imbros-kastro-forerunner", "Chapel of Saint John the Forerunner in Kastro", "Παρεκκλήσιον Ἁγίου Ἰωάννου τοῦ Προδρόμου", "Gokceada", "Chapel"),
    ib("tr-ep-imbros-kastro-john-theologian", "Chapel of Saint John the Theologian in Kastro", "Παρεκκλήσιον Ἁγίου Ἰωάννου τοῦ Θεολόγου", "Gokceada", "Chapel"),
])
add_wayside(IMBROS, "tr-ep-imbros-kastro-", "Gokceada", [
    ("panagia-kardaminiotissa", "Country Chapel of Panagia Kardaminiotissa", "Ἐξωκκλήσιον Παναγίας τῆς Καρδαμηνιωτίσσης"),
    ("forerunner-mersiniotis", "Country Chapel of Saint John the Forerunner at Mersiniotis", "Ἐξωκκλήσιον Ἁγίου Ἰωάννου τοῦ Προδρόμου (Μερσηνιώτης)"),
])

IMBROS.extend([
    ib("tr-ep-tenedos-dormition", "Church of the Dormition of the Theotokos on Tenedos", "Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου", "Bozcaada",
       address=["16780 Bozcaada-Çanakkale"], phones=["+90.286. 697.8839"]),
    ib("tr-ep-tenedos-paraskevi", "Church of Saint Paraskevi on Tenedos", "Ἱερός Ναός Ἁγίας Παρασκευῆς μεθ' Ἁγιάσματος", "Bozcaada"),
    ib("tr-ep-tenedos-george", "Chapel of Saint George on Tenedos", "Παρεκκλήσιον Ἁγίου Γεωργίου", "Bozcaada", "Chapel"),
])
add_wayside(IMBROS, "tr-ep-tenedos-", "Bozcaada", [
    ("spyridon", "Country Chapel of Saint Spyridon on Tenedos", "Ἐξωκκλήσιον Ἁγίου Σπυρίδωνος"),
    ("eustratius", "Country Chapel of Saint Eustratius on Tenedos", "Ἐξωκκλήσιον Ἁγίου Εὐστρατίου"),
    ("theodore", "Country Chapel of Saints Theodore on Tenedos", "Ἐξωκκλήσιον Ἁγίων Θεοδώρων"),
    ("anna", "Country Chapel of Saint Anna on Tenedos", "Ἐξωκκλήσιον Ἁγίας Ἄννης"),
    ("panagia-faneromeni", "Country Chapel of Panagia Faneromeni on Tenedos", "Ἐξωκκλήσιον Παναγίας Φανερωμένης"),
])

IMBROS.extend([
    ib("tr-ep-imbros-marmaros-nicholas-monastery", "Monastery of Saint Nicholas at Marmaros",
       "Μονύδριον Ἁγίου Νικολάου εἰς θέσιν Μάρμαρος", "Tepekoy", "Monastery", "monastery"),
    ib("tr-ep-imbros-derekoy-archangel-kardamiotis-monastery",
       "Monastery of the Archangel Kardamiotis at Derekoy",
       "Μονύδριον Ἀρχιστρατήγου τοῦ Καρδαμιώτη ἤ Καλαμιδιώτη Σχοινουδίου",
       "Derekoy", "Monastery", "monastery"),
    ib("tr-ep-imbros-mesadi-panagia-balomeni-monastery", "Monastery of Panagia Balomeni at Mesadi",
       "Μονύδριον Παναγίας Μπαλωμένης εἰς τό Μεσάδι", "Tepekoy", "Monastery", "monastery"),
    ib("tr-ep-imbros-nerimata-archangels-monastery", "Monastery of the Archangels at Nerimata",
       "Μονύδριον Ἀρχιστρατήγων εἰς τά Νερήματα", "Zeytinlikoy", "Monastery", "monastery"),
    ib("tr-ep-imbros-derekoy-holy-trinity-monastery", "Monastery of the Holy Trinity at Derekoy",
       "Μονύδριον Ἁγίας Τριάδος εἰς Σχοινούδιον", "Derekoy", "Monastery", "monastery"),
    ib("tr-ep-imbros-derekoy-george-kastelianos-monastery",
       "Monastery of Saint George Kastelianos at Kalami",
       "Μονύδριον Ἁγίου Γεωργίου τοῦ Καστελιανοῦ εἰς θέσιν Καλάμι Σχοινουδίου",
       "Derekoy", "Monastery", "monastery"),
])

# ROWS keeps references to the mutable branch lists. Rebuild the immutable
# validation maps after the compact Imbros roster above has been expanded.
ALL_SOURCE_ROWS = [item for rows in ROWS.values() for item in rows]
ENGLISH_NAMES = {item["id"]: item["name"] for item in ALL_SOURCE_ROWS}
ENGLISH_SEATS = {
    item["seat"]: item["seat"] for item in ALL_SOURCE_ROWS
    if item.get("seat")
}


if __name__ == "__main__":
    raise SystemExit(main())
