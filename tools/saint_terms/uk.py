# -*- coding: utf-8 -*-
"""Ukrainian for the vocabulary that stands beside the lives.

TEXT = {the phrase the index shows: the Ukrainian}. PARTS holds the pieces
the compound place-names are built from, and expand() assembles the wholes,
so a town cannot be spelled one way on one card and another way on the next.

The rank vocabulary was settled before any of this was written, and is set
down in docs/UKRAINIAN.md. The reason is the defect that had to be swept out
of the three finished languages: in a Slavonic-tradition tongue a saint's
honorific is his rank, and the bare word святий stands before a rank and
never before a name. Преподобний Сергій, святитель Миколай, благовірний
князь Володимир, праведний Симеон Богоприїмець.

The nearer trap here is Russian. Ukrainian is close enough to it that a
rendering can be correct Russian and merely Russian-shaped Ukrainian, which
a reader feels at once and no checker sees. So the Church's own Ukrainian
words are used: Церква declining as Церкви, чернець for the monk, сповідник
for the confessor, безсрібник for the unmercenary, Успіння for the Dormition,
Києво-Печерська лавра and its печерські fathers. Placenames take their
Ukrainian shapes - Київ, Чернігів, Волинь, Переяслав - and the princes their
Ukrainian names: Володимир, Ярослав, Борис і Гліб.

The keys are the phrases exactly as the index writes them, so a rendering
cannot quietly attach itself to the wrong saint.
"""
TEXT = {}


# The orders of sanctity, as the badge on a card names them.
TEXT.update({
    "Angelic": "Безтілесні сили",
    "Apostle": "Апостол",
    "Confessor": "Сповідник",
    "Equal-to-the-Apostles": "Рівноапостольний",
    "Feast": "Свято",
    "Fool-for-Christ": "Христа ради юродивий",
    "Great Martyr": "Великомученик",
    "Hierarch": "Святитель",
    "Hieromartyr": "Священномученик",
    "Martyr": "Мученик",
    "Monastic": "Преподобний",
    "New Martyr": "Новомученик",
    "Other": "Інше",
    "Passion-bearer": "Страстотерпець",
    "Prophet": "Пророк",
    "Righteous": "Праведний",
    "Unmercenary": "Безсрібник",
    "Virgin Martyr": "Мучениця-діва",
})


# The attributes a life is marked with.
TEXT.update({
    "Church Father": "Отець Церкви",
    "Desert ascetic": "Подвижник пустелі",
    "Enlightener": "Просвітитель",
    "Healing intercessor": "Цілитель",
    "Hymnographer": "Піснописець",
    "Iconographer": "Іконописець",
    "Incorrupt relics": "Нетлінні мощі",
    "Monastery founder": "Засновник обителі",
    "Myrrh-bearer": "Мироносиця",
    "Myrrh-streaming": "Мироточивий",
    "New martyr": "Новомученик",
    "Ruler or royal": "Правитель або з княжого роду",
    "Stylite": "Стовпник",
    "Warrior saint": "Святий воїн",
    "Wonderworker": "Чудотворець",
})


# The ranks the Typikon gives a feast.
TEXT.update({
    "Doxology": "Славослів'я",
    "Great Feast": "Велике свято",
    "Polyeleos": "Полієлей",
    "Simple": "Проста",
    "Vigil": "Всенічне бдіння",
})


# The jurisdictions whose calendars the index keeps.
TEXT.update({
    "Antiochian": "Антіохійський",
    "Greek": "Грецький",
    "OCA": "OCA",
    "Romanian": "Румунський",
    "Russian": "Російський",
    "Serbian": "Сербський",
    "Ukrainian": "Український",
})


# The estate a saint stood in.
TEXT.update({
    "Apostolic": "Апостольський",
    "Clergy": "Духівництво",
    "Laity": "Миряни",
    "Layman": "Мирянин",
    "Laywoman": "Мирянка",
    "Laywomen": "Мирянки",
    "Married": "Одружений",
    "Military": "Військовий",
    "Monastic": "Чернечий",
    "Prophet": "Пророк",
    "Royal": "Княжий",
    "Royalty": "Княжий рід",
    "Unknown": "Невідомо",
    "Unmarried": "Неодружений",
    "Widowed": "Овдовілий",
})


# The ages the lives are set in.
TEXT.update({
    "Age of the Celtic Saints": "Доба кельтських святих",
    "Age of the Ecumenical Councils": "Доба Вселенських Соборів",
    "Age of the Martyrs": "Доба мучеників",
    "Apostolic Age": "Апостольська доба",
    "Byzantine": "Візантійський",
    "Byzantine Balkans": "Візантійські Балкани",
    "Byzantine Era": "Візантійська доба",
    "Byzantine Iconoclasm": "Візантійське іконоборство",
    "Cossack Era": "Козацька доба",
    "Desert Fathers": "Отці пустелі",
    "Early Medieval West": "Ранньосередньовічний Захід",
    "Imperial Russia": "Імперська Росія",
    "Kievan Rus'": "Київська Русь",
    "Medieval Georgia": "Середньовічна Грузія",
    "Medieval Rus'": "Середньовічна Русь",
    "Medieval Serbia": "Середньовічна Сербія",
    "Modern": "Новітній",
    "Modern Era": "Новітня доба",
    "Muscovite Russia": "Московська Русь",
    "Old Testament": "Старий Завіт",
    "Ottoman Balkans": "Османські Балкани",
    "Ottoman Era": "Османська доба",
    "Ottoman period": "Османський період",
    "Polish-Lithuanian period": "Польсько-литовський період",
    "Soviet Era": "Радянська доба",
    "Soviet period": "Радянський період",
    "Synodal Russia": "Синодальна Росія",
})


# The one movable commemoration the index names.
TEXT.update({
    "Sunday of the Holy Forefathers": "Неділя святих праотців",
})


# The countries and the regions.
TEXT.update({
    "Aegean": "Егейське море",
    "America": "Америка",
    "Arabia": "Аравія",
    "Armenia": "Вірменія",
    "Asia Minor": "Мала Азія",
    "Balkans": "Балкани",
    "Belarus": "Білорусь",
    "Bithynia": "Віфінія",
    "Britain": "Британія",
    "British Isles": "Британські острови",
    "Bulgaria": "Болгарія",
    "Cappadocia": "Каппадокія",
    "Cilicia": "Кілікія",
    "Constantinople": "Константинополь",
    "Crimea": "Крим",
    "Cyprus": "Кіпр",
    "Czech Lands": "Чеські землі",
    "Dalmatia": "Далмація",
    "Danube lands": "Подунав'я",
    "Egypt": "Єгипет",
    "England": "Англія",
    "Ethiopia": "Ефіопія",
    "Gaul": "Галлія",
    "Georgia": "Грузія",
    "Greece": "Греція",
    "Holy Land": "Свята Земля",
    "Illyria": "Іллірія",
    "Illyricum": "Іллірик",
    "India": "Індія",
    "Ireland": "Ірландія",
    "Italy": "Італія",
    "Lithuania": "Литва",
    "Macedonia": "Македонія",
    "Mesopotamia": "Месопотамія",
    "Moldavia": "Молдова",
    "Montenegro": "Чорногорія",
    "Moravia": "Моравія",
    "Mount Athos": "Свята Гора Афон",
    "North Africa": "Північна Африка",
    "North America": "Північна Америка",
    "North Macedonia": "Північна Македонія",
    "Palestine": "Палестина",
    "Persia": "Персія",
    "Phoenicia": "Фінікія",
    "Poland": "Польща",
    "Pontus": "Понт",
    "Romania": "Румунія",
    "Rome": "Рим",
    "Russia": "Росія",
    "Scythia": "Скіфія",
    "Serbia": "Сербія",
    "Siberia": "Сибір",
    "Sinai": "Синай",
    "Spain": "Іспанія",
    "Syria": "Сирія",
    "Thrace": "Фракія",
    "Ukraine": "Україна",
    "Western Rus": "Західна Русь",
})


# The lands the fasting rule is kept in.
TEXT.update({
    "Albania": "Албанія",
    "Bohemia": "Богемія",
    "China": "Китай",
    "France": "Франція",
    "Judah": "Юдея",
    "Moesia": "Мезія",
    "Sicily": "Сицилія",
    "United States": "Сполучені Штати",
})

# The rank a saint held, as the menaia name it.
TEXT.update({
    "Abbess": "Ігуменя",
    "Abbot (Archimandrite)": "Ігумен (архімандрит)",
    "Abbot (Founder)": "Ігумен (засновник)",
    "Abbot (Igumen)": "Ігумен",
    "Abbot (Igumen), Confessor": "Ігумен, сповідник",
    "Abbot (Igumen), Hieromartyr": "Ігумен, священномученик",
    "Abbot (Igumen), Martyr": "Ігумен, мученик",
    "Abbot (Igumen), Monastic Martyr": "Ігумен, преподобномученик",
    "Abbot, Confessor": "Ігумен, сповідник",
    "Abbot, Confessor-Martyr": "Ігумен, сповідник і мученик",
    "Abbot, Priest": "Ігумен, ієрей",
    "Abbots": "Ігумени",
    "Anchorite": "Самітник",
    "Apostle of the Seventy": "Апостол від сімдесяти",
    "Apostle of the Seventy, Bishop": "Апостол від сімдесяти, єпископ",
    "Apostle of the Seventy, Martyr": "Апостол від сімдесяти, мученик",
    "Apostle, Evangelist": "Апостол, євангелист",
    "Apostle, Martyr": "Апостол, мученик",
    "Apostles": "Апостоли",
    "Apostles of the Seventy": "Апостоли від сімдесяти",
    "Apostles of the Seventy, Martyrs": "Апостоли від сімдесяти, мученики",
    "Archangel": "Архангел",
    "Archbishop": "Архієпископ",
    "Archbishop, Confessor": "Архієпископ, сповідник",
    "Archbishop, Equal-to-the-Apostles": "Архієпископ, рівноапостольний",
    "Archdeacon": "Архідиякон",
    "Archimandrite": "Архімандрит",
    "Bishop": "Єпископ",
    "Bishop, Church Father": "Єпископ, отець Церкви",
    "Bishop, Confessor": "Єпископ, сповідник",
    "Bishop, Equal-to-the-Apostles": "Єпископ, рівноапостольний",
    "Bishop, Hieromartyr": "Єпископ, священномученик",
    "Bishop, Monk": "Єпископ, чернець",
    "Bishops": "Єпископи",
    "Blessed Eldress": "Блаженна стариця",
    "Chamberlain (cubicularius)": "Кувікуларій",
    "Childmartyr": "Отрок-мученик",
    "Commander": "Воєвода",
    "Confessor, Archpriest": "Сповідник, протоієрей",
    "Deacon": "Диякон",
    "Deacon, Monk-martyr": "Диякон, преподобномученик",
    "Deaconess": "Дияконіса",
    "Deaconess and Martyr": "Дияконіса і мучениця",
    "Elder": "Старець",
    "Empress": "Цариця",
    "Equal-to-the-Apostles, Emperor": "Рівноапостольний, цар",
    "Equals-to-the-Apostles": "Рівноапостольні",
    "Grand Duchess": "Велика княгиня",
    "Grand Prince": "Великий князь",
    "Grand Princess": "Велика княгиня",
    "Great Martyr, Equal-to-the-Apostles": "Великомученик, рівноапостольний",
    "Great Prince, Martyr": "Великий князь, мученик",
    "Great-martyr": "Великомученик",
    "Great-martyr, Prince": "Великомученик, князь",
    "Hermit": "Пустельник",
    "Hermits": "Пустельники",
    "Hierarchs": "Святителі",
    "Hieromartyr (Hermit)": "Священномученик (пустельник)",
    "Hieromartyr, Apostle": "Священномученик, апостол",
    "Hieromartyr, Archbishop": "Священномученик, архієпископ",
    "Hieromartyr, Archimandrite": "Священномученик, архімандрит",
    "Hieromartyr, Archpriest": "Священномученик, протоієрей",
    "Hieromartyr, Bishop": "Священномученик, єпископ",
    "Hieromartyr, Confessor": "Священномученик, сповідник",
    "Hieromartyr, Deacon": "Священномученик, диякон",
    "Hieromartyr, Patriarch": "Священномученик, патріарх",
    "Hieromartyr, Pope": "Священномученик, папа Римський",
    "Hieromartyr, and his son": "Священномученик і син його",
    "Hieromartyrs": "Священномученики",
    "Hieromonk": "Ієромонах",
    "Hieroschemamonk": "Ієросхимонах",
    "High Priest": "Первосвященник",
    "Icon of the Mother of God": "Ікона Божої Матері",
    "King and Martyr": "Цар і мученик",
    "King and Prophet": "Цар і пророк",
    "Laymen": "Миряни",
    "Martyrs": "Мученики",
    "Master Builders, Monks": "Зодчі, ченці",
    "Metropolitan": "Митрополит",
    "Metropolitan, Equal-to-the-Apostles": "Митрополит, рівноапостольний",
    "Monastic Martyr": "Преподобномученик",
    "Monastic Martyrs": "Преподобномученики",
    "Monastic New Martyr": "Преподобномученик новий",
    "Monastics": "Ченці",
    "Monk": "Чернець",
    "Monk (Founder)": "Чернець (засновник)",
    "Monk (Hermit)": "Чернець (пустельник)",
    "Monk (elder)": "Чернець (старець)",
    "Monk (hermit)": "Чернець (пустельник)",
    "Monk (novice)": "Чернець (послушник)",
    "Monk (recluse)": "Чернець (затворник)",
    "Monk (stylite)": "Чернець (стовпник)",
    "Monk, Church Father": "Чернець, отець Церкви",
    "Monk, Confessor": "Чернець, сповідник",
    "Monk, Elder": "Чернець, старець",
    "Monk, Hymnographer": "Чернець, піснописець",
    "Monk, Martyr": "Чернець, мученик",
    "Monk, Recluse": "Чернець, затворник",
    "Monk, Unmercenary Physician": "Чернець, безсрібник-лікар",
    "Monk, former Great Zhupan": "Чернець, колишній великий жупан",
    "Monk-martyr": "Преподобномученик",
    "Monk-martyrs": "Преподобномученики",
    "Monks": "Ченці",
    "Monks (Founders)": "Ченці (засновники)",
    "Mother": "Мати",
    "Myrrhbearer": "Мироносиця",
    "New Martyrs": "Новомученики",
    "New Martyrs and Confessors": "Новомученики і сповідники",
    "Nun": "Черниця",
    "Nun-martyr": "Преподобномучениця",
    "Patriarch": "Патріарх",
    "Patriarch, Church Father": "Патріарх, отець Церкви",
    "Patriarch, Confessor": "Патріарх, сповідник",
    "Patriarch, Hieromartyr": "Патріарх, священномученик",
    "Physician": "Лікар",
    "Physicians": "Лікарі",
    "Pope": "Папа Римський",
    "Pope of Rome, Confessor": "Папа Римський, сповідник",
    "Presbyter and Deacon": "Пресвітер і диякон",
    "Presbyters, Confessors": "Пресвітери, сповідники",
    "Priest": "Ієрей",
    "Prince": "Князь",
    "Prince of Moldavia": "Господар Молдавський",
    "Prince, Passion-Bearer": "Князь, страстотерпець",
    "Princes": "Князі",
    "Princess": "Княгиня",
    "Princess, Nun": "Княгиня, черниця",
    "Proconsul (military commander)": "Проконсул (воєвода)",
    "Prophet and Forerunner": "Пророк і Предтеча",
    "Prophetess": "Пророчиця",
    "Protomartyr": "Первомученик",
    "Protopresbyter": "Протопресвітер",
    "Recluse": "Затворник",
    "Right-believing Prince": "Благовірний князь",
    "Right-believing Prince (Monk)": "Благовірний князь (чернець)",
    "Right-believing Prince and Princess": "Благовірні князь і княгиня",
    "Right-believing Prince, Passion-bearer": "Благовірний князь, страстотерпець",
    "Right-believing Princess (Nun)": "Благовірна княгиня (черниця)",
    "Right-believing Princess, Martyr": "Благовірна княгиня, мучениця",
    "Righteous (Child)": "Праведний (отрок)",
    "Righteous (Children)": "Праведні (отроки)",
    "Righteous (Unmercenary)": "Праведний (безсрібник)",
    "Righteous Forefather": "Праведний праотець",
    "Righteous Virgin": "Праведна діва",
    "Righteous, Priest": "Праведний, ієрей",
    "Roman soldier": "Римський воїн",
    "Schemamonk": "Схимонах",
    "Synaxis": "Собор",
    "Tsar and Imperial Family": "Цар і Царська родина",
    "Unmercenary Martyrs": "Безсрібники-мученики",
    "Venerable": "Преподобний",
    "Venerable Prince": "Преподобний князь",
    "Venerable Princess": "Преподобна княгиня",
    "Virgin": "Діва",
    "Virgin Martyrs": "Мучениці-діви",
    "Virgin-martyr": "Мучениця-діва",
    "Youths": "Отроки",
})


# The places, which are not a list but a grammar: a card names a town, a
# province and a country in one line, and the same town appears on twenty
# other cards inside a different line. The pieces are rendered once here and
# the wholes are assembled from them, so a town cannot be spelled one way on
# one card and another way on the next.
PARTS = {}


def expand(phrases):
    """The compounds, assembled from the parts above.

    Only the place line is built here - a town and a province and a country
    set down in one line. The title a card hangs on a name is not built,
    because Ukrainian does not form it with a preposition the way Romanian
    forms it with din: "of Ancyra" is Анкірський, an adjective agreeing with
    the saint, and "of the Kyiv Caves" is Києво-Печерський. Those are
    written out in TEXT, as Russian writes them, since no rule assembles
    them from the name of the town.
    """
    out = {}
    for p in phrases:
        bits = p.split(", ")
        if all(b in PARTS for b in bits):
            out[p] = ", ".join(PARTS[b] for b in bits)
    return out
