# -*- coding: utf-8 -*-
"""The dioceses of the Macedonian Orthodox Church - Ohrid Archbishopric.

THE COUNT IS TWELVE AND THE ARCHBISHOPRIC SAYS SO IN PROSE. Its own account
of itself, "MPC denes", at

    http://www.mpc.org.mk/MPC/mpc-denes.asp

says in as many words: "МПЦ-ОА пастирски е организирана во 12 епархии, од
кои 8 на територијата на Р. Северна Македонија, и 4 во дијаспората" - the
Church is organised in twelve dioceses, eight in North Macedonia and four
abroad - and then numbers all twelve, each with the hierarch who heads it.
Twelve rows are written here.

THE PAGE OF LINKS SAYS ELEVEN, AND IT IS THE STALER OF THE TWO. The list at
/MPC/eparhii.asp, which answers over plain http and not over https, carries
eight dioceses in North Macedonia and three abroad. The one it does not
carry is the Australian-Sydney diocese, which the prose list numbers twelfth
and the Archbishopric's own roll of its hierarchy names as well. A page of
links is a menu and goes stale a diocese at a time; what a Church says about
itself in a sentence is what this file counts by.

Two older lists on the same site were not used and are the reason to read the
navigation rather than the page body. The site's own sidebar, and the English
page of dioceses at English/dioceses.asp, both print an earlier division into
seven - with Polog and Kumanovo undivided and Debar without Kicevo - which the
Archbishopric's current list has replaced. The English names here follow that
English page where it and the current list agree.

THE FOUR ABROAD ARE NO LONGER DEFERRED. They were held for want of any
published location, on the ground that a row has to name a country. The
Archbishopric publishes no address for any of them and no page saying where
any of them sits, so each country here is said plainly and is the weakest
thing on its row:

  - America and Canada is filed under Canada, because the only thing the
    Archbishopric itself publishes about where that diocese is centred is
    its own English report of that diocese's assembly, which closes "in the
    hall at St. Clement of Ohrid's cathedral in Toronto". A cathedral is a
    seat; the report is from 2003, and the row is to be read again from the
    diocese's own site when one answers.
  - Europe is filed under Sweden, and its seat is Malmo, because the
    Archbishopric's own page for that diocese reports the building and then
    the opening of "the cathedral of the Macedonian Orthodox Diocese for
    Europe" - the church of St Naum of Ohrid at Malmo, which it calls in one
    headline "the new cathedral church in Malmo, Sweden".
  - Australia and New Zealand is filed under Australia and carries no seat.
    The see names two countries, the row must name one, and Australia is
    where the Archbishopric's other Australian see sits. Nothing on any page
    read here says where it is centred.
  - Australia and Sydney is filed under Australia with Sydney as its seat,
    which is the city its own name gives it.

SITES, AND ONE THAT MUST NOT BE FOLLOWED. Three dioceses answered at the
address the Archbishopric prints for them: Debar and Kicevo, Povardarie, and
Bregalnica. Tetovo and Gostivar has no site of its own and the Archbishopric
gives it a page on the Archbishopric's own site, which is what that row
links. Four addresses the Archbishopric prints are gone: spe.org.mk for
Skopje, josif.mk for Kumanovo and Osogovo, and mpceanz.org.au for the
Australian-New Zealand diocese do not resolve at all, and akmpe.org, printed
for the American-Canadian diocese, answers 200 and is an advertising site in
other hands. None of the four is published here. The four rows written now
carry no link and fall back to the Archbishopric, which is where they were
read.

ADDRESSES. The Archbishopric publishes none, and only Bregalnica prints one on
its own site. Eleven rows carry a name, a country and a citation, which is a
whole row. SEATS are given only where a see is named for the city it sits in
or where an address or a cathedral was read; Prespa and Pelagonia, Debar and
Kicevo, Povardarie and the Australian-New Zealand diocese are not placed on
any page read here."""

READ = "2026-09-14"

MPC = "http://www.mpc.org.mk/MPC/eparhii.asp"

# The Archbishopric's own account of itself, and the sentence that counts
# its dioceses.
DENES = "http://www.mpc.org.mk/MPC/mpc-denes.asp"

# The Archbishopric's own page for the diocese in Europe, and its own
# English report of the American-Canadian diocese's assembly.
EUROPE = "http://mpc.org.mk/europe-aktuelno.asp"
ACMOD = "http://www.mpc.org.mk/English/news2.asp?id=101"

ROWS = [

 dict(id="mk-skopje", parent="macedonia",
      name="Diocese of Skopje",
      local=u"Скопска епархија",
      seat="Skopje", country="MK",
      sources=[MPC]),

 dict(id="mk-prespa-pelagonia", parent="macedonia",
      name="Diocese of Prespa and Pelagonia",
      local=u"Преспанско-пелагониска епархија",
      country="MK",
      site="http://www.mpc.org.mk/MPC/ppe.asp",
      sources=["http://www.mpc.org.mk/MPC/ppe.asp", MPC]),

 dict(id="mk-debar-kicevo", parent="macedonia",
      name="Diocese of Debar and Kicevo",
      local=u"Дебарско-кичевска епархија",
      country="MK",
      site="https://dke.org.mk/",
      sources=["https://dke.org.mk/", MPC]),

 dict(id="mk-strumica", parent="macedonia",
      name="Diocese of Strumica",
      local=u"Струмичка епархија",
      seat="Strumica", country="MK",
      site="http://www.mpc.org.mk/MPC/se.asp",
      sources=["http://www.mpc.org.mk/MPC/se.asp", MPC]),

 dict(id="mk-povardarie", parent="macedonia",
      name="Diocese of Povardarie",
      local=u"Повардарска епархија",
      country="MK",
      site="http://www.povardarska-eparhija.org.mk/pe/",
      sources=["http://www.povardarska-eparhija.org.mk/pe/", MPC]),

 dict(id="mk-bregalnica", parent="macedonia",
      name="Diocese of Bregalnica",
      local=u"Брегалничка епархија",
      seat="Stip", country="MK",
      address=[u"Тошо Арсов бр. 3", u"Поштенски Фах бр. 97", u"2000 Штип"],
      site="https://bregalnickaeparhija.org.mk/",
      sources=["https://bregalnickaeparhija.org.mk/contact.html", MPC]),

 dict(id="mk-tetovo-gostivar", parent="macedonia",
      name="Diocese of Tetovo and Gostivar",
      local=u"Тетовско-гостиварска епархија",
      seat="Tetovo", country="MK",
      site="http://www.mpc.org.mk/tetovsko-gostivarska-aktuelno.asp",
      sources=["http://www.mpc.org.mk/tetovsko-gostivarska-aktuelno.asp", MPC]),

 dict(id="mk-kumanovo-osogovo", parent="macedonia",
      name="Diocese of Kumanovo and Osogovo",
      local=u"Кумановско-осоговска епархија",
      seat="Kumanovo", country="MK",
      sources=[MPC]),

 dict(id="mk-america-canada", parent="macedonia",
      name="Diocese of America and Canada",
      local=u"Американско-канадска епархија",
      seat="Toronto", country="CA",
      sources=[DENES, MPC, ACMOD]),

 dict(id="mk-europe", parent="macedonia",
      name="Diocese of Europe",
      local=u"Европска епархија",
      seat=u"Malm\u00f6", country="SE",
      sources=[DENES, EUROPE, MPC]),

 dict(id="mk-australia-nz", parent="macedonia",
      name="Diocese of Australia and New Zealand",
      local=u"Австралиско-новозеландска епархија",
      country="AU",
      sources=[DENES, MPC]),

 dict(id="mk-australia-sydney", parent="macedonia",
      name="Diocese of Australia and Sydney",
      local=u"Австралиско-сиднејска епархија",
      seat="Sydney", country="AU",
      sources=[DENES]),
]
