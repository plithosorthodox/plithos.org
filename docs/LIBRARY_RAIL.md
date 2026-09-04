# The Library's rail: decisions made once

Working notes. Not deployed.

The Library's left rail and its shelf headings come to 113 strings a
language: seven shelf descriptions, the sentence under the title, eight
counting patterns, the name of Church Slavonic, and the ninety-three tags a
work carries - the subjects, the uses, the centuries and the authors.
`tools/loop_ui.py <lang> --next` derives what is missing from the pages
themselves; the renderings live in `tools/ui_i18n/<lang>.py`.

These decisions were settled from what the site already publishes and are
recorded here so they are not settled again, differently, in the twentieth
language.

## The author is looked up, not decided

Every author on the shelf who is a saint is already named in
`NAMES_I18N` in `index.html`, in all twenty-one languages, because the
calendar commemorates him. So the rail takes the calendar's form rather
than composing a new one: Свт. Иоанн Златоуст is spelled out as
Святитель Иоанн Златоуст, Sfântul Ioan Gură de Aur is taken whole,
Άγιος Ιωάννης ο Χρυσόστομος likewise.

The rank carries the honorific, and the abbreviation the calendar uses for
want of room is spelled out, because the rail is a browsing list and not a
dense calendar line. The monastics take the monastic rank in every language
that keeps one apart: Όσιος Εφραίμ ο Σύρος, Преподобный Ефрем Сирин,
Cuviosul Efrem Sirul. That is why the Romanian rail says **Cuviosul Ioan
Damaschin** where the calendar says Sfântul: `tools/check_register.py`
counts the plain honorific before a monastic's name an error, and the rail
is not the place to keep an old slip alive.

Where the English label and the received name disagree about a see, the
received name wins, since it is the one a reader of that language knows:
St Methodius of Olympus is Священномученик Мефодий Патарский in Russian
and Sfințitul Mucenic Metodie al Patarei in Romanian, because Patara is
what those Churches call him.

The authors the Church does not number among the saints stand under their
names alone, as `tools/tag_library.py` has them: Origen, Clement of
Alexandria, Eusebius of Caesarea, Dionysius the Areopagite.

## Mathetes is the word, not a man

The letter to Diognetus is ascribed in the shelf to **Mathetes**, which is
not a name: it is μαθητής, the Greek for a disciple, and the Ante-Nicene
Fathers put it where an author's name goes. So the rail gives each language
its own word for a disciple - Ученик, Ucenicul, Ein Schüler, ܬܠܡܝܕܐ - which
is exactly what the Greek rail does by keeping Μαθητής. Transliterating it
would hand every reader outside Greek a proper name that never existed.

## The counting patterns

`cnt*` are patterns and `%1` is where the number goes. Only two forms are
offered, a singular and a plural, and a language with three or more numeral
classes cannot be served exactly by two. The site had already settled this
in Russian on the Library page itself - `fTitle` is название and `fTitles`
is названий - so the patterns follow: nominative singular against genitive
plural, and no attempt to smuggle a third form in.

## The centuries

The calendar writes them short, for want of room: `IV в.`, `sec. IV`,
`Δ΄ αι.`. The rail has room, so it writes the word out - IV век, secolul
IV, Δ΄ αιώνας - and keeps the numeral system the calendar chose for that
language, which for Greek is the Greek numerals, ΣΤ΄ for the sixth and not
6ος.

## Where the terms come from

`data/glossary-i18n.v1.<lang>.json` already carries 177 ecclesiastical
terms in every language, and a good part of the rail's subjects are among
them. Θέωσις, Обожение, Îndumnezeire for Deification; Богородица,
Născătoarea de Dumnezeu for the Theotokos; the Divine Liturgy, the
Eucharist, baptism, chrismation, confession, relics, the councils. The
glossary's own `lgNames` settles the name of Church Slavonic in all
twenty-one, so `lang:cu` is never composed either.

Where the glossary and the prayers disagree, the prayers win, because they
are the Church's own books.

## Done

All twenty-one languages report 0 remaining:

    for l in el ru ro uk de es ar fr pt it sr ka ja sw hy ko zh arc hi bn ur; do
        python3 tools/loop_ui.py $l --status | head -1
    done

2,373 renderings, 113 to a language, plus the day's-lives link that
`index.I18N` grew while the run was in progress. The rail is written; nothing
of it is installed until `tools/build_ui_i18n.py` is run, which belongs to the
parent session.

Three languages needed a decision the queue could not make, and all three were
settled from what the site already publishes rather than by ear:

  - **Armenian**: classical orthography, per docs/ARMENIAN.md. The Library's own
    chrome is reformed; that file records the divergence as a defect in those
    strings, and the prayers win.
  - **Syriac**: unvocalized, per docs/SYRIAC.md. The glossary's vocabulary is
    taken and its East Syriac pointing is not, because the other three bodies
    do not point. The seyame stays, being the plural and not a vowel.
  - **The monastic honorific**: seven languages had a monastic under the plain
    word for holy in the calendar - John of Damascus in Romanian, German,
    Spanish, Portuguese, Italian, French, Armenian, and the same in Georgian,
    Japanese, Korean, Chinese, Hindi, Bengali, Urdu, Arabic and Syriac. The
    rail gives him the monastic rank in every one of them, because
    `tools/check_register.py` counts the bare honorific before a monastic's
    name an error and the rail is not the place to keep an old slip alive.
