#!/usr/bin/env python3
"""Restore quoted Hindi Scripture in the first lives from the published edition."""

import ast
import base64
import json
from pathlib import Path
import zlib


ROOT = Path(__file__).resolve().parents[1]
LIVES = ROOT / "tools" / "saint_lives" / "hi.py"
BIBLE = ROOT / "data" / "bible.v4.hi.b64"


def verse(bible, book, chapter, verse):
    return bible["hi"][book][str(chapter)][str(verse)]


def spoken(text):
    """Return the words within the edition's outer typographic quotation marks."""
    if "“" in text:
        text = text.split("“", 1)[1]
    if text.endswith("”"):
        text = text[:-1]
    return text


def main():
    bible = json.loads(zlib.decompress(base64.b64decode(BIBLE.read_bytes())))

    acts_9_17 = spoken(verse(bible, "Acts", 9, 17)).split(" और तुम", 1)[0]
    expected = {
        "Afterfeast of the Meeting of our Lord in the Temple": (
            "परम प्रधान प्रभु, अब अपनी प्रतिज्ञा के अनुसार अपने सेवक को शांति में विदा कीजिए।",
            spoken(verse(bible, "Luke", 2, 29)),
        ),
        "Afterfeast of the Nativity of our Lord and Savior Jesus Christ": (
            "यह निश्चित है कि वह बढ़ते जाएँ और मैं घटता जाऊँ।",
            spoken(verse(bible, "John", 3, 30)),
        ),
        "Apostle Ananias of the Seventy": (
            "भाई शाऊल, तुम्हें दोबारा आँखों की रोशनी मिल जाए।",
            acts_9_17,
        ),
        "Apostle Andrew, the Holy and All-Praised First-Called": (
            "हमें मसीह मिल गए हैं।",
            spoken(verse(bible, "John", 1, 41)),
        ),
    }

    john_1_29 = spoken(verse(bible, "John", 1, 29))
    source = LIVES.read_text(encoding="utf-8")
    if john_1_29 not in source:
        raise SystemExit("John 1:29 is not already verbatim")

    lines = source.splitlines(keepends=True)
    corrected = 0
    for key, (old, new) in expected.items():
        key_line = json.dumps(key, ensure_ascii=False) + ":"
        try:
            index = next(i for i, line in enumerate(lines) if line.rstrip() == key_line)
        except StopIteration as exc:
            raise SystemExit(f"missing life: {key}") from exc
        value = ast.literal_eval(lines[index + 1].rstrip().removesuffix(","))
        if new in value:
            continue
        if old not in value:
            raise SystemExit(f"expected quoted span not found: {key}")
        value = value.replace(old, new, 1)
        ending = "\r\n" if lines[index + 1].endswith("\r\n") else "\n"
        lines[index + 1] = json.dumps(value, ensure_ascii=False) + "," + ending
        corrected += 1

    if corrected:
        LIVES.write_text("".join(lines), encoding="utf-8", newline="")
    print(f"corrected {corrected} quoted Scripture spans")


if __name__ == "__main__":
    main()
