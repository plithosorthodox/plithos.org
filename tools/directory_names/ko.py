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

The thirty-nine dioceses came afterwards, and the words for what they are
were counted first. 교구 is a diocese, 160 times; 관구 is a metropolis, 59
times and written of 스미르나의 관구 and of the metropolitan see of Rus, so it
carries the metropolises and the metropolitanates alike; 대교구 carries the
archdioceses, as it already carries Ohrid; 주교구 takes the Romanian
Episcopate and 본당, 113 times, the patriarchal parishes.

서울 and 한국 are both in the corpus, 4 and 52 times, so this lane's own
country and city needed no new form after all. 영국 is the site's word for
Britain in a modern sentence - it is where Saint Sophrony settled - and
carries Great Britain; 에스파냐 stands 52 against 스페인 25 and takes Spain.
The American seats were largely written here already: 알래스카, 시트카, 뉴욕,
보스턴, 시카고, 샌프란시스코, 캘리포니아, 일리노이, 펜실베이니아, 잭슨,
캐나다, 멕시코, 미국, 파리 and 베네치아, each written big to small as
뉴욕 사이오셋 already is. 중서부, 남부 and 서부 name the three American
regions. ROCOR reads 해외 러시아 정교회, since 해외 is the word the pages
already use for abroad.

Six syllables had never been written on these pages, one in each of six
cities no saint here is of: 뤼 in 브뤼셀, 샹 in 샹베지, 벡 in 퀘벡, 톡 in
스톡홀름, 컷 in 코네티컷 and 펙 in 위니펙. Each is the received Korean form
and is declared rather than passed off as gathered.
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
    "albanian-americas": u"아메리카 알바니아 정교회 교구",
    "acrod": u"미국 카르파티아 루스 정교회 북아메리카 교구",
    "ep-thyateira": u"티아티라와 영국 대교구",
    "goarch": u"아메리카 그리스 정교회 대교구",
    "ep-france": u"프랑스 그리스 정교회 관구",
    "ep-germany": u"독일 그리스 정교회 관구",
    "ep-austria": u"오스트리아의 거룩한 관구",
    "ep-korea": u"한국의 거룩한 관구",
    "ep-spain": u"에스파냐와 포르투갈의 거룩한 관구",
    "ep-belgium": u"벨기에 관구",
    "ep-sweden": u"스웨덴과 전 스칸디나비아 관구",
    "ep-switzerland": u"스위스 관구",
    "ep-hongkong": u"홍콩과 동남아시아 정교회 관구",
    "ep-singapore": u"싱가포르와 남아시아 정교회 관구",
    "ep-italy": u"이탈리아와 몰타의 거룩한 정교회 대교구",
    "uocc": u"캐나다 우크라이나 정교회",
    "uoc-usa": u"미국 우크라이나 정교회",
    "antiochian-na": u"북아메리카 안티오키아 정교 그리스도교 대교구",
    "rocor": u"해외 러시아 정교회",
    "mp-parishes-usa": u"미국 내 총대주교청 본당",
    "serbian-eastern": u"동부 아메리카 교구",
    "serbian-midwestern": u"새 그라차니차와 중서부 아메리카 교구",
    "serbian-western": u"서부 아메리카 교구",
    "romanian-americas": u"아메리카 루마니아 정교회 관구",
    "bulgarian-usa": u"미국과 캐나다와 오스트레일리아 불가리아 동방 정교회 교구",
    "oca-albanian": u"알바니아 대교구",
    "oca-canada": u"캐나다 대교구",
    "oca-washington": u"워싱턴 대교구",
    "oca-western-pa": u"서부 펜실베이니아 대교구",
    "oca-bulgarian": u"불가리아 교구",
    "oca-eastern-pa": u"동부 펜실베이니아 교구",
    "oca-mexico": u"멕시코 교구",
    "oca-new-england": u"뉴잉글랜드 교구",
    "oca-ny-nj": u"뉴욕과 뉴저지 교구",
    "oca-alaska": u"시트카와 알래스카 교구",
    "oca-midwest": u"중서부 교구",
    "oca-south": u"남부 교구",
    "oca-west": u"서부 교구",
    "oca-romanian": u"루마니아 주교구",
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
    "Alexandria, Virginia": u"버지니아 알렉산드리아",
    "Alhambra, California": u"캘리포니아 알함브라",
    "Anchorage, Alaska": u"알래스카 앵커리지",
    "Bath, Pennsylvania": u"펜실베이니아 배스",
    "Bonn": u"본",
    "Boston, Massachusetts": u"매사추세츠 보스턴",
    "Bronxville, New York": u"뉴욕 브롱크스빌",
    "Brussels": u"브뤼셀",
    "Chambesy": u"샹베지",
    "Chicago, Illinois": u"일리노이 시카고",
    "Cranberry Township, Pennsylvania": u"펜실베이니아 크랜베리 타운십",
    "Dallas, Texas": u"텍사스 댈러스",
    "Englewood, New Jersey": u"뉴저지 잉글우드",
    "Hong Kong": u"홍콩",
    "Jackson, Michigan": u"미시간 잭슨",
    "Johnstown, Pennsylvania": u"펜실베이니아 존스타운",
    "London": u"런던",
    "Madrid": u"마드리드",
    "Mexico City": u"멕시코시티",
    "New Rochelle, New York": u"뉴욕 뉴로셸",
    "New York": u"뉴욕",
    "Paris": u"파리",
    "Rawdon, Quebec": u"퀘벡 로던",
    "San Francisco, California": u"캘리포니아 샌프란시스코",
    "Seoul": u"서울",
    "Singapore": u"싱가포르",
    "Somerset, New Jersey": u"뉴저지 서머싯",
    "Stockholm": u"스톡홀름",
    "Third Lake, Illinois": u"일리노이 서드레이크",
    "Toledo, Ohio": u"오하이오 털리도",
    "Venice": u"베네치아",
    "Vienna": u"빈",
    "Windsor, Connecticut": u"코네티컷 윈저",
    "Winnipeg, Manitoba": u"매니토바 위니펙",
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
