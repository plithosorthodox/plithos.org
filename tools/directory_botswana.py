#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Botswana.

The Patriarchate of Alexandria already publishes Botswana's diocesan parent
in the directory spine. Its current material does not establish a completed
Alexandrian parish building by a stable current name. The Serbian Patriarchate
does establish the Church of Saint Sava in Gaborone as a current worshipping
body under the blessing of the Serbian Patriarch, so that church is published
directly beneath the Church of Serbia.

    python tools/directory_botswana.py --check
    python tools/directory_botswana.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

SPC_PAINTING = (
    "https://spc.rs/sr/news/3217."
    "nastavljeno-oslikavanje-crkve-svetog-save-u-bocvani.html"
)
SPC_WEDDING = (
    "https://spc.rs/sr/news/3405."
    "prvo-vencanje-u-crkvi-svetog-save-u-gaboronu%2C-bocvana.html"
)
AX_VISIT = (
    "https://www.patriarchateofalexandria.com/"
    "alexandrian-patriarch-s-visit-to-botswana/?lang=en"
)


DIRECT_SERBIA_ROWS = [
    {
        "id": "bw-sr-gaborone-saint-sava",
        "parent": "serbia",
        "kind": "parish",
        "rank": "Church",
        "name": "Church of Saint Sava in Gaborone",
        "local": "Храм Светог Саве у Габорону",
        "country": "BW",
        "checked": CHECKED,
        "sources": [SPC_PAINTING, SPC_WEDDING, AX_VISIT],
    },
]

EXPECTED = 1
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for row in DIRECT_SERBIA_ROWS
}


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    return row


def build_direct():
    rows = []
    seen = {"serbia"}
    for source in DIRECT_SERBIA_ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != "serbia":
            raise ValueError("%s does not answer to the Church of Serbia" %
                             row_id)
        if row.get("country") != "BW":
            raise ValueError("%s is outside Botswana" % row_id)
        if row.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable name" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED:
        raise ValueError("Botswana must publish exactly %d direct Serbian row" %
                         EXPECTED)
    if set(ENGLISH_NAMES) != seen - {"serbia"}:
        raise ValueError("Botswana English name map is out of sync")
    return rows


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        rows = build_direct()
    except (OSError, ValueError) as exc:
        print("directory Botswana: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(
            {"parent": "serbia", "country": "BW", "rows": rows},
            ensure_ascii=False, indent=2, sort_keys=True,
        ))
    print("Botswana: 1 current officially named body, plus the existing "
          "Alexandrian diocesan parent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
