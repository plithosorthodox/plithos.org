# -*- coding: utf-8 -*-
"""Churches read after the spine, and the record of what was asked.

The spine of twenty-two was read on 13 September 2026 and the page then said
every Orthodox Church was here. It was not: the Chinese Autonomous Orthodox
Church was missing, and one Church missing is reason to doubt the count
rather than to assert it. So the whole question was put again, body by body,
and this file holds both halves of the answer - the rows that came of it, and
the bodies that were considered and left out. The second half matters as much
as the first, because the next person needs to know the question was asked.

The bar is the one in docs/DIRECTORY.md and nothing was added to it: a body
appears because an autocephalous Church names it among its own. That is a
fact about a published list. Where Churches differ, `standing` names an act
and who did it, and the site never says who is right.


IN, AND ON WHAT

  china       The Chinese Autonomous Orthodox Church. The Statute of the
              Russian Orthodox Church, chapter XI, names it and the Japanese
              Orthodox Church as the two Autonomous Churches; the Moscow
              Patriarchate keeps a page for it at patriarchia.ru/org/265.
              The Moscow Patriarchate writes that it was founded in 1956,
              its bishop of Beijing being consecrated the following May; it
              has had no bishop since 1962 and its eparchies of Beijing and
              Shanghai stand vacant. Its communities are in china.py.

  rocor       The Russian Orthodox Church Outside of Russia. It was already
              in the directory, filed as a diocese under Russia, and that
              was wrong. The same chapter XII of the same Statute that names
              the three Self-governing Churches names ROCOR in section 17,
              in the same terms: a self-governing part of the Russian
              Orthodox Church, with its own historically established
              dioceses, parishes and institutions. A body with dioceses is
              not a diocese, and it was standing in the list beside nine of
              its own - Eastern America, Western America, Mid-America,
              Canada, Australia and New Zealand, Great Britain and Western
              Europe, Germany, South America - as though it were their
              equal. It keeps its id, so nothing that pointed at it breaks.
              Those nine still carry parent="russia" and want re-parenting
              to this row; that is russia.py's work, not this file's.

  latvia      The Latvian Orthodox Church. Chapter XII of the Statute of the
              Russian Orthodox Church names it first among the Self-governing
              Churches. Its own site publishes the address of its Synod. Two
              acts stand over it and the row names the nearer one: the Saeima
              amended the Law on the Latvian Orthodox Church on 8 September
              2022 to establish its status as autocephalous, and the Church's
              own Council of 20 October 2022 voted to amend its Statute
              accordingly. The site is read over http; https is refused from
              here.

  moldova     The Orthodox Church of Moldova, styling itself the Metropolis
              of Chisinau and All Moldova. Named second in the same chapter.
              Not to be confused with the Romanian Patriarchate's Archdiocese
              of Chisinau - the Metropolis of Bessarabia - which is already
              in this directory as ro-chisinau and sits in the same city
              under a different Church. Both are real and neither is a
              duplicate of the other.

  estonia-ekok
              The Estonian Christian Orthodox Church, seated in Tallinn, and
              not the Estonian Apostolic Orthodox Church, which has been
              here since the spine was read because Constantinople names it
              on its own page of autonomous Churches. docs/DIRECTORY.md
              deferred this one for a plain reason: its own site did not say
              which Church it belonged to and no published list naming it had
              been read. That is now met. The Holy Synod of the Russian
              Orthodox Church, on 10 April 2025, published a statement about
              the Estonian law and named the body in it as a self-governing
              Church within the Moscow Patriarchate. The bar is a published
              list naming the body, and this is one. Its own site gives its
              name and its address and still says nothing about jurisdiction,
              which is why the row's standing is attributed to the Synod that
              wrote it and not to the body itself.
              The note in docs/DIRECTORY.md under "Rows deliberately not yet
              published" is now out of date and wants rewriting.

  belarus     The Belarusian Exarchate. Chapter XIII of the Statute names one
              exarchate - "In the Russian Orthodox Church at present there is
              the Belarusian Exarchate" - and gives it a Synod and a second
              official name, the Belarusian Orthodox Church, which is the
              name its own site prints at the head of every page. Read over
              http; https is refused from here.


OUT, AND WHY

  ohrid       The Ohrid Archbishopric. There is nothing to add, and the
              reason is that there are two bodies of the name and neither
              wants a new row. The Macedonian Orthodox Church - Ohrid
              Archbishopric has been here since the spine was read, at
              Skopje, and the Serbian Patriarchate granted it autocephaly on
              5 June 2022. The other, the Serbian Church's own Orthodox
              Ohrid Archbishopric, which had stood in North Macedonia since
              2002, was united with it in Ohrid on 5 June 2023 and no longer
              exists separately. A row for it would be a row for a body that
              has been dissolved into one already listed.
              Worth a later pass: the macedonia row carries no standing, and
              the act of 5 June 2022 is exactly what standing is for.

  athos       The monastic republic of Mount Athos is in, but not as a
              Church, and so not in this file. The Ecumenical Patriarchate
              names the Monastic Community of the Holy Mountain among its
              own, under Patriarchal and Stavropegic Monasteries on its page
              of the Eparchies of the Throne, and calls it a Holy Patriarchal
              Exarchy. That is where the Patriarchate files it and that is
              where the row goes: under Constantinople, in tools/directory.py
              beside the Throne's other eparchies. It is not autocephalous
              and it is not an autonomous Church, and putting it in the list
              of Churches would say that it is. The Patriarchate publishes no
              postal address for it, only a telephone and an electronic one,
              so the row carries a name and its citations and nothing else,
              which docs/DIRECTORY.md says plainly is a good row.

  uoc-usa     The Ukrainian Orthodox Church of the USA and the Ukrainian
  uocc        Orthodox Church of Canada are filed as dioceses under
              Constantinople, and that is right. The Ecumenical Patriarchate
              lists both on its own page of the Eparchies of the Throne in
              America - "Ukrainian Orthodox Church in the USA" and "Ukrainian
              Orthodox Church in Canada" - beside the Archdiocese of America,
              the Metropolis of Buenos Aires and the rest. They are eparchies
              of the Throne by the Throne's own reckoning. Nothing to change.

  ru-exarch   The Patriarchal Exarchate of Africa, the Patriarchal Exarchate
              in Western Europe and the Patriarchal Exarchate of South-East
              Asia. All three are real, all three are published by the Moscow
              Patriarchate as its own, and under the bar all three belong
              here on the same terms as the Belarusian Exarchate. They are
              not in because they are groupings of dioceses abroad whose
              dioceses are already in russia.py under parent="russia", and
              lifting them means re-parenting those, which is that file's
              work and another lane's. Recorded so that the next pass adds
              them rather than concluding the list is complete. The Statute
              chapter that names exarchates knows only the Belarusian one;
              these three were established by the Holy Synod afterwards, in
              2018, 2019 and 2021, and the published chapter has not caught
              up with them.

  cn-beijing  Beijing, Hong Kong, Shanghai, Guangzhou, Shenzhen, Dalian and
  cn-hongkong Taipei all have Orthodox communities and none of them is a
  cn-shanghai community of the Chinese Autonomous Orthodox Church, so far as
              any Church publishes. The Moscow Patriarchate's own report of
              October 2024 on the Dormition church in Beijing names them
              together as its own: the church on the territory of the Russian
              embassy in Beijing, Saints Peter and Paul in Hong Kong, the
              parishes in Shenzhen and Guangzhou, the Holy Cross parish in
              Taipei, the community in Shanghai and the Archangel Michael
              parish in Dalian. The Hong Kong parish styles itself "Orthodox
              Parish of Apostles Saints Peter and Paul (Moscow Patriarchate)"
              and was revived by decision of the Holy Synod on 6 October
              2008. They belong under Russia, not under China, and that is
              russia.py's file to write.

  estonia-eaok
              Already here since the spine was read. Nothing changed.

Order runs on from twenty-two, which is where the spine stopped. It is a
sort key and not a ruling: the Churches read first hold the numbers they
were given, and these follow them rather than being interleaved.

One thing this file cannot say and the page cannot show. Four of the six
rows here are what the Statute of the Russian Orthodox Church calls
Self-governing Churches, and one is an Exarchate, and the page has two
groups only - autocephalous and autonomous - so they are grouped with the
autonomous. The heading is the page's own word for "not autocephalous"; the
exact word each Church uses for each body is on the row, in standing, where
it is attributed. A third group would be truer and is not this file's to
make.
"""

READ = "2026-09-14"

# The Statute of the Russian Orthodox Church, chapter by chapter, as the
# Department for External Church Relations publishes it. Four of the rows
# below are in this directory because a chapter of it names them.
UST_XI = "https://mospat.ru/en/documents/92097-xi-the-autonomous-churches/"
UST_XII = "https://mospat.ru/en/documents/92098-xii-the-self-governing-churches/"
UST_XIII = "https://mospat.ru/en/documents/92099-xiii-the-exarchates/"

ROWS = [
 dict(id="china", order=23, kind="autonomous",
      name="The Chinese Autonomous Orthodox Church",
      country="CN", checked=READ,
      sources=["https://patriarchia.ru/org/265", UST_XI],
      standing="The Statute of the Russian Orthodox Church names it, with the Japanese Orthodox Church, as one of the two Autonomous Churches.",
      standing_source=UST_XI),

 dict(id="rocor", order=24, kind="autonomous",
      name="Russian Orthodox Church Outside of Russia",
      seat="New York", country="US", checked=READ,
      address=["75 East 93rd Street", "New York, NY 10128"],
      site="https://www.synod.com/synod/indexeng.htm",
      sources=["https://www.synod.com/synod/indexeng.htm", UST_XII],
      standing="The Statute of the Russian Orthodox Church names it a self-governing part of that Church, with its historically established dioceses, parishes and institutions.",
      standing_source=UST_XII),

 dict(id="latvia", order=25, kind="autonomous",
      name="The Latvian Orthodox Church",
      local=u"Latvijas Pareizticīgā Baznīca",
      seat="Riga", country="LV", checked=READ,
      address=[u"Latvijas Pareizticīgās Baznīcas sinode", "Pils 14",
               u"Rīga LV-1050"],
      site="http://www.pareizticiba.lv/",
      sources=["http://www.pareizticiba.lv/index.php?id=89",
               "http://www.pareizticiba.lv/index.php?newid=9700", UST_XII],
      standing="Its Council of 20 October 2022 voted to amend the Statute of the Latvian Orthodox Church in accordance with the law on its autocephalous status adopted by the Saeima on 8 September 2022.",
      standing_source="http://www.pareizticiba.lv/index.php?newid=9700"),

 dict(id="moldova", order=26, kind="autonomous",
      name="The Orthodox Church of Moldova",
      local=u"Mitropolia Chişinăului şi a Întregii Moldove",
      seat="Chisinau", country="MD", checked=READ,
      address=[u"str. Bucureşti 119", u"MD-2004 Chişinău"],
      site="https://mitropolia.md/",
      sources=["https://mitropolia.md/contacte/", UST_XII],
      standing="The Statute of the Russian Orthodox Church names it among the Self-governing Churches.",
      standing_source=UST_XII),

 dict(id="estonia-ekok", order=27, kind="autonomous",
      name="Estonian Orthodox Christian Church",
      local=u"Eesti Kristlik Õigeusu Kirik",
      seat="Tallinn", country="EE", checked=READ,
      address=["Pikk 64/1-4", "10133 Tallinn"],
      site="https://et.orthodox.ee/",
      sources=["https://et.orthodox.ee/", "https://mospat.ru/en/news/93080/",
               UST_XII],
      standing="The Holy Synod of the Russian Orthodox Church, on 10 April 2025, named it a self-governing Church within the Moscow Patriarchate.",
      standing_source="https://mospat.ru/en/news/93080/"),

 dict(id="belarus", order=28, kind="autonomous",
      name="The Belarusian Exarchate",
      local=u"Белорусская Православная Церковь (Белорусский Экзархат Московского Патриархата)",
      seat="Minsk", country="BY", checked=READ,
      address=[u"220004, Минск", u"ул. Освобождения, 10"],
      site="http://church.by/",
      sources=["http://church.by/kontakty", UST_XIII],
      standing="The Statute of the Russian Orthodox Church names the Belarusian Exarchate as the one exarchate now in that Church, and the Belarusian Orthodox Church as its other official name.",
      standing_source=UST_XIII),
]
