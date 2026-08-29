# Armenian: the register, settled before the writing starts

The fourteenth language, and the second of the four ancient Eastern Churches
this index still owes a tongue. Written, not converted: the test is whether a
reader who grew up with Armenian in church would recognise it as something
written by someone who prays where he prays.

Armenian is the one language on this site where that sentence has to be
finished before anything else can be said, because the Armenian language and
the Eastern Orthodox Church do not arrive together.

## Whose Armenian this is

This site is Eastern Orthodox. The Armenian Apostolic Church is Oriental
Orthodox; the two are not in communion, and have not been since Chalcedon.
Its calendar is its own - the Nativity and the Theophany kept together on the
sixth of January, the Transfiguration movable and called Vardavar, its own
fasts, its own reckoning of Easter for centuries - and its saints and its
hierarchy are its own.

**This file is not the Armenian Church's synaxarion.** It is the Eastern
Orthodox synaxarion, in the Armenian language. The reader it is written for
is the Armenian-speaking Orthodox Christian: the faithful of the Ecumenical
Patriarchate and of the Patriarchates of Jerusalem and Antioch who read and
pray in Armenian, and the diaspora, who meet this calendar in an English or
a Greek that is not their mother tongue.

That reader is real and he is not well served anywhere. There is no large
printed corpus of Chalcedonian Armenian service books to read the register
off, as there is for Greek and Russian and as there is even for Georgian.
That absence is the whole difficulty of this language, and it is why the two
rules below are stated so flatly.

**Use the Armenian language and the whole of its Christian vocabulary.** It
is older than most of what this index describes; it has words for the desert
and the cave and the relic and the vigil that were in use when the saints of
the fourth century were alive. Nothing is gained by writing a thin Armenian
out of nervousness, and a reader would recognise the thinness at once.

**Do not carry over what asserts the other reckoning.** A proper noun, a
feast title or an honorific that belongs to the Armenian Church as a Church -
not to Armenian as a language - is not written here, because putting it in
this calendar would have this site say something it does not hold. The list
of what was and was not carried over is below, under *The judgement*, and it
is the substance of this language.

## What the site has already written in Armenian

    data/saint-names.v1.hy.json      1,528 commemorations
    data/calendar-names.v1.hy.json   1,640 calendar headings
    data/prayers-i18n.v2.hy.json     100 prayers
    data/glossary-i18n.v1.hy.json    177 ecclesiastical terms, defined
    data/rule-i18n.v5.hy.json        the fasting rule
    scripture/, data/bible.v4.hy.b64 Scripture

The first three are the precedent for this table, and where one of them has
decided a word, that word stands and is not re-decided here. The saints' names
table is the important one: it is an Armenian Orthodox synaxarion index of
fifteen hundred entries, every rank word below is read out of it rather than
proposed, and the vocabulary written here stands beside it on the same card.

## Orthography: classical, and the site is not of one mind

Armenian has two orthographies. The **classical** or Mesropian spelling
(դասական, Մեսրոպեան ուղղագրութիւն) is what the Church has always printed and
what the whole diaspora writes. The **reformed** spelling is the Soviet
revision of 1922 and 1940, in use in the Republic of Armenia.

**Classical throughout.** Two reasons, and the second is the stronger:

  - The readers this file is written for - Constantinople, Jerusalem, Antioch,
    the diaspora - write classical, and the Church prints classical even in
    Armenia.
  - The site already does. The two name tables and the hundred prayers, which
    is three thousand two hundred commemorations and the largest body of
    continuous Armenian prose here, are classical throughout: եւ against և by
    a thousand to seven, -ութիւն without a single -ություն beside it.

The site is not consistent about this and it should be said plainly rather
than discovered later. `data/ui-i18n.v5.hy.json` and the hundred and nineteen
calendar entries already in `data/saint-info.v1.hy.json` are in the reformed
spelling, and `data/rule-i18n.v5.hy.json` is mixed. This table does not follow
them. It follows the names it stands beside, and the divergence is a defect in
those files rather than a fork here.

What classical means, in the four places it shows:

| | classical | reformed |
|---|---|---|
| the diphthong | եւ, աւ | և, ո |
| the abstract ending | -ութիւն | -ություն |
| initial and medial յ | Յովհաննէս, Յարութիւն | Հովհաննես, Հարություն |
| է in the root | մարգարէ, Տէր, երէց | մարգարե, Տեր, երեց |

So: Աստուածածին and not Աստվածածին, սարկաւագ and not սարկավագ, սիւնակեաց
and not սյունակյաց, եօթանասուն and not յոթանասուն, Յիսուս and not Հիսուս.
**The ligature և is not written at all**; it is եւ, in every position.

### The grammar behind the spelling

Classical orthography is not classical Armenian. Grabar is the language of the
Liturgy and of the prayers this site publishes, and it is not the language of a
card of vocabulary; a reader would meet it as an inscription rather than as
something addressed to him.

What the names table writes, and what is written here, is **modern Eastern
Armenian in the classical spelling** - the combination the Church and the
publishers of the diaspora have used for a century. Eastern morphology: նրա and
not իր for the third person, the locative in -ում (Նովգորոդում, Գալիայում),
եղողները and չարչարուեցին. Classical spelling over the top of it, and the
classical genitive in -ոյ where the name asks for it.

The prayers are the exception and stay as they are. They are grabar because the
Church prays in grabar, and a line quoted from them is quoted, not re-rendered.

## Script and punctuation

The Armenian alphabet, and nothing else. No transliteration, no Latin letters
inside an Armenian word, no Greek or Cyrillic characters carried in from the
language a name came from.

Armenian sets its own points, and the site's Armenian prayers already do:

  - **։** the verjaket, which is the full stop. Not the ASCII period.
  - **,** the comma, which is the ASCII comma, as Armenian writes it.
  - **՝** the but, which sets off an apposition where English would use a
    comma or a dash. Used sparingly and only where the phrase asks for it.
  - **«»** the quotation marks, which are what the names table already uses
    for the titles of icons.

The emphasis marks - ՛ the shesht, ՜ the yerkarabanakan, ՞ the hartsakan -
belong to speech and to prayer, not to a card of vocabulary, and are not
written here. The prayers carry them properly and are the place to see them.

**Mirror the English punctuation.** The icon and relic lines are full
sentences in the English and end with a stop, so they end with ։. The place
names, the patronages and the titles are noun phrases and carry no stop, so
they carry none. Hyphens, never dashes; straight quotes, never the
typographic ones; European digits, as the rest of the site.

## Register: the honorific is the rank

Armenian, like Greek and Georgian and Romanian, lets the plain honorific stand
before a name. **սուրբ Նիկողայոս** is right, and the names table prints սուրբ
before a bare name some four hundred and eighty times. So `strict` stays False
and only the monastic distinction is asserted.

**A monastic is երանելի, not merely սուրբ.** This is the distinction English
does not make at all and the one most often lost. երանելի is what the names
table gives Ὅσιος and преподобный three hundred and thirty-eight times:
երանելի Եւթիմիոս, երանելի Սերգիոս, Անտիոքի ճգնաւոր երանելի Զենոն.

երանելի also renders *Blessed* - of the fools-for-Christ and of the
right-believing princes - and Armenian does not separate the two by the
honorific. It separates them by the rank noun that follows, which is how the
names table already writes them: **Երանելի Նիկողայոս, Քրիստոսի յիմար**,
**Երանելի Դովմոնտ, Փսկովի իշխան**. The rank does the work; the honorific is
the same word.

### The ranks

Read out of the names table and the glossary. The honorific is drawn from this
list rather than flattened into սուրբ.

| | |
|---|---|
| saint | սուրբ |
| monastic, venerable | երանելի |
| blessed | երանելի |
| righteous | արդար |
| martyr | նահատակ |
| martyrs | նահատակներ |
| woman martyr | վկայուհի |
| great-martyr | մեծ նահատակ |
| hieromartyr | քահանայ-նահատակ |
| venerable-martyr, monk-martyr | վանական նահատակ |
| virgin-martyr | կոյս վկայուհի |
| protomartyr | նախավկայ |
| new martyr | նոր նահատակ |
| passion-bearer | չարչարակիր |
| confessor | խոստովանող |
| apostle | առաքեալ |
| of the Seventy | եօթանասունից |
| equal-to-the-apostles | առաքելակից |
| prophet | մարգարէ |
| forerunner | կարապետ |
| evangelist | աւետարանիչ |
| hierarch (as a body) | սրբապետ |
| bishop | եպիսկոպոս |
| archbishop | արքեպիսկոպոս |
| metropolitan | մետրոպոլիտ |
| patriarch | պատրիարք |
| pope of Rome | Հռոմի պապ |
| priest | քահանայ |
| presbyter | երէց |
| archpriest | աւագ քահանայ |
| deacon | սարկաւագ |
| archdeacon | սարկաւագապետ |
| subdeacon | կիսասարկաւագ |
| reader | ընթերցող |
| abbot, igumen | վանահայր |
| abbess | վանամայր |
| archimandrite | արքիմանդրիտ |
| hieromonk | վանական քահանայ |
| hierodeacon | վանական սարկաւագ |
| monk | վանական |
| nun | միանձնուհի |
| novice | նորընծայ |
| elder | ծերունի |
| schemamonk | սքեմաւոր |
| great schema | մեծ սքեմ |
| ascetic, hermit | ճգնաւոր |
| anchorite | անապատական |
| recluse | մենակեաց |
| stylite | սիւնակեաց |
| fool-for-Christ | վասն Քրիստոսի յիմար |
| unmercenary | անարծաթ |
| wonderworker | սքանչելագործ |
| enlightener | լուսաւորիչ |
| myrrh-bearer | իւղաբեր |
| myrrh-streaming | իւղահոս |
| hymnographer | շարականագիր |
| iconographer | սրբանկարիչ |
| virgin | կոյս |
| teacher, doctor of the Church | վարդապետ |
| king | թագաւոր |
| queen | թագուհի |
| emperor | կայսր |
| empress | կայսրուհի |
| prince | իշխան |
| princess | իշխանուհի |
| grand prince | մեծ իշխան |
| right-believing | ուղղահաւատ |
| pious (of a sovereign) | բարեպաշտ |

## The judgement: what was carried over and what was not

This is the part of the register that only Armenian has, and it is written out
rather than left to be inferred phrase by phrase.

**Carried over without hesitation - the language, which belongs to nobody.**
սուրբ, Աստուածածին, Ամենասուրբ, Տէր, Յիսուս Քրիստոս, Սուրբ Հոգի,
Երրորդութիւն, եկեղեցի, վանք, տաճար, մասունք, սրբապատկեր, խաչ, աղօթք,
պահք, ճգնաւոր, անապատ, քարայր, նահատակ, առաքեալ, մարգարէ, եպիսկոպոս,
սարկաւագ, քահանայ, վանահայր, լուսաւորիչ, սքանչելագործ. These are the
Christian vocabulary of a Christian language and no Church owns them.

**Carried over: the saints and places the two Churches hold in common.**
Everything before Chalcedon is shared, and its Armenian forms are received
forms that this site would embarrass itself by re-transliterating from
English. Հռիփսիմէ and Գայիանէ, whom the Orthodox calendar keeps on the
thirtieth of September; Գրիգոր Լուսաւորիչ; Էջմիածին and Վաղարշապատ, where
their churches stand; Տրդատ the king; Հայաստան and Արարատ and Մելիտենէ.
These are written as Armenian writes them.

**Not carried over: the feast titles that carry the other reckoning.**
The Transfiguration is **Պայծառակերպութիւն** and never **Վարդավառ**: Vardavar
is the Armenian Church's own name for its own movable feast, and it is not the
sixth of August. The Theophany is **Աստուածայայտնութիւն** and stands alone,
not joined to the Nativity as **Ծնունդ եւ Աստուածայայտնութիւն**, which is the
sixth of January in that Church and two separate feasts in this calendar.
The Exaltation is written descriptively, as the names table already writes it -
**Պատուական Խաչի Վերացում** - and not as **Խաչվերաց**, that Church's movable
September feast. The word in each pair is Armenian; the title is a calendar,
and the calendar here is the Orthodox one.

**Not carried over: the honorifics of the other hierarchy.** **Վեհափառ
Հայրապետ** and **Կաթողիկոս** name the head of the Armenian Church and are not
written of anyone. **Սրբազան** is that Church's address for its bishops and is
not used as a title here; a bishop is **եպիսկոպոս** and the Three Hierarchs
are **երեք սուրբ սրբապետներ**, which is what the names table prints.
**Հայրապետ** is avoided as a rank for the same reason, though it is a good
Armenian word: in Armenian usage it names the Catholicos.

**Not carried over, and this one diverges from the names table:
վարդապետ is not the archimandrite.** The table renders *Archimandrite*
վարդապետ six times. Vardapet is a distinct order in the Armenian Church, with
its own degrees and its own staff, and it is not the Orthodox archimandrite;
writing it here would place a Russian abbot in an Armenian hierarchy. The
archimandrite is **արքիմանդրիտ**, which is what the site's own glossary
defines. **վարդապետ** keeps its other and older sense, the teacher and doctor
of the Church, which is how the same table uses it of the Three Hierarchs -
տիեզերական վարդապետներ, the ecumenical teachers - and that use stands.

**Two smaller departures from the names table, and the reasons.**
*Abbess* is **վանամայր** rather than the loan աբբայուհի, because վանահայր and
վանամայր are the received Armenian pair and the loan reads as a loan.
*Martyr* is **նահատակ** throughout, the table's own word by three hundred to
thirteen; **վկայ** is kept for the settled compounds the Church has fixed -
**նախավկայ** for the protomartyr and **վկայուհի** for a woman martyr, as in
**կոյս վկայուհի** - and is not used as a free variant of նահատակ.

**Coined here, because Armenian has no received rank for it.**
*Passion-bearer* is **չարչարակիր**, built on չարչարանք, the word for the
Passion and for suffering that the names table already uses, on the pattern of
իւղաբեր. Boris and Gleb are Slavic saints and the Armenian books have no word
waiting for them. This is named as a coinage so that no one later mistakes it
for something received.

## Word order

Armenian builds the noun phrase head-last. The see, the town or the monastery
comes first, in the genitive, where English trails it behind in a prepositional
phrase. The names table already does this fifteen hundred times:

    Archbishop of Caesarea in Cappadocia, Saint Basil the Great
      Կապադովկիոյ Կեսարիոյ արքեպիսկոպոս սուրբ Բարսեղ Մեծ

    Venerable Martinian, Abbot of Belozersk
      Բելոզերսկի վանահայր երանելի Մարտինիան

    Venerable Isaac the Recluse of the Kyiv Near Caves
      Կիեւի Մերձաւոր քարայրների մենակեաց երանելի Իսահակ

An entry that keeps the English order - the rank, then an Armenian rendering
of "of X" trailing after it - is legible and is immediately foreign, which is
the defect this register exists to prevent.

Where the epithet is a settled one-word ethnicon, it follows the name instead,
with the suffix **-ցի** for a town and **-ացի** for a land or a people:
**Մաքսիմոս Տոտմացի**, **Յովհաննէս Դամասկացի**, **Եփրեմ Ասորի**,
**Մարիամ Եգիպտացի**.

The genitive is the classical one. Place names in **-իա** take **-ոյ** -
Աղեքսանդրիոյ, Սիրիոյ, Կիլիկիոյ, Կապադովկիոյ, Բրիտանիոյ, Սերբիոյ, Ռուսիոյ -
and the rest take **-ի**: Կիեւի, Անտիոքի, Հռոմի, Նովգորոդի, Մոսկուայի.

## Names

Armenian has its own received forms for the saints of the first millennium and
does not transliterate them from English. **Յովհաննէս**, **Պետրոս**,
**Պօղոս**, **Անդրէաս**, **Մատթէոս**, **Մարկոս**, **Ղուկաս**, **Յակոբոս**,
**Ստեփանոս**, **Սիմէոն**, **Եղիա**, **Մովսէս**, **Դաւիթ**, **Մարիամ**.
The Greek fathers keep the Greek shape in Armenian dress: **Բարսեղ** for
Basil, **Գրիգոր**, **Աթանաս**, **Նիկողայոս**, **Կիւրեղ** for Cyril,
**Գէորգ**, **Անտոնիոս**, **Եփրեմ**, **Մակար**, **Արսէն**, **Սաբա**,
**Եւթիմիոս**, and **Յովհաննէս Ոսկեբերան** for Chrysostom, which is the
Armenian of the Golden Mouth and not a rendering of the Greek word.

Names with no received Armenian form - the Slavic, the Romanian, the Celtic,
and the new martyrs of the last century - are written on the sound of the
language they come from and not on the English spelling of it: Սերգիոս,
Վլադիմիր, Օլգա, Սերաֆիմ, Տիխոն. A Russian name is not routed through English
on its way into Armenian. The names table has already settled several hundred
of these and its spelling is the precedent.

## The words the site has already settled

| | |
|---|---|
| Theotokos, Mother of God | Աստուածածին |
| Most Holy | Ամենասուրբ |
| Ever-Virgin | Մշտակոյս |
| the Divine Liturgy | Սուրբ Պատարագ |
| relics | մասունքներ |
| translation of the relics | մասունքների փոխադրում |
| uncovering of the relics | մասունքների գիւտ |
| repose | հանգիստ |
| commemoration | յիշատակ |
| synaxis | ժողով |
| council | ժողով |
| feast | տօն |
| forefeast | նախատօն |
| leavetaking | տօնի արձակում |
| icon | սրբապատկեր |
| cross | խաչ |
| church | եկեղեցի |
| cathedral, temple | տաճար |
| monastery | վանք |
| hermitage, skete | մենաստան |
| caves | քարայրներ |
| desert, wilderness | անապատ |
| mountain | լեառն, gen. լերան |
| fast | պահք |
| Great Lent | Մեծ Պահք |
| Pascha | Զատիկ |
| Nativity | Ծնունդ |
| Theophany | Աստուածայայտնութիւն |
| Meeting of the Lord | Տեառնընդառաջ |
| Annunciation | Աւետում |
| Transfiguration | Պայծառակերպութիւն |
| Dormition | Վերափոխում |
| Exaltation of the Cross | Խաչի Վերացում |
| glorification | սրբադասում |
| incorrupt | անապական |
| spiritual father | հոգեւոր հայր |
| in baptism | մկրտութեամբ |
| tonsured | կրօնաւորեալ |
| Armenia | Հայաստան |

**Վերափոխում** is the one on this list that had to be argued. It is the
Armenian Church's name for the fifteenth of August and it renders *Assumption*
more nearly than *Dormition*; the exact Armenian of κοίμησις would be
**ննջումն**. It is kept, for three reasons: it asserts nothing that Chalcedon
divides, since the two Churches keep the same feast on the same day and teach
the same thing about it; it is the only word an Armenian reader has ever met
for that feast, and ննջումն in its place would be a coinage in the one line
where a coinage helps nobody; and the site's own names table already prints
it. Where the English says *falling asleep* of an ordinary saint rather than
of the Mother of God, the word is **ննջում** or **հանգիստ**, which is what the
names table gives *Repose* thirty times.

The glossary is the place to look before coining anything: a hundred and
seventy-seven ecclesiastical terms are already defined in Armenian there, from
Ակաթիստ to Տիպիկոն. It is written in the reformed spelling, so a word taken
from it is re-spelled classically on the way in - Մկրտություն becomes
մկրտութիւն - but the word itself stands, and one invented here that
contradicts one defined there is a defect in the site and not a variant.

## What a script can catch

`tools/check_register.py --lang hy` asserts the monastic rule and nothing else.
Its spec is scaffolded from the finished vocabulary - `--scaffold --lang hy`
reads the terms table and derives the rank patterns from the rank words it
already renders - and then two things are settled by hand, because no table
holds them:

  - **generic**, the bare word for holy: `սուրբ`, with the abbreviation `Ս.`
    allowed beside it, since Armenian books print both.
  - **strict**, which is **False**: Armenian lets that word stand before a bare
    name, so սուրբ before a name proves nothing either way.

`tools/loop.py` catches the rest before the file is touched: a character
outside the Armenian block, a combining mark, a Latin letter jammed against an
Armenian one, a block count that does not match the batch.

Neither of them catches the reformed spelling, which is the thing most likely
to drift in over ten thousand lines. The guard against that is the four rows
of the orthography table above, checked by eye against any line carrying
-ություն, և, Հով- or a bare -ե- where -է- belongs.

## The fields, and what each one is

Knowing which field a phrase came from settles most of the questions about how
to render it.

| field | count | what it is | how Armenian takes it |
|---|---|---|---|
| patronCauses | 2,622 | what is asked of him | a noun phrase, no stop: հիւանդներ եւ աղքատներ |
| patronWork | 1,572 | whom he is asked for | likewise |
| related | 1,476 | the kindred commemoration | a name and its apposition |
| icon | 1,407 | how he is written in an icon | a full sentence, closed with ։ |
| titles | 980 | how else the saint is named | Եփեսոսի եպիսկոպոս, խոստովանող |
| relics | 749 | where the relics rest | as the English is, sentence or phrase |
| place, origin, region, country | 1,207 | town, then the land it stood in | received form, comma as in the English |
| patronPlaces | 537 | the town a saint is patron of | the bare place name |
| rank, state, type | 208 | his order and his standing | a noun phrase |
| canonizedBy | 145 | who glorified him and when | a clause |
| baptismalName | 101 | the name before tonsure | the Armenian form of the name |
| era | 27 | the century | չորրորդ դար |

The two largest are the intercessions, and they are English of a deliberately
heightened kind - *those who bury the forgotten dead*, *the truth spoken to
emperors*. Armenian takes them as noun phrases and reaches for the participle
before the relative clause: **մոռացուածները թաղողները** rather than a որ-clause
that would double the length of every one of fourteen hundred lines and read
like a translation, which it would be.

## The order of work

Vocabulary, then the grammar drawn from it, then the lives, then the calendar
entries:

    python3 tools/loop.py terms hy --start Armenian
    python3 tools/loop.py terms hy --next 40
    python3 tools/check_register.py --scaffold --lang hy
    python3 tools/loop.py lives hy --next 6
    python3 tools/loop.py info hy --next 10

The scaffold refuses a language whose terms table does not exist, which is that
order enforced rather than remembered. See `docs/LOOP.md`.

The hundred and nineteen calendar entries already in
`data/saint-info.v1.hy.json` are in the reformed spelling and were written
before this register existed. They are not repaired here; the terms lane does
not own that file. It is written down so that whoever takes the calendar
entries knows what he will find.

## The trap

Deciding, phrase by phrase, whether an entry is an atom or a compound or a
title is a judgement per phrase, and a judgement per phrase is a stop per
phrase. `tools/saint_terms/hy.py` is written entirely as `TEXT`; `PARTS` and
`expand()` are optional and the builder calls `expand()` only if it exists.
Write all 10,632 out plainly and factor later or never.
