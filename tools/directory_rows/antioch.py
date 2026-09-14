# -*- coding: utf-8 -*-
"""The archdioceses of the Greek Orthodox Patriarchate of Antioch.

Read from the Patriarchate's own list of its archdioceses and from the page
it publishes for each, in English and in Arabic. The Arabic list is the one
the Patriarchate orders by its own alphabet, and it is where `local` comes
from; the English pages carry the addresses and the telephones.

That list was counted again on 14 September 2026, in both languages, and it
holds twenty-four entries in each - the same twenty-four, in the same order.
The Patriarchate states no total in prose anywhere this machine could reach;
its own list is the whole of what it says about how many there are.

Twenty-one of those twenty-four are rows here. Two are not. The first is
Antioch and Damascus and Dependencies, whose centre is the Patriarchate in
Damascus: that is the patriarchal see itself and it already has a row as the
Church. The second is New York and All North America, which the directory
has held since North America was done - `antiochian-na` - and which is not
written twice.

The last two entries stand on the list under a bishop's name rather than a
see's. One of them now has a row and the other still has none, and the
difference is what the page behind the name says. The Metropolitan of Shahba
has a page naming a body, The Antiochian Metochion in Moscow, Russia, with
an address of its own, and that body is `an-moscow-metochion`. The
Metropolitan Paul (Yazigi) has a page naming no body at all, and it is left
for a reading that can give it one.

GERMANY'S DOOR WAS QUESTIONED AND IS SOUND. rum-orthodox.de was flagged here
because a check looking for the words of this row's English name in the page
found none, which is what happens when a see in Germany writes in German. The
page is the body's own and says so across its masthead: Antiochenisch-Orthodoxe
Metropolie von Deutschland und Mitteleuropa, with its parishes from Munich to
Utrecht and Vienna, its metropolitan office, and its own Arabic beside the
German. The link stays. Worth knowing for a later pass: it styles itself a
Metropolitanate where the Patriarchate's list of its archdioceses calls it an
archdiocese, and the row keeps the Patriarchate's word because the row is read
from the Patriarchate's list.

RANK. The Patriarchate publishes these under one heading, Archdioceses, and
every row here carries that word. The Metochion in Moscow is not on that
heading and carries none.

The diaspora was the part expected to be short and was not: the nine
archdioceses the Patriarchate lists outside the Middle East - Australia and
New Zealand and the Philippines, Germany and Central Europe, the British
Isles and Ireland, France and Western and Southern Europe, Buenos Aires,
Santiago, Sao Paulo, Mexico, and New York - were all here already.
"""

AN = "https://antiochpatriarchate.org/en/category/archdioceses/64/"
# The same list in the Patriarchate's own language, where each archdiocese is
# named as it names itself.
AN_AR = "https://antiochpatriarchate.org/ar/category/archdioceses/64/"

ROWS = [
 dict(id="an-bosra", parent="antioch",
      name="Archdiocese of Bosra, Hauran and Jabal al-Arab",
      rank="Archdiocese",
      local=u"بصرى وحوران وجبل العرب",
      seat="Suwayda", country="SY",
      address=["Archdiocese of Bosra Horan and Jabal-Arab",
               "po.box: 18 Swaida - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/69/", AN]),

 dict(id="an-australia", parent="antioch",
      name="Archdiocese of Australia, New Zealand and the Philippines",
      rank="Archdiocese",
      local=u"أستراليا، نيوزيلندا والفيلبّين",
      seat="Sydney", country="AU",
      address=["Antiochian Orthodox Archdiocese of Australia, New Zealand and the Philippines",
               "2 Bampton Avenue",
               "Illawong, NSW 2234",
               "Australia"],
      sources=["https://antiochpatriarchate.org/en/category/66/", AN]),

 dict(id="an-germany", parent="antioch",
      name="Archdiocese of Germany and Central Europe",
      rank="Archdiocese",
      local=u"ألمانيا واوروبا الوسطى",
      seat="Cologne", country="DE",
      address=["Antiochian Orthodox Archdiocese of Germany and Central Europe",
               "Geranien Weg 27-29",
               "50769 Köln",
               "Germany"],
      site="https://rum-orthodox.de/",
      sources=["https://rum-orthodox.de/",
               "https://antiochpatriarchate.org/en/category/67/", AN]),

 dict(id="an-baghdad", parent="antioch",
      name="Archdiocese of Baghdad, Kuwait and Dependencies",
      rank="Archdiocese",
      local=u"بغداد والكويت وتوابعهما",
      seat="Baghdad", country="IQ",
      address=["Greek Orthodox Archdiocese",
               "P.O.Box: 8173  Al-Salemea 22052 - Kuwait"],
      sources=["https://antiochpatriarchate.org/en/category/71/", AN]),

 dict(id="an-british-isles", parent="antioch",
      name="Archdiocese of the British Isles and Ireland",
      rank="Archdiocese",
      local=u"الجُزُر البريطانيّة وإيرلندة",
      seat="London", country="GB",
      address=["St. George's Cathedral",
               "1A Redhill Street,",
               "Regent's Park  NW1 4BG",
               "UK"],
      sources=["https://antiochpatriarchate.org/en/category/73/", AN]),

 dict(id="an-beirut", parent="antioch",
      name="Archdiocese of Beirut and Dependencies",
      rank="Archdiocese",
      local=u"بيروت وتوابعها",
      seat="Beirut", country="LB",
      address=["Orthodox Archdiocese of Beirut",
               "P.O.Box: 186 Beirut - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/65/", AN]),

 dict(id="an-buenos-aires", parent="antioch",
      name="Archdiocese of Buenos Aires and All Argentine",
      rank="Archdiocese",
      local=u"بوينس آيرس وسائر الارجنتين",
      seat="Buenos Aires", country="AR",
      address=["Archdiocese of Buenos Aires and all Argentine",
               "Av. Raúl Scalabrini Ortiz 1261",
               "C1414DNM - Ciudad Autónoma de Buenos Aires",
               "Argentina"],
      site="https://acoantioquena.com/",
      sources=["https://acoantioquena.com/",
               "https://antiochpatriarchate.org/en/category/68/", AN]),

 dict(id="an-santiago", parent="antioch",
      name="Archdiocese of Santiago and All Chile",
      rank="Archdiocese",
      local=u"سانتياغو وتشيلي",
      seat="Santiago", country="CL",
      address=["Arquidiócesis Metropolitana Orthodoxa de Antiqúia",
               "Santa Filomena 372- Recoleta- Santiago-Chile"],
      site="https://www.chileortodoxo.cl/",
      sources=["https://www.chileortodoxo.cl/",
               "https://antiochpatriarchate.org/en/category/78/", AN]),

 dict(id="an-byblos", parent="antioch",
      name="Archdiocese of Byblos, Batroun and Dependencies",
      rank="Archdiocese",
      local=u"جبيل والبترون وما يليهما",
      seat="Brummana", country="LB",
      address=["Greek Orthodox Archdiocese - Brummana - Al-Matn - Lebanon"],
      site="http://www.ortmtlb.org.lb/",
      sources=["http://www.ortmtlb.org.lb/",
               "https://antiochpatriarchate.org/en/category/72/", AN]),

 dict(id="an-akkar", parent="antioch",
      name="Archdiocese of Akkar and Dependencies",
      rank="Archdiocese",
      local=u"عكّار وتوابعها",
      seat="Cheikh Taba", country="LB",
      address=["Greek Orthodox Archdiocese - Cheikh Taba - Akkar - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/82/", AN]),

 dict(id="an-aleppo", parent="antioch",
      name="Archdiocese of Aleppo, Alexandretta and Dependencies",
      rank="Archdiocese",
      local=u"حلب واسكندرون وتوابعهما",
      seat="Aleppo", country="SY",
      address=["6976 Al-Villat - Patriarch Elias Moawad Street - Aleppo - Syria"],
      site="https://alepporthodox.org/",
      sources=["https://alepporthodox.org/",
               "https://antiochpatriarchate.org/en/category/74/", AN]),

 dict(id="an-france", parent="antioch",
      name="Archdiocese of France, Western and Southern Europe",
      rank="Archdiocese",
      local=u"فرنسا وأوروبا الغربيّة والجنوبيّة",
      seat="Paris", country="FR",
      address=["Archevêché Orthodoxe Antiochien de France et d'Europe occidentale et du sud",
               "22, Avenue Kléber",
               "75116 Paris - FRANCE"],
      sources=["https://antiochpatriarchate.org/en/category/83/", AN]),

 dict(id="an-hama", parent="antioch",
      name="Archdiocese of Hama and Dependencies",
      rank="Archdiocese",
      local=u"حماه وتوابعها",
      seat="Hama", country="SY",
      address=["Almadena Neighborhood - Greek Orthodox Archdiocese - Hama - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/75/", AN]),

 dict(id="an-homs", parent="antioch",
      name="Archdiocese of Homs and Dependencies",
      rank="Archdiocese",
      local=u"حمص وتوابعها",
      seat="Homs", country="SY",
      address=["Greek Orthodox Archdiocese",
               "P.O.Box: 386 Homs - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/76/", AN]),

 dict(id="an-zahleh", parent="antioch",
      name="Archdiocese of Zahleh, Baalbek and Dependencies",
      rank="Archdiocese",
      local=u"زحلة وبعلبكّ وتوابعهما",
      seat="Zahleh", country="LB",
      address=["Greek Orthodox Archdiocese - Al-Midan quarter - Zahleh - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/77/", AN]),

 dict(id="an-sao-paulo", parent="antioch",
      name="Archdiocese of Sao Paulo and All Brazil",
      rank="Archdiocese",
      local=u"ساو باولو وسائر البرازيل",
      seat="Sao Paulo", country="BR",
      address=["Rua Vergueiro 1515, CEP: 04101 - 000",
               "Paraiso, São Paulo.",
               "Brazil"],
      sources=["https://antiochpatriarchate.org/en/category/79/", AN]),

 dict(id="an-tyre-sidon", parent="antioch",
      name="Archdiocese of Tyre, Sidon and Dependencies",
      rank="Archdiocese",
      local=u"صور وصيدا وتوابعهما",
      seat="Marjayoun", country="LB",
      address=["Greek Orthodox Archdiocese, P.O.Box: 4 - Marjayoun - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/80/", AN]),

 dict(id="an-tripoli", parent="antioch",
      name="Archdiocese of Tripoli, Al-Koura and Dependencies",
      rank="Archdiocese",
      local=u"طرابلس والكورة وتوابعهما",
      seat="Tripoli", country="LB",
      address=["Antiochian Orthodox Archdiocese of Tripoli, Al-Koura, and their dependencies",
               "Al-Marad Street - P.O.Box: 345 - Tripoli - Lebanon"],
      site="http://archtripoli.org/",
      sources=["http://archtripoli.org/",
               "https://antiochpatriarchate.org/en/category/81/", AN]),

 dict(id="an-mexico", parent="antioch",
      name="Archdiocese of Mexico, Venezuela, Central America and the Islands of the Caribbean Sea",
      rank="Archdiocese",
      local=u"المكسيك، فنزويلا، أميركا الوُسطى وجزر الكاريبي",
      seat="Mexico City", country="MX",
      address=["Pirules No 110, Col. Jardines del Pedregal, Cod. Post., 01900",
               "Mexico, D.F."],
      site="https://www.iglesiaortodoxa.org.mx/",
      sources=["https://www.iglesiaortodoxa.org.mx/",
               "https://antiochpatriarchate.org/en/category/85/", AN]),

 dict(id="an-lattakia", parent="antioch",
      name="Archdiocese of Lattakia and Dependencies",
      rank="Archdiocese",
      local=u"اللاذقيّة وتوابعها",
      seat="Lattakia", country="SY",
      address=["Greek Orthodox Archdiocese - P.O.Box: 27 - Lattakia - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/84/", AN]),

 # The Patriarchate's representation in Moscow. It stands on the list of
 # archdioceses under the name of the Metropolitan of Shahba rather than
 # under its own, and the page behind that name is where the body is named
 # and where its address is printed. The clergyman's line at the head of the
 # address block is dropped; a see is stable and a man in it is not.
 dict(id="an-moscow-metochion", parent="antioch",
      name="The Antiochian Metochion in Moscow, Russia",
      local=u"الأمطش الأنطاكيّ في موسكو - روسيا",
      seat="Moscow", country="RU", checked="2026-09-14",
      address=[u"Metoche d’Antioche à Moscou",
               "15 A. Archangelsky Pereoulok",
               "Moscou 101000",
               "Russia"],
      sources=["https://antiochpatriarchate.org/en/category/"
               "his-eminence-the-most-reverend-niphon-metropolitan-of-shahba/"
               "155/", AN]),
]
