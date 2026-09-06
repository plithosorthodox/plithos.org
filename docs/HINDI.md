# Hindi: the register, settled before the writing starts

This is the register document for the Hindi vocabulary in
`tools/saint_terms/hi.py`. It was written before the first batch, and it is
read off what this site has already published in Hindi rather than proposed
from outside. Every rule below is a count, and the count is given, so that a
later reader can check the arithmetic instead of taking the ruling on trust.

The method is the one that took Georgian, Japanese, Swahili, Armenian and
Korean to zero: find the competing forms in the files the site already serves,
count them, and let the larger number decide. Where the count is close, or
where the files invert, the reason for the choice is written out. Nothing here
is settled by ear.

## Whose Hindi this is

The Eastern Orthodox synaxarion in Hindi. That has to be said at the top
because two things will otherwise crowd out the right form in anything written
from memory, and both of them are stronger in Hindi than in most languages on
this site.

**First, Hindi Christian vocabulary is overwhelmingly Protestant and Roman
Catholic.** The Hindi Bible tradition is very old and very large, the
dictionaries follow it, and a search returns it first. It is not always wrong -
this site's own Hindi takes the Bible's proper names from it, and the doc says
so below - but it is not the Orthodox register and it does not decide the
ranks, the Theotokos, or the shape of a Greek saint's name.

**Second, Hindi draws its religious register from Sanskrit, and a word can be
exact and still be wrong.** देवी, देवता, भगवान, ऋषि, मुनि, अवतार, पूजा, आरती
are all available, all precise, and all carry a settled Hindu sense that would
say something this calendar does not mean. The published Hindi on this site
avoids every one of them for a saint or for God: भगवान appears zero times in
100 prayers, and देवी appears in the names table exactly once, inside the
English feast-title Lady Day. Sanskrit is used freely for the *offices* -
महाधर्माध्यक्ष, प्राधिधर्माध्यक्ष, स्वीकारकर्ता - and not for the persons of
the Godhead or for what is worshipped.

So nothing here is written from memory. Where the published files leave a term
unsettled, the doc says so and takes the form nearest the prayers.

## What the site has already written in Hindi

Four bodies, and they are not equal in authority. Where they disagree the
prayers win, because they are the Church's own books; after them the names
table, because it is the largest and it is specifically about how a saint is
named; then the glossary; then the calendar entries.

    data/prayers-i18n.v2.hi.json      100 prayers
    data/saint-names.v1.hi.json     1,528 commemorations
    data/saint-info.v1.hi.json        119 day panels
    data/glossary-i18n.v1.hi.json     177 terms

`data/calendar-names.v1.hi.json` is the same body as the names table with the
month headings added, and is not counted separately.

The order matters here more than it did in Korean, because the four Hindi
files genuinely disagree - on the Theotokos, on the bishop, on the monk, and
on Venerable. Each of those is worked through below rather than waved at.

## Script: Devanagari alone

Devanagari throughout, with no Latin letters in a rendering. This is a count:
of the 1,528 values in the names table, exactly **one** carries a Latin
letter, and it is the jurisdiction label `रूसी / ROCOR`, not a saint.

The appender permits the matras and the virama, which are combining marks
Devanagari cannot be written without. It forbids the en dash, the em dash and
the typographic quotes. Note that the published names table does use curly
quotes - 35 pairs, all around icon epithets - and this lane does not follow it
there: the house rule is straight quotes, and a straight quote is what goes in
this file.

    names table   em dash 0    en dash 0    hyphen 171    danda 0

Hyphens are ordinary in the compounds this vocabulary is full of -
पुरोहित-शहीद, ईश्वर-ग्रहणकर्ता, दुःख-वाहक, सुसमाचार-प्रचारक - and 171 of them
stand in the published table already.

## The names that had to be settled first

Counted in the prayers, which are the Church's own books. The second column is
the whole-word count in the 100 prayers; the third is the same count in the
1,528-entry names table.

| | form | prayers | names | rejected | prayers |
|---|---|---|---|---|---|
| Christ | मसीह | 136 | 29 | ख्रीस्तोस, क्राइस्ट | 0 |
| Jesus | यीशु | 84 | 11 | ईसा, येसु | 0 |
| God | परमेश्वर | 370 | 12 | भगवान, खुदा | 0 |
| Lord | प्रभु | 554 | 43 | | |
| Holy Spirit | पवित्र आत्मा | 66 | | रूह | 0 |
| Theotokos | ईश्वरमाता | 28 | 11 | थियोटोकोस | 9 |
| a saint | संत | 22 | 392 | | |
| holy | पवित्र | 351 | 92 | | |

Hindi does not take the Greek form of the Lord's name the way Japanese takes
ハリストス. मसीह and यीशु are what the prayers print, 136 and 84 times against
nothing. ईसा, which a reader might expect from Urdu and from Indian Muslim
usage, appears in the Hindi of this site only inside ईसाई, "Christian".

**God is परमेश्वर, not ईश्वर, standing alone.** 370 to 0 in the prayers. This
one needs care because the names table inverts it - ईश्वर 37, परमेश्वर 12 -
and the inversion is not a disagreement but a difference of position: every
one of those 37 is compound-initial, ईश्वरमाता, ईश्वर-ग्रहणकर्ता,
ईश्वरवाहक, ईश्वर-माता. So:

  - **परमेश्वर** where the word stands alone or takes a postposition.
  - **ईश्वर-** as the first member of a compound, unspaced or hyphenated as
    the published compound already is.

प्रभु is the Lord, 554 times, and is not interchangeable with either: it
renders Κύριος and stands wherever the English says Lord.

**The Theotokos is ईश्वरमाता.** This is the one ruling in the document where
the files most disagree, so the whole tally is given.

    prayers    ईश्वरमाता 28   परमेश्वर की माता 12   थियोटोकोस 9   ईश्वर की माता 0
    names      ईश्वर-माता 18  ईश्वरमाता 11   ईश्वर की माता 11   परमेश्वर की माता 11   थियोटोकोस 6
    glossary   थियोतोकोस (the headword, glossing the Greek)

The names table is split four ways and settles nothing on its own. The prayers
are not split: ईश्वरमाता wins them more than two to one over its nearest
competitor and is the only form of the four the prayers prefer. So ईश्वरमाता
is what this lane writes, unhyphenated, and परम पवित्र ईश्वरमाता renders Most
Holy Theotokos (परम पवित्र stands 45 times in the prayers). थियोटोकोस is left
to the glossary, where it explains the Greek word; it does not stand in a
saint's name written by this lane.

## How a foreign saint's name is transcribed

From the Greek or Latin, in the shape the names table already uses, and NOT
through English - except for the Bible's own people, who keep the form the
Hindi Bible gives them. The table has 1,528 renderings already and the rule is
read off them.

**A masculine name in -ius / -us takes -युस.** This is the single most
consequential rule in the document, and among the long tokens of the names
table -युस is the commonest ending there is:

    -युस  313 tokens

Worked through: Ignatius इग्नातियुस, Sergius सर्गियुस, Theodosius
थियोदोसियुस, Photius फोतियुस, Anastasius अनास्तासियुस, Dionysius दियोनुसियुस,
Athanasius अथानासियुस, Macarius मकारियुस, Demetrius देमेत्रियुस, Eugenius
एउजेनियुस, Theopemptus थेओपेम्प्तुस, Stratonicus स्त्रातोनिकुस.

Three correspondences fall out of the same list and are worth stating so they
are not re-decided per name:

  - **θ / Th- is थ**: थियोडोर, थियोदोसियुस, अथानासियुस, थेओपेम्प्तुस. Not ट.
  - **A Greek initial cluster keeps its shape**: स्त्रातोनिकुस, स्तेफन,
    स्तुदिओन. Not the English स्ट्रै-.
  - **c before a back vowel is क, not स**: मकारियुस, निकोलस, कुस्तुंतुनिया.

**The Bible's own people keep the Hindi Bible's form.** This is not an
inconsistency; it is what the table does, and a reader of Hindi Scripture
would not recognise a Greek-shaped Peter.

    पतरस    Peter, the Apostle          12
    पौलुस   Paul                        17
    यूहन्ना John                        66
    लूका    Luke        मरकुस  Mark     शिमौन  Simeon
    मरियम   Mary        अन्ना  Anna     हन्ना  Hannah
    एलिय्याह Elijah     दाऊद   David    तबीता  Tabitha

A later Peter who is not the Apostle takes the Greek shape पेत्रुस (8 in the
table: the Aleut, the presbyter of Phoenicia, the archbishop of Alexandria).
Where the published table has already made the choice for a given saint, that
choice stands and is not revisited.

**A saint long known in Hindi by an anglicised form keeps it.** The table does
this deliberately and consistently for the Western and the very famous:
निकोलस, जॉर्ज, ग्रेगोरी, बेसिल, सिरिल, कॉन्स्टेंटाइन, हेलेना, बारबरा,
क्रिस्तोफर, पैट्रिक, बीड. This lane does not re-Hellenise them.

**A place-name follows the published table**: कुस्तुंतुनिया Constantinople,
सिकंदरिया / अलेक्जेंड्रिया Alexandria, अंताकिया Antioch, यरूशलेम Jerusalem,
मिस्र Egypt, कीव Kyiv, मास्को Moscow, एथोस पर्वत Mount Athos, फारस Persia,
फ़िलिस्तीन Palestine, नोवगोरोद Novgorod, रोस्तोव Rostov, दमिश्क Damascus,
थेस्सलुनीके Thessalonica, सीरिया Syria, रोम Rome, बुल्गारिया Bulgaria.

## Word order

Hindi puts every modifier before its head, and the published table does this
without exception. **The place comes first, in the genitive, then the rank,
then the name.**

    Saint Nicholas of Myra              मीरा के संत निकोलस
    St Raphael, Bishop of Brooklyn      ब्रुकलिन के संत राफेल, बिशप
    Venerable Peter of Mount Athos      एथोस पर्वत के आदरणीय पतरस
    Hieromartyr Peter, Archbishop
      of Alexandria                     अलेक्जेंड्रिया के महाधर्माध्यक्ष
                                        पुरोहित-शहीद पेत्रुस
    Venerable Euphrosyne, Abbess
      of Polotsk                        पोलोत्स्क की मठाधीशा आदरणीय एवफ्रोसिने

The genitive postposition agrees with the head it governs, so it is का / के /
की and not one invariable form: पोलोत्स्क **की** मठाधीशा but एथोस पर्वत **के**
आदरणीय. Getting this wrong is the commonest way a Hindi rendering announces
that it was assembled rather than written.

A feast is likewise possessed and not prefixed: मसीह का जन्म, मसीह का
पुनरुत्थान, संत यूहन्ना अग्रदूत का जन्म, ईश्वरमाता की शुभसूचना.

The English keys in this queue are very often fragments that begin mid-phrase -
`of Egypt`, `(Vadim) of Persia`, `the Confessor, Bishop of Bithynia`. A
fragment is rendered as the fragment it is, in Hindi's own order, and not
padded out into a sentence.

## Register: the honorific is the rank

संत is not given to everyone. The names table carries the rank as the
honorific, and a saint's own order is the word that stands before the name.
Counted in the names table, with the calendar entries alongside where they
differ:

| English | Hindi | names | note |
|---|---|---|---|
| Saint | संत | 392 | may stand before a name; see below |
| Holy | पवित्र | 92 | attributive, before a rank or a feast |
| Venerable | आदरणीय | 385 | the monastic |
| Martyr | शहीद | 470 | |
| Great-martyr | महान शहीद | 25 | |
| Hieromartyr | पुरोहित-शहीद | 85 | याजक शहीद 4, not followed |
| New Martyr | नवशहीद | 12 | |
| Virgin-martyr | कुँवारी शहीद | | कुँवारी 34 in prose |
| Monastic Martyr | मठवासी शहीद | | |
| Confessor | स्वीकारकर्ता | 40 | |
| Righteous | धर्मी | 35 | |
| Blessed | धन्य | 20 | 62 in the prayers |
| Prophet | भविष्यवक्ता | 26 | भविष्यद्वक्ता 5, not followed |
| Prophetess | भविष्यवक्त्री | 3 | |
| Apostle | प्रेरित | 70 | प्रेरितों (oblique plural) 59 |
| Equal-to-the-Apostles | प्रेरितों के समतुल्य | | follows the name |
| Wonderworker | चमत्कारी | 56 | attributive, before the name |
| Wonderworker (noun) | चमत्कारकर्ता | 10 | in apposition after it |
| Unmercenary | निःशुल्क चिकित्सक | | |
| Fool-for-Christ | मसीह के लिए मूर्ख | | follows the name |
| Passion-bearer | दुःख-वाहक | | |
| Forerunner | अग्रदूत | 12 | |
| Evangelist | सुसमाचार-प्रचारक | 6 | |
| Archangel | महादूत | 4 | |
| Bishop | बिशप | 160 | धर्माध्यक्ष 3; see below |
| Archbishop | महाधर्माध्यक्ष | 49 | |
| Metropolitan | महानगराध्यक्ष | 18 | |
| Patriarch | प्राधिधर्माध्यक्ष | 21 | कुलपति 5, not followed |
| Abbot | मठाधीश | 93 | |
| Abbess | मठाधीशा | 4 | |
| Archimandrite | आर्किमंड्राइट | 6 | the names table spells it so; no rival form |
| Presbyter, Priest | पुरोहित | 99 | प्रेस्बिटर 7 where the English says Presbyter of a Greek |
| Deacon | डीकन | 16 | |
| Monastic, monk | मठवासी | 22 | attributive |
| Ascetic | तपस्वी | 12 | |
| Hermit | वैरागी | 14 | |
| Recluse | एकांतवासी | 21 | |
| Stylite | स्तंभवासी | 9 | |
| Prince | राजकुमार | 45 | राजकुमारी 11 |
| Emperor | सम्राट | 15 | साम्राज्ञी for the empress |

Three of these are contested between files and are settled here once:

**Venerable is आदरणीय, not वंदनीय.** The names table says आदरणीय 385 times
against 2, and the prayers say आदरणीय 14 times against 0. The calendar entries
invert it - वंदनीय 47 - but they are 119 entries against 1,528 and they are
the weakest of the four bodies. आदरणीय is what this lane writes. वंदनीय is not
wrong Hindi and the calendar's use of it is left alone; it is simply not the
form this vocabulary adds to.

**The bishop is बिशप, not धर्माध्यक्ष.** 160 to 3 in the names table, which is
the table about how a saint is named. The glossary prefers धर्माध्यक्ष (14),
and rightly, because the glossary is defining the office rather than naming a
man; and महाधर्माध्यक्ष stands unchallenged for the archbishop, 49 to 0, so
the Sanskrit compound is not being avoided. It is a difference of surface, and
this lane writes names.

**The monk has three words and they are not synonyms.** मठवासी is the
attributive, before a rank (मठवासी शहीद, 22); तपस्वी is the ascetic (12);
भिक्षु is the noun for a monk standing alone (4, and 8 in the calendar
entries). संन्यासी is the glossary's word (10) and carries a Hindu sense this
calendar does not want in a saint's name; it is not written here.

**संत may stand before a name.** Hindi is like Greek, Romanian, Georgian,
Armenian and Serbian in this and unlike Russian: संत निकोलस is what the table
prints, 392 times, and it gives no offence. So `strict` stays False in
`tools/check_register.py` and only the monastic rule is asserted there - a
monastic is आदरणीय, never merely संत.

## Prose register

The iconography descriptions in this queue are prose, not labels, and the
nearest published Hindi prose about the same saints is the `life` field of
`data/saint-info.v1.hi.json`. That is the register they follow: plain,
unornamented खड़ी बोली, Sanskritic where the Church's own offices are
Sanskritic and ordinary everywhere else. Not the high literary register, and
not Hindustani-Urdu.

The descriptions are noun phrases in the English - "A Roman general in armor
holding a cross, his soldiers behind him, a spring at his feet." Hindi renders
them as what they are: a headed noun phrase with its modifiers before it, the
appositive clauses following in order, and the verb only where the English has
one.

Render what the English entry says and nothing beyond it. No date, relic,
jurisdiction or episode is added that the key does not carry.

## Punctuation

**Prose takes the danda, `।`.** The calendar entries use it 356 times and the
full stop zero times; the glossary uses it 207 times and the full stop zero.
So an iconography sentence ends in `।`.

The prayers are the exception and are not the model here: they use the full
stop 1,869 times, because they are set as verse lines and short responses. The
prose bodies are unanimous the other way, and the iconography descriptions are
prose.

A phrase that is not a sentence takes no terminal punctuation at all, which is
what the names table does 1,528 times over.

    straight quotes, never typographic
    hyphens, never en or em dashes
    the interpunct · only where the site already uses it, in a rank chip
    Devanagari digits are not used: the table writes 351, 1860, 1961

## What a script can catch

`tools/check_register.py` is given a `hi` entry before the first batch, not
after. It asserts the one rule a script can assert: a monastic saint is
आदरणीय, and is not introduced by संत alone. The rank stems in that entry carry
no postposition, because Hindi puts the postposition after the noun and a bare
stem matches every case of it.

`python3 tools/build_saint_terms.py --check` is run after every batch. It
reports the count and it catches a rendering attached to the wrong key, which
is the failure this file is shaped to make impossible: the keys are the
English phrases exactly as the index writes them.

## The trap

The trap in Hindi is that every wrong choice available is a real Hindi word,
correctly spelled, and often the more elegant one. भगवान is better Hindi than
परमेश्वर by any literary measure. देवमाता is a more graceful compound than
ईश्वरमाता. संन्यासी is warmer than मठवासी. ईसा is what half of India calls
him. Every one of them would be a different religion's word doing this
calendar's work, and none of them appears in the Hindi this site has already
published.

So the discipline is the one at the top of this document: read what the
prayers say, count it, and follow the count.

## Where a hymn is the subject of the entry

The rule is that Holy Scripture, the Divine Liturgy and the other liturgical
texts are not rendered here. In the lives that means naming a hymn rather than
reproducing it: the kontakion of the Akathist that Cyril of White Lake heard,
the Song of the Three Youths, the fleece verse of the Entry canon, and the
kontakion Romanos the Melodist sang at the Nativity vigil all stand named and
undescribed in the Hindi.

The one entry that goes the other way is the icon called हे सर्वस्तुत्य माता,
where the hymn is not quoted in the life but is the icon's name, and the entry
exists to say where that name came from. There the thirteenth kontakion of the
Akathist is rendered, because naming it without its words would leave the entry
saying nothing. That is not a reading of the rule; it is what this site already
publishes, in eighteen languages, in this very entry.

Scripture has no such exception. Every verse quoted in the Hindi lives is taken
from the editions this site publishes, `data/bible.v4.hi.b64` and
`scripture/hi/<n>.json`, and where the excerpt can be cut at a clause boundary
it is cut there, so that the published punctuation carries through without a
dash. Where a published verse writes याहवेह, or पेतरॉस, or बंटवारा for the
sword, the quotation keeps it and the surrounding prose does not.

## Two lanes on this list

Hindi is worked from both ends at once: one lane takes `sorted()` forwards,
the other backwards, and `next_job.py` stops sharing the job well before the
ends can meet.

**`--from-end` belongs on both halves of the cycle.** The batch command the
queue prints carries it on `--next` and omits it on `--append`, so the far
lane is shown the last ten names and files its renderings against the first
ten - ten entries landing silently on ten saints the near lane is writing at
that moment, with the right count, the right script, the right shape and a
clean register check. That happened here once and was caught only by reading
the diff. Put the flag on the append as well:

```bash
python3 tools/loop.py info hi --append batch.txt --from-end
```

Read the keys the append reports before committing. `git diff` names them,
and ten wrong keys look exactly like ten right ones until it is read.

**A conflict on every push is normal and is not a merge to resolve by hand.**
Both lanes append immediately before the closing brace of the same file, so
two batches in the same window always collide there. Take the other lane's
file whole and re-run the append onto it; each batch re-reads the file, so
the queue has already dropped whatever the other lane wrote.

## The type line

The type line is the index speaking, not the entry, so it renders the English
word the index carries and not the word the saint's life would suggest. The
same icon of the Mother of God appears in these pages as Saint, as Feast, as
Icon and as Icon of the Mother of God, and each is rendered as it stands.

Words settled while writing the entries, where the vocabulary above had no
row for them:

| English | Hindi | why |
|---|---|---|
| Icon | प्रतिमा | the lives write प्रतिमा throughout; छवि is the second mention, not the head word |
| Icon of the Mother of God | ईश्वर-माता की प्रतिमा | |
| Nun | भिक्षुणी | the feminine of भिक्षु, which the lives already use of a nun |
| Nun-martyr | भिक्षुणी-शहीद | on the pattern of पुरोहित-शहीद |
| Monastics (of a household) | मठवासीगण | on the pattern of शहीदगण, which the file uses for a company |
| Hieromonk | भिक्षु-पुरोहित | already in the file, in a patron line |
| Recluse | एकांतवासी | from the rank vocabulary |
| Hermit | वैरागी | from the rank vocabulary |

Centuries are spelled out and never given in digits: आठवीं, नौवीं, दसवीं,
ग्यारहवीं, बारहवीं, तेरहवीं, चौदहवीं, पंद्रहवीं, सोलहवीं, सत्रहवीं,
अठारहवीं, उन्नीसवीं, बीसवीं.

## Where the English stops mid-clause

A number of the short English lives end at a semicolon and a full stop
together, or break off inside a phrase - "carried to the threshold.",
"his soldiering, and the injury", "for their parish church of the
Resurrection;." The Hindi cuts at the last clause boundary the English
actually reached and ends it with a danda. It does not finish the sentence
from the long life, because the short life is the day panel's and its length
is the English entry's decision; and it does not carry the broken punctuation
over, because that is the index's defect and not the edition's reading.

Where a title and its life disagree on a name - Alexandria's company is
headed Theodora and its life names Theodosia - the life decides, and nothing
is added either way.

Later additions to the type table, settled the same way:

| English | Hindi | why |
|---|---|---|
| Schemamonk | श्रेणी-भिक्षु | the lives already use it of the great schema |
| Monk, Elder | भिक्षु, वृद्ध | वृद्ध is the elder throughout the lives, never बुज़ुर्ग |
| Monk, former Great Zhupan | भिक्षु, पूर्व महान ज़ुपान | the Serbian title is transcribed, not translated |
| Fool-for-Christ | मसीह के लिए मूर्ख | already in the file |
| Stylite | स्तंभवासी | from the rank vocabulary |

## Perm pavitra: the spacing of the Theotokos' title

The site writes the title both ways, `परम पवित्र ईश्वरमाता` and
`परमपवित्र ईश्वरमाता`, and has done since before this work began: 53 of the
first against 60 of the second across the vocabulary, the names table, the
lives and the entries. The vocabulary file settles it, as it settles every
other split, and it carries eleven of the spaced form and none of the closed
one. **New writing uses `परम पवित्र`.**

What is already written stays. The split runs through the lives as well as the
entries, so normalising one file would not make the site consistent; it would
only move the seam, and the two files are being written by two lanes at once.
The form is settled for what is written from here, which is what a ruling is
for.

| Laywoman | सामान्य विश्वासिनी | the lives already write सामान्य विश्वासी of a layman; the feminine is marked, as it is on तपस्विनी and भिक्षुणी |
| Venerable (as a type of its own) | आदरणीय | Mary of Egypt carries it as her whole type |
| Anchorite | निर्जनवासी | kept apart from एकांतवासी, which is Recluse; the lives use both and mean different things by them |
| Monk, Hymnographer | भिक्षु, भजनकार | भजनकार is the hymnographer in the lives; भजन-रचयिता is used in patron lines |
