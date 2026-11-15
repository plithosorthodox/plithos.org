#!/usr/bin/env python3
"""New Zealand parish-scale contributions to shared directory branches.

Every row is grouped under an existing parent in ``data/directory.v1.json``.
Five of the six parents are multi-country branches, so this module deliberately
does not write branch payloads. The integration step must merge these rows with
the rows already published for the same parent.

    python tools/directory_new_zealand.py --check
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIRECTORY_INDEX = ROOT / "data" / "directory.v1.json"
CHECKED = "2026-11-14"

EP_NEW_ZEALAND = (
    "https://ec-patr.org/entities/iera-mitropoli-neas-zilandias/"
)

ANTIOCH_NZ = (
    "https://www.antiochian.org.au/portfolio_category/new-zealand/"
)
ANTIOCH_AUCKLAND = (
    "https://www.antiochian.org.au/avada_portfolio/"
    "st-george-mission-auckland/"
)
ANTIOCH_WELLINGTON = (
    "https://www.antiochian.org.au/avada_portfolio/"
    "st-george-mission-wellington/"
)
ANTIOCH_DUNEDIN = (
    "https://www.antiochian.org.au/avada_portfolio/"
    "st-michael-the-archangel-south-dunedin/"
)

SERBIAN_NZ = "https://soc.org.au/state/nz/"
SERBIAN_AUCKLAND = (
    "https://soc.org.au/parish/"
    "st-milutin-the-king-serbian-orthodox-church/"
)
SERBIAN_WELLINGTON = (
    "https://soc.org.au/parish/st-sava-serbian-orthodox-church-7/"
)
SERBIAN_CHRISTCHURCH = (
    "https://soc.org.au/parish/st-nicholas-serbian-orthodox-parish-2/"
)

ROMANIAN_NZ = "https://roeanz.com.au/eparhia/noua-zeelanda"
ROMANIAN_API = "https://roeanz.com.au/api/parish"

ROCOR_AUCKLAND = (
    "https://directory.synod.com/listing/228/"
    "church-of-the-resurrection-of-christ/"
)
ROCOR_WELLINGTON = (
    "https://directory.synod.com/listing/608/christ-the-savior-church/"
)
ROCOR_CHRISTCHURCH = (
    "https://directory.synod.com/listing/229/st-nicholas-church/"
)

MACEDONIAN_AUCKLAND = (
    "https://www.mocdanz.org.au/"
    "%D1%86%D1%80%D0%BA%D0%B2%D0%B8/"
    "moc-sinaxys-of-the-macedonian-saints-auckland/"
)


# These branches already or potentially carry rows from countries other than
# New Zealand. Their payloads must be merged, never replaced.
SHARED_PAYLOAD_PARENTS = {
    "an-australia",
    "sr-australia-new-zealand",
    "ro-australia-nz",
    "mk-australia-nz",
    "ru-australia-and-new-zealand-rocor",
}


ENGLISH_NAMES = {
    "nz-ep-wellington-annunciation-cathedral":
        "Cathedral of the Annunciation of the Theotokos in Wellington",
    "nz-ep-wellington-saint-andrew":
        "Metropolitan Church of Saint Andrew the Apostle in Wellington",
    "nz-ep-petone-saint-nektarios":
        "Church of Saint Nektarios in Petone",
    "nz-ep-auckland-holy-trinity":
        "Church of the Holy Trinity in Auckland",
    "nz-ep-christchurch-dormition":
        "Church of the Dormition of the Theotokos in Christchurch",
    "nz-ep-palmerston-north-saint-john-forerunner":
        "Church of Saint John the Forerunner in Palmerston North",
    "nz-ep-new-plymouth-saint-nicholas":
        "Church of Saint Nicholas in New Plymouth",
    "nz-ep-hastings-saint-demetrius":
        "Church of Saint Demetrius in Hastings",
    "nz-ep-masterton-divine-transfiguration":
        "Pilgrimage Church of the Divine Transfiguration in Masterton",
    "nz-ep-wellington-saint-lazarus-chapel":
        "Cemetery Chapel of Saint Lazarus in Wellington",
    "nz-ep-whangarei-transfiguration":
        "Church of the Transfiguration of the Savior in Whangarei",
    "nz-ep-levin-holy-archangels-monastery":
        "Holy Monastery of the Holy Archangels in Levin",
    "nz-antioch-auckland-waikato-saint-george":
        "Saint George Mission in Auckland and Waikato",
    "nz-antioch-wellington-saint-george":
        "Saint George Mission in Wellington",
    "nz-antioch-dunedin-saint-michael":
        "Church of Saint Michael the Archangel in Dunedin",
    "nz-serbian-auckland-saint-milutin":
        "Church of Saint Milutin the King in Auckland",
    "nz-serbian-wellington-saint-sava":
        "Church of Saint Sava in Wellington",
    "nz-serbian-christchurch-saint-nicholas":
        "Saint Nicholas Serbian Orthodox Parish in Christchurch",
    "nz-romanian-wellington-saint-mary":
        "Saint Mary's Church in Wellington",
    "nz-romanian-auckland-saint-ignatius":
        "Saint Ignatius the God-Bearer Parish in Auckland",
    "nz-romanian-hamilton-saint-george":
        "Saint George Church in Hamilton",
    "nz-romanian-christchurch-dormition":
        "Dormition of the Mother of God Church in Christchurch",
    "nz-romanian-ashburton-saint-stephen":
        "Saint Stephen the Archdeacon Church in Ashburton",
    "nz-romanian-gore-saint-basil":
        "Saint Basil the Great Church in Gore",
    "nz-rocor-auckland-resurrection":
        "Church of the Resurrection of Christ in Auckland",
    "nz-rocor-wellington-christ-saviour":
        "Church of Christ the Saviour in Wellington",
    "nz-rocor-christchurch-saint-nicholas":
        "Saint Nicholas Church in Christchurch",
    "nz-macedonian-auckland-all-macedonian-saints":
        "Church of the Synaxis of All Macedonian Saints in Auckland",
}


ROWS_BY_PARENT = {
    "ep-new-zealand": [
        dict(
            id="nz-ep-wellington-annunciation-cathedral",
            parent="ep-new-zealand", kind="parish", rank="Cathedral",
            local="Ἱερός Καθεδρικός Ναός Εὐαγγελισμός τῆς Θεοτόκου",
            country="NZ", dedication="The Annunciation of the Theotokos",
            address=["3 Hania Street, Wellington"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-wellington-saint-andrew",
            parent="ep-new-zealand", kind="parish",
            rank="Metropolitan Church",
            local="Ἱερός Μητροπολιτικός Ναός Ἁγίου Ἀποστόλου Ἀνδρέου",
            country="NZ", dedication="Saint Andrew the Apostle",
            address=["365 Broadway Street, Miramar, Wellington 6022"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-petone-saint-nektarios",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Ἁγίου Νεκταρίου", country="NZ",
            dedication="Saint Nektarios",
            address=["23 Bay Street, Petone, Hutt Valley"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-auckland-holy-trinity",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Ἁγίας Τριάδος", country="NZ",
            dedication="The Holy Trinity",
            address=["106 Western Springs Road, Auckland"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-christchurch-dormition",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Κοιμήσεως τῆς Θεοτόκου", country="NZ",
            dedication="The Dormition of the Theotokos",
            address=["58 Malvern Street, St Albans, Christchurch"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-palmerston-north-saint-john-forerunner",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Τιμίου Προδρόμου", country="NZ",
            dedication="Saint John the Forerunner",
            address=["30 Rochester Street, Palmerston North"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-new-plymouth-saint-nicholas",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Ἁγίου Νικολάου", country="NZ",
            dedication="Saint Nicholas",
            address=["201 Carrington Street, Vogeltown, New Plymouth"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-hastings-saint-demetrius",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Ἁγίου Δημητρίου", country="NZ",
            dedication="Saint Demetrius",
            address=["Willowpark Road and Heretaunga Street, Hastings"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-masterton-divine-transfiguration",
            parent="ep-new-zealand", kind="parish",
            rank="Pilgrimage Church",
            local="Ἱερός Προσκυνηματικός Ναός Θείας Μεταμορφώσεως",
            country="NZ", dedication="The Divine Transfiguration",
            address=["Masterton"], site=EP_NEW_ZEALAND,
            sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-wellington-saint-lazarus-chapel",
            parent="ep-new-zealand", kind="parish",
            rank="Cemetery Chapel",
            local="Ἱερόν Κοιμητηριακόν Παρεκκλήσιον Ἁγ. Λαζάρου",
            country="NZ", dedication="Saint Lazarus",
            address=["Makara, Wellington"], site=EP_NEW_ZEALAND,
            sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-whangarei-transfiguration",
            parent="ep-new-zealand", kind="parish", rank="Parish",
            local="Ἱερός Ναός Μεταμορφώσεως τοῦ Σωτῆρος", country="NZ",
            dedication="The Transfiguration of the Savior",
            address=["63 Hatea Road, Whangarei"], site=EP_NEW_ZEALAND,
            sources=[EP_NEW_ZEALAND]),
        dict(
            id="nz-ep-levin-holy-archangels-monastery",
            parent="ep-new-zealand", kind="monastery", rank="Monastery",
            local="Ἱερά Μονή Παμμεγίστων Ταξιαρχῶν", country="NZ",
            dedication="The Holy Archangels",
            address=["495 Gladstone Road, RD1, Levin 5571"],
            site=EP_NEW_ZEALAND, sources=[EP_NEW_ZEALAND]),
    ],
    "an-australia": [
        dict(
            id="nz-antioch-auckland-waikato-saint-george",
            parent="an-australia", kind="parish", rank="Mission",
            local="St. George Mission, Auckland", country="NZ",
            dedication="Saint George",
            address=[
                "All Saints' Anglican Church, old building",
                "Corner Cook Street and Selwyn Road, Howick, Auckland",
            ],
            languages=["Arabic", "English"],
            site="https://stgeorgeorthodoxnz.wordpress.com/",
            sources=[ANTIOCH_NZ, ANTIOCH_AUCKLAND]),
        dict(
            id="nz-antioch-wellington-saint-george",
            parent="an-australia", kind="parish", rank="Mission",
            local="St. George Mission, Wellington", country="NZ",
            dedication="Saint George",
            address=["365 Broadway, Wellington 6022"],
            languages=["Arabic", "English"],
            site=ANTIOCH_WELLINGTON,
            sources=[ANTIOCH_NZ, ANTIOCH_WELLINGTON]),
        dict(
            id="nz-antioch-dunedin-saint-michael",
            parent="an-australia", kind="parish", rank="Parish",
            local="St. Michael the Archangel, Dunedin", country="NZ",
            dedication="Saint Michael the Archangel",
            address=["72 Fingal Street, South Dunedin"],
            site=ANTIOCH_DUNEDIN,
            sources=[ANTIOCH_NZ, ANTIOCH_DUNEDIN]),
    ],
    "sr-australia-new-zealand": [
        dict(
            id="nz-serbian-auckland-saint-milutin",
            parent="sr-australia-new-zealand", kind="parish",
            rank="Parish",
            local=(
                "Свети Краљ Милутин Српски - Парохија и црквена општина "
                "за Окланд и Хамилтон"
            ),
            country="NZ", dedication="Saint Milutin the King",
            address=[
                "315 Point Chevalier Road, Point Chevalier, Auckland 1022",
            ],
            site="https://www.svetikralj.org.nz/",
            sources=[SERBIAN_NZ, SERBIAN_AUCKLAND,
                     "https://www.svetikralj.org.nz/"]),
        dict(
            id="nz-serbian-wellington-saint-sava",
            parent="sr-australia-new-zealand", kind="parish",
            rank="Parish", local="ST SAVA SERBIAN ORTHODOX CHURCH",
            country="NZ", dedication="Saint Sava",
            address=["75 The Parade, Island Bay, Wellington 6023"],
            site="https://www.svetisava.org.nz/",
            sources=[SERBIAN_NZ, SERBIAN_WELLINGTON,
                     "https://www.svetisava.org.nz/"]),
        dict(
            id="nz-serbian-christchurch-saint-nicholas",
            parent="sr-australia-new-zealand", kind="parish",
            rank="Parish", local="ST NICHOLAS SERBIAN ORTHODOX PARISH",
            country="NZ", dedication="Saint Nicholas",
            address=["297 Brougham Street, Christchurch"],
            site=SERBIAN_CHRISTCHURCH,
            sources=[SERBIAN_NZ, SERBIAN_CHRISTCHURCH]),
    ],
    "ro-australia-nz": [
        dict(
            id="nz-romanian-wellington-saint-mary",
            parent="ro-australia-nz", kind="parish", rank="Parish",
            local="Biserica Sfânta Maria - Wellington", country="NZ",
            dedication="Saint Mary",
            address=["511 Adelaide Road, 6002 Berhampore"],
            site="https://orthodoxrowellington.org.nz/wordpress/",
            sources=[ROMANIAN_NZ, ROMANIAN_API]),
        dict(
            id="nz-romanian-auckland-saint-ignatius",
            parent="ro-australia-nz", kind="parish", rank="Parish",
            local="Parohia Sfântul Ignatie Teoforul - Auckland",
            country="NZ", dedication="Saint Ignatius the God-Bearer",
            address=["355 Waitakere Road, Taupaki"],
            site="http://www.biserica.nz",
            sources=[ROMANIAN_NZ, ROMANIAN_API]),
        dict(
            id="nz-romanian-hamilton-saint-george",
            parent="ro-australia-nz", kind="parish", rank="Parish",
            local="Biserica Sfântul Gheorghe - Hamilton", country="NZ",
            dedication="Saint George",
            address=["591 Matangi Road, Tamahere 3284, Hamilton"],
            site="https://stgeorgehamilton.nz/",
            sources=[ROMANIAN_NZ, ROMANIAN_API]),
        dict(
            id="nz-romanian-christchurch-dormition",
            parent="ro-australia-nz", kind="parish", rank="Parish",
            local="Biserica Adormirea Maicii Domnului - Christchurch",
            country="NZ", dedication="The Dormition of the Mother of God",
            address=["40 Phillips Street, Phillipstown"],
            site="https://saintmary-christchurch.co.nz",
            sources=[ROMANIAN_NZ, ROMANIAN_API]),
        dict(
            id="nz-romanian-ashburton-saint-stephen",
            parent="ro-australia-nz", kind="parish", rank="Parish",
            local="Biserica Sfântul Arhidiacon Stefan - Ashburton",
            country="NZ", dedication="Saint Stephen the Archdeacon",
            address=["Ashburton"],
            site=(
                "https://roeanz.com.au/parohia/"
                "biserica-sfantul-arhidiacon-stefan-ashburton"
            ),
            sources=[ROMANIAN_NZ, ROMANIAN_API]),
        dict(
            id="nz-romanian-gore-saint-basil",
            parent="ro-australia-nz", kind="parish", rank="Parish",
            local="Biserica Sfântul Ier. Vasile cel Mare - Gore",
            country="NZ", dedication="Saint Basil the Great",
            address=["Gore"],
            site=(
                "https://roeanz.com.au/parohia/"
                "biserica-sfantul-ier-vasile-cel-mare-gore"
            ),
            sources=[ROMANIAN_NZ, ROMANIAN_API]),
    ],
    "ru-australia-and-new-zealand-rocor": [
        dict(
            id="nz-rocor-auckland-resurrection",
            parent="ru-australia-and-new-zealand-rocor", kind="parish",
            rank="Parish", local="Храм Воскресения Христова",
            country="NZ", dedication="The Resurrection of Christ",
            address=["455-461 Dominion Road, Mount Eden, Auckland"],
            languages=["Church Slavonic", "English"],
            site="https://www.orthodox.net.nz/",
            sources=[ROCOR_AUCKLAND, "https://www.orthodox.net.nz/"]),
        dict(
            id="nz-rocor-wellington-christ-saviour",
            parent="ru-australia-and-new-zealand-rocor", kind="parish",
            rank="Parish",
            local="Храм Христа Спасителя, г. Веллингтон (Новая Зеландия)",
            country="NZ", dedication="Christ the Saviour",
            address=["62 Darlington Road, Miramar, Wellington"],
            site="https://www.russian-church.nz/",
            sources=[ROCOR_WELLINGTON, "https://www.russian-church.nz/"]),
        dict(
            id="nz-rocor-christchurch-saint-nicholas",
            parent="ru-australia-and-new-zealand-rocor", kind="parish",
            rank="Parish", local="St. Nicholas Russian Orthodox Parish",
            country="NZ", dedication="Saint Nicholas",
            address=[
                "297 Brougham Street, Sydenham, Christchurch 8023",
            ],
            languages=["Church Slavonic", "English", "Serbian"],
            founded=["1962"],
            site="https://www.stnicholaschurch.org.nz/",
            sources=[ROCOR_CHRISTCHURCH,
                     "https://www.stnicholaschurch.org.nz/about/"]),
    ],
    "mk-australia-nz": [
        dict(
            id="nz-macedonian-auckland-all-macedonian-saints",
            parent="mk-australia-nz", kind="parish", rank="Parish",
            local=(
                "МПЦ Собор на Сите Македонски Светители - Окланд, "
                "Нов Зеланд"
            ),
            country="NZ", dedication="All Macedonian Saints",
            address=["P. O. Box 45-307, Waitakere, Auckland 0610"],
            site=MACEDONIAN_AUCKLAND, sources=[MACEDONIAN_AUCKLAND]),
    ],
}


EXPECTED_COUNTS = {
    "ep-new-zealand": 12,
    "an-australia": 3,
    "sr-australia-new-zealand": 3,
    "ro-australia-nz": 6,
    "ru-australia-and-new-zealand-rocor": 3,
    "mk-australia-nz": 1,
}


def clean(row):
    out = {key: value for key, value in row.items()
           if value not in (None, "", [])}
    row_id = out.get("id")
    if row_id not in ENGLISH_NAMES:
        raise ValueError("%s lacks an English name" % row_id)
    out["name"] = ENGLISH_NAMES[row_id]
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row_id)
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % row_id)
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("site") and not out["site"].startswith("http"):
        raise ValueError("%s carries a non-URL site" % row_id)
    for key in ("address", "languages", "services", "founded"):
        if out.get(key) and (not isinstance(out[key], list) or
                             not all(isinstance(value, str)
                                     for value in out[key])):
            raise ValueError("%s has invalid %s" % (row_id, key))
    for value in out.values():
        texts = value if isinstance(value, list) else [value]
        for text in texts:
            if isinstance(text, str) and ("\u2013" in text or "\u2014" in text):
                raise ValueError("%s carries a forbidden long dash" % row_id)
    return out


def build():
    public = json.loads(DIRECTORY_INDEX.read_text(encoding="utf-8"))
    public_ids = {row.get("id") for row in public.get("rows", [])}
    missing_parents = set(ROWS_BY_PARENT) - public_ids
    if missing_parents:
        raise ValueError("unknown parent ids: %s" %
                         ", ".join(sorted(missing_parents)))
    if set(ROWS_BY_PARENT) != set(EXPECTED_COUNTS):
        raise ValueError("parent count assertions do not match the source rows")

    contributions = {}
    seen = set()
    for parent, source_rows in ROWS_BY_PARENT.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen or row_id in public_ids:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if row.get("parent") != parent:
                raise ValueError("%s is grouped under the wrong parent" % row_id)
            if row.get("country") != "NZ":
                raise ValueError("%s is not a New Zealand row" % row_id)
            if row.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("rank") or not row.get("local"):
                raise ValueError("%s lacks its official rank or local name" %
                                 row_id)
            if not row.get("dedication"):
                raise ValueError("%s lacks a published dedication" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED_COUNTS[parent]:
            raise ValueError("%s must contribute %d rows" %
                             (parent, EXPECTED_COUNTS[parent]))
        contributions[parent] = rows

    if set(ENGLISH_NAMES) != seen:
        extra = set(ENGLISH_NAMES) - seen
        missing = seen - set(ENGLISH_NAMES)
        raise ValueError("English name coverage differs: extra=%s missing=%s" %
                         (sorted(extra), sorted(missing)))
    if sum(len(rows) for rows in contributions.values()) != 28:
        raise ValueError("New Zealand must contribute exactly 28 rows")
    return contributions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        contributions = build()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("directory New Zealand: %s" % exc, file=sys.stderr)
        return 1
    counts = ", ".join(
        "%s=%d" % (parent, len(rows))
        for parent, rows in contributions.items()
    )
    print("New Zealand directory contributions: 28 rows (%s)" % counts)
    print("Shared payload parents: %s" %
          ", ".join(sorted(SHARED_PAYLOAD_PARENTS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
