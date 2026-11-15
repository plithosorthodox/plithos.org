#!/usr/bin/env python3
"""Current officially named Eastern Orthodox bodies in Kyrgyzstan.

The Bishkek and Kyrgyzstan Diocese publishes forty-nine current bodies in
five deanery rosters. Current 2026 diocesan reports also establish the Holy
Trinity Monastery at Ak-Bulun as an active monastery with a resident sisterhood
and regular worship. The monastery is added from those reports because the
deanery roster has not yet caught up with the diocese's own current news.

    python tools/directory_kyrgyzstan.py --check
    python tools/directory_kyrgyzstan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

PATRIARCHATE = "https://patriarchia.ru/org/295"
CENTRAL = "https://pravoslavie.kg/blagochiniya/1"
TALAS = "https://pravoslavie.kg/blagochiniya/4"
ISSYK_KUL = "https://pravoslavie.kg/blagochiniya/5"
OSH = "https://pravoslavie.kg/blagochiniya/6"
CHUY_TOKMOK = "https://pravoslavie.kg/blagochiniya/7"
AK_BULUN_FEAST = "https://pravoslavie.kg/news/5058"
AK_BULUN_PILGRIMAGE = "https://pravoslavie.kg/news/5083"
AK_BULUN_PROGRAMME = "https://pravoslavie.kg/news/5027"


def body(row_id, name, local, seat, address, dedication, source,
         rank="Church", kind="parish"):
    row = {
        "id": row_id,
        "parent": "ru-bishkek",
        "kind": kind,
        "rank": rank,
        "name": name,
        "local": local,
        "seat": seat,
        "country": "KG",
        "dedication": dedication,
        "sources": source if isinstance(source, list) else [source],
    }
    if address:
        row["address"] = address if isinstance(address, list) else [address]
    return row


GROUPS = {
    "central": [
        body(
            "kg-ru-bishkek-holy-resurrection-cathedral",
            "Holy Resurrection Cathedral in Bishkek",
            "Свято-Воскресенский кафедральный собор",
            "Bishkek",
            "720033, Кыргызская Республика, г. Бишкек, пр. Жибек-Жолу, 1079",
            "The Resurrection of Christ",
            CENTRAL,
            rank="Cathedral",
        ),
        body(
            "kg-ru-bishkek-saint-vladimir-cathedral",
            "Cathedral of Saint Vladimir, Equal-to-the-Apostles, in Bishkek",
            (
                "Собор святого равноапостольного Великого Князя Владимира "
                "(мкрн. Асанбай)"
            ),
            "Bishkek",
            (
                "720049, Кыргызская Республика, г. Бишкек, "
                "микрорайон Асанбай, 52-а"
            ),
            "Saint Vladimir, Equal-to-the-Apostles",
            CENTRAL,
            rank="Cathedral",
        ),
        body(
            "kg-ru-bishkek-saint-olga",
            "Church of Saint Olga, Equal-to-the-Apostles, in Bishkek",
            (
                "Храм святой равноапостольной великой княгини Ольги "
                "(мкрн. Асанбай)"
            ),
            "Bishkek",
            (
                "720049, Кыргызская Республика, г. Бишкек, "
                "микрорайон Асанбай, 52-а"
            ),
            "Saint Olga, Equal-to-the-Apostles",
            CENTRAL,
        ),
        body(
            "kg-ru-leninskoye-nativity-theotokos",
            "Church of the Nativity of the Most Holy Theotokos in Leninskoye",
            "Храм Рождества Пресвятой Богородицы (с. Ленинское)",
            "Leninskoye",
            (
                "722173, Кыргызская Республика, Чуйская обл., "
                "Аламудунский р-н, с.Ленинское ул. Алма-Атинская, 246"
            ),
            "The Nativity of the Most Holy Theotokos",
            CENTRAL,
        ),
        body(
            "kg-ru-kant-protection-theotokos",
            "Church of the Protection of the Most Holy Theotokos in Kant",
            "Храм Покрова Пресвятой Богородицы (г. Кант)",
            "Kant",
            (
                "725000, Кыргызская Республика, Чуйская обл., "
                "Иссык-Атинский р-н, г.Кант, ул. Центральная, 42"
            ),
            "The Protection of the Most Holy Theotokos",
            CENTRAL,
        ),
        body(
            "kg-ru-novopokrovka-joy-all-who-sorrow",
            (
                "Church of the Joy of All Who Sorrow Icon of the Mother of "
                "God in Novopokrovka"
            ),
            (
                "Храм в честь иконы Божией Матери \"Всех скорбящих Радость\" "
                "(с. Ново-Покровка)"
            ),
            "Novopokrovka",
            (
                "722753, Кыргызская Республика, Чуйская обл-ть, "
                "Иссык-Атинский р-он, с. Ново-Покровка, ул. Ленина, 137"
            ),
            "The Joy of All Who Sorrow Icon of the Mother of God",
            CENTRAL,
        ),
        body(
            "kg-ru-manas-saint-john-kronstadt",
            "Church of Saint John of Kronstadt in Manas",
            "Храм во имя святого праведного Иоанна Кронштадтского (c. Манас)",
            "Manas",
            (
                "724815, Кыргызская Республика, Чуйская обл., "
                "Сокулукский р-н, с. Манас, ул. Заводская, 15"
            ),
            "Saint John of Kronstadt",
            CENTRAL,
        ),
        body(
            "kg-ru-vasilyevka-kazan-icon",
            "Church of the Kazan Icon of the Mother of God in Vasilyevka",
            "Храм в честь Казанской иконы Божией Матери (с. Васильевка)",
            "Vasilyevka",
            (
                "724308, Кыргызская Республика, Чуйская область, "
                "с. Васильевка, ул. Фрунзе, 114"
            ),
            "The Kazan Icon of the Mother of God",
            CENTRAL,
        ),
        body(
            "kg-ru-alamedin-tikhvin-icon",
            "Church of the Tikhvin Icon of the Mother of God in Alamedin",
            "Храм Тихвинской Иконы Божией Матери (с. Аламедин)",
            "Alamedin",
            (
                "Кыргызская Республика, Чуйская область, с. Аламедин, "
                "ул. Алматинская 82, 84"
            ),
            "The Tikhvin Icon of the Mother of God",
            CENTRAL,
        ),
        body(
            "kg-ru-kant-air-base-saint-alexander-nevsky",
            "Church of Saint Alexander Nevsky at Kant Air Base",
            (
                "Храм во имя святого благоверного великого князя Александра "
                "Невского, при Объединенной Российской военной базе ОДКБ "
                "\"КАНТ\""
            ),
            "Kant",
            (
                "725011, Кыргызская Республика, Чуйская область, "
                "Ыссык-Атинский район, ул. Полевая"
            ),
            "Saint Alexander Nevsky",
            CENTRAL,
        ),
        body(
            "kg-ru-sokuluk-descent-holy-spirit",
            "Church of the Descent of the Holy Spirit in Sokuluk",
            "Храм Сошествия Святого Духа (с. Сокулук)",
            "Sokuluk",
            (
                "722100, Кыргызская Республика, Чуйская обл. "
                "Сокулукский р-н, ул. Фрунзе, 216"
            ),
            "The Descent of the Holy Spirit",
            CENTRAL,
        ),
        body(
            "kg-ru-belovodskoye-archangel-michael",
            "Church of the Archangel Michael in Belovodskoye",
            "Храм Архистратига Божия Михаила (с. Беловодское)",
            "Belovodskoye",
            (
                "724600, Кыргызская Республика, Чуйская обл., "
                "Московский р-н, с. Беловодское, ул. Мира, 33"
            ),
            "The Archangel Michael",
            CENTRAL,
        ),
        body(
            "kg-ru-voyenno-antonovka-boris-gleb",
            "Church of the Right-Believing Princes Boris and Gleb in Voyenno-Antonovka",
            (
                "Храм во имя благоверных Князей Бориса и Глеба "
                "(с. Военно-Антоновка)"
            ),
            "Voyenno-Antonovka",
            (
                "722130, Кыргызская Республика, Чуйская обл., "
                "Сокулукский р-н, с. Военно-Антоновка, ул. Фрунзе, 112 А"
            ),
            "The Right-Believing Princes Boris and Gleb",
            CENTRAL,
        ),
        body(
            "kg-ru-chaldovar-protection-theotokos",
            "Church of the Protection of the Most Holy Theotokos in Chaldovar",
            "Храм Покрова Пресвятой Богородицы (с. Чалдовар)",
            "Chaldovar",
            (
                "722021, Кыргызская Республика, Чуйская обл., "
                "Фрунзенский р-н, с. Чалдовар, ул. Центральная, 275"
            ),
            "The Protection of the Most Holy Theotokos",
            CENTRAL,
        ),
        body(
            "kg-ru-sosnovka-saint-demetrius",
            "Church of Great Martyr Demetrius of Thessalonica in Sosnovka",
            (
                "Храм во имя святого великомученика Димитрия Солунского "
                "(с. Сосновка)"
            ),
            "Sosnovka",
            (
                "724421, Кыргызская Республика, Жайыльский район, "
                "с. Сосновка, ул. Фрунзе, 80"
            ),
            "Great Martyr Demetrius of Thessalonica",
            CENTRAL,
        ),
        body(
            "kg-ru-panfilovka-saint-nicholas",
            "Church of Saint Nicholas the Wonderworker in Panfilovka",
            "Храм во имя святителя Николая Чудотворца (с. Панфиловка)",
            "Panfilovka",
            (
                "724709, Кыргызская Республика, Чуйская обл., "
                "Панфиловский р-он, с. Панфиловка, ул. Центральная, 374"
            ),
            "Saint Nicholas the Wonderworker",
            CENTRAL,
        ),
        body(
            "kg-ru-kara-balta-kazan-icon",
            "Church of the Kazan Icon of the Mother of God in Kara-Balta",
            "Храм Казанской иконы Божией Матери г. Кара-Балта (с.Калининское)",
            "Kara-Balta",
            (
                "Кыргызская Республика, Чуйская обл., Жайыльский р-н, "
                "к. Кара-Балта, ул. Центральная, 156"
            ),
            "The Kazan Icon of the Mother of God",
            CENTRAL,
        ),
        body(
            "kg-ru-kara-balta-saint-spyridon-metochion",
            "Episcopal Metochion at the Church of Saint Spyridon in Kara-Balta",
            (
                "Архиерейское подворье при храме святителя Спиридона "
                "Тримифунтского г. Кара-Балта."
            ),
            "Kara-Balta",
            (
                "Кыргызская Республика, Чуйская обл., Жайыльский р-н, "
                "к. Кара-Балта, ул. Центральная, 164"
            ),
            "Saint Spyridon of Trimythous",
            CENTRAL,
            rank="Metochion",
        ),
    ],
    "talas": [
        body(
            "kg-ru-talas-saint-demetrius",
            "Church of Great Martyr Demetrius of Thessalonica in Talas",
            (
                "Храм во имя святого великомученика Димитрия Солунского "
                "(г. Талас)"
            ),
            "Talas",
            (
                "722200, Кыргызская Республика,Таласская обл., "
                "г. Талас, ул. Чынгыза Айтматова, 308"
            ),
            "Great Martyr Demetrius of Thessalonica",
            TALAS,
        ),
        body(
            "kg-ru-pokrovka-protection-mother-god",
            "Church of the Protection of the Mother of God in Pokrovka",
            "Храм Покрова Божьей Матери (с. Покровка)",
            "Pokrovka",
            (
                "724000, Кыргызская Республика, Таласская обл., "
                "Манасский р-н, с. Покровка, Улица: Жаманкулова, 164"
            ),
            "The Protection of the Mother of God",
            TALAS,
        ),
        body(
            "kg-ru-boo-terek-saint-nicholas",
            "Church of Saint Nicholas the Wonderworker in Boo-Terek",
            "Храм святителя Николая Чудотворца, село Боо - Терек (Ключёвка)",
            "Boo-Terek",
            (
                "Кыргызстан, Таласская область, Бакай-Атинский район, "
                "село Боо-Терек (Ключевка), ул. Ч. Сатаева № 122"
            ),
            "Saint Nicholas the Wonderworker",
            TALAS,
        ),
    ],
    "issyk_kul": [
        body(
            "kg-ru-karakol-holy-trinity",
            "Church of the Holy Trinity in Karakol",
            "Храм Пресвятой Троицы (г. Каракол)",
            "Karakol",
            (
                "Кыргызская Республика, Иссык-Кульская область, "
                "г. Каракол, ул. Гагарина, 16"
            ),
            "The Holy Trinity",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-teploklyuchenka-saint-demetrius",
            (
                "Church of Great Martyr Demetrius of Thessalonica in "
                "Teploklyuchenka"
            ),
            (
                "Храм во имя святого великомученика Димитрия Солунского "
                "(с. Теплоключенка)"
            ),
            "Teploklyuchenka",
            (
                "722347, Кыргызская Республика, Иссык-Кульская область, "
                "с. Теплоключенка, ул. Ленина, 95"
            ),
            "Great Martyr Demetrius of Thessalonica",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-tyup-kazan-icon",
            "Church of the Kazan Icon of the Mother of God in Tyup",
            "Храм в честь Казанской иконы Божией Матери (с. Тюп)",
            "Tyup",
            (
                "722330, Кыргызская Республика, Иссык-Кульская область "
                "с. Тюп, ул. Мокоева, 91"
            ),
            "The Kazan Icon of the Mother of God",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-ananyevo-saint-nicholas",
            "Church of Saint Nicholas the Wonderworker in Ananyevo",
            "Храм во имя святителя Николая Чудотворца (с. Ананьево/Сазановка)",
            "Ananyevo",
            (
                "722101, Кыргызская Республика, Иссык-Кульская область, "
                "с. Ананьево, пер. Советский, 21"
            ),
            "Saint Nicholas the Wonderworker",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-kyzyl-suu-protection-theotokos",
            (
                "Church of the Protection of the Most Holy Theotokos in "
                "Kyzyl-Suu"
            ),
            "Храм Покрова Пресвятой Богородицы (с. Кызыл-Суу или Покровка)",
            "Kyzyl-Suu",
            (
                "722400, Кыргызская Республика, Иссык-Кульская обл., "
                "Джеты-Огузский р-он, г. Кызыл-Суу, ул. Дзержинского, 38"
            ),
            "The Protection of the Most Holy Theotokos",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-balykchy-saint-xenia",
            "Church of Blessed Xenia of Saint Petersburg in Balykchy",
            (
                "Храм во имя святой блаженной Ксении Петербургской "
                "(г. Балыкчи)"
            ),
            "Balykchy",
            (
                "Кыргызская Республика, Иссык-Кульская область, "
                "г. Балыкчи, ул. Озерная, 145"
            ),
            "Blessed Xenia of Saint Petersburg",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-cholpon-ata-hieromartyr-benjamin",
            "Church of Hieromartyr Benjamin of Petrograd in Cholpon-Ata",
            (
                "Храм во имя священномученика Вениамина, митрополита "
                "Петроградского (г. Чолпон-Ата)"
            ),
            "Cholpon-Ata",
            (
                "722100, Кыргызская Республика, Иссык-Кульская область "
                "г. Чолпон-Ата, ул. Комарова, 4"
            ),
            "Hieromartyr Benjamin, Metropolitan of Petrograd",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-grigorievka-protection-theotokos",
            (
                "Church of the Protection of the Most Holy Theotokos in "
                "Grigorievka"
            ),
            "Храм Покрова Пресвятой Богородицы (с. Григорьевка)",
            "Grigorievka",
            (
                "Кыргызская Республика, Иссык-Кульская область, "
                "с. Григорьевка, ул. Садыр-Аке, 27"
            ),
            "The Protection of the Most Holy Theotokos",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-semenovka-archangel-michael",
            "Church of the Archangel Michael in Semenovka",
            "Храм Архангела Михаила (с. Семеновка)",
            "Semenovka",
            (
                "722118, Кыргызская Республика, Иссык-Кульская область "
                "с. Семеновка, ул. Алма-Кучукова, 68"
            ),
            "The Archangel Michael",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-tamga-saint-dimitry-donskoy",
            "Church of Saint Dimitry Donskoy in Tamga",
            (
                "Храм во имя святого благоверного Князя Димитрия Донского "
                "(с. Тамга)"
            ),
            "Tamga",
            (
                "Кыргызская Республика, Иссык-Кульская область, "
                "Джети-Огузский район, с. Тамга, ул.Докомбаева, 21"
            ),
            "Saint Dimitry Donskoy",
            ISSYK_KUL,
        ),
        body(
            "kg-ru-przhevalsk-nativity-christ-prayer-room",
            "Nativity of Christ Prayer Room in Przhevalsk",
            "Молельная комната в честь Рождества Христова",
            "Przhevalsk",
            "Кыргызская Республика, Иссык-Кульская область, г. Пржевальск",
            "The Nativity of Christ",
            ISSYK_KUL,
            rank="Prayer Room",
        ),
        body(
            "kg-ru-balykchy-iveron-monastery",
            "Iveron Women's Monastery in Balykchy",
            (
                "Иверский женский монастырь г. Балыкчи, Иссык-Кульской "
                "области Республики Кыргызстан."
            ),
            "Balykchy",
            (
                "Кыргызская Республика, иссык-Кульская обл., "
                "г. Балыкчи, ул. Озёрная, 268"
            ),
            "The Iveron Icon of the Mother of God",
            ISSYK_KUL,
            rank="Convent",
            kind="monastery",
        ),
    ],
    "osh": [
        body(
            "kg-ru-osh-archangel-michael",
            "Church of the Archangel Michael in Osh",
            "Храм Архистратига Божия Михаила (г.Ош)",
            "Osh",
            "714000, Кыргызская Республика, г. Ош, ул. Курманжан-Датки, 219",
            "The Archangel Michael",
            OSH,
        ),
        body(
            "kg-ru-jalal-abad-dormition-mother-god",
            "Church of the Dormition of the Mother of God in Jalal-Abad",
            "Храм Успения Божией Матери (г. Джалал-Абад)",
            "Jalal-Abad",
            (
                "715600, Кыргызская Республика, Джалал-Абадская обл., "
                "г. Джалал-Абад, ул. Нагимы Айтматовой, 34"
            ),
            "The Dormition of the Mother of God",
            OSH,
        ),
        body(
            "kg-ru-kurshab-protection-theotokos",
            "Church of the Protection of the Most Holy Theotokos in Kurshab",
            "Храм Покрова Пресвятой Богородицы (с. Куршаб)",
            "Kurshab",
            (
                "715160, Кыргызская Республика, Ошская область, "
                "Узгенский район, с.Куршаб, ул. Ленина, б/н."
            ),
            "The Protection of the Most Holy Theotokos",
            OSH,
        ),
        body(
            "kg-ru-kyzyl-kiya-prophet-elijah",
            "Church of the Prophet Elijah in Kyzyl-Kiya",
            "Храм пророка Божия Илии (г. Кызыл-Кия)",
            "Kyzyl-Kiya",
            (
                "Кыргызская Республика, Ошская область, Кадамжайский р-он, "
                "г. Кызыл-Кия, ул. Советская, 28"
            ),
            "The Prophet Elijah",
            OSH,
        ),
        body(
            "kg-ru-kara-kul-saint-seraphim",
            "Church of Saint Seraphim of Sarov in Kara-Kul",
            "Храм во имя преподобного Серафима Саровского (г. Кара-Куль)",
            "Kara-Kul",
            "Кыргызская Республика, Джалал-Абадская область, г. Кара-Куль",
            "Saint Seraphim of Sarov",
            OSH,
        ),
        body(
            "kg-ru-mailuu-suu-vladimir-icon",
            "Church of the Vladimir Icon of the Mother of God in Mailuu-Suu",
            (
                "Храм в честь Владимирской иконы Божией Матери "
                "(г. Майлуу - Суу)"
            ),
            "Mailuu-Suu",
            (
                "Кыргызская Республика, Джалал-Абадская область, "
                "г. Майлуу-Суу, ул. Ташкентская, 93"
            ),
            "The Vladimir Icon of the Mother of God",
            OSH,
        ),
        body(
            "kg-ru-kok-janggak-nativity-theotokos",
            "Church of the Nativity of the Most Holy Theotokos in Kok-Janggak",
            "Храм Рождества Пресвятой Богородицы (г. Кок-Енгаг)",
            "Kok-Janggak",
            (
                "720901, Кыргызская Республика, Жалалабадская область, "
                "г. Кок-Енгак, ул. Ленина, 66."
            ),
            "The Nativity of the Most Holy Theotokos",
            OSH,
        ),
        body(
            "kg-ru-sulukta-protection-theotokos",
            "Church of the Protection of the Most Holy Theotokos in Sulukta",
            "Храм Покрова Пресвятой Богородицы (г. Сулюкта)",
            "Sulukta",
            (
                "718002, Кыргызская Республика, Баткенская область, "
                "г. Сулюкта, ул. Каркасная, б/н."
            ),
            "The Protection of the Most Holy Theotokos",
            OSH,
        ),
        body(
            "kg-ru-khaidarkan-tikhvin-icon-chapel",
            "Chapel of the Tikhvin Icon of the Mother of God in Khaidarkan",
            "Часовня в честь Тихвинской иконы Божией Матери (п. Хайдаркен)",
            "Khaidarkan",
            (
                "Кыргызская Республика, Баткенская область, "
                "г. Хайдаркан, ул. Центральная б/н."
            ),
            "The Tikhvin Icon of the Mother of God",
            OSH,
            rank="Chapel",
        ),
        body(
            "kg-ru-kadamjay-iveron-icon-prayer-room",
            "Iveron Icon of the Mother of God Prayer Room in Kadamjay",
            (
                "Молельная комната в честь Иверской иконы Божией Матери "
                "(п. Кадамжай)"
            ),
            "Kadamjay",
            "Кыргызская Республика, п. Кадамжай",
            "The Iveron Icon of the Mother of God",
            OSH,
            rank="Prayer Room",
        ),
    ],
    "chuy_tokmok": [
        body(
            "kg-ru-tokmok-saint-george",
            "Church of Great Martyr George the Victory-Bearer in Tokmok",
            (
                "Храм святого великомученика Георгия Победоносца "
                "(г. Чуй-Токмок)"
            ),
            "Tokmok",
            (
                "Кыргызская Республика, Чуйская область, "
                "г. Чуй-Токмок, ул. Трясина, 118"
            ),
            "Great Martyr George the Victory-Bearer",
            CHUY_TOKMOK,
        ),
        body(
            "kg-ru-tash-tyube-protection-theotokos",
            (
                "Church of the Protection of the Most Holy Theotokos in "
                "Tash-Tyube"
            ),
            (
                "Храм Покрова Пресвятой Богородицы "
                "(с. Таш-Тюбе или Воронцовка)"
            ),
            "Tash-Tyube",
            (
                "722165, Кыргызская Республика, Чуйская обл., "
                "Аламединский район, с. Таш-Тюбе, ул. Школьная, 37"
            ),
            "The Protection of the Most Holy Theotokos",
            CHUY_TOKMOK,
        ),
        body(
            "kg-ru-orlovka-kazan-icon",
            "Church of the Kazan Icon of the Mother of God in Orlovka",
            "Храм в честь Казанской иконы Божией Матери (г. Орловка)",
            "Orlovka",
            (
                "724517, Кыргызская Республика, Чуйская область "
                "Кеминский район, г. Орловка, ул. Арычная, 106"
            ),
            "The Kazan Icon of the Mother of God",
            CHUY_TOKMOK,
        ),
        body(
            "kg-ru-ivanovka-saint-john-theologian",
            "Church of Saint John the Theologian in Ivanovka",
            (
                "Храм во имя святого апостола и евангелиста Иоанна "
                "Богослова (с. Ивановка)"
            ),
            "Ivanovka",
            (
                "722221, Кыргызская Республика, Чуйская обл. "
                "Иссык-Атинский р-он, с. Ивановка, ул. Почтовая, 85"
            ),
            "Saint John the Apostle and Evangelist",
            CHUY_TOKMOK,
        ),
        body(
            "kg-ru-kemin-protection-theotokos",
            "Church of the Protection of the Most Holy Theotokos in Kemin",
            "Храм Покрова Пресвятой Богородицы (г. Кемин)",
            "Kemin",
            (
                "724500, Кыргызская Республика, Чуйская обл, "
                "Кеминский район, с. Кемин, ул. Панфилова, 48"
            ),
            "The Protection of the Most Holy Theotokos",
            CHUY_TOKMOK,
        ),
        body(
            "kg-ru-krasnaya-rechka-saint-seraphim",
            "Church of Saint Seraphim of Sarov in Krasnaya Rechka",
            (
                "Храм во имя преподобного Серафима Саровского "
                "(с. Красная речка)"
            ),
            "Krasnaya Rechka",
            (
                "725019, Кыргызская Республика, Чуйская обл., "
                "Иссык-Атинский р-н, с. Красная Речка, ул. Бирюкова, 1 А"
            ),
            "Saint Seraphim of Sarov",
            CHUY_TOKMOK,
        ),
    ],
    "current_news": [
        body(
            "kg-ru-ak-bulun-holy-trinity-monastery",
            "Holy Trinity Monastery in Ak-Bulun",
            "Свято-Троицкий монастырь в селе Ак-Булун (Светлый Мыс)",
            "Ak-Bulun",
            None,
            "The Holy Trinity",
            [AK_BULUN_FEAST, AK_BULUN_PILGRIMAGE, AK_BULUN_PROGRAMME],
            rank="Monastery",
            kind="monastery",
        ),
    ],
}

EXPECTED_GROUPS = {
    "central": 18,
    "talas": 3,
    "issyk_kul": 12,
    "osh": 10,
    "chuy_tokmok": 6,
    "current_news": 1,
}
EXPECTED_TOTAL = 50
EXPECTED_KINDS = {"parish": 48, "monastery": 2}
ALLOWED_RANKS = {
    "Cathedral",
    "Church",
    "Chapel",
    "Prayer Room",
    "Metochion",
    "Convent",
    "Monastery",
}

ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in GROUPS.values()
    for row in rows
}
ENGLISH_SEATS = {
    row["seat"]: row["seat"]
    for rows in GROUPS.values()
    for row in rows
}

FORBIDDEN_PUNCTUATION = (
    "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d",
    "\u00ab", "\u00bb", "\ufffd",
)
CONTACT_RE = re.compile(r"(?:контакт|тел(?:ефон)?|e-?mail|@|\+996)", re.I)


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
    for key in ("address", "languages", "founded"):
        if row.get(key) and (
                not isinstance(row[key], list) or
                not all(isinstance(value, str) for value in row[key])):
            raise ValueError("%s has invalid %s" % (row.get("id"), key))
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in FORBIDDEN_PUNCTUATION):
        raise ValueError("%s carries forbidden punctuation" % row.get("id"))
    if CONTACT_RE.search(" ".join(row.get("address") or [])):
        raise ValueError("%s leaks contact prose into its address" % row.get("id"))
    if row.get("checked") != CHECKED:
        raise ValueError("%s carries the wrong checked date" % row.get("id"))
    return row


def build():
    rows = []
    seen_ids = {"ru-bishkek"}
    seen_names = {}
    kind_counts = {kind: 0 for kind in EXPECTED_KINDS}
    for group, source_rows in GROUPS.items():
        if len(source_rows) != EXPECTED_GROUPS[group]:
            raise ValueError("%s must contain exactly %d source rows" % (
                group, EXPECTED_GROUPS[group],
            ))
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen_ids:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if row.get("parent") != "ru-bishkek":
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if row.get("country") != "KG":
                raise ValueError("%s is outside Kyrgyzstan" % row_id)
            if row.get("kind") not in EXPECTED_KINDS:
                raise ValueError("%s has an unsupported kind" % row_id)
            if row.get("rank") not in ALLOWED_RANKS:
                raise ValueError("%s has an unsupported rank" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            if not row.get("dedication"):
                raise ValueError("%s lacks its published dedication" % row_id)
            name_key = row["name"].casefold()
            if name_key in seen_names:
                raise ValueError("duplicate reader-facing name: %s and %s" % (
                    seen_names[name_key], row_id,
                ))
            seen_names[name_key] = row_id
            seen_ids.add(row_id)
            kind_counts[row["kind"]] += 1
            rows.append(row)
    if len(rows) != EXPECTED_TOTAL:
        raise ValueError("Kyrgyzstan must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if kind_counts != EXPECTED_KINDS:
        raise ValueError("Kyrgyzstan kind counts changed: %s" % kind_counts)
    if set(ENGLISH_NAMES) != seen_ids - {"ru-bishkek"}:
        raise ValueError("Kyrgyzstan English name map is out of sync")
    return {
        "ru-bishkek": {
            "v": 1,
            "parent": "ru-bishkek",
            "country": "KG",
            "rows": rows,
        }
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dump", action="store_true")
    args = parser.parse_args()
    try:
        payloads = build()
    except (OSError, ValueError) as exc:
        print("directory Kyrgyzstan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print(
        "Kyrgyzstan: 50 current bodies under the Bishkek Diocese "
        "(48 parish bodies and 2 monasteries)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
