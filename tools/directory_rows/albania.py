# -*- coding: utf-8 -*-
"""The dioceses of the Church of Albania.

Read on 14 September 2026 from the Church's own account of how it is
organised, which it publishes and keeps current at

    https://orthodoxalbania.org/2026/organizimi-kishtar-kisha-orthodhokse-autoqefale-e-shqiperise-2026/

It holds six sees - the Archdiocese of Tirana and Durres and five
metropolises - with the archihieratical vicariates of each beneath them, and
prints an address and a telephone for every one. Six rows are written here,
and the Church had none before.

The same page carries a second, shorter list at its foot, "Kontaktet e
Mitropolive", which gives each see's seat and telephone again. The two agree,
and where the shorter list prints only the city the fuller one prints the
street; the street is what the row carries.

ADDRESSES are the Church's own lines, in the words and the quotation marks it
prints them in, translated nowhere. The country line is dropped, because the
page writes it in the reader's language. Four of the six publish a street.
Elbasan is published with the city alone, which is all the Church prints, and
the Archdiocese with its seat alone: the Church gives the Archdiocese's
telephone and e-mail on that page and its street on the row of the Church
itself, which is the same house, and the row does not repeat it.

SITES. The Church gives each see a page of its own and links it as "Faqja e
Mitropolisë"; all six answered and each row carries its own. The addresses
under /sq/mitropolite/ that the page also carries are not published here: they
redirect to the Church's front page, which means there is nothing there yet."""

READ = "2026-09-14"

AL = ("https://orthodoxalbania.org/2026/"
      "organizimi-kishtar-kisha-orthodhokse-autoqefale-e-shqiperise-2026/")
TAG = "https://orthodoxalbania.org/2026/tag/"

ROWS = [

 dict(id="al-tirana-durres", parent="albania",
      name=u"Archdiocese of Tirana and Durrës",
      local=u"Kryepiskopata e Shenjtë e Tiranës dhe e Durrësit",
      seat="Tirana", country="AL",
      site=TAG + "tirane/",
      sources=[AL, TAG + "tirane/"]),

 dict(id="al-apollonia-fier", parent="albania",
      name="Metropolis of Apollonia and Fier",
      local=u"Mitropolia e Apollonisë dhe e Fierit",
      seat="Fier", country="AL",
      address=[u"Lagjja “1 Maji”, rr. “Jani Bakalli”", u"Fier"],
      site=TAG + "mitropolia-e-apollonise-dhe-e-fierit/",
      sources=[AL, TAG + "mitropolia-e-apollonise-dhe-e-fierit/"]),

 dict(id="al-elbasan", parent="albania",
      name="Metropolis of Elbasan",
      local="Mitropolia e Elbasanit",
      seat="Elbasan", country="AL",
      address=["Elbasan"],
      site=TAG + "mitropolia-e-elbasanit/",
      sources=[AL, TAG + "mitropolia-e-elbasanit/"]),

 dict(id="al-berat", parent="albania",
      name="Metropolis of Berat",
      local="Mitropolia e Beratit",
      seat="Berat", country="AL",
      address=[u"Lagjja “28 Nëntori”", u"Berat"],
      site=TAG + "mitropolia-e-beratit/",
      sources=[AL, TAG + "mitropolia-e-beratit/"]),

 dict(id="al-gjirokaster", parent="albania",
      name=u"Metropolis of Gjirokastër",
      local=u"Mitropolia e Gjirokastrës",
      seat=u"Gjirokastër", country="AL",
      address=[u"Rr. “Alqi Kondi”, nr. 27", u"Gjirokastër"],
      site=TAG + "mitropolia-e-gjirokastres/",
      sources=[AL, TAG + "mitropolia-e-gjirokastres/"]),

 dict(id="al-korce", parent="albania",
      name=u"Metropolis of Korçë",
      local=u"Mitropolia e Korçës",
      seat=u"Korçë", country="AL",
      address=[u"Rr. “Kryepiskopi Anastas” nr. 2", u"Korçë"],
      site=TAG + "mitropolia-e-korces/",
      sources=[AL, TAG + "mitropolia-e-korces/"]),
]
