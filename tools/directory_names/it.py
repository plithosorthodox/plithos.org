# -*- coding: utf-8 -*-
"""Le Chiese e le loro sedi, in italiano.

Nothing here was rendered afresh. Every country, city and see was read off
the Italian this site already publishes - the place vocabulary beside the
lives, the calendar entries and the saints' names - and the form that
stands is the form already printed: Costantinopoli, Alessandria,
Antiochia, Gerusalemme, Mosca, Atene, Damasco, Belgrado, Bucarest,
Varsavia, Terre ceche.

Two forms had to be settled by counting, because two were available:

  - **Kyiv**, not Kiev: 1,090 against 3 across the Italian corpus, which is
    docs/ITALIAN.md's rule ("Ukrainian places take their Ukrainian form")
    already carried out.
  - **Ocrida**, not Ohrid: 13 against 2, and the place vocabulary renders
    Ohrid as Ocrida outright.

The name of a local Church takes the article and the bare preposition the
site already uses - Chiesa di Costantinopoli, Chiesa di Georgia, Chiesa di
Grecia, Chiesa di Cipro, Chiesa di Ucraina - except where Italian will not
drop the article at all, so the Sinai and the Giappone keep theirs. Chiesa
ortodossa in America is the site's own wording, written twenty-three times.

What the Italian pages have never had occasion to say is written here for
the first time, in the received Italian form. Seven cities: Istanbul,
Tirana, Prešov, Syosset, Skopje, Tallinn and Tokyo - all but two spelled as
English spells them, which is what Italian does with them. And three
countries: Estonia, Finlandia and Giappone. The site knows two of those
peoples - the lives write gli estoni and i finlandesi - but has never named
the countries, and Japan it has not named at all. Slovacchia follows i
fedeli slovacchi, which the calendar already says of Saint Gorazd's flock;
Arcivescovado follows arcivescovo, which stands 379 times.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Italian this site publishes and
are taken whole - Patriarcato ecumenico and the Chiesa ortodossa russa,
serba, romena and ucraina of the commemorations.

The three ancient sees follow the Patriarcato di Antiochia the calendar
writes, and e di tutto l'Oriente follows the e di tutta la Russia of the
patriarch of Moscow. The lower case of ortodossa and ecumenico is the site's
own Italian and is kept; Oriente is a place and keeps its capital.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Italian name for either body
carries it, so it is not written here.
"""
NAMES = {
    "constantinople": u"La Chiesa di Costantinopoli",
    "alexandria": u"La Chiesa di Alessandria",
    "antioch": u"La Chiesa di Antiochia",
    "jerusalem": u"La Chiesa di Gerusalemme",
    "russia": u"La Chiesa di Russia",
    "georgia": u"La Chiesa di Georgia",
    "serbia": u"La Chiesa di Serbia",
    "romania": u"La Chiesa di Romania",
    "bulgaria": u"La Chiesa di Bulgaria",
    "cyprus": u"La Chiesa di Cipro",
    "greece": u"La Chiesa di Grecia",
    "albania": u"La Chiesa di Albania",
    "poland": u"La Chiesa di Polonia",
    "czech-slovakia": u"La Chiesa delle Terre ceche e della Slovacchia",
    "oca": u"La Chiesa ortodossa in America",
    "macedonia": u"La Chiesa ortodossa macedone - Arcivescovado di Ocrida",
    "ukraine-uoc": u"La Chiesa di Ucraina",
    "ukraine-ocu": u"Chiesa ortodossa di Ucraina",
    "sinai": u"La Chiesa del Sinai",
    "finland": u"La Chiesa autonoma di Finlandia",
    "japan": u"La Chiesa del Giappone",
    "estonia-eaok": u"Chiesa ortodossa di Estonia",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Alessandria",
    "Damascus": u"Damasco",
    "Jerusalem": u"Gerusalemme",
    "Moscow": u"Mosca",
    "Tbilisi": u"Tbilisi",
    "Belgrade": u"Belgrado",
    "Bucharest": u"Bucarest",
    "Sofia": u"Sofia",
    "Nicosia": u"Nicosia",
    "Athens": u"Atene",
    "Tirana": u"Tirana",
    "Warsaw": u"Varsavia",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Kyiv",
    "Mount Sinai": u"Monte Sinai",
    "Helsinki": u"Helsinki",
    "Tokyo": u"Tokyo",
    "Tallinn": u"Tallinn",
}
STYLED = {
    "constantinople": u"Patriarcato ecumenico",
    "alexandria": u"Patriarcato di Alessandria",
    "antioch": u"Patriarcato di Antiochia e di tutto l'Oriente",
    "jerusalem": u"Patriarcato di Gerusalemme",
    "russia": u"Chiesa ortodossa russa",
    "serbia": u"Chiesa ortodossa serba",
    "romania": u"Chiesa ortodossa romena",
    "bulgaria": u"Chiesa ortodossa bulgara - Patriarcato bulgaro",
    "ukraine-uoc": u"Chiesa ortodossa ucraina",
}
