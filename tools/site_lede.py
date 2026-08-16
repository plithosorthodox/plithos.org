#!/usr/bin/env python3
"""
Say what the site is, in the page itself.

A search engine quoting this site had nothing to quote. The calendar draws
itself after the page loads, so the markup a crawler is handed carries the
masthead, the controls, empty containers and the footer - and the only whole
sentence in it was the disclaimer. So that is the sentence that was shown to
anyone searching for Plithos: what the site is not, rather than what it is.

The site already says what it is, and in every language it offers: the first
sentence of the About panel. It was only unreachable, held in a table the
page reads after it loads. This lifts that sentence into the footer, beside
the disclaimer it now precedes, where a reader meets it and a crawler can
read it without running anything.

    python3 tools/site_lede.py --check
    python3 tools/site_lede.py --write

Nothing is translated here. The words are the ones the About panel already
carries, taken as they stand.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
KEY = "siteLede"


def literal(s, name):
    """The balanced object literal assigned to `name`."""
    m = re.search(r"(?:const|var|let)\s+%s\s*=" % re.escape(name), s)
    if not m:
        raise SystemExit("no %s in the page" % name)
    i = s.index("{", m.start())
    depth = 0
    j = i
    instr = None
    esc = False
    while j < len(s):
        c = s[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == instr:
                instr = None
        else:
            if c in "\"'`":
                instr = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i, j + 1, s[i:j + 1]
        j += 1
    raise SystemExit("%s literal does not close" % name)


def as_json(lit):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write("console.log(JSON.stringify(" + lit + "))")
        path = f.name
    out = subprocess.run(["node", path], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit("could not read the literal: %s"
                         % out.stderr.strip().splitlines()[-1][:160])
    return json.loads(out.stdout)


def first_sentence(html):
    """The opening sentence of the About text, without its markup."""
    p = re.search(r"<p>(.*?)</p>", html, re.S)
    text = p.group(1) if p else html
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # Sentences here end at a full stop followed by a space and a capital, which
    # leaves abbreviations and the Greek question mark alone.
    m = re.search(r"^(.+?[.!?])(\s+[^\s])", text)
    return (m.group(1) if m else text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    s = PAGE.read_text(encoding="utf-8")
    _, _, info_lit = literal(s, "SITE_INFO_I18N")
    info = as_json(info_lit)

    ledes = {}
    for lang, html in info.items():
        if not re.fullmatch(r"[a-z]{2,3}", lang) or not isinstance(html, str):
            continue
        one = first_sentence(html)
        if one:
            ledes[lang] = one
    print("the site describes itself in %d languages" % len(ledes))
    print("  en: %s" % ledes.get("en", "")[:120])

    start, end, i18n_lit = literal(s, "I18N")
    i18n = as_json(i18n_lit)

    added = 0
    for lang, one in ledes.items():
        if lang not in i18n:
            continue
        ui = i18n[lang].setdefault("ui", {})
        if ui.get(KEY) != one:
            ui[KEY] = one
            added += 1
    print("  %s set for %d language(s)" % (KEY, added))
    missing = [l for l in i18n if re.fullmatch(r"[a-z]{2,3}", l)
               and KEY not in i18n[l].get("ui", {})]
    if missing:
        print("  ! no About text for: %s" % " ".join(sorted(missing)))

    # The table is spliced first, by byte offset. Any edit made before this
    # one would move those offsets and the splice would land in the wrong
    # place, which is exactly how this file was once overwritten.
    out = json.dumps(i18n, ensure_ascii=False, separators=(",", ":"),
                     sort_keys=True)
    s = s[:start] + out + s[end:]
    if not re.search(r"(?:const|var|let)\s+I18N\s*=", s):
        raise SystemExit("the splice destroyed the table's declaration")

    body = ('<div class="sitedesc" data-i18n="%s">%s</div>'
            % (KEY, ledes["en"]))
    if 'class="sitedesc"' in s:
        s = re.sub(r'<div class="sitedesc"[^>]*>.*?</div>', body, s, count=1,
                   flags=re.S)
        placed = "replaced"
    else:
        anchor = '<div class="discl"'
        if anchor not in s:
            raise SystemExit("no footer disclaimer to sit beside")
        s = s.replace(anchor, body + anchor, 1)
        placed = "placed before the disclaimer"
    print("  the sentence is %s in the footer" % placed)

    css = (".sitedesc{max-width:70ch;margin:0 auto 10px;color:var(--ink-soft);"
           "font-size:13.5px;line-height:1.6;text-align:center}\n")
    if ".sitedesc{" not in s:
        i = s.index("</style>")
        s = s[:i] + css + s[i:]
        print("  style added")

    if a.write:
        PAGE.write_text(s, encoding="utf-8")
        print("written")
    else:
        print("(--check: nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
