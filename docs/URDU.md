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

## Pascha stays پاسخا even where the vocabulary says فسح

The vocabulary's line on Gregory V writes عین فسح کے دن. The lives keep
**پاسخا**, which the glossary says eleven times and the prayers twice, and
which this doc settled; فسح remains where it is printed, as an adjective on
the paschal sermons and the paschal fire and here. Nothing is corrected in the
index.

Niketas نکیتاس, the Skete of Saint Anne سینٹ آنا کا اسقیطس, Serres سیرس,
Pancratius پنکراتیس, Taormina تاورمینا, Paphnutius پفنوتیس, Gregory the Fifth
گریگوری پنجم, Dimitsana دیمیتسانا, the Peloponnese پیلوپونیس, the Phanar فنار,
Odessa اودیسا, Patrick پیٹرک, and his three presbyters اکاکیوس، مینینڈر اور
پولیئنوس - all the site's own. The menaia are عبادت کی کتابیں, described
rather than transliterated, as the Areopagite's titles were.

## Solovki, and the Moscow metropolitan

Solovki is سولوفکی, the vocabulary's two entries against the commemorations'
سولووکی; Tver تویر, the oprichnik اوپریچنک, Feodor Kolychev فیودور کولیچیو,
Philosophos فلوسوفوس, Phocas فوکاس, Sinope سنوپے. Philip of Moscow is فلپ, as
his own commemoration has him; the entry for his relics writes فلپس and is
left alone.

The words heard at the Liturgy that sent him north are the edition's: کوئی
خادم دو مالکوں کی خدمت نہیں کر سکتا, Matthew 6:24. Achillas, Otroch, Malyuta
Skuratov, Alexei, Ornatsky, Petrograd and Bolshevik had no form: اکیلاس,
اوتروچ, مالیوتا سکوراتوف, الیکسی, اورناتسکی, پیتروگراد, بالشویک.

## A check the appender does not make

`loop.py --append` rejects the forbidden dashes and quotes and enforces the
script range, but a truncated multi-byte character can still pass. One slipped
into a block this session and was caught by counting ASCII full stops in the
batch file before appending, since the lives use only the Arabic full stop.
Two greps are worth running on every block file from here on: the forbidden
set, and `". "`.

Solovki سولوفکی and Uglich اوگلچ both follow the vocabulary against the
commemorations. Bucolus بوکولس, Proterius پروتیریس, Flavian فلاویان, Publius
پبلیس, Malta مالٹا, Sadoc صادوق - an Arabic-script name the commemorations
give him rather than a transliteration - Seraphim سیرافیم (سموئیلووچ),
Poltava پولتاوا. Timothy the Cat is تیمتھیس، جو بلا کہلاتا تھا, the byname
translated as the entry translates it; a locum tenens is قائم مقام.

## The Persian and Roman companies

Seleucia-Ctesiphon is سلوکیہ-طیسفون, Usthazanes اوستھازانیس - the vocabulary
has both استزانیس and اوستھازانیس, and the fuller form is the one the lives
use - Hegesippus ہیجیسیپوس, Sisinius سسینیس, Cyriacus کیریاکس, Terence ٹیرنس,
Lycaonia لکانیہ, Silvanus سلوانس. Ananias the presbyter is حننیاہ, which the
commemorations give the Phoenician presbyter of that name and the Scripture
gives the man of Damascus.

Phaeno, Clopas, Pella, Atticus, Abdechalas, Pusicius, Smaragdus, Largus,
Apronian, Crescentian, Maurus, Lucina and Artemia had no form: فائنو, کلوپاس,
پیلا, اتیکس, ابدیخلاس, پوسیکیس, سماراگدس, لارگس, اپرونیان, کریسینتیان, ماورس,
لوسینا, ارتیمیا.

## Cyrenia, and the Prologue

Cyrenia is کیرینیا, the vocabulary's two place-lines against the
commemorations' کرینیا; the Prologue is پرولوگ, which the vocabulary already
writes of the two Serbian bishops who carried it. Therapon تھیراپون,
Theopemptus تھیوپیمپتس, Theonas تھیوناس, Theodotus تھیوڈوتس, Philippa فلپا,
Dioscorus ڈیوسکورس, Socrates سقراط - the received Urdu name of the
philosopher, which the vocabulary gives this martyr too. An ambo is منبر, the
word the lives already use of a pulpit.

## Zeno of Verona, and a whole icon carried over

The vocabulary already draws Zeno with his fishing rod, his line of
catechumens, the Adige and the flood held at his church door; the life takes
those words. Verona ویرونا, the Adige ادیجے, San Zeno سان زینو, Gregory the
Dialogist گریگوری مکالمہ نگار, Urban اربن, Cecilia سیسیلیا, Vitalius وٹالیس,
Ravenna راونا, Lydia لیدیا, Timothy of Prusa تیمتھی - the shorter form his own
commemoration gives him, against the تیمتھیس of the apostle.

A fisher of men is **آدم گیر**, which is the received Urdu of the Gospel's
phrase; Alexander Severus had no form and is الیگزینڈر سیویرس.

## Myra is میرا, Cilicia کلیکیا

Both are settled by the larger count and both differ from a single entry:
Nicander's commemoration writes مائرا and Zenobius' writes کلیکیہ, while the
vocabulary and the other commemorations write میرا and کلیکیا. The lives use
the majority, as with Iconium and Adrianopolis.

Zenobius زینوبیوس and Zenobia زینوبیا, Aegae ایگائی, Akepsimas اکیپسیماس,
Aeithalas ایتھالاس, Snandulia سنندولیا, Nicander نکندر, Hermas ہرماس, Pionius
پیونیس, Limnus لمنس, Sabina سبینا, Asclepiades اسکلیپیادیس - all the site's
own. Licius, Naesson, Libanius and Polemon had no form: لیکیس, نیسون,
لیبانیس, پولیمون; the agora is بازار.

## Cyzicus is کیزیکس

Three spellings are on the site - کیزیکس in the vocabulary, کزیکس and کزیکوس
in the commemorations - and the vocabulary's is used. Parium is پاریم,
Erasmus ایراسمس, Formia فورمیا, Campania کیمپانیا, Emilian ایمیلیان. The
seven of the Corinthian company keep the commemorations' spellings, except
that Sosthenes is سوستھینس as his own entry has him, not the سوستھنیس of the
list.

Argyropolis, Diospolis, Adriaca, Dyrrhachium, Mount Lebanon and Elmo had no
form: ارگیروپولس, دیوسپولس, ادریاکا, دورّاکیم, کوہِ لبنان, ایلمو.

## Rulers and their titles, batch forty-five

Six names written here for the first time, each settled the way the rest have
been: from the site's own bodies where they appear, and from the ear of the
published Urdu Scripture where they do not.

| English | Urdu | settled from |
|---|---|---|
| Justin I | جسٹن اول | the ordinal form the commemorations use for regnal numbers |
| Ashot | اشوت | transliteration; Georgian short o, no long vowel |
| Kuropalates | کوروپالاتیس | Greek court title, carried as the calendar carries Greek titles |
| Bagratid | باگراتی | the dynastic adjective, formed as the site forms others |
| Murad | مراد | already an Urdu word; no transliteration needed |
| Vitus | ویتس | Latin -us as ـس, as the vocabulary does throughout |

Vidovdan stays ودوودان, the form the commemorations already carry, and is not
translated: it is the day's name in Serbian and the calendar treats it as one.

The rank order held again in this batch. A ruler who is a martyr is named by
his martyrdom and his crown together where the English entry gives both, but
the crown does not displace the rank: Lazar is great-martyr first, prince
second, because the Church commemorates him for the death and not the throne.

## Edessa, and a name the commemorations settle against the vocabulary

The vocabulary writes اڈیسا nine times; the commemorations write ایڈیسا four
times and the day entries once, and the vocabulary itself has ایڈیسا three
times besides. Nine against eight is no majority, and the tie goes the way the
order already set: the commemorations outrank the vocabulary, and the
commemoration of these three confessors is itself
ایڈیسا کے مقدس شہداء اور اقراری گوریاس، سموناس اور حبیبس. So **ایڈیسا**.

## Elizabeth is two names here, and they are not interchangeable

The mother of the Forerunner is **الیشبع**. The prayer for a woman in
childbirth calls her that, and the prayers decide; the vocabulary agrees
twice, in her own day line and in that of her sister Anna. **الزبتھ** is the
Russian name and belongs to the New Martyr Grand Duchess, whom the vocabulary
and the commemorations name that way and no other. One commemoration does give
the Forerunner's mother الزبتھ; it loses to the prayers.

The same division holds for her husband. **زکریا** is the Forerunner's father
- five vocabulary lines, among them the icon of the altar of incense, and his
own commemoration - and **زکریاہ** is the prophet Zechariah son of Berechiah,
which is the form the published Urdu Scripture uses for that prophet as well.

## The divine name in the Old Testament edition

The Urdu Old Testament published here renders the Tetragrammaton **یاہوہ**.
Nothing else on this site does: across the prayers, the commemorations, the
glossary, the vocabulary and the day entries the count is 670 for خداوند and
none at all for the other. The edition is not corrected, and it is not carried
across either. Where a verse the entry needs contains the divine name, the
life quotes the part that does not and reports the rest in its own prose, as
Malachi's promise of Elijah is reported here. Where the verse says خداوند, as
Malachi 3:1 does, it is quoted as it stands.

Malachi 1:11, 3:1 and 4:2 are woven in from the edition with its pointing and
its quotation marks dropped, which is what the lives have done with received
wording from the first. From the New Testament: Luke 1:6, 1:17, 1:63 and 1:80,
and Matthew 23:35, whose بیت المقدس اور قربان گاہ کے درمیان is kept as the
edition prints it although the site's own word for the Temple is ہیکل.

Elim ایلم, Horeb حورب, the twelve springs and seventy palms
پانی کے بارہ چشمے اور کھجور کے ستر درخت, all from Exodus 15:27 and 3:1.

## The fathers of Sinai and Raithu, and an opening that had to carry the rank

Written for the first time: Ammonius امونیس, the Blemmyes بلیمی, Batu باتو,
Domnus دومنس. Isaiah the monk is اشعیا, not the prophet's یسعیاہ; Sabbas
ساباس; Hypatius ہپاتیس and Eusebius یوسیبیس, the commemorations' forms rather
than the vocabulary's ہیپاتیوس and یوسیبیوس; Elias ایلیاس, Macarius مکاریس,
Mark مرقس, Benjamin بنیامین, Sergius سرجیئس.

The opening first read مقدس باپ and was named as a review. The commemoration
itself says مقدس راہب آباء, and it is right: these are monastics killed at
prayer, and the rank is the whole point of the day. The commemoration's own
wording now opens the life.

## Psalm 50 is published here, and it settles three names at once

The Midnight Office prints the fiftieth psalm entire, with its superscription:
داؤد کا زبور ... جب داؤد کے بت سبع کے ساتھ زنا کرنے کے بعد ناتن نبی اُس کے
پاس آیا, and then اے اللہ، اپنی شفقت کے مطابق مجھ پر مہربانی کر. That is the
prayers speaking, so David is **داؤد**, Bathsheba **بت سبع** and Nathan
**ناتن**, and the psalm's first line in David's life is the line the reader
already prays. The Old Testament edition writes داویؔد and the prayers do
not; the prayers decide, as they always do here.

The rest of David comes from the Scripture with the same one substitution the
rule has always allowed for a saint's own name: Jesse یشائی, Samuel شموایل,
Saul شاؤل, Goliath گولیت, Hebron حبرون, all as the edition prints them. Where
a verse carries the divine name - the Lord looks on the heart, the name of the
Lord of hosts, the dancing before the ark - the life reports it in its own
prose, as the last batch settled.

Moses keeps موسیٰ against the edition's موشہ, which was corrected in these
lives once already. Numbers 12:3 and Deuteronomy 34:6 and 34:7 are quoted:
روئے زمین کے ہر شخص سے زیادہ حلیم, آج کے دن تک کوئی نہیں جانتا کہ اس کی قبر
کہاں ہے, ایک سو بیس برس. The books are خروج and استثنا, the Psalter زبور,
Levi لاوی, Nebo کوہِ نبو, Horeb حورب.

## Joseph the Betrothed, and the four brothers

The commemorations call him **راستباز منگیتر یوسف** and the vocabulary agrees
four times; the Scripture's یوسیف is the edition's spelling of the same name
and does not travel. Matthew 1:19, 1:24, 1:25 and 13:55 and Luke 2:48 are
woven in: چپکے سے طلاق دینے کا ارادہ, اپنی بیوی کو گھر لے آیا,
بچے کا نام یسوع رکھا, کیا یہ بڑھئی کا بیٹا نہیں. Luke 1:32 gives the throne
of his father David and Mark 10:47 the cry ابن داؤد, both with the site's
داؤد for the edition's داویؔد.

James یعقوب, Simon شمعون and Jude یہوداہ are the site's own forms. **Joses**
had none. The edition spells him یوسیف, the same as Joseph, which would put
father and son under one name in a sentence that lists them apart, so he is
**یوسیس**, on the pattern the vocabulary uses for every other Greek name in
ـس.

## Diomedes and Theodosia

Diomedes is **ڈیومیڈیس**, his own commemoration's form, against the
vocabulary's single دیومیدیس; the commemorations outrank the vocabulary, as
Edessa settled. Tarsus ترسس, Cilicia کلیکیا, Nicaea نیقیہ, Bithynia بتھینیا.
The Mystery of Holy Unction is **مقدس مسح کا بھید**, from the glossary's own
two entries, مُقدّس مسح and بھید.

Theodosia's icon line was already written, and the life takes its shape from
it: اٹھارہ برس کی ایک کنواری جو عدالت کے سامنے زنجیروں میں جکڑے معترفین کو
جھک کر سلام کر رہی ہے. Tyre is **صور**, which the prayers use twenty-nine
times. Eusebius of Caesarea keeps the vocabulary's **یوسیبیوس**, which is
written twice of him by name; the monk of Sinai in the batch before took the
commemorations' یوسیبیس. Two men, two settled forms, and neither is guessed.
Urbanus, who had none, is **اربانس**.

## The unmercenaries have three names here, and each life takes its own

The site carries three phrases for the order: **بے غرض معالج** twenty-four
times in the vocabulary and three in the commemorations, **بلامعاوضہ طبیب**
four times in the commemorations and never in the vocabulary, and
**بے اجرت طبیب** three times across both. That is not a contest one form wins
outright, and it does not need to be. The standing term in the site's own
prose is بے غرض معالج, so the lives use it when they speak of the calling; and
each life opens with the phrase its own commemoration uses, because that is
the line a reader met on the day. So Cosmas and Damian of Mesopotamia, Cosmas
and Damian at Rome, and Cyrus and John all open with بلامعاوضہ طبیب, Diomedes
opened with بے اجرت طبیب in the batch before, and all four say بے غرض معالج
when the sentence turns to what the order is.

## Chrysostom, settled by the prayers

**سنہری دہن** against زریں دہن. The vocabulary has it thirty-four times to
four, the commemorations go the other way five to none, and the prayers, which
decide, have سنہری دہن three times and the other once.

## Names of this batch

From the site: Olympias اولمپیاس, deaconess شماسہ, Cosmas کوسماس, Damian
دامیان, Theodota تھیوڈوتا, Feremane فیریمانے, Cyrus سائرس, Canopus کانوپس,
Menuthis مینوتھس, Athanasia اتھاناسیا, Alexandria اسکندریہ, Arabia عرب,
Joachim یوآخیم, Anna آنا, the Golden Gate سنہری دروازہ, the Ancestors of God
خدا کے آباؤ, and the Synaxis اجتماع.

Written for the first time: Palladia پالادیا, Carinus کارینس, Theoktista
تھیوکتستا, Eudoxia یوڈوکسیا.

The whole shape of Cosmas and Damian of Mesopotamia was already in the
vocabulary before the life was written - the two brothers with their medicine
boxes and their mother at prayer above them, the common grave at Feremane
glorified with healings - and the life carries those clauses over rather than
saying the same thing a second way.

## The Mystical Supper has a name here, and the prayers give it

**پراسرار ضیافت**, from the communion prayer the site publishes:
آج مجھے قبول کر، اے خدا کے بیٹے، اپنی پراسرار ضیافت میں شریک کے طور پر. Philip
asks his question at that supper, and the life uses the reader's own words for
it rather than inventing a phrase.

## Two apostles, two spellings the site keeps apart

Philip is **فلپس**. Counting the forms that are not the other's prefix, the
vocabulary has فلپس ten times to six, the commemorations four to five, and his
own commemoration is مقدس، ہمہ ستودہ رسول فلپس. Thomas is **توما**, which is
his own commemoration's form and the Scripture's, while **تھامس** belongs to
the second Sunday of Pascha, which the site names تھامس اتوار. Both stand; the
day is not renamed to match the man, and the man is not renamed to match the
day.

John 1:43 and 1:46, 6:5, 12:21, 14:8 and 14:9 carry Philip; John 11:16, 20:25,
20:27 and 20:28 carry Thomas; and the great answers are quoted as the edition
prints them: چل کر خود ہی دیکھ لو, جس نے مجھے دیکھا ہے اس نے باپ کو دیکھا ہے,
اے میرے خداوند اور اے میرے خدا.

Names: Bethsaida بیت صیدا, Nathanael نتن ایل, Mariamne مریمنے, Bartholomew
برتلمائی (eight times in the vocabulary), Hierapolis ہیراپولس, the proconsul
پروکونسل, Mylapore مائلاپور. Domitian and Phrygia written for the first time:
دومیشین, فروجیہ. The Nativity Fast keeps the wording of Philip's own day line,
پیدائش کا روزہ، جو اس کی عید کے بعد شروع ہوتا ہے, though the glossary heading
is میلاد کا روزہ; the vigil is the glossary's رات بھر کی شب بیداری.

## Elijah, and Anna who is two names on this site

Elijah's whole life is in 3 and 4 Kingdoms and the edition supplies it:
تشبے in گلعاد, Ahab احاب, Jezebel ایزبل, Baal بعل, the ravens کوّے, the widow
of صارفت in صیدون, کوہِ کرمل and the four hundred and fifty, Horeb حورب, and
the ایک ہلکی سی دھیمی آواز which is the whole point of that mountain. Elisha
is الیشع, which the vocabulary and the commemorations both write. Where the
verse carries the divine name it is reported, as the rule stands.

Anna the Prophetess has two commemorations here and they do not agree: one
says مقدس، راستباز نبیہ آنا and the other راستباز حنّہ نبیہ، فنوایل کی بیٹی,
while the Scripture calls her حنّا. The life is written to the first, because
that is the entry it answers to, and Luke 2:36 to 38 is woven in with آنا for
the edition's حنّا, which is the same substitution every saint's own name has
had. Phanuel فنوایل, Asher آشر, Simeon شمعون.

Demetrios is **دیمیتریس**, from مُر بہانے والے سینٹ دیمیتریس; Thessaloniki
**تھیسالونیکی**, the commemorations' eight against the vocabulary's two;
Nestor **نسٹور**, the form used of this very disciple; Lyaios لیائیوس. Galerius
Maximian written for the first time: گلیریوس میکسیمین.

## Simeon's canticle comes from the evening service, not the Gospel

The site publishes the Nunc Dimittis in Compline and in Vespers, so the life
sings it as the reader sings it: اب، اے مالک، تُو اپنے بندے کو سلامتی سے رخصت
کر، اپنے کلام کے مطابق... غیر قوموں کو روشن کرنے کا نور، اور تیری امت اسرائیل
کی تمجید. The Gospel supplies what the prayers do not: Luke 2:25 and 2:26 for
the promise, and 2:34 and 2:35 for the prophecy to the Mother, including
غم کی تلوار تیری جان کو بھی چھید ڈالے گی, which is the edition's own wording.
Isaiah 7:14 is quoted for the sentence Simeon is said to have doubted.

The prophet Isaiah is **یسعیاہ** when the prophet is meant - the
commemorations and the glossary both - and **اشعیا** is the monastic name, as
the Sinai fathers took. Golgotha گلگتا, six times in the vocabulary.

## The four icons, and where their words came from

Every one of these entries already had a line in the site's own vocabulary,
and the lives are built out from those lines rather than around them: the
winged fiery Angel on the seven pillars with the Theotokos and the Forerunner
at his sides; the icon venerated at the Armatian monastery in Constantinople;
the Kasperov icon enshrined in the Kherson lands and honored at Odessa, which
it delivered in the Crimean War; the old darkened icon renewed at a grieving
woman's prayer.

Proverbs 9:1 supplies the pillars in the edition's words:
حکمت نے اپنا گھر بنا لیا؛ اس نے اپنے ساتوں ستون تراش لیے ہیں.

Names: Novgorod نووگوروڈ, the Armatian monastery ارماتی مٹھ, Kasperovo
کاسپیرووو, Kherson خرسون, Odessa اودیسا, Kholm خیلم (the Ukrainian city, which
the vocabulary distinguishes from Krasny Kholm کراسنی خولم in the Tver lands),
Volhynia وولہینیا, the Crimean War کریمیا کی جنگ, iconoclasm شبیہ شکنی, the
Seventh Ecumenical Council ساتویں عالمی کونسل.

Written for the first time: Armation ارماتیون, Armatios ارماتیوس, Zeno زینو,
Kasperova کاسپیرووا, Byzantium بازنطیم, the Unia یونیا. The last needs care:
the vocabulary already has یونیا for the Apostle Junia, so the two words are
identical on the page and only the sentence tells them apart. That is the
site's own situation in English as well, and no new spelling is invented to
avoid it.

## Five icons, and the two entries for one image

The Sweet Kissing has two commemorations on this site and therefore two lives,
and the vocabulary already had two lines for it, each with its own emphasis:
one on the monks of Philotheou receiving the icon at the shore where the
spring broke out, and one on the sea carrying it upright from the city of the
icon-breakers. The two lives are written from those two lines, so they tell
the one history from the two angles the site itself takes, rather than saying
the same sentences twice.

The image is **شیریں بوسہ**, with **گلیکوفیلوسا** beside it as the vocabulary
writes both; the Tenderness type is **نرمی**, and the Eleousa is
ایلیوسا (نرم دلی) where the vocabulary names it. Philotheou فیلوتھیو, Athos
کوہ آتھوس, Bright Week روشن ہفتہ from the glossary.

Kyiv-Bratsk کیف-براتسک, the Podil پودل, the Dnieper دنیپر, Vyshgorod ویشگوروڈ,
Lubyatov لوبیاتوف, Pskov پسکوف, Pochaiv پوچائیف, Volhynia وولہینیا, the
Footprint نقشِ قدم, Neophytos نیوفیتوس, the akathist اکاتھسٹ.

Written for the first time: Bratsky براتسکی, Victoria وکٹوریا, Symeon the
senator سیمیون, Anna Goyska آنا گوئسکا, and Ivan the Terrible
**زار ایوان ہیبتناک**. The vocabulary has ایوان for the name and simply زار
for this man in the Lubyatov line; the epithet had no form, and ہیبتناک is
the ordinary Urdu word for what the Russian actually says of him.

## Kursk, and a name that is right twice over

The commemoration calls the icon **کرسک-جڑ** and the vocabulary calls the city
**کورسک**. Both stand. The icon's name is a proper name and it is written the
way the entry the reader opened writes it; the city is a city and keeps its
own spelling. The same holds for Rzhev: the town is رژیف in the vocabulary and
the icon is رژیوسک کی والدہ خدا کا آئیکن in the commemorations, which is what
the life is called.

The Unbreakable Wall has the same doubling and it is not a conflict either.
The commemoration titles the icon **ناقابل شکست دیوار**; the vocabulary, where
it speaks of what the Mother of God is to those who take refuge in her, says
**نہ ٹوٹنے والی دیوار**. The life uses the title for the icon and the
vocabulary's phrase for the thing the title means, which is how the site
itself has the two.

Names: the Orans اورانس, mosaic پچی کاری, the apse محراب, Volokolamsk
وولوکولامسک, Volotsk وولوتسک, the Vladimir icon ولادیمیر آئیکن, Tamerlane
تیمور, the Eleousa ایلیوسا, the Passion icon آلام کا, the Strastnoy monastery
ستراستنوئے, the Hodegetria ہودیگیتریا, the Theotokos of the Sign
نشان کی والدہ خدا.

Written for the first time: Okovetskaya اوکوویتسکایا, the Tuskar توسکار,
Catherine کاترینا, and the riza قیمتی غلاف - the last described rather than
transliterated, since the site has no word for it and a reader meets the thing
before the term.

## The Annunciation troparion is reported, not quoted

No Urdu of it is published here, so the leavetaking says what the troparion
says in the site's own prose and sets no words apart as received. That is the
same treatment the katavasia of the Nativity had. What the Gospel does supply
is quoted: Luke 1:38's فرشتہ ان کے پاس سے چلا گیا and Luke 2:19's
مریم ساری باتوں کو دل میں رکھ کر ان پر غور کرتی رہیں, which is the whole point
of the day and is the edition's own wording.

The vocabulary of the calendar was already settled and the life uses it:
leavetaking **اختتام**, apodosis **عید کا اختتام**, afterfeast
**عید کے بعد کے دن**, the Annunciation **بشارت**, the synaxis **اجتماع**, the
troparion **تروپاریون**.

## The icons of this batch

Joy of All Who Sorrow تمام غمزدوں کی خوشی, with coins سکوں کے ساتھ, the Neva
نیوا; the Surety of Sinners **گناہگاروں کا ضامن**, Odrino اودرینو, the Orel
lands اوریل; the Inexhaustible Chalice **نہ ختم ہونے والا پیالہ**, Serpukhov
سرپوخوف, the Vladychny monastery ولادیچنی, Venerable Varlaam ورلام; the Kazan
icon کازان آئیکن, Saint Petersburg سینٹ پیٹرز برگ.

Written for the first time: Tula تولا, and the moleben, which is
**دعا کی خدمت**. The site has no transliteration for it and the glossary does
not carry the word; a reader meets a service of prayer, and that is what the
life calls it, on the same reasoning that gave the riza a description rather
than a name.

## Five leavetakings, and the words the calendar already had

Nothing new had to be invented for these. The feasts are named as the
commemorations name them: خدا کی ماں کی وفات کا اختتام,
قیمتی اور حیات بخش صلیب کی عالمگیر سربلندی,
نہایت مقدس تھیوٹوکوس کے ہیکل میں داخلے کا اختتام, خداوند کی ہیکل میں ملاقات,
خداوند کا ختنہ. The apodosis is عید کا اختتام, the Triodion ترودیون, the
katavasia کاتاواسیا, the canon کانون, the Magi مجوسی, the Holy of Holies
پاک ترین مقام as Exodus 26:33 has it.

Galatians 6:14 is quoted whole for the Cross, as the edition prints it, and
Matthew 1:23 gives عمانوایل with its own gloss خدا ہمارے ساتھ; Matthew 2:12
gives the Magi's other way. Simeon's line comes from Compline, where the site
publishes it, and the katavasia of the Nativity is reported rather than quoted,
which is where that rule was first set.

## Theophany water, and two martyrs

The Great Agiasma had no name here. The glossary calls the Theophany blessing
**پانی کی بڑی برکت**, so the life says برکت پایا ہوا پانی and names the
blessing once, which keeps the reader's own word without inventing a term for
the water itself.

The Transfiguration keeps the division the doc set: **تجلّی** as the feast,
which is its commemoration's name, and صورت بدل گئی in the narrative, which
is Matthew 17:2. Matthew 17:5 supplies the Father's witness. Theophany as a
feast is **تجلّیِ الٰہی**.

Aboudimos ابودیموس and Tenedos تینیدوس come from his commemoration; Troy and
the Aegean had no form and are ٹرائے and بحیرۂ ایجیئن. Abraham of Bulgaria
ابراہیم, Bolgar بولگار, the Volga وولگا, Suzdal سوزدال and the Knyaginin
monastery کنیاگینن all stood already, and the vocabulary's line about the
translation of 1230 is carried into the life whole. The Kama had no form:
کاما. George Vsevolodovich is جارج ویسیوولودووچ, built from the ویسیوولود the
commemorations already carry.

## Decius, Palermo, and the executioner's block

Decius is **دیسیس**: five in the vocabulary and one in the commemorations
against four for دیقیوس. Palermo is **پالیرمو** in Agatha's own commemoration
and her day entry, against پالرمو three times in the vocabulary; the
commemoration wins, as Edessa settled. Maximian **میکسیمیان**, the centurion
**صوبیدار**, twelve times in the vocabulary.

Acacius's life first said بلاک for the executioner's block, which is an
English word wearing Urdu letters and says nothing to a reader who has not met
it. It was written out before the batch was appended: the thanksgiving is made
تلوار کے نیچے, and the rank he attained is the one he received
قتل کی جگہ پر. Where a thing has no name here, describe it in the language
rather than borrow a word the language has not borrowed - the same decision
that gave the riza and the moleben their phrases.

Written for the first time: Firmus فرمس, the Martesian regiment مارتیسی,
Perinthus پیرینتھس, Calabria کالابریا, Quintianus کوئنتیانوس, Aphrodisia
افروڈیسیا, Paulina پاؤلینا, Eutolmius یوتولمیوس, Theoprepius تھیوپریپیس,
Acindynus اکندینس, Pontus پونتوس, Agathocleia اگاتھوکلیہ, Agathonicus
اگاتھونیکس, Agrippina اگرپینا. From the site: Catania کاتانیا, Etna ایتنا,
Mineo مینیو, Selymbria سیلمبریا, Thrace تھریس, Chalcedon کلقیدون, Zoticus
زوتیکس, Acacius اکاکیس.

## A persecutor's name is not a saint's name

Alexandra's commemoration writes the emperor **ڈایوکلیشن**; the vocabulary
writes **دیوکلیشین** four times and every life so far has followed it. The
rule that lets a saint's own name override the edition does not reach here,
because Diocletian is not a saint and this is not his entry: he is a name
inside someone else's life, and inside a life the site's standing form wins.
So Alexandra's opening names her rank and her husband without repeating the
one-off spelling: مقدس شہید ملکہ الیگزینڈرا، جسے روایت خود دیوکلیشین کی بیوی
کہتی ہے.

## The fuller, and the two entries for him

Anastasius has two commemorations here, identical in wording, and the site's
own vocabulary spells his benefactress two ways, once **اسکلیپیا** and once
**اسکالوپیا**, because the English entries do. Neither is corrected: each life
keeps the name its own entry gives, which is what the site publishes and what
a reader comparing the two days will see. The fuller himself is **دھوبی**,
which is the vocabulary's word for the trade and for his title, and his icon
line - the cross painted openly on the door, the stone and the sea waiting -
is carried into both lives.

Revelation 7:14 closes the second: اپنا جامہ برّہ کے خون میں دھو کر سفید کر
لیا, the edition's own words, which say of the martyr exactly what his trade
did for a living. Acts 7:56 gives Stephen استفنس and the opened heaven.

Aithalas ایتھالاس, Sapor شاپور, Persia فارس, Ananias حننیاہ, Salona سالونا,
Dalmatia ڈلمیشیا, Aquileia اکویلیا, the Great Martyr George عظیم شہید جارج -
all standing forms.

## A correction: Thessaloniki, against a decision already written down

Batch forty-nine gave Demetrios تھیسالونیکی on a count of the commemorations
alone. That was wrong, and this document already said so: تھسلنیکے is the
vocabulary's form twenty-four times and the New Testament's at Acts 17:1, and
the rule is that where the Scripture and the larger body agree the stray is
left where it is printed. All four occurrences in the lives were corrected to
**تھسلنیکے**. Counting one body is not counting; the decision was on this page
and should have been read before the count was made.

## Anna of Constantinople is a nun before she is a martyr

Her commemoration says only شہید آنا, but the index types her a nun and the
rank check named the opening as a review. She was tonsured by Stephen the New
and died in prison for refusing to slander him, so the monastic word comes
first: مقدس راہبہ اور شہید آنا. This is the same finding the abbots of Sinai
gave, and the rule holds - where a saint's order is monastic, the life says so
in its first breath even when the commemoration is shorter.

## Names of this batch

Gideon is **جدعون**, the commemoration's form, against the Old Testament
edition's گدعون. The rule that overrides a commemoration needs the Scripture
and the vocabulary together, as Gamaliel had; here the vocabulary is silent,
so the entry a reader would find in the calendar decides.

Stratelates سٹراٹیلیٹس, Mount Taurus کوہ طوروس, Cilicia کلیکیا, Tarsus ترسس,
Stephen the New نیا سینٹ اسٹیفن, Mount Auxentius کوہ اوکسینتیس, Ambrose of
Milan میلان کا سینٹ ایمبروز, Arian آریوسی, Nicaea نیقیہ, Alexandria اسکندریہ.
Anthusa's icon line - the Roman matron refusing the Arian rite, the fire
kindled behind her, Ambrose blessing from afar - is carried into her life.

Written for the first time: Copronymus کوپرونیمس, Trichinarion تریخیناریون,
Sunilda سونیلدا.

## Counting all five bodies, every time

The Thessaloniki correction is now the method, and it decided two names here.
Sebaste is **سیباستے** - fourteen in the vocabulary, one in the commemorations
and one in the day entries, against سبسطیہ five times in the commemorations
alone, among them Antiochus's own. Byblos is **بیبلوس**, four in the
vocabulary including Aquilina's own icon line, against a single بائبلوس in
her commemoration. A commemoration outranks the vocabulary where the two are
close, as Edessa was; it does not outrank it three and four to one.

Antiochus is **انطیوکس**, and the prayers have him once, which settles it
without a count. Platon is **افلاطون**, Aquilina **اکویلینا**, the actor
**اداکار**, the theater **تماشا گاہ** - all the site's own.

## Names of this batch

Archil آرچل and Kartli کارتلی from his commemoration and the vocabulary;
Nicaea نیقیہ, Bithynia بتھینیا, Phoenicia فینیکے, the caliph خلیفہ, the
Caucasus قفقاز.

Written for the first time: Antonina انتونینا, Volusian وولوسیان, Murvan the
Deaf **مروان بہرا**, Ardalion اردالیون, Maximian Galerius میکسیمیان گلیریوس.

Ardalion's life first said اسٹیج for the stage machinery. The vocabulary
already had the whole picture in Urdu - مذاق کے تماشے کی رسیوں پر معلق - so
the life uses تماشے کی رسیاں and the borrowed word came out before the batch
was appended. That is the second time in three batches; the check is now part
of the reading, not an accident.

## A second correction: Phrygia

Batch forty-nine wrote **فروجیہ** for Phrygia at Hierapolis. That form appears
nowhere on this site. The vocabulary has **فروگیہ** twelve times and the
commemorations فریجیا twice; the invented spelling was corrected to فروگیہ,
which the count settles and which Ariadne's own Prymnessus line already
carries. Neither of the two corrections this session was caught by a script:
both came from counting the site before writing, which is the only check there
is.

Brest is **بریست**, four times in the vocabulary, and not the بریتسک of the
commemoration, which is the English key's own spelling carried across.

## Athanasius of Brest opens as a monastic

His commemoration says مٹھ کے سربراہ, which is the office and not the rank the
check looks for. He was tonsured at Vilna and ordained hieromonk, so the life
opens مقدس راہب اور کاہن شہید اتھاناسیس، بریست کے مٹھ کا سربراہ. Same finding
as Anna's and the Sinai fathers'; the rule is now three times proved.

Timothy is **تیمتھی** for this disciple, which both his commemoration and the
vocabulary line for Babylas write, though تیمتھیس is the commoner form
elsewhere on the site for other men of the name.

Names from the site: Najran نجران, Ethiopia ایتھوپیا, Elesbaan ایلسبان,
Prymnessus پریمنیسوس, Antinoe انتینوئے, the Thebaid تھیبائیڈ, the Nile
دریائے نیل, Sicily سسلی, Agapius اگاپیس, Vilna ولنا.

Written for the first time: Arethas اریتھاس, Dunaan دوناان, the Himyarites
حمیری, Justin جسٹن, Ariadne آریادنے, Tertullus ترتلوس, Hadrian ہادریان,
Asclas اسکلاس, Arrian آریان, Philippovich فیلیپووچ, Babylas بابیلاس. The Sejm
is **شاہی مجلس**, described rather than transliterated, as the riza and the
moleben were.

## Basil, settled by the prayers, and Ancyra by the vocabulary

**باسل**, not بازل. The two forms are almost level across the site - thirty-six
against thirty-three - but the prayers print سینٹ باسل اعظم twice and بازل
never, and the prayers decide. The lives had already used باسل twenty-five
times; the one بازل, in the leavetaking of the Nativity, was corrected.

Ancyra is **انقرہ**: seventeen in the vocabulary against eleven for انکیرا
across the commemorations and the day entries. The vocabulary is the larger
body here and it is not close, which is the Thessaloniki rule again.

## Names of this batch

From the site: Morea موریا, Bacchus باخوس, Callimachus کالیماخوس, Dionysius
ڈیونیسیس, the censer بخوردان, Romanus رومانس, Asclepiades اسکلیپیادیس, Comana
کومانا, Basiliscus باسیلسکس, Theodore the Recruit تھیوڈور نوآموز سپاہی,
Eutropius یوٹروپیس, Cleonicus کلیونیکس, Agrippa اگریپا, Julian the Apostate
مرتد جولین, Galatia گلتیہ, Pontus پونتوس.

Barbarus's whole scene was already in the vocabulary - the victorious champion
refusing the sacrifice of his own triumph, the three soldiers believing at the
sight, four crowns on one refusal - and the life carries those clauses rather
than saying it a second way. So is Basiliscus's leave-taking from his mother
and his shrine at Comana where he would welcome the exiled Chrysostom.

Matthew 21:16 supplies the last line of Barulas: بچوں اور شیرخواروں کے لبوں سے
بھی اپنی حمد کروائی, the edition's own words for the psalm it quotes.

Written for the first time: Barbarus باربارس, Barlaam برلام, Barulas بارولاس.

## Edessa has a third spelling, and it is left where it is printed

Bassa's commemoration writes **ایدیسا**, which appears nowhere else on the
site. Edessa was settled at **ایڈیسا** for the confessors Gurias, Samonas and
Habibus, and the lives keep that form, so the two entries agree with each
other and with the eight places the site already uses it. The stray is not
copied and not corrected; it is simply not followed, which is what the rule
about strays has said since Thessalonica.

Aglaida is **اگلائیدا**, three times in the vocabulary, and not the اگلائیا of
her commemoration, which follows the English key's spelling rather than the
body of the entry. Tarsus stays **ترسس**, the vocabulary's, against the
commemoration's ترسوس.

## Names of this batch

From the site: Macedonia مکدنیہ, Zeus زیوس, Boniface بونیفیس, Callinicus
کالینیکس, Gangra گنگرا, Galatia گلتیہ, Amisos امیسوس, Charitina خریتینا,
Callistratus کالسٹراٹس, Claudius کلاڈیس, Carthage کارتھیج.

Pontius Pilate is **پونطیس پیلاطس**, from Matthew 27:2 where the edition
writes پیلاطس; the first name had no form here.

Written for the first time: Bassa باسا, Theognis تھیوگنس, Pistus پسٹس,
Sacerdon ساسردون, Neochorus نیوخورس, Dometius دومیتیس - the governor, not the
disciple of Dionysiou, whom the vocabulary already writes the same way.

## Three more spellings settled by the same count

Lycia is **لیکیا** - twenty-four in the vocabulary and twelve in the
commemorations - against the لوکیا of Christopher's own entry. Aegae is
**ایگائی**, four vocabulary lines against the commemoration's ایگے. Asterius
is **استیریوس**, four against the commemoration's اسٹیریس. In each case the
commemoration is alone and the rest of the site is not; a commemoration decides
a near tie and nothing more.

Leontius is **لیونٹیس** and Serapion **سراپیون**, both the larger form.

## Names of this batch

Christina کرسٹینا, Christodoulos کرسٹودولوس, Christopher کرسٹوفر, Chronides
کرونیدیس, Callinica کالینیکا, Aquilina اکویلینا, Theonilla تھیونیلا, Neon
نیون, Claudius کلاڈیس, Seleucus سیلیوکس, Stratonicus ستراتونیکس, Urban اربن,
Tyre صور, Decius دیسیس. The Christ-bearer is **مسیح بردار**, which the
vocabulary already writes of this saint's earned name.

Written for the first time: Lysias لوسیاس.

1 Corinthians 6:20 gives Christodoulos his one quoted line, قیمت سے خریدا گیا,
which is what his name says of him and what the Apostle says of everyone.

## Isauria, Cyrene, and a place the site spells two ways once each

Isauria is **اسوریہ**, nine in the vocabulary against اسوریا twice in the
commemorations. Cyrene is **کرینے**, the vocabulary's two place-lines, against
the commemoration's سائرین. Macedonia keeps **مکدنیہ**, settled long ago from
the vocabulary and Acts 16:12, and Danax's commemoration مقدونیہ is another
stray of the kind that is not followed.

Ascalon is the rare case where the count is one to one: **اشقلون** in the
place-line, **اسقلون** in Cyril's own icon line. The life uses the icon line's
form, because that line is about these very martyrs and the life is built out
from it.

## Names of this batch

From the site: Conon کونون, Myra میرا, Lycia لیکیا, Heliopolis ہیلیوپولس,
Gaza غزہ, Auleneia اولینیا, the reader قاری, the chalice پیالہ, Nestor نسٹور,
Anna آنا, the Archangel Michael سردار فرشتہ میکائیل.

Conon's icon line was already written whole - the martyr of Isauria with the
Archangel above him, the demons sealed in clay vessels at his feet, the wedding
candle of his parable in his hand - and so was Crescens's, the noble elder of
Myra refusing even to feign the sacrifice while the pyre spares a hair of his
head. Both lives take those clauses as they stand.

Written for the first time: Badine بادینے, Nada نادا, Crescens کریسکنس,
Cyrilla سیریلا, Danax داناکس. The paten had no word here and is **طشتری**, the
ordinary Urdu for the dish it is, beside the vocabulary's پیالہ for the
chalice.

## Second Maccabees is not published here

The site's Urdu Old Testament carries thirty-nine books; the deuterocanon is
in the index but not in `scripture/ur`. So Eleazar's account is told in the
site's own prose and the book is simply named, **مکابیوں کی دوسری کتاب**,
built from the vocabulary's مکابی. Nothing is set apart as received, which is
the rule wherever no Urdu of a text is published.

The baptismal words Drosis said over herself are the prayers' own opening
formula, باپ اور بیٹے اور روح القدس کے نام سے, which every reader of this site
already says; Matthew 3:9 closes her life with the edition's پتھروں سے بھی
حضرت ابراہام کے لیے اولاد.

## Names of this batch

From the site: Nisibis نصیبین, Cyrrhus کوروس, Anazarbus انازاربس, Trajan
ٹریجن, Dabuda دابودا, Eleazar الیعزر, the Maccabees مکابی, the archimandrite
آرکمنڈرائٹ, the catechumen نو مرید, Thrace تھریس, Persia فارس.

Written for the first time: Uaros واروس, Urbelos اربیلوس, Amapas اماپاس,
Domnina دومنینا, Drosis دروسس, Antiochus Epiphanes انطیوکس ایپیفانیس - the
first name being the انطیوکس the prayers already carry, so only the epithet is
new.

## Silistra and Dorostolum, both kept

Emilian's commemoration calls the place **سلسٹریا** and the vocabulary calls
it **دوروستولم (سلسترا)**. Both stand and neither is a stray: the ancient city
is دوروستولم, which is what the life narrates in, and the modern town is the
name the commemoration gives, which is where the reader finds the day. The
vocabulary's own line already prints the two together.

## Names of this batch

From the site: the chamberlain خاص خادم (کوبیکولاریوس), the Danube ڈینیوب,
Theodotus تھیوڈوتس, Germanus جرمانس, Anatolia اناطولیہ, Sapor شاپور, the
Samaritan سامری, Fortune قسمت, Hadrian ہادریان, Trajan ٹریجن.

Eupsychius's icon line was already whole - the young bridegroom leading the
Christians of Caesarea against the temple of Fortune, the wedding garment
exchanged within days for the martyr's crown, and Basil the Great behind him
keeping his feast - and the life is built out from it.

Written for the first time: Eleutherius ایلیوتھیریس, Emilian ایمیلیان,
Capitolinus کاپیتولینوس, Eudokia یودوکیا, Baalbek بعلبک, Philostrates
فیلوستراتیس, Vicentius ویسینتیوس, Eupsychius یوپسیکیس. The panegyris had no
form here and is **جشن**, described rather than transliterated; the site has
اکاتھسٹ and کاتاواسیا for parts of the service books, but a yearly festival is
a plain thing and takes the plain word.

## The Gareji martyrs are monastics before they are new martyrs

The opening said only مقدس نئے شہید and was named as a review. They are the
brotherhood of a lavra, killed in their own monastery, so the life now opens
مقدس راہب اور نئے شہید. Fourth time this rule has been proved, after the Sinai
fathers, Anna of Constantinople and Athanasius of Brest; where the index types
a saint monastic, the first breath of the life says so.

Gareji is **ڈیوڈ گاریجی**, which the place-lines and the commemoration write,
against the داؤد گاریجی of one icon line; the saint who founded it keeps ڈیوڈ
here because that is how the monastery is named on this site, and the life
follows the monastery.

Paphlagonia is **پفلاگونیا**, four vocabulary place-lines against the
commemoration's پافلاگونیا; Thessalonica keeps **تھسلنیکے**, the settled form,
against another commemoration's stray.

## Names of this batch

From the site: Publius پبلیس, Silvanus سلوانس, Otar اوتار, Ancyra انقرہ,
Edessa ایڈیسا, Mesopotamia میسوپوٹیمیا, Basiliscus باسیلسکس, Constantine the
Great قسطنطین اعظم.

Written for the first time: Eusignius یوسگنیس, Constantius Chlorus
کونستانتیوس کلوروس, Felicitas فیلیسیتاس, Januarius یانواریس, Felix فیلکس,
Vitalis ویتالس, Martial مارتیالیس, Marcus Aurelius مارکس اوریلیس, Florentius
فلورنٹیس, Gemellus گیمیلس, Gerontius جیرونٹیس, Bessarion بیساریون, Dagestani
داغستانی. A hierodeacon is **راہب شماس**, formed on the site's own راہب کاہن.

## Names of this batch

From the site: Gobron گوبرون, the Kveli fortress کویلی کا قلعہ, the emir امیر,
Gorazd گورازد, Prague پراگ, Moravia موراویا, Methodius میتھوڈیس, Cyril سیرل,
Gordius گورڈیس, Corinth کرنتھس, Athena ایتھینا, Aurelian اورلیان, Antoninus
انتونینس, Comana کومانا, the sorcerer جادوگر, Matthias متیاس.

Heliconis keeps **تھسلنیکے** against her commemoration's تھیسالونیکی, and her
icon line already uses that form: تھسلنیکے کی ایک کنواری جو کرنتھس میں ایتھینا
کا بت گرا رہی ہے. The whole scene of that line - the beasts crouching harmless
at her feet, the angel comforting her in prison - is carried into the life.

Written for the first time: Silesia سلیسیا, Heydrich ہائیڈرش, Kobylisy
کوبیلیسی, Czech چیک, Slovak سلوواک, Gordian گورڈیان, Heliconis ہیلیکونس,
Hermias ہرمیاس.

## Two Irenes, and they are not merged

This martyr's own commemoration writes **آئرین**; Irene of Thessalonica, whose
sisters Agape and Chionia stand with her in the vocabulary's icon line, is
**آئرینے**. Her life names both, and keeps them apart, because that is the
question the entry itself raises: whether the two are one saint. The site's
two spellings let the sentence ask it without answering it, which is what the
menaia do.

Sebaste keeps **سیباستے** and Amastris **اماستریس**, both against a
commemoration standing alone.

## The diptych has no word here

The calendar read aloud before God is described, not named:
ناموں کا وہ ورق جو خداوند کے سامنے بلند آواز سے پڑھا جاتا ہے. As with the riza,
the moleben, the paten and the panegyris, a thing the site has never named is
told in the language rather than borrowed into it.

Philippians 4:7 supplies the peace that passes understanding in the edition's
words, جو انسان کی سمجھ سے بالکل باہر ہے, and Revelation 3:5 the name that
cannot be blotted out.

## Names of this batch

Hyacinth ہائیسنتھ and Hyacinthus ہائیسنتھس, each as his own commemoration
writes him; Irenarchus ایرینارکس, Acacius اکاکیس, Maximus میکسمس, the menaia
مینایا, Theodosia of Tyre صور کی تھیوڈوسیا, Agape اگاپے, Chionia خیونیا,
Kazan کازان, the khan خان, Eusebius of Caesarea یوسیبیوس.

## Two more borrowed words caught before the append

Juvenal's life first said انجینئر for his training and مشن for the Alaskan
mission. Neither word is on this site. He is now
کان کنی کے فن میں تربیت پائے ہوئے, and the mission is
راست ایمان مبلغانہ مہم, built from the مبلغ the vocabulary already uses of
him. That is three batches in a row where an English word reached the block
file and was written out before it reached the site; the reading pass now
looks for them by habit.

His opening also needed his rank: he is typed hieromonk, so the life opens
مقدس راہب کاہن اور شہید جووینل. Fifth proof of the same rule.

## Names of this batch

From the site: Campania کیمپانیا, Flavian فلاویان, Tarsus ترسس, Flavia
Neapolis فلاویا نیاپولس, Samaria سامریہ, Rusticus رسٹیکس, and Justin's
companions whole from their own vocabulary line - خاریتون، خاریتو،
یوایلپستوس، ہیراکس، پیون، ویلیرین اور یوستس. Nerchinsk نرچنسک, Kodiak کودیاک,
Valaam والام, Herman ہرمن, Iliamna الیامنا, Protomartyr of America
امریکہ کا اولین شہید.

Julitta is **جولیتا**, her own commemoration's form, against the vocabulary's
single یولیتا in another saint's line; one against one, and the entry decides.

Shechem is **شکیم**, which is what Acts 7:16 calls it.

Written for the first time: Antoninus Pius انتونینس پیوس, Trypho تروفو - not
the ٹریفون of the saint Tryphon, since these are two men and the site keeps
two names - Crescens the Cynic کلبی کریسکنس, Juvenal جووینل, Kenai کینائی. The
schools of philosophy are رواقی، مشائی، فیثاغورثی، افلاطونی, the ordinary Urdu
names for them.

## A commemoration with an English word in it

Laodicius's commemoration reads شہید جیلر لاودیکیس. **جیلر** is an English
word in Urdu letters and the site has its own: **داروغہ**, four times in the
vocabulary, including in the two lines written about this very man and about
Glyceria whose jailer he was. The life uses داروغہ. The rule against borrowing
does not stop at the lives; where a commemoration has borrowed and the
vocabulary has not, the vocabulary is what the site actually says.

His name is **لاؤدیکیس** for the same reason, the vocabulary's form against the
commemoration's لاودیکیس, and Asistavi is **اسیستاوی**, the vocabulary's
against اسستاوی.

## Longinus, from the four Gospels

Mark 15:39 and Matthew 27:54 give the confession as the edition prints it,
یہ شخص یقیناً خدا کا بیٹا تھا; John 19:34 the spear and the blood and water;
Matthew 28:13 the bribe at the tomb. Pilate is پونطیس پیلاطس, as Matthew 27:2
settled him.

## Names of this batch

Glyceria گلیکیریا, Heraclea ہیراکلیہ, Longinus لونگینس, the centurion صوبیدار,
Samosata ساموساتا, Drepanum دریپانم, Helenopolis ہیلینوپولس, Helen ہیلینا,
Paula پاؤلا, Claudius کلاڈیس, Hypatius ہیپاتیوس, Golgotha گلگتا, Aurelian
اورلیان - all standing forms, and Lucillian's whole company comes from the one
vocabulary line already written for them.

Written for the first time: Lucian لوسیان, Lucillian لوسیلیان, Maximinus
میکسیمینس.

## Four hundred lives

Marinus's icon line was already written whole and the life is built out from
it: ایک سپاہی بشپ کے سامنے جس کے آگے تلوار اور انجیل کی کتاب رکھی ہے، اس کا
ہاتھ انجیل پر، اور صوبیدار کا عصا پیچھے چھوڑا ہوا. So were Mamas's parents,
Manetha's companions, and Lupus twice over; by four hundred lives the
vocabulary is answering most of what a life needs before the Scripture is
opened at all.

Names from the site: Lupus لوپس, Demetrios دیمیتریس, Thessalonica تھسلنیکے,
Mamas ماماس, Theodotus تھیوڈوتس, Rufina روفینا, Paphlagonia پفلاگونیا,
Aurelian اورلیان, Manetha مانیتھا, Antoninus انتونینس, Nikephoros نکیفوروس,
Germanus جرمانس, Marinus مارینس, Asterius the senator استیریوس, Eusebius
یوسیبیوس, Maximinus میکسیمینس.

Written for the first time: Ammia امیا, Theotecnus تھیوتیکنس. The trident is
**سہ شاخہ نیزہ**, described in the language; the centurion's vine-staff is
**صوبیدار کا عصا**, which is what the vocabulary already calls it in Marinus's
own line.

## Names of this batch

Chios is **خیوس**, four times in the vocabulary against the کیوس of
Markella's commemoration; Volissos ولیسوس; Anazarbus انازاربس; Thessalonica
تھسلنیکے again, against another commemoration's stray; Matrona ماترونا, Martha
مارتھا, Markella مارکیلا, Habakkuk حبقوق, Callistus کالستس, Valentine
ویلنٹائن, Asterius استیریوس, Lysias لوسیاس.

Written for the first time: Audifax اودیفاکس, Cyrenus کیرینوس, the Tiber
دریائے تائبر, Claudius the Second کلاڈیس دوم, Pautila پاؤتیلا with the Greek
accounts' پانتیلا beside it, as the English entry gives both.

## Tver

**تویر** - seventeen in the vocabulary and two in the commemorations, against
ٹور seven and seven. Closer than most of these counts, but the vocabulary is
decisive on its own and the commemorations are split against themselves, one
of them naming this very prince's wife with تویر. The life follows the
vocabulary, and Michael's two icon lines - the prince in the stocks at the camp
of the Horde, refusing flight, his heart offered for his city - are carried in
whole.

## Names of this batch

From the site: Meletius میلیتیس, Stratelates سٹراٹیلیٹس, Galatia گلتیہ,
Serapion سراپیون, Callinicus کالینیکس, Kyriakos کیریاکوس, Menas میناس,
Cotyaeum کوتیائیوم, Phrygia فروگیہ, Mareotis ماریوتس, Mercurius مرکوریس,
Smolensk سمولینسک, the Hodegetria ہودیگیتریا, Batu باتو, the sexton
کلیسا کا خادم, the stocks کاٹھ, Mauretania موریطانیہ, Mertius مرٹیس.

Susanna is **سوسناہ**, from Luke 8:3, the edition's own spelling.

Written for the first time: Marciana مارکیانا, Palladia پالادیا (already used
of Cosmas and Damian's patient, and the same form serves), Christian کرسٹیان,
Faustus فاؤستس, Dolgomostye دولگوموستیے, Yuri یوری.

## Names of this batch

Cyzicus is **کیزیکس**, four vocabulary lines against the کزیکس of Myron's
commemoration; Thessalonica **تھسلنیکے** once more.

From the site: Tennis تینس, the emir امیر, the Saracens سراسین, Achaia اخیہ,
Antipater انتیپاتر, Hartland ہارٹ لینڈ, Devon ڈیون, Mount Olympus کوہ اولمپس,
Bithynia بتھینیا, Neophytus نیوفیتس, Nestor نسٹور, Lyaeus لیائیوس, Demetrios
دیمیتریس, Mirax میراکس, Myron میرون, Nectan نیکٹان.

Nectan's icon line was written whole - the Celtic hermit of the Devon coast
bearing his own severed head to the spring, the robbers behind him, crowned a
martyr among the saints of Britain - and so was Nestor's, the youth casting
the giant from the platform while the imprisoned Demetrios blesses him. Both
lives are built out from those lines.

Written for the first time: Brychan بریخان, Welsh ویلش, the Vandal وندال.
Florence the mother of Neophytus takes **فلورنس**, the same word the site uses
of the Italian city; the sentence tells them apart and no new spelling is
invented to keep them separate.

Matthew 21:16 closes Neophytus as it closed Barulas, in the same words.

## Names of this batch

Isauria keeps **اسوریہ** against Onesimus's commemoration, as it did against
Conon's.

From the site: Nikephoros نکیفوروس, Forgiveness Sunday معافی کا اتوار, Valerian
ویلیرین, Taormina تاورمینا, Melitene ملیتینے, Chios خیوس, Quintianus
کوئنتیانوس, Agatha اگاتھا, Decius دیسیس, Tyana تیانا, Demetrius of Rostov
روستوف کا دیمیتریس, the Five Martyrs پانچ شہید, Maximinus میکسیمینس, Conon
کونون.

Written for the first time: Nicander نکندر, Sapricius ساپریکیوس, Nikon نکون,
Ganos گانوس, Onesimus اونیسیمس with اونیسیس beside it, Orestes اوریستیس.

## Names of this batch

Lycaonia is **لکانیہ**, five vocabulary lines including Papas's own, against
the لائکونیا of his commemoration.

From the site: Barnabas برنباس, Bithynia بتھینیا, Heraclea ہیراکلیہ, Thrace
تھریس, Hadrian ہادریان, Antoninus Pius انتونینس پیوس, Decius دیسیس,
Nicomedia نیکومیڈیا.

Papas's icon line was written whole - the martyr of Lycaonia driven along the
road in sandals of nails, bound at last to a barren tree that bears fruit
above him - and the life takes it as it stands.

Matthew 10:33 gives Pancharius the sentence his mother's letter carried, in
the edition's own words.

Written for the first time: Pancharius پنکاریس, Papas پاپاس, Paramon پارامون,
Aquilinus اکوئلینس, Isis ایسس, Paraskevi پراسکیوی, Pausilippus پوسیلپس.

Paraskevi's opening needed her rank; she is typed a nun, so the life opens
مقدس راہبہ اور شہید پراسکیوی. Sixth time.

## Names of this batch

Philoumenus is **فیلومینس** and Phaedrus **فیدروس**, both the vocabulary's
forms, and both of those vocabulary lines are written about these very men;
their commemorations' فلومینس and فیدرس lose. Ancyra keeps **انقرہ**.

From the site: Peter the Aleut الیوت پطرس, the Aleuts الیوت, Kodiak کودیاک,
Herman ہرمن, Philetus فلیتس, Lydia لدیہ, Amphilochius امفیلوکیس, Cronides
کرونیدیس, the notary محرر, Illyria الیریا, Theoprepius تھیوپریپیس, Lycaonia
لکانیہ, Galatia گلتیہ, Aurelian اورلیان, Valerian ویلیرین, Felix فیلکس, the
baker نانبائی.

Peter's icon line was written whole - a young Aleut holding a cross, his
mutilated hands bound, confessing before his tormentors - and so was the whole
company of Philetus in one line; both lives take them as they stand.

Matthew 5:29 gives Philosophus his one quoted clause, that it is better a
member be lost than the whole body.

Written for the first time: Macedon میکیدون, Philosophus فلوسوفوس, California
کیلیفورنیا.

## Names of this batch

Melitene is **ملیتینے**, twelve vocabulary lines and a day entry against the
میلیتین of Polyeuktos's commemoration; Ancyra **انقرہ**; Victor **وکٹر**, five
in the vocabulary and three in the commemorations against a single وکتور;
Nearchus **نیارخس**, the form his own icon line uses.

Platon is **افلاطون**, which both his commemoration and Antiochus's vocabulary
line write of this brother.

From the site: Photini فوتینی, the Samaritan woman سامری عورت, Sebastian
سباستین, Domnina دومنینا, Carthage کارتھیج, Naples نیپلز, Felix فیلکس,
Antiochus انطیوکس, Alexandria اسکندریہ, Galatia گلتیہ.

John 4 supplies Photini's whole first scene in the edition's words: مجھے پانی
پلا, زندگی کا پانی, روح اور سچائی سے پرستش, وہ عورت پانی کا گھڑا وہیں چھوڑ کر,
and Sychar سوخار from John 4:5. Polyeuktos's icon line was already written
whole and the life takes it as it stands.

Written for the first time: Anatola اناتولا, Photo فوتو, Photis فوتس,
Paraskeva پراسکیوا, Kyriake کیریاکے, Photinus فوتینوس, Nero نیرو, Agrippinus
اگریپینس, Polycarp پولی کارپ, Polyeuktos پولیوکتوس, Paulina پاؤلینا, Potitus
پوتیتس, Epiros ایپیروس.

## Hermopolis, and a tie broken by the saint's own lines

The vocabulary writes **ہرموپولیس** twice and **ہرموپولس** twice. The two
ہرموپولیس are the icon lines written about Sabinus himself; the two ہرموپولس
are bare place-lines. The life uses ہرموپولیس, on the Ascalon principle: where
the count is level, the line written about this saint decides.

Psalm 27:10 carries the divine name, so the closing sentence of Quadratus of
Corinth reports it rather than quoting it: خواہ باپ اور ماں چھوڑ دیں، خداوند
اپنا لیتا ہے.

## Names of this batch

From the site: Quadratus کواڈراٹس, Rufina روفینا, Saturninus ساتورنینس,
Rufinus روفینس, Cyprian کپرین, Crescens کریسکنس, the Hellespont ہیلیسپونٹ,
Romanus رومانس, Barulas بارولاس, Asclepiades اسکلیپیادیس, Romulus رومولس,
Sabinus سابینس, Abibus ابیبس, Corinth کرنتھس, Nicomedia نیکومیڈیا, Trajan
ٹریجن, Armenia آرمینیا, Valerian ویلیرین, Decius دیسیس.

Sabinus's two icon lines were already written whole - the nobleman of
Hermopolis sold for two gold coins by a beggar he had fed, bound to a stone
and given to the Nile - and the life takes them as they stand.

Written for the first time: Anectus انیکتس.

## Two more borrowings written out

Savva's life first said کیریئر for his career and رجسٹر for the army's rolls.
Neither is on this site. They are now پیشہ and فہرست. That is the fourth
batch in which an English word reached the block file and was removed before
the append; the pass is working.

## Names of this batch

Sebaste keeps **سیباستے** against Severian's commemoration. Sebastian of Rome
is **سباستیان**, his own commemoration's form; the Sebastian of Jackson in the
vocabulary stays سباستین, and the two are different men.

From the site: Savva ساوا, Stratelates سٹراٹیلیٹس, the Goths گوتھ, Aurelian
اورلیان, Zoe زوئے, Lucina لوسینا, the catacombs سرنگ قبرستان, Victorinus
وکٹورینس, Claudius کلاڈیس, Serapion سراپیون, Severian سیویرین, Licinius
لیکینیس, the Forty Martyrs of Sebaste سیباستے کے چالیس شہید, Hermopolis
ہرموپولیس.

Written for the first time: Marcellinus مارسیلینس, Tranquillinus ترانکوئلینس,
Nicostratus نیکوستراتس, Castorius کاستوریس, Symphorian سمفوریان, Tiburtius
تیبورتیس, Castulus کاستولس, Achilles اکیلس, Severus سیویرس. The praetorian
guard is **شاہی محافظ دستہ**, described rather than transliterated.

## Faith, Hope and Love

Sophia's three daughters had no names on this site. They are named for the
three virtues, and 1 Corinthians 13:13 gives those three words in the
edition's own Urdu: **ایمان، امید اور محبت**. The life uses them and quotes
the verse that names them, so the daughters carry the Apostle's wording rather
than a transliteration of the Greek.

## Names of this batch

From the site: Solomonia سولومونیا, Antiochus Epiphanes انطیوکس ایپیفانیس, the
Maccabees مکابی, Sophia صوفیہ, Hadrian ہادریان, Artemis ارتیمس, Alsace الزاس,
Pompeiopolis پومپیوپولس, Tarasius تراسیس, Lycaonia لکانیہ, Cilicia کلیکیا,
Stephanida استیفانیدا, Victor وکٹر, Damascus دمشق, Marcus Aurelius
مارکس اوریلیس, Hereti ہیریتی, Georgia جارجیا, the protomartyr اولین شہید.

Written for the first time: Sozon سوزون, Shushanik شوشانیک with the
commemoration's سوسانا beside it, as the entry gives both, and Varsken وارسکن.

## Names of this batch

Terence is **تیرینس**, twice in the vocabulary including his own icon line,
against the ٹیرنس of his commemoration. Theodota keeps **تھیوڈوتا**.

From the site: Edessa ایڈیسا, Hadrian ہادریان, Apollo اپالو, Claudiopolis
کلاڈیوپولس, Urban اربن, Bithynia بتھینیا, Carthage کارتھیج, Petra پیترا,
Euphemia یوفیمیا, Theodosius تھیوڈوسیس, Nicetas نکیتاس, Anastasia اناستاسیا,
Nicaea نیقیہ, Maximus میکسمس, Zeno زینو, Macarius مکاریس.

Terence's icon line was written whole - Terence and his company before the
proconsul of Carthage, the dungeon of serpents harmless around the leaders,
forty crowns descending and the shrine at Petra receiving them - and so was
Tatiana's, the deaconess with lifted hands, the idol of Apollo shattered
behind her, her converted torturers crowned beside her and a lion at her feet.
Both lives are built out from those lines.

Mark 16:18 closes Terence in the edition's words: وہ سانپوں کو اٹھا لیں گے
اور انہیں کچھ نقصان نہ پہنچے گا.

Written for the first time: Tathuil تتھوئل, Bebaia بیبائیا, Thiphael تیفائل,
Tatiana تاتیانا, Alexander Severus الیگزینڈر سیویرس, Tation تاتیون, Africanus
افریکانس, Pompeius پومپیئس, Fortunianus فورتونیانس, Leucadius لیوکادیس,
Evodus ایوودس. A menagerie is not چڑیا گھر, which is a modern zoo; the life
says چھوڑے ہوئے جانور, which is what the proconsul actually released.

## Names of this batch

Ancyra keeps **انقرہ** against Theodotus's commemoration, and Theodotus's two
icon lines were already written - the innkeeper of Ancyra drawing the seven
drowned virgins from the lake by night with an angel guiding him, his inn
behind him where the Liturgy was served - so the life is built out from them.
The seven virgins come whole from their own vocabulary line: الیگزینڈرا،
تیکوسا، کلاڈیا، فائنے، یوفراسیا، ماترونا اور جولیا.

From the site: Theodota تھیوڈوتا, Alexander Severus الیگزینڈر سیویرس, Fronto
فرونتو, Theodula تھیودولا, Anazarbus انازاربس, Helladius ہیلاڈیس, Macarius
میکیریس, Evagrius ایواگریس, Thomais تومائس, Abba Daniel of Sketis
اسقیطس کا ابا دانیال, Timothy تیمتھی, Maura مورا, the Thebaid تھیبائیڈ, the
reader قاری, the innkeeper سرائے والا.

The governor of the Thebaid is **آریان**, the form already used of him in
Asclas's life; the English spells him Arrian there and Arianus here, and he is
one man.

Romans 8:35 gives Theodota her closing line, نہ مصیبت اور نہ تنگی, in the
edition's own words.

Written for the first time: Pelagius پیلاگیس.

## Names of this batch

Tryphaena is **تریفینا**, the vocabulary's form for her shrine at Cyzicus,
against her commemoration's ٹرائفینے. Tryphon of Kampsada is **ٹرائفون**, his
own commemoration's form; Tryphon of Pechenga in the vocabulary keeps ٹریفون,
and the two are different men, as the two Sebastians were. Lycia keeps
**لیکیا** against Trophimus's commemoration.

From the site: Troadius تروادیس, Neocaesarea نیوقیصریہ, Gregory the
Wonderworker معجزہ گر گریگوری, Pontus پونتوس, Trophimus تروفیمس, Cyzicus
کیزیکس, the Hellespont ہیلیسپونٹ, Anastasios اناستاسیوس, Kampsada کامپسادا,
Apamea اپامیہ, Phrygia فروگیہ, Aquilinus اکوئلینس, Gordian گورڈیان, Ivan the
Terrible ایوان ہیبتناک, Urpasianus اورپاسیانس, Maximian Galerius
میکسیمیان گلیریوس, the Forty of Sebaste سیباستے کے چالیس.

Troadius's icon line and Tryphon's were both written whole - the young martyr
of Neocaesarea in his torments with Gregory watching in the spirit from his
hiding place, and the young gooseherd with a falcon on his arm and the locusts
turning from the fields at his prayer - and the two lives are built out from
them.

Written for the first time: Sokratia سوکراتیا, Caesarius کیساریوس, Patrikeyev
پاتریکییف.

## Names of this batch

Varus is **واروس**, three vocabulary lines against the وارس of his
commemoration; Spain is **ہسپانیہ**, the vocabulary's, against the اسپین of
Vincent's, and it agrees with the ہسپانوی already written of Stephanida.

From the site: Valerian ویلیرین, Philoumenus فیلومینس, Ancyra انقرہ, Galatia
گلتیہ, Aurelian اورلیان, Cleopatra کلیوپیٹرا, Edra ایدرا, Mount Tabor
کوہ تبور, Victor وکٹر, Damascus دمشق, Stephanida استیفانیدا, Zoticus زوتیکس,
Zeno زینو, Acindynus اکندینس, Severian سیویرین, Saragossa سراگوسا, Valerius
ویلیریس, Valencia ویلنسیا, the archdeacon سردار شماس, the gridiron
لوہے کا جنگلا, Menas میناس.

Varus's icon line was already written - the widow at the martyr's shrine, her
son appearing in shining armor beside Varus in glory - and the life keeps it.

Written for the first time: Dacian داکیان, Vincent ونسنٹ.

Two more borrowings were caught in the block file: اسٹیج for the arena's
staging and ایڈیشن for an edition of the Gospel. They are now تماشا گاہ and
اشاعت. The count of such catches is now six batches out of the last dozen,
which says the pass belongs in the method and not in the exceptions.

## Names of this batch

Pisidia is **پسیدیہ**, three vocabulary lines against the پسیدیا of Zosimus's
commemoration; Catania is **کاتانیا**, settled with Agatha, against the
کاتانیہ of Euplus's.

From the site: Zosimas زوسیماس, Zosimus زوسیمس, Zoticus زوتیکس, Euplus یوپلس,
Laurence لارنس, Sixtus سکستس, Agapitus اگاپیتس, Hippolytus ہپولیتس, the lepers
کوڑھی, the archdeacon سردار شماس, Trajan ٹریجن, Valerian ویلیرین, Naples
نیپلز, Constantine the Great قسطنطین اعظم.

Zoticus's icon line was already written whole - the priest presenting a company
of lepers to the emperor as his purchased pearls, the wild mules and the
healing spring of his end beside him - and the life is built out from it.

Written for the first time: Dometian دومیتیان, Constantius کونستانتیوس,
Felicissimus فیلیسیسیمس, Lucillus لوسیلس, the Bosphorus باسفورس. The
Orphanotropheion is **یتیم خانہ**, described rather than transliterated, which
is also what the entry's own title calls him: یتیموں کا نگہبان.

## Names of this batch

Sabbas is **ساباس** and his lavra **مار سابا**, both the vocabulary's, against
the ساوا of the commemoration; Terence keeps **تیرینس**.

From the site: the Great Lavra عظیم لاورا, the Judean desert یہودیہ کا ویرانہ,
Leonilla لیونیلا, Jonilla جونیلا, Turbo توربو, Neon نیون, Langres لانگرے,
Gaul گال, Shapur شاپور, Paulopetrion پاؤلوپیتریون, the anvil نہائی, Africanus
افریکانس, Publius پبلیس, Carthage کارتھیج, Nicomedia نیکومیڈیا.

Adrian's icon line was already written - the soldier-martyr with his hand on
an anvil, his wife beside him - and the life keeps it. Mark 16:18 closes the
three of Carthage as it closed Terence's own entry, in the same words, since
the two entries are the same company remembered twice.

Written for the first time: Speusippus سپیوسپس, Eleusippus ایلیوسپس,
Meleusippus میلیوسپس, Acindynus اکندینس, Pegasius پیگاسیس, Aphthonius
افتھونیس, Elpidephorus الپیدیفورس, Anempodistus انیمپودسٹس, Adrian آدریان,
Natalia ناتالیا, Dido دیدو.

## Names of this batch

Phoenicia is **فینیکے**, settled with Aquilina, against the فینیشیا of
Ananias's commemoration; Thessalonica **تھسلنیکے**; Lycia **لیکیا**.

From the site: Agapius اگاپیس, Publius پبلیس, Timolaus تیمولاس, Romulus
رومولس, Urbanus اربانس, Eusebius of Caesarea قیصریہ کا یوسیبیوس, Agathopodes
اگاتھوپودیس, Theodulus تھیودولس, Akepsimas اکیپسیماس, Aithalas ایتھالاس,
Arbela اربیلا, Apphianus اپفیانس, Aedesius ایدیسیوس, Amphianus امفیانس,
Edesius ایدیسیس, Pamphilus پامفلس, Ananias حننیاہ, Peter پطرس, Maximus
میکسمس, Gaza غزہ, Pontus پونتوس.

Apphianus's own vocabulary line was already written - the sea, shaken by an
earthquake, casting his body back before the gates of Caesarea - and the life
takes it as it stands.

Written for the first time: Paesis پائسس, Diospolis دیوسپولس, Tripolis
تریپولس, Berytus بیریتوس, Hierocles ہیروکلیس, Maximin میکسیمن, Acepsius
اکیپسیس. A subdeacon is **ذیلی شماس**, formed on the site's own شماس.

## Names of this batch

From the site: Syracuse سراکیوز, Vilnius ولنیئس, Kumets کومیتس, Nezhilo
نیژیلو, Kruglets کروگلیتس, Philotheos فیلوتھیوس, Sergius of Radonezh
رادونیج کا سرجیئس, the Varangians وارانگی, Mstislav مستسلاو, the Kyiv Caves
کیف کے غار, Nestor نیستور, the Saracens سراسین, the emir امیر.

The three of Vilnius had their whole scene in the vocabulary already - three
young courtiers of Lithuania hanged upon the sacred oak, the altar-table
rising from its stump, their incorrupt relics enthroned at Vilnius within a
generation - and the life is built out from it.

Written for the first time: Anatolius اناتولیس, Protoleon پروتولیون, Anicetus
انیکیتس, Photius فوتیس, Hercules ہرکولیس, Algirdas آلگرداس, Svyatopolk
سویاتوپولک, Antonius انتونیس. مشین was caught in the block file and replaced
with آلہ.

## Batch ninety-one

Five lives: Basilissa and Anastasia of Rome, Carpus and Papylus at Pergamum,
Christopher Theonas and Anthony at Rome, Chrysanthus and Daria, Dada Maximus
and Quinctilian.

Names already on the site and carried unchanged: باسیلیسا, اناستاسیا, کارپس,
پاپیلس, اگاتھادورس, اگاتھونیکا, پرگامم, تھواتیرہ, کرسٹوفر, تھیوناس, انتھونی,
کرائسانتھس, داریا, کلاڈیس, ہیلاریا, جیسن, ماورس, دیودورس, ماریانس,
ویا سلاریا, دادا, میکسمس, کوئنکٹیلین, اوزوویا, دوروستولم, موئیسیا,
پاسیکریٹس, ویلنٹائن, داسیوس.

Written here for the first time, on the pattern the site already uses for
Latin and Greek names: Polemius پولیمیس, Carpophorus کارپوفورس,
Minerva مینروا, Ceres سیریس, Nero نیرو.

Chrysanthus and Daria's icon line, and the line naming the whole company
buried with them, are already written in the vocabulary. They are carried in
whole rather than re-rendered; where a saint's own line exists, the life is
built out from it.

## Batch ninety-two

Five lives: Dadas Gabdelas and Kazdoa of Persia, Demetrius Euanthia and
Demetrian at Skepsis, the deacons Diodorus and Rhodopianus at Aphrodisias,
Elias Probus and Ares in Cilicia, Elpidius Marcellus and Eustochius under
Julian the Apostate.

**Elpidius has two forms on the site.** The Cherson hieromartyrs carry
ایلپیدیس (vocabulary 1, commemorations 1); this saint's own commemoration
carries الپیدیس (commemorations 1). Two against one is a near tie, and in a
near tie the commemoration decides - and here the commemoration is the one
written for this very saint. The life keeps الپیدیس, and the Cherson
hieromartyr keeps ایلپیدیس when his turn comes. The site names two men, not
one.

**Eusebius likewise, and the vocabulary has already separated them.** The
historian of Caesarea is یوسیبیوس (vocabulary 5, and the icon line calls him
مورخ by name); the monk of Syria and the bishop of Samosata are یوسیبیس. No
counting was needed: the distinction is already drawn where the site names
the historian as historian.

Maximian: میکسیمیان (4 across the bodies) over مکسیمیان (2).

Names already written and carried unchanged: داداس, گبدیلاس, کازدوآ, شاپور,
دیمیتریس, یوانتھیا, دیمیتریان, سکیپسس, ہیلیسپونٹ, صوبیدار کرنیلیس, دیودورس,
رودوپیانس, افرودیسیاس, کاریا, ایلیاس, پروبس, آریس, کلیکیا, اشقلون,
دیوکلیشین, مارسیلس, یوستوکیس, مرتد جولین, استفنس.

Written here for the first time: Firmilian فرمیلیان.

For the Nativity the life uses the site's own phrase خداوند کی پیدائش
(vocabulary 3, commemorations 6) rather than میلاد, which the site keeps for
the feast's title.

For the Roman governor the lives use حاکم, which is what they have used
throughout (166 against 76 for والی, most of those the ordinary compound).

## Batch ninety-three, and Ancyra settled everywhere

Five lives: the soldier martyrs of Sebaste under Licinius, Eudoxius Zeno and
Macarius, the four of Trebizond, Eulampius and Eulampia at Nicomedia,
Eustochius and his kinsmen at Ancyra.

**The Ancyra decision was made twice on this page and only the second count
was a count.** The first section wrote انکیرا on three commemorations against
one vocabulary entry; the later one counted the whole site and found
seventeen انقرہ against eleven انکیرا, and settled on انقرہ. The lives had
been written from the earlier note and carried انکیرا fourteen times. All
fourteen are now انقرہ. A decision recorded twice is worse than none, and the
later count stands.

Sebaste is **سیباستے**: sixteen across the site against five for سبسطیہ and
two for سباستے. Not close, so the commemoration's سبسطیہ does not decide it.

Melitene is **ملیتینے**: thirteen against four for ملیطینے and two for
میلیتین.

Trebizond is **ترابزون**: eight in the vocabulary, including the icon line
for these very martyrs and the note on Eugene's relics, against one
ٹریبیزونڈ in the commemorations.

Eugene of Trebizond is **یوجینس**, the form his own commemoration and the
note on his relics both give him; یوجین in the icon line is the same name
shortened and does not outweigh them.

Lollius is a true tie, one against one, and there the commemoration decides:
**لولیس**.

Written here for the first time: Carterius کارٹیریس, Istucarius استوکاریس,
Styrax سٹیراکس, Pactobius پاکٹوبیس, Nictopolion نکٹوپولیون, Galerius گلیریس,
Lysias لوسیاس, the Komnenoi کومنینوس, and the god Mars مریخ, which is the
name Urdu already gives him.

The cauldron is دیگ, as the vocabulary writes it a dozen times over.

## Batch ninety-four, and the two prayers of the Five Companions

Five lives: the Five Companions at Sebaste, Eutropius Cleonicus and
Basiliscus of Amasea, Florus and Laurus of Illyria, Frontasius and his
companions in Gaul, Galacteon Juliana and Saturninus at Byzantium.

**The Five Companions' life names two prayers, and the site publishes one of
them.** The Third Hour prayer is Mardarius' own, and the site prints it in
Urdu: اے مالک خدا، قادرِ مطلق باپ. The life carries that opening word for
word, unquoted, as the lives carry received wording. The Saturday midnight
prayer is Eustratius' own, and the site publishes the daily Midnight Office,
not the Saturday one; so the life says what the prayer does - that in it the
Lord's greatness is magnified - and sets no words in quotation marks as
though they were received. This is the rule working in both directions in a
single paragraph.

Auxentius of the Five Companions is **آکسینٹس**, the form his own
commemoration gives him; اوکسینتیس on this site is the ascetic of Bithynia
and Chalcedon, a different man. Two saints, two spellings, as with Elpidius.

Laurus is **لورس**: five across the site, including his own commemoration,
against three لاورس, which come from the name of a church in Novgorod.

Names already written and carried unchanged: یوسٹریٹس, یوجینس, مرداریس,
اوریستیس, اراوراکا, لوسیاس, بلیز, سیباستے, یوٹروپیس, کلیونیکس, باسیلسکس,
اماسیہ, اسکلیپیودوتس, کومانا, تھیوڈور نوآموز سپاہی, فلورس, الیریا, پروکلس,
میکسمس, فرونٹاسیس, سیویرینس, سیویرین, سیلانس, گال, گلاکتیون, جولیانا,
ساتورنینس, بازنطیم.

Written here for the first time: Agricolaus اگریکولاؤس, Satala ساتالا,
Perigueux پیریگو.

## Batch ninety-five

Five lives: Galaction and Epistemis at Emesa, the four martyrs of Milan,
Heliodorus and Dosa of Persia, Heraclius Paulinus and Benedimus at
Noviodunum, Hermes Serapion and Polyaenus of Rome.

Decius is **دیقیوس**: four in the vocabulary and thirteen already in the
lives, against two ڈیسیس in the commemorations. Settled long since and
confirmed here.

Serapion is **سراپیون**, eight across the site against two سیراپیون, and it
is also the form this martyr's own commemoration gives him.

Paulinus and Polyaenus are both **پولینس** on this site, and the
commemorations write them so. Two different men who share a form is what the
index has, and nothing here can change it; the lives keep them apart by their
companions, as the calendar does.

Benedimus is **بینیدمس** (two against one بینیدیمس); Scythia is **سکوتھیا**
(the vocabulary's own label نوویودونم، چھوٹا سکوتھیا) against one سکیتھیا.

Names already written and carried unchanged: گلاکتیون, اپستیمس, ایمیسا,
اونوفریس, نزاریس, گرواسیس, پروٹاسیس, سیلسس, میلان, ایمبروز, لینس, وٹالیس,
ویلیریا, پرپیتوا, نیرو, ہیلیودورس, دوسا, شاپور, ہیراکلیس, نوویودونم,
ڈینیوب, ہرمیس.

Written here for the first time: Leucippe لیوکیپے, Publion پبلیون,
Eutolmius یوتولمیس.

## Batch ninety-six, and a substring that was not a count

Five lives: Hermylus and Stratonicus at Belgrade, Inna Pinna and Rimma in
Scythia, Isaac Apollos and Quadratus at Nicomedia, Isidore and Myrope of
Chios, James and his deacons in Persia.

**Chios looked like a close call and was not.** A plain string count gave
خیوس thirteen and کیوس sixteen, which would have overturned the island's
name. But کیوس is a substring of اکاکیوس, اویرکیوس, امفیلوکیوس and لیوکیوس,
and one of the remaining hits is کیوس، بِتھینیا, which is Cius on the sea of
Marmara and a different place. The real count is thirteen to two, and Chios
is **خیوس**. A substring is not a word; check the context before letting a
number decide.

Scythia is **سکوتھیا** on a full count, seven to one, so the commemoration's
سکیتھیا does not decide it and batch ninety-five's choice stands.

Stratonicus of Belgrade is **سٹریٹونیکس**, his own commemoration's form; the
ستراتونیکس of the vocabulary is the Nicomedian martyr, a different man.

Abdicius is a true tie, one against one, and the commemoration decides:
**ابدیکیس**. Alexandra is **الیگزینڈرا**, five against one.

Carried from the site: عظیم شہید جارج, سب سے پہلے بلایا گیا رسول آندریو,
شاپور دوم, نیزہ بردار, اکیپسیماس, ازاداینس, اسیدور, میروپے, امیر البحر,
سنگیدونم, بلغراد, ایا صوفیہ, اِنّا, پِنّا, رِمّا, اپلوس, کواڈراٹس, وینس,
سان مارکو.

Written here for the first time: Numerius نومیریس.

## Batch ninety-seven

Five lives: Julian and Caesarius at Terracina, Kyriaina and Juliana in
Cilicia, Kyriake Valeria and Mary at Caesarea in Palestine, Leonidas and the
eight women of Corinth, Leontius Hypatius and Theodulus at Tripoli.

Apollo is **اپولو** (four against one اپالو); Tarsus **ترسس** (fourteen
against four ترسوس); Theodulus **تھیودولس** (six against one); Phoenicia
**فینیکے** (seven against one فینیشیا).

Hypatius of Tripoli is **ہپاٹیس**, his own commemoration's form; ہپاتیس is
the wonderworker of Gangra and ہیپاتیوس another man again. Three men, three
spellings, all of them the site's own.

The Red Sea is **بحیرہ قلزم** and the Jordan **یردن**, both as the
vocabulary writes them, and Pascha is **فسح**.

The vocabulary already holds the icon line for Leonidas and the eight women
walking on the sea, and for the soldier of Tripoli with the men sent to
arrest him. Both lives are built out from those lines rather than composed
away from them.

A zero-width non-joiner had crept into one word of the block file and was
stripped before appending. The append checks forbidden dashes and quotes,
not invisible joiners; the block file should be swept for them too.

## Batch ninety-eight, and two verses handled two ways

Five lives: Manuel and Theodosius, the three Persian envoys, the notaries of
Constantinople, Maurice and the seventy at Apamea, the four of Adrianopolis.

**Philippians 3:8 is quoted; Psalm 138:8 is reported.** The Adrianopolis life
ends with Asclepiodota counting her rank as loss, and the published New
Testament gives the words: اُن چیزوں کو کوڑا سمجھتا ہوں، تاکہ المسیح کو حاصل
کر لوں. That is carried in with the edition's pointing dropped, including its
المسیح, which is not corrected. The notaries' life has them praying in the
Psalm's words that God would finish what He began; the published verse is
Psalm 138:8 in the Hebrew numbering, and it opens with the divine name, so
the life reports that half in its own prose and quotes only وہ اُن کے لیے
اپنا مقصد پورا کرے. The rule from the Malachi entry, applied twice in one
batch.

The Book of Life is **کتاب حیات**, which is what Revelation 20:12 calls it in
the published text.

Chrysostom is **یوحنا سنہری دہن**: thirty-seven across the site against ten
for زریں دہن, and the prayers print سنہری دہن three times against one. The
vocabulary's own line for these martyrs says he raised the church over their
grave, and the life carries it.

Consubstantial is **ہم ذات**, the vocabulary's one word for it.

Carried from the site: مانوئل, تھیودوسیس, سابل, اسماعیل, مارکیان, مارٹیریس,
محرر, معترف پولس, آریوسی, مورس, فوتینس, اپامیہ, میکسمس, تھیوڈوتس, ہیسیکیس,
اسکلیپیودوتا, ادریانوپولِس, تھریس.

A note on the block file: it is now swept for zero-width joiners and other
invisibles as well as for dashes and curly quotes, after one crept in last
batch.

## Batch ninety-nine, and a stripping rule that was too wide

Five lives: Menas Hermogenes and Eugraphus at Alexandria, the three sisters
at Nicomedia, Vitus with Modestus and Crescentia, the four of Perge,
Nikephoros Antoninus and Germanus at Caesarea.

**The rule for dropping the edition's pointing had been drawn too wide.** The
Urdu Scripture writes کوئی as ک و ی + U+0654 + ی, that is with a combining
hamza above rather than the single letter ئ. U+0654 there is not decoration:
strip it and Matthew 10:32 reads کویی, which is not a word. The pointing that
is dropped is the vowel and tanween marks and the U+0614 that marks names;
U+0654 and U+0653 stay, and where the edition builds a letter out of a base
plus a combining hamza the sequence is normalised to the single letter the
rest of the site uses. Nothing already written was damaged - the lives carry
no such sequence and no stray یی - but the check is now part of the batch.

Matthew 10:32 closes the life of the four of Perge, carried in with the
edition's quotation marks dropped, as the lives have always done.

Hermogenes the eparch of Alexandria is **ہرموگینس**, his own commemoration's
form; ہرموجینیس is the patriarch of Moscow, a different man. Nestor of Perge
is **نسٹور**, as both his commemorations have him; نیستر is the chronicler of
the Caves.

Modestus and Crescentia are exact ties, one against one, the icon line
writing موڈیستس and کریسکینتیا and the commemoration موڈیسٹس and کریسینٹیا.
The commemoration decides both, as it decides every tie.

Carried from the site: میناس, یوگرافس, مینودورا, میٹرودورا, نمفودورا,
پیتھیاس, وائٹس, لوکانیا, سسلی, ٹریبیمیس, پرگے, پامفیلیا, نکیفوروس,
انتونینس, جرمانس, مانیتھا, فرمیلیان, دیقیوس.

Written here for the first time: Kallikelados کالیکیلادوس, Fronton فرونتون,
Maximinus میکسیمینس.

## Batch one hundred

Five lives: Onesiphorus and Porphyrius at Ephesus, Pamphilius and his eleven
companions at Caesarea, Patermuthius Coprius and Alexander in Egypt, Paul and
Juliana at Ptolemais, Paul and the two sisters at Caesarea.

**Patermuthius and Coprius are monastics and their opening had to say so.**
The commemoration calls the three simply شہداء, and the life followed it; the
register check caught the two desert fathers introduced without a monastic
word. The opening now reads مقدس راہب شہید پاتیرموتھیس اور کوپریس، اور اُن کے
ساتھ سپاہی الیگزینڈر, which keeps the soldier out of the monastic rank while
giving the two elders theirs. A commemoration that omits a rank is not a
ruling that the saint has none.

The prophet Isaiah is **یسعیاہ** - three across the site as the prophet
(نبی یسعیاہ in the vocabulary and the commemorations, and the glossary's note
on his vision) against one اشعیا as the prophet; the other five اشعیا are the
bishop of Rostov and the wonderworker of the Caves, other men. So the Egyptian
youth who took a prophet's name takes یسعیاہ.

Jerusalem is **یروشلم**, sixty-eight across every body against one یروشلیم.

The deacon of Jerusalem is **ویلنس** and the Arian emperor **والنس**; the site
already separates them and the life keeps them apart.

Carried from the site: اونیسیفورس, پورفیریس, افسس, پامفیلیس, سیلیوکس,
تھیودولس, بیروت, جیروم, یرمیاہ, سموئیل, دانیال, پاتیرموتھیس, کوپریس,
اورلیان, پتلمیس, خیونیا, تھیا, الیوتینا, ویلنٹینا, فرمیلیان, یوسیبیوس.

Written here for the first time: Jamnia یمنیہ.

## Batch one hundred and one

Five lives: Perpetua and Felicitas at Carthage, the five under Decius at
Lampsacus and Tyre, the three brothers of Sicily, Philemon and his company in
Egypt, Probus Tarachus and Andronicus at Tarsus.

Felicitas is **فیلیسیتاس**, three across the site against one فیلیسیٹی. A
catechumen is **نومرید**, which the commemorations and the vocabulary already
use seven times over for this very company.

Tyre is **صور**, as the vocabulary and Christina's own commemoration have it.

Venus had no form on the site. She is written **زہرہ**, the name Urdu already
gives her, on the same footing as Mars مریخ in batch ninety-three: a goddess
the site has not named is described in the language, not borrowed into it.

Perpetua's answer to her father is reported, not quoted. The diary is not a
text this site publishes, and a sentence set in quotation marks would claim a
received wording that no reader could check.

Carried from the site: پرپیتوا, ساتورس, ریووکاتس, ساتورنینس, سیکنڈولس,
کارتھیج, بازیلیکا مایورم, لیمپساکس, کرسٹینا, فلاڈیلفس, کپرین, الفیس,
اونیسیمس, ایراسمس, لینتینی, واستے, یوتھالیا, فلیمون, اپولونیوس, اریان,
تھیوناس, انتینوئے, پروبس, تاراکس, اندرونیکس, ترسس, موپسوئستیا, انازاربس,
سیدے, افسس.

Written here for the first time: Vibia ویبیا.

## Batch one hundred and two, and a pair spelled by two different rules

Five lives: Processus and Martinian at Rome, Proclus and Hilary of Ancyra,
Rhipsime and Gaiane in Armenia, Rusticus and Eleutherius in Gaul, Sergius and
Bacchus in Syria.

**Sergius is سرجیئس and Bacchus is باکس, and the two were settled by
different rules, which is not an inconsistency.** Sergius stands at
sixty-five across the site against five, and the five are not a distinct
saint: رادونیج کے سینٹ سرجیس writes the same man's name the short way in the
commemorations, so there is no second form belonging to a second saint, only
one name spelled two ways, and the larger body wins as it won for
Thessaloniki and Ancyra. Bacchus stands at two against one, which is a near
tie, and there the commemoration for this very pair decides. The reader will
meet سرجیس اور باکس in the calendar heading and سرجیئس اور باکس in the life;
the heading follows the index, the life follows the site.

Rhipsime is **ریپسیمے** and Gaiane **گائنے**, each one against one against
the forms used in the names of their churches at Echmiadzin, and each
carrying its commemoration. Echmiadzin itself is **ایچمیادزین**, the form in
the martyrs' own icon line rather than the one in the shrine note.

Domitian the emperor takes **دومیتیان**, the form the site already gives the
bishop of Melitene; one name, one spelling.

Philippians 1:21 closes the answer of Sergius and Bacchus to Antiochus,
carried from the published text: کیونکہ زندہ رہنا میرے لیے المسیح ہے، اور
مرنا نفع.

Carried from the site: پروسیسس, مارٹینین, مامیرتینے, لوسینا, ٹریجن, پروکلس,
ہلیری, واغارشاپات, تیریداتیس, رسٹیکس, ایلیوتھیریس, اریوپیگس کا ڈیونیسیس,
پیرس, انطیوکس, رصافہ, سرجیوپولس, موسیٰ.

Written here for the first time: Lutetia لوتیشیا, Barbalissos باربالیسوس.

## Batch one hundred and three

Five lives: Simeon Isaac and Bachtisius of Persia, the three Egyptian
soldiers at Chalcedon, Sophia Irene and Castor in Egypt, Theodore the
Varangian and his son John at Kyiv, Theodotus and Rufina at Caesarea.

Chalcedon is **کلقیدون**: twenty-nine across the site against one کلیسیڈن in
these martyrs' own commemoration. Not close, so the commemoration does not
decide it.

Zoroastrian had no form on the site and is written **زرتشتی**, the word Urdu
already has for it, on the footing of Mars and Venus: a thing the site has
not named is described in the language rather than borrowed into it.

Carried from the site: شمعون, اسحاق, بختیسیس, سولوخون, پامفامیر, پامفالون,
صوفیہ, آئرینے, کاسٹر, تھیوڈور وارانگی, یوحنا, کیف, ولادیمیر, تھیوڈوتس,
روفینا, ماماس, گنگرا, فاوستس, کپادوکیہ کا قیصریہ.

## Batch one hundred and four, and another substring that lied

Five lives: Theodotus Asclepiodotus and Maximus at Adrianopolis, Thyrsus
Leucius and Callinicus at Apollonia, Timothy Agapius and Thecla in Palestine,
Trophimus and Eucarpus at Nicomedia, Trophimus Sabbatius and Dorymedon at
Synnada.

**Timothy is تیمتھیس, and a plain count said otherwise.** تیمتھی is a
substring of تیمتھیس, so the naive figures were sixteen to eleven in favour
of the short form. Counted with the longer form excluded, it is eleven
تیمتھیس against five تیمتھی, and the longer form wins. This is the Chios
mistake in a new place; a count over a language written without spaces
between name and suffix has to exclude the longer form before it means
anything.

**Asclepiodotus of this company is اسکلیپیودوتس and the Asclepiodota of batch
ninety-eight stays اسکلیپیودوتا.** The calendar carries two companies of
Adrianopolis close together, one with a man of that name and one with a
noblewoman; the commemorations spell them differently and the lives keep them
apart.

Carried from the site: مارکیانوپولس, تھریس, ادریانوپولِس, تھرسوس, لیوکیوس,
کالینیکوس, اپولونیا, اگاپیس, تھیکلا, تروفیمس, یوکارپس, سباتیس, دوریمیدون,
سناڈا, فروگیہ, انطاکیہ, دمشق, ساؤل, پروبس.

Written here for the first time: Cumbricius کومبریسیوس.

## Batch one hundred and five

Five lives: Pasikrates and Valentine at Durostorum, the seven of Corinth,
Zeno and Zenas at Philadelphia, Boris and Gleb, Cosmas and Damian with their
three brothers.

Durostorum is **دوروستولم** (eight against four دوروستورم) and Moesia
**موئیسیا** (five against one موسیا in the commemoration).

Passion-bearer is **آلام بردار**, eighteen across the site; مصیبت بردار
appears once, in the entry on the translation of the relics.

Unmercenary is **بے غرض معالج**, twenty-six against four بلامعاوضہ طبیب and
two بے اجرت طبیب.

Boris and Gleb take **رومن اور ڈیوڈ** for their baptismal names. Both forms
are in the commemorations, ڈیوڈ where the two brothers are named together and
داؤد where Gleb is named alone; the life is for both brothers, so it follows
the entry that names both. داؤد stays the prophet's name, as the prayers
write it twenty-eight times.

Psalm 34:20 closes the life of the seven of Corinth, carried from the
published text; the verse carries no divine name, so it is quoted whole.

The counting script now reports a whole-word figure beside the raw one, after
Chios and Timothy were both nearly settled by a substring.

Carried from the site: پاسیکریٹس, ویلنٹائن, داسیوس, وکٹورینس, وکٹر,
نکیفوروس, کلاڈیس, دیودورس, سراپیون, پاپیاس, کرنتھس, اگنیشیس, زینو, زیناس,
فلاڈیلفیا, عرب, بورس, گلیب, ولادیمیر, روستوف, مُروم, کوسماس, دامیان,
لیونٹیس, انتھیمس, یوٹروپیس, ایگائی, لوسیاس.

Written here for the first time: Absolanus ابسولانوس, Svyatopolk سویاتوپولک.

## Batch one hundred and six

Five entries: the martyrs of Kvabtakhevi, the Meeting of the Vladimir Icon,
Adrian of Poshekhonye, Anastasia the Roman, Anastasius the deacon of the Near
Caves.

**The Vladimir Icon entry is a feast, not a saint, and its opening says so.**
It begins اِس دن کلیسا, not with a rank, because there is no person to rank.
The register check reads openings that introduce a saint and passes this one
by; a feast written as though it were a saint would be the worse error.

Barlaam of Khutyn is **ورلام**: eight in the vocabulary, including the entry
that names him as the spiritual father, against four برلام in the
commemorations, which belong to other men of the name. Not a tie, so the
count decides.

Tamerlane is **تیمور**, the form the commemoration of the Vladimir Icon
already uses for him. Mehmed Giray is written محمد گرائے, and the life keeps
the Russian accounts' own ماخمیت-گیرے beside it, as the English entry does.

The Great Fast is **بڑے روزے**, as the glossary writes it nine times.

The three monastic saints of this batch carry monastic words in their
openings: راہب شہید آدریان, راہبہ شہید اناستاسیا, راہب شہید شماس اناستاسیس.

The sentence from the service of the Near Caves fathers is reported, not
quoted. The site does not publish that service, so no words are set as
received.

Carried from the site: کوابتاخیوی, کارتلی, جارجیا, ولادیمیر آئیکن, ماسکو,
کریمیا, رادونیج کے سرجیئس, آدریان, پوشیخونیے, یاروسلاول, کومیل کے کرنیلیس,
لیونیداس, وفات, اناستاسیا, صوفیہ, ویلیرین, پروبس, اناستاسیس, ٹائٹس,
اتھاناسیس, قریبی غار, لاورا, انتھونی.

Written here for the first time: Bagrat باگرات, Ahmed احمد.

## Batch one hundred and seven

Five lives, all monastic martyrs: Anastasius the Persian, Andrew of Crete,
Bademus of Persia, Christopher of Dionysiou, Damascene of the Lavra.

Andrew is **آندریو**, twenty-four across the site against six اندریاس, and
his own commemoration writes it so; the اندریاس of the vocabulary belongs to
the hymnographer of the Great Canon, whom this entry is careful to keep
separate.

Crete is **کریٹ**: ten against eight کریتی, which is a near tie, and the
commemoration for this saint decides it.

Adrianople in Christopher's life is **ادریانوپل**, five in the vocabulary
including his own icon line, against two ادریانوپولِس in the commemorations,
which name the martyrs of that city under the older form. The two forms are
already both on the site and each entry keeps the one its own line uses.

Islam is **اسلام**, which the vocabulary already writes six times; a mosque
is مسجد, the ordinary word, which the site has not needed before.

Written here for the first time: Bavi باوی, Magundates ماگونداتیس, Chosroes
خسرو, Copronymus کوپرونیموس.

Carried from the site: بیتھسالوئے, نینوہ, ماماس, کریسس, بادیمس, وادم,
بیت لاپیتا, نیرسان, دیونیسیو, مقدس پہاڑ, دمشقین, گلاتا, کیریاکوس, دیامانتیس,
عظیم اسکیما, فنار, ایا صوفیہ, کلقیدون, شاپور.

## Batch one hundred and eight

Five monastic martyrs: Euphrosynus of the Blue Lake, Eustratius the Faster of
the Near Caves, Euthymius of Prodromou, Joseph and Macarius of Dionysiou.

Prodromou is **پرودرومو** (three against one پروڈرومو); the Peloponnese
**پیلوپونیس** (eleven against one پیلوپونیز); Stephen **اسٹیفن**
(thirty-three against twenty).

Palm Sunday is **کھجور کا اتوار**, and the vocabulary's own icon line for
Euthymius already says his head was cut off on that very day, so the life is
built out from it. Chrismation is **مسح**, seven in the vocabulary and five
in the glossary. The Holy Mysteries are **مقدس اسرار**, which the prayers
write four times.

Written here for the first time: Polovtsian پولووتسی, Bonyak بونیاک.

Carried from the site: یوفروسینس, بلو جے جھیل, سینوزیرسک, کاریلی, لادوگا,
والام, تیخوین, بشارت, یونس, مصیبتوں کا زمانہ, یوسٹریٹس, روزہ دار, خرسون,
پاتیریک, یوتھیمیس, دیمیتسانا, ایلیوتھیریوس, وزیر, اگنیشیس, اکاکیس, یوسف,
ایودوکیمس, مکاریس, نیفون, تھسلنیکے, عظیم اسکیما.

## Batch one hundred and nine, and forty per cent

Five monastic martyrs: Macarius of Saint Anne's, Paul of the Lavra, Stephen
the New, Conon and his son at Iconium, Menas David and John of Palestine.

A skete is **اسقیطس**, thirty-four across the vocabulary against two سکیتے in
the commemorations, and Anne is **آنا**, nine against one اینی; so the house
is سینٹ آنا کا اسقیطس even though the commemoration writes it the other way.
Neither is a tie.

Macarius is **مکاریس** (twenty-four against six میکیریس); Iconium
**اکونیوم** (ten against one); Chariton **خریطون** (five against two);
Sabbas **ساباس** (nineteen against one).

Stephen the New's answer before the emperor is reported, not quoted. It is
not Scripture and the site publishes no service that carries it.

Carried from the site: کیوس, نیا اسٹیفن, بلاخیرنے, کوہ اوکسینتیس,
راست دینی کی فتح, آئیکن شکنی, کونون, دومیتیان, اچرنو, کیمپانیا, اورلیان,
یوتھیمیس, سراسین, مار سابا, لاورا, میناس, داؤد, یوحنا, یردن.

## Batch one hundred and ten, and the hamza that had to be put back

Five entries: the confessors imprisoned with Stephen the New, Mary Magdalene,
the Nativity of the Forerunner, Anastasius of Epirus, Vasily Martysz.

**Elizabeth is الیشبع, settled by the prayers.** The site carries three of
each form; the prayers print الیشبع once and الزبتھ never, and the prayers
decide, as they decided Basil. The commemoration of the Forerunner's parents
writes الزبتھ, and it is outranked.

Martysz is a true tie, one against one, and the commemoration decides:
**مارتش**. Chelm is **خیلم**, the only form on the site.

**Four verses are woven into the Nativity of the Forerunner**, Luke 1:17, Luke
1:63, John 1:29 and Luke 7:28, all carried from the published text with the
edition's pointing and quotation marks dropped, and with its ی plus combining
hamza normalised to the single letter ئ, so that لیٔے reads لئے and کویٔی
reads کوئی as the rest of the site writes them. This is the correction made in
batch ninety-nine, now applied where it matters: stripping that hamza would
have printed three broken words in the middle of the Gospel.

Luke 1:63 keeps the edition's own زکریاہ inside the quotation, while the rest
of the entry writes the site's زکریا, seven times across the bodies. An
edition is not corrected inside its own sentence and not imposed outside it.

Carried from the site: مریم مجدلیہ, مجدل, خوشبو لانے والی, رسولوں کے برابر,
جبرائیل, ایپیروس, پارامیتھیا, دانیال, تیراتین, الاسکا, وارسا, یوحنا کلیماکس,
کوپرونیموس, اوکسینتیس, نیا اسٹیفن.

Written here for the first time: Tiberius تیبیریس, Pilsudski پیلسودسکی.

## Batch one hundred and eleven

Five new martyrs: Ephraim of Nea Makri, Euthymius of Athos, Habakkuk,
Ignatius of Athos, John Kalphes.

**Ephraim has three forms on the site and takes the largest.** افریم stands
at sixteen across the vocabulary and the commemorations, افرائیم at seven
(Ephraim the tribe and the hill country, and the prayers' one), and افرایم at
one, in this saint's own commemoration. Sixteen to one is not a tie, so the
commemoration does not decide it, and the life writes **افریم**.

Panteleimon is **پانتیلیمون**, seven against one.

Habakkuk's entry calls him venerable and the index types him a monk, so his
opening had to carry a monastic word; it now reads مقدس راہب اور نیا شہید
حبقوق. The commemoration gives only نیا شہید, and an omission there is not a
ruling, as with the desert fathers of batch one hundred.

The vocabulary already holds icon lines for four of these five, and each life
is built out from its own: the hieromonk bound to the mulberry tree of his
courtyard, the abbess Makaria whose obedience uncovered the relics, the young
monk hanged at Daktyloporta with his childhood fear behind him, the young
builder of the Ottoman court with the apprentice he taught.

Written here for the first time: Prote پروتے, Gregory the Fifth
گریگوری پنجم.

Carried from the site: نیا ماکری, تریکالا, تھیسالی, کوہ اموموں, اٹیکا,
مکاریا, شہتوت, دیمیتسانا, ایویرون, نکیفوروس, اکاکیس, گریگوریو, حبقوق,
ستارا زاگورا, داکتیلوپورتا, کلفیس, پیش رو کا اسقیطس, سینٹ آنا کا اسقیطس.

## Batch one hundred and twelve, and six hundred lives

Five entries: John of Ioannina, John the New of Suceava, Lazarus of Bulgaria,
the New Martyrs of Butovo, the Synaxis of the New Martyrs of Russia.

Suceava is **سوچاوا**, four across the site including the commemoration,
against one سُچاوا in a relic note; Tikhon is **تیخون**, twenty-one against
two طیخون.

Elizabeth here is **الزبتھ**, not the الیشبع settled in batch one hundred and
ten. They are two women: the prayers write الیشبع for the Forerunner's
mother, and the vocabulary writes الزبتھ for the Grand Duchess who was thrown
down the mine shaft. One name, two people, two spellings the site already
keeps apart.

The Butovo and Russia entries are synaxes, not single saints, and open
accordingly, اِس دن کلیسا and روس کے مقدس نئے شہداء اور معترفین کا اجتماع.

Written here for the first time: Alexy الیکسی.

Carried from the site: یوآنینا, بیلگوروڈ, اکرمان, مولداویا, لعزر, پرگامم,
انتیپاس, بوتوو, گلگتا, نکولس, جوبلی کونسل, بیرون ملک روسی کلیسا, ولادیمیر,
آلام بردار.

## Batch one hundred and thirteen

Five entries: the Nine of Cyzicus, Eugenia of Rome, the passion-bearer Gleb,
the Persian martyrs at Martyropolis, the presbyters Eugene and Macarius.

Rufus and Magnus are both exact ties between the vocabulary and the
commemorations, and both go to the commemoration: **رفس** and **میگنس**.

The catholicos Symeon is **شمعون**, fifty-two across the site against six
سیمیون. The prayers carry سیمیون three times, but for the Slavic Symeons, not
this Syriac one, and fifty-two to six is not the near-level case where the
prayers decide.

Gleb keeps **ڈیوڈ** for his baptismal name, as settled in batch one hundred
and five: the entry that names both brothers is the one that names both
baptismal names.

Written here for the first time: Propontis پروپونتس, Helenus ہیلینس,
Melanthia میلانتھیا, Smyadyn سمیادین, catholicos کاتھولیکوس.

Carried from the site: کیزیکس, تھیوگنیس, انتیپاتر, تھیوستیکس, ارتیماس,
تھیوڈوتس, تھاؤماسیس, فلیمون, یوجینیا, پروٹاس, ہائیسنتھ, باسیلا, ویشگوروڈ,
یاروسلاو, سمولینسک, ماروتھاس, مارتیروپولِس, مایپرقات, میسوپوٹیمیا,
سویاتوپولک, شاپور دوم, زرتشتی, مرتد جولین.

## Batch one hundred and fourteen

Five entries: John Kochurov, Jonah of Pechenga, Anna of Novgorod, the
Procession of the Cross, the Prophet Amos.

**Amos is read off the published Scripture, not rendered by ear.** The Urdu
Old Testament gives the prophet عاموس, Tekoa تقوع, Amaziah اماضیاہ, Jeroboam
یربعام, and the sycamore گولر کا درخت, and the vocabulary's icon line for him
already uses تقوعہ, گولر کے انجیر and بیت ایل. Three verses are woven in:
Amos 5:24 whole, Amos 2:6 from its second half only, since the first carries
the divine name, and Amos 6:4 in part. Amos 7:14 supplies the sentence that
he was no prophet nor a prophet's son, reported rather than quoted because
the life speaks it in its own voice.

Anna of Novgorod takes **آنا** from her commemoration and **آئرینے** for her
baptismal name, the form the vocabulary already gives the martyr of Corinth
whose house she founded in Kyiv.

Carried from the site: کوچوروف, ریازان, شکاگو, تسارسکویے سیلو, تیخون,
پیچنگا, وارزوگا, پوموریے, کولا, ٹریفون, سولوفکی, یونس, دانا یاروسلاو,
نووگورود, حیات بخش صلیب, روس کا بپتسمہ, مقدس حکمت.

Written here for the first time: Ingigerd انگیگرد, Olof اولوف, the Lapps
لیپ لوگ.

## Batch one hundred and fifteen, five prophets read off the page

Five prophets: Daniel, Elisha, Ezekiel, Habakkuk, Haggai. Their books are
published here, so almost nothing in these five lives is rendered by ear.

Names taken from the Urdu Old Testament: Nebuchadnezzar نبوکدنضر, Belshazzar
بیلشضر, Darius داریاویش, the Chebar کبار نہر, Buzi بوزی, Jechoniah یہویاکین,
Naaman نعمان, Aram ارام, Zerubbabel زربابیل, Joshua the high priest یہوشع,
Tekoa تقوع.

Verses woven in whole, none of them carrying the divine name: Daniel 7:13,
Daniel 10:11 (معزز مرد), 2 Kings 13:21, Ezekiel 18:20, Habakkuk 2:3 and 2:4.
Verses quoted in part, the divine name reported rather than carried: Ezekiel
37:4 (اے سوکھی ہڈیوں), Ezekiel 44:2 (یہ پھاٹک بند رہے گا), Haggai 1:5
(تم اپنی روش پر غور کرو), Haggai 2:9 and 2:7. Habakkuk 3:2 opens twice with
the divine name and is reported entirely.

**The prophet's own name is the site's, the edition's stays in the quotation.**
Daniel is **دانیال** across the entry, twenty-one against four, though the
verse quoted from him prints دانی ایل; Haggai is **حجی** as his commemoration
has him, though his own book heads him حگی. An edition is not corrected inside
its sentence and not imposed outside it, which is the rule set in batch one
hundred and ten and applied here five times over.

Susanna and the Habakkuk of the lions' den are in the Greek Daniel, which the
published Urdu Old Testament does not carry. Both are told in the site's own
prose and the book is simply named, as 2 Maccabees was named for Eleazar. The
entry says what a thing is; it does not announce what is missing from a file.

## Batch one hundred and sixteen, five more prophets

Hosea, Isaiah, Jeremiah, Joad, Joel. As with the last batch, the names and the
verses come off the published Old Testament.

Names read from the edition: Hosea ہوشیع, Beeri بیری, Gomer گومر, Amoz آموص,
Uzziah عزیاہ, Jotham یوتام, Ahaz آحاز, Hezekiah حزقیاہ, Manasseh منشہ,
Immanuel عمانوایل, Jesse یشائی, Hilkiah خلقیاہ, Anathoth عناتوت, Benjamin
بنیامین, Baruch باروک, Taphanes تحفنحیس, Josiah یوشیاہ, Pethuel پتھوایل.
The prophet himself keeps the site's **یسعیاہ**, settled in batch one hundred,
though his own book heads him یشعیاہ - the same rule as Daniel and Haggai.

Quoted whole, no divine name in them: Hosea 14:4, 6:6, 11:1, 13:14; Isaiah
6:1, 6:7, 6:8, 9:6, 11:1, 53:3, 53:5, 53:7, 40:1; Jeremiah 1:5, 9:1; 1 Kings
13:30 and 13:31; 2 Kings 23:18.

Quoted in part, the divine name reported: Isaiah 7:14 from دیکھو ایک کنواری
onward, Isaiah 40:3, Jeremiah 20:9 from آپ کا کلام onward, Jeremiah 31:33 and
31:34, 1 Kings 13:2 (اے مذبح، اے مذبح), 1 Kings 13:4 (اِس شخص کو گرفتار کر
لو), Joel 2:13 and 2:28.

**Isaiah 6:3 is reported, and only the threefold word is carried.** The verse
in the edition reads قدوس، قدوس، قدوس قادرمطلق یاہوہ; the prayers print
قدوس، قدوس، قدوس ہے تُو، اے خدا. Rather than choose between them the life
says the seraphim cried قدوس، قدوس، قدوس to one another, which both bodies
write identically and neither divides.

## Batch one hundred and seventeen, and two hundred thousand words

Jonah, Micah, Nahum, Obadiah, Samuel.

The prophets keep the site's names against their own books again: Jonah is
**یونس** (thirteen against one یوناہ, and the book heads him یوناہ), Samuel
is **سموئیل** (six across the site, none for the book's شموایل). Micah
**میکاہ**, Nahum **ناحوم** and Obadiah **عبدیاہ** agree in both bodies.

Read from the edition: Amathi امتائی, Tarshish ترشیش, Moresheth موریشیت,
Bethlehem Ephrathah بیت لحم افراتہ, Elkosh القوش, Zion صیون, Edom ادوم, Ahab
اخی اب, Jezebel ایزبل, Shiloh شیلوہ, Eli عیلی, Hannah حنہ.

Quoted whole: Micah 5:2, Jonah 4:11, Nahum 1:15, Obadiah 1:17, and Samuel's
answer at the sanctuary. Quoted in part with the divine name reported: Micah
6:8, Nahum 1:7, Obadiah 1:4 and 1:21.

## Batch one hundred and eighteen

Shemaiah, Zechariah, Zephaniah, the Prophetess Hannah, and the Protomartyr
Stephen.

**Stephen is استفنس, on the Scripture and not on the commemorations.** The
commemorations write استیفن twice and استفنس once, which by the tie rule would
favour the longer form; but Acts prints استفنس throughout, and a name that
occurs in the Bible is read off the text, which is the rule this page set for
دبورہ and بارک and every other. The lives already carried استفنس from the
deacons of Aphrodisias.

Shemaiah keeps the site's **سمعیاہ** against the edition's شمعیاہ, and
Zechariah the site's **زکریاہ**, distinct from the زکریا of the Forerunner's
father, whom the site names without the final ہ.

Read from the edition: Rehoboam رحبعام, Shishak شیشاق, Elkanah القانہ,
Ramathaim راماتائیم, Gamaliel گملی ایل, Ephrathah افراتہ.

Quoted whole: Zechariah 9:9, 12:10 in part, Zephaniah 1:15, 3:14, 1 Samuel
2:5, and the four sentences of Acts 6:15, 7:56, 7:59 and 7:60. Quoted with the
divine name reported: 1 Kings 12:24, Zechariah 11:13, 13:7 and 14:7,
Zephaniah 2:3 and 3:17, 1 Samuel 2:1 and 2:7.

Written here for the first time: Eleutheropolis ایلیوتھیروپولِس,
Kaphar Gamala کفر جملا.

## Batch one hundred and nineteen

Thekla, Anna of Kashin, Job of Pochaev, Alexander Nevsky, Alexis Toth.

Kashin is **کاشن** (eight in the vocabulary against two کاشین in the
commemorations); Alexis **ایلکسیس** (fourteen against one الیکسس and one
الکسیس), which the prince of the Neva also takes for his monastic name;
Isauria **اسوریہ** (nine against two).

Written here for the first time: Lake Chudskoye چودسکویے جھیل, the Teutonic
knights ٹیوٹونی سورما, Gorodets گوروڈیتس, the Old Believers پرانے عقیدے
والے, Metropolitan Cyril کرل, John Ireland جان آئرلینڈ.

Carried from the site: تھیکلا, اکونیوم, سلوکیہ, تویر, ایوب, پوچائیف,
وولہینیا, بریست کا اتحاد, الیگزینڈر نیفسکی, نیوا, پیریسلاول-زالیسکی,
زیمپلن, کارپاتھی روس, مینیاپولس, ولکس-بیری, تیخون, کارپاتھو-روس, یونیایٹ.

## Batch one hundred and twenty, and a correction from the batch before

Arsenius of Serbia, Cyprian of Moscow, Cyril the Teacher of the Slavs,
Eustathius the First of Serbia, Herman of Kazan.

**Cyril is سیرل, thirty-two across the site against five کیرل**, and batch one
hundred and nineteen had written Metropolitan Cyril of Kyiv as کرل, a form
that appears nowhere. It is corrected. A name written for the first time
should be counted even when it is only a walk-on.

Kazan is **کازان** (forty-seven against eight قازان), Pec **پیچ**, Cyprian of
Moscow **کپرین** (the Carthaginian bishop stays سائپرین, a different man),
Herman of Kazan **جرمانس** as his own commemoration has him.

Written here for the first time: Vladislav ولادیسلاو, Milesevo میلیشیوو,
Zdrebaonik زدریبااونک, Saint Mary Major سینٹ میری میجر, Stephen Urosh
اسٹیفن اوروش, the Polevs پولیو, the oprichnina اوپریچنینا.

Carried from the site: ارسینیس, سریم, ژچا, ساوا, ترنووو, میتھوڈیس, موراویا,
خزر, سان کلیمینتے, ہادریان, یوستاتھیس, بودیملیے, زیتا, ہلندار, ستاریتسا,
وولوکولامسک, گوریاس, سویاژسک, تیمور, ولادیمیر آئیکن.

## Batch one hundred and twenty-one

Innocent of Alaska and Moscow, Innocent of Irkutsk, Jacob Netsvetov, John
Chrysostom, Jonah of Novgorod.

Irkutsk is **ارکوتسک** (twelve in the vocabulary against two ارکتسک in the
commemorations); Innocent is **انوسنٹ** (seven against one اینوکینتیس, which
belongs to the disciple of Nilus of Sora, a different man). The kayak is
**کیاک**, which the vocabulary already uses five times of this very saint.

Written here for the first time: Unalaska اونالاسکا, the Tlingit تلنگت,
Kamchatka کامچاٹکا, the Kuriles کوریل جزیرے, the Yakuts یاکوت, Yakutsk
یاکوتسک, the Amur آمور, Kulchitsky کولچیتسکی, Beijing بیجنگ, the Buryats
بوریات, the taiga تائیگا, the Unangan اونانگان, Kvikhpak کویخپاک, the Yukon
یوکون, Ikogmiute اِکوگمیوت, Tobolsk توبولسک, Libanius لیبانیوس, Eudoxia
یوڈوکسیا.

Chrysostom's last words are reported in the site's own prose rather than set
in quotation marks: the sentence is famous, but it is not Scripture and the
site publishes no service that carries it.

Carried from the site: ایوان پوپوف-وینیامینوف, الیوت, سٹکا, انگا, سائبیریا,
چرنیگوف, نیتسویتوف, اتکا, انتھوسا, میلیتیس, کومانا, یونس, نووگوروڈ, کلوپس,
اوتنیا, یوحنا سنہری دہن, رادونیج کے سرجیئس.

## Batch one hundred and twenty-two

Nikolai of Zhicha, Peter of Moscow, Raphael of Brooklyn, Theodore
Yaroslavich, Theodosius of Chernihiv.

**Chernihiv is چرنیہیو**, eighteen across the site against five چرنیگوف and
one کرنیگوف. The vocabulary's own place label writes چرنیگوف کی سرزمین, and
batch one hundred and twenty-one followed it for the birthplace of Innocent of
Irkutsk; that one occurrence is now چرنیہیو too. A place should not be two
places in one body of lives.

Raphael of Brooklyn is **رافیل**, two against one رافایل; both forms are in
his own two commemorations, so the tie is broken by the vocabulary, which
writes رافیل of the new martyr of Lesbos.

The words of the Mother of God on the sea and Saint Peter's prophecy to Ivan
Kalita are reported in the site's prose rather than set in quotation marks:
neither is Scripture, and the site publishes no service that carries them.

Written here for the first time: Gavrilo گاوریلو, the Rata راتا, Kalita
کلیتا, Halki خالکی, al-Kalimat الکلمة, Vsevolodovich وسیوولودووچ, the Uglicki
اوگلیتسکی, Vydubitsky ویدوبیتسکی, Yelets یلیتس.

Carried from the site: نکولائی, نکولا ویلیمیروویچ, لیلچ, اوہرد, پرولوگ,
داخاؤ, لبرٹی ول, پیتروفسکایا, پیریاسلاول, بروکلین, انطاکی بستی, پودولیا,
کورسون, لازار, تھیوڈور یاروسلاوچ, ژچا, تیخون, انوسنٹ.

## Batch one hundred and twenty-three, and forty-five per cent

Theoktistos of Novgorod, Tikhon of Moscow, Abramius of Galich, Cornelius of
Pereyaslavl, Herman of Alaska.

Chukhloma is **چخلوما** (two in the commemorations against one چوخلوما).
Abramius of Galich keeps **ابرامیس**, his own commemoration's form; the
ابرامیوس of the vocabulary is the disciple who moved the relics at
Palaeostrov, a different man. Cornelius of Pereyaslavl is **کرنیلیس**, his
own commemoration's form, against the کورنیلیوس of the Pskov Caves and the
Komel rule.

The last words of Patriarch Tikhon and the rule Saint Herman gave on the boat
are reported in the site's prose without quotation marks, as the lives have
handled every saying that is not Scripture and not in a service the site
publishes.

Written here for the first time: the Renovationists تجدید پسند, Lukianov
لوکیانوف, Boris and Gleb on the Sands ریت پر بورس اور گلیب.

Carried from the site: تھیوکتستوس, واسیلی بیلاوین, توروپیتس, ولنیئس,
دونسکوئے, گالچ, کونون, ریازان, روستوف کا دیمیتریس, ہرمن, سرپوخوف, نزاریس,
کودیاک, الوتیک, اسپروس جزیرہ, والام, لادوگا.

## Batch one hundred and twenty-four

Job of Pochaev, Nilus of Sora, Seraphim of Sarov, Sergius of Radonezh, Shio
of Mgvime.

**Saint Seraphim's rock prayer is the publican's, and the site publishes it.**
The thousand nights on the stone were prayed in the words of Luke 18:13, which
the Urdu New Testament gives as خدا، مجھ گنہگار پر رحم کر, and the life
carries them from the published text. His Paschal greeting and the word to
Motovilov are reported in the site's own prose: neither is Scripture.

Nilus of Sora is **نیلس**, his own commemoration's form, the same the site
gives Nilus of Sinai; Job of Pochaev is **ایوب**, as the vocabulary already
writes him.

Written here for the first time: Ugornits اوگورنیتس, Dubno دُبنو, the
Non-Possessors غیر مالک, Moshnin موشنین, Motovilov موتوویلوف, Kulikovo
کولیکووو, Kirillo-Belozersk کیریلو-بیلوزرسک.

Carried from the site: ایوان ژیلیزو, پوکوتیا, گلیسیا, اوستروگ, دوسیتھیس,
سورا, نکولس مائکوف, وولوتسک کا یوسف, سیرافیم, ساروف, کورسک-جڑ, دیویوو,
رادونیج, برتلمائی, شیو, مگویمے, زیدازینی, متسختا, تیرہ شامی آبا.

## Batch one hundred and twenty-five

John of Ustyug, John the Theologian, Anna of Kashin's repose, the return of
the relics of Bartholomew, Roman of Uglich.

**Bartholomew is برتلمائی, and the New Testament settles it.** The site
carries three forms: برتلمائی eight times in the vocabulary, برتولما once and
برتھولومیو once in the commemorations. Matthew 10:3 prints برتلمائی, and a
name that occurs in the Bible is read off the text, as it was for Stephen.

Ustyug is **اُستیوگ**, ten against three, and the vocabulary already has the
fool's own icon line: چیتھڑوں میں تنور کے گرم پتھروں پر, out of which the
life is built.

Read from the New Testament: Zebedee زبدی, Salome سلومی, Jairus یائیر, and
the burden of the epistles, خدا محبت ہے, which is 1 John 4:8 word for word.

Anna of Kashin's repose is a second entry for the saint of batch one hundred
and nineteen, and her opening here had to carry the monastic word her order
requires: مقدسہ راہبہ شہزادی کاشن کی آنا. A princess who ends in the schema is
typed a nun, and the register check is right to want it said.

Carried from the site: پاتموس, افسس, عالمِ الٰہیات, اناستاسیوپولِس, لیپاری,
اگاتھون, بینیوینتو, نیپلز, اوگلچ, تویر, کاشن, تبور, گتسمنی.

## Batch one hundred and twenty-six, and Basil made one form

George of Vladimir, Rostislav-Michael of Kyiv, John of Uglich, Basil of
Rostov, Roman of Ryazan.

**Basil is باسل everywhere in the lives now.** The page settled it long ago on
the prayers, which print باسل twice and بازل never; but the commemoration of
the prince of Rostov writes دیندار شہزادہ بازل (واسلکو), and batch one
hundred and twenty-five had followed it for Anna of Kashin's son. That one
occurrence is corrected. The decision was made for the name, not for one
saint.

Written here for the first time: Big Nest بڑا گھونسلہ, Batu باتو, the
Monomashichi مونوماشچی, Olegovich اولیگووچ.

Carried from the site: جارج, وسیوولود, نیژنی نووگوروڈ, سیت دریا, اگاتھا,
روستیسلاو-میخائل, مستسلاو, ولادیمیر مونوماخ, سمولینسک, پولیکارپ, اگنیشیس,
پریلوکی, وولوگدا, واسلکو, سوزدال, شیرن, سنہری گروہ, خان, ریازان, روستوف,
سیرل.

## Batch one hundred and twenty-seven

Vladimir Yaroslavich of Novgorod, Juliana of Vyazma, the Righteous Abel, Anna
the Prophetess, Artemius of Verkola.

**Anna the Prophetess is حنا, off the Gospel.** The site gives her two forms
in her two commemorations, حنّہ and آنا, and neither is the published text's.
Luke 2:36 writes حنا, and a name that occurs in the Bible is read off the
text; حنّہ stays the name of Samuel's mother, whom the Old Testament writes
so, and آنا the name of the Theotokos' mother and the princess of Kashin.
Three women, three spellings, each from the body that names her.

Juliana of Vyazma is **جولیانا**, eight across the site against three
یولیانا; the یولیانا of her relics entry is outnumbered by her own other
commemoration and by the virgin martyrs.

Abel is **ہابل** and Cain **قائن**, from Genesis 4, and the life carries
Hebrews 11:4 and 12:24 and the phrase راستباز ہابل of Matthew 23:35 from the
published text. The verses used carry no divine name; Genesis 4:4 and 4:10
do, and are reported.

Written here for the first time: the Tvertsa تویرتسا, the Pinega پینیگا,
Phanuel فنوایل, Asher آشر, Simeon Mstislavich شمعون مستسلاووچ.

## Batch one hundred and twenty-eight

Athanasius of Novolotsk, the Righteous Benjamin, the Righteous Child Artemius
of Verkola, the Righteous Deborah, Eudocimus of Cappadocia.

The calendar carries Artemius of Verkola twice, once as a righteous man and
once as a righteous child, and each entry is written from its own English. The
two lives agree in every name and differ in what their sources tell.

Read from the published Old Testament: Ben-oni بن اونی, Benjamin بنیامین,
Rachel راخل, Ephrath افرات, Jabin یابین, Sisera سیسرا, Barak براق, Jael
یاعیل, Megiddo مجدو, Ramah رامہ, Deborah دبورہ. Genesis 49:27 and Judges 5:20
are carried whole; Judges 4:9 and 5:31 carry the divine name and are reported.

Written here for the first time: Kargopol کارگوپول, Olonets اولونیتس,
Petrozavodsk پیتروزاوودسک, the verst ورست, the semantron سیمانترون, the Vaga
واگا, Chorziane خورزیانے, Eudokia ایودوکیا.

Carried from the site: نوولوتسک کے اتھاناسیس, ویرخولیدسکایا سلوبودکا,
شینکرسک, ورکولا, ارتیمیس, پینیگا, ایودوکیمس, تھیوفیلوس, کپادوکیہ,
شمالی تھیبائیڈ.

## Batch one hundred and twenty-nine, the first of the Forefathers

Abraham, Adam, Arphaxad, Cainan, Eber. These are genealogy entries, and
almost every word in them is a name from the published Old Testament.

Read from the edition: Abram ابرام, Abraham ابراہام, Ur of the Chaldees
کسدیوں کا اور, Lot لوط, Sarah سارہ, Mamre ممرے, Machpelah مکفیلہ, Hebron
حبرون, Adam آدم, Eve حوا, Shem شم, Arphaxad ارفاکسد, Enos انوش, Cainan
قینان, Salah شلح, Eber عبر, Peleg پلگ.

Quoted whole: Genesis 12:3 and 5:5; Hebrews 11:8; John 8:56; 1 Corinthians
15:22. Quoted in part: Genesis 22:12 from تُو نے مجھ سے onward. Reported
because they carry the divine name: Genesis 15:6, 18:1 and 2:7.

The short Forefather entries are three or four sentences in the English and
are three or four in the Urdu. Where the source says only that a man stood in
the line and lived so many years, the life says that and stops; padding a
genealogy would be inventing a life.

## Batch one hundred and thirty, and the two patriarchs' names

Enoch, Enos, Isaac, Jacob, Jared.

**Abraham is ابراہام and Isaac is اصحاق, and the reasons differ.**

The vocabulary and the commemorations write the patriarch ابراہیم, eight
times, against three ابراہام. But one of those three is in the prayers, and
it is the Magnificat, جیسا اُس نے ہمارے باپ دادا سے کہا تھا، ابراہام اور اُس
کی نسل سے ابد تک, which is both the Church's own book and Holy Scripture
naming this very man. Two of the strongest bodies against the count of the
weakest, as with Basil; ابراہام stands.

Isaac is harder, because the site never names the patriarch at all. Its
thirteen اسحاق are other men, and three of them, the ones in the prayers, are
Isaac the Syrian. The only body that names the son of Abraham is the
published Old Testament, and it writes اصحاق throughout. So the patriarch is
اصحاق and every other Isaac keeps اسحاق, one name and several men, as with
Elizabeth and Anna. Batch one hundred and twenty-nine had written the
patriarch اسحاق and is corrected.

Read from the edition: Enoch حنوخ, Jared یارد, Mahalalel مہلل ایل, Seth شیت,
Rebecca ربقہ, Laban لابن, Leah لیاہ, Esau عیسو, Moriah موریاہ, Luz لوز.
Hebrews 11:5, Genesis 5:24, 22:7 and 22:8, 28:12, 28:19 and 32:28 are carried
whole; Genesis 4:26 and 28:16 carry the divine name and are reported.

## Batch one hundred and thirty-one

Lamech, Mahalalel, Methuselah, Nahor, Noah.

**Noah is نوحا, because nothing else on the site names him.** The vocabulary,
the commemorations, the glossary and the prayers have no Noah at all; the
published Old Testament writes نوحا throughout. This is the Isaac case again,
and the two lives that had already written نوح - the Georgian ark of survival
and the line from Noah to Abraham - are corrected.

Read from the edition: Lamech لمک, Methuselah متوسلح, Nahor ناحور, Serug
سروگ, Terah تیراح, Ham حام, Japheth یافیت, Ararat اراراط, gopher wood
صنوبر کی لکڑی, the dove فاختہ, the rainbow قوس قزح.

Genesis 6:9, 6:10, 6:14, 7:12, 7:24, 8:4, 8:11, 9:13 and 9:29 are carried
whole. Genesis 5:29, 6:5 and 6:8 carry the divine name and are reported.

## Batch one hundred and thirty-two

Peleg, Reu, Salah, Serug, Seth: the last of the short Forefather entries.

Read from the edition: Peleg پلگ, Reu رعو, Serug سروگ, Salah شلح, Seth شیت,
Joktan یقطان, Babel بابیل. Genesis 4:25, 5:8 and 10:25 are carried whole;
Genesis 11:9, which gives Babel its name, carries the divine name twice and
is reported.

The Reu entry says in the site's own voice why the Church keeps men of whom
nothing is written, and the Urdu says it in the same three clauses the
English uses. These entries are short because their sources are; nothing is
added to fill them.

## Batch one hundred and thirty-three, the first Foremothers

Terah, Bathsheba, Esther, Eve, Huldah.

Read from the edition: Terah تیراح, Haran حاران, Bathsheba بتشیبا, Uriah the
Hittite حتی اوریاہ, Nathan ناتن, Esther ایستر, Hadassah ہدساہ, Mordecai
مردکی, Susa شوشن, Huldah حلدہ.

**David stays داؤد and Solomon سلیمان outside the quotations**, as the site
writes them, though the edition heads them داوید and شلومون. The rule from
batch one hundred and ten holds in both directions: the edition is not
corrected inside its sentence and not imposed outside it.

Quoted whole: Genesis 3:15 and 3:20; Esther 4:14 and 4:16; 2 Kings 22:20 from
سلامتی کے ساتھ onward. Reported because they carry the divine name: Genesis
2:21, 2 Samuel 12:7.

Written here for the first time: Haman ہامان, Eliam الیعام.

## Batch one hundred and thirty-four

Judith, Leah, Rachel, Rebecca, Ruth.

**Judith is not in the published Urdu Old Testament**, which carries
thirty-nine books, so her account is told in the site's own prose and the
book is simply named یہودیت کی کتاب, as 2 Maccabees was named for Eleazar and
the Greek Daniel for Susanna. The vocabulary already writes یہودیت and
ہولوفرنیس in her icon line, and the life uses them.

Read from the edition: Ruth روت, Naomi نعومی, Boaz بوعز, Obed عوبید,
Elimelech الیملک, Jesse یشائی. Ruth 1:16, Genesis 24:58 and 29:20 are carried
whole; Jeremiah 31:15 opens with the divine name, so the life quotes it from
رامہ شہر میں onward, which is also where Matthew 2:18 begins it. Genesis
25:23 and 29:31 carry the divine name and are reported.

Rachel and Rebecca and Leah keep the forms settled in batch one hundred and
thirty: راخل, ربقہ, لیاہ.

## Batch one hundred and thirty-five

Sarah, Tamar, Hezron, Jael, James the Brother of the Lord.

**Where the two Testaments spell a genealogy name differently, the entry
follows the list it is standing in.** Genesis writes Perez پیریز and Hezron
حضرون; Matthew's genealogy writes فارص, حصرون and ارام. These entries are
about the Messiah's line, which is Matthew's list, so they take Matthew's
forms and Tamar's تامار with them.

Read from the edition: Sarah سارہ, Heber the Kenite حبر قینی, Hazor حصور.
Genesis 18:12, 23:1, 38:26; Judges 4:21 and 5:24; 1 Peter 3:4 and Hebrews
11:11 are carried whole. Genesis 18:14 carries the divine name and is
reported.

James and Joseph take the site's own titles: خداوند کا بھائی یعقوب and
منگیتر یوسف, both in the commemorations and in the icon line for this synaxis.

## Batch 136: Japheth, Job, Joseph the All-Comely, Joshua, Lot

Names of the patriarchs come off the published Old Testament, which is the
only body that carries them: یافیت, شم, نوحا, ایوب, عوض (Uz), حوران, عیسو,
پوطیفار, فرعون, نون, کالب, یریحو, جبعون, یردن, لوط, سدوم, کسدیوں کا اور.

Joseph keeps the site's یوسف. The edition writes یوسیف, but the name is on
the commemorations and in the prayers as یوسف, and a spelling inside a
quotation is not imposed on the prose around it. His epithet is the
vocabulary's نہایت حسین.

Joshua takes the edition's یہوشع: the site does not name him anywhere else,
so the published text decides. Moses stays موسیٰ in the prose, which is the
form the prayers and the commemorations carry, though the edition writes موشہ
inside its own verses.

Carried whole, because none of them names God with the word the edition uses
for Him and the site does not: Genesis 9:27, Job 1:1, Job 2:10, Job 19:25,
Job 19:26, Genesis 39:9, Genesis 45:5, Genesis 13:11, Genesis 19:26,
2 Peter 2:7, and the second half of Joshua 24:15.

Reported in the site's own prose rather than quoted: Job 1:21 and the first
clause of Joshua 24:15, which carry that name; and the sun standing still at
Joshua 10:13.

## Batch 137: Martha and Mary, Melchizedek, Miriam, Olga of Kwethluk, Asher

Martha is مرتھا. The vocabulary and the commemoration of this very entry
write it that way six times against three for مارتھا, and the published Gospel
agrees.

Miriam is مِریم, with the kasra, because that is the one place on the site
that names the sister of Moses, and it was written that way to keep her apart
from the Mother of God, whom every other body here calls مریم. The published
Old Testament gives both women the same spelling and so cannot decide it.

Abraham keeps ابراہام, the form the whole line of the forefathers already
carries here and the form the published text uses; the blessing quoted from
Genesis keeps ابرام, since Abraham had not yet been renamed when it was
spoken.

Asher is آشر in the prose. The vocabulary and the published Gospel both write
it so, and the tribe is already named that way in the life of the Prophetess
Anna; the blessing quoted from Genesis keeps the Old Testament's آشیر.

For the sons of Jacob the title is بزرگ. The site keeps سرپرست اعلیٰ for a
patriarch of a see, which is not what these men were, and جدِ امجد is already
carrying Forefather; the lives of the forefathers already use بزرگ of these
men when they speak of their ages.

Pharaoh stays فرعون and Aaron ہارون, as the life of the Prophet Moses has
them, though the published text writes فرعوہ and اہرون. Kadesh is قادس, the
Red Sea بحیرہ قلزم, and the Yup'ik people یوپک, from the life of Saint Jacob
Netsvetov. Michael, as Matushka Olga's married name, takes the site's میکائیل.

Bread and wine at Salem are روٹی اور مے, which is the phrase the glossary uses
of the offering; the published verse's انگوری شیرہ is not carried out of it.

Quoted whole: Luke 10:41-42, John 11:25, Hebrews 7:3, Genesis 14:19 and
Genesis 49:20. The Psalm on the priesthood after the order of Melchizedek is
carried only from its second half, and the songs of Exodus 15 and the rebuke
of Numbers 12 are reported in prose, because those verses name God with the
word the published text uses for Him and the site does not.

## Batch 138: Dan, Gad, Issachar, Judah, Levi

Levi is لاوی. The published Old Testament writes لیوی in the blessing of
Jacob, but لاوی is already on the site eight times over, in the life of the
Prophet Moses among others, and in the day entries. Issachar, whom no other
body here names, takes the published یسکار; so do Bilhah بلہاہ, Shechem
شکیم, Jezreel یزرعیل and Samson شمشون.

Perez is فارص, from the genealogy in the Gospel and from the life of the
Foremother Tamar, not the Old Testament's پیریز: the name stands here in the
line that runs to David, which is the list the Gospel gives.

Quoted whole: the blessing of Dan at Genesis 49:16, the words on the men of
Issachar at 1 Chronicles 12:32, the lion and the sceptre from Genesis 49:9-10,
and the Lion of the tribe of Judah from Revelation 5:5. The blessings of Gad
and of Issachar are reported in prose, since the published rendering of each
turns on a word the English entry does not have.

## Batch 139: Naphtali, Reuben, Simeon, Zebulun, Philaret the Merciful

Naphtali نفتالی, Zebulun زبولون, Reuben روبن, Bilhah بلہاہ and Dinah دینہ
come off the published text, which is the only body that names them; دینا is
the verb, not the name, and was not counted.

Paphlagonia is پفلاگونیا, on the vocabulary nine times against the one
پافلاگونیا of a commemoration. Philaret is فیلارت and Amnia امنیا, both from
his own commemoration. George is جارج, Maria ماریا, Irene ایرین. Hypatia is
ہیپاتیا, following the ہیپاتیوس the vocabulary already writes; Theoseba
تھیوسیبا and Evanthia ایوانتھیا follow the same ear for the Greek.

Granddaughter is پوتی. The site renders the same relation as پوتا where it
names Phinehas the grandson of Aaron, and the entry says only granddaughter,
so the word that carries no further claim about the line is the right one.

Quoted whole: the blessings of Naphtali and Zebulun at Genesis 49:21 and
49:13, the word to Reuben at 49:4, and the sentence on Simeon and Levi at
49:7. Isaiah's promise is given in the Evangelist's words at Matthew 4:16.
The Apostle's reminder is 1 Timothy 6:7 and David's assurance Psalm 37:25,
both carried in the site's prose rather than set as quotations, since the
entry reports them rather than citing them.

## Batch 140: Phineas, Aaron, Procopius of Ustiug, Shem, Simeon of Verkhoturye

Phineas is فینحاس in the prose, from his own commemoration; the published text
writes فنحاس, and that spelling stays inside the words quoted from Numbers.
Eleazar الیعزر, Moab موآب, Shittim شطیم, Baal-Peor پعور کا بعل, Midian مدیان,
Mount Hor کوہِ ہور and Korah قورح come off the published text. The hill
country of Ephraim is افرائیم کا پہاڑی علاقہ, and the place that bore his
name is described as the vocabulary already describes it.

Procopius is پروکوپیس and Ustiug اُستیوگ, both from the commemorations, as is
the Annunciation Icon of Ustiug, which the vocabulary names in full. Simeon of
Verkhoturye is شمعون, with ویرخوتوریے, میرکوشینو, دریائے تورا, یورال,
سائبیریا and توبولسک all standing in the vocabulary already.

Quoted whole: the word to Moses at Numbers 25:11-13 and the Psalmist's verdict
at Psalm 106:31. The blessing of Shem at Genesis 9:26 is reported instead,
since it names God with the word the published text uses for Him.

## Batch 141: Solomon, Tarasius of Liconium, Theodora, Glykeria, Glaphyra

Solomon is سلیمان, the form the vocabulary already uses of his throne; the
published text writes شلومون, and that stays inside its own verses. The temple
is ہیکل in the prose, as the lives already have it, and the edition's
بیت المقدس is not carried out of the quotation.

Tarasius is تراسیس and Liconium لیکونیم, from his commemoration; Lycaonia is
لکانیہ, which the vocabulary already writes of the country. Proverbs is امثال
and the Wisdom of Solomon حکمت سلیمان, the names the published index gives
them, and vespers is the glossary's شام کی دعا.

Theodora تھیودورا, Theophilus تھیوفیلوس and iconoclast شبیہ شکن all stand in
her own commemoration; Methodius میتھوڈیس, Corfu کورفو, the Seventh Ecumenical
Council ساتویں عالمی کونسل and the Triumph of Orthodoxy راست دینی کی فتح come
off the vocabulary. Her son Michael takes میکائیل, the site's form for the
name.

Glykeria گلیکیریا and Novgorod نووگوروڈ from her commemoration; Florus and
Laurus فلورس اور لورس from theirs; Panteleimon is پانتیلیمون, the vocabulary's
form against the one پنتیلیمون of a commemoration.

Glaphyra گلافیرا, Licinius لیکینیس, Nicomedia نیکومیڈیا, Amasea اماسیہ,
Pontus پونتوس and the bishop Basil باسل are all already on the site, the last
in the commemoration of his own martyrdom.

Quoted whole: the promise to Solomon at 1 Kings 3:11-12 and his prayer at
8:29. The appearing at Gibeon, the Lord's pleasure at the asking and the glory
filling the house are reported in prose, since those verses name God with the
word the published text uses for Him.

## Batch 142: John and Jacob of Meniugi, the Royal Passionbearers, Agapitos, Aidan, Akakios

Menyusha and Meniugi are one place; the site writes مینیوگی in the
commemoration and that is the form the life carries throughout.

The Royal Passionbearers are named exactly as their commemoration names them,
down to درد کش for passion-bearer; Yekaterinburg is یکاترینبرگ from the
vocabulary, and the Bolsheviks, whom the site does not name elsewhere, are
بالشویک.

Phrygia is فروگیہ, on the vocabulary twelve times against the three of the
commemorations, and Melitene ملیتینے, thirteen against five, though Agapitos'
and Akakios' own commemorations spell both the other way. A commemoration
naming one saint does not outweigh a form the site uses of the place itself.

Agapitos اگاپیتوس, Synnada سناڈا, and the martyrs وکتور، دوروتھیس، تھیوڈولس
اور اگریپا are all in the vocabulary's description of his icon. Decius is
دیقیوس, twice on the vocabulary against one ڈیسیس; Constantine قسطنطین;
Ephesus افسس.

Aidan ایڈن, Lindisfarne لنڈسفارن, Northumbria نارتھمبریا, Iona آئیونا,
Columba کولمبا and Ireland آئرلینڈ all stand already; Oswald is اوسوالڈ, from
the vocabulary.

## Batch 143: Alban, Alexander of Guria, Alexander of Constantinople, Alexei of Moscow, Ambrose

Alban is ایلبن and Britain برطانیہ, from his commemoration; Verulamium, which
the site does not name, is ویرولامیم.

The Georgian names all stand in the vocabulary already: گوریا, سامیگریلو,
ابخازیتی, تبلیسی, گوری, دیسیوی, شیو-مگویمے, زیدازینی, داویت-گاریجی, and
راستباز سینٹ ایلیا. Shemokmedi شیموکمیدی, Jvari جواری, Svetitskhoveli
سویتیتسخوویلی and Okropiridze اوکروپیریدزے are written here for the first
time. Kazan is کازان, on the vocabulary forty-two times against the six
قازان of the commemorations.

Arius is آریوس and his party آریوسی, as the lives already have them; Metrophanes
میتروفینس, Nicaea نیقیہ.

The metropolitan of Moscow is الیکسی here, because that is what his own
commemoration calls him; the site also writes ایلکسیس, in the commemoration of
the uncovering of his relics and in the vocabulary's list of the Moscow
hierarchs, exactly where the English says Alexis. Each entry takes the form its
own commemoration uses. With him stand پطرس، یونس، فلپ اور ہرموجینیس; کریملن,
چودوف and سنہری گروہ are the vocabulary's, and مولیبن the glossary's.

Ambrose ایمبروز, Milan میلان, Gervasius and Protasius گرواسیس اور پروٹاسیس,
Augustine آگسٹین, Theodosius تھیوڈوسیس, Thessalonica تھسلنیکے and Justina
جسٹینا all stand already; Trier ٹریر, Liguria لیگوریا and Aemilia ایمیلیا do
not and are written here.

## Batch 144: Amphilochius of Vladimir, Amphilochius of Iconium, Anastasia the Patrician, Anastasius, Andrew of Crete

Amphilochius is امفیلوکیس, the form already in the lives three times over and in
the commemoration; Vladimir in Volhynia takes ولادیمیر, from that same
commemoration, though the vocabulary writes وولودیمیر of the town. Iconium is
اکونیوم, twice on the vocabulary against the one اِکونیم of a commemoration.

Two forms in the vocabulary's description of Anastasia's icon are outvoted by
the site's own weight elsewhere: Justinian is جسٹینین, three times over against
one یوستینیان, and Scetis اسقیطس, fifty-two times against one سکیتس. An icon
description is one line; the place is written across the whole shelf.

Strumica is سٹرومیتسا, from Anastasius' own commemoration; Radoviste رادوویشتے
is new. Andrew of Crete is اندریاس, Crete کریٹ, Mytilene میٹیلین, the Great
Canon عظیم قانون and the Holy Sepulchre مقدس قبر, all standing already.

Eunomius یونومیس, Macedonius مقدونیوس and Arcadius آرکیڈیس are written here
for the first time.

Her opening was rewritten to name Anastasia راہبہ. The register check reported
her as a monastic introduced by another rank, and it is right: اشرافی is a
worldly title, not an order, and she died a nun in a cave.

## Batch 145: Angelina of Serbia, Anthony of Krasny Kholm, Antiochus, Archippus, Arkadios

Angelina اینجلینا, Stephen Brankovic سٹیفن برانکوویچ, Krushedol کروشیدول and
Sirmium سرمیم are all on the site; her opening carries جلیل القدر, since the
index types her a nun and she died one, and her commemoration gives her no rank
at all.

Anthony of Krasny Kholm کراسنی خولم, with the Antoniev monastery انتونیف,
Tver تویر and the White Lake سفید جھیل, all from the vocabulary; the Mologa
مولوگا is written here.

Antiochus انطیوکس, the Great Lavra of Saint Sabbas سینٹ ساباس کا عظیم لاورا,
Galatia گلتیہ, Ancyra انقرہ and Eustathius یوستاتھیس all stand already. Great
Compline is بڑی کمپلین, the glossary's own phrase. The petition that comes down
under his name is reported, not quoted: the site publishes no Urdu text of it,
and a prayer that has not been received in the language is not set in
quotation marks here.

Archippus ارخپس, Hierapolis ہیراپولس, Colossae کلسے and the Chief Commander
مہاراست فرشتہ میکائیل come off the commemorations. Arsinoe is ارسینوئے, four
times on the vocabulary against the one ارسینوے of a commemoration; Arkadios
ارکادیوس, Nikon نکون and Theosebios تھیوسیبیوس are the vocabulary's.

## Batch 146: Arsenius of Tver, Artemon of Seleucia, Athanasius of Lubensk, Athanasius the Great twice

Arsenius ارسینیس, Tver تویر, the Zheltikov monastery ژیلتیکوف and the
Paterikon پاتیریک all stand in the vocabulary; Metropolitan Cyprian is کپرین,
from his own commemoration, and the Tmaka تماکا is written here.

Artemon ارتیمون, Seleucia سلوکیہ and Pisidia پسیدیہ come off the
commemorations and the vocabulary.

Athanasius Patellarios of Lubensk اتھاناسیس، لوبینسک کے, with لوبنی, مگار,
خارکیو and ریتھمنون, is described in the vocabulary down to the seated relics.
Crete stays کریٹ, the form Andrew of Crete's commemoration gives and this file
already carries, though the vocabulary writes کریتی of Rethymnon's island.

Athanasius the Great اتھاناسیس اعظم, Alexandria اسکندریہ, Cyril سیرل, Anthony
the Great انتھونی اعظم, Julian the Apostate مرتد جولین and Valens والنس all
stand already. Homoousios is ہم ذات, the phrase the lives already use of the
Son five times over, and Constantius قسطنطیوس as they already write him. Tyre
is صور, Trier ٹریر; Sardica ساردیکا is new.

The two entries for Athanasius are the January feast and the May one, and each
is written to what its own English says: the first ends with Cyril and the
Creed, the second with the arithmetic of the exiles.

## Batch 147: Averkios, Barsanuphius of Tver, Basil of Poiana Marului, Basil of Parium, Basil the Great

Basil is باسل, and the count is close enough to be worth writing down properly:
باسل thirty-six across the five bodies against بازل thirty-three, and the
prayers, which decide a near-level case, have باسل twice and بازل never. Three
of the four Basils in this batch are spelled بازل in their own commemorations;
the file's fifty-four باسل and the prayers outweigh them.

Averkios is اویرکیوس and his city ہیروپولِس, both from his own commemoration.
The site keeps this apart from the ہیراپولس of Archippus, which is a different
place, and the distinction is left standing rather than levelled.

Barsanuphius بارسانوفیس, Serpukhov سرپوخوف, Gurias گوریاس and Tver تویر are on
the site; Pesnosha پیسنوشا is written here.

Poiana Marului پویانا مارولوئی, Buzau بوزاؤ, Paisius Velichkovsky پائسیوس
ولچکووسکی, Gregory of Sinai سینا کا گریگوری and Nilus of Sora سورا کا نیلس all
stand already; نیلس beats نیلوس nine to four, and the lives already carry it
five times. Wallachia والاخیہ is new.

Parium پاریم, Macrina مکرینا, Athens ایتھنز, Mesopotamia میسوپوٹیمیا, the
Euphrates فرات, the Hellespont ہیلیسپونٹ, Marcus Aurelius مارکس اوریلیس and
the Three Holy Hierarchs تین مقدس سردار کاہن are all the site's. The Basiliad
باسیلیاد is new.

Basil of Poiana Marului opens as جلیل القدر: the register check reported him a
monastic named by another rank, and the index types him an igumen.

## Batch 148: Basil of Zakholmsk, Boniface the Merciful, Brannock, Bucolus, Caesarius

Zakholmsk زاخولمسک, Zahumlje زاہوملیے, Montenegro مونٹینیگرو, Ostrog اوستروگ,
Tvrdos تورڈوش, Pec پیچ and the Prologue پرولوگ are all on the site, several of
them in the vocabulary's own note that the two entries are one saint. Menaion
is مینایون, the glossary's; Mrkonjici مرکونیچی and Stojan Jovanovic
سٹویان یووانوویچ are written here.

Boniface بونیفیس, Ferentino فیرینتینو, Gregory the Great گریگوری اعظم and the
Dialogues مکالمات come off the commemorations and the vocabulary. Cana is
کانا, off the published Gospel.

Brannock برانوک, Braunton براؤنٹن, Devon ڈیون and Wales ویلز stand already;
Brychan بریخان and Brittany بریتانی are new. His opening carries جلیل القدر,
the index typing him Venerable.

Bucolus بوکولس, Smyrna سمرنا, Polycarp پولی کارپ and John the Theologian
یوحنا عالمِ الٰہیات are the site's.

Caesarius کیساریس, Nazianzus نازیانزوس, Nonna نونا, Gregory the Elder
گریگوری بزرگ, Julian the Apostate مرتد جولین and Valens والنس all stand;
Bithynia is بتھینیا, the unpointed form the lives carry sixteen times.

Also corrected: the Lord's command in the life of Basil of Parium, written last
batch in my own words, now reads as the published Gospel has it at Matthew
10:23. Where the site publishes the verse, the verse is what the life carries.

## Batch 149: Charitina, Clement of Ochrid, Clement the Stylite, Cosmas of Maiuma, Cosmas of Chalcedon

Charitina خاریتینا and Lithuania لتھوانیا come off her commemoration; Sinich
hill سینچ is new. Her opening carries راہبہ, since the entry makes her an
abbess and the commemoration gives her only شہزادی.

The five enlighteners are named exactly as their joint commemoration names
them, کلیمنٹ، ناحوم، ساوا، گورازد اور انگیلار, with اوہرد, عظیم مقدونیہ,
موراویا, بلغاریہ and سلاوی زبان, the last being the phrase the lives already
use of the tongue Cyril gave letters to. Boris is بورس, ten times in the lives.

Boeotia is بویوتیا, four times on the vocabulary against the one بوئیشیا of
this saint's own commemoration; both bodies describe the same man and disagree,
and the place is written oftener than the entry. Sagmata ساگماتا and Thebes
تھیبس complete it.

Cosmas the Hymnographer نغمہ نگار کوسماس, Maiuma مایوما, Gaza غزہ and John of
Damascus دمشق کا یوحنا all stand. The hymn the Mother of God came to thank him
for is quoted from the site's own published prayer, تو کروبیوں سے زیادہ
قابلِ تعظیم ہے, and not rendered afresh.

Cosmas of Chalcedon کوسماس, Auxentius اوکسینتیس, Chalcedon کلقیدون, Leo the
Armenian لیو ارمنی and the Fourth and Seventh Councils are all the site's, the
first two down to the vocabulary's description of the pair standing together.

## Batch 150: Cyril of Alexandria, Cyril of Jerusalem, Cyril of Catania, Cyril of Turov, David of Thessaloniki

Cyril is سیرل throughout, thirty-two across the bodies against five کیرل, even
though the commemoration of Cyril of Turov writes کیرل. Thessalonica likewise
stays تھسلنیکے, fifty-six against eleven, though David's own commemoration
writes تھیسالونیکی. Neither count is near enough for a commemoration to
decide it.

Theotokos is والدہ خدا, the site's ordinary word, not the تھیوٹوکوس of one
commemoration. Golgotha گلگتا, the Mount of Olives زیتون کا پہاڑ, Ephesus
افسس, Catania کاتانیا, Antioch انطاکیہ and Turov تورو all stand already, the
first two in the vocabulary's own description of the cross of light. Marah is
مارہ, off the published text and already in the lives.

Chrysostom is زریں دہن; Nestorius نسطوریس is new. Dendrite is rendered
درخت نشین, on the pattern of the site's ستون نشین for a stylite, rather than
carried over as a Greek word the site has never used.

David of Thessaloniki opens as جلیل القدر, the index typing him a monk.

## Batch 151: Dionysios the builder, Dionysius of Suzdal, Dometian, Donatus, Eleni of Lesbos

Dionysiou دیونیسیو, Korissos کوریسوس, Kastoria کاستوریا, Philotheou فیلوتھیو
and Trebizond ترابزون are all on the site; ترابزون beats ٹریبیزونڈ seven to
one in the lives alone.

Suzdal سوزدال, Nizhny Novgorod نیژنی نووگوروڈ, the Pechersky monastery پیچرسکی,
Euthymius یوتھیمیس and Macarius of Zheltovod ژلتوود کا مکاریس all stand, most
of them in the vocabulary's description of this saint's own icon. The
Laurentian Chronicle is لاورینتی تاریخ نامہ.

Melitene ملیتینے and Dometian دومیتیان are settled; Justin the Younger takes
جسٹن, the form the lives already use of that emperor five times.

Donatus دوناتس, Euroea یوروئیا and Epirus ایپیروس come off his commemoration
and the vocabulary's account of the serpent at the spring. Chamaigephyrai
خامائیگیفیرائی is written here.

Eleni ایلینی and Susanna سوسانہ are given in her own commemoration, with
لیسبوس; Raphael رافایل, Nicholas نکولس and Irene ایرین stand already, and
Thermi تھرمی is new.

Dionysios the builder opens as جلیل القدر: مقدس معمار was flagged by the
register check, and rightly, since معمار is a trade and not an order.

## Batch 152: Emilia, Emilian of Rome, Emilian of Cyzicus, Emmeleia, Ephraim of Antioch

Emilia and Emmeleia are one saint under two English names, and both entries
take ایمیلیا, which is what the site's commemoration gives. Each life is
written to what its own English says.

Her household is named as the site already names it: باسل اعظم, نیصا کا
گریگوری, سیباستے کا پطرس, مکرینا, باسل بزرگ, معجزہ گر گریگوری, دیوکلیشین,
and انیسا on the Pontus. Naucratius ناوکراتیس, Theosebia تھیوسیبیا and the
Iris ایریس are written here.

Cyzicus is کیزیکس, eleven times across the bodies against two کزیکس, though
Emilian's own commemoration writes the shorter form.

Monophysite is یک طبیعتی, the phrase the lives already use of the error;
Ephraim افریم, Anastasius اناستاسیس, Chalcedon کلقیدون and Antioch انطاکیہ
all stand. Victorinus ویکٹورینس is new, and the Count of the East is rendered
مشرق کا کاؤنٹ with the office explained beside it.

Emilia and Emilian of Rome both open as جلیل القدر, the index typing her
Venerable and him a monk, and both being received by the Church as monastics.

## Batch 153: Epiphanius of Cyprus, Eulogius the Hospitable, Eulogius of Alexandria, Eumenius, Euphrosyne of Moscow

Epiphanius ایپیفانیس, Cyprus قبرص, Hilarion the Great ہیلاریون اعظم,
Eleutheropolis ایلیوتھروپولس and the Panarion پناریون all stand on the site,
the last two in the vocabulary's description of his icon. Besanduc بیساندوک,
Constantia کونستانتیا and Salamis سلامیس are written here; Pentaglot is given
as پانچ زبانوں والا rather than carried over.

Eulogius is یولوگیس in both entries, from their own commemorations; Abba
Daniel ابّا دانیال and Scetis اسقیطس stand as settled, and Justin is جسٹن.

Gregory the Dialogist مکالمہ نگار گریگوری and the Tome of Leo لیو کا مکتوب
are the vocabulary's. Severian سیویری and Novatianist نوواتیانی are new.

Eumenius یومینیس, Gortyna گورتینا, Crete کریٹ, the Thebaid تھیبائیڈ and Cyril
سیرل all stand; Raxos راکسوس is new.

Euphrosyne of Moscow is یوفروسینے, from her own commemoration; Eudokia is
یودوکیا, six times in the lives already, against the ایودوکیا of another
entry's commemoration. Dmitry Donskoy دیمتری دونسکوئے, Alexis الیکسی, Sergius
of Radonezh رادونیج کے سرجیئس, the Vladimir Icon ولادیمیر آئیکن, Tamerlane
تیمور and the Kremlin کریملن all stand. Kulikovo کولیکووو and Tokhtamysh
تختامش are new.

## Batch 154: Euschemon, Eustathius of Bithynia, Eustathius of Antioch, Euthymius of Novgorod, Eutychius of Melitene

Euschemon یوسکیمون and Lampsacus لیمپساکس come off his commemoration; Theodore
the Studite اسٹودیت تھیوڈور and the Studion سٹودیون are the site's.

Eustathius is یوستاتھیس in both entries, the form already eight times in the
lives; Bithynia بتھینیا, Side سیدے, Pamphylia پامفیلیا, Beroea بیریہ,
Meletius میلیتیس, Eusebius یوسیبیس and Thrace تھریس all stand already.
Trajanopolis تراجانوپولس is new. Endor is عین دور, off the published text,
where the woman Saul consulted lived.

Euthymius یوتھیمیس, Vyazhishchi ویاژشچی, Jonah یونس and Pachomius پاخومیس all
stand, the second in the vocabulary's account of the grave opened to read the
letter of pardon. Grammota is given as معافی کا خط, since the site has no
Slavonic chancery word and the entry means only a letter.

Eutychius یوتیخیس, Melitene ملیتینے, Armenia Minor چھوٹا آرمینیا and the
Menaion مینایون are all on the site.

## Batch 155: Eutychius of Constantinople, Flavian the Confessor, Flavian of Antioch, Frumentius, Fulvian

The Tome of Leo is لیو کا طومس. The vocabulary writes it both ways, طومس in
the line about Flavian, to whom it was addressed, and مکتوب elsewhere; طومس is
the term for the document and the general word is not, so the file now uses it
throughout, and the one مکتوب written in the life of Eulogius of Alexandria has
been changed to match.

Eutychius یوتیخیس, Amasia اماسیہ, the Fifth Ecumenical Council پانچویں عالمی
کونسل, Justinian جسٹینین and Phrygia فروگیہ all stand. Menas مینس, Justin the
Second جسٹن دوم and the Aphthartodocetae افتارتودوکیت are new; the last is
carried as a name with its teaching stated beside it.

Flavian فلاویان and the Robber Council ڈاکو کونسل come off the commemorations
and the vocabulary. Eutyches is یوتیخس, which the site keeps distinct from the
یوتیخیس of the patriarch; Dioscorus ڈیوسکورس, Leo the Great لیو اعظم, Lydia
لیدیا and Chalcedon کلقیدون all stand. Chrysaphius کرساپھیوس, Hypaepa ہیپائپا
and Pulcheria پلخیریا are new.

Meletius میلیتیس, Chrysostom زریں دہن, Antioch انطاکیہ and Theodosius
تھیوڈوسیس all stand for the second Flavian.

Frumentius فرومینتیس, Abyssinia ابیسینیا, Ethiopia ایتھوپیا, Aksum اکسوم,
Tyre صور, the Red Sea بحیرۂ قلزم and Athanasius اتھاناسیس are the site's;
Aedesius ایدیسیس and Ezana ایزانا are new, and Abba Salama and Kesate Birhan
are carried as the Ethiopian Church says them, with their sense given beside.

Fulvian فلویان and Matthew متی are from his own commemoration; Platon پلاتون
is new.

## Batch 156: Gennadius, George Matskvereli, George of Pisidian Antioch, George of Mytilene, George of Amastris

Gennadius is گیناڈیس, written here for the first time and shaped on the site's
own habit with Greek names in Ge-, as in گورازد, گریگوری and گوریاس. Daniel
the Stylite ستون نشین دانیال, Marcian مارکیان, the Studite house اسٹودیت and
Eleutherius ایلیوتھیریس all stand; simony is given as the vocabulary already
gives it, کلیسائی مناصب کی خرید و فروخت.

The Georgian names come off the vocabulary's own description of this saint:
جارج ماٹسکیویریلی, آتسکوری, سامتسخے, کلارجیتی, خندزتا کا گریگول, زرزما کا
سراپیون, and رسول آندریو with the Atskuri icon. George Merchule مرچولے,
Basil of Zarzma, the Shuartqeli شوارتقیلی, Opiza اوپیزا and George Chorchaneli
چورچانیلی are new.

Constantine Copronymus is قسطنطین کوپرونیموس, four times in the lives against
one کوپرونیمس; Leo the Armenian لیو ارمنی, Nikephoros نکیفوروس, Mytilene
میٹیلین, Amastris اماستریس, Tarasius تراسیس, Paphlagonia پفلاگونیا, the
Saracens سراسین and the Rus روس all stand already. Kromna کرومنا is new, and
the Standard-Bearer is rendered علم بردار.

## Batch 157: Gerasimus of Perm, Germanus of Auxerre, Germanus of Constantinople, Gregory the Dialogist, Gregory the Theologian

Gerasimus گیراسیمس, Perm پرم, Stephen of Perm پرم کا سٹیفن, Ust-Vym اُست-وِم,
Pitirim پتیریم and Jonah یونس all stand on the site. The Zyrians زیری and the
Voguls ووگل are new.

Auxerre is اوسیر, five times on the vocabulary against the two اوکسر of its
commemorations. Germanus is جرمانس, seven times in the lives already, and it
serves both saints of that name. Ravenna راونا and Gaul گال stand; Honorius
ہونوریس, Amator اماتور, Celestine سیلیسٹین, the Pelagians پیلاجی, the Saxons
ساکسن, the Picts پکٹ and Armorica آرموریکا are new.

Heraclius ہیراکلیس, Cyzicus کیزیکس and the Seventh Council all stand; Leo the
Isaurian is لیو اسورین, new here.

Gregory the Dialogist مکالمہ نگار گریگوری, the Liturgy of the Presanctified
Gifts پیش تقدیس شدہ نذروں کا قداس, Benedict of Nursia نرسیا کا بینیڈکٹ and
Augustine آگسٹین are the site's. The Caelian کائیلین, Hadrian's mausoleum,
the Lombards لمبارڈ and the Angles انگل are new; the Pastoral Rule and the
Moralia on Job are given by their sense, چرواہی کا قاعدہ and ایوب پر اخلاقیات,
since the site has no titles for them.

Gregory the Theologian گریگوری عالمِ الٰہیات, Arianzus اریانزوس, Nazianzus
نازیانزوس, Nonna نونا, Gregory the Elder گریگوری بزرگ, Basil باسل, Athens
ایتھنز and Meletius میلیتیس all stand. Symeon the New Theologian is
نیا عالم الٰہیات شمعون, exactly as his own commemoration has him. Sasima
ساسیما and the Anastasia chapel اناستاسیا are new.

## Batch 158: Gregory of Alexandria, Gregory of Agrigentum, Gregory of Nyssa, Gregory the Wonderworker, Gurias of Kazan

Agrigentum اگریجینتم, Pretorium پریتوریم and Sicily سسلی come off his
commemoration and the vocabulary. Chariton is خاریتون, four times across the
vocabulary and the lives against the two خریطون of commemorations; Theodota is
تھیوڈوتا. Ecclesiastes is واعظ, the name the published index gives the book.

Nyssa نیصا, Eunomius یونومیس, Valens والنس, Theodosius تھیوڈوسیس, Emilia
ایمیلیا and Macrina مکرینا all stand. Basil's Hexaemeron is given by its
subject, چھ دنوں کی تخلیق پر تفسیر, since the site has no title for it.

Neocaesarea نیوقیصریہ, Origen اوریجن, Pontus پونتوس and Decius دیقیوس all
stand; the Lycus لیکس is new.

Gurias گوریاس, Radonezh رادونیج, Kazan کازان, the Joseph-Volokolamsk monastery
یوسف وولوکولامسک, Barsanuphius بارسانوفیس, Hermogenes ہرموجینیس and the Volga
وولگا are all the site's. Rugotin روگوتین and Ivan Penkov ایوان پینکوف are
new.

## Batch 159: Hilarion of Tvali, Hilarion of Suzdal, Hosius of Cordoba, Hypatius of Gangra twice

Hilarion is ہلاریون for both, the form already in the lives; Tvali ٹوالی and
Khakhuli خاخولی come off his commemoration and the vocabulary, خاخولی six
times against one کھاخولی. George of the Holy Mountain is مقدس پہاڑ کا جارج;
Tulashvili تولاشویلی is new. His opening carries جلیل القدر, the index typing
him an igumen.

Suzdal سوزدال, the Florishchev hermitage فلوریشچیو and Nizhny Novgorod
نیژنی نووگوروڈ all stand; Yuriev یوریف, Gorokhovets گوروخوویتس and Feodor
Alekseevich فیودور الیکسییویچ are new.

Hosius ہوسیس, Cordoba قرطبہ, Spain ہسپانیہ, Sirmium سرمیم and Constantius
قسطنطیوس all stand already.

Hypatius of Gangra is ہپاتیس, which both of his commemorations give and which
the lives already carry; the site's one ہیپاتیوس belongs to another man, and
the two spellings are left standing for the two people. Gangra گنگرا,
Paphlagonia پفلاگونیا, the Ipatiev monastery ایپاتیف, Kostroma کوسترما
(thirteen against three), the Novatians نوواتیانی, the Protomartyr Stephen
اولین شہید اسٹیفن and Abel ہابل are all the site's.

## Batch 160: Ignatius of Rostov, Ignatius of Constantinople, Illyricus, Innocent of Komel, Isaac of Spoleto

Ignatius is اگنیشیس, sixteen times on the site and twelve in the lives; Rostov
روستوف stands. Nicetas نیکیتاس, Michael Rangabe میکائیل رانگابے and Bardas
باردس are new.

Illyricus الیریکس, Myrsinon مرسینون and Peloponnesus پیلوپونیسس come off his
own commemoration; the site also writes پیلوپونیس of the peninsula in another
entry, and each keeps the form its own commemoration gives.

Innocent of Komel is انوکینتی, on the pattern of the ایکینتیس and انوکینتیس
the commemorations already use of that name in the north; Komel کومیل,
Vologda وولوگدا, Nilus of Sora سورا کا نیلس, Cyril of the White Lake
سفید جھیل کا سیرل and John the Forerunner یوحنا پیش رو all stand. The
Okhlyabinin اوخلیابینن are new.

Spoleto is سپولیتو, four times against two اسپولیتو, and Isaac the Syrian
keeps اسحاق, which the site uses for him and holds apart from the اصحاق of
the patriarch. Monteluco مونتے لوکو and Gregory the Dialogist
مکالمہ نگار گریگوری are the vocabulary's.

## Batch 161: Isaiah of Rostov, James of Catania, James of Rostov, Joanna, Joannicius of Devich

Isaiah is یسعیاہ and James یعقوب, both long settled in the lives; Rostov
روستوف, Suzdal سوزدال, Lake Nero نیرو جھیل, Catania کاتانیا, Etna ایتنا and
Markian مارکیان all stand. Nikita نکیتا is new.

Joanna is یوآنا, the form her own commemoration gives, not the یوأنہ of the
published Gospel; Chuza takes the Gospel's خوزہ, since no other body names
him. Herod ہیرودیس and Herodias ہیرودیاس stand already, as does
خوشبو لانے والی for myrrh-bearing.

Joannicius جوانیکیس, Devich دیویچ, Kosovo کوسوو and Zeta زیتا stand. Drenica
is written درینیتسا, the form the vocabulary uses when naming the place
itself; it also writes درنیتسا once inside an icon description, and the place
label is preferred for a place. Crna Reka is given as کرنا ریکا with its sense
beside it, and George Brankovich as جارج برانکوویچ, the surname already on the
site.

## Batch 162: Joasaph of Belgorod, John Chrysostom, John of Tobolsk, John of Shanghai, John of Khakhuli

Joasaph یوآساف, Belgorod بیلگوروڈ, Poltava پولتاوا, Lubny لوبنی and the
Trinity-Sergius Lavra تثلیث-سرجیئس لاورا all stand; Pryluky پریلوکی, the
Gorlenkos گورلینکو and Joachim یوآخم are new.

Chrysostom زریں دہن, Antioch انطاکیہ, Anthusa انتھوسا, Comana کومانا,
Cucusus کوکوسوس and Libanius لیبانیس all stand; Eudoxia یودوکسیا and Pityus
پیتیئس are new.

Tobolsk توبولسک, Nizhyn نیژین, Chernihiv چرنیہیو, Peking بیجنگ, Shanghai and
San Francisco شنگھائی اور سان فرانسسکو, Kharkiv خارکیو and Belgrade بلغراد
all stand; the Kursk-Root icon is کرسک-جڑ, from its own commemoration, and
Seattle سیئٹل is new. The Iliotropion is named by its meaning, سورج مکھی,
which is what the entry itself explains it to be.

Khakhuli stays خاخولی, as settled three batches ago, though this saint's own
commemoration writes کھاخولی; the count is six to one. Oqropiri اوقروپیری is
his commemoration's. Tao تاو is the vocabulary's; David Kuropalates
داویت کوروپالاتیس, Bagrat the Third باگرات سوم and the Tortumi تورتومی are new.

The register check lists John of Khakhuli as a monastic named by another rank,
and he keeps سردار کاہن: the site's own vocabulary calls him a hierarch of
Khakhuli and his English title does the same, which is exactly the case the
check leaves to a reader rather than calling an error.

## Batch 163: John the Chozebite, John the Merciful, John the Russian, John of Novgorod, John of Polybotum

Choziba خوزیبا, George the Chozebite خوزیبا کا جارج, Jericho یریحو, Thebes
تھیبس and Caesarea in Palestine فلسطین کا قیصریہ all stand.

Amathus is اماتھوس, twice on the vocabulary against one اماتھس; John the
Merciful is رحم دل یوحنا, from his own commemoration.

Euboea is یوبویا, three times on the vocabulary against the one ایوبویا of
his commemoration; Prokopion پروکوپیون and New Prokopion نیو پروکوپیون are the
vocabulary's, as is the account of the relics carried across in the exchange
of populations. Peter the First پطرس اوّل and the Pruth پروت are new.

Novgorod نووگوروڈ, Suzdal سوزدال, the Volkhov وولخوف, Gabriel جبرائیل and the
Holy Wisdom cathedral مقدس حکمت all stand; the feast of the Sign is
نشان کی عید, the wording the site uses of that icon. Ilyina street is
ایلینا گلی, new.

Polybotum پولیبوتم, Phrygia فروگیہ and Leo the Isaurian لیو اسورین all stand.

## Batch 164: John of Suzdal, John of the Goths, John the Faster, John-Vladimir, Jonah the Presbyter

Suzdal سوزدال, Nizhny Novgorod نیژنی نووگوروڈ, the Volga وولگا and Bogolyubov
بوگولیوبووو all stand.

The Goths گوتھ, the Khazars خزر, the Crimea کریمیا and Georgia جارجیا all
stand, the first two in the vocabulary's own note about that see.

John the Faster is روزہ دار یوحنا and Paul the New نیا پولس, both from the
vocabulary line that pairs them.

John-Vladimir جان-ولادیمیر, Dioclea دیوکلیا, Zeta زیتا, Elbasan البسان,
Albania البانیہ, Tsar Samuel زار سموئیل and Kosara کوسارا all stand; Ivan
Vladislav ایوان ولادیسلاو is new.

Jonah یونس, Theophanes the Hymnographer نغمہ نگار تھیوفینس, Theodore Graptus
تھیوڈور گراپتس with his epithet داغ دار, and the Lavra of Saint Sabbas all
come off the commemorations.

## Batch 165: Jonah of Perm, Jonah of Moscow, Julian of Le Mans, Julius and Julian of Novara, Justinian

Perm پرم, Stephen of Perm پرم کا سٹیفن, Ust-Vym اُست-وِم and the Zyrians زیری
all stand; the Vychegda وچیگدا and the Vym وِم are new.

Jonah یونس, Ryazan ریازان, Galich گالچ, Isidore اسیدور and the Kremlin کریملن
all stand; Florence فلورنس is new.

Cenomanis سینومانس, Le Mans لے مان and Gaul گال come off his commemoration and
the vocabulary; Simon the Leper is شمعون کوڑھی, off the published Gospel.

Novara نوارا, Aegina ایجینا, Lake Orta اورتا جھیل and San Giulio سان جیولیو
are all the vocabulary's, as are the brothers کاہن جولیس اور شماس جولین;
Piedmont پیئدمونت is new.

Justinian جسٹینین, Hagia Sophia ایا صوفیہ with مقدس حکمت کا کلیسا, Theodora
تھیودورا, Origen اوریجن and the Fifth Council all stand; Illyricum اِلّیریکم
and Tauresium تاوریسیم are new.

His hymn is named, not quoted: اکلوتا بیٹا اور خدا کا کلام is the title of a
work, which a life may carry, and the site publishes no Urdu text of the hymn
itself. The word at the consecration of the Great Church is reported speech
from the tradition, not a liturgical text, and is given as the entry gives it.

## Batch 166: Juvenal of Jerusalem, Kevin of Glendalough, two Laurences of the Caves, Leo of Cappadocia

Euthymios the Great یوتھیمیس اعظم, Marcian مارکیان, Nestorius نسطوریس,
Eutyches یوتیخس, Eudokia یودوکیا and Simeon the Stylite شمعون ستون نشین all
stand; Juvenal جووینال is new.

Kevin کیون, Glendalough گلینڈالو, Leinster لینسٹر and Ireland آئرلینڈ come off
his commemoration and the vocabulary, the last describing the bird nesting in
his hand.

Laurence is لارنس for both, six times in the lives already; the Far Caves
دور کے غار, Turov تورو, Demetrius دیمیتریس (twenty-five times) and the
Paterikon پاتیریک all stand. The two are kept apart in the second life exactly
as the English keeps them apart.

Leo of Cappadocia لیو and the Saracens سراسین stand. His opening now carries
راہب شہید, the index typing him a monk and martyr and the entry itself telling
how he was killed. The Lord's word about greater love is quoted from the
published Gospel at John 15:13, not rendered afresh.

## Batch 167: Leo the Great, Leo of Catania, Liberius, Luke of Simferopol, Macarius the Roman

Leo the Great لیو اعظم, the Tome طومس, Flavian فلاویان, Chalcedon کلقیدون,
Attila اتیلا and Aquileia اکویلیا all stand, the last two in the vocabulary's
own description of the meeting at the river. Gaiseric گائزریک, the Vandals
وینڈل, the Huns ہن and the Mincio مِنچو are new.

Leo of Catania لیو, Catania کاتانیا, Etna ایتنا, Agatha اگاتھا, Elijah ایلیاہ
and Babylon بابل all stand; Heliodorus ہیلیودورس is the commemorations'.

Liberius لیبیریس is new; Julius جولیس, Constantius قسطنطیوس, Sirmium سرمیم
and Athanasius اتھاناسیس all stand.

Luke is لوقا, twenty-one times in the lives; Voino-Yasenetsky وائنو-یاسینیتسکی,
Simferopol سمفیروپول and the Crimea کریمیا come off the vocabulary. Valentin
Feliksovich والنتین فیلکسووچ is new.

Macarius the Roman رومی مکاریس and Mesopotamia میسوپوٹیمیا come off his
commemoration; Theophilus تھیوفیلوس and Sergius سرجیئس stand, and Hyginus
ہائجینس is new.

## Batch 168: Makarios the Roman, Marcian of Cyrrhus, Marcian the Presbyter, Mardarije, Mariamne

The site names two Romans called Macarius and spells them differently in their
own commemorations, رومی مکاریوس for the hermit of the Lezna and رومی مکاریس
for the elder of Mesopotamia; both forms stand, one to each man, as the site
already has them.

Alexander of Svir سویر کا الیگزینڈر, the Lezna لیزنا and Novgorod نووگوروڈ all
stand.

Cyrrhus is قورس in this entry, from his own commemoration, though the
vocabulary writes کوروس of the place and another commemoration سیرس; three
forms, none of them a majority, and the entry's own decides. Chalcis خالکیس
stands, as do Eusebius یوسیبیس and Agapitus اگاپیتوس.

Marcian the Presbyter پادری مارکیان, the Great Martyr Anastasia the Deliverer
from Poisons زہر سے چھڑانے والی عظیم شہید اناستاسیا, and Hagia Sophia
ایا صوفیہ all stand.

Mardarije مرداریے with اسکوکووچ, Libertyville لبرٹی ول, Sebastian of Jackson
جیکسن کا سباستین, Montenegro مونٹینیگرو, Belgrade بلغراد and Saint Sava
سینٹ ساوا all stand; Kornet کورنیت, Ivan ایوان and Chicago شکاگو are new.

Mariamne مریمنے, Philip فلپس, Bartholomew برتلمائی, Hierapolis ہیراپولس,
Phrygia فروگیہ, Lycaonia لکانیہ, India ہندوستان and Armenia آرمینیا all stand.

Makarios the Roman and Marcian of Cyrrhus both now open as جلیل القدر: رومی
is a byname and not an order, and the index types both of them monks.

## Batch 169: Mark of Ephesus, Martin the Confessor, Maruthas, Matrona of Moscow, Maximus of Kyiv

Mark is مرقس, from his own commemoration and twenty-six times in the lives;
Gregory Palamas گریگوری پالاماس, Photius فوتیس, Ephesus افسس, Florence فلورنس
and Gennadius گیناڈیس all stand. Eugenikos یوجینیکوس, Ferrara فیرارا, Lemnos
لیمنوس, Scholarios اسکولاریوس and Mangana مانگانا are new.

Maximus the Confessor is میکسمس, nine times across the vocabulary and the
lives against six میکسیمس in the commemorations, and the same form serves the
metropolitan of Kyiv, whom no commemoration names. Martin معترف مارٹن,
Cherson خرسون and the Lateran لاتیران all stand. Monothelite is یک مرضی, on
the pattern of the یک طبیعتی the lives already use of the other error; Constans
کونستانس, Naxos ناکسوس, Tuscany توسکانی and Cyrus of Alexandria
اسکندریہ کا کوروس are new, and Sophronius is سوفرونیس from his own
commemoration.

Maruthas ماروتھاس, Martyropolis مارتیروپولِس, Mayperqat مایپرقات and
Mesopotamia میسوپوٹیمیا all stand in the vocabulary's own account of the
relics he gathered; Yazdegerd یزدگرد and Seleucia-Ctesiphon سلوکیہ-تیسفون
are new.

Matrona ماترونا, Sebino سیبینو, Tula تولا and John of Kronstadt
کرونسٹاٹ کا یوحنا all stand; Nikonova نیکونووا and the Danilov cemetery
دانیلوف are new.

Vladimir ولادیمیر, the Golden Horde سنہری گروہ and the Dormition cathedral all
stand for the metropolitan of Kyiv; the Klyazma کلیازما and the Maximov icon
ماکسیموف are new.

## Batch 170: Meletius of Antioch, Meletius of Kharkov, Menas, Methodius of Moravia, Methodius of Constantinople

Meletius is میلیتیس for both, from the site's commemorations; Melitene ملیتینے,
Antioch انطاکیہ, Chrysostom زریں دہن, Gregory of Nyssa نیصا کا گریگوری,
Kharkov خارکوف, Kharkiv خارکیو, Akhtyrsk اختیرسک and Poltava پولتاوا all
stand. The city keeps both of its forms, خارکوف in the see's title as the
commemoration gives it and خارکیو where the entry speaks of the city today,
which is how the site already has them. Leontovich لیونتوویچ is new.

Menas مینس, Sampson سیمسن, Justinian جسٹینین, Anthimus انتھیمس, Agapetus
اگاپیتس and Severus سیویرس all stand.

Methodius میتھوڈیس, Moravia موراویا, Cyril سیرل, Olympus اولمپس, Bithynia
بتھینیا, the Khazars خزر, Swabia سواب, Clement کلیمنٹ, Naum ناحوم and
Thessalonica تھسلنیکے all stand, several of them in the vocabulary's own
description of the brothers. The Franks are فرینک, new here.

Syracuse سراکیوز, Sicily سسلی, Leo the Armenian لیو ارمنی, Theophilus
تھیوفیلوس, Theodora تھیودورا and the Triumph of Orthodoxy راست دینی کی فتح all
stand.

## Batch 171: Metrophanes, Michael of Synnada, Michael of Kyiv, Modestos, Moses of Novgorod

Metrophanes میتروفینس, Byzantium بازنطیم, Constantine قسطنطین, Nicaea نیقیہ,
Alexander الیگزینڈر and Titus ٹائٹس all stand; Dometius دومیتیس and Probus
پروبس are new.

Michael میکائیل, Synnada سناڈا, Phrygia فروگیہ, Tarasius تراسیس, the Great
Lavra عظیم لاورا and Iveron ایویرون all stand; Athanasius keeps اتھاناسیس,
which the lives carry twenty-six times against the vocabulary's two
اتھاناسیوس. Harun al-Rashid ہارون الرشید and Charlemagne شارلمین are new.

Kyiv کیف, the Dnipro دنیپرو, Vladimir ولادیمیر, Novgorod نووگوروڈ and Rostov
روستوف all stand.

Modestos موڈیستوس, Sebaste سیباستے, Cappadocia کپادوکیہ, John the Almsgiver
خیرات دینے والا یوحنا, Zachariah زکریا, Chosroes خسرو, the Holy Sepulchre
مقدس قبر, Golgotha گلگتا, Bethlehem بیت لحم and the Mount of Olives
زیتون کا پہاڑ all stand.

Moses موسیٰ, Yuriev یوریو, Skovorodka اسکوورودکا, the Volkhov وولخوف and the
panagia پاناگیا all stand, the last from the glossary; Mitrofan میتروفان is
new.

## Batch 172: Mstislav of Novgorod, Nektarios of Aegina, Nicholas of Myra, Nikephoros, Niketas of Chalcedon

Mstislav is مستسلاو with جارج in baptism, exactly as his commemoration gives
him; Novgorod نووگوروڈ, Kyiv کیف and Holy Wisdom مقدس حکمت stand.

Nektarios نکتاریوس and Aegina ایجینا stand; Selymbria سیلمبریا, Thrace تھریس,
Chios خیوس, Athens ایتھنز and Egypt مصر all stand too. Anastasios Kephalas
اناستاسیوس کیفالاس, Pentapolis پینتاپولس and the Rizarios seminary ریزاریوس
are new.

Nicholas نکولس, Myra میرا, Lycia لیشیا, Patara پتارا, Bari باری, Diocletian
دیوکلیشین, Constantine قسطنطین, Nicaea نیقیہ and Arius آریوس all stand.

Nikephoros نکیفوروس, Theodore اسٹودیت تھیوڈور, Leo the Armenian لیو ارمنی and
the Bosphorus باسفورس all stand.

Niketas is نکیتاس, eight times in the lives; Chalcedon stays کلقیدون, the
site's ordinary form, though his own commemoration writes کلیسڈن.

## Batch 173: Nikita of Novgorod, Nino of Georgia, Niphon of Constantia, Niphon of Novgorod, Oleg of Briansk

Nikita نکیتاس, Nikon نکون, Pimen پیمن, Isaiah یسعیاہ, Isaac اسحاق, Agapitus
اگاپیتوس and Philip فلپس all stand. Gleb Sviatoslavich گلیب سویاتوسلاویچ and
Zavolochye زاوولوچیے are new.

Nino نینو (نینا), Georgia جارجیا, Mtskheta متسختا, Svetitskhoveli
سویتیتسخوویلی, Bodbe بودبے, Kakheti کاخیتی, Cappadocia کپادوکیہ and George
جارج all stand; Iberia is ایبیریا, already twice in the lives, and Mirian
میریان, Nana نانا and Sidonia سیدونیا are new.

Niphon is نیفون for both, from their commemorations. Constantia in Cyprus is
قسطنطیہ here, the form his own commemoration gives, though the vocabulary
writes کونستانتیا of the same town in the life of Epiphanius; each entry keeps
the form its own commemoration uses. Paphlagonia پفلاگونیا, Alexander
الیگزینڈر, Athanasius اتھاناسیس and Alexandria اسکندریہ all stand.

Klim Smolyatich کلِم اسمولیاتیچ and Izyaslav ایزیاسلاو are new; Theodosius
تھیوڈوسیس stands.

Oleg اولیگ, Briansk بریانسک and Michael of Chernihiv چرنیہیو کا میکائیل all
come off the commemorations.

## Batch 174: Onuphrius of Gareji, Pakhomios of Keno Lake, Papias, Parthenios, Patrick

Onuphrius is اونوفریس, the form all his commemorations use, and his opening
carries جلیل القدر, the index typing him a monk. The monastery is
سینٹ داویت کا مٹھ at گاریجی, keeping the Georgian داویت the vocabulary
already writes of Davit-Gareji rather than the anglicised David of the
commemoration; Kartli کارتلی stands and Otar Machutadze اوتار ماچوتادزے is new.

Pakhomios پاخومیوس, Keno Lake کینو جھیل, Alexander of Oshevensk
اوشیوینسک کا الیگزینڈر, Anthony of Siya سیا کا انتھونی and the northern
Thebaid تھیبائیڈ all stand; Onega اونیگا is new.

Papias پاپیاس, Irenaeus ایرینیس, Hierapolis ہیراپولس, Polycarp پولی کارپ,
Smyrna سمرنا, Philip فلپس, Mark مرقس and Peter پطرس all stand.

Lampsakos is لیمپساکوس here, the form Parthenios' own commemoration gives,
against the لیمپساکس of Euschemon's; each entry keeps its own. Parthenios
پارتھینیوس, Melitopolis ملیتوپولس, the Hellespont ہیلیسپونٹ and Christopher
کرسٹوفر complete it.

Patrick پیٹرک, Armagh آرما, Ireland آئرلینڈ, Downpatrick ڈاؤن پیٹرک, Slane
سلین, Britain برطانیہ and Gaul گال all stand. Calpurnius کلپورنیس, Victoricus
وکٹوریکس, Tara تارا and Coroticus کوروتیکس are new, and the shamrock is
carried as شیمروک with the three leaves named beside it.

## Batch 175: Paul the Confessor, Paul of Plousias, Paul the New, Paul the Physician, Peter of Argos

Paul is پولس throughout; Thessalonica تھسلنیکے, Alexander الیگزینڈر,
Constantius قسطنطیوس, Julius جولیس, Athanasius اتھاناسیس, Cucusus کوکوسوس,
Chrysostom زریں دہن and Theodosius تھیوڈوسیس all stand.

Plousias پلوسیاس, Bithynia بتھینیا and Theophylact of Nicomedia
نیکومیڈیا کا تھیوفیلیکٹس all come off the commemorations and the vocabulary.

Paul the New is نیا پولس, Tarasius تراسیس and Cyprus قبرص.

Corinth کرنتھس stands, with the vocabulary's own account of the newborn who
spoke.

Argos is ارگوس, the form of his own commemoration and of the vocabulary's icon
description, against the آرگوس of a bare place label. The Peloponnese is
پیلوپونیس here, the form the site uses of the peninsula itself; پیلوپونیسس
stands in the commemoration of Illyricus, and each keeps its own. The Saracens
سراسین and Elijah ایلیاہ stand.

## Batch 176: Peter of the Horde, Philip of Irap, Philogonius, Photius of Kyiv, Photius the Great

Rostov روستوف, Lake Nero نیرو جھیل, Cyril سیرل and the Golden Horde
سنہری گروہ all stand; Ordinsk اوردینسک is new.

Philip فلپس, Irap اِراپ, Cherepovets چیریپوویتس and Cornelius of Komel
کومیل کا کورنیلیوس all come off his commemoration and the vocabulary. His
opening keeps مٹھ کے سربراہ, which is what his own commemoration calls him and
exactly the order the index gives; the register check lists him only because
its monastic pattern does not include that word, and the entry is right as it
stands.

Philogonius فیلوگونیس, Antioch انطاکیہ, Licinius لیکینیس, Arius آریوس,
Nicaea نیقیہ and Chrysostom زریں دہن all stand.

Photius فوتیس for both, Monembasia مونیمواسیا, the Peloponnese پیلوپونیس,
Tarasius تراسیس, the Myriobiblion میریوبیبلیون, Cyril and Methodius
سیرل اور میتھوڈیس, Moravia موراویا, Bulgaria بلغاریہ, Mark of Ephesus
افسس کا مرقس and Gregory Palamas گریگوری پالاماس all stand. Poland پولینڈ and
Lithuania لتھوانیا stand; the Strigolniki اسٹریگولنکی, Pope Nicholas
پوپ نکولس and the Filioque فِلیوکوے are written here, the last carried as the
name of the addition with what it says given beside it.

## Batch 177: Piamoun, Pitirim of Perm, Pitirim of Tambov, Platonis, Porphyrius of Gaza

Piamoun پیامون and Palladius پلادیس come off the commemorations, with the
Lausiac History لاؤسیاک تاریخ as the vocabulary names it; the Nile نیل stands.

Pitirim پتیریم, Perm پرم, Gerasimus گیراسیمس, Chudov چودوف, Alexis الیکسی,
the Zyrians زیری, the Voguls ووگل and Ust-Vym اُست-وِم all stand; Asyka آسیکا
is new.

Tambov is تامبوف, twice on the vocabulary against the one تمبوف of a
commemoration; Vyazma ویازما, Joachim یوآخم and Procopius پروکوپیس stand.

Platonis پلاتونس, Nisibis نصیبین, Mesopotamia میسوپوٹیمیا, James یعقوب and
Ephrem افریم all stand, and deaconess is خاتون شماس, the vocabulary's own
phrase for her order.

Porphyrius is پورفیریس, from his own commemoration and three times in the
lives, and the site keeps پورفیریوس for other men of the name. Gaza غزہ,
Thessalonica تھسلنیکے, Scetis اسقیطس, the Jordan یردن, Jerusalem یروشلم, the
Good Thief نیک ڈاکو, Caesarea قیصریہ, Marnas مارناس, the Marneion مارنیون,
Eudoxia یودوکسیا and Chrysostom زریں دہن all stand; the Eudoxiana یودوکسیانا
is new, and stavrophylax is given as صلیب کا نگہبان, which is how the
vocabulary already describes the office.

## Batch 178: Prochorus of the Pshinja, Proclus, Publius, Quiricus and Julitta, Sampson

Prochorus is پروخورس and the Pshinja پشینیا, from the vocabulary's icon
description; the place label writes پشینا, and the fuller line is preferred.
The Vranski desert ورانسکی صحرا and John of Rila ریلا کا یوحنا stand; Romanos
Diogenes رومانوس دیوجینیس is new.

Proclus پروکلس, Chrysostom زریں دہن, Cyzicus کیزیکس, Nestorius نسطوریس and
Theotokos والدہ خدا all stand. The Trisagion is قدوس خدا کا گیت, the phrase
the vocabulary uses of it, and the hymn itself is given in the words the site's
published prayers use.

Publius پبلیس, Zeugma زیوگما, Theodoret of Cyrrhus کوروس کا تھیودوریت and the
Euphrates فرات all stand. His opening keeps زاہد, which is what his own
commemoration calls him; the register check lists it only because that word is
not in its monastic pattern.

Quiricus کوئریکس and Julitta جولیتا come off their commemoration; Iconium
اکونیوم, Diocletian دیوکلیشین, Seleucia سلوکیہ and Alexander الیگزینڈر stand.
Tarsus is ترسس, eighteen times in the lives against no ترسوس there at all.

Sampson سیمسن and Justinian جسٹینین stand.

## Batch 179: Sava II, Sava I, Sebastiana, Serapion of Novgorod, Sergius of Malopinega

Serapion of Novgorod is written سراپیون, not the سیراپیون of his own
commemoration. The site carries سراپیون three times in the vocabulary and in
five commemorations against سیراپیون once and once, and eight times already
in the lives; the count is not near, so the site's weight decides and the one
commemoration does not.

Standing forms confirmed and reused: ساوا for Sava and ساوا دوم for the
second of the name, both from their own commemorations; ہلندار, واتوپیدی,
پانتیلیمون, کوہ آتھوس, سیمیون for the monk Symeon, سٹیفن نیمانیا, پہلا تاج
پوش سٹیفن, میلیشیوا, وراچار, پیچ, ژچہ, ترنووو, بلغراد, نیقیہ, ارسینیس;
نووگوروڈ, ماسکو, تثلیث-سرجیئس, وولوتسک کا یوسف, مالوپینیگا, تجلّی, جارج;
سیباستیانا, مارکیانوپولس, ہیراکلیہ, تھریس, پولس, دومیتیان. لاورا for lavra
(98 in the vocabulary against لارا once), اسکیما for the schema, خود مختاری
for autocephaly, وفات for the Dormition, عظیم شہزادہ for the Great Prince,
خاموشی کا عابد for the hesychast.

Written here for the first time: پریدیسلاو نیمانیچ for Predislav Nemanjić,
راستکو for Rastko, ہُم for the Adriatic principality, سنان پاشا, سترومین for
Stromyn, مارکیان نیکلیود. Sava's law book is named as the site names a work
it does not publish: اپنے نوموکینن، زاکونوپراویلو میں, the Slavonic title
given and the kind of book said in Urdu beside it.

The Chud have no form on the site: چودوف is the Moscow monastery and
چودھویں is the ordinal, and neither is the people. They are written چود
لوگ, on the pattern of پرمیوں for the Permians in the vocabulary.

Ranks. None of the five is typed monastic, so none needs جلیل القدر. The two
Savas and Serapion open with سردار اسقف, their own order; Sebastiana with
مقدس شہید; Sergius of Malopinega with مقدس کاہن, since the entry has him a
parish priest for thirty-two years and in the schema only in his last year.

## Batch 180: Shalva of Akhaltsikhe, Simeon Stylites, Simeon of Egypt, Simon of Vladimir, Sophronius of Cyprus

Chalcedon is کلقیدون. The vocabulary carries it twenty-eight times and one
commemoration once, against کلیسیڈن in a single commemoration; the lives
already have کلقیدون twenty-eight times. Nitria is نتریا, three in the
vocabulary against نطریہ once.

Standing forms reused: شالوا and اخالتسیخے from his commemoration, and his
own vocabulary line supplies سالار for the commander, فاتح for the
conqueror and پاؤں تلے روندنا for trampling the icon; شمعون for both
Simeons and for Simon of Vladimir, all three so named in their
commemorations; ستون نشین for the stylite; کلیکیا, کپادوکیہ, انطاکیہ,
فارس, عظیم روزے, اسقیطس, تھیبائیڈ, انتھونی اعظم, تھیوناس, پبلیس, پاتیریک,
پولیکارپ, سوزدال, ولادیمیر, قریبی غار, والدہ خدا کا میلاد, خودنمائی for
vainglory, تاج for the mitre, سوفرونیس, قبرص, خیرات for almsgiving,
عظیم شہید.

Monophysites are یک طبیعتی, which the lives already use eight times as an
adjective (یک طبیعتی بدعت, یک طبیعتی جماعتوں); the party itself is written
یک طبیعتیوں کے مقابل.

The Beatitudes have no form here and are not given one. The published Urdu
Gospel opens each with مُبارک ہیں وہ, and the life says what the entry says:
خداوند کی اُن مبارک باتوں سے جو پہاڑ پر کہی گئیں. Nothing is set in
quotation marks, since the entry quotes nothing.

Written here for the first time: فوربینس for Phorbinus, کلیازما for the
Klyazma, جارج وسیوولودووچ for the great prince, keeping the جارج by which
the site already names him. The synaxaria have no form either and are
called یادداشت کی کتابیں beside تقویمیں for the calendars.

Ranks. Shalva is Greatmartyr-typed and opens عظیم شہید; the two Simeons are
monastic-typed and open جلیل القدر; Simon of Vladimir opens بشپ, the word
his own commemoration uses; Sophronius opens سردار اسقف.

## Batch 181: Sophronius of Irkutsk, Sophronius of Jerusalem, Spyridon, Stephen the New Light, Stephen of Constantinople

Three contested spellings settled by weight. Irkutsk is ارکوتسک: twelve in
the vocabulary and four in the lives against ارکتسک in two commemorations.
Spyridon is سپیریڈون: two in the vocabulary, his own commemoration, and the
one occurrence already in the lives, against سپیریدون once. Maximus the
Confessor is میکسمس: twenty-two in the lives and six in the vocabulary and
three commemorations, against میکسیمس in six commemorations including his
own; the count is not near, so his commemoration does not decide it.

Monothelites keep the یک مرضی written for them earlier, not the ایک ارادے
والوں of the Lateran council line in the vocabulary. Both are the site's,
but Maximus's own vocabulary line says مسیح کی دو مرضیوں, so مرضی is the
site's word for the will in this argument, and یک مرضی sits beside the یک
طبیعتی the lives already use. ارادہ and عمل are still used for the will and
the energy where the sentence needs them apart.

Standing forms reused: بیریزان، پولتاوا کا علاقہ، یوکرین exactly as the
vocabulary has it; سائبیریا, الیگزینڈر نیفسکی لاورا; یوحنا موسخوس and
روحانی چراگاہ for the Spiritual Meadow; خیرات دینے والا یوحنا; دمشق,
فلسطین, سینا, یروشلم, اسکندریہ, خلیفہ, اسلام; قیامت کا کلیسا for the
Anastasis, which the site names قیامت کے کلیسا (مقدس قبر); مصر کی مریم;
سائرس اور یوحنا; چھٹی عالمی کونسل and پہلی عالمی کونسل; تریمیتھس, کورفو,
نیقیہ; نیولامپیس and ایا صوفیہ, both from Stephen's own vocabulary line,
which also gives نیا جلا ہوا چراغ for the image; والدہ خدا کا حمل; دانا
شہنشاہ لیو for Leo the Wise.

Written here for the first time: سٹیفن کریستالیفسکی, تائیگا, بوریات and
یاکوت for the Siberian peoples, and بازل اول مقدونی for Basil the First,
keeping the بازل by which the site already names the Great. Sophronius's
Synodical Letter is called مجلسی خط, the kind of document said in Urdu,
the site publishing no title for it.

Ranks: بشپ for Irkutsk, سرپرست اعلیٰ for Jerusalem, بشپ for Spyridon whose
commemoration says so, کاہن for the New Light who was of the clergy of the
Great Church, سردار اسقف for the emperor's brother.

## Batch 182: Stephen of Perm, Sylvester of Rome, Tabitha, Tarasius, Theodora the Empress

Tabitha is written تبیتا, not the طبیتا of her commemoration, because her
name is in Holy Scripture and the site publishes the passage: Acts 9 gives
تبیتا, ڈورکاس, ہرنی for the gazelle, and یافا for Joppa. A name the Bible
carries is read off the published text, and one commemoration does not
overturn it.

Her life quotes that passage twice and both times in the received wording:
جو ہمیشہ نیکی کرنے اور غریبوں کی مدد کرنے میں لگی رہتی تھی from Acts 9:36,
and اے تبیتا، اٹھ from Acts 9:40. Nothing is set in quotation marks; the
lives use none anywhere. Lydda keeps the vocabulary's لِدہ, which is the
Bible's word with its kasra.

Three more settled by weight: Justinian is جسٹینین (twelve in the lives,
three elsewhere, against یوستینیان once or twice); Sergius is سرجیئس
(twenty-one in the lives and sixty-seven elsewhere against seven); the
iconoclasts are آئیکن شکن (thirty-eight in the lives, thirteen in the
vocabulary) rather than شبیہ شکن, which the day entries use.

Standing forms reused: پرم, زیریان, ویلیکی اُستیوگ, روستوف, ایپیفانیوس
دانا, حروفِ تہجی and برچ from Stephen's own vocabulary line, کریملن;
سلویسٹر, پوپ, سرنگ قبرستان for the catacombs, قسطنطین اعظم, ہیلینا, پہلی
عالمی کونسل; تراسیس, سلطنت کا پہلا سیکرٹری exactly as the vocabulary has
it, ساتویں عالمی کونسل, فوتیس, اماستریس کا جارج; تھیودورا, ارغوانی,
ایا صوفیہ, مقدس رسولوں کا کلیسا, مفلوج کا اتوار.

Written here for the first time: کومی, ابور for the Zyrian alphabet, تامگا
for the carved signs, ویچیگدا, پام for the sorcerer; زمبری; ملکہ آئرین,
the site naming martyrs آئرین but no empress; نیکا کی بغاوت for the Nika
rising.

Ranks: بشپ for Perm, پوپ for Sylvester, بیوہ for Tabitha, whose
commemoration gives her that and no other, سردار اسقف for Tarasius, ملکہ
for Theodora.

## Batch 183: Theodore the Sykeote, Theodore of Constantinople, Theodore of Edessa, Theodore of Smolensk, Theodore of Rostov

Edessa is ایڈیسا: sixteen in the lives, three in the vocabulary and four
commemorations, including this Theodore's own, against اڈیسا nine times in
the vocabulary. The Syriac Orhay has no form here and is not introduced.

Standing forms reused: سیکیوت and اناستاسیوپولس from his commemoration,
گلتیہ, سیکیون, عظیم شہید جارج, اوموفوریون, بدروح زدہ and لوہے کا پنجرا
from his own vocabulary line, ٹڈیاں; ایا صوفیہ, سنکیلوس from Michael the
Synkellos in the vocabulary, چھٹی عالمی کونسل; مقدس سینٹ ساباس for Sabbas
the Sanctified, whose Lavra keeps that name; سمولینسک, یاروسلاول,
موژائسک, تھیوڈور سٹراٹیلیٹس, تاتاری, گروہ for the Horde and سنہری گروہ
where it is named whole, خان; روستوف, سوزدال, ولادیمیر, روشن کنندہ.

Written here for the first time: قسطنطین پوگوناتس, and فنی for the Finnic
tribes of the Rostov land. Theodore of Smolensk keeps his byname in plain
Urdu, جنہیں کالا کہا جاتا تھا.

Ranks: بشپ for the Sykeote, Edessa and Rostov, all three so named in their
commemorations; سردار اسقف for Constantinople; شہزادہ for Smolensk, the
word his own commemoration uses.

## Batch 184: Theodosius of Ostrog, Theodosius of Antioch, Theodota, Theodoulus the Eparch, Theognostus of Kyiv

The unmercenary physicians are بے غرض معالج. The vocabulary has it
twenty-three times and three commemorations more, and the lives nine,
against بلامعاوضہ طبیب in four commemorations and بے اجرت طبیب in three
places. All three are the site's; the count is not near.

Standing forms reused: اوستروگ, وولہینیا, پودولیا, دور کے غار, لاطینی for
the Latins (twelve in the lives), لتھوانیا, پولینڈ والے, تاتاری; روسوس،
کلیکیا exactly as the vocabulary has it; تھیوڈوتا, کوسماس اور دامیان;
گورنر for the eparch, which is the word his own commemoration uses,
تھیوڈوسیس اعظم for the emperor, ستون نشین, ایڈیسا, کورنیلیوس;
تھیوگنوستس, میٹروپولیٹن, ماسکو کا سینٹ پطرس, الکسی, کریملن, وفات کا بڑا
کلیسا, گروہ and خان.

Written here for the first time: گرنوالڈ, ٹیوٹونی سورما for the Teutonic
Knights, لتھوانیائی, and کالی موت for the Black Death.

Ranks. Theodosius of Ostrog and Theodoulus are both monastic-typed and both
open جلیل القدر, Theodoulus keeping the گورنر of his commemoration beside
it; Theodosius of Antioch is Venerable and opens جلیل القدر; Theognostus
opens میٹروپولیٹن. Theodota has no order of her own: the site knows her
only as the mother of the Unmercenaries, so her life opens with them and
names her مقدسہ تھیوڈوتا in its own place, which is what her commemoration
does.

## Batch 185: Theonas of Egypt, Theophanes the Branded, Theophano, Theophilus of Novgorod, Theophilus of Antioch

A hymnographic canon is قانون, the word the site already uses for it:
Theophanes's own vocabulary line has قانونوں کا طومار beside the verses
branded on his face, and Andrew of Crete's Great Canon is عظیم قانون.
The word does double duty for a canon of law, as it does in English.

The hymnographer is گیت نگار, eleven in the vocabulary and four in the
lives, against نغمہ نگار in five commemorations; Eusebius is یوسیبیوس,
fifteen in the lives and five elsewhere against nine and four.

Standing forms reused: تھیوناس, شمعون, پبلیس, فوربینس and یادداشت کی
کتابیں carried over from batch 180; داغ دار for the Graptoi and تھیوڈور
گراپتس for the brother, both from the vocabulary, تھیوفینس, یونس for
their father, مقدس سینٹ ساباس, نیقیہ, لیو ارمنی, میتھوڈیس, راست دینی کی
فتح and راست دینی کا اتوار, آئیکن شکنی; تھیوفانو from her commemoration,
بازل مقدونی and لیو دانا from batch 181 and the vocabulary, ارغوانی, فنار,
تمام سینٹس کا اتوار as the site names it; چودوف, دنیپرو, ایوان, لتھوانیا,
دور کے غار; ہرموجینیس, مکاشفہ, مدافع for the apologist.

Written here for the first time: قسطنطین مارتیناکیوس, اوٹولیکس and
مارکیون, and ہیرو and ایروس among the first bishops of Antioch.

Ranks: جلیل القدر for Theonas, who is monastic-typed; بشپ for Theophanes
of Nicaea and Theophilus of Antioch; ملکہ for Theophano; سردار اسقف for
Theophilus of Novgorod.

## Batch 186: Theophylact of Nicomedia, Thomas of Constantinople, Tikhon of Amathus, Tikhon of Zadonsk, Triphyllius of Nicosia

Amathus is اماتھس, and the two occurrences the lives already carried, in
the life of John the Merciful, have been changed to match. The vocabulary
holds both forms twice each and so decides nothing; the count was near, and
in a near tie the saint's own commemoration decides, and his says اماتھس.

Voronezh is وورونیژ, five in the vocabulary and four in the lives against
the ورونیج of Tikhon's own commemoration; that count is not near.

Standing forms reused: تھیوفیلیکٹس, نیکومیڈیا, تراسیس, ساتویں عالمی کونسل,
باسفورس, کوڑھی and the washing of their wounds from his own vocabulary
line, لیو ارمنی, نکیفوروس, ستروبل، ایشیائے کوچک exactly as the vocabulary
has it, ملکہ تھیودورا; روزہ دار یوحنا, فوکاس, سیکیون کا تھیوڈور, and
جلوس کی ہلتی ہوئی صلیبیں from Thomas's own vocabulary line; تیخون, اماتھس,
قاری, ایپیفانیوس; زادونسک, گیت گانے والا for the cantor; ٹریفیلیس,
لیوکوسیا (نکوسیا) with the site's own parenthesis, بیروت, سپیریڈون,
تریمیتھس.

Written here for the first time: ساکیلاریوس and منیمونیوس. Tikhon of
Zadonsk's books are named in Urdu, the site publishing neither: سچی
مسیحیت کے بارے میں and وہ روحانی خزانہ جو دنیا میں سے جمع کیا گیا.

All five are bishops and all five open بشپ, which is what each
commemoration says.

## Batch 187: Varnava (Nastic), Vincent of Lerins, Vsevolod-Gabriel of Pskov, Xenophon of Robeika, Eutychius and Florentius of Nursia

Vsevolod is وسیوولود: four in the vocabulary, two commemorations and four
in the lives, against the ویسیوولود of one commemoration and one day entry.
The wonderworker is معجزہ گر throughout, ninety-eight in the vocabulary and
sixty-four commemorations against عجائب گر in five places, so Vsevolod's
own commemoration does not carry its عجائب گر into his life either.

Standing forms reused: ورناوا and خوسنو from his commemoration, بیوچن مٹھ,
میلیشیوا, بلغراد, سینٹ ساوا; لیرنس کے ونسنٹ, لیرین کے جزیرے and
کومونیتوریوم and عالمگیری کا قاعدہ all from his own vocabulary line, گال;
مستسلاو, ولادیمیر مونوماخ, پسکوف, نووگوروڈ, مقدس تثلیث; زینوفون, روبیکا,
خوتین کا ورلام, اسیدور, مٹھ کا سربراہ; یوتیخیس, فلورینٹیس, نرسیا,
مکالمات for Gregory's Dialogues, کوڑھ.

Written here for the first time: ویوئسلاو ناستچ, گیری، انڈیانا, سرائیوو,
دابر-بوسنا, زینیتسا, سریمسکا میتروویتسا, and ویچے for the Novgorod
assembly, which the site has no word for.

Ranks. Varnava opens بشپ, and نئے معترف beside it, both from his own title;
Vincent, Xenophon, Eutychius and Florentius are all monastic-typed and all
open جلیل القدر, Xenophon keeping مٹھ کے سربراہ beside it since that is his
order; Vsevolod opens مبارک شہزادہ, the words his commemorations use.

## Batch 188: Martinian, Zoe and Photina; Peter and Fevronia of Murom; Xanthippe and Polyxene; Zenon and Zoilus; the Second Day of the Nativity

Zoe is زوئے. The vocabulary and her own commemoration have it once each
against زوئی once in the vocabulary and once in the lives; the count is
near, so her commemoration decides. Spain is ہسپانیہ, eight in the
vocabulary against اسپین in three commemorations.

The Second Day quotes Matthew 2 twice and both times in the received
wording the site publishes: اٹھو، بچے اور اس کی ماں کو ساتھ لے کر مصر
بھاگ جاؤ، کیونکہ ہیرودیس اس بچے کو ڈھونڈ کر ہلاک کرنا چاہتا ہے from
verse 13, and میں اپنے بیٹے کو مصر سے بلایا from verse 15. Martinian's
two sayings are not Scripture and are written as prose.

Standing forms reused: مارٹینین, زوئے, فوتینا, فلسطین کا قیصریہ, بیت لحم,
ڈولفن and the whole image from the day's own vocabulary line, ایتھنز;
مُروم with its damma as the vocabulary writes it, پطرس اور فیورونیا, ڈیوڈ
اور یوفروسینے, ریازان, بویار, شہد کی مکھیاں پالنے والا; زانتھپی and
پولکسینی and پروبس from their commemorations, رسول اندریاس; زینون اور
زوئلس, راستباز, منگیتر یوسف, خدا کو قبول کرنے والا شمعون, یادداشت کی
کتابیں; نہایت مقدس والدہ خدا کا اجتماع, عید کے بعد کے دن, اختتام for the
leavetaking, مجسم ہونا for the Incarnation, and مصر کے بت گرتے ہوئے from
the day's own vocabulary line.

Written here for the first time: سینٹ پاؤلا, whose Bethlehem convent the
site does not otherwise name.

Ranks: جلیل القدر for Martinian, who is hermit-typed, with مقدسہ for the
two women beside him; شہزادہ and شہزادی for Peter and Fevronia; راستباز
for Zenon and Zoilus, which is their type and their commemoration. The
Spanish sisters have no order at all, so their life opens with their
country and calls them مقدسہ بہنیں, which is all the site knows of them.

## Batch 189: the translation of Herman of Kazan, the Seven Martyred Brothers, Anthony of the Kyiv Caves, Basil of Ostrog, Calinic of Cernica

Kazan is کازان, forty-two in the vocabulary, five commemorations and
thirty-three in the lives, against قازان in six commemorations and two day
entries. Cernica is چیرنیکا, six in the vocabulary against the چرنیکا of
Calinic's one commemoration.

Standing forms reused: جرمانس, سویاژسک, گوریاس, وفات کا مٹھ; اورینٹیس،
فارناکیس، ایروس، فرمس، فرمینس، سیریاکس اور لونگینس exactly as their
commemoration lists them, بحیرہ اسود, قفقاز; انتھونی, لیوبیچ، چرنیگوف کے
قریب as the vocabulary has it, انتیپاس, کوہ آتھوس, دنیپر, تھیوڈوسیس,
نکون; اوستروگ, بازل, زاہوملیے, ہرزیگووینا, مرکونیچی، پوپووو exactly as
the vocabulary has it, تورڈوش, زیتا, پیچ, آرکمنڈرائٹ, والدہ خدا کے ہیکل
میں داخلہ; چیرنیکا, بخارسٹ, رمنیک, فراسینے, یسوع کی دعا, پائسیوس,
بصیرت والا for the clairvoyant.

Written here for the first time: سٹویان یووانووچ, زاوالا, ترے بینیے for
Trebinje, سکندریا for Skenderija, والاخیا for Wallachia, and خون کا محصول
for the devshirme, which the site has no word for and which is named here
by what it was.

Ranks: the Herman entry is a feast and opens with the day, naming him
سردار اسقف in its own place; شہید for the seven brothers; جلیل القدر for
Anthony, who is hermit-typed; میٹروپولیٹن for Basil; بشپ for Calinic.

## Batch 190: Dimitrie the New, Dionysios of Zakynthos, Joseph of Damascus, Kosmas Aitolos, Olga

Three settled by weight. Dionysius is ڈیونیسیس: twenty-five in the
vocabulary, five commemorations and thirty-five in the lives, against
ڈایونیسیس in three commemorations, including this saint's own, and
دیونیسیس in four more. Equal-to-the-Apostles is رسولوں کے برابر, eighteen
in the vocabulary, eleven commemorations, two day entries and twenty in
the lives, against رسولوں کے ہمسر in six commemorations, Kosmas's and
Olga's among them. Nestor the Chronicler is نسٹور, five and three against
one.

Standing forms reused: نیا دیمتری and باسربوو, ڈینیوب, میٹروپولیٹن کا بڑا
کلیسا, بخارسٹ; زاکنتھوس, ایجینا, فرشتوں کا اسکیما, عالمی پیٹریارکیٹ;
دمشق, انطاکیہ, مقدس عطیے for the Holy Gifts, دمشق کے نئے شہداء exactly as
the vocabulary has it; ایتولیا, کوسماس, کوہ مقدس, واتوپیدی, فیلوتھیو,
البانیہ; اولگا, اِگور, ہیلینا, ولادیمیر, دسویں حصے کا کلیسا, نائب حکمران
for the regent, تاریخ نویس نسٹور.

Written here for the first time: لوم for the river, سیگورس, ستروفادیس,
انافونیتریا, کونستاس, ایونی جزیرے, سویاتوسلاو, and منادی کی صلیبیں for
the preaching crosses Kosmas raised.

Ranks: جلیل القدر for Dimitrie, who is monastic-typed; سردار اسقف for
Dionysios; کاہن شہید for Joseph of Damascus, whose entry calls him
hieromartyr; راہب کاہن for Kosmas; عظیم شہزادی for Olga.

## Batch 191: Parascheva of Iasi, Sava of Serbia again, Seraphim of Sarov, Sergius of Radonezh, Simeon the Myrrh-gusher

The site carries Saint Sava of Serbia twice, under two entries with the
same English word for word. The second is rendered with the first's Urdu
verbatim, since one saint told the same way in the same language should
read the same both times.

Parascheva's life quotes the Lord's call to deny oneself. The published
Urdu carries it twice, and the Markan wording is the one that matches the
entry's whosoever, so the life reads جو کوئی میری پیروی کرنا چاہے تو وہ
خودی کا انکار کرے, from Mark 8:34, and not the Matthean form.

Seraphim's greeting is not invented either: the site's own day entry for
his repose already has him meeting everyone with مسیح جی اٹھا، میری خوشی,
and the life uses those words exactly.

Standing forms reused: پاراسکیوا, ایپیواتو، تھریس as the vocabulary has
it, یاشی, مالدووا, ترنووو, بلغراد; سیرافیم, ساروف, کورسک, پروخور, and
رُوح القدس کا حاصل کرنا, which the vocabulary already gives for the
acquisition of the Holy Spirit; سرجیئس, رادونیج, روستوف, تثلیث کا لاورا;
مُر بہانے والا شمعون, ژوپان, ستودینیتسا, ہلندار, پہلا تاج پوش سٹیفن,
راستکو, اناستاسیا.

Written here for the first time: بحیرہ مرمرہ, پونتس کا ہیراکلیہ, بازل
لوپو, موشنن, برتھولومیو for Sergius's baptismal name, and کولیکوو for
the battle, with دیمیتریس for the Grand Prince who fought it.

Ranks: جلیل القدر for Parascheva, Seraphim, Sergius and Simeon, all four
monastic, Sergius keeping مٹھ کے سربراہ beside it; Sava keeps the سردار
اسقف of his first telling.

## Batch 192: Stephen the Great, Theodosius of the Kyiv Caves, Vladimir and Volodymyr, Xenia of Petersburg

The site carries Saint Vladimir twice, under Vladimir and under Volodymyr,
with the same English word for word, as it carries Sava twice. The second
takes the first's Urdu verbatim, on the rule settled in batch 191.

Stephen the Great of Moldavia is اسٹیفن, the form his own commemoration
uses. Whole-word, the site holds اسٹیفن and سٹیفن at about sixty and fifty,
which is near, so the commemoration decides; the Serbian Stefans keep the
سٹیفن their own commemorations give them, and the two names stay apart.

Standing forms reused: مولداویا, پوتنا, ہیسوخاست دانیال; واسیلیو، کیف کے
قریب as the vocabulary has it, کورسک, پروسفورا, اسٹودیت, انتھونی, نکون,
وفات کا بڑا کلیسا, بویار, دور کے غار; ولادیمیر, سویاتوسلاو, اولگا, بازل,
آنا, دنیپر, قسطنطین; زینیا and سینٹ پیٹرز برگ from her commemoration,
مسیح کے لیے احمق, سمولینسک آئیکن.

Written here for the first time: بوگدان دوم, رازبوئینی; قائن as the
comparison Theodosius wrote of the prince; بیلاروسی; آندرے فیودوروچ
پیتروف, ملکہ الزبتھ, کوپیک, پیروژکی, بلینی for the funeral pancakes, and
اوختا for the cemetery.

Ranks: شہزادہ for Stephen the Great; جلیل القدر for Theodosius, who is
monastic; عظیم شہزادہ for Vladimir; مبارک with مسیح کے لیے احمق for
Xenia, both from her own type and commemoration.

A thousand of the fourteen hundred and fifty-six lives are now written.

## Batch 193: the Synaxes of Gabriel, of Michael, of the Three Hierarchs, of the Kazan hierarchs, of the Moscow hierarchs

Three of the Church's most-named fathers are settled here, and where the
bodies disagreed the prayers decided, as they always do.

John Chrysostom is سنہری دہن. The prayers carry it three times against
زریں دہن once, and the vocabulary thirty-four times against four; the
lives held both, nineteen and thirteen, and the nineteen have been changed
to match, so the whole file now says one thing. His five commemorations
all read زریں دہن, but the count against it is not near. Both sentences
that gloss the epithet still read correctly, since it is دہن that the
gloss سنہری منہ explains.

Basil the Great is باسل اعظم: two in the prayers, four in the vocabulary
and twenty in the lives, against بازل اعظم fifteen in the vocabulary and
none in the lives, and عظیم باسل in two commemorations. Gregory is
گریگوری عالمِ الٰہیات, nine in the vocabulary and five in the lives
against عالم دین گریگوری in two commemorations.

Barsanuphius of Tver keeps بارسانوفیس, his own commemoration's form and
the lives' five; برسانوفیوس in the vocabulary is the other Barsanuphius,
of Gaza, and the site keeps the two men apart.

The angelic ranks are read off the published Scripture. Colossians 1:16
gives شاہی تخت، قوتیں، حکمران، صاحب اختیار and Ephesians 1:21 gives
حکمرانی، اختیار، قدرت، ریاست, and the nine are written from those words:
سرافیم، کروبیم اور تخت؛ ریاستیں، قوتیں اور اختیارات؛ حکومتیں، سردار
فرشتے اور فرشتے. سرافیم and کروبیم are the prayers' own, nine and eight
times.

Two verses are quoted in the received wording: جب ابن آدم اپنے جلال میں
آئے گا اور اس کے ساتھ سبھی فرشتے آئیں گے from Matthew 25:31, and ایک
گنہگار کے توبہ کرنے پر خوشی منائی جاتی ہے from Luke 15:10. The third,
Psalm 34:7 on the angel encamping about those who fear the Lord, carries
یاہوہ in the Urdu Old Testament, so it is reported in the site's own prose
and not quoted, as the rule for that name requires.

Michael's cry is written as prose. The site publishes no Urdu form of the
deacon's exclamation, and nothing is set out as though it were received.

Standing forms reused: سردار فرشتہ, جبرائیل, میکائیل, بے جسم قوتیں,
اجتماع for the synaxis, بشارت; تین سردار کاہن, یوحنا ماوروپوس and
یوخائٹا, both from the vocabulary; کازان, گوریاس, جرمانس, سویاژسک,
ہرموجینیس, تجلّی; پطرس, الکسی, یونس, فلپس, مصیبتوں کا زمانہ, گروہ.

Written here for the first time: یوریل، سیلافیل، یگودیل، باراکیل and
یریمیل among the archangels, سردار سالار for the Archistrategos,
الیکسیوس کومنینوس, ایوان مہیب, ایوب, فیلارت, انوسنٹ, تیخون, الطائی and
کروتیتسا.

## Batch 194: the Synaxes of the Novgorod hierarchs, of the Forerunner, of the Twelve, of the Theotokos, of the saints of North America

The Apostle Andrew is آندریو, not the اندریاس of the published Acts and
Matthew. This refines the rule set for Tabitha rather than contradicting
it. Scripture decides a name the site has not settled: Tabitha stood at
one commemoration against the published text, and the text won. Here the
site has settled its own form heavily, آندریو fifty-seven times against
nine, and the vocabulary uses it of this apostle by name; and the site
keeps اندریاس for Andrew of Crete, whose Great Canon it names that way, so
the two men are told apart. The one اندریاس written for the Apostle in an
earlier batch has been changed to match.

The rest of the Twelve are read straight off the published Matthew 10 and
Luke 6: پطرس، آندریو، یعقوب، یوحنا، فلپس، برتلمائی، توما، متی، حلفئی کا
بیٹا یعقوب، تدی، متیاہ, with نتن ایل from John 1:45 and رعد کے بیٹے from
the vocabulary. Simon keeps the شمعون غیور of his own commemoration rather
than the قنانی of Matthew or the زیلوتیس of Luke, both of which transcribe
rather than translate the epithet.

The Forerunner's synaxis quotes the received text throughout: مجھے تو آپ
سے پاک غسل لینے کی ضرورت ہے اور آپ میرے پاس آئے ہیں and ابھی تو ایسا ہی
ہونے دو from Matthew 3, جو عورتوں سے پیدا ہوئے ہیں ان میں یوحنا سے بڑا
کوئی نہیں ہوا from Matthew 11:11, دلہے کا دوست... اس کی آواز سن کر خوش
ہوتا ہے from John 3:29, and لازم ہے کہ وہ بڑھے اور میں گھٹتا رہوں from
John 3:30, with اونٹ کے بالوں سے بنا لباس and ٹڈیاں اور جنگلی شہد from
Mark 1:6. The Twelve quote تاکہ وہ ان کے ساتھ رہیں اور وہ انہیں منادی
کرنے کے لئے بھیجیں from Mark 3:14 and تمام قوموں کو شاگرد بناؤ from
Matthew 28:19. The edition's پاک غسل stands inside the quotations, as an
edition's wording must; the site's own prose keeps its بپتسمہ.

Standing forms reused: مقدس حکمت, کورسون کا یوآخیم, نکیتاس, ویچے carried
over from batch 187, پسکوف, گیناڈیس; پیش رو, تجلّیِ الٰہی, زکریا, یردن,
خدا کا برہ; مقدس، جلیل القدر اور سب کے سراہے بارہ رسولوں کا اجتماع exactly
as the commemoration has it, پنتیکست; والدہ خدا, ایپیفانیوس, مجوسی, عید کے
بعد کے دن, اختتام; والام, الاسکا کا ہرمن, جیکب نیتسویتوف, تیخون.

Written here for the first time: لوکا ژدیاتا, نیفونت, باسل کالیکا, کلوبک
for the white cowl, وولخوف, مارتیریس; میلاد کے تحفے for the Nativity
Gifts the oldest books call this day; انوسنٹ وینیامینوف.

## Batch 195: the Synaxes of the Rostov saints, the Volhynian saints, the Seventy, the Caves fathers, the Near Caves fathers

The Seventy raise a question the site has not met before. The published
Urdu Luke reads بہتر شاگرد at 10:1 and 10:17, seventy-two, where the feast
and the whole site say ستر. The edition is not corrected and the number is
not argued with: the life quotes the sayings, which carry no number, and
gives the number in the site's own prose. So دیکھو میں تمہیں گویا بروں کو
بھیڑیوں کے درمیان بھیج رہا ہوں (10:3), اپنے ساتھ بٹوا نہ لے جانا نہ تھیلی
نہ جوتے (10:4), خدا کی بادشاہی تمہارے نزدیک آ گئی ہے (10:9), آپ کے نام سے
تو بدروحیں بھی ہمارا حکم مانتی ہیں (10:17), and تمہارے نام آسمان پر لکھے
ہوئے ہیں (10:20) all stand in the received wording, and the two clauses
that name the number are reported instead.

Standing forms reused: روستوف, یاروسلاول, لیونٹیس, اشعیا, دیمیتریس,
ویلس from the vocabulary line about the felled idol, ایرینارکس, اوگلچ,
پیریسلاول, پوشیخونیے, الیگزینڈر نیفسکی; امفیلوکیس, یاروپولک, یولیانا
اولشانسکایا, کانیف کا مکاریس, پوچائیف کا ایوب, لاطینی; ستر رسول, برناباس,
تیمتھیس, ٹائٹس, سیلاس, اپلوس, پروخورس, گیت نگار یوسف, قانون for the
hymnographic canon; انتھونی, تھیوڈوسیس, اسٹودیت, پاتیریک, کُکشا, ویاتیچی,
اگاپیتس, الیپیس, قریبی غار and دور کے غار; نسٹور, دامیان, ایلیاہ, ہنگری
موسیٰ.

Written here for the first time: اسیدور تویردیسلوو, ابرامیس for Abraham of
Rostov, تساریوچ پطرس, نکیتاس ستون نشین, اوبنورا کا سلویسٹر, صور کا
دوروتھیس, نکولس سویاتوشا, مارک قبر کھودنے والا, بتھوا for the pigweed
Prochorus baked, and کارپیتھیائی پہاڑ.

## Batch 196: the Adoration of the Magi, the Annunciation, the Beheading, the Burning of Sava's relics, the Circumcision

Four of these five carry Scripture, and every clause of it is the received
wording the site publishes. The Magi: یہودیوں کا بادشاہ جو پیدا ہوا ہے،
وہ کہاں ہے (Matthew 2:2), بچے کو اس کی ماں حضرت مریم کے پاس جا کر ان کے
آگے جھک کر سجدہ کیا and اپنے ڈبے کھول کر with سونا، لوبان اور مُر (2:11),
کسی دوسرے راستے سے اپنے ملک واپس چلے گئے (2:12). The Annunciation: سلام،
آپ پر بڑا فضل ہوا ہے! خداوند آپ کے ساتھ ہے (Luke 1:28), پاک روح آپ پر
نازل ہوگا، اور خداتعالیٰ کی قدرت آپ پر سایہ ڈالے گی (1:35), میں تو خداوند
کی بندی ہوں (1:38), and کلام مجسم ہوا (John 1:14). The Circumcision takes
its eighth day and its name from Luke 2:21, and the Beheading its تھال from
Matthew 14:8.

Hades is پاتال, twelve in the prayers and two in the lives, and the
prayers decide it.

Standing forms reused: مجوسی and ملکیور، کیسپر اور بلتھاسر from the day's
own entry, سنہری دہن, تھیوفیلیکٹس, روستوف کا دیمیتریس, میکاہ, بیت لحم,
کولون; بشارت, ناصرت, سردار فرشتہ جبرائیل, عظیم روزے; پیش رو, سر قلم,
گلیل, بپتسمہ; ساوا, میلیشیوا, وراچار, بلغراد, سنان پاشا, سرنگ قبرستان;
ختنہ, ابراہیم, باسل اعظم, قیصریہ, نیا سال.

Written here for the first time: ہیرودیس انتیپاس, ہیرودیاس, چوتھائی حاکم
for the tetrarch, بانات, وزیرِ اعظم for the grand vizier, نئی حوا, and پاک
ہفتہ for Holy Week, on the pattern of the site's own پاک پیر.

## Batch 197: Zosimas of Vorbozomsk, the Dormition, the Entry into the Temple, Paul, Peter

Vorbozomsk is ووربوزومسک, six whole-word in the vocabulary against
وربوزومسک in two commemorations. The Mother of God stays والدہ خدا: the
Entry's own commemoration writes تھیوٹوکوس, which appears in six
commemorations and nowhere else, against والدہ خدا everywhere on the site.

Peter and Paul carry Scripture and every clause is the published wording:
اے ساؤل، اے ساؤل، تو مجھے کیوں ستاتا ہے (Acts 9:4), یہودی، یونانی... کی
تفریق باقی نہیں رہی (Galatians 3:28), ایمان، امید اور محبت... محبت ان میں
افضل ہے (1 Corinthians 13:13); آپ زندہ خدا کے بیٹے المسیح ہیں (Matthew
16:16), عالم ارواح کے دروازے اس پر غالب نہ آئیں گے (16:18), کیفا یعنی
پطرس (John 1:42), آدم گیر (Matthew 4:19), وہ باہر جا کر زار زار رویا
(Luke 22:62), and کیا تم مجھ سے محبت رکھتے ہو with تم میری بھیڑیں چراؤ
(John 21:17). The Entry's پاک ترین مقام is the Holy of Holies of Hebrews
9:3.

The Nativity katavasia has no published Urdu, so the line the Church first
sings on that day is given in the site's own prose, مسیح پیدا ہوا ہے، اُس
کی تمجید کرو, with nothing set out as though it were received.

Standing forms reused: زوسیماس, کومیل کا کورنیلیوس, بیلوزیرسک, بشارت,
اناستاسیا; وفات, گتسمنی, توما; یوآخیم اور آنا, زکریا, صندوق; ترسس,
بنیمین, فریسی, دمشق, سٹیفن, نیرو, ایشیائے کوچک; بیت صیدا, گلیل, آندریو as
settled in batch 194, تجلّی, پنتیکست, انطاکیہ.

## Batch 198: Peter and Paul together, the Hieromartyrs of Cherson, Demetrius of Uglich, the Transfiguration, the Meeting

The Transfiguration and the Meeting quote the received text throughout:
حضور کا چہرہ سورج کی مانند چمکنے لگا اور حضور کے کپڑے نور کی مانند سفید
ہو گئے and یہ میرا پیارا بیٹا ہے... اس کی بات غور سے سنو from Matthew 17;
اے خداوند! تو اپنے وعدہ کے مطابق، اب اپنے خادم کو سلامتی سے رخصت کر with
میری آنکھوں نے تیری نجات کو دیکھ لیا ہے from Luke 2:29 and 30, مکاشفہ کا
نور and اسرائیل کا جلال from 2:32, غم کی تلوار تیری جان کو بھی چھید ڈالے
گی from 2:35, and یروشلم کی مخلصی کے منتظر from 2:38.

Standing forms reused: خرسون with its seven names exactly as the
commemoration lists them, تاوریدا, کریمیا, ڈینیوب, دنیپر, ہیلیسپونٹ,
فیلونیون, آندریو, ولادیمیر; تساریوچ دیمیتریس, اوگلچ, ایوان مہیب, نائب
حکمران, مصیبتوں کا زمانہ, کریملن, سردار فرشتہ میکائیل, آلام بردار and
بورس اور گلیب, تجلّی; کوہ تبور, موسیٰ, ایلیاہ; ملاقات as the site names
the feast, خدا کو قبول کرنے والا شمعون, نبیہ آنا.

Written here for the first time: ہرمون for the bishop of Jerusalem who
sent the seven; ماریا ناگایا, فیودور, بورس گودونوف, واسیلی شوئیسکی, and
the four named murderers اوسِپ اور دانیل وولوخوف، میخائیل بیتیاگووسکی اور
نکیتا کاچالوف; شام کی عبادت for Vespers, at which Symeon's words are sung.

## Batch 199: the Nativity of the Lord, the Nativity of the Theotokos, the Cincture, the Robe at Moscow, the Robe at Blachernae

Blachernae is بلاخیرنے, four in the vocabulary and five in the lives
against بلاخرنے twice in the vocabulary and once in a commemoration.

The Nativity takes its whole scene from the published Luke 2: چرنی میں
رکھا گیا کیونکہ ان کے لیے سرائے میں کوئی جگہ نہ تھی (2:7), رات کے وقت
میدان میں اپنے ریوڑ کی نگہبانی کر رہے تھے (2:8), آسمانی لشکر (2:13), and
سب چیزیں کلام کے وسیلے پیدا کی گئیں from John 1:3.

The Cincture is کمربند with پٹکا beside it at first mention, exactly as
its own commemoration names it; the Robe is چوغہ, which the vocabulary uses
of the relic itself, and معزز beside it where the feast names it.

Standing forms reused: بیت لحم, چرنی, مجوسی, سونا، لوبان اور مُر, فسح,
مجسم ہونا; یوآخیم اور آنا, داؤد, وفات, آفتابِ صداقت; کوہ مقدس, لیو دانا,
کپادوکیہ, توما; کریملن, وفات کا بڑا کلیسا, صلیب کی تعظیم; فوتیس, فلسطین.

Written here for the first time: خلکوپراتیا, زیلا, ملکہ زوئے, میخائیل
فیودوروچ, فیلارت, لیو اعظم, گالبیوس اور کاندیدوس, گیناڈیس, and آوار for
the Avars.

## Batch 200: the Protection, Gideon, the Three Holy Youths, the Exaltation of the Cross, the Third Day of the Nativity

Gideon is گدعون, the published Judges, not the جدعون of his one
commemoration. That is the Tabitha case exactly: a single occurrence on the
site against the text the site publishes, and the text wins.

His life quotes the clean verses and reports the two that carry the divine
name. Judges 6:12 and 8:23 both read یاہوہ in the Urdu Old Testament, so
the angel's greeting and Gideon's refusal of the crown are told in the
site's prose; 6:15, 6:37, 6:40 and 7:12 are quoted as published, and
Hebrews 11:33 gives ایمان ہی سے سلطنتوں کو مغلوب کیا.

The Three Youths quote Daniel 3:17, 3:18 and 3:25 in the received wording,
including its معبودوں کے بیٹے کی مانند, which is what the edition prints.
The Song of the Three is not quoted at all: the Urdu Daniel 3 runs to
thirty verses and does not carry it, so the hymn the Church took for her
seventh and eighth odes is described in the site's own prose instead.

The Meeting's prophecy in the Third Day is Luke 2:34, ایسا نشان بنے گا جس
کی مخالفت کی جائے گی.

Standing forms reused: حفاظت for the Protection, بلاخیرنے, آندریو مسیح کے
لیے احمق, پیش رو, عالمِ الٰہیات, اوموفوریون; شدرک، میشک اور عبدنگو and
نبوکدنضر and دانی ایل from the published Daniel, بابل, بیت لحم; صلیب کی
سربلندی, ملکہ ہیلینا, گلگتا, قیامت کا کلیسا, مکاریس, ہیراکلیس; اولین شہید
اسٹیفن, چرنی, عید کے بعد کے دن.

Written here for the first time: آندرے بوگولیوبسکی, ایپیفانیوس as Andrew's
disciple, دورا for the plain of the image, and بائبل کے گیت for the
Biblical Odes.

## Batch 201: the Third Finding of the Forerunner's head, the Image Not-Made-by-Hands, Sergius and Herman of Valaam, Borys and Hlib, Cyrus and John

Edessa keeps the ایڈیسا settled in batch 183, which is also this feast's
own commemoration; the vocabulary's اڈیسا in the Abgar line does not
reopen it.

Standing forms reused: پیش رو, کومانا, باسیلسکس, کپادوکیہ, سنہری دہن,
آئیکن شکن, خدا کا برہ; ہاتھوں سے نہ بنی صورت and ابگر and تھدیوس from the
vocabulary, گلیل, جسٹینین, وفات; والام, لادوگا جھیل, تجلّی, کاریلیا,
نووگوروڈ, راہب کاہن; بورس اور گلیب, رومانس اور داؤد, ویشگوروڈ, دانا
یاروسلاو, سویاتوسلاو, وسیوولود, ولادیمیر مونوماخ, آلام بردار, رسولوں کے
برابر; سائرس اور یوحنا, بے غرض معالج, مینوتھس, اسکندریہ کا سیرل,
دیوکلیشین.

Written here for the first time: ایزیاسلاو.

One opening was caught by the register check and mended: Sergius and Herman
are monastic-typed and were opened with مقدس and their names alone; they
now open والام کے جلیل القدر سرجیئس اور ہرمن, which is the wording of their
own commemoration.

## Batch 202: the translations of James of Borovichi, Vsevolod of Pskov, Philip of Moscow, Simeon of Verkhoturye, Gurias of Kazan

Standing forms reused: بوروویچی and یعقوب from the commemoration, خداوند
کا بھائی یعقوب, ایویرون, والدائی, نکون; وسیوولود-جبرائیل, پسکوف, ولادیمیر
مونوماخ, مقدس تثلیث, فسح and مسیح جی اٹھا as settled in batch 191; فلپس,
فیودور کولیچیو exactly as the vocabulary writes it, سولوفکی, تویر, ایوان
مہیب, کریملن, وفات کا بڑا کلیسا; شمعون, ویرخوتوریے, میرکوشینو, دریائے
تورا, یورال, سائبیریا; گوریاس, کازان, بارسانوفیس, تاتاری, خانیت.

Written here for the first time: مستا for the river, اوتروچ for the
monastery at Tver, یوسف for the patriarch of that translation, الکسی
میخائیلووچ, and ایوان چہارم where the entry names the tsar by number
rather than by byname.

## Batch 203: the translations of Hilarion of Meglin, John Chrysostom, Maximus the Confessor, Nicholas to Bari, Nikephoros of Constantinople

Lycia is لیکیا, thirty-six in the lives and two in the vocabulary against
لوکیا once in the lives and twice in commemorations.

Two sayings are given in the site's own prose because the site publishes
no Urdu form of either: Chrysostom's dying ہر چیز کے لیے خدا کا جلال ہو
and the greeting سب کو سلامتی ہو that the tradition says his relics spoke.
Neither is set out as though it were received text, the lives using no
quotation marks anywhere.

Standing forms reused: میگلن and ہلاریون from the commemoration, ترنووو,
مقدونیہ, یک طبیعتی; سنہری دہن, کومانا, پروکلس, ارکیڈیس, باسفورس, مقدس
رسولوں کا کلیسا; میکسمس, ہیراکلیس, یک مرضی, دو فطری مرضیاں, لازیکا, چھٹی
عالمی کونسل; نکولس, میرا, باری, مُر; نکیفوروس, ملکہ آئرین, لیو ارمنی,
اسٹودیت تھیوڈور, آئیکن شکنی, ملکہ تھیودورا, میتھوڈیس.

Written here for the first time: کالویان, بوگومل for the heresy of that
country, یودوکسیا, تھیوڈوسیس دوم, خروسوپولس, کونستانس, and سلجوقی.
Maximus's Mystagogy is named as the site names an unpublished work, by what
it is: الٰہی عبادتوں پر اُن کی کتاب.

The register check flagged Maximus's opening as a monastic named by another
rank; he now opens جلیل القدر معترف میکسمس, which is the wording of his own
commemoration.

## Batch 204: the translations of Peter of Moscow, Theoctistus of Novgorod, Tikhon of Lukhov, Ephraim of Perekop, John of Rila

Lukhov is لوخوف, seven in the vocabulary and one commemoration against
لوچوف two and one; Kostroma is کوسترما, thirteen in the vocabulary against
کوسٹروما in three commemorations.

Standing forms reused: پطرس, کریملن, وفات کا بڑا کلیسا, تاتاری; یوریو کا
مٹھ, وولخوف, آرکمنڈرائٹ, بشارت; تیخون, لتھوانیائی, سینٹ نکولس کا مٹھ;
افریم and پیریکوپ from the commemoration, ایلمین جھیل, تجلّیِ الٰہی, بازل
for the Great Prince; یوحنا, ریلا, سکرینو, صوفیہ, ترنووو.

Written here for the first time: تھیوکتستس, فوتیس as the archimandrite of
Yuriev, ویرینڈا, کلنکووو, رومانس for the abbot of the relocation, and
سریدیتس for the old name of Sofia. Perekop's name is explained in the
site's own prose, کھود کر پار نکالنا, since the entry turns on it.

The register check flagged John of Rila's opening as a monastic named by
another rank; he now opens مٹھ کے سربراہ جلیل القدر یوحنا, which is his own
commemoration's wording.

## Batch 205: the translations of Lazarus of Galesion, Nilus of Stolobensk, Theodore the Studite, Theodosius of the Caves, Zosimas and Sabbatius

Solovki is سولوفکی, twenty-four in the vocabulary and six in the lives
against سولووکی in five commemorations and two day entries.

Vasilevo near Kyiv is a genuine tie: the vocabulary carries واسیلیوو twice
under one English spelling and واسیلیو once under another, and no
commemoration names the place at all. The lives already had واسیلیو from
batch 192, so that form stands and the file keeps one spelling; where the
vocabulary itself is divided and no commemoration decides, the lives'
own consistency is the tie-break.

Standing forms reused: کوہ گالیسیون، افسس کے قریب exactly as the
vocabulary has it, لعزر, لدیہ, میگنیسیا, مقدس سینٹ ساباس, ستون نشین;
نیلس, سٹولوبینسک, ستولوبنی, سیلیگر جھیل, کریپیتسک, پسکوف, تویر; اسٹودیوس,
تھیوڈور, تھسلنیکے کا یوسف, میتھوڈیس, راست دینی کی فتح, آئیکن شکنی;
تھیوڈوسیس, واسیلیو, دنیپر, انتھونی, وفات کا بڑا کلیسا; سباتیس اور
زوسیماس, سفید سمندر, تجلّی, شہد کی مکھیاں پالنے والے.

Written here for the first time: پرنکیپو and نیلو-ستولوبینسکی for the
hermitage that grew on Nilus's island.

Two openings were mended after the register check: Zosimas and Sabbatius,
and Lazarus, all three monastic-typed, now open جلیل القدر, as their own
commemorations do.

## Batch 206: the translations of Demetrius of Uglich, Theodore Stratelates, Ignatius the God-bearer, Phocas of Sinope, Epimachus of Pelusium

Sinope is سنوپے, ten in the vocabulary and one commemoration against سنوپ
in one commemoration.

Standing forms reused: تساریوچ دیمیتریس, اوگلچ, آلام بردار, واسیلی
شوئیسکی, مصیبتوں کا زمانہ, کریملن, سردار فرشتہ میکائیل, یوحنا پیش رو;
تھیوڈور سٹراٹیلیٹس, سٹراٹیلیٹس kept beside سالار as the vocabulary does,
پونتس کا ہیراکلیہ, لیکینیس, یوخائٹا; خدا بردار اگنیشیس, انطاکیہ, ٹریجن,
کولوزیم, دافنے, تھیوڈوسیس دوم, and خدا کا گیہوں جو باریک پیسا گیا, which
is the vocabulary's own wording of his saying; فوکاس, سنوپے, بحیرہ اسود;
ایپیماکس, پلوسیم, اسکندریہ, دیسیس for the persecutor.

Written here for the first time: فیلو اور اگاتھوپس, the two companions who
carried Ignatius home.

## Batch 207: the translation of Stephen's relics, Igor of Chernihiv, the finding of the Cross by Helena, Acacius of Melitene, Juliana Olshanskaya

Chernihiv is چرنیہیو, fourteen in the vocabulary, four commemorations and
ten in the lives, against چرنیگوف four and one; the single چرنیگوف the
lives carried, written in batch 189 from the vocabulary's Liubech line,
has been changed to match. Melitene is ملیتینے, twelve in the vocabulary
and eighteen in the lives against ملیطینے in four commemorations and
میلیتین in one.

Pilate is پیلاطس, off the published John 19:19.

Standing forms reused: اولین شہید اسٹیفن, گملی ایل, نیکودیمس, کافرگمالا
and ابیباس from the vocabulary, تھیوڈوسیس دوم; اِگور-جارج and جبرائیل and
چرنیہیو from his commemoration, عظیم اسکیما, آلام بردار, بورس اور گلیب;
ملکہ ہیلینا, قسطنطین اعظم, گلگتا, مکاریس, صلیب کی سربلندی, قیمتی کیلیں;
اکاکیوس, دیسیس, آرمینیا, افسس کی تیسری عالمی کونسل; یولیانا اولشانسکایا,
اولشانسک, لتھوانیائی, لاورا.

Written here for the first time: لوسیان for the priest of the vision,
مقدس صیون for holy Zion, شماس لارنس, اِگور اولگووچ, مارکیانوس, and یوری
دوبروویتسکی-اولشانسکی.

## Batch 208: the uncoverings of Alexis of Moscow, Andrew of Smolensk, Basil of Amasea, Demetrius of Rostov, Gurias and Barsanuphius

Standing forms reused: الکسی, تائیدولا and چودوف from the vocabulary line
about the healing, سردار فرشتہ میکائیل, کریملن, دیمیتریس for the Grand
Prince as in batch 191; آندریو, سمولینسک, پیریسلاول-زالیسکی, پیریسلاول کا
دانیال, کلیسا کا خادم for the sexton, and the ring, chain and note from
his own vocabulary line; باسل, اماسیہ, گلافیرا, لیکینیس, نیکومیڈیا, سنوپے,
پونتس; دیمیتریس, روستوف, کیف, وولوکولامسک, وولگا, تویر; گوریاس,
بارسانوفیس, کازان, تجلّی, ہرموجینیس, مُر.

Written here for the first time: دیمیتریس دونسکوی, دانیال توپتالو, گریگوری
روگوتن, پرانی رسم والے for the Old Ritualists, سینٹ یعقوب کا مٹھ, and
مجلسی دور for the Synodal age. Demetrius of Rostov's Menaion is named as
the site names an unpublished work, by what it is: برس کے ہر دن کے لیے
مقدسین کی زندگیوں کا بڑا مجموعہ, which is also how the vocabulary
describes him, مقدسین کی زندگیوں کا لکھنے والا.

## Batch 209: the uncoverings of Innocent of Irkutsk, Joasaph of Belgorod, Niketas of Novgorod, Vsevolod of Pskov, Alexander of Svir

Standing forms reused: انوسنٹ, ارکوتسک as settled in batch 181, صعود کا
مٹھ, سائبیریا, یورال; یوآساف and بیلگوروڈ from the commemoration, پریلوکی,
پولتاوا, مگار, تثلیث-سرجیئس کا لاورا, والدہ خدا کا میلاد; نکیتاس, نووگوروڈ,
مقدس حکمت, مکاریس; وسیوولود-جبرائیل, پسکوف, ولادیمیر مونوماخ, مستسلاو,
زندگی بخش تثلیث; الیگزینڈر, سویر, لادوگا, اونیگا, تجلّی.

Written here for the first time: پطرس اعظم, چھوٹے روس for the Little
Russian country, چین, بحرالکاہل, مجلس for the Synod that investigated
Innocent, and گورلینکو for Joasaph's family.

## Batch 210: the uncoverings of Athanasius of Brest, Ephraim of Novy Torg, James of Zheleznoborov, Juliana of Vyazma, Macarius of Kalyazin

Juliana of Vyazma is جولیانا. Her own two commemorations disagree, one
جولیانا and one یولیانا, and the site's weight settles it, جولیانا eight
against three. Juliana Olshanskaya keeps the یولیانا of batch 207, both of
her commemorations using it; the two women are told apart as the site tells
them apart.

Brest is بریست, the vocabulary's form; his commemoration's compound
بریسٹ-لیتووسک is not carried into the prose.

The Union has no Urdu form on the site: یونیا there is the Apostle Junia,
and would collide. It is written روم کے ساتھ اتحاد at first mention and
اتحاد after, named by what it was.

Standing forms reused: اتھاناسیس, پولش-لتھوانیائی, سینٹ شمعون کا مٹھ;
افریم, نووی تورگ, تورژوک, بورس اور گلیب, آلام بردار; یعقوب, ژلیزنوبوروف,
رادونیج کا سرجیئس, کوسترما, یوحنا پیش رو; جولیانا, ویازما, شمعون, یوری,
سمولینسک, and دریائے وازوزا with the body borne upstream, both from her own
vocabulary line; مکاریس, کالیازن, وولگا, تویر, متی کوژن as the vocabulary
writes it, بویار.

Written here for the first time: دریائے تویرتسا and مکاریو کا مٹھ for the
house at Kalyazin that took its founder's name.

The register check flagged Athanasius, who is abbot-typed; he now opens
مٹھ کے سربراہ جلیل القدر اتھاناسیس, as his commemoration does.

## Batch 211: the uncoverings of Martinian of Belozersk, Maximus of Moscow, Seraphim of Sarov, Sergius of Radonezh, the martyrs at the Gate of Eugenius

Ferapontov is فیراپونتوف, six in the vocabulary against فراپونتوف two.

Maximus of Moscow is میکسیمس, the form of his own commemoration. Maximus
the Confessor stays میکسمس as settled in batch 181; the site tells the two
men apart, as it does the two Barsanuphii and the two Julianas.

Andronicus and Junia are named in the site's own form, اندرونیکس اور یونیا,
which is their commemoration; the published Romans 16:7 writes اندرنیکس اور
یونیاس, so the verse's clauses are quoted in the received wording, میرے
رشتہ دار ہیں اور میرے ساتھ قید میں بھی رہے تھے and رسولوں میں مشہور ہیں
اور مجھ سے پہلے المسیح پر ایمان لا چکے تھے, while the names in the
sentence stay the site's. The clause is quoted, the address is the site's.

Standing forms reused: مارتینین, سفید جھیل کا سیرل, بیلوزیرسک, راہب کاہن;
میکسیمس, ماسکو, مسیح کے لیے احمق, تاتاری; سیرافیم, ساروف, زوسیماس اور
سباتیس, راہب کاہن; سرجیئس, رادونیج, نکون, مقدس تثلیث کا مٹھ, لاورا;
یوجینیوس کا دروازہ from the commemoration, ارکیڈیس.

Written here for the first time: میخائیل for Martinian's baptismal name,
بازل تاریک, دیمیتریس شیمیاکا, نکولس دوم, ادیگے, خطاط نکولس, زندگی کی
کتاب, and اندرونیکس for the twelfth-century emperor who built the church.

Two openings were mended after the register check, Martinian and Sergius,
both abbot-typed; both now open جلیل القدر.

## Batch 212: Thallelaios of Aegae, Abramius the Recluse and Mary, Abramius of Smolensk, Abramius of Rostov, Acacius of Sinai

Acacius of Sinai is اکاکیس, the form of his own commemoration; Acacius of
Melitene, written in batch 207, keeps اکاکیوس from his. Two men, two forms,
as the site itself has them.

Standing forms reused: تھالیلیوس، ایگائی، الیگزینڈر اور آستیریوس exactly as
their commemoration lists them, کلیکیا, انازاربس, بے غرض معالج; ابرامیس,
میسوپوٹامیہ, ایڈیسا, افریم سریانی; سمولینسک, اگنیشیس; روستوف, ویلس and the
staff and the felled idol from his own vocabulary line, یوحنا عالمِ
الٰہیات, تجلّیِ الٰہی, آرکمنڈرائٹ; اکاکیس, سینا, یوحنا کلیماکس, سیڑھی.

Written here for the first time: نومیریان, بیروکیوس اور رومیلیا, and
چودسکوئے for the end of Rostov where the idol stood.

The two sayings, Abramius to his niece and Acacius from the tomb, are not
Scripture and are written as prose, as the lives write every such saying.

## Batch 213: Adrian of Ondrusov, Agapitus the Unmercenary, Agathon of the Caves, Akepsimas of Cyrrhus, Alexander of Kushta

Cyrrhus is کوروس, seven in the vocabulary and three in the lives, and the
vocabulary itself uses it of this saint's country, کوروس کے قریب، شام, and
of his biographer, کوروس کا تھیودوریت. سیرس on the site is chiefly the
Greek Serres, and قورس appears once.

Standing forms reused: آدریان and اوندروسوف from his commemoration,
والام, لادوگا جھیل, سویر کا الیگزینڈر; اگاپیتس, بے غرض معالج, انتھونی,
قریبی غار, ولادیمیر مونوماخ, چرنیہیو; دور کے غار, تھیوڈوسیس, لاورا, and
ہاتھ رکھنے سے شفا, which the vocabulary gives for the laying on of hands;
اکپسیماس and کوروس from his commemoration and the vocabulary, تھیودوریت,
مقدس عطیے; الیگزینڈر, کُشتا with its damma as the vocabulary writes it,
کوبینسکویے جھیل, شمالی تھیبائیڈ, وولوگدا, وفات.

Written here for the first time: آندرے زاوالیشن and اگاتھون.

## Batch 214: Alexander of Oshevensk, Alexander of Svir, Alexei Kabalyuk, Alexis the Man of God, Alexius the Recluse

Oshevensk is اوشیوینسک, three in the vocabulary against اوشیونسک in one
commemoration. Amos, the prophet whose feast gave Alexander of Svir his
baptismal name, is عاموس off the published Scripture.

Standing forms reused: الیگزینڈر, سفید جھیل کا سیرل, کارگوپول, نووگوروڈ,
شمالی تھیبائیڈ; سویر, والام, زندگی بخش تثلیث, ابراہیم, مُر بہاتے آثار;
کارپاتھو-روس and ماوراء کارپاتھیا and ایزا from the vocabulary, کوہ مقدس,
پانتیلیمون, راہب کاہن, آرکمنڈرائٹ, الیگزینڈر نیفسکی, اتحاد for the Union as
settled in batch 210; خدا کا آدمی ایلکسیس, ایڈیسا, ہاتھوں سے نہ بنی صورت,
میسوپوٹامیہ, ترسس, گیت نگار یوسف, قانون for the hymnographic canon; گوشہ
نشین ایلکسیس and ساوا from their commemorations, قریبی غار, انتھونی.

Written here for the first time: نکیفوروس اوشاوین, دریائے چوریوگا, کیریلوف
for the White Lake school, انتیمنس; الیگزینڈر کابالیوک, یابلوچنسکی,
اونوفریوس, ویلیکیے لوچکی, یاسینیا, خُست, مارماروش-سیگت; یوفیمیانوس,
اگلائیس, ربولا.

Two openings were mended after the register check, Alexander of Svir and
Alexei Kabalyuk, both monastic-typed; both now open جلیل القدر.

## Batch 215: the Alphanov brothers, Alypius the Iconographer, Alypius the Stylite, Amphilochius of Glushitsa, Ananias the Iconographer

The iconographer is آئیکن نگار, nineteen in the vocabulary and eleven in
the lives, against شبیہ نگار in five commemorations. Sokolnitsky is
سوکولنیتسکی, three in the vocabulary against سوکولنتسکی once.

Standing forms reused: سوکولنیتسکی and the five brothers in one household
from their own vocabulary line, نووگوروڈ, مقدس نکولس; الیپیس, نکون, راہب
کاہن, قریبی غار, والدہ خدا; ادریانوپولس، پفلاگونیا exactly as the
vocabulary has it, یوفیمیا, خاتون شماس, ستون نشین, شمعون and دانیال among
the great stylites; امفیلوکیس, گلوشیتسا, ڈیونیسیس, وولوگدا, اوستیوگ;
حننیاہ, انتونیوس رومی.

Written here for the first time: الفانوف for the family name, سوکولیا for
the hill, and نکیتا، کیرل، نکیفور، کلیمنٹ اور اسحاق for the five brothers.

Two openings were mended after the register check: Alypius the Iconographer
now opens غاروں کے جلیل القدر آئیکن نگار الیپیس and Alypius the Stylite
ادریانوپولس کے ستون نشین جلیل القدر الیپیس, which is his commemoration's
own wording.

## Batch 216: Anatolius of the Near Caves, Anatolius the Recluse, Andrei Rublev, Andronicus and Athanasia, Andronikos of Moscow

Standing forms reused: قریبی غار and دور کے غار, لاورا; آندرے روبلیو,
رادونیج کا سرجیئس, نکون, مقدس تثلیث, ولادیمیر, ابراہیم, آئیکن نگار as
settled in batch 215; انطاکیہ, اسقیطس, تابینیسی, مصر; ماسکو, الکسی, منجی
کی ہاتھوں سے نہ بنی صورت, قسطنطنیہ.

Written here for the first time: اناتولیس, منجی-اندرونیکوف for the
Spaso-Andronikov monastery, یونانی تھیوفینس, اندرونیکس اور اتھاناسیا,
جولین for the martyr of the vision, دریائے یاؤزا, and چاندی کا کاریگر for
the silversmith.

Two openings were mended after the register check: Rublev, who is
monastic-typed, now opens جلیل القدر آئیکن نگار; Andronicus and Athanasia,
who have no order between them, open مصر کے جلیل القدر, the venerable of
their own title.

## Batch 217: Anthony of Chernoezero, Anthony of Dymsk, Anthony of the Far Caves (twice), Anthony the Roman

The site carries Anthony of the Kyiv Caves three times, once under Caves
and twice under Far Caves, with the same English word for word each time;
all three now carry one Urdu text, on the rule settled for Sava in batch
191 and Vladimir in batch 192.

Dymsk is دیمسک, five whole-word in the vocabulary against دمسک in two
commemorations.

Standing forms reused: چرنوئزیرو and چیریپوویتس from the vocabulary,
لتھوانیائی, والدہ خدا; خوتین, ورلام, دیمسکویے جھیل, تیخوین, and لوہے کی
ٹوپی, which the vocabulary already uses of this saint and glosses عاجزی کی
لوہے کی ٹوپی; انتھونی رومی, وولخوف, نکیتاس, لاطینی, والدہ خدا کا میلاد.

Written here for the first time: شچیرا and سویڈن والے.

Anthony the Roman's opening was mended after the register check and now
reads رومی اور نووگوروڈ کے مٹھ کے سربراہ جلیل القدر انتھونی, which is his
commemoration's own wording.

## Batch 218: Anthony of Dymsk again, Anthony of Leokhnov, Anthony of Siya, Anthousa, Antiochus and Antoninus

Leokhnov keeps the vocabulary's لیوخنووو for the place and the
commemoration's لیوخنوف in the saint's own title, which is how the site
itself has them; Antiochus is انتیوکس, his own commemoration's form,
rather than the انطیوکس the vocabulary uses once.

Standing forms reused: دیمسک and دیمسکویے جھیل and لوہے کی ٹوپی as settled
in batch 217, خوتین, ورلام, تیخوین; تجلّی, مصیبتوں کا زمانہ, سویڈن,
بصیرت; سیا, کیختا, دوینا, زندگی بخش تثلیث, آئیکن نگار; انتھوسا and
مانتینیا from the vocabulary, پفلاگونیا, آئیکن شکن; کوروس کا تھیودوریت,
شامی صحرا, زاہد.

Written here for the first time: روبلیوو, کینا for the river of the
Pachomius monastery, قسطنطین کوپرونیموس, سٹراتیجیوس, فبرونیا, and آندریو
for Anthony of Siya's baptismal name.

Two openings were mended after the register check, Leokhnov and Siya, both
abbot-typed; both now open مٹھ کے سربراہ جلیل القدر, as their
commemorations do.

## Batch 219: Arcadius of Cyprus, Arcadius of Novotorsk, Arethas the Recluse, Arsenius of Novgorod, Arsenius the Great

The site keeps the saints named Arcadius as ارکادیس and the emperor
Arcadius as ارکیڈیس; both appear in this batch and both keep their own
form.

Standing forms reused: ارکادیس, قبرص, قسطنطین اعظم, جولین اور یوبولوس from
his own vocabulary line, مرتد جولین; نوووتورسک, ویازما, افریم, اسکیما,
بورس اور گلیب; اریتھاس's Caves setting with قریبی غار; ارسینیس, نووگوروڈ,
مسیح کے لیے احمق, ایوان مہیب; عظیم ارسینیس, تھیوڈوسیس, ارکیڈیس, اسقیطس,
کانوپس, اسکندریہ.

Written here for the first time: اریتھاس, ہونوریوس, ترویے, قبطی for the
Copts, and اشرافی for the patrician house.

The two voices Arsenius heard, and his answer about the peasant's alphabet,
are not Scripture and are written as prose, as the lives write every saying
the site does not publish.

## Batch 220: Arsenius the Lover-of-Labor, Arsenius of Komel, Arsenius of Konevits, Athanasius of Murom, Athanasius the Recluse

Arsenius of the Far Caves is محنت دوست, the compact form of his own
commemoration, rather than the vocabulary's fuller محنت سے محبت رکھنے والا.

Standing forms reused: دور کے غار, لاورا, فرمانبردار and روزہ دار as the
Caves' own titles; کومیل, وولوگدا, ماسکو, سرجیئس کا تثلیث کا مٹھ, تاتاری;
کونیویتس and کونیوسکایا and لادوگا جھیل and کوہ آتھوس from the founder's
own vocabulary line, والدہ خدا کا میلاد; مُروم and مُروم جزیرہ and اونیگا
جھیل and لعزر from the vocabulary, زنجیریں; تھیوڈوسیس, عظیم روزے.

Written here for the first time: شیلیگود, ورست for the Russian mile,
گھوڑے کا پتھر for the idol-rock of Konevets, and تانبے کا کاریگر for the
coppersmith.

Arsenius of Komel's opening was mended after the register check and now
reads مٹھ کے سربراہ جلیل القدر ارسینیس.

## Batch 221: Athanasius the Resurrected, Athanasius of Syandemsk, Athanasius the Athonite, Auxentius of Bithynia, Barlaam of Shenkursk

Three settled by weight: Syandemsk is سیانڈیمسک, three in the vocabulary
against سیاندیمسک in one commemoration and one day entry; Trebizond is
ترابزون, eight in the vocabulary against ٹریبیزونڈ in one commemoration;
Auxentius is اوکسینتیس, two in the vocabulary and one commemoration against
اوکسینٹیس in one.

Standing forms reused: قریبی غار, لاورا, آرکمنڈرائٹ, انتھونی اور
تھیوڈوسیس; سویر کا الیگزینڈر, کاریلیا, سیانڈیبا, وفات, شمالی تھیبائیڈ,
اسکندریہ کا اتھاناسیس; عظیم لاورا, کوہ آتھوس, ابراہیم, and اکونومسا, which
the vocabulary already gives for the Stewardess of the Holy Mountain;
بِتھینیا, کلقیدون, کوہ اسکوپا, چوتھی عالمی کونسل, دو فطرتیں; برلام,
شینکرسک, واگا, بویار, یوحنا عالمِ الٰہیات.

Written here for the first time: پولی کارپ as the archimandrite of the
Caves, واویلا, نکیفوروس فوکاس, اوکسیا for the mountain's older name,
سوویزیمتسیو, and واسیلی for Barlaam's name in the world.

Athanasius the Athonite's opening was mended after the register check and
now reads آتھوسی جلیل القدر اتھاناسیس.

## Batch 222: Barlaam of Khutyn, Barlaam of the Kyiv Caves, Barnabas of Vetluga, Barsanuphius the Great and John the Prophet, Basil the Confessor

Two Barlaams in one batch, and the site keeps them apart the way it already
did. Barlaam of Khutyn is **ورلام**, settled in batch 3053's count - eight in
the vocabulary against four برلام in the commemorations - and every other
Barlaam is **برلام**, which is what the martyr of Caesarea and the venerable
of Shenkursk already carry in the lives. So the first abbot of the Kyiv Caves
is برلام, and Khutyn keeps its own form. خوتین (thirteen in the vocabulary,
nine in the lives) stands against the commemoration's خوتن.

Barsanuphius the Great is **برسانوفیوس اعظم**, and John the Prophet is
**یوحنا نبی**, both from the day entry, which carries this pair already and
also gives ابا سیریڈس and غزہ. His namesake of Tver keeps بارسانوفیس, as
batch 193 settled. The commemoration of the Gaza pair writes بارسانوفیس too,
but the day entry is about these two men and no others, and it is followed.

Basil the Confessor is **باسل**, not the بازل his own commemoration writes.
That was settled long ago on the prayers, which print باسل twice and بازل
never, and the lives now stand at ninety-eight against thirteen. Decapolis is
**دیکاپولس**, eleven in the vocabulary against four ڈیکاپولس in the
commemorations, and Procopius is **پروکوپیس**, which the lives already carry
four times.

Written for the first time: Vetluga ویتلوگا and the Red Mountain سرخ پہاڑ,
both from the vocabulary; the Volkhov وولخوف, seven times in the lives
already; Izyaslav ایزیاسلاو, three in the lives against one ازیاسلاو;
Seridos سیریڈس and Dorotheos of Gaza غزہ کا دوروتھیس, both from the
vocabulary; Alexis ایلکسیس, the baptismal name of Barlaam of Khutyn, settled
in batch 210; Leo the Isaurian لیو اسورین, which the lives already use.

Frost is پالا, the ordinary word, in the June snow at Khutyn; despondency in
Barsanuphius' letters is مایوسی, which the prayers print five times and the
lives six. Nothing in these five lives quotes Holy Scripture. Basil's closing
alludes to the sending out of the apostles two by two, and it is written as
the site's own prose, not set as a quotation.

## Batch 223: Bassian of Tiksnensk, Benedict of Nursia, Benjamin of the Kyiv Caves, Bessarion of Egypt, Botolph of Iken

Totma is **ٹوٹما** in the lives. The vocabulary writes توتما of its other
saints, thirteen times, but the lives already carry ٹوٹما eight times for the
town itself, and two commemorations have it that way; the file keeps one form
for one place, and the note at batch 794 said as much already.

Iken is **آئکن**, which the vocabulary writes, not the commemoration's آئیکن.
The commemoration's form is the site's own word for an icon, fifty-one times
in the lives alone, and a marsh in East Anglia should not be spelled like the
holy images. The vocabulary settles it without any strain.

Written for the first time: Bassian باسیان and Tiksnensk تکسننسک, both from
the commemoration, and the river Tiksna تِکسنا from the vocabulary; Subiaco
سوبیاکو, Monte Cassino مونتے کاسینو and Scholastica اسکولاستیکا, all three
already in the vocabulary; Botolph بوتولف from his commemoration. Three names
had no form anywhere and are written on the site's own patterns: the Gothic
king Totila توتیلا, the monastery Ikanhoe اِکانہو, and the river Alde آلڈے.
Boston is بوسٹن.

Benedict's Rule is **قاعدہ**, the word the vocabulary uses of Gregory's
Pastoral Rule and the lives use thirty times; a synaxarion is سناکسارین,
settled at batch 1124; obedience is فرمانبرداری, eighty-seven in the lives.
Gregory's phrase about the boy who fled Rome, knowingly unlearned and wisely
untaught, is his own and is written as prose, without quotation marks, as
this file writes every saying.

The one place Holy Scripture is quoted is Benjamin's conversion, where the
English says he heard the words of the Savior: Matthew 19:23 is given as the
published Urdu New Testament has it. The rich man and the needle's eye, the
pearl of great price, and what is impossible with men are alluded to in the
site's own prose, as the English alludes to them, and are not set as
quotations.

## Batch 224: Cassian and Gregory of Avnezh, the two Cassians of Uglich, Cassian of Komel, Chariton of Syanzhemsk

Avnezh is **آونیژ**, five times in the vocabulary, against the
commemoration's اونیج. Ferapontov is فیراپونتوف, six in the vocabulary and
two in the lives against two فراپونتوف.

Cornelius needed sorting, because three men carry the name and the site was
using three spellings without dividing them. It divides them now. The
centurion of Acts is **کرنیلیس**, which the lives use of him six times;
Cornelius of Komel is **کورنیلیوس**, three in the lives and both of the
vocabulary's entries about his monastery; Cornelius of the Pskov Caves is
کورنیلیئس, his own commemoration's form. One stray کرنیلیس of Komel in the
lives was corrected to کورنیلیوس.

Chariton of Syanzhemsk is **خریطون**, his own commemoration's form and the
Palestinian confessor's as well; خاریتون in the lives belongs to a martyr
deacon and to a companion in another martyrdom, and the two are left apart.
Syanzhemsk is سیانژیمسک and the river Syanzhema سیانژیما; the monastery is
of the Ascension of the Lord, خداوند کا صعود, as the commemorations write it.

Written for the first time: Mangup مانگوپ and Uchma اوچما from the
vocabulary, Lake Sura سورا جھیل likewise, and Sophia Palaiologina
**صوفیہ پیلیولوگینا**, who had no form anywhere on the site and is written
here on the pattern the site uses for Greek names in Russian entries.

The site carries the Uglich Greek twice, as Cassian of Uglich and as Cassian
the Greek of Uglich, with different English. Both are written, each from its
own entry, and both take اوگلچ کے کاسیان with the names, places and dates
agreeing between them, since they are one man.

## Batch 225: Chariton of Palestine, Cherimon of Egypt, Constantine and Cosmas of Kosinsk, Constantine of Synnada, Constantine of Murom

Constantine is **قسطنطین**, eighty-six times in the lives against one
کونسٹنٹائن, which stands in a list of martyrs. Three commemorations write
کونسٹنٹائن, including both of this batch's, but the file's own weight settles
it and the men are the same name. Kosinsk is کوسینسک and Dymsk دیمسک, both
from the vocabulary against the commemorations' کوسنسک and دمسک; Iconium is
اکونیوم, fourteen in the lives; Phrygia فروگیہ, nineteen.

The prince of Murom is opened **مُروم کے دیندار شہزادہ قسطنطین**, the rank
this site gives every right-believing prince, though his commemoration writes
جلیل القدر. The register check reports it as a saint given another rank than
his order suggests, which is a review and not an error, and it is the right
answer: the English calls him the Holy Right-believing Prince, and دیندار
شہزادہ is what that is in Urdu.

Written for the first time: the lavras of Douka دوکا and Souka سوکا, which
had no form anywhere and are written on the pattern of فاران; Cherimon
خریمون and Staraya Russa ستارایا روسا from the commemorations and the
vocabulary; Svyatoslav سویاتوسلاو, eight in the lives already; Jericho یریحو,
which the published Scripture and the lives both write.

Galatians 4:4-5 stands behind the last sentence of Constantine of Synnada,
and the English weaves it into its own sentence rather than quoting it. It is
written the same way here, in the site's prose but following the published
edition's words, شریعت کے ماتحت and خرید کر چھڑا لے, and it is not set as a
quotation.

## Batch 226: the two Corneliuses again, Cosmas of Yakhrom, and the two Cyriacuses of the Carpathians

A fourth Cornelius arrived, of Paleostrov, and his commemoration writes
کرنیلیس, which batch 224 had given to the centurion of Acts. He keeps it. The
division that matters is between the two Russian founders, Komel's
**کورنیلیوس** and the Pskov Caves' کورنیلیئس; nobody will take an island
abbot on Lake Onega for a Roman centurion, and a man's own commemoration is
worth more than a spelling kept free for tidiness.

Paleostrov is پالیوستروف, three in the vocabulary against the
commemoration's پالیوسٹروف. Tazlău is **تازلاو**: three تازلاؤ in the
vocabulary against two تازلاو there and one in the commemoration, an exact
tie, and a commemoration decides a tie.

Standing forms reused: اولونیتس, اونیگا, پالی, ابرامیوس, یاخروما, نورما,
تھیبائیڈ, بیسیریکانی, نیامتس, بستریتسا, دوسوفتے, کارپاتھی, پاتیریک,
گیناڈیس, عظیم اسٹیفن, and والدہ خدا کے ہیکل میں داخلہ for the Komel
monastery's feast. A podvig is معرکہ and a hesychast خاموشی کا عابد, both
the vocabulary's own.

Written for the first time: the Kriukovs کریوکوف and the brother Lukian
لوکیان; the Kosmin monastery کوسمین, named from its founder as the English
names it; Mesteacăn مستیاکان and the mountain Măgura ماگورا; Transylvania
ٹرانسلوانیا. The Calvinist pressure on Moldavia is written
کالون کے ماننے والوں کا پرچار, since the site has no word for the party and
names it by its founder, as it does other movements.

Nothing in these five lives quotes Holy Scripture.

## Batch 227: three Cyrils, Dalmatus of Constantinople, and the three of the Near Caves

Cyril is **سیرل**, fifty-eight in the lives and twenty-six in the vocabulary
against کرل and کیرل, which the commemorations use; all three men in this
batch take it. Novoezersk is نوویزیرسک, Belozersk بیلوزیرسک, Chelma Hill
خیلما پہاڑی, Nestor the Chronicler نسٹور, Nestorius نسطوریس, Ephesus افسس,
all on the vocabulary's and the lives' weight.

Ferapont, Cyril's companion, is **فیراپونت**, ten in the vocabulary and the
name the lives already carry three times in فیراپونتوف, his monastery. His
commemoration writes تھیراپون, but the lives use تھیراپون of two martyred
bishops, of Cyprus and of Sardis, seven times between them, and the White
Lake founder is a different man.

**Two texts the site does not publish in Urdu, and how they are handled.**
The infant Cyril cries the Sanctus in his mother's womb. The site's prayers
do not carry the anaphora, and the Urdu Isaiah 6:3, which is where the words
come from, renders the divine name یاہوہ, which appears nowhere else here; so
the verse is not quoted. The life says instead, in the site's own prose, that
the child cried the threefold Holy of the seraphim that Isaiah heard in the
temple. The eighth kontakion of the Akathist to the Theotokos is handled the
same way: only the Akathist for the Departed is published in Urdu, so the
kontakion is described, not set down as a received text. The Mother of God's
own words to Cyril are neither Scripture nor a service text, and are written
as prose like every other saying in this file.

Written for the first time: the Chud people چود; Lake Siverskoye
سیورسکویے and Mount Myaura میاؤرا; Beloozero بیلوزیرو from the vocabulary;
the Kirillo-Belozersky کیریلو بیلوزیرسکی. Standing forms reused: گالچ,
کارگوپول, سرخ جزیرہ, تجلّیِ الٰہی, سیمونوف, ماخرا, ہودیگیتریا,
مقدس انتونیوس رومی کا مٹھ, دلماتی خانقاہ, دالماتس, فاوستس, آرکمنڈرائٹ.
Cyril's baptismal name is کوسما, forty-six across the bodies against
thirty-six کوسماس.
## Lane C, first batch: ten icons of the Mother of God

This lane works the same list from the back, so its batches begin at the Z end
of the index and are numbered from where the file stood when it started. The
first ten are all icons of the Mother of God, and all ten are already named in
the commemorations, so the name and the place were looked up rather than
decided.

The commemorations set an icon's title in typographic quotes and call it a
شبیہ - پسکوف غاروں کی ”نرمی کی کنواری“ والدہ خدا کی شبیہ. The lives take the
straight quotes the house rules require and the آئیکن the lives' own register
uses; the words inside the quotes are the commemoration's and are not
re-decided.

Korets is **کوریتس**, the vocabulary's form four times, against the
commemoration's کوریٹس once. The rule that the commemorations win is a rule
about how the Church names her saints; here the vocabulary carries this icon's
own place-line, its convent and its title, and the Byblos note settles it the
same way.

Shuya is **شویا** throughout, which the vocabulary writes of the town, so the
icon is شویا-سمولینسک and not the commemoration's شویو-, whose spelling comes
from the English key's Shuiu. One form for one place, as batch 223 said of
Totma.

Sinners are **گناہگار**, which the commemoration of this icon and the
vocabulary's title of the other Surety icon both write; گنہگار stands where it
is already printed and is not spread.

Simeon's prophecy is narrated, not quoted, because the entry narrates it: the
words are Luke 2:35 as the published Urdu New Testament has them, غم کی تلوار
تیری جان کو بھی چھید ڈالے گی, put in the third person and unpointed. The
thirteenth kontakion of the Akathist goes the other way and is reported in the
site's own prose without quotation marks, since no Urdu of it is published
here; that is the rule the katavasia note set.

An icon's precious cover is **غلاف**, the word the vocabulary uses of the
Vladimir copy; the Kozelshchansk riza is چاندی کا غلاف. Polish is
**پولستانی**, which the lives use of the Time of Troubles rather than the
modern پولش.

Written for the first time: the river Desna دیسنا and the Kapnist family
کاپنست, neither of which had a form anywhere, both on the site's own patterns.

## Lane C, second batch: the Bogolyubov and Yaroslavl-Pechersk icons, and eight virgin martyrs

The Yaroslavl-Pechersk entry carries a bracketed editorial note about which
icon belongs to the day in this collection. It is not part of the life and is
not written here, on the rule that nothing about how the site is made reaches a
reader; German, Spanish, Romanian, Hindi and Arabic drop it too, and the three
that carry it are the exceptions.

Amisus is **امیسوس**, the form its own place-line gives; the اماسوس of the
clause naming the seven companions is the stray. The seventh sister is
**تھیوڈوسیا** in the life and in that same clause, though the commemoration's
title says Theodora; the entry is written from the life, which is what the
Church is remembering.

Taken from the vocabulary rather than rendered again: the Bogolyubov vision
itself - والدہ خدا تنہا دعا میں کھڑی, its طومار turned toward Christ - the
Chalke gate خالکے دروازہ and the ram's horn, the brazen ox پیتل کا بیل, the
brothel بدکاری کا گھر, the wheel چرخی, the church of the Procession of the
Precious and Life-giving Cross at Yaroslavl, and the Melkite synaxarion
ملکائی سناکسارین. Leo the Isaurian is لیو اسورین, Diocletian دیوکلیشین,
Maximian مکسیمیان, Hadrian ہادریان, Thessalonica تھسلنیکے.

A pagan is **بت پرست**, three hundred and forty-six times in the lives and the
vocabulary; one اَن یہودی written here was corrected before the batch was
filed, since it says non-Jew and not idolater.

Written for the first time, none of them having a form anywhere: Yuri
Dolgoruky یوری دولگوروکی, Alexandra Dmitrievna Dobychkina الیگزینڈرا
دمیتریئیونا دوبیچکینا, and the four officials of the martyrdoms - Paschasius
پاسکاسیس, Africanus افریکانوس, Eleusius الیوسیس and Virilus ویریلس.

## Batch 228: three Daniels, the Stylite of the Bosphorus, and Demetrius of Priluki

Demetrius of Priluki is **دیمیتریس**, forty-four in the lives and fourteen in
the vocabulary, though his own commemoration writes دیمتریوس, which appears
nowhere else. Donskoy stays دیمتری دونسکوئے, as he has been since batch 4187.

**There is no word for a godfather on this site, and none is coined.** The
vocabulary says of Donskoy that Demetrius took his children from the font of
baptism, بپتسمہ کے حوض سے لیے, and both lives in this batch that need the idea
use that construction: Daniel is called to take the prince's son from the
font, and Demetrius takes the heirs of Moscow from it. It reads as a Church
sentence rather than a loan word, which is the point.

Standing forms reused: عظیم اسکیما, ساموساتا, ستون نشین شمعون, اناپلوس,
باسفورس, گیناڈیس, زینو, باسیلسکس, تھریس, پیریسلاول-زالیسکی, پفنوتیس,
بوروفسک, پریلوکی and منجی-پریلوکی, پاخومیس, شوژگورا and شوژگورسک,
اولین شہید, تائیگا, and زار ایوان مہیب. A Monophysite is یک طبیعت, fourteen
in the lives; a cenobitic house is اجتماعی.

Written for the first time: Niverta نیویرتا and Maratha ماراتھا, neither of
which had a form anywhere; the Goritsky monastery گوریتسکی. The skudelnitsa
is kept as **سکودیلنیتسا** and glossed in the sentence itself as the common
burial place on the hill outside the town, because it is the name of the
place Daniel carried the dead to and not a general word.

Daniel the Stylite's mother is مرتھا, the vocabulary's form in the entry
about this very saint; مارتھا in the lives belongs to the mother of Simeon
the Stylite the Younger. Nothing in these five lives quotes Holy Scripture.

## Batch 229: Diodoros of George Hill, three Dionysii, and the paschal answer from the relics

Dionysius is **ڈیونیسیس**, settled long ago on the count and standing at
forty-two in the lives against one دیونیسیس; all three men in this batch take
it, though all three commemorations write دیونیسیس. Solovki is سولوفکی,
twenty-four in the vocabulary; Rzhev رژیف; Glushitsa گلوشیتسا; Hermogenes
ہرموجینیس; Aegina ایجینا; Zakynthos زاکنتھوس; George Hill جارج پہاڑی; the
Time of Troubles مصیبتوں کا زمانہ.

**The paschal greeting, and its answer.** The lives already carry
**مسیح جی اٹھا** five times, and one day entry has it with میری خوشی, so the
greeting was not decided here; it was already the site's. The answer had no
form anywhere, and is written **بے شک وہ جی اٹھا**. بے شک is the lives' own
word, six times, and it is the half of the exchange the relics of the fathers
gave back to Dionysius in the Far Caves, so it is written as the greeting's
own answer and not as a rendering of a service book.

Written for the first time: Turchasovo تورچاسووو and Vodlozero وودلوزیرو;
Yuryeva Gora یوریوا گورا beside the vocabulary's جارج پہاڑی; Hierotheos
ہیروتھیوس; the Sigouros family سیگوروس, the Strophades سٹروفادیس and
Anaphonitria انافونیتریا, none of which had a form; Shchepa شچیپا; Avraamy
Palitsyn آورامی پالیتسن. A cellarer is **بھنڈاری**, the ordinary Urdu word
for the keeper of a house's stores, which is exactly the office; the site had
no term.

Diodoros' mother is ماریا, which the lives use seventeen times of women who
are not the Theotokos; مریم is kept for her and for the Marys of Scripture.

## Lane C, third batch: eight virgin martyrs, Peter's chains, and Anthony the Great

**Anthony the Great is انتھونی اعظم.** Both bodies write both orders, and the
commemorations themselves are divided - عظیم انتھونی and عظیم مکاریس against
اتھاناسیس اعظم and بازل اعظم - so the counting decides rather than the rule
that the commemorations win. The vocabulary writes X اعظم throughout: باسل
اعظم twenty-six against one, اتھاناسیس اعظم eleven against one, انتھونی اعظم
nine against two. The lives take the majority pattern, which is also the one
the commemorations use more often than not.

Heraclea is **ہیراکلیہ**, six times in the vocabulary including this martyr's
own place-line and her island, against the commemoration's ہیراکلیا; the
Korets note settles it. Thessalonica stays **تھسلنیکے**, so Anysia's
commemoration, which writes تھیسالونیکا, is a third stray beside the
تھیسالونیکی the Thessalonica note already left alone.

Eupraxia of Tabenna is opened **جلیل القدر**, not سینٹ. The index calls her a
virgin martyr and the entry a nun who fell asleep in peace at thirty; a
monastic takes the monastic honorific, which is the one distinction the
register check asserts, and the entry was corrected before it was filed.

Scripture is looked up, not rendered. Matthew 19:21 in Anthony's life, and in
the feast of the Chains, Acts 12:7 and the iron gate of 12:10, all as the
published Urdu New Testament has them, unpointed; the apostle's own word over
the chains is 2 Timothy 2:9, خدا کا کلام قید نہیں ہے, and the sentence the
Church reads over Agnes is 1 Corinthians 1:27. Anysia's one sentence to the
soldier is written as prose without quotation marks, as this file writes every
saying.

Taken from the vocabulary: Bryene برینے, Laodicius لاؤدیکیس, the three martyr
brothers Alphaeus, Philadelphus and Cyprian, Leontini لیونتینی, Tabennisi
تابینیسی, Coma کوما, Paul of Thebes تھیبس کا پولس, the Via Nomentana, the
empress Eudocia یودوکیا, and Nisibis نصیبین.

Written for the first time: Pispir پسپیر, Sirmianus سرمیانوس, Dacian داکیان,
the prefect Sabinus سبینس, the patriarch Juvenal جووینل taken from the form
the vocabulary gives the Alaskan of that name, and the emperor Antoninus
انتونینس.

## Batch 230: Dius of Antioch, Dometius of Dionysiou, Domnica, and the two Dositheuses

Every name in this batch was already on the site, and the commemorations and
the vocabulary agree throughout: دیوس, دومیتیس, دیونیسیو, دومنیکا, دوسیتھیس,
دوروتھیس, سیریڈس, یوفروسینس, ویرکنیوسٹروف, ویرخنی اوستروف, پسکوف جھیل,
کارتھیج, گتسمنی, کوہِ آتھوس, یوحنا پیش رو, نبی زکریاہ. Nectarius is
نکتاریوس, the form the commemoration of Nectarios of Aegina carries.

**Dispassion is نفسانی خواہشوں سے آزادی.** The vocabulary has no word for
apatheia, but it does name the passions twice, نفسانی خواہشیں, so the freedom
from them is written out of the site's own phrase rather than translated as
بے حسی, which in Urdu means callousness and would say the opposite of what
the fathers mean.

The three sayings in Dositheus of Palestine, the Mother of God's little rule
at the icon of the Judgment, Dorotheos' word about the knife, and the Great
Old Man's dismissal, are sayings in a life and not service texts, and are
written as prose like every other saying in this file. Barsanuphius keeps
برسانوفیوس, as batch 222 settled, since this is the Gaza elder.

## Lane C, fourth batch: two Zosimases, two Zenos, two Xenophons, and Xenia of Rome

Solovki is **سولوفکی**, twenty-four times in the vocabulary and nine in the
lives already, against the commemorations' سولووکی five. The lives keep one
form for one place, as the Totma and Shuya notes both say, and the form they
are already written in is the one they keep.

Sabbatius of Solovki is **سباتیس**, fourteen times across the three bodies;
the ساواتیوس of one vocabulary clause is the stray. Mylasa is **میلاسا**
unpointed, the pointed مِیلاسا beside it being the vocabulary writing with
diacritics the index does not reproduce.

Taken from the vocabulary rather than rendered again: the Charsia gate
خارسیا, the church suspended in the air over Solovki, Theodoret of Cyrrhus
تھیودوریت, Varlaam of Khutyn خوتین کے ورلام, Robeika روبیکا, Khlynov خلینوف,
Mezen میزین, Cornelius of Komel, Caria کاریا, and the deaconess خاتون شماس.

Written for the first time: Marfa Boretskaya مارفا بوریتسکایا, the Pyskor
monastery پسکور, the river Mulyanka مولیانکا, and the two peoples of the
Kama, the Ostyaks اوستیاک and the Voguls ووگول.

## Batch 231: Eleazar of Anzersk, Elias of Murom, Ephraim the Syrian, and two more Ephraims

**The Prayer of Saint Ephraim is not published in Urdu on this site, so it is
not set down here.** The prayers carry a hundred texts and this is not one of
them; the glossary's پاک دامنی belongs to the entry on a monk's vows, not to
the Lenten prayer. So the life does what the English does, and names what the
prayer asks: against سستی، مایوسی، حکومت کی چاہ اور فضول باتیں, and for
پاک دامنی، فروتنی، صبر اور محبت, with its opening named and its last line
reported rather than reproduced, that the Lord grant His servant to see his
own sins and not to judge his brother. Naming a prayer's petitions is not
publishing the prayer, and the site will not put an unreceived rendering of a
Lenten text into a reader's mouth.

Elias of Murom is **ایلیاہ**, his own commemoration's form, which keeps him
apart from the Prophet Elijah, ایلیاس in the lives four times. Edessa is
ایڈیسا, twenty-six in the lives against the vocabulary's nine اڈیسا; Nisibis
نصیبین; Anzersk انزیرسک, the vocabulary's form against the commemoration's
انزرسک; Eustathius یوستاتھیس, seventeen in the lives.

Standing forms reused: الیعزر, کوزیلسک, ایرینارکس, اسقیطس, نکون, ابگر,
تورژوک, نووی تورگ, بورس, گلیب, ہنگری موسیٰ, آلام بردار, پیریکوپ, کاشن,
ایلمین. An equerry is **میر آخور**, which the vocabulary already writes of
this very saint.

Written for the first time: the Severiukov family سیویریوکوف; Nikita نکیتا;
Tsar Michael زار میخائل; Chobotok چوبوتوک, glossed as the boot in the
sentence, since it is a nickname and not a word; the bogatyr بوگاتیر and Ilya
ایلیا of the epic songs; the madrashe مدراشے, glossed as teaching hymns;
Svyatopolk سویاتوپولک and the river Alta آلتا; the river Verenda ویرنڈا.

## Lane C, fifth batch: two Tituses, two Tikhons, two Thomases, two Theraponts

Lukhov is **لوخوف**, thirteen times across the bodies including this saint's
own place-line and the monastery that grew from his labor, against the لوچوف
of his feast's commemoration. Symbola goes the same way and for the same
reason: **سیمبولا**, five times in the vocabulary, which carries his
place-line "of Symbola in Bithynia", against the commemoration's سمبولا.

Bithynia is **بتھینیا** unpointed. The vocabulary writes بِتھینیا thirty-three
times, but the lives already write the unpointed form twenty-two times against
eight, and the pointing rule is that the index does not point.

Ferapontov is **فیراپونتوف**, as batch 224 settled; the فراپونتوف of one
vocabulary clause is the stray. Theophilus of the Near Caves is **تھیوفیلس**,
his own commemoration's form, though the vocabulary's clause for his companion
Sisoes calls him تھیوفیلوس; both forms stand elsewhere and neither is spread.

Taken from the vocabulary rather than rendered again: the angel with the
flaming spear between Titus and Evagrius, the sealed letter answered unopened
on Mount Kyminas, the hollow oak on the Vepreika, the sacks of grain stored
against the famine on the Monza, and the Paterikon پاتیریک.

Written for the first time: the river Kopytovka کوپیتووکا, Prince Theodore
Belsky تھیوڈور بیلسکی, Maloyaroslavets مالویاروسلاویتس, and the iconographer
Dionisius دیونیسی.

## Batch 232: Erasmus of the Caves and four Euphrosynes

Euphrosyne is **یوفروسینے**, six in the lives, five in the vocabulary and
three in the commemorations, against ایفروسینے in four commemorations and
nowhere else; all four women take it. Eudokia of Moscow is **یودوکیا** on the
same reasoning, three across the bodies against one ایودوکیا, which stands
only in her own commemoration.

The Mother of God's words to Erasmus carry a clause of the Gospel inside
them, that the poor you have always with you. The site publishes John 12:8
and Matthew 26:11 in identical words, so that clause is written as the
published edition has it, غریب غربا تو ہمیشہ تمہارے ساتھ رہیں گے, and her own
half of the sentence continues from it in prose. The rest of her words, and
Euphrosyne of Alexandria's disclosure to her father, are sayings in a life
and are written as prose, without quotation marks, as this file writes every
saying.

Standing forms reused: ایراسمس, سوزدال, کریملن, باتو, پولوتسک, پریدسلاوا,
لازار بوگشا, بیلاروس, تھیودولیا, پفنوتیس, خواجہ سرا, صعود کا راہبہ خانہ,
چوغے کے رکھے جانے کا راہبہ خانہ, and قیمتی صلیب for the True Cross. An
icon's cover is غلاف, which Lane C settled at its batch 225.

Written for the first time: Smaragdus سماراگدس, the name Euphrosyne of
Alexandria took as a monk, and Vseslavich وسیسلاوچ, neither of which had a
form anywhere.

## Lane C, sixth batch: three Theophaneses, four Theodosiuses, two Theodores

Totma stays **ٹوٹما** in the lives, as batch 223 settled; the vocabulary's
توتما is not brought in even where it carries this saint's own salt works.
Pachomius the Great is **پاخومیس اعظم**, the name seven times against two and
the epithet in the order the Anthony note fixed.

Theodosius of Totma keeps his family name **سومورین** and his monastery
اسپاسو-سومورین, both from the vocabulary. The Studite rule is سٹودیون کا
قاعدہ, the form the lives and the commemorations both use.

The Far Caves entry says in the Church's own voice that the founder is
listed twice under one feast, once simply of the Caves and once of the Far
Caves, and it is written as it stands; that is a statement about the
Church's calendars, not about how this collection is made, and the note at
the Yaroslavl-Pechersk icon does not reach it.

Dropsy had no form here and is **استسقا**. Written for the first time
besides: Megalo میگالو, George the Syncellus جارج سنکیلوس, and Euboea ایویا.

## Batch 233: Eusebius of the open sky, three Euthymii and Euthymius the Great

Psalm 19:1 is quoted from the published Urdu Psalter, آسمان خدا کا جلال ظاہر
کرتا ہے, in the closing sentence of Eusebius, where the English says he took
the Psalmist literally. The verse carries no divine name and needed no
reporting. The voice to the parents of Euthymius the Great is a saying in a
life and is written as prose.

Standing forms reused: اسیخا, کوروس کا تھیودوریت, نیژنی نووگوروڈ, ڈیونیسیس,
کوبینا جھیل, کُشتا, الیگزینڈر, سیانژیما, خریطون, ملیتینے, یودوکسیس, فاران,
تھیوکتسٹس, ساباس, کیریاکوس, کلقیدون, ملکہ یودوکیا, سراسین, اوپسو, گلتیہ,
نکیتاس, اولمپس, بِتھینیا, پیریستیرائی, تھیسالونیکا, آندریو. Euthymius is
یوتھیمیس throughout, as the commemorations and the vocabulary both write him;
a coenobium is مشترکہ مٹھ; the Three Hierarchs are تین سردار کاہن, the
vocabulary's own.

Written for the first time: Boris Konstantinovich بورس کونستانتینووچ, and the
Stone Island of Lake Kubena, پتھر کا جزیرہ, which the site names only by its
lake. Nothing else in this batch needed deciding.

## Batch 234: Euthymius the Silent, Faustus, Genevieve of Paris, Gennadius of Kostroma, George of Maleon

Gennadius is **گیناڈیس**, seven in the lives and one each in the vocabulary
and the commemorations, against گناڈیس which stands only in this saint's own
commemoration. Kostroma is کوسترما, twenty-one across the vocabulary and the
lives against three کوسٹروما in commemorations; the Peloponnese is پیلوپونیس,
twenty against one پیلوپونیز.

Standing forms reused: اسکیما راہب, دنیپر, اسحاقیس, دالماتس, فاوستس, والنس,
آریوسی, نسطوریس, دلماتی خانقاہ, نانتیر, اوسیر کا جرمانس, اتیلا, ہُن, ترویے,
لیوبیموگراد, موگیلیف, پروسفورا, زارینہ, سویر کا الیگزینڈر, کورنیلیوس,
سورا جھیل, کوہ مالیون, لاکونیا, سناکسارین.

Written for the first time: the Seine سین; Clovis کلوویس and Childeric
چلدیرک, and the Franks فرینک, none of which had a form; Anastasia Romanovna
اناستاسیا رومانوونا and the Romanov house رومانوف; Ivan the Fourth
ایوان چہارم, written as the English names him rather than as زار ایوان مہیب,
which the site keeps for the byname; the Gennadiev monastery گیناڈیف, named
from its founder as the English names it.

Euthymius the Silent's byname is written **خاموش**, the plain word, and the
sentence says the Lavra's books call him so; the site has no title to borrow
and none is invented. Nothing in these five lives quotes Holy Scripture.

## Lane C, seventh batch: Theodore Trichinas, the Branded, and the desert mothers

The life of Theodore Graptus takes its words from his brother's, which the
lives already carry: داغ دار for the Branded, the twelve verses cut with hot
needles, لیو ارمنی and میخائیل and تھیوفیلس, and the confession written on the
face. Where one brother's life has already said a thing, the other's says it
the same way.

Symbola stays **سیمبولا**. A second commemoration has now turned up writing
سمبولا, so the count is five in the vocabulary against two in the
commemorations; the vocabulary carries both saints' place-lines, the lives now
carry the form once, and one place keeps one form.

Written for the first time: Trichinas ٹریخیناس and the garment ٹریخینا,
Graptoi گراپتوئی, Michael the Stammerer میخائیل ہکلانے والا, Cucomo کوکومو,
Theopiste تھیوپسٹے, Synkletika سنکلیتیکا, and the desert mother's title
امّا. A procuress is دلالہ and a cancer سرطان, which the lives already use.

## Batch 235: George the Chozebite, three Gerasimuses and Gerontius the canonarch

Lycia is لیکیا and Cephalonia کیفالونیا, both the vocabulary's forms against
the commemorations' لوکیا and سیفالونیا. Everything else was already settled:
خوزیبا, وادی قلط, قبرص, یردن, تھیبائیڈ, یوتیخس, چوتھی عالمی کونسل, تریکالا,
اومالا, کیننارک, لیونٹیس, پاتیریک, گیراسیمس, گیرونٹیس, سناکسارین.

Written for the first time: the Gnilets monastery گنیلیتس and the Kaisarova
creek کائیساروفا; the Notaras house نوتاراس; New Jerusalem نیا یروشلیم, the
convent on Cephalonia, written plainly since it is a monastery's name and not
the city's. A lamplighter at the Holy Sepulchre is چراغ جلانے والا,
descriptive, as the site names offices it has no word for.

The **kliros** is written **کلیروس** and glossed in the sentence as the
singers' place. The site has no word for it, and the alternatives all name
either the choir or the platform rather than the office the last sentence of
Gerontius means, which is the singers' station understood as a station of
service. So the word is kept and explained where it stands.

## Lane C, eighth batch: two Sylvesters, five Stephens, two Sophronii

The index carries Simeon the Myrrh-gusher twice, once under his monastic name
and once as Stephen (in monasticism Simeon), Prince of Serbia, with the same
English word for word. Both entries are written, and the second is the first
verbatim, since they are one man and one text.

Triglia is **ٹریگلیا**, the commemoration's form, four against the
vocabulary's two. Sophronius of the Far Caves is **سوفرونیس**, as his
commemoration has him; Sophrony Sakharov of Essex, who has no commemoration
here, is **سوفرونی**, the Russian name kept distinct from the Greek one, and
his family name **سخاروف**.

Written for the first time: Vydubichi ویدوبیچی, Makhrishche ماخرشچے (the
place Makhra ماخرا being already in the vocabulary), and the Sunday of the
Publican and the Pharisee, محصول لینے والے اور فریسی کا اتوار. The Lenten
Triodion keeps the ترودیون the lives already write.

## Batch 236: Gregory the Decapolite, Gregory the Iconographer, Gregory of Pelsheme, Herodion, Hilarion of Gdov

Four forms settled against the commemorations, all on weight. Decapolis is
دیکاپولس, eleven in the vocabulary against four ڈیکاپولس, as batch 225
already settled. An iconographer is **آئیکن نگار**, twenty-five in the lives
and twenty-one in the vocabulary against شبیہ نگار in five commemorations.
Iloezersk is ایلوزیرسک, the vocabulary's, not the commemoration's ایلوئزرسک.
Hilarion is **ہلاریون**, eight in the lives and ten in the commemorations
against ہیلاریون once in the lives and three times in the vocabulary; here
the commemorations and the lives agree and the vocabulary is the outlier.

Standing forms reused: آئرینوپولس, اسوریہ, گیت نگار یوسف, بستریتسا, الیپیس,
پیلشما, لوپوتوف, گالچ, ایلو جھیل, ہیروڈیون, کورنیلیوس, بیلوزیرسک,
یوفروسینس, گدوف, ژیلچا, لیوونی, and حفاظت for the Protection of the
Theotokos.

Written for the first time: Prince Yuri of Galich یوری and Dimitri Shemyaka
دیمتری شیمیاکا, and Lake Chudskoe چودسکویے, none of which had a form
anywhere. Nothing in these five lives quotes Holy Scripture.

## Batch 237: five Hilarions

Hilarion of Gdov appears twice on the site, here and in batch 236, with
different English; both are written, and the name, the river, the dedication
and the date agree between them, since they are one man. Hilarion is ہلاریون
throughout, as batch 236 settled.

Standing forms reused: تاباتھا, مایوما, پافوس, ہیسیکیس, ڈلمیشیا, پیلیکیتے,
پروسا, لیو ارمنی, تھیوفیلوس, دلماتوس, راست دینی کی فتح, یاروسلاو,
شریعت اور فضل کا وعظ, اوموفوریون, دنیپر, ژیلچا, لیوونی, حفاظت. The
Metropolitan is میٹروپولیٹن and a schemamonk اسکیما راہب, both the site's own.

Written for the first time: Constantine Copronymus قسطنطین کوپرونیمس and the
princely village of Berestovo بیریستووو, neither of which had a form. The
emperor Michael is میخائل, as batch 231 wrote the tsar.

Hilarion the Great's saying that the grace of God is not for sale is a saying
in a life and is written as prose. Nothing in these five lives quotes Holy
Scripture.

## Lane C, ninth batch: Sophia of Suzdal, three Sisoeses, three Simeons, two Silvanuses

Hell is **دوزخ**, the word the lives use of the place of fire; پاتال is Hades,
where the Forerunner preached, and is not put in its place. Silouan's word is
written as prose without quotation marks, as this file writes every saying:
اپنا ذہن دوزخ میں رکھ اور نا امید نہ ہو.

Martha, the mother of Simeon of the Wonderful Mountain, is **مارتھا**, her own
commemoration's form, though the vocabulary's cross-reference in her son's
entry writes مرتھا. Simeon the New Theologian keeps the نیا عالم الٰہیات شمعون
his commemoration gives him, which is not the یوحنا عالمِ الٰہیات of the
Evangelist; the two titles stay apart here as the Theologian note requires.

Taken from the vocabulary: the Wonderful Mountain عجیب پہاڑ, Emesa ایمیسا,
Solomonia سولومونیا, Shovskoe شوفسکویے, Symeon the Studite the Pious, the
uncreated Light غیر مخلوق نور, and the Hymns of Divine Love.

Written for the first time: Saburova سابوروفا, Prince Kurbsky کورپسکی, and
Stephen of Nicomedia.

## Batch 238: two Ignatii, two Irenarchi, and Isaac of the Dalmatos monastery

Ignatius of Loma is opened **لوما اور یاروسلاول کے**, the city's settled
form, where his commemoration writes یاروسلاو. That form belongs to the
prince, settled at batch 225 and used again for Yaroslav the Wise in batch
237; the entry means the city on the Volga, and the site already writes it
یاروسلاول.

Standing forms reused: لوما, کونداکووو, پریلوکی, سفید جھیل, سیرل, تھیبائیڈ,
اسقیطس, پروسفورا, خدا بردار اگنیشیس, ایرینارکس, بورس اور گلیب, پوژارسکی,
مینن, کریملن, مصیبتوں کا زمانہ, سولوفکی, زوسیماس, سباتیس, والنس, آریوسی,
گوتھ, ادریانوپل, دوسری عالمی کونسل, دالماتس, دلماتی گھر.

Written for the first time: the Polish commander Sapieha ساپیہا, who had no
form; the Danes are ڈنمارک والے, named from their country as the site names
peoples it has no adjective for, beside the Swedes سویڈن which the lives
already carry.

The words of Irenarchus to Sapieha, and the canon's line to Ignatius of the
Caves, are a saying and a hymn line inside a life, and are written as prose,
without quotation marks, as this file writes both.
