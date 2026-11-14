#!/usr/bin/env python3
"""Build the source-bound Arabic parallel Liturgy sections.

The 1890 Beirut edition is transcribed by printed page. The Library's five
older Chrysostom editions are divided into eleven service sections. This
builder follows the checked boundary map, preserves every Arabic source line
exactly once, and emits section blocks for the comparative reader. Material
printed after the ordinary dismissal remains an Arabic-only appendix.

    PYTHONUTF8=1 python tools/build_arabic_liturgy_alignment.py --check
    PYTHONUTF8=1 python tools/build_arabic_liturgy_alignment.py --write
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "tools" / "manuscripts" / "messara_1890_chrysostom_alignment.json"
OUT = ROOT / "data" / "library" / "liturgy-align.chrysostom.ar.v1.json"
FORBIDDEN = ("\u2013", "\u2014", "\ufffd")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten(spec: dict) -> list[dict]:
    rows: list[dict] = []
    for source in spec["source_files"]:
        path = ROOT / source["path"]
        actual = digest(path)
        if actual != source["sha256"]:
            raise ValueError("%s has SHA-256 %s, expected %s"
                             % (source["path"], actual, source["sha256"]))
        data = load(path)
        for page in data["pages"]:
            for block in page["blocks"]:
                for position, line in enumerate(block["lines"], 1):
                    if line["line"] != position:
                        raise ValueError("%s line order changed" % block["block_id"])
                    text = line["text"]
                    if any(mark in text for mark in FORBIDDEN):
                        raise ValueError("%s:%s contains a forbidden character"
                                         % (block["block_id"], position))
                    rows.append({
                        "ref": "%s:%s" % (block["block_id"], position),
                        "scan_page": page["scan_page"],
                        "block_id": block["block_id"],
                        "line": position,
                        "role": block["role"],
                        "text": text,
                    })
    return rows


def check_boundary(label: str, expected: dict, actual: dict) -> None:
    for key in ("ref", "scan_page", "block_id", "line", "role", "text"):
        if expected.get(key) != actual.get(key):
            raise ValueError("%s %s changed" % (label, key))


def blocks(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        if (not out or out[-1]["block_id"] != row["block_id"]):
            out.append({
                "block_id": row["block_id"],
                "scan_page": row["scan_page"],
                "role": row["role"],
                "start_ref": row["ref"],
                "end_ref": row["ref"],
                "text": row["text"],
            })
        else:
            out[-1]["end_ref"] = row["ref"]
            out[-1]["text"] += "\n" + row["text"]
    return out


def build_range(item: dict, rows: list[dict]) -> dict:
    result = {
        "key": item["key"],
        "title": item["title"],
        "kind": item["kind"],
        "start_ref": rows[0]["ref"],
        "end_ref": rows[-1]["ref"],
        "line_count": len(rows),
        "blocks": blocks(rows),
    }
    if "section_index" in item:
        result["section_index"] = item["section_index"]
    if "appendix_index" in item:
        result["appendix_index"] = item["appendix_index"]
    return result


def build(spec: dict) -> dict:
    if spec.get("format") != "plithos-liturgy-source-section-map":
        raise ValueError("wrong map format")
    if spec.get("version") != 1:
        raise ValueError("wrong map version")
    rows = flatten(spec)
    refs = [row["ref"] for row in rows]
    if len(refs) != len(set(refs)):
        raise ValueError("source references are not unique")
    coverage = spec["coverage"]
    if len(rows) != coverage["expected_line_count"]:
        raise ValueError("source line count changed")
    if refs[0] != coverage["first"] or refs[-1] != coverage["last"]:
        raise ValueError("source coverage endpoints changed")
    lookup = {ref: i for i, ref in enumerate(refs)}

    cursor = 0
    made_sections: list[dict] = []
    made_appendices: list[dict] = []
    for item in spec["sections"] + spec["appendices"]:
        start = lookup.get(item["start"]["ref"])
        end = lookup.get(item["end"]["ref"])
        if start is None or end is None or end < start:
            raise ValueError("%s has an invalid range" % item["key"])
        if start != cursor:
            raise ValueError("%s is not adjacent to the preceding range"
                             % item["key"])
        selected = rows[start:end + 1]
        if len(selected) != item["expected_line_count"]:
            raise ValueError("%s line count changed" % item["key"])
        check_boundary(item["key"] + " start", item["start"], selected[0])
        check_boundary(item["key"] + " end", item["end"], selected[-1])
        built = build_range(item, selected)
        if item["kind"] == "comparator":
            made_sections.append(built)
        else:
            made_appendices.append(built)
        cursor = end + 1
    if cursor != len(rows):
        raise ValueError("mapped ranges do not cover every source line")
    if [item["section_index"] for item in made_sections] != list(range(11)):
        raise ValueError("comparator sections are not zero through ten")

    return {
        "format": "plithos-liturgy-alignment",
        "version": 1,
        "group_id": spec["edition_of"],
        "work_id": spec["work_id"],
        "language": spec["language"],
        "source": spec["source"],
        "source_line_count": len(rows),
        "sections": made_sections,
        "appendices": made_appendices,
    }


def serialise(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=1) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    expected = build(load(MAP))
    text = serialise(expected)
    if args.write:
        OUT.write_text(text, encoding="utf-8")
        print("wrote %s" % OUT.relative_to(ROOT))
    elif not OUT.is_file():
        raise SystemExit("%s is missing" % OUT.relative_to(ROOT))
    elif OUT.read_text(encoding="utf-8") != text:
        raise SystemExit("%s is stale" % OUT.relative_to(ROOT))
    print("OK Arabic Liturgy alignment: 11 sections, 1 appendix, %d source lines"
          % expected["source_line_count"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
