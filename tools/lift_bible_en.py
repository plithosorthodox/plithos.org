#!/usr/bin/env python3
"""Take the English New Testament out of the calendar page.

    python3 tools/lift_bible_en.py --files --write
    python3 tools/lift_bible_en.py --page --write

BIBLE is the King James New Testament, inlined so that a reading's reference
can be resolved to its verses. It is 1.14 million characters of a page that is
now 4.25 million, and a reader who never opens a reading never needs a word of
it. Every other language's scripture is already fetched on demand; only
English was in the page.

Three things touch it and each is handled:

  pericope() reads BIBLE[book] and would throw on a book that is not there.
  It returns nothing instead, which is what it already does for a reference
  that does not resolve.

  vlink() decides whether a reference is worth making clickable by resolving
  it first. Before the text has arrived it cannot, so it makes the reference
  clickable if it parses at all. The references in the calendar come from the
  lectionary and do resolve; the cost of being wrong is a link that opens an
  empty panel, and the cost of the alternative is every reading in the
  calendar rendering as dead text for as long as the fetch takes.

  showVerses() is opened by the reader, so it fetches first and shows itself
  again when the text lands - the same thing it already does for the other
  twenty-two languages.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
OUT = ROOT / "data" / "bible-en.v1.json"
MARK = "BIBLE="


def table():
    s = io.open(PAGE, encoding="utf-8").read()
    m = re.search(r"\n(?:const|var|let)\s+BIBLE\s*=", s)
    i = m.start() + 1
    k = s.index("=", m.start()) + 1
    j = s.index("\n", k)
    return s, i, j, json.loads(s[k:j].rstrip(";"))


def files(write):
    _s, _i, _j, d = table()
    blob = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    print("  %d books, %.2f MB" % (len(d), len(blob.encode("utf-8")) / 1048576.0))
    if write:
        OUT.write_text(blob, encoding="utf-8")
        print("  wrote %s" % OUT.name)


LOADER = '''/* The King James New Testament, fetched rather than inlined. It was 1.14
   million characters of this page and a reader who never opens a reading
   never needs a word of it; every other language's scripture already loads
   this way. The content type is checked as well as r.ok, because Pages
   answers a path that does not exist with the whole of this page and a 200. */
var BIBLE={},BIBLE_READY=false,_bibEnPending=false;
function loadBibleEn(cb){
  if(BIBLE_READY){if(cb)cb();return;}
  if(_bibEnPending){return;}
  _bibEnPending=true;
  fetch("data/bible-en.v1.json")
    .then(function(r){
      var ct=(r.headers.get("content-type")||"").toLowerCase();
      if(!r.ok||ct.indexOf("json")<0)return null;
      return r.json();
    })
    .then(function(d){
      _bibEnPending=false;
      if(d){BIBLE=d;BIBLE_READY=true;}
      if(cb)cb();
    },function(){_bibEnPending=false;if(cb)cb();});
}'''


def page(write):
    s, i, j, _d = table()
    out = s[:i] + LOADER + s[j:]

    # pericope must not throw on a book that has not arrived
    old = "function pericope(book,ranges){\n  const B=BIBLE[book],out=[];"
    if old not in out:
        old = re.search(r"function pericope\(book,ranges\)\{\s*const B=BIBLE\[book\],out=\[\];",
                        out).group(0)
    out = out.replace(old, old.replace(
        "const B=BIBLE[book],out=[];",
        "const B=BIBLE[book],out=[];if(!B)return out;"), 1)

    # a reference that parses is clickable even before the text is here
    vold = "const _ok=_p&&pericope(_p.book,_p.ranges).length;"
    assert vold in out, "vlink not found"
    out = out.replace(
        vold,
        "const _ok=_p&&(!BIBLE_READY||pericope(_p.book,_p.ranges).length);", 1)

    # opening a reading fetches the text and shows itself again
    sold = "function showVerses(ref){\n  lastRef=ref;"
    if sold not in out:
        sold = re.search(r"function showVerses\(ref\)\{\s*lastRef=ref;", out).group(0)
    out = out.replace(sold, sold + "\n  if(!BIBLE_READY){loadBibleEn(function(){showVerses(ref);});}", 1)

    # and it is warmed when the reader is idle, beside the other two
    boot = "warmBibleLang();"
    assert boot in out
    out = out.replace(boot, boot + " loadBibleEn(renderAll);", 1)

    print("  index.html %.2f M -> %.2f M chars"
          % (len(s) / 1048576.0, len(out) / 1048576.0))
    if write:
        io.open(PAGE, "w", encoding="utf-8").write(out)
        print("  wrote index.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", action="store_true")
    ap.add_argument("--page", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    if a.files:
        files(a.write)
    if a.page:
        page(a.write)
    return 0


if __name__ == "__main__":
    sys.exit(main())
