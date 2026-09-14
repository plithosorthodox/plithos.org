# -*- coding: utf-8 -*-
"""The dioceses of the Russian Orthodox Church Outside of Russia.

Eight dioceses and the Russian Ecclesiastical Mission in Jerusalem. They
stood in tools/directory_rows/russia.py, filed among the Moscow eparchies,
from the day ROCOR was still a diocese itself; ROCOR has its own row in
_churches.py now, and its own list belongs in its own file.

WHAT THE CHURCH SAYS ABOUT ITSELF, AND WHERE THE TWO PAGES DIFFER

ROCOR states no number in prose. Its Regulations describe a Church "of
dioceses with their parishes, church communities, spiritual missions and
monasteries" and count none of them. So the count comes from the two lists
it publishes, and they agree on eight: the roll of its Hierarchy names eight
diocesan bishops, and its page of sites names the same eight dioceses.

Its parish directory disagrees, and the difference is worth stating rather
than picking quietly. The filter there offers nine, splitting a Diocese of
Great Britain from a Diocese of Western Europe. The Diocese itself settles
it on its own chancellery page: the formerly separate Diocese of Great
Britain and Ireland was united with that of Western Europe, and the Geneva
chancellery was formally closed at the end of 2019. One diocese, two
regions, and a parish filter that still sorts by the older pair. The
directory carries the eight.

The same parish filter lists the Ecclesiastical Mission in Jerusalem beside
the dioceses, and so do the roll of the Hierarchy and the page of sites. It
is not a diocese and is not counted as one; it is a body ROCOR names among
its own, with a street of its own and a door of its own, and it has a row.
"Stavropegial Institutions" also stands in that filter and has none: it is a
heading over houses, not a body.

The vicariates are not here and are not omissions. Manhattan, Syracuse,
Boston, Sonora, Seattle and Stuttgart are auxiliary sees within the
dioceses of Eastern America, Western America and Germany, and the Church
lists them under those dioceses rather than beside them.

WHAT WAS READ

All nine were read on 14 September 2026 from ROCOR's own pages - the roll of
its Hierarchy, its page of sites, and the chancellery page of the British
and Western European diocese. Every one of the eight diocesan sites was
requested and every one answered as itself. The register of the Moscow
Patriarchate, which is the Church above this one, keeps a page for each
diocese and those pages stay cited beside ROCOR's own.

Three rows had no address and have one now: Canada and South America from
the roll of the Hierarchy, Great Britain and Western Europe from its own
chancellery. The roll prints a hierarch's name above two of those streets
and the row carries the street alone, as every row here does.

The Western American diocese answers at wadiocese.com. ROCOR's page of
sites prints wadiocese.org, which answers at its root and 404s at the path
printed; the row keeps the address that answers whole.
"""

READ = "2026-09-14"

HIER = "https://www.synod.com/synod/engrocor/enbishops.html"
LINKS = "https://www.synod.com/synod/engrocor/enlinks.html"
CHANCELLERY = "https://orthodox-europe.org/english/diocese/chancellery/"
MISSION = "https://missionrocor.ru/contacts"

ROWS = [
 dict(id="ru-eastern-america-rocor", parent="rocor",
      name="Diocese of Eastern America (ROCOR)",
      rank="Diocese",
      local=u"Восточно-Американская епархия (РПЦЗ)",
      seat="New York", country="US",
      address=[u"Eastern American Diocese, 210 Alexander Avenue, Howell, NJ 07731 USA"],
      site="https://eadiocese.org/",
      sources=["https://patriarchia.ru/org/608", HIER, LINKS]),

 dict(id="ru-mid-america-rocor", parent="rocor",
      name="Diocese of Mid-America (ROCOR)",
      rank="Diocese",
      local=u"Средне-Американская епархия (РПЦЗ)",
      seat="Des Plaines", country="US",
      address=[u"Diocese of Chicago & Detroit, ROCOR, P.O. Box 1367, Des Plaines, IL 60017"],
      site="https://chicagodiocese.org/",
      sources=["https://patriarchia.ru/org/600", HIER, LINKS]),

 dict(id="ru-western-america-rocor", parent="rocor",
      name="Diocese of Western America (ROCOR)",
      rank="Diocese",
      local=u"Западно-Американская епархия (РПЦЗ)",
      seat="San Francisco", country="US",
      address=[u"598 15th Avenue, San Francisco, CA 94118"],
      site="https://www.wadiocese.com/",
      sources=["https://patriarchia.ru/org/592", HIER, LINKS]),

 dict(id="ru-canada-rocor", parent="rocor",
      name="Diocese of Canada (ROCOR)",
      rank="Diocese",
      local=u"Канадская епархия (РПЦЗ)",
      seat="Montreal", country="CA",
      address=[u"425 Edouard Charles Avenue", u"Outremont, QC H2V 2N3"],
      site="http://mcdiocese.com/",
      sources=[HIER, LINKS, "https://patriarchia.ru/org/601"]),

 dict(id="ru-south-america-rocor", parent="rocor",
      name="Diocese of South America (ROCOR)",
      rank="Diocese",
      local=u"Южно-Американская епархия (РПЦЗ)",
      seat="Buenos Aires", country="AR",
      address=[u"Nunez 3541", u"1430 Buenos Aires"],
      site="https://iglesiarusa.info/",
      sources=[HIER, LINKS, "https://patriarchia.ru/org/594"]),

 dict(id="ru-great-britain-and-western-europe-rocor", parent="rocor",
      name="Diocese of Great Britain and Western Europe (ROCOR)",
      rank="Diocese",
      local=u"Великобританская и Западно-Европейская епархия (РПЦЗ)",
      seat="London", country="GB",
      address=[u"483 Green Lanes", u"London, N13 4BS"],
      site="https://orthodox-europe.org/",
      sources=[CHANCELLERY, LINKS, "https://patriarchia.ru/org/626"]),

 dict(id="ru-germany-rocor", parent="rocor",
      name="Diocese of Germany (ROCOR)",
      rank="Diocese",
      local=u"Германская епархия (РПЦЗ)",
      seat="Munich", country="DE",
      address=[u"Hofbauernstr. 26, 81247 München"],
      site="https://rocor.de/",
      sources=["https://patriarchia.ru/org/619", HIER, LINKS]),

 dict(id="ru-australia-and-new-zealand-rocor", parent="rocor",
      name="Diocese of Australia and New Zealand (ROCOR)",
      rank="Diocese",
      local=u"Австралийско-Новозеландская епархия (РПЦЗ)",
      seat="Sydney", country="AU",
      address=[u"20 Chelmsford Avenue, Croydon NSW 2132, Australia"],
      site="http://rocor.org.au/",
      sources=["https://patriarchia.ru/org/602", HIER, LINKS]),

 # Not a diocese. ROCOR names it beside them on all three of its own lists,
 # it prints its own street, and its own site answers in Russian and
 # English.
 dict(id="ru-jerusalem-mission-rocor", parent="rocor",
      name="Russian Ecclesiastical Mission in Jerusalem (ROCOR)",
      local=u"Русская Духовная Миссия в Иерусалиме",
      seat="Jerusalem", country="IL",
      address=[u"P.O. Box 20164", u"Jerusalem 91200"],
      site="https://missionrocor.ru/",
      sources=[MISSION, HIER, LINKS]),
]
