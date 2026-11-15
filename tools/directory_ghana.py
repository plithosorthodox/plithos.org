#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Ghana.

The current Patriarchate of Alexandria register establishes the Holy
Archdiocese of Accra. Current official archdiocesan reporting names the
eighteen Ghanaian worship bodies published here. Conflicting aggregate
counts and unnamed communities stay in the companion candidate ledger.

    python tools/directory_ghana.py --check
    python tools/directory_ghana.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

AX_ACCRA = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-accra/?lang=en"
)
IONIAN_STAFF = "https://envi.ionio.gr/saint-cyril/en/staff/"
APPOINTMENTS = (
    "https://orthodoxtimes.com/ordinations-and-appointments-in-the-"
    "metropolis-of-accra/"
)
LARTEH_TEMA = (
    "https://orthodoxtimes.com/metropolitan-of-accra-held-first-"
    "missionary-visit-to-the-orthodox-communities/"
)
ASHANTI = (
    "https://orthodoxtimes.com/the-orthodox-church-of-ghana-grows-stronger/"
)
GYAHA = (
    "https://orthodoxtimes.com/the-first-pastoral-visit-to-the-orthodox-"
    "christian-community-of-gyaha/"
)
FOMENA_2025 = (
    "https://greek.vema.com.au/2025/11/14/"
    "mnimi-agiou-ioannou-tou-chrysostomou-stin-kentriki-gkana/"
)
FOMENA_2026 = (
    "https://greek.vema.com.au/2026/11/14/"
    "i-eorti-tou-agiou-ioannou-tou-chrysostomou-sti-gkana/"
)
REVIVAL = (
    "https://orthodoxtimes.com/ghanas-orthodox-community-rejoices-in-"
    "69th-annual-spiritual-revival/"
)
AKIM_BREMAN = "https://orthodoxhouse.com/article/news-d75d9938"
MEDICAL_OUTREACH = (
    "https://ampelonas-trygetes.blogspot.com/2025/07/"
    "free-medical-outreach-in-orthodox.html?m=0"
)
CENTRAL_GHANA = (
    "https://ampelonas-trygetes.blogspot.com/2024/05/?m=0"
)
GOMOA_OGUAA = (
    "https://ampelonas-trygetes.blogspot.com/2024/06/blog-post_25.html"
)


def row(row_id, name, local, locality, sources, kind="parish", rank="Parish"):
    return {
        "id": row_id,
        "parent": "ax-accra",
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": locality,
        "country": "GH",
        "sources": sources,
    }


ROWS = [
    row(
        "gh-ax-accra-transfiguration-cathedral",
        "Holy Transfiguration of Christ Cathedral in Accra",
        "Καθεδρικός Ιερός Ναός Μεταμορφώσεως του Χριστού στην Άκκρα",
        "Accra",
        [AX_ACCRA, IONIAN_STAFF, APPOINTMENTS],
        rank="Cathedral",
    ),
    row(
        "gh-ax-larteh-peter-paul-nektarios",
        "Church of Saints Peter and Paul and Saint Nektarios in Larteh",
        "Ιερός Ναός Αγίων Αποστόλων Πέτρου και Παύλου και Αγίου Νεκταρίου στο Λάρτε",
        "Larteh",
        [LARTEH_TEMA, IONIAN_STAFF],
    ),
    row(
        "gh-ax-domeabra-thomas",
        "Parish of Saint Thomas the Apostle in Domeabra",
        "Ενορία Αγίου Αποστόλου Θωμά στη Ντομεάμπρα",
        "Domeabra",
        [APPOINTMENTS, IONIAN_STAFF],
    ),
    row(
        "gh-ax-adeiso-charalambos-george",
        "Church of Saints Charalambos and George in Adeiso",
        "Ιερός Ναός Αγίων Χαραλάμπους και Γεωργίου στο Αντέισο",
        "Adeiso",
        [APPOINTMENTS],
    ),
    row(
        "gh-ax-gomoa-afransi-james",
        "Parish of Saint James the Brother of the Lord in Gomoa Afransi",
        "Ενορία Αγίου Ιακώβου του Αδελφοθέου στο Γκομόα Αφράνσι",
        "Gomoa Afransi",
        [APPOINTMENTS],
    ),
    row(
        "gh-ax-kasoa-dormition",
        "Parish of the Dormition of the Theotokos in Kasoa",
        "Ενορία Κοιμήσεως της Θεοτόκου στην Κασόα",
        "Kasoa",
        [APPOINTMENTS],
    ),
    row(
        "gh-ax-agona-swedru-mark",
        "Parish of Saint Mark the Evangelist in Agona Swedru",
        "Ενορία Αγίου Μάρκου του Ευαγγελιστού στην Αγκόνα Σουέντρου",
        "Agona Swedru",
        [APPOINTMENTS],
    ),
    row(
        "gh-ax-gyaha-nativity-christ",
        "Church of the Nativity of Christ in Gyaha",
        "Ιερός Ναός Γεννήσεως του Χριστού στη Γκιάχα",
        "Gyaha",
        [GYAHA],
    ),
    row(
        "gh-ax-akrokyere-athanasius-ambrose",
        "Parish Church of Saints Athanasius the Great and Ambrose of Milan in Akrokyere",
        "Ενοριακός Ιερός Ναός Αγίων Αθανασίου του Μεγάλου και Αμβροσίου Μεδιολάνων στο Ακροκιέρε",
        "Akrokyere",
        [ASHANTI],
    ),
    row(
        "gh-ax-kumawu-catherine",
        "Parish of Saint Catherine the Great Martyr in Kumawu",
        "Ενορία Αγίας Μεγαλομάρτυρος Αικατερίνης στο Κουμάου",
        "Kumawu",
        [ASHANTI],
    ),
    row(
        "gh-ax-gomoa-fomena-annunciation-chrysostom",
        "Parish Church of the Annunciation of the Theotokos and Saint John Chrysostom in Gomoa Fomena",
        "Ενοριακός Ιερός Ναός Ευαγγελισμού της Θεοτόκου και Αγίου Ιωάννου του Χρυσοστόμου στο Γκομόα Φομένα",
        "Gomoa Fomena",
        [FOMENA_2025, FOMENA_2026],
    ),
    row(
        "gh-ax-gomoa-fomena-raphael-pilgrimage",
        "Pilgrimage Church of Saint Raphael in Gomoa Fomena",
        "Προσκυνηματικός Ιερός Ναός Αγίου Ραφαήλ στο Γκομόα Φομένα",
        "Gomoa Fomena",
        [REVIVAL],
        rank="Pilgrimage Church",
    ),
    row(
        "gh-ax-tema-newtown-nicholas",
        "Church of Saint Nicholas in Tema Newtown",
        "Ιερός Ναός Αγίου Νικολάου στο Τέμα Νιούταουν",
        "Tema Newtown",
        [LARTEH_TEMA],
    ),
    row(
        "gh-ax-akim-breman-epiphany",
        "Parish Church of the Holy Epiphany in Akim Breman",
        "Ενοριακός Ιερός Ναός Αγίων Θεοφανείων στο Ακίμ Μπρέμαν",
        "Akim Breman",
        [AKIM_BREMAN, MEDICAL_OUTREACH],
    ),
    row(
        "gh-ax-agona-abodom-john-theologian",
        "Church of Saint John the Theologian in Agona Abodom",
        "Ιερός Ναός Αγίου Ιωάννου του Θεολόγου στην Αγκόνα Αμπόντομ",
        "Agona Abodom",
        [CENTRAL_GHANA, FOMENA_2026],
    ),
    row(
        "gh-ax-gomoa-oguaa-nativity-theotokos",
        "Church of the Nativity of the Theotokos in Gomoa Oguaa",
        "Ιερός Ναός Γεννήσεως της Θεοτόκου στο Γκομόα Ογκουάα",
        "Gomoa Oguaa",
        [GOMOA_OGUAA],
    ),
    row(
        "gh-ax-essaman-matthew",
        "Parish of the Holy Apostle Matthew in Essaman",
        "Ενορία Αγίου Αποστόλου Ματθαίου στο Εσαμάν",
        "Essaman",
        [FOMENA_2026],
    ),
    row(
        "gh-ax-odina-ogua-theotokos",
        "Parish of the Most Holy Theotokos in Odina Ogua",
        "Ενορία Υπεραγίας Θεοτόκου στην Οντίνα Ογκούα",
        "Odina Ogua",
        [FOMENA_2026],
    ),
]

EXPECTED = 18
ENGLISH_NAMES = {item["id"]: item["name"] for item in ROWS}
ENGLISH_SEATS = {item["seat"]: item["seat"] for item in ROWS}


def clean(source):
    item = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    item.setdefault("checked", CHECKED)
    sources = list(item.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % item.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % item.get("id"))
    item["sources"] = sources
    item["cite"] = list(sources)
    rendered = json.dumps(item, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         item.get("id"))
    return item


def build():
    rows = []
    seen = {"ax-accra"}
    for source in ROWS:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if item.get("parent") != "ax-accra":
            raise ValueError("%s hangs off the wrong parent" % row_id)
        if item.get("country") != "GH":
            raise ValueError("%s is outside Ghana" % row_id)
        if item.get("kind") != "parish":
            raise ValueError("%s has an unsupported kind" % row_id)
        if not item.get("name") or not item.get("local") or not item.get("seat"):
            raise ValueError("%s lacks a usable name or locality" % row_id)
        seen.add(row_id)
        rows.append(item)
    if len(rows) != EXPECTED:
        raise ValueError("Ghana must publish exactly %d rows" % EXPECTED)
    if set(ENGLISH_NAMES) != seen - {"ax-accra"}:
        raise ValueError("Ghana English name map is out of sync")
    return {
        "ax-accra": {
            "v": 1,
            "parent": "ax-accra",
            "country": "GH",
            "rows": rows,
        },
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
        print("directory Ghana: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Ghana: 18 current officially named bodies under the existing "
          "Alexandrian archdiocesan parent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
