# -*- coding: utf-8 -*-
"""الكنائس وكراسيها - the Churches and their seats, in Arabic.

The Antiochian register, as docs/ARABIC.md settles it. Nothing here was
rendered afresh: every see, country and city was read off the Arabic this
site already publishes - the place vocabulary beside the lives, the
calendar entries and the saints' names - so القسطنطينية, الإسكندرية,
أنطاكية, أورشليم, دمشق, موسكو, أثينا, وارسو, بوخارست, صوفيا and نيقوسيا
are the forms already printed, not new ones.

Five forms had to be settled by counting, because the site prints two:

  - **أورشليم**, not القدس: 279 against 229, and the place vocabulary
    renders Jerusalem as أورشليم.
  - **بولندة**, not بولندا: 8 against 3, and the place vocabulary writes
    بولندة.
  - **أوهريد**, not أوخريد: 6 against 5, and the place vocabulary writes
    أوهريد.
  - **تبليسي**, not تفليس: 8 against 2.
  - **جبل سيناء**, not طور سيناء: 5 against 1.

Two more were settled by reading the counts by sense rather than by total.
America stands at أميركا 114 against أمريكا 62 in general, but the body
named in this row is written الكنيسة الأرثوذكسية في أمريكا 51 times against
18, so that row keeps أمريكا and the rest of the site keeps أميركا. And
مكدونية, the commoner of the two Macedonias here at 23 against 19, is in
every instance the ancient province St Paul crossed; the modern country is
مقدونيا, which the vocabulary writes as مقدونيا الشمالية, so the Church of
this row is المقدونية.

The place vocabulary gives Belgrade as بيلوزيرسك, which is Belozersk; the
corpus writes بلغراد 23 times and that is what stands here.

What the Arabic pages have never had occasion to say is written here in the
received Arabic form. Seven cities: إسطنبول, تيرانا, بريشوف, سكوبيه, سيوسيت,
طوكيو and تالين. And three countries: سلوفاكيا, فنلندا and اليابان. Two of
those peoples the site does name - the lives write السلوفاك and الفنلنديين -
but never the countries, and Japan it has not named at all.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Arabic this site publishes and are
taken whole - البطريركية المسكونية and the الكنيسة الأرثوذكسية الروسية,
الصربية, الرومانية and الأوكرانية of the commemorations.

Antioch and Jerusalem are the two rows where the English word Greek means the
Rum rite and communion and not the Greek nation, and Arabic has the received
form for it. This site already prints it: the thanksgiving prayer after the
reading is credited to رعية طرابلس للروم الأرثوذكس. So the two read
بطريركية أنطاكية وسائر المشرق للروم الأرثوذكس and
بطريركية أورشليم للروم الأرثوذكس, which is the Antiochian register the rest
of this site's Arabic is written in, and not a rendering of the English.
"""
NAMES = {
    "constantinople": u"كنيسة القسطنطينية",
    "alexandria": u"كنيسة الإسكندرية",
    "antioch": u"كنيسة أنطاكية",
    "jerusalem": u"كنيسة أورشليم",
    "russia": u"كنيسة روسيا",
    "georgia": u"كنيسة جورجيا",
    "serbia": u"كنيسة صربيا",
    "romania": u"كنيسة رومانيا",
    "bulgaria": u"كنيسة بلغاريا",
    "cyprus": u"كنيسة قبرص",
    "greece": u"كنيسة اليونان",
    "albania": u"كنيسة ألبانيا",
    "poland": u"كنيسة بولندة",
    "czech-slovakia": u"كنيسة الأراضي التشيكية وسلوفاكيا",
    "oca": u"الكنيسة الأرثوذكسية في أمريكا",
    "macedonia": u"الكنيسة الأرثوذكسية المقدونية - رئاسة أساقفة أوهريد",
    "ukraine-uoc": u"كنيسة أوكرانيا",
    "ukraine-ocu": u"كنيسة أوكرانيا الأرثوذكسية",
    "sinai": u"كنيسة سيناء",
    "finland": u"كنيسة فنلندا ذات الحكم الذاتي",
    "japan": u"كنيسة اليابان",
    "estonia-eaok": u"كنيسة إستونيا الأرثوذكسية",
}
SEATS = {
    "Istanbul": u"إسطنبول",
    "Alexandria": u"الإسكندرية",
    "Damascus": u"دمشق",
    "Jerusalem": u"أورشليم",
    "Moscow": u"موسكو",
    "Tbilisi": u"تبليسي",
    "Belgrade": u"بلغراد",
    "Bucharest": u"بوخارست",
    "Sofia": u"صوفيا",
    "Nicosia": u"نيقوسيا",
    "Athens": u"أثينا",
    "Tirana": u"تيرانا",
    "Warsaw": u"وارسو",
    "Prešov": u"بريشوف",
    "Syosset, New York": u"سيوسيت، نيويورك",
    "Skopje": u"سكوبيه",
    "Kyiv": u"كييف",
    "Mount Sinai": u"جبل سيناء",
    "Helsinki": u"هلسنكي",
    "Tokyo": u"طوكيو",
    "Tallinn": u"تالين",
}
STYLED = {
    "constantinople": u"البطريركية المسكونية",
    "alexandria": u"بطريركية الإسكندرية",
    "antioch": u"بطريركية أنطاكية وسائر المشرق للروم الأرثوذكس",
    "jerusalem": u"بطريركية أورشليم للروم الأرثوذكس",
    "russia": u"الكنيسة الأرثوذكسية الروسية",
    "serbia": u"الكنيسة الأرثوذكسية الصربية",
    "romania": u"الكنيسة الأرثوذكسية الرومانية",
    "bulgaria": u"الكنيسة الأرثوذكسية البلغارية - البطريركية البلغارية",
    "ukraine-uoc": u"الكنيسة الأرثوذكسية الأوكرانية",
}
