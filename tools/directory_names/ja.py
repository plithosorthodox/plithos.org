# -*- coding: utf-8 -*-
"""The directory's Churches and their seats, in Japanese.

The Japanese Orthodox Church has had its own vocabulary since Saint Nicholas
of Japan, and this site's Japanese already uses it. Nothing here is written
out of a modern gazetteer; every form is read off
data/saint-terms.v5.ja.json, the saint names and the lives.

The city is コンスタンディヌポリ, which stands 1,425 times against no other
form. With it come the -ヤ endings the Church's Japanese books keep and the
ordinary katakana does not: アレクサンドリヤ, アンティオキヤ, ギリシヤ,
ロシヤ, グルジヤ, セルビヤ, アルバニヤ, マケドニヤ, スロヴァキヤ,
エストニヤ, キプル, ソフィヤ, ニコシヤ. キエフ is the site's form and is
kept.

"The Church of X" is the English label of the list the rows were read from,
not a proper name, so it takes the shape this site's Japanese already gives
that phrase: X教会, from コンスタンディヌポリ教会, ギリシヤ教会 and
ロシヤ教会. Where the English itself says Orthodox Church the row takes
正教会, which is the site's own form for a named body - アメリカ正教会 and
ウクライナ正教会 both stand in the files. So the two Ukrainian rows keep the
distinction the English keeps, and the Church of Japan is 日本教会 by the
same rule that gives コンスタンディヌポリ教会, the body's own
日本ハリストス正教会 being its local name and not translated here.

The Czech row follows the site's own チェコとスロヴァキヤの信者, which names
the two together, rather than the terms table's チェコの地 standing alone.

自治 for autonomous is the glossary's word. Seven seats this site has never
named are written in their received Japanese forms: ティラナ, スコピエ,
イスタンブール, プレショフ, サイオセット, タリン and 東京; 大主教区 for
the Ohrid Archbishopric is built from the glossary's 大主教.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Japanese this site publishes and
are taken whole - 全地総主教庁 and the ロシヤ, セルビヤ, ルーマニア and
ウクライナ正教会 of the commemorations.

総主教座 is written more often here than 総主教庁, 46 to 36, and the count is
not the question: the two are not the same word. 総主教座 is the throne a man
ascends to and the cathedral that holds it; 総主教庁 is the body that
glorifies a saint and receives relics, which is what this table names. So the
patriarchates take 総主教庁. アンティオキヤ及び全東方総主教庁 follows the
モスクワ及び全ロシヤの総主教 of the calendar.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Japanese name for either
body carries it, so it is not written here.

The thirty-nine dioceses came afterwards, and the -ヤ register governs them
too: the place vocabulary writes ペンシルヴェニヤ and カリフォルニヤ for
American states and アジヤ 320 times against アジア 48, so ヴァージニヤ,
オーストリヤ and オーストラリヤ follow, and the Alexandria of Virginia is
アレクサンドリヤ, the one form this site has. フランキヤ stands 10 against
フランス 3, ゲルマニヤ and イスパニヤ are the vocabulary's own, and
スカンディナヴィヤ is read off the life of Saint Anna of Novgorod.

教区 is a diocese, 383 times; 府主教区 is a metropolis, written of the
metropolitan see of Rus, and carries the metropolises and the
metropolitanates alike; 大主教区 carries the archdioceses, as it already
carries Ohrid; 主教区 takes the Romanian Episcopate and 小教区, the glossary's
word for a parish, the patriarchal parishes. The American seats were largely
written here already - アラスカ, シトカ, ニューヨーク, ボストン, シカゴ,
サンフランシスコ, ジャクソン, カナダ, メキシコ, アメリカ合衆国 - and 中西部,
南部 and 西部 name the three American regions.

The English Antiochian Orthodox Christian Archdiocese loses its Christian
here, and the Japanese says only 正教: 正教キリスト教 is not a phrase in the
language, and 正教 already carries what the English doubles.

One character had never been written on these pages: 韓, in 韓国, which is the
Japanese name for the country the Metropolis of Korea sits in. Nothing else
in the table is new.
"""
NAMES = {
    "constantinople": u"コンスタンディヌポリ教会",
    "alexandria": u"アレクサンドリヤ教会",
    "antioch": u"アンティオキヤ教会",
    "jerusalem": u"エルサレム教会",
    "russia": u"ロシヤ教会",
    "georgia": u"グルジヤ教会",
    "serbia": u"セルビヤ教会",
    "romania": u"ルーマニア教会",
    "bulgaria": u"ブルガリア教会",
    "cyprus": u"キプル教会",
    "greece": u"ギリシヤ教会",
    "albania": u"アルバニヤ教会",
    "poland": u"ポーランド教会",
    "czech-slovakia": u"チェコとスロヴァキヤの教会",
    "oca": u"アメリカ正教会",
    "macedonia": u"マケドニヤ正教会 - オフリド大主教区",
    "ukraine-uoc": u"ウクライナ教会",
    "ukraine-ocu": u"ウクライナ正教会",
    "sinai": u"シナイ教会",
    "finland": u"フィンランド自治教会",
    "japan": u"日本教会",
    "estonia-eaok": u"エストニヤ正教会",
}
SEATS = {
    "Istanbul": u"イスタンブール",
    "Alexandria": u"アレクサンドリヤ",
    "Damascus": u"ダマスク",
    "Jerusalem": u"エルサレム",
    "Moscow": u"モスクワ",
    "Tbilisi": u"トビリシ",
    "Belgrade": u"ベオグラード",
    "Bucharest": u"ブカレスト",
    "Sofia": u"ソフィヤ",
    "Nicosia": u"ニコシヤ",
    "Athens": u"アテネ",
    "Tirana": u"ティラナ",
    "Warsaw": u"ワルシャワ",
    "Prešov": u"プレショフ",
    "Syosset, New York": u"サイオセット、ニューヨーク",
    "Skopje": u"スコピエ",
    "Kyiv": u"キエフ",
    "Mount Sinai": u"シナイ山",
    "Helsinki": u"ヘルシンキ",
    "Tokyo": u"東京",
    "Tallinn": u"タリン",
}
STYLED = {
    "constantinople": u"全地総主教庁",
    "alexandria": u"アレクサンドリヤ総主教庁",
    "antioch": u"アンティオキヤ及び全東方総主教庁",
    "jerusalem": u"エルサレム総主教庁",
    "russia": u"ロシヤ正教会",
    "serbia": u"セルビヤ正教会",
    "romania": u"ルーマニア正教会",
    "bulgaria": u"ブルガリア正教会 - ブルガリア総主教庁",
    "ukraine-uoc": u"ウクライナ正教会",
}
