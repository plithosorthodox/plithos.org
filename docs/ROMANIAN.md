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

## In progress: the vocabulary

`tools/saint_terms/ro.py`. Ten thousand six hundred and thirty-two phrases,
of which about eleven hundred are the pieces the place-names are assembled
from - a card names a town, a province and a country in one line, and the
same town turns up inside twenty other lines, so the pieces are rendered
once in `PARTS` and `expand()` builds the wholes. `expand()` also builds the
title that is nothing but the place again, "of Ancyra" from Ancira, so a
town cannot be spelled one way in the place line and another in the title
above it. The rest are written out.

At the time of writing: **3,599 of 10,632**.

| field | count | state |
|---|---|---|
| the small closed sets, ranks, canonizations, baptismal names | 309 | done |
| the pieces the places are built from | 1,076 | done |
| the places, patronal places, origins, regions | 1,625 | done, via `expand()` |
| how else a saint is named | 980 | done |
| where a saint's relics rest | 749 | done |
| the callings a saint keeps | 1,572 | to do |
| the kindred commemorations | 1,476 | to do |
| how a saint is written in an icon | 1,407 | to do |
| the intercessions asked of a saint | 2,622 | to do |

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
