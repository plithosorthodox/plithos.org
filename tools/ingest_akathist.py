#!/usr/bin/env python3
"""
The Akathist Hymn to the Most Holy Theotokos, in the languages it is sung in.

The oldest and greatest of the akathists, sung standing - which is what the
name says - on the Fridays of the Great Fast and whole on the Saturday of the
fifth week. It is of the sixth century and its author is not known, though the
Church has long named Romanos the Melodist among those it may be.

    python3 tools/ingest_akathist.py --check
    python3 tools/ingest_akathist.py --write

The shape of the hymn, which is what this verifies against

Twenty-five stanzas. A kontakion opens, then a kontakion and an oikos
alternate to the end. The oikos is the longer, carries twelve salutations
beginning Hail, and closes with the greeting to the Bride unwedded; the
kontakion is the shorter and closes with Alleluia.

The first kontakion is the exception and it is the whole difficulty: it closes
with the Bride unwedded like an oikos, not with Alleluia. So the hymn has
thirteen closings of one kind and twelve of the other, not thirteen and
thirteen, and a count of thirteen Alleluias will never be found in a sound
text. This was asserted the wrong way round once and the Greek was rejected
for being right. The two closings are the hymn's own division, they are the
same in every language, and the printed edition of 1917 - which sets the Greek
and an English verse translation on facing pages - counts them the same way.

Sources. The texts are the received ones, taken as they stand: nothing here is
rendered.

A note on where a text may be taken from. Greek Wikisource carries the
received Byzantine text under a heading that names it and no dispute attaches
to it. The Russian akathists there are a different matter: in August 2025 the
editors of that wiki listed the whole group of them for deletion as, in their
own words, a collage from internet blogs without sources, probably
self-published and a breach of copyright, and one of them had already been
described on its talk page as a Soviet reworking rather than the text of the
Triodion. None of them is used here, and a Russian text will be taken from a
printed edition or not at all.
"""
import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-akathist")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
BASE = "akathist-theotokos"

STANZAS = 25          # the whole hymn
ALLELUIA = 12         # kontakia 2 to 13
BRIDE = 13            # kontakion 1 and the twelve oikoi


def fetch(lang, page):
    # Keyed on the page as well as the language. It was keyed on the language
    # alone, and nine different akathists then came back as nine copies of the
    # first one - each dividing correctly and each reporting the same 1,654
    # words, which is the only reason it was caught.
    slug = re.sub(r"[^\w]+", "-", page, flags=re.U).strip("-")
    p = CACHE / ("%s.%s.json" % (lang, slug))
    if not p.exists():
        url = ("https://%s.wikisource.org/w/api.php?action=parse&page=%s"
               "&prop=wikitext&format=json&formatversion=2"
               % (lang, urllib.parse.quote(page)))
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=40) as r:
                    p.write_bytes(r.read())
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(15 * (attempt + 1))
        time.sleep(3)
    d = json.loads(p.read_text(encoding="utf-8"))
    if "error" in d:
        raise SystemExit("%s: %s" % (lang, d["error"].get("info")))
    return d["parse"]["wikitext"]


def strip_markup(w):
    w = re.sub(r"<noinclude>.*?</noinclude>", "", w, flags=re.S)
    w = re.sub(r"\{\{[^{}]*\}\}", "\n", w)
    w = re.sub(r"\{\{[^{}]*\}\}", "\n", w)          # nested, one level
    w = re.sub(r"\[\[(?:[^]|]*\|)?([^]]*)\]\]", r"\1", w)
    w = re.sub(r"</?poem>|</?div[^>]*>|<br\s*/?>", "\n", w)
    w = re.sub(r"'''?", "", w)
    w = re.sub(r"<[^>]+>", "", w)
    w = re.sub(r"^[=\s]*=+\s*|\s*=+\s*$", "", w, flags=re.M)
    w = re.sub(r"[ \t]+", " ", w)
    w = re.sub(r"\n{3,}", "\n\n", w)
    return w.strip()


# The two closings, which are how the hymn divides itself.
# Written loosely on purpose. The closing is not printed the same way twice:
# the kontakia give Χαῖρε Νύμφη ἀνύμφευτε without the comma and the oikoi with
# it, and the bride is capitalised in some stanzas and not in others. Each of
# those three variations, taken strictly, swallowed one stanza into the one
# before it - and the alphabet below then reported an Α and a Δ missing from a
# page that carries both. Match the words; let the printer set them as he did.
GREEK_CLOSE = re.compile(
    r"(Ἀλληλού[ιϊ]α\.?|Χαῖρε,?\s*Νύμφη [Ἀἀ]νύμφευτε\.?)")

# The heading the Greek prints over the oikoi. It belongs to the page, not to
# the first stanza, which would otherwise begin with it.
GREEK_HEADING = re.compile(r"^\s*ΟΙ ΟΙΚΟΙ\s*(?:\[[^]]*\])?\s*", re.M)

# The acrostic. The twenty-four stanzas after the opening kontakion begin with
# the letters of the Greek alphabet in order, which is the hymn's own signature
# and the one check that says WHICH stanza is missing rather than how many.
ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"


def initial(text):
    """The stanza's letter, with its breathing and accent taken off."""
    c = text.strip()[:1]
    d = unicodedata.normalize("NFD", c)
    return "".join(x for x in d if not unicodedata.combining(x)).upper()


def split_greek(w):
    """Found by the words the stanzas end with, not by how the page was typed.

    The whole hymn sits inside a centring template, so the verse is lifted out
    of it first; stripping templates before that empties the page. The service
    prints the kontakion of the Annunciation ahead of the hymn, and the hymn
    proper begins at the words to the Champion Leader."""
    poems = re.findall(r"<poem>(.*?)</poem>", w, re.S)
    body = strip_markup("\n\n".join(poems) if poems else w)
    start = body.find("Τῇ ὑπερμάχῳ")
    if start > 0:
        body = body[start:]
    body = GREEK_HEADING.sub("", body)
    pieces = GREEK_CLOSE.split(body)
    out = []
    for i in range(0, len(pieces) - 1, 2):
        text = (pieces[i] + pieces[i + 1]).strip()
        if text:
            out.append(("Ἀλληλού" in pieces[i + 1], text))
    stanzas = name_stanzas(out, "Κοντάκιον", "Οἶκος")
    check_acrostic(stanzas)
    return stanzas


def name_stanzas(pieces, kontakion, oikos):
    """Give each stanza its name and number.

    Which is which does not follow from the closing alone, because the first
    kontakion closes as an oikos does. It follows from the order, which is
    fixed: a kontakion opens the hymn and then the two alternate to the end.
    The closings are then checked against that order, so a text that alternates
    differently from the hymn is refused rather than renumbered."""
    out = []
    k = o = 0
    for n, (alleluia, text) in enumerate(pieces, 1):
        if n == 1 or n % 2 == 1:
            k += 1
            kind, num = kontakion, k
            want_alleluia = (n != 1)
        else:
            o += 1
            kind, num = oikos, o
            want_alleluia = False
        if alleluia != want_alleluia:
            raise ValueError(
                "stanza %d closes with %s; the hymn has %s there"
                % (n, "Alleluia" if alleluia else "the Bride unwedded",
                   "Alleluia" if want_alleluia else "the Bride unwedded"))
        out.append((kind, num, text))
    return out


def check_acrostic(stanzas):
    """The twenty-four after the opening kontakion spell the alphabet.

    A count alone says only that something is wrong. This says what: it names
    the letters that are absent, and a missing letter is a missing stanza. It
    applies to the Greek, where the acrostic is in the words themselves; a
    translation keeps the order of the stanzas but not their initials, so it
    is not asked of one."""
    got = [initial(t) for _k, _n, t in stanzas[1:]]
    missing = [c for c in ALPHABET if c not in set(got)]
    if missing:
        raise ValueError("the acrostic is broken; no stanza begins %s"
                         % " ".join(missing))
    if got != list(ALPHABET):
        raise ValueError("the acrostic runs %s" % " ".join(got))


# ---------------------------------------------------------------------------
# The English of 1919.
#
# "The Akathist Hymn and Little Compline", London, 1919: the Greek and an
# English prose rendering on facing pages, arranged as the service is sung,
# with the Priest's part and the Choir's answer marked. It is out of copyright
# by any measure, and it is a published translation rather than one made here,
# which is what a liturgical text on this shelf has to be.
#
# The translators built an acrostic of their own to stand for the Greek one:
# the twenty-four stanzas after the opening kontakion begin A B C D E F G H I
# K L M N O P Q R S T U V W Y Z - the twenty-four letter Latin alphabet, J and
# X omitted, as the Greek has twenty-four. So the same check applies to the
# English as to the Greek, and it is the translators' device, not one imposed
# on them.
ARCHIVE = "akathisthymnlitt00londuoft"
ENGLISH_ACROSTIC = "ABCDEFGHIKLMNOPQRSTUVWYZ"

# The two closings as the scan may have mangled them, with everything that
# leads into them, so a stanza ends where the book ends it.
ENGLISH_CLOSE = re.compile(
    r"Alleluia|(?:Hail[^A-Za-z]{0,3}\s*)?(?:thou[^A-Za-z]{0,3}\s*)?Bride[^A-Za-z]{0,3}\s*unwedded")

# What the scan misread, what the page reads, and where to look.
#
# Every one of these is a place where the Greek of the facing page printed
# through onto the English and the scanner read the ghost instead of the
# letters under it. Each was settled by reading the page itself, and the page
# is named so that anyone can check it. Nothing here is conjecture: where the
# page could not be read, the text would not be published.
REPAIRS = [
    # p. 18-19
    ("how speakest thou of a a Se Fe virgin", "how speakest thou of a virgin"),
    # p. 19
    ("for a Son tobe born", "for a Son to be born"),
    ("hail, Bridge ening from earth to", "hail, Bridge leading from earth to"),
    ("from earth to n dven", "from earth to heaven."),
    # p. 20
    ("marvel and wonder ey of Angels", "marvel and wonder of Angels"),
    ("completer of His ordinances,", "completer of His ordinances."),
    ("from earth to heaven.:", "from earth to heaven."),
    ("cause of wailing in Demons,", "cause of wailing in Demons."),
    # p. 21
    ("Enshrinings-God in her womb", "Enshrining God in her womb"),
    ("whose unborn babe once recognised",
     "whose unborn babe at once recognised"),
    ("hail, Oblation for all the world,", "hail, Oblation for all the world."),
    # p. 22, the printer's signature mark caught between two sentences
    ("Favour of .God to mortals", "Favour of God to mortals"),
    ("Access of mortals to God. A Hail, thou Bride",
     "Access of mortals to God. Hail, thou Bride"),
    ("when he learnt of thy con through the Holy Ghost",
     "when he learnt of thy conception through the Holy Ghost"),
    # p. 26
    ("ascribe thankofferings", "ascribe thank-offerings"),
    ("for thou, O.Mother of God", "for thou, O Mother of God"),
    ("so that to thee I may cry.:", "so that to thee I may cry:"),
    # p. 27-28: the Greek of the facing page came through and was read as
    # English letters. The sentences on either side meet.
    ("Gates of Paradise. : Hail,", "Gates of Paradise. Hail,"),
    ("courage of the Champions, Hail,", "courage of the Champions. Hail,"),
    # p. 29
    ("Hail, never-silent. Voice", "Hail, never-silent Voice"),
    ("showest forth the. Lord", "showest forth the Lord"),
    ("Hail, thou who, quenchest", "Hail, thou who quenchest"),
    ("out the inhuman, tyrant of old", "out the inhuman tyrant of old"),
    ("thou who sedeuiiinat eck the creeds",
     "thou who redeemest from the creeds"),
    ("thou who madest, the worship", "thou who madest the worship"),
    # p. 29-30
    ("to be allayed. . Hail, Guide the wisdom the faithful",
     "to be allayed. Hail, Guide of the wisdom of the faithful"),
    # p. 30
    ("became, when they: -returned", "became, when they returned"),
    ("preached Thee as the: Christ", "preached Thee as the Christ"),
    ("and they left: Herod", "and they left Herod"),
    ("who knew not to ei Alleluia", "who knew not how to cry: Alleluia"),
    # p. 31
    ("hail, downfall of demens", "hail, downfall of demons"),
    ("tramplest upon nthe wanderings", "tramplest upon the wanderings"),
    ("refutest the lies of Hail, Sea which drowned",
     "refutest the lies of idols. Hail, Sea which drowned"),
    ("hail, EBA of . holy joy", "hail, messenger of holy joy."),
    # p. 32
    ("Marvelling at: Thine", "Marvelling at Thine"),
    ("ineffable wisdom when; Thou wast", "ineffable wisdom when Thou wast"),
    ("presented to-him", "presented to him"),
    ("nearing his time departure", "nearing his time of departure"),
    ("from this .age.. of, error", "from this age of error"),
    ("as perfect God, ane he cried", "as perfect God, and he cried"),
    ("and he cried ; Alleluia", "and he cried: Alleluia"),
    ("from this age of error; recognised", "from this age of error, recognised"),
    ("great deed of. Incarnation", "great deed of Incarnation"),
    # p. 38-40
    ("New was the Creation heen the Creator",
     "New was the Creation which the Creator"),
    ("He appeared born from the womb a Virgin",
     "He appeared born from the womb of a Virgin"),
    ("forgiveness for many transgressors, Hail, Robe",
     "forgiveness for many transgressors. Hail, Robe"),
    ("Hail, Robe of boldnessfor thenaked",
     "Hail, Robe of boldness for the naked"),
    # p. 40-41
    ("the Uncircumscribed Word yet in no way",
     "the Uncircumscribed Word, yet in no way"),
    ("hail, undoubting Boast the faithful",
     "hail, undoubting Boast of the faithful"),
    ("hail, allglorious Chair", "hail, all-glorious Chair"),
    # p. 42-43
    ("marvel at this mysterv", "marvel at this mystery"),
    ("Hail thou that showest philosophers fools ;..hail",
     "Hail, thou that showest philosophers fools ; hail"),
    ("hearing from all: Alleluia Alleluia", "hearing from all: Alleluia"),
    # p. 44
    ("world, and for this; by His own will", "world, and for this, by His own will"),
    # p. 54
    ("to those in darkness for she kindles",
     "to those in darkness : for she kindles"),
    ("Ray of the Living Sun hail, Flash", "Ray of the Living Sun : hail, Flash"),
    # p. 55-56
    ("of all men, would a grant grace", "of all men, would grant grace"),
    ("inexhaustible treasury of Life a, Hail",
     "inexhaustible treasury of Life. Hail"),
]


def fetch_archive(item):
    """The scan's text with its pages and lines still in it.

    The flat transcript is not used. It has thrown the lines away, and the line
    is what tells a hyphen that breaks a word across two of them from a hyphen
    the printer set: rejoining every one of them turned thank-offerings into
    thankofferings and Corn-land into Cornland. The page-level file keeps both,
    so each hyphen is read as what it is."""
    p = CACHE / (item + ".xml")
    if not p.exists():
        url = "https://archive.org/download/%s/%s_djvu.xml" % (item, item)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=300) as r:
            p.write_bytes(r.read())
    return p.read_text(encoding="utf-8", errors="replace")


LINE_RE = re.compile(r"<LINE\b[^>]*>(.*?)</LINE>", re.S)
WORD_RE = re.compile(r"<WORD[^>]*>([^<]*)</WORD>")


def page_text(page):
    """One page, its lines rejoined as the printer set them.

    A line holding nothing but a number is the page number, and a line holding
    one or two letters at the foot is the printer's signature mark; neither is
    part of the text. A word broken at the end of a line is put back together
    without its hyphen; a hyphen anywhere else is the printer's and stays."""
    lines = []
    for m in LINE_RE.finditer(page):
        words = [w for w in WORD_RE.findall(m.group(1)) if w.strip()]
        if not words:
            continue
        line = " ".join(words).strip()
        if re.fullmatch(r"[\d\W]{1,6}|[A-Za-z]{1,2}\d?", line):
            continue
        lines.append(line)
    out = []
    for line in lines:
        if out and out[-1].endswith("-"):
            out[-1] = out[-1][:-1] + line.split(" ", 1)[0]
            rest = line.split(" ", 1)[1:]
            if rest:
                out.append(rest[0])
        else:
            out.append(line)
    return " ".join(out)


def english_pages(xml):
    """The English half. The book sets the Greek and the English on facing
    pages, so a page is one or the other."""
    out = []
    for page in re.split(r"<OBJECT\b", xml)[1:]:
        t = page_text(page)
        greek = sum(1 for c in t if "GREEK" in unicodedata.name(c, ""))
        latin = sum(1 for c in t if c.isascii() and c.isalpha())
        if latin > greek and len(t) > 200:
            out.append(t)
    return out


def english_clean(s):
    """Undo what the scanner did, and nothing else.

    Line-end hyphens rejoined, the Greek that printed through from the facing
    page taken out, page numbers and signature marks dropped. The printer's own
    spacing before semicolons is left alone: that is how the book is set."""
    s = re.sub(r"\s+", " ", s)
    s = "".join(" " if "GREEK" in unicodedata.name(c, "") else c for c in s)
    s = s.replace("\u00bb", " ").replace("\u00ab", " ").replace("_", " ")
    s = re.sub(r"[\u2018\u2019]", "'", s)
    s = re.sub(r"[\u201c\u201d]", '"', s)
    s = re.sub(r"[^\x00-\x7f]", " ", s)
    s = re.sub(r"(?<![\w'])\d{1,3}(?![\w'])", " ", s)
    s = re.sub(r"[<>\\|~^*]", " ", s)
    # Punctuation the scanner saw in the ghost of the facing page and the
    # printed page does not have. A sentence in this book never opens with a
    # small letter, so a full stop before one was never set; the same goes for
    # a quotation mark with white space on both sides of it, and for an
    # ellipsis, which the hymn itself never uses.
    s = re.sub(r"&[a-z]+;", " ", s)
    # A stop, a colon or a comma that the scanner found in the ghost of the
    # facing page. No sentence in this book opens with a small letter and no
    # word is broken by a stop, so each of these marks a place where the page
    # has none. The printer's own spacing before a semicolon is left alone:
    # that is how the book is set.
    s = re.sub(r"\s*\.\s*\.\s*\.+\s*", " ", s)
    s = re.sub(r"([a-z]),?\.\s*(?=[a-z])", r"\1 ", s)
    s = re.sub(r"([A-Za-z]):\s*(?=[a-z])", r"\1 ", s)
    s = re.sub(r"\bhail;", "hail,", s)
    s = re.sub(r"(?<![A-Za-z])'|'(?![A-Za-z])", " ", s)
    s = re.sub(r"\s*-\s+(?=[a-z])", " ", s)
    s = re.sub(r",\s*\.", ",", s)
    s = re.sub(r"\s+([;:,.?!])", r" \1", s)
    s = re.sub(r"([,;:])(?=[A-Za-z])", r"\1 ", s)
    # The dropped capital that opens a stanza is set apart from the word it
    # begins and the scan reads the gap as a space: F loods. Only at the head,
    # or the rule closes up I may cry into Imay cry.
    s = re.sub(r"^([A-Z]) ([a-z]{2,})", r"\1\2", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip(" .,:;'\"-")


def split_english(txt):
    eng = " ".join(english_pages(txt))
    blocks = re.split(r"\s*\b(?:Priest|Choir)\s*[.,!:]\s*", eng)
    stanzas = []
    for b in blocks:
        t = english_clean(b)
        # A kontakion runs to about forty words and an oikos to about a
        # hundred and forty. Anything far outside that is not a stanza: where
        # the scan lost a speaker's name, whole pages of the Canon ran together
        # into one block, and one of them began with an A and was taken for the
        # first oikos.
        if not 25 <= len(t.split()) <= 200:
            continue
        # A stanza ends at its closing. What follows on the page - the choir's
        # answer, a catchword, the printer's signature mark - is not part of
        # it, and the scan runs it on.
        #
        # The closing has to be matched loosely, for the same reason as in the
        # Greek: the ghost of the facing page falls across it and the scanner
        # reads punctuation that is not there. Bride: unwedded, Bride'unwedded
        # and thou. Bride. unwedded are all one line of type, and requiring it
        # clean lost three stanzas. The words are matched; what the closing is
        # then written as is what the book prints.
        ms = list(ENGLISH_CLOSE.finditer(t))
        if not ms:
            continue
        m = ms[-1]
        alleluia = m.group(0).startswith("Alleluia")
        head = t[:m.start()]
        # The choir's answer repeats the closing, and where the scan lost the
        # marker between them the stanza runs on into it.
        head = re.sub(r"[\s.,:;]*Choirs?[\s.,:;]*$", " ", head)
        t = head + ("Alleluia." if alleluia
                    else "Hail, thou Bride unwedded.")
        stanzas.append(re.sub(r"\s+", " ", t).strip())

    opening = next((t for t in stanzas if t.startswith("To thee, the Champion")),
                   None)
    if opening is None:
        raise ValueError("the opening kontakion was not found")

    # Take the acrostic stanzas in order, each one having to begin with the
    # letter the alphabet is up to. A stanza out of order is a stanza this has
    # not understood, and it stops rather than guessing.
    want = list(ENGLISH_ACROSTIC)
    body = []
    for t in stanzas:
        if want and t[:1].upper() == want[0]:
            body.append(t)
            want.pop(0)
    if want:
        raise ValueError("no stanza begins %s" % " ".join(want))

    fired = set()
    stanzas = [repair(t, fired) for t in [opening] + body]
    missed = [bad for bad, _good in REPAIRS if bad not in fired]
    if missed:
        raise ValueError("%d repair(s) found nothing to repair, so the scan is "
                         "not the one they were read against: %s"
                         % (len(missed), missed[0]))
    return name_stanzas([(t.endswith("Alleluia."), t) for t in stanzas],
                        "Kontakion", "Oikos")


def repair(t, fired):
    """Put back what the facing page's ghost took out.

    Every replacement here was read off the page it is filed under, in the
    scan's own images. None of it is conjecture: where a page could not be
    read the text would not be published. The caller checks that every one of
    them found its place, so a scan that changes underneath this is caught
    rather than silently half-applied."""
    for bad, good in REPAIRS:
        if bad in t:
            fired.add(bad)
            t = t.replace(bad, good)
    return t


LANGS = [
    {
        "lang": "el", "wiki": "el", "page": "Ακάθιστος ύμνος",
        "split": split_greek,
        "title": "The Akathist Hymn to the Most Holy Theotokos (Greek)",
        "source": "Received Greek text of the Orthodox Church",
        "date": "6th century",
        "translator": None,
        "pub_year": None,
        "digitized": "Wikisource",
    },
    {
        "lang": "en", "archive": ARCHIVE, "split": split_english,
        "title": "The Akathist Hymn to the Most Holy Theotokos (English)",
        "source": ("The Akathist Hymn and Little Compline, London: Longmans, "
                   "Green and Co., 1919"),
        "date": "6th century; this rendering 1919",
        "translator": "The edition of 1919",
        "pub_year": 1919,
        "digitized": "Internet Archive",
    },
]

COMMON = ("Sung standing, which is what its name says, on the Fridays of the "
          "Great Fast and whole on the Saturday of the fifth week. Twenty-four "
          "stanzas whose first letters run through the alphabet, and a hundred "
          "and forty-four salutations beginning Hail, each one addressed to "
          "the Mother of God, with a kontakion before them and a thirteenth at "
          "the end. It is of the sixth century; the Church has long named "
          "Romanos the Melodist among those who may have written it, and does "
          "not say so certainly. ")

DESC = {
    "el": COMMON + "This is the Greek, which is the original.",
    "en": COMMON + (
        "This is the English of the edition published at London in 1919, "
        "which sets the Greek and the English on facing pages and arranges "
        "both as the service is sung, with the priest's part and the choir's "
        "answer marked. Its translators built an alphabet of their own to "
        "stand where the Greek has one: the twenty-four stanzas open A to Z, "
        "J and X passed over so that the count comes out the same."),
}


def build(spec):
    if "archive" in spec:
        w = fetch_archive(spec["archive"])
    else:
        w = fetch(spec["wiki"], spec["page"])
    try:
        got = spec["split"](w)
    except ValueError as e:
        return None, str(e)
    if len(got) != STANZAS:
        return None, "%d stanzas, expected %d" % (len(got), STANZAS)
    wid = "%s-%s" % (BASE, spec["lang"])
    units = []
    for n, (kind, num, text) in enumerate(got, 1):
        if not text.strip():
            return None, "stanza %d is empty" % n
        units.append({
            "unit_id": "%s::u%03d" % (wid, n),
            "work_id": wid,
            "work_title": spec["title"],
            "author": "Anonymous, of the sixth century",
            "source_class": "liturgical",
            "ordinal": n,
            "citation_anchor": "%s %d" % (kind, num),
            "chapter_title": None,
            "text": text,
        })
    return units, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.write or a.check):
        a.check = True

    built, failed = [], []
    for spec in LANGS:
        units, err = build(spec)
        if err:
            failed.append(spec["lang"])
            print("  FAIL  %-4s %s" % (spec["lang"], err))
            continue
        words = sum(len(u["text"].split()) for u in units)
        bad = sum(len(re.findall(r"[–—]", u["text"])) for u in units)
        print("  ok    %-4s %2d stanzas  %6s words  %d dashes"
              % (spec["lang"], len(units), format(words, ","), bad))
        built.append((spec, units))

    # A language that verifies is published; one that does not is named and
    # left out. The hymn is fixed in shape, so a text that will not divide
    # into it is a text this has not understood, and a liturgical text is the
    # last thing to guess at.
    if failed:
        print("\n  not published: %s" % ", ".join(failed))

    if a.write:
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        for spec, units in built:
            wid = "%s-%s" % (BASE, spec["lang"])
            meta = {
                "work_id": wid,
                "edition_of": BASE,
                "title": spec["title"],
                "author": "Anonymous, of the sixth century",
                "language": spec["lang"],
                "date": spec["date"],
                "translator": spec["translator"],
                "pub_year": spec["pub_year"],
                "source": spec["source"],
                "source_class": "liturgical",
                "description": DESC[spec["lang"]],
                "digitized": spec["digitized"],
                "license": "Public Domain",
                "saint": None,
                "is_saint": False,
            }
            OUTDIR.joinpath(wid + ".json").write_text(
                json.dumps({"work": meta, "units": units},
                           ensure_ascii=False, indent=1), encoding="utf-8")
            cat = [x for x in cat if x["work_id"] != wid]
            cat.append(meta)
        cat.sort(key=lambda x: x["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %d edition(s) and updated the catalogue" % len(built))
    elif not a.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
