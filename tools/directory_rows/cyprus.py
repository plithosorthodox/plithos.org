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
"""

READ = "2026-09-14"

CY = "https://churchofcyprus.org.cy/diikitiki_diathrosi"
S = "https://churchofcyprus.org.cy/"

ROWS = [
 dict(id="cy-archbishopric", parent="cyprus",
      name="Holy Archbishopric of Cyprus",
      local=u"Ιερά Αρχιεπισκοπή Κύπρου",
      seat="Nicosia", country="CY",
      address=[u"Τ.Θ. 21130", u"1502 Λευκωσία"],
      sources=[S + "stoicheia-epikoinonias", CY]),

 dict(id="cy-paphos", parent="cyprus",
      name="Holy Metropolis of Paphos",
      local=u"Ιερά Μητρόπολις Πάφου",
      seat="Paphos", country="CY",
      address=[u"τ.κ. 60054", u"8100 Πάφος"],
      site="https://impaphou.org/",
      sources=["https://impaphou.org/", S + "stixia-impafou", CY]),

 dict(id="cy-kition", parent="cyprus",
      name="Holy Metropolis of Kition",
      local=u"Ιερά Μητρόπολις Κιτίου",
      seat="Larnaca", country="CY",
      address=[u"τ.θ. 40036", u"6300 Λάρνακα"],
      site="https://www.imkitiou.org/",
      sources=["https://www.imkitiou.org/", S + "stixia_imkitiou", CY]),

 dict(id="cy-kyrenia", parent="cyprus",
      name="Holy Metropolis of Kyrenia",
      local=u"Ιερά Μητρόπολις Κυρηνείας",
      seat="Kyrenia", country="CY",
      address=[u"Τ.Θ. 20258", u"2150, Λευκωσία"],
      site="https://www.metropolisofkyrenia.org/",
      sources=["https://www.metropolisofkyrenia.org/",
               S + "stixia_impkirinias", CY]),

 dict(id="cy-limassol", parent="cyprus",
      name="Holy Metropolis of Limassol",
      local=u"Ιερά Μητρόπολις Λεμεσού",
      seat="Limassol", country="CY",
      address=[u"ὁδὸς Ἁγίου Ἀνδρέου 306", u"τ.θ. 56091", u"3304 Λεμεσός"],
      site="https://iml.cy/",
      sources=["https://iml.cy/", S + "stixia_imlemesou", CY]),

 dict(id="cy-morphou", parent="cyprus",
      name="Holy Metropolis of Morphou",
      local=u"Ιερά Μητρόπολις Μόρφου",
      seat="Morphou", country="CY",
      address=[u"Μητροπόλεως 3", u"2831 Εὐρύχου"],
      site="https://immorfou.org.cy/",
      sources=["https://immorfou.org.cy/", S + "stixia_immorfou", CY]),

 dict(id="cy-constantia", parent="cyprus",
      name="Holy Metropolis of Constantia and Ammochostos",
      local=u"Ιερά Μητρόπολις Κωνσταντίας και Αμμοχώστου",
      seat="Famagusta", country="CY",
      address=[u"Ἀγίου Γεωργίου 12", u"Τ.Θ. 34034", u"5309 Παραλίμνιον"],
      site="https://imconstantias.org.cy/",
      sources=["https://imconstantias.org.cy/", S + "stixia_imkwnstantias",
               CY]),

 dict(id="cy-kykkos", parent="cyprus",
      name="Holy Metropolis of Kykkos and Tillyria",
      local=u"Ιερά Μητρόπολις Κύκκου και Τηλλυρίας",
      country="CY",
      address=[u"Μετόχιον ῾Ιερᾶς Μονῆς Κύκκου Ἅγιος Προκόπιος, ἐν Λευκωσίᾳ",
               u"τ.θ. 24850", u"1304 Λευκωσία"],
      site="https://imkykkou.org.cy/",
      sources=["https://imkykkou.org.cy/", S + "stixia_imkukkou", CY]),

 dict(id="cy-tamasos", parent="cyprus",
      name="Holy Metropolis of Tamasos and Oreini",
      local=u"Ιερά Μητρόπολις Ταμασού και Ορεινής",
      seat="Episkopeio", country="CY",
      address=[u"Λεωφόρος Σταύρου Στυλιανίδη", u"2642 Ἐπισκοπειό"],
      site="https://www.imtamasou.org.cy/",
      sources=["https://www.imtamasou.org.cy/", S + "stixia_imtamasou", CY]),

 dict(id="cy-trimythous", parent="cyprus",
      name="Holy Metropolis of Trimythous",
      local=u"Ιερά Μητρόπολις Τριμυθούντος",
      seat="Idalion", country="CY",
      address=[u"τ.θ. 11001", u"2550 Ἰδάλιον"],
      site="https://imtrimythountos.org.cy/",
      sources=["https://imtrimythountos.org.cy/",
               S + "stixia_imtrimithountos", CY]),

 dict(id="cy-karpasia", parent="cyprus",
      name="Holy Bishopric of Karpasia",
      local=u"Επισκοπή Καρπασίας",
      seat="Aigialousa", country="CY",
      address=[u"τ.θ. 21130", u"1502 Λευκωσία"],
      sources=[S + "stixia-epkarpasias", CY]),

 dict(id="cy-arsinoe", parent="cyprus",
      name="Holy Bishopric of Arsinoe",
      local=u"Επισκοπή Αρσινόης",
      seat="Peristerona", country="CY",
      address=[u"Περιστερώνα Πάφου", u"Τ.Κ. 8810"],
      sources=[S + "stixia-eparsinois", CY]),

 dict(id="cy-amathus", parent="cyprus",
      name="Holy Bishopric of Amathus",
      local=u"Επισκοπή Αμαθούντος",
      seat="Agios Tychonas", country="CY",
      address=[u"Ἁγίου Ἀνδρέου 306", u"Τ.Θ. 56091", u"3304 Λεμεσός"],
      sources=[S + "stixia-epamathountos", CY]),
]
