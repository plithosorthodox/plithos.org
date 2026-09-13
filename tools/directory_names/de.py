# -*- coding: utf-8 -*-
"""The directory's rows in German.

Read off what the site already publishes in German rather than composed.
The shape of a row is the one the calendar's own canonization lines use -
Kirche von Griechenland, Kirche der Rus, Orthodoxe Kirche in Amerika - so
the row keeps the article German gives a named Church and takes von before
a country that stands without one and the genitive before a country that
does not: von Russland, von Zypern, but der Ukraine, der Slowakei, vom
Sinai.

Two forms competed and were counted across everything this site publishes
in German:

  Tiflis against Tbilisi, for the seat of the Church of Georgia. Tiflis
  stands ten times in the German and Tbilisi only where the English name
  is quoted beside it; Tiflis.

  Makedonisch against Mazedonisch, for the Church whose archbishopric sits
  at Ohrid. The German here writes Makedonien eighteen times, Makedonia,
  Makedonier and Grossmakedonien besides, and Mazedonien not once; so
  Makedonische Orthodoxe Kirche.

Böhmische Länder is the site's own German for the Czech Lands, taken from
the vocabulary beside the saints' cards rather than rendered again here.

Five seats had never been named in German here and are written new:
Istanbul, Tirana, Skopje, Tallinn and Tokio, each in the form German usage
has received, and Prešov, which German writes as Slovak writes it.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the German this site publishes and are
taken whole - Ökumenisches Patriarchat and the Russische, Serbische,
Rumänische and Ukrainische Orthodoxe Kirche of the commemorations.

The three ancient sees follow the Patriarchat von Antiochien the calendar
already writes, and und dem ganzen Osten follows the und ganz Russland of the
patriarch of Moscow.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no German name for either body
carries it, so it is not written here.
"""
NAMES = {
    "constantinople": u"Die Kirche von Konstantinopel",
    "alexandria": u"Die Kirche von Alexandria",
    "antioch": u"Die Kirche von Antiochien",
    "jerusalem": u"Die Kirche von Jerusalem",
    "russia": u"Die Kirche von Russland",
    "georgia": u"Die Kirche von Georgien",
    "serbia": u"Die Kirche von Serbien",
    "romania": u"Die Kirche von Rumänien",
    "bulgaria": u"Die Kirche von Bulgarien",
    "cyprus": u"Die Kirche von Zypern",
    "greece": u"Die Kirche von Griechenland",
    "albania": u"Die Kirche von Albanien",
    "poland": u"Die Kirche von Polen",
    "czech-slovakia": u"Die Kirche der Böhmischen Länder und der Slowakei",
    "oca": u"Die Orthodoxe Kirche in Amerika",
    "macedonia": u"Die Makedonische Orthodoxe Kirche - Erzbistum Ohrid",
    "ukraine-uoc": u"Die Kirche der Ukraine",
    "ukraine-ocu": u"Orthodoxe Kirche der Ukraine",
    "sinai": u"Die Kirche vom Sinai",
    "finland": u"Die Autonome Kirche von Finnland",
    "japan": u"Die Kirche von Japan",
    "estonia-eaok": u"Orthodoxe Kirche von Estland",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Alexandria",
    "Damascus": u"Damaskus",
    "Jerusalem": u"Jerusalem",
    "Moscow": u"Moskau",
    "Tbilisi": u"Tiflis",
    "Belgrade": u"Belgrad",
    "Bucharest": u"Bukarest",
    "Sofia": u"Sofia",
    "Nicosia": u"Nikosia",
    "Athens": u"Athen",
    "Tirana": u"Tirana",
    "Warsaw": u"Warschau",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Kiew",
    "Mount Sinai": u"Berg Sinai",
    "Helsinki": u"Helsinki",
    "Tokyo": u"Tokio",
    "Tallinn": u"Tallinn",
}
STYLED = {
    "constantinople": u"Ökumenisches Patriarchat",
    "alexandria": u"Patriarchat von Alexandria",
    "antioch": u"Patriarchat von Antiochien und dem ganzen Osten",
    "jerusalem": u"Patriarchat von Jerusalem",
    "russia": u"Russische Orthodoxe Kirche",
    "serbia": u"Serbische Orthodoxe Kirche",
    "romania": u"Rumänische Orthodoxe Kirche",
    "bulgaria": u"Bulgarische Orthodoxe Kirche - Bulgarisches Patriarchat",
    "ukraine-uoc": u"Ukrainische Orthodoxe Kirche",
}
