#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Chinese on this site is simplified. Two places were not.

LANG_NAMES calls the language 简体中文. The calendar's names, the saints'
lives and their vocabulary, the prayers, the glossary, the scriptures and
the chrome are all simplified, and measured on the characters that differ
between the scripts, none of them carries a traditional one.

Two bodies did, both in copy a reader sees:

    SITE_INFO_I18N in index.html, the paragraph the site gives about
    itself when the mark is tapped, traditional throughout

    data/rule-i18n.v5.zh.json, the Rule page, traditional in twenty-nine
    of its seventy-four blocks and simplified in the rest, so a reader met
    祈禱規則 in one paragraph and 祈祷规程 in the heading above it

Mixed is worse than either. This converts both, character by character,
and prints every substitution it made so the change can be read rather
than trusted. Nothing but the script changes: a string whose length moves
is refused, because that is a phrase being rewritten and not a character
being simplified.

    python3 tools/chinese_script.py            report
    python3 tools/chinese_script.py --write    convert

The Rule's bundles are served immutable under their version, so the whole
family moves to v6 and v5 is left exactly as the readers holding it have
it. The other twenty languages are copied across untouched.
"""

import io
import json
import os
import re
import sys

try:
    import opencc
except ImportError:
    opencc = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CJK = re.compile(u"[㐀-䶿一-鿿]")


def converter():
    if opencc is None:
        raise SystemExit(
            "This needs a traditional-to-simplified converter:\n"
            "    pip install opencc-python-reimplemented")
    return opencc.OpenCC("t2s")


def convert(cc, text):
    """Simplify, and refuse anything that is not one character for one."""
    out = cc.convert(text)
    if len(out) != len(text):
        raise SystemExit("refused: %r became %r, which is a rewriting and "
                         "not a simplification" % (text[:40], out[:40]))
    return out


def changes(before, after):
    return set((b, a) for b, a in zip(before, after) if b != a)


def corpus():
    """Every Chinese this site already publishes, to check the result against."""
    import glob
    b = ""
    for p in (glob.glob(os.path.join(ROOT, "data", "*.zh.json"))
              + glob.glob(os.path.join(ROOT, "scripture", "zh", "*.json"))
              + glob.glob(os.path.join(ROOT, "tools", "saint_*", "zh.py"))):
        if "rule-i18n" in p:
            continue
        try:
            b += io.open(p, encoding="utf-8").read()
        except Exception:
            pass
    return b


def site_info(cc, write):
    p = os.path.join(ROOT, "index.html")
    s = io.open(p, encoding="utf-8").read()
    i = s.index("const SITE_INFO_I18N=")
    st = s.index("{", i)
    d = 0
    for k in range(st, len(s)):
        if s[k] == "{":
            d += 1
        elif s[k] == "}":
            d -= 1
            if not d:
                en = k + 1
                break
    tab = json.loads(s[st:en])
    made = convert(cc, tab["zh"])
    seen = changes(tab["zh"], made)
    if write and made != tab["zh"]:
        tab["zh"] = made
        io.open(p, "w", encoding="utf-8").write(
            s[:st] + json.dumps(tab, ensure_ascii=False,
                                separators=(",", ":")) + s[en:])
    return seen


def rule(cc, write):
    src = os.path.join(ROOT, "data")
    seen = set()
    import glob
    for old in sorted(glob.glob(os.path.join(src, "rule-i18n.v5.*.json"))):
        lang = os.path.basename(old).split(".")[-2]
        new = os.path.join(src, "rule-i18n.v6.%s.json" % lang)
        d = json.load(io.open(old, encoding="utf-8"))
        if lang == "zh":
            for k, v in d.items():
                made = convert(cc, v)
                seen |= changes(v, made)
                d[k] = made
        if write:
            io.open(new, "w", encoding="utf-8").write(
                json.dumps(d, ensure_ascii=False, indent=1,
                           sort_keys=True) + "\n")
    return seen


def main():
    write = "--write" in sys.argv
    cc = converter()
    seen = site_info(cc, write) | rule(cc, write)
    have = corpus()
    print("%d characters simplified:" % len(seen))
    line, unattested = [], []
    for b, a in sorted(seen):
        line.append("%s>%s" % (b, a))
        if a not in have:
            unattested.append((b, a))
    for n in range(0, len(line), 12):
        print("  " + "  ".join(line[n:n + 12]))
    if unattested:
        print("  not otherwise published on this site: %s"
              % " ".join("%s>%s" % x for x in unattested))
    else:
        print("  every one of them already stands in the site's own Chinese")
    if write:
        print("wrote index.html and data/rule-i18n.v6.*.json")
        print("point rule.html at v6 and add the stem to _headers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
