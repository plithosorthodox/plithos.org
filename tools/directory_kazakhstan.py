#!/usr/bin/env python3
"""Current canonical Eastern Orthodox worship bodies in Kazakhstan.

The rows are confined to exact named bodies on current official Church
rosters. Aggregate counts, construction notices, historical churches, and
uncertain bodies stay in tools/directory_candidates/kazakhstan.json.

    python tools/directory_kazakhstan.py --check
    python tools/directory_kazakhstan.py --dump
"""

import argparse
import json
import re
import sys


CHECKED = "2026-11-15"

MITROPOLIA = "https://mitropolia.kz/info/organizations/churches/"
MITROPOLIA_MONASTERIES = "https://mitropolia.kz/info/organizations/monasteries.html"
AKTOBE_A = "https://aktobe-eparhiya.kz/aktyubinskoe-blagochinie/"
AKTOBE_K = "https://aktobe-eparhiya.kz/kyzylordinskoe-blagochinie/"
KARAGANDA = "https://eparhia.kz/node/25"
SHAKHTINSK = "https://eparhia.kz/node/31"
KARAGANDA_NEW = "https://eparhia.kz/news/troitse-sevastianovskij-sobor"
KOKSHETAU = "https://pravest-kokshe.kz/temples/318-Hramy_Kokshetauskoy_i_Akmolinskoy_Eparhii_202"
KOKSHETAU_CATHEDRAL = "https://pravest-kokshe.kz/Raspisanie_bogoslugheniy/3176-Raspisanie_bogoslugheniy_v_kafedralynom_sobore_Voskreseniya_Hristova_na_9-15_marta_2026_goda.html"

ROWS = {
    parent: [] for parent in (
        "ru-aktobe", "ru-astana", "ru-karaganda", "ru-kokshetau",
        "ru-kostanay", "ru-pavlodar", "ru-petropavl-and-bulayevo",
        "ru-taldykorgan-vicariate", "ru-uralsk", "ru-ust-kamenogorsk",
        "ru-shymkent",
    )
}


def add_block(parent, source, text):
    """Add pipe-delimited static rows sharing one official roster source."""
    sources = [source] if isinstance(source, str) else list(source)
    for raw in text.strip().splitlines():
        slug, rank, kind, name, local = raw.split("|", 4)
        ROWS[parent].append({
            "id": "kz-" + slug,
            "parent": parent,
            "kind": kind,
            "rank": rank,
            "name": name,
            "local": local,
            "country": "KZ",
            "sources": sources,
        })


add_block("ru-astana", MITROPOLIA + "almaty.html", """
ru-astana-almaty-ascension|Cathedral Parish|parish|Ascension Cathedral in Almaty|Кафедральный собор в честь Вознесения Господня, город Алма-Ата
ru-astana-almaty-saint-nicholas|Cathedral Parish|parish|Saint Nicholas Cathedral in Almaty|Собор во имя святителя Николая, архиепископа Мир Ликийских, чудотворца, город Алма-Ата
ru-astana-almaty-kazan-icon|Cathedral Parish|parish|Kazan Icon of the Mother of God Cathedral in Almaty|Собор в честь иконы Божией Матери «Казанская», город Алма-Ата
ru-astana-almaty-faith-hope-love-sophia|Cathedral Parish|parish|Holy Martyrs Faith, Hope, Love, and Sophia Cathedral in Almaty|Собор во имя святых мучениц Веры, Надежды, Любови и матери их Софии, город Алма-Ата
ru-astana-akbulak-nativity-christ|Cathedral Parish|parish|Nativity of Christ Cathedral in Akbulak|Собор в честь Рождества Христова, поселок Акбулак. (Алма-Ата)
ru-astana-almaty-protection|Church|parish|Protection of the Most Holy Theotokos Church in Almaty|Храм в честь Покрова Пресвятой Богородицы, город Алма-Ата
ru-astana-kosmos-life-giving-spring|Church|parish|Life-Giving Spring Icon of the Mother of God Church in Kosmos|Храм в честь иконы Божией Матери «Живоносный источник», поселок Космос
ru-astana-almaty-theophany|Church|parish|Theophany Church in Almaty|Храм в честь Богоявления Господня, город Алма-Ата
ru-astana-karabulak-royal-passion-bearers|Church|parish|Royal Passion-Bearers Church in Karabulak|Храм в честь царственных страстотерпцев, поселок Карабулак
ru-astana-almaty-peter-paul|Church|parish|Holy Apostles Peter and Paul Church in Almaty|Храм святых апостолов Петра и Павла, город Алма-Ата
ru-astana-almaty-paraskeva|Church|parish|Great Martyr Paraskeva Church in Almaty|Храм во имя святой великомученицы Параскевы Пятницы, город Алма-Ата
ru-astana-almaty-alexander-nevsky|Church|parish|Saint Alexander Nevsky Church in Almaty|Храм святого блговерного князя Александра Невского
""")

add_block("ru-astana", MITROPOLIA + "almaty.html?start=12", """
ru-astana-almaty-joy-all-sorrow|Church|parish|Joy of All Who Sorrow Icon of the Mother of God Church in Almaty|Храм в честь иконы Божией Матери «Всех скорбящих Радосте», город Алма-Ата
ru-astana-almaty-saint-philaret-seminary|Church|parish|Saint Philaret of Moscow Church at the Almaty Orthodox Theological Seminary|Храм во имя святителя Филарета Московского при Алма-Атинской православной духовной семинарии, город Алма-Ата
ru-astana-almaty-exaltation-cross|Church|parish|Exaltation of the Cross Church in Almaty|Храм в честь Воздвижения Креста Господня, город Алма-Ата
ru-astana-almaty-cosmas-damian|Church|parish|Saints Cosmas and Damian Church in Almaty|Храм во имя святых Космы и Дамиана, город Алма-Ата
ru-astana-alatau-annunciation|Church|parish|Annunciation of the Most Holy Theotokos Church in Alatau|Храм в честь Благовещения Пресвятой Богородицы, поселок Алатау (Алма-Ата)
ru-astana-almaty-john-theologian|Church|parish|Holy Apostle and Evangelist John the Theologian Church in Almaty|Храм во имя святого апостола и евангелиста Иоанна Богослова, город Алма-Ата
ru-astana-koldi-saint-elizabeth|Church|parish|Holy Martyr Grand Duchess Elizabeth Church in Koldi|Храм во имя святой преподобномученицы великой княгини Елисаветы, поселок Колди
ru-astana-almaty-bishops-house-iveron|House Church|parish|Iveron Icon of the Mother of God House Church at the Bishop's Residence in Almaty|Домовой храм Архиерейского дома в честь Иверской иконы Божией Матери, город Алма-Ата
ru-astana-kosozen-inexhaustible-chalice|Church|parish|Inexhaustible Chalice Icon of the Mother of God Church in Kosozen|Храм в честь иконы Божией Матери «Неупиваемая Чаша», село Косозен
ru-astana-akzhar-nativity-theotokos|Church|parish|Nativity of the Most Holy Theotokos Church in Akzhar|Храм в честь Рождества Пресвятой Богородицы, поселок Акжар
ru-astana-baganashil-saint-vladimir|Church|parish|Saint Vladimir Church in Baganashil|Храм во имя святого равноапостольного великого князя Владимира, поселок Баганашил
ru-astana-baganashil-hieromartyr-pimen|Chapel|parish|Hieromartyr Pimen of Verny and Semirechye Chapel in Baganashil|Часовня священномученика Пимена, епископа Верненского и Семиреченского, Баганашил
""")

add_block("ru-astana", MITROPOLIA + "almaty.html?start=24", """
ru-astana-kunaev-xenia|Church|parish|Blessed Xenia of Petersburg Church in Kunaev|Храм во имя святой блаженной Ксении Петербургской, город Кунаев
ru-astana-guldala-john-baptist|Church|parish|Nativity of Saint John the Baptist Church in Guldala|Храм в честь Рождества Иоанна Предтечи, поселок Гульдала
""")

add_block("ru-astana", "https://mitropolia.kz/archbishop/worship/13835-v-den-pamyati-ravnoapostolnoj-niny-v-alma-ate-molitvenno-otmetili-10-letie-osvyashcheniya-khrama-svyatoj-prosvetitelnitsy-gruzii.html", """
ru-astana-almaty-saint-nina|Church|parish|Saint Nina, Enlightener of Georgia Church in Almaty|храм во имя святой равноапостольной Нины
""")

add_block("ru-astana", "https://mitropolia.kz/news/patriarch/13259-svyatejshij-patriarkh-kirill-sovershil-osvyashchenie-khrama-prepodobnogo-sergiya-radonezhskogo-v-astane.html", """
ru-astana-city-sergius-radonezh|Church|parish|Saint Sergius of Radonezh Church in Astana|храм преподобного Сергия Радонежского в Астане
""")

add_block("ru-astana", "https://mitropolia.kz/archbishop/worship/13754-glava-mitropolichego-okruga-vozglavil-prestolnye-torzhestva-alma-atinskogo-khrama-v-chest-sobora-presvyatoj-bogoroditsy-3.html", """
ru-astana-almaty-synaxis-theotokos|Church|parish|Synaxis of the Most Holy Theotokos Church in Almaty|храм в честь Собора Пресвятой Богородицы города Алма-Аты
""")

add_block("ru-astana", MITROPOLIA + "astana.html", """
ru-astana-city-dormition|Cathedral Parish|parish|Dormition of the Most Holy Theotokos Cathedral in Astana|Кафедральный собор в честь Успения Пресвятой Богородицы, город Астана
ru-astana-city-constantine-helen|Cathedral Parish|parish|Saints Constantine and Helen Cathedral in Astana|Собор во имя святых равноапостольных царя Константина и матери его Елены, город Астана
ru-astana-city-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Astana|Храм во имя святого преподобного Серафима Саровского, город Астана
ru-astana-city-alexander-nevsky|Church|parish|Saint Alexander Nevsky Monastery Church in Astana|Монастырский храм во имя святого благоверного князя Александра Невского, город Астана
ru-astana-vozdvizhenka-exaltation-cross|Church|parish|Exaltation of the Cross Church in Vozdvizhenka|Храм в честь Воздвижения Креста Господня, село Воздвиженка
ru-astana-rodina-john-baptist|Church|parish|Saint John the Baptist Church in Rodina|Храм во имя святого Предтечи и Крестителя Господня Иоанна, село Родина
ru-astana-malotimofeevka-saint-nicholas|Church|parish|Saint Nicholas Church in Malotimofeevka|Храм во имя святителя Николая, архиепископа Мир Ликийских, чудотворца. Село Малотимофеевка
ru-astana-akmol-new-martyrs|Church|parish|New Martyrs and Confessors of Akmola Church in Akmol|Храм новомучеников и исповедников Акмолинских, село Акмол
""")

add_block("ru-astana", MITROPOLIA + "ili.html", """
ru-astana-kemel-dormition|Church|parish|Dormition of the Most Holy Theotokos Church in Kemel|Храм в честь Успения Пресвятой Богородицы, микрорайон Кемел
ru-astana-tuymebaeva-sergius-radonezh|Church|parish|Saint Sergius of Radonezh Church in Tuymebaeva|Храм во имя святого преподобного Сергия Радонежского, поселок Туймебаева
ru-astana-zhetygen-john-kronstadt|Church|parish|Saint John of Kronstadt Church in Zhetygen|Храм во имя святого праведного Иоанна Кронштадтского, поселок Жетыген
ru-astana-karaoy-prophet-elijah|Church|parish|Prophet Elijah Church in Karaoy|Храм во имя святого пророка Божия Илии, поселок Караой
ru-astana-boralday-iveron-icon|Church|parish|Iveron Icon of the Mother of God Church in Boralday|Храм в честь Иверской иконы Божией Матери, поселок Боралдай
ru-astana-mezhdurechenskoe-saint-nicholas|Church|parish|Saint Nicholas Church in Mezhdurechenskoe|Храм во имя святителя Николая, архиепископа Мир Ликийских, чудотворца, село Междуреченское
ru-astana-chapaevo-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Chapaevo|Храм во имя святого преподобного Серафима Саровского, поселок Чапаево
ru-astana-baiserke-demetrius|Church|parish|Saint Demetrius of Thessalonica Church in Baiserke|Храм во имя святого великомученика Димитрия Солунского, поселок Байсерке
ru-astana-zarechnoe-prophet-elijah|Church|parish|Prophet Elijah Church in Zarechnoe|Храм во имя святого пророка Божия Илии, село Заречное
""")

add_block("ru-astana", MITROPOLIA + "uzun-agash.html", """
ru-astana-uzyn-agash-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Uzyn-Agash|Храм в честь Казанской иконы Божией Матери, село Узын-Агаш
ru-astana-kaskelen-archangel-michael|Church|parish|Archangel Michael Church in Kaskelen|Храм во имя святого Архистратига Божия Михаила, город Каскелен
ru-astana-irgeli-nicholas-almaty|Church|parish|Saint Nicholas of Almaty and Kazakhstan Church in Irgeli|Храм во имя святителя Николая Алма-Атинского и Казахстанского, исповедника, село Иргели
ru-astana-chemolgan-vladimir-icon|Church|parish|Vladimir Icon of the Mother of God Church at Chemolgan Station|Храм в честь Владимирской иконы Божией Матери, станция Чемолган
ru-astana-kargaly-saint-tikhon|Church|parish|Saint Tikhon, Patriarch of All Russia Church in Kargaly|Храм во имя святителя Тихона, Патриарха Всероссийского, поселок Каргалы
ru-astana-chemolgan-protection|Church|parish|Protection of the Most Holy Theotokos Church in Chemolgan|Храм в честь Покрова Пресвятой Богородицы, село Чемолган
ru-astana-mynbaeva-john-theologian|Church|parish|Apostle and Evangelist John the Theologian Church in Mynbaeva|Храм апостола и евангелиста Иоанна Богослова, поселок Мынбаева
ru-astana-zhalpaksay-holy-trinity|Church|parish|Holy Trinity Church in Zhalpaksay|Храм в честь Пресвятой Троицы, посёлок Жалпаксай
""")

add_block("ru-astana", MITROPOLIA + "issyk.html", """
ru-astana-issyk-protection|Church|parish|Protection of the Most Holy Theotokos Church in Issyk|Храм в честь Покрова Пресвятой Богородицы, город Иссык
ru-astana-turgen-archangel-michael|Church|parish|Archangel Michael Church in Turgen|Храм во имя святого Архистратига Божия Михаила, село Тургень
ru-astana-talgar-saint-nicholas|Church|parish|Saint Nicholas Church in Talgar|Храм во имя святителя Николая, архиепископа Мир Ликийских, чудотворца, город Талгар
ru-astana-panfilova-assuage-sorrows|Church|parish|Assuage My Sorrows Icon of the Mother of God Church in Panfilova|Храм в честь иконы Божией Матери «Утоли моя печали», поселок Панфилова
ru-astana-talgar-paraskeva|Church|parish|Great Martyr Paraskeva Church in Talgar|Храм во имя святой великомученицы Параскевы Пятницы, город Талгар
ru-astana-shelek-demetrius|Church|parish|Saint Demetrius of Thessalonica Church in Shelek|Храм во имя святого великомученика Димитрия Солунского, село Шелек
ru-astana-belbulak-saint-george|Church|parish|Saint George the Victory-Bearer Church in Belbulak|Храм во имя святого великомученика и победоносца Георгия, село Бельбулак
ru-astana-baidibek-bi-theophany|Church|parish|Theophany Church in Baidibek Bi|Храм в честь Богоявления Господня, село Байдибек би
ru-astana-baiterek-saint-alexis|Church|parish|Saint Alexis, Metropolitan of Moscow Church in Baiterek|Храм во имя святителя Алексия, митрополита Московского, чудотворца, село Байтерек
ru-astana-saimasai-alexander-nevsky|Church|parish|Saint Alexander Nevsky Church in Saimasai|Храм во имя святого благоверного князя Александра Невского, село Саймасай
""")

add_block("ru-astana", MITROPOLIA + "zharkent.html", """
ru-astana-taldybulak-holy-trinity|Church|parish|Holy Trinity Church in Taldybulak|Храм в честь Святой Троицы, село Талдыбулак
ru-astana-zharkent-prophet-elijah|Church|parish|Prophet Elijah Church in Zharkent|Храм во имя Пророка Божия Илии, город Жаркент
ru-astana-chundzha-new-martyrs-kazakhstan|House Church|parish|New Martyrs and Confessors of Kazakhstan House Church in Chundzha|Домовой храм в честь новомучеников и исповедников Казахстанских, село Чунджа
ru-astana-koktal-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Koktal|Храм в честь Казанской иконы Божией Матери, село Коктал
ru-astana-taskarasu-bogolyubovo-icon|Parish|parish|Bogolyubovo Icon of the Mother of God Parish in Taskarasu|Приход в честь Боголюбской иконы Божией Матери, поселок Таскарасу
""")

add_block("ru-taldykorgan-vicariate", MITROPOLIA + "taldykorgan.html", """
ru-taldykorgan-city-john-theologian|Cathedral Parish|parish|Apostle and Evangelist John the Theologian Cathedral in Taldykorgan|Собор во имя святого апостола и евангелиста Иоанна Богослова, город Талдыкорган
ru-taldykorgan-city-archangel-gabriel|Church|parish|Archangel Gabriel Church in Taldykorgan|Храм во имя святого архангела Гавриила, город Талдыкорган
ru-taldykorgan-tekeli-holy-trinity|Church|parish|Holy Trinity Church in Tekeli|Храм во имя Пресвятой Троицы, город Текели
ru-taldykorgan-karabulak-abala-sign-icon|Church|parish|Abalatsk Sign Icon of the Mother of God Church in Karabulak|Храм в честь Абалацкой иконы Божией Матери «Знамение», поселок Карабулак
ru-taldykorgan-balpyk-bi-presentation|Church|parish|Presentation of the Lord Church in Balpyk Bi|Храм в честь Сретения Господня, поселок Балпык Би
ru-taldykorgan-kabanbai-nativity-theotokos|Church|parish|Nativity of the Most Holy Theotokos Church in Kabanbai|Храм в честь Рождества Пресвятой Богородицы, аул Кабанбай
ru-taldykorgan-tokzhailau-transfiguration|Church|parish|Transfiguration of the Lord Church in Tokzhailau|Храм в честь Преображения Господня, поселок Токжайлау
ru-taldykorgan-kogaly-saint-nicholas|Church|parish|Saint Nicholas Church in Kogaly|Храм во имя святителя Николая, архиепископа Мир Ликийских, чудотворца, село Когалы
ru-taldykorgan-ush-aral-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Ush-Aral|Храм в честь Казанской иконы Божией Матери, город Уш-Арал
ru-taldykorgan-sarkand-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Sarkand|Храм в честь иконы Казанской Божией Матери, город Сарканд
ru-taldykorgan-ushtobe-archangel-michael|Prayer House|parish|Archangel Michael Prayer House in Ushtobe|Молитвенный дом во имя святого Архистратига Божия Михаила, город Уштобе
""")

add_block("ru-astana", MITROPOLIA_MONASTERIES, """
ru-astana-kaskelen-seraphim-theognostus-hermitage|Hermitage|monastery|Saints Seraphim and Theognostus of Almaty Hermitage in Kaskelen|Мужская пустынь во имя святых преподобномучеников Серафима и Феогноста Алма-Атинских, город Каскелен
ru-astana-issyk-silouan-hermitage|Hermitage|monastery|Saint Silouan the Athonite Hermitage in Issyk|Мужская пустынь во имя святого преподобного Силуана Афонского, город Иссык
ru-astana-almaty-iveron-seraphim-convent|Convent|monastery|Iveron-Seraphim Convent in Almaty|Иверско-Серафимовский женский монастырь
ru-astana-seeking-lost-convent|Convent|monastery|Seeking the Lost Icon of the Mother of God Convent|Монастырь в честь иконы Божией Матери «Взыскание погибших»
""")

add_block("ru-aktobe", AKTOBE_A, """
ru-aktobe-city-saint-nicholas|Cathedral Parish|parish|Saint Nicholas Cathedral in Aktobe|Свято-Никольский Кафедральный Собор г.Актобе.
ru-aktobe-city-archangel-michael|Church|parish|Archangel Michael Church in Aktobe|Храм Архангела Михаила г.Актобе.
ru-aktobe-city-prince-vladimir|Church|parish|Saint Vladimir Church in Aktobe|Храм св.равноапостольного великого князя Владимира г. Актобе.
ru-aktobe-khromtau-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Khromtau|Храм преподобного Серафима Саровского г. Хромтау.
ru-aktobe-alga-holy-trinity|Church|parish|Holy Trinity Church in Alga|Храм св. Троицы г. Алга.
ru-aktobe-temir-dormition|Church|parish|Dormition of the Mother of God Church in Temir|Храм Успения Божией Матери г. Темир.
ru-aktobe-martuk-protection|Church|parish|Protection of the Mother of God Church in Martuk|Храм Покрова Божией Матери п. Мартук.
ru-aktobe-martuk-softener-evil-hearts|Church|parish|Softener of Evil Hearts Icon of the Mother of God Church in Martuk|Храм иконы Божией Матери «Умягчение злых сердец» п. Мартук.
""")

add_block("ru-aktobe", AKTOBE_K, """
ru-aktobe-kyzylorda-kazan-icon|Cathedral Parish|parish|Kazan Icon of the Mother of God Cathedral in Kyzylorda|Кафедральный Собор Казанской иконы Божией Матери г. Кызылорда.
ru-aktobe-baikonur-saint-george|Church|parish|Saint George the Victory-Bearer Church in Baikonur|Храм великомученика Георгия Победоносца г. Байконур.
""")

add_block("ru-karaganda", KARAGANDA, """
ru-karaganda-city-entry-theotokos|Cathedral Parish|parish|Entry of the Theotokos Cathedral in Karaganda|Караганда Введенский кафедральный собор
ru-karaganda-city-archangel-michael|Cathedral Parish|parish|Archangel Michael Cathedral in Karaganda|Караганда Михаило-Архангельский собор
ru-karaganda-city-nativity-theotokos-monastery|Monastery|monastery|Nativity of the Theotokos Monastery in Karaganda|Караганда Богородице-Рождественский монастырь
ru-karaganda-city-annunciation|Church|parish|Annunciation Church in Karaganda|Караганда Благовещенский храм
ru-karaganda-city-exaltation-cross|Church|parish|Exaltation of the Cross Church in Karaganda|Караганда Крестовоздвиженский храм
ru-karaganda-city-peter-paul|Church|parish|Saints Peter and Paul Church in Karaganda|Караганда Петропавловский храм
ru-karaganda-temirtau-saint-nicholas|Cathedral Parish|parish|Saint Nicholas Cathedral in Temirtau|Темиртау Никольский собор
ru-karaganda-temirtau-protection|Church|parish|Protection Church in Temirtau|Темиртау Покровский храм
ru-karaganda-osakarovka-kazan-icon|Church|parish|Kazan Icon Church in Osakarovka|Осакаровка Казанский храм
ru-karaganda-nura-saint-sergius|Church|parish|Saint Sergius Church in Nura|Нура Сергиевский храм
ru-karaganda-botakara-holy-trinity|Church|parish|Holy Trinity Church in Botakara|Ботакара Троицкий храм
ru-karaganda-balkhash-saint-nicholas|Church|parish|Saint Nicholas Church in Balkhash|Балхаш Никольский храм
ru-karaganda-priozersk-saint-alexander|Church|parish|Saint Alexander Church in Priozersk|Приозерск Александровский храм
ru-karaganda-akbulak-theophany|Church|parish|Theophany Church in Akbulak|Акбулак Богоявленский храм
""")

add_block("ru-karaganda", SHAKHTINSK, """
ru-karaganda-shakhtinsk-quick-hearer|Church|parish|Quick to Hear Icon of the Mother of God Church in Shakhtinsk|Шахтинск Скоропослушнический храм
ru-karaganda-saran-saint-tikhon|Church|parish|Saint Tikhon Church in Saran|Сарань Тихоновский храм
ru-karaganda-abai-joy-all-sorrow|Church|parish|Joy of All Who Sorrow Icon Church in Abai|Абай Всех скорбящих Радость храм
ru-karaganda-topar-transfiguration|Church|parish|Transfiguration Church in Topar|Топар Преображенский храм
ru-karaganda-shakhan-saint-nicholas|Church|parish|Saint Nicholas Church in Shakhan|Шахан Никольский храм
ru-karaganda-novodolinsky-saint-elizabeth|Church|parish|Saint Elizabeth Church in Novodolinsky|Новодолинский Елисаветинский храм
ru-karaganda-zhartas-new-martyrs|Church|parish|New Martyrs and Confessors Church in Zhartas|Жартас Новомучеников и исповедников храм
ru-karaganda-aktas-saint-nicholas|Church|parish|Saint Nicholas Church in Aktas|Актас Никольский храм
ru-karaganda-zhezkazgan-saint-andrew|Church|parish|Saint Andrew Church in Zhezkazgan|Жезказган Андреевский храм
ru-karaganda-zhezkazgan-iveron-icon|Church|parish|Iveron Icon Church in Zhezkazgan|Жезказган Иверский храм
ru-karaganda-satpaev-saint-nicholas|Church|parish|Saint Nicholas Church in Satpaev|Сатпаев Никольский храм
""")

add_block("ru-karaganda", KARAGANDA_NEW, """
ru-karaganda-city-trinity-sebastian|Cathedral Parish|parish|Holy Trinity and Saint Sebastian Cathedral in Karaganda|Троице-Севастиановский собор
""")

add_block("ru-kokshetau", KOKSHETAU, """
ru-kokshetau-city-archangel-michael|Church|parish|Archangel Michael Church in Kokshetau|Храм Архистратига Михаила, город Кокшетау
ru-kokshetau-zerenda-archangel-michael|Church|parish|Archangel Michael Church in Zerenda|Храм Архистратига Михаила, село Зеренда
ru-kokshetau-balkashino-vladimir-icon|Church|parish|Vladimir Icon of the Mother of God Church in Balkashino|Храм Владимирской иконы Божией Матери, село Балкашино
ru-kokshetau-maksimovka-saint-nicholas|Church|parish|Saint Nicholas Church in Maksimovka|Храм Свято-Никольский, село Максимовка
ru-kokshetau-shantobe-panteleimon|Church|parish|Saint Panteleimon Church in Shantobe|Храм святого великомученика и чудотворца Пантелеимона, посёлок Шантобе
ru-kokshetau-kuropatkino-peter-paul|Church|parish|Holy Apostles Peter and Paul Church in Kuropatkino|Храм святых апостолов Петра и Павла, село Куропаткино
ru-kokshetau-molodezhnoe-cyprian-justina|Church|parish|Saints Cyprian and Justina Church in Molodezhnoe|Храм святых Киприана и Иустины, село Молодежное
ru-kokshetau-shchuchinsk-archangel-michael|Church|parish|Archangel Michael Church in Shchuchinsk|Храм Архистратига Михаила, город Щучинск
ru-kokshetau-makinsk-saint-nicholas|Church|parish|Saint Nicholas Church in Makinsk|Храм святителя Николая Чудотворца, город Макинск
ru-kokshetau-novobratskoe-matrona|Church|parish|Blessed Matrona of Moscow Church in Novobratskoe|Храм в честь блаженной Матроны Московской село Новобратское
ru-kokshetau-burabay-panteleimon|Church|parish|Saint Panteleimon Church in Burabay|Храм святого великомученика и чудотворца Пантелеимона, посёлок Бурабай
ru-kokshetau-dmitrievka-demetrius|Church|parish|Saint Demetrius of Thessalonica Church in Dmitrievka|Храм великомученика Димитрия Солунского, село Дмитриевка
ru-kokshetau-katarkol-saint-nicholas|Church|parish|Saint Nicholas Church in Katarkol|Храм святителя Николая Чудотворца, село Катарколь
ru-kokshetau-atbasar-sergius-radonezh|Church|parish|Saint Sergius of Radonezh Church in Atbasar|Храм преподобного Сергия Радонежского, город Атбасар
ru-kokshetau-zaporozhye-john-baptist|Church|parish|Nativity of Saint John the Baptist Church in Zaporozhye|Храм Рождества Иоанна Крестителя, село Запорожье
ru-kokshetau-timashevka-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Timashevka|Храм Казанской иконы Божией Матери, село Тимашевка
ru-kokshetau-derzhavinsk-protection|Church|parish|Protection of the Most Holy Theotokos Church in Derzhavinsk|Храм Покрова Пресвятой Богородицы, город Державинск
ru-kokshetau-esil-dormition|Church|parish|Dormition of the Mother of God Church in Esil|Храм Успения Божией Матери, город Есиль
ru-kokshetau-astrakhanka-john-chrysostom|Church|parish|Saint John Chrysostom Church in Astrakhanka|Храм святителя Иоанна Златоуста, село Астраханка
ru-kokshetau-egindykol-protection|Church|parish|Protection of the Most Holy Theotokos Church in Egindykol|Храм Покрова Пресвятой Богородицы, село Егиндыколь
ru-kokshetau-marinovka-archangel-michael|Church|parish|Archangel Michael Church in Marinovka|Храм Архистратига Михаила, село Мариновка
ru-kokshetau-stepnogorsk-eleutherius|Church|parish|Hieromartyr Eleutherius of Rome Church in Stepnogorsk|Храм священномученика Елевферия Римского, город Степногорск
ru-kokshetau-ereymentau-elizabeth|Church|parish|Grand Duchess Elizabeth Church in Ereymentau|Храм великой княгини Елисаветы, город Ерейментау
ru-kokshetau-akkol-saint-barbara|Church|parish|Great Martyr Barbara Church in Akkol|Храм святой великомученицы Варвары, город Акколь
ru-kokshetau-arshaly-saint-catherine|Church|parish|Great Martyr Catherine Church in Arshaly|Храм святой великомученицы Екатерины, посёлок Аршалы
ru-kokshetau-novomarkovka-constantine-helen|Church|parish|Saints Constantine and Helen Church in Novomarkovka|Храм святых равноапостольных Константина и Елены, село Новомарковка
ru-kokshetau-shortandy-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Shortandy|Храм преподобного Серафима Саровского, посёлок Шортанды
""")

add_block("ru-kokshetau", KOKSHETAU_CATHEDRAL, """
ru-kokshetau-city-resurrection|Cathedral Parish|parish|Resurrection of Christ Cathedral in Kokshetau|кафедральный собор Воскресения Христова г.Кокшетау
""")

KOSTANAY = "https://kst-eparhia.kz/hramy-i-prihody/"
add_block("ru-kostanay", KOSTANAY, """
ru-kostanay-feodorovka-saint-nicholas|Church|parish|Saint Nicholas Church in Feodorovka|Храм во имя святителя Николая, архиепископа Мир Ликийских, чудотворца села Феодоровка
ru-kostanay-karabalyk-seraphim|Church|parish|Saint Seraphim Church in Karabalyk|Свято-Серафимовский храм поселка Карабалык
ru-kostanay-oktyabrskoe-iveron-peter-paul-convent|Convent|monastery|Iveron-Peter and Paul Convent in Oktyabrskoe|Иверско-Петропавловский женский монастырь села Октябрьское
ru-kostanay-oktyabrskoe-saint-nicholas|Church|parish|Saint Nicholas Church in Oktyabrskoe|Храм во имя святителя Николая, архиепископа Мир Ликийских, чудотворца села Октябрьское
ru-kostanay-lisakovsk-all-saints-chapel|Chapel|parish|All Saints Cemetery Chapel in Lisakovsk|Кладбищенская часовня в честь Всех Святых города Лисаковск
ru-kostanay-city-matrona-chapel|Chapel|parish|Blessed Matrona of Moscow Chapel in Kostanay|Часовня святой блаженной Матроны Московской города Костаная
ru-kostanay-auliekol-alexander-nevsky|Church|parish|Saint Alexander Nevsky Church in Auliekol|Александро-Невский храм села Аулиеколь
ru-kostanay-karasu-protection|Church|parish|Protection Church in Karasu|Свято-Покровский храм села Карасу
ru-kostanay-krasny-kordon-unburnt-bush|Church|parish|Unburnt Bush Icon of the Mother of God Church in Krasny Kordon|Храм в честь иконы Божией Матери «Неопалимая Купина» села Красный Кардон
""")

add_block("ru-kostanay", KOSTANAY + "2", """
ru-kostanay-sarykol-all-saints|Church|parish|All Saints Church in Sarykol|Всехсвятский храм поселка Сарыколь
ru-kostanay-mikhailovka-archangel-michael|Church|parish|Archangel Michael Church in Mikhailovka|Храм Архангела Михаила села Михайловка
ru-kostanay-peshkovka-saint-helen|Church|parish|Saint Helen Church in Peshkovka|Храм равноапостольной царицы Елены села Пешковка
ru-kostanay-presnogorkovka-saint-nicholas|Church|parish|Saint Nicholas Church in Presnogorkovka|Свято-Никольский храм села Пресногорьковка
ru-kostanay-uzunkol-peter-paul|Church|parish|Saints Peter and Paul Church in Uzunkol|Петро-Павловский храм села Узунколь
ru-kostanay-borovskoe-cosmas-damian|Church|parish|Saints Cosmas and Damian Church in Borovskoe|Косьмо-Дамиановский храм с. Боровское
ru-kostanay-kamysty-iveron-icon|Church|parish|Iveron Icon of the Mother of God Church in Kamysty|Храм Иверской иконы Божией Матери села Камысты
ru-kostanay-frunzenskoe-archangel-michael|Church|parish|Archangel Michael Church in Frunzenskoe|Храм Михаила Архангела села Фрунзенское
ru-kostanay-denisovka-meet-it-is|Church|parish|It Is Truly Meet Icon of the Mother of God Church in Denisovka|Храм иконы Божией Матери «Достойно есть» с. Денисовска
""")

add_block("ru-kostanay", KOSTANAY + "3", """
ru-kostanay-zhitikara-sergius-radonezh|Church|parish|Saint Sergius of Radonezh Church in Zhitikara|Храм преподобного Сергия Радонежского г. Житикара
ru-kostanay-zhitikara-panteleimon|Church|parish|Great Martyr and Healer Panteleimon Church in Zhitikara|Храм великомученика и целителя Пантелеимона г. Житикара
ru-kostanay-asenkritovka-protection|Church|parish|Protection Church in Asenkritovka|Покровский храм села Асенкритовка
ru-kostanay-tobol-sergius-radonezh|Church|parish|Saint Sergius of Radonezh Church in Tobol|Храм преподобного Сергия Радонежского поселка Тобол
ru-kostanay-lisakovsk-john-kronstadt|Church|parish|Saint John of Kronstadt Church in Lisakovsk|Храм святого праведного Иоанна Кронштадтского г. Лисаковск
ru-kostanay-arkalyk-holy-trinity|Church|parish|Holy Trinity Church in Arkalyk|Свято-Троицкий храм г. Аркалык
ru-kostanay-aleksandrovka-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Aleksandrovka|Храм в честь иконы Божией Матери «Казанская» села Александровка
ru-kostanay-kachar-archangel-michael|Church|parish|Archangel Michael Church in Kachar|Храм во имя святого Архистратига Божия Михаила посёлка Качар
ru-kostanay-aiet-demetrius|Church|parish|Saint Demetrius of Thessalonica Church in Aiet|Храм великомученика Дмитрия Солунского села Айет
""")

add_block("ru-kostanay", KOSTANAY + "4", """
ru-kostanay-tobyl-kazan-icon|Church|parish|Kazan Icon Church in Tobyl|Свято-Казанский храм города Тобыл
ru-kostanay-rudny-theophany|Church|parish|Theophany Church in Rudny|Свято-Богоявленский храм города Рудный
ru-kostanay-city-archangel-michael|Church|parish|Archangel Michael Church in Kostanay|Михайло-Архангельский храм г. Костанай
ru-kostanay-city-saint-nicholas|Cathedral Parish|parish|Saint Nicholas Cathedral in Kostanay|Свято-Никольский собор города Костаная
ru-kostanay-rudny-john-theologian|Cathedral Parish|parish|Saint John the Theologian Cathedral in Rudny|Иоанно-Богословский кафедральный собор города Рудный
ru-kostanay-city-constantine-helen|Cathedral Parish|parish|Saints Constantine and Helen Cathedral in Kostanay|Константино-Еленинский кафедральный собор г. Костанай
""")

PAVLODAR = "http://pavlodar-eparhia.ru/info/khramy-eparkhii"
PAVLODAR_MONASTERY = "http://pavlodar-eparhia.ru/info/petropavlovskii-zhenskii-monastyr"
add_block("ru-pavlodar", PAVLODAR, """
ru-pavlodar-city-annunciation|Cathedral Parish|parish|Annunciation Cathedral in Pavlodar|Благовещенский кафедральный собор города Павлодар
ru-pavlodar-ekibastuz-iveron-seraphim|Cathedral Parish|parish|Iveron-Seraphim Cathedral in Ekibastuz|Иверско-Серафимовский собор города Экибастуз
ru-pavlodar-city-archangel-michael|Church|parish|Archangel Michael Church in Pavlodar|Михаило-Архангельский храм города Павлодар
ru-pavlodar-city-nativity-christ|Church|parish|Nativity of Christ Church in Pavlodar|Христо-Рождественский храм города Павлодар
ru-pavlodar-aksu-resurrection|Church|parish|Resurrection Church in Aksu|Воскресенский храм города Аксу
ru-pavlodar-uspenka-dormition|Church|parish|Dormition Church in Uspenka|Успенский храм села Успенка
ru-pavlodar-terenkol-three-hierarchs|Church|parish|Three Hierarchs Church in Terenkol|Трехсвятительский храм села Теренколь
ru-pavlodar-zhelezinka-holy-trinity|Church|parish|Holy Trinity Church in Zhelezinka|Троицкий храм села Железинка
ru-pavlodar-peschanoe-prophet-elijah|Church|parish|Prophet Elijah Church in Peschanoe|Ильинский храм села Песчаное
ru-pavlodar-orlovka-john-baptist|Church|parish|Saint John the Baptist Church in Orlovka|Иоанно-Предтеченский храм села Орловка
ru-pavlodar-solnechny-all-saints-russia|Church|parish|All Saints Who Shone Forth in the Russian Land Church in Solnechny|Храм Всех святых в земле Российской просиявших пос. Солнечный
ru-pavlodar-irtyshsk-alexander-nevsky|Church|parish|Saint Alexander Nevsky Church in Irtyshsk|Александро-Невский храм села Иртышск
ru-pavlodar-city-saint-nicholas|Church|parish|Saint Nicholas Church in Pavlodar|Никольский храм города Павлодар
ru-pavlodar-pavlodarskoe-peter-paul|Church|parish|Saints Peter and Paul Church in Pavlodarskoe|Петропавловский храм села Павлодарское (при соименном монастыре)
ru-pavlodar-ivanovka-protection|Church|parish|Protection Church in Ivanovka|Покровский храм села Ивановка
ru-pavlodar-sharbakty-saint-elizabeth|Church|parish|Saint Elizabeth Church in Sharbakty|Елизаветинский храм села Шарбакты
ru-pavlodar-aksu-saint-nicholas|Church|parish|Saint Nicholas Church in Aksu|Никольский храм города Аксу
ru-pavlodar-aktogay-panteleimon|Prayer House|parish|Saint Panteleimon Prayer House in Aktogay|Пантелеимоновский молитвенный дом села Актогай
ru-pavlodar-yamyshevo-john-theologian|Church|parish|Saint John the Theologian Church in Yamyshevo|Иоанно-Богословский храм в селе Ямышево
ru-pavlodar-aleksandrovka-holy-trinity|Chapel|parish|Holy Trinity Church-Chapel in Aleksandrovka|Троицкий храм-часовня села Александровка
ru-pavlodar-golubovka-holy-spirit|Chapel|parish|Holy Spirit Church-Chapel in Golubovka|Свято-Духовский храм-часовня села Голубовка
ru-pavlodar-kyzylzhar-saint-nicholas|Chapel|parish|Saint Nicholas Church-Chapel in Kyzylzhar|Никольский храм-часовня села Кызылжар
ru-pavlodar-zhambyl-kazan-icon|Prayer House|parish|Kazan Icon Prayer House in Zhambyl|Казанский молитвенный дом села Жамбыл
ru-pavlodar-konstantinovka-constantine-helen|Prayer House|parish|Saints Constantine and Helen Prayer House in Konstantinovka|Константино-Еленинский молитвенный дом села Константиновка
ru-pavlodar-bashmachnoe-panteleimon|Prayer House|parish|Saint Panteleimon Prayer House in Bashmachnoe|Пантелеимоновский молитвенный дом села Башмачное
ru-pavlodar-zhanabet-kazan-icon|Prayer House|parish|Kazan Icon Prayer House in Zhanabet|Казанский молитвенный дом села Жанабет
ru-pavlodar-beregovoe-new-martyrs-kazakhstan|Prayer House|parish|New Martyrs and Confessors of Kazakhstan Prayer House in Beregovoe|Новомучеников и исповедников Казахстанских молитвенный дом села Береговое
ru-pavlodar-city-saint-nicholas-chapel|Chapel|parish|Saint Nicholas Chapel in Pavlodar|Часовня святителя Николая Чудотворца в городе Павлодар
ru-pavlodar-city-all-saints-cemetery|Chapel|parish|All Saints Chapel at Suvorov Cemetery in Pavlodar|Часовня во имя Всех святых (на Суворовском кладбище города Павлодар)
ru-pavlodar-terenkol-smolensk-icon|Chapel|parish|Smolensk Icon of the Mother of God Chapel in Terenkol|Часовня Смоленской иконы Божией Матери в селе Теренколь
ru-pavlodar-peschanoe-resurrection|Chapel|parish|Resurrection Chapel in Peschanoe|Воскресенская часовня в селе Песчаное
ru-pavlodar-chaldai-cemetery|Chapel|parish|Cemetery Chapel in Chaldai|Кладбищенская часовня в селе Чалдай
""")

add_block("ru-pavlodar", (PAVLODAR, PAVLODAR_MONASTERY), """
ru-pavlodar-pavlodarskoe-peter-paul-convent|Convent|monastery|Saints Peter and Paul Convent in Pavlodarskoe|Петропавловский женский монастырь
""")

PETROPAVL = "https://www.pbe.kz/"
add_block("ru-petropavl-and-bulayevo", PETROPAVL + "petropavlovskoe-blagochinie-0", """
ru-petropavl-city-ascension|Cathedral Parish|parish|Ascension Cathedral in Petropavl|Вознесенский кафедральный собор
ru-petropavl-city-peter-paul|Cathedral Parish|parish|Holy Apostles Peter and Paul Cathedral in Petropavl|Собор Святых апостолов Петра и Павла
ru-petropavl-city-sebastian-mary-magdalene|Church|parish|Saint Sebastian and Saint Mary Magdalene Church in Petropavl|Севастиано-Магдалининский храм
ru-petropavl-city-all-saints|Church|parish|All Saints Church in Petropavl|Храм Всех Святых
ru-petropavl-city-hieromartyr-methodius|Church|parish|Hieromartyr Methodius of Petropavl Church in Petropavl|Храм в честь священномученика Мефодия Петропавловского
""")

add_block("ru-petropavl-and-bulayevo", PETROPAVL + "bulaevskoe-blagochinie", """
ru-petropavl-bulaevo-saint-nicholas|Church|parish|Saint Nicholas Church in Bulaevo|Храм в честь святителя Николая Мирликийского, город Булаево
ru-petropavl-bolshoi-izyum-dormition|Church|parish|Dormition of the Most Holy Theotokos Church in Bolshoi Izyum|Храм в честь Успения Пресвятой Богородицы, село Большой Изюм
ru-petropavl-kara-goga-matrona|Church|parish|Blessed Matrona of Moscow Church in Kara-Goga|Храм в честь блаженной Матроны Московской, село Кара-Гога
ru-petropavl-lebyazhye-prophet-elijah|Church|parish|Prophet Elijah Church in Lebyazhye|Храм в честь пророка Илии, село Лебяжье
ru-petropavl-taiynsha-protection|Church|parish|Protection of the Most Holy Theotokos Church in Taiynsha|Храм в честь Покрова Пресвятой Богородицы, село Тайынша
ru-petropavl-chkalovo-three-hierarchs|Church|parish|Three Hierarchs Church in Chkalovo|Храм в честь Трёх Святителей, село Чкалово
ru-petropavl-nadezhka-faith-hope-love-sophia|Church|parish|Holy Martyrs Faith, Hope, Love, and Sophia Church in Nadezhka|Храм в честь мучениц Веры, Надежды, Любови и матери их Софии, село Надежка
""")

add_block("ru-petropavl-and-bulayevo", PETROPAVL + "beskolskoe-blagochinie", """
ru-petropavl-arkhangelskoe-archangel-michael|Church|parish|Archangel Michael Church in Arkhangelskoe|Храм в честь Архангела Михаила, село Архангельское
ru-petropavl-bogolyubovo-bogolyubovo-icon|Church|parish|Bogolyubovo Icon of the Mother of God Church in Bogolyubovo|Храм в честь Боголюбской иконы Божией Матери, село Боголюбово
ru-petropavl-beskol-protection|Church|parish|Protection of the Most Holy Theotokos Church in Beskol|Храм в честь Покрова Пресвятой Богородицы, село Бесколь
ru-petropavl-novo-nikolskoe-saint-nicholas|Church|parish|Saint Nicholas Church in Novonikolskoe|Храм в честь святителя Николая Мирликийского, село Новоникольское
ru-petropavl-sokolovka-saint-george|Church|parish|Saint George the Victory-Bearer Church in Sokolovka|Храм великомученика Георгия Победоносца, село Соколовка
ru-petropavl-voznesenka-ascension|Church|parish|Ascension of the Lord Church in Voznesenka|Храм в честь Вознесения Господня, села Вознесенка
ru-petropavl-smirnovo-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Smirnovo|Храм в честь преподобного Серафима Саровского, село Смирново
ru-petropavl-tokushi-ambrose-optina|Church|parish|Saint Ambrose of Optina Church in Tokushi|Храм в честь преподобного Амвросия Оптинского, село Токуши
ru-petropavl-peterfeld-xenia|Church|parish|Blessed Xenia of Petersburg Church in Peterfeld|Храм в честь блаженной Ксении Петербургской, село Петерфельд
ru-petropavl-novokamenka-demetrius|Church|parish|Saint Demetrius of Thessalonica Church in Novokamenka|Храм в честь великомученика Димитрия Солунского, село Новокаменка
ru-petropavl-penkovo-matrona|Church|parish|Blessed Matrona of Moscow Church in Penkovo|Храм в честь блаженной Матроны Московской, села Пеньково
ru-petropavl-kiyaly-panteleimon|Church|parish|Saint Panteleimon Church in Kiyaly|Храм в честь великомученика и целителя Пантелеимона, село Киялы
ru-petropavl-cherkasskoe-job-pochaev|Church|parish|Saint Job of Pochaev Church in Cherkasskoe|Храм в честь преподобного Иова Почаевского, села Черкасское
""")

add_block("ru-petropavl-and-bulayevo", PETROPAVL + "presnovskoe-blagochinie", """
ru-petropavl-mamlyutka-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Mamlyutka|Храм в честь иконы Божией Матери Казанской, города Мамлютка
ru-petropavl-kladbinka-tikhon-zadonsk|Church|parish|Saint Tikhon of Zadonsk Church in Kladbinka|Храм в честь святителя Тихона Задонского, села Кладбинка
ru-petropavl-mirnoe-saint-vitaly|Church|parish|Saint Vitaly the Monk Church in Mirnoe|Храм в честь преподобного Виталия Монаха, село Мирное
ru-petropavl-blagoveshchenka-annunciation|Church|parish|Annunciation Church in Blagoveshchenka|Храм в честь Благовещения Пресвятой Богородицы, села Благовещенка
ru-petropavl-presnovka-archangel-michael|Church|parish|Archangel Michael Church in Presnovka|Храм в честь Архангела Михаила, села Пресновка
ru-petropavl-petrovka-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Petrovka|Храм в честь иконы Божией Матери Казанской, села Петровка
ru-petropavl-novomikhailovka-archangel-michael|Church|parish|Archangel Michael Church in Novomikhailovka|Храм в честь Архистратига Божия Михаила, село Новомихайловка
""")

add_block("ru-petropavl-and-bulayevo", PETROPAVL + "sergeevskoe-blagochinie", """
ru-petropavl-sergeevka-sergius-radonezh|Church|parish|Saint Sergius of Radonezh Church in Sergeevka|Храм в честь преподобного Сергия Радонежского, город Сергеевка
ru-petropavl-yavlenka-theophany|Church|parish|Theophany Church in Yavlenka|Храм в честь Богоявления Господня, село Явленка
ru-petropavl-timiryazevo-demetrius|Church|parish|Saint Demetrius of Thessalonica Church in Timiryazevo|Храм в честь великомученика Димитрия Солунского, село Тимирязево
ru-petropavl-saumalkol-entry-theotokos|Church|parish|Entry of the Most Holy Theotokos Church in Saumalkol|Храм в честь введения во храм Пресвятой Богородицы, село Саумалколь
ru-petropavl-korneevka-panteleimon|Church|parish|Saint Panteleimon Church in Korneevka|Храм в честь великомученика и целителя Пантелеимона, село Корнеевка
ru-petropavl-imantau-prophet-elijah|Church|parish|Prophet Elijah Church in Imantau|Храм в честь пророка Божия Илии, село Имантау
ru-petropavl-povoznoe-multiplier-wheat|Church|parish|Multiplier of Wheat Icon of the Mother of God Church in Povoznochnoe|Храм в честь иконы Божие Матери «Спорительница Хлебов», село Повозочное
ru-petropavl-zagradovka-holy-trinity|Church|parish|Holy Trinity Church in Zagradovka|Храм в честь Святой Троицы, село Заградовка
ru-petropavl-yasnovka-archangel-michael|Church|parish|Archangel Michael Church in Yasnovka|Храм в честь Архистратига Божия Михаила, село Ясновка
ru-petropavl-novopokrovka-protection|Church|parish|Protection of the Most Holy Theotokos Church in Novopokrovka|Храм в честь Покрова Пресвятой Богородицы, село Новопокровка
""")

add_block("ru-petropavl-and-bulayevo", PETROPAVL + "novoishimskoe-blagochinie", """
ru-petropavl-novoishimskoe-saint-nicholas|Church|parish|Saint Nicholas Church in Novoishimskoe|Храм в честь святителя Николая Мирликийского, село Новоишимское
ru-petropavl-chistopolye-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Chistopolye|Храм в честь иконы Пресвятой Богородицы Казанской, село Чистополье
ru-petropavl-stavropolka-holy-trinity|Church|parish|Holy Trinity Church in Stavropolovka|Храм в честь Святой Троицы, село Ставрополовка
""")

URALSK_CITY = "https://uralsk-eparhiya.kz/index.php?id=11"
URALSK_OUTER = "https://uralsk-eparhiya.kz/index.php?id=8"
URALSK_MONASTERY = "https://uralsk-eparhiya.kz/index.php?id=20&tx_news_pi1%5Bnews%5D=3941&cHash=cb7ff5a3c6b0bda74bd9bef5d5d195f6"
add_block("ru-uralsk", URALSK_CITY, """
ru-uralsk-city-archangel-michael|Cathedral Parish|parish|Archangel Michael Cathedral in Uralsk|Кафедральный Собор Архангела Михаила. Уральск.
ru-uralsk-city-christ-savior|Church|parish|Christ the Savior Church in Uralsk|Храм Христа Спасителя. Уральск.
ru-uralsk-city-protection-convent|Convent|monastery|Protection Convent in Uralsk|Покровский женский монастырь. Уральск.
ru-uralsk-city-saint-nicholas|Church|parish|Saint Nicholas Church in Uralsk|Храм святителя Николая Чудотворца. Уральск.
ru-uralsk-atyrau-dormition|Cathedral Parish|parish|Dormition of the Mother of God Cathedral in Atyrau|Собор Успения Божией Матери. Атырау.
ru-uralsk-aktau-annunciation|Parish|parish|Annunciation Parish in Aktau|Благовещенский приход. Актау.
""")

add_block("ru-uralsk", URALSK_OUTER, """
ru-uralsk-city-transfiguration|Parish|parish|Transfiguration Parish in Uralsk|Спасо-Преображенский приход. Уральск.
ru-uralsk-peremetnoe-nativity-theotokos|Church|parish|Nativity of the Most Holy Theotokos Church in Peremetnoe|Храм Рождества Пресвятой Богородицы Зеленовского района п. Переметное ЗКО
ru-uralsk-serebryakovo-saint-nicholas|Parish|parish|Saint Nicholas Parish in Serebryakovo|Приход Святителя Николая п. Серебряково
ru-uralsk-krugloozernoe-peter-paul|Parish|parish|Saints Peter and Paul Parish in Krugloozernoe|Приход Петра и Павла п. Круглоозерное
ru-uralsk-pokatilovka-ascension|Parish|parish|Ascension of the Lord Church Parish in Pokatilovka|Приход церкви «Вознесения Господня». Село Покатиловка
ru-uralsk-daryinskoe-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Daryinskoe|Храм в честь Казанской иконы Божией Матери. Село Дарьинское.
ru-uralsk-aksai-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Aksai|Церковь преподобного Серафима Саровского. Аксай.
ru-uralsk-chapaevo-three-hierarchs|Parish|parish|Saints Basil the Great, Gregory the Theologian, and John Chrysostom Parish in Chapaevo|Приход святителей Василия Великого, Григория Богослова и Иоанна Златоустого. Село Чапаево.
ru-uralsk-fedorovka-prophet-elijah|Parish|parish|Prophet Elijah Parish in Fedorovka|Приход Святого Пророка Ильи. Село Федоровка.
ru-uralsk-bolshoi-chagan-dormition|Church|parish|Dormition of the Mother of God Church in Bolshoi Chagan|Храм Успения Божией Матери п.Б.Чаган, Байтерекский р-он ЗКО ( подворье Покровского женского монастыря г. Уральска).
""")

add_block("ru-uralsk", URALSK_MONASTERY, """
ru-uralsk-derkul-saint-nicholas-monastery|Monastery|monastery|Saint Nicholas Monastery in Derkul|Свято-Никольский мужской монастырь п. Деркул
""")

USTK = "https://vko-eparhia.kz/eparhiya/khramy-eparkhii/44-ust-kamenogorskoe-blagochinie.html"
SEMIPALATINSK = "https://vko-eparhia.kz/eparhiya/khramy-eparkhii/45-semipalatinskoe-blagochinie.html"
add_block("ru-ust-kamenogorsk", USTK, """
ru-ust-kamenogorsk-city-saint-andrew|Cathedral Parish|parish|Saint Andrew Cathedral in Ust-Kamenogorsk|г.Усть-Каменогорск, Андреевский кафедральный собор
ru-ust-kamenogorsk-city-holy-trinity|Church|parish|Holy Trinity Church in Ust-Kamenogorsk|г.Усть-Каменогорск, Свято-Троицкий храм (памятник архитектуры)
ru-ust-kamenogorsk-mirny-protection|Cathedral Parish|parish|Protection Cathedral in the Mirny District of Ust-Kamenogorsk|г.Усть-Каменогорск, р-н Мирный, Покровский собор
ru-ust-kamenogorsk-city-holy-trinity-monastery|Monastery|monastery|Holy Trinity Monastery in Ust-Kamenogorsk|г.Усть-Каменогорск, Свято-Троицкий мужской монастырь
ru-ust-kamenogorsk-novaya-sogra-saint-zinovy|Church|parish|Saint Zinovy Church in Novaya Sogra, Ust-Kamenogorsk|г.Усть-Каменогорск, р-н Новая Согра, Зиновьевский храм
ru-ust-kamenogorsk-ablaketka-nativity-theotokos|Church|parish|Nativity of the Theotokos Church in Ablaketka, Ust-Kamenogorsk|г.Усть-Каменогорск, р-н Аблакетка, Богородице-Рождественский храм
ru-ust-kamenogorsk-ridder-unexpected-joy|Church|parish|Unexpected Joy Icon of the Mother of God Church in Ridder|г.Риддер, храм в честь иконы Божией Матери «Нечаянная радость»
ru-ust-kamenogorsk-ridder-saint-nicholas|Church|parish|Saint Nicholas Church in Ridder|г.Риддер, Никольский храм
ru-ust-kamenogorsk-predgornoe-saint-stephen|Church|parish|Saint Stephen Church in Predgornoe|с.Предгорное, Стефаниевский храм
ru-ust-kamenogorsk-glubokoe-three-hierarchs|Church|parish|Three Hierarchs Church in Glubokoe|пос.Глубокое, Трёхсвятительский храм
ru-ust-kamenogorsk-uvarovo-archangel-michael|Prayer House|parish|Archangel Michael Prayer House in Uvarovo|c.Уварово, Михайло-Архангельский молитвенный дом
ru-ust-kamenogorsk-zaisan-alexander-nevsky|Church|parish|Saint Alexander Nevsky Church in Zaisan|г.Зайсан, Александро-Невский храм
ru-ust-kamenogorsk-zhastar-new-martyrs|Chapel|parish|New Martyrs and Confessors of Russia and Kazakhstan Chapel in Zhastar Park, Ust-Kamenogorsk|г.Усть-Каменогорск, парк «Жастар», часовня в честь Новомучеников и Исповедников Российских и Казахстанских
ru-ust-kamenogorsk-altai-saint-daniel|Church|parish|Saint Daniel Church in Altai|г.Алтай, Свято-Данииловский храм
ru-ust-kamenogorsk-ust-talovka-kazan-icon|Church|parish|Kazan Icon Church in Ust-Talovka|п.Усть-Таловка, Казанский храм
ru-ust-kamenogorsk-shemonaikha-transfiguration|Church|parish|Transfiguration Church in Shemonaikha|г.Шемонаиха, Спасо-Преображенский храм
ru-ust-kamenogorsk-mitrofanovka-peter-paul|Church|parish|Saints Peter and Paul Church in Mitrofanovka|с.Митрофановка, Петро-Павловский храм
ru-ust-kamenogorsk-tavricheskoe-sign-icon|Church|parish|Sign Icon of the Mother of God Church in Tavricheskoe|с.Таврическое, храм в честь иконы Божией Матери «Знамение»
ru-ust-kamenogorsk-asu-bulak-nativity-theotokos|Church|parish|Nativity of the Theotokos Church in Asu-Bulak|пос.Асу-Булак, Богородице-Рождественский храм
ru-ust-kamenogorsk-urdzhar-prophet-elijah|Church|parish|Prophet Elijah Church in Urdzhar|с.Урджар, Свято-Ильинский храм
ru-ust-kamenogorsk-gerasimovka-saint-gerasim|Church|parish|Saint Gerasim Church in Gerasimovka|с.Герасимовка, Герасимовский храм
ru-ust-kamenogorsk-pervomaisky-john-baptist|Church|parish|Saint John the Baptist Church in Pervomaisky|пос.Первомайский, Иоанно-Предтеченский храм
ru-ust-kamenogorsk-novaya-bukhtarma-saint-catherine|Church|parish|Saint Catherine Church in Novaya Bukhtarma|пос.Новая Бухтарма, Екатерининский храм
ru-ust-kamenogorsk-samarskoe-protection|Church|parish|Protection Church in Samarskoe|с.Самарское, Покровский храм
ru-ust-kamenogorsk-sennoe-protection|Church|parish|Protection Church in Sennoe|с.Сенное, Покровский храм
ru-ust-kamenogorsk-verkh-uba-protection|Church|parish|Protection Church in Verkh-Uba|с.Верх-Уба, Покровский храм
ru-ust-kamenogorsk-serebryansk-prophet-elijah|Church|parish|Prophet Elijah Church in Serebryansk|г.Серебрянск, Пророко-Ильинский храм
ru-ust-kamenogorsk-novo-troitskoe-prayer-house|Prayer House|parish|Novo-Troitskoe Prayer House|с.Ново-Троицкое, Ново-Троицкий молельный дом
ru-ust-kamenogorsk-glubochanka-prayer-room|Prayer Room|parish|Prayer Room in Glubochanka|с.Глубочанка, молитвенная комната
ru-ust-kamenogorsk-ushanovskoe-tender-mercy|Chapel|parish|Tender Mercy Seraphim-Diveyevo Icon of the Mother of God Chapel at Ushanovskoe Cemetery, Ust-Kamenogorsk|г.Усть-Каменогорск, Ушановское кладбище, часовня в честь иконы Божией Матери «Умиление» Серафимо-Дивеевской
ru-ust-kamenogorsk-shemonaikha-panteleimon-chapel|Chapel|parish|Saint Panteleimon Hospital Chapel in Shemonaikha|г.Шемонаиха, часовня во имя великомученика и целителя Пантелеимона, прибольничная
ru-ust-kamenogorsk-altai-sergius-chapel|Chapel|parish|Saint Sergius of Radonezh Chapel in Victory Park, Altai|г.Алтай, парк Победы, часовня во имя преподобного Сергия Радонежского
ru-ust-kamenogorsk-city-martyr-varus|Chapel|parish|Martyr Varus Chapel in Ust-Kamenogorsk|г. Усть-Каменогорск, часовня во имя мученика Уара
ru-ust-kamenogorsk-belousovka-seraphim|Church|parish|Saint Seraphim Church in Belousovka|пос. Белоусовка, Свято-Серафимовский храм
ru-ust-kamenogorsk-ulken-naryn-prince-vladimir|Chapel|parish|Saint Vladimir Church-Chapel in Ulken Naryn|с. Улькен Нарын (до 2009 года - Большенарымское), храм-часовня во имя равноапостольного князя Владимира, Крестителя Руси
ru-ust-kamenogorsk-snegirevo-dormition|Chapel|parish|Dormition of the Most Holy Theotokos Chapel in Snegirevo|с. Снегирёво, часовня в честь Успения Пресвятой Богородицы
""")

add_block("ru-ust-kamenogorsk", SEMIPALATINSK, """
ru-ust-kamenogorsk-novo-pokrovka-protection|Church|parish|Protection of the Most Holy Theotokos Church in Novo-Pokrovka|с.Ново-Покровка, храм Покрова Пресвятой Богородицы (Семипалатинское благочиние)
ru-ust-kamenogorsk-ozerki-john-baptist|Church|parish|Nativity of Saint John the Baptist Church in Ozerki|с.Озерки, храм в честь рождества Пророка, Предтечи и Крестителя Господня Иоанна (Семипалатинское благочиние)
ru-ust-kamenogorsk-semipalatinsk-saint-nicholas-chapel|Chapel|parish|Saint Nicholas Chapel in Semipalatinsk|г.Семипалатинск, часовня во имя свт.Николая (Семипалатинское благочиние)
ru-ust-kamenogorsk-kurchatov-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Kurchatov|г.Курчатов, храм Казанской иконы Божией Матери (Семипалатинское благочиние)
ru-ust-kamenogorsk-beskaragai-holy-trinity|Church|parish|Holy Trinity Church in Beskaragai|с.Бескарагай (Большая Владимировка), храм Святой Троицы (Семипалатинское благочиние)
ru-ust-kamenogorsk-semipalatinsk-resurrection|Cathedral Parish|parish|Resurrection Cathedral in Semipalatinsk|г.Семипалатинск, Воскресенский собор (Семипалатинское благочиние)
ru-ust-kamenogorsk-semipalatinsk-abala-sign-convent|Convent|monastery|Abalatsk Sign Saints Peter and Paul Convent in Semipalatinsk|г.Семипалатинск, Абалацко-Знаменский Петро-Павловский женский монастырь (Семипалатинское благочиние)
ru-ust-kamenogorsk-borodulikha-saint-nicholas|Church|parish|Saint Nicholas Church in Borodulikha|с.Бородулиха, Никольский храм (Семипалатинское благочиние)
ru-ust-kamenogorsk-novaya-shulba-vladimir-icon|Church|parish|Vladimir Icon of the Mother of God Church in Novaya Shulba|с.Новая Шульба, храм в честь Владимирской иконы Божией Матери (Семипалатинское благочиние)
ru-ust-kamenogorsk-shulbinsk-archangel-michael|Church|parish|Archangel Michael Church in Shulbinsk|пос.Шульбинск, Михайло-Архангельский храм (Семипалатинское благочиние)
ru-ust-kamenogorsk-kanonerka-dormition|Church|parish|Dormition Church in Kanonerka|с.Канонерка, Успенский храм (Семипалатинское благочиние)
ru-ust-kamenogorsk-zhezkent-john-theologian|Church|parish|Holy Apostle and Evangelist John the Theologian Church in Zhezkent|пос.Жезкент, храм Святого апостола и евангелиста Иоанна Богослова (Семипалатинское благочиние)
""")

SHYMKENT = "https://chim-eparhiya.cerkov.ru/xramy-eparxii/"
add_block("ru-shymkent", SHYMKENT, """
ru-shymkent-city-saint-nicholas|Cathedral Parish|parish|Saint Nicholas Cathedral in Shymkent|Свято-Никольский кафедральный собор города Шымкента
ru-shymkent-city-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in Shymkent|Храм преподобного Серафима Саровского города Шымкента
ru-shymkent-city-panteleimon|Church|parish|Great Martyr and Healer Panteleimon Church in Shymkent|Храм великомученика и целителя Пантелеимона города Шымкента
ru-shymkent-city-archangel-michael|Church|parish|Archangel Michael Church in Shymkent|Храм Архангела Михаила города Шымкента
ru-shymkent-city-kazan-icon|Church|parish|Kazan Icon Church in Shymkent|Казанский храм города Шымкента
ru-shymkent-taraz-dormition|Cathedral Parish|parish|Dormition Cathedral in Taraz|Успенский собор города Тараза
ru-shymkent-taraz-protection|Church|parish|Protection Church in Taraz|Покровский храм города Тараза
ru-shymkent-shu-archangel-michael|Church|parish|Archangel Michael Church in Shu|Храм Архангела Михаила города Шу
ru-shymkent-saryagash-saint-nicholas|Church|parish|Saint Nicholas Church in Saryagash|Никольский храм города Сарыагаш
ru-shymkent-arys-kazan-icon|Church|parish|Kazan Icon Church in Arys|Казанский храм города Арыси
ru-shymkent-turkestan-saint-nicholas|Church|parish|Saint Nicholas Church in Turkestan|Никольский храм города Туркестана
ru-shymkent-zhetysai-saint-george|Church|parish|Saint George the Victory-Bearer Church in Zhetysai|Храм св. Георгия Победоносца города Жетысай
ru-shymkent-kentau-annunciation|Church|parish|Annunciation Church in Kentau|Благовещенский храм города Кентау
ru-shymkent-shardara-john-kronstadt|Church|parish|Saint John of Kronstadt Church in Shardara|Храм праведного Иоанна Кронштадтского города Шардара
ru-shymkent-karatau-three-hierarchs|Church|parish|Three Hierarchs Church in Karatau|Храм Трех святителей города Каратау
ru-shymkent-koksaek-saint-george|Church|parish|Great Martyr George the Victory-Bearer Church in Koksaek|Храм великомученика Георгия Победоносца села Коксаек
ru-shymkent-aksukent-joy-all-sorrow|Church|parish|Joy of All Who Sorrow Icon of the Mother of God Church in Aksukent|Храм иконы Божией Матери «Всех скорбящих Радость» села Аксукент
ru-shymkent-atakent-john-russian|Church|parish|Saint John the Russian Church in Atakent|Храм праведного Иоанна Русского села Атакент
ru-shymkent-kyzylzhar-seraphim-theognostus|Church|parish|Saints Seraphim and Theognostus Church in Kyzylzhar|Храм преподобномучеников Серафима и Феогноста села Кызылжар
ru-shymkent-lenger-macarius-egypt|Church|parish|Saint Macarius of Egypt Church in Lenger|Храм преподобного Макария Египетского города Ленгера
ru-shymkent-t-ryskulov-john-theologian|Church|parish|Apostle John the Theologian Church in T. Ryskulov|Храм апостола Иоанна Богослова села Т. Рыскулова
ru-shymkent-sastobe-xenia|Church|parish|Blessed Xenia of Petersburg Church in Sastobe|Храм блаженной Ксении Петербургской села Састобе
ru-shymkent-turlansky-demetrius|Church|parish|Great Martyr Demetrius of Thessalonica Church in Turlansky|Храм великомученика Димитрия Солунского поселка Турланский
ru-shymkent-kainarbulak-iveron-icon|Church|parish|Iveron Icon of the Mother of God Church in Kainarbulak|Храм Иверской иконы Божией Матери поселка Кайнарбулак
ru-shymkent-kosagash-inexhaustible-chalice|Church|parish|Inexhaustible Chalice Icon of the Mother of God Church in Kosagash|Храм иконы Божией Матери «Неупиваемая Чаша» села Косагаш
ru-shymkent-b-momyshuly-seraphim-sarov|Church|parish|Saint Seraphim of Sarov Church in B. Momyshuly|Храм преподобного Серафима Саровского села Б. Момышулы
ru-shymkent-kordai-saint-george|Church|parish|Great Martyr George the Victory-Bearer Church in Kordai|Храм великомученика Георгия Победоносца села Кордай
ru-shymkent-merke-nativity-theotokos|Church|parish|Nativity of the Theotokos Church in Merke|Храм Рождества Богородицы села Мерке
ru-shymkent-sarymoldaevo-nativity-theotokos|Church|parish|Nativity of the Theotokos Church in Sarymoldaevo|Храм Рождества Богородицы села Сарымолдаево
ru-shymkent-kulan-kazan-icon|Church|parish|Kazan Icon of the Mother of God Church in Kulan|Храм Казанской иконы Божией Матери села Кулан
ru-shymkent-otegen-batyr-adrian-natalia|Church|parish|Holy Martyrs Adrian and Natalia Church in Otegen Batyr|Храм святых мучеников Адриана и Наталии поселка Отеген батыр Алматинской области (подворье Чимкентской епархии)
ru-shymkent-taraz-cemetery-chapel|Chapel|parish|Cemetery Chapel in Taraz|Часовня на кладбище города Тараза
ru-shymkent-turkestan-cemetery-chapel|Chapel|parish|Cemetery Chapel in Turkestan|Часовня на кладбище города Туркестана
ru-shymkent-akyrtobe-cemetery-chapel|Chapel|parish|Cemetery Chapel in Akyrtobe|Часовня на кладбище с. Акыртобе Жамбылской обл.
""")

ENGLISH_NAMES = {
    row["id"]: row["name"]
    for rows in ROWS.values()
    for row in rows
}
ENGLISH_SEATS = {}

EXPECTED = {
    "ru-aktobe": 10,
    "ru-astana": 73,
    "ru-karaganda": 26,
    "ru-kokshetau": 28,
    "ru-kostanay": 33,
    "ru-pavlodar": 33,
    "ru-petropavl-and-bulayevo": 45,
    "ru-taldykorgan-vicariate": 11,
    "ru-uralsk": 17,
    "ru-ust-kamenogorsk": 48,
    "ru-shymkent": 34,
}
EXPECTED_TOTAL = 358
EXPECTED_KINDS = {"parish": 347, "monastery": 11}
ALLOWED_RANKS = {
    "Cathedral Parish", "Parish", "Church", "House Church", "Chapel",
    "Prayer House", "Prayer Room", "Monastery", "Convent", "Hermitage",
}
FORBIDDEN_FIELDS = {
    "contact", "contacts", "email", "phone", "telephone", "clergy",
    "priest", "rector", "abbot", "abbess",
}
FORBIDDEN_PUNCTUATION = (
    "\u2013", "\u2014", "\u2018", "\u2019", "\u201c", "\u201d", "\ufffd",
)


def clean(source):
    row = {
        key: value for key, value in source.items()
        if value not in (None, "", [])
    }
    row.setdefault("checked", CHECKED)
    sources = list(row.get("sources") or [])
    if not sources or len(sources) > 3:
        raise ValueError("%s must cite one to three sources" % row.get("id"))
    if len(sources) != len(set(sources)):
        raise ValueError("%s repeats a source" % row.get("id"))
    if not all(
            str(url).startswith("https://") or
            str(url).startswith("http://pavlodar-eparhia.ru/")
            for url in sources):
        raise ValueError("%s carries an unapproved source scheme" % row.get("id"))
    row["sources"] = sources
    row["cite"] = list(sources)
    rendered = json.dumps(row, ensure_ascii=False)
    if any(mark in rendered for mark in FORBIDDEN_PUNCTUATION):
        raise ValueError("%s carries forbidden punctuation or encoding" %
                         row.get("id"))
    return row


def semantic_key(value):
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def build():
    if set(ROWS) != set(EXPECTED):
        raise ValueError("Kazakhstan parent set is out of sync")
    payloads = {}
    seen_ids = set()
    seen_names = {}
    seen_locals = {}
    kind_counts = {"parish": 0, "monastery": 0}
    total = 0
    for parent, source_rows in ROWS.items():
        rows = []
        for source in source_rows:
            row = clean(source)
            row_id = row.get("id")
            if not row_id or row_id in seen_ids:
                raise ValueError("duplicate or missing id: %s" % row_id)
            if not re.fullmatch(r"[a-z0-9-]+", row_id):
                raise ValueError("%s is not a stable ASCII id" % row_id)
            if row.get("parent") != parent:
                raise ValueError("%s hangs off the wrong parent" % row_id)
            if row.get("country") != "KZ":
                raise ValueError("%s is outside Kazakhstan" % row_id)
            kind = row.get("kind")
            if kind not in EXPECTED_KINDS:
                raise ValueError("%s has unsupported kind %s" % (row_id, kind))
            if row.get("rank") not in ALLOWED_RANKS:
                raise ValueError("%s has unsupported rank %s" %
                                 (row_id, row.get("rank")))
            if kind == "monastery" and row["rank"] not in {
                    "Monastery", "Convent", "Hermitage"}:
                raise ValueError("%s has a non-monastic rank" % row_id)
            if kind == "parish" and row["rank"] in {
                    "Monastery", "Convent", "Hermitage"}:
                raise ValueError("%s has a monastic rank" % row_id)
            if not row.get("name") or not row.get("local"):
                raise ValueError("%s lacks a usable name" % row_id)
            if re.search(r"[А-Яа-яЁё]", row["name"]):
                raise ValueError("%s lacks an English reader name" % row_id)
            if not re.search(r"[А-Яа-яЁё]", row["local"]):
                raise ValueError("%s lacks its official local name" % row_id)
            if FORBIDDEN_FIELDS.intersection(row):
                raise ValueError("%s carries contact or personnel prose" % row_id)
            name_key = semantic_key(row["name"])
            local_key = " ".join(row["local"].casefold().split())
            if name_key in seen_names:
                raise ValueError("semantic English duplicate: %s and %s" %
                                 (seen_names[name_key], row_id))
            if local_key in seen_locals:
                raise ValueError("semantic local duplicate: %s and %s" %
                                 (seen_locals[local_key], row_id))
            seen_names[name_key] = row_id
            seen_locals[local_key] = row_id
            seen_ids.add(row_id)
            kind_counts[kind] += 1
            rows.append(row)
        if len(rows) != EXPECTED[parent]:
            raise ValueError("%s must publish exactly %d rows" %
                             (parent, EXPECTED[parent]))
        total += len(rows)
        payloads[parent] = {
            "v": 1,
            "parent": parent,
            "country": "KZ",
            "rows": rows,
        }
    if total != EXPECTED_TOTAL:
        raise ValueError("Kazakhstan must publish exactly %d rows" %
                         EXPECTED_TOTAL)
    if kind_counts != EXPECTED_KINDS:
        raise ValueError("Kazakhstan kind counts are out of sync: %s" %
                         kind_counts)
    if set(ENGLISH_NAMES) != seen_ids:
        raise ValueError("Kazakhstan English name map is out of sync")
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
        print("directory Kazakhstan: %s" % exc, file=sys.stderr)
        return 1
    if args.dump:
        print(json.dumps(payloads, ensure_ascii=False, indent=2,
                         sort_keys=True))
    print("Kazakhstan: 358 current named bodies (347 parishes, 11 monasteries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
