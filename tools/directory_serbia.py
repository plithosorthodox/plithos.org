#!/usr/bin/env python3
"""Validated directory fragments for Serbia.

Current first-party diocesan rosters are reproduced as discrete deaneries,
parishes, church communities, churches, chapels, worship sites, and
monasteries. Public count-only and inaccessible roster gaps remain in the
companion candidate ledger.

    python tools/directory_serbia.py --check
    python tools/directory_serbia.py --dump
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse

import directory_bosnia_montenegro as serbian


CHECKED = "2026-11-15"

NIS_ROOT = "https://eparhijaniska.rs/parohije"
NIS_DATA = json.loads(r'''{"parishes":[{"label":"Алексинац","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/aleksincke-parohije","count":4,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6336-aleksinačke-parohije-hramovi","temples":["Храм преноса моштију светог оца Николаја","Храм светих Архангела Михаила и Гаврила на Алексиначком гробљу","Храм светог Пророка Илије у Суботинцу","Храм Св. Великомученика Пантелејмона у Краљеву","Капела светих Апостола Петра и Павла у Краљеву","Храм Свете Тројице у Глоговици","Храм светог Јована Крститеља у Алексиначком Бујмиру"]},{"label":"Чукуровац","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/cukurovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6368-čukurovačka-parohija-hramovi","temples":["Храм Светог великомученика Прокопија у Чукуровцу","Храм Светог Николаја у Вукањи","Храм Светог великомученика Пантелејмона у Вукањи","Храм Светог Јована Крститеља у Породину","Храм Преображења Господњег у Љуптену"]},{"label":"Ђунис","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/djunisk-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6347-đuniška-parohija-hramovi","temples":["Храм Светог великомученика Пантелејмона у Ђунису","Храм Свете Петке у Ђунису","Храм Светих апостола Петра и Павла у Јошју"]},{"label":"Гредетин","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/gredetinska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6343-gredetinska-parohija-hramovi","temples":["Храм Покрова Пресвете Богородице у Гредетину","Храм Свете Марије Магдалине у Радевцу","Храм Светих Константина и Јелене у Лозанцу","Храм Светог архиђакона Стефана у Каменици"]},{"label":"Грејач","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/grejacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6344-grejačka-parohija-hramovi","temples":["Храм Вазнесења Господњег у Грејачу","Храм Свете великомученице Параскеве у Великом Дреновцу","Храм Свете Варваре у Малом Дреновцу","Храм Светих Константина и Јелене у Лоћики"]},{"label":"Каоник","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/kaonicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6349-kaonička-parohija-hramovi","temples":["Храм Свете великомученице Недеље у Каонику","Храм Свете Петке у Каонику","Храм Усековања главе Светог Јована Крститеља у Каонику","Храм Покрова Пресвете Богородице у Каонику","Храм Светог мученика Мине у Каонику","Црква Светог апостола Вартоломеја у Каонику","Храм Свете Марије Магдалине у Каонику","Храм Свете Параскеве у Каонику","Храм Вазнесења Господњег у Црквини","Храм Светог Атанасија Великог у Малом Шиљеговцу"]},{"label":"Мозгово","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/mozgovska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6352-mozgovska-parohija-hramovi","temples":["Храм Свете Тројице у Мозгову","Храм Свете Преподобномученице Параскеве у Мозгову (Река)","Храм Светог архангела Гаврила у Бовну"]},{"label":"Рибаре","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/ribarska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6354-ribarska-parohija-hramovi","temples":["Храм Светог пророка Илије у Рибару","Храм Свете Тројице у Рибару","Храм Светог апостола Марка у Бољевцу","Храм Светих Константина и Јелене у Великом Крушинцу","Храм Светог Антонија Великог у Гревцима","Храм Светог Алимпија Столпника у Зубовцу","Храм Свете Петке у Росици"]},{"label":"Рутевац","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/rutevacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6356-rutevačka-parohija-hramovi","temples":["Храм Свете великомученице Марине у Рутевцу","Храм Светих Архангела Михаила и Гаврила у Делиграду"]},{"label":"Станци","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/stanacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6358-stanačka-parohija-hramovi","temples":["Храм Светог Великомученика Прокопија у Катуну","Храм Преподобномученице Параскеве у Станцима","Храм Светог Јована Крститеља у Црној Бари","Капела Преподобномученице Параскеве у Катуну","Капела светих Мученика Савела, Исмаила и Мануила у Пруговцу"]},{"label":"Тешица","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/tesicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6359-tešička-parohija-hramovi","temples":["Храм Успења Пресвете Богородице у Тешици","Храм Светог Пророка Илије у Тешици","Храм Светог архангела Михаила у Лужанима"]},{"label":"Трнава","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/trnavska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6361-trnavska-parohija-hramovi","temples":["Храм Светог пророка Илије у Доњој Трнави","Храм Светих архангела у Горњој Трнави","Храм Светог Јована Крститеља у Доњем Крупцу","Храм Светог Јована Крститеља у Врелу"]},{"label":"Трњане","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/trnjanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6366-trnjanska-parohija-hramovi","temples":["Храм Преподобномученице Параскеве у Трњану"]},{"label":"Велики Шиљеговац","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/velikosiljegovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6340-velikošiljegovačka-parohija-hramovi","temples":["Храм Светог архангела Гаврила у Великом Шиљеговцу","Храм Покрова Пресвете Богородице у Великом Шиљеговцу","Храм Свете Петке у Великом Шиљеговцу","Храм Светих апостола Петра и Павла у Великом Шиљеговцу","Капела Светог Николаја у Зебици, у изградњи"]},{"label":"Житковац","url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/zitkovacke-parohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/aleksinacko-namesnistvo/6338-žitkovačke-parohije-hramovi","temples":["Храм Светог архангела Гаврила у Житковцу","Храм Светог великомученика Георгија у Моравцу","Храм Светог Јована Крститеља у Горњем Сухотну","Храм Светог пророка Илије у Доњем Сухотну у изградњи","Храм Свете Тројице у Горњем Адровцу","Храм Свете мученице Недеље у Горњем Адровцу"]},{"label":"Бабушница","url":"https://eparhijaniska.rs/parohije/belopalanacko-namesnistvo/babusnicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/belopalanacko-namesnistvo/6374-babušnička-parohija-hramovi","temples":["Храм Преноса моштију Светог Николаја Чудотворца у Бабушници","Храм Свете Тројице у Драгинцу","Храм Светог пророка Илије у Љуберађи","Храм Успења Пресвете Богородице у Стрелцу"]},{"label":"Бела Паланка","url":"https://eparhijaniska.rs/parohije/belopalanacko-namesnistvo/belopalanacke-parohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/belopalanacko-namesnistvo/6372-belopalanačke-parohije-hramovi","temples":["Храм Вазнесења Господњег у Белој Паланци","Храм Светог великомученика Георгија у Осмакову","Храм Светог архангела Гаврила у Моклишту","Храм Светог великомученика Пантелејмона у Враништу","Храм Свете Петке у Градишту","Храм Светог Илије у Клисури","Храм Светих апостола Петра и Павла у Црноклишту","Храм Светих Ћирила и Методија у Црвеној Реци","Храм Рођења Пресвете Богородице у Мокри","Храм Свете преподобномученице Параскеве у Шпају","Храм Светог Јована Крститеља у Мирановачкој Кули","Храм Светог Николаја у Горњем Стрижевцу"]},{"label":"Доњи Матејевац","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/donjematejevacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/donjematejevacka-parohija/6298-donjomatejevačka-parohija-hramovi","temples":["Храм Светог архангела Михаила у Доњем Матејевцу","Храм Свете Петке у Доњем Матејевцу","Храм Светог великомученика Георгија у Каменици","Храм светог Николаја у Каменици"]},{"label":"Доња Врежина","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/donjovrezinska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/6288-donjovrežinske-parohije-hramovi","temples":["Храм Успења Пресвете Богородице Доњој Врежини"]},{"label":"Горњи Матејевац","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/gornjematejevacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/gornjematejevacka-parohija/6297-gornjomatejevačka-parohija-hramovi","temples":["Храм Свете Тројице Русалијске или ''Латинска црква'' у Горњем Матејевцу","Храм Вазнесења Господњег у Горњем Матејевцу","Храм Светих апостола Петра и Павла у Горњем Матејевцу","Храм Светог пророка Илије у Кнез Селу","Храм Успења Пресвете Богородице у Кнез Селу"]},{"label":"Хум","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/humska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/humska-parohija/6304-humska-parohija-hramovi","temples":["Храм Светог оца Николаја у Хуму","Храм Преображења Господњег у Хуму","Храм Преподобне Параскеве у Рујнику","Храм Светог Архангела Гаврила у Лесковику"]},{"label":"Комрен","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/komrenske-parohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/6290-komrenske-parohije-hramovi","temples":["Храм Светог пророка Илије у Комрену","Храм Светог Саве, првог архиепископа српског у Комрену"]},{"label":"Малча","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/malcanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/malcanska-parohija/6300-malčanska-parohija-hramovi","temples":["Храм Свете Петке у Малчи","Храм Светог великомученика Димитрија у Пасјачи","Храм Свете Тројице у Горњој Врежини","Храм Рођења Светог Јована Крститеља у селу Ореовац"]},{"label":"Миљковац","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/miljkovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/miljkovacka-parohija/6303-miljkovačka-parohija-hramovi","temples":["Храм Успења Пресвете Богородице у Миљковцу","Храм Светог Николе у Миљковцу","Храм Светог Јована Крститеља у Палиграцу","Храм Свете преподобномученице Параскеве у Крављу","Храм Светог Јована Крститеља у Крављу","Храм Свете великомученице Марине у Паљини","Храм светог Романа Ђунишког у Паљини","Храм свете Петке у Церју"]},{"label":"Ниш, Храм Светог Пантелејмона","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/nis-hram-svetog-pantelejmona","count":6,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/6286-niš-hram-svetog-pantelejmona-hramovi","temples":["Храм светог великомученика и исцелитеља Пантелејмона у Нишу"]},{"label":"Сврљиг","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/svrljiske-parohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/svrljiske-parohije/6464-svrljiške-parohije-hramovi","temples":["Храм Светих царева Константина и царице Јелене у Сврљигу","Храм Светог пророка Илије у Нишевцу","Храм Светог Николаја у Драјинцу","Храм Свете Тројице у Преконоги","Храм Светог Николаја у Лалинцу","Храм Свете Тројице у Грбавче","Храм Светог пророка Илије и Светог Лазара у Грбавче","Храм Успења Пресвете Богородице у Црнољевици","Храм Светих апостола Петра и Павла у Гулијану","Храм Светих царева Константина и царице Јелене у Манојлици","Храм Свете великомученице Петке у Извору","Храм Светог апостола Марка у Белоињу"]},{"label":"Вртиште","url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/vrtiska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/drugo-nisko-namesnistvo/vrtiska-parohija/6294-vrtiška-parohija-hramovi","temples":["Храм светих апостола Петра и Павла у Вртишту"]},{"label":"Бојник","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/bojnicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6391-bojnička-parohija-hramovi","temples":["Храм Светог архангела Гаврила у Придворици","Храм Светих Апостола Петра и Павла у Доњем Коњувцу","Храм Светог великомученика Георгија у Горњем Брестовцу","Храм Светог Симеона Столпника у Плавцу","Храм Светог Спиридона у Граници","Храм Светог Пантелејмона у Ћуковцу","Храм Свете Петке у Ђинђуши","Храм Воздвижења Часног крста у Великој Црквици"]},{"label":"Бошњаце","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/bosnjacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6387-bošnjačke-parohije-hramovi","temples":["Храм Свете преподобномученице Параскеве","Храм Светог Николаја Мириликијског у Тогочевцу"]},{"label":"Горње Бријање","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/gornjebrijanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6392-gornjebrijanjska-parohija-hramovi","temples":["Храм Светог Саве у Горњем Бријању"]},{"label":"Лебане","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/lebanske-parohije","count":3,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6389-lebanske-parohije-hramovi","temples":["Храм Усековања главе Светог Јована Крститеља у Лебану","Храм Успења Пресвете Богородице у Гргуровцу","Храм Светог великомученика Прокопија у Шуману","Храм Прображења Господњег у Клајићу","Храм Светог Николаја у Липовици","Храм Светог великомученика Прокопија у Радевцу","Храм Успења Пресвете Богородице у Оргулици","Храм Светог великомученика Пантелејмона у Рафуни","Храм Свете Параскеве у Поповцу","Храм Светог Симеона Столпника у Гагинцу","Храм Успења Пресвете Богородице у селу Ђукекаре"]},{"label":"Медвеђа","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/medvedjska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6394-medveđska-parohija-hramovi","temples":["Храм Вазнесења Господњег у Медвеђи","Храм Светог Архангела Гаврила у Црном Врху Храм Светог Илије у Гајтану","Храм Светог великомученика Пантелејмона у Газдарама"]},{"label":"Прекопчелица","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/prekopcelacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6397-prekopčelička-parohija-hramovi","temples":["Храм Преноса моштију Светог Николаја Мирликијског у Прекопчелици","Храм Свете Тројице у Ображдама","Храм Свете Петке у Петровцу","Храм Светих апостола Петра и Павла у Петровој Гори","Храм Светог кнеза Лазара у Лозанама"]},{"label":"Сијаринска Бања","url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/sijarinskobanjska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/jablanicko-namesnistvo/6398-sijarinskobanjska-parohija-hramovi","temples":["Храм Светог пророка Илије у Сијaринској бањи","Храм Свете Тројице у Туларама","Храм Светог архангела Гаврила у Маћедонцу","Храм Свете Тројице у Маровцу","Храм Свете великомученице Марине у Чокотину","Храм Светог Николе у Равној Бањи","Храм Свете Петке у Станушићима","Храм Свете Петке у Гвоздићу","Храм Преображења Господњег у Сијарини"]},{"label":"Блаце","url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/blacke-parhohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/6410-blačke-parohije-hramovi","temples":["Храм Успења Пресвете Богородице у Блацу","Храм Свете Тројице у Трубњу","Храм Светог пророка Јеремије у Сибници","Храм Свете великомученице Марине у Чучалу","Храм Светог архангела Гаврила у Врбовцу","Храм Свете великомученице Марине у Претрешњи","Храм Рођења Светог Јована Крститеља у Качапору","Храм Светог пророка Илије у Горњој Драгуши","Храм Преображења Господњег у Доњој Јошаници"]},{"label":"Гргуре и Туларе","url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/grgurska-tularska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/6413-grgursko-tularska-parohija-hramovi","temples":["Храм Светог цара Константина и царице Јелене у Барбатовцу","Храм Светог Јована Крститеља у Гргуру","Храм Светог Алексија Човека Божијег у Чунгули","Храм Васкрсења Лазаревог у Коњуви","Храм Свете Параскеве у Кашевару","Храм Свете Петке у Вишеселу","Храм Светих Јоакима и Ане у Бацу","Храм Светих апостола Петра и Павла у Калудри","Храм Свете Тројице у Вичи","Храм Свете великомученице Марине у Вичи","Храм Светог цара Константина и царице Јелене у Плочнику"]},{"label":"Куршумлија","url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/kursumlijske-parhohije","count":3,"temple_url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/6411-kuršumlijske-parohije-hramovi","temples":["Саборни храм Свете Тројице у Куршумлији","Храм Свете Петке у Мачковцу","Храм Светог архангела Михаила у Богујевцу","Храм Светог Николаја у Космачу","Храм Светог мученика Мине у Штави","Храм Светих апостола Петра и Павла у Лукову","Храм Светог великомученика Георгија у Луковској Бањи","Храм Свете Тројице у Требињу","Храм-брвнара Светог кнеза Лазара у Пролому","Храм Преображења Господњег у Пролом Бањи","Храм Свете Марије Магдалине у Игришту","Капела Светог архангела Гаврила и капела Свете Тројице у Рудару","Храм Пресвете Богородице у Бабици","Храм Светих врачева Козме и Дамјана у Микуљану","Храм Светог апостола и јеванђелисте Луке у Сагоњеву","Храм Свете Петке у Жучу","Храм Покрова Пресвете Богородице у Мирници","Храм Светог Василија Острошког у Растелици","Храм Свете Тројице у Селишту","Храм Преображења Господњег у Магову","Храм Светог архиђакона Стефана у Влахињи","Храм Светог великомученика Георгија у Селови"]},{"label":"Рача","url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/racanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/kosanicko-namesnistvo/6415-račanska-parohija-hramovi","temples":["Саборни храм Светог пророка Илије у Рачи","Храм Свете Петке у Добром Долу","Храм Светог Николаја у Мердару","Храм Свете Тројице у Заграђу"]},{"label":"Бели Поток","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/belopotocka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6423-belopotočka-parohija-hramovi","temples":["Храм Светог великомученика Георгија у Белом Потоку","Капела Источни Петак у Жабљану"]},{"label":"Брестовац","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/brestovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6442-brestovačka-parohija-hramovi","temples":["Храм Успења Пресвете Богородице у Брестовцу","Храм Светог архангела Гаврила у Дукату","Храм Свете великомученице Недеље у Заплањској Топоници"]},{"label":"Бунуша","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/bunuska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6444-bunuška-parohija-hramovi","temples":["Храм Светог великомученика Георгија у Бунуши","Храм Светих врачева Козме и Дамјана у Вини","Храм Преображења Господњег у Игришту","Храм преподобног Симеона Столпника у Славујевцу"]},{"label":"Чукљеник","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/cukljenicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6433-čukljenička-parohija-hramovi","temples":["Храм Светог оца Николаја у Чукљенику","Храм Светог архангела Гаврила у Накривњу"]},{"label":"Доња Стопања","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/donjestopanjska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6446-donjestopanjska-parohija-hramovi","temples":["Храм Светог Николаја у Доњем Стопању","Храм Успења Пресвете Богородице у Доњем Стопању"]},{"label":"Градашница","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/gradasnicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6427-gradašnička-parohija-hramovi","temples":["Храм Светог архангела Гаврила у Градашници","Храм Светог Николаја у Јарсенову","Храм Свете преподобне Параскеве у Ступници"]},{"label":"Лесковац, Храм Св. Симеона Мироточивог","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/hram-sv-simeona-mirotocivog-parohije","count":5,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6435-leskovac-hram-svetog-simeona-hramovi","temples":["Храм Светог Симеона Мироточивог у Лесковцу","Храм Светог пророка Илије у Лесковцу"]},{"label":"Јашуња и Бабичко","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/jasunjsko-babicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6429-jašunjsko-babička-parohija-hramovi","temples":["Храм Рођења Светог Јована Крститеља у Јашуњи","Храм Светих апостола Петра и Павла у Доњој Локошници","Храм Силаска Светог Духа на апостоле у Бабичком"]},{"label":"Кумарево","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/kumarevske-parohije","count":4,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6419-kumarevske-parohije-hramovi","temples":["Храм Свете преподобне мајке Параскеве у Кумареву","Храм Свете великомученице Недеље у Јелашници"]},{"label":"Кутлеш","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/kutleska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6448-kutleška-parohija-hramovi","temples":["Храм Свете преподобне Параскеве у Култешу"]},{"label":"Ораовица","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/oraovicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6431-oraovička-parohija-hramovi","temples":["Храм Светог оца Николаја у Ораовици"]},{"label":"Печењевац","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/pecenjevacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6450-pečenjevačka-parohija-hramovi","temples":["Храм Светог пророка Илије у Печењевцу"]},{"label":"Пуковац","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/pukovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6452-pukovačka-parohija-hramovi","temples":["Храм Светог Николаја у Пуковцу"]},{"label":"Рударе","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/rudarske-parohje","count":2,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6421-rudarske-parohije-hramovi","temples":["Храм Свете великомученице Параскеве у Рудару","Храм Светих врачева Козме и Дамјана у Шишинцу"]},{"label":"Лесковац, Саборни храм Свете Тројице","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/saborni-hram-parohije","count":6,"temple_url":null,"temples":[]},{"label":"Турековац","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/turekovacke-parohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6437-turekovačke-parohije-hramovi","temples":["Храм Сабора светих Апостола у Турековцу"]},{"label":"Вучје","url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/vucjanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/leskovacko-namesnistvo/6425-vučjanska-parohija-hramovi","temples":["Храм Рођења светог Јована Крститеља у Вучју","Капела Свете великомученице Марине у Брзи","Капела Светог Пантелејмона у Горини"]},{"label":"Димитровград","url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/dimitrovgradska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/dimitrovgradska-parohija/6385-dimitrovgradska-hramovi","temples":["Храм Рођења Пресвете Богородице у Димитровграду","Храм Cветог мученика Мине у Димитровграду","Храм Свете Тројице у Димитровграду","Храм Свете Петке у Димитровграду","Храм Светог великомученика Георгија у Жељуши","Храм Вазнесења Господњег у Жељуши","Храм Светог архангела Михаила у Бољевом Долу","Храм Светог Пантелејмона у Сенокосу","Храм Светог Димитрија у Бребевници","Храм Свете Тројице у Гуленовцима","Храм Светог Јована у Височким Одоровцима","Храм Светог великомученика Георгија у Мазгошу","Храм светог Јована Богослова у Мојинцима","Храм Свете Тројице у Петерлашу","Храм Светог Јована Крститеља у Петерлашу","Храм Ваведења Пресвете Богородице у Радејни","Храм Светог великомученика Георгија у Радејни","Храм Светог Великомученика Георгија у Протопопинцима","Храм Вазнесења Господњег у Смиловцима","Храм Свете Петке у Смиловцима","Храм Вазнесења Господњег у Градињу","Храм Свете Тројице у Борову","Храм Успења Пресвете Богородице у Борову","Храм Светог пророка Илије у Доњој Невљи","Храм Пресвете Богородице у Горњој Невљи","Храм Свете Тројице у Лукавици","Храм Светог пророка Илије у Срећковцима","Храм Свете Марије Магдалине у Чиниглавцима","Храм Светог архангела Михаила у Чиниглавцима"]},{"label":"Извор","url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/izvorska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/6458-izvorska-parohija-hramovi","temples":["Храм Свете Тројице у Извору","Храм Свете Петке у Градишници","Храм Светог архангела Михаила у Пољској Ржани"]},{"label":"Крупац","url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/krupacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/6460-krupačka-parohija-hramovi","temples":["Храм Преноса моштију Светог Николаја Мирликијског у Крупцу","Храм Светог Саве у Великом Јовановцу","Храм Успења Пресвете Богородице у Великом Селу"]},{"label":"Пирот, Саборна црква, ''Тијабарска''","url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/pirot-saborna-crkva","count":6,"temple_url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/6456-saborna-crkva-tijabarska-pirot-hramovi","temples":["Саборни храм Успења Пресвете Богородице у Пироту","Храм Светог Николаја Мирликијског у Белој","Храм Светог Јована Крститеља у Гостуши"]},{"label":"Пирот, Стара црква „Пазарска“","url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/pirot-stara-crkva-pazarska","count":5,"temple_url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/6454-stara-crkva-pazarska-pirot-hramovi","temples":["Храм Рођења Христовог у Пироту","Храм Светог великомученика Харалампија у Костуру","Храм Светих лекара Козме и Дамјана у Расници","Храм Светог Игнатија Богоносца у Великом Суводолу","Храм Свете Петке у Малом Суводолу","Храм Свете Тројице у Гњилану","Храм Светог великомученика Георгија у Присјану","Храм Светих апостола Петра и Павла у Бојнеговцу"]},{"label":"Темска","url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/temacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/pirotsko-namesnistvo/6463-temačka-parohija-hramovi","temples":["Храм Свете Петке у Темској","Храм Светог пророка Илије у Сопоту","Храм Светог Николаја - Свете Петке у Станичењу","Храм Светог Јована Крститеља у Станичењу","Храм Светих Кирика и Јулите у Станињцу","Храм Свете Петке у Јаловик Извору","Храм Светог великомученика Пантелејмона у Кални","Храм Светих апостола Петра и Павла у Ћуштици","Храм Светог Илије у Црном Врху","Храм Свете Тројице у Рудињу","Храм Свете Тројице у Топлом Долу","Храм Свете Тројице у Засковцима","Храм Свих светих у Балти Бериловцу","Храм Свете Тројице у Куманову","Храм Светог пророка Илије у Црвенчеву","Храм Свете Петке у Церови","Храм свете Петке у Орљи","Храм Светог великомученика Георгија у Вртовцима"]},{"label":"Белотинац","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/belotinacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6227-белотиначка-парохија-храмови","temples":["Храм светог Романа Ђунишког у Белотинцу","Храм преподобне Параскеве у Горњем Међурову"]},{"label":"Брзи Брод","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/brzobrodska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/brzobrodska-parohija/6272-brzobrodska-parohija-hramovi","temples":["Храм света Три Јерарха у Брзом броду"]},{"label":"Чокот","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/cokotska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6235-чокотска-парохија-храмови","temples":["Храм светог пророка Илије у Чокоту"]},{"label":"Ћурлина","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/curlinska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6234-ћурлинска-парохија-храмови","temples":["Храм свете преподобномученице Параскеве у Ћурлини"]},{"label":"Доње Међурово","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/donjemedjurovska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/donjemedjurovska-parohija/4119-доњемеђуровска-парохија","temples":["Храм Успења Пресвете Богородице у Доњем Међурову"]},{"label":"Габровац","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/gabrovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/gabrovacka-parohija/4120-габровачка-парохија","temples":["Храм Свете Тројице у Габровцу","Храм светог пророка Илије у Вукманову","Храм светог великомученика Димитрија у Бербатову","Храм светог Лазара Четвородневног у Доњем Власу"]},{"label":"Јелашница","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/jelasnicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/jelasnicka-parohija/6276-jelašnička-parohija-hramovi","temples":["Храм светих апостола Петра и Павла у Јелашници","Храм светог Николаја Мириликијског у селу Доња Студена","Храм Свете Тројице у Горњој Студени","Храм светог Николаја Мириликијског у селу Манастир"]},{"label":"Кочане","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/kocanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6230-кочанска-парохија-храмови","temples":["Храм светог Архангела Гаврила у Кочану"]},{"label":"Насеље Никола Тесла","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/naselje-nikola-tesla-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/naselje-nikola-tesla-parohija/6278-parohija-nikola-tesla-hramovi","temples":["Храм Светих врачева Козме и Дамјана у насељу ''Никола Тесла''","Храм Светог Архангела Гаврила у Првој Кутини"]},{"label":"Ниш, Храм Светог Цара Константина и Царице Јелене","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-sv-cara-konstantina-i-carice-jelene","count":7,"temple_url":null,"temples":[]},{"label":"Ниш, Храм Светог Василија Острошког","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-sv-cilija-ostroskog","count":3,"temple_url":null,"temples":[]},{"label":"Ниш, Храм Светог Оца Николаја","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-sv-oca-nikolaja","count":4,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6225-ниш-храм-светог-оца-николаја-храмови","temples":["Храм преноса моштију светог оца Николаја"]},{"label":"Ниш, Храм Свете Петке","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-svete-petke","count":4,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6224-ni%C5%A1-svete-petke-hramovi","temples":["Храм Свете Петке у Нишу","Храм светог краља Стефана Дечанског у комплексу нишког Казнено- поправног завода"]},{"label":"Ниш, Храм Светог Луке","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-svetog-luke","count":4,"temple_url":null,"temples":[]},{"label":"Ниш, Храм Васкрсења Христовог","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-vaskrsenja-hristovog","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6226-ниш-храм-васкрсења-храмови","temples":["Храм Васкрсења Христовог у Нишу"]},{"label":"Ниш, Храм Воздвижења Часног Крста","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-hram-vozdvizenja-svetog-krsta","count":3,"temple_url":null,"temples":[]},{"label":"Ниш, Саборни храм Силаска Светога Духа","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-saborni-hram","count":5,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/nis-saborni-hram/6223-ni%C5%A1-saborni-hram-hramovi","temples":["Саборни храм Силаска Светог Духа на Апостоле у Нишу"]},{"label":"Нишка Бања","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/niskobanjske-parohije","count":2,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/niskobanjske-parohije/6270-niškobanjske-hramovi","temples":["Храм светог пророка Илије у Нишкој Бањи"]},{"label":"Новоселска парохија","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/novoselska-parohija","count":1,"temple_url":null,"temples":[]},{"label":"Орљане","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/orljanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6232-орљанска-парохија-храмови","temples":["Храм свете преподобне Параскеве у Орљану","Храм Рођења светог Јована Крститеља у Орљану"]},{"label":"Паси Пољана","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/pasipoljanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/6233-пасипољанска-парохија-храмови","temples":["Храм свете великомученице Недеље у Пасипољани"]},{"label":"Заплање","url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/zaplanjska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/prvo-nisko-namesnistvo/zaplanjska-parohija/6274-zaplanjska-parohija-hramovi","temples":["Храм светог великомученика Георгија у Горњем Барбешу","Храм Успења Пресвете Богородице у Гркињи","Храм свете Петке у Мариној Кутини","Храм Вазнесења Господњег у Великом Крчимиру","Храм светог Николаја у Доњем Драговљу"]},{"label":"Азбресница","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/azbresnicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6470-azbresnička-parohija-hramovi","temples":["Храм Светог великомученика Теодора Тирона у Азбресници","Храм Светог великомученика Пантелејмона у Азбресници","Храм Успења Пресвете Богородице у Крајковцу","Храм Светог Јована Крститеља у Крајковцу","Храм Свете Петке у Сечаници","Храм Светог Романа Ђунишког у Сечаници","Храм Светих апостола Петра и Павла у Дудулајцу","Храм Свете Тројице у Лалинским Појатама"]},{"label":"Балајинац","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/baljinacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6472-balajinačka-parohija-hramovi","temples":["Храм Успења Пресвете Богородице у Балајинцу","Храм Свете великомученице Недеље у Батушинцу"]},{"label":"Балиновац","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/blinovacka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6474-balinovačka-parohija-hramovi","temples":["Храм Светог пророка Илије у Балиновцу","Храм Светог архангела Михаила у Џигољу","Храм Светог архангела Гаврила у Дешилову","Храм Свете Петке у Девчи","Храм Светих лекара Козме и Дамјана у Горњем Кординцу","Храм Свете великомученице Марине у Клисурици"]},{"label":"Конџељ","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/kondzeljskа-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6480-kondželjska-parohija-hramovi","temples":["Храм Светих архангела Михаила и Гаврила у Конџељу","Храм Светих Бесребреника Козме и Дамјана у Малој Плани","Храм Светих апостола Петра и Павла у Гојиновцу"]},{"label":"Мерошина","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/merosinska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6483-merošinska-parohija-hramovi","temples":["Храм Светог Николаја у Биљегу","Храм Светог Георгија у Рожини","Храм Свете Петке у Бресту"]},{"label":"Прокупље","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/prokupacke-parohije","count":6,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6466-prokupačke-parohije-hramovi","temples":["Храм Светог великомученика Прокопија у Прокупљу","Храм Светих лекара Козме и Дамјана у комплексу Прокупачке болнице","Храм Свете Петке у Губетину","Храм Светог Василија Острошког у Влахову","Храм Светог великомученика Пантелејмона у Селишту","Храм Светог апостола и јеванђелиста Марка у Водицaма","Храм Преподобне Параскеве у Доњој Трнави"]},{"label":"Велика Плана","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/velikoplanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6476-velikoplanska-parohija-hramovi","temples":["Храм Светог Јована Крститеља у Меровцу","Храм Свете Петке у Прекопуцу","Храм Рођења Пресвете Богородице у Доњoj РечициХрам Рођења Пресвете Богородице у Доњој Речици","Храм светих Апостола Петра и Павла у селу БулатовацХрам Светих апостола Петра и Павла у Булатовцу","Храм свете великомученице Марине у селу ЈуговацХрам Свете великомученице Марине у Југовцу"]},{"label":"Житорађa","url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/zitoradjske-parohije","count":3,"temple_url":"https://eparhijaniska.rs/parohije/toplicko-namesnistvo/6468-žitorađske-parohije-hramovi","temples":["Храм Светих апостола Петра и Павла у Житорађи","Храм Успења Пресвете Богородице у Житорађи","Храм Светог првомученика и архиђакона Стефана у Глашинцу","Храм Светог пророка Илије у Јасеници","Храм Светог Симеона Мироточивог у Доњем Црнатову","Храм Преподобне Параскеве у Доњој Рсовачи","Храм Светог пророка Илије у Дубову","Храм Светог Николаја у Речици"]},{"label":"Грделица","url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/grdelicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/6378-grdelička-parohija-hramovi","temples":["Храм Рођења Светог Јована Крститеља у Грделици"]},{"label":"Конопница","url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/konopnicka-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/6380-konopnička-parohija-hramovi","temples":["Храм Успења Пресвете Богородице у Конопници"]},{"label":"Предејане","url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/predejanska-parohija","count":1,"temple_url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/6382-predejanska-parohija-hramovi","temples":["Храм Светог архистратига Гаврила у Предејану","Храм Светог архистратига Гаврила у Рупљу"]},{"label":"Власотинце","url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/vlasotinacke-parohije","count":4,"temple_url":"https://eparhijaniska.rs/parohije/vlasotinacko-namesnistvo/6376-vlasotinačke-parohije-hramovi","temples":["Храм Силаска Светог Духа на Апостоле у Власотинцу","Храм Светог архангела Гаврила у Крушевици","Храм Светих цара Константина и царице Јелене у Црвеној Јабуци","Храм Светих апостола Петра и Павла у Раковом Долу","Храм Светог великомученика Димитрија у Добровишу","Храм Светог Николаја у Великом Боњинцу","Храм Обновљења храма светог Великомученика Георгија у Завидинцима","Храм Светог Николаја у Козару"]}],"monasteries":[{"local":"Манастир Ајдановац","url":"https://eparhijaniska.rs/manastiri/manastir-ajdanovac"},{"local":"Манастир Црковница","url":"https://eparhijaniska.rs/manastiri/manastir-crkovnica"},{"local":"Манастир Дивљана","url":"https://eparhijaniska.rs/manastiri/manastir-divljana"},{"local":"Манастир Ђунис","url":"https://eparhijaniska.rs/manastiri/manastir-djunis"},{"local":"Манастир Габровац","url":"https://eparhijaniska.rs/manastiri/manastir-gabrovac"},{"local":"Манастир Горњи Матејевац","url":"https://eparhijaniska.rs/manastiri/manastir-gornji-matejevac"},{"local":"Манастир Иверица","url":"https://eparhijaniska.rs/manastiri/manastir-iverica"},{"local":"Манастир Изатовац","url":"https://eparhijaniska.rs/manastiri/manastir-izatovac"},{"local":"Манастир Јашуња - Пр. Богородице","url":"https://eparhijaniska.rs/manastiri/manastir-jasunja-pr-bogorodice"},{"local":"Манастир Јашуња - Св.Јован Крститељ","url":"https://eparhijaniska.rs/manastiri/manastir-jasunja-sv-jovan-krstitelj"},{"local":"Манастир Каменица","url":"https://eparhijaniska.rs/manastiri/manastir-kamenica"},{"local":"Манастир Крупац","url":"https://eparhijaniska.rs/manastiri/manastir-krupac"},{"local":"Манастир Липовац","url":"https://eparhijaniska.rs/manastiri/manastir-lipovac"},{"local":"Манастир Св. Димитрија - Манастирче","url":"https://eparhijaniska.rs/manastiri/manastir-manastirce"},{"local":"Манастир Пирковац","url":"https://eparhijaniska.rs/manastiri/manastir-pirkovac"},{"local":"Манастир Планиница","url":"https://eparhijaniska.rs/manastiri/manastir-planinica"},{"local":"Манастир Плочник","url":"https://eparhijaniska.rs/manastiri/manastir-plocnik"},{"local":"Манастир Поганово","url":"https://eparhijaniska.rs/manastiri/manastir-poganovo"},{"local":"Манастир Рсовци","url":"https://eparhijaniska.rs/manastiri/manastir-rsovci"},{"local":"Манастир Сићево","url":"https://eparhijaniska.rs/manastiri/manastir-sicevo"},{"local":"Манастир Сињац","url":"https://eparhijaniska.rs/manastiri/manastir-sinjac"},{"local":"Манастир Смиловци","url":"https://eparhijaniska.rs/manastiri/manastir-smilovci"},{"local":"Манастир Суково","url":"https://eparhijaniska.rs/manastiri/manastir-sukovo"},{"local":"Манастир Св. Николе - Куршумлија","url":"https://eparhijaniska.rs/manastiri/manastir-sv-nikole-kursumlija"},{"local":"Манастир Св. Онуфрија","url":"https://eparhijaniska.rs/manastiri/manastir-sv-onufrija"},{"local":"Манастир Св. Роман","url":"https://eparhijaniska.rs/manastiri/manastir-sv-roman"},{"local":"Манастир Темска","url":"https://eparhijaniska.rs/manastiri/manastir-temska"},{"local":"Манастир Вета","url":"https://eparhijaniska.rs/manastiri/manastir-veta"},{"local":"Манастир Височка Ржана","url":"https://eparhijaniska.rs/manastiri/manastir-visocka-rzana"},{"local":"Манастир Завидинце","url":"https://eparhijaniska.rs/manastiri/manastir-zavidince"}]}''')
ZICA_MONASTERIES = "https://eparhija-zicka.rs/manastiri/"
ZICA_DATA = json.loads(r'''{"deaneries":[{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-gruzansko-2/","label":"ГРУЖАНСКО (БОРАЧ)","parish_count":8,"community_count":8,"communities":[{"local":"Црквена општина Борач","temples":["Храм Светог Архангела Гаврила"]},{"local":"Црквена општина Гунцати","temples":["Храм Успења Пресвете Богородице","Храм Светог великомученика Пантелејмона (Бумбарево Брдо)"]},{"local":"Црквена општина Гривац","temples":["Храм Рођења Пресвете Богородице"]},{"local":"Црквена општина Закута","temples":["Храм Преподобне Ангелине Српске","Храм Светих апостола Петра и Павла - Витковац","Храм Свете Тројице - Печеног"]},{"local":"Црквена општина Кнић","temples":["Храм Светог пророка Илије"]},{"local":"Црквена општина Пајсијевићи","temples":["Храм Покрова Пресвете Богородице"]},{"local":"Црквена општина Рамаћа","temples":["Храм Светог Николаја Мирликијског","Храм Вазнесења Господњег - Каменица"]},{"local":"Црквена општина Честин","temples":["Храм Рођења Пресвете Богородице, при Манастиру Каменцу"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-dragacevsko-2/","label":"ДРАГАЧЕВСКО (ГУЧА)","parish_count":9,"community_count":7,"communities":[{"local":"Црквена општина Вича","temples":["Храм Светог пророка Илије - Вича","Храм Светог архангела Гаврила"]},{"local":"Црквена општина Гуча","temples":["Храм Светог архангела Гаврила"]},{"local":"Црквена општина Горачићи","temples":["Храм Рођења Пресвете Богородице"]},{"local":"Црквена општина Каона","temples":["Храм Усековања главе Светог Јована Крститеља"]},{"local":"Црквена општина Котража","temples":["Храм Светог Великомученика Георгија"]},{"local":"Црквена општина Лучани","temples":["Храм Спаљивања моштију Светог Саве Српског","Храм Светог архангела Михаила - Јелен До"]},{"local":"Црквена општина Тијање","temples":["Храм Светог великомученика Прокопија"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-zicko-2/","label":"ЖИЧКО (КРАЉЕВО)","parish_count":37,"community_count":16,"communities":[{"local":"Црквена општина при Храму Свете Тројице","temples":["Храм Свете Тројице"]},{"local":"Црквена општина при Храму Светог Саве Српског","temples":["Храм Светог Саве Српског"]},{"local":"Црквена општина при Храму Светог Василија Острошког","temples":["Храм Светог Василија Острошког"]},{"local":"Парохија при манастиру Жичи","temples":["Храм Светог четвородневног Лазара"]},{"local":"Црквена општина Ратина","temples":["Храм Рођења Светог Јована Крститеља"]},{"local":"Црквена општина Врба","temples":["Храм Вазнесења Господњег"]},{"local":"Црквена општина Врњачка Бања","temples":["Храм Рођења Пресвете Богородице","Храм Живоносног Источника Пресвете Богородице"]},{"local":"Црквена општина Вукушица","temples":["Храм Светог Јована Крститеља - Вукушица","Храм Светог Саве Српског - Вранеши"]},{"local":"Црквена општина Самаила","temples":["Храм Светог великомученика Пантелејмона - Самаила","Храм Светих апостола Петра и Павла - Мрсаћ"]},{"local":"Црквена општина Врдила","temples":["Храм Богојављења Господњег"]},{"local":"Црквена општина Матарушка Бања","temples":["Храм Светог великомученика кнеза Лазара","Храм Пресвете Богородице Тројеручице - Конарево","Храм Светих апостола Петра и Павла - Богутовачка Бања"]},{"local":"Црквена општина Конарево","temples":["Храм Пресвете Богородице Тројеручице"]},{"local":"Црквена општина Чукојевац","temples":["Храм Покрова Пресвете Богородице"]},{"local":"Црквена општина Цветке","temples":["Храм Светог Апостола Павла"]},{"local":"Црквена општина Грачац","temples":["Храм Светог Саве"]},{"local":"Црквена општина Годачица","temples":["Храм Успења Пресвете Богородице"]},{"local":"Црквена општина Сирча","temples":["Храм Светог пророка Илије"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-kacersko-2/","label":"КАЧЕРСКО (ЉИГ)","parish_count":6,"community_count":6,"communities":[{"local":"Црквена општина Бeлановица","temples":["Храм Покрова Пресвете Богородице"]},{"local":"Црквена општина Бољковци","temples":["Храм Светог Николаја Мирликијског","храм Сабора Светих апостола - Штавица"]},{"local":"Црквена општина Заграђе","temples":["Храм Светог архангела Гаврила"]},{"local":"Црквена општина Јарменовци","temples":["Храм Покрова Пресвете Богородице","Храм Светог Саве Српског","Храм Св. великомученика Георгија - Рудник"]},{"local":"Црквена општина Љиг","temples":["Храм Рођења Светог Јована Крститеља - Љиг","Храм Светог Николаја Мирликијског - Ивановци","Храм Св. Јована Крститеља - Дићи"]},{"local":"Црквена општина Моравци","temples":["Храм Светог архангела Гаврила, Манастир Моравци"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-ljubicko-2/","label":"ЉУБИЋКО (ПРЕЉИНА)","parish_count":11,"community_count":10,"communities":[{"local":"Црквена општина брђанско-прислоничка","temples":["Храм Светог великомученика Пантелејмона"]},{"local":"Црквена општина Бресница","temples":["Храм Покрова Пресвете Богородице","Храм Светог апостола и јеванђелисте Марка"]},{"local":"Црквена општина Горња Горевница","temples":["Храм Светог великомученика Георгија","Храм Преподобне Параскеве у Горњој Горевници","Храм Живоносног Источника у Милићевцима","Храм Светог великомученика Георгија у Вранићима"]},{"local":"Црквена општина Катрга","temples":["Храм Светог архангела Гаврила"]},{"local":"Црквена општина Коњевићи","temples":["Храм Светог цара Константина и царице Јелене"]},{"local":"Црквена општина Миоковци","temples":["Храм Покрова Пресвете Богородице"]},{"local":"Црквена општина Мојсиње","temples":["Храм Успења Пресвете Богородице"]},{"local":"Црквена општина Мрчајевци","temples":["Храм Светих апостола Петра и Павла"]},{"local":"Црквена општина Прељина","temples":["Храм Светог Јоакима и Ане","Храм Светог Василија Острошког - Прељина","Храм Сретења Господњег - Соколићи","Храм Светог пророка Илије - Доња Трепча"]},{"local":"Црквена општина Рожачко-пријеворска","temples":["Храм Светог великомученика Георгија"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-moravicko-2/","label":"МОРАВИЧКО (ИВАЊИЦА)","parish_count":14,"community_count":7,"communities":[{"local":"Црквена општина Ивањица","temples":["Храм Светог архангела Гаврила у Црњеву","Храм Преноса моштију Светог Николаја Мирликијског у Косовици","Храм Светог великомученика кнеза Лазара у Бединој Вароши","Храм Светог великомученика Георгија у Глијечи","Храм Светог архангела Гаврила у Рашчићима","Храм Светих апостола Петра и Павла у Буткову","Храм Светог Илије у Куманици","Храм Светих бесребреника Козме и Дамјана у Будожељи","Храм Светог великомученика Прокопија у Комадинама","Храм Свете Тројице у Међуречју","Храм Светог деспота Стефана Лазаревића у Буковици (у изградњи)","Храм Светог цара Константина и царице Јелене"]},{"local":"Црквена општина Брезова/Катићи","temples":["Храм Светог Николаја Мирликијског - Брезова","Храм Преподобне мати Параскеве - Мочиоци"]},{"local":"Црквена општина Луке","temples":["Храм Покрова Пресвете Богородице - Луке","Храм Светог архангела Гаврила - Осоница","Храм Светих апостола Петра и Павла - Лиса"]},{"local":"Црквена општина Миланџа","temples":["Храм Светог Саве Српског - Миланџа","Храм Успења Пресвете Богородице - Кушићи","Храм Преображења Господњег - Братљево"]},{"local":"Црквена општина Девићи","temples":["Храм Светог апостола и јеванђелисте Луке - Девићи","Храм Светих Козме и Дамјана - Остатија","Храм Усековања главе Светог Јована Крститеља - Коритник","Храм Успења Свете Ане - Брусник","Храм Светих 40 мученика Севастијских - Старо Село","Храм Светог пророка Илије - Одвраћеница"]},{"local":"Црквена општина Прилике","temples":["Храм Светог архангела Михаила - Прилике","Храм Вазнесења Господњег - Дубрава"]},{"local":"Црквена општина Радаљево","temples":["Храм Светог великомученика Георгија - Радаљево","Храм Светог великомученика Георгија - Доње Радаљево"]},{"local":"Парохија при манастиру Придворица","temples":["Храм Преображења Господњег - ман. Придворица","Храм Свете муч. Марине - Головша","Храм Светих врача Козме и Дамјана - Вељовићи"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-pozesko-ariljsko-2/","label":"ПОЖЕШКО-АРИЉСКО (АРИЉЕ)","parish_count":18,"community_count":10,"communities":[{"local":"Црквена општина Пожега","temples":["Храм Светог цара Конастантина и царице Јелене","храм Света Три Јерарха са параклисима Светог кнеза Лазара и Свете Петке","храм Светог апостола Луке","храм Вазнесења Господњег - Расна","храм Светог Саве - Савинац Висибаба"]},{"local":"Црквена општина Ариље","temples":["Храм Светог Ахилија, задужбина Светог Теоктиста Монаха (краља Драгутина)"]},{"local":"Црквена општина Бреково","temples":["Храм Светог Николе - Бреково","Храм Свете Тројице - Бјелуша"]},{"local":"Црквена општина Годовик","temples":["Храм Обновљења храма Светог великомученика Георгија, храм Светог пророка Илије"]},{"local":"Црквена општина Горобиље","temples":["Храм Рођења Светог Јована Крститеља"]},{"local":"Црквена општина Горња Добриња","temples":["Храм Светих Апостола Петра и Павла"]},{"local":"Црквена општина Трешњевица","temples":["Храм Светог Николаја Жичког - Трешњевица"]},{"local":"Црквена општина Драгојевац","temples":["Храм Вазнесења Господњег"]},{"local":"Црквена општина Засеље","temples":["Храм Сабора Светог Јована Крститеља, храм Сабора Српских Светитеља - Миљаковина"]},{"local":"Црквена општина Прилипац","temples":["Храм Рођења Пресвете Богородице"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-racansko-2/","label":"РАЧАНСКО (БАЈИНА БАШТА)","parish_count":11,"community_count":5,"communities":[{"local":"Црквена општина Бајина Башта","temples":["Храм Светог пророка Илије - Бајина Башта","Храм Пресвете Богородице - Живоносног Источника - Солотуша","Храм Покрова Пресвете Богородице - Растиште","Храм Светог великомученика Пантелејмона - Доња Црвица"]},{"local":"Црквена општина Рогачица","temples":["Храм Вазнесења Господњег - Рогачица","Храм Светог великомученика Димитрија - Оклетац","Храм Светог Николаја Мирликијског - Гвоздац","Храм Свете Тројице - Зарожје","Храм Светих апостола Петра и Павла - Пашина Раван"]},{"local":"Црквена општина Дуб","temples":["Храм Вазнесења Господњег","Храм Светих ап. Петра и Павла"]},{"local":"Црквена општина Мокра Гора","temples":["Храм Светог пророка Илије","Храм Светог Јована Крститеља - Мокра Гора","Храм Вазнесења Господњег - Кршање","Храм Свете Тројице и Св. цара Лазара - Заовине","Храм Преноса моштију Светог Саве Српског - Мећавник"]},{"local":"Црквена општина Кремна","temples":["Храм Светог великомученика Георгија - Кремна","Храм Светог цара Константина и царице Јелене - Шарган"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-studenicko-2/","label":"СТУДЕНИЧКО (РАШКА)","parish_count":10,"community_count":9,"communities":[{"local":"Црквена општина Рашка","temples":["Храм Светог архангела Гаврила - Рашка","Храм Рођења Пресвете Богородице - Власово","Храм Свете Тројице - Варево"]},{"local":"Црквена општина Рудница","temples":["Храм Преподобне мати Параскеве - Рудница","Храм Светог апостола и јеванђелисте Марка - Бељак"]},{"local":"Црквена општина Баљевац","temples":["Храм Усековања главе Светог Јована Крститеља - Баљевац","Храм Светог Николаја Мирликијског - Беоце","Храм Светог Николаја Мирликијског - Шумник"]},{"local":"Црквена општина Савово","temples":["Храм Успења Пресвете Богородице, при Манастиру Студеници","Храм Покрова Пресвете Богородице - Савово","Храм Светог великомученика Георгија - Врх","Храм Светог Николаја Мирликијског - Палеж"]},{"local":"Црквена општина Градац","temples":["Храм Благовести Пресвете Богородице, при Манастиру Градац","Храм Светог пророка Илије - Рудно","Храм Светих апостола Петра и Павла - Ржана"]},{"local":"Црквена општина Јошаничка Бања","temples":["Храм Успења Пресвете Богородице"]},{"local":"Црквена општина Трнава","temples":["Храм Успења Пресвете Богородице","Храм Преподобне Параскеве","Храм Светог архиђакона Стефана","Храм Светог пророка Илије - Боровић","Храм Свете Марије Магдалине - Плешин","Храм Свете великомученице Марине - Бело Поље"]},{"local":"Црквена општина Павлица","temples":["Храм Ваведења Пресвете Богородице, при Манастиру Павлица","Храм Светог апостола и јеванђелисте Марка - Поцесје"]},{"local":"Црквена општина Ушће","temples":["Храм Светог Николаја Мирликијског"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-takovsko-2/","label":"ТАКОВСКО (ГОРЊИ МИЛАНОВАЦ)","parish_count":14,"community_count":10,"communities":[{"local":"Црквена општина Горњи Милановац","temples":["Храм Свете Тројице - Горњи Милановац","Храм Успенија Пресвете Богородице - Јабланица","Храм Светог Методија Патарског - Велереч"]},{"local":"Црквена општина Брусница","temples":["Храм Преноса моштију Светог Николаја Мирликијског - Брусница"]},{"local":"Црквена општина Брезна","temples":["Храм Светог великомученика Димитрија - Брезна","Храм Преподобне Параскеве - Коштунићи","Храм Покрова Пресвете Богородице - Горњи Бањани"]},{"local":"Црквена општина Доња Црнућа","temples":["Храм Светог великомученика Георгија, при Манастиру Враћевшници","Храм Светог архангела Гаврила - Доња Врбава"]},{"local":"Црквена општина Каменица","temples":["Храм Светог пророка Илије - Каменица","Храм Силаска Светог Духа на Апостоле - Душковци"]},{"local":"Црквена општина Љутовница","temples":["Храм Преноса моштију Светог Николаја Мирликијског","Храм Светог Николаја Мирликијског - Шилопај"]},{"local":"Црквена општина Мајдан","temples":["Храм Свете Тројице"]},{"local":"Црквена општина Прањани","temples":["Храм Вазнесења Господњег"]},{"local":"Црквена општина Савинац","temples":["Храм Светог Саве Српског","Храм Рођења Светог Јована Крститеља - Озрем, Црква брвнара у Такову (18 в.)"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-trnavsko-2/","label":"ТРНАВСКО (ЧАЧАК)","parish_count":25,"community_count":8,"communities":[{"local":"Црквена општина при Храму Вазнесења Господњег (XII в.)","temples":["Храм Вазнесења Господњег (XII в.)"]},{"local":"Црквена општина при Храму Успења Пресвете Богородице","temples":["Храм Успења Пресвете Богородице"]},{"local":"Црквена општина при Храму Свете великомученице Марине","temples":["Храм Свете великомученице Марине"]},{"local":"Црквена општина при Храму Светог великомученика кнеза Лазара на Љубићу ул. Драгослава Бојића бб","temples":["Храм Светог великомученика кнеза Лазара на Љубићу ул. Драгослава Бојића бб"]},{"local":"Црквена општина Заблаће","temples":["Храм Светог архангела Гаврила (1874. г.)","Храм Свете Тројице у Мршинцима"]},{"local":"Црквена општина Горичани","temples":["Храм Светог цара Константина и царице Јелене - Горичани (1930)","Храм Светих апостола Петра и Павла - Жаочани","Храм Рођења Пресвете Богородице - Качуљице"]},{"local":"Црквена општина Лазац","temples":["Храм Светих апостола Петра и Павла (1965)"]},{"local":"Црквена општина Трнава","temples":["Храм Благовести Пресвете Богородице"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-uzicko-2/","label":"УЖИЧКО (УЖИЦЕ)","parish_count":33,"community_count":15,"communities":[{"local":"Црквена општина при Храму Светог великомученика Георгија","temples":["Храм Светог великомученика Георгија"]},{"local":"Црквена општина при Храму Светог апостола и јеванђелисте Марка","temples":["Храм Светог апостола и јеванђелисте Марка"]},{"local":"Црквена општина при Храму Покрова Пресвете Богородице","temples":["Храм Покрова Пресвете Богородице"]},{"local":"Црквена општина Дрежник","temples":["Храм Успења Пресвете Богородице"]},{"local":"Црквена општина Доброселица","temples":["Храм Светог пророка Илије - Доброселица","Храм Покрова Пресвете Богородице - Јабланица","Храм Свете Тројице - Драглица"]},{"local":"Црквена општина Златибор","temples":["Храм Преображења Господњег - Златибор","Храм Рођења Светог Јована Крститеља - Семегњево"]},{"local":"Црквена општина Каран","temples":["Храм Благовештења Господњег - Каран","Храм Светог Василија Острошког - Рибашевина","Храм Светог Николаја Жичког - Гостиница"]},{"local":"Црквена општина љубишко-белоречка","temples":["Храм Светог цара Константина и царице Јелене","Храм Преображења Господњег"]},{"local":"Црквена општина Мачкат","temples":["Храм Светог пророка Илије - Мачкат","Храм Свете Недеље - Трипкова"]},{"local":"Црквена општина Негбина","temples":["Храм Рођења Светог Јована Крститеља"]},{"local":"Црквена општина Биоска","temples":["Храм Светих апостола Петра и Павла - Биоска","Храм Преподобне Параскеве - Поникве"]},{"local":"Црквена општина Севојно","temples":["Храм Светог архангела Гаврила"]},{"local":"Црквена општина Сирогојно","temples":["Храм Светих апостола Петра и Павла - Сирогојно","Храм Светог Киријака Отшелника - Никојевићи","Храм Светог пророка Илије - Равањско Поље"]},{"local":"Црквена општина Чајетина","temples":["Храм Светог архангела Гаврила"]},{"local":"Црквена општина Шљивовица","temples":["Храм Рођења Пресвете Богородице","Храм Свете Марије Магдалине - Шљивовица"]}]},{"url":"https://eparhija-zicka.rs/arhijerejsko-namesnistvo-crnogorsko-2/","label":"ЦРНОГОРСКО (КОСЈЕРИЋ)","parish_count":6,"community_count":5,"communities":[{"local":"Црквена општина Косјерић","temples":["Храм Рођења Пресвете Богородице - Косјерић, храм светог архангела Гаврила - Радановци"]},{"local":"Црквена општина Сеча Река","temples":["Храм Светог великомученика Георгија"]},{"local":"Црквена општина Ражана","temples":["Храм Успења Пресвете Богородице"]},{"local":"Црквена општина Маковиште","temples":["Храм Свете Тројице"]},{"local":"Црквена општина Субјел","temples":["Храм Светог апостола и јеванђелисте Луке"]}]}],"summary":{"deaneries":13,"parishes":202,"declared_communities":116,"parsed_communities":117,"temples":221}}''')
SREM_CHURCHES = "https://eparhijasremska.rs/потражите-храм/"
SREM_DEANERIES = "https://eparhijasremska.rs/намесништва/"
SREM_MONASTERIES = "https://eparhijasremska.rs/манастири/"
SREM_DATA = json.loads(r'''{"deaneries":[{"local":"Архијерејско намесништво земунско","sites":[{"number":1,"local":"Храм Светог архангела Гаврила , Пуковника Миленка Павловића бр.2, Батајница"},{"number":2,"local":"Храм Рођења Пресвете Богородице , Бихаћка бр.1, Батајница"},{"number":3,"local":"Храм Светог Саве, 11. октобра бр.11, Бечмен"},{"number":4,"local":"Храм Преподобне мати Параскеве, Браће Кокар бр.3, Бољевци"},{"number":5,"local":"Храм Светих Ћирила и Методија, Епископа Саве Трлајића бр.2, Бусије - Угриновци"},{"number":6,"local":"Храм Преноса моштију Светог оца Николаја, Земунска бр.1, Добановци"},{"number":7,"local":"Храм Вазнесења Господњег, Проте Стаматовића бр.33, Јаково"},{"number":8,"local":"Храм Рођења Светог Јована Крститеља, Душана Вукасовића бр.5, Петровчић"},{"number":9,"local":"Храм Светог архангела Гаврила, Жртава фашизма бр.5, Прогар"},{"number":10,"local":"Храм Преподобне мати Параскеве, Војвођанска бр.81, Сурчин"},{"number":11,"local":"Храм Светог апостола Матеја, Београдска бр.30, Угриновци"},{"number":12,"local":"Храм Светог великомученика Георгија, Београдска бр.1, Угриновци"},{"number":13,"local":"Храм Светог Пророка Илије, 20. нова бр. 48, Добановци - Грмовац"}]},{"local":"Архијерејско намесништво пећиначко","sites":[{"number":14,"local":"Храм Светог архангела Гаврила, Каменова бр.6, Ашања"},{"number":15,"local":"Храм Светог архангела Гаврила, Лазе Кромпића бр.5, Брестач"},{"number":16,"local":"Храм Вазнесења Господњег, Ивана Петровића бр.12, Деч"},{"number":17,"local":"Храм Светих апостола Петра и Павла, Браће Шовљански бр.6, Доњи Товарник"},{"number":18,"local":"Храм Пренос моштију Светог оца Николаја, Горњанска бр.22, Карловчић"},{"number":19,"local":"Храм Свете Тројице, Бранка Маџаревића бр.45, Купиново"},{"number":20,"local":"Храм Светог апостола и јеванђелиста Луке, Бранка Маџаревића бр.142, Купиново"},{"number":21,"local":"Храм Преображења Господњег, Пролетерска бр.10, Обреж"},{"number":22,"local":"Храм Преноса моштију Светог оца Николаја, Партизанска бр.2, Огар"},{"number":23,"local":"Храм Преноса моштију Светог оца Николаја, Браће Видаковић бр.5, Пећинци"},{"number":24,"local":"Храм Сабора светог архангела Гаврила, ЈНА бр.2, Попинци"},{"number":25,"local":"Храм Преноса моштију Светог оца Николаја, Шимановачка бр.8, Прхово"},{"number":26,"local":"Храм Преноса моштију Светог оца Николаја, Сибач"},{"number":27,"local":"Храм Светог Јована Богослова, Шимановачка бр.1, Сремски Михаљевци"},{"number":28,"local":"Храм Рођења Светог Јована Крститеља, Партизанска бр.9, Суботиште"},{"number":29,"local":"Храм Преноса моштију Светог оца Николаја, Трг Светог Николаја бр.7, Шимановци"}]},{"local":"Архијерејско намесништво подунавско","sites":[{"number":30,"local":"Храм Светог великомученика Георгија, Цара Душана бр.2, Баноштор"},{"number":31,"local":"Храм Преображења Господњег, Стојана Вукосављевића бр.62, Беочин"},{"number":32,"local":"Храм Светог Василија Острошког, Светосавска бр.4б, Беочин"},{"number":33,"local":"Храм Вазнесења Господњег, Видовданска бр.6, Буковац"},{"number":34,"local":"Храм Чудо Светог Архангела Михаила, Нештин"},{"number":35,"local":"Храм Преноса моштију Светог оца Николаја, Ириг"},{"number":36,"local":"Храм Успења Пресвете Богородице, Ириг"},{"number":37,"local":"Храм Светог великомученика Теодора Тирона, Ириг"},{"number":38,"local":"Храм Преноса моштију Светог оца Николаја, Змај Јовина бр.6, Нови Лединци"},{"number":39,"local":"Храм Светих бесребреника и чудотвораца Козме и Дамјана, Црквеношколска бр.22, Нештин"},{"number":40,"local":"Храм Свете великомученице Марине - Огњене Марије, Славујева бб, Сремска Каменица"},{"number":41,"local":"Храм Светог апостола Павла, Владимира Назора бб, Петроварадин"},{"number":42,"local":"Храм Преподобне мати Параскеве, Рељковићева, Петроварадин"},{"number":43,"local":"Храм Светог исповедника Варнаве Беочинског, Петроварадин"},{"number":44,"local":"Храм Покрова Пресвете Богородице, Петроварадин"},{"number":45,"local":"Храм Ваведења Пресвете Богородице, Сусек"},{"number":46,"local":"Храм Рођења Пресвете Богородице, Трг Краља Петра Првог бб, Сремска Каменица"},{"number":47,"local":"Храм - капела Светог Нектарија Егинског, Институт КВБ, Сремска Каменица"},{"number":48,"local":"Храм Светог пророка Илије, Татарско брдо, Сремска Каменица"},{"number":49,"local":"Храм Светог архангела Гаврила, Николе Тесле бр.52, Сусек"},{"number":50,"local":"Храм Светог Саве, Миленка Шербана бр.12, Черевић"},{"number":51,"local":"Храм Светог великомученика Георгија, бр.Ириг, Ривица"}]},{"local":"Архијерејско намесништво румско","sites":[{"number":52,"local":"Храм Светих архангела Михаила и Гаврила, Маршала Тита бр.3, Буђановци"},{"number":53,"local":"Храм Рођења Пресвете Богородице, Гробљанска бб, Платичево"},{"number":54,"local":"Храм Преноса моштију Светог оца Николаја, Бакићева бр.7, Вогањ"},{"number":55,"local":"Храм Рођења Светог Јована Претече и Крститеља, Девете војвођанске бригаде бр.92, Врдник"},{"number":56,"local":"Храм Светог великомученика Георгија, Главна бр.42, Грабовци"},{"number":57,"local":"Храм Преноса моштију Светог оца Николаја, Маре Гмизић бр.5, Добринци"},{"number":58,"local":"Храм Преноса моштију Светог оца Николаја, Цара Уроша бр.40, Јазак"},{"number":59,"local":"Храм Преноса моштију Светог оца Николаја, Главна бр.13, Кленак"},{"number":60,"local":"Храм Преноса моштију Светог оца Николаја, Румска бр.2, Краљевци"},{"number":61,"local":"Храм Преноса моштију Светог оца Николаја, Кратка бр.1, Мали Радинци"},{"number":62,"local":"Храм Вазнесења Господњег, Војводе Мишића бр.64, Никинци"},{"number":63,"local":"Храм Светог архангела Гаврила, 29. октобра бр.4, Платичево"},{"number":64,"local":"Храм Преноса моштију Светог оца Николаја, Јазак, Павловци"},{"number":65,"local":"Храм Светог великомученика Георгија, Војводе Степе бр.2, Хртковци"},{"number":66,"local":"Храм Светог пророка Илије, Доситеја Обрадовића бр.1, Жарковац"},{"number":67,"local":"Храм Силаска Светог Духа на апостоле, Главна бр.159, Рума"},{"number":68,"local":"Храм Преноса моштију Светог оца Николаја, Иришка бр.37, Рума"},{"number":69,"local":"Храм Вазнесења Господњег, Станка Пауновића Вељка бр.190, Рума"},{"number":70,"local":"Храм Сабора Српских Светитеља, Тицанова бб, Рума"},{"number":71,"local":"Храм Пресвете Богородице Млекопитатљнице, Рума"}]},{"local":"Архијерејско намесништво сремскокарловачко","sites":[{"number":72,"local":"Храм Ваведења Пресвете Богородице, Кнеза Милоша бр.3, Бешка"},{"number":73,"local":"Храм Сретења Господњег, Карловачка бр.16, Крушедол"},{"number":74,"local":"Храм Преноса моштију Светог оца Николаја, Наде Јаношевић бр.1, Крчедин"},{"number":75,"local":"Храм Светог Саве, Фрушкогорска бр.23, Марадик"},{"number":76,"local":"Храм Преноса моштију Светог оца Николаја, Главна бр.3, Ириг"},{"number":77,"local":"Храм Сретења Господњег, Главна бр.1, Нови Карловци"},{"number":78,"local":"Храм Преображења Господњег, Цара Душана бр.102, Нови Сланкамен"},{"number":79,"local":"Храм Светог оца Николаја, Стари Сланкамен"},{"number":80,"local":"Саборни храм Светог оца Николаја, Сремски Карловци"},{"number":81,"local":"Манастир Ваведења Пресвете Богородице, Сремски Карловци"},{"number":82,"local":"Храм Светих апостола Петра и Павла, Митрополита Стратимировића бр.15, Сремски Карловци"},{"number":83,"local":"Храм Ваведења Пресвете Богородице, Цара Душана бр.6, Инђија"},{"number":84,"local":"Храм Светог цара Константина и царице Јелене, Инђија"},{"number":85,"local":"Храм Светог великомученика Георгија, Инђија"},{"number":86,"local":"Храм Успења Пресвете Богородице, I новембра бр.35, Љуково"},{"number":87,"local":"Храм Преноса моштију Светог оца Николаја, Рада Опарушића бр.81, Доњи Петровци"},{"number":88,"local":"Храм Светог архангела Гаврила, Кнез Михајлова бр.3, Путинци"},{"number":89,"local":"Храм Преноса моштију Светог оца Николаја, Главна бр.45, Чортановци"},{"number":90,"local":"Храм Свете Марије Магдалине, Банстол"},{"number":91,"local":"Храм Преображења Господњег, Ириг"},{"number":92,"local":"Храм Светих апостола Петра и Павла, Ивана Милутиновића бр.127, Јарковци"}]},{"local":"Архијерејско намесништво сремскомитровачко","sites":[{"number":93,"local":"Храм Светог архангела Гаврила, Драгиње Никшић бб, Бешеново"},{"number":94,"local":"Храм Рођења Светог Јована Претече, 10. марта бр.98, Босут"},{"number":95,"local":"Храм Светог архангела Гаврила, Румска бр.1, Велики Радинци"},{"number":96,"local":"Храм Светог архангела Гаврила, Војвођанска бр.69, Гргуревци"},{"number":97,"local":"Храм Светог великомученика Георгија, Лекина бр.4, Дивош"},{"number":98,"local":"Храм Светог великомученика Георгија, Савска бр.23, Јарак"},{"number":99,"local":"Храм Св. лекара и чудотвораца Козме и Дамјана, Фрушкогорска бр.2, Кузмин"},{"number":100,"local":"Храм Светог архангела Гаврила, 1. Новембра бр.210, Лаћарак"},{"number":101,"local":"Храм Светог великомученика Георгија, Задружна бр.12, Лежимир"},{"number":102,"local":"Храм Светог великомученика Георгија, Пинкијева бр.24, Манђелос"},{"number":103,"local":"Храм Преноса моштију Светог оца Николаја, Савска бр.4, Мартинци"},{"number":104,"local":"Саборни храм Светог великомученика Димитрија, Трг Ћире Милекића бр.5, Сремска Митровица"},{"number":105,"local":"Храм Светог првомученика и архиђакона Стефана, Музејска бб, Сремска Митровица"},{"number":106,"local":"Храм Светих сирмијских мученика (Мала Босна), Раднички пут бб, Сремска Митровица"},{"number":107,"local":"Храм Св. Кирила и Методија у насељу Камењар, Војводе Степе бб, Сремска Митровица"},{"number":108,"local":"Храм Светог Јована Богослова на Новом гробљу, Вогањски пут бб, Сремска Митровица"},{"number":109,"local":"Базилика Светог великомученика Димитрија, Трг Војвођанских бригада бб, Сремска Митровица"},{"number":110,"local":"Капела Светог Козме и Дамјана (у кругу градске болнице), Сремска Митровица"},{"number":111,"local":"Капела Преподобне мати Параскеве на Старом православном, Жртава Фашизма бб, Сремска Митровица"},{"number":112,"local":"Капела Преподобне мати Параскеве и Светог Варнаве Хвостанског, Фрушкогорска бб, КПЗ Сремска Митровица"},{"number":113,"local":"Храм Преноса моштију Светог оца Николаја, Фрушкогорска бр.27, Стејановци"},{"number":114,"local":"Храм Успења Пресвете Богородице, Пионирска бр.8, Сремска Рача"},{"number":115,"local":"Храм Светог великомученика Георгија, Победа бр.10, Чалма"},{"number":116,"local":"Храм Силаска Светог Духа, Светозара Милетића бр.3, Шашинци"},{"number":117,"local":"Храм Преноса моштију Светог оца Николаја, Школска бр.1, Шуљам"}]},{"local":"Архијерејско намесништво старопазовачко","sites":[{"number":118,"local":"Храм Преноса моштију Светог оца Николаја, Краља Петра I бр.17, Белегиш"},{"number":119,"local":"Храм Преноса моштију Светог оца Николаја, Карађорђева бр.5, Војка"},{"number":120,"local":"Храм Ваведења Пресвете Богородице, Путиначка бр.3, Голубинци"},{"number":121,"local":"Храм Благовештења Пресвете Богородице, Војачка бр.2, Крњешевци"},{"number":122,"local":"Храм Свете Тројице, Светосавска бр.1, Нова Пазова"},{"number":123,"local":"Храм посвећен Преподобном Сисоју Великом, Његошева бр.3, Нова Пазова"},{"number":124,"local":"Храм Преподобне мати Параскеве, Цара Душана бр.16, Нова Пазова"},{"number":125,"local":"Храм Светог Василија Острошког чудотворца, Школска бб, Нови Бановци"},{"number":126,"local":"Храм Преноса моштију Светог оца Николаја, Главна бр.48, Стари Бановци"},{"number":127,"local":"Храм Светог пророка Илије, Вука Караџића бр.1, Стара Пазова"},{"number":128,"local":"Храм Покрова Пресвете Богородице, Његошева бр.105, Стара Пазова"},{"number":129,"local":"Храм Преноса моштију Светог оца Николаја, Брђанска бр.4, Сурдук"}]},{"local":"Архијерејско намесништво шидско","sites":[{"number":130,"local":"Храм Преноса моштију Светог оца Николаја, Бранка Радичевића бр.21, Адашевци"},{"number":131,"local":"Храм Светих апостола Петра и Павла, Батровци"},{"number":132,"local":"Храм Преноса моштију Светог оца Николаја, Војвођанска бр.2, Бачинци"},{"number":133,"local":"Храм Светих апостола Петра и Павла, Староградска бр.3, Беркасово"},{"number":134,"local":"Храм Светог Георгија, Нушићева бр.4, Бингула"},{"number":135,"local":"Храм Светог великомученика Георгија, Лењинова бр.3, Вашица"},{"number":136,"local":"Храм Преноса моштију Светог оца Николаја, Филипа Вишњића бр.2, Вишњићево"},{"number":137,"local":"Храм Свeтог прорoка Илије, Гибарац"},{"number":138,"local":"Храм Преноса моштију Светог оца Николаја, Светог Саве бр.3, Ердевик"},{"number":139,"local":"Храм Светог великомученика Георгија, Бана Јелачића бр.8, РХ Товарник"},{"number":140,"local":"Храм Светог пророка Илије, Војвођанска бр.14, Илинци"},{"number":141,"local":"Храм Светог архангела Михаила, Трг Николе Илочког бр.4, РХ Илок"},{"number":142,"local":"Храм Светог великомученика Георгија, Милоша Обилића бб, Јамена"},{"number":143,"local":"Храм Успења Пресвете Богородице, Светог Саве бр.10, Кукујевци"},{"number":144,"local":"Храм Светог архангела Гаврила, Фрушкогорска бр.41, Моловин"},{"number":145,"local":"Храм Светих апостола Петра и Павла, Сот"},{"number":146,"local":"Храм Рођења Пресвете Богородице, Краља Петра Првог бр.5, Моровић"},{"number":147,"local":"Храм Преподобне мати Параскеве, Маршала Тита бр.1, РХ Шидски Бановци"},{"number":148,"local":"Храм Преноса моштију Светог оца Николаја, Школска бр.2, Шид"},{"number":149,"local":"Храм Успенија Пресвете Богородице, Теодора Станивуковића бр.6, Шид"},{"number":150,"local":"Храм Светог великомученика Кнеза Лазара, Цара Лазара бр.49, Шид СРПСКА ПРАВОСЛАВНА ЕПАРХИЈА СРЕМСКА"}]}],"monasteries":["Манастир Крушедол","Манастир Гргетег","Манастир Велика Ремета","Манастир Ваведење","Манастир Старо Хопово","Манастир Раковац","Манастир Беочин","Манастир Врдник","Манастир Кувеждин","Манастир Ђипша","Манастир Привина Глава","Манастир Фенек","Манастир Беркасово","Манастир Бешеново","Манастир Јазак","Манастир Ново Хопово","Манастир Мала Ремета","Манастир Петковица","Манастир Шишатовац","Манастир Савинац","Манастир Свети Марко","Манастир Грабово","Манастир Манђелос","Манастир Обед"],"summary":{"deaneries":8,"sites":150,"serbia_sites":147,"croatia_sites":3,"monasteries":24}}''')
TIMOK_PARISHES = "https://eparhija-timocka.org/parohije/"
TIMOK_DATA = json.loads(r'''{"deaneries":{"57":{"local":"Архијерејско намесништво зајечарско","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-zajecarsko/"},"97":{"local":"Архијерејско намесништво бољевачко","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-boljevacko/"},"115":{"local":"Архијерејско намесништво борско-поречко","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-borsko/"},"138":{"local":"Архијерејско намесништво кључко","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-kljucko/"},"158":{"local":"Архијерејско намесништво књажевачко","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-knjazevacko/"},"176":{"local":"Архијерејско намесништво неготинско","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-negotinsko/"},"177":{"local":"Архијерејско намесништво сокобањско","url":"https://eparhija-timocka.org/namesnistvo/arhijerejsko-namesnistvo-sokobanjsko/"}},"parishes":[{"descriptor":"доњомилановачки","url":"https://eparhija-timocka.org/protojerej-ivan-milanovic/","deanery_id":115},{"descriptor":"други борски","url":"https://eparhija-timocka.org/protojerej-samoilo-sergic/","deanery_id":115},{"descriptor":"пети борски","url":"https://eparhija-timocka.org/protojerej-milenko-bajic/","deanery_id":115},{"descriptor":"први борски","url":"https://eparhija-timocka.org/djakon-dusan-stojmenovic/","deanery_id":115},{"descriptor":"први мајданпечки","url":"https://eparhija-timocka.org/protonamesnik-vlada-vukovic/","deanery_id":115},{"descriptor":"трећи борски","url":"https://eparhija-timocka.org/protojerej-milorad-filipovic/","deanery_id":115},{"descriptor":"четврти борски","url":"https://eparhija-timocka.org/protojerej-radoje-mijovic/","deanery_id":115},{"descriptor":"шести борски","url":"https://eparhija-timocka.org/jerej-darjan-komnenovic/","deanery_id":115},{"descriptor":"други бољевачки","url":"https://eparhija-timocka.org/protojerej-dejan-milivojevic/","deanery_id":97},{"descriptor":"подгорачки","url":"https://eparhija-timocka.org/jerej-milan-milanovic/","deanery_id":97},{"descriptor":"први бољевачки","url":"https://eparhija-timocka.org/protonamesnik-ristibor-stevic/","deanery_id":97},{"descriptor":"градсковачко-јасеновачки","url":"https://eparhija-timocka.org/jerej-mihajlo-gavric/","deanery_id":57},{"descriptor":"грљански","url":"https://eparhija-timocka.org/protonamesnik-zlatko-zdravkovic/","deanery_id":57},{"descriptor":"други зајечарски","url":"https://eparhija-timocka.org/protojerej-mr-igor-ivkovic/","deanery_id":57},{"descriptor":"пети зајечарски","url":"https://eparhija-timocka.org/protonamesnik-marko-pajcin/","deanery_id":57},{"descriptor":"први зајечарски","url":"https://eparhija-timocka.org/jerej-marko-radosavljevic/","deanery_id":57},{"descriptor":"седми зајечарски","url":"https://eparhija-timocka.org/jerej-nikola-pantic/","deanery_id":57},{"descriptor":"трећи зајечарски","url":"https://eparhija-timocka.org/protojerej-zoran-golubovic/","deanery_id":57},{"descriptor":"четврти зајечарски","url":"https://eparhija-timocka.org/protojerej-tomislav-stankovic/","deanery_id":57},{"descriptor":"шести зајечарски","url":"https://eparhija-timocka.org/jerej-dragan-blindzov/","deanery_id":57},{"descriptor":"брзо-паланачки","url":"https://eparhija-timocka.org/jerej-dusan-micicelovic/","deanery_id":138},{"descriptor":"велико-врбичка","url":"https://eparhija-timocka.org/jerej-milan-jankovic/","deanery_id":138},{"descriptor":"грабовички","url":"https://eparhija-timocka.org/protojerej-miroljub-pavlovic/","deanery_id":138},{"descriptor":"други кладовски","url":"https://eparhija-timocka.org/protojerej-stavrofor-milan-blagojevic/","deanery_id":138},{"descriptor":"први кладовски","url":"https://eparhija-timocka.org/protojerej-stavrofor-dragan-ivanovic/","deanery_id":138},{"descriptor":"трећи кладовски","url":"https://eparhija-timocka.org/protojerej-dejan-pajic/","deanery_id":138},{"descriptor":"четврти кладовски","url":"https://eparhija-timocka.org/protonamesnik-dusan-dinic/","deanery_id":138},{"descriptor":"други књажевачки","url":"https://eparhija-timocka.org/protonamesnik-nemanja-tobic/","deanery_id":158},{"descriptor":"први књажевачки","url":"https://eparhija-timocka.org/jerej-bogdan-tomic/","deanery_id":158},{"descriptor":"трећи књажевачки","url":"https://eparhija-timocka.org/jerej-milan-milosavljevic/","deanery_id":158},{"descriptor":"други неготински","url":"https://eparhija-timocka.org/jerej-novak-bojanic/","deanery_id":176},{"descriptor":"кобишничко-буковчански","url":"https://eparhija-timocka.org/protojerej-stavrofor-trandafir-m-jankovic/","deanery_id":176},{"descriptor":"михајловачки","url":"https://eparhija-timocka.org/protojerej-stavrofor-djordjo-jokic/","deanery_id":176},{"descriptor":"праховски","url":"https://eparhija-timocka.org/protojerej-stavrofor-ranko-aleksic/","deanery_id":176},{"descriptor":"први неготински","url":"https://eparhija-timocka.org/jerej-nikola-nesic/","deanery_id":176},{"descriptor":"радујевачки","url":"https://eparhija-timocka.org/protojerej-stavrofor-blagoje-tomic/","deanery_id":176},{"descriptor":"рајачко-рогљевски","url":"https://eparhija-timocka.org/protonamesnik-petar-colic/","deanery_id":176},{"descriptor":"трећи неготински","url":"https://eparhija-timocka.org/protonamesnik-marjan-kerculj/","deanery_id":176},{"descriptor":"четврти неготински","url":"https://eparhija-timocka.org/jerej-vuk-jovanovic/","deanery_id":176},{"descriptor":"јабуковачки","url":"https://eparhija-timocka.org/protojerej-stavrofor-vlajko-bankovic/","deanery_id":176},{"descriptor":"јасенички","url":"https://eparhija-timocka.org/jerej-slavisa-vidovic/","deanery_id":176},{"descriptor":"3. сокобањски","url":"https://eparhija-timocka.org/paroh-3-sokobanjski/","deanery_id":177},{"descriptor":"други сокобањски","url":"https://eparhija-timocka.org/protonamesnik-ivica-stankovic/","deanery_id":177},{"descriptor":"први сокобањски","url":"https://eparhija-timocka.org/protojerej-vanja-kovacevic/","deanery_id":177},{"descriptor":"јошанички","url":"https://eparhija-timocka.org/protojerej-stavrofor-ljubomir-jovanovic/","deanery_id":177}],"monasteries":[{"local":"Манастир Буково","url":"http://manastirbukovo.org/"},{"local":"Манастир Свете Тројице","url":"https://eparhija-timocka.org/manastiri/manastir-svete-trojice/"},{"local":"Манастир Суводол","url":"https://eparhija-timocka.org/manastiri/manastir-suvodol/"},{"local":"Манастир Вратна","url":"https://eparhija-timocka.org/manastir-vratna/"},{"local":"Манастир Лозица","url":"https://eparhija-timocka.org/manastiri/manastir-lozica/"},{"local":"Манастир Крепичевац","url":"https://eparhija-timocka.org/manastiri/manastir-krepicevac/"},{"local":"Манастир Грлиште","url":"https://eparhija-timocka.org/manastiri/manastir-grliste/"},{"local":"Манастир Манастирица","url":"https://eparhija-timocka.org/manastiri/manastir-manastirica/"},{"local":"Манастир Короглаш","url":"https://eparhija-timocka.org/manastiri/manastir-koroglas/"},{"local":"Манастир Лапушња","url":"https://eparhija-timocka.org/manastiri/manastir-lapusnja/"},{"local":"Манастир Јерменчић","url":"https://eparhija-timocka.org/manastiri/manastir-jermencic/"}],"summary":{"deaneries":7,"parishes":45,"monasteries":11}}''')

MILESEVA_PRIBOJ = (
    "https://milesevskaeparhija.rs/eparhija/crkve/"
    "архиејерејско-намесништво-прибојско/"
)
MILESEVA_PRIJEPOLJE = (
    "https://milesevskaeparhija.rs/eparhija/crkve/"
    "архиејерејско-намесништво-пријепољско/"
)
MILESEVA_NOVA_VAROS = (
    "https://milesevskaeparhija.rs/eparhija/crkve/"
    "arhijerejsko-namesnistvo-novovarosko/"
)
MILESEVA_PLJEVLJA = (
    "https://milesevskaeparhija.rs/eparhija/crkve/"
    "архиејерејско-намесништво-пљеваљско/"
)
MILESEVA_MONASTERIES = (
    "https://milesevskaeparhija.rs/eparhija/manastiri/"
)
RASKA_PARISHES = "https://eparhija-prizren.com/sr/parohije/"
RASKA_MONASTERIES = "https://eparhija-prizren.com/sr/manastiri/"
BACKA_SCHEMATISM = "https://eparhijabacka.info/sematizam-eparhije-backe/"
BACKA_MONASTERIES = (
    "https://eparhijabacka.info/raspored-bogosluzenja/manstiri/"
)
BANAT_MONASTERIES = "https://www.eparhijabanatska.rs/manastiri/"
SUMADIJA_MONASTERIES = (
    "https://www.eparhija-sumadijska.org.rs/index.php/eparhija/manastiri"
)
VALJEVO_SITES = "https://www.eparhijavaljevska.rs/index.php/svetinje/"

HELD_CONSTRUCTION_SITES = {
    "Капела Светог Николаја у Зебици, у изградњи",
    "Храм Светог пророка Илије у Доњем Сухотну у изградњи",
    "Храм Свете Параскеве у Каонику",
    "Храм Покрова Пресвете Богородице у Каонику",
    "Храм Светог деспота Стефана Лазаревића у Буковици (у изградњи)",
}

NIS_PARISH_CONTEXT = {
    "Новоселска парохија": "Novo Selo",
    "Ниш, Храм Светог Пантелејмона": "Niš Saint Panteleimon",
    "Ниш, Храм Светог Цара Константина и Царице Јелене":
        "Niš Saints Constantine and Helen",
    "Ниш, Храм Светог Василија Острошког": "Niš Saint Basil of Ostrog",
    "Ниш, Храм Светог Оца Николаја": "Niš Saint Nicholas",
    "Ниш, Храм Свете Петке": "Niš Saint Paraskeva",
    "Ниш, Храм Светог Луке": "Niš Saint Luke",
    "Ниш, Храм Воздвижења Часног Крста":
        "Niš Exaltation of the Holy Cross",
    "Ниш, Саборни храм Силаска Светога Духа":
        "Niš Descent of the Holy Spirit Cathedral",
    "Лесковац, Храм Св. Симеона Мироточивог":
        "Leskovac Saint Simeon the Myrrh-streaming",
    "Лесковац, Саборни храм Свете Тројице":
        "Leskovac Holy Trinity Cathedral",
    "Пирот, Саборна црква, \"Тијабарска\"":
        "Pirot Tijabara Cathedral",
    "Пирот, Стара црква \"Пазарска\"":
        "Pirot Pazar Old Church",
}

DIOCESE_QUALIFIERS = {
    "sr-milesevo": "Mileševa Diocese",
    "sr-nis": "Niš Diocese",
    "sr-raska-prizren": "Raška-Prizren Diocese",
    "sr-srem": "Srem Diocese",
    "sr-sumadija": "Šumadija Diocese",
    "sr-valjevo": "Valjevo Diocese",
    "sr-zica": "Žiča Diocese",
}
QUALIFIED_MONASTERIES = {
    "manastir-pustinja", "manastir-gracanica", "manastir-petkovica",
    "manastir-blagovestenje", "manastir-voljavca", "manastir-nikolje",
    "manastir-celije",
}

DACIA_ADMIN = "https://episcopiadaciafelix.ro/administratie-eparhiala/"
DACIA_CATHEDRAL = (
    "https://episcopiadaciafelix.ro/"
    "catedrala-episcopala-inaltarea-domnului/"
)
ROMANIAN_EXTERNAL = (
    "https://arhiva.patriarhia.ro/"
    "comunitaile-bisericesti-externe-in-anul-2023-2871.html"
)
RUSSIAN_BELGRADE = "https://patriarchia.ru/en/org/516"

TRANSLATED_LABELS = json.loads(r'''{"Базилика Светог великомученика Димитрија":"Basilica of the Holy Great Martyr Demetrius","Капела Источни Петак у Жабљану":"East Friday Chapel in Žabljan","Капела Преподобне мати Параскеве и Светог Варнаве Хвостанског":"Chapel of the Venerable Mother Paraskeva and Saint Barnabas of Hvostan","Капела Преподобне мати Параскеве на Старом православном":"Chapel of the Venerable Mother Paraskeva on the Old Orthodox Church","Капела Преподобномученице Параскеве у Катуну":"Chapel of the Venerable Martyr Paraskeva in Katun","Капела Свете великомученице Марине у Брзи":"Chapel of the Holy Great Martyr Marina in Brza","Капела Светог Козме и Дамјана (у кругу градске болнице)":"Chapel of St. Cosmas and Damian (inside the city hospital)","Капела Светог Пантелејмона у Горини":"Chapel of Saint Panteleimon in Gorina","Капела Светог архангела Гаврила":"Chapel of the Holy Archangel Gabriel","Капела светих Апостола Петра и Павла у Краљеву":"Chapel of the Holy Apostles Peter and Paul in Kraljevo","Капела светих Мученика Савела, Исмаила и Мануила у Пруговцу":"Chapel of the Holy Martyrs Savel, Ismail and Manuel in Prugovec","Манастир - Скит Светог великомученика Димитрија у Влајковцу":"Monastery - Monastery of the Holy Great Martyr Demetrius in Vlajkovac","Манастир Ђипша":"Đipša Monastery","Манастир Ђунис":"Djunis Monastery","Манастир Ђурђеви Ступови":"Đurđevi Stupovi Monastery","Манастир Јазак":"Jazak Monastery","Манастир Јашуња - Пр. Богородице":"Jašunja Monastery - Pr. Mother of God","Манастир Јашуња - Св.Јован Крститељ":"Jašunja Monastery - St. John the Baptist","Манастир Јежевица":"Ježevica Monastery","Манастир Јерменчић":"Jermenčić Monastery","Манастир Јовања":"Jovanja Monastery","Манастир Јовање":"Jovanje Monastery","Манастир Јошаница":"Jošanica Monastery","Манастир Ћелије":"Čelije Monastery","Манастир Ајдановац":"Ajdanovac Monastery","Манастир Баваниште":"Bavanište Monastery","Манастир Бањска":"Banjska Monastery","Манастир Беочин":"Beočin Monastery","Манастир Беркасово":"Berkasovo Monastery","Манастир Бешеново":"Bešenovo Monastery","Манастир Бистрица":"Bistrica Monastery","Манастир Благовештење":"Annunciation Monastery","Манастир Боговађа":"Monastery of Bogovađa","Манастир Бођани":"Bođani Monastery","Манастир Брезовац":"Brezovac Monastery","Манастир Брњак":"Brnjak Monastery","Манастир Будисавци":"Budisavci Monastery","Манастир Буково":"Bukovo Monastery","Манастир Ваведења Пресвете Богородице":"Monastery of the Introduction of the Holy Mother of God","Манастир Ваведење":"Vavedenje Monastery","Манастир Вазнесење":"Ascension Monastery","Манастир Велика Ремета":"Velika Remeta Monastery","Манастир Вета":"Veta Monastery","Манастир Високи Дечани":"Visoki Decani Monastery","Манастир Височка Ржана":"Monastery of Visočka Ržana","Манастир Војловица":"Vojlovica Monastery","Манастир Вољавча":"Voljavca Monastery","Манастир Вратна":"Vratna Monastery","Манастир Врачево":"Vračevo Monastery","Манастир Враћевшница":"Vraćevšnica Monastery","Манастир Врдник":"Vrdnik Monastery","Манастир Вујан":"Vujan Monastery","Манастир Габровац":"Gabrovac Monastery","Манастир Гориоч":"Gorioč Monastery","Манастир Горњи Матејевац":"Gornji Matejevac Monastery","Манастир Грабовац":"Grabovac Monastery","Манастир Грабово":"Grabovo Monastery","Манастир Градац":"Gradac Monastery","Манастир Грачаница":"Gracanica Monastery","Манастир Гргетег":"Grgeteg Monastery","Манастир Грлиште":"Grlište Monastery","Манастир Грнчарица":"Grnčarica Monastery","Манастир Давидовица":"Davidovica Monastery","Манастир Девине Воде":"Devine Voda Monastery","Манастир Девич":"Devič Monastery","Манастир Денковац":"Denkovac Monastery","Манастир Дивостин":"Divostin Monastery","Манастир Дивљана":"Divljana Monastery","Манастир Доброводица":"Dobrovodica Monastery","Манастир Докмир":"Dokmir Monastery","Манастир Драганац":"Draganac Monastery","Манастир Драча":"Monastery of Durres","Манастир Дубница":"Dubnica Monastery","Манастир Дубоки Поток":"Duboki Potok Monastery","Манастир Дубрава":"Dubrava Monastery","Манастир Жича":"Žiča Monastery","Манастир Завидинце":"Monastery of Zavidince","Манастир Згодачица":"Zgodacica Monastery","Манастир Зочиште":"Zočište Monastery","Манастир Иверица":"Iverica monastery","Манастир Изатовац":"Izatovac Monastery","Манастир Каленић":"Kalenić Monastery","Манастир Каменац":"Kamenac Monastery","Манастир Каменица":"Kamenica Monastery","Манастир Кастаљан":"Kastaljan Monastery","Манастир Клисура":"Klisura Monastery","Манастир Ковиљ":"Kovilj Monastery","Манастир Ковиље":"Kovilje Monastery","Манастир Кончул":"Končul Monastery","Манастир Короглаш":"Koroglaš Monastery","Манастир Крепичевац":"Krepičevac Monastery","Манастир Крупац":"Krupac Monastery","Манастир Крушедол":"Krušedol Monastery","Манастир Кувеждин":"Kuvezhdin Monastery","Манастир Куманица":"Kumanica Monastery","Манастир Лапушња":"Lapusnja Monastery","Манастир Лелић":"Lelić Monastery","Манастир Липар":"Lipar Monastery","Манастир Липовац":"Lipovac Monastery","Манастир Лозица":"Lozica Monastery","Манастир Мажићи":"Mažići Monastery","Манастир Мала Ремета":"Mala Remeta Monastery","Манастир Манастирак":"Manastirak Monastery","Манастир Манастирица":"Monastery Monastery","Манастир Манђелос":"Manđelos Monastery","Манастир Месић":"Mesić Monastery","Манастир Милешева":"Mileševa Monastery","Манастир Никоље":"Nikolje Monastery","Манастир Нова Павлица":"Nova Pavlica Monastery","Манастир Ново Хопово":"Novo Hopovo Monastery","Манастир Обед":"Monastery Obed","Манастир Павловац":"Pavlovac Monastery","Манастир Петковица":"Petkovica Monastery","Манастир Пећка Патријаршија":"Peć Patriarchate Monastery","Манастир Пиносава":"Pinosava Monastery","Манастир Пирковац":"Pirkovac Monastery","Манастир Планиница":"Planinica Monastery","Манастир Плочник":"Pločnik Monastery","Манастир Поганово":"Poganovo Monastery","Манастир Прекопеча":"Prekopeča Monastery","Манастир Преображење":"Transfiguration Monastery","Манастир Прерадовац":"Preradovac Monastery","Манастир Привина Глава":"Privina Glava Monastery","Манастир Придворица":"Pridvorica Monastery","Манастир Пустиња":"Pustinja Monastery","Манастир Раковац":"Rakovac Monastery","Манастир Ралетинац":"Raletinac Monastery","Манастир Рача":"Rača Monastery","Манастир Рсовци":"Rsovci Monastery","Манастир Рујан":"Rujan Monastery","Манастир Савинац":"Savinac Monastery","Манастир Саринац":"Sarinac Monastery","Манастир Св. Димитрија - Манастирче":"Monastery of St. Dimitrija - Manastirče","Манастир Св. Николе - Куршумлија":"Monastery of St. Nikole - Kuršumlija","Манастир Св. Онуфрија":"Monastery of St. Onufria","Манастир Св. Роман":"Monastery of St. Novel","Манастир Света Тројица":"Holy Trinity Monastery","Манастир Свете Меланије у Зрењанину":"Monastery of Saint Melania in Zrenjanin","Манастир Свете Недеље":"Monastery of Saint Nedelja","Манастир Свете Тројице":"Monastery of the Holy Trinity","Манастир Свете Тројице у Кикинди":"Monastery of the Holy Trinity in Kikinda","Манастир Свети Марко":"Saint Mark's Monastery","Манастир Светих Арханђела":"Monastery of the Holy Archangels","Манастир Светих Козме и Дамјана - Водена Пољана":"Monastery of Saints Cosmas and Damian - Vodena Poljana","Манастир Светог Јоакима и Ане - Света Јања":"Monastery of St. Joachim and Anna - St. Janja","Манастир Светог Димитрија у Сушици":"Monastery of Saint Demetrius in Sušica","Манастир Светог Николаја - Прибојска Бања":"Saint Nicholas Monastery - Pribojska Banja","Манастир Светог пророка Илије - Јабука":"Monastery of the Holy Prophet Elijah - Jabuka","Манастир Сељани":"Seljani Monastery","Манастир Сибница":"Sibnica Monastery","Манастир Сињац":"Sinjac Monastery","Манастир Сићево":"Sićevo Monastery","Манастир Смиловци":"Smilovci Monastery","Манастир Соколица":"Sokolica Monastery","Манастир Сопоћани":"Sopoćani Monastery","Манастир Сочаница":"Sočanica Monastery","Манастир Средиште":"Srediste Monastery","Манастир Сретење":"Sretenje Monastery","Манастир Старо Хопово":"Staro Hopovo Monastery","Манастир Стубал":"Stubal Monastery","Манастир Студеница":"Studenica Monastery","Манастир Стјеник":"Stjenik Monastery","Манастир Суводол":"Suvodol Monastery","Манастир Суково":"Sukovo Monastery","Манастир Темска":"Temska Monastery","Манастир Тресије":"Tresije Monastery","Манастир Тушимља":"Tušimlja Monastery","Манастир Увац":"Uvac Monastery","Манастир Улије":"Ulija Monastery","Манастир Успеније":"Uspenija Monastery","Манастир Успења Пресавете Богородице у Ђаковици":"Monastery of the Assumption of the Blessed Virgin Mary in Đakovica","Манастир Успења Пресвете Богородице у Доњем Кормињану":"Monastery of the Assumption of the Blessed Virgin Mary in Donji Korminjan","Манастир Фенек":"Fenek Monastery","Манастир Хајдучица":"Hajdučica Monastery","Манастир Црковница":"Crkovnica Monastery","Манастир Црна Река":"Crna Reka Monastery","Манастир Шишатовац":"Šišatovac Monastery","Манастир Шуљковац":"Monastery Šuljkovac","Манастир у Каћу":"Monastery in Kać","Саборни":"Cathedral","Саборни храм Светог Василија Острошког, Пријепоље":"Cathedral of Saint Vasilij Ostroški, Prijepolje","Саборни храм Светог великомученика Димитрија":"Cathedral of the Holy Great Martyr Demetrius","Саборни храм Светог оца Николаја":"Cathedral of Saint Father Nicholas","Скит Светих четрдесет мученика севастијских у Старом Селу код Гаја":"Skete of the Holy Forty Martyrs of Sevasti in Stari Selo near Guy","Храм - капела Светог Нектарија Егинског":"Church - Chapel of Saint Nektarios of Aegina","Храм Cветог мученика Мине у Димитровграду":"Church of the Flower Martyr Mina in Dimitrovgrad","Храм Благовести Пресвете Богородице":"Church of the Annunciation of the Holy Mother of God","Храм Благовести Пресвете Богородице, при Манастиру Градац":"The Church of the Annunciation of the Holy Mother of God, near the Gradac Monastery","Храм Благовештења Господњег - Каран":"Temple of the Annunciation of the Lord - Karan","Храм Благовештења Пресвете Богородице":"Church of the Annunciation of the Holy Mother of God","Храм Благовештења Пресвете Богородице, Буковик":"Church of the Annunciation of the Blessed Virgin Mary, Bukovik","Храм Благовештења Пресвете Богородице, Штитково":"Church of the Annunciation of the Blessed Virgin Mary, Štitkovo","Храм Богојављења Господњег":"Church of the Epiphany of the Lord","Храм Ваведења Пресвете Богородице":"Church of the Presentation of the Holy Mother of God","Храм Ваведења Пресвете Богородице у Радејни":"Church of the Presentation of the Blessed Virgin Mary in Radejna","Храм Ваведења Пресвете Богородице, Ранче Поље":"Church of the Presentation of the Blessed Virgin Mary, Ranche Polje","Храм Ваведења Пресвете Богородице, при Манастиру Павлица":"The Church of the Presentation of the Blessed Virgin Mary, near the Pavlica Monastery","Храм Вазнесења Господњег":"Temple of the Ascension of the Lord","Храм Вазнесења Господњег (XII в.)":"Temple of the Ascension (XII century)","Храм Вазнесења Господњег - Дубрава":"Temple of the Ascension of the Lord - Dubrava","Храм Вазнесења Господњег - Каменица":"Temple of the Ascension - Kamenica","Храм Вазнесења Господњег - Кршање":"Temple of the Ascension - Violation","Храм Вазнесења Господњег - Рогачица":"Temple of the Ascension of the Lord - Rogačica","Храм Вазнесења Господњег у Белој Паланци":"Temple of the Ascension in Bela Palanka","Храм Вазнесења Господњег у Великом Крчимиру":"Church of the Ascension of the Lord in Veliki Krčimir","Храм Вазнесења Господњег у Горњем Матејевцу":"Church of the Ascension of the Lord in Gornji Matejevac","Храм Вазнесења Господњег у Градињу":"Temple of the Ascension of the Lord in Gradinje","Храм Вазнесења Господњег у Грејачу":"Temple of the Ascension in Grejač","Храм Вазнесења Господњег у Жељуши":"Temple of the Ascension of the Lord in Željuša","Храм Вазнесења Господњег у Медвеђи":"Temple of the Ascension of the Lord in Medvedja","Храм Вазнесења Господњег у Смиловцима":"Church of the Ascension of the Lord in Smilovci","Храм Вазнесења Господњег у Црквини":"Temple of the Ascension of the Lord in the Church","Храм Вазнесења Господњег, Бучје":"Temple of the Ascension of the Lord, Bučje","Храм Вазнесења Господњег, Височка":"Church of the Ascension of the Lord, Visočka","Храм Вазнесења Господњег, Штаваљ":"Temple of the Ascension of the Lord, Štavalj","Храм Васкрсења Лазаревог у Коњуви":"Church of the Resurrection of Lazarus in Konjuva","Храм Васкрсења Христовог у Нишу":"Church of the Resurrection of Christ in Niš","Храм Васкрсења Христовог, Нови Прибој":"Church of the Resurrection of Christ, Novi Priboj","Храм Воздвижења Часног крста у Великој Црквици":"The Church of the Exaltation of the Holy Cross in Velika Crkvica","Храм Живоносног Источника Пресвете Богородице":"Church of the Life-giving Source of the Most Holy Theotokos","Храм Живоносног Источника у Милићевцима":"Temple of the Living Source in Milićevci","Храм Обновљења храма Светог великомученика Георгија":"Church of the Restoration of the Church of the Holy Great Martyr George","Храм Обновљења храма светог Великомученика Георгија у Завидинцима":"Church of the Restoration of the Church of the Holy Great Martyr George in Zavidinci","Храм Покрова Пресвете Богородице":"Temple of the Shroud of the Holy Mother of God","Храм Покрова Пресвете Богородице - Јабланица":"Temple of the Intercession of the Holy Virgin - Jablanica","Храм Покрова Пресвете Богородице - Горњи Бањани":"Temple of the Intercession of the Holy Virgin - Gornji Banjani","Храм Покрова Пресвете Богородице - Луке":"Temple of the Covering of the Holy Virgin - Luke","Храм Покрова Пресвете Богородице - Растиште":"Temple of the Intercession of the Holy Mother of God - Rastište","Храм Покрова Пресвете Богородице - Савово":"Temple of the Intercession of the Holy Virgin - Savovo","Храм Покрова Пресвете Богородице у Великом Шиљеговцу":"Temple of the Intercession of the Holy Virgin in Veliki Šiljegovec","Храм Покрова Пресвете Богородице у Гредетину":"Temple of the Intercession of the Holy Virgin in Gredetin","Храм Покрова Пресвете Богородице у Мирници":"The Church of the Intercession of the Holy Mother of God in Mirnica","Храм Покрова Пресвете Богородице, Прибојска Голеша, Прибој":"Temple of the Intercession of the Holy Virgin, Pribojska Goleša, Priboj","Храм Пренос моштију Светог оца Николаја":"Church of the Transfer of the Relics of the Holy Father Nicholas","Храм Преноса моштију Светог Николаја Мирликијског":"The Church of the Transfer of the Relics of Saint Nicholas of Myrliki","Храм Преноса моштију Светог Николаја Мирликијског - Брусница":"The Church of the Transfer of the Relics of St. Nicholas of Myrliki - Brusnica","Храм Преноса моштију Светог Николаја Мирликијског у Косовици":"The Church of the Transfer of the Relics of St. Nicholas of Myrliki in Kosovica","Храм Преноса моштију Светог Николаја Мирликијског у Крупцу":"The Church of the Transfer of the Relics of St. Nicholas of Mirliki in Krupac","Храм Преноса моштију Светог Николаја Мирликијског у Прекопчелици":"The Church of the Transfer of the Relics of St. Nicholas of Myrliki in Prekopčelica","Храм Преноса моштију Светог Николаја Чудотворца у Бабушници":"The Church of the Transfer of the Relics of Saint Nicholas the Wonderworker in Babušnica","Храм Преноса моштију Светог Саве Српског - Мећавник":"Church of the Transfer of the Relics of Saint Sava of Serbia - Mećavnik","Храм Преноса моштију Светог оца Николаја":"The Church of the Transfer of the Relics of Saint Nicholas","Храм Преображења Господњег":"Temple of the Transfiguration of the Lord","Храм Преображења Господњег - Братљево":"Temple of the Transfiguration of the Lord - Bratljevo","Храм Преображења Господњег - Златибор":"Temple of the Transfiguration - Zlatibor","Храм Преображења Господњег - ман. Придворица":"Temple of the Transfiguration of the Lord - min. Courthouse","Храм Преображења Господњег у Љуптену":"The Church of the Transfiguration of the Lord in Ljuptena","Храм Преображења Господњег у Доњој Јошаници":"The Church of the Transfiguration of the Lord in Donja Jošanica","Храм Преображења Господњег у Игришту":"The Church of the Transfiguration in the Playground","Храм Преображења Господњег у Магову":"The Church of the Transfiguration of the Lord in Magova","Храм Преображења Господњег у Пролом Бањи":"Temple of the Transfiguration in Prolom Banja","Храм Преображења Господњег у Сијарини":"The Church of the Transfiguration of the Lord in Sijarina","Храм Преображења Господњег у Хуму":"The Church of the Transfiguration of the Lord in Hum","Храм Преображења Господњег, Радоина":"Church of the Transfiguration of the Lord, Radoina","Храм Преподобне Ангелине Српске":"Church of Venerable Angelina Srpska","Храм Преподобне Параскеве":"Church of the Venerable Paraskeva","Храм Преподобне Параскеве - Коштунићи":"Church of the Venerable Paraskeva - Koštunići","Храм Преподобне Параскеве - Поникве":"Church of the Venerable Paraskeva - Ponikve","Храм Преподобне Параскеве у Горњој Горевници":"The Church of the Venerable Paraskeva in Gornja Gorevnica","Храм Преподобне Параскеве у Доњој Рсовачи":"The Church of the Venerable Paraskeva in Donja Rsovača","Храм Преподобне Параскеве у Доњој Трнави":"The Church of the Venerable Paraskeva in Donja Trnava","Храм Преподобне Параскеве у Рујнику":"The Church of the Venerable Paraskeva in Rujnik","Храм Преподобне мати Параскеве":"Church of the Venerable Mother Paraskeva","Храм Преподобне мати Параскеве - Мочиоци":"Church of the Venerable Mother Paraskeva - Močioci","Храм Преподобне мати Параскеве - Рудница":"Church of the Venerable Mother Paraskeva - Rudnica","Храм Преподобне мати Параскеве - Свете Петке, Бабине":"Church of the Venerable Mother Paraskeva - Svete Petka, Babine","Храм Преподобномученице Параскеве у Станцима":"The Church of the Venerable Martyr Paraskeva in Stanci","Храм Преподобномученице Параскеве у Трњану":"Church of the Venerable Martyr Paraskeva in Trnjan","Храм Пресвете Богородице - Живоносног Источника - Солотуша":"Church of the Holy Mother of God - Life-giving Source - Solotuša","Храм Пресвете Богородице Млекопитатљнице":"Church of the Holy Mother of God of the Milkmaid","Храм Пресвете Богородице Тројеручице":"Church of the Most Holy Theotokos Trojeručica","Храм Пресвете Богородице Тројеручице - Конарево":"Church of the Most Holy Theotokos - Konarevo","Храм Пресвете Богородице у Бабици":"Church of the Holy Virgin in Babica","Храм Пресвете Богородице у Горњој Невљи":"The Church of the Holy Virgin in Gornja Nevlja","Храм Прображења Господњег у Клајићу":"Church of the Transfiguration of the Lord in Klajić","Храм Рођења Пресвете Богородице":"Church of the Nativity of the Holy Mother of God","Храм Рођења Пресвете Богородице - Власово":"Church of the Nativity of the Blessed Virgin Mary - Vlasovo","Храм Рођења Пресвете Богородице - Качуљице":"Church of the Nativity of the Blessed Virgin Mary - Kačuljice","Храм Рођења Пресвете Богородице - Косјерић":"Church of the Birth of the Blessed Virgin Mary - Kosjerić","Храм Рођења Пресвете Богородице у Димитровграду":"Church of the Nativity of the Blessed Virgin Mary in Dimitrovgrad","Храм Рођења Пресвете Богородице у Доњoj РечициХрам Рођења Пресвете Богородице у Доњој Речици":"Church of the Nativity of the Holy Mother of God in Donja Rečica Temple of the Birth of the Holy Mother of God in Donja Rečica","Храм Рођења Пресвете Богородице у Мокри":"Church of the Nativity of the Holy Mother of God in Mokra","Храм Рођења Пресвете Богородице, при Манастиру Каменцу":"The Church of the Nativity of the Blessed Virgin Mary, near the Kamenec Monastery","Храм Рођења Светог Јована Крститеља":"Church of the Nativity of St. John the Baptist","Храм Рођења Светог Јована Крститеља - Љиг":"Church of the Nativity of St. John the Baptist - Ljig","Храм Рођења Светог Јована Крститеља - Озрем":"Church of the Nativity of St. John the Baptist - Ozrem","Храм Рођења Светог Јована Крститеља - Семегњево":"Church of the Nativity of St. John the Baptist - Semegnjevo","Храм Рођења Светог Јована Крститеља у Јашуњи":"Church of the Nativity of St. John the Baptist in Jašunja","Храм Рођења Светог Јована Крститеља у Грделици":"Church of the Nativity of St. John the Baptist in Grdelica","Храм Рођења Светог Јована Крститеља у Качапору":"Church of the Nativity of St. John the Baptist in Kačapor","Храм Рођења Светог Јована Крститеља у селу Ореовац":"Church of the Nativity of St. John the Baptist in the village of Oreovac","Храм Рођења Светог Јована Претече":"Church of the Nativity of St. John the Forerunner","Храм Рођења Светог Јована Претече и Крститеља":"Church of the Nativity of St. John the Forerunner and Baptist","Храм Рођења Христовог у Пироту":"Church of the Nativity of Christ in Pirot","Храм Рођења Христовог, Златар":"Church of the Nativity of Christ, Zlatar","Храм Рођења светог Јована Крститеља у Вучју":"Church of the Nativity of St. John the Baptist in Vučje","Храм Рођења светог Јована Крститеља у Орљану":"Church of the Nativity of St. John the Baptist in Orljan","Храм Сабора Светог Јована Крститеља":"Church of the Congregation of St. John the Baptist","Храм Сабора Српских Светитеља":"Church of the Assembly of Serbian Saints","Храм Сабора светих Апостола у Турековцу":"Church of the Assembly of the Holy Apostles in Turekovac","Храм Сабора светог архангела Гаврила":"Church of the Assembly of the Holy Archangel Gabriel","Храм Св. Јована Крститеља - Дићи":"Temple of St. John the Baptist - Dici","Храм Св. Великомученика Пантелејмона у Краљеву":"Temple of St. Great Martyr Panteleimon in Kraljevo","Храм Св. Кирила и Методија у насељу Камењар":"Temple of St. Cyril and Methodius in the Kamenjar settlement","Храм Св. великомученика Георгија - Рудник":"Temple of St. of the Great Martyr Georgi - Rudnik","Храм Св. лекара и чудотвораца Козме и Дамјана":"Temple of St. doctors and miracle workers Cosma and Damjan","Храм Свeтог прорoка Илије":"Temple of the Holy Prophet Ilia","Храм Свете Варваре у Малом Дреновцу":"Church of St. Varvara in Mali Drenovac","Храм Свете Марије Магдалине":"Church of St. Mary Magdalene","Храм Свете Марије Магдалине - Плешин":"Church of St. Mary Magdalene - Plešin","Храм Свете Марије Магдалине - Шљивовица":"Church of St. Mary Magdalene - Šljivovica","Храм Свете Марије Магдалине у Игришту":"Church of St. Mary Magdalene in Igrište","Храм Свете Марије Магдалине у Каонику":"Church of St. Mary Magdalene in Kaonik","Храм Свете Марије Магдалине у Радевцу":"Church of St. Mary Magdalene in Radevac","Храм Свете Марије Магдалине у Чиниглавцима":"Church of Saint Mary Magdalene in Činiglavci","Храм Свете Марије Магдалине, Врсјенице":"Church of St. Mary Magdalene, Vrsjenica","Храм Свете Недеље - Трипкова":"Church of Saint Nedelja - Tripkova","Храм Свете Параскеве у Кашевару":"Church of St. Paraskeva in Kaševar","Храм Свете Параскеве у Поповцу":"Church of Saint Paraskeva in Popovac","Храм Свете Петке у Ђинђуши":"Church of Saint Petka in Đinđuša","Храм Свете Петке у Ђунису":"Church of Saint Petka in Djunis","Храм Свете Петке у Јаловик Извору":"Church of Saint Petka in Jalovik Izvor","Храм Свете Петке у Бресту":"Church of Saint Petka in Brest","Храм Свете Петке у Великом Шиљеговцу":"Church of Saint Petka in Veliki Šiljegovac","Храм Свете Петке у Вишеселу":"Church of Saint Petka in Višeselo","Храм Свете Петке у Гвоздићу":"Church of Saint Petka in Gvozdić","Храм Свете Петке у Градишници":"Church of Saint Friday in Gradisnica","Храм Свете Петке у Градишту":"Church of Saint Friday in Gradište","Храм Свете Петке у Губетину":"Church of Saint Petka in Gubetin","Храм Свете Петке у Девчи":"Church of Saint Petka in Devča","Храм Свете Петке у Димитровграду":"Church of Saint Petka in Dimitrovgrad","Храм Свете Петке у Добром Долу":"Church of Saint Petka in Dobro Dol","Храм Свете Петке у Доњем Матејевцу":"Church of Saint Petka in Donji Matejevac","Храм Свете Петке у Жучу":"Church of Saint Petka in Žuč","Храм Свете Петке у Каонику":"Church of Saint Petka in Kaonik","Храм Свете Петке у Малом Суводолу":"Church of Saint Petka in Mali Suvodol","Храм Свете Петке у Малчи":"Church of Saint Petka in Malca","Храм Свете Петке у Мачковцу":"Church of Saint Petka in Mačkovec","Храм Свете Петке у Нишу":"Church of Saint Petka in Niš","Храм Свете Петке у Петровцу":"Church of Saint Petka in Petrovac","Храм Свете Петке у Прекопуцу":"Church of Saint Friday in Prekopuc","Храм Свете Петке у Росици":"Church of Saint Petka in Rosica","Храм Свете Петке у Сечаници":"Church of Saint Friday in Sečanica","Храм Свете Петке у Смиловцима":"Church of Saint Petka in Smilovci","Храм Свете Петке у Станушићима":"Church of Saint Petka in Stanušići","Храм Свете Петке у Темској":"Church of Saint Friday in Temska","Храм Свете Петке у Церови":"Church of Saint Petka in Cerova","Храм Свете Преподобномученице Параскеве у Мозгову (Река)":"Church of the Holy Martyr Paraskeva in Mozgov (Reka)","Храм Свете Тројице":"Church of the Holy Trinity","Храм Свете Тројице - Бјелуша":"Church of the Holy Trinity - Bjeluša","Храм Свете Тројице - Варево":"Church of the Holy Trinity - Varevo","Храм Свете Тројице - Горњи Милановац":"Church of the Holy Trinity - Gornji Milanovac","Храм Свете Тројице - Драглица":"Holy Trinity Church - Draglica","Храм Свете Тројице - Зарожје":"Holy Trinity Church - Zarožje","Храм Свете Тројице - Печеног":"Church of the Holy Trinity - Pečenog","Храм Свете Тројице Русалијске или ''Латинска црква'' у Горњем Матејевцу":"Church of the Holy Trinity Rusal or \"Latin church\" in Gornji Matejevac","Храм Свете Тројице и Св. цара Лазара - Заовине":"Church of the Holy Trinity and St. Tsar Lazar - Zaovina","Храм Свете Тројице у Борову":"Church of the Holy Trinity in Borovo","Храм Свете Тројице у Вичи":"Church of the Holy Trinity in Viča","Храм Свете Тројице у Габровцу":"Church of the Holy Trinity in Gabrovac","Храм Свете Тројице у Глоговици":"Church of the Holy Trinity in Glogovica","Храм Свете Тројице у Горњем Адровцу":"Holy Trinity Church in Gornji Adrovac","Храм Свете Тројице у Горњој Врежини":"Holy Trinity Church in Gornja Vrežina","Храм Свете Тројице у Горњој Студени":"Holy Trinity Church in Gornja Studena","Храм Свете Тројице у Грбавче":"Church of the Holy Trinity in Grbavce","Храм Свете Тројице у Гуленовцима":"The Church of the Holy Trinity in Gulenovice","Храм Свете Тројице у Гњилану":"Church of the Holy Trinity in Gjilan","Храм Свете Тројице у Димитровграду":"Church of the Holy Trinity in Dimitrovgrad","Храм Свете Тројице у Драгинцу":"Holy Trinity Church in Draginac","Храм Свете Тројице у Заграђу":"Holy Trinity Church in Zagrađe","Храм Свете Тројице у Засковцима":"Holy Trinity Church in Zaskovci","Храм Свете Тројице у Извору":"Church of the Holy Trinity in Izvor","Храм Свете Тројице у Куманову":"Church of the Holy Trinity in Kumanovo","Храм Свете Тројице у Лалинским Појатама":"The Church of the Holy Trinity in Lalinski Pojate","Храм Свете Тројице у Лукавици":"Church of the Holy Trinity in Lukavica","Храм Свете Тројице у Маровцу":"Holy Trinity Church in Marovac","Храм Свете Тројице у Међуречју":"Church of the Holy Trinity in Medjurečje","Храм Свете Тројице у Мозгову":"Church of the Holy Trinity in Mozgov","Храм Свете Тројице у Мршинцима":"Holy Trinity Church in Mršinci","Храм Свете Тројице у Ображдама":"Holy Trinity Church in Obrazde","Храм Свете Тројице у Петерлашу":"Church of the Holy Trinity in Peterlash","Храм Свете Тројице у Преконоги":"Church of the Holy Trinity in Prekonoga","Храм Свете Тројице у Рибару":"Church of the Holy Trinity in Ribar","Храм Свете Тројице у Рудињу":"Church of the Holy Trinity in Rudinje","Храм Свете Тројице у Селишту":"Holy Trinity Church in Seliste","Храм Свете Тројице у Топлом Долу":"Holy Trinity Church in Toplo Dol","Храм Свете Тројице у Требињу":"Holy Trinity Church in Trebinje","Храм Свете Тројице у Трубњу":"Church of the Holy Trinity in Trubnje","Храм Свете Тројице у Туларама":"Holy Trinity Church in Tulare","Храм Свете Тројице, Брњица":"Church of the Holy Trinity, Brnjica","Храм Свете Тројице, Нова Варош":"Church of the Holy Trinity, Nova Varoš","Храм Свете Тројице, Радијевићи":"Church of the Holy Trinity, Radijevići","Храм Свете великомученице Марине":"Church of the Holy Great Martyr Marina","Храм Свете великомученице Марине - Бело Поље":"Church of the Holy Martyr Marina - Belo Polje","Храм Свете великомученице Марине - Огњене Марије":"Church of Saint Great Martyr Marina - Fire Mary","Храм Свете великомученице Марине у Вичи":"Church of the Holy Great Martyr Marina in Viča","Храм Свете великомученице Марине у Клисурици":"Church of the Holy Great Martyr Marina in Klisurika","Храм Свете великомученице Марине у Паљини":"Church of the Holy Great Martyr Marina in Paljina","Храм Свете великомученице Марине у Претрешњи":"Church of the Holy Great Martyr Marina in Pretrešnja","Храм Свете великомученице Марине у Рутевцу":"Church of the Holy Great Martyr Marina in Rutevac","Храм Свете великомученице Марине у Чокотину":"Church of the Holy Great Martyr Marina in Čokotin","Храм Свете великомученице Марине у Чучалу":"Church of the Holy Great Martyr Marina in Čučal","Храм Свете великомученице Марине, Камена Гора":"Church of the Holy Martyr Marina, Kamena Gora","Храм Свете великомученице Недеље у Јелашници":"Church of the Holy Great Martyr Nedelja in Jelasnica","Храм Свете великомученице Недеље у Батушинцу":"Church of the Holy Great Martyr Nedelja in Batušinac","Храм Свете великомученице Недеље у Заплањској Топоници":"Church of the Holy Great Martyr Nedelja in Zaplanjska Toponica","Храм Свете великомученице Недеље у Каонику":"Church of the Holy Great Martyr Nedelja in Kaonik","Храм Свете великомученице Параскеве у Великом Дреновцу":"The Church of the Holy Great Martyr Paraskeva in Veliki Drenovac","Храм Свете великомученице Параскеве у Рудару":"Church of the Holy Great Martyr Paraskeva in Rudar","Храм Свете великомученице Петке у Извору":"Church of the Holy Great Martyr Petka in Izvor","Храм Свете муч. Марине - Головша":"Church of the Holy Martyr. Marine - Golovsha","Храм Свете мученице Недеље у Горњем Адровцу":"Church of the Holy Martyr Nedelja in Gornji Adrovac","Храм Свете преподобне Параскеве у Култешу":"Church of Saint Paraskeva in Kulteš","Храм Свете преподобне Параскеве у Ступници":"Church of Saint Paraskeva in Stupnica","Храм Свете преподобне мајке Параскеве у Кумареву":"Church of the Holy Venerable Mother Paraskeva in Kumarevo","Храм Свете преподобномученице Параскеве":"Church of the Holy Venerable Martyr Paraskeva","Храм Свете преподобномученице Параскеве у Крављу":"Church of the Holy Reverend Martyr Paraskeva in Kravlje","Храм Свете преподобномученице Параскеве у Шпају":"Church of the Holy Reverend Martyr Paraskeva in Špaj","Храм Светих 40 мученика Севастијских - Старо Село":"Church of the Holy 40 Martyrs of Sevastija - Staro Selo","Храм Светих Јоакима и Ане у Бацу":"Church of Saints Joachim and Anna in Bac","Храм Светих Ћирила и Методија":"Church of Saints Cyril and Methodius","Храм Светих Ћирила и Методија у Црвеној Реци":"Church of Saints Cyril and Methodius in Crvena Reka","Храм Светих Апостола Петра и Павла":"Church of the Holy Apostles Peter and Paul","Храм Светих Апостола Петра и Павла у Доњем Коњувцу":"Church of the Holy Apostles Peter and Paul in Donji Konjuvac","Храм Светих Архангела Михаила и Гаврила у Делиграду":"Church of the Holy Archangels Michael and Gabriel in Deligrad","Храм Светих Бесребреника Козме и Дамјана у Малој Плани":"Church of Saints Besrebrenik Cosma and Damian in Mala Plana","Храм Светих Кирика и Јулите у Станињцу":"Church of Saints Kirik and Julita in Staninjec","Храм Светих Козме и Дамјана - Остатија":"Church of Saints Cosmas and Damian - Ostija","Храм Светих Константина и Јелене у Великом Крушинцу":"Church of Saints Constantine and Jelena in Veliki Krušinac","Храм Светих Константина и Јелене у Лозанцу":"Church of Saints Constantine and Helena in Lausanne","Храм Светих Константина и Јелене у Лоћики":"Church of Saints Constantine and Jelena in Loćika","Храм Светих ап. Петра и Павла":"Church of Saints ap. Peter and Paul","Храм Светих апостола Петра и Павла":"Church of the Holy Apostles Peter and Paul","Храм Светих апостола Петра и Павла (1965)":"Church of the Holy Apostles Peter and Paul (1965)","Храм Светих апостола Петра и Павла - Биоска":"Church of the Holy Apostles Peter and Paul - Bioska","Храм Светих апостола Петра и Павла - Богутовачка Бања":"Church of the Holy Apostles Peter and Paul - Bogutovačka Spa","Храм Светих апостола Петра и Павла - Витковац":"Church of the Holy Apostles Peter and Paul - Vitkovac","Храм Светих апостола Петра и Павла - Жаочани":"Church of the Holy Apostles Peter and Paul - Zaočani","Храм Светих апостола Петра и Павла - Лиса":"Church of the Holy Apostles Peter and Paul - Lisa","Храм Светих апостола Петра и Павла - Мрсаћ":"Church of the Holy Apostles Peter and Paul - Mrsać","Храм Светих апостола Петра и Павла - Пашина Раван":"Church of the Holy Apostles Peter and Paul - Pašina Ravan","Храм Светих апостола Петра и Павла - Ржана":"Church of the Holy Apostles Peter and Paul - Ržana","Храм Светих апостола Петра и Павла - Сирогојно":"Church of the Holy Apostles Peter and Paul - Sirogojno","Храм Светих апостола Петра и Павла у Јошју":"Church of the Holy Apostles Peter and Paul in Jošje","Храм Светих апостола Петра и Павла у Ћуштици":"Church of the Holy Apostles Peter and Paul in Ćuštica","Храм Светих апостола Петра и Павла у Бојнеговцу":"Church of the Holy Apostles Peter and Paul in Bojnegovac","Храм Светих апостола Петра и Павла у Буткову":"Church of the Holy Apostles Peter and Paul in Butkovo","Храм Светих апостола Петра и Павла у Великом Шиљеговцу":"Church of the Holy Apostles Peter and Paul in Veliki Šiljegovec","Храм Светих апостола Петра и Павла у Горњем Матејевцу":"Church of the Holy Apostles Peter and Paul in Gornji Matejevac","Храм Светих апостола Петра и Павла у Гојиновцу":"Church of the Holy Apostles Peter and Paul in Gojinovac","Храм Светих апостола Петра и Павла у Гулијану":"Church of the Holy Apostles Peter and Paul in Guljan","Храм Светих апостола Петра и Павла у Доњој Локошници":"Church of the Holy Apostles Peter and Paul in Donja Lokošnica","Храм Светих апостола Петра и Павла у Дудулајцу":"Church of the Holy Apostles Peter and Paul in Dudulajac","Храм Светих апостола Петра и Павла у Житорађи":"Church of the Holy Apostles Peter and Paul in Žitoraža","Храм Светих апостола Петра и Павла у Калудри":"Church of the Holy Apostles Peter and Paul in Kaludra","Храм Светих апостола Петра и Павла у Лукову":"Church of the Holy Apostles Peter and Paul in Lukovo","Храм Светих апостола Петра и Павла у Петровој Гори":"Church of the Holy Apostles Peter and Paul in Petrova Gora","Храм Светих апостола Петра и Павла у Раковом Долу":"Church of the Holy Apostles Peter and Paul in Rakovo Dol","Храм Светих апостола Петра и Павла у Црноклишту":"Church of the Holy Apostles Peter and Paul in Crnoklista","Храм Светих апостола Петра и Павла, Рутоши":"Church of the Holy Apostles Peter and Paul, Rutoši","Храм Светих апостола Петра и Павла, Сјеница":"Church of the Holy Apostles Peter and Paul, Sjenica","Храм Светих апостола Петра и Павла, Црквени Тоци":"Church of the Holy Apostles Peter and Paul, Crkveni Toci","Храм Светих архангела Михаила и Гаврила":"Church of the Holy Archangels Michael and Gabriel","Храм Светих архангела Михаила и Гаврила у Конџељу":"Church of the Holy Archangels Michael and Gabriel in Kondželj","Храм Светих архангела у Горњој Трнави":"Church of the Holy Archangels in Gornja Trnava","Храм Светих бесребреника Козме и Дамјана у Будожељи":"The Church of Saints Cosma and Damian in Budoželja","Храм Светих бесребреника и чудотвораца Козме и Дамјана":"Temple of Saints Besrebrenik and miracle workers Cosma and Damian","Храм Светих врача Козме и Дамјана - Вељовићи":"Church of the Holy Witches Cosma and Damjan - Veljovići","Храм Светих врачева Козме и Дамјана у Вини":"Temple of the Holy Witches Cosma and Damian in Vina","Храм Светих врачева Козме и Дамјана у Микуљану":"Church of the Holy Witches Cosma and Damian in Mikuljan","Храм Светих врачева Козме и Дамјана у Шишинцу":"Church of the Holy Witches Cosma and Damian in Šišinac","Храм Светих врачева Козме и Дамјана у насељу ''Никола Тесла''":"Temple of the Holy Witches Cosma and Damian in the settlement \"Nikola Tesla\"","Храм Светих дванаест апостола, Буђево":"Church of the Holy Twelve Apostles, Budjevo","Храм Светих лекара Козме и Дамјана у Горњем Кординцу":"Church of the Holy Doctors Cosma and Damjan in Gornji Kordinac","Храм Светих лекара Козме и Дамјана у Расници":"Church of the Holy Doctors Cosma and Damian in Rasnica","Храм Светих лекара Козме и Дамјана у комплексу Прокупачке болнице":"Temple of the Holy Doctors Cosma and Damian in the complex of the Prokupac hospital","Храм Светих сирмијских мученика (Мала Босна)":"Church of the Holy Martyrs of Sirmi (Mala Bosna)","Храм Светих цара Константина и царице Јелене у Црвеној Јабуци":"Church of the Holy Emperors Constantine and Empress Jelena in Crvena Jabuka","Храм Светих царева Константина и царице Јелене у Манојлици":"Temple of the Holy Emperors Constantine and Empress Jelena in Manojlica","Храм Светих царева Константина и царице Јелене у Сврљигу":"Church of the Holy Emperors Constantine and Empress Jelena in Svrljig","Храм Светог Јоакима и Ане":"Church of St. Joachim and Anna","Храм Светог Јована Богослова":"Church of Saint John the Theologian","Храм Светог Јована Богослова на Новом гробљу":"Church of Saint John the Theologian at the New Cemetery","Храм Светог Јована Крститеља - Вукушица":"Church of St. John the Baptist - Vukušica","Храм Светог Јована Крститеља - Мокра Гора":"Church of St. John the Baptist - Mokra Gora","Храм Светог Јована Крститеља у Врелу":"Church of St. John the Baptist in Vrel","Храм Светог Јована Крститеља у Горњем Сухотну":"Church of St. John the Baptist in Gornji Suhotno","Храм Светог Јована Крститеља у Гостуши":"Church of St. John the Baptist in Gostusa","Храм Светог Јована Крститеља у Гргуру":"Church of St. John the Baptist in Grgur","Храм Светог Јована Крститеља у Доњем Крупцу":"Church of St. John the Baptist in Donji Krupac","Храм Светог Јована Крститеља у Крављу":"Church of St. John the Baptist in Kravlje","Храм Светог Јована Крститеља у Крајковцу":"Church of St. John the Baptist in Krajkovac","Храм Светог Јована Крститеља у Меровцу":"Church of St. John the Baptist in Merovac","Храм Светог Јована Крститеља у Мирановачкој Кули":"Church of St. John the Baptist in Miranovačka Kula","Храм Светог Јована Крститеља у Палиграцу":"Church of St. John the Baptist in Paligrac","Храм Светог Јована Крститеља у Петерлашу":"Church of St. John the Baptist in Peterlash","Храм Светог Јована Крститеља у Породину":"Church of St. John the Baptist in Porodina","Храм Светог Јована Крститеља у Станичењу":"Church of St. John the Baptist in Stanicenje","Храм Светог Јована Крститеља у Црној Бари":"Church of Saint John the Baptist in Crna Bara","Храм Светог Јована Крститеља, Вилови":"Church of St. John the Baptist, Vilovi","Храм Светог Јована у Височким Одоровцима":"Church of St. John in Visočki Odorovci","Храм Светог Алексија Човека Божијег у Чунгули":"Church of St. Alexius the Man of God in Chungula","Храм Светог Алимпија Столпника у Зубовцу":"The Church of St. Olimpius Stolpnik in Zubovac","Храм Светог Антонија Великог у Гревцима":"Church of Saint Anthony the Great in Grevci","Храм Светог Апостола Павла":"Church of Saint Paul the Apostle","Храм Светог Архангела Гаврила":"Church of St. Archangel Gabriel","Храм Светог Архангела Гаврила у Лесковику":"Church of St. Archangel Gabriel in Leskovik","Храм Светог Архангела Гаврила у Првој Кутини":"Church of St. Archangel Gabriel in Prva Kutina","Храм Светог Архангела Гаврила у Црном Врху":"Church of St. Archangel Gabriel in Crni Vrh","Храм Светог Архангела Михаила, Поблаће, Прибој":"Church of Saint Archangel Michael, Poblaće, Priboj","Храм Светог Атанасија Великог у Малом Шиљеговцу":"Church of Saint Athanasius the Great in Mali Šiljegovec","Храм Светог Ахилија, задужбина Светог Теоктиста Монаха (краља Драгутина)":"Temple of Saint Achille, endowment of Saint Theoctistus the Monk (King Dragutin)","Храм Светог Василија Острошког":"Church of Saint Vasilij Ostroski","Храм Светог Василија Острошког - Прељина":"Church of Saint Vasilij Ostroški - Preljina","Храм Светог Василија Острошког - Рибашевина":"Church of St. Basil Ostroski - Ribasevina","Храм Светог Василија Острошког у Влахову":"Church of Saint Vasilij Ostroski in Vlahov","Храм Светог Василија Острошког у Растелици":"Church of Saint Vasilij Ostroski in Rastelica","Храм Светог Василија Острошког чудотворца":"Church of St. Basil the Wonderworker of Ostrog","Храм Светог Великомученика Георгија":"Church of St. Great Martyr George","Храм Светог Великомученика Георгија у Протопопинцима":"Church of St. Great Martyr George in Protopopinci","Храм Светог Великомученика Прокопија у Катуну":"Temple of the Holy Great Martyr Procopius in Katun","Храм Светог Георгија":"Church of St. George","Храм Светог Георгија у Рожини":"Church of St. George in Rožina","Храм Светог Димитрија у Бребевници":"Church of St. Demetrius in Brebevnica","Храм Светог Игнатија Богоносца у Великом Суводолу":"Church of St. Ignatius the God-bearer in Veliki Suvodol","Храм Светог Илије у Гајтану":"Church of St. Elijah in Gaitan","Храм Светог Илије у Клисури":"Church of Saint Ilia in Klisura","Храм Светог Илије у Куманици":"Church of St. Elijah in Kumanica","Храм Светог Илије у Црном Врху":"Church of St. Elijah in Crni Vrh","Храм Светог Киријака Отшелника - Никојевићи":"Church of St. Kiriak the Outcast - Nikojevići","Храм Светог Методија Патарског - Велереч":"Church of St. Methodius of Patara - Velereč","Храм Светог Николаја - Свете Петке у Станичењу":"Church of St. Nicholas - St. Petka in Stanicenje","Храм Светог Николаја Жичког - Гостиница":"Church of St. Nicholas of Žički - Hotel","Храм Светог Николаја Жичког - Трешњевица":"Church of Saint Nicholas Žički - Trešnjevica","Храм Светог Николаја Мириликијског у Тогочевцу":"The Church of St. Nicholas of Myriliki in Togočevac","Храм Светог Николаја Мирликијског":"Church of St. Nicholas of Myrliki","Храм Светог Николаја Мирликијског - Беоце":"Church of St. Nicholas of Mirlikia - Beoce","Храм Светог Николаја Мирликијског - Брезова":"Church of St. Nicholas of Mirlikia - Brezova","Храм Светог Николаја Мирликијског - Гвоздац":"Church of St. Nicholas of Mirlikiski - Gvozdac","Храм Светог Николаја Мирликијског - Ивановци":"Church of St. Nicholas of Mirlikii - Ivanovci","Храм Светог Николаја Мирликијског - Палеж":"Church of St. Nicholas of Mirlikii - Palež","Храм Светог Николаја Мирликијског - Шилопај":"Church of St. Nicholas of Mirlikii - Silopaj","Храм Светог Николаја Мирликијског - Шумник":"Church of St. Nicholas of Mirlikia - Šumnik","Храм Светог Николаја Мирликијског у Белој":"Church of St. Nicholas of Mirliki in Bela","Храм Светог Николаја Српског, Коловрат":"Church of Saint Nicholas of Serbia, Kolovrat","Храм Светог Николаја мирликијског, Манастир Бања, Прибојска Бања":"Church of St. Nicholas of Mirlikia, Banja Monastery, Pribojska Banja","Храм Светог Николаја у Јарсенову":"Church of Saint Nicholas in Jarsenovo","Храм Светог Николаја у Биљегу":"Church of Saint Nicholas in Biljeg","Храм Светог Николаја у Великом Боњинцу":"Church of Saint Nicholas in Veliki Bonjinac","Храм Светог Николаја у Вукањи":"Saint Nicholas Church in Vukanja","Храм Светог Николаја у Горњем Стрижевцу":"Saint Nicholas Church in Gornji Striževac","Храм Светог Николаја у Доњем Стопању":"Church of Saint Nicholas in Donji Stopanje","Храм Светог Николаја у Драјинцу":"Church of St. Nicholas in Drajinac","Храм Светог Николаја у Козару":"Church of St. Nicholas in Kozar","Храм Светог Николаја у Космачу":"Church of Saint Nicholas in Kosmač","Храм Светог Николаја у Лалинцу":"Church of Saint Nicholas in Lalinac","Храм Светог Николаја у Липовици":"Church of Saint Nicholas in Lipovica","Храм Светог Николаја у Мердару":"Church of Saint Nicholas in Merdar","Храм Светог Николаја у Пуковцу":"Church of St. Nicholas in Pukovac","Храм Светог Николаја у Речици":"Church of St. Nicholas in Rečica","Храм Светог Николе - Бреково":"Church of Saint Nicholas - Brekovo","Храм Светог Николе у Миљковцу":"Church of Saint Nicholas in Miljkovac","Храм Светог Николе у Равној Бањи":"Church of Saint Nicholas in Ravna Banja","Храм Светог Пантелејмона у Ћуковцу":"Church of Saint Panteleimon in Ćukovac","Храм Светог Пантелејмона у Сенокосу":"Church of Saint Panteleimon in Senokos","Храм Светог Петра Дабробосанског, Саставци, Прибој":"Church of St. Peter Dabrobosanski, Sastavci, Priboj","Храм Светог Пророка Илије":"Temple of the Holy Prophet Elijah","Храм Светог Пророка Илије у Тешици":"Church of the Holy Prophet Elijah in Tešica","Храм Светог Романа Ђунишког у Сечаници":"Church of St. Roman Đuniški in Sečanica","Храм Светог Саве":"Church of Saint Sava","Храм Светог Саве Српског":"Church of Saint Sava of Serbia","Храм Светог Саве Српског - Вранеши":"Church of Saint Sava of Serbia - Vraneši","Храм Светог Саве Српског - Миланџа":"Church of Saint Sava of Serbia - Milandža","Храм Светог Саве у Великом Јовановцу":"Church of St. Sava in Veliki Jovanovac","Храм Светог Саве у Горњем Бријању":"Church of St. Sava in Gornji Brijan","Храм Светог Саве, Аљиновићи":"Church of St. Sava, Aljinovići","Храм Светог Саве, Сопотница":"Church of Saint Sava, Sopotnica","Храм Светог Саве, првог архиепископа српског у Комрену":"Church of Saint Sava, the first Serbian archbishop in Komren","Храм Светог Симеона Мироточивог у Доњем Црнатову":"The Church of Saint Simeon Myrotočivo in Donji Crnatovo","Храм Светог Симеона Мироточивог у Лесковцу":"The Church of Saint Simeon Myrotočivo in Leskovac","Храм Светог Симеона Столпника у Гагинцу":"The Church of Saint Simeon Stolpnik in Gaginac","Храм Светог Симеона Столпника у Плавцу":"The Church of Saint Simeon Stolpnik in Plavac","Храм Светог Спиридона у Граници":"Church of Saint Spyridon in Granica","Храм Светог апостола Марка у Белоињу":"Church of the Holy Apostle Mark in Beloinje","Храм Светог апостола Марка у Бољевцу":"Church of the Holy Apostle Mark in Boljevac","Храм Светог апостола Матеја":"Church of Saint Matthew the Apostle","Храм Светог апостола Павла":"Church of Saint Paul the Apostle","Храм Светог апостола и јеванђелиста Луке":"Church of the Holy Apostle and Evangelist Luke","Храм Светог апостола и јеванђелиста Марка у Водицaма":"Church of the Holy Apostle and Evangelist Mark in Vodice","Храм Светог апостола и јеванђелисте Луке":"Church of the Holy Apostle and Evangelist Luke","Храм Светог апостола и јеванђелисте Луке - Девићи":"Church of the Holy Apostle and Evangelist Luke - Devići","Храм Светог апостола и јеванђелисте Луке у Сагоњеву":"Church of the Holy Apostle and Evangelist Luke in Sagonjevo","Храм Светог апостола и јеванђелисте Марка":"Church of the Holy Apostle and Evangelist Mark","Храм Светог апостола и јеванђелисте Марка - Бељак":"Church of the Holy Apostle and Evangelist Mark - Beljak","Храм Светог апостола и јеванђелисте Марка - Поцесје":"Church of the Holy Apostle and Evangelist Mark - Pocesje","Храм Светог архангела Гаврила":"Church of the Holy Archangel Gabriel","Храм Светог архангела Гаврила (1874. г.)":"Church of the Holy Archangel Gabriel (1874)","Храм Светог архангела Гаврила - Доња Врбава":"Church of the Holy Archangel Gabriel - Donja Vrbava","Храм Светог архангела Гаврила - Осоница":"Church of the Holy Archangel Gabriel - Osonica","Храм Светог архангела Гаврила - Рашка":"Church of the Holy Archangel Gabriel - Raška","Храм Светог архангела Гаврила у Бовну":"Church of the Holy Archangel Gabriel in Bovno","Храм Светог архангела Гаврила у Великом Шиљеговцу":"Church of the Holy Archangel Gabriel in Veliki Šiljegovec","Храм Светог архангела Гаврила у Врбовцу":"Church of the Holy Archangel Gabriel in Vrbovac","Храм Светог архангела Гаврила у Градашници":"Church of the Holy Archangel Gabriel in Gradašnica","Храм Светог архангела Гаврила у Дешилову":"Church of the Holy Archangel Gabriel in Dešilovo","Храм Светог архангела Гаврила у Дукату":"Church of the Holy Archangel Gabriel in Dukat","Храм Светог архангела Гаврила у Житковцу":"Church of the Holy Archangel Gabriel in Žitkovac","Храм Светог архангела Гаврила у Крушевици":"Church of the Holy Archangel Gabriel in Kruševica","Храм Светог архангела Гаврила у Маћедонцу":"Church of the Holy Archangel Gabriel in Macedonac","Храм Светог архангела Гаврила у Моклишту":"Church of the Holy Archangel Gabriel in Moklishta","Храм Светог архангела Гаврила у Накривњу":"Church of the Holy Archangel Gabriel in Nakrivnje","Храм Светог архангела Гаврила у Придворици":"Church of the Holy Archangel Gabriel in Pridvorica","Храм Светог архангела Гаврила у Рашчићима":"Church of the Holy Archangel Gabriel in Raščići","Храм Светог архангела Гаврила у Црњеву":"Church of the Holy Archangel Gabriel in Crnjevo","Храм Светог архангела Гаврила, Манастир Моравци":"Church of the Holy Archangel Gabriel, Moravci Monastery","Храм Светог архангела Михаила - Јелен До":"Church of Saint Michael the Archangel - Jelen Do","Храм Светог архангела Михаила - Прилике":"Church of Saint Michael the Archangel - Opportunities","Храм Светог архангела Михаила у Џигољу":"Church of Saint Michael the Archangel in Jigolje","Храм Светог архангела Михаила у Богујевцу":"Church of the Holy Archangel Michael in Bogujevac","Храм Светог архангела Михаила у Бољевом Долу":"Church of Saint Michael the Archangel in Boljevo Dol","Храм Светог архангела Михаила у Доњем Матејевцу":"Church of the Holy Archangel Michael in Donji Matejevac","Храм Светог архангела Михаила у Лужанима":"Church of Saint Michael the Archangel in Luzani","Храм Светог архангела Михаила у Пољској Ржани":"Church of Saint Michael the Archangel in Ržana, Poland","Храм Светог архангела Михаила у Чиниглавцима":"Church of Saint Michael the Archangel in Činiglavci","Храм Светог архистратига Гаврила у Предејану":"The Church of St. Archangel Gavril in Predejan","Храм Светог архистратига Гаврила у Рупљу":"The Church of Saint Gavril the Archangel in Ruplje","Храм Светог архиђакона Стефана":"Church of Saint Archdeacon Stephen","Храм Светог архиђакона Стефана у Влахињи":"Church of Saint Archdeacon Stefan in Vlahinja","Храм Светог архиђакона Стефана у Каменици":"Church of Saint Archdeacon Stefan in Kamenica","Храм Светог архиђакона Стефана, Џурово Брдо":"Church of Saint Archdeacon Stefan, Djurovo Brdo","Храм Светог великомученика Георгија":"Church of the Holy Great Martyr George","Храм Светог великомученика Георгија - Врх":"Church of the Holy Great Martyr Georgi - Vrh","Храм Светог великомученика Георгија - Доње Радаљево":"Church of the Holy Great Martyr George - Donje Radaljevo","Храм Светог великомученика Георгија - Кремна":"Church of the Holy Great Martyr Georgi - Kremna","Храм Светог великомученика Георгија - Радаљево":"Church of the Holy Great Martyr Georgi - Radaljevo","Храм Светог великомученика Георгија у Белом Потоку":"Church of the Holy Great Martyr Georgi in Beli Potok","Храм Светог великомученика Георгија у Бунуши":"Church of the Holy Great Martyr George in Bunuša","Храм Светог великомученика Георгија у Вранићима":"Church of the Holy Great Martyr Georgi in Vranići","Храм Светог великомученика Георгија у Вртовцима":"Church of the Holy Great Martyr George in Vrtovci","Храм Светог великомученика Георгија у Глијечи":"Church of the Holy Great Martyr George in Gliječa","Храм Светог великомученика Георгија у Горњем Брестовцу":"Church of the Holy Great Martyr Georgi in Gornji Brestovac","Храм Светог великомученика Георгија у Жељуши":"Church of the Holy Great Martyr George in Željuša","Храм Светог великомученика Георгија у Каменици":"Church of the Holy Great Martyr George in Kamenica","Храм Светог великомученика Георгија у Луковској Бањи":"Church of the Holy Great Martyr George in Lukovska Banja","Храм Светог великомученика Георгија у Мазгошу":"Church of the Holy Great Martyr George in Mazgoš","Храм Светог великомученика Георгија у Моравцу":"Church of the Holy Great Martyr George in Moravac","Храм Светог великомученика Георгија у Осмакову":"Church of the Holy Great Martyr George in Osmakovo","Храм Светог великомученика Георгија у Присјану":"Church of the Holy Great Martyr George in Prisjan","Храм Светог великомученика Георгија у Радејни":"Church of the Holy Great Martyr George in Radejna","Храм Светог великомученика Георгија у Селови":"Church of the Holy Great Martyr Georgi in Selova","Храм Светог великомученика Георгија, Лопиже":"Church of the Holy Great Martyr Georgi, Lopiže","Храм Светог великомученика Георгија, при Манастиру Враћевшници":"Church of the Holy Great Martyr George, near the Vraćevšnica Monastery","Храм Светог великомученика Димитрија - Брезна":"Church of the Holy Great Martyr Dimitrija - Brezna","Храм Светог великомученика Димитрија - Оклетац":"Church of the Holy Great Martyr Dimitrija - Okletac","Храм Светог великомученика Димитрија у Добровишу":"Church of the Holy Great Martyr Dimitrije in Dobroviš","Храм Светог великомученика Димитрија у Пасјачи":"Church of the Holy Great Martyr Dimitrije in Pasjača","Храм Светог великомученика Кнеза Лазара":"Church of the Holy Great Martyr Knez Lazar","Храм Светог великомученика Пантелејмона":"Temple of the Holy Great Martyr Panteleimon","Храм Светог великомученика Пантелејмона (Бумбарево Брдо)":"Temple of the Holy Great Martyr Panteleimon (Bumbarevo Brdo)","Храм Светог великомученика Пантелејмона - Доња Црвица":"Church of the Holy Great Martyr Panteleimon - Donja Crvica","Храм Светог великомученика Пантелејмона - Самаила":"Temple of the Holy Great Martyr Panteleimon - Samail","Храм Светог великомученика Пантелејмона у Ђунису":"Church of the Holy Great Martyr Panteleimon in Djunis","Храм Светог великомученика Пантелејмона у Азбресници":"Church of the Holy Great Martyr Panteleimon in Azbresnica","Храм Светог великомученика Пантелејмона у Враништу":"Temple of the Holy Great Martyr Panteleimon in Vranište","Храм Светог великомученика Пантелејмона у Вукањи":"Temple of the Holy Great Martyr Panteleimon in Vukanja","Храм Светог великомученика Пантелејмона у Газдарама":"Church of the Holy Great Martyr Panteleimon in Gazdare","Храм Светог великомученика Пантелејмона у Кални":"Temple of the Holy Great Martyr Panteleimon in Kalna","Храм Светог великомученика Пантелејмона у Рафуни":"Church of the Holy Great Martyr Panteleimon in Rafuna","Храм Светог великомученика Пантелејмона у Селишту":"Church of the Holy Great Martyr Panteleimon in Seliste","Храм Светог великомученика Пантелејмона, Пожегрмац, Прибој":"Church of the Holy Great Martyr Panteleimon, Požegrmac, Priboj","Храм Светог великомученика Прокопија":"Temple of the Holy Great Martyr Procopius","Храм Светог великомученика Прокопија у Комадинама":"Temple of the Holy Great Martyr Procopius in Komadine","Храм Светог великомученика Прокопија у Прокупљу":"Temple of the Holy Great Martyr Procopius in Prokuplje","Храм Светог великомученика Прокопија у Радевцу":"Temple of the Holy Great Martyr Procopius in Radevac","Храм Светог великомученика Прокопија у Чукуровцу":"Church of the Holy Great Martyr Procopius in Čukurovac","Храм Светог великомученика Прокопија у Шуману":"Temple of the Holy Great Martyr Procopius in Shuman","Храм Светог великомученика Прокопија, Велика Жупа":"Church of the Holy Great Martyr Procopius, Velika Zupa","Храм Светог великомученика Прокопија, Кратово, Прибој":"Church of the Holy Great Martyr Procopius, Kratovo, Priboj","Храм Светог великомученика Теодора Тирона":"Temple of the Holy Great Martyr Theodore Tiron","Храм Светог великомученика Теодора Тирона у Азбресници":"Church of the Holy Great Martyr Theodore Tiron in Azbresnica","Храм Светог великомученика Харалампија у Костуру":"Church of the Holy Great Martyr Haralampi in Kostur","Храм Светог великомученика кнеза Лазара":"Church of the Holy Great Martyr Prince Lazar","Храм Светог великомученика кнеза Лазара на Љубићу ул. Драгослава Бојића бб":"Church of the Holy Great Martyr Prince Lazar on Ljubić ul. Dragoslava Bojića bb","Храм Светог великомученика кнеза Лазара у Бединој Вароши":"Church of the Holy Great Martyr Prince Lazar in Bedina Varosha","Храм Светог великомученика кнеза Лазара, Бродарево":"Church of the Holy Great Martyr Prince Lazar, Brodarevo","Храм Светог великомученика кнеза Лазара, Стари Прибој":"Church of the Holy Great Martyr Prince Lazar, Stari Priboj","Храм Светог великомученика кнеза Лазара, Сјеничке Баре":"Church of the Holy Great Martyr Prince Lazar, Sjenička Bara","Храм Светог исповедника Варнаве Беочинског":"Church of the Holy Confessor Barnabas Beočinski","Храм Светог кнеза Лазара у Лозанама":"Church of Saint Prince Lazarus in Lausanne","Храм Светог мученика Мине у Каонику":"Church of the Holy Martyr Mina in Kaonik","Храм Светог мученика Мине у Штави":"Church of the Holy Martyr Mina in Stava","Храм Светог оца Николаја":"Church of the Holy Father Nicholas","Храм Светог оца Николаја у Ораовици":"Church of Saint Father Nicholas in Oraovica","Храм Светог оца Николаја у Хуму":"Church of Saint Nicholas in Hum","Храм Светог оца Николаја у Чукљенику":"Church of Saint Father Nicholas in Čukljenik","Храм Светог првомученика и архиђакона Стефана":"Church of the Holy First Martyr and Archdeacon Stefan","Храм Светог првомученика и архиђакона Стефана у Глашинцу":"Church of the Holy First Martyr and Archdeacon Stefan in Glašinac","Храм Светог пророка Јеремије у Сибници":"Church of the Holy Prophet Jeremiah in Sibnica","Храм Светог пророка Илије":"Temple of the Holy Prophet Ilia","Храм Светог пророка Илије - Бајина Башта":"Church of the Holy Prophet Elijah - Bajina Bašta","Храм Светог пророка Илије - Боровић":"Church of the Holy Prophet Elijah - Borović","Храм Светог пророка Илије - Вича":"Church of the Holy Prophet Elijah - Viča","Храм Светог пророка Илије - Доброселица":"Church of the Holy Prophet Elijah - Dobroselica","Храм Светог пророка Илије - Доња Трепча":"Church of the Holy Prophet Elijah - Donja Trepča","Храм Светог пророка Илије - Каменица":"Church of the Holy Prophet Elijah - Kamenica","Храм Светог пророка Илије - Мачкат":"Church of the Holy Prophet Elijah - Mačkat","Храм Светог пророка Илије - Одвраћеница":"Church of the Holy Prophet Ilia - Odvračenica","Храм Светог пророка Илије - Равањско Поље":"Church of the Holy Prophet Elijah - Ravanjsko Polje","Храм Светог пророка Илије - Рудно":"Church of the Holy Prophet Elijah - Rudno","Храм Светог пророка Илије и Светог Лазара у Грбавче":"Church of Saint Prophet Elijah and Saint Lazarus in Grbavce","Храм Светог пророка Илије у Јасеници":"Church of the Holy Prophet Elijah in Jasenica","Храм Светог пророка Илије у Љуберађи":"Church of the Holy Prophet Elijah in Ljuberadja","Храм Светог пророка Илије у Балиновцу":"Church of the Holy Prophet Elijah in Balinovac","Храм Светог пророка Илије у Горњој Драгуши":"Church of the Holy Prophet Elijah in Gornja Draguša","Храм Светог пророка Илије у Доњој Невљи":"Church of the Holy Prophet Elijah in Donja Nevlja","Храм Светог пророка Илије у Доњој Трнави":"Church of the Holy Prophet Elijah in Donja Trnava","Храм Светог пророка Илије у Дубову":"Church of the Holy Prophet Elijah in Dubov","Храм Светог пророка Илије у Кнез Селу":"Church of the Holy Prophet Elijah in Knez Selo","Храм Светог пророка Илије у Комрену":"Temple of the Holy Prophet Elijah in Komren","Храм Светог пророка Илије у Лесковцу":"Church of the Holy Prophet Elijah in Leskovac","Храм Светог пророка Илије у Нишевцу":"Church of the Holy Prophet Elijah in Niševac","Храм Светог пророка Илије у Печењевцу":"Church of the Holy Prophet Elijah in Pečenjevac","Храм Светог пророка Илије у Рибару":"Church of the Holy Prophet Elijah in Ribar","Храм Светог пророка Илије у Сијaринској бањи":"The Church of the Holy Prophet Elijah in Sijarinska banja","Храм Светог пророка Илије у Сопоту":"Church of the Holy Prophet Elijah in Sopot","Храм Светог пророка Илије у Срећковцима":"Church of the Holy Prophet Elijah in Srećkovci","Храм Светог пророка Илије у Црвенчеву":"Church of the Holy Prophet Elijah in Crvencevo","Храм Светог пророка Илије, Манастир Бања, Прибојска Бања":"Church of the Holy Prophet Elijah, Banja Monastery, Pribojska Banja","Храм Светог цара Конастантина и царице Јелене":"Church of Saint Emperor Constantine and Empress Jelena","Храм Светог цара Константина и царице Јелене":"Temple of Saint Emperor Constantine and Empress Jelena","Храм Светог цара Константина и царице Јелене - Горичани (1930)":"Church of Saint Emperor Constantine and Empress Jelena - Goričani (1930)","Храм Светог цара Константина и царице Јелене - Шарган":"Church of Saint Emperor Constantine and Empress Jelena - Šargan","Храм Светог цара Константина и царице Јелене у Барбатовцу":"Church of Saint Emperor Constantine and Empress Jelena in Barbatovac","Храм Светог цара Константина и царице Јелене у Плочнику":"Church of Saint Emperor Constantine and Empress Jelena in Pločnik","Храм Светог цара Константина и царице Јелене, Сељашница":"Temple of Saint Emperor Constantine and Empress Jelena, Seljašnica","Храм Светог цара Константина и царице Јелене, Херцеговачка Голеша, Прибој":"Church of Saint Emperor Constantine and Empress Jelena, Herzegovina Goleša, Priboj","Храм Светог четвородневног Лазара":"Church of Saint Lazarus of the four-day age","Храм Свих Светих, Житин - Боровице":"Church of All Saints, Žitin - Borovice","Храм Свих светих у Балти Бериловцу":"Church of All Saints in Balta Berilovac","Храм Силаска Светог Духа":"Temple of the Descent of the Holy Spirit","Храм Силаска Светог Духа на Апостоле - Душковци":"Temple of the Descent of the Holy Spirit on the Apostles - Duškovci","Храм Силаска Светог Духа на Апостоле у Власотинцу":"The Church of the Descent of the Holy Spirit on the Apostles in Vlasotinac","Храм Силаска Светог Духа на апостоле":"Temple of the Descent of the Holy Spirit on the Apostles","Храм Силаска Светог Духа на апостоле у Бабичком":"Church of the Descent of the Holy Spirit on the Apostles in Babicki","Храм Спаљивања моштију Светог Саве Српског":"Temple of the Burning of the Relics of Saint Sava of Serbia","Храм Сретења Господњег":"Church of the Meeting of the Lord","Храм Сретења Господњег - Соколићи":"Church of the Meeting of the Lord - Sokolići","Храм Српских мученика и новомученика, Љепојевићи - Јавор":"Church of Serbian Martyrs and New Martyrs, Ljepojevići - Javor","Храм Трећег обретења главе Светог Јована Крститеља, Џурово":"Church of the Third Conversion of the Head of St. John the Baptist, Djurovo","Храм Усековања главе Светог Јована Крститеља":"Church of the Beheading of St. John the Baptist","Храм Усековања главе Светог Јована Крститеља - Баљевац":"Church of the Beheading of St. John the Baptist - Baljevac","Храм Усековања главе Светог Јована Крститеља - Коритник":"Church of the Beheading of St. John the Baptist - Koritnik","Храм Усековања главе Светог Јована Крститеља у Каонику":"Church of the Beheading of Saint John the Baptist in Kaonik","Храм Усековања главе Светог Јована Крститеља у Лебану":"Church of the Beheading of Saint John the Baptist in Lebanon","Храм Успенија Пресвете Богородице":"Church of the Assumption of the Holy Mother of God","Храм Успенија Пресвете Богородице - Јабланица":"Church of the Assumption of the Blessed Virgin Mary - Jablanica","Храм Успења Пресвете Богородице":"Church of the Assumption of the Blessed Virgin Mary","Храм Успења Пресвете Богородице - Кушићи":"Church of the Assumption of the Blessed Virgin Mary - Kušići","Храм Успења Пресвете Богородице Доњој Врежини":"Church of the Assumption of the Blessed Virgin Mary in Donja Vrežina","Храм Успења Пресвете Богородице у Балајинцу":"Church of the Assumption of the Blessed Virgin Mary in Balajinac","Храм Успења Пресвете Богородице у Блацу":"Church of the Assumption of the Blessed Virgin Mary in Blac","Храм Успења Пресвете Богородице у Борову":"Church of the Assumption of the Blessed Virgin Mary in Borovo","Храм Успења Пресвете Богородице у Брестовцу":"Church of the Assumption of the Blessed Virgin Mary in Brestovac","Храм Успења Пресвете Богородице у Великом Селу":"Church of the Assumption of the Blessed Virgin Mary in Veliko Selo","Храм Успења Пресвете Богородице у Гргуровцу":"Church of the Assumption of the Blessed Virgin Mary in Grgurovac","Храм Успења Пресвете Богородице у Гркињи":"Church of the Assumption of the Blessed Virgin Mary in Grkinka","Храм Успења Пресвете Богородице у Доњем Међурову":"Church of the Assumption of the Blessed Virgin Mary in Donji Međurovo","Храм Успења Пресвете Богородице у Доњем Стопању":"The Church of the Assumption of the Blessed Virgin Mary in Donji Stopanje","Храм Успења Пресвете Богородице у Житорађи":"Church of the Assumption of the Blessed Virgin Mary in Žitoraža","Храм Успења Пресвете Богородице у Кнез Селу":"Church of the Assumption of the Blessed Virgin Mary in Knez Selo","Храм Успења Пресвете Богородице у Конопници":"Church of the Assumption of the Blessed Virgin Mary in Konopnica","Храм Успења Пресвете Богородице у Крајковцу":"Church of the Assumption of the Blessed Virgin Mary in Krajkovac","Храм Успења Пресвете Богородице у Миљковцу":"Church of the Assumption of the Blessed Virgin Mary in Miljkovac","Храм Успења Пресвете Богородице у Оргулици":"Church of the Assumption of the Blessed Virgin Mary in Orgulica","Храм Успења Пресвете Богородице у Стрелцу":"Church of the Assumption of the Blessed Virgin Mary in Strelac","Храм Успења Пресвете Богородице у Тешици":"Church of the Assumption of the Blessed Virgin Mary in Tešica","Храм Успења Пресвете Богородице у Црнољевици":"Church of the Assumption of the Blessed Virgin Mary in Crnoljevica","Храм Успења Пресвете Богородице у селу Ђукекаре":"The Church of the Assumption of the Blessed Virgin Mary in the village of Đukekare","Храм Успења Пресвете Богородице, Ивање":"Church of the Assumption of the Blessed Virgin Mary, Ivanje","Храм Успења Пресвете Богородице, при Манастиру Студеници":"The Church of the Assumption of the Blessed Virgin Mary, near the Studenica Monastery","Храм Успења Свете Ане - Брусник":"Church of the Assumption of Saint Anne - Brusnik","Храм Чудо Светог Архангела Михаила":"Temple of the Miracle of Saint Michael the Archangel","Храм посвећен Преподобном Сисоју Великом":"The temple dedicated to Venerable Sisoy the Great","Храм преноса моштију светог оца Николаја":"The Church of the Transfer of the Relics of Saint Nicholas","Храм преподобне Параскеве у Горњем Међурову":"Church of the Venerable Paraskeva in Gornji Međurovo","Храм преподобног Симеона Столпника у Славујевцу":"The temple of Venerable Simeon Stolpnik in Slavujevac","Храм света Три Јерарха у Брзом броду":"The Holy Temple of the Three Hierarchs in the Fast Ship","Храм свете Петке у Мариној Кутини":"Church of Saint Petka in Marina Kutina","Храм свете Петке у Орљи":"Church of Saint Petka in Orlja","Храм свете Петке у Церју":"Church of Saint Petka in Cerje","Храм свете великомученице Марине у селу ЈуговацХрам Свете великомученице Марине у Југовцу":"The Temple of the Holy Great Martyr Marina in the village of JugovacThe Temple of the Holy Great Martyr Marina in Jugovac","Храм свете великомученице Недеље у Пасипољани":"Temple of the Holy Great Martyr Nedelja in Pasipoljana","Храм свете преподобне Параскеве у Орљану":"The temple of Saint Paraskeva in Orljan","Храм свете преподобномученице Параскеве у Ћурлини":"The Church of the Holy Reverend Martyr Paraskeva in Ćurlina","Храм светих Апостола Петра и Павла у селу БулатовацХрам Светих апостола Петра и Павла у Булатовцу":"Church of the Holy Apostles Peter and Paul in the village of BulatovacChurch of the Holy Apostles Peter and Paul in Bulatovac","Храм светих Архангела Михаила и Гаврила на Алексиначком гробљу":"Church of Saint Archangels Michael and Gabriel at the Aleksinac Cemetery","Храм светих апостола Петра и Павла у Јелашници":"Church of the Holy Apostles Peter and Paul in Jelašnica","Храм светих апостола Петра и Павла у Вртишту":"Church of the Holy Apostles Peter and Paul in Vrtište","Храм светог Јована Богослова у Мојинцима":"Church of St. John the Baptist in Mojinci","Храм светог Јована Крститеља у Алексиначком Бујмиру":"Church of St. John the Baptist in Aleksinack Bujmir","Храм светог Архангела Гаврила у Кочану":"Church of St. Archangel Gabriel in Kočan","Храм светог Лазара Четвородневног у Доњем Власу":"Church of St. Lazar the Four-Day in Donji Vlas","Храм светог Николаја Мириликијског у селу Доња Студена":"Church of St. Nicholas of Myriliki in the village of Donja Studena","Храм светог Николаја Мириликијског у селу Манастир":"Church of St. Nicholas of Myriliki in the village of Manastir","Храм светог Николаја у Доњем Драговљу":"Church of St. Nicholas in Donji Dragovlje","Храм светог Николаја у Каменици":"Church of Saint Nicholas in Kamenica","Храм светог Пророка Илије у Суботинцу":"Church of the Holy Prophet Elijah in Subotinac","Храм светог Романа Ђунишког у Белотинцу":"Church of St. Roman Đuniški in Belotinac","Храм светог Романа Ђунишког у Паљини":"The Church of St. Roman Đuniški in Paljina","Храм светог великомученика Георгија у Горњем Барбешу":"Church of the Holy Great Martyr George in Gornji Barbes","Храм светог великомученика Димитрија у Бербатову":"The Church of the Holy Great Martyr Demetrius in Berbatovo","Храм светог великомученика и исцелитеља Пантелејмона у Нишу":"The temple of the holy great martyr and healer Panteleimon in Niš","Храм светог краља Стефана Дечанског у комплексу нишког Казнено- поправног завода":"The temple of the holy King Stefan Dečanski in the complex of the Niš Penitentiary","Храм светог пророка Илије у Вукманову":"Church of the Holy Prophet Elijah in Vukmanovo","Храм светог пророка Илије у Нишкој Бањи":"Temple of the Holy Prophet Elijah in Niška Banja","Храм светог пророка Илије у Чокоту":"Temple of the Holy Prophet Elijah in Chokot","Храм-брвнара Светог кнеза Лазара у Пролому":"Log cabin temple of Saint Prince Lazar in Prolom","Црква Светог апостола Вартоломеја у Каонику":"Church of the Holy Apostle Bartholomew in Kaonik","Црква брвнара у Такову (18 в.)":"Log cabin church in Takovo (18th century)","капела Свете Тројице у Рудару":"Chapel of the Holy Trinity in Rudar","храм Вазнесења Господњег - Расна":"temple of the Ascension of the Lord - Rasna","храм Сабора Светих апостола - Штавица":"Church of the Assembly of the Holy Apostles - Štavica","храм Сабора Српских Светитеља - Миљаковина":"the church of the Assembly of Serbian Saints - Miljakovina","храм Света Три Јерарха са параклисима Светог кнеза Лазара и Свете Петке":"the temple of the Holy Three Hierarchs with the chapels of Saint Prince Lazarus and Saint Petka","храм Свете Тројице у Куршумлији":"Holy Trinity Church in Kuršumlija","храм Светог Саве - Савинац Висибаба":"Saint Sava temple - Savinac Visibaba","храм Светог апостола Луке":"Church of Saint Luke the Apostle","храм Светог пророка Илије":"the temple of the Holy Prophet Elijah","храм Светог пророка Илије у Рачи":"the temple of the Holy Prophet Elijah in Rača","храм Силаска Светог Духа на Апостоле у Нишу":"the temple of the Descent of the Holy Spirit on the Apostles in Niš","храм Успења Пресвете Богородице у Пироту":"Church of the Assumption of the Blessed Virgin Mary in Pirot","храм светог архангела Гаврила - Радановци":"Church of the Holy Archangel Gabriel - Radanovci"}''')


EXACT_ENGLISH_LABELS = {
    "Манастир Манастирица": "Manastirica",
    "Манастир у Каћу": "Kać",
    "Манастир Св. Николе - Куршумлија": "Saint Nicholas - Kuršumlija",
    "Манастир Св. Онуфрија": "Saint Onuphrius",
    "Храм светог Јована Богослова у Мојинцима":
        "Saint John the Theologian in Mojinci",
    "Храм Вазнесења Господњег у Црквини":
        "the Ascension of the Lord in Crkvina",
    "Храм Свете Тројице Русалијске или \"Латинска црква\" у Горњем Матејевцу":
        "the Holy Trinity Rusalije Church, also known as the Latin Church, in Gornji Matejevac",
    "Храм Светих Константина и Јелене у Лозанцу":
        "Saints Constantine and Helen in Lozanac",
    "Храм Св. лекара и чудотвораца Козме и Дамјана":
        "Holy Unmercenaries and Wonderworkers Cosmas and Damian",
    "Манастир - Скит Светог великомученика Димитрија у Влајковцу":
        "Holy Great Martyr Demetrios in Vlajkovac",
    "Храм - капела Светог Нектарија Егинског":
        "Saint Nektarios of Aegina",
    "Храм Св. великомученика Георгија - Рудник":
        "Saint Great Martyr George - Rudnik",
    "храм Светог Саве - Савинац Висибаба":
        "Saint Sava - Savinac Visibaba",
    "Храм-брвнара Светог кнеза Лазара у Пролому":
        "Log Church of Saint Prince Lazarus in Prolom",
    "Храм Светог Јована Крститеља у Врелу":
        "Saint John the Baptist in Vrelo",
}

DEANERY_NAMES = {
    "Архијерејско намесништво бачкопаланачко": "Bačka Palanka",
    "Архијерејско намесништво бечејско": "Bečej",
    "Архијерејско намесништво жабаљско": "Žabalj",
    "Архијерејско намесништво кулско": "Kula",
    "Архијерејско намесништво новосадско прво": "First Novi Sad",
    "Архијерејско намесништво новосадско друго": "Second Novi Sad",
    "Архијерејско намесништво сомборско": "Sombor",
    "Архијерејско намесништво суботичко": "Subotica",
    "Архијерејско намесништво алексиначко": "Aleksinac",
    "Архијерејско намесништво белопаланачко": "Bela Palanka",
    "Архијерејско намесништво власотиначко": "Vlasotince",
    "Архијерејско намесништво јабланичко": "Jablanica",
    "Архијерејско намесништво косаничко": "Kosanica",
    "Архијерејско намесништво лесковачко": "Leskovac",
    "Прво нишко архијерејско намесништво": "First Niš",
    "Друго нишко архијерејско намесништво": "Second Niš",
    "Архијерејско намесништво пиротско": "Pirot",
    "Архијерејско намесништво топличко": "Toplica",
    "Архијерејско намесништво прибојско": "Priboj",
    "Архијерејско намесништво пријепољско": "Prijepolje",
    "Архијерејско намесништво нововарошко": "Nova Varoš",
    "Архијерејско намесништво призренско": "Prizren",
    "Архијерејско намесништво пећско": "Peć",
    "Архијерејско намесништво приштинско": "Priština",
    "Архијерејско намесништво гњиланско": "Gnjilane",
    "Архијерејско намесништво косовскомитровичко": "Kosovska Mitrovica",
    "Архијерејско намесништво новопазарско": "Novi Pazar",
    "Архијерејско намесништво земунско": "Zemun",
    "Архијерејско намесништво пећиначко": "Pećinci",
    "Архијерејско намесништво подунавско": "Podunavlje",
    "Архијерејско намесништво румско": "Ruma",
    "Архијерејско намесништво сремскокарловачко": "Sremski Karlovci",
    "Архијерејско намесништво сремскомитровачко": "Sremska Mitrovica",
    "Архијерејско намесништво старопазовачко": "Stara Pazova",
    "Архијерејско намесништво шидско": "Šid",
    "Архијерејско намесништво бољевачко": "Boljevac",
    "Архијерејско намесништво борско-поречко": "Bor-Poreč",
    "Архијерејско намесништво зајечарско": "Zaječar",
    "Архијерејско намесништво кључко": "Ključ",
    "Архијерејско намесништво књажевачко": "Knjaževac",
    "Архијерејско намесништво неготинско": "Negotin",
    "Архијерејско намесништво сокобањско": "Sokobanja",
    "Архијерејско намесништво гружанско": "Gruža (Borač)",
    "Архијерејско намесништво драгачевско": "Dragačevo (Guča)",
    "Архијерејско намесништво жичко": "Žiča (Kraljevo)",
    "Архијерејско намесништво качерско": "Kačer (Ljig)",
    "Архијерејско намесништво љубићко": "Ljubić (Preljina)",
    "Архијерејско намесништво моравичко": "Moravica (Ivanjica)",
    "Архијерејско намесништво пожешко-ариљско": "Požega-Arilje",
    "Архијерејско намесништво рачанско": "Rača (Bajina Bašta)",
    "Архијерејско намесништво студеничко": "Studenica (Raška)",
    "Архијерејско намесништво таковско": "Takovo (Gornji Milanovac)",
    "Архијерејско намесништво трнавско": "Trnava (Čačak)",
    "Архијерејско намесништво ужичко": "Užice",
    "Архијерејско намесништво црногорско": "Crna Gora (Kosjerić)",
}

CHURCH_COMMUNITY_NAMES = {
    "Црквена општина призренска": "Prizren",
    "Црквена општина сиринићка": "Štrpce-Sirinić",
    "Црквена општина великохочанска": "Velika Hoča",
    "Црквена општина ораховачка": "Orahovac",
    "Црквена општина пећка": "Peć",
    "Црквена општина гораждевачка": "Goraždevac",
    "Црквена општина осојанска": "Osojane",
    "Црквена општина источка": "Istok",
    "Црквена општина приштинска": "Priština",
    "Црквена општина липљанска": "Lipljan",
    "Црквена општина грачаничка - Ливађе": "Gračanica-Livađe",
    "Црквена општина лапљеселска": "Laplje Selo",
    "Црквена општина косовопољска": "Kosovo Polje",
    "Црквена општина доњегуштеричка": "Donja Gušterica",
    "Црквена општина урошевачка": "Uroševac",
    "Црквена општина гњиланска": "Gnjilane",
    "Црквена општина партешка": "Parteš",
    "Црквена општина пасјанска": "Pasjane",
    "Црквена општина витинска": "Vitina",
    "Црквена општина ранилушка": "Ranilug",
    "Црквена општина великоропотовска": "Veliko Ropotovo",
    "Црквена општина косовскокаменичка": "Kosovska Kamenica",
    "Црквена општина новобрдска": "Novo Brdo",
    "Црквена општина Звечан": "Zvečan",
    "Црквена општина косовскомитровичка": "Kosovska Mitrovica",
    "Црквена општина врачевска": "Vračevo",
    "Црквена општина сочаничка": "Sočanica",
    "Црквена општина лепосавићка": "Leposavić",
    "Црквена општина дубокопоточка": "Duboki Potok",
    "Црквена општина вучитрнска": "Vučitrn",
    "Црквена општина бабиномошка": "Babin Most",
    "Црквена општина прилушко-племетинска": "Prilužje-Plemetina",
    "Црквена општина за рашку област": "Raška Region",
    "Црквена општина никољачка": "Nikoljac",
    "Црквена општина добрињска": "Dobrinja",
    "Црквена општина брђанско-прислоничка": "Brđani-Prislonica",
    "Црквена општина љубишко-белоречка": "Ljubiš-Bela Reka",
}


def clean_text(value):
    value = re.sub(r"[\u2013\u2014]", " - ", str(value))
    value = value.replace("„", '"').replace("“", '"')
    value = value.replace("’", "'")
    value = value.replace("''", '"')
    return re.sub(r"\s+", " ", value).strip()


SERBIAN_LATIN = str.maketrans({
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D",
    "Ђ": "Đ", "Е": "E", "Ж": "Ž", "З": "Z", "И": "I",
    "Ј": "J", "К": "K", "Л": "L", "Љ": "Lj", "М": "M",
    "Н": "N", "Њ": "Nj", "О": "O", "П": "P", "Р": "R",
    "С": "S", "Т": "T", "Ћ": "Ć", "У": "U", "Ф": "F",
    "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š",
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "ђ": "đ", "е": "e", "ж": "ž", "з": "z", "и": "i",
    "ј": "j", "к": "k", "л": "l", "љ": "lj", "м": "m",
    "н": "n", "њ": "nj", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "ћ": "ć", "у": "u", "ф": "f",
    "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
})
SEAT_OVERRIDES = {
    "КПЗ Сремска Митровица": "Sremska Mitrovica Correctional Institution",
}


def serbian_latin(value):
    value = clean_text(value)
    return SEAT_OVERRIDES.get(value, value.translate(SERBIAN_LATIN))


def slug(value):
    return serbian.slug(clean_text(value))


def unique_id(prefix, local, seen):
    base = prefix + "-" + slug(local)
    row_id = base
    suffix = 2
    while row_id in seen:
        row_id = "%s-%d" % (base, suffix)
        suffix += 1
    seen.add(row_id)
    return row_id


def english_name(local, rank):
    local = clean_text(local)
    if rank == "Deanery":
        if local in DEANERY_NAMES:
            return "%s Deanery" % DEANERY_NAMES[local]
        numbered = re.match(
            r"^(Прво|Друго)\s+(.+?)\s+архијерејско\s+намесништво$",
            local, flags=re.I,
        )
        if numbered:
            number = {"прво": "First", "друго": "Second"}[
                numbered.group(1).lower()
            ]
            return "%s %s Deanery" % (
                number, serbian.transliterate(numbered.group(2)).title(),
            )
        label = re.sub(
            r"^Архијерејско\s+намесништво\s+", "", local,
            flags=re.I,
        )
        return "%s Deanery" % serbian.transliterate(label).title()
    if rank == "Church Community":
        if local in CHURCH_COMMUNITY_NAMES:
            return "Serbian Orthodox Church Community: %s" % (
                CHURCH_COMMUNITY_NAMES[local]
            )
        label = re.sub(r"^Црквена\s+општина\s+", "", local, flags=re.I)
        at_church = re.match(r"^при\s+Храму\s+(.+)$", label, flags=re.I)
        if at_church:
            church_name = english_name(
                "Храм " + at_church.group(1), "Church",
            )
            church_name = church_name.split(": ", 1)[-1]
            return "Serbian Orthodox Church Community at %s Church" % (
                church_name
            )
        return "Serbian Orthodox Church Community: %s" % (
            serbian.transliterate(label)
        )
    if rank == "Monastery Parish":
        label = re.sub(r"^Парохија\s+при\s+манастиру\s+", "", local,
                       flags=re.I)
        return "Serbian Orthodox Monastery Parish: %s" % (
            serbian.transliterate(label)
        )
    translated = EXACT_ENGLISH_LABELS.get(
        local, TRANSLATED_LABELS.get(local)
    )
    if not translated and rank in {
            "Church", "Cathedral", "Chapel", "Cemetery Chapel",
            "Cemetery Church", "Monastery", "Skete"}:
        translated = serbian.english_name(local, rank).split(": ", 1)[-1]
    if translated:
        translated = translated.replace("St.", "Saint")
        translated = re.sub(r"\bSt\s+", "Saint ", translated)
        translated = translated.replace(
            "Transfer of the Relics", "Translation of the Relics"
        )
        translated = translated.replace("Empress Jelena", "Empress Helen")
        replacements = (
            (r"\bVasilij Ostroški\b", "Basil of Ostrog"),
            (r"\bVasilij Ostroski\b", "Basil of Ostrog"),
            (r"\bGeorgi\b", "George"),
            (r"\bDimitrija\b", "Demetrios"),
            (r"\bIlia\b", "Elijah"),
            (r"\bSimeona\b", "Simeon"),
            (r"\bMirotocivog\b", "the Myrrh-streaming"),
            (r"\bStolpnik\b", "the Stylite"),
            (r"\bSvete Petka\b", "Saint Paraskeva"),
            (r"\bSaint Petka\b", "Saint Paraskeva"),
            (r"\bMyriliki\b", "Myra"),
            (r"\bMyrliki\b", "Myra"),
            (r"\bHoly Witches Cosma and Damian\b",
             "Holy Unmercenaries Cosmas and Damian"),
            (r"\bHoly Witches Cosma and Damjan\b",
             "Holy Unmercenaries Cosmas and Damian"),
            (r"\bSaint Nicholas(?: of)? Žički\b", "Saint Nikolaj of Žiča"),
            (r"\bSaint Nicholas Žički\b", "Saint Nikolaj of Žiča"),
            (r"\bSaint Kiriak the Outcast\b",
             "Venerable Kyriakos the Anchorite"),
            (r"\bFlower Martyr Mina\b", "Holy Martyr Menas"),
            (r"\bHoly Reverend Martyr\b", "Venerable Martyr"),
            (r"\bSaint Dimitrija\b", "Saint Demetrios"),
            (r"\bSaint Novel\b", "Saint Roman"),
            (r"\bthe Assumption of the (?:Blessed Virgin Mary|Holy Mother of God)\b",
             "the Dormition of the Most Holy Theotokos"),
            (r"\bthe Presentation of the (?:Blessed Virgin Mary|Holy Mother of God)\b",
             "the Entrance of the Most Holy Theotokos"),
            (r"\bthe Introduction of the Holy Mother of God\b",
             "the Entrance of the Most Holy Theotokos"),
            (r"\bthe (?:Intercession|Covering|Shroud) of the (?:Holy Virgin|Holy Mother of God)\b",
             "the Protection of the Most Holy Theotokos"),
            (r"\bBlessed Virgin Mary\b", "Most Holy Theotokos"),
            (r"\bHoly Mother of God\b", "Most Holy Theotokos"),
            (r"\bHoly Virgin\b", "Most Holy Theotokos"),
            (r"\b - Hotel\b", " - Gostinica"),
            (r"\bin Lebanon\b", "in Lebane"),
            (r"\bin Lausanne\b", "in Lozane"),
            (r"\bin the Fast Ship\b", "in Brzi Brod"),
            (r"\b - Violation\b", " - Kršanje"),
            (r"\bMonastery of Durres\b", "Drača Monastery"),
            (r"\bnear Guy\b", "near Gaj"),
            (r"\bThird Conversion of the Head\b",
             "Third Finding of the Head"),
            (r"\bJelena\b", "Helen"),
            (r"\bHoly Great Martyr Nedelja\b", "Great Martyr Kyriaki"),
            (r"\bHoly Martyr Nedelja\b", "Martyr Kyriaki"),
            (r"\bSaint Nedelja\b", "Saint Kyriaki"),
            (r"\bAssembly of\b", "Synaxis of"),
            (r"\bSaint Lazar the Four-Day\b",
             "Saint Lazarus the Four-Days-Dead"),
            (r"\bSaint Lazarus of the four-day age\b",
             "Saint Lazarus the Four-Days-Dead"),
            (r"\bPr\. Mother of God\b", "the Most Holy Theotokos"),
            (r"\bHoly Father Nicholas\b", "Saint Nicholas"),
            (r"\bdedicated to Venerable Sisoy the Great\b",
             "Venerable Sisoes the Great"),
            (r"\bAssumption of Saint Anne\b", "Dormition of Saint Anne"),
            (r"\bSaint Friday\b", "Saint Paraskeva"),
            (r"\bEast Friday Chapel\b", "Bright Friday Chapel"),
            (r"\bHoly Doctors Cosma and Damian\b",
             "Holy Unmercenaries Cosmas and Damian"),
            (r"\bHoly Doctors Cosma and Damjan\b",
             "Holy Unmercenaries Cosmas and Damian"),
            (r"\bMirlikia\b", "Myra"),
            (r"\bMirlikii\b", "Myra"),
            (r"\bLife-giving Source\b", "Life-giving Spring"),
            (r"\bLiving Source\b", "Life-giving Spring"),
            (r"\bBasil Ostroski\b", "Basil of Ostrog"),
            (r"\bTransfiguration in the Playground\b",
             "Transfiguration of the Lord in Igrište"),
            (r"\bSaint Father Nicholas\b", "Saint Nicholas"),
            (r"\bSaint Simeon Myrotočivo\b",
             "Saint Simeon the Myrrh-streaming"),
            (r"\bSaint Simeon Mirotočivo\b",
             "Saint Simeon the Myrrh-streaming"),
            (r"\bSaint Olimpius the Stylite\b",
             "Saint Alypius the Stylite"),
            (r"\bSaint Varvara\b", "Saint Barbara"),
            (r"\bin Kursumliji\b", "in Kuršumlija"),
            (r"\bin Raci\b", "in Rača"),
            (r"\bin Mozgov\b", "in Mozgovo"),
            (r"\bSaints Constantine and Helena\b",
             "Saints Constantine and Helen"),
        )
        for pattern, target in replacements:
            translated = re.sub(pattern, target, translated, flags=re.I)
        translated = re.sub(
            r"^(?:The\s+)?(?:Church|Temple|Cathedral(?: Church)?|"
            r"Chapel|Monastery|Skete)(?:\s+of)?\s+",
            "", translated, flags=re.I,
        )
        translated = translated.strip(" .,:-")
        translated = re.sub(r"\s+", " ", translated)
        return "Serbian Orthodox %s: %s" % (rank, translated)
    return serbian.english_name(local, rank)


def row(row_id, parent, country, local, sources, rank="Parish",
        kind="parish", name=None, **extra):
    local = clean_text(local)
    if rank in {"Deanery", "Vicariate"} and kind == "parish":
        kind = "diocese"
    item = {
        "id": row_id,
        "parent": parent,
        "kind": kind,
        "rank": rank,
        "name": name or english_name(local, rank),
        "local": local,
        "country": country,
        "sources": list(sources),
    }
    item.update(extra)
    return item


def site_rank(local):
    upper = local.upper().strip()
    if upper.startswith("МАНАСТИР"):
        return "Monastery"
    if upper.startswith("СКИТ"):
        return "Skete"
    if "САБОРНИ" in upper or "КАТЕДРАЛНИ" in upper:
        return "Cathedral"
    if "КАПЕЛ" in upper and "ГРОБЉ" in upper:
        return "Cemetery Chapel"
    if "КАПЕЛ" in upper:
        return "Chapel"
    return "Church"


def monastery_rank(local):
    return "Skete" if "СКИТ" in local.upper() else "Monastery"


def qualify_monastery(name, local, parent):
    if slug(local) in QUALIFIED_MONASTERIES:
        return "%s (%s)" % (name, DIOCESE_QUALIFIERS[parent])
    return name


def srem_site_parts(value):
    pieces = [clean_text(piece).strip(" ,") for piece in value.split(",")]
    pieces = [piece for piece in pieces if piece]
    title = pieces[0]
    seat = pieces[-1] if len(pieces) > 1 else None
    if seat:
        seat = re.sub(
            r"\s+СРПСКА\s+ПРАВОСЛАВНА\s+ЕПАРХИЈА\s+СРЕМСКА$",
            "", seat, flags=re.I,
        ).strip()
    address = pieces[1:-1] if len(pieces) > 2 else []
    return title, seat, address


def split_embedded_address(value):
    match = re.search(r"\s+(ул\.\s+.+?\s+бб)$", value, flags=re.I)
    if not match:
        return value, []
    return value[:match.start()].strip(" ,"), [match.group(1)]


TIMOK_PARISH_NAMES = {
    "доњомилановачки": "Donji Milanovac",
    "борски": "Bor",
    "мајданпечки": "Majdanpek",
    "бољевачки": "Boljevac",
    "подгорачки": "Podgorac",
    "градсковачко-јасеновачки": "Gradskovo-Jasenovac",
    "грљански": "Grljan",
    "зајечарски": "Zaječar",
    "брзо-паланачки": "Brza Palanka",
    "велико-врбичка": "Velika Vrbica",
    "грабовички": "Grabovica",
    "кладовски": "Kladovo",
    "књажевачки": "Knjaževac",
    "неготински": "Negotin",
    "кобишничко-буковчански": "Kobišnica-Bukovče",
    "михајловачки": "Mihajlovac",
    "праховски": "Prahovo",
    "радујевачки": "Radujevac",
    "рајачко-рогљевски": "Rajac-Rogljevo",
    "јабуковачки": "Jabukovac",
    "јасенички": "Jasenica",
    "сокобањски": "Sokobanja",
    "јошанички": "Jošanica",
}
SERBIAN_ORDINALS = {
    "први": "First", "други": "Second", "трећи": "Third",
    "четврти": "Fourth", "пети": "Fifth", "шести": "Sixth",
    "седми": "Seventh", "3.": "Third",
}


def timok_parish_name(descriptor):
    words = descriptor.split()
    ordinal = None
    if words and words[0] in SERBIAN_ORDINALS:
        ordinal = SERBIAN_ORDINALS[words.pop(0)]
    base = " ".join(words)
    place = TIMOK_PARISH_NAMES.get(base, serbian.transliterate(base).title())
    if ordinal:
        return "Serbian Orthodox Parish: %s %s" % (ordinal, place)
    return "Serbian Orthodox Parish: %s" % place


MILESEVA_PARISH_NAMES = {
    "Прва парохија прибојска": "First Priboj",
    "Друга парохија прибојска": "Second Priboj",
    "Трећа парохија прибојска": "Third Priboj",
    "Четврта парохија прибојска": "Fourth Priboj",
    "Пета парохија прибојска": "Fifth Priboj",
    "Шеста парохија прибојска": "Sixth Priboj",
    "Парохија поблаћка": "Poblaće",
    "Парохија саставачка": "Sastavci",
    "Парохија бањска": "Banja",
    "Парохија кратовска": "Kratovo",
    "Прва парохија пријепољска": "First Prijepolje",
    "Друга парохија пријепољска": "Second Prijepolje",
    "Трећа парохија пријепољска": "Third Prijepolje",
    "Парохија толачко-бабинска": "Tolac-Babine",
    "Прва парохија коловратска": "First Kolovrat",
    "Друга парохија коловратска": "Second Kolovrat",
    "Парохија ивањска": "Ivanje",
    "Парохија жупска": "Župa",
    "Парохија бродаревска": "Brodarevo",
    "Парохија сељанска": "Seljani",
    "Прва парохија нововарошка": "First Nova Varoš",
    "Друга парохија нововарошка": "Second Nova Varoš",
    "Трећа парохија нововарошка": "Third Nova Varoš",
    "Четврта парохија нововарошка": "Fourth Nova Varoš",
    "Парохија рутошко-радоињска": "Rutoši-Radoinja",
    "Парохија штитковачка": "Štitkovo",
    "Прва парохија сјеничка": "First Sjenica",
    "Друга парохија сјеничка": "Second Sjenica",
    "Парохија штаваљска": "Štavalj",
}


def expand_site_labels(value):
    value = clean_text(value)
    if "Латинска црква" in value:
        return [value]
    pieces = re.split(
        r"\s+и\s+(?=(?:Храм|Капела)\s+)|"
        r",\s+(?=(?:храм|Црква|Капела)\s+)",
        value, flags=re.I,
    )
    expanded = []
    for piece in pieces:
        piece = piece.strip(" ,")
        if not piece:
            continue
        if piece.startswith("Храм "):
            offset = piece.find(" Храм ", len("Храм "))
            if offset > 0:
                expanded.extend([piece[:offset], piece[offset + 1:]])
                continue
        joined = re.split(r"(?<=[а-яА-Я])(?=Храм\s+)", piece)
        expanded.extend(item.strip(" ,") for item in joined if item.strip(" ,"))
    return expanded


def nis_rows():
    parent = "sr-nis"
    seen = {parent}
    rows = []
    deanery_names = {
        "aleksinacko-namesnistvo": "Архијерејско намесништво алексиначко",
        "belopalanacko-namesnistvo": "Архијерејско намесништво белопаланачко",
        "vlasotinacko-namesnistvo": "Архијерејско намесништво власотиначко",
        "jablanicko-namesnistvo": "Архијерејско намесништво јабланичко",
        "kosanicko-namesnistvo": "Архијерејско намесништво косаничко",
        "leskovacko-namesnistvo": "Архијерејско намесништво лесковачко",
        "prvo-nisko-namesnistvo": "Прво нишко архијерејско намесништво",
        "drugo-nisko-namesnistvo": "Друго нишко архијерејско намесништво",
        "pirotsko-namesnistvo": "Архијерејско намесништво пиротско",
        "toplicko-namesnistvo": "Архијерејско намесништво топличко",
    }
    deanery_ids = {}
    for key, local in deanery_names.items():
        row_id = unique_id("rs-sr-nis-deanery", local, seen)
        deanery_ids[key] = row_id
        rows.append(row(
            row_id, parent, "RS", local, [NIS_ROOT], rank="Deanery",
        ))
    ordinals = [
        "прва", "друга", "трећа", "четврта", "пета",
        "шеста", "седма", "осма", "девета", "десета",
    ]
    ordinal_english = [
        "First", "Second", "Third", "Fourth", "Fifth",
        "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
    ]
    for item in NIS_DATA["parishes"]:
        deanery_key = urlparse(item["url"]).path.split("/")[2]
        deanery_id = deanery_ids[deanery_key]
        parish_ids = []
        for index in range(item["count"]):
            if item["count"] == 1:
                local = "Парохија %s" % item["label"]
            else:
                local = "%s - %s парохија" % (
                    item["label"], ordinals[index],
                )
            row_id = unique_id("rs-sr-nis-parish", local, seen)
            parish_ids.append(row_id)
            label = clean_text(item["label"])
            location = NIS_PARISH_CONTEXT.get(label)
            if not location:
                location = serbian.transliterate(
                    label.split(",", 1)[0].strip()
                )
            location = re.sub(r"\s+i\s+", " and ", location)
            parish_name = "Serbian Orthodox Parish: %s" % location
            if item["count"] > 1:
                parish_name = "Serbian Orthodox Parish: %s %s" % (
                    ordinal_english[index], location,
                )
            rows.append(row(
                row_id, deanery_id, "RS", local, [item["url"]],
                name=parish_name,
            ))
        site_parent = parish_ids[0] if parish_ids else deanery_id
        for source_local in item["temples"]:
            for local in expand_site_labels(source_local):
                if local in HELD_CONSTRUCTION_SITES:
                    continue
                rank = site_rank(local)
                site_name = english_name(local, rank)
                if not re.search(
                        r"\s(?:у|на)\s|,|\s-\s", local, flags=re.I):
                    context = item["label"].split(",", 1)[0].strip()
                    site_name = "%s in %s" % (
                        site_name, serbian.transliterate(context),
                    )
                rows.append(row(
                    unique_id("rs-sr-nis-site", local, seen),
                    site_parent, "RS", local,
                    [item["temple_url"] or item["url"]], rank=rank,
                    kind="monastery" if rank in {"Monastery", "Skete"}
                    else "parish", name=site_name,
                ))
    for item in NIS_DATA["monasteries"]:
        local = item["local"]
        rank = monastery_rank(local)
        monastery_name = qualify_monastery(
            english_name(local, rank), local, parent,
        )
        rows.append(row(
            unique_id("rs-sr-nis-monastery", local, seen),
            parent, "RS", local, [item["url"]], rank=rank,
            kind="monastery", name=monastery_name,
        ))
    return rows


def zica_rows():
    parent = "sr-zica"
    seen = {parent}
    rows = []
    community_counts = {}
    for deanery in ZICA_DATA["deaneries"]:
        for community in deanery["communities"]:
            key = clean_text(community["local"]).casefold()
            community_counts[key] = community_counts.get(key, 0) + 1
    for item in ZICA_DATA["deaneries"]:
        label = item["label"].split("(", 1)[0].strip().lower()
        local = "Архијерејско намесништво %s" % label
        deanery_id = unique_id("rs-sr-zica-deanery", local, seen)
        rows.append(row(
            deanery_id, parent, "RS", local, [item["url"]],
            rank="Deanery",
        ))
        for community in item["communities"]:
            local, community_address = split_embedded_address(
                clean_text(community["local"])
            )
            rank = (
                "Monastery Parish"
                if local.lower().startswith("парохија при манастиру")
                else "Church Community"
            )
            community_id = unique_id(
                "rs-sr-zica-community", local, seen,
            )
            community_name = english_name(local, rank)
            if community_counts[clean_text(community["local"]).casefold()] > 1:
                deanery_label = item["label"].split("(", 1)[0].strip().title()
                community_name = "%s (%s Deanery)" % (
                    community_name, serbian.transliterate(deanery_label),
                )
            rows.append(row(
                community_id, deanery_id, "RS", local, [item["url"]],
                rank=rank, name=community_name,
                address=community_address,
            ))
            for source_temple in community["temples"]:
                for temple in expand_site_labels(source_temple):
                    temple, temple_address = split_embedded_address(temple)
                    if temple in HELD_CONSTRUCTION_SITES:
                        continue
                    temple_rank = site_rank(temple)
                    community_place = re.sub(
                        r"^(?:Црквена општина|Парохија при манастиру)\s+",
                        "", local, flags=re.I,
                    )
                    if community_place.lower().startswith("при храму "):
                        community_place = item["label"].split("(", 1)[0].strip()
                        community_place = "%s deanery" % community_place.title()
                    temple_name = "%s in %s" % (
                        english_name(temple, temple_rank),
                        serbian.transliterate(community_place),
                    )
                    rows.append(row(
                        unique_id("rs-sr-zica-site", temple, seen),
                        community_id, "RS", temple, [item["url"]],
                        rank=temple_rank,
                        kind="monastery"
                        if temple_rank in {"Monastery", "Skete"}
                        else "parish", name=temple_name,
                        address=temple_address,
                    ))
    monasteries = [
        "Манастир Благовештење", "Манастир Ваведење",
        "Манастир Вазнесење", "Манастир Вољавча", "Манастир Враћевшница",
        "Манастир Вујан", "Манастир Градац", "Манастир Дубрава",
        "Манастир Жича", "Манастир Згодачица", "Манастир Јежевица",
        "Манастир Јовање", "Манастир Каменац", "Манастир Клисура",
        "Манастир Ковиље", "Манастир Никоље", "Манастир Нова Павлица",
        "Манастир Преображење", "Манастир Придворица", "Манастир Рача",
        "Манастир Рујан", "Манастир Света Тројица", "Манастир Сретење",
        "Манастир Стјеник", "Манастир Стубал", "Манастир Студеница",
        "Манастир Увац", "Манастир Успеније",
    ]
    for local in monasteries:
        monastery_name = qualify_monastery(
            english_name(local, "Monastery"), local, parent,
        )
        rows.append(row(
            unique_id("rs-sr-zica-monastery", local, seen),
            parent, "RS", local, [ZICA_MONASTERIES], rank="Monastery",
            kind="monastery", name=monastery_name,
        ))
    return rows


def srem_rows():
    parent = "sr-srem"
    seen = {parent}
    rows = []
    numbered_monasteries = set()
    for item in SREM_DATA["deaneries"]:
        local = item["local"]
        deanery_id = unique_id("rs-sr-srem-deanery", local, seen)
        rows.append(row(
            deanery_id, parent, "RS", local, [SREM_DEANERIES],
            rank="Deanery",
        ))
        for site in item["sites"]:
            source_local = site["local"]
            if "РХ " in source_local:
                continue
            local, seat, address = srem_site_parts(source_local)
            if local == "Храм Преноса моштију Светог оца Николаја" \
                    and seat == "Ириг" and site["number"] == 35:
                continue
            rank = site_rank(local)
            if rank == "Monastery":
                numbered_monasteries.add("Манастир Ваведење")
            site_name = english_name(local, rank)
            if seat:
                site_name = "%s in %s" % (
                    site_name, serbian_latin(seat),
                )
            rows.append(row(
                unique_id(
                    "rs-sr-srem-site", "%s %s" % (local, seat or ""),
                    seen,
                ),
                deanery_id, "RS", local, [SREM_CHURCHES], rank=rank,
                kind="monastery" if rank == "Monastery" else "parish",
                name=site_name, seat=seat, address=address,
            ))
    for local in SREM_DATA["monasteries"]:
        if local in numbered_monasteries:
            continue
        monastery_name = qualify_monastery(
            english_name(local, monastery_rank(local)), local, parent,
        )
        rows.append(row(
            unique_id("rs-sr-srem-monastery", local, seen),
            parent, "RS", local, [SREM_MONASTERIES],
            rank=monastery_rank(local), kind="monastery",
            name=monastery_name,
        ))
    return rows


def timok_rows():
    parent = "sr-timok"
    seen = {parent}
    rows = []
    deanery_ids = {}
    for term_id, item in TIMOK_DATA["deaneries"].items():
        local = item["local"]
        row_id = unique_id("rs-sr-timok-deanery", local, seen)
        deanery_ids[int(term_id)] = row_id
        rows.append(row(
            row_id, parent, "RS", local, [item["url"]],
            rank="Deanery",
        ))
    for item in TIMOK_DATA["parishes"]:
        local = "Парохија - %s" % item["descriptor"]
        rows.append(row(
            unique_id("rs-sr-timok-parish", local, seen),
            deanery_ids[item["deanery_id"]], "RS", local,
            [item["url"]], name=timok_parish_name(item["descriptor"]),
        ))
    for item in TIMOK_DATA["monasteries"]:
        local = item["local"]
        rows.append(row(
            unique_id("rs-sr-timok-monastery", local, seen),
            parent, "RS", local, [item["url"]],
            rank=monastery_rank(local), kind="monastery",
        ))
    return rows


MILESEVA = {
    "pribojsko": {
        "local": "Архијерејско намесништво прибојско",
        "source": MILESEVA_PRIBOJ,
        "parishes": [
            "Прва парохија прибојска", "Друга парохија прибојска",
            "Трећа парохија прибојска", "Четврта парохија прибојска",
            "Пета парохија прибојска", "Шеста парохија прибојска",
            "Парохија поблаћка", "Парохија саставачка",
            "Парохија бањска", "Парохија кратовска",
        ],
        "sites": [
            "Храм Васкрсења Христовог, Нови Прибој",
            "Храм Светог великомученика кнеза Лазара, Стари Прибој",
            "Храм Светог Петра Дабробосанског, Саставци, Прибој",
            "Храм Светог цара Константина и царице Јелене, Херцеговачка Голеша, Прибој",
            "Храм Покрова Пресвете Богородице, Прибојска Голеша, Прибој",
            "Храм Светог великомученика Пантелејмона, Пожегрмац, Прибој",
            "Храм Светог Архангела Михаила, Поблаће, Прибој",
            "Храм Светог великомученика Прокопија, Кратово, Прибој",
            "Храм Светог пророка Илије, Манастир Бања, Прибојска Бања",
            "Храм Светог Николаја мирликијског, Манастир Бања, Прибојска Бања",
        ],
    },
    "prijepoljsko": {
        "local": "Архијерејско намесништво пријепољско",
        "source": MILESEVA_PRIJEPOLJE,
        "parishes": [
            "Прва парохија пријепољска", "Друга парохија пријепољска",
            "Трећа парохија пријепољска", "Парохија толачко-бабинска",
            "Прва парохија коловратска", "Друга парохија коловратска",
            "Парохија ивањска", "Парохија жупска",
            "Парохија бродаревска", "Парохија сељанска",
        ],
        "sites": [
            "Храм Светог великомученика Прокопија, Велика Жупа",
            "Храм Преподобне мати Параскеве - Свете Петке, Бабине",
            "Храм Трећег обретења главе Светог Јована Крститеља, Џурово",
            "Храм Светих апостола Петра и Павла, Црквени Тоци",
            "Саборни храм Светог Василија Острошког, Пријепоље",
            "Храм Светог цара Константина и царице Јелене, Сељашница",
            "Храм Ваведења Пресвете Богородице, Ранче Поље",
            "Храм Светог архиђакона Стефана, Џурово Брдо",
            "Храм Успења Пресвете Богородице, Ивање",
            "Храм Светог великомученика кнеза Лазара, Бродарево",
            "Храм Светог Саве, Сопотница",
            "Храм Светог Николаја Српског, Коловрат",
            "Храм Свете великомученице Марине, Камена Гора",
            "Храм Свих Светих, Житин - Боровице",
        ],
    },
    "novovarosko": {
        "local": "Архијерејско намесништво нововарошко",
        "source": MILESEVA_NOVA_VAROS,
        "parishes": [
            "Прва парохија нововарошка", "Друга парохија нововарошка",
            "Трећа парохија нововарошка", "Четврта парохија нововарошка",
            "Парохија рутошко-радоињска", "Парохија штитковачка",
            "Прва парохија сјеничка", "Друга парохија сјеничка",
            "Парохија штаваљска",
        ],
        "sites": [
            "Храм Благовештења Пресвете Богородице, Буковик",
            "Храм Свете Тројице, Нова Варош",
            "Храм Светих апостола Петра и Павла, Рутоши",
            "Храм Преображења Господњег, Радоина",
            "Храм Рођења Христовог, Златар",
            "Храм Светог Јована Крститеља, Вилови",
            "Храм Благовештења Пресвете Богородице, Штитково",
            "Храм Свете Тројице, Радијевићи",
            "Храм Српских мученика и новомученика, Љепојевићи - Јавор",
            "Храм Светог Саве, Аљиновићи",
            "Храм Светих апостола Петра и Павла, Сјеница",
            "Храм Светог великомученика Георгија, Лопиже",
            "Храм Вазнесења Господњег, Штаваљ",
            "Храм Светих дванаест апостола, Буђево",
            "Храм Свете Тројице, Брњица",
            "Храм Светог великомученика кнеза Лазара, Сјеничке Баре",
            "Храм Свете Марије Магдалине, Врсјенице",
            "Храм Вазнесења Господњег, Височка",
        ],
    },
}


def mileseva_rows():
    parent = "sr-milesevo"
    seen = {parent}
    rows = []
    for item in MILESEVA.values():
        deanery_id = unique_id("rs-sr-mil-deanery", item["local"], seen)
        rows.append(row(
            deanery_id, parent, "RS", item["local"], [item["source"]],
            rank="Deanery",
        ))
        for local in item["parishes"]:
            rows.append(row(
                unique_id("rs-sr-mil-parish", local, seen),
                deanery_id, "RS", local, [item["source"]],
                name="Serbian Orthodox Parish: %s" %
                MILESEVA_PARISH_NAMES[local],
            ))
        for local in item["sites"]:
            rows.append(row(
                unique_id("rs-sr-mil-church", local, seen),
                deanery_id, "RS", local, [item["source"]],
                rank=site_rank(local),
            ))
    bucje = "Храм Вазнесења Господњег, Бучје"
    rows.append(row(
        unique_id("rs-sr-mil-church", bucje, seen),
        parent, "RS", bucje, [MILESEVA_PLJEVLJA], rank="Church",
    ))
    monasteries = [
        "Манастир Милешева", "Манастир Сељани", "Манастир Давидовица",
        "Манастир Пустиња", "Манастир Светог пророка Илије - Јабука",
        "Манастир Куманица", "Манастир Светог Николаја - Прибојска Бања",
        "Манастир Мажићи", "Манастир Светог Јоакима и Ане - Света Јања",
        "Манастир Бистрица", "Манастир Дубница",
        "Манастир Светих Козме и Дамјана - Водена Пољана",
    ]
    for local in monasteries:
        monastery_name = qualify_monastery(
            english_name(local, "Monastery"), local, parent,
        )
        rows.append(row(
            unique_id("rs-sr-mil-monastery", local, seen),
            parent, "RS", local, [MILESEVA_MONASTERIES],
            rank="Monastery", kind="monastery", name=monastery_name,
        ))
    return rows


RASKA_COMMUNITIES = {
    "призренско": [
        "Црквена општина призренска", "Црквена општина сиринићка",
        "Црквена општина великохочанска", "Црквена општина ораховачка",
    ],
    "пећско": [
        "Црквена општина пећка", "Црквена општина гораждевачка",
        "Црквена општина осојанска", "Црквена општина источка",
    ],
    "приштинско": [
        "Црквена општина приштинска", "Црквена општина липљанска",
        "Црквена општина грачаничка - Ливађе",
        "Црквена општина лапљеселска", "Црквена општина косовопољска",
        "Црквена општина доњегуштеричка", "Црквена општина урошевачка",
    ],
    "гњиланско": [
        "Црквена општина гњиланска", "Црквена општина партешка",
        "Црквена општина пасјанска", "Црквена општина витинска",
        "Црквена општина ранилушка", "Црквена општина великоропотовска",
        "Црквена општина косовскокаменичка", "Црквена општина новобрдска",
    ],
    "косовскомитровичко": [
        "Црквена општина Звечан", "Црквена општина косовскомитровичка",
        "Црквена општина врачевска", "Црквена општина сочаничка",
        "Црквена општина лепосавићка", "Црквена општина дубокопоточка",
        "Црквена општина вучитрнска", "Црквена општина бабиномошка",
        "Црквена општина прилушко-племетинска",
    ],
    "новопазарско": [
        "Црквена општина за рашку област",
        "Црквена општина никољачка", "Црквена општина добрињска",
    ],
}


def raska_rows():
    parent = "sr-raska-prizren"
    seen = {parent}
    rows = []
    for deanery, communities in RASKA_COMMUNITIES.items():
        local = "Архијерејско намесништво %s" % deanery
        deanery_id = unique_id("rs-sr-rp-deanery", local, seen)
        rows.append(row(
            deanery_id, parent, "RS", local, [RASKA_PARISHES],
            rank="Deanery",
        ))
        for local in communities:
            rows.append(row(
                unique_id("rs-sr-rp-community", local, seen),
                deanery_id, "RS", local, [RASKA_PARISHES],
                rank="Church Community",
            ))
    monasteries = [
        "Манастир Свете Недеље",
        "Манастир Успења Пресвете Богородице у Доњем Кормињану",
        "Манастир Светог Димитрија у Сушици", "Манастир Тушимља",
        "Манастир Успења Пресавете Богородице у Ђаковици",
        "Манастир Врачево", "Манастир Будисавци", "Манастир Дубоки Поток",
        "Манастир Кончул", "Манастир Сочаница", "Манастир Улије",
        "Манастир Девине Воде", "Манастир Зочиште",
        "Манастир Ђурђеви Ступови", "Манастир Соколица", "Манастир Девич",
        "Манастир Брњак", "Манастир Драганац", "Манастир Гориоч",
        "Манастир Бањска", "Манастир Сопоћани", "Манастир Црна Река",
        "Манастир Светих Арханђела", "Манастир Пећка Патријаршија",
        "Манастир Грачаница", "Манастир Високи Дечани",
    ]
    for local in monasteries:
        monastery_name = qualify_monastery(
            english_name(local, "Monastery"), local, parent,
        )
        rows.append(row(
            unique_id("rs-sr-rp-monastery", local, seen),
            parent, "RS", local, [RASKA_MONASTERIES],
            rank="Monastery", kind="monastery", name=monastery_name,
        ))
    return rows


def simple_branch(parent, values, source, prefix, rank="Monastery"):
    seen = {parent}
    rows = []
    for local in values:
        actual_rank = monastery_rank(local) if rank == "Monastery" else rank
        item_name = english_name(local, actual_rank)
        if actual_rank in {"Monastery", "Skete"}:
            item_name = qualify_monastery(
                item_name, local, parent,
            )
        rows.append(row(
            unique_id(prefix, local, seen), parent, "RS", local, [source],
            rank=actual_rank,
            kind="monastery" if actual_rank in {"Monastery", "Skete"}
            else "parish", name=item_name,
        ))
    return rows


def backa_rows():
    parent = "sr-backa"
    seen = {parent}
    rows = []
    for label in [
        "бачкопаланачко", "бечејско", "жабаљско", "кулско",
        "новосадско прво", "новосадско друго", "сомборско", "суботичко",
    ]:
        local = "Архијерејско намесништво %s" % label
        rows.append(row(
            unique_id("rs-sr-backa-deanery", local, seen),
            parent, "RS", local, [BACKA_SCHEMATISM], rank="Deanery",
        ))
    for local in ["Манастир Ковиљ", "Манастир у Каћу", "Манастир Бођани"]:
        rows.append(row(
            unique_id("rs-sr-backa-monastery", local, seen),
            parent, "RS", local, [BACKA_MONASTERIES],
            rank="Monastery", kind="monastery",
        ))
    return rows


BANAT_MONASTERY_NAMES = [
    "Манастир Војловица", "Манастир Средиште", "Манастир Баваниште",
    "Скит Светих четрдесет мученика севастијских у Старом Селу код Гаја",
    "Манастир Месић", "Манастир Свете Меланије у Зрењанину",
    "Манастир Свете Тројице у Кикинди", "Манастир Хајдучица",
    "Манастир - Скит Светог великомученика Димитрија у Влајковцу",
]
SUMADIJA_MONASTERY_NAMES = [
    "Манастир Благовештење", "Манастир Брезовац", "Манастир Вољавча",
    "Манастир Грнчарица", "Манастир Денковац", "Манастир Дивостин",
    "Манастир Доброводица", "Манастир Драча", "Манастир Јошаница",
    "Манастир Каленић", "Манастир Кастаљан", "Манастир Липар",
    "Манастир Манастирак", "Манастир Никоље", "Манастир Павловац",
    "Манастир Петковица", "Манастир Пиносава", "Манастир Прекопеча",
    "Манастир Прерадовац", "Манастир Ралетинац", "Манастир Саринац",
    "Манастир Сибница", "Манастир Тресије", "Манастир Ћелије",
    "Манастир Шуљковац",
]
VALJEVO_MONASTERY_NAMES = [
    "Манастир Боговађа", "Манастир Грабовац", "Манастир Докмир",
    "Манастир Грачаница", "Манастир Јовања", "Манастир Пустиња",
    "Манастир Лелић", "Манастир Ћелије",
]


DACIA_ROWS = [
    {
        "id": "rs-ro-df-vojvodina-vicariate",
        "parent": "ro-dacia-felix",
        "country": "RS",
        "kind": "diocese",
        "rank": "Vicariate",
        "local": "Vicariatul Ortodox Român al Voivodinei",
        "name": "Romanian Orthodox Vicariate of Vojvodina",
        "sources": [DACIA_ADMIN, ROMANIAN_EXTERNAL],
    },
    {
        "id": "rs-ro-df-timok-vicariate",
        "parent": "ro-dacia-felix",
        "country": "RS",
        "kind": "diocese",
        "rank": "Vicariate",
        "local": "Vicariatul Ortodox Român al Timocului",
        "name": "Romanian Orthodox Vicariate of Timok",
        "sources": [DACIA_ADMIN, ROMANIAN_EXTERNAL],
    },
    {
        "id": "rs-ro-df-vrsac-ascension-cathedral",
        "parent": "ro-dacia-felix",
        "country": "RS",
        "kind": "parish",
        "rank": "Cathedral",
        "local": "Catedrala Episcopală \"Înălțarea Domnului\" din Vârșeț",
        "name": "Ascension of the Lord Episcopal Cathedral in Vrsac",
        "sources": [DACIA_CATHEDRAL],
    },
]

DIRECT_RUSSIA_ROWS = [
    {
        "id": "rs-ru-belgrade-metochion",
        "parent": "russia",
        "country": "RS",
        "kind": "parish",
        "rank": "Patriarchal Metochion",
        "local": "Подворье Русской Православной Церкви в Белграде",
        "name": "Patriarchal Metochion of the Russian Orthodox Church in Belgrade",
        "seat": "Belgrade",
        "address": ["Таковска 4", "11000 Београд"],
        "sources": [RUSSIAN_BELGRADE],
    },
    {
        "id": "rs-ru-belgrade-holy-trinity",
        "parent": "rs-ru-belgrade-metochion",
        "country": "RS",
        "kind": "parish",
        "rank": "Church",
        "local": "Храм Святой Троицы в Белграде",
        "name": "Holy Trinity Church in Belgrade",
        "address": ["Таковска 4", "11000 Београд"],
        "sources": [RUSSIAN_BELGRADE],
    },
    {
        "id": "rs-ru-belgrade-iveron-chapel",
        "parent": "rs-ru-belgrade-metochion",
        "country": "RS",
        "kind": "parish",
        "rank": "Cemetery Chapel",
        "local": "Иверская часовня на Русском кладбище в Белграде",
        "name": "Iveron Chapel at the Russian Cemetery in Belgrade",
        "sources": [RUSSIAN_BELGRADE],
    },
]


def build_rows():
    return {
        "sr-backa": backa_rows(),
        "sr-banat": simple_branch(
            "sr-banat", BANAT_MONASTERY_NAMES, BANAT_MONASTERIES,
            "rs-sr-banat-monastery",
        ),
        "sr-milesevo": mileseva_rows(),
        "sr-nis": nis_rows(),
        "sr-raska-prizren": raska_rows(),
        "sr-srem": srem_rows(),
        "sr-sumadija": simple_branch(
            "sr-sumadija", SUMADIJA_MONASTERY_NAMES,
            SUMADIJA_MONASTERIES, "rs-sr-sumadija-monastery",
        ),
        "sr-timok": timok_rows(),
        "sr-valjevo": simple_branch(
            "sr-valjevo", VALJEVO_MONASTERY_NAMES,
            VALJEVO_SITES, "rs-sr-valjevo-monastery",
        ),
        "sr-zica": zica_rows(),
        "ro-dacia-felix": [dict(item) for item in DACIA_ROWS],
    }


ROWS = build_rows()
ENGLISH_NAMES = {
    item["id"]: item["name"]
    for source_rows in list(ROWS.values()) + [DIRECT_RUSSIA_ROWS]
    for item in source_rows
}
ENGLISH_SEATS = {
    item["seat"]: serbian_latin(item["seat"])
    for source_rows in list(ROWS.values()) + [DIRECT_RUSSIA_ROWS]
    for item in source_rows
    if item.get("seat")
}

EXPECTED = {
    "sr-backa": 11,
    "sr-banat": 9,
    "sr-milesevo": 87,
    "sr-nis": 604,
    "sr-raska-prizren": 67,
    "sr-srem": 177,
    "sr-sumadija": 25,
    "sr-timok": 63,
    "sr-valjevo": 8,
    "sr-zica": 382,
    "ro-dacia-felix": 3,
}
DIRECT_RUSSIA_EXPECTED = 3

UNTRANSLATED_NAME_PATTERNS = (
    r"\b(?:rodjenja|prenosa|mostiju|cudotvorca|careva|carice|"
    r"vaskrsenja|prepodobnog|arhistratiga|uspenja|jevandjelista|"
    r"obretenja|usekovanja|zivonosnog|istocnika|posvecen|sabora|"
    r"mirotocivog|stolpnika|mirilikijskog|besrebrenika|cudotvoraca|"
    r"sirmijskih|velikomucenika|velikomucenice|prepodobnomucenice|"
    r"vasilij|georgi|dimitrija|ilia|stolpnik)\b",
    r"\bpri\s+hramu\b",
    r"\bsvetog\s+proroka\b",
    r"\bpresvete\s+bogorodice\b",
    r"\bsaborna\s+crkva\b",
    r"\b(?:borski|zajecarski|kladovski|knjazevacki|negotinski|"
    r"sokobanjski)\b",
    r"\b(?:peti|cetvrti|sesti|sedmi|treci|prvi)\b",
    r"\bnovoselska\s+parohija\b",
    r"\bbasil\s+ostroski\b",
    r"\bsaint\s+friday\b",
    r"\beast\s+friday\b",
    r"\bholy\s+doctors\b",
    r"\bmirlik(?:ia|ii)\b",
    r"\b(?:living|life-giving)\s+source\b",
    r"\btransfiguration\s+in\s+the\s+playground\b",
    r"\bsaint\s+father\s+nicholas\b",
    r"\bsaint\s+simeon\s+(?:myro|miro)točivo\b",
    r"\bsaint\s+olimpius\b",
    r"\bsaint\s+varvara\b",
    r"\bin\s+(?:kursumliji|raci|mozgov)\b",
    r"\bsaint\s+doctors\s+and\s+miracle\s+workers\b",
    r"\bskete:\s+monastery\s+of\b",
    r"\bchapel:\s+chapel\s+of\b",
    r"\bsaint\s+of\s+the\s+great\s+martyr\b",
    r"\bsaint\s+sava\s+temple\b",
    r"\blog\s+cabin\s+temple\b",
    r"\bin\s+vrel\b",
)


def clean(source):
    out = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    out.setdefault("checked", CHECKED)
    sources = list(out.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % out.get("id"))
    if not all(str(url).startswith("http") for url in sources):
        raise ValueError("%s carries a non-URL source" % out.get("id"))
    out["sources"] = sources
    out["cite"] = list(sources)
    return out


def validate_rows(source_rows, branch_parent, all_seen):
    rows = []
    branch_seen = {branch_parent}
    countries = set()
    for source in source_rows:
        item = clean(source)
        row_id = item.get("id")
        if not row_id or row_id in all_seen:
            raise ValueError("duplicate or missing id: %s" % row_id)
        if item.get("parent") not in branch_seen:
            raise ValueError(
                "%s hangs off an unknown branch parent: %s" %
                (row_id, item.get("parent"))
            )
        if item.get("kind") not in {"diocese", "parish", "monastery"}:
            raise ValueError("%s has unsupported kind" % row_id)
        if item.get("country") != "RS":
            raise ValueError("%s has invalid country" % row_id)
        if not item.get("local") or not item.get("name"):
            raise ValueError("%s has no usable local or English name" % row_id)
        english = item["name"]
        if any("\u0400" <= char <= "\u04ff" for char in english):
            raise ValueError("%s has Cyrillic in its English name" % row_id)
        if any(re.search(pattern, english, flags=re.I)
               for pattern in UNTRANSLATED_NAME_PATTERNS):
            raise ValueError("%s has untranslated ecclesiastical text" % row_id)
        if (re.search(r"\s-\s*$", english) or "''" in english
                or "  " in english):
            raise ValueError("%s has a malformed English ending or quote" % row_id)
        if re.search(r"\bul\.\s|\bbb\b", english, flags=re.I):
            raise ValueError("%s carries a street address in its name" % row_id)
        suffix = english.split(": ", 1)[-1]
        if suffix[:1].islower() and not suffix.startswith("the "):
            raise ValueError("%s has an unnormalized English name" % row_id)
        rendered = json.dumps(item, ensure_ascii=False)
        if any(mark in rendered for mark in ("\u2013", "\u2014", "\ufffd")):
            raise ValueError(
                "%s has forbidden punctuation or encoding" % row_id
            )
        all_seen.add(row_id)
        branch_seen.add(row_id)
        countries.add(item["country"])
        rows.append(item)
    return rows, countries


def build_all():
    payloads = {}
    all_seen = set(ROWS)
    all_seen.add("russia")
    for parent, source_rows in ROWS.items():
        rows, countries = validate_rows(source_rows, parent, all_seen)
        payload = {"v": 1, "parent": parent, "rows": rows}
        if len(countries) == 1:
            payload["country"] = next(iter(countries))
        payloads[parent] = payload
    direct, _ = validate_rows(DIRECT_RUSSIA_ROWS, "russia", all_seen)
    counts = {
        parent: len(payload["rows"])
        for parent, payload in payloads.items()
    }
    if counts != EXPECTED:
        raise ValueError("Serbia counts changed: %r" % counts)
    if len(direct) != DIRECT_RUSSIA_EXPECTED:
        raise ValueError("Russian direct count changed: %d" % len(direct))
    return payloads, direct


def build():
    return build_all()[0]


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads, direct = build_all()
    except (OSError, ValueError) as exc:
        print("directory Serbia: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(
            {"branches": payloads, "direct_russia_rows": direct},
            ensure_ascii=False, indent=2, sort_keys=True,
        ))
    total = sum(len(payload["rows"]) for payload in payloads.values())
    print(
        "Serbia: %d verified bodies across %d canonical parents, plus %d direct Russian rows"
        % (total, len(payloads), len(direct))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
