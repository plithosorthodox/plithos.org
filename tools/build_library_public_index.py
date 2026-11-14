#!/usr/bin/env python3
"""Build the versioned public Library catalogue snapshot.

Library ingest and editorial tools continue to update the canonical catalogue
at data/library/works-index.json. The page reads a versioned copy so a reader
cannot retain an older catalogue after new sections or works are published.

    python tools/build_library_public_index.py --check
    python tools/build_library_public_index.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "library" / "works-index.json"
OUTPUT = ROOT / "data" / "library-index.v1.json"


def read_catalog():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("canonical Library catalogue must be a non-empty list")
    seen = set()
    for number, work in enumerate(data, 1):
        if not isinstance(work, dict):
            raise ValueError("catalogue entry %d is not an object" % number)
        work_id = work.get("work_id")
        if not work_id:
            raise ValueError("catalogue entry %d has no work_id" % number)
        if work_id in seen:
            raise ValueError("duplicate work_id: " + work_id)
        seen.add(work_id)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Build the versioned public Library catalogue snapshot")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        catalog = read_catalog()
        expected = (json.dumps(catalog, ensure_ascii=False, indent=2)
                    + "\n").encode("utf-8")
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1

    if args.write:
        OUTPUT.write_bytes(expected)
        print("wrote %s (%d works)" %
              (OUTPUT.relative_to(ROOT), len(catalog)))
        return 0

    if not OUTPUT.exists():
        print("error: %s is missing; run with --write" %
              OUTPUT.relative_to(ROOT), file=sys.stderr)
        return 1
    if OUTPUT.read_bytes() != expected:
        print("error: %s is stale; run with --write" %
              OUTPUT.relative_to(ROOT), file=sys.stderr)
        return 1
    print("public Library catalogue matches the canonical index")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
