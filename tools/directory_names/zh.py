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

The thirty-nine dioceses came afterwards, and the words for what they are
were read off the same pages. 教区 is a diocese, 238 times; 都主教区 is a
metropolis, 10 times and always of a metropolitan's own church - 罗斯的都主教区,
立陶宛都主教区 - so it carries the metropolises and the metropolitanates of
Hong Kong and Singapore alike; 大主教区 carries the archdioceses, as it
already carries Ohrid; 主教区 takes the Romanian Episcopate and 堂区, 131
times, the patriarchal parishes, with 驻 doing the work of the English in.

The American places were largely written here already: 阿拉斯加, 锡特卡, 纽约,
波士顿, 芝加哥, 旧金山, 加利福尼亚, 伊利诺伊, 宾夕法尼亚, 杰克逊, 加拿大, 墨西哥,
美国, 巴黎 and 威尼斯 all stand in the place vocabulary or the lives, and a
seat is written big to small and unseparated, 纽约布朗克斯维尔, as 纽约赛奥塞特
already is. 中西部, 南部 and 西部 are the site's own words for the three
American regions. The Alexandria of Virginia is 亚历山德里亚 and not the
亚历山大城 of the ancient see, because it is a different city.

Three characters had never been written on these pages and are declared here:
韩, in 韩国, which is the only Chinese name for the country the Metropolis of
Korea sits in, since 朝鲜 is a different state; 澳, in 澳大利亚; and 亥, in
俄亥俄. Nothing else in the table is new.

Ten eparchies of the Romanian Patriarchate came last, and they take the
words already counted out for this table: 大主教区 for an archdiocese and
都主教区 for a metropolis.

雅西 is the one city of the ten the Chinese here had already named, in the
life and the commemoration of the venerable Parascheva, so nothing had to be
chosen for it.

托米斯 is not 康斯坦察. It is the ancient see the modern city stands on, and
the row carries it while 康斯坦察 stands beside it as the seat.

New in Chinese, there having been nothing to gather: 锡比乌, 克卢日-纳波卡,
康斯坦察, 克拉约瓦, 蒂米什瓦拉, 基希讷乌, 托米斯, 利穆尔, 纽伦堡, and 瓦德
and 费莱亚克, which stand with 克卢日 in the title of one see and are all
three kept. Each is the received Chinese form, and the characters of them
the audit reports are new here whatever else they begin.
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
    "albanian-americas": u"美洲阿尔巴尼亚正教会教区",
    "acrod": u"美国喀尔巴阡罗斯正教会北美教区",
    "ep-thyateira": u"推雅推喇与大不列颠大主教区",
    "goarch": u"美洲希腊正教会大主教区",
    "ep-france": u"法国希腊正教会都主教区",
    "ep-germany": u"德国希腊正教会都主教区",
    "ep-austria": u"奥地利神圣都主教区",
    "ep-korea": u"韩国神圣都主教区",
    "ep-spain": u"西班牙与葡萄牙神圣都主教区",
    "ep-belgium": u"比利时都主教区",
    "ep-sweden": u"瑞典及全斯堪的纳维亚都主教区",
    "ep-switzerland": u"瑞士都主教区",
    "ep-hongkong": u"香港及东南亚正教会都主教区",
    "ep-singapore": u"新加坡及南亚正教会都主教区",
    "ep-italy": u"意大利与马耳他神圣正教会大主教区",
    "uocc": u"加拿大乌克兰正教会",
    "uoc-usa": u"美国乌克兰正教会",
    "antiochian-na": u"北美安提阿正教基督教大主教区",
    "rocor": u"海外俄罗斯正教会",
    "mp-parishes-usa": u"牧首驻美国堂区",
    "serbian-eastern": u"美洲东部教区",
    "serbian-midwestern": u"新格拉查尼察与美洲中西部教区",
    "serbian-western": u"美洲西部教区",
    "romanian-americas": u"美洲罗马尼亚正教会都主教区",
    "bulgarian-usa": u"美国、加拿大与澳大利亚保加利亚东方正教会教区",
    "oca-albanian": u"阿尔巴尼亚大主教区",
    "oca-canada": u"加拿大大主教区",
    "oca-washington": u"华盛顿特区大主教区",
    "oca-western-pa": u"宾夕法尼亚西部大主教区",
    "oca-bulgarian": u"保加利亚教区",
    "oca-eastern-pa": u"宾夕法尼亚东部教区",
    "oca-mexico": u"墨西哥教区",
    "oca-new-england": u"新英格兰教区",
    "oca-ny-nj": u"纽约与新泽西教区",
    "oca-alaska": u"锡特卡与阿拉斯加教区",
    "oca-midwest": u"中西部教区",
    "oca-south": u"南部教区",
    "oca-west": u"西部教区",
    "oca-romanian": u"罗马尼亚主教区",
    "ro-bucharest": u"布加勒斯特大主教区",
    "ro-chisinau": u"基希讷乌大主教区",
    "ro-craiova": u"克拉约瓦大主教区",
    "ro-iasi": u"雅西大主教区",
    "ro-sibiu": u"锡比乌大主教区",
    "ro-timisoara": u"蒂米什瓦拉大主教区",
    "ro-tomis": u"托米斯大主教区",
    "ro-cluj": u"瓦德、费莱亚克与克卢日大主教区",
    "ro-western-europe": u"西欧罗马尼亚正教会大主教区",
    "ro-germany": u"德国与中欧、北欧罗马尼亚正教会都主教区",
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
    "Alexandria, Virginia": u"弗吉尼亚亚历山德里亚",
    "Alhambra, California": u"加利福尼亚阿罕布拉",
    "Anchorage, Alaska": u"阿拉斯加安克雷奇",
    "Bath, Pennsylvania": u"宾夕法尼亚巴斯",
    "Bonn": u"波恩",
    "Boston, Massachusetts": u"马萨诸塞波士顿",
    "Bronxville, New York": u"纽约布朗克斯维尔",
    "Brussels": u"布鲁塞尔",
    "Chambesy": u"尚贝西",
    "Chicago, Illinois": u"伊利诺伊芝加哥",
    "Cranberry Township, Pennsylvania": u"宾夕法尼亚克兰伯里镇",
    "Dallas, Texas": u"得克萨斯达拉斯",
    "Englewood, New Jersey": u"新泽西恩格尔伍德",
    "Hong Kong": u"香港",
    "Jackson, Michigan": u"密歇根杰克逊",
    "Johnstown, Pennsylvania": u"宾夕法尼亚约翰斯敦",
    "London": u"伦敦",
    "Madrid": u"马德里",
    "Mexico City": u"墨西哥城",
    "New Rochelle, New York": u"纽约新罗谢尔",
    "New York": u"纽约",
    "Paris": u"巴黎",
    "Rawdon, Quebec": u"魁北克罗顿",
    "San Francisco, California": u"加利福尼亚旧金山",
    "Seoul": u"首尔",
    "Singapore": u"新加坡",
    "Somerset, New Jersey": u"新泽西萨默塞特",
    "Stockholm": u"斯德哥尔摩",
    "Third Lake, Illinois": u"伊利诺伊第三湖",
    "Toledo, Ohio": u"俄亥俄托莱多",
    "Venice": u"威尼斯",
    "Vienna": u"维也纳",
    "Windsor, Connecticut": u"康涅狄格温莎",
    "Winnipeg, Manitoba": u"马尼托巴温尼伯",
    "Chisinau": u"基希讷乌",
    "Cluj-Napoca": u"克卢日-纳波卡",
    "Constanta": u"康斯坦察",
    "Craiova": u"克拉约瓦",
    "Jassy": u"雅西",
    "Limours": u"利穆尔",
    "Nuremberg": u"纽伦堡",
    "Sibiu": u"锡比乌",
    "Timisoara": u"蒂米什瓦拉",
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
