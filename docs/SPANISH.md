# Spanish: the register, settled before the writing starts

Spanish comes to the Saints page with its lives already written - 1,456 of
them, 414,138 words - and without its vocabulary and its calendar entries.
That is the reverse of the order every language before it took, and it is a
gift rather than a difficulty: the register is not a thing to be decided
here, it is a thing to be *read off* what is already standing. Where this
file states a rule, the rule was taken from `tools/saint_lives/es.py` and
can be checked there.

## What Spanish is not

The danger is not the one German faced, and it is not the one Ukrainian
faced. Spanish has no neighbouring alphabet to drift into, and its Western
church vocabulary is not borrowed - it is the language's own, formed over
fifteen centuries of Latin Christianity in the peninsula and in America. A
Spanish reader has *beato*, *santo patrón*, *Asunción*, *Misa*, *Cuaresma*
and *estampa* ready for every word, and each of them carries a Church behind
it that is not this one.

- **Dormición**, never *Asunción*. The Assumption is a Roman dogma of 1950
  and a different claim; the Dormition is a falling asleep.
- **Divina Liturgia**, never *Misa*.
- **Padre de la Iglesia**, never *Doctor de la Iglesia*. The Doctors are a
  Roman category with a list, and the Fathers are not on it.
- **Icono**, masculine, never *estampa* and never *imagen* where the icon is
  meant as such. The Spanish-speaking Orthodox say *el icono*; *la icona* is
  an Italianism.
- **Theotokos** where the title is the Council's word, and **Madre de Dios**
  where the language would simply say it. *Virgen María* alone is the
  devotional register of another Church and does not stand as an honorific
  here.
- **Venerable** for the monastic, never *beato*. *Beato* renders the Roman
  *beatus*, a degree one step below canonisation. In Orthodox Spanish
  **bienaventurado** is the word for the fools for Christ and for the
  blessed departed, and it is a description, not a rank in a process.
- **Ayuno** and the named fasts - *la Gran Cuaresma*, *el ayuno de los
  Apóstoles*, *el ayuno de la Dormición*, *el ayuno de la Natividad*. The
  bare word *Cuaresma* means the Great Fast only.
- **Reliquias**, never *restos*. **Traslación** for the translation of
  relics and **hallazgo** for their uncovering, which are the two distinct
  feasts the calendar keeps and which *invención* blurs.
- **Presbítero** or **sacerdote**, never *párroco*, which is an office in a
  parish register, and never *pastor*.
- **Monasterio** and **lavra**; a *convento* is a house of a Western order.

Where Spanish-speaking Orthodoxy has settled a word - the jurisdictions in
Spain and in Mexico, Argentina, Chile and the United States all publish -
that word is used. This is not a field where the site invents.

## The honorific

Spanish belongs with Greek, Romanian and German and not with Russian: *san
Nicolás* is ordinary Spanish and gives no offence. So the site is held to
one distinction and one only, and it is the one Spanish Orthodox usage
actually keeps.

| the calendar's rank | Spanish | note |
|---|---|---|
| Venerable (monastic) | **nuestro venerable padre** N. | *nuestra venerable madre*; never *san* alone |
| Saint (bishop) | **nuestro padre entre los santos** N. | the received shape; *el santo jerarca* where the rank is the label |
| Martyr | el santo mártir N. | *la santa mártir* |
| Great Martyr | el santo gran mártir N. | *la santa gran mártir* |
| Hieromartyr | el santo hieromártir N. | |
| Monk-martyr | el venerable mártir N. | built on the monastic word, as Slavonic builds it |
| New Martyr | el santo neomártir N. | |
| Protomartyr | el santo protomártir N. | |
| Apostle | el santo apóstol N. | |
| Prophet | el santo profeta N. | *la santa profetisa* |
| Confessor | el santo confesor N. | |
| Righteous | el justo N. | *la justa*; *los santos y justos Joaquín y Ana* |
| Blessed, fool | el bienaventurado N., loco por Cristo | |
| Unmercenary | el santo anárgiro N. | *sanador anárgiro* |
| Equal-to-the-Apostles | el santo igual a los apóstoles N. | |
| Passion-bearer | el santo portador de la pasión N. | |
| Stylite | el santo estilita N. | |
| Myrrh-bearer | la santa mirófora N. | |
| Right-believing prince | el santo príncipe N. | *el santo gran príncipe* |
| Wonderworker | el taumaturgo N. | |
| Abbot | el igumeno N. | *archimandrita*, *abad* where the house is Western |
| Forefather | el santo antepasado N. | *los santos padres* |

`tools/check_register.py --lang es` asserts the monastic rule and nothing
else, exactly as it does for Greek, Romanian and German:

```bash
python3 tools/check_register.py --lang es
```

Run it on every sitting, not at the end.

## Where San, Santo and Santa may stand

This is the decision that touches the most lines of the vocabulary, because
the vocabulary is full of churches, monasteries, towns and dedications, and
every one of them wants the apocopated form.

**Before a person named as a saint in his own right, the honorific is his
rank, not the bare word.** *El santo mártir Jorge*, not *san Jorge el
mártir*; *nuestro venerable padre Sergio*, not *san Sergio*. The vocabulary
is what stands beside a life on a card, so it speaks of the saint the way
the life does.

**Before the name of a thing, the apocopated form is the only right one.**
A church, a monastery, a town, a gate, a bridge, a feast that names itself
after a saint - these are proper names in Spanish and they take *San*,
*Santo*, *Santa* and nothing else: *el monasterio de San Sabas*, *la iglesia
de Santa Irene*, *la laura de San Atanasio*, *San Petersburgo*. Writing *la
iglesia del santo mártir Jorge* for a dedication is the calendar's language
put where the map's language belongs.

The apocopation itself is the ordinary Spanish rule and there is no room to
choose:

- **san** before a masculine name: san Juan, san Basilio, san Nicolás.
- **santo** before a masculine name beginning *To-* or *Do-*: santo Tomás,
  santo Domingo, santo Tomé. And **Santo** standing before a noun rather
  than a name: el Santo Sepulcro, el Santo Monte, los Santos Lugares.
- **santa** before a feminine name, always, with no apocopation: santa Ana,
  santa Tecla, santa Teodora.
- Capitalised when it is part of a proper name (San Sabas the monastery),
  lower case when it is the adjective doing its ordinary work (el santo
  mártir Jorge, los santos padres).

## The ranks the English writes as a compound

The calendar carries 175 distinct rank strings, and most of the compound
ones are two ranks joined by a comma. Spanish joins them with **y** where
both are borne at once and keeps the comma where the second names an office:
*Obispo, hieromártir* becomes **hieromártir y obispo**, because the Spanish
ear puts the order of sanctity first and the see after it. *Abad (Igumen)*
is **igumeno**, not a gloss inside brackets: Spanish has the word and does
not need to explain the Greek to itself.

Where the English carries a parenthetical that is a real alternative name -
*(Voino-Yasenetsky)*, *(Abibus)* - the parenthesis is kept, because it is
the index's own apparatus and not a gloss.

## Spelling

The house text rules hold: hyphens and never dashes, straight quotes, one
blank line between paragraphs. To them Spanish adds two of its own.

- **Accents are written in full, on capitals as well.** *Éfeso*, *África*,
  *Ávila*, *Ámbar*. A capital letter does not lose its tilde; that was a
  typewriter's limitation and never a rule of the language.
- **The site does not use the inverted opening marks in labels.** The
  vocabulary is made of noun phrases, not sentences, so the question is
  moot; where a full sentence in the lives asks a question, the language's
  own punctuation stands and is not simplified.

## Cyrillic is transliterated the Spanish way

Spanish-language Orthodox books do not pass Slavic names through the
English. The scheme is the ordinary Spanish one, and it exists so that a
reader sounding out the word arrives at something close to the Russian
rather than at something that is neither language:

| Cyrillic | Spanish | | Cyrillic | Spanish |
|---|---|---|---|---|
| в | v | | х | j |
| ж | zh | | ц | ts |
| з | z | | ч | ch |
| ш | sh | | щ | sch |
| й | i | | ы | y |
| ю | yu | | э | e |
| я | ya | | ё | io |
| г | g, gu before e and i | | е after a vowel | ie |

So Киев is **Kiev**, Новгород **Nóvgorod**, Владимир **Vladímir**, Суздаль
**Súzdal**, Чернигов **Chernígov**, Радонеж **Rádonezh**, Вологда
**Vólogda**, Рязань **Riazán**, Оптина **Óptina**.

**The written accent carries the Russian stress.** This is the rule behind
every one of those forms and it is not decoration. Spanish stress is fixed
by the ending: a word ending in a consonant other than *n* or *s* is
stressed on its last syllable, so an unmarked *Novgorod* is read
*novgoRÓD* and an unmarked *Radonezh* *radoNÉZH*, neither of which is a
word anyone says. The accent goes where the Spanish rule would otherwise
move the stress off where the Russian puts it, and stays off where the two
already agree - **Sarov**, **Smolensk**, **Kazán**, **Yaroslavl**,
**Irkutsk**, **Tobolsk**.

It is written on the names a reader will say aloud - the cities, the
lands, the great houses - which is exactly the set the lives already
accent: Nóvgorod, Vladímir, Súzdal, Vólogda, Chernígov, Bélgorod, Riazán,
Kostromá, Múrom, Rádonezh, Óptina. The small northern foundations, whose
names a Spanish reader meets once and does not say, keep the plain
transliteration the lives give them - Belozersk, Borovsk, Dymsk, Galich,
Perekop, Solovki, Vorbozomsk - and the vocabulary follows the lives there
rather than accenting names the lives leave bare. The rule is not that
every Slavic word carries a mark; it is that no word a reader will
pronounce is left to be pronounced wrongly.

Greek and Latin names take the Spanish form where Spanish has one -
**Éfeso**, **Ancira**, **Nicomedia**, **Cesarea**, **Calcedonia**,
**Tesalónica**, **Adrianópolis**, **Asia Menor**, **Antioquía**,
**Alejandría** - and are otherwise transliterated from the Greek rather than
passed through the English: *Amasea*, *Anazarbo*, *Arianzo*.

Celtic, English and Georgian names keep their own spelling, since Spanish
has received no form for most of them, and take a Spanish preposition
around it: *de Lindisfarne*, *de Iona*, *de Gareji*.

## What a script can catch in a Spanish value

Less than in a Slavonic language and more than in German, because Spanish
carries diacritics that English does not.

- **A Greek or Cyrillic letter.** Spanish is written in Latin letters, so
  one Cyrillic character means a name was copied by eye from a Russian
  source and one letter was never touched. `tools/loop.py` refuses the
  block; that is the guard, and it fires before the file is written.
- **A combining mark.** Accented letters are written precomposed. A value
  carrying *e* followed by a combining acute looks identical on the page and
  sorts and searches as a different word.
- **A value identical to its English key** means nothing was written.
- **A house-rule character**: a long dash, a curly quote, a soft hyphen.

The appender in `tools/loop.py` tests every one of these on every block, so
none of them can reach the file. What it cannot test is whether the Spanish
reads as Spanish, and that is the whole of the work.

## The order of work

| | where it is written | what publishes it | where it stands |
|---|---|---|---|
| the names | in `NAMES_I18N`, `index.html` | `tools/build_saint_names.py` | done |
| the lives | `tools/saint_lives/es.py` | `tools/build_saint_lives.py` | 1,456 of 1,456 |
| the vocabulary | `tools/saint_terms/es.py` | `tools/build_saint_terms.py` | 10,632 of 10,632 |
| the calendar entries | `tools/saint_info/es.py` | `tools/saint_info_i18n.py` | in hand |

The vocabulary is done. `python3 tools/build_saint_terms.py --check` reports
`es 10,632 of 10,632`, beside German, Greek, Romanian, Russian, Serbian and
Ukrainian, and a scan of the values for combining marks, soft hyphens, Greek
and Cyrillic letters and the forbidden punctuation comes back clean. Three
hundred and twenty-two renderings are identical to their English key, and
every one of them is a place or a person Spanish spells the same way -
Belozersk, Brest, Nea Makri, Solovki, Valaam; none is a phrase left in
English.

It was written in the order
`tools/loop.py` hands them out, which is `sorted()` over the phrases the
index actually shows - so nothing can be missed and nothing invented. The
loop is one command:

```bash
python3 tools/loop.py terms es --status
python3 tools/loop.py terms es --next 40
python3 tools/loop.py terms es --append batch.txt && \
  python3 tools/build_saint_terms.py --check && \
  python3 tools/loop.py terms es --next 40
```

`tools/saint_terms/es.py` is written entirely as `TEXT`. `PARTS` and
`expand()` are an optimisation the older languages took and are not
required; deciding per phrase whether it is an atom or a compound is a
judgment per phrase, and a judgment per phrase is a stop per phrase. The
lands can be factored out afterwards, or never.

## The nine fields, and what each one is

The vocabulary is not one kind of phrase. Knowing which field a phrase came
from settles most of the questions about how to render it.

| field | count | what it is | how Spanish takes it |
|---|---|---|---|
| type, state, era, rank | 235 | the badge on a card | a noun phrase, capitalised as a label |
| place, origin, region, country | 1,197 | town, then the land it stood in | received form, comma as in the English |
| patronPlaces | 537 | the town a saint is patron of | the bare place name |
| canonizedBy | 145 | who glorified him and when | a clause: *Iglesia de Rusia, glorificado en 1108* |
| baptismalName | 101 | the name before tonsure | the Spanish form of the name |
| titles | 980 | how else the saint is named | *de Ancira*, *el Confesor*, *obispo de Éfeso* |
| relics | 749 | where the relics rest | a full sentence, as the English is |
| patronWork, patronCauses | 4,194 | what is asked of him | a noun phrase, lower case, no article unless the English has one |
| related | 1,476 | the kindred commemoration | a name and its apposition |
| icon | 1,407 | how he is written in an icon | a full descriptive sentence |

The two largest are the intercessions and the icons, and they are the two
where the temptation to translate word for word is strongest, because both
are English of a deliberately heightened kind. *The demons driven from the
temples* is **los demonios expulsados de los templos** and not a relative
clause; *A tall austere virgin martyr with a radiant crown* is **Una virgen
mártir alta y austera, con una corona resplandeciente**. Spanish puts the
adjective after the noun and does not stack three of them before it.

## The trap at the end

`data/saint-terms.v5.*.json` is the name the Saints page fetches now, and it
is rewritten under that same name on every sitting while being served
`immutable, max-age=31536000`. A reader who opens the Saints page in Spanish
while the vocabulary is a tenth written holds that tenth for a year.

So when Spanish is finished, the filename version moves - terms, lives and
names together if they have all moved - and the fetch in `saints.html` moves
with it. `tools/check_site.py` compares the name the page asks for against
the name the builder writes. This is the same defect Romanian recorded and
Ukrainian was caught by; see the closing section of `docs/UKRAINIAN.md`.

Publishing is not this sitting's work. `--check` only; no `--write`, no
stamp, no page touched.

## Then

French and Italian, whose lives are already written or begun; then pt;
then sw, ja, ko, zh; then hy, arc, hi, bn, ur.
