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

**The saints.** The local lists have gone from twenty-nine to sixty-six.

| jurisdiction | own commemorations |
|---|---|
| Romanian | 26 |
| Serbian | 21 |
| Ukrainian, Russian, Georgian | 4 each |
| Greek, Bulgarian | 3 each |
| Antiochian | 1 |
| OCA | 0, being the base |

Romania's twenty-two additions are read off the Romanian Patriarchate's own
news agency, Basilica, which prints the canonised saints of that Church with
the day of each; Serbia's fifteen off the calendar of the Serbian Orthodox
Church, in the Julian reckoning her own entries here already used. Every
candidate was checked against the base synaxarion first, and the ones already
there were dropped rather than repeated.

**Choosing whose saints to see.** The scope control had two settings, this
Church or all of them, and "all of them" said nothing about who kept which.
There are now three, the third being a row of the ten Churches to tick, and
every local commemoration carries the Church that keeps it on its own line.

## What is still open

**Six Churches still have almost nothing of their own.** Greece, Bulgaria,
Georgia, Ukraine, Russia and Antioch are on three or four entries apiece and
want the same treatment Romania and Serbia have had: a published list from
the Church herself, checked against the base, with the source recorded.

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
