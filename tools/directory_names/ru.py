# -*- coding: utf-8 -*-
"""The rows in Russian.

Gathered from what the site already publishes in Russian, where the sees
stand in the titles of the saints themselves: патриарх Константинопольский,
патриарх Московский, архиепископ Александрийский, Антиохийский,
Иерусалимский. The bodies are named as Russian names a local Church, by the
adjective of the land with Православная Церковь after it; the two whose
standing is disputed are named the way Russian itself keeps them apart, the
Ukrainian Church by the adjective and the Church of Ukraine by the genitive.

Settled by counting the Russian corpus:

  - Константинополь 2096, Стамбул 0. The site has never once written the
    Turkish name, and the see is Константинополь.
  - Тбилиси 32, Тифлис 16. The modern name wins on its own numbers.
  - Хельсинки is the exception where the count was not followed. The Russian
    here writes Гельсингфорс, seven times, all of them inside the life of
    the Priestmartyr Alexander Hotovitzky, where the year is 1917 and the
    imperial name is the right one; the Serbian and Ukrainian of that same
    sentence write Хелсинки and Гельсінкі. The seat of a Church living today
    is Хельсинки.

The Church of Finland carries two Russian names and both are in use,
Финляндская in the official registers and Финская in ordinary Russian
writing about her. The row is a label, not a letterhead, so Финская stands
here.

Прешов and Сайоссет are written here for the first time in Russian on this
site; there was nothing to gather. Both are the received Russian forms,
Сайоссет the one the Russian reference works give for the chancery on Long
Island, not a transliteration made up for the occasion.
"""
NAMES = {
    "constantinople": u"Константинопольская Православная Церковь",
    "alexandria": u"Александрийская Православная Церковь",
    "antioch": u"Антиохийская Православная Церковь",
    "jerusalem": u"Иерусалимская Православная Церковь",
    "russia": u"Русская Православная Церковь",
    "georgia": u"Грузинская Православная Церковь",
    "serbia": u"Сербская Православная Церковь",
    "romania": u"Румынская Православная Церковь",
    "bulgaria": u"Болгарская Православная Церковь",
    "cyprus": u"Кипрская Православная Церковь",
    "greece": u"Элладская Православная Церковь",
    "albania": u"Албанская Православная Церковь",
    "poland": u"Польская Православная Церковь",
    "czech-slovakia": u"Православная Церковь Чешских земель и Словакии",
    "oca": u"Православная Церковь в Америке",
    "macedonia": u"Македонская Православная Церковь - Охридская Архиепископия",
    "ukraine-uoc": u"Украинская Православная Церковь",
    "ukraine-ocu": u"Православная Церковь Украины",
    "sinai": u"Синайская Православная Церковь",
    "finland": u"Финская Автономная Православная Церковь",
    "japan": u"Японская Православная Церковь",
    "estonia-eaok": u"Православная Церковь Эстонии",
}
SEATS = {
    "Istanbul": u"Константинополь",
    "Alexandria": u"Александрия",
    "Damascus": u"Дамаск",
    "Jerusalem": u"Иерусалим",
    "Moscow": u"Москва",
    "Tbilisi": u"Тбилиси",
    "Belgrade": u"Белград",
    "Bucharest": u"Бухарест",
    "Sofia": u"София",
    "Nicosia": u"Никосия",
    "Athens": u"Афины",
    "Tirana": u"Тирана",
    "Warsaw": u"Варшава",
    "Prešov": u"Прешов",
    "Syosset, New York": u"Сайоссет, Нью-Йорк",
    "Skopje": u"Скопье",
    "Kyiv": u"Киев",
    "Mount Sinai": u"Гора Синай",
    "Helsinki": u"Хельсинки",
    "Tokyo": u"Токио",
    "Tallinn": u"Таллин",
}
