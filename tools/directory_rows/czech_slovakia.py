# -*- coding: utf-8 -*-
"""The eparchies of the Church of the Czech Lands and Slovakia.

Read on 14 September 2026 from the Church's own schematism at

    https://orthodox.sk/schematizmus/

which lists four eparchies - Presov and Michalovce-Kosice in Slovakia, Prague
and Olomouc-Brno in the Czech Lands - and links each to its own site. Four
rows are written here, and the Church had none before.

THE COUNT IS FOUR AND THE CHURCH'S OWN CONSTITUTION IS WHERE IT WAS CHECKED.
The Ústava, which the Church publishes at orthodox.sk/pravoslavna-cirkev/
ustava/, states no number in a sentence, but its own account of how the four
came to be does: the Prague eparchy and the eparchy of Mukačevo and Prešov
between the wars, Olomouc-Brno set apart from the Czech eparchy on 7 December
1949, Prešov constituted separately in 1950, and Michalovce on 28 and 29 July
1950. It then says that the Constitution of 1951, under which autocephaly was
declared, was received by "zástupcami eparchií pražskej, olomoucko-brnenskej,
prešovskej a michalovskej" - the representatives of those four eparchies and
no others. The schematism, the site's own navigation and the Constitution's
history all name the same four, so this file is complete.

THE CHURCH HAS TWO HALVES AND THEY ARE NOT SEES. Article 1 of the Ústava says
the Church "sa administratívne člení na dve rovnocenné územné časti: na
eparchie v Českej republike a na eparchie v Slovenskej republike", each with a
metropolitan council of its own, and below them arcidekanáty, dekanáty and
parishes. That is a body between the Church and its eparchies in the sense of
administration, and it is not one in the sense this register lists: neither
half has a bishop of its own or a see, both are governed by the one Holy Synod
under the one metropolitan, and naming them would put two rows on the page
that no reader could write to. So the four eparchies hang off the Church
itself, and this note is here so the next pass does not have to find the
article again.

THE CHURCH'S CZECH SITE CANNOT BE READ FROM HERE. pravoslavnacirkev.cz answers
every request, over http and https alike, with a Cloudflare challenge page, so
the whole of this was read from the Church's Slovak site, which is the same
Church and answers freely. The Prague eparchy's own site, pp-eparchie.cz,
answers 502 at every address tried and is not published; that row carries the
Church's schematism as its link, and is to be tried again rather than written
off.

ADDRESSES. The schematism prints the seat of each Slovak eparchy at the head of
its entry, under the word USTREDIE, and those are the two addresses here; the
Olomouc-Brno address is the eparchial office as its own site prints it, in the
lettering it uses - the town in capitals - and stands that way. Prague
publishes none that could be read, and that row carries a name, a country and
a citation, which is a whole row. The country line is dropped from each,
because the page writes it in the reader's language.

NAMES. `local` is the wording of the list it was read from, which is Slovak,
except for Olomouc-Brno, which was read from its own site and gives itself its
Czech name there. The Prague eparchy is therefore named here in Slovak, which
is what the only list this site could read prints; its own Czech wording is to
be taken from its own site when that site answers again.

SITES. Presov answers at eparchiapo.sk and Olomouc-Brno at ob-eparchie.cz,
which is the address its own pages at eparchie-ob.eu send a reader to and where
its contacts are kept. Michalovce and Kosice publishes news.mkpe.sk, which
refuses the request here, so that row falls back to the schematism entry the
Church publishes for it, which carries its address anyway.
RANK AND A SECOND PAGE, 14 SEPTEMBER 2026. All four are eparchies in this
Church's own word and the rows say so. Michalovce and Kosice cited only its
own page and now cites the Schematismus, which names all four. Prague keeps
one citation and there is no honest second: its own site at pp-eparchie.cz
answers a 502 from here, the Czech half of the Church at pravoslavnacirkev.cz
refuses the request outright, and the only other page that names it is the
menu that stands on every page of the Slovak site, which is not a second
source but the same one again.
"""

READ = "2026-09-14"

SCH = "https://orthodox.sk/schematizmus/"

ROWS = [

 dict(id="cs-presov", parent="czech-slovakia",
      name="Eparchy of Presov",
      local=u"Prešovská pravoslávna eparchia",
      rank="Eparchy",
      seat="Presov", country="SK",
      address=[u"Budovateľská 1", u"080 01 Prešov"],
      site="https://www.eparchiapo.sk/",
      sources=[SCH + "pe-pravoslavna-eparchia/", "https://www.eparchiapo.sk/"]),

 dict(id="cs-michalovce-kosice", parent="czech-slovakia",
      name="Eparchy of Michalovce and Kosice",
      local=u"Michalovsko-košická pravoslávna eparchia",
      rank="Eparchy",
      seat="Michalovce", country="SK",
      address=[u"Duklianska 16", u"071 01 Michalovce"],
      sources=[SCH + "pravoslavna-eparchia/", SCH]),

 dict(id="cs-prague", parent="czech-slovakia",
      name="Eparchy of Prague",
      local=u"Pražská pravoslávna eparchia",
      rank="Eparchy",
      seat="Prague", country="CZ",
      sources=[SCH]),

 dict(id="cs-olomouc-brno", parent="czech-slovakia",
      name="Eparchy of Olomouc and Brno",
      local=u"Olomoucko-brněnská eparchie",
      rank="Eparchy",
      seat="Olomouc", country="CZ",
      address=[u"Masarykova tř. 17", u"77900 OLOMOUC"],
      site="https://www.ob-eparchie.cz/",
      sources=["https://www.ob-eparchie.cz/kontakty/", SCH]),
]
