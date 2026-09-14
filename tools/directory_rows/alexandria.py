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
      country="EG",
      address=["P.O. Box 2006, Alexandria Egypt."],
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
      sources=[AX + "iera-mitropoli-antananarivo-kai-voreioy-madagaskaris/",
               AX + "holy-archdiocese-of-antananarivo-and-north-madagascar/?lang=en"]),

 dict(id="ax-libya", parent="alexandria",
      name="Holy Metropolis of Libya",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΛΙΒΥΗΣ",
      seat="Tripoli", country="LY",
      address=["Saint Mary's Square, Old Town, Metropolitan Church of Saint George of the Slaves"],
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
      sources=[AX + "iera-mitropoli-kalis-elpidos/",
               AX + "holy-archdiocese-of-the-cape-of-good-hope/?lang=en"]),

 dict(id="ax-zambia", parent="alexandria",
      name="Holy Metropolis of Zambia and Mozambique",
      rank="Metropolis",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΖΑΜΠΙΑΣ ΚΑΙ ΜΟΖΑΜΒΙΚΗΣ",
      seat="Lusaka", country="ZM",
      address=["P.O. Box 51333, Lusaka, Zambia"],
      sources=[AX + "iera-mitropoli-zampias/",
               AX + "holy-archdiocese-of-zamvia/?lang=en"]),

 dict(id="ax-zimbabwe", parent="alexandria",
      name="Holy Archdiocese of Zimbabwe and Angola",
      rank="Archdiocese",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΗ ΖΙΜΠΑΜΠΟΥΕ ΚΑΙ ΑΓΚΟΛΑΣ",
      seat="Harare", country="ZW",
      address=["P.O. Box 2832, Harare, Zimbabwe."],
      site="https://ierazimpampoue.com/",
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
      sources=[AX + "iera-episkopi-mpenin-togko-kai-mpoyrkina-faso/", AX_D]),

 dict(id="ax-juba", parent="alexandria",
      name="Holy Diocese of Juba and South Sudan",
      rank="Diocese",
      local=u"ΙΕΡΑ ΕΠΙΣΚΟΠΗ ΤΖΟΥΜΠΑ ΚΑΙ ΝΟΤΙΟΥ ΣΟΥΔΑΝ",
      seat="Juba", country="SS",
      address=["Plot 7JK Hai Nimra Talat. Juba-South Sudan"],
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
