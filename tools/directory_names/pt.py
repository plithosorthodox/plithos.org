# -*- coding: utf-8 -*-
"""The Churches and their seats, in Portuguese.

Brazilian Portuguese in the orthography of the 1990 Agreement, as
docs/PORTUGUESE.md settles it. Nothing here was rendered afresh: every
country, city and see was read off the Portuguese this site already
publishes - the vocabulary beside the lives, the calendar entries and the
saints' names - and the form that stands is the form already printed.

Three forms had to be settled by counting, because the site prints two:

  - **Kiev**, not Kyiv. The lives and the place vocabulary write Kiev 374
    times against 334 for Kyiv in the names index, and docs/PORTUGUESE.md
    lists Kiev among the plain transliterations that carry no accent.
  - **Ohrid**, not Ocrida. The place vocabulary renders Ohrid as Ohrid, 7
    times against 2; Ocrida stands only inside the received epithet of
    Saint Clement, which is a saint's name and not the city.
  - **Tbilissi**, with the doubled s the vocabulary writes, because a single
    s between vowels is voiced in Portuguese and would not be the name.

Ten places the Portuguese pages have never had occasion to name are written
here for the first time, in the received Portuguese form: Istambul, Tirana,
Prešov, Syosset, Skopje, Tallinn, Tóquio, Eslováquia, Finlândia and Japão.
Prešov keeps the Slovak spelling, as Žiča, Krušedol and Tvrdoš keep the
Serbian one on these pages.
"""
NAMES = {
    "constantinople": u"A Igreja de Constantinopla",
    "alexandria": u"A Igreja de Alexandria",
    "antioch": u"A Igreja de Antioquia",
    "jerusalem": u"A Igreja de Jerusalém",
    "russia": u"A Igreja da Rússia",
    "georgia": u"A Igreja da Geórgia",
    "serbia": u"A Igreja da Sérvia",
    "romania": u"A Igreja da Romênia",
    "bulgaria": u"A Igreja da Bulgária",
    "cyprus": u"A Igreja de Chipre",
    "greece": u"A Igreja da Grécia",
    "albania": u"A Igreja da Albânia",
    "poland": u"A Igreja da Polônia",
    "czech-slovakia": u"A Igreja das Terras Tchecas e da Eslováquia",
    "oca": u"A Igreja Ortodoxa na América",
    "macedonia": u"A Igreja Ortodoxa Macedônia - Arcebispado de Ohrid",
    "ukraine-uoc": u"A Igreja da Ucrânia",
    "ukraine-ocu": u"Igreja Ortodoxa da Ucrânia",
    "sinai": u"A Igreja do Sinai",
    "finland": u"A Igreja Autônoma da Finlândia",
    "japan": u"A Igreja do Japão",
    "estonia-eaok": u"Igreja Ortodoxa da Estônia",
}
SEATS = {
    "Istanbul": u"Istambul",
    "Alexandria": u"Alexandria",
    "Damascus": u"Damasco",
    "Jerusalem": u"Jerusalém",
    "Moscow": u"Moscou",
    "Tbilisi": u"Tbilissi",
    "Belgrade": u"Belgrado",
    "Bucharest": u"Bucareste",
    "Sofia": u"Sófia",
    "Nicosia": u"Nicósia",
    "Athens": u"Atenas",
    "Tirana": u"Tirana",
    "Warsaw": u"Varsóvia",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, Nova York",
    "Skopje": u"Skopje",
    "Kyiv": u"Kiev",
    "Mount Sinai": u"Monte Sinai",
    "Helsinki": u"Helsinque",
    "Tokyo": u"Tóquio",
    "Tallinn": u"Tallinn",
}
