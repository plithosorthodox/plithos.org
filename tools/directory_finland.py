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

HELSINKI_SITES = "https://www.hos.fi/kirkot-ja-pyhakot/"
TURKU_SITES = "https://ort.fi/turku/pyhakot/"
SOUTHEAST_SITES = "https://kaakko.ort.fi/yhteystiedot/"
SOUTHEAST_KOUVOLA = "https://kaakko.ort.fi/yhteystiedot-2/"
SOUTHEAST_KOTKA = "https://kaakko.ort.fi/kotka-loviisa/yhteystiedot/"
KUOPIO_SITES = "https://ortkuopio.fi/seurakuntamme/pyhakot/"
JOENSUU_SITES = "https://ortjoensuu.fi/ota-yhteytta/alueet-ja-pyhakot"
JYVASKYLA_SITES = "https://jklort.fi/tietoja/pyhakot/"
TAIPALE_SITES = "https://ort.fi/taipale/pyhakot/"
NURMES_SITES = "https://ort.fi/nurmes/pyhakot/"
SAIMAA_SITES = "https://www.ortsaimaa.net/10"
SAIMAA_OTHER = "https://www.ortsaimaa.net/muualla-palvelukset"
NORTH_SITES = (
    "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/"
)
LAPLAND_SITES = "https://www.ortlappi.fi/seurakunnan-toiminta/pyhakot/"
KAINUU_SITES = "https://ort.fi/kajaani/pyhakot/"
TAMPERE_SITES = "https://www.tampereort.fi/tilat"
VAASA_SITES = "https://www.vaasaort.com/yhteystiedot.html"
VALAMO_CHURCHES = "https://valamo.fi/luostari/kirkot"
VALAMO_CHAPELS = "https://valamo.fi/luostari/kirkot/tsasounat"
LINTULA_SITES = (
    "https://www.lintulanluostari.fi/luostari/kirkko-ja-tsasounat/"
)
MOSCOW_CALENDAR = "https://calendar.rop.ru/index.php?inc=12"
MOSCOW_FINLAND = "https://sobor.patriarchia.ru/article/60757"
SAINT_NICHOLAS = "https://www.svt-nikolai.org/en/"
SAINT_NICHOLAS_CONTACT = "https://www.svt-nikolai.org/en/?page_id=10"


def sacred(work_id, parent, rank, name, local, address, source,
           dedication=None, site=None, languages=None):
    """Return one officially documented sacred place or worship site."""
    return dict(
        id=work_id, parent=parent, kind="parish", rank=rank,
        name=name, local=local, country="FI", dedication=dedication,
        address=address, site=site, languages=languages,
        sources=[source],
    )


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


# Sacred places published by the local Finnish Orthodox bodies. A church,
# chapel, prayer room, or recurring borrowed venue is a parish-scale row.
ROWS["fi-helsinki"].extend([
    sacred("fi-helsinki-uspenski-cathedral", "fi-helsinki-parish",
           "Cathedral", "Uspenski Cathedral", "Uspenskin katedraali",
           ["Pormestarinrinne 1", "00160 Helsinki"], HELSINKI_SITES,
           "The Dormition of the Theotokos"),
    sacred("fi-helsinki-holy-trinity", "fi-helsinki-parish", "Church",
           "Holy Trinity Church in Helsinki", "Pyhän Kolminaisuuden kirkko",
           ["Unioninkatu 31", "00170 Helsinki"], HELSINKI_SITES,
           "The Holy Trinity", languages=["Church Slavonic"]),
    sacred("fi-helsinki-home-church", "fi-helsinki-parish", "Church",
           "Home Church in Helsinki", "Kotikirkko",
           ["Liisankatu 29 A, 4th floor", "00170 Helsinki"], HELSINKI_SITES,
           "The Apostle James and Great Martyr Catherine"),
    sacred("fi-helsinki-prophet-elijah-cemetery", "fi-helsinki-parish",
           "Cemetery Church", "Church of the Prophet Elijah in Helsinki",
           "Hautausmaan kirkko, Profeetta Elian kirkko",
           ["Lapinlahdentie 2", "00180 Helsinki"], HELSINKI_SITES,
           "The Prophet Elijah", languages=["Finnish", "Ukrainian"]),
    sacred("fi-helsinki-myllypuro-saint-alexander-svir", "fi-helsinki-parish",
           "Chapel", "Chapel of Saint Alexander of Svir in Myllypuro",
           "Myllypuron kappeli, Pyhittäjä Aleksanteri Syväriläisen kappeli",
           ["Jauhokuja 3 B 2", "00920 Helsinki"], HELSINKI_SITES,
           "Saint Alexander of Svir"),
    sacred("fi-espoo-tapiola-saint-herman-alaska", "fi-helsinki-parish",
           "Church", "Church of Saint Herman of Alaska in Tapiola",
           "Tapiolan kirkko, Pyhittäjä Herman Alaskalaisen kirkko",
           ["Kaupinkalliontie 2", "02100 Espoo"], HELSINKI_SITES,
           "Saint Herman of Alaska"),
    sacred("fi-vantaa-tikkurila-ascension", "fi-helsinki-parish", "Church",
           "Church of the Ascension in Tikkurila",
           "Tikkurilan kirkko, Kristuksen taivaaseenastumisen kirkko",
           ["Läntinen Valkoisenlähteentie 48", "01300 Vantaa"],
           HELSINKI_SITES, "The Ascension of Christ"),
    sacred("fi-hanko-saints-vladimir-mary-magdalene", "fi-helsinki-parish",
           "Church", "Church of Saints Vladimir and Mary Magdalene in Hanko",
           "Hangon kirkko, pyhien apostolienvertaisten Vladimir Kiovalaisen "
           "ja Magdalan Marian kirkko",
           ["Täktomintie 5", "10900 Hanko"], HELSINKI_SITES,
           "Saints Vladimir of Kyiv and Mary Magdalene"),
    sacred("fi-heinola-ascension", "fi-helsinki-parish", "Church",
           "Church of the Ascension in Heinola",
           "Heinolan kirkko, Kristuksen taivaaseenastumisen kirkko",
           ["Hämeenkatu 6", "18100 Heinola"], HELSINKI_SITES,
           "The Ascension of Christ"),
    sacred("fi-hyvinkaa-enlighteners-karelia", "fi-helsinki-parish",
           "Church", "Church of the Enlighteners of Karelia in Hyvinkää",
           "Hyvinkään kirkko, Karjalan valistajien kirkko",
           ["Tsasounakuja 1", "05830 Hyvinkää"], HELSINKI_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-hameenlinna-tikhvin-icon", "fi-helsinki-parish", "Church",
           "Church of the Tikhvin Icon of the Mother of God in Hämeenlinna",
           "Hämeenlinnan kirkko, Jumalanäidin Tihvinäläisen ikonin kirkko",
           ["Erottajakatu 2", "13130 Hämeenlinna"], HELSINKI_SITES,
           "The Tikhvin Icon of the Mother of God"),
    sacred("fi-hameenlinna-ahvenisto-saint-john", "fi-helsinki-parish",
           "Church", "Church of the Beheading of Saint John in Ahvenisto",
           "Ahveniston kirkko, pyhän Johannes Kastajan mestauksen muistolle "
           "pyhitetty kirkko", ["Parantolankatu 3", "13530 Hämeenlinna"],
           HELSINKI_SITES, "The Beheading of Saint John the Baptist"),
    sacred("fi-jarvenpaa-kazan-icon", "fi-helsinki-parish", "Church",
           "Church of the Kazan Icon of the Mother of God in Järvenpää",
           "Järvenpään kirkko, Jumalansynnyttäjän Kazanilaisen ikonin kirkko",
           ["Kartanontie 45", "04410 Järvenpää"], HELSINKI_SITES,
           "The Kazan Icon of the Mother of God"),
    sacred("fi-loppi-kaunisniemi-saints-james-anna", "fi-helsinki-parish",
           "Church", "Church of Saints James and Anna in Kaunisniemi",
           "Kaunisniemen kirkko, apostoli Jaakobin ja Herran äidinäidin, "
           "pyhän Annan kuolonuneen nukkumisen muistolle pyhitetty kirkko",
           ["Kaunisniementie 18", "12600 Loppi"], HELSINKI_SITES,
           "The Apostle James and the Dormition of Saint Anna"),
    sacred("fi-iitti-kausala-nativity-theotokos", "fi-helsinki-parish",
           "Chapel", "Chapel of the Nativity of the Theotokos in Kausala",
           "Kausalan tsasouna, Neitseen Marian syntymän tsasouna",
           ["Keskikatu 4", "47400 Iitti"], HELSINKI_SITES,
           "The Nativity of the Theotokos"),
    sacred("fi-klaukkala-saint-nektarios", "fi-helsinki-parish", "Church",
           "Church of Saint Nektarios in Klaukkala",
           "Klaukkalan kirkko, Pyhän Nektarios Eginalaisen kirkko",
           ["Kuonomäentie 80", "01800 Klaukkala"], HELSINKI_SITES,
           "Saint Nektarios of Aegina"),
    sacred("fi-lahti-holy-trinity", "fi-helsinki-parish", "Church",
           "Holy Trinity Church in Lahti",
           "Lahden kirkko, Pyhän Kolminaisuuden kirkko",
           ["Harjukatu 5", "15110 Lahti"], HELSINKI_SITES,
           "The Holy Trinity"),
    sacred("fi-lohja-enlighteners-karelia", "fi-helsinki-parish", "Church",
           "Church of the Enlighteners of Karelia in Lohja",
           "Lohjan kirkko, Karjalan valistajien kirkko",
           ["Nahkurinkatu 4", "08100 Lohja"], HELSINKI_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-lohja-metsola-all-saints", "fi-helsinki-parish", "Chapel",
           "All Saints Chapel at Metsola Cemetery in Lohja",
           "Lohjan Metsolan tsasouna, Kaikkien pyhien tsasouna",
           ["Metsolan hautausmaa", "Myyryntie", "08150 Lohja"],
           HELSINKI_SITES, "All Saints"),
    sacred("fi-orimattila-saints-peter-paul", "fi-helsinki-parish", "Chapel",
           "Chapel of Saints Peter and Paul in Orimattila",
           "Orimattilan tsasouna, Pyhien Pietarin ja Paavalin tsasouna",
           ["Toivolantie 19", "16300 Orimattila"], HELSINKI_SITES,
           "Saints Peter and Paul"),
    sacred("fi-porvoo-transfiguration", "fi-helsinki-parish", "Church",
           "Church of the Transfiguration in Porvoo",
           "Porvoon kirkko, Kristuksen kirkastumisen kirkko",
           ["Vanha Helsingintie 2", "06100 Porvoo"], HELSINKI_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-forssa-saint-seraphim", "fi-helsinki-parish", "Prayer Room",
           "Prayer Room of Saint Seraphim of Sarov in Forssa",
           "Forssan rukoushuone, Pyhittäjä Serafim Sarovilaisen rukoushuone",
           ["Keskuskatu 10", "30100 Forssa"], HELSINKI_SITES,
           "Saint Seraphim of Sarov"),
    sacred("fi-riihimaki-minea", "fi-helsinki-parish", "Prayer Room",
           "Minea Orthodox Prayer Room in Riihimäki",
           "Riihimäen toimitila Minea",
           ["Valtakatu 3", "11130 Riihimäki"], HELSINKI_SITES),
    sacred("fi-helsinki-mikonkatu-nativity-theotokos", "fi-helsinki",
           "Chapel", "Chapel of the Nativity of the Theotokos on Mikonkatu",
           "Mikonkadun kappeli, Jumalansynnyttäjän syntymän kappeli",
           ["Mikonkatu 25 D 62, 4th floor", "00100 Helsinki"],
           HELSINKI_SITES, "The Nativity of the Theotokos"),
    sacred("fi-helsinki-stefanos-home", "fi-helsinki", "Chapel",
           "Chapel of Saint Stephen at Stefanos Home",
           "Stefanoskodin kappeli, Pyhän Stefanoksen kappeli",
           ["Hallatie 2", "00780 Helsinki"], HELSINKI_SITES,
           "Saint Stephen"),
    sacred("fi-helsinki-sofia-holy-wisdom", "fi-helsinki", "Chapel",
           "Holy Wisdom Chapel at Sofia Cultural Center",
           "Kulttuurikeskus Sofian kappeli, Pyhän Viisauden kappeli",
           ["Kallvikinniementie 35 A", "00980 Helsinki"], HELSINKI_SITES,
           "Holy Wisdom"),
    sacred("fi-helsinki-sofia-saint-maria-paris", "fi-helsinki", "Chapel",
           "Chapel of Saint Maria of Paris at Sofia Cultural Center",
           "Kulttuurikeskus Sofian tsasouna, Pyhän Maria Pariisilaisen "
           "tsasouna", ["Kallvikinniementie 35 D", "00980 Helsinki"],
           HELSINKI_SITES, "Saint Maria of Paris"),
    sacred("fi-helsinki-helena-home-child-martyrs", "fi-helsinki", "Church",
           "Church of the Holy Child Martyrs at Helena Care Home",
           "Hoiva- ja palvelukoti Helenan kirkko, pyhien lapsimarttyyrien "
           "Pistiksen, Elpiksen, Agapen ja heidän äitinsä Sofian kirkko",
           ["Hämeentie 55", "00580 Helsinki"], HELSINKI_SITES,
           "Saints Pistis, Elpis, Agape, and Sophia"),
    sacred("fi-janakkala-lintuvuori-all-athonite-saints", "fi-helsinki",
           "Chapel", "Chapel of All Saints of Mount Athos in Lintuvuori",
           "Lintuvuoren tsasouna, Kaikkien Athosvuoren pyhien tsasouna",
           ["Lammintie 386", "14200 Janakkala"], HELSINKI_SITES,
           "All Saints of Mount Athos"),
    sacred("fi-kirkkonummi-pokrova", "fi-helsinki", "Brotherhood Church",
           "Pokrova Church in Kirkkonummi",
           "Pokrovan kirkko, Jumalanäidin suojeluksen kirkko",
           ["Elfvinginkuja 11", "02420 Kirkkonummi"], HELSINKI_SITES,
           "The Protection of the Mother of God", site="https://pokrova.fi/"),
    sacred("fi-nummela-nativity-theotokos", "fi-helsinki", "Prayer Room",
           "Prayer Room of the Nativity of the Theotokos in Nummela",
           "Nummelan rukoushuone, Jumalansynnyttäjän syntymän rukoushuone",
           ["Naaranpajuntie 7", "03100 Nummela"], HELSINKI_SITES,
           "The Nativity of the Theotokos"),
])

ROWS["fi-helsinki"].extend([
    sacred("fi-turku-saint-alexandra", "fi-turku-parish", "Church",
           "Church of Holy Martyr Empress Alexandra in Turku",
           "Turun Pyhän marttyyrikeisarinna Aleksandran kirkko",
           ["Yliopistonkatu 19", "Turku"], TURKU_SITES,
           "Holy Martyr Empress Alexandra"),
    sacred("fi-turku-cemetery-chapel", "fi-turku-parish",
           "Cemetery Chapel", "Orthodox Cemetery Chapel in Turku",
           "Turun hautausmaan kappeli",
           ["Uudenmaantie 76", "Turku"], TURKU_SITES),
    sacred("fi-rauma-saint-nicholas", "fi-turku-parish", "Prayer Room",
           "Prayer Room of Saint Nicholas in Rauma",
           "Rauman Pyhän Nikolaoksen rukoushuone",
           ["Länsikatu 10", "Rauma"], TURKU_SITES, "Saint Nicholas"),
    sacred("fi-salo-holy-cross", "fi-turku-parish", "Chapel",
           "Chapel of the Holy Cross in Salo", "Salon Pyhän Ristin tsasouna",
           ["Uskelankirkkotie 23", "Salo"], TURKU_SITES, "The Holy Cross"),
    sacred("fi-eura-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Eura",
           "Euran evankelis-luterilainen seurakuntatalo",
           ["Sorkkistentie 3", "Eura"], TURKU_SITES),
    sacred("fi-huittinen-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Huittinen",
           "Huittisten evankelis-luterilainen seurakuntakeskus",
           ["Papintie 1", "Huittinen"], TURKU_SITES),
    sacred("fi-laitila-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Laitila",
           "Laitilan Pyhän Mikaelin kirkko",
           ["Keskuskatu 7", "Laitila"], TURKU_SITES),
    sacred("fi-loimaa-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Loimaa",
           "Loimaan evankelis-luterilainen kaupunginkirkko",
           ["Turuntie 32", "Loimaa"], TURKU_SITES),
    sacred("fi-maarianhamina-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Mariehamn",
           "Margaretagården", ["Måsvägen 4", "Maarianhamina"], TURKU_SITES),
    sacred("fi-paimio-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Paimio",
           "Mikaelintalon kappeli", ["Pyölintie 3", "Paimio"], TURKU_SITES),
    sacred("fi-sauvo-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Sauvo", "Sauvon kirkko",
           ["Sauvontie 50", "Sauvo"], TURKU_SITES),
    sacred("fi-sakyla-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Säkylä",
           "Säkylän evankelis-luterilainen seurakuntatalo",
           ["Tuulimyllyntie 21", "Säkylä"], TURKU_SITES),
    sacred("fi-uusikaupunki-orthodox-worship-site", "fi-turku-parish",
           "Worship Site", "Orthodox Worship Site in Uusikaupunki",
           "Saarniston evankelis-luterilainen seurakuntakoti",
           ["Pajusuontie 2", "Uusikaupunki"], TURKU_SITES),
])

ROWS["fi-helsinki"].extend([
    sacred("fi-lappeenranta-protection-theotokos", "fi-southeast-parish",
           "Church", "Church of the Protection of the Theotokos in Lappeenranta",
           "Lappeenrannan Jumalansynnyttäjän suojeluksen kirkko",
           ["Kristiinankatu 3", "53900 Lappeenranta"], SOUTHEAST_SITES,
           "The Protection of the Theotokos"),
    sacred("fi-imatra-saint-nicholas", "fi-southeast-parish", "Church",
           "Church of Saint Nicholas in Imatra", "Imatran pyhän Nikolaoksen kirkko",
           ["Vuoksenniskantie 3", "55510 Imatra"], SOUTHEAST_SITES,
           "Saint Nicholas"),
    sacred("fi-parikkala-saint-john-baptist", "fi-southeast-parish",
           "Prayer Room", "Prayer Room of Saint John the Baptist in Parikkala",
           "Parikkalan pyhän Johannes Kastajan rukoushuone",
           ["Uimalantie 1", "59100 Parikkala"], SOUTHEAST_SITES,
           "Saint John the Baptist"),
    sacred("fi-koitsanlahti-saints-peter-paul", "fi-southeast-parish",
           "Prayer Room", "Prayer Room of Saints Peter and Paul in Koitsanlahti",
           "Koitsanlahden pyhien apostolien Pietarin ja Paavalin rukoushuone",
           ["Syrjärinteentie", "Koitsanlahti", "Parikkala"],
           SOUTHEAST_SITES, "Saints Peter and Paul"),
    sacred("fi-kouvola-exaltation-cross", "fi-southeast-parish", "Church",
           "Church of the Exaltation of the Cross in Kouvola",
           "Kouvolan pyhän ristin ylentämisen kirkko",
           ["Kirkonmäenkatu 2", "Kouvola"], SOUTHEAST_KOUVOLA,
           "The Exaltation of the Holy Cross"),
    sacred("fi-hamina-saints-peter-paul", "fi-southeast-parish", "Church",
           "Church of Saints Peter and Paul in Hamina",
           "Haminan pyhien apostolien Pietarin ja Paavalin kirkko",
           ["Raatihuoneentori 2", "Hamina"], SOUTHEAST_KOUVOLA,
           "Saints Peter and Paul"),
    sacred("fi-myllykoski-theotokos", "fi-southeast-parish", "Chapel",
           "Chapel of the Mother of God in Myllykoski",
           "Myllykosken Jumalansynnyttäjän muistolle pyhitetty tsasouna",
           ["Koulutie 4", "Kouvola"], SOUTHEAST_KOUVOLA,
           "The Mother of God"),
    sacred("fi-hamina-cemetery-joy-all-sorrow", "fi-southeast-parish",
           "Cemetery Church", "Church of the Joy of All Who Sorrow in Hamina",
           "Haminan hautausmaan kirkko, Kaikkien murheellisten ilo -ikonin kirkko",
           ["Hirveläntie 22", "Hamina"], SOUTHEAST_KOUVOLA,
           "The Joy of All Who Sorrow Icon of the Mother of God"),
    sacred("fi-kotka-saint-nicholas", "fi-southeast-parish", "Church",
           "Church of Saint Nicholas in Kotka", "Kotkan Pyhän Nikolaoksen kirkko",
           ["Isopuisto", "48100 Kotka"], SOUTHEAST_KOTKA, "Saint Nicholas"),
    sacred("fi-loviisa-kazan-icon", "fi-southeast-parish", "Church",
           "Church of the Kazan Icon of the Mother of God in Loviisa",
           "Loviisan Jumalanäidin Kasanilaisen ikonin kirkko",
           ["Itäinen Tullikatu 17", "Loviisa"], SOUTHEAST_KOTKA,
           "The Kazan Icon of the Mother of God"),
])

ROWS["fi-kuopio"].extend([
    sacred("fi-kuopio-saint-nicholas-cathedral", "fi-kuopio-parish",
           "Cathedral", "Cathedral of Saint Nicholas in Kuopio",
           "Pyhän Nikolaoksen katedraali",
           ["Sepänkatu 7", "70100 Kuopio"], KUOPIO_SITES, "Saint Nicholas"),
    sacred("fi-iisalmi-prophet-elijah", "fi-kuopio-parish", "Church",
           "Church of the Prophet Elijah in Iisalmi", "Profeetta Elian kirkko",
           ["Kirkkopuistonkatu 28", "74100 Iisalmi"], KUOPIO_SITES,
           "The Prophet Elijah"),
    sacred("fi-siilinjarvi-saint-george", "fi-kuopio-parish", "Church",
           "Church of Great Martyr George in Siilinjärvi",
           "Suurmarttyyri Georgios Voittajan kirkko",
           ["Harjamäentie 2", "71800 Siilinjärvi"], KUOPIO_SITES,
           "Great Martyr George the Victory-Bearer"),
    sacred("fi-pyhasalmi-prophet-elijah", "fi-kuopio-parish", "Prayer Room",
           "Prayer Room of the Prophet Elijah in Pyhäsalmi",
           "Pyhän Profeetta Elian rukoushuone",
           ["Vesitornintie 15", "86800 Pyhäsalmi"], KUOPIO_SITES,
           "The Prophet Elijah"),
    sacred("fi-salahmi-saint-nicholas", "fi-kuopio-parish", "Chapel",
           "Chapel of Saint Nicholas in Salahmi", "Pyhän Nikolaoksen tsasouna",
           ["Latokankaantie 83", "74230 Salahmi"], KUOPIO_SITES,
           "Saint Nicholas"),
    sacred("fi-muuruvesi-saint-nicholas", "fi-kuopio-parish", "Chapel",
           "Chapel of Saint Nicholas in Muuruvesi", "Pyhän Nikolaoksen tsasouna",
           ["Kumpuniementie 1", "73460 Muuruvesi"], KUOPIO_SITES,
           "Saint Nicholas"),
    sacred("fi-rautalampi-saint-nicholas", "fi-kuopio-parish", "Church",
           "Church of Saint Nicholas in Rautalampi", "Pyhän Nikolaoksen kirkko",
           ["Nikolaoksentie 1", "77700 Rautalampi"], KUOPIO_SITES,
           "Saint Nicholas"),
    sacred("fi-kiuruvesi-saint-nicholas", "fi-kuopio-parish", "Church",
           "Church of Saint Nicholas in Kiuruvesi", "Pyhän Nikolaoksen kirkko",
           ["Niemistenkatu 6", "74700 Kiuruvesi"], KUOPIO_SITES,
           "Saint Nicholas"),
    sacred("fi-alapitka-holy-trinity", "fi-kuopio-parish", "Chapel",
           "Holy Trinity Chapel in Alapitkä", "Pyhän Kolminaisuuden tsasouna",
           ["Alapitkäntie 14", "71910 Alapitkä"], KUOPIO_SITES,
           "The Holy Trinity"),
    sacred("fi-vesanto-nativity-saint-john", "fi-kuopio-parish", "Chapel",
           "Chapel of the Nativity of Saint John the Baptist in Vesanto",
           "Pyhän Johannes Kastajan syntymän tsasouna",
           ["Koulutie 6", "72300 Vesanto"], KUOPIO_SITES,
           "The Nativity of Saint John the Baptist"),
    sacred("fi-nilsia-saint-john-baptist", "fi-kuopio-parish", "Church",
           "Church of Saint John the Baptist in Nilsiä",
           "Pyhän Johannes Kastajan kirkko",
           ["Laitisenmäentie 1", "73300 Nilsiä"], KUOPIO_SITES,
           "Saint John the Baptist"),
    sacred("fi-vehmersalmi-saint-herman-alaska", "fi-kuopio-parish", "Chapel",
           "Chapel of Saint Herman of Alaska in Vehmersalmi",
           "Pyhän Herman Alaskalaisen tsasouna",
           ["Lepokiventie 147", "71310 Vehmersalmi"], KUOPIO_SITES,
           "Saint Herman of Alaska"),
    sacred("fi-haapavesi-nativity-theotokos", "fi-kuopio-parish",
           "Prayer Room", "Prayer Room of the Nativity of the Theotokos in Haapavesi",
           "Neitsyt Marian syntymän rukoushuone",
           ["Kytökyläntie 724", "86650 Kytökylä"], KUOPIO_SITES,
           "The Nativity of the Theotokos"),
    sacred("fi-kaarmelahti-transfiguration", "fi-kuopio-parish", "Chapel",
           "Chapel of the Transfiguration in Käärmelahti",
           "Kristuksen kirkastumisen tsasouna",
           ["Hyttiläntie 27", "71730 Kinnulanlahti"], KUOPIO_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-suonenjoki-transfiguration", "fi-kuopio-parish", "Church",
           "Church of the Transfiguration in Suonenjoki",
           "Kristuksen kirkastumisen kirkko",
           ["Herralantie 120", "77600 Suonenjoki"], KUOPIO_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-karvoskyla-transfiguration", "fi-kuopio-parish", "Church",
           "Church of the Transfiguration in Karvoskylä",
           "Kristuksen kirkastumisen kirkko",
           ["Jokikyläntie 7", "85580 Nivala"], KUOPIO_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-maaninka-enlighteners-karelia", "fi-kuopio-parish", "Church",
           "Church of the Enlighteners of Karelia in Maaninka",
           "Karjalan valistajien kirkko",
           ["Pihtisalmentie 120", "71750 Maaninka"], KUOPIO_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-lapinlahti-all-saints", "fi-kuopio-parish", "Church",
           "Church of All Saints in Lapinlahti", "Kaikkien pyhien kirkko",
           ["Pekka Halosentie 18", "73100 Lapinlahti"], KUOPIO_SITES,
           "All Saints"),
    sacred("fi-juankoski-protection-theotokos", "fi-kuopio-parish", "Church",
           "Church of the Protection of the Theotokos in Juankoski",
           "Jumalansynnyttäjän suojeluksen kirkko",
           ["Kaavintie 59", "73500 Juankoski"], KUOPIO_SITES,
           "The Protection of the Theotokos"),
    sacred("fi-vuorela-dormition-theotokos", "fi-kuopio-parish", "Chapel",
           "Chapel of the Dormition of the Theotokos in Vuorela",
           "Jumalansynnyttäjän kuolonuneen nukkumisen tsasouna",
           ["Kivitie 21", "70910 Vuorela"], KUOPIO_SITES,
           "The Dormition of the Theotokos"),
    sacred("fi-sonkajarvi-dormition-theotokos", "fi-kuopio-parish", "Chapel",
           "Chapel of the Dormition of the Theotokos in Sonkajärvi",
           "Jumalansynnyttäjän kuolonuneen nukkumisen tsasouna",
           ["Lepokankaantie 6", "74300 Sonkajärvi"], KUOPIO_SITES,
           "The Dormition of the Theotokos"),
    sacred("fi-sukeva-saints-peter-paul", "fi-kuopio-parish", "Chapel",
           "Chapel of Saints Peter and Paul in Sukeva",
           "Apostolien Pietarin ja Paavalin tsasouna",
           ["Vankilantie 52 A", "74340 Sukeva"], KUOPIO_SITES,
           "Saints Peter and Paul"),
    sacred("fi-tuusniemi-saints-peter-paul", "fi-kuopio-parish", "Church",
           "Church of Saints Peter and Paul in Tuusniemi",
           "Apostolien Pietarin ja Paavalin kirkko",
           ["Keskitie 54", "71200 Tuusniemi"], KUOPIO_SITES,
           "Saints Peter and Paul"),
    sacred("fi-keitele-saint-arsenius-konevsky", "fi-kuopio-parish", "Church",
           "Church of Saint Arsenius of Konevsky in Keitele",
           "Pyhittäjä Arseni Konevitsalaisen kirkko",
           ["Arsenintie 1", "72600 Keitele"], KUOPIO_SITES,
           "Saint Arsenius of Konevsky"),
    sacred("fi-pielavesi-saints-peter-paul", "fi-kuopio-parish", "Church",
           "Church of Saints Peter and Paul in Pielavesi",
           "Apostolien Pietarin ja Paavalin kirkko",
           ["Puistotie 2", "72400 Pielavesi"], KUOPIO_SITES,
           "Saints Peter and Paul"),
    sacred("fi-karttula-archangel-michael", "fi-kuopio-parish", "Prayer Room",
           "Prayer Room of Archangel Michael in Karttula",
           "Ylienkeli Mikaelin rukoushuone",
           ["Mihailantie 8", "71570 Syvänniemi"], KUOPIO_SITES,
           "Archangel Michael"),
    sacred("fi-tervo-prophet-elijah", "fi-kuopio-parish", "Prayer Room",
           "Prayer Room of the Prophet Elijah in Tervo",
           "Pyhän profeetta Elian rukoushuone",
           ["Kirkkotie 9", "72210 Tervo"], KUOPIO_SITES,
           "The Prophet Elijah"),
])

ROWS["fi-oulu"].extend([
    sacred("fi-oulu-holy-trinity-cathedral", "fi-northern-parish",
           "Cathedral", "Holy Trinity Cathedral in Oulu",
           "Pyhän Kolminaisuuden katedraali",
           ["Torikatu 74", "90120 Oulu"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/OULU/",
           "The Holy Trinity"),
    sacred("fi-kemi-nativity-saint-john", "fi-northern-parish", "Church",
           "Church of the Nativity of Saint John the Baptist in Kemi",
           "Pyhän Johannes Kastajan syntymän kirkko",
           ["Lehtokatu 31", "Kemi"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/KEMI/",
           "The Nativity of Saint John the Baptist"),
    sacred("fi-tornio-saints-peter-paul", "fi-northern-parish", "Church",
           "Church of Saints Peter and Paul in Tornio",
           "Pyhien apostolien Pietarin ja Paavalin kirkko",
           ["Lukiokatu 1", "Tornio"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/TORNIO/",
           "Saints Peter and Paul"),
    sacred("fi-varejoki-saint-tryphon", "fi-northern-parish",
           "Prayer Room", "Prayer Room of Saint Tryphon of Petsamo in Varejoki",
           "Pyhittäjä Trifon Petsamolaisen rukoushuone",
           ["Tsasounantie 34", "Tervola"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/VAREJOKI/",
           "Saint Tryphon of Petsamo"),
    sacred("fi-vihanti-protection-theotokos", "fi-northern-parish",
           "Prayer Room", "Prayer Room of the Protection of the Theotokos in Vihanti",
           "Jumalansynnyttäjän suojeluksen rukoushuone",
           ["Vanha Ouluntie 26", "Vihanti"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/VIHANTI/",
           "The Protection of the Theotokos"),
    sacred("fi-muhos-ankkuri-worship-site", "fi-northern-parish",
           "Worship Site", "Orthodox Worship Site at Ankkuri in Muhos",
           "Toimintakeskus Ankkuri",
           ["Valtatie 17", "Muhos"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/MUHOS/"),
    sacred("fi-muhos-koortila-worship-site", "fi-northern-parish",
           "Worship Site", "Orthodox Worship Site at Koortila in Muhos",
           "Koortilan toimintakeskus",
           ["Koortilantie 30", "Muhos"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/MUHOS/"),
    sacred("fi-vaala-orthodox-worship-site", "fi-northern-parish",
           "Worship Site", "Orthodox Worship Site in Vaala",
           "Vaalan evankelis-luterilainen kirkko",
           ["Järvikyläntie 3", "Vaala"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/MUHOS/"),
    sacred("fi-kalajoki-saint-nicholas", "fi-northern-parish",
           "Prayer Room", "Prayer Room of Saint Nicholas in Kalajoki",
           "Pyhän Nikolaos Ihmeidentekijän rukoushuone",
           ["Matkailutie 249", "Kalajoki"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/KALAJOKI/",
           "Saint Nicholas the Wonderworker"),
    sacred("fi-kuusamo-orthodox-worship-site", "fi-northern-parish",
           "Worship Site", "Orthodox Worship Site in Kuusamo",
           "Evankelis-luterilaisen seurakuntatalon takkahuone",
           ["Kirkkotie 1 B", "Kuusamo"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/KUUSAMO/"),
    sacred("fi-raahe-pattijoki-worship-site", "fi-northern-parish",
           "Worship Site", "Orthodox Worship Site at Pattijoki Rectory",
           "Pattijoen pappila",
           ["Koulutie 8", "Pattijoki"],
           "https://pohjoissuomenortodoksinenseurakunta.fi/JUMALANPALVELUKSET/RAAHE/"),
    sacred("fi-rovaniemi-saint-andrew", "fi-lapland-chapel-parish", "Church",
           "Church of Saint Andrew the Apostle in Rovaniemi",
           "Pyhän apostoli Andreaksen kirkko",
           ["Ounasvaarantie 16", "96400 Rovaniemi"], LAPLAND_SITES,
           "Saint Andrew the Apostle"),
    sacred("fi-nellim-holy-trinity-saint-tryphon", "fi-lapland-chapel-parish",
           "Church", "Church of the Holy Trinity and Saint Tryphon in Nellim",
           "Pyhän Kolminaisuuden ja pyhän pyhittäjä Trifon Petsamolaisen kirkko",
           ["Siikajärventie 64 A", "99860 Nellim"], LAPLAND_SITES,
           "The Holy Trinity and Saint Tryphon of Petsamo"),
    sacred("fi-ivalo-saint-nicholas", "fi-lapland-chapel-parish", "Church",
           "Church of Saint Nicholas in Ivalo",
           "Pyhän esipaimen Nikolaoksen kirkko",
           ["Rantatie 22", "99800 Ivalo"], LAPLAND_SITES,
           "Saint Nicholas"),
    sacred("fi-sevettijarvi-saint-tryphon", "fi-lapland-chapel-parish", "Church",
           "Church of Saint Tryphon of Petsamo in Sevettijärvi",
           "Pyhän pyhittäjä Trifon Petsamolaisen kirkko",
           ["Sevettijärventie 9065", "99930 Sevettijärvi"], LAPLAND_SITES,
           "Saint Tryphon of Petsamo"),
    sacred("fi-kevajarvi-saints-boris-gleb", "fi-lapland-chapel-parish", "Chapel",
           "Chapel of Saints Boris and Gleb in Keväjärvi",
           "Pyhien Boriksen ja Glebin tsasouna",
           ["Siskelintie", "99800 Ivalo"], LAPLAND_SITES,
           "Saints Boris and Gleb"),
    sacred("fi-kajaani-transfiguration", "fi-kainuu-chapel-parish", "Church",
           "Church of the Transfiguration in Kajaani",
           "Kristuksen kirkastumisen kirkko",
           ["Kirkkokatu 17a", "Kajaani"], KAINUU_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-sotkamo-protection-theotokos", "fi-kainuu-chapel-parish", "Church",
           "Church of the Protection of the Theotokos in Sotkamo",
           "Jumalansynnyttäjän suojeluksen kirkko",
           ["Rauhantie 13", "Sotkamo"], KAINUU_SITES,
           "The Protection of the Theotokos"),
    sacred("fi-kuhmo-enlighteners-karelia", "fi-kainuu-chapel-parish", "Church",
           "Church of the Enlighteners of Karelia in Kuhmo",
           "Karjalan valistajien kirkko",
           ["Koulukatu 47", "Kuhmo"], KAINUU_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-ammasaari-holy-cross", "fi-kainuu-chapel-parish", "Chapel",
           "Chapel of the Holy Cross in Ämmänsaari",
           "Pyhän Ristin tsasouna",
           ["Keskuskatu 1", "Ämmänsaari"], KAINUU_SITES,
           "The Holy Cross"),
    sacred("fi-kuivajarvi-saint-nicholas", "fi-kainuu-chapel-parish",
           "Prayer Room", "Prayer Room of Saint Nicholas in Kuivajärvi",
           "Pyhän Nikolauksen rukoushuone",
           ["Kuivajärventie 196", "Kuivajärvi"], KAINUU_SITES,
           "Saint Nicholas"),
    sacred("fi-kirkkoaho-saint-lazarus", "fi-kainuu-chapel-parish", "Chapel",
           "Chapel of Saint Lazarus of Murom in Kirkkoaho",
           "Pyhittäjä Lasari Muromalaisen tsasouna",
           ["Kirkkoahontie 633", "Kajaani"], KAINUU_SITES,
           "Saint Lazarus of Murom"),
    sacred("fi-tampere-saints-alexander-nicholas", "fi-tampere-parish", "Church",
           "Church of Saints Alexander Nevsky and Nicholas in Tampere",
           "Pyhän Aleksanteri Nevalaisen ja pyhän Nikolaoksen kirkko",
           ["Tuomiokirkonkatu 27", "33100 Tampere"], TAMPERE_SITES,
           "Saints Alexander Nevsky and Nicholas"),
    sacred("fi-kolho-enlighteners-karelia", "fi-tampere-parish", "Church",
           "Church of the Enlighteners of Karelia in Kolho",
           "Karjalan valistajien kirkko",
           ["Kappelitie 8", "35990 Kolho"], TAMPERE_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-valkeakoski-saint-nicholas", "fi-tampere-parish", "Chapel",
           "Chapel of Saint Nicholas in Valkeakoski",
           "Pyhän Nikolaoksen tšasouna",
           ["Kalmistonkatu 8", "37600 Valkeakoski"], TAMPERE_SITES,
           "Saint Nicholas"),
    sacred("fi-tampere-kalliosalmi-worship-site", "fi-tampere-parish",
           "Worship Site", "Orthodox Worship Site at Kalliosalmi Camp Center",
           "Kalliosalmen leirikeskus",
           ["Salmenkalliontie 86", "33720 Tampere"], TAMPERE_SITES),
    sacred("fi-pori-saint-john-theologian", "fi-tampere-parish", "Church",
           "Church of Saint John the Theologian in Pori",
           "Apostoli Johannes Teologin kirkko",
           ["Maantiekatu 46", "28120 Pori"], TAMPERE_SITES,
           "Saint John the Theologian"),
    sacred("fi-ylojarvi-saint-john-russian", "fi-tampere-parish", "Chapel",
           "Chapel of Saint John the Russian in Ylöjärvi",
           "Pyhän Johannes Venäläisen tšasouna",
           ["Nopanperäntie 586", "39310 Ylöjärvi"], TAMPERE_SITES,
           "Saint John the Russian"),
    sacred("fi-vaasa-saint-nicholas", "fi-vaasa-chapel-parish", "Church",
           "Church of Saint Nicholas in Vaasa", "Pyhän Nikolaoksen kirkko",
           ["Nikolainkuja 1", "65100 Vaasa"], VAASA_SITES,
           "Saint Nicholas"),
    sacred("fi-kokkola-saints-simeon-anna", "fi-vaasa-chapel-parish",
           "Prayer Room", "Prayer Room of Saints Simeon and Anna in Kokkola",
           "Pyhän Simeonin ja Hannan rukoushuone",
           ["Katariinankatu 3", "67100 Kokkola"], VAASA_SITES,
           "Saints Simeon and Anna"),
    sacred("fi-pietarsaari-prophet-elijah-saint-anna", "fi-vaasa-chapel-parish",
           "Prayer Room", "Prayer Room of the Prophet Elijah and Saint Anna in Pietarsaari",
           "Pyhien Eliaan ja vanhurskaan Annan rukoushuone",
           ["Narsinkatu 2", "68600 Pietarsaari"], VAASA_SITES,
           "The Prophet Elijah and Saint Anna"),
    sacred("fi-lapua-saint-seraphim", "fi-vaasa-chapel-parish", "Prayer Room",
           "Prayer Room of Saint Seraphim of Sarov in Lapua",
           "Pyhittäjä Serafim Sarovilaisen rukoushuone",
           ["Koulukatu 7", "62100 Lapua"], VAASA_SITES,
           "Saint Seraphim of Sarov"),
    sacred("fi-seinajoki-protection-theotokos", "fi-vaasa-chapel-parish",
           "Prayer Room", "Prayer Room of the Protection of the Theotokos in Seinäjoki",
           "Jumalanäidin suojeluksen rukoushuone",
           ["Päivölänkatu 32", "60120 Seinäjoki"], VAASA_SITES,
           "The Protection of the Theotokos"),
])

ROWS["russia"] = [
    dict(id="fi-mp-patriarchal-parishes", parent="russia",
         kind="diocese", rank="Patriarchal Parishes",
         name="Patriarchal Parishes in Finland",
         local="Патриаршие приходы в Финляндии", country="FI",
         sources=[MOSCOW_FINLAND, MOSCOW_CALENDAR]),
    dict(id="fi-mp-helsinki-protection", parent="fi-mp-patriarchal-parishes",
         kind="parish", rank="Parish",
         name="Parish of the Protection of the Theotokos in Helsinki",
         local="Приход Покрова Пресвятой Богородицы в Хельсинки",
         country="FI", dedication="The Protection of the Theotokos",
         address=["Tiilimäki 25", "00330 Helsinki"],
         site="http://finland.orthodoxy.ru",
         sources=[MOSCOW_CALENDAR, MOSCOW_FINLAND]),
    dict(id="fi-mp-helsinki-saint-nicholas", parent="fi-mp-patriarchal-parishes",
         kind="parish", rank="Parish",
         name="Saint Nicholas Orthodox Parish in Helsinki",
         local="Ortodoksinen Pyhän Nikolauksen seurakunta Helsingissä",
         country="FI", dedication="Saint Nicholas the Wonderworker",
         address=["Tuonelankuja 3", "00100 Helsinki"],
         site=SAINT_NICHOLAS,
         founded=["The parish was founded in 1927."],
         sources=[MOSCOW_CALENDAR, SAINT_NICHOLAS, SAINT_NICHOLAS_CONTACT]),
    dict(id="fi-mp-helsinki-blessed-xenia",
         parent="fi-mp-helsinki-saint-nicholas", kind="parish", rank="Church",
         name="Church of Blessed Xenia of Saint Petersburg in Helsinki",
         local="Pyhän Ksenia Pietarilaisen kirkko", country="FI",
         dedication="Blessed Xenia of Saint Petersburg",
         address=["Aarteenetsijäntie 2", "00970 Helsinki"],
         site=SAINT_NICHOLAS,
         sources=[SAINT_NICHOLAS, SAINT_NICHOLAS_CONTACT]),
    dict(id="fi-mp-turku-dormition", parent="fi-mp-patriarchal-parishes",
         kind="parish", rank="Church",
         name="Church of the Dormition in Turku",
         local="Успенский храм в Турку", country="FI",
         dedication="The Dormition of the Theotokos",
         address=["Vartiovuorenkatu 2", "20700 Turku"],
         sources=[MOSCOW_CALENDAR]),
]


SHARED_MULTI_COUNTRY_PARENTS = frozenset({"russia"})
LOCAL_PAYLOAD_PARENTS = ("fi-helsinki", "fi-kuopio", "fi-oulu")

EXPECTED = {
    "fi-helsinki": 57,
    "fi-kuopio": 113,
    "fi-oulu": 38,
    "russia": 5,
}

ROWS["fi-kuopio"].extend([
    sacred("fi-joensuu-saint-nicholas", "fi-joensuu-parish", "Church",
           "Church of Saint Nicholas in Joensuu",
           "Joensuun Pyhän Nikolaoksen kirkko",
           ["Kirkkokatu 32", "80100 Joensuu"], JOENSUU_SITES,
           "Saint Nicholas"),
    sacred("fi-joensuu-kuhasalo-icon-shelter", "fi-joensuu-parish",
           "Icon Shelter", "Icon Shelter at Kuhasalo Cemetery",
           "Kuhasalon kalmiston ikonikatos",
           ["Luostarintie", "80220 Joensuu"], JOENSUU_SITES),
    sacred("fi-joensuu-cemetery-holy-cross", "fi-joensuu-parish",
           "Cemetery Chapel", "Holy Cross Chapel at Joensuu Cemetery",
           "Hautausmaan Pyhän ristin tsasouna",
           ["Nurmeksentie 1", "80100 Joensuu"], JOENSUU_SITES,
           "The Holy Cross"),
    sacred("fi-joensuu-seminary-saint-john-theologian", "fi-joensuu-parish",
           "Seminary Church", "Church of Saint John the Theologian in Joensuu",
           "Pyhän Johannes Teologin kirkko",
           ["Torikatu 41", "80100 Joensuu"], JOENSUU_SITES,
           "Saint John the Theologian"),
    sacred("fi-kontiolahti-ascension", "fi-joensuu-parish", "Church",
           "Church of the Ascension in Kontiolahti",
           "Kontiolahden Kristuksen taivaaseenastumisen kirkko",
           ["Keskuskatu 53", "81100 Kontiolahti"], JOENSUU_SITES,
           "The Ascension of Christ"),
    sacred("fi-eno-transfiguration", "fi-joensuu-parish", "Chapel",
           "Chapel of the Transfiguration in Eno",
           "Enon Kristuksen kirkastumisen tsasouna",
           ["Tornitie 8", "81200 Eno"], JOENSUU_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-heinavaara-not-made-by-hands", "fi-joensuu-parish", "Chapel",
           "Chapel of the Icon Not Made by Hands in Heinävaara",
           "Heinävaaran Kristuksen käsittätehdyn ikonin tsasouna",
           ["Heinävaarantie 140", "82110 Heinävaara"], JOENSUU_SITES,
           "The Icon of Christ Not Made by Hands"),
    sacred("fi-sikrenvaara-enlighteners-karelia", "fi-joensuu-parish",
           "Chapel", "Chapel of the Enlighteners of Karelia in Sikrenvaara",
           "Sikrenvaaran Pyhien Karjalan valistajien kappeli",
           ["Koveronvaarantie 2", "81320 Kuismavaara"], JOENSUU_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-kitee-holy-trinity", "fi-joensuu-parish", "Church",
           "Holy Trinity Church in Kitee", "Kiteen Pyhän Kolminaisuuden kirkko",
           ["Valamontie 4", "82500 Kitee"], JOENSUU_SITES,
           "The Holy Trinity"),
    sacred("fi-honkavaara-saint-john-baptist", "fi-joensuu-parish", "Chapel",
           "Chapel of Saint John the Baptist in Honkavaara",
           "Honkavaaran Pyhän Johannes Kastajan tsasouna",
           ["Rekivaarantie 24", "82200 Hammaslahti"], JOENSUU_SITES,
           "Saint John the Baptist"),
    sacred("fi-lieksa-prophet-elijah", "fi-joensuu-parish", "Church",
           "Church of the Prophet Elijah in Lieksa",
           "Lieksan Pyhän profeetta Elian kirkko",
           ["Iljankatu 14", "81700 Lieksa"], JOENSUU_SITES,
           "The Prophet Elijah"),
    sacred("fi-lieksa-kirkkopuisto-transfiguration", "fi-joensuu-parish",
           "Chapel", "Chapel of the Transfiguration in Lieksa Church Park",
           "Kirkkopuiston Kristuksen kirkastumisen tsasouna",
           ["Lieksan kirkkopuisto", "Lieksa"], JOENSUU_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-vuonisjarvi-dormition-theotokos", "fi-joensuu-parish",
           "Chapel", "Chapel of the Dormition of the Theotokos in Vuonisjärvi",
           "Vuonisjärven Jumalansynnyttäjän kuolonuneen nukkumisen tsasouna",
           ["Kylätie 5", "Vuonisjärvi"], JOENSUU_SITES,
           "The Dormition of the Theotokos"),
    sacred("fi-viekijarvi-saint-nicholas", "fi-joensuu-parish", "Chapel",
           "Chapel of Saint Nicholas in Viekijärvi",
           "Viekijärven Pyhän Nikolaoksen tsasouna",
           ["Kannelkoskentie 3", "Viekijärvi"], JOENSUU_SITES,
           "Saint Nicholas"),
    sacred("fi-lontsinniemi-konevitsa-icon", "fi-joensuu-parish", "Chapel",
           "Chapel of the Konevitsa Icon of the Mother of God in Lontsinniemi",
           "Lontsinniemen Konevitsalaisen Jumalanäidin ikonin tsasouna",
           ["Viensuuntie", "81820 Kylänlahti"], JOENSUU_SITES,
           "The Konevitsa Icon of the Mother of God"),
    sacred("fi-konttinen-archangel-gabriel", "fi-joensuu-parish", "Chapel",
           "Chapel of Archangel Gabriel in Konttinen",
           "Konttisen Pyhän ylienkeli Gabrielin tsasouna",
           ["Konttisentie 13 b", "81700 Lieksa"], JOENSUU_SITES,
           "Archangel Gabriel"),
    sacred("fi-sonkajanranta-saint-anna", "fi-joensuu-parish", "Church",
           "Church of Saint Anna in Sonkajanranta",
           "Sonkajanrannan Pyhän Hannan kirkko",
           ["Kirkkotuvantie 3", "82815 Sonkajanranta"], JOENSUU_SITES,
           "Saint Anna"),
    sacred("fi-hoilola-saint-nicholas", "fi-joensuu-parish", "Church",
           "Church of Saint Nicholas in Hoilola",
           "Hoilolan Pyhän Nikolaoksen kirkko",
           ["Tsiikontie 6a", "82760 Hoilola"], JOENSUU_SITES,
           "Saint Nicholas"),
    sacred("fi-saarivaara-transfiguration", "fi-joensuu-parish", "Chapel",
           "Chapel of the Transfiguration in Saarivaara",
           "Saarivaaran Kristuksen kirkastumisen tsasouna",
           ["Hoilolantie 42", "82769 Joensuu"], JOENSUU_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-tuupovaara-not-made-by-hands", "fi-joensuu-parish", "Chapel",
           "Chapel of the Icon Not Made by Hands in Tuupovaara",
           "Tuupovaaran Kristuksen käsittätehdyn ikonin kappeli",
           ["Lähdetie 1", "82730 Tuupovaara"], JOENSUU_SITES,
           "The Icon of Christ Not Made by Hands"),
    sacred("fi-kovero-saint-herman-alaska", "fi-joensuu-parish", "Chapel",
           "Chapel of Saint Herman of Alaska in Kovero",
           "Koveron Pyhittäjä Herman Alaskalaisen tsasouna",
           ["Töriseväntie 1", "82710 Kovero"], JOENSUU_SITES,
           "Saint Herman of Alaska"),
    sacred("fi-valkeavaara-saint-george", "fi-joensuu-parish", "Chapel",
           "Chapel of Saint George in Valkeavaara",
           "Pyhän Georgios Voittajan tsasouna",
           ["Vatalantie", "82140 Kiihtelysvaara"], JOENSUU_SITES,
           "Saint George the Victory-Bearer"),
    sacred("fi-ilomantsi-prophet-elijah", "fi-ilomantsi-chapel-parish",
           "Church", "Church of the Prophet Elijah in Ilomantsi",
           "Pyhän profeetta Elian kirkko",
           ["Kirkkotie 15", "82900 Ilomantsi"], JOENSUU_SITES,
           "The Prophet Elijah"),
    sacred("fi-mutalahti-nativity-theotokos", "fi-ilomantsi-chapel-parish",
           "Chapel", "Chapel of the Nativity of the Theotokos in Mutalahti",
           "Mutalahden Neitsyt Marian syntymän tsasouna",
           ["Mutalahdentie 238", "82900 Mutalahti"], JOENSUU_SITES,
           "The Nativity of the Theotokos"),
    sacred("fi-hattuvaara-saints-peter-paul", "fi-ilomantsi-chapel-parish",
           "Chapel", "Chapel of Saints Peter and Paul in Hattuvaara",
           "Hattuvaaran Pyhien Pietarin ja Paavalin tsasouna",
           ["Hattujärventie 1", "82967 Hattuvaara"], JOENSUU_SITES,
           "Saints Peter and Paul"),
    sacred("fi-sonkaja-holy-cross", "fi-ilomantsi-chapel-parish", "Chapel",
           "Chapel of the Holy Cross in Sonkaja",
           "Sonkajan Pyhän ristin tsasouna",
           ["Issakantie 115", "82915 Sonkaja"], JOENSUU_SITES,
           "The Holy Cross"),
    sacred("fi-huhus-ascension", "fi-ilomantsi-chapel-parish", "Chapel",
           "Chapel of the Ascension in Huhus",
           "Huhuksen Kristuksen taivaaseenastumisen tsasouna",
           ["Huhuksentie 33", "82900 Ilomantsi"], JOENSUU_SITES,
           "The Ascension of Christ"),
    sacred("fi-parppeinvaara-all-saints", "fi-ilomantsi-chapel-parish",
           "Chapel", "Chapel of All Saints in Parppeinvaara",
           "Parppeinvaaran Kaikkien pyhien tsasouna",
           ["Parppeintie 4c", "82900 Ilomantsi"], JOENSUU_SITES,
           "All Saints"),
])

ROWS["fi-kuopio"].extend([
    sacred("fi-jyvaskyla-resurrection", "fi-jyvaskyla-parish", "Church",
           "Church of the Resurrection in Jyväskylä",
           "Kristuksen ylösnousemuksen kirkko",
           ["Rajakatu 39", "40200 Jyväskylä"], JYVASKYLA_SITES,
           "The Resurrection of Christ"),
    sacred("fi-karstula-nativity-theotokos", "fi-jyvaskyla-parish", "Chapel",
           "Chapel of the Nativity of the Theotokos in Karstula",
           "Karstulan Jumalansynnyttäjän syntymän tsasouna",
           ["Tsasounantie 1", "43500 Karstula"], JYVASKYLA_SITES,
           "The Nativity of the Theotokos"),
    sacred("fi-lievestuore-saint-nicholas", "fi-jyvaskyla-parish",
           "Prayer Room", "Prayer Room of Saint Nicholas in Lievestuore",
           "Lievestuoreen pyhän Nikolaoksen rukoushuone",
           ["Mäkikalliontie 11", "41400 Lievestuore"], JYVASKYLA_SITES,
           "Saint Nicholas"),
    sacred("fi-saarijarvi-saint-arsenius-konevsky", "fi-jyvaskyla-parish",
           "Chapel", "Chapel of Saint Arsenius of Konevsky in Saarijärvi",
           "Saarijärven pyhittäjä Arseni Konevitsalaisen tsasouna",
           ["Matosalmentie 1", "43100 Saarijärvi"], JYVASKYLA_SITES,
           "Saint Arsenius of Konevsky"),
    sacred("fi-suolahti-archangel-michael", "fi-jyvaskyla-parish", "Chapel",
           "Chapel of Archangel Michael in Suolahti",
           "Suolahden ylienkeli Mikaelin tsasouna",
           ["Harjusenkatu 41", "44200 Suolahti"], JYVASKYLA_SITES,
           "Archangel Michael"),
    sacred("fi-viitasaari-transfiguration", "fi-jyvaskyla-parish", "Chapel",
           "Chapel of the Transfiguration in Viitasaari",
           "Viitasaaren Kristuksen kirkastumisen tsasouna",
           ["Kirkkotie 12", "44500 Viitasaari"], JYVASKYLA_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-aanekoski-dormition-theotokos", "fi-jyvaskyla-parish",
           "Chapel", "Chapel of the Dormition of the Theotokos in Äänekoski",
           "Äänekosken Jumalansynnyttäjän kuolonuneen nukkumisen tsasouna",
           ["Palokuja 2", "44100 Äänekoski"], JYVASKYLA_SITES,
           "The Dormition of the Theotokos"),
    sacred("fi-pyhakangas-exaltation-cross", "fi-jyvaskyla-parish",
           "Camp Chapel", "Chapel of the Exaltation of the Cross at Pyhäkangas",
           "Pyhäkankaan leirikeskuksen Ristin ylentämisen kappeli",
           ["Pölykankaantie 279", "41290 Kangashäkki"], JYVASKYLA_SITES,
           "The Exaltation of the Holy Cross"),
])

ROWS["fi-kuopio"].extend([
    sacred("fi-viinijarvi-tikhvin-icon", "fi-taipale-parish", "Church",
           "Church of the Tikhvin Icon of the Mother of God in Viinijärvi",
           "Jumalanäidin Tihvinäläisen ikonin kirkko",
           ["Viinijärventie 8", "83400 Viinijärvi"], TAIPALE_SITES,
           "The Tikhvin Icon of the Mother of God"),
    sacred("fi-polvijarvi-saint-john-baptist", "fi-taipale-parish", "Church",
           "Church of Saint John the Baptist in Polvijärvi",
           "Pyhän Johannes Kastajan kirkko",
           ["Haavikontie 31", "83700 Polvijärvi"], TAIPALE_SITES,
           "Saint John the Baptist"),
    sacred("fi-outokumpu-holy-spirit", "fi-taipale-parish", "Church",
           "Church of the Holy Spirit in Outokumpu", "Pyhän Hengen kirkko",
           ["Kirkkopolku 3", "83500 Outokumpu"], TAIPALE_SITES,
           "The Holy Spirit"),
    sacred("fi-sotkuma-prophet-elijah", "fi-taipale-parish", "Chapel",
           "Chapel of the Prophet Elijah in Sotkuma",
           "Pyhän profeetta Elian tsasouna",
           ["Malanintie 4", "83750 Sotkuma"], TAIPALE_SITES,
           "The Prophet Elijah"),
    sacred("fi-liperi-saint-andrew", "fi-taipale-parish", "Chapel",
           "Chapel of Saint Andrew the Apostle in Liperi",
           "Pyhän apostoli Andreaksen tsasouna",
           ["Tsasounakuja 1", "83100 Liperi"], TAIPALE_SITES,
           "Saint Andrew the Apostle"),
    sacred("fi-nurmes-saints-peter-paul", "fi-nurmes-chapel-parish", "Church",
           "Church of Saints Peter and Paul in Nurmes",
           "Nurmeksen pyhien apostolien Pietarin ja Paavalin kirkko",
           ["Kirkkokatu 31", "75500 Nurmes"], NURMES_SITES,
           "Saints Peter and Paul"),
    sacred("fi-bomba-saints-sergius-herman-valaam", "fi-nurmes-chapel-parish",
           "Chapel", "Chapel of Saints Sergius and Herman of Valaam at Bomba",
           "Bomban pyhittäjäisien Sergei ja Herman Valamolaisen tsasouna",
           ["Suojärvenkatu 1", "75500 Nurmes"], NURMES_SITES,
           "Saints Sergius and Herman of Valaam"),
    sacred("fi-valtimo-holy-trinity", "fi-nurmes-chapel-parish", "Church",
           "Holy Trinity Church in Valtimo", "Valtimon Pyhän Kolminaisuuden kirkko",
           ["Lokkiharjuntie 40", "75700 Valtimo"], NURMES_SITES,
           "The Holy Trinity"),
    sacred("fi-rasimaki-saint-john-baptist", "fi-nurmes-chapel-parish",
           "Chapel", "Chapel of Saint John the Baptist in Rasimäki",
           "Rasimäen pyhän Johannes Kastajan tsasouna",
           ["Rasimäentie 631", "75790 Rumo"], NURMES_SITES,
           "Saint John the Baptist"),
    sacred("fi-juuka-prophet-elijah", "fi-nurmes-chapel-parish", "Chapel",
           "Chapel of the Prophet Elijah in Juuka",
           "Juuan pyhän profeetta Elian tsasouna",
           ["Laurilantie 7", "83900 Juuka"], NURMES_SITES,
           "The Prophet Elijah"),
    sacred("fi-juuka-orthodox-worship-site", "fi-nurmes-chapel-parish",
           "Worship Site", "Orthodox Worship Site in Juuka",
           "Juuan seurakuntasali", ["Laurilantie 9", "83900 Juuka"],
           NURMES_SITES),
    sacred("fi-pyotikko-exaltation-cross", "fi-nurmes-chapel-parish",
           "Chapel", "Chapel of the Exaltation of the Cross in Pyötikkö",
           "Pyötikön Ristin ylentämisen tsasouna",
           ["Kojonniementie 310 A", "83900 Juuka"], NURMES_SITES,
           "The Exaltation of the Holy Cross"),
    sacred("fi-rautavaara-orthodox-worship-site", "fi-nurmes-chapel-parish",
           "Worship Site", "Orthodox Worship Site in Rautavaara",
           "Rautavaaran evankelis-luterilainen seurakuntasali",
           ["Tulimäentie 11", "Rautavaara"], NURMES_SITES),
    sacred("fi-erakkola-holy-cross-saint-john-chrysostom",
           "fi-nurmes-chapel-parish", "Chapel",
           "Chapel of the Holy Cross and Saint John Chrysostom in Erakkola",
           "Erakkolan pyhän Ristin ylentämisen ja pyhän Johannes "
           "Krysostomoksen tsasouna",
           ["Rasimäentie 521", "75770 Puukari"], NURMES_SITES,
           "The Exaltation of the Holy Cross and Saint John Chrysostom"),
    sacred("fi-keski-vuokko-transfiguration", "fi-nurmes-chapel-parish",
           "Chapel", "Chapel of the Transfiguration in Keski-Vuokko",
           "Keski-Vuokon Kristuksen kirkastumisen tsasouna",
           ["Keski-Vuokontie", "83900 Juuka"], NURMES_SITES,
           "The Transfiguration of Christ"),
    sacred("fi-palomaki-saint-anna", "fi-nurmes-chapel-parish", "Chapel",
           "Chapel of Saint Anna in Palomäki",
           "Herran äidinäidin Annan tsasouna",
           ["Kuopiontie 260", "Palomäki"], NURMES_SITES, "Saint Anna"),
    sacred("fi-paalasmaa-saint-herman-alaska", "fi-nurmes-chapel-parish",
           "Chapel", "Chapel of Saint Herman of Alaska in Paalasmaa",
           "Paalasmaan pyhän Herman Alaskalaisen tsasouna",
           ["Arvinniementie 106", "83910 Paalasmaa"], NURMES_SITES,
           "Saint Herman of Alaska"),
    sacred("fi-tuopanjoki-tikhvin-icon", "fi-nurmes-chapel-parish", "Chapel",
           "Chapel of the Tikhvin Icon of the Mother of God in Tuopanjoki",
           "Tuopanjoen Jumalansynnyttäjän Tihviniläisen ikonin tsasouna",
           ["Tuopanvaarantie 560", "83985 Tuopanjoki"], NURMES_SITES,
           "The Tikhvin Icon of the Mother of God"),
    sacred("fi-vastimo-dormition-theotokos", "fi-nurmes-chapel-parish",
           "Chapel", "Chapel of the Dormition of the Theotokos in Vastimo",
           "Vastimon Jumalansynnyttäjän kuolonuneen nukkumisen tsasouna",
           ["Vastimontie 30", "75500 Nurmes"], NURMES_SITES,
           "The Dormition of the Theotokos"),
])

ROWS["fi-kuopio"].extend([
    sacred("fi-varkaus-ascension", "fi-saimaa-parish", "Church",
           "Church of the Ascension in Varkaus", "Varkauden kirkko",
           ["Relanderinkatu 5", "78200 Varkaus"], SAIMAA_SITES,
           "The Ascension of Christ"),
    sacred("fi-mikkeli-archangel-michael", "fi-saimaa-parish", "Church",
           "Church of Archangel Michael in Mikkeli", "Mikkelin kirkko",
           ["Paavalinkatu 4", "50110 Mikkeli"], SAIMAA_SITES,
           "Archangel Michael"),
    sacred("fi-savonlinna-saints-zacharias-elizabeth", "fi-saimaa-parish",
           "Church", "Church of Saints Zacharias and Elizabeth in Savonlinna",
           "Savonlinnan kirkko",
           ["Olavinkatu 29", "57130 Savonlinna"], SAIMAA_SITES,
           "The Prophet Zacharias and Righteous Elizabeth"),
    sacred("fi-pieksamaki-nativity-theotokos", "fi-saimaa-parish", "Church",
           "Church of the Nativity of the Theotokos in Pieksämäki",
           "Pieksämäen kirkko",
           ["Vanha Mikkelintie 18", "76150 Pieksämäki"], SAIMAA_SITES,
           "The Nativity of the Theotokos"),
    sacred("fi-leppavirta-enlighteners-karelia", "fi-saimaa-parish",
           "Prayer Room", "Prayer Room of the Enlighteners of Karelia in Leppävirta",
           "Leppävirran rukoushuone",
           ["Rinnetie 9", "79100 Leppävirta"], SAIMAA_SITES,
           "The Enlighteners of Karelia"),
    sacred("fi-joroinen-saint-george", "fi-saimaa-parish", "Chapel",
           "Chapel of Saint George in Joroinen", "Joroisten tsasouna",
           ["Kaitaistentie 345", "79690 Joroinen"], SAIMAA_SITES,
           "Saint George the Victory-Bearer"),
    sacred("fi-haukiniemi-saint-seraphim", "fi-saimaa-parish", "Chapel",
           "Chapel of Saint Seraphim of Sarov in Haukiniemi",
           "Savonlinnan Haukiniemen tsasouna",
           ["Juvonlantie 1968", "57130 Savonlinna"], SAIMAA_SITES,
           "Saint Seraphim of Sarov"),
    sacred("fi-visulahti-saints-peter-paul", "fi-saimaa-parish", "Chapel",
           "Chapel of Saints Peter and Paul in Visulahti",
           "Mikkelin Visulahden tsasouna",
           ["Visulahdentie", "50180 Mikkeli"], SAIMAA_SITES,
           "Saints Peter and Paul"),
    sacred("fi-mikkeli-saint-alexander-svir", "fi-saimaa-parish", "Chapel",
           "Chapel of Saint Alexander of Svir in Mikkeli",
           "Aleksanteri Syväriläisen tsasouna",
           ["Kivimäentie 35", "50970 Mikkeli"], SAIMAA_SITES,
           "Saint Alexander of Svir"),
    sacred("fi-mikkeli-cemetery-saint-paraskeva", "fi-saimaa-parish",
           "Cemetery Chapel", "Chapel of Great Martyr Paraskeva at Mikkeli Cemetery",
           "Mikkelin hautausmaan tsasouna",
           ["Saattotie 7", "50120 Mikkeli"], SAIMAA_SITES,
           "Great Martyr Paraskeva"),
    sacred("fi-kangasniemi-orthodox-worship-site", "fi-saimaa-parish",
           "Worship Site", "Orthodox Worship Site in Kangasniemi",
           "Torikulma",
           ["Keskustie 3", "Kangasniemi"], SAIMAA_OTHER),
    sacred("fi-sysma-orthodox-worship-site", "fi-saimaa-parish",
           "Worship Site", "Orthodox Worship Site in Sysmä",
           "Ortodoksinen jumalanpalveluspaikka Sysmässä",
           ["Mataristonkuja 22", "Sysmä"], SAIMAA_OTHER),
    sacred("fi-valamo-transfiguration-main-church", "fi-valamo-monastery",
           "Monastery Church", "Main Church of the Transfiguration at Valamo Monastery",
           "Pääkirkko, Kristuksen kirkastumisen kirkko",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHURCHES,
           "The Transfiguration of Christ"),
    sacred("fi-valamo-all-saints-old-church", "fi-valamo-monastery",
           "Monastery Church", "Old Church of All Saints of Valaam at Valamo Monastery",
           "Vanha kirkko, Kaikkien Valamon pyhien kirkko",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHURCHES,
           "All Saints of Valaam"),
    sacred("fi-valamo-saints-sergius-herman-winter-church",
           "fi-valamo-monastery", "Monastery Church",
           "Winter Church of Saints Sergius and Herman at Valamo Monastery",
           "Talvikirkko, Pyhittäjien Sergein ja Hermanin kirkko",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHURCHES,
           "Saints Sergius and Herman of Valaam"),
    sacred("fi-valamo-saint-nicholas-chapel", "fi-valamo-monastery", "Chapel",
           "Chapel of Saint Nicholas at Valamo Monastery",
           "Pyhän Nikolaos Ihmeidentekijän tsasouna",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHAPELS,
           "Saint Nicholas the Wonderworker"),
    sacred("fi-valamo-saint-herman-alaska-chapel", "fi-valamo-monastery",
           "Chapel", "Chapel of Saint Herman of Alaska at Valamo Monastery",
           "Pyhittäjä Herman Alaskalaisen tsasouna",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHAPELS,
           "Saint Herman of Alaska"),
    sacred("fi-valamo-saint-john-baptist-chapel", "fi-valamo-monastery",
           "Chapel", "Chapel of Saint John the Baptist at Valamo Monastery",
           "Pyhän Johannes Edelläkävijän ja Kastajan tsasouna",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHAPELS,
           "Saint John the Forerunner and Baptist"),
    sacred("fi-valamo-saint-seraphim-chapel", "fi-valamo-monastery", "Chapel",
           "Chapel of Saint Seraphim of Sarov at Valamo Monastery",
           "Pyhittäjä Serafim Sarovilaisen tsasouna",
           ["Valamontie 42", "79850 Uusi-Valamo"], VALAMO_CHAPELS,
           "Saint Seraphim of Sarov"),
    sacred("fi-lintula-holy-trinity-church", "fi-lintula-monastery",
           "Monastery Church", "Holy Trinity Church at Lintula Monastery",
           "Pyhän Kolminaisuuden kirkko",
           ["Honkasalontie 3", "79830 Palokki"], LINTULA_SITES,
           "The Holy Trinity"),
    sacred("fi-lintula-jerusalem-icon-chapel", "fi-lintula-monastery",
           "Chapel", "Chapel of the Jerusalem Icon at Lintula Monastery",
           "Jumalansynnyttäjän Jerusalemilaisen ikonin tsasouna",
           ["Honkasalontie 3", "79830 Palokki"], LINTULA_SITES,
           "The Jerusalem Icon of the Mother of God"),
    sacred("fi-lintula-saint-paraskeva-chapel", "fi-lintula-monastery",
           "Chapel", "Chapel of Venerable Martyr Paraskeva at Lintula Monastery",
           "Pyhittäjämarttyyri Paraskevan tsasouna",
           ["Honkasalontie 3", "79830 Palokki"], LINTULA_SITES,
           "Venerable Martyr Paraskeva"),
])


ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}

DIRECT_RUSSIA_ROWS = ROWS["russia"]


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
    for value in out.values():
        texts = value if isinstance(value, list) else [value]
        for item in texts:
            if isinstance(item, str) and ("\u2013" in item or "\u2014" in item):
                raise ValueError("%s carries a forbidden long dash" %
                                 out.get("id"))
    return out


def _build_all():
    payloads = {}
    seen = set(ROWS)
    allowed_kinds = {"diocese", "parish", "monastery"}
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
    actual = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if actual != EXPECTED:
        raise ValueError("Finland parent counts changed: %r" % actual)
    row_ids = {item["id"] for source_rows in ROWS.values()
               for item in source_rows}
    if (set(ENGLISH_NAMES) != row_ids or
            len(ENGLISH_NAMES) != sum(EXPECTED.values())):
        raise ValueError("Finland English name coverage changed")
    if SHARED_MULTI_COUNTRY_PARENTS - frozenset(EXPECTED):
        raise ValueError("Finland shared parent coverage changed")
    return payloads


def build():
    """Build Finland's three country-local branch payloads."""
    payloads = _build_all()
    return {parent: payloads[parent] for parent in LOCAL_PAYLOAD_PARENTS}


def contributions(payloads=None):
    """Return source rows grouped for the shared directory builders."""
    payloads = payloads or _build_all()
    return {parent: list(payload["rows"])
            for parent, payload in payloads.items()}


def manifest(payloads=None):
    payloads = payloads or build()
    return {
        parent: {
            "url": "/data/directory/%s.v1.json" % parent,
            "count": len(payload["rows"]),
            "country": payload["country"],
            "merge_required": parent in SHARED_MULTI_COUNTRY_PARENTS,
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
        if parent in SHARED_MULTI_COUNTRY_PARENTS:
            print("merge required for %s (%d Finland rows)" %
                  (parent, len(payload["rows"])))
            continue
        path = output_path(parent)
        path.write_bytes(encoded(payload))
        print("wrote %s (%d rows)" %
              (path.relative_to(ROOT), len(payload["rows"])))


def problems(payloads):
    errors = []
    expected = set()
    for parent, payload in sorted(payloads.items()):
        if parent in SHARED_MULTI_COUNTRY_PARENTS:
            continue
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


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = []
    for parent in set(payloads) | set(SHARED_MULTI_COUNTRY_PARENTS):
        if parent not in base_ids:
            errors.append("missing directory parent: %s" % parent)
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Finland row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        if args.write:
            write(payloads)
            errors = problems(payloads)
        else:
            errors = repository_problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Finland: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
        return 0
    print("Finland branches: %d bodies under %d local parents" %
          (sum(len(payload["rows"]) for payload in payloads.values()),
           len(payloads)))
    for parent, entry in manifest(payloads).items():
        suffix = " (merge required)" if entry["merge_required"] else ""
        print("%s: %d%s" % (parent, entry["count"], suffix))
    print("russia: %d direct rows (merge required)" %
          len(DIRECT_RUSSIA_ROWS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
