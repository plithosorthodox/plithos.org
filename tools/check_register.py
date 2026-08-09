#!/usr/bin/env python3
"""
Hold each language to its own way of naming a saint.

English has one honorific and gives it to everyone: Saint Nicholas, Saint
Sergius, Saint Anne. Most of the languages this site publishes in do not
work that way. A saint carries the title of his order - his rank - and that
title is the honorific. Russian does not say "святой Сергий"; it says
"преподобный Сергий", because Sergius was a monastic, and "святитель
Николай" for a bishop, "благоверный князь Александр" for a prince,
"праведный Симеон Богоприимец" for a righteous man. The bare word святой
stands before a rank, not before a name: "святой апостол Андрей" is right,
"святой Андрей" is the English sentence wearing Russian words.

That is a defect no spellchecker finds, because every word in it is
correctly spelled and correctly declined. It survives proofreading too: it
reads as slightly stiff rather than as wrong, and only a native ear catches
that nobody would say it. So it is checked mechanically here.

Two things are asserted.

    A rank must follow the bare honorific. Свят- may be followed by
      апостол, пророк, мученик, святитель, преподобный, праведный,
      благоверный and the rest, but not directly by a person's name.

    The monastic saint takes the monastic title. Russian преподобный,
      Ukrainian преподобний, Greek Ὅσιος, Romanian Cuviosul. This is the
      one distinction every language on the site makes and English does
      not make at all, so it is the one most often lost.

Romanian and Greek are held only to the monastic rule. Sfântul and Ἅγιος
before a name are ordinary in both, and prove nothing either way.

    python3 tools/check_register.py
    python3 tools/check_register.py --lang ru --show 20

What this cannot do is tell whether the sentence after the honorific reads
as though a native speaker wrote it. Nothing mechanical can. It closes the
one hole that is closable.
"""
import argparse
import importlib
import json
import pkgutil
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
INFO_DIR = Path(__file__).resolve().parent / "saint_info"
LIVES_DIR = Path(__file__).resolve().parent / "saint_lives"

# Which commemorations are monastic. Taken from the English rank, which the
# calendar carries for every one of them. A monastic who is also a martyr is
# a monastic here: both languages that distinguish them build the compound on
# the monastic stem (преподобномученик, Cuviosul Mucenic).
MONASTIC_WORDS = (
    "Monk", "Monastic", "Abbot", "Abbess", "Nun", "Hieromonk", "Archimandrite",
    "Schemamonk", "Hieroschemamonk", "Hermit", "Anchorite", "Stylite",
    "Recluse", "Igumen", "Monk-martyr", "Nun-martyr",
)
# "Elder" is deliberately absent: English uses it both for the monastic
# starets and for any aged man, and Eleazar the Maccabee is not a monk.
#
# Ranks that are emphatically not monastic even though the word "Monk" or a
# monastic house may appear in the title.
NOT_MONASTIC_WORDS = ("Bishop", "Archbishop", "Metropolitan", "Patriarch",
                      "Pope", "Apostle", "Prophet", "Prince", "Princess",
                      "Hierarch", "Fool-for-Christ", "Passion-bearer",
                      "Passionbearer", "Righteous", "Deaconess", "Icon")

LANGS = {
    "ru": {
        "generic": r"^\W*Свят(ой|ая|ые|ых)\b",
        "ranks": (r"апостол|пророк|мучени|преподобн|святител|праведн|"
                  r"благоверн|равноапостольн|страстотерпец|бессребреник|"
                  r"блаженн|исповедник|юродив|столпник|пустынник|затворник|"
                  r"царь|царица|князь|княгиня|игумен|игумения|архиепископ|"
                  r"епископ|митрополит|патриарх|диакон|пресвитер|иерей|"
                  r"архимандрит|схимонах|инок|монах|отшельник|дева|отроки?|"
                  r"жёны|жены|отцы|отец|праотец|богоотец|песнописец|"
                  r"земля|апостолов|обители|храм|икон|собор|праздник"),
        "monastic": r"[Пп]реподобн",
        "strict": True,
    },
    "uk": {
        "generic": r"^\W*Свят(ий|а|і|их)\b",
        "ranks": (r"апостол|пророк|мучени|преподобн|святител|праведн|"
                  r"благовірн|рівноапостольн|страстотерпец|безсрібник|"
                  r"блаженн|сповідник|юродив|стовпник|пустельник|затворник|"
                  r"цар|цариця|князь|княгиня|ігумен|архієпископ|єпископ|"
                  r"митрополит|патріарх|диякон|пресвітер|ієрей|архімандрит|"
                  r"схимонах|чернець|монах|самітник|діва|отроки?|отці|отець|"
                  r"праотець|праматір|піснописець|земля|обителі|храм|ікон|"
                  r"собор|свято"),
        "monastic": r"[Пп]реподобн",
        "strict": True,
    },
    "ro": {
        "generic": r"^\W*Sf[âa]nt(ul|a)\b",
        "ranks": (r"[Cc]uvio(s|ș|a)|[Mm]ucenic|[Aa]postol|[Pp]rooroc|[Dd]rept|"
                  r"[Bb]inecredincio|[Ff]ericit|[Ii]erarh|[Ee]gumen|[Ss]tareț|"
                  r"[Aa]rhiepiscop|[Ee]piscop|[Mm]itropolit|[Pp]atriarh|"
                  r"[Cc]neaz|[Cc]neaghin|[Îî]mpărat|[Dd]iacon|[Pp]reot|"
                  r"[Ss]tâlpnic|[Nn]ebun pentru Hristos|fără de arginți|"
                  r"[Pp]urtător de patimi|[Ss]obor|[Mm]onah|[Ss]ihastru|"
                  r"[Zz]ăvorât|[Pp]ostitor|[Mm]ironosiț|[Aa]rhimandrit|"
                  r"[Ss]chimonah|[Ff]ecioar|[Pp]raznic|[Ii]coana|[Ss]trămoș"),
        "monastic": r"[Cc]uvio(s|ș|a)",
    },
    "el": {
        "generic": r"^\W*[ὉΟ]?\s?[ἍΆΑ]γι(ος|α|οι)\b",
        "ranks": (r"[ὅὍόΌοΟ]σ[ιί]|απόστολ|Απόστολ|προφήτ|Προφήτ|μάρτυ|Μάρτυ|"
                  r"μαρτυ|ιεράρχ|Ιεράρχ|δίκαι|Δίκαι|ηγούμεν|Ηγούμεν|"
                  r"επίσκοπ|Επίσκοπ|αρχιεπίσκοπ|Αρχιεπίσκοπ|μητροπολίτ|"
                  r"πατριάρχ|Πατριάρχ|μοναχ|Μοναχ|ομολογητ|Ομολογητ|"
                  r"στυλίτ|διάκον|πρεσβύτερ|ερημίτ|εγκλειστ|βασιλ|πρίγκιπ|"
                  r"σύναξ|Σύναξ|εορτ|Εορτ|εικόν|Εικόν|παρθέν|προπάτορ"),
        "monastic": r"[ὅὍόΌοΟ]σ[ιί]",
    },
}


def english_types():
    """The English rank, and the English life beneath it.

    The rank alone is not enough. Seraphim of Sarov is filed under the bare
    word Saint, and nothing in that tells a script he was a monk - which is
    exactly the information the Slavonic and Romanian honorifics turn on. So
    the English name and life are read too: "Venerable" is English for
    Ὅσιος and преподобный and is decisive wherever it appears, and a life
    that calls its subject a monk is describing a monastic whatever the rank
    column happens to say."""
    src = PAGE.read_text(encoding="utf-8")
    i = src.index("const SAINT_INFO=")
    eq = src.index("=", i)
    j = src.index("\n", i)
    info = json.loads(src[eq + 1:j].rstrip().rstrip(";"))
    return {k: "%s || %s || %s" % (v.get("type") or "", k, v.get("life") or "")
            for k, v in info.items()}


def is_monastic(blob):
    rank = blob.split(" || ")[0]
    for w in NOT_MONASTIC_WORDS:
        if re.search(r"\b%s\b" % re.escape(w), rank):
            return False
    if re.search(r"\bVenerable\b", blob):
        return True
    if any(re.search(r"\b%s\b" % re.escape(w), rank) for w in MONASTIC_WORDS):
        return True
    # The life is consulted only where the rank column says nothing useful.
    # Almost every bishop was tonsured before his consecration, and Russian
    # still calls him святитель, so reading the life for a rank that is
    # already given would turn every hierarch into a monastic.
    if rank.split(" \u00b7 ")[0].strip() not in ("Saint", "Venerable", ""):
        return False
    return bool(re.search(r"\b(a monk|a nun|the monastic life|as a monk|"
                          r"was tonsured|received the tonsure|monastic habit|"
                          r"a hermit|an anchorite)\b", blob))


def modules(pkg, directory):
    sys.path.insert(0, str(directory.parent))
    out = {}
    for m in pkgutil.iter_modules([str(directory)]):
        mod = importlib.import_module("%s.%s" % (pkg, m.name))
        out[m.name] = dict(getattr(mod, "TEXT", {}))
    return out


def opening(text):
    return " ".join((text or "").split()[:14])


def audit(lang, entries, types, source):
    """Two findings, and the difference between them matters.

    An error is a saint introduced by the generic word for holy and nothing
    else - the English sentence in the language's words. A review is a saint
    given some other real rank than the one his order would suggest, which
    is a judgement a calendar may legitimately make and a script may not.
    """
    spec = LANGS[lang]
    generic = re.compile(spec["generic"])
    ranks = re.compile(spec["ranks"])
    monastic = re.compile(spec["monastic"])
    errors, review = [], []
    for name, value in sorted(entries.items()):
        text = value.get("life") if isinstance(value, dict) else value
        head = opening(text)
        if not head:
            continue
        m = generic.match(head)
        opens_generic = bool(m) and not ranks.search(head[m.end():m.end() + 40])
        if is_monastic(types.get(name, "")):
            if monastic.search(head):
                continue
            if opens_generic:
                errors.append(("monastic given the generic honorific",
                               source, name, head))
            else:
                review.append(("monastic named by another rank",
                               source, name, head))
            continue
        if opens_generic and spec.get("strict"):
            errors.append(("bare honorific before a name", source, name, head))
    return errors, review


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang")
    ap.add_argument("--show", type=int, default=5)
    args = ap.parse_args()

    types = english_types()
    info = modules("saint_info", INFO_DIR)
    lives = modules("saint_lives", LIVES_DIR)

    langs = [args.lang] if args.lang else sorted(set(info) | set(lives))
    total = 0
    for lang in langs:
        if lang not in LANGS:
            print("%-4s no register rules written yet" % lang)
            continue
        e1, r1 = audit(lang, info.get(lang, {}), types, "calendar")
        e2, r2 = audit(lang, lives.get(lang, {}), types, "life")
        found, soft = e1 + e2, r1 + r2
        total += len(found)
        n = len(info.get(lang, {})) + len(lives.get(lang, {}))
        print("%-4s %4d of %d openings name a saint the English way   "
              "(%d more worth a second look)" % (lang, len(found), n, len(soft)))
        kinds = {}
        for kind, src, name, head in found:
            kinds.setdefault(kind, []).append((src, name, head))
        for kind in sorted(kinds, key=lambda k: -len(kinds[k])):
            print("       %-30s %4d" % (kind, len(kinds[kind])))
            for src, name, head in kinds[kind][:args.show]:
                print("           [%s] %s" % (src, name[:60]))
                print("                %s" % head[:100])

    if total:
        print("\n%d opening(s) name a saint the way English does." % total)
        return 1
    print("\nEvery opening names the saint the way the language does.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
