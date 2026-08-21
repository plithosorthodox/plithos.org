#!/usr/bin/env python3
"""
Publish the vocabulary that stands beside a life, in the languages it has.

The Saints index carries more than the life. Down the side of every one of
them run the order, the century, the era, the place, the relics, the
patronage, the kindred commemorations, and the note on how the saint is
written in an icon. Ten thousand distinct phrases, and until now they were
English on every page, so a reader who had set the site to Russian met a
Russian name over a Russian life with "Hierarch", "Medieval Rus'" and
"Galich region, Russia" ranged underneath it.

They are short and they repeat, which is why they are gathered here as one
flat table of English phrase to its rendering, rather than saint by saint:
"Age of the Martyrs" is written once and serves the three hundred and more
commemorations that carry it.

Terms live in tools/saint_terms/<lang>.py as TEXT = {English: rendering}.
Every key is checked against the phrases the index actually uses, so a term
that no longer appears there, or was never spelled the way the index spells
it, fails here instead of silently never being shown.

    python3 tools/build_saint_terms.py --check
    python3 tools/build_saint_terms.py --write
"""
import argparse
import importlib
import json
import pkgutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "saints.html"
OUT = ROOT / "data"
TEXT_DIR = Path(__file__).resolve().parent / "saint_terms"

# The fields whose values are shown to a reader as they stand.
PLAIN = ("type", "place", "era", "rank", "state", "origin", "region",
         "canonizedBy", "relics", "feastRank", "icon", "baptismalName")
LISTS = ("patronPlaces", "patronWork", "patronCauses", "titles", "related",
         "movableFeasts")

# Labels the page supplies itself, which are shown in the same slots.
JURNAME = ("Greek", "Antiochian", "Romanian", "Ukrainian", "Russian",
           "Serbian", "OCA")
ATTRLABEL = ("Monastery founder", "Wonderworker", "Ruler or royal",
             "Confessor", "Desert ascetic", "Enlightener", "Fool-for-Christ",
             "New martyr", "Healing intercessor", "Stylite", "Hymnographer",
             "Passion-bearer", "Church Father", "Iconographer", "Apostle",
             "Prophet", "Unmercenary", "Myrrh-bearer", "Myrrh-streaming",
             "Warrior saint", "Incorrupt relics")


def literal(src, name):
    """The array literal assigned to name, to its matching bracket.

    Counted rather than read to the end of the line, because more than one
    of these lines carries a function after the data it declares.
    """
    start = src.index("[", src.index("const %s=" % name))
    depth, i, instr, esc = 0, start, False, False
    while i < len(src):
        c = src[i]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return json.loads(src[start:i + 1])
        i += 1
    raise SystemExit("%s never closed" % name)


def english():
    """Every phrase the index shows beside a life."""
    src = PAGE.read_text(encoding="utf-8")
    saints = literal(src, "SAINTS")
    rules = literal(src, "CRULES")
    seen = set()
    for s in saints:
        for k in PLAIN:
            v = s.get(k)
            if isinstance(v, str) and v.strip():
                seen.add(v.strip())
        for k in LISTS:
            for item in s.get(k) or []:
                if item and item.strip():
                    seen.add(item.strip())
    seen.update(country for _, country in rules)
    seen.update(JURNAME)
    seen.update(ATTRLABEL)
    return seen


def languages(en):
    """Each language's table, with whatever it assembles from its own parts.

    A place is a compound - a town, then the land it stood in - and the lands
    repeat: Russia closes a hundred and sixty-seven of them. A language may
    therefore render the parts once and declare an expand() that assembles
    the wholes, which keeps one town from being spelled two ways on two
    cards. Anything written out in TEXT stands over what expand() builds.
    """
    sys.path.insert(0, str(TEXT_DIR.parent))
    out = {}
    for m in pkgutil.iter_modules([str(TEXT_DIR)]):
        mod = importlib.import_module("saint_terms." + m.name)
        built = {}
        if hasattr(mod, "expand"):
            built.update(mod.expand(en))
        built.update(getattr(mod, "TEXT", {}))
        out[m.name] = built
    return out



def sync_langs(page, var, pattern):
    """Tell the page which languages actually have a file.

    Pages answers a path that does not exist with the whole of the calendar
    and a 200, so a page that asks for every language downloads 6.8 MB for
    each one that has not been written. The content-type check keeps the page
    correct; this keeps it from asking at all. It is written here, beside the
    files, because a list kept by hand goes stale the day a language lands."""
    langs = sorted(p.name.split(".")[2] for p in (ROOT / "data").glob(pattern))
    want = "var %s={%s};" % (var, ",".join("%s:1" % l for l in langs))
    src = page.read_text(encoding="utf-8")
    i = src.index("var %s={" % var)
    j = src.index("};", i) + 2
    if src[i:j] != want:
        page.write_text(src[:i] + want + src[j:], encoding="utf-8")
        print("  %s -> %s" % (var, " ".join(langs)))
    return langs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    en = english()
    langs = languages(en)
    print("%s phrases stand beside the lives" % format(len(en), ","))

    bad = []
    for lang, text in sorted(langs.items()):
        for k in sorted(k for k in text if k not in en):
            bad.append("%s: %r is not a phrase the index shows" % (lang, k))
        for k in sorted(k for k, v in text.items() if not v.strip()):
            bad.append("%s: %r is empty" % (lang, k))
        done = len([k for k in text if k in en])
        print("   %-4s %5s of %s  (%.1f%%)"
              % (lang, format(done, ","), format(len(en), ","),
                 100.0 * done / len(en)))

    if bad:
        print("\n%d problem(s):" % len(bad))
        for b in bad:
            print("   %s" % b)
        return 1

    if args.write:
        for lang, text in sorted(langs.items()):
            p = OUT / ("saint-terms.v5.%s.json" % lang)
            # Sorted, because expand() walks a set and Python hashes strings
            # differently in every process: without this the file is written
            # with its keys in a new order each time, and a table that has
            # not changed at all shows up as changed.
            p.write_text(json.dumps(text, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")), encoding="utf-8")
            print("wrote %s  (%s KB)"
                  % (p.name, format(p.stat().st_size // 1024, ",")))
        sync_langs(PAGE, "TERMS_LANGS", "saint-terms.v5.*.json")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
