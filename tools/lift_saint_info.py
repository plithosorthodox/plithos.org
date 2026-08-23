#!/usr/bin/env python3
"""Take the calendar entries out of the calendar page.

    python3 tools/lift_saint_info.py --files      writes data/saint-info.v1.*.json
    python3 tools/lift_saint_info.py --page       points index.html at them

index.html is 16.2 MB on the disk and 4.57 MB over the wire, and SAINT_INFO_I18N
is two thirds of it: the day-panel entries for every saint in every language,
handed to every reader whatever language he is in. A reader in English is sent
the Georgian and the Arabic and the Serbian and reads none of it.

Only one language is ever looked at. The lookup is
SAINT_INFO_I18N[lang][name], and the one other place that touches the table is
buildSIndex, which builds the search haystack once and lazily. So the entries
are fetched for the language in front of the reader, the way the saints' lives
and the vocabulary already are, and the search index is thrown away when a new
language arrives so that it is built again with it.

What is lost, and it is worth writing down: a search for words in the body of
an entry in a language the reader has not loaded will no longer match. Saints'
names still match in every language, because those come from their own file,
and the whole-site search index is a separate thing and unaffected.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
OUT = ROOT / "data"
VERSION = "v1"
MARK = "SAINT_INFO_I18N="


def table():
    s = io.open(PAGE, encoding="utf-8").read()
    i = s.index(MARK)
    j = s.index("\n", i)
    return s, i, j, json.loads(s[i + len(MARK):j].rstrip(";"))


def files(write):
    _s, _i, _j, d = table()
    total = 0
    for lang in sorted(d):
        blob = json.dumps(d[lang], ensure_ascii=False, separators=(",", ":"))
        total += len(blob.encode("utf-8"))
        p = OUT / ("saint-info.%s.%s.json" % (VERSION, lang))
        print("  %-4s %5d entries  %7.1f KB  %s"
              % (lang, len(d[lang]), len(blob.encode("utf-8")) / 1024.0,
                 p.name if write else "(would write)"))
        if write:
            p.write_text(blob, encoding="utf-8")
    print("\n%d languages, %.2f MB lifted out of the page"
          % (len(d), total / 1048576.0))
    return sorted(d)


LOADER = '''
/* The day-panel entries, fetched for the language in front of the reader.
   They were inlined here for every language at once - two thirds of this
   page - and only one is ever read. The list is checked against the files
   before every publication so it cannot go stale, and the content type is
   checked as well as r.ok because Pages answers a path that does not exist
   with the whole of this page and a 200. */
var SAINT_INFO_LANGS=%s;
var SAINT_INFO_I18N={},_siPending={};
function loadSaintInfo(L,cb){
  if(!L||L==="en"||SAINT_INFO_I18N[L]||!SAINT_INFO_LANGS[L]){if(cb)cb();return;}
  if(_siPending[L]){if(cb)cb();return;}
  _siPending[L]=1;
  fetch("data/saint-info.%s."+L+".json")
    .then(function(r){
      var ct=(r.headers.get("content-type")||"").toLowerCase();
      if(!r.ok||ct.indexOf("json")<0)return null;
      return r.json();
    })
    .then(function(d){
      if(d){SAINT_INFO_I18N[L]=d;_sidx=null;}
      if(cb)cb();
    },function(){if(cb)cb();});
}
'''


def page(write, langs):
    s, i, j, _d = table()
    listed = "{" + ",".join("%s:1" % l for l in langs) + "}"
    block = LOADER % (listed, VERSION)
    s2 = s[:i] + block.strip() + s[j:]
    # the assignment line is replaced entirely; nothing else on it
    s2 = s2.replace(MARK, "", 1) if s2.count(MARK) > 1 else s2
    if s2 == s:
        print("  nothing changed")
        return
    print("  index.html %.2f MB -> %.2f MB"
          % (len(s) / 1048576.0, len(s2) / 1048576.0))
    if write:
        io.open(PAGE, "w", encoding="utf-8").write(s2)
        print("  wrote index.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", action="store_true")
    ap.add_argument("--page", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    langs = files(a.write and a.files)
    if a.page:
        page(a.write, langs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
