#!/usr/bin/env python3
"""
Publish the saints' lives in the languages they have been written in.

The Saints index carries a life for every commemoration - three hundred and
ninety-seven thousand words of them - and until now they were English and
only English. The names beside them have been translated for years; the lives
never were, because there is no way to translate four hundred thousand words
except by writing them.

So this is built to be filled a little at a time and to be useful at every
stage. A life that has been written in a language is served in it; a life
that has not shows the English, with nothing said about it, which is what a
reader gets today for all of them. There is no half-translated state to
explain, and no reason to wait until a language is finished before publishing
what it has.

One file to a language, fetched only when a reader opens a life, because the
whole of one language will eventually be larger than the page itself.

Lives live in tools/saint_lives/<lang>.py as TEXT = {English name: the life},
keyed by the name the index uses, so a life cannot drift onto the wrong saint
without the key failing outright.

    python3 tools/build_saint_lives.py --check
    python3 tools/build_saint_lives.py --write
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
TEXT_DIR = Path(__file__).resolve().parent / "saint_lives"


def english():
    """The English lives, which are a file now and not the page.

    They were 2.17 MB of saints.html - seventy-three per cent of it - and
    came out for the same reason the other eleven languages were never put
    in. The page is still read for the list of names, because that is what
    says which commemorations exist; the text comes from the file."""
    src = PAGE.read_text(encoding="utf-8")
    i = src.index("const SAINTS")
    eq = src.index("=", i)
    j = src.index("\n", i)
    saints = json.loads(src[eq + 1:j].rstrip().rstrip(";"))
    en_file = ROOT / "data" / "saint-lives.v6.en.json"
    if en_file.exists():
        have = json.loads(en_file.read_text(encoding="utf-8"))
        return {s["name"]: (have.get(s["name"]) or s.get("life") or "")
                for s in saints}
    return {s["name"]: (s.get("life") or "") for s in saints}


def languages():
    sys.path.insert(0, str(TEXT_DIR.parent))
    out = {}
    for m in pkgutil.iter_modules([str(TEXT_DIR)]):
        mod = importlib.import_module("saint_lives." + m.name)
        out[m.name] = dict(getattr(mod, "TEXT", {}))
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
    have = {k for k, v in en.items() if v}
    print("%d commemorations, %d with a life written" % (len(en), len(have)))

    bad = []
    for lang, text in sorted(languages().items()):
        stray = sorted(k for k in text if k not in en)
        for k in stray:
            bad.append("%s: %r is not a commemoration in the index" % (lang, k))
        empty = sorted(k for k, v in text.items() if not v.strip())
        for k in empty:
            bad.append("%s: %r is empty" % (lang, k))
        done = len([k for k in text if k in have])
        words = sum(len(v.split()) for v in text.values())
        print("   %-4s %5d of %d lives  (%s words, %.1f%%)"
              % (lang, done, len(have), format(words, ","),
                 100.0 * done / len(have)))

    if bad:
        print("\n%d problem(s):" % len(bad))
        for b in bad:
            print("   %s" % b)
        return 1

    if args.write:
        for lang, text in sorted(languages().items()):
            p = OUT / ("saint-lives.v6.%s.json" % lang)
            p.write_text(json.dumps(text, ensure_ascii=False,
                                    separators=(",", ":")), encoding="utf-8")
            print("wrote %s  (%s KB)" % (p.name, format(p.stat().st_size // 1024, ",")))
        sync_langs(PAGE, "LIVES_LANGS", "saint-lives.v6.*.json")
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
