# -*- coding: utf-8 -*-
"""The 45 metropolises and dioceses of the Patriarchate of Alexandria.

The jurisdiction is the whole of Africa, and these are the hardest rows on
this directory for a reader to find anywhere else. They are read from the
Patriarchate's own two lists - the metropolises of the Patriarchal Throne
and the dioceses of the Patriarchal Throne - and from the page it publishes
for each see.

THE COUNT, AND WHERE THE CHURCH STATES IT

Counted again on 14 September 2026 against the roll the Patriarchate
publishes of the Hierarchy of the Throne, which is the Church speaking about
itself rather than a page of links. The roll numbers 29 Metropolitans of
sees and 16 diocesan Bishops, two of the sixteen standing vacant, and the
two lists of links carry the same 29 and the same 16. Forty-five, three ways,
and forty-five rows. Nothing was found missing and nothing here is not a see.

Four other kinds of hierarch stand on that roll and none of them is a row: a
titular Metropolitan of Tamiathis, five auxiliary Bishops, four retired, and
the Patriarch himself, whose own see is the Most Holy Archdiocese of
Alexandria and is the Church's own row. The Patriarchate also publishes two
Patriarchal Vicariates under its administrative organisation, Alexandria and
Cairo. The first is that Archdiocese under another name; the second
administers the parishes of Cairo under the Patriarch directly. Neither is a
see, neither stands on the roll, and neither has a row.

Five sees with no link of their own print an address somewhere on their
page. Four of them were tried again on 14 September 2026 over both http and
https and did not answer at all - Tanzania for Irinopolis, Ptolemais, Congo
for Brazzaville and Gabon, and Kisumu - and the fifth is a blog kept in a
bishop's own name, which is not a diocese's door. Those rows go on falling
back to the Patriarchate, which does answer.

Each see has two pages, one Greek and one English. They are not the same
page. The Greek is the maintained one: it carries a modification date, and
on a dozen sees it carries a name or an address the English has not caught
up with - the Metropolis of Libya is still headed Botswana in English, the
Metropolis of Diospolis still Cameroon, Zambia and Mozambique still Zambia
alone. So every row here is read from the Greek page, which is also the
canonical one the site declares, and the English page is cited beside it
where the two name the same see. `local` is the title as the Greek page
sets it.

Sixteen sees have no website of their own that answered from here, and
seven that the Patriarchate prints did not answer at all; those rows carry
the Patriarchate's page, which is the level a reader can still get
somewhere from. Three answered and are linked: Nigeria, Zimbabwe and
Angola, and Bunia and Kisangani.

Where the Patriarchate prints no seat - four of the Egyptian sees, whose
address is the Patriarchate's own post office box in Alexandria - the row
carries none. A see this site can name and point at is worth a row without
one.


RANK, ADDED 14 SEPTEMBER 2026. Every row here already carried the Church's own
word for what the body is, inside the name its own list prints - Holy Metropolis, Holy Archdiocese, Holy Diocese -
and `rank` now says it in a field of its own so a reader can see it and a
filter can use it. Nothing was read again for this and nothing was guessed: a
row whose list gives it no such word carries no rank.
"""

AX = "https://www.patriarchateofalexandria.com/archdioceses/"
AX_M = ("https://www.patriarchateofalexandria.com/archdiocese_category/"
        "mitropoleis-patriarxikou-thronou/")
AX_D = ("https://www.patriarchateofalexandria.com/archdiocese_category/"
        "episkopes-patriarxikou-thronou/")

ROWS = [
 # ------------------------------------------- metropolises of the Throne
 dict(id="ax-caesarea", parent="alexandria",
      name="Holy Metropolis of Caesarea",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΙΣ ΚΑΙΣΑΡΕΙΑΣ",
      country="EG", checked="2026-09-14",
      address=["P.O. Box 2006, Alexandria Egypt."],
      founded=[(
        u"Η Ιερά Μητρόπολη Καισαρείας καταγράφεται στους ιστορικούς δέλτους "
        u"από τα έτη της βασιλείας του Αυτοκράτορος Ιουστινιανού του Μεγάλου "
        u"(6ος αι.μΧ), ως εξέχουσα εκκλησιαστική Επαρχία του Αποστολικού "
        u"Θρόνου Αλεξανδρείας, κειμένη στα εδάφη του τότε ενδόξου Βερβερικού "
        u"Βασιλείου της Νουμιδίας, στην Βόρειο Αφρική"),
       (
        u"Διά του Πατριαρχικού και Συνοδικού Τόμου της 15ης Φεβρουαρίου 2024 "
        u"ανεσυστάθη ως εν ενεργεία Ιερά Μητρόπολη του Πρεσβυγενούς "
        u"Πατριαρχείου Αλεξανδρείας")],
      sources=[AX + "era-mitropolis-kaisareias/", AX_M]),

 dict(id="ax-accra", parent="alexandria",
      name="Holy Archdiocese of Accra",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΑΚΚΡΑΣ",
      seat="Accra", country="GH",
      address=["Orthodox Church Ghana, V271 Flower Str, Abeka Lapaz, Accra, Ghana (P.O. Box LG 274. Legon-Accra, Ghana)."],
      sources=[AX + "iera-mitropoli-akkras/",
               AX + "holy-archdiocese-of-accra/?lang=en"]),

 dict(id="ax-aksum", parent="alexandria",
      name="Holy Archdiocese of Aksum",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΑΞΩΜΗΣ",
      seat="Addis Ababa", country="ET",
      address=["P.O. Box 571, Addis-Ababa, Ethiopia."],
      sources=[AX + "iera-mitropoli-axomis/",
               AX + "holy-archdiocese-of-aksum/?lang=en"]),

 dict(id="ax-antananarivo", parent="alexandria",
      name="Holy Archdiocese of Antananarivo and North Madagascar",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΑΝΤΑΝΑΝΑΡΙΒΟ ΚΑΙ ΒΟΡΕΙΟΥ ΜΑΔΑΓΑΣΚΑΡΗΣ",
      seat="Antananarivo", country="MG",
      address=["B.P. 456, Antananarivo 101 - Madagascar."],
      checked="2026-09-14",
      founded=[(
        u"Η Ιερά Μητρόπολη Μαδαγασκάρης ιδρύθη διά Πατριαρχικού και "
        u"Συνοδικού Τόμου την 23η Σεπτεμβρίου 1997"),
       (
        u"Την 21 Νοεμβρίου 2012 ανυψώθη δια Πατριαρχικού και Συνοδικού Τόμου "
        u"σε Μητρόπολη")],
      sources=[AX + "iera-mitropoli-antananarivo-kai-voreioy-madagaskaris/",
               AX + "holy-archdiocese-of-antananarivo-and-north-madagascar/?lang=en"]),

 dict(id="ax-libya", parent="alexandria",
      name="Holy Metropolis of Libya",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΛΙΒΥΗΣ",
      seat="Tripoli", country="LY",
      address=["Saint Mary's Square, Old Town, Metropolitan Church of Saint George of the Slaves"],
      checked="2026-09-14",
      founded=[(
        u"Η Ιερά Μητρόπολη Λιβύης είναι σήμερα η έως την 15η Φεβρουαρίου "
        u"2024 Ιερά Μητρόπολη Tριπόλεως, η οποία ιδρύθη διά Πατριαρχικού και "
        u"Συνοδικού Τόμου το έτος 1866"),
       u"Το έτος 1959 συνεχωνεύθη με την Ιερά Μητρόπολη Καρθαγένης",
       (
        u"Την 27η Οκτωβρίου 2004 ανεσυστήθη εκ νέου διά Πατριαρχικού και "
        u"Συνοδικού Τόμου"),
       (
        u"Διά του Πατριαρχικού και Συνοδικού Τόμου της 15ης Φεβρουαρίου 2024 "
        u"μετονομάσθη από Ιερά Μητρόπολη Τριπόλεως σε Ιερά Μητρόπολη Λιβύης")],
      sources=[AX + "iera-mitropoli-mpotsoyanas/", AX_M]),

 dict(id="ax-cameroon", parent="alexandria",
      name="Holy Archdiocese of Cameroon",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΑΜΕΡΟΥΝ",
      seat="Yaounde", country="CM",
      address=["P.O. Box. 949 Yaounde - Cameroun."],
      sources=[AX + "iera-mitropoli-kameroyn/",
               AX + "holy-archdiocese-of-cameroon/?lang=en"]),

 dict(id="ax-carthage", parent="alexandria",
      name="Holy Archdiocese of Carthage",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΑΡΘΑΓΕΝΗΣ",
      seat="Tunis", country="TN",
      address=["5 Rue de Rome, Tunnis 1000. Tunisie"],
      checked="2026-09-14",
      founded=(
        u"Η ιστορική Ιερά Μητρόπολη Καρθαγένης απετέλεσε τους πρώτους "
        u"χριστιανικούς αιώνες ισχυρό πνευματικό κέντρο και αυτόνομη "
        u"Εκκλησία, όπου συνήλθε το 419 η περίφημη εν Καρθαγένη Τοπική "
        u"Σύνοδος, επανιδρύθη διά Πατριαρχικού και Συνοδικού Τόμου το έτος "
        u"1931"),
      sources=[AX + "iera-mitropoli-karthagenis/",
               AX + "holy-archdiocese-of-carthage/?lang=en"]),

 dict(id="ax-cyrene", parent="alexandria",
      name="Holy Archdiocese of Cyrene",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΥΡΗΝΗΣ",
      country="EG",
      address=["P.O. Box 2006, Alexandria Egypt."],
      sources=[AX + "iera-mitropoli-kyrinis/",
               AX + "holy-archdiocese-of-cyrene/?lang=en"]),

 dict(id="ax-ermoupolis", parent="alexandria",
      name="Holy Archdiocese of Ermoupolis",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΕΡΜΟΥΠΟΛΕΩΣ",
      seat="Tanta", country="EG",
      address=["12 Abou Sombol Str. P.C. 11351 Heliopolis Cairo, Egypt."],
      sources=[AX + "iera-mitropoli-ermoypoleos/",
               AX + "holy-archdiocese-of-ermoupolis/?lang=en"]),

 dict(id="ax-guinea", parent="alexandria",
      name="Holy Archdiocese of Guinea",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΓΟΥΪΝΕΑΣ",
      seat="Conakry", country="GN",
      checked="2026-09-14",
      founded=[(
        u"Η Ιερά Μητρόπολη Γουϊνέας ιδρύθη διά Πατριαρχικού και Συνοδικού "
        u"Τόμου την 10η Οκτωβρίου του έτος 2010, κατ' αρχήν ως Ιερά Επισκοπή "
        u"Σιέρρα Λεόνε"),
       (
        u"Την 21η Νοεμβρίου 2012 ανυψώθη σε Μητρόπολη, υπό τον τίτλο "
        u"Γουϊνέας")],
      sources=[AX + "iera-mitropoli-goyineas/",
               AX + "holy-archdiocese-of-guinea/?lang=en"]),

 dict(id="ax-irinopolis", parent="alexandria",
      name="Holy Archdiocese of Irinopolis",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΕΙΡΗΝΟΥΠΟΛΕΩΣ",
      seat="Dar es Salaam", country="TZ",
      address=["P.O. Box 1090, Dar-Es-Salaam, Tanzania."],
      sources=[AX + "iera-mitropoli-eirinoypoleos/",
               AX + "holy-archdiocese-of-irinopolis/?lang=en"]),

 dict(id="ax-johannesburg", parent="alexandria",
      name="Holy Archdiocese of Johannesburg and Pretoria",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΙΩΑΝΝΟΥΠΟΛΕΩΣ ΚΑΙ ΠΡΕΤΟΡΙΑΣ",
      seat="Johannesburg", country="ZA",
      address=["P.O. Box 1096, Houghton 2041, Johannesburg, Republic of South Africa."],
      checked="2026-09-14",
      founded=(
        u"Η Ιερά Μητρόπολη Ιωαννουπόλεως και Πρετορίας ιδρύθη διά "
        u"Πατριαρχικού και Συνοδικού Τόμου το έτος 1927"),
      sources=[AX + "iera-mitropoli-ioannoypoleos-kai-pretorias/",
               AX + "holy-archdiocese-of-johannesburg-and-pretoria/?lang=en"]),

 dict(id="ax-kinshasa", parent="alexandria",
      name="Holy Archdiocese of Kinshasa",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΙΝΣΑΣΑΣ",
      seat="Kinshasa", country="CD",
      address=["B.P. 11097, Boulevard du 30 Juin, Kinshasa 1. Democratic Republic of Congo"],
      sources=[AX + "iera-mitropoli-kinsasa/", AX_M]),

 dict(id="ax-leontopolis", parent="alexandria",
      name="Holy Archdiocese of Leontopolis",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΛΕΟΝΤΟΠΟΛΕΩΣ",
      seat="Ismailia", country="EG",
      address=["P.O. Box 2006 Alexandria, Egypt."],
      sources=[AX + "iera-mitropoli-leontopoleos/",
               AX + "holy-archdiocese-of-leontopolis/?lang=en"]),

 dict(id="ax-kampala", parent="alexandria",
      name="Holy Metropolis of Kampala",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΑΜΠΑΛΑΣ",
      seat="Kampala", country="UG",
      address=["P.O. Box 3970, Kampala, Uganda."],
      sources=[AX + "iera-mitropoli-kampalas/", AX_M]),

 dict(id="ax-nairobi", parent="alexandria",
      name="Holy Archdiocese of Nairobi",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΝΑΪΡΟΜΠΙ",
      seat="Nairobi", country="KE",
      address=["P.O. Box 46119, Nairobi - Kenya."],
      sources=[AX + "iera-mitropoli-nairompi/",
               AX + "holy-archdiocese-of-nairobi/?lang=en"]),

 dict(id="ax-nigeria", parent="alexandria",
      name="Holy Archdiocese of Nigeria",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΝΙΓΗΡΙΑΣ",
      seat="Lagos", country="NG",
      address=["Orthodox Archdiocese of Nigeria, P.O.Box 75550, Victoria Island, Lagos, Nigeria.",
               "Orthodox Archdiocese of Nigeria, Block 2, Iddo Compound, A.G. Leventis Premises, Ebute Metta, Lagos, Nigeria."],
      site="https://orthodoxchurchnigeria.org/",
      sources=["https://orthodoxchurchnigeria.org/",
               AX + "iera-mitropoli-nigirias/",
               AX + "holy-archdiocese-of-nigeria/?lang=en"]),

 dict(id="ax-nubia", parent="alexandria",
      name="Holy Archdiocese of Nubia",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΝΟΥΒΙΑΣ",
      seat="Khartoum", country="SD",
      address=["P.O. Box 47 Khartoum, Sudan"],
      sources=[AX + "iera-mitropoli-noyvias/",
               AX + "holy-archdiocese-of-nouvias/?lang=en"]),

 dict(id="ax-good-hope", parent="alexandria",
      name="Holy Archdiocese of the Cape of Good Hope",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΑΛΗΣ ΕΛΠΙΔΟΣ",
      seat="Cape Town", country="ZA",
      address=["P.O.Box 4740, Cape Town 8000, Republic of South Africa."],
      checked="2026-09-14",
      founded=(
        u"Η Ιερά Μητρόπολη Καλής Ελπίδος ιδρύθη διά Πατριαρχικού και "
        u"Συνοδικού Τόμου το έτος 1968"),
      sources=[AX + "iera-mitropoli-kalis-elpidos/",
               AX + "holy-archdiocese-of-the-cape-of-good-hope/?lang=en"]),

 dict(id="ax-zambia", parent="alexandria",
      name="Holy Metropolis of Zambia and Mozambique",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΖΑΜΠΙΑΣ ΚΑΙ ΜΟΖΑΜΒΙΚΗΣ",
      seat="Lusaka", country="ZM",
      address=["P.O. Box 51333, Lusaka, Zambia"],
      checked="2026-09-14",
      founded=[(
        u"Η Ιερά Μητρόπολη Ζάμπιας ιδρύθη διά Πατριαρχικού και Συνοδικού "
        u"Τόμου την 22α Φεβρουαρίου 2001 αρχικώς ως Ιερά Επισκοπή Ζάμπιας"),
       (
        u"Δια του Πατριαρχικού και Συνοδικού Τόμο της 9ης Οκτωβρίου 2009 "
        u"ανυψώθη σε Μητροπολιτική Επαρχία του Πατριαρχικού Θρόνου "
        u"Αλεξανδρείας, υπό τον τίτλο Ιερά Μητρόπολη Ζάμπιας"),
       (
        u"Διά του Πατριαρχικού και Συνοδικού Τόμου της 15ης Φεβρουαρίου 2024 "
        u"προσαρτηθη στην πνευματική και ποιμαντική δικαιοδοσία άχρι καιρού "
        u"η έως τότε χηρεύουσα Ιερά Επισκοπή Μοζαμβίκης, μετονομασθείσης της "
        u"εκκλησιαστικής Επαρχίας Ζάμπιας σε Ιερά Μητροπολη Ζάμπιας και "
        u"Μοζαμβίκη")],
      sources=[AX + "iera-mitropoli-zampias/",
               AX + "holy-archdiocese-of-zamvia/?lang=en"]),

 dict(id="ax-zimbabwe", parent="alexandria",
      name="Holy Archdiocese of Zimbabwe and Angola",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΖΙΜΠΑΜΠΟΥΕ ΚΑΙ ΑΓΚΟΛΑΣ",
      seat="Harare", country="ZW",
      address=["P.O. Box 2832, Harare, Zimbabwe."],
      site="https://ierazimpampoue.com/",
      checked="2026-09-14",
      founded=(
        u"H Ιερά Μητρόπολη Ζιμπάμπουε ιδρύθηκε με Συνοδικό Τόμο με απόφαση "
        u"της Ιεράς Πατριαρχικής Συνόδου του Ελληνορθόδοξου Πατριαρχείου "
        u"Αλεξανδρείας και πάσης Αφρικής μετά από πρόταση του μακαριστού "
        u"Πατριάρχου Νικολάου το 1968"),
      sources=["https://ierazimpampoue.com/",
               AX + "iera-mitropoli-zimpampoye-kai-agkolas/",
               AX + "holy-archdiocese-of-zimbabwe-and-angola/?lang=en"]),

 dict(id="ax-heliopolis", parent="alexandria",
      name="Holy Metropolis of Heliopolis",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΗΛΙΟΥΠΟΛΕΩΣ",
      country="EG",
      address=["P.O. Box 2006, Alexandria Egypt"],
      sources=[AX + "iera-mitropoli-ilioypoleos/",
               AX + "holy-metropolis-of-heliopolis/?lang=en"]),

 dict(id="ax-kananga", parent="alexandria",
      name="Holy Metropolis of Kananga",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΑΝΑΓΚΑΣ",
      seat="Kananga", country="CD",
      sources=[AX + "iera-mitropoli-kanagkas/",
               AX + "holy-metropolis-of-kananga/?lang=en"]),

 dict(id="ax-katanga", parent="alexandria",
      name="Holy Metropolis of Katanga",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΚΑΤΑΝΓΚΑΣ",
      seat="Lubumbashi", country="CD",
      address=["B.P. Box 108, Kulwezi, Congo."],
      checked="2026-09-14",
      founded=[(
        u"Η Ιερά Μητρόπολη Κατάγκας ιδρύθη διά Πατριαρχικού και Συνοδικού "
        u"Τόμου την 1η Νοεμβρίου 2006 αρχικώς ως Ιερά Επισκοπή Κολουέζι, "
        u"μετονομασθείσα την 9η Οκτωβρίου 2009 σε Επισκοπή Κατάγκας"),
       (
        u"Κατόπιν ανυψώθη σε Μητροπολιτική Επαρχία του Πατριαρχικού Θρόνου "
        u"Αλεξανδρείας, υπό τον τίτλο Ιερά Μητρόπολη Κατάγκας")],
      sources=[AX + "iera-mitropoli-katangkas/",
               AX + "holy-metropolis-of-katanga/?lang=en"]),

 dict(id="ax-memphis", parent="alexandria",
      name="Holy Metropolis of Memphis",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΜΕΜΦΙΔΟΣ",
      seat="Cairo", country="EG",
      address=["Rue Shebin No 1 (Midan Salah el Dine), Heliopolis, Cairo, Egypt"],
      sources=[AX + "iera-mitropoli-memfidos/",
               AX + "holy-metropolis-of-memphis/?lang=en"]),

 dict(id="ax-pelusium", parent="alexandria",
      name="Holy Metropolis of Pelusium",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΠΗΛΟΥΣΙΟΥ",
      seat="Port Said", country="EG",
      address=["P.O. Box 251, Port Said, Egypt"],
      sources=[AX + "iera-mitropoli-piloysioy/",
               AX + "holy-metropolis-of-pelusium/?lang=en"]),

 dict(id="ax-ptolemais", parent="alexandria",
      name="Holy Archdiocese of Ptolemais",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΠΤΟΛΕΜΑΙΔΟΣ",
      seat="Minya", country="EG",
      address=["Greek Orthodox Patriarchate of Alexandria and all Africa, P.O. Box 2006-Alexandria, Egypt."],
      sources=[AX + "iera-mitropoli-ptolemaidos/",
               AX + "holy-archdiocese-of-ptolemais/?lang=en"]),

 dict(id="ax-diospolis", parent="alexandria",
      name="Holy Metropolis of Diospolis",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΔΙΟΣΠΟΛΕΩΣ",
      seat="Cairo", country="EG",
      address=["P.O. Box 40, Hamzawi, Cairo, Egypt."],
      sources=[AX + "iera-mitropoli-kameroyn-2/", AX_M]),

 dict(id="ax-brazzaville", parent="alexandria",
      name="Holy Metropolis of Brazzaville and Gabon",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗΣ ΜΠΡΑΖΑΒΙΛ ΚΑΙ ΓΚΑΜΠΟΝ",
      seat="Pointe-Noire", country="CG",
      address=["24, Av. Stephane Tchitchelle, Centre Ville, B.P. 183",
               "Pointe-Noire, Republique du Congo, Africa."],
      checked="2026-09-14",
      founded=[(
        u"Η Ιερά Μητρόπολη Μπραζαβίλ και Γκαμπόν ιδρύθη αρχικώς ως Ιερά "
        u"Επισκοπή, διά Πατριαρχικού και Συνοδικού Τόμου την 7η Οκτωβρίου "
        u"2010"),
       (
        u"Διά του Πατριαρχικού και Συνοδικού Τόμου της 24ης Οκτωβρίου 2017 "
        u"ανυψώθηκε δε σε Ιερά Μητρόπολη")],
      sources=[AX + "iera-mitropolis-mprazavil-kai-gkampon/", AX_M]),

 # ---------------------------------------------- dioceses of the Throne
 dict(id="ax-arusha", parent="alexandria",
      name="Holy Diocese of Arusha and Central Tanzania",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΑΡΟΥΣΑΣ ΚΑΙ ΚΕΝΤΡΙΚΗΣ ΤΑΝΖΑΝΙΑΣ",
      seat="Arusha", country="TZ",
      address=["Bishopric of Arusa and Central Tanzania, P.O. Box 623, Iringa, Tanzania, East Africa."],
      sources=[AX + "iera-episkopi-aroysas-kai-kentrikis-tanzanias/",
               AX + "holy-diocese-of-arusha-and-central-tanzania/?lang=en"]),

 dict(id="ax-gaborone", parent="alexandria",
      name="Holy Diocese of Gaborone and Botswana",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΓΚΑΜΠΟΡΟΝΕ ΚΑΙ ΜΠΟΤΣΟΥΑΝΑΣ",
      seat="Gaborone", country="BW",
      sources=[AX + "iera-episkopi-gkamporone-kai-mpotsoyanas/", AX_D]),

 dict(id="ax-goma", parent="alexandria",
      name="Holy Diocese of Goma and Great Kivu",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΓΚΟΜΑΣ ΚΑΙ ΜΕΓΑΛΟΥ ΚΙΒΟΥ",
      seat="Goma", country="CD",
      address=["Province du Nord-Kivu/Commune de Karisimbi/Q. Mugunga /Av. Ruchagara, no 1 B.P.214, Republique Democratique du Congo"],
      sources=[AX + "iera-episkopi-gkomas/",
               AX + "holy-diocese-of-goma/?lang=en"]),

 dict(id="ax-gulu", parent="alexandria",
      name="Holy Diocese of Gulu and Northern Uganda",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΓΚΟΥΛΟΥ ΚΑΙ ΒΟΡΕΙΟΥ ΟΥΓΚΑΝΤΑΣ",
      seat="Gulu", country="UG",
      address=["Orthodox Bishopric of Gulu and North Uganda, P.O Box 817, Gulu, Uganda"],
      sources=[AX + "iera-episkopi-gkoyloy-kai-voreioy-oygkantas/",
               AX + "holy-diocese-of-gulu-and-northern-ugada/?lang=en"]),

 dict(id="ax-kigali", parent="alexandria",
      name="Holy Diocese of Kigali and Rwanda",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΚΙΓΚΑΛΙ ΚΑΙ ΡΟΥΑΝΤΑΣ",
      seat="Kigali", country="RW",
      sources=[AX + "iera-episkopi-kigkali-kai-royantas/", AX_D]),

 dict(id="ax-kisangani", parent="alexandria",
      name="Holy Diocese of Bunia, Kisangani and Eastern Congo",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΜΠΟΥΝΙΑΣ, ΚΙΣΑΝΓΚΑΝΙ & ΑΝΑΤ. ΚΟΝΓΚΟ",
      seat="Kisangani", country="CD",
      address=["Consulat de Grece a Kisangani, face de la place de martyrs, Republique Democratique du Congo"],
      site="https://iekisangani.com/",
      sources=["https://iekisangani.com/",
               AX + "iera-episkopi-kisangkani/",
               AX + "iera-episkopi-kisangkani/?lang=en"]),

 dict(id="ax-kisumu", parent="alexandria",
      name="Holy Diocese of Kisumu and Western Kenya",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΚΙΣΟΥΜΟΥ ΚΑΙ ΔΥΤΙΚΗΣ ΚΕΝΥΑΣ",
      seat="Kisumu", country="KE",
      address=["P.O. Box 829-40123 Megacity Kisumu-Kenya"],
      sources=[AX + "iera-episkopi-kisoymoy-kai-dytikis-kenyas/",
               AX + "holy-diocese-of-kisumu-and-western-kenya/?lang=en"]),

 dict(id="ax-malawi", parent="alexandria",
      name="Holy Diocese of Malawi",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΜΑΛΑΟΥΙ",
      seat="Blantyre", country="MW",
      address=["Orthodox Bishopric of Malawi, P.O. Box 1854, Blantyre, Malawi, Central Africa"],
      sources=[AX + "iera-episkopi-malaoyi/",
               AX + "holy-diocese-of-malawi/?lang=en"]),

 dict(id="ax-benin", parent="alexandria",
      name="Holy Diocese of Benin, Togo and Burkina Faso",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΜΠΕΝΙΝ, ΤΟΓΚΟ και ΜΠΟΥΡΚΙΝΑ ΦΑΣΟ",
      seat="Porto-Novo", country="BJ",
      address=["01 BP : 1135 Quartier Zèbè ToKpota 2 Porto-Novo",
               "République du Benin."],
      checked="2026-09-14",
      founded=(
        u"Η Ιερά Επισκοπή Μπενίν, Τόγκο και Μπουρκίνα Φάσο ιδρύθη διά "
        u"Πατριαρχικού και Συνοδικού Τόμου την 15η Φεβρουαρίου 2024, εξ "
        u"αποσπάσεως της Δημοκρατίας του Μπενίν και της Δημοκρατίας του "
        u"Τόγκο από την πνευματική δικαιοδοσία της Ι. Μητροπόλεως Νιγηρίας, "
        u"ως και της Δημοκρατίας της Μπουρκίνα Φάσο από την πνευματική "
        u"δικαιοδοσία της Ιεράς Μητροπόλεως Άκκρας"),
      sources=[AX + "iera-episkopi-mpenin-togko-kai-mpoyrkina-faso/", AX_D]),

 dict(id="ax-juba", parent="alexandria",
      name="Holy Diocese of Juba and South Sudan",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΤΖΟΥΜΠΑ ΚΑΙ ΝΟΤΙΟΥ ΣΟΥΔΑΝ",
      seat="Juba", country="SS",
      address=["Plot 7JK Hai Nimra Talat. Juba-South Sudan"],
      checked="2026-09-14",
      founded=(
        u"Η Ιερά Επισκοπή Τζούμπα και Νοτίου Σουδάν ιδρύθη διά του "
        u"Πατριαρχικού και Συνοδικού Τόμου της 15ης Φεβρουαρίου 2024, "
        u"συμφωνα με τον οποίο το νέο κράτος του Νοτίου Σουδάν απεσπάσθη από "
        u"την πνευματική δικαιοδοσία της Ιεράς Μητροπόλεως Νουβίας"),
      sources=[AX + "iera-episkopi-mpenin-tsoympa-kai-notioy-soydan/", AX_D]),

 dict(id="ax-bukoba", parent="alexandria",
      name="Holy Diocese of Bukoba and West Tanzania",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΜΠΟΥΚΟΜΠΑ ΚΑΙ ΔΥΤΙΚΗΣ ΤΑΝΖΑΝΙΑΣ",
      seat="Bukoba", country="TZ",
      address=["P.O.B 1704 Bukoba Tanzania"],
      sources=[AX + "iera-episkopi-mpoykompa-kai-dytikis-tanzanias/",
               AX + "holy-diocese-of-bukoba-and-west-tanzania/?lang=en"]),

 dict(id="ax-bujumbura", parent="alexandria",
      name="Holy Diocese of Bujumbura and Burundi",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΜΠΟΥΖΟΥΜΠΟΥΡΑΣ ΚΑΙ ΜΠΟΥΡΟΥΝΤΙ",
      seat="Bujumbura", country="BI",
      address=["Eglise Orthodoxe de Burundi, Rohero II, Avenue du Congo 3, B.P. 3569 Bujumbura - Burundi"],
      sources=[AX + "iera-episkopi-mpoyzoympoyras-kai-mpoyroynti/",
               AX + "holy-diocese-of-bujumbura-and-burundi/?lang=en"]),

 dict(id="ax-nieri", parent="alexandria",
      name="Holy Diocese of Nieri and Mount Kenya",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΝΙΕΡΙ ΚΑΙ ΟΡΟΥΣ ΚΕΝΥΑΣ",
      seat="Nyeri", country="KE",
      address=["P.O. Box 256-0103, Mukurwelni, Kenya."],
      sources=[AX + "iera-episkopi-nieri-kai-oroys-kenyas-2/",
               AX + "holy-diocese-of-nieri-and-mount-kenya-2/?lang=en"]),

 dict(id="ax-eldoret", parent="alexandria",
      name="Holy Diocese of Eldoret and Northern Kenya",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΕΛΝΤΟΡΕΤ ΚΑΙ ΒΟΡΕΙΟΥ ΚΕΝΥΑΣ",
      seat="Kapsabet", country="KE",
      address=["Orthodox Bishopric of Eldoret and Northen Kenya, P.O. Box 447-30300, Kapsabet, Kenya."],
      sources=[AX + "iera-episkopi-nieri-kai-oroys-kenyas/",
               AX + "holy-diocese-of-nieri-and-mount-kenya/?lang=en"]),

 dict(id="ax-toliara", parent="alexandria",
      name="Holy Diocese of Toliara and Southern Madagascar",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΤΟΛΙΑΡΑΣ ΚΑΙ ΝΟΤΙΟΥ ΜΑΔΑΓΑΣΚΑΡΗΣ",
      seat="Toliara", country="MG",
      address=["Saint Diocese Orthodoxe de Tulear, Mitsinjo, Betanimena, 601 Toliara Madagascar"],
      sources=[AX + "iera-episkopi-toliaras-kai-notioy-madagaskaris/",
               AX + "holy-diocese-of-toliara-and-southern-madagascar/?lang=en"]),

 dict(id="ax-jinja", parent="alexandria",
      name="Holy Diocese of Jinja and Eastern Uganda",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΤΖΙΝΤΖΑ ΚΑΙ ΑΝΑΤΟΛΙΚΗΣ ΟΥΓΚΑΝΤΑΣ",
      seat="Jinja", country="UG",
      address=["Orthodox Bishopric of Jinja and Eastern Uganda, P.O. Box 980, Jinja, Uganda."],
      sources=[AX + "iera-episkopi-tzintza-kai-anatolikis-oygkantas/",
               AX + "holy-diocese-of-gulu-and-eastern-uganda/?lang=en"]),
]
