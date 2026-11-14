#!/usr/bin/env python3
"""Build and publish complete Greek BKV editions.

The University of Fribourg BKV site exposes these editions as one division
per web page rather than as EPUB downloads. This builder reads the asserted
division tree, keeps every valid division and every note, and writes only the
individual Library JSON files. It deliberately does not edit the catalogue,
search data, page data, tags, topics, or reception records.

    python3 tools/ingest_bkv_greek.py --check
    python3 tools/ingest_bkv_greek.py --write-files-only
    python3 tools/ingest_bkv_greek.py --write --only justin-first-apology-grc
"""
import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import sys
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path(tempfile.gettempdir()) / "plithos-bkv-greek"
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
DIGITIZED = "University of Fribourg, Bibliothek der Kirchenväter"
RIGHTS = "Public domain"
RIGHTS_URL = "https://bkv.unifr.ch/en/about/copyrights"


CATALOGUE = [
    {
        "work_id": "justin-first-apology-grc",
        "edition_of": "justin-first-apology",
        "url": "https://bkv.unifr.ch/en/works/cpg-1073a/versions/apologia-prima",
        "title": "Ἀπολογία πρώτη",
        "author": "St Justin the Philosopher",
        "date": "c. 155",
        "editor": "Edgar J. Goodspeed",
        "pub_year": 1915,
        "source": "Die ältesten Apologeten, edited by Edgar J. Goodspeed (Göttingen: Vandenhoeck & Ruprecht, 1915), pp. 26-77",
        "description": "The complete Greek text of St Justin's First Apology in Edgar J. Goodspeed's 1915 edition.",
        "tree_nodes": 69,
        "units": 68,
        "first_heading": "1",
        "last_heading": "68",
        "metadata_markers": ("E. J. Goodspeed", "1915", "Edition, Greek", "CPG 1073a"),
        "digest": "7a465b88bd42a172dd5994b3709385114ea1fab992e3620655d4a3b96e3ea6d4",
    },
    {
        "work_id": "justin-second-apology-grc",
        "edition_of": "justin-second-apology",
        "url": "https://bkv.unifr.ch/en/works/cpg-1073b/versions/apologia-secunda",
        "title": "Ἀπολογία δευτέρα",
        "author": "St Justin the Philosopher",
        "date": "c. 155",
        "editor": "Edgar J. Goodspeed",
        "pub_year": 1915,
        "source": "Die ältesten Apologeten, edited by Edgar J. Goodspeed (Göttingen: Vandenhoeck & Ruprecht, 1915), pp. 78-89",
        "description": "The complete Greek text of St Justin's Second Apology in Edgar J. Goodspeed's 1915 edition.",
        "tree_nodes": 16,
        "units": 15,
        "first_heading": "I",
        "last_heading": "XV",
        "metadata_markers": ("E. J. Goodspeed", "1915", "Edition, Greek", "CPG 1073b"),
        "digest": "ca0246940b704655aa0390ad9df4bf21466f7d0c927d6228b7b2702e96e7ef6b",
    },
    {
        "work_id": "justin-dialogue-trypho-grc",
        "edition_of": "justin-dialogue-trypho",
        "url": "https://bkv.unifr.ch/en/works/cpg-1076/versions/dialogus-cum-tryphono-judaeo",
        "title": "Πρὸς Τρύφωνα Ἰουδαῖον διάλογος",
        "author": "St Justin the Philosopher",
        "date": "c. 160",
        "editor": "Edgar J. Goodspeed",
        "pub_year": 1915,
        "source": "Die ältesten Apologeten, edited by Edgar J. Goodspeed (Göttingen: Vandenhoeck & Ruprecht, 1915), pp. 90-265",
        "description": "The complete Greek text of St Justin's Dialogue with Trypho in Edgar J. Goodspeed's 1915 edition.",
        "tree_nodes": 143,
        "units": 142,
        "first_heading": "1",
        "last_heading": "142",
        "metadata_markers": ("E. J. Goodspeed", "1915", "Edition, Greek", "CPG 1076"),
        "digest": "6bf44185717e4d798caebd24a0cddcd3ac05a4e49c2a689473c4fafa50e8f630",
    },
]


def fetch(url, cache_name):
    path = CACHE / cache_name
    if path.exists():
        return path.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as response:
        body = response.read()
    path.write_bytes(body)
    return body


def text_fragment(value):
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value, flags=re.I | re.S)
    value = html.unescape(value).replace("\xa0", " ")
    value = (value.replace("\u2013", "-").replace("\u2014", "-")
             .replace("\u2018", "'").replace("\u2019", "'")
             .replace("\u201c", '"').replace("\u201d", '"'))
    return " ".join(value.split())


def version_tree(entry):
    raw = fetch(entry["url"], entry["work_id"] + "-version.html").decode("utf-8")
    visible = text_fragment(raw)
    missing = [marker for marker in entry["metadata_markers"] if marker not in visible]
    if missing:
        raise ValueError("%s: missing edition metadata: %s"
                         % (entry["work_id"], ", ".join(missing)))
    match = re.search(r'<collapsible-tree\s+:data="(\[.*?\])"', raw,
                      flags=re.S)
    if not match:
        raise ValueError("%s: division tree is missing" % entry["work_id"])
    tree = json.loads(html.unescape(match.group(1)))
    if len(tree) != entry["tree_nodes"]:
        raise ValueError("%s: expected %d tree nodes, found %d"
                         % (entry["work_id"], entry["tree_nodes"], len(tree)))
    valid = [node for node in tree if node["has_valid_content"]]
    if len(valid) != entry["units"]:
        raise ValueError("%s: expected %d content divisions, found %d"
                         % (entry["work_id"], entry["units"], len(valid)))
    if valid[0]["title"] != entry["first_heading"]:
        raise ValueError("%s: first heading changed" % entry["work_id"])
    if valid[-1]["title"] != entry["last_heading"]:
        raise ValueError("%s: last heading changed" % entry["work_id"])
    return valid


def replace_note_ref(match):
    label = text_fragment(match.group(0))
    return "[%s]" % label


def render_paragraph(fragment):
    fragment = re.sub(
        r'<sup\b[^>]*>\s*<a\b[^>]*class="[^"]*footnote-ref[^"]*"'
        r'[^>]*>.*?</a>\s*</sup>',
                      replace_note_ref, fragment, flags=re.I | re.S)
    fragment = re.sub(r'<a\b[^>]*class="[^"]*footnote-backref[^"]*"[^>]*>.*?</a>',
                      "", fragment, flags=re.I | re.S)
    fragment = re.sub(r'<a\b[^>]*href="[^"]*/scans/[^"]*"[^>]*>.*?</a>',
                      "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"\[P\.\s*\d+\]\(\)", "", fragment)
    return text_fragment(fragment)


def parse_division(entry, node):
    division_id = node["division_id"]
    url = entry["url"] + "/divisions/" + str(division_id)
    cache_name = "%s-division-%d.html" % (entry["work_id"], division_id)
    raw = fetch(url, cache_name).decode("utf-8")
    match = re.search(
        r'<div class="">\s*<(h1|h2)>(.*?)</\1>(.*?)'
        r'<div class="ornament">', raw, flags=re.I | re.S)
    if not match:
        raise ValueError("%s: division %d structure changed"
                         % (entry["work_id"], division_id))
    heading = text_fragment(match.group(2))
    if heading != node["title"]:
        raise ValueError("%s: division %d heading changed"
                         % (entry["work_id"], division_id))
    body = match.group(3)
    pieces = re.split(r'<div class="footnotes">', body, maxsplit=1, flags=re.I)
    paragraphs = [render_paragraph(value) for value in
                  re.findall(r"<p\b[^>]*>(.*?)</p>", pieces[0], flags=re.I | re.S)]
    paragraphs = [value for value in paragraphs if value]
    if not paragraphs:
        raise ValueError("%s: division %d is empty"
                         % (entry["work_id"], division_id))
    text = "\n\n".join(paragraphs)

    refs = re.findall(
        r'<a\b(?=[^>]*class="[^"]*footnote-ref[^"]*")'
        r'(?=[^>]*href="#fn:([^"#]+)")[^>]*>', pieces[0],
        flags=re.I | re.S)
    notes = {}
    if len(pieces) == 2:
        for note_id, fragment in re.findall(
                r'<li\s+id="fn:([^"]+)">(.*?)</li>', pieces[1], flags=re.I | re.S):
            note_parts = [render_paragraph(value) for value in
                          re.findall(r"<p\b[^>]*>(.*?)</p>", fragment,
                                     flags=re.I | re.S)]
            notes[note_id] = " ".join(value for value in note_parts if value)
    if set(refs) != set(notes):
        raise ValueError("%s: division %d note references do not match notes"
                         % (entry["work_id"], division_id))
    if refs:
        text += "\n\n" + "\n\n".join("[%s] %s" % (ref, notes[ref])
                                         for ref in refs)
    if ("\ufffd" in text or re.search(r"https?://|\[P\.\s*\d+\]", text)):
        raise ValueError("%s: division %d contains a transcription artifact"
                         % (entry["work_id"], division_id))
    return heading, text


def build(entry):
    nodes = version_tree(entry)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        rows = list(executor.map(lambda node: parse_division(entry, node), nodes))
    canonical = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if entry["digest"] and digest != entry["digest"]:
        raise ValueError("%s: source digest changed: %s"
                         % (entry["work_id"], digest))
    work = {
        "work_id": entry["work_id"],
        "edition_of": entry["edition_of"],
        "title": entry["title"],
        "author": entry["author"],
        "language": "grc",
        "date": entry["date"],
        "translator": None,
        "editor": entry["editor"],
        "pub_year": entry["pub_year"],
        "source": entry["source"],
        "source_class": "patristic",
        "description": entry["description"],
        "source_url": entry["url"] + "/divisions",
        "digitized": DIGITIZED,
        "rights": RIGHTS,
        "rights_url": RIGHTS_URL,
    }
    width = max(2, len(str(len(rows))))
    units = []
    for ordinal, (heading, text) in enumerate(rows, 1):
        units.append({
            "unit_id": "%s::u%0*d" % (entry["work_id"], width, ordinal),
            "work_id": entry["work_id"],
            "work_title": entry["title"],
            "author": entry["author"],
            "source_class": "patristic",
            "ordinal": ordinal,
            "citation_anchor": heading,
            "text": text,
        })
    return {"work": work, "units": units}, digest


def encoded(payload):
    return (json.dumps(payload, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    action.add_argument("--write-files-only", action="store_true")
    parser.add_argument("--only", action="append", default=[])
    args = parser.parse_args()

    chosen = [entry for entry in CATALOGUE
              if not args.only or entry["work_id"] in args.only]
    unknown = sorted(set(args.only) - {entry["work_id"] for entry in CATALOGUE})
    if unknown:
        raise ValueError("unknown work id: %s" % ", ".join(unknown))

    changed = []
    built = []
    for entry in chosen:
        payload, digest = build(entry)
        built.append(payload)
        path = OUTDIR / (entry["work_id"] + ".json")
        body = encoded(payload)
        current = path.read_bytes() if path.exists() else None
        if current != body:
            changed.append(entry["work_id"])
            if args.write or args.write_files_only:
                path.write_bytes(body)
        print("%s: %d units, digest %s"
              % (entry["work_id"], len(payload["units"]), digest))

    if args.check and changed:
        print("staged Greek files differ: %s" % ", ".join(changed), file=sys.stderr)
        return 1
    if args.write:
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        ids = {payload["work"]["work_id"] for payload in built}
        index = [item for item in index if item.get("work_id") not in ids]
        index.extend(payload["work"] for payload in built)
        index.sort(key=lambda item: item["work_id"])
        INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")
        print("updated %s" % INDEX.relative_to(ROOT))
    if args.write or args.write_files_only:
        print("wrote %d staged Greek file(s)" % len(changed))
    else:
        print("all staged Greek files are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
