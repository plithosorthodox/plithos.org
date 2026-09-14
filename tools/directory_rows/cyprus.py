# -*- coding: utf-8 -*-
"""The sees of the Church of Cyprus.

Read on 14 September 2026 from the Church's own site, from its page of
administrative structure and then from the page of contact details it
publishes for each see. That page sets out one Archbishopric, nine
metropolises and seven bishoprics; thirteen of the seventeen are written
here, and the four that are not are named below with the reason.

HOW THE SITE WAS REACHED, because it had refused every request from here
before. churchofcyprus.org.cy answers its front page and its section pages
with a challenge that a plain request cannot pass, and it was written down
as unreachable on that evidence. It is not: the leaf pages answer perfectly
well, directly and first time. Every page this file cites was fetched at its
own address with a browser's headers, and the Church's own front page is
still refused, which is why no row here carries it as a link. A site that
turns away the door is not a site that is shut.

THE FOUR THAT ARE NOT ROWS. The Church divides its bishops into three kinds
and says which is which: bishops with a province - Karpasia, Arsinoe and
Amathus - bishops who are abbots, Ledra at the Monastery of Machairas and
Chytron at the Monastery of Saint Neophytos, and titular bishops, Neapolis
and Mesaoria, whose address is the Archbishopric's own. Its own menu tells
them apart a second way: the first three have parishes listed under them and
the other four have none. A title and a monastery are not dioceses, and
jerusalem.py settled for that Patriarchate the rule followed here - titles
are not rows.

THE NAMES. The Church publishes in Greek and nowhere in English, save two
lines: it gives Kyrenia's address in English as "The Holy Metropolis of
Kyrenia" and Tamasos' as "Metropolitan Isaias of Tamasos and Orinis". So
`name` is the Greek rendered, uniformly, and `local` is the Greek as the
Church's own structure page prints it. The Metropolis of Tamasos styles
itself in English "Holy Bishopric of Tamasos and Oreinis" on its own site,
which is its own business and not the form used here for a metropolis.

SEATS AND ADDRESSES ARE DIFFERENT FACTS ON THIS ISLAND and the Church keeps
them apart, so the rows do too. Kyrenia, Morphou, Constantia and Karpasia
give a see under occupation and an address somewhere else, and each row
carries the see as its seat and the working address as its address, exactly
as the Church sets them out. Kykkos has no seat because its see is the Holy
Monastery of Kykkos and not a town; its address is the monastery's
dependency in Nicosia.

Every metropolis but Kykkos publishes a site of its own and every one of them
answered. Kykkos publishes none; the one its neighbours link to,
imkykkou.com.cy, does not resolve, and the metropolis answers under its own
name at imkykkou.org.cy, which is the address the row carries. Limassol's
own site redirects to iml.cy and the row gives the address that answers.
The Church prints the Metropolis of Limassol's site for the Bishopric of
Amathus as well; that is the metropolis's site and not the bishopric's, so
the bishopric's row carries no link of its own.

THE SEVENTEEN ARE THE CHURCH'S OWN NUMBER. Its page of the Hierarchy sets out
the composition of the Holy Synod of the Autocephalous Church of Cyprus and
numbers it from one to seventeen: the Archbishop, nine metropolitans, and
seven bishops. That is where the count comes from, and it agrees with the page
of administrative structure, which separates the same seventeen into the sees
with a province and those without. Ten and three is the thirteen rows here,
counted again on 14 September 2026, and nothing is missing.

The Synod's own list styles the tenth metropolis of Trimythous and Lefkara,
where the page of administrative structure and the metropolis's own contact
details style it of Trimythous alone. The row keeps the form the page it was
read from prints. A see is not renamed here on the strength of a second page
of the same site.


RANK, ADDED 14 SEPTEMBER 2026. Every row here already carried the Church's own
word for what the body is, inside the name its own list prints - Holy Archbishopric, Holy Metropolis, Holy Bishopric -
and `rank` now says it in a field of its own so a reader can see it and a
filter can use it. Nothing was read again for this and nothing was guessed: a
row whose list gives it no such word carries no rank.
"""

READ = "2026-09-14"

CY = "https://churchofcyprus.org.cy/diikitiki_diathrosi"
IMM_SOLON = ("https://immorfou.org.cy/%ce%b5%cf%80%ce%b9%cf%83%ce%ba%ce%bf"
             "%cf%80%ce%ae-%cf%83%cf%8c%ce%bb%cf%89%ce%bd/")
S = "https://churchofcyprus.org.cy/"

ROWS = [
 dict(id="cy-archbishopric", parent="cyprus",
      name="Holy Archbishopric of Cyprus",
      rank="Archbishopric",
      local=u"Ιερά Αρχιεπισκοπή Κύπρου",
      seat="Nicosia", country="CY",
      address=[u"Τ.Θ. 21130", u"1502 Λευκωσία"],
      sources=[S + "stoicheia-epikoinonias", CY]),

 dict(id="cy-paphos", parent="cyprus",
      name="Holy Metropolis of Paphos",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Πάφου",
      seat="Paphos", country="CY",
      address=[u"τ.κ. 60054", u"8100 Πάφος"],
      site="https://impaphou.org/",
      founded=[(
        u"Ἡ πιό πάνω περικοπή ἀπό τίς Πράξεις τῶν Ἀποστόλων (Πράξ. 13, 4 - "
        u"12) θά μποροῦσε νά θεωρηθεῖ ὡς ἡ ἐπίσημη πράξη τῆς ἵδρυσης τῆς "
        u"Ἐκκλησίας τῆς Πάφου"),
       (
        u"ἡ ἐπέτειος τῶν 1950 ἐτῶν ἀπό τῆς ἱδρύσεως τῆς Ἐκκλησίας τῆς Πάφου "
        u"(46 - 1996)")],
      sources=["https://impaphou.org/mitropoli/istoriko-mitropoleos-pafou/",
               S + "stixia-impafou", CY]),

 dict(id="cy-kition", parent="cyprus",
      name="Holy Metropolis of Kition",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Κιτίου",
      seat="Larnaca", country="CY",
      address=[u"τ.θ. 40036", u"6300 Λάρνακα"],
      site="https://www.imkitiou.org/",
      founded=[(
        u"Το Κίτιο υπήρξε από τα πρώτα χρόνια του Χριστιανισμού έδρα "
        u"Επισκόπου"),
       (
        u"Κατά την περίοδο της Φραγκοκρατίας (1191 - 1478), και πιο "
        u"συγκεκριμένα το πρώτο μισό του 13ου αιώνα, η Επισκοπή Κιτίου, αφού "
        u"καταργήθηκε, συγχωνεύτηκε με την Επισκοπή Λευκωσίας"),
       (
        u"Μετά την τουρκική κατάκτηση του 1571 η Επισκοπή Κιτίου "
        u"επανασυστάθηκε, περιλαμβάνοντας τώρα στα όριά της τις παλιές "
        u"Επισκοπές Κιτίου, Αμαθούντος, Λεμεσού και Κουρίου, με έδρα τη "
        u"Λάρνακα")],
      sources=["https://www.imkitiou.org/mitropolis/istoria",
               S + "stixia_imkitiou", CY]),

 dict(id="cy-kyrenia", parent="cyprus",
      name="Holy Metropolis of Kyrenia",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Κυρηνείας",
      seat="Kyrenia", country="CY",
      address=[u"Τ.Θ. 20258", u"2150, Λευκωσία"],
      site="https://www.metropolisofkyrenia.org/",
      sources=["https://www.metropolisofkyrenia.org/",
               S + "stixia_impkirinias", CY]),

 dict(id="cy-limassol", parent="cyprus",
      name="Holy Metropolis of Limassol",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Λεμεσού",
      seat="Limassol", country="CY",
      address=[u"ὁδὸς Ἁγίου Ἀνδρέου 306", u"τ.θ. 56091", u"3304 Λεμεσός"],
      site="https://iml.cy/",
      founded=[(
        u"Από το 1222 μέχρι την Τουρκική κατάκτηση του 1571, λοιπόν, μόνο "
        u"Επισκοπή Λεμεσού υπήρχε, η οποία συμπεριελάμβανε και τις άλλοτε "
        u"Επισκοπές Αμαθούντος και Κουρίου"),
       (
        u"Μετά την Τουρκική κατάκτηση και την αποκατάσταση της Εκκλησίας της "
        u"Κύπρου, η Επισκοπή Λεμεσού συγχωνεύθηκε με την επανασυσταθείσαν "
        u"Επισκοπή Κιτίου στην οποία τελικά υπήχθη, και παρέμεινε έτσι μέχρι "
        u"το 1973, οπότε η τότε Ιερά Σύνοδος απανασύστησε την Επισκοπή "
        u"Λεμεσού, αποσπώντας την πόλη και επαρχία της Λεμεσού από τη "
        u"Μητρόπολη Κιτίου")],
      sources=["https://iml.cy/article/istoriko-ieras-mitropoleos-amathoyntos/",
               S + "stixia_imlemesou", CY]),

 dict(id="cy-morphou", parent="cyprus",
      name="Holy Metropolis of Morphou",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Μόρφου",
      seat="Morphou", country="CY",
      address=[u"Μητροπόλεως 3", u"2831 Εὐρύχου"],
      site="https://immorfou.org.cy/",
      founded=[(
        u"Η Επισκοπή Σόλων, σύμφωνα με τον βίο του Αγίου Αυξιβίου, ιδρύθηκε "
        u"το έτος 57"),
       (
        u"Η Επισκοπή των Σόλων ανασυστήθηκε το 1973 αλλά ο Επίσκοπος Σόλων "
        u"φέρει τον τίτλον Μητροπολίτης Μόρφου και έχει έδρα την Μόρφου")],
      sources=[IMM_SOLON, S + "stixia_immorfou", CY]),

 dict(id="cy-constantia", parent="cyprus",
      name="Holy Metropolis of Constantia and Ammochostos",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Κωνσταντίας και Αμμοχώστου",
      seat="Famagusta", country="CY",
      address=[u"Ἀγίου Γεωργίου 12", u"Τ.Θ. 34034", u"5309 Παραλίμνιον"],
      site="https://imconstantias.org.cy/",
      founded=[(
        u"Η Ιερά Σύνοδος της Εκκλησίας της Κύπρου αποφάσισε σε συνεδρία της, "
        u"στις 12 Φεβρουαρίου 2007, την αύξηση των Μητροπόλεων και "
        u"Χωρεπισκοπών της σε δώδεκα. Επρόκειτο ουσιαστικά για μια απόφαση "
        u"ανασύστασης παλαιών επισκοπών, που για διάφορους ιστορικούς λόγους "
        u"έπαψαν να υφίστανται"),
       (
        u"Έτσι, μετά από οκτώ περίπου αιώνες, ο θρόνος του Αποστόλου Βαρνάβα "
        u"(Σαλαμίνα και στη συνέχεια Κωνσταντίας και Αμμόχωστος) γίνεται "
        u"ξανά Μητρόπολη")],
      sources=["https://imconstantias.org.cy/istoriko/", S + "stixia_imkwnstantias",
               CY]),

 dict(id="cy-kykkos", parent="cyprus",
      name="Holy Metropolis of Kykkos and Tillyria",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Κύκκου και Τηλλυρίας",
      country="CY",
      address=[u"Μετόχιον ῾Ιερᾶς Μονῆς Κύκκου Ἅγιος Προκόπιος, ἐν Λευκωσίᾳ",
               u"τ.θ. 24850", u"1304 Λευκωσία"],
      site="https://imkykkou.org.cy/",
      founded=(
        u"Η Ιερά Σύνοδος της Αγιωτάτης Εκκλησίας της Κύπρου, κατά τη "
        u"συνεδρία της, στις 19 Μαρτίου 2007, αποφάσισε όπως, προς την "
        u"καλύτερη και πληρέστερη θεραπεία των αναγκών του πληρώματος αυτής, "
        u"αυξήσει τις επισκοπικές περιφέρειες, δημιουργώντας, μεταξύ άλλων, "
        u"και Μητρόπολη Κύκκου και Τηλλυρίας"),
      sources=["https://imkykkou.org.cy/istoriko-idrysis-2/apofasi-sistasis",
               S + "stixia_imkukkou", CY]),

 dict(id="cy-tamasos", parent="cyprus",
      name="Holy Metropolis of Tamasos and Oreini",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Ταμασού και Ορεινής",
      seat="Episkopeio", country="CY",
      address=[u"Λεωφόρος Σταύρου Στυλιανίδη", u"2642 Ἐπισκοπειό"],
      site="https://www.imtamasou.org.cy/",
      founded=[(
        u"Η μητρόπολη Ταμασού και Ορεινής αποτελεί μία από τις αρχαιότερες "
        u"επισκοπές της Κύπρου αφού ο πρώτος επίσκοπός της χειροτονήθηκε από "
        u"τους αποστόλους Βαρνάβα και Παύλο κατά το έτος 45 μ.Χ."),
       (
        u"Κατά τη ριζική αναδιοργάνωση της Εκκλησίας της Κύπρου το 2007, "
        u"ανασυστάθηκε η επισκοπή Ταμασού και Ορεινής")],
      sources=["https://www.imtamasou.org.cy/tamasos-2/episkopi_tamasou/",
               S + "stixia_imtamasou", CY]),

 dict(id="cy-trimythous", parent="cyprus",
      name="Holy Metropolis of Trimythous",
      rank="Metropolis",
      local=u"Ιερά Μητρόπολις Τριμυθούντος",
      seat="Idalion", country="CY",
      address=[u"τ.θ. 11001", u"2550 Ἰδάλιον"],
      site="https://imtrimythountos.org.cy/",
      founded=[(
        u"Ἡ Μητρόπολη Τριμυθοῦντος εἶναι γνωστὴ ἀπὸ τοὺς πρώτους κιόλας "
        u"βυζαντινοὺς χρόνους. Κάποια στιγμή, μὲ τὴν πάροδο τοῦ χρόνου, ἡ "
        u"Μητρόπολη ἐγκαταλήφθηκε καὶ στὴ συνέχεια λειτούργησε ὡς "
        u"χωρεπισκοπὴ ὑπὸ τὸν Ἀρχιεπίσκοπο Κύπρου"),
       u"Ἡ ἐκ νέου ἀνασύσταση τῆς Μητροπόλεως ἔγινε τὸ 2007"],
      sources=["https://imtrimythountos.org.cy/istoriko/",
               S + "stixia_imtrimithountos", CY]),

 dict(id="cy-karpasia", parent="cyprus",
      name="Holy Bishopric of Karpasia",
      rank="Bishopric",
      local=u"Επισκοπή Καρπασίας",
      seat="Aigialousa", country="CY",
      address=[u"τ.θ. 21130", u"1502 Λευκωσία"],
      founded=(
        u"Ἀποφάσει τῆς Ἱερᾶς Συνόδου τῆς Ἐκκλησίας τῆς Κύπρου ἀνασυνεστήθη ἡ "
        u"πάλαι ποτὲ διαλάμψασα Ἐπισκοπὴ Καρπασίας"),
      sources=[S + "stixia-epkarpasias", CY]),

 dict(id="cy-arsinoe", parent="cyprus",
      name="Holy Bishopric of Arsinoe",
      rank="Bishopric",
      local=u"Επισκοπή Αρσινόης",
      seat="Peristerona", country="CY",
      address=[u"Περιστερώνα Πάφου", u"Τ.Κ. 8810"],
      founded=[(
        u"Την Εκκλησία της Πάφου αποτελούσαν μέχρι το 1260 δύο Επισκοπικές "
        u"περιφέρειες, της Πάφου και της Αρσινόης"),
       (
        u"Το 1260, ο πάπας Αλέξανδρος ο Δ΄, με τη Bulla Cypria, κατάργησε "
        u"τις περισσότερες Ορθόδοξες Επισκοπές και τις μείωσε από 14 σε 4. "
        u"Τότε, η Επισκοπή Αρσινόης συγχωνεύτηκε με την Επισκοπή Πάφου"),
       (
        u"Με τη χειροτονία του νέου Επισκόπου, στις 26 Μαΐου 1996, έχουμε "
        u"ουσιαστικά και την ανασύσταση της Χωρεπισκοπής Αρσινόης")],
      sources=["https://impaphou.org/episkopi-arsinois/istoriko-episkopis-arsinois/",
               S + "stixia-eparsinois", CY]),

 dict(id="cy-amathus", parent="cyprus",
      name="Holy Bishopric of Amathus",
      rank="Bishopric",
      local=u"Επισκοπή Αμαθούντος",
      seat="Agios Tychonas", country="CY",
      address=[u"Ἁγίου Ἀνδρέου 306", u"Τ.Θ. 56091", u"3304 Λεμεσός"],
      founded=(
        u"Η επισκοπή Αμαθούντος απέκτησε ξανά κανονικό Ποιμένα και επίσκοπο, "
        u"εν κανονικοίς ορίοις, κατά την αρχαίαν ημών παράδοσιν, ο οποίος "
        u"στις 22 Μαΐου 2007 εξελέγη από την Ιερά Σύνοδο της Εκκλησίας της "
        u"Κύπρου Χωρεπίσκοπος Αμαθούντος και χειροτονήθηκε την 10ην Ιουνίου "
        u"2007"),
      sources=["https://iml.cy/article/istoriko-episkopis/",
               S + "stixia-epamathountos", CY]),
]
