#!/usr/bin/env python3
"""Build source-bound French Guillon editions for the Library.

The literary text is the public-domain 1837 Guillon translation. The page
transcription is fetched from the validated French Wikisource page tied to
the same facsimile. Each normalized page is pinned by revision and digest.
The Internet Archive PDF can also be verified byte for byte with
``--verify-pdf``.

This tool deliberately writes edition files only. Catalogue and search
publication remain a separate reviewed step.
"""

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "manuscripts" / "guillon_1837_fr.json"
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path(tempfile.gettempdir()) / "plithos-guillon-1837"
API = "https://fr.wikisource.org/w/api.php"
UA = "Plithos source audit/1.0 (+https://plithos.org/)"

HOUSE_TRANSLATION = str.maketrans({
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
    "\u2014": "-", "\u2015": "-", "\u2018": "'", "\u2019": "'",
    "\u201a": "'", "\u201b": "'", "\u201c": '"', "\u201d": '"',
    "\u201e": '"', "\u201f": '"', "\u00a0": " ",
})


def house(value):
    value = html.unescape(value or "").translate(HOUSE_TRANSLATION)
    return re.sub(r"\s+", " ", value).strip()


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_text(value):
    return sha256_bytes(value.encode("utf-8"))


def fetch_json(url, cache_name):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / cache_name
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=45) as response:
        body = response.read()
    path.write_bytes(body)
    return json.loads(body.decode("utf-8"))


class PageTextParser(HTMLParser):
    """Read the visible edition text and notes from MediaWiki page HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.page_depth = None
        self.references_depth = None
        self.block = None
        self.block_tag = None
        self.block_depth = None
        self.note = None
        self.note_depth = None
        self.note_id = None
        self.list_note_id = None
        self.blocks = []
        self.notes = []

    @staticmethod
    def attrs_dict(attrs):
        return dict(attrs)

    @staticmethod
    def classes(attrs):
        return set(dict(attrs).get("class", "").split())

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        values = self.attrs_dict(attrs)
        classes = self.classes(attrs)
        if tag == "div" and "pagetext" in classes and self.page_depth is None:
            self.page_depth = self.depth
            return
        if self.page_depth is None:
            return
        if tag == "ol" and "references" in classes:
            self.references_depth = self.depth
            return
        if self.references_depth is not None and tag == "li":
            match = re.search(r"(\d+)$", values.get("id", ""))
            self.list_note_id = match.group(1) if match else None
        if (self.references_depth is not None and tag == "span"
                and "reference-text" in classes):
            self.note = []
            self.note_depth = self.depth
            self.note_id = self.list_note_id
            return
        if (self.references_depth is None and tag in ("h1", "h2", "h3", "p")
                and self.block is None):
            self.block = []
            self.block_tag = tag
            self.block_depth = self.depth
            return
        if tag == "br":
            if self.note is not None:
                self.note.append("\n")
            elif self.block is not None:
                self.block.append("\n")

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            if self.note is not None:
                self.note.append("\n")
            elif self.block is not None:
                self.block.append("\n")

    def handle_data(self, data):
        if self.note is not None:
            self.note.append(data)
        elif self.block is not None:
            self.block.append(data)

    def handle_endtag(self, tag):
        if (self.note is not None and self.depth == self.note_depth
                and tag == "span"):
            value = house("".join(self.note))
            if not self.note_id or not value:
                raise ValueError("reference note has no number or text")
            self.notes.append((self.note_id, value))
            self.note = None
            self.note_depth = None
            self.note_id = None
        if (self.block is not None and self.depth == self.block_depth
                and tag == self.block_tag):
            value = house("".join(self.block))
            if value:
                self.blocks.append(value)
            self.block = None
            self.block_tag = None
            self.block_depth = None
        if self.references_depth is not None and self.depth == self.references_depth:
            self.references_depth = None
        if self.page_depth is not None and self.depth == self.page_depth:
            self.page_depth = None
        self.depth -= 1


def page_title(manifest, page):
    return "%s/%d" % (manifest["transcription"]["page_title"],
                       page["scan_page"])


def page_url(title):
    query = urllib.parse.urlencode({
        "action": "parse",
        "page": title,
        "prop": "text|categories|revid",
        "format": "json",
        "formatversion": 2,
    })
    return API + "?" + query


def parse_page(manifest, page):
    title = page_title(manifest, page)
    payload = fetch_json(page_url(title), "page-%d.json" % page["scan_page"])
    record = payload.get("parse") or {}
    revision = record.get("revid")
    if revision != page["revision"]:
        raise ValueError("page %d revision changed: %r" %
                         (page["printed_page"], revision))
    categories = {item.get("category") for item in record.get("categories", [])}
    if "Page_validée" not in categories:
        raise ValueError("page %d is not validated by two contributors" %
                         page["printed_page"])
    parser = PageTextParser()
    parser.feed(record.get("text", ""))
    if not parser.blocks:
        raise ValueError("page %d has no edition text" % page["printed_page"])
    text = "\n\n".join(parser.blocks)
    if parser.notes:
        text += "\n\n" + "\n\n".join(
            "[%s] %s" % item for item in parser.notes)
    digest = sha256_text(text)
    if digest != page["digest"]:
        raise ValueError("page %d normalized digest changed: %s" %
                         (page["printed_page"], digest))
    for pattern, label in ((r"[\u2010-\u2015]", "forbidden dash"),
                           (r"[\u2018-\u201f]", "curly quote"),
                           (r"\ufffd", "replacement character")):
        if re.search(pattern, text):
            raise ValueError("page %d contains %s" %
                             (page["printed_page"], label))
    return text


def work_record(manifest):
    edition = dict(manifest["edition"])
    base_path = OUTDIR / (edition["edition_of"] + ".json")
    base = json.loads(base_path.read_text(encoding="utf-8"))["work"]
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    indexed = next((item for item in index
                    if item.get("work_id") == edition["edition_of"]), {})
    for field in ("saint", "is_saint", "purpose", "centuries", "century",
                  "period", "topics", "feast_day"):
        if field in indexed:
            edition[field] = indexed[field]
        elif field in base:
            edition[field] = base[field]
    return edition


def build(manifest):
    work = work_record(manifest)
    units = []
    for ordinal, page in enumerate(manifest["pages"], 1):
        text = parse_page(manifest, page)
        units.append({
            "unit_id": "%s::u%02d" % (work["work_id"], ordinal),
            "work_id": work["work_id"],
            "work_title": work["title"],
            "author": work["author"],
            "source_class": work["source_class"],
            "ordinal": ordinal,
            "citation_anchor": "%s, p. %d" %
                               (work["title"], page["printed_page"]),
            "text": text,
        })
    first = units[0]["text"]
    last = units[-1]["text"]
    if not first.startswith(manifest["verification"]["first_text"]):
        raise ValueError("first page opening changed")
    if not last.endswith(manifest["verification"]["last_text"]):
        raise ValueError("last page closing changed")
    if len(units) != manifest["verification"]["units"]:
        raise ValueError("unit count changed")
    return {"work": work, "units": units}


def verify_pdf(manifest, path):
    raw = path.read_bytes()
    source = manifest["source"]
    if len(raw) != source["bytes"]:
        raise ValueError("PDF size is %d, expected %d" %
                         (len(raw), source["bytes"]))
    digest = sha256_bytes(raw)
    if digest != source["sha256"]:
        raise ValueError("PDF SHA256 is %s, expected %s" %
                         (digest, source["sha256"]))
    print("verified PDF: %d bytes, sha256 %s" % (len(raw), digest))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-pdf", type=Path)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.verify_pdf:
        verify_pdf(manifest, args.verify_pdf)
    try:
        output = build(manifest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(exc)
        return 1
    destination = OUTDIR / (output["work"]["work_id"] + ".json")
    body = json.dumps(output, ensure_ascii=False, indent=1) + "\n"
    chars = sum(len(unit["text"]) for unit in output["units"])
    print("%s: %d source pages, %s characters, sha256 %s" %
          (output["work"]["work_id"], len(output["units"]),
           format(chars, ","), sha256_text(body)))
    if args.write:
        destination.write_text(body, encoding="utf-8")
        print("wrote %s" % destination.relative_to(ROOT))
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        index = [item for item in index
                 if item.get("work_id") != output["work"]["work_id"]]
        index.append(output["work"])
        index.sort(key=lambda item: item["work_id"])
        INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")
        print("updated %s" % INDEX.relative_to(ROOT))
    elif args.check:
        try:
            actual = destination.read_text(encoding="utf-8")
        except OSError as exc:
            print("stale or missing %s: %s" %
                  (destination.relative_to(ROOT), exc))
            return 1
        if actual != body:
            print("stale %s" % destination.relative_to(ROOT))
            return 1
    else:
        print("nothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
