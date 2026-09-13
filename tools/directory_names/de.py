# -*- coding: utf-8 -*-
"""The directory's rows in German.

Read off what the site already publishes in German rather than composed.
The shape of a row is the one the calendar's own canonization lines use -
Kirche von Griechenland, Kirche der Rus, Orthodoxe Kirche in Amerika - so
the row keeps the article German gives a named Church and takes von before
a country that stands without one and the genitive before a country that
does not: von Russland, von Zypern, but der Ukraine, der Slowakei, vom
Sinai.

Two forms competed and were counted across everything this site publishes
in German:

  Tiflis against Tbilisi, for the seat of the Church of Georgia. Tiflis
  stands ten times in the German and Tbilisi only where the English name
  is quoted beside it; Tiflis.

  Makedonisch against Mazedonisch, for the Church whose archbishopric sits
  at Ohrid. The German here writes Makedonien eighteen times, Makedonia,
  Makedonier and Grossmakedonien besides, and Mazedonien not once; so
  Makedonische Orthodoxe Kirche.

Böhmische Länder is the site's own German for the Czech Lands, taken from
the vocabulary beside the saints' cards rather than rendered again here.

Five seats had never been named in German here and are written new:
Istanbul, Tirana, Skopje, Tallinn and Tokio, each in the form German usage
has received, and Prešov, which German writes as Slovak writes it.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the German this site publishes and are
taken whole - Ökumenisches Patriarchat and the Russische, Serbische,
Rumänische and Ukrainische Orthodoxe Kirche of the commemorations.

The three ancient sees follow the Patriarchat von Antiochien the calendar
already writes, and und dem ganzen Osten follows the und ganz Russland of the
patriarch of Moscow.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no German name for either body
carries it, so it is not written here.

The thirty-nine dioceses were added on the same terms. The word for a
diocese is the page's own - Diözesen - and Erzdiözese stands beside it for
an archdiocese, keeping Erzbistum for the archbishopric of Ohrid it was
already given. Heilige does the work of both Holy and Sacred, German having
one word where the English list has two.

Almost all of it was already written here. Nordamerika, Kalifornien,
Pennsylvania, Alaska, Kanada, Mexiko, Neuengland, Illinois, Michigan and
Washington stand in the vocabulary beside the lives; San Francisco,
Kalifornien is in it whole. So is Amerikas for the Americas - Apostel
Amerikas, which is how this site's German says it, so the Albanian diocese
and the Romanian metropolia take the genitive rather than a preposition.
Der Mittlere Westen is the German the lives already use of the American
Midwest, in the life of the hieromartyr John Kochurov, and the diocese takes
it; des Südens and des Westens follow. Karpatorussische is the adjective the
same life uses of the Carpatho-Russian immigrants.

Russische Orthodoxe Auslandskirche is not composed either: Russische
Auslandskirche stands four times in the German already, in the
glorifications and beside the Kursk icon, and the Rule page names the Church
the same way.

Eastern in the Bulgarian diocese's English name is not written. German has
no Ostorthodox, and orthodox alone is what it says; the row stays apart from
the Orthodox Church in America's Bulgarische Diözese by the countries it
names.

Five words had never been written in German here and are written new, all of
them places: Grossbritannien, Hongkong, Südostasien, Australiens and
Mexiko-Stadt, of which only the last is built from words the site already
has. Seoul, London, Madrid, Quebec, Massachusetts, Ohio, Connecticut and
Texas are spelled in German as they are in English and are left alone.
"""
NAMES = {
    "constantinople": u"Die Kirche von Konstantinopel",
    "alexandria": u"Die Kirche von Alexandria",
    "antioch": u"Die Kirche von Antiochien",
    "jerusalem": u"Die Kirche von Jerusalem",
    "russia": u"Die Kirche von Russland",
    "georgia": u"Die Kirche von Georgien",
    "serbia": u"Die Kirche von Serbien",
    "romania": u"Die Kirche von Rumänien",
    "bulgaria": u"Die Kirche von Bulgarien",
    "cyprus": u"Die Kirche von Zypern",
    "greece": u"Die Kirche von Griechenland",
    "albania": u"Die Kirche von Albanien",
    "poland": u"Die Kirche von Polen",
    "czech-slovakia": u"Die Kirche der Böhmischen Länder und der Slowakei",
    "oca": u"Die Orthodoxe Kirche in Amerika",
    "macedonia": u"Die Makedonische Orthodoxe Kirche - Erzbistum Ohrid",
    "ukraine-uoc": u"Die Kirche der Ukraine",
    "ukraine-ocu": u"Orthodoxe Kirche der Ukraine",
    "sinai": u"Die Kirche vom Sinai",
    "finland": u"Die Autonome Kirche von Finnland",
    "japan": u"Die Kirche von Japan",
    "estonia-eaok": u"Orthodoxe Kirche von Estland",
    "albanian-americas": u"Albanische Orthodoxe Diözese Amerikas",
    "acrod": u"Amerikanische Karpatorussische Orthodoxe Diözese von Nordamerika",
    "ep-thyateira": u"Erzdiözese von Thyateira und Grossbritannien",
    "goarch": u"Griechisch-Orthodoxe Erzdiözese von Amerika",
    "ep-france": u"Griechisch-Orthodoxe Metropolie von Frankreich",
    "ep-germany": u"Griechisch-Orthodoxe Metropolie von Deutschland",
    "ep-austria": u"Heilige Metropolie von Österreich",
    "ep-korea": u"Heilige Metropolie von Korea",
    "ep-spain": u"Heilige Metropolie von Spanien und Portugal",
    "ep-belgium": u"Metropolie von Belgien",
    "ep-sweden": u"Metropolie von Schweden und ganz Skandinavien",
    "ep-switzerland": u"Metropolie der Schweiz",
    "ep-hongkong": u"Orthodoxe Metropolie von Hongkong und Südostasien",
    "ep-singapore": u"Orthodoxe Metropolie von Singapur und Südasien",
    "ep-italy": u"Heilige Orthodoxe Erzdiözese von Italien und Malta",
    "uocc": u"Ukrainische Orthodoxe Kirche von Kanada",
    "uoc-usa": u"Ukrainische Orthodoxe Kirche der USA",
    "antiochian-na": u"Antiochenische Orthodox-Christliche Erzdiözese von Nordamerika",
    "rocor": u"Russische Orthodoxe Auslandskirche",
    "mp-parishes-usa": u"Die Patriarchalen Gemeinden in den USA",
    "serbian-eastern": u"Diözese des östlichen Amerika",
    "serbian-midwestern": u"Diözese von Neu-Gracanica und dem Mittleren Westen Amerikas",
    "serbian-western": u"Diözese des westlichen Amerika",
    "romanian-americas": u"Rumänische Orthodoxe Metropolie Amerikas",
    "bulgarian-usa": u"Bulgarische Orthodoxe Diözese der USA, Kanadas und Australiens",
    "oca-albanian": u"Albanische Erzdiözese",
    "oca-canada": u"Erzdiözese von Kanada",
    "oca-washington": u"Erzdiözese von Washington, D.C.",
    "oca-western-pa": u"Erzdiözese des westlichen Pennsylvania",
    "oca-bulgarian": u"Bulgarische Diözese",
    "oca-eastern-pa": u"Diözese des östlichen Pennsylvania",
    "oca-mexico": u"Diözese von Mexiko",
    "oca-new-england": u"Diözese von Neuengland",
    "oca-ny-nj": u"Diözese von New York und New Jersey",
    "oca-alaska": u"Diözese von Sitka und Alaska",
    "oca-midwest": u"Diözese des Mittleren Westens",
    "oca-south": u"Diözese des Südens",
    "oca-west": u"Diözese des Westens",
    "oca-romanian": u"Rumänisches Episkopat",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Alexandria",
    "Damascus": u"Damaskus",
    "Jerusalem": u"Jerusalem",
    "Moscow": u"Moskau",
    "Tbilisi": u"Tiflis",
    "Belgrade": u"Belgrad",
    "Bucharest": u"Bukarest",
    "Sofia": u"Sofia",
    "Nicosia": u"Nikosia",
    "Athens": u"Athen",
    "Tirana": u"Tirana",
    "Warsaw": u"Warschau",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Kiew",
    "Mount Sinai": u"Berg Sinai",
    "Helsinki": u"Helsinki",
    "Tokyo": u"Tokio",
    "Tallinn": u"Tallinn",
    "Alexandria, Virginia": u"Alexandria, Virginia",
    "Alhambra, California": u"Alhambra, Kalifornien",
    "Anchorage, Alaska": u"Anchorage, Alaska",
    "Bath, Pennsylvania": u"Bath, Pennsylvania",
    "Bonn": u"Bonn",
    "Boston, Massachusetts": u"Boston, Massachusetts",
    "Bronxville, New York": u"Bronxville, New York",
    "Brussels": u"Brüssel",
    "Chambesy": u"Chambesy",
    "Chicago, Illinois": u"Chicago, Illinois",
    "Cranberry Township, Pennsylvania": u"Cranberry Township, Pennsylvania",
    "Dallas, Texas": u"Dallas, Texas",
    "Englewood, New Jersey": u"Englewood, New Jersey",
    "Hong Kong": u"Hongkong",
    "Jackson, Michigan": u"Jackson, Michigan",
    "Johnstown, Pennsylvania": u"Johnstown, Pennsylvania",
    "London": u"London",
    "Madrid": u"Madrid",
    "Mexico City": u"Mexiko-Stadt",
    "New Rochelle, New York": u"New Rochelle, New York",
    "New York": u"New York",
    "Paris": u"Paris",
    "Rawdon, Quebec": u"Rawdon, Quebec",
    "San Francisco, California": u"San Francisco, Kalifornien",
    "Seoul": u"Seoul",
    "Singapore": u"Singapur",
    "Somerset, New Jersey": u"Somerset, New Jersey",
    "Stockholm": u"Stockholm",
    "Third Lake, Illinois": u"Third Lake, Illinois",
    "Toledo, Ohio": u"Toledo, Ohio",
    "Venice": u"Venedig",
    "Vienna": u"Wien",
    "Windsor, Connecticut": u"Windsor, Connecticut",
    "Winnipeg, Manitoba": u"Winnipeg, Manitoba",
}
STYLED = {
    "constantinople": u"Ökumenisches Patriarchat",
    "alexandria": u"Patriarchat von Alexandria",
    "antioch": u"Patriarchat von Antiochien und dem ganzen Osten",
    "jerusalem": u"Patriarchat von Jerusalem",
    "russia": u"Russische Orthodoxe Kirche",
    "serbia": u"Serbische Orthodoxe Kirche",
    "romania": u"Rumänische Orthodoxe Kirche",
    "bulgaria": u"Bulgarische Orthodoxe Kirche - Bulgarisches Patriarchat",
    "ukraine-uoc": u"Ukrainische Orthodoxe Kirche",
}
