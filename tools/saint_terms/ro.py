# -*- coding: utf-8 -*-
"""Romanian for the vocabulary that stands beside the lives.

TEXT = {the phrase the index shows: the Romanian}. PARTS holds the pieces the
compound place-names are built from, and expand() assembles the wholes, so a
town cannot be spelled one way on one card and another way on the next.

Romanian is a liturgical tongue of the Church and has its own received words
for what the English calls by Greek or Latin names, so the orders of
sanctity, the ranks of the Typikon, the estates and the ages are given as
the Romanian Church gives them: Cuvios for the monastic saint, Sfintit
Mucenic for the hieromartyr, Nebun pentru Hristos for the fool. Greek,
Slavic, Georgian and Latin place-names take the forms Romanian usage has
received - Constantinopol, Tesalonic, Nicomidia, Chiev - and where no
received form exists the name is transliterated.

Diacritics are written in full: a with breve, a and i with circumflex, s and
t with comma below.

The keys are the phrases exactly as the index writes them, so a rendering
cannot quietly attach itself to the wrong saint.
"""
TEXT = {}


# The orders of sanctity, as the badge on a card names them.
TEXT.update({
    "Angelic": "Puteri netrupești",
    "Apostle": "Apostol",
    "Confessor": "Mărturisitor",
    "Equal-to-the-Apostles": "Întocmai cu Apostolii",
    "Feast": "Praznic",
    "Fool-for-Christ": "Nebun pentru Hristos",
    "Great Martyr": "Mare Mucenic",
    "Hierarch": "Ierarh",
    "Hieromartyr": "Sfințit Mucenic",
    "Martyr": "Mucenic",
    "Monastic": "Cuvios",
    "New Martyr": "Mucenic Nou",
    "Other": "Altele",
    "Passion-bearer": "Purtător de patimi",
    "Prophet": "Prooroc",
    "Righteous": "Drept",
    "Unmercenary": "Doctor fără de arginți",
    "Virgin Martyr": "Muceniță fecioară",
})


# The attributes a life is marked with.
TEXT.update({
    "Church Father": "Părinte al Bisericii",
    "Desert ascetic": "Nevoitor al pustiei",
    "Enlightener": "Luminător",
    "Healing intercessor": "Tămăduitor",
    "Hymnographer": "Imnograf",
    "Iconographer": "Iconar",
    "Incorrupt relics": "Moaște nestricate",
    "Monastery founder": "Ctitor de mănăstire",
    "Myrrh-bearer": "Mironosiță",
    "Myrrh-streaming": "Izvorâtor de mir",
    "New martyr": "Mucenic nou",
    "Ruler or royal": "Domnitor sau din neam domnesc",
    "Stylite": "Stâlpnic",
    "Warrior saint": "Sfânt ostaș",
    "Wonderworker": "Făcător de minuni",
})


# The ranks the Typikon gives a feast.
TEXT.update({
    "Doxology": "Doxologie",
    "Great Feast": "Praznic împărătesc",
    "Polyeleos": "Polieleu",
    "Simple": "Simplă",
    "Vigil": "Priveghere",
})


# The jurisdictions whose calendars the index keeps.
TEXT.update({
    "Antiochian": "Antiohian",
    "Greek": "Grec",
    "OCA": "OCA",
    "Romanian": "Român",
    "Russian": "Rus",
    "Serbian": "Sârb",
    "Ukrainian": "Ucrainean",
})


# The estate a saint stood in.
TEXT.update({
    "Apostolic": "Apostolic",
    "Clergy": "Cler",
    "Laity": "Mireni",
    "Layman": "Mirean",
    "Laywoman": "Mireancă",
    "Laywomen": "Mirence",
    "Married": "Căsătorit",
    "Military": "Ostășesc",
    "Monastic": "Monahal",
    "Prophet": "Prooroc",
    "Royal": "Domnesc",
    "Royalty": "Neam domnesc",
    "Unknown": "Necunoscut",
    "Unmarried": "Necăsătorit",
    "Widowed": "Văduv",
})


# The ages the lives are set in.
TEXT.update({
    "Age of the Celtic Saints": "Veacul sfinților celți",
    "Age of the Ecumenical Councils": "Veacul Sinoadelor Ecumenice",
    "Age of the Martyrs": "Veacul mucenicilor",
    "Apostolic Age": "Veacul apostolic",
    "Byzantine": "Bizantin",
    "Byzantine Balkans": "Balcanii bizantini",
    "Byzantine Era": "Epoca bizantină",
    "Byzantine Iconoclasm": "Iconoclasmul bizantin",
    "Cossack Era": "Epoca cazacilor",
    "Desert Fathers": "Părinții pustiei",
    "Early Medieval West": "Apusul medieval timpuriu",
    "Imperial Russia": "Rusia imperială",
    "Kievan Rus'": "Rusia Chieveană",
    "Medieval Georgia": "Georgia medievală",
    "Medieval Rus'": "Rusia medievală",
    "Medieval Serbia": "Serbia medievală",
    "Modern": "Modern",
    "Modern Era": "Epoca modernă",
    "Muscovite Russia": "Rusia moscovită",
    "Old Testament": "Vechiul Testament",
    "Ottoman Balkans": "Balcanii otomani",
    "Ottoman Era": "Epoca otomană",
    "Ottoman period": "Perioada otomană",
    "Polish-Lithuanian period": "Perioada polono-lituaniană",
    "Soviet Era": "Epoca sovietică",
    "Soviet period": "Perioada sovietică",
    "Synodal Russia": "Rusia sinodală",
})


# The one movable commemoration the index names.
TEXT.update({
    "Sunday of the Holy Forefathers": "Duminica Sfinților Strămoși",
})


# The countries and the regions.
TEXT.update({
    "Aegean": "Marea Egee",
    "America": "America",
    "Arabia": "Arabia",
    "Armenia": "Armenia",
    "Asia Minor": "Asia Mică",
    "Balkans": "Balcani",
    "Belarus": "Belarus",
    "Bithynia": "Bitinia",
    "Britain": "Britania",
    "British Isles": "Insulele Britanice",
    "Bulgaria": "Bulgaria",
    "Cappadocia": "Capadocia",
    "Cilicia": "Cilicia",
    "Constantinople": "Constantinopol",
    "Crimea": "Crimeea",
    "Cyprus": "Cipru",
    "Czech Lands": "Țările Cehe",
    "Dalmatia": "Dalmația",
    "Danube lands": "Ținuturile Dunării",
    "Egypt": "Egipt",
    "England": "Anglia",
    "Ethiopia": "Etiopia",
    "Gaul": "Galia",
    "Georgia": "Georgia",
    "Greece": "Grecia",
    "Holy Land": "Țara Sfântă",
    "Illyria": "Iliria",
    "Illyricum": "Iliric",
    "India": "India",
    "Ireland": "Irlanda",
    "Italy": "Italia",
    "Lithuania": "Lituania",
    "Macedonia": "Macedonia",
    "Mesopotamia": "Mesopotamia",
    "Moldavia": "Moldova",
    "Montenegro": "Muntenegru",
    "Moravia": "Moravia",
    "Mount Athos": "Muntele Athos",
    "North Africa": "Africa de Nord",
    "North America": "America de Nord",
    "North Macedonia": "Macedonia de Nord",
    "Palestine": "Palestina",
    "Persia": "Persia",
    "Phoenicia": "Fenicia",
    "Poland": "Polonia",
    "Pontus": "Pont",
    "Romania": "România",
    "Rome": "Roma",
    "Russia": "Rusia",
    "Scythia": "Scitia",
    "Serbia": "Serbia",
    "Siberia": "Siberia",
    "Sinai": "Sinai",
    "Spain": "Spania",
    "Syria": "Siria",
    "Thrace": "Tracia",
    "Ukraine": "Ucraina",
    "Western Rus": "Rusia apuseană",
})


# The places, which are not a list but a grammar: a card names a town, a
# province and a country in one line, and the same town appears on twenty
# other cards inside a different line. The pieces are rendered once here and
# the wholes are assembled from them, so a town cannot be spelled one way on
# one card and another way on the next.
PARTS = {}

def expand(phrases):
    """The compounds, assembled from the parts above."""
    out = {}
    for p in phrases:
        bits = p.split(", ")
        if all(b in PARTS for b in bits):
            out[p] = ", ".join(PARTS[b] for b in bits)
    return out


# The lands the fasting rule is kept in.
TEXT.update({
    "Albania": "Albania",
    "Bohemia": "Boemia",
    "China": "China",
    "France": "Franța",
    "Judah": "Iuda",
    "Moesia": "Moesia",
    "Sicily": "Sicilia",
    "United States": "Statele Unite",
})


# The rank a saint is given.
TEXT.update({
    "Abbess": "Stareță",
    "Abbot (Archimandrite)": "Stareț (Arhimandrit)",
    "Abbot (Founder)": "Stareț (Ctitor)",
    "Abbot (Igumen)": "Stareț (Egumen)",
    "Abbot (Igumen), Confessor": "Stareț (Egumen), Mărturisitor",
    "Abbot (Igumen), Hieromartyr": "Stareț (Egumen), Sfințit Mucenic",
    "Abbot (Igumen), Martyr": "Stareț (Egumen), Mucenic",
    "Abbot (Igumen), Monastic Martyr": "Stareț (Egumen), Cuvios Mucenic",
    "Abbot, Confessor": "Stareț, Mărturisitor",
    "Abbot, Confessor-Martyr": "Stareț, Mărturisitor și Mucenic",
    "Abbot, Priest": "Stareț, Preot",
    "Abbots": "Stareți",
    "Anchorite": "Sihastru",
    "Apostle of the Seventy": "Apostol din cei Șaptezeci",
    "Apostle of the Seventy, Bishop": "Apostol din cei Șaptezeci, Episcop",
    "Apostle of the Seventy, Martyr": "Apostol din cei Șaptezeci, Mucenic",
    "Apostle, Evangelist": "Apostol, Evanghelist",
    "Apostle, Martyr": "Apostol, Mucenic",
    "Apostles": "Apostoli",
    "Apostles of the Seventy": "Apostoli din cei Șaptezeci",
    "Apostles of the Seventy, Martyrs": "Apostoli din cei Șaptezeci, Mucenici",
    "Archangel": "Arhanghel",
    "Archbishop": "Arhiepiscop",
    "Archbishop, Confessor": "Arhiepiscop, Mărturisitor",
    "Archbishop, Equal-to-the-Apostles": "Arhiepiscop, Întocmai cu Apostolii",
    "Archdeacon": "Arhidiacon",
    "Archimandrite": "Arhimandrit",
    "Bishop": "Episcop",
    "Bishop, Church Father": "Episcop, Părinte al Bisericii",
    "Bishop, Confessor": "Episcop, Mărturisitor",
    "Bishop, Equal-to-the-Apostles": "Episcop, Întocmai cu Apostolii",
    "Bishop, Hieromartyr": "Episcop, Sfințit Mucenic",
    "Bishop, Monk": "Episcop, Monah",
    "Bishops": "Episcopi",
    "Blessed Eldress": "Fericita Maică duhovnicească",
    "Chamberlain (cubicularius)": "Cubicular (cubicularius)",
    "Childmartyr": "Prunc mucenic",
    "Commander": "Comandant",
    "Confessor, Archpriest": "Mărturisitor, Protoiereu",
    "Deacon": "Diacon",
    "Deacon, Monk-martyr": "Diacon, Cuvios Mucenic",
    "Deaconess": "Diaconiță",
    "Deaconess and Martyr": "Diaconiță și Muceniță",
    "Elder": "Stareț",
    "Empress": "Împărăteasă",
    "Equal-to-the-Apostles, Emperor": "Întocmai cu Apostolii, Împărat",
    "Equals-to-the-Apostles": "Întocmai cu Apostolii",
    "Grand Duchess": "Mare Ducesă",
    "Grand Prince": "Mare Cneaz",
    "Grand Princess": "Mare Cneaghină",
    "Great Martyr, Equal-to-the-Apostles": "Mare Mucenic, Întocmai cu Apostolii",
    "Great Prince, Martyr": "Mare Cneaz, Mucenic",
    "Great-martyr": "Mare Mucenic",
    "Great-martyr, Prince": "Mare Mucenic, Cneaz",
    "Hermit": "Pustnic",
    "Hermits": "Pustnici",
    "Hierarchs": "Ierarhi",
    "Hieromartyr (Hermit)": "Sfințit Mucenic (Pustnic)",
    "Hieromartyr, Apostle": "Sfințit Mucenic, Apostol",
    "Hieromartyr, Archbishop": "Sfințit Mucenic, Arhiepiscop",
    "Hieromartyr, Archimandrite": "Sfințit Mucenic, Arhimandrit",
    "Hieromartyr, Archpriest": "Sfințit Mucenic, Protoiereu",
    "Hieromartyr, Bishop": "Sfințit Mucenic, Episcop",
    "Hieromartyr, Confessor": "Sfințit Mucenic, Mărturisitor",
    "Hieromartyr, Deacon": "Sfințit Mucenic, Diacon",
    "Hieromartyr, Patriarch": "Sfințit Mucenic, Patriarh",
    "Hieromartyr, Pope": "Sfințit Mucenic, Papă",
    "Hieromartyr, and his son": "Sfințit Mucenic, și fiul său",
    "Hieromartyrs": "Sfințiți Mucenici",
    "Hieromonk": "Ieromonah",
    "Hieroschemamonk": "Ieroschimonah",
    "High Priest": "Arhiereu",
    "Icon of the Mother of God": "Icoana Maicii Domnului",
    "King and Martyr": "Rege și Mucenic",
    "King and Prophet": "Rege și Prooroc",
    "Laymen": "Mireni",
    "Martyrs": "Mucenici",
    "Master Builders, Monks": "Meșteri zidari, Monahi",
    "Metropolitan": "Mitropolit",
    "Metropolitan, Equal-to-the-Apostles": "Mitropolit, Întocmai cu Apostolii",
    "Monastic Martyr": "Cuvios Mucenic",
    "Monastic Martyrs": "Cuvioși Mucenici",
    "Monastic New Martyr": "Cuvios Mucenic Nou",
    "Monastics": "Cuvioși",
    "Monk": "Monah",
    "Monk (Founder)": "Monah (Ctitor)",
    "Monk (Hermit)": "Monah (Pustnic)",
    "Monk (elder)": "Monah (stareț)",
    "Monk (hermit)": "Monah (pustnic)",
    "Monk (novice)": "Monah (novice)",
    "Monk (recluse)": "Monah (zăvorât)",
    "Monk (stylite)": "Monah (stâlpnic)",
    "Monk, Church Father": "Monah, Părinte al Bisericii",
    "Monk, Confessor": "Monah, Mărturisitor",
    "Monk, Elder": "Monah, Stareț",
    "Monk, Hymnographer": "Monah, Imnograf",
    "Monk, Martyr": "Monah, Mucenic",
    "Monk, Recluse": "Monah, Zăvorât",
    "Monk, Unmercenary Physician": "Monah, Doctor fără de arginți",
    "Monk, former Great Zhupan": "Monah, fost Mare Jupan",
    "Monk-martyr": "Cuvios Mucenic",
    "Monk-martyrs": "Cuvioși Mucenici",
    "Monks": "Monahi",
    "Monks (Founders)": "Monahi (Ctitori)",
    "Mother": "Maică",
    "Myrrhbearer": "Mironosiță",
    "New Martyrs": "Mucenici Noi",
    "New Martyrs and Confessors": "Mucenici Noi și Mărturisitori",
    "Nun": "Monahie",
    "Nun-martyr": "Cuvioasă Muceniță",
    "Patriarch": "Patriarh",
    "Patriarch, Church Father": "Patriarh, Părinte al Bisericii",
    "Patriarch, Confessor": "Patriarh, Mărturisitor",
    "Patriarch, Hieromartyr": "Patriarh, Sfințit Mucenic",
    "Physician": "Doctor",
    "Physicians": "Doctori",
    "Pope": "Papă",
    "Pope of Rome, Confessor": "Papă al Romei, Mărturisitor",
    "Presbyter and Deacon": "Preot și Diacon",
    "Presbyters, Confessors": "Preoți, Mărturisitori",
    "Priest": "Preot",
    "Prince": "Cneaz",
    "Prince of Moldavia": "Domn al Moldovei",
    "Prince, Passion-Bearer": "Cneaz, Purtător de patimi",
    "Princes": "Cneji",
    "Princess": "Cneaghină",
    "Princess, Nun": "Cneaghină, Monahie",
    "Proconsul (military commander)": "Proconsul (comandant de oaste)",
    "Prophet and Forerunner": "Prooroc și Înaintemergător",
    "Prophetess": "Proorociță",
    "Protomartyr": "Întâiul Mucenic",
    "Protopresbyter": "Protopresbiter",
    "Recluse": "Zăvorât",
    "Right-believing Prince": "Binecredinciosul Cneaz",
    "Right-believing Prince (Monk)": "Binecredinciosul Cneaz (Monah)",
    "Right-believing Prince and Princess": "Binecredincioșii Cneaz și Cneaghină",
    "Right-believing Prince, Passion-bearer": "Binecredinciosul Cneaz, Purtător de patimi",
    "Right-believing Princess (Nun)": "Binecredincioasa Cneaghină (Monahie)",
    "Right-believing Princess, Martyr": "Binecredincioasa Cneaghină, Muceniță",
    "Righteous (Child)": "Drept (Prunc)",
    "Righteous (Children)": "Drepți (Prunci)",
    "Righteous (Unmercenary)": "Drept (Doctor fără de arginți)",
    "Righteous Forefather": "Drept Strămoș",
    "Righteous Virgin": "Dreapta Fecioară",
    "Righteous, Priest": "Drept, Preot",
    "Roman soldier": "Ostaș roman",
    "Schemamonk": "Schimonah",
    "Synaxis": "Sobor",
    "Tsar and Imperial Family": "Țar și Familia Imperială",
    "Unmercenary Martyrs": "Mucenici doctori fără de arginți",
    "Venerable": "Cuvios",
    "Venerable Prince": "Cuviosul Cneaz",
    "Venerable Princess": "Cuvioasa Cneaghină",
    "Virgin": "Fecioară",
    "Virgin Martyrs": "Mucenițe fecioare",
    "Virgin-martyr": "Muceniță fecioară",
    "Youths": "Tineri",
})
