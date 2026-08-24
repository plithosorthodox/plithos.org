# The jurisdictions, and how far apart they actually are

The calendar on this site is one calendar. Its base is the synaxarion of the
Orthodox Church in America - CLAUDE.md says so and every entry's `src` field
names it - and choosing a jurisdiction changed four things, and only four:

  - whether the reckoning is old or new (`cal`)
  - whether the rite is Western, which branches the whole day (`rite`)
  - the name and the cross shown at the head of the month
  - a short list of that Church's own commemorations, ADDED to the base

Measured on 24 August 2026 it was twenty-nine commemorations across ten
Churches, which is why they read as the same calendar with a different label.

## Where it stands now

**The fasting rule** now takes the jurisdiction. `fastingFor` reads the
Church as well as the date, and the Nativity and the Apostles' fasts - the
two seasons on which the Churches openly print different rules - come out
differently for a Greek reader and a Slavic one:

  - Constantinople and the Church of Greece give fish on every day but
    Wednesday and Friday until 17 December, and keep the last week strictly.
    Source: the Greek Orthodox Archdiocese of America's published guidelines.
  - The Typikon, which the Slavic Churches and Antioch publish, keeps fish to
    Saturday and Sunday, gives wine and oil on Tuesday and Thursday, leaves
    Monday, Wednesday and Friday without oil, and withdraws fish altogether
    from 20 December. Source: the Orthodox Church in America, "Fasting and
    Fast-Free Seasons of the Church", and the Antiochian Archdiocese's rules.

The same pass corrected four things the rule had wrong for everybody: Great
Saturday had wine and oil where the canons give neither (Trullo 89); Palm
Sunday had wine where the Typikon gives fish; the Annunciation in Lent and
the Transfiguration in the Dormition Fast had no exception at all; and the
three fixed strict days - the Exaltation of the Cross, the Beheading of the
Forerunner and the eve of Theophany - were simply absent, so they showed as
no fast unless they happened to fall on a Wednesday.

**The saints.** The local lists have gone from twenty-nine to a hundred and
nineteen, and eight of the nine Churches have a list worth the name.

| jurisdiction | own commemorations |
|---|---|
| Romanian | 27 |
| Georgian | 25 |
| Bulgarian | 22 |
| Serbian | 19 |
| Russian | 10 |
| Greek | 10 |
| Ukrainian | 8 |
| Antiochian | 6 |
| OCA | 2, being the base |

Each list is read off a published one and the source is recorded in
`tools/local_saints.py` beside the entries it produced: Romania from the
Romanian Patriarchate's own news agency, Basilica; Serbia from the calendar
of the Serbian Orthodox Church; Bulgaria from the list of Bulgarian saints
with the day of each; Georgia from the Georgian synaxarion published in
English by that Church in Canada; Greece from the acts that proclaimed her
modern saints; Antioch from the commemorations her Patriarchate keeps as her
own, together with the Synaxis of All Saints of Antioch, which her Holy Synod
set on the second Sunday after Pentecost.

**Old and new reckonings are not mixed.** Every entry is a menaion day, which
is what `fixedCivil` expects. Romania and Bulgaria keep the new calendar and
their published days are already menaion days; Serbia and Georgia keep the
old, so the Serbian entries take the Julian date of the pair her calendar
prints and the Georgian ones take the printed civil day less thirteen. The
base confirms the conversion at four points: Shio of Mgvime, Queen Shushanik,
All Saints of Georgia, and St Sava on 14 January.

**Nothing is written twice.** `tools/check_site.py` now compares every local
entry against the base entries for its day on the shape of the name rather
than its letters, because the six that slipped through by eye all differed by
transliteration - Gerasimus of Cephalonia against Gerasimos of Kephalonia,
John-Vladimir against Jovan Vladimir. It reports an error where every
distinctive word of a local entry is inside a base one, which is the same
saint written twice, and a review where they merely overlap, which two
different saints on one day may perfectly well do. Seven entries came out
again on that check, including St Dionysios of Zakynthos, whom the base has
carried all along as Dionysius of Aegina.

**Choosing whose saints to see.** The scope control had two settings, this
Church or all of them, and "all of them" said nothing about who kept which.
There are now three, the third being a row of the ten Churches to tick, and
every local commemoration carries the Church that keeps it on its own line.

## What is still open

**The lists are a beginning, not a census.** Romania's own agency prints
seventy-six canonised saints and twenty-two of them are here; Bulgaria's list
runs past a hundred. What is here is what could be read off a published list
and checked, and each Church's list should keep growing from her own calendar.

**The names are English in every language.** `NAMES_I18N` carries thirty-seven
names and none of the local commemorations is among them, so a Serbian reader
is shown "St Stefan Dečanski, King of Serbia" in English. That is not new -
the twenty-nine entries that were here before had the same fault - but there
are now a hundred and nineteen of them, and the register rules in CLAUDE.md
apply: the honorific is the rank, not the word for holy.

**Declining is built but empty.** `OMIT_FIXED` lets a jurisdiction decline a
base commemoration that is not hers, and the table has no lines in it. The
obvious candidates are the North American saints the base carries - Herman,
Innocent, Juvenaly, Peter the Aleut, Alexis Toth, Jacob Netsvetov - which a
Greek or a Romanian calendar does not print. But an omission asserted without
a source is worse than the fault it mends: it tells a reader his Church does
not keep a feast that she does, and he has no way to know he has been misled.
Each line wants the Church's own calendar for that day, read and named.

**Some base dates are civil where the site reads them as menaion.** The base
carries St Tikhon's repose at 04-07 and St Matrona at 05-02, which are the
Gregorian equivalents of 25 March and 19 April, not the menaion days. For a
new-calendar reader this is invisible; for an old-calendar one the site
shifts them another thirteen days. The entries want auditing against the
menaion, which is a separate job from this one and is not to be guessed at
entry by entry.

**The readings.** `afterPentReading` implements a Lukan jump anchored on the
Sunday after the Elevation of the Cross. That is the Constantinopolitan
reckoning, and it is given to every Church. The Slavic practice differs and
the divergence runs for weeks each autumn. Like the fast, this wants the
typikon each Church actually follows, named, before a reader is told what to
read.

## The rule for filling any of it

Nothing here is inferred. CLAUDE.md forbids inventing hagiography or a feast
date, so every line - added or declined - names the calendar it is read from:
the Church's own published calendar or synaxarion, the way
`tools/add_saints.py` already requires for a commemoration.

The tools that hold these lists are `tools/local_saints.py` for the Churches'
own saints, `tools/jurisdictions.py` for what a Church declines,
`tools/fasting_rule.py` for the rule the calendar prints and
`tools/fasting_notes.py` for the line under it.
