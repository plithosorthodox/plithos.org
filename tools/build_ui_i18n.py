#!/usr/bin/env python3
"""
Install the interface strings the lanes have written into the pages.

A lane writes one file, tools/ui_i18n/<lang>.py, and never touches a page.
This is the other half: it merges those renderings into the table each one
belongs to and writes the page back. It edits index.html, saints.html,
library.html and prayers.html, so it belongs to one session at a time and no
lane may run it - the same rule the other builders keep.

Five destinations, four of them ordinary object literals and one not:

    names          NAMES_I18N["<the English name>"]={...}; statements in
                   index.html, about sixteen hundred of them, appended to
                   or merged with rather than rewritten
    index.I18N     I18N.<lang>.ui.about and .guide
    index.NOTES    NOTES_I18N.<lang>
    saints.SUI     SUI.<lang>          library.RLEX  RLEX.<lang>
    prayers.T      T.<lang>

The literal is re-serialised by node from the merged object rather than
patched by regular expression, so a table cannot be left half-valid; the
page is parsed again afterwards and the write is rolled back if it is not.

    python3 tools/build_ui_i18n.py --check
    python3 tools/build_ui_i18n.py --write
"""
import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
OUT = TOOLS / "ui_i18n"

sys.path.insert(0, str(TOOLS))
import check_i18n as ci                                     # noqa: E402

DEST = {
    "index.I18N":   ("index.html", "I18N"),
    "index.NOTES":  ("index.html", "NOTES_I18N"),
    "saints.SUI":   ("saints.html", "SUI"),
    "library.RLEX": ("library.html", "RLEX"),
    "prayers.T":    ("prayers.html", "T"),
}


def written():
    """{lang: {(surface, key): rendering}}"""
    out = {}
    if not OUT.exists():
        return out
    for p in sorted(OUT.glob("*.py")):
        lang = p.stem
        if lang.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location("ui_" + lang, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        got = {}
        for k, v in getattr(m, "TEXT", {}).items():
            if "|" not in k:
                raise SystemExit("%s: %r is not surface|key" % (p.name, k))
            s, kk = k.split("|", 1)
            got[(s, kk)] = v
        out[lang] = got
    return out


def _set(d, dotted, value):
    cur = d
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = value


def serialise(obj):
    tmp = TOOLS / ".ui-build.js"
    tmp.write_text("const O=" + json.dumps(obj, ensure_ascii=False)
                   + ";process.stdout.write(JSON.stringify(O));", encoding="utf-8")
    try:
        r = subprocess.run(["node", str(tmp)], capture_output=True, text=True,
                           timeout=180, encoding="utf-8")
    finally:
        tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        raise SystemExit("node: " + r.stderr[:200])
    return r.stdout


def install_tables(all_written, write):
    changed = 0
    by_page = {}
    for surface, (page, var) in DEST.items():
        by_page.setdefault(page, []).append((surface, var))
    for page, jobs in by_page.items():
        src = (ROOT / page).read_text(encoding="utf-8")
        original = src
        for surface, var in jobs:
            lit = None
            for name, l in ci.literals(src):
                if name == var:
                    lit = l
                    break
            if lit is None:
                print("   %s: no %s" % (page, var))
                continue
            obj, err = ci.evaluate(lit)
            if obj is None:
                raise SystemExit("%s %s would not evaluate: %s" % (page, var, err))
            n = 0
            for lang, got in all_written.items():
                for (s, key), value in got.items():
                    if s != surface:
                        continue
                    _set(obj.setdefault(lang, {}), key, value)
                    n += 1
            if not n:
                continue
            print("   %-14s %-12s %4d renderings" % (page, var, n))
            changed += n
            src = src.replace(lit, serialise(obj), 1)
        if write and src != original:
            shutil.copy(ROOT / page, str(ROOT / page) + ".bak")
            (ROOT / page).write_text(src, encoding="utf-8")
    return changed


NAMES_RE = re.compile(r'NAMES_I18N\[(?:"((?:[^"\\]|\\.)*)")\]\s*=\s*(\{[^;]*?\});')


def install_names(all_written, write):
    page = ROOT / "index.html"
    src = page.read_text(encoding="utf-8")
    add = {}
    for lang, got in all_written.items():
        for (s, key), value in got.items():
            if s == "names":
                add.setdefault(key, {})[lang] = value
    if not add:
        return 0
    existing = {}
    for m in NAMES_RE.finditer(src):
        existing[ci.unesc(m.group(1))] = m
    n = 0
    out = src
    tail = []
    for key, per in sorted(add.items()):
        m = existing.get(key)
        if m:
            obj = json.loads(m.group(2)) if m.group(2).strip().startswith('{"') else None
            if obj is None:
                obj, err = ci.evaluate(m.group(2))
                if obj is None:
                    raise SystemExit("NAMES_I18N[%r] would not evaluate: %s" % (key, err))
            obj.update(per)
            stmt = 'NAMES_I18N[%s]=%s;' % (json.dumps(key, ensure_ascii=False),
                                           serialise(obj))
            out = out.replace(m.group(0), stmt, 1)
        else:
            tail.append('NAMES_I18N[%s]=%s;' % (json.dumps(key, ensure_ascii=False),
                                                serialise(per)))
        n += len(per)
    if tail:
        anchor = list(NAMES_RE.finditer(out))
        if not anchor:
            raise SystemExit("no NAMES_I18N statement to append after")
        last = anchor[-1]
        out = out[:last.end()] + "\n" + "\n".join(tail) + out[last.end():]
    print("   %-14s %-12s %4d renderings over %d names"
          % ("index.html", "NAMES_I18N", n, len(add)))
    if write:
        shutil.copy(page, str(page) + ".bak")
        page.write_text(out, encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    got = written()
    if not got:
        print("nothing written yet in tools/ui_i18n/")
        return 0
    print("%d languages have interface strings written:" % len(got))
    for l in sorted(got):
        print("   %-4s %4d" % (l, len(got[l])))
    print()
    total = install_names(got, a.write)
    total += install_tables(got, a.write)
    print("\n%d renderings %s" % (total, "installed" if a.write else "ready to install"))
    if a.write:
        for page in ("index.html", "saints.html", "library.html", "prayers.html"):
            src = (ROOT / page).read_text(encoding="utf-8")
            for name, lit in ci.literals(src):
                if name in ("I18N", "SUI", "RLEX", "T", "NOTES_I18N"):
                    o, err = ci.evaluate(lit)
                    if o is None:
                        shutil.copy(str(ROOT / page) + ".bak", ROOT / page)
                        raise SystemExit("%s %s broke, page restored: %s"
                                         % (page, name, err))
        print("every table still evaluates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
