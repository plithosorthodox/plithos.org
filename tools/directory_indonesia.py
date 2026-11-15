#!/usr/bin/env python3
"""Current officially named canonical Orthodox bodies in Indonesia.

The current Ecumenical Patriarchate metropolitan roster, Moscow Patriarchate
exarchal map, and ROCOR synodal directory establish the bodies published here.
Russian listings that appear in both the exarchal map and the more specific
ROCOR directory are assigned to the ROCOR parent once and cite both sources.

    python tools/directory_indonesia.py --check
    python tools/directory_indonesia.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

EP_ROSTER = "https://omsgsa.org/parishes-indonesia"
EP_SCOPE = "https://omsgsa.org/about-us"
MP_MAP = "https://exarchate.asia/en/karta-prihodov/"
MP_DIOCESES = "https://exarchate.asia/en/patriarshij-ekzarhat/eparhii/"
ROCOR_BASE = "https://directory.synod.com/listing/%d/"

EP_PARENT = "ep-singapore"
MP_PARENT = "ru-singapore"
ROCOR_PARENT = "ru-australia-and-new-zealand-rocor"

ROWS = []


def add(row_id, parent, name, local, rank="Parish", dedication=None,
        address=None, languages=None, sources=None, kind="parish"):
    row = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "ID",
        "sources": list(sources or []),
    }
    if dedication:
        row["dedication"] = dedication
    if address:
        row["address"] = list(address)
    if languages:
        row["languages"] = list(languages)
    if len(row["sources"]) == 1:
        row["site"] = row["sources"][0]
    ROWS.append(row)


# Ecumenical Patriarchate, Metropolitanate of Singapore and South Asia.
add(
    "id-ep-medan-saint-demetrios", EP_PARENT,
    "Saint Demetrios Church in Medan", "Saint Demetrios Chrurch",
    dedication="Saint Demetrios",
    address=[
        "Jl. Kapten Purba Gg. Gereja No. 1, Simalingkar",
        "Medan, North Sumatra 20141, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-medan-saint-sophia", EP_PARENT,
    "Saint Sophia Church in Medan", "Saint Sophia Church",
    dedication="Saint Sophia",
    address=[
        "Jl. Kapten Purba Gg. Gereja No. 1, Simalingkar",
        "Medan, North Sumatra 20141, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-tarutung-saint-evdokia", EP_PARENT,
    "Saint Evdokia Church in Tarutung", "Saint Evdokia Church",
    dedication="Saint Evdokia",
    address=["Hausada-sada, Tarutung, North Sumatra, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-lubuk-pakam-saint-john-baptist", EP_PARENT,
    "Saint John the Baptist Church in Lubuk Pakam",
    "Saint John the Baptism Church",
    dedication="Saint John the Baptist",
    address=["Lubuk Pakam, North Sumatra, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-hilifaosi-saint-catherine", EP_PARENT,
    "Saint Catherine Church in Hilifaosi", "Saint Catherine Church",
    dedication="Saint Catherine",
    address=["Hilifaosi, Nias Island, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-sirombu-saints-paul-martha", EP_PARENT,
    "Saints Paul and Martha Church in Sirombu",
    "Saint Paul and Saint Martha Church",
    dedication="Saints Paul and Martha",
    address=["Sirombu, Nias Island, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-gunung-sitoli-saint-nicholas", EP_PARENT,
    "Saint Nicholas Chapel in Gunung Sitoli", "Saint Nicholaos Chapel",
    rank="Chapel", dedication="Saint Nicholas the Wonderworker",
    address=["Gunung Sitoli, Nias Island, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-sidikalang-saint-ephraim", EP_PARENT,
    "Saint Ephraim Church in Sidikalang", "Saint Ephraim Church",
    dedication="Saint Ephraim",
    address=["Sidikalang, North Sumatra, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-sidikalang-annunciation", EP_PARENT,
    "Annunciation of the Theotokos Church in Sidikalang",
    "Annunciation of Theotokos Church",
    dedication="The Annunciation of the Theotokos",
    address=["Sidikalang, North Sumatra, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-siparbue-resurrection", EP_PARENT,
    "Holy Resurrection of Christ Church in Siparbue",
    "Holy Resurrection of the Christ Church",
    dedication="The Holy Resurrection of Christ",
    address=["Siparbue, Tarutung, North Sumatra, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-najambean-saint-nicholas", EP_PARENT,
    "Saint Nicholas Church in Najambean", "Saint Nicholaos Church",
    dedication="Saint Nicholas the Wonderworker",
    address=["Najambean, Tarutung, North Sumatra, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-jakarta-epiphany", EP_PARENT,
    "Holy Epiphany Church in Jakarta", "Epiphany Church Jakarta",
    dedication="The Holy Epiphany of the Lord",
    address=[
        "Jl. Meriam Block D 109, Kodam Kalimalang",
        "East Jakarta, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-yogyakarta-saint-dionysios", EP_PARENT,
    "Saint Dionysios of Zakynthos Church in Yogyakarta",
    "Saint Dionysios of Zakynthos Yogyakarta",
    dedication="Saint Dionysios of Zakynthos",
    address=[
        "Jl. Kricak Kidul TRI/1225",
        "Yogyakarta, Central Java, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-cilacap-saint-catherine", EP_PARENT,
    "Saint Catherine Church in Cilacap", "Saint Catherine Church Cilacap",
    dedication="Saint Catherine",
    address=[
        "Jl. Serutu A 23/409",
        "Cilacap, Central Java, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-grasak-saints-cyril-methodios", EP_PARENT,
    "Saints Cyril and Methodios Church in Grasak",
    "Saints Cyril and Methodios Grasak Boyolali",
    dedication="Saints Cyril and Methodios",
    address=[
        "Grasak RT 02 RW 04, Kismoyoso, Ngemplak",
        "Boyolali, Central Java, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-pandeyan-saint-catherine", EP_PARENT,
    "Saint Catherine Church in Pandeyan", "Saint Catherine Church Pandeyan",
    dedication="Saint Catherine",
    address=[
        "Pandeyan RT 12 RW 04, Ngemplak",
        "Boyolali, Central Java, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-pandeyan-saint-fanourios", EP_PARENT,
    "Saint Fanourios Church in Pandeyan", "Saint Fanourios Church Pandeyan Ngemplak Boyolali",
    dedication="Saint Fanourios",
    address=[
        "Pandeyan RT 12 RW 04, Ngemplak",
        "Boyolali, Central Java, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-krikilan-dormition", EP_PARENT,
    "Dormition of the Theotokos Church in Krikilan",
    "The Dormition of Theotokos Church",
    dedication="The Dormition of the Theotokos",
    address=["Krikilan, Ngemplak, Boyolali, Central Java, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-mojokerto-dormition", EP_PARENT,
    "Dormition of the Theotokos Church in Gunung Gedangan",
    "The Dormition of Theotokos Church Gunung Gedangan Mojokerto",
    dedication="The Dormition of the Theotokos",
    address=[
        "Jl. Kedung Sari RT 02 RW 03, Gunung Gedangan",
        "Mojokerto, East Java, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-surabaya-saint-paisios", EP_PARENT,
    "Saint Paisios Orthodox Community in Surabaya",
    "Saint Paisios Orthodox Community Surabaya",
    rank="Community", dedication="Saint Paisios of Mount Athos",
    address=["Jl. Bendul Merisi Selatan IV 11, Surabaya, East Java, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-jember-dormition", EP_PARENT,
    "Dormition of the Theotokos Orthodox Community in Jember",
    "Dormition of Theotokos Orthodox Community Jember",
    rank="Community", dedication="The Dormition of the Theotokos",
    address=["Jl. Doho 2 No. 01, Sumber Sari, Jember, East Java, Indonesia"],
    sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-singaraja-all-saints", EP_PARENT,
    "All Saints Church in Singaraja", "All Saints Church Singaraja Bali",
    dedication="All Saints",
    address=[
        "Jl. Dewi Uma No. 1, Dusun Bangkang RT 04",
        "Baktiseraga, Singaraja, Bali, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)
add(
    "id-ep-kupang-saint-kosmas", EP_PARENT,
    "Saint Kosmas of Aitolos Church in Kupang",
    "Saint Kosmas of Aitolos Church Nusa Tenggara Timur",
    dedication="Saint Kosmas of Aitolos",
    address=[
        "Jl. Gerbang Madya RT 07 RW 03, Kelapa Lima",
        "Kupang, East Nusa Tenggara, Indonesia",
    ], sources=[EP_ROSTER, EP_SCOPE],
)


# ROCOR synodal directory. Eight entries also appear on the Moscow exarchal
# map; those entries cite both sources and are not duplicated below.
ROCOR_ROWS = [
    (181, "id-rocor-surabaya-saint-jonah", "Community of Saint Jonah of Manchuria in Surabaya", "Community of St Jonah of Manchuria", "Community", "Saint Jonah of Manchuria", ["Dharmahusada Indah Selatan VII D-126", "Surabaya, East Java 60115, Indonesia"], ["Indonesian", "Church Slavonic", "Greek"], True),
    (182, "id-rocor-mojokerto-saint-panteleimon", "Community of Saint Panteleimon in Mojokerto", "Community of St. Panteleimon", "Community", "Saint Panteleimon", ["Mojokerto, East Java, Indonesia"], ["Javanese"], False),
    (183, "id-rocor-gresik-saint-seraphim", "Community of Saint Seraphim of Sarov in Gresik", "Community of St. Seraphim of Sarov", "Community", "Saint Seraphim of Sarov", ["Bougenvile V/7, Kota Damai, Kedamaian", "Gresik, East Java 61174, Indonesia"], ["Javanese", "Indonesian"], True),
    (184, "id-rocor-medan-saint-sergius", "Community of Saint Sergius of Radonezh in Medan", "Community of St. Sergius of Radonezh", "Community", "Saint Sergius of Radonezh", ["Jl. Tomat No. 16/7", "Medan, North Sumatra 20153, Indonesia"], ["Indonesian", "English", "Greek"], True),
    (185, "id-rocor-grasak-mission", "Grasak Mission", "Grasak Mission", "Mission", None, ["Grasak, Central Java, Indonesia"], ["Javanese"], False),
    (186, "id-rocor-surakarta-holy-trinity", "Holy Trinity Orthodox Church in Surakarta", "Holy Trinity Orthodox Church", "Parish", "The Holy Trinity", ["Jl. Pajajaran No. 20", "Sumber RT 02 RW XV, Banjarsari", "Surakarta, Central Java 57138, Indonesia"], ["Indonesian", "Javanese"], False),
    (187, "id-rocor-jayapura-saint-athanasius", "Saint Athanasius the Great Parish in Jayapura", "Jayapura Mission", "Mission", "Saint Athanasius the Great", ["Jayapura, Papua, Indonesia"], ["Indonesian"], True),
    (188, "id-rocor-yogyakarta-mission", "Yogyakarta City Mission", "Yogyakarta City Mission", "Mission", None, ["Yogyakarta, Central Java, Indonesia"], ["Javanese"], False),
    (189, "id-rocor-jombang-saint-john-baptist", "Saint John the Baptist Church in Jombang", "St. John the Baptist Church", "Parish", "Saint John the Baptist", ["Jombang, East Java, Indonesia"], ["Javanese"], False),
    (190, "id-rocor-kabuh-mission", "Kabuh Village Mission", "Kabuh Village Mission", "Mission", None, ["Kabuh, East Java, Indonesia"], ["Indonesian"], False),
    (191, "id-rocor-kupang-mission", "Kupang Mission", "Kupang Mission", "Mission", None, ["Kupang, East Nusa Tenggara, Indonesia"], ["Indonesian"], False),
    (192, "id-rocor-bandung-mission", "Bandung Mission", "Bandung Mission", "Mission", None, ["Bandung, West Java, Indonesia"], ["Javanese"], True),
    (193, "id-rocor-ngemplak-mission", "Ngemplak Mission", "Ngemplak Mission", "Mission", None, ["Ngemplak, Central Java, Indonesia"], ["Javanese"], False),
    (194, "id-rocor-plandaan-mission", "Mission in Plandaan", "Mission in Plandaan", "Mission", None, ["Plandaan, East Java, Indonesia"], ["Javanese"], False),
    (195, "id-rocor-salatiga-saint-anthony", "Saint Anthony the Great Community in Salatiga", "St. Anthony the Great Community", "Community", "Saint Anthony the Great", ["Salatiga, Central Java, Indonesia"], ["Javanese"], False),
    (196, "id-rocor-tlatar-saint-george", "Saint George Mission in Tlatar", "St. George Mission", "Mission", "Saint George", ["Tlatar, Central Java, Indonesia"], ["Javanese"], False),
    (197, "id-rocor-semanggi-saint-john-kronstadt", "Saint John of Kronstadt Mission in Semanggi", "St. John of Kronstadt Mission", "Mission", "Saint John of Kronstadt", ["Semanggi, Central Java, Indonesia"], ["Javanese"], False),
    (198, "id-rocor-boyolali-saint-mark", "Saint Mark Mission in Boyolali", "St. Mark Mission", "Mission", "Saint Mark the Evangelist", ["Jl. Tentara Pelajar, Dk. Tlatar RT 01 RW 02, Kebonbimo", "Boyolali, Central Java, Indonesia"], ["Javanese"], False),
    (199, "id-rocor-manado-nativity-theotokos", "Nativity of the Theotokos Parish in Manado", "Nativity of the Theotokos Parish", "Parish", "The Nativity of the Theotokos", ["Manado, North Sulawesi, Indonesia"], ["Indonesian"], False),
    (200, "id-rocor-jakarta-saint-thomas", "Saint Thomas Parish in Jakarta", "St. Thomas Parish", "Parish", "Saint Thomas the Apostle", ["Jakarta, Indonesia"], ["Indonesian"], True),
    (201, "id-rocor-tambak-mission", "Tambak Mission", "Tambak Mission", "Mission", None, ["Tambak, Central Java, Indonesia"], ["Javanese"], False),
    (202, "id-rocor-langowan-saint-gregory-nyssa", "Saint Gregory of Nyssa Church in Langowan", "St. Gregory of Nyssa Church", "Parish", "Saint Gregory of Nyssa", ["Langowan, North Sulawesi, Indonesia"], ["Indonesian"], False),
    (203, "id-rocor-tomohon-saint-paraskeva", "Holy Great Martyr Paraskeva Parish in Tomohon", "Tomohon Mission", "Mission", "The Holy Great Martyr Paraskeva", ["Tomohon, North Sulawesi, Indonesia"], ["Indonesian"], True),
    (204, "id-rocor-singaraja-saint-nicholas", "Saint Nicholas the Wonderworker Parish in Singaraja", "Bali Mission", "Mission", "Saint Nicholas the Wonderworker", ["Singaraja, Bali, Indonesia"], ["Indonesian"], True),
    (205, "id-rocor-jombang-city-mission", "Jombang City Mission", "Jombang City Mission, East Java", "Mission", None, ["Jombang, East Java, Indonesia"], ["English"], False),
    (206, "id-rocor-bekasi-prophet-elijah", "Community of the Holy Prophet Elijah in Bekasi", "Community St. Elijah The Prophet", "Community", "The Holy Prophet Elijah", ["Jl. Raya Cikarang Cibarusah No. 7", "Pasirsari, Cikarang Selatan", "Bekasi, West Java 17530, Indonesia"], ["Indonesian", "English"], False),
]

for listing_id, row_id, name, local, rank, dedication, address, languages, also_mp in ROCOR_ROWS:
    sources = [ROCOR_BASE % listing_id]
    if also_mp:
        sources.append(MP_MAP)
    add(
        row_id, ROCOR_PARENT, name, local, rank=rank,
        dedication=dedication, address=address, languages=languages,
        sources=sources,
    )


# Moscow Patriarchate Diocese of Singapore bodies not represented by a more
# specific current ROCOR synodal listing.
add(
    "id-ru-bekasi-saint-vladimir-metochion", MP_PARENT,
    "Archpastor's Metochion of Saint Vladimir's Church in Bekasi",
    "Archpastor's Metochion of St. Vladimir's Church in Bekasi",
    rank="Metochion", dedication="Saint Vladimir, Equal-to-the-Apostles",
    address=[
        "Jalan Kampung Sawah Raya, Gg. Kenanga 2 No. 90",
        "Jatimurni, Pondok Melati, Bekasi, West Java 17431, Indonesia",
    ], sources=[MP_MAP, MP_DIOCESES],
)
add(
    "id-ru-surakarta-meeting-lord", MP_PARENT,
    "Meeting of the Lord Parish in Surakarta",
    "Parish in honour of the Meeting of the Lord in Surakarta",
    dedication="The Meeting of the Lord",
    address=["Surakarta, Central Java, Indonesia"],
    sources=[MP_MAP, MP_DIOCESES],
)
add(
    "id-ru-ungasan-saint-sergius", MP_PARENT,
    "Saint Sergius of Radonezh Parish in Ungasan",
    "Parish of St. Sergiy of Radonezh in Ungasan on the island of Bali",
    dedication="Saint Sergius of Radonezh",
    address=["Jl. Goa Gong, Ungasan, South Kuta, Badung, Bali 80361, Indonesia"],
    sources=[MP_MAP, MP_DIOCESES],
)
add(
    "id-ru-medan-saint-benedict", MP_PARENT,
    "Saint Benedict of Nursia Parish in Medan",
    "Parish of St. Benedict of Nursia in Medan",
    dedication="Saint Benedict of Nursia",
    address=[
        "Jl. Sei Brantas No. 8G, Perumahan De Villa",
        "Medan, North Sumatra, Indonesia",
    ], sources=[MP_MAP, MP_DIOCESES],
)
add(
    "id-ru-boyolali-saint-basil", MP_PARENT,
    "Saint Basil the Great Parish in Boyolali",
    "Parish of St. Basil the Great in Boyolali",
    dedication="Saint Basil the Great",
    address=[
        "Jl. Wonokerti No. 884, RT 019 RW 006, Pelem, Simo",
        "Boyolali, Central Java, Indonesia",
    ], sources=[MP_MAP, MP_DIOCESES],
)
add(
    "id-ru-malang-saint-kosmas", MP_PARENT,
    "Saint Kosmas of Aitolos Parish in Malang",
    "Parish of St. Equal to the Apostles Cosmos of Aetolia in Malang",
    dedication="Saint Kosmas of Aitolos",
    address=[
        "Jl. Danau Maninjau Barat D3 No. A2, Sawojajar",
        "Malang, East Java, Indonesia",
    ], sources=[MP_MAP, MP_DIOCESES],
)
add(
    "id-ru-jayapura-saint-nicholas", MP_PARENT,
    "Saint Nicholas the Wonderworker Parish in Jayapura",
    "Parish of St. Nicholay, the Wonderworker of Myra, in Jayapura",
    dedication="Saint Nicholas the Wonderworker",
    address=[
        "Kampung Pokhouw RT 002 RW 002, Yabansai, Heram",
        "Jayapura, Papua, Indonesia",
    ], sources=[MP_MAP, MP_DIOCESES],
)


EXPECTED = {
    EP_PARENT: 23,
    ROCOR_PARENT: 26,
    MP_PARENT: 7,
}
ENGLISH_NAMES = {row["id"]: row["name"] for row in ROWS}
ENGLISH_SEATS = {}
EXPECTED_KINDS = {"parish"}
EXPECTED_RANKS = {"Parish", "Chapel", "Community", "Mission", "Metochion"}
FORBIDDEN_FIELDS = {
    "contact", "contacts", "email", "phone", "telephone", "clergy",
    "priest", "rector", "abbot", "abbess",
}
FORBIDDEN_PUNCTUATION = (
    "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d", "\ufffd",
)


def clean(source):
    row = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if len(sources) != len(set(sources)):
        raise ValueError("%s repeats a source" % row.get("id"))
    if not all(str(url).startswith("https://") for url in sources):
        raise ValueError("%s carries a non-HTTPS source" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in FORBIDDEN_PUNCTUATION):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    return row


def semantic_key(value):
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def build():
    payload_rows = {parent: [] for parent in EXPECTED}
    seen_ids = set()
    seen_names = {}
    for source in ROWS:
        row = clean(source)
        row_id = row.get("id")
        if not row_id or row_id in seen_ids:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if not re.fullmatch(r"[a-z0-9-]+", row_id):
            raise ValueError("%s is not a stable ASCII id" % row_id)
        if row.get("parent") not in EXPECTED or row.get("country") != "ID":
            raise ValueError("%s is grouped outside Indonesia" % row_id)
        if (row.get("kind") not in EXPECTED_KINDS
                or row.get("rank") not in EXPECTED_RANKS):
            raise ValueError("%s has an unsupported kind or rank" % row_id)
        if not row.get("name") or not row.get("local"):
            raise ValueError("%s lacks a usable official identity" % row_id)
        if FORBIDDEN_FIELDS.intersection(row):
            raise ValueError("%s carries contact or personnel prose" % row_id)
        for key in ("address", "languages", "sources", "cite"):
            if row.get(key) and (not isinstance(row[key], list)
                                 or not all(isinstance(value, str)
                                            for value in row[key])):
                raise ValueError("%s has invalid %s" % (row_id, key))
        name_key = semantic_key(row["name"])
        if name_key in seen_names:
            raise ValueError("semantic duplicate: %s and %s" %
                             (seen_names[name_key], row_id))
        seen_names[name_key] = row_id
        seen_ids.add(row_id)
        payload_rows[row["parent"]].append(row)
    for parent, expected in EXPECTED.items():
        if len(payload_rows[parent]) != expected:
            raise ValueError(
                "Indonesia must publish exactly %d rows under %s" %
                (expected, parent))
    if set(ENGLISH_NAMES) != seen_ids:
        raise ValueError("Indonesia English name map is out of sync")
    return {
        parent: {
            "v": 1,
            "parent": parent,
            "country": "ID",
            "rows": rows,
        }
        for parent, rows in payload_rows.items()
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
        print("directory Indonesia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Indonesia: 56 current bodies across 3 canonical branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
