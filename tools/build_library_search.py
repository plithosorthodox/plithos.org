#!/usr/bin/env python3
"""Build the versioned work-level index for Library text search.

The browser uses a query token to fetch one small shard, intersects or joins
the work numbers in those postings, and then fetches only those work files.
The work itself remains the authority for exact phrase matching and snippets.

    python tools/build_library_search.py --write
    python tools/build_library_search.py --check

Files under /data are immutable. If the indexed corpus changes, increment
VERSION before writing. This script will not replace a different file inside
an existing version directory.
"""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "data" / "library"
VERSION = 2
SHARD_COUNT = 64
OUTPUT = LIBRARY / ("search-v%d" % VERSION)

RUNS = re.compile(
    r"[0-9a-z\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff"
    r"\u0530-\u058f\u0590-\u05ff\u0600-\u06ff\u0700-\u074f"
    r"\u0900-\u097f\u0980-\u09ff\u10a0-\u10ff"
    r"\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]+"
)
CJK = re.compile(r"^[\u3040-\u30ff\u3400-\u9fff]+$")
HANGUL = re.compile(r"[\uac00-\ud7af]")
COMBINING_LATIN = re.compile(r"[\u0300-\u036f]")
ARABIC_MARKS = re.compile(r"[\u064b-\u065f\u0670\u0640]")
ARABIC_FORMS = str.maketrans({"آ": "ا", "أ": "ا", "إ": "ا",
                              "ى": "ي", "ة": "ه", "ς": "σ"})


def fold(value):
    """Match library.html fold() for every script it normalizes."""
    text = unicodedata.normalize("NFD", str(value or "").lower())
    text = COMBINING_LATIN.sub("", text)
    text = ARABIC_MARKS.sub("", text).translate(ARABIC_FORMS)
    return unicodedata.normalize("NFC", text)


def tokens(value):
    """Match library.html tok(), including CJK bigrams and Hangul words."""
    out = []
    for run in RUNS.findall(fold(value)):
        if CJK.match(run):
            if len(run) < 2:
                out.append(run)
            else:
                out.extend(run[i:i + 2] for i in range(len(run) - 1))
        elif HANGUL.search(run):
            out.append(run)
        elif len(run) > 2:
            out.append(run)
    return out


def shard_number(token):
    """A 32-bit hash reproduced by the ES5 lookup loop in library.html."""
    value = 0
    for char in token:
        value = ((value * 33) + ord(char)) & 0xffffffff
    return value & (SHARD_COUNT - 1)


def compact(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def read_works():
    works = []
    errors = []
    for path in sorted(LIBRARY.glob("*.json"), key=lambda p: p.name):
        if path.name == "works-index.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append("%s: invalid JSON: %s" % (path.name, exc))
            continue
        work = data.get("work") if isinstance(data, dict) else None
        units = data.get("units") if isinstance(data, dict) else None
        if not isinstance(work, dict) or not isinstance(units, list):
            errors.append("%s: expected {work, units}" % path.name)
            continue
        work_id = work.get("work_id")
        if not work_id or work_id != path.stem:
            errors.append("%s: work_id does not match filename" % path.name)
            continue
        if not units:
            errors.append("%s: no units" % path.name)
            continue
        bad = [i for i, unit in enumerate(units)
               if not isinstance(unit, dict) or unit.get("work_id") != work_id
               or not isinstance(unit.get("text"), str)]
        if bad:
            errors.append("%s: invalid units at %s" %
                          (path.name, ", ".join(map(str, bad[:8]))))
            continue
        work_tokens = set()
        for unit in units:
            work_tokens.update(tokens(unit.get("text") or ""))
        works.append({"id": work_id, "units": len(units),
                      "tokens": work_tokens})
    if errors:
        raise ValueError("\n".join(errors))
    ids = [item["id"] for item in works]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate work_id in library files")
    return works


def build():
    works = read_works()
    postings = [{} for _ in range(SHARD_COUNT)]
    unit_count = 0
    for number, item in enumerate(works):
        unit_count += item["units"]
        for token in sorted(item["tokens"]):
            postings[shard_number(token)].setdefault(token, []).append(number)

    files = {}
    shard_meta = []
    token_count = 0
    posting_count = 0
    for number, shard in enumerate(postings):
        name = "%02x.json" % number
        body = compact(shard)
        digest = hashlib.sha256(body).hexdigest()
        count = len(shard)
        postings_here = sum(len(values) for values in shard.values())
        token_count += count
        posting_count += postings_here
        files[name] = body
        shard_meta.append({"file": name, "tokens": count,
                           "postings": postings_here, "bytes": len(body),
                           "sha256": digest})

    manifest = {
        "format": "plithos-library-search",
        "version": VERSION,
        "source": "data/library/<work_id>.json units[].text",
        "tokenizer": "library.html fold/tok",
        "hash": "h=((h*33)+charCodeAt(i))>>>0; shard=h&63",
        "shard_count": SHARD_COUNT,
        "work_count": len(works),
        "unit_count": unit_count,
        "token_count": token_count,
        "posting_count": posting_count,
        "works": [item["id"] for item in works],
        "shards": shard_meta,
    }
    files["manifest.json"] = compact(manifest)
    return files, manifest


def compare(files):
    problems = []
    for name, body in sorted(files.items()):
        path = OUTPUT / name
        if not path.exists():
            problems.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes() != body:
            problems.append("stale %s" % path.relative_to(ROOT))
    if OUTPUT.exists():
        expected = set(files)
        for path in OUTPUT.iterdir():
            if path.is_file() and path.name not in expected:
                problems.append("unexpected %s" % path.relative_to(ROOT))
    return problems


def write(files):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, body in sorted(files.items()):
        path = OUTPUT / name
        if path.exists() and path.read_bytes() != body:
            raise ValueError(
                "%s is immutable and differs; increment VERSION" %
                path.relative_to(ROOT))
        path.write_bytes(body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check:
        parser.error("choose --write or --check")
    try:
        files, manifest = build()
        if args.write:
            write(files)
        problems = compare(files)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    total = sum(len(body) for body in files.values())
    print("library search v%d: %d works, %d units, %d tokens, %d postings, %d bytes" %
          (manifest["version"], manifest["work_count"],
           manifest["unit_count"], manifest["token_count"],
           manifest["posting_count"], total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
