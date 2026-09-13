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

The thirty-nine dioceses of North America and of the Throne's eparchies were
added on the same terms. Diözese is the word the page itself already uses;
Erzdiözese stands beside it for an archdiocese, Erzbistum staying with the
archbishopric of Ohrid it was given. Metropolie is the word the lives use of
a metropolitan see - die Metropolie der Rus, die Metropolie von Smyrna - and
the eparchies take it. Heilige does the work of both Holy and Sacred, German
having one word where the English list has two.

Most of what the rows needed was already written. Nordamerika, Amerikas,
Kalifornien, Kanada, Mexiko, Illinois, Alaska, Pennsylvania, Britannien,
Schweden, Skandinavien, Malta, Thyateira, Wien and Venedig all stand in the
German this site publishes, and San Francisco, Kalifornien stands whole in
the vocabulary beside the lives. Apostel Amerikas is how that German says of
the Americas, so the Albanian diocese and the Romanian metropolia take the
genitive and not a preposition.

Three were settled by reading rather than by choosing. Der Mittlere Westen
is the German the life of the hieromartyr John Kochurov uses of the American
Midwest, and the diocese of that name takes it, with des Südens and des
Westens beside it. Karpatorussische follows the karpatorussischen Einwanderer
of the same life. And Russische Orthodoxe Auslandskirche is not composed at
all: Russische Auslandskirche stands in the glorifications and beside the
Kursk icon, and the Rule page names that Church der Auslandskirche.

Eastern in the Bulgarian diocese's English name is not written. German has no
Ostorthodox and orthodox alone is what it says; the row stays apart from the
Orthodox Church in America's Bulgarische Diözese by the countries it names.

What German spells as English spells it is left alone - London, Madrid,
Seoul, Stockholm, Quebec, Washington, Michigan, Massachusetts, Ohio,
Connecticut, Texas, Portugal. What German does not, and what this site had
never had occasion to write, is written here in the received form: the cities
Brüssel, Hongkong, Mexiko-Stadt and Singapur, the countries Belgien,
Grossbritannien, Österreich, die Schweiz and Australien, and the regions
Neuengland, Südasien and Südostasien. Of those, Grossbritannien, Hongkong,
Südostasien and Australien are the words the audit reports, the rest
answering to a stem the German already has.

Ten eparchies of the Romanian Patriarchate came last, and they take the
words this table already uses, Erzdiözese and Metropolie with von.

The German here had already settled the question these rows ask. German has
a name of its own for Iași, Jassy, and it stands in the Churches' own
commemorations; but what this site publishes in German writes Iași 25 times
against 15 for the bare Iasi and Jassy not once. So Iași, and with it the
rule for the rest: a Romanian city keeps the spelling its own language gives
it, and Hermannstadt, Klausenburg and Temeswar are not written here for
Sibiu, Cluj-Napoca and Timișoara.

Tomis is not Constanța. It is the ancient see the modern city stands on, and
the row carries it while Constanța stands beside it as the seat.

Nürnberg is the city's own name and is not a rendering of anything; Limours
is left as France writes it. Sibiu, Cluj-Napoca, Craiova, Timișoara,
Constanța, Chișinău and Tomis are new here, with Vad and Feleac, which stand
with Cluj in the title of one see and are all three kept.
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
    "ro-bucharest": u"Erzdiözese von Bukarest",
    "ro-chisinau": u"Erzdiözese von Chișinău",
    "ro-craiova": u"Erzdiözese von Craiova",
    "ro-iasi": u"Erzdiözese von Iași",
    "ro-sibiu": u"Erzdiözese von Sibiu",
    "ro-timisoara": u"Erzdiözese von Timișoara",
    "ro-tomis": u"Erzdiözese von Tomis",
    "ro-cluj": u"Erzdiözese von Vad, Feleac und Cluj",
    "ro-western-europe": u"Rumänische Orthodoxe Erzdiözese von Westeuropa",
    "ro-germany": u"Rumänische Orthodoxe Metropolie von Deutschland, Mittel- und Nordeuropa",
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
    "Chisinau": u"Chișinău",
    "Cluj-Napoca": u"Cluj-Napoca",
    "Constanta": u"Constanța",
    "Craiova": u"Craiova",
    "Jassy": u"Iași",
    "Limours": u"Limours",
    "Nuremberg": u"Nürnberg",
    "Sibiu": u"Sibiu",
    "Timisoara": u"Timișoara",
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
