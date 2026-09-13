# -*- coding: utf-8 -*-
"""The archdioceses of the Greek Orthodox Patriarchate of Antioch.

Read from the Patriarchate's own list of its archdioceses and from the page
it publishes for each, in English and in Arabic. The Arabic list is the one
the Patriarchate orders by its own alphabet, and it is where `local` comes
from; the English pages carry the addresses and the telephones.

Two entries on that list are not rows here. The first is Antioch and
Damascus and Dependencies, whose centre is the Patriarchate in Damascus:
that is the patriarchal see itself and it already has a row as the Church.
The second is New York and All North America, which the directory has held
since North America was done - `antiochian-na` - and which is not written
twice.

Two further entries stand on the list under a bishop's name rather than a
see's, and no see is named in either. They are left for a reading that can
give them one.
"""

AN = "https://antiochpatriarchate.org/en/category/archdioceses/64/"

ROWS = [
 dict(id="an-bosra", parent="antioch",
      name="Archdiocese of Bosra, Hauran and Jabal al-Arab",
      local=u"بصرى وحوران وجبل العرب",
      seat="Suwayda", country="SY",
      address=["Archdiocese of Bosra Horan and Jabal-Arab",
               "po.box: 18 Swaida - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/69/", AN]),

 dict(id="an-australia", parent="antioch",
      name="Archdiocese of Australia, New Zealand and the Philippines",
      local=u"أستراليا، نيوزيلندا والفيلبّين",
      seat="Sydney", country="AU",
      address=["Antiochian Orthodox Archdiocese of Australia, New Zealand and the Philippines",
               "2 Bampton Avenue",
               "Illawong, NSW 2234",
               "Australia"],
      sources=["https://antiochpatriarchate.org/en/category/66/", AN]),

 dict(id="an-germany", parent="antioch",
      name="Archdiocese of Germany and Central Europe",
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
      local=u"بغداد والكويت وتوابعهما",
      seat="Baghdad", country="IQ",
      address=["Greek Orthodox Archdiocese",
               "P.O.Box: 8173  Al-Salemea 22052 - Kuwait"],
      sources=["https://antiochpatriarchate.org/en/category/71/", AN]),

 dict(id="an-british-isles", parent="antioch",
      name="Archdiocese of the British Isles and Ireland",
      local=u"الجُزُر البريطانيّة وإيرلندة",
      seat="London", country="GB",
      address=["St. George's Cathedral",
               "1A Redhill Street,",
               "Regent's Park  NW1 4BG",
               "UK"],
      sources=["https://antiochpatriarchate.org/en/category/73/", AN]),

 dict(id="an-beirut", parent="antioch",
      name="Archdiocese of Beirut and Dependencies",
      local=u"بيروت وتوابعها",
      seat="Beirut", country="LB",
      address=["Orthodox Archdiocese of Beirut",
               "P.O.Box: 186 Beirut - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/65/", AN]),

 dict(id="an-buenos-aires", parent="antioch",
      name="Archdiocese of Buenos Aires and All Argentine",
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
      local=u"سانتياغو وتشيلي",
      seat="Santiago", country="CL",
      address=["Arquidiócesis Metropolitana Orthodoxa de Antiqúia",
               "Santa Filomena 372- Recoleta- Santiago-Chile"],
      site="https://www.chileortodoxo.cl/",
      sources=["https://www.chileortodoxo.cl/",
               "https://antiochpatriarchate.org/en/category/78/", AN]),

 dict(id="an-byblos", parent="antioch",
      name="Archdiocese of Byblos, Batroun and Dependencies",
      local=u"جبيل والبترون وما يليهما",
      seat="Brummana", country="LB",
      address=["Greek Orthodox Archdiocese - Brummana - Al-Matn - Lebanon"],
      site="http://www.ortmtlb.org.lb/",
      sources=["http://www.ortmtlb.org.lb/",
               "https://antiochpatriarchate.org/en/category/72/", AN]),

 dict(id="an-akkar", parent="antioch",
      name="Archdiocese of Akkar and Dependencies",
      local=u"عكّار وتوابعها",
      seat="Cheikh Taba", country="LB",
      address=["Greek Orthodox Archdiocese - Cheikh Taba - Akkar - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/82/", AN]),

 dict(id="an-aleppo", parent="antioch",
      name="Archdiocese of Aleppo, Alexandretta and Dependencies",
      local=u"حلب واسكندرون وتوابعهما",
      seat="Aleppo", country="SY",
      address=["6976 Al-Villat - Patriarch Elias Moawad Street - Aleppo - Syria"],
      site="https://alepporthodox.org/",
      sources=["https://alepporthodox.org/",
               "https://antiochpatriarchate.org/en/category/74/", AN]),

 dict(id="an-france", parent="antioch",
      name="Archdiocese of France, Western and Southern Europe",
      local=u"فرنسا وأوروبا الغربيّة والجنوبيّة",
      seat="Paris", country="FR",
      address=["Archevêché Orthodoxe Antiochien de France et d'Europe occidentale et du sud",
               "22, Avenue Kléber",
               "75116 Paris - FRANCE"],
      sources=["https://antiochpatriarchate.org/en/category/83/", AN]),

 dict(id="an-hama", parent="antioch",
      name="Archdiocese of Hama and Dependencies",
      local=u"حماه وتوابعها",
      seat="Hama", country="SY",
      address=["Almadena Neighborhood - Greek Orthodox Archdiocese - Hama - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/75/", AN]),

 dict(id="an-homs", parent="antioch",
      name="Archdiocese of Homs and Dependencies",
      local=u"حمص وتوابعها",
      seat="Homs", country="SY",
      address=["Greek Orthodox Archdiocese",
               "P.O.Box: 386 Homs - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/76/", AN]),

 dict(id="an-zahleh", parent="antioch",
      name="Archdiocese of Zahleh, Baalbek and Dependencies",
      local=u"زحلة وبعلبكّ وتوابعهما",
      seat="Zahleh", country="LB",
      address=["Greek Orthodox Archdiocese - Al-Midan quarter - Zahleh - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/77/", AN]),

 dict(id="an-sao-paulo", parent="antioch",
      name="Archdiocese of Sao Paulo and All Brazil",
      local=u"ساو باولو وسائر البرازيل",
      seat="Sao Paulo", country="BR",
      address=["Rua Vergueiro 1515, CEP: 04101 - 000",
               "Paraiso, São Paulo.",
               "Brazil"],
      sources=["https://antiochpatriarchate.org/en/category/79/", AN]),

 dict(id="an-tyre-sidon", parent="antioch",
      name="Archdiocese of Tyre, Sidon and Dependencies",
      local=u"صور وصيدا وتوابعهما",
      seat="Marjayoun", country="LB",
      address=["Greek Orthodox Archdiocese, P.O.Box: 4 - Marjayoun - Lebanon"],
      sources=["https://antiochpatriarchate.org/en/category/80/", AN]),

 dict(id="an-tripoli", parent="antioch",
      name="Archdiocese of Tripoli, Al-Koura and Dependencies",
      local=u"طرابلس والكورة وتوابعهما",
      seat="Tripoli", country="LB",
      address=["Antiochian Orthodox Archdiocese of Tripoli, Al-Koura, and their dependencies",
               "Al-Marad Street - P.O.Box: 345 - Tripoli - Lebanon"],
      site="http://archtripoli.org/",
      sources=["http://archtripoli.org/",
               "https://antiochpatriarchate.org/en/category/81/", AN]),

 dict(id="an-mexico", parent="antioch",
      name="Archdiocese of Mexico, Venezuela, Central America and the Islands of the Caribbean Sea",
      local=u"المكسيك، فنزويلا، أميركا الوُسطى وجزر الكاريبي",
      seat="Mexico City", country="MX",
      address=["Pirules No 110, Col. Jardines del Pedregal, Cod. Post., 01900",
               "Mexico, D.F."],
      site="https://www.iglesiaortodoxa.org.mx/",
      sources=["https://www.iglesiaortodoxa.org.mx/",
               "https://antiochpatriarchate.org/en/category/85/", AN]),

 dict(id="an-lattakia", parent="antioch",
      name="Archdiocese of Lattakia and Dependencies",
      local=u"اللاذقيّة وتوابعها",
      seat="Lattakia", country="SY",
      address=["Greek Orthodox Archdiocese - P.O.Box: 27 - Lattakia - Syria"],
      sources=["https://antiochpatriarchate.org/en/category/84/", AN]),
]
