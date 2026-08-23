#!/usr/bin/env python3
"""The language picker: its flags, and keeping it on the screen.

    python3 tools/lang_picker.py --check
    python3 tools/lang_picker.py --write

Three pages carry a picker of their own - the calendar, the saints and the
library - and each holds its own copy of the flags. Two things were wrong.

The menu is positioned against the button and nothing kept it inside the
window. On the Library at a phone's width it opened thirty-eight pixels off
the left edge, so every flag in it was drawn outside the screen and a reader
saw a list of bare names; on the calendar at a tablet's width it ran off the
right instead. The flags were always there. They were never on the screen.

And the Library offered twenty-one languages where the site offers
twenty-two: Bengali and Urdu were missing, and Church Slavonic was in the
list, which is not one of the site's languages, has no interface written in
it and no flag to show, so it drew a blank row. The Slavonic Bible is reached
from the shelf of editions, which lists it, and not from the language picker.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "saints.html", "library.html"]

# Kenya. The Church of Alexandria's Swahili-speaking flock is largest in
# Kenya, where the Orthodox seminary is and where most of the parishes are;
# the flag shown was Tanzania's.
KENYA = ('<svg class="langflag" viewBox="0 0 60 40">'
         '<rect width="60" height="40" fill="#fff"/>'
         '<rect width="60" height="12" fill="#000"/>'
         '<rect y="14" width="60" height="12" fill="#bb0000"/>'
         '<rect y="28" width="60" height="12" fill="#006b3f"/>'
         '<g stroke="#fff" stroke-width="2" stroke-linecap="round">'
         '<line x1="24" y1="33" x2="36" y2="7"/>'
         '<line x1="36" y1="33" x2="24" y2="7"/></g>'
         '<ellipse cx="30" cy="20" rx="5.5" ry="11" fill="#bb0000" '
         'stroke="#fff" stroke-width="1.4"/>'
         '<path d="M30 9.5V30.5" stroke="#000" stroke-width="3.2"/>'
         '<path d="M26.6 13a5 9 0 000 14M33.4 13a5 9 0 010 14" fill="none" '
         'stroke="#fff" stroke-width="1.3"/></svg>')

CLAMP = (
    '\n/* Keep the menu on the screen. It is positioned against the button,'
    '\n   and nothing held it inside the window: on the Library at a phone\'s'
    "\n   width it opened thirty-eight pixels off the left edge, so every flag"
    '\n   in it was drawn outside the screen and the reader saw a list of bare'
    '\n   names. On the calendar at a tablet\'s width it ran off the right'
    '\n   instead. Measured after it is shown, and shifted back by however'
    '\n   much it overhangs. */'
    '\nfunction langMenuClamp(){var m=document.getElementById("langmenu");'
    'if(!m||m.hidden)return;m.style.transform="";'
    'var r=m.getBoundingClientRect(),pad=8,dx=0;'
    'if(r.left<pad)dx=pad-r.left;'
    'else if(r.right>window.innerWidth-pad)dx=(window.innerWidth-pad)-r.right;'
    'if(dx)m.style.transform="translateX("+Math.round(dx)+"px)";}')

SWFLAG = re.compile(r"sw:'<svg class=\"langflag\".*?</svg>'")


def flags_json(write):
    p = ROOT / "data" / "flags.v1.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    if d.get("sw") == KENYA:
        print("  flags: Kenya already")
        return False
    d["sw"] = KENYA
    if write:
        # A new name, because /data/flags.v1.* is served immutable for a year
        # and a change under the old name would reach nobody who has been here.
        (ROOT / "data" / "flags.v2.json").write_text(
            json.dumps(d, ensure_ascii=False), encoding="utf-8")
        print("  wrote data/flags.v2.json (Kenya)")
    else:
        print("  flags: would write data/flags.v2.json (Kenya)")
    return True


def page(name, write):
    p = ROOT / name
    s = io.open(p, encoding="utf-8").read()
    before = s
    n = len(SWFLAG.findall(s))
    if n:
        s = SWFLAG.sub("sw:'%s'" % KENYA, s)
    if "langMenuClamp" not in s:
        # The three pages write langMenuOpen three different ways, so the
        # clamp is appended to whichever body is there rather than matched
        # against one spelling of it.
        m = re.search(r"function langMenuOpen\(\)\{[^}]*\}", s)
        if not m:
            print("  %-14s no langMenuOpen found" % name)
        else:
            body = m.group(0)[:-1] + "langMenuClamp();}"
            s = s[:m.start()] + CLAMP + "\n" + body + s[m.end():]
    if name == "library.html":
        idx = io.open(ROOT / "index.html", encoding="utf-8").read()
        m = re.search(r"LANG_NAMES=\{(.*?)\};", idx, re.S)
        want = re.findall(r'([a-z]{2,3}):"([^"]*)"', m.group(1))
        cur = re.search(r"(UILANGS\s*=\s*\[)(.*?)(\];)", s, re.S)
        have = re.findall(r'\["([a-z]{2,3})","([^"]*)"\]', cur.group(2))
        order = [c for c, _ in have if c != "cu"]
        order += [c for c, _ in want if c not in order]
        names = dict(want)
        for c, n2 in have:
            names.setdefault(c, n2)
        body = ",".join('["%s","%s"]' % (c, names[c]) for c in order)
        if body != cur.group(2):
            s = s[:cur.start(2)] + body + s[cur.end(2):]
            print("  library UILANGS -> %d languages (%s)"
                  % (len(order), " ".join(order)))
    if s == before:
        print("  %-14s nothing to change" % name)
        return False
    print("  %-14s flag=%d clamp=%s" % (name, n, "langMenuClamp" in s))
    if write:
        io.open(p, "w", encoding="utf-8").write(s)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    changed = flags_json(a.write)
    for name in PAGES:
        changed |= page(name, a.write)
    if changed and not a.write:
        print("\n(--write to apply)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
