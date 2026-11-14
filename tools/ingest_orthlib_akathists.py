#!/usr/bin/env python3
"""Stage Church Slavonic akathists from Orthlib's public-domain HIP files.

Orthlib publishes the source transcription in its HIP archive and the same
text as a typeset PDF.  This builder downloads the pinned HIP archive, checks
both archive and source digests, and converts the source through the pinned
HIP-to-Unicode table maintained by the Slavonic Computing Initiative.

The conversion table is data, not a language model or a transliteration.  It
maps every HIP token to the corresponding Unicode Church Slavonic character.
The source's accents, titla, historic letters, headings, and abbreviations are
therefore preserved.

    python tools/ingest_orthlib_akathists.py --check
    python tools/ingest_orthlib_akathists.py --write-files-only
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path(tempfile.gettempdir()) / "plithos-orthlib-akathists"
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
RIGHTS = "Public Domain"
RIGHTS_URL = "http://www.orthlib.info/Intellectual-Property.html"
SOURCE_ROOT = "http://www.orthlib.ru/worship/akafist/"
CONVERTER_COMMIT = "839c24501d1ce8e6c446dd8e935a54b3498051d4"
CONVERTER_URL = (
    "https://raw.githubusercontent.com/typiconman/Perl-Lingua-CU/"
    + CONVERTER_COMMIT + "/lib/Lingua/CU/Scripts/hipequivs"
)
CONVERTER_SHA256 = "374a6d263bbc4feccfdc6f8e7f19d02ee933a42630603bf20b610b01965ae3fc"


CATALOGUE = [
    {
        "name": "kazansk",
        "archive_sha256": "67d16642b81d6bc6c38f30ab90e3cbf9d039c725ac06fb07bc23fadec4979218",
        "hip_sha256": "e0cad26ee260d78cd30a1d726744d9a8ef437e6163927635e3cd2b2918f4a435",
        "work_id": "akathist-kazan-icon-cu",
        "edition_of": "akathist-kazan-icon",
        "title": "А҆КА́ѲІСТЪ ПРЕСТ҃Ѣ́Й БГ҃ОРО́ДИЦѢ, Ꙗ҆ВЛЕ́НІѦ РА́ДИ ЧꙊДОТВО́РНЫѦ Є҆Ѧ̀ І҆КѠ́НЫ КАЗА́НСКІѦ",
        "author": "Anonymous",
        "date": "traditional; this edition 1897",
        "pub_year": 1897,
        "source": (
            "Акафист Пресвятей Богородице, явления ради чудотворныя "
            "Ея иконы, 11th ed. (St Petersburg: Synodal Press, 1897)"
        ),
        "description": (
            "The Church Slavonic Akathist before the Kazan Icon of the Most "
            "Holy Theotokos, reproduced from the eleventh edition printed by "
            "the Synodal Press in 1897. Hyphens replace the edition's "
            "typographic dashes."
        ),
        "expected_units": 27,
        "first_heading": "Акафистъ",
        "last_heading": "Моли́тва Прест҃ѣ́й Бг҃оро́дицѣ",
        "digest": "04b203e4efbab73f254078724a8b886f9e65bfca1e887878b771f18b9fbf6c3a",
    },
    {
        "name": "afanasiy",
        "archive_sha256": "c77f03741ec6c1ee94c2fa3ed96d498b6a5272cad9ef963f5dfe469b1dd9cb1e",
        "hip_sha256": "25f4acb46878927abe879d44fea3b4ecfafd1dab921d82165a4e9e95ed953e47",
        "work_id": "akathist-athanasius-athos-cu",
        "edition_of": "akathist-athanasius-athos",
        "title": "А҆КА́ѲІСТЪ прпⷣбномꙋ и҆ бг҃оно́сномꙋ ѻ҆тцꙋ̀ на́шемꙋ А҆ѲАНА́СІЮ а҆ѳѡ́нскомꙋ чꙋдотво́рцꙋ",
        "author": "Anonymous",
        "date": "traditional; this edition 1908",
        "pub_year": 1908,
        "source": (
            "Акафист преподобному и богоносному отцу нашему Афанасию "
            "Афонскому чудотворцу (Moscow: Synodal Press, 1908)"
        ),
        "description": (
            "The Church Slavonic Akathist to St Athanasius of Athos, "
            "reproduced from the 1908 Moscow Synodal Press edition issued by "
            "the Russian Skete of the Ascension on Mount Athos. Hyphens "
            "replace the edition's typographic dashes."
        ),
        "expected_units": 30,
        "first_heading": "Акафистъ",
        "last_heading": "Конда́къ, гла́съ и҃",
        "digest": "5b2aba1acd5a9b6dcfa8f845aece897a4ce0c59c3fb743a27f6dc325cfeeb000",
    },
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url, name, expected):
    path = CACHE / name
    if not path.exists():
        request = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(request, timeout=120) as response:
            path.write_bytes(response.read())
    data = path.read_bytes()
    digest = sha256(data)
    if digest != expected:
        raise ValueError("%s digest %s, expected %s" % (name, digest, expected))
    return data


def extract_hip(entry, archive):
    """Extract one named HIP file with the system's archive reader."""
    target = CACHE / (entry["name"] + ".hip")
    if not target.exists():
        archive_path = CACHE / (entry["name"] + ".rar")
        archive_path.write_bytes(archive)
        unpacked = CACHE / (entry["name"] + "-unpacked")
        if unpacked.exists():
            shutil.rmtree(unpacked)
        unpacked.mkdir()
        command = ["tar", "-xf", str(archive_path), "-C", str(unpacked)]
        try:
            subprocess.run(command, check=True, capture_output=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ValueError("the system archive reader could not extract %s.rar: %s"
                             % (entry["name"], exc)) from exc
        source = unpacked / (entry["name"] + ".hip")
        if not source.exists():
            raise ValueError("%s.rar does not contain %s.hip"
                             % (entry["name"], entry["name"]))
        target.write_bytes(source.read_bytes())
    data = target.read_bytes()
    digest = sha256(data)
    if digest != entry["hip_sha256"]:
        raise ValueError("%s.hip digest %s, expected %s"
                         % (entry["name"], digest, entry["hip_sha256"]))
    return data.decode("cp1251")


def perl_string(value, quote):
    """Decode the limited Perl string syntax used by hipequivs."""
    if quote == "'":
        return value.replace("\\\\", "\\").replace("\\'", "'")
    return value.replace("\\\\", "\\").replace('\\"', '"')


def parse_mapping(raw):
    text = raw.decode("utf-8")
    mapping = []
    line_re = re.compile(r"^(['\"])(.*?)\1\s*=>\s*(.*),$")
    chr_re = re.compile(r"chr\(0x([0-9A-Fa-f]+)\)")
    for line in text.splitlines():
        match = line_re.match(line)
        if not match:
            continue
        token = perl_string(match.group(2), match.group(1))
        codepoints = chr_re.findall(match.group(3))
        if not codepoints:
            raise ValueError("unparsed converter row: %s" % line)
        mapping.append((token, "".join(chr(int(value, 16))
                                       for value in codepoints)))
    if len(mapping) < 180:
        raise ValueError("only %d HIP converter rows were parsed" % len(mapping))
    return mapping


def hip_to_unicode(source, mapping):
    marker = "<::слав>"
    if marker not in source:
        raise ValueError("Church Slavonic marker is absent")
    pattern = re.compile("|".join(re.escape(key) for key, _value in mapping))
    table = dict(mapping)
    diacritics = "".join(chr(value) for value in
                         list(range(0x0300, 0x0370))
                         + list(range(0x0483, 0x0488))
                         + list(range(0x2DE0, 0x2E00)))
    parts = re.split(r"(<::(?:лат|рус|слав|греч|глаг)>)",
                     source.split(marker, 1)[1])
    mode = "слав"
    converted = []
    for part in parts:
        mode_match = re.fullmatch(r"<::(лат|рус|слав|греч|глаг)>", part)
        if mode_match:
            mode = mode_match.group(1)
            continue
        part = part.replace("%<", "").replace("%>", "")
        part = part.replace("%[", "").replace("%]", "")
        part = part.replace("%(", "").replace("%)", "")
        if mode == "слав":
            part = pattern.sub(lambda match: table[match.group(0)], part)
            # Lingua::CU applies these two documented post-conversion steps.
            part = re.sub("\u0456([^%s])" % re.escape(diacritics),
                          "\u0456\u0308\\1", part)
            part = part.replace("\uf8ff", "\u0456")
        else:
            # The sole civil-text markup used by these editions is the dash
            # token in an editorial footnote.
            part = part.replace("<-->", "-")
        converted.append(part)
    text = "".join(converted)
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if re.search(r"%[<>\[\]()]|<::", text):
        raise ValueError("HIP formatting marker remains")
    if "\ufffd" in text:
        raise ValueError("unconvertible HIP token remains")
    return text


def plain_heading(value):
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value
                    if not unicodedata.combining(char))
    value = value.replace("҃", "").replace("҆", "")
    return unicodedata.normalize("NFC", value).lower()


def split_units(text):
    """Split at the source's own headings while keeping every word."""
    paragraphs = [value.strip() for value in re.split(r"\n\s*\n", text)
                  if value.strip()]
    units = []
    title = []
    current = None

    def is_heading(value):
        normalized = plain_heading(value)
        return normalized.startswith(("кондакъ", "ікосъ", "и паки",
                                      "молитва", "тропарь"))

    def separate_heading(value):
        # Some Orthlib files place the ikos text after its heading in the
        # same paragraph, while others place it in the next paragraph.
        stops = [position for position in (value.find(":"), value.find("."))
                 if position >= 0]
        if not stops:
            return value.strip(), ""
        stop = min(stops) + 1
        return value[:stop].strip(), value[stop:].strip()

    for paragraph in paragraphs:
        if is_heading(paragraph):
            if current:
                units.append(current)
            elif title:
                units.append(("Акафистъ", "\n\n".join(title)))
                title = []
            heading, body = separate_heading(paragraph)
            current = (heading.rstrip(".:"), paragraph if body else heading)
        elif current:
            current = (current[0], current[1] + "\n\n" + paragraph)
        else:
            title.append(paragraph)
    if current:
        units.append(current)
    elif title:
        units.append(("Акафистъ", "\n\n".join(title)))
    if not units:
        raise ValueError("no akathist units were found")
    return units


def build(entry, mapping):
    archive_name = entry["name"] + ".rar"
    archive = fetch(SOURCE_ROOT + archive_name, archive_name,
                    entry["archive_sha256"])
    source = extract_hip(entry, archive)
    text = hip_to_unicode(source, mapping)
    divisions = split_units(text)
    if len(divisions) != entry["expected_units"]:
        raise ValueError("%s has %d units, expected %d"
                         % (entry["work_id"], len(divisions),
                            entry["expected_units"]))
    if divisions[0][0] != entry["first_heading"]:
        raise ValueError("%s first heading is %r"
                         % (entry["work_id"], divisions[0][0]))
    if divisions[-1][0] != entry["last_heading"]:
        raise ValueError("%s last heading is %r"
                         % (entry["work_id"], divisions[-1][0]))

    work = {
        "work_id": entry["work_id"],
        "edition_of": entry["edition_of"],
        "title": entry["title"],
        "author": entry["author"],
        "language": "cu",
        "date": entry["date"],
        "translator": None,
        "pub_year": entry["pub_year"],
        "source": entry["source"],
        "source_url": SOURCE_ROOT + archive_name,
        "source_class": "liturgical",
        "description": entry["description"],
        "digitized": "Orthlib.ru",
        "license": RIGHTS,
        "rights_url": RIGHTS_URL,
        "saint": None,
        "is_saint": False,
    }
    width = max(2, len(str(len(divisions))))
    units = []
    for ordinal, (anchor, unit_text) in enumerate(divisions, 1):
        units.append({
            "unit_id": "%s::u%0*d" % (entry["work_id"], width, ordinal),
            "work_id": entry["work_id"],
            "work_title": entry["title"],
            "author": entry["author"],
            "source_class": "liturgical",
            "ordinal": ordinal,
            "citation_anchor": anchor,
            "chapter_title": None,
            "text": unit_text,
        })
    canonical = json.dumps([(anchor, unit_text)
                            for anchor, unit_text in divisions],
                           ensure_ascii=False, separators=(",", ":"))
    digest = sha256(canonical.encode("utf-8"))
    if digest != entry["digest"]:
        raise ValueError("%s text digest %s, expected %s"
                         % (entry["work_id"], digest, entry["digest"]))
    return {"work": work, "units": units}, digest


def encoded(payload):
    return (json.dumps(payload, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--write-files-only", action="store_true")
    parser.add_argument("--only", choices=[entry["work_id"] for entry in CATALOGUE])
    args = parser.parse_args()

    raw_mapping = fetch(CONVERTER_URL, "hipequivs", CONVERTER_SHA256)
    mapping = parse_mapping(raw_mapping)
    chosen = [entry for entry in CATALOGUE
              if not args.only or entry["work_id"] == args.only]
    failed = False
    built = []
    for entry in chosen:
        payload, digest = build(entry, mapping)
        built.append(payload)
        body = encoded(payload)
        path = OUTDIR / (entry["work_id"] + ".json")
        current = path.read_bytes() if path.exists() else None
        print("%s: %d units, %s characters, sha256 %s"
              % (entry["work_id"], len(payload["units"]),
                 format(sum(len(unit["text"]) for unit in payload["units"]), ","),
                 digest))
        if args.write or args.write_files_only:
            if current != body:
                path.write_bytes(body)
                print("wrote %s" % path.relative_to(ROOT))
        elif current != body:
            print("stale or missing %s" % path.relative_to(ROOT))
            failed = True
    if args.write:
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        ids = {payload["work"]["work_id"] for payload in built}
        index = [item for item in index if item.get("work_id") not in ids]
        index.extend(payload["work"] for payload in built)
        index.sort(key=lambda item: item["work_id"])
        INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")
        print("updated %s" % INDEX.relative_to(ROOT))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
