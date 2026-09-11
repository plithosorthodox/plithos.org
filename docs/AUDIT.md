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

The Library's own words, not the books on its shelves. The shelf
headings, their descriptions, the New Testament shelf, the names of the
editions' languages and the seventh century were done on 11 September;
what is below is what is left.

- **The note on the Septuagint canon.** `SCRIP_CAVEAT`, ninety words,
  shown under every Old Testament edition. English only, and the one
  item here that has no published translation to draw on: it has to be
  written, in twenty-one languages, in the site's own voice.
- **The roles in the side-by-side Liturgy**: Priest, Deacon, Choir,
  People, Reader, Bishop - and the line above the columns, "Choose one
  or more languages to read side by side." The Glossary carries priest,
  deacon, reader and bishop in twenty-one, but as headwords with their
  glosses (Greek gives "Πρεσβύτερος (ιερεύς)"), which is not how a rubric
  reads. Choir and people it does not carry at all.
- **The eleven section headings of the Divine Liturgy** - Opening and the
  Great Litany, the Antiphons and the Little Entrance, the Trisagion,
  the Anaphora - are English in every language. The Glossary has
  Trisagion, Cherubic Hymn, Great and Little Entrance and Anaphora;
  it does not have Creed, Antiphon, Litany, Dismissal or Communion.
  This one touches the Liturgy, which this site keeps human-translated,
  so it is a decision before it is a task.
- **"Outside testimony"**, the one shelf with no section of its own, and
  its line. One work stands on it.

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

Better than it did. The hidden `<h1>` at the top of the calendar, the
legend and reading panels, the civic-holiday menu and the prayer panel
now name themselves in the reader's language, and so does the language
control on all seven pages - that one from the shared chrome, which knew
the word all along and was not being asked. Every page carries the
mechanism now: `data-i18n-aria` on the calendar, `data-lx-aria` on the
Library.

What is left has no published word to draw on and needs writing:

- **Previous month, Next month, Previous year, Next year, Year, Close,
  Calendar style, Saints shown, View** on the calendar; **Catalog** and
  **Section contents** on the Library. Eleven labels, twenty-one
  languages.
- The `<title>` inside each jurisdiction's cross: "The Russian three-bar
  cross", "Grapevine Cross of Saint Nino", "Only unity saves the Serbs",
  "Jesus Christ conquers". These are the alt text of the emblems.

And one thing found by surfacing it: `key`, which names the legend
panel, is translated twenty-one ways that do not agree. Japanese,
Korean and Chinese say legend; Russian, Ukrainian, Spanish and Romanian
say dictionary or glossary; German, Greek, Serbian and Arabic say terms
or definitions; French, Italian and Portuguese say references. The word
had never been shown to anyone - it now labels the panel - and the
English "Key" is ambiguous enough to have caused it. It wants one
meaning chosen and twenty-one words written to it.

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

## The Chinese is of two minds about its own script

The site publishes simplified Chinese. `LANG_NAMES` calls the language
简体中文, and every body of Chinese on it is simplified: the calendar's
names, the saints' lives, the vocabulary, the prayers, the glossary, the
scriptures, the chrome. Measured on a probe of characters that differ
between the scripts, all of them come back simplified and none
traditional.

Two exceptions, both in served copy:

**The Rule page in Chinese is a mixture.** 29 of its 74 blocks in
`data/rule-i18n.v5.zh.json` are traditional and the rest are simplified,
so a reader meets 祈禱規則 in one paragraph and 祈祷规程 in the heading
above it. Mixed is worse than either.

**`SITE_INFO_I18N`** - the paragraph the site gives about itself when the
mark is tapped, and now also the description at every Chinese address -
is traditional throughout.

This is the same fault as the New Testament book names in `library.html`,
which were entered in traditional over a simplified text and were
corrected on 11 September. The conversion is mechanical and the decision
is already written down in `docs/CHINESE.md`; what is needed is to do it
and to check it, not to decide it again.

## Two small ones

`library.html` formats one count with `toLocaleString()`, which uses the
browser's locale rather than the language the reader chose.
`SCRIP_GROUP_LABEL` in the same file is dead: `GRP_TR` replaced it.
