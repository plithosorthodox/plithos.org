# -*- coding: utf-8 -*-
"""The three dioceses of the Orthodox Church of Estonia.

Its own page of dioceses opens by saying the Church has three, and names
them: Tallinn, Tartu, and Parnu and Saare. It gives no address for any of
them and no English, so the rows carry the Estonian names the Church
prints and the English the site would read in.

THE COUNT IS A SENTENCE AND NOT A LIST OF LINKS, which is why it settles
the matter: "Eesti Apostlik-Õigeusu Kirikul on kolm piiskopkonda" - the
Church has three dioceses - and the three it then names are these three.
Read again on 14 September 2026 and unchanged. This file is complete.

The chancery of the metropolitan - and with it the archbishopric of
Tallinn - is at the Church centre named for the Hieromartyr Platon, whose
address the Church publishes on its page of contacts.

RANK AND WHAT A SECOND PAGE WOULD HAVE TO BE, 14 SEPTEMBER 2026. The Church
writes peapiiskopkond of Tallinn and piiskopkond of the other two, which is an
archdiocese and two dioceses, and the rows carry those words. Tartu and Parnu
and Saare keep one citation each. The Church has a page under each of their
names, but it is an archive of articles filed under that name rather than a
page about the see, and a listing that happens to repeat a name is not a
second source. One honest citation is better.
"""

DIOCESES = "https://www.eoc.ee/eesti-apostlik-oigeusu-kirik/piiskopkonnad/"
CENTRE = ("https://www.eoc.ee/eesti-apostlik-oigeusu-kirik/meie-inimesed/"
          "kirikukeskus/")

ROWS = [
 dict(id="ee-tallinn", parent="estonia-eaok",
      name="Archdiocese of Tallinn",
      local="Tallinna peapiiskopkond",
      rank="Archdiocese",
      seat="Tallinn", country="EE",
      address=["Wismari 32", "10136 Tallinn"],
      sources=[DIOCESES, CENTRE]),
 dict(id="ee-tartu", parent="estonia-eaok",
      name="Diocese of Tartu",
      local="Tartu piiskopkond",
      rank="Diocese",
      seat="Tartu", country="EE",
      sources=[DIOCESES]),
 dict(id="ee-parnu-saare", parent="estonia-eaok",
      name="Diocese of Pärnu and Saare",
      local="Pärnu ja Saare piiskopkond",
      rank="Diocese",
      seat="Pärnu", country="EE",
      sources=[DIOCESES]),
]
