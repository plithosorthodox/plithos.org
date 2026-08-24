# The jurisdictions, and how far apart they actually are

The calendar on this site is one calendar. Its base is the synaxarion of the
Orthodox Church in America - CLAUDE.md says so and every entry's `src` field
names it - and choosing a jurisdiction changes four things:

  - whether the reckoning is old or new (`cal`)
  - whether the rite is Western, which branches the whole day (`rite`)
  - the name and the cross shown at the head of the month
  - a short list of that Church's own commemorations, ADDED to the base

That is all. Measured on 24 August 2026:

| jurisdiction | own commemorations |
|---|---|
| Serbian | 6 |
| Romanian, Ukrainian, Russian, Georgian | 4 each |
| Greek, Bulgarian | 3 each |
| Antiochian | 1 |
| OCA | 0, being the base |
| **all ten together** | **29** |

Ten Churches share one calendar and twenty-nine entries between them, which is
why they read as the same calendar with a different label.

## What is actually different, in the order a reader notices

**The saints.** Not four apiece. The Church of Romania has canonised dozens
since 1955; the Russian calendar carries the New Martyrs and Confessors; the
Serbian her own line of archbishops and kings; Georgia hers from the fourth
century on. And the difference runs both ways, which is the part that was
missing entirely: a Greek reader is shown St Herman of Alaska, St Peter the
Aleut and St Alexis Toth, which his Church does not keep, and an Antiochian
reader is not shown St Raphael of Brooklyn at all, because he is nowhere on
this site.

**The fasting rule.** `fastingFor(d, mode)` takes the date and the calendar
style and nothing else, so it cannot express a jurisdictional difference even
in principle. Real ones exist, chiefly over which days of the Nativity Fast
admit fish, and over wine and oil.

**The readings.** `afterPentReading` implements a Lukan jump anchored on the
Sunday after the Elevation of the Cross. That is the Constantinopolitan
reckoning. The Slavic practice differs, and the divergence runs for weeks each
autumn.

## What has been built

`OMIT_FIXED` in index.html, written by `tools/jurisdictions.py`: a jurisdiction
may now decline a base commemoration that is not hers. `commemsFor` honours it,
and it does not apply when the reader has asked to see every Church's saints at
once.

The table is **empty on purpose**. The capability lands first; the lists are
filled from each Church's published calendar, one jurisdiction at a time, with
the source recorded beside every line.

## The rule for filling it

Nothing here is inferred. CLAUDE.md forbids inventing hagiography or a feast
date, and an omission asserted without a source is worse than the fault it
mends: it tells a reader his Church does not keep a feast that she does, and
he has no way to know he has been misled.

So every line - added or declined - names the calendar it is read from: the
Church's own published calendar or synaxarion, the way `tools/add_saints.py`
already requires for a commemoration.

The fasting and the lectionary divergences are not to be written from
reasoning either. They want the typikon each Church actually follows, named,
before a reader is told what to keep.
