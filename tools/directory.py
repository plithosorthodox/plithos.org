#!/usr/bin/env python3
"""
The directory of Churches.

Builds data/directory.v1.json from the table below. The table is the
sourced record: every row carries the address it was read from and the day
it was read, and both are shown to the reader on the page.

The rule the table obeys is written in docs/DIRECTORY.md and is not
restated here, except for the one line that governs every edit to this
file: a body appears because an autocephalous Church lists it among its
own, and where Churches differ the row says who lists it rather than which
is right.

    python3 tools/directory.py --check
    python3 tools/directory.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import directory_rows

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory.v1.json"

# The day the spine was read. Every row below was confirmed on it.
READ = "2026-09-13"

# The two lists the rows were read from. A row names whichever it came
# from, so a reader can see for himself.
OCA_LIST = "https://www.oca.org/directories/world-churches"
OCA_DIOC = "https://www.oca.org/dioceses"
ASSEMBLY = "https://www.assemblyofbishops.org/directories/jurisdictions"
EP_EUROPE = "https://ec-patr.org/en/other-eparchies-in-europe/"
EP_ASIA = "https://ec-patr.org/en/eparchies-of-the-throne/eparchies-in-asia/"
RO_DIOC = "https://patriarhia.ro/en/organization-of-the-romanian-orthodox-church/dioceses/"

# ---------------------------------------------------------------- the rows
#
# `name` is as the source prints it in its list, so the twenty rows read
# from one list read alike. `styled` is the body's own English designation
# where its own site was read here, and `local` its own language. Four
# sites refused the request from here - Serbia, Cyprus, the Czech Lands and
# Macedonia - so those rows carry the list as their source and say so.
#
# The Patriarchate of Jerusalem writes its own title with a Latin v where the
# Greek nu belongs - Patriarcheiov - which is a slip of a keyboard and not a
# spelling. The row carries the letter the title plainly means. Nothing else
# on any row is altered from what the body prints.
#
# No telephone numbers. They are the field that goes stale invisibly, and
# the ones on the list read here already carried a Moscow dialling code
# retired in the 1990s. A website that answers is a better address than a
# number that does not, and the numbers come back per row when each body's
# own site has been read.

CHURCHES = [
 dict(id="constantinople", order=1, kind="church",
      name="The Church of Constantinople",
      styled="Ecumenical Patriarchate",
      local="Οικουμενικό Πατριαρχείο",
      seat="Istanbul", country="TR",
      address=["Rum Patrikliği", "Dr. Sadık Ahmet Cad. No. 19", "34083 Fatih-İstanbul"],
      site="https://ec-patr.org/", source="https://ec-patr.org/"),

 dict(id="alexandria", order=2, kind="church",
      name="The Church of Alexandria",
      styled="Patriarchate of Alexandria",
      local="Πατριαρχείο Αλεξανδρείας",
      seat="Alexandria", country="EG",
      address=["PO Box 2006", "Alexandria"],
      site="https://www.patriarchateofalexandria.com/",
      source="https://www.patriarchateofalexandria.com/"),

 dict(id="antioch", order=3, kind="church",
      name="The Church of Antioch",
      styled="Greek Orthodox Patriarchate of Antioch and All the East",
      seat="Damascus", country="SY",
      address=["BP 0009", "Damascus"],
      site="https://antiochpatriarchate.org/",
      source="https://antiochpatriarchate.org/"),

 dict(id="jerusalem", order=4, kind="church",
      name="The Church of Jerusalem",
      local=u"Πατριαρχείον Ιεροσολύμων",
      styled="Greek Orthodox Patriarchate of Jerusalem",
      seat="Jerusalem", country="IL",
      address=["P.O. Box 19632", "91190 Jerusalem"],
      site="https://jerusalem-patriarchate.info/",
      source="https://jerusalem-patriarchate.info/"),

 dict(id="russia", order=5, kind="church",
      name="The Church of Russia",
      styled="Russian Orthodox Church",
      local="Русская Православная Церковь",
      seat="Moscow", country="RU",
      address=["5 Chisty Pereulok", "Moscow 119034"],
      site="https://patriarchia.ru/", source="https://patriarchia.ru/"),

 dict(id="georgia", order=6, kind="church",
      name="The Church of Georgia",
      seat="Tbilisi", country="GE",
      address=["King Erekle II Square 1", "Tbilisi 0105"],
      site="https://patriarchate.ge/", source=OCA_LIST),

 dict(id="serbia", order=7, kind="church",
      name="The Church of Serbia",
      styled="Serbian Orthodox Church",
      seat="Belgrade", country="RS",
      address=["Kralja Petra 5", "11000 Belgrade"],
      site="https://spc.rs/",
      sources=["http://arhiva.spc.rs/eng/contact"]),

 dict(id="romania", order=8, kind="church",
      name="The Church of Romania",
      styled="Romanian Orthodox Church",
      local="Biserica Ortodoxă Română",
      seat="Bucharest", country="RO",
      address=["Aleea Patriarhiei 2", "Bucharest"],
      site="https://patriarhia.ro/", source="https://patriarhia.ro/"),

 dict(id="bulgaria", order=9, kind="church",
      name="The Church of Bulgaria",
      styled="Bulgarian Orthodox Church - Bulgarian Patriarchate",
      local="Българска Православна Църква - Българска Патриаршия",
      seat="Sofia", country="BG",
      address=["Oborishte 4", "1000 Sofia"],
      site="https://bg-patriarshia.bg/", source="https://bg-patriarshia.bg/"),

 dict(id="cyprus", order=10, kind="church",
      name="The Church of Cyprus",
      local=u"Ἐκκλησία τῆς Κύπρου",
      seat="Nicosia", country="CY",
      address=[u"Τ.Θ. 21130", u"1502 Λευκωσία"],
      site="https://churchofcyprus.org.cy/",
      sources=["https://churchofcyprus.org.cy/stoicheia-epikoinonias",
               "https://churchofcyprus.org.cy/diikitiki_diathrosi"]),

 dict(id="greece", order=11, kind="church",
      name="The Church of Greece",
      local="Η Εκκλησία της Ελλάδος",
      seat="Athens", country="GR",
      address=["Ag. Philotheis 21", "10556 Athens"],
      site="https://ecclesiagreece.gr/",
      sources=["https://ecclesiagreece.gr/", OCA_LIST]),

 dict(id="albania", order=12, kind="church",
      name="The Church of Albania",
      local="Kisha Orthodhokse Autoqefale e Shqipërisë",
      seat="Tirana", country="AL",
      address=["Rruga e Kavajës 151", "Tirana"],
      site="https://orthodoxalbania.org/",
      source="https://orthodoxalbania.org/"),

 dict(id="poland", order=13, kind="church",
      name="The Church of Poland",
      local="Polski Autokefaliczny Kościół Prawosławny",
      seat="Warsaw", country="PL",
      address=["Al. Solidarności 52", "03-402 Warszawa"],
      site="https://www.orthodox.pl/", source="https://www.orthodox.pl/"),

 dict(id="czech-slovakia", order=14, kind="church",
      name="The Church of the Czech Lands and Slovakia",
      local=u"Pravoslávna cirkev v českých krajinách a na Slovensku",
      seat="Prešov", country="SK",
      address=["Bayerova 8", "08001 Prešov"],
      site="https://orthodox.sk/", source="https://orthodox.sk/kontakt/"),

 dict(id="oca", order=15, kind="church",
      name="The Orthodox Church in America",
      seat="Syosset, New York", country="US",
      address=["PO Box 675", "Syosset, NY 11791-0675"],
      site="https://www.oca.org/", source="https://www.oca.org/",
      standing="Autocephaly was granted by the Church of Russia on 10 April 1970.",
      standing_source="https://www.oca.org/history-archives/tomos-of-autocephaly"),

 dict(id="macedonia", order=16, kind="church",
      name="The Macedonian Orthodox Church - Ohrid Archbishopric",
      local="Македонска Православна Црква - Охридска Архиепископија",
      seat="Skopje", country="MK",
      address=["Партизански одреди 12", "1000 Скопје"],
      site="http://www.mpc.org.mk/", sources=["http://www.mpc.org.mk/", OCA_LIST],
      standing="The Church of Serbia handed it a Tomos confirming its autocephaly on 5 June 2022.",
      standing_source="http://arhiva.spc.rs/sr/patrijarh_srpski_porfirije_uruchio_arhiepiskopu_stefanu_tomos_kojim_se_potvrdjuje_autekefalnost_make.html"),

 dict(id="ukraine-uoc", order=17, kind="church",
      name="The Church of Ukraine",
      local=u"Українська Православна Церква",
      styled="Ukrainian Orthodox Church",
      seat="Kyiv", country="UA",
      address=["Sichnevoho Povstannia 25, korp. 49", "01015 Kyiv"],
      site="https://church.ua/",
      sources=["https://church.ua/", OCA_LIST],
      standing="Its Council of 27 May 2022 amended the Statute in terms it says testify to the full independence and autonomy of the Ukrainian Orthodox Church.",
      standing_source="https://uoc-news.church/2022/05/28/resolutions-council-ukrainian-orthodox-church-may-27-2022/?lang=en"),

 dict(id="ukraine-ocu", order=18, kind="church",
      name="Orthodox Church of Ukraine",
      local="Православна Церква України",
      seat="Kyiv", country="UA",
      address=["Triokhsviatytelska 8", "01001 Kyiv"],
      site="https://www.pomisna.info/",
      source="https://www.pomisna.info/",
      standing="The Ecumenical Patriarchate bestowed autocephaly by Patriarchal and Synodal Tomos in January 2019.",
      standing_source="https://ec-patr.org/en/patriarchal-and-synodal-tomos-for-the-bestowal-of-the-ecclesiastical-status-of-autocephaly-to-the-orthodox-church-in-ukraine/"),

 dict(id="sinai", order=19, kind="autonomous",
      name="The Church of Sinai",
      local=u"Ιερά Μονή Θεοβαδίστου Όρους Σινά, Αγίας Αικατερίνης",
      seat="Mount Sinai", country="EG",
      address=["Monastery of Saint Catherine at Mount Sinai", "c/o Midan el-Daher", "11271 Cairo"],
      site="https://www.sinaimonastery.com/index.php/en/",
      source="https://www.sinaimonastery.com/index.php/en/"),

 dict(id="finland", order=20, kind="autonomous",
      name="The Autonomous Church of Finland",
      local=u"Suomen Ortodoksinen Kirkko",
      seat="Helsinki", country="FI",
      address=["Liisankatu 29 A", "00170 Helsinki"],
      site="https://ort.fi/", source="https://ort.fi/"),

 dict(id="japan", order=21, kind="autonomous",
      name="The Church of Japan",
      local=u"日本ハリストス正教会",
      seat="Tokyo", country="JP",
      address=["Nicholai-do, 1-4 Surugadai", "Kanda, Chiyoda-ku", "Tokyo 101"],
      site="https://www.orthodoxjapan.jp/",
      source="https://www.orthodoxjapan.jp/"),

 dict(id="estonia-eaok", order=22, kind="autonomous",
      name="Orthodox Church of Estonia",
      local="Eesti Apostlik-Õigeusu Kirik",
      seat="Tallinn", country="EE",
      site="https://www.eoc.ee/", source="https://www.eoc.ee/",
      standing="The Ecumenical Patriarchate names it among the autonomous Churches of the Throne.",
      standing_source="https://ec-patr.org/en/eparchies-of-the-throne/autonomous-churches/"),
]


# ------------------------------------------------------------- the dioceses
#
# North America first, and complete: every canonical jurisdiction on the
# continent and every diocese of the one autocephalous Church that is of it.
# It is the largest Orthodox population outside the traditional lands, it is
# where most readers of this site are, and - the reason it could be done
# first - the bishops of all of these Churches sit in one Assembly which
# publishes one list of them. That list is what a register wants: not one
# Church's view of who is here, but the view they hold together.
#
# The rest of the world follows. The Ecumenical Patriarchate's eparchies in
# Europe, Asia and Oceania are named on its own site but without addresses,
# and the metropolises of Greece and Turkey run to a hundred more; those are
# the next pass, not this one.

DIOCESES = [
 # The Orthodox Church in America, from its own directory of dioceses.
 dict(id="oca-alaska", parent="oca", name="Diocese of Sitka and Alaska",
      seat="Anchorage, Alaska", country="US",
      address=["430 C Street Ste 301", "Anchorage, AK 99501"],
      site="https://odosa.org/", source=OCA_DIOC),
 dict(id="oca-albanian", parent="oca", name="Albanian Archdiocese",
      seat="Boston, Massachusetts", country="US",
      address=["517 East Broadway", "South Boston, MA 02127-4415"],
      site="https://albanianarchdiocese.org/", source=OCA_DIOC),
 dict(id="oca-bulgarian", parent="oca", name="Bulgarian Diocese",
      seat="Toledo, Ohio", country="US",
      address=["519 Brynhaven Dr", "Oregon, OH 43616-2809"],
      site="https://www.bdoca.org/", source=OCA_DIOC),
 dict(id="oca-canada", parent="oca", name="Archdiocese of Canada",
      seat="Rawdon, Quebec", country="CA",
      address=["3441 15th Ave", "Rawdon, QC J0K 1S0"],
      site="https://www.archdiocese.ca/", source=OCA_DIOC),
 dict(id="oca-eastern-pa", parent="oca", name="Diocese of Eastern Pennsylvania",
      seat="Bath, Pennsylvania", country="US",
      address=["325 N Walnut St", "Bath, PA 18014"],
      site="https://doepa.org/", source=OCA_DIOC),
 dict(id="oca-mexico", parent="oca", name="Diocese of Mexico",
      seat="Mexico City", country="MX",
      address=["Calle Irapuato 53", "Penon de los Banos, Venustiano Carranza", "C.P. 15520, CDMX"],
      site="https://ocamexico.org/", source=OCA_DIOC),
 dict(id="oca-new-england", parent="oca", name="Diocese of New England",
      seat="Windsor, Connecticut", country="US",
      address=["9 River Bend Ln", "Windsor, CT 06095-1617"],
      site="https://www.dneoca.org/", source=OCA_DIOC),
 dict(id="oca-ny-nj", parent="oca", name="Diocese of New York and New Jersey",
      seat="Bronxville, New York", country="US",
      address=["33 Hewitt Avenue", "Bronxville, NY 10708-2333"],
      site="https://www.nynjoca.org/", source=OCA_DIOC),
 dict(id="oca-midwest", parent="oca", name="Diocese of the Midwest",
      seat="Chicago, Illinois", country="US",
      address=["917 North Wood Street", "Chicago, IL 60622"],
      site="https://domoca.org/", source=OCA_DIOC),
 dict(id="oca-south", parent="oca", name="Diocese of the South",
      seat="Dallas, Texas", country="US",
      address=["4222 Wycliff Ave", "Dallas, TX 75219"],
      site="https://dosoca.org/", source=OCA_DIOC),
 dict(id="oca-west", parent="oca", name="Diocese of the West",
      seat="San Francisco, California", country="US",
      address=["1520 Green St", "San Francisco, CA 94123-5102"],
      site="https://dowoca.org/", source=OCA_DIOC),
 dict(id="oca-washington", parent="oca", name="Archdiocese of Washington, D.C.",
      seat="Alexandria, Virginia", country="US",
      address=["PO Box 31409", "Alexandria, VA 22310"],
      site="https://wdcoca.org/", source=OCA_DIOC),
 dict(id="oca-western-pa", parent="oca", name="Archdiocese of Western Pennsylvania",
      seat="Cranberry Township, Pennsylvania", country="US",
      address=["8641 Peters Rd", "Cranberry Township, PA 16066-3825"],
      site="https://www.ocadwpa.org/", source=OCA_DIOC),
 dict(id="oca-romanian", parent="oca", name="Romanian Episcopate",
      seat="Jackson, Michigan", country="US",
      address=["2535 Grey Tower Rd", "Jackson, MI 49201"],
      site="https://roea.org/", source=OCA_DIOC),

 # Under the Ecumenical Patriarchate.
 dict(id="goarch", parent="constantinople",
      name="Greek Orthodox Archdiocese of America",
      seat="New York", country="US",
      address=["8 E. 79th St", "New York, NY 10021"],
      site="https://www.goarch.org/", source="https://ec-patr.org/en/eparchies-of-the-throne/eparchies-in-america/"),
 dict(id="acrod", parent="constantinople",
      name="American Carpatho-Russian Orthodox Diocese of North America",
      seat="Johnstown, Pennsylvania", country="US",
      address=["312 Garfield Street", "Johnstown, PA 15906"],
      site="https://www.acrod.org/", source="https://www.acrod.org/about/contact/"),
 dict(id="uoc-usa", parent="constantinople",
      name="Ukrainian Orthodox Church of the USA",
      seat="Somerset, New Jersey", country="US",
      address=["Metropolia Center", "135 Davidson Avenue", "Somerset, NJ 08873"],
      site="https://uocofusa.org/", source="https://uocofusa.org/"),
 dict(id="uocc", parent="constantinople",
      name="Ukrainian Orthodox Church of Canada",
      seat="Winnipeg, Manitoba", country="CA",
      address=["9 St. John's Avenue", "Winnipeg, MB R2W 1G8"],
      site="https://www.uocc.ca/", source="https://www.uocc.ca/contact/"),
 dict(id="albanian-americas", parent="constantinople",
      name="Albanian Orthodox Diocese of the Americas",
      local="Dioqeza Ortodokse Shqiptare e Amerikave",
      seat="Boston, Massachusetts", country="US",
      address=["PO Box 224", "245 D Street", "South Boston, MA 02127-0003"],
      site="https://albaniandiocese-ep.org/",
      source="https://albaniandiocese-ep.org/"),

 # Under Antioch.
 dict(id="antiochian-na", parent="antioch",
      name="Antiochian Orthodox Christian Archdiocese of North America",
      seat="Englewood, New Jersey", country="US",
      address=["PO Box 5238", "Englewood, NJ 07631-5238"],
      site="https://www.antiochian.org/",
      sources=["https://www.antiochian.org/", OCA_LIST]),

 # Under Russia. The Russian Orthodox Church Outside of Russia stood here
 # and no longer does: the Statute of the Russian Orthodox Church names it a
 # self-governing part of that Church with its own dioceses, and a body with
 # dioceses is not one. Its row is in directory_rows/_churches.py.
 dict(id="mp-parishes-usa", parent="russia",
      name="The Patriarchal Parishes in the USA",
      seat="New York", country="US",
      address=["15 E. 97th Street", "New York, NY 10029"],
      site="https://mospatusa.com/", source="https://mospatusa.com/"),

 # Under Serbia.
 dict(id="serbian-eastern", parent="serbia", name="Diocese of Eastern America",
      seat="New Rochelle, New York", country="US",
      address=["65 Overlook Circle", "New Rochelle, NY 10804-4501"],
      site="https://www.serborth.org/easternamerica",
      source="https://www.serborth.org/easternamerica"),
 dict(id="serbian-western", parent="serbia", name="Diocese of Western America",
      seat="Alhambra, California", country="US",
      address=["1621 W Garvey Avenue", "Alhambra, CA 91803"],
      site="https://www.serborth.org/westernamerica",
      source="https://www.serborth.org/westernamerica"),
 dict(id="serbian-midwestern", parent="serbia",
      name="Diocese of New Gracanica and Midwestern America",
      seat="Third Lake, Illinois", country="US",
      address=["35240 W Grant Ave", "Third Lake, IL 60046"],
      site="https://www.serborth.org/newgracanica",
      source="https://www.serborth.org/newgracanica"),

 # Under Romania.
 dict(id="romanian-americas", parent="romania",
      name="Romanian Orthodox Metropolia of the Americas",
      seat="Chicago, Illinois", country="US",
      address=["5410 N. Newland Ave", "Chicago, IL 60656-2026"],
      site="https://www.mitropolia.us/index.php/en/", source=RO_DIOC),

 # Under Bulgaria.
 dict(id="bulgarian-usa", parent="bulgaria",
      name="Bulgarian Eastern Orthodox Diocese of the USA, Canada and Australia",
      seat="New York", country="US",
      address=["550A W. 50th St", "New York, NY 10019"],
      site="https://www.bulgariandiocese.org/", source="https://www.bulgariandiocese.org/contact"),

 # The Ecumenical Patriarchate's eparchies beyond North America, from its
 # own pages for each. Where the address it publishes for an eparchy did not
 # answer, the row keeps the postal address - which is the part a reader can
 # still use - and offers no link rather than a dead one.
 dict(id="ep-thyateira", parent="constantinople",
      name="Archdiocese of Thyateira and Great Britain",
      seat="London", country="GB",
      address=["Thyateira House", "5 Craven Hill", "London W2 3EN"],
      site="https://www.thyateira.org.uk/",
      source="https://ec-patr.org/en/entities/holy-archdiocese-of-thyatira-and-great-britain/"),
 dict(id="ep-france", parent="constantinople",
      name="Greek Orthodox Metropolis of France",
      local="Metropole grecque-orthodoxe de France",
      seat="Paris", country="FR",
      address=["7 Rue Georges Bizet", "75116 Paris"],
      source="https://ec-patr.org/en/entities/metropolis-of-france/"),
 dict(id="ep-germany", parent="constantinople",
      name="Greek Orthodox Metropolis of Germany",
      local="Griechisch-Orthodoxe Metropolie von Deutschland",
      seat="Bonn", country="DE",
      address=["Dietrich-Bonhoeffer-Str. 2", "53227 Bonn"],
      site="https://www.orthodoxie.net/",
      source="https://ec-patr.org/en/entities/holy-metropolis-of-germany/"),
 dict(id="ep-austria", parent="constantinople",
      name="Holy Metropolis of Austria",
      seat="Vienna", country="AT",
      address=["Fleischmarkt 13", "1010 Wien"],
      site="https://www.metropolisaustria.at/",
      source="https://ec-patr.org/en/entities/holy-metropolis-of-austria/"),
 dict(id="ep-sweden", parent="constantinople",
      name="Metropolis of Sweden and All Scandinavia",
      seat="Stockholm", country="SE",
      address=["Birger Jarlsgatan 92", "114 20 Stockholm"],
      source="https://ec-patr.org/en/entities/holy-metropolis-of-sweden-and-all-scandinavia/"),
 dict(id="ep-belgium", parent="constantinople",
      name="Metropolis of Belgium",
      seat="Brussels", country="BE",
      address=["Avenue Charbo 71", "1030 Brussels"],
      site="https://orthodoxia.be/",
      source="https://ec-patr.org/en/entities/holy-metropolis-of-belgium/"),
 dict(id="ep-switzerland", parent="constantinople",
      name="Metropolis of Switzerland",
      seat="Chambesy", country="CH",
      address=["Route de Lausanne 282", "CH-1292 Chambesy"],
      site="https://dioceseorthodoxe.org/",
      source="https://ec-patr.org/en/entities/holy-metropolis-of-switzerland/"),
 dict(id="ep-italy", parent="constantinople",
      name="Sacred Orthodox Archdiocese of Italy and Malta",
      local="Sacra Arcidiocesi Ortodossa d'Italia e Malta",
      seat="Venice", country="IT",
      address=["Castello 3422", "Campo dei Greci", "30122 Venezia"],
      site="https://ortodossia.it/",
      source="https://ec-patr.org/en/entities/holy-metropolis-of-italy/"),
 dict(id="ep-spain", parent="constantinople",
      name="Holy Metropolis of Spain and Portugal",
      local="Arzobispado Ortodoxo de Espana y Portugal",
      seat="Madrid", country="ES",
      address=["Calle Nicaragua 12", "28016 Madrid"],
      source="https://ec-patr.org/en/entities/holy-metropolis-of-spain-and-portugal/"),
 dict(id="ep-hongkong", parent="constantinople",
      name="Orthodox Metropolitanate of Hong Kong and South East Asia",
      seat="Hong Kong", country="HK",
      address=["704 Universal Trade Center", "3 Arbuthnot Rd", "Hong Kong"],
      source="https://ec-patr.org/en/entities/holy-metropolis-of-hong-kong/"),
 dict(id="ep-korea", parent="constantinople",
      name="Holy Metropolis of Korea",
      seat="Seoul", country="KR",
      address=["424-1 Ahyeon-dong", "Mapo-gu, Seoul"],
      source="https://ec-patr.org/en/entities/holy-metropolis-of-korea/"),
 # The Holy Mountain. The Patriarchate names it among its own under
 # Patriarchal and Stavropegic Monasteries and calls it a Holy Patriarchal
 # Exarchy. It publishes no postal address for it.
 dict(id="athos", parent="constantinople",
      name="Monastic Community of the Holy Mountain",
      country="GR", checked="2026-09-14",
      sources=["https://ec-patr.org/en/entities/monastic-community-of-the-holy-mountain/",
               "https://ec-patr.org/en/eparchies-of-the-throne/patriarchal-and-stavropegic-monasteries/"]),

 dict(id="ep-singapore", parent="constantinople",
      name="Orthodox Metropolitanate of Singapore and South Asia",
      seat="Singapore", country="SG",
      address=["16 Raffles Quay, #41-07", "Hong Leong Building", "Singapore"],
      site="https://omsgsa.org/",
      source="https://ec-patr.org/en/entities/holy-metropolis-of-singapore/"),

 # The Romanian Patriarchate's own eparchies, from its own list of them. Its
 # metropolitan sees, which is what that list gives; the suffragan bishoprics
 # under each are a further pass.
 dict(id="ro-bucharest", parent="romania", name="Archdiocese of Bucharest",
      seat="Bucharest", country="RO",
      address=["Intrarea Miron Cristea 9", "RO-040162 Bucharest 4"],
      site="https://arhiepiscopiabucurestilor.ro/", source=RO_DIOC),
 dict(id="ro-iasi", parent="romania", name="Archdiocese of Jassy",
      seat="Jassy", country="RO",
      address=["Stefan cel Mare si Sfant 16", "RO-700064 Jassy, Jassy County"],
      site="https://mmb.ro/", source=RO_DIOC),
 dict(id="ro-sibiu", parent="romania", name="Archdiocese of Sibiu",
      seat="Sibiu", country="RO",
      address=["Strada Mitropoliei 24", "RO-550179 Sibiu, Sibiu County"],
      site="https://mitropolia-ardealului.ro/", source=RO_DIOC),
 dict(id="ro-cluj", parent="romania", name="Archdiocese of Vad, Feleac and Cluj",
      seat="Cluj-Napoca", country="RO",
      address=["Piata Avram Iancu 18", "RO-400117 Cluj-Napoca, Cluj"],
      site="https://mitropolia-clujului.ro/", source=RO_DIOC),
 dict(id="ro-craiova", parent="romania", name="Archdiocese of Craiova",
      seat="Craiova", country="RO",
      address=["Strada Mitropolitul Firmilian 3", "RO-200381 Craiova, Dolj"],
      site="https://mitropoliaolteniei.ro/", source=RO_DIOC),
 dict(id="ro-timisoara", parent="romania", name="Archdiocese of Timisoara",
      seat="Timisoara", country="RO",
      address=["Strada C.D. Loga 7", "RO-300021 Timisoara, Timis"],
      site="https://mitropolia-banatului.ro/", source=RO_DIOC),
 dict(id="ro-tomis", parent="romania", name="Archdiocese of Tomis",
      seat="Constanta", country="RO",
      address=["Strada Arhiepiscopiei 23", "RO-900732 Constanta"],
      site="https://arhiepiscopiatomisului.ro/", source=RO_DIOC),
 dict(id="ro-chisinau", parent="romania", name="Archdiocese of Chisinau",
      seat="Chisinau", country="MD",
      address=["Strada 31 August 161", "MD-2004 Chisinau"],
      site="https://mitropoliabasarabiei.md/", source=RO_DIOC),
 dict(id="ro-western-europe", parent="romania",
      name="Romanian Orthodox Archdiocese of Western Europe",
      seat="Limours", country="FR",
      address=["1 Boulevard du General Leclerc", "91470 Limours"],
      site="https://www.mitropolia.eu/", source=RO_DIOC),
 dict(id="ro-germany", parent="romania",
      name="Romanian Orthodox Metropolis of Germany, Central and Northern Europe",
      seat="Nuremberg", country="DE",
      address=["Fuertherstrasse 166-168", "D-90429 Nuernberg"],
      site="https://mitropolia-ro.de/", source=RO_DIOC),
]

# The countries a row can name, written out so the page has a word to show
# and a key to filter on. English here; the page carries the rest.
COUNTRIES = {
    "AM": "Armenia", "AZ": "Azerbaijan", "BY": "Belarus", "KG": "Kyrgyzstan", "KZ": "Kazakhstan", "LT": "Lithuania", "LV": "Latvia", "MT": "Malta", "NL": "Netherlands", "NZ": "New Zealand", "PH": "Philippines", "QA": "Qatar", "TH": "Thailand", "TJ": "Tajikistan", "TM": "Turkmenistan", "UZ": "Uzbekistan",
    "BA": "Bosnia and Herzegovina", "HR": "Croatia", "ME": "Montenegro",
    "AL": "Albania", "AT": "Austria", "MD": "Moldova", "BE": "Belgium", "BG": "Bulgaria",
    "BA": "Bosnia and Herzegovina", "CZ": "Czechia", "HR": "Croatia",
    "ME": "Montenegro",
    "CA": "Canada", "CH": "Switzerland", "CY": "Cyprus", "DE": "Germany",
    "EE": "Estonia", "ES": "Spain", "FR": "France", "GB": "United Kingdom",
    "HK": "Hong Kong", "IT": "Italy", "KR": "South Korea", "MX": "Mexico",
    "SE": "Sweden", "SG": "Singapore",
    "EG": "Egypt", "FI": "Finland", "GE": "Georgia", "GR": "Greece",
    "IL": "Israel", "JP": "Japan", "MK": "North Macedonia", "PL": "Poland",
    "RO": "Romania", "RS": "Serbia", "RU": "Russia", "SK": "Slovakia",
    "SY": "Syria", "TR": "Turkey", "UA": "Ukraine", "US": "United States",
    "AU": "Australia", "CN": "China", "HU": "Hungary", "IE": "Ireland",
    "AR": "Argentina", "BR": "Brazil", "CL": "Chile", "IQ": "Iraq",
    "JO": "Jordan", "LB": "Lebanon", "PS": "Palestine",
    "BI": "Burundi", "BJ": "Benin", "BW": "Botswana", "CD": "Congo-Kinshasa",
    "CG": "Congo-Brazzaville", "CM": "Cameroon", "ET": "Ethiopia",
    "GH": "Ghana", "GN": "Guinea", "KE": "Kenya", "LY": "Libya",
    "MG": "Madagascar", "MW": "Malawi", "NG": "Nigeria", "RW": "Rwanda",
    "SD": "Sudan", "SS": "South Sudan", "TN": "Tunisia", "TZ": "Tanzania",
    "UG": "Uganda", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe",
}


def sources_of(r):
    """One to three URLs, however the row wrote them.

    A row used to carry one source, which made a dead link a dead end: a
    reader who could not reach the one address the site gave him had nowhere
    else to go. Three is the cap, because a list of citations a reader will
    not follow is not provenance, it is decoration."""
    v = r.get("sources") or r.get("source") or []
    if isinstance(v, str):
        v = [v]
    v = [u for u in v if str(u).startswith("http")]
    if len(v) > 3:
        raise SystemExit("%s cites %d sources; three is the cap"
                         % (r.get("id"), len(v)))
    return v


def build():
    # The Churches read after the spine live in directory_rows/_churches.py,
    # and their dioceses in a file named for each, the same as every other
    # Church. A row that carries its own reading date keeps it: rows read
    # today were publishing the spine's date because one global stamped them
    # all.
    mod = directory_rows._mod("_churches")
    more = list(getattr(mod, "ROWS", [])) if mod else []
    rows = []
    for c in sorted(CHURCHES + more, key=lambda r: r["order"]):
        r = {k: v for k, v in c.items() if v not in (None, "", [])}
        r.setdefault("checked", READ)
        rows.append(r)
    order = dict((r["id"], r["order"]) for r in rows)
    every = DIOCESES + directory_rows.all_rows()
    for c in more:
        if c["id"] not in directory_rows.CHURCHES:
            every = every + directory_rows.rows(c["id"])
    # A diocese hangs off a Church, and some hang off a body that is itself
    # under a Church: the Church of Russia names among its own the Patriarchal
    # Exarchate of Africa, and the eparchies in Africa are the Exarchate's
    # rather than Moscow's directly. `parent` is always the body immediately
    # above, so the register can say which of the two a see belongs to, and
    # the Church it finally answers to is walked up to here.
    kin = dict((c["id"], c["parent"]) for c in every)
    def church_of(i):
        seen = set()
        while i in kin:
            if i in seen:
                raise SystemExit("%s sits inside itself" % i)
            seen.add(i)
            i = kin[i]
        return i
    for c in sorted(every, key=lambda r: (order.get(church_of(r["id"]), 99),
                                          r["name"])):
        r = {k: v for k, v in c.items() if v not in (None, "", [])}
        r["kind"] = "diocese"
        r.setdefault("checked", READ)
        if r["parent"] not in order and r["parent"] not in kin:
            raise SystemExit("%s hangs off nobody: %s"
                             % (r["id"], r["parent"]))
        if church_of(r["id"]) not in order:
            raise SystemExit("%s hangs off no Church: %s"
                             % (r["id"], church_of(r["id"])))
        rows.append(r)
    seen_ids = set()
    for r in rows:
        if r["id"] in seen_ids:
            raise SystemExit("duplicate id: " + r["id"])
        seen_ids.add(r["id"])
        if r["country"] not in COUNTRIES:
            raise SystemExit("no country name for " + r["country"])
        r["sources"] = sources_of(r)
        r.pop("source", None)
        if not r["sources"]:
            raise SystemExit("%s: cites nothing" % r["id"])
        # A seat is not required. A see this site can name and point at is
        # worth a row even where nobody publishes where it sits, and a row
        # that says a body exists and where to read about it is the whole
        # minimum. Name, country and a citation are that minimum.
        for f in ("name", "country"):
            if not r.get(f):
                raise SystemExit("%s: missing %s" % (r["id"], f))
        # An address is the lines it is printed on, not a sentence. The page
        # sets them one under another, the way an envelope wants them.
        if r.get("address") and not isinstance(r["address"], list):
            raise SystemExit("%s: address is not a list of lines" % r["id"])
        # What a body says about its own beginning, in its own words - a
        # year, or a phrase like "1219, restored 1992". It is written only
        # where the body or its Church publishes it, and it is never reduced
        # to a bare number the source did not print.
        if r.get("founded") and not isinstance(r["founded"], str):
            raise SystemExit("%s: founded is not what the source printed"
                             % r["id"])
        # Every row answers with a link. Where the body's own site did not
        # answer, the row gives the list it was read from - which is the next
        # level up and says where the entry came from. Which of the two it is
        # is remembered here and said on the page: two hundred and forty rows
        # were being given their Patriarchate's address under the plain word
        # Website, which tells a reader the body has a site of its own when
        # what it has is a page on somebody else's.
        r["mine"] = bool(r.get("site"))
        r.setdefault("site", r["sources"][0])

    # A row cites the body itself or the Church it belongs to, and nobody
    # else. Reading the Church of Serbia's address off another Church's
    # directory is how the entry was got, and printing that other Church on
    # the row makes it look like an authority over this one. So the page
    # shows the source only when it belongs to the row, and rows that would
    # cite a stranger are listed here to be read again from their own.
    where = dict((x["id"], x.get("site", "")) for x in rows)

    # A Church and its own archive are the same Church. Comparing whole
    # hostnames made arhiva.spc.rs a stranger to spc.rs, and the Serbian
    # Patriarchate's own contact page was refused as a citation for the
    # Serbian Patriarchate. What matters is the registrable domain, which is
    # the last two labels except under a second level like org.uk or com.mk,
    # where it is the last three.
    SECOND = {"co", "com", "org", "net", "gov", "edu", "ac", "or", "ne"}

    def dom(u):
        host = re.sub(r"^https?://", "", u or "").split("/")[0].lower()
        bits = [b for b in host.split(".") if b]
        if len(bits) > 2 and bits[-2] in SECOND:
            return ".".join(bits[-3:])
        return ".".join(bits[-2:])

    up = dict((x["id"], x.get("parent") or x.get("within")) for x in rows)
    for r in rows:
        # The body itself, the Church it belongs to, and the Church that one
        # belongs to. The chain matters because a Church can sit inside a
        # Church: the Russian Orthodox Church Outside of Russia is
        # self-governing and its dioceses are its own, but the register that
        # publishes them is Moscow's, and Moscow is not a stranger to them.
        # Beyond a grandparent it would be, so the walk stops there.
        own = {dom(r.get("site"))}
        seen, p = set(), r.get("parent") or r.get("within")
        while p and p not in seen:
            seen.add(p)
            own.add(dom(where.get(p)))
            p = up.get(p)
        r["cite"] = [u for u in r["sources"] if dom(u) in own]

        # Whose door the link is. A row that never had a site of its own,
        # and a row whose site is word for word the site of the Church above
        # it, are both answered by that Church, and the page names it rather
        # than printing the link bare. A row may say whose it is itself,
        # which is the only way to get it right where a Church answers on
        # more than one domain: the two churches in China are published by
        # Moscow at mospat.ru, and the Church of Russia's own site is
        # patriarchia.ru, so nothing here could have matched them up.
        here = (r.get("site") or "").rstrip("/")
        p = r.get("parent") or r.get("within")
        seen = set()
        while p and not r.get("site_of") and p not in seen:
            seen.add(p)
            there = (where.get(p) or "").rstrip("/")
            if there and (not r["mine"] and dom(there) == dom(here)
                          or here == there):
                r["site_of"] = p
                break
            p = up.get(p)
        if r.get("site_of") and r["site_of"] not in order and \
                r["site_of"] not in seen_ids:
            raise SystemExit("%s: site_of names nobody: %s"
                             % (r["id"], r["site_of"]))
        r.pop("mine", None)
    return {"v": 1, "read": READ, "countries": COUNTRIES, "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    d = build()
    text = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    if a.write:
        OUT.write_text(text, encoding="utf-8")
        print("wrote %s  (%d rows, %d countries, %d KB)"
              % (OUT.relative_to(ROOT), len(d["rows"]), len(d["countries"]),
                 len(text.encode("utf-8")) // 1024 or 1))
        return 0
    have = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if have != text:
        print("data/directory.v1.json is out of date", file=sys.stderr)
        return 1
    print("%d rows, %d countries, all sourced and dated"
          % (len(d["rows"]), len(d["countries"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
