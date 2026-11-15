#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in mainland China.

The competent Church sources distinguish two sets of bodies. Harbin and
Labdarin belong to the Chinese Autonomous Orthodox Church and remain in
directory_rows/china.py. The five bodies here are named by the Moscow
Patriarchate among its directly served communities in China.

    python tools/directory_china_mainland.py --check
    python tools/directory_china_mainland.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"
BEIJING_2026 = "https://mospat.ru/en/news/94160/"
CHINA_2024 = "https://mospat.ru/en/news/92369/"
CHINA_2025 = "https://mospat.ru/en/news/93357/"
SHANGHAI_2026 = "https://mospat.ru/en/news/94422/"


DIRECT_RUSSIA_ROWS = [
    {
        "id": "cn-ru-beijing-dormition",
        "parent": "russia",
        "kind": "parish",
        "rank": "Church",
        "name": "Church of the Dormition of the Mother of God in Beijing",
        "local": "Храм Успения Пресвятой Богородицы в Пекине",
        "seat": "Beijing",
        "country": "CN",
        "checked": CHECKED,
        "sources": [BEIJING_2026, CHINA_2025, CHINA_2024],
    },
    {
        "id": "cn-ru-shanghai-community",
        "parent": "russia",
        "kind": "parish",
        "rank": "Community",
        "name": "Orthodox Christian Community in Shanghai",
        "local": "Православная община в Шанхае",
        "seat": "Shanghai",
        "country": "CN",
        "checked": CHECKED,
        "sources": [SHANGHAI_2026, CHINA_2025, CHINA_2024],
    },
    {
        "id": "cn-ru-dalian-archangel-michael",
        "parent": "russia",
        "kind": "parish",
        "rank": "Parish",
        "name": "Archangel Michael Parish in Dalian",
        "local": "Приход Архистратига Божия Михаила в Даляне",
        "seat": "Dalian",
        "country": "CN",
        "checked": CHECKED,
        "sources": [CHINA_2025, CHINA_2024],
    },
    {
        "id": "cn-ru-shenzhen-parish",
        "parent": "russia",
        "kind": "parish",
        "rank": "Parish",
        "name": "Parish in Shenzhen",
        "local": "Приход в Шэньчжэне",
        "seat": "Shenzhen",
        "country": "CN",
        "checked": CHECKED,
        "sources": [CHINA_2024],
    },
    {
        "id": "cn-ru-guangzhou-parish",
        "parent": "russia",
        "kind": "parish",
        "rank": "Parish",
        "name": "Parish in Guangzhou",
        "local": "Приход в Гуанчжоу",
        "seat": "Guangzhou",
        "country": "CN",
        "checked": CHECKED,
        "sources": [CHINA_2024],
    },
]

EXPECTED_TOTAL = 5
ENGLISH_NAMES = {row["id"]: row["name"] for row in DIRECT_RUSSIA_ROWS}
ENGLISH_SEATS = {row["seat"]: row["seat"] for row in DIRECT_RUSSIA_ROWS}


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in (
            "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
            "\ufffd")):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    return row


def build():
    rows = []
    seen = {"russia"}
    for source in DIRECT_RUSSIA_ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") != "russia" or row.get("country") != "CN":
            raise ValueError("%s hangs outside mainland China's direct branch" %
                             row_id)
        if row.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable name" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != EXPECTED_TOTAL:
        raise ValueError("mainland China must publish exactly five direct rows")
    if set(ENGLISH_NAMES) != seen - {"russia"}:
        raise ValueError("mainland China English name map is out of sync")
    return {
        "russia": {
            "v": 1,
            "parent": "russia",
            "country": "CN",
            "rows": rows,
        }
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory mainland China: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("mainland China: 5 current direct Moscow Patriarchate bodies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
