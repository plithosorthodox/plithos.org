#!/usr/bin/env python3
"""
Plithos library ingester.

Fetches public-domain patristic texts, normalises them to house style, and
emits them in the CORPUS schema the reader already understands.

Source note. New Advent hosts the Ante-Nicene and Nicene and Post-Nicene
Fathers translations, which are public domain (published 1885 to 1900). New
Advent applies a light editorial layer, chiefly modernised second-person
pronouns, and asserts copyright over its compilation. The underlying
translations are unambiguously public domain. Provenance is recorded per work
so the position is auditable, and any work can be re-sourced from CCEL or the
Internet Archive if a stricter provenance is wanted.

House rules applied to every unit:
  no em or en dashes, converted to hyphens
  smart quotes normalised to straight
  inline scripture and encyclopedia links stripped, text kept
  editorial footnote markers removed
  paragraphs separated by one blank line
"""
import html
import json
import re
import time
import urllib.request
from pathlib import Path

LIB = Path("/home/claude/lib")
RAW = LIB / "raw"
OUT = LIB / "out"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"


def fetch(url, cache_name, delay=1.5):
    p = RAW / cache_name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


DASHES = dict.fromkeys(map(ord, "\u2013\u2014\u2012\u2015"), "-")
QUOTES = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x00A0: " "}


def clean_text(s):
    s = html.unescape(s)
    s = s.translate(DASHES).translate(QUOTES)
    s = re.sub(r"<a\b[^>]*>(.*?)</a>", r"\1", s, flags=re.S | re.I)
    s = re.sub(r"<sup\b[^>]*>.*?</sup>", "", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\[\d+\]|\(\d{1,3}\)", "", s)      # footnote markers
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def strip_scripture_refs(s):
    """New Advent inlines references such as 'Matthew 5:26' after a link."""
    books = (r"Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|"
             r"1 Samuel|2 Samuel|1 Kings|2 Kings|Psalm|Psalms|Proverbs|Isaiah|"
             r"Jeremiah|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|"
             r"Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|"
             r"Acts|Romans|1 Corinthians|2 Corinthians|Galatians|Ephesians|"
             r"Philippians|Colossians|1 Thessalonians|2 Thessalonians|1 Timothy|"
             r"2 Timothy|Titus|Philemon|Hebrews|James|1 Peter|2 Peter|1 John|"
             r"2 John|3 John|Jude|Revelation|Sirach|Wisdom|Tobit|Judith|Baruch")
    s = re.sub(r"\s*(?:cf\.\s*)?(?:" + books + r")\s+\d+:\d+(?:-\d+)?", "", s)
    return re.sub(r"[ \t]{2,}", " ", s).strip()


def parse_newadvent(body):
    """Return (preamble, [(heading, text), ...]) from a New Advent father page."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>(.*?)(?=<h2[^>]*>\s*About this page|\Z)",
                  body, re.S | re.I)
    if not m:
        raise ValueError("page shape not recognised")
    trunk = m.group(2)
    trunk = re.sub(r"<em>.*?Please help support the mission.*?</em>", "", trunk, flags=re.S | re.I)

    parts = re.split(r"<h2[^>]*>(.*?)</h2>", trunk, flags=re.S | re.I)
    preamble = clean_text(parts[0]) if parts else ""
    chapters = []
    for i in range(1, len(parts) - 1, 2):
        heading = clean_text(parts[i])
        text = strip_scripture_refs(clean_text(parts[i + 1]))
        if text:
            chapters.append((heading, text))
    return preamble, chapters


def build_work(meta, chapters):
    wid = meta["work_id"]
    units = []
    for n, (heading, text) in enumerate(chapters, start=1):
        units.append({
            "unit_id": f"{wid}::u{n:02d}",
            "work_id": wid,
            "work_title": meta["title"],
            "author": meta["author"],
            "source_class": meta["source_class"],
            "ordinal": n,
            "citation_anchor": heading,
            "text": text,
        })
    return meta, units


def emit(meta, units):
    OUT.joinpath(f"{meta['work_id']}.json").write_text(
        json.dumps({"work": meta, "units": units}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    words = sum(len(u["text"].split()) for u in units)
    dashes = sum(len(re.findall(r"[\u2013\u2014]", u["text"])) for u in units)
    return len(units), words, dashes


if __name__ == "__main__":
    CATALOGUE = [
        dict(work_id="didache", url="https://www.newadvent.org/fathers/0714.htm",
             title="The Didache", author="The Twelve Apostles",
             language="en", source_class="patristic", date="c. 100",
             translator="M. B. Riddle", pub_year=1886,
             source="Ante-Nicene Fathers, Vol. 7",
             digitized="New Advent", license="Public Domain",
             description="The earliest surviving manual of Christian practice, "
                         "covering the two ways, baptism, fasting, the Eucharist, "
                         "the discernment of prophets, and the Lord's coming."),
    ]
    for entry in CATALOGUE:
        url = entry.pop("url")
        body = fetch(url, entry["work_id"] + ".html")
        preamble, chapters = parse_newadvent(body)
        if preamble and not entry.get("description"):
            entry["description"] = preamble[:400]
        meta, units = build_work(entry, chapters)
        n, w, d = emit(meta, units)
        print(f"{meta['work_id']:34s} {n:>3} units  {w:>7,} words  dashes={d}")


# ---------------------------------------------------------------- multi-page works
def parse_index_links(body):
    """New Advent index pages link to their parts as ../fathers/NNNN.htm."""
    out, seen = [], set()
    for num, label in re.findall(r'href="\.\./fathers/(\d+)\.htm">(.*?)</a>', body, re.S | re.I):
        if num in seen:
            continue
        seen.add(num)
        out.append((num, clean_text(label)))
    return out


def ingest_multipage(entry, url, limit=None, delay=1.2):
    """Fetch an index page, then each part, flattening parts into units."""
    idx = fetch(url, entry["work_id"] + "__index.html", delay)
    parts = parse_index_links(idx)
    parts = [(n, t) for n, t in parts if t and not re.match(r"^(Home|Fathers|New Advent)", t)]
    if limit:
        parts = parts[:limit]
    chapters = []
    for num, label in parts:
        try:
            body = fetch(f"https://www.newadvent.org/fathers/{num}.htm",
                         f"{entry['work_id']}__{num}.html", delay)
            pre, chs = parse_newadvent(body)
        except Exception as e:
            print(f"    skip {num} {label[:40]}: {e}")
            continue
        if chs:
            for h, t in chs:
                chapters.append((f"{label}. {h}" if h and h != label else label, t))
        elif pre:
            chapters.append((label, strip_scripture_refs(pre)))
    return chapters
