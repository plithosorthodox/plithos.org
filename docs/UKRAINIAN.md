# Ukrainian: the register, settled before the writing starts

Working notes. Not deployed.

Ukrainian is the fourth language on the Saints page, after Russian, Greek and
Romanian. It is being begun the way `CLAUDE.md` now requires: the rank
vocabulary is fixed first, and `tools/check_register.py` already carries the
Ukrainian entry, so the honorific cannot drift for a thousand entries before
anyone notices.

## What the previous three taught

The defect that had to be swept out of all three finished languages was one
defect wearing three coats: the English word *Saint* rendered as though it
were a title, when in Slavonic-tradition languages the title is the saint's
**rank** and the rank is the honorific. Russian needed 85 corrections,
Romanian 290, Greek about 400. None of it was catchable by spelling; every
word was correct and no native speaker would have written the sentence.

Ukrainian inherits the same grammar of sanctity as Russian, so it is exposed
to exactly the same failure, and more insidiously - because Ukrainian is
close enough to Russian that a rendering can be right in Russian and merely
Russian-shaped in Ukrainian.

## The orders, and what each obliges

Written before the first life, not discovered during it.

| the calendar's rank | Ukrainian | note |
|---|---|---|
| Monastic, Monk, Abbot, Hermit | **преподобний** / преподобна | never святий |
| Bishop, Archbishop, Metropolitan | **святитель** | |
| Hieromartyr | **священномученик** | a priest martyred as a priest |
| a martyred monastic | **преподобномученик** | built on the monastic stem |
| Martyr | **мученик** / мучениця | |
| Great Martyr | **великомученик** | |
| Prince, Princess | **благовірний князь** / благовірна княгиня | |
| Passion-bearer | **страстотерпець** | |
| Righteous | **праведний** / праведна | |
| Fool-for-Christ | **блаженний**, Христа ради юродивий | |
| Unmercenary | **безсрібник** | |
| Confessor | **сповідник** | |
| Equal-to-the-Apostles | **рівноапостольний** | |
| Apostle | **апостол** | святий апостол, never святий + name |
| Stylite | **стовпник** | |
| Recluse | **затворник** | |

The bare word **святий** stands before a rank, never before a name.
`святий апостол Андрій` is right; `святий Андрій` is the English sentence in
Ukrainian words.

## Where Ukrainian is not Russian

The trap in this particular language is that a Russian rendering will look
almost right. It is not enough to avoid Russianisms in spelling; the
vocabulary of the Church differs at points where the eye slides past.

- **Церква, not Церков.** Ukrainian declines it as Церкви, Церкві.
- **обитель** and **монастир** both serve; **лавра** for the great houses.
- **Києво-Печерська лавра**, and its fathers are **печерські**.
- **чернець** for a monk where Russian has инок; **чернецтво** for the life.
- **сповідник**, not исповедник; **безсрібник**, not бессребреник.
- **Пресвята Богородиця**; the feast is **Успіння**, not Успение.
- **владика** for a hierarch addressed, **святитель** for one commemorated.
- Placenames take their Ukrainian forms: **Київ, Чернігів, Волинь,
  Переяслав, Царгород** for Constantinople in the older register beside
  Константинополь.
- Patronymics and princely names in their Ukrainian shape: **Володимир**,
  **Ярослав**, **Всеволод**, **Ольга**, **Борис і Гліб**.

## The order of work

Vocabulary, then the lives, then the calendar entries - the order Romanian
took, because the vocabulary is what a reader meets first and it stands
beside every card on the page.

| what | written in | built by |
|---|---|---|
| the names | already done, 1,528 | `tools/build_saint_names.py` |
| the vocabulary | `tools/saint_terms/uk.py` | `tools/build_saint_terms.py` |
| the lives | `tools/saint_lives/uk.py` | `tools/build_saint_lives.py` |
| the calendar entries | `tools/saint_info/uk.py` | `tools/saint_info_i18n.py` |

## Checking as it goes

```bash
python3 tools/check_register.py --lang uk
python3 tools/build_saint_terms.py --check
```

The register check is run on every sitting, not at the end. That is the whole
lesson of the first three languages.

## What a script can catch in a Ukrainian value

The register check reads the openings of the calendar entries and the lives.
It cannot see the letters. Two other kinds of fault get into a Ukrainian
value and neither is visible on the page:

- **A Russian letter.** `ы`, `э`, `ъ` do not exist in Ukrainian, and their
  presence means a Russian rendering was copied across. This is the failure
  this language is most exposed to and the only part of it a script can see.
- **A mark that is not a letter.** A stress mark (`Вéрка`, `Всеспівано́ї`),
  a soft hyphen inside a word, or an accented Latin letter standing in for a
  Cyrillic one. The site sets no accents; a combining mark is not caught by
  `isalpha`, and a soft hyphen is invisible in every editor.

Both slipped in once each while the vocabulary was being written, and both
were found by inspection rather than by the check. The batch helpers now
refuse a value carrying any of them, and the same scan is worth running over
the whole file before a language is published:

```bash
python3 -c "
import io, unicodedata as U
s = io.open('tools/saint_lives/uk.py', encoding='utf-8').read()
odd = sorted({c for c in s if U.combining(c)}
             | {c for c in s if ord(c) == 0xad}
             | {c for c in s if U.name(c, '').startswith('LATIN') and ord(c) > 127}
             | {c for c in s if c.lower() in 'ыэъ'})
print([hex(ord(c)) for c in odd])
"
```

Smart quotes and dashes will still show in the file: they belong to the
English keys, which have to match the page exactly. Only the values are the
site's own writing, and only those have to be clean.

## Finished

Ukrainian is complete. Everything the Saints page and the calendar say about
a saint is now written in it.

| | count |
|---|---|
| names | 1,528 |
| vocabulary beside the lives | 10,632 of 10,632 phrases |
| lives, the long ones on the Saints page | 1,456 of 1,456, 311,928 words |
| calendar entries, the short life and the intercession | 1,456 of 1,456 |
| the words the shared chrome says | all of them |

`python3 tools/check_register.py --lang uk` reports no opening that names a
saint the English way. Thirty-two are flagged for a second look, and all
thirty-two are right: a saint the calendar heads "Venerable" whom Ukrainian
knows as a священномученик, and the icon feasts, whose openings name no
saint at all.

### What had to move at the end

Three files were being rewritten under names that are served immutable for a
year, so each moved before Ukrainian was published:

- `saint-lives.v4` to `v5`, `saint-terms.v3` to `v4`. A reader who opened a
  life in Ukrainian while the language was half written would have held that
  half until next summer. This is the trap Romanian wrote down and it caught
  Ukrainian too.
- `ui-i18n.v3` to `v4`, and the shared script `plithos-ui.v8.js` to `v9.js`
  with it. This one is worse than a stale copy: the shared script has been
  asking for `ui-i18n.v3.uk.json` on every page for as long as Ukrainian has
  been an interface language, and until now there was no such file, so those
  requests were answered with the whole of the calendar and a 200 - and held
  for a year under the immutable header. Writing the bundle at `v3` would
  have published it to an edge that already holds the catch-all. **A language
  bundle fetched by code rather than named in a page has been requested,
  and answered wrongly, long before it is written.** Give it a name nothing
  has ever asked for.

`/data/saint-lives.*` and `/data/saint-terms.*` are deliberately NOT in
`_headers`, so they fall to `must-revalidate`. That is what keeps the rest of
the languages safe: the Saints page fetches
`saint-lives.v5.<lang>.json` for all twenty-two, eighteen of which do not
exist yet. Under an immutable rule every Spanish or Serbian reader who opened
a life would poison that name for a year before the language was begun. Do
not "fix" this by adding a rule for them.

## Then

Serbian, Arabic, Georgian; then es, fr, it, pt, de; then sw, ja, ko, zh;
then hy, arc, hi, bn, ur.
