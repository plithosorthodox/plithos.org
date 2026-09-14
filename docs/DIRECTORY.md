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

Both bodies get a row. Each row **names an act and who did it**, with the
source: the Ecumenical Patriarchate bestowed a Tomos in January 2019; the
Council of the other Church amended its own Statute in May 2022 in terms it
says testify to its full independence. The reader who came for the dispute
gets the actual state of it; the reader who came for a liturgy on Sunday
gets an address. Plithos never says which is right, and never has to revise
itself when a synod changes its mind: only the record of acts grows.

**This is the second attempt at that field and the first one was wrong.** It
was called `listed` and held the name of a Church that names the body among
its own. On the Ukrainian row it came out as "Listed by The Orthodox Church
in America", which was true and read as though the Orthodox Church in
America held some authority over a Church many times its size. It did not
even carry information: its source URL was the same one the row already
showed, because the Orthodox Church in America was simply where the entry
had been read.

Two things had been run together - **where a row came from**, which is
provenance and belongs to `source`, and **what was done about a body's
standing**, which is an act with an author and a date. Naming the first as
though it were the second turns a bibliography into a hierarchy. A row now
reports acts, attributed, and provenance is the separate line it always
was.

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
    parent      the id of the Church a diocese hangs off
    name        as the source's own list prints it
    styled      the body's own English designation, where its site was read
    local       as it styles itself in its own language, where published
    seat        the city
    country     ISO 3166-1 alpha-2
    address     as printed by the source
    site        the URL that answers, after redirects - written only where
                the link is the body's own, and left off otherwise
    site_of     the id of the body the link belongs to, where it is not the
                row's own; derived, and written by hand only where a Church
                answers on a domain other than the one its row declares
    founded     what the body says about its own beginning, in the words its
                source prints - optional, and left off unless published
    order       diptych position, for sorting
    standing    one sentence naming an act and who did it, with its source,
                where a reader would otherwise be misled
    sources     one to three URLs the row was read from
    checked     the date it was read

**A row may cite up to three sources, and the reason is the reader.** One
address that has gone dead should not be the end of his search. Three is the
cap, because a list of citations nobody will follow is not provenance, it is
decoration.

**The minimum a row needs is a name, a country and a citation.** A seat and
an address are wanted and are not required. A see this site can name and
point at is worth a row even where nobody publishes where it sits: a reader
who learns that a diocese exists, and where to read about it, has been given
something, and a body left out entirely because its address could not be
found has been hidden from him.

`standing` carries its own source URL beside it, because an act of a synod
is a different claim from an address and is not read off the same page.

## Whose website it is

Two hundred and forty rows had no site of their own and were given the front
page of their Patriarchate under the plain word Website. That tells a reader
the Greek Orthodox Metropolis of France has a website. It has not; what it
has is a page about it on ec-patr.org, and the difference is the whole
question for anyone trying to reach it.

So a row writes `site` only where the link is the body's own door. Where it
is not, the page names the body the link does belong to and puts the link
under that name instead:

    Website:                        The Church of Constantinople:
    ort.fi/oulunhiippakunta         ec-patr.org

The page shows the Church above as well where a body has a site of its own,
so that a link gone dead is not the end of the reader's search. Where the two
are on the same host it shows one line, not two.

This is derived, so a lane does not have to think about it: declare `site`
when the body has one and leave it off when it does not. The one case that
cannot be derived is a Church that answers on a domain other than the one its
own row declares - the two churches in China are published by Moscow at
mospat.ru while the Church of Russia's row declares patriarchia.ru - and
there the row says `site_of="russia"` itself.

## The year a body gives for itself

`founded` is optional and is taken, never composed. A see that says it was
founded in 1219 and one that says it was restored in 1992 are both saying
something true about themselves, and neither is this site's to reduce to a
number the source did not print. So the field holds the words the source
used, and a row whose source says nothing about a beginning simply has no
`founded`.

Take it where the page is already open. It is not worth a second fetch, and
a directory that is right about where a body is matters more than one that is
charming about when it began.

## When the Church does not publish an address

The rule is still that a row is read from an official source: the body's own
site, or the Church it belongs to. That is what establishes a body exists and
what it is called, and nothing else may establish it.

An address is a different kind of fact. Where a Church publishes none - and
many do not, and some publish one that has gone stale - the address may be
taken from a general source, a map listing among them, and cited as what it
is. It is a street, not a claim about who is in communion with whom, and a
reader who wants to visit is better served by an address from a map than by
no address at all.

Two limits hold. A general source may never be the only citation on a row:
the body's own page, or its Church's, has to be there establishing that the
body exists. And the row cites the page the address actually came from, so a
reader can see which fact rests on which source.

**A row with a name and a citation and nothing else is a good row.** It says
a diocese exists and where to read about it, which is more than a reader had
before. Do not hold one back for want of a street.

**A link that did not answer is not published.** The postal address stays,
because a reader can still use it, and the row simply carries no link.
Several of the Ecumenical Patriarchate's eparchies are in this position: the
address it prints for Spain no longer resolves at all, and Sweden, Korea and
Hong Kong did not answer here. Those are to be re-checked, not written off.

**No telephone numbers, for now.** It is the field that goes stale
invisibly: the numbers on the list read here still carried a Moscow
dialling code retired in the 1990s, and nothing about the entry said so. A
website that answers is a better address than a number that does not.
Numbers come back per row as each body's own site is read.

`standing` is absent on a row nobody disputes. Its absence means no dispute
is recorded - not that the site has looked and found none.

**Three kinds of text sit on a row, and they are not the same kind of
thing.** This was got wrong first time and is written down so it is not got
wrong again.

  - The **address** and the **site** are never translated. One goes on an
    envelope and the other into a browser, and both are reproduced exactly
    as the body itself prints them. So is the body's own name in its own
    language.

    The country is the single exception, and the rule the post itself goes
    by is why. Everything the destination has to read stays in the words the
    body prints, because a Turkish postman reads the Turkish. The country
    line is not read by the destination at all; it is read where the letter
    is posted, and the Universal Postal Union has it written in the language
    of the country of origin - the sender's, which here is the reader's -
    with an internationally known form added beside it. So the country
    appears in the reader's language with the English after it, and every
    line above it appears exactly as published.

    The label over the block is the page speaking and is translated, with
    the colon each script writes: a full-width one in Chinese and Japanese,
    the ordinary one everywhere else.
  - The **name** and the **seat** are translated. The first draft said they
    were not, on the reasoning that a name is a name - but "The Church of
    Constantinople" is not a proper name at all. It is the English label of
    the list the row was read from, and in Greek it should read as Greek.
    A city likewise has a received form in all twenty-two, and this site's
    own saints' lives are full of them.
  - The **page's own words** - headings, group labels, the caveat, the
    country chips - were translated from the first day.

The row names and seats are kept one language to a file under
`tools/directory_names/`, so the work can be handed out and nothing
collides. A key a language has not been given yet simply falls back to
English for that row alone, which is what lets a half-finished language
still read. `tools/directory_words.py --audit` reports how far each
language has got, and fails on any word that language does not already use
somewhere else on this site.

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

## A row cites its own, or nobody

Reading the Church of Serbia's address off another Church's directory is how
the entry was got, and printing that other Church on the row made it look
like an authority over this one. It is the same fault the `listed` field had
and it had been left standing in the confirmation line.

So the rule is now one rule. **A row names its source when the source belongs
to it - the body itself, or the Church it belongs to - and otherwise names
nobody.** The fourteen dioceses of the Orthodox Church in America go on
citing that Church, because it is theirs. The ten Romanian eparchies cite
the Romanian Patriarchate and the Ecumenical Patriarchate's eparchies cite
the Ecumenical Patriarchate, for the same reason. That is the level above,
and it is what a body with no site of its own should point to.

Four rows were re-read from where they belong: the Czech Lands and Slovakia
and the Bulgarian diocese in America from their own sites, the Romanian
Metropolia of the Americas from the Romanian Patriarchate's own list of its
eparchies, and the Greek Orthodox Archdiocese of America from the Ecumenical
Patriarchate's list of its eparchies in America.

Seven remained that were read off a body unconnected with them: Antioch's
archdiocese in North America, Cyprus, Georgia, Greece, Macedonia, Serbia and
the Ukrainian Orthodox Church. Their provenance stays in the data and the
page shows none, `tools/check_site.py` names them every run, and each is to
be read again from its own site or from its own Church. Showing nothing is
honest; it is not finished.

Six of the seven have since been read from their own, and every one of them
answered. The Church of Greece is at ecclesiagreece.gr behind a splash page,
and its Greek portal and its contact page both open from there. The
Macedonian Orthodox Church - Ohrid Archbishopric answers at mpc.org.mk over
plain http and not over https, and its row carries the Serbian Church's own
report of the Tomos confirming its autocephaly, handed over on 5 June 2022 -
an act and who did it, which is what `standing` is for. The Antiochian
Archdiocese of North America answers at antiochian.org and the Ukrainian
Orthodox Church at church.ua, each with its own name in its own title.

What none of the four publishes on a page this machine can read is a postal
address, so each row keeps the address it had. Two of those addresses want
looking at again for a different reason: the Ukrainian Orthodox Church's is
written in transliteration rather than in Ukrainian, which is not how an
address on this page is supposed to read, and the street it names was
renamed. An address is only worth having in the form a postman would take.

**The Church of Georgia is not one of them and is not to be written off.**
patriarchate.ge answers with two hundred kilobytes and no text: a cyber
security interstitial, thrown at requests from here rather than at readers.
That is not a dead site and its silence is not evidence about the Church. It
needs a route this machine does not have, and until it has one the row keeps
the provenance it has and shows nobody.

The Orthodox Church of Ukraine is not in the OCA's list. Its row is read
from its own site and from the Patriarchal and Synodal Tomos published by
the Ecumenical Patriarchate.

## Rows that were deferred, and are no longer

**The Estonian Christian Orthodox Church** was held out for want of a
published list naming it. Its own site said nothing about its jurisdiction
and no Church's list carried it, and the entry here said plainly that the
moment one did, it would get a row on the same terms as every other.

That happened. The Holy Synod of the Russian Orthodox Church named it a
self-governing Church within the Moscow Patriarchate on 10 April 2025, and
the row went in citing that act and attributing it, as every contested row
here does. Its own site still says nothing about jurisdiction, so nothing on
the row is said in its own voice.

The bar worked exactly as written, which is the point of writing a bar down:
the answer to "why is one Estonian Church listed and not the other" was that
one had been found in a Church's own list and the other had not, and when
the other was, no argument had to be had.

## The order of the work

1. The Churches themselves. Done.
2. Their dioceses. North America is done and complete for that continent,
   the Ecumenical Patriarchate's eparchies in Europe and Asia are in, and so
   are the Romanian Patriarchate's own. The rest follows Church by Church.
3. Parishes and monasteries, country by country, and only where an official
   directory exists that can be read again next year.

### Why North America was the first continent

Not because it matters most, but because the bishops of every canonical
Church on it sit in one Assembly, and that Assembly publishes one list of
its jurisdictions. That is exactly what a register wants: not one Church's
view of who is present, but the view they hold together. Fourteen
jurisdictions came from it, and the Orthodox Church in America's own
fourteen dioceses from its own directory, and the chancery address of each
was then read off that body's own site wherever the site would answer.

The Georgian Apostolic Orthodox Church in North America has no row yet. The
Assembly names it and gives a social media page rather than a site, and no
address for it was found. It is deferred for an address, not excluded - the
same treatment the Estonian row got, and for the same reason.

### And then the Throne's own eparchies

Twelve more, from the Ecumenical Patriarchate's own page for each: Great
Britain, France, Germany, Austria, Sweden, Belgium, Switzerland, Italy,
Spain and Portugal, Hong Kong, Korea and Singapore.

Eight of its eparchies have no row, and for one reason: the Patriarchate's
page for each of them says the site is under development and gives the
Patriarchate's own Istanbul address in place of theirs. Ireland, Malta,
Lithuania, Australia, New Zealand, Buenos Aires, Mexico and the Archdiocese
of Canada are all in that state. They are deferred until there is something
to read, and this note is here so the next pass knows to look rather than
concluding the list is complete.

The metropolises of Greece and Turkey run to a hundred more and are the pass
after that.

Worldwide parish coverage is tens of thousands of rows and will go stale.
Diocesan coverage will not. The site commits to the second and treats the
first as something added where it can be kept true, beginning with the
United States, where the Assembly of Canonical Orthodox Bishops publishes
one list covering every jurisdiction at once.

## Telling two bodies of the same name apart

There is an Albanian Archdiocese of the Orthodox Church in America, an
Albanian Orthodox Diocese of the Americas under Constantinople, and the
Church of Albania at Tirana. The same will be true of the Bulgarians, the
Romanians, the Serbs and the Ukrainians, and once parishes arrive there will
be a hundred churches of Saint Nicholas.

So a diocese names the Church it belongs to on the row itself, not only by
where the row is nested. Nesting is enough while a reader is reading down
the list and useless the moment a search or a country filter lifts a row out
of it, which is exactly when he most needs to know which of three Albanian
bodies he is looking at. The line is drawn from `parent` and costs nothing
per row.

`tools/check_site.py` counts the names. Two rows sharing one is normal and
is reported; two rows sharing one where neither hangs off a Church is an
error, because nothing on the page would tell them apart.

But the Albanian case was only the shape of the question, and the answer to
the question itself is not a naming device. There are two Romanian bodies in
America, in Chicago under Bucharest and in Jackson, Michigan within the
Orthodox Church in America, and they are not a duplicate or a mistake: they
are what emigration left behind. The page now says so once, above the list,
rather than leaving every reader to work it out from the rows. The same is
true of the Albanians, the Bulgarians and the Ukrainians.

## The body's own name, and the languages this site does not have

Every row can carry `local`, the name the body publishes for itself in its
own language, and it is never translated. Seventeen of the twenty-two
Churches have one. Four do not because their own sites could not be read
from here - Antioch, Georgia, Serbia and Cyprus - and the Orthodox Church in
America does not because its own name is the English one the row already
shows.

The Patriarchate of Jerusalem writes its own title with a Latin v where the
Greek nu belongs. That is a slip of a keyboard rather than a spelling, and
the row carries the letter the title plainly means; nothing else on any row
is altered from what the body prints.

Filling that field exposed something larger, and it is written here because
it is a decision about the site and not about this page. **Seven of the
twenty-two Churches speak a language this site does not publish in**:
Bulgarian, Albanian, Polish, Czech, Slovak, Macedonian, Finnish and
Estonian. The Bulgarian Patriarchate is the one that ought to trouble
anybody - some millions of faithful, a Church of the first rank, and this
site offers Syriac and Bengali before it offers Bulgarian.

That is not a gap this page can close and it is not created by this page.
It is recorded here because the directory is where it becomes visible: a
reader of any of those seven meets his own Church named in someone else's
language.

## Saying what is not here yet

A Church showing one diocese does not have one diocese. The Romanian
Patriarchate had exactly that on this page, because North America had been
sourced and Romania had not, and a count with nothing beside it reads as a
total. Ten of its own eparchies have since been read from its own list of
them, and the page carries a line saying plainly that the Churches are all
here and their dioceses are being added region by region.

That line matters more as the directory grows, not less. Every region added
makes the regions still missing look more like absences of fact.

**Its first wording overclaimed and was replaced.** It read "Every Orthodox
Church is here", which was written when the twenty-two looked like the whole
set and was already untrue: the Chinese Autonomous Orthodox Church is not
among them, and finding one missing is reason to doubt the count rather than
to assert it. A page that says a thing is complete is making a claim about
what it does not contain, which is the hardest claim on a site like this to
have any right to. It now says the list is being built, that a Church is here
once it has been read from an official source, and that a Church may be
missing altogether.

## The order of the work, and why it is not both at once

Sourcing comes first and translating follows it, one whole pass behind.

The directory was built the other way for a while - rows and their names in
twenty-two languages arriving together - and it cost real work twice. Ten
Romanian eparchies arrived a commit after the key file went to the lanes and
no language was ever asked to name them. Thirty-nine dioceses were named in
sixteen languages before ten more rows landed beside them.

So: read the rows, and while reading them take the body's own name in its own
language, which costs nothing extra because it is on the page being read
anyway and it is not a translation. Translate the rest in a pass of its own,
once a Church's list has stopped moving. A row that reads English for a while
is visibly unfinished; a row nobody was asked to name is invisibly unfinished,
and that is the failure worth designing against.

**Monasteries are a filter, not a section.** They are rows like any other
with `kind` set, so country, jurisdiction and kind are three filters over
one list. A separate section would duplicate every filter and split the
search.
