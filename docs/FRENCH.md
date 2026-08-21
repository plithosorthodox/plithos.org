# French: the register, settled before the writing starts

French comes to the Saints page the way Spanish did - with its lives already
written, 1,456 of them, and with neither its vocabulary nor its calendar
entries. So the register is not decided here. It is *read off* what is already
standing, and where this file states a rule the rule was taken from
`tools/saint_lives/fr.py` and can be checked there.

French is also the one language on this site with a long Orthodox literature
of its own. The parishes have been publishing in French for a century - the
service books, the great synaxaria, the Philocalie - and they have settled
nearly every word this vocabulary needs. Where they have, the received form
stands and is not rendered again: la Dormition, la Théophanie, la Rencontre,
l'Exaltation de la Croix, le Grand Carême, la Divine Liturgie, la Sainte
Montagne, l'higoumène, l'anargyre, le fol-en-Christ, l'invention des
reliques, les collyves, l'hésychie, la métanie. This is not a field where the
site invents.

## What French is not

The danger is German's, not Ukrainian's. There is no neighbouring alphabet to
drift into. What is at hand for every word is the Western church vocabulary,
and in French it is not a borrowing but the language's own, formed over
fifteen centuries of Latin Christianity in Gaul and in France. A French reader
has *Assomption*, *Messe*, *Docteur de l'Église*, *bienheureux*, *Notre-Dame*
and *image pieuse* ready before he is asked, and each of them carries a Church
behind it that is not this one.

- **la Dormition**, never *l'Assomption*. The Assumption is a Roman dogma of
  1950 and a different claim; the Dormition is a falling asleep.
- **la Divine Liturgie**, never *la Messe*. The lives write it simply *la
  Liturgie* where the context is plain, and that is right too.
- **Père de l'Église**, never *Docteur de l'Église*. The Doctors are a Roman
  category with a list, and the Fathers are not on it.
- **la Mère de Dieu**, and **la Théotokos** where the title is the Council's
  word. Never *Notre-Dame*, which is the devotional register of another
  Church and appears nowhere in the lives; never *la Sainte Vierge* standing
  alone as an honorific. *la Toute-Sainte* is available where the Greek
  Panagia is meant.
- **l'icône**, feminine, never *une image pieuse* and never *un tableau*.
- **le vénérable** for the monastic, never *le bienheureux*. *Bienheureux*
  renders the Roman *beatus*, a degree one step below canonisation. In
  Orthodox French it is the word for the fools for Christ and for the blessed
  departed, and it is a description and not a rank in a process.
- **le jeûne**, and the named fasts - *le Grand Carême*, *le carême des
  Apôtres*, *le carême de la Dormition*, *le carême de la Nativité*. The bare
  word *Carême* means the Great Fast only.
- **les reliques**, never *les restes*. **la translation** for the translation
  of relics and **l'invention** for their uncovering, which are the two
  distinct feasts the calendar keeps; the lives use both and keep them apart,
  and *l'invention des reliques* is the received French, not a false friend to
  be smoothed into *la découverte*.
- **prêtre** or **presbytre**, never *curé*, which is an office in a parish
  register, and never *pasteur*.
- **le monastère** and **la laure** and **le skite**. *Le couvent* is
  admitted, and only for a house of women, because the lives use it that way
  eighteen times - *le couvent du Saint-Sauveur*, *le couvent de l'Ascension*
  - and in French it does not carry the Western order behind it that
  *convento* carries in Spanish. A men's house is a *monastère*.
- **l'évêque**, **l'archevêque**, **le métropolite** - not *le métropolitain*,
  which in French is a railway.

## The honorific

French belongs with Greek, Romanian, German and Spanish, and not with
Russian: **saint Nicolas** is ordinary French and gives no offence. So the
site is held to one distinction and one only, and it is the one French
Orthodox usage actually keeps: the monastic is **vénérable**, never merely
*saint*.

| the calendar's rank | French | note |
|---|---|---|
| Venerable (monastic) | **le vénérable** N. | *la vénérable*; never *saint* alone |
| Saint (bishop) | saint N., évêque de X | *le saint hiérarque* where the rank is the label |
| Hierarch | le hiérarque | the type badge; *les saints hiérarques* |
| Martyr | le saint martyr N. | *la sainte martyre* |
| Great Martyr | le saint grand-martyr N. | *la sainte grande-martyre*, hyphenated |
| Hieromartyr | le saint hiéromartyr N. | |
| Monk-martyr | le saint moine-martyr N. | *la sainte moniale-martyre* |
| New Martyr | le saint néomartyr N. | *la sainte néomartyre* |
| Protomartyr | le saint protomartyr N. | *la sainte protomartyre* |
| Apostle | le saint apôtre N. | *le saint et tout-loué apôtre* for Andrew and Bartholomew |
| Prophet | le saint prophète N. | *la sainte prophétesse* |
| Confessor | le saint confesseur N. | *la sainte confesseuse* |
| Righteous | le juste N. | *la juste*; *les saints et justes Joachim et Anne* |
| Blessed, fool | le bienheureux N., fol-en-Christ | *la bienheureuse* N., *folle en Christ* |
| Unmercenary | le saint anargyre N. | *les saints anargyres* |
| Equal-to-the-Apostles | saint N., égal aux apôtres | *égale aux apôtres* |
| Passion-bearer | le saint porte-passion N. | plural *les saints porte-passion*, invariable |
| Stylite | le saint stylite N. | |
| Myrrh-bearer | la sainte myrophore N. | *myroblyte* is the myrrh-streaming saint, a different word |
| Right-believing prince | le saint prince fidèle N. | *le saint grand-prince*, *la sainte princesse fidèle* |
| Wonderworker | le thaumaturge N. | |
| Abbot | l'higoumène | *archimandrite*; *abbé* only where the house is Western |
| Forefather | le saint aïeul N. | *les saints ancêtres*, *les saints Pères* |
| Fool-for-Christ | le fol-en-Christ | *la folle en Christ*; the ascesis is *la folie pour le Christ* |

`tools/check_register.py --lang fr` already carries this vocabulary and
asserts the monastic rule and nothing else, exactly as it does for Greek,
Romanian, German and Spanish:

```bash
python3 tools/check_register.py --lang fr
```

It reports zero errors over the lives today, and it must stay there. Run it on
every sitting, not at the end.

## Where saint, sainte and Saint- may stand

This is the decision that touches the most lines of the vocabulary, because
the vocabulary is full of churches, monasteries, towns and dedications and
every one of them wants a form of the word.

**Before a person named as a saint in his own right, the honorific carries
his rank.** *Le saint martyr Georges*, not *saint Georges le martyr*; *le
vénérable Serge de Radonège*, not *saint Serge de Radonège* where the phrase
stands alone as a rank. Inside a running clause, where the name is mentioned
rather than announced, the plain *saint Serge* is what the lives write and is
right: the rule is about the honorific, not about every occurrence of a name.

**Before the name of a thing, the hyphenated form is the only right one.** A
church, a monastery, a town, a gate, a cathedral, a feast that names itself
after a saint - these are proper names in French and they take **Saint-**,
**Sainte-**, capitalised and hyphenated, and nothing else: *le monastère
Saint-Sabas*, *l'église Sainte-Irène*, *la laure Saint-Athanase*, *la
cathédrale Sainte-Sophie*, *Saint-Pétersbourg*, *le couvent du
Saint-Sauveur*, *la Trinité-Saint-Serge*. Writing *l'église du saint martyr
Georges* for a dedication is the calendar's language put where the map's
language belongs - though the lives do write exactly that when the sentence is
about the martyr and not about the building, and that stays.

The rest is the ordinary rule of the language and there is no room to choose:

- **saint / sainte**, lower case and unhyphenated, when it is the adjective
  doing its ordinary work before a rank or a name: le saint apôtre André,
  saint Basile le Grand, les saints Pères.
- **Saint- / Sainte-**, capitalised and hyphenated, when it is part of a
  proper name: Saint-Sabas the monastery, Sainte-Sophie the church,
  Saint-Pétersbourg the city.
- **Saint** capitalised and unhyphenated before a noun rather than a name: le
  Saint-Sépulcre, la Sainte Montagne, les Saints Lieux, le Saint-Esprit.
- Elision before a vowel: *l'église Saint-André*, *la laure Saint-Antoine*,
  and *Sainte-Anne* keeps its e.

## The ranks the English writes as a compound

The calendar carries 169 distinct rank strings and most of the compound ones
are two ranks joined by a comma. French joins them with **et** where both are
borne at once and keeps the order of sanctity first and the see after it:
*Bishop, Hieromartyr* becomes **hiéromartyr et évêque**, *Monk, Church
Father* becomes **moine et Père de l'Église**. *Abbot (Igumen)* is
**higoumène**, not a gloss inside brackets: French has the word and does not
need to explain the Greek to itself.

Where the English carries a parenthetical that is a real alternative name -
*(Voino-Yasenetsky)*, *(Abibus)* - the parenthesis is kept, because it is the
index's own apparatus and not a gloss.

## Spelling

The house text rules hold: hyphens and never dashes, straight quotes, one
blank line between paragraphs. To them French adds four of its own.

- **Accents are written in full, on capitals as well.** *Éphèse*, *Égypte*,
  *Édesse*, *Éthiopie*, *Évariste* - a capital does not lose its acute. That
  was a typewriter's limitation and never a rule of the language.
- **The oe ligature is written as a ligature.** **cœur**, **sœur**,
  **œuvre**, **chœur**, **vœu**, **œcuménique** - the lives write the
  single character four hundred and eighty-one times against seventy-six for
  the two letters, so the ligature is the house form and the table follows it.
  A phrase that spells it out reads as a different word to a search.
- **No guillemets and no typographic apostrophe.** The site quotes by
  indentation and never by marks, and the apostrophe is the straight one, as
  the house rule requires everywhere. `tools/loop.py` refuses a block that
  carries the curly form.
- **No narrow space before the high punctuation.** The vocabulary is made of
  noun phrases and short sentences; where a colon or a semicolon falls it
  takes an ordinary space before it, or none, because a thin space is a
  character a browser will break a line on.

## Cyrillic is transliterated the French way

French-language Orthodox books do not pass Slavic names through the English.
The scheme is the ordinary French one, it is the one the lives already use
throughout, and it exists so that a reader sounding out the word arrives at
something close to the Russian rather than at something that is neither
language:

| Cyrillic | French | | Cyrillic | French |
|---|---|---|---|---|
| у | ou | | х | kh |
| в | v | | ц | ts |
| ж | j | | ч | tch |
| з | z | | ш | ch |
| с between vowels | ss | | щ | chtch |
| й | i, ï after a vowel | | ы | y |
| ю | iou | | э | e |
| я | ia | | ё | io |
| г | g, gu before e and i | | е after a vowel | ïe |

So Курск is **Koursk**, Суздаль **Souzdal**, Ярославль **Iaroslavl**,
Чернигов **Tchernigov**, Муром **Mourom**, Калуга **Kalouga**, Галич
**Galitch**, Хутынь **Khoutyn**, Дивеево **Diveïevo**, Вологда **Vologda**,
Печерский **Petcherski**, Волоколамск **Volokolamsk**, Верхотурье
**Verkhotourie**, Пошехонье **Pochekhonié**, Тохтамыш **Tokhtamych**,
Кучково **Koutchkovo**, Мстиславич **Mstislavitch**.

The patronymics and family names in *-ович*, *-евич* end **-ovitch**,
**-iévitch**; the adjectival names in *-ский* end **-ski** and not *-sky*.

**Where French has received a form, the received form stands over the
scheme.** Радонеж is **Radonège** and not *Radonèje*; Москва is **Moscou**;
Киев is **Kyiv**, which is what the lives write two hundred times against
twenty for *Kiev*, and the Caves are **les Grottes de Kyiv**, **les Grottes
Proches** and **les Grottes Lointaines**, with **la Laure des Grottes**. The
land is **la Rus'** with its apostrophe, as the index itself writes it.

Greek and Latin names take the French form where French has one - **Éphèse**,
**Césarée**, **Nicomédie**, **Thessalonique**, **Antioche**, **Alexandrie**,
**Chalcédoine**, **Ancyre**, **Adrianople**, **Asie Mineure**, **Myre en
Lycie**, **Nicée**, **Trébizonde**, **Iconium** - and are otherwise
transliterated from the Greek rather than passed through the English:
*Amasée*, *Anazarbe*, *Arianze*.

Celtic, English, Georgian and Serbian names keep their own spelling, since
French has received no form for most of them, and take a French preposition
around it: *de Lindisfarne*, *d'Iona*, *de Garedja*, *de Detchani*. Where the
lives have already chosen a spelling for such a name, the vocabulary follows
the lives rather than choosing again.

## What a script can catch in a French value

Less than in a Slavonic language and about what Spanish allowed, because
French carries diacritics that English does not.

- **A Greek or Cyrillic letter.** French is written in Latin letters, so one
  Cyrillic character means a name was copied by eye from a Russian source and
  one letter was never touched. `tools/loop.py` refuses the block, and it
  fires before the file is written.
- **A combining mark.** Accented letters are written precomposed. A value
  carrying *e* followed by a combining acute looks identical on the page and
  sorts and searches as a different word.
- **A value identical to its English key** means nothing was written, unless
  the phrase is a place French spells the same way - Novgorod, Pskov, Rostov,
  Athos, Iona.
- **A house-rule character**: a long dash, a curly quote, a soft hyphen.

The appender tests every one of these on every block, so none of them can
reach the file. What it cannot test is whether the French reads as French, and
that is the whole of the work.

## The nine fields, and what each one is

The vocabulary is not one kind of phrase. Knowing which field a phrase came
from settles most of the questions about how to render it.

| field | count | what it is | how French takes it |
|---|---|---|---|
| type, state, era, rank | 234 | the badge on a card | a noun phrase, capitalised as a label |
| place, origin, region, country | 973 | town, then the land it stood in | received form, comma as in the English |
| patronPlaces | 435 | the town a saint is patron of | the bare place name |
| canonizedBy | 145 | who glorified him and when | a clause: *Église de Russie, glorifié en 1108* |
| baptismalName | 101 | the name before tonsure | the French form of the name |
| titles | 975 | how else the saint is named | *d'Ancyre*, *le Confesseur*, *évêque d'Éphèse* |
| relics | 726 | where the relics rest | a full sentence, as the English is |
| patronWork, patronCauses | 4,151 | what is asked of him | a noun phrase, lower case, with the article French wants |
| related | 1,476 | the kindred commemoration | a name and its apposition |
| icon | 1,407 | how he is written in an icon | a full descriptive sentence |

The two largest are the intercessions and the icons, and they are the two
where the temptation to translate word for word is strongest, because both are
English of a deliberately heightened kind. *The demons driven from the
temples* is **les démons chassés des temples** and not a relative clause; *A
tall austere virgin martyr with a radiant crown* is **Une vierge martyre
grande et austère, couronnée de lumière**. French puts the adjective after the
noun and does not stack three of them before it.

The intercessions take the definite article where French would not leave a
bare plural standing - *the poor and sick* is **les pauvres et les malades**,
not *pauvres et malades* - and take it likewise where the English phrase is an
abstraction: *humiliation embraced* is **l'humiliation embrassée**, *books
multiplied for God* is **les livres multipliés pour Dieu**. The rule is not
the English article; it is what French does with a noun standing as a heading.

The icon sentences keep the English full stop and the English order of
tableau: the figure first, then what is around him, then what the icon says
about him. French takes the participles the English strings after the comma as
participles - *tenant*, *portant*, *couronné de* - and does not turn them into
relative clauses, which is the one change that would double the length of a
thousand sentences.

## The order of work

| | where it is written | what publishes it | where it stands |
|---|---|---|---|
| the names | in `NAMES_I18N`, `index.html` | `tools/build_saint_names.py` | done |
| the lives | `tools/saint_lives/fr.py` | `tools/build_saint_lives.py` | 1,456 of 1,456 |
| the vocabulary | `tools/saint_terms/fr.py` | `tools/build_saint_terms.py` | in hand |
| the calendar entries | `tools/saint_info/fr.py` | `tools/saint_info_i18n.py` | in hand |

The vocabulary is written in the order `tools/loop.py` hands the phrases out,
which is `sorted()` over the phrases the index actually shows, so nothing can
be missed and nothing invented. The loop is one command:

```bash
python3 tools/loop.py terms fr --status
python3 tools/loop.py terms fr --next 40
python3 tools/loop.py terms fr --append batch.txt && \
  python3 tools/build_saint_terms.py --check && \
  python3 tools/loop.py terms fr --next 40
```

`tools/saint_terms/fr.py` is written entirely as `TEXT`. `PARTS` and
`expand()` are an optimisation the older languages took and are not required;
deciding per phrase whether it is an atom or a compound is a judgment per
phrase, and a judgment per phrase is a stop per phrase. The lands can be
factored out afterwards, or never.

## The trap at the end

`data/saint-terms.v5.*.json` is the name the Saints page fetches now, and it
is rewritten under that same name on every sitting while being served
`immutable, max-age=31536000`. A reader who opens the Saints page in French
while the vocabulary is a tenth written holds that tenth for a year.

So when French is finished the filename version moves - terms, lives and names
together if they have all moved - and the fetch in `saints.html` moves with
it. `tools/check_site.py` compares the name the page asks for against the name
the builder writes. This is the same defect Romanian recorded and Ukrainian
was caught by; see the closing section of `docs/UKRAINIAN.md`.

Publishing is not this sitting's work. `--check` only; no `--write`, no stamp,
no page touched.

## Then

Italian, whose lives are begun; then pt; then sw, ja, ko, zh; then hy, arc,
hi, bn, ur.
