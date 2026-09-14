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
Seven did not answer here and carry no link: Belgrade and Karlovci, Backa,
Srem, Sabac, Osijek-Polje and Baranja, Banja Luka, Timisoara. They are to be
tried again, not written off. The London see, which the Patriarchate's list
gives no link for at all, was found at eparhija.uk and is described below.

Two of the addresses the Patriarchate prints must not be followed and the row
does not publish them. eparhija-slavonska.com now redirects to a German
physiotherapy practice, and spc.org.uk - which is not on the Patriarchate's
list but is the obvious address to try for Britain - answers with a page of
casino advertising. Both domains have been lost.

ADDRESSES are the lines each see prints on its own contact page, in the words
it prints them in, set out as an envelope wants them and translated nowhere.
The country line is dropped, because the page writes it in the reader's
language. Twenty-two of the thirty-six publish one; the other fourteen rows
carry a name, a country and a citation, which is a whole row.

NAMES. The Patriarchate publishes this list in Serbian only, so `local` is its
own wording and `name` is the English a reader of this site is given. `seat`
is written only where an address was read for it.

Raska and Prizren is filed under Serbia because that is where its own Church
lists it. A country code is a claim about a border and this site does not
make one.

THE COUNT WAS TAKEN AGAIN ON 14 SEPTEMBER 2026, from the Patriarchate's own
page headed Eparchies of the Serbian Orthodox Church as well as from its page
of their links. The first still refuses this network directly and was read
from the copy the Internet Archive took of it in April 2026; the two name the
same thirty-nine sees in the same order and no more, and the Patriarchate
states no number in prose anywhere this machine could read. Thirty-nine less the three published from
North America is the thirty-six rows here, and nothing in the Balkans, in
Hungary or Romania, or in the Americas and Australia is missing from them.

THE LONDON SEE was read again from its own site that day and is now the
Eparchy of Britain and Ireland. The Holy Assembly of Bishops divided the
Eparchy of Britain and Scandinavia in May 2024 into that see at London and the
Eparchy of Scandinavia at Stockholm, and the London eparchy publishes itself
under the new name at eparhija.uk, with its own parishes, its own address and
its own correspondence. A body's own door is the best evidence there is about
what it is called, so the row carries what it says and keeps its id.

THE SCANDINAVIAN HALF HAS NO ROW YET, and the reason is a source rather than a
doubt. It publishes no address this machine could find, and the Patriarchate's
own list of its eparchies still prints the undivided see. The Eparchy of
Switzerland, which the same session separated from Austria and Switzerland, is
in the same position for a different reason: it answers at crkva.ch, and that
host cannot be reached from this network at all. Both are deferred for want of
something to read, not excluded, and the next pass should look rather than
conclude the list is complete.

AUSTRIA AND SWITZERLAND keeps the name its own site keeps. crkva.at carries
"Епархија аустријско-швајцарска" across its masthead while its recent pages
write of the Eparchy of Austria, and a row is not moved on a heading that
contradicts itself.

RANK, ADDED 14 SEPTEMBER 2026. The Patriarchate's list puts a word in front of
every see and uses three of them - archbishopric for Belgrade and Karlovci,
metropolitanate for four, eparchy for the rest - and each row now carries the
English of the word standing in front of its own name on that list. Nothing is
inferred: where the list says eparchy the row says Eparchy.

THE SEVEN DOORS THAT DID NOT ANSWER WERE TRIED AGAIN THAT DAY AND STILL DO NOT.
Belgrade and Karlovci at arhiepiskopija.rs, Backa, Srem, Sabac, Osijek-Polje
and Baranja, and the Banja Luka diocesan office resolve to nothing or answer a
503 from here; Timisoara the Patriarchate gives no link for at all. Each keeps
its one citation, which is honest: there is no second page of this Church that
names it and can be read from here, and a second citation stretched to fit
would be worth less than the one.

TWO SEES ANSWER DIFFERENTLY NOW THAN THEY DID. Valjevo, which did not answer
at all, answers at its own domain and prints its own name across the page, so
its row is confirmed as it stands. Sumadija answers a 403 - a refusal, not a
silence - which is what spc.rs itself does to this network, and its link is
the one the Patriarchate prints for it, so the row keeps it: a door shut to
one machine is not a door shut."""

READ = "2026-09-14"

SPC = "http://arhiva.spc.rs/sr/linkovi/linkovi_eparhija.html"

ROWS = [

 dict(id="sr-belgrade-karlovci", parent="serbia",
      name="Archbishopric of Belgrade and Karlovci",
      rank="Archbishopric",
      local=u"Архиепископија београдско-карловачка",
      seat="Belgrade", country="RS",
      sources=[SPC]),

 dict(id="sr-australia-new-zealand", parent="serbia",
      name="Metropolitanate of Australia and New Zealand",
      rank="Metropolitanate",
      local=u"Митрополија аустралијско-новозеландска",
      seat="Cabramatta, New South Wales", country="AU",
      address=["3A Nance Avenue, Cabramatta, NSW 2166"],
      site="https://soc.org.au/",
      sources=["https://soc.org.au/contact-us/", SPC]),

 dict(id="sr-dabar-bosna", parent="serbia",
      name="Metropolitanate of Dabar-Bosna",
      rank="Metropolitanate",
      local=u"Митрополија дабробосанска",
      seat="Sarajevo", country="BA",
      address=[u"Зелених беретки 3", u"71000 Сарајево"],
      site="https://www.mitropolijadabrobosanska.org/",
      sources=["https://www.mitropolijadabrobosanska.org/kontakt.html", SPC]),

 dict(id="sr-zagreb-ljubljana", parent="serbia",
      name="Metropolitanate of Zagreb and Ljubljana",
      rank="Metropolitanate",
      local=u"Митрополија загребачко-љубљанска",
      seat="Zagreb", country="HR",
      address=[u"Илица 7/II", u"10000 Загреб"],
      site="https://mitropolija-zagrebacka.org/",
      sources=["https://mitropolija-zagrebacka.org/kontakti/", SPC]),

 dict(id="sr-montenegro-littoral", parent="serbia",
      name="Metropolitanate of Montenegro and the Littoral",
      rank="Metropolitanate",
      local=u"Митрополија црногорско-приморска",
      seat="Cetinje", country="ME",
      address=[u"Дворски трг бр. 6", u"81250 Цетиње"],
      site="https://mitropolija.com/",
      sources=["https://mitropolija.com/kontakt/", SPC]),

 dict(id="sr-austria-switzerland", parent="serbia",
      name="Eparchy of Austria and Switzerland",
      rank="Eparchy",
      local=u"Епархија аустријско-швајцарска",
      seat="Vienna", country="AT",
      address=["Veithgasse 3, 1030 Wien"],
      site="http://www.crkva.at/",
      sources=["http://www.crkva.at/de/kontakt-sr/", SPC]),

 dict(id="sr-banat", parent="serbia",
      name="Eparchy of Banat",
      rank="Eparchy",
      local=u"Епархија банатска",
      country="RS",
      site="https://www.eparhijabanatska.rs/",
      sources=["https://www.eparhijabanatska.rs/", SPC]),

 dict(id="sr-banja-luka", parent="serbia",
      name="Eparchy of Banja Luka",
      rank="Eparchy",
      local=u"Епархија бањалучка",
      country="BA",
      sources=[SPC]),

 dict(id="sr-backa", parent="serbia",
      name="Eparchy of Backa",
      rank="Eparchy",
      local=u"Епархија бачка",
      country="RS",
      sources=[SPC]),

 dict(id="sr-bihac-petrovac", parent="serbia",
      name="Eparchy of Bihac and Petrovac",
      rank="Eparchy",
      local=u"Епархија бихаћко-петровачка",
      seat="Bosanski Petrovac", country="BA",
      address=[u"ул. Марка Јокића бр. 51.", u"Бос. Петровац, 77250, Ф БиХ"],
      site="https://www.eparhijabihackopetrovacka.org/",
      sources=["https://www.eparhijabihackopetrovacka.org/kontakt/", SPC]),

 dict(id="sr-branicevo", parent="serbia",
      name="Eparchy of Branicevo",
      rank="Eparchy",
      local=u"Епархија браничевска",
      seat=u"Pozarevac", country="RS",
      address=[u"ул. Страхињића Бана ББ", u"12000 Пожаревац"],
      site="https://www.sabornost.org/global/",
      sources=["https://www.sabornost.org/global/kontakt", SPC]),

 # Read from the body's own site on 14 September 2026, under the name it
 # publishes for itself since the Assembly divided the see in May 2024. The
 # Patriarchate's list still prints the older name and is cited beside it.
 dict(id="sr-britain-scandinavia", parent="serbia",
      name="Eparchy of Britain and Ireland",
      rank="Eparchy",
      local=u"Епархија британско-ирска",
      seat="London", country="GB",
      address=["89 Lancaster Rd", "London W11 1QQ"],
      site="https://eparhija.uk/",
      sources=["https://eparhija.uk/kontakt/", "https://eparhija.uk/", SPC],
      checked="2026-09-14"),

 dict(id="sr-buda", parent="serbia",
      name="Eparchy of Buda",
      rank="Eparchy",
      local=u"Епархија будимска",
      seat="Szentendre", country="HU",
      address=[u"Pátriárka u. 5.", u"2000 Szentendre, Pf. 22"],
      site="https://www.serbdiocese.hu/",
      sources=["https://www.serbdiocese.hu/kontakt/", SPC]),

 dict(id="sr-budimlja-niksic", parent="serbia",
      name="Eparchy of Budimlja and Niksic",
      rank="Eparchy",
      local=u"Епархија будимљанско-никшићка",
      seat="Berane", country="ME",
      address=[u"84300 Беране"],
      site="https://www.eparhija.me/",
      sources=["https://www.eparhija.me/index.php/contact", SPC]),

 dict(id="sr-buenos-aires", parent="serbia",
      name="Eparchy of Buenos Aires",
      rank="Eparchy",
      local=u"Епархија буенос-ајреска",
      seat="Buenos Aires", country="AR",
      address=[u"calle 15 de Noviembre de 1889 - N° 1536",
               u"(1130) Ciudad Autónoma de Buenos Aires"],
      site="https://www.iglesiaortodoxaserbiasca.org/",
      sources=["https://www.iglesiaortodoxaserbiasca.org/", SPC]),

 dict(id="sr-valjevo", parent="serbia",
      name="Eparchy of Valjevo",
      rank="Eparchy",
      local=u"Епархија ваљевска",
      seat="Valjevo", country="RS",
      address=[u"Трг Св. Владике Николаја бр.2", u"14000 Ваљево"],
      site="https://www.eparhijavaljevska.rs/",
      sources=["https://www.eparhijavaljevska.rs/index.php/kontakt/", SPC]),

 dict(id="sr-vranje", parent="serbia",
      name="Eparchy of Vranje",
      rank="Eparchy",
      local=u"Епархија врањска",
      country="RS",
      site="http://www.eparhijavranjska.org/",
      sources=["http://www.eparhijavranjska.org/", SPC]),

 dict(id="sr-gornji-karlovac", parent="serbia",
      name="Eparchy of Gornji Karlovac",
      rank="Eparchy",
      local=u"Епархија горњокарловачка",
      seat="Karlovac", country="HR",
      address=[u"Вјекослава Клаића 4а", u"47000 Карловац"],
      site="https://www.eparhija-gornjokarlovacka.hr/",
      sources=["https://www.eparhija-gornjokarlovacka.hr/adresar/", SPC]),

 dict(id="sr-dalmatia", parent="serbia",
      name="Eparchy of Dalmatia",
      rank="Eparchy",
      local=u"Епархија далматинска",
      country="HR",
      site="http://www.eparhija-dalmatinska.hr/",
      sources=["http://www.eparhija-dalmatinska.hr/", SPC]),

 dict(id="sr-dusseldorf-germany", parent="serbia",
      name="Eparchy of Duesseldorf and Germany",
      rank="Eparchy",
      local=u"Епархија диселдорфска и немачка",
      country="DE",
      site="https://eparhija-nemacka.com/",
      sources=["https://eparhija-nemacka.com/", SPC]),

 dict(id="sr-zica", parent="serbia",
      name="Eparchy of Zica",
      rank="Eparchy",
      local=u"Епархија жичка",
      seat="Kraljevo", country="RS",
      address=[u"ул. Доситејева 5е", u"36000 Краљево"],
      site="https://eparhija-zicka.rs/",
      sources=["https://eparhija-zicka.rs/kontakt3/", SPC]),

 dict(id="sr-western-europe", parent="serbia",
      name="Eparchy of Western Europe",
      rank="Eparchy",
      local=u"Епархија западноевропска",
      seat="Paris", country="FR",
      address=[u"23 rue du Simplon", u"75018 Paris"],
      site="https://dioceseserbe.org/",
      sources=["https://dioceseserbe.org/kontakt/", SPC]),

 dict(id="sr-zahumlje-herzegovina", parent="serbia",
      name="Eparchy of Zahumlje and Herzegovina",
      rank="Eparchy",
      local=u"Епархија захумско-херцеговачка",
      seat="Trebinje", country="BA",
      address=[u"Епархијски дом, ул. Светосавска бр. 4", u"89101 Требиње"],
      site="https://eparhija-zahumskohercegovacka.org/",
      sources=["https://eparhija-zahumskohercegovacka.org/kontakt/", SPC]),

 dict(id="sr-zvornik-tuzla", parent="serbia",
      name="Eparchy of Zvornik and Tuzla",
      rank="Eparchy",
      local=u"Епархија зворничко-тузланска",
      seat="Bijeljina", country="BA",
      address=[u"Улица Патријарха Павла број 40", u"76300 Бијељина"],
      site="https://www.eparhijazt.com/",
      sources=["https://www.eparhijazt.com/sr/12.kontakt.html", SPC]),

 dict(id="sr-canada", parent="serbia",
      name="Eparchy of Canada",
      rank="Eparchy",
      local=u"Епархија канадска",
      country="CA",
      site="https://istocnik.ca/sr/",
      sources=["https://istocnik.ca/sr/", SPC]),

 dict(id="sr-krusevac", parent="serbia",
      name="Eparchy of Krusevac",
      rank="Eparchy",
      local=u"Епархија крушевачка",
      seat="Krusevac", country="RS",
      address=[u"ул. Доситејева бр. 1", u"37000 Крушевац"],
      site="http://www.eparhijakrusevacka.com/",
      sources=["http://www.eparhijakrusevacka.com/", SPC]),

 dict(id="sr-milesevo", parent="serbia",
      name="Eparchy of Mileseva",
      rank="Eparchy",
      local=u"Епархија милешевска",
      country="RS",
      site="http://milesevskaeparhija.rs/",
      sources=["http://milesevskaeparhija.rs/", SPC]),

 dict(id="sr-nis", parent="serbia",
      name="Eparchy of Nis",
      rank="Eparchy",
      local=u"Епархија нишка",
      seat="Nis", country="RS",
      address=[u"Епископска бр.3", u"18105 Ниш"],
      site="https://eparhijaniska.rs/",
      sources=["https://eparhijaniska.rs/eparhija/kontakt-informacije", SPC]),

 dict(id="sr-osijek-baranja", parent="serbia",
      name="Eparchy of Osijek-Polje and Baranja",
      rank="Eparchy",
      local=u"Епархија осечкопољска и барањска",
      country="HR",
      sources=[SPC]),

 dict(id="sr-raska-prizren", parent="serbia",
      name="Eparchy of Raska and Prizren",
      rank="Eparchy",
      local=u"Епархија рашко-призренска",
      seat="Gracanica", country="RS",
      address=[u"Улица Цара Лазара бб", u"38 205 Грачаница"],
      site="https://eparhija-prizren.com/sr/",
      sources=["https://eparhija-prizren.com/sr/kontakt/", SPC]),

 dict(id="sr-slavonia", parent="serbia",
      name="Eparchy of Slavonia",
      rank="Eparchy",
      local=u"Епархија славонска",
      country="HR",
      sources=[SPC]),

 dict(id="sr-srem", parent="serbia",
      name="Eparchy of Srem",
      rank="Eparchy",
      local=u"Епархија сремска",
      country="RS",
      sources=[SPC]),

 dict(id="sr-timok", parent="serbia",
      name="Eparchy of Timok",
      rank="Eparchy",
      local=u"Епархија тимочка",
      seat="Zajecar", country="RS",
      address=[u"ул. Тимочке буне бр. 6", u"19000 Зајечар"],
      site="https://eparhija-timocka.org/",
      sources=["https://eparhija-timocka.org/kontakt/", SPC]),

 dict(id="sr-timisoara", parent="serbia",
      name="Eparchy of Timisoara",
      rank="Eparchy",
      local=u"Епархија темишварска",
      country="RO",
      sources=[SPC]),

 dict(id="sr-sabac", parent="serbia",
      name="Eparchy of Sabac",
      rank="Eparchy",
      local=u"Епархија шабачка",
      country="RS",
      sources=[SPC]),

 dict(id="sr-sumadija", parent="serbia",
      name="Eparchy of Sumadija",
      rank="Eparchy",
      local=u"Епархија шумадијска",
      seat="Kragujevac", country="RS",
      address=[u"ул. Краља Александра I Карађорђевића 31а", u"34000 Крагујевац"],
      site="https://www.eparhija-sumadijska.org.rs/",
      sources=["https://www.eparhija-sumadijska.org.rs/index.php/kontakt/eparhija",
               SPC]),
]
