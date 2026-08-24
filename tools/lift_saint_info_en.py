# -*- coding: utf-8 -*-
"""The English day-panel entries come out of the calendar.

index.html is 4.12 MB and 811 KB of it is SAINT_INFO - a quarter of the page,
and the single largest thing left in it. Twenty-one languages already read
theirs from data/saint-info.v1.<lang>.json, fetched at boot and painted when
it arrives; English was the exception only because it was the language the
page was written in.

It is more than a saving. SAINT_INFO was also the key set: siTr returned
nothing for a name that was not in it, so the English table had to be present
for a Russian reader to see anything at all. English becomes an entry in
SAINT_INFO_I18N like the others and is fetched alongside the reader's own
language, both painting as they arrive.

    python3 tools/lift_saint_info_en.py --file     # ship it, confirm it
    python3 tools/lift_saint_info_en.py --point    # then turn the page over
"""
import io, json, os, sys

PAGE = "index.html"
OUT = os.path.join("data", "saint-info.v1.en.json")
HEAD = "const SAINT_INFO="


def span(src):
    i = src.index(HEAD)
    j = src.index("\n", i)
    return i + len(HEAD), j


def write_file(src):
    a, b = span(src)
    info = json.loads(src[a:b].rstrip().rstrip(";"))
    if not info:
        raise SystemExit("SAINT_INFO is already empty")
    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(info, ensure_ascii=False, separators=(",", ":")))
    print("%s: %d entries, %.2f MB"
          % (OUT, len(info), os.path.getsize(OUT) / 1048576.0))


SUBS = [
 # English is fetched like the rest
 ('if(!L||L==="en"||SAINT_INFO_I18N[L]||!SAINT_INFO_LANGS[L]){if(cb)cb();return;}',
  'if(!L||SAINT_INFO_I18N[L]||!SAINT_INFO_LANGS[L]){if(cb)cb();return;}'),
 # and is the base the others fall back to, from wherever it has got to
 ('function siTr(name){const b=SAINT_INFO[name];if(!b)return null;',
  'function siTr(name){const b=(SAINT_INFO_I18N.en&&SAINT_INFO_I18N.en[name])||SAINT_INFO[name];if(!b)return null;'),
 ('const si=SAINT_INFO[nm];',
  'const si=(SAINT_INFO_I18N.en&&SAINT_INFO_I18N.en[nm])||SAINT_INFO[nm];'),
 # both files are asked for at once, and each paints when it lands
 ('warmBibleLang(); loadBibleEn(renderAll); loadSaintInfo(lang,renderAll);',
  'warmBibleLang(); loadBibleEn(renderAll); loadSaintInfo("en",renderAll); loadSaintInfo(lang,renderAll);'),
]


def point(src):
    if not os.path.exists(OUT):
        raise SystemExit("%s is not there; run --file first" % OUT)
    a, b = span(src)
    info = json.loads(src[a:b].rstrip().rstrip(";"))
    have = json.load(io.open(OUT, encoding="utf-8"))
    missing = [k for k in info if k not in have]
    if missing:
        raise SystemExit("%d entries are in the page but not in the file: %s"
                         % (len(missing), ", ".join(missing[:3])))
    src = src[:a] + "{}" + ";" + src[b:]
    for old, new in SUBS:
        if new in src:
            continue
        if old not in src:
            raise SystemExit("not found: " + old[:70])
        src = src.replace(old, new, 1)
    return src, len(info)


def main():
    src = io.open(PAGE, encoding="utf-8").read()
    if "--file" in sys.argv:
        write_file(src)
    elif "--point" in sys.argv:
        before = len(src)
        out, n = point(src)
        io.open(PAGE, "w", encoding="utf-8").write(out)
        print("%s: %d entries moved out, %.2f MB -> %.2f MB"
              % (PAGE, n, before / 1048576.0, len(out) / 1048576.0))
    else:
        a, b = span(src)
        print("%d bytes of SAINT_INFO in the page" % (b - a))


if __name__ == "__main__":
    main()
