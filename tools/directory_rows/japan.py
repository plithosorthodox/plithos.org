# -*- coding: utf-8 -*-
"""The three dioceses of the Church of Japan.

The Church's own guide to its churches is divided into its three dioceses,
one page to each, and those pages are what these rows are read from. It
publishes no address for a diocese as such and no English name for one, so
the rows carry the Japanese the Church prints and the English a reader of
this site would look them up under.

Where each bishop sits is said elsewhere on the same site rather than on
the list: the Church's account of its own history calls the bishop of the
Eastern diocese the Bishop of Sendai, and its report of the Western
diocesan assembly places that diocese's centre in Nakagyo-ku, Kyoto. Both
pages are cited beside the list.

THREE IS THE COUNT AND THE CHURCH SAYS IT BY ACTING ON IT. It publishes no
sentence numbering its dioceses - neither its account of itself, nor its
history, nor its page of the Primate and diocesan bishops gives a figure -
so the count was checked against what the Church reports itself doing. It
holds one diocesan assembly a year for each diocese and reports each of
them: in 2025 the Tokyo archdiocese on 29 June, the Eastern diocese on 22
June and the Western diocese on 15 June, and nothing else called an
assembly. Three guides to its churches, three assemblies, three dioceses,
and this file is complete.

RANK AND A SECOND PAGE, 14 SEPTEMBER 2026. The Church writes the Tokyo see
大主教教区 and the other two 主教教区 - an archdiocese and two dioceses - and
the rows carry the English of its own words. Tokyo cited only the guide to its
churches; the Church's account of its own history names the archdiocese too,
and the row now cites both, as the other two already did.
"""

TOKYO = "https://www.orthodoxjapan.jp/area-tokyo.html"
EAST = "https://www.orthodoxjapan.jp/area-higashi.html"
WEST = "https://www.orthodoxjapan.jp/area-nishi.html"
HISTORY = "https://www.orthodoxjapan.jp/h-n.html"
WEST_SYNOD = "https://www.orthodoxjapan.jp/article/20250615.html"

ROWS = [
 dict(id="jp-tokyo", parent="japan",
      name="Archdiocese of Tokyo",
      local=u"東京大主教教区",
      rank="Archdiocese",
      seat="Tokyo", country="JP",
      sources=[TOKYO, HISTORY]),
 dict(id="jp-east", parent="japan",
      name="Diocese of Eastern Japan",
      local=u"東日本主教教区",
      rank="Diocese",
      seat="Sendai", country="JP",
      sources=[EAST, HISTORY]),
 dict(id="jp-west", parent="japan",
      name="Diocese of Western Japan",
      local=u"西日本主教教区",
      rank="Diocese",
      seat="Kyoto", country="JP",
      sources=[WEST, WEST_SYNOD]),
]
