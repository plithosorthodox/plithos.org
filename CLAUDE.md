# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

The source for **plithos.org** — a free Orthodox Christian companion covering
the liturgical calendar, the daily saints and feasts, the fasting rule,
traditional prayers, the writings of the Holy Fathers, and Holy Scripture,
across many jurisdictions and languages.

Hosted on **Cloudflare Pages**. There is no build step: the files in this
repository are exactly what is served.

## Architecture

Three self-contained HTML applications. Each one inlines its own CSS, JS, and
primary dataset — there are no shared assets and no module system.

| File | Size | What it is |
|---|---|---|
| `index.html` | 6.8 MB | Calendar, feasts, fasting rule, prayers, search. The main app. |
| `plithos_saints.html` | 3.6 MB | Browsable saints index — 1,454 saints. |
| `plithos_reader.html` | 7.0 MB | The Library: patristic works + scripture reader. |

There is also `contact.html` (small, self-contained, its own 22-language table)
and one **shared** layer used by all four pages:

```
assets/plithos-ui.css              dark theme + command palette styling
assets/plithos-ui.js               command palette (Ctrl/Cmd-K) + theme toggle
```

This is the only shared code on the site. It is deliberately additive: it
reads no page internals, mounts itself into `header nav`, and re-themes the
pages by overriding the custom properties they all declare.

Data loaded on demand from `/data` and `/scripture`:

```
data/prayers-i18n.v1.<lang>.json   21 languages, 100 prayers each
data/bible.v1.<lang>.b64           New Testament; base64 of zlib-deflated JSON, inflated with pako
data/library/works-index.json      catalogue of lazy-loaded library works
data/library/<work_id>.json        one work's units, fetched when opened
data/search-index.v2.json          global search index, built by tools/build_search_index.py
scripture/index.json               book list, per-language availability, editions
scripture/<lang>/<n>.json          Old Testament by book number, 16 languages
tools/ingest.py                    builds library works from public-domain patristic sources
tools/build_search_index.py        regenerates data/search-index.v2.json
tools/ingest_canons.py             builds the conciliar canons from CCEL's NPNF2-14
```

### Adding a library work

`plithos_reader.html` lazy-loads anything listed in
`data/library/works-index.json`; the embedded `CORPUS` is only the original
core. To add a work: emit `data/library/<work_id>.json` in the
`{work: {...}, units: [...]}` shape, append its catalogue entry to
`works-index.json`, then re-run `tools/build_search_index.py`. No HTML changes
needed. **Every entry in `works-index.json` must have a matching file** - a
catalogue entry with no file shows in the UI and opens empty.

The catalogue entry must use the field names the reader reads: `work_id`,
`title`, `author`, `date`, `translator`, `pub_year`, `source`, `source_class`,
`description`, `digitized`. Anything else is silently not displayed.

When a source is paginated one unit to a page, derive the structure from its
table of contents rather than hand-listing section prefixes.
`tools/ingest_canons.py` did the latter first and dropped seven councils
without a single error; the counts per council are known numbers, so check
them.

### The Cloudflare Pages catch-all

Requesting a path that does not exist returns **HTTP 200 with the whole 6.8 MB
of `index.html`**, not a 404. So `if (r.ok)` is never a sufficient guard on a
`fetch`. Always check the content type as well:

```js
var ct = (r.headers.get("content-type") || "").toLowerCase();
if (ct.indexOf("json") < 0) return null;
```

Three separate silent 6.8 MB-per-load bugs on this site came from this.

### Editing the big HTML files

Their embedded data is written as **one enormous single line** (`const SAINTS=[...]`,
`const CORPUS = {...}`, `const PRAYERS=[...]`). Consequences:

- Do **not** try to read these files whole — you will blow out the context
  window. Locate the assignment, slice it, `json.loads` it, work on the
  parsed object, and write the line back.
- `Edit` with a small unique anchor works fine for markup and CSS. It does not
  work well inside the data lines.
- Prefer a Python script under `tools/` for any data-shaped change, so the
  transformation is repeatable and reviewable.

### Languages

22 UI languages, defined in `LANG_NAMES` in `index.html`:

```
en el ru ro uk de es ar fr pt it sr ka zh ja ko sw hy arc hi bn ur
```

`cu` (Church Slavonic) also appears in `scripture/` and the liturgy texts, but
is not a UI language. Translation coverage is uneven — see `docs/BASELINE.md`.

## Commands

No toolchain, nothing to install. To preview locally:

```bash
python3 -m http.server 8000    # then open http://localhost:8000
```

Note that `_headers` and `_redirects` are Cloudflare Pages directives and have
no effect under a local static server; extensionless routes like `/saints`
only work in production.

## Conventions

- **Match the surrounding file.** These files have a consistent house style —
  compact CSS, `var(--porphyry)` custom properties, ES5-flavoured JS with
  `function` declarations and `var`. Follow what is there rather than
  modernising it.
- **No new dependencies.** No framework, no build step, no new CDN `<script>`
  tag, no bundler. The zero-dependency design is deliberate. Ask first.
- **Shared chrome is duplicated across all four pages.** A change to the
  masthead, nav, or footer must be applied to `index.html`,
  `plithos_saints.html`, `plithos_reader.html`, and `contact.html`
  separately. Only `assets/plithos-ui.*` is genuinely shared.
- **Cache invalidation applies to `/assets` too** - it is cached for a week,
  so a change there takes up to seven days to reach returning visitors.
- **House text rules** (enforced by `tools/ingest.py`, follow them by hand too):
  no em or en dashes — use hyphens; straight quotes, not smart quotes;
  paragraphs separated by one blank line.
- **Accessibility:** meaningful `alt` on images, keyboard-operable controls,
  WCAG AA contrast.

## Voice of the site

Everything a visitor can see - page copy, notices, `alt` text, `title`
attributes, HTML comments, and comments in `/assets` - is written in the
site's own editorial voice. It is the voice of a publisher of the Church's
texts, and its authority rests on faithful transmission.

**Never let the machinery show.** Do not mention translation "passes",
pipelines, builds, scripts, generation, indexes, batches, data files, or
anything that frames the content as processed rather than published. Do not
mention automated or machine translation even to deny it - a denial still
raises the question. Do not reference tool filenames in served files.

| instead of | write |
|---|---|
| "Translation is a separate pass and has not been done" | "Definitions in the other languages are still in preparation" |
| "nothing here is machine-translated" | say nothing; do not raise it |
| "auto-generated from the corpus" | "drawn from the sources listed" |
| "run `tools/x.py` to regenerate" | keep it out of served files entirely |

Working notes belong in `docs/` and in commit messages, which are not
deployed. `.assetsignore` keeps `tools/`, `docs/` and `CLAUDE.md` out of the
upload; nothing in those files reaches a reader.

State what a thing *is*, not how it was made. "Definitions are given in
English for now" is complete. Anything further is process talk.

## Content

This is an Orthodox Christian site. Content includes liturgical text,
scripture, saints' lives, feast days, and Greek, Church Slavonic, Syriac, and
Georgian scripts.

- **Never paraphrase, modernise, "correct", or invent liturgical or scriptural
  text.** Reproduce sources exactly. If something looks wrong, ask rather than
  fixing it.
- **Never invent hagiography.** A saint's life, feast date, jurisdiction, or
  relics must come from a real source. Do not fill gaps with plausible prose.
- Preserve diacritics and non-ASCII exactly; every page must declare
  `<meta charset="utf-8">`.
- Record provenance for any added library work: translator, publication year,
  source volume, and licence. Only public-domain texts.
- **Only add a work the Church received, and only from before its author left
  her.** Tatian's *Address to the Greeks* was written while he was still in the
  Church; his Encratite writings are not here and are not to be added. Clement
  of Alexandria's *Instructor* and *Stromateis* are here; the *Hypotyposes*, on
  which the censure of Photius fell, is not. Check the reception before adding,
  not after. Where reception is itself the question, say so in the entry's
  `caution` field - `tools/reception.py` holds those notes and is the one place
  they are written.
- **Do not give the title of a saint to anyone the Orthodox Church does not
  venerate.** Origen, Tatian, Eusebius, Athenagoras and Clement of Alexandria
  are listed under their names alone. `tools/tag_library.py` carries the
  judgement for every author on the shelf as an explicit flag, so it is stated
  once rather than inferred from a name.
- A saint venerated by the Church but absent from the Saints index is a gap
  worth filling, particularly where the Library holds his writings; add him
  with `tools/add_saints.py`, which writes both the index and the calendar.
  Cite the synaxarion the commemoration comes from. Most of the index follows
  the calendar of the Orthodox Church in America; where a saint is commemorated
  elsewhere, name that source in the entry.

## Cache invalidation

`_headers` caches `/data/*` as `immutable, max-age=31536000`. Content filenames
therefore **carry a version** (`prayers-i18n.v1.el.json`). If you change a file
under `/data`, you must **bump the version in the filename** and update every
reference in the HTML, or returning visitors will keep the old copy for a year.

This applies to files nothing in the HTML names directly. The search index is
fetched by `assets/plithos-ui.v*.js`, not by a page, and it went several
content changes without a bump because the reference was one level away. It is
now `search-index.v2.json`, and `tools/check_site.py` compares the name the
shared script asks for against the name the builder writes. When you bump the
index you also bump the shared script, since its content changes with it, and
that means editing all seven pages. `data/search-index.v1.json` stays where it
is: it was served immutable, so browsers hold it, and pages held from before
the bump still ask for that exact name.

### Stamping a publication

The pages themselves are revalidated every visit, but a browser that cached a
page **before** those headers were in place keeps it under heuristic freshness
for days, and the reader is never told: the site looks live, and a section that
has since moved simply does nothing when tapped.

So every page carries `<meta name="plithos-build">`, `version.json` carries the
build now published and is never cached at any layer, and `assets/plithos-ui.*.js`
refetches a page whose stamp does not match. **Run `tools/stamp_build.py`
whenever a page changes**; `tools/check_site.py` fails if the stamps and
`version.json` disagree.

`assets/plithos-ui.js` - the unversioned name - is not dead. It is a recovery
shim for pages held from before the stamp existed, which still ask for that
exact name and cannot be changed. Leave it in place.

This reaches nothing older than the shared asset layer. A page that predates it
loads no same-origin script at all, so it can only expire or be cleared by hand.

## Working agreements

- Ask before anything destructive or hard to reverse — deleting pages,
  restructuring directories, rewriting git history, changing DNS or Cloudflare
  configuration.
- Do not commit or push unless asked.
- Report honestly. If something is untested or partly done, say so.

## Known issues

See `docs/BASELINE.md` for the current state audit and the open defect list.
