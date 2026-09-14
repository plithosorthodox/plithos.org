# -*- coding: utf-8 -*-
"""The two dioceses of the Latvian Orthodox Church.

The Church divides its churches and monasteries into two dioceses on its
own site and names no others: the Riga diocese, with the deaneries of Rīga,
Liepāja and Valmiera, and the Daugavpils diocese, with the deaneries of
Daugavpils, Rēzekne and Madona. Its Latvian pages give both names in
Latvian. The third hierarch named on its page of archpastors is the Bishop
of Jelgava, vicar of the Riga diocese, and a vicariate is not a see of its
own, so there is no third row.

The Church publishes no separate address for the Riga diocese - the one
address it gives is its Synod's, which the Church's own row already
carries - and that row therefore has a name and a citation and nothing
else.

The Daugavpils diocese keeps a site of its own. It prints its Latvian name
in full, Latvijas Pareizticīgās Baznīcas Daugavpils-Rēzeknes Diecēze, and
the address of its diocesan administration, and it was carrying news of
this month when it was read.

The Church's own site is read over http; https is refused from here. It
answers at pareizticiba.lv and at pravoslavie.lv alike and asks to be cited
at either.
"""

READ = "2026-09-14"

DIOCESES = "http://www.pareizticiba.lv/index.php?id=40"
DIOCESES_LV = "http://www.pareizticiba.lv/index.php?id=40&lang=LV"
RIGA = "http://www.pareizticiba.lv/index.php?id=244"
DAUGAVPILS = "https://eparhija.lv/"
DAUGAVPILS_OFFICE = "https://eparhija.lv/eparhialjnoe-upravlenie/"

ROWS = [
 dict(id="lv-riga", parent="latvia",
      name="Diocese of Riga",
      local=u"Rīgas eparhija",
      seat="Riga", country="LV",
      sources=[DIOCESES, RIGA, DIOCESES_LV]),
 dict(id="lv-daugavpils", parent="latvia",
      name=u"Diocese of Daugavpils and Rēzekne",
      local=u"Daugavpils-Rēzeknes Diecēze",
      seat="Daugavpils", country="LV",
      address=["18. novembra iela 95", "Daugavpils, LV-5404"],
      site=DAUGAVPILS,
      sources=[DAUGAVPILS_OFFICE, DAUGAVPILS, DIOCESES]),
]
