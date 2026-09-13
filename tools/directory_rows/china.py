# -*- coding: utf-8 -*-
"""The communities of the Chinese Autonomous Orthodox Church.

The Church of China has had no bishop since 1962, and its eparchies of
Beijing and Shanghai stand vacant. What it has are congregations, a few of
them with a priest of their own, and those are what a reader can be sent
to. So these rows are communities rather than dioceses: a church, the city
it stands in, and where it is written about.

Two sites carry them. Orthodoxy in China publishes a page for each church
and, for the four in the north and west, the street it stands on. The
Department for External Church Relations of the Moscow Patriarchate names
the Beijing, Harbin and Shanghai churches together in its account of the
first pilgrimage made to them, which is what places the Shanghai community
in the former cathedral of the Surety of Sinners.

Where a church stands but no address is published, the row says so by
carrying none. Several of these have no priest of their own and the pages
cited say as much; that is the state of the Church in China and not a gap
in the reading.
"""

DIOCESES = "https://www.orthodox.cn/contemporary/diocese_en.htm"
PARISHES = "https://www.orthodox.cn/contemporary/parish_en.htm"
PARISHES_CN = "https://www.orthodox.cn/contemporary/parish_cn.htm"
PILGRIMAGE = "https://mospat.ru/en/news/51616/"

ROWS = [
 dict(id="cn-beijing", parent="china",
      name="Church of the Dormition of the Mother of God in Beijing",
      seat="Beijing", country="CN",
      sources=[PILGRIMAGE, "https://mospat.ru/en/news/92369/",
               "https://www.orthodox.cn/contemporary/beijing/index_en.html"]),
 dict(id="cn-harbin", parent="china",
      name="Church of the Protection of the Mother of God in Harbin",
      seat="Harbin", country="CN",
      address=["266 Dongdazhi Street", "Nangang District, Harbin"],
      sources=["https://www.orthodox.cn/contemporary/harbin/pokrov_en.htm",
               "https://www.orthodox.cn/contemporary/harbin/index_en.html",
               PILGRIMAGE]),
 dict(id="cn-shanghai", parent="china",
      name="Cathedral of the Surety of Sinners Icon of the Mother of God in Shanghai",
      seat="Shanghai", country="CN",
      sources=[PILGRIMAGE,
               "https://www.orthodox.cn/contemporary/shanghai/index_en.html"]),
 dict(id="cn-labdarin", parent="china",
      name="St Innocent of Irkutsk Church in E'erguna (Labdarin)",
      seat="Ergun", country="CN",
      sources=["https://www.orthodox.cn/contemporary/neimenggu/eerguna_en.htm",
               "https://www.orthodox.cn/contemporary/neimenggu/index_en.html"]),
 dict(id="cn-enhe", parent="china",
      name="Russian Church of Enhe",
      seat="Enhe", country="CN",
      sources=["https://www.orthodox.cn/contemporary/neimenggu/enhe_en.htm",
               "https://www.orthodox.cn/contemporary/neimenggu/index_en.html"]),
 dict(id="cn-ghulja", parent="china",
      name="St Nicholas Church of Ghulja",
      seat="Yining", country="CN",
      sources=["https://www.orthodox.cn/contemporary/xinjiang/yiningnikolai_en.htm",
               "https://www.orthodox.cn/contemporary/xinjiang/index_en.html"]),
 dict(id="cn-urumqi", parent="china",
      name="St Nicholas Church of Urumqi",
      seat="Urumqi", country="CN",
      address=["90 Xindong Street", "Urumqi"],
      sources=["https://www.orthodox.cn/contemporary/xinjiang/urumqi_en.htm",
               "https://www.orthodox.cn/contemporary/xinjiang/index_en.html"]),
 dict(id="cn-hongkong", parent="china",
      name="Sts Peter and Paul Church in Hong Kong",
      seat="Hong Kong", country="HK",
      address=["12/F, Lee Fung Commercial Building",
               "32-36 Des Voeux Rd W, Sheung Wan"],
      site="https://orthodoxy.hk/",
      sources=["https://orthodoxy.hk/", PARISHES,
               "https://www.orthodox.cn/contemporary/hongkong/index_en.html"]),
 dict(id="cn-guangzhou", parent="china",
      name="Church of the Icon of the Mother of God Joy of All Who Sorrow in Guangzhou",
      local=u"广州“众哀伤者之欢乐”圣母像堂",
      seat="Guangzhou", country="CN",
      address=[u"广州市海珠区艺苑路珠江蒂景赏湖街3号悦涛轩A座3E室"],
      sources=[PARISHES_CN, PARISHES]),
 dict(id="cn-shenzhen", parent="china",
      name="St Sergius of Radonezh Parish in Shenzhen",
      local=u"深圳圣塞尔吉堂",
      seat="Shenzhen", country="CN",
      address=[u"深圳市罗湖区黄贝路华丽东村16栋2单元101号"],
      sources=[PARISHES_CN, PARISHES]),
]
