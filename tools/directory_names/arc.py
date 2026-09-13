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

Written here because the site has never named them in Syriac: ܬܝܪܢܐ Tirana,
ܣܩܘܦܝܐ Skopje, ܦܪܫܘܒ Presov, ܛܘܩܝܘ Tokyo, ܬܠܝܢ Tallinn and ܣܝܘܣܛ Syosset,
each ending as the Syriac habit for a transcribed place ends. Finland, Japan
and Estonia are the forms the site already publishes in its own Syriac table
of countries.
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
    "czech-slovakia": u"ܥܕܬܐ ܕܐܬܪ̈ܘܬܐ ܕܟܟܝܐ ܘܕܣܠܘܒܩܝܐ",
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
