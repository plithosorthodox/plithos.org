# -*- coding: utf-8 -*-
"""The dioceses of the Church of Poland.

Read on 14 September 2026 from the Church's own list of its dioceses at

    https://www.orthodox.pl/administracja/diecezje/

and then from the page it publishes for each one, which is where the address
and the diocese's own site come from and which each row cites. The list holds
eight entries: six dioceses, the Orthodox Ordinariate of the Polish Army, and
the Church's foreign units. Eight rows are written here.

WHERE THE COUNT COMES FROM. The Church states no number in a sentence
anywhere this machine could read, so it is the list of its own dioceses that
counts, and the eighth entry has to be opened rather than read off the menu.
Its own page of administration prints the same six and the Ordinariate again
and says nothing further.

THE EIGHTH ENTRY IS NOT ONE THING AND THE FIRST PASS TOOK IT FOR PARISHES.
"Kościelne jednostki zagraniczne" - the Church's foreign units - opens by
saying, in the Church's own words, that "Jurysdykcja Polskiego
Autokefalicznego Kościoła Prawosławnego obejmuje również misyjną Diecezję
Rio de Janeiro i Olinda-Recife - działającą na terenie Brazylii oraz Polską
Parafię Prawosławną w Brukseli." A missionary diocese in Brazil is a see and
has a row; the thirty parishes, missions and monastery under it, and the one
parish in Brussels, are parishes, which are a later pass on this site. So the
Church has seven dioceses at home and one abroad.

That row is the Rio de Janeiro and Olinda-Recife row, and its address is the
one the Church prints for the diocese's own cathedral, which is the address it
prints for the ordinary as well - the same house.

THE ORDINARIATE HAS ONE, because the Church lists it among its dioceses and it
is a jurisdiction with its own ordinary. It is a chaplaincy to the Polish army
rather than a territory, and its chancery is in Warsaw with the Metropolitan's.

ADDRESSES are the chancery the Church prints for each see - Kancelaria - in the
words and the order it prints them in, translated nowhere. The country line is
dropped, because the page writes it in the reader's language. All eight publish
one.

SITES. Four of the eight publish a site of their own and answered here:
Białystok and Gdańsk, Łódź and Poznań, Wrocław and Szczecin, and, since it
shares the Metropolitan's chancery, Warsaw and Bielsk at the Church's own
address. Lublin and Chełm publishes lublin.cerkiew.pl and the Ordinariate
powp.wp.mil.pl, and neither answered here; Przemyśl and Gorlice publishes an
e-mail address and no site at all, and the Church publishes none for the
missionary diocese in Brazil. Those four rows carry no link and fall back to
the Church.

NAMES. The Church publishes this list in Polish, so `local` is its own wording,
including the dash it sets between the two halves of a diocese's name, and
`name` is the English a reader of this site is given.
RANK AND A SECOND PAGE, 14 SEPTEMBER 2026. The Church calls each of the seven
in Poland a diecezja and the eighth a Prawosławny Ordynariat, and the rows
carry the English of those two words. Four rows cited only the Church's page
for the one diocese; its page of dioceses names all of them and each now cites
that as well.
"""

READ = "2026-09-14"

PL = "https://www.orthodox.pl/administracja/diecezje/"

ROWS = [

 dict(id="pl-warsaw-bielsk", parent="poland",
      name="Diocese of Warsaw and Bielsk",
      local=u"Diecezja Warszawsko–Bielska",
      rank="Diocese",
      seat="Warsaw", country="PL",
      address=[u"Al. Solidarności 52", u"03-402 Warszawa"],
      site="https://www.orthodox.pl/",
      sources=[PL + "diecezja-warszawsko-bielska/", PL]),

 dict(id="pl-bialystok-gdansk", parent="poland",
      name="Diocese of Bialystok and Gdansk",
      local=u"Diecezja Białostocko–Gdańska",
      rank="Diocese",
      seat="Bialystok", country="PL",
      address=[u"ul. Św. Mikołaja 3", u"15-419 Białystok"],
      site="https://orthodox.bialystok.pl/",
      sources=[PL + "diecezja-bialostocko-gdanskadiecezja-bialostocko-gdanska/",
               "https://orthodox.bialystok.pl/"]),

 dict(id="pl-lodz-poznan", parent="poland",
      name="Diocese of Lodz and Poznan",
      local=u"Diecezja Łódzko–Poznańska",
      rank="Diocese",
      seat="Lodz", country="PL",
      address=[u"ul. Narutowicza 46/1", u"90-135 Łódź"],
      site="https://diecezjalp.cerkiew.pl/",
      sources=[PL + "diecezja-lodzko-poznanska/",
               "https://diecezjalp.cerkiew.pl/"]),

 dict(id="pl-wroclaw-szczecin", parent="poland",
      name="Diocese of Wroclaw and Szczecin",
      local=u"Diecezja Wrocławsko–Szczecińska",
      rank="Diocese",
      seat="Wroclaw", country="PL",
      address=[u"ul. Św. Mikołaja 40", u"50-128 Wrocław"],
      site="https://www.diecezjawroclawsko-szczecinska.pl/",
      sources=[PL + "diecezja-wroclawsko-szczecinska/",
               "https://www.diecezjawroclawsko-szczecinska.pl/"]),

 dict(id="pl-przemysl-gorlice", parent="poland",
      name="Diocese of Przemysl and Gorlice",
      local=u"Diecezja Przemysko–Gorlicka",
      rank="Diocese",
      seat="Gorlice", country="PL",
      address=[u"ul. św. Maksyma 2", u"38-300 Gorlice"],
      sources=[PL + "diecezja-przemysko-gorlicka/", PL]),

 dict(id="pl-lublin-chelm", parent="poland",
      name="Diocese of Lublin and Chelm",
      local=u"Diecezja Lubelsko-Chełmska",
      rank="Diocese",
      seat="Lublin", country="PL",
      address=[u"ul. Ruska 15", u"20-126 Lublin"],
      sources=[PL + "diecezja-lubelsko-chelmska/", PL]),

 dict(id="pl-army-ordinariate", parent="poland",
      name="Orthodox Ordinariate of the Polish Army",
      local=u"Prawosławny Ordynariat Wojska Polskiego",
      rank="Ordinariate",
      seat="Warsaw", country="PL",
      address=[u"ul. Żwirki i Wigury 9/13", u"00-909 Warszawa"],
      sources=[PL + "prawoslawny-ordynariat-wojska-polskiego/", PL]),

 dict(id="pl-rio-recife", parent="poland",
      name="Missionary Diocese of Rio de Janeiro and Olinda-Recife",
      local=u"Diecezja Rio de Janeiro i Olinda\u2013Recife",
      rank="Diocese",
      seat="Rio de Janeiro", country="BR",
      address=[u"Rua Saint Romain n\u00ba 226",
               u"Copacobana, Rio de Janeiro (RJ)",
               u"CEP: 22071-060"],
      sources=[PL + "koscielne-jednostki-zagraniczne/", PL]),
]
