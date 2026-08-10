# -*- coding: utf-8 -*-
"""German for the vocabulary that stands beside the lives.

TEXT = {the phrase the index shows: the German}. PARTS holds the pieces the
compound place-names are built from, and expand() assembles the wholes, so a
town cannot be spelled one way on one card and another way on the next.

The rank vocabulary was settled before any of this was written, and is set
down in docs/GERMAN.md. German is not a Slavonic tongue and does not require
a rank before a name: der heilige Nikolaus is ordinary German. But it keeps
one distinction that the Western churches around it do not, and that
distinction is asserted everywhere here: the monastic saint is ehrwuerdig,
never merely heilig.

The trap in this language is not a neighbouring alphabet but the Western
church vocabulary standing ready for every word. Kirchenvater and not
Kirchenlehrer, which is a Roman category with a list. Entschlafung and not
Himmelfahrt Mariens, which is a Roman dogma of 1950 and a different claim.
Goettliche Liturgie and not Messe. Gottesgebaererin where the Theotokos is
named as such, because that is what the Council of Ephesus said. Ikone and
not Heiligenbild.

The site writes ss and never the sharp s, because these pages are read in
Switzerland as well as in Germany and Austria and Grossmaertyrer is right in
all three. Umlauts are written as umlauts.

The keys are the phrases exactly as the index writes them, so a rendering
cannot quietly attach itself to the wrong saint.
"""
TEXT = {}


# The orders of sanctity, as the badge on a card names them.
TEXT.update({
    "Angelic": "Himmlische Mächte",
    "Apostle": "Apostel",
    "Confessor": "Bekenner",
    "Equal-to-the-Apostles": "Apostelgleicher",
    "Feast": "Fest",
    "Fool-for-Christ": "Narr um Christi willen",
    "Great Martyr": "Grossmärtyrer",
    "Hierarch": "Hierarch",
    "Hieromartyr": "Priestermärtyrer",
    "Martyr": "Märtyrer",
    "Monastic": "Mönch oder Nonne",
    "New Martyr": "Neumärtyrer",
    "Other": "Weitere",
    "Passion-bearer": "Passionsträger",
    "Prophet": "Prophet",
    "Righteous": "Gerechter",
    "Unmercenary": "Uneigennütziger",
    "Virgin Martyr": "Jungfrau und Märtyrerin",
})


# The attributes a life is marked with.
TEXT.update({
    "Church Father": "Kirchenvater",
    "Desert ascetic": "Wüstenasket",
    "Enlightener": "Erleuchter",
    "Healing intercessor": "Helfer der Kranken",
    "Hymnographer": "Hymnendichter",
    "Iconographer": "Ikonenmaler",
    "Incorrupt relics": "Unverweste Reliquien",
    "Monastery founder": "Klostergründer",
    "Myrrh-bearer": "Myrrhenträgerin",
    "Myrrh-streaming": "Myrrhenströmend",
    "New martyr": "Neumärtyrer",
    "Ruler or royal": "Herrscher oder Königshaus",
    "Stylite": "Stylit",
    "Warrior saint": "Kriegerheiliger",
    "Wonderworker": "Wundertäter",
})


# The ranks the Typikon gives a feast.
TEXT.update({
    "Doxology": "Doxologie",
    "Great Feast": "Hochfest",
    "Polyeleos": "Polyeleos",
    "Simple": "Einfach",
    "Vigil": "Vigil",
})


# The jurisdictions whose calendars the index keeps.
TEXT.update({
    "Antiochian": "Antiochenisch",
    "Greek": "Griechisch",
    "OCA": "OCA",
    "Romanian": "Rumänisch",
    "Russian": "Russisch",
    "Serbian": "Serbisch",
    "Ukrainian": "Ukrainisch",
})


# The estate a saint stood in.
TEXT.update({
    "Apostolic": "Apostolisch",
    "Clergy": "Klerus",
    "Laity": "Laien",
    "Layman": "Laie",
    "Laywoman": "Laiin",
    "Laywomen": "Laiinnen",
    "Married": "Verheiratet",
    "Military": "Soldat",
    "Monastic": "Mönchtum",
    "Prophet": "Prophet",
    "Royal": "Königlich",
    "Royalty": "Königshaus",
    "Unknown": "Unbekannt",
    "Unmarried": "Unverheiratet",
    "Widowed": "Verwitwet",
})


# The ages the lives are set in.
TEXT.update({
    "Age of the Celtic Saints": "Zeit der keltischen Heiligen",
    "Age of the Ecumenical Councils": "Zeit der Ökumenischen Konzilien",
    "Age of the Martyrs": "Zeit der Märtyrer",
    "Apostolic Age": "Apostolische Zeit",
    "Byzantine": "Byzantinisch",
    "Byzantine Balkans": "Byzantinischer Balkan",
    "Byzantine Era": "Byzantinische Zeit",
    "Byzantine Iconoclasm": "Byzantinischer Bilderstreit",
    "Cossack Era": "Kosakenzeit",
    "Desert Fathers": "Wüstenväter",
    "Early Medieval West": "Frühmittelalterlicher Westen",
    "Imperial Russia": "Kaiserliches Russland",
    "Kievan Rus'": "Kiewer Rus",
    "Medieval Georgia": "Mittelalterliches Georgien",
    "Medieval Rus'": "Mittelalterliche Rus",
    "Medieval Serbia": "Mittelalterliches Serbien",
    "Modern": "Neuzeit",
    "Modern Era": "Neuzeit",
    "Muscovite Russia": "Moskauer Russland",
    "Old Testament": "Altes Testament",
    "Ottoman Balkans": "Osmanischer Balkan",
    "Ottoman Era": "Osmanische Zeit",
    "Ottoman period": "Osmanische Zeit",
    "Polish-Lithuanian period": "Polnisch-litauische Zeit",
    "Soviet Era": "Sowjetzeit",
    "Soviet period": "Sowjetzeit",
    "Synodal Russia": "Synodales Russland",
})


# The one movable commemoration the index names.
TEXT.update({
    "Sunday of the Holy Forefathers": "Sonntag der heiligen Altväter",
})


# The countries and the regions.
TEXT.update({
    "Aegean": "Ägäis",
    "America": "Amerika",
    "Arabia": "Arabien",
    "Armenia": "Armenien",
    "Asia Minor": "Kleinasien",
    "Balkans": "Balkan",
    "Belarus": "Weissrussland",
    "Bithynia": "Bithynien",
    "Britain": "Britannien",
    "British Isles": "Britische Inseln",
    "Bulgaria": "Bulgarien",
    "Cappadocia": "Kappadokien",
    "Cilicia": "Kilikien",
    "Constantinople": "Konstantinopel",
    "Crimea": "Krim",
    "Cyprus": "Zypern",
    "Czech Lands": "Böhmische Länder",
    "Dalmatia": "Dalmatien",
    "Danube lands": "Donauländer",
    "Egypt": "Ägypten",
    "England": "England",
    "Ethiopia": "Äthiopien",
    "Gaul": "Gallien",
    "Georgia": "Georgien",
    "Greece": "Griechenland",
    "Holy Land": "Heiliges Land",
    "Illyria": "Illyrien",
    "Illyricum": "Illyricum",
    "India": "Indien",
    "Ireland": "Irland",
    "Italy": "Italien",
    "Lithuania": "Litauen",
    "Macedonia": "Makedonien",
    "Mesopotamia": "Mesopotamien",
    "Moldavia": "Moldau",
    "Montenegro": "Montenegro",
    "Moravia": "Mähren",
    "Mount Athos": "Berg Athos",
    "North Africa": "Nordafrika",
    "North America": "Nordamerika",
    "North Macedonia": "Nordmazedonien",
    "Palestine": "Palästina",
    "Persia": "Persien",
    "Phoenicia": "Phönizien",
    "Poland": "Polen",
    "Pontus": "Pontos",
    "Romania": "Rumänien",
    "Rome": "Rom",
    "Russia": "Russland",
    "Scythia": "Skythien",
    "Serbia": "Serbien",
    "Siberia": "Sibirien",
    "Sinai": "Sinai",
    "Spain": "Spanien",
    "Syria": "Syrien",
    "Thrace": "Thrakien",
    "Ukraine": "Ukraine",
    "Western Rus": "Westliche Rus",
})


# The lands the fasting rule is kept in.
TEXT.update({
    "Albania": "Albanien",
    "Bohemia": "Böhmen",
    "China": "China",
    "France": "Frankreich",
    "Judah": "Juda",
    "Moesia": "Mösien",
    "Sicily": "Sizilien",
    "United States": "Vereinigte Staaten",
})


# The rank a saint held, as the menaia name it. The monastic is ehrwuerdig
# throughout, which is the one distinction German Orthodox usage keeps and
# the Western churches do not; see docs/GERMAN.md.
TEXT.update({
    "Abbess": "Äbtissin",
    "Abbot (Archimandrite)": "Abt (Archimandrit)",
    "Abbot (Founder)": "Abt (Gründer)",
    "Abbot (Igumen)": "Abt (Igumen)",
    "Abbot (Igumen), Confessor": "Abt (Igumen), Bekenner",
    "Abbot (Igumen), Hieromartyr": "Abt (Igumen), Priestermärtyrer",
    "Abbot (Igumen), Martyr": "Abt (Igumen), Märtyrer",
    "Abbot (Igumen), Monastic Martyr": "Abt (Igumen), Mönchsmärtyrer",
    "Abbot, Confessor": "Abt, Bekenner",
    "Abbot, Confessor-Martyr": "Abt, Bekenner und Märtyrer",
    "Abbot, Priest": "Abt, Priester",
    "Abbots": "Äbte",
    "Anchorite": "Anachoret",
    "Apostle of the Seventy": "Apostel der Siebzig",
    "Apostle of the Seventy, Bishop": "Apostel der Siebzig, Bischof",
    "Apostle of the Seventy, Martyr": "Apostel der Siebzig, Märtyrer",
    "Apostle, Evangelist": "Apostel und Evangelist",
    "Apostle, Martyr": "Apostel und Märtyrer",
    "Apostles": "Apostel",
    "Apostles of the Seventy": "Apostel der Siebzig",
    "Apostles of the Seventy, Martyrs": "Apostel der Siebzig, Märtyrer",
    "Archangel": "Erzengel",
    "Archbishop": "Erzbischof",
    "Archbishop, Confessor": "Erzbischof, Bekenner",
    "Archbishop, Equal-to-the-Apostles": "Erzbischof, Apostelgleicher",
    "Archdeacon": "Erzdiakon",
    "Archimandrite": "Archimandrit",
    "Bishop": "Bischof",
    "Bishop, Church Father": "Bischof, Kirchenvater",
    "Bishop, Confessor": "Bischof, Bekenner",
    "Bishop, Equal-to-the-Apostles": "Bischof, Apostelgleicher",
    "Bishop, Hieromartyr": "Bischof, Priestermärtyrer",
    "Bishop, Monk": "Bischof, Mönch",
    "Bishops": "Bischöfe",
    "Blessed Eldress": "Selige Starzin",
    "Chamberlain (cubicularius)": "Kämmerer (cubicularius)",
    "Childmartyr": "Kindermärtyrer",
    "Commander": "Feldherr",
    "Confessor, Archpriest": "Bekenner, Erzpriester",
    "Deacon": "Diakon",
    "Deacon, Monk-martyr": "Diakon, Mönchsmärtyrer",
    "Deaconess": "Diakonisse",
    "Deaconess and Martyr": "Diakonisse und Märtyrerin",
    "Elder": "Starez",
    "Empress": "Kaiserin",
    "Equal-to-the-Apostles, Emperor": "Apostelgleicher, Kaiser",
    "Equals-to-the-Apostles": "Apostelgleiche",
    "Grand Duchess": "Grossfürstin",
    "Grand Prince": "Grossfürst",
    "Grand Princess": "Grossfürstin",
    "Great Martyr, Equal-to-the-Apostles": "Grossmärtyrerin, Apostelgleiche",
    "Great Prince, Martyr": "Grossfürst, Märtyrer",
    "Great-martyr": "Grossmärtyrer",
    "Great-martyr, Prince": "Grossmärtyrer, Fürst",
    "Hermit": "Einsiedler",
    "Hermits": "Einsiedler",
    "Hierarchs": "Hierarchen",
    "Hieromartyr (Hermit)": "Priestermärtyrer (Einsiedler)",
    "Hieromartyr, Apostle": "Priestermärtyrer, Apostel",
    "Hieromartyr, Archbishop": "Priestermärtyrer, Erzbischof",
    "Hieromartyr, Archimandrite": "Priestermärtyrer, Archimandrit",
    "Hieromartyr, Archpriest": "Priestermärtyrer, Erzpriester",
    "Hieromartyr, Bishop": "Priestermärtyrer, Bischof",
    "Hieromartyr, Confessor": "Priestermärtyrer, Bekenner",
    "Hieromartyr, Deacon": "Priestermärtyrer, Diakon",
    "Hieromartyr, Patriarch": "Priestermärtyrer, Patriarch",
    "Hieromartyr, Pope": "Priestermärtyrer, Papst",
    "Hieromartyr, and his son": "Priestermärtyrer, und sein Sohn",
    "Hieromartyrs": "Priestermärtyrer",
    "Hieromonk": "Priestermönch",
    "Hieroschemamonk": "Priesterschemamönch",
    "High Priest": "Hoherpriester",
    "Icon of the Mother of God": "Ikone der Gottesmutter",
    "King and Martyr": "König und Märtyrer",
    "King and Prophet": "König und Prophet",
    "Laymen": "Laien",
    "Martyrs": "Märtyrer",
    "Master Builders, Monks": "Baumeister, Mönche",
    "Metropolitan": "Metropolit",
    "Metropolitan, Equal-to-the-Apostles": "Metropolit, Apostelgleicher",
    "Monastic Martyr": "Mönchsmärtyrer",
    "Monastic Martyrs": "Mönchsmärtyrer",
    "Monastic New Martyr": "Neuer Mönchsmärtyrer",
    "Monastics": "Mönche und Nonnen",
    "Monk": "Mönch",
    "Monk (Founder)": "Mönch (Gründer)",
    "Monk (Hermit)": "Mönch (Einsiedler)",
    "Monk (elder)": "Mönch (Starez)",
    "Monk (hermit)": "Mönch (Einsiedler)",
    "Monk (novice)": "Mönch (Novize)",
    "Monk (recluse)": "Mönch (Klausner)",
    "Monk (stylite)": "Mönch (Stylit)",
    "Monk, Church Father": "Mönch, Kirchenvater",
    "Monk, Confessor": "Mönch, Bekenner",
    "Monk, Elder": "Mönch, Starez",
    "Monk, Hymnographer": "Mönch, Hymnendichter",
    "Monk, Martyr": "Mönch, Märtyrer",
    "Monk, Recluse": "Mönch, Klausner",
    "Monk, Unmercenary Physician": "Mönch, uneigennütziger Arzt",
    "Monk, former Great Zhupan": "Mönch, vormals Grosszupan",
    "Monk-martyr": "Mönchsmärtyrer",
    "Monk-martyrs": "Mönchsmärtyrer",
    "Monks": "Mönche",
    "Monks (Founders)": "Mönche (Gründer)",
    "Mother": "Mutter",
    "Myrrhbearer": "Myrrhenträgerin",
    "New Martyrs": "Neumärtyrer",
    "New Martyrs and Confessors": "Neumärtyrer und Bekenner",
    "Nun": "Nonne",
    "Nun-martyr": "Nonnenmärtyrerin",
    "Patriarch": "Patriarch",
    "Patriarch, Church Father": "Patriarch, Kirchenvater",
    "Patriarch, Confessor": "Patriarch, Bekenner",
    "Patriarch, Hieromartyr": "Patriarch, Priestermärtyrer",
    "Physician": "Arzt",
    "Physicians": "Ärzte",
    "Pope": "Papst",
    "Pope of Rome, Confessor": "Papst von Rom, Bekenner",
    "Presbyter and Deacon": "Presbyter und Diakon",
    "Presbyters, Confessors": "Presbyter, Bekenner",
    "Priest": "Priester",
    "Prince": "Fürst",
    "Prince of Moldavia": "Fürst der Moldau",
    "Prince, Passion-Bearer": "Fürst, Passionsträger",
    "Princes": "Fürsten",
    "Princess": "Fürstin",
    "Princess, Nun": "Fürstin, Nonne",
    "Proconsul (military commander)": "Prokonsul (Feldherr)",
    "Prophet and Forerunner": "Prophet und Vorläufer",
    "Prophetess": "Prophetin",
    "Protomartyr": "Erzmärtyrer",
    "Protopresbyter": "Protopresbyter",
    "Recluse": "Klausner",
    "Right-believing Prince": "Rechtgläubiger Fürst",
    "Right-believing Prince (Monk)": "Rechtgläubiger Fürst (Mönch)",
    "Right-believing Prince and Princess": "Rechtgläubiger Fürst und Fürstin",
    "Right-believing Prince, Passion-bearer": "Rechtgläubiger Fürst, Passionsträger",
    "Right-believing Princess (Nun)": "Rechtgläubige Fürstin (Nonne)",
    "Right-believing Princess, Martyr": "Rechtgläubige Fürstin, Märtyrerin",
    "Righteous (Child)": "Gerechter (Kind)",
    "Righteous (Children)": "Gerechte (Kinder)",
    "Righteous (Unmercenary)": "Gerechter (Uneigennütziger)",
    "Righteous Forefather": "Gerechter Altvater",
    "Righteous Virgin": "Gerechte Jungfrau",
    "Righteous, Priest": "Gerechter, Priester",
    "Roman soldier": "Römischer Soldat",
    "Schemamonk": "Schemamönch",
    "Synaxis": "Synaxis",
    "Tsar and Imperial Family": "Zar und Kaiserfamilie",
    "Unmercenary Martyrs": "Uneigennützige Märtyrer",
    "Venerable": "Ehrwürdiger",
    "Venerable Prince": "Ehrwürdiger Fürst",
    "Venerable Princess": "Ehrwürdige Fürstin",
    "Virgin": "Jungfrau",
    "Virgin Martyrs": "Jungfrauen und Märtyrerinnen",
    "Virgin-martyr": "Jungfrau und Märtyrerin",
    "Youths": "Jünglinge",
})
