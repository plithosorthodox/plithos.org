# -*- coding: utf-8 -*-
"""The Old Testament the Western rite reads, which the page was throwing away.

When the English Bible was lifted out of index.html it went to
data/bible-en.v1.json - Psalms and the New Testament, twenty-eight books. The
eighteen Old Testament books the Western-rite lectionary cites stayed behind
as five statements that run at parse time:

    Object.assign(BIBLE,{"1 Kings":...,"Genesis":...,...})
    Object.assign(BIBLE,{"Judith":...})
    BIBLE.Daniel[2]  = ...        (the Three Holy Children)
    BIBLE.Daniel[12] = ...        (Susanna)
    BIBLE.Daniel[13] = ...        (Bel and the Dragon)

and loadBibleEn ends with `BIBLE=d`, which REPLACES the object. So the
eighteen books existed for as long as the fetch took and were then dropped.
Measured in a browser with the fetch held back:

    as parsed        Isa. 7:10-15 -> 6 verses, Dan. 3:47-51 -> 5, Prov. 8:22-35 -> 14
    after the fetch  all three unparsed

Which is to say every Old Testament reading in the Western-rite lectionary
has been dead on the site: no text, and not even a link, because vlink asks
pericope whether the passage is there before it makes one.

So the eighteen books join the file - bible-en.v2.json, because v1 is served
immutable for a year and must never be edited - the five statements go, and
loadBibleEn merges instead of replacing, so that the next thing written
beside it is not silently discarded too.

    python3 tools/lift_bible_ot.py --file     # ship it, confirm it
    python3 tools/lift_bible_ot.py --point    # then turn the page over
"""
import io, json, os, subprocess, sys

PAGE = "index.html"
SRC_FILE = os.path.join("data", "bible-en.v1.json")
OUT = os.path.join("data", "bible-en.v2.json")

STARTS = ("Object.assign(BIBLE,{", "BIBLE.Daniel[")


def inline_lines(src):
    return [l for l in src.split("\n") if l.startswith(STARTS)]


def build(src):
    lines = inline_lines(src)
    if not lines:
        raise SystemExit("the inline Old Testament is already gone")
    js = ("var BIBLE={};\n" + "\n".join(lines) +
          "\nvar have=JSON.parse(require('fs').readFileSync(%s,'utf8'));\n"
          "Object.assign(BIBLE,have);\n"
          "require('fs').writeFileSync(%s,JSON.stringify(BIBLE));\n"
          % (json.dumps(SRC_FILE), json.dumps(OUT)))
    io.open("/tmp/mkbible.js", "w", encoding="utf-8").write(js)
    subprocess.check_call(["node", "/tmp/mkbible.js"])
    out = json.load(io.open(OUT, encoding="utf-8"))
    was = json.load(io.open(SRC_FILE, encoding="utf-8"))
    added = sorted(set(out) - set(was))
    print("%s: %d books (%d were in v1, %d added), %.0f KB"
          % (OUT, len(out), len(was), len(added), os.path.getsize(OUT) / 1024.0))
    print("  added: %s" % ", ".join(added))
    d = out.get("Daniel") or []
    print("  Daniel: %d chapters, of which 3, 13 and 14 present: %s"
          % (len(d), all(d[i - 1] for i in (3, 13, 14) if i <= len(d))))


SUBS = [
 ('fetch("data/bible-en.v1.json")', 'fetch("data/bible-en.v2.json")'),
 # merge, do not replace: the next thing written beside this must survive
 ('if(d){BIBLE=d;BIBLE_READY=true;}',
  'if(d){Object.assign(BIBLE,d);BIBLE_READY=true;}'),
]


def point(src):
    if not os.path.exists(OUT):
        raise SystemExit("%s is not there; run --file first" % OUT)
    have = json.load(io.open(OUT, encoding="utf-8"))
    lines = src.split("\n")
    keep, dropped = [], 0
    for l in lines:
        if l.startswith(STARTS):
            dropped += 1
            continue
        keep.append(l)
    if not dropped:
        raise SystemExit("the inline Old Testament is already gone")
    src = "\n".join(keep)
    for old, new in SUBS:
        if new in src:
            continue
        if old not in src:
            raise SystemExit("not found: " + old[:60])
        src = src.replace(old, new, 1)
    return src, dropped, len(have)


def main():
    src = io.open(PAGE, encoding="utf-8").read()
    if "--file" in sys.argv:
        build(src)
    elif "--point" in sys.argv:
        before = len(src)
        out, dropped, books = point(src)
        io.open(PAGE, "w", encoding="utf-8").write(out)
        print("%s: %d statements removed, %d books read from the file, "
              "%.2f MB -> %.2f MB"
              % (PAGE, dropped, books, before / 1048576.0, len(out) / 1048576.0))
    else:
        n = sum(len(l) for l in inline_lines(src))
        print("%d inline statements, %.0f KB" % (len(inline_lines(src)), n / 1024.0))


if __name__ == "__main__":
    main()
