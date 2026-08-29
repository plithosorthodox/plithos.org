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
{"type": "Abate, Shahidi · karne ya 16", "life": "Mheshimiwa Korniliy, Abate wa Mapango ya Pskov na Kuhani Shahidi, alizaliwa Pskov mwaka wa 1501 kwa Stefano na Maria watukufu, na alifundwa katika monasteri ya Mirozh katika utamaduni wote wa utawa wa kaskazini, akitengeneza mishumaa, akipasua kuni, akinakili na kupamba vitabu, na akichora ikoni; na karani Misiur Munekhin alipompeleka kijana yule katika monasteri maskini ndogo ya Mapango msituni, uzuri wa mahali pale na taadhima ya kanisa la pangoni viliyaamua maisha yake, kwa maana Korniliy alinyolewa utawa huko wala hakuondoka tena.", "patron": "Maombezi yake huombwa kwa ajili ya maabate; watunga habari."},

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
{"type": "Abate, Shahidi Mtawa · karne ya 16", "life": "Siku hii Kanisa linaadhimisha kufukuliwa kwa masalia ya Mheshimiwa Adriano wa Poshekhonsk, Shahidi Mtawa, kulikotokea tarehe kumi na tisa ya Novemba mwaka wa 1625. Mtakatifu Adriano, mtawa na mchora ikoni mwenye kipaji aliyefundwa katika utamaduni wa monasteri kubwa za kaskazini, alikuwa ameanzisha pamoja na mjinyimaji mwenzake monasteri ya Kulala kwa Mzazi-Mungu Mtakatifu Zaidi katika misitu ya Poshekhonye katika nchi za Yaroslavl, akijitaabisha huko katika kufunga, sala na kuchora ikoni takatifu, na akikusanya jumuiya kulizunguka kanisa la nyikani.", "patron": "Maombezi yake huombwa kwa ajili ya wachora ikoni; watawa."},

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
{"type": "Abate, Mkiri Shahidi · karne ya 9", "life": "Mheshimiwa Theokteristo, aitwaye pia Theosterikto, Mkiri Shahidi na Abate wa monasteri ya Pelekete karibu na Prusa, alisimama katikati ya mojawapo ya matendo mabaya kuliko yote ya mateso ya wapinga-ikoni na akalipa Kanisa, kutoka giza lile, mojawapo ya sala zake zipendwazo kuliko zote. Alizaliwa Triglia katika Bithinia, na akawa mtawa katika ujana wake katika monasteri ya Mtakatifu Yohane.", "patron": "Maombezi yake huombwa kwa ajili ya maabate; watunga nyimbo takatifu."},

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
{"type": "Kuhani Shahidi, Mkiri · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Theodoto, Askofu wa Kirenia katika Kipro, alikuwa mzaliwa wa Galatia katika Asia Ndogo aliyekuja kulichunga jimbo lile la Kipro katika majira ya mwisho na mabaya kuliko yote ya mateso, wakati Likinio, akivunja urafiki na mwenzake Konstantino, alipoyafanya upya Mashariki mahangaiko ambayo Amri ya Milano ilipaswa kuwa imeyakomesha.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu walio chini ya mateso; wanaoishi zaidi ya watesi wao."},

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

"Kazan Icons of the Mother of God in Kazan, St. Petersburg, and Moscow":
{"type": "Ikoni · karne ya 16", "life": "Sikukuu hii inaadhimisha kutokea kwa Ikoni ya Kazan ya Mzazi-Mungu, iliyofunuliwa kwa muujiza katika mji wa Kazan mwaka wa 1579, wakati Mzazi-Mungu alipomwelekeza msichana mdogo katika maono mahali ambapo ikoni ilikuwa imefichwa katika majivu ya nyumba iliyoteketea.", "patron": "Huombwa kwa ajili ya ulinzi wa Urusi; ndoa na familia."},

"Leavetaking of the Annunciation":
{"type": "Sikukuu · karne ya 1", "life": "Siku hii Kanisa linaadhimisha kuagwa kwa Bishara, apodosi ya sikukuu ya mwanzo wa sikukuu zote, likiimba tena na kwa mara ya mwisho mwaka huu nyimbo za ujumbe wa Gabrieli kabla ya kuzikunja na kurudi katika Mfungo.", "patron": "Huombwa kwa ajili ya wote walioadhimisha sikukuu; siri iliyotiwa muhuri katika roho."},

"Leavetaking of the Dormition of the Mother of God":
{"type": "Kufunga sikukuu · kiliturujia", "life": "Hii ni Kuagwa kwa Sikukuu ya Kulala kwa Mzazi-Mungu Mtakatifu Zaidi, siku ya mwisho ambayo Kanisa linaadhimisha kulala kwake kwa heri na kuhamishwa kwake katika utukufu hadi mbinguni kabla ya kuileta sikukuu kwenye mwisho wake. Siku hii ibada ya sikukuu inaimbwa tena, ili waamini waage sikukuu wakiwa wamejazwa upya kwa furaha na faraja yake.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Leavetaking of the Elevation of the Cross":
{"type": "Kufunga sikukuu · kiliturujia", "life": "Hii ni Kuagwa kwa Sikukuu ya Kuinuliwa kwa Ulimwengu Wote kwa Msalaba wenye Thamani na Utoao Uzima, siku ya mwisho ya kipindi cha sikukuu ya Msalaba. Nyimbo za Kuinuliwa zinaimbwa tena katika ukamilifu wake, na waamini, wakiwa wameiadhimisha sikukuu katika siku zake za baada ya sikukuu, wanaiaga sherehe, wakiuheshimu Mti mtakatifu mara ya mwisho kabla haujarudishwa patakatifu.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Leavetaking of the Entry of the Most Holy Theotokos Into the Temple":
{"type": "Kufunga sikukuu · kiliturujia", "life": "Siku hii Kanisa linaadhimisha kuagwa, apodosi, ya sikukuu ya Kuingia kwa Mzazi-Mungu Mtakatifu Zaidi Hekaluni, likikusanya katika maadhimisho ya mwisho neema ya siku za sikukuu. Tena ibada zinarudi kwenye nyimbo za sikukuu, na Kanisa linamwona mtoto wa miaka mitatu akiongozwa juu ya ngazi za patakatifu, akipokelewa na Zekaria, na kuingizwa katika Patakatifu pa Patakatifu, hekalu safi la Mwokozi likiingia hekalu la kivuli, ili kivuli kiipishe kweli.", "patron": "Huombwa kwa ajili ya kutia muhuri sikukuu moyoni."},

"Leavetaking of the Nativity of our Lord":
{"type": "Kufunga sikukuu · kiliturujia", "life": "Kuagwa kwa Kuzaliwa kwa Bwana wetu, Apodosi, kunaadhimishwa tarehe thelathini na moja ya Desemba, na katika kwako Kanisa linaiimba sikukuu tena karibu katika utimilifu wake wote wa sikukuu, nyimbo na kanoni ya Bethlehemu zikirudi kwa nguvu kama katika sikukuu yenyewe, hata majira yanaisha si kwa kufifia bali kwa mwako wa mwisho, mlango wa sikukuu ukifungwa kutoka ndani kwa kuimba.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Leavetaking of the Nativity of the Mother of God":
{"type": "Kufunga sikukuu · kiliturujia", "life": "Hii ni Kuagwa kwa Sikukuu ya Kuzaliwa kwa Mzazi-Mungu Mtakatifu Zaidi, siku ya mwisho ya kipindi cha sikukuu ambamo Kanisa linaadhimisha kuzaliwa kwa Mzazi-Mungu. Siku hii nyimbo na masomo ya sikukuu yanaimbwa tena katika ukamilifu wake, na waamini wanaiaga sherehe, wakiwa wamejazwa furaha yake.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Leavetaking of the Transfiguration of our Lord":
{"type": "Kufunga sikukuu · kiliturujia", "life": "Hii ni Kuagwa kwa Sikukuu ya Kugeuka Sura kwa Bwana, siku ya mwisho ambayo Kanisa linaadhimisha utukufu uliofunuliwa juu ya mlima mtakatifu kabla ya kuileta sikukuu kwenye mwisho wake. Siku hii karibu ibada yote ya sikukuu inaimbwa tena, ili waamini waage sikukuu kuu wakiwa wamejazwa upya nuru ya Tabori.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Martyr Aboudimos of the Isle of Tenedos":
{"type": "Mlei · karne ya 4", "life": "Shahidi Mtakatifu Abudimo alikuwa wa kisiwa cha Tenedo, kilicho katika Aegea mkabala na mji wa kale wa Troya, naye alikuwa miongoni mwa wa kwanza kuteseka kwa ajili ya Kristo katika mateso chini ya Diokletiano mwanzoni mwa karne ya nne. Alipoamriwa aziabudu sanamu na kula chakula kilichotolewa kwazo, alikataa kwa uthabiti, na kwa ajili hiyo alifungwa na kupigwa kikatili, akivumilia mateso yake kwa ujasiri hadi alipopokea taji la shahada.", "patron": "Maombezi yake huombwa kwa ajili ya uthabiti."},

"Martyr Abraham of Bulgaria":
{"type": "Shahidi · karne ya 13", "life": "Shahidi Mtakatifu Abrahamu wa Bulgaria, Mtenda-Miujiza wa Vladimir, alikuwa mwana wa Wabulgari wa Volga, aliyezaliwa miongoni mwa Waislamu wa nchi ya Kama na Volga na kulelewa katika imani yao, mfanyabiashara tajiri aliyejulikana hata kabla ya kuongoka kwake kwa wema kwa maskini na wahitaji uliotangulia dini yake.", "patron": "Maombezi yake huombwa kwa ajili ya wafanyabiashara; walioongoka kutoka Uislamu."},

"Martyr Acacius the Centurion at Byzantium":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Akakio Akida aliteseka huko Bizanti mwaka wa 303, katika ghadhabu ya kwanza ya mateso ya Diokletiano, na kumbukumbu yake baadaye ikawa ya kitambaa chenyewe cha mji ambao ungekuwa Konstantinopoli.", "patron": "Shukrani iliyotolewa kwenye kigogo cha kuuawa."},

"Martyr Agathocleia":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Agathoklea alikuwa mtumishi wa mtu fulani Nikolao na mkewe Paulina; na ingawa bwana alikuwa Mkristo, bibi alikuwa mwabudu sanamu aliyeikasirikia imani ya mtumwa wake. Kwa miaka mingi Agathoklea alivumilia kutoka kwake kazi ngumu na za kikatili, kipigo, na kila namna ya mateso yaliyobuniwa ili kumlazimisha amkane Kristo na kutoa dhabihu kwa sanamu, akiyabeba yote kwa uvumilivu wa mashahidi huku akibaki bila kutikisika katika ukiri wake.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi; wanaoonewa."},

"Martyr Agathonicus of Nicomedia, and those with him, who suffered under Maximian":
{"type": "Mashahidi · karne ya 4", "life": "Shahidi Mtakatifu Agathoniko, pamoja na Zotiko, Theoprepio, Akindino, Severiano, Zeno na wengine, waliteseka kwa ajili ya Kristo katika mateso chini ya Maksimiano. Agathoniko alikuwa wa familia tukufu na alikaa Nikomedia, na kwa kuwa alikuwa mstadi katika Maandiko matakatifu aliwageuza wengi kutoka kuabudu sanamu kwa Kristo, miongoni mwao mtu mkuu wa Baraza la Seneti.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyr Agrippina of Rome":
{"type": "Bikira Shahidi · karne ya 3", "life": "Bikira Shahidi Mtakatifu Agripina aliteseka kwa ajili ya Kristo huko Roma katika mateso ya wafalme, na masalia yake matakatifu yakawa katika zama za baadaye hazina na ulinzi wa mji mmoja wa Sisilia.", "patron": "Mabikira waliowekwa wakfu kwa Kristo; ambao masalia yao yanachukuliwa mahali salama."},

"Martyr Aithalas of Persia":
{"type": "Shemasi · karne ya 4", "life": "Shahidi Mtakatifu Aithala, shemasi wa Kanisa katika Persia, aliteseka kwa ajili ya Kristo mwaka wa 380 katika mateso ya Wakristo chini ya mfalme Sapori. Akiikiri imani kwa uthabiti na akikataa kuuabudu moto na jua kama Waajemi walivyofanya, alihukumiwa kwa amri ya mfalme na akauawa kwa kupigwa mawe, na hivyo akapokea taji la shahada.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Alexandra the Empress, wife of Diocletian":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Aleksandra Malkia, ambaye mapokeo yanamtaja kuwa mke wa Diokletiano mwenyewe, aliipata taji yake katikati kabisa ya mateso, katika ukumbi ambamo yalikuwa yakiendeshwa; kwa maana katika siku za pambano la Shahidi Mkuu Georgi malkia alitazama kutoka mahali pake kando ya kiti cha enzi, na kile ambacho tamasha lile liliwafundisha wabeba-mikuki na watumishi kilimfundisha yeye pia, na kwa kutisha zaidi, kwa kuwa yeye peke yake miongoni mwa mashahidi wote alishiriki meza na kitanda cha mtesi.", "patron": "Maombezi yake huombwa kwa ajili ya wake wa watesi; malkia na waliopewa vyeo vikuu."},

"Martyr Ananias of Persia":
{"type": "Shahidi · kiliturujia", "life": "Shahidi Mtakatifu Anania wa Persia alimkiri Kristo katika nchi ya waabudu-moto na akautia muhuri ukiri wake kwa damu yake. Alipokamatwa na kuamriwa amkane Bwana, alikataa, akakabidhiwa kwa mateso; na katikati ya mateso yake Mungu aliyafumbua macho yake, hata shahidi akapaza sauti mbele ya wote, Naona ngazi ielekeayo mbinguni, na watu wang'aao wakiniita kwenye mji wa ajabu wa nuru.", "patron": "Maombezi yake huombwa kwa ajili ya maono yaliyotolewa kwa wanaoteseka."},

"Martyr Anastasius the Fuller at Salona in Dalmatia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Anastasio Mfuaji wa Nguo alizaliwa Akwileia katika Italia na akaifanya kazi yake ya kufua nguo huko Salona katika Dalmatia, katika siku za mateso ya Diokletiano. Akikataa kuificha imani ambayo kwa ajili yake wengine walikuwa wakifa, alichora Msalaba wa Kristo waziwazi juu ya mlango wa karakana yake, ili kila apitaye ajue ni mtumishi wa nani anayefanya kazi ndani.", "patron": "Maombezi yake huombwa kwa ajili ya wafuaji nguo; mafundi na wafanyabiashara."},

"Martyr Anastasius the Fuller of Salona in Dalmatia":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Anastasio Mfuaji wa Nguo aliishi Salona katika Dalmatia mwishoni mwa karne ya tatu, fundi aliyeifanya karakana yake ya kufua nguo kuwa mimbari. Alimhubiri Kristo wazi katika mji kwa neno na kwa ishara, akichora msalaba mahali panapoonekana juu ya mlango wake, hata kazi yake na imani yake vikasimama vikitangazwa pamoja.", "patron": "Maombezi yake huombwa kwa ajili ya wafuaji nguo."},

"Martyr Andrew Stratelates, and 2,593 soldiers with him, in Cilicia":
{"type": "Jemadari · karne ya 4", "life": "Shahidi Mtakatifu Andrea alikuwa jemadari katika jeshi la Warumi chini ya mfalme Maksimiano, akipendwa na wote kwa ushujaa wake na kwa haki yake, na jeshi kubwa la Waajemi lilipovamia nchi za Shamu alipewa uongozi mkuu pamoja na cheo cha Stratelati. Akichagua kikundi kidogo cha askari hodari, kama Gideoni wa zamani alivyochagua mia zake tatu, alikwenda kupambana na adui.", "patron": "Maombezi yao huombwa kwa ajili ya askari."},

"Martyr Anna":
{"type": "Mtawa wa kike · karne ya 8", "life": "Mheshimiwa Ana, Shahidi Mtawa, alikuwa mwanamke wa jamaa tukufu ya Konstantinopoli ambaye, akiwaka upendo wa Kristo, aliuza mali yake yote, akawapa maskini fedha, na akapokea unyoaji wa utawa kutoka kwa Mtakatifu Stefano Mpya alipokuwa akiishi katika Mlima Auxentio, naye akampeleka katika monasteri ya wanawake iitwayo Trikinarioni, ambako aling'aa katika kufunga na utii.", "patron": "Maombezi yake huombwa kwa ajili ya watawa wa kike; kukataa ushuhuda wa uongo."},

"Martyr Anna at Rome":
{"type": "Mlei wa kike · kiliturujia", "life": "Shahidi Mtakatifu Ana aliteseka kwa ajili ya Kristo huko Roma katika zama za mateso. Machache yamehifadhiwa juu yake, lakini nyimbo za Kanisa zinamheshimu kama nyota ing'aayo aliyemkiri Kristo kwa ujasiri, akiwageuza waamini kutoka mvuto wa sanamu na akipokea kutoka kwa Bwana taji lisiloharibika kwa mateso yake.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Martyr Anthony of Alexandria":
{"type": "Mlei · karne ya 4", "life": "Shahidi Mtakatifu Antonio alikuwa Mkristo wa mji wa Aleksandria aliyekamatwa kwa ukiri wake wa Kristo. Akifungwa mtini, mwili wake ulichanwa kwa kulabu za chuma, kisha akahukumiwa kuchomwa akiwa hai; lakini akiwa amesimama katikati ya moto, hakufadhaika, na kwa utulivu aliwahimiza waliokuwa wakitazama wasijitaabishe kwa ajili ya mwili, upitao, bali kwa ajili ya roho katika kupanda kwake kuelekea Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Anthusa at Rome":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Anthusa alikuwa mke wa afisa wa Kirumi katika siku ambazo uzushi wa Ario, ingawa ulikuwa umehukumiwa Nikea, bado ulishika mahakama na ikulu mkononi mwake; naye akitaka ubatizo mtakatifu, hakutaka kuupokea kutoka mkono wenye shaka, bali alipokea siri ya wokovu kutoka kwa Mtakatifu Ambrosio wa Milano mwenyewe, mtetezi mkuu wa Umungu wa Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya wake wa maofisa; ubatizo uliohifadhiwa bila kuchafuliwa."},

"Martyr Antiochus the Physician of Sebaste":
{"type": "Tabibu · karne ya 4", "life": "Shahidi Mtakatifu Antioko alikuwa mzaliwa wa Sebaste katika Kapadokia na tabibu kwa kazi yake, naye alikuwa ndugu wa Shahidi mtakatifu Platoni. Ilipojulikana kwa wapagani kwamba yeye ni Mkristo, alikamatwa na kuletwa mahakamani, na ingawa alidhulumiwa kwa mateso makali alibaki imara katika ukiri wake wa Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; wagonjwa."},

"Martyr Antonina of Nicea, in Bithynia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Antonina wa Nikea katika Bithinia aliteseka katika mateso yaliyoinuliwa chini ya Maksimiano mwanzoni mwa karne ya nne, wakati amri za kifalme zilipokuwa zikizijaza tena mahakama za Asia Ndogo kwa Wakristo wasiokubali kubadilisha chembe moja ya ubani kwa maisha yao.", "patron": "Maombezi yake huombwa kwa ajili ya wanawake mbele ya mahakama; ukiri uliohifadhiwa katika maji."},

"Martyr Aquilina of Byblos in Syria":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Akilina, mzaliwa wa mji wa Kifoinike wa Biblo, aliteseka kwa ajili ya Kristo akiwa bado mtoto katika mateso ya Diokletiano, naye anaonyesha kwamba ukiri wa imani haujui umri.", "patron": "Watoto na wasichana wadogo; wanaowaongoa marafiki zao."},

"Martyr Archil II, King of Georgia":
{"type": "Shahidi · karne ya 8", "life": "Mfalme Mtakatifu Arkili alikuwa mfalme wa Kartli, moyo wa nchi ya Georgia, katika karne ya nane, aliyewatetea watu wake Wakristo dhidi ya mvamizi na akavikwa taji ya shahada kwa kukataa kumkana Kristo.", "patron": "Wafalme wanaokufa kwa ajili ya imani; watetezi wa Georgia dhidi ya mvamizi."},

"Martyr Ardalion the Actor":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Ardalio Mwigizaji aliipata taji yake katikati ya maonyesho, na Kanisa daima limelithamini pambano lake kama mojawapo ya mavizio ya ujasiri zaidi ya neema. Akiwa mwigizaji stadi wa jukwaani katika utawala wa Maksimiano Galerio, Ardalio alipangiwa kucheza katika tamasha lililoandaliwa ili kuufurahisha umati kwa gharama ya Wakristo: alipaswa kucheza nafasi ya Mkristo anayehojiwa, akikataa kwanza kutoa dhabihu, na kisha, kwa mwisho wa kuchekesha, akimkana Kristo, ukanaji wa imani ukiigizwa kama burudani.", "patron": "Maombezi yake huombwa kwa ajili ya waigizaji na wachezaji; wote ambao sanaa yao huwa kweli."},

"Martyr Arethas and 4,299 Martyrs with him":
{"type": "Mashahidi · karne ya 6", "life": "Shahidi Mtakatifu Aretha na pamoja naye mashahidi elfu nne na mia mbili na tisini na tisa waliteseka mwaka wa 523 katika mji wa Najran katika Arabia, ambako imani ya Kikristo ilikuwa imeshika mizizi mirefu. Dunaani, mtawala wa Wahimyari, mtesi wa Kanisa, aliuzingira mji wa Kikristo, na alipokosa kuuteka kwa nguvu, aliapa kwa uongo kwamba hangemdhuru mtu yeyote, na alipokubaliwa kuingia, aliwapa waamini chaguo la kumkana Kristo au kufa.", "patron": "Maombezi yao huombwa kwa ajili ya Wakristo chini ya mateso; miji mizima iliyokuwa waaminifu hadi kufa."},

"Martyr Ariádnē of Phrygia":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Ariadni alikuwa mtumwa katika nyumba ya Tertulo, raia mashuhuri wa Primneso katika Frigia, katika siku za mfalme Hadriano; na ingawa alikuwa mtumishi kwa hadhi, alikuwa huru katika Kristo na mwenye hekima kuliko wanawake wengi watukufu wa mji wake.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi; walioteswa."},

"Martyr Asclas of Egypt":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Askla aliteseka kwa ajili ya Kristo katika mji wa Antinoe katika Thebaida ya Misri, katika mateso ya mwanzoni mwa karne ya nne, na pambano lake linakumbukwa kwa ajabu ambayo kwayo alimlazimisha mwamuzi wake mwenyewe kuikiri kweli.", "patron": "Mashua ya mtawala iliyosimamishwa katika Nili."},

"Martyr Athanasius, Abbot of Bretsk":
{"type": "Abate · karne ya 17", "life": "Mheshimiwa Athanasio, Abate wa Brest na Kuhani Shahidi, alizaliwa karibu mwaka wa 1597 katika jamaa ya Kibelarusi yenye uchaji Mungu iliyoitwa Filipovich na akapata elimu kamili, akitumika katika ujana wake kama mwalimu kabla ya kupokea unyoaji wa utawa katika monasteri ya Roho Mtakatifu ya Vilna. Alipowekwa mtawa kuhani na baadaye kufanywa mkuu wa monasteri ya Mtakatifu Simeoni huko Brest, alikuwa mmoja wa watetezi wa ujasiri kuliko wote wa Uorthodoksi katika nchi zilizotwaliwa na taji la Poland, ambako Muungano wa Brest ulikuwa ukilazimishwa juu ya waamini kwa nguvu.", "patron": "Maombezi yake huombwa kwa ajili ya utetezi wa Uorthodoksi; ujasiri mbele ya watawala."},

"Martyr Barbarus the Soldier, and those with him, in Morea":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Barbaro Askari aliteseka pamoja na wenzake Bako, Kalimako na Dionisio katika siku za Yuliano Mwasi, karibu mwaka wa 362, na pambano lake lilitegemea mtego wa kale kuliko yote uliowekewa askari Mkristo, dhabihu ya ushindi.", "patron": "Pambano la peke yake lililoshindwa na pambano kubwa zaidi kuchaguliwa."},

"Martyr Barlaam of Caesarea, in Cappadocia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Barlaamu alikuwa Mkristo mzee aliyeteseka katika mateso chini ya Diokletiano, karibu mwaka wa 304; habari za kale zinaweka pambano lake Kaisaria katika Kapadokia, au, kama wengine wasimuliavyo, Antiokia. Alipokamatwa na kuletwa mahakamani, mzee alijikiri kuwa Mkristo kwa maneno machache na rahisi, kwa maana hakuwa msomi.", "patron": "Maombezi yake huombwa kwa ajili ya wazee; uvumilivu katika udhaifu."},

"Martyr Barulas the Youth of Caesarea":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Barula Kijana alikuwa mtoto mdogo wa Antiokia ambaye Mungu alimfanya shahidi wa kweli mbele ya wenye mamlaka wa zama zile. Shemasi Romano aliposimama mahakamani mbele ya mkuu wa mji Asklepiade na kudhihakiwa kwa imani yake, mkiri alimwonyesha mvulana mdogo katika umati na akasema kwamba hata mtoto anamjua Mungu mmoja wa kweli ambaye wenye hekima wa wapagani wanamkana.", "patron": "Maombezi yake huombwa kwa ajili ya watoto; ushuhuda wa watoto."},

"Martyr Basiliscus, Bishop of Comana":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Basilisko aliteseka karibu na Komana katika Ponto katika mateso ya mfalme Maksimiano, karibu mwaka wa 308, naye alikuwa jamaa, mapokeo yashikavyo mpwa, wa Shahidi Mkuu Theodoro Askari Mpya.", "patron": "Ukiri uliohifadhiwa baada ya taji za wenzake."},

"Martyr Bassa of Edessa and her sons Theogonius, Agapius, and Pistus":
{"type": "Mashahidi · karne ya 4", "life": "Shahidi Mtakatifu Basa aliishi katika mji wa Edesa katika Makedonia na alikuwa ameolewa na kuhani mpagani, ingawa yeye mwenyewe alikuwa amelelewa tangu utoto katika imani ya Kikristo, ambayo aliwafundisha pia wanawe watatu, Theogni, Agapio na Pisto. Katika mateso chini ya Maksimiano, mumewe mwenyewe alimsingizia yeye na watoto kwa wenye mamlaka.", "patron": "Maombezi yao huombwa kwa ajili ya mama."},

"Martyr Boniface at Tarsus in Cilicia, and Righteous Aglaϊa of Rome":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Bonifasi alikuwa msimamizi wa mali wa Aglaida, mwanamke tajiri kijana wa Kirumi, na wawili hao waliishi katika dhambi pamoja, ingawa Bonifasi alikuwa na huruma kwa maskini na ukarimu kwa wageni, moyo mwema uliokuwa ukizama katika ulevi na ufisadi. Akitaka kuwa na masalia matakatifu kama ulinzi wa roho yake, Aglaida alimtuma msimamizi wake Mashariki, ambako mateso yalikuwa yakiwaka, ili kununua miili ya mashahidi.", "patron": "Maombezi yao huombwa kwa ajili ya wasimamizi wa mali; watumishi."},

"Martyr Callinicus of Gangra in Asia Minor":
{"type": "Mlei · karne ya 3", "life": "Shahidi Mtakatifu Kalinikos, mzaliwa wa Kilikia, alilelewa katika imani ya Kikristo tangu utoto, na akihuzunika kwamba wengi wangeangamia katika ibada ya sanamu, alipita katika miji na vijiji akimhubiri Kristo na akiwageuza wengi kwenye kweli. Alipokamatwa Ankira katika Galatia, aliletwa mbele ya gavana mkali Sakerdo, na alipokataa bila hofu kutoa dhabihu, akitangaza kwamba haogopi shahada, kwa kuwa kila mwamini hupokea nguvu kutoka kwa Kristo na kwa njia ya kifo hurithi uzima wa milele, alipigwa kikatili na mwili wake ukachanwa kwa kulabu za chuma.", "patron": "Maombezi yake huombwa kwa ajili ya kuhubiri; huruma kwa maadui."},

"Martyr Callistratus and 49 companions":
{"type": "Mashahidi · karne ya 4", "life": "Shahidi Mtakatifu Kalistrato alizaliwa Karthago katika jamaa ya Kikristo; babu yake Neokoro, askari katika Palestina chini ya Pontio Pilato, alikuwa ameuona Kusulubiwa na Kufufuka kwa Bwana na akarudi nyumbani mwamini, na imani ikarithishwa katika nyumba yake. Kalistrato mwenyewe akawa askari, akiwazidi wote kwa upole wa mwenendo, na akiamka usiku kwa sala.", "patron": "Maombezi yao huombwa kwa ajili ya askari."},

"Martyr Charitina of Amisos":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Karitina wa Amiso katika Ponto aliachwa yatima utotoni na akalelewa kama binti na Mkristo mcha Mungu aliyeitwa Klaudio, katika nyumba yake alikua katika uzuri, busara na wema, akiisoma sheria ya Mungu mchana na usiku na akiweka nadhiri ya ubikira wake kwa Kristo, huku kwa maneno yake akiwaleta wengi kwenye njia ya wokovu.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi; usafi."},

"Martyr Christina of Tyre":
{"type": "Bikira · karne ya 3", "life": "Shahidi Mtakatifu Kristina aliishi katika karne ya tatu, binti wa mtu tajiri aliyeitwa Urbano aliyekuwa gavana wa Tiro. Akikusudia kwamba atumike kama kuhani wa kike wa kipagani, baba yake alimfungia pamoja na sanamu nyingi za dhahabu na fedha na akamwamuru afukize ubani mbele yake.", "patron": "Maombezi yake huombwa kwa ajili ya kuongoka; uthabiti."},

"Martyr Christodoulos":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Kristodulo anakumbukwa siku hii miongoni mwa mashahidi wa Kanisa la kwanza, na jina lake ndiyo historia yake: Kristodulo, mtumwa wa Kristo, cheo ambacho mashahidi wa karne za kwanza walikidai mbele ya mahakama kama utambulisho wao wote wa kisheria, wakifagilia mbali familia, mji na hadhi katika utii ule mmoja ambao himaya haikuweza kuutoza kodi wala kuuamuru.", "patron": "Maombezi yake huombwa kwa ajili ya wote wanaolibeba jina la Kristo; jina lililokiriwa hadi mwisho."},

"Martyr Christopher of Lycia, and, with him, the Martyrs Callinika and Aquilina":
{"type": "Shahidi Mkuu · karne ya 3", "life": "Shahidi Mkuu Mtakatifu Kristoforo aliteseka katika Likia chini ya mfalme Desio, karibu mwaka wa 250, na Kanisa limempenda kwa karne kumi na saba kama mlinzi wa wasafiri na kemeo lisimamalo dhidi ya kila hukumu ya kwa kuangalia sura.", "patron": "Jina la Mbeba-Kristo lililopatikana."},

"Martyr Chronides of Alexandria and those with him":
{"type": "Mashahidi · karne ya 3", "life": "Shahidi Mtakatifu Kronide aliteseka kwa ajili ya Kristo katika karne ya tatu pamoja na Leontio na Serapioni, wote watatu wakiwa Wamisri, katika mateso ya zama zile. Baada ya kuvumilia mateso makali kwa ukiri wao wa imani, mashahidi watatu walifungwa mikono na miguu na kutupwa baharini, ambako waliitoa roho zao kwa Mungu.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyr Claudius, Asterius, Neon, and Theonilla of Aegæ in Cilicia":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Klaudio, Asterio na Neoni, pamoja na Shahidi Theonila, waliteseka Aegae katika Kilikia mwaka wa 285, chini ya gavana Lisia. Wale watatu walikuwa ndugu, na baba yao alipokufa, mama yao wa kambo, akitamani urithi, aliwasingizia watoto wa mumewe kwa wenye mamlaka kuwa Wakristo, akiwatoa kwa mateso kwa ajili ya mali yao.", "patron": "Maombezi yao huombwa kwa ajili ya waliodhulumiwa mali na kusalitiwa; mayatima waliodhulumiwa na jamaa."},

"Martyr Conon of Isauria":
{"type": "Shahidi · karne ya 1", "life": "Shahidi Mtakatifu Konon wa Isauria alizaliwa katika kijiji cha Badine karibu na mji wa Isauria katika Asia Ndogo, ambao watu wake walikuwa wameipokea imani kutoka kwa Mtume Paulo; na tangu ujana wake alikuwa chini ya ulinzi wa pekee wa Malaika Mkuu Mikaeli, mkuu wa majeshi ya mbinguni, aliyemtokea na kumsaidia katika mwendo wote wa maisha yake.", "patron": "Maombezi yake huombwa kwa ajili ya wanandoa walioitwa kujizuia; wanaozungukwa na mashetani."},

"Martyr Crescens of Myra in Lycia":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Kresenti wa Mira katika Likia alikuwa mtu wa jamaa tukufu na wa umri mkubwa asiyeweza kuutazama mji wake ukiabudu kile ambacho mikono yake yenyewe ilikitengeneza: akiona ibada ya sanamu ikishinda na majirani zake wakiwa watumwa wa vitu visivyo na uhai, mzee alikwenda kwa hiari yake katikati yao na akawahimiza wauache upotovu wa bure na warudi kwa Mungu ambaye Wakristo wanamwabudu, Muumba wa vyote na Bwana wa uzima, akijitolea kwa pambano ambalo bado hakuna aliyemtaka.", "patron": "Maombezi yake huombwa kwa ajili ya wazee katika ushuhuda; wanaoshinikizwa kujifanya."},

"Martyr Cyril the Deacon of Heliopolis, and those with him, who suffered under Julian the Apostate":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Kirilo Shemasi wa Heliopoli na wale walioteseka pamoja naye walikuwa wahanga wa mgeuko wa kipagani chini ya Yuliano Mwasi, mwaka wa 362, wakati kurudishwa kwa sanamu na mfalme kuliwapa wafuasi wa dini ya kale ruhusa ya kulipiza kisasi kwa Wakristo waliokuwa wamewadhili chini ya Konstantino.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wanaoteseka kwa bidii ya zamani sana."},

"Martyr Cyrilla of Cyrene in Libya, a widow":
{"type": "Mlei wa kike · karne ya 4", "life": "Shahidi Mtakatifu Kirila aliteseka Kirene katika Libya wakati wa mateso ya Diokletiano. Akiwa mjane aliyejitoa kwa Kristo, alikamatwa na kuamriwa afukize ubani kwa sanamu. Makaa ya moto pamoja na ubani yalipowekwa juu ya kiganja chake kilicho wazi, ili kwa kuyatupa aonekane kana kwamba anatoa sadaka kwa miungu ya uongo, alivumilia moto bila kutetemeka na akakataa kuyaacha makaa yaanguke, akichagua kuungua kuliko kuonekana hata kwa dakika moja akimkana Bwana wake.", "patron": "Maombezi yake huombwa kwa ajili ya uthabiti chini ya mateso."},

"Martyr Dometius of Persia and his two disciples":
{"type": "Shemasi · karne ya 4", "life": "Mheshimiwa Dometio wa Persia, Shahidi Mtawa, aliishi katika Persia katika karne ya nne na aliongolewa kwa Kristo katika ujana wake na mwamini aliyeitwa Uaro. Akiiacha nchi yake, alikuja katika mji wa mpakani wa Nisibisi, ambako alibatizwa na kunyolewa utawa, na baadaye alihamia monasteri ya Watakatifu Sergio na Bako chini ya arkimandriti mkali Urbelo.", "patron": "Maombezi yake huombwa kwa ajili ya uponyaji; kazi ya kujinyima."},

"Martyr Domnina of Anazarbus":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Domnina wa Anazarbo katika Kilikia aliteseka kwa ajili ya Kristo chini ya mfalme Diokletiano, akiletwa mahakamani mbele ya Lisia, gavana wa eneo lile. Akijikiri kuwa Mkristo na akikataa kutoa dhabihu kwa sanamu, alipigwa bila huruma kwa fimbo na akadhulumiwa kwa mateso mengine, kisha akatupwa gerezani, ambako, akiwa amechoka kwa majeraha yake na minyororo yake, aliitoa roho yake kwa Mungu karibu mwaka wa 286.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Drosίs, daughter of Emperor Trajan":
{"type": "Bikira Shahidi · karne ya 2", "life": "Bikira Mtakatifu Drosi, binti wa mfalme Trayano mwenyewe, ni ushuhuda wa Kanisa kwamba Injili ilipanda katika karne yake ya kwanza hadi kwenye jiko lenyewe la mtesi wake. Katika miaka ambayo amri ya baba yake iliongoza jinsi Wakristo walivyoshughulikiwa na miili ya mashahidi ilitupwa nje bila kuzikwa ili kuikamilisha aibu yao, Drosi alijiunga kwa siri.", "patron": "Maombezi yake huombwa kwa ajili ya binti wa nyumba zenye uadui; wanaozika mashahidi."},

"Martyr Dēmḗtrios of Thrace":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Demetrio wa Thrakia alikuwa Mkristo wa kijiji cha Dabuda, karibu na mji wa Amapa katika nchi ya Thrakia, naye aliteseka katika mateso ya mwishoni mwa karne ya tatu, karibu mwaka wa 298. Alipokamatwa kama Mkristo na kuletwa mbele ya gavana wa jimbo, alimkiri Bwana Yesu Kristo kwa unyofu na ujasiri, na wala ushawishi wala vitisho vya mwamuzi havikuweza kumfanya atoe dhabihu kwa sanamu.", "patron": "Maombezi yake huombwa kwa ajili ya uthabiti wa wasiojulikana."},

"Martyr Eleazar the Teacher of the Holy Seven Maccabee Martyrs":
{"type": "Mzee · karne ya 2 KK", "life": "Shahidi Mtakatifu Eleazari aliishi katika karne ya pili kabla ya Kristo na alikuwa mwandishi na mwalimu, mtu wa heshima kubwa na wa umri mkubwa. Antioko Epifane alipotaka kuwalazimisha Wayahudi waiache Sheria ya Musa na kula nyama ya nguruwe kinyume na agano, Eleazari, ingawa alikuwa na miaka tisini, alikataa kuyaokoa maisha yake kwa maafikiano madogo hivyo au hata kujifanya anatii, akihesabu kuwa jambo lisilostahili miaka yake na kikwazo kwa vijana.", "patron": "Maombezi yake huombwa kwa ajili ya walimu; uadilifu katika uzee."},

"Martyr Eleutherius of Constantinople":
{"type": "Mlei · karne ya 4", "life": "Shahidi Mtakatifu Eleftherio alitumika kama mwangalizi wa vyumba katika baraza la mfalme Maksimiano, na alipofikia imani ya Kristo alijiondoa hadi shamba lake na akajenga kanisa juu ya ardhi yake mwenyewe, ambako alimwabudu Mungu. Mmoja wa watumishi wake alimsaliti kwa mfalme, na alipoitwa na kuhojiwa, Eleftherio alijikiri bila hofu kuwa Mkristo.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Emilian of Silistria in Bulgaria":
{"type": "Mlei · karne ya 4", "life": "Shahidi Mtakatifu Emiliano, Mslavi kwa kuzaliwa, aliteseka kwa ajili ya Kristo chini ya Yuliano Mwasi, aliyetaka kuirudisha ibada ya sanamu katika himaya yote na akaamuru kifo kwa Mkristo yeyote asiyekubali kuziheshimu. Emiliano aliishi katika mji wa Dorostolo kando ya Danube, katika nchi ambayo sasa ni Bulgaria, akiwa mtumwa wa mpagani mkatili na mwenye ushabiki, huku akiishika kwa siri imani ya Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri wa ujasiri."},

"Martyr Eudokia of Heliopolis":
{"type": "Shahidi Mtawa · karne ya 2", "life": "Mheshimiwa Eudokia wa Heliopoli, Shahidi Mtawa, ndiye sura kubwa ya Kanisa ya toba mwanzoni mwa majira ya machipuko, Msamaria wa Heliopoli ya Foinike, ambayo leo ni Baalbek, katika siku za Trayano, ambaye uzuri wake ulikuwa umemfanya mmoja wa wanawake matajiri kuliko wote wa Mashariki na ambaye utajiri wake ulipatikana katika dhambi, roho yake, kama maisha yake yasemavyo waziwazi, ikiwa imekufa ganzi na moyo wake umekuwa mgumu.", "patron": "Maombezi yake huombwa kwa ajili ya wanaotubu; maabesi."},

"Martyr Eudokia of Persia":
{"type": "Mlei wa kike · karne ya 4", "life": "Shahidi Mtakatifu Eudokia alikuwa mzaliwa wa Anatolia aliyeishi katika karne ya nne, naye alichukuliwa utumwani pamoja na Wakristo elfu tisa na jeshi la mfalme wa Persia Sapori. Akiwa amezijua vizuri Maandiko matakatifu, aliwaimarisha na kuwafundisha wafungwa wenzake katika dhiki yao, naye aliihubiri Injili hata kwa wanawake wa Kipersia, akiwageuza wengi wao kwenye imani ya Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya wakatekisti; mateka."},

"Martyr Eupsychius of Caesarea, in Cappadocia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Eupsikio wa Kaisaria katika Kapadokia alikuwa kijana wa jamaa tukufu, aliyeoa karibuni, karamu ya arusi ikiwa imekwisha kwa shida, wakati utawala wa Yuliano Mwasi ulipowawekea Wakristo wa mji wake chaguo lililolifanya jina lake; kwa maana Kaisaria, iliyokuwa karibu yote ya Kikristo, bado ilikuwa na hekalu la Fortuna, sanamu ya mwisho iliyokuwa ikitumika ya miungu ya kale mjini, na Eupsikio, akiwaka bidii, alikusanya kikundi cha waamini na akaliangamiza kabisa, bwana arusi akiongoza ubomoaji kama watu wengine waongozavyo ngoma ya arusi.", "patron": "Maombezi yake huombwa kwa ajili ya waliooana karibuni; vijana wenye bidii."},

"Martyr Eusignius of Antioch":
{"type": "Mlei · karne ya 4", "life": "Shahidi Mtakatifu Eusignio alizaliwa Antiokia katikati ya karne ya tatu, na kwa miaka sitini alitumika kama askari katika majeshi ya Roma chini ya Diokletiano, Maksimiano, Konstantio Kloro, na Konstantino Mkuu na wanawe. Alikuwa mwenzake wa Shahidi Basilisko, ambaye mateso yake aliyaandika, na mwanzoni mwa utawala wa Konstantino yeye mwenyewe alikuwa shahidi wa macho wa kutokea kwa Msalaba angani kulikoutabiri ushindi wa mfalme.", "patron": "Maombezi yake huombwa kwa ajili ya askari; ukiri thabiti."},

"Martyr Felicitas of Rome, and her seven sons":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Felisita wa Roma, mjane tajiri na wa jamaa tukufu, aliteseka pamoja na wanawe saba chini ya mfalme Marko Aurelio, karibu mwaka wa 164, na Kanisa daima limemweka kando ya mama wa Wamakabayo, mama wawili wa saba walioviona vizazi vyao vyote vikiwatangulia katika utukufu.", "patron": "Maombezi yake huombwa kwa ajili ya mama; wajane."},

"Martyr Florentius of Thessalonica":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Florentio alikuwa mzaliwa wa Thesalonike, mwenye bidii kwa utukufu wa Mungu, aliyelifichua bila hofu giza la ibada ya sanamu kati ya wenzake wa mji na akawaongoza wengi katika nuru ya kumjua Mungu wa kweli, akiwafundisha imani katika Kristo na kutenda mapenzi yake.", "patron": "Maombezi yake huombwa kwa ajili ya mahubiri ya ujasiri."},

"Martyr Gemellus of Paphlagonia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Gemelo wa Paflagonia aliteseka mwaka wa 361 chini ya Yuliano Mwasi, mfalme aliyemkana Kristo aliyelelewa ndani yake na akajiwekea kuirudisha ibada ya sanamu. Alipokutana na mfalme huko Ankira katika Galatia, Gemelo aliukemea uasi wake uso kwa uso, kwa uhuru wa mtu amchaye Mungu kuliko wafalme.", "patron": "Maombezi yake huombwa kwa ajili ya ujasiri mbele ya watawala walioikana imani."},

"Martyr Gerontius, and those with him, of Saint David Gareji Monastery, Georgia":
{"type": "Watawa · karne ya 19", "life": "Mashahidi Waheshimiwa wapya wa monasteri ya Davidi Gareji katika jangwa la Georgia waliyatoa maisha yao kwa ajili ya Kristo katika kiangazi cha mwaka wa 1851, wakati jeshi la Kidagestani lilipoivamia lavra ile ya kale iliyoanzishwa na Mtakatifu Davidi. Wavamizi waliipora monasteri, wakichukua vyombo vyake vitakatifu na vitabu, na wakawachukua watawa mateka, wakiwatesa na kuwaua walio imara kuliko wote miongoni mwao.", "patron": "Maombezi yao huombwa kwa ajili ya watawa; ukiri thabiti wakati wa mateso."},

"Martyr Gobron (Michael) and 133 soldiers, of Georgia":
{"type": "Jemadari · karne ya 10", "life": "Shahidi Mtakatifu Gobron, katika ubatizo mtakatifu Mikaeli, alikuwa mtukufu na jemadari wa Kigeorgia, aliyeitwa Gobron, jasiri, kwa ushujaa wake; na mwaka wa 914, majeshi ya Kiislamu yalipozifagia nchi za Georgia, aliongoza utetezi wa ngome ya Kveli. Baada ya kuzingirwa kwa muda mrefu ngome ilianguka, na Mikaeli alichukuliwa mateka pamoja na askari wake mia moja na thelathini na watatu.", "patron": "Maombezi yao huombwa kwa ajili ya askari; uaminifu katika kushindwa."},

"Martyr Gorazd of Prague, Bohemia and Moravo-Cilezsk":
{"type": "Askofu · karne ya 20", "life": "Kuhani Shahidi Mtakatifu Gorazd, Askofu wa Prague na wa Bohemia na Moravia-Silesia, alizaliwa katika Moravia mwaka wa 1879 na akaitwa Matia katika ubatizo. Akiwekwa kwanza katika kanisa la Kirumi, aliingia katika Uorthodoksi baada ya Vita vya Kwanza vya Dunia na akawaongoza makumi ya maelfu ya wenzake wa taifa katika Kanisa la Kiorthodoksi, akiwekwa wakfu kuwa askofu wa nchi za Kicheki chini ya Upatriaki wa Serbia, akichukua jina la Gorazd kwa kumkumbuka mwanafunzi wa Mtakatifu Methodio.", "patron": "Maombezi yake huombwa kwa ajili ya wanaowapa hifadhi walioteswa; waamini wa Kicheki na Kislovakia."},

"Martyr Heliconis of Thessalonica":
{"type": "Shahidi · karne ya 3", "life": "Bikira Shahidi Mtakatifu Helikoni alikuwa mzaliwa wa Thesalonike aliyeteseka kwa ajili ya Kristo huko Korintho katika karne ya tatu, katika utawala wa mfalme Gordiano na, habari zinaendelea, wa Aureliano baada yake.", "patron": "Hekalu la Athena lililoangushwa kwa sala yake."},

"Martyr Hermias at Comana":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Hermia alikuwa askari mzee aliyeteseka kwa ajili ya Kristo huko Komana katika Kapadokia katika utawala wa mfalme Antonino, katika karne ya pili, na mateso yake ni kumbukumbu ya adhabu zilizonusurika kwa muujiza hadi Mungu alipopenda kumpokea.", "patron": "Askari mzee thabiti chini ya kila ukatili."},

"Martyr Hyacinth of Caesarea, in Cappadocia, and those with him":
{"type": "Mwangalizi wa vyumba · karne ya 2", "life": "Shahidi Mtakatifu Hiakinto alikuwa mzaliwa wa Kaisaria katika Kapadokia, aliyelelewa katika jamaa ya Kikristo, aliyetumika kama mwangalizi wa vyumba kwa mfalme Trayano huku akiificha imani yake ya Kristo. Siku moja, mfalme na baraza lake walipokuwa wakitoa dhabihu kwa sanamu, kijana Hiakinto alijiondoa hadi chumba cha faragha na akamsali Kristo kwa bidii.", "patron": "Maombezi yake huombwa kwa ajili ya uthabiti katika imani."},

"Martyr Hyacinthus of Amastridea":
{"type": "Mlei · karne ya 4", "life": "Shahidi Mtakatifu Hiakinto alizaliwa katika jamaa ya Kikristo yenye uchaji Mungu katika mji wa Amastri katika Asia Ndogo, na inasemwa kwamba malaika alitokea na kumpa jina lake. Hata akiwa mtoto mdogo alijaa neema, na alipokuwa na miaka mitatu tu sala yake ilimfufua mtoto mchanga aliyekufa, hata watoto wale wawili wakakua pamoja na kujitoa kwa mwenendo wa maisha ya kujinyima.", "patron": "Maombezi yake huombwa kwa ajili ya bidii dhidi ya ibada ya sanamu."},

"Martyr Irenarchus and Seven Women Martyrs at Sebaste":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Irenarko wa Sebaste katika Armenia alitumika, katika utawala wa Diokletiano, kama mnyongaji, mmoja wa wale waliowatesa wakiri wa Kristo; na Mungu, aliyemwita Paulo njiani na mwizi msalabani, alimwita Irenarko akiwa kwenye vyombo vya kazi yake.", "patron": "Maombezi yake huombwa kwa ajili ya wanyongaji walioongoka; wanaotubu ukatili."},

"Martyr Irene":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Irene anakumbukwa siku hii katika minaia za Kislavoni, zinazoliweka jina lake kando ya bikira shahidi Theodosia wa Tiro, wawili hao wakishikwa pamoja katika kalenda za makanisa ya Urusi na Ukraine kama wenzao wa ukumbusho mmoja; na juu ya pambano lake mahususi vitabu vimehifadhi mambo ya msingi tu, kwamba alikuwa mwanamke aliyemkiri Kristo katika zama za mateso na akautia muhuri ukiri kwa kifo chake, akipokea taji la shahidi.", "patron": "Maombezi yake huombwa kwa ajili ya wenzao wa mashahidi; jina lililohifadhiwa kando ya Theodosia."},

"Martyr Julian of Dalmatia":
{"type": "Mlei · karne ya 2", "life": "Shahidi Mtakatifu Yuliano aliteseka kwa ajili ya Kristo katika utawala wa mfalme Antonino Pio, katika jimbo la Kiitalia la Kampania. Gavana Flaviano alipokuwa akiwatafuta Wakristo ili awalete mahakamani, kijana Yuliano, aliyekuwa amefika Kampania kutoka Dalmatia, alionekana kuwa mfuasi wa Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Julian of Tarsus, in Cilicia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Yuliano wa Tarso katika Kilikia aliteseka kwa ajili ya Kristo katika mateso ya Diokletiano, na uvumilivu wake mrefu na kifo chake cha ajabu vilisifiwa na Mtakatifu Yohane Krisostomu mwenyewe. Yuliano alikuwa kijana wa ukoo mtukufu katika mji wa Tarso, Mkristo tangu ujana wake; na mateso yalipokuja, alikamatwa na kuletwa mbele ya gavana na kuamriwa atoe dhabihu kwa sanamu, na, akikataa, alimkiri Kristo kwa ujasiri.", "patron": "Vijana wanaomkiri Kristo; wanaovumilia mateso ya muda mrefu."},

"Martyr Julitta at Caesarea":
{"type": "Mlei wa kike · karne ya 4", "life": "Shahidi Mtakatifu Yulita aliishi Kaisaria katika Kapadokia wakati wa mateso chini ya mfalme Diokletiano. Mpagani fulani alipoitwaa mali yake yote naye akakata rufaa mahakamani atendewe haki, mshtakiwa wake alimsingizia mbele ya mwamuzi kuwa Mkristo, jambo lililomtoa nje ya ulinzi wa sheria.", "patron": "Maombezi yake huombwa kwa ajili ya uadilifu; kumpendelea Kristo kuliko mali."},

"Martyr Justin the Philosopher and those with him at Rome":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Yustino Mwanafalsafa alikuwa mmoja wa watetezi wa kwanza na wakuu kuliko wote wa Kikristo, mtafutaji wa kweli kupitia shule zote za falsafa ya kipagani aliyeipata mwishowe katika Kristo, naye akautia muhuri ushuhuda wake kwa damu yake huko Roma karibu mwaka wa 165.", "patron": "Wanafalsafa na watafutaji wa kweli; watetezi na walinzi wa imani."},

"Martyr Juvenal of Alaska":
{"type": "Mtawa kuhani · karne ya 18", "life": "Mheshimiwa Yuvenali, Shahidi wa Kwanza wa Amerika, alizaliwa mwaka wa 1761 huko Nerchinsk katika Siberia, na duniani alikuwa Yohane Feodorovich Hovorukhin, aliyefunzwa kuwa mhandisi wa migodi. Baada ya kifo cha mkewe aliingia katika maisha ya utawa, na akiwa mtawa kuhani wa Valaam alichaguliwa kwa utume wa kwanza wa Kiorthodoksi kwenda Amerika, akifika Kodiak mwaka wa 1794 pamoja na Mtakatifu Hermani na wenzao.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuangazwa kwa Amerika."},

"Martyr Laodicius the Keeper of the Prison":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Laodikio alikuwa mlinzi wa gereza ambamo bikira shahidi Glikeria alifungwa huko Heraklea katika Thrakia, na uongofu wake na taji yake vilikuwa tunda la ziara ya malaika katika chumba chake.", "patron": "Uponyaji wa malaika ulioaminiwa na kukiriwa."},

"Martyr Longinus of Asistavi":
{"type": "Shahidi · karne ya 1", "life": "Shahidi Mtakatifu Longino Akida anaadhimishwa siku hii katika kalenda ya Kigeorgia kwa jina la Longino Asistavi; kwa maana asistavi, mkuu wa mia, ni neno la Kigeorgia la akida, wala si mahali bali ni cheo cha shahidi katika lugha ya taifa lile la kale la Kikristo.", "patron": "Maombezi yake huombwa kwa ajili ya askari; magonjwa ya macho."},

"Martyr Longinus the Centurion, who stood at the Cross of the Lord":
{"type": "Shahidi · karne ya 1", "life": "Shahidi Mtakatifu Longino Akida alikuwa afisa wa Kirumi wa Kapadokia aliyetumika katika Yudea chini ya Pontio Pilato, na kikosi chake ndicho kilichokuwa kikilinda katika Kusulubiwa kwa Mwokozi juu ya Golgotha. Alipoona tetemeko la ardhi, jua lililotiwa giza, na maajabu yaliyoandamana na kifo cha Bwana, akida aliamini na akakiri mbele ya wote, Hakika huyu alikuwa Mwana wa Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya askari; magonjwa ya macho."},

"Martyr Lucian the Presbyter of Antioch":
{"type": "Kasisi · karne ya 4", "life": "Shahidi Mtakatifu Lukiano, kasisi wa Antiokia, alizaliwa Samosata na, akiachwa yatima akiwa mdogo, aliwapa maskini urithi wake na akajitoa mwenyewe kwa elimu takatifu, akiwa kasisi huko Antiokia na bwana wa shule yake maarufu ya Maandiko, ambako alijitaabisha katika kusahihisha maandishi ya Kiyunani ya Agano la Kale dhidi ya upotovu uliokuwa umeingia, na akawafunda wanafunzi wengi katika kujifunza kwa usahihi neno la Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya wasomi; watafsiri."},

"Martyr Lucillian and those who suffered with him at Byzantium":
{"type": "Mashahidi · karne ya 3", "life": "Shahidi Mtakatifu Lukiliano na wale walioteseka pamoja naye huko Bizanti walimshuhudia Kristo katika utawala wa mfalme Aureliano, katika karne ya tatu, na kikundi chao kiliunganisha mzee aliyeongoka katika uzee wake na vijana wanne na bikira mtakatifu.", "patron": "Walioongoka katika uzee; vijana wanaokiri pamoja."},

"Martyr Lupus":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Lupo alikuwa mtumishi mwaminifu wa Shahidi Mkuu Dimitri wa Thesalonike, naye alisimama kando ya bwana wake katika shahada yake. Akichovya upindo wa vazi lake na pete katika damu ya shahidi mkuu, aliviweka hivi kama hazina; na kwa vyo Bwana alitenda miujiza mingi katika Thesalonike, uponyaji ukitiririka kutoka damu ya Dimitri kwa mikono ya mtumishi wake, hata mji wote ukatikiswa.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi; utumishi wa uaminifu."},

"Martyr Lupus, slave of Saint Demetrius of Thessalonica":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Lupo aliishi mwanzoni mwa karne ya nne na alikuwa mtumishi mwaminifu wa Shahidi Mkuu Mtakatifu Dimitri wa Thesalonike. Akiwapo katika kifo cha bwana wake, alichovya vazi lake mwenyewe katika damu ya shahidi na akaichukua pete kutoka mkononi mwake.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Mamas of Caesarea in Cappadocia":
{"type": "Shahidi Mkuu · karne ya 3", "life": "Shahidi Mkuu Mtakatifu Mamas alizaliwa katika Paflagonia katika karne ya tatu, mwana wa Wakristo watukufu Theodoto na Rufina, waliotupwa gerezani Kaisaria ya Kapadokia kwa kumkiri Kristo; huko baba yake alikufa kabla hajateswa, na mama yake, akimzaa gerezani, alimkabidhi kwa Mungu na akaondoka katika maisha haya, hata mtoto mchanga akaachwa kati ya miili ya wazazi wake.", "patron": "Maombezi yake huombwa kwa ajili ya wachungaji; wachungaji wa mifugo."},

"Martyr Manetha of Cæsarea in Palestine":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Manetha aliteseka Kaisaria katika Palestina karibu mwaka wa 308, katika mateso chini ya Maksimino, akikamatwa pamoja na mashahidi watakatifu Antonino, Nikeforo na Germano, wanaokumbukwa pamoja naye siku hii. Akiwa bikira aliyewekwa wakfu kwa Kristo, alidhulumiwa kwa mateso mengi ili kuuvunja uthabiti wake.", "patron": "Maombezi yake huombwa kwa ajili ya usafi katika dhihaka."},

"Martyr Marinus":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Marino Askari aliteseka Kaisaria katika Palestina mwaka wa 262, na pambano lake, lililohifadhiwa na Eusebio wa mji ule, linategemea chaguo moja lililowekwa mbele yake kwa uwazi usiovumilika. Marino alikuwa askari mashuhuri wa ukoo mtukufu, na cheo cha akida kilipokuwa wazi, alisimama wa kwanza katika mstari wa kupandishwa.", "patron": "Maombezi yake huombwa kwa ajili ya askari kwenye njia panda ya dhamiri; Injili iliyochaguliwa kuliko upanga."},

"Martyr Marinus of Rome":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Marino alikuwa askari aliyeteseka Kaisaria katika Palestina katika karne ya tatu, na pambano lake lilitegemea kupandishwa cheo. Akiwa mashuhuri katika utumishi wake na wa pili katika mstari wa kupokea fimbo ya akida, alisingiziwa na mshindani wake kuwa Mkristo asiyeweza kukishika cheo kwa halali, kwa kuwa kupandishwa kulihitaji kiapo cha desturi kwa miungu ya kipagani na dhabihu kwa sanamu.", "patron": "Maombezi yake huombwa kwa ajili ya askari; maofisa wanaokabili viapo vya kupandishwa cheo."},

"Martyr Marinus the Elder at Anazarbus":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Marino Mzee aliteseka kwa ajili ya Kristo huko Anazarbo katika Kilikia katika utawala wa Diokletiano, akiwa tayari mkubwa kwa miaka mateso yalipomkuta. Alipoletwa mbele ya gavana Lisia, mzee alihimizwa aziepushe mvi zake na atoe dhabihu, lakini alijibu kwamba wingi wa siku ulikuwa umemthibitisha tu katika kumjua Mungu wa kweli, na kwamba hangemkana jioni ya maisha yake Bwana aliyemtumikia tangu asubuhi.", "patron": "Maombezi yake huombwa kwa ajili ya wazee; ujasiri katika uzee."},

"Martyr Marinus, his wife Martha, their children, and those with them at Rome":
{"type": "Walei · karne ya 3", "life": "Siku hii inawakumbuka mashahidi watakatifu Marino, mkewe Martha, na wanawe Audifaksi na Habakuki, pamoja na wengine walioteseka nao huko Roma chini ya mfalme Klaudio wa Pili. Jamaa yenye uchaji Mungu kutoka Persia, walisafiri hadi Roma ili kuyaheshimu makaburi ya mitume Petro na Paulo, na huko walijitoa kwa utumishi wa Kanisa lililoteswa, wakikusanya usiku miili ya mashahidi waliouawa na kuizika kwa heshima, hata wakiuopoa kutoka Tiber mwili wa shahidi Kireno.", "patron": "Maombezi yao huombwa kwa ajili ya Familia za Kikristo; kuwazika wafu."},

"Martyr Markella of Chios":
{"type": "Bikira · karne ya 14", "life": "Shahidi Mtakatifu Markella aliishi katika kijiji cha Volisso katika kisiwa cha Kio. Wazazi wake walikuwa wacha Mungu na miongoni mwa matajiri kuliko wote wa kijiji, na mama yake alipokufa akiwa kijana, baba yake, mkuu wa mahali pale, aliusimamia ulezi wake; alikua akiwa mnyenyekevu na safi, akiepuka mikusanyiko ambayo ingeweza kumdhuru kiroho.", "patron": "Maombezi yake huombwa kwa ajili ya usafi; ulinzi wa usafi."},

"Martyr Matrona of Thessalonica":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Matrona wa Thesalonike alikuwa mtumwa katika nyumba ya Pautila, aandikwaye Pantila katika habari za Kigiriki, mwanamke Myahudi wa cheo, mke wa jemadari wa mji ule, na shahada yake ilitimizwa yote ndani ya kuta za nyumba moja, bila mahakama, gavana wala amri, mateso yakipunguzwa hadi kipimo chake kidogo na cha karibu kuliko vyote, bibi na msichana mtumishi.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi na waliokuwa watumwa; wanaoadhibiwa kwa sala zao."},

"Martyr Meletius Stratelates who suffered in Galatia, and those with him":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Meletio Jemadari, aitwaye Stratelati, aliteseka pamoja na kikosi kikubwa cha wenzake katika Galatia ya Asia Ndogo katika utawala wa mfalme Antonino Pio, katika karne ya pili, na mateso yake ni mojawapo ya shahada kubwa za makundi katika kalenda, uongozi mzima ukivikwa taji pamoja.", "patron": "Mashetani waliofukuzwa kutoka mahekalu."},

"Martyr Menas of Egypt":
{"type": "Shahidi Mkuu · karne ya 4", "life": "Shahidi Mkuu Mtakatifu Mena alikuwa Mmisri na askari, aliyetumika katika Frigia huko Kotieo; na amri za Diokletiano zilipowaamuru wote watoe dhabihu kwa sanamu, aliuweka kando mshipi wake wa kijeshi badala ya kumkana Kristo, na akajiondoa milimani, ambako katika kufunga na sala alijiandaa kwa vita kubwa zaidi.", "patron": "Maombezi yake huombwa kwa ajili ya askari; wafanyabiashara."},

"Martyr Mercurius of Smolensk":
{"type": "Shahidi · karne ya 13", "life": "Shahidi Mtakatifu Merkurio wa Smolensk, mpiganaji wa asili tukufu kutoka nchi za magharibi aliyetumika katika jeshi la Smolensk, alikuwa mtu wa sala ya siri na wa maisha makali; na mwaka wa 1239, makundi ya Batu, baada ya kuizamisha Urusi katika damu, yalipoukaribia mji na kupiga kambi huko Dolgomostye, Mzazi-Mungu mwenyewe alimwinua mtetezi wake.", "patron": "Maombezi yake huombwa kwa ajili ya askari; watetezi wa miji."},

"Martyr Michael, Prince of Tver":
{"type": "Mkuu · karne ya 14", "life": "Shahidi Mtakatifu Mikaeli, Mkuu Mkubwa wa Tver, aliitawala nchi yake katika zama chungu za nira ya Watatari, wakati wakuu wa Urusi walipogombania upendeleo wa khani na watu wakalipia kila ugomvi. Akiwa mnyofu, mwenye sala na mpendwa wa mji wake, Mikaeli aliupokea ukuu mkubwa kwa haki ya ukubwa wa umri.", "patron": "Maombezi yake huombwa kwa ajili ya watawala; watawala wanaokufa kwa ajili ya watu wao."},

"Martyr Mirax of Egypt":
{"type": "Shahidi · karne ya 7", "life": "Shahidi Mtakatifu Miraksi wa Misri ndiye shahidi wa nafasi ya pili, na taji yake ni taji ya toba. Akizaliwa Tennis katika Misri kwa wazazi Wakristo wacha Mungu katika miaka baada ya ushindi wa Wasaraseni, alianguka katika ujana wake: mbele ya amiri alimkana Kristo, akaikubali dini ya washindi, na akaishi miaka katika kukana kwake, huku baba yake na mama yake, wakikataa kumkataa na kukata tamaa juu yake, wakiizingira mbingu kwa sala na machozi kwa ajili ya mwana wao.", "patron": "Maombezi yake huombwa kwa ajili ya toba baada ya kuikana imani; kurudi kwa waliokana."},

"Martyr Myron the Presbyter of Cyzicus":
{"type": "Kasisi · karne ya 3", "life": "Shahidi Mtakatifu Miro alikuwa kasisi katika Akaya, mtu wa asili tajiri na tukufu aliyekuwa hata hivyo mpole na mwema kwa wote, mpenzi wa Mungu na wa jirani yake, na jasiri katika kulitetea kundi lake. Aliteseka mwaka wa 250, katika mateso chini ya Desio, wakati katika sikukuu ya Kuzaliwa kwa Kristo gavana Antipatro alipopasua ndani ya kanisa wakati wa ibada ili kuwakamata Wakristo, na Mtakatifu Miro akamkemea kwa ujasiri kwa kuinajisi ibada ya Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya utetezi wa kundi."},

"Martyr Nectan of Hartland":
{"type": "Kuhani Shahidi · karne ya 6", "life": "Mheshimiwa Nektan wa Hartland alikuwa mtawa wa upweke wa Kikelti na shahidi wa karne ya sita, anayeheshimiwa katika Nchi ya Magharibi ya Britania, ambaye maisha yake ni ya jamaa ile kubwa ya watakatifu wa Kanisa la Kikelti walioziacha nchi zao ili kumtafuta Mungu katika upweke.", "patron": "Wapweke na waliojitenga peke yao; wanaobeba vichwa vyao wenyewe."},

"Martyr Nestor of Thessalonica":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Nestori wa Thesalonike alikuwa kijana Mkristo, mzuri kwa sura na aliyejulikana na Shahidi Mkuu Dimitri, aliyekuwa amemfundisha imani. Mfalme Maksimiano alipofanya michezo mjini, shujaa wake, Mvandali mkubwa aliyeitwa Lieo, aliwatupa wapinzani mmoja baada ya mwingine kutoka jukwaa refu juu ya mikuki iliyoelekezwa juu, kwa furaha ya mfalme na kwa maangamizi ya wengi, miongoni mwao Wakristo waliolazimishwa uwanjani.", "patron": "Maombezi yake huombwa kwa ajili ya askari; wanariadha."},

"Martyr Nicander of Egypt":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Nikanda wa Misri alikuwa tabibu, na katika mateso ya Diokletiano aliigeuza kazi yake kuwa huduma maradufu ambayo amri zilikuwa zimeifanya kosa la kuadhibiwa kwa kifo mara mbili: aliwatembelea Wakristo waliofungwa, akitibu majeraha yao ya mateso, akiwaletea chakula na faraja katika magereza ambamo himaya ilikusudia waoze kati ya mahojiano.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; wanaozika wafu."},

"Martyr Nikon and 199 disciples with him in Sicily":
{"type": "Kuhani Shahidi · karne ya 3", "life": "Mheshimiwa Nikoni, Askofu na Shahidi, pamoja na wanafunzi wake mia moja tisini na tisa waliteseka katika Sisilia katika mateso ya Desio, karibu mwaka wa 251, na njia yake kwenda katika kikundi kile ilianza jeshini. Akiwa askari kwa kazi, mwana wa baba mpagani na mama Mkristo, Nikoni alikwenda vitani bila kubatizwa lakini si bila kufundishwa, kwa maana mama yake alikuwa amepanda mbegu ya imani ndani yake.", "patron": "Maombezi yao huombwa kwa ajili ya maaskofu pamoja na makundi yao; walimu na wanafunzi wao."},

"Martyr Onesimus of Isauria":
{"type": "Shahidi · karne ya 1", "life": "Shahidi Mtakatifu Onesimo, aitwaye pia Onisio, amehesabiwa miongoni mwa mashahidi wa mwanzo wa Kristo waliotia muhuri ukiri wao kwa damu yao kwa upanga. Habari zilizobaki juu yake ni fupi kabisa, wala hazikubaliani kabisa hata juu ya nchi yake, kwa maana ingawa anaadhimishwa katika kalenda kama Onesimo wa Isauria, na kuwekwa kando ya shahidi Konon wa eneo lile, ambaye wimbo wake unaunganisha majina yao mawili, Maisha ya Watakatifu ya Kanisa la Kiorthodoksi katika Amerika yanaandika tu kwamba aliishi Palestina.", "patron": "Maombezi yake huombwa kwa ajili ya imara chini ya mahojiano; ukiri uliotiwa muhuri kwa upanga."},

"Martyr Orestes, Physician of Cappadocia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Oreste Tabibu aliishi Tiana katika Kapadokia katika utawala wa Diokletiano, mponyaji msomi na stadi wa miili na, tangu utoto, Mkristo wa kweli. Afisa Maksimino alipotumwa Tiana kuikandamiza imani, Oreste alikuwa miongoni mwa wa kwanza kuletwa mahakamani, naye akamkiri waziwazi Bwana Aliyesulubiwa na Aliyefufuka, bila kutikiswa na utajiri na heshima alizopewa.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; uponyaji."},

"Martyr Pancharius at Nicomedia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Pankario alikuwa Mrumi wa hadhi kubwa, kipenzi cha mfalme Maksimiano, na Mkristo; na pambano lake ni la thamani kwa Kanisa kwa sababu linaanza kwa kuanguka. Mateso yalipofanya imani na upendeleo visipatane, Pankario, asiyetaka kupoteza nafasi yake kando ya mfalme, aliuficha na kwa kweli akaukana Ukristo wake, akiishika ikulu na kumwachilia Kristo, ukanaji tulivu wa manufaa usioacha kovu lionekanalo kwa nje.", "patron": "Maombezi yake huombwa kwa ajili ya waliokana na wangependa kurudi; wana walio mbali na nyumbani."},

"Martyr Papas of Lyconia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Papas wa Likaonia aliteseka katika mateso mwanzoni mwa karne ya nne, wakati amri za Diokletiano na Maksimiano zilipoingia hadi nyanda za juu za Asia Ndogo ya ndani ambako Paulo na Barnaba walikuwa wamelipanda neno kwanza; na pambano la Papas linakumbukwa kwa barabara yake na mti wake.", "patron": "Maombezi yake huombwa kwa ajili ya waliosukumwa kupita uwezo wao wa kuvumilia; maandamano katika viatu vyenye misumari."},

"Martyr Paramon and 370 Martyrs in Bithynia":
{"type": "Mashahidi · karne ya 3", "life": "Shahidi Mtakatifu Paramoni na mashahidi mia tatu na sabini pamoja naye waliteseka katika Bithinia mwaka wa 250, katika mateso chini ya Desio. Mtawala Akilino, akija kwenye chemchemi za maji ya moto za sehemu zile, alikuwa na Wakristo wengi waliofungwa pamoja naye, mia tatu na sabini kwa idadi.", "patron": "Maombezi yao huombwa kwa ajili ya usemi usiokubali kunyamaza mbele ya dhuluma."},

"Martyr Paraskevi of Rome":
{"type": "Mtawa wa kike · karne ya 2", "life": "Mheshimiwa Paraskevi wa Roma, Bikira Shahidi, alikuwa binti pekee wa wazazi Wakristo wacha Mungu huko Roma, na tangu miaka yake ya mwanzo alijitoa kwa sala na kujifunza Maandiko matakatifu. Wazazi wake walipokufa aliwagawia maskini urithi wake na akauweka wakfu ubikira wake kwa Kristo, na katika kuwaiga mitume alikwenda huku na huku akiihubiri Injili na akiwageuza wapagani wengi kutoka sanamu zao.", "patron": "Maombezi yake huombwa kwa ajili ya magonjwa ya macho; wagonjwa."},

"Martyr Pausilippus of Heraclea in Thrace":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Pausilipo aliteseka Heraklea katika Thrakia katika utawala wa mfalme Hadriano, kati ya mwaka wa 117 na 138, katika kizazi ambacho mateso hayakuendeshwa kwa amri kubwa bali kwa dhoruba za mahali, bidii ya gavana au kinyongo cha mji kikitosha kuyajaza magereza.", "patron": "Maombezi yake huombwa kwa ajili ya wanaokufa kwa majeraha yao; wakiri nje ya uwanja."},

"Martyr Peter the Aleut":
{"type": "Shahidi · karne ya 19", "life": "Shahidi Mtakatifu Petro Mwaleuti alikuwa mzaliwa kijana wa eneo la Kodiak katika Alaska, aliyebatizwa katika imani ya Kiorthodoksi na wamisionari Warusi na kuajiriwa pamoja na wenzake wa nchi yake katika vikundi vya uwindaji vya koloni. Mwaka wa 1815 alitekwa pamoja na Waaleuti wengine na askari wa Kihispania katika California, na huko wafungwa walishinikizwa kuuacha Uorthodoksi kwa imani ya Kilatini.", "patron": "Maombezi yake huombwa kwa ajili ya wawindaji; wenyeji wa nchi."},

"Martyr Phaedrus":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Fedro anakumbukwa siku hii pamoja na Shahidi Filoumeno wa Ankira, katika kikundi cha wale walioteseka katika Galatia katika mateso chini ya mfalme Aureliano, karibu mwaka wa 274. Sinaksario za Kigiriki zinaandika namna ya pambano lake: akikataa kumkana Kristo, aliuawa kwa kumiminiwa lami inayochemka juu ya mwili wake, na hivyo, akiungua mwilini lakini bila kuunguzwa rohoni, aliitoa roho yake kwa Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya waamini wasioandikwa katika kumbukumbu."},

"Martyr Philetus the Senator, his wife and sons, and those with them in Illyria":
{"type": "Mashahidi · karne ya 2", "life": "Mashahidi Watakatifu Fileto Seneta, mkewe Lidia, wanawe Makedoni na Theoprepio, Amfilokio jemadari, na Kronide karani waliteseka katika utawala wa mfalme Hadriano, mwanzoni mwa karne ya pili, na pambano lao ni mojawapo ya yale ambayo Kanisa linayakumbuka kwa upole wa ajabu wa mwisho wake.", "patron": "Maombezi yao huombwa kwa ajili ya familia zinazokiri pamoja; maofisa walioongoka."},

"Martyr Philosophus at Alexandria":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Filosofo aliteseka kwa ajili ya Kristo huko Aleksandria katika mateso ya mfalme Desio, karibu mwaka wa 250, na pambano lake lilikuwa la namna adimu na ya kutisha, vita si dhidi ya upanga bali dhidi ya mwili, ambamo alishinda kwa kuyageuza maumivu yake mwenyewe dhidi ya wajaribu wake.", "patron": "Jaribu la mwili lililoshindwa kwa jeraha."},

"Martyr Philoumenus of Ancyra":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Filoumeno aliteseka kwa ajili ya Kristo mwaka wa 274, katika mateso chini ya mfalme Aureliano. Akiwa mzaliwa wa Likaonia na mwokaji kwa kazi, aliipatia mikate miji ya Galatia, akichuma riziki yake kwa uaminifu na akimkiri Kristo waziwazi; na watu wenye wivu walimsingizia kwa gavana Feliki huko Ankira kuwa Mkristo.", "patron": "Maombezi yake huombwa kwa ajili ya waokaji mikate; wafanyabiashara."},

"Martyr Photini the Samaritan Woman, her sons, and those with them":
{"type": "Shahidi · karne ya 1", "life": "Shahidi Mtakatifu Fotina ndiye mwanamke Msamaria aliyezungumza na Kristo kwenye kisima cha Yakobo. Baada ya Pentekoste aliihubiri Injili pamoja na jamaa yake na wenzake. Alipokamatwa chini ya Nero, alimkiri Kristo mbele ya mfalme. Baada ya mateso makali, wanawe na mashahidi wenzake waliteseka pamoja naye, naye akapokea taji la shahidi katika karne ya kwanza."},

"Martyr Platon of Ancyra":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Platoni aliteseka Ankira katika Galatia mwanzoni mwa karne ya nne, kijana wa nyumba ya Kikristo na ndugu wa shahidi Antioko. Akizunguka mjini kwa ujasiri, aliwafundisha wenzake wa mji kuzidharau sanamu na kumjua Mungu wa kweli, na kwa ajili hiyo alikamatwa na kuletwa mbele ya gavana Agripino.", "patron": "Maombezi yake huombwa kwa ajili ya vijana; kukataa kila mapatano dhidi ya Kristo."},

"Martyr Polycarp of Alexandria":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Polikarpo wa Aleksandria aliteseka mwanzoni mwa karne ya nne, katika mateso makuu chini ya Maksimiano, na pambano lake ni la kikundi cha wale ambao kuuona ukatili wenyewe kuliwasukuma uwanjani. Alipoona katika Aleksandria ushenzi ambao kwao wakiri wa Kristo walikuwa wakiteswa, wasio na hatia wakiteswa, hakuweza kunyamaza.", "patron": "Maombezi yake huombwa kwa ajili ya wanaosema dhidi ya ukatili; watesi waliokemewa uso kwa uso."},

"Martyr Potitus at Naples":
{"type": "Mlei · karne ya 2", "life": "Shahidi Mtakatifu Potito aliteseka katika karne ya pili chini ya mfalme Antonino Pio. Akiijua imani ya Kikristo akiwa mvulana, alibatizwa akiwa na miaka kumi na mitatu, na baba yake mpagani alipotaka kwanza kwa ushawishi na kisha kwa vitisho kumgeuza kutoka kwa Kristo, baba mwenyewe alishindwa na uthabiti wa mwanawe na akawa Mkristo.", "patron": "Maombezi yake huombwa kwa ajili ya wagonjwa; ukombozi kutoka mashetani."},

"Martyr Quadratus and those with him at Corinth":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Kuadrato wa Korintho alizaliwa jangwani na akalelewa na mbingu yenyewe: wakati wa mateso ya karne ya tatu mama yake, mwanamke mcha Mungu aliyeitwa Rufina, alikimbia kutoka Korintho hadi milimani ili kuwaepuka waliokuwa wakimwinda, na huko akamzaa mwana na akafa punde baadaye.", "patron": "Maombezi yake huombwa kwa ajili ya madaktari; mayatima."},

"Martyr Quadratus and those with him at Nicomedia":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Kuadrato wa Nikomedia aliteseka pamoja na Saturnino, Rufino na wengine katika mateso ya mfalme Desio na mrithi wake Valeriano. Akitoka katika jamaa mashuhuri na akiwa na utajiri mkubwa, Kuadrato hakuizuia mali yake kwa ajili ya Kristo, bali aliitumia kwa waliofungwa: magereza ya Nikomedia yalipojaa Wakristo, aliwaendea waziwazi, akiwahonga walinzi ili aingie, akiwapatia wafungwa mahitaji yao, akiwafunga majeraha yao, na zaidi ya yote akiziimarisha roho zao kwa pambano lililokuwa mbele, tajiri akiugeuza utajiri wake kuwa ujasiri kwa maskini.", "patron": "Maombezi yake huombwa kwa ajili ya wageni wa wafungwa; matajiri wanaojitoa wenyewe."},

"Martyr Romanus the Deacon of Caesarea":
{"type": "Shemasi · karne ya 4", "life": "Shahidi Mtakatifu Romano, shemasi wa kanisa la Kaisaria katika Palestina, alikuwa Antiokia mateso ya Diokletiano yalipouvunjikia mji ule; na akiwaona Wakristo wakimiminika kwa hofu kuelekea sikukuu ya kipagani ili kuyaokoa maisha yao kwa dhabihu, alisimama malangoni na akawapazia sauti wamkumbuke Kristo, akiwarudisha wengi kutoka kuikana imani katika kizingiti chenyewe cha hekalu.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wahubiri."},

"Martyr Romulus and with him many others":
{"type": "Mashahidi · karne ya 2", "life": "Shahidi Mtakatifu Romulo aliishi katika utawala wa mfalme Trayano na alishika cheo cha juu katika baraza la kifalme. Mfalme, akipigana vita Mashariki, alipoamuru Wakristo waliokuwa wakitumika katika majeshi yake wahesabiwe, walipatikana elfu kumi na moja, naye akaamuru wote wavuliwe vyeo vyao na kupelekwa uhamishoni Armenia.", "patron": "Maombezi yao huombwa kwa ajili ya askari."},

"Martyr Sabinus (Abibus) of Egypt":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Sabino, aitwaye pia Abibo, alikuwa mtu mashuhuri wa Hermopoli katika Misri, wa hadhi kubwa na aliyejulikana kwa sadaka zake; na mateso yalipoliangukia kanisa la Misri katika utawala wa Diokletiano, Wakristo wa mji walimsihi ajihifadhi, na Sabino akajiondoa pamoja na wenzake wachache hadi kibanda nje ya mji, ambako walibaki wamejificha, wakijilisha kwa sala na kufunga huku dhoruba ikipita katika Hermopoli.", "patron": "Maombezi yake huombwa kwa ajili ya waliosalitiwa; wafadhili waliolipwa kwa uovu."},

"Martyr Sabinus of Egypt":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Sabino wa Misri, ambaye kalenda za Kigiriki zinamkumbuka siku hii na za Kislavoni tarehe kumi na tatu ya Machi, alikuwa raia mashuhuri wa Hermopoli, aliyeheshimiwa mjini na mkarimu kwa maskini wake; na mateso ya utawala wa Diokletiano yalipoivunjikia Misri, Wakristo wa Hermopoli walimshawishi ajihifadhi kwa ajili ya kundi, na Sabino akajiondoa pamoja na wenzake wachache hadi kibanda nje ya mji, ambako walibaki wamejificha katika kufunga na sala isiyokoma huku mahakama zikiwashughulikia wakiri wa mji.", "patron": "Maombezi yake huombwa kwa ajili ya waliosalitiwa; wafadhili waliolipwa kwa uovu."},

"Martyr Savva Stratelates “the General” of Rome, and 70 soldiers with him":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Sava Stratelati, Jemadari, alikuwa Mgothi kwa asili aliyepanda katika utumishi wa Kirumi hadi cheo cha jemadari wa jeshi chini ya mfalme Aureliano, na aliishi ndani ya kazi ile maisha ambayo cheo hakikutengenezwa kuyabeba: akiwa Mkristo tangu ujana wake, aliyashika maagizo kwa usahihi wa askari, aliwapa wahitaji, na akayafanya magereza kituo chake cha pili, akiwatembelea wakiri katika minyororo yao, akiwapatia mahitaji yao, na akiwaimarisha kwa mapambano yao, jemadari akiyakagua majeshi ya Kanisa kwa moyo uleule aliokagua ya himaya.", "patron": "Maombezi yake huombwa kwa ajili ya majemadari; wageni wa gerezani."},

"Martyr Sebastian at Rome, and his companions":
{"type": "Mashahidi · karne ya 3", "life": "Shahidi Mtakatifu Sebastiano na wenzake waliteseka Roma mwaka wa 288, chini ya Diokletiano. Sebastiano, jemadari katika walinzi wa ikulu, akiheshimiwa na wafalme na akiwa Mkristo kwa siri, alikitumia cheo chake kama ngao ya Kanisa.", "patron": "Maombezi yao huombwa kwa ajili ya askari; wapiga mishale."},

"Martyr Serapion":
{"type": "Mlei · karne ya 3", "life": "Shahidi Mtakatifu Serapioni aliteseka kwa ajili ya Kristo katika mateso chini ya mfalme Severo. Akiletwa mbele ya gavana Akile na kuamriwa aikane imani yake, alijitangaza kwa uthabiti kuwa Mkristo na akamkiri Mungu wa kweli mbele ya wapagani, na kwa ajili hiyo alidhulumiwa kwa mateso yasiyo ya kibinadamu na akatupwa gerezani.", "patron": "Inaadhimishwa katika kalenda takatifu ya Kanisa."},

"Martyr Severian of Sebaste":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Severiano, mtukufu wa Sebaste katika Armenia, aliteseka kwa ajili ya Kristo mwaka wa 320, katika mateso chini ya mfalme Likinio. Mashahidi Arobaini wa Sebaste walipokuwa wamelala gerezani kwa ukiri wao wa Kristo, Severiano aliwaonyesha huruma ya wazi na isiyo na hofu, akiwatembelea katika minyororo yao, akiitia moyo roho zao, na akiwaimarisha kwa pambano lao juu ya ziwa lililoganda.", "patron": "Maombezi yake huombwa kwa ajili ya kuwatunza wafungwa; ukiri thabiti."},

"Martyr Solomonia, mother of the Holy Seven Maccabee Martyrs":
{"type": "Mama · karne ya 2 KK", "life": "Shahidi Mtakatifu Salomonia alikuwa mama wa ndugu saba Wamakabayo walioteseka chini ya Antioko Epifane kwa uaminifu wao kwa Sheria ya Mungu. Badala ya kuwashauri wanawe wayaokoe maisha yao kwa kulivunja agano, mama huyu shujaa aliwatia moyo kila mmoja wao abaki mwaminifu kwa Mungu hata mbele ya kifo, na kwa ujasiri uliopita maumbile yake aliwatazama wote saba wakifa katika siku moja, akiwahimiza wavumilie.", "patron": "Maombezi yake huombwa kwa ajili ya mama; ujasiri."},

"Martyr Sophia and her three daughters at Rome":
{"type": "Mashahidi · karne ya 2", "life": "Shahidi Mtakatifu Sofia na binti zake watatu wachanga, Imani, Tumaini na Upendo, waliteseka Roma karibu mwaka wa 137, katika utawala wa mfalme Hadriano. Sofia, ambaye jina lake lina maana ya Hekima, alikuwa mjane Mkristo aliyewapa binti zake majina ya fadhila tatu kuu na akawalea katika upendo wa moto kwa Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya mama."},

"Martyr Sozon of Cilicia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Sozoni, mzaliwa wa Likaonia aliyeitwa Tarasio kabla ya ubatizo wake, alikuwa mchungaji aliyeishi mwishoni mwa karne ya tatu, akijifunza Maandiko matakatifu alipokuwa akilichunga kundi lake na akistaajabia upole wa kondoo zake, aliojitahidi kuuiga na kuuzidi.", "patron": "Maombezi yake huombwa kwa ajili ya wachungaji."},

"Martyr Stephanida of Damascus":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Stefanida aliteseka Damasko katika karne ya pili, katika mateso chini ya Marko Aurelio. Akiwa mwanamke kijana Mkristo wa asili ya Kihispania na mke wa askari, alisimama kati ya watazamaji wakati Shahidi mtakatifu Viktori alipoteswa; na alipoiona neema ya Mungu iliyomtegemeza, aliona, kama habari isimuliavyo, taji mbili zikishuka kutoka mbinguni, moja kwa Viktori na moja kwa ajili yake mwenyewe, naye akapaza sauti waziwazi, akimbariki shahidi na akijikiri kuwa Mkristo.", "patron": "Maombezi yake huombwa kwa ajili ya wake vijana; ushuhuda uliowashwa kwa ushuhuda."},

"Martyr Susanna, Queen of Georgia":
{"type": "Shahidi · karne ya 5", "life": "Shahidi Mtakatifu Shushanik, aitwaye Susana, alikuwa mke wa Varsken, mtawala wa Hereti katika Georgia ya mashariki, naye alikuwa amelelewa tangu utoto katika jamaa yenye uchaji Mungu ya Kikristo. Mume wake alipokwenda kwa mfalme wa Persia na huko akamkana Kristo ili kuuabudu moto, akiahidi kuwageuza mkewe na watoto atakaporudi, Shushanik alichomwa moyoni.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti; wanaoteswa na jamaa kwa ajili ya imani."},

"Martyr Tathuil, and his sister, Bebaia":
{"type": "Mashahidi · karne ya 2", "life": "Mashahidi Watakatifu Tathuil na dada yake Bebaia waliteseka kwa ajili ya Kristo huko Edesa katika siku za mfalme Hadriano, kwa ajili ya kuhubiri kwao kwa ujasiri na kwa matunda Injili kati ya wapagani. Tathuil, ambaye habari nyingine zinamwita Thifaeli, alikuwa amegeuka kutoka utumishi wa sanamu kwa Mungu wa kweli, na kwa maneno yake wengi waliletwa kwenye imani.", "patron": "Maombezi yao huombwa kwa ajili ya mahubiri ya ujasiri; ukiri thabiti."},

"Martyr Tation (Tatio) of Claudiopolis":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Tatio aliishi katika Bithinia na aliteseka kwa ajili ya Kristo katika mateso chini ya Diokletiano. Ilipojulikana kwamba yeye ni Mkristo, alikamatwa na kuletwa katika mji wa Klaudiopoli mbele ya gavana Urbano, aliyemhimiza mara nyingi amkane Kristo na, aliposhindwa, akamtupa gerezani na kumdhulumu kwa mateso mbalimbali, akimpiga kwa fimbo.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Terence and 40 others beheaded at Carthage":
{"type": "Mashahidi · karne ya 3", "life": "Shahidi Mtakatifu Terentio na wenzake arobaini waliteseka Karthago katika mateso ya Desio, karibu mwaka wa 250, na wao ndio ukumbusho mkuu wa kikundi cha Kiafrika ambacho Kanisa linakikumbuka pia mwezi wa Machi; kalenda zinahifadhi majina ya viongozi, Terentio, Afrikano, Maksimo, Pompeio, na pamoja nao Zeno, Aleksandro, Theodoro na Makario, na zinahesabu mavuno yote kuwa zaidi ya taji arobaini.", "patron": "Maombezi yao huombwa kwa ajili ya vikundi vya wakiri; wafungwa."},

"Martyr Theodota and her three sons in Bithynia":
{"type": "Mlei wa kike · karne ya 4", "life": "Shahidi Mtakatifu Theodota na wanawe watatu wachanga waliteseka wakati wa mateso chini ya Diokletiano. Akiwa Mkristo na mjane wa Nikea katika Bithinia, aliishi maisha ya uchaji Mungu na akawalea wanawe katika imani, naye alikuwa rafiki wa karibu wa kiroho wa Mtakatifu Anastasia. Mateso yalipoinuka na wanawake watakatifu wakakamatwa, afisa Leukadio, akivutwa na uzuri wa Theodota, alimchukua nyumbani kwake akikusudia kumwoa.", "patron": "Maombezi yake huombwa kwa ajili ya mama; usafi."},

"Martyr Theodota at Nicea":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Theodota aliteseka kwa ajili ya Kristo huko Nikea katika Bithinia karibu mwaka wa 230, katika utawala wa mfalme Aleksanda Severo. Akishtakiwa kuwa Mkristo, alitupwa gerezani na akashikwa kwa muda mrefu, na alipoletwa mahakamani alimkiri Bwana wake bila kusita.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti."},

"Martyr Theodotus of Ancyra, and with him the seven Virgin Martyrs: Alexandra, Tecusa, Claudia, Phaine, Euphraisa, Matrona, and Julia, who suffered under Decius":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Theodoto na Mabikira saba watakatifu Aleksandra, Tekusa, Klaudia, Faine, Efrasia, Matrona na Yulia waliteseka Ankira katika Galatia katika mateso makuu ya mwanzoni mwa karne ya nne, na habari zao zilizounganishwa ni miongoni mwa zinazogusa moyo kuliko zote katika kalenda.", "patron": "Masalia ya mashahidi yaliyookolewa na kuzikwa."},

"Martyr Thomais of Alexandria":
{"type": "Shahidi · karne ya 5", "life": "Shahidi Mtakatifu Thomai wa Aleksandria alikuwa mwanamke kijana aliyeolewa wa mji ule, aliyelelewa katika uchaji Mungu na kuolewa na mvuvi, na shahada yake ilimjia si kutoka himaya bali kutoka ndani ya nyumba yake mwenyewe. Usiku mmoja mumewe alipokuwa ameenda kuvua, baba yake mkwe, kwa msukumo wa shetani na akitekwa na uzuri wake, alijaribu kumvuta mkwewe katika dhambi.", "patron": "Maombezi yake huombwa kwa ajili ya walioshambuliwa; wake."},

"Martyr Timothy the Reader and his wife, Maura, in Egypt":
{"type": "Shahidi · karne ya 4", "life": "Mashahidi Watakatifu Timotheo na Maura, mume na mke, waliteseka katika Thebaida ya Misri katika mateso makuu, mwaka wa 304 kama sinaksario ya Kimelkiti ihesabuvyo, au karibu 286 kama vitabu vingine vihesabuvyo, na pambano lao ni picha ya Kanisa iliyo laini kuliko zote ya ndoa iliyokamilishwa katika damu.", "patron": "Vitabu vilivyonyimwa moto."},

"Martyr Troadius of Neocaesarea":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Troadio wa Neokaisaria aliteseka katika mateso ya Desio, karibu mwaka wa 250, kijana wa mji ule wa Ponto ambaye pambano lake ni mashuhuri si kwa kumbukumbu yake yenyewe kuliko kwa hadhira yake, kwa maana Kanisa linamjua Troadio hasa kwa macho ya mtakatifu aliyemtazama kutoka maili nyingi mbali.", "patron": "Maombezi yake huombwa kwa ajili ya vijana katika jaribu; wanaotegemezwa na sala isiyoonekana."},

"Martyr Trophimus and 14 Others in Lycia":
{"type": "Walei · karne ya 4", "life": "Mashahidi Watakatifu Trofimo, Theofilo na wengine kumi na watatu pamoja nao waliteseka kwa ajili ya Kristo katika Likia wakati wa mateso chini ya mfalme Diokletiano. Wakiletwa mahakamani, walijikiri kwa ujasiri kuwa Wakristo na wakakataa kutoa dhabihu kwa sanamu, na baada ya kudhulumiwa kwa mateso makali miguu yao ilivunjwa nao wakatupwa motoni.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyr Tryphaίnē at Cyzicus":
{"type": "Shahidi · karne ya 1", "life": "Shahidi Mtakatifu Trifaina wa Kizikos, mji ulio kwenye Helesponti, alikuwa binti wa seneta Anastasio na mkewe mcha Mungu Sokratia, na alilelewa katika uchaji Mungu ambao pambano lake liliufanya wa hadharani; kwa maana mateso yalipoupata mji na akawaona wanyonge miongoni mwa Wakristo wakitetemeka kuelekea kukana, Trifaina hakungoja apatikane bali aliikiri imani yake kwa ujasiri na waziwazi, akimtangaza Kristo na ushindi wa mwisho wa kweli yake ili hasa kuwaimarisha waliositasita, roho imara ikijitolea kuwa mfano ambao waoga waliuhitaji.", "patron": "Maombezi yake huombwa kwa ajili ya mama wanaonyonyesha; wanawake wanaowatia nguvu wanyonge."},

"Martyr Tryphon of Lampsacus Near Apamea in Syria":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Trifoni alizaliwa katika kijiji cha Kampsada karibu na Apamea katika Frigia, mvulana mkulima aliyechunga bata bukini; na juu ya mponyaji huyu asiye na vyeti kuliko wote wa Kanisa Bwana alimwaga tangu miaka ya mapema nguvu ya kuwafukuza mashetani na kuponya kila ugonjwa. Maajabu yake yalikuwa na kipimo cha ukarimu wake: aliliokoa eneo lake la kuzaliwa na njaa kwa kuyageuza kwa sala makundi ya nzige yaliyokuwa yakiila nafaka, mchunga bata akiwaamuru waharibifu wa mashamba.", "patron": "Maombezi yake huombwa kwa ajili ya wakulima wa bustani; wakulima."},

"Martyr Urpasianus of Nicomedia":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Urpasiano aliteseka katika mji wa Nikomedia chini ya mfalme Maksimiano Galerio, aliyewatesa kwa ukatili Wakristo waliokuwa wakitumika katika jeshi lake na katika baraza lake; na katika kupepetwa kule, kama Maisha ya Watakatifu yaandikavyo, baadhi ya waoga wa roho walianza kusitasita na kuiabudu miungu ya kipagani, huku wenye nguvu wakivumilia hadi mwisho kabisa, na Urpasiano alisimama mbele ya wenye nguvu.", "patron": "Maombezi yake huombwa kwa ajili ya watumishi wa ikulu; wanaojiuzulu cheo kwa ajili ya Kristo."},

"Martyr Valerian":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Valeriano anakumbukwa siku hii pamoja na Shahidi Filoumeno wa Ankira, miongoni mwa wale walioteseka katika Galatia katika mateso chini ya mfalme Aureliano, karibu mwaka wa 274. Sinaksario za Kigiriki zinaandika kwamba alikamilishwa katika shahada kwa upanga: akimkiri Kristo mbele ya watesi na akikataa kila dai la kutoa dhabihu, alikatwa kichwa, na roho yake ikapaa kwa Bwana ambaye kwa ajili yake alikuwa ameyahesabu maisha yake kuwa si kitu.", "patron": "Maombezi yake huombwa kwa ajili ya waamini wasioandikwa katika kumbukumbu."},

"Martyr Varus, and seven Monastic Martyrs with him":
{"type": "Shahidi · karne ya 4", "life": "Shahidi Mtakatifu Varo alikuwa jemadari wa jeshi katika Misri katika siku za mateso chini ya Maksimiano, na Mkristo kwa siri, aliyewatembelea usiku wakiri waliofungwa, akiwaletea chakula, akifunga majeraha yao na akiziimarisha roho zao. Mara moja aliukesha usiku wote gerezani pamoja na walimu saba wajinyimaji wa Wakristo waliokuwa wakisubiri kuuawa, akistaajabia ujasiri wao na akiomboleza kwamba hofu ilikuwa hadi wakati ule imemzuia asikiri waziwazi.", "patron": "Maombezi yake huombwa kwa ajili ya askari; waliolala waliokufa nje ya imani."},

"Martyr Victor at Damascus":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Viktori alikuwa askari kutoka Italia aliyetumika Damasko katika utawala wa Marko Aurelio; na mateso yalipolitaka jeshi litoe dhabihu, alijitangaza kuwa Mkristo na akakataa. Jemadari alimtoa kwa mateso ya ukatili wa ajabu: vidole vyake vilivunjwa na kupotoshwa, alitupwa katika tanuru iliyowaka.", "patron": "Maombezi yake huombwa kwa ajili ya askari; uvumilivu unaopita maumbile."},

"Martyr Victor, and his companions, of Nicomedia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Viktori, Zotiko, Zeno, Akindino na Severiano waliteseka Nikomedia mwaka wa 303, na taji zao ziliwashwa kwenye moto wa mtu mwingine: walikuwa miongoni mwa umati ulioliona pambano la Shahidi Mkuu mtakatifu Georgi, aliyekuwa wakati ule akiteswa katika baraza la kifalme kwa ukatili wote wa kubuni wa mji mkuu wa Diokletiano, na kile ambacho tamasha lile lilikusudiwa kuwafundisha, ubatili wa tumaini la Kikristo, liliwafundisha kinyume chake.", "patron": "Maombezi yao huombwa kwa ajili ya askari walioongoka kwa ushuhuda wa wengine; watazamaji wanaovuka upande."},

"Martyr Vincent of Spain":
{"type": "Shemasi · karne ya 4", "life": "Shahidi Mtakatifu Vinsenti wa Hispania alikuwa shemasi mkuu wa kanisa la Saragossa chini ya askofu mzee Valerio, ambaye kigugumizi chake shemasi mfasaha alikijaza, akihubiri neno la Mungu kwa jina la askofu wake; na mateso ya Diokletiano yalipoifikia Hispania, gavana Dasiano aliwakamata wote wawili na kuwaleta kwa minyororo hadi Valencia.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wahubiri."},

"Martyr Zosimas the Hermit of Cilicia":
{"type": "Mtawa · karne ya 4", "life": "Mheshimiwa Zosima wa Kilikia, Shahidi Mtawa, aliishi katika karne ya nne kama mkaaji wa jangwa katika Kilikia, akiisha kujiondoa duniani ili kumtumikia Mungu katika utulivu; na neema kama ile ilikaa ndani yake hata wanyama wakali wa nyikani walikusanyika kwa upole kumzunguka kama walivyomzunguka Adamu peponi.", "patron": "Maombezi yake huombwa kwa ajili ya upatano na viumbe; uvumilivu chini ya mateso."},

"Martyr Zosimus the Soldier at Antioch, in Pisidia":
{"type": "Shahidi · karne ya 2", "life": "Shahidi Mtakatifu Zosimo Askari aliteseka kwa ajili ya Kristo katika zama za mateso, naye anaheshimiwa kwa ukiri thabiti ambao kwao mtu wa silaha aliyatoa maisha yake kwa ajili ya Bwana wake.", "patron": "Askari wanaomkiri Kristo; wanaoteswa kwa ajili ya imani."},

"Martyr Zoticus the Keeper of Orphans":
{"type": "Kasisi · karne ya 4", "life": "Kuhani Shahidi Mtakatifu Zotiko, Mtunza Yatima, alikuwa Mrumi mashuhuri na tajiri katika utumishi wa Mtakatifu Konstantino Mkuu, naye alikuja pamoja na mfalme katika mji mkuu mpya juu ya Bosforo, ambako aliwekwa kasisi na ambako utajiri wake ulipata wito wake. Amri, ikihofu maambukizo, ilipowahukumu wenye ukoma wa mji wazamishwe majini, Zotiko alikwenda kwa mfalme na akaomba dhahabu ili anunue mawe ya thamani na lulu kwa ajili ya utukufu wa kifalme.", "patron": "Maombezi yake huombwa kwa ajili ya mayatima; wenye ukoma."},

"Martyr and Archdeacon Euplus of Catania":
{"type": "Shemasi · karne ya 4", "life": "Shahidi Mtakatifu Euplo, Shemasi Mkuu, aliteseka mwaka wa 304 katika mji wa Kisisilia wa Katania, wakati wa mateso chini ya Diokletiano na Maksimiano. Aliibeba Injili pamoja naye kila mahali na akamhubiri Kristo kwa ujasiri kwa wapagani, na mara moja, alipokuwa akikisoma na kukieleza kitabu kitakatifu kwa watu, alikamatwa na kuletwa mahakamani.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; kuhubiri Injili."},

"Martyr and Archdeacon Laurence, and those with him, of Rome":
{"type": "Shemasi · karne ya 3", "life": "Shahidi Mtakatifu Laurentio, Shemasi Mkuu, na wale walio pamoja naye waliteseka Roma mwaka wa 258, katika mateso chini ya mfalme Valeriano. Mtakatifu Sisto, Mwathene aliyekuwa mwanafalsafa kabla ya kuwa Mkristo, alikuwa wakati ule Askofu wa Roma, na alipokamatwa pamoja na mashemasi wake Felisisimo na Agapito, Laurentio alimfuata akilia na akiomba aende naye.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wapishi."},

"Martyred Holy Fathers who were slain at the Monastery of Saint Savva":
{"type": "Mashahidi Watawa · karne ya 8", "life": "Mababa Waheshimiwa waliouawa katika Monasteri ya Mtakatifu Saba waliteseka mwaka wa 796, kwa habari nyingine 797, wakati vikundi vya wavamizi Waarabu, katika majira ya machafuko katika Palestina, vilipoivamia Lavra Kubwa katika jangwa la Yudea; na shahada yao inajulikana kwa Kanisa kwa maelezo adimu, kwa maana mmoja wa walionusurika aliandika habari za shahidi wa macho za kila kitu.", "patron": "Maombezi yao huombwa kwa ajili ya watawa wakati wa uvamizi; jumuiya zisizotawanyika."},

"Martyrs Acindynus, Pegasius, Aphthonius, Elpidephorus, Anempodistus, and 7,000 with them, of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Akindino, Pegasio, Aftonio, Elpidoforo na Anempodisto, pamoja na mashahidi elfu saba, waliteseka katika Persia karibu mwaka wa 341, chini ya Mfalme Sapori wa Pili. Akindino, Pegasio na Anempodisto walikuwa watumishi wa ikulu ya mfalme na Wakristo wa siri; na Sapori alipoinua mateso yake dhidi ya Kanisa, walisingiziwa na kuletwa mahakamani, ambako walimkiri Kristo waziwazi na wakatolewa kwa mateso makali hata muujiza baada ya muujiza ukawaandama, wanaoteseka wakihifadhiwa wazima huku watesi wao wakianguka wakiwa vipofu na kuponywa tena kwa sala ya mashahidi.", "patron": "Maombezi yao huombwa kwa ajili ya watumishi wa ikulu; maofisa."},

"Martyrs Adrian and Natalia and 23 companions, of Nicomedia":
{"type": "Mashahidi · karne ya 4", "life": "Shahidi Mtakatifu Adriano alikuwa afisa mpagani wa baraza la kifalme huko Nikomedia katika mateso chini ya Maksimiano, na akiwapo wakati Wakristo ishirini na watatu walipoteswa kwa ajili ya imani yao, alistaajabia uthabiti wao na akauliza ni thawabu gani waliyoitumaini; na waliponena juu ya mema ambayo Mungu amewaandalia wampendao, mara alisukumwa kujitangaza kuwa Mkristo pia, hata jina lake mwenyewe likaandikwa miongoni mwa waliohukumiwa.", "patron": "Maombezi yao huombwa kwa ajili ya wanandoa; ndoa."},

"Martyrs Africanus, Publius, and Terence, of Carthage":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Afrikano, Publio na Terentio waliteseka Karthago katika mateso ya Desio, karibu mwaka wa 250, majina matatu yaliyoshikwa siku hii kutoka kikundi kikubwa zaidi cha wakiri ambao ukumbusho wao mkuu Kanisa linauadhimisha mwezi wa Aprili; na ibada kwa heshima yao ziliadhimishwa tangu kale katika monasteri iitwayo Paulopetrio, mji mkuu wa Mashariki ukiiadhimisha sikukuu ya mashahidi wa Afrika, kama Kanisa lilivyoshirikisha daima mashahidi wake kuvuka bahari.", "patron": "Maombezi yao huombwa kwa ajili ya vikundi vya wakiri; shimo la nyoka lisilo na madhara."},

"Martyrs Agapius, Publius, Timolaus, Romulus, two named Dionysius, and two named Alexander, at Caesarea in Palestine":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Agapio, Publio, Timolao, Romulo, wale wawili waitwao Dionisio, na wale wawili waitwao Aleksandro waliteseka Kaisaria katika Palestina mwanzoni mwa mateso makuu, wakikatwa vichwa tarehe ishirini na nne ya Machi mwaka wa 304 kwa hesabu ya Eusebio na sinaksario ya Kigiriki, au mwaka wa 303 kwa habari za Kislavoni, na pambano lao limehifadhiwa kwa Kanisa na shahidi wa macho, kwa maana Eusebio wa Kaisaria, aliyeishi miaka ile katika mji ule, aliliandika miongoni mwa mashahidi wa Palestina.", "patron": "Maombezi yao huombwa kwa ajili ya vijana; wanaojitolea kwa ukiri."},

"Martyrs Agathopodes the Deacon and Theodulus the Reader at Thessalonica":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Agathopo Shemasi na Theodulo Msomaji walitumikia madhabahu moja huko Thesalonike na wakapokea taji moja, mateso ya miaka ya Diokletiano yakikusanya katika wavu mmoja ncha mbili za huduma ya kanisa, shemasi mzee aliyejaa miaka na heshima na msomaji kijana anayeng'aa katika usafi, babu na kijana wa patakatifu pamoja.", "patron": "Maombezi yao huombwa kwa ajili ya mashemasi na wasomaji; wazee na vijana walioungwa katika ukiri mmoja."},

"Martyrs Akepsimas and Aithalas of Egypt":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Akepsima na Aithala waliteseka Arbela katika nchi ya Persia, katika mateso ambayo wafalme wa Persia waliyainua dhidi ya Kanisa, wakati mamajusi walipowashinikiza Wakristo wa ufalme kuliabudu jua na moto na wakayatia muhuri makatao yao kwa damu. Mapokeo ya Kanisa lile lililoteseka yanasimulia kwamba Aithala mwenyewe alikuwa kuhani wa sanamu huko Arbela kabla neema ya Kristo haijampata, hata watesi wakampoteza kwa Injili mmoja wa watumishi wa madhabahu yao wenyewe, jeraha ambalo hawakulisamehe kamwe.", "patron": "Maombezi yao huombwa kwa ajili ya Kanisa chini ya Persia; makuhani wa sanamu walioongoka."},

"Martyrs Amphianus and Edesius of Lycia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Apfiano na Edesio, waitwao katika Kigiriki Apfiano na Aedesio, walikuwa ndugu wa nyumba tajiri ya kipagani ya Likia, waliopelekwa katika shule mashuhuri za Beruto, ambako badala ya ulimwengu walimpata Kristo; na Apfiano, akiacha jamaa na urithi, alifika Kaisaria katika Palestina na akajiunga na Pamfilo mtakatifu, ambaye katika shule yake ya Maandiko na utakatifu Eusebio, mwandishi wa habari za kifo chake, alikuwa mwanafunzi mwenzake.", "patron": "Maombezi yao huombwa kwa ajili ya wanafunzi; ndugu."},

"Martyrs Ananias the Presbyter, Peter, and seven soldiers, in Phoenicia":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Anania Kasisi, Petro mlinzi wa gereza, na askari saba waliteseka katika Foinike mwaka wa 295, wakati wa mateso chini ya Diokletiano. Anania, kasisi wa nchi ile, alikamatwa kwa kumkiri Kristo na kuzikataa sanamu, na akaletwa mbele ya Maksimo, gavana wa Foinike, aliyemwekea sarufi nzima ya mahakama: kasisi alipigwa kwa nyundo, akachomwa kwa moto, na akapakwa chumvi katika mwili wake ulioungua, naye akavumilia yote kwa utulivu wa mtu ambaye hazina yake iko kwingine.", "patron": "Maombezi yao huombwa kwa ajili ya makasisi; walinzi wa gereza."},

"Martyrs Anatolius and Protoleon, soldiers converted by witnessing the martyrdom of Saint George":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Anatolio na Protoleoni walikuwa askari huko Nikomedia, na taji zao zilishindwa katika dakika moja, dakika ambayo gurudumu lilishindwa. Shahidi Mkuu Georgi alipokuwa amevunjwa, kama wote walivyodhani, juu ya gurudumu la visu, na baraza likawa limetawanyika likiridhika kwamba shujaa wa Wakristo ameangamizwa, shahidi alionekana amesimama mzima, akiponywa na malaika wa Bwana, mbele ya walinzi waliostaajabu.", "patron": "Maombezi yao huombwa kwa ajili ya askari; wa kwanza kujitokeza mbele."},

"Martyrs Andrew, John, and John’s children: Peter and Antonius, of Syracuse, martyred in Africa":
{"type": "Mashahidi · karne ya 9", "life": "Mashahidi Watakatifu Andrea, Yohane, na wana wa Yohane Petro na Antonino walikuwa wazaliwa wa Sirakusa katika Sisilia, waliochukuliwa mateka hadi Afrika katika karne ya tisa, wakati Wasaraseni walipolivamia kisiwa. Wale wavulana wawili, waliochukuliwa wangali wadogo, walilelewa katika baraza la amiri na kufundishwa elimu na dini ya waliowateka, wakihesabiwa kwa nje miongoni mwa Waislamu.", "patron": "Maombezi yao huombwa kwa ajili ya mateka; imani iliyohifadhiwa katika nchi ya ugenini."},

"Martyrs Anicetus and Photius of Nicomedia, and those with them":
{"type": "Walei · karne ya 4", "life": "Mashahidi Watakatifu Aniketo na Fotio, mjomba na mpwa wake, walikuwa wazaliwa wa Nikomedia. Mfalme Diokletiano alipoweka katika uwanja wa hadhara chombo cha kuuawa ili kuwatisha Wakristo, Aniketo, afisa wa baraza, alimkemea waziwazi, na mfalme aliyeghadhibika akamtoa kwa mateso.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyrs Anthony, John, and Eustathius of Vilnius":
{"type": "Mashahidi · karne ya 14", "life": "Mashahidi Watakatifu Antonio, Yohane na Eustathio wa Vilnius walikuwa watumishi vijana wa baraza la Algirdas, Mkuu wa Lithuania ya kipagani, dola kubwa ya mwisho isiyobatizwa ya Ulaya, na kabla ya ubatizo walibeba majina Kumets, Nezhilo na Kruglets; wakifundishwa na kubatizwa kwa siri na kasisi aliyeitwa Nestori, ndugu Antonio na Yohane walijifichua wenyewe kwenye meza ya mkuu, kwa maana hawakukubali kula nyama siku za kufunga, na baraza lililoabudu moto liliisoma kujizuia kule kwa usahihi, mgongano wote wa dini mbili ukigundulika katika sahani iliyokataliwa.", "patron": "Maombezi yao huombwa kwa ajili ya watumishi wa ikulu za mamlaka za kipagani; ndugu katika ukiri."},

"Martyrs Basil and Theodore of the Kyiv Caves":
{"type": "Mtawa · karne ya 11", "life": "Waheshimiwa Basili na Theodoro wa Mapango ya Kyiv, Mashahidi Watawa, walijinyima katika karne ya kumi na moja katika Mapango ya Karibu ya Kyiv. Mtakatifu Theodoro alikuwa amegawa utajiri wake kwa maskini na akaingia katika monasteri, akikaa katika Pango la Wavarangi, lakini baada ya miaka mingi mtu adui alimjaribu kwa wazo la hazina ya dhahabu na fedha iliyosemekana kufichwa humo, akitaka kumtoa katika nadhiri zake za utawa.", "patron": "Maombezi yao huombwa kwa ajili ya kujitenga na mali; dhidi ya tamaa ya mali."},

"Martyrs Basilissa and Anastasia of Rome, disciples of Apostles Peter and Paul":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Basilisa na Anastasia walikuwa wanawake watukufu wa Roma, walioongolewa kwa kuhubiri kwa Mitume wakuu na kuhesabiwa miongoni mwa wanafunzi wa Petro na Paulo wenyewe, wakiundwa kwenye chemchemi yenyewe katika miaka ambayo kanisa la kwanza la mji mkuu lilikutana katika nyumba na imani ilipita kutoka midomo ya Mitume wenyewe.", "patron": "Maombezi yao huombwa kwa ajili ya wanaozika mashahidi; wanafunzi wa Mitume."},

"Martyrs Carpus, Papylus, Agathadorus, and Agathonica, at Pergamum":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Karpo, Papilo, Agathodoro na Agathonika waliteseka Pergamo katika mateso chini ya Desio, mwaka wa 251. Karpo alikuwa askofu wa Thiatira na Papilo shemasi wake, mtu aliyeutoa utajiri wake kwa maskini; na gavana wa eneo lile alipojua kwamba hawazishiki sikukuu za kipagani, aliwaleta mahakamani, na alipowakuta hawatikisiki katika ukiri wa Kristo, aliwadhulumu kwa mateso: walikokotwa nyuma ya farasi, wakachanwa, na wakatolewa kwa wanyama wakali, ambao hawakukubali kuwadhuru.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti; uponyaji."},

"Martyrs Christopher, Theonas, and Anthony, at Rome":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Kristoforo, Theona na Antonio walikuwa wabeba mikuki wa mfalme Diokletiano, askari wa walinzi wa ndani kabisa, na uongofu wao ulikuja kwa bei kubwa kuliko zote ambayo baraza lingeweza kuiona: walipoyaona mateso ya Shahidi Mkuu mtakatifu Georgi, jemadari kijana akiteswa mbele ya kiti cha enzi kwa kila kifaa na akitegemezwa katika yote kwa nguvu ambayo ikulu nzima ingeweza kuiona, walinzi watatu walitoa hitimisho la askari, kwamba ushindi ulikuwa upande wa mfungwa.", "patron": "Maombezi yao huombwa kwa ajili ya walinzi wa mfalme; walio karibu zaidi na mamlaka wanaomchagua Kristo."},

"Martyrs Chrysanthus and Daria, and those with them at Rome":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Krisantho na Daria waliteseka Roma mwaka wa 283 kwa hesabu za Kirumi na za Kigiriki, ingawa vitabu vinavyowaweka chini ya Valeriano vinatoa karibu mwaka wa 253, na pambano lao lilikusanya mavuno mazima ya wenzao kabla halijafungwa. Krisantho, mwana wa seneta Polemio, alikuja pamoja na baba yake kutoka Aleksandria hadi Roma, na katika mwendo wa masomo yake aliyakuta Maandiko, na kwa mafundisho ya kasisi Karpoforo alibatizwa, na mara akaanza kumkiri Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya wanandoa waliojiweka nadhiri ya usafi; walioongoka kwa njia ya walioongoka."},

"Martyrs Dada, Maximus, and Quinctilian, at Dorostolum":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Dada, Maksimo na Kwintiliano waliteseka katika kijiji cha Ozovia karibu na Dorostolo kando ya Danube, mwaka wa 286, chini ya mateso ya utawala wa Diokletiano, majina matatu zaidi katika shada tajiri la mashahidi la nchi ile ya mpakani ambayo ngome zake na vijiji vyake vilikilisha kalenda ya Kanisa kwa kizazi kizima.", "patron": "Maombezi yao huombwa kwa ajili ya wanakijiji katika ukiri; wanaoshambuliwa usiku."},

"Martyrs Dadas, Gabdelas, and Kazdoa of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Dada, Gabdela na Kazdoa waliteseka kwa ajili ya Kristo katika Persia chini ya mfalme Sapori. Dada, jamaa wa mfalme na msimamizi mkuu wa baraza lake, aligundulika kuwa Mkristo na akavuliwa heshima zake, na akatolewa kwa mateso; lakini moto uliokuwa umeandaliwa kwa ajili yake ulipogeuzwa kando kwa sala yake na maajabu yakatendeka mbele ya wote, mwana wa mfalme mwenyewe Gabdela na binti yake Kazdoa, walipoiona nguvu ya Kristo, walimwamini Mungu wa mtu yule waliyetumwa kumhukumu.", "patron": "Maombezi yao huombwa kwa ajili ya walioongoka kutoka nyumba za watesi."},

"Martyrs Demetrius, his wife Euanthia, and their son Demetrian, at Skepsis on the Hellespont":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Demetrio, mkewe Euanthia na mwanao Demetriano waliteseka kwa ajili ya Kristo katika karne ya kwanza katika mji wa Skepsi kwenye Helesponti. Demetrio alikuwa mtawala wa mji ule, na kwa mapokeo ya Kanisa aliletwa kwenye imani kwa mahubiri na maajabu ya Kuhani Shahidi Kornelio Akida, yuleyule ambaye Mtume Petro alimbatiza, wakati Kornelio alipofika Skepsi akimtangaza Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya Familia za Kikristo; ukiri thabiti."},

"Martyrs Diodorus and Rhodopianus, Deacons, at Aphrodisia in Anatolia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Diodoro na Rodopiano, mashemasi, waliteseka Afrodisia katika Karia katika mateso ya Diokletiano, kati ya mwaka wa 284 na 305, na pambano lao lina alama ya mji wao.", "patron": "Maombezi yao huombwa kwa ajili ya mashemasi; waliouawa na majirani zao."},

"Martyrs Elias, Probus, and Ares in Cilicia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Elia, Probo na Are walikuwa Wamisri kwa kuzaliwa, na uhalifu wao ulikuwa huruma: katika mateso chini ya Maksimiano waliondoka Misri kwenda Kilikia, bila kujali usalama wao wenyewe, ili kuwahudumia wakiri wa Kristo waliofungwa huko na kuhukumiwa machimbo, wakiwapelekea faraja wale ambao himaya ilikuwa imewatupa.", "patron": "Maombezi yao huombwa kwa ajili ya wageni wa gerezani; wanaowahudumia walioteswa."},

"Martyrs Elpidius, Marcellus, and Eustochius, who suffered under Julian the Apostate":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Elpidio, Marcelo na Eustokio waliteseka chini ya Yuliano Mwasi, katika miaka ya 361 hadi 363, wakati himaya, ikiisha kuionja amani ya Kanisa, ilipokokotwa nyuma na mtawala wake kuelekea ibada ya sanamu. Elpidio alikuwa seneta, mtu wa heshima kubwa, naye aliletwa pamoja na wenzake mbele ya mwamuzi wa kifalme kwa shtaka la kuwa Mkristo.", "patron": "Maombezi yao huombwa kwa ajili ya maseneta; maofisa."},

"Martyrs Eudoxios, Agapios, Atticus, and those with them, at Sebaste":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Atiko, Agapio, Eudoksio, Karterio, Istukario aitwaye Styraksi, Paktobio na Niktopolioni, pamoja na wenzao, walikuwa askari wa Sebaste katika Armenia, nao waliteseka karibu mwaka wa 320 katika mateso chini ya Likinio, ambaye, akijiandaa kwa vita dhidi ya Mtakatifu Konstantino, aliyasafisha majeshi yake kwa Wakristo na akadai kutoka kwa ngome dhabihu kwa sanamu.", "patron": "Maombezi yao huombwa kwa ajili ya askari; askari waaminifu kwa Kristo."},

"Martyrs Eudoxius, Zeno, and Macarius":
{"type": "Jemadari · karne ya 4", "life": "Mashahidi Watakatifu Eudoksio, Zeno na Makario waliteseka chini ya Maksimiano Galerio, mrithi wa Diokletiano. Eudoksio alikuwa jemadari wa cheo cha juu katika majeshi ya kifalme na Mkristo, kama walivyokuwa rafiki yake Zeno na msimamizi wake wa mali Makario; na amri ilipotoka dhidi ya waamini, alijiondoa pamoja na jamaa yake, lakini alitafutwa na askari ambao, bila kumjua, walipokea ukarimu wake.", "patron": "Maombezi yao huombwa kwa ajili ya askari."},

"Martyrs Eulampius and Eulampia, at Nicomedia, and 200 Martyrs with them":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Eulampio na Eulampia, ndugu wa kiume na wa kike, waliishi Nikomedia mwanzoni mwa karne ya nne. Amri ya mfalme Maksimiano iliyowahukumu Wakristo wote kifo ilipobandikwa mjini, Eulampio kijana aliisoma na akaomboleza kwa sauti kwamba mfalme aliinua silaha dhidi ya raia wake wasio na hatia badala ya dhidi ya adui za himaya.", "patron": "Maombezi yao huombwa kwa ajili ya ndugu wa kiume na wa kike katika Kristo; ujasiri mbele ya sanamu."},

"Martyrs Eustochius, Gaius, Probus, Lollius, and Urban, of Ancyra":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Eustokio, Gaio, Probo, Lolio na Urbano waliteseka kwa ajili ya Kristo huko Ankira katika Galatia katika zama za mateso, na kikundi chao kilikusanywa kwa Kristo na uthabiti wenyewe wa mashahidi ambao hapo awali walikuwa wamewapinga.", "patron": "Walioongoka kutoka upagani; jamaa wanaokiri pamoja."},

"Martyrs Eustratius, Auxentius, Eugene, Mardarius, and Orestes, at Sebaste":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Eustratio, Auksentio, Eugenio, Mardario na Oreste, Wenzake Watano, waling'aa kama nyota tano juu ya Armenia katika mateso ya Diokletiano na Maksimiano, karibu mwaka wa 296, na pambano lao ni mnyororo wa ukiri wa hiari, kila mtu akijitokeza mbele bila kulazimishwa. Auksentio, kasisi wa Arauraka, alikamatwa kwanza na magavana Lisia na Agrikolao.", "patron": "Maombezi yao huombwa kwa ajili ya askari; watunza nyaraka."},

"Martyrs Eutropius, Cleonicus, and Basiliscus of Amasea":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Eutropio, Kleoniko na Basilisko waliteseka Amasea katika Ponto karibu mwaka wa 308, na pambano lao ni mwendelezo wa pambano mashuhuri, kwa maana watatu walikuwa wenzake wa Shahidi Mkuu Theodoro Askari Mpya, Basilisko akiwa jamaa yake kwa damu na wote watatu jamaa zake katika silaha, waliokamatwa katika mateso yaleyale yaliyomvika taji Theodoro miaka miwili kabla na kushikwa katika gereza lilelile, ambako kumbukumbu ya ushindi wa askari mpya ilikuwa hewa ambayo watatu wale waliipumua.", "patron": "Maombezi yao huombwa kwa ajili ya jamaa na wenzake katika jaribu; askari wa Kristo."},

"Martyrs Florus and Laurus of Illyria":
{"type": "Mashahidi · karne ya 2", "life": "Mashahidi Watakatifu Floro na Lauro walikuwa ndugu mapacha, wenye undugu si katika mwili tu bali katika roho, walioishi katika karne ya pili na wakakaa katika Iliria, ambako walifanya kazi ya kuchonga mawe; kutoka kwa mabwana wao Wakristo, Proklo na Maksimo, walikuwa wamejifunza ufundi wao na njia ya maisha impendezayo Mungu.", "patron": "Maombezi yao huombwa kwa ajili ya waashi wa mawe; farasi na wapanda farasi."},

"Martyrs Frontasius, Severinus, Severian, and Silanus, of Gaul":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Frontasio, Severino, Severiano na Silano wanaheshimiwa kama miongoni mwa wahubiri wa kwanza wa Injili na mashahidi wa kwanza wa Gaul, wakishikiliwa na mapokeo ya eneo lao kuwa wa kizazi cha kwanza kabisa cha utume wa Kanisa katika nchi za magharibi.", "patron": "Waangazaji wa kwanza wa Gaul; wanafunzi wa wamisionari wa kitume."},

"Martyrs Galacteon, Juliana, and Saturninus, of Constantinople":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Galaktioni, Yuliana na Saturnino waliteseka kwa ajili ya Kristo huko Bizanti katika zama za mateso, na ingawa mambo madogo ya mateso yao hayajahifadhiwa kwa ukamilifu, Kanisa linayashika majina yao pamoja.", "patron": "Waliouawa pamoja; imara katika ukiri."},

"Martyrs Galaction and his wife, Epistemis, at Emesa":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Galaktioni na mkewe Epistemi waliteseka Emesa katika Syria mwaka wa 253, chini ya mateso ya Desio. Galaktioni alizaliwa na mwanamke mtukufu Leukipe, aliyekuwa tasa muda mrefu, aliyekuwa ameletwa kwa Kristo na kubatizwa na mtawa aliyeitwa Onufrio, naye akamlea mwanawe kwa siri katika imani.", "patron": "Maombezi yao huombwa kwa ajili ya wanandoa; watawa."},

"Martyrs Gervasius, Nazarius, Protasius, and Celsus of Milan":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Nazario, Gervasio, Protasio na Kelso wa Milano waliteseka katika utawala wa mfalme Nero. Nazario, aliyezaliwa Roma na Perpetua Mkristo na kubatizwa, kama mapokeo yasimuliavyo, na Lino mrithi wa Petro, aliutoa ujana wake kwa kumhubiri Kristo na kwa kuwatunza Wakristo walioteswa, na alipofika Milano aliwakuta huko gerezani ndugu mapacha Gervasio na Protasio, wana wa Vitalio shahidi na wa Valeria, waliokuwa wameutoa urithi wao kwa maskini na maisha yao kwa kufunga na sala.", "patron": "Maombezi yao huombwa kwa ajili ya kuwatunza Wakristo waliofungwa; kuwalea watoto kwa ajili ya Mungu."},

"Martyrs Heliodorus and Dosa of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Heliodoro na Dosa waliteseka kwa ajili ya Kristo katika Persia mwaka wa 380, wakati wa mateso marefu ya Wakristo chini ya mfalme Sapori. Ingawa machache ya pambano lao yamehifadhiwa, inajulikana kwamba waliikiri imani na wakavumilia kifo badala ya kumkana Bwana wao au kuuabudu moto na jua kama Waajemi walivyofanya.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyrs Heraclius, Paulinus, and Benedimus":
{"type": "Shahidi · karne ya 4", "life": "Mashahidi Watakatifu Herakli, Paulino na Benedimo waliteseka kwa ajili ya Kristo huko Noviodunum katika Skithia Ndogo, mji wa ngome kwenye Danube ya chini katika nchi ambayo sasa ni Romania, nao wameunganishwa katika kalenda ya siku hii na mashahidi Petro na Dionisio.", "patron": "Imani iliyokiriwa katika ukingo wa kaskazini wa himaya."},

"Martyrs Hermes, Serapion, and Polyaenus of Rome":
{"type": "Mashahidi · karne ya 2", "life": "Mashahidi Watakatifu Herme, Serapioni na Polieno walikuwa raia wa Roma katika karne ya pili, wenye bidii katika kueneza imani ya Kristo na katika kuzipinga hoja za wapagani. Wakikamatwa na kuletwa mbele ya wenye mamlaka, walisimama imara katika ukiri wa imani yao na hawakukubali kutoa dhabihu kwa sanamu, na kwa ajili hiyo walipigwa kikatili na wakatupwa katika gereza la giza na chafu, ambako walivumilia njaa na kila taabu bila kusitasita.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyrs Inna, Pinna, and Rimma, disciples of Apostle Andrew in Scythia":
{"type": "Mashahidi · karne ya 2", "life": "Mashahidi Watakatifu Inna, Pinna na Rimma walikuwa miongoni mwa malimbuko ya Injili katika nchi za kaskazini kando ya Bahari Nyeusi na Danube, wanafunzi wa Mtume Mtakatifu Andrea Aliyeitwa wa Kwanza.", "patron": "Wanafunzi wa Mitume; waangazaji wa nchi za kaskazini."},

"Martyrs Isaac, Apollos, and Quadratus, of Nicomedia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Isaka, Apolo na Kuadrato walikuwa watumishi wa nyumba ya kifalme huko Nikomedia, na taji zao zinayakamilisha mavuno ya kushangaza ambayo pambano la Shahidi Mkuu Georgi liliyavuna ndani ya ikulu yenyewe.", "patron": "Maombezi yao huombwa kwa ajili ya watumishi wa nyumba za wakuu; wanaokiri baada ya malkia."},

"Martyrs Isidore and Myrope of Chios":
{"type": "Shahidi · karne ya 3", "life": "Shahidi Mtakatifu Isidoro wa Kio, mzaliwa wa Aleksandria katika Misri, aliteseka katika kisiwa cha Kio chini ya mfalme Desio, karibu mwaka wa 251, na mateso yake yaliunganisha ukiri wa askari na uaminifu wa mwanamke.", "patron": "Kristo alikiriwa mbele ya amiri."},

"Martyrs James (Jacob) the Presbyter, and Azadanes and Abdicius, Deacons, of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Yakobo Kasisi na mashemasi Azadanes na Abdieso waliteseka katika Persia chini ya Mfalme Sapori wa Pili, karibu mwaka wa 380, katika miaka ya mwisho ya vita ya miaka arobaini ya utawala ule dhidi ya Kanisa; walikamatwa pamoja na askofu wao, Akepsima mtakatifu, ambaye Kanisa linamkumbuka mwezi wa Novemba, watesi wakikusanya katika kukamata kumoja madaraja matatu ya patakatifu, askofu, kasisi na mashemasi, wakleri wote wakichukuliwa kama fungu moja.", "patron": "Maombezi yao huombwa kwa ajili ya makasisi na mashemasi wakati wa mateso; waliokosa chakula na kuganda kwa baridi."},

"Martyrs Julian the Presbyter and Caesarius the Deacon at Terracina":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Yuliano Kasisi na Kaisario Shemasi waliteseka kwa ajili ya Kristo huko Terracina katika Italia katika zama za kwanza za Kanisa. Kaisario, shemasi aliyekuja kutoka Afrika, aliona katika mji ule desturi ya kikatili ya kipagani ambayo kwayo kijana mmoja, aliyelishwa vizuri kwa miezi kwa gharama ya mji, alijitupa kutoka mahali pa juu kama dhabihu kwa sanamu.", "patron": "Maombezi yao huombwa kwa ajili ya kupinga ukatili; ukiri thabiti."},

"Martyrs Kyriaina and Juliana in Cilicia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Kiriaina na Yuliana waliteseka katika Kilikia katika mateso chini ya Maksimiano, karibu mwaka wa 305. Kiriaina alikuwa wa Tarso na Yuliana wa mji wa Rosso, wote wanawake waliokuwa wameyatoa maisha yao kwa Kristo katika usafi na sala; na walipokamatwa na Marciano, gavana wa Kilikia, walikataa kila dai la kutoa dhabihu kwa sanamu.", "patron": "Maombezi yao huombwa kwa ajili ya heshima katika dhihaka; wanawake waaminifu hadi kufa."},

"Martyrs Kyriake, Kaleria, and Mary of Caesarea, in Palestine":
{"type": "Mashahidi · karne ya 4", "life": "Wanawake Watakatifu Mashahidi Kiriaki, Kaleria, aitwaye pia Valeria, na Maria waliteseka kwa ajili ya Kristo huko Kaisaria katika Palestina katika mateso ya Diokletiano, na habari yao fupi na nzuri ni ya kuongoka, sala na ukiri thabiti.", "patron": "Wanawake wanaoacha upagani kwa ajili ya Kristo; wanaoomba mateso yakome."},

"Martyrs Leonidas, Chariessa, Nice, Galina, Kalista, Nunechia, Basilissa, Theodora, and Irene, of Corinth":
{"type": "Mashahidi · karne ya 3", "life": "Shahidi Mtakatifu Leonida na wanawake watakatifu wanane walioteseka pamoja naye, Hariesa, Nike, Galina, Kalista, Nunehia, Basilisa, Theodora na Irene, walikuwa Wakristo wa Korintho, waliokamatwa katika mateso ya mwaka wa 258, katika majira ya Pasaka, wakiri wa Kristo aliyefufuka wakikamatwa katika majuma yaleyale ambayo Kanisa linaimba juu ya ushindi wake juu ya mauti.", "patron": "Maombezi yao huombwa kwa ajili ya vikundi vya wanawake wakiri; waimbaji."},

"Martyrs Leontius, Hypatius, and Theodulus at Tripoli in Syria":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Leontio, Hipatio na Theodulo waliteseka kwa ajili ya Kristo huko Tripoli katika Foinike katika zama za kwanza za Kanisa, na shahada yao ni habari ya mtesi aliyegeuzwa kuwa mkiri mwenzao.", "patron": "Askari na majemadari; walioongoka wakiwa wanatesa."},

"Martyrs Manuel and Theodosius":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Manueli na Theodosio waliteseka mwaka wa 304, katika kilele cha mateso makuu, nao ni wa kikundi kile cha mashahidi ambao vifo vya wengine viliwaandikisha: wakiuona uthabiti wa mashahidi wa eneo lao, mateso yaliyovumiliwa kwa furaha na taji zilizopokelewa mbele ya umati, vijana wale wawili hawakuogopa, kama watesi walivyokusudia kila mtazamaji aogope, bali waliwashwa, tamasha la uwanjani likifanya kazi kinyume kabisa, kama lilivyofanya katika zama zile zote, na kuwageuza watazamaji wake kuwa waamini.", "patron": "Maombezi yao huombwa kwa ajili ya walioamshwa na kielelezo cha mashahidi; ukiri uliotolewa kwa hiari."},

"Martyrs Manuel, Sabel, and Ismael, of Persia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Manueli, Sabeli na Ismaeli walikuwa ndugu watatu wa asili tukufu ya Kiajemi walioteseka kwa ajili ya Kristo katika baraza la Yuliano Mwasi katika karne ya nne, na shahada yao iligeuza ujumbe wa amani kuwa ushuhuda wa imani.", "patron": "Wajumbe na mabalozi; ndugu katika imani."},

"Martyrs Marcian and Martyrius, the Notaries of Constantinople":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Marciano na Martirio walitumika kama waandishi wa hati, yaani makatibu na wasomaji, kwa Mtakatifu Paulo Mkiri, Patriaki wa Konstantinopoli, katika miaka ambayo uzushi wa Ario, ukiungwa mkono na baraza la kifalme, ulipowaka dhidi ya watetezi wa imani ya Nikea. Patriaki mtakatifu alipofukuzwa na kunyongwa kwa siri uhamishoni, Waariani walitaka kuwavuta waandishi wake waaminifu, wakiwapa dhahabu, heshima na hata viti vya uaskofu kama wangeukubali uzushi uliomfanya Mwana wa Mungu kuwa kiumbe.", "patron": "Maombezi yao huombwa kwa ajili ya waandishi wa hati; makatibu."},

"Martyrs Maurice and his son, Photinus, and Martyrs Theodore, Philip, and 70 soldiers, at Apamea in Syria":
{"type": "Mashahidi · karne ya 4", "life": "Shahidi Mtakatifu Maurikio, jemadari wa jeshi wa Apamea katika Syria, aliteseka mwaka wa 305 chini ya Maksimiano Galerio, pamoja na mwanawe Fotino na askari sabini wa jeshi lake, ambao kati yao majina mawili tu, Theodoro na Filipo, yametufikia, wengine wakiandikwa, kama mababa wasemavyo juu ya vikundi kama hivyo, katika Kitabu cha Uzima peke yake.", "patron": "Maombezi yao huombwa kwa ajili ya majemadari; baba na wana walio jeshini."},

"Martyrs Maximus, Theodotus, Hesychius, and Asclepiodota, of Adrianopolis":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Maksimo, Theodoto, Hesikio na Asklepiodota waliteseka katika Thrakia katika mateso ya Maksimiano, karibu mwaka wa 305, wanaume watatu wa Adrianopoli na pamoja nao Asklepiodota, mwanamke wa jamaa tukufu ambaye ujasiri wake uliupanga mwelekeo wa pambano lote la kikundi.", "patron": "Maombezi yao huombwa kwa ajili ya wenzake katika jaribu; wanawake wa vyeo wenye ujasiri."},

"Martyrs Menas, Hermogenes, and Eugraphus, of Alexandria":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Mena, Hermogene na Eugrafo waliteseka Aleksandria karibu mwaka wa 313, chini ya mfalme Maksimiano, na pambano lao ni mnyororo wa uongofu uliofuliwa chini ya mateso. Mena, Mwathene mashuhuri kwa ufasaha, ambaye Wagiriki wanamwita Kallikelado, msemaji mtamu, alitumwa na mfalme Aleksandria ili kuutuliza ugomvi kati ya wapagani na Wakristo.", "patron": "Maombezi yao huombwa kwa ajili ya wanenaji; waamuzi."},

"Martyrs Menodora, Metrodora, and Nymphodora, at Nicomedia":
{"type": "Mashahidi · karne ya 4", "life": "Mabikira Mashahidi Watakatifu Menodora, Metrodora na Nimfodora walikuwa dada kutoka Bithinia katika Asia Ndogo, ambao, wakitaka kuuhifadhi ubikira wao kwa Kristo na kuukwepa ubatili wa dunia, walijiondoa hadi mahali pa upweke vilimani, ambako waliishi katika kufunga na sala; na habari za utakatifu wao zilienea, kwa maana uponyaji ulianza kutiririka kwa sala zao.", "patron": "Maombezi yao huombwa kwa ajili ya upendo wa kidada; usafi."},

"Martyrs Modestus, Crescentia, and Vitus, at Lucania":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Vito, Modesto na Kresentia waliteseka kwa ajili ya Kristo katika mateso ya Diokletiano, na kikundi chao kiliunganisha mvulana mchanga na mwalimu na mlezi waliomlea katika imani na wakafa pamoja naye.", "patron": "Watoto na walezi wao; walezi wa watoto na wauguzi."},

"Martyrs Nestor, Tribimius, and those with them":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Nestori, Tribimio, Marcelo na Antonio wa Perge katika Pamfilia waliteseka katika utawala wa mfalme Desio, karibu mwaka wa 250, katika mateso yaliyodai kutoka kwa kila roho katika himaya cheti cha dhabihu na yakalifanya kila katao kuwa kesi ya kifo. Wale wanne walikuwa Wakristo wa Perge ambao hawakungoja.", "patron": "Maombezi yao huombwa kwa ajili ya wenzake katika ukiri; taji nne kwa upanga."},

"Martyrs Nikephoros, Antoninus, and Germanus of Caesarea, in Palestine":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Antonino, Nikeforo na Germano waliteseka Kaisaria katika Palestina karibu mwaka wa 308, katika utawala wa Maksimino, wakati gavana Firmiliano alipoyasukuma mateso dhidi ya Kanisa kwa dhabihu za hadharani na matamasha. Ibada za kipagani zilipokuwa zikiadhimishwa mbele ya mji uliokusanyika, Wakristo watatu walijitokeza mbele kwa hiari yao na, wakisimama mbele ya gavana, waliikemea ibada ya sanamu zisizo na uhai na wakamkiri kwa sauti kuu Mungu mmoja wa kweli na Kristo wake.", "patron": "Maombezi yao huombwa kwa ajili ya ujasiri mbele ya watesi."},

"Martyrs Onesiphorus and Porphyrius of Ephesus":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Onesiforo na Porfirio waliteseka kwa ajili ya Kristo katika mateso chini ya Diokletiano, kuelekea mwisho wa karne ya tatu. Wakijikiri kuwa Wakristo, waliletwa mahakamani na wakadhulumiwa kwa mateso makali, wakipigwa na kuchomwa kwa moto; na maumivu wala ahadi zilipokosa kuwageuza kutoka kwa Kristo, watesi waliwafunga mashahidi kwa farasi wa mwitu, waliowakokota juu ya miamba na miiba hadi walipozitoa roho zao takatifu kwa Mungu.", "patron": "Maombezi yao huombwa kwa ajili ya uvumilivu hadi mwisho."},

"Martyrs Pamphilius the Presbyter, Valens the Deacon, and those with them, at Caesarea in Palestine":
{"type": "Kuhani Shahidi · karne ya 4", "life": "Mashahidi Watakatifu Pamfilo Kasisi, Valenti Shemasi, Paulo, Porfirio, Seleuko, Theodulo, Yuliano, na vijana watano Wamisri Elia, Yeremia, Isaya, Samweli na Danieli waliteseka Kaisaria katika Palestina karibu mwaka wa 309, katika mwaka wa saba wa mateso makuu, na pambano lao liliandikwa na shahidi wa macho aliyewapenda, Eusebio mwanahistoria, aliyekiita kikundi chao sura kamili ya kusanyiko lote la Kanisa.", "patron": "Maombezi yao huombwa kwa ajili ya wasomi; wanakili."},

"Martyrs Patermuthius, Coprius, and Alexander the Soldier, in Egypt":
{"type": "Mtawa · karne ya 4", "life": "Waheshimiwa Patermuthio na Koprio, Mashahidi Watawa, pamoja na Aleksanda Askari, waliteseka katika Misri chini ya mfalme Yuliano Mwasi. Patermuthio alikuwa amekuwa mpagani na kiongozi wa kikundi cha wanyang'anyi, lakini alipokuja katika toba alibatizwa na akajiondoa jangwani, ambako alijitoa kwa kazi ya kujinyima na akapewa vipaji vya uponyaji na unabii.", "patron": "Maombezi yao huombwa kwa ajili ya toba; kudumu."},

"Martyrs Paul and Juliana of Syria":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Paulo na dada yake Yuliana waliteseka kwa ajili ya Kristo katika utawala wa mfalme Aureliano, katika mji wa Kifoinike wa Ptolemai. Mfalme alipokuja katika mji ule, Paulo, akikutana naye katikati ya umati, alijifanyia ishara ya Msalaba, na kwa ajili hiyo alikamatwa na kutupwa gerezani, na siku iliyofuata, alipoletwa mahakamani, aliikiri imani yake katika Kristo waziwazi na bila hofu, na kwa ajili hiyo aliteswa kikatili.", "patron": "Maombezi yao huombwa kwa ajili ya usafi; ukiri thabiti."},

"Martyrs Paul and two sisters, Chionia (Thea) and Alevtina (Valentina), at Cæsarea in Palestine":
{"type": "Walei · karne ya 4", "life": "Mashahidi Watakatifu Paulo na dada wawili Kionia na Alevtina walikuwa wazaliwa wa Misri walioteseka kwa ajili ya Kristo katika mateso chini ya mfalme Maksimiano. Wakikamatwa kwa ajili ya imani yao, walipelekwa Kaisaria katika Palestina, ambako bila hofu hata kidogo walijikiri kuwa wafuasi wa Kristo mbele ya waamuzi wao na wakakataa kutoa dhabihu kwa sanamu.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri usio na woga."},

"Martyrs Perpetua, a woman of Carthage, and the Catechumens: Saturus, Revocatus, Saturninus, Secundulus and Felicitas":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Perpetua na Felisita, pamoja na wanaofundishwa imani Saturo, Revokato, Saturnino na Sekundulo, waliteseka Karthago karibu mwaka wa 203, na pambano lao ndilo linalojulikana kwa ukaribu kuliko yote ya Kanisa la kale, kwa maana Perpetua aliweka shajara gerezani, na Kanisa limekisoma kitabu cha mkono wake mwenyewe kwa karne kumi na nane, andiko la kwanza kabisa tulilo nalo kutoka kwa mwanamke Mkristo.", "patron": "Maombezi yao huombwa kwa ajili ya mama; wanawake wenye mimba."},

"Martyrs Peter, Dionysius, Andrew, Paul, and Christina who suffered under Decius":
{"type": "Shahidi · karne ya 3", "life": "Mashahidi Watakatifu Petro, Dionisio, Andrea, Paulo na Kristina waliteseka kwa ajili ya Kristo katika mateso ya mfalme Desio, karibu katikati ya karne ya tatu, nao wanakumbukwa pamoja siku hii, ingawa mapokeo yanayaweka mateso yao katika zaidi ya mji mmoja wa Mashariki.", "patron": "Imani iliyohifadhiwa chini ya Desio."},

"Martyrs Philadelphus, Cyprian, Alphius, Onesimus, Erasmus, and 14 others, in Sicily":
{"type": "Shahidi · karne ya 3", "life": "Mashahidi Watakatifu Alfio, Filadelfo na Kipriano, ndugu watatu, waliteseka pamoja na mwalimu wao Onesimo, pamoja na Erasmo, na pamoja na wengine kumi na wanne katika mateso ya Desio, karibu mwaka wa 251, na pambano lao liliunganisha ncha mbili za Mediterania ya Kikristo, likianzia kusini mwa Italia na kumalizikia Sisilia.", "patron": "Ndugu watatu na ukiri mmoja."},

"Martyrs Philemon, Apollonios, Arrian, and Theonas of Alexandria":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Filemoni, Apolonio, Arriano na Theona waliteseka katika Misri karibu mwaka wa 286, na habari yao ni mbio za kupokezana za neema ambamo kila mkimbiaji anampa mwenzake taji. Apolonio, msomaji wa kanisa la Antinoe, akiogopa mateso, alimwajiri mpagani Filemoni, mpiga filimbi maarufu katika Misri yote, ajifunike katika mavazi yake na atoe dhabihu kwa jina lake.", "patron": "Maombezi yao huombwa kwa ajili ya wanamuziki; wapiga filimbi."},

"Martyrs Probus, Tarachus, and Andronicus, at Tarsus in Cilicia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Probo, Tarako na Androniko waliteseka katika Kilikia mwaka wa 304, katika mateso chini ya Diokletiano. Tarako alikuwa askari mzee Mrumi wa miaka sitini na mitano, aliyeliacha jeshi badala ya kumkana Kristo; Probo alikuwa mtu wa Side, aliyeuacha utajiri kwa ajili ya imani.", "patron": "Maombezi yao huombwa kwa ajili ya askari; wazee."},

"Martyrs Processus and Martinian of Rome":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Proseso na Martiniano walikuwa walinzi wa gereza la Mamertino huko Roma, walinzi waliowekwa juu ya Mitume wakuu Petro na Paulo katika kifungo chao cha mwisho; na Kanisa linafurahia habari yao kama sura ndogo kamili ya njia ya Injili, kwa maana gereza liligeuza watu kinyume, kutoka ndani kwenda nje.", "patron": "Maombezi yao huombwa kwa ajili ya walinzi wa gereza; walinzi wa gereza walioongoka na wafungwa wao."},

"Martyrs Proclus and Hilary of Ancyra":
{"type": "Walei · karne ya 2", "life": "Mashahidi Watakatifu Proklo na Hilario walikuwa jamaa kutoka kijiji karibu na Ankira walioteseka katika mateso chini ya mfalme Trayano. Proklo alikamatwa kwanza, na alipomkiri Kristo kwa ujasiri mbele ya gavana Maksimo na akatabiri kwamba gavana mwenyewe siku moja angelazimika kumkiri Mungu wa kweli, aliteswa kikatili na akafanywa akimbie nyuma ya gari la gavana.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri wa ujasiri."},

"Martyrs Rhipsime and Gaianḗ of Armenia and those with them":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Ripsime na Gaiane na wenzao walikuwa mabikira wa jumuiya moja huko Roma, waliokimbilia Mashariki mfalme Diokletiano alipouona uzuri wa Ripsime na akataka kumtwaa kuwa mkewe; na walipofika Armenia, walikaa katika umaskini karibu na mji wa Vagharshapat, wakiishi kwa kazi ya mikono yao.", "patron": "Maombezi yao huombwa kwa ajili ya usafi; kuongoka kwa Armenia."},

"Martyrs Rusticus the Presbyter and Eleutherius the Deacon":
{"type": "Mashahidi · karne ya 1", "life": "Mashahidi Watakatifu Rustiko Kasisi na Eleftherio Shemasi walikuwa wenzake waaminifu wa Kuhani Shahidi Dionisio Mwareopago katika kazi zake za kitume katika Magharibi. Wakisafiri naye kutoka nchi hadi nchi, walishiriki mahubiri yake, hatari zake na minyororo yake, wakiwaongoa wengi kwa Kristo huko Roma na kwingineko.", "patron": "Maombezi yao huombwa kwa ajili ya urafiki wa uaminifu katika Injili."},

"Martyrs Sergius and Bacchus in Syria":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Sergio na Bako walikuwa Warumi watukufu, maafisa wa cheo cha juu katika majeshi ya nyumbani ya mfalme Maksimiano, aliyewaheshimu bila kujua kwamba wao ni Wakristo. Ilipoarifiwa kwamba hawaingii mahekaluni pamoja na baraza, mfalme aliwaamuru watoe dhabihu.", "patron": "Maombezi yao huombwa kwa ajili ya askari; urafiki mtakatifu."},

"Martyrs Simeon, Isaac and Bachtisius, of Persia":
{"type": "Shahidi · karne ya 4", "life": "Mashahidi Watakatifu Simeoni, Isaka na Bakhtisio waliteseka kwa ajili ya Kristo katika Persia, miongoni mwa jeshi kubwa la mashahidi ambao Kanisa la himaya ya Kiajemi lilimpa Mungu katika karne ya nne, wakati mamlaka ya Kizoroasta ilipoinuka dhidi ya waamini.", "patron": "Kristo alikiriwa dhidi ya ibada ya moto."},

"Martyrs Solochon, Pamphamer, and Pamphalon, at Chalcedon":
{"type": "Shahidi · karne ya 4", "life": "Mashahidi Watakatifu Solokoni, Pamfameri na Pamfaloni walikuwa askari, Wamisri kwa kuzaliwa, waliotumika katika jeshi la Kirumi huko Kalkedoni katika Bithinia katika utawala wa mfalme Maksimiano, katika mwanzo wa karne ya nne, nao waliteseka pamoja kwa kukataa dhabihu ambayo mateso yaliifanya kuwa kipimo cha uaminifu wa askari.", "patron": "Sadaka iliyokataliwa mbele ya jemadari."},

"Martyrs Sophia, Irene, and Castor of Egypt":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Sofia na Irene waliteseka kwa ajili ya Kristo katika Misri katika zama za mateso, na pamoja nao anakumbukwa Shahidi Kastori. Juu ya pambano lao machache yamehifadhiwa zaidi ya ushuhuda wa kalenda za kale, zinazoandika kwamba wanawake watakatifu, walipokwisha kumkiri Kristo mbele ya watesi wao na kukataa kutoa dhabihu kwa sanamu, walikatwa vichwa kwa upanga, na kwamba Kastori naye aliumaliza mwendo wake katika shahada.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyrs Theodore and his son, John, of Kyiv":
{"type": "Walei · karne ya 10", "life": "Mashahidi Watakatifu Theodoro Mvarangi na mwanawe Yohane walikuwa mashahidi wa kwanza wa nchi ya Urusi, wakiishi Kyiv katika karne ya kumi, katika siku kabla Mkuu Vladimiri hajaikumbatia imani. Theodoro, Mvarangi kwa asili na Mkristo, alikuwa amerudi Kyiv pamoja na mwanawe mdogo Yohane.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri mbele ya ibada ya sanamu."},

"Martyrs Theodotus and Rufina of Caesarea, in Cappadocia":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Theodoto na Rufina, wazazi wa Shahidi Mkuu Mamas, walikuwa wa jamaa tukufu na waliheshimiwa na wote kwa uchaji Mungu wao wa Kikristo. Hakimu wa Gangra alipowaita kwa kukataa kuziabudu sanamu kama amri ya kifalme ilivyoagiza, Theodoto hakukubali, na kwa kuwa cheo chake kitukufu kilimkataza hakimu kumwadhibu, alipelekwa kwa gavana Fausto huko Kaisaria katika Kapadokia, aliyemtupa gerezani mara moja.", "patron": "Maombezi yao huombwa kwa ajili ya wanandoa; ukiri thabiti."},

"Martyrs Theodotus, Asclepiodotus, and Maximus, of Adrianopolis":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Theodoto, Asklepiodota na Maksimo waliteseka mwanzoni mwa karne ya nne, katika mateso chini ya Maksimiano Galerio. Maksimo na Asklepiodota walikuwa raia mashuhuri wa Marcianopoli katika Thrakia walioishi maisha ya uchaji Mungu ya Kikristo, na pamoja na Theodoto walisingiziwa kwa ajili ya imani na wakaletwa mahakamani.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyrs Thyrsos, Leukios, and Kallinikos":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Tirso, Leukio na Kalinikos waliteseka Apolonia katika Bithinia karibu mwaka wa 250, katika mateso ya Desio. Leukio alilifungua pambano: akiuona ukatili uliotendwa kwa Wakristo, alimkemea gavana Kumbrikio uso kwa uso kwa kupigana vita na Mungu, na baada ya mateso alikatwa kichwa, ujasiri wake ukiuwasha mji.", "patron": "Maombezi yao huombwa kwa ajili ya wakata mbao; makasisi walioongoka kutoka ibada ya sanamu."},

"Martyrs Timothy, Agapius, and Thekla, of Palestine":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Timotheo, Agapio na Thekla waliteseka kwa ajili ya Kristo mwaka wa 304, katika mateso chini ya Diokletiano. Mtakatifu Timotheo alikuwa mzaliwa wa Kaisaria katika Palestina, aliyekuwa amejifunza Maandiko matakatifu na, akiwa na kipaji cha ufasaha, akawa mwalimu wa imani ya Kikristo. Alipokamatwa na kuamriwa amkane Kristo na kutoa dhabihu kwa sanamu, alikataa kwa uthabiti, na baada ya kuvumilia mateso makali alichomwa akiwa hai, akiitoa roho yake kwa Mungu.", "patron": "Maombezi yao huombwa kwa ajili ya ukiri thabiti."},

"Martyrs Trophimus and Eucarpus of Nicomedia":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Trofimo na Eukarpo walikuwa askari huko Nikomedia katika siku za mateso makuu, karibu mwaka wa 300, nao walianza upande usio sahihi wake: watu wenye kiburi na jeuri, wenye bidii katika kuwawinda Wakristo, waliojulikana miongoni mwa watesi kwa ukatili wao katika kuwafuatilia waamini, kuwakokota mahakamani na kujitajirisha kwa hofu ile, watekelezaji wawili wa amri wakitoka kwa shughuli ileile ambayo ingewakomesha.", "patron": "Maombezi yao huombwa kwa ajili ya watesi walioongoka; askari walioachana na ukatili."},

"Martyrs Trophimus, Sabbatius, and Dorymedon of Synnada":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Trofimo, Sabatio na Dorimedoni waliteseka kwa ajili ya Kristo katika utawala wa mfalme Probo. Trofimo na Sabatio, wakija Antiokia wakati wa sikukuu ya kipagani yenye ghasia, walihuzunika kwa tamasha lile na wakawaombea waliopotoka, na hapo walionekana, wakakamatwa na kuletwa mbele ya gavana; na wakiikiri imani bila kusita, Sabatio alikufa chini ya mateso yake makali, huku Trofimo akipelekwa, akivishwa viatu vya chuma vyenye misumari, katika safari ndefu kwenda Sinnada katika Frigia kwa mateso makali zaidi.", "patron": "Maombezi yao huombwa kwa ajili ya urafiki katika Kristo; kuwatunza wafungwa."},

"Martyrs Valentine and Pasikrates in Moesia, Bulgaria":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Pasikrate na Valentino walikuwa askari wa ngome ya Dorostolo kando ya Danube, ngome ya mpakani ya Moesia katika nchi za Bulgaria ya sasa, nao waliteseka chini ya gavana Absolano, mwaka wa 228 kama vitabu vihesabuvyo kwa kawaida, vijana wa miaka ishirini na miwili na thelathini ambao kikosi chao kilikuwa ulimwengu wao na ambao Kristo wao alikizidi kikosi chao cheo.", "patron": "Maombezi yao huombwa kwa ajili ya askari vijana; ndugu na wenzao katika jeshi."},

"Martyrs Victorinus, Victor, Nikēphóros, Claudius, Diodorus, Serapion, and Papias, of Egypt":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu Viktorino, Viktori, Nikeforo, Klaudio, Diodoro, Serapioni na Papia waliteseka Korintho mwaka wa 251, katika mateso chini ya mfalme Desio, Wakristo saba wa mji ule waliokamatwa katika mavuno ya himaya nzima ambayo Desio aliyaamuru alipowaagiza raia wote watoe dhabihu au wafe. Walipoletwa mbele ya mahakama, wale saba walikiri kwa sauti moja.", "patron": "Maombezi yao huombwa kwa ajili ya vikundi vya marafiki; wanaokabili majaribu ya namna mbalimbali."},

"Martyrs Zeno and his servant, Zenas, of Philadelphia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi Watakatifu Zeno na Zena mtumishi wake waliteseka kwa ajili ya Kristo huko Filadelfia katika Arabia katika mateso ya wafalme, na habari yao ni ushuhuda wa undugu ambao imani inaufanya kati ya bwana na mtumishi.", "patron": "Mabwana na watumishi wao; wanaowaacha huru watumwa wao."},

"Martyrs and Passion-Bearers Boris and Gleb":
{"type": "Wakuu · karne ya 11", "life": "Watakatifu Boris na Gleb, waitwao Roman na Davidi katika ubatizo mtakatifu, walikuwa wana wadogo wa Mtakatifu Vladimiri, mbatizaji wa Urusi, nao walikuwa watakatifu wa kwanza waliotukuzwa katika nchi ya Urusi. Baba yao alipokufa mwaka wa 1015, ndugu yao mkubwa Sviatopolk aliuteka kiti cha enzi cha Kyiv na akaazimia kuwaangamiza ndugu zake ili atawale bila mshindani.", "patron": "Maombezi yao huombwa kwa ajili ya kutopinga uovu; upendo wa kindugu."},

"Martyrs and Unmercenaries Cosmas and Damian in Cilicia, and their brothers, Leontius, Anthimus, and Eutropius":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Watakatifu na Wasiopokea-Malipo Kosma na Damiano wa Arabia, ambao Kanisa linawatofautisha na jozi mbili nyingine za ndugu watakatifu wasiopokea malipo wa majina yale yale, walikuwa matabibu waliosafiri katika miji na vijiji wakiwaponya wagonjwa bila malipo, wakiwaomba wale waliowaponya imani katika Kristo peke yake, na kwa sanaa yao na ukarimu wao waliwavuta wengi kwenye kumjua Mungu.", "patron": "Maombezi yao huombwa kwa ajili ya madaktari; waponyaji."},

"Martyrs of the Kvabtakhevi Monastery in Georgia":
{"type": "Mashahidi · karne ya 14", "life": "Mashahidi Watakatifu wa monasteri ya Kvabtakhevi waliteseka mwaka wa 1386, wakati Timur, aitwaye Tamerlane, alipoyamimina majeshi yake katika Georgia katika utawala wa Mfalme Bagrat wa Tano, uvamizi mmoja kati ya saba ambao pigo lile lilishukia nchi, likibomoa makanisa, likichukua hazina za karne nyingi na likiwakata watu wa Kartli.", "patron": "Maombezi yao huombwa kwa ajili ya watawa wakati wa uvamizi; makutaniko yasiyokubali kutawanyika."},

"Meeting of the Vladimir Icon of the Mother of God":
{"type": "Sikukuu · karne ya 16", "life": "Siku hii Kanisa linaadhimisha mojawapo ya sikukuu tatu kuu za Ikoni ya Vladimir ya Mzazi-Mungu Mtakatifu Zaidi, mlinzi wa nchi ya Urusi, iliyowekwa kwa shukrani kwa ukombozi wa Moscow kutoka uvamizi wa Watatari wa mwaka wa 1521.", "patron": "Moscow iliokolewa kutoka kwa Mtatari bila vita."},

"Monastic Martyr Adrian of Poshekhonye, Yaroslavl":
{"type": "Abate, Shahidi Mtawa · karne ya 16", "life": "Mheshimiwa Adriano wa Poshekhonye, Shahidi Mtawa, aliundwa katika maisha ya utawa katika monasteri ya Mheshimiwa Korniliy wa Komel, ambako akawa mchoraji stadi wa ikoni, mmoja wa kikundi cha ndugu wenye vipaji waliokusanyika kumzunguka mzee yule mkuu.", "patron": "Maombezi yake huombwa kwa ajili ya wachora ikoni; waanzilishi."},

"Monastic Martyr Anastasia of Rome":
{"type": "Mtawa wa kike · karne ya 3", "life": "Mheshimiwa Anastasia Mrumi, Shahidi Mtawa, aliachwa yatima akiwa na miaka mitatu na akalelewa katika jumuiya ya mabikira karibu na Roma na mzee mtakatifu wa kike Sofia, aliyemuunda katika sala, kufunga na upendo wa Kristo, hata alipokua uzuri wa roho yake ulizidi kung'aa kuliko uzuri mkubwa wa uso wake.", "patron": "Maombezi yake huombwa kwa ajili ya watawa wa kike; ubikira."},

"Monastic Martyr Andrew of Crete":
{"type": "Mtawa · karne ya 8", "life": "Mheshimiwa Andrea wa Krete, Shahidi Mtawa, ambaye Kanisa linamtofautisha na mtunga nyimbo mkuu wa jina lile lile na kisiwa kile kile, alikuwa mjinyimaji wa Krete katika siku ambazo mfalme Konstantino Kopronimo alipowaka dhidi ya ikoni takatifu, akiwatesa na kuwaua watawa waliozitetea. Aliposikia habari za mateso ya wakiri, Andrea aliuacha utulivu wake.", "patron": "Maombezi yake huombwa kwa ajili ya kuheshimu ikoni takatifu; ujasiri mbele ya wafalme."},

"Monastic Martyr Bademus (Vadim) of Persia":
{"type": "Shahidi Mtawa · karne ya 4", "life": "Mheshimiwa Bademo, aitwaye Vadimu, Shahidi Mtawa na arkimandriti wa Persia, alikuwa mtu tajiri wa Bethlapeta aliyeitoa mali yake kwa maskini na maisha yake kwa Mungu, akianzisha monasteri karibu na mji wake na akiwaunda wanafunzi katika mafundisho ya jangwani ya kufunga, kukesha na sala isiyokoma, abate wa utamu na utulivu kiasi kwamba sifa yake ilienea katika Persia yote katika miaka yaleyale ambayo mateso ya Mfalme Sapori yalikuwa yakiipekua.", "patron": "Maombezi yake huombwa kwa ajili ya maabate; waliouawa na walioikana imani."},

"Monastic Martyr Christopher of Dionysiou, Mount Athos":
{"type": "Shahidi Mtawa · karne ya 19", "life": "Mheshimiwa Kristoforo wa Dionisiu, Shahidi Mtawa, alitembea njia ambayo Kanisa la karne za Kituruki lilikuja kuiita toba ya waliokana, kitubio kigumu kuliko chote ambacho hekima yake ya kichungaji iliwahi kukiweka; kwa maana Kristoforo, Mkristo wa eneo la Adrianopoli, katika ujana wake, katika saa ya udhaifu chini ya shinikizo, hofu au tamaa, alikuwa ameikana imani na kupokelewa katika dini ya washindi, kuanguka ambako zama zile ziliwezesha na kurudi kutoka kwake ambako ziliadhibu kwa kifo.", "patron": "Maombezi yake huombwa kwa ajili ya wanaotubu wanaotafuta kurekebisha kukana; watawa wa Dionisiu."},

"Monastic Martyr Damascene of the Lavra":
{"type": "Mtawa · karne ya 17", "life": "Mheshimiwa Damaskino wa Lavra, Shahidi Mtawa, alizaliwa katika mtaa wa Galata wa Konstantinopoli kwa wazazi wacha Mungu Kiriako na Kiriaki, waliomwita mwanao Diamante. Akiachwa yatima akiwa mdogo na bila mwongozo, kijana alianguka katika maisha yasiyo na utaratibu, na alipokamatwa siku moja katika tendo lisilo halali, alijiokoa na adhabu kwa kukubali kuipokea dini ya washindi.", "patron": "Maombezi yake huombwa kwa ajili ya toba baada ya kukana; kuoshwa kwa kuikana imani katika damu."},

"Monastic Martyr Euphrosynus of Blue Jay Lake, Novgorod":
{"type": "Shahidi Mtawa · karne ya 17", "life": "Mheshimiwa Efrosino wa Ziwa la Bluu, Shahidi Mtawa, alikuwa Mkarelia kwa kuzaliwa, aliyelelewa karibu na Ladoga katika mzunguko wa monasteri kubwa ya Valaamu, na akalitumikia Kanisa kwanza kama msomaji kabla ya kupokea unyoaji katika monasteri ya Kulala ya Tikhvin.", "patron": "Maombezi yake huombwa kwa ajili ya wanaobaki wakati wengine wanapaswa kukimbia; wapweke wa nchi za mipakani."},

"Monastic Martyr Eustratius of the Kyiv Near Caves":
{"type": "Shahidi Mtawa · karne ya 11", "life": "Mheshimiwa Eustratio wa Mapango ya Karibu ya Kyiv, Shahidi Mtawa, aitwaye Mfungaji, alikuwa Mkyiv aliyeutoa urithi wake kwa maskini na akapokea unyoaji katika Mapango, ambako kufunga kwake kulikuwa kukali kiasi kwamba ndugu walimpa jina analolichukua.", "patron": "Maombezi yake huombwa kwa ajili ya mateka; wanaofunga."},

"Monastic Martyr Euthymius of Prodromou, Mount Athos":
{"type": "Shahidi Mpya · karne ya 19", "life": "Mheshimiwa Euthimio wa skete ya Prodromou katika Mlima Athos, Shahidi Mpya, alizaliwa akiitwa Eleftherio huko Demitsana katika Peloponeso kwa wazazi wacha Mungu, na akaanguka katika ujana wake kwa njia ambayo mashahidi wapya wengi waliipita: akitupwa kati ya Waturuki katika kutangatanga kwake, akishinikizwa na kunaswa, kijana yule katika saa ya udhaifu alimkana Kristo na akaipokea dini ya washindi, akipata usalama wa ulimwengu na kuipoteza amani yake mwenyewe, kwa maana kukana hakukumpa raha mchana wala usiku, na toba ikainuka ndani yake kama homa ambayo dawa moja tu ingeweza kuipoza.", "patron": "Maombezi yake huombwa kwa ajili ya waliokana na wangependa kurudi; vijana katika toba."},

"Monastic Martyr Joseph of Dionysiou, Mount Athos":
{"type": "Mtawa · karne ya 19", "life": "Mheshimiwa Yosefu alikuwa mtawa wa monasteri ya Dionisiu katika Mlima Athos, ambako aling'aa katika fadhila za maisha ya utawa na akafanya kazi kama mchoraji wa ikoni, akiichora ikoni ya Malaika Wakuu watakatifu kwa ajili ya ikonostasi ya kanisa kuu la monasteri. Kwa utii kwa abate wake Stefano, alisafiri hadi Konstantinopoli kama mwandani wa Eudokimo fulani, aliyekuwa ameikana imani na sasa, akitubu, alitamani kukiosha kukana kwake kwa kufa shahidi.", "patron": "Maombezi yake huombwa kwa ajili ya wachora ikoni; ukiri thabiti."},

"Monastic Martyr Macarius of Dionysiou, Mount Athos":
{"type": "Mtawa kuhani · karne ya 16", "life": "Mheshimiwa Makario alikuwa mtawa wa monasteri ya Dionisiu katika Mlima Athos na mwanafunzi wa Patriaki mtakatifu Nifoni wa Konstantinopoli, aliyejitaabisha katika monasteri hiyo katika miaka yake ya kustaafu; na kwa mzee wake Makario alijifunza utii, sala na upendo uwakao kwa Kristo. Akiwaka kwa shauku ya kumshuhudia Bwana wake kati ya waliomkana, alipokea baraka ya Mtakatifu Nifoni, aliyeutabiri mwisho wake, na akaenda Thesalonike, ambako alianza kumhubiri Kristo waziwazi kwa Waturuki na kuwaita watoke katika upotovu wao.", "patron": "Maombezi yake huombwa kwa ajili ya wahubiri; mahubiri ya ujasiri."},

"Monastic Martyr Macarius of Saint Anne Skete, Mount Athos":
{"type": "Mtawa · karne ya 16", "life": "Mheshimiwa Makario Shahidi Mpya alizaliwa Kios katika Bithinia, na katika ujana wake, katika siku za nira ya Kiothmani, alivutwa kwa nguvu na udanganyifu kuelekea dini ya washindi, jeraha lililowaka katika dhamiri yake tangu wakati ule. Akikimbilia Mlima Mtakatifu wa Athos, alifika katika skete ya Mtakatifu Anna, ambako alipokelewa, akanyolewa, na akaundwa katika toba, sala na machozi chini ya wazee wa mahali pale patakatifu.", "patron": "Maombezi yake huombwa kwa ajili ya toba iliyotiwa muhuri kwa damu; ukiri thabiti."},

"Monastic Martyr Paul of the Lavra, Mount Athos":
{"type": "Shahidi", "life": "Mheshimiwa Paulo wa Lavra katika Mlima Athos, Shahidi Mtawa, anakumbukwa na Kanisa siku hii kama mmoja wa watakatifu wake, ingawa juu ya mambo ya maisha yake na pambano lake hakuna kumbukumbu iliyotufikia, na vitabu vya kawaida vinakiri waziwazi kwamba hakuna habari yake iliyosalia.", "patron": "Taji iliyoshindwa na habari isiyoandikwa."},

"Monastic Martyr and Confessor Stephen the New":
{"type": "Mtawa · karne ya 8", "life": "Mheshimiwa Stefano Mpya, Shahidi Mtawa na Mkiri, shujaa mkuu wa ikoni takatifu, alizaliwa mwaka wa 715 huko Konstantinopoli kwa wazazi wacha Mungu ambao, wakiwa na binti wawili, walimwomba Bwana awape mwana; na mama yake, alipompokea, alimchukua mtoto mchanga hadi kanisa la Blakerne la Mzazi-Mungu Mtakatifu Zaidi na akamweka wakfu kwa Mungu mbele ya ikoni yake.", "patron": "Maombezi yake huombwa kwa ajili ya watawa; watetezi wa ikoni."},

"Monastic Martyrs Conon and his son, Conon, of Iconium":
{"type": "Kuhani Shahidi, na mwanawe · karne ya 3", "life": "Waheshimiwa Konon na mwanawe Konon, Mashahidi Watawa, waliteseka Ikonio katika Asia Ndogo katika utawala wa mfalme Aureliano. Konon mzee, aliyeachwa mjane, aliingia katika monasteri pamoja na mwanawe, na kwa utakatifu wa maisha yake alipewa neema kutoka juu, akiwatoa mapepo, akiwaponya wagonjwa, akiwapa vipofu kuona, na akimhubiri Kristo kati ya wapagani, na kwa hayo aliwaongoa wengi.", "patron": "Maombezi yao huombwa kwa ajili ya baba wajane; baba na wana."},

"Monastic Martyrs Menas, David, and John, of Palestine":
{"type": "Mashahidi Watawa · karne ya 7", "life": "Waheshimiwa Mena, Davidi na Yohane wa Palestina, Mashahidi Watawa, walikuwa watawa wa Palestina, wajinyimaji wa jumuiya za jangwani zilizoyabeba mapokeo ya Hariton, Euthimio na Sava katika karne zilizofuata baada ya ushindi wa Waajemi na Waarabu kuivunja amani ya kale ya Nchi Takatifu.", "patron": "Maombezi yao huombwa kwa ajili ya watawa waliouawa kwenye vyumba vyao; waamini wasioandikwa katika kumbukumbu."},

"Monastic Martyrs and Confessors Auxentius, Basil, Gregory, another Gregory, John, Andrew, Peter and many others":
{"type": "Mashahidi · karne ya 8", "life": "Mashahidi watakatifu na Wakiri Auksentio, Basili, Gregorio, Gregorio mwingine, Yohane, Andrea, Petro na wengine wengi waliteseka kwa ajili ya kuheshimiwa kwa ikoni takatifu katika mateso ya Konstantino Kopronimo, pamoja na Shahidi Mtawa Stefano Mpya. Hawa walikuwa wakiri, wengi wao watawa, ambao mfalme mpinga-ikoni alikuwa amewakusanya kutoka katika milki yote hadi katika magereza ya Konstantinopoli, watu waliokuwa tayari wakichukua mwilini mwao alama za mateso, waliochapwa mijeledi, kutiwa chapa ya moto, na kukatwa pua na masikio na mikono na macho kwa kukataa kuikufuru sanamu ya Kristo.", "patron": "Maombezi yao huombwa kwa ajili ya watawa; ikoni takatifu."},

"Myrrhbearer and Equal of the Apostles Mary Magdalene":
{"type": "Sawa na Mitume · karne ya 1", "life": "Mtakatifu Maria Magdalena, Mchukua-Manukato na Sawa na Mitume, alimfuata Kristo baada ya kumponya na akawa mmoja wa wanawake wachukua-manukato. Alisimama karibu na Msalaba, akaja kaburini na manukato, na akawa wa kwanza kuutangaza Ufufuo kwa mitume. Baadaye alimhubiri Kristo na akalala katika karne ya kwanza."},

"Nativity of the Holy Glorious Prophet, Forerunner and Baptist, John":
{"type": "Nabii · karne ya 1", "life": "Sikukuu hii inaadhimisha kuzaliwa kwa Mtakatifu Yohane Mtangulizi, mwana wa kuhani Zakaria na Elisabeti mwenye haki. Kuzaliwa kwake, kulikotangazwa na Malaika Mkuu Gabrieli, kuliumaliza ugumba wa Elisabeti na ukimya wa Zakaria. Yohane alijazwa Roho Mtakatifu tangu tumboni mwa mama yake na akaiandaa njia ya Kristo."},

"New Martyr Anastasius of Epirus":
{"type": "Shahidi · karne ya 18", "life": "Shahidi Mpya Anastasio wa Paramythia katika Epiro aliteseka chini ya nira ya Kiothmani mwaka wa 1750. Kijana Mgiriki Mkristo wa mji ule, alikamatwa na watu wa mtawala wa mahali pale na, akiwa amesingiziwa, akapewa chaguo lililowavunja au kuwavika taji wengi wa kizazi chake: kuipokea dini ya washindi na kuishi kwa heshima, au kubaki Mkristo na kufa.", "patron": "Maombezi yake huombwa kwa ajili ya Kanisa lililotiwa utumwani; ushuhuda unaoiongoa nyumba ya mtesi."},

"New Martyr Archpriest Vasily Martysz":
{"type": "Shahidi · karne ya 20", "life": "Shahidi Mpya Kasisi Mkuu Vasili Martysz aliziunganisha katika maisha moja dunia mbili za Kiorthodoksi za Alaska na Poland, na akazitia muhuri zote mbili kwa kifo katika Ijumaa Kuu.", "patron": "Safari za mtumbwi za Alaska."},

"New Martyr Ephraim":
{"type": "Shahidi · karne ya 15", "life": "Kuhani Shahidi Efraimu wa Nea Makri, Aliyefunuliwa Karibuni, alifichwa na Mungu kwa miaka mia tano na akapewa Kanisa katika hitaji lake la kisasa, na maisha yake kwa hiyo yanasimuliwa kutoka ncha zake zote mbili.", "patron": "Miezi minane ya mateso iliyovumiliwa."},

"New Martyr Euthymius of Mount Athos":
{"type": "Shahidi · karne ya 19", "life": "Mheshimiwa Euthimio wa Mlima Athos, Shahidi Mpya, anayekumbukwa siku hii katika sinaksi ya pamoja ya mashahidi wapya watatu wa Skete ya Mtangulizi, alizaliwa Demetsana katika Peloponeso, mji wa milimani uliolipa taifa la Ugiriki makasisi na mashahidi wake wengi.", "patron": "Kuikana imani kwa ujana kulikooshwa kwa damu."},

"New Martyr Habakkuk":
{"type": "Mtawa · karne ya 17", "life": "Mheshimiwa Habakuki, Shahidi Mpya, alimshuhudia Kristo katika mji mkuu wa Thesalonike mwaka wa 1628, wakati wa usiku mrefu wa nira ya Kituruki. Karibu hakuna kitu cha maisha yake kilichohifadhiwa, kwa maana hakuna habari kamili ya kufa kwake shahidi iliyosalia; kumbukumbu yake inajulikana tu kutoka ukumbusho mfupi ulioandikwa katika hati ya Lavra Kuu katika Mlima Athos, unaosema kwamba katika mwezi wa Agosti Habakuki mheshimiwa alitoa ushuhuda wake kwa Kristo, kwa utukufu na fahari ya Wakristo Waorthodoksi.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri thabiti wakati wa mateso."},

"New Martyr Ignatius the Martyr of Mount Athos":
{"type": "Shahidi · karne ya 19", "life": "Mheshimiwa Ignatio wa Mlima Athos, Shahidi Mpya, anayekumbukwa siku hii pamoja na Euthimio na Akakio katika sinaksi ya mashahidi wapya watatu wa Skete ya Mtangulizi, alizaliwa akiitwa Yohane huko Stara Zagora katika Bulgaria.", "patron": "Ahadi iliyodaiwa kwa woga, isiyosemwa katika damu."},

"New Martyr John Kalphes, the Apprentice":
{"type": "Shahidi Mpya · karne ya 16", "life": "Shahidi Mpya Yohane Kalfe aliteseka Konstantinopoli mwaka wa 1575, katika kizazi cha pili baada ya kuanguka kwa Mji, na cheo chake ni kazi yake: kalfe, fundi mkuu wa ujenzi aliyehitimu, kwa maana Yohane alikuwa fundi kijana stadi wa karakana za kifalme, Mkristo ambaye ubora wake ulikuwa umemwingiza katika utumishi wa baraza la Waothmani lenyewe, ambako alijenga na kumalizia kwa ajili ya washindi kwa uaminifu wa fundi, akiheshimiwa na wakuu kwa ufundi wake na kwa Wakristo kwa uchaji wake na sadaka zake za ukarimu.", "patron": "Maombezi yake huombwa kwa ajili ya wajenzi; maseremala."},

"New Martyr John the New of Epirus":
{"type": "Shahidi Mpya · karne ya 16", "life": "Shahidi Mpya Yohane wa Ioannina, aitwaye Mpya, alikuwa mshonaji kijana, aliyezaliwa katika Epiro kwa wazazi wacha Mungu, aliyekuja baada ya kifo chao Konstantinopoli na akaifanya kazi yake katika karakana karibu na eneo la kasri, mwanafunzi Mkristo kati ya mafundi Waislamu katika Mji uliokuwa umeshindwa karibuni, katika kizazi cha kwanza baada ya kuanguka kwake.", "patron": "Maombezi yake huombwa kwa ajili ya washonaji na mafundi; wanafunzi wa kazi walio chini ya mabwana wakali."},

"New Martyr John the New of Sochi, who suffered at Belgrade":
{"type": "Shahidi Mkuu · karne ya 14", "life": "Shahidi Mkuu Yohane Mpya wa Suceava alikuwa mfanyabiashara kijana wa Trapezunt kwenye Bahari Nyeusi, aliyeteseka kwa ajili ya Kristo huko Belgorod katika pwani ya Bahari Nyeusi katika karne ya kumi na nne, na akawa shahidi mkuu na mlinzi wa mbinguni wa nchi ya Moldavia.", "patron": "Maombezi yake huombwa kwa ajili ya wafanyabiashara na wasafiri; mashahidi chini ya upagani na Uislamu."},

"New Martyr Lazarus of Bulgaria":
{"type": "Shahidi Mpya · karne ya 19", "life": "Shahidi Mpya Lazaro wa Bulgaria alikuwa mchungaji kijana, aliyezaliwa kwa wazazi Wakristo katika nchi za Bulgaria, aliyekuja kusini kwa njia ya maskini wa karne zile akitafuta kazi, na akachunga makundi katika mashamba ya Pergamo katika Asia Ndogo, Mslavi aliyefanya kazi kati ya Wagiriki chini ya utawala wa Kiothmani, mgeni mara tatu na akiwa na silaha ya ubatizo wake tu.", "patron": "Maombezi yake huombwa kwa ajili ya wachungaji; waliosingiziwa."},

"New Martyrs and Confessors of Butovo":
{"type": "Mashahidi Wapya · karne ya 20", "life": "Siku hii Kanisa linawakumbuka Mashahidi Wapya na Wakiri wa Butovo, kikundi kikubwa cha waamini waliopigwa risasi kwa ajili ya Kristo katika uwanja wa kupigia risasi wa Butovo karibu na Moscow katika hofu ya miaka ya Kisovieti.", "patron": "Mashahidi wa mateso ya wasiomjua Mungu; wakleri na waamini waliouawa kwa ajili ya imani."},

"Nine Martyrs at Cyzicus: Theognes, Rufus, Antipater, Theostichus, Artemas, Magnus, Theodotus, Thaumasius, and Philemon":
{"type": "Mashahidi · karne ya 3", "life": "Mashahidi Tisa watakatifu wa Cyzicus, Theogne, Rufo, Antipatro, Theostiko, Artema, Magno, Theodoto, Thaumasio na Filemoni, walikusanywa na Mungu katika ukiri mmoja kutoka maisha tisa tofauti, wakitolewa, kama habari zisemavyo, katika miji na hali mbalimbali, askari na raia, wazee na vijana, hata kikundi chao kilikuwa mfano mdogo wa Kanisa lote, kila hali ikiwakilishwa mbele ya baraza la hukumu.", "patron": "Maombezi yao huombwa kwa ajili ya wenye homa na wanaosumbuliwa na malaria; vikundi vya waamini."},

"Nun-Martyr Eugenia of Rome":
{"type": "Shahidi Mtawa wa kike · karne ya 3", "life": "Mheshimiwa Eugenia, Shahidi Mtawa, alikuwa binti ya Filipo, mtawala wa Misri chini ya Warumi, aliyelelewa Aleksandria katika elimu yote ya zama zile; na akisoma kwa siri nyaraka za Mtume Paulo, binti ya mtawala mpagani alipata upendo wa Kristo uliyageuza maisha yake.", "patron": "Maombezi yake huombwa kwa ajili ya maabesi; wanawake waliojigeuza sura kwa ajili ya Mungu."},

"Passion-Bearer Gleb (in Baptism David)":
{"type": "Mkuu · karne ya 11", "life": "Mbeba-Mateso Gleb, aliyeitwa Daudi katika ubatizo mtakatifu, alikuwa miongoni mwa watakatifu wa kwanza waliotukuzwa katika nchi ya Rus, akiteseka mwaka wa 1015 pamoja na ndugu yake Boris kwa mikono ya ndugu yao Sviatopolk Aliyelaaniwa. Baba yao, Mkuu Mkubwa Vladimiri, alipokufa, Sviatopolk, akiwa amekwisha kumwua Boris, alimpelekea kijana Gleb habari kwamba baba yake alikuwa mgonjwa na akamwita Kyiv, akitumia hila kumvuta mrithi mwingine halali kwenye kifo chake.", "patron": "Maombezi yake huombwa kwa ajili ya wanaoteseka bila hatia; amani miongoni mwa jamaa."},

"Persian Martyrs in Martyropolis in Mesopotamia":
{"type": "Mashahidi · karne ya 4", "life": "Mashahidi watakatifu wa Kiajemi huko Martiropoli, wanaokumbukwa pamoja na Mtakatifu Marutha aliyewakusanya, ni jeshi la wale walioteseka katika mateso makuu ya milki ya Uajemi, marefu kuliko yote ambayo Kanisa limewahi kuyavumilia, wakati kwa miaka karibu arobaini chini ya Shapuri wa Pili na warithi wake dola ya Kizoroastria ilijiwekea kuwaangamiza Wakristo wa Mesopotamia na Uajemi.", "patron": "Maombezi yao huombwa kwa ajili ya walioteswa wa Mashariki; wakimbizi kwa ajili ya imani."},

"Presbyters and Confessors Eugene and Macarius, at Antioch":
{"type": "Makasisi, Wakiri · karne ya 4", "life": "Makasisi watakatifu na Wakiri Eugenio na Makario waliteseka Antiokia chini ya Yuliano Mwasi, mfalme aliyejaribu kuujenga upya upagani juu ya magofu ambayo nyumba ya mjomba wake ilikuwa imeufanya; na makasisi hao wawili walilipata cheo chao kwa njia ya moja kwa moja kuliko zote ambazo Kanisa linaziandika, kwa kumwambia Yuliano ukweli juu yake mwenyewe uso kwa uso.", "patron": "Maombezi yao huombwa kwa ajili ya makasisi uhamishoni; wanaokemea mamlaka."},

"Priestmartyr John Kochurov":
{"type": "Kasisi · karne ya 20", "life": "Kuhani Shahidi Yohane Kochurov, kuhani shahidi wa kwanza wa mapinduzi ya Urusi, alizaliwa mwaka wa 1871 katika jimbo la Ryazan, mwana wa kasisi wa kijiji, na baada ya Akademia ya Theolojia ya Petersburg alijitolea kwa misheni ya Amerika, akihudumu tangu mwaka wa 1895 kama mchungaji wa parokia ya Mtakatifu Vladimiri huko Chicago.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; makasisi wa parokia."},

"Priestmonk Jonah the Martyr of Pechenga":
{"type": "Mtawa kuhani · karne ya 16", "life": "Mheshimiwa Yona wa Pechenga, kuhani-mtawa na shahidi, alizaliwa katika kijiji cha Varzuga katika Pomorie ya kaskazini ya mbali ya Urusi, na alihudumu kwanza kama kasisi wa parokia; kisha, akivutwa kwenye monasteri ya kaskazini kuliko zote duniani, aliingia katika monasteri ya Utatu Mtakatifu ya Pechenga katika rasi ya Kola, iliyoanzishwa na Mtakatifu Trifoni kati ya Walapi ng'ambo ya mzingo wa Aktiki, na akawa mmoja wa wanafunzi wa karibu zaidi wa mwangazaji yule mkuu.", "patron": "Maombezi yake huombwa kwa ajili ya makasisi madhabahuni; watawa wa kaskazini ya mbali."},

"Procession of the Honorable Wood of the Life-Giving Cross of the Lord (First of the three “Feasts of the Savior” in August)":
{"type": "Sikukuu · kiliturujia", "life": "Mnamo tarehe moja Agosti Kanisa linaadhimisha Maandamano ya Mti Mtukufu na Hai wa Msalaba wa Bwana, sikukuu ya kwanza kati ya Sikukuu tatu za Mwokozi zinazoshikwa mwezi huu na siku ambayo Mfungo wa Kulala huanza. Sikukuu hii ilianzia katika mji wa kifalme wa Konstantinopoli, ambako, kwa sababu ya magonjwa yaliyokuja na joto la Agosti, ilikuwa desturi kuubeba Mti Mtukufu wa Msalaba katika maandamano barabarani kwa kutakaswa kwa mji na ukombozi wa watu kutoka ugonjwa.", "patron": "Ukombozi kutoka ugonjwa; kutakaswa kwa maji."},

"Prophet Amos":
{"type": "Nabii · karne ya 8 KK", "life": "Nabii Amosi mtakatifu alikuwa mmoja wa Manabii kumi na wawili Wadogo wa Agano la Kale, mchungaji aliyeitwa kutoka kundi lake ili alilie neno la Bwana dhidi ya ufalme uliostawi na uliopotoka.", "patron": "Wachungaji na vibarua walioitwa kutabiri; wanaohubiri dhidi ya dhuluma."},

"Prophet Daniel":
{"type": "Nabii · karne ya 6 KK", "life": "Nabii Danieli mtakatifu, wa ukoo wa kifalme wa Yuda, alichukuliwa Babeli akiwa kijana katika uhamisho wa kwanza, karibu miaka mia sita kabla ya Kristo, na huko, katika tanuru la uhamisho, Mungu alimfua nabii na mwanasiasa wa utumwani. Akikataa pamoja na wenzake watatu unajisi wa meza ya mfalme, alipewa hekima kuliko wote.", "patron": "Maombezi yake huombwa kwa ajili ya waliohamishwa; wakalimani."},

"Prophet Elisha":
{"type": "Nabii · karne ya 9 KK", "life": "Nabii Elisha mtakatifu alikuwa mwanafunzi, mwandani na mrithi wa Nabii Eliya mkuu, na mmoja wa manabii wenye nguvu zaidi wa Agano la Kale, ambaye maisha yake yalijaa maajabu ya rehema na uweza.", "patron": "Wanafunzi na warithi wa manabii; wanaopokea sehemu maradufu ya neema."},

"Prophet Ezekiel":
{"type": "Nabii · karne ya 6 KK", "life": "Nabii Ezekieli mtakatifu alikuwa wa kabila la Lawi, kuhani na mwana wa kuhani Buzi, na alichukuliwa utumwani Babeli akiwa na miaka ishirini na mitano, pamoja na mfalme Yekonia, watu wa Yuda walipopelekwa uhamishoni. Huko, kati ya waliohamishwa kando ya mto Kebari, neno la Bwana lilimjia, na akatabiri kwa miaka mingi, akiwaita watu kwenye toba na akiwafariji kwa tumaini la kurudi na kurejeshwa.", "patron": "Maombezi yake huombwa kwa ajili ya toba; tumaini la ufufuo."},

"Prophet Habakkuk":
{"type": "Nabii · karne ya 7 KK", "life": "Nabii Habakuki mtakatifu, wa nane kati ya manabii kumi na wawili wadogo, alikuwa wa kabila la Simeoni na alitabiri karibu mwaka wa 650 kabla ya Kristo, akiuona mbele uharibifu wa Hekalu, utumwa wa Babeli, na kurudi kwa waliohamishwa. Kitabu chake kinayahifadhi mazungumzo makuu ya mlinzi na Mungu: akisimama juu ya mnara wake ili aone Bwana atakavyojibu juu ya kufanikiwa kwa waovu, alipokea neno lililoilisha imani ya Maagano yote mawili, Ufunuo huu unasubiri wakati uliokubalika.", "patron": "Maombezi yake huombwa kwa ajili ya walinzi; imani inayosubiri maono."},

"Prophet Haggai":
{"type": "Nabii · karne ya 6 KK", "life": "Nabii Hagai mtakatifu, wa kumi kati ya manabii kumi na wawili wadogo, alizaliwa Babeli wakati wa utumwa na akapanda Yerusalemu pamoja na waliokuwa wakirudi kutoka uhamishoni; na katika mwaka wa pili wa mfalme Dario, karibu miaka mia tano na ishirini kabla ya Kristo, ujenzi upya wa Hekalu ulipokuwa umeachwa kwa kizazi kizima wakati watu wakijenga nyumba zao wenyewe zilizopambwa kwa mbao, neno la Bwana lilikuja kwa kinywa chake kama parapanda: Zitafakarini vyema njia zenu.", "patron": "Maombezi yake huombwa kwa ajili ya wajenzi; wanaojenga upya kile kilichopotea."},

"Prophet Hosea":
{"type": "Nabii · karne ya 8 KK", "life": "Nabii Hosea mtakatifu, mwana wa Beeri, alitabiri katika ufalme wa kaskazini wa Israeli katika karne ya nane kabla ya Kristo, katika vizazi vya mwisho kabla ya ufalme ule kuchukuliwa na Ashuru, na kitabu chake kinasimama cha kwanza kati ya manabii kumi na wawili wadogo. Kwa amri ya Mungu alimwoa Gomeri, mwanamke wa ukahaba, na akawapa watoto wake majina ya hukumu, ili nyumba yake mwenyewe iwe mfano hai wa Israeli, bibi arusi aliyekuwa amefuata miungu mingine.", "patron": "Maombezi yake huombwa kwa ajili ya huruma ya Mungu; kurudi kwa wasio waaminifu."},

"Prophet Isaiah":
{"type": "Nabii · Agano la Kale", "life": "Nabii Isaya mtakatifu, wa kwanza kwa cheo kati ya manabii wakuu na aitwaye na mababa mwinjilisti wa tano, alikuwa mwana wa Amozi, wa ukoo wa kifalme wa Yuda kama mapokeo yashikavyo, na akapokea utume wake katika mwaka ambao mfalme Uzia alikufa.", "patron": "Bwana aliyeonwa akiwa juu na ameinuliwa."},

"Prophet Jeremiah":
{"type": "Nabii · Agano la Kale", "life": "Nabii Yeremia mtakatifu, wa pili kwa cheo kati ya manabii wakuu, alikuwa mwana wa Hilkia, wa ukoo wa kikuhani, kutoka mji wa Anathothi katika nchi ya Benyamini, na aliitwa na Mungu akiwa bado karibu mtoto, akipinga kwamba hakuweza kusema.", "patron": "Neno kama moto lililofungwa mifupani."},

"Prophet Joad":
{"type": "Nabii · karne ya 10 KK", "life": "Nabii Yoadi mtakatifu ndilo jina ambalo mapokeo humpa mtu wa Mungu kutoka Yuda ambaye utume wake kwenda Betheli Kitabu cha Wafalme kinausimulia, mojawapo ya habari za kinabii zilizo nzito na zenye kuchunguza kuliko zote. Akitumwa kwa neno la Bwana kwenye madhabahu ya mfarakano ambayo Yeroboamu alikuwa ameiinua, Yoadi alipiga kelele dhidi ya madhabahu yenyewe, akimtaja kwa jina, karne tatu mbele, mfalme Yosia ambaye angeichoma mifupa ya watu juu yake.", "patron": "Maombezi yake huombwa kwa ajili ya wajumbe wenye ujumbe mgumu; wasiopaswa kugeuka kando."},

"Prophet Joel":
{"type": "Nabii · karne ya 9 KK", "life": "Nabii Yoeli mtakatifu, mwana wa Pethueli, alitabiri katika ufalme wa Yuda karibu miaka mia nane kabla ya Kristo, na kitabu chake kifupi kinasimama kati ya manabii kumi na wawili wadogo. Akichukua nafasi kutoka pigo la nzige na ukame vilivyoiacha nchi wazi, aliwaita makuhani na watu kwenye kufunga na toba, akilia, Rarueni mioyo yenu na siyo mavazi yenu; mrudieni Mwenyezi Mungu, Mungu wenu, kwa maana yeye ndiye mwenye neema na mwingi wa huruma.", "patron": "Maombezi yake huombwa kwa ajili ya toba; kumiminwa kwa Roho Mtakatifu."},

"Prophet Jonah":
{"type": "Nabii · karne ya 8 KK", "life": "Nabii Yona mtakatifu, mwana wa Amathi, alikuwa wa Gath-heferi katika Galilaya na alitabiri katika karne ya nane kabla ya Kristo, na kitabu chake kinasomwa katika Kanisa zaidi ya yote katika kesha la Pasaka, kwa maana katika yeye Bwana mwenyewe alitoa ishara ya kifo chake na Ufufuo wake.", "patron": "Maombezi yake huombwa kwa ajili ya toba; walio kilindini."},

"Prophet Nahum":
{"type": "Nabii · karne ya 7 KK", "life": "Nabii Nahumu mtakatifu, ambaye jina lake lina maana Mungu hufariji, alikuwa wa kijiji cha Elkoshi katika Galilaya, na alitabiri katika karne ya saba kabla ya Kristo, wa saba kwa mpango kati ya manabii kumi na wawili wadogo. Kitabu chake kifupi ni unabii mmoja uwakao dhidi ya Ninawi, mji mkuu wa Ashuru, uliokuwa umeiponda Israeli na kuyachukua makabila kumi.", "patron": "Maombezi yake huombwa kwa ajili ya faraja ya walioteswa; wanaosumbuliwa na matatizo ya akili."},

"Prophet Obadiah (Abdia)":
{"type": "Nabii · karne ya 9 KK", "life": "Nabii Obadia mtakatifu, ambaye kitabu chake, kifupi kuliko vyote katika Agano la Kale, kinasimama kati ya manabii kumi na wawili wadogo, alitabiri hukumu ya Mungu juu ya Edomu, taifa ndugu lenye kiburi lililoshangilia juu ya kuanguka kwa Yerusalemu: Ingawa unapaa juu kama tai na kufanya kiota chako kati ya nyota, nitakushusha chini kutoka huko, asema Mwenyezi Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya wasimamizi wa mali; kushushwa kwa kiburi."},

"Prophet Samuel":
{"type": "Nabii · karne ya 11 KK", "life": "Nabii Samweli alikuwa wa kumi na tano na wa mwisho kati ya Waamuzi wa Israeli na wa kwanza kati ya manabii wakuu baada ya Musa, akiishi zaidi ya miaka elfu moja na mia moja kabla ya kuja kwa Kristo. Alizaliwa kwa sala za bidii za mama yake Hana, aliyekuwa tasa kwa muda mrefu, na kwa kuwa alikuwa amemwomba kwa Bwana akamwita Samweli.", "patron": "Maombezi yake huombwa kwa ajili ya manabii; wanaotafuta watoto."},

"Prophet Zephaniah":
{"type": "Nabii · karne ya 7 KK", "life": "Nabii Sefania mtakatifu, wa tisa kati ya manabii kumi na wawili wadogo, alikuwa wa damu ya kifalme, akiufuata ukoo wake katika mwanzo wa kitabu chake kwa vizazi vinne hadi Mfalme Hezekia; naye alitabiri Yerusalemu katika siku za Mfalme Yosia kijana, katika karne ya saba kabla ya Kristo, mwenzake wa Yeremia na sauti iliyoyaandaa marekebisho makuu ya utawala ule.", "patron": "Maombezi yake huombwa kwa ajili ya kutafuta upole; furaha iliyoahidiwa baada ya hukumu."},

"Prophetess Hannah the mother of the Prophet Samuel":
{"type": "Nabii wa kike · karne ya 11 KK", "life": "Nabii wa kike Hana mtakatifu, mama wa Nabii Samweli, alikuwa mke wa Elkana wa Ramathaimu, tasa kwa miaka mingi na akijeruhiwa kila siku na uchokozi wa mshindani wake; na akipanda kwenye patakatifu pa Shilo, aliimimina roho yake mbele za Bwana, akilia na kuweka nadhiri kwamba kama angempa mwana, angemrudisha mtoto kwake siku zote za maisha yake.", "patron": "Maombezi yake huombwa kwa ajili ya mama; wasiozaa wanaosali."},

"Protomartyr and Archdeacon Stephen":
{"type": "Shemasi Mkuu · karne ya 1", "life": "Shahidi wa Kwanza na Shemasi Mkuu Stefano alikuwa wa kwanza wa mashemasi saba waliochaguliwa na mitume, mtu aliyejaa imani na Roho Mtakatifu, na aliyejaa neema na nguvu, aliyetenda maajabu makuu kati ya watu.", "patron": "Maombezi yake huombwa kwa ajili ya mashemasi; wahubiri."},

"Protomartyr and Equal of the Apostles Thekla":
{"type": "Shahidi · karne ya 1", "life": "Shahidi wa Kwanza na Sawa na Mitume Thekla alizaliwa Ikonio katika jamaa tukufu, na akiwa na miaka kumi na minane, akiwa amechumbiwa na kijana wa mji, alisikia kutoka dirishani mwake mahubiri ya Mtume Paulo juu ya ubikira na ufalme wa Mungu, na moyo wake ukawaka kiasi kwamba kwa siku tatu hakula wala hakunywa, bali alining'inia juu ya maneno yake.", "patron": "Maombezi yake huombwa kwa ajili ya mabikira; wanaoacha vyote kwa ajili ya Kristo."},

"Recovery of the Relics (1650) and the Second Glorification (1909) of the Holy Venerable Right-believing Great Princess Anna of Kashin, Wonderworker":
{"type": "Mkuu wa kike · karne ya 14", "life": "Siku hii Kanisa linakumbuka kupatikana kwa masalia mwaka wa 1650 na kutangazwa mtakatifu mara ya pili mwaka wa 1909 kwa Mkuu wa Kike Mkubwa Ana wa Kashin mwenye imani sahihi, mwanamke ambaye maisha yake yalikuwa kufa shahidi kwa muda mrefu katika huzuni na ambaye kuheshimiwa kwake kwenyewe kulipita katika kukandamizwa na kurudishwa.", "patron": "Wajane na mama wanaoomboleza; wanaopoteza vyote na kuhifadhi imani."},

"Recovery of the relics of Saint Job of Pochaiv":
{"type": "Abate · karne ya 17", "life": "Mheshimiwa Ayubu, abate na mtenda-miujiza wa Pochaev, alikuwa mmoja wa watetezi wakuu wa Uorthodoksi katika nchi za magharibi za Urusi katika zama za Muungano wa Brest, wakati waamini wa Volinia walipobanwa vikali wainame kwa Roma. Alinyolewa katika ujana wake na baadaye akaitwa kuiongoza monasteri juu ya mlima wa Pochaev.", "patron": "Maombezi yake huombwa kwa ajili ya watawa; utetezi wa Uorthodoksi."},

"Repose of Saint Alexander Nevsky":
{"type": "Mkuu · karne ya 13", "life": "Siku hii Kanisa linakumbuka kulala kwa Mkuu Aleksanda Nevsky mtakatifu, mtetezi wa Rus katika karne yake ya giza kuliko zote. Akizaliwa mwaka wa 1220 huko Pereslavl-Zalessky, mwana wa Mkuu Yaroslav, alikuwa bado kijana wa miaka ishirini wakati Waswidi walipopanda mto Neva dhidi ya Novgorod.", "patron": "Maombezi yake huombwa kwa ajili ya askari; mabalozi."},

"Repose of Saint Alexis Toth, Confessor and Defender of Orthodoxy in America":
{"type": "Mkiri · karne ya 20", "life": "Mtakatifu Aleksi Toth, Mkiri na Mtetezi wa Uorthodoksi katika Amerika, alitimiza kwa mlango mmoja uliofungwa kile ambacho kamati hazikitimizi kwa mia moja iliyo wazi.", "patron": "Mlango uliofungwa Minneapolis na mlango mkubwa zaidi uliofunguliwa."},

"Repose of Saint Arsenius, Archbishop of Serbia":
{"type": "Askofu Mkuu · karne ya 13", "life": "Mtakatifu Arsenio, Askofu Mkuu wa Serbia, alizaliwa Srem na akawa mtawa katika monasteri ya Zhicha chini ya uongozi wa Mtakatifu Sava, askofu mkuu wa kwanza wa Waserbia, ambaye kwa ukali wa maisha yake alimfanya abate wa monasteri ile ya kifalme. Majeshi ya Kihungaria yalipoitishia nchi, Sava alimtuma Arsenio kusini ili atafute makao salama zaidi kwa Kanisa.", "patron": "Maombezi yake huombwa kwa ajili ya wakuu wa Kanisa; Kanisa la Serbia."},

"Repose of Saint Cyprian, Metropolitan of Moscow and All Russia":
{"type": "Metropolita · karne ya 15", "life": "Mtakatifu Kipriano, Metropolita wa Kyiv na Moscow na wa Urusi yote, alikuwa Mbulgaria kwa kuzaliwa, wa mji wa Tarnovo, na akaundwa katika mapokeo ya wanaotafuta ukimya wa moyo, akijitaabisha kama mtawa katika Mlima Mtakatifu wa Athos kabla ya kutumwa kaskazini na Patriaki wa Konstantinopoli. Aliwekwa wakfu kuwa metropolita katika wakati wa mafarakano na machafuko.", "patron": "Maombezi yake huombwa kwa ajili ya watafsiri; watunga nyimbo takatifu."},

"Repose of Saint Cyril, Equal of the Apostles and Teacher of the Slavs":
{"type": "Sawa na Mitume · karne ya 9", "life": "Siku hii Kanisa linaishika kulala kwa Mtakatifu Kirilo, Sawa na Mitume na Mwalimu wa Waslavoni, aliyekufa Roma tarehe kumi na nne ya Februari mwaka wa 869; sikukuu yake ya pamoja na ndugu yake Methodio inaadhimishwa mwezi wa Mei, lakini siku hii ni yake mwenyewe.", "patron": "Maombezi yake huombwa kwa ajili ya watafsiri; walimu."},

"Repose of Saint Herman, Archbishop of Kazan":
{"type": "Askofu Mkuu · karne ya 16", "life": "Siku hii Kanisa linakumbuka kulala kwa Mtakatifu Germano, Askofu Mkuu wa Kazan. Akizaliwa akiitwa Gregorio, wa jamaa ya kitukufu ya kina Polev huko Starytsa, alinyolewa katika monasteri ya Volokolamsk ya Mtakatifu Yosefu, ambako elimu na kujinyima viliunganishwa, na akawa arkimandriti wa monasteri ya Kulala katika Starytsa nchi yake.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; kuangazwa kwa Kazan."},

"Repose of Saint Innocent, Metropolitan of Moscow, Enlightener of the Aleuts, Apostle to the Americas":
{"type": "Metropolita, Sawa na Mitume · karne ya 19", "life": "Mtakatifu Inokentio, Metropolita wa Moscow na Mwangazaji wa Amerika ya Kaskazini, alizaliwa akiitwa Ivani Popov mwaka wa 1797 katika kijiji cha Anga katika nchi ya Irkutsk ya Siberia, mwana maskini wa kasisi aliyelichukua jina la ukoo Veniaminov seminarini; na mwaka wa 1824, kasisi kijana aliyeoa mwenye vipaji ambavyo vingelipamba mji mkuu wowote, alijitolea kwa kazi ambayo hakuna aliyeitaka, visiwa vya Waaleuti kwenye ukingo wa dunia, na akasafiri baharini pamoja na jamaa yake hadi Unalaska.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; watafsiri."},

"Repose of Saint Innocent, first Bishop of Irkutsk":
{"type": "Askofu · karne ya 18", "life": "Siku hii Kanisa linamkumbuka Mtakatifu Inokentio, Askofu wa kwanza wa Irkutsk, mwangazaji wa Siberia ya mashariki. Akizaliwa karibu mwaka wa 1680 katika jamaa tukufu ya kina Kulchitsky ya nchi za Chernigov, Yohane alisomeshwa katika Akademia ya Kyiv, akapokea unyoaji wa kitawa kwa jina Inokentio, na akafundisha katika shule za Moscow na Petersburg.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; walimu."},

"Repose of Saint Jacob Netsvetov, Enlightener of the Peoples of Alaska":
{"type": "Kasisi · karne ya 19", "life": "Mtakatifu Yakobo Netsvetov, Mwangazaji wa watu wa Alaska, alizaliwa mwaka wa 1802 katika Kisiwa cha Atka katika visiwa vya Waaleuti, mwana wa baba Mrusi kutoka Tobolsk na mama Mwaleuti, na hivyo aliunganishwa kwa damu na watu wale wale ambao angewatumikia. Akiwa amesomeshwa na baada ya muda akapewa daraja la ukasisi, alirudi Atka.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; watafsiri."},

"Repose of Saint John Chrysostom, Archbishop of Constantinople":
{"type": "Askofu Mkuu · karne ya 5", "life": "Mtakatifu Yohane Krisostom, aitwaye Mwenye Kinywa cha Dhahabu kwa ufasaha wake usio na mshindani na anayeheshimiwa kama mmoja wa Maaskofu Watatu Watakatifu, alizaliwa Antiokia karibu mwaka wa 347 na akalelewa katika uchaji na mama yake mjane Anthusa. Akifunzwa usemi chini ya Libanio maarufu, aliiacha kazi tukufu ya kidunia, akabatizwa na Mtakatifu Meletio, na akajitoa kwa maisha ya kujinyima katika mapango karibu na Antiokia, hata afya yake ilipomwishia na akarudi mjini, ambako alipewa daraja la ushemasi na kisha la ukasisi.", "patron": "Maombezi yake huombwa kwa ajili ya wahubiri; wanenaji."},

"Repose of Saint Jonah, Archbishop of Novgorod":
{"type": "Askofu Mkuu · karne ya 15", "life": "Mtakatifu Yona, Askofu Mkuu wa Novgorod, alikuwa duniani Yohane, aliyeachwa yatima utotoni na akalelewa na mjane mcha Mungu huko Novgorod; na mara moja, mvulana alipokuwa amesimama kati ya wenzake, mbarikiwa Mikaeli wa Klops, mpumbavu kwa ajili ya Kristo, alipita, na akiinama kwa mtoto akasema, Yohane, jifunze kitabu chako kwa bidii, kwa maana utakuwa askofu mkuu wa Novgorod Kuu.", "patron": "Maombezi yake huombwa kwa ajili ya mayatima; wakuu wa Kanisa."},

"Repose of Saint Nikolai of Zhicha":
{"type": "Askofu, Mkiri · karne ya 20", "life": "Mtakatifu Nikolai wa Zhicha, Krisostom mpya wa Kanisa la Serbia, alizaliwa akiitwa Nikola Velimirovich mwaka wa 1880 katika kijiji cha Lelich, mkubwa wa watoto wengi wa wakulima wacha Mungu, na akapanda kwa akili aliyopewa na Mungu tu kupitia shule za Serbia na vyuo vikuu vya Ulaya, akipata shahada za udaktari huko magharibi huku akibaki kabisa mtoto wa kijiji cha Kiserbia na imani yake.", "patron": "Maombezi yake huombwa kwa ajili ya wahubiri; waandishi."},

"Repose of Saint Peter, Metropolitan of Moscow, Wonderworker of All Russia":
{"type": "Metropolita · karne ya 14", "life": "Mtakatifu Petro, Metropolita wa Kyiv na Rus yote, mtenda-miujiza wa Moscow, alizaliwa katika Volinia na akatolewa kwa monasteri akiwa na miaka kumi na miwili, ambako kando ya utii na sala aliufahamu ufundi wa ikoni, akichora ikoni za Mwokozi na za Mzazi-Mungu, mojawapo yake, ile ya Petrovskaya, ikiheshimiwa hadi leo.", "patron": "Maombezi yake huombwa kwa ajili ya wakuu wa Kanisa; wachora ikoni."},

"Repose of Saint Raphael, Bishop of Brooklyn":
{"type": "Askofu · karne ya 20", "life": "Mtakatifu Rafaeli, Askofu wa Brooklyn, ambaye siku hii inakumbuka kulala kwake, alikuwa mchungaji mwema wa kondoo waliopotea wa Amerika, na askofu wa kwanza wa Kiorthodoksi kuwekwa wakfu katika Dunia Mpya. Akizaliwa Beiruti mwaka wa 1860 katika jamaa maskini ya Kidameski iliyokimbia mauaji ya mwaka ule, alisomeshwa na Kanisa lililomtambua, katika shule ya kipatriaki, huko Halki, na katika Akademia ya Theolojia ya Kyiv, akiimudu Kiarabu, Kigiriki, Kituruki, Kirusi na baada ya muda Kiingereza, sinodi ya lugha katika mtu mmoja.", "patron": "Maombezi yake huombwa kwa ajili ya wahamiaji; maaskofu wamisionari."},

"Repose of Saint Theodore Yaroslavich, older brother of Saint Alexander Nevsky":
{"type": "Mkuu · karne ya 13", "life": "Mtakatifu Theodoro Yaroslavich alikuwa ndugu mkubwa wa Mtakatifu Aleksanda Nevsky mkuu.", "patron": "Vijana wanaokufa katika usafi; wakuu waliokatiliwa mbali kabla ya wakati wao."},

"Repose of Saint Theoktistos, Archbishop of Novgorod":
{"type": "Askofu Mkuu · karne ya 14", "life": "Mtakatifu Theoktisto, Askofu Mkuu wa Novgorod, alikuwa abate wa monasteri ya Bishara karibu na mji ule wakati, Askofu Mkuu Klementi alipolala mwaka wa 1300, watu wa Novgorod walipomchagua kuwa mchungaji wao kwa desturi ya kale ya jamhuri yao; naye aliwekwa wakfu tarehe ishirini na tisa ya Juni mwaka wa 1300 na Metropolita Maksimo wa Kyiv na Rus yote pamoja na maaskofu wa Rostov na Tver.", "patron": "Maombezi yake huombwa kwa ajili ya wakuu wa Kanisa wanaostaafu kwa unyenyekevu; wajenzi wa makanisa."},

"Repose of Saint Tikhon, Patriarch of Moscow, Enlightener of North America":
{"type": "Patriaki, Mkiri · karne ya 20", "life": "Mtakatifu Tikhoni, Patriaki wa Moscow na Mwangazaji wa Amerika ya Kaskazini, alizaliwa akiitwa Vasily Bellavin mwaka wa 1865, mwana wa kasisi wa kijijini kutoka Toropets, na akapanda kupitia seminari na unyoaji wa kitawa kwa upole uliodhihirika kiasi kwamba wanafunzi wenzake, nusu kwa mzaha na kwa unabii kamili, walimwita kijana yule Patriaki.", "patron": "Maombezi yake huombwa kwa ajili ya mapatriaki utumwani; Kanisa wakati wa mateso."},

"Repose of Venerable Abramius of Galich or Chukhloma Lake, disciple of Venerable Sergius of Radonezh":
{"type": "Mtawa · karne ya 14", "life": "Mheshimiwa Abramio wa Galich alikuwa mwanafunzi wa Mheshimiwa Sergio wa Radonezh aliyejitaabisha katika monasteri ya Utatu Mtakatifu katika karne ya kumi na nne, akitumika miaka mingi kama novisi kabla ya kupewa daraja la ukasisi. Akitamani ukimya wa ndani zaidi, alipokea baraka ya mzee wake na mwaka wa 1350 akajitenga katika jangwa la nchi ya Galich kaskazini mwa Urusi, ambayo wakati ule bado ilikaliwa na makabila yasiyobatizwa.", "patron": "Anakumbukwa katika kalenda takatifu ya Kanisa."},

"Repose of Venerable Cornelius of Pereyaslavl":
{"type": "Mtawa · karne ya 17", "life": "Mheshimiwa Kornelio wa Pereyaslavl, aliyeitwa Konon duniani, alikuwa mwana wa mfanyabiashara wa Ryazan. Katika ujana wake aliiacha nyumba ya wazazi wake na akatumika miaka mitano kama novisi chini ya mzee Paulo katika jangwa la Lukianov, kisha akahamia monasteri ya Pereyaslavl ya Watakatifu Boris na Gleb ya Mchangani.", "patron": "Maombezi yake huombwa kwa ajili ya watawa; ukimya."},

"Repose of Venerable Herman of Alaska, Wonderworker of All America":
{"type": "Mtawa · karne ya 19", "life": "Mheshimiwa Herman wa Alaska, Mtenda-Miujiza wa Amerika Yote, alizaliwa karibu mwaka wa 1756 huko Serpukhov karibu na Moscow, na akaundwa kama mtawa katika monasteri ya Valaam chini ya mzee Nazario; na mwaka wa 1794, akiwa mmoja wa wamisionari kumi waliotumwa kuvuka maili elfu saba za milki na bahari, alifika Kisiwa cha Kodiak katika Amerika ya Kirusi baada ya safari ya karibu mwaka mzima, ili kuwapelekea Injili watu wa Alutiiq.", "patron": "Maombezi yake huombwa kwa ajili ya wamisionari; mayatima."},

"Repose of Venerable Job the Wonderworker, Abbot of Pochaiv":
{"type": "Abate · karne ya 17", "life": "Mheshimiwa Ayubu wa Pochaev, aliyeitwa duniani Ivani Zhelezo, alizaliwa karibu mwaka wa 1551 katika Pokutia katika Galisia, na akaja akiwa na miaka kumi katika monasteri ya Kugeuka Sura huko Ugornitsi, akipokea unyoaji akiwa na miaka kumi na miwili kwa jina Ayubu. Utakatifu wake ulikomaa mapema kiasi kwamba alipewa daraja la ukasisi angali kijana na akawa mashuhuri katika nchi zote za magharibi.", "patron": "Maombezi yake huombwa kwa ajili ya wachapishaji; watetezi wa imani."},

"Repose of Venerable Nilus, Abbot of Sora":
{"type": "Mtawa · karne ya 16", "life": "Mheshimiwa Nilo wa Sora, mwalimu mkuu wa maisha ya skete na wa sala ya moyo katika Urusi, alizaliwa akiitwa Nikolao Maikov karibu mwaka wa 1433, wa Moscow, na akanyolewa katika monasteri ya Kirillo-Belozersk, shule kali kuliko zote za kaskazini; na malezi yake yalikamilishwa ng'ambo.", "patron": "Njia ya skete iliyopandwa katika Urusi."},

"Repose of Venerable Sergius the Wonderworker, Abbot of Radonezh":
{"type": "Mheshimiwa · karne ya 14", "life": "Mheshimiwa Sergio wa Radonezh alizaliwa akiitwa Bartholomeo na akawa mtawa katika misitu ya kaskazini mwa Moscow. Alianzisha monasteri ya Utatu Mtakatifu, akafundisha unyenyekevu, sala na upendo wa kindugu, na akawaongoza watawa na wakuu. Akijulikana kama mtenda-miujiza na mfanyaji upya wa maisha ya utawa ya Urusi, alilala mwaka wa 1392."},

"Repose of Venerable Shio the Anchorite of Georgia":
{"type": "Mtawa · karne ya 6", "life": "Mheshimiwa Shio wa Mgvime, Mtawa wa Upweke, mmoja wa Mababa Kumi na Watatu wa Kisiria waliopanda utawa katika Georgia, alikuja kutoka Antiokia katika karne ya sita akiwa mwanafunzi wa Mtakatifu Yohane wa Zedazeni, katika kikundi ambacho Kanisa la Georgia linakiheshimu kama kundi la nyota lililolianzisha jangwa lake.", "patron": "Njiwa aliyemletea mkate wake."},

"Repose of the Blessed John of Ustiug the Fool-for-Christ":
{"type": "Mpumbavu kwa ajili ya Kristo · karne ya 15", "life": "Mbarikiwa Yohane wa Ustyug, mpumbavu kwa ajili ya Kristo, alikuwa mjinyimaji wa mji wa kaskazini wa Veliky Ustyug aliyeichukua njia ngumu na iliyofichwa kuliko zote za utakatifu, upumbavu kwa ajili ya Kristo, na akaifanya tangu utoto wake wenyewe.", "patron": "Upumbavu uliojifanya ili kuficha kufunga na makesha."},

"Repose of the Holy Apostle and Evangelist John the Theologian":
{"type": "Mtume · karne ya 2", "life": "Mtume Mtakatifu na Mwinjilisti Yohane Mwanateolojia, mwanafunzi mpendwa, alikuwa mwana wa Zebedayo na Salome na ndugu wa Yakobo, aliyeitwa kutoka nyavu zake kwenye bahari ya Galilaya amfuate Kristo, na kati ya wanafunzi wote yeye ndiye aliyelala karibu zaidi na kifua cha Bwana.", "patron": "Maombezi yake huombwa kwa ajili ya wanateolojia; waandishi."},

"Repose of the Holy Right-believing Princess Anna of Kashin":
{"type": "Mtawa wa kike · karne ya 14", "life": "Mheshimiwa Ana wa Kashin, Mkuu wa Kike Mwenye Imani Sahihi, alikuwa binti wa Mkuu Dimitri wa Rostov, na mwaka wa 1294 akawa mke wa Mkuu Mkubwa mtakatifu Mikaeli wa Tver. Mungu akamwekea maisha ya huzuni isiyokatika: alimzika binti yake mchanga na baba yake, akaona Tver ikiungua na tauni ikiifagia nchi, na mwaka wa 1318 mume wake aliteswa na kuuawa katika Horde kwa kukataa kujiokoa kwa gharama ya watu wake.", "patron": "Maombezi yake huombwa kwa ajili ya wajane; waliofiwa kwa jeuri."},

"Return of the Relics of the Apostle Bartholomew from Anastasiopolis to Lipari":
{"type": "Mtume · karne ya 1", "life": "Mtume Mtakatifu Bartholomeo, mmoja wa wale Kumi na Wawili, aliteseka kwa ajili ya Kristo katika Armenia, ambako alichunwa ngozi na akakatwa kichwa karibu mwaka wa 71, na masalia yake yakabaki katika nchi ile yakitenda miujiza mingi. Katika utawala wa mfalme Anastasio yalichukuliwa hadi mji mpya wa Anastasiopoli, lakini mikono ya adui ilipoyatishia baadaye, waamini waliyaweka masalia katika sanduku la risasi na wakayatoa baharini, wakimkabidhi mtume kwa maongozi ya Mungu.", "patron": "Maombezi yake huombwa kwa ajili ya uponyaji."},

"Right-Believing Prince Roman of Uglich":
{"type": "Mkuu · karne ya 13", "life": "Mkuu Roman wa Uglich Mwenye Imani Sahihi aliitawala nchi yake ya Volga katika karne ya kumi na tatu, katika vizazi vya kwanza vichungu vya nira ya Wamongolia, na akaacha nyuma yake sifa adimu kuliko zote za zama za kati, utawala unaokumbukwa kwa wema tu. Mwana wa mkuu mcha Mungu Vladimiri wa Uglich, Roman alilelewa katika kumcha Mungu, na akapokea ukuu wake.", "patron": "Maombezi yake huombwa kwa ajili ya watawala; wajenzi wa makanisa na hospitali."},

"Right-believing George the Great Prince of Vladimir":
{"type": "Mkuu Mkubwa, Shahidi · karne ya 13", "life": "Georgi Mwenye Imani Sahihi, Mkuu Mkubwa wa Vladimir, alizaliwa mwaka wa 1189, mwana wa Mkuu Mkubwa Vsevolod aitwaye Kiota Kikubwa, na akapokea kiti cha enzi cha Vladimir mwaka wa 1212; akiwa mashuhuri tangu ujana kwa ushujaa wa kivita na kwa uchaji, aliitawala nchi yenye nguvu kuliko zote za kaskazini ya Urusi kwa robo karne ya ujenzi, akianzisha mwaka wa 1221, kwenye makutano ya Volga na Oka, mji ngome wa Nizhny Novgorod, ambao kuta zake zinailinda kumbukumbu yake hadi leo.", "patron": "Maombezi yake huombwa kwa ajili ya watawala wakati wa maafa; watetezi wa nchi."},

"Right-believing Great Prince Rostislav-Michael, Prince of Kyiv":
{"type": "Mkuu · karne ya 12", "life": "Mkuu Mkubwa Rostislav wa Kyiv Mwenye Imani Sahihi, aliyeitwa Mikaeli katika ubatizo mtakatifu, alikuwa mwana wa Mstislav Mkuu na mjukuu wa Vladimiri Monomakh, na akayabeba mema kuliko yote ya ukoo ule, uchaji wake na upatanishi wake, katika kimoja cha vizazi vyenye ugomvi kuliko vyote vya Rus. Kwa zaidi ya miaka thelathini alikuwa mkuu wa Smolensk.", "patron": "Maombezi yake huombwa kwa ajili ya watawala; wapatanishi."},

"Right-believing John, Prince of Uglich, tonsured as Ignatius":
{"type": "Mwenye imani sahihi · karne ya 16", "life": "Mheshimiwa Yohane, Mkuu wa Uglich Mwenye Imani Sahihi, aliyenyolewa kabla ya kifo chake kwa jina la Ignatio, alikuwa Mkristo mcha Mungu tangu ujana wake aliyepewa na dunia fungu la dhuluma tupu na akaligeuza, kwa neema, kuwa utakatifu uliofichwa.", "patron": "Miaka thelathini na miwili ya gereza iliyobebwa bila uchungu."},

"Right-believing Prince Basil (Vasilko) of Rostov":
{"type": "Mkuu, Mbeba-Mateso · karne ya 13", "life": "Mkuu Basili Mwenye Imani Sahihi, aitwaye Vasilko, wa Rostov alikuwa wa ukoo wa Suzdal wa kina Monomashichi, mjukuu wa Vsevolod aitwaye Kiota Kikubwa na mwana wa mkuu mcha Mungu Konstantino wa Rostov; na kumbukumbu za kaskazini zinamkumbuka kama ua la kizazi chake, mzuri, shujaa, mkarimu na mcha Mungu, mpendwa na watu wake na wakleri ambao ushauri wao aliushika.", "patron": "Maombezi yake huombwa kwa ajili ya watawala chini ya ushindi wa adui; vijana."},

"Right-believing Prince Roman of Ryazan":
{"type": "Mkuu · karne ya 13", "life": "Mkuu Roman Olegovich wa Ryazan aliitawala nchi yake katika miaka michungu ya nira ya Watatari, wakati nchi za Urusi zililala chini ya utawala wa Horde ya Dhahabu. Akiwa mtawala mcha Mungu na wa haki aliyewatetea watu wake na imani yake, alisingiziwa mbele ya Khani na watu wenye wivu waliomshtaki kwa kuitukana dini ya Watatari.", "patron": "Maombezi yake huombwa kwa ajili ya ukiri wa imani wakati wa mateso."},

"Right-believing Prince Vladimir Yaroslavich of Novgorod":
{"type": "Mkuu · karne ya 11", "life": "Mkuu Vladimiri Yaroslavich wa Novgorod, mtenda-miujiza, alikuwa mwana mkubwa wa Mkuu Mkubwa Yaroslav Mwenye Hekima na wa Mkuu wa Kike mcha Mungu Irene, aliyemaliza siku zake kama mtawa Ana na anayeheshimiwa pamoja na mwanawe. Akiwekwa juu ya Novgorod na baba yake akiwa na miaka kumi na minne, aliongozwa na washauri wenye hekima na askofu mtakatifu wa mji, na akakua kuwa mtetezi shujaa wa nchi na Mkristo mcha Mungu, akiwainulia watu wake ngome ya mawe na akijifundisha kwa bidii katika sheria ya Bwana.", "patron": "Maombezi yake huombwa kwa ajili ya wajenzi wa makanisa; ujenzi wa makanisa."},

"Right-believing Princess Juliana of Vyazma":
{"type": "Mkuu wa kike · karne ya 15", "life": "Mkuu wa Kike Yuliana wa Vyazma Mwenye Imani Sahihi, mbeba-mateso msafi, alikuwa mke wa Mkuu Simeoni Mstislavich wa Vyazma, na akashiriki uhamisho wake Smolensk na Vyazma vilipoangukia Lithuania na wakuu waliopokonywa nchi zao wakakimbilia Torzhok katika utumishi wa Mkuu Yuri wa Smolensk. Huko uzuri wake ukawa msalaba wake: Yuri, akiwaka tamaa kwa mke wa mwenzake mwaminifu mwenyewe, na akiiona fadhila yake haiwezi kutikiswa, aliamua kutumia nguvu, na katika karamu wakati wa baridi wa mwaka wa 1406 alimuua Mkuu Simeoni mezani, akidhani kumtwaa mjane pamoja na mume.", "patron": "Maombezi yake huombwa kwa ajili ya wake; wanawake walio hatarini."},

"Righteous Abel the Shepherd":
{"type": "Mwenye haki · Agano la Kale", "life": "Abeli alikuwa mwana wa pili wa Adamu na Hawa na alichunga kondoo, huku ndugu yake Kaini akiilima ardhi. Wote wawili walimletea Mungu sadaka, na Mungu akaitazama sadaka ya Abeli na dhabihu yake ya wazaliwa wa kwanza wa kundi lake, lakini hakuitazama sadaka ya Kaini. Kaini akakasirika, na akimwinukia ndugu yake shambani akamuua, na sauti ya damu yake ikalia kutoka ardhini.", "patron": "Maombezi yake huombwa kwa ajili ya wasio na hatia waliouawa; wachungaji."},

"Righteous Anna the Prophetess and Daughter of Phanuel, who met the Lord at the Temple in Jerusalem":
{"type": "Nabii wa kike · karne ya 1", "life": "Ana Nabii wa Kike Mwenye Haki alikuwa wa kabila la Asheri na binti wa Fanueli, na akiisha kuishi na mume wake miaka saba tu kabla ya kifo chake, aliyatoa maisha yake yote yaliyobaki kwa Mungu. Kama Injili ya Luka isimuliavyo, hakuondoka hekaluni, bali alimtumikia Mungu humo usiku na mchana kwa kufunga na kusali, na alikuwa amefikia umri mkubwa wa miaka themanini na minne.", "patron": "Maombezi yake huombwa kwa ajili ya wajane."},

"Righteous Artemius of Verkola":
{"type": "Mwenye haki · karne ya 16", "life": "Artemio Mwenye Haki wa Verkola alikuwa mvulana mkulima wa Kaskazini ya Urusi, mtoto wa ucha Mungu wa ajabu, ambaye Mungu alimtukuza baada ya kifo cha ghafla na kutelekezwa kwa muda mrefu kwa mwili wake.", "patron": "Watoto wachaji Mungu; wagonjwa na wenye homa."},

"Righteous Benjamin":
{"type": "Babu Mwenye Haki · karne ya 17 KK", "life": "Benyamini Mwenye Haki, mdogo kuliko wote wa wana kumi na wawili wa Babu Yakobo, alikuwa mtoto wa pili wa Raheli mpendwa, aliyekufa akimzaa njiani kwenda Efrathi na akamwita kwa pumzi yake ya mwisho Ben-oni, mwana wa huzuni yangu; lakini baba yake alimwita Benyamini, mwana wa mkono wa kuume, na mtoto wa huzuni akawa kipenzi cha uzee wa babu.", "patron": "Maombezi yake huombwa kwa ajili ya mdogo kuliko wote na mpendwa zaidi; huzuni iliyogeuzwa kuwa nguvu."},

"Righteous Child Artemius of Verkola":
{"type": "Mtoto mwenye haki · karne ya 16", "life": "Mtoto Mwenye Haki Artemio wa Verkola alizaliwa karibu mwaka wa 1532 katika kijiji kwenye mto Pinega katika kaskazini ya mbali, mwana wa wakulima wacha Mungu, na tangu miaka yake ya mwanzo alikuwa mpole, mtii, mwenye kusali na mwenye bidii katika kila kazi njema, mtoto asiyefanana na watoto wengine.", "patron": "Maombezi yake huombwa kwa ajili ya watoto."},

"Righteous Deborah":
{"type": "Nabii wa kike · karne ya 12 KK", "life": "Debora Mwenye Haki, nabii wa kike na mwamuzi wa Israeli, aliketi chini ya mtende wake kati ya Rama na Betheli katika nchi ya vilima ya Efraimu, na wana wa Israeli walimpandia kwa hukumu, katika kizazi cha giza wakati Yabini wa Kanaani na Sisera jemadari wake, wakiwa na magari ya vita mia tisa ya chuma, waliyaponda makabila kwa miaka ishirini.", "patron": "Maombezi yake huombwa kwa ajili ya waamuzi; wanawake wanaoongoza."},

"Righteous Eudocimus of Cappadocia":
{"type": "Jemadari · karne ya 9", "life": "Mtakatifu Eudokimo, mzaliwa wa Kapadokia, aliishi katika karne ya tisa katika utawala wa mfalme Theofilo, na alikuwa mwana wa wazazi wacha Mungu na mashuhuri, Basili na Eudokia, waliomlea katika nidhamu na maonyo ya Bwana. Kwa kufuata jina lake, lenye maana ya mwenye sifa njema, alifanikiwa katika kila fadhila, akiyatoa maisha yake kumpendeza Mungu na kumtumikia jirani yake.", "patron": "Maombezi yake huombwa kwa ajili ya makao ya familia; mayatima na wajane."},

"Righteous Forefather Abraham":
{"type": "Babu Mwenye Haki · karne ya 20 KK", "life": "Babu Mwenye Haki Abrahamu, baba wa wote waaminio, aliitwa na Mungu kutoka Uru wa Wakaldayo, akiiacha nchi yake na jamaa yake kwa neno la Bwana, aliyeahidi kwamba katika mbegu yake jamaa zote za dunia zingebarikiwa.", "patron": "Maombezi yake huombwa kwa ajili ya imani; ukarimu kwa wageni."},

"Righteous Forefather Adam":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Adamu alikuwa mtu wa kwanza, aliyeumbwa na Mungu kutoka mavumbi ya ardhi na akapewa pumzi ya uzima, na akawekwa Paradiso ailime na kuitunza. Aliumbwa katika sura ya Mungu na akapewa utawala juu ya kila kilicho hai, naye akawapa majina wanyama wa kondeni na ndege wa angani.", "patron": "Maombezi yake huombwa kwa ajili ya toba; kuomboleza dhambi."},

"Righteous Forefather Arphaxad":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Arfaksadi alikuwa mwana wa Shemu, aliyezaliwa miaka miwili baada ya gharika, naye anasimama mbele ya ukoo unaokwenda kutoka Noa hadi Abrahamu. Maandiko yanaandika nafasi yake katika orodha ya vizazi na kwamba aliishi miaka mia nne na thelathini na minane."},

"Righteous Forefather Cainan":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Kenani alikuwa mwana wa Enoshi na kizazi cha nne kutoka Adamu. Maandiko yanaandika juu yake nafasi yake katika orodha ya vizazi tu na kwamba aliishi miaka mia tisa na kumi."},

"Righteous Forefather Eber":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Eberi alikuwa mwana wa Sala na baba wa Pelegi, na kutoka jina lake watu Waebrania kwa mapokeo wanasemekana kuitwa. Maandiko yanaandika kwamba aliishi miaka mia nne na sitini na minne."},

"Righteous Forefather Enoch":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Henoko alikuwa mwana wa Yaredi na kizazi cha saba kutoka Adamu. Maandiko yanasema juu yake kile ambacho hayasemi juu ya mtu mwingine yeyote wa zama ile, kwamba Henoko alikwenda pamoja na Mungu, naye hakuonekana tena, kwa maana Mungu alimtwaa.", "patron": "Maombezi yake huombwa kwa ajili ya maisha yasiyo na lawama; tumaini la ufufuo."},

"Righteous Forefather Enos":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Enoshi alikuwa mwana wa Sethi na mjukuu wa Adamu. Juu ya kizazi chake Maandiko yanaandika kwamba watu walianza kuliitia jina la Bwana, na Mababa wanaelewa hili kama mwanzo wa ibada ya hadhara inayotolewa kwa Mungu waziwazi."},

"Righteous Forefather Isaac":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Isaka alikuwa mwana wa Abrahamu na Sara, aliyezaliwa kwao katika uzee wao kwa mujibu wa ahadi, na jina lake lina maana ya kicheko, kwa maana Sara alicheka aliposikia kwamba angezaa mwana.", "patron": "Maombezi yake huombwa kwa ajili ya utii; watoto waliosubiriwa kwa muda mrefu."},

"Righteous Forefather Jacob":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Yakobo alikuwa mwana mdogo wa Isaka na Rebeka na akapokea baraka ya mzaliwa wa kwanza. Akikimbia hasira ya ndugu yake Esau alilala mahali fulani na akaota ngazi iliyosimamishwa juu ya ardhi ambayo kilele chake kilifika mbinguni, na malaika wa Mungu wakipanda na kushuka juu yake, na Bwana amesimama juu yake akimfanyia upya ahadi aliyompa Abrahamu.", "patron": "Maombezi yake huombwa kwa ajili ya jitihada katika sala; waliohamishwa."},

"Righteous Forefather Jared":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Yaredi alikuwa mwana wa Mahalaleli na baba wa Henoko, kizazi cha sita kutoka Adamu. Maandiko yanaandika kwamba aliishi miaka mia tisa na sitini na miwili, wala hayatoi habari nyingine juu yake."},

"Righteous Forefather Lamech":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Lameki alikuwa mwana wa Methusela na baba wa Noa. Katika kuzaliwa kwa mwanawe alisema kwamba huyu atawafariji juu ya kazi yao na taabu ya mikono yao, kwa sababu ya ardhi ambayo Bwana aliilaani, na Mababa wanaona katika maneno haya unabii wa raha ambayo ingekuja kwa njia ya safina na baadaye kwa njia ya Kristo."},

"Righteous Forefather Mahalalel":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Mahalaleli alikuwa mwana wa Kenani na kizazi cha tano kutoka Adamu. Jina lake linaeleweka kuwa na maana ya sifa ya Mungu. Maandiko yanaandika kwamba aliishi miaka mia nane na tisini na mitano."},

"Righteous Forefather Methuselah":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Methusela alikuwa mwana wa Henoko na babu wa Noa. Aliishi miaka mia tisa na sitini na tisa, mingi kuliko ya mtu mwingine yeyote aliyeandikwa katika Maandiko, naye akafa katika mwaka wa gharika."},

"Righteous Forefather Nahor":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Nahori alikuwa mwana wa Serugi na baba wa Tera, na hivyo babu wa Abrahamu. Maandiko yanaandika kwamba aliishi miaka mia moja na arobaini na minane, maisha ya mababu yakizidi kuwa mafupi kadiri vizazi vilivyomkaribia Abrahamu."},

"Righteous Forefather Noah":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Babu Mwenye Haki Noa, wa kumi kutoka Adamu, alipata neema machoni pa Bwana wakati uovu wa wanadamu ulipokuwa umekua sana juu ya ardhi, na kwa amri ya Mungu akaijenga safina ambamo nyumba yake na kila kilicho hai vilihifadhiwa katika gharika; Mababa wanaona ndani yake mfano wa Kanisa.", "patron": "Maombezi yake huombwa kwa ajili ya kudumu katikati ya dhihaka; ukombozi kutoka gharika."},

"Righteous Forefather Peleg":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Pelegi alikuwa mwana wa Eberi. Maandiko yanasema kwamba katika siku zake ardhi iligawanywa, jambo linaloeleweka juu ya kutawanyika kwa mataifa baada ya mnara wa Babeli, na jina lake linaibeba maana ile. Aliishi miaka mia mbili na thelathini na tisa."},

"Righteous Forefather Reu":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Reu alikuwa mwana wa Pelegi na baba wa Serugi, aliyezaliwa katika vizazi baada ya kutawanyika kwa mataifa. Maandiko yanaandika nafasi yake katika orodha ya vizazi na kwamba aliishi miaka mia mbili na thelathini na tisa, wala hayatoi habari nyingine juu yake."},

"Righteous Forefather Salah":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Sala alikuwa mwana wa Arfaksadi na baba wa Eberi. Maandiko yanaandika juu yake nafasi yake tu katika ukoo unaokwenda kutoka Noa hadi Abrahamu na kwamba aliishi miaka mia nne na thelathini na mitatu."},

"Righteous Forefather Serug":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Serugi alikuwa mwana wa Reu, baba wa Nahori, na babu mkubwa wa Abrahamu. Maandiko yanaandika nafasi yake katika ukoo unaokwenda kutoka Noa hadi Abrahamu na kwamba aliishi miaka mia mbili na thelathini."},

"Righteous Forefather Seth":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Sethi alikuwa mwana wa tatu wa Adamu na Hawa, aliyepewa kwao baada ya kuuawa kwa Abeli, na Hawa akasema katika kuzaliwa kwake kwamba Mungu amemwekea mbegu nyingine mahali pa mwana ambaye Kaini alimwua. Kwa njia yake ukoo wa wenye haki uliendelezwa hadi Noa na hivyo hadi Kristo.", "patron": "Maombezi yake huombwa kwa ajili ya mwanzo wa ibada ya kweli."},

"Righteous Forefather Terah":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Tera alikuwa baba wa Abrahamu, Nahori na Harani, na babu wa Lutu. Aliitoa nyumba yake kutoka Uru wa Wakaldayo waende nchi ya Kanaani, lakini akafika Harani na akakaa huko, naye akafa Harani akiwa na miaka mia mbili na mitano."},

"Righteous Foremother Bathsheba":
{"type": "Mwenye haki · Agano la Kale", "life": "Bathsheba alikuwa mke wa Uria Mhiti na baadaye wa Mfalme Daudi, aliyemtwaa katika dhambi kubwa ambayo kwa ajili yake Nabii Nathani alimkemea na kwa ajili yake Daudi alitunga Zaburi ya Hamsini. Mtoto wa muungano ule alikufa, na Kanisa linaisoma habari yote kama mfano mkuu wa kimaandiko wa toba katika mtu mwenye haki.", "patron": "Maombezi yake huombwa kwa ajili ya toba."},

"Righteous Foremother Esther":
{"type": "Mwenye haki · Agano la Kale", "life": "Esta alikuwa msichana Myahudi wa kabila la Benyamini, aliyelelewa na jamaa yake Mordekai, aliyechaguliwa kuwa malkia na mfalme wa Uajemi. Hamani alipopata amri ya kuwaangamiza Wayahudi wote katika milki, Mordekai alimpelekea habari kwamba awaombee watu wake, akisema kwamba labda alikuwa amefika ufalmeni kwa wakati kama huu.", "patron": "Maombezi yake huombwa kwa ajili ya kuwaombea wengine; ujasiri mbele ya watawala."},

"Righteous Foremother Eve":
{"type": "Mwenye haki · Agano la Kale", "life": "Hawa alikuwa mwanamke wa kwanza, aliyeumbwa na Mungu kutoka ubavu wa Adamu alipokuwa amelala, na akapewa kwake kuwa msaidizi wa kumfaa. Adamu akamwita Hawa, yaani uzima, kwa sababu alikuwa mama wa walio hai wote.", "patron": "Maombezi yake huombwa kwa ajili ya mama; toba."},

"Righteous Foremother Huldah the Prophetess":
{"type": "Mwenye haki · Agano la Kale", "life": "Hulda alikuwa nabii wa kike katika Yerusalemu katika siku za Mfalme Yosia. Kitabu cha sheria kilipopatikana hekaluni wakati wa ukarabati wake na kikasomwa mbele ya mfalme, alirarua mavazi yake na akamtuma kuhani mkuu na watumishi wake wakamwulize Bwana, nao wakaenda kwa Hulda.", "patron": "Maombezi yake huombwa kwa ajili ya toba; kusoma Maandiko."},

"Righteous Foremother Judith":
{"type": "Mwenye haki · Agano la Kale", "life": "Yudithi alikuwa mjane wa Bethulia aliyefunga na kusali katika chumba juu ya dari yake. Mji ulipozingirwa na jeshi la Holoferne na wazee walipokuwa wameamua kujisalimisha kama msaada usingekuja ndani ya siku tano, aliwakemea kwa kumjaribu Mungu na akatoka pamoja na mjakazi wake kwenda kambini kwa adui.", "patron": "Maombezi yake huombwa kwa ajili ya ujasiri; wajane; ukombozi wa mji."},

"Righteous Foremother Leah":
{"type": "Mwenye haki · Agano la Kale", "life": "Lea alikuwa binti mkubwa wa Labani na mke wa kwanza wa Yakobo, aliyepewa kwake mahali pa Raheli ambaye alikuwa amemtumikia. Maandiko yanasema kwamba hakupendwa kama dada yake, na kwamba Bwana kwa hiyo akalifungua tumbo lake.", "patron": "Maombezi yake huombwa kwa ajili ya wasiopendwa; subira katika ndoa."},

"Righteous Foremother Rachel":
{"type": "Mwenye haki · Agano la Kale", "life": "Raheli alikuwa binti wa Labani na mke mpendwa wa Yakobo, aliyetumika miaka saba kwa ajili yake nayo ikamwonekana kama siku chache tu kwa sababu ya upendo aliokuwa nao kwake. Alikuwa tasa kwa muda mrefu huku dada yake Lea akizaa wana, na hatimaye akamzaa Yosefu na kisha Benyamini, naye akafa akimzaa njiani kwenda Bethlehemu.", "patron": "Maombezi yake huombwa kwa ajili ya ugumba; mama walio katika huzuni."},

"Righteous Foremother Rebecca":
{"type": "Mwenye haki · Agano la Kale", "life": "Rebeka alikuwa mke wa Isaka. Mtumishi wa Abrahamu alipokuja Mesopotamia akitafuta mke kwa mwana wa bwana wake, aliomba kwamba msichana ambaye angempa maji ya kunywa na kuwanywesha ngamia wake ndiye aliyewekwa, na Rebeka akatoka na mtungi wake na akafanya hivyo kabla hajamaliza kusema.", "patron": "Maombezi yake huombwa kwa ajili ya ukarimu kwa wageni; mwongozo katika ndoa."},

"Righteous Foremother Ruth":
{"type": "Mwenye haki · Agano la Kale", "life": "Ruthu alikuwa Mmoabi, mjane wa mwana wa Naomi. Naomi aliporudi Bethlehemu na kuwasihi wakwe zake warudi kwa watu wao wenyewe, Ruthu hakukubali kumwacha, akasema, Utakakoenda nami nitaenda, na wewe utakapoishi nitaishi; watu wako watakuwa watu wangu, na Mungu wako atakuwa Mungu wangu.", "patron": "Maombezi yake huombwa kwa ajili ya walioongoka; wajane; uaminifu."},

"Righteous Foremother Sarah":
{"type": "Mwenye haki · Agano la Kale", "life": "Sara alikuwa mke wa Abrahamu na akatoka pamoja naye kutoka Uru wa Wakaldayo. Alikuwa tasa hadi uzee, na malaika watatu walipokuja kwenye mwaloni wa Mamre na kusema kwamba angezaa mwana, alicheka moyoni mwake, kwa maana alikuwa na miaka tisini. Bwana akauliza kama kuna neno gumu lisilowezekana kwa Mungu, na kwa wakati wake akamzaa Isaka, ambaye jina lake lina maana ya kicheko.", "patron": "Maombezi yake huombwa kwa ajili ya ugumba; tumaini kinyume na matarajio."},

"Righteous Foremother Tamar":
{"type": "Mwenye haki · Agano la Kale", "life": "Tamari alikuwa mkwe wa Yuda, mjane mara mbili na aliyeachwa bila mtoto aliyestahili kupewa kwa desturi ya sheria. Yuda alipomzuilia mwanawe aliyebaki, alipata kwa hila kile kilichokuwa haki yake, na jambo lile lilipojulikana Yuda alikiri kwamba Tamari alikuwa mwenye haki kuliko yeye."},

"Righteous Hezron":
{"type": "Babu Mwenye Haki · karne ya 17 KK", "life": "Hesroni Mwenye Haki, mwana wa Peresi na mjukuu wa Babu Yuda, ni mmoja wa wachukuaji wa kimya wa ahadi, jina ambalo wasomaji wengi hulipita na mbingu haikulipita kamwe. Alikuwa miongoni mwa nafsi za nyumba ya Yakobo walioshuka Misri katika siku za Yosefu, akichukuliwa akiwa mtoto hadi nchi ambamo jamaa ya ahadi ingekua kuwa taifa.", "patron": "Maombezi yake huombwa kwa ajili ya viungo vilivyofichwa vya ahadi ya Mungu."},

"Righteous Jael":
{"type": "Mwenye haki · Agano la Kale", "life": "Yaeli alikuwa mke wa Heberi Mkeni. Sisera, jemadari wa jeshi lililokuwa limeidhulumu Israeli miaka ishirini, alipokimbia vitani na kufika hemani kwake, alimpokea na akampa maziwa anywe, na alipolala alimuua kwa kigingi cha hema na akaikomboa Israeli kutoka mkononi mwake.", "patron": "Maombezi yake huombwa kwa ajili ya ukombozi kutoka wadhalimu."},

"Righteous James the Brother of the Lord":
{"type": "Askofu · karne ya 1", "life": "Yakobo Mwenye Haki, Ndugu wa Bwana, anakumbukwa katika siku baada ya Kuzaliwa pamoja na Yosefu Mchumba baba yake na Daudi Mfalme, katika sinaksi ya jamaa za Bwana kwa jinsi ya mwili; ukumbusho wake kamili kama mtume, askofu wa kwanza wa Yerusalemu na shahidi Kanisa linaushika mwezi wa Oktoba, na hapa linamkumbuka hasa kama jamaa.", "patron": "Maombezi yake huombwa kwa ajili ya maaskofu; watunga ibada."},

"Righteous Japheth, son of Noah":
{"type": "Mwenye haki · Agano la Kale", "life": "Yafethi alikuwa mwana wa Noa na akapita katika gharika pamoja naye ndani ya safina. Pamoja na ndugu yake Shemu alimfunika baba yao bila kumtazama, na Noa akambariki akisema kwamba Mungu atamkuza Yafethi naye atakaa katika hema za Shemu."},

"Righteous Job the Long-Suffering":
{"type": "Mwenye haki · Agano la Kale", "life": "Ayubu Mwenye Haki na Mvumilivu, ambaye ukumbusho wake Kanisa linaushika siku hii, alikaa katika nchi ya Usi, ambayo mapokeo yanaiweka katika Haurani mashariki ya Yordani, na hesabu ya kale iliyohifadhiwa katika Maandiko ya Kigiriki inamhesabu kuwa wa ukoo wa Esau.", "patron": "Subira iliyohoji na bado ikabariki."},

"Righteous Joseph the All-Comely":
{"type": "Mwenye haki · Agano la Kale", "life": "Yosefu alikuwa mwana wa kumi na mmoja wa Yakobo na mzaliwa wa kwanza wa Raheli, na baba yake alimpenda kuliko watoto wake wote na akamfanyia joho la rangi nyingi. Ndugu zake walimchukia kwa sababu ya ndoto zake na wakamwuza kwa wafanyabiashara waliokuwa wakishuka Misri, na wakalichovya joho lake katika damu na wakalileta kwa baba yao.", "patron": "Maombezi yake huombwa kwa ajili ya usafi wa moyo; waliosingiziwa; wafungwa."},

"Righteous Joshua the Son of Nun":
{"type": "Mwenye haki · Agano la Kale", "life": "Yoshua alikuwa mwana wa Nuni na mtumishi na mrithi wa Musa. Alikuwa mmoja wa wale kumi na wawili waliotumwa kuipeleleza nchi, na pamoja na Kalebu peke yao walileta habari njema na wakawasihi watu wapande. Kwa ajili ya hili Bwana aliamuru kwamba yeye na Kalebu peke yao katika kizazi kile wangeingia nchini.", "patron": "Maombezi yake huombwa kwa ajili ya askari; kudumu."},

"Righteous Lot":
{"type": "Mwenye haki · Agano la Kale", "life": "Lutu alikuwa mpwa wa Abrahamu na akatoka pamoja naye kutoka Uru wa Wakaldayo. Wachungaji wao waliposhindana wakatengana, na Lutu akachagua tambarare ya Yordani yenye maji mengi na akakaa kuelekea Sodoma.", "patron": "Maombezi yake huombwa kwa ajili ya ukombozi kutoka mji uliohukumiwa."},

"Righteous Martha and Mary, the sisters of Lazarus":
{"type": "Wenye haki · karne ya 1", "life": "Martha na Maria Wenye Haki, dada za Lazaro, walikuwa miongoni mwa rafiki wa karibu zaidi wa Bwana hapa duniani, wa nyumba ile ya Bethania aliyoipenda na kuitembelea mara nyingi.", "patron": "Dada na wenyeji wa wageni; wanaohudumu na wanaoketi miguuni pa Bwana."},

"Righteous Melchizedek, King of Salem":
{"type": "Mwenye haki · Agano la Kale", "life": "Melkizedeki alikuwa mfalme wa Salemu na kuhani wa Mungu Aliye Juu. Abrahamu aliporudi kutoka kuwaua wafalme, Melkizedeki alitoka kumlaki na akaleta mkate na divai, na akambariki akisema, abarikiwe Abramu na Mungu Aliye Juu, mwenye mbingu na nchi. Abrahamu akampa fungu la kumi la nyara zote.", "patron": "Maombezi yake huombwa kwa ajili ya ukuhani."},

"Righteous Miriam, sister of Moses":
{"type": "Mwenye haki · Agano la Kale", "life": "Miriamu alikuwa dada wa Musa na Haruni. Akiwa mtoto aliliangalia kasha la manyasi kati ya matete ya mto na akasema na binti wa Farao, hata mama yake mwenyewe akaitwa amnyonyeshe mtoto.", "patron": "Maombezi yake huombwa kwa ajili ya ukombozi; shukrani baada ya ukombozi."},

"Righteous Mother Olga of Kwethluk, Tanqilria Arrsamquq, Wonderworker, Matushka of All Alaska":
{"type": "Mwenye haki · karne ya 20", "life": "Mama Olga Mwenye Haki wa Kwethluk, Tanqilria Arrsamquq, Matushka wa Alaska Yote, alizaliwa tarehe tatu ya Februari mwaka wa 1916 katika kijiji cha Kiyup'ik cha Kwethluk kwenye mto Kuskokwim, na jina lake la asili, Arrsamquq, lina maana ya mnyonge na aliyefichwa, unabii wa maisha yake yote.", "patron": "Maombezi yake huombwa kwa ajili ya wakunga; mama."},

"Righteous Patriarch Asher":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Asheri alikuwa mwana wa Yakobo kwa Zilpa. Baba yake alisema katika kumbariki kwamba mkate wake ungekuwa wa unono na kwamba angetoa vitoweo vya kifalme, na fungu la kabila lake lilikuwa kando ya pwani yenye rutuba kuelekea Tiro na Sidoni.", "patron": "Maombezi yake huombwa kwa ajili ya wingi; ukarimu kwa wageni."},

"Righteous Patriarch Dan":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Dani alikuwa mwana wa Yakobo kwa Bilha mjakazi wa Raheli. Jina lake lina maana ya hukumu, na baba yake alisema katika kumbariki kwamba Dani angewaamua watu wake kama mojawapo ya makabila ya Israeli.", "patron": "Maombezi yake huombwa kwa ajili ya waamuzi."},

"Righteous Patriarch Gad":
{"type": "Babu Mwenye Haki · Agano la Kale", "life": "Gadi alikuwa mwana wa Yakobo kwa Zilpa mjakazi wa Lea. Baba yake alisema katika kumbariki kwamba kikosi kingemshinda, lakini kwamba yeye angeshinda mwishoni.", "patron": "Maombezi yake huombwa kwa ajili ya askari; walioshindwa wanaoinuka tena."},
}
