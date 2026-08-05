#!/usr/bin/env python3
"""
Merge translated calendar entries into index.html.

Every commemoration has two lives on this site: the long one on the Saints
index, and the sixty-word one the calendar shows on its day panel. A saint is
not finished until both are done, and doing them apart means reading the same
life twice and coming back to the same saint months later.

The long lives are published from tools/saint_lives/. This does the calendar
half, which cannot be published the same way because SAINT_INFO_I18N lives
inside index.html as a single one-and-a-half-megabyte line. So it is parsed,
merged and written back, rather than edited by hand or by anchor - the sort
of change CLAUDE.md asks be made by a script.

Entries live in tools/saint_info/<lang>.py as

    TEXT = {English name: {"type": ..., "life": ..., "patron": ...}}

keyed by the name SAINT_INFO uses. A key that is not in SAINT_INFO fails the
run: a calendar entry attached to a saint who is not there would simply never
appear, and would look like a translation that had been done.

    python3 tools/saint_info_i18n.py --check
    python3 tools/saint_info_i18n.py --write
"""
import argparse
import importlib
import json
import pkgutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
TEXT_DIR = Path(__file__).resolve().parent / "saint_info"

FIELDS = ("type", "life", "patron", "src")


def literal(src, name):
    i = src.index("const %s=" % name)
    eq = src.index("=", i)
    j = src.index("\n", i)
    return i, j, json.loads(src[eq + 1:j].rstrip().rstrip(";"))


def languages():
    sys.path.insert(0, str(TEXT_DIR.parent))
    out = {}
    for m in pkgutil.iter_modules([str(TEXT_DIR)]):
        mod = importlib.import_module("saint_info." + m.name)
        out[m.name] = dict(getattr(mod, "TEXT", {}))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    src = PAGE.read_text(encoding="utf-8")
    _, _, info = literal(src, "SAINT_INFO")
    i, j, table = literal(src, "SAINT_INFO_I18N")
    print("%d commemorations on the calendar" % len(info))

    bad, added = [], 0
    for lang, text in sorted(languages().items()):
        for k, v in sorted(text.items()):
            if k not in info:
                bad.append("%s: %r is not on the calendar" % (lang, k))
                continue
            stray = sorted(set(v) - set(FIELDS))
            if stray:
                bad.append("%s %r: unknown field %s" % (lang, k, stray[0]))
            if not (v.get("life") or "").strip():
                bad.append("%s %r: no life" % (lang, k))
        have = table.setdefault(lang, {})
        fresh = [k for k in text if k not in have]
        added += len(fresh)
        print("   %-4s %4d of %d entries  (%d new here)"
              % (lang, len(set(have) | set(text)), len(info), len(fresh)))

    if bad:
        print("\n%d problem(s):" % len(bad))
        for b in bad:
            print("   %s" % b)
        return 1

    if args.write:
        for lang, text in languages().items():
            table.setdefault(lang, {}).update(text)
        line = ("const SAINT_INFO_I18N=" +
                json.dumps(table, ensure_ascii=False, separators=(",", ":")) + ";")
        PAGE.write_text(src[:i] + line + src[j:], encoding="utf-8")
        print("\nmerged %d new entries into index.html" % added)
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
