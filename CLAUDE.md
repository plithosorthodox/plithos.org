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
| `index.html` | 16.2 MB | Calendar, feasts, fasting rule, prayers, search. The main app. |
| `saints.html` | 3.7 MB | Browsable saints index — 1,454 saints. |
| `library.html` | 7.3 MB | The Library: patristic works + scripture reader. |

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

`library.html` lazy-loads anything listed in
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

A table of contents can also be wrong, so the count has to come from somewhere
else. The Nisibene Hymns are listed twice under one number in NPNF 2-13, and
one of the two entries is really the editor's note saying a hymn is missing.
De-duplicating the list resolved them into one, dropped the note, and yielded
exactly the number the entry claimed - the count agreed because both errors
were in the same direction. Take the expected number from what the edition
says about itself (its own preface or title page), not from the list you are
about to trust.

### The Cloudflare Pages catch-all

Requesting a path that does not exist returns **HTTP 200 with the whole 16.2 MB
of `index.html`**, not a 404. That figure grows with every language written:
it was 6.8 MB when this was first noted and is now more than twice that, so
the cost of the mistake grows too. So `if (r.ok)` is never a sufficient guard on a
`fetch`. Always check the content type as well:

```js
var ct = (r.headers.get("content-type") || "").toLowerCase();
if (ct.indexOf("json") < 0) return null;
```

Four separate silent whole-calendar-per-load bugs on this site came
from this. The fourth was the scripture bundles.

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
- **Shared chrome is duplicated across all seven pages.** A change to the
  masthead or footer must be applied to `index.html`, `saints.html`,
  `library.html`, `prayers.html`, `rule.html`, `glossary.html` and
  `contact.html` separately. Only `assets/plithos-ui.*` is genuinely shared.
- **The masthead nav is the exception, and it belongs to
  `tools/nav_chrome.py`.** Its design, its markup and its words in all
  twenty-two languages are written there and installed on all seven pages;
  run `python3 tools/nav_chrome.py --write` rather than editing a nav by
  hand. Every link carries `data-nav="<slot>"` and nothing else - not
  `data-i18n`, not `data-ui`, not `data-t` - because a page that keeps a nav
  word of its own is how the seven links came to be translated into
  twenty-two languages on the calendar, three on the Saints page and none at
  all on the Library and the Rule. A page announces a language change with
  `document.dispatchEvent(new CustomEvent("plithos:lang",{detail:L}))` and
  the nav repaints itself; the page does not repaint it.
- **A page's public URL is its filename.** Cloudflare Pages serves every
  `.html` file at its extensionless path and 308s the `.html` form to it, and
  that normalisation runs *before* `_redirects`, so a `200` rewrite declared
  there never takes effect. `/saints` was an alias for `plithos_saints.html`
  and answered every request with a redirect; the sitemap advertised it,
  Google followed it, and one page out of seven was indexed. To change a
  page's URL, **rename the file** and leave a `301` behind. Never paper over a
  filename with a rewrite. `tools/check_site.py` now reads `sitemap.xml` and
  fails if any entry redirects or disagrees with the page's canonical tag.
- **Every page needs a canonical URL, and it must be the URL that answers.**
  `saints.html` pointed its canonical at `/plithos_saints.html`, which is
  itself a redirect, and `plithos_reader.html` had no canonical at all.
- **Cache invalidation applies to `/assets` too** - it is served
  `immutable, max-age=31536000`, so a change there only reaches anyone under a
  new filename.
- **Never request a newly deployed file at its real URL until you know it is
  there.** A deploy is not atomic across Cloudflare's edge: `version.json` can
  report the new build while the same edge still answers `/assets/...` from
  the old one, and the answer to a path that does not exist is the whole of
  `index.html` with a `200`. Under the `/assets/*` and `/data/*` headers that
  catch-all is then **cached immutable for a year**, so one badly timed
  request permanently breaks the file for everyone behind that edge.
  `plithos-ui.v3.css` was lost that way within a minute of shipping and had to
  be abandoned for `v4.css`.

  So verify a new asset through a cache-busting query string, which fills a
  different cache key and cannot poison the real one:

  ```bash
  until curl -sI "https://plithos.org/assets/x.v9.css?probe=$(date +%s)" \
        | grep -qi 'content-type: text/css'; do sleep 10; done
  ```

  Only after that is the plain URL safe to fetch, and only then should the
  pages be pointed at it. Ship a new asset in two commits: the file alone
  first, the seven page references once the file answers.
- **House text rules** (enforced by `tools/ingest.py`, follow them by hand too):
  no em or en dashes — use hyphens; straight quotes, not smart quotes;
  paragraphs separated by one blank line.
- **Accessibility:** meaningful `alt` on images, keyboard-operable controls,
  WCAG AA contrast.

## Register: write the language, do not translate into it

Every language here is written, not converted. The test is not whether a
sentence is accurate; it is whether a reader who grew up in the language
would recognise it as something a person from his own Church wrote.

**A saint's honorific is his rank, not the word "Saint".** English has one
title and gives it to everyone. Most of these languages do not. Russian says
**преподобный** Сергий for a monastic, **святитель** Николай for a bishop,
**благоверный князь** Александр for a prince, **праведный** Симеон
Богоприимец for a righteous man, **мученица** Христина for a martyr. The
bare word святой stands before a rank, never before a name: святой апостол
Андрей is right and святой Андрей is the English sentence in Russian words.
Ukrainian works the same way. Greek keeps **Ὅσιος** apart from Ἅγιος for the
monastic saint; Romanian keeps **Cuviosul** apart from Sfântul for the same
reason. Romanian and Greek do allow the plain honorific before a name, so
only the monastic distinction is asserted for them.

`tools/check_register.py` enforces exactly this and nothing more:

```bash
python3 tools/check_register.py --lang ru
```

It reports two things and the difference matters. An **error** is a saint
introduced by the generic word for holy and no rank at all. A **review** is a
saint given some other real rank than his order would suggest, which a
calendar may legitimately do and a script may not judge. Add a language's
rank vocabulary to `LANGS` before beginning it, not after.

**This is the shape of the problem, not the whole of it.** The honorific is
the part a script can catch. Word order, the verbs a hagiography uses, which
clauses a language puts first, whether it says "was born in the city of X"
or simply "of X" - none of that is checkable, and all of it is what makes
the difference between a text that is understood and one that is read with
pleasure. Before starting a language, read a page of a real synaxarion in it
and write from that ear. Where a phrase has a received form in the language's
own liturgical books, use the received form and do not re-render it.

## Voice of the site

Everything a visitor can see - page copy, notices, `alt` text, `title`
attributes, HTML comments, and comments in `/assets` - is written in the
site's own editorial voice. It is the voice of a publisher of the Church's
texts, and its authority rests on faithful transmission.

**Never let the machinery show.** Do not mention "passes", pipelines, builds,
scripts, generation, indexes, batches, data files, or anything that frames the
content as processed rather than published. Do not reference tool filenames in
served files.

| instead of | write |
|---|---|
| "Translation is a separate pass and has not been done" | "Definitions in the other languages are still in preparation" |
| "auto-generated from the corpus" | "drawn from the sources listed" |
| "run `tools/x.py` to regenerate" | keep it out of served files entirely |

**Translation is the exception, and it is named plainly.** The site makes no
claim to reproduce texts exactly; it offers an edition, as any library does,
and says where that edition came from. So where **a whole work** is rendered
here rather than taken from a published translator, the entry says so, names
the tool, admits it is not the work of an expert or a native speaker, and asks
to be corrected. That is provenance, which is the site's whole business, and
it is the opposite of letting the machinery show: what is concealed is process,
what is declared is a source.

The threshold is the work, not the sentence. A translator's note belongs on a
book, a set of prayers, a life - something a reader could pick up and read as
a thing. It does not belong on a heading, a label, a short prayer supplied
where the language was missing, or a line filled in to complete a page that is
otherwise translated. Those are the ordinary work of publishing in twenty-two
languages, and a note on every one of them would say nothing except that the
site is nervous.

Three things stay human-translated: **Holy Scripture**, the **Divine Liturgy**,
and the other **liturgical texts**. Not because a claim of exactness is being
made about them, but because a reader meets them as the Church's own words in
her worship, and a rendering that has not been received by anyone should not
stand in that place. The Fathers, the prayers, the saints' lives and the site's
own copy may be rendered here where no published translation is available.

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
- **Do not correct an edition.** Titles, headings, spellings and section names
  are reproduced as the translator set them, including where a Western
  translator gives a Western title: John of Damascus' Dormition sermons are
  cited as *On the Assumption (koimesis)* because that is Mary Allies' heading
  and she prints the Greek herself. Where a heading is genuinely opaque on its
  own, explain it in the work's `description`, which is the site speaking in
  its own voice, and leave the citation alone. Renaming a section in the
  citation line is the site correcting a translator inside her own edition.
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
- **Where a source carries less than the whole work, say so in the entry.**
  New Advent prints 325 of the 366 letters it numbers for St Basil; the
  ingester asserts 325 and the description states it. A partial edition
  presented as the complete one is a quiet lie, and the reader has no way to
  detect it.
- A saint venerated by the Church but absent from the Saints index is a gap
  worth filling, particularly where the Library holds his writings; add him
  with `tools/add_saints.py`, which writes both the index and the calendar.
  Cite the synaxarion the commemoration comes from. Most of the index follows
  the calendar of the Orthodox Church in America; where a saint is commemorated
  elsewhere, name that source in the entry.

## The canon decides, before anything else

When choosing an edition of Holy Scripture for a language, **the edition that
carries the books the Church reads wins, always, and nothing outweighs it.**
Not familiarity, not that a translation is the received one, not that readers
know it by heart, not the beauty of its prose. An edition missing Wisdom,
Sirach, Tobit, Judith, Baruch or the Maccabees is not a smaller version of the
Bible; it is a different canon, and this site is not published in that canon.

The order is: an Orthodox edition first; failing that, whatever carries the
whole canon; and only where nothing carries it does the received text keep its
place, with the entry saying plainly what is missing.

This was got wrong once and is written down so it is not got wrong again.
Spanish was held on Reina-Valera 1909 and Portuguese on the Biblia Livre -
thirty-nine books each - on the reasoning that they are the translations those
readers know, and the recommendation was to leave them there. That reasoning
does not survive the question it was answered with: what is so good about a
translation that does not have the text? Both moved to editions carrying
fifty-one books, and both turned out to carry the Greek Daniel and the Greek
Esther and Psalm 151 as well, so the reader gained more than the count
suggested.

Where the choice costs something - an unfamiliar rendering in place of a loved
one - say so in the entry and in the commit. Do not hide the cost, and do not
let it decide.

## Cache invalidation

`_headers` caches `/data/*` as `immutable, max-age=31536000`. Content filenames
therefore **carry a version** (`prayers-i18n.v1.el.json`). If you change a file
under `/data`, you must **bump the version in the filename** and update every
reference in the HTML, or returning visitors will keep the old copy for a year.

**A new version needs a new rule in `_headers`, not just a new filename.**
The rules match on the versioned stem, so `bible.v2.*` matched nothing the day
the New Testament was bumped from v1. It fell through to the default and was
answered uncached for months: every reader who opened a reading pulled half a
megabyte again on every visit, and nothing failed. When you bump a family,
add the new stem to `_headers` in the same commit and leave the old stem
there, frozen.

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
