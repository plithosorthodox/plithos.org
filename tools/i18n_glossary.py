#!/usr/bin/env python3
"""
Translations for the Glossary page: the page chrome, the tag names on the
filter bar, and the names of the source languages shown beside a headword.

The headwords and definitions themselves are far larger and live one file per
language, under tools/glossary_terms/. They are emitted separately so a reader
fetches only the language in front of them.

Consumed by tools/build_glossary.py. en is the fallback throughout.
"""

LANGS = ["en", "el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it",
         "sr", "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur"]

RTL = ["ar", "arc", "ur"]

# ---------------------------------------------------------------- page chrome
UI = {
"en": {"navCal":"Calendar","navSaints":"Saints","navLib":"Library","navPrayers":"Prayers","navRule":"The Rule","navGlossary":"Glossary","navContact":"Contact",
 "h1":"Glossary","lede":"The vocabulary of the Orthodox Church: the services and their books, the vessels and vestments, the orders of clergy and monastics, the calendar and the fast, and the terms of the ascetic and theological tradition. Each word is given in its source language where one exists.",
 "ph":"Search terms, source words, and definitions","all":"All","none":"Nothing matches that.","n_one":"1 term","n_many":"# terms","see":"See also",
 "note":"The Greek, Church Slavonic and other forms beside each term are the word in its own tongue, and belong to the entry itself rather than being a rendering of the definition into that language.",
 "partial":"This entry is not yet available in this language, and is shown in English."},

"el": {"navCal":"Ημερολόγιο","navSaints":"Άγιοι","navLib":"Βιβλιοθήκη","navPrayers":"Προσευχές","navRule":"Ὁ Κανόνας","navGlossary":"Γλωσσάρι","navContact":"Επικοινωνία",
 "h1":"Γλωσσάρι","lede":"Το λεξιλόγιο της Ορθοδόξου Εκκλησίας: οι ακολουθίες και τα βιβλία τους, τα σκεύη και τα άμφια, οι τάξεις του κλήρου και των μοναχών, το ημερολόγιο και η νηστεία, και οι όροι της ασκητικής και θεολογικής παραδόσεως. Κάθε λέξη δίδεται στη γλώσσα της όπου υπάρχει.",
 "ph":"Αναζήτηση όρων, λέξεων και ορισμών","all":"Όλα","none":"Δεν βρέθηκε τίποτε.","n_one":"1 όρος","n_many":"# όροι","see":"Βλέπε επίσης",
 "note":"Οι ελληνικοί, εκκλησιαστικοί σλαβονικοί και λοιποί τύποι δίπλα σε κάθε όρο είναι η ίδια η λέξη στη γλώσσα της και ανήκουν στο ίδιο το λήμμα, δεν αποτελούν απόδοση του ορισμού στη γλώσσα εκείνη.",
 "partial":"Το λήμμα αυτό δεν είναι ακόμη διαθέσιμο σε αυτή τη γλώσσα και εμφανίζεται στα αγγλικά."},

"ru": {"navCal":"Календарь","navSaints":"Святые","navLib":"Библиотека","navPrayers":"Молитвы","navRule":"Правило","navGlossary":"Словарь","navContact":"Контакты",
 "h1":"Словарь","lede":"Словарь Православной Церкви: богослужения и их книги, сосуды и облачения, чины клира и монашества, календарь и пост, а также понятия аскетической и богословской традиции. Каждое слово дается на языке подлинника, где таковой есть.",
 "ph":"Поиск по терминам, словам и определениям","all":"Все","none":"Ничего не найдено.","n_one":"1 термин","n_many":"# терминов","see":"См. также",
 "note":"Греческие, церковнославянские и прочие формы рядом с каждым термином - это само слово на своем языке; они принадлежат самой статье, а не являются переводом определения на этот язык.",
 "partial":"Эта статья пока недоступна на этом языке и показана по-английски."},

"ro": {"navCal":"Calendar","navSaints":"Sfinți","navLib":"Bibliotecă","navPrayers":"Rugăciuni","navRule":"Pravila","navGlossary":"Glosar","navContact":"Contact",
 "h1":"Glosar","lede":"Vocabularul Bisericii Ortodoxe: slujbele și cărțile lor, vasele și veșmintele, treptele clerului și ale monahilor, calendarul și postul, și termenii tradiției ascetice și teologice. Fiecare cuvânt este dat în limba lui de obârșie, acolo unde există una.",
 "ph":"Caută termeni, cuvinte și definiții","all":"Toate","none":"Nu s-a găsit nimic.","n_one":"1 termen","n_many":"# termeni","see":"Vezi și",
 "note":"Formele grecești, slavone și celelalte de lângă fiecare termen sunt cuvântul însuși în limba lui și țin de articolul propriu-zis, nefiind o redare a definiției în acea limbă.",
 "partial":"Acest articol nu este încă disponibil în această limbă și este arătat în engleză."},

"uk": {"navCal":"Календар","navSaints":"Святі","navLib":"Бібліотека","navPrayers":"Молитви","navRule":"Правило","navGlossary":"Словник","navContact":"Контакти",
 "h1":"Словник","lede":"Словник Православної Церкви: богослужіння та їхні книги, посуд і облачення, чини кліру й чернецтва, календар і піст, а також поняття аскетичної та богословської традиції. Кожне слово подано мовою першоджерела, де така є.",
 "ph":"Пошук за термінами, словами й визначеннями","all":"Усі","none":"Нічого не знайдено.","n_one":"1 термін","n_many":"# термінів","see":"Див. також",
 "note":"Грецькі, церковнослов'янські та інші форми поряд із кожним терміном - це саме слово його мовою; вони належать до самої статті, а не є перекладом визначення тією мовою.",
 "partial":"Ця стаття поки недоступна цією мовою і показана англійською."},

"de": {"navCal":"Kalender","navSaints":"Heilige","navLib":"Bibliothek","navPrayers":"Gebete","navRule":"Die Regel","navGlossary":"Glossar","navContact":"Kontakt",
 "h1":"Glossar","lede":"Der Wortschatz der Orthodoxen Kirche: die Gottesdienste und ihre Bücher, die Gefässe und Gewänder, die Ordnungen der Geistlichen und der Mönche, Kalender und Fasten, und die Begriffe der asketischen und theologischen Überlieferung. Jedes Wort steht in seiner Ursprungssprache, wo es eine gibt.",
 "ph":"Begriffe, Wörter und Erklärungen durchsuchen","all":"Alle","none":"Nichts gefunden.","n_one":"1 Begriff","n_many":"# Begriffe","see":"Siehe auch",
 "note":"Die griechischen, kirchenslawischen und übrigen Formen neben jedem Begriff sind das Wort in seiner eigenen Sprache und gehören zum Eintrag selbst; sie sind keine Übertragung der Erklärung in jene Sprache.",
 "partial":"Dieser Eintrag ist in dieser Sprache noch nicht verfügbar und wird auf Englisch gezeigt."},

"es": {"navCal":"Calendario","navSaints":"Santos","navLib":"Biblioteca","navPrayers":"Oraciones","navRule":"La Regla","navGlossary":"Glosario","navContact":"Contacto",
 "h1":"Glosario","lede":"El vocabulario de la Iglesia Ortodoxa: los oficios y sus libros, los vasos y las vestiduras, los órdenes del clero y de los monjes, el calendario y el ayuno, y los términos de la tradición ascética y teológica. Cada palabra se da en su lengua de origen donde la hay.",
 "ph":"Buscar términos, palabras y definiciones","all":"Todos","none":"No se ha encontrado nada.","n_one":"1 término","n_many":"# términos","see":"Véase también",
 "note":"Las formas griegas, eslavas y demás junto a cada término son la palabra en su propia lengua y pertenecen a la entrada misma; no son una traducción de la definición a esa lengua.",
 "partial":"Esta entrada aún no está disponible en este idioma y se muestra en inglés."},

"ar": {"navCal":"التقويم","navSaints":"القديسون","navLib":"المكتبة","navPrayers":"الصلوات","navRule":"القانون","navGlossary":"مسرد","navContact":"اتصل بنا",
 "h1":"مسرد المصطلحات","lede":"مفردات الكنيسة الأرثوذكسية: الخدم وكتبها، والآنية والحلل، ورتب الإكليروس والرهبان، والتقويم والصوم، ومصطلحات التقليد النسكي واللاهوتي. وكل كلمة معطاة بلغتها الأصلية حيث توجد.",
 "ph":"ابحث في المصطلحات والكلمات والتعريفات","all":"الكل","none":"لا يوجد ما يطابق.","n_one":"مصطلح واحد","n_many":"# مصطلحاً","see":"انظر أيضاً",
 "note":"الصيغ اليونانية والسلافونية وغيرها بجانب كل مصطلح هي الكلمة نفسها بلغتها، وتخص المدخل ذاته، وليست ترجمة للتعريف إلى تلك اللغة.",
 "partial":"هذا المدخل غير متوفر بعد بهذه اللغة، ويُعرض بالإنجليزية."},

"fr": {"navCal":"Calendrier","navSaints":"Saints","navLib":"Bibliothèque","navPrayers":"Prières","navRule":"La Règle","navGlossary":"Glossaire","navContact":"Contact",
 "h1":"Glossaire","lede":"Le vocabulaire de l'Église orthodoxe: les offices et leurs livres, les vases et les vêtements, les ordres du clergé et des moines, le calendrier et le jeûne, et les termes de la tradition ascétique et théologique. Chaque mot est donné dans sa langue d'origine là où il en existe une.",
 "ph":"Rechercher termes, mots et définitions","all":"Tous","none":"Rien ne correspond.","n_one":"1 terme","n_many":"# termes","see":"Voir aussi",
 "note":"Les formes grecques, slavonnes et autres à côté de chaque terme sont le mot dans sa propre langue et appartiennent à l'entrée elle-même; ce n'est pas une traduction de la définition dans cette langue.",
 "partial":"Cette entrée n'est pas encore disponible dans cette langue; elle est montrée en anglais."},

"pt": {"navCal":"Calendário","navSaints":"Santos","navLib":"Biblioteca","navPrayers":"Orações","navRule":"A Regra","navGlossary":"Glossário","navContact":"Contacto",
 "h1":"Glossário","lede":"O vocabulário da Igreja Ortodoxa: os ofícios e os seus livros, os vasos e as vestes, as ordens do clero e dos monges, o calendário e o jejum, e os termos da tradição ascética e teológica. Cada palavra é dada na sua língua de origem onde existe uma.",
 "ph":"Pesquisar termos, palavras e definições","all":"Todos","none":"Nada corresponde.","n_one":"1 termo","n_many":"# termos","see":"Ver também",
 "note":"As formas gregas, eslavas e outras junto de cada termo são a palavra na sua própria língua e pertencem à própria entrada; não são uma tradução da definição para essa língua.",
 "partial":"Esta entrada ainda não está disponível nesta língua e é mostrada em inglês."},

"it": {"navCal":"Calendario","navSaints":"Santi","navLib":"Biblioteca","navPrayers":"Preghiere","navRule":"La Regola","navGlossary":"Glossario","navContact":"Contatti",
 "h1":"Glossario","lede":"Il lessico della Chiesa ortodossa: gli uffici e i loro libri, i vasi e i paramenti, gli ordini del clero e dei monaci, il calendario e il digiuno, e i termini della tradizione ascetica e teologica. Ogni parola è data nella sua lingua d'origine dove ve n'è una.",
 "ph":"Cerca termini, parole e definizioni","all":"Tutti","none":"Nessun risultato.","n_one":"1 termine","n_many":"# termini","see":"Vedi anche",
 "note":"Le forme greche, slavoniche e le altre accanto a ciascun termine sono la parola nella sua lingua e appartengono alla voce stessa; non sono una resa della definizione in quella lingua.",
 "partial":"Questa voce non è ancora disponibile in questa lingua ed è mostrata in inglese."},

"sr": {"navCal":"Календар","navSaints":"Свети","navLib":"Библиотека","navPrayers":"Молитве","navRule":"Правило","navGlossary":"Речник","navContact":"Контакт",
 "h1":"Речник","lede":"Речник Православне Цркве: богослужења и њихове књиге, сасуди и одежде, чинови клира и монаштва, календар и пост, и појмови подвижничког и богословског предања. Свака реч дата је на свом изворном језику где таквог има.",
 "ph":"Претрага појмова, речи и одредница","all":"Све","none":"Ништа није нађено.","n_one":"1 појам","n_many":"# појмова","see":"Види и",
 "note":"Грчки, црквенословенски и остали облици поред сваког појма јесу сама реч на свом језику и припадају самој одредници, а нису превод одреднице на тај језик.",
 "partial":"Ова одредница још није доступна на овом језику и приказана је на енглеском."},

"ka": {"navCal":"კალენდარი","navSaints":"წმინდანები","navLib":"ბიბლიოთეკა","navPrayers":"ლოცვები","navRule":"წესი","navGlossary":"ლექსიკონი","navContact":"კონტაქტი",
 "h1":"ლექსიკონი","lede":"მართლმადიდებელი ეკლესიის ლექსიკა: მსახურებანი და მათი წიგნები, ჭურჭელი და შესამოსელი, სამღვდელოებისა და მონაზონთა ხარისხები, კალენდარი და მარხვა, აგრეთვე ასკეტური და საღვთისმეტყველო ტრადიციის ცნებები. თითოეული სიტყვა მოცემულია თავის წყაროენაზე, სადაც ასეთი არსებობს.",
 "ph":"ტერმინების, სიტყვებისა და განმარტებების ძიება","all":"ყველა","none":"ვერაფერი მოიძებნა.","n_one":"1 ტერმინი","n_many":"# ტერმინი","see":"იხ. აგრეთვე",
 "note":"ბერძნული, საეკლესიო სლავური და სხვა ფორმები თითოეული ტერმინის გვერდით არის თავად სიტყვა თავის ენაზე და ეკუთვნის თვით სტატიას, და არა განმარტების თარგმანს იმ ენაზე.",
 "partial":"ეს სტატია ჯერ არ არის ხელმისაწვდომი ამ ენაზე და ნაჩვენებია ინგლისურად."},

"zh": {"navCal":"日历","navSaints":"圣人","navLib":"图书馆","navPrayers":"祈祷文","navRule":"祈祷规则","navGlossary":"词汇表","navContact":"联系",
 "h1":"词汇表","lede":"正教会的用语：各样礼仪及其经书、圣器与祭衣、圣职与修道的品级、历法与斋期，以及苦修与神学传统中的名词。凡有原文者，皆附其原文。",
 "ph":"搜索词条、原文与释义","all":"全部","none":"没有符合的词条。","n_one":"1 条","n_many":"# 条","see":"参见",
 "note":"每一词条旁的希腊文、教会斯拉夫文及其他形式，是该词在其本身语言中的写法，属于词条本身，并非将释义译成该语言。",
 "partial":"此词条尚无此语言版本，现以英文显示。"},

"ja": {"navCal":"暦","navSaints":"聖人","navLib":"図書室","navPrayers":"祈祷文","navRule":"祈りの規矩","navGlossary":"用語集","navContact":"お問い合わせ",
 "h1":"用語集","lede":"正教会の用語です。奉神礼とその書、器と祭服、聖職と修道の品級、暦と斎、そして修徳と神学の伝統における言葉を収めます。原語のあるものは、その原語を添えました。",
 "ph":"用語・原語・語釈を検索","all":"すべて","none":"該当する語はありません。","n_one":"1 語","n_many":"# 語","see":"参照",
 "note":"各項目に添えたギリシア語、教会スラヴ語その他の形は、その語をそれぞれの言語で記したものであり、項目そのものに属します。語釈をその言語に訳したものではありません。",
 "partial":"この項目はこの言語ではまだご用意がなく、英語で表示しております。"},

"ko": {"navCal":"달력","navSaints":"성인","navLib":"도서관","navPrayers":"기도문","navRule":"기도 규칙","navGlossary":"용어집","navContact":"연락",
 "h1":"용어집","lede":"정교회의 용어입니다. 예배와 그 책들, 그릇과 제의, 성직과 수도의 품계, 달력과 재계, 그리고 수덕과 신학 전통의 용어를 담았습니다. 원어가 있는 것은 그 원어를 함께 실었습니다.",
 "ph":"용어, 원어, 뜻풀이 검색","all":"전체","none":"해당하는 용어가 없습니다.","n_one":"1개 용어","n_many":"# 개 용어","see":"함께 보기",
 "note":"각 항목 옆의 그리스어, 교회 슬라브어 및 그 밖의 형태는 그 낱말을 제 언어로 적은 것이며 항목 자체에 속합니다. 뜻풀이를 그 언어로 옮긴 것이 아닙니다.",
 "partial":"이 항목은 아직 이 언어로 준비되지 않아 영어로 보여 드립니다."},

"sw": {"navCal":"Kalenda","navSaints":"Watakatifu","navLib":"Maktaba","navPrayers":"Sala","navRule":"Kanuni","navGlossary":"Kamusi","navContact":"Mawasiliano",
 "h1":"Kamusi","lede":"Msamiati wa Kanisa la Orthodoksi: ibada na vitabu vyake, vyombo na mavazi, madaraja ya makasisi na watawa, kalenda na mfungo, na maneno ya mapokeo ya kujinyima na ya kitheolojia. Kila neno limetolewa katika lugha yake ya asili panapokuwa na moja.",
 "ph":"Tafuta maneno, asili zake, na maelezo","all":"Yote","none":"Hakuna kinacholingana.","n_one":"Neno 1","n_many":"Maneno #","see":"Tazama pia",
 "note":"Maumbo ya Kiyunani, Kislavoni cha Kanisa na mengineyo yaliyo kando ya kila neno ni neno lenyewe katika lugha yake, na ni sehemu ya kidahizo chenyewe, si tafsiri ya maelezo katika lugha hiyo.",
 "partial":"Kidahizo hiki bado hakipatikani kwa lugha hii, na kimeonyeshwa kwa Kiingereza."},

"hy": {"navCal":"Օրացույց","navSaints":"Սուրբեր","navLib":"Գրադարան","navPrayers":"Աղոթքներ","navRule":"Կանոն","navGlossary":"Բառարան","navContact":"Կապ",
 "h1":"Բառարան","lede":"Ուղղափառ Եկեղեցու բառապաշարը՝ ժամերգություններն ու դրանց գրքերը, անոթներն ու զգեստները, հոգևորականների և վանականների աստիճանները, օրացույցն ու պահքը, և ճգնական ու աստվածաբանական ավանդույթի հասկացությունները։ Յուրաքանչյուր բառ տրված է իր սկզբնաղբյուր լեզվով, ուր այդպիսին կա։",
 "ph":"Որոնել եզրեր, բնագիր բառեր և բացատրություններ","all":"Բոլորը","none":"Ոչինչ չգտնվեց։","n_one":"1 եզր","n_many":"# եզր","see":"Տես նաև",
 "note":"Յուրաքանչյուր եզրի կողքին դրված հունարեն, եկեղեցասլավոնական և այլ ձևերը հենց բառն են իր լեզվով և պատկանում են բուն հոդվածին, ոչ թե բացատրության թարգմանությունն են այդ լեզվով։",
 "partial":"Այս հոդվածը դեռ հասանելի չէ այս լեզվով և ցուցադրվում է անգլերեն։"},

"arc": {"navCal":"ܣܘܼܪܓܵܕܵܐ","navSaints":"ܩܲܕܝܼܫܹ̈ܐ","navLib":"ܒܹܝܬ ܐܲܪܟܹܐ","navPrayers":"ܨܠܵܘܵܬܵܐ","navRule":"ܩܢܘܿܢܵܐ","navGlossary":"ܡܸܠܘܵܐܐ","navContact":"ܩܘܼܢܵܛܵܐ",
 "h1":"ܡܸܠܘܵܐܐ","lede":"ܡܸܠܹ̈ܐ ܕܥܹܕܬܵܐ ܬܪܝܼܨܲܬ ܫܘܼܒܚܵܐ: ܬܸܫܡܸܫܵܬܵܐ ܘܲܟ݂ܬܵܒܲܝ̈ܗܹܝܢ, ܘܡܵܐܢܹ̈ܐ ܘܢܲܚܬܹ̈ܐ, ܘܕܲܪ̈ܓܹܐ ܕܟܵܗܢܘܼܬܵܐ ܘܕܲܝܪܵܝܘܼܬܵܐ, ܘܣܘܼܪܓܵܕܵܐ ܘܨܵܘܡܵܐ, ܘܡܸܠܹ̈ܐ ܕܝܘܼܒܵܠܵܐ ܢܲܙܝܼܪܵܝܵܐ ܘܬܹܐܘܿܠܘܿܓ݂ܵܝܵܐ.",
 "ph":"ܒܨܵܝܵܐ ܒܡܸܠܹ̈ܐ ܘܲܒ݂ܦܘܼܫܵܩܹ̈ܐ","all":"ܟܠ","none":"ܠܵܐ ܡܘܼܫܟ݂ܸܚܠܲܢ ܡܸܢܕܝܼ.","n_one":"1 ܡܸܠܬܵܐ","n_many":"# ܡܸܠܹ̈ܐ","see":"ܚܙܝܼ ܐܵܦ",
 "note":"ܐܸܣܟܹܡܹ̈ܐ ܝܵܘܢܵܝܹܐ ܘܲܣܠܵܒ݂ܵܝܹܐ ܘܐ̄ܚܪ̈ܢܹܐ ܕܥܲܠ ܓܹܢܒ݂ ܟܠ ܡܸܠܬܵܐ ܝܼܢܵܐ ܗܝܼ ܡܸܠܬܵܐ ܒܠܸܫܵܢܵܗ̇, ܘܫܲܝܵܟ݂ܝܼ ܠܡܸܠܬܵܐ ܓܵܘܵܗ̇, ܘܠܵܐ ܝܢܵܐ ܡܲܥܒܲܪܬܵܐ ܕܦܘܼܫܵܩܵܐ ܠܗܵܘ ܠܸܫܵܢܵܐ.",
 "partial":"ܗܵܕܹܐ ܡܸܠܬܵܐ ܠܹܐ ܝܠܵܗ̇ ܗܲܕܟ݂ܵܐ ܒܗܵܢ ܠܸܫܵܢܵܐ, ܘܡܸܬܚܲܙܝܵܐ ܒܐܸܢܓܠܸܫܢܵܝܵܐ."},

"hi": {"navCal":"पंचांग","navSaints":"संत","navLib":"पुस्तकालय","navPrayers":"प्रार्थनाएँ","navRule":"नियम","navGlossary":"शब्दावली","navContact":"संपर्क",
 "h1":"शब्दावली","lede":"रूढ़िवादी कलीसिया की शब्दावली: आराधनाएँ और उनकी पुस्तकें, पात्र और परिधान, याजकों तथा संन्यासियों की श्रेणियाँ, पंचांग और उपवास, तथा तपस्वी एवं धर्मविज्ञान परंपरा के पारिभाषिक शब्द। जहाँ मूल भाषा है, वहाँ प्रत्येक शब्द उसी में दिया गया है।",
 "ph":"शब्द, मूल रूप और अर्थ खोजें","all":"सभी","none":"कुछ नहीं मिला।","n_one":"1 शब्द","n_many":"# शब्द","see":"यह भी देखिए",
 "note":"प्रत्येक शब्द के साथ दिए गए यूनानी, कलीसियाई स्लावोनी और अन्य रूप उस शब्द को उसी की भाषा में लिखा हुआ रूप हैं, और वे प्रविष्टि का ही अंग हैं; वे अर्थ का उस भाषा में अनुवाद नहीं हैं।",
 "partial":"यह प्रविष्टि अभी इस भाषा में उपलब्ध नहीं है, और अंग्रेज़ी में दिखाई गई है।"},

"bn": {"navCal":"পঞ্জিকা","navSaints":"সাধুগণ","navLib":"গ্রন্থাগার","navPrayers":"প্রার্থনা","navRule":"নিয়ম","navGlossary":"শব্দকোষ","navContact":"যোগাযোগ",
 "h1":"শব্দকোষ","lede":"অর্থোডক্স মণ্ডলীর পরিভাষা: উপাসনা ও তার পুস্তকসমূহ, পাত্র ও পরিচ্ছদ, যাজক ও সন্ন্যাসীদের স্তর, পঞ্জিকা ও উপবাস, এবং তপশ্চর্যা ও ধর্মতত্ত্ব পরম্পরার পারিভাষিক শব্দ। যেখানে মূল ভাষা আছে, প্রতিটি শব্দ সেই ভাষাতেই দেওয়া হয়েছে।",
 "ph":"শব্দ, মূল রূপ ও অর্থ খুঁজুন","all":"সব","none":"কিছুই মেলেনি।","n_one":"১টি শব্দ","n_many":"# টি শব্দ","see":"আরও দেখুন",
 "note":"প্রতিটি শব্দের পাশে দেওয়া গ্রিক, মণ্ডলী-স্লাভোনীয় ও অন্যান্য রূপ হল সেই শব্দটিই নিজ ভাষায় লিখিত, এবং তা ভুক্তিরই অংশ; সেগুলি অর্থের সেই ভাষায় অনুবাদ নয়।",
 "partial":"এই ভুক্তি এখনও এই ভাষায় পাওয়া যাচ্ছে না, ইংরেজিতে দেখানো হয়েছে।"},

"ur": {"navCal":"تقویم","navSaints":"مقدسین","navLib":"کتب خانہ","navPrayers":"دعائیں","navRule":"قاعدہ","navGlossary":"لغت","navContact":"رابطہ",
 "h1":"لغت","lede":"آرتھوڈکس کلیسیا کی اصطلاحات: عبادات اور اُن کی کتابیں، برتن اور لباس، کاہنوں اور راہبوں کے درجات، تقویم اور روزہ، اور ریاضت و الٰہیات کی روایت کی اصطلاحیں۔ جہاں اصل زبان موجود ہے، وہاں ہر لفظ اُسی میں دیا گیا ہے۔",
 "ph":"اصطلاحات، اصل الفاظ اور تشریحات تلاش کریں","all":"سب","none":"کچھ نہیں ملا۔","n_one":"1 اصطلاح","n_many":"# اصطلاحات","see":"یہ بھی دیکھیے",
 "note":"ہر اصطلاح کے ساتھ دی گئی یونانی، کلیسیائی سلاوونی اور دیگر صورتیں خود وہی لفظ اپنی زبان میں ہیں، اور وہ اندراج ہی کا حصہ ہیں؛ وہ تشریح کا اُس زبان میں ترجمہ نہیں۔",
 "partial":"یہ اندراج ابھی اس زبان میں دستیاب نہیں، اور انگریزی میں دکھایا گیا ہے۔"},
}

# ------------------------------------------------- names of the source scripts
LGNAMES = {
"el": {"el":"Ελληνικά","ru":"греческий","ro":"greacă","uk":"грецька","de":"Griechisch","es":"griego","ar":"يونانية","fr":"grec","pt":"grego","it":"greco","sr":"грчки","ka":"ბერძნული","zh":"希腊文","ja":"ギリシア語","ko":"그리스어","sw":"Kiyunani","hy":"հունարեն","arc":"ܝܵܘܢܵܝܵܐ","hi":"यूनानी","bn":"গ্রিক","ur":"یونانی"},
"cu": {"el":"Εκκλησιαστικά σλαβονικά","ru":"церковнославянский","ro":"slavonă bisericească","uk":"церковнослов'янська","de":"Kirchenslawisch","es":"eslavo eclesiástico","ar":"سلافونية كنسية","fr":"slavon d'église","pt":"eslavo eclesiástico","it":"slavo ecclesiastico","sr":"црквенословенски","ka":"საეკლესიო სლავური","zh":"教会斯拉夫文","ja":"教会スラヴ語","ko":"교회 슬라브어","sw":"Kislavoni cha Kanisa","hy":"եկեղեցասլավոնական","arc":"ܣܠܵܒ݂ܵܝܵܐ ܥܹܕܬܵܢܵܝܵܐ","hi":"कलीसियाई स्लावोनी","bn":"মণ্ডলী-স্লাভোনীয়","ur":"کلیسیائی سلاوونی"},
"la": {"el":"Λατινικά","ru":"латинский","ro":"latină","uk":"латинська","de":"Latein","es":"latín","ar":"لاتينية","fr":"latin","pt":"latim","it":"latino","sr":"латински","ka":"ლათინური","zh":"拉丁文","ja":"ラテン語","ko":"라틴어","sw":"Kilatini","hy":"լատիներեն","arc":"ܠܵܛܝܼܢܵܝܵܐ","hi":"लातीनी","bn":"লাতিন","ur":"لاطینی"},
"ar": {"el":"Αραβικά","ru":"арабский","ro":"arabă","uk":"арабська","de":"Arabisch","es":"árabe","ar":"عربية","fr":"arabe","pt":"árabe","it":"arabo","sr":"арапски","ka":"არაბული","zh":"阿拉伯文","ja":"アラビア語","ko":"아랍어","sw":"Kiarabu","hy":"արաբերեն","arc":"ܥܲܪܒ݂ܵܝܵܐ","hi":"अरबी","bn":"আরবি","ur":"عربی"},
"ka": {"el":"Γεωργιανά","ru":"грузинский","ro":"georgiană","uk":"грузинська","de":"Georgisch","es":"georgiano","ar":"جورجية","fr":"géorgien","pt":"georgiano","it":"georgiano","sr":"грузијски","ka":"ქართული","zh":"格鲁吉亚文","ja":"グルジア語","ko":"조지아어","sw":"Kijojia","hy":"վրացերեն","arc":"ܓܘܼܪܓ݂ܵܝܵܐ","hi":"जॉर्जियाई","bn":"জর্জীয়","ur":"جارجیائی"},
"hy": {"el":"Αρμενικά","ru":"армянский","ro":"armeană","uk":"вірменська","de":"Armenisch","es":"armenio","ar":"أرمنية","fr":"arménien","pt":"arménio","it":"armeno","sr":"јерменски","ka":"სომხური","zh":"亚美尼亚文","ja":"アルメニア語","ko":"아르메니아어","sw":"Kiarmenia","hy":"հայերեն","arc":"ܐܲܪܡܢܵܝܵܐ","hi":"आर्मेनियाई","bn":"আর্মেনীয়","ur":"آرمینیائی"},
"arc": {"el":"Συριακά","ru":"сирийский","ro":"siriacă","uk":"сирійська","de":"Syrisch","es":"siríaco","ar":"سريانية","fr":"syriaque","pt":"siríaco","it":"siriaco","sr":"сиријски","ka":"სირიული","zh":"叙利亚文","ja":"シリア語","ko":"시리아어","sw":"Kisiria","hy":"ասորերեն","arc":"ܣܘܼܪܝܵܝܵܐ","hi":"सुरयानी","bn":"সিরীয়","ur":"سریانی"},
}

# ------------------------------------------------------- tag names (filter bar)
TAGS = {
"eucharist": {"el":"Θεία Ευχαριστία","ru":"Евхаристия","ro":"Euharistie","uk":"Євхаристія","de":"Eucharistie","es":"Eucaristía","ar":"الإفخارستيا","fr":"Eucharistie","pt":"Eucaristia","it":"Eucaristia","sr":"Евхаристија","ka":"ევქარისტია","zh":"圣体血","ja":"聖体","ko":"성찬","sw":"Ekaristia","hy":"Հաղորդություն","arc":"ܩܘܼܪܒܵܢܵܐ","hi":"यूखरिस्त","bn":"ইউখারিস্ট","ur":"شکرگزاری"},
"ascetic": {"el":"Ασκητικά","ru":"аскетика","ro":"asceză","uk":"аскетика","de":"Askese","es":"ascesis","ar":"النسك","fr":"ascèse","pt":"ascese","it":"ascesi","sr":"подвижништво","ka":"ასკეტიკა","zh":"苦修","ja":"修徳","ko":"수덕","sw":"kujinyima","hy":"ճգնություն","arc":"ܢܙܝܼܪܘܼܬܵܐ","hi":"तपस्या","bn":"তপশ্চর্যা","ur":"ریاضت"},
"calendar": {"el":"Ημερολόγιο","ru":"календарь","ro":"calendar","uk":"календар","de":"Kalender","es":"calendario","ar":"التقويم","fr":"calendrier","pt":"calendário","it":"calendario","sr":"календар","ka":"კალენდარი","zh":"历法","ja":"暦","ko":"달력","sw":"kalenda","hy":"օրացույց","arc":"ܣܘܼܪܓܵܕܵܐ","hi":"पंचांग","bn":"পঞ্জিকা","ur":"تقویم"},
"hymn": {"el":"Ύμνοι","ru":"песнопения","ro":"imne","uk":"піснеспіви","de":"Hymnen","es":"himnos","ar":"التسابيح","fr":"hymnes","pt":"hinos","it":"inni","sr":"песмопенија","ka":"საგალობლები","zh":"颂歌","ja":"讃詞","ko":"찬가","sw":"nyimbo","hy":"շարականներ","arc":"ܙܘܼܡܵܪܹ̈ܐ","hi":"स्तोत्र","bn":"স্তোত্র","ur":"مناجات"},
"service": {"el":"Ακολουθίες","ru":"богослужение","ro":"slujbe","uk":"богослужіння","de":"Gottesdienst","es":"oficios","ar":"الخدم","fr":"offices","pt":"ofícios","it":"uffici","sr":"богослужење","ka":"მსახურება","zh":"礼仪","ja":"奉神礼","ko":"예배","sw":"ibada","hy":"ժամերգություն","arc":"ܬܸܫܡܸܫܬܵܐ","hi":"आराधना","bn":"উপাসনা","ur":"عبادت"},
"monastic": {"el":"Μοναχικά","ru":"монашество","ro":"monahism","uk":"чернецтво","de":"Mönchtum","es":"monacato","ar":"الرهبنة","fr":"monachisme","pt":"monaquismo","it":"monachesimo","sr":"монаштво","ka":"მონაზვნობა","zh":"修道","ja":"修道","ko":"수도","sw":"utawa","hy":"վանականություն","arc":"ܕܲܝܪܵܝܘܼܬܵܐ","hi":"संन्यास","bn":"সন্ন্যাস","ur":"رہبانیت"},
"vestment": {"el":"Άμφια","ru":"облачения","ro":"veșminte","uk":"облачення","de":"Gewänder","es":"vestiduras","ar":"الحلل","fr":"vêtements","pt":"vestes","it":"paramenti","sr":"одежде","ka":"შესამოსელი","zh":"祭衣","ja":"祭服","ko":"제의","sw":"mavazi","hy":"զգեստներ","arc":"ܢܲܚܬܹ̈ܐ","hi":"परिधान","bn":"পরিচ্ছদ","ur":"لباس"},
"order": {"el":"Τάξεις","ru":"чины","ro":"trepte","uk":"чини","de":"Weihestufen","es":"órdenes","ar":"الرتب","fr":"ordres","pt":"ordens","it":"ordini","sr":"чинови","ka":"ხარისხები","zh":"品级","ja":"品級","ko":"품계","sw":"madaraja","hy":"աստիճաններ","arc":"ܕܲܪ̈ܓܹܐ","hi":"श्रेणियाँ","bn":"স্তর","ur":"درجات"},
"book": {"el":"Βιβλία","ru":"книги","ro":"cărți","uk":"книги","de":"Bücher","es":"libros","ar":"الكتب","fr":"livres","pt":"livros","it":"libri","sr":"књиге","ka":"წიგნები","zh":"经书","ja":"書","ko":"책","sw":"vitabu","hy":"գրքեր","arc":"ܟܬܵܒܹ̈ܐ","hi":"पुस्तकें","bn":"পুস্তক","ur":"کتابیں"},
"vessel": {"el":"Σκεύη","ru":"сосуды","ro":"vase","uk":"посуд","de":"Gefässe","es":"vasos","ar":"الآنية","fr":"vases","pt":"vasos","it":"vasi","sr":"сасуди","ka":"ჭურჭელი","zh":"圣器","ja":"器","ko":"제구","sw":"vyombo","hy":"անոթներ","arc":"ܡܵܐܢܹ̈ܐ","hi":"पात्र","bn":"পাত্র","ur":"برتن"},
"mystery": {"el":"Μυστήρια","ru":"таинства","ro":"taine","uk":"таїнства","de":"Mysterien","es":"misterios","ar":"الأسرار","fr":"mystères","pt":"mistérios","it":"misteri","sr":"тајне","ka":"საიდუმლონი","zh":"奥迹","ja":"機密","ko":"성사","sw":"siri takatifu","hy":"խորհուրդներ","arc":"ܐ̄ܪ̈ܵܙܹܐ","hi":"रहस्य","bn":"রহস্য","ur":"اسرار"},
"prayer": {"el":"Προσευχή","ru":"молитва","ro":"rugăciune","uk":"молитва","de":"Gebet","es":"oración","ar":"الصلاة","fr":"prière","pt":"oração","it":"preghiera","sr":"молитва","ka":"ლოცვა","zh":"祈祷","ja":"祈り","ko":"기도","sw":"sala","hy":"աղոթք","arc":"ܨܠܘܿܬܵܐ","hi":"प्रार्थना","bn":"প্রার্থনা","ur":"دعا"},
"architecture": {"el":"Ναοδομία","ru":"устройство храма","ro":"arhitectură","uk":"будова храму","de":"Kirchenbau","es":"arquitectura","ar":"عمارة الكنيسة","fr":"architecture","pt":"arquitectura","it":"architettura","sr":"градња храма","ka":"ტაძრის მოწყობა","zh":"堂宇","ja":"聖堂","ko":"성당 구조","sw":"ujenzi wa kanisa","hy":"եկեղեցաշինություն","arc":"ܒܸܢܝܵܢ ܥܹܕܬܵܐ","hi":"मंदिर-रचना","bn":"মন্দিরের গঠন","ur":"کلیسیائی تعمیر"},
"clergy": {"el":"Κλήρος","ru":"клир","ro":"cler","uk":"клір","de":"Klerus","es":"clero","ar":"الإكليروس","fr":"clergé","pt":"clero","it":"clero","sr":"клир","ka":"სამღვდელოება","zh":"圣职","ja":"聖職","ko":"성직","sw":"makasisi","hy":"հոգևորականություն","arc":"ܟܵܗܢܘܼܬܵܐ","hi":"याजकवर्ग","bn":"যাজকবর্গ","ur":"کاہن"},
"theology": {"el":"Θεολογία","ru":"богословие","ro":"teologie","uk":"богослов'я","de":"Theologie","es":"teología","ar":"اللاهوت","fr":"théologie","pt":"teologia","it":"teologia","sr":"богословље","ka":"ღვთისმეტყველება","zh":"神学","ja":"神学","ko":"신학","sw":"theolojia","hy":"աստվածաբանություն","arc":"ܬܹܐܘܿܠܘܿܓ݂ܝܼܵܐ","hi":"धर्मविज्ञान","bn":"ধর্মতত্ত্ব","ur":"الٰہیات"},
"lent": {"el":"Μεγάλη Τεσσαρακοστή","ru":"Великий пост","ro":"Postul Mare","uk":"Великий піст","de":"Grosse Fastenzeit","es":"Gran Cuaresma","ar":"الصوم الكبير","fr":"Grand Carême","pt":"Grande Quaresma","it":"Grande Quaresima","sr":"Велики пост","ka":"დიდი მარხვა","zh":"大斋","ja":"大斎","ko":"대재","sw":"Kwaresima Kuu","hy":"Մեծ Պահք","arc":"ܨܵܘܡܵܐ ܪܲܒܵܐ","hi":"महान उपवास","bn":"মহা উপবাস","ur":"بڑا روزہ"},
"fast": {"el":"Νηστεία","ru":"пост","ro":"post","uk":"піст","de":"Fasten","es":"ayuno","ar":"الصوم","fr":"jeûne","pt":"jejum","it":"digiuno","sr":"пост","ka":"მარხვა","zh":"斋期","ja":"斎","ko":"재계","sw":"mfungo","hy":"պահք","arc":"ܨܵܘܡܵܐ","hi":"उपवास","bn":"উপবাস","ur":"روزہ"},
"theotokos": {"el":"Θεοτόκος","ru":"Богородица","ro":"Născătoarea de Dumnezeu","uk":"Богородиця","de":"Gottesmutter","es":"Theotokos","ar":"والدة الإله","fr":"Théotokos","pt":"Theotokos","it":"Theotokos","sr":"Богородица","ka":"ღვთისმშობელი","zh":"圣母","ja":"生神女","ko":"성모","sw":"Mzazi-Mungu","hy":"Աստվածածին","arc":"ܝܵܠܕܲܬ ܐܲܠܵܗܵܐ","hi":"थियोतोकोस","bn":"থিওতোকোস","ur":"والدہ خدا"},
"feast": {"el":"Εορτές","ru":"праздники","ro":"praznice","uk":"свята","de":"Feste","es":"fiestas","ar":"الأعياد","fr":"fêtes","pt":"festas","it":"feste","sr":"празници","ka":"დღესასწაულები","zh":"节期","ja":"祭","ko":"축일","sw":"sikukuu","hy":"տոներ","arc":"ܥܹܐܕܹ̈ܐ","hi":"पर्व","bn":"পর্ব","ur":"عیدیں"},
"canon-law": {"el":"Κανονικό δίκαιο","ru":"каноническое право","ro":"drept canonic","uk":"канонічне право","de":"Kirchenrecht","es":"derecho canónico","ar":"القوانين الكنسية","fr":"droit canonique","pt":"direito canónico","it":"diritto canonico","sr":"канонско право","ka":"საეკლესიო სამართალი","zh":"教规","ja":"教会法","ko":"교회법","sw":"sheria za Kanisa","hy":"կանոնական իրավունք","arc":"ܢܵܡܘܿܣܵܐ ܥܹܕܬܵܢܵܝܵܐ","hi":"कलीसियाई विधि","bn":"মণ্ডলীয় বিধি","ur":"کلیسیائی قانون"},
"departed": {"el":"Κεκοιμημένοι","ru":"усопшие","ro":"cei adormiți","uk":"спочилі","de":"Entschlafene","es":"difuntos","ar":"الراقدون","fr":"défunts","pt":"falecidos","it":"defunti","sr":"упокојени","ka":"გარდაცვლილნი","zh":"亡者","ja":"永眠者","ko":"잠든 이들","sw":"waliolala","hy":"ննջեցյալներ","arc":"ܥܲܢܝܼܕܹ̈ܐ","hi":"दिवंगत","bn":"প্রয়াতগণ","ur":"مرحومین"},
"repentance": {"el":"Μετάνοια","ru":"покаяние","ro":"pocăință","uk":"покаяння","de":"Busse","es":"arrepentimiento","ar":"التوبة","fr":"repentir","pt":"arrependimento","it":"pentimento","sr":"покајање","ka":"სინანული","zh":"痛悔","ja":"痛悔","ko":"회개","sw":"toba","hy":"ապաշխարություն","arc":"ܬܝܵܒ݂ܘܼܬܵܐ","hi":"पश्चात्ताप","bn":"অনুতাপ","ur":"توبہ"},
"saints": {"el":"Άγιοι","ru":"святые","ro":"sfinți","uk":"святі","de":"Heilige","es":"santos","ar":"القديسون","fr":"saints","pt":"santos","it":"santi","sr":"свети","ka":"წმინდანები","zh":"圣人","ja":"聖人","ko":"성인","sw":"watakatifu","hy":"սուրբեր","arc":"ܩܲܕܝܼܫܹ̈ܐ","hi":"संत","bn":"সাধুগণ","ur":"مقدسین"},
"scripture": {"el":"Αγία Γραφή","ru":"Писание","ro":"Scriptura","uk":"Писання","de":"Schrift","es":"Escritura","ar":"الكتاب المقدس","fr":"Écriture","pt":"Escritura","it":"Scrittura","sr":"Писмо","ka":"წერილი","zh":"圣经","ja":"聖書","ko":"성경","sw":"Maandiko","hy":"Սուրբ Գիրք","arc":"ܟܬܵܒܹ̈ܐ ܩܲܕܝܼܫܹ̈ܐ","hi":"पवित्र शास्त्र","bn":"শাস্ত্র","ur":"صحیفے"},
"bread": {"el":"Άρτος","ru":"хлеб","ro":"pâine","uk":"хліб","de":"Brot","es":"pan","ar":"الخبز","fr":"pain","pt":"pão","it":"pane","sr":"хлеб","ka":"პური","zh":"饼","ja":"パン","ko":"빵","sw":"mkate","hy":"հաց","arc":"ܠܲܚܡܵܐ","hi":"रोटी","bn":"রুটি","ur":"روٹی"},
"church-order": {"el":"Εκκλησιαστική τάξη","ru":"церковное устройство","ro":"rânduiala Bisericii","uk":"церковний устрій","de":"Kirchenordnung","es":"orden eclesiástico","ar":"النظام الكنسي","fr":"ordre ecclésial","pt":"ordem eclesial","it":"ordinamento ecclesiale","sr":"црквено уређење","ka":"საეკლესიო წყობა","zh":"教会体制","ja":"教会制度","ko":"교회 제도","sw":"utaratibu wa Kanisa","hy":"եկեղեցական կարգ","arc":"ܛܘܼܟܵܣܵܐ ܥܹܕܬܵܢܵܝܵܐ","hi":"कलीसियाई व्यवस्था","bn":"মণ্ডলীয় ব্যবস্থা","ur":"کلیسیائی نظام"},
"hours": {"el":"Ώρες","ru":"часы","ro":"ceasuri","uk":"часи","de":"Horen","es":"horas","ar":"الساعات","fr":"heures","pt":"horas","it":"ore","sr":"часови","ka":"ჟამნი","zh":"时课","ja":"時課","ko":"시과","sw":"saa za sala","hy":"ժամեր","arc":"ܫܵܥܹ̈ܐ","hi":"होरा","bn":"হোরা","ur":"ساعات"},
"icon": {"el":"Εικόνες","ru":"иконы","ro":"icoane","uk":"ікони","de":"Ikonen","es":"iconos","ar":"الأيقونات","fr":"icônes","pt":"ícones","it":"icone","sr":"иконе","ka":"ხატები","zh":"圣像","ja":"聖像","ko":"성화","sw":"ikoni","hy":"սրբապատկերներ","arc":"ܝܘܼܩܢܹ̈ܐ","hi":"प्रतिमा","bn":"প্রতিমা","ur":"شبیہیں"},
"music": {"el":"Μουσική","ru":"пение","ro":"muzică","uk":"спів","de":"Kirchengesang","es":"canto","ar":"الترتيل","fr":"chant","pt":"canto","it":"canto","sr":"појање","ka":"გალობა","zh":"圣咏","ja":"聖歌","ko":"성가","sw":"uimbaji","hy":"երգեցողություն","arc":"ܙܡܵܪܵܐ","hi":"संगीत","bn":"সংগীত","ur":"نغمہ"},
"pastoral": {"el":"Ποιμαντικά","ru":"пастырство","ro":"pastorație","uk":"пастирство","de":"Seelsorge","es":"pastoral","ar":"الرعاية","fr":"pastorale","pt":"pastoral","it":"pastorale","sr":"пастирство","ka":"მწყემსობა","zh":"牧养","ja":"牧会","ko":"목회","sw":"uchungaji","hy":"հովվություն","arc":"ܪܵܥܝܘܼܬܵܐ","hi":"पालकीय","bn":"পালকীয়","ur":"رعایت"},
"confession": {"el":"Εξομολόγηση","ru":"исповедь","ro":"spovedanie","uk":"сповідь","de":"Beichte","es":"confesión","ar":"الاعتراف","fr":"confession","pt":"confissão","it":"confessione","sr":"исповест","ka":"აღსარება","zh":"告解","ja":"告解","ko":"고해","sw":"kitubio","hy":"խոստովանություն","arc":"ܬܵܘܕܝܼܬܵܐ","hi":"पापस्वीकार","bn":"পাপস্বীকার","ur":"اعترافِ گناہ"},
"contested": {"el":"Αμφισβητούμενα","ru":"спорное","ro":"controversat","uk":"спірне","de":"umstritten","es":"discutido","ar":"موضع خلاف","fr":"controversé","pt":"controverso","it":"controverso","sr":"спорно","ka":"სადავო","zh":"有争议","ja":"議論のあるもの","ko":"논쟁되는 것","sw":"lenye mjadala","hy":"վիճելի","arc":"ܡܸܬܚܪܹܐ","hi":"विवादित","bn":"বিতর্কিত","ur":"متنازع"},
"council": {"el":"Σύνοδοι","ru":"соборы","ro":"sinoade","uk":"собори","de":"Konzilien","es":"concilios","ar":"المجامع","fr":"conciles","pt":"concílios","it":"concili","sr":"сабори","ka":"კრებები","zh":"公会议","ja":"公会議","ko":"공의회","sw":"mitaguso","hy":"ժողովներ","arc":"ܣܘܼܢܗܵܕܘܿܣ","hi":"महासभा","bn":"মহাসভা","ur":"مجالس"},
"eschatology": {"el":"Έσχατα","ru":"эсхатология","ro":"eshatologie","uk":"есхатологія","de":"Eschatologie","es":"escatología","ar":"الأمور الأخيرة","fr":"eschatologie","pt":"escatologia","it":"escatologia","sr":"есхатологија","ka":"ესქატოლოგია","zh":"末世论","ja":"終末論","ko":"종말론","sw":"mambo ya mwisho","hy":"վախճանաբանություն","arc":"ܚܲܪ̈ܵܝܵܬܵܐ","hi":"अंतिम बातें","bn":"শেষকাল","ur":"آخری باتیں"},
"food": {"el":"Τροφή","ru":"пища","ro":"hrană","uk":"їжа","de":"Speise","es":"alimento","ar":"الطعام","fr":"nourriture","pt":"alimento","it":"cibo","sr":"храна","ka":"საზრდო","zh":"食物","ja":"食物","ko":"음식","sw":"chakula","hy":"կերակուր","arc":"ܡܹܐܟ݂ܘܼܠܬܵܐ","hi":"आहार","bn":"খাদ্য","ur":"خوراک"},
"heresy": {"el":"Αιρέσεις","ru":"ереси","ro":"erezii","uk":"єресі","de":"Häresien","es":"herejías","ar":"البدع","fr":"hérésies","pt":"heresias","it":"eresie","sr":"јереси","ka":"ერესები","zh":"异端","ja":"異端","ko":"이단","sw":"uzushi","hy":"հերձվածներ","arc":"ܗܹܪܹܣܝܼܣ","hi":"विधर्म","bn":"বিধর্ম","ur":"بدعت"},
}
