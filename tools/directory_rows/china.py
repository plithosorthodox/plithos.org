# -*- coding: utf-8 -*-
"""The communities of the Chinese Autonomous Orthodox Church.

The Church of China has had no bishop since 1962 and its eparchies of Beijing
and Shanghai stand vacant. What it has are congregations, and those are what a
reader can be sent to. So these rows are communities rather than dioceses: a
church, the city it stands in, and where it is written about.

Two of them are here and the reason only two are is worth writing down.

The Moscow Patriarchate is the Church these communities belong to, and it is
what establishes that a community exists and what it is called. It names the
church of the Protecting Veil in Harbin as an acting parish of the Chinese
Autonomous Orthodox Church, and it reports the Divine Liturgy celebrated at
the church of St Innocent of Irkutsk in Labdarin, consecrated in 2009 by the
eldest priest of that Church. Those two are rows.

Orthodoxy in China, at orthodox.cn, publishes a page for every Orthodox church
in the country and the street many of them stand on. It is a fellowship's site
and not a Church's, so under the rule in docs/DIRECTORY.md it may give an
address and may not establish a body. The Harbin address is taken from it and
cited to it; nothing here rests on it alone.

That leaves real churches out, and they are named here so the next pass looks
for them rather than concluding there are only two:

  - St Nicholas of Urumqi, at 90 Xindong Street, rebuilt by the local
    government and finished in 1991, with no priest of its own.
  - St Nicholas of Ghulja (Yining), rebuilt in 2000 and consecrated in 2003,
    with no priest of its own.

Both are published by orthodox.cn and both are counted among the Chinese
Church's legally operating parishes in general accounts of it. No page of the
Moscow Patriarchate naming either was found here, so they are deferred for a
citation, not excluded. The church at Enhe is not deferred: the same source
says the building houses the museum of the Russian minority, which is not a
community.

The Orthodox communities in Beijing, Hong Kong, Shanghai, Guangzhou,
Shenzhen, Dalian and Taipei are not here either, and that is not an oversight.
The Moscow Patriarchate names them together as its own, not as this Church's.
They belong under Russia. The reasoning is set out in _churches.py.
"""

READ = "2026-09-14"

# The Department for External Church Relations of the Moscow Patriarchate.
# What a community is and whose it is comes from here.
HARBIN_MP = "https://mospat.ru/en/news/52733/"
PILGRIMS = "https://mospat.ru/en/news/51616/"
LABDARIN_MP = "https://mospat.ru/en/news/50408/"

# Orthodoxy in China. A general source, and the address comes from it.
HARBIN_CN = "https://www.orthodox.cn/contemporary/harbin/pokrov_en.htm"
LABDARIN_CN = "https://www.orthodox.cn/contemporary/neimenggu/eerguna_en.htm"

ROWS = [
 dict(id="cn-harbin", parent="china",
      name="Church of the Intercession in Harbin",
      seat="Harbin", country="CN",
      address=[u"266 Dōngdàzhí Street", u"Nángǎng District, Harbin"],
      site_of="russia",
      sources=[HARBIN_MP, PILGRIMS, HARBIN_CN]),

 dict(id="cn-labdarin", parent="china",
      name="Church of St Innocent of Irkutsk in Labdarin",
      seat="Labdarin", country="CN",
      site_of="russia",
      sources=[LABDARIN_MP, LABDARIN_CN]),
]
