#!/usr/bin/env python3
"""Publish country contributions to shared Oceania branches.

Country modules keep their official-source audits and exact local counts.
This owner combines their rows under the regional parent IDs which span
Australia and New Zealand. The ROCOR branch is owned by directory_korea
because that same diocese also has subordinate bodies in Korea.
"""

import argparse
import json
import sys
from pathlib import Path

import directory_new_zealand


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
SOURCE_MODULES = (directory_new_zealand,)
EXCLUDED_PARENTS = {"ru-australia-and-new-zealand-rocor"}


def build():
    payloads = {}
    countries = {}
    row_ids = set()
    for module in SOURCE_MODULES:
        for parent, contribution in module.build().items():
            if parent in EXCLUDED_PARENTS:
                continue
            payload = payloads.setdefault(
                parent, {"v": 1, "parent": parent, "rows": []})
            parent_countries = countries.setdefault(parent, set())
            for row in contribution:
                row_id = row.get("id")
                if not row_id or row_id in row_ids:
                    raise ValueError("duplicate or missing row id: %s" % row_id)
                if row.get("parent") != parent:
                    raise ValueError("%s belongs to the wrong parent" % row_id)
                country = row.get("country")
                if not country:
                    raise ValueError("%s lacks a country" % row_id)
                row_ids.add(row_id)
                parent_countries.add(country)
                payload["rows"].append(row)
    for parent, payload in payloads.items():
        scope = sorted(countries[parent])
        if len(scope) == 1:
            payload["country"] = scope[0]
        else:
            payload["countries"] = scope
    if len(payloads) != 5 or sum(len(p["rows"]) for p in payloads.values()) != 25:
        raise ValueError("Oceania must publish 5 parents and 25 rows")
    return dict(sorted(payloads.items()))


def manifest(payloads=None):
    payloads = payloads or build()
    answer = {}
    for parent, payload in payloads.items():
        entry = {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
        }
        if "countries" in payload:
            entry["countries"] = payload["countries"]
        else:
            entry["country"] = payload["country"]
        answer[parent] = entry
    return answer


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in payloads.items():
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    for parent, payload in payloads.items():
        path = output_path(parent)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Oceania: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Oceania branches: 5 parents, 25 subordinate bodies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
