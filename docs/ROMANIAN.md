# Romanian: where the translation stands

Working notes. Not deployed.

Russian and Greek are complete on the Saints page. Romanian is the third
language, and it is being written the same way: one language at a time,
completely, before the next is begun.

## The four things a language needs

| what | written in | built by |
|---|---|---|
| the names | `tools/saint_names/` | `tools/build_saint_names.py` |
| the vocabulary beside a life | `tools/saint_terms/ro.py` | `tools/build_saint_terms.py` |
| the lives themselves | `tools/saint_lives/ro.py` | `tools/build_saint_lives.py` |
| the calendar entries | `tools/saint_info/ro.py` | `tools/saint_info_i18n.py` |

The names were already done; the other three are new. The order taken here
is vocabulary, then lives, then calendar entries, because the vocabulary is
what a reader meets first and it stands beside every card on the page.

## Done: the vocabulary

`tools/saint_terms/ro.py`. Ten thousand six hundred and thirty-two phrases,
of which about eleven hundred are the pieces the place-names are assembled
from - a card names a town, a province and a country in one line, and the
same town turns up inside twenty other lines, so the pieces are rendered
once in `PARTS` and `expand()` builds the wholes. `expand()` also builds the
title that is nothing but the place again, "of Ancyra" from Ancira, so a
town cannot be spelled one way in the place line and another in the title
above it. The rest are written out.

**10,632 of 10,632.** `python3 tools/build_saint_terms.py --check` reports
`ro 10,632 of 10,632`, beside Greek and Russian.

| field | count | state |
|---|---|---|
| the small closed sets, ranks, canonizations, baptismal names | 309 | done |
| the pieces the places are built from | 1,076 | done |
| the places, patronal places, origins, regions | 1,625 | done, via `expand()` |
| how else a saint is named | 980 | done |
| where a saint's relics rest | 749 | done |
| the callings a saint keeps | 1,572 | done |
| the kindred commemorations | 1,476 | done |
| how a saint is written in an icon | 1,407 | done |
| the intercessions asked of a saint | 2,622 | done |

### The register

Romanian has its own received words where the English uses Greek or Latin
ones, and they are used: **Cuvios** for the monastic saint, **Sfintit
Mucenic** for the hieromartyr, **Mare Mucenic**, **Nebun pentru Hristos**,
**Purtator de patimi**, **Doctor fara de arginti**, **Stalpnic**,
**Mironosita**, **Facator de minuni**, **Sobor** for a synaxis, **Ctitor**
for a founder. A Slavic prince is a **Cneaz** and a Moldavian one a
**Domn**, which is what each is called in Romanian and not a distinction
the English makes.

Place-names take the forms Romanian usage has received - Constantinopol,
Tesalonic, Nicomidia, Cezareea, Efes, Chiev - and where no received form
exists the name is transliterated. Diacritics are written in full.

## In progress: the lives

`tools/saint_lives/ro.py`, 1,456 lives. **267 of 1,456 written**, in the
order `tools/build_saint_lives.py` reads the index, which is alphabetical by
the English name: the numbered feasts, the afterfeasts and forefeasts, the
apostles of the Seventy, the blessed fools for Christ, the great martyrs and
the whole run of the hieromartyrs are done, and the file is at the letter H.

Six lives a batch is a comfortable size; the long ones run past four hundred
words and the register has to hold across all of them, so the count matters
less than keeping the voice steady. After each batch:

    python3 tools/build_saint_lives.py --check
    python3 tools/build_saint_lives.py --write
    python3 tools/check_site.py

No page changes, so no stamping is needed for the lives. That changes with
the calendar entries.

## Then: the calendar entries

`tools/saint_info/ro.py`, 1,456 entries, merged into `index.html` by
`python3 tools/saint_info_i18n.py --write`, so the build has to be stamped on
every batch or `tools/check_site.py` fails:

    python3 tools/saint_info_i18n.py --write
    python3 tools/stamp_build.py
    python3 tools/check_site.py

Most calendar entries are literal prefixes of the index life for the same
saint, so the Romanian is already written once the lives are: open the
finished life, find the sentence the English prefix stops at, and take the
Romanian down to the matching point. Cutting by counting sentences or
characters is not safe and was rejected in Greek for the same reason - the
punctuation does not correspond clause for clause, and a mis-cut produces a
truncated entry no one would catch. The cut is made by eye.

## The trap to remember at the end

`data/saint-terms.v2.ro.json` is a new file, so nothing holds a stale copy
of it today. But it is served `immutable, max-age=31536000`, and every
sitting rewrites it under the same name. A reader who opens the Saints page
in Romanian while the vocabulary is a tenth written will hold that tenth for
a year.

So when Romanian is finished, **bump the filename version** - terms, lives
and names together if they have all moved - and update the fetch in
`plithos_saints.html`. This is the same defect that was found in the lives
and fixed by moving them to `v2` once Greek was complete;
`tools/check_site.py` compares the name the page asks for against the name
the builder writes.

## Then

The remaining eighteen languages, one at a time, completely: Ukrainian,
Serbian, Arabic, Georgian; then es, fr, it, pt, de; then sw, ja, ko, zh;
then hy, arc, hi, bn, ur.
