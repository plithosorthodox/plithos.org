# -*- coding: utf-8 -*-
"""The rows in Greek.

Gathered from what the site already publishes in Greek, where the sees are
named on nearly every page of the calendar: Κωνσταντινουπόλεως,
Αλεξανδρείας, Αντιοχείας, Ιεροσολύμων, Μόσχας, Αθηνών, Δαμασκού.

Three forms had a rival and were settled by counting the Greek corpus:

  - Κωνσταντινούπολη 128, Κωνσταντινούπολις 60. The demotic form wins, and
    it is the register the rest of this page speaks in. Ισταμπούλ is not
    written here once.
  - Αθήνα 110, Αθήναι 80. Demotic again.
  - Ιεροσόλυμα 308, Ιερουσαλήμ 411. The larger number is the scriptural
    name, which stands in Holy Scripture and in the hymns; the city is
    Ιεροσόλυμα, and a seat is a city.

Τίρανα and Τόκιο are the two the Greek here has never had occasion to
write. They are set down in their received Greek form.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Greek this site publishes and are
taken whole - Οικουμενικό Πατριαρχείο, written 52 times, and the Ρωσική,
Σερβική, Ρουμανική and Ουκρανική Ορθόδοξη Εκκλησία of the commemorations.

The three ancient sees are set in the demotic Πατριαρχείο, 156 against 66 for
Πατριαρχείον, which is the register the rest of this file speaks in, with the
see in the genitive the calendar already writes. Πατριαρχείο Βουλγαρίας
follows Πατριαρχείο Σερβίας, which is how the site names that patriarchate,
and πάσης Ανατολής follows the πάσης Ρωσίας of the patriarch of Moscow.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and Greek does not say it of
itself. Those two are Πατριαρχείο Αντιοχείας και πάσης Ανατολής and
Πατριαρχείο Ιεροσολύμων, which is what they call themselves in Greek.
"""
NAMES = {
    "constantinople": u"Η Εκκλησία της Κωνσταντινουπόλεως",
    "alexandria": u"Η Εκκλησία της Αλεξανδρείας",
    "antioch": u"Η Εκκλησία της Αντιοχείας",
    "jerusalem": u"Η Εκκλησία των Ιεροσολύμων",
    "russia": u"Η Εκκλησία της Ρωσίας",
    "georgia": u"Η Εκκλησία της Γεωργίας",
    "serbia": u"Η Εκκλησία της Σερβίας",
    "romania": u"Η Εκκλησία της Ρουμανίας",
    "bulgaria": u"Η Εκκλησία της Βουλγαρίας",
    "cyprus": u"Η Εκκλησία της Κύπρου",
    "greece": u"Η Εκκλησία της Ελλάδος",
    "albania": u"Η Εκκλησία της Αλβανίας",
    "poland": u"Η Εκκλησία της Πολωνίας",
    "czech-slovakia": u"Η Εκκλησία των Τσεχικών Χωρών και της Σλοβακίας",
    "oca": u"Η Ορθόδοξη Εκκλησία στην Αμερική",
    "macedonia": u"Η Μακεδονική Ορθόδοξη Εκκλησία - Αρχιεπισκοπή Αχρίδος",
    "ukraine-uoc": u"Η Εκκλησία της Ουκρανίας",
    "ukraine-ocu": u"Ορθόδοξη Εκκλησία της Ουκρανίας",
    "sinai": u"Η Εκκλησία του Σινά",
    "finland": u"Η Αυτόνομη Εκκλησία της Φινλανδίας",
    "japan": u"Η Εκκλησία της Ιαπωνίας",
    "estonia-eaok": u"Ορθόδοξη Εκκλησία της Εσθονίας",
}
SEATS = {
    "Istanbul": u"Κωνσταντινούπολη",
    "Alexandria": u"Αλεξάνδρεια",
    "Damascus": u"Δαμασκός",
    "Jerusalem": u"Ιεροσόλυμα",
    "Moscow": u"Μόσχα",
    "Tbilisi": u"Τιφλίδα",
    "Belgrade": u"Βελιγράδι",
    "Bucharest": u"Βουκουρέστι",
    "Sofia": u"Σόφια",
    "Nicosia": u"Λευκωσία",
    "Athens": u"Αθήνα",
    "Tirana": u"Τίρανα",
    "Warsaw": u"Βαρσοβία",
    "Prešov": u"Πρέσοβ",
    "Syosset, New York": u"Σύοσετ, Νέα Υόρκη",
    "Skopje": u"Σκόπια",
    "Kyiv": u"Κίεβο",
    "Mount Sinai": u"Όρος Σινά",
    "Helsinki": u"Ελσίνκι",
    "Tokyo": u"Τόκιο",
    "Tallinn": u"Ταλίν",
}
STYLED = {
    "constantinople": u"Οικουμενικό Πατριαρχείο",
    "alexandria": u"Πατριαρχείο Αλεξανδρείας",
    "antioch": u"Πατριαρχείο Αντιοχείας και πάσης Ανατολής",
    "jerusalem": u"Πατριαρχείο Ιεροσολύμων",
    "russia": u"Ρωσική Ορθόδοξη Εκκλησία",
    "serbia": u"Σερβική Ορθόδοξη Εκκλησία",
    "romania": u"Ρουμανική Ορθόδοξη Εκκλησία",
    "bulgaria": u"Βουλγαρική Ορθόδοξη Εκκλησία - Πατριαρχείο Βουλγαρίας",
    "ukraine-uoc": u"Ουκρανική Ορθόδοξη Εκκλησία",
}
