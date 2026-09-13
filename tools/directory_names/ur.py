# -*- coding: utf-8 -*-
"""The directory's rows in Urdu.

Perso-Arabic throughout, with the Arabic comma the four published bodies use.
The place comes first in the oblique and the head follows, as docs/URDU.md
settles it: انطاکیہ کا کلیسا, never the English order in Urdu words. کلیسا is
masculine, so the postposition is کا. روس کا کلیسا and امریکہ کا راست دین
کلیسا are taken whole from what the site already prints, and مقدونیائی راست
دین کلیسا follows the جارجیائی راست دین کلیسا pattern it prints beside them.

One name had to be settled by counting: **Macedonia is مقدونیہ**, 20 against
مکدنیہ 15, and it is the form the calendar and the commemorations use where
the vocabulary table alone gives the shorter one.

Constantinople keeps its received form قسطنطنیہ, which the site writes 1,306
times and which no استنبول stands beside; it is the seat the Ecumenical
Patriarchate is known by here. The mountain is کوہ سینا, as the site names it.

Written here because the site has never named them in Urdu, and named so that
nobody later mistakes them for received forms: تیرانا Tirana, سکوپیہ Skopje,
پریشوو Presov, ٹوکیو Tokyo, تالین Tallinn, سیوسٹ Syosset, فن لینڈ Finland,
جاپان Japan and سلوواکیہ Slovakia, the last built on سلوواک, which the site
already writes of the faithful of that land. Three of them - جاپان, ٹوکیو and
سیوسٹ - are what the audit reports, and the report is right: the corpus holds
nothing they can be read off. The rest answer to stems it already has.

سیوسٹ keeps the spelling the name is pronounced by, not the سائیوسٹ that
would have answered to a stem already here. A coincidence is not an
attestation and is not taken as one.

The Archbishopric of Ohrid is سردار اسقفی حلقہ, which is the site's own سردار
اسقف set over its own اسقفی حلقہ.
"""
NAMES = {
    "constantinople": u"قسطنطنیہ کا کلیسا",
    "alexandria": u"اسکندریہ کا کلیسا",
    "antioch": u"انطاکیہ کا کلیسا",
    "jerusalem": u"یروشلم کا کلیسا",
    "russia": u"روس کا کلیسا",
    "georgia": u"جارجیا کا کلیسا",
    "serbia": u"سربیا کا کلیسا",
    "romania": u"رومانیہ کا کلیسا",
    "bulgaria": u"بلغاریہ کا کلیسا",
    "cyprus": u"قبرص کا کلیسا",
    "greece": u"یونان کا کلیسا",
    "albania": u"البانیہ کا کلیسا",
    "poland": u"پولینڈ کا کلیسا",
    "czech-slovakia": u"چیک سرزمین اور سلوواکیہ کا کلیسا",
    "oca": u"امریکہ کا راست دین کلیسا",
    "macedonia": u"مقدونیائی راست دین کلیسا - اوہرد کا سردار اسقفی حلقہ",
    "ukraine-uoc": u"یوکرین کا کلیسا",
    "ukraine-ocu": u"یوکرین کا راست دین کلیسا",
    "sinai": u"سینا کا کلیسا",
    "finland": u"فن لینڈ کا خود اختیار کلیسا",
    "japan": u"جاپان کا کلیسا",
    "estonia-eaok": u"ایستونیا کا راست دین کلیسا",
}
SEATS = {
    "Istanbul": u"قسطنطنیہ",
    "Alexandria": u"اسکندریہ",
    "Damascus": u"دمشق",
    "Jerusalem": u"یروشلم",
    "Moscow": u"ماسکو",
    "Tbilisi": u"تبلیسی",
    "Belgrade": u"بلغراد",
    "Bucharest": u"بخارسٹ",
    "Sofia": u"صوفیہ",
    "Nicosia": u"نکوسیا",
    "Athens": u"ایتھنز",
    "Tirana": u"تیرانا",
    "Warsaw": u"وارسا",
    "Prešov": u"پریشوو",
    "Syosset, New York": u"سیوسٹ، نیو یارک",
    "Skopje": u"سکوپیہ",
    "Kyiv": u"کیف",
    "Mount Sinai": u"کوہ سینا",
    "Helsinki": u"ہیلسنکی",
    "Tokyo": u"ٹوکیو",
    "Tallinn": u"تالین",
}
