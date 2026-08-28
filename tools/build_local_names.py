#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Churches' own commemorations, named in every language.

Each Church keeps saints the others do not, and the calendar carries a
hundred and twenty-seven of them - St Nikephoros the Leper for the Greeks,
St Xenia of St Petersburg for the Russians, Queen Ketevan for the Georgians,
Tsar Lazar for the Serbs. They were carried in in English and stayed English,
so a Russian reader who chose his own Church met the whole calendar in
Russian and his own Church's saints in English.

The calendar already knows how to show a name in the reader's language: it
looks it up in NAMES_I18N. These names were simply never put there. So this
adds them, one file to a language:

    tools/local_names/<lang>.py   with  TEXT = {"<the English name>": "..."}

and appends the assignments NAMES_I18N is filled with anyway. Nothing that is
already in the table is touched; a name written twice keeps what was there.

    python3 tools/build_local_names.py --check
    python3 tools/build_local_names.py --check --lang ru
    python3 tools/build_local_names.py --write
"""
import argparse
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
TEXT_DIR = Path(__file__).resolve().parent / "local_names"

# The twenty-one besides English, as index.html offers them.
LANGS = ("el ru ro uk de es ar fr pt it sr ka zh ja ko sw hy arc hi bn ur"
         ).split()

# A language whose script is not the Latin one: a rendering that comes back
# pure ASCII in one of these has not been written, it has been copied.
NON_LATIN = set("el ru uk sr ar ka zh ja ko hy arc hi bn ur".split())

# The calendar's Greek is monotonic: of the one thousand five hundred and
# eighty-four Greek strings it already carries, all but the ones written to
# test this tool are. A polytonic name set beside them reads as another
# hand, so the breathings are refused here rather than found by a reader.
BREATHINGS = re.compile(u"[\u0313\u0314\u1F00-\u1FFF]")

BEGIN = "/* The Churches' own commemorations, in every language. */"
END = "/* end of the Churches' own commemorations. */"

# Bare keys are JavaScript and not JSON; a trailing comma likewise.
BARE_KEY = re.compile(r'([{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:')
TRAILING = re.compile(r",(\s*[}\]])")


def js_table(src, name):
    """One `const NAME = {...}` line out of index.html, as a Python object."""
    m = re.search(r"const %s\s*=\s*" % name, src)
    if not m:
        return None
    end = src.index("\n", m.end())
    raw = src[m.end():end].rstrip().rstrip(";")
    return json.loads(TRAILING.sub(r"\1", BARE_KEY.sub(r'\1"\2":', raw)))


def wanted(src):
    """Every name the local tables carry, in the order a reader meets them."""
    seen, out = set(), []
    for table in ("LOCAL_FIXED", "LOCAL_MOVABLE", "LOCAL_CIVIL"):
        d = js_table(src, table)
        if not d:
            continue
        for church in sorted(d):
            for entry in d[church]:
                n = entry.get("name")
                if n and n not in seen:
                    seen.add(n)
                    out.append(n)
    return out


def already(src):
    """Names NAMES_I18N can already show, so nothing is written twice.

    The block this tool manages is cut out first. Without that, the second
    run reads its own output as a name the calendar already had, skips it,
    and writes an empty block over the top of the one it wrote before -
    which is how three renderings disappeared the first time this was run
    twice."""
    if BEGIN in src and END in src:
        i = src.index(BEGIN)
        j = src.index(END, i) + len(END)
        src = src[:i] + src[j:]
    have = set()
    for m in re.finditer(r'NAMES_I18N\[("(?:[^"\\]|\\.)*")\]\s*=', src):
        have.add(json.loads(m.group(1)))
    m = re.search(r"NAMES_I18N\s*=\s*\{", src)
    if m:
        for k in re.finditer(r'\n\s*("(?:[^"\\]|\\.)*")\s*:\s*\{', src[m.end():m.end() + 400000]):
            have.add(json.loads(k.group(1)))
    return have


def load(lang):
    p = TEXT_DIR / ("%s.py" % lang)
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location("local_names_%s" % lang, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "TEXT", None)


def report(lang, text, names):
    """What is written, what is missing, and what should not be there."""
    n = len(names)
    if text is None:
        return 0, ["not begun"]
    want = set(names)
    problems = []
    stray = [k for k in text if k not in want]
    if stray:
        problems.append("%d name(s) the calendar does not carry: %s"
                        % (len(stray), "; ".join(sorted(stray)[:3])))
    done = 0
    ascii_only = []
    for k in names:
        v = (text.get(k) or "").strip()
        if not v:
            continue
        done += 1
        if lang in NON_LATIN and all(ord(c) < 128 for c in v):
            ascii_only.append(k)
    if ascii_only:
        problems.append("%d left in the Latin alphabet: %s"
                        % (len(ascii_only), "; ".join(ascii_only[:3])))
    if lang == "el":
        poly = [k for k in names
                if BREATHINGS.search((text.get(k) or ""))]
        if poly:
            problems.append("%d written polytonic; the calendar's Greek is "
                            "monotonic: %s" % (len(poly), "; ".join(poly[:3])))
    if done < n:
        problems.append("%d of %d written" % (done, n))
    return done, problems


def block(names, tables, have):
    """The assignments, in the shape NAMES_I18N is filled with anyway."""
    lines = [BEGIN]
    for name in names:
        if name in have:
            continue
        pairs = []
        for lang in LANGS:
            v = (tables.get(lang) or {}).get(name)
            if v and v.strip():
                pairs.append("%s:%s" % (lang, json.dumps(v.strip(),
                                                         ensure_ascii=False)))
        if not pairs:
            continue
        lines.append("NAMES_I18N[%s]={%s};"
                     % (json.dumps(name, ensure_ascii=False), ",".join(pairs)))
    lines.append(END)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--lang")
    a = ap.parse_args()

    src = io.open(PAGE, encoding="utf-8").read()
    names = wanted(src)
    if not names:
        print("the local tables carry no names; index.html has changed shape")
        return 1
    have = already(src)
    outstanding = [n for n in names if n not in have]

    langs = [a.lang] if a.lang else LANGS
    tables = {L: load(L) for L in langs}

    if a.write:
        full = {L: (load(L) or {}) for L in LANGS}
        body = block(names, full, have)
        if BEGIN in src:
            i = src.index(BEGIN)
            j = src.index(END, i) + len(END)
            src = src[:i] + body + src[j:]
        else:
            anchor = "NAMES_I18N["
            k = src.rindex(anchor)
            k = src.index("\n", k) + 1
            src = src[:k] + body + "\n" + src[k:]
        io.open(PAGE, "w", encoding="utf-8").write(src)
        written = body.count("NAMES_I18N[")
        print("%d of %d of the Churches' own commemorations now show in the "
              "reader's language" % (written, len(names)))
        return 0

    print("%d commemorations the Churches keep of their own; %d of them are "
          "not yet in the calendar's table of names"
          % (len(names), len(outstanding)))
    bad = 0
    for L in langs:
        done, problems = report(L, tables[L], names)
        mark = "  " if done == len(names) and not problems else "! "
        if mark == "! ":
            bad += 1
        print("%s%-4s %4d of %d%s" % (mark, L, done, len(names),
                                      ("   " + "; ".join(problems)) if problems else ""))
    if bad:
        print("\n%d of %d languages still to finish" % (bad, len(langs)))
        return 1
    print("\nevery Church's own saints are named in every language")
    return 0


if __name__ == "__main__":
    sys.exit(main())
