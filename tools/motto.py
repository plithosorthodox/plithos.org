#!/usr/bin/env python3
"""
The site's motto, over the wordmark, in every language the Library offers.

Six pages carry "According to the whole" - kath' holou, the phrase the word
catholic is made of. The Library carried "a library of the Fathers" instead,
and carried it smaller and in grey, so the one page that names the Fathers
was the one page that did not say what the site is.

The Greek is the phrase itself and is left as it stands; the rest render it.
The Saints page already had English, Russian and Greek, and those three are
kept word for word so the two pages do not disagree.

    python3 tools/motto.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"

WORDS = {
    "en": "according to the whole",
    "ru": "согласно целому",
    "el": "καθ' όλου",
    "uk": "згідно з цілим",
    "sr": "по целини",
    "ro": "potrivit întregului",
    "cu": "соглáсно цѣ́лому",
    "ka": "მთელის მიხედვით",
    "es": "según el todo",
    "pt": "segundo o todo",
    "it": "secondo il tutto",
    "fr": "selon le tout",
    "de": "nach dem Ganzen",
    "ar": "بحسب الكل",
    "zh": "依乎全體",
    "ja": "全体に従いて",
    "ko": "전체를 따라",
    "sw": "kwa mujibu wa yote",
    "hi": "सम्पूर्ण के अनुसार",
    "hy": "ըստ ամբողջի",
    "arc": "ܐܝܟ ܟܠܗ",
}


def main():
    s = PAGE.read_text(encoding="utf-8")
    i = s.index("const RLEX={")
    j = s.index("\n};", i)
    head, block, tail = s[:i], s[i:j + 2], s[j + 2:]

    n = 0
    for code, word in WORDS.items():
        m = re.search(r'\n ("?)%s\1:\{' % re.escape(code), block)
        if not m:
            print("no such language in the lexicon: %s" % code, file=sys.stderr)
            return 1
        at = m.end()
        end = block.index("\n", at)
        line = block[at:end]
        pat = re.compile(r'"?tagline"?:"(?:[^"\\]|\\.)*"')
        if not pat.search(line):
            print("no tagline for %s" % code, file=sys.stderr)
            return 1
        line = pat.sub('"tagline":%s' % json.dumps(word, ensure_ascii=False),
                       line, count=1)
        block = block[:at] + line + block[end:]
        n += 1

    PAGE.write_text(head + block + tail, encoding="utf-8")
    print("the motto is written in %d languages" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
