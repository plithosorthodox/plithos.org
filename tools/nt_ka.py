# -*- coding: utf-8 -*-
"""The Georgian New Testament, in the recension of St George the Hagiorite.

Georgian was the only language offered on this site without a New Testament,
and docs/BASELINE.md recorded at length where it had been looked for and not
found: not in eBible's manifest of 1,550 texts, not in CrossWire's 462
modules, not in bolls.life, not in helloao's thousand languages, and not on
Georgian Wikisource. All of that was true and none of it was the right place
to look.

The site's Old Georgian Old Testament, which came in with the original import
and named no source, is word for word the text allgeo.org publishes from the
Mtskheta manuscript. allgeo.org also publishes the New Testament, in Old
Georgian, all twenty-seven books, and says on the page which edition it is:

    the second complete edition of the critically established text of the
    recension of St George the Hagiorite

St George the Athonite (1009-1065) made the Georgian Church's received text
of the New Testament, and it is his recension she has read ever since. He is
in this calendar himself, on the 27th of June. The text is a thousand years
old and the register is the register of the Old Testament already published
here.

The pages set a chapter as a line holding nothing but its number, and number
every verse at its head, so both are read off the page rather than counted.
"""

BASE = "https://www.allgeo.org/index.php/ka/"

# book -> the page that holds it. The site sets them in the Orthodox order,
# the Gospels and Acts, then the catholic epistles, then Paul, then the
# Apocalypse; the reader here shows them in its own order, so what matters is
# that each book is fetched from its own page and not that the list is sorted.
PAGES = {
    "Matthew": "880-2019-04-18-01-16-41",
    "Mark": "881-2019-04-18-01-28-10",
    "Luke": "882-2019-04-18-01-35-27",
    "John": "883-2019-04-18-01-40-39",
    "Acts": "884-2019-04-18-01-48-34",
    "James": "893-2019-04-18-20-35-06",
    "1 Peter": "894-2019-04-18-22-59-50",
    "2 Peter": "895-2019-04-18-23-04-46",
    "1 John": "896-2019-04-19-00-24-40",
    "2 John": "897-2019-04-19-00-27-07",
    "3 John": "898-2019-04-19-00-29-12",
    "Jude": "899-2019-04-19-00-30-46",
    "Romans": "900-2019-04-19-00-40-17",
    "1 Corinthians": "901-2019-04-20-23-38-53",
    "2 Corinthians": "902-2019-04-20-23-41-50",
    "Galatians": "903-2019-04-21-00-06-59",
    "Ephesians": "904-2019-04-21-00-28-18",
    "Philippians": "905-2019-04-21-00-31-18",
    "Colossians": "906-2019-04-21-00-34-36",
    "1 Thessalonians": "907-2019-04-21-00-42-45",
    "2 Thessalonians": "908-2019-04-21-00-44-37",
    "1 Timothy": "909-2019-04-21-00-55-27",
    "2 Timothy": "910-2019-04-21-00-58-40",
    "Titus": "911-2019-04-21-01-01-32",
    "Philemon": "912-2019-04-21-01-12-34",
    "Hebrews": "913-2019-04-21-01-16-47",
    "Revelation": "914-2019-04-21-01-21-44",
}
