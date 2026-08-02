# plithos.org

Source for [plithos.org](https://plithos.org) — a free Orthodox Christian
companion: the liturgical calendar, the daily saints and feasts, the fasting
rule, traditional prayers, the writings of the Holy Fathers, and Holy
Scripture, across many jurisdictions and 22 languages.

Hosted on Cloudflare Pages. No build step — what is in this repository is what
is served.

## Layout

```
index.html              Calendar, feasts, fasting rule, prayers, search
plithos_saints.html     Saints index (1,454 saints)
plithos_reader.html     Library: 25 patristic works + scripture reader

data/                   Prayer translations and New Testament bundles
scripture/              Old Testament by language and book
tools/ingest.py         Builds library works from public-domain sources
docs/BASELINE.md        State-of-the-site audit and open defects

_headers                Cloudflare cache and security headers
_redirects              Cloudflare route aliases
CLAUDE.md               Project context and conventions for Claude Code
```

## Routes

| Path | Serves |
|---|---|
| `/` `/calendar` `/prayers` | `index.html` |
| `/saints` | `plithos_saints.html` |
| `/reader` `/library` | `plithos_reader.html` |

## Local preview

```bash
python3 -m http.server 8000    # then open http://localhost:8000
```

`_headers` and `_redirects` are Cloudflare directives and do nothing locally,
so extensionless routes such as `/saints` only work in production.

## Before you edit

Read [`CLAUDE.md`](CLAUDE.md). Two things bite immediately:

- The three HTML files embed their datasets as **single enormous lines**. Do
  not open them whole — slice out the assignment and parse it.
- `/data` is cached **immutable for one year**. Changing a file there without
  bumping the version in its filename will not reach returning visitors.

Current known defects are listed in [`docs/BASELINE.md`](docs/BASELINE.md).
