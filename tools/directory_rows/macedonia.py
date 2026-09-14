# -*- coding: utf-8 -*-
"""The dioceses of the Macedonian Orthodox Church - Ohrid Archbishopric.

Read on 14 September 2026 from the Archbishopric's own list of its dioceses at

    http://www.mpc.org.mk/MPC/eparhii.asp

which answers here over plain http and not over https. The list holds eleven
dioceses: eight in North Macedonia and three abroad - the American-Canadian,
the European and the Australian-New Zealand. Eight rows are written here.

THE THREE ABROAD ARE DEFERRED, NOT EXCLUDED. The Archbishopric names them and
gives an address for two of them, and neither address answers: akmpe.org, the
address it prints for the American-Canadian diocese, now redirects to an
advertising site and must not be followed, and mpceanz.org.au does not resolve
at all. The Archbishopric publishes no postal address for any of the three and
no page of its own that says where they sit, so this site cannot say what
country to file them under, and a row has to name one. They are held for a
source that answers, in the same way the Georgian archdiocese in North America
is held. This note is here so the next pass looks rather than concluding that
the list is eight.

Two older lists on the same site were not used and are the reason to read the
navigation rather than the page body. The site's own sidebar, and the English
page of dioceses at English/dioceses.asp, both print an earlier division into
seven - with Polog and Kumanovo undivided and Debar without Kicevo - which the
Archbishopric's current list has replaced. The English names here follow that
English page where it and the current list agree.

SITES. Three dioceses answered at the address the Archbishopric prints for
them: Debar and Kicevo, Povardarie, and Bregalnica. Tetovo and Gostivar has no
site of its own and the Archbishopric gives it a page on the Archbishopric's
own site, which is what the row links. Skopje's published address, spe.org.mk,
did not answer here and the row carries no link; it is to be tried again.

ADDRESSES. The Archbishopric publishes none, and only Bregalnica prints one on
its own site. Seven rows carry a name, a country and a citation, which is a
whole row. SEATS are given only where a see is named for the city it sits in
or where an address was read; Prespa and Pelagonia, Debar and Kicevo, and
Povardarie are named for regions and their seats are not published on any page
read here."""

READ = "2026-09-14"

MPC = "http://www.mpc.org.mk/MPC/eparhii.asp"

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
]
