# -*- coding: utf-8 -*-
"""Le Chiese e le loro sedi, in italiano.

Nothing here was rendered afresh. Every country, city and see was read off
the Italian this site already publishes - the place vocabulary beside the
lives, the calendar entries and the saints' names - and the form that
stands is the form already printed: Costantinopoli, Alessandria,
Antiochia, Gerusalemme, Mosca, Atene, Damasco, Belgrado, Bucarest,
Varsavia, Terre ceche.

Two forms had to be settled by counting, because two were available:

  - **Kyiv**, not Kiev: 1,090 against 3 across the Italian corpus, which is
    docs/ITALIAN.md's rule ("Ukrainian places take their Ukrainian form")
    already carried out.
  - **Ocrida**, not Ohrid: 13 against 2, and the place vocabulary renders
    Ohrid as Ocrida outright.

The name of a local Church takes the article and the bare preposition the
site already uses - Chiesa di Costantinopoli, Chiesa di Georgia, Chiesa di
Grecia, Chiesa di Cipro, Chiesa di Ucraina - except where Italian will not
drop the article at all, so the Sinai and the Giappone keep theirs. Chiesa
ortodossa in America is the site's own wording, written twenty-three times.

What the Italian pages have never had occasion to say is written here for
the first time, in the received Italian form. Seven cities: Istanbul,
Tirana, Prešov, Syosset, Skopje, Tallinn and Tokyo - all but two spelled as
English spells them, which is what Italian does with them. And three
countries: Estonia, Finlandia and Giappone. The site knows two of those
peoples - the lives write gli estoni and i finlandesi - but has never named
the countries, and Japan it has not named at all. Slovacchia follows i
fedeli slovacchi, which the calendar already says of Saint Gorazd's flock;
Arcivescovado follows arcivescovo, which stands 379 times.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Italian this site publishes and
are taken whole - Patriarcato ecumenico and the Chiesa ortodossa russa,
serba, romena and ucraina of the commemorations.

The three ancient sees follow the Patriarcato di Antiochia the calendar
writes, and e di tutto l'Oriente follows the e di tutta la Russia of the
patriarch of Moscow. The lower case of ortodossa and ecumenico is the site's
own Italian and is kept; Oriente is a place and keeps its capital.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Italian name for either body
carries it, so it is not written here.

The thirty-nine dioceses were added on the same terms. Arcidiocesi is the
word for an archdiocese and Arcivescovado is kept for the archbishopric of
Ocrida it was already given. Metropolia is the word the lives use of a
metropolitan see, of Smirne and of the Rus, and the Throne's eparchies take
it; metropolitanato, which the life of the metropolitan Constantine uses of
the see itself, is what the two Metropolitanates of Asia are called. Sacra
carries both Holy and Sacred, and the Archdiocese of Italy is called what it
calls itself, Sacra Arcidiocesi ortodossa d'Italia e Malta.

Nearly every seat was already written. The vocabulary beside the lives has
Parigi, Venezia, California, Pennsylvania, Alaska, Illinois, Michigan, New
York, America del Nord and le Americhe, and San Francisco, California
whole - Italian leaves the American states as they are spelled, and the
lexicon does. Il Midwest
is the Italian the life of the hieromartyr John Kochurov uses of the
American Midwest, and the diocese takes it; del Sud and dell'Ovest follow.
Carpatorussa follows the carpatorussi of the vocabulary, which the lives
also write carpato-russi; the two stand twice each and the unhyphenated one
is taken, being the form a title wants.

Chiesa ortodossa russa all'estero is taken from the Rule page, which names
that Church russa all'estero.

Eastern in the Bulgarian diocese's English name is not written. In Italian
ortodosso orientale names the Churches that did not receive Chalcedon, which
this body is not; ortodossa alone is what it says, and the row stays apart
from the Orthodox Church in America's Diocesi bulgara by the countries it
names.

Three words had never been written in Italian here and are written new, all
of them places: Portogallo, Svizzera and Seul.
"""
NAMES = {
    "constantinople": u"La Chiesa di Costantinopoli",
    "alexandria": u"La Chiesa di Alessandria",
    "antioch": u"La Chiesa di Antiochia",
    "jerusalem": u"La Chiesa di Gerusalemme",
    "russia": u"La Chiesa di Russia",
    "georgia": u"La Chiesa di Georgia",
    "serbia": u"La Chiesa di Serbia",
    "romania": u"La Chiesa di Romania",
    "bulgaria": u"La Chiesa di Bulgaria",
    "cyprus": u"La Chiesa di Cipro",
    "greece": u"La Chiesa di Grecia",
    "albania": u"La Chiesa di Albania",
    "poland": u"La Chiesa di Polonia",
    "czech-slovakia": u"La Chiesa delle Terre ceche e della Slovacchia",
    "oca": u"La Chiesa ortodossa in America",
    "macedonia": u"La Chiesa ortodossa macedone - Arcivescovado di Ocrida",
    "ukraine-uoc": u"La Chiesa di Ucraina",
    "ukraine-ocu": u"Chiesa ortodossa di Ucraina",
    "sinai": u"La Chiesa del Sinai",
    "finland": u"La Chiesa autonoma di Finlandia",
    "japan": u"La Chiesa del Giappone",
    "estonia-eaok": u"Chiesa ortodossa di Estonia",
    "albanian-americas": u"Diocesi ortodossa albanese delle Americhe",
    "acrod": u"Diocesi ortodossa americana carpatorussa dell'America del Nord",
    "ep-thyateira": u"Arcidiocesi di Tiatira e Gran Bretagna",
    "goarch": u"Arcidiocesi greco-ortodossa d'America",
    "ep-france": u"Metropolia greco-ortodossa di Francia",
    "ep-germany": u"Metropolia greco-ortodossa di Germania",
    "ep-austria": u"Sacra Metropolia d'Austria",
    "ep-korea": u"Sacra Metropolia di Corea",
    "ep-spain": u"Sacra Metropolia di Spagna e Portogallo",
    "ep-belgium": u"Metropolia del Belgio",
    "ep-sweden": u"Metropolia di Svezia e di tutta la Scandinavia",
    "ep-switzerland": u"Metropolia della Svizzera",
    "ep-hongkong": u"Metropolitanato ortodosso di Hong Kong e del Sud-Est asiatico",
    "ep-singapore": u"Metropolitanato ortodosso di Singapore e dell'Asia meridionale",
    "ep-italy": u"Sacra Arcidiocesi ortodossa d'Italia e Malta",
    "uocc": u"Chiesa ortodossa ucraina del Canada",
    "uoc-usa": u"Chiesa ortodossa ucraina degli Stati Uniti",
    "antiochian-na": u"Arcidiocesi cristiana ortodossa antiochena dell'America del Nord",
    "rocor": u"Chiesa ortodossa russa all'estero",
    "mp-parishes-usa": u"Le Parrocchie patriarcali negli Stati Uniti",
    "serbian-eastern": u"Diocesi dell'America orientale",
    "serbian-midwestern": u"Diocesi di Nuova Gracanica e del Midwest americano",
    "serbian-western": u"Diocesi dell'America occidentale",
    "romanian-americas": u"Metropolia ortodossa romena delle Americhe",
    "bulgarian-usa": u"Diocesi ortodossa bulgara degli Stati Uniti, del Canada e dell'Australia",
    "oca-albanian": u"Arcidiocesi albanese",
    "oca-canada": u"Arcidiocesi del Canada",
    "oca-washington": u"Arcidiocesi di Washington, D.C.",
    "oca-western-pa": u"Arcidiocesi della Pennsylvania occidentale",
    "oca-bulgarian": u"Diocesi bulgara",
    "oca-eastern-pa": u"Diocesi della Pennsylvania orientale",
    "oca-mexico": u"Diocesi del Messico",
    "oca-new-england": u"Diocesi della Nuova Inghilterra",
    "oca-ny-nj": u"Diocesi di New York e del New Jersey",
    "oca-alaska": u"Diocesi di Sitka e dell'Alaska",
    "oca-midwest": u"Diocesi del Midwest",
    "oca-south": u"Diocesi del Sud",
    "oca-west": u"Diocesi dell'Ovest",
    "oca-romanian": u"Episcopato romeno",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Alessandria",
    "Damascus": u"Damasco",
    "Jerusalem": u"Gerusalemme",
    "Moscow": u"Mosca",
    "Tbilisi": u"Tbilisi",
    "Belgrade": u"Belgrado",
    "Bucharest": u"Bucarest",
    "Sofia": u"Sofia",
    "Nicosia": u"Nicosia",
    "Athens": u"Atene",
    "Tirana": u"Tirana",
    "Warsaw": u"Varsavia",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Kyiv",
    "Mount Sinai": u"Monte Sinai",
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
    "Brussels": u"Bruxelles",
    "Chambesy": u"Chambesy",
    "Chicago, Illinois": u"Chicago, Illinois",
    "Cranberry Township, Pennsylvania": u"Cranberry Township, Pennsylvania",
    "Dallas, Texas": u"Dallas, Texas",
    "Englewood, New Jersey": u"Englewood, New Jersey",
    "Hong Kong": u"Hong Kong",
    "Jackson, Michigan": u"Jackson, Michigan",
    "Johnstown, Pennsylvania": u"Johnstown, Pennsylvania",
    "London": u"Londra",
    "Madrid": u"Madrid",
    "Mexico City": u"Città del Messico",
    "New Rochelle, New York": u"New Rochelle, New York",
    "New York": u"New York",
    "Paris": u"Parigi",
    "Rawdon, Quebec": u"Rawdon, Quebec",
    "San Francisco, California": u"San Francisco, California",
    "Seoul": u"Seul",
    "Singapore": u"Singapore",
    "Somerset, New Jersey": u"Somerset, New Jersey",
    "Stockholm": u"Stoccolma",
    "Third Lake, Illinois": u"Third Lake, Illinois",
    "Toledo, Ohio": u"Toledo, Ohio",
    "Venice": u"Venezia",
    "Vienna": u"Vienna",
    "Windsor, Connecticut": u"Windsor, Connecticut",
    "Winnipeg, Manitoba": u"Winnipeg, Manitoba",
}
STYLED = {
    "constantinople": u"Patriarcato ecumenico",
    "alexandria": u"Patriarcato di Alessandria",
    "antioch": u"Patriarcato di Antiochia e di tutto l'Oriente",
    "jerusalem": u"Patriarcato di Gerusalemme",
    "russia": u"Chiesa ortodossa russa",
    "serbia": u"Chiesa ortodossa serba",
    "romania": u"Chiesa ortodossa romena",
    "bulgaria": u"Chiesa ortodossa bulgara - Patriarcato bulgaro",
    "ukraine-uoc": u"Chiesa ortodossa ucraina",
}
