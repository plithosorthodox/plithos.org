# -*- coding: utf-8 -*-
"""The English lives come out of the Saints page.

saints.html is 3.55 MB and 2.17 MB of it is the life text - seventy-three per
cent of the page - sent to every reader whether he opens a life or not, and
again on every publication, because the page revalidates and the site is
stamped several times a day.

Eleven other languages already do this properly: the lives are one file to a
language under data/, fetched the first time a reader opens a life. English
was the exception only because it was the language the page was written in.
It becomes data/saint-lives.v6.en.json like the rest, and the page keeps the
names, dates, ranks and every filterable field, which is what the index is
for.

The builder that publishes the other languages reads English from this page
to fill in a life that has not been translated yet, so it is taught to read
the file instead; and tools/add_saints.py writes a new saint's life there
rather than into the page.

Two runs, and the order matters. A page pointed at a file the edge does not
have yet is answered with the whole of index.html and a 200.

    python3 tools/lift_saint_lives_en.py --file     # ship it, confirm it
    python3 tools/lift_saint_lives_en.py --point    # then turn the page over
"""
import io, json, os, sys

PAGE = "saints.html"
OUT = os.path.join("data", "saint-lives.v6.en.json")
HEAD = "const SAINTS="


def span(src):
    i = src.index(HEAD)
    j = src.index("\n", i)
    return i + len(HEAD), j


def read(src):
    a, b = span(src)
    return json.loads(src[a:b].rstrip().rstrip(";"))


def write_file(src):
    saints = read(src)
    lives = dict((s["name"], s.get("life") or "") for s in saints)
    written = sum(1 for v in lives.values() if v.strip())
    io.open(OUT, "w", encoding="utf-8").write(
        json.dumps(lives, ensure_ascii=False, separators=(",", ":")))
    print("%s: %d names, %d with a life, %.2f MB"
          % (OUT, len(lives), written, os.path.getsize(OUT) / 1048576.0))


SUBS = [
 # English is a language like the others now, so it is fetched like the others
 ('var SLIVES=null, SLIVES_WANT=(SLANG==="en"||!LIVES_LANGS[SLANG]?null:SLANG);',
  'var SLIVES=null, SLIVES_WANT=(!LIVES_LANGS[SLANG]?null:SLANG);'),
 ('SLIVES=null; SLIVES_WANT=(L==="en"||!LIVES_LANGS[L]?null:L);',
  'SLIVES=null; SLIVES_WANT=(!LIVES_LANGS[L]?null:L);'),
 # s.life is gone from the records; the empty string is what "not yet" looks
 # like here, and the page already has a line for it
 ('function slife(s){ return (SLIVES&&SLIVES[s.name])||s.life; }',
  'function slife(s){ return (SLIVES&&SLIVES[s.name])||s.life||""; }'),
]


def point(src):
    a, b = span(src)
    saints = json.loads(src[a:b].rstrip().rstrip(";"))
    if not any("life" in s for s in saints):
        raise SystemExit("the lives are already out of the page")
    if not os.path.exists(OUT):
        raise SystemExit("%s is not there; run --file first" % OUT)
    have = json.load(io.open(OUT, encoding="utf-8"))
    missing = [s["name"] for s in saints
               if (s.get("life") or "").strip() and not (have.get(s["name"]) or "").strip()]
    if missing:
        raise SystemExit("%d lives are in the page but not in the file: %s"
                         % (len(missing), ", ".join(missing[:3])))
    for s in saints:
        s.pop("life", None)
    src = (src[:a] + json.dumps(saints, ensure_ascii=False, separators=(",", ":"))
           + ";" + src[b:])
    for old, new in SUBS:
        if new in src:
            continue
        if old not in src:
            raise SystemExit("not found: " + old[:60])
        src = src.replace(old, new, 1)
    return src


def main():
    src = io.open(PAGE, encoding="utf-8").read()
    if "--file" in sys.argv:
        write_file(src)
    elif "--point" in sys.argv:
        before = len(src)
        out = point(src)
        io.open(PAGE, "w", encoding="utf-8").write(out)
        print("%s: %.2f MB -> %.2f MB"
              % (PAGE, before / 1048576.0, len(out) / 1048576.0))
    else:
        saints = read(src)
        n = sum(len(s.get("life") or "") for s in saints)
        print("%d saints, %.2f MB of life text in the page"
              % (len(saints), n / 1048576.0))


if __name__ == "__main__":
    main()
