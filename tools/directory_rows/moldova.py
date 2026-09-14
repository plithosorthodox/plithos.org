# -*- coding: utf-8 -*-
"""The six eparchies of the Metropolis of Chisinau and All Moldova.

The Metropolis publishes one page of its eparchies and names six on it, each
with the address of its own site, and the same six stand in the menu of
every page under the heading Structura BOM. Six are named there and six are
here.

The Metropolitan's own see is not among them and is not missing: the
Metropolis administers the deaneries of Chisinau directly, as its own page
of protopopiates shows, so the see appears in this directory as the Church
itself rather than as a seventh eparchy under it.

The rows had stood under the Church of Russia, read from the Moscow
Patriarchate's register of its organisations. They now hang off the Church
of Moldova and are read from it; their ids are unchanged, so nothing that
pointed at them breaks.

Reading them from their own Church changed what they say. The register
names each see in Russian and prints its street in Russian too - Kishinev,
ulitsa Bukuresht, ulitsa Natsionale - and this Church writes in Romanian.
An address goes on an envelope in the words the destination reads, so every
address here is the one the eparchy itself prints, and the name beside it is
the one its own Church prints, diacritics and all, including where the
Metropolis sets the cedilla forms for two of the six and the comma forms for
the other four.

Every one of the six sites answered and every one carries the address of its
own chancery. Tiraspol publishes in Russian and its address is given in the
words it prints; the line naming the territory is left off, as the line
naming the country is on every row, because the page writes the country in
the reader's own language and this site makes no claim about a border.


RANK, ADDED 14 SEPTEMBER 2026. Every row here already carried the Church's own
word for what the body is, inside the name its own list prints - Diocese -
and `rank` now says it in a field of its own so a reader can see it and a
filter can use it. Nothing was read again for this and nothing was guessed: a
row whose list gives it no such word carries no rank.
"""

READ = "2026-09-14"

EPARHII = "https://mitropolia.md/eparhii/"

ROWS = [

 dict(id="ru-balti", parent="moldova",
      name="Balti Diocese",
      rank="Diocese",
      local=u"Eparhia de Bălţi şi Făleşti",
      seat="Balti", country="MD",
      address=[u"str. Visarion Puiu 1", u"municipiul Bălţi"],
      site="https://ephbalti.md/",
      founded=u"Образована определением Священного Синода Русской Православной Церкви от 6 октября 2006 г. (журнал № 114) путем выделения из состава Кишиневской епархии.",
      sources=[EPARHII, "https://ephbalti.md/contacte",
               "https://patriarchia.ru/org/237"]),

 dict(id="ru-cahul", parent="moldova",
      name="Cahul Diocese",
      rank="Diocese",
      local=u"Eparhia de Cahul și Comrat",
      seat="Cahul", country="MD",
      address=[u"str. Lev Tolstoi 1", u"MD-3900, Mun. Cahul"],
      site="https://episcopiasud.md/ro/",
      founded=u"Образована 17 июля 1998 г.",
      sources=[EPARHII, "https://episcopiasud.md/ro/contacte",
               "https://patriarchia.ru/org/163"]),

 dict(id="ru-edinet", parent="moldova",
      name="Edinet Diocese",
      rank="Diocese",
      local=u"Eparhia de Edineţ şi Briceni",
      seat="Edinet", country="MD",
      address=[u"str. Șoseaua Bucovinei 35/4", u"MD - 4601, or. Edinet"],
      site="https://eparhia-edinet.md/",
      founded=u"Образована 6 октября 1998 г.",
      sources=[EPARHII, "https://eparhia-edinet.md/",
               "https://patriarchia.ru/org/162"]),

 dict(id="ru-soroca", parent="moldova",
      name="Soroca Diocese",
      rank="Diocese",
      local=u"Eparhia de Soroca și Drochia",
      seat="Soroca", country="MD",
      address=[u"str. Ștefan cel Mare, 32", u"MD - 3006, mun. Soroca"],
      site="https://eparhiasoroca.md/",
      founded=u"Священный Синод Русской Православной Церкви на заседании 30 мая 2024 г. (журнал № 52) постановил учредить Сорокскую епархию в административных границах Сорокского, Дрокиевского, Флорештского и Рышканского р-нов, выделив ее из состава Кишиневской епархии.",
      sources=[EPARHII, "https://eparhiasoroca.md/",
               "https://patriarchia.ru/org/581"]),

 dict(id="ru-tiraspol", parent="moldova",
      name="Tiraspol Diocese",
      rank="Diocese",
      local=u"Eparhia de Tiraspol și Dubăsari",
      seat="Tiraspol", country="MD",
      address=[u"ул. Шевченко 25", u"MD-3300, г. Тирасполь"],
      site="https://diocese-tiras.org/",
      founded=u"Образована решением Священного Синода Русской Православной Церкви 6 октября 1998 г. путем преобразования Дубоссарского викариатства Кишиневской епархии Кишиневской и Молдавской митрополии.",
      sources=[EPARHII, "https://diocese-tiras.org/",
               "https://patriarchia.ru/org/66"]),

 dict(id="ru-ungheni", parent="moldova",
      name="Ungheni Diocese",
      rank="Diocese",
      local=u"Eparhia de Ungheni și Nisporeni",
      seat="Ungheni", country="MD",
      address=[u"str. Națională, nr. 8", u"MD-3606, mun. Ungheni"],
      site="https://episcopia-ungheni.md/ro/",
      founded=u"Образована решением Священного Синода Русской Православной Церкви от 6 октября 2006 г. (журнал № 105) путем выделения из состава Кишиневской митрополии.",
      sources=[EPARHII, "https://episcopia-ungheni.md/ro/contact-2/",
               "https://patriarchia.ru/org/180"]),
]
