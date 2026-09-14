# -*- coding: utf-8 -*-
"""The three dioceses of the Autonomous Church of Finland.

The Church names all three on its own page of dioceses, gives the street of
each chancery there, and names them in English on its English page. The
postal codes are from the Church's own list of contacts. Every diocese has
a page of its own on that same site, and each answered.

THREE IS THE CHURCH'S OWN WORD AND IT IS A SENTENCE, NOT A MENU. That page
opens by saying "Suomen ortodoksinen kirkko muodostuu Helsingin
hiippakunnasta, Kuopion ja Karjalan hiippakunnasta ja Oulun
hiippakunnasta" - the Church is made up of the dioceses of Helsinki, of
Kuopio and Karelia, and of Oulu - and adds that all three rank as
metropolitanates. Three rows, and this file is complete.
"""

DIOCESES = "https://ort.fi/suomen-ortodoksinen-kirkko/hiippakunnat/"
ENGLISH = "https://ort.fi/en/finnish-orthodox-church"
CONTACTS = "https://ort.fi/yhteystiedot/"

ROWS = [
 dict(id="fi-helsinki", parent="finland",
      name="Diocese of Helsinki",
      rank="Diocese",
      local="Helsingin hiippakunta",
      seat="Helsinki", country="FI",
      address=["Liisankatu 29 A 13", "00170 Helsinki"],
      site="https://ort.fi/arkkipiispa/",
      sources=[DIOCESES, ENGLISH, CONTACTS]),
 dict(id="fi-kuopio", parent="finland",
      name="Diocese of Kuopio and Karelia",
      rank="Diocese",
      local="Kuopion ja Karjalan hiippakunta",
      seat="Kuopio", country="FI",
      address=["Karjalankatu 1", "70110 Kuopio"],
      site="https://ort.fi/kuopionjakarjalanhiippakunta/",
      sources=[DIOCESES, ENGLISH,
               "https://ort.fi/kuopionjakarjalanhiippakunta/"]),
 dict(id="fi-oulu", parent="finland",
      name="Diocese of Oulu",
      rank="Diocese",
      local="Oulun hiippakunta",
      seat="Oulu", country="FI",
      address=["Nummikatu 30 B 16", "90100 Oulu"],
      site="https://ort.fi/oulunhiippakunta/",
      sources=[DIOCESES, ENGLISH, "https://ort.fi/oulunhiippakunta/"]),
]
