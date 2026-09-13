# -*- coding: utf-8 -*-
"""The rows in Ukrainian.

Gathered from what the site already publishes in Ukrainian, where the sees
stand in the titles of the saints: патріарх Константинопольський, патріарх
Московський, архієпископ Александрійський, Антіохійський, Єрусалимський,
єпископ Афінський. The bodies are named as Ukrainian names a local Church,
by the adjective of the land with Православна Церква after it; the Ukrainian
Church and the Church of Ukraine are kept apart the way Ukrainian keeps
them apart, the one by the adjective and the other by the genitive.

Settled by counting the Ukrainian corpus:

  - Константинополь 737, Стамбул 0. The see is Константинополь.
  - Белград 55, Білград 3. The commemoration of the martyrs Hermylus and
    Stratonicus carries the rarer form; the city itself is Белград.
  - Гельсінкі is the site's own, in the life of the Priestmartyr Alexander
    Hotovitzky, and it is also the modern name, so nothing had to be chosen.

Kyiv is Київ here and Киев in the Russian file; neither language is written
with the other's form.

The Church of Finland carries two names in Ukrainian as it does in Russian,
Фінляндська in the official registers and Фінська in ordinary writing about
her. The row is a label, not a letterhead, so Фінська stands here.

Пряшів and Сайоссет are written here for the first time in Ukrainian on
this site; there was nothing to gather. Пряшів is the received Ukrainian
name of the Slovak city, not a rendering of the Slovak one. Словаччини is
likewise unwritten here, and is the standard Ukrainian name of the country;
Словакії would be a Russianism.
"""
NAMES = {
    "constantinople": u"Константинопольська Православна Церква",
    "alexandria": u"Александрійська Православна Церква",
    "antioch": u"Антіохійська Православна Церква",
    "jerusalem": u"Єрусалимська Православна Церква",
    "russia": u"Російська Православна Церква",
    "georgia": u"Грузинська Православна Церква",
    "serbia": u"Сербська Православна Церква",
    "romania": u"Румунська Православна Церква",
    "bulgaria": u"Болгарська Православна Церква",
    "cyprus": u"Кіпрська Православна Церква",
    "greece": u"Елладська Православна Церква",
    "albania": u"Албанська Православна Церква",
    "poland": u"Польська Православна Церква",
    "czech-slovakia": u"Православна Церква Чеських земель і Словаччини",
    "oca": u"Православна Церква в Америці",
    "macedonia": u"Македонська Православна Церква - Охридська Архієпископія",
    "ukraine-uoc": u"Українська Православна Церква",
    "ukraine-ocu": u"Православна Церква України",
    "sinai": u"Синайська Православна Церква",
    "finland": u"Фінська Автономна Православна Церква",
    "japan": u"Японська Православна Церква",
    "estonia-eaok": u"Православна Церква Естонії",
}
SEATS = {
    "Istanbul": u"Константинополь",
    "Alexandria": u"Александрія",
    "Damascus": u"Дамаск",
    "Jerusalem": u"Єрусалим",
    "Moscow": u"Москва",
    "Tbilisi": u"Тбілісі",
    "Belgrade": u"Белград",
    "Bucharest": u"Бухарест",
    "Sofia": u"Софія",
    "Nicosia": u"Нікосія",
    "Athens": u"Афіни",
    "Tirana": u"Тирана",
    "Warsaw": u"Варшава",
    "Prešov": u"Пряшів",
    "Syosset, New York": u"Сайоссет, Нью-Йорк",
    "Skopje": u"Скоп'є",
    "Kyiv": u"Київ",
    "Mount Sinai": u"Гора Синай",
    "Helsinki": u"Гельсінкі",
    "Tokyo": u"Токіо",
    "Tallinn": u"Таллінн",
}
