# plithos.org — baseline audit

State of the site as committed. Verified against the live site on 2026-08-02:
`index.html` served from plithos.org is **byte-identical** to the copy in this
repository apart from Cloudflare's injected analytics beacon, so this
repository is an accurate mirror of production.

Findings below were verified by parsing the data structures and by loading all
pages in headless Chromium, not by reading the source alone.

---

## 1. What exists

### Pages

| Route | File | Size |
|---|---|---|
| `/` `/calendar` `/prayers` | `index.html` | 6.8 MB |
| `/saints` | `plithos_saints.html` | 3.6 MB |
| `/reader` `/library` | `plithos_reader.html` | 7.0 MB |
| `/contact` | `contact.html` | 26 KB |

### Calendar and prayers (`index.html`)

- Full liturgical year: fixed and movable feasts, Paschalion, fasting rule with
  a five-level colour legend, multiple jurisdictions, ICS export by day/month.
- 100 prayers, categorised, with source notes.
- **1,454 calendar saint blurbs, all present** (`SAINT_INFO`), averaging 60
  words, 87,548 words total. Only 2 are under 20 words.
  The HTML header comment still reads *"blurbs through March complete (1047
  lives); 2026-07-17"* — **that comment is stale** and should be updated.

### Saints (`plithos_saints.html`)

- **1,454 saints**, filterable by name, day, order, place, attribute,
  jurisdiction, century, era.
- 28 fields per saint. Core fields are near-complete; optional ones are thin:

  | field | filled | | field | filled |
  |---|---|---|---|---|
  | `name` `type` `life` | 1454 | | `attributes` | 889 |
  | `icon` `feastRank` | 1435 | | `reposedYear` | 875 |
  | `feasts` | 1403 | | `relics` | 834 |
  | `era` | 1398 | | `origin` | 797 |
  | `patronCauses` | 1381 | | `jur` | 671 |
  | `canonizedBy` | 1361 | | `bornYear` | 170 |
  | `place` | 1351 | | `baptismalName` | 150 |
  | `region` | 1344 | | `movableFeasts` | 87 |
  | `century` | 1322 | | `glorifiedYear` | 76 |
  | `rank` `state` `sex` | ~1300 | | `great` | 54 |

- **English only.** No i18n mechanism on this page at all: no language JSON is
  fetched, no switcher, and it does not even read the shared `plithos.lang`
  key that the other pages use.
- Prose volume: **396,823 words** of lives + **31,034 words** of icon
  descriptions = **427,857 words** per language.

### Library (`plithos_reader.html`)

`CORPUS` holds 49 catalogue entries / 782 static units / 1,164,695 words.
Entries divide into three kinds:

| kind | entries | note |
|---|---|---|
| Patristic works with embedded text | **25** | the library proper |
| Bible catalogue stubs (`bible-*`) | 19 | units generated at runtime from `/data` |
| Divine Liturgy entries | 5 | units generated at runtime from `LIT_ALIGN` |

Works present: Athanasius (3), Basil (2), Justin Martyr (2), John of Damascus,
John Chrysostom (*On the Priesthood* only), Gregory of Nazianzus, Gregory of
Nyssa, Cyril of Jerusalem, Clement of Rome, Ignatius, Polycarp, Barnabas,
Diognetus, Papias, Athenagoras, Tatian, Theophilus, Vincent of Lérins, the
Martyrdom of Polycarp, the Nicene Creed, and the canons of the Seven
Ecumenical Councils.

### Scripture

Two **separate and inconsistent** delivery systems:

| | Old Testament | New Testament |
|---|---|---|
| consumed by | `plithos_reader.html` | `index.html` |
| path | `scripture/<lang>/<n>.json` | `data/bible.v1.<lang>.b64` |
| format | plain JSON | base64 of zlib-deflated JSON, inflated with pako |
| languages | 16 | 19 |
| size | 70 MB | ~7 MB |

`scripture/index.json` declares 54 books and carries a per-language `avail`
list, so the reader correctly hides books a language lacks rather than
offering broken links. The gap is one of **content, not of code**:

| tradition | languages | OT books |
|---|---|---|
| Septuagint | en (53), el (51), ru (50), cu (48), ka (39) | full or near-full |
| Masoretic | sr uk es pt it fr de ar zh ja ko | **39 — no deuterocanon** |

**11 of 16 languages ship a Protestant 39-book Old Testament** (Luther 1545,
Diodati 1649, Darby, Sagradas Escrituras 1569, Smith & Van Dyke, Union,
Kougo-yaku, Ohienko, Daničić-Karadžić). For an Orthodox site this is a
substantive gap: Tobit, Judith, Wisdom, Sirach, Baruch, and the Maccabees are
simply absent in those languages. Georgian is marked `septuagint` but also has
only 39 books. `2 Esdras` (book 68) is declared in the index but absent in
every language.

**Licence note.** `CLAUDE.md` states the site carries only public-domain
texts. Three scripture editions are not public domain: Greek LXX is *"Free for
non-commercial use"*, Portuguese *Bíblia Livre* is **CC BY** (requires
attribution), and Arabic Smith & Van Dyke is *"Free distribution permitted"*.
These are declared honestly in `index.json` but the CC BY attribution is not
surfaced anywhere in the UI.

**Verse numbers in the New Testament bundles are wrong in some chapters.**
Confirmed in Russian: `Matthew 17` is held with keys 1 to 26, contiguous,
while the Synodal chapter has 27 verses. Synodal 17:20 ("по неверию вашему")
is absent, and every verse after it is keyed one lower than its real number,
so a reader asking for 17:20 is shown 17:21. The reader prints the key as the
verse number, so the wrong number is displayed, and one verse of the Gospel is
missing outright.

Scale: 399 chapters across the eighteen bundles are keyed 1..N contiguously
while being shorter than the same chapter in the KJV, 45 of them in Russian.
Not all are defects - the Textus Receptus carries verses the critical texts
omit, and a chapter legitimately ends short when the omission falls last - but
every one of them is a candidate, and the Russian case proves the failure mode
is real rather than theoretical. 88 Russian chapters DO preserve real gaps in
their keys, so the fault is not uniform and cannot be corrected by arithmetic.

Fixing this means re-ingesting the New Testament with the source's own verse
numbers rather than its verse order. That work should wait on the provenance
question below, since it settles which text is being re-ingested.

**New Testament bundle provenance is unsettled for nine languages.** Each
`data/bible.v1.<lang>.b64` records the text it was built from, but for
`arc, de, es, fr, hi, hy, ko, pt, sw` the identifier does not settle which
revision is held, and for Spanish, French and Portuguese the likeliest
candidates include revisions that are **not** public domain: Reina-Valera 1960
is held by the United Bible Societies, `pt_aa` may be Almeida Revista e
Atualizada (1959), and `fr_apee` may be La Bible de l'Epee rather than
Ostervald. Until each is confirmed, the Library names the edition and gives no
year, since a date asserts a check that has not been made. Nine of nineteen
scripture entries stand that way; the other ten carry a year that is certain.
Resolving this is a licensing question before it is a metadata one.

---

## 2. Is all the content reachable?

Mostly yes. Verified checks:

| check | result |
|---|---|
| Calendar "Read the full life →" links (`#n=<name>`) resolve to a saints record | **1,454 / 1,454, zero broken** |
| Saints on the saints page missing from the calendar | **0** |
| Saints with no feast day at all (unreachable by date) | **0** (51 have movable feasts only) |
| Library units with no catalogue entry (orphan text) | **0** |
| Divine Liturgy text actually present | **yes** — 11 sections × 343 lines × 5 languages (en, el, cu, ro, de) at **100 %** |
| Books offered but not shipped | **0** — `avail` gates the list correctly |

**Correction to an earlier draft of this audit:** I previously reported that
the five Divine Liturgy entries had no text and that the calendar blurbs
stopped in March. Both were wrong. The liturgy is built at runtime by an IIFE
from `LIT_ALIGN` and is complete in five languages; the blurbs are complete at
1,454. I had trusted a stale source comment and looked only at the static
`CORPUS.units`.

### What *is* effectively invisible

**The interface is translated into 8 languages, not 22.** This is the largest
gap on the site and it is not visible from the language menu, which offers all
22 as though equal.

| layer | languages | notes |
|---|---|---|
| `I18N` — months, weekdays, fasting labels, all UI chrome | **8** (en el ru ro uk de es ar) | ~82–104 keys each |
| `UX` patch object | 22 | but only **5 keys**: nav labels, About, Guide |
| `NOTES_I18N`, `FASTNOTE_I18N`, `BOOK_I18N` | 7–8 | same 8-language set |
| `SAINT_INFO_I18N` — translated calendar blurbs | **4** (el ru ro uk) | |
| `SITE_INFO_I18N`, `PLITHOS_INFO_I18N`, `TAGLINE_INFO_I18N` | 22 | complete |
| `NAMES_I18N`, `KEY_I18N`, `CAT_I18N`, `TAGLINE_I18N` | 21 + en | complete |
| Prayers (`/data/prayers-i18n.v1.*`) | 21 + en | complete |

So a reader who picks **Japanese, French, Chinese, Korean, Swahili, Italian,
Portuguese, Serbian, Georgian, Armenian, Syriac, Hindi, Bengali, or Urdu**
gets translated prayers and About text, but **English month names, English
weekday names, English fasting labels, and an otherwise English interface**.
Fourteen of the twenty-two offered languages are in this state.

---

## 3. Defects

### D1 — Missing NT data triggers a silent 6.8 MB download, repeatedly

**Severity: high.** `data/bible.v1.<lang>.b64` does not exist for **`bn`
(Bengali), `ka` (Georgian), `ur` (Urdu)** — three offered UI languages. (`cu`
is also absent but is not a UI language.)

Cloudflare Pages' catch-all returns **HTTP 200 with the 6.8 MB body of
`index.html`** for any missing path:

```js
fetch("data/bible.v1."+L+".b64")
  .then(function(r){ return r.ok ? r.text() : null; })   // r.ok is TRUE — it's a 200
  .then(function(t){
     var b = atob(t.trim());                             // throws: HTML isn't base64
     bibLoaded[L] = true;                                // never reached
  })
  .catch(function(){})                                   // swallowed silently
```

6.8 MB downloaded and discarded, silent fallback to English, and because
`bibLoaded[L]` is never set it **repeats on every page load**.

### D2 — Every Library visit wastes 6.8 MB

**Severity: high — this affects all users, in every language.**

`plithos_reader.html` ends with an unconditional `loadLibraryIndex()`, which
fetches `data/library/works-index.json`. **That file does not exist**, so the
same catch-all returns 6.8 MB of `index.html`, `r.json()` throws, and
`.catch(function(){})` swallows it.

This is also the good news for extending the library: the reader already has a
complete lazy-loading mechanism built in and documented in a source comment —
`data/library/works-index.json` as a catalogue plus `data/library/<work_id>.json`
per work, joining `UNITS` and rebuilding the search index without a reload.
**The plumbing for item 1 exists; only the files are missing.**

### D3 — `_headers` emits conflicting `Cache-Control` on `/data/*`

**Severity: medium.** `/data/*` matches both the `/data/*` block and the
`/*.json` block, and Cloudflare concatenates them. Live response:

```
cache-control: public, max-age=31536000, immutable, public, max-age=604800
```

Browsers take the first, so the effective policy is **one year, immutable**.
Re-uploading a `prayers-i18n.v1.*.json` without bumping the filename version
will not reach returning visitors for a year. `docs/_headers.alternate.txt` is
a second variant you uploaded using `604800` instead; it is not live.

### D4 — No PWA, offline support, or install target

No `manifest.json`, service worker, `apple-touch-icon`, or `theme-color` on any
page. A PWA is the shortest credible path to "an app", and offline access is
the highest-value feature for a prayer and calendar app.

### D5 — No `robots.txt`, no `sitemap.xml`, no indexable content

Careful per-page metadata exists (canonical, OpenGraph, Twitter cards), but
nothing tells a crawler what exists, and all 1,454 saints and 25 works are
locked inside JS-rendered monoliths. Essentially none of the content is
indexable.

### D6 — No URL state anywhere except one entry point

| page | `pushState` | `location.hash` | `URLSearchParams` |
|---|---|---|---|
| `index.html` | 0 | 0 | 0 |
| `plithos_saints.html` | 0 | 1 (read only) | 0 |
| `plithos_reader.html` | 0 | 0 | 0 |

The calendar *links out* to `plithos_saints.html#n=<name>`, and the saints page
reads that hash on entry — but never writes it. Nothing else has URL state at
all. Consequences: no shareable link to a saint, prayer, work, or chapter; the
back button does not work within a page; nothing is bookmarkable; and search
engines have nothing to index. This is the root cause behind both D5 and much
of the "not intuitive" feeling.

### D7 — Google Fonts is a hard third-party dependency

All pages block on `fonts.googleapis.com` for Fraunces, Spectral, and IBM Plex
Mono. Render-blocking, a GDPR consideration, and a hard failure where Google is
blocked — including regions matching offered UI languages. `_headers` already
has a `woff2` rule, so self-hosting is straightforward.

### D8 — Chrome is inconsistent across pages

`index.html` has a footer with the pastoral disclaimer; `plithos_saints.html`
and `plithos_reader.html` have none. The saints page does not read
`plithos.lang`, so language choice does not survive navigating to it.

### D9 — The New Testament names its books in English in nineteen languages

`NT_BOOK_NAMES` in `library.html` carries Greek and Ukrainian and nothing
else, so a Russian reader opening the New Testament finds "John" over the
chapter, and a Romanian one finds "Matthew". The Old Testament does not have
this problem: `scripture/index.json` carries `names` per language and
`scripBookName()` reads them.

It became more visible with the Scripture search, which cites every hit by
book, but it is not caused by it - the reader has always shown these names.
Twenty-seven books across the seventeen remaining New Testament languages.
The received forms are well attested in each language's own printed
Testament, so this is transcription rather than translation.

### D10 — `/assets` and `/data` are one badly timed request from a dead file

Cloudflare answers a path it does not have with the whole of `index.html` and
a `200`, and `_headers` holds anything under `/assets/*` or `/data/*` for a
year as `immutable`. A deploy is not atomic across the edge, so a request for
a newly shipped file in the wrong minute is answered with the calendar, and
that answer is then cached for a year. `assets/plithos-ui.v3.css` was lost
this way within a minute of shipping and had to be abandoned for `v4.css`.

Mitigated by procedure, not by code: ship an asset in one commit, confirm it
answers through a cache-busting query string, point the pages at it in the
next. Written up in `CLAUDE.md` and beside the rule in `_headers`. Nothing in
the repository can detect the fault, because it lives in the edge cache.

---

## 4. The five requested items, sized

| # | Item | Assessment |
|---|---|---|
| 1 | Extend the library | **Very tractable, and half-built.** The lazy-load mechanism already exists (D2); `tools/ingest.py` already fetches, normalises to house style, and emits the right schema. Extending is mostly catalogue data entry. ANF/NPNF is 38 volumes against your 25 works. |
| 2 | Saints' lives in 22 languages | **Much the largest item.** 427,857 words × 21 languages ≈ **9.0 million words** of hagiography. The page has no i18n mechanism at all, so that must be built first. Given your instruction to source authentic translations before generating any, the realistic first step is a survey of what public-domain translated synaxaria actually exist per language — that will differ enormously by language and will determine the order of work. |
| 3 | More intuitive | Deep links (D6) first; then the language-honesty problem in §2; then consolidation. |
| 4 | Android and Apple apps | Start with a PWA (D4). |
| 5 | Contact section | **Done** — `contact.html`, 22 languages, five routed addresses. |

---

## 5. Additional recommendations

Ordered by value-to-effort.

1. **Fix D2** — every Library visit wastes 6.8 MB today.
2. **Fix D1** — three languages silently broken.
3. **Deep links and shareable URLs (D6)** — the biggest usability and SEO win.
4. **`robots.txt` + `sitemap.xml` + pre-rendered saint pages (D5).**
5. **Be honest about language coverage** — either finish the 14 partial UI
   languages or mark them as partial in the picker. Silently serving an English
   interface under a Japanese flag is the worst of both.
6. **Split the monoliths.** 6.8 MB parsed before first paint is slow on the
   mid-range Android phones much of the audience uses. Moving `SAINTS`,
   `CORPUS`, and `SYNAXARION` to fetched JSON needs no build step.
7. **Self-host fonts (D7).**
8. **PWA + offline (D4).**
9. **Dark mode.** Used at matins and compline; the CSS is already fully
   custom-property-based, so it is unusually cheap.
10. **Deuterocanon for the masoretic languages** — 11 languages lack the
    Orthodox canon.
11. **Surface the CC BY attribution** for the Portuguese scripture.
12. **Unify the OT/NT scripture architecture.**
13. **Reading settings** — font size, line height, typeface.
14. **"Today" as the landing state** — the day's saints, readings, and fast
    above the fold.
15. **Audio** — chant and read lives; also serves visually impaired and
    elderly users.
16. **Update the stale header comment** in `index.html`.

---

## 6. Repository notes

- `docs/_headers.alternate.txt` is your second `_headers` variant. Not live.
- `data/bible.v1.{bn,cu,ka,ur}.b64` are **deliberately absent** — the live
  server returns `index.html` for them (D1), so there is nothing correct to
  commit.
- `tools/ingest.py` hardcodes `LIB = Path("/home/claude/lib")` and needs a
  relative path before reuse.

## The masthead said different things on different pages

Fixed 2026-08-10. The seven nav links looked identical from page to page and
did not read identically. Each page painted them from its own table, under
its own attribute name:

| page | attribute | languages with all seven links |
|---|---|---|
| calendar | `data-i18n` | 22 |
| Saints | `data-ui` | 3 (en, el, ru) |
| Library | none | 0 - never translated |
| Prayers | `data-t` | 22 |
| the Rule | none | 0 - never translated |
| Glossary | `data-t` | 22 |
| Contact | `data-t` | 22 for four links, 0 for Prayers, the Rule and Glossary |

So a reader in French met his own language on the calendar and English on
the Saints page; a reader in Georgian met it on the Prayers page and English
on the Library. The words themselves also drifted where two pages did carry
them: the Saints page called the Rule page Устав where every other page
called it Правило, and the calendar and the other three disagreed on the
Chinese for Saints and Library, the Japanese for Calendar, Library and
Prayers, the Armenian for Saints, the Hindi for Calendar, and six of the
seven Syriac words.

`tools/nav_chrome.py` now owns the words as well as the design. Every one of
the twenty-two languages already had all seven words written somewhere on
the site, so the table was gathered, not composed; where the pages disagreed
the reading most of them already showed the reader is the one kept.

Three of those readings are worth a second opinion from someone who has the
language, since they were settled by counting pages rather than by judgement:

- **hi** Calendar is `पंचांग`, which is properly the Hindu almanac. The
  loanword `कैलेंडर` stood on the calendar page alone.
- **zh** Library is `图书馆`, the building. `文库`, a collection, stood on the
  calendar page and may suit a shelf of the Fathers better.
- **ja** Library is `図書室`, a reading room, against `ライブラリ` on the
  calendar page.

The one reading not settled by counting is the Greek Rule, which three pages
gave polytonic as `Ὁ Κανόνας` while the six Greek words beside it are
monotonic. It is set monotonic; a nav bar in two orthographies reads as a
mistake.

## Scripture

### The New Testament was the lectionary wearing the New Testament's name

The site carried a New Testament in nineteen languages. In eighteen of them it
carried only the verses the lectionary reads.

A Russian reader who opened the Apocalypse was given the seventh chapter and
no other - the one read on the Sunday of All Saints. Luke stood at 486 verses
of 1,151, Mark at 452 of 678, Acts at 596 of 1,007. Philemon was in no
language but English. Every language but English held 5,899 verses of the
7,957 that are there.

Nothing said so, and nothing could. The book list looked complete because
every book was named, and every book was a quarter of itself. No check asked
how much of a named book was present.

The numbering was worse than the absence. Where a verse had been dropped, the
verses after it moved up to fill the space, so Matthew 3:16 in Russian gave
the words of 3:17. A citation could not be trusted to land where it pointed,
in eighteen languages, and a reader had no way to know.

None of it was ever short at the source. Each edition has been fetched again
whole and numbered as its own edition numbers it, and
`tools/check_site.py` now refuses a bundle of fewer than 27 books or fewer
than 7,800 verses, which is the check whose absence let this stand.

Six of the nineteen could not be restored as they were:

  - **French and Portuguese** were published from an edition that could not be
    identified. Every French and Portuguese Bible obtainable was compared
    against the published text and none matched above six per cent, while the
    Library's entry named Ostervald and Martin over it. Each now reads the
    edition this site's own Old Testament reads - Darby, and the Biblia Livre
    - so that the two halves are one Bible.
  - **Chinese** is offered here as 简体中文 and was being served the Union
    Version in traditional characters, with a space set between every glyph.
    Same translation, the script the reader asked for.
  - **Swahili** came from a source that does not carry Philippians at all.
  - **Arabic** is Van Dyke as printed, with the vowel points, which the
    published copy had stripped.
  - **Romanian** was Cornilescu, a Protestant translation whose author died in
    1975. It now reads the Holy Synod's edition of 1914, the Orthodox Church
    of Romania's own and the edition its Old Testament already came from.

Church Slavonic had an Old Testament here and no New Testament; it now reads
the Elizabeth Bible of 1751 on both sides.

### What was added, and what is still missing

Swahili, Hindi, Bengali and Urdu now have an Old Testament, and Bengali and
Urdu a New Testament. What is left is **Georgian**, which wants a New
Testament, and **Armenian** and **Syriac**, which want Old Testaments.

### The structural reason, corrected

It was written here that the open ecosystem carries nothing beyond the
Protestant canon: that bible.helloao.org holds 1,256 translations in 1,004
languages and not one has more than sixty-six books. The count is right and
the conclusion drawn from it was wrong. helloao serves eBible's texts and
drops their deuterocanonical books; **eBible's own catalogue lists thirty-two
editions that carry them**, and three of those are in languages this site
already offers - a Spanish with sixteen deuterocanonical books, a French with
fifteen, a Portuguese with fifteen, all public domain and all revised this
year.

That matters, because Spanish, French and Portuguese readers here have
thirty-nine books and cannot open Wisdom or Sirach or the Maccabees at all.
The editions that would give them those books exist and are free. They are
modern free translations rather than the received Reina-Valera, Darby and
Almeida, which is a real cost and a real decision, and it has not been taken
yet.

The lesson is narrower than the old paragraph made it: **do not take a
catalogue's summary of another catalogue for the catalogue itself.** The
count came from an aggregator's book totals, not from eBible's own manifest,
which states the deuterocanonical count in a column of its own.

### The method that works, and its one hard requirement

The seventeen Old Testaments that were here first came from historic printed
editions, out of copyright by age and made before or apart from that
reduction: Brenton of 1851, the Elizabeth Bible of 1751, the Synodal of 1876,
Luther of 1545, Diodati of 1649, the Sagradas Escrituras of 1569, the Romanian
Synod's of 1914.

The requirement is that somebody must already have **transcribed** the
edition. A scan is not enough. The Romanian succeeded because a wiki had typed
the 1914 out, chapter by chapter, with the verse numbers marked.

### Georgian, in particular

Georgian has a complete Old Testament here - thirty-nine books of Old
Georgian, the Mtskheta recension. Only the New Testament is missing, and the
gap looks implausible for a nation of five million Orthodox with a scriptural
tradition of sixteen centuries. It was searched for properly:

  - **It is in no open catalogue at all.** Not eBible, whose full manifest of
    1,550 texts was read and holds no Georgian under any name; not CrossWire's
    SWORD modules, whose 462 packages and attic were listed; not wldeh's two
    hundred and ten versions; not bolls.life's thirty-one languages; not one
    of the thousand and four languages helloao carries.
  - **Georgian Wikisource has no Bible.** Searching it for the word returns
    conference proceedings; searching it for the Gospel returns manuscript
    catalogues.
  - **TITUS at Frankfurt has the Old Georgian gospels** and states on the page
    that no part may be republished in any form without prior permission. The
    text is fifteen centuries old; their edition of it is not, and it is
    theirs.
  - **The modern Georgian is under copyright** to the Bible Translation
    Institute in Stockholm and the Georgian Bible Society, 2002.
  - **The one copy on the Internet Archive marked public domain is modern.**
    That was checked rather than assumed: it carries two hundred and
    twenty-five modern forms and no archaic ones. The mark on it is an
    uploader's, not a verified one.
  - **holybible.ge answers, and was not taken from.** It is a React front end
    over an unauthenticated endpoint. Enumerating its parameters would produce
    a text with no edition named and no licence known, which is the one thing
    this site may not publish. It is somebody's site, not a source.

What would answer it: a transcription of the Bakar Bible of 1743, the first
printed Georgian Bible, or permission from TITUS.

### Spanish and Portuguese: what "the Orthodox one" can mean

No Orthodox Bible was ever made in either language, so the question is not
which of several to take but whether any free edition carries the canon the
Church reads. Settled on 23 August, and the answer is narrower than it looked.

**The received texts do not carry it.** Every Reina-Valera and every Almeida
in every free catalogue is sixty-six books - Reina Valera 1909, Reina Valera
Gomez, even the Valera 1602 Purificada, which is a modern revision that
dropped them. Reina printed the deuterocanonical books in the Biblia del Oso
of 1569 and Valera kept them in 1602, but nobody has transcribed either
printing with them.

**Wikisource has no full Bible in either language.** The Spanish Sagrada
Biblia there - Torres Amat, which does carry the whole canon in print - is
twenty-four book pages, mostly the New Testament, with no Genesis and no
deuterocanon. The Portuguese Almeida of 1819 is Genesis, Exodus and Matthew.
That route worked for French, where Giguet's Septuagint is transcribed and
proofread across all four volumes; it does not work here.

**Three editions carry the whole canon and all three are modern.** eBible has
`spabll`, the Santa Biblia libre Latinoamericano, with sixteen
deuterocanonical books; `spablm` with fifteen; and `porbrbsl`, the Biblia
Portuguesa Mundial, with fifteen. All three are public domain and all three
were revised this month.

So the choice is a real one and it has a cost on both sides. Keeping
Reina-Valera and Almeida keeps the translation those readers know and leaves
them unable to open Wisdom, Sirach, Tobit, Judith or the Maccabees at all.
Taking the free editions gives them the books the Church reads and takes away
a text many know by heart.

The instruction is to carry the Orthodox canon by default, however that looks,
so it is `spabll` for Spanish and `porbrbsl` for Portuguese, and the entry for
each says what edition it is. Neither is on bible.helloao.org, which is what
tools/ingest_scripture_ebible.py reads, so this wants a reader for eBible's
own USFM rather than a line in a table.

### Armenian and Syriac

Both looked closer than they are.

**Armenian.** The Zohrab Bible of Venice, 1805, is the Armenian Church's own
and carries the wider canon, and it is out of copyright by two centuries.
Armenian Wikisource has it - and has six books of it: Genesis, Exodus,
Leviticus and Ruth under one title, Genesis and Exodus under another. eBible
has no Armenian at all. CrossWire has two modules, and the Eastern one holds
Genesis, Exodus and the Gospels and says so in its own configuration file.
The rest of the Zohrab exists as page images on the Internet Archive and has
not been transcribed by anyone.

**Syriac.** CrossWire's Peshitta module lists an Old Testament in its file
manifest, and the files are there: `ot.bzv` carries an index of 24,115 verse
records, and `ot.bzs` and `ot.bzz`, which hold the text those records point
into, are **zero bytes long**. The index is complete and the text is not
there at all. This was found by reading the bytes; the module's own
description promises the whole Bible. eBible has no Classical Syriac, only
Assyrian Neo-Aramaic, which is a modern language and would not stand beside an
Old Georgian-era Peshitta New Testament.

### The Syriac New Testament has a Latin V where Hebrews wants a final mim

Thirty verses of the published Syriac New Testament carry the Latin letter
`V` in place of a final mim. They are a single run - Hebrews 6:20, 7:1-6,
7:9, 7:11, 7:13-15, 7:17, 7:19, 7:21, 7:24-28, 8:3, 8:5, 9:2, 9:12, 9:14,
9:15, 9:22, 9:24, 9:27, 10:1 - and the fault is mechanical, not editorial:
`ܠܥܠV` for `ܠܥܠܡ`, `ܐܒܪܗV` for `ܐܒܪܗܡ`, `ܟܠܡܕV` for `ܟܠܡܕܡ`,
`ܫܠܝV` for `ܫܠܝܡ`, `ܡܕV` for `ܡܕܡ`, `ܩܐV` for `ܩܐܡ`. It has been in the
file since `bible.v1.arc.b64` - twenty-seven verses then, thirty since the
v3 rebuild - and it is in `bible.v4.arc.b64`, which is what a reader is
served today. No other language has anything comparable: the Latin
characters counted in the other bundles are the Latin-script languages
themselves, or three strings of metadata.

The whole of Hebrews 7 is the epistle's argument about Melchizedek, so the
passage a reader most wants when he looks up that name is exactly the
passage that is broken.

Found while writing the Syriac life of Melchizedek, which quotes nothing in
consequence and reports the epistle as prose. Not fixed here: repairing it
means bumping the family to `bible.v5.arc.b64`, adding the new stem to
`_headers`, and repointing every page, and text of Holy Scripture is not
something to amend without asking first.

## Romanian keeps the 1914 edition's own verse numbers

The Synod's Bible of 1914 does not divide its verses where a modern Bible
does, and Isaiah 7 is the clearest case: it runs to twenty-four verses where
the common numbering has twenty-five, because it keeps as one verse what the
other splits at "and the son of Remaliah". Everything after that point in the
chapter therefore stands one number earlier, and the prophecy of Emmanuel -
"iata fecioara in pantece va lua si va naste fiu" - is printed as Isaiah 7:13
and not 7:14.

That is the edition's versification and not a fault in the reading of it. The
span the page carries and the number the edition prints agree with each other
throughout; both were checked against each other before this was concluded.
The Septuagint divides Isaiah differently from the Hebrew in several places
and this edition follows the Septuagint, which is why it is here.

So the numbers are kept as the Synod set them. CLAUDE.md forbids correcting an
edition, and renumbering a Bible to agree with a different one would be the
largest correction on this site. What it costs is that a reference taken from
a modern lectionary may land a verse away in Romanian, and a reader who knows
the verse will find it beside where he looked. What the alternative would cost
is a Bible that says the Synod printed something it did not.
