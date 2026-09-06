#!/usr/bin/env python3
"""
Advance a language one batch at a time, without deciding what comes next.

Three bodies of text are written per language and each was, until now, driven
by a script that lived in a scratch directory and died with the machine:

    lives   tools/saint_lives/<lang>.py    the life on the Saints index
    info    tools/saint_info/<lang>.py     the short entry on the day panel
    terms   tools/saint_terms/<lang>.py    the vocabulary beside a life

What made those runs continue for hours was not stamina. It was that the
next batch of work was a pure function of what is already written, so no
batch ever had to stop and look. That property is what lives here.

    python3 tools/loop.py info de --next 8      the next eight to write
    python3 tools/loop.py info de --append f    take the batch in f
    python3 tools/loop.py info de --status      how far the language is

Ordering is sorted(), not a frozen list, so the queue survives a lost
container, a new machine, and any interruption: the same command tomorrow
returns the same next eight. --append zips the blocks in the file against
that same order, so a key is never retyped and never lands on the wrong
saint. Blocks are separated by a line containing only @@@.

    lives   one block  = the life
    info    one block  = type, life, patron - each on its own line, and
                         two lines where the English carries no patron
    terms   one block  = the rendering of the phrase

Everything a batch used to check by hand is checked here instead: the count,
the stray characters that language may not contain, a placeholder that was
never resolved, and whether the file still imports. Nothing is written if
any of it fails.

A language that has no file yet is begun with --start, so the first batch of
a new language costs no more thought than the four hundredth.
"""
import argparse
import importlib.util
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent

KINDS = {
    "lives": {
        "dir": TOOLS / "saint_lives",
        "shape": "one block is the life, its paragraphs a line apart",
        # A life is usually one paragraph and was one line here. A few are
        # not - the Conception of the Theotokos runs to three, in the English
        # and in the Greek and Russian that were written from it - and a life
        # that arrived in paragraphs could not be filed at all. The paragraphs
        # of a block are kept and separated as the house style separates them.
        "lines": (1, 12),
    },
    "info": {
        "dir": TOOLS / "saint_info",
        "shape": "one block is type, life, patron - one per line",
        "lines": (2, 3),
    },
    "terms": {
        "dir": TOOLS / "saint_terms",
        "shape": "one block is the rendering of the phrase",
        "lines": (1, 1),
    },
}

# What a rendering in this language may not contain. The dashes, the
# typographic quotes and the soft hyphen are house rules and hold for every
# language. A script it does not use is a paste that came from somewhere
# else: German with Cyrillic in it is a name that was never transliterated.
HOUSE = "\u2013\u2014\u2018\u2019\u201c\u201d\u201e\u00ad"
GREEK = (0x370, 0x3ff)
CYRILLIC = (0x400, 0x52f)

SCRIPTS = {
    "el": [GREEK],
    "ru": [CYRILLIC], "uk": [CYRILLIC], "sr": [CYRILLIC], "bg": [CYRILLIC],
    "ka": [(0x10a0, 0x10ff)],
    "hy": [(0x530, 0x58f)],
    "ar": [(0x600, 0x6ff)], "ur": [(0x600, 0x6ff)],
    "arc": [(0x700, 0x74f)],
    "he": [(0x590, 0x5ff)],
    "hi": [(0x900, 0x97f)], "bn": [(0x980, 0x9ff)],
    "zh": [(0x4e00, 0x9fff)],
    "ja": [(0x3040, 0x30ff), (0x4e00, 0x9fff)],
    "ko": [(0xac00, 0xd7af), (0x1100, 0x11ff)],
}

# A letter the language's own spelling does not use, whatever Unicode allows.
# Cyrillic is one range, so requiring it does not tell one Cyrillic language
# from another, and the languages that share it are exactly the ones a writer
# drifts between. Serbian has its own six letters and does without ten that
# Russian keeps; naming those ten here turns a drift into Russian from
# something only a reader would notice into something the appender refuses.
#
# The Arabic block is one range and holds four languages, so requiring it tells
# Arabic from Greek and not from Urdu or Persian, which are the ones a writer
# drifts into. Every letter below is Persian or Urdu and none is Modern
# Standard Arabic: the Urdu kaf and yeh for the Arabic ones, the retroflexes
# Arabic has no sounds for, the four Persian consonants. Naming them turns a
# drift into Urdu from something only a reader of Arabic would notice into
# something the appender refuses.
#
# The reverse list, for Urdu, is deliberately not written. Urdu carries Arabic
# letters honestly in its loanwords and in the phrases it quotes, so the same
# trick does not work in that direction and would refuse good text. It wants
# writing when Urdu is begun, not guessing at now.
# A combining mark the language writes although it lies outside its own
# block. Syriac marks the plural with seyame, U+0308 over the letter, and
# all four bodies of Syriac on this site write it; a plural without it is a
# defect a reader sees at once.
MARKS = {"arc": "\u0308"}

FORBID = {
    "de": "\u00df",
    "ar": "\u067e\u0686\u0698\u06af\u06a9\u06cc\u06c1\u06be"
          "\u06d2\u06ba\u0679\u0688\u0691\u06c3\u06d3",
    "sr": "\u0451\u0439\u0449\u044a\u044b\u044c\u044d\u044e\u044f"
          "\u0401\u0419\u0429\u042a\u042b\u042c\u042d\u042e\u042f"
          "\u0456\u0457\u0454\u0491\u0406\u0407\u0404\u0490",
}


LATIN = re.compile(
    # A Latin letter with a Cyrillic or Greek letter against it, either side.
    # Half the Latin alphabet has a twin that is a different character with
    # the same picture - a, c, e, o, p, x - so this corruption is invisible
    # on the page and survives every check that reads the text as text. It
    # only shows when the word is compared with itself.
    "[A-Za-z][Ͱ-ϿЀ-ӿ]|[Ͱ-ϿЀ-ӿ][A-Za-z]")


def mixed(values):
    """Every word carrying two alphabets at once."""
    return sorted({w for v in values for w in v.split() if LATIN.search(w)})


def stray(lang, values):
    """Every character a rendering in this language may not carry."""
    allowed = SCRIPTS.get(lang, [])
    bad = set()
    for v in values:
        for c in v:
            o = ord(c)
            if c in HOUSE or c in FORBID.get(lang, ""):
                bad.add(c)
            elif unicodedata.combining(c) \
                    and c not in MARKS.get(lang, "") \
                    and not any(lo <= o <= hi for lo, hi in allowed):
                # A combining mark inside the language's own script is the
                # spelling, not a stray: Devanagari and Bengali cannot be
                # written without the virama, and Syriac and Arabic point
                # their vowels. A stress mark over a Cyrillic word, or a soft
                # hyphen anywhere, is still caught, because neither lies in
                # the range the language is written in.
                bad.add(c)
            elif (GREEK[0] <= o <= GREEK[1] or CYRILLIC[0] <= o <= CYRILLIC[1]) \
                    and not any(lo <= o <= hi for lo, hi in allowed):
                bad.add(c)
    return sorted(bad)


def load(path, name="_loop"):
    """The module's TEXT, imported under a name of our own.

    Under its own name it would collide: saint_terms/de.py, saint_lives/de.py
    and saint_info/de.py all bind de, and a plain import returns whichever
    was imported first.
    """
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def literal(src, name):
    """The JSON literal assigned to name on one line, as the pages write it."""
    i = src.index("const %s=" % name)
    eq = src.index("=", i)
    j = src.index("\n", i)
    return json.loads(src[eq + 1:j].rstrip().rstrip(";"))


def english(kind):
    """What there is to write, keyed the way the file must key it."""
    if kind == "info":
        import saint_info_en
        info = saint_info_en.load()
        return {k: {f: v[f] for f in ("type", "life", "patron") if v.get(f)}
                for k, v in info.items()}
    if kind == "lives":
        spec = importlib.util.spec_from_file_location(
            "_bsl", TOOLS / "build_saint_lives.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.english()
    spec = importlib.util.spec_from_file_location(
        "_bst", TOOLS / "build_saint_terms.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {p: p for p in mod.english()}


def published(kind, lang):
    """What is already on the page, which the module is not the only source of.

    The calendar entries are published to data/saint-info.v1.<lang>.json, and
    a language can carry entries there that were never in its module - German
    had a hundred and forty-six. Counting the module alone would put them all
    back in the queue and have them written a second time.

    They were inlined in index.html as SAINT_INFO_I18N until the page was cut
    from 16.2 MB to 4.1 by lifting them out. Reading them from the page after
    that returned nothing, which silently put every published entry back in
    the queue.
    """
    if kind != "info":
        return {}
    p = ROOT / "data" / ("saint-info.v1.%s.json" % lang)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def written(kind, lang):
    """What the language has already, including anything it assembles."""
    mod = load(KINDS[kind]["dir"] / ("%s.py" % lang), "_loop_%s" % kind)
    if mod is None:
        return None, {}
    have = dict(published(kind, lang))
    have.update(getattr(mod, "TEXT", {}))
    if kind == "terms" and hasattr(mod, "expand"):
        built = mod.expand(set(english("terms")))
        built.update(have)
        have = built
    return mod, have


def remaining(kind, lang):
    """The queue, in the one order that is the same tomorrow."""
    en = english(kind)
    _, have = written(kind, lang)
    return en, [k for k in sorted(en) if k not in have]


TEMPLATE = {
    "lives": '''# -*- coding: utf-8 -*-
"""%(name)s lives for the Saints index. TEXT = {English name: the life}.

The register was settled before a line of this file was written; see
docs/%(doc)s.md. Where a phrase has a received form in this language's own
liturgical books, the received form stands and is not re-rendered.
"""
TEXT = {
}
''',
    "info": '''# -*- coding: utf-8 -*-
"""%(name)s calendar entries. TEXT = {English name: {type, life, patron}}.

The calendar's life is the short one the day panel shows; the long one is in
tools/saint_lives/%(lang)s.py, and a saint is written in both places at once so
that neither has to be come back to.

Only the fields that have been written are given; anything absent falls back
to the English.
"""
TEXT = {
}
''',
    "terms": '''# -*- coding: utf-8 -*-
"""%(name)s for the vocabulary that stands beside the lives.

TEXT = {the phrase the index shows: the rendering}. The keys are the phrases
exactly as the index writes them, so a rendering cannot quietly attach itself
to the wrong saint.

A language may later declare PARTS and an expand() to assemble the compound
place-names from pieces rendered once, as the older languages do. It is an
optimisation and not a requirement: everything written in TEXT stands over
whatever expand() builds.
"""
TEXT = {
}
''',
}


def start(kind, lang, name):
    path = KINDS[kind]["dir"] / ("%s.py" % lang)
    if path.exists():
        raise SystemExit("%s already exists" % path)
    doc = {"de": "GERMAN", "el": "GREEK", "ro": "ROMANIAN",
           "uk": "UKRAINIAN"}.get(lang, name.upper())
    path.write_text(TEMPLATE[kind] % {"name": name, "lang": lang, "doc": doc},
                    encoding="utf-8")
    print("wrote %s" % path.relative_to(ROOT))


def show_next(kind, lang, n, from_end=False):
    """The next n to write, from the front of what remains or from the back.

    Two lanes may share one language when there is nothing else outstanding.
    They are given opposite ends of the same remaining list, so they walk
    towards each other and never hold the same saint: each batch re-reads the
    file, so what one has written is already gone from what the other is
    offered. next_job.py stops sharing a job before the ends can meet.
    """
    en, rem = remaining(kind, lang)
    print("remaining %d" % len(rem))
    print("blocks: %s" % KINDS[kind]["shape"])
    chosen = list(reversed(rem[-n:])) if from_end else rem[:n]
    for i, key in enumerate(chosen):
        v = en[key]
        print("\n===[%d] %s" % (i, key))
        if isinstance(v, dict):
            print("  type: %s" % v.get("type", ""))
            print("  life: %s" % v.get("life", ""))
            print("  patron: %s" % v.get("patron", "(none)"))
        elif kind == "terms":
            pass
        else:
            print(v)


def blocks(path):
    raw = io.open(path, encoding="utf-8").read()
    out = [b.strip("\n") for b in re.split(r"(?m)^@@@$", raw)]
    return [b for b in out if b.strip()]


def render(kind, key, block):
    """One block, as the file stores it."""
    lines = [l for l in block.split("\n") if l.strip()]
    lo, hi = KINDS[kind]["lines"]
    if not lo <= len(lines) <= hi:
        raise SystemExit("%r: %d lines, expected %d-%d\n%s"
                         % (key, len(lines), lo, hi, block))
    if kind == "info":
        d = {"type": lines[0].strip(), "life": lines[1].strip()}
        if len(lines) > 2:
            d["patron"] = lines[2].strip()
        return d
    if kind == "terms":
        return " ".join(l.strip() for l in lines)
    # One blank line between paragraphs, which is how the site writes them.
    return "\n\n".join(l.strip() for l in lines)


def append(kind, lang, path):
    en, rem = remaining(kind, lang)
    bs = blocks(path)
    if not bs:
        raise SystemExit("no blocks in %s" % path)
    if len(bs) > len(rem):
        raise SystemExit("%d blocks but only %d remain" % (len(bs), len(rem)))

    pairs = []
    for key, block in zip(rem, bs):
        if "@@" in block:
            raise SystemExit("%r still carries a placeholder:\n%s" % (key, block))
        value = render(kind, key, block)
        if kind == "info":
            src = en[key]
            if "patron" not in src:
                value.pop("patron", None)
            flat = list(value.values())
        else:
            flat = [value]
        bad = stray(lang, flat)
        if bad:
            raise SystemExit("%r carries %s"
                             % (key, " ".join("%r" % c for c in bad)))
        both = mixed(flat)
        if both:
            raise SystemExit("%r has two alphabets in one word: %s"
                             % (key, " ".join("%r" % w for w in both)))
        pairs.append((key, value))

    file = KINDS[kind]["dir"] / ("%s.py" % lang)
    s = file.read_text(encoding="utf-8")
    add = ""
    for key, value in pairs:
        k = json.dumps(key, ensure_ascii=False)
        if kind == "terms":
            add += "    %s: %s,\n" % (k, json.dumps(value, ensure_ascii=False))
        elif kind == "info":
            add += "\n%s:\n%s,\n" % (k, json.dumps(value, ensure_ascii=False))
        else:
            add += "\n%s:\n%s,\n" % (k, json.dumps(value, ensure_ascii=False))

    if kind == "terms":
        add = "\n\nTEXT.update({\n%s})\n" % add
        out = s.rstrip("\n") + add
    else:
        i = s.rindex("\n}")
        out = s[:i] + "\n" + add + s[i + 1:]

    backup = s
    file.write_text(out, encoding="utf-8")
    try:
        mod, have = written(kind, lang)
        for key, _ in pairs:
            if key not in have:
                raise SystemExit("%r did not land in TEXT" % key)
    except SystemExit:
        file.write_text(backup, encoding="utf-8")
        raise
    except Exception as exc:
        file.write_text(backup, encoding="utf-8")
        raise SystemExit("the file no longer imports: %s" % exc)

    en2, rem2 = remaining(kind, lang)
    print("appended %d   %s %s: %d of %d"
          % (len(pairs), lang, kind, len(en2) - len(rem2), len(en2)))


def status(kind, lang):
    en, rem = remaining(kind, lang)
    if rem is None:
        print("%s %s: no file yet; begin it with --start" % (lang, kind))
        return
    print("%-4s %-6s %5d of %d   (%d remaining)"
          % (lang, kind, len(en) - len(rem), len(en), len(rem)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("kind", choices=sorted(KINDS))
    ap.add_argument("lang")
    ap.add_argument("--next", type=int, metavar="N")
    ap.add_argument("--from-end", action="store_true",
                    help="take from the back of what remains, for a second "
                         "lane sharing this language")
    ap.add_argument("--append", metavar="FILE")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--start", metavar="NAME",
                    help="begin the language, NAME as it is written in English")
    args = ap.parse_args()

    if args.start:
        start(args.kind, args.lang, args.start)
        return 0
    if (KINDS[args.kind]["dir"] / ("%s.py" % args.lang)).exists() is False:
        raise SystemExit("no tools/%s/%s.py yet; begin it with --start NAME"
                         % (KINDS[args.kind]["dir"].name, args.lang))
    if args.append:
        append(args.kind, args.lang, args.append)
    if args.next:
        show_next(args.kind, args.lang, args.next, args.from_end)
    if args.status or not (args.append or args.next):
        status(args.kind, args.lang)
    return 0


if __name__ == "__main__":
    sys.exit(main())
