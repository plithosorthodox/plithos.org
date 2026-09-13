# -*- coding: utf-8 -*-
"""The directory's rows in Romanian.

Read off what the site already publishes in Romanian rather than composed.
The pattern for a local Church is the one the calendar's own canonization
lines use - Biserica Greciei, Biserica Rusiei, Biserica Ortodoxă din
America - so the row takes the enclitic article Romanian gives the word
Biserica and the country in the genitive. Constantinopolului is the form
standing in Patriarhia Ecumenică a Constantinopolului.

Two forms competed and were counted across everything this site publishes
in Romanian:

  Chiev against Kiev, for the seat of the Church of Ukraine. Chiev stands
  302 times against 200 for the genitive Kievului, and docs/ROMANIAN.md
  names Chiev among the received forms Romanian usage keeps; Chiev.

  Ohrida against Ohrid, for the Macedonian archbishopric. Ohrida stands 49
  times and Ohridei 10; the bare Ohrid appears only where the English is
  quoted. Ohrida.

Five seats had never been named in Romanian here and are written new:
Istanbul, Tirana, Skopje, Tallinn and Tokio, each in the form Romanian
usage has received, and Prešov and Syosset, which Romanian writes as
Slovak and English write them.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Romanian this site publishes and
are taken whole - Patriarhia Ecumenică and the Biserica Ortodoxă Rusă, Sârbă,
Română and Ucraineană of the commemorations.

Settled by counting: the East is Răsărit, 652 times, against Orient not once.
Antioch therefore reads Patriarhia Antiohiei și a întregului Răsărit, on the
pattern of the Patriarh al Moscovei și a toată Rusia the calendar writes.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Romanian name for either
body carries it, so it is not written here.
"""
NAMES = {
    "constantinople": u"Biserica Constantinopolului",
    "alexandria": u"Biserica Alexandriei",
    "antioch": u"Biserica Antiohiei",
    "jerusalem": u"Biserica Ierusalimului",
    "russia": u"Biserica Rusiei",
    "georgia": u"Biserica Georgiei",
    "serbia": u"Biserica Serbiei",
    "romania": u"Biserica României",
    "bulgaria": u"Biserica Bulgariei",
    "cyprus": u"Biserica Ciprului",
    "greece": u"Biserica Greciei",
    "albania": u"Biserica Albaniei",
    "poland": u"Biserica Poloniei",
    "czech-slovakia": u"Biserica Țărilor Cehe și a Slovaciei",
    "oca": u"Biserica Ortodoxă din America",
    "macedonia": u"Biserica Ortodoxă Macedoneană - Arhiepiscopia Ohridei",
    "ukraine-uoc": u"Biserica Ucrainei",
    "ukraine-ocu": u"Biserica Ortodoxă a Ucrainei",
    "sinai": u"Biserica Sinaiului",
    "finland": u"Biserica Autonomă a Finlandei",
    "japan": u"Biserica Japoniei",
    "estonia-eaok": u"Biserica Ortodoxă a Estoniei",
    "albanian-americas": u"Eparhia Ortodoxă Albaneză a Americilor",
    "acrod": u"Eparhia Ortodoxă Americană Carpato-Rusă a Americii de Nord",
    "ep-thyateira": u"Arhiepiscopia Tiatirei și a Marii Britanii",
    "goarch": u"Arhiepiscopia Ortodoxă Greacă a Americii",
    "ep-france": u"Mitropolia Ortodoxă Greacă a Franței",
    "ep-germany": u"Mitropolia Ortodoxă Greacă a Germaniei",
    "ep-austria": u"Sfânta Mitropolie a Austriei",
    "ep-korea": u"Sfânta Mitropolie a Coreei",
    "ep-spain": u"Sfânta Mitropolie a Spaniei și a Portugaliei",
    "ep-belgium": u"Mitropolia Belgiei",
    "ep-sweden": u"Mitropolia Suediei și a toată Scandinavia",
    "ep-switzerland": u"Mitropolia Elveției",
    "ep-hongkong": u"Mitropolia Ortodoxă de Hong Kong și Asia de Sud-Est",
    "ep-singapore": u"Mitropolia Ortodoxă de Singapore și Asia de Sud",
    "ep-italy": u"Sfânta Arhiepiscopie Ortodoxă a Italiei și a Maltei",
    "uocc": u"Biserica Ortodoxă Ucraineană din Canada",
    "uoc-usa": u"Biserica Ortodoxă Ucraineană din Statele Unite",
    "antiochian-na": u"Arhiepiscopia Creștină Ortodoxă Antiohiană a Americii de Nord",
    "rocor": u"Biserica Ortodoxă Rusă din afara Rusiei",
    "mp-parishes-usa": u"Parohiile Patriarhale din Statele Unite",
    "serbian-eastern": u"Eparhia Americii de Est",
    "serbian-midwestern": u"Eparhia de Noua Gracanica și a Americii de Mijloc",
    "serbian-western": u"Eparhia Americii de Vest",
    "romanian-americas": u"Mitropolia Ortodoxă Română a celor două Americi",
    "bulgarian-usa": u"Eparhia Ortodoxă Bulgară de Răsărit a Statelor Unite, Canadei și Australiei",
    "oca-albanian": u"Arhiepiscopia Albaneză",
    "oca-canada": u"Arhiepiscopia Canadei",
    "oca-washington": u"Arhiepiscopia de Washington",
    "oca-western-pa": u"Arhiepiscopia Pennsylvaniei de Vest",
    "oca-bulgarian": u"Eparhia Bulgară",
    "oca-eastern-pa": u"Eparhia Pennsylvaniei de Est",
    "oca-mexico": u"Eparhia Mexicului",
    "oca-new-england": u"Eparhia Noii Anglii",
    "oca-ny-nj": u"Eparhia de New York și New Jersey",
    "oca-alaska": u"Eparhia de Sitka și Alaska",
    "oca-midwest": u"Eparhia Vestului Mijlociu",
    "oca-south": u"Eparhia Sudului",
    "oca-west": u"Eparhia Vestului",
    "oca-romanian": u"Episcopia Română",
}
SEATS = {
    "Istanbul": u"Istanbul",
    "Alexandria": u"Alexandria",
    "Damascus": u"Damasc",
    "Jerusalem": u"Ierusalim",
    "Moscow": u"Moscova",
    "Tbilisi": u"Tbilisi",
    "Belgrade": u"Belgrad",
    "Bucharest": u"București",
    "Sofia": u"Sofia",
    "Nicosia": u"Nicosia",
    "Athens": u"Atena",
    "Tirana": u"Tirana",
    "Warsaw": u"Varșovia",
    "Prešov": u"Prešov",
    "Syosset, New York": u"Syosset, New York",
    "Skopje": u"Skopje",
    "Kyiv": u"Chiev",
    "Mount Sinai": u"Muntele Sinai",
    "Helsinki": u"Helsinki",
    "Tokyo": u"Tokio",
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
    "Mexico City": u"Ciudad de Mexico",
    "New Rochelle, New York": u"New Rochelle, New York",
    "New York": u"New York",
    "Paris": u"Paris",
    "Rawdon, Quebec": u"Rawdon, Quebec",
    "San Francisco, California": u"San Francisco, California",
    "Seoul": u"Seul",
    "Singapore": u"Singapore",
    "Somerset, New Jersey": u"Somerset, New Jersey",
    "Stockholm": u"Stockholm",
    "Third Lake, Illinois": u"Third Lake, Illinois",
    "Toledo, Ohio": u"Toledo, Ohio",
    "Venice": u"Veneția",
    "Vienna": u"Viena",
    "Windsor, Connecticut": u"Windsor, Connecticut",
    "Winnipeg, Manitoba": u"Winnipeg, Manitoba",
}
STYLED = {
    "constantinople": u"Patriarhia Ecumenică",
    "alexandria": u"Patriarhia Alexandriei",
    "antioch": u"Patriarhia Antiohiei și a întregului Răsărit",
    "jerusalem": u"Patriarhia Ierusalimului",
    "russia": u"Biserica Ortodoxă Rusă",
    "serbia": u"Biserica Ortodoxă Sârbă",
    "romania": u"Biserica Ortodoxă Română",
    "bulgaria": u"Biserica Ortodoxă Bulgară - Patriarhia Bulgară",
    "ukraine-uoc": u"Biserica Ortodoxă Ucraineană",
}
