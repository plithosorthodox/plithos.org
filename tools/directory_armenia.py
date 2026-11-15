#!/usr/bin/env python3
"""Current officially documented Eastern Orthodox bodies in Armenia.

The Yerevan and Armenia Diocese publishes eight active churches in its current
roster. Later first-party service records establish current worship at the
Archangel Michael church in Privolnoye and St. George chapel in Gyumri. Two
other historic buildings remain held because the diocese describes them as
needing or undergoing restoration.

    python tools/directory_armenia.py --check
    python tools/directory_armenia.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-15"

MP_DIOCESE = "https://armeparchy.org/eparhiya/"
MP_SHRINES = "https://armeparchy.org/svjatyni-armenii/"
MP_PATRIARCHATE = "https://patriarchia.ru/en/org/564"
MP_SCHEDULE = "https://armeparchy.org/category/raspisanie/"
MP_PRIVOLNOYE = (
    "https://armeparchy.org/2026/01/19/"
    "prazdnovanie-svjatogo-bogojavlenija-i-kreshhenija-gospoda-boga-i-"
    "spasa-nashego-iisusa-hrista-v-hramah-erevansko-armjanskoj-eparhii-"
    "fotoreportazh/"
)
MP_SAINT_GEORGE = (
    "https://armeparchy.org/2025/12/01/"
    "osvjashhena-chasovnja-svjatogo-georgija-pobedonosca-v-pogranichnom-"
    "upravlenii-fsb-rossii-v-respublike-armenija/"
)
MP_GYUMRI_SCHEDULE = (
    "https://armeparchy.org/2026/11/09/hramy-g-gjumri/"
)

ENGLISH_NAMES = {
    "am-ru-yerevan-protection-cathedral": (
        "Cathedral of the Protection of the Most Holy Theotokos in Yerevan"
    ),
    "am-ru-yerevan-exaltation-cross": (
        "Church of the Exaltation of the Holy Cross in Yerevan"
    ),
    "am-ru-vanadzor-nativity-theotokos": (
        "Church of the Nativity of the Most Holy Theotokos in Vanadzor"
    ),
    "am-ru-gyumri-archangel-michael": (
        "Chapel Church of the Archangel Michael in Gyumri"
    ),
    "am-ru-gyumri-martyr-alexandra": (
        "Church of the Holy Martyr Empress Alexandra of Rome in Gyumri"
    ),
    "am-ru-gyumri-matrona-house": (
        "House Church of Blessed Matrona of Moscow in Gyumri"
    ),
    "am-ru-yerevan-dormition-house": (
        "House Church of the Dormition of the Most Holy Theotokos in Yerevan"
    ),
    "am-ru-dimitrov-cyricus-julitta": (
        "Church of the Holy Martyrs Cyricus and Julitta in Dimitrov"
    ),
    "am-ru-privolnoye-archangel-michael": (
        "Church of the Archangel Michael in Privolnoye"
    ),
    "am-ru-border-directorate-saint-george-chapel": (
        "Chapel of St. George the Victory-Bearer at the FSB Border Directorate"
    ),
}


ROWS = [
    dict(
        id="am-ru-yerevan-protection-cathedral",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Cathedral Parish",
        name=ENGLISH_NAMES["am-ru-yerevan-protection-cathedral"],
        local="Храм Покрова Пресвятой Богородицы города Еревана",
        country="AM",
        dedication="The Protection of the Most Holy Theotokos",
        address=[
            "68 Zakaria Kanakertsi Street",
            "Yerevan 0091, Armenia",
        ],
        site="https://armeparchy.org/",
        sources=[MP_DIOCESE, MP_SHRINES, MP_PATRIARCHATE],
    ),
    dict(
        id="am-ru-yerevan-exaltation-cross",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["am-ru-yerevan-exaltation-cross"],
        local="Храм Воздвижения Креста Господня города Еревана",
        country="AM",
        dedication="The Exaltation of the Holy Cross",
        address=[
            "15/5 Admiral Isakov Avenue",
            "Yerevan 0082, Armenia",
        ],
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-vanadzor-nativity-theotokos",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["am-ru-vanadzor-nativity-theotokos"],
        local="Храм Рождества Пресвятой Богородицы города Ванадзора",
        country="AM",
        dedication="The Nativity of the Most Holy Theotokos",
        address=[
            "1 Vazgen Sargsyan Square",
            "Vanadzor 2001, Armenia",
        ],
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-gyumri-archangel-michael",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Chapel Parish",
        name=ENGLISH_NAMES["am-ru-gyumri-archangel-michael"],
        local="Храм-часовня святого Архангела Михаила города Гюмри",
        country="AM",
        dedication="The Archangel Michael",
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-gyumri-martyr-alexandra",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Military Parish",
        name=ENGLISH_NAMES["am-ru-gyumri-martyr-alexandra"],
        local="Храм святой мученицы царицы Александры Римской города Гюмри",
        country="AM",
        dedication="The Holy Martyr Empress Alexandra of Rome",
        address=[
            "102nd Russian Military Base",
            "Gyumri, Armenia",
        ],
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-gyumri-matrona-house",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Military Parish",
        name=ENGLISH_NAMES["am-ru-gyumri-matrona-house"],
        local="Домовый храм блаженной Матроны Московской города Гюмри",
        country="AM",
        dedication="Blessed Matrona of Moscow",
        address=[
            "102nd Russian Military Base",
            "Gyumri, Armenia",
        ],
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-yerevan-dormition-house",
        parent="ru-yerevan-and-armenia",
        kind="monastery",
        rank="House Church",
        name=ENGLISH_NAMES["am-ru-yerevan-dormition-house"],
        local="Домовый храм Успения Пресвятой Богородицы города Еревана",
        country="AM",
        dedication="The Dormition of the Most Holy Theotokos",
        address=[
            "117/4 Zakaria Kanakertsi Street",
            "Yerevan 0091, Armenia",
        ],
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-dimitrov-cyricus-julitta",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["am-ru-dimitrov-cyricus-julitta"],
        local="Храм святых мучеников Кирика и Иулитты села Димитров",
        country="AM",
        dedication="The Holy Martyrs Cyricus and Julitta",
        sources=[MP_DIOCESE, MP_SHRINES],
    ),
    dict(
        id="am-ru-privolnoye-archangel-michael",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Parish",
        name=ENGLISH_NAMES["am-ru-privolnoye-archangel-michael"],
        local="Храм Архистратига Михаила в селе Привольное",
        country="AM",
        dedication="The Archangel Michael",
        sources=[MP_PRIVOLNOYE, MP_DIOCESE],
    ),
    dict(
        id="am-ru-border-directorate-saint-george-chapel",
        parent="ru-yerevan-and-armenia",
        kind="parish",
        rank="Chapel Parish",
        name=ENGLISH_NAMES["am-ru-border-directorate-saint-george-chapel"],
        local=(
            "Часовня великомученика Георгия Победоносца на территории "
            "Пограничного управления ФСБ России в Республике Армения"
        ),
        country="AM",
        dedication="Saint George the Victory-Bearer",
        sources=[MP_SAINT_GEORGE, MP_GYUMRI_SCHEDULE, MP_SCHEDULE],
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
    seen = {"ru-yerevan-and-armenia"}
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if row.get("parent") != "ru-yerevan-and-armenia":
            raise ValueError("%s is grouped under the wrong parent" % row_id)
        if row.get("country") != "AM":
            raise ValueError("%s is outside Armenia" % row_id)
        if row.get("kind") not in {"parish", "monastery"}:
            raise ValueError("%s has an unsupported body type" % row_id)
        if not row.get("local"):
            raise ValueError("%s lacks its official local identity" % row_id)
        seen.add(row_id)
        rows.append(row)
    if len(rows) != 10:
        raise ValueError("Armenia must publish exactly ten current bodies")
    if set(ENGLISH_NAMES) != seen - {"ru-yerevan-and-armenia"}:
        raise ValueError("English name coverage differs from Armenia rows")
    return {
        "ru-yerevan-and-armenia": {
            "v": 1,
            "parent": "ru-yerevan-and-armenia",
            "rows": rows,
            "country": "AM",
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
            print("Armenia directory data is current (10 rows)")
        else:
            print(json.dumps(manifest(payloads), ensure_ascii=False,
                             indent=2))
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
