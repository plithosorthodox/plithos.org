# -*- coding: utf-8 -*-
"""What each language calls the books of the Bible.

The buttons that carry a reader from one book to the next are the site
speaking, not the edition, so they are labelled in the language the site is
set to. That needs a name for every book in every language offered here, and
three things were missing:

  Church Slavonic, Japanese and Serbian had every Old Testament book named in
  English, over text that is not English. A Slavonic reader was given Genesis,
  Exodus, Leviticus above the Elizabeth Bible.

  Sixteen deuterocanonical books are carried by five editions - Slavonic,
  Greek, English, Romanian, Russian - and named in almost no other language,
  so a reader of any of the other eighteen who opened one of those editions
  was given Tobit and Judith and the Maccabees in English.

  Church Slavonic and Georgian had no New Testament book names at all.

Where a name is set by the edition the language reads, it is taken from the
edition and is in scripture/index.json already; this table does not touch it.
What is here is the rest: the received name in that language's own Church
where there is one, and its Bible-society usage where there is not.

The Esdras books are numbered differently by every tradition and the numbering
is not a detail. The site's slot 67 holds what the Greek prints as Esdras A,
the Slavonic and Russian as the second book of Ezra, the Latin West as 3
Esdras, and the 1914 Romanian as 3 Esdra. Slot 68 holds what the Russian
prints as the third book of Ezra and the West as 4 Esdras. Each language is
given the name its own Bible uses, which is why they do not agree, and the
Russian entry corrects the site's own labels: they read "1-я Ездры" and
"2-я Ездры" against a Synodal Bible that heads them Вторая and Третья, and
the text under them is the Synodal's, as its opening line says.
"""

# lang -> {book number: name}, for languages whose Old Testament names were
# never translated at all.
FULL_OT = {
    # The Elizabeth Bible of 1751, in the civil orthography the text is set
    # in here - the site's Slavonic is not printed with the old letters, so
    # its book names are not either.
    "cu": {
        1: "Бытие", 2: "Исход", 3: "Левит", 4: "Числа", 5: "Второзаконие",
        6: "Иисус Навин", 7: "Судии", 8: "Руфь",
        9: "1-я Царств", 10: "2-я Царств", 11: "3-я Царств", 12: "4-я Царств",
        13: "1-я Паралипоменон", 14: "2-я Паралипоменон",
        15: "1-я Ездры", 16: "Неемия", 17: "Есфирь", 18: "Иов",
        19: "Псалтирь", 20: "Притчи Соломона", 21: "Екклесиаст",
        22: "Песнь песней", 23: "Исаия", 24: "Иеремия",
        25: "Плач Иеремиев", 26: "Иезекииль", 27: "Даниил",
        28: "Осия", 29: "Иоиль", 30: "Амос", 31: "Авдий", 32: "Иона",
        33: "Михей", 34: "Наум", 35: "Аввакум", 36: "Софония",
        37: "Аггей", 38: "Захария", 39: "Малахия",
    },
    # Kougo-yaku, which is the edition the Japanese Old Testament here is set
    # from, and whose titles are the ones a Japanese reader knows.
    "ja": {
        1: "創世記", 2: "出エジプト記", 3: "レビ記", 4: "民数記", 5: "申命記",
        6: "ヨシュア記", 7: "士師記", 8: "ルツ記",
        9: "サムエル記上", 10: "サムエル記下", 11: "列王記上", 12: "列王記下",
        13: "歴代誌上", 14: "歴代誌下", 15: "エズラ記", 16: "ネヘミヤ記",
        17: "エステル記", 18: "ヨブ記", 19: "詩篇", 20: "箴言",
        21: "伝道の書", 22: "雅歌", 23: "イザヤ書", 24: "エレミヤ書",
        25: "哀歌", 26: "エゼキエル書", 27: "ダニエル書", 28: "ホセア書",
        29: "ヨエル書", 30: "アモス書", 31: "オバデヤ書", 32: "ヨナ書",
        33: "ミカ書", 34: "ナホム書", 35: "ハバクク書", 36: "ゼパニヤ書",
        37: "ハガイ書", 38: "ゼカリヤ書", 39: "マラキ書",
    },
    # Serbian, in the Cyrillic and the Ekavian the site's Serbian is written
    # in. Danicic heads his books at length - "Prva knjiga Mojsijeva" - and
    # that is his title page, not a label to put on a button; these are the
    # short forms the Serbian Church uses for the same books.
    "sr": {
        1: "Постање", 2: "Излазак", 3: "Левитска", 4: "Бројеви",
        5: "Поновљени закон", 6: "Исус Навин", 7: "Судије", 8: "Рута",
        9: "1. Самуилова", 10: "2. Самуилова",
        11: "1. о царевима", 12: "2. о царевима",
        13: "1. дневника", 14: "2. дневника",
        15: "Јездра", 16: "Немија", 17: "Јестира", 18: "Јов",
        19: "Псалми", 20: "Приче Соломонове", 21: "Проповедник",
        22: "Песма над песмама", 23: "Исаија", 24: "Јеремија",
        25: "Плач Јеремијин", 26: "Језекиљ", 27: "Данило",
        28: "Осија", 29: "Јоил", 30: "Амос", 31: "Авдија", 32: "Јона",
        33: "Михеј", 34: "Наум", 35: "Авакум", 36: "Софонија",
        37: "Агеј", 38: "Захарија", 39: "Малахија",
    },
    # Armenian has no Old Testament here at all, so every name is wanting.
    # These are the Zohrab Bible's, which is the Armenian Church's own.
    "hy": {
        1: "Ծննդոց", 2: "Ելք", 3: "Ղեւտական", 4: "Թուոց",
        5: "Երկրորդ Օրինաց", 6: "Յեսու", 7: "Դատաւորաց", 8: "Հռութ",
        9: "Ա Թագաւորաց", 10: "Բ Թագաւորաց", 11: "Գ Թագաւորաց",
        12: "Դ Թագաւորաց", 13: "Ա Մնացորդաց", 14: "Բ Մնացորդաց",
        15: "Եզրաս", 16: "Նէեմի", 17: "Եսթեր", 18: "Յոբ",
        19: "Սաղմոս", 20: "Առակաց", 21: "Ժողովող", 22: "Երգ Երգոց",
        23: "Եսայի", 24: "Երեմիա", 25: "Ողբք Երեմիայի", 26: "Եզեկիէլ",
        27: "Դանիէլ", 28: "Ովսէէ", 29: "Յովէլ", 30: "Ամովս",
        31: "Աբդիու", 32: "Յովնան", 33: "Միքիա", 34: "Նաւում",
        35: "Ամբակում", 36: "Սոփոնիա", 37: "Անգէ", 38: "Զաքարիա",
        39: "Մաղաքիա",
    },
    # Syriac has no Old Testament here either. These are the Peshitta's own
    # titles.
    "arc": {
        1: "ܒܪܝܬܐ", 2: "ܡܦܩܢܐ", 3: "ܟܗܢܐ", 4: "ܡܢܝܢܐ",
        5: "ܬܢܝܢ ܢܡܘܣܐ", 6: "ܝܫܘܥ ܒܪܢܘܢ", 7: "ܕܝ̈ܢܐ", 8: "ܪܥܘܬ",
        9: "ܫܡܘܐܝܠ ܩܕܡܝܐ", 10: "ܫܡܘܐܝܠ ܬܪܝܢܐ",
        11: "ܡܠܟ̈ܐ ܩܕܡܝܐ", 12: "ܡܠܟ̈ܐ ܬܪܝܢܐ",
        13: "ܕܒܪܝܡܝܢ ܩܕܡܝܐ", 14: "ܕܒܪܝܡܝܢ ܬܪܝܢܐ",
        15: "ܥܙܪܐ", 16: "ܢܚܡܝܐ", 17: "ܐܣܬܝܪ", 18: "ܐܝܘܒ",
        19: "ܡܙܡܘܪ̈ܐ", 20: "ܡܬ̈ܠܐ", 21: "ܩܘܗܠܬ",
        22: "ܬܫܒܚܬ ܬܫܒܚ̈ܬܐ", 23: "ܐܫܥܝܐ", 24: "ܐܪܡܝܐ",
        25: "ܐܘܠܝ̈ܬܐ ܕܐܪܡܝܐ", 26: "ܚܙܩܝܐܝܠ", 27: "ܕܢܝܐܝܠ",
        28: "ܗܘܫܥ", 29: "ܝܘܐܝܠ", 30: "ܥܡܘܣ", 31: "ܥܘܒܕܝܐ",
        32: "ܝܘܢܢ", 33: "ܡܝܟܐ", 34: "ܢܚܘܡ", 35: "ܚܒܩܘܩ",
        36: "ܨܦܢܝܐ", 37: "ܚܓܝ", 38: "ܙܟܪܝܐ", 39: "ܡܠܐܟܝ",
    },
}


# The sixteen books beyond the Hebrew canon, in every language offered here.
# Five editions carry them - Slavonic, Greek, English, Romanian, Russian - and
# a reader of any other language who opens one of those five was given them in
# English.
#
# Each language keeps its own numbering of the books of Ezra, because each
# tradition numbers them differently and a reader knows his own: the Greek
# prints Esdras A where the German prints 3. Esra and the Romanian 3 Esdra.
DEUTERO = {
    "en": {68: "2 Esdras", 84: "Song of the Three Youths"},
    "el": {68: "Έσδρας Δ'", 79: "Προσευχή Μανασσή",
           84: "Ύμνος των Τριών Παίδων"},
    "ro": {68: "4 Esdra", 83: "4 Macavei"},
    # The Russian entry corrects as well as fills. The site read "1-я Ездры"
    # and "2-я Ездры" over a Synodal Bible that heads those books Вторая and
    # Третья, and the text under the second says so in its own first line:
    # "Вторая книга Ездры пророка, сына Сераии". Ezra itself takes back the
    # number the Synodal gives it.
    "ru": {15: "1-я Ездры", 67: "2-я Ездры", 68: "3-я Ездры",
           76: "Послание Иеремии", 77: "Сусанна", 78: "Вил и дракон",
           83: "4-я Маккавейская", 84: "Песнь трёх отроков"},
    "cu": {67: "2-я Ездры", 68: "3-я Ездры", 69: "Товит", 70: "Иудифь",
           73: "Премудрость Соломона",
           74: "Премудрость Иисуса сына Сирахова", 75: "Варух",
           76: "Послание Иеремиино", 77: "Сусанна", 78: "Вил и дракон",
           79: "Молитва Манассиина", 80: "1-я Маккавейская",
           81: "2-я Маккавейская", 82: "3-я Маккавейская",
           83: "4-я Маккавейская", 84: "Песнь трёх отроков"},
    "ar": {67: "عزرا الأول", 68: "عزرا الثاني", 69: "طوبيا", 70: "يهوديت",
           73: "حكمة سليمان", 74: "يشوع بن سيراخ", 75: "باروخ",
           76: "رسالة إرميا", 77: "سوسنة", 78: "بيل والتنين",
           79: "صلاة منسّى", 80: "المكابيين الأول", 81: "المكابيين الثاني",
           82: "المكابيين الثالث", 83: "المكابيين الرابع",
           84: "نشيد الفتية الثلاثة"},
    "bn": {67: "প্রথম ইষ্রা", 68: "দ্বিতীয় ইষ্রা", 69: "তোবিত", 70: "যুদিত",
           73: "প্রজ্ঞাপুস্তক", 74: "সিরাক", 75: "বারূক",
           76: "যিরমিয়ের পত্র", 77: "সুশন্না", 78: "বেল ও নাগ",
           79: "মনঃশির প্রার্থনা", 80: "প্রথম মক্কাবি", 81: "দ্বিতীয় মক্কাবি",
           82: "তৃতীয় মক্কাবি", 83: "চতুর্থ মক্কাবি",
           84: "তিন যুবকের স্তোত্র"},
    "de": {67: "3. Esra", 68: "4. Esra", 69: "Tobit", 70: "Judit",
           73: "Weisheit", 74: "Jesus Sirach", 75: "Baruch",
           76: "Brief des Jeremia", 77: "Susanna", 78: "Bel und der Drache",
           79: "Gebet des Manasse", 80: "1. Makkabäer", 81: "2. Makkabäer",
           82: "3. Makkabäer", 83: "4. Makkabäer",
           84: "Gesang der drei Männer im Feuerofen"},
    "es": {67: "1 Esdras", 68: "2 Esdras", 69: "Tobías", 70: "Judit",
           73: "Sabiduría", 74: "Eclesiástico", 75: "Baruc",
           76: "Carta de Jeremías", 77: "Susana", 78: "Bel y el dragón",
           79: "Oración de Manasés", 80: "1 Macabeos", 81: "2 Macabeos",
           82: "3 Macabeos", 83: "4 Macabeos",
           84: "Cántico de los tres jóvenes"},
    "fr": {67: "1 Esdras", 68: "2 Esdras", 69: "Tobie", 70: "Judith",
           73: "Sagesse", 74: "Siracide", 75: "Baruch",
           76: "Lettre de Jérémie", 77: "Suzanne", 78: "Bel et le dragon",
           79: "Prière de Manassé", 80: "1 Maccabées", 81: "2 Maccabées",
           82: "3 Maccabées", 83: "4 Maccabées",
           84: "Cantique des trois jeunes gens"},
    "hi": {67: "पहला एज़्रा", 68: "दूसरा एज़्रा", 69: "तोबित", 70: "यूदीत",
           73: "सुलैमान की बुद्धि", 74: "सिराख", 75: "बारूक",
           76: "यिर्मयाह का पत्र", 77: "सुज़ैना", 78: "बेल और अजगर",
           79: "मनश्शे की प्रार्थना", 80: "पहला मक्काबी",
           81: "दूसरा मक्काबी", 82: "तीसरा मक्काबी", 83: "चौथा मक्काबी",
           84: "तीन युवकों का गीत"},
    "it": {67: "1 Esdra", 68: "2 Esdra", 69: "Tobia", 70: "Giuditta",
           73: "Sapienza", 74: "Siracide", 75: "Baruc",
           76: "Lettera di Geremia", 77: "Susanna", 78: "Bel e il drago",
           79: "Preghiera di Manasse", 80: "1 Maccabei", 81: "2 Maccabei",
           82: "3 Maccabei", 83: "4 Maccabei",
           84: "Cantico dei tre giovani"},
    "ja": {67: "エズラ記（ギリシア語）", 68: "エズラ記（ラテン語）",
           69: "トビト記", 70: "ユディト記", 73: "知恵の書", 74: "シラ書",
           75: "バルク書", 76: "エレミヤの手紙", 77: "スザンナ",
           78: "ベルと竜", 79: "マナセの祈り", 80: "マカバイ記一",
           81: "マカバイ記二", 82: "マカバイ記三", 83: "マカバイ記四",
           84: "三人の若者の賛歌"},
    # Susanna is სუსანა. She is not შუშანიკი, who is the Georgian queen and
    # martyr and a different person entirely, and the two are easy to confuse
    # in Georgian precisely because the names are cognate.
    "ka": {67: "პირველი ეზრა", 68: "მეორე ეზრა", 69: "ტობითი",
           70: "ივდითი", 73: "სიბრძნე სოლომონისა", 74: "ზირაქი",
           75: "ბარუქი", 76: "ეპისტოლე იერემიასი", 77: "სუსანა",
           78: "ბელი და ვეშაპი", 79: "მანასეს ლოცვა",
           80: "პირველი მაკაბელთა", 81: "მეორე მაკაბელთა",
           82: "მესამე მაკაბელთა", 83: "მეოთხე მაკაბელთა",
           84: "სამთა ყრმათა გალობა"},
    "ko": {67: "에스드라 1서", 68: "에스드라 2서", 69: "토빗기",
           70: "유딧기", 73: "지혜서", 74: "집회서", 75: "바룩서",
           76: "예레미야의 편지", 77: "수산나", 78: "벨과 용",
           79: "므나쎄의 기도", 80: "마카베오기 상", 81: "마카베오기 하",
           82: "마카베오기 3서", 83: "마카베오기 4서",
           84: "세 젊은이의 노래"},
    "pt": {67: "1 Esdras", 68: "2 Esdras", 69: "Tobias", 70: "Judite",
           73: "Sabedoria", 74: "Eclesiástico", 75: "Baruc",
           76: "Carta de Jeremias", 77: "Susana", 78: "Bel e o dragão",
           79: "Oração de Manassés", 80: "1 Macabeus", 81: "2 Macabeus",
           82: "3 Macabeus", 83: "4 Macabeus",
           84: "Cântico dos três jovens"},
    "sr": {67: "2. Јездрина", 68: "3. Јездрина", 69: "Товит", 70: "Јудита",
           73: "Премудрости Соломонове",
           74: "Књига Исуса сина Сирахова", 75: "Варух",
           76: "Посланица Јеремијина", 77: "Сусана", 78: "Вил и аждаја",
           79: "Молитва Манасијина", 80: "1. Макавејска",
           81: "2. Макавејска", 82: "3. Макавејска", 83: "4. Макавејска",
           84: "Песма три младића"},
    "sw": {67: "Ezra wa Kwanza", 68: "Ezra wa Pili", 69: "Tobiti",
           70: "Yudithi", 73: "Hekima ya Solomoni", 74: "Yoshua bin Sira",
           75: "Baruku", 76: "Barua ya Yeremia", 77: "Susana",
           78: "Beli na Joka", 79: "Sala ya Manase", 80: "1 Wamakabayo",
           81: "2 Wamakabayo", 82: "3 Wamakabayo", 83: "4 Wamakabayo",
           84: "Wimbo wa Vijana Watatu"},
    "uk": {67: "2-а Ездри", 68: "3-я Ездри", 69: "Товит", 70: "Юдит",
           73: "Премудрості Соломона", 74: "Сирах", 75: "Барух",
           76: "Послання Єремії", 77: "Сусанна", 78: "Бел і дракон",
           79: "Молитва Манасії", 80: "1-а Макавеїв", 81: "2-а Макавеїв",
           82: "3-я Макавеїв", 83: "4-а Макавеїв",
           84: "Пісня трьох отроків"},
    "ur": {67: "پہلا عزرا", 68: "دوسرا عزرا", 69: "طوبیاہ", 70: "یہودیتھ",
           73: "حکمت سلیمان", 74: "یشوع بن سیراخ", 75: "باروک",
           76: "یرمیاہ کا خط", 77: "سوسنہ", 78: "بیل اور اژدہا",
           79: "منسّی کی دعا", 80: "پہلا مکابیوں", 81: "دوسرا مکابیوں",
           82: "تیسرا مکابیوں", 83: "چوتھا مکابیوں",
           84: "تین جوانوں کا گیت"},
    "zh": {67: "以斯拉续篇上卷", 68: "以斯拉续篇下卷", 69: "多比传",
           70: "犹滴传", 73: "所罗门智训", 74: "便西拉智训", 75: "巴录书",
           76: "耶利米书信", 77: "苏撒拿传", 78: "比勒与大龙",
           79: "玛拿西祷言", 80: "马加比一书", 81: "马加比二书",
           82: "马加比三书", 83: "马加比四书", 84: "三童歌"},
    "hy": {67: "Ա Եզրաս", 68: "Բ Եզրաս", 69: "Տուբիթ", 70: "Յուդիթ",
           73: "Իմաստութիւն Սողոմոնի", 74: "Սիրաք", 75: "Բարուք",
           76: "Թուղթ Երեմիայի", 77: "Շուշան", 78: "Բէլ եւ Վիշապ",
           79: "Աղօթք Մանասէի", 80: "Ա Մակաբայեցւոց",
           81: "Բ Մակաբայեցւոց", 82: "Գ Մակաբայեցւոց",
           83: "Դ Մակաբայեցւոց", 84: "Երգ Երից Մանկանց"},
    "arc": {67: "ܥܙܪܐ ܩܕܡܝܐ", 68: "ܥܙܪܐ ܬܪܝܢܐ", 69: "ܛܘܒܝܐ",
            70: "ܝܗܘܕܝܬ", 73: "ܚܟܡܬܐ ܕܫܠܝܡܘܢ", 74: "ܒܪ ܐܣܝܪܐ",
            75: "ܒܪܘܟ", 76: "ܐܓܪܬܐ ܕܐܪܡܝܐ", 77: "ܫܘܫܢ",
            78: "ܒܝܠ ܘܬܢܝܢܐ", 79: "ܨܠܘܬܐ ܕܡܢܫܐ", 80: "ܡܩܒܝ̈ܐ ܩܕܡܝܐ",
            81: "ܡܩܒܝ̈ܐ ܬܪܝܢܐ", 82: "ܡܩܒܝ̈ܐ ܬܠܝܬܝܐ",
            83: "ܡܩܒܝ̈ܐ ܪܒܝܥܝܐ", 84: "ܬܫܒܘܚܬܐ ܕܬܠܬܐ ܥܠܝ̈ܡܐ"},
}


# The New Testament, for the two languages that had no names for it at all.
# Church Slavonic has its own New Testament here and was being given English
# titles over it; Georgian has none of its own, so its reader meets another
# language's edition and should at least be told in Georgian which book he is
# opening.
NT = {
    "cu": {
        "Matthew": "От Матфеа", "Mark": "От Марка", "Luke": "От Луки",
        "John": "От Иоанна", "Acts": "Деяния святых апостол",
        "Romans": "К Римляном", "1 Corinthians": "1-е к Коринфяном",
        "2 Corinthians": "2-е к Коринфяном", "Galatians": "К Галатом",
        "Ephesians": "К Ефесеем", "Philippians": "К Филипписием",
        "Colossians": "К Колоссаем", "1 Thessalonians": "1-е к Солуняном",
        "2 Thessalonians": "2-е к Солуняном", "1 Timothy": "1-е к Тимофею",
        "2 Timothy": "2-е к Тимофею", "Titus": "К Титу",
        "Philemon": "К Филимону", "Hebrews": "К Евреом", "James": "Иакова",
        "1 Peter": "1-е Петрово", "2 Peter": "2-е Петрово",
        "1 John": "1-е Иоанново", "2 John": "2-е Иоанново",
        "3 John": "3-е Иоанново", "Jude": "Иудино",
        "Revelation": "Апокалипсис",
    },
    "ka": {
        "Matthew": "მათე", "Mark": "მარკოზი", "Luke": "ლუკა",
        "John": "იოანე", "Acts": "საქმე მოციქულთა",
        "Romans": "რომაელთა", "1 Corinthians": "I კორინთელთა",
        "2 Corinthians": "II კორინთელთა", "Galatians": "გალატელთა",
        "Ephesians": "ეფესელთა", "Philippians": "ფილიპელთა",
        "Colossians": "კოლასელთა", "1 Thessalonians": "I თესალონიკელთა",
        "2 Thessalonians": "II თესალონიკელთა", "1 Timothy": "I ტიმოთე",
        "2 Timothy": "II ტიმოთე", "Titus": "ტიტე",
        "Philemon": "ფილიმონი", "Hebrews": "ებრაელთა", "James": "იაკობი",
        "1 Peter": "I პეტრე", "2 Peter": "II პეტრე",
        "1 John": "I იოანე", "2 John": "II იოანე", "3 John": "III იოანე",
        "Jude": "იუდა", "Revelation": "გამოცხადება",
    },
}
