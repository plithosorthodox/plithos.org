# -*- coding: utf-8 -*-
"""Verse ranges written with a hyphen, as the house rule has it.

The lectionary was carried in with en dashes - 2 Cor. 8:7-15 with a rule
rather than a hyphen - and the site normalises them to hyphens before it
looks a reading up, so the reader saw one character and the Bible was asked
for another. This settles the printed form on the hyphen too.

It touches ranges of figures only. The em dash between a feast's name and its
subtitle stays: Greek, Russian, Romanian and Ukrainian all set that dash, and
a hyphen there would be the English sentence in their punctuation. So does
every dash inside the liturgical rubrics, which are reproduced, not edited.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")

# The reader's own normaliser is written with the two dashes in a character
# class. Rewriting that would leave it unable to read what it is repairing.
GUARD = u"[–—]"


def main():
    s = io.open(PAGE, encoding="utf-8").read()
    keep = s.count(GUARD)
    s = s.replace(GUARD, u"\x00GUARD\x00")

    s, n = re.subn(u"(?<=[0-9])–(?=[0-9])", u"-", s)
    # Jan-Mar, Jul-Dec: month spans in the working comments. And the spans
    # of hours the prayer times are given in - 20h-21h, 4h-6h.
    s, m = re.subn(u"(?<=[A-Za-z])–(?=[A-Z0-9])", u"-", s)

    s = s.replace(u"\x00GUARD\x00", GUARD)
    if s.count(GUARD) != keep:
        print("the normaliser's character class did not survive")
        return 1

    io.open(PAGE, "w", encoding="utf-8").write(s)
    left = s.count(u"–")
    print("%d verse ranges and %d month spans set with a hyphen; "
          "%d en dashes left, all inside the normaliser" % (n, m, left))
    return 0


if __name__ == "__main__":
    sys.exit(main())
