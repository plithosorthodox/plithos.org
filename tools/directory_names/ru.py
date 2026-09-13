# -*- coding: utf-8 -*-
"""The rows in Russian.

Gathered from what the site already publishes in Russian, where the sees
stand in the titles of the saints themselves: патриарх Константинопольский,
патриарх Московский, архиепископ Александрийский, Антиохийский,
Иерусалимский. The bodies are named as Russian names a local Church, by the
adjective of the land with Православная Церковь after it; the two whose
standing is disputed are named the way Russian itself keeps them apart, the
Ukrainian Church by the adjective and the Church of Ukraine by the genitive.

Settled by counting the Russian corpus:

  - Константинополь 2096, Стамбул 0. The site has never once written the
    Turkish name, and the see is Константинополь.
  - Тбилиси 32, Тифлис 16. The modern name wins on its own numbers.
  - Хельсинки is the exception where the count was not followed. The Russian
    here writes Гельсингфорс, seven times, all of them inside the life of
    the Priestmartyr Alexander Hotovitzky, where the year is 1917 and the
    imperial name is the right one; the Serbian and Ukrainian of that same
    sentence write Хелсинки and Гельсінкі. The seat of a Church living today
    is Хельсинки.

The Church of Finland carries two Russian names and both are in use,
Финляндская in the official registers and Финская in ordinary Russian
writing about her. The row is a label, not a letterhead, so Финская stands
here.

Прешов and Сайоссет are written here for the first time in Russian on this
site; there was nothing to gather. Both are the received Russian forms,
Сайоссет the one the Russian reference works give for the chancery on Long
Island, not a transliteration made up for the occasion.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Russian this site publishes and
are taken whole - Вселенская Патриархия and the Русская, Сербская, Румынская
and Украинская Православная Церковь of the commemorations.

Settled by counting: Вселенская Патриархия 49, Вселенский Патриархат 7, so
the see is a Патриархия here, and Александрийская and Иерусалимская follow
the Антиохийская Патриархия the corpus already writes. The one row that
breaks that pattern is Antioch, because the adjective cannot govern a second
member: и всего Востока, a phrase the lives already carry seventeen times,
needs the genitive in front of it, so that row reads Патриархия Антиохии и
всего Востока.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Russian name for either body
carries it, so it is not written here.

Four rows come out word for word as their labels - Russia, Serbia, Romania
and the Ukrainian Church. Russian has one name for each of those bodies, and
the page shows it once.
"""
NAMES = {
    "constantinople": u"Константинопольская Православная Церковь",
    "alexandria": u"Александрийская Православная Церковь",
    "antioch": u"Антиохийская Православная Церковь",
    "jerusalem": u"Иерусалимская Православная Церковь",
    "russia": u"Русская Православная Церковь",
    "georgia": u"Грузинская Православная Церковь",
    "serbia": u"Сербская Православная Церковь",
    "romania": u"Румынская Православная Церковь",
    "bulgaria": u"Болгарская Православная Церковь",
    "cyprus": u"Кипрская Православная Церковь",
    "greece": u"Элладская Православная Церковь",
    "albania": u"Албанская Православная Церковь",
    "poland": u"Польская Православная Церковь",
    "czech-slovakia": u"Православная Церковь Чешских земель и Словакии",
    "oca": u"Православная Церковь в Америке",
    "macedonia": u"Македонская Православная Церковь - Охридская Архиепископия",
    "ukraine-uoc": u"Украинская Православная Церковь",
    "ukraine-ocu": u"Православная Церковь Украины",
    "sinai": u"Синайская Православная Церковь",
    "finland": u"Финская Автономная Православная Церковь",
    "japan": u"Японская Православная Церковь",
    "estonia-eaok": u"Православная Церковь Эстонии",
    "albanian-americas": u"Албанская Православная епархия Америки",
    "acrod": u"Американская Карпаторусская Православная епархия Северной Америки",
    "ep-thyateira": u"Архиепископия Фиатиры и Великой Британии",
    "goarch": u"Греческая Православная архиепископия Америки",
    "ep-france": u"Греческая Православная митрополия Франции",
    "ep-germany": u"Греческая Православная митрополия Германии",
    "ep-austria": u"Священная митрополия Австрии",
    "ep-korea": u"Священная митрополия Кореи",
    "ep-spain": u"Священная митрополия Испании и Португалии",
    "ep-belgium": u"Митрополия Бельгии",
    "ep-sweden": u"Митрополия Швеции и всей Скандинавии",
    "ep-switzerland": u"Митрополия Швейцарии",
    "ep-hongkong": u"Православная митрополия Гонконга и Юго-Восточной Азии",
    "ep-singapore": u"Православная митрополия Сингапура и Южной Азии",
    "ep-italy": u"Священная Православная архиепископия Италии и Мальты",
    "uocc": u"Украинская Православная Церковь Канады",
    "uoc-usa": u"Украинская Православная Церковь США",
    "antiochian-na": u"Антиохийская Православная Христианская архиепископия Северной Америки",
    "rocor": u"Русская Православная Церковь Заграницей",
    "mp-parishes-usa": u"Патриаршие приходы в США",
    "serbian-eastern": u"Епархия Восточной Америки",
    "serbian-midwestern": u"Епархия Новой Грачаницы и Среднего Запада Америки",
    "serbian-western": u"Епархия Западной Америки",
    "romanian-americas": u"Румынская Православная митрополия обеих Америк",
    "bulgarian-usa": u"Болгарская Восточно-Православная епархия США, Канады и Австралии",
    "oca-albanian": u"Албанская архиепископия",
    "oca-canada": u"Архиепископия Канады",
    "oca-washington": u"Архиепископия Вашингтона",
    "oca-western-pa": u"Архиепископия Западной Пенсильвании",
    "oca-bulgarian": u"Болгарская епархия",
    "oca-eastern-pa": u"Епархия Восточной Пенсильвании",
    "oca-mexico": u"Епархия Мексики",
    "oca-new-england": u"Епархия Новой Англии",
    "oca-ny-nj": u"Епархия Нью-Йорка и Нью-Джерси",
    "oca-alaska": u"Епархия Ситки и Аляски",
    "oca-midwest": u"Епархия Среднего Запада",
    "oca-south": u"Епархия Юга",
    "oca-west": u"Епархия Запада",
    "oca-romanian": u"Румынская епископия",
}
SEATS = {
    "Istanbul": u"Константинополь",
    "Alexandria": u"Александрия",
    "Damascus": u"Дамаск",
    "Jerusalem": u"Иерусалим",
    "Moscow": u"Москва",
    "Tbilisi": u"Тбилиси",
    "Belgrade": u"Белград",
    "Bucharest": u"Бухарест",
    "Sofia": u"София",
    "Nicosia": u"Никосия",
    "Athens": u"Афины",
    "Tirana": u"Тирана",
    "Warsaw": u"Варшава",
    "Prešov": u"Прешов",
    "Syosset, New York": u"Сайоссет, Нью-Йорк",
    "Skopje": u"Скопье",
    "Kyiv": u"Киев",
    "Mount Sinai": u"Гора Синай",
    "Helsinki": u"Хельсинки",
    "Tokyo": u"Токио",
    "Tallinn": u"Таллин",
    "Alexandria, Virginia": u"Александрия, Вирджиния",
    "Alhambra, California": u"Алхамбра, Калифорния",
    "Anchorage, Alaska": u"Анкоридж, Аляска",
    "Bath, Pennsylvania": u"Бат, Пенсильвания",
    "Bonn": u"Бонн",
    "Boston, Massachusetts": u"Бостон, Массачусетс",
    "Bronxville, New York": u"Бронксвилл, Нью-Йорк",
    "Brussels": u"Брюссель",
    "Chambesy": u"Шамбези",
    "Chicago, Illinois": u"Чикаго, Иллинойс",
    "Cranberry Township, Pennsylvania": u"Крэнберри-Тауншип, Пенсильвания",
    "Dallas, Texas": u"Даллас, Техас",
    "Englewood, New Jersey": u"Энглвуд, Нью-Джерси",
    "Hong Kong": u"Гонконг",
    "Jackson, Michigan": u"Джексон, Мичиган",
    "Johnstown, Pennsylvania": u"Джонстаун, Пенсильвания",
    "London": u"Лондон",
    "Madrid": u"Мадрид",
    "Mexico City": u"Мехико",
    "New Rochelle, New York": u"Нью-Рошелл, Нью-Йорк",
    "New York": u"Нью-Йорк",
    "Paris": u"Париж",
    "Rawdon, Quebec": u"Родон, Квебек",
    "San Francisco, California": u"Сан-Франциско, Калифорния",
    "Seoul": u"Сеул",
    "Singapore": u"Сингапур",
    "Somerset, New Jersey": u"Сомерсет, Нью-Джерси",
    "Stockholm": u"Стокгольм",
    "Third Lake, Illinois": u"Тёрд-Лейк, Иллинойс",
    "Toledo, Ohio": u"Толидо, Огайо",
    "Venice": u"Венеция",
    "Vienna": u"Вена",
    "Windsor, Connecticut": u"Виндзор, Коннектикут",
    "Winnipeg, Manitoba": u"Виннипег, Манитоба",
}
STYLED = {
    "constantinople": u"Вселенская Патриархия",
    "alexandria": u"Александрийская Патриархия",
    "antioch": u"Патриархия Антиохии и всего Востока",
    "jerusalem": u"Иерусалимская Патриархия",
    "russia": u"Русская Православная Церковь",
    "serbia": u"Сербская Православная Церковь",
    "romania": u"Румынская Православная Церковь",
    "bulgaria": u"Болгарская Православная Церковь - Болгарская Патриархия",
    "ukraine-uoc": u"Украинская Православная Церковь",
}
