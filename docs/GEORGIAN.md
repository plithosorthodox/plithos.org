# Georgian: the register, settled before the writing starts

The eleventh language, and the first of the four ancient Eastern Churches this
index still owes a tongue. Written, not converted: the test is whether a reader
who grew up in the Church of Georgia would recognise it as something written by
someone from his own Church.

Georgia is not a mission field being described from outside. It is an
autocephalous patriarchate older than most of the sees this calendar names, with
its own alphabet, its own hymnography, and its own saints - Nino, Shushanik,
Abo, Shio, David of Gareji, the martyrs of Kvabtakhevi - a good number of whom
are already in this index and none of whom has ever stood here in his own
language. That is the whole reason Georgian is taken first of what is left.

## The site has already written a great deal of Georgian

This is the fact that settles most of the register, and it settles it the way
CLAUDE.md says a register is settled: by reading off what the Church already
prints, not by deciding afresh.

    data/saint-names.v1.ka.json      1,528 commemorations, in Georgian
    data/glossary-i18n.v1.ka.json    the ecclesiastical vocabulary, defined
    data/prayers-i18n.v2.ka.json     100 prayers
    data/rule-i18n.v5.ka.json        the fasting rule
    scripture/ka/                    the Old Testament

Where one of those has decided a word, that word stands and is not re-decided
here. The saints' names table is the important one: it is a Georgian synaxarion
index of fifteen hundred entries, and every rank word below is read out of it
rather than proposed.

## Script and spelling

**Mkhedruli**, the ordinary Georgian alphabet, and nothing else:

    ა ბ გ დ ე ვ ზ თ ი კ ლ მ ნ ო პ ჟ რ ს ტ უ ფ ქ ღ ყ შ ჩ ც ძ წ ჭ ხ ჯ ჰ

**No Asomtavruli** (Ⴀ Ⴁ Ⴂ) and **no Nuskhuri** (ⴀ ⴁ ⴂ). Both are real Georgian
scripts and both are wrong here: they belong to manuscript facsimiles and to the
capitals of an inscription, not to running prose, and a reader meets them as
decoration. **No Mtavruli** either - the all-caps set at U+1C90 - because
nothing in this index is set in capitals.

Georgian has no upper case. A sentence begins with the same letter shape it
would carry in the middle, and a name is not capitalised. Nothing here is to be
"capitalised" by borrowing another alphabet's capitals.

The archaic letters ჱ ჲ ჳ ჴ ჵ are not written. They are in the Unicode block and
in the older editions; modern Georgian, including what the Patriarchate prints,
does without them, and the one place they may stand is inside a received name
that the Church still spells that way.

Hyphens, never dashes. Straight quotes, never the typographic ones. Numerals are
the European digits the rest of the site uses.

## Register

Georgian, like Greek and Romanian and Serbian, allows the plain honorific before
a name. **წმინდა გიორგი** is right and **წმინდა ნინო** is right, and the saints'
names table prints them that way four hundred and eighty-five times. So `strict`
stays False and only the monastic distinction is asserted.

**A monastic is ღირსი, never merely წმინდა.** This is the one distinction
English does not make at all and the one most often lost. ღირსი is Georgian for
Ὅσιος and преподобный: ღირს ევთიმე, ღირს საბატი, ღირსი შიო.

### The truncation, which is the thing a writer gets wrong

Georgian attributive adjectives ending in **-ი** drop that **-ი** before the
noun they qualify. So the monastic honorific is **ღირს** when it stands
immediately before the saint's name and **ღირსი** when it does not:

    ღირს ევთიმე              venerable Euthymius
    ღირს მარტინიანე          venerable Martinian
    ღირსი შიოს ...           of venerable Shio (a genitive follows)
    ღირსი                    standing alone, as a label

The names table has ღირს three hundred and seventy-seven times and ღირსი twelve,
which is that rule and not a preference. The same truncation governs
**მართალი / მართალ**, **ნეტარი / ნეტარ**, **წმინდანი / წმინდან**. It does not
touch **წმინდა**, which ends in **-ა** and never changes, nor **მოწამე**,
**დიდმოწამე**, **მღვდელმოწამე**, **მოციქული** or the other ranks that are nouns
in apposition rather than adjectives.

### The ranks

Read out of the saints' names table and the glossary. The honorific is drawn
from this list rather than flattened into წმინდა:

| | |
|---|---|
| monastic | ღირსი, ღირს |
| hierarch (as a body) | მღვდელმთავარი |
| bishop | ეპისკოპოსი |
| archbishop | მთავარეპისკოპოსი |
| metropolitan | მიტროპოლიტი |
| patriarch | პატრიარქი |
| pope of Rome | რომის პაპი |
| martyr | მოწამე |
| martyrs | მოწამენი |
| great-martyr | დიდმოწამე |
| hieromartyr | მღვდელმოწამე |
| venerable-martyr | ღირსმოწამე |
| new martyr | ახალმოწამე |
| protomartyr | პირველმოწამე |
| passion-bearer | ვნებათმძლე |
| confessor | აღმსარებელი |
| righteous | მართალი |
| blessed | ნეტარი |
| right-believing | კეთილმორწმუნე |
| pious (of a sovereign) | კეთილმსახური |
| apostle | მოციქული |
| of the Seventy | სამოცდაათთაგანი |
| equal-to-the-apostles | მოციქულთა სწორი |
| prophet | წინასწარმეტყველი |
| enlightener | განმანათლებელი |
| wonderworker | სასწაულმოქმედი |
| fool-for-Christ | ქრისტესთვის სული, სულელი |
| unmercenary | უვერცხლო |
| stylite | სვეტმდგომი |
| recluse | დაყუდებული |
| anchorite | განდეგილი |
| abbot, igumen | წინამძღვარი |
| archimandrite | არქიმანდრიტი |
| hieromonk | მღვდელმონაზონი |
| hierodeacon | იერდიაკონი |
| monk | მონაზონი |
| nun | მონაზონი, მოღვაწე დედა |
| elder | ბერი |
| schemamonk | სქემოსანი |
| virgin | ქალწული |
| deacon | დიაკვანი, დიაკონი |
| presbyter, priest | ხუცესი, მღვდელი |
| king | მეფე |
| queen, empress | დედოფალი |
| prince | მთავარი |
| grand prince | დიდი მთავარი |

**ხუცესი** is worth its own line. It is the old Georgian word for a presbyter,
it is what the names table prints - იულიანე ხუცესი, კინდეოს ხუცესი - and it is
not to be replaced with a transliterated პრესვიტერი. Where the English says
*priest* of a parish clergyman rather than of the order, **მღვდელი** is the
ordinary word.

**კეთილმორწმუნე** is the honorific of a believing king or prince, and it is what
the table already prints for every one of them. **კეთილმსახური** is the word the
Georgian books give a *pious* sovereign, and it stands where the English says
pious rather than right-believing. Neither is decided per phrase: the English
word decides it.

## Word order

Georgian builds the noun phrase head-last, and the see or the town comes first,
in the genitive, where English puts it last in a prepositional phrase:

    Archbishop of Antioch, Saint Eustathius
      ანტიოქიის მთავარეპისკოპოსი წმინდა ევსტათი

    Venerable Martinian, Abbot of Belozersk
      ბელოზერსკის წინამძღვარ ღირს მარტინიანე

    Venerable Onesiphorus the Confessor of the Kyiv Near Caves
      კიევის ახლო გამოქვაბულების აღმსარებელი ღირს ონისიფორე

This is not stylistic. An entry that keeps the English order - the rank, then a
Georgian rendering of "of X" trailing behind it - is legible and is immediately
foreign, which is the whole defect this register exists to prevent. Where the
epithet is a settled one-word ethnicon the language already has, that is used
instead and it follows the name: **გიორგი ხოზებელი**, **კვიპრიანე
კართაგენელი**, **გრიგოლ ღვთისმეტყველი**. The suffix is **-ელი** (**-ული**,
**-ური** for a people or a rite).

## Names

Georgian has its own received forms for the saints of the first millennium and
does not transliterate them from English. **იოანე** and not ჯონი, **პეტრე**,
**პავლე**, **ანდრია**, **მათე**, **მარკოზი**, **ლუკა**, **სვიმეონი**,
**იაკობი**, **ილია**, **მოსე**, **დავითი**. The Greek fathers keep the Greek
shape in Georgian dress: **ბასილი**, **გრიგოლი**, **ათანასე**, **ნიკოლოზი**,
**დიმიტრი**, **გიორგი**, **ანტონი**, **ეფრემი**, **მაკარი**, **არსენი**,
**საბა**, **ევთიმე**, **იოანე ოქროპირი** for Chrysostom.

The Georgian saints have received forms that are not to be re-rendered from the
English spelling at all:

    ნინო            Nino, equal-to-the-apostles, enlightener of Georgia
    გიორგი          George
    შუშანიკი        Shushanik
    აბო თბილელი     Abo of Tbilisi
    შიო მღვიმელი    Shio of the Caves
    დავით გარეჯელი  David of Gareji
    იოანე ზედაზნელი John of Zedazeni
    გრიგოლ ხანძთელი Gregory of Khandzta
    ევსტათი მცხეთელი Eustathius of Mtskheta
    თამარ           Tamar
    დავით აღმაშენებელი  David the Builder
    ქეთევან         Ketevan
    ილია მართალი    Elijah the Righteous (Chavchavadze)
    გაბრიელი        Gabriel

These are the names a Georgian reader will check first, and they are the ones an
English-sounding transliteration would embarrass the site with.

Names with no received Georgian form - the Slavic, Romanian and Celtic saints,
and the new martyrs of the last century - are written on the sound of the
language they come from, not on the English spelling of it: სერგი, ვლადიმირი,
ოლგა, სტეფანე. A Russian name is not routed through English on its way into
Georgian. The names table has already done several hundred of these, and its
spelling is the precedent.

## The words the site has already settled

| | |
|---|---|
| Theotokos, Mother of God | ღვთისმშობელი |
| Most Holy | ყოვლადწმინდა |
| Ever-Virgin | მარადის ქალწული |
| the Divine Liturgy | საღმრთო ლიტურგია |
| relics | ნაწილები |
| translation of the relics | ნაწილების გადასვენება |
| uncovering of the relics | ნაწილების პოვნა |
| repose | მიცვალება |
| synaxis | კრება |
| feast | დღესასწაული |
| forefeast | წინადღესასწაული |
| leavetaking | დღესასწაულის დასრულება |
| commemoration | ხსენება |
| icon | ხატი |
| cross | ჯვარი |
| monastery | მონასტერი |
| caves | გამოქვაბულები |
| desert, wilderness | უდაბნო |
| fast | მარხვა |
| Great Lent | დიდი მარხვა |
| Pascha | აღდგომა |
| glorification | წმიდანად შერაცხვა |
| incorrupt | უხრწნელი |
| spiritual father | სულიერი მამა |
| in baptism | ნათლისღებაში, ნათლობით |
| tonsured | აღკვეცილი |
| Georgia | საქართველო |

The glossary is the place to look before coining anything: it holds a hundred
and eighty ecclesiastical terms already defined in Georgian, from აკათისტო to
ტიპიკონი, and a word invented here that contradicts one defined there is a
defect in the site and not a variant.

## What a script can catch

`tools/check_register.py --lang ka` asserts the monastic rule and nothing else.
Its spec is scaffolded from the finished vocabulary -
`--scaffold --lang ka` reads the terms table and derives the rank patterns from
the rank words it already renders - and then two things are settled by hand,
because no table holds them:

  - **generic**, the bare word for holy: `წმინდა`, with `წმიდა` allowed beside
    it, since both spellings are printed in Georgian books.
  - **strict**, which is **False**: Georgian lets that word stand before a bare
    name, so the presence of წმინდა before a name proves nothing either way.

`tools/loop.py` catches the rest before the file is touched: a character outside
the Georgian block, a combining mark, a Latin letter jammed against a Georgian
one, a block count that does not match the batch.

## The fields, and what each one is

Knowing which field a phrase came from settles most of the questions about how
to render it.

| field | count | what it is | how Georgian takes it |
|---|---|---|---|
| patronCauses | 2,622 | what is asked of him | a noun phrase, lower case: ავადმყოფნი და გლახაკნი |
| patronWork | 1,572 | whom he is asked for | likewise |
| related | 1,476 | the kindred commemoration | a name and its apposition |
| icon | 1,407 | how he is written in an icon | a full descriptive sentence |
| titles | 980 | how else the saint is named | ეფესოს ეპისკოპოსი, აღმსარებელი |
| relics | 749 | where the relics rest | a full sentence, as the English is |
| place, origin, region, country | 1,207 | town, then the land it stood in | received form, comma as in the English |
| patronPlaces | 537 | the town a saint is patron of | the bare place name |
| rank, state, type | 208 | his order and his standing | a noun phrase |
| canonizedBy | 145 | who glorified him and when | a clause |
| baptismalName | 101 | the name before tonsure | the Georgian form of the name |
| era | 27 | the century | მეოთხე საუკუნე |

The two largest are the intercessions, and they are English of a deliberately
heightened kind - *those who bury the forgotten dead*, *the truth spoken to
emperors*. Georgian takes them as noun phrases and uses the participle rather
than a relative clause wherever it can: turning fourteen hundred participial
strings into subordinate clauses would double the length of every one of them
and read like a translation, which it would be.

## The order of work

Vocabulary, then the grammar drawn from it, then the lives, then the calendar
entries:

    python3 tools/loop.py terms ka --start Georgian
    python3 tools/loop.py terms ka --next 40
    python3 tools/check_register.py --scaffold --lang ka
    python3 tools/loop.py lives ka --next 6
    python3 tools/loop.py info ka --next 10

The scaffold refuses a language whose terms table does not exist, which is that
order enforced rather than remembered. See `docs/LOOP.md`.

## The trap

Deciding, phrase by phrase, whether an entry is an atom or a compound or a title
is a judgement per phrase, and a judgement per phrase is a stop per phrase.
`tools/saint_terms/ka.py` is written entirely as `TEXT`; `PARTS` and `expand()`
are optional and the builder calls `expand()` only if it exists. Write all
10,632 out plainly and factor later or never.
