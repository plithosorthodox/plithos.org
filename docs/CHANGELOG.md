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

### Known gaps after this change

- Deep links are **entry points only**: the pages still do not write state
  back to the URL, so the back button and "copy current view" do not work.
- Dark mode is a first pass. Colours hardcoded outside the custom properties
  are patched where found; more will surface.
- The calendar keeps its own magnifier for jumping to a day. Two search
  affordances on one page is not ideal and wants a decision.
- The interface is still translated into 8 languages, not 22.
