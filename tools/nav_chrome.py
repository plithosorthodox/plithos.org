#!/usr/bin/env python3
"""
One masthead nav, the same on every page.

There were three. Five pages carried the design the site actually reads by -
12.5px, a maroon pill on the page you are standing on. The Library had its
own at 11px in grey with no pill, and the calendar a third at 11px with
vertical bars between the links and the current page merely coloured. The
same seven words looked like three different sites.

The five-page design wins, because it is the one most of the site already
wears and the only one that says plainly where the reader is. It is written
once here and installed on all seven pages, and the calendar's Guide and
About read exactly as the links do, so a page with more options is still the
same nav with more in it.

Scoped to .topnav rather than to bare `nav`, because the Library's catalog
and its section list are <nav> elements too and were being styled by rules
meant for the masthead.

    python3 tools/nav_chrome.py --check
    python3 tools/nav_chrome.py --write
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = ["index.html", "saints.html", "library.html", "prayers.html",
         "rule.html", "glossary.html", "contact.html"]

# Named without naming this file: nothing in a served page describes how the
# page was made. tools/check_site.py enforces that and caught it.
MARK = "/* The masthead nav, one design on every page. */"

# The dark theme is not repeated here: assets/plithos-ui.*.css already turns
# the pill on `nav a[aria-current=page]` to the deep red and keeps the links
# free of the underline it gives every other link.
CSS = MARK + """
.topnav{display:flex;flex-wrap:wrap;align-items:center;gap:2px;min-width:0;flex-shrink:1}
.topnav a,.topnav button{font-family:var(--mono);font-size:12.5px;font-weight:400;line-height:1.2;
  text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft);white-space:nowrap;
  padding:7px 11px;border-radius:7px;background:none;border:0;margin:0;cursor:pointer;
  text-decoration:none}
.topnav a:hover,.topnav button:hover{background:var(--rail);color:var(--ink)}
.topnav a:focus-visible,.topnav button:focus-visible{outline:2px solid var(--porphyry);outline-offset:2px}
.topnav a[aria-current=page]{background:var(--porphyry);color:#f2ece0}
"""

# Every rule any page used to style the masthead nav with. Removed wholesale
# so the block above is the only thing that speaks.
DEAD = re.compile(
    r"^(?:nav\{|nav a\b|nav a:hover|\.nav\{|\.nav>|\.nav a\b|\.navbtn|\.topnav)"
    r"[^\n]*\n", re.M)

# A rule can run onto a second line; these are the ones that do.
DEAD_MULTI = [
    ".nav{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);display:flex;flex-wrap:nowrap;flex-shrink:0;gap:0;align-items:center}\n",
]

# The comment that explained a rule now gone.
DEAD_COMMENT = """/* Seven links and the two controls the shared layer mounts beside them do not
   fit a phone on one line, and a 1fr track will not go below its content, so
   the month grid pushed the page wider than the screen. Let both give way. */
"""


def masthead_nav(s):
    """(start, end) of the opening <nav> tag that holds the site links."""
    for m in re.finditer(r"<nav\b[^>]*>", s):
        after = s[m.end():m.end() + 400]
        # The page you are on links to itself with "#", so no single href is
        # present on all seven. Two of the others always are.
        hrefs = sum(1 for h in ('/saints', '/library', '/prayers', '/rule',
                                '/glossary', '/contact')
                    if ('href="%s"' % h) in after)
        if hrefs >= 4:
            return m.start(), m.end()
    return None


def fix(name, s):
    notes = []

    # 1. the nav carries the class the rules are written against
    span = masthead_nav(s)
    if not span:
        notes.append("no masthead nav found")
        return s, notes
    a, b = span
    tag = s[a:b]
    new = re.sub(r'\s*class="[^"]*"', "", tag)
    new = new[:4] + ' class="topnav"' + new[4:]
    if new != tag:
        notes.append("nav class -> topnav")
        s = s[:a] + new + s[b:]

    # 2. the old rules go
    head_end = s.index("</style>")
    head, tail = s[:head_end], s[head_end:]
    for d in DEAD_MULTI:
        if d in head:
            head = head.replace(d, "")
            notes.append("removed a wrapped rule")
    if DEAD_COMMENT in head:
        head = head.replace(DEAD_COMMENT, "")
        notes.append("removed a stale note")
    head, n = DEAD.subn("", head)
    if n:
        notes.append("removed %d rules" % n)

    # 3. and the one block goes in last, so nothing left can outrank it
    head = re.sub(re.escape(MARK) + r".*?\n(?=\S|\Z)", "", head, flags=re.S)
    head = head.rstrip("\n") + "\n" + CSS
    return head + tail, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    for name in PAGES:
        p = ROOT / name
        s = p.read_text(encoding="utf-8")
        out, notes = fix(name, s)
        print("%-14s %s" % (name, "; ".join(notes) or "already uniform"))
        if a.write and out != s:
            p.write_text(out, encoding="utf-8")
    if a.write:
        print("written")
    else:
        print("(--check: nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
