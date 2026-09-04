# Urdu

The register for `tools/saint_terms/ur.py`, read off the Urdu this site has
already published rather than proposed from scratch. Four bodies were already
here when this began, all four complete, and between them they settle almost
every question the vocabulary raises:

| file | what it is | strings |
|---|---|---|
| `data/prayers-i18n.v2.ur.json` | 100 prayers, the liturgical register | 241 |
| `data/saint-names.v1.ur.json` | 1,528 commemorations, every rank word and the word order | 1,528 |
| `data/glossary-i18n.v1.ur.json` | 177 ecclesiastical terms | 177 |
| `data/saint-info.v1.ur.json` | 119 calendar entries, modern prose | 119 |

Where they disagree the prayers decide, because they are the Church's own
books. Where the prayers are silent - and they are silent about ranks, since a
prayer names no saint by his order - the names table decides, because the
vocabulary written here stands beside it in the same index, and because it is
the largest and most systematic of the four.

## What is being written

The Eastern Orthodox synaxarion in Urdu, in the Perso-Arabic script, read
right to left.

Two hazards sit in front of every word, and neither is settled by ear. Urdu's
Christian vocabulary comes overwhelmingly from the Protestant Bible and from
Roman Catholic usage, so a dictionary hands back forms this site does not use;
and Urdu shares much of its religious vocabulary with Islam through Arabic and
Persian, so a word can be exact and still carry a settled Islamic sense that
makes it wrong in a synaxarion. Both hazards are answered the same way: count
what the published files say, and follow it.

The counts below are from those four files. They are recorded so the decisions
are decisions and not recollections.

## The names that were counted first

| | Urdu | prayers | names | glossary | entries |
|---|---|---|---|---|---|
| God | خدا | 919 | 107 | 28 | 22 |
| | الله | **0** | 0 | 0 | 0 |
| Jesus | یسوع | 86 | 11 | 4 | 3 |
| | عیسیٰ | **0** | 0 | 0 | 0 |
| Christ | مسیح | 147 | 29 | 15 | 69 |
| Lord | خداوند | 554 | 43 | 2 | 10 |
| Holy Spirit | روح القدس | 57 | 0 | 0 | 2 |
| | پاک روح | 4 | 0 | 0 | 0 |
| Theotokos | والدہ خدا | 37 | 41 | 0 | 0 |
| | خدا کی ماں | 10 | 11 | 0 | 0 |
| | تھیوٹوکوس | **0** | 6 | 0 | 0 |

**الله and عیسیٰ are absent from all four bodies, and stay absent.** Both are
exact Urdu words and both carry a settled Islamic sense; the site's own prayers
say خدا and یسوع nine hundred and eighty-six times between them and never once
say the others. That is the whole argument, and it is not reopened.

**تھیوٹوکوس is in the names table six times and in the prayers not once.**
The prayers win: والدہ خدا. The transliteration is left where the index
already prints it and is not spread.

**قدوس and مقدس are not synonyms here.** The prayers say قدوس of God, in the
Trisagion and the Thrice-Holy, 82 times and never of a saint; مقدس is the word
for a holy person or a holy thing, 149 times in the prayers and 104 in the
names table. A saint is مقدس. God is قدوس.

## The honorific is the rank

The names table prints سینٹ 400 times, and it stands before a name without
offence, as Saint does in English. So `strict` is False in
`tools/check_register.py`, and only the distinctions the table itself keeps are
asserted: a monastic is جلیل القدر, a martyr شہید, and neither is merely مقدس.

### The ranks

Drawn from the names table unless marked otherwise; the count is that table's.

| English | Urdu | count |
|---|---|---|
| Saint | سینٹ | 400 |
| Holy | مقدس | 104 |
| Venerable | جلیل القدر | 381 |
| Martyr | شہید | 377 |
| Great Martyr | عظیم شہید | |
| Hieromartyr | کاہن شہید | 90 |
| Virgin Martyr | کنواری شہید | 23 |
| New Martyrs | نئے شہداء | |
| Woman martyrs | خواتین شہداء | |
| Protomartyr | اولین شہید | |
| Confessor | معترف | 35 |
| Passion-bearer | جاں نثار | |
| Prophet | نبی | 25 |
| Prophetess | نبیہ | |
| Apostle | رسول | 58 |
| Equal-to-the-Apostles | رسولوں کے برابر | 11 |
| Righteous | راستباز | 35 |
| Blessed | مبارک | 20 |
| Fool-for-Christ | مسیح کے لیے احمق | 12 |
| Wonderworker | معجزہ گر | 64 |
| Unmercenary physician | بے غرض معالج | 3 |
| God-bearing | خدا بردار | |
| Bishop | بشپ | 163 |
| | اسقف | 48 |
| Archbishop | سردار اسقف | 46 |
| Metropolitan | میٹروپولیٹن | |
| Patriarch | پیٹریارک | |
| Priest | کاہن | 108 |
| Deacon | شماس | |
| Monk, monastic | راہب | 45 |
| Abbot | مٹھ کے سربراہ | 93 |
| Virgin | کنواری | 33 |
| Monastery | مٹھ 97, خانقاہ 20 | |

**بشپ and اسقف both stand, and the table uses both in one breath** - one entry
reads کے بشپ and the next کے اسقف of the same office. بشپ is the majority and
is written here; اسقف is not corrected where the index already prints it.

**رسولوں کے برابر and رسولوں کے ہمسر both appear**, eleven against six. The
majority is taken and held.

**Equal ranks, unequal counts.** Where the table has only one or two instances
of a rank, the form is taken from those instances and not improved on.

## Names

**A biblical name takes the form the Urdu Bible gives it; every other name is
transcribed through English.** The table settles this without ambiguity:
پطرس, پولس, اندریاس, فلپس, تیمتھیس, یوحنا, زکریاہ, ملاکی, میکاہ, شمعون - the
received Urdu scriptural names; and beside them جارج for George, جان for John
Climacus, بازل for Basil, اتھاناسیس for Athanasius, سیرل for Cyril, انتھونی
for Anthony, تھیوڈور for Theodore, نکولس for Nicholas. These are English
sounds in Urdu letters, not Greek ones: Anthony and not Antonios, George and
not Georgios. The rule is the table's, not a preference, and it is followed.

## Word order

Urdu puts the modifier before the head, so a commemoration runs
**place, then rank, then name**, with the place in the oblique with کے / کی:

| English | Urdu |
|---|---|
| Martyr Basil of Ancyra | انکیرا کے شہید باسل |
| Venerable Paul of Thebes | تھیبس کے جلیل القدر پولس |
| St Raphael, Bishop of Brooklyn | بروکلین کے سینٹ رافیل، بشپ |
| Great Martyr Marina of Antioch | انطاکیہ کی عظیم شہید مرینا |
| and those with him | اور ان کے ساتھ والے |
| who suffered with her | اور ان کے ساتھ دکھ سہنے والے |
| Translation of the relics of N | ن کے آثار کی منتقلی |
| Nativity of the Most Holy Theotokos | نہایت مقدس والدہ خدا کی پیدائش |
| Sunday of N | ن کا اتوار |
| Feast | تہوار |
| Monastery of N | ن کا مٹھ |
| the Caves | غار |
| Repose of N | ن کی وفات |

The English "of PLACE" becomes a preceding genitive, never a trailing one. A
place ending the phrase would be English word order in Urdu words.

## Punctuation and script

- **Comma: U+060C ARABIC COMMA `،`**, which is what all four bodies use.
- **Full stop: `۔` U+06D4 ARABIC FULL STOP**, as the prayers set it.
- **Straight quotes `"..."`**, per the house rule.
- **Hyphens, never em or en dashes.**
- **Perso-Arabic script throughout.** No Latin letter and no Devanagari
  character anywhere. Digits are the ASCII digits the other tables use.

## Before writing a batch

- Look the name up in `data/saint-names.v1.ur.json` first. If the
  commemoration is there, its rendering of the name and the place is the one
  to use; the vocabulary must not invent a second spelling of a saint the
  index already prints.
- Take an ecclesiastical term from `data/glossary-i18n.v1.ur.json`.
- Consult `tools/saint_terms/ar.py` where a Christian word is wanted and the
  Urdu bodies are silent. Arabic settled these questions in a script Urdu
  shares, and where it found a received Christian word rather than a borrowed
  one that is evidence worth weighing. It is evidence and not a source: Urdu
  is not Arabic and its readers are not Arabic readers, and nothing is copied
  across without a reason in the Urdu bodies.
- Render what the English entry says and nothing beyond it. No date, relic,
  jurisdiction or episode that is not in the entry.

## One thing the glossary does that is not followed

`data/glossary-i18n.v1.ur.json` writes with the full apparatus of Urdu
diacritics - مُقدّس, شمّاس, بزرگ - where the names table and the prayers write
unpointed: مقدس, شماس. Its **vocabulary** is authoritative and is used; its
**pointing** is not reproduced, because three of the four bodies do not point
and the index would read as two languages set side by side.

## The Forerunner, and the spelling of baptism

The commemorations settle both. Saint John is "پیش رو اور بپتسمہ دینے والے
یوحنا" there - پیش رو seven times and پیشرو twice for the Forerunner, and
بپتسمہ دینے والا for the Baptist. The two-word پیش رو is what the
commemorations mostly write, so it is what the vocabulary writes. A house of
his dedication is "یوحنا پیش رو کا مٹھ".

The noun is بپتسمہ, never باپتسمہ: 6 in the prayers, 16 in the
commemorations, 3 in the glossary and 16 in the notes, against none of the
longer spelling anywhere. Two early entries had written the Forerunner as
"کرن باپتسمہ دینے والے", which is neither the site's word for him nor its
spelling of the sacrament; both were corrected.

## Three more settled from the commemorations

The Archangel is **سردار فرشتہ** - "سردار فرشتہ میکائیل اور جبرائیل کا
اجتماع" and "سردار فرشتہ میکائیل اور دیگر بے جسم قوتوں کا اجتماع" - and one
stray مہاراست فرشتہ beside them does not displace it. An early entry had
written مقرب فرشتہ; it was brought into line.

The Annunciation is **بشارت** (five in the commemorations, none competing).
The Protection is **حفاظت**: "ہماری نہایت مقدس بی بی، والدہ خدا اور ہمیشہ
کنواری مریم کی حفاظت". پناہ is the prayers' word for refuge taken in God, 24
times, and is not the name of the feast.

Saint John Chrysostom is **یوحنا سنہری دہن**. The commemorations prefer زریں
دہن (5 against 1), but the prayers say سنہری دہن three times to زریں دہن
once, and the prayers win.

## A council is a کونسل

The commemorations say it seven times and never anything else: "پہلی عالمی
کونسل کے مقدس آباء", "ساتویں عالمی کونسل", "پہلی چھ کونسلوں کے آباء". The
glossary's مجلس (7) is the general word for an assembly and does not name the
Councils; between the two the commemorations decide, because it is their own
subject. Four early entries had written سونہدوس, a Greek word this site does
not use in Urdu anywhere, and three had written مجلس; all seven were brought
to کونسل.

The Fathers of a Council are آباء, and the Sunday of Orthodoxy is
"راست دینی کا اتوار".

## The Liturgy, communion, and the passion-bearer

The Liturgy is **قداس** - the glossary says it nineteen times and nothing
competes with it anywhere. Two early entries had written عبادت, which is
worship in general, and were corrected. عبادت کا لباس stays for vestments,
where it is not naming the service.

To give communion is to give **مقدس اسرار** (4 in the prayers, 2 in the
notes); عشائے ربانی, 6 in the prayers, is the Supper itself and not the act.

A passion-bearer is **آلام بردار**, as the commemorations write Saint Gleb.

## Biblical names are looked up, not transcribed

The site publishes Holy Scripture in Urdu - the New Testament in
data/bible.v4.ur.b64 and the Old in scripture/ur - so a name that occurs in
the Bible is read off the text rather than rendered by ear: دبورہ, بارک,
گومر, ہوشیع, ایلیاہ, الیشع, شونمی, نعمان, رحبعام, شمعیاہ, نینوہ, بیت لحم,
یردن, صیون. The edition points its names heavily and marks them with U+0614;
the vocabulary keeps the letters and drops both, as the commemorations do.

## Place and person names follow the commemorations, not the ear

Where the commemorations already spell a name, that spelling is the site's
and the vocabulary uses it without re-deciding: رادونیج (9) not رادونیژ,
سرجیئس (11) not سرگیوس, وولودیمیر for Volodymyr in Volhynia, پیریسلاول-
زالیسکی, پیشنوشا, پیریکوپ, روبیکا, ژلیزنوبوروف. Six early entries had
guessed رادونیژ and سرگیوس and were brought into line.

"Abbot of X" is "X کے مٹھ کا سربراہ", which is the commemorations' own
construction.

## Two words the site had not yet needed

**The archpriest is بڑا کاہن.** Nothing in the prayers, the commemorations,
the glossary or the notes names him, so the word is chosen rather than found;
it is kept distinct from سردار کاہن, which stands for the hierarch and for
Aaron the high priest.

**Holy Friday is مقدس جمعہ**, from the commemorations, and Holy Thursday
مقدس جمعرات on the same pattern.

## The Evangelist, and the Seventy

The Evangelist is **مبشر** - "رسول اور مبشر مرقس", "رسول اور مبشر یوحنا
عالمِ الٰہیات" - five times in the commemorations against one انجیل نویس.
Three early entries had written انجیل نویس and were corrected.

An Apostle of the Seventy is **ستر کے رسول**, thirty-seven times over. Six
early entries had built the phrase differently and were brought to the
commemorations' construction.

The Ancestors of God are **خدا کے آباؤ**, as the commemorations name Joachim
and Anna, and Anna herself is **آنا**. The Apostle Andrew is **آندریو**.
