#!/usr/bin/env python3
"""Publish the 1895 Constantinople encyclical from its bilingual edition.

The source is the edition prepared by Archimandrite Eustathius Metallinos,
published for the Orthodox Greek Community in Manchester in 1896, with the
authorized Greek text and Metallinos's English translation on facing pages.
The English was revised for publication by Henry Ramsden Bramley.

Internet Archive item:
    https://archive.org/details/answerofgreatchu0000eust

The archive's OCR is read by page, never trusted as a free-standing modern
transcription.  Every correction below is an error visible in that OCR and
checked against the printed page.  Typography alone is normalized to the
house style: straight quotes and hyphens in place of typographic dashes.

    python tools/ingest_1895_encyclical.py --check
    python tools/ingest_1895_encyclical.py --write-files-only
"""
import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-1895-encyclical")
CACHE.mkdir(parents=True, exist_ok=True)

ITEM = "answerofgreatchu0000eust"
XML_NAME = ITEM + "_djvu.xml"
SOURCE_URL = "https://archive.org/details/" + ITEM
XML_URL = "https://archive.org/download/%s/%s" % (ITEM, XML_NAME)
XML_SHA256 = "02a6f6a6e6c746fc02dd633c83c329ca764be0ef8c1e857b4cefc3364e6b8036"
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"

WORK_ID = "patriarchal-encyclical-1895-en"
BASE_ID = "patriarchal-encyclical-1895"

# One-indexed leaf numbers in the Internet Archive object.  The book prints
# Greek on the left and English on the right.  The English preface begins at
# leaf 13 and the signatures end at leaf 71.
ENGLISH_PAGES = tuple(range(13, 72, 2))

# OCR errors checked against the page images.  These are not editorial
# alterations to the edition.  The assertions below require every repair to
# fire, so a changed OCR source cannot silently bypass this review.
REPAIRS = [
    ('"Remember them which', "'Remember them which"),
    ("Be not earried", "Be not carried"),
    ("{'Remember them that", "['Remember them that"),
    ("and ther sacred", "and their sacred"),
    ("I, Every", "I. Every"),
    ("make havoe", "make havoc"),
    ("Ill. No doubt", "III. No doubt"),
    ("he is lable", "he is liable"),
    ("impartia] judgement-seat", "impartial judgement-seat"),
    ("Phot. Lpist.", "Phot. Epist."),
    ("or do not hold it", "or does not hold it"),
    ("searcely forty", "scarcely forty"),
    ("universal Chureh", "universal Church"),
    ("Eneyclical", "Encyclical"),
    ("a manifest e1ror", "a manifest error"),
    ("knows wel]", "knows well"),
    ("those provinees", "those provinces"),
    ("catholie and orthodox", "catholic and orthodox"),
    ("Mpcccxcy", "MDCCCXCV"),
    ("divine purpose\n\n| of the establishment", "divine purpose of the establishment"),
    ("chief corner stone.'", "chief corner stone 1.'"),
    ("our Lord Jesus Christ *.", "our Lord Jesus Christ 2."),
    ("? Eph. ii. 20. 2 John xiv. 6.", "1 Eph. ii. 20. 2 John xiv. 6."),
    ("transformed into apostles of Christ 4,", "transformed into apostles of Christ 1,"),
    ("affairs of others *.'", "affairs of others 2.'"),
    ("ta Cor, Xl. 53. 2 Phot. Epist. iil. § 10. C2",
     "1 2 Cor. xi. 13. 2 Phot. Epist. iii. § 10."),
    ("in you all 35%", "in you all 1.'"),
    ("(Haec Leo posui amore et cautela fidei orthodoxae) ®.",
     "(Haec Leo posui amore et cautela fidei orthodoxae) 2."),
    ("-LEpist. v. § 3.", "-Epist. v. § 3."),
    ("sound faith?'", "sound faith 2.'"),
    ("Peo uMimierieet 4 eee luna: vil 20) 2 St. Basil the Great, Zp. 243, To the Bishops of Italy and Gaul.",
     "1 2 Tim. i. 14; 1 Tim. vi. 20. 2 St. Basil the Great, Ep. 243, To the Bishops of Italy and Gaul."),
    ("for this © is my blood?", "for this is my blood 1.'"),
    ("' Drink ye all of it?'", "' Drink ye all of it 2,'"),
    ("1 Matt. xxvi, 26-28. 2 Matt. xxvi. 28.",
     "1 Matt. xxvi. 26-28. 2 Matt. xxvi. 28."),
    ("'which are fallen asleep in the Lord'!';",
     "'which are fallen asleep in the Lord 1';"),
    ("1 Matt. xxvi 31; Heb. xi. 39; 2 Tim. iv. 8; 2 Mace. xii, 48. D2",
     "1 Matt. xxvi. 31; Heb. xi. 39; 2 Tim. iv. 8; 2 Macc. xii. 48."),
    ("supreme authority and _ infallible", "supreme authority and infallible"),
    ("the body, the Church ','", "the body, the Church 1,'"),
    ("the end of the world*.", "the end of the world 2.'"),
    ("Epistle to the Galatians *.", "Epistle to the Galatians 3."),
    ("upon this rock I will build my Church',", "upon this rock I will build my Church 4,'"),
    ("Cola, 13: 2 Matt. xxviii. 20. 3 Gal. ii. BT. * Matt. xvi. 18.",
     "1 Col. i. 18. 2 Matt. xxviii. 20. 3 Gal. ii. 11. 4 Matt. xvi. 18."),
    ("the Son of the living God!\"", "the Son of the living God 1.'"),
    ("which is Jesus Christ.'", "which is Jesus Christ 2.'"),
    ("which is the Church?;", "which is the Church 3;"),
    ("chief corner stone*.'", "chief corner stone 4.'"),
    ("? Matt. xvi. 16. 2p Cou piiie LOT. Se Colmrees. 4 Eph. ii. 19, 20. Cp.1 Pet. ii. 4; Rev. xxi. 14.",
     "1 Matt. xvi. 16. 2 1 Cor. iii. 10, 11. 3 Col. i. 24. 4 Eph. ii. 19, 20. Cp. 1 Pet. ii. 4; Rev. xxi. 14."),
    ("well known to all?.", "well known to all 1."),
    ("case of Marcellus!", "case of Marcellus 1.'"),
    ("truth of the Gospel!.", "truth of the Gospel 1.\n\n1 Gal. ii. 11."),
    ("retains till this E 2\n\nvery day", "retains till this very day"),
    ("the pillar and ground of the truth!' ;",
     "the pillar and ground of the truth 1';\n\n1 1 Tim. iii. 15."),
    ("Christ it is impossible to please God?;'",
     "Christ it is impossible to please God 2;'"),
    ("wd Were able ag 2 Heb. xi. 6.", "1 1 Tim. iii. 15. 2 Heb. xi. 6."),
    ("for ever '.'", "for ever 1.'"),
    ("following universality, antiquity, and consent*.'",
     "following universality, antiquity, and consent 2.'"),
    ('"Tn ipsa item catholica Ecclesia', "'In ipsa item catholica Ecclesia"),
    ("Sed hoe fiet", "Sed hoc fiet"),
    ("(Vincentil Lirinensis", "(Vincentii Lirinensis"),
    ("cap. ili. ef. cap. viii.", "cap. iii. cf. cap. viii."),
    ("whether by word, or our epistle*;'", "whether by word, or our epistle 1;'"),
    ("would pervert the gospel of Christ?'", "would pervert the gospel of Christ 2.'"),
    ("fair speeches deceive the hearts of the simple*;'",
     "fair speeches deceive the hearts of the simple 3;'"),
    ("1 5 Thess. ii. 15. 2 Gal. i. 6. 3 Rom. xvi. 18.",
     "1 1 Thess. ii. 15. 2 Gal. i. 6. 3 Rom. xvi. 18."),
    ("65 of Christ", "of Christ"),
    ("His own blood!)", "His own blood 1,'"),
    ('edify one another*."', "edify one another 2.'"),
    ("strengthen, settle us*,", "strengthen, settle us 3,'"),
    ("grant that , all those", "grant that all those"),
    ("' Acts xx. 28. 2 1 Thess. v. Il. $ x Pet. v. Io. F",
     "1 Acts xx. 28. 2 1 Thess. v. 11. 3 1 Pet. v. 10."),
    ("JEROME of Nicaea. beloved", "JEROME of Nicaea, beloved"),
    # The OCR read the cross before signatures as several stray symbols.
    ('%" ANTHIMUS', "ANTHIMUS"),
    ('%" NICODEMUS', "NICODEMUS"),
    ('%" PHILOTHEUS', "PHILOTHEUS"),
    ("% JEROME", "JEROME"),
    ("% NATHANAEL", "NATHANAEL"),
    ("% BASIL", "BASIL"),
    ("% STEPHEN", "STEPHEN"),
    ("y% ATHANASIUS", "ATHANASIUS"),
    ("% BESSARION", "BESSARION"),
    ("% DOROTHEUS", "DOROTHEUS"),
    ("% SOPHRONIUS", "SOPHRONIUS"),
    ('%" DIONYSIUS', "DIONYSIUS"),
]

# Words which the compositor hyphenated and which must keep their hyphen
# after line-end hyphenation is removed.
COMPOUNDS = (
    "all-sacred", "anti-evangelical", "divinely-beloved",
    "divinely-transmitted", "English-speaking", "empty-mindedness",
    "God-bearing", "God-man", "head-covering", "highly-to-be-praised",
    "Most Blessed", "only-begotten", "right-thinking", "self-administered",
    "self-contradiction", "self-evident", "self-governing",
)


def fetch():
    path = CACHE / XML_NAME
    if not path.exists():
        request = urllib.request.Request(XML_URL, headers={"User-Agent": UA})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    path.write_bytes(response.read())
                break
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(5 * (attempt + 1))
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if XML_SHA256 and digest != XML_SHA256:
        raise ValueError("source digest %s, expected %s" % (digest, XML_SHA256))
    return raw, digest


def line_text(line):
    words = []
    for word in line.findall(".//WORD"):
        text = "".join(word.itertext()).strip()
        if text:
            words.append(text)
    return " ".join(words)


def join_lines(lines):
    """Join printed lines and remove only their mechanical hyphenation."""
    out = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not out:
            out = line
        elif out.endswith("-") and re.match(r"^[a-z]", line):
            out = out[:-1] + line
        else:
            out += " " + line
    return out


def extract_paragraphs(raw):
    root = ET.fromstring(raw)
    objects = root.findall(".//OBJECT")
    if len(objects) != 76:
        raise ValueError("%d source leaves, expected 76" % len(objects))
    paragraphs = []
    for page in ENGLISH_PAGES:
        obj = objects[page - 1]
        for para in obj.findall(".//PARAGRAPH"):
            lines = [line_text(line) for line in para.findall(".//LINE")]
            text = join_lines([x for x in lines if x])
            if text:
                paragraphs.append(text)
    return paragraphs


def clean(paragraphs):
    text = "\n\n".join(paragraphs)
    text = text.translate({
        0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
        0x00AB: '"', 0x00BB: '"', 0x2013: "-", 0x2014: "-",
        0x00A0: " ",
    })

    # Running page numbers, printer's signatures, and three OCR fragments in
    # the lower margin.  They are page furniture, not words of the edition.
    drops = {
        "15", "21", "25", "30", "31", "35", "39", "41", "43", "45",
        "49", "51", "53", "55", "57", "59", "61", "63", "65", "67",
        "C2", "D", "E", "E 2", "F", "aT", "a3", "oS)", "oS", "Os)", "=)",
        "2I", "3)",
        "=", "|", "iedl", "ey Oe Cae ee]", "Peo uMimierieet 4 eee luna: vil 20)",
        "WiGalsiie cr.", "reli Vis 05.", "wd Were able ag",
    }
    text = "\n\n".join(p for p in text.split("\n\n") if p.strip() not in drops)

    # Restore the few printed compounds whose hyphen occupied a line end.
    for compound in COMPOUNDS:
        plain = compound.replace("-", "")
        text = re.sub(r"\b%s\b" % re.escape(plain), compound, text,
                      flags=re.I)

    fired = set()
    for bad, good in REPAIRS:
        if bad in text:
            fired.add(bad)
            text = text.replace(bad, good)
    missed = [bad for bad, _good in REPAIRS if bad not in fired]
    if missed:
        raise ValueError("%d OCR repairs did not fire: %s" %
                         (len(missed), missed[0]))

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n\n *", "\n\n", text).strip()
    return text


def split_units(text):
    # The Preface and the address with Hebrews precede the numbered letter.
    start = text.find("PATRIARCHAL AND SYNODICAL LETTER")
    first = text.find("I. Every", start)
    signatures = text.find("In the Patriarchal Palace of Constantinople")
    if min(start, first, signatures) < 0:
        raise ValueError("the preface, letter, or signatures were not found")
    preface = text[:start].strip()
    address = text[start:first].strip()
    body = text[first:signatures].strip()
    ending = text[signatures:].strip()

    marks = list(re.finditer(
        r"(?<![A-Za-z])(?:XXV|XXIV|XXIII|XXII|XXI|XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\. ",
        body))
    if len(marks) != 25:
        raise ValueError("%d numbered sections, expected 25" % len(marks))
    roman = [m.group(0).strip(". ") for m in marks]
    expected = [
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
        "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV",
    ]
    if roman != expected:
        raise ValueError("section order is %s" % ", ".join(roman))

    units = [("Preface", preface), ("Address", address)]
    for n, mark in enumerate(marks):
        stop = marks[n + 1].start() if n + 1 < len(marks) else len(body)
        units.append(("Section " + roman[n], body[mark.start():stop].strip()))
    units.append(("Signatures", ending))
    return units


def build():
    raw, digest = fetch()
    text = clean(extract_paragraphs(raw))
    divisions = split_units(text)
    if len(divisions) != 28:
        raise ValueError("%d divisions, expected 28" % len(divisions))
    if "ANTHIMUS of Constantinople" not in divisions[-1][1]:
        raise ValueError("the Patriarch's signature is absent")
    if "DIONYSIUS of Eleutheropolis" not in divisions[-1][1]:
        raise ValueError("the last synodal signature is absent")
    if re.search(r"[\u2013\u2014\u2018\u2019\u201c\u201d]", text):
        raise ValueError("typographic dash or curly quote remains")

    title = "Answer of the Great Church of Constantinople to the Papal Encyclical on Union (English)"
    author = "The Great Church of Constantinople, Patriarch Anthimus VII and the Holy Synod"
    work = {
        "work_id": WORK_ID,
        "edition_of": BASE_ID,
        "title": title,
        "author": author,
        "language": "en",
        "date": "1895",
        "translator": "Archimandrite Eustathius Metallinos; revised by Henry Ramsden Bramley",
        "pub_year": 1896,
        "publisher": "Orthodox Greek Community of Manchester; printed at Oxford by Horace Hart",
        "source": "Answer of the Great Church of Constantinople to the Papal Encyclical on Union, 1896",
        "source_url": SOURCE_URL,
        "source_class": "conciliar",
        "description": (
            "The Patriarchal and Synodical reply of Constantinople to Pope Leo XIII's appeal for reunion. "
            "It states the Eastern Orthodox objections concerning the Creed, baptism, the Eucharist, "
            "the papacy, and the conciliar order of the Church. This is a primary Orthodox document of "
            "1895, not a neutral history of the division. The English is the translation published beside "
            "the authorized Greek text in 1896. The wording is preserved; straight quotes and hyphens "
            "replace the edition's typographic quotes and dash."
        ),
        "digitized": "Internet Archive",
        "license": "Public Domain",
        "rights_url": SOURCE_URL,
        "saint": None,
        "is_saint": False,
    }
    units = []
    for ordinal, (anchor, unit_text) in enumerate(divisions, 1):
        units.append({
            "unit_id": "%s::u%03d" % (WORK_ID, ordinal),
            "work_id": WORK_ID,
            "work_title": title,
            "author": author,
            "source_class": "conciliar",
            "ordinal": ordinal,
            "citation_anchor": anchor,
            "chapter_title": None,
            "text": unit_text,
        })
    return {"work": work, "units": units}, digest


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--write-files-only", action="store_true")
    args = parser.parse_args()

    payload, digest = build()
    chars = sum(len(unit["text"]) for unit in payload["units"])
    print("ok %s: %d divisions, %s characters, source sha256 %s" %
          (WORK_ID, len(payload["units"]), format(chars, ","), digest))
    path = OUTDIR / (WORK_ID + ".json")
    body = json.dumps(payload, ensure_ascii=False, indent=1) + "\n"
    if args.write or args.write_files_only:
        path.write_text(body, encoding="utf-8")
        print("wrote %s" % path.relative_to(ROOT))
    elif not path.exists() or path.read_text(encoding="utf-8") != body:
        print("stale or missing %s" % path.relative_to(ROOT))
        return 1
    if args.write:
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        index = [item for item in index if item.get("work_id") != WORK_ID]
        index.append(payload["work"])
        index.sort(key=lambda item: item["work_id"])
        INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")
        print("updated %s" % INDEX.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
