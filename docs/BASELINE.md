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
