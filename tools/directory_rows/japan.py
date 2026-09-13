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
      seat="Tokyo", country="JP",
      sources=[TOKYO]),
 dict(id="jp-east", parent="japan",
      name="Diocese of Eastern Japan",
      local=u"東日本主教教区",
      seat="Sendai", country="JP",
      sources=[EAST, HISTORY]),
 dict(id="jp-west", parent="japan",
      name="Diocese of Western Japan",
      local=u"西日本主教教区",
      seat="Kyoto", country="JP",
      sources=[WEST, WEST_SYNOD]),
]
