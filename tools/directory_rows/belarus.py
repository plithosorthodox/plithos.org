# -*- coding: utf-8 -*-
"""The fifteen dioceses of the Belarusian Exarchate.

The Exarchate carries its own dioceses in the menu of every page of
church.by, under the heading it gives itself - Белорусский Экзархат - and
publishes a page for each one naming the see, its deaneries, its parishes
and the address of its own website. Fifteen are named there and fifteen are
here.

The rows had stood under the Church of Russia, read from the Moscow
Patriarchate's register of its organisations, because that register holds
them and the Exarchate's own list had not been read. They now hang off the
Exarchate and are read from it, which is where they belong; their ids are
unchanged, so nothing that pointed at them breaks and no language has to
name them again.

Reading them from the Exarchate is not only a matter of provenance. Two
addresses in the register have moved on: Turov's diocesan administration is
at Mitropolita Filareta 1 in Mozyr and no longer on Komsomolskaya, and
Polotsk gives its postcode as 211407. Both are taken here as each see itself
prints them.

Every diocesan website named on church.by was requested and read. Thirteen
answered and carry the address of their own chancery. Two did not - Borisov
refused the request outright and Minsk's did not resolve from here - so
those two rows carry no link of their own and fall back to the Exarchate,
which does answer. Their addresses stay, from the register that published
them, because a reader can still use a street. Both are to be tried again
rather than written off.

Minsk is the exception in one further way: the Exarchate and the Minsk
diocesan administration share a house, and the address on that row is the
one church.by prints for the diocesan administration itself.


RANK, ADDED 14 SEPTEMBER 2026. Every row here already carried the Church's own
word for what the body is, inside the name its own list prints - Diocese -
and `rank` now says it in a field of its own so a reader can see it and a
filter can use it. Nothing was read again for this and nothing was guessed: a
row whose list gives it no such word carries no rank.
"""

READ = "2026-09-14"

EX = "http://church.by/belorusskiy-ekzarhat/"
CONTACTS = "http://church.by/kontakty"

ROWS = [

 dict(id="ru-babruysk", parent="belarus",
      name="Babruysk Diocese",
      rank="Diocese",
      local=u"Бобруйская епархия",
      seat="Babruysk", country="BY",
      address=[u"ул. Карбышева, д. 28, к. 2",
               u"213809, Могилевской обл., г. Бобруйск"],
      site="https://bobreparhiya.by/",
      sources=[EX + "bobrujskaja-eparhija",
               "https://bobreparhiya.by/kontakti/"]),

 dict(id="ru-barysaw", parent="belarus",
      name="Barysaw Diocese",
      rank="Diocese",
      local=u"Борисовская епархия",
      seat="Barysaw", country="BY",
      address=[u"ул. Лопатина, 32",
               u"222517, Минская область, г. Борисов"],
      sources=[EX + "borisovskaja-eparhija",
               "https://patriarchia.ru/org/475"]),

 dict(id="ru-brest", parent="belarus",
      name="Brest Diocese",
      rank="Diocese",
      local=u"Брестская епархия",
      seat="Brest", country="BY",
      address=[u"улица Гоголя, 74", u"224030, г. Брест"],
      site="https://pravbrest.by/",
      sources=[EX + "brestskaja-eparhija",
               "https://pravbrest.by/%d0%b5%d0%bf%d0%b0%d1%80%d1%85%d0%b8"
               "%d0%b0%d0%bb%d1%8c%d0%bd%d0%be%d0%b5-%d1%83%d0%bf%d1%80"
               "%d0%b0%d0%b2%d0%bb%d0%b5%d0%bd%d0%b8%d0%b5-3/"]),

 dict(id="ru-vitebsk", parent="belarus",
      name="Vitebsk Diocese",
      rank="Diocese",
      local=u"Витебская епархия",
      seat="Vitebsk", country="BY",
      address=[u"ул.Чехова, 19", u"210026, г. Витебск"],
      site="https://vitprav.by/",
      sources=[EX + "vitebskaja-eparhija", "https://vitprav.by/"]),

 dict(id="ru-homel", parent="belarus",
      name="Homel Diocese",
      rank="Diocese",
      local=u"Гомельская епархия",
      seat="Homel", country="BY",
      address=[u"ул. Митрополита Филарета, 2", u"246014, г.Гомель"],
      site="https://eparhiya.by/",
      sources=[EX + "gomelskaja-eparhija", "https://eparhiya.by/"]),

 dict(id="ru-hrodna", parent="belarus",
      name="Hrodna Diocese",
      rank="Diocese",
      local=u"Гродненская епархия",
      seat="Hrodna", country="BY",
      address=[u"ул. Митрополита Филарета, 1", u"230023, г. Гродно"],
      site="https://orthos.org/",
      sources=[EX + "grodnenskaja-eparhija", "https://orthos.org/"]),

 dict(id="ru-lida", parent="belarus",
      name="Lida Diocese",
      rank="Diocese",
      local=u"Лидская епархия",
      seat="Lida", country="BY",
      address=[u"ул. Советская, 20",
               u"231300, Гродненская обл., г. Лида"],
      site="http://lida-eparhia.by/",
      sources=[EX + "lidskaja-eparhija",
               "http://lida-eparhia.by/?page_id=16"]),

 dict(id="ru-minsk", parent="belarus",
      name="Minsk Diocese",
      rank="Diocese",
      local=u"Минская епархия",
      seat="Minsk", country="BY",
      address=[u"ул. Освобождения, 10", u"220004, Минск"],
      sources=[EX + "minskaja-eparhija", CONTACTS]),

 dict(id="ru-mahilyow", parent="belarus",
      name="Mahilyow Diocese",
      rank="Diocese",
      local=u"Могилёвская епархия",
      seat="Mahilyow", country="BY",
      address=[u"ул.Первомайская, 75", u"212030, г.Могилев"],
      site="http://mogeparhia.by/",
      sources=[EX + "mogilevskaja-eparhija",
               "http://mogeparhia.by/kontakty/"]),

 dict(id="ru-maladzyechna", parent="belarus",
      name="Maladzyechna Diocese",
      rank="Diocese",
      local=u"Молодечненская епархия",
      seat="Maladzyechna", country="BY",
      address=[u"пл. Старое Место", u"Минская обл., г. Молодечно"],
      site="https://molod-eparchy.by/",
      sources=[EX + "molodechnenskaja-eparhija",
               "https://patriarchia.ru/org/476"]),

 dict(id="ru-navahrudak", parent="belarus",
      name="Navahrudak Diocese",
      rank="Diocese",
      local=u"Новогрудская епархия",
      seat="Navahrudak", country="BY",
      address=[u"ул. Соборная, 57", u"231822, Жировичи"],
      site="http://www.eparhia.by/novogrudskaja-eparkhija.html",
      sources=[EX + "novogrudskaja-eparhija",
               "http://www.eparhia.by/kontakty.html"]),

 dict(id="ru-pinsk", parent="belarus",
      name="Pinsk Diocese",
      rank="Diocese",
      local=u"Пинская епархия",
      seat="Pinsk", country="BY",
      address=[u"ул.Первомайская, 15",
               u"225710, Брестская обл., г.Пинск"],
      site="http://pinskeparh.by/",
      sources=[EX + "pinskaja-eparhija", "http://pinskeparh.by/"]),

 dict(id="ru-polatsk", parent="belarus",
      name="Polatsk Diocese",
      rank="Diocese",
      local=u"Полоцкая епархия",
      seat="Polatsk", country="BY",
      address=[u"ул. Евфросинии Полоцкой, 80", u"211407, г. Полоцк"],
      site="https://eparhia992.by/",
      sources=[EX + "polockaja-eparhija", "https://eparhia992.by/"]),

 dict(id="ru-slutsk", parent="belarus",
      name="Slutsk Diocese",
      rank="Diocese",
      local=u"Слуцкая епархия",
      seat="Slutsk", country="BY",
      address=[u"улица Максима Богдановича, д. 9",
               u"223609, Минская область, г. Слуцк"],
      site="https://sluck-eparchiya.by/",
      sources=[EX + "sluckaja-eparhija",
               "https://sluck-eparchiya.by/kontakty/"]),

 dict(id="ru-turaw", parent="belarus",
      name="Turaw Diocese",
      rank="Diocese",
      local=u"Туровская епархия",
      seat="Mazyr", country="BY",
      founded=u"основана в 1005 году, возрождена в 1992 году",
      address=[u"ул. Митрополита Филарета, д. 1, к. 1",
               u"247777, Гомельская обл., г. Мозырь"],
      site="http://turov.by/",
      sources=[EX + "turovskaja-eparhija", "http://turov.by/"]),
]
