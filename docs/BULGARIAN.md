# Bulgarian

This file is two things. It is the brief for adding Bulgarian to this site as
its twenty-third language, and it is where the decisions about Bulgarian get
written down as they are settled, so each is made once. Anyone doing the work
should read it first and add to it as they go.

Read `CLAUDE.md` before anything here. Its rules bind this work and are not
restated in full below; the ones that bite hardest are repeated where they
bite.

## Why Bulgarian, and why it is not just another language

Seven of the twenty-two Orthodox Churches speak a language this site does not
publish in. The Bulgarian Patriarchate is the one that ought to trouble
anybody: a Church of the first rank, older as a patriarchate than most on the
list, and this site offers Syriac and Bengali before it offers Bulgarian. See
`docs/DIRECTORY.md`, where it became visible.

Bulgarian is also the easiest of the seven to do well, and the easiest to do
badly. Cyrillic script, a Slavonic liturgical vocabulary, and Russian,
Ukrainian, Serbian and Church Slavonic already on the site to read against.
The trap is exactly that: Bulgarian is not Russian written differently. It has
its own definite article, no cases, its own received forms for the feasts and
the ranks, and a reader will hear a Russianism at once. Use the Slavonic
languages already here to check yourself, never to generate.

## The one rule that inverts for a new language

Everywhere else on this site the rule is **gather, do not compose**: find the
form the site already publishes in that language and use it. Bulgarian has no
corpus here to gather from. On the first day there is nothing.

So for Bulgarian the rule becomes: **gather from the Bulgarian Church, not
from this site.** Every word comes from what Bulgarian Orthodoxy already
publishes - the Patriarchate at bg-patriarshia.bg, the Synodal publishing
house, the Church's own calendar and prayer book - and not from a rendering
made for the occasion.

The corpus builds itself as the phases below complete. From Phase 2 onward
there is enough Bulgarian on the site to start counting competing forms
against, which is how every other language here was settled. Write each count
into this file when you make it.

## What must never be rendered

From `CLAUDE.md`, and it governs the largest phases:

- **Holy Scripture, the Divine Liturgy, and the other liturgical texts stay
  human-translated.** They are the Church's own words in her worship, and a
  rendering nobody has received does not stand in that place. For Bulgarian
  this means the prayers and the liturgical texts are a **sourcing** job, not
  a translation job: find the Bulgarian Church's published text.
- **Never invent hagiography.** A saint's life, feast date, jurisdiction or
  relics come from a real source.
- **Never paraphrase, modernise or correct a liturgical or scriptural text.**
  If something looks wrong, ask.

The Fathers, the saints' lives, the site's own copy and the interface may be
rendered where no published Bulgarian text exists. Nothing else.

## House rules that will fail a check

- No em dashes and no en dashes anywhere. A plain hyphen.
- Straight quotes, never curly.
- Never let the machinery show in anything a reader sees: no passes,
  pipelines, builds, scripts, tools or filenames in served text.
- `/data` is cached immutable for a year, but **adding a new language file to
  an existing family needs no version bump**. `_headers` matches on wildcard
  stems - `/data/prayers-i18n.v2.*` - so `prayers-i18n.v2.bg.json` is a new
  path and is covered already. Only **changing** an existing file forces a
  bump. One file in this work does change: `data/flags.v2.json`, which must
  become `flags.v3.json` with its own `_headers` stem and every reference
  updated.
- Run `python3 tools/stamp_build.py` whenever a page changes, and
  `python3 tools/check_site.py` must pass before anything ships.

## Phase 0 - register the code

Nothing else works until `bg` is a language this site knows. Small, and it is
the whole of the first commit.

| where | what |
|---|---|
| `index.html` | `LANG_NAMES` gains `bg:"Български"` |
| `tools/lang_routes.py` | `LANGS` and `NAMES` gain `bg`; then `--write` generates `functions/bg/`, the hreflang alternates on all eight pages, and the sitemap |
| `tools/nav_chrome.py` | `NAV["bg"]` - the eight masthead words; then `--write` |
| `data/flags.v3.json` | the Bulgarian flag, as an inline SVG in the shape the others use; bump the family and add the `_headers` stem |
| `tools/directory_words.py` | `LANGS` gains `bg`; `W["bg"]` and `COUNTRIES` if the browser cannot name countries in Bulgarian |
| `tools/page_meta.py`, `tools/check_site.py` | wherever the language list is written down |

After Phase 0 the site answers at `/bg/`, `/bg/saints` and the rest, the
picker offers Bulgarian, and every page falls back to English inside. That is
correct and expected: the fallback is what lets a half-written language read.

### Phase 0 decisions

The masthead uses `Календар`, `Църкви`, `Светии`, `Библиотека`, `Молитви`,
`Правило`, `Речник` and `Контакти`. The Bulgarian Patriarchate itself prints
`Календар`, `Контакти` and `Молитви` in its navigation, `БИБЛИОТЕКА` over its
published collection, and `Жития на светии` over its lives. Its list of local
Churches uses `Поместни православни църкви`. These forms settle the shared
nouns; the remaining interface nouns are ordinary modern Bulgarian site copy.

The language name is `Български`. The picker uses the civil tricolour in the
same compact inline SVG shape as the other flags. Browser `Intl.DisplayNames`
returns the directory's country names in Bulgarian, so no `COUNTRIES["bg"]`
table is needed.

### Phase 1 decisions

The interface follows the vocabulary the Bulgarian Patriarchate publishes:
`Светии`, `Жития`, `Свещеното Писание`, `Календар`, `Молитви` and
`Поместни православни църкви`. The calendar selector therefore says
`Поместна църква`, not the administrative loanword `Юрисдикция`, and the
Saints filter says `Всички поместни църкви`. The Church's own calendar and
its account of the calendar reform settle `Нов (новоюлиански) календар`,
`Стар (юлиански) календар`, `Блажи се`, `Строг пост`, `Разрешава се риба`
and the ecclesial word `елей`.

Sources checked for these forms: the Patriarchate's
[2026 calendar](https://bg-patriarshia.bg/calendar/2026),
[lives collection](https://bg-patriarshia.bg/lives-of-saints),
[Synodal Bible](https://bg-patriarshia.bg/web-bible),
[prayer book](https://bg-patriarshia.bg/liturgical-prayer), and
[contact page](https://bg-patriarshia.bg/contacts).

The collection heading is `Светиите`, while singular search results may use
`светец`. Metadata uses `Чин`, `Съсловие`, `Прославление`, `Причисляване към
светиите`, `Мощи` and `Степен на празника`. These are the forms used in the
Patriarchate's lives and notices of glorification, rather than literal copies
of the English field names.

The Library uses the modern interface forms `Старият Завет` and `Новият
Завет`, but the formal title of the Synodal Bible remains untouched wherever
it is cited. Its traditional fourfold grouping supplies `Законоположителни
книги`, `Исторически книги`, `Учителни книги` and `Пророчески книги`.
`Анагигноскомена (неканонични книги)` preserves the site's category while
using the historical Synodal description.

The Plithos line `according to the whole` is reader-facing editorial copy,
not a received Bulgarian Church phrase. It is rendered `Съобразно цялото`:
idiomatic Bulgarian without adding the more specific doctrinal claims carried
by `съборност` or `католичност`.

Phase 1 writes all 415 strings in the calendar, Saints, Library, prayers,
contact, accessibility and shared-chrome surfaces, including all 108
nameable Library search tags. The Glossary adds all 17 page strings, 35 tag
names and seven source-language names. The Churches page has all 15 page
strings. The search index first added in Phase 0 remains an English fallback
at `search-index.v10.bg.json`; that path is now immutable and must never be
overwritten. Its Bulgarian replacement will be published under a new search
index family after enough content exists to justify the one site-wide asset
bump.

Page metadata remains deliberately staged where its source belongs to a later
phase: the calendar's descriptive prose is Phase 2, the prayer collection's
data is Phase 3, and the Rule is Phase 4. English fallback remains visible and
honest for those pages until their own source is complete.

## The order of the phases, and why

Highest value per word first. A reader who chooses Bulgarian should see the
site is his before he sees every word of it.

**Phase 1 - the chrome.** The words around the content.

| file | size |
|---|---|
| `tools/ui_i18n/bg.py` -> `data/ui-i18n.v6.bg.json` | 23 strings (search, theme, tagline) |
| `index.html` `const I18N` | ~3 KB per language |
| `saints.html` `const SUI` | the Saints interface |
| `library.html` `const RLEX` | the Library interface |
| prayers, rule, glossary, contact, churches page chrome | small each |

**Phase 2 - the calendar's own words.** This is the site's heart and the
point at which Bulgarian becomes usable.

| file | size |
|---|---|
| `FASTNOTE_I18N` in `index.html` | 39 fasting notes |
| `BOOK_I18N` | 46 books of Scripture, by name |
| `SUN_AP`, `CAT_I18N`, `NOTES_I18N`, `TAGLINE_I18N`, `SITE_INFO_I18N` | small |
| `KEY_I18N` | the Guide, ~7.5 KB |
| `data/calendar-names.v1.bg.json` | **1,719 commemorations** |
| `tools/local_names/bg.py` | 127 Churches' own commemorations |

The 1,719 are the largest single block in the whole job and the one where the
Bulgarian Church's own calendar is the source. Do not render them from
English. The Patriarchate publishes a calendar; read it.

**Phase 3 - the prayers.** `data/prayers-i18n.v2.bg.json`, 100 prayers.
**Sourcing, not translation.** Find the Bulgarian Church's published prayer
book. Where a prayer genuinely has no received Bulgarian text, that is the one
case where it may be rendered, and `CLAUDE.md` says a short prayer supplied to
complete a page does not need a translator's note.

Phase 3 is complete: all 100 prayers follow the canonical key and paragraph
order. Received Bulgarian text comes first, principally from the Bulgarian
Patriarchate's [morning prayers](https://bg-patriarshia.bg/liturgical-prayer/utrinni-molitvi),
[evening prayers](https://bg-patriarshia.bg/liturgical-prayer/vecherni-molitvi),
[Communion prayers](https://bg-patriarshia.bg/liturgical-prayer/molitvi-predi-sveto-pricheshtenie)
and [prayers for particular needs](https://bg-patriarshia.bg/liturgical-prayer/molitvi-pri-razlichni-sluchai).
The reader services preserve the exact selected passages from the
[Synodal Bible](https://bg-patriarshia.bg/web-bible). The naming prayer follows
the Sofia Metropolia's 2024 `Цветен требник`, pages 25-26. Where focused source
work found no intact received Bulgarian counterpart, the canonical prayer was
rendered faithfully without changing its scope, sequence, rubrics,
placeholders or repetitions.

**Phase 4 - the Rule, the Glossary, the saints.**

| file | size |
|---|---|
| `tools/rule_text/bg.py` -> `data/rule-i18n.v6.bg.json` | 74 blocks |
| `tools/glossary_terms/bg.py` -> `data/glossary-i18n.v1.bg.json` | 177 terms |
| `tools/saint_terms/bg.py` -> `data/saint-terms.v5.bg.json` | **10,632 entries**, the place and rank lexicon |
| `tools/saint_names/` equivalent -> `data/saint-names.v1.bg.json` | 1,528 names |
| `tools/saint_lives/bg.py` -> `data/saint-lives.v6.bg.json` | 1,456 lives |
| `tools/saint_info/bg.py` -> `data/saint-info.v1.bg.json` | 1,456 |

The saints' terms file is the largest by count and the most useful: every
later phase reads places and ranks out of it. Do it before the lives.

The Rule's 74 blocks are complete. Its received forms come from the
Patriarchate's [Jesus Prayer](https://bg-patriarshia.bg/liturgical-prayer/iisusovata-molitva),
[prayer-rule teaching](https://bg-patriarshia.bg/news/molitvenite-pravila-i-tyahnoto-izpalnenie),
[Communion prayers](https://bg-patriarshia.bg/old/index1316.html?file=participial_prayers.xml)
and Synodal Scripture, with the received Bulgarian wording of Rule 29 from
the Sofia Metropolia's publication of the ecumenical canons. The two Didache
quotations follow the Bulgarian text published as `Дидахи`. Focused source
work found no accessible received Bulgarian edition of the page's exact
Cassian and Chrysostom excerpts, so those excerpts are faithful renderings
of the canonical text and are not represented as verbatim Bulgarian
editions.

**Phase 5 - Scripture.** Optional for shipping - Armenian and Syriac are
published here without it - and governed by the hardest rule on the site.

**The canon decides, before anything else.** An edition missing Wisdom,
Sirach, Tobit, Judith, Baruch or the Maccabees is not a smaller Bible; it is a
different canon, and this site is not published in that canon. The order is:
an Orthodox edition first; failing that, whatever carries the whole canon;
and only where nothing carries it does the received text keep its place, with
the entry saying plainly what is missing. Read the whole section in
`CLAUDE.md` before choosing. Register the edition in `scripture/index.json`
with its tradition, edition name and licence, and put the books under
`scripture/bg/`.

Only public-domain or freely licensed texts. Record the licence.

**Phase 6 - the directory.** `tools/directory_names/bg.py` with NAMES, SEATS
and STYLED. Small, and there are twenty-two worked examples beside it.

## The jurisdiction on the calendar

**Bulgaria is already there, and more of it than you would expect.** Before
adding anything, read what exists:

| | |
|---|---|
| selector entry | `JURISDICTIONS.bulgarian` in `index.html` |
| reckoning | new calendar |
| rite | Byzantine |
| emblem | present, one of ten in `JURISDICTION_CROSSES` |
| own commemorations | **22** - 21 fixed and one movable, in `tools/local_saints.py` under `"bulgarian"` |

Those twenty-two are read off published Bulgarian sources and the source is
recorded beside them - St Euthymius and St Joachim I of Tarnovo, St
Sophronius of Vratsa, St Boris-Michael the Baptizer of Bulgaria, St Paisius
of Hilendar, the Seven Holy Apostles, the repose of St John of Rila, the
Synaxis of All Saints of Bulgaria on the second Sunday after Pentecost. Only
Romanian and Georgian have more.

So the jurisdiction does not need building. What it needs is three things,
and the first two are part of the phases above:

1. **Those twenty-two commemorations in Bulgarian.**
   `tools/local_names/bg.py`, which is one file of 127 entries covering every
   Church's own commemorations, not only Bulgaria's. It is a small file with
   twenty-one worked examples beside it.

2. **The rest of the calendar in Bulgarian**, which is Phase 2. A Bulgarian
   reader who picks the Bulgarian jurisdiction today gets his own Church's
   saints and every word around them in English.

3. **A question to settle, not a file to write.** The fasting rule branches
   on the jurisdiction, and only `greek` takes the Constantinople and Church
   of Greece reckoning of the Nativity and Apostles' fasts; every other
   Church, Bulgaria included, takes the Typikon that the Slavic Churches and
   Antioch publish. Bulgaria is a new-calendar Church that keeps the Slavic
   Typikon, so that is probably right - but it was assigned by default rather
   than decided, and nobody has checked it against what the Bulgarian Holy
   Synod actually prints. Check it, and write the answer here with the
   source. See `docs/JURISDICTIONS.md` for how the two traditions differ and
   which Churches were named for each.

   **Settled from the Bulgarian Patriarchate, 2026-09-13.** The present
   generic Slavic branch is not an exact statement of Bulgarian practice.
   The Holy Synod's Nativity Fast notice gives 15 November through 24
   December; vegetable food with oil in the first week and from 20 through
   24 December; shellfish, except on Wednesdays and Fridays, on the other
   days; and fish by tradition only on the Entry of the Theotokos and St
   Nicholas. That is narrower than the branch's general weekend-fish rule.
   Its Apostles' Fast notice likewise gives its own provisions rather than
   assigning Bulgaria by family resemblance. A future jurisdiction-rules
   change therefore needs a Bulgarian branch; this translation phase records
   the result but does not change fasting logic. Sources: the Patriarchate's
   [Nativity Fast notice](https://bg-patriarshia.bg/news/zapochva-rozhdestvenskiat-post)
   and [Apostles' Fast notice](https://bg-patriarshia.bg/news/zapochna-petroviat-post).

### One thing that is already done, checked rather than assumed

The jurisdiction picker **is** translated, in every offered language. Each
option carries `data-i18n="jz_<jurisdiction>"` and every one of the ten keys
is written in `I18N[lang].ui`; the heading over the month resolves the same
name through `NAMES_I18N` first and falls back to that key. A Bulgarian
reader will pick his Church from a Bulgarian list the moment `bg` exists.

This paragraph replaces one that said the opposite. It was written from
`JURISDICTIONS[k].name` holding a single English string, which is true and is
not what the reader sees. Left uncorrected it would have sent somebody to
rebuild a working thing.

## The register check

`tools/check_register.py` holds each language to its own way of naming a
saint, and Bulgarian needs an entry in its `LANGS` table **before** the
commemorations are written, not after. The entry needs:

- `generic` - a pattern matching the bare word for holy used with no rank,
  which is the error the check exists to catch
- `monastic` - the word Bulgarian uses of a monastic saint
- `ranks` - the vocabulary of every rank Bulgarian actually uses
- `strict` - whether Bulgarian allows the plain honorific before a name

Derive all four from the Bulgarian Church's own calendar. Do not copy the
Russian entry and adjust it; that is exactly the failure this file warns
about. Write the vocabulary into this file when you settle it, with the
counts that settled it.

**Settled from the Patriarchate's 2026 calendar, 2026-09-13.** Its 365
records use `Св.` 559 times, while full forms of `Свети` and `Света` appear
five times. About 200 of the 557 immediate tokens after `Св.` are personal
names rather than ranks, so the bare honorific is received Bulgarian usage
and `strict` is `False`. The same calendar has 192 `Преп.` forms; `мчк`,
`мчца` and `мчци` occur 89, 33 and 64 times; `свщмчк` and `свщмчци` occur
55 and seven times; the three `прпмч` forms occur 12, eight and two times;
and `вмчк` and `вмчца` occur 11 and ten times. It also supplies both
abbreviated and full forms for apostle, prophet, Equal-to-the-Apostles,
righteous and unmercenary, plus confessor, fool-for-Christ,
right-believing and wonderworker. Those counts settle the generic,
monastic and rank patterns in `tools/check_register.py`; hierarchy, clergy
and monastic-house titles there are the forms present in the same calendar.
Source: the Patriarchate's [2026 calendar API](https://bg-patriarshia.bg/api/calendar/2026).

## Phase 2 calendar-name decisions

**Settled from the Patriarchate's calendar archive, 2026-09-13.** The archive
exposes one official record for every civil date from 2016 through 2026. The
Bulgarian name corpus takes a fixed commemoration only from the same month and
day, prefers the 2026 form, and copies an exact source substring after
normalizing forbidden punctuation to the site's plain hyphen and straight
quotes. The principal fixed and Paschal feasts use the same official archive.

The accepted corpus has 551 exact base and principal-feast mappings. Together
with the 127 exact local-Church mappings, Bulgarian supplies 678 of the 1,719
calendar names. The other 1,041 remain visibly in English. That fallback is
deliberate: records absent from the Bulgarian calendar, unsplittable groups,
homonyms, conflicting identities, and event names for which the source prints
only a person were omitted rather than plausibly rendered. A received
Bulgarian rank or locator is retained when the identity and date are exact;
the English wording does not override the Bulgarian Church's own title.

The source modules are divided by month so every accepted form can be checked
against one date without reading the page's large name table. Source:
the Patriarchate's [calendar archive](https://bg-patriarshia.bg/calendar/2026)
and annual [calendar API](https://bg-patriarshia.bg/api/calendar/2026).

## Verification, every time

```
python3 tools/lang_routes.py --check
python3 tools/nav_chrome.py --check
python3 tools/check_register.py --lang bg
python3 tools/check_i18n.py
python3 tools/stamp_build.py
python3 tools/check_site.py
```

`check_site.py` is the gate: thirty-three checks, and nothing ships while it
reports an error. Warnings are for work that is honest but unfinished, which
a half-written language legitimately is.

## What not to do

- Do not translate a postal address, a URL, or a body's own name in its own
  language. See `docs/DIRECTORY.md` for the rule and the reason.
- Do not fill a gap with plausible prose. An entry that is not there is
  better than an entry that is invented, and the site's whole authority is
  that distinction.
- Do not escalate an editorial question about Bulgarian. Settle it from what
  the Bulgarian Church publishes, count the competing forms rather than
  choosing by ear, and write the decision here. Deletion is the only thing to
  ask about.
- Do not ship a phase half-done in a way that reads as finished. English
  fallback is visible and honest; a rendered guess is not.

## Decisions settled so far

Phase 0 registration and Phase 1 interface decisions are recorded above.
Later-phase decisions will be added in their own sections as their source
corpora are gathered.
