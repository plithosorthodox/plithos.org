# -*- coding: utf-8 -*-
"""The directory's rows in Romanian.

Read off what the site already publishes in Romanian rather than composed.
The pattern for a local Church is the one the calendar's own canonization
lines use - Biserica Greciei, Biserica Rusiei, Biserica Ortodoxă din
America - so the row takes the enclitic article Romanian gives the word
Biserica and the country in the genitive. Constantinopolului is the form
standing in Patriarhia Ecumenică a Constantinopolului.

Two forms competed and were counted across everything this site publishes
in Romanian:

  Chiev against Kiev, for the seat of the Church of Ukraine. Chiev stands
  302 times against 200 for the genitive Kievului, and docs/ROMANIAN.md
  names Chiev among the received forms Romanian usage keeps; Chiev.

  Ohrida against Ohrid, for the Macedonian archbishopric. Ohrida stands 49
  times and Ohridei 10; the bare Ohrid appears only where the English is
  quoted. Ohrida.

Five seats had never been named in Romanian here and are written new:
Istanbul, Tirana, Skopje, Tallinn and Tokio, each in the form Romanian
usage has received, and Prešov and Syosset, which Romanian writes as
Slovak and English write them.
"""
NAMES = {
    "constantinople": u"Biserica Constantinopolului",
    "alexandria": u"Biserica Alexandriei",
    "antioch": u"Biserica Antiohiei",
    "jerusalem": u"Biserica Ierusalimului",
    "russia": u"Biserica Rusiei",
    "georgia": u"Biserica Georgiei",
    "serbia": u"Biserica Serbiei",
    "romania": u"Biserica României",
    "bulgaria": u"Biserica Bulgariei",
    "cyprus": u"Biserica Ciprului",
    "greece": u"Biserica Greciei",
    "albania": u"Biserica Albaniei",
    "poland": u"Biserica Poloniei",
    "czech-slovakia": u"Biserica Țărilor Cehe și a Slovaciei",
    "oca": u"Biserica Ortodoxă din America",
    "macedonia": u"Biserica Ortodoxă Macedoneană - Arhiepiscopia Ohridei",
    "ukraine-uoc": u"Biserica Ucrainei",
    "ukraine-ocu": u"Biserica Ortodoxă a Ucrainei",
    "sinai": u"Biserica Sinaiului",
    "finland": u"Biserica Autonomă a Finlandei",
    "japan": u"Biserica Japoniei",
    "estonia-eaok": u"Biserica Ortodoxă a Estoniei",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Alexandria",
    "Damascus": u"Damasc",
    "Jerusalem": u"Ierusalim",
    "Moscow": u"Moscova",
    "Tbilisi": u"Tbilisi",
    "Belgrade": u"Belgrad",
    "Bucharest": u"București",
    "Sofia": u"Sofia",
    "Nicosia": u"Nicosia",
    "Athens": u"Atena",
    "Tirana": u"Tirana",
    "Warsaw": u"Varșovia",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Chiev",
    "Mount Sinai": u"Muntele Sinai",
    "Helsinki": u"Helsinki",
    "Tokyo": u"Tokio",
    "Tallinn": u"Tallinn",
}
