#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What each page calls itself, in each language.

Every page on this site carried one title and one description, in English,
at all one hundred and fifty-four of its addresses. functions/_lang.js
serves /el/rule and its twenty companions properly - it sets the document's
language, rewrites the canonical, and answers the question about language
before the page's own scripts put it - but it did not touch the head's
words. So a Greek page told a browser tab, a search result and a shared
link that it was English.

Nothing here is written. Each page already says what it is, in every
language, somewhere the reader can see:

    /           the nav word for the calendar, and the paragraph the site
                gives about itself when the mark is tapped
    /saints     the Saints page's own title and lede
    /library    the Library's nav word and the line over the whole shelf
    /prayers    the prayer book's heading and lede
    /rule       the first two blocks of the Rule, which are its heading
                and its opening sentence
    /glossary   the glossary's heading and lede
    /contact    the contact page's heading and lede

English is left exactly as it stands. Its titles are the ones already
written down elsewhere and indexed, and moving them would cost the only
pages that are found today.

    python3 tools/page_meta.py            report
    python3 tools/page_meta.py --write    write functions/_meta.js
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "functions", "_meta.js")

PAGES = ["", "saints", "library", "prayers", "rule", "glossary", "contact"]


def read(*parts):
    return io.open(os.path.join(ROOT, *parts), encoding="utf-8").read()


def literal(src, name):
    """The whole of a brace-balanced assignment.

    Some of these tables are JSON and some are written the way the rest of
    the page is written, with bare keys and single quotes. Node reads both,
    and is already required to run nothing here, so it is asked only when
    the strict reader will not have it."""
    i = src.index(name)
    start = src.index("{", i)
    depth = 0
    for k in range(start, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if not depth:
                body = src[start:k + 1]
                break
    else:
        raise SystemExit("%s never closes" % name)
    try:
        return json.loads(body)
    except ValueError:
        pass
    tmp = os.path.join(tempfile.gettempdir(), "plithos-literal.js")
    io.open(tmp, "w", encoding="utf-8").write(
        "console.log(JSON.stringify(" + body + "));")
    out = subprocess.check_output(["node", tmp])
    os.remove(tmp)
    return json.loads(out.decode("utf-8"))


def sentence(html):
    """The first paragraph of a block of the site's own prose, as text."""
    m = re.search(r"<p>(.*?)</p>", html or "", re.S)
    text = m.group(1) if m else (html or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def languages(idx):
    m = re.search(r"LANG_NAMES=\{(.*?)\};", idx)
    return [x.group(1) for x in re.finditer(r'(\w+):"', m.group(1))]


def gather():
    idx = read("index.html")
    langs = languages(idx)

    i18n = literal(idx, "const I18N=")
    site = literal(idx, "const SITE_INFO_I18N=")
    sui = literal(read("saints.html"), "const SUI=")
    rlex = literal(read("library.html"), "const RLEX=")
    contact = literal(read("contact.html"), "var T=")
    prayers = json.loads(read("data", "prayers.v2.json"))["ui"]
    gloss = json.loads(read("data", "glossary.v4.json"))["ui"]

    # The Rule's prose is keyed by a hash of the English it replaces; the
    # first two blocks are its heading and its opening sentence.
    rule_en = read("rule.html")
    rule_keys = re.findall(r'data-t="(\w+)"', rule_en)[:2]

    out = {}
    for lang in langs:
        if lang == "en":
            continue
        rule = {}
        p = os.path.join(ROOT, "data", "rule-i18n.v5.%s.json" % lang)
        if os.path.exists(p):
            rule = json.load(io.open(p, encoding="utf-8"))
        pages = {
            "": (((i18n.get(lang) or {}).get("ui") or {}).get("calendar"),
                 sentence(site.get(lang))),
            "saints": ((sui.get(lang) or {}).get("title"),
                       (sui.get(lang) or {}).get("lede")),
            "library": ((rlex.get(lang) or {}).get("navLibrary"),
                        (rlex.get(lang) or {}).get("secBrowseDesc")),
            "prayers": ((prayers.get(lang) or {}).get("h1"),
                        (prayers.get(lang) or {}).get("lede")),
            "rule": (rule.get(rule_keys[0]), sentence(rule.get(rule_keys[1]))),
            "glossary": ((gloss.get(lang) or {}).get("h1"),
                         (gloss.get(lang) or {}).get("lede")),
            "contact": ((contact.get(lang) or {}).get("h1"),
                        (contact.get(lang) or {}).get("lede")),
        }
        here = {}
        for slug, (title, desc) in pages.items():
            if not title or not desc:
                continue
            here[slug] = {"t": "%s · Plithos" % title.strip(),
                          "d": desc.strip()}
        out[lang] = here
    return langs, out


def main():
    write = "--write" in sys.argv
    langs, meta = gather()
    short = []
    for lang in langs:
        if lang == "en":
            continue
        have = meta.get(lang) or {}
        missing = [p or "/" for p in PAGES if p not in have]
        if missing:
            short.append("%s (%s)" % (lang, ", ".join(missing)))
    print("%d languages, %d of %d pages named in each"
          % (len(langs) - 1, min(len(v) for v in meta.values()), len(PAGES)))
    if short:
        print("  no published heading or lede for: %s" % "; ".join(short))
    if not write:
        return 0
    body = ("/* Written by tools/page_meta.py from what each page already\n"
            " * says about itself in each language. Do not edit by hand: the\n"
            " * words live on the pages, not here.\n"
            " *\n"
            " * English is absent on purpose. Its titles are the ones already\n"
            " * indexed and they are left exactly as the pages carry them.\n"
            " */\n"
            "export const META = %s;\n"
            % json.dumps(meta, ensure_ascii=False, sort_keys=True,
                         indent=1))
    io.open(OUT, "w", encoding="utf-8").write(body)
    print("wrote functions/_meta.js (%.0f KB)"
          % (os.path.getsize(OUT) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
