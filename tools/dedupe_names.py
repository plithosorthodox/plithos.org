#!/usr/bin/env python3
"""
Collapse the duplicated NAMES_I18N statements in index.html.

index.html assigns each commemoration's renderings with a statement of its
own, about seventeen hundred of them. The installer merged a new rendering
into the statement already there - unless it could not find it, and for a
name that is not ASCII it could not: the key was read back through
`.encode().decode("unicode_escape")`, which re-reads the UTF-8 bytes one to a
character, so an em dash came back as three and matched nothing. Those names
got a second statement appended instead, and a third on the next install.

Seventy-six commemorations ended with more than one - PASCHA, Clean Monday,
Ash Wednesday, and every name printed with curly quotes among them. No reader
lost anything, because the statement that runs last carried everything the
earlier ones did; but the file grew a hundred and forty-seven statements that
say what an earlier line already said, and the audit read the mangled key and
reported all of them untranslated.

The reader on the key is fixed in tools/check_i18n.py. This collapses what
accumulated while it was not: the statements for one name are merged in the
order they appear, so a later rendering still wins, and the merged statement
is written where the first one stood.

    python3 tools/dedupe_names.py --check
    python3 tools/dedupe_names.py --write
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import check_i18n as ci                                      # noqa: E402

STMT = re.compile(r'NAMES_I18N\[(?:"((?:[^"\\]|\\.)*)")\]\s*=\s*(\{[^;]*?\});')


def serialise(obj):
    tmp = TOOLS / ".dedupe.js"
    tmp.write_text("const O=" + json.dumps(obj, ensure_ascii=False)
                   + ";process.stdout.write(JSON.stringify(O));", encoding="utf-8")
    try:
        r = subprocess.run(["node", str(tmp)], capture_output=True, text=True,
                           timeout=180)
    finally:
        tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        raise SystemExit("node: " + r.stderr[:200])
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    page = ROOT / "index.html"
    src = page.read_text(encoding="utf-8")
    matches = list(STMT.finditer(src))
    order, groups = [], {}
    for m in matches:
        key = ci.unesc(m.group(1))
        if key not in groups:
            order.append(key)
            groups[key] = []
        groups[key].append(m)

    dup = [k for k in order if len(groups[k]) > 1]
    print("%d statements, %d names, %d named more than once"
          % (len(matches), len(order), len(dup)))
    if not dup:
        return 0
    for k in dup[:6]:
        print("   x%d  %s" % (len(groups[k]), k[:70]))
    if len(dup) > 6:
        print("   ... and %d more" % (len(dup) - 6))

    shadowed = 0
    out = src
    for key in dup:
        ms = groups[key]
        merged = {}
        for m in ms:
            o, err = ci.evaluate(m.group(2))
            if o is None:
                raise SystemExit("NAMES_I18N[%r] would not evaluate: %s" % (key, err))
            merged.update(o)
        last, _ = ci.evaluate(ms[-1].group(2))
        shadowed += len(set(merged) - set(last))
        stmt = 'NAMES_I18N[%s]=%s;' % (json.dumps(key, ensure_ascii=False),
                                       serialise(merged))
        out = out.replace(ms[0].group(0), stmt, 1)
        for m in ms[1:]:
            out = out.replace("\n" + m.group(0), "", 1)
            out = out.replace(m.group(0), "", 1)

    print("\n%d rendering(s) the last statement had dropped are restored"
          % shadowed)
    print("%d statement(s) %s" % (len(matches) - len(order),
                                  "removed" if a.write else "to remove"))
    if not a.write:
        return 0

    shutil.copy(page, str(page) + ".bak")
    page.write_text(out, encoding="utf-8")
    again = list(STMT.finditer(page.read_text(encoding="utf-8")))
    keys = {ci.unesc(m.group(1)) for m in again}
    if len(again) != len(order) or keys != set(order):
        shutil.copy(str(page) + ".bak", page)
        raise SystemExit("the names would not come back whole; index.html restored")
    for m in again:
        if ci.evaluate(m.group(2))[0] is None:
            shutil.copy(str(page) + ".bak", page)
            raise SystemExit("a statement no longer evaluates; index.html restored")
    Path(str(page) + ".bak").unlink(missing_ok=True)
    print("%d statements, one to a name, all evaluating" % len(again))
    return 0


if __name__ == "__main__":
    sys.exit(main())
