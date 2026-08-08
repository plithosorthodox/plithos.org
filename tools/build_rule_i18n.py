#!/usr/bin/env python3
"""
Build the Rule page in every language.

rule.html stays English in the file. That matters: tools/check_site.py checks
every blockquote on it against the texts this site hosts, so the English
quotations cannot drift. The translations travel beside it, one file per
language, fetched only for the language a reader has chosen.

Each translatable element carries data-t="<key>". The key is derived from the
English text, so it survives the element moving around the page and only
changes when the English does - at which point that string shows up as
untranslated in every language, which is the correct outcome.

    python3 tools/build_rule_i18n.py --keys     # stamp data-t onto rule.html
    python3 tools/build_rule_i18n.py --extract  # print the English strings
    python3 tools/build_rule_i18n.py            # emit data/rule-i18n.v3.*.json

A language publishes only when every string is present. An incomplete file is
reported and withheld, because a half-translated page is worse than an English
one: the reader cannot tell which half they are missing.
"""
import argparse
import hashlib
import importlib
import json
import pkgutil
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "rule.html"
OUT = ROOT / "data"
TEXT_DIR = Path(__file__).resolve().parent / "rule_text"

# Elements whose text a reader sees. .cite carries the source line, which is
# part of the page's argument and not chrome, so it travels too.
TAGS = r"(?:h1|h2|h3|p|li)"


def key_for(text):
    return "k" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def elements(src):
    """(start, end, open_tag, inner) for every translatable element, in order.

    Matched non-greedily on the innermost tags only. The page has no nested
    paragraphs, so this is exact rather than approximate."""
    for m in re.finditer(r"<(%s)\b([^>]*)>(.*?)</\1>" % TAGS, src, re.S):
        inner = m.group(3)
        if not norm(re.sub(r"<[^>]+>", "", inner)):
            continue
        yield m


def stamp(src):
    """Add data-t to every translatable element that lacks one."""
    out, last, n = [], 0, 0
    for m in elements(src):
        attrs = m.group(2)
        if "data-t=" in attrs:
            continue
        k = key_for(norm(m.group(3)))
        out.append(src[last:m.start()])
        out.append("<%s%s data-t=\"%s\">%s</%s>"
                   % (m.group(1), attrs, k, m.group(3), m.group(1)))
        last = m.end()
        n += 1
    out.append(src[last:])
    return "".join(out), n


def strings(src):
    """key -> English inner HTML, in page order."""
    d = {}
    for m in elements(src):
        km = re.search(r'data-t="([^"]+)"', m.group(2))
        if km:
            d[km.group(1)] = norm(m.group(3))
    return d


def load_langs():
    mods = {}
    if not TEXT_DIR.exists():
        return mods
    sys.path.insert(0, str(TEXT_DIR.parent))
    for mi in pkgutil.iter_modules([str(TEXT_DIR)]):
        if mi.name.startswith("_"):
            continue
        mods[mi.name] = importlib.import_module("rule_text." + mi.name).TEXT
    return mods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", action="store_true")
    ap.add_argument("--extract", action="store_true")
    args = ap.parse_args()

    src = PAGE.read_text(encoding="utf-8")

    if args.keys:
        new, n = stamp(src)
        PAGE.write_text(new, encoding="utf-8")
        print("stamped %d elements" % n)
        src = new

    eng = strings(src)
    if not eng:
        print("no data-t keys on rule.html; run --keys first")
        return 1

    if args.extract:
        for k, v in eng.items():
            print("%s\t%s" % (k, v))
        print("\n%d strings, %d words"
              % (len(eng), sum(len(re.sub(r"<[^>]+>", " ", v).split())
                               for v in eng.values())))
        return 0

    langs = load_langs()
    published = []
    for lang in sorted(langs):
        t = langs[lang]
        missing = [k for k in eng if not t.get(k)]
        extra = [k for k in t if k not in eng]
        if extra:
            print("  %-4s %d strings no longer on the page" % (lang, len(extra)))
        if missing:
            print("  %-4s INCOMPLETE, %d of %d missing, withheld"
                  % (lang, len(missing), len(eng)))
            continue
        p = OUT / ("rule-i18n.v3.%s.json" % lang)
        p.write_text(json.dumps({k: t[k] for k in eng}, ensure_ascii=False,
                                separators=(",", ":")), encoding="utf-8")
        published.append(lang)
        print("  %-4s %d strings  (%d KB)" % (lang, len(eng),
                                              p.stat().st_size // 1024))

    # The page asks for this before it can build the picker, so it lists only
    # languages that actually have a file. A language named here with no file
    # would offer a reader a choice that silently does nothing.
    (OUT / "rule-langs.json").write_text(
        json.dumps({"langs": ["en"] + published}, ensure_ascii=False,
                   separators=(",", ":")), encoding="utf-8")

    print("\n%d strings on the page, %d languages published: %s"
          % (len(eng), len(published), " ".join(published) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
