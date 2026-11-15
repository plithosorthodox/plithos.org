#!/usr/bin/env python3
"""Validated directory fragments for Bosnia and Herzegovina and Montenegro.

Current first-party diocesan rosters are reproduced as discrete parishes,
churches, chapels, worship sites, and monasteries.  Public roster gaps and
unclear historical bodies remain in the companion candidate ledger.

    python tools/directory_bosnia_montenegro.py --check
    python tools/directory_bosnia_montenegro.py --dump
"""

import argparse
import json
import re
import sys
import unicodedata


CHECKED = "2026-11-15"

ZT_HUB = "https://www.eparhijazt.com/sr/1477.eparhija.html"
ZT_MONASTERIES = "https://www.eparhijazt.com/sr/8.manastiri.html"
BP_ROSTER = (
    "https://www.eparhijabihackopetrovacka.org/"
    "eparhija/arhijerejska-namjesnistva/"
)
BP_ADDRESS = "https://www.eparhijabihackopetrovacka.org/adresar/"
BANJA_MONASTERIES = (
    "https://spc.rs/sr/news/517.sakralna-arhitektura-"
    "banjalucke-eparhije.html"
)
BANJA_MILOSEVAC = (
    "https://www.spc.rs/sr/news/iz-medija/16756."
    "praznik-u-manastiru-milosevac.html"
)
BANJA_KARANOVAC = (
    "https://spc.rs/sr/news/iz-zivota-crkve/-/14708."
    "osvecenje-manastirske-kapele-uspenja-presvete-bogorodice-"
    "u-manastiru-karanovcu.html"
)
DABAR_MONASTERIES = (
    "https://www.mitropolijadabrobosanska.org/manastiri.html"
)
ZAH_ROSTER = "https://eparhija-zahumskohercegovacka.org/parohije/"
ZAH_MONASTERIES = "https://eparhija-zahumskohercegovacka.org/parohije/"
ZAH_SUTORINA = (
    "https://eparhija-zahumskohercegovacka.org/"
    "proba-za-parohije-kategorije/"
)
MCL_PARISHES = "https://mitropolija.com/parohije-2/"
MCL_MONASTERIES = "https://mitropolija.com/manastiri/"
BN_PARISHES = "https://www.eparhija.me/index.php/parohije"
BN_MONASTERIES = "https://www.eparhija.me/index.php/manastir"
MILESEVA_PLJEVLJA = (
    "https://milesevskaeparhija.rs/eparhija/crkve/"
    "архиејерејско-намесништво-пљеваљско/"
)

_DATA = json.loads(r'''{"scraped":{"zt_parishes":[{"key":"40","local":"Амајлијска","url":"https://www.eparhijazt.com/sr/40.amajlijska.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Пресвете Тројице у Амајлијама"]},{"key":"41","local":"Балатунско - велиноселска","url":"https://www.eparhijazt.com/sr/41.balatunsko---velinoselska.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Света три јерарха у Балатуну"]},{"key":"42","local":"Батковић - Храм Светог Саве1. парохија","url":"https://www.eparhijazt.com/sr/42.batkovic---hram-svetog-save1-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светога Саве у Батковићу","Филијални храм - ГРОБЉЕ Батковић"]},{"key":"45","local":"Батковић - Храм Светог Саве2. парохија","url":"https://www.eparhijazt.com/sr/45.batkovic---hram-svetog-save2-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светога Саве у Батковићу","Филијални храм - ОСТОЈИЋЕВО"]},{"key":"47","local":"Бијељина - храм Светог влмч. Георгија1. парохија","url":"https://www.eparhijazt.com/sr/47.bijeljina---hram-svetog-vlmc-georgija1-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Георгија у Бијељини"]},{"key":"48","local":"Бијељина - храм Светог влмч. Георгија2. парохија","url":"https://www.eparhijazt.com/sr/48.bijeljina---hram-svetog-vlmc-georgija2-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Георгија"]},{"key":"49","local":"Бијељина - храм Светог влмч. Георгија3. парохија","url":"https://www.eparhijazt.com/sr/49.bijeljina---hram-svetog-vlmc-georgija3-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Георгија у Бијељини"]},{"key":"4672","local":"Бијељина - храм Светог влмч. Георгија4. парохија","url":"https://www.eparhijazt.com/sr/4672.bijeljina---hram-svetog-vlmc-georgija4-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Георгија"]},{"key":"50","local":"Бијељина - храм Рођења Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/50.bijeljina---hram-rodenja-presvete-bogorodice1-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Саборни храм Рођења Пресвете Богородице"]},{"key":"51","local":"Бијељина - храм Рођења Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/51.bijeljina---hram-rodenja-presvete-bogorodice2-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Саборни храм Рођења Пресвете Богородице у Бијељини"]},{"key":"52","local":"Бијељина - храм Рођења Пресвете Богородице3. парохија","url":"https://www.eparhijazt.com/sr/52.bijeljina---hram-rodenja-presvete-bogorodice3-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Саборни храм Рођења Пресвете Богородице"]},{"key":"4670","local":"Бијељина - храм Рођења Пресвете Богородице4. парохија","url":"https://www.eparhijazt.com/sr/4670.bijeljina---hram-rodenja-presvete-bogorodice4-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":[]},{"key":"4851","local":"Бијељина - храм Рођења Пресвете Богородице5. парохија","url":"https://www.eparhijazt.com/sr/4851.bijeljina---hram-rodenja-presvete-bogorodice5-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":[]},{"key":"53","local":"Бијељина - храм св. апостола Петра и Павла1. парохија","url":"https://www.eparhijazt.com/sr/53.bijeljina---hram-sv-apostola-petra-i-pavla1-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светих апостола Петра и Павла у Бијељини"]},{"key":"54","local":"Бијељина - храм св. апостола Петра и Павла2. парохија","url":"https://www.eparhijazt.com/sr/54.bijeljina---hram-sv-apostola-petra-i-pavla2-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светих апостола Петра и Павла у Бијељини"]},{"key":"56","local":"Бијељина - храм св. апостола Петра и Павла3. парохија","url":"https://www.eparhijazt.com/sr/56.bijeljina---hram-sv-apostola-petra-i-pavla3-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светих апостола Петра и Павла у Бијељини"]},{"key":"4753","local":"Бијељина - храм св. апостола Петра и Павла4. парохија","url":"https://www.eparhijazt.com/sr/4753.bijeljina---hram-sv-apostola-petra-i-pavla4-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светих апостола Петра и Павла у Бијељини"]},{"key":"57","local":"Бијељина - храм Светог вмуч. Пантелејмона1. парохија","url":"https://www.eparhijazt.com/sr/57.bijeljina---hram-svetog-vmuc-pantelejmona1-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Пантелејмона у Бијељини - Крушик"]},{"key":"59","local":"Бијељина - Светог вмуч. Пантелејмона2. парохија","url":"https://www.eparhijazt.com/sr/59.bijeljina---svetog-vmuc-pantelejmona2-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Пантелејмона у Бијељини"]},{"key":"58","local":"Бијељина - Светог вмуч. Пантелејмона3. парохија","url":"https://www.eparhijazt.com/sr/58.bijeljina---svetog-vmuc-pantelejmona3-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Пантелејмона"]},{"key":"4662","local":"Бијељина - Светог вмуч. Пантелејмона4. парохија","url":"https://www.eparhijazt.com/sr/4662.bijeljina---svetog-vmuc-pantelejmona4-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Пантелејмона у Бијељини"]},{"key":"60","local":"Бродачка","url":"https://www.eparhijazt.com/sr/60.brodacka.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог архангела Михаила (Сабор Светог архангела Михаила) у Бродцу"]},{"key":"62","local":"Велика Обарска - Храм светог апостола Марка1. парохија","url":"https://www.eparhijazt.com/sr/62.velika-obarska---hram-svetog-apostola-marka1-parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог апостола и јеванђелисте Марка у Великој Обарској"]},{"key":"79","local":"Велика Обарска - Храм светог апостола Марка2.парохија","url":"https://www.eparhijazt.com/sr/79.velika-obarska---hram-svetog-apostola-marka2parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог апостола и јеванђелисте Марка у Великој Обарској"]},{"key":"63","local":"Вршанска","url":"https://www.eparhijazt.com/sr/63.vrsanska.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светога Саве у Вршанима","Филијални храм - Д"]},{"key":"65","local":"Горњоцрњеловачка","url":"https://www.eparhijazt.com/sr/65.gornjocrnjelovacka.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Вазнесења Господњег у Горњем Црњелову"]},{"key":"4673","local":"Гробље Пучиле - Храм преноса моштију св. првомуч. архиђ. Стефана","url":"https://www.eparhijazt.com/sr/4673.groblje-pucile---hram-prenosa-mostiju-sv-prvomuc-arhid-stefana.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог архиђакона Стефана на Градском гробљу „Пучиле“ у Бијељини"]},{"key":"66","local":"Даздаревачко - тријешничка","url":"https://www.eparhijazt.com/sr/66.dazdarevacko---trijesnicka.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Сабора српских светитеља налази се у Даздареву","Филијални храм - ТРИЈЕШНИЦА"]},{"key":"68","local":"Дворови - Храм св. вмуч. Прокопија1.парохија","url":"https://www.eparhijazt.com/sr/68.dvorovi---hram-sv-vmuc-prokopija1parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм светог великомученика Прокопија у Дворовима"]},{"key":"4633","local":"Дворови - Храм св. вмуч. Прокопија2.парохија","url":"https://www.eparhijazt.com/sr/4633.dvorovi---hram-sv-vmuc-prokopija2parohija.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог великомученика Прокопија у Дворовима"]},{"key":"69","local":"Доњоцрњеловачка","url":"https://www.eparhijazt.com/sr/69.donjocrnjelovacka.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Рођења Пресвете Богородице у Доњем Црњелову"]},{"key":"70","local":"Љељеначка","url":"https://www.eparhijazt.com/sr/70.ljeljenacka.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Пресвете Тројице у Љељенчи","Филијални храм - ОБАРСКА БУКОВИЦА"]},{"key":"72","local":"Међашанско - трњачанска","url":"https://www.eparhijazt.com/sr/72.medasansko---trnjacanska.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светог пророка Илије у Трњацима","Филијални храм - МЕЂАШИ"]},{"key":"74","local":"Новодворовска","url":"https://www.eparhijazt.com/sr/74.novodvorovska.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Рођења Светог Јована Крститеља у Новим Дворовима","Филијални храм - ГРОБЉЕ"]},{"key":"4847","local":"Поповљанска","url":"https://www.eparhijazt.com/sr/4847.popovljanska.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Васкрсења Христовог"]},{"key":"77","local":"Чађавичка","url":"https://www.eparhijazt.com/sr/77.cadavicka.html","deanery":"39.arhijerejsko-namjesnistvo-bijeljinsko.html","sites":["Храм Светога пророка Илије у селу Доња Чађавица","Филијални храм - Д","Филијални храм - ГРАДАЦ"]},{"key":"81","local":"Босанско - бијелска","url":"https://www.eparhijazt.com/sr/81.bosansko---bijelska.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Вазнесења Господњег у Бијелој","Филијални храм - ЦЕРИК"]},{"key":"83","local":"Брезовопољска","url":"https://www.eparhijazt.com/sr/83.brezovopoljska.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преображења Господњег у Брезовом Пољу","Филијални храм - Д"]},{"key":"86","local":"Брчко (Српска варош) 1. парохија","url":"https://www.eparhijazt.com/sr/86.brcko-srpska-varosnbsp1-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Успења Пресвете Богородице у Брчком","Филијални храм - ЗОВИК"]},{"key":"88","local":"Брчко (Српска варош) 2. парохија","url":"https://www.eparhijazt.com/sr/88.brcko-srpska-varosnbsp2-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Успења Пресвете Богородице у Брчком"]},{"key":"89","local":"Брчко (Српска варош) 3. парохија","url":"https://www.eparhijazt.com/sr/89.brcko-srpska-varosnbsp3-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Успења Пресвете Богородице у Брчком","Филијални храм"]},{"key":"4635","local":"Брчко (Српска варош) 4. парохија","url":"https://www.eparhijazt.com/sr/4635.brcko-srpska-varosnbsp4-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Успења Пресвете Богородице у Брчком"]},{"key":"99","local":"Брчко (Грчица) 1. парохија","url":"https://www.eparhijazt.com/sr/99.brcko-grcicanbsp1-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Грчици","Филијални храм"]},{"key":"101","local":"Брчко (Грчица) 2. парохија","url":"https://www.eparhijazt.com/sr/101.brcko-grcicanbsp2-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Грчици"]},{"key":"4831","local":"Брчко (Грчица) 3. парохија","url":"https://www.eparhijazt.com/sr/4831.brcko-grcicanbsp3-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Грчици","Филијални храм","Филијални храм - (ГРОБЉЕ - ШУМАРИ)"]},{"key":"4832","local":"Брчко (Грчица) 4. парохија","url":"https://www.eparhijazt.com/sr/4832.brcko-grcicanbsp4-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Грчици","Филијални храм","Филијални храм - ГРЧИЦА"]},{"key":"105","local":"Брчко (Колобара - Грбавица) 1. парохија","url":"https://www.eparhijazt.com/sr/105.brcko-kolobara---grbavica-1-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм свете великомученице Недеље је једнобродна грађевина и налази се у насељу Колобара у Брчком","Филијални храм Светих апостола Петра и Павла (2 .парохија)","Филијални храм Пренос моштију светог Николе (2"]},{"key":"107","local":"Брчко (Колобара - Грбавица) 2. парохија","url":"https://www.eparhijazt.com/sr/107.brcko-kolobara---grbavica-2-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Свете великомученице Недеље у насељу Колобара у Брчком","Филијални храм - ГРБАВИЦА (Св","Филијални храм - ГРБАВИЦА (Светог Николе)"]},{"key":"91","local":"Бузекарачка","url":"https://www.eparhijazt.com/sr/91.buzekaracka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Сабор Светог архангела Гаврила у селу Бузекара","Филијални храм - ДУБРАВИЦЕ (ГРОБЉЕ)","Филијални храм - ПУКИШ"]},{"key":"93","local":"Буквичка","url":"https://www.eparhijazt.com/sr/93.bukvicka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Светог пророка Илије у Буквику","Филијални храм - БУКОВАЦ","Филијални храм - СПОМЕН ХРАМ (Буквик)"]},{"key":"102","local":"Доњобрезичка прва","url":"https://www.eparhijazt.com/sr/102.donjobrezicka-prva.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Вазнесења Господњег"]},{"key":"104","local":"Доњобрезичка друга","url":"https://www.eparhijazt.com/sr/104.donjobrezicka-druga.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Вазнесења Господњег у Доњем Брезику"]},{"key":"108","local":"Лончарско - вучиловачка","url":"https://www.eparhijazt.com/sr/108.loncarsko---vucilovacka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Воздвижења Часног крста Господњег у Лончарима","Филијални храм - ВУЧИЛОВАЦ","Филијални храм - КРЕПШИЋ"]},{"key":"110","local":"Мртвичка","url":"https://www.eparhijazt.com/sr/110.mrtvicka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Светога пророка Илије у Мртвици","Филијални храм - БОБЕТИНО БРДО"]},{"key":"114","local":"Обудовац - Храм Рођења Пресвете Богородице 1. парохија","url":"https://www.eparhijazt.com/sr/114.obudovac---hram-rodenja-presvete-bogorodice-1-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Филијални храмови у Баткуши и Брвнику су у оквиру 2","Храм Рођења Пресвете Богородице у Обудовцу"]},{"key":"112","local":"Обудовац - Храм Рођења Пресвете Богородице 2. парохија","url":"https://www.eparhijazt.com/sr/112.obudovac---hram-rodenja-presvete-bogorodice-2-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Рођења Пресвете Богородице у Обудовцу","Филијални храм - БАТКУША","Филијални храм - БРВНИК"]},{"key":"95","local":"Пелагићево - Храм светог пророка Илије1. парохија","url":"https://www.eparhijazt.com/sr/95.pelagicevo---hram-svetog-proroka-ilije1-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Светога пророка Илије у Пелагићеву","Филијални храм - ПЕЛАГИЋЕВО (гробље)"]},{"key":"97","local":"Пелагићево - Храм светог пророка Илије2. парохија","url":"https://www.eparhijazt.com/sr/97.pelagicevo---hram-svetog-proroka-ilije2-parohija.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Светог пророка Илије у Пелагићеву","Филијални храм - САМАРЕВАЦ"]},{"key":"115","local":"Пиперачка","url":"https://www.eparhijazt.com/sr/115.piperacka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Пиперцима","Филијални храм - Г","Филијални храм - КОРЕНИТА"]},{"key":"117","local":"Поребричка","url":"https://www.eparhijazt.com/sr/117.porebricka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Поребрицама","Филијални храм - БЛАЖЕВАЦ"]},{"key":"119","local":"Поточарско - брезичка","url":"https://www.eparhijazt.com/sr/119.potocarsko---brezicka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Сабора Срба светитеља у селу Поточари код Брчког","Филијални храм - ПОТОЧАРИ (гробље)","Филијални храм - Г"]},{"key":"121","local":"Ражљевачка","url":"https://www.eparhijazt.com/sr/121.razljevacka.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Светог великомученика Димитрија у Ражљеву","Филијални храм - САНДИЋИ","Филијални храм - СЛИЈЕПЧЕВИЋИ"]},{"key":"123","local":"Човићпољско - доњожабарска","url":"https://www.eparhijazt.com/sr/123.covicpoljsko---donjozabarska.html","deanery":"80.arhijerejsko-namjesnistvo-brcansko.html","sites":["Храм Покрова Пресвете Богородице у Доњем Жабару","Филијални храм - ЧОВИЋ ПОЉЕ","Филијални храм- ОРАШЈЕ"]},{"key":"126","local":"Брестовачка","url":"https://www.eparhijazt.com/sr/126.brestovacka.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Покрова Пресвете Богородице у Брестову","Филијални храм - ЦВРТКОВЦИ","Филијални храм - ГОРЊЕ БРЕСТОВО"]},{"key":"128","local":"Брод - Храм Покрова Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/128.brod---hram-pokrova-presvete-bogorodice1-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Покрова Пресвете Богородице у Броду","Филијални храм - СИЈЕКОВАЦ"]},{"key":"130","local":"Брод - Храм Покрова Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/130.brod---hram-pokrova-presvete-bogorodice2-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Покрова Пресвете Богородице у Броду"]},{"key":"131","local":"Брод - Храм Покрова Пресвете Богородице3. парохија","url":"https://www.eparhijazt.com/sr/131.brod---hram-pokrova-presvete-bogorodice3-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Покрова Пресвете Богородице у Броду"]},{"key":"132","local":"Вишћанска","url":"https://www.eparhijazt.com/sr/132.viscanska.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Рођења Пресвете Богородице у Винској","Филијални храмови: ГОРЊА ВРЕЛА, ВЕЛИКА БРУСНИЦА, МАЛА БРУСНИЦА, МАЛА БРУСНИЦА - гробље, ГРК, ДОЊИ КЛАКАР, САБАШТАН, ВИНСКА - гробље, ВИНСКА - гробље нова капела, УНКА, ДУБОКОВАЦ"]},{"key":"134","local":"Дервента - Саборни храм Успења Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/134.derventa---saborni-hram-uspenja-presvete-bogorodice1-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Саборни храм Успења Пресвете Богородице у Дервенти","Капела Светог апостола Томе у Спомен комплексу Чардак - Дервента"]},{"key":"136","local":"Дервента - Саборни храм Успења Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/136.derventa---saborni-hram-uspenja-presvete-bogorodice2-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Успења Пресвете Богородице у Дервенти","Филијални храм - ЧАРДАК"]},{"key":"137","local":"Дервента - Саборни храм Успења Пресвете Богородице3. парохија","url":"https://www.eparhijazt.com/sr/137.derventa---saborni-hram-uspenja-presvete-bogorodice3-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Успења Пресвете Богородице у Дервенти","Филијални храм - СТАРА ЦРКВА"]},{"key":"4879","local":"Дервента - Саборни храм Успења Пресвете Богородице4. парохија","url":"https://www.eparhijazt.com/sr/4879.derventa---saborni-hram-uspenja-presvete-bogorodice4-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Успења Пресвете Богородице у Дервенти"]},{"key":"139","local":"Дервента - Храм Преображења Господњег -Ново Насеље1. парохија","url":"https://www.eparhijazt.com/sr/139.derventa---hram-preobrazenja-gospodnjeg--novo-naselje1-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Преображења Господњег","Филијални храм - АГИЋИ","Филијални храм - МИШКОВЦИ","Филијални храм - ГРОБЉЕ АГИЋИ"]},{"key":"141","local":"Дервента - Храм Преображења Господњег -Ново Насеље2. парохија","url":"https://www.eparhijazt.com/sr/141.derventa---hram-preobrazenja-gospodnjeg--novo-naselje2-parohija.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Преображења Господњег"]},{"key":"143","local":"Дугопољска","url":"https://www.eparhijazt.com/sr/143.dugopoljska.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Рођења Пресвете Богородице (заселак Доњани)","Филијални храм - КУТЛОВАЦ","Филијални храм - ВАРОШ","Филијални храм - БОТАЈИЦА"]},{"key":"145","local":"Календеровачка","url":"https://www.eparhijazt.com/sr/145.kalenderovacka.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Светог цара Константина и царице Јелене у Календеровцима","Филијални храм - ГОРЊИ ДЕТЛАК","Филијални храм - ДРИЈЕН"]},{"key":"147","local":"Лијешћанска","url":"https://www.eparhijazt.com/sr/147.lijescanska.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Пресвете Тројице у Лијешћу","Филијални храм - ГРОБЉЕ ЛИЈЕШЋЕ","Филијални храм - ПОЛОЈ","Филијални храм - БРОДСКО ПОЉЕ"]},{"key":"149","local":"Лужанска","url":"https://www.eparhijazt.com/sr/149.luzanska.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Свих светих у Лужанима","Филијални храм - ПОЉЕ","Филијални храм - ЗБОРИШТЕ","Филијални храм - ДОЊА БАРИЦА","Филијални храм - КОСТРЕШ"]},{"key":"409","local":"Лупљаничка","url":"https://www.eparhijazt.com/sr/409.lupljanicka.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Светог Василија Острошког Чудотворца у Доњој Лупљаници - Поповића Гај","Филијални храм - БОЈАНИЋА ГРОБЉЕ"]},{"key":"152","local":"Мајевачка","url":"https://www.eparhijazt.com/sr/152.majevacka.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Покрова Пресвете Богородице у Мајевцу","Филијални храм - РИТЕШИЋ - Храм св","Филијални храм - РИТЕШИЋ - Гробље","Филијални храм - ШЕШЛИЈЕ","Филијални храм - ГОРЊИ МАЈЕВАЦ","Филијални храм - ТРЊАНИ","Филијални храм - ДОЊИ БОЖИНЦИ"]},{"key":"154","local":"Осиња","url":"https://www.eparhijazt.com/sr/154.osinja.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Светог великомученика Пантелејмона у Осињи","Филијални храм - ГОРЊИ ЦЕРАНИ","Филијални храм - ЦРНЧА"]},{"key":"158","local":"Подновљанска","url":"https://www.eparhijazt.com/sr/158.podnovljanska.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Преображења Господњег у Подновљу","Филијални храм - ГЛОГОВИЦА","Филијални храм - ЛИПА","Филијални храм - ГОРЊИ ВИШЊИК"]},{"key":"160","local":"Појежњанска","url":"https://www.eparhijazt.com/sr/160.pojeznjanska.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Светог великомученика кнеза Лазара у Појезни","Филијални храм - ДОЊИ ЦЕРАНИ"]},{"key":"162","local":"Сочаничка","url":"https://www.eparhijazt.com/sr/162.socanicka.html","deanery":"125.arhijerejsko-namjesnistvo-derventsko.html","sites":["Храм Вазнесења Господњег у Великој Сочаници","Филијални храм - ГРОБЉЕ В","Филијални храм - МАЛА СОЧАНИЦА","Филијални храм - МИШИНЦИ"]},{"key":"165","local":"Бољаничка","url":"https://www.eparhijazt.com/sr/165.boljanicka.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Силаска Светог Духа на апостоле у Бољанићу","Филијални храм - КОНОПЉИШТА"]},{"key":"167","local":"Бочињска","url":"https://www.eparhijazt.com/sr/167.bocinjska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Бочињи","Филијални храм - ДОЛАЦ"]},{"key":"169","local":"Великобуковичка прва","url":"https://www.eparhijazt.com/sr/169.velikobukovicka-prva.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светих апостола Петра и Павла у Великобуковичким Лужанима"]},{"key":"170","local":"Великобуковичка друга","url":"https://www.eparhijazt.com/sr/170.velikobukovicka-druga.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светог пророка Илије у Великој Буковици","Филијални храм - РУДАНКА","Филијални храм - ГРАБОВИЦА"]},{"key":"172","local":"Грачаничка","url":"https://www.eparhijazt.com/sr/172.gracanicka.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Вазнесења Господњег у Грачаници","Филијални храм - ОЗРЕНСКО СУВО ПОЉЕ","Филијални храм - ТЕКУЋИЦА"]},{"key":"174","local":"Добој - Храм св. ап. Петра и Павла1. парохија","url":"https://www.eparhijazt.com/sr/174.doboj---hram-sv-ap-petra-i-pavla1-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светих апостола Петра и Павла у Добоју","Филијални храм у Плочнику припада Добојској 2"]},{"key":"176","local":"Добој - Храм св. ап. Петра и Павла2. парохија","url":"https://www.eparhijazt.com/sr/176.doboj---hram-sv-ap-petra-i-pavla2-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светих апостола Петра и Павла у Добоју"]},{"key":"4636","local":"Добој - Храм св. ап. Петра и Павла3. парохија","url":"https://www.eparhijazt.com/sr/4636.doboj---hram-sv-ap-petra-i-pavla3-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светих апостола Петра и Павла у Добоју"]},{"key":"4854","local":"Добој - Храм св. ап. Петра и Павла4. парохија","url":"https://www.eparhijazt.com/sr/4854.doboj---hram-sv-ap-petra-i-pavla4-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":[]},{"key":"177","local":"Добој - Спомен-храм Рођења Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/177.doboj---spomen-hram-rodenja-presvete-bogorodice1-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Спомен храм Рођења Пресвете Богородице у Добоју"]},{"key":"178","local":"Добој - Спомен-храм Рођења Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/178.doboj---spomen-hram-rodenja-presvete-bogorodice2-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":[]},{"key":"179","local":"Добој - Спомен-храм Рођења Пресвете Богородице3. парохија","url":"https://www.eparhijazt.com/sr/179.doboj---spomen-hram-rodenja-presvete-bogorodice3-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Спомен-храм Рођења Пресвете Богородице у Добоју"]},{"key":"4675","local":"Добој - Спомен-храм Рођења Пресвете Богородице4. парохија","url":"https://www.eparhijazt.com/sr/4675.doboj---spomen-hram-rodenja-presvete-bogorodice4-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Филијални храм - ПЛОЧНИК"]},{"key":"182","local":"Доњопалежничка","url":"https://www.eparhijazt.com/sr/182.donjopaleznicka.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светог пророка Илије у Доњој Палежници","Филијални храм - СЈЕНИНА РИЈЕКА"]},{"key":"186","local":"Кладарска","url":"https://www.eparhijazt.com/sr/186.kladarska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Рођења Пресвете Богородице у Кладарима","Филијални храм - МАЛИ ПРЊАВОР","Филијални храм - ЗАРЈЕЧА","Филијални храм - ТОРИНЕ"]},{"key":"188","local":"Кожушка","url":"https://www.eparhijazt.com/sr/188.kozuska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светог пророка Илије у Кожухама","Филијални храм - ГОРЊА ПАЛЕЖНИЦА","Филијални храм - СЈЕНИНА РИЈЕКА","Филијални храм - СКИПОВАЦ"]},{"key":"190","local":"Липачко - придјелска","url":"https://www.eparhijazt.com/sr/190.lipacko---pridjelska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Свете великомученице Недеље у Липцу","Филијални храм - ПРИДЈЕЛ"]},{"key":"192","local":"Маглајска","url":"https://www.eparhijazt.com/sr/192.maglajska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светог пророка Илије у Маглају","Филијални храм - РЈЕЧИЦА"]},{"key":"193","local":"Осјечанска","url":"https://www.eparhijazt.com/sr/193.osjecanska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Ваведења Пресвете Богородице у Доњим Осјечанима","Филијални храм - ГОРЊИ ОСЈЕЧАНИ"]},{"key":"196","local":"Пољичко - костајничка","url":"https://www.eparhijazt.com/sr/196.poljicko---kostajnicka.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Преподобног Сисоја Великог у Гаврићима","Филијални храм - ГОРЊА КОСТАЈНИЦА"]},{"key":"198","local":"Раковачка","url":"https://www.eparhijazt.com/sr/198.rakovacka.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Силаска Светог Духа на апостоле у Доњем Раковцу","Филијални храм - ГОРЊИ РАКОВАЦ"]},{"key":"200","local":"Српско - грапска","url":"https://www.eparhijazt.com/sr/200.srpsko---grapska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Вазнесења Господњег у Српској Грапској","Филијални храм - ДОЊА КОСТАЈНИЦА"]},{"key":"202","local":"Станари - Храм преподобне Параскеве1. парохија","url":"https://www.eparhijazt.com/sr/202.stanari---hram-prepodobne-paraskeve1-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Станарима","Филијални храм - ОСТРУЖЊА ДОЊА","Филијални храм - ЈЕЛАЊСКА"]},{"key":"4634","local":"Станари - Храм Васкрсења Христовог2. парохија","url":"https://www.eparhijazt.com/sr/4634.stanari---hram-vaskrsenja-hristovog2-parohija.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Васкрсења Христовог у Станарима"]},{"key":"204","local":"Становска","url":"https://www.eparhijazt.com/sr/204.stanovska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Рођења Светог Јована Крститеља у Становима","Филијални храм - ЉЕСКОВЕ ВОДЕ","Филијални храм - ТИСОВАЦ"]},{"key":"206","local":"Стријежевичка","url":"https://www.eparhijazt.com/sr/206.strijezevicka.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Рођења Пресвете Богородице у Стријежевици","Филијални храм - ГОРЊА ПАКЛЕНИЦА","Филијални храм - ДОЊА ПАКЛЕНИЦА","Филијални храм - ОСОЈНИЦА"]},{"key":"208","local":"Усорска","url":"https://www.eparhijazt.com/sr/208.usorska.html","deanery":"164.arhijerejsko-namjesnistvo-dobojsko.html","sites":["Храм Светог Василија Острошког у Усори"]},{"key":"210","local":"Дрињачка","url":"https://www.eparhijazt.com/sr/210.drinjacka.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светог ђакона Авакума у Дрињачи","Филијални храм - ЛИЈЕШАЊ","Филијални храм - ЗЕЛИЊЕ"]},{"key":"212","local":"Зворник- Саборни храм Рођења Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/212.zvornik--saborni-hram-rodenja-presvete-bogorodice1-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Филијални храм - ЂУРЂЕВ ГРАД - види под 2","Филијални храм - МЛАЂЕВАЦ - види под 2"]},{"key":"213","local":"Зворник- Саборни храм Рођења Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/213.zvornik--saborni-hram-rodenja-presvete-bogorodice2-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Рођења Пресвете Богородице у Зворнику","Филијални храм - ЂУРЂЕВ ГРАД","Филијални храм - МЛАЂЕВАЦ"]},{"key":"4873","local":"Зворник- Саборни храм Рођења Пресвете Богородице3. парохија","url":"https://www.eparhijazt.com/sr/4873.zvornik--saborni-hram-rodenja-presvete-bogorodice3-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Филијални храм - БОЛНИЦА"]},{"key":"216","local":"Зворник- Храм Рођења св. Јована Крститеља1. парохија","url":"https://www.eparhijazt.com/sr/216.zvornik--hram-rodenja-sv-jovana-krstitelja1-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Рођења светог Јована Крститеља у Зворнику"]},{"key":"215","local":"Зворник- Храм Рођења св. Јована Крститеља2. парохија","url":"https://www.eparhijazt.com/sr/215.zvornik--hram-rodenja-sv-jovana-krstitelja2-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Рођења светог Јована Крститеља у Зворнику"]},{"key":"4884","local":"Зворник- Храм Рођења Св. Јована Крститеља3. парохија","url":"https://www.eparhijazt.com/sr/4884.zvornik--hram-rodenja-sv-jovana-krstitelja3-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Рођења светог Јована Крститеља у Зворнику"]},{"key":"1540","local":"Зворник - КАРАКАЈ","url":"https://www.eparhijazt.com/sr/1540.zvornik---karakaj.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Васкрсења Господњег у Каракају"]},{"key":"217","local":"Кисељачко - јасеничка и трновичка","url":"https://www.eparhijazt.com/sr/217.kiseljacko---jasenicka-i-trnovicka.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Преображења Господњег у Трновици","Филијални храм - ЈАСЕНИЦА","Филијални храм - КИСЕЉАК"]},{"key":"219","local":"Козлук - Храм св. ап. Петра и Павла 1. парохија","url":"https://www.eparhijazt.com/sr/219.kozluk---hram-sv-ap-petra-i-pavlanbsp1-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светих апостола Петра и Павла","Филијални храм 1","Филијални храм - СКОЧИЋ","Филијални храм - СТАРИ ХРАМ - Козлук"]},{"key":"221","local":"Козлук - Храм св. ап. Петра и Павла2. парохија","url":"https://www.eparhijazt.com/sr/221.kozluk---hram-sv-ap-petra-i-pavla2-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светих апостола Петра и Павла у Козлуку","Филијални храм 2","Филијални храм - ТРШИЋ"]},{"key":"223","local":"Локањска","url":"https://www.eparhijazt.com/sr/223.lokanjska.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Покрова Пресвете Богородице у Горњем Локању","Филијални храм - ДОЊИ ЛОКАЊ (ГРОБЉЕ)","Филијални храм - ГОРЊИ ЛОКАЊ (ГРОБЉЕ)"]},{"key":"225","local":"Ораовачка","url":"https://www.eparhijazt.com/sr/225.oraovacka.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светог великомученика Пантелејмона у Оравцу","Филијални храм - ЈАРДАН"]},{"key":"227","local":"Пиличка","url":"https://www.eparhijazt.com/sr/227.pilicka.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Пилици","Филијални храм - БАРЕ","Филијални храм - ДОЊА ПИЛИЦА"]},{"key":"229","local":"Роћевићка","url":"https://www.eparhijazt.com/sr/229.rocevicka.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светог великомученика Прокопија у Роћевићу"]},{"key":"230","local":"Тишчанска","url":"https://www.eparhijazt.com/sr/230.tiscanska.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светог великомученика Прокопија у Тишчи","Филијални храм - ТРНОВО","Филијални храм - ВРЕЛО"]},{"key":"232","local":"Челопек - Храм св. велмуч. Марине1. парохија","url":"https://www.eparhijazt.com/sr/232.celopek---hram-sv-velmuc-marine1-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Свете великомученице Марине у Челопеку","Филијални храм Сабора српских светитеља у Церу (види под 2"]},{"key":"234","local":"Челопек - Храм св. велмуч. Марине2. парохија","url":"https://www.eparhijazt.com/sr/234.celopek---hram-sv-velmuc-marine2-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Свете великомученице Марине у Челопеку","Филијални храм - ЦЕР"]},{"key":"235","local":"Шековићи - Храм Покрова Пресвете Богородице 1. парохија","url":"https://www.eparhijazt.com/sr/235.sekovici---hram-pokrova-presvete-bogorodice-1-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Покрова Пресвете Богородице у Шековићима","Филијални храм - КАШТИЈЕЉ","Филијални храм - РАШЕВО","Филијални храм - ТУПАНАРИ","Филијални храм - ГОРЊИ БРАЈИНЦИ"]},{"key":"4796","local":"Шековићи - Храм Покрова Пресвете Богородице 2. парохија","url":"https://www.eparhijazt.com/sr/4796.sekovici---hram-pokrova-presvete-bogorodice-2-parohija.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":[]},{"key":"237","local":"Шепачко - брањевска","url":"https://www.eparhijazt.com/sr/237.sepacko---branjevska.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светог великомученика Пантелејмона у Шепку","Филијални храм - БРАЊЕВО"]},{"key":"239","local":"Шетићка","url":"https://www.eparhijazt.com/sr/239.seticka.html","deanery":"209.arhijerejsko-namjesnistvo-zvornicko.html","sites":["Храм Светог пророка Илије у Шетићима","Филијални храм - БОШКОВИЋИ","Филијални храм - МАЛЕШИЋ"]},{"key":"242","local":"Врањачка","url":"https://www.eparhijazt.com/sr/242.vranjacka.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светог великомученика Георгија у Врањаку","Филијални храм - ПОКРОВА ПРЕСВЕТЕ БОГОРОДИЦЕ","Филијални храм - Гробље ЊИВИЦЕ"]},{"key":"244","local":"Гаревац - Храм Преподобне Параскеве1. парохија","url":"https://www.eparhijazt.com/sr/244.garevac---hram-prepodobne-paraskeve1-parohija.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Гаревцу"]},{"key":"245","local":"Гаревац - Храм Преподобне Параскеве2. парохија","url":"https://www.eparhijazt.com/sr/245.garevac---hram-prepodobne-paraskeve2-parohija.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке"]},{"key":"246","local":"Градачачка","url":"https://www.eparhijazt.com/sr/246.gradacacka.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светог пророка Илије у Градачцу"]},{"key":"247","local":"Копривљанска","url":"https://www.eparhijazt.com/sr/247.koprivljanska.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Вазнесења Господњег у Копривни","Филијални храм - СВЕТЕ ПЕТКЕ"]},{"key":"249","local":"Крушковопољска","url":"https://www.eparhijazt.com/sr/249.kruskovopoljska.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светог кнеза Лазара у Крушковом Пољу","Филијални храм - ЛУГОВИ"]},{"key":"251","local":"Милошевачка","url":"https://www.eparhijazt.com/sr/251.milosevacka.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светога Николе у Милошевцу"]},{"key":"252","local":"Модричка прва","url":"https://www.eparhijazt.com/sr/252.modricka-prva.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Успења Пресвете Богородице","Филијални храм - ДОБРИЊА"]},{"key":"254","local":"Модричка друга","url":"https://www.eparhijazt.com/sr/254.modricka-druga-.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Успења Пресвете Богородице","Филијални храм - ВИШЊИК"]},{"key":"256","local":"Модричка трећа","url":"https://www.eparhijazt.com/sr/256.modricka-treca.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Успења Пресвете Богородице у Модричи"]},{"key":"257","local":"Модричка четврта","url":"https://www.eparhijazt.com/sr/257.modricka-cetvrta-.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Успења Пресвете Богородице"]},{"key":"258","local":"Новоградска","url":"https://www.eparhijazt.com/sr/258.novogradska.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светих апостола Петра и Павла у Новом Граду","Филијални храм - ВУКОСАВЉЕ","Филијални храм - ГНИОНИЦА","Филијални храм - ГНИОНИЦА ГРОБЉЕ","Филијални храм - ЈОШАВА"]},{"key":"260","local":"Скугрићка","url":"https://www.eparhijazt.com/sr/260.skugricka.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Рођења Пресвете Богородице у Скугрићу"]},{"key":"261","local":"Слатинска","url":"https://www.eparhijazt.com/sr/261.slatinska.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светога Саве у Горњој Слатини","Филијални храм - ГАЈЕВИ","Филијални храм - ДОЊА СЛАТИНА","Филијални храм - СРЕДЊА СЛАТИНА"]},{"key":"265","local":"Толишка","url":"https://www.eparhijazt.com/sr/265.toliska.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светих апостола Петра и Павла у Горњој Толиси","Филијални храм - ГОРЊА ЗЕЛИЊА","Филијални храм - ГОРЊА ЗЕЛИЊА (СПЛЕТЕНА ЛИПА)","Филијални храм - ГОРЊЕ КРЕЧАНЕ","Филијални храм - ГОРЊИ РИЈЕЧАНИ"]},{"key":"267","local":"Црквинска","url":"https://www.eparhijazt.com/sr/267.crkvinska.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Вазнесења Господњег у Црквини","Филијални храм - (ГРОБЉЕ - ШКАРИЋ)"]},{"key":"268","local":"Шамачка прва","url":"https://www.eparhijazt.com/sr/268.samacka-prva-.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светог великомученика Димитрија у Шамцу","Филијални храм - ГРОБЉЕ (Капела св","Филијални храм - ДОЊА ДУБИЦА","Филијални храм - ПИСАРИ"]},{"key":"270","local":"Шамачка друга","url":"https://www.eparhijazt.com/sr/270.samacka-druga-.html","deanery":"241.arhijerejsko-namjesnistvo-modricko---gradacacko.html","sites":["Храм Светог великомученика Димитрија у Шамцу","Филијални храм - ГРОБЉЕ (КАПЕЛА СВ","Филијални храм - ГРЕБНИЦЕ","Филијални храм - СРПСКА ТИШИНА"]},{"key":"298","local":"Бањаврућичка","url":"https://www.eparhijazt.com/sr/298.banjavrucicka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Вазнесења Господњег у Бањи Врућици"]},{"key":"300","local":"Блатничка","url":"https://www.eparhijazt.com/sr/300.blatnicka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог великомученика кнеза Лазара Косовског у Блатници","Филијални храм - ЖИРАЈА","Филијални храм - ЈАСЕНИЦА","Филијални храм - КОЗИЛА","Филијални храм - ПРЕСЕДЛО"]},{"key":"302","local":"Булетићка","url":"https://www.eparhijazt.com/sr/302.buleticka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Свете великомученице Марине - Огњене Марије у Булетићу"]},{"key":"303","local":"Врућичка","url":"https://www.eparhijazt.com/sr/303.vrucicka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светих апостола Петра и Павла у Врућици","Филијални храм - БРВНАРА"]},{"key":"305","local":"Горњорадњанска","url":"https://www.eparhijazt.com/sr/305.gornjoradnjanska.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог великомученика кнеза Лазара Косовског у Горњој Радњи","Филијални храм - ДОЊА РАДЊА (Драганићи)","Филијални храм - ДОЊА РАДЊА (гробље)","Филијални храм - ОСИВИЦА (гробље)"]},{"key":"307","local":"Младиковинска","url":"https://www.eparhijazt.com/sr/307.mladikovinska.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Покрова Пресвете Богородице у Младиковинама","Филијални храм - МИЛАН ПОЉЕ","Филијални храм - МИЛАН ПОЉЕ (ЦВИЈИЋА ГРОБЉЕ)","Филијални храм - УЗВИНСКА","Филијални храм - УЗВИНСКА (КАПЕЛА)","Филијални храм - САВИЋИ","Филијални храм - САВИЋИ (ЂУРИЋА ГРОБЉЕ)","Филијални храм - ГЛАВИЦЕ (ГРОБЉЕ)","Филијални храм - МАРКОВИЋА ГРОБЉЕ","Филијални храм - КАРПИЋА ГРОБЉЕ"]},{"key":"309","local":"Осредачка","url":"https://www.eparhijazt.com/sr/309.osredacka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог апостола и јеванђелисте Луке у Осретку","Филијални храм - СТУПА","Филијални храм - СТУПА (ГРОБЉЕ)","Филијални храм - ЉЕБ","Филијални храм - ЉЕБ (ГРОБЉЕ)"]},{"key":"311","local":"Прибинићка","url":"https://www.eparhijazt.com/sr/311.pribinicka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светих цара Константина и царице Јелене у Прибинићу","Филијални храм - КАСИМОВИНА (ГРОБЉЕ)"]},{"key":"313","local":"Растушко-укриничка","url":"https://www.eparhijazt.com/sr/313.rastusko-ukrinicka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Покрова Пресвете Богородице у Растуши","Филијални храм - РИЈЕКА (ГРОБЉЕ)"]},{"key":"320","local":"Теслић - Храм Пресвете Тројице1.парохија","url":"https://www.eparhijazt.com/sr/320.teslic---hram-presvete-trojice1parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Спомен храм Пресвете Тројице у Теслићу"]},{"key":"316","local":"Теслић - Храм Пресвете Тројице 2.парохија","url":"https://www.eparhijazt.com/sr/316.nbspteslic---hram-presvete-trojice-2parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Пресвете Тројице у Теслићу","Филијални храм - КУЗМАНИ","Филијални храм - ГОРЊИ ВЛАЈИЋИ"]},{"key":"4677","local":"Теслић - Храм Пресвете Тројице3.парохија","url":"https://www.eparhijazt.com/sr/4677.teslic---hram-presvete-trojice3parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Пресвете Тројице"]},{"key":"4857","local":"Теслић - Храм Пресвете Тројице 4.парохија","url":"https://www.eparhijazt.com/sr/4857.teslic---hram-presvete-trojicenbsp4parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Филијални храм у Жарковини","Храм Пресвете Тројице","Филијални храм - ЖАРКОВИНА"]},{"key":"315","local":"Теслић - Храм св. пророка Илије 1.парохија","url":"https://www.eparhijazt.com/sr/315.nbspteslic---hram-sv-proroka-ilije-1parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог пророка Илије у Теслићу"]},{"key":"321","local":"Теслић - Храм св. пророка Илије2.парохија","url":"https://www.eparhijazt.com/sr/321.teslic---hram-sv-proroka-ilije2parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог пророка Илије у Теслићу","Филијални храм - ВУЈАНОВИЋИ (гробље)"]},{"key":"4798","local":"Теслић - Храм св. пророка Илије3. парохија","url":"https://www.eparhijazt.com/sr/4798.teslic---hram-sv-proroka-ilije3-parohija.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог пророка Илије у Теслићу"]},{"key":"323","local":"Тешањска","url":"https://www.eparhijazt.com/sr/323.tesanjska.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Покрова Пресвете Богородице у Тешњу","Филијални храм - РОСУЉЕ"]},{"key":"325","local":"Угодновичко - очаушка","url":"https://www.eparhijazt.com/sr/325.ugodnovicko---ocauska.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светог великомученика Прокопија у Очаушу","Филијални храм - ОЧАУШ (ГРОБЉЕ)","Филијални храм - КРИВАЈА","Филијални храм - ГОРЊЕ БИЈЕЛО БУЧЈЕ"]},{"key":"327","local":"Церовичка","url":"https://www.eparhijazt.com/sr/327.cerovicka.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Светих апостола Петра и Павла у Церовици","Филијални храм - ВИТКОВЦИ"]},{"key":"329","local":"Чечавска","url":"https://www.eparhijazt.com/sr/329.cecavska.html","deanery":"297.arhijerejsko-namjesnistvo-teslicko.html","sites":["Храм Рођења Пресвете Богородице у Чечави"]},{"key":"331","local":"Бријесничко - тумарска","url":"https://www.eparhijazt.com/sr/331.brijesnicko---tumarska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Пресвете Тројице у Тумарама"]},{"key":"332","local":"Дубничкa","url":"https://www.eparhijazt.com/sr/332.dubnicka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светих праведних Јоакима и Ане у Дубници","Филијални храм - ЈЕГИНОВ ЛУГ"]},{"key":"334","local":"Живиничко - Подгајевска","url":"https://www.eparhijazt.com/sr/334.zivinicko---podgajevska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Силаска Светог Духа на апостоле у Подгајевима"]},{"key":"335","local":"Јасеничко - Потпећка","url":"https://www.eparhijazt.com/sr/335.jasenicko---potpecka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светих апостола Петра и Павла у Јасеници код Сребреника","Филијални храм - СТАРИ ХРАМ - Јасеница","Филијални храм - ПОТПЕЋ","Филијални храм - СРЕДЊА ДРАГУЊА"]},{"key":"337","local":"Какмушка","url":"https://www.eparhijazt.com/sr/337.kakmuska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Пресвете Тројице у Какмужу"]},{"key":"4803","local":"Карановачко - сочковачка","url":"https://www.eparhijazt.com/sr/4803.karanovacko---sockovacka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светог пророка Илије у Карановцу","Филијални храм - СОЧКОВАЦ"]},{"key":"338","local":"Кладањска","url":"https://www.eparhijazt.com/sr/338.kladanjska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светог великомученика Димитрија у Кладњу"]},{"key":"4747","local":"Лопарска","url":"https://www.eparhijazt.com/sr/4747.loparska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":[]},{"key":"339","local":"Мачковац - Храм Рођења Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/339.mackovac-ndash-hram-rodenja-presvete-bogorodice1-parohija.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Рођења Пресвете Богородице у Мачковцу","Филијални храм - МИРОСАВЦИ"]},{"key":"341","local":"Мачковац - Храм Рођења Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/341.mackovac-ndash-hram-rodenja-presvete-bogorodice2-parohija.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Рођења Пресвете Богородице у Мачковцу","Филијални храм - ЈАБЛАНИЦА","Филијални храм - ГОРЊИ МАЧКОВАЦ"]},{"key":"343","local":"Озренска","url":"https://www.eparhijazt.com/sr/343.ozrenska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Рођења Пресвете Богородице у Порјечини","Филијални храм - БРЕЗИЦИ","Филијални храм - БАЈКОВАЦ"]},{"key":"347","local":"Осмачка","url":"https://www.eparhijazt.com/sr/347.osmacka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Пресвете Тројице у Осмацима","Филијални храм - РАКИНО БРДО"]},{"key":"349","local":"Папраћка","url":"https://www.eparhijazt.com/sr/349.papracka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":[]},{"key":"350","local":"Петровљанска","url":"https://www.eparhijazt.com/sr/350.petrovljanska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Покрова Пресвете Богородице у Петрову"]},{"key":"351","local":"Пиперска","url":"https://www.eparhijazt.com/sr/351.piperska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светог Јована Крститеља у Пиперима","Филијални храм - БРУСНИЦА","Филијални храм - ВАКУФ","Филијални храм - ЛУКАВИЦА","Филијални храм - МИЛАДИЋИ"]},{"key":"353","local":"Пожарничка","url":"https://www.eparhijazt.com/sr/353.pozarnicka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Вазнесења Господњег у Пожарници"]},{"key":"354","local":"Прибојска","url":"https://www.eparhijazt.com/sr/354.pribojska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Рођења Пресвете Богородице у Прибоју","Филијални храм - ПОТРАШ","Филијални храм - ПЕЉАВЕ"]},{"key":"356","local":"Пурачићка","url":"https://www.eparhijazt.com/sr/356.puracicka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светога пророка Илије у Пурачићу","Филијални храм - КРТОВА"]},{"key":"358","local":"Растошничка","url":"https://www.eparhijazt.com/sr/358.rastosnicka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светог великомученика кнеза Лазара у Растошници"]},{"key":"359","local":"Тобутска","url":"https://www.eparhijazt.com/sr/359.tobutska.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Светог Јована Крститеља у Тобуту (Зачеће Св","Филијални храм - ЛАБУЦКА","Филијални храм - МЕЗГРАЈА КОСЕ"]},{"key":"361","local":"Тузла - Саборни храм Успења Пресвете Богородице1. парохија","url":"https://www.eparhijazt.com/sr/361.tuzla-ndash-saborni-hram-uspenja-presvete-bogorodice1-parohija.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Филијални храм - ТРНОВАЦ - гробље"]},{"key":"363","local":"Тузла - Саборни храм Успења Пресвете Богородице2. парохија","url":"https://www.eparhijazt.com/sr/363.tuzla-ndash-saborni-hram-uspenja-presvete-bogorodice2-parohija.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Филијални храм - ЦРНО БЛАТО"]},{"key":"365","local":"Цапарде","url":"https://www.eparhijazt.com/sr/365.caparde.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Свете великомученице Марине у Цапардама"]},{"key":"366","local":"Шпионичка","url":"https://www.eparhijazt.com/sr/366.spionicka.html","deanery":"330.arhijerejsko-namjesnistvo-tuzlansko.html","sites":["Храм Успења Пресвете Богородице у Шпионици","Филијални храм - ДОЊЕ СРНИЦЕ","Филијални храм - ГРОБЉЕ СРНИЦЕ"]},{"key":"369","local":"Главичичка","url":"https://www.eparhijazt.com/sr/369.glavicicka-.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Рођења Пресвете Богородице у Главичицама","Филијални храм - ГРОБЉЕ ГЛАВИЧИЦЕ","Филијални храм - ГРОБЉЕ РУХОТИНА"]},{"key":"371","local":"Горњозабрђска","url":"https://www.eparhijazt.com/sr/371.gornjozabrdska.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светога пророка Илије у Горњем Забрђу"]},{"key":"373","local":"Доњозабрђска","url":"https://www.eparhijazt.com/sr/373.donjozabrdska.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светих апостола Петра и Павла у Доњем Забрђу","Филијални храм - УГЉЕВИЧКА ОБРИЈЕЖ"]},{"key":"375","local":"Драгаљевачка","url":"https://www.eparhijazt.com/sr/375.dragaljevacka.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":[]},{"key":"376","local":"Загонска","url":"https://www.eparhijazt.com/sr/376.zagonska-.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светог великомученика Прокопија у Загонима","Филијални храм - ХАСЕ"]},{"key":"378","local":"Јања - Храм св. пророка Илије1. парохија","url":"https://www.eparhijazt.com/sr/378.janja-ndash-hram-sv-proroka-ilije1-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светог пророка Илије у Јањи"]},{"key":"379","local":"Јања - Храм св. пророка Илије2. парохија","url":"https://www.eparhijazt.com/sr/379.janja-ndash-hram-sv-proroka-ilije2-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светог пророка Илије у Јањи"]},{"key":"380","local":"Љесковачка","url":"https://www.eparhijazt.com/sr/380.ljeskovacka.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Свете великомученице Марине у Љесковцу"]},{"key":"381","local":"Модранско - Ченгићка","url":"https://www.eparhijazt.com/sr/381.modransko---cengicka.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светог Јована Крститеља у Ченгићу","Филијални храм - МОДРАН"]},{"key":"383","local":"Патковача - Храм Васкрсења Господњег 1. парохија","url":"https://www.eparhijazt.com/sr/383.patkovaca---hram-vaskrsenja-gospodnjeg-1-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Васкрсења Господњег у Патковачи у изградњи"]},{"key":"4883","local":"Патковачка - Храм Васкрсења Господњег 2. парохија","url":"https://www.eparhijazt.com/sr/4883.patkovacka---hram-vaskrsenja-gospodnjeg-2-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Васкрсења Господњег у Патковачи у изградњи"]},{"key":"384","local":"Пучиљанска","url":"https://www.eparhijazt.com/sr/384.puciljanska.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светих праведних Јоакима и Ане у Пучилама"]},{"key":"385","local":"Сувопољска","url":"https://www.eparhijazt.com/sr/385.suvopoljska-.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Вазнесења Господњег у Сувом Пољу"]},{"key":"386","local":"Тавњанска","url":"https://www.eparhijazt.com/sr/386.tavnjanska.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":[]},{"key":"387","local":"Трновска","url":"https://www.eparhijazt.com/sr/387.trnovska-.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светих апостола Петра и Павла у Доњој Трнови","Филијални храм - ГОРЊА ТРНОВА"]},{"key":"389","local":"Тутњевачка","url":"https://www.eparhijazt.com/sr/389.tutnjevacka.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Покрова Пресвете Богородице у Тутњевцу","Филијални храм - ПУШКОВАЦ"]},{"key":"391","local":"Угљевик - Храм свете Петке1. парохија","url":"https://www.eparhijazt.com/sr/391.ugljevik---hram-svete-petke1-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Преподобне мати Параскеве - Свете Петке у Угљевику"]},{"key":"392","local":"Угљевик - Храм свете Петке2. парохија","url":"https://www.eparhijazt.com/sr/392.ugljevik---hram-svete-petke2-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм свете Петке у Угљевику","Филијални храм - МЕЗГРАЈА"]},{"key":"1539","local":"Угљевик Сјевер - Храм св. Козме и Дамјана1. парохија","url":"https://www.eparhijazt.com/sr/1539.ugljevik-sjever---hram-sv-kozme-i-damjana1-parohija.html","deanery":"368.arhijerejsko-namjesnistvo-ugljevicko---janjsko.html","sites":["Храм Светих бесребреника Козме и Дамјана у Угљевику, насеље Сјевер","Филијални храм - СТАРИ УГЉЕВИК"]}],"zt_monasteries":["МАНАСТИР ЧАСНОГ КРСТА","МАНАСТИР ТАВНА","МАНАСТИР ОЗРЕН","МАНАСТИР ПАПРАЋА","МАНАСТИР ЛОВНИЦА","МАНАСТИР САСЕ","МАНАСТИР ДРАГАЉЕВАЦ","МАНАСТИР КНЕЖИНА","МАНАСТИР СВЕТОГ ВАСИЛИЈА ОСТРОШКОГ","МАНАСТИР СВЕТОГ НИКОЛАЈА МИРЛИКИЈСКОГ","МАНАСТИР ПРЕПОДОБНЕ МАТИ ПАРАСКЕВЕ - СВЕТЕ ПЕТКЕ","МАНАСТИР ДУГА ЊИВА","МАНАСТИР ДОЊА БИШЊА","МАНАСТИР КАРНО","МАНАСТИР ДОЊИ ДЕТЛАК","МАНАСТИР ПЈЕНОВАЦ","МАНАСТИР СВЕТЕ МАТРОНЕ МОСКОВСКЕ","МАНАСТИР РОЖАЊ"],"zt_fails":[],"bp_old":[{"local":"Великоцвјетнићка","sites":["Парохијски храм Преображења Господњег у Великом Цвјетнићу","Рођења Пресвете Богородице у Трубару","Св"]},{"local":"Граховско-преодачка","sites":["Парохијски храм св","Гробљанска капела на Мраморју у Бос","Покрова Пресвете Богородице у Маринковцима","Силаска Светога Духа на апостоле у Преодцу"]},{"local":"Дрварска I","sites":["Парохијски храм св","Покрова Пресвете Богородице у Шиповљанима"]},{"local":"Дрварска II","sites":["Парохијски храм св","Капела Вазнесења Господњег у Доњем Врточу (Спасовина)","св"]},{"local":"Мартинбродска","sites":["Манастирски храм св","Вазнесења Господњег у Кулен Вакуфу"]},{"local":"Пећка","sites":["Парохијски храм Силаска Светога Духа на апостоле у Пећима"]},{"local":"Прекајска","sites":["Парохијски храм Успенија Пресвете Богородице у Прекаји"]},{"local":"Црнолушка","sites":["Парохијски храм св","Св"]},{"local":"Соколовачко-козичка","sites":["Парохијски храм Успења Пресвете Богородице у Соколову","Св","Вазнесења Господњег на Пећима"]},{"local":"Веселинска","sites":["Манастирски храм Рођења св","Ктиторска капела","Спомен-капела мученички пострадалих Срба - пострадалих од усташа у Другом свјетском рату од 1941-1944"]},{"local":"Гламочка I","sites":["Парохијски храм Силаска Светога Духа на апостоле у Гламочу","св"]},{"local":"Гламочка II","sites":["Парохијски храм Силаска Светога Духа на апостоле у Гламочу","Св"]},{"local":"Губинско-врбичка","sites":["Парохијски храм Успења Пресвете Богородице у Губину, Општина Ливно","капела у Доњим Рујанима","Силаска Светога Духа на апостоле у Врбици"]},{"local":"Лијевљанска","sites":["Парохијски храм Успенија Пресвете Богородице у Лијевну/Ливну/","Гробљанска капела св","Капела, спомен-костурница у Лијевну/Ливну/"]},{"local":"Бихаћка","sites":["Катедрални храм Епархије бихаћке Силаска Светога Духа на апостоле у Бихаћу","Капела жена Мироносица у Бихаћу","Св","Силаска Светога Духа на апостоле у Дољанима (Босанским)","Вазнесења Господњег у Липи"]},{"local":"Бјелајска-врточка","sites":["Парохијски храм св","Св","Успенија Пресвете Богородице у Пркосима"]},{"local":"Буковачка","sites":["Парохијски храм Рођења Пресвете Богородице у Буковачи","Силаска Светога Духа на апостоле у Дринићу"]},{"local":"Глиничко-кладушка","sites":["Парохијски храм Преображења Господњег у Бос","Покрова Пресвете Богородице у Шиљковачи","Св"]},{"local":"Крњеушко-вођеничка","sites":["Парохијски храм Успенија Пресвете Богородице у Крњеуши","Рођења Пресвете Богородице у Вођеници"]},{"local":"Петровачка I","sites":["Парохијски храм Св","Покрова Пресвете Богородице у Суваји"]},{"local":"Петровачка II","sites":["Парохијски храм Св"]},{"local":"Петровачка III","sites":["Парохијски храм Св","Преображења Господњег у Колунићу"]},{"local":"Смољанскo-бравска","sites":["Парохијски храм св","Покрова Пресвете Богородице у Јањилама","Св"]},{"local":"Блатњанско-бушевићка","sites":["Парохијски храм Вазнесења Господњег у Бушевићу","Преображења Господњег у Матавазима","Св"]},{"local":"Дабарска","sites":["Парохијски храм Св"]},{"local":"Јасеничко-сувајска","sites":["Парохијски храм св","Св","Рођења св"]},{"local":"Крупска","sites":["Парохијски храм Рођења Пресвете Богородице у Бос","Успенија Пресвете Богородице у Ивањској","Св","Покрова Пресвете Богородице у Великом Радићу","Вазнесења Господњег у Врелу"]},{"local":"Лушципаланачка","sites":["Парохијски храм Вазнесења Господњег у Лушци Паланци","Св","Преображења Господњег у Мајкић Јапри"]},{"local":"Оштролучка","sites":["Парохијски храм Силаска Светога Духа на апостоле у Оштрој Луци","Св"]},{"local":"Расавачка","sites":["Парохијски храм св","Вазнесења Господњег у Расавцима"]},{"local":"Рујишко-дубовичка","sites":["Парохијски храм Рођења Пресвете Богородице у Великој Рујишкој","Св","Силаска Светога Духа на апостоле у Средњем Дубовику - Клисина"]},{"local":"Санска","sites":["Парохијски храм св"]},{"local":"Старомајданска","sites":["Парохијски храм Успенија Пресвете Богородице у Старом Мајдану","Силаска Светога Духа на апостоле у Подвидачи","Св","Пресвете Богородице и њене иконе Тројеручице у Батковцима"]},{"local":"Томинска","sites":["Парохијски храм Св","Св","Преноса Моштију Св","Вазнесења Господњег у Кљевцима (стари храм)","Парохијски храм Вазнесења Господњег у Јапри (Будимлић)","Рођења Пресвете Богородице у Маринима"]},{"local":"Бабићка","sites":["Парохијски храм св","Св"]},{"local":"Герзовачко-бараћка","sites":["Парохијски храм Светог Богојављења у Герзову","Св"]}],"bp_current":["герзовачко-бараћке","I шиповске","густоварске","медљанске","I мркоњићке при храму рођења Пресвете Богородице","Стројичке","III петровачке","пљевско-мујџићке","II мркоњићке при храму рођења Пресвете Богородице","језерске","чађавичко-ораховљанске","II мркоњићке при храму Светог Саве","рујишко-дубовичке","старомајданске","оштролучке","бушевићко-блатњанске","I мркоњићке при храму Светог Саве","подбрдско-грачачке","I дрварске","бабићке","буковачко-дринићке","II шиповске","II петровачке","III шиповске","подрашничке","превијске","бјелајачке","бихаћке","крњеушко-вођеничке","врбљанске","кључке","рибничке","хадровачке","гламочке","граховско-маринковачке","санске","II дрварске","I петровачке"]},"manual":{"mcl_parishes":["Прва парохија цетињска","Друга парохија цетињска","Трећа парохија цетињска","Четврта парохија цетињска","Парохија добрско-метеришка","Пета парохија подгоричка","Шеста парохија подгоричка","Девета подгоричка парохија","Десета подгоричка парохија","Једанаеста парохија подгоричка","Дванаеста парохија подгоричка","Тринаеста парохија подгоричка","Седамнаеста парохија подгоричка","Парохија кучко-братоножићка и љеворечка","Парохија морачко-ровачка","Парохија колашинска","Друга парохија подгоричка","Трећа подгоричка парохија","Четврта парохија подгоричка","Седма парохија подгоричка","Осма парохија подгоричка","Прва парохија подгоричка","Осамнаеста парохија подгоричка","Шеснаеста парохија подгоричка","Деветнаеста парохија подгоричка","Четрнаеста парохија подгоричка","Петнаеста парохија подгоричка","Парохија даниловградска","Парохија јеленачко-подострошка","Парохија спушко-мартинићка","Парохија команско-бандићка, загарачка и загредска","Парохија пјешивачка","Прва парохија зетска","Друга парохија зетска","Трећа парохија зетска","Четврта парохија зетска","Пета парохија зетска","Парохија ријечка","Парохија љешкопољска и љешанске нахије","Друга парохија барска","Трећа парохија барска","Пета парохија барска","Прва барска парохија","Четврта барска парохија","Шеста барска парохија","Прва парохија улцињска","Друга парохија улцињска","Парохија црмничка","Парохија спичанско-мишићка","Прва парохија будванска","Друга парохија будванска","Трећа парохија будванска","Прва парохија маинско-брајићка","Друга парохија маинско-брајићка","Четврта парохија будванска","Парохија петровачка","Парохија паштровско-тудоровићка","Парохија бечићка","Прва парохија которска","Друга парохија которска","Трећа парохија которска","Четврта парохија которска","Прва парохија тиватска","Друга парохија тиватска","Трећа парохија тиватска","Парохија ластванска","Парохија доњогрбаљска","Парохија горњогрбаљска","Парохија ораовачко-перашка","Парохија рисанска","Парохија кривошијска","Парохија морињска","Парохија кртољска","Парохија луштичка","Прва парохија херцегновска","Трећа парохија херцегновска","Пета парохија херцегновска","Друга парохија херцегновска","Четврта парохија херцегновска","Парохија пођанско-сасовићка","Парохија кућанска","Парохија кумборска","Парохија ђеновићка","Парохија баошићка","Прва парохија бијељска","Друга парохија бијељска","Парохија јошичка"],"mcl_monasteries":["Манастир Светог Георгија - Бања","Манастир Свете Параскеве - Буновићи","Манастир Рођења Пресвете Богородице - Подластва","Манастир Свете Матроне Московске","Манастир Светог Саве - Савина Главица-Грбаљ","Манастир Светог Димитрија - Војнић","Манастир Светог Архиђакона Стефана - Дуљево","Манастир Успења Пресвете Богородице - Рустово","Манастир Светог Сергија Радоњешког - Микулићи под Румијом код Бара","Манастир Благовијести - Бешка","Манастир Успенија Пресвете Богородице - Пречиста Крајинска","Манастир Покрова Пресвете Богородице - Горње Брчеле","Манастир Свети Никола - Ободски манастир","Манастир Ваведења Пресвете Богородице - Добрска Ћелија","Манастир Успења Пресвете Богородице - Дуга Морачка","Манастир Светог Николе-Пелев Бријег","Манастир Рођења Пресвете Богородице - Ћелија Пиперска","Манастир Светог Арханђела Михаила - Ждребаоник","Манастир Светог Димитрија - Боан Кадића","Манастир Преподобне Мати Параскеве - Гостиље","Манастир Светих Архангела у Прекобрђу - Морача","Манастир Светих Кирила и Методија - Ћириловац","Манастир Златица","Манастир Цетињски","Манастир Острог","Манастир Успења Пресвете Богородице - Морача","Манастир Успења Пресвете Богородице - Савина","Манастир Ваведења Пресвете Богородице - Жањице","Манастир Светог Арханђела Михаила на Михољској Превлаци","Манастир Светог Арханђела Михаила - Бијелићи","Манастир Успења Пресвете Богородице - Подмаине","Манастир Свете Тројице - Стањевићи","Манастир Светог Николе - Прасквица","Манастир Успења Пресвете Богородице - Режевићи","Манастир Светог Николе - Градиште","Манастир Светог Василија Острошког - Рибњак","Манастир Светог Николе - Врањина","Манастир Успенија Пресвете Богородице - Старчева Горица","Манастир Пресвете Богородице Тројеручице - Морачник","Манастир Светог Димитрија - Топхана","Манастир Светог Николе - Орахово","Манастир Светог Николе - Доње Брчеле","Манастир Успења Пресвете Богородице - Ком","Манастир Св. Георгија - Космач","Манастир Успења Пресвете Богородице - Дајбабе","Манастир-Лавра Св. Симеона Мироточивог","Манастир Пресвете Богородице Јерусалимске - Речине, Колашин"],"bn_parishes":["Парохија Грудске махале и Растока","Горњепољска парохија","Душка парохија","Голијска парохија","Рудопољска парохија","Прва бистричка парохија","Друга бистричка парохија","Друга требјешка парохија","Прва требјешка парохија","Мркошничка парохија","Рубешко-хумачка парохија","Страшевинска парохија","Старотребјешко-кличевска парохија","Кочанска парохија","Парохија Заврх","Парохија Милочани","Драговолучка парохија","Озринићка парохија","Граховска парохија","Жабљачка парохија","Шавничка парохија","Пивска парохија","Бањанско-рудинска парохија","Прва градска парохија","Друга градска парохија","Парохија Шипачно","Парохија Орах","Жупска парохија","Прва беранска парохија","Староградска парохија","Лужачко-долачка парохија","Парохија Парк","Бучичко-виницка парохија","Лубничка парохија","Лимска парохија","Парохија Пешца","Новонасељска парохија","Парохија Берансело","Парохија Заостро","Андријевичка парохија","Трепачко-шекуларска парохија","Горњеполимско-гусињска парохија","Рожајска парохија","Јасиковачка парохија","Дапсићко-петњичка парохија","Прва бјелопољска парохија","Друга бјелопољска парохија","Трећа бјелопољска парохија","Сутиванска парохија","Затонско-брзавска парохија","Ивањска парохија","Прва мојковачка парохија","Друга мојковачка парохија","Томашевска парохија","Павинопољска парохија"],"bn_monasteries":["Манастир Сомина","Манастир Светог Саве","Манастир Златеш","Манастир Шудиково","Манастир Црнча код Бијелог Поља","Манастир Урошевица","Манастир Бијела","Манастир Блишкова","Манастир Брезојевица","Манастир Вољавац","Манастир Добриловина","Манастир Ђурђеви Ступови","Манастир Заграђе","Манастир Кичава или Кладник","Манастир Косијерево","Манастир Никољац у Никољцу код Бијелог Поља","Манастир Пивска дола","Манастир Калудра","Манастир Светог Луке у Жупи Никшићкој","Манастир Самоград","Манастир Подврх","Манастир Пива"],"mil_parishes":["Прва парохија пљеваљска","Друга парохија пљеваљска","Трећа парохија пљеваљска","Прва парохија при храму Св. великомученика Георгија","Друга парохија при храму Св. великомученика Георгија","Трећа парохија при храму Св. великомученика Георгија"],"mil_churches":["Храм Преподобне мати Параскеве у Пљевљима","Саборни храм Светог великомученика Георгија на Гукама, Пљевља","Храм Светог великомученика Прокопија у Љутићима","Храм Светог великомученика Димитрија у Вруљи","Храм Светих равноапостолних Кирила и Методија у Обардама","Храм Светог пророка Илије на Илином брду","Храм Светог великомученика Прокопија на Шулима","Храм Светог Василија Острошког у Малим Крћама","Храм Светих апостола Петра и Павла на Бољанићима"],"mil_monasteries":["Манастир Светог Николаја Мирликијског - Дубочица у Отиловићима","Манастир Свете Тројице у Пљевљима","Манастир Светог архангела Михаила у Ђурђевића Тари","Манастир Успења Пресвете Богородице - Довоља у Премћанима"],"zah_me_parishes":["Српска православна парохија суторинско-крушевичка у Суторини"],"zah_me_churches":["Црква Преображења Господњег у Суторини","Црква Светог великомученика Георгија у Жвињу","Црква Светог пророка Илије на Илијином брду","Црква Светог Николе у Крушевицама"],"zah_ba_parishes":["1. билећка парохија","1. гатачка парохија","1. парохија мостарска","1. парохија невесињска","1. требињска парохија","2. билећка парохија","2. гатачка парохија","2. парохија мостарска","2. парохија невесињска","2. требињска парохија","3. билећка парохија","3. парохија мостарска","3. требињска парохија","4. требињска парохија","5. требињска парохија","6. требињска парохија","7. требињска парохија"],"zah_ba_monasteries":["МАНАСТИР ТВРДОШ","МАНАСТИР ЗАВАЛА","МАНАСТИР ЖИТОМИСЛИЋ","МАНАСТИР ДУЖИ","МАНАСТИР ДОБРИЋЕВО","МАНАСТИР ПЕТРОПАВЛОВ","МАНАСТИР ХЕРЦЕГОВАЧКА ГРАЧАНИЦА","МАНАСТИР ЗУБЦИ"],"dabar_monasteries":["МАНАСТИР УСПЕЊА ПРЕСВЕТЕ БОГОРОДИЦЕ, ДОБРУН","МАНАСТИР СВЕТЕ ТРОЈИЦЕ, ВОЗУЋИЦА","МАНАСТИР СВ. ВЕЛИКОМУЧЕНИКА ГЕОРГИЈА, РАВНА РОМАНИЈА","МАНАСТИР СВ. ОЦА НИКОЛАЈА, ДОБРУНСКА РИЈЕКА","Манастирски скит Благовијести Пресвете Богородице, ВАГАН","МАНАСТИР СВЕТОГ САВЕ, ГОРЊА ЛИЈЕСКА","МАНАСТИР ВАЗНЕСЕЊА ГОСПОДЊЕГ, ВАРДИШТЕ","МАНАСТИР СВЕТЕ ТРОЈИЦЕ, ОЗЕРКОВИЋИ"],"banja_monasteries":["Манастир Гомионица","Манастир Крупа на Врбасу","Манастир Моштаница","Манастир Липље","Манастир Ступље","Манастир Осовица"],"bp_monasteries":["Манастир Рмањ","Манастир Глоговац","Манастир Клисина","Манастир Веселиње","Манастир Трескавац","Манастир Медна","Манастир Милановац","Манастир Соколово","Манастир Губин"]}}''')
SCRAPED = _DATA["scraped"]
MANUAL = _DATA["manual"]

BANJA_CURRENT_MONASTERIES = [
    (local, BANJA_MONASTERIES)
    for local in MANUAL["banja_monasteries"]
] + [
    ("Манастир Милошевац", BANJA_MILOSEVAC),
    ("Манастир Карановац", BANJA_KARANOVAC),
]

ZT_CURRENT_MONASTERIES = [
    ("МАНАСТИР ТАВНА", ZT_MONASTERIES),
    ("МАНАСТИР ЛОВНИЦА", ZT_MONASTERIES),
    ("МАНАСТИР ОЗРЕН", ZT_MONASTERIES),
    ("МАНАСТИР ПАПРАЋА", ZT_MONASTERIES),
    ("МАНАСТИР СВЕТОГ ВАСИЛИЈА ОСТРОШКОГ", ZT_MONASTERIES),
    ("МАНАСТИР СВЕТЕ ПЕТКЕ - ПЕТ ЈЕЗЕРА", ZT_MONASTERIES),
    ("МАНАСТИР СВЕТОГ НИКОЛАЈА МИРЛИКИЈСКОГ", ZT_MONASTERIES),
    ("МАНАСТИР ДРАГАЉЕВАЦ", ZT_MONASTERIES),
    ("МАНАСТИР ДУГА ЊИВА", ZT_MONASTERIES),
    ("МАНАСТИР ДОЊА БИШЊА", ZT_MONASTERIES),
    ("МАНАСТИР СВЕТЕ МАТРОНЕ МОСКОВСКЕ", ZT_MONASTERIES),
    ("МАНАСТИР ЧАСНОГ КРСТА", ZT_MONASTERIES),
    ("МАНАСТИР ДОЊИ ДЕТЛАК", ZT_MONASTERIES),
    ("МАНАСТИР РОЖАЊ", ZT_MONASTERIES),
    ("МАНАСТИР ПРЕСВЕТЕ ТРОЈИЦЕ - ПОДНОВЉЕ", ZT_MONASTERIES),
    ("МАНАСТИР СВ. АЛЕКСАНДРА НЕВСКОГ", ZT_MONASTERIES),
    ("МАНАСТИР ГАВРИЛОВО (ПОПОВО ПОЉЕ)", ZT_MONASTERIES),
    ("МАНАСТИР КРСТОВА ГОРА", ZT_MONASTERIES),
    (
        "МАНАСТИР САСЕ",
        "https://www.eparhijazt.com/en/1572.manastir-sase.html",
    ),
    (
        "МАНАСТИР КНЕЖИНА",
        "https://www.eparhijazt.com/en/1574.manastir-knezina.html",
    ),
    (
        "МАНАСТИР КАРНО",
        "https://www.eparhijazt.com/en/1581.manastir-karno.html",
    ),
    (
        "МАНАСТИР ПЈЕНОВАЦ",
        "https://www.eparhijazt.com/en/1586.manastir-pjenovac.html",
    ),
]
BP_CORRECTED = json.loads(r'''[{"local":"Великоцвјетнићка","sites":["Парохијски храм Преображења Господњег у Великом Цвјетнићу","Рођења Пресвете Богородице у Трубару","Св. равноапостолних Константина и Јелене у Бобољусцима"]},{"local":"Граховско-преодачка","sites":["Парохијски храм св. ап. Петра и Павла у Бос. Грахову","Гробљанска капела на Мраморју у Бос. Грахову","Покрова Пресвете Богородице у Маринковцима","Силаска Светога Духа на апостоле у Преодцу"]},{"local":"Дрварска I","sites":["Парохијски храм св. Саве српског у Дрвару","Покрова Пресвете Богородице у Шиповљанима"]},{"local":"Дрварска II","sites":["Парохијски храм св. Саве српског у Дрвару","Капела Вазнесења Господњег у Доњем Врточу (Спасовина)","св. пророка Илије у Бастасима"]},{"local":"Мартинбродска","sites":["Манастирски храм св. оца Николаја у манастиру Рмњу","Вазнесења Господњег у Кулен Вакуфу"]},{"local":"Пећка","sites":["Парохијски храм Силаска Светога Духа на апостоле у Пећима"]},{"local":"Прекајска","sites":["Парохијски храм Успенија Пресвете Богородице у Прекаји"]},{"local":"Црнолушка","sites":["Парохијски храм св. пророка Илије у Црном Лугу","Св. вмч. Георгија у Пеуљама"]},{"local":"Соколовачко-козичка","sites":["Парохијски храм Успења Пресвете Богородице у Соколову","Св. кнеза Лазара Косовског у Козици","Вазнесења Господњег на Пећима"]},{"local":"Веселинска","sites":["Манастирски храм Рођења св. Јована Крститеља у ман. Веселиње","Ктиторска капела","Спомен-капела мученички пострадалих Срба - пострадалих од усташа у Другом свјетском рату од 1941-1944. године"]},{"local":"Гламочка I","sites":["Парохијски храм Силаска Светога Духа на апостоле у Гламочу","св. пророка Илије у Рорама"]},{"local":"Гламочка II","sites":["Парохијски храм Силаска Светога Духа на апостоле у Гламочу","Св. ап. Петра и Павла у Вагану","Св. царева Константина и Јелене у Стекеровцима"]},{"local":"Губинско-врбичка","sites":["Парохијски храм Успења Пресвете Богородице у Губину, Општина Ливно. Црквено-народни сабор Убрус - Нерукотвореног Лика Господа Исуса Христа","капела у Доњим Рујанима","Силаска Светога Духа на апостоле у Врбици"]},{"local":"Лијевљанска","sites":["Парохијски храм Успенија Пресвете Богородице у Лијевну/Ливну/","Гробљанска капела св. ап. и јев. Марка на гробљу у Застињу","Капела, спомен-костурница у Лијевну/Ливну/"]},{"local":"Бихаћка","sites":["Катедрални храм Епархије бихаћке Силаска Светога Духа на апостоле у Бихаћу","Капела жена Мироносица у Бихаћу","Св. Пантелејмона у Грмуши","Св. ап. Петра и Павла у Гати","Св. ап. Петра и Павла у Притоци","Силаска Светога Духа на апостоле у Дољанима (Босанским)","Вазнесења Господњег у Липи"]},{"local":"Бјелајска-врточка","sites":["Парохијски храм св. вмч. Георгија у Бјелају","Св. пророка Илије у Врточу","Успенија Пресвете Богородице у Пркосима"]},{"local":"Буковачка","sites":["Парохијски храм Рођења Пресвете Богородице у Буковачи","Силаска Светога Духа на апостоле у Дринићу"]},{"local":"Глиничко-кладушка","sites":["Парохијски храм Преображења Господњег у Бос. Бојни","Покрова Пресвете Богородице у Шиљковачи","Св. вмч. Георгија у Великој Кладуши","Св. пророка Илије у Зборишту"]},{"local":"Крњеушко-вођеничка","sites":["Парохијски храм Успенија Пресвете Богородице у Крњеуши","Рођења Пресвете Богородице у Вођеници"]},{"local":"Петровачка I","sites":["Парохијски храм Св. ап. Петра и Павла у Бос. Петровцу","Покрова Пресвете Богородице у Суваји"]},{"local":"Петровачка II","sites":["Парохијски храм Св. ап. Петра и Павла у Бос. Петровцу"]},{"local":"Петровачка III","sites":["Парохијски храм Св. ап. Петра и Павла у Бос. Петровцу","Преображења Господњег у Колунићу"]},{"local":"Смољанскo-бравска","sites":["Парохијски храм св. пророка Илије у Смољани","Покрова Пресвете Богородице у Јањилама","Св. пророка Илије у Бравску"]},{"local":"Блатњанско-бушевићка","sites":["Парохијски храм Вазнесења Господњег у Бушевићу","Преображења Господњег у Матавазима","Св. Тројице у Блатној. (Храм је у изградњи од 2006.године)"]},{"local":"Дабарска","sites":["Парохијски храм Св. ап. и Јеванђ. Марка у Дабру"]},{"local":"Јасеничко-сувајска","sites":["Парохијски храм св. арханг. Гаврила у Српској Јасеници","Св. кнеза Лазара Косовског у Бенаковцу","Св. царева Константина и Јелене у Горњој Суваји","Рођења св. Јована Крститеља у Хашанима"]},{"local":"Крупска","sites":["Парохијски храм Рођења Пресвете Богородице у Бос. Крупи","Успенија Пресвете Богородице у Ивањској","Св. вмч. Пантелејмона у Доњим Петровићима","Св. вмч. Марине у Горњим Петровићима","Св. пророка Илије у Врањској","Покрова Пресвете Богородице у Великом Радићу","Вазнесења Господњег у Врелу"]},{"local":"Лушципаланачка","sites":["Парохијски храм Вазнесења Господњег у Лушци Паланци","Св. Јована Крститеља у Јелашиновцима","Преображења Господњег у Мајкић Јапри","Св. пророка Илије у Липнику"]},{"local":"Оштролучка","sites":["Парохијски храм Силаска Светога Духа на апостоле у Оштрој Луци","Св. кнеза Лазара Косовског у Усорцима"]},{"local":"Расавачка","sites":["Парохијски храм св. вмч. Пантелејмона у Расавцима","Вазнесења Господњег у Расавцима"]},{"local":"Рујишко-дубовичка","sites":["Парохијски храм Рођења Пресвете Богородице у Великој Рујишкој","Св. Јована Богослова у Доњем Дубовику /на камену/","Силаска Светога Духа на апостоле у Средњем Дубовику - Клисина"]},{"local":"Санска","sites":["Парохијски храм св. ап. Петра и Павла у Санском Мосту"]},{"local":"Старомајданска","sites":["Парохијски храм Успенија Пресвете Богородице у Старом Мајдану","Силаска Светога Духа на апостоле у Подвидачи","Св. деспота Стефана Лазаревића и преп. мајке Евгеније у Копривни","Пресвете Богородице и њене иконе Тројеручице у Батковцима"]},{"local":"Томинска","sites":["Парохијски храм Св. царева Константина и Јелене у Томини","Св. вмч. Недјеље у Кијеву","Преноса Моштију Св. оца Николаја у Подовима","Вазнесења Господњег у Кљевцима (стари храм)","Св. архиђакона Стефана у Кљевцима (нови храм)","Парохијски храм Вазнесења Господњег у Јапри (Будимлић)","Св. ап. Јакова Заведејева у Хадровцима","Рођења Пресвете Богородице у Маринима","Св. царева Константина и Јелене у М. Нов. Рујишкој"]},{"local":"Бабићка","sites":["Парохијски храм св. вмч. Прокопија у Бабићима","Св. Василија Острошког у Прибељцима","Св. оца Николаја у Грбавици"]},{"local":"Герзовачко-бараћка","sites":["Парохијски храм Светог Богојављења у Герзову","Св. ап. Петра и Павла у Бараћима"]}]''')

MCL_CHURCHES = [
    "Влашка црква",
    "Храм Св. Ђорђа под Горицом",
    "Храм Св. Архангела Михаила у Дољанима",
    "Храм Рођења Пресвете Богородице на гробљу Чепурци",
    "Саборни храм Вазнесења Господњег на Ублима - Кучи",
    "Саборни храм Св. великомученика Димитрија у Колашину",
    "Саборни храм Васкрсења Христовог у Подгорици",
    "Храм Св. Димитрија на Крушевцу",
    "Храм Св. Ђорђа и 42 новомученика момишићких у Момишићима",
    "Храм Св. Макавеја у Толошима",
    "Храм Рождества Богородице - Зорска црква у селу Грбе",
    "Храм Св. Ђорђа у Доњој Горици",
    "Храм Св. првомученице Текле у Даниловграду",
    "Храм Св. Николаја на Јеленку",
    "Саборни храм Св. Петра Цетињског у Спужу",
    "Саборни храм Св. Николаја у Ливаде бандићке",
    "Саборни храм Светог Јована у Богетићима",
    "Саборни храм Светог Ђорђа у Српској",
    "Саборни храм Преподобне Параскеве-Петке у Голубовцима",
    "Саборни храм Светог великомученика Димитрија у Бијелом Пољу",
    "Саборни храм Светог Николе у Матагужима",
    "Храм Св. Јована Владимира у Бару",
    "Храм Св. Николе у Старом Бару",
    "Храм Свих Светих на Великом пијеску",
    "Црква Пресвете Тројице на Румији",
    "Храм Св. Николе на Лиману",
    "Саборни храм Успења Пресвете Богородице у Вирпазару",
    "Саборни храм Преподобне Параскеве-Петке у Спичанском пољу",
    "Храм Св. Тројице у Старом граду",
    "Храм Преподобне-Петке Параскеве у Подострогу",
    "Филијални храм Св. Димитрија на Брајићима",
    "Саборни храм Св. Илије у Петровцу",
    "Саборни храм Св. Николаја у Тудоровићима",
    "Саборни храм Св. Апостола Томе у Бечићима",
    "Храм Св. Николе у Старом граду",
    "Храм Св. Саве у Тивту",
    "Саборни храм Успења Пресвете Богородице у Радановићима",
    "Саборни храм Свете Тројице у Пелинову",
    "Саборни храм Св. Ђорђа у Ораовцу",
    "Саборни храм Пресвете Богородице у Перасту",
    "Саборни храм Св. Апостола Петра и Павла у Рисну",
    "Саборни храм Покрова Пресвете Богородице на Драгаљу",
    "Саборни храм Св. Саве у Морињу",
    "Саборни храм Успења Пресвете Богородице у Радовићима",
    "Саборни храм Св. Николаја у Радованићима",
    "Храм Св. Вазнесења Господњег на Топлој",
    "Храм Св. Архангела Михаила у Старом граду",
    "Храм Светог праведног Теодора Ушакова на градском гробљу",
    "Саборни храм Св. Сергија и Вакха у Подима",
    "Саборни храм Свете Тројице у Кутима",
    "Саборни храм Св. Василија Острошког у Кумбору",
    "Саборни храм Св. Спиридона у Ђеновићима",
    "Саборни храм Св. Николаја у Баошићима",
    "Саборни храм Полагања ризе Пресвете Богородице у Бијелој",
    "Саборни храм Св. Недеље у Јошици - Каменарима",
]


CYRILLIC = {
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Dj",
    "Е": "E", "Ж": "Z", "З": "Z", "И": "I", "Ј": "J", "К": "K",
    "Л": "L", "Љ": "Lj", "М": "M", "Н": "N", "Њ": "Nj", "О": "O",
    "П": "P", "Р": "R", "С": "S", "Т": "T", "Ћ": "C", "У": "U",
    "Ф": "F", "Х": "H", "Ц": "C", "Ч": "C", "Џ": "Dz", "Ш": "S",
}
CYRILLIC.update({key.lower(): value.lower()
                 for key, value in list(CYRILLIC.items())})


def transliterate(value):
    return "".join(CYRILLIC.get(char, char) for char in value)


ENGLISH_PHRASES = (
    ("Спомен-капела мученички пострадалих Срба - пострадалих од усташа "
     "у Другом свјетском рату од 1941-1944. године",
     "Memorial Chapel to the Serbs martyred by the Ustasha in the "
     "Second World War, 1941-1944"),
    ("Епархије бихаћке Силаска Светога Духа на апостоле у Бихаћу",
     "the Descent of the Holy Spirit upon the Apostles of the Bihac "
     "Eparchy in Bihac"),
    ("Светог великомученика кнеза Лазара Косовског",
     "Saint Great Martyr Prince Lazar of Kosovo"),
    ("Светог Василија Острошког Чудотворца",
     "Saint Basil of Ostrog the Wonderworker"),
    ("Светих бесребреника Козме и Дамјана",
     "Holy Unmercenaries Cosmas and Damian"),
    ("Светих праведних Јоакима и Ане",
     "Saints Righteous Joachim and Anna"),
    ("Светих цара Константина и царице Јелене",
     "Saints Emperor Constantine and Empress Helen"),
    ("Св. Ђорђа и 42 новомученика момишићких",
     "Saint George and the 42 New Martyrs of Momisici"),
    ("Сабора Срба светитеља", "the Synaxis of the Serbian Saints"),
    ("Преподобног Сисоја Великог", "Venerable Sisoes the Great"),
    ("Св. ап. Јакова Заведејева",
     "Saint Apostle James, Son of Zebedee"),
    ("Лавра Св. Симеона Мироточивог",
     "Lavra of Saint Simeon the Myrrh-Streamer"),
    ("Светих Кирила и Методија", "Saints Cyril and Methodius"),
    ("Преподобне-Петке Параскеве", "Venerable Paraskeva"),
    ("Св. првомученице Текле", "Saint Protomartyr Thekla"),
    ("Светог ђакона Авакума", "Saint Deacon Avakum"),
    ("Храм св. Василија Великог", "Church of Saint Basil the Great"),
    ("Св. Александра Невског", "Saint Alexander Nevsky"),
    ("Св. Јована Владимира", "Saint John Vladimir"),
    ("Св. Вазнесења Господњег", "the Ascension of the Lord"),
    ("Св. вмч. Недјеље", "Saint Great Martyr Kyriaki"),
    ("Св. Недеље", "Saint Kyriaki"),
    ("Св. Макавеја", "the Holy Maccabees"),
    ("Светих Архангела", "the Holy Archangels"),
    ("Храм Светог Саве", "Church of Saint Sava"),
    ("Св. Козме и Дамјана", "Saints Cosmas and Damian"),
    ("Козме и Дамјана", "Cosmas and Damian"),
    ("Светог Николе-Пелев Бријег", "Saint Nicholas - Pelev Brijeg"),
    ("Нерукотвореног Лика Господа Исуса Христа",
     "the Image of the Lord Jesus Christ Not Made by Hands"),
    ("Пресвете Богородице и њене иконе Тројеручице",
     "the Most Holy Theotokos and Her Three-Handed Icon"),
    ("Силаска Светога Духа на апостоле",
     "the Descent of the Holy Spirit upon the Apostles"),
    ("Силаска Светог Духа на апостоле",
     "the Descent of the Holy Spirit upon the Apostles"),
    ("Полагања ризе Пресвете Богородице",
     "the Deposition of the Robe of the Most Holy Theotokos"),
    ("Рођења Пресвете Богородице",
     "the Nativity of the Most Holy Theotokos"),
    ("Рождества Пресвете Богородице",
     "the Nativity of the Most Holy Theotokos"),
    ("Рождества Богородице",
     "the Nativity of the Theotokos"),
    ("Успења Пресвете Богородице",
     "the Dormition of the Most Holy Theotokos"),
    ("Успенија Пресвете Богородице",
     "the Dormition of the Most Holy Theotokos"),
    ("Покрова Пресвете Богородице",
     "the Protection of the Most Holy Theotokos"),
    ("Ваведења Пресвете Богородице",
     "the Entrance of the Most Holy Theotokos"),
    ("Благовијести Пресвете Богородице",
     "the Annunciation of the Most Holy Theotokos"),
    ("Благовести Пресвете Богородице",
     "the Annunciation of the Most Holy Theotokos"),
    ("Пресвете Богородице Тројеручице",
     "the Three-Handed Icon of the Most Holy Theotokos"),
    ("Пресвете Богородице",
     "the Most Holy Theotokos"),
    ("Сабора српских светитеља", "the Synaxis of the Serbian Saints"),
    ("Сабор Срба светитеља", "the Synaxis of the Serbian Saints"),
    ("Света три јерарха", "the Three Holy Hierarchs"),
    ("Сабор Светог архангела Гаврила",
     "the Synaxis of the Archangel Gabriel"),
    ("Сабор Светог архангела Михаила",
     "the Synaxis of the Archangel Michael"),
    ("Воздвижења Часног крста", "the Exaltation of the Holy Cross"),
    ("Воздвижења Часног Крста", "the Exaltation of the Holy Cross"),
    ("Часног крста", "the Holy Cross"),
    ("Преображења Господњег", "the Transfiguration of the Lord"),
    ("Вазнесења Господњег", "the Ascension of the Lord"),
    ("Васкрсења Христовог", "the Resurrection of Christ"),
    ("Рођења Светог Јована Крститеља",
     "the Nativity of Saint John the Baptist"),
    ("Рођења св. Јована Крститеља",
     "the Nativity of Saint John the Baptist"),
    ("Зачеће Св. Јована Крститеља",
     "the Conception of Saint John the Baptist"),
    ("Преноса моштију Светог оца Николаја",
     "the Translation of the Relics of Saint Nicholas"),
    ("Пренос моштију светог Николе",
     "the Translation of the Relics of Saint Nicholas"),
    ("Преноса Моштију Св. оца Николаја",
     "the Translation of the Relics of Saint Nicholas"),
    ("Светих апостола Петра и Павла",
     "Saints Peter and Paul"),
    ("Св. ап. Петра и Павла", "Saints Peter and Paul"),
    ("Св. Апостола Петра и Павла", "Saints Peter and Paul"),
    ("Св. царева Константина и Јелене",
     "Saints Constantine and Helen"),
    ("Св. равноапостолних Константина и Јелене",
     "Saints Constantine and Helen, Equal-to-the-Apostles"),
    ("Светих равноапостолних Кирила и Методија",
     "Saints Cyril and Methodius, Equal-to-the-Apostles"),
    ("Светог Јована Богослова", "Saint John the Theologian"),
    ("Св. Јована Богослова", "Saint John the Theologian"),
    ("Светог Василија Острошког", "Saint Basil of Ostrog"),
    ("Св. Василија Острошког", "Saint Basil of Ostrog"),
    ("Светог Петра Цетињског", "Saint Peter of Cetinje"),
    ("Св. Петра Цетињског", "Saint Peter of Cetinje"),
    ("Светог краља Стефана Дечанског", "Saint Stephen of Decani"),
    ("Светог праведног Теодора Ушакова",
     "Saint Righteous Theodore Ushakov"),
    ("Св. кнеза Лазара Косовског", "Saint Prince Lazar of Kosovo"),
    ("Светог кнеза Лазара", "Saint Prince Lazar"),
    ("Св. кнеза Лазара", "Saint Prince Lazar"),
    ("Св. деспота Стефана Лазаревића и преп. мајке Евгеније",
     "Saint Stefan Lazarevic and Venerable Mother Eugenia"),
    ("Светог архангела Михаила", "Saint Archangel Michael"),
    ("Св. Архангела Михаила", "Saint Archangel Michael"),
    ("Светог архангела Гаврила", "Saint Archangel Gabriel"),
    ("Св. арханг. Гаврила", "Saint Archangel Gabriel"),
    ("Светог архиђакона Стефана", "Saint Archdeacon Stephen"),
    ("Св. архиђакона Стефана", "Saint Archdeacon Stephen"),
    ("Светог великомученика Георгија", "Saint Great Martyr George"),
    ("Светог великомученика Димитрија",
     "Saint Great Martyr Demetrios"),
    ("Светог великомученика Пантелејмона",
     "Saint Great Martyr Panteleimon"),
    ("Светог великомученика Прокопија",
     "Saint Great Martyr Procopius"),
    ("Св. вмч. Георгија", "Saint Great Martyr George"),
    ("Св. вмч. Пантелејмона", "Saint Great Martyr Panteleimon"),
    ("Св. вмч. Прокопија", "Saint Great Martyr Procopius"),
    ("Св. вмуч. Пантелејмона", "Saint Great Martyr Panteleimon"),
    ("Св. вмуч. Марине", "Saint Great Martyr Marina"),
    ("Св. великомученице Недеље", "Saint Great Martyr Kyriaki"),
    ("Свете великомученице Недеље", "Saint Great Martyr Kyriaki"),
    ("Свете првомученице Текле", "Saint Protomartyr Thekla"),
    ("Светог цара Константина и царице Јелене",
     "Saints Emperor Constantine and Empress Helen"),
    ("Св. цара Константина и царице Јелене",
     "Saints Emperor Constantine and Empress Helen"),
    ("Свете Матроне Московске", "Saint Matrona of Moscow"),
    ("Св. Матроне Московске", "Saint Matrona of Moscow"),
    ("Светог Николаја Мирликијског", "Saint Nicholas of Myra"),
    ("Светог Сергија Радоњешког", "Saint Sergius of Radonezh"),
    ("Св. Сергија Радоњешког", "Saint Sergius of Radonezh"),
    ("Свети Никола - Ободски манастир",
     "Saint Nicholas - Obod Monastery"),
    ("Храм Покрова Пресвете Богородице",
     "Church of the Protection of the Most Holy Theotokos"),
    ("Храм Рођења Пресвете Богородице",
     "Church of the Nativity of the Most Holy Theotokos"),
    ("Храм Успења Пресвете Богородице",
     "Church of the Dormition of the Most Holy Theotokos"),
    ("Храм Преображења Господњег",
     "Church of the Transfiguration of the Lord"),
    ("Храм Вазнесења Господњег",
     "Church of the Ascension of the Lord"),
    ("Храм Светог", "Church of Saint"),
    ("Храм Свете", "Church of Saint"),
    ("Храм Св.", "Church of Saint"),
    ("Светог пророка Илије", "Saint Prophet Elijah"),
    ("Св. пророка Илије", "Saint Prophet Elijah"),
    ("Светога пророка Илије", "Saint Prophet Elijah"),
    ("Светог апостола Марка", "Saint Apostle Mark"),
    ("Св. ап. и Јеванђ. Марка", "Saint Apostle and Evangelist Mark"),
    ("Св. ап. и јев. Марка", "Saint Apostle and Evangelist Mark"),
    ("Светог апостола Томе", "Saint Apostle Thomas"),
    ("Св. Апостола Томе", "Saint Apostle Thomas"),
    ("Светог Јована Крститеља", "Saint John the Baptist"),
    ("Св. Јована Крститеља", "Saint John the Baptist"),
    ("Светог Николе", "Saint Nicholas"),
    ("Светог Николаја", "Saint Nicholas"),
    ("Св. Николе", "Saint Nicholas"),
    ("Св. Николаја", "Saint Nicholas"),
    ("Светог Саве", "Saint Sava"),
    ("Светога Саве", "Saint Sava"),
    ("Св. Саве", "Saint Sava"),
    ("Светог Димитрија", "Saint Demetrios"),
    ("Св. Димитрија", "Saint Demetrios"),
    ("Светог Ђорђа", "Saint George"),
    ("Св. Ђорђа", "Saint George"),
    ("Светог Георгија", "Saint George"),
    ("Светог Пантелејмона", "Saint Panteleimon"),
    ("Св. Пантелејмона", "Saint Panteleimon"),
    ("Светог Василија", "Saint Basil"),
    ("Св. Василија", "Saint Basil"),
    ("Светог Спиридона", "Saint Spyridon"),
    ("Св. Спиридона", "Saint Spyridon"),
    ("Светог Сергија и Вакха", "Saints Sergius and Bacchus"),
    ("Св. Сергија и Вакха", "Saints Sergius and Bacchus"),
    ("Свете Параскеве", "Saint Paraskeva"),
    ("Св. Параскеве", "Saint Paraskeva"),
    ("Свете Петке", "Saint Paraskeva"),
    ("Св. Петке", "Saint Paraskeva"),
    ("Преподобне мати Параскеве - Свете Петке",
     "Venerable Mother Paraskeva"),
    ("Преподобне Параскеве-Петке", "Venerable Paraskeva"),
    ("Свих Светих", "All Saints"),
    ("Светог Богојављења", "the Theophany of the Lord"),
    ("Васкрсења Господњег", "the Resurrection of the Lord"),
    ("Св. Тројице", "the Holy Trinity"),
    ("Светог Саве српског", "Saint Sava of Serbia"),
    ("Епархије бихаћке", "the Bihac Eparchy"),
    ("Српска православна парохија", ""),
    ("Српска православна", "Serbian Orthodox"),
    ("Светог великомученика", "Saint Great Martyr"),
    ("Свете великомученице", "Saint Great Martyr"),
    ("Светих великомученика", "Saint Great Martyrs"),
    ("Светог апостола и јеванђелисте",
     "Saint Apostle and Evangelist"),
    ("Светог апостола", "Saint Apostle"),
    ("Светих апостола", "Saints Apostles"),
    ("Светог пророка", "Saint Prophet"),
    ("Светог архангела", "Saint Archangel"),
    ("Светог арханђела", "Saint Archangel"),
    ("Светог архиђакона", "Saint Archdeacon"),
    ("Светог праведног", "Saint Righteous"),
    ("Светог кнеза", "Saint Prince"),
    ("Светог краља", "Saint King"),
    ("Преподобне мати", "Venerable Mother"),
    ("Преподобне", "Venerable"),
    ("великомученика", "Great Martyr"),
    ("великомученице", "Great Martyr"),
    ("великомученици", "Great Martyrs"),
    ("првомученика", "Protomartyr"),
    ("мученика", "Martyr"),
    ("мученице", "Martyr"),
    ("велмуч.", "Great Martyr"),
    ("велмуч", "Great Martyr"),
    ("равноапостолних", "Equal-to-the-Apostles"),
    ("апостола и јеванђелисте", "Apostle and Evangelist"),
    ("апостола", "Apostle"),
    ("јеванђелисте", "Evangelist"),
    ("пророка", "Prophet"),
    ("архиђакона", "Archdeacon"),
    ("архангела", "Archangel"),
    ("арханђела", "Archangel"),
    ("праведног", "Righteous"),
    ("кнеза", "Prince"),
    ("оца", ""),
    ("мати", "Mother"),
    ("вмч.", "Great Martyr"),
    ("вмуч.", "Great Martyr"),
    ("влмч.", "Great Martyr"),
    ("вмч", "Great Martyr"),
    ("вмуч", "Great Martyr"),
    ("влмч", "Great Martyr"),
    ("ап.", "Apostle"),
    ("јев.", "Evangelist"),
    ("јеванђ.", "Evangelist"),
    ("Св.", "Saint"),
    ("Светога", "Saint"),
    ("Светог", "Saint"),
    ("Свети", "Saint"),
    ("Свете", "Saint"),
    ("Светих", "Saints"),
    ("Параскеве", "Paraskeva"),
    ("Петке", "Paraskeva"),
    ("Георгија", "George"),
    ("Ђорђа", "George"),
    ("Пантелејмона", "Panteleimon"),
    ("Прокопија", "Procopius"),
    ("Николаја", "Nicholas"),
    ("Николе", "Nicholas"),
    ("Никола", "Nicholas"),
    ("Димитрија", "Demetrios"),
    ("Василија", "Basil"),
    ("Михаила", "Michael"),
    ("Гаврила", "Gabriel"),
    ("Јована", "John"),
    ("Крститеља", "the Baptist"),
    ("Стефана", "Stephen"),
    ("Петра", "Peter"),
    ("Павла", "Paul"),
    ("Илије", "Elijah"),
    ("Марка", "Mark"),
    ("Марине", "Marina"),
    ("Лазара", "Lazarus"),
    ("Константина", "Constantine"),
    ("Јелене", "Helen"),
    ("Томе", "Thomas"),
    ("Спиридона", "Spyridon"),
    ("српског", "of Serbia"),
    ("српских", "Serbian"),
    ("Ктиторска", "Founder's"),
    ("Спомен", "Memorial"),
    ("спомен", "memorial"),
    ("Парохија", ""),
    ("парохија", ""),
    ("Саборни", "Cathedral"),
    ("храму", "church"),
    ("налази се", ""),
    ("Молитвени дом", "Prayer House"),
    ("насеље", "settlement"),
    ("насељу", "settlement"),
    ("Сјевер", "North"),
    ("варош", "town"),
    ("граду", "town"),
    ("брду", "hill"),
    ("под", "below"),
    ("од", "from"),
    ("године", ""),
    ("нова", "new"),
    ("Горњи", "Upper"),
    ("Горња", "Upper"),
    ("Горње", "Upper"),
    ("Горњем", "Upper"),
    ("Горњој", "Upper"),
    ("Доњи", "Lower"),
    ("Доња", "Lower"),
    ("Доње", "Lower"),
    ("Доњем", "Lower"),
    ("Доњој", "Lower"),
    ("Доњим", "Lower"),
    ("Стари", "Old"),
    ("Старом", "Old"),
    ("Нови", "New"),
    ("Ново", "New"),
    ("при", "at"),
    ("жена Мироносица", "the Myrrh-bearing Women"),
    ("Другом свјетском рату", "Second World War"),
    ("Градском гробљу", "City Cemetery"),
    ("градском гробљу", "city cemetery"),
    ("Спомен комплексу", "Memorial Complex"),
    ("спомен-костурница", "memorial ossuary"),
    ("Спомен-капела", "Memorial Chapel"),
    ("Гробљанска капела", "Cemetery Chapel"),
    ("парохијски храм", "parish church"),
    ("манастирски храм", "monastery church"),
    ("манастиру", "monastery"),
    ("ман.", "monastery"),
    ("Манастир", "Monastery"),
    ("Филијални храм", "dependent church"),
    ("Саборни храм", "cathedral"),
    ("Катедрални храм", "cathedral"),
    ("Парохијски храм", "parish church"),
    ("Храм", "Church"),
    ("Црква", "Church"),
    ("Капела", "Chapel"),
    ("капела", "chapel"),
    ("гробље", "cemetery"),
    ("гробљу", "cemetery"),
    ("Богородице", "the Theotokos"),
    ("Господњег", "of the Lord"),
    ("Христовог", "of Christ"),
    ("Свете Тројице", "the Holy Trinity"),
    ("Пресвете Тројице", "the Holy Trinity"),
    ("Благовијести", "the Annunciation"),
    ("Благовести", "the Annunciation"),
    ("Богојављења", "the Theophany"),
    ("При храму", "at the church of"),
    ("при храму", "at the church of"),
    ("у изградњи", "under construction"),
    ("стари храм", "old church"),
    ("нови храм", "new church"),
    ("Општина", "Municipality of"),
    ("селу", "the village of"),
    ("село", "the village of"),
    ("код", "near"),
    ("у", "in"),
    ("на", "at"),
    ("и", "and"),
    ("Прва", "First"),
    ("Први", "First"),
    ("Друга", "Second"),
    ("Други", "Second"),
    ("Трећа", "Third"),
    ("Трећи", "Third"),
    ("Четврта", "Fourth"),
    ("Пета", "Fifth"),
    ("Шеста", "Sixth"),
    ("Седма", "Seventh"),
)


def translate_serbian_label(value):
    text = re.sub(r"\s+", " ", value).strip()
    for source, target in sorted(
            ENGLISH_PHRASES, key=lambda item: len(item[0]), reverse=True):
        pattern = r"(?<!\w)%s(?!\w)" % re.escape(source)
        text = re.sub(pattern, target, text, flags=re.IGNORECASE)
    text = transliterate(text)
    text = text.replace("„", '"').replace("“", '"')
    text = text.replace("Memorial-Church", "Memorial Church")
    text = text.replace("Cathedral Church", "Cathedral")
    text = re.sub(r"\bChurch the\b", "Church of the", text)
    text = re.sub(r"\bChurch (Saints?|Venerable)\b", r"Church of \1", text)
    text = re.sub(
        r"\s*-\s*(?=(?:New|Cathedral|Church|Memorial)\b)",
        " - ", text,
    )
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.)])", r"\1", text)
    text = re.sub(r"([(])\s+", r"\1", text)
    text = text.strip(" -,")
    return text[:1].upper() + text[1:]


def slug(value):
    value = transliterate(value)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value
                    if not unicodedata.combining(char))
    value = value.lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def english_name(local, rank):
    text = re.sub(r"\s+", " ", local).strip()
    if rank == "Parish":
        ordinal = {
            "1": "First", "2": "Second", "3": "Third",
            "4": "Fourth", "5": "Fifth", "6": "Sixth",
            "7": "Seventh",
        }
        leading = re.match(r"^([1-7])\.\s*(.*?)$", text)
        if leading:
            text = "%s %s" % (ordinal[leading.group(1)], leading.group(2))
        roman_number = {
            "I": "First", "II": "Second", "III": "Third",
            "IV": "Fourth", "V": "Fifth", "VI": "Sixth",
        }
        leading_roman = re.match(r"^(I|II|III|IV|V|VI)\s+(.*?)$", text)
        if leading_roman:
            text = "%s %s" % (
                roman_number[leading_roman.group(1)],
                leading_roman.group(2),
            )
        match = re.match(r"^(.*?)([1-7])\.\s*парохија$", text,
                         flags=re.IGNORECASE)
        if match:
            text = "%s %s" % (ordinal[match.group(2)], match.group(1))
        text = re.sub(r"^(Прва|Друга|Трећа|Четврта|Пета|Шеста|Седма)\s+парохија\s+",
                      r"\1 ", text, flags=re.IGNORECASE)
        text = re.sub(r"^Парохија\s+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+парохија$", "", text, flags=re.IGNORECASE)
        roman = re.match(r"^(.*?)\s+(I|II|III|IV|V|VI)$", text)
        if roman:
            number = roman_number[roman.group(2)]
            text = "%s %s" % (number, roman.group(1))
    else:
        text = re.sub(
            r"^(?:Манастирски скит|Манастирски храм|Гробљанска капела|"
            r"Парохијски храм|Филијални храм|Саборни храм|"
            r"Катедрални храм|Српска православна|МАНАСТИР|Манастир|"
            r"Црква|Храм|Капела)\s*(?:-\s*)?",
            "", text, flags=re.IGNORECASE,
        )
    text = translate_serbian_label(text)
    if rank == "Parish":
        trailing_ordinal = re.match(
            r"^(.*?)\s+(First|Second|Third|Fourth|Fifth|Sixth|Seventh)$",
            text,
        )
        if trailing_ordinal:
            text = "%s %s" % (
                trailing_ordinal.group(2), trailing_ordinal.group(1),
            )
    return "Serbian Orthodox %s: %s" % (rank, text)


def unique_id(prefix, local, seen):
    base = prefix + "-" + slug(local)
    row_id = base
    index = 2
    while row_id in seen:
        row_id = "%s-%d" % (base, index)
        index += 1
    seen.add(row_id)
    return row_id


def row(row_id, parent, country, local, source, rank="Parish",
        kind="parish"):
    return {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": english_name(local, rank),
        "local": local,
        "country": country,
        "sources": [source],
    }


def site_rank(local):
    upper = local.upper()
    if "ИЗГРАДЊ" in upper:
        return "Church Under Construction"
    if "САБОРНИ" in upper or "КАТЕДРАЛНИ" in upper:
        return "Cathedral"
    if "СКИТ" in upper:
        return "Skete"
    if "ГРОБЉ" in upper and "КАПЕЛ" in upper:
        return "Cemetery Chapel"
    if "ГРОБЉ" in upper:
        return "Cemetery Church"
    if "КАПЕЛ" in upper:
        return "Chapel"
    if "МОЛИТВ" in upper:
        return "Prayer House"
    return "Church"


def monastery_rank(local):
    if "СКИТ" in local.upper():
        return "Skete"
    return "Monastery"


def simple_rows(parent, country, prefix, values, source, rank="Parish",
                kind="parish", seen=None):
    seen = seen if seen is not None else {parent}
    return [
        row(unique_id(prefix, local, seen), parent, country, local, source,
            rank=rank(local) if callable(rank) else rank, kind=kind)
        for local in values
    ]


def sourced_rows(parent, country, prefix, values, rank="Parish",
                  kind="parish", seen=None):
    seen = seen if seen is not None else {parent}
    return [
        row(unique_id(prefix, local, seen), parent, country, local, source,
            rank=rank(local) if callable(rank) else rank, kind=kind)
        for local, source in values
    ]


ZT_DIRECT_SITES = {
    "4673": (
        "ba-sr-zt-cemetery-church-pucile",
        "Храм Светог архиђакона Стефана на Градском гробљу "
        "„Пучиле“ у Бијељини",
        "Cemetery Church",
    ),
}


def zt_rows():
    parent = "sr-zvornik-tuzla"
    seen = {parent}
    rows = []
    physical_main = {}
    for parish in SCRAPED["zt_parishes"]:
        direct = ZT_DIRECT_SITES.get(parish["key"])
        if direct:
            row_id, local, rank = direct
            if row_id in seen:
                raise ValueError("duplicate Zvornik-Tuzla direct-site id")
            seen.add(row_id)
            rows.append(row(
                row_id, parent, "BA", local, parish["url"], rank=rank,
            ))
            continue
        parish_id = "ba-sr-zt-parish-" + parish["key"]
        if parish_id in seen:
            raise ValueError("duplicate Zvornik-Tuzla parish id")
        seen.add(parish_id)
        rows.append(row(
            parish_id, parent, "BA", parish["local"], parish["url"],
        ))
        for local in parish["sites"]:
            local = ZT_SITE_REPLACEMENTS.get(
                (parish["key"], local), local,
            )
            if local is None:
                continue
            values = local if isinstance(local, list) else [local]
            for value in values:
                key = re.sub(r"\s+", " ", value.casefold()).strip()
                if (not value.startswith("Филијални") and
                        key in physical_main):
                    continue
                if not value.startswith("Филијални"):
                    physical_main[key] = parish_id
                rank = site_rank(value)
                rows.append(row(
                    unique_id(parish_id + "-site", value, seen),
                    parish_id, "BA", value, parish["url"], rank=rank,
                ))
    rows.extend(sourced_rows(
        parent, "BA", "ba-sr-zt-monastery",
        ZT_CURRENT_MONASTERIES,
        rank=monastery_rank, kind="monastery", seen=seen,
    ))
    return rows


BP_CURRENT_ALIASES = {
    "герзовачко-бараћке", "iii петровачке", "ii петровачке",
    "i петровачке", "рујишко-дубовичке", "старомајданске",
    "оштролучке", "бушевићко-блатњанске", "i дрварске",
    "ii дрварске", "бабићке", "буковачко-дринићке",
    "бјелајачке", "бихаћке", "крњеушко-вођеничке",
    "гламочке", "санске",
}

BP_SITE_REPLACEMENTS = {
    "Св. Тројице у Блатној. (Храм је у изградњи од 2006.године)":
        "Св. Тројице у Блатној (храм у изградњи)",
}

BP_SITE_EXCLUSIONS = {
    (
        "Мартинбродска",
        "Манастирски храм св. оца Николаја у манастиру Рмњу",
    ),
    (
        "Соколовачко-козичка",
        "Парохијски храм Успења Пресвете Богородице у Соколову",
    ),
    (
        "Веселинска",
        "Манастирски храм Рођења св. Јована Крститеља у ман. Веселиње",
    ),
    (
        "Губинско-врбичка",
        "Парохијски храм Успења Пресвете Богородице у Губину, "
        "Општина Ливно. Црквено-народни сабор Убрус - "
        "Нерукотвореног Лика Господа Исуса Христа",
    ),
}

ZT_SITE_REPLACEMENTS = {
    ("48", "Храм Светог великомученика Георгија"):
        "Храм Светог великомученика Георгија у Бијељини",
    ("49", "Храм Светог великомученика Георгија у Бијељини"):
        "Храм Светог великомученика Георгија у Бијељини",
    ("4672", "Храм Светог великомученика Георгија"):
        "Храм Светог великомученика Георгија у Бијељини",
    ("50", "Саборни храм Рођења Пресвете Богородице"):
        "Саборни храм Рођења Пресвете Богородице у Бијељини",
    ("51", "Саборни храм Рођења Пресвете Богородице у Бијељини"):
        "Саборни храм Рођења Пресвете Богородице у Бијељини",
    ("52", "Саборни храм Рођења Пресвете Богородице"):
        "Саборни храм Рођења Пресвете Богородице у Бијељини",
    ("59", "Храм Светог великомученика Пантелејмона у Бијељини"):
        "Храм Светог великомученика Пантелејмона у Бијељини - Крушик",
    ("58", "Храм Светог великомученика Пантелејмона"):
        "Храм Светог великомученика Пантелејмона у Бијељини - Крушик",
    ("4662", "Храм Светог великомученика Пантелејмона у Бијељини"):
        "Храм Светог великомученика Пантелејмона у Бијељини - Крушик",
    ("63", "Филијални храм - Д"): "Филијални храм - Д. МАГНОЈЕВИЋ",
    ("66", "Храм Сабора српских светитеља налази се у Даздареву"):
        "Храм Сабора српских светитеља у Даздареву",
    ("77", "Филијални храм - Д"): "Филијални храм - Д. ДРАГАЉЕВАЦ",
    ("83", "Филијални храм - Д"): "Филијални храм - Д. БУКОВИЦА",
    ("89", "Филијални храм"): None,
    ("99", "Филијални храм"): "Храм Успења Пресвете Богородице",
    ("4831", "Филијални храм"): None,
    ("4832", "Филијални храм"): "Храм Рођења Пресвете Богородице",
    (
        "105",
        "Храм свете великомученице Недеље је једнобродна грађевина "
        "и налази се у насељу Колобара у Брчком",
    ): "Храм Свете великомученице Недеље у насељу Колобара у Брчком",
    ("105", "Филијални храм Светих апостола Петра и Павла (2 .парохија)"):
        None,
    ("105", "Филијални храм Пренос моштију светог Николе (2"):
        None,
    (
        "107",
        "Храм Свете великомученице Недеље у насељу Колобара у Брчком",
    ): "Храм Свете великомученице Недеље у насељу Колобара у Брчком",
    ("107", "Филијални храм - ГРБАВИЦА (Св"):
        "Филијални храм - ГРБАВИЦА (Св. ап. Петра и Павла)",
    ("102", "Храм Вазнесења Господњег"):
        "Храм Вазнесења Господњег у Доњем Брезику",
    ("104", "Храм Вазнесења Господњег у Доњем Брезику"):
        "Храм Вазнесења Господњег у Доњем Брезику",
    ("114", "Филијални храмови у Баткуши и Брвнику су у оквиру 2"):
        None,
    ("115", "Филијални храм - Г"):
        "Филијални храм - Г. БУКОВИЦА",
    ("119", "Филијални храм - Г"): [
        "Филијални храм - Г. БРЕЗИК",
        "Филијални храм - Г. БРЕЗИК (гробље)",
    ],
    ("174", "Филијални храм у Плочнику припада Добојској 2"):
        None,
    ("212", "Филијални храм - ЂУРЂЕВ ГРАД - види под 2"):
        None,
    ("212", "Филијални храм - МЛАЂЕВАЦ - види под 2"):
        None,
    ("219", "Филијални храм 1"): None,
    ("221", "Филијални храм 2"): None,
    ("232", "Филијални храм Сабора српских светитеља у Церу (види под 2"):
        None,
    ("152", "Филијални храм - РИТЕШИЋ - Храм св"): [
        "Филијални храм - РИТЕШИЋ - Храм св. Јована Крститеља",
        "Филијални храм - РИТЕШИЋ - Храм св. Василија Великог",
    ],
    ("162", "Филијални храм - ГРОБЉЕ В"):
        "Филијални храм - ГРОБЉЕ В. СОЧАНИЦА",
    ("97", "Храм Светог пророка Илије у Пелагићеву"):
        "Храм Светога пророка Илије у Пелагићеву",
    (
        "134",
        "Капела Светог апостола Томе у Спомен комплексу Чардак - Дервента",
    ): None,
    ("136", "Храм Успења Пресвете Богородице у Дервенти"):
        "Саборни храм Успења Пресвете Богородице у Дервенти",
    ("137", "Храм Успења Пресвете Богородице у Дервенти"):
        "Саборни храм Успења Пресвете Богородице у Дервенти",
    ("4879", "Храм Успења Пресвете Богородице у Дервенти"):
        "Саборни храм Успења Пресвете Богородице у Дервенти",
    ("136", "Филијални храм - ЧАРДАК"):
        "Капела Светог апостола Томе у Спомен комплексу Чардак - Дервента",
    ("179", "Спомен-храм Рођења Пресвете Богородице у Добоју"):
        "Спомен храм Рођења Пресвете Богородице у Добоју",
    ("188", "Филијални храм - СЈЕНИНА РИЈЕКА"): None,
    ("219", "Храм Светих апостола Петра и Павла"):
        "Храм Светих апостола Петра и Павла у Козлуку",
    ("221", "Храм Светих апостола Петра и Павла у Козлуку"):
        "Храм Светих апостола Петра и Павла у Козлуку",
    ("245", "Храм Преподобне мати Параскеве - Свете Петке"):
        "Храм Преподобне мати Параскеве - Свете Петке у Гаревцу",
    ("252", "Храм Успења Пресвете Богородице"):
        "Храм Успења Пресвете Богородице у Модричи",
    ("254", "Храм Успења Пресвете Богородице"):
        "Храм Успења Пресвете Богородице у Модричи",
    ("256", "Храм Успења Пресвете Богородице у Модричи"):
        "Храм Успења Пресвете Богородице у Модричи",
    ("257", "Храм Успења Пресвете Богородице"):
        "Храм Успења Пресвете Богородице у Модричи",
    ("268", "Филијални храм - ГРОБЉЕ (Капела св"):
        "Филијални храм - ГРОБЉЕ (Капела св. кнеза Лазара)",
    ("270", "Филијални храм - ГРОБЉЕ (КАПЕЛА СВ"):
        "Филијални храм - ГРОБЉЕ (КАПЕЛА СВ. АП. МАРКА)",
    ("359", "Храм Светог Јована Крститеља у Тобуту (Зачеће Св"):
        "Храм Светог Јована Крститеља у Тобуту "
        "(Зачеће Св. Јована Крститеља)",
    ("316", "Храм Пресвете Тројице у Теслићу"):
        "Спомен храм Пресвете Тројице у Теслићу",
    ("4677", "Храм Пресвете Тројице"):
        "Спомен храм Пресвете Тројице у Теслићу",
    ("4857", "Храм Пресвете Тројице"):
        "Спомен храм Пресвете Тројице у Теслићу",
    ("4857", "Филијални храм - ЖАРКОВИНА"): None,
    ("392", "Храм свете Петке у Угљевику"):
        "Храм Преподобне мати Параскеве - Свете Петке у Угљевику",
    (
        "132",
        "Филијални храмови: ГОРЊА ВРЕЛА, ВЕЛИКА БРУСНИЦА, "
        "МАЛА БРУСНИЦА, МАЛА БРУСНИЦА - гробље, ГРК, "
        "ДОЊИ КЛАКАР, САБАШТАН, ВИНСКА - гробље, "
        "ВИНСКА - гробље нова капела, УНКА, ДУБОКОВАЦ",
    ): [
        "Филијални храм - ГОРЊА ВРЕЛА",
        "Филијални храм - ВЕЛИКА БРУСНИЦА",
        "Филијални храм - МАЛА БРУСНИЦА",
        "Филијални храм - МАЛА БРУСНИЦА - гробље",
        "Филијални храм - ГРК",
        "Филијални храм - ДОЊИ КЛАКАР",
        "Филијални храм - САБАШТАН",
        "Филијални храм - ВИНСКА - гробље",
        "Филијални храм - ВИНСКА - гробље нова капела",
        "Филијални храм - УНКА",
        "Филијални храм - ДУБОКОВАЦ",
    ],
}


def bp_rows():
    parent = "sr-bihac-petrovac"
    seen = {parent}
    rows = []
    physical_sites = set()
    for parish in BP_CORRECTED:
        parish_id = unique_id(
            "ba-sr-bp-parish", parish["local"], seen,
        )
        rows.append(row(
            parish_id, parent, "BA", parish["local"], BP_ROSTER,
        ))
        for local in parish["sites"]:
            if (parish["local"], local) in BP_SITE_EXCLUSIONS:
                continue
            local = BP_SITE_REPLACEMENTS.get(local, local)
            key = re.sub(r"\s+", " ", local.casefold()).strip()
            if key in physical_sites:
                continue
            physical_sites.add(key)
            rank = site_rank(local)
            rows.append(row(
                unique_id(parish_id + "-site", local, seen),
                parish_id, "BA", local, BP_ROSTER, rank=rank,
            ))
    for local in SCRAPED["bp_current"]:
        if local.casefold() in BP_CURRENT_ALIASES:
            continue
        rows.append(row(
            unique_id("ba-sr-bp-current-parish", local, seen),
            parent, "BA", local, BP_ADDRESS,
        ))
    rows.extend(simple_rows(
        parent, "BA", "ba-sr-bp-monastery",
        MANUAL["bp_monasteries"], BP_ADDRESS,
        rank=monastery_rank, kind="monastery", seen=seen,
    ))
    return rows


def zah_rows():
    parent = "sr-zahumlje-herzegovina"
    seen = {parent}
    rows = []
    rows.extend(simple_rows(
        parent, "BA", "ba-sr-zah-parish",
        MANUAL["zah_ba_parishes"], ZAH_ROSTER, seen=seen,
    ))
    rows.extend(simple_rows(
        parent, "BA", "ba-sr-zah-monastery",
        MANUAL["zah_ba_monasteries"], ZAH_MONASTERIES,
        rank=monastery_rank, kind="monastery", seen=seen,
    ))
    me_parishes = simple_rows(
        parent, "ME", "me-sr-zah-parish",
        MANUAL["zah_me_parishes"], ZAH_SUTORINA, seen=seen,
    )
    rows.extend(me_parishes)
    me_parent = me_parishes[0]["id"]
    rows.extend(simple_rows(
        me_parent, "ME", "me-sr-zah-church",
        MANUAL["zah_me_churches"], ZAH_SUTORINA,
        rank=site_rank, seen=seen,
    ))
    return rows


def build_rows():
    return {
        "sr-banja-luka": sourced_rows(
            "sr-banja-luka", "BA", "ba-sr-bl-monastery",
            BANJA_CURRENT_MONASTERIES,
            rank=monastery_rank, kind="monastery",
        ),
        "sr-bihac-petrovac": bp_rows(),
        "sr-budimlja-niksic": (
            simple_rows(
                "sr-budimlja-niksic", "ME", "me-sr-bn-parish",
                MANUAL["bn_parishes"], BN_PARISHES,
            )
            + simple_rows(
                "sr-budimlja-niksic", "ME", "me-sr-bn-monastery",
                MANUAL["bn_monasteries"], BN_MONASTERIES,
                rank=monastery_rank, kind="monastery",
            )
        ),
        "sr-dabar-bosna": simple_rows(
            "sr-dabar-bosna", "BA", "ba-sr-db-monastery",
            MANUAL["dabar_monasteries"], DABAR_MONASTERIES,
            rank=monastery_rank, kind="monastery",
        ),
        "sr-milesevo": (
            simple_rows(
                "sr-milesevo", "ME", "me-sr-mil-parish",
                MANUAL["mil_parishes"], MILESEVA_PLJEVLJA,
            )
            + simple_rows(
                "sr-milesevo", "ME", "me-sr-mil-church",
                MANUAL["mil_churches"], MILESEVA_PLJEVLJA,
                rank=site_rank,
            )
            + simple_rows(
                "sr-milesevo", "ME", "me-sr-mil-monastery",
                MANUAL["mil_monasteries"], MILESEVA_PLJEVLJA,
                rank=monastery_rank, kind="monastery",
            )
        ),
        "sr-montenegro-littoral": (
            simple_rows(
                "sr-montenegro-littoral", "ME", "me-sr-mcl-parish",
                MANUAL["mcl_parishes"], MCL_PARISHES,
            )
            + simple_rows(
                "sr-montenegro-littoral", "ME", "me-sr-mcl-church",
                MCL_CHURCHES, MCL_PARISHES, rank=site_rank,
            )
            + simple_rows(
                "sr-montenegro-littoral", "ME", "me-sr-mcl-monastery",
                MANUAL["mcl_monasteries"], MCL_MONASTERIES,
                rank=monastery_rank, kind="monastery",
            )
        ),
        "sr-zahumlje-herzegovina": zah_rows(),
        "sr-zvornik-tuzla": zt_rows(),
    }


ROWS = build_rows()
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in ROWS.values()
    for item in source_rows
}

EXPECTED = {
    "sr-banja-luka": 8,
    "sr-bihac-petrovac": 164,
    "sr-budimlja-niksic": 77,
    "sr-dabar-bosna": 8,
    "sr-milesevo": 19,
    "sr-montenegro-littoral": 189,
    "sr-zahumlje-herzegovina": 30,
    "sr-zvornik-tuzla": 611,
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
    return out


def build():
    payloads = {}
    all_seen = set(ROWS)
    for parent, source_rows in ROWS.items():
        rows = []
        branch_seen = {parent}
        countries = set()
        for source in source_rows:
            item = clean(source)
            row_id = item.get("id")
            if not row_id or row_id in all_seen:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if item.get("parent") not in branch_seen:
                raise ValueError("%s hangs off an unknown branch parent: %s" %
                                 (row_id, item.get("parent")))
            if item.get("kind") not in {"parish", "monastery"}:
                raise ValueError("%s has unsupported kind" % row_id)
            if item.get("country") not in {"BA", "ME"}:
                raise ValueError("%s has invalid country" % row_id)
            if not item.get("local"):
                raise ValueError("%s has no local name" % row_id)
            if any(mark in json.dumps(item, ensure_ascii=False)
                   for mark in ("\u2013", "\u2014", "\ufffd")):
                raise ValueError("%s has forbidden punctuation or encoding" %
                                 row_id)
            all_seen.add(row_id)
            branch_seen.add(row_id)
            countries.add(item["country"])
            rows.append(item)
        payload = {"v": 1, "parent": parent, "rows": rows}
        if len(countries) == 1:
            payload["country"] = next(iter(countries))
        else:
            payload["countries"] = sorted(countries)
        payloads[parent] = payload
    counts = {parent: len(payload["rows"])
              for parent, payload in payloads.items()}
    if counts != EXPECTED:
        raise ValueError("Bosnia and Montenegro counts changed: %r" % counts)
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
        print("directory Bosnia and Montenegro: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    total = sum(len(payload["rows"]) for payload in payloads.values())
    print("Bosnia and Montenegro: %d verified bodies across %d canonical parents"
          % (total, len(payloads)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
