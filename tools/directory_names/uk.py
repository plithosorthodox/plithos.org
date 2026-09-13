# -*- coding: utf-8 -*-
"""The rows in Ukrainian.

Gathered from what the site already publishes in Ukrainian, where the sees
stand in the titles of the saints: патріарх Константинопольський, патріарх
Московський, архієпископ Александрійський, Антіохійський, Єрусалимський,
єпископ Афінський. The bodies are named as Ukrainian names a local Church,
by the adjective of the land with Православна Церква after it; the Ukrainian
Church and the Church of Ukraine are kept apart the way Ukrainian keeps
them apart, the one by the adjective and the other by the genitive.

Settled by counting the Ukrainian corpus:

  - Константинополь 737, Стамбул 0. The see is Константинополь.
  - Белград 55, Білград 3. The commemoration of the martyrs Hermylus and
    Stratonicus carries the rarer form; the city itself is Белград.
  - Гельсінкі is the site's own, in the life of the Priestmartyr Alexander
    Hotovitzky, and it is also the modern name, so nothing had to be chosen.

Kyiv is Київ here and Киев in the Russian file; neither language is written
with the other's form.

The Church of Finland carries two names in Ukrainian as it does in Russian,
Фінляндська in the official registers and Фінська in ordinary writing about
her. The row is a label, not a letterhead, so Фінська stands here.

Пряшів and Сайоссет are written here for the first time in Ukrainian on
this site; there was nothing to gather. Пряшів is the received Ukrainian
name of the Slovak city, not a rendering of the Slovak one. Словаччини is
likewise unwritten here, and is the standard Ukrainian name of the country;
Словакії would be a Russianism.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Ukrainian this site publishes and
are taken whole - Вселенський Патріархат, written 36 times against 6 for
Вселенська Патріархія, and the Російська, Сербська, Румунська and Українська
Православна Церква of the commemorations.

Александрійський is kept, not Олександрійський, on the same count that
settled the label: 185 to 90. Antioch takes the genitive rather than the
adjective, because и всього Сходу cannot hang on Антіохійський, and the
tail follows the і всієї Русі of the metropolitans of Kyiv.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Ukrainian name for either
body carries it, so it is not written here.

Four rows come out word for word as their labels - Russia, Serbia, Romania
and the Ukrainian Church. Ukrainian has one name for each of those bodies,
and the page shows it once.
"""
NAMES = {
    "constantinople": u"Константинопольська Православна Церква",
    "alexandria": u"Александрійська Православна Церква",
    "antioch": u"Антіохійська Православна Церква",
    "jerusalem": u"Єрусалимська Православна Церква",
    "russia": u"Російська Православна Церква",
    "georgia": u"Грузинська Православна Церква",
    "serbia": u"Сербська Православна Церква",
    "romania": u"Румунська Православна Церква",
    "bulgaria": u"Болгарська Православна Церква",
    "cyprus": u"Кіпрська Православна Церква",
    "greece": u"Елладська Православна Церква",
    "albania": u"Албанська Православна Церква",
    "poland": u"Польська Православна Церква",
    "czech-slovakia": u"Православна Церква Чеських земель і Словаччини",
    "oca": u"Православна Церква в Америці",
    "macedonia": u"Македонська Православна Церква - Охридська Архієпископія",
    "ukraine-uoc": u"Українська Православна Церква",
    "ukraine-ocu": u"Православна Церква України",
    "sinai": u"Синайська Православна Церква",
    "finland": u"Фінська Автономна Православна Церква",
    "japan": u"Японська Православна Церква",
    "estonia-eaok": u"Православна Церква Естонії",
    "albanian-americas": u"Албанська Православна єпархія Америки",
    "acrod": u"Американська Карпаторуська Православна єпархія Північної Америки",
    "ep-thyateira": u"Архієпископія Фіатири і Великої Британії",
    "goarch": u"Грецька Православна архієпископія Америки",
    "ep-france": u"Грецька Православна митрополія Франції",
    "ep-germany": u"Грецька Православна митрополія Німеччини",
    "ep-austria": u"Священна митрополія Австрії",
    "ep-korea": u"Священна митрополія Кореї",
    "ep-spain": u"Священна митрополія Іспанії і Португалії",
    "ep-belgium": u"Митрополія Бельгії",
    "ep-sweden": u"Митрополія Швеції і всієї Скандинавії",
    "ep-switzerland": u"Митрополія Швейцарії",
    "ep-hongkong": u"Православна митрополія Гонконгу і Південно-Східної Азії",
    "ep-singapore": u"Православна митрополія Сінгапуру і Південної Азії",
    "ep-italy": u"Священна Православна архієпископія Італії і Мальти",
    "uocc": u"Українська Православна Церква Канади",
    "uoc-usa": u"Українська Православна Церква США",
    "antiochian-na": u"Антіохійська Православна Християнська архієпископія Північної Америки",
    "rocor": u"Російська Православна Церква Закордоном",
    "mp-parishes-usa": u"Патріарші парафії у США",
    "serbian-eastern": u"Єпархія Східної Америки",
    "serbian-midwestern": u"Єпархія Нової Грачаниці і Середнього Заходу Америки",
    "serbian-western": u"Єпархія Західної Америки",
    "romanian-americas": u"Румунська Православна митрополія обох Америк",
    "bulgarian-usa": u"Болгарська Східно-Православна єпархія США, Канади і Австралії",
    "oca-albanian": u"Албанська архієпископія",
    "oca-canada": u"Архієпископія Канади",
    "oca-washington": u"Архієпископія Вашингтона",
    "oca-western-pa": u"Архієпископія Західної Пенсильванії",
    "oca-bulgarian": u"Болгарська єпархія",
    "oca-eastern-pa": u"Єпархія Східної Пенсильванії",
    "oca-mexico": u"Єпархія Мексики",
    "oca-new-england": u"Єпархія Нової Англії",
    "oca-ny-nj": u"Єпархія Нью-Йорка і Нью-Джерсі",
    "oca-alaska": u"Єпархія Ситки і Аляски",
    "oca-midwest": u"Єпархія Середнього Заходу",
    "oca-south": u"Єпархія Півдня",
    "oca-west": u"Єпархія Заходу",
    "oca-romanian": u"Румунська єпископія",
}
SEATS = {
    "Istanbul": u"Константинополь",
    "Alexandria": u"Александрія",
    "Damascus": u"Дамаск",
    "Jerusalem": u"Єрусалим",
    "Moscow": u"Москва",
    "Tbilisi": u"Тбілісі",
    "Belgrade": u"Белград",
    "Bucharest": u"Бухарест",
    "Sofia": u"Софія",
    "Nicosia": u"Нікосія",
    "Athens": u"Афіни",
    "Tirana": u"Тирана",
    "Warsaw": u"Варшава",
    "Prešov": u"Пряшів",
    "Syosset, New York": u"Сайоссет, Нью-Йорк",
    "Skopje": u"Скоп'є",
    "Kyiv": u"Київ",
    "Mount Sinai": u"Гора Синай",
    "Helsinki": u"Гельсінкі",
    "Tokyo": u"Токіо",
    "Tallinn": u"Таллінн",
    "Alexandria, Virginia": u"Александрія, Вірджинія",
    "Alhambra, California": u"Алхамбра, Каліфорнія",
    "Anchorage, Alaska": u"Анкоридж, Аляска",
    "Bath, Pennsylvania": u"Бат, Пенсильванія",
    "Bonn": u"Бонн",
    "Boston, Massachusetts": u"Бостон, Массачусетс",
    "Bronxville, New York": u"Бронксвілл, Нью-Йорк",
    "Brussels": u"Брюссель",
    "Chambesy": u"Шамбезі",
    "Chicago, Illinois": u"Чикаго, Іллінойс",
    "Cranberry Township, Pennsylvania": u"Кренберрі-Тауншип, Пенсильванія",
    "Dallas, Texas": u"Даллас, Техас",
    "Englewood, New Jersey": u"Енглвуд, Нью-Джерсі",
    "Hong Kong": u"Гонконг",
    "Jackson, Michigan": u"Джексон, Мічиган",
    "Johnstown, Pennsylvania": u"Джонстаун, Пенсильванія",
    "London": u"Лондон",
    "Madrid": u"Мадрид",
    "Mexico City": u"Мехіко",
    "New Rochelle, New York": u"Нью-Рошелл, Нью-Йорк",
    "New York": u"Нью-Йорк",
    "Paris": u"Париж",
    "Rawdon, Quebec": u"Родон, Квебек",
    "San Francisco, California": u"Сан-Франциско, Каліфорнія",
    "Seoul": u"Сеул",
    "Singapore": u"Сінгапур",
    "Somerset, New Jersey": u"Сомерсет, Нью-Джерсі",
    "Stockholm": u"Стокгольм",
    "Third Lake, Illinois": u"Терд-Лейк, Іллінойс",
    "Toledo, Ohio": u"Толідо, Огайо",
    "Venice": u"Венеція",
    "Vienna": u"Відень",
    "Windsor, Connecticut": u"Віндзор, Коннектикут",
    "Winnipeg, Manitoba": u"Вінніпег, Манітоба",
}
STYLED = {
    "constantinople": u"Вселенський Патріархат",
    "alexandria": u"Александрійський Патріархат",
    "antioch": u"Патріархат Антіохії і всього Сходу",
    "jerusalem": u"Єрусалимський Патріархат",
    "russia": u"Російська Православна Церква",
    "serbia": u"Сербська Православна Церква",
    "romania": u"Румунська Православна Церква",
    "bulgaria": u"Болгарська Православна Церква - Болгарський Патріархат",
    "ukraine-uoc": u"Українська Православна Церква",
}
