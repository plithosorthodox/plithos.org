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

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Swahili this site publishes and
are taken whole - Upatriaki wa Ulimwengu and the Kanisa la Kiothodoksi la
Urusi, Serbia, Rumania and Ukraine of the commemorations.

Upatriaki is the site's own word for a patriarchate against Patriaki for the
man, and the three ancient sees take it with wa, as Upatriaki wa Antiokia
already does. Upatriaki wa Antiokia na Mashariki Yote follows the Patriaki wa
Moscow na Urusi Yote of the calendar.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Swahili name for either body
carries it, so it is not written here.

The thirty-nine dioceses came afterwards, and the seats follow the rule
already set down here: the modern cities stand as the site prints them, so
Boston, Massachusetts and Rawdon, Quebec and London and Stockholm are left
alone, and only Venice, which the vocabulary writes Venezia, is turned.

Dayosisi is the word for a diocese, 79 times and the word the directory's own
heading uses; Jimbo Kuu, which already carries the Ohrid Archbishopric,
carries the archdioceses; Mitropolia, built on the glossary's mitropoliti,
carries the metropolises, since a metropolis and an archdiocese are different
things in the list and one word for both would lose that. Uaskofu takes the
Romanian Episcopate and Parokia za Kipatriaki the patriarchal parishes,
kipatriaki being the site's own word, as in shule ya kipatriaki. The
jurisdiction table supplied the adjectives whole - kiromania, kiukreni,
kibulgaria, kiserbia, kigiriki - so the Romanian, Ukrainian and Bulgarian
rows stay apart from the Churches of the same names, and Kialbania is formed
beside them for the two Albanian rows.

Amerika ya Kaskazini, Marekani, Kanada, Alaska, Sitka and Karpato-Urusi are
the vocabulary's own. Kusini, Magharibi and Magharibi ya Kati name the three
American regions. One word had to be written: Ubelgiji, which is the Swahili
for Belgium, and which these pages have never had occasion to say.
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
    "albanian-americas": u"Dayosisi ya Kiothodoksi ya Kialbania ya Amerika",
    "acrod": u"Dayosisi ya Kiothodoksi ya Kiamerika ya Karpato-Urusi katika Amerika ya Kaskazini",
    "ep-thyateira": u"Jimbo Kuu la Thiatira na Britania Kuu",
    "goarch": u"Jimbo Kuu la Kiothodoksi la Kigiriki la Amerika",
    "ep-france": u"Mitropolia ya Kiothodoksi ya Kigiriki ya Ufaransa",
    "ep-germany": u"Mitropolia ya Kiothodoksi ya Kigiriki ya Ujerumani",
    "ep-austria": u"Mitropolia Takatifu ya Austria",
    "ep-korea": u"Mitropolia Takatifu ya Korea",
    "ep-spain": u"Mitropolia Takatifu ya Hispania na Ureno",
    "ep-belgium": u"Mitropolia ya Ubelgiji",
    "ep-sweden": u"Mitropolia ya Uswidi na Skandinavia Yote",
    "ep-switzerland": u"Mitropolia ya Uswisi",
    "ep-hongkong": u"Mitropolia ya Kiothodoksi ya Hong Kong na Asia ya Kusini-Mashariki",
    "ep-singapore": u"Mitropolia ya Kiothodoksi ya Singapore na Asia ya Kusini",
    "ep-italy": u"Jimbo Kuu Takatifu la Kiothodoksi la Italia na Malta",
    "uocc": u"Kanisa la Kiothodoksi la Kiukreni la Kanada",
    "uoc-usa": u"Kanisa la Kiothodoksi la Kiukreni la Marekani",
    "antiochian-na": u"Jimbo Kuu la Kikristo la Kiothodoksi la Antiokia la Amerika ya Kaskazini",
    "rocor": u"Kanisa la Kiothodoksi la Urusi Nje ya Urusi",
    "mp-parishes-usa": u"Parokia za Kipatriaki katika Marekani",
    "serbian-eastern": u"Dayosisi ya Amerika ya Mashariki",
    "serbian-midwestern": u"Dayosisi ya Gracanica Mpya na Amerika ya Magharibi ya Kati",
    "serbian-western": u"Dayosisi ya Amerika ya Magharibi",
    "romanian-americas": u"Mitropolia ya Kiothodoksi ya Kiromania ya Amerika",
    "bulgarian-usa": u"Dayosisi ya Kiothodoksi ya Mashariki ya Kibulgaria ya Marekani, Kanada na Australia",
    "oca-albanian": u"Jimbo Kuu la Kialbania",
    "oca-canada": u"Jimbo Kuu la Kanada",
    "oca-washington": u"Jimbo Kuu la Washington, D.C.",
    "oca-western-pa": u"Jimbo Kuu la Pennsylvania ya Magharibi",
    "oca-bulgarian": u"Dayosisi ya Kibulgaria",
    "oca-eastern-pa": u"Dayosisi ya Pennsylvania ya Mashariki",
    "oca-mexico": u"Dayosisi ya Mexico",
    "oca-new-england": u"Dayosisi ya New England",
    "oca-ny-nj": u"Dayosisi ya New York na New Jersey",
    "oca-alaska": u"Dayosisi ya Sitka na Alaska",
    "oca-midwest": u"Dayosisi ya Magharibi ya Kati",
    "oca-south": u"Dayosisi ya Kusini",
    "oca-west": u"Dayosisi ya Magharibi",
    "oca-romanian": u"Uaskofu wa Kiromania",
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
    "Alexandria, Virginia": u"Alexandria, Virginia",
    "Alhambra, California": u"Alhambra, California",
    "Anchorage, Alaska": u"Anchorage, Alaska",
    "Bath, Pennsylvania": u"Bath, Pennsylvania",
    "Bonn": u"Bonn",
    "Boston, Massachusetts": u"Boston, Massachusetts",
    "Bronxville, New York": u"Bronxville, New York",
    "Brussels": u"Brussels",
    "Chambesy": u"Chambesy",
    "Chicago, Illinois": u"Chicago, Illinois",
    "Cranberry Township, Pennsylvania": u"Cranberry Township, Pennsylvania",
    "Dallas, Texas": u"Dallas, Texas",
    "Englewood, New Jersey": u"Englewood, New Jersey",
    "Hong Kong": u"Hong Kong",
    "Jackson, Michigan": u"Jackson, Michigan",
    "Johnstown, Pennsylvania": u"Johnstown, Pennsylvania",
    "London": u"London",
    "Madrid": u"Madrid",
    "Mexico City": u"Mexico City",
    "New Rochelle, New York": u"New Rochelle, New York",
    "New York": u"New York",
    "Paris": u"Paris",
    "Rawdon, Quebec": u"Rawdon, Quebec",
    "San Francisco, California": u"San Francisco, California",
    "Seoul": u"Seoul",
    "Singapore": u"Singapore",
    "Somerset, New Jersey": u"Somerset, New Jersey",
    "Stockholm": u"Stockholm",
    "Third Lake, Illinois": u"Third Lake, Illinois",
    "Toledo, Ohio": u"Toledo, Ohio",
    "Venice": u"Venezia",
    "Vienna": u"Vienna",
    "Windsor, Connecticut": u"Windsor, Connecticut",
    "Winnipeg, Manitoba": u"Winnipeg, Manitoba",
}
STYLED = {
    "constantinople": u"Upatriaki wa Ulimwengu",
    "alexandria": u"Upatriaki wa Aleksandria",
    "antioch": u"Upatriaki wa Antiokia na Mashariki Yote",
    "jerusalem": u"Upatriaki wa Yerusalemu",
    "russia": u"Kanisa la Kiothodoksi la Urusi",
    "serbia": u"Kanisa la Kiothodoksi la Serbia",
    "romania": u"Kanisa la Kiothodoksi la Rumania",
    "bulgaria": u"Kanisa la Kiothodoksi la Bulgaria - Upatriaki wa Bulgaria",
    "ukraine-uoc": u"Kanisa la Kiothodoksi la Ukraine",
}
