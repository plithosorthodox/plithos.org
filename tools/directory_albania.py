#!/usr/bin/env python3
"""Validated current Orthodox bodies in Albania.

The Church of Albania's 2026 organization page names fifteen current
cathedrals and churches and seven current monastic houses. Current official
Fier material names another six churches. It does not expose a complete parish
roster. Older construction and restoration galleries are therefore kept in
the candidate ledger instead of being presented as proof of current worship.

    python tools/directory_albania.py --check
    python tools/directory_albania.py --dump
"""

import argparse
import json
import sys


CHECKED = "2026-11-15"

ORGANIZATION = (
    "https://orthodoxalbania.org/2026/"
    "organizimi-kishtar-kisha-orthodhokse-autoqefale-e-shqiperise-2026/"
)
ORGANIZATION_EN = (
    "https://orthodoxalbania.org/2026/en/church-organization-2026/"
)
CONTACTS = (
    "https://orthodoxalbania.org/2026/2020/04/14/"
    "informacione-kontakti/"
)
FIER_CURRENT = (
    "https://orthodoxalbania.org/2026/2026/04/02/"
    "radio-ngjallja-vepra-katekitike-e-mitropolise-se-apollonise-dhe-"
    "fierit-ne-muajin-mars-2026/"
)


def row(row_id, parent, name, local, rank, kind="parish", address=None,
        sources=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "AL",
        "sources": list(sources or [ORGANIZATION, ORGANIZATION_EN]),
    }
    if address:
        value["address"] = list(address)
    return value


ROWS = {
    "al-tirana-durres": [
        row(
            "al-tirana-resurrection-cathedral", "al-tirana-durres",
            "Resurrection of Christ Cathedral in Tirana",
            "Katedralja Ngjallja e Krishtit, Tiranë", "Cathedral",
            address=["Rruga Ibrahim Rugova", "Tiranë, Albania"],
        ),
        row(
            "al-tirana-annunciation", "al-tirana-durres",
            "Annunciation of the Theotokos Church in Tirana",
            "Kisha Ungjillëzimi i Hyjlindëses, Tiranë", "Church",
            address=["Tirana, Albania"],
        ),
        row(
            "al-durres-paul-astius", "al-tirana-durres",
            "Apostle Paul and Saint Astius Church in Durrës",
            "Kisha Apostull Pavli e Shën Asti, Durrës", "Church",
            address=["Durrës, Albania"],
        ),
        row(
            "al-kavaje-nicholas", "al-tirana-durres",
            "Saint Nicholas Church in Kavajë",
            "Kisha Shën Nikolla, Kavajë", "Church",
            address=["Kavajë, Albania"],
        ),
        row(
            "al-shkoder-nativity-christ", "al-tirana-durres",
            "Nativity of Christ Church in Shkodër",
            "Kisha Lindja e Krishtit, Shkodër", "Church",
            address=["Shkodër, Albania"],
        ),
    ],
    "al-apollonia-fier": [
        row(
            "al-fier-george-cathedral", "al-apollonia-fier",
            "Saint George Cathedral in Fier",
            "Katedralja e Shën Gjergjit, Fier", "Cathedral",
            address=["Lagjja 1 Maji", "Rruga Jani Bakalli", "Fier, Albania"],
            sources=[ORGANIZATION, CONTACTS, FIER_CURRENT],
        ),
        row(
            "al-ndernenas-annunciation", "al-apollonia-fier",
            "Annunciation of the Theotokos Church in Ndërnënas",
            "Kisha e Ungjillëzimit të Hyjlindëses Mari, Ndërnënas",
            "Church", address=["Ndërnënas, Albania"],
            sources=[FIER_CURRENT],
        ),
        row(
            "al-libofshe-george", "al-apollonia-fier",
            "Saint George Church in Libofshë",
            "Kisha Shën Gjergji, Libofshë", "Church",
            address=["Libofshë, Albania"], sources=[FIER_CURRENT],
        ),
        row(
            "al-agim-transfiguration", "al-apollonia-fier",
            "Transfiguration of the Lord Church in Agim",
            "Kisha Metamorfoza e Zotit Krisht, Agim", "Church",
            address=["Agim, Albania"], sources=[FIER_CURRENT],
        ),
        row(
            "al-pojan-dormition", "al-apollonia-fier",
            "Dormition of the Theotokos Church in Pojan",
            "Kisha Fjetja e Hyjlindëses Mari, Pojan", "Church",
            address=["Pojan, Albania"], sources=[FIER_CURRENT],
        ),
        row(
            "al-sheqishte-mary", "al-apollonia-fier",
            "Saint Mary Church in Sheqishte",
            "Kisha Shën Maria, Sheqishtë", "Church",
            address=["Sheqishtë, Albania"], sources=[FIER_CURRENT],
        ),
    ],
    "al-elbasan": [
        row(
            "al-elbasan-nicholas", "al-elbasan",
            "Saint Nicholas Church in Elbasan",
            "Kisha Shën Nikolla, Elbasan", "Church",
            address=["Elbasan, Albania"],
        ),
        row(
            "al-elbasan-athanasius", "al-elbasan",
            "Saint Athanasius Church in Elbasan",
            "Kisha Shën Athanasi, Elbasan", "Church",
            address=["Elbasan, Albania"],
        ),
    ],
    "al-berat": [
        row(
            "al-berat-demetrius-cathedral", "al-berat",
            "Saint Demetrius Cathedral in Berat",
            "Katedralja Shën Dhimitri, Berat", "Cathedral",
            address=["Berat, Albania"],
        ),
        row(
            "al-vlore-holy-theodores", "al-berat",
            "Holy Theodores Church in Vlorë",
            "Kisha Shën Theodhorët, Vlorë", "Church",
            address=["Vlorë, Albania"],
        ),
        row(
            "al-lushnje-george", "al-berat",
            "Saint George Church in Lushnje",
            "Kisha Shën Gjergji, Lushnjë", "Church",
            address=["Lushnjë, Albania"],
        ),
    ],
    "al-gjirokaster": [
        row(
            "al-gjirokaster-resurrection-cathedral", "al-gjirokaster",
            "Resurrection of Christ Cathedral in Gjirokastër",
            "Katedralja Ngjallja e Krishtit, Gjirokastër", "Cathedral",
            address=["Gjirokastër, Albania"],
        ),
        row(
            "al-sarande-charalambos", "al-gjirokaster",
            "Saint Charalambos Church in Sarandë",
            "Kisha Shën Harallambi, Sarandë", "Church",
            address=["Sarandë, Albania"],
        ),
        row(
            "al-himare-all-saints", "al-gjirokaster",
            "All Saints Church in Himarë",
            "Kisha Gjithë Shenjtorët, Himarë", "Church",
            address=["Himarë, Albania"],
        ),
    ],
    "al-korce": [
        row(
            "al-korce-resurrection-cathedral", "al-korce",
            "Resurrection of Christ Cathedral in Korçë",
            "Katedralja Ngjallja e Krishtit, Korçë", "Cathedral",
            address=["Korçë, Albania"],
        ),
        row(
            "al-pogradec-resurrection", "al-korce",
            "Resurrection of Christ Church in Pogradec",
            "Kisha Ngjallja e Krishtit, Pogradec", "Church",
            address=["Pogradec, Albania"],
        ),
    ],
    "albania": [
        row(
            "al-shen-vlash-monastery", "albania",
            "Holy New Monastery of Saint Vlash in Durrës",
            "Manastiri i Shenjtë i Ri i Shën Vlashit", "Monastery",
            kind="monastery", address=["Shën Vlash", "Durrës, Albania"],
        ),
        row(
            "al-shen-vlash-myrrhbearers-skete", "albania",
            "Skete of the Myrrh-bearing Women in Shën Vlash",
            "Skiti i Miroprurëseve", "Skete", kind="monastery",
            address=["Shën Vlash", "Durrës, Albania"],
        ),
        row(
            "al-ardenice-nativity-monastery", "albania",
            "Nativity of the Theotokos Monastery in Ardenicë",
            "Manastiri Lindja e Hyjlindëses", "Monastery",
            kind="monastery", address=["Ardenicë, Albania"],
        ),
        row(
            "al-kolkondas-cosmas-monastery", "albania",
            "Saint Cosmas Monastery in Kolkondas",
            "Manastiri Shën Kozmai", "Monastery", kind="monastery",
            address=["Kolkondas, Albania"],
        ),
        row(
            "al-dhermi-life-giving-spring-monastery", "albania",
            "Life-giving Spring Monastery in Dhërmi",
            "Manastiri Burimi Jetëdhënës", "Monastery", kind="monastery",
            address=["Dhërmi, Albania"],
        ),
        row(
            "al-qeparo-demetrius-monastery", "albania",
            "Saint Demetrius Monastery in Qeparo",
            "Manastiri Shën Dhimitri", "Monastery", kind="monastery",
            address=["Qeparo, Albania"],
        ),
        row(
            "al-gjirokaster-anne-skete", "albania",
            "Saint Anna Skete in Gjirokastër",
            "Skiti i Shën Anës", "Skete", kind="monastery",
            address=["Gjirokastër, Albania"],
        ),
    ],
}


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}


EXPECTED = {
    "al-apollonia-fier": 6,
    "al-berat": 3,
    "al-elbasan": 2,
    "al-gjirokaster": 3,
    "al-korce": 2,
    "al-tirana-durres": 5,
    "albania": 7,
}


def clean(source):
    out = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("address") and (
            not isinstance(out["address"], list) or
            not all(isinstance(item, str) for item in out["address"])):
        raise ValueError("%s has an invalid address" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if item.get("country") != "AL":
                raise ValueError("%s is outside Albania" % row_id)
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has an unsupported kind" % row_id)
            if not item.get("local"):
                raise ValueError("%s has no local name" % row_id)
            seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "AL",
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Albania counts changed: %r" % counts)
    return payloads


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Albania: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Albania: 28 verified bodies across 7 canonical parents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
