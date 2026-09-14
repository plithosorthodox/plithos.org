# -*- coding: utf-8 -*-
"""The two dioceses of the Estonian Orthodox Christian Church.

The Church sets out its structure on its own page of the Church and names
two dioceses there, Tallinn and Narva, and its page of contacts gives each
of them its ruling see, its office hours and the street of its
administration. The Estonian pages name both in Estonian - Tallinna
piiskopkond, Narva ja Peipsiveere piiskopkond - and the Russian pages name
them in Russian.

The chancery of the metropolitan and the Tallinn diocesan administration
are one office at one address, which the Church prints on both. The Narva
and Peipsiveere diocese keeps a site of its own, which the Church links
from that page; it was carrying news of this month when it was read and
answers over http only, its certificate not matching its name.

The Church writes in Estonian and in Russian side by side. Its own
Estonian pages are the ones read for the names here, except that the page
of the Church's structure has not been put into Estonian and still carries
the Russian.
"""

READ = "2026-09-14"

CONTACTS = "https://et.orthodox.ee/contacts/"
CHURCH = "https://ru.orthodox.ee/church/"
NARVA = "http://www.narvaeparhia.ee/"

ROWS = [
 dict(id="ekok-tallinn", parent="estonia-ekok",
      name="Diocese of Tallinn",
      rank="Diocese",
      local=u"Tallinna piiskopkond",
      seat="Tallinn", country="EE",
      address=["Pikk 64/1-4", "10133 Tallinn"],
      sources=[CONTACTS, CHURCH]),
 dict(id="ekok-narva", parent="estonia-ekok",
      name="Diocese of Narva and Peipsi",
      rank="Diocese",
      local=u"Narva ja Peipsiveere piiskopkond",
      seat="Narva", country="EE",
      address=["Bastrakovi 4", "20308 Narva"],
      site=NARVA,
      sources=[CONTACTS, NARVA, CHURCH]),
]
