# Syriac

The register for `tools/saint_terms/arc.py`, read off the Syriac this site has
already published rather than proposed from scratch. Four bodies were already
here when this began, and between them they settle almost every question the
vocabulary raises:

| file | what it is | size |
|---|---|---|
| `data/saint-names.v1.arc.json` | 1,528 commemorations, every rank word and the word order | 45,267 Syriac characters |
| `data/prayers-i18n.v2.arc.json` | 100 prayers, the liturgical register | 79,661 |
| `data/glossary-i18n.v1.arc.json` | 177 ecclesiastical terms | 17,823 |
| `data/saint-info.v1.arc.json` | 119 calendar entries, modern prose | 23,643 |

Where they disagree the prayers decide, because they are the Church's own
books. Where the prayers are silent - and they are silent about ranks, since a
prayer names no saint by his order - the names table decides, because the
vocabulary written here stands beside it in the same index, and because it is
the largest and most systematic of the four.

## What is being written

The Eastern Orthodox synaxarion in Classical Syriac: the language of Ephrem
and of Isaac of Nineveh, both of whom stand in this calendar and whose works
are on this site's shelves.

It is **not** the Syriac Orthodox Church's own calendar, and **not** the
Church of the East's. Their feast names, their reckoning and their proper
saints are not to be imported here on the strength of the shared language. The
commemorations are the ones this site already keeps; only the words are
Syriac. Where Syriac has a received Christian word, the received word is used
and is not re-invented.

## Script and orthography

**Unvocalized Classical Syriac**, script-neutral consonantal text, exactly as
the names table, the prayers and the calendar entries all print it. No vowel
points.

The glossary is the exception in the corpus and is not followed: it is pointed
East Syriac, with the full apparatus of vowel marks and diacritics
(`ܪܹܫ ܕܲܝܪܵܐ` where the names table prints `ܪܝܫ ܕܝܪܐ`). Its **vocabulary** is
authoritative and is used; its **pointing** is not reproduced, because three of
the four bodies do not point and the index would read as two languages set
side by side.

Seyame, the plural marker, is written with U+0308 COMBINING DIAERESIS over the
letter, as all four bodies write it: `ܣܗ̈ܕܐ`, `ܡܥܪ̈ܐ`, `ܫܠܝ̈ܚܐ`. It is not
optional. A plural without it is a defect a reader sees at once.

The construct `ܪܝܫ` is spelled full, not `ܪܫ`. The names table prints `ܪܝܫ`
155 times and `ܪܫ` 3 times; the glossary prefers `ܪܫ`, and loses here.

## Punctuation

- **Comma: U+060C ARABIC COMMA `،`**, which is what the corpus uses. It stands
  in 191 of the 1,528 name entries and 2,465 times in the prayers. Classical
  Syriac has no comma of its own in Unicode and modern Syriac typesetting
  borrows this one; it is a settled convention here, not an intrusion.
- **Full stop: `.`**, as the prayers use it.
- **`܀` belongs to the prayers**, which set it at the end of a versicle. An
  index phrase is not a versicle and does not take it.
- **Straight quotes `"..."`**, per the house rule, for a quoted epithet.
- **Hyphens, never em or en dashes.**

## The honorific is the rank

The bare word for holy stands before a name in Syriac without offence, as it
does in Greek, Romanian and Georgian: `ܩܕܝܫܬܐ ܐܢܓܠܝܢܐ ܕܣܪܒܝܐ` is what the
names table prints and what a Syriac reader expects. So `strict` is False in
`tools/check_register.py`, and only the monastic distinction is asserted: a
monk, a nun, an abbot, a recluse is `ܡܝܩܪܐ`, never merely `ܩܕܝܫܐ`.

### The ranks

Drawn from the names table unless marked otherwise.

| English | Syriac | feminine | plural |
|---|---|---|---|
| Saint | ܩܕܝܫܐ | ܩܕܝܫܬܐ | ܩܕܝ̈ܫܐ |
| Venerable | ܡܝܩܪܐ | ܡܝܩܪܬܐ | ܡܝܩܪ̈ܐ |
| Hierarch | ܪܒ ܟܗ̈ܢܐ | | ܪ̈ܝܫܝ ܟܗ̈ܢܐ |
| Martyr | ܣܗܕܐ | ܣܗܕܬܐ | ܣܗ̈ܕܐ / ܣܗ̈ܕܬܐ |
| Great Martyr | ܣܗܕܐ ܪܒܐ | ܣܗܕܬܐ ܪܒܬܐ | |
| Hieromartyr | ܟܗܢܐ ܣܗܕܐ | | ܟܗ̈ܢܐ ܣܗ̈ܕܐ |
| Monastic Martyr | ܕܝܪܝܐ ܣܗܕܐ | ܕܝܪܝܬܐ ܣܗܕܬܐ | |
| Virgin Martyr | ܒܬܘܠܬܐ ܣܗܕܬܐ | | ܒܬܘ̈ܠܬܐ ܣܗ̈ܕܬܐ |
| New Martyr | ܣܗܕܐ ܚܕܬܐ | | ܣܗ̈ܕܐ ܚܕ̈ܬܐ |
| Passion-bearer | ܚܫܘܫܐ | | ܚܫܘ̈ܫܐ, royal ܣܒ̈ܠܝ ܚܫܐ ܡܠܟܝ̈ܐ |
| Confessor | ܡܘܕܝܢܐ | | ܡܘܕ̈ܝܢܐ |
| Prophet | ܢܒܝܐ | ܢܒܝܬܐ | ܢܒܝ̈ܐ |
| Apostle | ܫܠܝܚܐ | | ܫܠܝ̈ܚܐ |
| Equal-to-the-Apostles | ܫܘܐ ܠܫܠܝ̈ܚܐ | ܫܘܝܬ ܠܫܠܝ̈ܚܐ | |
| Evangelist | ܡܣܒܪܢܐ | | |
| Righteous | ܙܕܝܩܐ | ܙܕܝܩܬܐ | ܙܕܝ̈ܩܐ |
| Blessed | ܛܘܒܢܐ | ܛܘܒܢܝܬܐ | |
| Fool-for-Christ | ܫܛܝܐ ܡܛܠ ܡܫܝܚܐ | | |
| Wonderworker | ܥܒܕ ܬܕܡܪ̈ܬܐ | | ܥܒ̈ܕܝ ܬܕܡܪ̈ܬܐ |
| Unmercenary | ܠܐ ܢܣ̈ܒܝ ܟܣܦܐ | | physician ܐܣܝܐ ܕܠܐ ܟܣܦ |
| Enlightener | ܡܢܗܪܢܐ | ܡܢܗܪܢܝܬܐ | |
| Bishop | ܐܦܣܩܘܦܐ | | ܐܦܣ̈ܩܘܦܐ |
| Archbishop | ܪܝܫ ܐܦܣܩܘܦܐ | | |
| Metropolitan | ܡܝܛܪܘܦܘܠܝܛܐ | | |
| Patriarch | ܦܛܪܝܪܟܐ | | |
| Archpriest | ܪܝܫ ܟܗ̈ܢܐ | | |
| Priest | ܟܗܢܐ | | ܟܗ̈ܢܐ |
| Presbyter, Elder | ܩܫܝܫܐ | | |
| Deacon | ܡܫܡܫܢܐ | ܡܫܡܫܢܝܬܐ | ܡܫܡ̈ܫܢܐ |
| Reader | ܩܪܘܝܐ | | |
| Abbot | ܪܝܫ ܕܝܪܐ | ܪܝܫܬ ܕܝܪܐ | |
| Archimandrite | ܐܪܟܝܡܢܕܪܝܛܐ (glossary) | | |
| Monk, Hermit | ܕܝܪܝܐ | ܕܝܪܝܬܐ | ܕܝܪ̈ܝܐ |
| Schemamonk | ܐܣܟܡܝܐ | | |
| Ascetic | ܥܢܘܝܐ | | |
| Anchorite | ܐܢܟܘܪܝܛܐ | | |
| Recluse | ܚܒܝܫܐ | | |
| Stylite | ܐܣܛܘܢܪܐ | | |
| Silent | ܫܬܝܩܐ | | |
| Faster | ܨܝܡܐ | | |
| Virgin | ܒܬܘܠܬܐ | | ܒܬܘ̈ܠܬܐ |
| Hymnographer | ܡܙܡܪܢܐ | | |
| Iconographer | ܨܝܪ ܝܘܩ̈ܢܐ | | |
| Theologian | ܬܐܘܠܘܓܘܣ | | |
| Myrrh-bearer | ܡܝܬܝܬ ܒܣ̈ܡܐ | | ܢܫ̈ܐ ܫܩ̈ܠܝ ܒܣ̈ܡܐ |
| Myrrh-streamer | ܡܪܕܐ ܡܘܪܘܢ | | |
| God-bearing | ܠܒܝܫ ܐܠܗܐ | | |
| Prince | ܪܫܐ | | Right-believing ܡܗܝܡܢܐ |
| Princess | ܐܡܝܪܬܐ | | ܐܡܝܪ̈ܬܐ ܪܘܪ̈ܒܬܐ |
| King, Emperor, Tsar | ܡܠܟܐ (also ܩܣܪ) | ܡܠܟܬܐ | |
| Archangel | ܪܝܫ ܡܠܐܟ̈ܐ | | ܪ̈ܝܫܝ ܡܠܐܟ̈ܐ |
| Father | ܐܒܐ | ܐܡܐ | ܐܒܗ̈ܬܐ |

### The six ranks re-checked before the vocabulary reached them

The vocabulary meets a rank long after the table above sets it, so these six
were read out of the names table again at the point of first use rather than
carried on trust. All six stand:

| English | Syriac | as the names table has it |
|---|---|---|
| Venerable | ܡܝܩܪܐ | ܡܝܩܪܐ ܦܘܠܘܣ ܕܬܒܣ |
| Unmercenary | ܠܐ ܢܣ̈ܒܝ ܟܣܦܐ | ܩܕܝ̈ܫܐ ܥܒ̈ܕܝ ܬܕܡܪ̈ܬܐ ܘܠܐ ܢܣ̈ܒܝ ܟܣܦܐ ܩܘܪܘܣ ܘܝܘܚܢܢ |
| Unmercenary physician | ܐܣܝܐ ܕܠܐ ܟܣܦ | ܐܣܝܐ ܕܠܐ ܟܣܦ ܬܠܠܐܘܣ |
| Virgin Martyr | ܒܬܘܠܬܐ ܣܗܕܬܐ | ܒܬܘܠܬܐ ܣܗܕܬܐ ܐܓܢܣ ܕܪܗܘܡܐ |
| Virgin | ܒܬܘܠܬܐ | ܒܬܘܠܬܐ ܐܡܝܢܐܝܬ ܡܪܝܡ |
| Presbyter | ܩܫܝܫܐ | ܩܕܝܫܐ ܡܪܩܝܢܘܣ ܩܫܝܫܐ |
| King | ܡܠܟܐ | ܙܕܝܩܐ ܩܕܝܫܐ ܕܘܝܕ ܡܠܟܐ |

Two of them carry a point of word order worth keeping. The unmercenary
physician is ܐܣܝܐ ܕܠܐ ܟܣܦ in the singular but ܠܐ ܢܣ̈ܒܝ ܟܣܦܐ when the rank
stands for a group without the word physician, and the table uses both in the
same breath; neither is a variant of the other. And ܡܠܟܐ follows the name
where ܩܕܝܫܐ and ܙܕܝܩܐ precede it - ܕܘܝܕ ܡܠܟܐ, not ܡܠܟܐ ܕܘܝܕ - except where the
king is being introduced as a king, as in ܡܠܟܐ ܩܕܝܫܐ ܐܣܩܝܘܛ.

### Four ranks on which two bodies disagree

The calendar entries in `data/saint-info.v1.arc.json` use a different word
from the names table in four places. The names table is followed, for the
reason given at the top; the alternative is recorded here so that it is a
decision and not an oversight.

| | names table (followed) | calendar entries |
|---|---|---|
| Venerable | ܡܝܩܪܐ (308) | ܚܣܝܐ (39) |
| Righteous | ܙܕܝܩܐ (18) | ܟܐܢܐ (3) |
| Hieromartyr | ܟܗܢܐ ܣܗܕܐ (90) | ܣܗܕܐ ܕܒܟܗ̈ܢܐ, ܣܗܕܐ ܟܗܢܝܐ |
| Fool-for-Christ | ܫܛܝܐ ܡܛܠ ܡܫܝܚܐ | ܣܟܠܐ ܡܛܠ ܡܫܝܚܐ |

Righteous is settled beyond argument by the prayers, which have ܙܕܝܩ 24 times
against ܟܐܢ 4, and of those four only one is the adjective.

**Hierarch** is the one rank the names table never renders, having no
commemoration that uses the bare English word. It is taken from the calendar
entries, which render it ܪܒ ܟܗ̈ܢܐ ten times and ܪܝܫ ܟܗ̈ܢܐ nine. ܪܒ ܟܗ̈ܢܐ is
used here for the hierarch and ܪܝܫ ܟܗ̈ܢܐ is left to the archpriest, which is
the glossary's word for it, so that the two do not collapse into one.

**ܡܪܝ is rare and is not the general honorific.** It stands three times in the
whole names table: ܡܪܝ ܝܘܚܢܢ ܫܒܘܩܐ, ܕܝܪܐ ܕܡܪܝ ܣܒܐ, ܣܗܕܘܬܐ ܕܡܪܝ ܓܐܘܪܓܝܣ. The
other 36 apparent hits are ܡܪܝܡ (Mary), ܡܪܝܐ (the Lord) and ܡܪܝܢܘܣ (Marinus).
It is kept for the fathers and monasteries of the Syriac house that already
carry it, and is not spread over the calendar.

## What is already settled and is not to be re-derived

| | |
|---|---|
| Theotokos | ܝܠܕܬ ܐܠܗܐ |
| Our Most Holy Lady the Theotokos and Ever-Virgin Mary | ܡܪܬܢ ܩܕܝܫܬ ܟܠ، ܝܠܕܬ ܐܠܗܐ ܘܒܬܘܠܬܐ ܐܡܝܢܐܝܬ ܡܪܝܡ |
| Nativity of Christ | ܡܘܠܕܐ ܕܡܫܝܚܐ |
| Theophany | ܕܢܚܐ ܕܡܪܢ |
| Entry of the Theotokos into the Temple | ܡܥܠܬܐ ܕܝܠܕܬ ܐܠܗܐ ܠܗܝܟܠܐ |
| Exaltation of the Cross | ܪܘܡܪܡܐ ܕܨܠܝܒܐ |
| Christ | ܡܫܝܚܐ |
| Jesus | ܝܫܘܥ |
| Lord | ܡܪܝܐ, our Lord ܡܪܢ |
| Cross | ܨܠܝܒܐ |
| Icon | ܝܘܩܢܐ, pl ܝܘܩ̈ܢܐ |
| Icon of the Mother of God | ܝܘܩܢܐ ܕܝܠܕܬ ܐܠܗܐ |
| Pascha | ܦܨܚܐ |
| Great Lent | ܨܘܡܐ ܪܒܐ |
| Divine Liturgy | ܩܘܕܫܐ ܐܠܗܝܐ |
| Ecumenical Council | ܣܘܢܗܕܘܣ ܬܒܝܠܝܬܐ |

### The check that keeps the semkath rule honest

Quotations from `data/bible.v4.arc.b64` are kept verbatim, and that
edition writes final semkath where this house writes U+0723, so a batch
that quotes Scripture will legitimately contain characters the rule
otherwise forbids. The two rules only stay separable if the exception is
confined to what is inside the quotation marks, and that is checkable:

```python
quoted = {m.start(1) + i for m in re.finditer(r'"([^"]*)"', text)
          for i, c in enumerate(m.group(1)) if c == "\u0724"}
loose = [i for i, c in enumerate(text) if c == "\u0724" and i not in quoted]
```

`loose` must be empty. The batch that wrote the Meeting of the Lord
carried seven final semkaths, all of them inside the Nunc Dimittis and
Luke's introduction of Anna, and none in this house's own prose.

### Where the vocabulary and the index part company, in practice

The rule is stated once at the top - the vocabulary stands - and it is
worth seeing what it costs, because a reader comparing a life against
its heading will meet the difference. These are the divergences the
lives carry, and every one of them is deliberate:

| | names table | vocabulary, and the lives |
|---|---|---|
| a fuller | ܡܚܘܪܐ | ܩܨܪܐ, and the trade ܩܨܪ̈ܐ |
| an actor | ܐܣܛܪܘܢܐ | ܡܫܥܝܐ, and ܡܫܥ̈ܝܢܐ |
| Bithynia | ܒܘܬܘܢܝܐ | ܒܝܬܘܢܝܐ |
| Brest | ܒܪܛܣܩ | ܒܪܣܛ |
| Chernihiv | ܟܪܢܝܗܒ | ܟܪܢܝܗܝܒ |
| Stachys | ܣܛܟܘܣ | ܐܣܛܟܘܣ |

The saints' own names are untouched by this: where the index prints a
name, the life spells it as the index spells it. What the vocabulary
settles is the common noun and the place.

### The index writes curly quotes around an icon's title; the lives do not

`data/saint-names.v1.arc.json` heads the icons with U+201C and U+201D -
`"ܫܘܪܐ ܕܠܐ ܡܬܬܒܪ"` is printed there with curly quotes. The house rule is
straight quotes, `tools/saint_terms/arc.py` uses straight quotes for the
same titles, and the lives follow the house rule. This is punctuation, not
a rendering of the name, so it is not a case for the rule that the index's
own spelling of a name stands.

## The shapes a commemoration takes

The genitive is the prefixed `ܕ`, and it does nearly all the work that "of"
does in English.

| English | Syriac |
|---|---|
| N of PLACE | ܣܗܕܐ ܒܣܝܠܝܘܣ ܕܐܢܩܘܪܐ |
| N at PLACE | ܣܗܕܐ ܓܘܪܕܝܘܣ ܒܩܣܪܝܐ ܕܩܦܘܕܩܝܐ |
| and those with him / them | ܘܐܝܠܝܢ ܕܥܡܗ / ܘܐܝܠܝܢ ܕܥܡܗܘܢ |
| and his companions | ܘܚܒܪ̈ܘܗܝ |
| who suffered with her | ܘܐܝܠܝܢ ܕܚܫܘ ܥܡܗ |
| Translation of the relics of | ܡܫܢܝܢܘܬܐ ܕܓܪ̈ܡܐ ܕ |
| Uncovering of the relics of | ܫܟܚܬܐ ܕܓܪ̈ܡܐ ܕ |
| Repose of | ܫܟܒܬܐ ܕ |
| Dormition | ܫܘܟܒܐ |
| Glorification of | ܫܘܒܚܐ ܕ |
| Commemoration of | ܕܘܟܪܢܐ ܕ |
| Synaxis of | ܟܢܘܫܝܐ ܕ |
| Dedication of the Church of | ܚܘܕܬܐ ܕܥܕܬܐ ܕ |
| Forefeast of | ܩܕܡ ܥܐܕܐ ܕ |
| Afterfeast of | ܒܬܪ ܥܐܕܐ ܕ |
| Leavetaking of | ܫܘܠܡ ܥܐܕܐ ܕ |
| Sunday of | ܚܕ ܒܫܒܐ ܕ |
| Feast | ܥܐܕܐ |
| Monastery of | ܕܝܪܐ ܕ |
| Kyiv Caves | ܡܥܪ̈ܐ ܕܟܝܒ |
| Kyiv Near Caves / Far Caves | ܡܥܪ̈ܐ ܩܪ̈ܝܒܬܐ ܕܟܝܒ / ܡܥܪ̈ܐ ܪ̈ܚܝܩܬܐ ܕܟܝܒ |
| Mount Athos | ܛܘܪ ܐܬܘܣ |
| the wilderness, the desert | ܡܕܒܪܐ, pl ܡܕܒܪ̈ܐ |
| Island | ܓܙܪܬܐ |
| Lake | ܝܡܬܐ |
| River | ܢܗܪܐ |
| in Baptism N | ܒܡܥܡܘܕܝܬܐ ܢ |
| called also N | ܕܡܬܩܪܝܐ ܐܦ ܢ |

### Where the index's rank and the life's own first words disagree

The Saints index heads some commemorations `ܟܗܢܐ ܣܗܕܐ` whose English
life opens by calling the saint something else, and the difference is not
always a slip in the index: Theodotus of Ancyra is headed a hieromartyr
bishop and his life says in its second sentence that he held no office in
the Church at all and kept an inn; Theodore of Perge is headed the same and
his life calls him a young man taken in the levy of recruits; Zeno of Verona
is headed the same and his life reposes him in peace at Verona. The
vocabulary agrees with the lives in all three - it draws the innkeeper of
Ancyra, the young martyr of Perge and the fisherman-bishop of Verona - so
the rule that the vocabulary stands settles it.

So a life opens with the rank its own English asserts: `ܣܗܕܐ ܩܕܝܫܐ` for
Theodotus and for Theodore, `ܩܕܝܫܐ ... ܐܦܣܩܘܦܐ` for Zeno. The honorific
is the rank, and a rank the entry itself denies is not a rank. The index
heading is not this lane's file and is left as it stands.

### Uglich is spelled two ways and the saint's own entry decides

The town is `ܐܘܓܠܝܟ` in twenty-nine places across the corpus and
`ܐܘܓܠܝܛܫ` in two - and the two are the entry for Seraphim
(Samoilovich) in `data/saint-names.v1.arc.json` and the icon-description of
that same archbishop in the vocabulary. The majority rule would take
`ܐܘܓܠܝܟ`, but a life stands directly beneath the heading the index
prints, and the heading here says `ܐܘܓܠܝܛܫ`; a life that spelled its
saint's see differently from the line above it would read as a mistake in the
place a reader is most likely to notice. So the saint's own entry wins over
the corpus majority, and the rest of the Uglich saints keep `ܐܘܓܠܝܟ`.
The general rule is unchanged: the majority spelling stands where the
commemoration being written does not itself print one.

Where the names table itself wavers, the majority spelling is taken and held:
ܥܐܕܐ (24) over ܥܕܥܕܐ (8) for the feast, ܡܥܪ̈ܐ (85) over ܡܥܪ̈ܬܐ (4) for the
caves, ܫܟܒܬܐ (30) over ܫܘܟܒܐ (3) for the repose. Smyrna is ܙܡܘܪܢܐ (8)
over ܙܡܝܪܢܐ (5), and this one holds against the vocabulary as well as with
it: `tools/saint_terms/arc.py` writes both, giving Polycarp's see one
spelling and Pionius' the other, so there is no single vocabulary reading
for the rule about the vocabulary to prefer. The majority decides, and the
lives are consistent with each other.

### Maximinus is not Maximian, and the corpus had only one word

`tools/saint_terms/arc.py` writes ܡܟܣܝܡܝܢܘܣ four times and every one of
them is Maximian. Maximinus, under whom Lucian of Antioch died at
Nicomedia and Manetha at Caesarea, appears nowhere, and the transliteration
that would fall to him is the one Maximian already holds. Two emperors
under one word in the same index is worse than a compressed vowel, so
Maximinus is **ܡܟܣܝܡܢܘܣ** here and ܡܟܣܝܡܝܢܘܣ stays Maximian's. Maximus,
which the names table already writes ܡܟܣܝܡܘܣ, is untouched by this.

## Three defects found in the published names table

`data/saint-names.v1.arc.json` is not this lane's file and is not edited here.
These are recorded so that the pattern is not copied.

**1. 240 Arabic characters. Not a defect.** Every one of them is U+060C ARABIC
COMMA, in 191 entries, used as the comma. The prayers use the same character
2,465 times and the calendar entries 485 times. Classical Syriac has no comma
of its own in Unicode, and this is the settled convention of the whole corpus.
It is followed here.

**2. 5 Latin characters. A defect.** All five are in one entry:

    "Russian / ROCOR"  ->  "ܪܘܣܝܐ / ROCOR"

A jurisdiction left in Latin script inside the Syriac column, and the only
place in 1,528 entries where the Syriac falls back to the Latin alphabet. It
is not reproduced here; where an abbreviation of this kind is unavoidable the
name is written out in Syriac.

**3. 22 final semkath, in 20 entries. A defect, and one nobody would see.**
U+0724 SYRIAC LETTER FINAL SEMKATH stands where U+0723 SYRIAC LETTER SEMKATH
belongs, word-initially and word-medially: ܡܟܤܐ, ܐܤܘܛܐ, ܤܓܕܬ ܨܠܝܒܐ, ܦܤܩܘܒ
for Pskov, ܐܤܛܪܛܠܛܘܣ, ܬܪ̈ܥܤܪ. The two characters render almost alike in many
fonts, so it survives proofreading; it breaks search and collation, since a
reader searching ܦܣܩܘܒ will not find ܦܤܩܘܒ. The other 3,068 semkaths in the
file are correct. **Only U+0723 is written here.**

## Before writing a batch

- Look the name up in `data/saint-names.v1.arc.json` first. If the
  commemoration is there, its rendering of the name and the place is the one
  to use; the vocabulary file must not invent a second spelling of a saint the
  index already prints.
- Take an ecclesiastical term from `data/glossary-i18n.v1.arc.json`, stripped
  of its vowel points.
- Render what the English entry says and nothing beyond it. No date, relic,
  jurisdiction or episode that is not in the entry.

## The lives

The vocabulary is a table of phrases; a life is prose. What follows is
settled at the head of `tools/saint_lives/arc.py` and is not re-opened.

**Every form the vocabulary already fixed is looked up, not decided again.**
`tools/saint_terms/arc.py` holds all 10,632 names, ranks, places and epithets,
and it renders the icon-description of nearly every commemoration in the
calendar, so a saint's name, his city and his order are read off it before a
line of his life is written. Where it and the names table differ, the
vocabulary stands: it was written against the table with the table open.

**Holy Scripture is quoted, never rendered.** Where a life quotes the New
Testament the verse is taken verbatim from `data/bible.v4.arc.b64` and set in
straight quotes. Two consequences follow from taking it verbatim:

- The Peshitta text there writes final semkath - ܤܓܝܐܐ in John 12:24 - and it
  is kept. The rule against U+0724 governs what this house writes, not what it
  quotes; correcting an edition inside a quotation of it would be worse than
  the inconsistency.
- The `܀` that closes a verse in that edition is a mark of the verse boundary,
  not a word of Scripture, and is dropped where the quotation stands inside a
  sentence. A citation in prose ends at the closing quote.

This site publishes no Old Testament in Syriac. Where a life quotes one, what
the life says about the passage is written as prose and no words are set in
quotation as though they were the received text.

**The same restraint covers the liturgical texts.** The Synodikon of Orthodoxy
is proclaimed in the Church's own books, and no Syriac form of it has been
received by anyone; where a life reports what the rite proclaims, the report
is prose and carries no quotation marks. The Jesus Prayer is the opposite
case and is quoted, because `data/prayers-i18n.v2.arc.json` already publishes
it: ܡܪܝ ܝܫܘܥ ܡܫܝܚܐ ܒܪܗ ܕܐܠܗܐ ܐܬܪܚܡ ܥܠܝ ܚܛܝܐ. Where a life gives only part
of it, the received words are quoted to exactly the point the life stops.

## Ten lives that were filed under the wrong saints

A batch of ten apostles received the ten lives of the batch before it. The
appender zips the blocks of a file against `sorted()` of what is still
unwritten, so a batch file that holds the previous batch's blocks lands
every one of them on the wrong key without a single error: Sosthenes
carried the life of Matthias, Tertius the life of Nathanael, Thaddeus the
life of Nicanor, Timon the life of Onesimus, Timothy the life of Philip,
Titus the life of Pudens, Trophimus the life of Quadratus, John the
Theologian the life of Silas, and the Evangelist Luke the lives of
Silvanus and of Simon the Zealot. Ten saints' lives, each of them true,
each of them under another saint's name.

Nothing in the file said so. The lives were sound Syriac, the counts were
right, `check_register.py` passed, and the register check reads the opening
of a life for its honorific, not for whose life it is. What showed it was
comparing each life against the name the index prints for that
commemoration: ten entries carried no word of their own saint's name, and
ten texts stood in the file twice.

The check is cheap and is worth running after any batch:

    for k, v in LIVES.items():
        n = NAMES.get(k)
        if n and not any(w in v for w in personal_words(n)):
            print(k)

The ten were rewritten from the English and set in place with
`tools/fix_arc_lives.py`, which corrects named entries and refuses a key
the file does not already hold. The appender is right to refuse to
overwrite; correcting a misfiled life is a separate operation and now has
a separate tool.

## Two lanes on this language at once

Syriac is large enough that a spare lane joins it rather than standing idle,
and the two are given opposite ends of the same remaining list: one works
`sorted()` forwards, the other backwards, and they walk towards each other.
`next_job.py` stops sharing the job well before the ends can meet.

**`--from-end` belongs on both halves of the cycle.** It was taught to
`--next` and not to `--append`, so the far lane was shown the last ten names
and would have filed its renderings against the first ten - ten lives landing
silently on ten saints the near lane was writing at that moment, with the
right count, the right script, the right shape and a clean register check.
`append` takes the flag now. On one half alone it files the batch against the
other end of the queue, so keep it on every call.

**A conflict on every push is normal here and is not a merge to resolve by
hand.** Both lanes append immediately before the closing brace of the same
file, so two batches in the same window always collide there. Do not edit the
conflict markers. Take the other lane's file whole, re-run the append onto it,
rebuild, and continue - each batch re-reads the file, so the queue has already
dropped whatever the other lane wrote:

```bash
git checkout --ours tools/saint_lives/arc.py data/saint-lives.v6.arc.json
python3 tools/loop.py lives arc --append batch.txt --from-end
python3 tools/build_saint_lives.py --write
git checkout -- data/saint-lives.v6.hi.json
git add tools/saint_lives/arc.py data/saint-lives.v6.arc.json
GIT_EDITOR=true git rebase --continue
```

Check the pairing before appending, not after. The batch file's blocks are
zipped against the queue in order, so a block that names no word of its own
saint is a batch that has slipped by one:

```python
words = [w.strip('"“”،.') for w in NAMES[key].split() if len(w) > 2]
if words and not any(w in block for w in words):
    print(key)
```

### A heading that stands alone does not outweigh the vocabulary

The index writes Carthage `ܩܪܬܓܢܐ` in Julia's entry and Syracuse
`ܣܝܪܩܘܣܐ` in Lucy's, and nowhere else in the corpus: `ܩܪܛܓܢܐ` stands
thirty times against the one and `ܣܘܪܩܘܣܐ` seven times against the one, and
the vocabulary, writing about these same two saints, uses the majority form
in both. That is the Uglich case reversed. There the divergent spelling had
the vocabulary behind it as well as the heading, and two witnesses carried
it; here the heading stands alone, so the vocabulary stands and the lives
read with the rest of the corpus.

## The builder writes every language, not one

`tools/build_saint_lives.py --write` regenerates the data file of every
language it finds a source for, not only the one just edited. A lane that
runs it and then stages everything commits four or five other languages'
data files along with its own, and on a branch four lanes are pushing to,
that is how one lane's rebuild lands on top of another's newer file. It
happened here: a commit of ten Syriac lives carried bn, hi, hy and ko with
it and stopped on a conflict in the Hindi data.

Nothing was lost - a fresh build afterwards produced no diff, so every
file already matched its source - but the near miss is the point. Stage
the two files this lane owns and nothing else:

    git add tools/saint_lives/arc.py data/saint-lives.v6.arc.json

`git add -A` after a build is the mistake, and it looks like housekeeping.
