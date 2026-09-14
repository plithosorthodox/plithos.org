# -*- coding: utf-8 -*-
"""The communities of the Chinese Autonomous Orthodox Church.

The Church of China has had no bishop since 1962 and its eparchies of Beijing
and Shanghai stand vacant. What it has are congregations, and those are what a
reader can be sent to. So these rows are communities rather than dioceses: a
church, the city it stands in, and where it is written about.

THERE IS NO NUMBER TO TAKE, AND THAT IS THE FINDING. The Church of China
publishes nothing of its own: it has had no bishop since 1962, orthodox.cn is
a fellowship's site and not a Church's, and the Church above it - the Moscow
Patriarchate, whose Statute names it, with the Japanese Orthodox Church, as
one of the two Autonomous Churches - sets out no list of its communities and
no count of them in that Statute or on its own register page for the Church at
patriarchia.ru/org/265, which answers here with no text at all. So this file
is not a list checked against a list. It is as many communities as the Moscow
Patriarchate has been found naming, which on 14 September 2026 is still two,
and the ones known to be missing are named below so that the page is not
mistaken for the whole.

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

READ AGAIN ON 14 SEPTEMBER 2026, IN CHINESE. The two rows were citing that
site's English edition, which writes both the name and the street in pinyin.
An address on this page is reproduced in the language the destination reads
and a transliteration is not that, so each row now cites the Chinese edition
of the same article, carries the church's name as it is written in Chinese,
and gives the Harbin street in the characters a postman there would read.

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

# Orthodoxy in China. A general source. The address comes from it, and so does
# each church's name in Chinese: the Moscow Patriarchate, which is what
# establishes that these two communities exist, writes about them in Russian
# and in English and never in the language they stand in. A name is of the
# same kind as a street here - it is how a reader finds the door, not a claim
# about whose the community is - so it is taken from this page and cited to
# it, and nothing about either row's standing rests on it.
#
# The Church itself has no name here in its own language for the same reason
# it has almost nothing else: it publishes nothing of its own. What stands in
# Chinese on this page is a fellowship's wording, not the Church's, so the
# Church's row carries none rather than one borrowed from a stranger.
HARBIN_CN = "https://www.orthodox.cn/contemporary/harbin/pokrov_cn.htm"
LABDARIN_CN = "https://www.orthodox.cn/contemporary/neimenggu/eerguna_cn.htm"

ROWS = [
 dict(id="cn-harbin", parent="china",
      name="Church of the Intercession in Harbin",
      local=u"\u54c8\u5c14\u6ee8\u5723\u6bcd\u5e21\u5e6a\uff08\u5b88\u62a4\uff09\u5802",
      seat="Harbin", country="CN",
      address=[u"\u5357\u5c97\u533a\u4e1c\u5927\u76f4\u8857266\u53f7"],
      site_of="russia",
      sources=[HARBIN_MP, PILGRIMS, HARBIN_CN]),

 dict(id="cn-labdarin", parent="china",
      name="Church of St Innocent of Irkutsk in Labdarin",
      local=u"\u989d\u5c14\u53e4\u7eb3\u5723\u82f1\u8bfa\u80af\u63d0\u4e59\u5802",
      seat="Labdarin", country="CN",
      site_of="russia",
      sources=[LABDARIN_MP, LABDARIN_CN]),
]
