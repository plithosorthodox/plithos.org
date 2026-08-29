# -*- coding: utf-8 -*-
"""Swahili calendar entries. TEXT = {English name: {type, life, patron}}.

The calendar's life is the short one the day panel shows; the long one is in
tools/saint_lives/sw.py, and a saint is written in both places at once so
that neither has to be come back to.

Only the fields that have been written are given; anything absent falls back
to the English.
"""
TEXT = {

"10 Holy Martyrs of Crete":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Kumi Watakatifu wa Krete - Theodulo, Saturnino, Euporo, Gelasio, Eunikiano, Zotiko, Pompio, Agathopo, Basilide na Evaristo - waliteseka mwaka wa 250 chini ya mfalme Desio, ambaye mtawala wake katika kisiwa kile, Desio naye kwa jina na kwa ukatili, alijitwika kuing'oa imani katika Krete.", "patron": "Maombezi yao huombwa kwa ajili ya furaha mbele ya kifo; taji iliyoshindaniwa katika upendo."},

"12 Greeks who built the Dormition Cathedral in the Kyiv Caves, Far Caves, Lavra":
{"type": "Wajenzi wakuu, watawa · karne ya 11", "life": "Wagiriki Kumi na Wawili waliojenga kanisa kuu la Kulala la Mapango ya Kyiv wanaadhimishwa siku hii, mafundi wakuu wa Konstantinopoli ambao Mzazi-Mungu mwenyewe aliwaajiri kwa kazi kubwa kuliko zote za ujenzi katika Urusi ya kale. Paterikoni ya Mapango imehifadhi ushuhuda wao wenyewe waliouapia: Malkia wa Mbinguni aliwatokea katika kanisa la Blakerne huko Konstantinopoli, kwa sura ya malkia akiwa amezungukwa na askari, akawaamuru waende Urusi, Kyiv, wakajenge huko kanisa kwa heshima yake mahali watakapoonyeshwa.", "patron": "Maombezi yao huombwa kwa ajili ya wajenzi; wasanifu majengo."},

"120 Martyrs of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Mia Moja na Ishirini Watakatifu wa Persia waliteseka katika mateso makuu ya Mfalme Sapori wa Pili, karibu mwaka wa 344, katika miaka ambayo ufalme wa Persia, ukiwa vitani na himaya ya Warumi iliyokuwa imekuwa ya Kikristo karibuni, uligeukia Kanisa lililo ndani ya mipaka yake kama kwa koloni la adui, na wakiri wa Kristo katika Mesopotamia na Persia wakakamatwa kwa maelfu.", "patron": "Maombezi yao huombwa kwa ajili ya mateka; vikundi vya wakiri."},

"1st Saturday of Great Lent: The Miracle of the Boiled Wheat":
{"type": "Sikukuu · karne ya 4", "life": "Jumamosi ya kwanza ya Kwaresima Kuu Kanisa linaadhimisha muujiza wa ngano iliyochemshwa, koliva, uliotendwa na Shahidi Mkuu Theodoro Askari Mpya nusu karne baada ya shahada yake mwenyewe, askari wa Kristo aliyekufa akilinda juma la kwanza la kufunga la Kanisa.", "patron": "Huombwa kwa ajili ya wote wanaoshika Mfungo; waliojaribiwa na kudanganywa."},

"1st Sunday of Great Lent: Sunday of Orthodoxy":
{"type": "Sikukuu · karne ya 9", "life": "Dominika ya kwanza ya Kwaresima Kuu Kanisa linaadhimisha Dominika ya Uorthodoksi, sikukuu ya Ushindi wa imani ya kweli, iliyowekwa mwaka wa 843 wakati malkia mtakatifu Theodora na Patriaki mtakatifu Methodio waliporudisha heshima ya ikoni na kuumaliza uzushi mkuu wa mwisho wa ulimwengu wa kale.", "patron": "Huombwa kwa ajili ya Kanisa lote lililo vitani; wote wanaoshika imani ya Mababa."},

"20,000 Martyrs of Nicomedia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu 20,000 wa Nikomedia waliteseka mwaka wa 302, wakati mfalme Maksimiano, alipojifunza jinsi imani ilivyokuwa imekua kwa nguvu katika mji wake mkuu mwenyewe, alipoazimia kuwaangamiza Wakristo wa mji katika usiku mmoja, na akauchagua usiku ambao wangekusanyika wote: sikukuu ya Kuzaliwa kwa Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya makutaniko yaliyo hatarini; wanaofundishwa imani."},

"26 Martyrs in the Crimea":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Ishirini na Sita Watakatifu, ambao masalia yao yaliitakasa Krimea, waliteseka katika nchi ya Wagothi ng'ambo ya Danube karibu mwaka wa 375, wakati mfalme mpagani wa Wagothi alipoinua mateso dhidi ya Wakristo wa watu wake, na kanisa changa la Wagothi, lililopandwa na mateka na wamisionari, likalipa gharama yake kubwa ya kwanza kwa damu.", "patron": "Maombezi yao huombwa kwa ajili ya makutaniko yaliyo katika ibada; mataifa yaliyoongoka karibuni."},

"2nd Sunday of Great Lent: St Gregory Palamas":
{"type": "Sikukuu · karne ya 14", "life": "Dominika ya pili ya Kwaresima Kuu Kanisa linaadhimisha kumbukumbu ya Mtakatifu Gregorio Palama, Askofu Mkuu wa Thesalonike, na siku ile inaitwa kwa haki Ushindi wa pili wa Uorthodoksi, kwa maana inaupanua wa kwanza: kama Dominika ya kwanza inavyotangaza kwamba Mungu aweza kuchorwa kwa sababu alikuwa mwanadamu kweli, ya pili inatangaza kwamba Mungu aweza kuonjwa kwa sababu anajitoa mwenyewe kweli, ikoni na nuru zikiwa hukumu mbili za imani moja.", "patron": "Huombwa kwa ajili ya wanaotafuta ukimya wa moyo na wote wanaosali; wanateolojia wa uzoefu."},

"33 Holy Martyrs of Melitene":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Thelathini na Watatu Watakatifu wa Melitene waliteseka karibu mwaka wa 290, katika utawala wa Diokletiano na Maksimiano, wakati kikosi chini ya jemadari Lisia kilipotumwa katika Kapadokia ili kuing'oa imani na kuwaandikisha wanaume wenye nguvu jeshini. Mbele yao anasimama Hieroni, mkulima wa Tiana, aliyelelewa katika uchaji na mama yake, mwanamume wa nguvu za ajabu za mwili.", "patron": "Maombezi yao huombwa kwa ajili ya wakulima; walioandikishwa jeshini."},

"3rd Sunday of Great Lent: Veneration of the Cross":
{"type": "Sikukuu · karne ya 4", "life": "Dominika ya tatu ya Kwaresima Kuu Kanisa linautoa Msalaba wenye thamani na utoao uzima na kuuweka katikati ya waamini, ukiwa umepambwa kwa maua, ili uheshimiwe katika juma linalofuata; na mahali penyewe ni teolojia yote ya siku ile, kwa maana Msalaba unapandwa katikati kabisa ya Mfungo, katikati ya siku arobaini, kama mti wa mapumziko katikati ya njia ngumu.", "patron": "Huombwa kwa ajili ya wote wanaobeba misalaba; waliochoka katikati ya safari."},

"40 Holy Martyrs of Sebaste":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Arobaini Watakatifu wa Sebaste walikuwa askari wa Jeshi maarufu la Kumi na Mbili, liitwalo la Ngurumo, lililokuwa Sebaste katika Armenia karibu mwaka wa 320, ambao sinaksario ya Bizanti inauhesabu kuwa 322 au 323, wakati mfalme Likinio, akivunja amani yake na Kanisa, aliviamuru vikosi vyake kutoa dhabihu.", "patron": "Maombezi yao huombwa kwa ajili ya askari; vikundi na udugu."},

"42 Martyrs of Ammoria in Phrygia":
{"type": "Mashahidi · karne ya 9", "life": "Mashahidi Arobaini na Wawili Watakatifu wa Amorio walikuwa majemadari na watukufu wa jeshi la Bizanti waliotekwa wakati mji mkubwa wa Amorio katika Frigia ulipoangukia mikononi mwa Wasarakeni mwaka wa 838, miongoni mwao Konstantino, Aetio, Theofilo, Theodoro, Melisseno, Kalisto na Basoe, ua la uongozi wa himaya lililochukuliwa mateka hadi Mesopotamia.", "patron": "Maombezi yao huombwa kwa ajili ya askari; majemadari."},

"45 Holy Martyrs at Nicopolis in Armenia":
{"type": "Walei · karne ya 4", "life": "Mashahidi Arobaini na Watano Watakatifu wa Nikopoli katika Armenia waliteseka chini ya mfalme Likinio, aliyeitawala Mashariki na kulitesa Kanisa kwa ukali, akiamuru kifo kwa Mkristo yeyote asiyerudi kwa sanamu. Mateso yalipoifikia Nikopoli, waamini zaidi ya arobaini, wakiongozwa na Leontio, Maurikio, Danieli, Antonio na Aleksandro, waliazimia wasijifiche bali wajitokeze wazi mbele ya watesi na kumkiri Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri wa ujasiri."},

"4th Sunday of Great Lent: St John Climacus (of the Ladder)":
{"type": "Sikukuu · karne ya 7", "life": "Dominika ya nne ya Kwaresima Kuu Kanisa linawawekea watoto wake mbele Mtakatifu Yohane wa Ngazi, abate wa Sinai na mwandishi wa Ngazi ya Kupanda kwa Kimungu, na kuwekwa kwake ni ufundishaji wa makusudi: baada ya katikati ya Mfungo, Msalaba ukiwa umekwisha heshimiwa na Pasaka bado haijaonekana, Kanisa linamtoa mchora-ramani wake mkuu wa maisha ya kiroho.", "patron": "Huombwa kwa ajili ya wote wanaopanda kuelekea Mungu; wanaopambana katikati ya Kwaresima."},

"5th Saturday of Great Lent: of the Akathist to the Theotokos":
{"type": "Sikukuu · karne ya 7", "life": "Jumamosi ya tano ya Kwaresima Kuu Kanisa linaadhimisha sikukuu ya Akathisto, likiimba mzima, katika usiku mmoja wa taadhima, wimbo mkuu kwa Mzazi-Mungu Mtakatifu Zaidi ambao katika mwaka wote mwingine huimbwa kwa sehemu; na sikukuu hii ni ukumbusho wa vita kama ilivyo ibada, kwa maana iliwekwa kwa shukrani kwa ajili ya kuokolewa kwa Konstantinopoli.", "patron": "Huombwa kwa ajili ya wote wanaomkimbilia Mzazi-Mungu; miji iliyozingirwa."},

"5th Sunday of Great Lent: St Mary of Egypt":
{"type": "Sikukuu · karne ya 6", "life": "Mtakatifu Maria wa Misri, ambaye maisha yake yanasomwa kanisani wakati wa Kwaresima Kuu kama sura ya toba, aliutumia ujana wake katika Aleksandria katika ufisadi mkubwa. Alipokwenda Yerusalemu, alijikuta amezuiwa na nguvu isiyoonekana asiingie kanisani katika Kuinuliwa kwa Msalaba, na akiwa amechomwa moyoni, alilia mbele ya ikoni ya Mzazi-Mungu na akaweka nadhiri ya kuyarekebisha maisha yake.", "patron": "Huombwa kwa ajili ya wanaotubu katika kilele cha Kwaresima; wote waliokata tamaa ya kubadilika."},

"7 Holy Maccabee Martyrs":
{"type": "Vijana · karne ya 2 KK", "life": "Ndugu saba watakatifu Wamakabayo, Abimu, Antonio, Guria, Eleazari, Eusebono, Alimo na Marcelo, waliteseka mwaka wa 166 kabla ya Kristo chini ya mfalme asiyemcha Mungu Antioko Epifane, aliyeidharau imani ya Wayahudi na kujitahidi kuwageuza watu kutoka Sheria ya Musa, akilinajisi Hekalu na kusimamisha ndani yake sanamu ya Zeu ili wote waiabudu.", "patron": "Maombezi yao huombwa kwa ajili ya uaminifu kwa sheria ya Mungu; ujasiri chini ya mateso."},

"7 Holy Youths “Seven Sleepers” of Ephesus":
{"type": "Vijana · karne ya 5", "life": "Vijana saba watakatifu wa Efeso, Maksimiliano, Iambliko, Martiniano, Yohane, Dionisio, Eksakustodiano na Antonino, waliishi katika karne ya tatu na walikuwa wana wa raia mashuhuri, marafiki tangu utoto na askari pamoja. Mfalme Desio alipofika Efeso na kuamuru wote watoe dhabihu kwa sanamu, wale saba walimkiri Kristo, na ingawa mishipi yao ya cheo ilivuliwa, mfalme aliwaacha huru kwa muda, akitumaini kwamba wangelegeza.", "patron": "Maombezi yao huombwa kwa ajili ya ufufuo wa wafu; wagonjwa wasioweza kulala."},

"Afterfeast of the Dormition of the Mother of God":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Katika siku za Baada ya Sikukuu ya Kulala kwa Mzazi-Mungu, Kanisa linaendelea kuadhimisha kulala kwa heri kwa Bibi yetu Mtakatifu Zaidi Mzazi-Mungu na kuhamishwa kwake katika utukufu hadi ufalme wa mbinguni. Nyimbo za siku hizi zinatangaza kwamba yeye aliyemzaa Mtoaji wa Uzima hakuuacha ulimwengu katika kulala kwake, bali alitwaliwa juu na Mwana wake ili atawale pamoja naye na kuwaombea bila kukoma wote wanaomheshimu.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Afterfeast of the Elevation of the Cross":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Hizi ni siku za Baada ya Sikukuu ya Kuinuliwa kwa Ulimwengu Wote kwa Msalaba wenye Thamani na Utoao Uzima, ambazo katika hizo Kanisa linaendelea kuadhimisha sikukuu kuu ya Msalaba wa Bwana. Nyimbo za Kuinuliwa zinaunganishwa na ibada za kila siku, na waamini wanaendelea kuuheshimu Mti mtakatifu ulioinuliwa katikati ya dunia, wakiitafakari siri ambayo kwayo chombo cha kifo kikawa mti wa uzima.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Afterfeast of the Entry of the Most Holy Mother of God into the Temple":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Katika siku za baada ya sikukuu ya Kuingia kwa Mzazi-Mungu Mtakatifu Zaidi Hekaluni, Kanisa linabaki ndani ya nuru ya sikukuu, likiendelea kuimba nyimbo zake na kutafakari siri yake: mtoto wa miaka mitatu, aliyeletwa na Yoakimu na Ana katika kutimiza nadhiri yao, akipanda ngazi kubwa za Hekalu bila kusaidiwa, akipokelewa na kuhani mkuu Zekaria, na kuongozwa, kinyume na desturi yote, hadi ndani ya Patakatifu pa Patakatifu penyewe, mahali sanduku na kiti cha rehema vilipokuwa zamani.", "patron": "Huombwa kwa ajili ya kudumu katika neema ya sikukuu."},

"Afterfeast of the Meeting of our Lord in the Temple":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Siku za Baada ya Sikukuu ya Kukutana kwa Bwana wetu Hekaluni zinaibeba sikukuu ya tarehe pili ya Februari katika siku zinazofuata, hadi kuagwa kwake tarehe tisa, na katika hizo Kanisa linabaki limesimama Hekaluni likiwa na Mtoto mikononi mwake; kwa maana Kukutana ndiko bawaba ambayo juu yake mzunguko wote wa Kuzaliwa unafungwa, utimizo wa siku arobaini wa sheria ya Kupata Mwili, na siri ya uzito huo haiagwi kwa siku moja.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Afterfeast of the Nativity of our Lord and Savior Jesus Christ":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Siku za Baada ya Sikukuu ya Kuzaliwa kwa Bwana wetu zinayabeba maadhimisho katika siku zinazofuata sikukuu, kwa maana Kanisa halilifungi pango la Bethlehemu baada ya siku moja bali linakaa ndani yake, likirudia katika kila ibada troparioni na kontakioni ya sikukuu, likiimba Kristo amezaliwa, mtukuzeni juu ya watakatifu wa kila siku na kazi za kila siku, hata mashahidi, maaskofu na wajinyimaji wanaoadhimishwa katika siku hizi wote wanaonwa katika nuru ya hori.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Afterfeast of the Nativity of the Mother of God":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Hizi ni siku za Baada ya Sikukuu ya Kuzaliwa kwa Mzazi-Mungu Mtakatifu Zaidi, ambazo katika hizo Kanisa linaendelea kuadhimisha kuzaliwa kwa Mzazi-Mungu kutoka kwa wenye haki Yoakimu na Ana. Nyimbo za sikukuu zinaimbwa pamoja na ibada za kila siku, zikiirefusha furaha ya sherehe, huku waamini wakitafakari kufunguliwa kwa utasa wa Ana na kuonekana ulimwenguni kwa yeye aliyekusudiwa tangu milele kuwa Mama wa Mwokozi.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Afterfeast of the Transfiguration of our Lord":
{"type": "Baada ya sikukuu · kiliturujia", "life": "Hii ni siku ya kwanza ya Baada ya Sikukuu ya Kugeuka Sura kwa Bwana, ambayo katika hiyo Kanisa linaendelea kuadhimisha utukufu uliofunuliwa juu ya mlima mtakatifu. Nyimbo za sikukuu zinakumbusha kushangaa kwa mitume Petro, Yakobo na Yohane walipomwona Bwana wao amegeuka sura mbele yao, uso wake na mavazi yake vikiangaza kuliko jua, nazo zinatangaza usawa wake na Baba, kwa maana yeye ajifunikaye nuru kama vazi aliwaonyesha wanafunzi wake mng'ao wake wa Kimungu.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Apostle Alphaeus of the Seventy":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Alfayo alikuwa mmoja wa wale Sabini ambao Bwana aliwachagua na kuwatuma mbele yake, wawili wawili, katika kila mji na mahali ambapo yeye mwenyewe angekuja, naye anaheshimiwa na Kanisa miongoni mwa daraja lile la pili la mitume ambao, baada ya wale Kumi na Wawili, waliipeleka Injili ulimwenguni kote.", "patron": "Injili iliyohubiriwa miongoni mwa wanafunzi wa kwanza."},

"Apostle Ananias of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Anania wa wale Sabini alikuwa mwanafunzi wa Bwana aliyekaa Damasko, ambaye Bwana alimtokea katika maono, akimwambia aende katika njia iitwayo Nyofu na aweke mikono juu ya Sauli wa Tarso, mtesi wa Kanisa, aliyekuwa akisali huko akiwa kipofu.", "patron": "Maombezi yake huombwa kwa ajili ya uponyaji wa upofu; utii kwa wito wa Mungu."},

"Apostle Andrew, the Holy and All-Praised First-Called":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Mwenye Sifa Zote Andrea, Aliyeitwa wa Kwanza, alikuwa wa Bethsaida katika Galilaya, mvuvi na ndugu wa Simoni Petro; na akiwa mwanafunzi wa Yohane Mtangulizi, alimsikia Mbatizaji akisema juu ya Yesu, Tazama Mwana-Kondoo wa Mungu, naye akamfuata Bwana kabla ya mitume wote, ndiyo maana Kanisa linamwita Aliyeitwa wa Kwanza.", "patron": "Maombezi yake huombwa kwa ajili ya wavuvi; wamisionari."},

"Apostle Andronicus of the Seventy and his fellow-laborer, Junia":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Androniko, mmoja wa wale Sabini, na mtenda kazi mwenzake Yunia, wamehifadhiwa majina yao kwa Kanisa na Mtakatifu Paulo mwenyewe, katika salamu ya waraka wake kwa Warumi ambapo anaandika, Wasalimuni Androniko na Yunia, jamaa zangu na wafungwa wenzangu.", "patron": "Jamaa na wafungwa wenzake wa Paulo."},

"Apostle Aquila of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Akila, mmoja wa wale Sabini, alikuwa Myahudi na mzaliwa wa Ponto aliyeishi Roma pamoja na mkewe Priskila hadi, katika utawala wa mfalme Klaudio, Wayahudi walipofukuzwa katika mji na wanandoa wale wakakaa Korintho. Huko walikutana na Mtume Paulo, ambaye, kwa kuwa alikuwa wa kazi ile ile, alifikia kwao na kufanya kazi pamoja nao katika kushona mahema, na baada ya kupokea ubatizo kutoka kwake wakawa wanafunzi wake waaminifu.", "patron": "Maombezi yao huombwa kwa ajili ya watengeneza mahema; wanandoa."},

"Apostle Aristarchus of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Aristarko wa wale Sabini alikuwa Mmakedonia wa Thesalonike na mmoja wa wenzake waaminifu kuliko wote wa Mtume Mtakatifu Paulo, aliyetajwa naye katika nyaraka zake kama mtenda kazi mwenzake na mfungwa mwenzake. Alishiriki taabu na hatari za Mtume huko Efeso, ambapo alikamatwa na umati katika ukumbi wa michezo.", "patron": "Maombezi yake huombwa kwa ajili ya watenda kazi wenzake; uaminifu katika urafiki."},

"Apostle Aristobulus of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Aristobulo wa wale Sabini, ndugu wa Mtume Barnaba, alizaliwa Kipro na alimfuata Mtume Mtakatifu Paulo, anayeisalimu nyumba yake katika Waraka kwa Warumi; na alipowekwa wakfu na Paulo, kama habari za kale zinavyosimulia, alitumwa kuwa askofu wa Britania, upande wa magharibi kabisa wa ulimwengu uliojulikana.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuangazwa kwa visiwa."},

"Apostle Aristobulus of the Seventy, Bishop of Britain":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Aristobulo wa wale Sabini alizaliwa Kipro, ndugu wa Mtume Barnaba, na pamoja na ndugu yake aliandamana na Mtume Paulo katika safari zake za umisionari, mmoja wa daraja lile la pili la mitume ambao Bwana aliwatuma mbele ya uso wake na ambao wale Kumi na Wawili waliwatawanya ulimwenguni kote baada ya Pentekoste.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari kwenda mipaka ya mbali; wahubiri wa kwanza wa nchi."},

"Apostle Barnabas of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Barnaba, mmoja wa wale Sabini, alikuwa miongoni mwa viongozi wa kwanza na wapendwa kuliko wote wa Kanisa la kitume, mwenzake wa Mtakatifu Paulo na mwanzilishi wa Kanisa la Kipro nchi yake ya kuzaliwa.", "patron": "Kisiwa cha Kipro; wanaotia moyo na kufariji."},

"Apostle Bartholomew of the Twelve":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Mwenye Sifa Zote Bartholomeo, mmoja wa wale Kumi na Wawili, kwa kawaida anashikwa na mapokeo ya Kanisa kuwa ni yeye yule Nathanaeli wa Kana ya Galilaya, Mwisraeli asiye na hila ambaye Bwana alimwona chini ya mtini kabla Filipo hajamwita.", "patron": "Nchi ya Armenia; wamisionari kwenda Mashariki."},

"Apostle Carpus of the Seventy":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Karpo alikuwa mmoja wa wale Sabini na mwenzake na msaidizi wa Mtume Paulo, na jina lake limehifadhiwa kwa Kanisa katika Maandiko kwa mkono wa Paulo mwenyewe, katika waraka wa pili kwa Timotheo.", "patron": "Joho lililotunzwa kwa ajili ya Mtume huko Troa."},

"Apostle Crescens of the Seventy":
{"type": "Askofu · karne ya 2", "life": "Mtume Mtakatifu Kreskenti, mmoja wa wale Sabini, alikuwa mwanafunzi wa Mwokozi ambaye Mtume Paulo anamtaja katika Waraka wake wa Pili kwa Timotheo, akiandika kwamba Kreskenti alikuwa amekwenda kuhubiri Galatia. Huko alifanywa askofu, na baadaye aliipeleka Injili hadi Gaula, upande wa magharibi, ambapo huko Vienne alimweka mwanafunzi wake Zakaria kuwa askofu.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri ya umisionari."},

"Apostle Epenetus of the Seventy":
{"type": "Askofu · karne ya 1", "life": "Mtume Mtakatifu Epeneto, mmoja wa wale Sabini, alikuwa mwanafunzi wa Mwokozi ambaye Mtume Paulo anamsalimu kwa upendo katika Waraka wake kwa Warumi kama Epeneto mpendwa wake, malimbuko ya Akaya kwa Kristo. Aliwekwa kuwa Askofu wa Kartago, na huko, akivumilia mateso mengi mikononi mwa waabudu sanamu, alijitaabisha kuwaleta wapagani katika ujuzi wa Mungu wa kweli, akiwavuta wengi kwenye imani.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri ya umisionari."},

"Apostle Epίmakhos of Alexandria":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Epimako wa Aleksandria alikuwa Mmisri ambaye tangu ujana wake alimpenda Bwana na akajitenga hadi eneo la Pelusio, akiishi kama mjinyimaji jangwani katika kufunga na sala. Mateso ya Desio yalipoiangukia Aleksandria, mtawa wa upweke, akiwaka bidii, alishuka mjini ili kuwatia nguvu wakiri.", "patron": "Maombezi yake huombwa kwa ajili ya uponyaji wa macho; bidii kwa ajili ya Mungu."},

"Apostle Hermas of the Seventy":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Hermas alikuwa mmoja wa wale Sabini, na jina lake nalo limehifadhiwa kwa Kanisa katika Maandiko kwa mkono wa Mtakatifu Paulo, ambaye katika salamu za mwisho za waraka wake kwa Warumi anamsalimu Hermas miongoni mwa waamini wa kanisa la Roma.", "patron": "Jina lililosalimiwa katika waraka kwa Warumi."},

"Apostle Hermes of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Hermesi wa wale Sabini ni mmoja wa watu ambao Maandiko yamewafanya wasisahaulike kwa neno moja: Mtume Paulo, akiumaliza Waraka wake kwa Warumi kwa orodha ya ndugu aliowapenda, anaandika, Wasalimuni Asinkrito, Flegoni, Hermas, Patroba, Hermesi, na ndugu walio pamoja nao; na kwa salamu ile Hermesi aliingia katika kanuni ya Maandiko, akisomwa kwa sauti katika kila kanisa la ulimwengu katika kila kizazi tangu wakati ule, wasifu mfupi kuliko wote uwezekanao na uliochapishwa kwa upana kuliko wote.", "patron": "Maombezi yake huombwa kwa ajili ya waliosalimiwa na wasiokumbukwa; maaskofu wa majimbo tulivu."},

"Apostle Herodion of the Seventy, and those with Him":
{"type": "Mitume wa Sabini · karne ya 1", "life": "Siku hii Kanisa linaadhimisha mitume sita wa wale Sabini pamoja, Herodioni, Agabo, Rufo, Asinkrito, Flegoni na Hermesi, kikundi kilichokusanywa hasa kutoka ukurasa mmoja wa Maandiko, sura ya kumi na sita ya Waraka kwa Warumi, ambapo Mtume Paulo, akilisalimu kanisa la mji mkuu jina kwa jina, bila kujua aliiandika sehemu ya kalenda ya Kanisa.", "patron": "Maombezi yao huombwa kwa ajili ya maaskofu wa upandaji wa kwanza; manabii."},

"Apostle James the Brother of Saint John the Theologian":
{"type": "Mtume, shahidi · karne ya 1", "life": "Mtume Mtakatifu Yakobo, mwana wa Zebedayo na ndugu wa Yohane Mwanateolojia, aliitwa kutoka nyavu za Galilaya pamoja na ndugu yake katika wito mmoja, wawili wale wakimwacha baba yao ndani ya mashua kwa neno moja; na Bwana aliwapa jina la ziada Boanerge, wana wa ngurumo, kwa ajili ya moto uliokuwa ndani yao ambao mara moja ulitaka kuuita moto wa mbinguni juu ya kijiji kisichokaribisha, nao ukafundishwa badala yake roho ambayo ulikuwa nayo.", "patron": "Maombezi yake huombwa kwa ajili ya mitume na wamisionari; wana wa ngurumo."},

"Apostle James, son of Alphaeus":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Yakobo, mwana wa Alfayo, alikuwa mmoja wa wale Kumi na Wawili, aliyeitwa na Bwana pamoja na wavuvi wa Galilaya, na kwa mapokeo ya Kanisa alikuwa ndugu wa Mtume na Mwinjilisti Mathayo aliyekuwa mtoza ushuru. Injili hazikuandika lolote la maneno yake, lakini matendo yake yanaujaza ukimya: baada ya Pentekoste alitoka kuhubiri.", "patron": "Maombezi yake huombwa kwa ajili ya kupanda kwa neno; kazi ya kitume."},

"Apostle James, the Brother of the Lord":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Yakobo, Ndugu wa Bwana, alikuwa mwana wa Mwenye haki Yosefu Mchumba katika ndoa yake ya kwanza, na tangu utoto alishiriki umaskini na safari za Familia Takatifu, akiandamana nao, kama mapokeo yasimuliavyo, katika kukimbilia Misri. Akiwa Mnadhiri aliyewekwa wakfu kwa Mungu, hakunywa divai, hakula nyama, na alivaa vazi moja tu, naye alisali bila kukoma Hekaluni hata magoti yake yakawa magumu kama ya ngamia, ndiyo maana Yerusalemu yote, hata walio nje ya Kanisa, walimwita Yakobo Mwenye haki.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu; watunga ibada."},

"Apostle Jude the Brother of the Lord":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Yuda, aitwaye Ndugu wa Bwana, alikuwa mmoja wa Mitume Kumi na Wawili, ajulikanaye pia kwa majina Thadayo na Lebayo, naye anaheshimiwa kama jamaa wa Kristo kwa jinsi ya mwili.", "patron": "Jamaa wa Bwana; wanaouliza jinsi Kristo anavyojulikana."},

"Apostle Justus of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Yusto wa wale Sabini, aitwaye Yosefu Barsaba, alikuwa, kwa mapokeo ya Kanisa, mwana wa Mwenye haki Yosefu Mchumba, na hivyo alihesabiwa miongoni mwa ndugu za Bwana, akikua katika kivuli cha Neno Aliyepata Mwili. Baada ya Kupaa, wale kumi na mmoja walipotafuta kuijaza nafasi ya Yuda, wawili walitolewa miongoni mwa wale waliokuwa pamoja na Bwana tangu ubatizo wa Yohane, Yosefu aitwaye Barsaba, mwenye jina la ziada Yusto, na Mathia.", "patron": "Maombezi yake huombwa kwa ajili ya kuridhika bila heshima; uaminifu usiochaguliwa."},

"Apostle Mark of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Marko wa wale Sabini, ambaye Kanisa linamtofautisha na Mwinjilisti wa jina lile lile, anatambulishwa katika mapokeo kuwa Yohane aitwaye Marko, ambaye katika nyumba ya mama yake Maria huko Yerusalemu waamini walikusanyika kwa sala, na ambako Petro alifika malaika alipomtoa gerezani.", "patron": "Maombezi yake huombwa kwa ajili ya uponyaji; utumishi wa Injili."},

"Apostle Matthias of the Seventy":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Mathiya alizaliwa Bethlehemu wa kabila la Yuda, na tangu utoto wake alifundishwa Sheria ya Mungu na Mtakatifu Simeoni Mpokea-Mungu. Bwana Yesu Kristo alipodhihirika ulimwenguni, Mathiya alimwamini kuwa ndiye Masiya na akamfuata kwa uaminifu, naye alihesabiwa miongoni mwa wale Sabini ambao Bwana aliwatuma wawili wawili mbele ya uso wake.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; uaminifu uliofichwa."},

"Apostle Nathaniel of the Seventy":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Nathanaeli, anayeadhimishwa siku hii pamoja na Luka na Klementi, ni mtu wa Kana ya Galilaya ambaye Injili ya Yohane inauhifadhi wito wake kama moja ya vito vyake: Filipo alipomkuta na habari kwamba yule aliyeandikwa juu yake na Musa na manabii amepatikana, Yesu wa Nazareti, Nathanaeli alijibu kwa chuki ya kweli ya mtu mnyofu, Laweza neno jema kutoka Nazareti, naye Filipo, bila kupoteza hoja, alisema tu, Njoo uone.", "patron": "Maombezi yake huombwa kwa ajili ya wasio na hila; wanafunzi wa Maandiko."},

"Apostle Nicanor the Deacon of the Seventy":
{"type": "Shemasi · karne ya 1", "life": "Mtume Mtakatifu Nikanoro alikuwa mmoja wa mashemasi saba wa kwanza wa Kanisa la Kristo, waliochaguliwa, kama Matendo ya Mitume yanavyoandika, wakati wale Kumi na Wawili walipouita umati wa wanafunzi na kuwaweka watu saba wenye sifa njema, waliojaa Roho Mtakatifu na hekima - Stefano, Filipo, Prokoro, Nikanoro, Timoni, Parmena na Nikolao - ili wahudumu meza na kuwatunza wajane, ili huduma ya rehema iwe na utaratibu kama huduma ya neno.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wanaohudumu mezani."},

"Apostle Onesimus of the Seventy":
{"type": "Mtume wa Sabini, shahidi · karne ya 2", "life": "Mtume Mtakatifu Onesimo wa wale Sabini ndiye mtu pekee katika Agano Jipya aliye pia mada yake, kwa maana waraka mfupi kuliko yote wa Paulo uliandikwa kumhusu yeye peke yake. Akiwa mtumwa wa Filemoni, Mkristo wa Kolosai, Onesimo alimkosea bwana wake na akakimbia, na njia ya mtoro ile iliishia, kwa maongozi yanayoziongoza njia kama hizo, huko Roma, miguuni pa Paulo aliyekuwa kifungoni.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi; waliokuwa watumwa."},

"Apostle Philip of the Seventy, One of the Seven Deacons":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Filipo wa wale Sabini, mmoja wa Mashemasi Saba, alichaguliwa pamoja na Stefano na wengine na mitume ili ahudumu meza za wajane katika Kanisa la kwanza la Yerusalemu, akiwa mtu aliyejaa imani na Roho Mtakatifu. Mateso yalipolitawanya Kanisa, Filipo alishuka Samaria na kumhubiri Kristo huko kwa ishara na maajabu, hata mji ukalipokea neno kwa furaha kubwa, na hata Simoni mchawi aliamini na akabatizwa.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wainjilisti."},

"Apostle Pudens of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Pudensi wa wale Sabini alikuwa Mroma wa cheo cha useneta, naye anasimama katika Maandiko katika salamu moja, kwa maana Mtume Paulo, akiandika waraka wake wa mwisho kutoka gereza lake la Roma, anampelekea Timotheo salamu za Eubulo, na Pudensi, na Lino, na Klaudia, mzunguko uliobaki wa Mtume aliyehukumiwa katika mji mkuu ukibanwa katika majina manne, ambayo moja lilikuwa la mwana wa seneta huyu.", "patron": "Maombezi yake huombwa kwa ajili ya wenyeji wa Kanisa; nyumba zinazokuwa makanisa."},

"Apostle Quadratus of the Seventy":
{"type": "Mtume wa Sabini · karne ya 2", "life": "Mtume Mtakatifu Kodrato wa wale Sabini alilihubiri neno la Mungu huko Athene na huko Magnesia, na alikuwa Askofu wa Athene, akiitwa na mwandishi wa maisha yake nyota ya asubuhi ing'aayo katikati ya mawingu ya upagani. Kwa mahubiri yake aliwageuza wapagani wengi kwenye imani ya kweli, na kwa ajili hiyo alivumilia mateso, kupigwa mawe na kufungwa gerezani mikononi mwa adui za Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya watetezi wa imani; utetezi wa imani."},

"Apostle Silas of the Seventy":
{"type": "Askofu · karne ya 1", "life": "Mtume Mtakatifu Sila, mmoja wa wale Sabini, alikuwa mtu aliyeheshimiwa katika Kanisa la kwanza la Yerusalemu na alihesabiwa miongoni mwa wakuu wa ndugu. Baraza la Kitume lilipokutana Yerusalemu ili liamue kwamba waliogeuka kutoka mataifa hawana haja ya kuishika Sheria ya Musa, Sila alichaguliwa, kwa kuwa amejaa neema ya Roho Mtakatifu, ili aupeleke na kuueleza uamuzi wake kwa waamini wa Antiokia.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri ya umisionari."},

"Apostle Silvanus of the Seventy":
{"type": "Askofu · karne ya 1", "life": "Mtume Mtakatifu Silvano, mmoja wa wale Sabini, alilihubiri neno la Mungu pamoja na mitume wakuu Petro na Paulo, na Mtume Petro anamtaja kwa heshima katika Waraka wake wa Kwanza, akimwita ndugu mwaminifu ambaye kwa mkono wake aliandika. Akijitaabisha katika kuieneza Injili na kuyaimarisha makanisa, Mtakatifu Silvano aliwekwa kuwa Askofu wa Thesalonike, ambapo alilichunga kundi la Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri ya umisionari."},

"Apostle Simon the Zealot":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Simoni Mwenye Bidii alikuwa mmoja wa wale Kumi na Wawili waliochaguliwa na Bwana, aitwaye na Mtakatifu Mathayo Mkananayo na na Mtakatifu Luka Mwenye Bidii, majina mawili yenye maana moja, kwa maana Mkananayo linatafsiri neno la Kiaramu ambalo Kiyunani Zelote nalo hulitafsiri.", "patron": "Bidii iliyompa jina lake."},

"Apostle Sosthenes of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Sostheni wa wale Sabini anaingia katika Maandiko mara mbili, mara moja akipigwa na mara moja akibariki, na umbali kati ya hizo mbili ndizo habari za roho yake. Katika Matendo ya Mitume yeye ni mkuu wa sinagogi huko Korintho wakati Wayahudi walipomwinukia Paulo na kumkokota mbele ya kiti cha hukumu cha liwali Galio.", "patron": "Maombezi yake huombwa kwa ajili ya walioongoka kutoka miongoni mwa wapinzani; wanaopigwa isivyo haki."},

"Apostle Tertius of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Tertio wa wale Sabini ameacha salamu yake mwenyewe ndani ya Maandiko Matakatifu, kwa maana ulikuwa mkono wake ulioandika Waraka wa Mtume Paulo kwa Warumi kwa kunenwa na Mtume, na hapo aliandika, Mimi Tertio, niliyeuandika waraka huu, nawasalimu katika Bwana - mwandishi wa barua kuu ya Injili ya neema akiwa mwenyewe neno dogo lililo hai ndani yake.", "patron": "Maombezi yake huombwa kwa ajili ya waandishi; wanakili."},

"Apostle Thaddeus of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Thadayo, mmoja wa wale Sabini, alikuwa Mwebrania kwa kuzaliwa, aliyezaliwa katika mji wa Kisyria wa Edesa; anapaswa kutofautishwa na Yuda, aitwaye pia Thadayo, aliyekuwa mmoja wa wale Kumi na Wawili. Alipofika Yerusalemu kwa sikukuu, alisikia mahubiri ya Yohane Mtangulizi na akabatizwa naye, na alipomwona Bwana Yesu alimfuata na akahesabiwa miongoni mwa wanafunzi Sabini.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; mahubiri ya umisionari."},

"Apostle Timon the Deacon of the Seventy":
{"type": "Askofu · karne ya 1", "life": "Mtume Mtakatifu Timoni alikuwa mmoja wa mashemasi saba waliowekwa na mitume, kama Matendo ya Mitume yanavyoandika, wakati wale Kumi na Wawili walipowachagua watu waliojaa Roho Mtakatifu na hekima ili wawahudumie wajane maskini wa kanisa la Yerusalemu, Stefano na Filipo wakiwa mbele yao na Timoni miongoni mwa idadi yao, watumishi wa kwanza waliowekwa wakfu kwa rehema ya Kanisa.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; maaskofu wa majimbo ya mipakani."},

"Apostle Titus of the Seventy and Bishop of Crete":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Tito, mmoja wa wale Sabini, alikuwa mzaliwa wa Krete na mwana wa familia mashuhuri ya kipagani, na katika ujana wake alijifunza falsafa na mashairi ya Wagiriki huku akijilinda na maovu yao. Akivutwa na kweli, alikuwa mwanafunzi na mtenda kazi mpendwa mwenzake wa Mtume Paulo, aliyemwita mwanawe wa kweli katika imani moja na akamweka kuwa Askofu wa kwanza wa Krete.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; Krete."},

"Apostle Trophimus of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mtume Mtakatifu Trofimo wa wale Sabini alikuwa Mgiriki wa Efeso, mmoja wa walioongoka kutoka mataifa ambao Mtume Paulo aliwafunga kwake kama wenzake wa barabarani, na Maandiko yanamwonyesha mara tatu, kila mwonekano ukiwa kituo cha ufuasi. Anaonekana kwanza miongoni mwa wajumbe walioandamana na Paulo kutoka Ugiriki kuelekea Yerusalemu wakiwa na mchango kwa watakatifu maskini, sadaka ya makanisa machanga ikisafiri chini ya ulinzi wa wana wao wenyewe.", "patron": "Maombezi yake huombwa kwa ajili ya wenzao wa wakuu; wagonjwa walioachwa nyuma."},

"Apostle and Evangelist John the Theologian":
{"type": "Mtume · karne ya 1", "life": "Mtakatifu Yohane Mwanateolojia, mwana wa Zebedayo na ndugu wa Yakobo, alikuwa mwanafunzi mpendwa wa Kristo. Aliuona Kugeuka Sura na alisimama kando ya Msalaba pamoja na Mzazi-Mungu. Aliihubiri Injili, akaandika Injili ya nne, nyaraka, na Ufunuo, naye alipumzika huko Efeso katika uzee mkubwa."},

"Apostle and Evangelist Luke":
{"type": "Mtume · karne ya 1", "life": "Mtume na Mwinjilisti Mtakatifu Luka alikuwa mzaliwa wa Antiokia, tabibu kwa ufundi na msomi pia katika uchoraji, na alipomjia Bwana alihesabiwa miongoni mwa wale Sabini na kutumwa mbele ya uso wake; naye alikuwa mmoja wa wanafunzi wawili ambao Kristo aliyefufuka aliwatokea njiani kwenda Emau, mioyo yao ilipowaka ndani yao alipowafunulia Maandiko.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; wachora ikoni."},

"Apostle and Evangelist Luke of the Seventy":
{"type": "Mtume, mwinjili · karne ya 1", "life": "Mtume na Mwinjilisti Mtakatifu Luka, ambaye kalenda za siku hii zinamwadhimisha pamoja na mitume Nathanaeli na Klementi, na ambaye sikukuu yake kuu Kanisa linaiadhimisha mwezi wa Oktoba, alikuwa Mgiriki wa Antiokia, tabibu kwa kazi na, mapokeo yanaongeza, mchoraji, sanaa zile mbili za mwili na jicho zikiletwa nzima katika utumishi wa Injili.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; wachora ikoni na wachoraji."},

"Apostle and Evangelist Mark":
{"type": "Mtume · karne ya 1", "life": "Mtakatifu Marko alikuwa mmoja wa Mitume Sabini na Mwinjilisti aliyeandika Injili ya pili. Akiwa mwenzake wa Petro, Paulo na Barnaba, alihubiri katika sehemu nyingi na akalianzisha Kanisa la Aleksandria. Aliteseka kwa ajili ya Kristo huko Misri na akapokea taji la shahidi katika karne ya kwanza."},

"Apostle and Evangelist Matthew":
{"type": "Mtume · karne ya 1", "life": "Mtakatifu Mathayo alikuwa mtoza ushuru aliyeitwa na Kristo kuwa mmoja wa Mitume Kumi na Wawili. Aliacha kazi yake ya awali, akamfuata Bwana, na akaandika Injili ibebayo jina lake. Baada ya Pentekoste aliihubiri Injili katika nchi nyingi, akavumilia mateso kwa ajili ya Kristo, na akapokea taji la shahidi katika karne ya kwanza."},

"Apostles Jason and Sosipater of the Seventy, the Virgin Kerkyra, and those with them":
{"type": "Mitume wa Sabini, mashahidi · karne ya 1", "life": "Mitume Watakatifu Yasoni na Sosipatro wa wale Sabini, pamoja na Bikira Kerkira na waliokuwa pamoja nao, walilipa Kanisa mojawapo ya kuongoka kamili kuliko kote kwa kisiwa katika zama za kitume; Yasoni alikuwa wa Tarso, Mkristo wa kwanza wa mji wa Mtume Paulo mwenyewe, na Sosipatro wa Akaya, na Paulo katika Waraka kwa Warumi anawaita jamaa zake, na mapokeo yanaongeza kwamba Yasoni ndiye mtu wa Thesalonike aliyewafikia Paulo na Sila na kujibu kwa ajili yao mbele ya watawala, na Sosipatro ndiye Sopatro wa Matendo.", "patron": "Maombezi yao huombwa kwa ajili ya makanisa ya visiwani; wafungwa na waliowaongoa."},

"Apostles Patrobus, Hermes, Linus, Gaius, and Philologus, of the Seventy":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mitume Watakatifu Patroba, Hermesi, Lino, Gaio na Filologo wa wale Sabini wanasalimiwa katika nyaraka za Mtume Paulo, na kila mmoja aliitumikia Injili kama askofu, akivumilia kazi na hatari za zama za kwanza za Kanisa. Lino, ambaye Paulo anamtaja katika waraka wake wa mwisho, alikuwa baada ya shahada ya mitume wakuu askofu wa kwanza wa Roma, akilitawala kanisa la mji wa kifalme katika miaka ya mateso ya Nero.", "patron": "Maombezi yao huombwa kwa ajili ya maaskofu; kupandwa kwa makanisa."},

"Apostles of the Seventy Archippus and Philemon, and Martyr Apphia":
{"type": "Mitume wa Sabini, mashahidi · karne ya 1", "life": "Mitume Watakatifu Arkipo na Filemoni wa wale Sabini, na Shahidi Afia, ni nyumba ya waraka mfupi kuliko yote, familia ya Kolosai ambayo Paulo aliiandikia barua ibebayo jina la Filemoni.", "patron": "Maombezi yao huombwa kwa ajili ya makanisa ya nyumbani; waume na wake wanaotumika pamoja."},

"Apostles of the Seventy Philemon and Archippus, Martyr Apphia, wife of Philemon and Equal-to-the-Apostles, and Onesimus, disciple of Saint Paul":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mitume Watakatifu Filemoni na Arkipo, Shahidi Afia, mke wa Filemoni, na Mtakatifu Onesimo, mwanafunzi wa Mtume Paulo, wamefungwa pamoja milele na waraka mfupi kuliko yote wa Paulo, ulioandikwa kwa Filemoni mpendwa wetu na mtenda kazi mwenzetu, kwa Afia mpendwa, kwa Arkipo askari mwenzetu, na kwa kanisa lililo nyumbani mwako.", "patron": "Maombezi yao huombwa kwa ajili ya nyumba za imani; mabwana na watumishi."},

"Apostles of the Seventy: Erastus, Olympas, Herodion, Sosipater, Quartus, and Tertius":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mitume Watakatifu Erasto, Olimpa, Herodioni, Sosipatro, Kuarto na Tertio wa wale Sabini walikuwa wanafunzi na watenda kazi wenzake wa Mtume Mtakatifu Paulo, anayewasalimu katika Waraka wake kwa Warumi. Erasto, ambaye Paulo anamwita mtunza hazina wa mji, alihudumu kama msimamizi wa Kanisa la Yerusalemu na baadaye kama askofu wa Panea katika Palestina.", "patron": "Maombezi yao huombwa kwa ajili ya maaskofu; watunza hazina."},

"Appearance of Christ to Saint Martin of Tours":
{"type": "Sikukuu · karne ya 4", "life": "Siku hii Kanisa linaadhimisha kumtokea kwa Kristo Mtakatifu Martini wa Tours, maono yanayosimama mwanzoni mwa mojawapo ya maisha yanayopendwa kuliko yote ya Magharibi na yanayohubiri, katika tukio moja la usiku, sura yote ya ishirini na tano ya Mathayo. Martini alikuwa wakati ule askari kijana wa wapanda farasi wa Roma huko Gaula, na bado mwanafunzi wa imani, hajabatizwa.", "patron": "Maombezi yake huombwa kwa ajili ya askari; watoaji wa sadaka."},

"Appearance of the Icon of the Mother of God “The Footprint” at Pochaiv":
{"type": "Sikukuu · karne ya 14", "life": "Siku hii Kanisa linaadhimisha kutokea kwa Mzazi-Mungu Mtakatifu Zaidi juu ya mlima wa Pochaiv, muujiza ulioanzisha Lavra kubwa ya Volhynia na kuacha katika mwamba ulio hai alama ya wayo wake ambayo waamini wanaiita tu Wayo.", "patron": "Nyayo iliyoachwa katika mwamba."},

"Arrival of the Ivḗron Icon of the Mother of God in Georgia":
{"type": "Sikukuu · karne ya 20", "life": "Siku hii Kanisa la Georgia linaadhimisha kuwasili kwa Ikoni ya Iveroni ya Mzazi-Mungu Mtakatifu Zaidi katika Georgia. Tarehe ishirini na sita ya Septemba mwaka wa 1989, nakala kamili ya Portaitissa maarufu na itendayo miujiza, Mlinzi wa Mlango wa monasteri ya Iveroni katika Mlima Athos, iliwasili Tbilisi kutoka Mlima Mtakatifu, iliyochorwa na watawa wa Athos kwa baraka ya Katholikos-Patriaki Ilia wa Pili kama ishara ya upendo na shukrani kwa watu wa Georgia, ambao baba zao waliianzisha monasteri ya Iveroni tangu kale.", "patron": "Huombwa kwa ajili ya ulinzi wa Georgia; faraja katika nyakati ngumu."},

"Beginning of Great Lent":
{"type": "Sikukuu · karne ya 4", "life": "Siku hii Kanisa linaingia katika Kwaresima Kuu, Siku Arobaini takatifu, majira ya kale na makuu kuliko yote ya toba, yaliyoadhimishwa tangu vizazi vya kwanza kabisa kama zaka ya mwaka iliyotolewa kwa Mungu na safari ya pamoja ya waamini wote kuelekea Pasaka. Mizizi yake inafika mwanzoni kabisa: Bwana mwenyewe alifunga siku arobaini.", "patron": "Huombwa kwa ajili ya waamini wote; wanaofundishwa imani wanaojiandaa kwa ubatizo."},

"Beheading of Venerable Cornelius, Abbot of the Pskov Caves":
{"type": "Abate, shahidi · karne ya 16", "life": "Mheshimiwa Korniliy, Abate wa Mapango ya Pskov na Kuhani Shahidi, alizaliwa Pskov mwaka wa 1501 kwa Stefano na Maria watukufu, na alifundwa katika monasteri ya Mirozh katika utamaduni wote wa utawa wa kaskazini, akitengeneza mishumaa, akipasua kuni, akinakili na kupamba vitabu, na akichora ikoni; na karani Misiur Munekhin alipompeleka kijana yule katika monasteri maskini ndogo ya Mapango msituni, uzuri wa mahali pale na taadhima ya kanisa la pangoni viliyaamua maisha yake, kwa maana Korniliy alinyolewa utawa huko wala hakuondoka tena.", "patron": "Maombezi yake huombwa kwa ajili ya maabate; watunga habari."},

"Blessed Andrew of Totma the Fool-For-Christ":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 17", "life": "Mbarikiwa Andrea wa Totma, Mpumbavu kwa ajili ya Kristo, alizaliwa mwaka wa 1638 katika kijiji cha Ust-Totma katika nchi za Vologda, na akiwa bado mtoto aliamua kuuacha ulimwengu. Kwa baraka ya Stefano, abate wa monasteri ya Ufufuo huko Galich, alijitwika wito mgumu wa upumbavu kwa ajili ya Kristo, na akakaa katika kanisa la Ufufuo katika mji wa Totma kando ya mto Sukhona.", "patron": "Maombezi yake huombwa kwa ajili ya umaskini wa hiari; kutoa sadaka kwa siri."},

"Blessed Andrew the Fool-For-Christ at Constantinople":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 10", "life": "Mbarikiwa Andrea Mpumbavu kwa ajili ya Kristo alikuwa Mslavi kwa kuzaliwa, aliyeletwa akiwa mtumwa katika ujana wake Konstantinopoli, ambako alimtumikia mtukufu mmoja wa mji na alipendwa kwa upole wake na bidii yake katika Maandiko. Alipoona katika ndoto majeshi ya malaika na ya mashetani yakipigana, na kumsikia Bwana akimwita kwenye pambano, alijitwika, baada ya bwana wake kumwacha huru, njia ngumu kuliko zote za ujinyimaji, akijifanya mwendawazimu kwa ajili ya Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi wa Mungu waliofichwa; maono ya mambo ya mbinguni."},

"Blessed Cleopatra with her son John, in Egypt":
{"type": "Mtakatifu · karne ya 4", "life": "Mbarikiwa Kleopatra alikuwa mjane mchaji Mungu wa Palestina, aliyeishi Misri katika siku za mateso, na alipoliona pambano la Shahidi mtakatifu Varo, aliupata mwili wake kwa siri na akaubeba hadi kijiji chake cha kuzaliwa cha Edra karibu na Mlima Tabori, ambapo aliuzika kwa heshima na akajenga juu yake kanisa kwa jina la shahidi, nyumba yake yote ikimheshimu kama mlinzi wao.", "patron": "Maombezi yake huombwa kwa ajili ya mama; mama wanaoomboleza."},

"Blessed Constantine, Metropolitan of Kyiv":
{"type": "Metropolita · karne ya 12", "life": "Mbarikiwa Konstantino, Metropolita wa Kyiv, aliliongoza Kanisa la Urusi katikati ya karne ya kumi na mbili, katika wakati wa ugomvi mzito juu ya jimbo la metropolita, na anakumbukwa hasa kwa unyenyekevu wa kushangaza ambao kwao alitafuta, hata katika kifo, nafasi ya chini kuliko zote.", "patron": "Wakuu wa Kanisa wanaotafuta nafasi ya mwisho; wanyenyekevu walio katika vyeo vikuu."},

"Blessed Dovmont (Timothy), Prince of Pskov":
{"type": "Mkuu Mwaminifu · karne ya 13", "life": "Mkuu Mwaminifu Mtakatifu Dovmont wa Pskov, aitwaye Timotheo tangu ubatizo wake, alikuwa mkuu Mlithuania na mpagani aliyekuwa mmoja wa watawala wapendwa kuliko wote na mlinzi wa mbinguni wa mji wa Urusi, maisha yake yakiwa mfano wa bidii ya aliyeongoka iliyomiminwa katika kuwatetea watu aliowachukua kuwa wake.", "patron": "Mkuu mpagani aliyefanywa shujaa wa Kikristo."},

"Blessed John “the Hairy” and Fool-For-Christ at Rostov":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 16", "life": "Mbarikiwa Yohane, aitwaye Mwenye Huruma na pia Mwenye Nywele, alijitwika huko Rostov jitihada ngumu na iliyofichwa ya upumbavu kwa ajili ya Kristo, akivumilia baridi, njaa na lawama kwa ajili ya upendo wa Mungu. Hakuwa na nyumba yake mwenyewe, bali alipata makao mara katika nyumba ya baba yake wa kiroho, kasisi wa kanisa la Watakatifu Wote, mara kwa mjane huyu au yule maskini wa mji.", "patron": "Maombezi yake huombwa kwa ajili ya unyenyekevu; wasio na nyumbani."},

"Blessed Laurence the Fool-For-Christ at Kaluga":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 16", "life": "Mbarikiwa Laurenti, mpumbavu kwa ajili ya Kristo na mtenda-miujiza wa Kaluga, aliishi mwanzoni mwa karne ya kumi na sita karibu na mji wa kale wa Kaluga, karibu na kanisa la Kuzaliwa kwa Kristo lililowekwa juu ya kilima kirefu chenye miti, ambako njia ndefu ya chini ya ardhi iliongoza kutoka makao yake ili apate kuhudhuria ibada.", "patron": "Maombezi yake huombwa kwa ajili ya utetezi wa Kaluga."},

"Blessed Nicholas (Salos) of Pskov the Fool-For-Christ":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 16", "life": "Mbarikiwa Nikolao Salos wa Pskov, ambaye mji ulimwita Mikula Mpumbavu, aliibeba jitihada ya upumbavu kwa ajili ya Kristo kwa zaidi ya miongo mitatu, akilala katika baraza, akivumilia baridi kali na dhihaka akiwa na matambara, akinena kwa mafumbo yaliyotimia, na akipata, muda mrefu kabla ya kupumzika kwake, neema ya kutenda miujiza na ya unabii, mwendawazimu wa mji akiwa kimyakimya mtabiri wake wa kutegemewa kuliko wote.", "patron": "Maombezi yake huombwa kwa ajili ya wapumbavu kwa ajili ya Kristo; wasemao kweli mbele ya mamlaka."},

"Blessed Nicholas Kochanov the Fool-For-Christ at Novgorod":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 14", "life": "Mbarikiwa Nikolao Kochanov, mpumbavu kwa ajili ya Kristo wa Novgorod, alizaliwa katika familia tajiri na tukufu na tangu ujana wake alipenda kanisa, kufunga na sala. Watu walipoanza kumsifu kwa fadhila zake, aliikimbia heshima yao kwa kujitwika njia ngumu ya upumbavu kwa ajili ya Kristo, akiificha utakatifu wake chini ya sura ya wazimu.", "patron": "Maombezi yake huombwa kwa ajili ya upatanisho; amani katikati ya ugomvi."},

"Blessed Prince Gleb Andreevich, son of Saint Andrew Bogoliubsky":
{"type": "Mkuu · karne ya 12", "life": "Mtakatifu Gleb Andreevich alikuwa mkuu kijana wa Vladimir, mwana wa Mkuu mtakatifu Andrei Bogoliubsky, aliyeishi maisha mafupi ya uchaji adimu na akatukuzwa na Mungu kwa kutooza.", "patron": "Wakuu vijana wa uchaji Mungu; wanaopenda Maandiko na Kanisa."},

"Blessed Yaropolk (in Baptism Peter), Prince of Volodymyr-Volhynia":
{"type": "Mkuu · karne ya 11", "life": "Mkuu Mtakatifu Yaropolk wa Volodymyr-Volhynia, aitwaye Petro katika ubatizo mtakatifu, alikuwa mwana wa Mkuu Mkubwa Izyaslav wa Kyiv na mjukuu wa Yaroslav Mwenye Hekima; na maisha yake mafupi yalikuwa shule ya kunyang'anywa, kwa maana alishiriki uhamisho wa mara kwa mara wa baba yake miongoni mwa Wapoland na Wajerumani wakati ugomvi wa wakuu ulipowafukuza kutoka Urusi, akijifunza mapema kwamba viti vya enzi hukopeshwa wala havitolewi.", "patron": "Maombezi yake huombwa kwa ajili ya watawala; wakuu wanaoteseka dhuluma bila kulipiza kisasi."},

"Childmartyr Gabriel of Bialystok":
{"type": "Mtoto shahidi · karne ya 17", "life": "Shahidi Mtoto Mtakatifu Gabrieli wa Bialystok alizaliwa mwaka wa 1684 katika kijiji cha Zverki karibu na Bialystok, mwana wa wanakijiji wachaji Mungu wa Kiorthodoksi, Petro na Anastasia, na aliishi miaka sita mifupi aliyopewa katika utakatifu wa kawaida wa utoto mpendwa wa kijijini: sala zilizojifunzwa magotini mwa mama yake, sikukuu za kanisa, mashamba.", "patron": "Maombezi yake huombwa kwa ajili ya watoto; wasio na hatia na wasio na msaada."},

"Church New Year":
{"type": "Sikukuu · kiliturujia", "life": "Siku ya kwanza ya Septemba Kanisa linaadhimisha mwanzo wa Indikto, yaani Mwaka Mpya wa Kanisa. Mababa wa Baraza la Kwanza la Kiekumeni huko Nikea waliamuru kwamba mwaka wa Kanisa uanze siku hii, wakifuata hesabu ya kale ambayo kwayo Septemba, mwezi wa kuvuna, ulikuwa mwanzo wa mwaka miongoni mwa Waebrania, ambao katika majira haya walimtolea Mungu shukrani kwa ukarimu wake.", "patron": "Huombwa kwa ajili ya mwaka mpya; shukrani."},

"Commemoration of the Apparition of the Sign of the Precious Cross Over Jerusalem, in 351 AD":
{"type": "Sikukuu · karne ya 4", "life": "Siku hii Kanisa linaadhimisha kutokea kwa ishara ya Msalaba wenye thamani angani juu ya Yerusalemu, mwaka wa 351, chini ya mfalme Konstantio, mwana wa Konstantino Mkuu; tarehe saba ya Mei, Jumanne kabla ya sikukuu ya Kupaa.", "patron": "Msalaba ulioandikwa angani kote."},

"Commemoration of the Founding of Constantinople":
{"type": "Sikukuu · karne ya 4", "life": "Siku hii Kanisa linaadhimisha kuanzishwa na kuwekwa wakfu kwa Konstantinopoli, kulikotokea Jumatatu, tarehe kumi na moja ya Mei, mwaka wa 330, katika Indikto ya tatu, kwa amri ya mfalme mkuu na Mkristo Konstantino.", "patron": "Roma Mpya iliyoanzishwa chini ya Msalaba."},

"Commemoration of the Founding of the Church of the Resurrection (Holy Sepulchre) at Jerusalem":
{"type": "Ukumbusho · karne ya 4", "life": "Siku hii Kanisa linaadhimisha kuanzishwa, yaani kuwekwa wakfu kwa taadhima, kwa Kanisa la Ufufuo wa Kristo huko Yerusalemu, lililoinuliwa na Mtakatifu Konstantino Mkuu na mama yake Malkia mtakatifu Helena juu ya Kaburi la Bwana na kilima cha Golgotha. Helena alipofika Yerusalemu, akaziangamiza sanamu za kipagani zilizopanajisi mahali patakatifu, na akaupata Msalaba Utoao Uzima chini ya hekalu la Venus, Konstantino aliamuru lijengwe kanisa kubwa na tukufu likizingira pote mahali pa Kusulubiwa na Kaburi la Ufufuo.", "patron": "Huombwa kwa ajili ya kuwekwa wakfu kwa makanisa."},

"Commemoration of the Great Earthquake at Constantinople":
{"type": "Ukumbusho · karne ya 8", "life": "Siku hii Kanisa linaadhimisha tetemeko kubwa la ardhi lililoupiga Konstantinopoli mwaka wa 740, katika utawala wa Leo Mwisauria, wakati ghadhabu ya Mungu ilipoutikisa mji wa kifalme, ikiangusha makanisa, makao, na sehemu ndefu za kuta za mji pamoja na minara yake, na kuwaangamiza watu wengi, mitetemeko ikiendelea kwa miezi hata wakazi wakakaa kwa hofu chini ya anga wazi.", "patron": "Huombwa kwa ajili ya ukombozi kutoka matetemeko ya ardhi; toba mbele ya hukumu za Mungu."},

"Commemoration of the Holy Fathers of the First Ecumenical Council":
{"type": "Sikukuu · karne ya 4", "life": "Siku hii Kanisa linaadhimisha Mababa Watakatifu wa Mtaguso Mkuu wa Kwanza.", "patron": "Watetezi wa umungu wa Mwana; mababa wa mabaraza."},

"Commemoration of the Holy Fathers of the Second Ecumenical Council":
{"type": "Sikukuu · karne ya 4", "life": "Siku hii Kanisa linaadhimisha Mababa Watakatifu wa Mtaguso Mkuu wa Pili, mia moja na hamsini waliokusanyika Konstantinopoli mwaka wa 381, chini ya mfalme Theodosio Mkuu.", "patron": "Kanuni ya Imani iliyokamilishwa kwa kifungu cha Roho."},

"Commemoration of the Holy Fathers of the Seventh Ecumenical Council":
{"type": "Sikukuu · karne ya 8", "life": "Siku hii Kanisa linaadhimisha Mababa Watakatifu wa Mtaguso Mkuu wa Saba, uliokusanyika Nikea mwaka wa 787, katika siku za malkia Irene na mwanawe Konstantino, chini ya uenyekiti wa Mtakatifu Tarasio, Patriaki wa Konstantinopoli. Mababa wapatao mia tatu na hamsini walikusanyika dhidi ya uzushi wa wapiga-ikoni, ambao kwa miongo kadhaa ulikuwa umeliharibu Kanisa, ukiziangamiza ikoni takatifu na kuwatesa waliokuwa wakiziheshimu.", "patron": "Huombwa kwa ajili ya kuheshimu ikoni takatifu; utimilifu wa mafundisho ya Kiorthodoksi."},

"Commemoration of the Holy Righteous David the King, Joseph the Betrothed, and James the Brother of the Lord":
{"type": "Wenye haki · karne ya 1", "life": "Katika siku baada ya Kuzaliwa Kanisa linawaadhimisha pamoja Mwenye haki Mtakatifu Yosefu Mchumba, Daudi Mfalme na Yakobo Ndugu wa Bwana, sinaksi ya jamaa za Bwana kwa jinsi ya mwili, iliyowekwa tangu kale kwa Dominika baada ya sikukuu na kuadhimishwa pia siku hii.", "patron": "Maombezi yao huombwa kwa ajili ya familia za watumishi wa Bwana; undugu na Kristo kwa utii."},

"Commemoration of the Kazan Icon of the Mother of God and the deliverance from the Poles":
{"type": "Ukumbusho · karne ya 17", "life": "Siku hii Kanisa linaadhimisha Ikoni ya Kazan ya Mzazi-Mungu Mtakatifu Zaidi kwa kumbukumbu ya ukombozi wa Moscow na Urusi yote kutoka kwa Wapoland mwaka wa 1612. Katika Zama za Machafuko, nchi ilipokuwa imeraruliwa na uvamizi na uhaini na Moscow yenyewe ikiwa mikononi mwa majeshi ya kigeni yaliyodhihaki imani ya Kiorthodoksi, Patriaki Hermogene aliyekuwa kifungoni aliwaita watu wainuke kwa ajili ya kulitetea Kanisa na nchi.", "patron": "Huombwa kwa ajili ya ukombozi wa mataifa; ulinzi wakati wa machafuko."},

"Commemoration of the Miracle of the Archangel Michael at Colossae":
{"type": "Ukumbusho · kiliturujia", "life": "Siku hii Kanisa linaadhimisha muujiza mtukufu uliotendwa na Malaika Mkuu Mikaeli huko Khone, karibu na Kolosai katika Frigia. Mahali pale palikuwa na chemchemi itendayo miujiza, iliyotabiriwa na Mtume Yohane Mwanateolojia alipohubiri Hierapoli; na mtu mmoja wa Laodikia, ambaye binti yake bubu alipata kunena kwa maji yake baada ya Malaika Mkuu kumtokea katika ndoto, alibatizwa pamoja na nyumba yake yote na akajenga juu ya chemchemi kanisa kwa heshima ya Jemadari Mkuu Mikaeli.", "patron": "Huombwa kwa ajili ya ulinzi; uponyaji."},

"Commemoration of the Shepherds in Bethlehem who were watching their flocks, and went to see the Lord":
{"type": "Wenye haki · karne ya 1", "life": "Siku ya kwanza ya Kuzaliwa Kanisa linawaadhimisha Wachungaji wa Bethlehemu, waliokuwa wakilinda makundi yao usiku mashambani wakati utukufu wa Bwana ulipowaangazia pande zote, nao wakawa wa kwanza wa jamii ya wanadamu kuisikia Injili ikihubiriwa.", "patron": "Maombezi yao huombwa kwa ajili ya wachungaji; walinzi wa usiku."},

"Commemoration of the Vladimir Icon of the Mother of God and the deliverance of Moscow from the Invasion of Tamerlane":
{"type": "Ikoni · karne ya 14", "life": "Ikoni ya Vladimir ya Mzazi-Mungu Mtakatifu Zaidi, kwa mapokeo iliyochorwa na Mwinjilisti Luka na kuletwa kutoka Konstantinopoli hadi Urusi, iliwekwa na Mtakatifu Andrei Bogoliubsky katika kanisa kuu la Vladimir, ambako ilipata jina lake, nayo ikawa ikoni ipendwayo na ilindayo kuliko zote ya nchi ya Urusi.", "patron": "Huombwa kwa ajili ya ulinzi wa Urusi; ukombozi kutoka uvamizi."},

"Conception of the Honorable Glorious Prophet, Forerunner and Baptist John":
{"type": "Sikukuu · karne ya 1", "life": "Siku hii Kanisa linaadhimisha Kutungwa Mimba kwa Nabii Mtangulizi na Mbatizaji Yohane, anayeheshimiwa na mtukufu, mwanzo wa habari za Injili. Kasisi Zakaria, katika zamu ya kikundi chake, alipoingia katika Hekalu la Bwana ili kufukiza ubani, Malaika Mkuu Gabrieli alimtokea upande wa kuume wa madhabahu ya ubani.", "patron": "Huombwa kwa ajili ya wanandoa wasio na watoto; sala iliyojibiwa."},

"Conception of the Most Holy Theotokos by Saint Anna":
{"type": "Sikukuu · kiliturujia", "life": "Sikukuu hii inaadhimisha kutungwa mimba kwa Bikira Maria na mama yake, Ana mwenye haki, miezi tisa kabla ya sikukuu ya kuzaliwa kwa Maria tarehe nane ya Septemba. Kwa mapokeo ya Kanisa, Yoakimu na Ana walikuwa wenye haki lakini hawakuwa na mtoto na walikuwa wamesonga katika umri, na kukosa kwao mtoto kulihesabiwa kuwa lawama.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Confessors Barses and Eulogius, Bishops of Edessa, and Protogenes, Bishop of Carrhae":
{"type": "Maaskofu · karne ya 4", "life": "Watakatifu Barse na Eulogio, Maaskofu wa Edesa, na Protogene, Askofu wa Karrhae, walikuwa wakiri walioteseka mikononi mwa Waariani katika nusu ya pili ya karne ya nne, wakati mfalme Valente alipotaka kuueneza uzushi ule na kuwatesa Waorthodoksi kwa ukatili. Mtakatifu Barse, shujaa imara wa imani ya kweli, alifukuzwa kutoka kiti chake cha Edesa na kupelekwa uhamishoni, kwanza mahali pamoja na kisha pengine, daima mbali zaidi na mji wake.", "patron": "Maombezi yao huombwa kwa ajili ya Othodoksi dhidi ya uzushi; uvumilivu uhamishoni."},

"Consecration of the Church of the Holy Great Martyr George in Lydda":
{"type": "Ukumbusho · karne ya 4", "life": "Siku hii Kanisa linaadhimisha kuwekwa wakfu kwa kanisa la Shahidi Mkuu Mtakatifu Georgi huko Lida katika Palestina, na kuwekwa humo kwa masalia yake yenye thamani. Shahidi mkuu, aliyeteseka Nikomedia mwaka wa 303 chini ya Diokletiano, alikuwa amemwomba mtumishi wake kabla ya pambano lake aupeleke mwili wake Lida, nyumbani kwa jamaa za mama yake katika Nchi Takatifu.", "patron": "Huombwa kwa ajili ya kuheshimu Shahidi Mkuu Georgi."},

"Constantinople Icon of the Mother of God":
{"type": "Sikukuu · karne ya 1", "life": "Siku hii Kanisa linaadhimisha Ikoni ya Konstantinopoli ya Mzazi-Mungu Mtakatifu Zaidi, sura ambayo mapokeo yanaihesabu miongoni mwa zile zilizochorwa na Mtume na Mwinjilisti Mtakatifu Luka mwenyewe, tabibu na mchora ikoni wa Mzazi-Mungu, ambaye kalamu yake, Kanisa linashika, iliwapa waamini kwanza mfano wake na ikapokea baraka yake mwenyewe juu ya kazi ile, neno lake kwamba neema yake ingekuwa pamoja na sura zile.", "patron": "Huombwa kwa ajili ya wachora ikoni; wote wanaoziheshimu ikoni za Mzazi-Mungu."},

"Dedication of the Church of the Greatmartyr George at Kyiv":
{"type": "Ukumbusho · karne ya 11", "life": "Siku hii Kanisa linaadhimisha kuwekwa wakfu kwa kanisa la Shahidi Mkuu Mtakatifu Georgi huko Kyiv. Ilikuwa desturi ya uchaji ya wakuu wa Urusi, tangu Mtakatifu Vladimiri, kuinua makanisa kwa heshima ya watakatifu wao walinzi: Vladimiri, aitwaye Basili katika ubatizo, alijenga mahekalu ya Mtakatifu Basili huko Kyiv na Vyshgorod, na wanawe walimfuata katika jambo hili.", "patron": "Huombwa kwa ajili ya kuheshimu Shahidi Mkuu Georgi katika Urusi; makanisa yaliyojengwa kwa shukrani."},

"Dormition of the Righteous Anna, the Mother of the Most Holy Theotokos":
{"type": "Mwenye haki · karne ya 1", "life": "Sikukuu hii inaadhimisha kulala kwa amani kwa Mwenye haki Ana, mama wa Mzazi-Mungu Mtakatifu Zaidi na bibi wa Bwana wetu kwa jinsi ya mwili. Ana alikuwa binti wa kuhani Matthani, wa kabila la Lawi na ukoo wa Haruni, na pamoja na mumewe, Mwenye haki Yoakimu, alibeba kwa miaka mingi lawama ya kukosa mtoto, hadi katika uzee wao Mungu alipozisikia sala zao na kuwapa binti, Bikira Maria safi, aliyekuwa atakuwa Mama wa Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya mama; mabibi."},

"Entrance of the Apostle Andrew into Georgia":
{"type": "Sikukuu · karne ya 1", "life": "Siku hii Kanisa la Georgia linaadhimisha kuingia kwa Mtume Mtakatifu Andrea Aliyeitwa wa Kwanza katika nchi za Georgia, msingi wa kitume ambao juu yake Kanisa lile la kale linasimama. Mapokeo ya Georgia yanasimulia kwamba mitume walipopiga kura kwa ajili ya mataifa, Iberia ilimwangukia Mzazi-Mungu Mtakatifu Zaidi mwenyewe.", "patron": "Huombwa kwa ajili ya msingi wa kitume wa Kanisa la Georgia; Mzazi-Mungu kama mlinzi wa Georgia."},

"Equal of the Apostles and Emperor Constantine with his Mother Helen":
{"type": "Sawa na Mitume · karne ya 4", "life": "Mtakatifu Konstantino alikuwa mfalme wa Roma na aliyakomesha mateso ya Wakristo kwa Amri ya Milano. Aliliunga mkono Kanisa na akauitisha Mtaguso Mkuu wa Kwanza huko Nikea. Mama yake, Mtakatifu Helena, alisafiri hadi Yerusalemu naye anahusishwa na kupatikana kwa Msalaba Utoao Uzima. Walipumzika katika karne ya nne."},

"Equal-to-the-Apostles Blessed Great Princess Olga (in Holy Baptism Helen)":
{"type": "Sawa na Mitume · karne ya 10", "life": "Mtakatifu Olga alikuwa mkuu wa kike wa Kyiv na bibi wa Mtakatifu Vladimiri. Baada ya kifo cha Mkuu Igori, aliitawala Urusi kwa hekima. Alipokea ubatizo mtakatifu kwa jina la Helena na akaueneza Ukristo miongoni mwa watu wake, ingawa Urusi ilikuwa bado haijabatizwa. Alipumzika mwaka wa 969."},

"Equals of the Apostles and Teachers of the Slavs, Cyril and Methodius":
{"type": "Mtume · karne ya 9", "life": "Watakatifu Walio Sawa na Mitume Kirilo na Methodio, Walimu wa Waslavoni, walikuwa ndugu wa familia ya useneta ya Thesalonike, mji ulio katika ukingo wa ulimwengu wa Kislavi ambao mitaa yake ilikuwa imewafundisha lugha ya Kislavoni tangu utoto, maongozi kwa ajili ya kazi iliyokuwa ikiwangoja.", "patron": "Alfabeti iliyotolewa kwa Waslavi."},

"Eve of the Nativity of our Lord":
{"type": "Sikukuu · kiliturujia", "life": "Mkesha wa Kuzaliwa kwa Bwana wetu, uitwao Paramoni, ni kizingiti cha sikukuu, na Kanisa linauadhimisha kama linavyoadhimisha mkesha wa Theofania peke yake, kwa siku ya kufunga kwa ukali na maandalizi ya taadhima kuliko yote ya mwaka wake. Asubuhi zinaimbwa Saa za Kifalme, zilizoitwa hivyo kwa sababu wafalme walisimama humo zamani: katika kila saa zinasomwa zaburi za Kupata Mwili, unabii, Mtume, na Injili ya kuzaliwa, Maandiko yote yakikusanywa kulizunguka pango.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Fathers of the First Six Councils":
{"type": "Maaskofu · kiliturujia", "life": "Siku hii inawaadhimisha Mababa watakatifu wa Mitaguso Mikuu sita ya kwanza, wakuu wa Kanisa na walimu wabeba-Mungu waliokusanyika kutoka kila sehemu ya ulimwengu wa Kikristo ili kuitetea imani ya kitume dhidi ya uzushi uliolishambulia. Huko Nikea na katika Mtaguso wa Kwanza wa Konstantinopoli walitangaza umungu wa Mwana na wa Roho Mtakatifu na wakalipa Kanisa Kanuni ya Imani tunayoikiri hadi leo.", "patron": "Huombwa kwa ajili ya Mafundisho ya Kiothodoksi; imani ya kweli."},

"Finding of the Relics of Saints Basil and Constantine, Princes of Yaroslavl":
{"type": "Sikukuu · karne ya 16", "life": "Siku hii Kanisa linaadhimisha kupatikana kwa masalia ya Wakuu Waaminifu Watakatifu Basili na Konstantino wa Yaroslavl, ndugu waliotawala na kuteseka kwa ajili ya mji wao katika miaka michungu ya nira ya Watatari na ambao miili yao isiyooza ilifunuliwa muda mrefu baadaye katika moto.", "patron": "Wakuu wa Yaroslavl; ambao masalia yao yanapatikana baada ya moto."},

"Finding of the relics of Monastic Martyr Adrian of Poshekhonsk, Yaroslavl":
{"type": "Abate, shahidi mtawa · karne ya 16", "life": "Siku hii Kanisa linaadhimisha kufukuliwa kwa masalia ya Mheshimiwa Adriano wa Poshekhonsk, Shahidi Mtawa, kulikotokea tarehe kumi na tisa ya Novemba mwaka wa 1625. Mtakatifu Adriano, mtawa na mchora ikoni mwenye kipaji aliyefundwa katika utamaduni wa monasteri kubwa za kaskazini, alikuwa ameanzisha pamoja na mjinyimaji mwenzake monasteri ya Kulala kwa Mzazi-Mungu Mtakatifu Zaidi katika misitu ya Poshekhonye katika nchi za Yaroslavl, akijitaabisha huko katika kufunga, sala na kuchora ikoni takatifu, na akikusanya jumuiya kulizunguka kanisa la nyikani.", "patron": "Maombezi yake huombwa kwa ajili ya wachora ikoni; watawa."},

"Finding of the relics of Righteous Saint Νikόdēmos":
{"type": "Mwenye haki · karne ya 1", "life": "Mtakatifu Nikodimo alikuwa Farisayo na mkuu wa Wayahudi aliyemjia Bwana Yesu usiku, kama Injili ya Yohane isimuliavyo, na akasikia kutoka kwake juu ya kuzaliwa upya kwa maji na Roho. Ingawa mwanzoni alikuja kwa siri kwa kuwaogopa Wayahudi, alimtetea Mwokozi mbele ya baraza, na baada ya kusulubiwa alikuja waziwazi pamoja na Yosefu wa Arimathaya, akileta mchanganyiko wa manemane na uudi, na akasaidia kuupaka na kuuzika mwili wa Bwana.", "patron": "Maombezi yake huombwa kwa ajili ya wanafunzi wa siri; watafutaji wa kweli."},

"Finding of the relics of Saint Abibas":
{"type": "Mwenye haki · karne ya 1", "life": "Mtakatifu Abiba alikuwa mwana wa Gamalieli mwenye haki, mwalimu wa Mtakatifu Paulo, na pamoja na baba yake alipokea ubatizo mtakatifu mikononi mwa mitume, akiikubali imani ya Kristo. Akiishi katika usafi, alipumzika angali kijana na akazikwa na baba yake katika pango la Kafargamala, ambapo Shahidi wa Kwanza Stefano na Mtakatifu Nikodimo walikuwa tayari wamelala.", "patron": "Maombezi yake huombwa kwa ajili ya usafi."},

"Finding of the relics of Saint Basil, Bishop of Ryazan":
{"type": "Sikukuu · karne ya 17", "life": "Siku hii Kanisa linaadhimisha kupatikana kwa masalia ya Mtakatifu Basili, Askofu wa Ryazan, mkuu wa Kanisa wa karne ya kumi na tatu ambaye kutokuwa kwake na hatia kulithibitishwa kwa muujiza maarufu na ambaye masalia yake yalifunuliwa katika miaka ya machafuko ya karne ya kumi na saba.", "patron": "Waliosingiziwa; maaskofu waliofukuzwa kwa uchongezi."},

"Finding of the relics of Saint Gamaliel":
{"type": "Mwenye haki · karne ya 1", "life": "Mtakatifu Gamalieli alikuwa Farisayo na mwalimu maarufu wa Sheria, aliyeheshimiwa miongoni mwa Wayahudi, aliyeshauri kiasi kuelekea mitume walipoletwa mbele ya baraza, kama inavyosimuliwa katika Matendo ya Mitume, naye alikuwa mwalimu wa Mtakatifu Paulo. Kwa siri alikuwa mwanafunzi wa Kristo, na Shahidi wa Kwanza Stefano alipopigwa mawe na kuachwa bila kuzikwa, ni Gamalieli aliyeuchukua mwili wake kwa heshima na kuuweka katika pango katika shamba lake mwenyewe la Kafargamala.", "patron": "Maombezi yake huombwa kwa ajili ya walimu; wanafunzi wa siri."},

"Finding of the relics of Saint Theodore, Prince of Smolensk and Yaroslavl, and his children":
{"type": "Mkuu · karne ya 13", "life": "Siku hii Kanisa linaadhimisha kufukuliwa kwa masalia ya Mkuu Mwaminifu Theodoro wa Smolensk na Yaroslavl, aitwaye Mweusi, pamoja na wanawe Daudi na Konstantino, kulikotokea Yaroslavl tarehe tano ya Machi mwaka wa 1463; kupumzika kwake mwenyewe kunaadhimishwa mwezi wa Septemba, lakini siku hii ni ya kupatikana kwa mwili wake usiooza.", "patron": "Maombezi yao huombwa kwa ajili ya watawala; familia."},

"Finding of the relics of Venerable Cyril, Abbot of Novoezersk, Vologda":
{"type": "Abate · karne ya 16", "life": "Siku hii Kanisa linaadhimisha kupatikana kwa masalia ya Mheshimiwa Kirilo, Abate wa Novoezersk, kulikotokea mwaka wa 1649. Alizaliwa katika familia tukufu ya Galich, akakimbia nyumba ya wazazi wake akiwa na miaka kumi na mitano, akivutwa na upendo wa Kristo, na akafika kupitia misitu kwa mzee mkuu Korniliy wa Komel, ambaye, akiuona muhuri wa Mungu juu ya kijana yule, alimnyoa utawa.", "patron": "Maombezi yake huombwa kwa ajili ya watawa; kujiweka wakfu katika ujana."},

"Finding of the relics of Venerable Maximus the Greek (July 4, 1996)":
{"type": "Mtawa · karne ya 16", "life": "Sikukuu hii inaadhimisha kupatikana kwa masalia ya Mheshimiwa Maksimo Mgiriki, mtawa msomi na mkiri. Alizaliwa akiitwa Mikaeli Trivoli huko Arta katika Ugiriki karibu mwaka wa 1470, alisoma Italia, kisha akawa mtawa katika Mlima Athos, na mwaka wa 1518 alitumwa Urusi ili kutafsiri na kusahihisha vitabu vitakatifu.", "patron": "Maombezi yake huombwa kwa ajili ya watafsiri na wasomi; waliofungwa isivyo haki."},

"First Translation of the relics of Saint Herman, Archbishop of Kazan":
{"type": "Askofu Mkuu · karne ya 16", "life": "Mtakatifu Hermani, Askofu Mkuu wa Kazan, alizaliwa Staritsa katika familia tukufu ya Sadyrev-Polev, na alipopokea unyoaji wa utawa katika monasteri ya Volokolamsk, alifundwa katika shule ya Mtakatifu Yosefu, akijulikana kwa usomi wake, maisha yake ya ujinyimaji na kazi yake ya kunakili vitabu. Nchi za Kazan zilizokuwa zimeshindwa karibuni zilipofunguliwa kwa Injili, alitumwa pamoja na Mtakatifu Guria kwa kuziangaza, na akaanzisha huko Sviyazhsk monasteri ya Kulala kwa Mzazi-Mungu, iliyokuwa kitovu cha misheni kwa watu wa Volga.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuangazwa kwa nchi za Kazan."},

"First and second finding of the Honorable Head of the Holy Glorious Prophet, Forerunner, and Baptist of the Lord, John":
{"type": "Sikukuu · karne ya 5", "life": "Siku hii Kanisa linaadhimisha Kupatikana kwa Kwanza na kwa Pili kwa Kichwa chenye Thamani cha Mtakatifu Yohane Mtangulizi, sura mbili za kwanza kabisa katika safari ya ajabu ya salia inayoheshimiwa kuliko zote katika Ukristo baada ya vyombo vya Mateso. Herodia alipokipata kichwa cha Mbatizaji juu ya sinia ya kisasi chake, hakukubali kizikwe pamoja na mwili wake, akihofu, mapokeo yasemavyo, ufufuo wa mtu aliyemnyamazisha, na akakificha mahali pasipo safi katika jumba la Herode.", "patron": "Huombwa kwa ajili ya wote wanaotafuta kilichofichwa; walinzi wa masalia."},

"First finding of the relics of Saint Metrophanes, first Bishop of Voronezh":
{"type": "Askofu · karne ya 18", "life": "Mtakatifu Mitrofani alikuwa Askofu wa kwanza wa Voronezh, aliyewekwa wakfu mwaka wa 1682, naye alijulikana kwa uchaji wake wa kina, uangalizi wake kwa maskini na bidii yake kwa Kanisa; akiwa mshauri na mtegemezi wa mfalme Petro Mkuu katika kujenga jeshi la wanamaji la Urusi huko Voronezh, hakuogopa kumkemea mfalme sanamu za kipagani zilipowekwa, naye alisikilizwa.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Forefeast of the Annunciation":
{"type": "Sikukuu · karne ya 1", "life": "Siku hii Kanisa linaadhimisha siku ya kabla ya sikukuu ya Bishara, siku moja tu ya maandalizi kabla ya sikukuu ambayo mababa waliiita taji ya wokovu wetu na mwanzo wa sikukuu zote, na nyimbo za siku hii zinasimama kwa vidole vya miguu: leo, zinaimba, siri kubwa inakaribia, malaika mkuu anatumwa, Bikira yuko katika sala zake, na furaha ya viumbe vyote iko jioni moja tu mbele.", "patron": "Huombwa kwa ajili ya wote wanaojiandaa kwa furaha kubwa; mkesha wa habari njema kuu."},

"Forefeast of the Dormition of the Mother of God":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Siku hii ni ya kabla ya sikukuu ya Kulala kwa Bibi yetu Mtakatifu Zaidi Mzazi-Mungu, ambayo katika hiyo Kanisa linaanza kuadhimisha kulala kwake kwa heri, kunakoadhimishwa tarehe kumi na tano ya Agosti mwishoni mwa mfungo uliowekwa kwa ajili yake. Nyimbo za kabla ya sikukuu zinawaita waamini wakusanyike kwa furaha, kwa maana Mzazi-Mungu yu karibu kuondoka duniani kwenda ufalme wa mbinguni, ili atwaliwe juu katika utukufu na Mwana wake.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Forefeast of the Elevation of the Cross":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Hii ni Siku ya Kabla ya Sikukuu ya Kuinuliwa kwa Ulimwengu Wote kwa Msalaba wenye Thamani na Utoao Uzima, ambayo katika hiyo Kanisa linaanza kuadhimisha sikukuu kuu ya kesho. Katika ibada nyimbo za Msalaba zinaanza kusikika, zikiwaita waamini wazitakase roho zao ili wapate kuuona Mti mtakatifu ulioinuliwa katikati ya dunia.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Forefeast of the Entry into the Temple of the Most Holy Theotokos":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Siku hii Kanisa linaadhimisha siku ya kabla ya sikukuu ya Kuingia kwa Mzazi-Mungu Mtakatifu Zaidi Hekaluni, likisimama katika kizingiti cha sikukuu kama mtoto Maria alivyosimama katika kizingiti cha patakatifu. Nyimbo za kabla ya sikukuu zinawaita waamini wajiandae: Sisi waamini na tufurahi leo, tukimwimbia Bwana zaburi, na tuiheshimu maskani yake iliyowekwa wakfu, sanduku lililo hai lililombeba Neno asiyeweza kubebwa.", "patron": "Huombwa kwa ajili ya maandalizi ya sikukuu za Mzazi-Mungu."},

"Forefeast of the Meeting of our Lord in the Temple":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Siku ya Kabla ya Sikukuu ya Kukutana kwa Bwana wetu Hekaluni inaadhimishwa tarehe moja ya Februari, siku moja tu ya maandalizi kabla ya sikukuu inayofunga mzunguko wote wa Kuzaliwa kwa Bwana; na katika hiyo Kanisa linayageuza macho yake kuelekea Hekalu la Yerusalemu, ambapo kesho Mtoa-Sheria atabebwa ndani akiwa mtoto wa siku arobaini ili aitimize Sheria yake mwenyewe.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Forefeast of the Nativity of our Lord":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Siku za Kabla ya Sikukuu ya Kuzaliwa kwa Bwana wetu zinakumbatia siku tangu tarehe ishirini ya Desemba hadi kesha la sikukuu, na katika hizo Kanisa, kama Bethlehemu katika nyimbo, linajiandaa. Ibada zinageukia pango kabisa: katika stikira za kila siku wito unalia, Bethlehemu, jiandae.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Forefeast of the Nativity of the Mother of God":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Hii ni Siku ya Kabla ya Sikukuu ya Kuzaliwa kwa Mzazi-Mungu Mtakatifu Zaidi, ambayo katika hiyo Kanisa linaanza kuadhimisha ya kwanza ya sikukuu kuu za mwaka mpya wa kanisa, kuzaliwa kwa Mzazi-Mungu kutoka kwa wenye haki Yoakimu na Ana. Siku hii nyimbo za sikukuu inayokuja zinaanza kusikika katika ibada, zikiwaita waamini waitayarishe mioyo yao ili wamlaki Bikira ambaye kuzaliwa kwake kuliutangazia ulimwengu kukaribia kwa wokovu wake.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Forefeast of the Procession of the Honorable and Lifegiving Cross of the Lord":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Siku hii ni ya kabla ya sikukuu ya Maandamano ya Msalaba wenye Thamani na Utoao Uzima wa Bwana, ambayo Kanisa linaiadhimisha tarehe moja ya Agosti. Katika mji wa kifalme wa Konstantinopoli ilikuwa desturi, katika mwezi wa Agosti wakati magonjwa yalipokuwa mengi kuliko wakati mwingine, kuutoa Mti wa heshima wa Msalaba kutoka hazina.", "patron": "Huombwa kwa ajili ya ukombozi kutoka ugonjwa; kutakaswa."},

"Forefeast of the Transfiguration of our Lord":
{"type": "Kabla ya sikukuu · kiliturujia", "life": "Siku hii ni ya kabla ya sikukuu ya Kugeuka Sura kwa Bwana, Mungu na Mwokozi wetu Yesu Kristo, ambayo Kanisa linaiadhimisha tarehe sita ya Agosti. Akitaka kuwapa wanafunzi wake ladha ya kwanza ya utukufu wa Ufalme kabla ya Mateso yake, Bwana aliwachukua Petro, Yakobo na Yohane na akawapandisha mlima mrefu, na huko aligeuka sura mbele yao, hata uso wake ukang'aa kama jua na mavazi yake yakawa meupe kama nuru.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Glorification of Saint Innocent, Metropolitan of Moscow, Enlightener of the Aleuts, Apostle to the Americas":
{"type": "Metropolita · karne ya 19", "life": "Siku hii Kanisa linaadhimisha kutukuzwa kwa Mtakatifu Inokentio, Metropolita wa Moscow, Mwangazaji wa Waaleuti na Mtume wa Amerika, aliyehesabiwa miongoni mwa watakatifu na Kanisa la Kiorthodoksi la Urusi tarehe sita ya Oktoba mwaka wa 1977, kwa ombi la Kanisa la Kiorthodoksi katika Amerika. Alizaliwa akiitwa Yohane Popov-Veniaminov mwaka wa 1797 katika kijiji cha Siberia.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; watafsiri."},

"Glorification of Saint John of Kronstadt":
{"type": "Kasisi · karne ya 20", "life": "Mtakatifu Yohane wa Kronstadt, mmoja wa wachungaji wakuu wa Kanisa la Urusi, alizaliwa akiitwa Yohane Sergiev mwaka wa 1829 katika kijiji maskini cha kaskazini ya mbali na akawa kasisi wa parokia aliyeoa katika Kanisa Kuu la Mtakatifu Andrea huko Kronstadt, karibu na Saint Petersburg, ambako alihudumu kwa zaidi ya miaka hamsini.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Glorification of Saint Tikhon, Patriarch of Moscow and All Russia, Enlightener of North America":
{"type": "Patriaki · karne ya 20", "life": "Siku hii Kanisa linaadhimisha kutukuzwa kwa Mtakatifu Tikhoni, Patriaki wa Moscow na Urusi Yote, aliyehesabiwa miongoni mwa watakatifu na Baraza la Maaskofu la Kanisa la Kiorthodoksi la Urusi tarehe tisa ya Oktoba mwaka wa 1989. Alizaliwa akiitwa Basili Bellavin mwaka wa 1865, mwana wa kasisi wa kijiji wa Toropets, na alipendwa sana kwa upole wake hata wanafunzi wenzake wa seminari walimwita Patriaki kwa mzaha, bila kujua walikuwa wakitabiri.", "patron": "Maombezi yake huombwa kwa ajili ya wakuu wa Kanisa; wamisionari."},

"Glorification of Venerable Herman of Alaska, Wonderworker of All America":
{"type": "Mtawa · karne ya 19", "life": "Mheshimiwa Hermani wa Alaska, wa kwanza wa watakatifu wa Kiorthodoksi wa Amerika ya Kaskazini, alikuwa mtawa mnyenyekevu wa monasteri ya Valaam katika Urusi ambaye mwaka wa 1794 alijiunga na utume uliotumwa kuipeleka Injili kwa watu wenyeji wa Alaska. Akikaa katika Kisiwa cha Spruce, alichokiita Valaam Mpya, aliishi kama mjinyimaji na akawa baba na mlinzi kwa watu wa Kialeuti, akiwatetea dhidi ya dhuluma za wafanyabiashara wa Kirusi, akiwafundisha watoto, na akiwatunza wagonjwa na yatima, akiwavuta wengi kwa Kristo kwa upole na upendo wake.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Glorification of the Priestmartyr Alexander Hotovitzky":
{"type": "Kuhani Shahidi · karne ya 20", "life": "Siku hii Kanisa linaadhimisha kutukuzwa kwa Kuhani Shahidi Aleksanda Hotovitzky, aliyehesabiwa miongoni mwa watakatifu na Kanisa la Kiorthodoksi la Urusi tarehe nne ya Desemba mwaka wa 1994. Alizaliwa tarehe kumi na moja ya Februari mwaka wa 1872 huko Kremenets katika Volhynia, mwana wa kasisi mkuu mpendwa na mkuu wa seminari, naye Aleksanda alihitimu kwa ubora kutoka Chuo cha Teolojia cha Saint Petersburg.", "patron": "Maombezi yake huombwa kwa ajili ya makasisi wa parokia; wamisionari."},

"Great Martyr Anastasia the Deliverer from Poisons, her teacher, Martyr Chrysogonos, and many with them":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Anastasia, Mkombozi kutoka Sumu, alikuwa Mroma wa ukoo mtukufu, binti wa baba mpagani na mama Mkristo wa siri, Fausta, na alifundwa katika imani na mwalimu wake, mkiri mwenye hekima Krisogono. Akiwa ameolewa kinyume na moyo wake na mpagani Publio, aliihifadhi ubikira wake kwa kujifanya mgonjwa, na akivaa mavazi ya mwombaji, alikwenda pamoja na mtumishi mmoja tu katika magereza ya Roma, akiwalisha, akiwatibu na akiwakomboa mateka wa Kristo, kwa maana alikuwa stadi katika sanaa ya utabibu na akaifanya elimu yake kuwa huduma.", "patron": "Maombezi yake huombwa kwa ajili ya wauguzi; madaktari."},

"Great Martyr Euphemia the All-praised":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Eufemia Mwenye Sifa Zote alikuwa binti wa Wakristo wachaji Mungu wa Kalkedoni, naye aliteseka katika mji ule mwaka wa 303, katika mateso chini ya Diokletiano. Mtawala Prisko alipoamuru wakazi wote washiriki katika sherehe ya sanamu Ares, Eufemia, pamoja na Wakristo wengine waliokuwa wamejificha ili kumwabudu Mungu wa kweli, aligunduliwa na kupelekwa mahakamani.", "patron": "Maombezi yake huombwa kwa ajili ya usafi; kuthibitishwa kwa Uorthodoksi."},

"Great Martyr Irene":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Irene, mmoja wa wanawake mashahidi wapendwao kuliko wote wa Mashariki, alizaliwa, habari za Kigiriki zisimuliavyo, katika mji wa Magedoni, binti wa mtawala mpagani aitwaye Likinio, naye aliitwa Penelope; baba yake alijivunia uzuri wake.", "patron": "Jina la Amani lililopatikana kupitia vita."},

"Great Martyr Katherine of Alexandria":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Katerina wa Aleksandria alikuwa msichana msomi wa ukoo wa kifalme aliyemkiri Kristo wakati wa mateso ya Maksimino. Aliwapinga wanafalsafa wapagani, akawaongoa wengi, na akakataa kuolewa na mfalme. Baada ya kufungwa gerezani na mateso, pamoja na gurudumu lililovunjika, alikatwa kichwa na akapokea taji la shahidi mwanzoni mwa karne ya nne."},

"Great Martyr Marina (Margaret) of Antioch":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Marina, ajulikanaye Magharibi kama Margareti, alilelewa Antiokia ya Pisidia na akamkiri Kristo akiwa msichana wakati wa mateso ya Diokletiano. Akikataa kuolewa na ofisa mpagani na kukataa kutoa dhabihu kwa sanamu, alivumilia kufungwa gerezani na mateso. Akiimarishwa na Kristo, hatimaye alikatwa kichwa na akapokea taji la shahidi mwanzoni mwa karne ya nne."},

"Great Martyr Mercurius of Caesarea, in Cappadocia":
{"type": "Shahidi Mkuu · karne ya 3", "life": "Shahidi Mkuu Mtakatifu Merkurio wa Kaisaria alikuwa askari kijana wa asili ya Kiskithia aliyehudumu katika majeshi ya Kirumi, mwana wa ofisa Mkristo; na washenzi walipomiminika kuvuka mpaka katika siku za mfalme Desio, malaika wa Bwana alimtokea, akaweka upanga mkononi mwake na akamwahidi ushindi, akimwambia amkumbuke Bwana Mungu wake.", "patron": "Maombezi yake huombwa kwa ajili ya askari; ushindi uliotolewa kutoka mbinguni."},

"Great Martyr Theodore the Tyro (Recruit)":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Theodoro Tiro alikuwa askari mpya katika jeshi la Kirumi huko Amasea wakati wa mateso ya Maksimiano. Akikataa kutoa dhabihu kwa sanamu, aliliteketeza hekalu la kipagani na akamkiri Kristo mbele ya mtawala. Baada ya kufungwa gerezani na mateso, alitupwa motoni na akapokea taji la shahidi mwanzoni mwa karne ya nne.", "patron": "Kwa desturi huombwa kwa ajili ya kupatikana kwa vitu vilivyoibwa."},

"Greatmartyr Artemius at Antioch":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Artemio wa Antiokia alikuwa jemadari mashuhuri chini ya Mtakatifu Konstantino Mkuu na mwanawe Konstantio, aliyeheshimiwa kwa ushujaa na utumishi na kufanywa mwakilishi wa mfalme katika Misri, ambako alijitaabisha sana kwa kuieneza imani; na ni Artemio ambaye mfalme alimtuma kuyaleta masalia ya Mtume Andrea kutoka Patra na ya Mtume Luka kutoka Thebe ya Boiotia hadi Konstantinopoli, ambako yaliwekwa katika kanisa la Mitume Watakatifu.", "patron": "Maombezi yake huombwa kwa ajili ya askari; maofisa."},

"Greatmartyr Barbara and Martyr Juliana, at Heliopolis in Syria":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Barbara aliishi Heliopoli katika Syria wakati wa utawala wa Maksimiano. Akiwa amefungiwa peke yake na baba yake mpagani, alimjua Mungu wa kweli na akamkiri Kristo. Baada ya mateso, alikatwa kichwa na baba yake mwenyewe. Mtakatifu Juliana, aliyeyaona mateso yake na akamkiri Kristo, naye aliuawa shahidi mwanzoni mwa karne ya nne."},

"Greatmartyr Euphemia the All-praised":
{"type": "Bikira · karne ya 4", "life": "Siku hii inaadhimisha muujiza mkubwa uliotendwa kupitia Mtakatifu Eufemia Mwenye Sifa Zote katika kuitetea imani ya Kiorthodoksi. Alipokwisha kuteseka shahada huko Kalkedoni chini ya Diokletiano, alitukuzwa upya karne moja na nusu baadaye, mwaka wa 451, wakati Mtaguso Mkuu wa Nne ulipokusanyika katika kanisa lile lile ambamo masalia yake yalilala, ili kuuhukumu uzushi wa Wamonofisi na kukiri asili mbili za Kristo, ya Kimungu na ya kibinadamu.", "patron": "Huombwa kwa ajili ya utetezi wa mafundisho ya Kiorthodoksi."},

"Greatmartyr Eustáthios Placidas, with his wife and children, of Rome":
{"type": "Shahidi Mkuu · karne ya 2", "life": "Shahidi Mkuu Mtakatifu Eustathio, aliyeitwa kabla ya ubatizo wake Plakida, alikuwa jemadari maarufu wa Kirumi chini ya wafalme Tito na Trayano, mkarimu kwa maskini ingawa alikuwa bado mpagani; na alipokuwa akiwinda siku moja alipewa maono ya ajabu, kulungu akimgeukia uso kwa uso na Msalaba wa Kristo ung'aao kati ya pembe zake, na sauti ikimwita kwa jina lake, ikisema, Kwa nini unanifuatilia, Plakida, mimi ni Kristo unayemheshimu bila kujua kwa matendo yako mema.", "patron": "Maombezi yake huombwa kwa ajili ya askari; wawindaji."},

"Greatmartyr George the New at Sofia, Bulgaria":
{"type": "Shahidi Mkuu · karne ya 16", "life": "Shahidi Mkuu Mtakatifu Georgi Mpya, aliyeteseka huko Sofia, alikuwa Mkristo kijana wa Kislavi wa kusini wa zama za nira ya Kituruki, na siku hii inashika kumbukumbu ya kuchukuliwa na kuwekwa mahali pa heshima kwa masalia yake matakatifu, kulikofuata mara baada ya shahada yake.", "patron": "Kijana wa miaka kumi na minane imara kama almasi."},

"Greatmartyr James the Persian":
{"type": "Shahidi Mkuu · karne ya 5", "life": "Shahidi Mkuu Mtakatifu Yakobo Mwajemi, aitwaye Intersiso, Aliyekatwakatwa Vipande, alikuwa mtukufu Mkristo wa Persia, tajiri, mwenye heshima na mpendwa wa Mfalme Yezdegerdi; na roho yake, iliyonaswa na urafiki wa mfalme, ilianguka katika dhambi kubwa ya maisha yake, kwa maana mfalme alipowageukia Wakristo, Yakobo, asiyetaka kupoteza fadhila, alimkana Kristo pamoja na watu wa ikulu.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi wa ikulu; toba baada ya kukana."},

"Greatmartyr Niketas the Goth":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Niketa alikuwa Mgothi, aliyezaliwa na kukaa kando ya Danube, naye alibatizwa na Theofilo, Askofu wa Wagothi, aliyeshiriki katika Mtaguso Mkuu wa Kwanza. Vita vilipowagawanya watu wake na chifu mpagani Athanariki alipoinua mateso makali dhidi ya Wakristo miongoni mwa Wagothi, Niketa, ambaye kwa mahubiri yake na maisha yake matakatifu alikuwa amewaleta jamaa zake wengi kwa Kristo, alikuwa nguzo ya Kanisa lililoteswa, akiwaimarisha waamini kwa shahada na akimshutumu mtesi kwa ujasiri kwa ukatili wake na kutomcha Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya askari; watoto."},

"Greatmartyr Paraskevi of Iconium":
{"type": "Shahidi Mkuu · karne ya 3", "life": "Shahidi Mkuu Mtakatifu Paraskevi wa Ikonio aliishi katika karne ya tatu, akizaliwa katika familia tajiri na yenye uchaji Mungu iliyoiheshimu kwa namna ya pekee Ijumaa ya Mateso ya Bwana, na kwa hiyo wakampa binti yao jina Paraskevi, linalomaanisha Ijumaa. Akipenda usafi tangu ujana wake, aliweka nadhiri ya ubikira wake kwa Kristo na, wazazi wake walipopumzika, aliwapa maskini mali yake na akajitoa kuwaangazia wapagani wa mji wake kwa nuru ya Injili.", "patron": "Maombezi yake huombwa kwa ajili ya wafanyabiashara."},

"Greatmartyr Procopius of Caesarea, in Palestine":
{"type": "Mwakilishi wa mfalme (jemadari) · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Prokopio, aliyeitwa Neanio kabla ya ubatizo wake, alikuwa mzaliwa wa Yerusalemu aliyeishi chini ya mfalme Diokletiano. Akiwa amelelewa na mama yake mpagani Theodosia baada ya kifo cha baba yake Mkristo, alipata elimu bora, akapanda haraka katika utumishi wa kifalme, na akatumwa kama mwakilishi wa mfalme huko Aleksandria ili kuwatesa Wakristo.", "patron": "Maombezi yake huombwa kwa ajili ya askari; kuongoka."},

"Greatmartyr and Healer Panteleimon":
{"type": "Shahidi Mkuu · mwanzo wa karne ya 4", "life": "Shahidi Mkuu na Mponyaji Mtakatifu Panteleimoni alikuwa tabibu kijana wa Nikomedia, aliyeongoka kwa Kristo na kufundishwa na kasisi Hermolao. Aliwaponya wagonjwa bure kwa jina la Kristo, hata wale ambao madaktari wapagani hawakuweza kuwaponya, na akawapa maskini mali yake. Alipodhihirishwa chini ya Maksimiano, alivumilia mateso mengi bila kudhurika kabla ya kukatwa kichwa. Anahesabiwa miongoni mwa Wasiopokea-Malipo Watakatifu.", "patron": "Mlinzi wa madaktari na wagonjwa; huombwa kwa ajili ya afya ya mwili na roho."},

"Greatmartyr, Victory-bearer, and Wonderworker George":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Georgi alikuwa askari Mkapadokia aliyehudumu katika jeshi la Kirumi chini ya Diokletiano. Mateso yalipoinuka, alimkiri Kristo waziwazi, akatoa mali yake, na akakataa kuabudu sanamu. Alivumilia mateso mengi na akakatwa kichwa huko Nikomedia karibu mwaka wa 303, akijulikana kama mbeba-ushindi na mtenda-miujiza."},

"Heiromartyr Theokteristus":
{"type": "Abate, mkiri shahidi · karne ya 9", "life": "Mheshimiwa Theokteristo, aitwaye pia Theosterikto, Mkiri Shahidi na Abate wa monasteri ya Pelekete karibu na Prusa, alisimama katikati ya mojawapo ya matendo mabaya kuliko yote ya mateso ya wapinga-ikoni na akalipa Kanisa, kutoka giza lile, mojawapo ya sala zake zipendwazo kuliko zote. Alizaliwa Triglia katika Bithinia, na akawa mtawa katika ujana wake katika monasteri ya Mtakatifu Yohane.", "patron": "Maombezi yake huombwa kwa ajili ya maabate; watunga nyimbo takatifu."},

"Hieromartyr Alexander of Sίdē, in Pamphylia":
{"type": "Kuhani Shahidi · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Aleksanda alikuwa kasisi wa mji wa Side katika Pamfilia, katika pwani ya kusini ya Asia Ndogo, naye aliteseka katika utawala wa mfalme Aureliano, katika mshtuko wa mwisho wa mateso wa karne ya tatu kabla ya dhoruba kubwa ya Diokletiano. Alipoletwa mbele ya mtawala Antonino, kasisi aliulizwa jina lake na wito wake, naye alijibu kwa ukiri uliofanya mengine yote yasiepukike, kwamba alikuwa Mkristo na mchungaji wa kundi la Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya makasisi mbele ya mahakama; jibu la ujasiri chini ya Aureliano."},

"Hieromartyr Alexander, Bishop of Adrianopolis, and the Martyrs Heraclius, Anna, Elizabeth, Theodota, and Glyceria":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Aleksanda Askofu, Herakleo askari, na wanawake Ana, Elisabeti, Theodota na Glikeria waliteseka huko Adrianopoli katika Thrakia katika zama za mateso. Aleksanda, askofu wa mji ule, aliitangaza Injili kwa ujasiri na akakataa kutoa dhabihu kwa sanamu, na kwa ajili hiyo alidhulumiwa kwa mateso ya muda mrefu na ya kikatili.", "patron": "Maombezi yao huombwa kwa ajili ya kuongoka kupitia ushuhuda wa mashahidi."},

"Hieromartyr Alexander, Bishop of Comana":
{"type": "Askofu · karne ya 3", "life": "Mtakatifu Aleksanda aliishi katika karne ya tatu karibu na Neokaisaria, mtu msomi katika Maandiko na katika sayansi nyingi, ambaye hata hivyo alijitwika jitihada iliyofichwa ya upumbavu kwa ajili ya Kristo, akiishi katika umaskini na akiuza makaa katika uwanja wa mji. Uso wake ulikuwa daima umepakwa weusi wa vumbi la makaa, na wengi walimtazama kwa dharau, bila kuijua hekima yake wala utakatifu wake.", "patron": "Maombezi yake huombwa kwa ajili ya unyenyekevu; hekima iliyofichwa."},

"Hieromartyr Alexander, Bishop of Jerusalem":
{"type": "Askofu · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Aleksanda, Askofu wa Yerusalemu, alifundwa katika shule ya kufundisha imani ya Aleksandria chini ya Klementi, mwanafunzi mwenzake na rafiki wa maisha yote wa Origeni, na akawa askofu wa mji mmoja katika Kapadokia, ambako mateso ya Septimio Severo yalimtia minyororo kwa miaka, mkiri kabla hajawa mkuu wa Kanisa.", "patron": "Maombezi yake huombwa kwa ajili ya watunza maktaba; wasomi."},

"Hieromartyr Antherus (Antheros) Pope of Rome":
{"type": "Askofu · karne ya 3", "life": "Mtakatifu Antero, Mgiriki kwa kuzaliwa, alichaguliwa kuwa Askofu wa Roma akimrithi Mtakatifu Pontiano, lakini alilishika jimbo kwa muda mfupi tu, kwa maana punde alimkiri Kristo na akapata kifo kwa ajili ya imani mwaka wa 236. Alizikwa katika katakomba ya Mtakatifu Kalisto, wa kwanza wa maaskofu wa Roma kuzikwa mahali pale patakatifu, na baada yake Mtakatifu Fabiano alichaguliwa kulichunga Kanisa la Roma.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Hieromartyr Anthimus, Bishop of Nicomedia and those with him":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Anthimo, Askofu wa Nikomedia, alizaliwa katika mji ule na akalelewa tangu utoto katika imani ya Kikristo, na akiwa mnyenyekevu, mwenye amani na aliyejaa bidii kwa utukufu wa Mungu, kwa wakati wake alifanywa askofu wa Nikomedia. Alilichunga Kanisa huko wakati wa mateso makali chini ya Diokletiano na Maksimiano, damu ya Wakristo ilipomwagwa.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti; uchungaji wa uaminifu wakati wa mateso."},

"Hieromartyr Antipas, Bishop of Pergamum and Disciple of Saint John the Theologian":
{"type": "Kuhani Shahidi · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Antipa, Askofu wa Pergamo, anabeba tofauti isiyoshirikiwa na shahidi mwingine yeyote wa Kanisa, kwamba ushuhuda wake umethibitishwa katika Maandiko na sauti ya Kristo mwenyewe; kwa maana katika Ufunuo, katika waraka kwa kanisa la Pergamo, Bwana asema, Napajua unapokaa, ndipo penye kiti cha enzi cha Shetani, nawe walishika sana jina langu, wala hukuikana imani yangu, hata katika siku zile ambazo Antipa shahidi wangu mwaminifu aliuawa kwenu, hapo akaapo Shetani - kumbukumbu ya kifo cha askofu iliyoandikwa na Mungu wake.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu wa upandaji wa kitume; wanaosumbuliwa na magonjwa ya meno."},

"Hieromartyr Apollinaris, Bishop of Ravenna":
{"type": "Askofu · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Apolinari alikuwa mwanafunzi wa Mtume Petro, ambaye alimfuata kutoka Antiokia hadi Roma, na Petro akamweka wakfu kuwa askofu wa kwanza wa Ravenna na akamtuma huko kuihubiri Injili. Alipofika kama mgeni, alipewa makao na askari Irenayo, ambaye alimponya mwanawe kipofu, na hivyo Irenayo na nyumba yake wakawa Wakristo wa kwanza wa Ravenna.", "patron": "Maombezi yake huombwa kwa ajili ya kuangaza kwa umisionari; uponyaji."},

"Hieromartyr Artemon of Laodikeia":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Artemoni, kasisi wa Laodikia katika Syria, alilipa Kanisa maisha yote kabla hajalipa damu yake: alizaliwa kwa wazazi Wakristo, alihudumu kama msomaji kwa miaka kumi na sita, kama shemasi kwa ishirini na minane, na kama kasisi kwa thelathini na mitatu, miaka sabini na saba katika madaraja yapandayo ya patakatifu, hata mateso ya Diokletiano yalipoanza, mtu yaliyemkuta Laodikia alikuwa mzee ambaye vizazi vitatu vilikuwa vimemsikia akisoma, akihudumu na akitoa dhabihu.", "patron": "Maombezi yake huombwa kwa ajili ya wasomaji, mashemasi na makasisi; waliohudumu kwa muda mrefu."},

"Hieromartyr Athanasios, Venerable Anthousa, and others":
{"type": "Askofu · karne ya 3", "life": "Mtakatifu Athanasio, Askofu wa Tarso katika Kilikia, na waliokuwa pamoja naye waliteseka kwa ajili ya Kristo katika karne ya tatu. Mheshimiwa Anthusa, mwanamwali wa Seleukia katika Syria na binti wa wapagani matajiri, alikuwa amesikia habari za imani ya Kikristo na alitamani kufundishwa na askofu Athanasio, na hivyo, akiwachukua watumishi wawili, Karisimo na Neofito, alifika Tarso kwa kisingizio cha safari nyingine.", "patron": "Maombezi yao huombwa kwa ajili ya kuongoka; ukiri thabiti."},

"Hieromartyr Athenogenes, Bishop of Heracleopolis, and his ten disciples":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Athenogene, Askofu wa Herakleopoli, aliteseka pamoja na wanafunzi wake kumi wakati wa mateso chini ya Diokletiano katika mji wa Sebaste katika Kapadokia. Mtawala Filomako alipofanya sikukuu kubwa kwa sanamu na kuwaamuru watu watoe dhabihu, wakazi wa Sebaste, ambao wengi wao walikuwa Wakristo, walikataa, na wengi walipokea taji la shahada chini ya panga za askari.", "patron": "Maombezi yake huombwa kwa ajili ya uchungaji wa uaminifu."},

"Hieromartyr Autonomus, Bishop in Italy":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Autonomo alikuwa askofu katika Italia katika siku za mateso ya Diokletiano, na akijitenga mbele ya dhoruba, alifika Soreoi katika Bithinia, ambako alipokelewa na mtu mchaji Mungu aitwaye Kornelio na, mbali na kupumzika katika usalama, alijitoa kwa mahubiri yasiyochoka, akiwaongoa wapagani wengi mno hata akamweka Kornelio kuwa shemasi na baadaye askofu kwa kundi alilokusanya.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; mahubiri ya umisionari."},

"Hieromartyr Babylas, Bishop of Antioch, and those with him":
{"type": "Askofu · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Babila, Askofu wa Antiokia, aliteseka chini ya mfalme Desio pamoja na ndugu watatu vijana Urbano, Prilidiano na Epoloni na mama yao Kristodula. Mfalme, wakati wa sikukuu ya kipagani mjini, alipotaka kwa udadisi kuingia katika kanisa ambamo askofu mtakatifu alikuwa akiadhimisha Liturujia Takatifu, Babila alitoka na kumzuia njia, akikataa kumruhusu mtawala asiyemcha Mungu aingie katika hekalu la Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya ujasiri mbele ya watawala; ukiri thabiti."},

"Hieromartyr Basil of Ancyra":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Basili, kasisi wa Ankira katika Galatia, alikuwa mlinzi wa kundi la mji ule katika dhoruba mbili zilizofuatana, ya Kiariani na ya kipagani, naye akaanguka katika ya pili. Katika miaka ambayo Waariani walishika mamlaka na makanisa ya Galatia yalitaabishwa, kasisi Basili alijitaabisha bila kuchoka kwa ajili ya imani ya Nikea, akiwaimarisha waliositasita, akiukemea uzushi waziwazi, na akiwashika watu wa Ankira katika ukiri wa kweli ingawa ilimgharimu udhia na kusimamishwa mikononi mwa Waariani.", "patron": "Maombezi yake huombwa kwa ajili ya makasisi wa parokia; watetezi wa kundi dhidi ya uzushi na kuikana imani."},

"Hieromartyr Basil, Bishop of Amasea":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Basili, Askofu wa Amasea katika Ponto, aliishinda taji yake katika saa ya mwisho kabisa ya mateso, chini ya Likinio, wakati mfalme mwenza wa Mashariki, akivunja ahadi zake za uvumilivu, alipowageukia tena Wakristo kwa wivu wake kwa Konstantino; na pambano la Basili lilitokana na tendo la kuhifadhi.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu wanaowahifadhi wanaowindwa; walinzi wa wanawake walio hatarini."},

"Hieromartyr Clement, Pope of Rome":
{"type": "Patriaki · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Klementi, Papa wa Roma, alizaliwa Roma katika familia tajiri na mashuhuri iliyo jamaa ya wafalme, na kwa uangalizi wa ajabu wa Mungu alitengwa katika utoto na wazazi wake na ndugu zake, akalelewa miongoni mwa wageni kwa kila faida ya elimu lakini kwa moyo wa yatima wenye kutamani.", "patron": "Maombezi yake huombwa kwa ajili ya wachonga mawe; waliohamishwa."},

"Hieromartyr Cornelius the Centurion":
{"type": "Askofu · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Kornelio Akida, malimbuko ya watu wa mataifa, alikuwa ofisa wa Kirumi wa kikosi cha Kiitalia kilichokuwa Kaisaria katika Palestina, mtu mchaji Mungu aliyemcha Mungu pamoja na nyumba yake yote, aliyetoa sadaka kwa ukarimu na kusali daima, kama Matendo ya Mitume yashuhudiavyo. Malaika alimtokea, akimwambia kwamba sala zake na sadaka zake zimepanda kuwa ukumbusho mbele za Mungu, na akimwagiza amwite Simoni Petro.", "patron": "Maombezi yake huombwa kwa ajili ya askari; walioongoka."},

"Hieromartyr Cyprian, Bishop of Carthage":
{"type": "Askofu · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Kipriano, Askofu wa Karthago, mmoja wa Mababa wakuu kuliko wote wa Kanisa la mwanzo, alizaliwa karibu mwaka wa 200 katika mji ule, mwana wa seneta mpagani tajiri, na akawa mwalimu maarufu wa ufasaha na falsafa na wakili katika mahakama. Kwa muda mrefu, kama alivyokiri baadaye, alibaki katika giza nene, mbali na nuru ya kweli, na mali zake na anasa zake hazikuweza kuizima kiu yake ya kitu cha juu zaidi.", "patron": "Maombezi yake huombwa kwa ajili ya wanateolojia; umoja wa Kanisa."},

"Hieromartyr Cyprian, Virgin Martyr Justina, and Martyr Theoctistus, of Nicomedia":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Kipriano, Bikira Shahidi Yustina, na Shahidi Theoktisto waliteseka Nikomedia mwaka wa 304. Kipriano alikuwa mwanafalsafa na mchawi wa Antiokia, aliyefundishwa tangu utoto katika siri za kipagani juu ya Olimpo na katika Argo, Memfi na Babeli, hata akajulikana kama mtumishi wa mkuu wa giza.", "patron": "Maombezi yao huombwa kwa ajili ya ukombozi kutoka uchawi na pepo wabaya; usafi uliolindwa na Msalaba."},

"Hieromartyr Cyril, Bishop of Gortyna in Crete":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Kirilo alikuwa askofu wa Gortina katika kisiwa cha Krete, aliyeichunga kwa uaminifu kwa miaka hamsini, naye alikuwa mzee wa umri mkubwa wakati mateso ya Wakristo yalipoufikia mji wake. Alipokamatwa na kuamriwa atoe dhabihu kwa sanamu, alikataa, na akahukumiwa kuchomwa akiwa hai.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri thabiti."},

"Hieromartyr Desan, Bishop in Persia, and 272 others with him":
{"type": "Makuhani Mashahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Desani, Askofu katika Persia, aliteseka pamoja na wenzake mia mbili na sabini na wawili katika mateso ya Mfalme Sapori wa Pili, karibu miaka ya 362 hadi 364, na pambano lao linahifadhi kumbukumbu ya mojawapo ya ukatili wa pekee wa mateso yale, shahada ya waliohamishwa kwa nguvu. Majeshi ya Persia yalipoziteka ngome za mpaka wa Kirumi za Mesopotamia, yaliwachukua Wakristo wote hadi ndani ya ufalme, wakleri na watu pamoja, makutaniko yakingolewa pamoja na wachungaji wao na kutembezwa mashariki kama nyara zilizo hai.", "patron": "Maombezi yao huombwa kwa ajili ya makutaniko yaliyohamishwa kwa nguvu; wakleri pamoja na watu wao."},

"Hieromartyr Dionysius the Areopagite, Bishop of Athens":
{"type": "Askofu · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Dionisio Mwareopago alikuwa Mwathene mtukufu, msomi katika hekima yote ya Wagiriki, ambaye akiwa kijana akisoma huko Heliopoli katika Misri aliliona giza lililoifunika nchi katika saa ya Kusulubiwa na akasema, Ama Mungu anateseka, ama ulimwengu unafikia mwisho wake.", "patron": "Maombezi yake huombwa kwa ajili ya wanateolojia; wanafalsafa."},

"Hieromartyr Dorotheus, Bishop of Tyre":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Dorotheo, Askofu wa Tiro, alikuwa mkiri na shahidi wa maisha marefu ya ajabu, aliyevumilia katika mateso matatu na akalipa Kanisa, zaidi ya ushuhuda wake, habari zinazothaminiwa juu ya mitume.", "patron": "Maaskofu wa maisha marefu na majaribu mengi; wakiri katika mateso yaliyofuatana."},

"Hieromartyr Emilian and with him Martyrs Hilarion, Dionysius, and Hermippus":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Emiliano, Askofu wa Trebia, pamoja na Hilarioni, Dionisio na Hermipo, alizaliwa katika Armenia; na baada ya kifo cha wazazi wao ndugu Emiliano, Dionisio na Hermipo, pamoja na mwalimu wao Hilarioni, waliiacha nchi yao na wakafika Italia, katika mji wa Spoleto. Huko Emiliano aliihubiri Injili kwa wapagani, na kwa kuwa aliheshimiwa kwa maisha yake makali na yenye fadhila alichaguliwa kuwa Askofu wa Trebia na akawekwa wakfu na Marselino wa Roma.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri ya umisionari."},

"Hieromartyr Eusebius, Bishop of Samosata":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Eusebio, Askofu wa Samosata, alikuwa mmoja wa mashujaa wakuu wa imani ya Kiorthodoksi dhidi ya uzushi wa Kiariani katika karne ya nne, rafiki na mtenda kazi mwenzake wa mababa wakuu kuliko wote wa zama zake na mkiri aliyekufa kifo cha shahidi.", "patron": "Watetezi wa Uorthodoksi dhidi ya uzushi; maaskofu waliohamishwa kwa ajili ya imani."},

"Hieromartyr Euthymius, Bishop of Sardis":
{"type": "Askofu · karne ya 9", "life": "Kuhani Shahidi Mtakatifu Euthimio, Askofu wa Sardi, aliinuliwa hadi jimbo lile la kale kwa maisha yake yenye fadhila katika siku za Konstantino na Irene, na akasimama katika Mtaguso Mkuu wa Saba mwaka wa 787 miongoni mwa waliokemea uzushi wa wapiga-ikoni; na uzushi ulipokirudia kiti cha enzi, uaskofu wake ukawa mnyororo wa uhamisho wa miaka arobaini, mmoja kwa kila mfalme aliyedai kile ambacho hangekitoa.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu waliohamishwa; kuheshimu ikoni takatifu."},

"Hieromartyr Eutyches, disciple of Saint John the Theologian":
{"type": "Askofu · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Eutike alikuwa mwanafunzi wa Mitume watakatifu Yohane Mwanateolojia na Paulo, na ingawa hakuwa miongoni mwa wale Sabini, anaheshimiwa kwa jina la Mtume kwa kazi zake pamoja nao, ambao walimweka kuwa askofu. Alizaliwa katika mji wa Sebastea katika Samaria, kwanza alimfuata Mtume Yohane, na baadaye, alipokutana na Mtume Paulo, aliihubiri Injili pamoja naye katika safari zake, naye alisafiri katika nchi nyingi akimtangaza Kristo na kuyaangusha mahekalu ya sanamu.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuhubiri."},

"Hieromartyr Gregory, Bishop of Greater Armenia, Equal of the Apostles, Enlightener of Armenia":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Gregorio, Askofu wa Armenia Kubwa, Sawa na Mitume na Mwangazaji wa Armenia, alikuwa mwana wa mtukufu Mparthia Anaki, aliyekuwa amemwua mfalme wa Armenia; na mtoto mchanga Gregorio, aliyeokolewa na kisasi kilichoiangamiza nyumba yake, alichukuliwa hadi Kaisaria katika Kapadokia na akalelewa huko katika imani ya Kikristo.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuangazwa kwa mataifa."},

"Hieromartyr Hermogenes, Patriarch of Moscow and All Russia":
{"type": "Shahidi · karne ya 17", "life": "Kuhani Shahidi Mtakatifu Hermogene, Patriaki wa Moscow na Urusi Yote, ambaye kutukuzwa kwake Kanisa linakuadhimisha siku hii, alikuwa mchungaji ambaye uthabiti wake gerezani uliiokoa nchi yake, na ambaye sikukuu yake Kanisa la Urusi linaiadhimisha katika tarehe ya kutukuzwa kwake kama linavyoadhimisha kupumzika kwake mwezi wa Februari.", "patron": "Barua zilizoinua majeshi ya wananchi."},

"Hieromartyr Hermogenes, Patriarch of Moscow, Wonderworker of All Russia":
{"type": "Patriaki, kuhani shahidi · karne ya 17", "life": "Kuhani Shahidi Mtakatifu Hermogene, Patriaki wa Moscow na Urusi Yote, alikuwa nanga iliyolishika taifa lililokuwa likizama, naye aliishika kutoka chumba cha njaa. Alizaliwa karibu mwaka wa 1530, alihudumu kama kasisi wa parokia huko Kazan, na mwaka wa 1579 alisimama katika tukio lililoyatia alama maisha yake, kupatikana kwa Ikoni ya Kazan ya Mzazi-Mungu, akiibeba sura iliyofunuliwa karibuni katika maandamano kwa mikono yake mwenyewe na baadaye akatunga habari za kutokea kwake na ibada kwa heshima yake, kasisi akiwa mwandishi wa kwanza wa historia ya ikoni ile.", "patron": "Maombezi yake huombwa kwa ajili ya mapatriaki; watetezi wa roho ya taifa."},

"Hieromartyr Hermolaus and Martyrs Hermippus and Hermocrates at Nicomedia":
{"type": "Kasisi · karne ya 4", "life": "Makuhani Mashahidi Watakatifu Hermolao, Hermipo na Hermokrate walikuwa miongoni mwa wachache waliosalia baada ya Wakristo elfu ishirini kuteketezwa hadi kufa katika kanisa huko Nikomedia wakati wa mateso chini ya Maksimiano. Wakiishi mafichoni, hawakuacha kuihubiri Injili kwa wapagani, na ni kasisi Hermolao ambaye, alipomwona kijana mpagani Pantoleoni akipita karibu na makao yake, alimwita ndani na akamfundisha ubatili wa kuabudu sanamu na kweli ya Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya wakatekisti."},

"Hieromartyr Hierotheus, Bishop of Athens":
{"type": "Askofu · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Hierotheo, Askofu wa Athene, alikuwa mmoja wa baraza la Areopago na aliletwa kwa Kristo, pamoja na Dionisio Mwareopago, kwa mahubiri ya Mtume Mtakatifu Paulo, aliyemweka wakfu kuwa askofu wa kwanza wa Athene; naye kwa upande wake alimfundisha Dionisio kwa ukamilifu zaidi katika siri za imani, hata mwanafunzi wake anamwita mwalimu na anazungumza kwa heshima juu ya nyimbo zake na maelezo yake ya upendo wa Kimungu.", "patron": "Maombezi yake huombwa kwa ajili ya wanateolojia; watunga nyimbo takatifu."},

"Hieromartyr Hippolytus, and those with him":
{"type": "Kuhani Shahidi · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Hipolito wa Roma aliteseka pamoja na mashahidi Kensorino, Sabino, bikira Krise, na wengine ishirini katika karne ya tatu, karibu mwaka wa 269, chini ya mfalme Klaudio; na pambano la kikundi kile lilianza na hakimu. Kensorino, ofisa wa cheo cha juu, alisingiziwa kuwa Mkristo na akafungwa gerezani, na gerezani neema ya Kristo ikatenda kazi.", "patron": "Maombezi yao huombwa kwa ajili ya wanateolojia; waandishi."},

"Hieromartyr Ignatius the God-Bearer, Bishop of Antioch":
{"type": "Kuhani Shahidi · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Ignatio Mbeba-Mungu alikuwa Askofu wa Antiokia na mwanafunzi wa zama za kitume. Alipokamatwa chini ya mfalme Trayano, alichukuliwa kuelekea Roma na akaandika nyaraka zikiyaimarisha makanisa katika imani, umoja na utii. Alitamani kuteseka kwa ajili ya Kristo na akatupwa kwa wanyama wakali huko Roma mwanzoni mwa karne ya pili."},

"Hieromartyr Irenaeus, Bishop of Lyons":
{"type": "Askofu · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Ireneo, Askofu wa Lyons, mmoja wa walimu wakuu wa Kanisa la mwanzo, alizaliwa karibu mwaka wa 130 huko Smirna na akapokea elimu bora katika ujuzi wa siku zake. Mwongozi wake katika imani alikuwa Mtakatifu Polikarpo wa Smirna, ambaye yeye mwenyewe alikuwa mwanafunzi wa Mtume Yohane Mwanateolojia, na katika uzee wake Ireneo alikumbuka jinsi akiwa mvulana alivyomsikiliza Polikarpo akinena juu ya mazungumzo yake na wale waliomwona Bwana, akiyaandika mambo hayo, kama alivyosema, si juu ya karatasi bali juu ya moyo wake.", "patron": "Maombezi yake huombwa kwa ajili ya wanateolojia; Teolojia ya Kiothodoksi."},

"Hieromartyr Irenaeus, Bishop of Sirmium":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Ireneo, Askofu wa Sirmio katika Panonia, aliteseka katika mateso makuu mwaka wa 304, na pambano lake limehifadhiwa katika habari za uhalisi wa daraja la kwanza, miongoni mwa zilizo na thamani kuliko zote za kumbukumbu za kale za mashahidi. Akiwa kijana kwa cheo chake, na mtu mwenye mke na watoto kwa nidhamu ya zama zile, Ireneo alikamatwa akiwa askofu na akaletwa mbele ya mtawala Probo.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu wenye familia; ambao wapendwa wao wanasihi dhidi ya ukiri wao."},

"Hieromartyr Januarius, Bishop of Benevento, and his companions, at Pozzuoli":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Yanuario, Askofu wa Benevento, aliteseka pamoja na wenzake huko Pozzuoli mwaka wa 305, katika kilele cha mateso ya Diokletiano, na mateso yake ni picha ya kamba za upendo za Kanisa la kale, kwa maana alikamatwa kwa sababu ya kutembelea: shemasi wake Sosio wa Miseno na wakleri wengine walipokuwa wamefungwa gerezani.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu pamoja na mashemasi wao; miji na walinzi wake."},

"Hieromartyr Kindeos the Presbyter of Pamphylia":
{"type": "Kasisi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Kindeo alikuwa kasisi katika Pamfilia katika Asia Ndogo wakati wa mateso ya mfalme Diokletiano. Bila kutishwa na hatari, alifanya kazi kwa bidii kuihubiri Injili na kuwaimarisha waamini, na aliposingiziwa kwa mamlaka kwa ajili hiyo, alikamatwa na akauawa kwa jina la Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri yenye bidii."},

"Hieromartyr Kuksha and Venerable Pimen of the Kyiv Near Caves":
{"type": "Mtawa kuhani · karne ya 12", "life": "Mheshimiwa Kuksha, Kuhani Shahidi, alikuwa mtawa wa Mapango ya Kyiv aliyetoka kwenda kuihubiri Injili kwa Wavyatichi, taifa kali la kipagani lililokaa katika misitu kando ya mto Oka, waliokuwa wakiishi, kama mtunga habari alivyosema, kwa siku ya leo peke yake na hawakujua lolote la sheria ya Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuangaza kwa umisionari."},

"Hieromartyr Lucian the Presbyter of the Kyiv Caves":
{"type": "Kuhani Shahidi · karne ya 13", "life": "Kuhani Shahidi Mtakatifu Lukiano, Kasisi wa Mapango ya Kyiv, alimtumikia Mungu kama mtawa kuhani wa Lavra kubwa katika miaka ya kutisha kuliko yote ambayo mji wake uliwahi kuyajua, wakati makundi ya Batu yalipoivamia Urusi, na Kyiv, mama wa miji yake, ikatolewa kwa moto na machinjo. Katika uharibifu ule, karibu mwaka wa 1243, kasisi Lukiano alipokea taji la shahada, akiuawa na wavamizi wasiomcha Mungu huku akibaki katika kituo chake miongoni mwa mapango matakatifu.", "patron": "Maombezi yake huombwa kwa ajili ya uaminifu hadi damu."},

"Hieromartyr Lucian, Bishop of Beauvais, and those with him in France":
{"type": "Kuhani Shahidi · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Lukiano, Askofu wa Beauvais, alikuwa mmoja wa waangazaji wamisionari wa Gaul ya kale, aliyetumwa, mapokeo yashikavyo, kutoka Roma kuihubiri Injili miongoni mwa makabila ya kaskazini yaliyokuwa bado ya kipagani, naye aliutia muhuri utume wake huko kwa shahada katika karne ya tatu.", "patron": "Maaskofu wamisionari; waangazaji wa Gaul."},

"Hieromartyr Marcellinus, Pope of Rome, and those with him":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Marselino, Papa wa Roma, aliliongoza Kanisa la Roma katika kilele cha mateso ya Diokletiano, wakati, habari zisemavyo, maelfu waliuawa shahidi katika mwezi mmoja.", "patron": "Mwenye toba baada ya kuanguka; waliorudishwa kwa toba."},

"Hieromartyr Mark, Bishop of Arethusa, who suffered under Julian the Apostate":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Marko, Askofu wa Arethusa katika Syria, alikuwa tayari mzee aliyejaa miaka na heshima wakati Yuliano Mwasi alipowaachilia wapagani juu ya Kanisa, na pambano lake, lililohifadhiwa kwa vizazi na Mtakatifu Gregorio Mwanateolojia, ni mojawapo ya ya ajabu na ya utukufu kuliko yote ya mateso yale ya ajabu.", "patron": "Maombezi yake huombwa kwa ajili ya wazee katika jaribu; wanaojitoa wenyewe kwa ajili ya wengine."},

"Hieromartyr Methodius, Bishop of Patara":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Methodio, Askofu wa Patara, alikuwa mmoja wa mababa wasomi na wanateolojia wa Kanisa la mwanzo, mtetezi wa imani ya kweli dhidi ya upotovu na shahidi katika mateso makuu ya mwisho. Alikuwa askofu wa Olimpo na wa Patara katika Likia, na baadaye, mapokeo yasemavyo, wa Tiro, mtu wa elimu pana na ufasaha, naye alitumia vipaji vyake katika utumishi wa imani, hasa katika kazi mbili kubwa.", "patron": "Maaskofu na wanateolojia; watetezi wa ufufuo wa mwili."},

"Hieromartyr Mocius the Presbyter of Amphipolis in Macedonia":
{"type": "Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Mokio alikuwa kasisi wa kanisa la Amfipoli katika Makedonia, au kama habari nyingine zimwekavyo katika Thrakia, naye aliteseka huko Bizanti katika mateso ya Diokletiano, karibu na mwanzo wa karne ya nne.", "patron": "Hekalu la sanamu lililoangushwa."},

"Hieromartyr Mίlos (or Milēs) the Wonderworker, and two disciples":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Milo, Askofu wa Persia, alikuwa katika ujana wake askari na jemadari, na alipouacha utumishi wa wafalme wa duniani, alikuwa mtawa na kwa wakati wake akawekwa askofu wa mji wa kale wa Susa, ambako Nabii Danieli aliyaona maono yake. Kwa maisha yake ya ujinyimaji Mungu alimpamba kwa vipaji vya uponyaji na unabii.", "patron": "Maombezi yake huombwa kwa ajili ya ujasiri wa kinabii; Kanisa la Persia."},

"Hieromartyr Nestor, Bishop of Magydos in Pamphylia":
{"type": "Kuhani Shahidi · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Nestori, Askofu wa Magido katika Pamfilia, aliteseka mwaka wa 250, katika mateso ya Desio, na pambano lake linaonyesha hesabu ya mchungaji katika umbo lake safi kuliko yote: wote watoke, yeye wa mwisho, yeye peke yake. Amri ya kifalme ilipoifikia Pamfilia na uwindaji ukaanza, Nestori hakuliita kundi lake kwa msimamo mtukufu wa pamoja.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu wanaobaki; wachungaji wa makundi yanayowindwa."},

"Hieromartyr Nikḗtas":
{"type": "Kuhani Shahidi · karne ya 19", "life": "Mheshimiwa Niketa Mpya, Kuhani Shahidi ambaye kalenda za siku hii zinamwadhimisha, alikuwa mtawa kuhani wa Skete ya Mtakatifu Ana juu ya Mlima Mtakatifu, naye ni wa kikundi chenye nuru cha mashahidi wapya wa Athos, watawa ambao Mlima Mtakatifu, katika karne za nira ya Kituruki, uliwaiva kwa makusudi na kuwaachilia kwenye shahada, wazee wakiwaandaa wa kujitolea kwa ujinyimaji mrefu na sala isiyokoma kwa huduma ile moja ambayo Kanisa lililoshindwa lingeweza bado kuitekeleza hadharani, ukiri wa Kristo hadi damu.", "patron": "Maombezi yake huombwa kwa ajili ya watawa makuhani; wahubiri chini ya mamlaka yenye uadui."},

"Hieromartyr Pancratius, Bishop of Taormina in Sicily":
{"type": "Askofu · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Pankratio, Askofu wa Taormina, alizaliwa katika siku ambazo Bwana wetu alitembea juu ya nchi, kwa wazazi wa Antiokia. Baba yake, aliposikia habari za Mwalimu mkuu, alimchukua Pankratio kijana pamoja naye hadi Yerusalemu, na alipoiona miujiza na kusikia mafundisho ya Kimungu, alimwamini Kristo na akawakaribia mitume, hasa Petro.", "patron": "Maombezi yake huombwa kwa ajili ya kuangaza kwa umisionari."},

"Hieromartyr Paphnutius of Jerusalem":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Pafnutio wa Yerusalemu aliteseka katika mateso makuu ya mwisho, katika miaka ya Diokletiano na wenzake, na kalenda zinaishika kumbukumbu yake pamoja na cheo na kikundi: akiwa askofu, alipitia, habari zinavyoandika, kipimo kizima kinachopanda cha hoja za mahakama, akiteswa kwa moto, akitupwa kwa wanyama wakali, na mwishoni akikatwa kichwa kwa upanga, vyombo vitatu vya kawaida vikimalizwa juu ya mkiri mmoja asiyetikisika.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu katika machimbo na magereza; vikundi vya waliohamishwa."},

"Hieromartyr Patriarch Gregory V of Constantinople":
{"type": "Kuhani Shahidi, patriaki · karne ya 19", "life": "Kuhani Shahidi Mtakatifu Gregorio wa Tano, Patriaki wa Konstantinopoli, alizaliwa akiitwa Georgio Angelopulo mwaka wa 1746 huko Dimitsana katika Peloponeso, kwa wazazi maskini na wachaji Mungu, na akapanda kwa elimu na ukali wa maisha kupitia monasteri na jimbo la Smirna hadi kiti cha enzi cha kiekumeni, alichokikalia mara tatu, vipindi vya katikati vikijazwa na uhamisho katika Athos, kwa maana bidii yake katika kujenga upya makanisa, kuchapisha vitabu na kuwaadibu wakleri ilimfanya asiwe wa kupendeza kwa wenye mamlaka mara zaidi ya moja.", "patron": "Maombezi yake huombwa kwa ajili ya mapatriaki; taifa la Ugiriki."},

"Hieromartyr Patrick, Bishop of Prusa, and his companions":
{"type": "Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Patriki, Askofu wa Prusa katika Bithinia, aliteseka pamoja na wenzake makasisi Akakio, Menanda na Polieno katika zama za mateso, na pambano lake liligeukia ukiri wa ujasiri na wa uzuri uliotolewa kwenye chemchemi maarufu za maji ya moto za mji wake.", "patron": "Muumba wa chemchemi za moto na moto wa hukumu aliyekiriwa."},

"Hieromartyr Peter, Archbishop of Alexandria":
{"type": "Patriaki · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Petro, Askofu Mkuu wa Aleksandria, alilelewa katika shule kubwa ya kufundisha imani ya mji ule, ambayo alikuwa mkuu wake, na mwaka wa 300 alipanda kiti cha enzi cha upatriaki, ili tu alichunge Kanisa lake moja kwa moja hadi katika moto wa mateso ya mwisho na makali kuliko yote. Akiwindwa kutoka mahali hadi mahali, aliliongoza kundi lake lililotawanyika kwa wajumbe na nyaraka, akiwaimarisha wakiri, na akitunga kwa hekima ya kichungaji kanuni za toba ambazo kwazo walioanguka chini ya mateso wangeweza kurudishwa kwa toba, kanuni ambazo Kanisa lote lilizipokea katika sheria yake.", "patron": "Maombezi yake huombwa kwa ajili ya wakatekisti; wakuu wa Kanisa."},

"Hieromartyr Philip, Bishop of Heraclea and with him the Martyrs Severus, Memnon, and 37 Soldiers in Thrace":
{"type": "Askofu · karne ya 4", "life": "Mtakatifu Filipo, Askofu wa Heraklea, aliteseka kwa ajili ya Kristo katika mji wa Filipopoli katika Thrakia, pamoja na kikundi kikubwa cha waamini, katika mateso chini ya Diokletiano. Miongoni mwao alikuwa Mtakatifu Severo, aliyekuwa amemleta akida Memnoni katika imani ya Kristo; na jambo hili lilipojulikana kwa mtawala, alimtoa askari yule kwa mateso, na Severo naye aliteswa kikatili, akichanwa kwa kulabu za chuma, akichomwa kwa pete zilizotiwa moto na mshipi wa chuma, na mwishoni akinyang'anywa kuona kwake.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Hieromartyr Philosophos of St. Petersburg":
{"type": "Shahidi · karne ya 20", "life": "Kuhani Shahidi Mtakatifu Filosofo Ornatsky, kasisi mkuu wa Saint Petersburg, alikuwa mmoja wa wa kwanza na mashuhuri kuliko wote wa mashahidi wapya wa Kanisa la Urusi chini ya mateso ya Wabolsheviki, mchungaji maarufu wa mji mkuu wa kifalme aliyeuawa shahidi pamoja na wanawe wawili katika mapambazuko yenyewe ya hofu isiyomcha Mungu.", "patron": "Imani iliyohubiriwa kwa ujasiri katika mji mkuu."},

"Hieromartyr Phocas, Bishop of Sinope":
{"type": "Askofu · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Foka, Askofu wa Sinope kando ya Bahari Nyeusi, aliishi maisha yenye fadhila tangu ujana wake na akiwa askofu wa mji wa kwao aliwageuza wapagani wengi kwenye imani ya Kristo. Katika mateso chini ya mfalme Trayano mtawala alidai amkane Bwana, na mtakatifu alipokataa, alidhulumiwa kwa mateso makali na mwishoni akafungiwa katika bafu iliyotiwa moto, ambako alipokea taji la shahada mwaka wa 117.", "patron": "Maombezi yake huombwa kwa ajili ya mabaharia; ulinzi kutoka moto."},

"Hieromartyr Polycarp, Bishop of Smyrna":
{"type": "Kuhani Shahidi · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Polikarpo, Askofu wa Smirna, ni bawaba kubwa kati ya mitume na Kanisa la zama zote: mwanafunzi wa Yohane Mwanateolojia mwenyewe, aliyewekwa katika jimbo la Smirna katika mfululizo wa Bukolo, rafiki ambaye Ignatio aliyehukumiwa alimwandikia akiwa njiani, Simama imara kama fuawe chini ya nyundo.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu; waamini wazee."},

"Hieromartyr Proterius, Patriarch of Alexandria":
{"type": "Patriaki, kuhani shahidi · karne ya 5", "life": "Kuhani Shahidi Mtakatifu Proterio, Patriaki wa Aleksandria, alikuwa mtu aliyewekwa kulishika jimbo la hatari kuliko yote katika Ukristo kwa ajili ya imani ya Kalkedoni, naye akalishika hadi tone la mwisho. Akiwa kasisi wa Aleksandria chini ya patriaki Dioskoro, alikuwa na ujasiri wa kuukemea upotovu wa Kimonofisi wa mkuu wake mwenyewe wa Kanisa na kuikiri imani ya Kiorthodoksi ya asili mbili wakati Dioskoro alipokuwa katika kilele cha nguvu zake.", "patron": "Maombezi yake huombwa kwa ajili ya wakuu wa Kanisa katikati ya makundi ya ghasia; watetezi wa Kalkedoni."},

"Hieromartyr Publius, Bishop of Athens":
{"type": "Kuhani Shahidi · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Publio, Askofu wa Athene, anaingia katika Maandiko kwa tendo la ukarimu: yeye ni Publio wa Matendo ya Mitume, mtu mkuu wa kisiwa cha Malta, ambaye, Mtume Paulo alipotupwa ufuoni huko na kuvunjika kwa meli katika safari ya kwenda Roma, alimpokea Mtume na wenzake na kuwafikisha kwa siku tatu kwa ukarimu.", "patron": "Maombezi yake huombwa kwa ajili ya wenyeji na wakarimu; maaskofu wa majimbo ya kale."},

"Hieromartyr Sadoc (Sadoth), Bishop of Persia, and 128 Martyrs with him":
{"type": "Askofu, kuhani shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Sadoki, Askofu wa Persia, aliteseka pamoja na wenzake mia moja na ishirini na wanane karibu mwaka wa 342, katika mateso makuu ya Shapuri wa Pili, wakati himaya ya Persia ilipojiwekea kulikomesha Kanisa la Mashariki; alikuwa amemrithi kuhani shahidi Simeoni, wa kwanza wa maaskofu wa mateso yale kuvikwa taji, naye alirithi pamoja na kiti cha enzi uhakika wa karibu wa mwisho uleule.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu wakati wa mateso; vikundi vya wakiri."},

"Hieromartyr Seraphim (Samoilovich), Archbishop of Uglich":
{"type": "Askofu Mkuu · karne ya 20", "life": "Kuhani Shahidi Mtakatifu Serafimu, Askofu Mkuu wa Uglich, alizaliwa akiitwa Semyon Samoylovich mwaka wa 1881 huko Myrgorod katika nchi za Poltava, na baada ya seminari alijitolea kwa utume wa Amerika, akifundisha katika shule ya kanisa ya Unalaska na kisha huko Sitka, ambako alinyolewa utawa na kuwekwa mtawa kuhani, akiitumikia misheni ya Alaska na seminari ya Sitka kama mtenda kazi mwenzake mwenye bidii wa Patriaki Tikhoni wa baadaye, aliyemthamini sana.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; wakuu wa Kanisa."},

"Hieromartyr Silvanus of Gaza":
{"type": "Askofu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Silvano wa Gaza alikuwa mzaliwa wa mji ule, kwanza askari na baadaye kasisi, na katika uzee wake aliinuliwa hadi uaskofu, akilichunga Kanisa la Gaza katika miaka ya mateso makuu. Akisingiziwa na kuhukumiwa, alihukumiwa kazi ngumu katika machimbo ya shaba ya Faeno, ambako, akiwa mzee na aliyechoka, alibeba taabu ya kuponda kwa imani isiyovunjika, akiwaimarisha wakiri wengi waliohukumiwa pamoja naye na bila kukoma kuwafundisha na kuwafariji kama baba wa kweli.", "patron": "Maombezi yake huombwa kwa ajili ya wafungwa; wachimba migodi."},

"Hieromartyr Simeon, Bishop in Persia, and those with him":
{"type": "Kuhani Shahidi, askofu mkuu · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Simeoni, Askofu Mkuu wa Seleukia-Ktesifoni na Mkuu wa Kanisa la Persia, alisimama mbele ya Kanisa lile wakati Mfalme Sapori wa Pili, akiwa vitani na himaya ya Kikristo ya Warumi, alipowafungulia raia wake Wakristo mateso yaliyodumu miaka arobaini na kuvuna maelfu wasiohesabika.", "patron": "Maombezi yake huombwa kwa ajili ya wakuu wa Makanisa wakati wa mateso; wakleri waliouawa pamoja na askofu wao."},

"Hieromartyr Simeon, kinsman of the Lord, second Bishop of Jerusalem":
{"type": "Kuhani Shahidi, mtume · karne ya 2", "life": "Kuhani Shahidi Mtakatifu Simeoni, jamaa wa Bwana na Askofu wa pili wa Yerusalemu, alikuwa mwana wa Klopa, ndugu wa Mwenye haki Yosefu Mchumba, na hivyo, kwa namna ya hesabu ya Sheria, binamu wa Bwana kwa jinsi ya mwili, mmoja wa mzunguko ule wa familia ambao kutoamini kuliuona wakati mmoja kuwa kikwazo na neema ikaufanya kuwa kitalu cha maaskofu.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu wa utumishi mrefu; jamaa wa Bwana."},

"Hieromartyr Sisinius the Deacon of Rome and those with him":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Sisinio Shemasi aliteseka kwa ajili ya Kristo huko Roma, pamoja na kikundi kikubwa cha mashahidi wenzake, katika mateso makali ya wafalme mwanzoni mwa karne ya nne.", "patron": "Mashemasi na watumishi wa Kanisa; vikundi vizima vilivyouawa pamoja."},

"Hieromartyr Terence, Bishop of Iconium":
{"type": "Askofu · karne ya 1", "life": "Kuhani Shahidi Mtakatifu Terentio, Askofu wa Ikonio, alikuwa mmoja wa wachungaji wa kwanza wa zama za kitume, aliyewekwa juu ya Kanisa la Ikonio katika Likaonia, mji ambako Mtume Paulo alikuwa amehubiri na kuteseka, naye aliutia muhuri uaskofu wake kwa shahada.", "patron": "Maaskofu wa kwanza wa Makanisa ya kitume; waliowekwa na mitume."},

"Hieromartyr Theodore of Perge in Pamphylia, his mother, Philippa, and Martyrs Dioscorus, Socrates, and Dionysius":
{"type": "Mashahidi · karne ya 2", "life": "Shahidi Mtakatifu Theodoro wa Perge katika Pamfilia aliteseka katika karne ya pili, katika utawala wa Antonino, pamoja na mama yake Filipa na mashahidi Dioskoro, Sokrate na Dionisio, na mateso yake yanakusanya katika pambano moja ukiongoko ule tatu upendwao na Kanisa: mwana, mama na wanyongaji.", "patron": "Maombezi yao huombwa kwa ajili ya vijana walioandikishwa jeshini; mama wa mashahidi."},

"Hieromartyr Theodotus, Bishop of Ancyra":
{"type": "Shahidi · karne ya 4", "life": "Siku hii Kanisa linaadhimisha kumbukumbu ya pekee ya Shahidi Mtakatifu Theodoto wa Ankira, ambaye mateso yake yanasimuliwa kwa ukamilifu zaidi katika kalenda pamoja na mabikira saba wa Ankira, na ambaye sikukuu hii inamheshimu hasa katika shahada yake mwenyewe.", "patron": "Wenye nyumba za wageni na wenyeji; wanaozika mashahidi."},

"Hieromartyr Theodotus, Bishop of Cyrenia":
{"type": "Kuhani Shahidi, mkiri · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Theodoto, Askofu wa Kirenia katika Kipro, alikuwa mzaliwa wa Galatia katika Asia Ndogo aliyekuja kulichunga jimbo lile la Kipro katika majira ya mwisho na mabaya kuliko yote ya mateso, wakati Likinio, akivunja urafiki na mwenzake Konstantino, alipoyafanya upya Mashariki mahangaiko ambayo Amri ya Milano ilipaswa kuwa imeyakomesha.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu walio chini ya mateso; wanaoishi zaidi ya watesi wao."},

"Hieromartyr Therapon, Bishop of Cyprus":
{"type": "Shahidi · kiliturujia", "life": "Kuhani Shahidi Mtakatifu Therapo, Askofu wa Kipro, alikuwa mchungaji wa Kanisa katika kisiwa kile aliyeutia muhuri utumishi wake kwa kifo cha shahidi, na ambaye masalia yake yakajulikana kwa manukato ya uponyaji yaliyotiririka kutoka kwake.", "patron": "Ukiri uliotiwa muhuri kwa damu huko Kipro."},

"Hieromartyr Therapon, Bishop of Sardis":
{"type": "Shahidi · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Therapo, Askofu wa Sardi katika Lidia, aliteseka kwa ajili ya Kristo katika mateso ya karne ya tatu, na mateso yake yanapambwa na muujiza uliokigeuza chombo chenyewe cha mateso yake kuwa ishara ya uzima.", "patron": "Mti mkavu uliofanywa mbichi kwa damu ya shahidi."},

"Hieromartyr Timothy, Bishop of Prusa":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Timotheo, Askofu wa Prusa katika Bithinia, alikuwa mchungaji, mtenda-miujiza na shahidi aliyeteseka kwa ajili ya Kristo chini ya Yuliano Mwasi katika karne ya nne.", "patron": "Maaskofu na watenda-miujiza; wanaomwua joka kwa sala."},

"Hieromartyr Urban, Pope of Rome":
{"type": "Shahidi · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Urbano, Papa wa Roma, aliliongoza Kanisa la Roma katika miongo ya kwanza ya karne ya tatu, katika utawala wa mfalme Aleksanda Severo, mchungaji aliyekishika kiti cha Mtume Petro katika miaka ambayo kuwa Mkristo kulikuwa hatari.", "patron": "Kundi la Roma lililochungwa katika zama za damu."},

"Hieromartyr Vitalius, Bishop of Ravenna":
{"type": "Askofu · kiliturujia", "life": "Kuhani Shahidi Mtakatifu Vitalio anaheshimiwa miongoni mwa maaskofu wa mwanzo na mashahidi wa mji wa Ravenna, naye anaadhimishwa siku hii pamoja na Kuhani Shahidi Apolinari, askofu wa kwanza wa jimbo lile. Habari za kina za maisha yake hazikuhifadhiwa nyingi, lakini Kanisa linamkumbuka kama mchungaji aliyemkiri Kristo na akautia muhuri ushuhuda wake kwa shahada katika karne za mwanzo, naye anahesabiwa miongoni mwa wakuu watakatifu wa Kanisa waliopanda na kunywesha imani katika mji ule wa kale.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Hieromartyr Zeno, Bishop of Verona":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Mtakatifu Zeno, Askofu wa Verona, alitoka, mapokeo yashikavyo, Afrika, akiipeleka kaskazini ya Italia moto wa kanisa la Afrika lililokuwa limeipa magharibi ya Kilatini sauti zake kuu za kwanza; alipoinuliwa hadi jimbo la Verona karibu mwaka wa 362, aliuchunga mji katika mitikisiko ya mwisho ya upagani na katika kilele cha mahangaiko ya Kiariani, na silaha zake zilikuwa mbili, ubatizo na mahubiri.", "patron": "Maombezi yake huombwa kwa ajili ya wahubiri; wavuvi na wavua kwa ndoana."},

"Hieromartyr Zenobios and his sister Zenobia, of Aegæ in Cilicia":
{"type": "Askofu · karne ya 3", "life": "Kuhani Shahidi Mtakatifu Zenobio, Askofu wa Ege, na dada yake Zenobia waliteseka shahada katika Kilikia mwaka wa 285. Walipolelewa na wazazi Wakristo katika uchaji na usafi, waliwapa maskini utajiri waliourithi walipofikia umri; na Bwana alimlipa Zenobio kwa kipaji cha uponyaji, hata magonjwa yalikimbia kwa mguso wa mikono yake, naye alimrudisha miongoni mwa wengine mwanamke aliyekuwa akidhoofika kwa ugonjwa usiotibika wa titi, ndiyo maana wanaosumbuliwa na ugonjwa ule wanamwomba hadi leo.", "patron": "Maombezi yao huombwa kwa ajili ya madaktari; wanaosumbuliwa na magonjwa ya matiti."},

"Hieromartyrs Akepsimas, Bishop in Persia, Presbyter Joseph, and Deacon Aeithalas":
{"type": "Askofu · karne ya 4", "life": "Makuhani Mashahidi Watakatifu Akepsima Askofu, Yosefu Kasisi na Aeithala Shemasi waliliongoza Kanisa la Kikristo katika mji wa Kipersia wa Naeso, ambako kundi lilimpenda kwa moyo mkuu wao wa Kanisa kwa maisha yake ya ujinyimaji na kazi yake ya kichungaji isiyochoka. Katika mateso makuu chini ya Mfalme Shapuri wa Pili, askofu mzee, aliyekuwa na miaka themanini hivi, alikamatwa na watumishi wa mfalme waliokuwa wakiwawinda wakleri wa Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya wakleri wazee; uvumilivu katika kifungo kirefu."},

"Hieromartyrs John the Bishop and Jacob (James) the Presbyter, of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Makuhani Mashahidi Watakatifu Yohane Askofu na Yakobo Kasisi, aitwaye Mwenye Bidii, waliteseka katika Persia katika utawala wa Mfalme Shapuri wa Pili, mtesi mkuu wa Kanisa ng'ambo ya mpaka wa mashariki wa himaya. Wakiihubiri imani ya kweli kwa ujasiri, waliwavuta wengi wachaji Mungu kwa Kristo, na kukua kwa Kanisa kwa kazi zao kuliwaleta mbele ya mfalme.", "patron": "Maombezi yao huombwa kwa ajili ya Kanisa wakati wa mateso ya Waajemi."},

"Hieromartyrs Nicander, Bishop of Myra, and Hermas, the Presbyter":
{"type": "Mashahidi · karne ya 1", "life": "Makuhani Mashahidi Watakatifu Nikanda, Askofu wa Mira, na Herma Kasisi walikuwa wanafunzi wa Mtume Tito, mwenzake wa Paulo, na waliwekwa naye katika utumishi mtakatifu katika Likia. Wakiunganisha kazi ya kichungaji isiyokoma na maisha ya ujinyimaji, waliwageuza wapagani wengi kwa Kristo, na kwa ajili hiyo walisingiziwa na kuletwa mbele ya mtawala Libanio.", "patron": "Maombezi yao huombwa kwa ajili ya uvumilivu wa kichungaji."},

"Hieromartyrs Pionius and Limnus of Smyrna and those with them: Asclepiades, Macedonia, and Sabina":
{"type": "Kuhani Shahidi · karne ya 3", "life": "Makuhani Mashahidi Watakatifu Pionio na Limno, makasisi, na mashahidi Sabina, Makedonia na Asklepiade waliteseka huko Smirna katika mateso ya Desio, katika kanisa ambalo Mtume Yohane Mwanateolojia alilianzisha na damu ya Polikarpo ikalitukuza; na pambano la Pionio, lililohifadhiwa katika mojawapo ya kumbukumbu za kale za mashahidi zenye thamani kuliko zote, linaanza kwa jambo lisilo na kifani katika habari za mashahidi: alijua.", "patron": "Maombezi yao huombwa kwa ajili ya makasisi; watetezi wa imani."},

"Holy Apostles Stakhys, Apelles, Amplias, Urban, and Narcissus of the 70":
{"type": "Mtume wa Sabini · karne ya 1", "life": "Mitume Watakatifu Stakisi, Apele, Amplia, Urbano na Narkiso wa wale Sabini wanasalimiwa kwa majina katika Waraka wa Mtume Paulo kwa Warumi, na Kanisa linawaadhimisha pamoja siku hii pamoja na Mtume Aristobulo. Stakisi, ambaye Paulo anamwita mpendwa wake, aliwekwa na Mtume Andrea Aliyeitwa wa Kwanza kuwa askofu wa kwanza wa Bizanti, mji mdogo ambao siku moja ungekuwa Konstantinopoli, hata kiti cha enzi cha mapatriaki wa kiekumeni kinaufuatilia mfululizo wake hadi kwake.", "patron": "Maombezi yao huombwa kwa ajili ya maaskofu; kupanda makanisa ya mahali."},

"Holy Apostles of the Seventy and Deacons: Prochorus, Nicanor, Timon, and Parmenas":
{"type": "Shemasi · karne ya 1", "life": "Watakatifu Prokoro, Nikanori, Timoni na Parmena walikuwa miongoni mwa watu saba, waliojaa Roho Mtakatifu na hekima, ambao mitume kumi na wawili waliwachagua na kuwaweka kuwa mashemasi wa kwanza wa Kanisa, kama inavyosimuliwa katika Matendo ya Mitume, nao wanahesabiwa pia miongoni mwa wale Sabini.", "patron": "Maombezi yao huombwa kwa ajili ya mashemasi; utumishi wa ushemasi."},

"Holy Apostles of the Seventy: Sosthenes, Apollos, Cephas, Tychicus, Epaphroditus, Caesar, and Onesiphorus":
{"type": "Mitume wa Sabini · karne ya 1", "life": "Mitume Watakatifu wa wale Sabini Sosthene, Apolo, Kefa, Tikiko, Epafrodito, Kaisari na Onesiforo walikuwa wa kwaya ile ya pili ambayo Bwana mwenyewe aliituma wawili wawili mbele ya uso wake, na kazi zao zimefumwa katika nyaraka za Paulo. Sosthene alikuwa amekuwa mkuu wa sinagogi huko Korintho, naye alipigwa mbele ya kiti cha hukumu katika ghasia dhidi ya Paulo.", "patron": "Maombezi yao huombwa kwa ajili ya wahubiri; wachukua barua."},

"Holy Confessor Emilian, Bishop of Kyzikos":
{"type": "Askofu · karne ya 9", "life": "Mtakatifu Emiliano alikuwa Askofu wa Kizikos mwanzoni mwa karne ya tisa, katika wakati wa shambulio la pili juu ya ikoni takatifu chini ya mfalme mpiga-ikoni Leo Mwarmenia. Alipoitwa pamoja na maaskofu wengine mbele ya mfalme na kuamriwa alikataze kundi lake kuziheshimu sura takatifu, Mtakatifu Emiliano alijibu kwa ujasiri kwamba swali linalogusa imani ya Kanisa lapaswa kuchunguzwa na kuamuliwa ndani ya Kanisa na wachungaji wake wa kiroho, wala si kutatuliwa katika ikulu ya mfalme.", "patron": "Maombezi yake huombwa kwa ajili ya kuheshimu ikoni; uhuru wa Kanisa."},

"Holy Confessor Erasmus, Bishop of Formia in Campania":
{"type": "Askofu · karne ya 4", "life": "Mkiri Mtakatifu Erasmo, Askofu wa Formia katika Kampania, alianza Mashariki na akamalizia Magharibi, na kati ya ncha mbili za njia yake palilala jiografia yote ya mateso ya mwisho.", "patron": "Mateso yaliyoishiwa zaidi na ukiri kuhifadhiwa."},

"Holy Empress Markianḗ":
{"type": "Malkia · karne ya 6", "life": "Malkia Mtakatifu Markiane alikuwa mke wa mfalme Yustino wa Kwanza, aliyetawala Konstantinopoli tangu mwaka wa 518 hadi 527, mfalme askari wa asili ya wakulima ambaye nyumba yake Mungu aliiinua kutoka mashambani ya Balkani hadi kwenye zambarau; na Markiane, akishiriki kupanda kule kwa kushangaza, alizihifadhi ndani yake fadhila ambazo viti vya enzi huviyeyusha mara nyingi zaidi.", "patron": "Maombezi yake huombwa kwa ajili ya wanawake wa vyeo; wafadhili wa kike."},

"Holy Great Prince Vladimir (Basil in Baptism), Equal of the Apostles, and Enlightener of Rus'":
{"type": "Sawa na Mitume · karne ya 10", "life": "Mtakatifu Vladimiri, Mkuu Mkubwa wa Kyiv, alibatizwa kwa jina la Basili na akaleta Ukristo wa Kiorthodoksi katika Urusi. Baada ya kuzichunguza imani, alipokea ubatizo na akaamuru watu wa Kyiv wabatizwe katika Dnieper. Anakumbukwa kama mwangazaji wa Urusi, naye alipumzika mwaka wa 1015."},

"Holy Great-martyr Tsar Lazar (Vidovdan)":
{"type": "Mkuu · karne ya 14", "life": "Shahidi Mkuu Mtakatifu Lazari, Mkuu wa Serbia, aliwaongoza watu wake katika Vita vya Kosovo siku ambayo Waserbia wanaiita Vidovdan, na kwa kifo chake na chaguo lake akawa moyo wa imani na utambulisho wa taifa la Serbia.", "patron": "Watu na taifa la Serbia; wanaochagua ufalme wa mbinguni."},

"Holy King Askiot of Georgia":
{"type": "Mfalme na shahidi · karne ya 9", "life": "Mtakatifu Ashoti Kuropalate, Mfalme wa Georgia, alitawala katika karne ya tisa, katika kizazi ambacho nchi za Georgia zililala zikiwa zimeharibiwa na uvamizi wa Waarabu, naye akawa mtawala ambaye chini yake taifa lilianza kuinuka kutoka magofu yake. Akijiondoa kutoka Kartli iliyokaliwa na adui hadi nyanda za juu zenye miti za Tao-Klarjeti, Ashoti alikuwa wa kwanza wa ukoo wa Wabagrationi kubeba cheo kile.", "patron": "Maombezi yake huombwa kwa ajili ya watawala wanaojenga upya; wafadhili wa monasteri."},

"Holy Martyr Euthymius":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Euthimio aliteseka kwa ajili ya Kristo huko Nikomedia katika mateso makuu chini ya Diokletiano na Maksimiano, ambamo Wakristo wa mji ule waliangamia kwa idadi kubwa. Miili ya mashahidi watakatifu ilipolala bila kuzikwa, Euthimio, pamoja na bikira Domna aliyekuwa amegeuka kutoka upagani wake wa awali kwa Kristo, waliwahurumia wafu na wakajitoa kwa kazi ya uchaji ya kuwazika waamini walioanguka kwa heshima.", "patron": "Maombezi yao huombwa kwa ajili ya kuwahudumia wafu; ukiri thabiti."},

"Holy Martyr and Confessor Michael and his councilor, Theodore, Wonderworkers of Chernihiv":
{"type": "Mkuu · karne ya 13", "life": "Shahidi na Mkiri Mtakatifu Mikaeli, Mkuu wa Chernihiv, na mshauri wake mwaminifu bwana Theodoro waliteseka katika Horde ya Dhahabu mwaka wa 1246. Mkuu Mikaeli, aliyejulikana tangu utoto kwa uchaji na upole, alikuwa ametawala Novgorod na Kyiv katika miaka ya dhoruba ya Wamongolia; na alipoitwa kwenye Horde ili apokee kutoka kwa Batu haki ya utawala wake, wapagani walidai kwanza apite kati ya moto na aziinamie sanamu zao, kama desturi yao ilivyokuwa.", "patron": "Maombezi yao huombwa kwa ajili ya watawala; washauri."},

"Holy Martyrs and Confessors Gurias, Samonas, and Habibus, of Edessa":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi na Wakiri Watakatifu Guria, Samona na Habibu ni walinzi wakuu wa mji wa Edesa na wa ndoa yenye heshima. Guria na Samona, wahubiri wa neno la Mungu, walikamatwa katika mateso chini ya Diokletiano; walipokataa kutoa dhabihu, walipigwa, wakatundikwa kwa mikono yao wakiwa na mizigo mizito iliyofungwa miguuni mwao, na wakatupwa katika gereza lisilo na hewa, na baada ya mateso marefu walikatwa vichwa, karibu mwaka wa 306, Samona akisali kwa maneno ambayo shahidi mmoja aliyaandika kwa ajili ya Kanisa.", "patron": "Maombezi yao huombwa kwa ajili ya ndoa yenye heshima; ukombozi kutoka machafuko ya familia."},

"Holy Prophet Zachariah and Righteous Elizabeth, parents of Saint John the Baptist":
{"type": "Nabii · karne ya 1", "life": "Nabii Mtakatifu Zakaria na Mwenye haki Elisabeti walikuwa wazazi wa Mtakatifu Yohane, Mtangulizi na Mbatizaji wa Bwana. Wote wawili walikuwa wa ukoo wa Haruni, Zakaria akihudumu kama kuhani katika Hekalu la Yerusalemu na Elisabeti akiwa jamaa wa Mzazi-Mungu Mtakatifu Zaidi; na kama Injili ishuhudiavyo, walienenda bila lawama katika amri zote za Bwana, lakini walikuwa wamezeeka bila watoto.", "patron": "Maombezi yao huombwa kwa ajili ya makasisi; wanandoa wasio na watoto."},

"Holy Prophet and God-seer Moses":
{"type": "Nabii · karne ya 16 KK", "life": "Nabii Mtakatifu na Mwonaji wa Mungu Musa, mtunga sheria mkuu wa Israeli, alikuwa wa kabila la Lawi, na maisha yake yameandikwa katika vitabu vya Kutoka hadi Kumbukumbu la Torati. Alizaliwa Misri wakati Farao alipoamuru kila mtoto wa kiume wa Waebrania auawe, akafichwa na mama yake katika kikapu miongoni mwa matete ya Nile, ambako binti wa Farao alimpata na akamlea kama mwanawe mwenyewe katika hekima yote ya Wamisri.", "patron": "Maombezi yake huombwa kwa ajili ya watunga sheria; manabii."},

"Holy Righteous David the King":
{"type": "Mfalme na nabii · karne ya 10 KK", "life": "Nabii na Mfalme Mtakatifu Daudi, mwimbaji mtamu wa Israeli, alikuwa mwana mdogo kuliko wote wa Yese wa Bethlehemu, mvulana mchungaji aliyeletwa kutoka kundini ili apakwe mafuta na Samweli huku ndugu zake warefu wakipitwa, kwa maana Bwana huutazama moyo. Ujana wake ni utenzi wa Israeli: kinubi kilichotuliza giza la Sauli.", "patron": "Maombezi yake huombwa kwa ajili ya wafalme; waimbaji."},

"Holy Righteous Joseph the Betrothed":
{"type": "Mwenye haki · karne ya 1", "life": "Mwenye haki Mtakatifu Yosefu Mchumba, wa ukoo wa kifalme wa Daudi, alikuwa seremala wa Nazareti, mjane mzee mwenye wana na binti, miongoni mwao Yakobo, Yose, Simoni na Yuda, ambao Injili zinawaita ndugu za Bwana; na kwake, kama kwa mlinzi aliyethibitishwa, makuhani wa Hekalu walimchumbisha Bikira Maria miaka yake ya kukaa patakatifu ilipotimia, uchumba uliokuwa ulinzi, mwenye haki akipokea hazina ya Israeli ili aililinde nadhiri yake.", "patron": "Maombezi yake huombwa kwa ajili ya maseremala; walezi."},

"Holy Unmercenary Physician Diomedes":
{"type": "Tabibu · karne ya 3", "life": "Mtakatifu Diomede alizaliwa Tarso katika Kilikia na akafundishwa sanaa ya utabibu, lakini elimu yake haikumjaza kiburi, kwa maana aliushika uchaji ambamo wazazi wake walikuwa wamemlea. Katika kumwiga Kristo, Tabibu wa roho na miili, aliitumia sanaa yake ya uponyaji bure na bila malipo, na alipowahudumia wagonjwa mwilini aliwatunza pia rohoni, akiwahubiria Injili ya wokovu na akiwaleta wengi katika imani ya Mwokozi.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; wagonjwa."},

"Holy Virgin Martyr Theodosίa of Tyre":
{"type": "Bikira Shahidi · karne ya 4", "life": "Bikira Shahidi Mtakatifu Theodosia wa Tiro alikuwa mwanamwali ambaye alikuwa bado hajafikia miaka kumi na minane, na shahada yake, iliyoandikwa na Eusebio aliyeishi katika siku zile huko Kaisaria, ilianza kwa tendo la heshima. Kikundi cha wakiri kilikuwa kimeketi kwa minyororo mbele ya mahakama ya mtawala huko Kaisaria, wakingoja hukumu.", "patron": "Maombezi yake huombwa kwa ajili ya vijana; wanaowaheshimu wakiri."},

"Holy Woman Olympias (Olympiada) the Deaconess of Constantinople":
{"type": "Shemasi wa kike · karne ya 5", "life": "Mtakatifu Olimpia alizaliwa Konstantinopoli katika familia mashuhuri ya useneta na akaachwa katika ujana wake mrithi tajiri. Alipochumbiwa na mkuu mtukufu aliyekufa kabla ndoa yao haijakamilika, alijihesabu kuwa mjane na, ingawa mfalme na jamaa zake walimsihi aolewe tena, alikataa, akichagua badala yake kujiweka wakfu kwa Mungu kabisa.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi wa kike; kutoa sadaka."},

"Holy Wonderworkers and Unmercenaries Cosmas and Damian of Mesopotamia":
{"type": "Wasiopokea-Malipo · karne ya 3", "life": "Watenda-Miujiza na Wasiopokea-Malipo Watakatifu Kosma na Damiano wa Asia, wa kwanza wa jozi tatu za ndugu watakatifu wasiopokea malipo wa majina haya, walizaliwa katika Asia Ndogo kwa baba mpagani aliyekufa walipokuwa wadogo, na kwa Theodota mtakatifu, aliyewalea katika uchaji na katika kusoma vitabu vya Kimungu.", "patron": "Maombezi yao huombwa kwa ajili ya madaktari; wapasuaji."},

"Holy Wonderworkers and Unmercenaries Cyrus and John, and those with them":
{"type": "Wasiopokea-Malipo, mashahidi · karne ya 4", "life": "Watenda-Miujiza na Wasiopokea-Malipo Watakatifu Kiro na Yohane waliteseka huko Kanopo katika Misri mwaka wa 311, na Kanisa linawaweka kando ya Kosma na Damiano miongoni mwa matabibu wasiokubali kuchukua malipo. Kiro alikuwa daktari wa Aleksandria, maarufu katika Misri yote kwa utabibu uliponya mara mbili, kwa maana aliutibu mwili bila malipo na akatumia kitanda cha mgonjwa kuitibu roho, akiwaambia wagonjwa wake kwamba ugonjwa mara nyingi hufuata dhambi na akiwaongoza kwa Tabibu wa wote.", "patron": "Maombezi yao huombwa kwa ajili ya madaktari; wauguzi."},

"Holy Wonderworking Unmercenary Physicians Cosmas and Damian at Rome":
{"type": "Matabibu · karne ya 3", "life": "Mashahidi na Matabibu Wasiopokea-Malipo Watakatifu Kosma na Damiano wa Roma walikuwa ndugu, waliozaliwa Roma na kufundishwa kuwa matabibu, waliopokea kutoka kwa Mungu kipawa cha uponyaji. Wasipochukua malipo yoyote kwa uangalizi wao wa wagonjwa, ndiyo maana wanaitwa wasiopokea-malipo, waliwatibu wote waliokuja kwa jina la Kristo na wakawavuta wengi kwenye imani.", "patron": "Maombezi yao huombwa kwa ajili ya madaktari; wapasuaji."},

"Holy and Righteous Ancestors of God, Joachim and Anna":
{"type": "Wenye haki · karne ya 1", "life": "Siku inayofuata Kuzaliwa kwa Mzazi-Mungu Kanisa linaadhimisha Sinaksi ya Wazazi Wenye haki Watakatifu wa Mungu, Yoakimu na Ana, likikusanyika kuwaheshimu wale ambao kupitia kwao Mzazi-Mungu alitolewa kwa ulimwengu. Yoakimu alikuwa wa ukoo wa kifalme wa Daudi na Ana wa ukoo wa kikuhani wa Haruni, nao waliishi katika haki, wakimpa Mungu theluthi ya mapato yao na theluthi kwa maskini.", "patron": "Maombezi yao huombwa kwa ajili ya wanandoa wasio na watoto; babu na bibi."},

"Holy, All-Praised Apostle Philip":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Mwenye Sifa Zote Filipo, mmoja wa wale Kumi na Wawili, alikuwa wa Bethsaida katika Galilaya, mji wa Andrea na Petro, na alikuwa mstadi tangu ujana katika Maandiko; na Bwana alipomkuta na kusema, Nifuate, Filipo mara moja alimtafuta Nathanaeli na akayajibu mashaka yake kwa maneno yaliyobaki kuwa njia yote ya Injili: Njoo uone.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kumpata Kristo."},

"Holy, Glorious Apostle Thomas":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu na Mtukufu Thoma, aitwaye Pacha, alikuwa mvuvi Mgalilaya aliyeitwa na Bwana katika kikundi cha wale Kumi na Wawili, na Injili inaonyesha moyo wake wenye moto, kwa maana Bwana alipokwenda Yudea kumfufua Lazaro, ni Thoma aliyesema, Twendeni sisi nasi, tufe pamoja naye.", "patron": "Maombezi yake huombwa kwa ajili ya wajenzi; wasanifu majengo."},

"Holy, Glorious Demetrios the Myrrh-gusher of Thessaloniki":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Dimitri wa Thesalonike, aitwaye Mtiririsha-Manukato, alikuwa Mkristo mtukufu wa mji ule na ofisa chini ya mfalme Maksimiano. Aliifundisha imani waziwazi na akawaimarisha Wakristo licha ya mateso. Alipofungwa gerezani na mfalme, alimbariki Nestori aende kupambana na shujaa mpagani Lieo. Dimitri alichomwa kwa mikuki gerezani na akapokea taji la shahidi karibu mwaka wa 306.", "patron": "Katika mapokeo ya Kislavi anahusishwa hasa na ushujaa wa kijeshi na utetezi wa nchi ya kwao."},

"Holy, Glorious Prophet Elijah":
{"type": "Nabii · karne ya 9 KK", "life": "Nabii Mtakatifu Eliya aliishi katika ufalme wa Israeli wakati wa utawala wa Ahabu. Akiwa na bidii kwa Bwana, aliukemea uabudu sanamu, akaiita Israeli kwenye toba, na akatenda maajabu kwa nguvu za Mungu. Maandiko yanasema kwamba alitwaliwa juu mbinguni katika gari la moto badala ya kufa kwa namna ya kawaida."},

"Holy, Righteous Anna the Prophetess":
{"type": "Nabii wa kike · karne ya 1", "life": "Mwenye haki Mtakatifu Ana Nabii wa kike anasimama kando ya Simeoni katika Kukutana kwa Bwana, shahidi wa pili mzee ambaye Mungu alimweka Hekaluni kwa ajili ya siku ya arobaini; na Mwinjilisti Luka, ambaye peke yake anamwandika, anampa utambulisho kamili na wa uangalifu, kama vile anayeandika ushuhuda: Ana, nabii wa kike, binti wa Fanueli, wa kabila la Asheri.", "patron": "Maombezi yake huombwa kwa ajili ya wajane; wazee."},

"Holy, Righteous Simeon the God-Receiver":
{"type": "Mwenye haki · karne ya 1", "life": "Mwenye haki Mtakatifu Simeoni Mpokea-Mungu ni mzee wa Kukutana, mtu aliyewekwa na Mungu kusimama katika mpaka wa Maagano mawili na kulipokea la pili mikononi mwake; Injili ya Luka inamweleza kikamilifu kwa mistari mitatu - mwenye haki na mcha Mungu, akiitazamia faraja ya Israeli, na Roho Mtakatifu alikuwa juu yake - nayo inaandika ahadi iliyoyapanga maisha yake marefu, kwamba alikuwa amefunuliwa na Roho Mtakatifu kwamba hataona mauti kabla hajamwona Kristo wa Bwana.", "patron": "Maombezi yake huombwa kwa ajili ya wazee; watafsiri."},

"Icon of Sophia, the Wisdom of God (Novgorod)":
{"type": "Ikoni · karne ya 15", "life": "Ikoni ya Sofia, Hekima ya Mungu, ya namna ya Novgorod ilitokea kwanza katika mji ule katika karne ya kumi na tano, ingawa kanisa la kwanza katika Urusi lililowekwa wakfu kwa Hekima Takatifu lilikuwa limeinuliwa Novgorod katika karne ya kumi. Katikati ya sura Hekima ya Mungu inaonyeshwa kama Malaika mwenye mabawa na wa moto, aliyeketi juu ya kiti cha enzi cha dhahabu kilichobebwa na nguzo saba, kulingana na maneno ya Mithali kwamba Hekima amejenga nyumba yake na amechonga nguzo zake saba.", "patron": "Huombwa kwa ajili ya hekima ya kimungu; wagonjwa."},

"Icon of the Mother of God of Armatia":
{"type": "Ikoni · kiliturujia", "life": "Ikoni ya Armatia ya Mzazi-Mungu iliheshimiwa huko Konstantinopoli katika monasteri ya Armatia, iliyochukua jina lake kutoka mahali paitwapo Armation, panapohusishwa na mkuu Armatio katika siku za mfalme Zeno. Maadhimisho ya ikoni hii itendayo miujiza yaliwekwa kwa shukrani kwa ajili ya ukombozi wa Kanisa kutoka uzushi wa kupiga ikoni, uliokuwa umezipiga vita sura takatifu hadi Kanisa, likiongozwa na Mtaguso Mkuu wa Saba, lilipoirudisha heshima yao kulingana na Maandiko na Mapokeo.", "patron": "Huombwa kwa ajili ya kuheshimu ikoni takatifu."},

"Icon of the Mother of God of Kasperov":
{"type": "Ikoni · karne ya 19", "life": "Siku hii Kanisa linaadhimisha Ikoni ya Kasperov itendayo miujiza ya Mzazi-Mungu Mtakatifu Zaidi, sura iliyotukuzwa katika nchi za kusini za Urusi kwa kufanywa upya kwake na kwa ukombozi wa mji mkubwa.", "patron": "Wanaosali mbele ya ikoni zilizosahauliwa; watetezi wa miji."},

"Icon of the Mother of God of Kholm":
{"type": "Ikoni · kiliturujia", "life": "Ikoni ya Kholm ya Mzazi-Mungu ni mojawapo ya ikoni za kale na zinazoheshimiwa kuliko zote za nchi za magharibi za Urusi, na mapokeo ya uchaji yanaipatia kuchorwa kwake Mwinjilisti mtakatifu Luka na yanashika kwamba ililetwa kutoka Bizanti katika siku za Mtakatifu Vladimiri, wakati nchi ya Urusi ilipopokea ubatizo mtakatifu.", "patron": "Huombwa kwa ajili ya ulinzi; uponyaji."},

"Icon of the Mother of God of Kyiv-Bratsk":
{"type": "Ikoni · karne ya 17", "life": "Siku hii Kanisa linaadhimisha Ikoni itendayo miujiza ya Mzazi-Mungu Mtakatifu Zaidi iitwayo ya Kyiv-Bratsk, ikoni ya monasteri ya Udugu wa Kyiv, au Bratsky, katika Podil, mtaa wa Kyiv kando ya Dnieper.", "patron": "Udugu wa Kyiv na shule yake; wanaokimbilia kwa Mzazi-Mungu."},

"Icon of the Mother of God of Lubyatov":
{"type": "Ikoni ya Mzazi-Mungu · karne ya 16", "life": "Ikoni ya Lubyatov ya Mzazi-Mungu, sura ya Upole, ilitunzwa katika monasteri ya Mtakatifu Nikolao huko Lubyatov nje kidogo ya Pskov, na sikukuu yake inahifadhi kumbukumbu ya usiku mmoja ambao, mapokeo ya nchi ya Pskov yashikavyo, Mzazi-Mungu aliuepusha uharibifu wa mji.", "patron": "Huombwa kwa ajili ya miji iliyo chini ya ghadhabu; waombezi kwa ajili ya waliohukumiwa."},

"Icon of the Mother of God of Mount Athos, “Sweet Kissing”":
{"type": "Ikoni ya Mzazi-Mungu · karne ya 9", "life": "Ikoni ya Mzazi-Mungu iitwayo Busu Tamu, Glikofilusa, ni mojawapo ya hazina za monasteri ya Filotheou juu ya Mlima Athos, nayo inaonyesha Mama na Mtoto katika utimilifu wa Upole, shavu likikandamizwa kwenye shavu, upendo wa pande zote wa Bikira na Mungu wake ukifanywa kuwa somo lote la sura ile.", "patron": "Huombwa kwa ajili ya wanaopaswa kuacha wanachokipenda ili kukiokoa; mahujaji."},

"Icon of the Mother of God of Mt. Athos, “Sweet Kissing”":
{"type": "Sikukuu · karne ya 9", "life": "Siku hii Kanisa linaadhimisha ikoni itendayo miujiza ya Mzazi-Mungu Mtakatifu Zaidi iitwayo Glikofilusa, Busu Tamu, mojawapo ya hazina za monasteri ya Filotheou juu ya Mlima Athos na mojawapo ya sura zake za upole kuliko zote.", "patron": "Ikoni iliyookolewa kutoka wapiga-ikoni kwa njia ya bahari."},

"Icon of the Mother of God of Pochaiv":
{"type": "Ikoni · karne ya 16", "life": "Ikoni ya Pochaiv ya Mzazi-Mungu ni mojawapo ya hazina kuu kuliko zote za ulimwengu wa Kiorthodoksi, iliyowekwa mahali pa taadhima kwa zaidi ya karne nne katika Lavra ya Pochaiv katika Volhynia. Ikoni ililetwa kutoka Konstantinopoli mwaka wa 1559 na Metropolita Neofito, ambaye, alipopokelewa katika nyumba ya mwanamke mtukufu mchaji Mungu Ana Goyska, alimbariki kwa ikoni ile kwa shukrani.", "patron": "Huombwa kwa ajili ya ulinzi; uponyaji."},

"Icon of the Mother of God of Rzhevsk":
{"type": "Ikoni · karne ya 16", "life": "Ikoni ya Rzhev ya Mzazi-Mungu, iitwayo pia Okovetskaya, ilitokea mwaka wa 1539 katika msitu karibu na mji wa Rzhev, ambako msalaba utendao miujiza na ikoni ya Mzazi-Mungu pamoja na Mtakatifu Nikolao viligunduliwa juu ya mti. Uponyaji mwingi ulitolewa kwa waliokuja kwa imani, na habari za maajabu zilienea, hata sura takatifu zilipelekwa kwa muda Moscow na kuheshimiwa kwa taadhima kabla ya kurudishwa mahali pa kutokea kwao.", "patron": "Huombwa kwa ajili ya uponyaji."},

"Icon of the Mother of God of Volokolamsk":
{"type": "Ikoni ya Mzazi-Mungu · karne ya 16", "life": "Ikoni ya Volokolamsk ya Mzazi-Mungu ni nakala itendayo miujiza ya sura kubwa ya Vladimir, ikoni ipendwayo kuliko zote ya nchi ya Urusi, na sikukuu yake inaadhimisha siku ya mwaka wa 1572 wakati ilipoletwa kwa taadhima katika monasteri ya Yosefu-Volokolamsk, nyumba maarufu ya Mtakatifu Yosefu wa Volotsk, na kupokelewa kwa heshima yote malangoni mwake, ikilakiwa na ndugu katika maandamano na kuwekwa katika kanisa kuu la Kulala la monasteri.", "patron": "Huombwa kwa ajili ya monasteri; mahujaji."},

"Icon of the Mother of God “The Unbreakable Wall”":
{"type": "Ikoni · karne ya 11", "life": "Siku hii Kanisa linaadhimisha Ikoni ya kale na inayoheshimiwa ya Mzazi-Mungu Mtakatifu Zaidi iitwayo Ukuta Usiovunjika, sura kubwa ya musaiki ya Mzazi-Mungu inayosimama katika tao la madhabahu la Kanisa Kuu la Hekima Takatifu huko Kyiv.", "patron": "Wanaokimbilia kwa Mzazi-Mungu; watetezi wa miji na makanisa."},

"Icon of the Mother of God “of the Passion”":
{"type": "Ikoni · karne ya 17", "life": "Siku hii Kanisa linaadhimisha Ikoni itendayo miujiza ya Mzazi-Mungu Mtakatifu Zaidi iitwayo ya Mateso, sura ambayo mpangilio wake wenyewe ni tafakari juu ya mateso ya Kristo yaliyojulikana mbele.", "patron": "Wanaokimbilia kwa Mzazi-Mungu kutoka mateso; waoga na wenye huzuni."},

"Icon of the Mother of God “of the Sign”, the “Kursk-Root”":
{"type": "Ikoni · karne ya 13", "life": "Ikoni ya Kursk-Mzizi ya Mzazi-Mungu wa Ishara ni mojawapo ya ikoni zitendazo miujiza zinazoheshimiwa kuliko zote za nchi ya Urusi. Ilipatikana tarehe nane ya Septemba mwaka wa 1295, wakati mwindaji katika msitu kando ya mto Tuskar, karibu na mji wa Kursk ambao Watatari walikuwa wameuharibu, alipoiona ikoni ikiwa imelala kifudifudi kwenye mzizi wa mti.", "patron": "Huombwa kwa ajili ya ulinzi; Warusi walio ugenini."},

"Icon of the Mother of God “the Joy of All who Sorrow” (with coins) in St. Petersburg":
{"type": "Ikoni · karne ya 19", "life": "Ikoni hii itendayo miujiza ya Mzazi-Mungu, iitwayo Furaha ya Wote Wenye Huzuni yenye sarafu, ilitukuzwa huko Saint Petersburg mwaka wa 1888. Katika dhoruba kali ya radi, umeme ulipiga kanisa dogo kando ya Neva, na ingawa moto uliunguza na kutia weusi vyote vilivyokuwa ndani, ikoni ya Malkia wa Mbinguni iliachwa bila kudhurika na hata ilionekana imefanywa upya na kung'arishwa.", "patron": "Huombwa kwa ajili ya faraja katika huzuni; uponyaji."},

"Icon of the Mother of God “the Surety of Sinners”":
{"type": "Sikukuu · karne ya 19", "life": "Siku hii Kanisa linaadhimisha Ikoni itendayo miujiza ya Mzazi-Mungu Mtakatifu Zaidi iitwayo Mdhamini wa Wenye Dhambi, ambaye jina lake lenyewe ni teolojia na faraja, kwa maana sura inabeba maandishi ambayo kwayo Mzazi-Mungu anajitangaza kuwa dhamana na mdhamini.", "patron": "Mzazi-Mungu aliyewekwa dhamana kwa wenye dhambi."},

"Inexhastible Chalice Icon of the Mother of God":
{"type": "Sikukuu · karne ya 19", "life": "Siku hii Kanisa linaadhimisha Ikoni ya Kikombe Kisichoisha ya Mzazi-Mungu Mtakatifu Zaidi, iliyotukuzwa huko Serpukhov mwaka wa 1878 na kutolewa na Mungu kwa unyofu ambao zama zile zilikuhitaji.", "patron": "Kikombe kisichokauka."},
}
