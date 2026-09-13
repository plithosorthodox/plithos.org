# -*- coding: utf-8 -*-
"""The directory's Churches and their seats, in Swahili.

Every form is read off data/saint-terms.v5.sw.json, the saint names and the
lives, and follows the concord docs/SWAHILI.md sets down: kanisa is class 5,
so the genitive particle is la.

"The Church of X" is the English label of the list the rows were read from,
not a proper name, so it takes the shape this site's Swahili already gives
that phrase: Kanisa la X, from Kanisa la Konstantinopoli, Kanisa la Ugiriki
and Kanisa la Rus. Where the English itself says Orthodox Church the row
takes Kanisa la Kiothodoksi - the site writes Kanisa la Kiothodoksi katika
Amerika for the Orthodox Church in America, and that entry is reproduced
whole - so the two Ukrainian rows keep the distinction the English keeps.

The seats divide the way the site's own Swahili divides them, and the rule
was read off the files rather than chosen: the ancient sees have Swahili
forms and take them - Konstantinopoli, Aleksandria, Antiokia, Yerusalemu,
Damasko, Athene, Nikosia, Bukarest, Mlima Sinai - while the modern cities
stand as the site prints them, unadapted: Moscow, Kyiv, Belgrade, Warsaw,
Tbilisi, Helsinki, New York.

Autonomous is the one word that had to be settled. The glossary gives
Kujitawala for autonomy and Kujitegemea for autocephaly, but the directory
page itself already says Makanisa yenye kujitegemea over the group this row
falls in. A row reading one word under a heading reading another is worse
than either, so Finland follows the heading above it.

Three seats this site has never named stand as they are printed: Tokyo,
Syosset and Prešov, the last keeping its hacek, which the site's Swahili
keeps on foreign names elsewhere.
"""
NAMES = {
    "constantinople": u"Kanisa la Konstantinopoli",
    "alexandria": u"Kanisa la Aleksandria",
    "antioch": u"Kanisa la Antiokia",
    "jerusalem": u"Kanisa la Yerusalemu",
    "russia": u"Kanisa la Urusi",
    "georgia": u"Kanisa la Georgia",
    "serbia": u"Kanisa la Serbia",
    "romania": u"Kanisa la Rumania",
    "bulgaria": u"Kanisa la Bulgaria",
    "cyprus": u"Kanisa la Kipro",
    "greece": u"Kanisa la Ugiriki",
    "albania": u"Kanisa la Albania",
    "poland": u"Kanisa la Polandi",
    "czech-slovakia": u"Kanisa la Nchi za Cheki na Slovakia",
    "oca": u"Kanisa la Kiothodoksi katika Amerika",
    "macedonia": u"Kanisa la Kiothodoksi la Makedonia - Jimbo Kuu la Ohridi",
    "ukraine-uoc": u"Kanisa la Ukraine",
    "ukraine-ocu": u"Kanisa la Kiothodoksi la Ukraine",
    "sinai": u"Kanisa la Sinai",
    "finland": u"Kanisa la Ufini lenye kujitegemea",
    "japan": u"Kanisa la Japani",
    "estonia-eaok": u"Kanisa la Kiothodoksi la Estonia",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Aleksandria",
    "Damascus": u"Damasko",
    "Jerusalem": u"Yerusalemu",
    "Moscow": u"Moscow",
    "Tbilisi": u"Tbilisi",
    "Belgrade": u"Belgrade",
    "Bucharest": u"Bukarest",
    "Sofia": u"Sofia",
    "Nicosia": u"Nikosia",
    "Athens": u"Athene",
    "Tirana": u"Tirana",
    "Warsaw": u"Warsaw",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Kyiv",
    "Mount Sinai": u"Mlima Sinai",
    "Helsinki": u"Helsinki",
    "Tokyo": u"Tokyo",
    "Tallinn": u"Tallinn",
}
