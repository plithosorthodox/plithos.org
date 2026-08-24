# -*- coding: utf-8 -*-
"""The Fathers come out of the Library page and become files, like the rest.

library.html carried the whole text of twenty-four works inside itself -
6.1 MB of Athanasius, Basil, Cyril, Gregory and the councils - while the
seventy-three works added since load one file each, on demand, through
machinery this page already has. Every reader was sent all of it whether he
opened a work or not, and again on every publication, because the page
revalidates and the site is stamped several times a day.

The page's own full-text search is the one thing that needed the text in
hand. It is not a box on this page: the Library lends its search to the
shared command palette. So the texts are fetched when a search is actually
made, and the palette is asked to draw again when they arrive. A reader who
only reads pays nothing for a search he never makes.

Two runs, and the order matters. A page pointed at a file the edge does not
have yet is answered with the whole of index.html and a 200.

    python3 tools/lift_library_core.py --files    # ship these, confirm them
    python3 tools/lift_library_core.py --point    # then turn the page over
"""
import io, json, os, re, sys

PAGE = "library.html"
OUT = os.path.join("data", "library")
HEAD = "const CORPUS = "


def corpus_span(src):
    i = src.index(HEAD)
    j = src.index("\n", i)
    return i + len(HEAD), j


def read_corpus(src):
    a, b = corpus_span(src)
    return json.loads(src[a:b].rstrip().rstrip(";"))


def write_files(src):
    c = read_corpus(src)
    by = {}
    for u in c["units"]:
        by.setdefault(u["work_id"], []).append(u)
    works = dict((w["work_id"], w) for w in c["works"])
    n = 0
    for wid, units in sorted(by.items()):
        path = os.path.join(OUT, wid + ".json")
        units.sort(key=lambda u: u.get("ordinal", 0))
        doc = {"work": works[wid], "units": units}
        io.open(path, "w", encoding="utf-8").write(
            json.dumps(doc, ensure_ascii=False, separators=(",", ":")))
        n += 1
        print("  %-42s %4d units  %6.1f KB"
              % (wid, len(units), os.path.getsize(path) / 1024.0))
    print("%d files written under %s" % (n, OUT))


LOADER = u'''
/* The twenty-four works whose text this page used to carry. They are files
   now, like the seventy-three added since, and the page fetches them when a
   search is made rather than sending six megabytes to every reader who never
   makes one. The palette is asked to draw again when they arrive. */
var CORE_WORKS = %s;
var coreTexts = null;
function ensureCoreTexts(){
  if(coreTexts) return coreTexts;
  coreTexts = Promise.all(CORE_WORKS.map(loadLibraryWork)).then(function(){
    try{
      var pi = document.getElementById("pl-input");
      if(pi && pi.value) pi.dispatchEvent(new Event("input",{bubbles:true}));
      else if(lastQuery) renderResults(lastQuery, search(lastQuery));
    }catch(e){}
  });
  return coreTexts;
}
'''

CALLS = [
 # the palette asks on every keystroke; the first one starts the fetch
 ('  search: function(query){\n    try{\n      return search(query)',
  '  search: function(query){\n    try{\n      ensureCoreTexts();\n      return search(query)'),
 ('  showAll: function(query){\n    try{ renderResults(query, search(query)); }catch(e){}',
  '  showAll: function(query){\n    try{ ensureCoreTexts(); renderResults(query, search(query)); }catch(e){}'),
]


def point(src):
    a, b = corpus_span(src)
    c = json.loads(src[a:b].rstrip().rstrip(";"))
    ids = sorted(set(u["work_id"] for u in c["units"]))
    if not ids:
        raise SystemExit("CORPUS.units is already empty")
    for w in c["works"]:
        if w["work_id"] in ids:
            w["lazy"] = True
    c["units"] = []
    src = (src[:a] + json.dumps(c, ensure_ascii=False, separators=(",", ":"))
           + ";" + src[b:])

    # the loader goes in after loadLibraryWork, which it calls
    anchor = "/* Four different things used to run together in one line"
    if "function ensureCoreTexts()" not in src:
        src = src.replace(anchor, LOADER % json.dumps(ids) + "\n" + anchor, 1)
    for old, new in CALLS:
        if new in src:
            continue
        if old not in src:
            raise SystemExit("search entry point not found: " + old[:50])
        src = src.replace(old, new, 1)

    # the #find= route, which renders results without the palette
    old = 'if(fq){ renderResults(fq, search(fq)); return; }'
    if old in src:
        src = src.replace(old, 'if(fq){ ensureCoreTexts(); renderResults(fq, search(fq)); return; }', 1)
    return src, len(ids)


def main():
    src = io.open(PAGE, encoding="utf-8").read()
    if "--files" in sys.argv:
        write_files(src)
    elif "--point" in sys.argv:
        before = len(src)
        out, n = point(src)
        io.open(PAGE, "w", encoding="utf-8").write(out)
        print("%s: %d works made lazy, %.2f MB -> %.2f MB"
              % (PAGE, n, before / 1048576.0, len(out) / 1048576.0))
    else:
        c = read_corpus(src)
        print("%d works, %d units inline; %.2f MB of text"
              % (len(c["works"]), len(c["units"]),
                 sum(len(u.get("text") or "") for u in c["units"]) / 1048576.0))


if __name__ == "__main__":
    main()
