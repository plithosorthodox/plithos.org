# -*- coding: utf-8 -*-
"""The calendar's engine, lifted whole so a second thing can run it.

The site is one page per subject and the calendar's reckoning lives inside
index.html: Pascha, the Julian offset, the menaion, the movable cycle, the
fast, the lectionary, and what each of the ten Churches adds or declines. An
embeddable panel and a JSON endpoint both need exactly that reckoning, and a
second copy of it written by hand would be wrong within a week.

So it is not written twice. This copies the tables and the functions OUT of
index.html, unchanged, into

    data/calendar-tables.v2.json      the tables, as JSON
    assets/plithos-calendar.v2.js     the functions, verbatim, in a closure

Nothing in the extracted code is edited. The functions read `lang`, `mode`,
`rite`, `juris` and `saintsScope` as free variables, exactly as they do in the
page; here they are `let` bindings in the enclosing scope, so the same code
means the same thing. That is the whole trick, and it is why this cannot
drift into disagreeing with the calendar.

tools/check_site.py regenerates and compares, so a change to the engine that
is not carried across fails before it ships.

    python3 tools/build_calendar_engine.py --check
    python3 tools/build_calendar_engine.py --write
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "index.html")
TABLES_OUT = os.path.join(ROOT, "data", "calendar-tables.v2.json")
NAMES_OUT = os.path.join(ROOT, "data", "calendar-names.v1.%s.json")
JS_OUT = os.path.join(ROOT, "assets", "plithos-calendar.v2.js")

TABLES = ["LUKE_SUN", "LUKE_TAIL", "GREAT_READINGS", "GREEK_GOSPEL", "WEPI", "WXMAS", "WPENT", "MATT_GO", "I18N", "FASTNOTE_I18N", "FAST", "JURISDICTIONS",
          "TWELVE_FIXED", "TWELVE_MOVABLE", "MAJOR_FIXED", "PASCHAL_NAMES",
          "PASCHAL_READINGS", "DAILY_LIT", "SYNAXARION", "MOVABLE_SYNAXARION",
          "LOCAL_FIXED", "LOCAL_MOVABLE", "LOCAL_CIVIL", "OMIT_FIXED",
          "AFTER_PENT_EP",
          "WFIX", "WOFF", "WADV", "WESTERN_FIXED", "WESTERN_MOVABLE"]

# copied verbatim, in this order; each is one whole declaration
CONSTS = ["SUN_AP", "DAY", "MN", "addDays", "fmtISO", "pad", "T", "Lmon", "t"]

FUNCS = ["westGreenSunday", "sundayAP", "juliOffset", "pascha", "fixedCivil", "nthWeekday", "lastWeekday",
         "adventSunday", "ordinal", "offsetFromPascha", "prevSun", "nextSun",
         "westSlot",
         "westReadingFor", "commemsWestern", "fastingWestern",
         "scopeKeys", "localsFrom", "dedupeLocal", "dedupeLocalMovable",
         "dedupeLocalCivil", "afterPentReading", "commemsFor", "fastingFor",
         "tn", "fnote", "dayData"]

HEAD = u"""/* The calendar's reckoning, copied out of index.html by
 * tools/build_calendar_engine.py. DO NOT EDIT. Edit the calendar and run the
 * tool; check_site.py fails if the two disagree.
 *
 * The functions below are the page's own, unchanged. They read lang, mode,
 * rite, juris and saintsScope as free variables; here those are bindings in
 * this closure, so the same code means the same thing it means in the page.
 */
export function calendar(TABLES, NAMES, NAMES_LANG){
  const {%s} = TABLES;
  /* One language's names, as the page's own table is shaped. tn() is the
     page's function, unchanged, and reads NAMES_I18N[name][lang]. */
  const NAMES_I18N = {};
  if (NAMES) { const L = NAMES_LANG || "en";
    for (const k in NAMES) { const o = {}; o[L] = NAMES[k]; NAMES_I18N[k] = o; } }

  let lang="en", mode="new", rite="byzantine", juris="greek",
      saintsScope="church", saintsPick=new Set(Object.keys(TABLES.JURISDICTIONS));

"""

TAIL = u"""
  /* The one thing written here rather than copied: the way in. */

  /* A word in the reader's language, English where his has none. The tables
     already carry every one of these; an earlier draft of this file simply
     did not ask for them, and answered an Arabic reader in English. */
  function say(group, key){
    const mine = TABLES.I18N[lang] && TABLES.I18N[lang][group];
    return (mine && mine[key]) || TABLES.I18N.en[group][key] || key;
  }

  /* A Church is named, not keyed. "greek" is how the calendar files it. */
  function churchName(k){
    const u = TABLES.I18N[lang] && TABLES.I18N[lang].ui;
    if (u && u["jz_" + k]) return u["jz_" + k];
    const e = TABLES.I18N.en.ui;
    if (e && e["jz_" + k]) return e["jz_" + k];
    return (TABLES.JURISDICTIONS[k] || {}).name || k;
  }

  return function day(iso, opts){
    opts = opts || {};
    const j = TABLES.JURISDICTIONS[opts.juris] ? opts.juris : "greek";
    juris = j;
    rite = TABLES.JURISDICTIONS[j].rite;
    mode = (opts.cal === "old" || opts.cal === "new") ? opts.cal
                                                      : TABLES.JURISDICTIONS[j].cal;
    lang = TABLES.I18N[opts.lang] ? opts.lang : "en";
    saintsScope = (opts.scope === "all") ? "all" : "church";
    const p = String(iso).split("-").map(Number);
    const d = new Date(p[0], p[1] - 1, p[2]);
    if (isNaN(d.getTime())) return null;
    const dd = dayData(d);
    const os = addDays(d, -juliOffset(d.getFullYear()));
    return {
      date: fmtISO(d),
      julian: fmtISO(os),
      jurisdiction: j,
      jurisdiction_name: churchName(j),
      calendar: mode,
      rite: rite,
      language: lang,
      day_name: dd.dayName || null,
      headline: dd.headline,
      great: !!dd.great,
      commemorations: dd.commems.map(function(c){
        return { name: tn(c.name), english: c.name, great: !!c.great,
                 local: !!c.local, church: c.j || null,
                 church_name: c.j ? churchName(c.j) : null };
      }),
      fast: { level: dd.fast.info.k, label: say("fast", dd.fast.info.k),
              english: dd.fast.info.label,
              note: dd.fast.note ? fnote(dd.fast.note) : "" },
      readings: dd.dayReading
        ? { epistle: dd.dayReading.ep || null, gospel: dd.dayReading.go || null,
            epistle_label: say("ui", "epistle"), gospel_label: say("ui", "gospel") }
        : null
    };
  };
}
"""


def app_start(src):
    """Where the page's own code begins.

    pako is inlined above it, minified, and its single line declares `T`, `t`
    and a dozen other single letters. Searching the whole file for `const T=`
    finds the deflate stream's state machine and not the calendar's language
    table, which is a mistake worth making only once."""
    m = src.index("pako inflate (from Nodeca project)")
    return src.index("\n", m) + 1


def read(src, name, kind, start=0):
    """One whole declaration, taken by balancing braces."""
    head = ("function %s(" % name) if kind == "fn" else ("const %s=" % name)
    i = src.find(head, start)
    if i < 0:
        raise SystemExit("%s %s: not found" % (kind, name))
    k = src.index("{", i) if kind == "fn" else i + len(head)
    if kind != "fn":
        # a const runs to the end of its line; the tables balance instead
        j = src.index("\n", i)
        return src[i:j].rstrip().rstrip(";")
    depth, instr, q, esc, line_c = 0, False, "", False, False
    while k < len(src):
        c = src[k]
        if line_c:
            if c == "\n":
                line_c = False
            k += 1
            continue
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == q:
                instr = False
            k += 1
            continue
        if c in "\"'`":
            instr, q = True, c
            k += 1
            continue
        if c == "/" and src[k + 1:k + 2] == "*":
            k = src.index("*/", k) + 2
            continue
        if c == "/" and src[k + 1:k + 2] == "/":
            line_c = True
            k += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
        k += 1
    raise SystemExit("%s: unbalanced" % name)


def table_span(src, name, start=0):
    head = "const %s=" % name
    i = src.index(head, start)
    k = i + len(head)
    while src[k] not in "{[":
        k += 1
    a, depth, instr, q, esc = k, 0, False, "", False
    while k < len(src):
        c = src[k]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == q:
                instr = False
            k += 1
            continue
        if c in "\"'`":
            instr, q = True, c
            k += 1
            continue
        if c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
            if depth == 0:
                return src[a:k + 1]
        k += 1
    raise SystemExit("%s: unbalanced table" % name)



def statements(src, prefix, start=0):
    """Every top-level `PREFIX...;` statement, whole.

    NAMES_I18N is declared with thirty-seven names and then filled by 1,491
    separate assignments spread over sixteen hundred lines. Taking only the
    declaration gave an engine that answered every feast in English however it
    was asked, which looked like a language bug and was a scraping bug."""
    out = []
    i = src.find(prefix, start)
    while i >= 0:
        k, depth, instr, q, esc = i, 0, False, "", False
        while k < len(src):
            c = src[k]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == q:
                    instr = False
            elif c in "\"'`":
                instr, q = True, c
            elif c in "{[(":
                depth += 1
            elif c in "}])":
                depth -= 1
            elif c == ";" and depth == 0:
                out.append(src[i:k + 1])
                break
            k += 1
        i = src.find(prefix, k + 1)
    return out


def build(write=False):
    src = io.open(PAGE, encoding="utf-8").read()
    at = app_start(src)

    # the tables, through node because several carry bare keys
    parts = ["const T={};"]
    for n in TABLES:
        parts.append("T[%s]=%s;" % (json.dumps(n), table_span(src, n, at)))
    # the names table is declared small and then filled by 1,491 assignments
    adds = statements(src, 'NAMES_I18N["', at)
    if len(adds) < 1000:
        raise SystemExit("only %d NAMES_I18N assignments found; the scrape is "
                         "wrong and every feast would answer in English" % len(adds))
    parts.append("T.NAMES_I18N=%s;" % table_span(src, "NAMES_I18N", at))
    parts.append("const NAMES_I18N=T.NAMES_I18N;")
    parts.extend(adds)
    parts.append("require('fs').writeFileSync(%s,JSON.stringify(T));"
                 % json.dumps(TABLES_OUT + ".all"))
    io.open("/tmp/mktables.js", "w", encoding="utf-8").write("\n".join(parts))
    subprocess.check_call(["node", "/tmp/mktables.js"])

    # The names are 1,528 feasts and saints in twenty-one languages, which is
    # 2.3 MB of the 2.7 and all but one language of it is dead weight to any
    # one reader. They go out one file per language, and the base keeps none.
    whole = json.load(io.open(TABLES_OUT + ".all", encoding="utf-8"))
    names = whole.pop("NAMES_I18N")
    langs = sorted(set(l for v in names.values() for l in v))
    made = dict((lang, dict((k, v[lang]) for k, v in names.items()
                            if v.get(lang))) for lang in langs)
    os.remove(TABLES_OUT + ".all")

    # A check must not touch the tree. This wrote all twenty-two data files
    # whether or not --write was given, so every run of check_site.py left
    # twenty-one modified files behind and a worker then had either to commit
    # the churn or to restore them by hand; both happened. What differed was
    # only the order the keys came out in, so the comparison is of the parsed
    # content and a reordering is not a failure.
    if not write:
        stale = [p for p, want in
                 [(NAMES_OUT % lang, made[lang]) for lang in langs]
                 + [(TABLES_OUT, whole)]
                 if not os.path.exists(p)
                 or json.load(io.open(p, encoding="utf-8")) != want]
        if stale:
            print("  %d of the calendar's data files no longer match "
                  "index.html; run --write" % len(stale))
            return None
        print("  %d names in %d languages, every file current"
              % (len(names), len(langs)))
    else:
        for lang in langs:
            io.open(NAMES_OUT % lang, "w", encoding="utf-8").write(
                json.dumps(made[lang], ensure_ascii=False,
                           separators=(",", ":")))
        io.open(TABLES_OUT, "w", encoding="utf-8").write(
            json.dumps(whole, ensure_ascii=False, separators=(",", ":")))
        print("  %d names in %d languages, one file each"
              % (len(names), len(langs)))

    body = []
    for n in CONSTS:
        body.append("  " + read(src, n, "const", at) + ";")
    for n in FUNCS:
        body.append("  " + read(src, n, "fn", at))
    js = (HEAD % ", ".join(TABLES)) + "\n".join(body) + TAIL
    return js


def main():
    write = "--write" in sys.argv
    js = build(write)
    if js is None:
        return 1
    old = io.open(JS_OUT, encoding="utf-8").read() if os.path.exists(JS_OUT) else None
    if write:
        io.open(JS_OUT, "w", encoding="utf-8").write(js)
        print("wrote %s (%.0f KB) and %s (%.0f KB)"
              % (os.path.relpath(JS_OUT, ROOT), len(js) / 1024.0,
                 os.path.relpath(TABLES_OUT, ROOT),
                 os.path.getsize(TABLES_OUT) / 1024.0))
    elif old is None:
        print("%s does not exist yet" % os.path.relpath(JS_OUT, ROOT))
        return 1
    elif old != js:
        print("%s no longer matches index.html; run --write"
              % os.path.relpath(JS_OUT, ROOT))
        return 1
    else:
        print("the engine matches the calendar (%d tables, %d functions)"
              % (len(TABLES), len(FUNCS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
