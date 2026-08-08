#!/usr/bin/env python3
"""
The word "Languages" over the Library's language picker, in every language.

The picker was headed with an English literal written into the code, so a
reader in Greek or Arabic met one English word in the middle of his own page.
It now stands where the rest of the page's words stand, and it is used by the
picker on every item and not only by the Liturgy's.

    python3 tools/language_words.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"

WORDS = {
    "en": "Languages", "ru": "Языки", "uk": "Мови", "sr": "Језици",
    "el": "Γλώσσες", "ro": "Limbi", "cu": "Љзы́цы", "ka": "ენები",
    "es": "Idiomas", "pt": "Idiomas", "it": "Lingue", "fr": "Langues",
    "de": "Sprachen", "ar": "اللغات", "zh": "语言", "ja": "言語",
    "ko": "언어", "sw": "Lugha", "hi": "भाषाएँ", "hy": "Լեզուներ",
    "arc": "ܠܫܢܐ",
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
        # The key, not the word: English already carries langsWord:"languages"
        # as a value, and matching on the bare word skipped it.
        if re.search(r'"?languages"?\s*:', block[at:end]):
            continue
        block = block[:at] + '"languages":%s,' % json.dumps(word, ensure_ascii=False) + block[at:]
        n += 1

    PAGE.write_text(head + block + tail, encoding="utf-8")
    print("wrote the word for languages to %d languages" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
