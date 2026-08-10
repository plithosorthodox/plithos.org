#!/usr/bin/env python3
"""
Put the site's own voice into American spelling.

The site is published from the United States and should read as one thing.
It did not: "colour" in a note beside the theme, "Defence of the faith" on
the shelf, "Canonisation" in the glossary, "centre of unity" in a definition.
Those are the site speaking, and they are now American.

What this does NOT touch, and must never touch:

  * the text of the Fathers. The translations here are British editions of
    the 1880s and 1890s - Salmond, Schaff, Roberts and Donaldson - and
    "Saviour" and "defence" are what those translators wrote. Changing them
    would mean the site no longer reproduces what it says it reproduces.
  * the prayers and the liturgical texts. "More honourable than the Cherubim"
    is the Church's own English, received and prayed. It is not ours to
    respell.
  * Holy Scripture, for the same reason.
  * a work's title, author, translator, source or publisher, and the section
    headings a translator set. An edition is cited as it was printed.
  * proper names that only look British: Tyre, the Holy Sepulchre, the
    Prologue of Ohrid, St Gregory's Dialogues, Labour Day as a civil holiday,
    and every string in French, Portuguese or any other language.
  * Scripture quoted inside the site's own prose. A life may carry a verse
    without quotation marks, and the verse is still the verse: PROTECTED
    below holds those, and the pass refuses to run if one of them changes.

So the rule is by field, not by file: the site's own descriptions, notes,
labels, definitions, saints' lives and shelf vocabulary change; the texts it
carries do not.

    python3 tools/us_spelling.py --check    # report, change nothing
    python3 tools/us_spelling.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# British form -> American form. Only entries where the two conventions really
# differ; "dialogue", "epilogue" and "prologue" are standard American and are
# absent on purpose.
US = {
    "colour": "color", "colours": "colors", "coloured": "colored",
    "colouring": "coloring", "colourful": "colorful",
    "offence": "offense", "offences": "offenses",
    "defence": "defense", "defences": "defenses",
    "pretence": "pretense", "licence": "license",
    "honour": "honor", "honours": "honors", "honoured": "honored",
    "honouring": "honoring", "honourable": "honorable", "honourably": "honorably",
    "saviour": "savior", "saviours": "saviors",
    "favour": "favor", "favours": "favors", "favoured": "favored",
    "favouring": "favoring", "favourable": "favorable", "favourably": "favorably",
    "favourite": "favorite", "favourites": "favorites",
    "labour": "labor", "labours": "labors", "laboured": "labored",
    "labouring": "laboring", "labourer": "laborer", "labourers": "laborers",
    "neighbour": "neighbor", "neighbours": "neighbors",
    "neighbouring": "neighboring", "neighbourhood": "neighborhood",
    "behaviour": "behavior", "behaviours": "behaviors",
    "endeavour": "endeavor", "endeavours": "endeavors", "endeavoured": "endeavored",
    "splendour": "splendor", "splendours": "splendors",
    "vapour": "vapor", "vapours": "vapors", "vigour": "vigor",
    "odour": "odor", "odours": "odors", "ardour": "ardor",
    "clamour": "clamor", "clamours": "clamors", "fervour": "fervor",
    "rigour": "rigor", "rigours": "rigors", "valour": "valor",
    "succour": "succor", "succoured": "succored", "armour": "armor",
    "armoured": "armored", "harbour": "harbor", "harboured": "harbored",
    "rumour": "rumor", "rumours": "rumors", "tumour": "tumor",
    "centre": "center", "centres": "centers", "centred": "centered",
    "centring": "centering", "theatre": "theater", "theatres": "theaters",
    "fibre": "fiber", "fibres": "fibers", "sombre": "somber",
    "practise": "practice", "practised": "practiced", "practises": "practices",
    "practising": "practicing",
    "travelling": "traveling", "travelled": "traveled",
    "traveller": "traveler", "travellers": "travelers",
    "counselling": "counseling", "counselled": "counseled",
    "counsellor": "counselor", "counsellors": "counselors",
    "marvellous": "marvelous", "marvellously": "marvelously", "marvelled": "marveled",
    "woollen": "woolen", "jewellery": "jewelry",
    "labelled": "labeled", "labelling": "labeling",
    "fulfil": "fulfill", "fulfils": "fulfills",
    "enrol": "enroll", "enrols": "enrolls",
    "skilful": "skillful", "skilfully": "skillfully",
    "wilful": "willful", "wilfully": "willfully",
    "judgement": "judgment", "judgements": "judgments",
    "acknowledgement": "acknowledgment", "acknowledgements": "acknowledgments",
    "catalogue": "catalog", "catalogues": "catalogs", "catalogued": "cataloged",
    "analogue": "analog", "analogues": "analogs",
    "grey": "gray", "greys": "grays", "greyish": "grayish",
    "plough": "plow", "ploughs": "plows", "ploughed": "plowed", "ploughing": "plowing",
    "mould": "mold", "moulds": "molds", "moulded": "molded", "moulding": "molding",
    "smoulder": "smolder", "smouldering": "smoldering",
    "sceptic": "skeptic", "sceptics": "skeptics",
    "sceptical": "skeptical", "scepticism": "skepticism",
    "analyse": "analyze", "analysed": "analyzed", "analyses": "analyzes",
    "analysing": "analyzing", "paralyse": "paralyze", "paralysed": "paralyzed",
    "storey": "story", "storeys": "stories",
    "aeon": "eon", "aeons": "eons", "manoeuvre": "maneuver",
    # -ise/-isation, only where the British suffix is genuine
    "baptise": "baptize", "baptised": "baptized", "baptises": "baptizes",
    "baptising": "baptizing",
    "canonise": "canonize", "canonised": "canonized",
    "canonisation": "canonization",
    "catechise": "catechize", "catechised": "catechized",
    "anathematise": "anathematize", "anathematised": "anathematized",
    "evangelise": "evangelize", "evangelised": "evangelized",
    "solemnise": "solemnize", "solemnised": "solemnized",
    "proselytise": "proselytize", "proselytising": "proselytizing",
    "recognise": "recognize", "recognised": "recognized", "recognises": "recognizes",
    "organise": "organize", "organised": "organized", "organising": "organizing",
    "organisation": "organization", "organisations": "organizations",
    "realise": "realize", "realised": "realized", "realising": "realizing",
    "emphasise": "emphasize", "emphasised": "emphasized", "emphasising": "emphasizing",
    "criticise": "criticize", "criticised": "criticized",
    "apologise": "apologize", "apologised": "apologized",
    "memorise": "memorize", "memorised": "memorized",
    "minimise": "minimize", "maximise": "maximize",
    "summarise": "summarize", "summarised": "summarized", "summarising": "summarizing",
    "sympathise": "sympathize", "symbolise": "symbolize", "symbolised": "symbolized",
    "utilise": "utilize", "utilised": "utilized",
    "authorise": "authorize", "authorised": "authorized",
    "characterise": "characterize", "characterised": "characterized",
    "generalise": "generalize", "generalised": "generalized",
    "formalise": "formalize", "formalised": "formalized", "formalising": "formalizing",
    "systematise": "systematize", "systematised": "systematized",
    "specialise": "specialize", "specialised": "specialized",
    "standardise": "standardize", "standardised": "standardized",
    "harmonise": "harmonize", "harmonised": "harmonized",
    "moralise": "moralize", "moralising": "moralizing",
    "allegorise": "allegorize", "allegorised": "allegorized",
    "spiritualise": "spiritualize", "spiritualised": "spiritualized",
    "secularise": "secularize", "secularised": "secularized",
    "legalise": "legalize", "legalised": "legalized",
    "civilise": "civilize", "civilised": "civilized",
    "idolise": "idolize", "idolised": "idolized",
    "agonise": "agonize", "agonised": "agonized", "agonising": "agonizing",
    "philosophise": "philosophize", "monopolise": "monopolize",
    "scrutinise": "scrutinize", "scrutinised": "scrutinized",
    "patronise": "patronize", "patronised": "patronized",
    "rationalise": "rationalize", "rationalised": "rationalized",
    "familiarise": "familiarize", "familiarised": "familiarized",
    "prioritise": "prioritize", "publicise": "publicize",
    "vandalise": "vandalized", "sterilise": "sterilize",
    "immortalise": "immortalize", "immortalised": "immortalized",
    "normalise": "normalize", "localise": "localize",
    "colonise": "colonize", "colonised": "colonized",
}


# Scripture standing inside a sentence the site wrote. The words around
# these may be respelled; these may not.
PROTECTED = [
    "Take heed to the ministry which thou hast received in the Lord, "
    "that thou fulfil it",
]


def _cap(word, model):
    """Carry the British word's capitalisation onto the American one."""
    if model.isupper():
        return word.upper()
    if model[:1].isupper():
        return word[:1].upper() + word[1:]
    return word


_RE = re.compile(r"\b(%s)\b" % "|".join(sorted(US, key=len, reverse=True)),
                 re.IGNORECASE)


def respell(s):
    """Every British word in a string replaced. Case is preserved.

    Scripture standing inside the sentence is lifted out first and put back
    untouched, so a verse keeps the spelling it was received in even where
    the sentence around it does not."""
    held = []
    for i, q in enumerate(PROTECTED):
        if q in s:
            s = s.replace(q, "\u0000%d\u0000" % i)
            held.append((i, q))

    def sub(m):
        w = m.group(1)
        us = US.get(w.lower())
        return _cap(us, w) if us else w
    s = _RE.sub(sub, s)
    for i, q in held:
        s = s.replace("\u0000%d\u0000" % i, q)
    return s


def changes(s):
    for q in PROTECTED:
        s = s.replace(q, "")
    out = []
    for m in _RE.finditer(s):
        us = US.get(m.group(1).lower())
        if us and _cap(us, m.group(1)) != m.group(1):
            out.append((m.group(1), _cap(us, m.group(1))))
    return out


# ---------------------------------------------------------------- comments

# Comments in a served file are the site talking to whoever reads the source,
# and CLAUDE.md counts them as its voice. Nothing else in these files is
# touched by this pass: the prose replacements below are named one by one.
COMMENT = re.compile(r"<!--.*?-->|/\*.*?\*/", re.S)


def do_comments(path, report):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")

    def one(m):
        new = respell(m.group(0))
        if new != m.group(0):
            report.setdefault(path, []).extend(changes(m.group(0)))
        return new

    return s, COMMENT.sub(one, s)


# --------------------------------------------------------- named prose

# Reader-visible sentences in the site's own voice, quoted in full so that
# each one is a decision rather than a pattern. The French, Portuguese and
# other-language strings beside some of them are deliberately not here:
# "licence" is correct French and stays.
PROSE = [
    ("rule.html",
     "St Seraphim gave it to labourers and householders",
     "St Seraphim gave it to laborers and householders"),
    ("rule.html",
     "peace with one's neighbour",
     "peace with one's neighbor"),
    ("rule.html",
     "take a difference of custom for a judgement on him",
     "take a difference of custom for a judgment on him"),
    ("rule.html",
     "the three canons, to the Saviour, to the Theotokos",
     "the three canons, to the Savior, to the Theotokos"),
    ("contact.html",
     "questions of provenance and licence",
     "questions of provenance and license"),
    ("library.html",
     "Each edition is labelled by its tradition.",
     "Each edition is labeled by its tradition."),
]


def do_prose(path, s, report):
    for f, old, new in PROSE:
        if f != path:
            continue
        n = s.count(old)
        if n == 0:
            print("prose no longer present in %s: %r" % (f, old[:50]), file=sys.stderr)
            continue
        if n > 1:
            print("prose is not unique in %s: %r" % (f, old[:50]), file=sys.stderr)
            continue
        s = s.replace(old, new)
        report.setdefault(path, []).extend(changes(old))
    return s


# ------------------------------------------------------------ data fields

# The fields the site writes itself. Everything absent from this list is a
# source being reproduced and is left exactly as it stands - above all
# `text`, `body`, `citation_anchor`, `title`, `author`, `translator`,
# `source` and `publisher`.
OWN_FIELDS = {
    "description", "caution", "purpose", "topics",
    "life", "icon", "patronWork", "patronCauses", "patronPlaces",
    "related", "relics", "titles", "origin", "place", "region",
    "d", "t",
}


def walk_fields(o, report, path, seen):
    """Respell the site's own fields, in place, anywhere in a structure."""
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if isinstance(v, str) and k in OWN_FIELDS:
                new = respell(v)
                if new != v:
                    report.setdefault(path, []).extend(changes(v))
                    o[k] = new
            elif isinstance(v, list) and k in OWN_FIELDS:
                o[k] = [respell(x) if isinstance(x, str) else x for x in v]
                for x in v:
                    if isinstance(x, str):
                        report.setdefault(path, []).extend(changes(x))
            else:
                walk_fields(v, report, path, seen)
    elif isinstance(o, list):
        for v in o:
            walk_fields(v, report, path, seen)


def one_line_of(src, name, opener):
    needle = "const " + name + opener
    i = src.index(needle)
    start = i + len("const " + name)
    j = src.index("\n", i)
    raw = src[start:j].lstrip()
    if raw.startswith("="):
        raw = raw[1:]
    return i, j, json.loads(raw.strip().rstrip(";"))


def do_inline_data(path, s, name, opener, report):
    """One of the enormous single-line datasets inside a page."""
    i, j, data = one_line_of(s, name, opener)
    walk_fields(data, report, path, set())
    line = "const %s=%s;" % (name, json.dumps(data, ensure_ascii=False,
                                              separators=(",", ":")))
    if opener.startswith(" "):
        line = "const %s = %s;" % (name, json.dumps(data, ensure_ascii=False,
                                                    separators=(",", ":")))
    return s[:i] + line + s[j:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    report = {}
    writes = {}

    pages = ["index.html", "saints.html", "library.html", "prayers.html",
             "glossary.html", "rule.html", "contact.html"]
    # Only the versions the pages load. The earlier ones were served
    # immutable and are frozen: a browser holding one keeps it for a year,
    # so editing them changes nothing and loses the record of what shipped.
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    assets = re.findall(r"assets/(plithos-ui\.v\d+\.(?:css|js))", idx)

    for f in pages + ["assets/" + n for n in assets]:
        _, s = do_comments(f, report)
        s = do_prose(f, s, report)
        writes[f] = s

    # The two inline datasets that carry fields the site wrote.
    writes["saints.html"] = do_inline_data(
        "saints.html", writes["saints.html"], "SAINTS", "=[", report)
    writes["library.html"] = do_inline_data(
        "library.html", writes["library.html"], "CORPUS", " = {", report)

    # The catalogue, the works, and the glossary.
    # Each file is written back in the shape it was found in: the work files
    # and the catalogue are indented, the glossary is one line. Reformatting
    # a file this pass did not change would bury the change in noise.
    jsons = {}
    for p in sorted((ROOT / "data" / "library").glob("*.json")) + \
             [ROOT / "data" / "glossary.v4.json"]:
        raw = p.read_text(encoding="utf-8")
        d = json.loads(raw)
        rel = str(p.relative_to(ROOT))
        before = len(report.get(rel, []))
        walk_fields(d, report, rel, set())
        if len(report.get(rel, [])) > before:
            jsons[rel] = (d, "\n" in raw.strip())

    # Nothing in PROTECTED may have moved. These are verses, and the pass
    # has no business inside them.
    for f, s_ in writes.items():
        for q in PROTECTED:
            if q in (ROOT / f).read_text(encoding="utf-8") and q not in s_:
                print("refusing: the pass altered Scripture quoted in %s:\n  %s"
                      % (f, q), file=sys.stderr)
                return 1

    total = sum(len(v) for v in report.values())
    for f in sorted(report):
        if not report[f]:
            continue
        from collections import Counter
        c = Counter("%s -> %s" % (a_, b_) for a_, b_ in report[f])
        print("%-34s %4d  %s" % (f, len(report[f]),
                                 ", ".join("%s x%d" % (k, n) for k, n in c.most_common(6))))
    print("%d replacements in the site's own voice" % total)

    if not a.write:
        print("(--check: nothing written)")
        return 0

    n = 0
    for f, s in writes.items():
        if (ROOT / f).read_text(encoding="utf-8") != s:
            (ROOT / f).write_text(s, encoding="utf-8")
            n += 1
    for rel, (d, indented) in jsons.items():
        text = (json.dumps(d, ensure_ascii=False, indent=1) if indented
                else json.dumps(d, ensure_ascii=False, separators=(",", ":")))
        (ROOT / rel).write_text(text + "\n", encoding="utf-8")
        n += 1
    print("written: %d files" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
