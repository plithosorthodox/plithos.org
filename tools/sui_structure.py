#!/usr/bin/env python3
"""
Fill the three fields of a SUI block that are not words.

docs/LOOP.md names them and says why they are the dangerous ones: dayFirst,
mabbr and months are a boolean and two arrays, and copying the English on any
of them is wrong in a way no proofreader of the text itself will catch. That
is exactly what happened - tools/loop_ui.py queues only string values, so a
lane writing a new SUI block was never offered them, and check_site.py caught
four languages with forty-five words each and no month names at all.

Nothing here is composed. The month names are copied from I18N in index.html,
where the calendar has published them in every language for months. What is
decided here is only the shape of a date, and it is decided the way the
language writes one:

    zh  ko   month then day, joined - 1月15日, 1월 15일 - which neither branch
             of dayFirst can express, so they take mdFmt, as Japanese does
    arc hi   day then month, as Syriac and Hindi write it, so dayFirst is true

mabbr is the abbreviation used in a list of feast days. Chinese, Korean and
Syriac month names are already short, and Hindi's are not abbreviated here
rather than have this file invent abbreviations no reader has seen; Japanese
sets that precedent, using its full forms in both fields.

    python3 tools/sui_structure.py --check
    python3 tools/sui_structure.py --write
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import check_i18n as ci                                      # noqa: E402

# the shape of a date, and nothing else
SHAPE = {
    "zh":  {"dayFirst": False, "mdFmt": "%1%2日"},
    "ko":  {"dayFirst": False, "mdFmt": "%1 %2일"},
    "arc": {"dayFirst": True},
    "hi":  {"dayFirst": True},
}


def literal_of(page, var):
    src = (ROOT / page).read_text(encoding="utf-8")
    for name, lit in ci.literals(src):
        if name == var:
            return src, lit
    raise SystemExit("no %s in %s" % (var, page))


def serialise(obj):
    tmp = TOOLS / ".sui-struct.js"
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

    _, ilit = literal_of("index.html", "I18N")
    i18n, err = ci.evaluate(ilit)
    if i18n is None:
        raise SystemExit("I18N would not evaluate: %s" % err)

    src, slit = literal_of("saints.html", "SUI")
    sui, err = ci.evaluate(slit)
    if sui is None:
        raise SystemExit("SUI would not evaluate: %s" % err)

    changed = 0
    for lang, shape in SHAPE.items():
        blk = sui.get(lang)
        if blk is None:
            print("   %-4s no SUI block yet; skipped" % lang)
            continue
        months = (i18n.get(lang) or {}).get("months")
        if not (isinstance(months, list) and len(months) == 12):
            print("   %-4s the calendar publishes no months; skipped" % lang)
            continue
        add = {}
        if "months" not in blk:
            add["months"] = list(months)
        if "mabbr" not in blk:
            add["mabbr"] = list(months)      # short already, or not invented
        for k, v in shape.items():
            if k not in blk:
                add[k] = v
        if not add:
            print("   %-4s already complete" % lang)
            continue
        print("   %-4s + %s" % (lang, ", ".join(sorted(add))))
        blk.update(add)
        changed += len(add)

    print("\n%d field(s) %s" % (changed, "written" if a.write else "to write"))
    if not (a.write and changed):
        return 0

    page = ROOT / "saints.html"
    shutil.copy(page, str(page) + ".bak")
    page.write_text(src.replace(slit, serialise(sui), 1), encoding="utf-8")
    _, again = literal_of("saints.html", "SUI")
    o, err = ci.evaluate(again)
    if o is None:
        shutil.copy(str(page) + ".bak", page)
        raise SystemExit("SUI broke, saints.html restored: %s" % err)
    Path(str(page) + ".bak").unlink(missing_ok=True)
    print("SUI still evaluates, %d languages" % len(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
