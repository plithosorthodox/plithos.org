# -*- coding: utf-8 -*-
"""The directory's Churches and their seats, in Korean.

Hangul alone, with no hanja, as docs/KOREAN.md settles for this language.
Every form is read off data/saint-terms.v5.ko.json, the saint names and the
lives, which are drawn from the books of the Orthodox Metropolis of Korea.

"The Church of X" is the English label of the list the rows were read from,
not a proper name, so it takes the shape this site's Korean already gives
that phrase: X 교회, with the space, from 콘스탄티노폴리스 교회, 그리스 교회
and 루스 교회. Where the English itself says Orthodox Church the row takes
정교회, which is the site's own form for a named body - 아메리카 정교회 and
우크라이나 정교회 both stand in the files - so the two Ukrainian rows keep
the distinction the English keeps.

콘스탄티노폴리스 and 키예프 are the site's forms and are kept; 자치 for
autonomous is the glossary's word, and the Ohrid Archbishopric takes 대교구,
which is the ordinary Korean for an archdiocese and is the 교구 of the
glossary's entry for a bishop under the 대- of its 대주교.

Seven seats this site has never named are written in their received Korean
forms: 이스탄불, 티라나, 스코페, 프레쇼프, 사이오셋, 탈린 and 도쿄.
One syllable in that list, the 쿄 of 도쿄, appears nowhere in the Korean this
site publishes; it is written here because 도쿄 is what a Korean reader is
given for the city, and the Sino-Korean 동경 that the corpus could have
supplied is not the name anyone uses now.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Korean this site publishes and are
taken whole - 세계 총대주교청 and the 러시아, 세르비아, 루마니아 and
우크라이나 정교회 of the commemorations.

총대주교좌 is written far more often here than 총대주교청, 122 to 36, and the
count is not the question: the two are not the same word. 총대주교좌 is the
throne a man ascends to; 총대주교청 is the body that glorifies a saint and
receives relics, which is what this table names. So the patriarchates take
총대주교청. 안티오키아와 전 동방 총대주교청 follows the 모스크바와 전 러시아의
총대주교 of the calendar.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Korean name for either body
carries it, so it is not written here.
"""
NAMES = {
    "constantinople": u"콘스탄티노폴리스 교회",
    "alexandria": u"알렉산드리아 교회",
    "antioch": u"안티오키아 교회",
    "jerusalem": u"예루살렘 교회",
    "russia": u"러시아 교회",
    "georgia": u"조지아 교회",
    "serbia": u"세르비아 교회",
    "romania": u"루마니아 교회",
    "bulgaria": u"불가리아 교회",
    "cyprus": u"키프로스 교회",
    "greece": u"그리스 교회",
    "albania": u"알바니아 교회",
    "poland": u"폴란드 교회",
    "czech-slovakia": u"체코 땅과 슬로바키아 교회",
    "oca": u"아메리카 정교회",
    "macedonia": u"마케도니아 정교회 - 오흐리드 대교구",
    "ukraine-uoc": u"우크라이나 교회",
    "ukraine-ocu": u"우크라이나 정교회",
    "sinai": u"시나이 교회",
    "finland": u"핀란드 자치 교회",
    "japan": u"일본 교회",
    "estonia-eaok": u"에스토니아 정교회",
}
SEATS = {
    "Istanbul": u"이스탄불",
    "Alexandria": u"알렉산드리아",
    "Damascus": u"다마스쿠스",
    "Jerusalem": u"예루살렘",
    "Moscow": u"모스크바",
    "Tbilisi": u"트빌리시",
    "Belgrade": u"베오그라드",
    "Bucharest": u"부쿠레슈티",
    "Sofia": u"소피아",
    "Nicosia": u"니코시아",
    "Athens": u"아테네",
    "Tirana": u"티라나",
    "Warsaw": u"바르샤바",
    "Prešov": u"프레쇼프",
    "Syosset, New York": u"뉴욕 사이오셋",
    "Skopje": u"스코페",
    "Kyiv": u"키예프",
    "Mount Sinai": u"시나이 산",
    "Helsinki": u"헬싱키",
    "Tokyo": u"도쿄",
    "Tallinn": u"탈린",
}
STYLED = {
    "constantinople": u"세계 총대주교청",
    "alexandria": u"알렉산드리아 총대주교청",
    "antioch": u"안티오키아와 전 동방 총대주교청",
    "jerusalem": u"예루살렘 총대주교청",
    "russia": u"러시아 정교회",
    "serbia": u"세르비아 정교회",
    "romania": u"루마니아 정교회",
    "bulgaria": u"불가리아 정교회 - 불가리아 총대주교청",
    "ukraine-uoc": u"우크라이나 정교회",
}
