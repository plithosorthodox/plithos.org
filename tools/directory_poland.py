#!/usr/bin/env python3
"""Validated directory fragment for canonical Orthodox bodies in Poland.

The current first-party union names every parish, chapel, pastoral point,
military parish, monastery, religious house, and skete that can be published
without inference. Statistics Poland reports three additional non-military
parishes for which the Polish Church roster does not expose current names;
those remain in the candidate ledger.

    python tools/directory_poland.py --check
    python tools/directory_poland.py --dump
"""

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKED = "2026-11-15"

POLISH_ROSTER = "https://ukraina.cerkiew.pl/pl/parafie-2/"
POLISH_STATS = (
    "https://stat.gov.pl/files/gfx/portalinformacyjny/en/"
    "defaultaktualnosci/3632/1/4/1/"
    "religious_denominations_in_poland_2022_2024.pdf"
)
POLISH_SUMMARY = (
    "https://ukraina.cerkiew.pl/pl/prawoslawna-cerkiew-w-polsce/"
)
LUBLIN_MONASTERIES = "https://lublin.cerkiew.pl/monastery/"

JABLECZNA = "https://cerkiew.pl/parafie/monaster-sw-onufrego-w-jablecznej"
GRABARKA = (
    "https://cerkiew.pl/parafie/"
    "monaster-swietych-marty-i-marii-na-swietej-gorze-grabarce"
)
SAKI = "https://cerkiew.pl/parafie/monaster-sw-dymitra-solunskiego-w-sakach"
SUPRASL = (
    "https://cerkiew.pl/parafie/"
    "monaster-zwiastowania-przenajswietszej-bogurodzicy-i-sw-jana-"
    "teologa-w-supraslu"
)
ZWIERKI = (
    "https://cerkiew.pl/parafie/"
    "monaster-narodzenia-przenajswietszej-bogurodzicy-w-zwierkach"
)
WOJNOWO = (
    "https://cerkiew.pl/parafie/"
    "monaster-zasniecia-matki-bozej-w-wojnowie"
)
TURKOWICE = "https://lublin.cerkiew.pl/monastery/turkowice/"
ZALESZANY = (
    "https://cerkiew.pl/parafie/monaster-sw-katarzyny-w-zaleszanach"
)
WYSOWA = (
    "https://cerkiew.pl/polska/"
    "remont-cerkwi-pw-sw-archaniola-michala-w-wysowej-zdroju-2"
)
KOSTOMLOTY = "https://lublin.cerkiew.pl/monastery/kostomloty/"
HOLESZOW = (
    "https://lublin.cerkiew.pl/parafie/"
    "dekanat-chelmski/holeszow-sw-michala-archaniola/"
)
ODRYNKI = (
    "https://cerkiew.pl/parafie/"
    "skit-swietych-antoniego-i-teodozjusza-pieczerskich-w-odrynkach"
)

DIOCESE_BY_TABLE = {}
for table in range(0, 6):
    DIOCESE_BY_TABLE[table] = "Warsaw-Bielsk Diocese"
for table in range(6, 11):
    DIOCESE_BY_TABLE[table] = "Bialystok-Gdansk Diocese"
for table in range(11, 14):
    DIOCESE_BY_TABLE[table] = "Lodz-Poznan Diocese"
for table in range(14, 18):
    DIOCESE_BY_TABLE[table] = "Przemysl-Gorlice Diocese"
for table in range(18, 23):
    DIOCESE_BY_TABLE[table] = "Wroclaw-Szczecin Diocese"
for table in range(23, 28):
    DIOCESE_BY_TABLE[table] = "Lublin-Chelm Diocese"
DIOCESE_BY_TABLE[28] = "Military Ordinariate"

PARENT_BY_TABLE = {}
for table in range(0, 6):
    PARENT_BY_TABLE[table] = "pl-warsaw-bielsk"
for table in range(6, 11):
    PARENT_BY_TABLE[table] = "pl-bialystok-gdansk"
for table in range(11, 14):
    PARENT_BY_TABLE[table] = "pl-lodz-poznan"
for table in range(14, 18):
    PARENT_BY_TABLE[table] = "pl-przemysl-gorlice"
for table in range(18, 23):
    PARENT_BY_TABLE[table] = "pl-wroclaw-szczecin"
for table in range(23, 28):
    PARENT_BY_TABLE[table] = "pl-lublin-chelm"
PARENT_BY_TABLE[28] = "pl-army-ordinariate"

EXPECTED_ROSTER = {
    "Bialystok-Gdansk Diocese": 58,
    "Lodz-Poznan Diocese": 13,
    "Lublin-Chelm Diocese": 30,
    "Military Ordinariate": 7,
    "Przemysl-Gorlice Diocese": 26,
    "Warsaw-Bielsk Diocese": 71,
    "Wroclaw-Szczecin Diocese": 46,
}

# Each item is table number, place, official local dedication, and address.
# The first-party page groups tables by deanery. Table ranges above preserve
# the diocese grouping while avoiding guessed deanery names in public rows.
PARISH_DATA = [
    [0,"Warszawa","Praga. Katedra św. Marii Magdaleny","03-402 Warszawa, al. Solidarności 52"],
    [0,"Warszawa","Wola. Św. Jana Klimaka","01-126 Warszawa, ul. Wolska 138/140"],
    [0,"Warszawa","Ursynów. Św. Sofii - Mądrości Bożej","02-884 Warszawa, ul. Puławska 568"],
    [0,"Warszawa","Kaplica św. św. Cyryla i Metodego","03-403 Warszawa, ul. śww. Cyryla i Metodego 4"],
    [0,"Warszawa","Podwale. Kaplica Świętej Trójcy","00-252 Warszawa, ul. Podwale 5"],
    [0,"Warszawa","Saska Kępa. Kaplica Seminarium","03-945 Warszawa, ul. Paryska 27"],
    [0,"Warszawa","Kaplica św. męcz. archim. Grzegorza","02-351 Warszawa, ul. Lelechowska 5"],
    [0,"Płock","Przemienienia Pańskiego","09-402 Płock, ul. Kościuszki 18"],
    [0,"Stanisławowo","Św. Aleksandry","05-180 Pomiechówek, w. Stanisławowo 20"],
    [0,"Wołomin","Św. św. apostołów Piotra i Pawła","05-200 Wołomin, ul. Fieldorfa 12"],
    [1,"Augustowo","Św. ap. i ewangelisty Jana Teologa","17-100 Bielsk Podlaski; Augustowo 196"],
    [1,"Bielsk Podlaski","Św. archanioła Michała","17-100 Bielsk Podlaski, ul. Mickiewicza 36 skr. poczt. 6"],
    [1,"Bielsk Podlaski","Narodzenia NMP","17-100 Bielsk Podlaski, ul. Jagiellońska 6A"],
    [1,"Bielsk Podlaski","Zmartwychwstania Pańskiego","17-100 Bielsk Podlaski, ul. Traugutta 3"],
    [1,"Bielsk Podlaski","Zaśnięcia NMP","17-100 Bielsk Podlaski, ul. Mickiewicza 179"],
    [1,"Bielsk Podlaski","Opieki Matki Bożej","17-100 Bielsk Podlaski, ul. Reymonta 6"],
    [1,"Boćki","Zaśnięcia NMP","17-111 Boćki, pl. Armii Krajowej 7"],
    [1,"Malesze i Brańsk","Św. św. apostołów Piotra i Pawła","17-121 Łubin Kościelny, w. Malesze 78"],
    [1,"Orla","Św. archanioła Michała","17-106 Orla, ul. Kleszczelowska 9"],
    [1,"Pasynki","Narodzenia św. Jana Chrzciciela","17-100 Bielsk Podlaski, w. Pasynki 40A"],
    [1,"Ploski","Przemienienia Pańskiego","17-100 Bielsk Podlaski, w. Ploski 84"],
    [1,"Podbiele","Św. Proroka Eliasza","17-100 Bielsk Podlaski, w. Podbiele 10"],
    [1,"Rajsk","Św. św. apostołów Piotra i Pawła","17-100 Bielsk Podlaski, w. Rajsk 44"],
    [1,"Ryboły","Św. św. Kosmy i Damiana","16-060 Zabłudów, w. Ryboły 104"],
    [1,"Sasiny","Przemienienia Pańskiego","17-111 Boćki, w. Sasiny 15"],
    [1,"Szczyty","Ścięcia Głowy św. Jana Chrzciciela","17-106 Orla, w. Szczyty-Dzięciołowo 13"],
    [1,"Widowo","Kaspierowskiej ikony Matki Bożej","17-100 Bielsk Podlaski, w. Widowo"],
    [2,"Białowieża","Św. Mikołaja","17-230 Białowieża, ul. Sportowa 9"],
    [2,"Czyże","Zaśnięcia NMP","17-207 Czyże 72"],
    [2,"Dubiny","Zaśnięcia NMP","17-200 Hajnówka, Dubiny, ul. Szkolna 2"],
    [2,"Hajnówka","Świętej Trójcy","17-200 Hajnówka, ul. ks. A. Dziewiatowskiego 15"],
    [2,"Hajnówka","Św. wielkiego męcz. Dymitra","17-200 Hajnówka, ul. Warszawska 103"],
    [2,"Hajnówka","Narodzenia św. Jana Chrzciciela","17-200 Hajnówka, ul. Reja 12"],
    [2,"Kuraszewo","Św. Antoniego Pieczerskiego","17-207 Czyże, w. Kuraszewo 86"],
    [2,"Lewkowo Stare","Św. św. apostołów Piotra i Pawła","17-220 Narewka, w. Lewkowo Stare 23"],
    [2,"Narewka","Św. Mikołaja","17-220 Narewka, ul. Mickiewicza 58"],
    [2,"Nowoberezowo","Wniebowstąpienia Pańskiego","17-200 Hajnówka, w. Nowoberezowo 46"],
    [2,"Orzeszkowo","Wniebowstąpienia Pańskiego","17-200 Hajnówka, w. Orzeszkowo 86A"],
    [2,"Siemianówka","Św. Jerzego","17-222 Siemianówka, ul. Szkolna 46"],
    [2,"Stary Kornin","Św. Michała Archanioła","17-204 Dubicze Cerkiewne, Stary Kornin 23A"],
    [3,"Klejniki","Wniebowstąpienia Pańskiego","17-207 Czyże, w. Klejniki 55"],
    [3,"Łosinka","Św. apostoła Jakuba","17-210 Narew, w. Łosinka 17A"],
    [3,"Narew","Podwyższenia Krzyża Pańskiego","17-210 Narew, ul. Poniatowskiego 27"],
    [3,"Puchły","Opieki Matki Bożej","17-210 Narew, w. Puchły 49"],
    [3,"Trześcianka","Św. Michała Archanioła","17-210 Narew, Trześcianka 120"],
    [3,"Tyniewicze Duże","Św. ew. i apostoła Łukasza","17-210 Narew, w. Tyniewicze Duże 74"],
    [4,"Boratyniec Ruski","Św. Anny","17-300 Siemiatycze Stacja, w. Boratyniec Ruski"],
    [4,"Ciechanowiec","Wniebowstąpienia Pańskiego","18-230 Ciechanowiec, ul. Mickiewicza 37"],
    [4,"Czarna Cerkiewna","Opieki Matki Bożej","17-315 Grodzisk, w. Czarna Cerkiewna 46"],
    [4,"Drohiczyn","Św. Mikołaja","17-312 Drohiczyn, ul. Kraszewskiego 7"],
    [4,"Grabarka","Św. św. Marty i Marii","17-330 Nurzec Stacja, w. Grabarka"],
    [4,"Grodzisk","Św. Mikołaja","17-315 Grodzisk, ul. 22 Lipca 12"],
    [4,"Mielnik","Narodzenia NMP","17-307 Mielnik, ul. Brzeska 93"],
    [4,"Narojki","Św. św. Kosmy i Damiana","17-312 Drohiczyn, w. Narojki 8"],
    [4,"Rogawka","Cudownego Zbawiciela","17-300 Siemiatycze, w. Rogawka 67a"],
    [4,"Siemiatycze","Św. św. apostołów Piotra i Pawła","17-300 Siemiatycze, ul. Powstania Styczniowego 1"],
    [4,"Siemiatycze","Zmartwychwstania Pańskiego","17-300 Siemiatycze, ul. Sikorskiego 3"],
    [4,"Telatycze","Św. św. Kosmy i Damiana","17-330 Nurzec Stacja, w. Anusin 8a"],
    [4,"Tokary","Ikony Matki Bożej \"Wszystkich Strapionych Radość\"","17-307 Mielnik, w. Tokary 25"],
    [4,"Żerczyce","Św. Dymitra Sołuńskiego","17-330 Nurzec, w. Żerczyce 27"],
    [5,"Czeremcha","Matki Bożej \"Miłującej\"","17-240 Czeremcha, ul. Szkolna 15"],
    [5,"Dubicze Cerkiewne","Opieki Matki Bożej","17-204 Dubicze Cerkiewne, ul. Parkowa 15"],
    [5,"Kleszczele","Zaśnięcia NMP","17-250 Kleszczele, ul. 1 Maja 2"],
    [5,"Kośna","Św. Mikołaja","17-250 Kleszczele, w. Kośna 85"],
    [5,"Kuzawa","Św. Barbary","17-240 Czeremcha, w. Kuzawa 68A"],
    [5,"Milejczyce","Św. Barbary","17-332 Milejczyce, ul. św. Barbary 34"],
    [5,"Rogacze","Narodzenia NMP","17-332 Milejczyce, Rogacze 16"],
    [5,"Saki","Św. Dymitra Sołuńskiego","17-250 Kleszczele, w. Saki 54"],
    [5,"Werstok","Podwyższenia Krzyża Pańskiego","17-204 Dubicze Cerkiewne, w. Werstok 2"],
    [5,"Wólka Wygonowska","Św. Michała Archanioła","17-106 Orla, w. Wólka Wygonowska 47"],
    [5,"Zubacze","Opieki Matki Bożej","17-240 Czeremcha, w. Zubacze 37"],
    [6,"Białystok","św. Mikołaja","15-419 Białystok, ul. Świętego Mikołaja 4a"],
    [6,"Białystok","Świętego Ducha","15-762 Białystok, ul. Antoniuk Fabryczny 13"],
    [6,"Białystok","Św. wielkiego męcz. Jerzego","15-346 Białystok, ul. Krucza 5/2 m. 2a"],
    [6,"Białystok","Wszystkich Świętych","15-126 Białystok, ul. Wysockiego 1"],
    [6,"Białystok","Hagia Sophia","15-161 Białystok, ul. Trawiasta 5"],
    [6,"Białystok","Zmartwychwstania Pańskiego","15-667 Białystok, ul. Sikorskiego 9"],
    [6,"Białystok","Św. proroka Eliasza","15-568 Białystok, ul. ks. Aleksandra Tomkowida 6"],
    [6,"Białystok","Św. ap. i ewangelisty Jana Teologa","15-779 Białystok, ul. Zbigniewa Herberta 61"],
    [6,"Białystok - Fasty","Podwyższenia Krzyża Świętego","15-694 Białystok, w. Fasty, ul. św. Krzyża 1"],
    [6,"Białystok","Zaśnięcia NMP","15-616 Białystok, ul. Węgierska 15"],
    [6,"Białystok","św. męcz. archimandryty Grzegorza",""],
    [6,"Białystok-Zaścianki","Św. wielkiego męcz. Pantelejmona","15-521 Białystok-Zaścianki, ul. Grecka 2"],
    [6,"Choroszcz","Opieki Matki Bożej","16-070 Choroszcz, ul. Lipowa 1"],
    [6,"Czarna Białostocka","Św. św. Niewiast Miro Niosących","16-020 Czarna Białostocka, ul. Białostocka 12a"],
    [6,"Ełk","Św. św. apostołów Piotra i Pawła","19-300 Ełk, ul. Konopnickiej 6"],
    [6,"Kożany","Podwyższenia Krzyża Pańskiego","16-063 Bogdanka, w. Kożany"],
    [6,"Supraśl","Zwiastowania NMP","16-030 Supraśl, ul. Klasztorna 1"],
    [6,"Suwałki","Wszystkich Świętych","16-300 Augustów, ul. Mazurska 16"],
    [6,"Topilec","Św. Mikołaja Cudotwórcy","16-070 Choroszcz, w. Topilec 2a"],
    [6,"Wasilków","Św. św. apostołów Piotra i Pawła","16-010 Wasilków, Rynek Kilińskiego / 16-010 Wasilków, ul. Mickiewicza 17 (proboszcz)"],
    [6,"Zabłudów","Zaśnięcia NMP","16-060 Zabłudów, ul. Cerkiewna 8"],
    [7,"Braniewo","Przemienienia Pańskiego","14-500 Braniewo, ul. Wspólna 15"],
    [7,"Elbląg","Św. Marii Magdaleny","82-300 Elbląg, ul. Sadowa 58"],
    [7,"Gdańsk","Św. Mikołaja","80-221 Gdańsk-Wrzeszcz, ul. Traugutta 45"],
    [7,"Orneta","Św. Mikołaja","11-130 Orneta, al. Wojska Polskiego 8 / 14-500 Braniewo, ul. Wspólna 15 (p.o. proboszcza)"],
    [7,"Pasłęk","Św. Onufrego","14-400 Pasłęk, ul. Westerplatte 11 / 82-300 Elbląg, ul. Sadowa 58 (proboszcz)"],
    [8,"Gródek","Narodzenia NMP","16-040 Gródek, ul. ks. Metropolity Bazylego Doroszkiewicza 1"],
    [8,"Jałówka","Podwyższenia Krzyża Świętego","16-060 Michałowo, w. Topolany, ul. Lipowa 2"],
    [8,"Juszkowy Gród","Narodzenia NMP","16-053 Michałowo, w. Juszkowy Gród 33"],
    [8,"Królowy Most","Św. Anny","16-040 Gródek, w. Królowy Most"],
    [8,"Michałowo","Św. Mikołaja","16-050 Michałowo, ul. Młynowa 10B"],
    [8,"Mostowlany","Św. ap. i ewangelisty Jana Teologa","16-040 Gródek, w. Mostowlany 8"],
    [8,"Nowa Wola","Narodzenia św. Jana Chrzciciela","16-050 Michałowo, w. Nowa Wola 85"],
    [8,"Topolany","Przemienienia Pańskiego","16-050 Michałowo, w. Topolany 111 / 16-050 Michałowo, w. Topolany 6 (proboszcz)"],
    [9,"Giżycko","Św. Anny","11-500 Giżycko, ul. Warszawska 41 / 11-500 Giżycko, ul. Pionierska 8 m 17"],
    [9,"Górowo Iławeckie","Zaśnięcia NMP","11-220 Górowo Iławeckie, ul. Wyszyńskiego 30 / 10-291 Olsztyn, ul. Wojska Polskiego 71 m 5 (p. o. proboszcza)"],
    [9,"Kętrzyn","Narodzenia NMP","11-400 Kętrzyn, ul. Limanowskiego 9"],
    [9,"Korsze","Św. św. apostołów Piotra i Pawła","11-430 Korsze, ul. Mickiewicza 33"],
    [9,"Kruklanki","Św. Dymitra","11-612 Kruklanki, ul. 22 Lipca 46"],
    [9,"Lidzbark Warmiński","Św. św. apostołów Piotra i Pawła","11-100 Lidzbark Warmiński, ul. Wysoka Brama 2 / 10-291 Olsztyn, ul. Wojska Polskiego 71 m 5 (p. o. proboszcza)"],
    [9,"Mrągowo","Przemienienia Pańskiego","11-700 Mrągowo, ul. Roosevelta 3 / 11- 700 Mrągowo, ul. Wolności 15/3 (proboszcz)"],
    [9,"Olsztyn","Opieki Matki Bożej","10-229 Olsztyn, al. Wojska Polskiego 38 / 10-229 Olsztyn, al. Wojska Polskiego 71/5 (proboszcz)"],
    [9,"Orłowo","Narodzenia św. Jana Chrzciciela","11- 505 Orłowo 41"],
    [9,"Orzysz","Św. Jerzego","12-250 Orzysz, ul. Ełcka 22"],
    [9,"Węgorzewo","Św. św. apostołów Piotra i Pawła","11-600 Węgorzewo, ul. Pionierska 2 / 11-400 Kętrzyn, ul. Limanowskiego 9 (proboszcz)"],
    [9,"Wojnowo","Zaśnięcia NMP","12-220 Ruciane-Nida, w. Wojnowo 24"],
    [10,"Augustów","Wniebowstąpienia Pańskiego","16-300 Augustów, Rynek Zygmunta Augusta 4 / 16-300 Augustów, ul. Mazurska 16 (proboszcz)"],
    [10,"Dąbrowa Białostocka","Św. ap. i ewangelisty Jana Teologa","16-200 Dąbrowa Białostocka, ul. Kopernika 10"],
    [10,"Jaczno","Zmartwychwstania Pańskiego","16-200 Dąbrowa Białostocka, w. Jaczno 20"],
    [10,"Jurowlany","Św. Jerzego","16-120 Krynki, w. Jurowlany"],
    [10,"Kruszyniany","Św. Anny","16-120 Krynki, w. Kruszyniany"],
    [10,"Krynki","Narodzenia NMP","16-120 Krynki, ul. Cerkiewna 7"],
    [10,"Kuźnica","Podwyższenia Krzyża Pańskiego","16-123 Kuźnica, ul. Sidrzańska 12"],
    [10,"Nowy Dwór","Św. Mikołaja","16-205 Nowy Dwór, ul. Grodzieńska 23"],
    [10,"Ostrów Płn","Zaśnięcia NMP","16-113 Szudziałowo, w. Ostrów Północny"],
    [10,"Samogród","Św. św. apostołów Piotra i Pawła","16-113 Szudziałowo, Suchynicze 80"],
    [10,"Sokółka","Św. Aleksandra Newskiego","16-100 Sokółka, ul. Piłsudskiego 2"],
    [10,"Wierzchlesie","Św. wielkiego męcz. Jerzego","16-113 Szudziałowo, w. Wierzchlesie"],
    [11,"Łódź","św. Aleksandra Newskiego","90-135 Łódź, ul. Kilińskiego 56"],
    [11,"Kalisz","Św. św. apostołów Piotra i Pawła","62-800 Kalisz, ul. Niecała 1"],
    [11,"Piotrków Trybunalski","Wszystkich Świętych","97-300 Piotrków Trybunalski, ul. Słowackiego 15"],
    [11,"Poznań","św. Mikołaja","60-801 Poznań, ul. Marcelińska 20"],
    [12,"Kraków","Zaśnięcia NMP","31-024 Kraków, ul. Szpitalna 24"],
    [12,"Sosnowiec","Św. św. męcz. Wiery, Nadziei, Luby i matki ich Zofii","41-200 Sosnowiec, ul. Kilińskiego 39"],
    [12,"Częstochowa","Częstochowskiej Ikony Matki Bożej","42-217 Częstochowa, ul. Kopernika 7/9"],
    [12,"Radom","Św. Mikołaja","26-617 Radom, ul. Warszawska 15"],
    [12,"Kielce","Św. Mikołaja","25-308 Kielce, ul. Bodzentyńska 46 / ul. Hoża 39/15, 25-618 Kielce (kancelaria)"],
    [13,"Bydgoszcz","Św. Mikołaja","85-131 Bydgoszcz, ul. Nowy Rynek 5"],
    [13,"Toruń","Św. Mikołaja","87-100 Toruń, ul. Podgórna 69"],
    [13,"Grudziądz","Kazańskiej Ikony Bogarodzicy","86-300 Grudziądz, ul. Armii Krajowej 20/1 (parter)"],
    [13,"Włocławek","Św. Mikołaja","87-800 Włocławek, ul. Chopina 3/5"],
    [14,"Gorlice","Katedra Świętej Trójcy","38-300 Gorlice, ul. św. Maksyma 2"],
    [14,"Bartne","Św. św. Kosmy i Damiana","38-307 Sękowa, Bartne 23"],
    [14,"Bielanka","Opieki Matki Bożej i Poczajowskiej Ikony Matki Bożej","38-315 Uście Gorlickie, Kunkowa 43"],
    [14,"Kunkowa","Św. ap. i ewangelisty Łukasza","38-315 Uście Gorlickie, Kunkowa 43"],
    [14,"Leszczyny","Św. ap. i ewangelisty Łukasza","38-315 Uście Gorlickie, Kunkowa 43"],
    [14,"Gładyszów","Narodzenia św. Jana Chrzciciela","38-315 Uście Gorlickie, Gładyszów 45"],
    [14,"Rozdziele","Narodzenia Najświętszej Marii Panny","38-300 Gorlice, ul. św. Maksyma 2"],
    [14,"Żdynia","Opieki Matki Bożej","38-315 Uście Gorlickie, Gładyszów 45"],
    [15,"Hańczowa","Opieki Matki Bożej","38-316 Wysowa-Zdrój, Hańczowa 56"],
    [15,"Krynica-Zdrój","Św. Włodzimierza Wielkiego","33-380 Krynica-Zdrój, ul. św. Włodzimierza 3/1"],
    [15,"Wysowa-Zdrój","Św. Michała Archanioła","38-316 Wysowa-Zdrój"],
    [15,"Nowy Sącz","Prawosławny Punkt Duszpasterski św. św. Cyryla i Metodego","Nowy Sącz, ul. Pijarska 21 (kościół ewangelicko-augsburski)"],
    [15,"Tarnów","Prawosławny Punkt Duszpasterski pw. Częstochowskiej Ikony Matki Bożej","Tarnów, ul. Bernardyńska 24 (kaplica Kościoła polskokatolickiego)"],
    [16,"Kalników","Zaśnięcia NMP","37-724 Kalników 20"],
    [16,"Kłokowice","Opieki Matki Bożej","37-734 Fredropol, Kłokowice 16"],
    [16,"Przemyśl","prokatedra Zaśnięcia NMP","37-700 Przemyśl, ul. Wilczańska 21 / 37-700 Przemyśl, ul. 3 Maja 58 (proboszcz)"],
    [16,"Rzeszów","Przeniesienia relikwii św. Mikołaja z Mir Licejskich do Bari","35-323 Rzeszów, ul. Cienista 20"],
    [16,"Zapałów","Św. św. Kosmy i Damiana","37-544 Zapałów 244"],
    [17,"Komańcza","Opieki Matki Bożej","38-543 Komańcza 216"],
    [17,"Morochów","Spotkania Pańskiego","38-542 Rzepedź, Morochów 15"],
    [17,"Pielgrzymka","Św. archanioła Michała","38-223 Osiek Jasielski Pielgrzymka / 38-300 Gorlice, ul. św. Maksyma 2 (proboszcz)"],
    [17,"Sanok","Świętej Trójcy","38-500 Sanok, ul. Zamkowa 14 / 38-500 Sanok, ul. Kochanowskiego 19/5 (proboszcz)"],
    [17,"Szczawne","Zaśnięcia NMP","38-542 Rzepedź, Morochów 15"],
    [17,"Turzańsk","Św. Archanioła Michała","38-542 Turzańsk 24 / 38-543 Komańcza 216 (proboszcz)"],
    [17,"Zagórz","Św. Archanioła Michała","38-540 Zagórz, ul. Piłsudskiego 51 / 38-500 Sanok, ul. Kochanowskiego 19/5 (proboszcz)"],
    [17,"Zyndranowa","Św. Mikołaja","38-543 Komańcza 216"],
    [18,"Wrocław","Katedra Narodzenia Przenajświętszej Bogurodzicy","50-128 Wrocław, ul. św. Mikołaja 40"],
    [18,"Wrocław","Św. św. Cyryla i Metodego","50-266 Wrocław, ul. św. Jadwigi 13"],
    [18,"Wrocław","Św. Piotra Mohyły","50-266 Wrocław, ul. św. Jadwigi 13"],
    [18,"Kędzierzyn-Koźle","Ikony Bogurodzicy Wszystkich Strapionych Radości","47-220 Kędzierzyn-Koźle, ul. Kościelna 11"],
    [18,"Malczyce","Zwiastowania Przenajświętszej Bogurodzicy","50-130 Malczyce, ul. Mickiewicza 29"],
    [18,"Oleśnica","Zaśnięcia Przenajświętszej Bogurodzicy","56-400 Oleśnica, ul. Łużycka 20"],
    [18,"Opole","Punkt Duszpasterski Poczajowskiej Ikony Bogurodzicy","47-220 Kędzierzyn-Koźle, ul. Kościelna 11"],
    [18,"Sokołowsko","Św. Archanioła Michała","58-350 Mieroszów, ul. Unisławska 8"],
    [18,"Świdnica","Św. Mikołaja","58-100 Świdnica, ul. Łukasińskiego 49"],
    [18,"Wałbrzych","Wszystkich Świętych","tymczasowa kaplica: 58-300 Wałbrzych, ul. Mickiewicza 31"],
    [18,"Stary Wołów","Św. Dymitra Sołuńskiego","56-100 Stary Wołów"],
    [18,"Ząbkowice Śląskie","Św. Jerzego","57-200 Ząbkowice Śląskie, ul. Kłodzka 6"],
    [18,"Żmigród","Św. Jerzego","55-140 Żmigród, ul. Kościuszki 9"],
    [18,"Samborz","Św. Paraskiewy","55-311 Samborz 29"],
    [19,"Głogów","Św. Maksyma Gorlickiego","67-200 Głogów, ul. Bolesława Krzywoustego 2"],
    [19,"Jelenia Góra","Św. św. apostołów Piotra i Pawła","58-500 Jelenia Góra, ul. 1 Maja 40"],
    [19,"Legnica","Zmartwychwstania Pańskiego","59-220 Legnica, ul. Zofii Kossak 9 / 59-220 Legnica, ul. Jaworzyńska 9 (proboszcz)"],
    [19,"Lubin","Świętej Trójcy","59-300 Lubin, ul. 1 Maja 13B"],
    [19,"Michałów","Św. archanioła Michała","59-140 Michałów / Bukowna 20, 59-307 Lubin (proboszcz)"],
    [19,"Rudna","Podwyższenia Krzyża Świętego","ul. Plac Kościelny 2, 59-305 Rudna"],
    [19,"Studzionki","Św. św. Kosmy i Damiana","59-305 Rudna, w. Studzionki"],
    [19,"Zimna Woda","Zaśnięcia Przenajświętszej Bogurodzicy","Zimna Woda 54, 59-300 Lubin / Bukowna 20, 59-307 Lubin (proboszcz)"],
    [19,"Zgorzelec","Św. św. równych apostołom Konstantyna i Heleny","59-903 Zgorzelec, pl. św. św. Konstantyna i Heleny 1 / 59-903 Zgorzelec 5, skr. poczt. 1"],
    [19,"Cieplice","Kaplica pw. Świętego Apostoła Pierwszego Męczennika i Archidiakona Stefana","ul. Cieplicka 70a 58-560 Jelenia Góra"],
    [20,"Buczyna","Św. Dymitra Sołuńskiego","59-160 Radwanice, w. Buczyna 48"],
    [20,"Kożuchów","Wszystkich Świętych","67-120 Kożuchów, ul. Szprotawska 23"],
    [20,"Leszno Górne","Narodzenia Przenajświętszej Bogurodzicy","67-321 Leszno Górne, ul. Szkolna 6"],
    [20,"Lipiny","Św. Michała Archanioła","67-108 Lubięcin, w. Lipiny / ul. Szprotawska 23, 67-120 Kożuchów (proboszcz)"],
    [20,"Przemków","Św. archanioła Michała","59-170 Przemków, pl. Kościelny 6"],
    [20,"Słubice","Opieki Matki Bożej","69-100 Słubice, ul. Bolesława Krzywoustego 4 / ul. Sienkiewicza 24 c, 69-100 Słubice (proboszcz)"],
    [20,"Torzym","Św. archanioła Michała","66-235 Torzym, ul. Sulęcińska 12 / ul. Sulęcińska 8, 66-235 Torzym (proboszcz)"],
    [20,"Zielona Góra","Św. Mikołaja Cudotwórcy","65-332 Zielona Góra, ul. Partyzantów 6"],
    [21,"Barlinek","Zaśnięcia Przenajświętszej Bogurodzicy","74-320 Barlinek, ul. Górna 7"],
    [21,"Brzoza","Św. archanioła Michała","66-500 Brzoza 72"],
    [21,"Gorzów Wielkopolski","Narodzenia Przenajświętszej Bogurodzicy","66-400 Gorzów Wielkopolski, ul. Kostrzyńska 2B"],
    [21,"Gryfice","Zaśnięcia Przenajświętszej Bogurodzicy","72-300 Gryfice, ul. Nowy Świat 1"],
    [21,"Łobez","Św. Jerzego","73-300 Łobez, ul. Wojska Polskiego 8"],
    [21,"Ługi","Zaśnięcia Przenajświętszej Bogurodzicy","66-520 Dobiegniew, w. Ługi 15A"],
    [21,"Stargard","Św. św. apostołów Piotra i Pawła","73-110 Stargard, ul. Nadbrzeżna 4"],
    [21,"Szczecin","Św. Mikołaja","Szczecin, ul. Zygmunta Starego 1A"],
    [21,"Trzebiatów","Świętego Ducha","ul. Wojska Polskiego 44, ul. Nowy Świat 1, 72-300 Gryfice (proboszcz)"],
    [22,"Bobolice","Wszystkich Świętych","ul. Pocztowa 19, Bobolice"],
    [22,"Koszalin","Zaśnięcia Przenajświętszej Bogurodzicy","ul. Tatarkiewicza 9 m 2, 75-351 Koszalin"],
    [22,"Słupsk","Św. św. apostołów Piotra i Pawła","76-200 Słupsk, ul. Krasińskiego 5"],
    [22,"Szczecinek","Świętej Trójcy","78-400 Szczecinek, ul. Szkolna 6"],
    [22,"Wałcz","Świętej Trójcy","78-600 Wałcz, ul. Kujawska 15A"],
    [23,"Lublin","Przemienienia Pańskiego","20-126 Lublin, ul. Ruska 15"],
    [23,"Lublin","Św. metropolity Piotra (Mohyły)","20-127 Lublin, ul. G. Dolińskiego 1"],
    [23,"Puławy","Św. równej apostołom Marii Magdaleny","24-100 Puławy, ul. W. Reymonta 23"],
    [23,"Sandomierz","Św. św. równych apostołom braci Cyryla i Metodego","27-600 Sandomierz, ul. Puławiaków 6"],
    [24,"Biłgoraj","Św. Jerzego Zwycięzcy","23-400 Biłgoraj, ul. Tarnogrodzka 3"],
    [24,"Bończa","Opieki Matki Bożej","22-310 Kraśniczyn, w. Bończa 28"],
    [24,"Hrubieszów","Zaśnięcia NMP","22-500 Hrubieszów, ul. 3 Maja / 22-500 Hrubieszów, ul. Bolesława Prusa 3 m 12 (proboszcz)"],
    [24,"Tarnogród","Świętej Trójcy","23-420 Tarnogród, ul. Cerkiewna 1"],
    [24,"Zamość","Św. Mikołaja Cudotwórcy","22-400 Zamość, ul. gen. M. Bołtucia 26"],
    [24,"Tomaszów Lubelski","Św. Mikołaja Cudotwórcy","22-600 Tomaszów Lubelski, ul. Rynek 13 / ul. M. Kopernika 19 22 - 600 Tomaszów Lubelski (proboszcz)"],
    [25,"Chełm","Św. ap. i ewangelisty Jana Teologa","22-100 Chełm, ul. H. Sienkiewicza 1"],
    [25,"Horostyta","Podwyższenia Krzyża Pańskiego","22-205 Wyryki, w. Horostyta 85"],
    [25,"Włodawa","Narodzenia NMP","22-200 Włodawa, ul. Kościelna 11A"],
    [26,"Biała Podlaska","Św. św. równych apostołom Cyryla i Metodego","21- 500 Biała Podlaska, ul. Terebelska 19"],
    [26,"Biała Podlaska","Św. męcz. Serafina, abpa smoleńskiego","21-500 Biała Podlaska, ul. Dokudowska 4"],
    [26,"Kijowiec","Świętego Ducha","21-512 Zalesie, w. Kijowiec"],
    [26,"Mińsk Mazowiecki","św. Spirydona Cudotwórcy","05-300 Mińsk Mazowiecki, ul. Warszawska 69"],
    [26,"Nosów","Św. Michała Archanioła","21-542 Leśna Podlaska, w. Nosów 36B"],
    [26,"Siedlce","Świętej Trójcy","08-110 Siedlce, ul. Brzeska 15"],
    [26,"Zahorów","Św. św. apostołów Piotra i Pawła","21-530 Piszczac, w. Zahorów 28"],
    [27,"Holeszów","Św. Michała Archanioła","22-213 Hanna, w. Holeszów 43A"],
    [27,"Kobylany","Opieki Matki Bożej","21-540 Małaszewicze, w. Kobylany"],
    [27,"Kodeń","Św. Michała Archanioła","21-509 Kodeń, ul. Sławatycka 19 / 21-509 Kodeń, ul. Sławatycka 11 (proboszcz)"],
    [27,"Kopytów","Św. ap. i ewangelisty Jana Teologa","21-509 Kodeń, w. Kopytów"],
    [27,"Kostomłoty","Św. Serafina z Sarowa","21- 509 Kodeń, w. Kostomłoty 57"],
    [27,"Międzyleś","Św. Anny","21-523 Tuczna, w. Międzyleś 74a"],
    [27,"Dobratycze","Podwyższenia Krzyża Pańskiego","21-509 Dobratycze"],
    [27,"Sławatycze","Opieki Matki Bożej","21-515 Sławatycze, ul. Kodeńska 2"],
    [27,"Terespol","Św. ap. i ewangelisty Jana Teologa","21-550 Terespol, ul. Cerkiewna 2"],
    [27,"Zabłocie","Św. Mikołaja Cudotwórcy","21-509 Kodeń, w. Zabłocie 97"],
    [28,"Warszawa","Św. Jerzego Zwycięzcy","00-909 Warszawa, ul. Żwirki i Wigury 9/13"],
    [28,"Białystok","Św. Wlk. Męcz. Dymitra Sołuńskiego","15-063 Białystok, ul. Warszawska 16 / 15-601 Białystok 6, ul. Kawaleryjska 70/57/6 (kancelaria)"],
    [28,"Gdańsk","Św. Jerzego Zwycięzcy","80-221 Gdańsk, ul. Traugutta 45"],
    [28,"Wrocław","Cywilno-Wojskowa Parafia świętych Cyryla i Metodego","50-266 Wrocław (wyspa Piasek), ul. Św. Jadwigi 13"],
    [28,"Ciechocinek","Św. Michała Archanioła","72-700 Ciechocinek, ul. Wojska Polskiego 3"],
    [28,"Przemyśl","Narodzenia NMP","37-700 Przemyśl, ul. Mariacka 4"],
    [28,"Biała Podlaska","Wojskowo-Cywilna Parafia św. ap. i ewangelisty Marka","21-500 Biała Podlaska, ul. Łomaska 96a / 21-500 Biała Podlaska, ul. Dokudowska 4 (kancelaria)"],
]


def normalize(value):
    table = str.maketrans({
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
    })
    return re.sub(r"\s+", " ", str(value).translate(table)).strip()


def slug(value):
    value = normalize(value).replace("Ł", "L").replace("ł", "l")
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def row(row_id, name, local, sources, rank="Parish", kind="parish",
        address=None, parent="poland"):
    value = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "country": "PL",
        "sources": sources,
    }
    if address:
        value["address"] = address
    return value


def parish_rank(table, local):
    lower = local.lower()
    if table == 28:
        return "Military Parish"
    if "prokatedra" in lower:
        return "Pro-Cathedral"
    if "katedra" in lower:
        return "Cathedral"
    if "punkt duszpasterski" in lower:
        return "Pastoral Ministry"
    if "kaplica" in lower:
        return "Chapel"
    return "Parish"


def build_parish_rows():
    rows = []
    ids = Counter()
    diocese_counts = Counter()
    for table, raw_place, raw_local, raw_address in PARISH_DATA:
        if table not in DIOCESE_BY_TABLE:
            raise ValueError("unknown roster table: %r" % table)
        place = normalize(raw_place)
        local = normalize(raw_local)
        address_text = normalize(raw_address)
        if not place or not local:
            raise ValueError("blank place or dedication in roster table %d" %
                             table)
        local_slug = slug(local)[:72] or "body"
        base = "pl-pol-%s-%s" % (slug(place) or "place", local_slug)
        ids[base] += 1
        row_id = base if ids[base] == 1 else "%s-%d" % (base, ids[base])
        rank = parish_rank(table, local)
        name = "Polish Orthodox %s in %s (%s)" % (rank, place, local)
        addresses = [normalize(part) for part in address_text.split(" / ")
                     if normalize(part)]
        rows.append(row(
            row_id, name, local, [POLISH_ROSTER],
            rank=rank, address=addresses, parent=PARENT_BY_TABLE[table],
        ))
        diocese_counts[DIOCESE_BY_TABLE[table]] += 1
    if len(rows) != 251:
        raise ValueError("Polish Church roster changed: %d rows" % len(rows))
    if dict(sorted(diocese_counts.items())) != EXPECTED_ROSTER:
        raise ValueError("Polish Church roster grouping changed: %r" %
                         dict(sorted(diocese_counts.items())))
    return rows


MONASTIC_ROWS = [
    row(
        "pl-pol-jableczna-onuphrius-monastery",
        "St Onuphrius Monastery in Jableczna",
        "Monaster św. Onufrego w Jabłecznej",
        [POLISH_STATS, JABLECZNA], rank="Monastery", kind="monastery",
        address=["Jabłeczna 69", "21-526 Jabłeczna"],
    ),
    row(
        "pl-pol-grabarka-martha-mary-monastery",
        "Saints Martha and Mary Monastery at Holy Mount Grabarka",
        "Monaster Świętych Marty i Marii na Świętej Górze Grabarce",
        [POLISH_STATS, GRABARKA], rank="Monastery", kind="monastery",
        address=["Grabarka Klasztor 1", "17-330 Nurzec Stacja"],
    ),
    row(
        "pl-pol-saki-demetrius-monastery",
        "St Demetrius of Thessalonica Monastery in Saki",
        "Monaster św. Dymitra Sołuńskiego w Sakach",
        [POLISH_STATS, SAKI], rank="Monastery", kind="monastery",
        address=["Saki 54", "17-250 Kleszczele"],
    ),
    row(
        "pl-pol-suprasl-annunciation-john-monastery",
        "Annunciation of the Most Holy Theotokos and St John the Theologian Monastery in Suprasl",
        "Monaster Zwiastowania Przenajświętszej Bogurodzicy i św. Jana Teologa w Supraślu",
        [POLISH_STATS, SUPRASL], rank="Monastery", kind="monastery",
        address=["ul. Klasztorna 1", "16-030 Supraśl"],
    ),
    row(
        "pl-pol-zwierki-nativity-monastery",
        "Nativity of the Most Holy Theotokos Monastery in Zwierki",
        "Monaster Narodzenia Przenajświętszej Bogurodzicy w Zwierkach",
        [POLISH_STATS, ZWIERKI], rank="Monastery", kind="monastery",
        address=["Zwierki 46", "16-060 Zabłudów"],
    ),
    row(
        "pl-pol-wojnowo-dormition-monastery",
        "Dormition of the Mother of God Monastery in Wojnowo",
        "Monaster Zaśnięcia Matki Bożej w Wojnowie",
        [POLISH_STATS, WOJNOWO], rank="Monastery", kind="monastery",
        address=["Wojnowo 24", "66-120 Wojnowo"],
    ),
    row(
        "pl-pol-turkowice-protection-monastery",
        "Protection of the Mother of God Monastery in Turkowice",
        "Żeński Monaster pw. Opieki Matki Bożej w Turkowicach",
        [POLISH_STATS, TURKOWICE], rank="Monastery", kind="monastery",
        address=["Turkowice 133", "22-546 Turkowice"],
    ),
    row(
        "pl-pol-zaleszany-catherine-house",
        "St Catherine Women's Religious House in Zaleszany",
        "Żeński Dom Zakonny pw. św. Katarzyny w Zaleszanach",
        [POLISH_STATS, ZALESZANY], rank="Religious House",
        kind="monastery", address=["Zaleszany 21", "17-250 Kleszczele"],
    ),
    row(
        "pl-pol-wysowa-protection-house",
        "Protection of the Mother of God Men's Religious House in Wysowa-Zdroj",
        "Prawosławny Męski Dom Zakonny pw. Opieki Matki Bożej w Wysowej-Zdroju",
        [POLISH_STATS, WYSOWA], rank="Religious House",
        kind="monastery", address=["38-316 Wysowa-Zdrój"],
    ),
    row(
        "pl-pol-kostomloty-seraphim-house",
        "St Seraphim of Sarov Men's Religious House in Kostomloty",
        "Męski Dom Zakonny pw. św. Serafina z Sarowa w Kostomłotach",
        [POLISH_STATS, KOSTOMLOTY], rank="Religious House",
        kind="monastery", address=["Kostomłoty 57", "21-509 Kodeń"],
    ),
    row(
        "pl-pol-holeszow-nicholas-house",
        "St Nicholas the Wonderworker Women's Religious House in Holeszow",
        "Żeński Dom Zakonny św. Mikołaja Cudotwórcy w Holeszowie",
        [POLISH_STATS, LUBLIN_MONASTERIES, HOLESZOW],
        rank="Religious House", kind="monastery",
        address=["Holeszów 43A", "22-210 Hanna"],
    ),
    row(
        "pl-pol-odrynki-anthony-theodosius-skete",
        "Sts Anthony and Theodosius of the Kyiv Caves Skete in Odrynki",
        "Skit Świętych Antoniego i Teodozjusza Pieczerskich w Odrynkach",
        [POLISH_STATS, ODRYNKI], rank="Skete", kind="monastery",
        address=["Skit Kudak 1", "17-210 Narew"],
    ),
]


ROWS = {
    "pl-army-ordinariate": [],
    "pl-bialystok-gdansk": [],
    "pl-lodz-poznan": [],
    "pl-lublin-chelm": [],
    "pl-przemysl-gorlice": [],
    "pl-warsaw-bielsk": [],
    "pl-wroclaw-szczecin": [],
    "poland": MONASTIC_ROWS,
}
for _item in build_parish_rows():
    ROWS[_item["parent"]].append(_item)

ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}

EXPECTED = {
    "pl-army-ordinariate": 7,
    "pl-bialystok-gdansk": 58,
    "pl-lodz-poznan": 13,
    "pl-lublin-chelm": 30,
    "pl-przemysl-gorlice": 26,
    "pl-warsaw-bielsk": 71,
    "pl-wroclaw-szczecin": 46,
    "poland": 12,
}


def clean(source):
    out = {key: value for key, value in source.items()
           if value not in (None, "", [])}
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(isinstance(url, str) and url.startswith("http")
               for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    if out.get("address") and (
            not isinstance(out["address"], list) or
            not all(isinstance(item, str) for item in out["address"])):
        raise ValueError("%s has an invalid address" % out.get("id"))
    encoded = json.dumps(out, ensure_ascii=False)
    if "\u2013" in encoded or "\u2014" in encoded:
        raise ValueError("%s contains a long dash" % out.get("id"))
    if "\ufffd" in encoded:
        raise ValueError("%s contains a replacement character" % out.get("id"))
    return out


def build():
    payloads = {}
    seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if item.get("country") != "PL":
                raise ValueError("%s has the wrong country" % row_id)
            if not item.get("name") or not item.get("local"):
                raise ValueError("%s has no usable name" % row_id)
            seen.add(row_id)
            branch_seen.add(row_id)
            rows.append(item)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "PL",
            "rows": rows,
        }
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Poland counts changed: %r" % counts)
    row_ids = [item["id"] for payload in payloads.values()
               for item in payload["rows"]]
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("Poland row IDs are not unique")
    if len(ENGLISH_NAMES) != 263:
        raise ValueError("Poland English name registry changed")
    return payloads


def repository_problems(payloads):
    path = ROOT / "data" / "directory.v1.json"
    try:
        directory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot read %s: %s" % (path.relative_to(ROOT), exc)]
    base_ids = {item.get("id") for item in directory.get("rows", [])}
    errors = []
    for parent in payloads:
        if parent not in base_ids:
            errors.append("missing directory parent: %s" % parent)
    new_ids = {item["id"] for payload in payloads.values()
               for item in payload["rows"]}
    duplicate_ids = sorted(new_ids & base_ids)
    if duplicate_ids:
        errors.append("Poland row IDs already in directory spine: %s" %
                      ", ".join(duplicate_ids))
    return errors


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
        errors = repository_problems(payloads)
    except (OSError, ValueError) as exc:
        print("directory Poland: %s" % exc, file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
        return 0
    ranks = Counter(item["rank"] for payload in payloads.values()
                    for item in payload["rows"])
    print("Poland: 263 verified bodies under the autocephalous Polish Church")
    print("roster: 251 named bodies; monastic institutions: 12")
    print("branches: 6 dioceses, 1 military ordinariate, 1 national monastic union")
    print("ranks: %s" % ", ".join(
        "%s=%d" % pair for pair in sorted(ranks.items())
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
