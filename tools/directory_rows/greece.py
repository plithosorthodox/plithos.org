# -*- coding: utf-8 -*-
"""The dioceses of the Church of Greece.

Read on 14 September 2026 from the Church's own list of its metropolises at
ecclesiagreece.gr, and then from the Church's page for each see, and then
from each metropolis's own site where one answered. The Church's list holds
eighty-two entries: the Archdiocese of Athens and eighty-one metropolises.
Forty-six rows are written here.

THE OTHER THIRTY-SIX ARE ALREADY PUBLISHED, UNDER THE THRONE. The Church of
Greece prints the thirty-six metropolises of the "New Lands" in the same list
as its own, because it administers them; they are canonically of the
Ecumenical Patriarchate, which prints them in its own list of the eparchies
of the Throne, and `constantinople.py` holds them on that ground. The ids in
that file were read before this one was begun and every id here was checked
against them: none of the thirty-six appears twice. The arithmetic is the
check a reader can repeat - 82 entries, less 36 filed under the Throne, is
the 45 metropolises of the autocephalous territory, and the Archdiocese of
Athens makes 46.

WHERE THE NAMES COME FROM. The Church of Greece publishes its own list twice,
in Greek and in English, and `name` is the English it prints, less the word
Holy, which every entry carries and none of them distinguishes. Seventy-six
of the eighty-two have an English entry; five of the sees here do not, and one
more is filed there under a title the Church's own Greek list has since
replaced. Those six are given in English as the Greek reads, following the
spellings the English list itself uses:

  Glyfada, Ilia and Oleni, Ilion Petroupolis and Acharnai, Kifisia
  Amarousion Oropos and Marathon, and Mani have no English entry at all.

  Trikki, Gardiki and Pyli stands in the English list as "Trikki and Stagoi",
  which is the see as it was before Stagoi and Meteora was set up as a
  metropolis of its own. Stagoi and Meteora has its own row and its own
  English entry, so publishing the older title would have put one place in
  two sees. Thebes carries a smaller version of the same fault: the English
  list stops at "Thevai and Levadeia" where the Greek list, and the
  metropolis itself, say Thebes, Levadeia and Aulis.

`local` is the Greek the Church of Greece prints, with the style word the
Church uses before it. Six metropolises style themselves differently on their
own sites, and where that happens the row cites the site as well so a reader
can see both:

  Kythira writes itself Ιερά Μητρόπολις Κυθήρων και Αντικυθήρων.
  Nea Ionia and Philadelphia writes itself Ιερά Μητρόπολις Νέας Ιωνίας,
    Φιλαδελφείας, Ηρακλείου και Χαλκηδόνος.
  Kifisia writes itself without Marathon, and Ilion puts Acharnai before
    Petroupolis.
  Trikki still writes itself Ιερά Μητρόπολις Τρίκκης και Σταγών, the title
    its own Church has replaced.
  Aitolia is the one place the Church's Greek list is the short form: it
    prints Αιτωλίας where its English list prints Aitolia and Acarnania and
    the metropolis prints Αιτωλίας και Ακαρνανίας. The full name is written.

ADDRESSES are the lines the Church prints, in the order it prints them, set
out as an envelope wants them and translated nowhere. Nothing is added to
them and nothing is tidied: Nea Smyrni is printed with the city's name cut
short, and stands as printed; Kalavryta prints its post box after its
postcode, and keeps it there; Ilion gives an address it marks as temporary,
and it is the only one the Church gives. Ten sees are published with a
locality and a postcode and no street, which is all the Church prints.

SITES. Thirty-six metropolises answered here and carry their own link, and so
does the Archdiocese of Athens. The other nine fall back to the Church of
Greece, and three of those are worth naming because the reason differs:

  Kefallinia's published address, imk.gr, is no longer the metropolis's. It
    answers, and what answers is a blog about video game codes. The domain
    has been lost and the row must not point at it.
  Mantineia and Kynouria's published address, immk.gr, returns a suspended
    account. The metropolis answers at immk.org instead, under its own name,
    and the row uses that and cites it. It prints a different street number
    and postcode than the Church does; the Church's is the address published
    here, and both pages are cited.
  Argolis, Glyfada, Ilia, Thebes and Messinia publish real sites that would
    not answer from here - a certificate, a redirect loop, a challenge page.
    Messinia answered at its bare domain and carries its link; the other four
    are to be re-checked rather than written off.

No clergy names, not the ruling metropolitan's, per docs/DIRECTORY.md.
"""

# The Church of Greece's own two lists of its dioceses, and the page it keeps
# for each see. A row cites the Greek page it was read from, the English entry
# its name is printed in, and the metropolis's own site where that answered.
G = "http://www.ecclesiagreece.gr/ecclesiajoomla/index.php/el/metropoleis/"
E = "http://www.ecclesiagreece.gr/ecclesiajoomla/index.php/en/dioceses/"
H = "holy-metropolis-of-"

ROWS = [

 # ----------------------------------------------- the Archdiocese of Athens
 dict(id="gr-athens", parent="greece",
      name="Archdiocese of Athens",
      local=u"Ιερά Αρχιεπισκοπή Αθηνών",
      seat="Athens", country="GR",
      address=[u"Οδ. Αγίας Φιλοθέης 21", u"Τ.Κ. 105 56", u"Αθήνα"],
      site="https://www.iaath.gr/",
      sources=[G, "https://www.iaath.gr/",
               "https://www.iaath.gr/index.php/dimosiotita/epikoinonia"]),

 # ------------------------- the metropolises of the autocephalous territory
 dict(id="gr-aitolia", parent="greece",
      name="Metropolis of Aitolia and Acarnania",
      local=u"Ιερά Μητρόπολις Αιτωλίας και Ακαρνανίας",
      seat="Missolonghi", country="GR",
      address=[u"Αρχιεπ. Δαμασκηνού 10", u"Ι.Π.Μεσολογγίου Τ.Κ.: 302 00"],
      site="https://imaa.gr/",
      sources=[G + "aitolias", E + H + "aitolia-and-acarnania",
               "https://imaa.gr/"]),
 dict(id="gr-argolis", parent="greece",
      name="Metropolis of Argolis",
      local=u"Ιερά Μητρόπολις Αργολίδος",
      seat="Nafplio", country="GR",
      address=[u"Βασιλέως Κων/νου 31", u"Ναύπλιο. Τ.Κ.: 21100"],
      sources=[G + "iera-metropole-argolidos", E + H + "argolis"]),
 dict(id="gr-arta", parent="greece",
      name="Metropolis of Arta",
      local=u"Ιερά Μητρόπολις Άρτης",
      seat="Arta", country="GR",
      address=[u"Εμμανουήλ Ξάνθου 2", u"Τ.Κ. 47100 - Άρτα"],
      site="https://www.imartis.gr/",
      sources=[G + "iera-metropole-artes", E + H + "arta",
               "https://www.imartis.gr/"]),
 dict(id="gr-glyfada", parent="greece",
      name="Metropolis of Glyfada",
      local=u"Ιερά Μητρόπολις Γλυφάδας",
      seat="Voula", country="GR",
      address=[u"Β. Παύλου 2", u"Τ.Κ. 16673 - Βούλα"],
      sources=[G + "glyphadas"]),
 dict(id="gr-gortys", parent="greece",
      name="Metropolis of Gortys and Megalopolis",
      local=u"Ιερά Μητρόπολις Γόρτυνος και Μεγαλοπόλεως",
      seat="Dimitsana", country="GR",
      address=[u"Δημητσάνα. Τ.Κ.: 22007"],
      site="https://imgortmeg.gr/",
      sources=[G + "gortynos-kai-megalopoleos",
               E + H + "gortys-and-megalopolis", "https://imgortmeg.gr/"]),
 dict(id="gr-demetrias", parent="greece",
      name="Metropolis of Demetrias and Almyros",
      local=u"Ιερά Μητρόπολις Δημητριάδος και Αλμυρού",
      seat="Volos", country="GR",
      address=[u"Βόλος. Συνεδριακό Κέντρο Θεσσαλίας",
               u"Μελισσιάτικα, Ν. Ιωνίας Μαγνησίας",
               u"Τ.Θ.1308. Τ.Κ. 38001"],
      site="https://imd.gr/",
      sources=[G + "demetriados-kai-almyrou",
               E + H + "demetrias-and-almyros", "https://imd.gr/"]),
 dict(id="gr-zakynthos", parent="greece",
      name="Metropolis of Zakynthos and Strophades",
      local=u"Ιερά Μητρόπολις Ζακύνθου και Στροφάδων",
      seat="Zakynthos", country="GR",
      address=[u"Ελ. Βενιζέλου 3", u"Τ.Κ. 29100 - Ζάκυνθος"],
      site="https://www.imzante.gr/",
      sources=[G + "zakynthou-kai-strophadon",
               E + H + "zakynthos-and-strophades", "https://www.imzante.gr/"]),
 dict(id="gr-ilia", parent="greece",
      name="Metropolis of Ilia and Oleni",
      local=u"Ιερά Μητρόπολις Ηλείας και Ωλένης",
      seat="Pyrgos", country="GR",
      address=[u"28ης Οκτωβρίου 54", u"Τ.Κ. 27100 - Πύργος"],
      sources=[G + "eleias-kai-olenes"]),
 dict(id="gr-thessaliotis", parent="greece",
      name="Metropolis of Thessaliotis and Fanariofersala",
      local=u"Ιερά Μητρόπολις Θεσσαλιώτιδος και Φαναριοφερσάλων",
      seat="Karditsa", country="GR",
      address=[u"Μητρ. Ιεζεκιήλ 30", u"Τ.Κ. 43100, Καρδίτσα"],
      site="https://www.imthf.gr/",
      sources=[G + "thessaliotidos-kai-phanariophersalon",
               E + H + "thessaliotis-and-fanariofersala",
               "https://www.imthf.gr/"]),
 dict(id="gr-thebes", parent="greece",
      name="Metropolis of Thevai, Levadeia and Aulis",
      local=u"Ιερά Μητρόπολις Θηβών, Λεβαδείας και Αυλίδος",
      seat="Livadeia", country="GR",
      address=[u"Πλατεία Αθανασίου Διάκου", u"Τ.Κ. 32100 Λιβαδειά"],
      sources=[G + "thebon-lebadeias-kai-aulidos",
               E + H + "thevai-and-levadeia"]),
 dict(id="gr-thera", parent="greece",
      name="Metropolis of Thera, Amorgos, and Nisoi",
      local=u"Ιερά Μητρόπολις Θήρας, Αμοργού και Νήσων",
      seat="Fira", country="GR",
      address=[u"Φηρά Θήρας. Τ.Κ. 84700"],
      site="https://imthiras.gr/",
      sources=[G + "theras-amorgou-kai-neson",
               E + H + "thera-amorgos-and-nisoi", "https://imthiras.gr/"]),
 dict(id="gr-ilion", parent="greece",
      name="Metropolis of Ilion, Petroupolis and Acharnai",
      local=u"Ιερά Μητρόπολις Ιλίου, Πετρουπόλεως και Αχαρνών",
      seat="Ilion", country="GR",
      address=[u"Αγίου Γεωργίου 5", u"13451 Καματερό"],
      site="https://imiliou.gr/",
      sources=[G + "iliou-petroupoleos-kai-acharnon", "https://imiliou.gr/"]),
 dict(id="gr-kaisariani", parent="greece",
      name="Metropolis of Kaisariani, Vyron and Ymittos",
      local=u"Ιερά Μητρόπολις Καισαριανής, Βύρωνος και Υμηττού",
      seat="Kaisariani", country="GR",
      address=[u"Υμηττού 47-51", u"Τ. Κ. 16121 Καισαριανή"],
      site="https://imkby.gr/",
      sources=[G + "kaisarianes-byronos-kai-ymettou",
               E + H + "kaisariani-vyron-and-ymittos", "https://imkby.gr/"]),
 dict(id="gr-kalavryta", parent="greece",
      name="Metropolis of Kalavryta and Aigialeia",
      local=u"Ιερά Μητρόπολις Καλαβρύτων και Αιγιαλείας",
      seat="Aigio", country="GR",
      address=[u"Ρωμανιώλη 43", u"Τ.Κ. 25100 - Αίγιο Αχαίας", u"Τ.Θ. 83"],
      site="https://www.imkalaig.gr/",
      sources=[G + "kalabryton-kai-aigialeias",
               E + H + "kalavryta-and-aigialeia",
               "https://www.imkalaig.gr/"]),
 dict(id="gr-karpenision", parent="greece",
      name="Metropolis of Karpenision",
      local=u"Ιερά Μητρόπολις Καρπενησίου",
      seat="Karpenisi", country="GR",
      address=[u"Δημοκρατίας 1", u"Τ.Κ. 36100 - Καρπενήσι"],
      site="https://imkarpenisiou.gr/cms/",
      sources=[G + "karpenesiou", E + H + "karpenision",
               "https://imkarpenisiou.gr/cms/"]),
 dict(id="gr-karystia", parent="greece",
      name="Metropolis of Karystia and Skyros",
      local=u"Ιερά Μητρόπολις Καρυστίας και Σκύρου",
      seat="Kymi", country="GR",
      address=[u"Κύμη. Τ.Κ. 34003"],
      sources=[G + "karystias-kai-skyrou", E + H + "karystia-and-skyros"]),
 dict(id="gr-kerkyra", parent="greece",
      name="Metropolis of Kerkyra, Paxoi and Diapontioi Nisoi",
      local=u"Ιερά Μητρόπολις Κερκύρας, Παξών και Διαποντίων Νήσων",
      seat="Corfu", country="GR",
      address=[u"Αρσενίου 1, Τ.Θ. 447", u"Τ.Κ. 49100 Κέρκυρα"],
      site="https://imcorfu.gr/",
      sources=[G + "kerkyras-paxon-kai-diapontion-neson",
               E + H + "kerkyra-paxoi-and-diapontioi-nisoi",
               "https://imcorfu.gr/"]),
 dict(id="gr-kefallinia", parent="greece",
      name="Metropolis of Kefallinia",
      local=u"Ιερά Μητρόπολις Κεφαλληνίας",
      seat="Argostoli", country="GR",
      address=[u"Γερμανού Καλλιγά 1", u"Τ.Κ. 28100 - Αργοστόλι"],
      sources=[G + "kephallenias", E + H + "kefallinia"]),
 dict(id="gr-kifisia", parent="greece",
      name="Metropolis of Kifisia, Amarousion, Oropos and Marathon",
      local=u"Ιερά Μητρόπολις Κηφισίας, Αμαρουσίου, Ωρωπού και Μαραθώνος",
      seat="Kifisia", country="GR",
      address=[u"Γρηγ. Λαμπράκη 32", u"Τ.Κ. 145 10 Κηφισιά"],
      site="https://www.imkifissias.gr/",
      sources=[G + "kephisias-amarousiou-oropou-kai-marathonos",
               "https://www.imkifissias.gr/"]),
 dict(id="gr-korinthos", parent="greece",
      name="Metropolis of Korinthos, Sikion, Zemenon, Tarsos and Polyfengos",
      local=u"Ιερά Μητρόπολις Κορίνθου, Σικιώνος, Ζεμενού, Ταρσού "
            u"και Πολυφέγγους",
      seat="Corinth", country="GR",
      address=[u"Πυλαρινού 76", u"Τ.Κ. 20100 Κόρινθος"],
      site="https://imkorinthou.org/",
      sources=[G + "korinthou-sikionos-zemenou-tarsou-kai-polyphengous",
               E + H + "korinthos-sikion-zemenon-tarsos-and-polyfengos",
               "https://imkorinthou.org/"]),
 dict(id="gr-kythira", parent="greece",
      name="Metropolis of Kythira",
      local=u"Ιερά Μητρόπολις Κυθήρων",
      seat="Kythira", country="GR",
      address=[u"Χώρα Κυθήρων", u"Τ. Κ. 80100"],
      site="https://www.imkythiron.gr/index.php/el/",
      sources=[G + "kytheron", E + H + "kythira",
               "https://www.imkythiron.gr/index.php/el/"]),
 dict(id="gr-larisa", parent="greece",
      name="Metropolis of Larisa and Tyrnavos",
      local=u"Ιερά Μητρόπολις Λαρίσης και Τυρνάβου",
      seat="Larissa", country="GR",
      address=[u"Ιωαννίνων 3", u"Τ.Κ. 41334 Λάρισα"],
      site="https://imlarisis.gr/",
      sources=[G + "larises-kai-tyrnabou", E + H + "larisa-and-tyrnavos",
               "https://imlarisis.gr/"]),
 dict(id="gr-lefkas", parent="greece",
      name="Metropolis of Lefkas and Ithaki",
      local=u"Ιερά Μητρόπολις Λευκάδος και Ιθάκης",
      seat="Lefkada", country="GR",
      address=[u"Τ.Κ. 31100 Λευκάδα"],
      site="https://imli.gr/",
      sources=[G + "leukados-kai-ithakes", E + H + "lefkas-and-ithaki",
               "https://imli.gr/"]),
 dict(id="gr-mani", parent="greece",
      name="Metropolis of Mani",
      local=u"Ιερά Μητρόπολις Μάνης",
      seat="Gytheio", country="GR",
      address=[u"Γύθειο. Τ.Κ.: 23200"],
      site="https://www.im-manis.gr/index.php/el/",
      sources=[G + "manes", "https://www.im-manis.gr/index.php/el/"]),
 dict(id="gr-mantineia", parent="greece",
      name="Metropolis of Mantineia and Kynouria",
      local=u"Ιερά Μητρόπολις Μαντινείας και Κυνουρίας",
      seat="Tripoli", country="GR",
      address=[u"Οδός Πατρ. Γρηγορίου Ε' 13-15", u"Τ.Κ. 22100 Τρίπολη"],
      site="https://www.immk.org/",
      sources=[G + "mantineias-kai-kynourias",
               E + H + "mantineia-and-kynouria", "https://www.immk.org/"]),
 dict(id="gr-megara", parent="greece",
      name="Metropolis of Megara and Salamis",
      local=u"Ιερά Μητρόπολις Μεγάρων και Σαλαμίνος",
      seat="Megara", country="GR",
      address=[u"Ὁδός: Ἁγίου Λαυρεντίου 1", u"Τ.Κ. 19100, Μέγαρα"],
      site="https://www.immesa.gr/",
      sources=[G + "megaron-kai-salaminos", E + H + "megara-and-salamis",
               "https://www.immesa.gr/"]),
 dict(id="gr-mesogaia", parent="greece",
      name="Metropolis of Mesogaia and Lavreotiki",
      local=u"Ιερά Μητρόπολις Μεσογαίας και Λαυρεωτικής",
      seat="Spata", country="GR",
      address=[u"Σπάτα. Θουκυδίδου και Βυζαντίου", u"Τ.Κ. 19004"],
      site="https://imml.gr/",
      sources=[G + "mesogaias-kai-laureotikes",
               E + H + "mesogaia-and-lavreotiki", "https://imml.gr/"]),
 dict(id="gr-messinia", parent="greece",
      name="Metropolis of Messinia",
      local=u"Ιερά Μητρόπολις Μεσσηνίας",
      seat="Kalamata", country="GR",
      address=[u"Οδός Μητροπολίτου Μελετίου 13", u"Τ. Κ. 24100 Καλαμάτα"],
      site="https://mmess.gr/",
      sources=[G + "messenias", E + H + "messinia", "https://mmess.gr/"]),
 dict(id="gr-monemvasia", parent="greece",
      name="Metropolis of Monemvasia and Sparta",
      local=u"Ιερά Μητρόπολις Μονεμβασίας και Σπάρτης",
      seat="Sparta", country="GR",
      address=[u"Λυσάνδρου 5", u"Τ. Κ. 23100 Σπάρτη"],
      site="https://immspartis.gr/",
      sources=[G + "monembasias-kai-spartes",
               E + H + "monemvasia-and-sparta", "https://immspartis.gr/"]),
 dict(id="gr-nafpaktos", parent="greece",
      name="Metropolis of Nafpaktos and Agios Vlasios",
      local=u"Ιερά Μητρόπολις Ναυπάκτου και Αγίου Βλασίου",
      seat="Nafpaktos", country="GR",
      address=[u"Γ. Αθανασιάδη-Νόβα 1", u"Τ. Κ. 30300 Ναύπακτος"],
      site="https://www.parembasis.gr/",
      sources=[G + "naupaktou-kai-agiou-blasiou",
               E + H + "nafpaktos-and-agios-vlasios",
               "https://www.parembasis.gr/"]),
 dict(id="gr-nea-ionia", parent="greece",
      name="Metropolis of Nea Ionia and Philadelphia",
      local=u"Ιερά Μητρόπολις Νέας Ιωνίας και Φιλαδελφείας",
      seat="Nea Ionia", country="GR",
      address=[u"Λεωφ. Ηρακλείου 340", u"Τ.Κ. 14231 Νέα Ιωνία"],
      site="https://www.nif.gr/",
      sources=[G + "neas-ionias-kai-philadelpheias",
               E + H + "nea-ionia-and-philadelphia", "https://www.nif.gr/"]),
 dict(id="gr-nea-smyrni", parent="greece",
      name="Metropolis of Nea Smyrni",
      local=u"Ιερά Μητρόπολις Νέας Σμύρνης",
      seat="Nea Smyrni", country="GR",
      address=[u"Αγίου Ανδρέου 14", u"171 22, Νέ Σμύρνη"],
      site="http://www.imns.gr/",
      sources=[G + "neas-smyrnes", E + H + "nea-smyrni",
               "http://www.imns.gr/"]),
 dict(id="gr-nikaia", parent="greece",
      name="Metropolis of Nikaia",
      local=u"Ιερά Μητρόπολις Νικαίας",
      seat="Nikaia", country="GR",
      address=[u"Κύπρου & Ιωνίας Νίκαια", u"Τ.Κ. 18450"],
      sources=[G + "nikaias", E + H + "nikaia"]),
 dict(id="gr-paronaxia", parent="greece",
      name="Metropolis of Paronaxia",
      local=u"Ιερά Μητρόπολις Παροναξίας",
      seat="Naxos", country="GR",
      address=[u"Χώρα Νάξου", u"Τ. Κ. 84300 - Νάξος"],
      site="http://www.i-m-paronaxias.gr/paronaxia/index.php/el/",
      sources=[G + "paronaxias", E + H + "paronaxia",
               "http://www.i-m-paronaxias.gr/paronaxia/index.php/el/"]),
 dict(id="gr-patrai", parent="greece",
      name="Metropolis of Patrai",
      local=u"Ιερά Μητρόπολις Πατρών",
      seat="Patras", country="GR",
      address=[u"Βότση 34. Τ.Θ.: 2155", u"Τ.Κ.: 26221 Πάτρα"],
      site="https://i-m-patron.gr/",
      sources=[G + "patron", E + H + "patrai", "https://i-m-patron.gr/"]),
 dict(id="gr-peiraeus", parent="greece",
      name="Metropolis of Peiraeus",
      local=u"Ιερά Μητρόπολις Πειραιώς",
      seat="Piraeus", country="GR",
      address=[u"Ακτή Θεμιστοκλέους 190", u"Τ. Κ. 18539 Πειραιάς"],
      site="https://imp.gr/",
      sources=[G + "peiraios", E + H + "peiraeus", "https://imp.gr/"]),
 dict(id="gr-peristerion", parent="greece",
      name="Metropolis of Peristerion",
      local=u"Ιερά Μητρόπολις Περιστερίου",
      seat="Peristeri", country="GR",
      address=[u"Χαλκοκονδύλη και Εθνικής Αντιστάσεως 96", u"Τ.Κ. 12131"],
      site="https://imperisteriou.gr/",
      sources=[G + "peristeriou", E + H + "peristerion",
               "https://imperisteriou.gr/"]),
 dict(id="gr-stagoi", parent="greece",
      name="Metropolis of Stagoi and Meteora",
      local=u"Ιερά Μητρόπολις Σταγών και Μετεώρων",
      seat="Kalambaka", country="GR",
      address=[u"Βλαχάβα 43", u"Τ. Κ. 42200 - Καλαμπάκα"],
      sources=[G + "stagon-kai-meteoron", E + H + "stagoi-and-meteora"]),
 dict(id="gr-syros", parent="greece",
      name="Metropolis of Syros, Tinos, Andros, Kea and Milos",
      local=u"Ιερά Μητρόπολις Σύρου, Τήνου, Άνδρου, Κέας και Μήλου",
      seat="Ermoupoli", country="GR",
      address=[u"Σταματίου Βαφειαδάκη 2", u"Τ. Κ. 84100 - Ερμούπολη Σύρου"],
      site="http://www.imsyrou.gr/index.php/el/",
      sources=[G + "syrou-tenou-androu-keas-kai-melou",
               E + H + "syros-tinos-andros-kea-and-milos",
               "http://www.imsyrou.gr/index.php/el/"]),
 dict(id="gr-trikki", parent="greece",
      name="Metropolis of Trikki, Gardiki and Pyli",
      local=u"Ιερά Μητρόπολις Τρίκκης, Γαρδικίου και Πύλης",
      seat="Trikala", country="GR",
      address=[u"Απόλλωνος 19", u"Τ. Κ. 42100 Τρίκαλα"],
      site="https://imtks.gr/index.php/el/",
      sources=[G + "trikkes-gardikiou-kai-pyles",
               "https://imtks.gr/index.php/el/"]),
 dict(id="gr-triphylia", parent="greece",
      name="Metropolis of Triphylia and Olympia",
      local=u"Ιερά Μητρόπολις Τριφυλίας και Ολυμπίας",
      seat="Kyparissia", country="GR",
      address=[u"Κυπαρισσία. Τ. Κ. 24500"],
      sources=[G + "triphylias-kai-olympias",
               E + H + "triphylia-and-olympia"]),
 dict(id="gr-ydra", parent="greece",
      name="Metropolis of Ydra, Spetsai and Aigina",
      local=u"Ιερά Μητρόπολις Ύδρας, Σπετσών και Αιγίνης",
      seat="Hydra", country="GR",
      address=[u"Ύδρα. Τ. Κ. 18040"],
      site="https://imhydra.gr/",
      sources=[G + "ydras-spetson-kai-aigines",
               E + H + "ydra-spetsai-and-aigina", "https://imhydra.gr/"]),
 dict(id="gr-fthiotis", parent="greece",
      name="Metropolis of Fthiotis",
      local=u"Ιερά Μητρόπολις Φθιώτιδος",
      seat="Lamia", country="GR",
      address=[u"Λαμία. Τ. Κ. 35100"],
      site="https://www.imfth.gr/",
      sources=[G + "phthiotidos", E + H + "fthiotis",
               "https://www.imfth.gr/"]),
 dict(id="gr-phokis", parent="greece",
      name="Metropolis of Phokis",
      local=u"Ιερά Μητρόπολις Φωκίδος",
      seat="Amfissa", country="GR",
      address=[u"Άμφισσα. Τ. Κ. 33100"],
      site="http://www.imfokid.gr/",
      sources=[G + "phokidos", E + H + "phokis", "http://www.imfokid.gr/"]),
 dict(id="gr-chalkis", parent="greece",
      name="Metropolis of Chalkis",
      local=u"Ιερά Μητρόπολις Χαλκίδος",
      seat="Chalkida", country="GR",
      address=[u"Βάκη 21", u"Τ.Κ. 34100 - Χαλκίδα"],
      site="http://www.imchalkidos.gr/",
      sources=[G + "chalkidos", E + H + "chalkis",
               "http://www.imchalkidos.gr/"]),
]
