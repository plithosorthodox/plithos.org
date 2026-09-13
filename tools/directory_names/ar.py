# -*- coding: utf-8 -*-
"""الكنائس وكراسيها - the Churches and their seats, in Arabic.

The Antiochian register, as docs/ARABIC.md settles it. Nothing here was
rendered afresh: every see, country and city was read off the Arabic this
site already publishes - the place vocabulary beside the lives, the
calendar entries and the saints' names - so القسطنطينية, الإسكندرية,
أنطاكية, أورشليم, دمشق, موسكو, أثينا, وارسو, بوخارست, صوفيا and نيقوسيا
are the forms already printed, not new ones.

Five forms had to be settled by counting, because the site prints two:

  - **أورشليم**, not القدس: 279 against 229, and the place vocabulary
    renders Jerusalem as أورشليم.
  - **بولندة**, not بولندا: 8 against 3, and the place vocabulary writes
    بولندة.
  - **أوهريد**, not أوخريد: 6 against 5, and the place vocabulary writes
    أوهريد.
  - **تبليسي**, not تفليس: 8 against 2.
  - **جبل سيناء**, not طور سيناء: 5 against 1.

Two more were settled by reading the counts by sense rather than by total.
America stands at أميركا 114 against أمريكا 62 in general, but the body
named in this row is written الكنيسة الأرثوذكسية في أمريكا 51 times against
18, so that row keeps أمريكا and the rest of the site keeps أميركا. And
مكدونية, the commoner of the two Macedonias here at 23 against 19, is in
every instance the ancient province St Paul crossed; the modern country is
مقدونيا, which the vocabulary writes as مقدونيا الشمالية, so the Church of
this row is المقدونية.

The place vocabulary gives Belgrade as بيلوزيرسك, which is Belozersk; the
corpus writes بلغراد 23 times and that is what stands here.

What the Arabic pages have never had occasion to say is written here in the
received Arabic form. Seven cities: إسطنبول, تيرانا, بريشوف, سكوبيه, سيوسيت,
طوكيو and تالين. And three countries: سلوفاكيا, فنلندا and اليابان. Two of
those peoples the site does name - the lives write السلوفاك and الفنلنديين -
but never the countries, and Japan it has not named at all.

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Arabic this site publishes and are
taken whole - البطريركية المسكونية and the الكنيسة الأرثوذكسية الروسية,
الصربية, الرومانية and الأوكرانية of the commemorations.

Antioch and Jerusalem are the two rows where the English word Greek means the
Rum rite and communion and not the Greek nation, and Arabic has the received
form for it. This site already prints it: the thanksgiving prayer after the
reading is credited to رعية طرابلس للروم الأرثوذكس. So the two read
بطريركية أنطاكية وسائر المشرق للروم الأرثوذكس and
بطريركية أورشليم للروم الأرثوذكس, which is the Antiochian register the rest
of this site's Arabic is written in, and not a rendering of the English.

The thirty-nine dioceses came afterwards, and the words for what they are
were counted before anything was written. أبرشية stands 65 times against
مطرانية 6, so a diocese is an أبرشية. رئاسة أساقفة, already here for the
Ohrid Archbishopric, is what the lives call an archbishop's see and carries
the archdioceses; متروبوليتية, 18 times and always of a metropolitan's own
church - المتروبوليتية الروسية, متروبوليتية إزمير - carries the metropolises.
الأسقفية takes the Romanian Episcopate and الرعايا البطريركية the patriarchal
parishes, both words these pages already print, and بلدة, the word the life of
Saint Raphael uses for a mill town, takes Cranberry Township.

Arabic builds these titles as an idafa, so the row reads متروبوليتية النمسا
المقدسة and not a chain of lam prefixes after the English. Most of the
American places were already written here: أبرشية الأليوت وأميركا الشمالية
stands in the life of Saint Alexis, and with it ألاسكا, سيتكا, نيويورك,
بوسطن, شيكاغو, سان فرنسيسكو, كاليفورنيا, إلينوي, بنسلفانيا, باث, جاكسون,
كندا, المكسيك, الولايات المتحدة, باريس and البندقية. الغرب الأوسط is the
site's own phrase for the American Midwest, at 2 against nothing else, and
الجنوب and الغرب its words for the other two regions. The Alexandria of
Virginia takes الإسكندرية, which is the one Arabic form for the name.

The rest are small American towns and European and Asian capitals no saint
here is of, and the Arabic pages have never had occasion to name them. They
are written in the received Arabic form and are declared here rather than
passed off as gathered: لندن, مدريد, ستوكهولم, سيول, هونغ كونغ, بلجيكا,
إسكندنافيا, واشنطن, ماساتشوستس, تكساس, ميشيغان, نيوجيرسي, كيبيك, أستراليا,
شامبيزي, برونكسفيل, إنغلوود, سومرست, جونستاون, أنكوريج, نيو روشيل, ويندسور,
ثيرد ليك and غراتشانيتسا. Where two spellings of one of them are both in use
the commoner is taken - الهامبرا rather than ألهامبرا - since the corpus
settles neither.
"""
NAMES = {
    "constantinople": u"كنيسة القسطنطينية",
    "alexandria": u"كنيسة الإسكندرية",
    "antioch": u"كنيسة أنطاكية",
    "jerusalem": u"كنيسة أورشليم",
    "russia": u"كنيسة روسيا",
    "georgia": u"كنيسة جورجيا",
    "serbia": u"كنيسة صربيا",
    "romania": u"كنيسة رومانيا",
    "bulgaria": u"كنيسة بلغاريا",
    "cyprus": u"كنيسة قبرص",
    "greece": u"كنيسة اليونان",
    "albania": u"كنيسة ألبانيا",
    "poland": u"كنيسة بولندة",
    "czech-slovakia": u"كنيسة الأراضي التشيكية وسلوفاكيا",
    "oca": u"الكنيسة الأرثوذكسية في أمريكا",
    "macedonia": u"الكنيسة الأرثوذكسية المقدونية - رئاسة أساقفة أوهريد",
    "ukraine-uoc": u"كنيسة أوكرانيا",
    "ukraine-ocu": u"كنيسة أوكرانيا الأرثوذكسية",
    "sinai": u"كنيسة سيناء",
    "finland": u"كنيسة فنلندا ذات الحكم الذاتي",
    "japan": u"كنيسة اليابان",
    "estonia-eaok": u"كنيسة إستونيا الأرثوذكسية",
    "albanian-americas": u"الأبرشية الألبانية الأرثوذكسية لأميركا",
    "acrod": u"الأبرشية الأميركية الأرثوذكسية لروسيا الكاربات في أميركا الشمالية",
    "ep-thyateira": u"رئاسة أساقفة ثياتيرا وبريطانيا العظمى",
    "goarch": u"رئاسة أساقفة أميركا اليونانية الأرثوذكسية",
    "ep-france": u"متروبوليتية فرنسا اليونانية الأرثوذكسية",
    "ep-germany": u"متروبوليتية ألمانيا اليونانية الأرثوذكسية",
    "ep-austria": u"متروبوليتية النمسا المقدسة",
    "ep-korea": u"متروبوليتية كوريا المقدسة",
    "ep-spain": u"متروبوليتية إسبانيا والبرتغال المقدسة",
    "ep-belgium": u"متروبوليتية بلجيكا",
    "ep-sweden": u"متروبوليتية السويد وسائر إسكندنافيا",
    "ep-switzerland": u"متروبوليتية سويسرا",
    "ep-hongkong": u"متروبوليتية هونغ كونغ وجنوب شرق آسيا الأرثوذكسية",
    "ep-singapore": u"متروبوليتية سنغافورة وجنوب آسيا الأرثوذكسية",
    "ep-italy": u"رئاسة الأساقفة الأرثوذكسية المقدسة لإيطاليا ومالطة",
    "uocc": u"الكنيسة الأوكرانية الأرثوذكسية في كندا",
    "uoc-usa": u"الكنيسة الأوكرانية الأرثوذكسية في الولايات المتحدة",
    "antiochian-na": u"رئاسة الأساقفة الأنطاكية الأرثوذكسية المسيحية لأميركا الشمالية",
    "rocor": u"الكنيسة الروسية الأرثوذكسية خارج روسيا",
    "mp-parishes-usa": u"الرعايا البطريركية في الولايات المتحدة",
    "serbian-eastern": u"أبرشية أميركا الشرقية",
    "serbian-midwestern": u"أبرشية غراتشانيتسا الجديدة وأميركا الغرب الأوسط",
    "serbian-western": u"أبرشية أميركا الغربية",
    "romanian-americas": u"المتروبوليتية الرومانية الأرثوذكسية لأميركا",
    "bulgarian-usa": u"الأبرشية البلغارية الأرثوذكسية الشرقية للولايات المتحدة وكندا وأستراليا",
    "oca-albanian": u"رئاسة الأساقفة الألبانية",
    "oca-canada": u"رئاسة أساقفة كندا",
    "oca-washington": u"رئاسة أساقفة واشنطن العاصمة",
    "oca-western-pa": u"رئاسة أساقفة بنسلفانيا الغربية",
    "oca-bulgarian": u"الأبرشية البلغارية",
    "oca-eastern-pa": u"أبرشية بنسلفانيا الشرقية",
    "oca-mexico": u"أبرشية المكسيك",
    "oca-new-england": u"أبرشية نيو إنغلاند",
    "oca-ny-nj": u"أبرشية نيويورك ونيوجيرسي",
    "oca-alaska": u"أبرشية سيتكا وألاسكا",
    "oca-midwest": u"أبرشية الغرب الأوسط",
    "oca-south": u"أبرشية الجنوب",
    "oca-west": u"أبرشية الغرب",
    "oca-romanian": u"الأسقفية الرومانية",
}
SEATS = {
    "Istanbul": u"إسطنبول",
    "Alexandria": u"الإسكندرية",
    "Damascus": u"دمشق",
    "Jerusalem": u"أورشليم",
    "Moscow": u"موسكو",
    "Tbilisi": u"تبليسي",
    "Belgrade": u"بلغراد",
    "Bucharest": u"بوخارست",
    "Sofia": u"صوفيا",
    "Nicosia": u"نيقوسيا",
    "Athens": u"أثينا",
    "Tirana": u"تيرانا",
    "Warsaw": u"وارسو",
    "Prešov": u"بريشوف",
    "Syosset, New York": u"سيوسيت، نيويورك",
    "Skopje": u"سكوبيه",
    "Kyiv": u"كييف",
    "Mount Sinai": u"جبل سيناء",
    "Helsinki": u"هلسنكي",
    "Tokyo": u"طوكيو",
    "Tallinn": u"تالين",
    "Alexandria, Virginia": u"الإسكندرية، فرجينيا",
    "Alhambra, California": u"الهامبرا، كاليفورنيا",
    "Anchorage, Alaska": u"أنكوريج، ألاسكا",
    "Bath, Pennsylvania": u"باث، بنسلفانيا",
    "Bonn": u"بون",
    "Boston, Massachusetts": u"بوسطن، ماساتشوستس",
    "Bronxville, New York": u"برونكسفيل، نيويورك",
    "Brussels": u"بروكسل",
    "Chambesy": u"شامبيزي",
    "Chicago, Illinois": u"شيكاغو، إلينوي",
    "Cranberry Township, Pennsylvania": u"بلدة كرانبيري، بنسلفانيا",
    "Dallas, Texas": u"دالاس، تكساس",
    "Englewood, New Jersey": u"إنغلوود، نيوجيرسي",
    "Hong Kong": u"هونغ كونغ",
    "Jackson, Michigan": u"جاكسون، ميشيغان",
    "Johnstown, Pennsylvania": u"جونستاون، بنسلفانيا",
    "London": u"لندن",
    "Madrid": u"مدريد",
    "Mexico City": u"مدينة المكسيك",
    "New Rochelle, New York": u"نيو روشيل، نيويورك",
    "New York": u"نيويورك",
    "Paris": u"باريس",
    "Rawdon, Quebec": u"راودون، كيبيك",
    "San Francisco, California": u"سان فرنسيسكو، كاليفورنيا",
    "Seoul": u"سيول",
    "Singapore": u"سنغافورة",
    "Somerset, New Jersey": u"سومرست، نيوجيرسي",
    "Stockholm": u"ستوكهولم",
    "Third Lake, Illinois": u"ثيرد ليك، إلينوي",
    "Toledo, Ohio": u"توليدو، أوهايو",
    "Venice": u"البندقية",
    "Vienna": u"فيينا",
    "Windsor, Connecticut": u"ويندسور، كونيتيكت",
    "Winnipeg, Manitoba": u"وينيبيغ، مانيتوبا",
}
STYLED = {
    "constantinople": u"البطريركية المسكونية",
    "alexandria": u"بطريركية الإسكندرية",
    "antioch": u"بطريركية أنطاكية وسائر المشرق للروم الأرثوذكس",
    "jerusalem": u"بطريركية أورشليم للروم الأرثوذكس",
    "russia": u"الكنيسة الأرثوذكسية الروسية",
    "serbia": u"الكنيسة الأرثوذكسية الصربية",
    "romania": u"الكنيسة الأرثوذكسية الرومانية",
    "bulgaria": u"الكنيسة الأرثوذكسية البلغارية - البطريركية البلغارية",
    "ukraine-uoc": u"الكنيسة الأرثوذكسية الأوكرانية",
}
