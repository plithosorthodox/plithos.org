# -*- coding: utf-8 -*-
"""The eparchies of the Church of Serbia.

Read on 14 September 2026 from the Patriarchate's own list of its eparchies,
which is published at spc.rs and answers here only from the Church's own
archive host over plain http:

    http://arhiva.spc.rs/sr/linkovi/linkovi_eparhija.html

That list holds 39 sees - one archbishopric, four metropolitanates and
thirty-four eparchies - each with the address of its own site where it keeps
one. Three of the thirty-nine were already published from North America
(Eastern America, Western America, New Gracanica and Midwestern America), so
36 rows are written here. 39 less 3 is the arithmetic a reader can repeat.

WHY THE ARCHIVE HOST. spc.rs refuses the request from this network: the
connection is opened and then closed with nothing sent, over http and https
alike, and its certificate arrives without its issuer besides. arhiva.spc.rs
is the same Church's own host, it answers over plain http, and the page it
serves at the address above carries the same 39 sees in the same order as the
Patriarchate's live page. Every row cites it. Nothing here was read off
another Church's directory.

THE SEES' OWN SITES. Each was requested at the address the Patriarchate
prints for it. Twenty-six answered and carry their own link; a further two
answer at an address the Patriarchate does not print - Branicevo at
sabornost.org, which the Patriarchate's list gives no link for at all, and
Zagreb and Ljubljana at its bare domain, where the www form returns 404.
Eight did not answer here and carry no link: Belgrade and Karlovci, Backa,
Srem, Sabac, Osijek-Polje and Baranja, Banja Luka, Britain and Scandinavia,
Timisoara. They are to be tried again, not written off.

Two of the addresses the Patriarchate prints must not be followed and the row
does not publish them. eparhija-slavonska.com now redirects to a German
physiotherapy practice, and spc.org.uk - which is not on the Patriarchate's
list but is the obvious address to try for Britain - answers with a page of
casino advertising. Both domains have been lost.

ADDRESSES are the lines each see prints on its own contact page, in the words
it prints them in, set out as an envelope wants them and translated nowhere.
The country line is dropped, because the page writes it in the reader's
language. Eighteen sees publish one; the other eighteen rows carry a name, a
country and a citation, which is a whole row.

NAMES. The Patriarchate publishes this list in Serbian only, so `local` is its
own wording and `name` is the English a reader of this site is given. `seat`
is written only where an address was read for it.

Raska and Prizren is filed under Serbia because that is where its own Church
lists it. A country code is a claim about a border and this site does not
make one.

BRITAIN AND SCANDINAVIA is one see here because the Patriarchate's own list
prints one. Reports of a division into two are not in any list this site has
read, and the bar for a row is a Church's own list and nothing else."""

READ = "2026-09-14"

SPC = "http://arhiva.spc.rs/sr/linkovi/linkovi_eparhija.html"

ROWS = [

 dict(id="sr-belgrade-karlovci", parent="serbia",
      name="Archbishopric of Belgrade and Karlovci",
      local=u"Архиепископија београдско-карловачка",
      seat="Belgrade", country="RS",
      sources=[SPC]),

 dict(id="sr-australia-new-zealand", parent="serbia",
      name="Metropolitanate of Australia and New Zealand",
      local=u"Митрополија аустралијско-новозеландска",
      seat="Cabramatta, New South Wales", country="AU",
      address=["3A Nance Avenue, Cabramatta, NSW 2166"],
      site="https://soc.org.au/",
      sources=["https://soc.org.au/contact-us/", SPC]),

 dict(id="sr-dabar-bosna", parent="serbia",
      name="Metropolitanate of Dabar-Bosna",
      local=u"Митрополија дабробосанска",
      seat="Sarajevo", country="BA",
      address=[u"Зелених беретки 3", u"71000 Сарајево"],
      site="https://www.mitropolijadabrobosanska.org/",
      sources=["https://www.mitropolijadabrobosanska.org/kontakt.html", SPC]),

 dict(id="sr-zagreb-ljubljana", parent="serbia",
      name="Metropolitanate of Zagreb and Ljubljana",
      local=u"Митрополија загребачко-љубљанска",
      seat="Zagreb", country="HR",
      address=[u"Илица 7/II", u"10000 Загреб"],
      site="https://mitropolija-zagrebacka.org/",
      sources=["https://mitropolija-zagrebacka.org/kontakti/", SPC]),

 dict(id="sr-montenegro-littoral", parent="serbia",
      name="Metropolitanate of Montenegro and the Littoral",
      local=u"Митрополија црногорско-приморска",
      seat="Cetinje", country="ME",
      address=[u"Дворски трг бр. 6", u"81250 Цетиње"],
      site="https://mitropolija.com/",
      sources=["https://mitropolija.com/kontakt/", SPC]),

 dict(id="sr-austria-switzerland", parent="serbia",
      name="Eparchy of Austria and Switzerland",
      local=u"Епархија аустријско-швајцарска",
      seat="Vienna", country="AT",
      address=["Veithgasse 3, 1030 Wien"],
      site="http://www.crkva.at/",
      sources=["http://www.crkva.at/de/kontakt-sr/", SPC]),

 dict(id="sr-banat", parent="serbia",
      name="Eparchy of Banat",
      local=u"Епархија банатска",
      country="RS",
      site="https://www.eparhijabanatska.rs/",
      sources=["https://www.eparhijabanatska.rs/", SPC]),

 dict(id="sr-banja-luka", parent="serbia",
      name="Eparchy of Banja Luka",
      local=u"Епархија бањалучка",
      country="BA",
      sources=[SPC]),

 dict(id="sr-backa", parent="serbia",
      name="Eparchy of Backa",
      local=u"Епархија бачка",
      country="RS",
      sources=[SPC]),

 dict(id="sr-bihac-petrovac", parent="serbia",
      name="Eparchy of Bihac and Petrovac",
      local=u"Епархија бихаћко-петровачка",
      seat="Bosanski Petrovac", country="BA",
      address=[u"ул. Марка Јокића бр. 51.", u"Бос. Петровац, 77250, Ф БиХ"],
      site="https://www.eparhijabihackopetrovacka.org/",
      sources=["https://www.eparhijabihackopetrovacka.org/kontakt/", SPC]),

 dict(id="sr-branicevo", parent="serbia",
      name="Eparchy of Branicevo",
      local=u"Епархија браничевска",
      seat=u"Pozarevac", country="RS",
      address=[u"ул. Страхињића Бана ББ", u"12000 Пожаревац"],
      site="https://www.sabornost.org/global/",
      sources=["https://www.sabornost.org/global/kontakt", SPC]),

 dict(id="sr-britain-scandinavia", parent="serbia",
      name="Eparchy of Britain and Scandinavia",
      local=u"Епархија британско-скандинавска",
      seat="London", country="GB",
      sources=[SPC]),

 dict(id="sr-buda", parent="serbia",
      name="Eparchy of Buda",
      local=u"Епархија будимска",
      seat="Szentendre", country="HU",
      address=[u"Pátriárka u. 5.", u"2000 Szentendre, Pf. 22"],
      site="https://www.serbdiocese.hu/",
      sources=["https://www.serbdiocese.hu/kontakt/", SPC]),

 dict(id="sr-budimlja-niksic", parent="serbia",
      name="Eparchy of Budimlja and Niksic",
      local=u"Епархија будимљанско-никшићка",
      seat="Berane", country="ME",
      address=[u"84300 Беране"],
      site="https://www.eparhija.me/",
      sources=["https://www.eparhija.me/index.php/contact", SPC]),

 dict(id="sr-buenos-aires", parent="serbia",
      name="Eparchy of Buenos Aires",
      local=u"Епархија буенос-ајреска",
      seat="Buenos Aires", country="AR",
      address=[u"calle 15 de Noviembre de 1889 - N° 1536",
               u"(1130) Ciudad Autónoma de Buenos Aires"],
      site="https://www.iglesiaortodoxaserbiasca.org/",
      sources=["https://www.iglesiaortodoxaserbiasca.org/", SPC]),

 dict(id="sr-valjevo", parent="serbia",
      name="Eparchy of Valjevo",
      local=u"Епархија ваљевска",
      seat="Valjevo", country="RS",
      address=[u"Трг Св. Владике Николаја бр.2", u"14000 Ваљево"],
      site="https://www.eparhijavaljevska.rs/",
      sources=["https://www.eparhijavaljevska.rs/index.php/kontakt/", SPC]),

 dict(id="sr-vranje", parent="serbia",
      name="Eparchy of Vranje",
      local=u"Епархија врањска",
      country="RS",
      site="http://www.eparhijavranjska.org/",
      sources=["http://www.eparhijavranjska.org/", SPC]),

 dict(id="sr-gornji-karlovac", parent="serbia",
      name="Eparchy of Gornji Karlovac",
      local=u"Епархија горњокарловачка",
      seat="Karlovac", country="HR",
      address=[u"Вјекослава Клаића 4а", u"47000 Карловац"],
      site="https://www.eparhija-gornjokarlovacka.hr/",
      sources=["https://www.eparhija-gornjokarlovacka.hr/adresar/", SPC]),

 dict(id="sr-dalmatia", parent="serbia",
      name="Eparchy of Dalmatia",
      local=u"Епархија далматинска",
      country="HR",
      site="http://www.eparhija-dalmatinska.hr/",
      sources=["http://www.eparhija-dalmatinska.hr/", SPC]),

 dict(id="sr-dusseldorf-germany", parent="serbia",
      name="Eparchy of Duesseldorf and Germany",
      local=u"Епархија диселдорфска и немачка",
      country="DE",
      site="https://eparhija-nemacka.com/",
      sources=["https://eparhija-nemacka.com/", SPC]),

 dict(id="sr-zica", parent="serbia",
      name="Eparchy of Zica",
      local=u"Епархија жичка",
      seat="Kraljevo", country="RS",
      address=[u"ул. Доситејева 5е", u"36000 Краљево"],
      site="https://eparhija-zicka.rs/",
      sources=["https://eparhija-zicka.rs/kontakt3/", SPC]),

 dict(id="sr-western-europe", parent="serbia",
      name="Eparchy of Western Europe",
      local=u"Епархија западноевропска",
      seat="Paris", country="FR",
      address=[u"23 rue du Simplon", u"75018 Paris"],
      site="https://dioceseserbe.org/",
      sources=["https://dioceseserbe.org/kontakt/", SPC]),

 dict(id="sr-zahumlje-herzegovina", parent="serbia",
      name="Eparchy of Zahumlje and Herzegovina",
      local=u"Епархија захумско-херцеговачка",
      seat="Trebinje", country="BA",
      address=[u"Епархијски дом, ул. Светосавска бр. 4", u"89101 Требиње"],
      site="https://eparhija-zahumskohercegovacka.org/",
      sources=["https://eparhija-zahumskohercegovacka.org/kontakt/", SPC]),

 dict(id="sr-zvornik-tuzla", parent="serbia",
      name="Eparchy of Zvornik and Tuzla",
      local=u"Епархија зворничко-тузланска",
      seat="Bijeljina", country="BA",
      address=[u"Улица Патријарха Павла број 40", u"76300 Бијељина"],
      site="https://www.eparhijazt.com/",
      sources=["https://www.eparhijazt.com/sr/12.kontakt.html", SPC]),

 dict(id="sr-canada", parent="serbia",
      name="Eparchy of Canada",
      local=u"Епархија канадска",
      country="CA",
      site="https://istocnik.ca/sr/",
      sources=["https://istocnik.ca/sr/", SPC]),

 dict(id="sr-krusevac", parent="serbia",
      name="Eparchy of Krusevac",
      local=u"Епархија крушевачка",
      seat="Krusevac", country="RS",
      address=[u"ул. Доситејева бр. 1", u"37000 Крушевац"],
      site="http://www.eparhijakrusevacka.com/",
      sources=["http://www.eparhijakrusevacka.com/", SPC]),

 dict(id="sr-milesevo", parent="serbia",
      name="Eparchy of Mileseva",
      local=u"Епархија милешевска",
      country="RS",
      site="http://milesevskaeparhija.rs/",
      sources=["http://milesevskaeparhija.rs/", SPC]),

 dict(id="sr-nis", parent="serbia",
      name="Eparchy of Nis",
      local=u"Епархија нишка",
      seat="Nis", country="RS",
      address=[u"Епископска бр.3", u"18105 Ниш"],
      site="https://eparhijaniska.rs/",
      sources=["https://eparhijaniska.rs/eparhija/kontakt-informacije", SPC]),

 dict(id="sr-osijek-baranja", parent="serbia",
      name="Eparchy of Osijek-Polje and Baranja",
      local=u"Епархија осечкопољска и барањска",
      country="HR",
      sources=[SPC]),

 dict(id="sr-raska-prizren", parent="serbia",
      name="Eparchy of Raska and Prizren",
      local=u"Епархија рашко-призренска",
      seat="Gracanica", country="RS",
      address=[u"Улица Цара Лазара бб", u"38 205 Грачаница"],
      site="https://eparhija-prizren.com/sr/",
      sources=["https://eparhija-prizren.com/sr/kontakt/", SPC]),

 dict(id="sr-slavonia", parent="serbia",
      name="Eparchy of Slavonia",
      local=u"Епархија славонска",
      country="HR",
      sources=[SPC]),

 dict(id="sr-srem", parent="serbia",
      name="Eparchy of Srem",
      local=u"Епархија сремска",
      country="RS",
      sources=[SPC]),

 dict(id="sr-timok", parent="serbia",
      name="Eparchy of Timok",
      local=u"Епархија тимочка",
      seat="Zajecar", country="RS",
      address=[u"ул. Тимочке буне бр. 6", u"19000 Зајечар"],
      site="https://eparhija-timocka.org/",
      sources=["https://eparhija-timocka.org/kontakt/", SPC]),

 dict(id="sr-timisoara", parent="serbia",
      name="Eparchy of Timisoara",
      local=u"Епархија темишварска",
      country="RO",
      sources=[SPC]),

 dict(id="sr-sabac", parent="serbia",
      name="Eparchy of Sabac",
      local=u"Епархија шабачка",
      country="RS",
      sources=[SPC]),

 dict(id="sr-sumadija", parent="serbia",
      name="Eparchy of Sumadija",
      local=u"Епархија шумадијска",
      seat="Kragujevac", country="RS",
      address=[u"ул. Краља Александра I Карађорђевића 31а", u"34000 Крагујевац"],
      site="https://www.eparhija-sumadijska.org.rs/",
      sources=["https://www.eparhija-sumadijska.org.rs/index.php/kontakt/eparhija",
               SPC]),
]
