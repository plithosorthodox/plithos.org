#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Madagascar.

The Patriarchate of Alexandria and the Moscow Patriarchate's African
Exarchate both publish current structures in Madagascar. Only exact named
bodies supported by competent first-party Church records are emitted here.
Aggregate-only, unnamed, construction-only, and historically unresolved
identities remain in the companion candidate ledger.

    python tools/directory_madagascar.py --check
    python tools/directory_madagascar.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = (
    ROOT / "tools" / "directory_candidates" / "madagascar.json"
)

AX_ANTANANARIVO = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-antananarivo-and-north-madagascar/?lang=en"
)
AX_ENTRANCE_EN = (
    "https://www.patriarchateofalexandria.com/"
    "oloklirothike-i-poimantiki-episkepsi-tis-a-th-m-stin-madagaskari/"
    "?lang=en&print=print"
)
AX_ENTRANCE_EL = (
    "https://www.patriarchateofalexandria.com/"
    "oloklirothike-i-poimantiki-episkepsi-tis-a-th-m-stin-madagaskari/"
)
AX_TOLIARA = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-diocese-of-toliara-and-southern-madagascar/?lang=en"
)
AX_SAINT_ANDREW_EN = (
    "https://www.patriarchateofalexandria.com/"
    "patriarchal-pastoral-visit-to-the-holy-diocese-of-toliara-and-"
    "southern-madagascar/?lang=en"
)
AX_SAINT_ANDREW_EL = (
    "https://www.patriarchateofalexandria.com/"
    "patriarchiki-poimantiki-episkepsi-stin-iera-episkopi-toliaras-"
    "kai-notioy-madagaskaris/"
)

RU_ROSTER = (
    "https://exarchate-africa.ru/en/dioceses_cat/"
    "south-african-diocese/"
)
RU_NECTARIOS = "https://mospat.ru/en/news/92436/"
RU_AMPARAKY = (
    "https://exarchate-africa.ru/novosti/"
    "na-preobrazhenskom-prihode-na-madagaskare-soversheno-tainstvo-"
    "kreshheniya/"
)
RU_ARCHANGEL = (
    "https://exarchate-africa.ru/novosti/"
    "na-mihailo-arhangelskom-prihode-v-stolicze-madagaskara-otmetili-"
    "prazdnik-svetlogo-hristova-voskreseniya/"
)
RU_MARK = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihode-apostola-marka-na-madagaskare-sostoyalos-otkrytie-"
    "shvejnoj-shkoly/"
)
RU_NATIVITY = (
    "https://exarchate-africa.ru/novosti/"
    "patriarshij-ekzarh-afriki-sovershil-liturgiyu-na-prihode-"
    "rozhdestva-presvyatoj-bogorodiczy-na-madagaskare/"
)
RU_MATRONA = (
    "https://exarchate-africa.ru/novosti/"
    "v-preddverii-novogo-uchebnogo-goda-okazana-pomoshh-shkolnikam-"
    "na-prihode-blazhennoj-matrony-na-yuge-madagaskara/"
)
RU_LEONIDAS = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihode-muchenika-leonid-na-yugo-zapade-madagaskara-postroen-"
    "vodonakopitel/"
)
RU_ANTSIRABE = (
    "https://exarchate-africa.ru/novosti/"
    "v-prazdnik-rozhdestva-hristova-sostoyalis-bogosluzheniya-na-"
    "madagaskare/"
)
RU_BELAMBO_BARBARA = (
    "https://exarchate-africa.ru/novosti/"
    "okazana-gumanitarnaya-pomoshh-pravoslavnym-veruyushhim-v-"
    "yuzhnom-blagochinii-madagaskara/"
)
RU_PETER_PAUL = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihode-svyatyh-apostolov-petra-i-pavla-na-madagaskare-"
    "kreshheny-tri-cheloveka/"
)
RU_CRESCENS = (
    "https://exarchate-africa.ru/novosti/"
    "na-prihode-svyatogo-kriskenta-na-madagaskare-kreshheny-shestero-"
    "detej/"
)
RU_MEETING = (
    "https://exarchate-africa.ru/novosti/"
    "20-chelovek-prisoedinilis-k-czerkvi-hristovoj-na-madagaskare/"
)
RU_TRINITY = (
    "https://exarchate-africa.ru/novosti/"
    "russkaya-pravoslavnaya-czerkov-peredala-pomoshh-zhitelyam-"
    "madagaskara-postradavshim-v-rezultate-cziklona-gezani/"
)
RU_AMBONDROMAMY = (
    "https://exarchate-africa.ru/novosti/"
    "veruyushhie-v-severnom-blagochinii-madagaskara-vstretili-"
    "hristovo-rozhdestvo/"
)
RU_ANNUNCIATION = (
    "https://exarchate-africa.ru/novosti/"
    "v-yuzhnom-blagochinii-madagaskara-kreshheny-18-mestnyh-zhitelej/"
)


def parish(row_id, name, local, seat, sources, rank="Parish"):
    return {
        "id": row_id,
        "parent": "ru-south-africa",
        "kind": "parish",
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "MG",
        "sources": sources,
    }


ROWS = {
    "ax-antananarivo": [
        {
            "id": "mg-ax-antananarivo-entrance-theotokos",
            "parent": "ax-antananarivo",
            "kind": "parish",
            "rank": "Metropolitan Church",
            "name": (
                "Metropolitan Church of the Entrance of the Theotokos "
                "in Antananarivo"
            ),
            "local": "Μητροπολιτικός Ναός των Εισοδίων της Θεοτόκου",
            "seat": "Antananarivo",
            "country": "MG",
            "sources": [AX_ENTRANCE_EN, AX_ENTRANCE_EL, AX_ANTANANARIVO],
        },
    ],
    "ax-toliara": [
        {
            "id": "mg-ax-toliara-saint-andrew",
            "parent": "ax-toliara",
            "kind": "parish",
            "rank": "Church",
            "name": "Holy Church of Saint Andrew in Toliara",
            "local": "Ιερός Ναός του Αγίου Ανδρέα",
            "seat": "Toliara",
            "country": "MG",
            "sources": [AX_SAINT_ANDREW_EN, AX_SAINT_ANDREW_EL, AX_TOLIARA],
        },
    ],
    "ru-south-africa": [
        parish(
            "mg-ru-mahajanga-nectarios-aegina",
            "Parish of Saint Nectarios of Aegina in Mahajanga",
            "Приход святителя Нектария Эгинского в г. Махадзанга",
            "Mahajanga",
            [RU_ROSTER, RU_NECTARIOS],
        ),
        parish(
            "mg-ru-morahita-nicholas",
            "Parish of Saint Nicholas the Wonderworker in Morahita",
            "Приход святителя Николая Чудотворца в с. Мурахита",
            "Morahita",
            [RU_ROSTER],
        ),
        parish(
            "mg-ru-amparaky-transfiguration",
            "Parish of the Transfiguration of the Lord in Amparaky",
            "Приход Преображения Господня в с. Ампараки",
            "Amparaky",
            [RU_AMPARAKY, RU_ROSTER],
        ),
        parish(
            "mg-ru-antananarivo-archangel-michael",
            "Parish of the Archangel Michael in Antananarivo",
            "Приход Архистратига Божия Михаила в г. Антананариву",
            "Antananarivo",
            [RU_ARCHANGEL, RU_ROSTER],
        ),
        parish(
            "mg-ru-ambatondrazaka-apostle-mark",
            "Parish of the Apostle Mark in Ambatondrazaka",
            "Приход апостола Марка в с. Амбатундразака",
            "Ambatondrazaka",
            [RU_MARK, RU_NATIVITY],
        ),
        parish(
            "mg-ru-ambatondrazaka-nativity-theotokos",
            "Parish of the Nativity of the Most Holy Theotokos in Ambatondrazaka",
            "Приход Рождества Пресвятой Богородицы в г. Амбатундразака",
            "Ambatondrazaka",
            [RU_NATIVITY, RU_ROSTER],
        ),
        parish(
            "mg-ru-tanjombato-matrona-moscow",
            "Parish of Blessed Matrona of Moscow in Tanjombato",
            "Приход блаженной Матроны Московской в Тандзомбату",
            "Tanjombato",
            [RU_MATRONA, RU_ANTSIRABE],
        ),
        parish(
            "mg-ru-andamoti-leonidas-alexandria",
            "Parish of the Martyr Leonidas of Alexandria in Andamoti",
            "Приход мученика Леонида Александрийского в с. Андамути",
            "Andamoti",
            [RU_LEONIDAS, RU_ROSTER],
        ),
        parish(
            "mg-ru-antsirabe-nicholas",
            "Parish of Saint Nicholas the Wonderworker in Antsirabe",
            "Приход святителя Николая Чудотворца в г. Анцирабе",
            "Antsirabe",
            [RU_ANTSIRABE, RU_ROSTER],
        ),
        parish(
            "mg-ru-belambo-nicholas",
            "Parish of Saint Nicholas the Wonderworker in Belambo",
            "Приход святителя Николая Чудотворца в г. Беламбо",
            "Belambo",
            [RU_BELAMBO_BARBARA, RU_ROSTER],
        ),
        parish(
            "mg-ru-andapa-peter-paul",
            "Parish of the Holy Chief Apostles Peter and Paul in Andapa",
            "Приход первоверховных апостолов Петра и Павла в с. Андапа",
            "Andapa",
            [RU_PETER_PAUL, RU_ROSTER],
        ),
        parish(
            "mg-ru-sambava-crescens",
            "Parish of the Martyr Crescens in Sambava",
            "Приход мученика Крискента в с. Самбава",
            "Sambava",
            [RU_CRESCENS, RU_ROSTER],
        ),
        parish(
            "mg-ru-morondava-meeting-lord",
            "Community of the Meeting of the Lord near Morondava",
            "Община Сретения Господня в окрестностях г. Мурундава",
            "Morondava",
            [RU_MEETING, RU_ROSTER],
            "Community",
        ),
        parish(
            "mg-ru-toamasina-holy-trinity",
            "Parish of the Holy Trinity in Toamasina",
            "Приход Святой Троицы в Туамасине",
            "Toamasina",
            [RU_TRINITY, RU_AMBONDROMAMY],
        ),
        parish(
            "mg-ru-ambondromamy-nicholas",
            "Parish of Saint Nicholas the Wonderworker in Ambondromamy",
            "Приход святителя Николая Чудотворца в с. Амбундрумами",
            "Ambondromamy",
            [RU_AMBONDROMAMY, RU_ROSTER],
        ),
        parish(
            "mg-ru-ankizandava-annunciation",
            "Parish of the Annunciation of the Most Holy Theotokos in Ankizandava",
            "Приход Благовещения Пресвятой Богородицы в с. Анкидзандава",
            "Ankizandava",
            [RU_ANNUNCIATION, RU_ROSTER],
        ),
        parish(
            "mg-ru-tanamilihitse-barbara",
            "Parish of the Great Martyr Barbara in Tanamilihitse",
            "Приход великомученицы Варвары в с. Танамилихице",
            "Tanamilihitse",
            [RU_BELAMBO_BARBARA, RU_ROSTER],
        ),
    ],
}

EXPECTED = {
    "ax-antananarivo": 1,
    "ax-toliara": 1,
    "ru-south-africa": 17,
}
ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in ROWS.values()
    for row in rows
    if row.get("seat")
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
            if row.get("country") != "MG":
                raise ValueError("%s is outside Madagascar" % row_id)
            if row.get("kind") != "parish":
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "MG",
            "rows": rows,
        }
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Madagascar English name map is out of sync")
    if sum(len(payload["rows"]) for payload in payloads.values()) != 19:
        raise ValueError("Madagascar must publish exactly 19 rows")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "MG":
        raise ValueError(
            "Madagascar candidate ledger has the wrong schema or country"
        )
    if ledger.get("checked") != CHECKED:
        raise ValueError("Madagascar candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if (
            summary.get("ax-antananarivo") != 1 or
            summary.get("ax-toliara") != 1 or
            summary.get("ru-south-africa") != 17 or
            summary.get("russian_roster_total") != 30 or
            summary.get("russian_aggregate_only_remainder") != 13 or
            summary.get("total") != 19):
        raise ValueError("Madagascar candidate ledger totals are out of sync")
    required_lists = ("candidates", "official_jurisdiction_audit")
    for key in required_lists:
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Madagascar candidate ledger lacks %s" % key)
    candidate_ids = []
    for item in ledger["candidates"]:
        candidate_id = item.get("candidate_id")
        if not candidate_id or not re.fullmatch(r"[a-z0-9-]+", candidate_id):
            raise ValueError("candidate ledger carries an invalid id")
        if item.get("country") != "MG":
            raise ValueError("%s is outside Madagascar" % candidate_id)
        candidate_ids.append(candidate_id)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Madagascar candidate ledger has duplicate ids")
    for section in required_lists:
        for item in ledger[section]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError(
                    "Madagascar ledger item must cite one to three sources"
                )
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError(
                    "Madagascar ledger item carries a non-HTTPS source"
                )
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Madagascar candidate ledger has forbidden punctuation")
    return ledger


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        validate_candidate_ledger()
    except (OSError, ValueError) as exc:
        print("directory Madagascar: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    else:
        print(
            "Madagascar: 19 current officially named bodies across "
            "3 jurisdictional parents"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
