#!/usr/bin/env python3
"""Deterministic guards shared by every translation appender."""
import re
import unicodedata


SCRIPT_RANGES = {
    "el": ((0x0370, 0x03ff),),
    "ru": ((0x0400, 0x052f),), "uk": ((0x0400, 0x052f),),
    "sr": ((0x0400, 0x052f),), "ka": ((0x10a0, 0x10ff),),
    "hy": ((0x0530, 0x058f),), "ar": ((0x0600, 0x06ff),),
    "ur": ((0x0600, 0x06ff),), "arc": ((0x0700, 0x074f),),
    "hi": ((0x0900, 0x097f),), "bn": ((0x0980, 0x09ff),),
    "zh": ((0x3400, 0x9fff),),
    "ja": ((0x3040, 0x30ff), (0x3400, 0x9fff)),
    "ko": ((0x1100, 0x11ff), (0xac00, 0xd7af)),
}
PLACEHOLDER = re.compile(r"(?:@@|\b(?:todo|tbd|placeholder)\b)", re.I)
NUMBER = re.compile(r"(?<!\w)\d+(?:[:./-]\d+)*(?:st|nd|rd|th)?(?!\w)", re.I)


def _plain(value):
    return " ".join(value.casefold().split())


def validate_pairs(lang, pairs):
    """Return stable errors for (key, English source, rendering) triples."""
    errors = []
    rendered = {}
    ranges = SCRIPT_RANGES.get(lang, ())
    for key, source, value in pairs:
        value = value if isinstance(value, str) else ""
        if not value.strip():
            errors.append("%r is blank" % key)
            continue
        if PLACEHOLDER.search(value):
            errors.append("%r carries a placeholder" % key)
        if _plain(value) == _plain(source) and re.search(r"[A-Za-z]", source):
            errors.append("%r is an unexplained English fallback" % key)
        if ranges and re.search(r"[A-Za-z]", source) and not any(
                lo <= ord(c) <= hi for c in value for lo, hi in ranges):
            errors.append("%r has no required native-script character" % key)
        source_numbers = NUMBER.findall(source)
        value_numbers = NUMBER.findall(value)
        if source_numbers != value_numbers:
            errors.append("%r changes numbers/dates/references: %r != %r"
                          % (key, source_numbers, value_numbers))
        if len(source.strip()) >= 80 and len(value.strip()) < len(source.strip()) * .20:
            errors.append("%r is suspiciously truncated" % key)
        norm = _plain(value)
        if len(source.strip()) >= 40 and norm:
            rendered.setdefault(norm, []).append((key, source))
    for same in rendered.values():
        sources = {_plain(source) for _, source in same}
        if len(same) > 1 and len(sources) > 1:
            errors.append("%r and %r have suspicious duplicate translations"
                          % (same[0][0], same[1][0]))
    return errors


def assert_pairs(lang, pairs):
    errors = validate_pairs(lang, pairs)
    if errors:
        raise SystemExit("translation check failed:\n  " + "\n  ".join(errors))
