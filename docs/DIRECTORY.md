# The directory of Churches

A worldwide list of Orthodox Christian Churches, dioceses, parishes and
monasteries: where they are, what they call themselves, and how to reach
them. It is published at `/churches`.

This file is the decision, made once, so it does not have to be argued
again each time a hard case turns up. The hard cases are the reason the
page exists in the shape it does.

## The bar for entry

**A body appears here because an autocephalous Church lists it among its
own.** That is a fact about a published list, not a judgement about the
body. The site records who says what; it does not say who is right.

A community that no autocephalous Church lists simply has no row, and the
page never says why. That is the point. It means the directory can leave
out a monastery that has fallen out with everyone without publishing an
accusation about it, and it means no one has to maintain a register of
grievances. Silence is the whole mechanism, and it is deliberate.

There is no `caution` field and no warning text, and none is to be added.
A warning is a claim the site would have to defend, keep current, and
eventually answer for, about a named community with named leadership. The
bar already does the work.

## The register, not the verdict

Where Churches disagree - the live case being Ukraine - the directory does
not resolve it.

Both bodies get a row. Each row says **who lists it**, with the source. The
reader who came for the dispute gets the actual state of it; the reader who
came for a liturgy on Sunday gets an address. Plithos never says which is
right, and never has to revise itself when a synod changes its mind: only
the recognition line moves.

This was chosen over the alternative, which was to name one Church as
authoritative when Churches conflict - in practice, deferring to the
Ecumenical Patriarchate as first among equals. That was rejected for two
reasons. It turns a record into a position, and the site's authority rests
on faithful transmission, not on adjudication. And it does not survive its
own first application: under such a rule the Orthodox Church in America,
whose autocephaly Constantinople does not recognise, would be demoted by a
rule written about Ukraine, and several hundred real parishes with it.

**Primacy is kept for order, not for arbitration.** The Churches are listed
in the order of the diptychs, which is a received sequence, and sorting a
page by it is faithful rather than partisan.

## What a row records

Every row carries the source it was read from and the date it was read.
Both are shown to the reader. A stale row is then visible as stale, rather
than quietly wrong.

    id          stable key, never reused
    kind        church | autonomous | diocese | parish | monastery | seat
    name        as the source's own list prints it
    styled      the body's own English designation, where its site was read
    local       as it styles itself in its own language, where published
    seat        the city
    country     ISO 3166-1 alpha-2
    address     as printed by the source
    site        the URL that answers, after redirects
    order       diptych position, for sorting
    listed      who lists it, where that is not universal
    standing    one factual sentence, only where recognition differs
    source      the URL the row was read from
    checked     the date it was read

`listed` and `standing` each carry their own source URL beside them, because
a recognition is a different claim from an address and is not read off the
same page.

**No telephone numbers, for now.** It is the field that goes stale
invisibly: the numbers on the list read here still carried a Moscow
dialling code retired in the 1990s, and nothing about the entry said so. A
website that answers is a better address than a number that does not.
Numbers come back per row as each body's own site is read.

`listed` and `standing` are absent on a row nobody disputes. Their absence
means no dispute is recorded - not that the site has looked and found none.

**Names are not translated.** A parish's name is its name, and the site
stores it as the body itself publishes it, with a Latin form only where the
body itself publishes one. What gets translated is the page's own words -
the headings, the kind labels, the country names - which is a bounded
vocabulary and the reason twenty-two languages cost nothing per row.

**No clergy names.** Not the parish priest, and not the primate either. A
see is stable and a man in it is not, and a directory that lists men is
out of date the week it is published. Where a title is wanted the
institutional one is used - "Archbishop of Athens and All Greece" - which
does not change.

## Where the rows came from

The spine was read on 13 September 2026 from the directory of world
Churches published by the Orthodox Church in America, and each website in
it was then requested directly and recorded at the address that actually
answered. Four of those addresses had moved or changed hands and the
published one was stale:

  - Constantinople: `patriarchate.org` now answers at `ec-patr.org`
  - Greece: `ecclesia.gr` now answers at `ecclesiagreece.gr`
  - Albania: `orthodoxalbania.net` now answers at `orthodoxalbania.org`
  - Sinai: `sinaimonastery.com` now answers under `/index.php/en/`

Four sites could not be read from here at all - Serbia, Cyprus, the Czech
Lands, and Macedonia refused the request rather than failing to answer.
Those four rows carry the OCA directory as their source, which is what was
actually read, and the date it was read. That is the honest record and it
is what the page shows.

The Orthodox Church of Ukraine is not in the OCA's list. Its row is read
from its own site and from the Patriarchal and Synodal Tomos published by
the Ecumenical Patriarchate.

## Rows deliberately not yet published

**The Estonian Christian Orthodox Church** (`orthodox.ee`, formerly the
Estonian Orthodox Church of the Moscow Patriarchate). Its own site does not
say which Church it belongs to, and no published list naming it has been
read here. Under the bar it has no row until one is. The Estonian Apostolic
Orthodox Church does have one, because Constantinople names it on its own
page of autonomous Churches.

This is the bar working rather than a gap: the answer to "why is one
Estonian Church listed and not the other" is that one was found in a
Church's own list and the other was not, and the moment the other is, it
gets a row on the same terms.

## The order of the work

1. The Churches themselves. Bounded, finishable, and complete as it stands.
2. Their dioceses. Several hundred rows, every one on an official site.
3. Parishes and monasteries, country by country, and only where an official
   directory exists that can be read again next year.

Worldwide parish coverage is tens of thousands of rows and will go stale.
Diocesan coverage will not. The site commits to the second and treats the
first as something added where it can be kept true, beginning with the
United States, where the Assembly of Canonical Orthodox Bishops publishes
one list covering every jurisdiction at once.

**Monasteries are a filter, not a section.** They are rows like any other
with `kind` set, so country, jurisdiction and kind are three filters over
one list. A separate section would duplicate every filter and split the
search.
