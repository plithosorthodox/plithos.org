# German: the register, settled before the writing starts

German is the fifth language on the Saints page, after Russian, Greek,
Romanian and Ukrainian. It is the first that is not a Slavonic or Greek
language, and the first written for a Church that received Orthodoxy in
translation rather than in her own tongue, so the question it raises is
different from the one the first four raised.

## The German is not the Latin

The failure to guard against is not the one Ukrainian was exposed to. There
is no neighbouring language whose forms will creep in unnoticed. The German
danger is Western church vocabulary, which is at hand for every word and
carries a different Church behind it.

- **Kirchenvater, not Kirchenlehrer.** *Doctor of the Church* is a Roman
  category with a list; the Fathers are not on it.
- **Ehrwürdig, not selig.** *Selig* renders the Roman *beatus*, one step
  below canonisation. In Orthodox German it is the word for the blessed
  fools and for the departed, not a degree.
- **Gottesgebärerin**, not *Muttergottes* alone, where the Theotokos is
  named as such. Both are said in German; the first is what the Council of
  Ephesus said.
- **Entschlafung**, not *Himmelfahrt Mariens*. The Dormition is a falling
  asleep. The Assumption is a Roman dogma of 1950 and is a different claim.
- **Göttliche Liturgie**, not *Messe*.
- **Fasten** as the Church's, not *Fastenzeit* used only of Lent.
- **Ikone**, not *Heiligenbild*.
- **Presbyter or Priester**, not *Pfarrer*, which is an office in a parish
  register.

Where a German Orthodox jurisdiction has settled a word, that word is used.
The German-speaking Orthodox have their own liturgical books and their own
usage; this is not a field where the site invents.

## The honorific

German does what Greek and Romanian do and Russian does not: **der heilige
Nikolaus** is ordinary German and gives no offence. So only one distinction
is asserted here, and it is the one German Orthodox usage actually keeps:

| the calendar's rank | German | note |
|---|---|---|
| Venerable (monastic) | **der ehrwürdige** Vater N. | never merely *heilig* |
| Saint (bishop) | der heilige Hierarch N. | or *Erzbischof*, *Bischof* |
| Martyr | der heilige Märtyrer N. | *Märtyrerin* |
| Great Martyr | der heilige Großmärtyrer N. | |
| Hieromartyr | der heilige Priestermärtyrer N. | |
| Monk-martyr | der heilige Mönchsmärtyrer N. | *Nonnenmärtyrerin* |
| Apostle | der heilige Apostel N. | |
| Prophet | der heilige Prophet N. | *Prophetin* |
| Confessor | der heilige Bekenner N. | |
| Righteous | der heilige Gerechte N. | |
| Blessed, fool | der selige N., Narr um Christi willen | |
| Unmercenary | der heilige uneigennützige Arzt N. | |
| Equal-to-the-Apostles | der heilige apostelgleiche N. | |
| Passion-bearer | der heilige Passionsträger N. | |
| Stylite | der heilige Stylit N. | *Säulensteher* |
| Right-believing prince | der heilige rechtgläubige Fürst N. | |
| Forefather | der heilige Altvater N. | |

`tools/check_register.py --lang de` asserts the monastic rule and nothing
else, exactly as it does for Greek and Romanian:

```bash
python3 tools/check_register.py --lang de
```

Run it on every sitting, not at the end. That is the whole lesson of the
first four languages.

## Spelling

**No ß.** The house rule is straight quotes and no dashes but hyphens; the
German equivalent is that the site writes *ss*, because the pages are read
in Switzerland as well as in Germany and Austria, and *Grossmärtyrer* is
correct in all three while *Großmärtyrer* is correct in two. Umlauts are
written as umlauts and never as *ae, oe, ue*.

Otherwise the house text rules hold as everywhere: hyphens rather than
dashes, straight quotes, one blank line between paragraphs. German
quotation marks are not used; the site uses none, because it quotes by
indentation.

## Cyrillic is transliterated the German way, not the English

This is the decision that touches the most lines, so it is settled here
rather than discovered halfway through. German-language Orthodox books write
**Sergij von Radonesch** and **Serafim von Sarow**, not Sergius of Radonezh
and Seraphim of Sarov. The site follows them, because a German reader
sounding out *Radonezh* gets a word that is neither German nor Russian.

The scheme is the ordinary German one:

| Cyrillic | German | | Cyrillic | German |
|---|---|---|---|---|
| в | w | | х | ch |
| з | s | | ц | z |
| ж | sch | | ч | tsch |
| ш | sch | | щ | schtsch |
| с between vowels | ss | | ы | y |
| й | i | | э | e |
| ю | ju | | я | ja |
| ё | jo | | е after a vowel | je |

So Белозерск is **Belosersk**, Брянск is **Brjansk**, Боровичи is
**Borowitschi**, Боголюбово is **Bogoljubowo**, Чернигов is
**Tschernigow**, Киев is **Kiew**, Москва is **Moskau**.

Greek and Latin place-names take the German form where German has one -
Ankyra, Antiochien, Nikomedien, Thessaloniki, Adrianopel, Kleinasien - and
are otherwise transliterated from the Greek rather than passed through the
English: Amaseia, Anazarbos, Arianzos, not Amasea, Anazarbus, Arianzus.

## What a script can catch in a German value

Very little, which is why the reading matters more here than it did for the
Slavonic languages. There is no alphabet test: German shares its letters
with English, so a sentence left in English is invisible to a scan. The
checks that do work:

- **ß anywhere in a value** is a house-rule violation and is catchable.
- **A value identical to its English key's text** means nothing was written.
- **A Greek or Cyrillic letter.** German is written in Latin letters only,
  so a single Cyrillic character means a name was transliterated by eye from
  a Russian source and one letter was never touched. This is not theoretical:
  a Cyrillic **о** stood inside *Scheleso* in the baptismal names and is
  invisible on the page, in a diff, and in every editor.
- **A stray mark that is not a letter**: a stress mark, a soft hyphen, an
  accented Latin letter standing in for a plain one.

```bash
python3 -c "
import io, unicodedata as U
s = io.open('tools/saint_lives/de.py', encoding='utf-8').read()
odd = sorted({c for c in s if U.combining(c)}
             | {c for c in s if ord(c) == 0xad}
             | {c for c in s if c == chr(0xdf)}
             | {c for c in s if 0x370 <= ord(c) <= 0x4ff})
print([(hex(ord(c)), U.name(c, '?')) for c in odd])
"
```

## The order of work

| | where it is written | what publishes it | where it stands |
|---|---|---|---|
| the names | in `NAMES_I18N`, `index.html` | `tools/build_saint_names.py` | 1,528 of 1,528 |
| the vocabulary | `tools/saint_terms/de.py` | `tools/build_saint_terms.py` | 10,632 of 10,632 |
| the lives | `tools/saint_lives/de.py` | `tools/build_saint_lives.py` | 93 of 1,456 |
| the calendar entries | `tools/saint_info/de.py` | `tools/saint_info_i18n.py` | not begun |

The vocabulary was written field by field in the order the builder reports
them - the names and titles, the places, the origins, the relics, the
patronage, the baptismal names, the kindred commemorations, and last the
icons, which are a third of the whole. Each field's phrases were taken from
the index itself rather than from a list made by hand, so nothing could be
missed and nothing invented; `tools/build_saint_terms.py --check` is the
count, and it is the only count.

The lives are the long part. There are 1,456 of them and they run to
397,364 English words, so this is several sittings' work and was several
sittings' work in every language before it. They are written in the order
the index lists them, eight to a commit, and the checks below are run after
every batch, not at the end.

One note on the character scan: run it over the **values** and not the whole
file. Several of the English keys carry Greek letters, because the index
spells some names that way - `Apostle Epίmakhos of Alexandria` - and a scan
of the file reports them as strays in a language that has none.

```bash
python3 -c "
import sys, unicodedata as U
sys.path.insert(0, 'tools/saint_lives'); import de
print(sorted({hex(ord(c)) for v in de.TEXT.values() for c in v
              if U.combining(c) or ord(c) == 0xad or c == chr(0xdf)
              or 0x370 <= ord(c) <= 0x4ff}) or 'clean')"
```

`check_register.py --lang de` reports one saint under review and should:
Cornelius of the Pskov Caves is typed *Venerable* in the index, but the
commemoration is his beheading and both the English and the German open him
as **Priestermärtyrer**, which is what the Church calls him.

## The house spelling on the calendar

The German names and copy in `index.html` were written before the register
was settled and carried the sharp s throughout, along with six long dashes.
`tools/de_house_spelling.py` brought them to the house spelling in one pass;
run it again if German is ever added by a hand that has not read this file.
It deliberately leaves `library.html` alone, whose German is the Divine
Liturgy and is reproduced as its translator set it.


## How to run the loop, so that it does not stop

This is written down because the vocabulary was written in far more sittings
than it needed, and the lives in far fewer, and the difference was not the
work but the shape of the loop.

The lives run well because the English was frozen to a static file once, in
the order the index lists them. A batch is a slice, the next slice is known
without recomputing anything, and so the call that writes batch N can also
print batch N+1. Nothing comes back that has to be read before continuing.

The vocabulary ran badly because the remaining work was derived from the
module after every write - import the file, expand the generated phrases,
diff against the todo. That makes each batch depend on the result of the one
before it, and every dependency is an invitation to stop and look.

So, before the first batch of anything:

1. **Freeze the work list.** Write the remaining phrases, in order, to one
   JSON file in the scratchpad. Slices are then deterministic.
2. **Match the dump to the write.** Print exactly as many entries as the next
   batch will translate. A dump of a hundred and thirty against a batch of
   fifty-five forces a re-sync every time.
3. **Build the crib sheet once.** One pass that pulls every German form
   already settled - the places, the honorifics, the icon types, the feast
   names - into a file to consult. The per-batch grep for how a town was
   spelled last time is what generated most of the stops.
4. **Pipeline the call.** One invocation appends the batch, runs the count,
   runs the character scan, commits, pushes, and prints the next batch.

And the rule the other four exist to serve: a batch ending is not a reason to
stop. The count rising and the scan coming back clean is the loop holding, not
news. Stop for a failed check, for an editorial fork that precedent cannot
settle, or for the end of the room - and for nothing else.

## The trap at the end

`data/saint-lives.v5.*` and `data/saint-terms.v4.*` are the names the Saints
page fetches now. They are rewritten under the same name every sitting, so
when German is finished both must move to a fresh version, exactly as
Ukrainian's did. See the closing section of `docs/UKRAINIAN.md`, which
records why, and why `/data/saint-lives.*` must stay out of `_headers`.

## Then

Serbian, Arabic, Georgian; then es, fr, it, pt; then sw, ja, ko, zh;
then hy, arc, hi, bn, ur.
