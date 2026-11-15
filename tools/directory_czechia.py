#!/usr/bin/env python3
"""Validated directory fragments for canonical Orthodox bodies in Czechia.

The local Church's current Moravian and Silesian schematism is combined with
the Czech Ministry of Culture's live register of active Prague-eparchy parish
communities.  Other canonical jurisdictions are added only from their own
current official lists.

    python tools/directory_czechia.py --check
    python tools/directory_czechia.py --dump
"""

import argparse
import json
import re
import sys
import unicodedata


CHECKED = "2026-11-15"

PRAGUE_REGISTRY = (
    "https://www-cns.mkcr.cz/cns_internet/CNS/"
    "Seznam_cpo.aspx?id_subj=1198&str_zpet=Seznam_CPO.aspx"
)
OLOMOUC_SCHEMATISM = "https://www.ob-eparchie.cz/schematismus/"
RUSSIAN_KARLOVY = (
    "https://orthodox.sk/zastupitelstvo-pri-moskovskom-patriarchate/"
)
RUSSIAN_KARLOVY_HISTORY = "https://mospat.ru/en/news/45656/"
RUSSIAN_PRAGUE = "https://mospat.ru/en/news/92900/"
RUSSIAN_PRAGUE_CURRENT = "https://patriarchia.ru/index.ht/article/122732"
OCU_MISSION = "https://cerkva-praha.cz/en"
OCU_MISSION_CLERGY = "https://cerkva-praha.cz/en/clergy"
OCU_SYNOD = (
    "https://www.pomisna.info/uk/document-post/"
    "dokumenty-zasidannya-svyashhennogo-synodu-18-zhovtnya-2022-r/"
)


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value
                    if not unicodedata.combining(char))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value


def row(row_id, parent, name, local, sources, rank="Parish Community",
        kind="parish", address=None, site=None):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "CZ",
        "sources": sources,
    }
    if address:
        value["address"] = address
    if site:
        value["site"] = site
    return value


# Active legal parish communities in the Prague Eparchy.  The Ministry's
# live register marks erased entities with X; those records are retained in
# the candidate ledger rather than emitted here.
PRAGUE_SPECS = [
    ("as-second", "Second Orthodox Parish Community in As",
     "Pravoslavná církevní obec /II. v Aši"),
    ("beroun", "Orthodox Parish Community in Beroun",
     "Pravoslavná církevní obec v Berouně"),
    ("bilina", "Orthodox Parish Community in Bilina",
     "Pravoslavná církevní obec v Bílině"),
    ("brandys-stara-boleslav",
     "Orthodox Parish Community in Brandys nad Labem-Stara Boleslav",
     "Pravoslavná církevní obec v Brandýse nad Labem-Staré Boleslavi"),
    ("ceske-budejovice", "Orthodox Parish Community in Ceske Budejovice",
     "Pravoslavná církevní obec v Českých Budějovicích"),
    ("halze", "Orthodox Parish Community in Halze",
     "Pravoslavná církevní obec v Halžích"),
    ("horsovsky-tyn", "Orthodox Parish Community in Horsovsky Tyn",
     "Pravoslavná církevní obec v Horšovském Týně"),
    ("hradec-kralove", "Orthodox Parish Community in Hradec Kralove",
     "Pravoslavná církevní obec v Hradci Králové"),
    ("chomutov", "Orthodox Parish Community in Chomutov",
     "Pravoslavná církevní obec v Chomutově"),
    ("jablonec-nad-nisou",
     "Orthodox Parish Community in Jablonec nad Nisou",
     "Pravoslavná církevní obec v Jablonci nad Nisou"),
    ("jindrichuv-hradec",
     "Orthodox Parish Community in Jindrichuv Hradec",
     "Pravoslavná církevní obec v Jindřichově Hradci"),
    ("kadan", "Orthodox Parish Community in Kadan",
     "Pravoslavná církevní obec v Kadani"),
    ("kladno", "Orthodox Parish Community in Kladno",
     "Pravoslavná církevní obec v Kladně"),
    ("klatovy", "Orthodox Parish Community in Klatovy",
     "Pravoslavná církevní obec v Klatovech"),
    ("kolin", "Orthodox Parish Community in Kolin",
     "Pravoslavná církevní obec v Kolíně"),
    ("kralupy", "Orthodox Parish Community in Kralupy nad Vltavou",
     "Pravoslavná církevní obec v Kralupech n. Vltavou"),
    ("krupka", "Orthodox Parish Community in Krupka",
     "Pravoslavná církevní obec v Krupce"),
    ("lanskroun", "Orthodox Parish Community in Lanskroun",
     "Pravoslavná církevní obec v Lanškrouně"),
    ("lesna", "Orthodox Parish Community in Lesna",
     "Pravoslavná církevní obec v Lesné"),
    ("liberec", "Orthodox Parish Community in Liberec",
     "Pravoslavná církevní obec v Liberci"),
    ("litomerice", "Orthodox Parish Community in Litomerice",
     "Pravoslavná církevní obec v Litoměřicích"),
    ("marianske-lazne", "Orthodox Parish Community in Marianske Lazne",
     "Pravoslavná církevní obec v Mariánských Lázních"),
    ("melnik", "Orthodox Parish Community in Melnik",
     "Pravoslavná církevní obec v Mělníku"),
    ("milire", "Orthodox Parish Community in Milire",
     "Pravoslavná církevní obec v Milířích"),
    ("mlada-boleslav", "Orthodox Parish Community in Mlada Boleslav",
     "Pravoslavná církevní obec v Mladé Boleslavi"),
    ("mochov", "Orthodox Parish Community in Mochov",
     "Pravoslavná církevní obec v Mochově"),
    ("most", "Orthodox Parish Community in Most",
     "Pravoslavná církevní obec v Mostě"),
    ("mukarov", "Orthodox Parish Community in Mukarov",
     "Pravoslavná církevní obec v Mukařově"),
    ("pardubice", "Orthodox Parish Community in Pardubice",
     "Pravoslavná církevní obec v Pardubicích"),
    ("plzen", "Orthodox Parish Community in Plzen",
     "Pravoslavná církevní obec v Plzni"),
    ("prague-1-iii", "Orthodox Parish Community in Prague 1/III - New Town",
     "Pravoslavná církevní obec v Praze 1/III. - Nové Město"),
    ("prague-1-vii", "Orthodox Parish Community in Prague 1/VII - New Town",
     "Pravoslavná církevní obec v Praze 1/VII - Nové Město"),
    ("prague-13-xii", "Orthodox Parish Community in Prague 13/XII - Trebonice",
     "Pravoslavná církevní obec v Praze 13/XII - Třebonice"),
    ("prague-2-i", "Orthodox Parish Community in Prague 2/I - New Town",
     "Pravoslavná církevní obec v Praze 2/I. - Nové Město"),
    ("prague-2-viii", "Orthodox Parish Community in Prague 2/VIII",
     "Pravoslavná církevní obec v Praze 2/VIII"),
    ("prague-3-ii", "Orthodox Parish Community in Prague 3/II - Zizkov",
     "Pravoslavná církevní obec v Praze 3/II - Žižkov"),
    ("prague-4-v", "Orthodox Parish Community in Prague 4/V",
     "Pravoslavná církevní obec v Praze 4/V."),
    ("prague-5-ix", "Orthodox Parish Community in Prague 5/IX - Mala Chuchle",
     "Pravoslavná církevní obec v Praze 5/IX - Malé Chuchli"),
    ("prague-5-vi-michael",
     "St Michael Orthodox Parish Community in Prague 5/VI - Smichov",
     "Pravoslavná církevní obec v Praze 5/VI Chrám sv. Michala v Kinského zahradě - Praha 5-Smíchov"),
    ("prague-5-xi", "Orthodox Parish Community in Prague 5/XI - Zbraslav",
     "Pravoslavná církevní obec v Praze 5/XI - Zbraslav"),
    ("prague-6-iv", "Orthodox Parish Community in Prague 6/IV - Bubenec",
     "Pravoslavná církevní obec v Praze 6/IV - Bubeneč"),
    ("pribram", "Orthodox Parish Community in Pribram",
     "Pravoslavná církevní obec v Příbrami"),
    ("rakovnik", "Orthodox Parish Community in Rakovnik",
     "Pravoslavná církevní obec v Rakovníku"),
    ("rokycany", "Orthodox Parish Community in Rokycany",
     "Pravoslavná církevní obec v Rokycanech"),
    ("roudnice", "Orthodox Parish Community in Roudnice nad Labem",
     "Pravoslavná církevní obec v Roudnici nad Labem"),
    ("rumburk", "Orthodox Parish Community in Rumburk",
     "Pravoslavná církevní obec v Rumburku"),
    ("sokolov", "Orthodox Parish Community in Sokolov",
     "Pravoslavná církevní obec v Sokolově"),
    ("tabor", "Orthodox Parish Community in Tabor",
     "Pravoslavná církevní obec v Táboře"),
    ("tachov", "Orthodox Parish Community in Tachov",
     "Pravoslavná církevní obec v Tachově"),
    ("teplice", "Orthodox Parish Community in Teplice",
     "Pravoslavná církevní obec v Teplicích"),
    ("trnova", "Orthodox Parish Community in Trnova",
     "Pravoslavná církevní obec v Trnové (Praha - západ)"),
    ("trutnov", "Orthodox Parish Community in Trutnov",
     "Pravoslavná církevní obec v Trutnově"),
    ("usti-nad-labem", "Orthodox Parish Community in Usti nad Labem",
     "Pravoslavná církevní obec v Ústí nad Labem"),
    ("zatec", "Orthodox Parish Community in Zatec",
     "Pravoslavná církevní obec v Žatci"),
    ("zelezny-brod", "Orthodox Parish Community in Zelezny Brod",
     "Pravoslavná církevní obec v Železném Brodě"),
    ("frantiskovy-lazne",
     "Orthodox Parish Community in Frantiskovy Lazne",
     "Pravoslavná církevní obec ve Františkových Lázních"),
    ("frydlant", "Orthodox Parish Community in Frydlant in Bohemia",
     "Pravoslavná církevní obec ve Frýdlantu v Čechách"),
    ("straz-pod-ralskem",
     "Orthodox Parish Community in Straz pod Ralskem",
     "Pravoslavná církevní obec ve Stráži pod Ralskem"),
]


PRAGUE_ROWS = [
    row("cz-cs-prague-" + suffix, "cs-prague", name, local,
        [PRAGUE_REGISTRY])
    for suffix, name, local in PRAGUE_SPECS
]


OLOMOUC_SPECS = [
    ("olomouc-gorazd-cathedral", "St Gorazd Cathedral in Olomouc",
     "Katedrální chrám sv. Gorazda, žáka Metodějova", "Cathedral", "parish"),
    ("olomouc-protection-chapel", "Protection of the Theotokos Chapel in Olomouc",
     "Kaple Záštity přesvaté Bohorodice", "Chapel", "parish"),
    ("olomouc-gorazd-ii-chapel", "St Gorazd II Chapel in Olomouc",
     "Kaple sv. mučedníka biskupa Gorazda II.", "Chapel", "parish"),
    ("celechovice-trinity", "Holy Trinity Filial Church in Celechovice na Hane",
     "Filiální církevní obec Čelechovice na Hané - chrám Svaté Trojice", "Filial Church", "parish"),
    ("olomouc-city-gorazd", "St Gorazd I Orthodox Parish Community in Olomouc",
     "Olomouc město - chrám sv. Gorazda I.", "Parish Community", "parish"),
    ("prerov-cyril-methodius", "Sts Cyril and Methodius Church in Prerov",
     "Přerov - chrám sv. Cyrila a Metoděje", "Church", "parish"),
    ("prostejov", "Orthodox Parish Community in Prostejov",
     "Prostějov", "Parish Community", "parish"),
    ("libina-james", "St James the Apostle Church in Libina",
     "Libina - chrám sv. ap. Jakuba", "Church", "parish"),
    ("unicov-resurrection", "Holy Resurrection Church in Unicov",
     "Uničov - chrám sv. Vzkříšení", "Church", "parish"),
    ("stepanov-procopius", "St Procopius of Sazava Filial Church in Stepanov",
     "Filiální církevní obec Štěpánov - chrám sv. Prokopa Sázavského", "Filial Church", "parish"),
    ("rimice-ludmila", "St Ludmila Church in Rimice",
     "Řimice - chrám sv. Ludmily", "Church", "parish"),
    ("chudobin-cyril-methodius", "Sts Cyril and Methodius Filial Church in Chudobin",
     "Filiální církevní obec Chudobín - chrám sv. Cyrila a Metoděje", "Filial Church", "parish"),
    ("chudobin-nicholas-chapel", "St Nicholas the Wonderworker Chapel in Chudobin",
     "Kaple sv. Mikuláše Divotvůrce", "Chapel", "parish"),
    ("mohelnice-vladimir", "St Vladimir Filial Church in Mohelnice",
     "Filiální církevní obec Mohelnice - chrám sv. Vladimíra", "Filial Church", "parish"),
    ("stremenicko-wenceslas", "St Wenceslas Filial Church in Stremenicko",
     "Filiální církevní obec Střemeníčko u Bouzova - chrám sv. Václava", "Filial Church", "parish"),
    ("svitavy-george", "St George Church in Svitavy",
     "Svitavy - chrám sv. Jiří", "Church", "parish"),
    ("sumperk-holy-spirit", "Holy Spirit Church in Sumperk",
     "Šumperk - chrám Svatého Ducha", "Church", "parish"),
    ("brno-wenceslas-cathedral", "St Wenceslas Cathedral in Brno",
     "Brno - katedrální chrám sv. Václava", "Cathedral", "parish"),
    ("brno-turany-protection", "Protection of the Theotokos Church in Brno-Turany",
     "Brno Tuřany - chrám Záštity přesvaté Bohorodice", "Church", "parish"),
    ("brno-north-wenceslas", "St Wenceslas Orthodox Parish Community in Brno North",
     "Brno Sever - chrám sv. Václava", "Parish Community", "parish"),
    ("brno-south-vladimir", "St Vladimir Church in Brno South",
     "Brno Jih - chrám sv. Vladimíra", "Church", "parish"),
    ("dolni-kounice-barbara", "St Barbara Church in Dolni Kounice",
     "Dolní Kounice - chrám sv. Barbory", "Church", "parish"),
    ("mikulov-nicholas", "St Nicholas Church in Mikulov",
     "Mikulov - chrám sv. Mikuláše", "Church", "parish"),
    ("hodonin-methodius", "St Methodius Chapel in Hodonin",
     "Hodonín - kaple sv. Metoděje", "Chapel", "parish"),
    ("kromeriz-cyril-methodius", "Sts Cyril and Methodius Church in Kromeriz",
     "Kroměříž - chrám sv. Cyrila a Metoděje", "Church", "parish"),
    ("zlin-ivan", "St Ivan the Czech Chapel in Zlin",
     "Zlín - kaple sv. Ivana Českého", "Chapel", "parish"),
    ("uhersky-brod-george", "St George Church in Uhersky Brod",
     "Uherský Brod - chrám sv. Jiří", "Church", "parish"),
    ("hruba-vrbka", "Orthodox Parish Community in Hruba Vrbka",
     "Hrubá Vrbka", "Parish Community", "parish"),
    ("jihlava-wenceslas-ludmila-house", "Sts Wenceslas and Ludmila House Chapel in Jihlava",
     "Jihlava - domovní kaple sv. Václava a Ludmily", "House Chapel", "parish"),
    ("jihlava-holy-spirit-john", "Holy Spirit and Conception of St John the Baptist Church in Jihlava",
     "Jihlava - chrám Svatého Ducha a Početí sv. proroka Jana Křtitele", "Church", "parish"),
    ("opatov-joachim-anna", "Sts Joachim and Anna Filial Church in Opatov",
     "Filiální církevní obec Opatov - chrám sv. Jáchyma a Anny", "Filial Church", "parish"),
    ("brtnice-rastislav", "St Rastislav Chapel in Brtnice",
     "Brtnice - kaple sv. Rostislava", "Chapel", "parish"),
    ("trebic-wenceslas-ludmila", "Sts Wenceslas and Ludmila Church in Trebic",
     "Třebíč - chrám sv. Václava a Ludmily", "Church", "parish"),
    ("znojmo-rastislav", "St Rastislav Church in Znojmo",
     "Znojmo - chrám sv. Rostislava", "Church", "parish"),
    ("olbramovice-cyril-methodius", "Sts Cyril and Methodius Chapel in Olbramovice",
     "Olbramovice - kaple sv. Cyrila a Metoděje", "Chapel", "parish"),
    ("zdar", "Orthodox Parish Community in Zdar nad Sazavou",
     "Žďár nad Sázavou", "Parish Community", "parish"),
    ("milotice-annunciation", "Annunciation of the Theotokos Church in Milotice nad Opavou",
     "Milotice nad Opavou - chrám Zvěstování přesvaté Bohorodice", "Church", "parish"),
    ("bruntal-consoler", "Our Lady the Consoler Church in Bruntal",
     "Bruntál - chrám Panny Marie Těšitelky", "Church", "parish"),
    ("opava-peter-paul", "Sts Peter and Paul Chapel in Opava-Kylesovice",
     "Opava - kaple sv. Petra a Pavla", "Chapel", "parish"),
    ("sudice-wenceslas", "St Wenceslas Filial Church in Sudice",
     "Filiální obec Sudice - chrám sv. Václava", "Filial Church", "parish"),
    ("osoblaha-nicholas", "St Nicholas Church in Osoblaha",
     "Osoblaha - chrám sv. Mikuláše", "Church", "parish"),
    ("ostrava-michalkovice-nativity", "Nativity of the Theotokos Church in Ostrava-Michalkovice",
     "Ostrava - Michálkovice - chrám Narození přesvaté Bohorodice", "Church", "parish"),
    ("ostrava-pustkovec-angels", "Holy Guardian Angels Church in Ostrava-Pustkovec",
     "Ostrava - Pustkovec - chrám svatých Andělů strážných", "Church", "parish"),
    ("frydek-mistek", "Orthodox Parish Community in Frydek-Mistek",
     "Frýdek-Místek", "Parish Community", "parish"),
    ("ostrava-poruba-george", "St George Chapel in Ostrava-Poruba",
     "Ostrava - Poruba - kaple sv. Jiří", "Chapel", "parish"),
    ("jesenik-dormition", "Dormition of the Theotokos Chapel in Jesenik",
     "Jeseník - kaple Zesnutí přesvaté Bohorodice", "Chapel", "parish"),
    ("vilemov-dormition-monastery", "Dormition of the Theotokos Monastery in Vilemov",
     "Monastýr Zesnutí přesvaté Bohorodice ve Vilémově", "Monastery", "monastery"),
    ("hruba-vrbka-gorazd-monastery", "St Gorazd the Martyr Monastery in Hruba Vrbka",
     "Monastýr svatého mučedníka Gorazda v Hrubé Vrbce", "Monastery", "monastery"),
    ("brno-ludmila-monastery", "St Ludmila, Princess of the Czechs, Monastery in Brno",
     "Monastýr svaté kněžny české Ludmily", "Monastery", "monastery"),
    ("hruba-vrbka-gorazd-memorial", "St Gorazd the Martyr Memorial Chapel in Hruba Vrbka",
     "Památník s kaplí sv. mučedníka biskupa Gorazda", "Memorial Chapel", "parish"),
]


OLOMOUC_ROWS = [
    row("cz-cs-ob-" + suffix, "cs-olomouc-brno", name, local,
        [OLOMOUC_SCHEMATISM], rank=rank, kind=kind)
    for suffix, name, local, rank, kind in OLOMOUC_SPECS
]


RUSSIAN_ROWS = [
    row(
        "cz-ru-karlovy-vary-peter-paul-metochion", "russia",
        "Representation of the Russian Orthodox Church - Metochion - Church of the Holy Apostles Peter and Paul",
        "Представительство Русской Православной Церкви - Подворье - храм святых апостолов Петра и Павла",
        [RUSSIAN_KARLOVY, RUSSIAN_KARLOVY_HISTORY],
        rank="Metochion",
        address=["Krále Jiřího 1040/26", "360 01 Karlovy Vary, Czechia"],
    ),
    row(
        "cz-ru-prague-george-embassy", "russia",
        "Church of the Holy Great Martyr George at the Embassy of the Russian Federation in Prague",
        "Храм святого великомученика Георгия Победоносца при Посольстве Российской Федерации в Праге",
        [RUSSIAN_PRAGUE, RUSSIAN_PRAGUE_CURRENT], rank="Church",
    ),
]


OCU_ROWS = [
    row(
        "cz-ocu-prague-chaplaincy-mission", "ukraine-ocu",
        "Chaplaincy Mission of the Orthodox Church of Ukraine for Orthodox Ukrainians in Czechia",
        "Капеланська місія Православної Церкви України для православних українців у Чехії",
        [OCU_MISSION, OCU_MISSION_CLERGY, OCU_SYNOD], rank="Mission",
        address=["Holy Trinity Church", "Na Václavce 117/1", "150 00 Praha 5, Czechia"],
        site=OCU_MISSION,
    ),
]


ROWS = {
    "cs-olomouc-brno": OLOMOUC_ROWS,
    "cs-prague": PRAGUE_ROWS,
    "russia": RUSSIAN_ROWS,
    "ukraine-ocu": OCU_ROWS,
}

EXPECTED = {
    "cs-olomouc-brno": 50,
    "cs-prague": 58,
    "russia": 2,
    "ukraine-ocu": 1,
}

ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
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
    serialized = json.dumps(out, ensure_ascii=False)
    if "\u2013" in serialized or "\u2014" in serialized:
        raise ValueError("%s contains a long dash" % out.get("id"))
    if "\u2018" in serialized or "\u2019" in serialized:
        raise ValueError("%s contains a curly apostrophe" % out.get("id"))
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
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row_id):
                raise ValueError("invalid Czechia row id: %s" % row_id)
            if item.get("parent") != parent:
                raise ValueError("%s has wrong parent" % row_id)
            if item.get("country") != "CZ":
                raise ValueError("%s is outside Czechia" % row_id)
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s lacks a name" % row_id)
            seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "CZ",
            "rows": rows,
        }
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Czechia parent counts changed: %r" % actual)
    if len(ENGLISH_NAMES) != sum(EXPECTED.values()):
        raise ValueError("Czechia English name coverage changed")
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
        print("directory Czechia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
        return 0
    print("Czechia: %d verified bodies across 4 canonical parents" %
          sum(EXPECTED.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
