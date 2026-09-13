# -*- coding: utf-8 -*-
"""The rows in Serbian.

The Serbian of this site is Cyrillic throughout, and so is this file.

Gathered from what the site already publishes in Serbian, where the sees
stand in the titles of the saints: патријарх цариградски, архиепископ
александријски, антиохијски, патријарх јерусалимски, епископ атински,
архиепископ српски. The bodies are named as Serbian names a local Church,
by the adjective of the land with Православна Црква after it; the Ukrainian
Church and the Church of Ukraine are kept apart by the adjective and the
genitive, as Serbian keeps them apart.

Settled by counting the Serbian corpus:

  - Цариград 1443, Константинопољ 2, Истанбул 0. Serbian has its own name
    for the city and this site uses it on nearly every page.
  - Хелсинки, Тирана, Талин, Београд, Букурешт, Никозија and Варшава are
    all the site's own; none of them had to be chosen.

Токио is written here for the first time in Serbian on this site; there was
nothing to gather. Сајосет has no received Serbian form either, and is set
down by transcription, as Serbian sets down foreign place names.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Serbian this site publishes and
are taken whole - Васељенска Патријаршија and the Руска, Српска, Румунска
and Украјинска Православна Црква of the commemorations.

The ancient sees keep the word order the commemorations keep, the noun first
and the adjective after it in lower case: Патријаршија антиохијска is the
site's own, and Патријаршија александријска and јерусалимска follow it.
Antioch takes the genitive instead, because и целог Истока cannot hang on the
adjective, and that tail follows the и целе Русије of the patriarch of Moscow.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Serbian name for either body
carries it, so it is not written here.

Four rows come out word for word as their labels - Russia, Serbia, Romania
and the Ukrainian Church. Serbian has one name for each of those bodies, and
the page shows it once.
"""
NAMES = {
    "constantinople": u"Цариградска Православна Црква",
    "alexandria": u"Александријска Православна Црква",
    "antioch": u"Антиохијска Православна Црква",
    "jerusalem": u"Јерусалимска Православна Црква",
    "russia": u"Руска Православна Црква",
    "georgia": u"Грузијска Православна Црква",
    "serbia": u"Српска Православна Црква",
    "romania": u"Румунска Православна Црква",
    "bulgaria": u"Бугарска Православна Црква",
    "cyprus": u"Кипарска Православна Црква",
    "greece": u"Грчка Православна Црква",
    "albania": u"Албанска Православна Црква",
    "poland": u"Пољска Православна Црква",
    "czech-slovakia": u"Православна Црква Чешких земаља и Словачке",
    "oca": u"Православна Црква у Америци",
    "macedonia": u"Македонска Православна Црква - Охридска Архиепископија",
    "ukraine-uoc": u"Украјинска Православна Црква",
    "ukraine-ocu": u"Православна Црква Украјине",
    "sinai": u"Синајска Православна Црква",
    "finland": u"Финска Аутономна Православна Црква",
    "japan": u"Јапанска Православна Црква",
    "estonia-eaok": u"Православна Црква Естоније",
}
SEATS = {
    "Istanbul": u"Цариград",
    "Alexandria": u"Александрија",
    "Damascus": u"Дамаск",
    "Jerusalem": u"Јерусалим",
    "Moscow": u"Москва",
    "Tbilisi": u"Тбилиси",
    "Belgrade": u"Београд",
    "Bucharest": u"Букурешт",
    "Sofia": u"Софија",
    "Nicosia": u"Никозија",
    "Athens": u"Атина",
    "Tirana": u"Тирана",
    "Warsaw": u"Варшава",
    "Prešov": u"Прешов",
    "Syosset, New York": u"Сајосет, Њујорк",
    "Skopje": u"Скопље",
    "Kyiv": u"Кијев",
    "Mount Sinai": u"Гора Синај",
    "Helsinki": u"Хелсинки",
    "Tokyo": u"Токио",
    "Tallinn": u"Талин",
}
STYLED = {
    "constantinople": u"Васељенска Патријаршија",
    "alexandria": u"Патријаршија александријска",
    "antioch": u"Патријаршија Антиохије и целог Истока",
    "jerusalem": u"Патријаршија јерусалимска",
    "russia": u"Руска Православна Црква",
    "serbia": u"Српска Православна Црква",
    "romania": u"Румунска Православна Црква",
    "bulgaria": u"Бугарска Православна Црква - Бугарска Патријаршија",
    "ukraine-uoc": u"Украјинска Православна Црква",
}
