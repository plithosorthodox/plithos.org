#!/usr/bin/env python3
"""
Add "editions" to the Library's lexicon, in every language.

The line under the wordmark read "117 works", while the shelf beside it
offered 86. Both numbers were right and neither said what it was counting:
the New Testament in nineteen languages is nineteen editions and one title.
The line now names all three counts, so the shelf no longer looks short.

The word for a title the lexicon already had, as fTitles; only the word for
an edition was missing.

Run once from the repository root:

    python3 tools/tally_words.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"

# An edition is one printing of a title: the shelf offers the Nisibene Hymns
# once, and stands on the Greek and the English of it. A plain library word
# in every language here.
WORDS = {
    "en": "editions",
    "ru": "изданий",
    "uk": "видань",
    "sr": "издања",
    "el": "εκδόσεις",
    "ro": "ediții",
    "cu": "изданій",
    "ka": "გამოცემა",
    "es": "ediciones",
    "pt": "edições",
    "it": "edizioni",
    "fr": "éditions",
    "de": "Ausgaben",
    "ar": "طبعات",
    "zh": "版本",
    "ja": "版",
    "ko": "판본",
    "sw": "matoleo",
    "hi": "संस्करण",
    "hy": "հրատարակություն",
    "arc": "ܡܦܩܬܐ",
}


def main():
    s = PAGE.read_text(encoding="utf-8")
    i = s.index("const RLEX={")
    j = s.index("\n};", i)
    head, block, tail = s[:i], s[i:j + 2], s[j + 2:]

    added = 0
    for code, editions in WORDS.items():
        # Each language is one line: `  <code>:{...}` or `  "<code>":{...}`.
        m = re.search(r'\n ("?)%s\1:\{' % re.escape(code), block)
        if not m:
            print("no such language in the lexicon: %s" % code, file=sys.stderr)
            return 1
        at = m.end()
        if '"editions"' in block[at:block.index("\n", at)]:
            continue
        ins = '"editions":%s,' % json.dumps(editions, ensure_ascii=False)
        block = block[:at] + ins + block[at:]
        added += 1

    PAGE.write_text(head + block + tail, encoding="utf-8")
    print("added editions to %d languages" % added)
    return 0


if __name__ == "__main__":
    sys.exit(main())
