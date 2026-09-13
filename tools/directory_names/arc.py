# -*- coding: utf-8 -*-
"""The directory's rows in Syriac.

Unvocalized Classical Syriac, as docs/SYRIAC.md settles it, with seyame on
the plural and the Arabic comma the corpus uses. The genitive is the prefixed
ܕ, which does all the work of "of": ܥܕܬܐ ܕܐܘܪܫܠܡ. Three of these rows are
not composed at all but taken whole from what the site already prints -
ܥܕܬܐ ܕܝܘܢ for the Church of Greece, ܥܕܬܐ ܬܪܝܨܬ ܫܘܒܚܐ ܕܒܐܡܪܝܩܐ for the
Orthodox Church in America, and the adjectival ܥܕܬܐ ܣܪܒܝܝܬܐ ܬܪܝܨܬ ܫܘܒܚܐ
pattern that ܥܕܬܐ ܡܩܕܘܢܝܝܬܐ follows.

Syriac's own cities keep their own names and are not transcribed from
English: ܐܢܛܝܘܟܝܐ, ܕܪܡܣܘܩ, ܐܘܪܫܠܡ, ܛܘܪ ܣܝܢܝ. The seat of the Ecumenical
Patriarchate is ܩܘܣܛܢܛܝܢܘܦܘܠܝܣ, which the corpus writes 1,703 times and
which has no Syriac rival.

Two names had to be settled by counting, because the corpus carries more than
one spelling:

  - **Ukraine is ܐܘܩܪܐܝܢܐ**, 173 times, against ܐܘܟܪܝܢܐ 16, ܐܘܟܪܢܝܐ 3 and
    ܐܘܩܪܝܢܐ 2. The country chips print a fifth form that stands nowhere else.
  - **Poland is ܦܘܠܢܝܐ**, 30 to ܦܘܠܘܢܝܐ 27, and it is the form the site's own
    table gives for the country's name rather than for its people.

Ohrid is ܐܘܟܪܝܕ, 28 against a single ܐܘܚܪܝܕ.

Written here because the site has never named them in Syriac, and named so
that nobody later mistakes them for received forms: ܬܝܪܢܐ Tirana, ܣܩܘܦܝܐ
Skopje, ܦܪܫܘܒ Presov, ܛܘܩܝܘ Tokyo, ܬܠܝܢ Tallinn and ܣܝܘܣܛ Syosset, each
ending as the Syriac habit for a transcribed place ends. Of those, ܛܘܩܝܘ and
ܣܝܘܣܛ are the two the audit reports, because the corpus holds nothing they
can be read off; the other four answer to stems it already has.

ܦܝܢܠܢܕܝܐ, ܝܦܢ and ܐܣܛܘܢܝܐ are not new: they are the forms this site already
publishes in its own Syriac table of countries. The audit reports ܕܝܦܢ all
the same, because it reads the proclitic ܕ as part of the word and the corpus
has never had occasion to write that name with it.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Syriac this site publishes and are
taken whole - ܦܛܪܝܪܟܘܬܐ ܬܒܠܝܬܐ, ܦܛܪܝܪܟܘܬܐ ܕܐܠܟܣܢܕܪܝܐ, and the adjectival
ܥܕܬܐ ܪܘܣܝܝܬܐ, ܣܪܒܝܝܬܐ and ܪܘܡܢܝܬܐ ܬܪܝܨܬ ܫܘܒܚܐ of the commemorations.

Bulgaria has no adjectival form anywhere in the corpus, which writes the
country with the prefixed ܕ instead - ܕܒܘܠܓܪܝܐ, 87 times - so both members of
that row take ܕ, as the label does. Ukraine is ܐܘܩܪܐܝܢܐ here, the spelling
this file settled by counting 173 to 16, not the ܐܘܟܪܝܢܐ the commemorations
happen to carry; a row and its label are not written two ways on one page.
ܘܕܟܠܗ ܡܕܢܚܐ follows the ܘܕܟܠܗ ܪܘܣܝܐ of the patriarch of Moscow.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation. Syriac has no received form for it
in anything this site publishes, and one is not invented here.
"""
NAMES = {
    "constantinople": u"ܥܕܬܐ ܕܩܘܣܛܢܛܝܢܘܦܘܠܝܣ",
    "alexandria": u"ܥܕܬܐ ܕܐܠܟܣܢܕܪܝܐ",
    "antioch": u"ܥܕܬܐ ܕܐܢܛܝܘܟܝܐ",
    "jerusalem": u"ܥܕܬܐ ܕܐܘܪܫܠܡ",
    "russia": u"ܥܕܬܐ ܕܪܘܣܝܐ",
    "georgia": u"ܥܕܬܐ ܕܓܘܪܓܝܐ",
    "serbia": u"ܥܕܬܐ ܕܣܪܒܝܐ",
    "romania": u"ܥܕܬܐ ܕܪܘܡܢܝܐ",
    "bulgaria": u"ܥܕܬܐ ܕܒܘܠܓܪܝܐ",
    "cyprus": u"ܥܕܬܐ ܕܩܘܦܪܘܣ",
    "greece": u"ܥܕܬܐ ܕܝܘܢ",
    "albania": u"ܥܕܬܐ ܕܐܠܒܢܝܐ",
    "poland": u"ܥܕܬܐ ܕܦܘܠܢܝܐ",
    "czech-slovakia": u"ܥܕܬܐ ܕܐܬܪ̈ܘܬܐ ܕܟܟܝܐ ܘܣܠܘܒܩܝܐ",
    "oca": u"ܥܕܬܐ ܬܪܝܨܬ ܫܘܒܚܐ ܕܒܐܡܪܝܩܐ",
    "macedonia": u"ܥܕܬܐ ܡܩܕܘܢܝܝܬܐ ܬܪܝܨܬ ܫܘܒܚܐ - ܪܝܫ ܐܦܣܩܘܦܘܬܐ ܕܐܘܟܪܝܕ",
    "ukraine-uoc": u"ܥܕܬܐ ܕܐܘܩܪܐܝܢܐ",
    "ukraine-ocu": u"ܥܕܬܐ ܬܪܝܨܬ ܫܘܒܚܐ ܕܐܘܩܪܐܝܢܐ",
    "sinai": u"ܥܕܬܐ ܕܣܝܢܝ",
    "finland": u"ܥܕܬܐ ܕܦܝܢܠܢܕܝܐ ܕܡܕܒܪܐ ܢܦܫܗ̇",
    "japan": u"ܥܕܬܐ ܕܝܦܢ",
    "estonia-eaok": u"ܥܕܬܐ ܬܪܝܨܬ ܫܘܒܚܐ ܕܐܣܛܘܢܝܐ",
}
SEATS = {
    "Istanbul": u"ܩܘܣܛܢܛܝܢܘܦܘܠܝܣ",
    "Alexandria": u"ܐܠܟܣܢܕܪܝܐ",
    "Damascus": u"ܕܪܡܣܘܩ",
    "Jerusalem": u"ܐܘܪܫܠܡ",
    "Moscow": u"ܡܘܣܩܒܐ",
    "Tbilisi": u"ܬܒܝܠܝܣܝ",
    "Belgrade": u"ܒܠܓܪܕ",
    "Bucharest": u"ܒܘܟܪܣܛ",
    "Sofia": u"ܣܘܦܝܐ",
    "Nicosia": u"ܢܝܩܘܣܝܐ",
    "Athens": u"ܐܬܢܘܣ",
    "Tirana": u"ܬܝܪܢܐ",
    "Warsaw": u"ܘܪܫܘ",
    "Prešov": u"ܦܪܫܘܒ",
    "Syosset, New York": u"ܣܝܘܣܛ، ܢܝܘ ܝܘܪܩ",
    "Skopje": u"ܣܩܘܦܝܐ",
    "Kyiv": u"ܟܝܒ",
    "Mount Sinai": u"ܛܘܪ ܣܝܢܝ",
    "Helsinki": u"ܗܠܣܢܩܝ",
    "Tokyo": u"ܛܘܩܝܘ",
    "Tallinn": u"ܬܠܝܢ",
}
STYLED = {
    "constantinople": u"ܦܛܪܝܪܟܘܬܐ ܬܒܠܝܬܐ",
    "alexandria": u"ܦܛܪܝܪܟܘܬܐ ܕܐܠܟܣܢܕܪܝܐ",
    "antioch": u"ܦܛܪܝܪܟܘܬܐ ܕܐܢܛܝܘܟܝܐ ܘܕܟܠܗ ܡܕܢܚܐ",
    "jerusalem": u"ܦܛܪܝܪܟܘܬܐ ܕܐܘܪܫܠܡ",
    "russia": u"ܥܕܬܐ ܪܘܣܝܝܬܐ ܬܪܝܨܬ ܫܘܒܚܐ",
    "serbia": u"ܥܕܬܐ ܣܪܒܝܝܬܐ ܬܪܝܨܬ ܫܘܒܚܐ",
    "romania": u"ܥܕܬܐ ܪܘܡܢܝܬܐ ܬܪܝܨܬ ܫܘܒܚܐ",
    "bulgaria": u"ܥܕܬܐ ܬܪܝܨܬ ܫܘܒܚܐ ܕܒܘܠܓܪܝܐ - ܦܛܪܝܪܟܘܬܐ ܕܒܘܠܓܪܝܐ",
    "ukraine-uoc": u"ܥܕܬܐ ܬܪܝܨܬ ܫܘܒܚܐ ܕܐܘܩܪܐܝܢܐ",
}
