# Arabic

The tenth language. Written, not converted: the test is whether a reader who
grew up in the Church of Antioch would recognise it as something written by
someone from his own Church.

Arabic is the first language here that is not written in a European script and
not read from the left. Both facts change what the register has to settle, and
neither changes the rule that settles it: the register is *read off* what the
Church already prints, and the site already carries a great deal of it. The
prayer book in `data/prayers-i18n.v2.ar.json`, the Scriptures under
`scripture/ar/`, and the interface strings on the calendar were written in
Arabic before a single saint was. Where they have decided a word, that word
stands and is not re-decided here.

## Script and spelling

Modern Standard Arabic in the Arabic script, unvocalised, as the Antiochian
books print running prose. Vowel marks are not written: not fatha, damma,
kasra, sukun, shadda, nor the tanwin. This is the ordinary practice of Arabic
prose and it is also enforced, because every one of those marks is a combining
character and `tools/loop.py` refuses combining marks in any language.

Hamza and madda are **letters**, not marks, and are written: أ إ آ ؤ ئ ء. So is
the ta marbuta ة, and the alif maqsura ى, and the shadda-less doubling is not a
licence to drop a letter. What must not appear is the bare Latin letter inside
an Arabic word, and the Persian and Urdu letters that Arabic does not use -
پ چ ژ گ ک ی ہ - which are the mark of a rendering pasted from a neighbouring
language rather than written.

Punctuation is Arabic: the comma **،** and the semicolon **؛** and the question
mark **؟**. The full stop is the ordinary one. Hyphens, never dashes. Straight
quotes, never the typographic ones - the guillemets «» that Arabic typography
sometimes takes are not used here, because the index quotes nothing.

Numerals are the European digits the rest of the site uses, not the Eastern
Arabic ones, so that a year reads the same in every language on the page.

## Register

Arabic, like Greek and Romanian, allows the plain honorific before a name.
**القديس نيقولاوس** is right, and so is **القديسة بربارة**. The prayer book
already writes القديس يوحنا الذهبي الفم and شكر القديس باسيليوس الكبير, and
those are the received forms.

So only the monastic distinction is asserted. A monastic is **البار** and a
woman monastic **البارة**, never merely القديس: the prayer book already writes
**البار مكاريوس**, and that is the pattern. The rest of the ranks the Church of
Antioch uses, from which the honorific is drawn rather than flattened into
القديس:

| | |
|---|---|
| hierarch, bishop | الأسقف, رئيس الأساقفة, المطران |
| patriarch | البطريرك |
| monastic | البار, البارة |
| hieromartyr | الشهيد في الكهنة |
| venerable-martyr | البار الشهيد |
| great-martyr | العظيم في الشهداء, العظيمة في الشهيدات |
| martyr | الشهيد, الشهيدة |
| new martyr | الشهيد الجديد, الشهيدة الجديدة |
| righteous | البار, الصديق |
| ruler, prince | الأمير المؤمن |
| confessor | المعترف |
| unmercenary | عديم الفضة |
| fool-for-Christ | المتباله بالمسيح |
| apostle | الرسول |
| apostle of the Seventy | الرسول من السبعين |
| prophet | النبي, النبية |
| stylite | العمودي |
| equal-to-the-apostles | المعادل للرسل |
| enlightener | منير |
| wonderworker | العجائبي, صانع العجائب |
| deacon | الشماس |
| archdeacon | رئيس الشمامسة |
| abbot | رئيس الدير |
| archimandrite | الأرشمندريت |
| nun | الراهبة |
| virgin | البتول |

The Mother of God is **والدة الإله**, and where the English says *Most Holy* she
is **والدة الإله الكلية القداسة**; *Ever-Virgin* is **الدائمة البتولية**. The
Liturgy is **القداس الإلهي**. All of these the prayer book has already fixed.

`tools/check_register.py --lang ar` will enforce the monastic distinction and
nothing else, once the vocabulary exists to scaffold it from.

## Order

Vocabulary, then grammar, then the lives and the calendar entries:

    python3 tools/loop.py terms ar --next 40
    python3 tools/check_register.py --scaffold --lang ar
    python3 tools/loop.py lives ar --next 6
    python3 tools/loop.py info ar --next 10

The scaffold reads the terms table and derives the rank patterns from it, so it
refuses to run before the vocabulary is there. See `docs/LOOP.md`.

## Names

Arabic has its own received forms for the saints of the first millennium and
does not transliterate them from English. **يوحنا** and not جون, **بطرس** and
not بيتر, **يعقوب**, **بولس**, **أندراوس**, **متى**, **مرقس**, **لوقا**,
**سمعان**, **إسحق**, **يوسف**, **إيليا**, **موسى**, **داود**. The Greek fathers
keep the Greek shape in its Arabic dress: **باسيليوس**, **غريغوريوس**,
**أثناسيوس**, **نيقولاوس**, **ديمتريوس**, **جاورجيوس**, **أنطونيوس**,
**أفرام**, **مكاريوس**, **أرسانيوس**, **سابا**. Where a name has a received
Arabic form, that form is used and is not re-rendered from the English spelling.

Names that have no received Arabic form - the Slavic, Georgian, Romanian and
Celtic saints, and the new martyrs of the last century - are transliterated on
the sound of the language they come from, not on the English spelling of it:
سرجيوس, فلاديمير, أولغا, نينا, ستيفان. A Russian name is not routed through
English on its way into Arabic.

## Places

A see or a town is given in its received Arabic form where the Church has one -
أنطاكية, الإسكندرية, أورشليم, القسطنطينية, تسالونيكي, أفسس, نيقية, خلقيدونية,
دمشق, حمص, صيدنايا - and transliterated where it has none. The epithet is a
prepositional phrase and not an adjective: **أسقف ميرا** and not a coined
nisba, except where Arabic has long had the nisba and uses it.

## The ten fields, and what each one is

The vocabulary is not one kind of phrase, and knowing which field a phrase came
from settles most of the questions about how to render it.

| field | count | what it is | how Arabic takes it |
|---|---|---|---|
| patronCauses | 3,021 | what is asked of him | a definite noun phrase: الفقراء والمرضى |
| patronWork | 2,483 | whom he is asked for | likewise, definite |
| related | 1,692 | the kindred commemoration | a name and its apposition |
| type | 1,456 | the badge on a card | a noun phrase, as a label |
| feastRank | 1,437 | the weight of the day | likewise |
| icon | 1,435 | how he is written in an icon | a full descriptive sentence |
| era | 1,400 | the century | القرن الرابع, and قبل الميلاد before Christ |
| canonizedBy | 1,363 | who glorified him and when | a clause |
| patronPlaces | 1,354 | the town a saint is patron of | the bare place name |
| place, origin, region | 3,496 | town, then the land it stood in | received form, comma as in the English |
| titles | 1,340 | how else the saint is named | أسقف أفسس, المعترف |
| rank, state | 2,608 | his order and his standing | a noun phrase |
| relics | 834 | where the relics rest | a full sentence, as the English is |
| baptismalName | 150 | the name before tonsure | the Arabic form of the name |

The two largest are the intercessions and the icons, and both are English of a
deliberately heightened kind. Arabic takes the intercessions as definite noun
phrases - *the poor and sick* is **الفقراء والمرضى** - and does not turn the
participial strings of the icon sentences into subordinate clauses, which is
the one change that would double the length of fourteen hundred sentences.
Arabic has the participle for exactly this: *holding the Gospel* is **حاملاً
الإنجيل**, and *crowned with* is **مكللاً بـ**.

## The word that must not creep in

The site is published by a Church, and the Arabic of a Church is not the Arabic
of a newspaper. Where Islamic religious vocabulary and Christian Arabic differ,
the Christian word is used: **الله** for God as the Christian Arabs have always
said it, **الرب** for the Lord, **الكنيسة** for the Church, **الأسرار المقدسة**
for the Mysteries, **القداس** for the Liturgy, **الصوم** for the Fast,
**الشهيد** for the martyr in the Church's sense. What is avoided is not a word
but a cadence: the formulas of another book, which a reader hears at once.
