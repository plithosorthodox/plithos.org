# -*- coding: utf-8 -*-
"""Russian for the vocabulary beside a life. TEXT = {English: rendering}.

Keyed by the English phrase exactly as the index spells it, so a phrase that
is no longer there fails the build rather than quietly never appearing.

Received Russian forms throughout: the orders of sanctity as the menaia name
them, the Typikon's ranks of feast, and the ordinary Russian names of places
and peoples. Where no received form exists the name is transliterated.
"""

TEXT = {}

# The order of sanctity, which is the badge on every card. These follow the
# calendar's own renderings, so the two pages name a saint the same way.
TEXT.update({
    "Angelic": "Бесплотные Силы",
    "Apostle": "Апостол",
    "Confessor": "Исповедник",
    "Equal-to-the-Apostles": "Равноапостольный",
    "Feast": "Праздник",
    "Fool-for-Christ": "Юродивый",
    "Great Martyr": "Великомученик",
    "Hierarch": "Святитель",
    "Hieromartyr": "Священномученик",
    "Martyr": "Мученик",
    "Monastic": "Преподобный",
    "New Martyr": "Новомученик",
    "Other": "Иное",
    "Passion-bearer": "Страстотерпец",
    "Prophet": "Пророк",
    "Righteous": "Праведный",
    "Unmercenary": "Бессребреник",
    "Virgin Martyr": "Мученица дева",
})

# The Churches whose calendars keep the day.
TEXT.update({
    "Greek": "Греческая",
    "Antiochian": "Антиохийская",
    "Romanian": "Румынская",
    "Ukrainian": "Украинская",
    "Russian": "Русская",
    "Serbian": "Сербская",
    "OCA": "ПЦА",
})

# The chips under a name.
TEXT.update({
    "Monastery founder": "Основатель обители",
    "Wonderworker": "Чудотворец",
    "Ruler or royal": "Правитель или царского рода",
    "Desert ascetic": "Пустынник",
    "Enlightener": "Просветитель",
    "New martyr": "Новомученик",
    "Healing intercessor": "Целитель",
    "Stylite": "Столпник",
    "Hymnographer": "Песнописец",
    "Church Father": "Отец Церкви",
    "Iconographer": "Иконописец",
    "Myrrh-bearer": "Мироносица",
    "Myrrh-streaming": "Мироточивый",
    "Warrior saint": "Воин",
    "Incorrupt relics": "Нетленные мощи",
})

# The estate a saint lived in.
TEXT.update({
    "Apostolic": "Апостольское",
    "Clergy": "Духовенство",
    "Laity": "Миряне",
    "Layman": "Мирянин",
    "Laywoman": "Мирянка",
    "Laywomen": "Мирянки",
    "Married": "В браке",
    "Military": "Воинство",
    "Royal": "Царское",
    "Royalty": "Царский род",
    "Unknown": "Неизвестно",
    "Unmarried": "Безбрачие",
    "Widowed": "Вдовство",
})

# The rank of the service, as the Typikon reckons it.
TEXT.update({
    "Doxology": "Славословный",
    "Great Feast": "Великий праздник",
    "Polyeleos": "Полиелейный",
    "Simple": "Простой",
    "Vigil": "Бденный",
})

TEXT.update({
    "Age of the Celtic Saints": "Век кельтских святых",
    "Age of the Ecumenical Councils": "Век Вселенских Соборов",
    "Age of the Martyrs": "Век мучеников",
    "Apostolic Age": "Апостольский век",
    "Byzantine": "Византия",
    "Byzantine Balkans": "Византийские Балканы",
    "Byzantine Era": "Византийская эпоха",
    "Byzantine Iconoclasm": "Византийское иконоборчество",
    "Cossack Era": "Казачья эпоха",
    "Desert Fathers": "Отцы пустыни",
    "Early Medieval West": "Раннесредневековый Запад",
    "Imperial Russia": "Императорская Россия",
    "Kievan Rus'": "Киевская Русь",
    "Medieval Georgia": "Средневековая Грузия",
    "Medieval Rus'": "Средневековая Русь",
    "Medieval Serbia": "Средневековая Сербия",
    "Modern": "Новое время",
    "Modern Era": "Новейшая эпоха",
    "Muscovite Russia": "Московская Русь",
    "Old Testament": "Ветхий Завет",
    "Ottoman Balkans": "Османские Балканы",
    "Ottoman Era": "Османская эпоха",
    "Ottoman period": "Османский период",
    "Polish-Lithuanian period": "Польско-литовский период",
    "Soviet Era": "Советская эпоха",
    "Soviet period": "Советский период",
    "Synodal Russia": "Синодальная Россия",
})

# Lands and regions.
TEXT.update({
    "Aegean": "Эгейские острова",
    "Albania": "Албания",
    "America": "Америка",
    "Arabia": "Аравия",
    "Armenia": "Армения",
    "Asia Minor": "Малая Азия",
    "Balkans": "Балканы",
    "Belarus": "Белоруссия",
    "Bithynia": "Вифиния",
    "Bohemia": "Богемия",
    "Britain": "Британия",
    "British Isles": "Британские острова",
    "Bulgaria": "Болгария",
    "Cappadocia": "Каппадокия",
    "China": "Китай",
    "Cilicia": "Киликия",
    "Constantinople": "Константинополь",
    "Crimea": "Крым",
    "Cyprus": "Кипр",
    "Czech Lands": "Чешские земли",
    "Dalmatia": "Далмация",
    "Danube lands": "Подунавье",
    "Egypt": "Египет",
    "England": "Англия",
    "Ethiopia": "Эфиопия",
    "France": "Франция",
    "Gaul": "Галлия",
    "Georgia": "Грузия",
    "Greece": "Греция",
    "Holy Land": "Святая Земля",
    "Illyria": "Иллирия",
    "Illyricum": "Иллирик",
    "India": "Индия",
    "Ireland": "Ирландия",
    "Italy": "Италия",
    "Judah": "Иудея",
    "Lithuania": "Литва",
    "Macedonia": "Македония",
    "Mesopotamia": "Месопотамия",
    "Moesia": "Мёзия",
    "Moldavia": "Молдавия",
    "Montenegro": "Черногория",
    "Moravia": "Моравия",
    "Mount Athos": "Афон",
    "North Africa": "Северная Африка",
    "North America": "Северная Америка",
    "North Macedonia": "Северная Македония",
    "Palestine": "Палестина",
    "Persia": "Персия",
    "Phoenicia": "Финикия",
    "Poland": "Польша",
    "Pontus": "Понт",
    "Romania": "Румыния",
    "Rome": "Рим",
    "Russia": "Россия",
    "Scythia": "Скифия",
    "Serbia": "Сербия",
    "Siberia": "Сибирь",
    "Sicily": "Сицилия",
    "Sinai": "Синай",
    "Spain": "Испания",
    "Syria": "Сирия",
    "Thrace": "Фракия",
    "Ukraine": "Украина",
    "United States": "Соединённые Штаты",
    "Western Rus": "Западная Русь",
})

TEXT.update({
    "Sunday of the Holy Forefathers": "Неделя святых праотец",
})
