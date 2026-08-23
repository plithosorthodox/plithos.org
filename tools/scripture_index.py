#!/usr/bin/env python3
"""The scripture index, under the name the reader asks for.

    python3 tools/scripture_index.py

scripture/index.json says which books each language carries and what that
language calls them. It is served under /scripture/*, which is held for a
week, and its name carries no version - so a correction to it took a week to
reach anybody who had already been to the site, and there was no way to say
otherwise.

It is therefore published twice: index.json stays where it is, because pages
held from before this ask for that exact name and would get the whole calendar
and a 200 if it were gone, and the same content is published as index.v2.json,
which the reader asks for now. A new name has no cached copy anywhere, so a
correction lands at once. Bump the version when that matters again.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "scripture" / "index.json"
LIVE = ROOT / "scripture" / "index.v2.json"


def sync():
    """Publish index.json under the versioned name as well."""
    raw = BASE.read_text(encoding="utf-8")
    if LIVE.exists() and LIVE.read_text(encoding="utf-8") == raw:
        return False
    json.loads(raw)                       # never publish what will not parse
    LIVE.write_text(raw, encoding="utf-8")
    return True


if __name__ == "__main__":
    print("wrote %s" % LIVE.name if sync() else "already in step")
    sys.exit(0)
