# The interface, looked at closely

## Re-audit - 13 November 2026

Measured against the live production site in the dark theme at 390 by 844,
with a 360 by 800 calendar check, and at 1440 by 900 on desktop. Pointer
activations are counted below. Typing and scrolling are stated separately.

October field traffic makes the priority clear: 330 of 490 estimated
pageviews, 67 percent, were mobile. Calendar, Prayers and Library together
accounted for 380 pageviews, 78 percent. Field rendering performance was
strong, with P75 LCP at 592 ms, INP at 72 ms and CLS at zero. The primary
problems are information architecture, first-screen visibility, control size
and semantics, not transfer or rendering speed.

### Prayer discovery redesign - 13 November 2026

Measured from the frozen pre-change backup and the finished local page in the
dark and light themes at 390 by 844 and 1440 by 900. External requests were
aborted during measurement; all same-origin requests completed without error.

| mobile measure | before | after |
|---|---:|---:|
| Search begins | 447 px | 310 px |
| Search field height | 19 px | 44 px |
| Guidance block | 538 to 856 px, open | after results, collapsed |
| First global-search result | below the 878 px list start | 480 px |
| First selected-topic result | no topic directory | 553 px |
| Visible topic links | 0 | 30 in 5 groups |
| Exposed controls | 115 | 146 |
| Controls under 44 px | 14 | 12, all in shared masthead chrome |

Every topic is visible on the initial page. Topic links form two columns on a
390 px phone, while the five groups form three columns on desktop. Each of the
100 prayers has one to four topics, so prayers that concern more than one need
appear wherever a reader would reasonably look. The older sections remain as
a secondary prayer-book-order selector. That selector uses the nine broad
sections as group headings and exposes all 28 real subtypes beneath them. A
reader can therefore choose a whole section or go directly to a narrower
entry such as Immediately before receiving or For Travelers.

Search now clears the topic and section filters, searches all prayers, and
ranks exact and prefix title matches ahead of topic, category, description and
body matches. Results begin within the first phone screen. Choosing a topic
takes one activation and places its first prayer in the first phone screen.
Opening the prayer takes the second activation. From the home page this is
three activations including Prayers in the masthead; a known prayer found by
search remains two activations, with typing not counted.

Prayer and topic links now have stable addresses. Old numeric prayer and
section links still resolve. Browser Back restores the prior topic or query,
scroll position and keyboard focus. Browser checks covered English and Arabic,
old and new routes, exact-title ranking, cross-section search, both themes,
mobile and desktop layouts, focus restoration and horizontal overflow.

### Task depth from the home page

| task | mobile taps | desktop clicks | friction not shown by the count |
|---|---:|---:|---|
| Open today's short saint life | 1 | 1 | First mobile saint is around y=1,143. Full life needs a second tap. |
| Find and open a specific prayer | 3 | 3 | First mobile prayer begins around y=1,085. Global Search can reduce a known prayer to 2. |
| Open a specific Library work | 2 to 3 | 3 | There is no usable in-work section control. |
| Open an arbitrary Scripture passage | 4, or 5 with edition change | 4 | Book and chapter are not encoded in the URL. |
| Open today's Scripture reading | 1 | 1 | Mobile trigger is only 136 by 22 px. |
| Search for and open a saint | 3 | 3 | Global Search can reduce a known saint to 2. |
| Filter Churches to a country | 2 | 2 | United States is around y=1,553 and results start around y=1,658 on mobile. |
| Find a Glossary term | 2 | 2 | Search works, but the field is unnamed to assistive technology. |
| Read today's fasting rule | 0 | 0 | It starts around y=990 on mobile. |
| Reach general fasting guidance | 1 plus scrolling | 1 plus scrolling | The section begins around y=8,392 and The Rule has no contents list. |
| Change language | 2 | 2 | This works consistently and changes the document language correctly. |

The site keeps every top-level page one activation from every other page. That
is valuable. The redesign should not trade it away casually. The largest wins
come from moving content upward, removing duplicate controls and adding deep
links, not merely removing clicks.

### The calendar front door still hides the day

At 390 by 844 the header and preferences occupy the first 450 px. Today's
panel starts at y=833, leaving 11 px of it in the first screen. The fasting
rule starts at y=990, the first saint at y=1,143, the reading at y=1,319 and the
month grid near y=1,500. At 360 by 800, today's panel moves to y=869 and the
grid to about y=1,600. Seventy-seven of 78 exposed controls fail the 44 px
target test, and a calendar day is only 23 by 56 px.

Put today's date, fast, commemorations and readings directly after a compact
masthead. Fold jurisdiction, calendar style, saints scope, view and language
into one preferences control. A successful mobile revision should show the
date, fast and first commemoration in the first 600 px at 390 by 844, while
keeping the primary day tasks at zero or one activation.

### Library discovery improves at the shelf and then collapses in the reader

The Library home repeats the same seven destinations in a select, a rail and
the collection cards. Its header ends at y=327, the controls run to about
y=832, the stage title starts at y=886 and the first collection card starts at
y=1,064.

Selecting The Fathers renders all 98 works in a 5,171 px rail. The selected
work title then begins around y=5,585. The tested article was 314,922 px tall;
Book II began around y=56,065. Chapter markers are plain `div` elements, not
headings, links or keyboard targets. Desktop showed the same issue in a
177,289 px reading surface with 566 paragraphs and no useful contents list.

On mobile, use one compact collection picker followed immediately by the
selected work. Replace the 98-item rail with searchable work selection. Add a
semantic table of contents, render a bounded section at a time, show the
current section and encode work, book, chapter and section in the URL. The
target is any named section in no more than three activations from home.

**Mobile Library controls revised on 13 November.** Measured again at 390 by
844 in the dark theme, with the production network blocked during the local
render:

| mobile measure | before | after |
|---|---:|---:|
| Persistent masthead | 297 px | 176 px |
| Home rail before the Library introduction | 506 px | 85 px |
| First collection card begins | y=1,010 | y=468 |
| Liturgy text-language heading begins | y=827, inside the closed Filters drawer | y=332, always visible |
| Liturgy Filters control begins | y=783 | y=423 |

At 1440 by 900, the persistent masthead fell from 162 px to 91 px. The page
language control and catalog tally no longer enlarge the persistent masthead.
Home presents the collection cards once, while the section selector appears
after a collection is opened. Text languages stand directly below that
selector and outside Filters. Filters now precede the potentially long work
list.

### Large collections are rendered without restraint

| page | live DOM elements | document height | consequence |
|---|---:|---:|---|
| Saints | 12,026 | 177,665 px on mobile | All 1,457 cards exist at first paint. |
| Churches | 17,913 | 10,494 px on desktop | 905 entries and a large country-chip field are rendered together. |
| Glossary | 2,905 | 25,616 px on desktop | Tags and cross-references dominate the control and tab order. |

Saints needs incremental rendering, a month or alphabet index, real links or
buttons for cards, shareable saint URLs and a correctly labelled detail
dialog. Churches needs search and one searchable country or region selector,
with filtered results immediately below it. Glossary should keep search
prominent and move secondary tags into a filter panel or combobox.

### Tap targets and accessibility

Mobile counts exclude descendants of closed `details` elements.

| page | exposed controls | under 44 px |
|---|---:|---:|
| Calendar | 78 | 77 |
| Prayers | 116 | 14 |
| Library home | 28 | 12 |
| Saints | 14 | 13 |
| Churches | 173 | 172 |
| Glossary | 676 | 675 |
| The Rule | 26 | 23 |

The Saints count is deceptively low because the 1,457 clickable cards are
plain `div` elements and therefore are not exposed as controls. The detail
sheet is not a dialog, does not move or trap focus and has a 32 px close
button. Calendar saint expanders do not expose `aria-expanded` or
`aria-controls`. The daily reading dialog lacks `aria-modal`, leaves focus on
its trigger and has a 25 by 28 px close target. Active country and Glossary tag
filters communicate state by colour alone. Several pages expose both a custom
language button and a clipped but tabbable native select.

Global Search is the strongest shortcut, but its active result state is not
fully exposed and Escape restores focus to the body rather than its trigger.
The home page also needs a `main` landmark and a skip link.

### Recommended implementation order

1. Put today's content first on the calendar and compact its preferences.
2. Rebuild the Library mobile flow, add semantic section navigation and make
   work, book, chapter and section shareable.
3. Move Prayer search results directly below search, search all prayers by
   default, prioritize title matches and collapse the guidance essay. Give
   Thanksgiving and Akathists visible topic entries.
4. Make saint cards and sheets semantic and keyboard safe, then incrementally
   render Saints with a month or alphabet index.
5. Replace the Churches country cloud and Glossary tag cloud with labelled,
   stateful search and filter controls. Render long results progressively.
6. Raise repeated navigation, chip, calendar and dialog controls to at least
   44 px. Add shared landmarks, focus restoration and state attributes.
7. Rename The Rule to Prayer Rule, then expose fasting guidance directly or
   add a top-level contents list with a Fasting and confession link.

The target architecture keeps Calendar, Prayers, Library and Search directly
available on mobile because they carry nearly four-fifths of observed traffic.
Less-used destinations may sit under one clearly labelled More control if that
is necessary to recover the first screen, but no top-level page should take
more than two activations to reach.

## Historical baseline - 13 September 2026

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
**Done on 13 September.** Compact month below 760 pixels, a week view
beside it, the day panel above the calendar. What follows is what was
found.

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

## The prayers had their sections and could not be seen to

**Corrected on 13 September.** This section first said the nine sections
were declared and unused. That was wrong and the mistake is worth
keeping: the page does use them. `renderRail()` builds all ten buttons -
All, and the nine - with their counts and their translated titles, and
choosing one narrows the list and prints that section's description.

What was true is what it looked like. On a phone the rail becomes a
39-pixel horizontal strip behind a fade, with its heading hidden, about
two and a half sections wide, sitting between the language picker and a
large essay card. Nothing says it is a list, nothing says it scrolls,
and a reader would take it for decoration - which is why the sections
looked absent when they were not.

Below 860 pixels the ten sections are now the control the platform gives
for choosing one of a list, with the counts beside them. And showing
everything used to mean twenty-six headings in a row, ten of which hold
a single prayer; the nine sections are the coarser spine the data
already carried, so they head the list and the finer headings keep their
place inside it. Choosing Holy Communion takes the page from 10,614
pixels to 2,647.

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
