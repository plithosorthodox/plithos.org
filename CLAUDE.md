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

Data loaded on demand from `/data` and `/scripture`:

```
data/prayers-i18n.v1.<lang>.json   21 languages, 100 prayers each
data/bible.v1.<lang>.b64           New Testament; base64 of zlib-deflated JSON, inflated with pako
scripture/index.json               book list + groupings
scripture/<lang>/<n>.json          Old Testament by book number, 16 languages
tools/ingest.py                    builds library works from public-domain patristic sources
```

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
- **Shared chrome is duplicated across all three pages.** A change to the
  masthead, nav, or footer must be applied to `index.html`,
  `plithos_saints.html`, and `plithos_reader.html` separately.
- **House text rules** (enforced by `tools/ingest.py`, follow them by hand too):
  no em or en dashes — use hyphens; straight quotes, not smart quotes;
  paragraphs separated by one blank line.
- **Accessibility:** meaningful `alt` on images, keyboard-operable controls,
  WCAG AA contrast.

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

## Cache invalidation

`_headers` caches `/data/*` as `immutable, max-age=31536000`. Content filenames
therefore **carry a version** (`prayers-i18n.v1.el.json`). If you change a file
under `/data`, you must **bump the version in the filename** and update every
reference in the HTML, or returning visitors will keep the old copy for a year.

## Working agreements

- Ask before anything destructive or hard to reverse — deleting pages,
  restructuring directories, rewriting git history, changing DNS or Cloudflare
  configuration.
- Do not commit or push unless asked.
- Report honestly. If something is untested or partly done, say so.

## Known issues

See `docs/BASELINE.md` for the current state audit and the open defect list.
