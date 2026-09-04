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

## When the Bible and the commemorations both have a name

They mostly agree; where they do not, the commemorations win for a saint,
because a saint's name in this index is his name as the Church commemorates
him and not a verse reference. So the Apostle Andrew is آندریو, though the
Urdu New Testament writes اندریاس at John 1:44, and the desert father is
دانیال, though the Bible's book is دانی ایل. The rule is general: the commemorations win wherever they
speak, and the Bible fills the gaps. So Mesopotamia is میسوپوٹیمیا, Arethusa
ارتھوسا, Armagh آرما and Pergamum پرگامم, while a place the commemorations
never name goes to the Bible: بیت عنیاہ, بیت صیدا, گلیل, بابل, اشقلون,
ابی نوعم, برسباس.

Great Lent is **عظیم روزے**, nine times in the commemorations against the
glossary's بڑے روزے; one early entry was corrected. Cherson is خرسون, as the
commemorations of its hieromartyrs have it, not the خیرسون two entries had
guessed.

## Relics are آثار

The commemorations say آثار seventy times - "کے آثار کی بازیافت", "کے آثار
کی منتقلی" - and the glossary's باقیات six. The commemorations win, and
sixty entries that had been written with باقیات were rewritten, the
agreement following the noun from feminine to masculine: "اس کی مقدس باقیات
جو لے جائی گئیں" becomes "اس کے مقدس آثار جو لے جائے گئے".

## Where the index and the vocabulary had begun to differ

Two names were being written twice, once in each body, and the commemorations
settled both because a name in this index is the name the Church commemorates.
The prince of Novgorod is **مستسلاو**, as "نووگوروڈ کے شہزادے سینٹ مستسلاو
(جارج)" has him, and the one entry that had written مستیسلاو was brought into
line. **بوتوو** is the spelling of Butovo, from "بوتوو کے نئے شہداء اور
معترفین", and the entry that had written بوتووو was corrected. A place ending
in -ovo that the commemorations do not name keeps the vocabulary's own longer
spelling - بوگولیوبووو, کاسپیرووو, کونداکووو - which is the majority there.

Where the vocabulary had already settled a form and the commemorations only
brush against it, the vocabulary holds: میرا for Myra (four against one مائرا),
پیلوپونیس, بِتھینیا, موژائسک, and نیصا for Nyssa, where the single
commemoration writes نِسّا with the full pointing that is not reproduced here.
Where the commemorations do speak plainly they are followed: پائسیس for
Paisius against the one پائسیوس the vocabulary had written, and پارامونی for
the Paramony, which the commemorations name at the eve of both feasts.

## The myrrh-bearers

The commemorations keep two phrases apart and so does the vocabulary. A
myrrh-bearer is **خوشبو لانے والی** - the Sunday of the Myrrh-bearing Women,
Joanna, Mary Magdalene, and the word is feminine because in this index every
one of them is. To stream myrrh is **مُر بہانا**, of Saint Demetrios and Saint
Simeon, and it is not the same word.

## A verse is looked up, not rendered

"Nathanael in whom there was no guile" is John 1:47, and the Urdu New
Testament this site publishes has it: نتن ایل جس کے دل میں کھوٹ نہیں. The
name and the clause are both taken from there, with the edition's pointing
dropped as everywhere else.

## Arius, and the word for his teaching

The four bodies write the name اریوس sixteen times and the adjective آریوسی
seven, and Arianism is آریوسیت, which the day entries already use. The
vocabulary follows all three rather than levelling them, because that is what
the site publishes.

## Two words the counting settled after the first table was written

**The patriarch is سرپرست اعلیٰ.** The rank table above had said پیٹریارک, but
that word never once stands for the man: all thirteen of its appearances are
inside پیٹریارکیٹ, which is the institution. The person is سرپرست اعلیٰ - 38
times in the vocabulary and 21 in the commemorations - and that is what is
written. سرپرستی is the adjective, as "پیچ میں، قدیم سرب سرپرستی کی کرسی" has
it, and سرپرست alone is the patron of a place or a trade.

**Thessalonica is تھسلنیکے.** The commemorations write تھیسالونیکی and
تھیسالونیکا between them eleven times and the vocabulary تھسلنیکے ten, so the
count decides nothing; the Urdu New Testament this site publishes does. It
writes تھِسلُنِیکے at Acts 17:1 and at the head of both epistles, and the
vocabulary already had the pointing dropped and the letters right.

Patara went the other way for want of any evidence at all - one instance in
each body - and the commemoration's پتارا was taken, the one پاتارا corrected.

## Smolensk, and the archpriest the doc had missed

**Smolensk is سمولینسک.** The vocabulary had written اسمولینسک six times,
giving the initial cluster the prosthetic alif Urdu gives اسکول and اسکندریہ;
the commemorations and the day entries write سمولینسک seven times between
them. The rule holds and the six were corrected.

The note above that the archpriest is بڑا کاہن says nothing in the four
bodies names him. That is not so: the glossary has him, as **رئیس الکہنہ**.
بڑا کاہن stands where the vocabulary has already written it, but the glossary
is the older word and the entry should have been read before the choice was
made. **The protopresbyter is پروتوپریسبیتر**, on the pattern of the
glossary's own ہیرودیاکون, which transliterates a Greek rank where Urdu has
no word of its own.

## Alexander, and the words for a man's place in a line

**Alexander is الیگزینڈر.** The commemorations write it twenty times and never
anything else; the vocabulary had written الکسنڈر six times beside two of its
own الیگزینڈر, and the six were corrected. The saints of Svir, of Kushta, of
Oshevensk and of Alexandria are all one spelling now.

A **successor** is جانشین and a **predecessor** is اس سے پہلے والا. پیش رو
would be the natural word and is not available: it belongs to the Forerunner
and to no one else. **سلف** was considered and set aside, because in Urdu it
carries a settled Islamic sense that a saint's entry has no business borrowing.

## Dionysius, counted rather than chosen

Four spellings were in use across the bodies and none was obviously the
site's: ڈیونیسیس seven, دیونیسیوس six, دیونیسیس four, ڈایونیسیس three. The
largest is **ڈیونیسیس** and the vocabulary now writes it alone; the six
دیونیسیوس it had written were changed. **دیونیسیو** is a different word and
is untouched - it is the Athonite house of Dionysiou, not the saint.

Ephraim is **افریم**, one name after all. It was written here as two - افریم
for the Syrian and افرایم for the Russians - on the strength of a single
commemoration of a new martyr; the commemorations write افریم for the Syrian
and for the abbot of Novy Torg both, and the vocabulary's افرایم were changed
to match. The Hesychast is ہیسوخاست, from the glossary's ہیسوخاسم.

The Studite is **اسٹودیت**. It was written into the vocabulary as استودیتی
first, on the Arabic's pattern and on the belief that no Urdu body here had
the word; the vocabulary already had it, inside a sentence too long for the
search that looked, and the five استودیتی were brought to the one that was
here before them.

## When the two bodies each have the name once

A place spelled once in the vocabulary and once in the commemorations, and
differently, settles nothing by counting. The rule above decides it: the
commemorations win, because a name in this index is the name the Church
commemorates. So پتارا, سرمیم, سکیپسس, شینکرسک, کرونسٹاٹ, نورما, ورکولا,
ویشیرا and ویرتسا, and the single instance in the vocabulary was corrected
each time.

The exception is a name the vocabulary has settled in the **received**
register - the form Urdu already has for that place, not a transcription of
the English. ہسپانیہ, انقرہ, طیسفون, ترابزون and صوفیہ stand for that reason,
and would read as two languages beside قرطبہ and نصیبین and رصافہ if they
did not.

## Kostroma and Nicomedia, and where a stray spelling stands

Two names had drifted once each inside the vocabulary itself. Kostroma is
کوسترما eight times in the vocabulary and کوسٹروما once; the commemorations
have کوسٹروما three times. The rule above gives a one-to-one tie to the
commemorations, but this is not a tie: the vocabulary holds a clear majority
and the single stray was corrected to کوسترما. Nicomedia is نیکومیڈیا
eighteen times in the vocabulary and nineteen in the commemorations, against
one نیکومیدیہ; that one was corrected too.

Neither correction touches the commemorations, which are not this lane's to
write. Where the two bodies still differ on Kostroma, the vocabulary is the
one that carries the name eight times and it keeps its spelling.

## The words for a house of saints

The captions that name a theme rather than a saint arrive without an
honorific, and they are written as the language writes a phrase, not as a
gloss of the English. A participle in English becomes a relative clause in
Urdu: "a monastery grown from one cell" is ایک مٹھ جو ایک ہی حجرے سے بڑھا,
and "a century of labor crowned" is ایک صدی کی محنت جو تاج پوش ہوئی.

Two of the words in them were settled from the prayers rather than chosen.
The prayers call the Theotokos بے عیب, so a blameless life is a بے عیب
زندگی. For peaceful the prayers are divided between پُرامن and پرامن once
each and settle nothing, so the vocabulary's own پرامن stands; and a saint's
death is his وفات here, as it is everywhere else in this table, so the
caption is پرامن وفات.

## Zerubbabel and Joshua, read out of the Scripture

Neither name is in the commemorations or in the prayers, and the Urdu
Scripture this site publishes has both in the first verse of Haggai:
زرُبّابِیل and یہوشُع. They are written here as that verse writes them,
without the edition's own mark over a proper name, which belongs to the
edition and not to the name. The pointing is kept, as it is kept for بِتھینیا
and اُست-وِم, because these are names an Urdu reader does not meet often.

The rank is the exception. That verse says اعلیٰ کاہِن, but this table has
said سردار کاہن for the high priest from Aaron onwards, and a table that
calls Aaron سردار کاہن and Joshua something else is two vocabularies. The
Scripture settles the names; the table keeps its own word for the office.
