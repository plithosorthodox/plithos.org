# -*- coding: utf-8 -*-
"""The dioceses of each Church, one Church to a file.

The directory began with the Churches themselves and grew its dioceses a
region at a time, which was right while the regions were few and is wrong
now: two dioceses stood under the Church of Russia and none under either
Ukrainian Church, on a page that gives no sign it is showing part of a list.
A Church with three hundred eparchies and two rows does not read as
incomplete. It reads as wrong.

So the dioceses come out of `tools/directory.py` and into one file per
Church, which is what lets the work divide. Each file exports ROWS, a list
in the shape `tools/directory.py` documents, and nothing else:

    tools/directory_rows/russia.py      ROWS = [dict(id=..., parent="russia", ...)]

The rules a row obeys are in docs/DIRECTORY.md and are not restated here,
except the two that decide whether a row may exist at all:

  - Every row is read from an official site - the body's own, or the Church
    it belongs to - and carries the URL it was read from and the day it was
    read. Nothing is written from memory.
  - Every row answers with a link. Where the body's own site does not
    answer, the row gives the Church above it, which is the level a reader
    can still get somewhere from.

A file may be partial. A Church whose list is half-read is better than a
Church with two dioceses and no sign that more exist, and the page says
above the list that the dioceses are still being added.
"""
import importlib
import os

CHURCHES = [
    "constantinople", "alexandria", "antioch", "jerusalem", "russia",
    "georgia", "serbia", "romania", "bulgaria", "cyprus", "greece",
    "albania", "poland", "czech-slovakia", "oca", "macedonia",
    "ukraine-uoc", "ukraine-ocu", "sinai", "finland", "japan",
    "estonia-eaok",
]


def _mod(name):
    for base in ("directory_rows.", "tools.directory_rows."):
        try:
            return importlib.import_module(base + name.replace("-", "_"))
        except ImportError:
            continue
    return None


def rows(church):
    m = _mod(church)
    return list(getattr(m, "ROWS", [])) if m else []


def all_rows():
    out = []
    for c in CHURCHES:
        out.extend(rows(c))
    return out


def written():
    here = os.path.dirname(os.path.abspath(__file__))
    return [c for c in CHURCHES
            if os.path.exists(os.path.join(here, c.replace("-", "_") + ".py"))]
