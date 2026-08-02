# Changelog

## Unreleased - presentation, discoverability, and three silent bugs

### The library roughly tripled

Fifteen works that had been built but never deployed are now installed under
`data/library/`. The reader already had a lazy-loading mechanism for exactly
this; only the files were missing.

| | before | after |
|---|---|---|
| works with text | 25 | **40** |
| units | 782 | **3,207** |
| words | 1.16 M | **3.34 M** |

Added: Cassian's *Conferences* and *Institutes*; Chrysostom's homilies on
Matthew, John, Romans and Hebrews, and *On the Statues*; Clement of
Alexandria's *Instructor* and *Stromata*; Eusebius' *Church History*; Origen's
*De Principiis*; Justin's *Dialogue with Trypho*; Gregory the Great's
*Pastoral Rule*; the *Shepherd of Hermas*; and the *Didache*.

`apostolic-constitutions` is listed in the uploaded catalogue but its units
file was not among the uploads, so it is **held back** - a catalogue entry
with no file shows in the UI and opens empty.

### Bugs fixed

- **Every Library visit wasted 6.8 MB.** `plithos_reader.html` fetched
  `data/library/works-index.json`, which did not exist. Cloudflare Pages
  answers a missing path with HTTP 200 and the whole of `index.html`, so
  `r.ok` was true, `r.json()` threw, and a bare `.catch(){}` swallowed it.
  The file now exists and the fetch checks the content type.
- **Bengali, Georgian and Urdu did the same on every page load**, via
  `data/bible.v1.<lang>.b64`. Same guard added, and the language is now
  marked settled whatever happens, so it no longer re-downloads forever.
- **`loadLibraryWork` had the same hole**; guarded too.
- **`_headers` emitted conflicting `Cache-Control`.** `/data/*.json` matched
  both `/data/*` and `/*.json`, producing
  `max-age=31536000, immutable, public, max-age=604800`. Rules are now
  mutually exclusive, and `/data/library/*` is deliberately short-cached
  because its filenames carry no version.
- **The Library home showed stale counts** ("The Fathers: 22 works") because
  `renderHome()` runs before the lazy catalogue arrives. It now re-renders.

### New

- **Command palette** on `Ctrl/Cmd-K` or `/`, on all four pages. Searches
  1,454 saints, 64 library entries, 100 prayers and 54 books of scripture in
  one box - the first thing on the site that spans all three apps. Backed by
  `data/search-index.v1.json` (299 KB), fetched once on first open.
- **Dark theme**, following the system preference and remembered per browser.
- **Deep links.** `index.html#prayer=<n>`, `index.html#day=MM-DD`,
  `plithos_reader.html#work=<id>`, `plithos_reader.html#book=<nr>`.
  `plithos_saints.html#n=<name>` already worked.
- `robots.txt` and `sitemap.xml`.
- `tools/build_search_index.py`.

### URL state - the other half of deep links

Deep links were entry points only; the pages now write state back to the
address bar, so the back button works and any view can be copied and shared.

| page | writes |
|---|---|
| `index.html` | `#day=YYYY-MM-DD` on any day click, `#prayer=<n>` on opening a prayer |
| `plithos_saints.html` | `#n=<name>` on opening a life, cleared on close |
| `plithos_reader.html` | `#work=<id>`, `#book=<nr>`, cleared on returning home |

Implemented by wrapping the existing open/close functions rather than editing
them, so the original logic is untouched and the whole layer lifts out again.
The reader guards this with a `booted` flag: `loadLibraryIndex()` re-renders
the home screen when the catalogue arrives, and `renderHome` clears the hash,
which would otherwise wipe an incoming `#work=` link before it was read.

### Two magnifiers, resolved by labelling rather than removing

The calendar's own search jumps to a day; the new palette searches the whole
site. They looked identical in the masthead. The calendar's is now labelled
**Day** (translated into all 22 languages) instead of being a bare icon.
Nothing was removed.

### Deployment

- `.github/workflows/deploy.yml` - dormant until credentials are added. Uses
  `cloudflare/wrangler-action`, since `cloudflare/pages-action` is deprecated.
- `tools/check_site.py` - pre-deploy gate. Catches catalogue entries with no
  file, missing scripture files, a stale search index, a page that lost the
  shared UI, and the `_headers` double-match. Exits non-zero.
- `.assetsignore` - keeps `tools/`, `docs/`, `.github/` out of the upload.
- `docs/DEPLOYING.md` - setup written for a first-time GitHub user, including
  why the simpler Cloudflare-watches-GitHub route is the better default here.

### Known gaps after this change

- Dark mode is a first pass. Colours hardcoded outside the custom properties
  are patched where found; more will surface on pages I have not exercised.
- The calendar does not yet put jurisdiction, language, or calendar mode in
  the URL - only the selected day. Sharing a link shows your day, but the
  recipient's own jurisdiction setting.
- The interface is still translated into 8 languages, not 22.
- `apostolic-constitutions` still needs its units file.
