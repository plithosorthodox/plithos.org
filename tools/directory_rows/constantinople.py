# -*- coding: utf-8 -*-
"""The eparchies of the Ecumenical Patriarchate.

The rows the directory already carried were the Throne's eparchies abroad -
Great Britain, France, Germany and the rest - read one page at a time from
the Patriarchate's own site. This file adds the sees the Throne holds at
home and the ones abroad those twelve rows missed: the metropolitan sees in
Turkiye, the Church of Crete, the metropolitan sees in the Dodecanese, the
Exarchate of Patmos, the metropolises of the "New Lands", the metropolises
of the Archdiocese of America, and the eparchies in Ireland, Malta,
Lithuania, Australia, New Zealand, Canada, Argentina and Mexico.

THE NEW LANDS ARE FILED HERE, AND THIS IS WHY. The thirty-six metropolises
of northern Greece are canonically of the Ecumenical Patriarchate and
administered by the Church of Greece, so either file could hold them. They
are here because the Ecumenical Patriarchate publishes them in its own list
of the eparchies of the Throne, under its own heading "Metropolitan Sees of
the 'New Lands'", and a row belongs with the list that claims it. They
appear here once and nowhere else; `greece.py` holds the forty-five
metropolises of the autocephalous territory and the Archdiocese of Athens,
and no see is in both files.

Their names are given as the Throne's own list prints them, which is not
always how the Church of Greece prints them now: Lagadas, Lete and Komotini
is Lagadas alone on the Church of Greece's list, and Edessa and Pella is
Edessa, Pella and Almopia. The row cites both, and a reader can see for
himself. Their addresses are read from the Church of Greece, which prints
them ordered as an envelope wants them and prints them for every one of the
thirty-six; the Patriarchate prints a location for thirty-two and runs the
lines together.

Two smaller things, so they are not mistaken for slips of this file. The
Patriarchate writes "Metropolis of Derkoi" with a Greek iota for the final
letter; that is a keyboard, not a spelling, and the row carries the letter
the title plainly means. And the Patriarchate gives its own Istanbul
address for the Metropolis of Smyrna, as it does for the eparchies whose
pages are still in preparation, so that row carries no address rather than
the Patriarchate's.

Five of the sees in Turkiye - Vryoula, Selybria, Adrianople, Bursa, and
Ganos and Chora - are published with a name and nothing else. They are
listed on those terms.

READ AGAIN ON 14 SEPTEMBER 2026, region by region, against every section
the Throne publishes beneath "Eparchies of the Throne" in both English and
Greek: the Archdiocese of Constantinople, the metropolitan sees in Turkiye,
the metropolitan sees in Greece, the autonomous Churches, the patriarchal
and stavropegic monasteries, the other eparchies in Europe, and the
eparchies in America, Asia and Oceania. The two languages name the same
bodies in the same order everywhere, and the twelve eparchies in Europe,
the three in Asia, the two in Oceania and the seventeen in America were
already here to the last one. Eight were not, and those eight carry their
own reading date; every other row in this file keeps the day it was read.

The Throne's own brief history does not agree with its own list about
Turkiye, and neither has been quietly preferred. The history says that what
is left there is the Archdiocese of Constantinople and the Metropolises of
Chalcedon, Derkon, the Princes Islands, and Imvros and Tenedos - five
bodies. The list of eparchies names eleven metropolises beside the
Archdiocese, the six further ones being sees the Throne still fills and no
longer has a flock in. The rows follow the list, which is the page that
sets out to be a list; the history is cited on the Archdiocese's row, where
the two agree.

The Archdiocese of Constantinople divides into five districts - Stavrodromi,
Tatavla, the Bosphorus, Hypsomatheia, and the Phanar and the Golden Horn -
each with a hierarch and a street of its own, and they are not here. The
Greek entry gives them as the Patriarch's representation within his own see,
set out beside its thirty-seven communities, its churches and its schools;
they are the inside of one eparchy, not eparchies, and they belong with the
parishes rather than with the sees. The metropolises under the Archdiocese
of America are here because the Throne gives each of them an entry of its
own in its list of eparchies. The Archdiocese of Australia's districts are
in neither position: the Patriarchate publishes Australia and New Zealand
and nothing beneath them.
"""

# The Throne's own lists. A row cites the page it was read from and, where
# the address came from elsewhere, the page that printed the address.
TR_LIST = "https://ec-patr.org/en/eparchies-of-the-throne/metropolitan-sees-in-turkiye/"
GR_LIST = "https://ec-patr.org/en/eparchies-of-the-throne/metropolitan-sees-in-greece/"
US_LIST = "https://ec-patr.org/en/eparchies-of-the-throne/eparchies-in-america/"
EU_LIST = "https://ec-patr.org/en/other-eparchies-in-europe/"
OC_LIST = "https://ec-patr.org/en/eparchies-of-the-throne/eparchies-in-oceania/"
E = "https://ec-patr.org/en/entities/"
G = "http://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
MON_LIST = ("https://ec-patr.org/en/eparchies-of-the-throne/"
            "patriarchal-and-stavropegic-monasteries/")
# The Throne in its own language. Where a body's name in Greek was wanted,
# or what it says about its own beginning, it was read from the Greek entry
# the English one points at.
EG = "https://ec-patr.org/entities/"

# What the thirty-six metropolises of the "New Lands" carry in `standing`.
# A reader who finds a see in northern Greece filed under Istanbul is owed
# the act that put it there, and the act is published in full by the Church
# of Greece's own Apostoliki Diakonia: "τηρουμένου του επί των Επαρχιών
# τούτων ανωτάτου κανονικού δικαιώματος του Αγιωτάτου Πατριαρχικού
# Οικουμενικού Θρόνου, η διοίκησις ... διεξάγηται εφεξής επιτροπικώς υπό
# της ... Εκκλησίας της Ελλάδος", subscribed "εν έτει σωτηρίω 1928, μηνός
# Σεπτεμβρίου δ". The site does not adjudicate the arrangement; it names
# the act and who did it, which is all `standing` is for.
ACT_1928 = ("The Ecumenical Patriarchate committed the administration of the"
            " metropolises of the New Lands to the Church of Greece by the"
            " Patriarchal and Synodal Act of 4 September 1928, the supreme"
            " canonical right over them staying with the Throne.")
ACT_1928_TEXT = ("https://apostoliki-diakonia.gr/"
                 "synodiki-praksi-1928-dioikisi-mitropoleon/")

ROWS = [

 # ------------------------------------------- the metropolitan sees in Turkiye
 dict(id="ep-chalcedon", parent="constantinople",
      name="Metropolis of Chalcedon",
      seat="Istanbul", country="TR",
      address=["Bahariye Cad. 31", "34710 Kadıköy, İstanbul"],
      sources=[E + "holy-metropolis-of-chalcedon/", TR_LIST]),
 dict(id="ep-derkoi", parent="constantinople",
      name="Metropolis of Derkoi",
      seat="Istanbul", country="TR",
      address=["Ebuziya Cad. No. 15", "34720 Bakırköy-İstanbul"],
      sources=[E + "holy-metropolis-of-derkoi/", TR_LIST]),
 dict(id="ep-princes-islands", parent="constantinople",
      name="Metropolis of Princes Islands",
      seat="Istanbul", country="TR",
      address=["Kıvılcım Sok. No. 3", "Büyükada, İstanbul"],
      sources=[E + "holy-metropolis-of-the-princes-islands/", TR_LIST]),
 dict(id="ep-vryoula", parent="constantinople",
      name="Metropolis of Vryoula",
      country="TR",
      sources=[E + "metropolis-of-vryoula/", TR_LIST]),
 dict(id="ep-pisidia", parent="constantinople",
      name="Metropolis of Pisidia",
      seat="Antalya", country="TR",
      address=["Kılınçarslan Mah., Kurtuluş Sok. No: 4", "Muratpaşa-Antalya"],
      sources=[E + "holy-metropolis-of-pisidia/", TR_LIST]),
 dict(id="ep-selybria", parent="constantinople",
      name="Metropolis of Selybria",
      country="TR",
      sources=[E + "metropolis-of-selybria/", TR_LIST]),
 dict(id="ep-adrianople", parent="constantinople",
      name="Metropolis of Adrianople",
      country="TR",
      sources=[E + "metropolis-of-adrianople/", TR_LIST]),
 dict(id="ep-smyrna", parent="constantinople",
      name="Metropolis of Smyrna",
      seat="Izmir", country="TR",
      sources=[E + "holy-metropolis-of-smyrna/", TR_LIST]),
 dict(id="ep-imbros-tenedos", parent="constantinople",
      name="Metropolis of Imbros and Tenedos",
      seat="Imbros", country="TR",
      address=["P.K. 42", "117 60 Gökçeada-Çanakkale"],
      sources=[E + "holy-metropolis-of-imvros-and-tenedos/", TR_LIST]),
 dict(id="ep-bursa", parent="constantinople",
      name="Metropolis of Bursa",
      seat="Bursa", country="TR",
      sources=[E + "metropolis-of-bursa/", TR_LIST]),
 dict(id="ep-ganos-chora", parent="constantinople",
      name="Metropolis of Ganou and Chora",
      country="TR",
      sources=[E + "metropolis-of-ganou-and-chora/", TR_LIST]),

 # ------------------------------------------------ the Church of Crete
 dict(id="ep-crete", parent="constantinople",
      name="Archdiocese of Crete",
      seat="Heraklion", country="GR",
      address=[u"Ἁγίου Μηνᾶ 25", u"Τ.Κ. 712 01 ῾Ηράκλειον"],
      site="https://www.iak.gr/",
      sources=[E + "archdiocese-of-crete", GR_LIST]),
 dict(id="ep-gortyne", parent="constantinople",
      name="Metropolis of Gortyne and Arkadia",
      country="GR",
      site="https://www.imga.gr/",
      sources=[E + "metropolis-of-gortyna-and-arkadia", GR_LIST]),
 dict(id="ep-rethymne", parent="constantinople",
      name="Metropolis of Rethymne and Avlopotamos",
      seat="Rethymno", country="GR",
      sources=[E + "metropolis-of-rethymno-and-avlopotamos", GR_LIST]),
 dict(id="ep-kydonia", parent="constantinople",
      name="Metropolis of Kydonia and Apokoronos",
      seat="Chania", country="GR",
      address=[u"Πλατεῖα Πατρ. Ἀθηναγόρου", u"Τ.Κ. 73132 Χανιά"],
      site="https://imka.gr/",
      sources=[E + "metropolis-of-kydonia-and-apokoronos", GR_LIST]),
 dict(id="ep-lampe", parent="constantinople",
      name="Metropolis of Lampe, Syvrito and Sfakia",
      country="GR",
      sources=[E + "metropolis-of-lampe-syvritos-and-sfakia", GR_LIST]),
 dict(id="ep-hierapytne", parent="constantinople",
      name="Metropolis of Hierapytne and Siteia",
      country="GR",
      site="https://www.imis.gr/",
      sources=[E + "metropolis-of-ierapitna-and-sitia", GR_LIST]),
 dict(id="ep-petra", parent="constantinople",
      name="Metropolis of Petra and Cherronesos",
      country="GR",
      site="https://www.impeh.gr/",
      sources=[E + "metropolis-of-petra-and-cherronisos", GR_LIST]),
 dict(id="ep-kisamos", parent="constantinople",
      name="Metropolis of Kisamos and Selinos",
      local=u"Ιερά Μητρόπολις Κισάμου & Σελίνου",
      seat="Kissamos", country="GR",
      address=[u"Κίσαμος – Χανιά", u"Τ.Κ. 73400"],
      site="https://imks.gr/",
      sources=[E + "metropolis-of-kisamos-and-selinos/", GR_LIST,
               "https://imks.gr/"]),
 dict(id="ep-arkalochorion", parent="constantinople",
      name="Metropolis of Arkalochorion",
      country="GR",
      site="https://www.imakb.gr/",
      sources=[E + "metropolis-of-arkalochori", GR_LIST]),

 # ------------------------------------ the metropolitan sees in the Dodecanese
 dict(id="ep-rhodes", parent="constantinople",
      name="Metropolis of Rhodes",
      seat="Rhodes", country="GR",
      site="https://www.imr.gr/",
      sources=[E + "metropolis-of-rhodes", GR_LIST]),
 dict(id="ep-kos", parent="constantinople",
      name="Metropolis of Kos and Nisyros",
      seat="Kos", country="GR",
      sources=[E + "metropolis-of-kos-and-nisyros", GR_LIST]),
 dict(id="ep-leros", parent="constantinople",
      name="Metropolis of Leros, Kalymnos, and Astypalaia",
      seat="Leros", country="GR",
      site="http://im-leka.gr/",
      sources=[E + "metropolis-of-leros-kalymnos-and-astypalaia", GR_LIST]),
 dict(id="ep-karpathos", parent="constantinople",
      name="Metropolis of Karpathos and Kasos",
      seat="Karpathos", country="GR",
      sources=[E + "metropolis-of-karpathos-and-kasos", GR_LIST]),
 dict(id="ep-syme", parent="constantinople",
      name="Metropolis of Syme",
      seat="Syme", country="GR",
      site="https://www.imsymis.gr/index.php/el/",
      sources=[E + "metropolis-of-simi", GR_LIST]),
 dict(id="ep-patmos", parent="constantinople",
      name="Patriarchal Exarchate of Patmos",
      seat="Patmos", country="GR",
      address=[u"Τ.Θ. 25", u"Τ.Κ. 855 00 Πάτμος"],
      sources=[E + "patriarchal-exarchate-of-patmos/"]),

 # ------------------------------------- the metropolises of the "New Lands"
 #
 # Named as the Throne's list names them; addressed as the Church of Greece,
 # which administers them, prints the address.
 dict(id="ep-alexandroupolis", parent="constantinople",
      name="Metropolis of Alexandroupolis",
      seat="Alexandroupolis", country="GR",
      address=[u"Ανθίμειο Εκκλησιαστικό Κέντρο",
               u"Πλαταιών και Αμφιπόλεως",
               u"Αλεξανδρούπολη. Τ.Κ 68100"],
      sources=[E + "holy-metropolis-of-alexandroupolis/", GR_LIST,
               G + "alexandroupoleos"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-beroia", parent="constantinople",
      name="Metropolis of Beroia Naousa and Kampania",
      seat="Veroia", country="GR",
      address=[u"Μητροπόλεως 30, Τ.Θ. 241", u"Τ.Κ. 59100 - Βέροια"],
      site="https://imverias.gr/",
      sources=[E + "holy-metropolis-of-beroia-naousa-and-kampania/", GR_LIST,
               G + "iera-metropole-beroias-kai-naouses"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-goumenissa", parent="constantinople",
      name="Metropolis of Goumenissa Axiopolis and Polykarpos",
      seat="Goumenissa", country="GR",
      address=[u"Ι. Μ. Παναγίας (Επισκοπείον)", u"Τ.Κ. 61300 - Γουμένισσα"],
      site="http://www.imgap.gr/",
      sources=[E + "holy-metropolis-of-goumenissa-axiopolis-and-polykarpos/",
               GR_LIST, G + "goumenisses-axioupoleos-kai-polykastrou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-grevena", parent="constantinople",
      name="Metropolis of Grevena",
      seat="Grevena", country="GR",
      address=[u"Εὐαγγελιστρίας 22", u"Γρεβενά. Τ.Κ. 51100"],
      sources=[E + "holy-metropolis-of-grevena/", GR_LIST, G + "grebenon"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-didymoteichon", parent="constantinople",
      name="Metropolis of Didymoteichon Orestiada and Souflion",
      seat="Didymoteicho", country="GR",
      address=[u"Πατριάρχου Διονυσίου 7", u"Τ.Κ. 68300 - Διδυμότειχο"],
      site="https://imdos.gr/",
      sources=[E + "holy-metropolis-of-didymoteichon-orestiada-and-souflion/",
               GR_LIST, G + "didymoteichou-kai-orestiados"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-drama", parent="constantinople",
      name="Metropolis of Drama",
      seat="Drama", country="GR",
      address=[u"Νενιζέλου 168. Τ.Θ. 78", u"Τ.Κ. 66100 - Δράμα"],
      site="http://www.imdramas.gr/",
      sources=[E + "holy-metropolis-of-drama/", GR_LIST, G + "dramas"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-dryinoupolis", parent="constantinople",
      name="Metropolis of Dryinoypolis Pogoniane and Konitsa",
      seat="Delvinaki", country="GR",
      address=[u"Δελβινάκι", u"ΤΚ 44002"],
      site="https://www.imdpk.gr/",
      sources=[E + "holy-metropolis-of-dryinoypolis-pogoniane-and-konitsa/",
               GR_LIST, G + "dryinoupoleos-pogonianes-kai-konitses"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-edessa", parent="constantinople",
      name="Metropolis of Edessa and Pella",
      seat="Edessa", country="GR",
      address=[u"Μ. Αλεξάνδρου 4", u"Τ.Κ. 58200 - Έδεσσα"],
      site="https://www.imepa.gr/",
      sources=[E + "holy-metropolis-of-edessa-and-pella/", GR_LIST,
               G + "edesses-pelles-kai-almopias"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-elassona", parent="constantinople",
      name="Metropolis of Helassona",
      seat="Elassona", country="GR",
      address=[u"1ης Μεραρχίας 2", u"Τ.Κ. 40200 - Ελασσώνα"],
      site="https://www.elassona.com.gr/",
      sources=[E + "holy-metropolis-of-elasson/", GR_LIST, G + "elassonos"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-eleftheroupolis", parent="constantinople",
      name="Metropolis of Eleftheroupolis",
      seat="Eleftheroupoli", country="GR",
      address=[u"Αγίου Νικολάου 4", u"Τ.Κ. 64100 - Ελευθερούπολη"],
      site="https://imelef.gr/",
      sources=[E + "holy-metropolis-of-eleftheroupolis/", GR_LIST,
               G + "eleutheroupoleos"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-zihna", parent="constantinople",
      name="Metropolis of Zihna and Nevrokopion",
      seat="Nea Zichni", country="GR",
      address=[u"Νέα Ζίχνη", u"Τ.Κ. 62042"],
      sources=[E + "holy-metropolis-of-zihna-and-nevrokopion/", GR_LIST,
               G + "iera-metropole-zichnon-kai-neurokopiou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-thessaloniki", parent="constantinople",
      name="Metropolis of Thessaloniki",
      seat="Thessaloniki", country="GR",
      address=[u"Βογατσικού 7", u"Τ.Κ. 54622 Θεσσαλονίκη"],
      site="https://imth.gr/",
      sources=[E + "holy-metropolis-of-thessaloniki/", GR_LIST,
               G + "thessalonikes"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-hierissos", parent="constantinople",
      name="Metropolis of Hierissos the Holy Mountain and Ardamerion",
      seat="Arnaia", country="GR",
      address=[u"Αρναία Χαλκιδικής", u"Τ.Κ. 63074"],
      site="https://web.im-ierissou.gr/",
      sources=[E + "holy-metropolis-of-herissos-the-holy-mountain-athos-and-ardamerion/",
               GR_LIST, G + "ierissou-agiou-orous-kai-ardameriou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-ioannina", parent="constantinople",
      name="Metropolis of Ioannina",
      seat="Ioannina", country="GR",
      address=[u"Πατριάρχου Ιωακείμ Γ΄ 10, Τ.Θ.: 1130",
               u"Τ.Κ. 45221 Ιωάννινα"],
      sources=[E + "holy-metropolis-of-ioannina/", GR_LIST, G + "ioanninon"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-kassandreia", parent="constantinople",
      name="Metropolis of Kassandreia",
      seat="Polygyros", country="GR",
      address=[u"Πολύγυρος Χαλκιδικής", u"Τ.Κ. 63200"],
      site="https://www.imkassandreias.gr/index.php/el/",
      sources=[E + "holy-metropolis-of-kassandreia/", GR_LIST,
               G + "kassandreias"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-kastoria", parent="constantinople",
      name="Metropolis of Kastoria",
      seat="Kastoria", country="GR",
      address=[u"Πλατειά Παύλου Μελά 1", u"Τ.Κ. 52100 Καστοριά"],
      site="https://www.imkastorias.gr/",
      sources=[E + "holy-metropolis-of-kastoria/", GR_LIST, G + "kastorias"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-kitros", parent="constantinople",
      name="Metropolis of Kitros",
      seat="Katerini", country="GR",
      address=[u"Μητροπόλεως 6. Τ.Θ. 80", u"Τ. Κ. 60100 - Κατερίνη"],
      site="https://imkitrous.gr/",
      sources=[E + "holy-metropolis-of-kitros/", GR_LIST,
               G + "kitrous-katerines-kai-platamonos"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-lagadas", parent="constantinople",
      name="Metropolis of Lagadas Lete and Komotini",
      seat="Lagadas", country="GR",
      address=[u"27ης Οκτωβρίου 1", u"Τ.Κ. 57200 - Λαγκαδάς"],
      site="https://www.imlagada.gr/",
      sources=[E + "holy-metropolis-of-lagadas-lete-and-komotini/", GR_LIST,
               G + "lankada"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-lemnos", parent="constantinople",
      name="Metropolis of Lemnos",
      seat="Myrina", country="GR",
      address=[u"Τ.Κ. 81400 Μύρινα Λήμνου"],
      sources=[E + "holy-metropolis-of-lemnos/", GR_LIST,
               G + "lemnou-kai-agiou-eustratiou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-maroneia", parent="constantinople",
      name="Metropolis of Maroneia and Komotini",
      seat="Komotini", country="GR",
      address=[u"Πλατεία Αυτοκράτωρος Θεοδοσίου 7",
               u"Τ.Κ.: 69100 - Κομοτηνή"],
      site="https://immaroniaskomotinis.gr/",
      sources=[E + "holy-metropolis-of-maroneia-and-komotini/", GR_LIST,
               G + "maroneias-kai-komotenes"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-mithymna", parent="constantinople",
      name="Metropolis of Mithymna",
      seat="Kalloni", country="GR",
      address=[u"Καλλονή Λέσβου", u"Τ.Κ. 81107"],
      sources=[E + "holy-metropolis-of-mithymna/", GR_LIST, G + "methymnes"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-mytilene", parent="constantinople",
      name="Metropolis of Mytilene",
      seat="Mytilene", country="GR",
      address=[u"Μητροπόλεως 1", u"Τ.Κ. 81100 - Μυτιλήνη"],
      site="https://www.immyt.gr/",
      sources=[E + "holy-metropolis-of-mytilene/", GR_LIST,
               G + "mytilenes-eressou-kai-plomariou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-neapolis-stavroupolis", parent="constantinople",
      name="Metropolis of Neapolis and Stavroupolis",
      seat="Neapoli", country="GR",
      address=[u"Νεάπολη Θεσσαλονίκης", u"Μητροπόλεως 11", u"Τ. Κ. 56728"],
      site="https://imnst.gr/",
      sources=[E + "holy-metropolis-of-neapolis-and-stavroupolis/", GR_LIST,
               G + "neapoleos-kai-stauroupoleos"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-nea-krini", parent="constantinople",
      name="Metropolis of Nea Krini and Kalamaria",
      seat="Kalamaria", country="GR",
      address=[u"Μητροπολίτου Χρύσανθου 1", u"Καλαμαριά, Τ. Κ. 55132"],
      sources=[E + "holy-metropolis-of-nea-krini-and-kalamaria/", GR_LIST,
               G + "neas-krenes-kai-kalamarias"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-nikopolis", parent="constantinople",
      name="Metropolis of Nikopolis and Prebeza",
      seat="Preveza", country="GR",
      address=[u"Πρέβεζα. Τ. Κ. 48100"],
      site="https://imprevezis.blogspot.com/",
      sources=[E + "holy-metropolis-of-nikopolis-and-prebeza/", GR_LIST,
               G + "nikopoleos-kai-prebezes"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-xanthi", parent="constantinople",
      name="Metropolis of Xanthi",
      seat="Xanthi", country="GR",
      address=[u"Πλατεία Μητροπόλεως. Ξάνθη", u"Τ. Θ 270. Τ. Κ. 67100"],
      site="https://im-xanthis.gr/",
      sources=[E + "holy-metropolis-of-xanthi/", GR_LIST,
               G + "xanthes-kai-peritheoriou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-paramythia", parent="constantinople",
      name="Metropolis of Paramythia Filiata and Geromerion",
      seat="Paramythia", country="GR",
      address=[u"Παραμυθιά. Τ. Κ. 46200"],
      site="https://imparamythias.gr/",
      sources=[E + "holy-metropolis-of-paramythia-filiata-and-geromerion/",
               GR_LIST, G + "paramythias-philiaton-geromeriou-kai-pargas"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-polyane", parent="constantinople",
      name="Metropolis of Polyane and Kilkis",
      seat="Kilkis", country="GR",
      address=[u"Κιλκίς, ὁδὸς Ἔλ. Βενιζέλου 2", u"Τ.Κ. 611 00"],
      site="https://www.impk.gr/",
      sources=[E + "holy-metropolis-of-polyane-and-kilkis/", GR_LIST,
               G + "polyanes-kai-kilkisiou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-samos", parent="constantinople",
      name="Metropolis of Samos and Ikaria",
      seat="Samos", country="GR",
      address=[u"28ης Οκτωβρίου Σάμος", u"Τ. Κ. 83100"],
      site="https://www.imsamou.gr/index.php/el/",
      sources=[E + "holy-metropolis-of-samos-and-ikaria/", GR_LIST,
               G + "samou-kai-ikarias"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-servia-kozani", parent="constantinople",
      name="Metropolis of Servia and Kozani",
      seat="Kozani", country="GR",
      address=[u"Οδός Χαρισίου Μεγδάνη 6", u"Τ. Κ. 50100 Κοζάνη"],
      site="https://imsk.gr/el/",
      sources=[E + "holy-metropolis-of-servia-and-kozani/", GR_LIST,
               G + "serbion-kai-kozanes"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-serres", parent="constantinople",
      name="Metropolis of Serres and Nigrite",
      seat="Serres", country="GR",
      address=[u"Οδός Κύπρου 10", u"Τ. Κ. 62122 Σέρρες"],
      site="https://www.imsn.gr/",
      sources=[E + "holy-metropolis-of-serres-and-nigrite/", GR_LIST,
               G + "serron-kai-nigrites"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-siderokastron", parent="constantinople",
      name="Metropolis of Siderokastron",
      seat="Siderokastro", country="GR",
      address=[u"Μητροπόλεως 12", u"Τ.Κ. 62300 - Σιδηρόκαστρο"],
      sources=[E + "holy-metropolis-of-siderokastron/", GR_LIST,
               G + "siderokastrou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-sisanion", parent="constantinople",
      name="Metropolis of Sisanion and Siatista",
      seat="Siatista", country="GR",
      address=[u"Μητροπολίτου Ιακώβου 1", u"Τ. Κ.: 50300 - Σιάτιστα"],
      sources=[E + "holy-metropolis-of-sisanion-and-siatista/", GR_LIST,
               G + "sisaniou-kai-siatistes"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-philippoi", parent="constantinople",
      name="Metropolis of Philippoi Neapolis and Thasos",
      seat="Kavala", country="GR",
      address=[u"Μητροπόλεως 1. Τ.Θ.: 1243", u"Τ. Κ. 65403 - Καβάλα"],
      site="https://www.im-philippon.gr/",
      sources=[E + "holy-metropolis-of-philippoi-neapolis-and-thasos/",
               GR_LIST, G + "philippon-neapoleos-kai-thasou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-phlorina", parent="constantinople",
      name="Metropolis of Phlorina Prespes and Eordaia",
      seat="Florina", country="GR",
      address=[u"Μητροπόλεως 1, Τ.Θ. 20", u"Τ. Κ. 53100 - Φλώρινα"],
      sources=[E + "holy-metropolis-of-phlorina-prespes-and-eordaia/",
               GR_LIST, G + "phlorines-prespon-kai-eordaias"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),
 dict(id="ep-chios", parent="constantinople",
      name="Metropolis of Chios",
      seat="Chios", country="GR",
      address=[u"Κων/νου Αμάντου 24", u"Τ. Κ. 82100 - Χίος"],
      site="https://www.imchiou.gr/index.php/el/",
      sources=[E + "holy-metropolis-of-chios/", GR_LIST, G + "chiou"],
      standing=ACT_1928, standing_source=ACT_1928_TEXT),

 # ------------------------- the metropolises of the Archdiocese of America
 #
 # The Archdiocese itself already has a row. These are the eight metropolises
 # the Throne lists beneath it.
 dict(id="ep-boston", parent="constantinople",
      name="Metropolis of Boston",
      seat="Brookline, Massachusetts", country="US",
      address=["162 Goddard Avenue", "Brookline, MA 02445"],
      site="https://boston.goarch.org/",
      sources=[E + "holy-metropolis-of-boston/", US_LIST]),
 dict(id="ep-atlanta", parent="constantinople",
      name="Metropolis of Atlanta",
      seat="Atlanta, Georgia", country="US",
      address=["2480 Clairmont Road NE", "GA 30329"],
      site="https://atlmetropolis.org/",
      sources=[E + "holy-metropolis-of-atlanta/", US_LIST]),
 dict(id="ep-detroit", parent="constantinople",
      name="Metropolis of Detroit",
      country="US",
      sources=[E + "holy-metropolis-of-detroit/", US_LIST]),
 dict(id="ep-pittsburgh", parent="constantinople",
      name="Metropolis of Pittsburgh",
      seat="Pittsburgh, Pennsylvania", country="US",
      address=["5201 Ellsworth Avenue", "Pittsburgh, PA. 15232"],
      sources=[E + "holy-metropolis-of-pittsburgh/", US_LIST]),
 dict(id="ep-san-francisco", parent="constantinople",
      name="Metropolis of San Francisco",
      seat="San Francisco, California", country="US",
      address=["245 Valencia Street", "San Francisco CA 94103"],
      sources=[E + "holy-metropolis-of-san-francisco/", US_LIST]),
 dict(id="ep-new-jersey", parent="constantinople",
      name="Metropolis of New Jersey",
      seat="Westfield, New Jersey", country="US",
      address=["215 East Grove Street", "Westfield, New Jersey 07090-1656"],
      site="https://nj.goarch.org/",
      sources=[E + "holy-metropolis-of-new-jersey/", US_LIST]),
 dict(id="ep-chicago", parent="constantinople",
      name="Metropolis of Chicago",
      seat="Chicago, Illinois", country="US",
      address=["40 East Burton Place", "Chicago, Illinois 60610-1697"],
      site="https://chicago.goarch.org/",
      sources=[E + "holy-metropolis-of-chicago/", US_LIST]),
 dict(id="ep-denver", parent="constantinople",
      name="Metropolis of Denver",
      seat="Denver, Colorado", country="US",
      address=["4550 East Alameda Avenue", "Denver. Colorado 80246-1208"],
      sources=[E + "holy-metropolis-of-denver/", US_LIST]),

 # ------------------------------- the eparchies abroad the earlier rows missed
 dict(id="ep-ireland", parent="constantinople",
      name="Metropolitan of Ireland",
      country="IE",
      sources=[E + "metropolitan-of-ireland/", EU_LIST]),
 dict(id="ep-malta", parent="constantinople",
      name="Patriarchal Exarchate of Malta",
      seat="Valletta", country="MT",
      address=["Greek Orthodox Church of St Nicholas",
               "Merchants Street, Valetta"],
      site="https://www.exarmalta.com/",
      sources=[E + "patriarchal-exarchate-of-malta/", EU_LIST,
               "https://www.exarmalta.com/"]),
 dict(id="ep-lithuania", parent="constantinople",
      name="Patriarchal Exarchate of Lithuania",
      country="LT",
      sources=[E + "patriarchal-exarchate-of-lithuania/", EU_LIST]),
 dict(id="ep-australia", parent="constantinople",
      name="Archdiocese of Australia",
      seat="Sydney", country="AU",
      address=["242 Cleveland Street", "Redfern NSW 2016"],
      site="https://greekorthodox.org.au/",
      sources=[E + "archdiocese-of-australia/", OC_LIST,
               "https://greekorthodox.org.au/contact/"]),
 dict(id="ep-new-zealand", parent="constantinople",
      name="Metropolis of New Zealand",
      country="NZ",
      sources=[E + "metropolis-of-new-zealand/", OC_LIST]),
 dict(id="ep-canada", parent="constantinople",
      name="Archdiocese of Canada",
      seat="Toronto, Ontario", country="CA",
      address=["1 Patriarch Bartholomew Way", "(86 Overlea Boulevard)",
               "Toronto, ON M4H 1C6"],
      site="https://goarchdiocese.ca/",
      sources=[E + "archdiocese-of-canada/", US_LIST,
               "https://goarchdiocese.ca/"]),
 dict(id="ep-buenos-aires", parent="constantinople",
      name="Metropolis of Buenos Aires",
      country="AR",
      sources=[E + "metropolis-of-buenos-aires/", US_LIST]),
 dict(id="ep-mexico", parent="constantinople",
      name="Metropolis of Mexico",
      country="MX",
      sources=[E + "metropolis-of-mexico/", US_LIST]),

 # --------------------------- the Patriarch's own see, read 14 September 2026
 #
 # The Throne opens its list of eparchies with the Archdiocese it keeps at
 # the Phanar, before the metropolitan sees in Turkiye, and its own brief
 # history names the Archdiocese first among what is left to it there. The
 # street is the one the Patriarchate prints on the entry.
 dict(id="ep-constantinople", parent="constantinople",
      name="Archdiocese of Constantinople",
      local=u"Αρχιεπισκοπή Κωνσταντινουπόλεως",
      seat="Istanbul", country="TR", checked="2026-09-14",
      address=["Cumhuriyet Cad. King Apt. No. 275/7",
               u"Harbiye, İstanbul"],
      sources=[E + "archiodese-of-constaninople/",
               EG + "archiepiskopi-konstantinoypoleos/", TR_LIST]),

 # ------------------------------------- the Church of Crete, read 14 Sept 2026
 #
 # The Archdiocese of Crete and its eight metropolises were already here. The
 # Synod they sit in was not, and it is the body the Throne prints at the head
 # of them: the Orthodox Church in Crete, which the Patriarchate calls
 # semi-autonomous and which answers on a site of its own at Heraklion.
 dict(id="ep-crete-synod", parent="constantinople",
      name="Eparchial Synod of the Church of Crete",
      local=u"Ἱερά Ἐπαρχιακή Σύνοδος Ἐκκλησίας Κρήτης",
      seat="Heraklion", country="GR", checked="2026-09-14",
      address=[u"Ἁγίου Μηνᾶ 25",
               u"71201 - Ἡράκλειον"],
      site="https://ekklisiakritis.com/",
      sources=[E + "eparchial-synod-of-the-church-of-crete",
               EG + "iera-eparhiaki-sunodos-ekklisias-kritis/",
               "https://ekklisiakritis.com/"]),

 # ------------------ the patriarchal and stavropegic monasteries, 14 Sept
 #
 # The Holy Mountain and the Exarchate of Patmos stood alone out of a section
 # of eight. These are the other six, each from the Throne's own entry for it,
 # in English and in Greek. Three of the six publish a door of their own and
 # each was opened and read; the rest carry an address and no link.
 dict(id="ep-mon-anastasia", parent="constantinople",
      name=("Sacred Royal, Patriarchal and Stavropegic Monastery of Saint "
            "Anastasia Pharmakolytria in Chakidiki"),
      local=u"Ἱερά Βασιλική Πατριαρχική καί Σταυροπηγιακή Μονή τῆς Ἁγίας Ἀναστασίας τῆς Φαρμακολυτρίας ἐν Χαλκιδικῇ",
      seat="Vasilika", country="GR", checked="2026-09-14",
      address=[u"570 06 Βασιλικά Χαλκιδικῆς"],
      founded=u"Ἱδρύθη τό ἔτος 888 ὑπό τῆς Αὐγούστης Θεοφανοῦς, ἐπί Πατριαρχίας Φωτίου τοῦ Μεγάλου",
      sources=[E + ("sacred-royal-patriarchal-and-stavropegic-monastery-of-"
                    "saint-anastasia-pharmakolytria-in-chakidiki/"),
               EG + ("iera-vasiliki-patriarxiki-stayropigiaki-moni-agias-"
                     "anastasias/"), MON_LIST]),
 dict(id="ep-mon-vlatades", parent="constantinople",
      name=("Sacred Royal, Patriarchal and Stavropegic Monastery of "
            "Vlatades in Thessaloniki"),
      local=u"Ἱερά Βασιλική Πατριαρχική καί Σταυροπηγιακή Μονή Βλατάδων ἐν Θεσσαλονίκῃ",
      seat="Thessaloniki", country="GR", checked="2026-09-14",
      address=[u"Ἑπταπυργίου 64",
               u"54634 Θεσσαλονίκη"],
      founded=u"Ἱδρύθη περί τό ἔτος 1350 ὑπό τῶν ἀδελφῶν Δωροθέου καί Μάρκου Βλατ(τ)έων ἤ Βλατάδων, μαθητῶν καί φίλων τοῦ Ἁγίου Γρηγορίου Παλαμᾶ",
      sources=[E + ("sacred-royal-patriarchal-and-stavropegic-monastery-of-"
                    "vlatades-in-thessaloniki/"),
               EG + "iera-vasiliki-patriarxiki-stayropigiaki-moni-vlatadon/",
               MON_LIST]),
 dict(id="ep-mon-essex", parent="constantinople",
      name=("Sacred Patriarchal and Stavropegic Monastery of the Venerable "
            "Forerunner in Essex, UK"),
      local=u"Ιερά Πατριαρχική καί Σταυροπηγιακή Μονή τοῦ Τιμίου Προδρόμου ἐν Ἔσσεξ Ἀγγλίας",
      seat="Tolleshunt Knights", country="GB", checked="2026-09-14",
      address=["The Old Rectory, Rectory Road",
               "Tolleshunt Knights, by Maldon",
               "Essex CM 9 8EZ"],
      sources=[E + ("sacred-patriarchal-and-stavropegic-monastery-of-the-"
                    "venerable-forerunner-in-essex-uk/"),
               EG + "iera-patriarxiki-stayropigiaki-moni-timioy-prodromoy/",
               MON_LIST]),
 dict(id="ep-mon-alabama", parent="constantinople",
      name=("Sacred Patriarchal and Stavropegic Monastery of the Entry of "
            "the Theotokos in Alabama, USA"),
      local=u"Ιερά Πατριαρχική καί Σταυροπηγιακή Μονή τῶν Εἰσοδίων τῆς Θεοτόκου ἐν Ἀλαμπάμᾳ Η.Π.Α.",
      country="US", checked="2026-09-14",
      address=["Malbis Plantation", "Darpline Alabama"],
      sources=[E + ("sacred-patriarchal-and-stavropegic-monastery-of-the-"
                    "entry-of-the-theotokos-in-alabama-usa/"),
               EG + "iera-patriarxiki-stayropigiaki-moni-esodion-theotokoy/",
               MON_LIST]),
 dict(id="ep-mon-st-irene", parent="constantinople",
      name=("Sacred Patriarchal and Stavropegic Monastery of Saint Irene "
            "Chrysovalantou in Astoria, NY, USA"),
      local=u"Ἱερά Πατριαρχική καί Σταυροπηγιακή Μονή τῆς Ὁσίας Εἰρήνης τοῦ Χρυσοβαλάντου ἐν Ἀστορίᾳ Νέας Ὑόρκης Η.Π.Α.",
      seat="Astoria, New York", country="US", checked="2026-09-14",
      address=["36-04 23rd Avenue", "Astoria, NY 11105-1916"],
      site="https://www.stirene.org/",
      sources=[E + ("sacred-patriarchal-and-stavropegic-monastery-of-saint-"
                    "irene-chrysovalantou-in-astoria-ny-usa/"),
               EG + ("iera-patriarchiki-kai-stayropigiaki-moni-tis-osias-"
                     "eirinis/"), "https://www.stirene.org/"]),
 dict(id="ep-mon-kyiv", parent="constantinople",
      name="Stavropegic Monastery of the Ecumenical Patriarchate in Kyiv",
      local=u"Ставропігія Вселенського Патріархату в Україні",
      seat="Kyiv", country="UA", checked="2026-09-14",
      address=[u"Андріївський узвіз 23",
               u"Київ, 04070"],
      founded=u"ἀνασυνεστήθη ὑπό τῆς Μητρός Ἐκκλησίας κατ' Ἰανουάριον 2019",
      site="https://www.stavropigiainua.org/",
      sources=[E + "stavropegic-monastery-of-the-ecumenical-patriarchate-in-kyiv/",
               EG + "stauropigion-tou-oikoumenikou-patriarheiou-en-kievo/",
               "https://www.stavropigiainua.org/"]),
]
