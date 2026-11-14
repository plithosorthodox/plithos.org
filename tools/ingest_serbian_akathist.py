#!/usr/bin/env python3
"""Build the Serbian Akathist to St Ambrose of Optina from a pinned source.

The Serbian Wikisource page names its translator and copyeditor, identifies
the approved Church Slavonic source from which it was translated, and releases
the text without copyright for unrestricted use. The permanent revision is
used so a later wiki edit cannot silently alter the Library text.

    python tools/ingest_serbian_akathist.py --check
    python tools/ingest_serbian_akathist.py --write
"""
import argparse
import hashlib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
WORK_ID = "akathist-ambrose-optina-sr"
EDITION_OF = "akathist-ambrose-optina"
REVISION = 140629
MEDIAWIKI_SHA1 = "a3026f1e55450393bf0881436f1d2ef1fec6a79e"
WIKITEXT_SHA256 = "631cce9db9d977307d016b89843f99006c724489c9c2194af9f7c21ff2f54d68"
CANONICAL_SHA256 = "712fbf6c3b7e0ce6f5ae88027e9396e1b9feba87c20864e9a36bcac1708651d8"
PAGE = (
    "https://sr.wikisource.org/wiki/"
    "%D0%90%D0%BA%D0%B0%D1%82%D0%B8%D1%81%D1%82_"
    "%D0%A1%D0%B2%D0%B5%D1%82%D0%BE%D0%BC_"
    "%D0%90%D0%BC%D0%B2%D1%80%D0%BE%D1%81%D0%B8%D1%98%D1%83_"
    "%D0%9E%D0%BF%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%BC"
)
PERMANENT = PAGE + "?oldid=%d" % REVISION
API = (
    "https://sr.wikisource.org/w/api.php?action=query&prop=revisions"
    "&revids=%d&rvprop=ids%%7Ctimestamp%%7Csha1%%7Ccontent&rvslots=main"
    "&format=json&formatversion=2" % REVISION
)
UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def fetch_revision():
    request = urllib.request.Request(API, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read()
    payload = json.loads(raw.decode("utf-8"))
    revision = payload["query"]["pages"][0]["revisions"][0]
    if revision.get("revid") != REVISION:
        raise ValueError("MediaWiki returned revision %r" % revision.get("revid"))
    if revision.get("sha1") != MEDIAWIKI_SHA1:
        raise ValueError("MediaWiki SHA1 changed: %r" % revision.get("sha1"))
    text = revision["slots"]["main"]["content"]
    digest = sha256(text.encode("utf-8"))
    if digest != WIKITEXT_SHA256:
        raise ValueError("wikitext SHA256 %s, expected %s" %
                         (digest, WIKITEXT_SHA256))
    return text


def plain(value):
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"</?(?:center|big|small|span|div|poem|b|i)(?:\s[^>]*)?>",
                   "", value, flags=re.I)
    value = re.sub(r"'''?", "", value)
    value = re.sub(r"\[\[(?:[^]|]*\|)?([^]]+)\]\]", r"\1", value)
    value = html.unescape(value)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def split_units(wikitext):
    body = re.sub(r"^\{\{заглавље\b.*?\}\}\s*", "", wikitext,
                  count=1, flags=re.S | re.I)
    body = re.sub(r"^\[\[Категорија:[^]]+\]\]\s*", "", body,
                  flags=re.M | re.I)
    matches = list(re.finditer(r"^===\s*(.+?)\s*===\s*$", body, re.M))
    if len(matches) != 26:
        raise ValueError("found %d source headings, expected 26" % len(matches))

    units = [("Наслов и спомен", plain(body[:matches[0].start()]))]
    for number, match in enumerate(matches):
        end = matches[number + 1].start() if number + 1 < len(matches) else len(body)
        units.append((plain(match.group(1)), plain(body[match.end():end])))

    expected = []
    for number in range(1, 14):
        expected.append("Кондак %d." % number)
        if number <= 12:
            expected.append("Икос %d." % number)
    expected.append("Молитва")
    got = [heading for heading, _text in units[1:]]
    if got != expected:
        raise ValueError("source heading sequence changed: %r" % got)
    if any(not text for _heading, text in units):
        raise ValueError("an empty unit was found")
    if sum(text.count("Алилуја!") for _heading, text in units) != 12:
        raise ValueError("the akathist must contain 12 Alleluia closings")
    refrain = "Радуј се, преподобни оче Амвросије, богомудри учитељу вере и побожности!"
    if sum(text.count(refrain) for _heading, text in units) != 13:
        raise ValueError("the common refrain must occur 13 times")
    rubric = "Овај кондак се чита трипут, а затим опет Икос 1. и Кондак 1."
    if rubric not in dict(units)["Кондак 13."]:
        raise ValueError("the closing repetition rubric is missing")
    return units


def build():
    divisions = split_units(fetch_revision())
    title = "Акатист Светом Амвросију Оптинском"
    work = {
        "work_id": WORK_ID,
        "edition_of": EDITION_OF,
        "title": title,
        "author": "Anonymous",
        "language": "sr",
        "date": "traditional; this Serbian translation 2020",
        "translator": "Бојан Боровићанин",
        "pub_year": 2020,
        "source": (
            "Акатист Светом Амвросију Оптинском, translated and edited "
            "from the Church Slavonic text approved by the Russian Orthodox "
            "Church under Patriarch Pimen on September 22, 1988"
        ),
        "source_url": PERMANENT,
        "source_class": "liturgical",
        "description": (
            "The complete Serbian Akathist to St Ambrose of Optina: thirteen "
            "kontakia, twelve ikoi, the direction to repeat the final "
            "kontakion and return to the first ikos and kontakion, and the "
            "concluding prayer. Bojan Borovicanin translated and edited it "
            "in Kragujevac in 2020 from the Church Slavonic text approved by "
            "the Russian Orthodox Church under Patriarch Pimen on September "
            "22, 1988; Biljana Todorcevic checked and copyedited the Serbian "
            "text. The source releases this text without copyright for "
            "unrestricted use."
        ),
        "digitized": "Serbian Wikisource",
        "rights": "Public Domain dedication by the translator",
        "rights_url": PERMANENT,
        "attribution": (
            "Serbian translation and editing by Бојан Боровићанин; "
            "copyediting by Биљана Тодорчевић"
        ),
        "transcription_url": PERMANENT,
        "saint": None,
        "is_saint": False,
        "purpose": "The life of prayer",
        "centuries": [21],
        "century": 21,
        "period": "21st century",
    }
    width = len(str(len(divisions)))
    units = []
    for ordinal, (heading, text) in enumerate(divisions, 1):
        units.append({
            "unit_id": "%s::u%0*d" % (WORK_ID, width, ordinal),
            "work_id": WORK_ID,
            "work_title": title,
            "author": work["author"],
            "source_class": work["source_class"],
            "ordinal": ordinal,
            "citation_anchor": heading,
            "chapter_title": None,
            "text": text,
        })
    canonical = json.dumps(divisions, ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")
    digest = sha256(canonical)
    if CANONICAL_SHA256 and digest != CANONICAL_SHA256:
        raise ValueError("canonical SHA256 %s, expected %s" %
                         (digest, CANONICAL_SHA256))
    return {"work": work, "units": units}, digest


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    try:
        payload, digest = build()
        path = OUTDIR / (WORK_ID + ".json")
        expected = encoded(payload)
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        rows = [row for row in index if row.get("work_id") != WORK_ID]
        rows.append(payload["work"])
        rows.sort(key=lambda row: row.get("work_id", ""))
        expected_index = encoded(rows)
        if args.write:
            path.write_bytes(expected)
            INDEX.write_bytes(expected_index)
        stale = []
        if not path.exists() or path.read_bytes() != expected:
            stale.append(str(path.relative_to(ROOT)))
        if json.loads(INDEX.read_text(encoding="utf-8")) != rows:
            stale.append(str(INDEX.relative_to(ROOT)))
        if stale:
            raise ValueError("stale: " + ", ".join(stale))
        print("%s: %d units, canonical sha256 %s" %
              (WORK_ID, len(payload["units"]), digest))
        return 0
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
