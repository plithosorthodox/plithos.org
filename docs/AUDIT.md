# What is still in English, 11 September 2026

A sweep of all seven pages in all twenty-two languages, made after the
fasting notes and the book names were finished. Nothing here is fixed;
this is the list to choose from.

The method was not reading. Every table that holds language was parsed,
every key path compared against English, and every string the pages
actually display was collected from the data and looked up in the file
that is supposed to translate it. Where a count appears below, it was
counted.

## Where the interface is already whole

Worth stating first, so the work goes where it is needed.

Every interface table on every page is complete in all twenty-two
languages, key for key and to the leaf: `I18N`, `UX`, `NOTES_I18N`,
`KEY_I18N` on the calendar; `SUI` on the Saints page; `RLEX` on the
Library, 187 keys apiece; the prayers and contact tables; the Rule's
seventy-four blocks; and `ui-i18n.v5`, the shared masthead, search box
and theme switch.

The Saints page is the strongest. Of 10,895 distinct strings it puts on
the screen - places, origins, regions, ranks, states, eras, the manner
of canonisation, relics, the description of each saint's icon, the
patronages, the related commemorations, the titles - 10,874 are
translated in all twenty-one. The twenty-one that are not are internal
slugs that never reach a reader.

The glossary's 177 entries and the 100 prayers are complete in
twenty-one. So are the months, the weekdays, the degrees of the fast,
the jurisdictions and the country names. All seven pages set `lang` and
`dir`, so Arabic, Syriac and Urdu lay out right to left. The chosen
language carries between pages, and both scripture readers open in it
when that language has an edition.

## The largest one: the search finds only English

`data/search-index.v9.json` carries 2,095 entries - 1,456 saints, 177
glossary terms, 158 tags, 149 works, 100 prayers, 55 books of scripture
- and one name each, in English. `assets/plithos-ui.v15.js` prints that
name as it stands.

So the search box, which is on all seven pages and is the fastest way
into anything here, answers in English to every reader and can only be
questioned in English. A Greek reader cannot find Ἅγιος Νικόλαος by
typing it.

Its own words are translated - the placeholder, the group headings, the
counts, the hints - in all twenty-two. It is only the entries.

Every name it needs is already published: `data/saint-names.v1.*`,
`data/prayers-i18n.v2.*`, `data/glossary-i18n.v1.*`, the book names in
`scripture/index.json` and in `NT_BOOK_NAMES`.

## The second: every page tells a search engine it is English

`functions/_lang.js` serves `/el/rule` and its twenty-one companions
properly - it sets the `lang` attribute, rewrites the canonical, and
presets the language before the page's own scripts run. It does not
touch four things:

    <title>
    <meta name="description">
    og:title, og:description, twitter:title, twitter:description
    og:url, which still says https://plithos.org/ on every one of them

So all 154 addresses describe themselves in English - in the browser
tab, in a search result, and in the card that appears when someone
shares the link. The hook is already there; only the words are missing.

## The Library

The Library's own words, not the books on its shelves.

- **The shelf headings and their descriptions.** `CLASS_LABEL` and
  `CLASS_DESC`: Scripture, Conciliar, Patristic, Catechetical,
  Hagiographic, Liturgical, Modern, Outside testimony, each with a line
  under it. English only, and they are the headings of the browse view.
- **The note on the Septuagint canon.** `SCRIP_CAVEAT`, ninety words,
  shown under every Old Testament edition. English only.
- **The New Testament shelf**, its title and its description.
- **The roles in the side-by-side Liturgy**: Priest, Deacon, Choir,
  People, Reader, Bishop - and the line above the columns, "Choose one
  or more languages to read side by side."
- **The names of the editions' languages.** The Glossary already carries
  these translated into twenty-one, as `lgNames` in `data/glossary.v4.json`
  - Greek is 希腊文 to a Chinese reader there. The Library has no such
  table, so it shows either English ("Greek", "Latin", "Syriac") or the
  autonym ("Ελληνικά"), neither of which is the reader's language.
- **"7th century."** The other centuries on the shelf have an `lx:` key
  and are translated; the seventh has none and is English in all
  twenty-one.

## The calendar

- **One fasting note is still English.** `"A day of strict fasting."` is
  assigned straight into the day rather than through `FASTNOTE_I18N`, so
  it never passes the lookup. The other thirty-eight are complete.
- **The civic holidays are never translated**, and they disagree with
  themselves about what language they are in. 161 names across sixteen
  countries: the American, British, Canadian, Russian, Ukrainian, Greek,
  Romanian, Serbian, Bulgarian, Cypriot, Lebanese and Georgian ones are
  in English, while the German, Spanish, French and Mexican ones are in
  their own. Neither follows the reader.
- **The Western Rite names six of its days in English**, for a Greek or
  Russian reader as much as for a Bengali one, because they are
  assembled as sentences rather than looked up: the Nth Sunday in
  Advent, after Pentecost, after Epiphany and after Epiphany (resumed),
  the Last Sunday after Pentecost, and Christmastide. `SUN_AP` is the
  pattern for how to do them.

## What a screen reader hears

English, mostly, whatever language the page is in.

- The hidden `<h1>` at the top of the calendar.
- Most `aria-label`s: Previous month, Next month, Calendar style, Saints
  shown, View, Close, Library section, Catalog, Section contents. Two
  are translated; the rest are not. The placeholders all are.
- The `<title>` inside each jurisdiction's cross: "The Russian three-bar
  cross", "Grapevine Cross of Saint Nino", "Only unity saves the Serbs",
  "Jesus Christ conquers". These are the alt text of the emblems.

## Three things that are not about language

**Two works cannot be reached by browsing.** `canons-ecumenical` - the
canons of the Ecumenical Councils - and `cassian-conferences` carry
`source_class` values of `canons` and `ascetic`. `CLASS_ORDER` does not
list either, and the Councils and Creeds section filters on
`conciliar`. Both works are on the shelf, both are in the search index,
and neither appears anywhere a reader would look for them.

**The Western Rite kalendar is made of two uses.** It names Whitsunday,
Trinity Sunday and Corpus Christi, and then counts the green Sundays
after Pentecost. The Antiochian vicariate keeps two uses - St Gregory,
which is Roman and counts after Pentecost, and St Tikhon, which is
Sarum and counts after Trinity - and this is one kalendar built from
both. It wants a decision, not a patch.

**A language link overwrites a reader's choice.** `_lang.js` writes
`plithos.lang` when it serves a prefixed address, so a Greek reader who
follows a link to `/zh/saints` finds the whole site in Chinese
afterwards, on every page, until he changes it back.

## Two small ones

`library.html` formats one count with `toLocaleString()`, which uses the
browser's locale rather than the language the reader chose.
`SCRIP_GROUP_LABEL` in the same file is dead: `GRP_TR` replaced it.
