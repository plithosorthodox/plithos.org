#!/usr/bin/env python3
"""Set named lives in tools/saint_lives/<lang>.py from a keyed block file.

The appender only ever adds a life that is not yet written, which is right:
a batch cannot quietly overwrite the work of the batch before it. The one
thing it therefore cannot do is correct a life that was filed under the
wrong saint, and ten of the Syriac lives were - a batch of ten apostles
received the ten lives of the batch before it, so Sosthenes carried the
life of Matthias, Titus the life of Pudens, and the Evangelist Luke the
life of Silvanus. This rewrites named entries in place and leaves every
other line of the file exactly as it was.

    python3 tools/fix_arc_lives.py arc repair.txt

Blocks are separated by a line containing only @@@; the first line of a
block is the English key, the rest is the life, its paragraphs a line
apart. A key the file does not already hold is refused, since this
corrects and does not append.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(lang, path):
    src = ROOT / "tools" / "saint_lives" / ("%s.py" % lang)
    text = src.read_text(encoding="utf-8")
    blocks = [b for b in Path(path).read_text(encoding="utf-8").split("\n@@@\n")
              if b.strip()]
    for block in blocks:
        lines = block.strip("\n").split("\n")
        key, life = lines[0], "\n\n".join(l for l in lines[1:] if l.strip())
        old = '"%s":\n' % key
        i = text.find(old)
        if i < 0:
            sys.exit("not in the file: %s" % key)
        j = text.index("\n", i + len(old))
        text = text[:i + len(old)] + json.dumps(life, ensure_ascii=False) \
            + "," + text[j:]
        print("set %s" % key)
    src.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
