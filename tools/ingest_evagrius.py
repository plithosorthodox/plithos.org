#!/usr/bin/env python3
"""Stage Walford's complete English Evagrius without publishing it.

Roger Pearse's Tertullian.org transcription reproduces Edward Walford's
1846 translation book by book and marks the whole text public domain. This
builder pins every source page, keeps the preface, all 173 chapters, and all
55 notes, removes only scan page furniture, and writes the individual Library
JSON file. It does not change the catalogue, search data, or reader page.

The source page for Book V omits the Chapter V heading and prints Chapter
XIII as "CHAPTER X" in its HTML. The table of contents on the same site has
both headings. The two structural repairs below are asserted against the
pinned source and do not alter the chapter text.

    python tools/ingest_evagrius.py --check
    python tools/ingest_evagrius.py --write-files-only
"""
import argparse
import hashlib
import html
import json
import re
import sys
import tempfile
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path(tempfile.gettempdir()) / "plithos-evagrius"
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
BASE_URL = "https://www.tertullian.org/fathers/"
TOC_NAME = "evagrius_0_toc.htm"
TOC_SHA256 = "b095d03c4ef1b7fe6ef7a9f70dc182d5821241989f40efa36865102494a8b8cf"
BOOK_SHA256 = (
    "cd400502d3df81f3e72d99830129c4b2a7b32c2f6f0579f8c7197ac2fc592b24",
    "5b3e42d0c66f50e79a28ba3599449775ee5251a80d80285c77d0bff588db4e05",
    "3b561a283e56747bcd955f40a9efa9298aa9a9751190ef6e26e5e3a26dff608e",
    "eef6c420cbc87b6f3f8c98cbb024d6a607051f398183d1bca6c15002a039256f",
    "447ab3e9008b4b8906f9c7c307e26ba6f96580881fcc379e961f30a93ff01951",
    "e042cfe564bd3e0b8a7f5d93bcdc6d4480ba73f6630be4e0113f1120ea2528b8",
)
BOOK_CHAPTERS = (22, 18, 44, 41, 24, 24)
BOOK_NOTES = (6, 6, 8, 17, 8, 10)
TEXT_SHA256 = "ab6c34985b3d68293ccda3ca28225d747fb85467037cb825d1cc1d930558a4c3"

WORK_ID = "evagrius-ecclesiastical-history"
ROMAN = (
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII",
    "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI",
    "XXVII", "XXVIII", "XXIX", "XXX", "XXXI", "XXXII", "XXXIII",
    "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
    "XLI", "XLII", "XLIII", "XLIV",
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fetch(name, expected):
    path = CACHE / name
    if not path.exists():
        request = urllib.request.Request(BASE_URL + name,
                                         headers={"User-Agent": UA})
        with urllib.request.urlopen(request, timeout=120) as response:
            path.write_bytes(response.read())
    data = path.read_bytes()
    digest = sha256(data)
    if digest != expected:
        raise ValueError("%s digest %s, expected %s" %
                         (name, digest, expected))
    return data.decode("utf-8")


class VisibleText(HTMLParser):
    """Render source HTML as plain text while retaining its paragraphs."""

    BLOCKS = {
        "address", "blockquote", "div", "h1", "h2", "h3", "h4", "h5",
        "h6", "li", "p", "pre", "table", "td", "th", "tr",
    }

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.parts = []
        self.hidden = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict((key.lower(), value or "") for key, value in attrs)
        if self.hidden:
            self.hidden.append(tag)
            return
        if tag in ("script", "style"):
            self.hidden.append(tag)
            return
        if tag == "span" and "pb" in attrs.get("class", "").lower().split():
            self.hidden.append(tag)
            return
        if tag == "br":
            self.parts.append("\n")
        elif tag in self.BLOCKS:
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.hidden:
            if tag == self.hidden[-1]:
                self.hidden.pop()
            return
        if tag in self.BLOCKS:
            self.parts.append("\n\n")

    def handle_data(self, data):
        if not self.hidden:
            # Newlines in the HTML source are layout whitespace. Paragraphs
            # and deliberate line breaks enter through their tags above.
            self.parts.append(re.sub(r"\s+", " ", data))


def house_text(value):
    value = (value.replace("\u2013", "-").replace("\u2014", "-")
             .replace("\u2018", "'").replace("\u2019", "'")
             .replace("\u201c", '"').replace("\u201d", '"')
             .replace("\xa0", " "))
    lines = []
    for line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)
        elif lines and lines[-1] != "":
            lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def render(fragment):
    fragment = re.sub(
        r'<a\b[^>]*href=["\']#(\d+)["\'][^>]*>\s*<sup>.*?</sup>\s*</a>',
        lambda match: "[%s]" % match.group(1), fragment,
        flags=re.I | re.S)
    parser = VisibleText()
    parser.feed(fragment)
    parser.close()
    return house_text("".join(parser.parts))


def notes_from(raw, book):
    marker = re.search(r'<p\b[^>]*class=["\']editorial["\'][^>]*>', raw,
                       flags=re.I)
    if not marker:
        raise ValueError("Book %d has no footnote editorial marker" % book)
    end = re.search(r"<hr\b", raw[marker.end():], flags=re.I)
    if not end:
        raise ValueError("Book %d footnote section has no end" % book)
    footer = raw[marker.end():marker.end() + end.start()]
    anchors = list(re.finditer(
        r'<a\b[^>]*name=["\']#?(\d+)["\'][^>]*>\s*</a>', footer,
        flags=re.I | re.S))
    if len(anchors) != BOOK_NOTES[book - 1]:
        raise ValueError("Book %d has %d notes, expected %d" %
                         (book, len(anchors), BOOK_NOTES[book - 1]))
    notes = {}
    for number, anchor in enumerate(anchors):
        stop = anchors[number + 1].start() if number + 1 < len(anchors) else len(footer)
        fragment = footer[anchor.end():stop]
        fragment = re.sub(r"^\s*%s\.\s*(?:&nbsp;)?" % anchor.group(1), "",
                          fragment, count=1, flags=re.I)
        note = render(fragment)
        note = re.sub(r"\n+$", "", note).strip()
        if not note:
            raise ValueError("Book %d note %s is empty" %
                             (book, anchor.group(1)))
        notes[anchor.group(1)] = note
    return notes, marker.start()


def insert_book_five_heading(raw):
    marker = re.compile(
        r"(?is)(</p>\s*)(<p>\s*JUSTIN also ejected Anastasius from the episcopate)")
    matches = list(marker.finditer(raw))
    if len(matches) != 1:
        raise ValueError("Book V Chapter V boundary fired %d times" % len(matches))
    replacement = (matches[0].group(1)
                   + '<h4 align="center">CHAPTER V.</h4>\n'
                   + matches[0].group(2))
    return raw[:matches[0].start()] + replacement + raw[matches[0].end():]


def chapter_title_and_text(fragment, book, chapter):
    if book == 5 and chapter == 5:
        title = "DEPOSITION OF ANASTASIUS, PATRIARCH OF ANTIOCH."
        body = render(fragment)
        return title, title + "\n\n" + body

    title_match = re.match(r'''(?is)\s*<p\b[^>]*align=["']center["'][^>]*>'''
                           r"(.*?)</p>", fragment)
    if not title_match:
        raise ValueError("Book %d Chapter %d has no title paragraph" %
                         (book, chapter))
    title_with_ref = render(title_match.group(1))
    title = re.sub(r"\s*\[\d+\]\s*$", "", title_with_ref).strip()
    body = render(fragment[title_match.end():])
    text = title_with_ref + ("\n\n" + body if body else "")
    return title, text


def divisions_from(raw, book):
    if book == 5:
        raw = insert_book_five_heading(raw)
    notes, footer_start = notes_from(raw, book)
    body = raw[:footer_start]
    headings = list(re.finditer(r"(?is)<h4\b[^>]*>(.*?)</h4>", body))
    expected = BOOK_CHAPTERS[book - 1] + (1 if book == 1 else 0)
    if len(headings) != expected:
        raise ValueError("Book %d has %d divisions, expected %d" %
                         (book, len(headings), expected))

    divisions = []
    referenced = set()
    for position, heading in enumerate(headings):
        label = render(heading.group(1)).strip().rstrip(".")
        if book == 1 and position == 0:
            if label != "PREFACE":
                raise ValueError("Book I preface heading changed")
            chapter = 0
        else:
            chapter = position if book == 1 else position + 1
            expected_label = "CHAPTER " + ROMAN[chapter - 1]
            if label != expected_label:
                if not (book == 5 and chapter == 13 and label == "CHAPTER X"):
                    raise ValueError("Book %d Chapter %d heading is %r" %
                                     (book, chapter, label))
        stop = headings[position + 1].start() if position + 1 < len(headings) else len(body)
        fragment = body[heading.end():stop]
        refs = re.findall(r'href=["\']#(\d+)["\']', fragment, flags=re.I)
        referenced.update(refs)
        title, text = chapter_title_and_text(fragment, book, chapter)
        for ref in refs:
            if ref not in notes:
                raise ValueError("Book %d note %s has no definition" % (book, ref))
        if refs:
            text += "\n\n" + "\n\n".join("[%s] %s" % (ref, notes[ref])
                                             for ref in refs)
        if chapter == 0:
            anchor = "Book I. Preface. " + title
        else:
            anchor = "Book %s. Chapter %d. %s" % (ROMAN[book - 1], chapter,
                                                   title)
        divisions.append((anchor, text))
    if referenced != set(notes):
        raise ValueError("Book %d unreferenced notes: %s" %
                         (book, ", ".join(sorted(set(notes) - referenced))))
    return divisions


def build():
    toc = fetch(TOC_NAME, TOC_SHA256)
    if "All material on this page is in the public domain - copy freely." not in toc:
        raise ValueError("public-domain statement is absent from the table of contents")

    divisions = []
    for book, expected in enumerate(BOOK_SHA256, 1):
        name = "evagrius_%d_book%d.htm" % (book, book)
        raw = fetch(name, expected)
        if "All material on this page is in the public domain - copy freely." not in raw:
            raise ValueError("Book %d public-domain statement is absent" % book)
        divisions.extend(divisions_from(raw, book))

    if len(divisions) != 174:
        raise ValueError("%d divisions, expected 174" % len(divisions))
    canonical = json.dumps(divisions, ensure_ascii=False, separators=(",", ":"))
    digest = sha256(canonical.encode("utf-8"))
    if TEXT_SHA256 and digest != TEXT_SHA256:
        raise ValueError("normalized text digest %s, expected %s" %
                         (digest, TEXT_SHA256))

    title = "Ecclesiastical History"
    author = "Evagrius Scholasticus"
    work = {
        "work_id": WORK_ID,
        "title": title,
        "author": author,
        "language": "en",
        "date": "c. 594",
        "translator": "Edward Walford",
        "pub_year": 1846,
        "publisher": "Samuel Bagster and Sons, London",
        "source": "The Ecclesiastical History of Evagrius, translated by Edward Walford (London: Samuel Bagster and Sons, 1846)",
        "source_url": BASE_URL + TOC_NAME,
        "source_class": "patristic",
        "description": (
            "A history of the Church from 431 to 594, continuing the earlier "
            "historians through the Councils of Ephesus and Chalcedon and the "
            "disputes, imperial policies, and divisions that followed. The "
            "1846 wording is preserved; straight quotes and hyphens replace "
            "the transcription's typographic quotes and dashes."
        ),
        "digitized": "Roger Pearse, Tertullian.org",
        "license": "Public Domain",
        "rights_url": BASE_URL + TOC_NAME,
        "saint": None,
        "is_saint": False,
    }
    units = []
    for ordinal, (anchor, text) in enumerate(divisions, 1):
        units.append({
            "unit_id": "%s::u%03d" % (WORK_ID, ordinal),
            "work_id": WORK_ID,
            "work_title": title,
            "author": author,
            "source_class": "patristic",
            "ordinal": ordinal,
            "citation_anchor": anchor,
            "chapter_title": None,
            "text": text,
        })
    return {"work": work, "units": units}, digest


def encoded(payload):
    return (json.dumps(payload, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--write-files-only", action="store_true")
    args = parser.parse_args()

    payload, digest = build()
    path = OUTDIR / (WORK_ID + ".json")
    body = encoded(payload)
    chars = sum(len(unit["text"]) for unit in payload["units"])
    print("%s: %d divisions, %s characters, sha256 %s" %
          (WORK_ID, len(payload["units"]), format(chars, ","), digest))
    if args.write or args.write_files_only:
        if not path.exists() or path.read_bytes() != body:
            path.write_bytes(body)
            print("wrote %s" % path.relative_to(ROOT))
    elif not path.exists() or path.read_bytes() != body:
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
    raise SystemExit(main())
