# -*- coding: utf-8 -*-
"""The dioceses of the Church of Poland.

Read on 14 September 2026 from the Church's own list of its dioceses at

    https://www.orthodox.pl/administracja/diecezje/

and then from the page it publishes for each one, which is where the address
and the diocese's own site come from and which each row cites. The list holds
eight entries: six dioceses, the Orthodox Ordinariate of the Polish Army, and
the Church's foreign units. Seven rows are written here.

THE EIGHTH ENTRY IS NOT A DIOCESE. "Kościelne jednostki zagraniczne" is the
Church's list of its parishes, missions and monasteries abroad - some thirty
of them in Brazil and Portugal, each with its own priest and address - and not
a see. Parishes are a later pass on this site and are not rows yet, so the
entry has no row and the Church has seven.

THE ORDINARIATE HAS ONE, because the Church lists it among its dioceses and it
is a jurisdiction with its own ordinary. It is a chaplaincy to the Polish army
rather than a territory, and its chancery is in Warsaw with the Metropolitan's.

ADDRESSES are the chancery the Church prints for each see - Kancelaria - in the
words and the order it prints them in, translated nowhere. The country line is
dropped, because the page writes it in the reader's language. All seven publish
one.

SITES. Four of the seven publish a site of their own and answered here:
Białystok and Gdańsk, Łódź and Poznań, Wrocław and Szczecin, and, since it
shares the Metropolitan's chancery, Warsaw and Bielsk at the Church's own
address. Lublin and Chełm publishes lublin.cerkiew.pl and the Ordinariate
powp.wp.mil.pl, and neither answered here; Przemyśl and Gorlice publishes an
e-mail address and no site at all. Those three rows carry no link and fall
back to the Church, and the first two are to be tried again.

NAMES. The Church publishes this list in Polish, so `local` is its own wording,
including the dash it sets between the two halves of a diocese's name, and
`name` is the English a reader of this site is given."""

READ = "2026-09-14"

PL = "https://www.orthodox.pl/administracja/diecezje/"

ROWS = [

 dict(id="pl-warsaw-bielsk", parent="poland",
      name="Diocese of Warsaw and Bielsk",
      local=u"Diecezja Warszawsko–Bielska",
      seat="Warsaw", country="PL",
      address=[u"Al. Solidarności 52", u"03-402 Warszawa"],
      site="https://www.orthodox.pl/",
      sources=[PL + "diecezja-warszawsko-bielska/"]),

 dict(id="pl-bialystok-gdansk", parent="poland",
      name="Diocese of Bialystok and Gdansk",
      local=u"Diecezja Białostocko–Gdańska",
      seat="Bialystok", country="PL",
      address=[u"ul. Św. Mikołaja 3", u"15-419 Białystok"],
      site="https://orthodox.bialystok.pl/",
      sources=[PL + "diecezja-bialostocko-gdanskadiecezja-bialostocko-gdanska/",
               "https://orthodox.bialystok.pl/"]),

 dict(id="pl-lodz-poznan", parent="poland",
      name="Diocese of Lodz and Poznan",
      local=u"Diecezja Łódzko–Poznańska",
      seat="Lodz", country="PL",
      address=[u"ul. Narutowicza 46/1", u"90-135 Łódź"],
      site="https://diecezjalp.cerkiew.pl/",
      sources=[PL + "diecezja-lodzko-poznanska/",
               "https://diecezjalp.cerkiew.pl/"]),

 dict(id="pl-wroclaw-szczecin", parent="poland",
      name="Diocese of Wroclaw and Szczecin",
      local=u"Diecezja Wrocławsko–Szczecińska",
      seat="Wroclaw", country="PL",
      address=[u"ul. Św. Mikołaja 40", u"50-128 Wrocław"],
      site="https://www.diecezjawroclawsko-szczecinska.pl/",
      sources=[PL + "diecezja-wroclawsko-szczecinska/",
               "https://www.diecezjawroclawsko-szczecinska.pl/"]),

 dict(id="pl-przemysl-gorlice", parent="poland",
      name="Diocese of Przemysl and Gorlice",
      local=u"Diecezja Przemysko–Gorlicka",
      seat="Gorlice", country="PL",
      address=[u"ul. św. Maksyma 2", u"38-300 Gorlice"],
      sources=[PL + "diecezja-przemysko-gorlicka/"]),

 dict(id="pl-lublin-chelm", parent="poland",
      name="Diocese of Lublin and Chelm",
      local=u"Diecezja Lubelsko-Chełmska",
      seat="Lublin", country="PL",
      address=[u"ul. Ruska 15", u"20-126 Lublin"],
      sources=[PL + "diecezja-lubelsko-chelmska/"]),

 dict(id="pl-army-ordinariate", parent="poland",
      name="Orthodox Ordinariate of the Polish Army",
      local=u"Prawosławny Ordynariat Wojska Polskiego",
      seat="Warsaw", country="PL",
      address=[u"ul. Żwirki i Wigury 9/13", u"00-909 Warszawa"],
      sources=[PL + "prawoslawny-ordynariat-wojska-polskiego/"]),
]
