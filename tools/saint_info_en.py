# -*- coding: utf-8 -*-
"""The English day-panel entries, wherever they are kept.

SAINT_INFO sat in index.html as 811 KB of English - a quarter of the page -
long after the other twenty-one languages had moved to
data/saint-info.v1.<lang>.json. It is a file now like the rest, and three
tools that read it from the page read it from here instead, so none of them
has to know which side of the move it is on.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
FILE = ROOT / "data" / "saint-info.v1.en.json"


def from_page():
    src = PAGE.read_text(encoding="utf-8")
    i = src.index("const SAINT_INFO=")
    eq = src.index("=", i)
    j = src.index("\n", i)
    return json.loads(src[eq + 1:j].rstrip().rstrip(";"))


def load():
    """The entries, from the file where there is one and the page otherwise."""
    if FILE.exists():
        d = json.loads(FILE.read_text(encoding="utf-8"))
        if d:
            return d
    return from_page()
