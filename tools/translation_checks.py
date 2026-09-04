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
# "todo" is not a marker, it is the Spanish for "all", and it stands in six
# hundred and nineteen Spanish lives that are correct. Only the bracketed and
# upper-case forms a person actually leaves behind are looked for.
PLACEHOLDER = re.compile(r"(?:@@@|\[(?:todo|tbd|fixme|placeholder)[^\]]*\]"
                         r"|\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b)")

# A number is what it counts, not the digits it is written with. Arabic and
# Urdu set the Eastern numerals, Bengali, Hindi and Georgian their own, and
# Chinese and Japanese write a year in characters and no digits at all. Compare
# the values, after folding every script's digits to the Arabic ones.
NUMBER = re.compile(r"(?<!\w)\d+(?:[:./-]\d+)*(?:st|nd|rd|th)?(?!\w)", re.I)
GROUPED = re.compile(r"(?<=\d)[,\u00a0\u202f](?=\d\d\d(?!\d))")


def _plain(value):
    return " ".join(value.casefold().split())


def _numbers(value):
    """The numbers a text carries, in any script, as a multiset.

    Folded to Arabic digits, thousands separators removed, and unordered: a
    language may set 20,000 as 20000 and may put the year before the place."""
    folded = []
    for c in value:
        d = unicodedata.digit(c, None) if not c.isascii() else None
        folded.append(str(d) if d is not None else c)
    return sorted(NUMBER.findall(GROUPED.sub("", "".join(folded))))


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
        # A rendering identical to its source is only suspicious where the
        # language does not share the alphabet. German writes Prophet for
        # Prophet and Italian writes Amasea for Amasea; there were 1,788 of
        # those, every one of them right.
        if _plain(value) == _plain(source) and re.search(r"[A-Za-z]", source) \
                and ranges:
            errors.append("%r is an unexplained English fallback" % key)
        if ranges and re.search(r"[A-Za-z]", source) and not any(
                lo <= ord(c) <= hi for c in value for lo, hi in ranges):
            errors.append("%r has no required native-script character" % key)
        source_numbers = _numbers(source)
        value_numbers = _numbers(value)
        # Chinese and Japanese write a year in characters, so a rendering that
        # carries no digit at all is not thereby missing the number.
        if source_numbers != value_numbers and value_numbers:
            errors.append("%r changes numbers/dates/references: %r != %r"
                          % (key, source_numbers, value_numbers))
        if len(source.strip()) >= 80 and len(value.strip()) < len(source.strip()) * .20:
            errors.append("%r is suspiciously truncated" % key)
        norm = _plain(value)
        if len(source.strip()) >= 40 and norm:
            rendered.setdefault(norm, []).append((key, source))
    for same in rendered.values():
        sources = {_plain(source) for _, source in same}
        if len(same) > 1 and len(sources) > 1 and not _same_subject(same):
            errors.append("%r and %r have suspicious duplicate translations"
                          % (same[0][0], same[1][0]))
    return errors


# The index carries one saint under more than one spelling - St Sava and Saint
# Savva I, Vladimir and Volodymyr, Anthony of the Kyiv Caves three ways - and
# the same life belongs to each. Seventy-four of the ninety-four identical
# lives in the corpus are that, and are right. The twenty that are not were a
# batch of ten appended twice.
STOP = {"st", "saint", "the", "of", "and", "in", "venerable", "blessed", "holy",
        "apostle", "martyr", "first", "great", "prince", "princess", "repose",
        "equal-to-the-apostles", "wonderworker", "abbot", "archbishop", "bishop",
        "founder", "monasticism", "seventy", "one", "deacon", "evangelist"}


def _same_subject(same):
    """Two keys naming one saint, which may share a life."""
    # The KEYS, which name the saint. Comparing the sources compares two whole
    # lives, and any two English lives share enough ordinary words to look like
    # one subject - which silenced the twenty Syriac lives this exists to find.
    words = [{w.strip(",.()'\u2019") for w in _plain(k).split()} - STOP
             for k, _ in same]
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if not (words[i] & words[j]):
                return False
    return True


def assert_pairs(lang, pairs):
    errors = validate_pairs(lang, pairs)
    if errors:
        raise SystemExit("translation check failed:\n  " + "\n  ".join(errors))
