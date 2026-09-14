# -*- coding: utf-8 -*-
"""The eparchies of the Orthodox Church of Ukraine.

Read on 14 September 2026 from the Church's own map of its eparchies at
https://www.pomisna.info/uk/tserkva/karta-yeparhij/, which is the only list
of its eparchies the Church publishes, and then from each eparchy's own site
where it has one and the site answered. The map holds 31 eparchies. 36 rows
are here, and the difference is set out below.

The map names the eparchies region by region and prints nothing else that can
be used: the address block under every one of them carries the same Kyiv
monastery, which is the template the page was built on and was never filled
in. So the names are the map's and the addresses are each eparchy's own,
taken from its own site, and a row carries an address only where its own site
prints one.

Three decisions were taken and are written here so they are not taken again:

  - Two of the map's names are the Church's older regional ones, and the
    eparchies themselves publish under longer ones. Zhytomyr is one eparchy
    on the map and two that publish - Zhytomyr and Ovruch, Zhytomyr and
    Polissia - and Pereiaslav publishes as Pereiaslav and Vyshneve. Those
    rows are written as the eparchies write themselves, and the map's shorter
    name is not written a second time beside them.
  - Five eparchies publish sites of their own that the map does not name at
    all - Vinnytsia and Bar, Vinnytsia and Tulchyn, Mukachevo and the
    Carpathians, Ternopil and Buchach, Kharkiv and Poltava - and each has a
    row on its own site's authority, which is the rule the whole directory
    runs on: a row names its source when the source belongs to it. That
    several places hold more than one eparchy apiece - Vinnytsia, Ternopil,
    Kharkiv, Zhytomyr, Transcarpathia - is not an error in the reading. The
    Church's own page of its bishops names a ruling bishop for each of them
    separately, and each publishes its own site. No row here says which of
    two eparchies in one city is the elder, or whether either stands over the
    other; the directory records what each published page says of itself.
  - The map carries a thirty-first name, in Chernivtsi region, that no page
    of the Church's own and no eparchy site could be found to confirm, and it
    is the one row not written. A missing eparchy is better than a wrong one.

A seat is written only where the eparchy's own site prints an address that
names the town, so nothing on a row is inferred from the name of a region.
Nineteen rows accordingly carry no address, and sixteen of those carry no
link of their own either: a name, a country and a citation, which is the
directory's declared minimum. A reader who learns that an eparchy exists, and
where to read about it, has been given something, and an eparchy left out
because its address could not be found has been hidden from him.

Two of the sites still carry the name of the Church their eparchy belonged to
before December 2018 - Crimea and Drohobych and Sambir both style themselves
of the Kyiv Patriarchate. The address each prints is the address each prints,
and the row carries it; the row's name is the one the Orthodox Church of
Ukraine gives the eparchy on its own map.

Volyn and Transcarpathia have sites of their own that refused the request
from here rather than failing to answer, and half a dozen more addresses that
were tried did not resolve at all. Those rows carry no link and fall back to
the Church's own map, which does answer. They are to be tried again, not
written off.

Addresses are each site's own words, set out as an envelope wants them: the
street on one line, the postcode and town on the next. Nothing is translated
and nothing is added. The country line is dropped, because the page writes it
in the reader's language.
"""

# The day these sources were read. A row carries it as its confirmed date.
READ = "2026-09-14"


MAP = "https://www.pomisna.info/uk/tserkva/karta-yeparhij/"

ROWS = [

 dict(id="ocu-kyiv", parent="ukraine-ocu",
      name="Kyiv Eparchy",
      local=u"Київська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-crimea", parent="ukraine-ocu",
      name="Crimea Eparchy",
      local=u"Кримська єпархія",
      seat="Simferopol", country="UA",
      address=[u"вул. Севастопольська, 17-А", u"Сімферополь, 95011 АР Крим"],
      site="https://cerkva-krim.at.ua/",
      sources=[MAP, "https://cerkva-krim.at.ua/index/0-3"]),

 dict(id="ocu-vinnytsia", parent="ukraine-ocu",
      name="Vinnytsia Eparchy",
      local=u"Вінницька єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-vinnytsia-bar", parent="ukraine-ocu",
      name="Vinnytsia-Bar Eparchy",
      local=u"Вінницько-Барська єпархія",
      seat="Vinnytsia", country="UA",
      address=[u"вул. Соборна, 23", u"21050, м. Вінниця"],
      site="https://orthodox.vinnica.ua/",
      sources=["https://orthodox.vinnica.ua/kontakty/"]),

 dict(id="ocu-vinnytsia-tulchyn", parent="ukraine-ocu",
      name="Vinnytsia-Tulchyn Eparchy",
      local=u"Вінницько-Тульчинська єпархія",
      country="UA",
      site="https://cerkva.vn.ua/",
      sources=["https://cerkva.vn.ua/"]),

 dict(id="ocu-volyn", parent="ukraine-ocu",
      name="Volyn Eparchy",
      local=u"Волинська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-volodymyr-volynskyi", parent="ukraine-ocu",
      name="Volodymyr-Volynskyi Eparchy",
      local=u"Володимир-Волинська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-dnipropetrovsk", parent="ukraine-ocu",
      name="Dnipropetrovsk Eparchy",
      local=u"Дніпропетровська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-donetsk", parent="ukraine-ocu",
      name="Donetsk Eparchy",
      local=u"Донецька єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-zhytomyr-ovruch", parent="ukraine-ocu",
      name="Zhytomyr-Ovruch Eparchy",
      local=u"Житомирсько-Овруцька єпархія",
      country="UA",
      site="https://saint.in.ua/",
      sources=[MAP, "https://saint.in.ua/contacts"]),

 dict(id="ocu-zhytomyr-polissia", parent="ukraine-ocu",
      name="Zhytomyr-Polissia Eparchy",
      local=u"Житомирсько-Поліська єпархія",
      seat="Zhytomyr", country="UA",
      address=[u"вул. Київська, 53", u"10030, м. Житомир"],
      site="http://uapc.zt.ua/",
      sources=[MAP, "http://uapc.zt.ua/page/contacts"]),

 dict(id="ocu-zakarpattia", parent="ukraine-ocu",
      name="Zakarpattia Eparchy",
      local=u"Закарпатська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-mukachevo", parent="ukraine-ocu",
      name="Mukachevo-Karpaty Eparchy",
      local=u"Мукачівсько-Карпатська єпархія",
      seat="Uzhhorod", country="UA",
      address=[u"вул. Ю. Гойди, 4", u"88000, Закарпатська обл., м. Ужгород"],
      site="https://www.keuapc.org/",
      sources=["https://www.keuapc.org/kontakty-mkie-ptsu-2/"]),

 dict(id="ocu-zaporizhzhia", parent="ukraine-ocu",
      name="Zaporizhzhia Eparchy",
      local=u"Запорізька єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-ivano-frankivsk", parent="ukraine-ocu",
      name="Ivano-Frankivsk Eparchy",
      local=u"Івано-Франківська єпархія",
      seat="Ivano-Frankivsk", country="UA",
      address=[u"вул. Мельничука, 5", u"м. Івано-Франківськ"],
      site="https://pcu.if.ua/",
      sources=[MAP, "https://pcu.if.ua/%D0%9A%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B8"]),

 dict(id="ocu-kolomyia", parent="ukraine-ocu",
      name="Kolomyia Eparchy",
      local=u"Коломийська єпархія",
      seat="Kolomyia", country="UA",
      address=[u"вул. Є. Коновальця, 27", u"78200, м. Коломия"],
      site="https://kolomija.com/",
      sources=[MAP, "https://kolomija.com/kontakty/"]),

 dict(id="ocu-pereiaslav", parent="ukraine-ocu",
      name="Pereiaslav-Vyshneve Eparchy",
      local=u"Переяславсько-Вишневська єпархія",
      seat="Kyiv", country="UA",
      address=[u"вул. Самійла Кішки, 3А", u"03191, м. Київ"],
      site="https://pereyaslav-eparchia.kiev.ua/",
      sources=[MAP, "https://pereyaslav-eparchia.kiev.ua/kontakti"]),

 dict(id="ocu-kirovohrad", parent="ukraine-ocu",
      name="Kirovohrad Eparchy",
      local=u"Кіровоградська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-luhansk", parent="ukraine-ocu",
      name="Luhansk Eparchy",
      local=u"Луганська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-lviv", parent="ukraine-ocu",
      name="Lviv Eparchy",
      local=u"Львівська єпархія",
      seat="Lviv", country="UA",
      address=[u"вул. Федорова, 11", u"79008, м. Львів"],
      site="https://uaoc.lviv.ua/",
      sources=[MAP, "https://uaoc.lviv.ua/nashi-kontakti/"]),

 dict(id="ocu-drohobych", parent="ukraine-ocu",
      name="Drohobych-Sambir Eparchy",
      local=u"Дрогобицько-Самбірська єпархія",
      seat="Drohobych", country="UA",
      address=[u"вул. Б. Лепкого, 17/1", u"82108, Львівська обл., м. Дрогобич"],
      site="http://drogobych-orthodox.info/ukr/",
      sources=[MAP, "http://drogobych-orthodox.info/ukr/index.php/contacts"]),

 dict(id="ocu-mykolaiv", parent="ukraine-ocu",
      name="Mykolaiv Eparchy",
      local=u"Миколаївська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-odesa", parent="ukraine-ocu",
      name="Odesa Eparchy",
      local=u"Одеська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-poltava", parent="ukraine-ocu",
      name="Poltava Eparchy",
      local=u"Полтавська єпархія",
      seat="Poltava", country="UA",
      address=[u"вул. Соборний майдан, 1", u"36000, м. Полтава"],
      site="https://cerkva.pl.ua/",
      sources=[MAP, "https://cerkva.pl.ua/index.php?view=contacts"]),

 dict(id="ocu-rivne", parent="ukraine-ocu",
      name="Rivne Eparchy",
      local=u"Рівненська єпархія",
      seat="Rivne", country="UA",
      address=[u"вул. 16 липня, 4-а", u"33028, м. Рівне"],
      site="http://rivne-cerkva.rv.ua/",
      sources=[MAP, "http://rivne-cerkva.rv.ua/eparhia/upravlinnia.html"]),

 dict(id="ocu-sumy", parent="ukraine-ocu",
      name="Sumy Eparchy",
      local=u"Сумська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-ternopil", parent="ukraine-ocu",
      name="Ternopil Eparchy",
      local=u"Тернопільська єпархія",
      seat="Ternopil", country="UA",
      address=[u"вул. Князя Острозького, 19", u"46008, м. Тернопіль"],
      site="https://cerkva.te.ua/",
      sources=[MAP, "https://cerkva.te.ua/kontakty/"]),

 dict(id="ocu-ternopil-buchach", parent="ukraine-ocu",
      name="Ternopil-Buchach Eparchy",
      local=u"Тернопільсько-Бучацька єпархія",
      seat="Ternopil", country="UA",
      address=[u"вул. Руська, 22", u"46001, м. Тернопіль"],
      site="https://www.uapc.net.ua/",
      sources=["https://www.uapc.net.ua/about/"]),

 dict(id="ocu-ternopil-terebovlia", parent="ukraine-ocu",
      name="Ternopil-Terebovlia Eparchy",
      local=u"Тернопільсько-Теребовлянська єпархія",
      country="UA",
      site="https://eparchy.te.ua/",
      sources=[MAP, "https://eparchy.te.ua/"]),

 dict(id="ocu-kharkiv", parent="ukraine-ocu",
      name="Kharkiv Eparchy",
      local=u"Харківська єпархія",
      seat="Kharkiv", country="UA",
      address=[u"вулиця Семінарська, 4", u"61093, м. Харків"],
      site="https://cerkva.kharkov.ua/",
      sources=[MAP, "https://cerkva.kharkov.ua/kontakti"]),

 dict(id="ocu-kharkiv-poltava", parent="ukraine-ocu",
      name="Kharkiv-Poltava Eparchy",
      local=u"Харківсько-Полтавська єпархія",
      seat="Poltava", country="UA",
      address=[u"а/с 37", u"36000, м. Полтава"],
      site="https://uaoch.com/",
      sources=["https://uaoch.com/contact/"]),

 dict(id="ocu-kherson", parent="ukraine-ocu",
      name="Kherson Eparchy",
      local=u"Херсонська єпархія",
      seat="Kherson", country="UA",
      address=[u"вулиця Василя Стуса, 45", u"73011, Херсон"],
      site="https://pravoslav.ks.ua/",
      sources=[MAP, "https://pravoslav.ks.ua/history-diocese/"]),

 dict(id="ocu-khmelnytskyi", parent="ukraine-ocu",
      name="Khmelnytskyi Eparchy",
      local=u"Хмельницька єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-cherkasy", parent="ukraine-ocu",
      name="Cherkasy Eparchy",
      local=u"Черкаська єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-chernivtsi", parent="ukraine-ocu",
      name="Chernivtsi Eparchy",
      local=u"Чернівецька єпархія",
      country="UA",
      sources=[MAP]),

 dict(id="ocu-chernihiv", parent="ukraine-ocu",
      name="Chernihiv Eparchy",
      local=u"Чернігівська єпархія",
      seat="Chernihiv", country="UA",
      address=[u"вул. Коцюбинського, 37", u"14000, м. Чернігів"],
      site="https://www.cerkva.in.ua/",
      sources=[MAP, "https://www.cerkva.in.ua/?page_id=16"]),
]
