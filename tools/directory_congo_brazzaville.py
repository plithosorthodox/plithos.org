#!/usr/bin/env python3
"""Current canonical Eastern Orthodox bodies in Congo-Brazzaville.

The current Alexandrian metropolis and Russian African Exarchate both publish
structures in the Republic of the Congo. Body-level Alexandrian records are
paired with the current metropolis page. The Russian rows come from the
current diocesan roster and a March 2026 visit to all six named parishes.

    python tools/directory_congo_brazzaville.py --check
    python tools/directory_congo_brazzaville.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_DIOCESE = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "iera-mitropolis-mprazavil-kai-gkampon/"
)
AX_VISIT_2019 = (
    "https://www.patriarchateofalexandria.com/"
    "peratosi-tis-episimoy-episkepseos-toy-patriarchoy-alexandreias-"
    "stin-i-mitropoli-mprazavil/"
)
AX_CATHEDRAL = (
    "https://www.patriarchateofalexandria.com/"
    "istorika-egkainia-toy-i-kathedrikoy-naoy-ag-dimitrioy-tis-ieras-"
    "mitropoleos-mprazavil/"
)
AX_ASCENSION = (
    "https://www.patriarchateofalexandria.com/"
    "episkepsi-agapis-stis-fylakes-toy-pointe-noire/"
)
AX_PHOTINI = (
    "https://www.patriarchateofalexandria.com/"
    "kyriaki-tis-samareitidos-ston-i-nao-ag-foteinis-pointe-noire/"
)
AX_IRENE = (
    "https://www.patriarchateofalexandria.com/"
    "i-eorti-tis-enoriakis-koinotitos-agias-eirinis-dolisie/"
)
AX_EARLY_ROSTER = (
    "https://www.patriarchateofalexandria.com/"
    "synantisi-tis-athm-me-ton-patriarchiko-epitropo-mprazavil-i-"
    "neosystati-episkopi-mprazavil-kai-gkampon/"
)
AX_NKAYI = (
    "https://www.patriarchateofalexandria.com/"
    "epitheorisi-ton-ergasion-stin-enoria-tis-poleos-nkayi/"
)
AX_IMPFONDO = (
    "https://www.patriarchateofalexandria.com/"
    "proodos-ton-ergasion-kataskeyis-dyo-naon-tis-i-episkopis-mprazavil/"
)
BASILICA_IMPFONDO = (
    "https://arhiva.basilica.ro/mitropolitul-pantelimon-de-congo-"
    "brazzaville-si-gabon-a-efectuat-o-vizita-pastorala-in-tinutul-"
    "pigmeilor/"
)

RU_DIOCESE = (
    "https://exarchate-africa.ru/en/dioceses_cat/south-african-diocese/"
)
RU_VISIT = (
    "https://exarchate-africa.ru/fr/actualite/"
    "lexarque-patriarcal-dafrique-en-republique-du-congo/"
)
RU_DEANERIES = (
    "https://exarchate-africa.ru/en/news/"
    "the-deanery-of-the-republic-of-the-congo-has-been-split-into-two-"
    "deaneries/"
)


def body(row_id, parent, name, local, seat, rank, sources, address=None):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "CG",
        "sources": sources,
    }
    if address:
        row["address"] = address
    return row


AX_ROWS = [
    body(
        "cg-ax-brazzaville-resurrection", "ax-brazzaville",
        "Resurrection of the Lord Parish in Brazzaville",
        "Paroisse de la Résurrection du Seigneur à Brazzaville",
        "Brazzaville", "Parish", [AX_DIOCESE, AX_VISIT_2019],
    ),
    body(
        "cg-ax-pointe-noire-demetrius-cathedral", "ax-brazzaville",
        "Saint Demetrius the Myrrh-Streamer Cathedral in Pointe-Noire",
        "Cathédrale Saint-Dimitri-le-Myroblite à Pointe-Noire",
        "Pointe-Noire", "Cathedral", [AX_DIOCESE, AX_CATHEDRAL],
        ["24, Av. Stephane Tchitchelle, Centre Ville", "B.P. 183",
         "Pointe-Noire, République du Congo"],
    ),
    body(
        "cg-ax-pointe-noire-ascension", "ax-brazzaville",
        "Ascension of the Lord Parish in Pointe-Noire",
        "Paroisse de l'Ascension du Seigneur à Pointe-Noire",
        "Pointe-Noire", "Parish", [AX_DIOCESE, AX_ASCENSION],
    ),
    body(
        "cg-ax-pointe-noire-photini", "ax-brazzaville",
        "Saint Photini the Samaritan Woman Parish in Mpaka",
        "Paroisse Sainte-Photine-la-Samaritaine à Mpaka",
        "Pointe-Noire", "Parish", [AX_DIOCESE, AX_PHOTINI, AX_VISIT_2019],
    ),
    body(
        "cg-ax-dolisie-irene", "ax-brazzaville",
        "Saint Irene Parish in Dolisie",
        "Paroisse Sainte-Irène à Dolisie", "Dolisie", "Parish",
        [AX_DIOCESE, AX_IRENE, AX_VISIT_2019],
    ),
    body(
        "cg-ax-dolisie-nicholas", "ax-brazzaville",
        "Saint Nicholas Church in Dolisie",
        "Église Saint-Nicolas à Dolisie", "Dolisie", "Church",
        [AX_DIOCESE, AX_EARLY_ROSTER],
    ),
    body(
        "cg-ax-nkayi-transfiguration-kosmas", "ax-brazzaville",
        "Transfiguration of the Lord and Saint Kosmas of Aetolia Parish in Nkayi",
        "Paroisse de la Transfiguration-du-Seigneur-et-Saint-Cosmas-"
        "d'Étolie à Nkayi", "Nkayi", "Parish",
        [AX_DIOCESE, AX_NKAYI],
    ),
    body(
        "cg-ax-impfondo-john-baptist-nicholas", "ax-brazzaville",
        "Saint John the Baptist and Saint Nicholas Church in Impfondo",
        "Église Saint-Jean-Baptiste-et-Saint-Nicolas à Impfondo",
        "Impfondo", "Church",
        [AX_DIOCESE, AX_IMPFONDO, BASILICA_IMPFONDO],
    ),
]


RU_ROWS = [
    body(
        "cg-ru-brazzaville-basil", "ru-south-africa",
        "Saint Basil the Great Parish in Brazzaville",
        "Paroisse Saint-Basile-le-Grand de Brazzaville",
        "Brazzaville", "Parish", [RU_DIOCESE, RU_VISIT, RU_DEANERIES],
    ),
    body(
        "cg-ru-brazzaville-john-nativity", "ru-south-africa",
        "Nativity of Saint John the Baptist Parish in Brazzaville",
        "Paroisse de la Nativité de saint Jean-Baptiste de Brazzaville",
        "Brazzaville", "Parish", [RU_DIOCESE, RU_VISIT, RU_DEANERIES],
    ),
    body(
        "cg-ru-dolisie-gregory-theologian", "ru-south-africa",
        "Saint Gregory the Theologian Parish in Dolisie",
        "Paroisse Saint-Grégoire-le-Théologien de Dolisie",
        "Dolisie", "Parish", [RU_DIOCESE, RU_VISIT],
    ),
    body(
        "cg-ru-nkayi-nativity-theotokos", "ru-south-africa",
        "Nativity of the Theotokos Parish in Nkayi",
        "Paroisse de la Nativité-de-la-Mère-de-Dieu de Nkayi",
        "Nkayi", "Parish", [RU_DIOCESE, RU_VISIT],
    ),
    body(
        "cg-ru-nsiene-john-chrysostom", "ru-south-africa",
        "Saint John Chrysostom Parish in Nsiene",
        "Paroisse Saint-Jean-Chrysostome de Nsiene", "Nsiene", "Parish",
        [RU_DIOCESE, RU_VISIT],
    ),
    body(
        "cg-ru-pointe-noire-nicholas", "ru-south-africa",
        "Saint Nicholas Parish in Pointe-Noire",
        "Paroisse Saint-Nicolas de Pointe-Noire", "Pointe-Noire", "Parish",
        [RU_DIOCESE, RU_VISIT, RU_DEANERIES],
        ["former premises of the Russian Embassy", "Pointe-Noire",
         "Republic of the Congo"],
    ),
]


ROWS = {
    "ax-brazzaville": AX_ROWS,
    "ru-south-africa": RU_ROWS,
}
EXPECTED = {"ax-brazzaville": 8, "ru-south-africa": 6}
EXPECTED_TOTAL = 14
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in ROWS.values()
    for row in rows
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


def build():
    payloads = {}
    seen = set(ROWS)
    total = 0
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if row.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if row.get("country") != "CG":
                raise ValueError("%s is outside Congo-Brazzaville" % row_id)
            if row.get("kind") != "parish":
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        total += len(rows)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "CG",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Congo-Brazzaville must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Congo-Brazzaville English name map is out of sync")
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
        print("directory Congo-Brazzaville: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Congo-Brazzaville: 14 current bodies across 2 jurisdictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
