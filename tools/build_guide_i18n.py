# -*- coding: utf-8 -*-
"""The Guide, in the languages it is read in.

The Guide overlay is the calendar's one piece of continuous prose: the prayer
rule, the hours, the fast, and the terms a reader meets on the day panel. Its
English lives in KEY inside index.html and its translations in KEY_I18N beside
it. The prayer rule and the hours are written in twenty-one languages; the
fasting section, added on 24 August, is written in none, and the terms in only
seven.

Translations live in tools/guide_text/<lang>.py as

    TEXT = {"fastBody": "...", "fastSrc": "...",
            "termsHead": "...", "terms": [{"t": "...", "d": "..."}, ...]}

keyed the way KEY_I18N keys them, so a block cannot drift onto the wrong page
of the guide.

WHAT THIS CHECKS, AND WHY EACH ONE

  The shape. fastBody is HTML and the English has a fixed number of <h4>, <p>
  and <li>. A translation with fewer has dropped a section; with more has
  invented one. Both fail here.

  The script. A language written in its own alphabet whose text comes back
  pure ASCII has not been written, whatever it looks like.

  The house punctuation. No em or en dashes, no smart quotes. CLAUDE.md says
  so for the English and there is no reason the other twenty carry a different
  typography.

  The terms. The English has eleven and they are positional: KEY_I18N[lang]
  .terms[i] answers KEY.terms[i]. A short array silently re-labels the rest.

    python3 tools/build_guide_i18n.py --check
    python3 tools/build_guide_i18n.py --write
"""
import argparse
import importlib
import io
import json
import os
import pkgutil
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")
TEXT_DIR = os.path.join(ROOT, "tools", "guide_text")

# The languages the calendar offers, less English, which is the source.
LANGS = ["el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it", "sr",
         "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi", "bn", "ur"]

# Written in their own alphabets: a pure-ASCII answer is not a translation.
NON_LATIN = {"el", "ru", "uk", "sr", "ar", "ka", "zh", "ja", "ko", "hy",
             "arc", "hi", "bn", "ur"}

FIELDS = ("fastBody", "fastSrc", "termsHead", "terms")


def js_literal(src, decl):
    i = src.index(decl)
    k = i + len(decl)
    while src[k] not in "{[":
        k += 1
    a, depth, instr, q, esc = k, 0, False, "", False
    while k < len(src):
        c = src[k]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == q:
                instr = False
            k += 1
            continue
        if c in "\"'`":
            instr, q = True, c
            k += 1
            continue
        if c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
            if depth == 0:
                return a, k + 1
        k += 1
    raise SystemExit(decl + ": unbalanced")


def load_js(src, a, b, tmp):
    io.open("/tmp/gi18n.js", "w", encoding="utf-8").write(
        u"require('fs').writeFileSync(%s,JSON.stringify(%s));"
        % (json.dumps(tmp), src[a:b]))
    subprocess.check_call(["node", "/tmp/gi18n.js"])
    return json.load(io.open(tmp, encoding="utf-8"))


def english():
    src = io.open(PAGE, encoding="utf-8").read()
    a, b = js_literal(src, "const KEY=")
    return load_js(src, a, b, "/tmp/key.json")


def shape(html):
    """What a translation of this HTML must also have."""
    return {t: len(re.findall("<%s[ >]" % t, html)) for t in ("h4", "p", "li")}


def written():
    sys.path.insert(0, os.path.dirname(TEXT_DIR))
    out = {}
    for m in pkgutil.iter_modules([TEXT_DIR]):
        mod = importlib.import_module("guide_text." + m.name)
        t = getattr(mod, "TEXT", None)
        if t:
            out[m.name] = dict(t)
    return out


def faults(lang, t, en):
    bad = []
    body = t.get("fastBody") or ""
    if not body.strip():
        return ["fastBody is empty"]
    want, got = shape(en["fastBody"]), shape(body)
    for tag in ("h4", "p", "li"):
        if want[tag] != got[tag]:
            bad.append("fastBody has %d <%s> where the English has %d"
                       % (got[tag], tag, want[tag]))
    joined = body + (t.get("fastSrc") or "") + (t.get("termsHead") or "")
    joined += "".join((x.get("t", "") + x.get("d", ""))
                      for x in (t.get("terms") or []))
    if lang in NON_LATIN and joined.strip() and all(ord(c) < 128 for c in joined):
        bad.append("every character is ASCII, so nothing has been written in "
                   "the language's own alphabet")
    if re.search(u"[–—]", joined):
        bad.append("an em or en dash; the house uses hyphens")
    if re.search(u"[‘’“”]", joined):
        bad.append("a smart quote; the house uses straight quotes")
    terms = t.get("terms")
    if terms is not None and len(terms) != len(en["terms"]):
        bad.append("%d terms where the English has %d, and they are positional"
                   % (len(terms), len(en["terms"])))
    if not (t.get("fastSrc") or "").strip():
        bad.append("fastSrc is empty")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    en = english()
    have = written()
    src = io.open(PAGE, encoding="utf-8").read()
    a, b = js_literal(src, "const KEY_I18N=")
    table = load_js(src, a, b, "/tmp/keyi18n.json")

    bad, done = [], []
    for lang in LANGS:
        t = have.get(lang)
        if not t:
            continue
        f = faults(lang, t, en)
        if f:
            bad.extend("%s: %s" % (lang, x) for x in f)
        else:
            done.append(lang)

    n = 0
    for lang in done:
        entry = table.setdefault(lang, {})
        for k in FIELDS:
            v = have[lang].get(k)
            if v and entry.get(k) != v:
                entry[k] = v
                n += 1

    print("the fasting section is written in %d of %d languages: %s"
          % (len(done), len(LANGS), " ".join(done) or "-"))
    missing = [l for l in LANGS if l not in done and l not in
               set(x.split(":")[0] for x in bad)]
    if missing:
        print("  not yet written: %s" % " ".join(missing))
    for x in bad:
        print("  PROBLEM %s" % x)
    if bad:
        return 1

    if args.write and n:
        out = (src[:a] + json.dumps(table, ensure_ascii=False,
                                    separators=(",", ":")) + src[b:])
        io.open(PAGE, "w", encoding="utf-8").write(out)
        print("wrote %d field(s) into KEY_I18N" % n)
    elif args.write:
        print("nothing new to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
