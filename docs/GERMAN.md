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
- **A stray mark that is not a letter**: a stress mark, a soft hyphen, an
  accented Latin letter standing in for a plain one. The same scan as
  Ukrainian's, minus the Cyrillic clause.

```bash
python3 -c "
import io, unicodedata as U
s = io.open('tools/saint_lives/de.py', encoding='utf-8').read()
odd = sorted({c for c in s if U.combining(c)}
             | {c for c in s if ord(c) == 0xad}
             | {c for c in s if c == chr(0xdf)})
print([hex(ord(c)) for c in odd])
"
```

## The order of work

| | where it is written | what publishes it |
|---|---|---|
| the names | already done, 1,528 | `tools/build_saint_names.py` |
| the vocabulary | `tools/saint_terms/de.py` | `tools/build_saint_terms.py` |
| the lives | `tools/saint_lives/de.py` | `tools/build_saint_lives.py` |
| the calendar entries | `tools/saint_info/de.py` | `tools/saint_info_i18n.py` |

## The trap at the end

`data/saint-lives.v5.*` and `data/saint-terms.v4.*` are the names the Saints
page fetches now. They are rewritten under the same name every sitting, so
when German is finished both must move to a fresh version, exactly as
Ukrainian's did. See the closing section of `docs/UKRAINIAN.md`, which
records why, and why `/data/saint-lives.*` must stay out of `_headers`.

## Then

Serbian, Arabic, Georgian; then es, fr, it, pt; then sw, ja, ko, zh;
then hy, arc, hi, bn, ur.
