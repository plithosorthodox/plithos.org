# Italian: the register, settled before the writing starts

The tenth language. Written, not converted: the test is whether a reader who
grew up in an Italian-speaking Orthodox parish would recognise it as something
someone from his own Church wrote.

Italian comes to this site with a difficulty none of the others has. It is the
language of the country where the Latin Church is at home, and its whole
devotional vocabulary is to hand and is nearly right. *Assunzione*,
*Messa*, *Dottore della Chiesa*, *beato*, *convento*, *santo patrono* are
all good Italian and all belong to another Church's order of things. The
Orthodox parishes of Italy - Greek, Romanian, Russian, Serbian, and the
Italian-language ones the exarchates have raised - have their own received
forms, and where they have one it is used here.

## What Italian is not

| not this | this | why |
|---|---|---|
| l'Assunzione | **la Dormizione** | the feast is the falling-asleep, not the assuming |
| la Messa | **la Divina Liturgia** | the rite has its own name |
| Dottore della Chiesa | **Padre della Chiesa** | *Dottore* is a Latin title of honour the East does not confer |
| convento | **monastero** | *convento* only for a house of women, and rarely |
| il beato N. (a monastic) | **il venerabile N.** | see below |
| curato, parroco | **sacerdote**, **presbitero** | the office, not the benefice |
| santo patrono di | **protettore di** | the intercession, not the parish dedication |

## The honorific is the rank

CLAUDE.md's rule holds here as everywhere: a saint's honorific is his rank,
not the word *santo*. Italian sets *san*, *santo*, *sant'* or *santa* before
the name and the rank after it - **san Basilio il Grande, arcivescovo di
Cesarea** - and that is right. What is wrong is the bare *santo* standing
where the Church names an order.

The distinction Italian must keep, and the one `tools/check_register.py`
enforces for this language and nothing else, is the monastic:

> **il venerabile** Sergio di Radonež, not *il beato* and not *san* alone.

*Beato* is kept for what it renders in the East: the fool for Christ - **il
beato Basilio, folle per Cristo** - and the blessed of a local veneration.
Giving it to a monk is the Latin ladder of beatification imported into a
calendar that has no such step.

## The ranks

Fixed, and the pattern in `LANGS["it"]` is derived from them:

| English | Italian |
|---|---|
| Martyr / Great-martyr | il martire / il grande martire |
| Hieromartyr / Monk-martyr | lo ieromartire / il monaco martire |
| New Martyr / Protomartyr | il neomartire / il protomartire |
| Venerable (monastic) | il venerabile |
| Monk / Nun / Hermit | il monaco / la monaca / l'eremita |
| Abbot (Igumen) / Abbess | l'igumeno / la badessa |
| Archimandrite / Hieromonk | l'archimandrita / lo ieromonaco |
| Bishop / Archbishop | il vescovo / l'arcivescovo |
| Metropolitan / Patriarch | il metropolita / il patriarca |
| Hierarch | il gerarca |
| Apostle / of the Seventy | l'apostolo / dei Settanta |
| Prophet / Forerunner | il profeta / il Precursore |
| Confessor / Righteous | il confessore / il giusto |
| Fool-for-Christ | il folle per Cristo |
| Equal-to-the-Apostles | pari agli apostoli |
| Unmercenary / Myrrh-bearer | l'anargiro / la miroforo |
| Passion-bearer | il portatore della passione |
| Wonderworker / Stylite | il taumaturgo / lo stilita |
| Right-believing Prince | il principe fedele |
| Synaxis / Feast / Icon | la sinassi / la festa / l'icona |

*Metropolita*, never *metropolitano*, which in Italian is a railway.

## Spelling

Hyphens, never dashes. Straight apostrophes and straight quotes: the
typographic ones are refused by `tools/loop.py` before the file is touched,
and Italian needs the apostrophe constantly - *dell'*, *un'*, *sant'* - so this
is the rule that gets tested every third line.

Accents as Italian writes them and not as a hurried hand leaves them:
*perché*, *è*, *città*, *virtù*, *santità*. `E` and `È` are different words.

## Slavic names are transliterated the Italian scholarly way

The lives already written settle it: **Radonež, Galič, Vyšgorod, Černihiv,
Čudov, Mirož** - `ž`, `č`, `š` precomposed, never a letter with a combining
caron after it. Ukrainian places take their Ukrainian form, as the English
keys do: **Kyiv**, **Černihiv**, **Rus'** with the apostrophe.

Saints whose names Italian has long had keep the Italian form - Giovanni,
Basilio, Gregorio, Teodoro, Demetrio, Nicola, Michele - and saints Italian
has never had keep the transliteration.

## The ten fields, and what each one is

The vocabulary is not one kind of phrase, and knowing which field a phrase
came from settles most of the questions about how to render it.

| field | count | what it is | how Italian takes it |
|---|---|---|---|
| patronCauses | 2,622 | what is asked of him | a noun phrase with the article Italian wants |
| patronWork | 1,572 | whom he is asked for | likewise, lower case |
| related | 1,476 | the kindred commemoration | a name and its apposition |
| icon | 1,407 | how he is written in an icon | a full descriptive sentence |
| titles | 980 | how else the saint is named | *di Ancira*, *il Confessore*, *vescovo di Efeso* |
| relics | 749 | where the relics rest | a full sentence, as the English is |
| place, origin, region, country | 1,197 | town, then the land it stood in | received form, comma as in the English |
| patronPlaces | 537 | the town a saint is patron of | the bare place name |
| rank, type, era, state, feastRank | 240 | the badge on a card | a noun phrase, capitalised as a label |
| canonizedBy | 145 | who glorified him and when | a clause: *Chiesa di Russia, glorificato nel 1108* |
| baptismalName | 101 | the name before tonsure | the Italian form of the name |

The two largest are the intercessions and the icons. Both are English of a
deliberately heightened kind, and both are where translating word for word
does the most damage. *The demons driven from the temples* is **i demoni
scacciati dai templi** and not a relative clause. Italian takes the
participles the English strings after the comma as participles - *tenendo*,
*portando*, *coronato di* - and does not turn them into subordinate clauses,
which is the one change that would double the length of fourteen hundred
sentences.

The intercessions take the definite article where Italian would not leave a
bare plural standing - *the poor and sick* is **i poveri e i malati** - and
take it likewise where the phrase is an abstraction: *humiliation embraced* is
**l'umiliazione abbracciata**.

## The order of work

| | where it is written | what publishes it | where it stands |
|---|---|---|---|
| the lives | `tools/saint_lives/it.py` | `tools/build_saint_lives.py` | 120 of 1,456 |
| the vocabulary | `tools/saint_terms/it.py` | `tools/build_saint_terms.py` | 10,632 of 10,632 |
| the calendar entries | `tools/saint_info/it.py` | `tools/saint_info_i18n.py` | not begun |

`docs/LOOP.md` states the rule the lives here broke: the vocabulary comes
first, because `check_register.py --scaffold` derives a language's rank
patterns from its own terms table. Italian was given its patterns by hand in
`LANGS` instead, which is why the hundred and twenty lives could be checked at
all. The vocabulary is finished, and the lives that follow inherit it rather than
the other way round.

Two of those hundred and twenty lives write *Grotte di Kiev* where the other
twelve mentions of the city write *Kyiv*. The vocabulary writes **Kyiv**
throughout; the two strays belong to the lives file and are for the lives lane
to settle.
