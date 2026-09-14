# -*- coding: utf-8 -*-
"""The dioceses of the Church of Bulgaria.

Read on 14 September 2026 from the Patriarchate's own list of its dioceses at

    https://bg-patriarshia.bg/dioceses

and then from the administration page the Patriarchate publishes for each one,
which is where the address and the diocese's own site come from and which each
row cites. The list holds thirteen dioceses in Bulgaria and two abroad, and
alongside them two entries that are not dioceses and have no row here: the
Patriarchate's page of its holy places abroad, and the Slavo-Bulgarian
monastery of Zograf on Athos.

Fifteen dioceses, less the Bulgarian Eastern Orthodox Diocese of the USA,
Canada and Australia, which was already published from North America, is the
fourteen rows written here.

ADDRESSES are the lines the Patriarchate's own administration page prints, in
the words and the lettering it prints them in - Veliko Tarnovo is set in
capitals throughout and stands that way - set out as an envelope wants them
and translated nowhere. The country line is dropped, because the page writes
it in the reader's language. Twelve of the fourteen publish an address; Vidin
and Pleven give none, and those two rows carry a name, a seat, a country and
a citation, which is a whole row.

SITES. Five dioceses publish a site of their own on that page and all five
answered: Sofia, Varna and Veliki Preslav, Vidin, Dorostol, and Ruse. Varna's
published address, mitropolia-varna.org, now answers at varnenskamitropolia.bg
and the row uses the address that answers. The other nine have no site of
their own on the Patriarchate's page and fall back to it.

NAMES. The Patriarchate publishes this list in Bulgarian, so `local` is its own
wording and `name` is the English a reader of this site is given. The diocese
in Berlin is one of the two the Patriarchate lists abroad; it prints its own
German title on its administration page, and the German is what the address
is written in.

THE NUMBER IS THE CHURCH'S OWN AND NOT ONLY ITS PAGE OF LINKS. The Statute of
the Bulgarian Orthodox Church - Bulgarian Patriarchate, published at
bg-patriarshia.bg/statute, divides the Church's territory within Bulgaria into
thirteen dioceses in its third article and names every one of them; the fourth
names the two abroad, at New York and at Berlin. Thirteen and two is fifteen,
which is what the page of dioceses lists and what this directory holds, so
nothing is missing. The Statute also names a Bulgarian church community at
Istanbul for the Orthodox Bulgarians in Turkey; a community is not a diocese
and has no row."""

READ = "2026-09-14"

BG = "https://bg-patriarshia.bg/"

ROWS = [

 dict(id="bg-sofia", parent="bulgaria",
      name="Diocese of Sofia",
      local=u"Софийска епархия",
      seat="Sofia", country="BG",
      address=[u"ул. „Цар Калоян” № 7", u"гр. София 1000"],
      site="https://mitropolia-sofia.org/",
      sources=[BG + "sofia-diocese-administration",
               "https://mitropolia-sofia.org/"]),

 dict(id="bg-varna", parent="bulgaria",
      name="Diocese of Varna and Veliki Preslav",
      local=u"Варненска и Великопреславска епархия",
      seat="Varna", country="BG",
      address=[u"пл. „Св. св. Кирил и Методий“ № 1", u"гр. Варна 9000"],
      site="https://varnenskamitropolia.bg/",
      sources=[BG + "varna-diocese-administration",
               "https://varnenskamitropolia.bg/"]),

 dict(id="bg-veliko-tarnovo", parent="bulgaria",
      name="Diocese of Veliko Tarnovo",
      local=u"Великотърновска епархия",
      seat="Veliko Tarnovo", country="BG",
      address=[u"УЛ. ИВАН ВАЗОВ № 25", u"ПОЩЕНСКА КУТИЯ 131",
               u"ГР. ВЕЛИКО ТЪРНОВО 5000"],
      sources=[BG + "turnovo-diocese-administration"]),

 dict(id="bg-vidin", parent="bulgaria",
      name="Diocese of Vidin",
      local=u"Видинска епархия",
      seat="Vidin", country="BG",
      site="https://vidinskamitropolia.bg/",
      sources=[BG + "vidin-diocese-administration",
               "https://vidinskamitropolia.bg/"]),

 dict(id="bg-vratsa", parent="bulgaria",
      name="Diocese of Vratsa",
      local=u"Врачанска епархия",
      seat="Vratsa", country="BG",
      address=[u"бул. \"Христо Ботев\" № 4а", u"Враца - 3000"],
      sources=[BG + "vraca-diocese-administration"]),

 dict(id="bg-dorostol", parent="bulgaria",
      name="Diocese of Dorostol",
      local=u"Доростолска епархия",
      seat="Silistra", country="BG",
      address=[u"ул. „Софроний Врачански” № 6", u"Силистра - 7500"],
      site="https://www.dorostolskamitropolia.com/",
      sources=[BG + "dorostol-diocese-administration",
               "https://www.dorostolskamitropolia.com/"]),

 dict(id="bg-lovech", parent="bulgaria",
      name="Diocese of Lovech",
      local=u"Ловчанска епархия",
      seat="Lovech", country="BG",
      address=[u"ул. \"Черковна\"№12", u"гр. Ловеч - 5500"],
      sources=[BG + "lovech-diocese-administration"]),

 dict(id="bg-nevrokop", parent="bulgaria",
      name="Diocese of Nevrokop",
      local=u"Неврокопска епархия",
      seat="Gotse Delchev", country="BG",
      address=[u"Бул. \"Гоце Делчев\" № 1", u"Гр. Гоце Делчев 2900"],
      sources=[BG + "nevrokop-diocese-administration"]),

 dict(id="bg-pleven", parent="bulgaria",
      name="Diocese of Pleven",
      local=u"Плевенска епархия",
      seat="Pleven", country="BG",
      sources=[BG + "pleven-diocese-administration"]),

 dict(id="bg-plovdiv", parent="bulgaria",
      name="Diocese of Plovdiv",
      local=u"Пловдивска епархия",
      seat="Plovdiv", country="BG",
      address=[u"ул. \"Станислав Доспевски\" № 14-16", u"Пловдив - 4000"],
      sources=[BG + "plovdiv-diocese-administration"]),

 dict(id="bg-ruse", parent="bulgaria",
      name="Diocese of Ruse",
      local=u"Русенска епархия",
      seat="Ruse", country="BG",
      address=[u"пл. Св. Троица, № 9", u"7000 гр. Русе"],
      site="https://www.rusenska-mitropolia.bg/",
      sources=[BG + "ruse-diocese-administration",
               "https://www.rusenska-mitropolia.bg/"]),

 dict(id="bg-sliven", parent="bulgaria",
      name="Diocese of Sliven",
      local=u"Сливенска епархия",
      seat="Sliven", country="BG",
      address=[u"площад \"Хаджи Димитър\" 5", u"гр. Сливен 8800"],
      sources=[BG + "sliven-diocese-administration"]),

 dict(id="bg-stara-zagora", parent="bulgaria",
      name="Diocese of Stara Zagora",
      local=u"Старозагорска епархия",
      seat="Stara Zagora", country="BG",
      address=[u"уч. \"Св. ап. Карп\" № 4", u"Стара Загора - 6000"],
      sources=[BG + "zagora-diocese-administration"]),

 dict(id="bg-western-central-europe", parent="bulgaria",
      name="Bulgarian Eastern Orthodox Diocese of Western and Central Europe",
      local=u"Българска източноправославна епархия в Западна и Средна Европа",
      seat="Berlin", country="DE",
      address=[u"Leibnizstraße 77", u"10625 Berlin"],
      sources=[BG + "west-eu-diocese-administration"]),
]
