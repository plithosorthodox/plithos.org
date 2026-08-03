#!/usr/bin/env python3
"""
Translations for the Prayers page: the page chrome, the section names, the
category headings, and the group headings.

These are descriptive and navigational strings. The prayers themselves are
translated separately and live in data/prayers-i18n.v1.<lang>.json.

Consumed by tools/build_prayers.py, which folds them into
data/prayers.v1.json so the page makes one request rather than two.

en is the fallback for anything absent, and the page marks a prayer whose own
text is unavailable in the chosen language rather than showing English under
another language's name.
"""

LANGS = ["en", "el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it",
         "sr", "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur"]

# ---------------------------------------------------------------- page chrome
UI = {
"en": {"navCal":"Calendar","navSaints":"Saints","navLib":"Library","navPrayers":"Prayers","navRule":"The Rule","navGlossary":"Glossary","navContact":"Contact",
 "h1":"Prayers","lede":"The traditional prayers of the Orthodox Church, ordered as a prayer book. Choose a section, or search.",
 "sections":"Sections","all":"All prayers","ph":"Search prayers","back":"All prayers","copy":"Copy","copied":"Copied",
 "none":"No prayer matches that.","n_one":"1 prayer","n_many":"# prayers","src":"Source","words":"words",
 "partial":"This prayer is not yet available in this language, and is shown in English."},

"el": {"navCal":"Ημερολόγιο","navSaints":"Άγιοι","navLib":"Βιβλιοθήκη","navPrayers":"Προσευχές","navRule":"Ὁ Κανόνας","navGlossary":"Γλωσσάρι","navContact":"Επικοινωνία",
 "h1":"Προσευχές","lede":"Οι παραδοσιακές προσευχές της Ορθοδόξου Εκκλησίας, κατά την τάξη του προσευχηταρίου. Επιλέξτε ενότητα ή αναζητήστε.",
 "sections":"Ενότητες","all":"Όλες οι προσευχές","ph":"Αναζήτηση προσευχών","back":"Όλες οι προσευχές","copy":"Αντιγραφή","copied":"Αντιγράφηκε",
 "none":"Καμία προσευχή δεν ταιριάζει.","n_one":"1 προσευχή","n_many":"# προσευχές","src":"Πηγή","words":"λέξεις",
 "partial":"Η προσευχή αυτή δεν είναι ακόμη διαθέσιμη σε αυτή τη γλώσσα και εμφανίζεται στα αγγλικά."},

"ru": {"navCal":"Календарь","navSaints":"Святые","navLib":"Библиотека","navPrayers":"Молитвы","navRule":"Правило","navGlossary":"Словарь","navContact":"Контакты",
 "h1":"Молитвы","lede":"Традиционные молитвы Православной Церкви, расположенные как в молитвослове. Выберите раздел или воспользуйтесь поиском.",
 "sections":"Разделы","all":"Все молитвы","ph":"Поиск молитв","back":"Все молитвы","copy":"Копировать","copied":"Скопировано",
 "none":"Ничего не найдено.","n_one":"1 молитва","n_many":"# молитв","src":"Источник","words":"слов",
 "partial":"Эта молитва пока недоступна на этом языке и показана по-английски."},

"ro": {"navCal":"Calendar","navSaints":"Sfinți","navLib":"Bibliotecă","navPrayers":"Rugăciuni","navRule":"Pravila","navGlossary":"Glosar","navContact":"Contact",
 "h1":"Rugăciuni","lede":"Rugăciunile tradiționale ale Bisericii Ortodoxe, rânduite ca într-un ceaslov. Alegeți o secțiune sau căutați.",
 "sections":"Secțiuni","all":"Toate rugăciunile","ph":"Caută rugăciuni","back":"Toate rugăciunile","copy":"Copiază","copied":"Copiat",
 "none":"Nicio rugăciune nu se potrivește.","n_one":"1 rugăciune","n_many":"# rugăciuni","src":"Sursă","words":"cuvinte",
 "partial":"Această rugăciune nu este încă disponibilă în această limbă și este arătată în engleză."},

"uk": {"navCal":"Календар","navSaints":"Святі","navLib":"Бібліотека","navPrayers":"Молитви","navRule":"Правило","navGlossary":"Словник","navContact":"Контакти",
 "h1":"Молитви","lede":"Традиційні молитви Православної Церкви, розташовані як у молитовнику. Оберіть розділ або скористайтеся пошуком.",
 "sections":"Розділи","all":"Усі молитви","ph":"Пошук молитов","back":"Усі молитви","copy":"Копіювати","copied":"Скопійовано",
 "none":"Нічого не знайдено.","n_one":"1 молитва","n_many":"# молитов","src":"Джерело","words":"слів",
 "partial":"Ця молитва поки недоступна цією мовою і показана англійською."},

"de": {"navCal":"Kalender","navSaints":"Heilige","navLib":"Bibliothek","navPrayers":"Gebete","navRule":"Die Regel","navGlossary":"Glossar","navContact":"Kontakt",
 "h1":"Gebete","lede":"Die überlieferten Gebete der Orthodoxen Kirche, geordnet wie ein Gebetbuch. Wählen Sie einen Abschnitt oder suchen Sie.",
 "sections":"Abschnitte","all":"Alle Gebete","ph":"Gebete suchen","back":"Alle Gebete","copy":"Kopieren","copied":"Kopiert",
 "none":"Kein Gebet gefunden.","n_one":"1 Gebet","n_many":"# Gebete","src":"Quelle","words":"Wörter",
 "partial":"Dieses Gebet ist in dieser Sprache noch nicht verfügbar und wird auf Englisch gezeigt."},

"es": {"navCal":"Calendario","navSaints":"Santos","navLib":"Biblioteca","navPrayers":"Oraciones","navRule":"La Regla","navGlossary":"Glosario","navContact":"Contacto",
 "h1":"Oraciones","lede":"Las oraciones tradicionales de la Iglesia Ortodoxa, ordenadas como un devocionario. Elija una sección o busque.",
 "sections":"Secciones","all":"Todas las oraciones","ph":"Buscar oraciones","back":"Todas las oraciones","copy":"Copiar","copied":"Copiado",
 "none":"Ninguna oración coincide.","n_one":"1 oración","n_many":"# oraciones","src":"Fuente","words":"palabras",
 "partial":"Esta oración aún no está disponible en este idioma y se muestra en inglés."},

"ar": {"navCal":"التقويم","navSaints":"القديسون","navLib":"المكتبة","navPrayers":"الصلوات","navRule":"القانون","navGlossary":"مسرد","navContact":"اتصل بنا",
 "h1":"الصلوات","lede":"صلوات الكنيسة الأرثوذكسية المتوارثة، مرتبة على نسق كتاب الصلوات. اختر قسماً أو ابحث.",
 "sections":"الأقسام","all":"كل الصلوات","ph":"البحث في الصلوات","back":"كل الصلوات","copy":"نسخ","copied":"تم النسخ",
 "none":"لا توجد صلاة مطابقة.","n_one":"صلاة واحدة","n_many":"# صلاة","src":"المصدر","words":"كلمة",
 "partial":"هذه الصلاة غير متوفرة بعد بهذه اللغة، وتُعرض بالإنجليزية."},

"fr": {"navCal":"Calendrier","navSaints":"Saints","navLib":"Bibliothèque","navPrayers":"Prières","navRule":"La Règle","navGlossary":"Glossaire","navContact":"Contact",
 "h1":"Prières","lede":"Les prières traditionnelles de l'Église orthodoxe, rangées comme un livre de prières. Choisissez une section ou cherchez.",
 "sections":"Sections","all":"Toutes les prières","ph":"Rechercher des prières","back":"Toutes les prières","copy":"Copier","copied":"Copié",
 "none":"Aucune prière ne correspond.","n_one":"1 prière","n_many":"# prières","src":"Source","words":"mots",
 "partial":"Cette prière n'est pas encore disponible dans cette langue; elle est montrée en anglais."},

"pt": {"navCal":"Calendário","navSaints":"Santos","navLib":"Biblioteca","navPrayers":"Orações","navRule":"A Regra","navGlossary":"Glossário","navContact":"Contacto",
 "h1":"Orações","lede":"As orações tradicionais da Igreja Ortodoxa, dispostas como um livro de orações. Escolha uma secção ou pesquise.",
 "sections":"Secções","all":"Todas as orações","ph":"Pesquisar orações","back":"Todas as orações","copy":"Copiar","copied":"Copiado",
 "none":"Nenhuma oração corresponde.","n_one":"1 oração","n_many":"# orações","src":"Fonte","words":"palavras",
 "partial":"Esta oração ainda não está disponível nesta língua e é mostrada em inglês."},

"it": {"navCal":"Calendario","navSaints":"Santi","navLib":"Biblioteca","navPrayers":"Preghiere","navRule":"La Regola","navGlossary":"Glossario","navContact":"Contatti",
 "h1":"Preghiere","lede":"Le preghiere tradizionali della Chiesa ortodossa, ordinate come un libro di preghiere. Scegliete una sezione o cercate.",
 "sections":"Sezioni","all":"Tutte le preghiere","ph":"Cerca preghiere","back":"Tutte le preghiere","copy":"Copia","copied":"Copiato",
 "none":"Nessuna preghiera corrisponde.","n_one":"1 preghiera","n_many":"# preghiere","src":"Fonte","words":"parole",
 "partial":"Questa preghiera non è ancora disponibile in questa lingua ed è mostrata in inglese."},

"sr": {"navCal":"Календар","navSaints":"Свети","navLib":"Библиотека","navPrayers":"Молитве","navRule":"Правило","navGlossary":"Речник","navContact":"Контакт",
 "h1":"Молитве","lede":"Традиционалне молитве Православне Цркве, поређане као у молитвенику. Изаберите одељак или претражите.",
 "sections":"Одељци","all":"Све молитве","ph":"Претрага молитава","back":"Све молитве","copy":"Копирај","copied":"Копирано",
 "none":"Ниједна молитва не одговара.","n_one":"1 молитва","n_many":"# молитава","src":"Извор","words":"речи",
 "partial":"Ова молитва још није доступна на овом језику и приказана је на енглеском."},

"ka": {"navCal":"კალენდარი","navSaints":"წმინდანები","navLib":"ბიბლიოთეკა","navPrayers":"ლოცვები","navRule":"წესი","navGlossary":"ლექსიკონი","navContact":"კონტაქტი",
 "h1":"ლოცვები","lede":"მართლმადიდებელი ეკლესიის ტრადიციული ლოცვები, ლოცვანის წესით დალაგებული. აირჩიეთ განყოფილება ან მოძებნეთ.",
 "sections":"განყოფილებები","all":"ყველა ლოცვა","ph":"ლოცვების ძიება","back":"ყველა ლოცვა","copy":"კოპირება","copied":"დაკოპირდა",
 "none":"შესაბამისი ლოცვა ვერ მოიძებნა.","n_one":"1 ლოცვა","n_many":"# ლოცვა","src":"წყარო","words":"სიტყვა",
 "partial":"ეს ლოცვა ჯერ არ არის ხელმისაწვდომი ამ ენაზე და ნაჩვენებია ინგლისურად."},

"zh": {"navCal":"日历","navSaints":"圣人","navLib":"图书馆","navPrayers":"祈祷文","navRule":"祈祷规则","navGlossary":"词汇表","navContact":"联系",
 "h1":"祈祷文","lede":"正教会传统祈祷文，依祈祷书之次序编排。请选择一个部分，或直接搜索。",
 "sections":"部分","all":"全部祈祷文","ph":"搜索祈祷文","back":"全部祈祷文","copy":"复制","copied":"已复制",
 "none":"没有符合的祈祷文。","n_one":"1 篇","n_many":"# 篇","src":"来源","words":"字",
 "partial":"此祈祷文尚无此语言版本，现以英文显示。"},

"ja": {"navCal":"暦","navSaints":"聖人","navLib":"図書室","navPrayers":"祈祷文","navRule":"祈りの規矩","navGlossary":"用語集","navContact":"お問い合わせ",
 "h1":"祈祷文","lede":"正教会の伝統的な祈祷文を、祈祷書の順に配したものです。部門をお選びいただくか、お探しください。",
 "sections":"部門","all":"すべての祈祷文","ph":"祈祷文を検索","back":"すべての祈祷文","copy":"コピー","copied":"コピーしました",
 "none":"該当する祈祷文はありません。","n_one":"1 篇","n_many":"# 篇","src":"典拠","words":"語",
 "partial":"この祈祷文はこの言語ではまだご用意がなく、英語で表示しております。"},

"ko": {"navCal":"달력","navSaints":"성인","navLib":"도서관","navPrayers":"기도문","navRule":"기도 규칙","navGlossary":"용어집","navContact":"연락",
 "h1":"기도문","lede":"정교회의 전통 기도문을 기도서의 차례대로 실었습니다. 항목을 고르시거나 검색하십시오.",
 "sections":"항목","all":"모든 기도문","ph":"기도문 검색","back":"모든 기도문","copy":"복사","copied":"복사됨",
 "none":"해당하는 기도문이 없습니다.","n_one":"1편","n_many":"# 편","src":"출처","words":"단어",
 "partial":"이 기도문은 아직 이 언어로 준비되지 않아 영어로 보여 드립니다."},

"sw": {"navCal":"Kalenda","navSaints":"Watakatifu","navLib":"Maktaba","navPrayers":"Sala","navRule":"Kanuni","navGlossary":"Kamusi","navContact":"Mawasiliano",
 "h1":"Sala","lede":"Sala za jadi za Kanisa la Orthodoksi, zilizopangwa kama kitabu cha sala. Chagua sehemu, au tafuta.",
 "sections":"Sehemu","all":"Sala zote","ph":"Tafuta sala","back":"Sala zote","copy":"Nakili","copied":"Imenakiliwa",
 "none":"Hakuna sala inayolingana.","n_one":"Sala 1","n_many":"Sala #","src":"Chanzo","words":"maneno",
 "partial":"Sala hii bado haipatikani kwa lugha hii, na imeonyeshwa kwa Kiingereza."},

"hy": {"navCal":"Օրացույց","navSaints":"Սուրբեր","navLib":"Գրադարան","navPrayers":"Աղոթքներ","navRule":"Կանոն","navGlossary":"Բառարան","navContact":"Կապ",
 "h1":"Աղոթքներ","lede":"Ուղղափառ Եկեղեցու ավանդական աղոթքները՝ աղոթագրքի կարգով դասավորված։ Ընտրեք բաժին կամ որոնեք։",
 "sections":"Բաժիններ","all":"Բոլոր աղոթքները","ph":"Որոնել աղոթքներ","back":"Բոլոր աղոթքները","copy":"Պատճենել","copied":"Պատճենվեց",
 "none":"Համապատասխան աղոթք չգտնվեց։","n_one":"1 աղոթք","n_many":"# աղոթք","src":"Աղբյուր","words":"բառ",
 "partial":"Այս աղոթքը դեռ հասանելի չէ այս լեզվով և ցուցադրվում է անգլերեն։"},

"arc": {"navCal":"ܣܘܼܪܓܵܕܵܐ","navSaints":"ܩܲܕܝܼܫܹ̈ܐ","navLib":"ܒܹܝܬ ܐܲܪܟܹܐ","navPrayers":"ܨܠܵܘܵܬܵܐ","navRule":"ܩܢܘܿܢܵܐ","navGlossary":"ܡܸܠܘܵܐܐ","navContact":"ܩܘܼܢܵܛܵܐ",
 "h1":"ܨܠܵܘܵܬܵܐ","lede":"ܨܠܵܘܵܬܵܐ ܥܲܬܝܼܩܵܬܵܐ ܕܥܹܕܬܵܐ ܬܪܝܼܨܲܬ ܫܘܼܒܚܵܐ, ܡܣܘܼܕܪܹ̈ܐ ܐܲܝܟ݂ ܟܬܵܒܵܐ ܕܲܨܠܵܘܵܬܵܐ.",
 "sections":"ܦܘܼܠܵܓܹ̈ܐ","all":"ܟܠ ܨܠܵܘܵܬܵܐ","ph":"ܒܨܵܝܵܐ ܒܲܨܠܵܘܵܬܵܐ","back":"ܟܠ ܨܠܵܘܵܬܵܐ","copy":"ܢܣܵܟ݂ܵܐ","copied":"ܢܘܼܣܟ݂ܵܐ ܥܒܝܼܕܵܐ",
 "none":"ܠܵܐ ܡܘܼܫܟ݂ܸܚܠܲܢ ܨܠܘܿܬܵܐ.","n_one":"1 ܨܠܘܿܬܵܐ","n_many":"# ܨܠܵܘܵܬܵܐ","src":"ܡܲܒܘܼܥܵܐ","words":"ܡܸܠܹ̈ܐ",
 "partial":"ܗܵܕܹܐ ܨܠܘܿܬܵܐ ܠܹܐ ܝܠܵܗ̇ ܗܲܕܟ݂ܵܐ ܒܗܵܢ ܠܸܫܵܢܵܐ, ܘܡܸܬܚܲܙܝܵܐ ܒܐܸܢܓܠܸܫܢܵܝܵܐ."},

"hi": {"navCal":"पंचांग","navSaints":"संत","navLib":"पुस्तकालय","navPrayers":"प्रार्थनाएँ","navRule":"नियम","navGlossary":"शब्दावली","navContact":"संपर्क",
 "h1":"प्रार्थनाएँ","lede":"रूढ़िवादी कलीसिया की पारंपरिक प्रार्थनाएँ, प्रार्थना-पुस्तक के क्रम में। कोई वर्ग चुनिए, या खोजिए।",
 "sections":"वर्ग","all":"सभी प्रार्थनाएँ","ph":"प्रार्थनाएँ खोजें","back":"सभी प्रार्थनाएँ","copy":"प्रतिलिपि","copied":"प्रतिलिपि हुई",
 "none":"कोई प्रार्थना नहीं मिली।","n_one":"1 प्रार्थना","n_many":"# प्रार्थनाएँ","src":"स्रोत","words":"शब्द",
 "partial":"यह प्रार्थना अभी इस भाषा में उपलब्ध नहीं है, और अंग्रेज़ी में दिखाई गई है।"},

"bn": {"navCal":"পঞ্জিকা","navSaints":"সাধুগণ","navLib":"গ্রন্থাগার","navPrayers":"প্রার্থনা","navRule":"নিয়ম","navGlossary":"শব্দকোষ","navContact":"যোগাযোগ",
 "h1":"প্রার্থনা","lede":"অর্থোডক্স মণ্ডলীর পরম্পরাগত প্রার্থনা, প্রার্থনাপুস্তকের ক্রমে সাজানো। একটি বিভাগ বাছুন, বা খুঁজুন।",
 "sections":"বিভাগ","all":"সব প্রার্থনা","ph":"প্রার্থনা খুঁজুন","back":"সব প্রার্থনা","copy":"অনুলিপি","copied":"অনুলিপি হয়েছে",
 "none":"মিলে এমন প্রার্থনা নেই।","n_one":"১টি প্রার্থনা","n_many":"# টি প্রার্থনা","src":"উৎস","words":"শব্দ",
 "partial":"এই প্রার্থনা এখনও এই ভাষায় পাওয়া যাচ্ছে না, ইংরেজিতে দেখানো হয়েছে।"},

"ur": {"navCal":"تقویم","navSaints":"مقدسین","navLib":"کتب خانہ","navPrayers":"دعائیں","navRule":"قاعدہ","navGlossary":"لغت","navContact":"رابطہ",
 "h1":"دعائیں","lede":"آرتھوڈکس کلیسیا کی روایتی دعائیں، دعا کی کتاب کی ترتیب پر۔ کوئی حصہ منتخب کیجیے، یا تلاش کیجیے۔",
 "sections":"حصے","all":"تمام دعائیں","ph":"دعائیں تلاش کریں","back":"تمام دعائیں","copy":"نقل","copied":"نقل ہو گیا",
 "none":"کوئی دعا نہیں ملی۔","n_one":"1 دعا","n_many":"# دعائیں","src":"ماخذ","words":"الفاظ",
 "partial":"یہ دعا ابھی اس زبان میں دستیاب نہیں، اور انگریزی میں دکھائی گئی ہے۔"},
}

# ------------------------------------------------------- section names (rail)
SECTIONS = {
"daily":       {"el":"Πρωί και Εσπέρας","ru":"Утренние и вечерние","ro":"Dimineața și seara","uk":"Ранкові та вечірні","de":"Morgen und Abend","es":"Mañana y tarde","ar":"صلوات الصباح والمساء","fr":"Matin et soir","pt":"Manhã e tarde","it":"Mattino e sera","sr":"Јутарње и вечерње","ka":"დილისა და საღამოს","zh":"晨昏祷","ja":"朝と夕","ko":"아침과 저녁","sw":"Asubuhi na jioni","hy":"Առավոտյան և երեկոյան","arc":"ܕܨܲܦܪܵܐ ܘܲܕܪܲܡܫܵܐ","hi":"प्रातः और सायं","bn":"প্রভাত ও সন্ধ্যা","ur":"صبح و شام"},
"hours":       {"el":"Οι Ώρες","ru":"Часы","ro":"Ceasurile","uk":"Часи","de":"Die Horen","es":"Las Horas","ar":"السواعي","fr":"Les Heures","pt":"As Horas","it":"Le Ore","sr":"Часови","ka":"ჟამნი","zh":"时课","ja":"時課","ko":"시과","sw":"Saa za sala","hy":"Ժամերգություններ","arc":"ܫܵܥܹ̈ܐ","hi":"होरा","bn":"হোরা","ur":"ساعات"},
"heart":       {"el":"Η Ευχή του Ιησού και σύντομες προσευχές","ru":"Иисусова молитва и краткие молитвы","ro":"Rugăciunea lui Iisus și rugăciuni scurte","uk":"Ісусова молитва і короткі молитви","de":"Das Jesusgebet und kurze Gebete","es":"La Oración de Jesús y oraciones breves","ar":"صلاة يسوع وصلوات قصيرة","fr":"La Prière de Jésus et prières brèves","pt":"A Oração de Jesus e orações breves","it":"La Preghiera di Gesù e preghiere brevi","sr":"Исусова молитва и кратке молитве","ka":"იესოს ლოცვა და მოკლე ლოცვები","zh":"耶稣祷文与短祷","ja":"イイススの祈りと短い祈り","ko":"예수 기도와 짧은 기도","sw":"Sala ya Yesu na sala fupi","hy":"Հիսուսյան աղոթք և կարճ աղոթքներ","arc":"ܨܠܘܿܬܵܐ ܕܝܼܫܘܿܥ ܘܲܨܠܵܘܵܬܵܐ ܟܲܪ̈ܝܵܬܵܐ","hi":"यीशु-प्रार्थना और लघु प्रार्थनाएँ","bn":"যীশু-প্রার্থনা ও সংক্ষিপ্ত প্রার্থনা","ur":"یسوع کی دعا اور مختصر دعائیں"},
"communion":   {"el":"Θεία Κοινωνία","ru":"Святое Причащение","ro":"Sfânta Împărtășanie","uk":"Святе Причастя","de":"Heilige Kommunion","es":"Santa Comunión","ar":"المناولة المقدسة","fr":"La Sainte Communion","pt":"Santa Comunhão","it":"Santa Comunione","sr":"Свето Причешће","ka":"წმიდა ზიარება","zh":"领圣体血","ja":"聖体礼儀の領聖","ko":"성찬","sw":"Komunyo Takatifu","hy":"Սուրբ Հաղորդություն","arc":"ܩܘܼܪܒܵܢܵܐ ܩܲܕܝܼܫܵܐ","hi":"पवित्र प्रभुभोज","bn":"পবিত্র সহভাগিতা","ur":"مقدس عشائے ربانی"},
"intercession":{"el":"Θεοτόκος, Άγγελοι και Άγιοι","ru":"Богородица, Ангелы и святые","ro":"Născătoarea de Dumnezeu, îngerii și sfinții","uk":"Богородиця, Ангели і святі","de":"Gottesmutter, Engel und Heilige","es":"La Theotokos, los ángeles y los santos","ar":"والدة الإله والملائكة والقديسون","fr":"La Théotokos, les anges et les saints","pt":"A Theotokos, os anjos e os santos","it":"La Theotokos, gli angeli e i santi","sr":"Богородица, анђели и свети","ka":"ღვთისმშობელი, ანგელოზები და წმინდანები","zh":"圣母、天使与圣人","ja":"生神女、天使、諸聖人","ko":"성모, 천사, 성인","sw":"Mzazi-Mungu, malaika na watakatifu","hy":"Աստվածածին, հրեշտակներ և սուրբեր","arc":"ܝܵܠܕܲܬ ܐܲܠܵܗܵܐ ܘܡܲܠܲܐܟܹ̈ܐ ܘܩܲܕܝܼܫܹ̈ܐ","hi":"थियोतोकोस, स्वर्गदूत और संत","bn":"থিওতোকোস, স্বর্গদূত ও সাধুগণ","ur":"والدہ خدا، فرشتے اور مقدسین"},
"others":      {"el":"Υπέρ των άλλων","ru":"О других","ro":"Pentru alții","uk":"За інших","de":"Für andere","es":"Por los demás","ar":"من أجل الآخرين","fr":"Pour les autres","pt":"Pelos outros","it":"Per gli altri","sr":"За друге","ka":"სხვათათვის","zh":"为他人","ja":"他者のために","ko":"다른 이를 위하여","sw":"Kwa ajili ya wengine","hy":"Ուրիշների համար","arc":"ܚܠܵܦ ܐ̄ܚܹܪ̈ܢܹܐ","hi":"दूसरों के लिए","bn":"অন্যদের জন্য","ur":"دوسروں کے لیے"},
"self":        {"el":"Υπέρ εαυτού","ru":"О себе","ro":"Pentru sine","uk":"За себе","de":"Für sich selbst","es":"Por uno mismo","ar":"من أجل النفس","fr":"Pour soi-même","pt":"Por si mesmo","it":"Per sé stessi","sr":"За себе","ka":"საკუთარი თავისთვის","zh":"为己","ja":"自らのために","ko":"자신을 위하여","sw":"Kwa ajili yako mwenyewe","hy":"Անձի համար","arc":"ܚܠܵܦ ܢܲܦ̮ܫܵܐ","hi":"अपने लिए","bn":"নিজের জন্য","ur":"اپنے لیے"},
"occasions":   {"el":"Ο βίος και οι περιστάσεις του","ru":"Житейские обстоятельства","ro":"Viața și împrejurările ei","uk":"Життєві обставини","de":"Das Leben und seine Anlässe","es":"La vida y sus ocasiones","ar":"الحياة ومناسباتها","fr":"La vie et ses occasions","pt":"A vida e as suas ocasiões","it":"La vita e le sue occasioni","sr":"Живот и његове прилике","ka":"ცხოვრება და მისი შემთხვევები","zh":"生活各样境遇","ja":"生活の折々に","ko":"삶의 여러 때에","sw":"Maisha na nyakati zake","hy":"Կյանքը և նրա առիթները","arc":"ܚܲܝܹ̈ܐ ܘܥܸܕܵܢܲܝ̈ܗܘܿܢ","hi":"जीवन और उसके अवसर","bn":"জীবন ও তার নানা উপলক্ষ","ur":"زندگی اور اس کے مواقع"},
"psalms":      {"el":"Ψαλμοί","ru":"Псалмы","ro":"Psalmi","uk":"Псалми","de":"Psalmen","es":"Salmos","ar":"المزامير","fr":"Psaumes","pt":"Salmos","it":"Salmi","sr":"Псалми","ka":"ფსალმუნები","zh":"圣咏","ja":"聖詠","ko":"시편","sw":"Zaburi","hy":"Սաղմոսներ","arc":"ܡܲܙܡܘܼܪܹ̈ܐ","hi":"भजन","bn":"গীতসংহিতা","ur":"زبور"},
}

# ------------------------------------------- group headings within a section
GROUPS = {
"The Order of Preparation": {"el":"Η Ακολουθία της Θείας Μεταλήψεως","ru":"Последование ко Святому Причащению","ro":"Rânduiala Sfintei Împărtășanii","uk":"Послідування до Святого Причастя","de":"Die Ordnung der Vorbereitung","es":"El Orden de Preparación","ar":"ترتيب الاستعداد","fr":"L'Office de préparation","pt":"A Ordem de Preparação","it":"L'Ufficio di preparazione","sr":"Последовање Светог Причешћа","ka":"მზადების წესი","zh":"预备之序","ja":"準備の式","ko":"준비의 차서","sw":"Utaratibu wa Maandalizi","hy":"Պատրաստության կարգ","arc":"ܛܘܼܟܵܣܵܐ ܕܛܘܼܝܵܒܵܐ","hi":"तैयारी का क्रम","bn":"প্রস্তুতির ক্রম","ur":"تیاری کی ترتیب"},
"Immediately before receiving": {"el":"Ἀμέσως πρὸ τῆς μεταλήψεως","ru":"Непосредственно перед причащением","ro":"Chiar înainte de împărtășire","uk":"Безпосередньо перед причастям","de":"Unmittelbar vor dem Empfang","es":"Inmediatamente antes de comulgar","ar":"قبيل التناول مباشرة","fr":"Immédiatement avant de communier","pt":"Imediatamente antes de comungar","it":"Immediatamente prima di comunicarsi","sr":"Непосредно пред причешће","ka":"უშუალოდ ზიარებამდე","zh":"临领之前","ja":"領聖の直前に","ko":"영성체 직전에","sw":"Kabla tu ya kupokea","hy":"Անմիջապես հաղորդությունից առաջ","arc":"ܩܲܕ݇ܡ ܩܘܼܪܒܵܢܵܐ ܡܸܚܕܵܐ","hi":"ग्रहण करने से ठीक पूर्व","bn":"গ্রহণের ঠিক পূর্বে","ur":"لینے سے عین پہلے"},
"After receiving": {"el":"Μετὰ τὴν μετάληψιν","ru":"После причащения","ro":"După împărtășire","uk":"Після причастя","de":"Nach dem Empfang","es":"Después de comulgar","ar":"بعد التناول","fr":"Après avoir communié","pt":"Depois de comungar","it":"Dopo essersi comunicati","sr":"После причешћа","ka":"ზიარების შემდეგ","zh":"领后","ja":"領聖の後に","ko":"영성체 후에","sw":"Baada ya kupokea","hy":"Հաղորդությունից հետո","arc":"ܒܵܬܲܪ ܩܘܼܪܒܵܢܵܐ","hi":"ग्रहण करने के पश्चात्","bn":"গ্রহণের পরে","ur":"لینے کے بعد"},
"The Jesus Prayer": {"el":"Η Ευχή του Ιησού","ru":"Иисусова молитва","ro":"Rugăciunea lui Iisus","uk":"Ісусова молитва","de":"Das Jesusgebet","es":"La Oración de Jesús","ar":"صلاة يسوع","fr":"La Prière de Jésus","pt":"A Oração de Jesus","it":"La Preghiera di Gesù","sr":"Исусова молитва","ka":"იესოს ლოცვა","zh":"耶稣祷文","ja":"イイススの祈り","ko":"예수 기도","sw":"Sala ya Yesu","hy":"Հիսուսյան աղոթք","arc":"ܨܠܘܿܬܵܐ ܕܝܼܫܘܿܥ","hi":"यीशु-प्रार्थना","bn":"যীশু-প্রার্থনা","ur":"یسوع کی دعا"},
"Short prayers for use through the day": {"el":"Σύντομες προσευχές για όλη την ημέρα","ru":"Краткие молитвы на всякий час","ro":"Rugăciuni scurte pentru toată ziua","uk":"Короткі молитви на всякий час","de":"Kurze Gebete für den Tag","es":"Oraciones breves para el día","ar":"صلوات قصيرة لسائر النهار","fr":"Prières brèves pour la journée","pt":"Orações breves para o dia","it":"Preghiere brevi per la giornata","sr":"Кратке молитве за сваки час","ka":"მოკლე ლოცვები დღის განმავლობაში","zh":"日间短祷","ja":"日中の短い祈り","ko":"하루 중의 짧은 기도","sw":"Sala fupi kwa mchana kutwa","hy":"Կարճ աղոթքներ օրվա ընթացքում","arc":"ܨܠܵܘܵܬܵܐ ܟܲܪ̈ܝܵܬܵܐ ܠܝܵܘܡܵܐ","hi":"दिनभर के लिए लघु प्रार्थनाएँ","bn":"সারাদিনের সংক্ষিপ্ত প্রার্থনা","ur":"دن بھر کے لیے مختصر دعائیں"},
}
