# -*- coding: utf-8 -*-
"""Greek for the vocabulary that stands beside the lives.

TEXT = {the phrase the index shows: the Greek}. PARTS holds the pieces the
compound place-names are built from, and expand() assembles the wholes, so a
town cannot be spelled one way on one card and another way on the next.

Greek is the tongue the greater part of this vocabulary was first said in,
and where that is so the phrase goes home rather than being carried across:
the orders of sanctity, the ranks of the Typikon, the ancient sees and the
provinces of the Christian East are given as the Greek Church gives them,
not as renderings of the English renderings of them. The Slavic, Georgian
and Latin names take the forms the Greek synaxaria have received, and where
no received form exists the name is transliterated.

The keys are the phrases exactly as the index writes them, so a rendering
cannot quietly attach itself to the wrong saint.
"""
TEXT = {}



# The orders of sanctity, as the badge on a card names them.
TEXT.update({
    "Angelic": "Ασώματοι Δυνάμεις",
    "Apostle": "Απόστολος",
    "Confessor": "Ομολογητής",
    "Equal-to-the-Apostles": "Ισαπόστολος",
    "Feast": "Εορτή",
    "Fool-for-Christ": "Διά Χριστόν σαλός",
    "Great Martyr": "Μεγαλομάρτυς",
    "Hierarch": "Ιεράρχης",
    "Hieromartyr": "Ιερομάρτυς",
    "Martyr": "Μάρτυς",
    "Monastic": "Όσιος",
    "New Martyr": "Νεομάρτυς",
    "Other": "Άλλο",
    "Passion-bearer": "Παθοφόρος",
    "Prophet": "Προφήτης",
    "Righteous": "Δίκαιος",
    "Unmercenary": "Ανάργυρος",
    "Virgin Martyr": "Παρθενομάρτυς",
})


# The attributes a life is marked with.
TEXT.update({
    "Apostle": "Απόστολος",
    "Church Father": "Πατήρ της Εκκλησίας",
    "Confessor": "Ομολογητής",
    "Desert ascetic": "Ασκητής της ερήμου",
    "Enlightener": "Φωτιστής",
    "Fool-for-Christ": "Διά Χριστόν σαλός",
    "Healing intercessor": "Ιαματικός",
    "Hymnographer": "Υμνογράφος",
    "Iconographer": "Αγιογράφος",
    "Incorrupt relics": "Άφθαρτα λείψανα",
    "Monastery founder": "Κτίτωρ μονής",
    "Myrrh-bearer": "Μυροφόρος",
    "Myrrh-streaming": "Μυροβλύτης",
    "New martyr": "Νεομάρτυς",
    "Passion-bearer": "Παθοφόρος",
    "Prophet": "Προφήτης",
    "Ruler or royal": "Ηγεμών ή βασιλικού γένους",
    "Stylite": "Στυλίτης",
    "Unmercenary": "Ανάργυρος",
    "Warrior saint": "Στρατιωτικός άγιος",
    "Wonderworker": "Θαυματουργός",
})


# The ranks the Typikon gives a feast.
TEXT.update({
    "Doxology": "Δοξολογία",
    "Great Feast": "Μεγάλη εορτή",
    "Polyeleos": "Πολυέλεος",
    "Simple": "Απλή",
    "Vigil": "Αγρυπνία",
})


# The jurisdictions whose calendars the index keeps.
TEXT.update({
    "Antiochian": "Αντιοχειανή",
    "Greek": "Ελληνική",
    "OCA": "ΟΕΑ",
    "Romanian": "Ρουμανική",
    "Russian": "Ρωσική",
    "Serbian": "Σερβική",
    "Ukrainian": "Ουκρανική",
})


# The estate a saint stood in.
TEXT.update({
    "Apostolic": "Αποστολική",
    "Clergy": "Κλήρος",
    "Laity": "Λαϊκοί",
    "Layman": "Λαϊκός",
    "Laywoman": "Λαϊκή",
    "Laywomen": "Λαϊκές",
    "Married": "Έγγαμος βίος",
    "Military": "Στρατιωτικός",
    "Monastic": "Μοναχικός",
    "Prophet": "Προφήτης",
    "Royal": "Βασιλικό",
    "Royalty": "Βασιλικό γένος",
    "Unknown": "Άγνωστο",
    "Unmarried": "Αγαμία",
    "Widowed": "Χηρεία",
})


# The ages the lives are set in.
TEXT.update({
    "Age of the Celtic Saints": "Εποχή των Κελτών αγίων",
    "Age of the Ecumenical Councils": "Εποχή των Οικουμενικών Συνόδων",
    "Age of the Martyrs": "Εποχή των Μαρτύρων",
    "Apostolic Age": "Αποστολική εποχή",
    "Byzantine": "Βυζαντινή",
    "Byzantine Balkans": "Βυζαντινά Βαλκάνια",
    "Byzantine Era": "Βυζαντινή εποχή",
    "Byzantine Iconoclasm": "Βυζαντινή εικονομαχία",
    "Cossack Era": "Εποχή των Κοζάκων",
    "Desert Fathers": "Πατέρες της ερήμου",
    "Early Medieval West": "Πρώιμη μεσαιωνική Δύση",
    "Imperial Russia": "Αυτοκρατορική Ρωσία",
    "Kievan Rus'": "Ρωσία του Κιέβου",
    "Medieval Georgia": "Μεσαιωνική Γεωργία",
    "Medieval Rus'": "Μεσαιωνική Ρωσία",
    "Medieval Serbia": "Μεσαιωνική Σερβία",
    "Modern": "Νεότερη",
    "Modern Era": "Νεότερη εποχή",
    "Muscovite Russia": "Ρωσία της Μόσχας",
    "Old Testament": "Παλαιά Διαθήκη",
    "Ottoman Balkans": "Οθωμανικά Βαλκάνια",
    "Ottoman Era": "Οθωμανική εποχή",
    "Ottoman period": "Οθωμανική περίοδος",
    "Polish-Lithuanian period": "Πολωνολιθουανική περίοδος",
    "Soviet Era": "Σοβιετική εποχή",
    "Soviet period": "Σοβιετική περίοδος",
    "Synodal Russia": "Συνοδική Ρωσία",
})


# The countries and the regions.
TEXT.update({
    "Aegean": "Αιγαίο",
    "Albania": "Αλβανία",
    "America": "Αμερική",
    "Arabia": "Αραβία",
    "Armenia": "Αρμενία",
    "Asia Minor": "Μικρά Ασία",
    "Balkans": "Βαλκάνια",
    "Belarus": "Λευκορωσία",
    "Bithynia": "Βιθυνία",
    "Bohemia": "Βοημία",
    "Britain": "Βρετανία",
    "British Isles": "Βρετανικές Νήσοι",
    "Bulgaria": "Βουλγαρία",
    "Cappadocia": "Καππαδοκία",
    "China": "Κίνα",
    "Cilicia": "Κιλικία",
    "Constantinople": "Κωνσταντινούπολη",
    "Crimea": "Κριμαία",
    "Cyprus": "Κύπρος",
    "Czech Lands": "Τσεχικές χώρες",
    "Dalmatia": "Δαλματία",
    "Danube lands": "Παραδουνάβιες χώρες",
    "Egypt": "Αίγυπτος",
    "England": "Αγγλία",
    "Ethiopia": "Αιθιοπία",
    "France": "Γαλλία",
    "Gaul": "Γαλατία",
    "Georgia": "Γεωργία",
    "Greece": "Ελλάδα",
    "Holy Land": "Άγιοι Τόποι",
    "Illyria": "Ιλλυρία",
    "Illyricum": "Ιλλυρικό",
    "India": "Ινδία",
    "Ireland": "Ιρλανδία",
    "Italy": "Ιταλία",
    "Judah": "Ιουδαία",
    "Lithuania": "Λιθουανία",
    "Macedonia": "Μακεδονία",
    "Mesopotamia": "Μεσοποταμία",
    "Moesia": "Μοισία",
    "Moldavia": "Μολδαβία",
    "Montenegro": "Μαυροβούνιο",
    "Moravia": "Μοραβία",
    "Mount Athos": "Άγιον Όρος",
    "North Africa": "Βόρεια Αφρική",
    "North America": "Βόρεια Αμερική",
    "North Macedonia": "Βόρεια Μακεδονία",
    "Palestine": "Παλαιστίνη",
    "Persia": "Περσία",
    "Phoenicia": "Φοινίκη",
    "Poland": "Πολωνία",
    "Pontus": "Πόντος",
    "Romania": "Ρουμανία",
    "Rome": "Ρώμη",
    "Russia": "Ρωσία",
    "Scythia": "Σκυθία",
    "Serbia": "Σερβία",
    "Siberia": "Σιβηρία",
    "Sicily": "Σικελία",
    "Sinai": "Σινά",
    "Spain": "Ισπανία",
    "Syria": "Συρία",
    "Thrace": "Θράκη",
    "Ukraine": "Ουκρανία",
    "United States": "Ηνωμένες Πολιτείες",
    "Western Rus": "Δυτική Ρωσία",
})


# The one movable commemoration the index names.
TEXT.update({
    "Sunday of the Holy Forefathers": "Κυριακή των Αγίων Προπατόρων",
})
