#!/usr/bin/env python3
"""
The directory of Churches.

Builds data/directory.v1.json from the table below. The table is the
sourced record: every row carries the address it was read from and the day
it was read, and both are shown to the reader on the page.

The rule the table obeys is written in docs/DIRECTORY.md and is not
restated here, except for the one line that governs every edit to this
file: a body appears because an autocephalous Church lists it among its
own, and where Churches differ the row says who lists it rather than which
is right.

    python3 tools/directory.py --check
    python3 tools/directory.py --write
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory.v1.json"

# The day the spine was read. Every row below was confirmed on it.
READ = "2026-09-13"

# The two lists the rows were read from. A row names whichever it came
# from, so a reader can see for himself.
OCA_LIST = "https://www.oca.org/directories/world-churches"

# ---------------------------------------------------------------- the rows
#
# `name` is as the source prints it in its list, so the twenty rows read
# from one list read alike. `styled` is the body's own English designation
# where its own site was read here, and `local` its own language. Four
# sites refused the request from here - Serbia, Cyprus, the Czech Lands and
# Macedonia - so those rows carry the list as their source and say so.
#
# No telephone numbers. They are the field that goes stale invisibly, and
# the ones on the list read here already carried a Moscow dialling code
# retired in the 1990s. A website that answers is a better address than a
# number that does not, and the numbers come back per row when each body's
# own site has been read.

CHURCHES = [
 dict(id="constantinople", order=1, kind="church",
      name="The Church of Constantinople",
      styled="Ecumenical Patriarchate",
      local="Οικουμενικό Πατριαρχείο",
      seat="Istanbul", country="TR",
      address="Rum Patrikliği, Dr. Sadık Ahmet Cad. No. 19, 34083 Fatih-İstanbul",
      site="https://ec-patr.org/", source="https://ec-patr.org/"),

 dict(id="alexandria", order=2, kind="church",
      name="The Church of Alexandria",
      styled="Patriarchate of Alexandria",
      local="Πατριαρχείο Αλεξανδρείας",
      seat="Alexandria", country="EG",
      address="PO Box 2006, Alexandria",
      site="https://www.patriarchateofalexandria.com/",
      source="https://www.patriarchateofalexandria.com/"),

 dict(id="antioch", order=3, kind="church",
      name="The Church of Antioch",
      styled="Greek Orthodox Patriarchate of Antioch and All the East",
      seat="Damascus", country="SY",
      address="BP 0009, Damascus",
      site="https://antiochpatriarchate.org/",
      source="https://antiochpatriarchate.org/"),

 dict(id="jerusalem", order=4, kind="church",
      name="The Church of Jerusalem",
      styled="Greek Orthodox Patriarchate of Jerusalem",
      seat="Jerusalem", country="IL",
      address="P.O. Box 19632, 91190 Jerusalem",
      site="https://jerusalem-patriarchate.info/",
      source="https://jerusalem-patriarchate.info/"),

 dict(id="russia", order=5, kind="church",
      name="The Church of Russia",
      styled="Russian Orthodox Church",
      local="Русская Православная Церковь",
      seat="Moscow", country="RU",
      address="5 Chisty Pereulok, Moscow 119034",
      site="https://patriarchia.ru/", source="https://patriarchia.ru/"),

 dict(id="georgia", order=6, kind="church",
      name="The Church of Georgia",
      seat="Tbilisi", country="GE",
      address="King Erekle II Square 1, Tbilisi 0105",
      site="https://patriarchate.ge/", source=OCA_LIST),

 dict(id="serbia", order=7, kind="church",
      name="The Church of Serbia",
      styled="Serbian Orthodox Church",
      seat="Belgrade", country="RS",
      address="Kralja Petra 5, 11000 Belgrade",
      site="https://spc.rs/", source=OCA_LIST),

 dict(id="romania", order=8, kind="church",
      name="The Church of Romania",
      styled="Romanian Orthodox Church",
      local="Biserica Ortodoxă Română",
      seat="Bucharest", country="RO",
      address="Aleea Patriarhiei 2, Bucharest",
      site="https://patriarhia.ro/", source="https://patriarhia.ro/"),

 dict(id="bulgaria", order=9, kind="church",
      name="The Church of Bulgaria",
      styled="Bulgarian Orthodox Church - Bulgarian Patriarchate",
      local="Българска Православна Църква - Българска Патриаршия",
      seat="Sofia", country="BG",
      address="Oborishte 4, 1000 Sofia",
      site="https://bg-patriarshia.bg/", source="https://bg-patriarshia.bg/"),

 dict(id="cyprus", order=10, kind="church",
      name="The Church of Cyprus",
      seat="Nicosia", country="CY",
      address="PO Box 1130, Nicosia 1016",
      site="https://churchofcyprus.org.cy/", source=OCA_LIST),

 dict(id="greece", order=11, kind="church",
      name="The Church of Greece",
      local="Η Εκκλησία της Ελλάδος",
      seat="Athens", country="GR",
      address="Ag. Philotheis 21, 10556 Athens",
      site="https://ecclesiagreece.gr/", source=OCA_LIST),

 dict(id="albania", order=12, kind="church",
      name="The Church of Albania",
      local="Kisha Orthodhokse Autoqefale e Shqipërisë",
      seat="Tirana", country="AL",
      address="Rruga e Kavajës 151, Tirana",
      site="https://orthodoxalbania.org/",
      source="https://orthodoxalbania.org/"),

 dict(id="poland", order=13, kind="church",
      name="The Church of Poland",
      local="Polski Autokefaliczny Kościół Prawosławny",
      seat="Warsaw", country="PL",
      address="Al. Solidarności 52, 03-402 Warszawa",
      site="https://www.orthodox.pl/", source="https://www.orthodox.pl/"),

 dict(id="czech-slovakia", order=14, kind="church",
      name="The Church of the Czech Lands and Slovakia",
      seat="Prešov", country="SK",
      address="Bayerova 8, 08001 Prešov",
      site="https://orthodox.sk/", source=OCA_LIST),

 dict(id="oca", order=15, kind="church",
      name="The Orthodox Church in America",
      seat="Syosset, New York", country="US",
      address="PO Box 675, Syosset, NY 11791-0675",
      site="https://www.oca.org/", source="https://www.oca.org/",
      standing="Autocephaly was granted by the Church of Russia on 10 April 1970.",
      standing_source="https://www.oca.org/history-archives/tomos-of-autocephaly"),

 dict(id="macedonia", order=16, kind="church",
      name="The Macedonian Orthodox Church - Ohrid Archbishopric",
      local="Македонска православна црква - Охридска архиепископија",
      seat="Skopje", country="MK",
      address="Партизански одреди 12, 1000 Скопје",
      site="http://www.mpc.org.mk/English/default.asp", source=OCA_LIST),

 dict(id="ukraine-uoc", order=17, kind="church",
      name="The Church of Ukraine",
      styled="Ukrainian Orthodox Church",
      seat="Kyiv", country="UA",
      address="Sichnevoho Povstannia 25, korp. 49, 01015 Kyiv",
      site="https://church.ua/", source=OCA_LIST,
      listed=["The Orthodox Church in America"],
      listed_source=OCA_LIST),

 dict(id="ukraine-ocu", order=18, kind="church",
      name="Orthodox Church of Ukraine",
      local="Православна Церква України",
      seat="Kyiv", country="UA",
      address="Triokhsviatytelska 8, 01001 Kyiv",
      site="https://www.pomisna.info/",
      source="https://www.pomisna.info/",
      listed=["The Ecumenical Patriarchate"],
      listed_source="https://ec-patr.org/en/patriarchal-and-synodal-tomos-for-the-bestowal-of-the-ecclesiastical-status-of-autocephaly-to-the-orthodox-church-in-ukraine/",
      standing="The Ecumenical Patriarchate bestowed autocephaly by Patriarchal and Synodal Tomos in January 2019.",
      standing_source="https://ec-patr.org/en/patriarchal-and-synodal-tomos-for-the-bestowal-of-the-ecclesiastical-status-of-autocephaly-to-the-orthodox-church-in-ukraine/"),

 dict(id="sinai", order=19, kind="autonomous",
      name="The Church of Sinai",
      seat="Mount Sinai", country="EG",
      address="Monastery of Saint Catherine at Mount Sinai, c/o Midan el-Daher, 11271 Cairo",
      site="https://www.sinaimonastery.com/index.php/en/",
      source="https://www.sinaimonastery.com/index.php/en/"),

 dict(id="finland", order=20, kind="autonomous",
      name="The Autonomous Church of Finland",
      seat="Helsinki", country="FI",
      address="Liisankatu 29 A, 00170 Helsinki",
      site="https://ort.fi/", source="https://ort.fi/"),

 dict(id="japan", order=21, kind="autonomous",
      name="The Church of Japan",
      seat="Tokyo", country="JP",
      address="Nicholai-do, 1-4 Surugadai, Kanda, Chiyoda-ku, Tokyo 101",
      site="https://www.orthodoxjapan.jp/",
      source="https://www.orthodoxjapan.jp/"),

 dict(id="estonia-eaok", order=22, kind="autonomous",
      name="Orthodox Church of Estonia",
      local="Eesti Apostlik-Õigeusu Kirik",
      seat="Tallinn", country="EE",
      site="https://www.eoc.ee/", source="https://www.eoc.ee/",
      listed=["The Ecumenical Patriarchate"],
      listed_source="https://ec-patr.org/en/eparchies-of-the-throne/autonomous-churches/"),
]

# The countries a row can name, written out so the page has a word to show
# and a key to filter on. English here; the page carries the rest.
COUNTRIES = {
    "AL": "Albania", "BG": "Bulgaria", "CY": "Cyprus", "EE": "Estonia",
    "EG": "Egypt", "FI": "Finland", "GE": "Georgia", "GR": "Greece",
    "IL": "Israel", "JP": "Japan", "MK": "North Macedonia", "PL": "Poland",
    "RO": "Romania", "RS": "Serbia", "RU": "Russia", "SK": "Slovakia",
    "SY": "Syria", "TR": "Turkey", "UA": "Ukraine", "US": "United States",
}


def build():
    rows = []
    for c in sorted(CHURCHES, key=lambda r: r["order"]):
        r = {k: v for k, v in c.items() if v not in (None, "", [])}
        r["checked"] = READ
        rows.append(r)
    seen = set()
    for r in rows:
        if r["id"] in seen:
            raise SystemExit("duplicate id: " + r["id"])
        seen.add(r["id"])
        if r["country"] not in COUNTRIES:
            raise SystemExit("no country name for " + r["country"])
        for f in ("name", "seat", "country", "site", "source"):
            if not r.get(f):
                raise SystemExit("%s: missing %s" % (r["id"], f))
    return {"v": 1, "read": READ, "countries": COUNTRIES, "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    d = build()
    text = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    if a.write:
        OUT.write_text(text, encoding="utf-8")
        print("wrote %s  (%d rows, %d countries, %d KB)"
              % (OUT.relative_to(ROOT), len(d["rows"]), len(d["countries"]),
                 len(text.encode("utf-8")) // 1024 or 1))
        return 0
    have = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if have != text:
        print("data/directory.v1.json is out of date", file=sys.stderr)
        return 1
    print("%d rows, %d countries, all sourced and dated"
          % (len(d["rows"]), len(d["countries"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
