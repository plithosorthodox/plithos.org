# -*- coding: utf-8 -*-
"""The directory's rows in Armenian.

Classical orthography throughout, as docs/ARMENIAN.md requires and as the
names table, the lives and the prayers already write - Բուլղարիոյ, Նիւ Եորք,
Աթէնք, Երուսաղէմ. The word order is the one the commemorations keep fifteen
hundred times: the see first, in the genitive, then Եկեղեցի. Ռուսիոյ Եկեղեցի
is not composed here at all; it is what the site already prints for the
Church of Rus'.

Three things had to be settled by counting the corpus.

  - **The genitive of a name in -իա is the classical -ոյ.** Ռուսիոյ 531 to 4,
    Սերբիոյ 93 to 38, Բուլղարիոյ 36 to 30, Աղեքսանդրիոյ 136 to 130; the whole
    class stands 816 to 222. The Alexandria pair is nearly even and follows
    the class rather than its own narrow margin.
  - **Romania is Ռումինիա, not Ռումանիա** - 59 to 3 across the corpus. The
    country chips print Ռումանիա; the calendar and the lives do not, and they
    are the larger body.
  - **Ohrid is Օհրիդ**, 22 against a single Օխրիդ.

Two entries are the received form of the city rather than the modern one, and
both follow the site's own usage: the seat of the Ecumenical Patriarchate is
Կոստանդնուպոլիս, which the corpus writes 292 times in the nominative and
Ստամբուլ never; and the mountain is Սինա լեռ, which is how the site names it.

Written here because the site has never named them in Armenian, and named so
that nobody later mistakes them for received forms: Պրեշով Presov, Սիոսեթ
Syosset, Տոկիո Tokyo and Տալլին Tallinn. Those four are what the audit
reports, and the report is right. Տիրանա and Սկոպիե are new here too but
answer to stems the corpus already holds; Ֆինլանդիա, Ճապոնիա, Էստոնիա and
Սլովակիա are not new at all, being the forms the site already publishes in
its own Armenian table of countries.

The classical geminate is kept in Տալլին, which is how Armenian prints the
city, rather than the single-l spelling that would have answered to a stem
already here. A coincidence is not an attestation and is not taken as one.
"""
NAMES = {
    "constantinople": u"Կոստանդնուպոլսի Եկեղեցի",
    "alexandria": u"Աղեքսանդրիոյ Եկեղեցի",
    "antioch": u"Անտիոքի Եկեղեցի",
    "jerusalem": u"Երուսաղէմի Եկեղեցի",
    "russia": u"Ռուսիոյ Եկեղեցի",
    "georgia": u"Վրաստանի Եկեղեցի",
    "serbia": u"Սերբիոյ Եկեղեցի",
    "romania": u"Ռումինիոյ Եկեղեցի",
    "bulgaria": u"Բուլղարիոյ Եկեղեցի",
    "cyprus": u"Կիպրոսի Եկեղեցի",
    "greece": u"Յունաստանի Եկեղեցի",
    "albania": u"Ալբանիոյ Եկեղեցի",
    "poland": u"Լեհաստանի Եկեղեցի",
    "czech-slovakia": u"Չեխական երկրների եւ Սլովակիոյ Եկեղեցի",
    "oca": u"Ամերիկայի Ուղղափառ Եկեղեցի",
    "macedonia": u"Մակեդոնիոյ Ուղղափառ Եկեղեցի - Օհրիդի Արքեպիսկոպոսութիւն",
    "ukraine-uoc": u"Ուկրաինայի Եկեղեցի",
    "ukraine-ocu": u"Ուկրաինայի Ուղղափառ Եկեղեցի",
    "sinai": u"Սինայի Եկեղեցի",
    "finland": u"Ֆինլանդիոյ Ինքնավար Եկեղեցի",
    "japan": u"Ճապոնիոյ Եկեղեցի",
    "estonia-eaok": u"Էստոնիոյ Ուղղափառ Եկեղեցի",
}
SEATS = {
    "Istanbul": u"Կոստանդնուպոլիս",
    "Alexandria": u"Աղեքսանդրիա",
    "Damascus": u"Դամասկոս",
    "Jerusalem": u"Երուսաղէմ",
    "Moscow": u"Մոսկուա",
    "Tbilisi": u"Թբիլիսի",
    "Belgrade": u"Բելգրադ",
    "Bucharest": u"Բուխարեստ",
    "Sofia": u"Սոֆիա",
    "Nicosia": u"Նիկոսիա",
    "Athens": u"Աթէնք",
    "Tirana": u"Տիրանա",
    "Warsaw": u"Վարշաւա",
    "Prešov": u"Պրեշով",
    "Syosset, New York": u"Սիոսեթ, Նիւ Եորք",
    "Skopje": u"Սկոպիե",
    "Kyiv": u"Կիեւ",
    "Mount Sinai": u"Սինա լեռ",
    "Helsinki": u"Հելսինկի",
    "Tokyo": u"Տոկիո",
    "Tallinn": u"Տալլին",
}
