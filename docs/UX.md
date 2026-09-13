# The interface, looked at closely - 13 September 2026

Measured, not guessed. Every number below was taken in a browser at 390
by 844, the size of an ordinary phone, in the dark theme, with the
network throttled to what the site actually ships.

The site reads well on a desk. Almost everything here is about a phone.

## The first screen is nearly all chrome

| page | masthead | where the page's own content begins |
|---|---|---|
| calendar | 347 px | 706 px - 83% of the screen is gone |
| Library | 297 px | 296 px |
| prayers | 176 px | 267 px |
| Saints | 184 px | 184 px |

The calendar is the worst and it is the front door. A reader opening
plithos.org on a phone sees the mark, seven navigation words over three
rows, a search button, a theme button, a jurisdiction picker, a
new/old switch, a three-way saints switch, a calendar/list switch and a
language picker - and then has to scroll to find out what day it is.

The nav is seven links on three rows because it is seven links. The
controls under it are six separate switches, all of them shown at once,
and most readers will set them once and never touch them again.

Worth trying: the day first and the machinery after it; the masthead
collapsed to the mark, the page name and one button below a certain
width; the six switches folded into one "Settings" sheet with the two
that change daily - jurisdiction and language - left out where they are.

## The month grid is unreadable on a phone

Seven columns in 390 pixels give each day about 55 pixels. The
commemorations do not fit, so they wrap to one or two characters a line:
"Forefe / ast of / the / Nativi / ty of / the / Mothe / r o...". One
week of the grid is about 570 pixels tall - taller than the screen. The
reader cannot read a single day without opening it.

This is the thing to fix first. Three ways, and they are not exclusive:

- **A week view.** Seven rows instead of seven columns, each a full
  line wide. This is what a phone wants and it is a new view, not a
  change to the existing one.
- **A compact month.** The grid keeps the numbers and the fasting marks
  and drops the names; a day opens on a tap. The month is then a month -
  something to see at a glance - which is what a grid is for.
- **Default to the list below a certain width.** The list view already
  reads well. The switch stays, so a reader who wants the grid has it.

The honest answer is probably all three: compact month as the default
grid on a phone, a week view beside it, and the list as it is.

## The day's commemorations should be above the calendar

They are the reason the page exists and they are below the fold on a
phone. On a desk the calendar is worth seeing first because the whole
month fits; on a phone it is not.

## The prayers are sorted by a layer that is not used

`data/prayers.v2.json` declares nine sections - Morning and Evening, The
Hours, The Jesus Prayer and Short Prayers, Holy Communion, The Theotokos
the Angels and the Saints, For Others, For Oneself, Life and Its
Occasions, Psalms - each with a title and a sentence of description,
each translated into twenty-two languages. Every one of the hundred
prayers carries the section it belongs to.

The page does not use any of it. It prints one flat list under
twenty-six headings taken from the finer `cat` field, ten of which hold
a single prayer: For Kindred, In Seeking a Spouse, Finding a Spiritual
Father, For the Victims of Abortion. The result is a 9,663-pixel scroll
with no way to jump, no way to collapse, and a heading every four
prayers.

The fix is mostly deletion. Render the nine sections; keep `cat` as the
sub-heading inside a section; put the nine at the top as a chooser, so a
reader who wants the evening prayers can reach them in one tap. The
words are already written and already translated.

## The Library asks five questions before it offers anything

The first screen of the Library on a phone, after 590 pixels of chrome,
is a section dropdown, a catalogue search box, and five collapsed
filters - Subject 32, Author 50, Century 8, Purpose 18, Translator 50 -
and only after all of that, the shelves themselves. The reader is asked
to narrow a thing he has not yet been shown.

Turn it around: the shelves first, the filters behind one control. The
sections (The whole shelf, The Divine Liturgy, Old Testament, New
Testament, The Fathers, Councils and Creeds, Lives and Martyrdoms) are
the Library's real structure and they are good; they should be the first
thing under the masthead, and on a phone they want to be cards rather
than a dropdown.

The counts line - "113 titles - 149 editions - 55 units" - is the kind
of thing a cataloguer wants and a reader does not. It would sit better
at the foot.

## The Saints page renders all 1,456 at once

The document is 170,936 pixels tall. Every commemoration is in the DOM
from the first paint, which is why the page is slow to settle on a phone
and why scrolling it is unrewarding: there is no sense of where one is,
and "Showing 1,456 of 1,456" is the only orientation offered.

Worth trying: render a screenful and add as the reader scrolls, and an
index down the side - by month, or by letter - so the list has a shape.

## Tap targets

Counted at phone width: 33 controls under 40 pixels on the calendar, 55
on the Library, 851 on the Glossary, which is every one of its tag
chips. Forty-four pixels is the usual floor. Most of these are one or
two pixels of padding away from it.

## Contrast

Fixed on 13 September and recorded here so the numbers are kept. The
Saints page's order chips were white on pale pink in the dark theme,
1.24:1 where AA asks 4.5; the attribute chips 1.19:1. `--muted`, which
colours every secondary line on the site - a place, a jurisdiction tag,
a source - was 3.36:1 on parchment at ten and eleven pixels, and had
been since the palette was written.

Everything measured now clears AA in both themes.
