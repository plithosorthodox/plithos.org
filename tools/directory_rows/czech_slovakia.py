# -*- coding: utf-8 -*-
"""The eparchies of the Church of the Czech Lands and Slovakia.

Read on 14 September 2026 from the Church's own schematism at

    https://orthodox.sk/schematizmus/

which lists four eparchies - Presov and Michalovce-Kosice in Slovakia, Prague
and Olomouc-Brno in the Czech Lands - and links each to its own site. Four
rows are written here, and the Church had none before.

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
Church publishes for it, which carries its address anyway."""

READ = "2026-09-14"

SCH = "https://orthodox.sk/schematizmus/"

ROWS = [

 dict(id="cs-presov", parent="czech-slovakia",
      name="Eparchy of Presov",
      local=u"Prešovská pravoslávna eparchia",
      seat="Presov", country="SK",
      address=[u"Budovateľská 1", u"080 01 Prešov"],
      site="https://www.eparchiapo.sk/",
      sources=[SCH + "pe-pravoslavna-eparchia/", "https://www.eparchiapo.sk/"]),

 dict(id="cs-michalovce-kosice", parent="czech-slovakia",
      name="Eparchy of Michalovce and Kosice",
      local=u"Michalovsko-košická pravoslávna eparchia",
      seat="Michalovce", country="SK",
      address=[u"Duklianska 16", u"071 01 Michalovce"],
      sources=[SCH + "pravoslavna-eparchia/"]),

 dict(id="cs-prague", parent="czech-slovakia",
      name="Eparchy of Prague",
      local=u"Pražská pravoslávna eparchia",
      seat="Prague", country="CZ",
      sources=[SCH]),

 dict(id="cs-olomouc-brno", parent="czech-slovakia",
      name="Eparchy of Olomouc and Brno",
      local=u"Olomoucko-brněnská eparchie",
      seat="Olomouc", country="CZ",
      address=[u"Masarykova tř. 17", u"77900 OLOMOUC"],
      site="https://www.ob-eparchie.cz/",
      sources=["https://www.ob-eparchie.cz/kontakty/", SCH]),
]
