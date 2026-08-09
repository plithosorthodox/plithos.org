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
