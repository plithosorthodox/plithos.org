#!/usr/bin/env python3
"""Keep narrow, reviewed corrections to embedded Library catalog copy."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"
HEAD = "const CORPUS = "

REPAIRS = {
    "divine-liturgy-chrysostom-ro": {
        "before": (
            "The Romanian text of the principal Eucharistic service of the "
            "Orthodox Church, attributed to St. John Chrysostom. Romanian is "
            "the liturgical language of the Russian and other Slavic Orthodox "
            "Churches. The received liturgical text, public domain."
        ),
        "after": (
            "The Romanian text of the principal Eucharistic service of the "
            "Orthodox Church, attributed to St. John Chrysostom. Romanian is "
            "the liturgical language of the Romanian Orthodox Church. The "
            "received liturgical text, public domain."
        ),
    },
}


def read_assignment(source):
    start = source.index(HEAD) + len(HEAD)
    end = source.index("\n", start)
    literal = source[start:end].rstrip().rstrip(";")
    data = json.loads(literal)
    roundtrip = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if roundtrip != literal:
        raise ValueError("CORPUS no longer has its canonical serialization")
    return start, end, data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    source = PAGE.read_text(encoding="utf-8")
    start, end, corpus = read_assignment(source)
    by_id = {work["work_id"]: work for work in corpus.get("works", [])}
    changes = 0
    for work_id, repair in REPAIRS.items():
        work = by_id.get(work_id)
        if not work:
            raise ValueError("missing embedded work: " + work_id)
        value = work.get("description")
        if value == repair["after"]:
            continue
        if value != repair["before"]:
            raise ValueError("unexpected description for " + work_id)
        work["description"] = repair["after"]
        changes += 1

    print("library metadata repairs: %d change(s) needed" % changes)
    if changes and args.write:
        literal = json.dumps(corpus, ensure_ascii=False, separators=(",", ":"))
        PAGE.write_text(source[:start] + literal + ";" + source[end:],
                        encoding="utf-8")
        print("updated library.html")
    return 1 if changes and not args.write else 0


if __name__ == "__main__":
    raise SystemExit(main())
