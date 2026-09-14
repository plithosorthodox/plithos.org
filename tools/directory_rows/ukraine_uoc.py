# -*- coding: utf-8 -*-
"""The eparchies of the Ukrainian Orthodox Church.

Read on 14 September 2026 from the Church's own list of its eparchies at
https://church.ua/jeparxiji/, which is where it publishes the address of
every eparchial administration. The list holds 53 eparchies. All 53 are
here.

Ten sees that the Moscow Patriarchate's register now carries among its own
were left out of tools/directory_rows/russia.py, because a country code is a
claim about a border and this site does not make one. Nine of them -
Berdiansk, Donetsk, Dzhankoi, Feodosia, Horlivka, Luhansk, Rovenky,
Sievierodonetsk and Simferopol - stand on the Ukrainian Orthodox Church's own
list, and they stand here, under that Church, with the country code UA,
because that is where their own Church puts them. This is not a finding about
a border; it is the rule the whole directory runs on, that a body appears
because a Church lists it among its own.

Skadovsk is the exception and has no row anywhere. It is on the Moscow
register and it is not on this list, and the territory it names is the
Ukrainian Orthodox Church's Nova Kakhovka eparchy. A see this site can find
in only one of two registers, where the two disagree about which Church holds
it, is a see this site has nothing to say about yet.

Names and seats are given in English; the see's own name in Ukrainian stands
beside it as the list writes it, in ordinary case rather than the capitals
the list sets its headings in.

Addresses are the list's own words, set out as an envelope wants them: the
street on one line, the postcode and town on the next. Nothing is translated
and nothing is added. The country line is dropped, because the page writes it
in the reader's language. Where a see's chancery does not stand in the town
the see is named for - Kirovohrad at Kropyvnytskyi, Voznesensk at Pervomaisk,
Feodosia at Kerch, Dnipropetrovsk at Dnipro, Volyn at Lutsk - the see keeps
its own name and the seat names the town. Where the chancery stands in a
village of the see's own city or district - Krykhivtsi for Ivano-Frankivsk,
Horodyshche for Shepetivka - the seat names the city and the address says the
rest.

The list gives Khmelnytskyi two addresses, a registered one and the one the
eparchy works from. The row carries the one a letter would reach.

A site is written only where it answered when it was tried, and thirty-three
did. Ten of the sees publish none - Berdiansk, Chernivtsi-Bukovyna, Donetsk,
Dzhankoi, Feodosia, Luhansk, Nova Kakhovka, Rovenky, Sievierodonetsk and
Simferopol - and ten publish one that did not answer here: five did not
resolve or timed out (Kyiv, Balta, Horlivka, Nizhyn, Volodymyr-Volynskyi),
two refused the request (Uman, Kryvyi Rih), one has expired and one has been
parked (Kamianske, Kamianets-Podilskyi), and one - Boryspil - now answers as
something else altogether and is not linked from here on that account. Those
twenty rows carry no link and fall back to the Church's own list, which does
answer. The ten that did not answer are to be tried again, not written off.
"""

# The day these sources were read. A row carries it as its confirmed date.
READ = "2026-09-14"


LIST = "https://church.ua/jeparxiji/"

ROWS = [

 dict(id="uoc-kyiv", parent="ukraine-uoc",
      name="Kyiv Eparchy",
      local=u"Київська єпархія",
      seat="Kyiv", country="UA",
      address=[u"вул. Лаврська, 15, корп. 49", u"01015, м. Київ"],
      sources=[LIST]),

 dict(id="uoc-balta", parent="ukraine-uoc",
      name="Balta Eparchy",
      local=u"Балтська єпархія",
      seat="Balta", country="UA",
      address=[u"вул. Уварова, 106", u"66100, м. Балта Одеської обл."],
      sources=[LIST]),

 dict(id="uoc-berdiansk", parent="ukraine-uoc",
      name="Berdiansk Eparchy",
      local=u"Бердянська єпархія",
      seat="Berdiansk", country="UA",
      address=[u"вул. Університетська, 23",
               u"71118, м. Бердянськ Запорізької обл."],
      sources=[LIST]),

 dict(id="uoc-bila-tserkva", parent="ukraine-uoc",
      name="Bila Tserkva Eparchy",
      local=u"Білоцерківська єпархія",
      seat="Bila Tserkva", country="UA",
      address=[u"вул. Млинова, 12", u"09117, м. Біла Церква Київської обл."],
      site="https://bilatserkva.church.ua/",
      sources=[LIST]),

 dict(id="uoc-boryspil", parent="ukraine-uoc",
      name="Boryspil Eparchy",
      local=u"Бориспільська єпархія",
      seat="Kyiv", country="UA",
      address=[u"вул. Лаврська, 15", u"001015, м. Київ"],
      sources=[LIST]),

 dict(id="uoc-vinnytsia", parent="ukraine-uoc",
      name="Vinnytsia Eparchy",
      local=u"Вінницька єпархія",
      seat="Vinnytsia", country="UA",
      address=[u"вул. Ярослава Мудрого 5 (мкр Пирогово)", u"21008, м. Вінниця"],
      site="https://eparhia.vn.ua/",
      sources=[LIST]),

 dict(id="uoc-voznesensk", parent="ukraine-uoc",
      name="Voznesensk Eparchy",
      local=u"Вознесенська єпархія",
      seat="Pervomaisk", country="UA",
      address=[u"вул. Корабельна, 46Б",
               u"55220, м. Первомайськ Миколаївської обл."],
      site="https://voznesensk.church.ua/",
      sources=[LIST]),

 dict(id="uoc-volyn", parent="ukraine-uoc",
      name="Volyn Eparchy",
      local=u"Волинська єпархія",
      seat="Lutsk", country="UA",
      address=[u"вул. Караїмська, 11", u"43016, м. Луцьк"],
      site="https://pravoslavna.volyn.ua/",
      sources=[LIST]),

 dict(id="uoc-volodymyr-volynskyi", parent="ukraine-uoc",
      name="Volodymyr-Volynskyi Eparchy",
      local=u"Володимир-Волинська єпархія",
      seat="Volodymyr", country="UA",
      address=[u"вул. Соборна, 27", u"44700, м. Володимир, Волинської обл."],
      sources=[LIST]),

 dict(id="uoc-horlivka", parent="ukraine-uoc",
      name="Horlivka Eparchy",
      local=u"Горлівська єпархія",
      seat="Horlivka", country="UA",
      address=[u"вул. Кірова, 41", u"84627, м. Горлівка Донецької обл."],
      sources=[LIST]),

 dict(id="uoc-dzhankoi", parent="ukraine-uoc",
      name="Dzhankoi Eparchy",
      local=u"Джанкойська єпархія",
      seat="Dzhankoi", country="UA",
      address=[u"вул. Р. Люксембург, 33", u"296100, м. Джанкой"],
      sources=[LIST]),

 dict(id="uoc-dnipropetrovsk", parent="ukraine-uoc",
      name="Dnipropetrovsk Eparchy",
      local=u"Дніпропетровська єпархія",
      seat="Dnipro", country="UA",
      address=[u"вул. М. Грушевського, 4а", u"49070, м. Дніпро"],
      site="https://eparhia.dp.ua/",
      sources=[LIST]),

 dict(id="uoc-donetsk", parent="ukraine-uoc",
      name="Donetsk Eparchy",
      local=u"Донецька єпархія",
      seat="Donetsk", country="UA",
      address=[u"вул. Тушинська, 7", u"83062, м. Донецьк"],
      sources=[LIST]),

 dict(id="uoc-zhytomyr", parent="ukraine-uoc",
      name="Zhytomyr Eparchy",
      local=u"Житомирська єпархія",
      seat="Zhytomyr", country="UA",
      address=[u"Подільська, 19", u"10003, м. Житомир"],
      site="https://zhytomyr-eparchy.org/",
      sources=[LIST]),

 dict(id="uoc-zaporizhzhia", parent="ukraine-uoc",
      name="Zaporizhzhia Eparchy",
      local=u"Запорізька єпархія",
      seat="Zaporizhzhia", country="UA",
      address=[u"вул. Кияшка, 26", u"69041, м. Запоріжжя"],
      site="https://hramzp.ua/",
      sources=[LIST]),

 dict(id="uoc-ivano-frankivsk", parent="ukraine-uoc",
      name="Ivano-Frankivsk Eparchy",
      local=u"Івано-Франківська єпархія",
      seat="Ivano-Frankivsk", country="UA",
      address=[u"вул. Виноградна, 10",
               u"76493, с. Крихівці, Тисменицького р-ну Івано-Франківської обл."],
      site="https://ivano-frankivsk.church.ua/",
      sources=[LIST]),

 dict(id="uoc-izium", parent="ukraine-uoc",
      name="Izium Eparchy",
      local=u"Ізюмська єпархія",
      seat="Izium", country="UA",
      address=[u"вул. Івана Мазепи 30Б", u"64303, м. Ізюм Харківської обл."],
      site="https://izum.church.ua/",
      sources=[LIST]),

 dict(id="uoc-kamianske", parent="ukraine-uoc",
      name="Kamianske Eparchy",
      local=u"Кам’янська єпархія",
      seat="Kamianske", country="UA",
      address=[u"вул. Соборна, 6",
               u"51925, м. Кам’янське Дніпропетровської обл."],
      sources=[LIST]),

 dict(id="uoc-kamianets-podilskyi", parent="ukraine-uoc",
      name="Kamianets-Podilskyi Eparchy",
      local=u"Кам’янець-Подільська єпархія",
      seat="Kamianets-Podilskyi", country="UA",
      address=[u"вул. Францисканська, 8", u"32301, м. Кам’янець-Подільський"],
      sources=[LIST]),

 dict(id="uoc-kirovohrad", parent="ukraine-uoc",
      name="Kirovohrad Eparchy",
      local=u"Кіровоградська єпархія",
      seat="Kropyvnytskyi", country="UA",
      address=[u"вул. Велика Перспективна, 74", u"25006, м. Кропивницький"],
      site="http://orthodox-kr.org.ua/",
      sources=[LIST]),

 dict(id="uoc-konotop", parent="ukraine-uoc",
      name="Konotop Eparchy",
      local=u"Конотопська єпархія",
      seat="Konotop", country="UA",
      address=[u"вул. Б. Хмельницького, 7", u"41600, м. Конотоп Сумської обл."],
      site="https://konotop.church.ua/",
      sources=[LIST]),

 dict(id="uoc-kremenchuk", parent="ukraine-uoc",
      name="Kremenchuk Eparchy",
      local=u"Кременчуцька єпархія",
      seat="Kremenchuk", country="UA",
      address=[u"вул. Республіканська, 107",
               u"39621, м. Кременчук Полтавської обл."],
      site="https://kremen-eparh.org/",
      sources=[LIST]),

 dict(id="uoc-kryvyi-rih", parent="ukraine-uoc",
      name="Kryvyi Rih Eparchy",
      local=u"Криворізька єпархія",
      seat="Kryvyi Rih", country="UA",
      address=[u"вул. Церковна, 4",
               u"50000, м. Кривий Ріг Дніпропетровської обл."],
      sources=[LIST]),

 dict(id="uoc-luhansk", parent="ukraine-uoc",
      name="Luhansk Eparchy",
      local=u"Луганська єпархія",
      seat="Luhansk", country="UA",
      address=[u"пров. Крупської, 29б", u"91002, м. Луганськ"],
      sources=[LIST]),

 dict(id="uoc-lviv", parent="ukraine-uoc",
      name="Lviv Eparchy",
      local=u"Львівська єпархія",
      seat="Lviv", country="UA",
      address=[u"вул. Короленка, 3, а/c 1352", u"79008, м. Львів"],
      site="https://upc.lviv.ua/",
      sources=[LIST]),

 dict(id="uoc-mykolaiv", parent="ukraine-uoc",
      name="Mykolaiv Eparchy",
      local=u"Миколаївська єпархія",
      seat="Mykolaiv", country="UA",
      address=[u"вул. Потьомкінська, 50", u"54001, м. Миколаїв"],
      site="http://eparhia.mk.ua/",
      sources=[LIST]),

 dict(id="uoc-mohyliv-podilskyi", parent="ukraine-uoc",
      name="Mohyliv-Podilskyi Eparchy",
      local=u"Могилів-Подільська єпархія",
      seat="Mohyliv-Podilskyi", country="UA",
      address=[u"пл. Соборна, 2/1",
               u"24000, м. Могилів-Подільський Вінницької обл."],
      site="https://moh-pod.church.ua/",
      sources=[LIST]),

 dict(id="uoc-mukachevo", parent="ukraine-uoc",
      name="Mukachevo Eparchy",
      local=u"Мукачівська єпархія",
      seat="Mukachevo", country="UA",
      address=[u"вул. Єпархіальна, 12", u"89600, м. Мукачево Закарпатської обл."],
      site="https://m-church.org.ua/",
      sources=[LIST]),

 dict(id="uoc-nizhyn", parent="ukraine-uoc",
      name="Nizhyn Eparchy",
      local=u"Ніжинська єпархія",
      seat="Nizhyn", country="UA",
      address=[u"вул. Стефана Яворського, 2",
               u"16600, м. Ніжин Чернігівської обл."],
      sources=[LIST]),

 dict(id="uoc-nova-kakhovka", parent="ukraine-uoc",
      name="Nova Kakhovka Eparchy",
      local=u"Новокаховська єпархія",
      seat="Nova Kakhovka", country="UA",
      address=[u"вул. Соборна, 14а",
               u"74909, м. Нова Каховка Херсонської обл."],
      sources=[LIST]),

 dict(id="uoc-ovruch", parent="ukraine-uoc",
      name="Ovruch Eparchy",
      local=u"Овруцька єпархія",
      seat="Ovruch", country="UA",
      address=[u"вул. Соборна, 3", u"11101, м. Овруч Житомирської обл."],
      site="https://ovruch.church.ua/",
      sources=[LIST]),

 dict(id="uoc-odesa", parent="ukraine-uoc",
      name="Odesa Eparchy",
      local=u"Одеська єпархія",
      seat="Odesa", country="UA",
      address=[u"вул. Пантелеймонівська, 58", u"65012, м. Одеса"],
      site="https://eparhiya.od.ua/",
      sources=[LIST]),

 dict(id="uoc-oleksandriia", parent="ukraine-uoc",
      name="Oleksandriia Eparchy",
      local=u"Олександрійська єпархія",
      seat="Oleksandriia", country="UA",
      address=[u"вул. Кременчуцька, 107а",
               u"28001, м. Олександрія Кіровоградської обл."],
      site="https://www.oleksandriya-eparhia.in.ua/",
      sources=[LIST]),

 dict(id="uoc-poltava", parent="ukraine-uoc",
      name="Poltava Eparchy",
      local=u"Полтавська єпархія",
      seat="Poltava", country="UA",
      address=[u"вул. Героїв України, 1б", u"36040, м. Полтава"],
      site="https://pravoslavie.poltava.ua/",
      sources=[LIST]),

 dict(id="uoc-rivne", parent="ukraine-uoc",
      name="Rivne Eparchy",
      local=u"Рівненська єпархія",
      seat="Rivne", country="UA",
      address=[u"Казимира Любомирського, 3", u"33028, м. Рівне"],
      site="https://rivne.church.ua/",
      sources=[LIST]),

 dict(id="uoc-rovenky", parent="ukraine-uoc",
      name="Rovenky Eparchy",
      local=u"Ровеньківська єпархія",
      seat="Rovenky", country="UA",
      address=[u"кв-л Гагаріна, 25", u"94707, м. Ровеньки Луганської обл."],
      sources=[LIST]),

 dict(id="uoc-romny", parent="ukraine-uoc",
      name="Romny Eparchy",
      local=u"Роменська єпархія",
      seat="Romny", country="UA",
      address=[u"пл. Базарна, 15а", u"42000, м. Ромни Сумської обл."],
      site="https://romny.church.ua/",
      sources=[LIST]),

 dict(id="uoc-sarny", parent="ukraine-uoc",
      name="Sarny Eparchy",
      local=u"Сарненська єпархія",
      seat="Sarny", country="UA",
      address=[u"вул. Залізнична, 27", u"34500, м. Сарни Рівненської обл."],
      site="https://sarny.church.ua/",
      sources=[LIST]),

 dict(id="uoc-sievierodonetsk", parent="ukraine-uoc",
      name="Sievierodonetsk Eparchy",
      local=u"Сєвєродонецька єпархія",
      seat="Sievierodonetsk", country="UA",
      address=[u"пл. Соборна, 1", u"93416, м. Сєвєродонецьк Луганської обл."],
      sources=[LIST]),

 dict(id="uoc-simferopol", parent="ukraine-uoc",
      name="Simferopol Eparchy",
      local=u"Сімферопольська єпархія",
      seat="Simferopol", country="UA",
      address=[u"вул. Героїв Аджимушкая, 9/11", u"295011, м. Сімферополь"],
      sources=[LIST]),

 dict(id="uoc-sumy", parent="ukraine-uoc",
      name="Sumy Eparchy",
      local=u"Сумська єпархія",
      seat="Sumy", country="UA",
      address=[u"вул. Соборна, 31", u"40000, м. Суми"],
      site="https://portal-pravoslavie.sumy.ua/",
      sources=[LIST]),

 dict(id="uoc-ternopil", parent="ukraine-uoc",
      name="Ternopil Eparchy",
      local=u"Тернопільська єпархія",
      seat="Ternopil", country="UA",
      address=[u"вул. Коновальця, 1", u"46020, м. Тернопіль"],
      site="https://ternopil.church.ua/",
      sources=[LIST]),

 dict(id="uoc-tulchyn", parent="ukraine-uoc",
      name="Tulchyn Eparchy",
      local=u"Тульчинська єпархія",
      seat="Tulchyn", country="UA",
      address=[u"вул. М. Леонтовича, 41",
               u"23600, м. Тульчин Вінницької обл."],
      site="https://tulchin-eparchia.org.ua/",
      sources=[LIST]),

 dict(id="uoc-uman", parent="ukraine-uoc",
      name="Uman Eparchy",
      local=u"Уманська єпархія",
      seat="Uman", country="UA",
      address=[u"вул. Небесної Сотні, 35/2",
               u"20300, м. Умань Черкаської обл."],
      sources=[LIST]),

 dict(id="uoc-feodosia", parent="ukraine-uoc",
      name="Feodosia Eparchy",
      local=u"Феодосійська єпархія",
      seat="Kerch", country="UA",
      address=[u"вул. Донського, 5", u"298320, м. Керч"],
      sources=[LIST]),

 dict(id="uoc-kharkiv", parent="ukraine-uoc",
      name="Kharkiv Eparchy",
      local=u"Харківська єпархія",
      seat="Kharkiv", country="UA",
      address=[u"вул. Університетська, 8", u"61003, м. Харків"],
      site="http://www.eparchia.kharkov.ua/",
      sources=[LIST]),

 dict(id="uoc-kherson", parent="ukraine-uoc",
      name="Kherson Eparchy",
      local=u"Херсонська єпархія",
      seat="Kherson", country="UA",
      address=[u"вул. Преображенська, 36", u"73025, м. Херсон"],
      site="http://pravoslavie.ks.ua/",
      sources=[LIST]),

 dict(id="uoc-khmelnytskyi", parent="ukraine-uoc",
      name="Khmelnytskyi Eparchy",
      local=u"Хмельницька єпархія",
      seat="Khmelnytskyi", country="UA",
      address=[u"вул. Молодіжна 2/3", u"29016, м. Хмельницький"],
      site="https://www.eparhia.khmelnitskiy.ua/",
      sources=[LIST]),

 dict(id="uoc-khust", parent="ukraine-uoc",
      name="Khust Eparchy",
      local=u"Хустська єпархія",
      seat="Khust", country="UA",
      address=[u"вул. Львівська", u"90400, м. Хуст Закарпатської обл."],
      site="http://www.orthodoxkhust.org.ua/",
      sources=[LIST]),

 dict(id="uoc-cherkasy", parent="ukraine-uoc",
      name="Cherkasy Eparchy",
      local=u"Черкаська єпархія",
      seat="Cherkasy", country="UA",
      address=[u"вул. Надпільна, 230", u"18015, м. Черкаси"],
      site="https://cherkasy.church.ua/",
      sources=[LIST]),

 dict(id="uoc-chernivtsi", parent="ukraine-uoc",
      name="Chernivtsi-Bukovyna Eparchy",
      local=u"Чернівецько-Буковинська єпархія",
      seat="Chernivtsi", country="UA",
      address=[u"вул. Руська, 33", u"58003, м. Чернівці"],
      sources=[LIST]),

 dict(id="uoc-chernihiv", parent="ukraine-uoc",
      name="Chernihiv Eparchy",
      local=u"Чернігівська єпархія",
      seat="Chernihiv", country="UA",
      address=[u"вул. Толстого, 92є", u"14014, м. Чернігів"],
      site="https://orthodox.com.ua/",
      sources=[LIST]),

 dict(id="uoc-shepetivka", parent="ukraine-uoc",
      name="Shepetivka Eparchy",
      local=u"Шепетівська єпархія",
      seat="Shepetivka", country="UA",
      address=[u"вул. Шкільна, 23",
               u"30423, с. Городище Шепетівського р-ну Хмельницької обл."],
      site="https://shep.church.ua/",
      sources=[LIST]),
]
