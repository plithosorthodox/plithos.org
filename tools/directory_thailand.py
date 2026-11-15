#!/usr/bin/env python3
"""Current officially named Orthodox bodies in Thailand.

The Moscow Patriarchate's current exarchal map names nine parishes and one
monastic community in Thailand. Aggregate diocesan prose reports ten parishes,
a monastery, and a religious school, but does not identify the additional
parish or the school. Those unresolved bodies remain in the candidate ledger.

    python tools/directory_thailand.py --check
    python tools/directory_thailand.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-15"

MP_MAP = "https://exarchate.asia/en/karta-prihodov/"
MP_THAILAND = (
    "https://exarchate.asia/en/category/map-of-parishes/"
    "thailand-diocese-en/"
)
MP_DIOCESE = "https://exarchate.asia/en/patriarshij-ekzarhat/eparhii/"

ENGLISH_NAMES = {
    "th-ru-bangkok-saint-nicholas": "St. Nicholas Cathedral in Bangkok",
    "th-ru-phuket-holy-trinity": (
        "Parish of the Holy Life-Giving Trinity on Phuket"
    ),
    "th-ru-pattaya-all-saints": "Parish of All Saints in Pattaya",
    "th-ru-pattaya-protection": (
        "Parish of the Protection of the Mother of God in Pattaya"
    ),
    "th-ru-koh-samui-ascension": (
        "Parish of the Holy Ascension on Koh Samui"
    ),
    "th-ru-hua-hin-royal-passion-bearers": (
        "Parish of the Holy Royal Passion-Bearers in Hua Hin"
    ),
    "th-ru-chiang-mai-saint-vladimir": (
        "Parish of St. Vladimir in Chiang Mai"
    ),
    "th-ru-koh-chang-saint-sergius": (
        "Parish of St. Sergius of Radonezh on Koh Chang"
    ),
    "th-ru-koh-phangan-saint-seraphim": (
        "Parish of St. Seraphim of Sarov on Koh Phangan"
    ),
    "th-ru-ratchaburi-dormition": (
        "Monastic Community of the Dormition of the Mother of God in Ratchaburi"
    ),
}


ROWS = [
    dict(
        id="th-ru-bangkok-saint-nicholas",
        parent="ru-thailand",
        kind="parish",
        rank="Cathedral Parish",
        name=ENGLISH_NAMES["th-ru-bangkok-saint-nicholas"],
        local="Свято-Николаевский собор в Бангкоке",
        country="TH",
        dedication="Saint Nicholas the Wonderworker",
        address=[
            "26-28 Soi Wachiratham Sathit 36",
            "Sukhumvit Soi 101/1, Bangchak, Phrakanong",
            "Bangkok 10260, Thailand",
        ],
        site="http://bkk.orthodox.or.th/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-phuket-holy-trinity",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-phuket-holy-trinity"],
        local="Храм Святой Живоначальной Троицы на острове Пхукет",
        country="TH",
        dedication="The Holy Life-Giving Trinity",
        address=[
            "121 and 121/1 Moo 7, Soi Nanai",
            "Tambon Thepkasattri, Thalang District",
            "Phuket 83110, Thailand",
        ],
        site="http://phuket.ortox.ru/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-pattaya-all-saints",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-pattaya-all-saints"],
        local="Храм Всех Святых в Паттайе",
        country="TH",
        dedication="All Saints",
        address=[
            "275/82 Moo 5, Soi 16, Naklua Road",
            "Tambon Naklua, Banglamung District",
            "Chonburi 20150, Thailand",
        ],
        site="http://pattaya.orthodox.or.th/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-pattaya-protection",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-pattaya-protection"],
        local="Храм Покрова Пресвятой Богородицы в Паттайе",
        country="TH",
        dedication="The Protection of the Most Holy Theotokos",
        address=[
            "105/126 Moo 11, Huai Yai Road",
            "Banglamung District, Chonburi 20150, Thailand",
        ],
        site="http://khram-pokrova.blogspot.com/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-koh-samui-ascension",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-koh-samui-ascension"],
        local="Храм Вознесения Господня на острове Самуи",
        country="TH",
        dedication="The Holy Ascension of the Lord",
        address=[
            "127/245 Moo 3, Maret",
            "Koh Samui, Surat Thani 84000, Thailand",
        ],
        site="https://siamorthodox.ru/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-hua-hin-royal-passion-bearers",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-hua-hin-royal-passion-bearers"],
        local="Храм Святых Царственных Страстотерпцев в Хуа Хине",
        country="TH",
        dedication="The Holy Royal Passion-Bearers",
        address=[
            "64/172 Alley Nong Kae, Soi 102",
            "Hua Hin, Prachuap Khiri Khan 77110, Thailand",
        ],
        site="http://huahin.cerkov.ru/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-chiang-mai-saint-vladimir",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-chiang-mai-saint-vladimir"],
        local="Храм Святого Равноапостольного Князя Владимира в Чиангмае",
        country="TH",
        dedication="Saint Vladimir, Equal-to-the-Apostles",
        address=[
            "4 Srichadon Road, Chang Khlan",
            "Chiang Mai, Thailand",
        ],
        site="http://hramchiangmai.pravorg.ru/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-koh-chang-saint-sergius",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-koh-chang-saint-sergius"],
        local="Храм Преподобного Сергия Радонежского на острове Чанг",
        country="TH",
        dedication="Saint Sergius of Radonezh",
        address=[
            "42/8 Moo 3, Klong Son",
            "Koh Chang, Trat 23170, Thailand",
        ],
        site="http://hramkochang.pravorg.ru/",
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-koh-phangan-saint-seraphim",
        parent="ru-thailand",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["th-ru-koh-phangan-saint-seraphim"],
        local="Храм Преподобного Серафима Саровского на острове Пханган",
        country="TH",
        dedication="Saint Seraphim of Sarov",
        address=[
            "45/35 Moo 2",
            "Koh Phangan, Surat Thani 84280, Thailand",
        ],
        sources=[MP_MAP, MP_THAILAND],
    ),
    dict(
        id="th-ru-ratchaburi-dormition",
        parent="ru-thailand",
        kind="monastery",
        rank="Monastic Community",
        name=ENGLISH_NAMES["th-ru-ratchaburi-dormition"],
        local=(
            "Монашеская община в честь Успения Божией Матери "
            "в провинции Ратчабури"
        ),
        country="TH",
        dedication="The Dormition of the Mother of God",
        address=[
            "111 Moo 3, Tambon Ang Thong",
            "Mueang Ratchaburi, Ratchaburi, Thailand",
        ],
        sources=[MP_MAP, MP_THAILAND, MP_DIOCESE],
    ),
]


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    if row.get("site") and not row["site"].startswith("http"):
        raise ValueError("%s carries a non-URL site" % row.get("id"))
    for key in ("address", "languages", "founded"):
        if row.get(key) and (not isinstance(row[key], list) or
                             not all(isinstance(value, str)
                                     for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    for value in row.values():
        texts = value if isinstance(value, list) else [value]
        for text in texts:
            if isinstance(text, str) and ("\u2013" in text or "\u2014" in text):
                raise ValueError("%s carries a forbidden long dash" %
                                 row.get("id"))
    return row


def build():
    rows = []
    seen = {"ru-thailand"}
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if row.get("parent") != "ru-thailand":
            raise ValueError("%s is grouped under the wrong parent" % row_id)
        if row.get("country") != "TH":
            raise ValueError("%s is outside Thailand" % row_id)
        if row.get("kind") not in {"parish", "monastery"}:
            raise ValueError("%s has an unsupported body type" % row_id)
        if not row.get("local"):
            raise ValueError("%s lacks its official local identity" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != 10:
        raise ValueError("Thailand must publish exactly ten named bodies")
    if sum(row["kind"] == "parish" for row in rows) != 9:
        raise ValueError("Thailand must publish exactly nine named parishes")
    if set(ENGLISH_NAMES) != seen - {"ru-thailand"}:
        raise ValueError("English name coverage differs from Thailand rows")
    return {
        "ru-thailand": {
            "v": 1,
            "parent": "ru-thailand",
            "rows": rows,
            "country": "TH",
        }
    }


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
        }
        for parent, payload in sorted(payloads.items())
    }


def encoded(payload):
    return json.dumps(payload, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")


def output_path(parent):
    return OUT / ("%s.v1.json" % parent)


def write(payloads):
    OUT.mkdir(parents=True, exist_ok=True)
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        elif args.check:
            errors = problems(payloads)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("Thailand directory data is current (10 rows)")
        else:
            print(json.dumps(manifest(payloads), ensure_ascii=False,
                             indent=2))
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
