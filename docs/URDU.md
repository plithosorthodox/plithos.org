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
| Passion-bearer | آلام بردار | 20 (vocabulary) |
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

## The ascetic has two words, and both are right

عابد stands forty times in the vocabulary and زاہد three; the commemorations
have زاہد twelve times and عابد not once. That is not a disagreement to be
resolved by deleting one of them, because the two bodies are doing different
work. زاہد is the title the commemorations set before a saint's name - شام کے
زاہد سینٹ پبلیس - and where a rendering here reproduces a commemoration's own
line, زاہد stands with it. عابد is the word the vocabulary uses for the man
himself in its own sentences, and it keeps that work, with عابدانہ for the
adjective: عابدانہ محنت, عابدانہ جدوجہد, ارغوانی کے نیچے عابدانہ زندگی.

## Four names counted, and where the tie went

Pasikrates was پاسیکراتیس once in the vocabulary and پاسیکریٹس once in the
commemorations. One against one is the tie the rule gives to the
commemorations, and the vocabulary was brought to پاسیکریٹس. Daria and
Claudius went the same way, to داریا and کلاڈیس, and Antoninus to انتونینس,
which the commemorations carry twice.

Chios and Moesia went the other way for the same reason: خیوس stands ten
times in the vocabulary against one کیوس in the commemorations, and موئیسیا
four times against one موسیا. A majority that size is not a tie.

## The canonarch is not the reader

Two renderings had called the canonarch قاری, which is the reader, a
different order; a third transliterated him کانونارک and the commemorations
call him کیننارک. This was not a spelling to be counted but an office to be
got right, so all four now read کیننارک, and قاری is left to the reader
alone.

## Boldness before God and boldness before a governor

The prayers say جرأت and the vocabulary says دلیری, and they are not
competing. The prayers use جرأت for what a sinner does not have before the
Son and what a mother has with him - the boldness of approach. دلیری is what
a priest of Side shows a governor under torture, and that is the word the
headings take: دلیرانہ اقرار, حکمرانوں کے سامنے دلیری, بتوں کے خلاف دلیری.

## Courage and boldness are two words here

دلیری is what a martyr shows a governor, and the headings that translate
boldness take it: حکمرانوں کے سامنے دلیری, بتوں کے خلاف دلیری. ہمت, which
the prayers and the vocabulary both carry, is courage: بڑھاپے میں ہمت, وہ
ہمت جو ڈگمگانے والوں کو مضبوط کرتی ہے. The one heading that had taken
دلیری for courage was brought over.

The deaconess is شماسہ, three times in the vocabulary and once in the
commemorations against two خاتون شماس, and compunction is the glossary's own
دل کا چھِدنا.

## Humility is عاجزی

The prayers say عاجزی eight times and the vocabulary had انکساری three; the
prayers win, and the vocabulary already called the humble man عاجز, so the
noun and the adjective now belong to one another. Every انکساری was brought
over.

## Tyre is صور

The vocabulary had تیر four times and صور four; the commemorations have صور
twice and تیر not at all, so صور carries it six to four and the four تیر
were brought over. It is also the name the Urdu reader already has for the
city, which تیر - the ordinary word for an arrow - is not.

## The lives take their register from the index, not from the day panel

The short entries in `data/saint-info.v1.ur.json` were written before the
vocabulary and use another set of words: ڈیکن for the deacon, پریسبیٹر for
the presbyter, خانقاہی for the monastic, آرتھوڈوکس چرچ for the Church. The
lives stand beside the Saints index, whose names come from the
commemorations and whose vocabulary is the terms table, so they take that
register: شماس, کاہن, راہب, راست دین کلیسا, جلیل القدر, معترف, عابد, مٹھ,
بے فساد, آلام بردار, مقدس آثار. Where a life needs a word the table has
already settled - a place, a rank, an icon's name - it uses the table's
word and does not settle it again.

## Andrew, and the one place the Scripture is not followed

The Urdu Scripture calls the Apostle اندریاس. This site calls him آندریو
eighteen times in the vocabulary and six in the commemorations, and keeps
اندریاس for Andrew of Crete, whom both bodies name that way. The
distinction is real and useful, so the Apostle stays آندریو and the
hymnographer of the Great Canon stays اندریاس; what the Scripture settles
in his life is not his name but his words, and the confession he carried to
his brother is written as John's Gospel writes it.

## Herodion, Decius, and where the two bodies pull apart

Three spellings of Herodion stand on the site: the commemorations write
ہیروڈین twice, once in the entry for this very day, and ہیروڈیون once for the
abbot of Iloezersk; the vocabulary writes ہیرودیون once. The apostle takes the
form his own commemoration gives him, ہیروڈین, and the abbot keeps his.

Decius goes the other way, and the reason is that he is not a saint. The rule
that the commemorations win is a rule about how the Church names the men she
venerates; an emperor is named in passing, and here the vocabulary has دیقیوس
four times against the commemorations' ڈیسیس twice, and five lives were
already written with دیقیوس. It stands.

Rufus is روفس, which the vocabulary has ten times and the Urdu New Testament
has at Romans 16:13 and Mark 15:21; the رفس of two entries is the stray.

## A roll of names is reported, not transcribed

Romans 16:14 greets five men at once, and the edition spells one of them
اسنکرتس where this site's vocabulary has اسینکریتس. A verse quoted for its
words is followed; a verse cited for the men it names is reported in the names
by which the site commemorates them, since the reader has met those names in
the index and will meet them again. So the greeting is given as اسینکریتس،
فلیگون، ہرماس، پترباس اور ہرمیس, and nothing is set in quotation marks.

## The Theologian, and Gregory

Saint John is یوحنا عالمِ الٰہیات - the vocabulary thirty-eight times and the
commemorations four, including the entry for his brother James. Saint Gregory
is عالم دین گریگوری, which is the only form the commemorations give him. The
two titles are not interchangeable here; each name keeps the one the site has
already given it.

## Years are written in figures alone

The lives write 1341، 1347 اور 1351 میں and تقریباً 250 میں, with no era
particle after the number. The commemorations do the same with feast dates.

## Matthias, Byblos, and the place-line that belongs to a saint

Three names came up where the commemorations and the vocabulary each have a
form, and the rule that the commemorations win did not decide them cleanly.

Matthias is متیاہ in the vocabulary twice and in the Urdu New Testament at
Acts 1:23 and 1:26, and متیاس in the commemorations once. Where the Scripture
and the vocabulary agree against a single commemoration, the two are followed:
متیاہ. The apostle Justus keeps the جسٹس his own commemoration gives him,
though the same verse names him یوستس, because that is his name in this index.

Byblos is بیبلوس and Phoenicia فینیکے in the vocabulary, which carries the
place-line of this very saint - Byblos, Phoenicia - as the Saints index prints
it beneath him; the commemoration of a martyr of the same town writes بائبلوس
and puts her in شام. A saint's own place-line is followed for that saint.

Edessa goes the other way and follows the commemorations: ایڈیسا, not the
vocabulary's اڈیسا. Aristarchus stays ارسٹارکس, as two vocabulary entries and
an earlier life have him.

## Words the lives needed and the site had not written

- Nazirite: **نذیر**, from Numbers 6:2 and Judges 13:5.
- Ararat: **اراراط**, from Genesis 8:4.
- The pinnacle of the Temple: **ہیکل کا سب سے اونچا مقام**, as Matthew 4:5
  has it.
- A fuller: **دھوبی**, which is the vocabulary's word for the martyr of Salona.
- The granary: **کھتّہ**, and wheat **گیہوں**, from Matthew 3:12 and 13:30.
- A catholic epistle: **عام خط**. The site had no term; this is the ordinary
  Urdu one and is used for both James and Jude.
- The Mystical Supper: **بھید بھرا عشائیہ**. The prayers say عشائے ربانی of
  Holy Communion, which is the gift and not the evening, so it is not borrowed
  for the night on which the gift was given.
- Idumea: **ادومیہ**, built on the ادوم of Genesis 36:8.

## The seven deacons, and the eunuch on the Gaza road

Acts 6:5 names the first seven, and the site keeps two of its own spellings
against the edition's: اسٹیفن for Stephen and پروخورس for Prochorus, which the
commemorations have, beside the edition's فلپس, نکانور, تیمون, پرمیناس and
نیکلاؤس, which nothing here contradicts. نکانور and پرمیناس are the
commemorations' own, and they agree.

The Ethiopian is خواجہ سرا, which is the word the vocabulary uses of him in
the Saints index, and the edition's خوجہ is left where it stands. Baptism is
بپتسمہ throughout, as this doc settled before the vocabulary was begun, and
not the edition's پاک غسل.

Azotus is اشدود and Isaiah یشعیاہ, both from Acts 8. Onesimus keeps the
اونیسیمس of his commemoration though Philemon 1:10 writes انیسمس; the epistle
supplies everything else about him - the son begotten in bonds, the man once
of no use and now of great use, the beloved brother, the debt to be charged to
Paul's account.

The Caspian Sea had to be written for the first time: **بحیرہ قزوین**.

## Thessalonica and Macedonia

Thessalonica is **تھسلنیکے** - the vocabulary twenty-four times and the Urdu
New Testament at Acts 17:1 - against تھیسالونیکی, which the commemorations
have eight times and two vocabulary entries besides. Where the Scripture and
the larger body agree, they are followed, and the stray is left where it is
printed.

Macedonia is **مکدنیہ** for the same reason: five vocabulary place-lines and
Acts 16:12, against a مقدونیہ that the commemorations use four times, once of
a man of that name rather than the province. Philippi is فلپی.

Simon the Zealot is **شمعون غیور**, which the commemorations and the
vocabulary both give him; the edition's شمعون قنانی and زیلوتیس are the two
Gospel names, and the life gives them as the Gospels give them, side by side.

Three more written for the first time: Abkhazia **ابخازیہ**, Aramaic
**ارامی**, and the emperor Nero **نیرو** - the نیرو already on the site is a
lake near Rostov, and the coincidence is left alone.

## The Forerunner's title in the lives

The commemorations call Saint John آگے چلنے والا, and the lives use that and
not a transliteration. Thaddeus of the Seventy was baptized by him, and it is
the only place so far the lives have needed the title.

## Names the epistles to Timothy gave the lives

The two epistles supply their own vocabulary and it is used as it stands:
the deposit committed to him is **امانت**, the gift to be stirred up is
**نعمت کے شعلے کو بھڑکانا**, no man is to despise his youth in the edition's
own words, and Paul's own son in the faith is **ایمان کے لحاظ سے حقیقی بیٹا**.
Lois is لوئس, Eunice یونیکے, Lystra لسترہ, Berea بیریہ.

Sosthenes keeps the سوستھینس of his commemoration; the edition spells him two
ways in two verses, سوتھینیس at Acts 18:17 and سوستھینیس at 1 Corinthians 1:1,
which is itself a reason not to take the name from there. Gallio is گلیو and
Crispus کرسپس, both from Acts 18.

Iconium is اکونیوم and Phrygia فروگیہ, as the vocabulary's place-lines have
them. Domitian and the Katagogia had no form here and are written دومیتیان
and کاتاگوگیا.

## The icon, and the words that came with it

An icon is **آئیکن** - the vocabulary two hundred and sixty-eight times - and
an iconographer **آئیکن نگار**, twenty-one times there against the
commemorations' شبیہ نگار. شبیہ keeps its own places, chiefly in the glossary
and in the titles of the iconoclast emperors, and is not spread into the
lives.

The Dormition is **وفات**, as the commemorations have it of the Theotokos.
The Beloved Disciple is **وہ شاگرد جس سے یسوع محبت رکھتے تھے**, which the
vocabulary already writes in full rather than shortening.

## What the vocabulary had already written for a life

The Saints index carries, in the vocabulary, a whole sentence about the holy
dust that rose each year from the empty tomb at Ephesus. The life of the
Theologian takes that sentence as it stands rather than rendering the English
again. Where the vocabulary has already said a thing in Urdu, the life says it
the same way; this is the first place a whole clause could be carried over,
and it will not be the last.

Crete is کریٹ and Gortyna گورتینا, both from the commemorations; Boeotia is
بویوتیا and Achaia اخیہ from the vocabulary; Emmaus اماؤس, Salome سلومی and
Miletus میلیتس from the Scripture; Patmos پاتموس, not the edition's پتمس,
because the vocabulary names the island and the commemorations do not.

## Pascha is پاسخا

The glossary says پاسخا eleven times and the prayers twice; the commemorations
have ایسٹر once, in the title of the feast itself, and the vocabulary uses
فسح only as an adjective, in فسح کے وعظ and فسح کی آگ. The prayers and the
glossary agree, so the feast is پاسخا in the lives and the two existing forms
are left where they are printed.

## The household of the shortest epistle

Philemon's family keeps the commemorations' spellings, not the edition's:
آرکیپس for Archippus where Philemon 1:2 writes ارخپس, and اپفیا for Apphia
where it writes افیہ; فلیمون agrees in both. The same rule gives جیسن and
سوسپیٹر for Jason and Sosipater, against the edition's یاسون and سوسپطرس,
and پیٹروباس، ہرماس، لینس، گایس، فیلولوگس for the five bishops of one
greeting, all from the commemoration that names them together.

Kerkyra is the island کیرکیرا and the king's daughter کرکیرا, which is how the
two bodies have them; Corfu is کورفو. Capernaum کفرنحوم, Perga پرگہ, Sinope
سنوپے, Neapolis نیاپولس, Parthia پارتھیا, Tarsus ترسس, Venice وینس. Media,
Serapis and Artemis had no form here and are written میدیا, سراپیس, ارتیمس.

## Two more clauses taken over whole

The vocabulary had already written the Amiens vision - Christ by night in the
half of a soldier's cloak, the beggar and the catechumen Martin - and the
Pochaiv footprint, including the name نقشِ قدم. Both lives use those words
rather than rendering the English again, on the rule the Theologian's tomb
established.

A catechumen is **نومرید**, which the vocabulary and the commemorations both
use. Gaul is گال, Amiens امیان, Volhynia وولہینیا, Pochaiv پوچائیف, a lavra
لاورا, Athos کوہ آتھوس, Iveron ایویرون, Portaitissa پورتائتیسا, Tbilisi
تبلیسی, and the Sioni cathedral سیونی کا بڑا کلیسا - all from the site's own
place-lines.

Two things had no form here. Bright Friday is written **روشن جمعہ**, on the
pattern of the Paschal week's own name; and the head of the Georgian Church is
**کاتھولیکوس اور پیٹریارک**, taking پیٹریارک from the rank table and
transliterating the first word, which Urdu has no other way to say.

## Moses is موسیٰ

The Old Testament edition writes موشہ; every body on this site writes موسیٰ -
the vocabulary ten times, the commemorations five, the prayers twice, the
glossary and the day entries once each. The prayers decide, and three lives
written with موشہ were brought into line. The doc's rule that a biblical name
takes the Bible's form holds where the site is silent; here the site is not
silent, and it has spoken with one voice.

Elijah keeps ایلیاہ, which both the edition and the vocabulary have.

## The Fast, and its furniture

The commemorations and the vocabulary have already named every station of the
Great Fast, and the life uses their words without inventing any: عظیم روزے,
پاک پیر, معافی کا اتوار, راست دینی کا اتوار, صلیب کی تعظیم, مصر کی سینٹ مریم,
لعزر کا ہفتہ, کھجور کا اتوار, پیش تقدیس شدہ نذروں کا قداس, and the عظیم قانون
of Saint Andrew of Crete read in the first week.

Two were missing. The Triodion is written **ترودیون**, transliterated as the
site transliterates اکاتھسٹ and اوموفوریون. A prostration is **زمین تک جھکنا**;
سجدہ is the exact word and carries a settled Islamic sense, which is the same
reason الله and عیسیٰ stay out, so the phrase is used instead.

Ivan the Terrible had no form and is **زار ایوان مہیب**. Andrew of Totma and
Andrew of Constantinople are both اینڈریو, as their own commemorations have
them, and Totma is ٹوٹما in this entry though the vocabulary writes توتما of
its other saints.

## The Russian north, and the word for a struggle

The commemorations name all five saints of this batch and their places, and
the lives follow them: قسطنطین, دوومونت (تیمتھیس), بالوں والے یوحنا, لارنس,
میکسیمس; کیف, پسکوف, روستوف, کالوگا, ٹوٹما, ورنیتسا, نالشیا, لتھوانیا. A
right-believing prince is **دیندار شہزادہ**, which the vocabulary and the
commemorations both print.

Chernihiv is چرنیہیو, from the commemorations, not the vocabulary's کرنیگوف.

The English lives use the Slavonic word podvig for the ascetic's struggle.
Urdu has no borrowing for it and does not need one: **جدوجہد** carries it, and
the lives already use لڑائی and محنت for the same thing where the sentence
prefers them.

Mindaugas, the Velikaya, the Khitrovo family and the Crimean Tatars had no
form here and are written مندوگاس, دریائے ویلیکایا, خیتروو and
کریمیا کے تاتاری, the last built on the تاتاری گروہ the vocabulary already has.

## A passion-bearer is آلام بردار, and the rank table was wrong

The table above lists جاں نثار for Passion-bearer. That form appears nowhere
on this site. The vocabulary says **آلام بردار** twenty times and the
commemorations twice; مصیبت بردار stands in one commemoration and is left
there. The lives use آلام بردار, and the table entry is corrected.

## Five entries said an ascetic was dressed in cats

بلی is a cat and چیتھڑا is a rag, and five vocabulary entries rendered "in
rags" as بلیوں میں. The site's own other word, چیتھڑوں میں, stands four times
beside it and is what the lives use. The five were corrected in
`tools/saint_terms/ur.py`; nothing else in that file was touched.

A tsar is **زار** - a hundred and forty-five times in the vocabulary against
eight for تسار - and the oprichnik اوپریچنک, which the vocabulary already has.

## Jerusalem is یروشلم

The vocabulary writes یروشلم forty-six times, the commemorations thirteen, the
prayers four, the day entries five. The Urdu New Testament writes یروشلیم, and
twenty lives had followed it. They were corrected. The rule is the one Moses
settled: the edition supplies what the site has not said, and yields where the
site has said it with one voice.

## The Church's own year

The commemorations name the day: کلیسیائی نیا سال (انڈکشن). Nicaea is نیقیہ,
Byzantium بازنطیم, the Bosphorus باسفورس, the New Rome نیا روم, the Holy
Wisdom مقدس حکمت, the Exaltation صلیب کی سربلندی, Saint Helen ہیلینا,
Bithynia بتھینیا, and Demetrios دیمیتریس - all from the site's own bodies.

Constantius, the Milvian Bridge, Leo the Isaurian and the Martyrion had no
form and are written قسطنطیوس, ملویان کا پل, لیو ایسورین, مارتیریون. The
acceptable year of the Lord is the edition's سالِ مقبول, from Luke 4:19.

## The councils, and the words the vocabulary already had for them

An ecumenical council is **عالمی کونسل** in the commemorations, and the lives
use that though the vocabulary elsewhere says عالمگیر of the Exaltation and of
the teachers. The Creed is **قانونِ ایمان**; the Son is **ایک ہی ذات کا** with
the Father and the homoousios **ہم ذات**, both phrases the vocabulary already
prints. An iconoclast is **شبیہ شکن**, which is where شبیہ properly lives.

Kazan is کازان, twice in the vocabulary against one قازان. Gregory of Nyssa is
نیصا کا گریگوری, twice in the vocabulary against the commemorations' نِسّا;
Nisibis نصیبین, Tarasius تراسیس, Spyridon سپیریڈون, Paphnutius پفنوتیس,
Meletius میلیتیس, Hermogenes ہرموجینیس, Pozharsky پوژارسکی, Arsenius ارسینیس.

The Pneumatomachi are given as the English gives them, **رُوح سے لڑنے والے**,
with no transliteration; the Time of Troubles is **مصیبتوں کا زمانہ**.

## Zachariah and Elizabeth

The Forerunner's parents are **زکریا** and **الزبتھ**, which is how their own
commemoration names them. The edition writes زکریاہ and الیشابیت, and one
vocabulary line writes الیشبع; the commemoration decides, as it does for every
saint. The Names section above lists زکریاہ among the received scriptural
names, and that stands for the prophet of the Old Testament book; the priest
of Luke 1 is زکریا here because that is the name the index gives him.

## Tamerlane is تیمور

Not a transliteration through English but the name the commemoration itself
uses, which is also the name he has in Urdu. Chonae is خونائے, Hierapolis
ہیراپولس, Laodicea لودیکیہ, Chudov چودوف, Joachim یوآخیم and Anna آنا, and
the Sretensky monastery ملاقات کا مٹھ، سریتینسکی - all the site's own.

Kuchkovo Field had no form and is کچکووو کا میدان. The Archangel is
مہاراست فرشتہ, as the vocabulary has him, and Chief Commander is سپہ سالار.

## Levi is لاوی

Twenty-six times across the vocabulary, the commemorations, the glossary and
the day entries, against six لیوی; the New Testament edition writes لیوی at
Acts 4:36 and Luke 5:27. One life had followed the edition and was corrected.
The tribe, the priestly line, and the publican whom the Lord called all take
the same form.

## A confessor is معترف, whatever one entry says

One commemoration writes اقراری of the confessors of Edessa. معترف stands
thirty-five times in the commemorations and is the rank word the table
settled; the life uses it, and اقراری is left where it is printed. This is the
same treatment بشپ/اسقف got: the majority is written, the stray is not
corrected.

Lydda is لِدہ, Carrhae کارہائی, the Thebaid تھیبائیڈ, Valens والنس,
Diocletian دیوکلیشین, Vyshgorod ویشگوروڈ, Aaron ہارون, and George the
Trophy-bearer فتح بردار جارج - all the site's own. Matthan and the Yuriev day
had no form and are متان and یوریو کا دن.

## The Nativity eve, and the words the prayers keep

The Paramony is پارامونی and a forefeast پیش تہوار, both from the
commemorations; a troparion is **تروپاریون** and a kontakion **کونتاکیون**,
which the prayers use fifteen and nine times. The Magi are مجوسی. Isaiah's
word is the edition's: ہمارے لیے ایک ولد پیدا ہوا ہے; Balaam's star is
یعقوب سے ایک ستارہ نکلے گا, from Numbers 24:17.

The Royal Hours had no form. The site has no word for the Hours at all, so
they are written **شاہی اوقات**, on the one اوقات the prayers use.

Iberia is ایبیریا, Atsquri اتسکوری and Samtskhe سامتسخے from the vocabulary's
Georgian place-lines; Olga اولگا, Igor اِگور, Nestor the chronicler نیستر (the
martyr of that name stays نسٹور), Photius فوتیس, Methodius میتھوڈیس, Moravia
موراویا, Rostislav روستیسلاو, Licinius لیکینیس, Milan میلان, and the Church
of the Tithes دسویں حصے کا کلیسا. Maxentius, Naissus and Sviatoslav had no
form: میکسنٹیس, نائیسس, سویاتوسلاو.

## Theophany is تھیوفنی

Both forms are on the site: تجلّیِ الٰہی seven times, and تھیوفنی twenty -
five in the vocabulary, six in the commemorations, nine in the day entries.
The larger count wins, and it has the further advantage of not colliding with
تجلّی, which is the Transfiguration in every church name the vocabulary
prints. The Jordan is یردن.

Chalcedon is کلقیدون, twice in the vocabulary against one کلیسیڈن. Christ's
two wills are مسیح کے دو ارادے, which the vocabulary already writes of the
Confessor. Yaroslavl is یاروسلاول, Poshekhonye پوشیخونیے - though this entry's
own commemoration says پوشیخونسک, and the life of that entry follows it -
Adrian آدریان, Philaret فیلارت.

Nestorius, the Monophysites, the Agiasma and the Feast of Lights had no form.
The first is نسطوریوس and the second یک طبیعت والے. The other two are not
transliterated at all: the holy water is عظیم مقدس پانی and the Greek name of
the feast انوار کی عید, because both are said in the English entry itself and
a borrowed word would tell the reader less than the plain one.

## The graves at Caphargamala

Gamaliel is **گملی ایل**, which the vocabulary and Acts 5:34 both write, and
not the commemoration's single گملئیل; it is the one place a commemoration
loses, and it loses to the Scripture and the vocabulary together, as Matthias
did. Nicodemus is نیکودیمس, Abibas ابیباس, Caphargamala کافرگمالا, Joseph of
Arimathea ارمتیاہ کا یوسف, Lucian لوسیان. The myrrh and aloes are the
edition's مُر اور عُود.

Ryazan is ریازان, Murom مُروم, the Oka اوکا, and the Golden Horde
سنہری گروہ - the vocabulary carries the whole scene of the bishop standing on
his mantle upon the water, and the life takes its words.

## A finding is still the saint's entry

Three entries in this batch are titled for the finding of relics rather than
for the saint, and the opening still has to name him by his rank: a monastic
gets جلیل القدر, not سینٹ, even when the sentence begins with the Church and
the day rather than with the man. Two openings were rewritten for this.

Novoezersk is نوویزیرسک, Cornelius of Komel کورنیلیوس (the abbot of the Pskov
Caves stays کورنیلیئس), Maximus یونانی میکسیمس, the Trinity-Sergius Lavra
مقدس تثلیث-سینٹ سرجیئس لاورا, Volokolamsk وولوکولامسک, Gurias گوریاس,
Sviyazhsk سویاژسک, Emesa ایمیسا, an archimandrite آرکمنڈرائٹ, the great schema
عظیم اسکیما, Voronezh وورونیژ, Metrophanes میتروفانیس.

Herman of Kazan is **جرمانس**: two commemorations and a vocabulary line spell
him so, and the third commemoration's ہرمن is the stray. Joanna is یوآنا from
her own commemoration, not the edition's یوآنّہ; Chuza خوزہ and the platter
تھال are the edition's. Peter the Great, Arta, Trivolis, Staritsa, Marcellus
and Uranius had no form: پیٹر اعظم, آرتا, ترائیوولس, ستاریتسا, مارسیلس,
یورینیس.

## The forefeasts

Every one of these days is already named in the commemorations, and the lives
use those names exactly: بشارت کا پیش تہوار, وفات کا پیش تہوار,
قیمتی اور حیات بخش صلیب کی عالمگیر سربلندی, تھیوٹوکوس کا ہیکل میں داخلہ,
ہیکل میں ہمارے خداوند کی ملاقات.

The greeting at Nazareth is the edition's سلام، آپ پر بڑا فضل ہوا ہے and the
answer میں تو خداوند کی بندی ہوں; Malachi's word and Isaiah's are quoted from
the Old Testament as the edition prints them. The Holy of Holies is
**پاک ترین مقام**, which is what Exodus 26:33 calls it; قدس الاقداس is the
familiar Urdu phrase and appears nowhere on this site or in this edition, so
it is not introduced.

## Stichera and katavasia

Two more of the service's own words had no form here. They are transliterated,
**ستیخیرا** and **کاتاواسیا**, on the pattern the site already set with
اکاتھسٹ, اوموفوریون, ستیخاریون and ترودیون: where the thing is a named part of
the Church's own books, the name is carried over rather than described.

The Transfiguration is تجلّی as a feast, which is the name its own
commemoration gives it, and صورت بدل گئی in the narrative, which is how
Matthew 17:2 says it happened; the forefeast's commemoration says
صورت بدلنے کا پیش تہوار and the life follows it there.

Christ is born, glorify Him is reported, not quoted: no Urdu of that katavasia
is published here, so the life says what the hymn says in its own prose and
sets no words apart as received.

## The American saints

Tikhon is **تیخون** - twice in the vocabulary and twice in the commemorations,
against one طیخون. Innocent انوسنٹ, Herman ہرمن, John of Kronstadt
کرونسٹاٹ کا سینٹ یوحنا, the Aleuts الیوت, Sitka سٹکا, Valaam والام, Spruce
Island اسپروس جزیرہ, Toropets توروپیتس, the Donskoy monastery دونسکوئے,
Kremenets کریمینیتس, Hotovitzky ہوتووٹسکی, and a protopresbyter
پروتوپریسبیتر - all already on the site. A glorification is **تمجید**, which
is what every one of these entries calls it.

Unalaska, Kamchatka, the Kurils, Yakutia, the Amur, the Lena, Helsinki and
Vyshinsky had no form: اونالاسکا, کامچاٹکا, کوریل, یاکوتیا, آمور, لینا,
ہیلسنکی, وشینسکی.

## The great women martyrs

All five names are already set: اناستاسیا with her title فارماکولیتریا and
its rendering زہروں سے چھڑانے والی, کرائسوگونوس, یوفیمیا, آئرین, کیتھرین,
مرینا (مارگریٹ). Chalcedon کلقیدون, Illyricum الیریکم, Pisidian Antioch
پسیدیہ کا انطاکیہ, Sinai سینا, Theodota تھیوڈوتا, and the three sisters
اگاپے، خیونیا اور ایرین from their own commemoration.

The vocabulary already carries the whole of Irene's ending - the empty tomb at
Ephesus and مقدس سلامتی کا بڑا کلیسا at Constantinople - and the life takes
its words. The emperor who rebuilt that church is جسٹینین, from his own
commemoration, though the vocabulary writes یوستینیان of his court.

Fausta, Publius, Zoilos, Evodus, Eutychianus, Apollinaria, Priscus, Ares,
Magedon, Penelope, Apellian, Sedecias and Sapor had no form and are written
فاؤستا, پبلیس, زوئیلوس, ایوودس, یوتیخیانوس, اپولیناریا, پرسکس, آریس,
میگیدون, پینیلوپے, اپیلیان, سیدیکیاس, ساپور.

## Kolyva, and the soldier saints

Kolyva is **کولیوا**, which the vocabulary already writes of the first
Saturday of the Fast; the wheat boiled with honey is گیہوں اور شہد, as the
Scripture's word for wheat has it. Mercurius is مرکوریس, Theodore
تھیوڈور تیرو with the commemoration's own gloss نوآموز سپاہی, Artemius
آرتیمیس, Barbara باربرا, Juliana جولیانا, Euphemia یوفیمیا; Amasea اماسیہ,
Pontus پونتوس, Euchaita یوخائٹا, Eusebia یوسیبیا, Heliopolis ہیلیوپولیس,
Dioscorus ڈیوسکورس, Anatolius اناتولیس, and Julian the Apostate مرتد جولین.

Scythian, the Marmarita cohort and Eudoxius had no form: سکوتی, مارماریتا,
یودوکسیس. Julian's dying word is reported, not quoted - اے گلیلی، تو غالب
آ گیا - since no Urdu of it is published here.

## Iconium stays اکونیوم

Paraskevi's own commemoration writes اکونیم and the vocabulary's two
place-lines write اکونیوم; three lives already use the latter. A place keeps
one spelling across the lives even where a single entry differs, which is the
same treatment بشپ/اسقف and معترف/اقراری got: the majority is written and the
stray is left in the index where it stands. Her own name is پراسکیوی, from
that same commemoration, and the Slavic pyatnitsa is پیاتنیتسا.

Eustathius is یوستاتھیس پلاکیداس, George the New نیا جارج at صوفیہ, born at
کراتوو; James the Persian is فارسی یعقوب, Niketas نکیتاس, the Danube ڈینیوب,
Mopsuestia موپسوئستیا, Theophilus of the Goths گوتھوں کا بشپ تھیوفیلس.

Theopiste, Agapius, Theopistus, Yezdegerd, Athanaric, Marianus, Selim, the
presbyter Peja and the surname Intercisus had no form: تھیوپستے, اگاپیس,
تھیوپستوس, یزدگرد, اتھاناریک, ماریانوس, سلیم, پیجا, and انترکیسوس, which the
life glosses as the entry glosses it, ٹکڑے ٹکڑے کیا گیا.

## An abbot is a monastic first

Theokteristus is typed Abbot and Confessor-Martyr, and an opening that gave
him only معترف اور شہید read as a monastic named by another rank. He opens
جلیل القدر معترف اور شہید. The pattern now holds for every abbot in the
lives: the monastic word comes first and the martyric rank after it.

Panteleimon stays **پانتیلیمون**, which the vocabulary writes twice, against
the پنتیلیمون of his own commemoration - the same treatment Iconium got, and
for the same reason: the lives already use it. Maximian is میکسیمیان,
Procopius پروکوپیس, Neanius نیانیس, Apamea اپامیہ, Theodore سٹراٹیلیٹس,
Heraclea ہیراکلیہ, Pelecete پیلیکیتے, Prusa پروسا, Triglia تریگلیا.

Copronymos and the Small Supplicatory Canon had no form: کوپرونیموس and
چھوٹا التجائی قانون, the second rendered rather than transliterated, since the
name says what the thing is and the reader has met قانون already in the
Great Canon of Saint Andrew.

## Adrianopolis and Theodota

Adrianopolis is ادریانوپولس, from the vocabulary's two place-lines, not the
ایڈریانوپولِس of one commemoration; Theodota is تھیوڈوتا, as the vocabulary
and the life of Anastasia have her, not that entry's تھیوڈوٹا. Both are the
same rule as Iconium and Panteleimon: the lives keep one spelling and the
index keeps its own.

Side سیدے, Pamphylia پامفیلیا, Aurelian اورلیان, Comana کومانا, Neocaesarea
نیوقیصریہ, Gregory the Wonderworker معجزہ گر گریگوری, Origen اوریجن,
Narcissus نرکسس, Eusebius of Caesarea قیصریہ کا یوسیبیوس, Antherus انتھیرس,
Glyceria گلیکیریا - all the site's own. A coadjutor is **معاون بشپ**, on the
vocabulary's معاون; a catacomb تہ خانہ. Antoninus, Septimius Severus, Pontian,
Callistus and Fabian had no form: انتونینس, سیپتیمیس سیویرس, پونتیان, کالستس,
فابیان.

## Antipas, and the one obituary written in Scripture

Revelation 2:13 is quoted as the edition prints it, with one change the rule
already required: the martyr is انتیپاس, as the vocabulary and his own
commemoration name him, not the edition's انِتپاس. The brazen bull is
پیتل کا بیل, which the vocabulary already writes of his icon, and Satan's seat
شیطان کی تخت گاہ, from the verse.

Laodicea is لودیکیہ, the vocabulary's two place-lines, not the لاودیکیہ of
Artemon's commemoration. Ravenna راونا, Pergamum پرگامم, Seleucia سلوکیہ,
Anthimus انتھیمس, Apollinaris اپولیناریس, Artemon آرتیمون, Anthousa انتھوسا,
Valerian ویلیرین.

Vespasian, Irenaeus, Patricius, Sisinnius, Charisimus, Neophytus and Artemis
had no form: ویسپاسیان, ایرینیس, پاتریکیس, سیسینیس, خاریسمس, نیوفیتس, ارتیمس.
A synaxarion is سناکسارین, as the commemorations already write سناکسس.

## Ancyra is انکیرا

Three commemorations write انکیرا and one vocabulary entry انقرہ, which is the
modern city's Urdu name; the ancient see keeps the form the index gives it.
Sebaste is سیباستے, Heracleopolis ہیراکلیوپولس, Daphne دافنے, Apollo اپولو,
Amasea اماسیہ, Sinope سنوپے, Glaphyra گلافیرا. Basil of Amasea is باسل, as
his own commemoration has him, though the entry for his relics writes بازل.

Philomachos, Soreoi, Saturninus and the deaconess Maria had no form:
فیلوماخوس, سوریوئی, ساتورنینس, شماسہ ماریا - the last built on the
commemorations' own شماس.

## Three Corneliuses and three Clements

The site keeps them apart and the lives follow it: the centurion of Acts is
**کرنیلیس**, the abbot of Komel کورنیلیوس, the abbot of the Pskov Caves
کورنیلیئس; the pope of Rome and the bishop of Ancyra are both کلیمنٹ, as their
commemorations have them, and Clement of Alexandria is the same word without
the title of saint.

Blaise بلیز, Agathangelus اگاتھنگیلس, Chersonesus خرسونیسوس, Skepsis سکیپسس,
the Hellespont ہیلیسپونٹ, Carthage کارتھیج, Cyprian سائپرین, Chariton خاریتون.
Mount Argeos, Euphrosyne, Sophia, Agrippina, Cyrenius, Dometius, Christopher,
Tertullian and Donatus had no form: آرگیوس, یوفروسینے, صوفیہ, اگریپینا,
کیرینیس, دومیتیس, کرسٹوفر, ترتلیان, دوناتس.

## The Areopagite's books

The four titles are rendered, not transliterated: آسمانی درجہ بندی,
کلیسیائی درجہ بندی, الٰہی نام, باطنی الٰہیات - the last already the
vocabulary's phrase for mystical theology. A book's title says what the book
is, and the Urdu reader who meets ستیخیرا and کونتاکیون as names of the
Church's own things gains nothing from a transliterated Greek title he cannot
open. The Unknown God is the edition's ایک نامعلوم خدا, from Acts 17:23.

Maximus the Confessor is معترف میکسیمس, twice in the commemorations against
one میکسمس. Justina جسٹینا, Theoctistus تھیوکتسٹس, Desan دیسان, Hierotheus
ہیروتھیس, Rusticus رسٹیکس, Eleutherius ایلیوتھیریس, Paris پیرس, Tyre صور,
Dorotheus دوروتھیس.

Argos, Memphis, Olympus, Mariab, Lutetia, Catulla and Odyssopolis had no form:
آرگوس, میمفس, اولمپس, ماریاب, لوتیشیا, کاتولا, اودیسوپولس.

## Two hundred lives, and where the count stands

At two hundred of the fourteen hundred and fifty-six, the method has not
changed and does not need to: list the batch, look every name up in the four
published bodies before writing it, take the Scripture for what the Scripture
says, count where the bodies disagree, write the decision down here, and never
ask the owner. Every batch so far has come back from
`tools/check_register.py --lang ur` at zero errors.

Sardis is سردیس, from the vocabulary's two place-lines, against the
commemorations' سارڈس; Samosata ساموساتا for the same reason. Eusebius of
Samosata is یوسیبیس, as his own commemoration has him - the historian of
Caesarea stays یوسیبیوس, and the site keeps the two apart as it keeps the
three Corneliuses apart.

Emilian ایمیلیان, Trebia تریبیا, Spoleto سپولیتو, Euthymius یوتھیمیس, Eutyches
یوتیخس, Tiridates تیریداتیس, Rhipsime and Gaiane ریپسیمے اور گائنے,
Etchmiadzin ایچمیادزین, Leo the Armenian لیو ارمنی, the Triumph of Orthodoxy
راست دینی کی فتح. Hermippus, Nikephoros, Patalareia, Assia, Michael the
Stammerer, Anak, Artashat and Sebastea had no form: ہرمپس, نکیفوروس,
پاتالاریا, اسّا, میخائیل لکنت والا, اناک, ارتاشات, سیباستیہ - the last kept
distinct from سیباستے in Cappadocia, which is a different town.

## The two entries for Hermogenes

The calendar carries the patriarch twice, for his glorification and for his
repose, and the English gives two different lives; the Urdu gives two
different lives too, as it did for the two Lukes. Nothing is copied between
them.

Hermolaus is ہرمولاؤس, the vocabulary's form, used already in the life of
Panteleimon, not the ہرمولاس of this entry. Thessaly is تھیسالی from the
vocabulary's place-lines. Meteora میتیورا, Nizhny Novgorod نیژنی نووگوروڈ,
Minin and Pozharsky مینن اور پوژارسکی, Hermocrates ہرموکراتیس, Hierotheus
ہیروتھیس, Galina گالینا. The Maeander, Yermolai, Wladyslaw, Pantoleon and the
White Sea had no form: مینڈر, یرمولائی, ولادیسواف, پانتولیون, سفید سمندر.

## Ignatius' seven letters, and the words he coined

The addressees are named as the Urdu New Testament names those churches -
افسیوں، میگنیسیوں، ترالیوں، رومیوں، فلادلفیوں، سمرنیوں - and his two famous
phrases are reported, not quoted, since no Urdu of the letters is published
here: بقا کی دوا for the medicine of immortality, کاتھولک کلیسا for the words
he wrote first, and the plea about God's wheat given in the site's own prose.

Polycarp is پولیکارپ, from two vocabulary entries against the commemorations'
پولی کارپ. Hippolytus ہپولیتس, Chryse خریسے, Ostia اوستیا, Irenaeus ایرینیس
(both of them), Lyons لیون, Pothinus پوتھینس, Sirmium سرمیم, Januarius
جنواریس, Benevento بینیوینتو, Pozzuoli پوزولی, Naples نیپلز, Probus پروبس.

Gnostic is **عرفانی**, from عرفان, which is what the heresy claimed to be
selling; Sossius, Misenum, Festus, Desiderius, Proculus, Eutychius, Acutius,
Pannonia and the Sava had no form: سوسیس, میسینم, فیستس, دیسیدیریس, پروکلس,
یوتیخیس, اکوتیس, پانونیا, ساوا.

## Three Lucians

The presbyter of Antioch, the priest-monk of the Kyiv Caves and the bishop of
Beauvais are all لوسیان, as their commemorations have them; the site does not
distinguish them by spelling and neither do the lives.

Kindeos کندیس, Kuksha کُکشا, Pimen پیمن, the Vyatichi ویاتیچی, Beauvais بووے,
Marcellinus مارسلینس, the Near and Far Caves قریبی غار and دور کے غار. Nikon,
Batu, the Bellovaci, Cyrinus and Antoninus had no form: نیکون, باتو,
بیلوواکی, کیرینس, انتونینس.

## Susa is شوشن

The vocabulary's place-line gives the Persian city its received Urdu name,
شوشن، فارس, which is what the Old Testament calls it; the transliteration is
not used. The Prophet Daniel is دانی ایل, twice in the vocabulary against one
دانیال in the commemorations - the desert father of that name keeps دانیال, as
this doc settled earlier, and the two are now distinguished on the page as
they are in the calendar.

The Banquet of the Ten Virgins is **دس کنواریوں کی ضیافت**, which the
vocabulary already writes on Methodius' icon line; Lycia is لیکیا, Patara
پتارا, Arethusa ارتھوسا, Amphipolis امفیپولس, Magydos میگیدوس, Perge پرگے,
Mocius موکیس, Milos میلوس. Mark of Arethusa is مرقس, the same form the
Evangelist has, because that is what his commemoration gives him.
