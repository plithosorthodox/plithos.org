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
}
