#!/usr/bin/env python3
"""
Every word a reader can see, in every language, on every page.

The saints' lives and the calendar entries are counted by their own tools.
Nothing counted the rest: the buttons, the column headings, the placeholder
in a search box, the notice a panel shows only when it has nothing to show.
Those live in a different table on every page - I18N on the calendar, SUI on
the Saints index, RLEX in the Library, T on the small pages, a block inside a
file under /data for the rule and the glossary - and a language missing from
one of them meets that page in English however complete its saints are.

Two questions are asked, and the second is the one no per-table count
answers on its own:

  1. Of the strings a surface declares in English, how many does each
     language actually carry?
  2. Which strings does a page put on the screen without asking any table?
     A hard-coded string cannot be reported missing from a translation,
     because there is no translation for it to be missing from. It is
     English in all twenty-two languages and nothing flags it.

Tables are found by walking the page for object literals and are read by
evaluating them in node, not by converting JavaScript to JSON with a
substitution: that broke on the first apostrophe inside a string, and a
table that fails to parse silently reports as complete, which is the one
failure this must not have. Shape is detected rather than declared - a table
may be {lang:{key:text}} or {key:{lang:text}}, and both are in use here.

    python3 tools/check_i18n.py
    python3 tools/check_i18n.py --surface RLEX
    python3 tools/check_i18n.py --hardcoded
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = "en el ru ro uk de es ar fr pt it sr ka zh ja ko sw hy arc hi bn ur".split()
LANGSET = set(LANGS)

PAGES = ["index.html", "saints.html", "library.html", "prayers.html",
         "rule.html", "glossary.html", "contact.html"]

# Tables that hold prose the reader never sees as interface, or data the
# language picker itself needs in every language by design.
SKIP = {"CORPUS", "LIT_ALIGN", "NAMES_I18N", "SAINT_INFO_I18N", "PRAYERS",
        "SAINT_INFO", "LIBRARY_STATE", "BIBLE_CACHE"}


def literals(src):
    """Every `NAME = {...}` in the source, balanced over braces and strings."""
    for m in re.finditer(r'(?:const|var|let)\s+([A-Za-z_$][\w$]*)\s*=\s*\{', src):
        name = m.group(1)
        i = m.end() - 1
        depth = 0
        quote = None
        esc = False
        for j in range(i, len(src)):
            c = src[j]
            if quote:
                if esc:
                    esc = False
                elif c == '\\':
                    esc = True
                elif c == quote:
                    quote = None
                continue
            if c in '"\'`':
                quote = c
            elif c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    yield name, src[i:j + 1]
                    break


def evaluate(lit):
    # via a file, not -e: KEY_I18N is 142 KB and argv has a limit
    prog = "const O=" + lit + ";process.stdout.write(JSON.stringify(O));"
    tmp = None
    try:
        # The system temp directory, not tools/. The finally below removes
        # this file on any ordinary exit, but a killed process - a container
        # restart, a timeout on the command that called this - never reaches
        # a finally, and the leftover then sits in the repository as an
        # untracked file that looks like work somebody forgot to commit.
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         suffix=".i18n-eval.js",
                                         delete=False) as f:
            f.write(prog)
            tmp = Path(f.name)
        r = subprocess.run(["node", str(tmp)], capture_output=True,
                           timeout=180, text=True, encoding="utf-8")
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, "node did not run (%s)" % e
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        return None, (r.stderr.strip().split("\n") or [""])[-1][:120]
    try:
        return json.loads(r.stdout), None
    except ValueError as e:
        return None, str(e)[:120]


def shape(obj):
    """by_lang if the top keys are language codes; by_key if the values' are."""
    if not isinstance(obj, dict) or not obj:
        return None
    top = [k for k in obj if isinstance(k, str)]
    hits = LANGSET & set(top)
    # A table holding ONLY English is the very defect this looks for, so one
    # language code is enough to call it language-keyed when every key is one.
    if hits and (len(hits) == len(top) or len(hits) >= max(3, len(top) * 0.5)):
        return "by_lang"
    inner = set()
    for v in list(obj.values())[:40]:
        if isinstance(v, dict):
            inner |= set(v)
    if inner and len(LANGSET & inner) >= max(3, len(inner) * 0.5):
        return "by_key"
    return None


def leaves(d, prefix=""):
    got = set()
    if not isinstance(d, dict):
        return got
    for k, v in d.items():
        kk = prefix + "." + k if prefix else k
        if isinstance(v, dict):
            got |= leaves(v, kk)
        elif isinstance(v, str):
            if v.strip():
                got.add(kk)
        elif v is not None:
            got.add(kk)
    return got


def as_by_lang(obj, sh):
    if sh == "by_lang":
        return obj
    out = {}
    for key, per in obj.items():
        if isinstance(per, dict):
            for l, v in per.items():
                out.setdefault(l, {})[key] = v
    return out


def surfaces():
    """(where, name, {lang: {key: text}}) for every translated surface."""
    found = []
    for page in PAGES:
        src = (ROOT / page).read_text(encoding="utf-8")
        for name, lit in literals(src):
            if name in SKIP or len(lit) > 4_000_000:
                continue
            if not (LANGSET & set(re.findall(r'[{,]\s*"?([a-z]{2,3})"?\s*:', lit[:400000]))):
                continue
            obj, err = evaluate(lit)
            if obj is None:
                found.append((page, name, None, err))
                continue
            sh = shape(obj)
            if sh is None:
                continue
            found.append((page, name, as_by_lang(obj, sh), None))

    # the shared command palette, on all seven pages
    en = json.loads((ROOT / "data/ui-i18n.v5.en.json").read_text(encoding="utf-8"))
    table = {"en": en}
    for l in LANGS:
        p = ROOT / ("data/ui-i18n.v5.%s.json" % l)
        if p.exists():
            table[l] = json.loads(p.read_text(encoding="utf-8"))
    found.append(("assets/plithos-ui.js", "ui-i18n.v5", table, None))

    # the fasting rule: English is the markup, the rest is one file a language
    rsrc = (ROOT / "rule.html").read_text(encoding="utf-8")
    keys = sorted(set(re.findall(r'data-t="([^"]+)"', rsrc)))
    table = {"en": {k: "x" for k in keys}}
    for l in LANGS:
        p = ROOT / ("data/rule-i18n.v5.%s.json" % l)
        if p.exists():
            table[l] = json.loads(p.read_text(encoding="utf-8"))
    found.append(("rule.html", "rule-i18n.v5", table, None))

    # the glossary's own chrome, its tag names and its language names
    g = json.loads((ROOT / "data/glossary.v4.json").read_text(encoding="utf-8"))
    for blk in ("ui", "tagNames", "lgNames"):
        if blk in g:
            sh = shape(g[blk])
            if sh:
                found.append(("glossary.html", "glossary.v4:" + blk,
                              as_by_lang(g[blk], sh), None))
    return found


PROSE = re.compile(r'^[A-Z(“][^<>{}]*[A-Za-z)”.!?]$')


def englishy(v):
    return (isinstance(v, str) and len(v) > 3
            and len(re.findall(r'[A-Za-z]{3,}', v)) >= 2
            and PROSE.match(v.strip()))


def no_language_dimension():
    """Reader-facing English constants that no language can override.

    These never appear as a missing translation, because there is no
    language axis for them to be missing from. They are English in all
    twenty-two, permanently, and only a check like this one finds them."""
    out = {}
    for page in PAGES:
        src = (ROOT / page).read_text(encoding="utf-8")
        rows = []
        for name, lit in literals(src):
            if name in SKIP or len(lit) > 2_000_000:
                continue
            obj, err = evaluate(lit)
            if obj is None or shape(obj):
                continue
            vals = [v for v in obj.values() if englishy(v)]
            if vals and len(vals) >= max(1, len(obj) * 0.5):
                rows.append((name, len(obj), vals[:2]))
        for m in re.finditer(r'(?:const|var|let)\s+([A-Z_][A-Z_0-9]*)\s*=\s*\[', src):
            nm = m.group(1)
            i = m.end() - 1
            d = 0
            q = None
            esc = False
            end = None
            for j in range(i, min(len(src), i + 200000)):
                c = src[j]
                if q:
                    if esc:
                        esc = False
                    elif c == '\\':
                        esc = True
                    elif c == q:
                        q = None
                    continue
                if c in '"\'`':
                    q = c
                elif c == '[':
                    d += 1
                elif c == ']':
                    d -= 1
                    if d == 0:
                        end = j + 1
                        break
            if end is None:
                continue
            try:
                arr = json.loads(re.sub(r',\s*\]', ']', src[i:end]))
            except Exception:
                continue
            vals = [v for v in arr if englishy(v)]
            if vals and len(vals) >= max(1, len(arr) * 0.6):
                rows.append((nm, len(arr), vals[:2]))
        if rows:
            out[page] = rows
    return out


# A JS string key read back out of the page. `s.encode().decode("unicode_escape")`
# is the obvious way to undo the escapes and is wrong the moment a key is not
# ASCII: it re-reads the UTF-8 bytes one to a character, so an em dash comes
# back as three. Seventy-six commemorations carry one - PASCHA, Clean Monday,
# every name printed with curly quotes - and each was reported as untranslated
# long after it had been written, and appended a second time on every install.
def unesc(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})|\\(.)',
                  lambda m: chr(int(m.group(1), 16)) if m.group(1) else m.group(2), s)


def untranslated_names():
    """Commemoration names the calendar shows through tn(), which falls back
    to English without saying so, and for which NAMES_I18N has no entry."""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    have = {unesc(h)
            for h in re.findall(r'NAMES_I18N\[(?:"((?:[^"\\]|\\.)*)")\]\s*=', src)}
    lits = {n: l for n, l in literals(src)}
    out = []
    for var in ("TWELVE_MOVABLE", "PASCHAL_NAMES", "WESTERN_MOVABLE",
                "MOVABLE_SYNAXARION", "SYNAXARION"):
        if var not in lits:
            continue
        obj, err = evaluate(lits[var])
        if obj is None:
            continue
        names = []

        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in ("name", "n") and isinstance(v, str):
                        names.append(v)
                    elif k not in ("ep", "go", "e", "g"):
                        # the epistle and the gospel of a feast; a reference,
                        # not a name, and rendered by the books of the Bible
                        walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
            elif isinstance(x, str):
                names.append(x)
        walk(obj)
        names = [n for n in names if englishy(n) or " " in n]
        miss = [n for n in names if n not in have]
        if miss:
            out.append((var, len(names), miss))
    return out


EMIT = re.compile(
    r'\.(?:textContent|innerHTML|innerText|title|placeholder|value|label|ariaLabel)\s*[+]?=\s*'
    r'|\.setAttribute\(\s*["\'](?:title|placeholder|aria-label|alt)["\']\s*,\s*'
    r'|\b(?:alert|confirm|prompt)\s*\(')
WORDS = re.compile(r'[A-Za-z]{3,}')


def hardcoded():
    out = {}
    for page in PAGES:
        src = (ROOT / page).read_text(encoding="utf-8")
        hits = []
        for m in EMIT.finditer(src):
            sm = re.match(r'\s*(["\'])((?:\\.|(?!\1).){0,240})\1',
                          src[m.end():m.end() + 320])
            if not sm:
                continue
            s = sm.group(2).strip()
            if not s or s.startswith("<") or "${" in s or "'+" in s:
                continue
            words = WORDS.findall(s)
            if len(words) < 2:
                continue
            if re.fullmatch(r'[a-z][\w-]*(?:[ -][a-z][\w-]*)*', s):
                continue          # a class list or an identifier
            hits.append((src.count("\n", 0, m.start()) + 1, s[:100]))
        if hits:
            out[page] = hits
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface")
    ap.add_argument("--hardcoded", action="store_true")
    args = ap.parse_args()
    problems = 0

    if not args.hardcoded:
        print("Interface strings: what each language carries of what English declares\n")
        print("%-22s %-18s %7s  %s" % ("page", "surface", "strings", "languages"))
        for page, name, table, err in surfaces():
            if args.surface and args.surface not in name:
                continue
            if table is None:
                print("%-22s %-18s   %s" % (page, name, "WOULD NOT EVALUATE: " + err))
                problems += 1
                continue
            en = leaves(table.get("en", {}))
            if not en:
                continue
            absent, partial = [], {}
            for l in LANGS:
                if l == "en":
                    continue
                if l not in table:
                    absent.append(l)
                else:
                    miss = sorted(en - leaves(table[l]))
                    if miss:
                        partial[l] = miss
            ok = len(LANGS) - len(absent) - len(partial)
            flag = "" if ok == len(LANGS) else "   <-- gap"
            print("%-22s %-18s %7d  %2d of %d%s"
                  % (page, name, len(en), ok, len(LANGS), flag))
            if absent:
                print("%42s no table at all: %s" % ("", " ".join(absent)))
                problems += 1
            for l, miss in sorted(partial.items()):
                print("%42s %-4s missing %d: %s"
                      % ("", l, len(miss), ", ".join(miss[:8])))
                problems += 1
        print()

    print("Reader-facing English with no language dimension at all\n")
    for page, rows in sorted(no_language_dimension().items()):
        print("%-22s" % page)
        for nm, n, sample in rows:
            print("%24s %-20s %4d entries   e.g. %s"
                  % ("", nm, n, "; ".join(repr(x)[:40] for x in sample)))
            problems += n
    print()

    print("Commemoration names with no translation entry (tn() shows English)\n")
    for var, total, miss in untranslated_names():
        print("%-22s %4d names, %4d have none: %s"
              % (var, total, len(miss), "; ".join(miss[:2])[:90]))
        problems += len(miss)
    print()

    print("Strings assigned straight to the DOM with no translation behind them\n")
    hc = hardcoded()
    if not hc:
        print("   none found")
    for page, hits in sorted(hc.items()):
        print("%-22s %d" % (page, len(hits)))
        for line, s in hits[:15]:
            print("%24s :%-6d %r" % ("", line, s))
        if len(hits) > 15:
            print("%24s ... and %d more" % ("", len(hits) - 15))
        problems += len(hits)

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
