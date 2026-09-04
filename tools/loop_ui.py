#!/usr/bin/env python3
"""
Advance the interface of a language one batch at a time.

`tools/check_i18n.py` found what is missing; this is how it gets written.
The queue is not a list anybody maintains - it is derived from the pages
themselves every time it is asked, exactly as loop.py derives its own from
the calendar, so the same command tomorrow returns the same next twenty, on
another machine, after the container is gone, and a string that has since
been written simply stops being offered.

Six surfaces, and none of them needed a code change to become writable:

    names        the commemorations index.html shows through tn(), which
                 falls back to English without saying so. PASCHA, Pentecost,
                 the Ascension, the Entry into Jerusalem and twenty-five of
                 the great movable Sundays are in this queue.
    index.I18N   the calendar's own words
    index.NOTES  the notes under the prayer rule
    saints.SUI   the Saints page's forty-eight
    library.RLEX the Library's seventy-four
    prayers.T    the whole of the Prayers page's chrome, which has never had
                 a language other than English

One file to a language, tools/ui_i18n/<lang>.py, so two lanes writing two
languages never touch the same file. Installing them into the pages is a
separate step and belongs to one session; see tools/build_ui_i18n.py.

    python3 tools/loop_ui.py el --status
    python3 tools/loop_ui.py el --next 20
    python3 tools/loop_ui.py el --append batch.txt
"""
import argparse
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
OUT = TOOLS / "ui_i18n"

sys.path.insert(0, str(TOOLS))
import check_i18n as ci                                    # noqa: E402
from loop import stray, mixed                              # noqa: E402
from translation_checks import assert_pairs                # noqa: E402

LANGS = [l for l in ci.LANGS if l != "en"]


def _lit(page, var):
    src = (ROOT / page).read_text(encoding="utf-8")
    for name, lit in ci.literals(src):
        if name == var:
            obj, err = ci.evaluate(lit)
            if obj is None:
                raise SystemExit("%s %s would not evaluate: %s" % (page, var, err))
            return obj
    raise SystemExit("no %s in %s" % (var, page))


def _flat(d, prefix=""):
    out = {}
    for k, v in (d or {}).items():
        kk = prefix + "." + k if prefix else k
        if isinstance(v, dict):
            out.update(_flat(v, kk))
        elif isinstance(v, str) and v.strip():
            out[kk] = v
    return out


def _get(d, dotted):
    cur = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur if isinstance(cur, str) else None


def english():
    """{surface: {key: the English text}} - read from the pages, not stored."""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    have = {ci.unesc(h)
            for h in re.findall(r'NAMES_I18N\[(?:"((?:[^"\\]|\\.)*)")\]\s*=', src)}
    names = []
    for var in ("TWELVE_MOVABLE", "PASCHAL_NAMES", "WESTERN_MOVABLE",
                "MOVABLE_SYNAXARION", "SYNAXARION"):
        obj = _lit("index.html", var)

        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in ("name", "n") and isinstance(v, str):
                        names.append(v)
                    elif k not in ("ep", "go", "e", "g"):
                        walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
            elif isinstance(x, str):
                names.append(x)
        walk(obj)
    # a commemoration, not a reading or a rubric
    names = [n for n in names
             if n not in have and len(n) > 6 and " " in n
             and not re.match(r'^\d|^[A-Z]?[a-z]*\.? ?\d+[:.]', n)
             and not re.search(r'\b\d+:\d+', n)]

    return {
        "names": {n: n for n in sorted(set(names))},
        # Every ui string, not a hand-picked two. `allLives` was absent from
        # the table for every language including English, so t() returned the
        # key and the page printed ALLLIVES in capitals with the words run
        # together - and the queue could not offer it, because the queue only
        # ever looked at about and guide.
        "index.I18N": _flat(_lit("index.html", "I18N")["en"]),
        "index.NOTES": _flat(_lit("index.html", "NOTES_I18N").get("en", {})),
        "saints.SUI": {k: v for k, v in _lit("saints.html", "SUI")["en"].items()
                       if isinstance(v, str) and v.strip()},
        "library.RLEX": {k: v for k, v in _lit("library.html", "RLEX")["en"].items()
                         if isinstance(v, str) and v.strip()},
        "prayers.T": {k: v for k, v in _lit("prayers.html", "T")["en"].items()
                      if isinstance(v, str) and v.strip()},
    }


def carried(lang):
    """What the pages already serve this language, plus what it has written."""
    got = set()
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    for m in re.finditer(r'NAMES_I18N\[(?:"((?:[^"\\]|\\.)*)")\]\s*=\s*(\{[^;]*\})', src):
        key = ci.unesc(m.group(1))
        if re.search(r'[{,]\s*"?' + lang + r'"?\s*:', m.group(2)):
            got.add(("names", key))
    for surface, page, var in (("index.I18N", "index.html", "I18N"),
                               ("index.NOTES", "index.html", "NOTES_I18N"),
                               ("saints.SUI", "saints.html", "SUI"),
                               ("library.RLEX", "library.html", "RLEX"),
                               ("prayers.T", "prayers.html", "T")):
        blk = _lit(page, var).get(lang)
        if not blk:
            continue
        for k in _flat(blk):
            got.add((surface, k))
    got |= {(s, k) for s, k in written(lang)}
    return got


def written(lang):
    p = OUT / ("%s.py" % lang)
    if not p.exists():
        return {}
    spec = importlib.util.spec_from_file_location("ui_" + lang, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return {tuple(k.split("|", 1)): v for k, v in getattr(m, "TEXT", {}).items()}


def remaining(lang):
    en = english()
    have = carried(lang)
    out = []
    # smallest surface first, so a language finishes whole surfaces early and
    # the largest - the commemoration names - is what a long run is spent on
    for surface in ("index.I18N", "index.NOTES", "prayers.T",
                    "saints.SUI", "library.RLEX", "names"):
        for k in sorted(en[surface]):
            if (surface, k) not in have:
                out.append((surface, k, en[surface][k]))
    return out


HEAD = '''# -*- coding: utf-8 -*-
"""%s interface strings. TEXT = {"surface|key": the rendering}.

Written against tools/loop_ui.py, which derives what is missing from the
pages themselves. Installed by tools/build_ui_i18n.py; nothing here edits a
page directly, so two languages can be written at once.
"""
TEXT = {
'''


def append(lang, path, count):
    todo = remaining(lang)[:count]
    blocks = [b.strip() for b in Path(path).read_text(encoding="utf-8").split("@@@")]
    blocks = [b for b in blocks if b]
    if len(blocks) != len(todo):
        raise SystemExit("%d blocks against %d queued" % (len(blocks), len(todo)))
    for (surface, key, en), b in zip(todo, blocks):
        if "\n" in b:
            raise SystemExit("one line to a block; %r has %d" % (key, b.count("\n") + 1))
        if not b.strip():
            raise SystemExit("%r is empty" % key)
    vals = blocks
    assert_pairs(lang, [("%s|%s" % (s, k), en, value)
                        for (s, k, en), value in zip(todo, vals)])
    bad = stray(lang, vals)
    if bad:
        raise SystemExit("characters %s may not carry: %s"
                         % (lang, " ".join(repr(c) for c in bad)))
    m = mixed(vals)
    if m:
        raise SystemExit("two alphabets in one word: %s" % ", ".join(m[:6]))

    p = OUT / ("%s.py" % lang)
    OUT.mkdir(exist_ok=True)
    if p.exists():
        shutil.copy(p, str(p) + ".bak")
        src = p.read_text(encoding="utf-8").rstrip()
        assert src.endswith("}")
        head = src[:-1].rstrip() + "\n"
    else:
        head = HEAD % lang.upper()
    body = "".join('\n%s:\n%s,\n' % (json.dumps("%s|%s" % (s, k), ensure_ascii=False),
                                     json.dumps(v, ensure_ascii=False))
                   for (s, k, _), v in zip(todo, vals))
    p.write_text(head + body + "}\n", encoding="utf-8")
    try:
        written(lang)
    except Exception as e:
        if Path(str(p) + ".bak").exists():
            shutil.copy(str(p) + ".bak", p)
        raise SystemExit("would not import, restored: %s" % e)
    print("wrote %d; %d remain" % (len(vals), len(remaining(lang))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--next", type=int)
    ap.add_argument("--append")
    a = ap.parse_args()
    if a.lang not in LANGS:
        raise SystemExit("not a language of this site: %s" % a.lang)

    if a.append:
        n = a.next or 20
        return append(a.lang, a.append, n)

    todo = remaining(a.lang)
    if a.status or not a.next:
        en = english()
        total = sum(len(v) for v in en.values())
        print("%-4s %d of %d interface strings written  (%d remain)"
              % (a.lang, total - len(todo), total, len(todo)))
        by = {}
        for s, k, _ in todo:
            by[s] = by.get(s, 0) + 1
        for s in sorted(by):
            print("     %-14s %4d" % (s, by[s]))
        return 0

    for surface, key, en in todo[:a.next]:
        print("--- %s | %s\n%s" % (surface, key, en))
    print("\n%d shown; separate the renderings with lines containing only @@@,"
          " in this order." % min(a.next, len(todo)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
