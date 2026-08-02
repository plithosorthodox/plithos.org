# plithos.org — baseline audit

State of the site as committed. Verified against the live site on 2026-08-02:
`index.html` served from plithos.org is **byte-identical** to the copy in this
repository apart from Cloudflare's injected analytics beacon, so this
repository is an accurate mirror of production.

---

## 1. What exists

### Pages

| Route | File | Size |
|---|---|---|
| `/` `/calendar` `/prayers` | `index.html` | 6.8 MB |
| `/saints` | `plithos_saints.html` | 3.6 MB |
| `/reader` `/library` | `plithos_reader.html` | 7.0 MB |

### Calendar and prayers (`index.html`)

- Full liturgical year: fixed and movable feasts, Paschalion, fasting rule with
  a five-level colour legend, multiple jurisdictions, ICS export by day/month.
- 100 prayers, categorised, with source notes.
- Saint blurbs for the calendar (`SYNAXARION` / `SAINT_INFO`); the file header
  notes "blurbs through March complete (1047 lives)" — so the calendar's own
  saint blurbs are roughly a quarter of the year short.
- Fully internationalised across 22 languages: `I18N`, `NAMES_I18N`,
  `NOTES_I18N`, `SAINT_INFO_I18N`, `PRAYERS_I18N`, `SITE_INFO_I18N`,
  `KEY_I18N`, `FASTNOTE_I18N`, `BOOK_I18N`, `CAT_I18N`, `TAGLINE_I18N`.

### Saints (`plithos_saints.html`)

- **1,454 saints**, filterable by name, day, order, place, attribute,
  jurisdiction, century, era.
- 28 fields per saint. Coverage is strong on the core fields and thin on the
  optional ones:

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

- **English only.** There is no i18n mechanism on this page at all — no
  language JSON is fetched, no language switcher. This is item 2 on your list.
- Prose volume: **396,823 words** of lives + **31,034 words** of icon
  descriptions = **427,857 words** per language.

### Library (`plithos_reader.html`)

`CORPUS` holds 49 catalogue entries / 782 units / **1,164,695 words**. But the
entries are not all texts:

| kind | entries | units | note |
|---|---|---|---|
| Patristic works with real text | **25** | 782 | the actual library |
| Bible catalogue stubs (`bible-*`) | 19 | 0 | pointers to `/data` NT files |
| Divine Liturgy entries | 5 | 0 | metadata only, **no text loaded** |

So the library is genuinely **25 works**. Present:

Athanasius (3), Basil (2), Justin Martyr (2), John of Damascus,
John Chrysostom (*On the Priesthood* only), Gregory of Nazianzus,
Gregory of Nyssa, Cyril of Jerusalem, Clement of Rome, Ignatius, Polycarp,
Barnabas, Diognetus, Papias, Athenagoras, Tatian, Theophilus,
Vincent of Lérins, Martyrdom of Polycarp, the Nicene Creed,
and the canons of the Seven Ecumenical Councils.

### Scripture

Two **separate and inconsistent** delivery systems:

| | Old Testament | New Testament |
|---|---|---|
| consumed by | `plithos_reader.html` | `index.html` |
| path | `scripture/<lang>/<n>.json` | `data/bible.v1.<lang>.b64` |
| format | plain JSON | base64 of zlib-deflated JSON, inflated with pako |
| languages | 16 (`ar cu de el en es fr it ja ka ko pt ru sr uk zh`) | 19 |
| size | 70 MB | ~7 MB |

Neither set covers all 22 UI languages, and the two sets do not cover the same
languages.

---

## 2. Defects found

### D1 — Missing NT data causes a silent 6.8 MB download on every page load

**Severity: high.** `data/bible.v1.<lang>.b64` does not exist for **`bn`
(Bengali), `ka` (Georgian), `ur` (Urdu)** — three of the 22 offered UI
languages. (`cu` is also absent but is not a UI language.)

Cloudflare Pages has a catch-all that returns **HTTP 200 with the 6.8 MB body
of `index.html`** for any missing path. The loader in `index.html`:

```js
fetch("data/bible.v1."+L+".b64")
  .then(function(r){ return r.ok ? r.text() : null; })   // r.ok is TRUE — it's a 200
  .then(function(t){
     if(!t) return;
     var b = atob(t.trim());                             // throws: HTML isn't base64
     ...
     bibLoaded[L] = true;                                // never reached
  })
  .catch(function(){})                                   // swallowed silently
```

Consequences for a Bengali, Georgian, or Urdu reader:

1. 6.8 MB is downloaded and thrown away.
2. `atob` throws; the error is silently swallowed.
3. Scripture silently falls back to English with no message.
4. Because `bibLoaded[L]` is never set, **this repeats on every single page
   load** — it never caches the failure.

Two fixes, both wanted: validate the response before decoding (check
`content-type`, or that the body matches `/^[A-Za-z0-9+/=]+$/`), and build the
three missing language files.

### D2 — `_headers` emits conflicting `Cache-Control` on `/data/*`

**Severity: medium.** `/data/*` matches two rules in `_headers` — the `/data/*`
block and the `/*.json` block — and Cloudflare concatenates both. Live response:

```
cache-control: public, max-age=31536000, immutable, public, max-age=604800
```

Two conflicting `max-age` values in one header. Browsers take the first, so the
effective policy is **one year, immutable**. Any re-upload of a
`prayers-i18n.v1.*.json` file without a filename version bump will not reach
returning visitors for a year. `/scripture/*` has the same double-match, though
harmlessly (both say 604800).

Note: `docs/_headers.alternate.txt` is a second variant of this file you
uploaded, which uses `max-age=604800` for `/data/*` instead of immutable. It is
**not** what is live. Decide which policy you want and keep only one.

### D3 — No PWA, offline support, or install target

None of the three pages reference a `manifest.json`, a service worker,
`apple-touch-icon`, or `theme-color`. This matters directly for item 4 on your
list: a PWA is the shortest credible path to "an app", and offline access is
the single most valuable feature for a prayer and calendar app (church
basements have no signal).

### D4 — No `robots.txt`, no `sitemap.xml`

The site has careful per-page SEO metadata (canonical, OpenGraph, Twitter
cards, keywords) but nothing telling a crawler what exists. With 1,454 saints
and 25 works locked inside three JS-rendered pages, essentially none of that
content is indexable. This is the biggest missed reach opportunity on the site.

### D5 — Google Fonts is a hard third-party dependency

All three pages block on `fonts.googleapis.com` for Fraunces, Spectral, and IBM
Plex Mono. That is a render-blocking cross-origin request, a GDPR
consideration for EU visitors, and a hard failure in regions where Google is
blocked — including some where you offer a UI language. Self-hosting the
`woff2` files is straightforward and `_headers` already has a rule for them.

### D6 — No contact route

No email address, contact form, or `mailto:` appears anywhere in the three
pages. This is item 5 on your list; the Cloudflare routing already exists.

### D7 — Divine Liturgy entries have no text

The five `divine-liturgy-chrysostom-*` catalogue entries (en, de, el, cu, ro)
carry metadata but zero units, so they appear in the library and open empty.

---

## 3. Your five items, sized

| # | Item | Assessment |
|---|---|---|
| 1 | Extend the library | **Very tractable.** `tools/ingest.py` already does this — it fetches New Advent, normalises to house style, and emits the exact `CORPUS` schema. It ships with a one-entry catalogue and an unused `ingest_multipage()` helper. Extending the `CATALOGUE` list is mostly data entry. ANF/NPNF is 38 volumes; the obvious next tier is Chrysostom's homilies, Augustine, Cyril of Alexandria, Ephrem, Maximus, Gregory the Great, the Philokalia (where public domain), and the Apostolic Constitutions. |
| 2 | Translate saints' lives into 22 languages | **By far the largest item.** 427,857 words × 21 additional languages ≈ **9.0 million words** of religious prose where accuracy is doctrinally serious. This needs a plan of its own: machine translation is not acceptable unreviewed for hagiography. Realistic approach is to build the i18n *mechanism* first (the page has none), ship 2–3 high-demand languages with review, and grow. |
| 3 | More intuitive and user friendly | Needs specifics — see suggestions below. |
| 4 | Android and Apple apps | **Start with a PWA** (D3). It is days rather than months, works on both platforms, gives offline access, and is a prerequisite for a good wrapped app anyway. Native/Capacitor store submission is a separate, larger decision. |
| 5 | Contact section | **Small.** A day's work including the i18n strings. |

---

## 4. Additional suggestions

Ordered by value-to-effort, highest first.

1. **Fix D1.** Three languages are silently broken and burning 6.8 MB per load.
2. **Add `robots.txt` + `sitemap.xml`, and pre-render saint pages (D4).**
   1,454 saints at stable URLs (`/saints/john-chrysostom`) would multiply the
   site's discoverability. Currently a search for any individual saint cannot
   find you.
3. **Split the monolith files.** 6.8 MB of HTML parsed before first paint is
   slow on the mid-range Android phones much of your target audience uses.
   Moving `SAINTS`, `CORPUS`, and `SYNAXARION` into fetched JSON would cut
   time-to-interactive dramatically without adding a build step.
4. **Self-host fonts (D5).**
5. **PWA + offline (D3)** — install prompt, offline calendar and prayers.
6. **Finish the calendar blurbs** — currently complete only through March.
7. **Fill the Divine Liturgy texts (D7).**
8. **Deep links and shareable URLs.** The apps appear to hold state in JS
   rather than the URL, so a reader cannot link to a specific saint, prayer, or
   chapter. This is the single biggest "intuitive and user friendly" win (item
   3) and it also feeds SEO.
9. **Dark mode.** A prayer app is used at matins and compline in the dark. The
   CSS is already fully custom-property-based, so this is unusually cheap.
10. **Reading settings** — font size, line height, and a serif/dyslexic toggle.
11. **"Today" as the landing state**, with the day's saints, readings, and
    fasting rule above the fold.
12. **Audio.** Chant recordings and read lives would be a significant
    differentiator, and serve visually impaired and elderly users.
13. **Consistent scripture architecture.** Unify the OT and NT delivery paths
    so a language is either fully supported or visibly marked as partial.
14. **Language coverage matrix in the UI** — be honest about what is translated
    rather than silently falling back to English.
15. **Analytics beyond Cloudflare's beacon** — you have no view of which
    languages, saints, or works people actually use, which should drive the
    translation priority order in item 2.

---

## 5. Repository notes

- `docs/_headers.alternate.txt` is your second `_headers` variant, kept for
  reference. Not live.
- `data/bible.v1.{bn,cu,ka,ur}.b64` are **deliberately absent** — the live
  server returns `index.html` for them (D1), so committing what it serves
  would commit 6.8 MB of wrong content four times.
- `tools/ingest.py` is the library builder. Its `LIB` path is hardcoded to
  `/home/claude/lib` and will need to be made relative before reuse.
