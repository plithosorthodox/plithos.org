#!/usr/bin/env python3
"""
Install the interface strings the lanes have written into the pages.

A lane writes one file, tools/ui_i18n/<lang>.py, and never touches a page.
This is the other half: it merges those renderings into the table each one
belongs to and writes the page back. It edits index.html, saints.html,
library.html, prayers.html and contact.html, and writes the shared bundle, so
it belongs to one session at a time and no lane may run it - the same rule the
other builders keep.

Thirteen destinations, eight ordinary object literals, three differently
shaped calendar tables and two not:

    names          NAMES_I18N["<the English name>"]={...}; statements in
                   index.html, about sixteen hundred of them, appended to
                   or merged with rather than rewritten
    index.I18N     I18N.<lang>.ui.about and .guide
    index.NOTES    NOTES_I18N.<lang>
    index.ARIA     ARIA_I18N.<lang>
    index.VIEW     VIEW_I18N.<lang>
    index.UX       UX.<lang>
    index.TAGLINE  TAGLINE_I18N.<lang>
    index.SITE_INFO SITE_INFO_I18N.<lang>
    index.CAT      CAT_I18N[<English category>].<lang>
    index.SUN_AP   SUN_AP.<lang>, from a single {n} template
    saints.SUI     SUI.<lang>          library.RLEX  RLEX.<lang>
    prayers.T      T.<lang>            contact.T     T.<lang>
    shared.UI      data/ui-i18n.v6.<lang>.json

The literal is re-serialised by node from the merged object rather than
patched by regular expression, so a table cannot be left half-valid; the
page is parsed again afterwards and the write is rolled back if it is not.

    python3 tools/build_ui_i18n.py --check
    python3 tools/build_ui_i18n.py --write
"""
import argparse
import ast
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
    "index.ARIA":   ("index.html", "ARIA_I18N"),
    "index.VIEW":   ("index.html", "VIEW_I18N"),
    "index.UX":     ("index.html", "UX"),
    "saints.SUI":   ("saints.html", "SUI"),
    "library.RLEX": ("library.html", "RLEX"),
    "prayers.T":    ("prayers.html", "T"),
    "contact.T":    ("contact.html", "T"),
}

SCALAR_DEST = {
    "index.TAGLINE":  ("index.html", "TAGLINE_I18N"),
    "index.SITE_INFO": ("index.html", "SITE_INFO_I18N"),
}

REVERSE_DEST = {
    "index.CAT": ("index.html", "CAT_I18N"),
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
        tree = ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        for node in tree.body:
            if (not isinstance(node, ast.Assign)
                    or not any(isinstance(t, ast.Name) and t.id == "TEXT"
                               for t in node.targets)
                    or not isinstance(node.value, ast.Dict)):
                continue
            keys = [k.value for k in node.value.keys
                    if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            dup = sorted(set(k for k in keys if keys.count(k) > 1))
            if dup:
                raise SystemExit("%s repeats TEXT key(s): %s"
                                 % (p.name, ", ".join(dup)))
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


def install_scalars(all_written, write):
    """Install tables whose language value is a string, not an object."""
    changed = 0
    by_page = {}
    for surface, (page, var) in SCALAR_DEST.items():
        by_page.setdefault(page, []).append((surface, var))
    for page, jobs in by_page.items():
        src = (ROOT / page).read_text(encoding="utf-8")
        original = src
        for surface, var in jobs:
            lit = next((l for name, l in ci.literals(src) if name == var), None)
            if lit is None:
                raise SystemExit("%s: no %s" % (page, var))
            obj, err = ci.evaluate(lit)
            if obj is None:
                raise SystemExit("%s %s would not evaluate: %s" % (page, var, err))
            n = 0
            for lang, got in all_written.items():
                value = got.get((surface, "value"))
                if value is None:
                    continue
                obj[lang] = value
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


def install_reverse_tables(all_written, write):
    """Install tables keyed by the English source, then by language."""
    changed = 0
    for surface, (page, var) in REVERSE_DEST.items():
        src = (ROOT / page).read_text(encoding="utf-8")
        original = src
        lit = next((l for name, l in ci.literals(src) if name == var), None)
        if lit is None:
            raise SystemExit("%s: no %s" % (page, var))
        obj, err = ci.evaluate(lit)
        if obj is None:
            raise SystemExit("%s %s would not evaluate: %s" % (page, var, err))
        allowed = set(obj)
        if var == "CAT_I18N":
            allowed.update(json.loads('"%s"' % m.group(1))
                           for m in re.finditer(
                               r'"cat":"((?:[^"\\]|\\.)*)"', src))
        n = 0
        for lang, got in all_written.items():
            for (s, key), value in got.items():
                if s != surface:
                    continue
                if key not in allowed:
                    raise SystemExit("%s: %r is not an English %s key"
                                     % (surface, key, var))
                obj.setdefault(key, {})[lang] = value
                n += 1
        if n:
            print("   %-14s %-12s %4d renderings" % (page, var, n))
            changed += n
            src = src.replace(lit, serialise(obj), 1)
        if write and src != original:
            shutil.copy(ROOT / page, str(ROOT / page) + ".bak")
            (ROOT / page).write_text(src, encoding="utf-8")
    return changed


def install_sun_ap(all_written, write):
    """Install the numbered Sunday phrase as an ES5 function."""
    page = ROOT / "index.html"
    src = page.read_text(encoding="utf-8")
    original = src
    n = 0
    for lang, got in sorted(all_written.items()):
        value = got.get(("index.SUN_AP", "value"))
        if value is None:
            continue
        if value.count("{n}") != 1 or re.search(r"\{(?!n\})|(?<!\{n)\}", value):
            raise SystemExit("index.SUN_AP %s must contain exactly one {n}"
                             % lang)
        before, after = value.split("{n}")
        stmt = "SUN_AP.%s=function(n){return %s+n+%s;};" % (
            lang, json.dumps(before, ensure_ascii=False),
            json.dumps(after, ensure_ascii=False))
        old = re.search(r"SUN_AP\.%s=function\(n\)\{[^;]*;\};" % lang, src)
        if old:
            src = src[:old.start()] + stmt + src[old.end():]
        else:
            anchor = "function sundayAP(n)"
            at = src.find(anchor)
            if at < 0:
                raise SystemExit("index.html has no sundayAP anchor")
            src = src[:at] + stmt + "\n" + src[at:]
        n += 1
    if n:
        print("   %-14s %-12s %4d renderings" % ("index.html", "SUN_AP", n))
    if write and src != original:
        shutil.copy(page, str(page) + ".bak")
        page.write_text(src, encoding="utf-8")
    return n


NAMES_RE = re.compile(r'NAMES_I18N\[(?:"((?:[^"\\]|\\.)*)")\]\s*=\s*(\{[^;]*?\});')
# The opening marker of the block tools/build_local_names.py owns. Anything
# appended after it is inside that block and will not survive the next run
# of it.
LOCAL_NAMES_BLOCK = "/* The Churches' own commemorations, in every language. */"


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
        # Append before the block tools/build_local_names.py manages, never
        # inside it. That block sits at the end of the NAMES_I18N region, so
        # "after the last statement" lands within it, and the next run of that
        # tool rewrites the block from its own sources and takes these names
        # with it. It went unnoticed because nothing failed: this tool reported
        # the renderings installed, that tool reported its own count, and one
        # hundred and seven names in twenty-two languages - Pascha, Great and
        # Holy Friday, Silouan the Athonite, Sophrony of Essex - were simply
        # gone from the page.
        region = out
        cut = out.find(LOCAL_NAMES_BLOCK)
        if cut >= 0:
            region = out[:cut]
        anchor = list(NAMES_RE.finditer(region))
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


def install_shared(all_written, write):
    """Write the shared chrome as one new language file.

    The family is immutable, but a language not previously present is a new
    path and therefore needs no family bump. Existing language files are not
    rewritten here.
    """
    n = 0
    for lang, got in sorted(all_written.items()):
        add = {key: value for (surface, key), value in got.items()
               if surface == "shared.UI"}
        if not add:
            continue
        template = json.loads((ROOT / "data" / "ui-i18n.v6.en.json")
                              .read_text(encoding="utf-8"))
        out = dict(template)
        for key, value in add.items():
            _set(out, key, value)

        # The palette's shelf tags are the same vocabulary already written
        # in library.RLEX. Read them from that source rather than asking for
        # a second translation. Twelve current tags do not yet appear as
        # Library facets; those may be supplied explicitly in shared.UI.tags.
        ref = json.loads((ROOT / "data" / "ui-i18n.v6.ru.json")
                         .read_text(encoding="utf-8")).get("tags") or {}
        tags = dict(out.get("tags") or {})
        ordinal = {"1": "1st", "2": "2nd", "3": "3rd"}
        for tag in ref:
            dim, value = tag.split(":", 1)
            if dim == "translator":
                tags[tag] = ""
                continue
            if tags.get(tag):
                continue
            if dim == "century":
                value = ordinal.get(value, value + "th") + " century"
            tags[tag] = got.get(("library.RLEX", "lx:" + value), "")
        out["tags"] = tags
        path = ROOT / "data" / ("ui-i18n.v6.%s.json" % lang)
        if path.exists():
            current = json.loads(path.read_text(encoding="utf-8"))
            if current != out:
                raise SystemExit(
                    "%s already exists and is served immutable; "
                    "publish the changed family under a new version" % path.name)
            out = current
        n += len(add)
        print("   %-14s %-12s %4d renderings"
              % (path.name, "shared.UI", len(add)))
        if write and not path.exists():
            path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
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
    total += install_shared(got, a.write)
    total += install_tables(got, a.write)
    total += install_scalars(got, a.write)
    total += install_reverse_tables(got, a.write)
    total += install_sun_ap(got, a.write)
    print("\n%d renderings %s" % (total, "installed" if a.write else "ready to install"))
    if a.write:
        for page in ("index.html", "saints.html", "library.html", "prayers.html",
                     "contact.html"):
            src = (ROOT / page).read_text(encoding="utf-8")
            for name, lit in ci.literals(src):
                if name in ("I18N", "SUI", "RLEX", "T", "NOTES_I18N",
                            "ARIA_I18N", "VIEW_I18N", "UX", "TAGLINE_I18N",
                            "SITE_INFO_I18N", "CAT_I18N"):
                    o, err = ci.evaluate(lit)
                    if o is None:
                        shutil.copy(str(ROOT / page) + ".bak", ROOT / page)
                        raise SystemExit("%s %s broke, page restored: %s"
                                         % (page, name, err))
        print("every table still evaluates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
