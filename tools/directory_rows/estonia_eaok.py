# -*- coding: utf-8 -*-
"""The three dioceses of the Orthodox Church of Estonia.

Its own page of dioceses opens by saying the Church has three, and names
them: Tallinn, Tartu, and Parnu and Saare. It gives no address for any of
them and no English, so the rows carry the Estonian names the Church
prints and the English the site would read in.

The chancery of the metropolitan - and with it the archbishopric of
Tallinn - is at the Church centre named for the Hieromartyr Platon, whose
address the Church publishes on its page of contacts.
"""

DIOCESES = "https://www.eoc.ee/eesti-apostlik-oigeusu-kirik/piiskopkonnad/"
CENTRE = ("https://www.eoc.ee/eesti-apostlik-oigeusu-kirik/meie-inimesed/"
          "kirikukeskus/")

ROWS = [
 dict(id="ee-tallinn", parent="estonia-eaok",
      name="Archdiocese of Tallinn",
      local="Tallinna peapiiskopkond",
      seat="Tallinn", country="EE",
      address=["Wismari 32", "10136 Tallinn"],
      sources=[DIOCESES, CENTRE]),
 dict(id="ee-tartu", parent="estonia-eaok",
      name="Diocese of Tartu",
      local="Tartu piiskopkond",
      seat="Tartu", country="EE",
      sources=[DIOCESES]),
 dict(id="ee-parnu-saare", parent="estonia-eaok",
      name="Diocese of Pärnu and Saare",
      local="Pärnu ja Saare piiskopkond",
      seat="Pärnu", country="EE",
      sources=[DIOCESES]),
]
