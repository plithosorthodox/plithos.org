#!/usr/bin/env python3
"""Build source-bound English Cyprian works from the BKV ANF edition.

The University of Fribourg BKV catalogue supplies a complete division tree,
page transcription, notes, and page images for the public-domain 1886
Ante-Nicene Fathers, volume 5. Each edition below pins the catalogue tree,
normalized literary text, headings, note count, and first and last text.

The files-only mode supports the repository's two-stage publication rule:

    python tools/ingest_cyprian_en.py --write-files-only
    python tools/ingest_cyprian_en.py --check
    python tools/ingest_cyprian_en.py --write

The first command writes edition JSON without changing the public catalogue.
The regular write mode keeps the established behavior and publishes catalogue
records as well.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import tempfile
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path(tempfile.gettempdir()) / "plithos-cyprian-en"
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
DIGITIZED = "University of Fribourg, Bibliothek der Kirchenväter"
RIGHTS = "Public domain"
RIGHTS_URL = "https://bkv.unifr.ch/en/about/copyrights"
FACSIMILE = "https://www.loc.gov/resource/gdc.27027909v5/"

HOUSE_TRANSLATION = str.maketrans({
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
    "\u2014": "-", "\u2015": "-", "\u2018": "'", "\u2019": "'",
    "\u201a": "'", "\u201b": "'", "\u201c": '"', "\u201d": '"',
    "\u201e": '"', "\u201f": '"', "\u00a0": " ",
})

SOURCE = ("Ante-Nicene Fathers, Vol. 5, Christian Literature Publishing "
          "Company, Buffalo, 1886")

CATALOGUE = [
    {
        "work_id": "cyprian-to-donatus",
        "version_url": "https://bkv.unifr.ch/en/works/cpl-38/versions/ad-donatum",
        "title": "To Donatus",
        "author": "St Cyprian of Carthage",
        "date": "c. 246",
        "translator": "Robert Ernest Wallis",
        "pub_year": 1886,
        "source": SOURCE,
        "source_class": "patristic",
        "description": ("St Cyprian's address to Donatus on baptism, the "
                        "transformation of life in Christ, and contempt for "
                        "the corruptions of the world."),
        "cpl": "CPL 38",
        "units": 17,
        "tree_nodes": 22,
        "notes": 15,
        "first_heading": "Ad Donatum. [1]",
        "last_heading": "16.",
        "first_text": ("To Donatus.\n\nArgument.--Cyprian Had Promised Donatus "
                       "that He Would Have a Discourse with Him Concerning "
                       "Things Divine, and Now Being Reminded of His Promise, "
                       "He Fulfils It."),
        "last_text": ("[1] [See Cowper, on \"the Sabine bard,\" Task, b. iv. But "
                      "compare even the best of Horatian epistles with this: "
                      "\"O noctes coenaeque Deum,\" etc. What a blessed contrast "
                      "in Christian society!]\n\n"
                      "[2] [Here recall the Evening Hymn, vol. ii. p. 298.]"),
        "tree_digest": "920728de5ab280891d4c527ef5418a65ecd0ca97bbc08fef86d6f75e3b7bb45f",
        "bibliographic_digest": "d30655215647842567d012474a9373a38df273926deb5090342b07fbedef6381",
        "digest": "efd3061da0b60824fd741e6bcd55698c9997f87e0750c414f65faeb4128be3a5",
    },
    {
        "work_id": "cyprian-exhortation-to-martyrdom",
        "version_url": ("https://bkv.unifr.ch/en/works/cpl-45-1/versions/"
                        "exhortation-to-martyrdom-addressed-to-fortunatus"),
        "title": "Exhortation to Martyrdom, Addressed to Fortunatus",
        "author": "St Cyprian of Carthage",
        "date": "252 or 257",
        "translator": "Robert Ernest Wallis",
        "pub_year": 1886,
        "source": SOURCE,
        "source_class": "patristic",
        "description": ("St Cyprian's scriptural exhortation strengthening "
                        "Christians to confess the faith under persecution."),
        "cpl": "CPL 45",
        "units": 30,
        "tree_nodes": 33,
        "notes": 119,
        "first_heading": "Exhortation to Martyrdom, Addressed to Fortunatus.[1]",
        "last_heading": "13.",
        "first_text": "[1] [Oxford number, xiii. Assigned to a.d. 252 or 257.]",
        "last_text": (" to retain the fact that for three hundred years to be "
                      "a Christian was to be a martyr, at least in spirit and "
                      "in daily liability. 1 Cor. xv. 31; 1 Pet. iv. 12.]"),
        "tree_digest": "93b4dc7f68bab5b4930a76a8504787734268a04e829179c9d433dc40e0c16129",
        "bibliographic_digest": "d30655215647842567d012474a9373a38df273926deb5090342b07fbedef6381",
        "digest": "0d4423233b61c749d720f2958b2ee17e657d1b1cbd1a488815ed9a666acf6327",
    },
    {
        "work_id": "cyprian-three-books-of-testimonies",
        "version_url": ("https://bkv.unifr.ch/en/works/cpl-39-1/versions/"
                        "three-books-of-testimonies-against-the-jews"),
        "title": "Three Books of Testimonies Against the Jews",
        "author": "St Cyprian of Carthage",
        "date": "c. 248",
        "translator": "Robert Ernest Wallis",
        "pub_year": 1886,
        "source": SOURCE,
        "source_class": "patristic",
        "description": ("St Cyprian's three-book collection of scriptural "
                        "testimonies addressed to Quirinus."),
        "cpl": "CPL 39",
        "units": 178,
        "tree_nodes": 178,
        "notes": 825,
        "first_heading": "Three Books of Testimonies Against the Jews.[1]",
        "last_heading": "120.",
        "first_text": ("Cyprian to his son Quirinus, greeting. It was necessary, "
                       "my beloved son, that I should obey your spiritual desire, "
                       "which asked with most urgent petition for those divine "
                       "teachings"),
        "last_text": ("[In a day when there were few Bibles, and no printed "
                      "books, no concordances, and no published collections of "
                      "this sort, "
                      "reflect on the value of this treatise to a young believer, "
                      "and on the labour of his pastor in making it.]"),
        "tree_digest": "0044eb647399043345fb695b46a89594952bb2726d2a7d0f253172d814ff07cc",
        "bibliographic_digest": "d30655215647842567d012474a9373a38df273926deb5090342b07fbedef6381",
        "digest": "d156926347b4b87c9c3822e1f218898b3e94ef4a40a9f17279cbc2848c390c50",
    },
    {
        "work_id": "seventh-council-of-carthage",
        "version_url": ("https://bkv.unifr.ch/en/works/cpl-56/versions/"
                        "the-seventh-council-of-carthage-under-cyprian"),
        "title": "The Seventh Council of Carthage Under Cyprian",
        "author": "The eighty-seven bishops at Carthage",
        "date": "256",
        "translator": "Robert Ernest Wallis",
        "pub_year": 1886,
        "source": SOURCE,
        "source_class": "conciliar",
        "description": ("The record of the bishops assembled at Carthage "
                        "under St Cyprian concerning the baptism of heretics. "
                        "The ANF prooemium printed within this edition dates "
                        "the council to 258; the assembly took place in 256."),
        "cpl": "CPL 56",
        "units": 3,
        "tree_nodes": 3,
        "notes": 141,
        "first_heading": "The Seventh Council of Carthage under Cyprian. [1]",
        "last_heading": "Final Word",
        "first_text": ("Concerning the Baptism of Heretics. The Judgment of "
                       "Eighty-Seven Bishops on the Baptism of Heretics.\n\n"
                       "[1] [On councils, see Oxford trans., pp. 232, 240.]"),
        "last_text": ("]\n\n[1] [Here Cyprian sums up, and gives the sentence of the "
                      "council, after the example of St. James, who presided in "
                      "the Council of Jerusalem, Acts xv. 13, 19.]"),
        "tree_digest": "55d279a3c953ba6286e049f7a74d35c986ae8330d1e8c34749fd9c2e3380455e",
        "bibliographic_digest": "d30655215647842567d012474a9373a38df273926deb5090342b07fbedef6381",
        "digest": "9eec3e2d8ec74b264e41ea5cad5d75cb1b4918064b51cc26ba815084100b7fd5",
    },
]


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def quoted_url(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc,
                                    urllib.parse.quote(parts.path),
                                    parts.query, parts.fragment))


def fetch(url, cache_name):
    path = CACHE / cache_name
    if path.exists():
        return path.read_text(encoding="utf-8")
    request = urllib.request.Request(quoted_url(url), headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=45) as response:
        body = response.read().decode("utf-8")
    path.write_text(body, encoding="utf-8")
    return body


def house(value):
    value = html.unescape(value or "").translate(HOUSE_TRANSLATION)
    return re.sub(r"\s+", " ", value).strip()


def fragment_text(fragment):
    def note_ref(match):
        label = house(re.sub(r"<[^>]+>", "", match.group(1)))
        return "[%s]" % label

    fragment = re.sub(
        r'<sup\b[^>]*>\s*<a\b[^>]*class="[^"]*footnote-ref[^"]*"[^>]*>'
        r'(.*?)</a>\s*</sup>', note_ref, fragment, flags=re.I | re.S)
    fragment = re.sub(
        r'<a\b[^>]*class="[^"]*footnote-backref[^"]*"[^>]*>.*?</a>',
        "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    return house(re.sub(r"<[^>]+>", "", fragment))


def version_record(entry):
    raw = fetch(entry["version_url"], entry["work_id"] + "-version.html")
    match = re.search(r'<h3>Bibliographic Reference</h3>\s*<p>(.*?)</p>',
                      raw, flags=re.I | re.S)
    if not match:
        raise ValueError("%s: bibliographic record is missing" % entry["work_id"])
    bibliography = fragment_text(match.group(1))
    required = ("ANTE-NICENE FATHERS VOLUME 5",
                "Alexander Roberts", "James Donaldson", "A. Cleveland Coxe",
                "Christian Literature Publishing Company, 1886",
                "Translation, English", entry["cpl"])
    visible = fragment_text(raw)
    missing = [value for value in required if value not in visible]
    if missing:
        raise ValueError("%s: edition metadata changed or is incomplete: %s" %
                         (entry["work_id"], ", ".join(missing)))
    tree_match = re.search(r'<collapsible-tree\s+:data="([^"]+)"', raw,
                           flags=re.I | re.S)
    if not tree_match:
        raise ValueError("%s: division tree is missing" % entry["work_id"])
    try:
        tree = json.loads(html.unescape(tree_match.group(1)))
    except (TypeError, ValueError) as exc:
        raise ValueError("%s: invalid division tree: %s" %
                         (entry["work_id"], exc))
    if not isinstance(tree, list) or not tree:
        raise ValueError("%s: empty division tree" % entry["work_id"])
    ids = [node.get("division_id") for node in tree]
    if any(not isinstance(value, int) for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("%s: invalid or duplicate division IDs" % entry["work_id"])
    canonical = [{key: node.get(key) for key in
                  ("division_id", "parent", "depth", "title", "has_valid_content")}
                 for node in tree]
    tree_digest = sha256_text(json.dumps(canonical, ensure_ascii=False,
                                         separators=(",", ":")))
    valid = [node for node in tree if node.get("has_valid_content")]
    if not valid:
        raise ValueError("%s: no readable divisions" % entry["work_id"])
    return bibliography, sha256_text(bibliography), tree, valid, tree_digest


def parse_division(entry, node):
    division_id = node["division_id"]
    url = "%s/divisions/%d" % (entry["version_url"], division_id)
    raw = fetch(url, "%s-division-%d.html" % (entry["work_id"], division_id))
    match = re.search(r'<div class="">\s*(.*?)\s*<div class="ornament">',
                      raw, flags=re.I | re.S)
    if not match:
        raise ValueError("%s: division %d page structure changed" %
                         (entry["work_id"], division_id))
    content = match.group(1)
    heading_match = re.search(r'<h([1-6])>(.*?)</h\1>', content,
                              flags=re.I | re.S)
    if not heading_match:
        raise ValueError("%s: division %d has no heading" %
                         (entry["work_id"], division_id))
    heading = fragment_text(heading_match.group(2))
    tree_heading = house(node.get("title") or "")
    without_refs = re.sub(r"\s*\[\d+\]\s*", " ", heading).strip()
    if without_refs != tree_heading:
        raise ValueError("%s: division %d heading differs from tree: %r / %r" %
                         (entry["work_id"], division_id, heading, tree_heading))

    parts = re.split(r'<div class="footnotes">', content, maxsplit=1,
                     flags=re.I)
    literary = parts[0]
    literary = literary[:heading_match.start()] + literary[heading_match.end():]
    paragraphs_html = re.findall(r"<p>(.*?)</p>", literary,
                                 flags=re.I | re.S)
    paragraphs = [fragment_text(value) for value in paragraphs_html]
    paragraphs = [value for value in paragraphs if value]
    residue = re.sub(r"<p>.*?</p>", "", literary, flags=re.I | re.S)
    if fragment_text(residue):
        raise ValueError("%s: unparsed literary content in division %d" %
                         (entry["work_id"], division_id))
    references = re.findall(
        r'<a\b[^>]*href="#(fn:[^"]+)"[^>]*class="[^"]*footnote-ref[^"]*"'
        r'[^>]*>(.*?)</a>', content if len(parts) == 1 else parts[0],
        flags=re.I | re.S)
    ref_ids = [item[0] for item in references]
    ref_labels = [fragment_text(item[1]) for item in references]
    if len(ref_ids) != len(set(ref_ids)):
        raise ValueError("%s: duplicate note reference in division %d" %
                         (entry["work_id"], division_id))

    notes = []
    if len(parts) == 2:
        note_rows = re.findall(
            r'<li\s+id="(fn:[^"]+)">\s*<p>(.*?)</p>\s*</li>',
            parts[1], flags=re.I | re.S)
        notes = [(note_id, fragment_text(value)) for note_id, value in note_rows]
        if any(not value for _, value in notes):
            raise ValueError("%s: empty note in division %d" %
                             (entry["work_id"], division_id))
    note_ids = [item[0] for item in notes]
    if ref_ids != note_ids:
        raise ValueError("%s: notes do not map exactly in division %d" %
                         (entry["work_id"], division_id))

    text = "\n\n".join(paragraphs)
    if notes:
        if text:
            text += "\n\n"
        text += "\n\n".join(
            "[%s] %s" % (label, note)
            for label, (_, note) in zip(ref_labels, notes))
    if not text:
        text = heading
    return heading, text, len(notes)


def validate_text(entry, units):
    for unit in units:
        text = unit["text"]
        if "\ufffd" in text:
            raise ValueError("%s: replacement character in division %d" %
                             (entry["work_id"], unit["ordinal"]))
        if re.search(r"[\u2010-\u2015]", text):
            raise ValueError("%s: forbidden dash in division %d" %
                             (entry["work_id"], unit["ordinal"]))
        if re.search(r"[\u2018-\u201f]", text):
            raise ValueError("%s: curly quote in division %d" %
                             (entry["work_id"], unit["ordinal"]))
        artifacts = []
        for pattern, label in ((r"\bPAGE\s+\d+\b", "bare PAGE marker"),
                               (r"##\s+\d", "Markdown heading"),
                               (r"\[\^\d+\]", "Markdown footnote"),
                               (r"<[^>]+>", "HTML tag"),
                               (r"https?://", "source URL"),
                               (r"\u21a9", "note backlink")):
            if re.search(pattern, text, flags=re.I):
                artifacts.append(label)
        if artifacts:
            raise ValueError("%s: source artifacts in division %d: %s" %
                             (entry["work_id"], unit["ordinal"],
                              ", ".join(artifacts)))


def work_record(entry):
    keys = ("work_id", "title", "author", "date", "translator", "pub_year",
            "source", "source_class", "description")
    work = {key: entry[key] for key in keys}
    work.update({
        "language": "en",
        "publisher": "Christian Literature Publishing Company, Buffalo",
        "source_url": entry["version_url"],
        "source_facsimile_url": FACSIMILE,
        "digitized": DIGITIZED,
        "rights": RIGHTS,
        "rights_url": RIGHTS_URL,
        "modifications": "Typography and spacing normalized by Plithos.",
    })
    return work


def build(entry, probe=False):
    bibliography, bib_digest, tree, valid, tree_digest = version_record(entry)
    with ThreadPoolExecutor(max_workers=8) as pool:
        parsed = list(pool.map(lambda node: parse_division(entry, node), valid))
    rows = [(heading, text) for heading, text, _ in parsed]
    note_count = sum(notes for _, _, notes in parsed)
    units = [{
        "unit_id": "%s::u%03d" % (entry["work_id"], ordinal),
        "work_id": entry["work_id"],
        "work_title": entry["title"],
        "author": entry["author"],
        "source_class": entry["source_class"],
        "ordinal": ordinal,
        "citation_anchor": heading,
        "text": text,
    } for ordinal, (heading, text) in enumerate(rows, 1)]
    validate_text(entry, units)
    canonical = json.dumps({"headings": [row[0] for row in rows],
                            "texts": [row[1] for row in rows]},
                           ensure_ascii=False, separators=(",", ":"))
    digest = sha256_text(canonical)
    report = {
        "units": len(units), "tree_nodes": len(tree), "notes": note_count,
        "first_heading": rows[0][0], "last_heading": rows[-1][0],
        "first_text": rows[0][1][:160], "last_text": rows[-1][1][-160:],
        "tree_digest": tree_digest, "bibliographic_digest": bib_digest,
        "digest": digest, "bibliography": bibliography,
    }
    if not probe:
        for key in ("units", "tree_nodes", "notes", "first_heading",
                    "last_heading", "tree_digest", "bibliographic_digest",
                    "digest"):
            if entry[key] != report[key]:
                raise ValueError("%s: %s changed: %r, expected %r" %
                                 (entry["work_id"], key, report[key], entry[key]))
        if not rows[0][1].startswith(entry["first_text"]):
            raise ValueError("%s: first text changed" % entry["work_id"])
        if not rows[-1][1].endswith(entry["last_text"]):
            raise ValueError("%s: last text changed" % entry["work_id"])
    return {"work": work_record(entry), "units": units}, report


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--write-files-only", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--probe", action="store_true")
    parser.add_argument("--only", choices=[item["work_id"] for item in CATALOGUE])
    args = parser.parse_args()
    selected = [item for item in CATALOGUE
                if not args.only or item["work_id"] == args.only]
    outputs = []
    for entry in selected:
        try:
            output, report = build(entry, probe=args.probe)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            print(exc, file=sys.stderr)
            return 1
        outputs.append((entry, output))
        print("%s: %d divisions, %d tree nodes, %d notes, %s characters, sha256 %s" %
              (entry["work_id"], report["units"], report["tree_nodes"],
               report["notes"],
               format(sum(len(unit["text"]) for unit in output["units"]), ","),
               report["digest"]))
        if args.probe:
            print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.probe:
        return 0
    if args.write or args.write_files_only:
        for entry, output in outputs:
            destination = OUTDIR / (entry["work_id"] + ".json")
            destination.write_text(json.dumps(output, ensure_ascii=False,
                                              indent=1) + "\n",
                                   encoding="utf-8")
            print("wrote %s" % destination.relative_to(ROOT))
        if args.write:
            index = json.loads(INDEX.read_text(encoding="utf-8"))
            ids = {entry["work_id"] for entry, _ in outputs}
            index = [item for item in index if item.get("work_id") not in ids]
            index.extend(output["work"] for _, output in outputs)
            index.sort(key=lambda item: item["work_id"])
            INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n",
                             encoding="utf-8")
            print("updated %s" % INDEX.relative_to(ROOT))
        return 0

    failed = False
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    indexed = {item.get("work_id"): item for item in index}
    for entry, output in outputs:
        destination = OUTDIR / (entry["work_id"] + ".json")
        body = json.dumps(output, ensure_ascii=False, indent=1) + "\n"
        try:
            actual = destination.read_text(encoding="utf-8")
        except OSError as exc:
            print("stale or missing %s: %s" % (destination.relative_to(ROOT), exc))
            failed = True
            continue
        if actual != body:
            print("stale %s" % destination.relative_to(ROOT))
            failed = True
        indexed_work = indexed.get(entry["work_id"])
        if indexed_work is None or any(indexed_work.get(key) != value
                                       for key, value in output["work"].items()):
            print("stale catalogue record: %s" % entry["work_id"])
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
