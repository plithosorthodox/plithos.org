#!/usr/bin/env python3
"""The parish-scale Korea and Japan exarchate branches of the directory.

The Ecumenical Patriarchate's Metropolis of Korea and the Moscow
Patriarchate's Diocese of Korea each publish a current directory of their
South Korea churches. The ROCOR directory also publishes two Korean bodies
under its Diocese of Australia and New Zealand. Monasteries are taken from
the Metropolis's own monastery directory. One Moscow chapel which is absent
from the diocesan directory remains listed by the parent exarchate and in the
diocese's own parish news.

    python tools/directory_korea.py --check
    python tools/directory_korea.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-14"

EP_PARISHES_KO = "https://orthodoxkorea.org/our-parishes_ko/"
EP_PARISHES_EN = "https://orthodoxkorea.org/our-parishes_en/"
EP_MONASTERIES_KO = "https://orthodoxkorea.org/monasteries_ko/"
EP_MONASTERIES_EN = "https://orthodoxkorea.org/monasteries_en/"
EP_HISTORY = "https://orthodoxkorea.org/history_en/"
TRANSFIGURATION = "https://orthodoxmonasterykorea.org/"
TRANSFIGURATION_HISTORY = "https://orthodoxmonasterykorea.org/16"
EP_OKINAWA = (
    "https://orthodoxkorea.org/"
    "pastoral-visit-to-okinawa-and-tokyo-japan-2/"
)
EP_JAPAN_PASCHA = "https://orthodoxkorea.org/holy-week-and-pascha-in-japan/"

MP_PARISHES_KO = "https://churchkr.com/2337-2/"
MP_PARISHES_RU = "https://churchkr.com/ru/hramy/"
MP_EXARCHATE = "https://exarchate.asia/en/karta-prihodov/"
MP_ST_ANTHONY = (
    "https://churchkr.com/2025/04/26/"
    "%EB%8C%80%ED%95%9C%EC%A0%95%EA%B5%90%ED%9A%8C-%EA%B0%81-"
    "%EB%B3%B8%EB%8B%B9%EB%93%A4%EC%97%90%EC%84%9C-"
    "%EA%B4%91%EB%AA%85%EC%A3%BC%EA%B0%84-"
    "%EC%98%88%EB%B0%B0-%EA%B1%B0%ED%96%89/"
)

ROCOR_HOLY_TRINITY = (
    "https://directory.synod.com/listing/241/"
    "holy-trinity-skete-and-st-anna-church/?lang=en"
)
ROCOR_HOLY_TRINITY_KO = (
    "https://web.archive.org/web/20080121231932id_/"
    "http://www.korthodox.org/News/history_new.html"
)
ROCOR_ST_JOHN = (
    "https://directory.synod.com/listing/242/"
    "korean-orthodox-mission-st-john-the-theologian/?lang=en"
)
ROCOR_ST_JOHN_KO = (
    "https://web.archive.org/web/20230811071625id_/"
    "http://www.korthodox.org/org"
)


ROWS = {
    "ep-korea": [
        dict(id="kr-ep-seoul-st-nicholas-cathedral", parent="ep-korea",
             kind="parish", rank="Parish",
             name="St. Nicholas Cathedral, Seoul",
             local="성 니콜라스 대성당", country="KR",
             dedication="Saint Nicholas",
             address=["서울, 마포구, 마포대로 18-43 (04205)"],
             services=[
                 "조과 8:45am / 성찬 예배 10:00am",
                 "9am / 5pm",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-seoul-st-maximus", parent="ep-korea",
             kind="parish", rank="Chapel",
             name="St. Maxim's, Seoul", local="성 막심 성당", country="KR",
             dedication="Saint Maximus the Greek",
             address=["서울, 마포구, 마포대로 18-43 (04205)"],
             services=[
                 "조과 8:45am / 성찬 예배 10:00am",
                 "9am / 5pm",
             ],
             languages=["Slavonic", "English"],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN, EP_HISTORY]),
        dict(id="kr-ep-busan-annunciation", parent="ep-korea",
             kind="parish", rank="Parish",
             name="The Annunciation of the Most Holy Theotokos, Busan",
             local="성모 희보 성당", country="KR",
             dedication="The Annunciation of the Most Holy Theotokos",
             address=["부산, 중구, 중구로 97-7 (48971)"],
             services=[
                 "조과 9:00am / 성찬 예배 10:00am",
                 "8:30am / 6pm",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-incheon-st-paul", parent="ep-korea",
             kind="parish", rank="Parish",
             name="St. Paul's, Incheon", local="성 바울로 성당", country="KR",
             dedication="Saint Paul",
             address=["인천, 남동구, 석산로 111-62 (21550)"],
             services=[
                 "조과 9:00am, 성찬 예배 10:00am",
                 "수요일 3pm (9시과 & 소만과)",
                 "토요일 3pm (9시과 & 대만과)",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-jeonju-dormition", parent="ep-korea",
             kind="parish", rank="Parish",
             name="The Dormition of the Theotokos, Jeonju",
             local="성모 안식 성당", country="KR",
             dedication="The Dormition of the Theotokos",
             address=["30, 효천남로, 완산구, 전주, 전라북도(55152 )"],
             services=[
                 "조과 9:00am / 성찬 예배 10:00am",
                 "9am, 5pm",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-chuncheon-st-boris", parent="ep-korea",
             kind="parish", rank="Parish",
             name="St. Boris, Chuncheon", local="성 보리스 성당", country="KR",
             dedication="Saint Boris",
             address=["강원도, 춘천, 서면 신숭겸로 52-3 (24461)"],
             services=[
                 "조과 9:00am / 성찬 예배 10:00am",
                 "화요일 - 금요일 9am / 5pm (여름에는 6pm)",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-ulsan-st-dionysios", parent="ep-korea",
             kind="parish", rank="Parish",
             name="St. Dionysios, Ulsan",
             local="성 디오니시오스 성당", country="KR",
             dedication="Saint Dionysios",
             address=["울산,동구, 문재 7-38 (44095)"],
             services=[
                 "조과 9:00am / 성찬 예배 10:00am",
                 "8:45am / 6:30pm",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-wanju-st-anna", parent="ep-korea",
             kind="parish", rank="Parish",
             name="St. Anna, Jeonju", local="성 안나 성당", country="KR",
             dedication="Saint Anna",
             address=[
                 "전라북도, 완주군 구이면 신전길 120(학교법인 성•안나 교육재단, 55362)",
             ],
             services=[
                 "조과 9am / 성찬 예배 10am",
                 "수요일 5pm 소만과 (저녁 기도)",
                 "토요일 5pm 대만과 (저녁 기도)",
             ],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-yongmiri-resurrection", parent="ep-korea",
             kind="parish", rank="Chapel",
             name="Resurrection Chapel, Yongmi-ri",
             local="구세주 부활 성당", country="KR",
             dedication="The Resurrection of the Savior",
             address=["경기도, 파주, 광탄면, 양지말길 25"],
             sources=[EP_PARISHES_KO, EP_PARISHES_EN]),
        dict(id="kr-ep-gapyeong-transfiguration-monastery",
             parent="ep-korea", kind="monastery", rank="Monastery",
             name="Monastery of the Transfiguration of the Savior, Gapyeong",
             local="가평 구세주 변모 수도원", country="KR",
             dedication="The Transfiguration of the Savior",
             address=["〒12446 경기도 가평군 녹수계곡로 157-227"],
             site=TRANSFIGURATION,
             founded=[
                 "주님의 영광스러운 변모를 기념하는 수도원을 건립하려는 한국 정교회의 노력은 1985년 콘스탄티노플 세계 총대주교의 승인과 축복을 받음으로써 구체화되었고, 1987년 공사를 시작해 완공되었습니다.",
             ],
             sources=[EP_MONASTERIES_KO, TRANSFIGURATION,
                      TRANSFIGURATION_HISTORY]),
        dict(id="kr-ep-yanggu-st-andrew-monastery", parent="ep-korea",
             kind="monastery", rank="Monastery",
             name="Monastery of St. Andreas, Palang-ri",
             local="양구 성 안드레아 수도원", country="KR",
             dedication="Saint Andrew the First-Called",
             address=["강원도 양구군 동면 바랑길 189-12 (24506)"],
             services=["오전 9시 조과/ 오전 10시 성찬예배"],
             sources=[EP_MONASTERIES_KO, EP_MONASTERIES_EN]),
        dict(id="jp-ep-okinawa-nativity-parish", parent="ep-korea",
             kind="parish", rank="Parish",
             name="Parish of the Nativity of Christ in Okinawa",
             local="Parish of the Nativity of Christ", country="JP",
             dedication="Nativity of Christ",
             sources=[EP_OKINAWA, EP_JAPAN_PASCHA]),
    ],
    "ru-korea": [
        dict(id="kr-ru-seoul-resurrection", parent="ru-korea",
             kind="parish", rank="Parish",
             name="Church of the Resurrection of Christ in Seoul",
             local="서울 그리스도 부활 성당", country="KR",
             dedication="The Resurrection of Christ",
             address=["대한민국 서울 한강로동 한강대로 62길 45-11, 2층"],
             sources=[MP_PARISHES_KO, MP_PARISHES_RU]),
        dict(id="kr-ru-busan-nativity", parent="ru-korea",
             kind="parish", rank="Parish",
             name="Church of the Nativity of the Blessed Virgin Mary in Busan",
             local="부산 성모탄생성당", country="KR",
             dedication="The Nativity of the Most Holy Theotokos",
             address=["대한민국 부산 동구 초량동 1163-5, 3층"],
             sources=[MP_PARISHES_KO, MP_PARISHES_RU]),
        dict(id="kr-ru-incheon-st-anthony", parent="ru-korea",
             kind="parish", rank="Chapel",
             name="Church of St. Anthony the Great in Incheon",
             local="인천 성 대 안토니오스 소성당", country="KR",
             dedication="Saint Anthony the Great",
             address=["1257-50 Unbuk-dong, Jung-gu, Incheon"],
             sources=[MP_EXARCHATE, MP_ST_ANTHONY]),
        dict(id="kr-ru-incheon-all-saints", parent="ru-korea",
             kind="parish", rank="Parish",
             name="Church of All Saints in Incheon",
             local="인천 모든 성인 성당", country="KR",
             dedication="All Saints",
             address=["인천 연수구 함박뫼로50번길 101, 광용빌딩, 6층"],
             sources=[MP_PARISHES_KO, MP_PARISHES_RU]),
        dict(id="kr-ru-gyeongju-royal-passion-bearers",
             parent="ru-korea", kind="parish", rank="Parish",
             name="Parish of the Holy Royal Passion-Bearers, Gyeongju",
             local="경주 성 니콜라이 수난자 황가 성당", country="KR",
             dedication="The Holy Royal Passion-Bearers",
             address=["경북 경주시 금성로372번길 52"],
             sources=[MP_PARISHES_KO, MP_PARISHES_RU]),
        dict(id="kr-ru-cheongju-archangel-michael", parent="ru-korea",
             kind="parish", rank="Parish",
             name="Church of the Archangel Michael in Cheongju",
             local="청주 모든 천사 성당", country="KR",
             dedication="The Archangel Michael",
             address=["충북 청주시 흥덕구 봉명로 136 2층"],
             sources=[MP_PARISHES_KO, MP_PARISHES_RU]),
        dict(id="kr-ru-gwangju-exaltation-cross", parent="ru-korea",
             kind="parish", rank="Parish",
             name="Church of the Exaltation of the Holy and Life-Giving Cross of the Lord in Gwangju",
             local="광주 성 십자가 현양 성당", country="KR",
             dedication="The Exaltation of the Holy and Life-Giving Cross of the Lord",
             address=["광주 월곡동 680-6 3층 302-1호"],
             sources=[MP_PARISHES_KO, MP_PARISHES_RU]),
    ],
    "ru-australia-and-new-zealand-rocor": [
        dict(id="kr-rocor-samcheok-holy-trinity-skete",
             parent="ru-australia-and-new-zealand-rocor",
             kind="monastery", rank="Skete",
             name="Holy Trinity Skete and St. Anna Church",
             local="성 삼위 스키트(암자)와 성 안나 성당", country="KR",
             dedication="The Holy Trinity and Saint Anna",
             address=[
                 "451-1, Yongwa, Geunduk-myon",
                 "Samchok-si, Kangwon-do",
             ],
             services=[
                 "Saturday vespers 6pm; Sunday matins 7am; Divine Liturgy 9am; weekdays and feastdays vespers, matins and Divine Liturgy according to the Church calendar",
             ],
             languages=["Korean"],
             sources=[ROCOR_HOLY_TRINITY, ROCOR_HOLY_TRINITY_KO]),
        dict(id="kr-rocor-gumi-st-john-the-theologian",
             parent="ru-australia-and-new-zealand-rocor",
             kind="parish", rank="Parish",
             name="Korean Orthodox Mission, St. John the Theologian Parish",
             local="대한 그리스도 정교회 성 요한 성당", country="KR",
             dedication="Saint John the Theologian",
             address=[
                 "104-1501 Hyunjin Evervill",
                 "Okgye-dong, Gumi",
             ],
             languages=["Korean"],
             founded=["2009"],
             sources=[ROCOR_ST_JOHN, ROCOR_ST_JOHN_KO]),
    ],
}


def clean(row):
    out = {key: value for key, value in row.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("address") and (not isinstance(out["address"], list) or
                               not all(isinstance(line, str)
                                       for line in out["address"])):
        raise ValueError("%s has an invalid address" % out.get("id"))
    if out.get("languages") and (not isinstance(out["languages"], list) or
                                 not all(isinstance(word, str)
                                         for word in out["languages"])):
        raise ValueError("%s has invalid worship languages" % out.get("id"))
    if out.get("services") and (not isinstance(out["services"], list) or
                                not all(isinstance(line, str)
                                        for line in out["services"])):
        raise ValueError("%s has invalid service times" % out.get("id"))
    if out.get("founded") and (not isinstance(out["founded"], list) or
                               not all(isinstance(line, str)
                                       for line in out["founded"])):
        raise ValueError("%s has invalid history text" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"parish", "monastery"}
    parent_countries = {
        "ep-korea": ["JP", "KR"],
        "ru-korea": ["KR"],
        "ru-australia-and-new-zealand-rocor": ["KR"],
    }
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            row = clean(source)
            work_id = row.get("id")
            if not work_id or work_id in seen:
                raise ValueError("duplicate or missing id: %s" % work_id)
            if row.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (work_id, row.get("parent")))
            if row.get("kind") not in allowed_kinds:
                raise ValueError("%s has unsupported kind: %s" %
                                 (work_id, row.get("kind")))
            if row.get("kind") == "parish" and not row.get("local"):
                raise ValueError("%s is a parish without its own name" % work_id)
            if row.get("country") not in parent_countries[parent]:
                raise ValueError("%s is outside its branch countries" % work_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a name" % work_id)
            if not row.get("dedication"):
                raise ValueError("%s lacks a published dedication" % work_id)
            if row.get("site") and not row["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % work_id)
            seen.add(work_id)
            branch_seen.add(work_id)
            rows.append(row)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "rows": rows,
        }
        if len(parent_countries[parent]) == 1:
            payloads[parent]["country"] = parent_countries[parent][0]
        else:
            payloads[parent]["countries"] = parent_countries[parent]
    if len(payloads["ep-korea"]["rows"]) != 12:
        raise ValueError("the Ecumenical Patriarchate branch must have 12 rows")
    if len(payloads["ru-korea"]["rows"]) != 7:
        raise ValueError("the Moscow Patriarchate branch must have 7 rows")
    if len(payloads["ru-australia-and-new-zealand-rocor"]["rows"]) != 2:
        raise ValueError("the ROCOR branch must have 2 rows")
    return payloads


def manifest(payloads=None):
    payloads = payloads or build()
    out = {}
    for parent, payload in sorted(payloads.items()):
        spec = {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
        }
        if payload.get("countries"):
            spec["countries"] = payload["countries"]
        else:
            spec["country"] = payload["country"]
        out[parent] = spec
    return out


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
    expected = set()
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        expected.add(path.name)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    if OUT.exists():
        for name in ("ep-korea.v1.json", "ru-korea.v1.json",
                     "ru-australia-and-new-zealand-rocor.v1.json"):
            path = OUT / name
            if path.exists() and path.name not in expected:
                errors.append("unexpected %s" % path.relative_to(ROOT))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
        errors = problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Korea and Japan exarchate: %s" % exc,
              file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Korea and Japan exarchate branches: 15 parishes, 3 chapels, "
          "3 monasteries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
