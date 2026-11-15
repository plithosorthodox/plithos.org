#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Nigeria.

The Holy Archdiocese of Nigeria publishes a current clergy and communities
roster. The Moscow Patriarchate's African Exarchate publishes a current
Nigeria deanery count and current reports naming some of its parishes. Exact
named current bodies are emitted. Aggregate-only, unnamed, historical, and
reception-pending communities remain in the companion candidate ledger.

    python tools/directory_nigeria.py --check
    python tools/directory_nigeria.py --dump
"""

import argparse
import json
import re
import sys
from pathlib import Path


CHECKED = "2026-11-15"
ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_LEDGER = ROOT / "tools" / "directory_candidates" / "nigeria.json"

AX_COMMUNITIES = (
    "https://orthodoxchurchnigeria.org/"
    "the-orthodox-archdiocese-of-nigeria-overview/clergy-communities/"
)
AX_CURRENT = (
    "https://www.patriarchateofalexandria.com/archdioceses/"
    "holy-archdiocese-of-nigeria/?lang=en"
)
RU_ROSTER = (
    "https://exarchate-africa.ru/en/dioceses_cat/"
    "diocese-of-north-africa/"
)
RU_TRIP = (
    "https://exarchate-africa.ru/en/news/"
    "priest-george-maximov-traveled-to-nigeria/"
)
RU_WELLS = (
    "https://exarchate-africa.ru/novosti/"
    "probureny-shest-novyh-skvazhin-na-prihodah-patriarshego-"
    "ekzarhata-afriki-v-nigerii/"
)
RU_SOUTHEAST = (
    "https://exarchate-africa.ru/novosti/"
    "blagochinnyj-prihodov-v-nigerii-posetil-prihody-na-yugo-"
    "vostoke-strany/"
)
RU_LUKE = (
    "https://exarchate-africa.ru/novosti/"
    "eshhe-odin-svyashhennik-prinyat-v-russkuyu-pravoslavnuyu-"
    "czerkov-v-nigerii/"
)
RU_CLERGY = (
    "https://exarchate-africa.ru/novosti/"
    "v-nigerii-proshlo-obshhee-sobranie-duhovenstva/"
)


def ax(row_id, name, seat, rank="Parish", kind="parish"):
    return dict(
        id=row_id,
        parent="ax-nigeria",
        kind=kind,
        rank=rank,
        name=name,
        local=name,
        seat=seat,
        country="NG",
        sources=[AX_COMMUNITIES, AX_CURRENT],
    )


AX_ROWS = [
    ax("ng-ax-abuja-barnabas", "Community of Saint Barnabas the Apostle in Abuja", "Abuja", "Community"),
    ax("ng-ax-lagos-resurrection-cathedral", "Cathedral of the Resurrection of the Lord in Lagos", "Lagos", "Cathedral"),
    ax("ng-ax-lagos-anthony-chapel", "Chapel of Saint Anthony in Ebute Metta", "Ebute Metta", "Chapel"),
    ax("ng-ax-nanka-dormition", "Parish of the Dormition of the Virgin Mary in Nanka", "Nanka"),
    ax("ng-ax-agbilagba-moses-ethiopian", "Mission Station of Saint Moses the Ethiopian in Agbilagba", "Agbilagba", "Mission Station"),
    ax("ng-ax-umudala-catherine", "Mission Station of Saint Catherine in Umudala", "Umudala", "Mission Station"),
    ax("ng-ax-ifite-john-chrysostom", "Mission Station of Saint John Chrysostom in Ifite", "Ifite", "Mission Station"),
    ax("ng-ax-ubahu-nectarios", "Mission Station of Saint Nectarios in Ubahu", "Ubahu", "Mission Station"),
    ax("ng-ax-etti-basil-great", "Mission Station of Saint Basil the Great in Etti", "Etti", "Mission Station"),
    ax("ng-ax-neni-archangels", "Parish of the Archangels in Neni", "Neni"),
    ax("ng-ax-ukpor-ignatius", "Parish of Saint Ignatius the God-bearer in Ukpor", "Ukpor"),
    ax("ng-ax-uga-gregory-theologian", "Parish of Saint Gregory the Theologian in Uga", "Uga"),
    ax("ng-ax-umudioka-virgin-mary-grace", "Parish of the Virgin Mary Full of Grace in Umudioka", "Umudioka"),
    ax("ng-ax-enugu-agidi-nicholas", "Parish of Saint Nicholas in Enugu-Agidi", "Enugu-Agidi"),
    ax("ng-ax-nzagha-ukpor-holy-cross", "Parish of the Holy Cross in Nzagha-Ukpor", "Nzagha-Ukpor"),
    ax("ng-ax-ihiala-peter-paul", "Parish of Saints Peter and Paul in Ihiala", "Ihiala"),
    ax("ng-ax-uli-michael", "Parish of Saint Michael in Uli", "Uli"),
    ax("ng-ax-lilu-transfiguration", "Parish of the Transfiguration of the Lord in Lilu", "Lilu"),
    ax("ng-ax-onitsha-mark", "Parish of Saint Mark in Onitsha", "Onitsha"),
    ax("ng-ax-yamto-mbagba-stephen", "Parish of Saint Stephen in Yamto, Mbagba", "Yamto, Mbagba"),
    ax("ng-ax-dzer-andrew", "Church of Saint Andrew in Dzer", "Dzer", "Church"),
    ax("ng-ax-gboko-nectarios", "Parish of Saint Nectarios in Gboko", "Gboko"),
    ax("ng-ax-mbaagwa-ande-paul", "Church of Saint Paul in Mbaagwa, Ande", "Mbaagwa, Ande", "Church"),
    ax("ng-ax-ugba-moses-ethiopian", "Church of Saint Moses the Ethiopian in Ugba", "Ugba", "Church"),
    ax("ng-ax-mbakua-euphemia", "Parish of Saint Euphemia in Mbakua", "Mbakua"),
    ax("ng-ax-tsedaa-ugba-james", "Parish of Saint James in TseDaa, Ugba", "TseDaa, Ugba"),
    ax("ng-ax-nor-mbayegh-holy-cross", "Parish of the Holy Cross in Nor, Mbayegh", "Nor, Mbayegh"),
    ax("ng-ax-atee-ikov-thomas", "Parish of Saint Thomas in Atee-Ikov", "Atee-Ikov"),
    ax("ng-ax-nyev-michael", "Parish of Saint Michael in Nyev", "Nyev"),
    ax("ng-ax-mbaagasema-tsekucha-catherine", "Parish of Saint Catherine in Mbaagasema, Tsekucha", "Mbaagasema, Tsekucha"),
    ax("ng-ax-ada-mkovur-transfiguration", "Parish of the Transfiguration of the Lord in Ada, Mkovur", "Ada, Mkovur"),
    ax("ng-ax-mbakyura-buruku-annunciation", "Parish of the Annunciation of the Virgin Mary in Mbakyura, Buruku", "Mbakyura, Buruku"),
    ax("ng-ax-usaka-anthony", "Parish of Saint Anthony in Usaka", "Usaka"),
    ax("ng-ax-awo-idemili-christopher", "Parish of Saint Christopher in Awo-Idemili", "Awo-Idemili"),
    ax("ng-ax-okwuamaraihe-annunciation", "Mission Station of the Annunciation of the Virgin Mary in Okwuamaraihe", "Okwuamaraihe", "Mission Station"),
    ax("ng-ax-ohukabia-philip", "Mission Station of Saint Philip in Ohukabia", "Ohukabia", "Mission Station"),
    ax("ng-ax-ede-ukwu-john-baptist", "Mission Station of Saint John the Baptist in Ede Ukwu", "Ede Ukwu", "Mission Station"),
    ax("ng-ax-isieke-edenta-andrew", "Mission Station of Saint Andrew the Apostle in Isieke-Edenta", "Isieke-Edenta", "Mission Station"),
    ax("ng-ax-amaimo-moses", "Mission Station of Saint Moses in Amaimo", "Amaimo", "Mission Station"),
    ax("ng-ax-ahaba-irene", "Mission Station of Saint Irene in Ahaba", "Ahaba", "Mission Station"),
    ax("ng-ax-amaokwe-athanasius-cyril", "Mission Station of Saints Athanasius and Cyril in Amaokwe", "Amaokwe", "Mission Station"),
    ax("ng-ax-ubahaezedeke-holy-cross", "Mission Station of the Holy Cross in Ubahaezedeke", "Ubahaezedeke", "Mission Station"),
    ax("ng-ax-umuhu-okabia-nativity", "Parish of the Nativity of the Lord in Umuhu-Okabia", "Umuhu-Okabia"),
    ax("ng-ax-akokwa-anthony", "Parish of Saint Anthony in Akokwa", "Akokwa"),
    ax("ng-ax-ihetenansa-george", "Parish of Saint George in Ihetenansa", "Ihetenansa"),
    ax("ng-ax-oyede-paul", "Parish of Saint Paul in Oyede", "Oyede"),
    ax("ng-ax-aviara-gregory-theologian", "Parish of Saint Gregory the Theologian in Aviara", "Aviara"),
    ax("ng-ax-ukpude-mark", "Parish of Saint Mark in Ukpude", "Ukpude"),
    ax("ng-ax-ewokpaka-catherine", "Parish of Saint Catherine in Ewokpaka", "Ewokpaka"),
    ax("ng-ax-ibedeni-michael", "Parish of Saint Michael in Ibedeni", "Ibedeni"),
    ax("ng-ax-olomoro-john", "Parish of Saint John in Olomoro", "Olomoro"),
    ax("ng-ax-ivrogbo-george", "Parish of Saint George in Ivrogbo", "Ivrogbo"),
    ax("ng-ax-benin-city-luke", "Parish of Saint Luke the Evangelist in Benin City", "Benin City"),
    ax("ng-ax-iselue-ewohimi-basil", "Parish of Saint Basil the Great in Iselue-Ewohimi", "Iselue-Ewohimi"),
    ax("ng-ax-afashio-uzaroe-annunciation", "Parish of the Annunciation of the Virgin Mary in Afashio-Uzaroe", "Afashio-Uzaroe"),
    ax("ng-ax-port-harcourt-irene", "Community of Saint Irene in Port Harcourt", "Port Harcourt", "Community"),
]


def ru(row_id, name, local, seat, sources):
    return dict(
        id=row_id,
        parent="ru-north-africa",
        kind="parish",
        rank="Parish",
        name=name,
        local=local,
        seat=seat,
        country="NG",
        sources=sources,
    )


RU_ROWS = [
    dict(
        id="ng-ru-national-deanery",
        parent="ru-north-africa",
        kind="diocese",
        rank="Deanery",
        name="Deanery of the Federal Republic of Nigeria",
        local="Благочиние Федеративной Республики Нигерия",
        country="NG",
        sources=[RU_ROSTER, RU_TRIP],
    ),
    ru("ng-ru-abuja-holy-trinity", "Parish of the Life-Giving Trinity in Abuja", "Свято-Троицкий приход в Абудже", "Abuja", [RU_ROSTER, RU_TRIP]),
    ru("ng-ru-ukpor-matrona", "Parish of Blessed Matrona of Moscow in Ukpor", "Приход блаженной Матроны Московской в Укпоре", "Ukpor", [RU_TRIP]),
    ru("ng-ru-ogbunike-catherine", "Parish of the Great Martyr Catherine in Ogbunike", "Приход великомученицы Екатерины в с. Огбунике", "Ogbunike", [RU_WELLS, RU_TRIP]),
    ru("ng-ru-onicha-peter", "Parish of the Apostle Peter in Onicha", "Приход апостола Петра в Ониче", "Onicha", [RU_TRIP]),
    ru("ng-ru-ugbaikyo-george", "Parish of the Great Martyr George the Victory-Bearer in Ugbaikyo", "Приход великомученика Георгия Победоносца в г. Угбайкьо", "Ugbaikyo", [RU_WELLS, RU_SOUTHEAST, RU_TRIP]),
    ru("ng-ru-adikpo-james", "Parish of the Apostle James in Adikpo", "Приход апостола Иакова в Адикпо", "Adikpo", [RU_TRIP]),
    ru("ng-ru-atee-joseph", "Parish of Saint Joseph in Atee", "Приход святого Иосифа в с. Ати", "Atee", [RU_WELLS, RU_TRIP]),
    ru("ng-ru-mbaakir-seraphim", "Parish of Saint Seraphim of Sarov in Mbaakir", "Приход преподобного Серафима Саровского в с. Мбаакир", "Mbaakir", [RU_WELLS, RU_SOUTHEAST]),
    ru("ng-ru-benin-city-luke", "Parish of the Apostle Luke in Benin City", "Приход апостола Луки в г. Бенин-Сити", "Benin City", [RU_LUKE]),
    ru("ng-ru-akokwa-leonidas", "Parish of the Martyr Leonidas of Egypt in Akokwa", "Приход мученика Леонида Египетского в с. Акоква", "Akokwa", [RU_CLERGY]),
]

ROWS = {"ax-nigeria": AX_ROWS, "ru-north-africa": RU_ROWS}
EXPECTED = {"ax-nigeria": 56, "ru-north-africa": 11}
ENGLISH_NAMES = {row["id"]: row["name"] for rows in ROWS.values() for row in rows}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in ROWS.values()
    for row in rows
    if row.get("seat")
}


def clean(source):
    row = {key: value for key, value in source.items() if value not in (None, "", [])}
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
        raise ValueError("%s carries forbidden punctuation or encoding" % row.get("id"))
    return row


def build():
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"diocese", "parish"}
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
            if row.get("country") != "NG":
                raise ValueError("%s is outside Nigeria" % row_id)
            if row.get("kind") not in allowed_kinds:
                raise ValueError("%s has an unsupported kind" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            seen.add(row_id)
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" % (parent, EXPECTED[parent]))
        payloads[parent] = {"v": 1, "parent": parent, "country": "NG", "rows": rows}
    if set(ENGLISH_NAMES) != seen - set(ROWS):
        raise ValueError("Nigeria English name map is out of sync")
    return payloads


def validate_candidate_ledger():
    ledger = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
    if ledger.get("v") != 1 or ledger.get("country") != "NG":
        raise ValueError("Nigeria candidate ledger has the wrong schema")
    if ledger.get("checked") != CHECKED:
        raise ValueError("Nigeria candidate ledger check date is out of sync")
    summary = ledger.get("published_summary") or {}
    if summary.get("total") != sum(EXPECTED.values()):
        raise ValueError("Nigeria candidate ledger total is out of sync")
    for parent, count in EXPECTED.items():
        if summary.get(parent) != count:
            raise ValueError("Nigeria ledger count is out of sync for %s" % parent)
    for key in ("candidates", "source_reconciliations", "official_jurisdiction_audit"):
        if not isinstance(ledger.get(key), list) or not ledger[key]:
            raise ValueError("Nigeria candidate ledger lacks %s" % key)
        for item in ledger[key]:
            sources = item.get("sources") or []
            if not sources or len(sources) > 3:
                raise ValueError("Nigeria ledger item has invalid sources")
            if not all(str(url).startswith("https://") for url in sources):
                raise ValueError("Nigeria ledger item has a non-HTTPS source")
    rendered = json.dumps(ledger, ensure_ascii=False)
    if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
        raise ValueError("Nigeria candidate ledger has forbidden punctuation")
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
        print("directory Nigeria: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("Nigeria: 67 current named bodies across 2 overlapping jurisdictions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
