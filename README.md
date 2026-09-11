# plithos.org

Source for [plithos.org](https://plithos.org) - a free Orthodox Christian
companion: the liturgical calendar, the daily saints and feasts, the fasting
rule, traditional prayers, the writings of the Holy Fathers, and Holy
Scripture, in twenty-two languages.

Hosted on Cloudflare Pages. There is no build step: what is in this repository
is what is served.

## Layout

```
index.html              Calendar, feasts, fasting rule, search
saints.html             Saints index, 1,456 saints
library.html            The Library: patristic works and the scripture reader
prayers.html            The prayer book, 100 prayers
rule.html               The fasting rule
glossary.html           Terms
contact.html            Contact
embed.html              The calendar panel, for embedding elsewhere

data/                   Datasets fetched for the one language a reader chose
scripture/              Old Testament by language and book, 21 languages
assets/                 The only shared CSS and JS on the site
functions/              Cloudflare Functions: per-language routes and /api/day
app/                    Capacitor wrapper that ships the site as an Android app

tools/                  Builders, checkers, and the translation source modules
docs/                   Editorial authority per language, and the defect list
CLAUDE.md               Architecture and the rules that bind anyone editing
AGENTS.md               The same, for agents that do not read CLAUDE.md
```

`tools/` and `docs/` are not served; `.assetsignore` keeps them out of the
upload. They are, however, the source of truth for everything under `data/`:
the twenty-one language modules in `tools/saint_lives/`, `tools/saint_info/`,
`tools/saint_terms/` and `tools/ui_i18n/` are what the published bundles are
built from, and deleting them would leave the site unmaintainable.

## Routes

| Path | Serves |
|---|---|
| `/` `/calendar` | `index.html` |
| `/saints` | `saints.html` |
| `/library` `/reader` | `library.html` |
| `/prayers` `/rule` `/glossary` | their own pages |
| `/<lang>/...` | the same pages, language pinned, via `functions/` |
| `/api/day` | the day's calendar as JSON |

## The translation, finished 11 September 2026

Every one of the four tracks is now complete in all twenty-one translated
languages: **the vocabulary a life is built from, the interface, the 1,456
saints' lives, and the 1,456 calendar entries** that the day panel shows.

| | |
|---|---|
| Languages | 22 served, 21 of them translations of the English base |
| Translated items | 274,963 |
| Characters | 58.8 million, roughly 9.8 million words |
| Saints | 1,456, each with a long life and a sixty-word calendar entry |

Greek, Russian, Romanian, Ukrainian, German, Spanish, Arabic, French,
Portuguese, Italian, Serbian, Georgian, Chinese, Japanese, Korean, Swahili,
Armenian, Syriac, Hindi, Bengali and Urdu.

### How it was done, and how long it took

Roughly three weeks, from the third week of August to 11 September 2026.

The work was run by several agent sessions writing in parallel against a
shared branch. A small queue held the four tracks in dependency order -
vocabulary first, because the grammar of a life is drawn from it, then the
interface and the lives, and the calendar entries only once a language's lives
were complete. Each worker asked the queue what was unwritten, took a claim so
that two would not write the same saint, wrote a batch by hand, and pushed. A
language large enough to be worth it was worked from both ends at once by two
workers walking towards each other.

**That machinery has been deleted.** The queue, the claims file, the batch
driver and the standing orders that drove them are gone, because a repository
that still contains instructions to "take the next job" will eventually
persuade something to start translating a language that is already finished.
What remains of it is the part worth keeping: the editorial decisions, in
`docs/<LANGUAGE>.md`, and the checkers in `tools/`.

Each language was settled before it was written. The register - whether a
saint takes the bare word for holy or the rank his order gives him, how a
place is spelled, how a sentence ends - was decided from what the site already
published and written into that language's doc, so it was decided once.
`tools/check_register.py` enforces the part of it a script can see.

### What is verified, and what is not

The corpus is **complete** and **structurally sound**: every key present, every
rendering in the right script, no placeholders, no English left standing, and
the published bundles agree with their sources.

It is **not verified for accuracy or for veracity.** Nobody has read most of it
in the language it is written in. The known faults, and an honest account of
what a real review would cost, are in
[`docs/BASELINE.md`](docs/BASELINE.md) under the open defects of 11 September
2026. The largest of them are worth naming here: thirty Hindi lives quote
Scripture in the site's house spelling rather than the edition's, a run of
Arabic place names sits one key out of step, and thirty-two lives across
Syriac, Portuguese and Italian are materially shorter than their source.

## What comes next

Nothing below is started. It is the shape of the work as it stands today.

- **Repair first.** The open defects above, and the checkers themselves:
  `check_translations.py` reports some eleven thousand findings of which the
  great majority are locale artefacts - a full stop as a thousands separator
  in Portuguese and Romanian, ordinals as digits in Russian, Chinese counted
  short because Chinese is compact. A checker nobody trusts is why 7,622
  finished calendar entries sat unpublished for days without anything going
  red. Fixing its rules is a day and is the highest-value day available.
- **A published app.** `app/` holds a Capacitor wrapper that ships the site
  itself as an Android app. It has never been built, signed or submitted, and
  there is no iOS target.
- **An Orthodox assistant.** A companion that answers from this corpus rather
  than from the open internet, grounded in what the site publishes and
  refusing what it cannot ground. Intended in two forms: a general one, and an
  Orthodox one for laypeople, with the base level reachable from Plithos.
- **The Library, expanded and translated.** 97 works are catalogued, all of
  them in English. Two separate jobs: adding works the Church received and
  whose translations are public domain, and rendering what is already here
  into the other twenty-one languages. The second is larger than the entire
  saints' translation just completed, and should not be started until the
  review question above is answered.
- **Scripture coverage.** 21 languages carry an Old Testament. The canon rule
  in `CLAUDE.md` decides every edition question and is not negotiable: the
  edition carrying the books the Church reads wins.

## Local preview

```bash
python3 -m http.server 8000    # then open http://localhost:8000
```

`_headers`, `_redirects` and `functions/` are Cloudflare directives and do
nothing locally, so extensionless routes such as `/saints` and the per-language
routes only work in production.

## Before you edit

Read [`CLAUDE.md`](CLAUDE.md). Three things bite immediately:

- The HTML files embed their remaining datasets as **single enormous lines**.
  Do not open one whole; slice out the assignment and parse it.
- **Most of `/data` is cached immutable for one year.** Changing a file there
  without bumping the version in its filename will not reach returning
  visitors. The exceptions are declared in `_headers`; read it rather than
  assuming either way.
- A saint's life, feast date, jurisdiction or relics must come from a real
  source. Nothing here is paraphrased, modernised or filled in with plausible
  prose, and that rule is the reason the site is worth publishing.
