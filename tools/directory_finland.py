#!/usr/bin/env python3
"""The parish-scale Finland branch of the Churches directory.

The directory spine remains small enough to load on every visit. Parish and
monastery rows live one diocese to a file and are fetched only when a reader
needs that branch. The Finnish Church publishes the full hierarchy on its own
site and links each body from its contact directory.

    python tools/directory_finland.py --check
    python tools/directory_finland.py --write
"""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory"
CHECKED = "2026-11-14"
PARISHES = "https://ort.fi/suomen-ortodoksinen-kirkko/seurakunnat/"
CONTACTS = "https://ort.fi/yhteystiedot/"
MONASTERIES = "https://ort.fi/suomen-ortodoksinen-kirkko/luostarit/"


ROWS = {
    "fi-helsinki": [
        dict(id="fi-helsinki-parish", parent="fi-helsinki",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Helsinki",
             local="Helsingin ortodoksinen seurakunta", country="FI",
             address=["Liisankatu 29 A 1", "00170 Helsinki"],
             site="https://hos.fi/",
             founded=[
                 "Helsingin ortodoksisen seurakunnan syntyhistoria voidaan palauttaa Pyhän Kolminaisuuden kirkon vihkipäivään 26. elokuuta 1827.",
             ],
             sources=[
                 PARISHES,
                 "https://hos.fi/yhteystiedot/asiakaspalvelu/",
                 "https://www.hos.fi/yhteystiedot/tietoa-seurakunnasta/historia/",
             ]),
        dict(id="fi-turku-parish", parent="fi-helsinki",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Turku",
             local="Turun ortodoksinen seurakunta", country="FI",
             address=["Yliopistonkatu 19 B 3", "20100 Turku"],
             languages=["suomi"],
             site="https://ort.fi/turku/",
             sources=[
                 PARISHES,
                 "https://ort.fi/turku/ota-yhteytta/",
                 "https://ort.fi/turku/liity-kirkkoon/",
             ]),
        dict(id="fi-southeast-parish", parent="fi-helsinki",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Southeast Finland",
             local="Kaakkois-Suomen ortodoksinen seurakunta", country="FI",
             address=["Kristiinankatu 5", "53900 Lappeenranta"],
             site="https://kaakko.ort.fi/",
             founded=[
                 "Kaakkois-Suomen ortodoksinen seurakunta aloitti toimintansa 1.1.2021.",
             ],
             sources=[
                 PARISHES,
                 "https://kaakko.ort.fi/yhteystiedot/",
                 "https://kaakko.ort.fi/wp-content/uploads/2025/10/Vuosikertomus-2024.pdf",
             ]),
    ],
    "fi-kuopio": [
        dict(id="fi-kuopio-parish", parent="fi-kuopio",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Kuopio",
             local="Kuopion ortodoksinen seurakunta", country="FI",
             address=["Snellmaninkatu 8", "70100 Kuopio"],
             site="https://ortkuopio.fi/",
             services=[
                 "Pyhän Nikolaoksen katedraalissa toimitettiin säännöllisesti seuraavat jumalanpalvelukset: lauantai-iltaisin vigilia ja sunnuntaisin liturgia, keskiviikkoiltaisin ehtoopalvelus, akatistos tai yleinen panihida.",
             ],
             languages=["slaavi", "suomi"],
             founded=[
                 "Seurakunnalla on pitkät perinteet jo vuodesta 1846, ja se näkyy alueella selvästi.",
             ],
             sources=[
                 "https://ortkuopio.fi/",
                 "https://ortkuopio.fi/ota-yhteytta/laita-viesti-tai-soita-suoraan/",
                 "https://ortkuopio.fi/wp-content/uploads/vuosikertomus-2025.pdf",
             ]),
        dict(id="fi-joensuu-parish", parent="fi-kuopio",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Joensuu",
             local="Joensuun ortodoksinen seurakunta", country="FI",
             address=["Kirkkokatu 32", "80100 Joensuu"],
             site="https://ortjoensuu.fi/",
             services=[
                 "Keskustassa jumalanpalveluksia on viikoittain, lähialueilla harvemmin.",
                 "Ke 11.11. Klo 17 Ehtoopalvelus kirkossa",
                 "La 14.11. Klo 17 Vigilia kirkossa",
                 "Su 15.11. Klo 10 Liturgia kirkossa",
             ],
             founded=[
                 "Joensuun ortodoksinen seurakunta perustettiin vuonna 1893, kun yli neljäkymmentä vuotta aiemmin perustetun Joensuun kaupungin asukasmäärä kasvoi.",
             ],
             sources=[
                 "https://ortjoensuu.fi/",
                 "https://ortjoensuu.fi/ota-yhteytta/alueet-ja-pyhakot",
                 "https://ortjoensuu.fi/kalenteri/joensuu-keskus",
             ]),
        dict(id="fi-ilomantsi-chapel-parish", parent="fi-joensuu-parish",
             kind="parish", rank="Chapel Parish",
             name="Orthodox Chapel Parish of Ilomantsi",
             local="Ilomantsin ortodoksinen kappeliseurakunta", country="FI",
             address=["Kirkkotie 17", "82900 Ilomantsi"],
             site="https://ort.fi/ilomantsi/",
             services=[
                 "Ke 30.9. klo 17 ehtoopalvelus Elian kirkko",
                 "La 3.10. klo 17 ehtoopalvelus, Elian kirkko",
                 "Su 4.10. klo 9 aamupalvelus ja liturgia, Elian kirkko",
             ],
             founded=[
                 "Ilomantsin ortodoksinen seurakunta liitettiin Joensuun ortodoksisen seurakunnan kappeliseurakunnaksi vuonna 2021.",
             ],
             sources=[
                 "https://ort.fi/ilomantsi/yhteystiedot/",
                 "https://ort.fi/ilomantsi/pyhakot/",
                 "https://ortjoensuu.fi/ota-yhteytta/alueet-ja-pyhakot",
             ]),
        dict(id="fi-jyvaskyla-parish", parent="fi-kuopio",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Jyväskylä",
             local="Jyväskylän ortodoksinen seurakunta", country="FI",
             address=["Rajakatu 39", "40200 JYVÄSKYLÄ"],
             site="https://jklort.fi/",
             services=[
                 "Säännölliset jumalanpalvelukset toimitetaan kirkossa joka viikko: keskiviikkoisin klo 17 ehtoopalvelus, lauantaisin klo 17 vigilia ja sunnuntaisin klo 10 liturgia.",
             ],
             languages=["suomi", "kirkkoslaavi"],
             founded=[
                 "Vuonna 1950 perustettu seurakuntamme jatkaa Sortavalan ortodoksisen katedraaliseurakunnan perinteitä Keski-Suomessa.",
             ],
             sources=[
                 "https://jklort.fi/yhteystiedot/",
                 "https://jklort.fi/jumalanpalvelukset/",
                 "https://jklort.fi/",
             ]),
        dict(id="fi-taipale-parish", parent="fi-kuopio",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Taipale",
             local="Taipaleen ortodoksinen seurakunta", country="FI",
             address=["Viinijärventie 7", "83400 Viinijärvi"],
             site="https://ort.fi/taipale/",
             services=[
                 "Seurakunnan alueen kirkoissa toimitetaan jumalanpalvelukset säännöllisesti: vigilia lauantaisin ja juhlien aattoina, liturgia sunnuntaisin ja juhlapäivinä sekä maallikkopalveluksina Jeesuksen rukouspalveluksia",
             ],
             languages=["suomi", "slaavi", "englanti"],
             founded=[
                 "Noin 450 vuotta sitten perustettuun Taipaleen ortodoksiseen seurakuntaan kuuluvat Liperin, Outokummun ja Polvijärven kunnat sekä Nurmeksen ortodoksisen kappeliseurakunnan kunnat Nurmes, Juuka ja Rautavaara.",
             ],
             sources=[
                 "https://ort.fi/taipale/",
                 "https://ort.fi/taipale/2026/06/21/taipaleen-kirkot-avoinna-kesalla/",
                 "https://ort.fi/taipale/wp-content/uploads/2023/11/Liite-6-Toiminta-ja-talous-2024-2026.pdf",
             ]),
        dict(id="fi-nurmes-chapel-parish", parent="fi-taipale-parish",
             kind="parish", rank="Chapel Parish",
             name="Orthodox Chapel Parish of Nurmes",
             local="Nurmeksen ortodoksinen kappeliseurakunta", country="FI",
             address=["Salmenkatu 5", "75500 NURMES"],
             site="https://ort.fi/nurmes/",
             services=[
                 "Nurmeksessa palveluksia toimitetaan talviaikaan pääasiassa Nurmeksessa, Juuassa ja Valtimolla, sunnuntaisin aamupalvelus ja liturgia ja lauantaisin ehtoopalvelus.",
                 "Nurmeksessa arkipalveluksia toimitetaan säännöllisesti keskiviikkoisin ja torstaisin.",
             ],
             languages=["suomi", "slaavi", "englanti"],
             sources=[
                 "https://ort.fi/nurmes/yhteystiedot/",
                 "https://ort.fi/kuopionjakarjalanhiippakunta/nurmes/",
                 "https://ort.fi/taipale/wp-content/uploads/2023/11/Liite-6-Toiminta-ja-talous-2024-2026.pdf",
             ]),
        dict(id="fi-saimaa-parish", parent="fi-kuopio",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Saimaa",
             local="Saimaan ortodoksinen seurakunta", country="FI",
             address=["Relanderinkatu 5", "78200 Varkaus"],
             site="https://www.ortsaimaa.net/",
             services=[
                 "Su 8.11. klo 10 liturgia",
                 "Su 22.11. klo 10 opetusliturgia",
                 "Su 6.12. klo 10 perheliturgia, kiitosrukoushetki itsenäisyyspäivänä ja puurojuhla",
                 "To 24.12. klo 17 jouluaaton ehtoopalvelus",
                 "Pe 25.12. klo 9 aamupalvelus ja liturgia, Kristuksen syntymä",
             ],
             founded=[
                 "Saimaan ortodoksinen seurakunta (lyhenne: SOS) syntyi 1.1.2017, kun Mikkelin seurakunta liittyi Varkauden seurakuntaan ja jonka nimi muutettiin Saimaan ortodoksiseksi seurakunnaksi.",
             ],
             sources=[
                 "https://www.ortsaimaa.net/perustiedot-sossta",
                 "https://www.ortsaimaa.net/10",
                 "https://www.ortsaimaa.net/varkaus-palvelukset",
             ]),
        dict(id="fi-valamo-monastery", parent="fi-kuopio",
             kind="monastery", rank="Monastery",
             name="Valamo Monastery", local="Valamon luostari", country="FI",
             address=["Valamontie 42", "79850 Uusi-Valamo"],
             site="https://valamo.fi/",
             services=[
                 "Aamupalvelus alkaa luostarin pääkirkossa arkisin klo 6 ja ehtoopalvelus kello 18.",
                 "Tiistaisin ja torstaisin aamupalvelusta seuraa liturgia, joka alkaa noin klo 7.",
                 "Lauantaiaamuisin toimitettava aamupalvelus ja liturgia alkaa kello 6.",
                 "Lauantai-illan vigilia alkaa kello 18 ja sunnuntaiaamun liturgia kello 9.",
             ],
             founded=[
                 "Perimätiedon mukaan luostari on perustettu viimeistään 1300-luvulla.",
                 "Nykyisellä paikallaan Heinäveden Papinniemessä luostari on toiminut vuodesta 1940.",
             ],
             sources=[
                 MONASTERIES,
                 "https://valamo.fi/yhteystiedot",
                 "https://valamo.fi/luostari/kirkot/paakirkko",
             ]),
        dict(id="fi-lintula-monastery", parent="fi-kuopio",
             kind="monastery", rank="Monastery",
             name="Lintula Holy Trinity Monastery",
             local="Lintulan Pyhän Kolminaisuuden luostari", country="FI",
             address=["Honkasalontie 3", "79830 Palokki"],
             site="https://www.lintulanluostari.fi/",
             services=[
                 "Kirkossa toimitetaan jumalanpalvelukset aamuin ja illoin.",
                 "JUMALANPALVELUKSET LINTULAN LUOSTARISSA KESÄLLÄ :",
                 "arkipäivinä: klo 6.00 aamupalvelus",
                 "klo 18.00 iltapalvelus (IX hetki ja ehtoopalvelus).",
                 "lauantaisin: klo 8.00 VI hetki ja liturgia",
                 "klo 18.00 vigilia ja I hetki",
                 "sunnuntaisin: klo 8.00 III hetki ja liturgia",
                 "klo 18.00 IX hetki, ehtoopalvelus ja akatistos vuoroviikoin Jumalanäidille ja Pyhälle Hengelle",
                 "JUMALANPALVELUKSET LINTULAN LUOSTARISSA TALVIKAUDELLA",
                 "arkipäivinä: klo 6.00 aamupalvelus",
                 "klo 17.00 iltapalvelus (IX hetki ja ehtoopalvelus). Tiistai-iltaisin ehtoopalveluksen jälkeen akatistos Jumalansynnyttäjälle.",
                 "Keskiviikkoisin iltapalveluksena toimitetaan Jeesuksen rukous -palvelus, ellei toisin ilmoiteta.",
                 "Perjantai-iltaisin toimitetaan aamupalvelus.",
                 "lauantaisin: klo 8.00 VI hetki ja liturgia",
                 "klo 17.00 vigilia ja I hetki",
                 "sunnuntaisin: klo 8.00 III hetki ja liturgia",
                 "klo 17.00 IX hetki, ehtoopalvelus ja akatistos vuoroviikoin Jumalanäidille ja Pyhälle Hengelle",
             ],
             languages=["suomi"],
             founded=[
                 "Lintulan Pyhän Kolminaisuuden naisyhteisö ja sittemmin luostari, perustettiin 1895 Karjalan kannakselle, Kivennavan pitäjään, vain 50km päähän Pietarista.",
                 "Arpa osui Palokin kylään Heinävedellä, jonne sisaristo muutti vuonna 1946.",
             ],
             sources=[
                 "https://www.lintulanluostari.fi/kauppa/toimitusehdot-maksutavat/",
                 "https://www.lintulanluostari.fi/jumalanpalvelukset/",
                 "https://www.lintulanluostari.fi/luostari/luostarin-historia/",
             ]),
    ],
    "fi-oulu": [
        dict(id="fi-northern-parish", parent="fi-oulu",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Northern Finland",
             local="Pohjois-Suomen ortodoksinen seurakunta", country="FI",
             address=["Torikatu 74", "90120 Oulu"],
             site="https://pohjoissuomenortodoksinenseurakunta.fi/",
             services=[
                 "On Wednesdays and Thursdays there are vespers at 18 o'clock, on Saturdays vigil at 18 o'clock, and on Sundays divine liturgy at 10 o'clock.",
             ],
             languages=["Finnish", "Church Slavonic", "Greek", "English",
                        "other languages"],
             founded=[
                 "Vuoden 2022 alussa Oulun ortodoksinen seurakunta, Kajaanin ortodoksinen seurakunta ja Lapin ortodoksinen seurakunta yhdistyivät yhdeksi Pohjois-Suomen ortodoksiseksi seurakunnaksi",
             ],
             sources=[
                 "https://pohjoissuomenortodoksinenseurakunta.fi/",
                 "https://pohjoissuomenortodoksinenseurakunta.fi/YHTEYSTIEDOT/%2C-%2C-in-english/",
                 "https://ort.fi/wp-content/uploads/2025/05/UTF-8KH-tilinpaatos-2023-allekirjoitettu.pdf",
             ]),
        dict(id="fi-lapland-chapel-parish", parent="fi-northern-parish",
             kind="parish", rank="Chapel Parish",
             name="Orthodox Chapel Parish of Lapland",
             local="Lapin ortodoksinen kappeliseurakunta", country="FI",
             address=["Ounasvaarantie 16", "96400 ROVANIEMI"],
             site="https://www.ortlappi.fi/",
             services=[
                 "Sunnuntaisin ja juhlapäivinä toimitetaan liturgia.",
                 "Vigilia lauantaisin ja juhlien aattona toimitettava iltapalvelus, jossa on peräkkäin ehtoo- ja aamupalvelus.",
             ],
             languages=["suomi", "ukraina", "kirkkoslaavi", "koltansaame"],
             sources=[
                 "https://www.ortlappi.fi/ota-yhteys/",
                 "https://www.ortlappi.fi/seurakunnan-toiminta/pyhakot/",
                 "https://www.ortlappi.fi/seurakunnan-toiminta/",
             ]),
        dict(id="fi-kainuu-chapel-parish", parent="fi-northern-parish",
             kind="parish", rank="Chapel Parish",
             name="Orthodox Chapel Parish of Kainuu",
             local="Kainuun ortodoksinen kappeliseurakunta", country="FI",
             address=["Väinämöisenkatu 29 A 1", "87100 KAJAANI"],
             site="https://ort.fi/kajaani/",
             services=[
                 "la 5.9. klo 17 vigilia",
                 "ke 9.9. klo 17 ehtoopalvelus",
                 "to 10.9. klo 10 aamupalvelus",
                 "su 20.9. klo 10 liturgia",
             ],
             founded=[
                 "Tammikuun 1. päivänä 1950 perustettiin Kajaanin ortodoksinen seurakunta.",
                 "Seurakunnan 71 vuotta kestänyt toiminta itsenäisenä seurakuntana päättyi 31.12.2021.",
                 "Vuoden 2022 alusta Kajaanin, Lapin ja Oulun ortodoksiset seurakunnan yhdistyivät uudeksi seurakunnaksi, jonka nimeksi tuli Pohjois-Suomen ortodoksinen seurakunta.",
                 "Entisestä Kajaanin ortodoksisesta seurakunnasta on käytetty 1.1.2022 jälkeen nimeä Kainuun ortodoksinen kappeliseurakunta.",
             ],
             sources=[
                 "https://ort.fi/kajaani/yhteystiedot/",
                 "https://ort.fi/kajaani/jumalanpalvelukset/",
                 "https://ort.fi/kajaani/yleistietoja-seurakunnasta/",
             ]),
        dict(id="fi-tampere-parish", parent="fi-oulu",
             kind="parish", rank="Parish",
             name="Orthodox Parish of Tampere",
             local="Tampereen ortodoksinen seurakunta", country="FI",
             address=["Suvantokatu 10, 1. kerros", "33100 Tampere"],
             site="https://www.tampereort.fi/",
             services=[
                 "La 14.11. klo 17 Vigilia",
                 "Su 15.11. klo 10 Liturgia",
                 "Ke 18.11. klo 9 Liturgia",
                 "Su 29.11. klo 10 Liturgia (slaavinkielinen)",
                 "La 12.12. klo 10 Liturgia (romaniankielinen)",
                 "Su 20.12. klo 10 Liturgia (slaavinkielinen)",
             ],
             languages=["slaavinkielinen", "romaniankielinen"],
             founded=[
                 "1.1.2021 Vaasa ja Tampere yhdistyivät hallinnollisesti yhdeksi kokonaisuudeksi.",
             ],
             sources=[
                 "https://www.tampereort.fi/seurakunta",
                 "https://www.tampereort.fi/jumalanpalvelukset",
             ]),
        dict(id="fi-vaasa-chapel-parish", parent="fi-tampere-parish",
             kind="parish", rank="Chapel Parish",
             name="Orthodox Chapel Parish of Vaasa",
             local="Vaasan ortodoksinen kappeliseurakunta", country="FI",
             address=["Koulukatu 45", "65100 Vaasa"],
             site="https://www.vaasaort.com/",
             services=[
                 "Su 1.11. klo 10.00 Liturgia",
                 "Ke 4.11. klo 17.00 Ehtoopalvelus",
                 "La 14.11. klo 17.00 Vigilia",
                 "Su 15.11. klo 10.00 Liturgia, perhepäivä.",
             ],
             founded=[
                 "Vaasan ortodoksisen seurakunnan perustamisvuotena voitaneen pitää vuotta 1862.",
             ],
             sources=[
                 "https://www.vaasaort.com/yhteystiedot.html",
                 "https://www.vaasaort.com/jumalanpalvelukset.html",
                 "https://www.vaasaort.com/seurakunnan-historiasta.html",
             ]),
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
            if row.get("country") != "FI":
                raise ValueError("%s is outside Finland" % work_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a name" % work_id)
            if row.get("site") and not row["site"].startswith("http"):
                raise ValueError("%s carries a non-URL site" % work_id)
            seen.add(work_id)
            branch_seen.add(work_id)
            rows.append(row)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "FI",
            "rows": rows,
        }
    if sum(len(payload["rows"]) for payload in payloads.values()) != 17:
        raise ValueError("Finland must publish exactly 17 branch rows")
    return payloads


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
    expected = set()
    for parent, payload in sorted(payloads.items()):
        path = output_path(parent)
        expected.add(path.name)
        if not path.exists():
            errors.append("missing %s" % path.relative_to(ROOT))
        elif path.read_bytes().replace(b"\r\n", b"\n") != encoded(payload):
            errors.append("stale %s" % path.relative_to(ROOT))
    if OUT.exists():
        for path in OUT.glob("fi-*.v1.json"):
            if path.name not in expected:
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
        print("directory Finland: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Finland branches: 3 dioceses, 10 parishes, 5 chapel parishes, "
          "2 monasteries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
