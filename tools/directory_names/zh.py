# -*- coding: utf-8 -*-
"""The directory's Churches and their seats, in Chinese.

Simplified throughout, as docs/CHINESE.md settles for this language. Every
word here was read off the Chinese this site already publishes rather than
composed: the forms come from data/saint-terms.v5.zh.json, the saint names
and the lives.

"The Church of X" is the English label of the list the rows were read from,
not a proper name, so it is written the way this site's Chinese already
writes that phrase: X教会, from 由君士坦丁堡教会设立, 希腊教会 and 罗斯教会.
Where the English itself says Orthodox Church the row takes 正教会, which is
the site's own form for a named body - 美洲正教会 for the Orthodox Church in
America, and 俄罗斯正教会, 塞尔维亚正教会, 罗马尼亚正教会, 格鲁吉亚正教会
elsewhere. The two Ukrainian rows keep the distinction the English keeps:
乌克兰教会 for the label, 乌克兰正教会 for the body that styles itself so.

Sofia was the one that had to be counted. 索菲亚 stands 82 times and 索非亚
29, but the counts are of two different things: 索菲亚 is the saint and the
Great Church - 圣索菲亚大教堂, 致命女索菲亚 - and every one of the 29 is the
Bulgarian city, including the terms table's own "Sofia": "索非亚". The city
is 索非亚.

The Czech row follows the site's own 捷克与斯洛伐克的信众 rather than the
terms table's 捷克地区, since the two halves are named together there and
that is the phrase a reader has already met.

Six seats this site has never named are written in their received Chinese
forms, each built only of characters already on these pages: 伊斯坦布尔,
地拉那, 斯科普里, 普雷绍夫, 赛奥塞特 and 东京. 大主教区 for the Ohrid
Archbishopric is likewise built from the glossary's 大主教 and the 教区 of
its entry for a bishop.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Chinese this site publishes and
are taken whole - 普世牧首区 and the 俄罗斯, 塞尔维亚, 罗马尼亚 and 乌克兰正教会
of the commemorations.

牧首区 is the site's own word for a patriarchate, written 50 times, and the
three ancient sees take it. 安提阿及全东方牧首区 follows the 莫斯科及全俄罗斯牧首
of the calendar. The Bulgarian row is joined without spaces, as the
Macedonian label already is.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Chinese name for either body
carries it, so it is not written here.
"""
NAMES = {
    "constantinople": u"君士坦丁堡教会",
    "alexandria": u"亚历山大教会",
    "antioch": u"安提阿教会",
    "jerusalem": u"耶路撒冷教会",
    "russia": u"俄罗斯教会",
    "georgia": u"格鲁吉亚教会",
    "serbia": u"塞尔维亚教会",
    "romania": u"罗马尼亚教会",
    "bulgaria": u"保加利亚教会",
    "cyprus": u"塞浦路斯教会",
    "greece": u"希腊教会",
    "albania": u"阿尔巴尼亚教会",
    "poland": u"波兰教会",
    "czech-slovakia": u"捷克与斯洛伐克教会",
    "oca": u"美洲正教会",
    "macedonia": u"马其顿正教会-奥赫里德大主教区",
    "ukraine-uoc": u"乌克兰教会",
    "ukraine-ocu": u"乌克兰正教会",
    "sinai": u"西奈教会",
    "finland": u"芬兰自治教会",
    "japan": u"日本教会",
    "estonia-eaok": u"爱沙尼亚正教会",
}
SEATS = {
    "Istanbul": u"伊斯坦布尔",
    "Alexandria": u"亚历山大城",
    "Damascus": u"大马士革",
    "Jerusalem": u"耶路撒冷",
    "Moscow": u"莫斯科",
    "Tbilisi": u"第比利斯",
    "Belgrade": u"贝尔格莱德",
    "Bucharest": u"布加勒斯特",
    "Sofia": u"索非亚",
    "Nicosia": u"尼科西亚",
    "Athens": u"雅典",
    "Tirana": u"地拉那",
    "Warsaw": u"华沙",
    "Prešov": u"普雷绍夫",
    "Syosset, New York": u"纽约赛奥塞特",
    "Skopje": u"斯科普里",
    "Kyiv": u"基辅",
    "Mount Sinai": u"西奈山",
    "Helsinki": u"赫尔辛基",
    "Tokyo": u"东京",
    "Tallinn": u"塔林",
}
STYLED = {
    "constantinople": u"普世牧首区",
    "alexandria": u"亚历山大牧首区",
    "antioch": u"安提阿及全东方牧首区",
    "jerusalem": u"耶路撒冷牧首区",
    "russia": u"俄罗斯正教会",
    "serbia": u"塞尔维亚正教会",
    "romania": u"罗马尼亚正教会",
    "bulgaria": u"保加利亚正教会-保加利亚牧首区",
    "ukraine-uoc": u"乌克兰正教会",
}
