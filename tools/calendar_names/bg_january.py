"""Bulgarian Patriarchate calendar forms for fixed January commemorations."""

SOURCES = (
    "https://bg-patriarshia.bg/api/calendar/2026",
    "https://bg-patriarshia.bg/api/calendar/2023",
    "https://bg-patriarshia.bg/api/calendar/2021",
    "https://bg-patriarshia.bg/api/calendar/2018",
)

TEXT = {
    # 01-01
    "The Circumcision of our Lord and Savior Jesus Christ": "Обрезание Господне",
    "Saint Basil the Great, Archbishop of Caesarea in Cappadocia": "Св. Василий Велики",
    "Martyr Basil of Ancyra": "Св. мчк Василий Анкирски",
    "Saint Emilia, Mother of Saint Basil the Great": "Св. Емилия",

    # 01-02
    "Forefeast of the Theophany of our Lord and Savior Jesus Christ": "Предпразненство на св. Богоявление",
    "Repose of Venerable Seraphim, Wonderworker of Sarov": "Преп. Серафим Саровски Чудотворец",
    "Saint Sylvester, Pope of Rome": "Св. Силвестър, папа Римски",

    # 01-03
    "Holy Prophet Malachi": "Св. прор. Малахия",
    "Martyr Gordius at Caesarea, in Cappadocia": "Св. мчк Гордий",

    # 01-04
    "Synaxis of the Seventy Apostles": "Събор на св. 70 апостоли",
    "Venerable Theoctistus, Abbot at Cucomo, in Sicily": "Преп. Теоктист",

    # 01-05
    "Eve of the Theophany of our Lord and Savior Jesus Christ": "Водици",
    "Hieromartyr Theopemptus, Bishop of Nicomedia, and Martyr Theonas": "Св. мчци Теопемт и Теона",
    "Venerable Synkletika of Alexandria": "Преп. Синклитикия",
    "Prophet Micah": "Св. прор. Михей",

    # 01-06
    "Feast of the Theophany of our Lord and Savior Jesus Christ": "Св. Богоявление",

    # 01-07
    "Synaxis of the Holy Glorious Prophet, Forerunner and Baptist John": "Св. Йоан Кръстител",

    # 01-08
    "Venerable George the Chozebite, Abbot": "Преп. Георги Хозевит",
    "Venerable Domnica of Constantinople": "Преп. Домника",
    "Saint Emilian the Confessor, Bishop of Cyzicus": "Св. Емилиан изповедник",

    # 01-09
    "Martyr Polyeuktos of Melitene in Armenia": "Св. мчк Полиевкт",
    "Prophet Shemaiah (Samaia or Semeias)": "Св. прор. Самей",

    # 01-10
    "Saint Gregory, Bishop of Nyssa": "Св. Григорий, еп. Нисийски",
    "Saint Dometian, Bishop of Melitene": "Преп. Дометиан, еп. Мелитински",
    "Saint Marcian the Presbyter in Constantinople": "Св. Маркиан",

    # 01-11
    "Venerable Theodosius the Great, the Cenobiarch": "Преп. Теодосий Велики",
    "Saint Theodosius of Antioch": "Преп. Теодосий Антиохийски",

    # 01-12
    "Martyr Tatiana of Rome, and those who suffered with her": "Св. мчца Татяна Римска",
    "Martyr Mertius of Mauretania": "Св. мчк Мертий",

    # 01-13
    "Martyrs Hermylus and Stratonicus of Belgrade": "Св. мчци Ермил и Стратоник",
    "Venerable Irenarchus the Recluse of Rostov": "Преп. Иринарх Ростовски",

    # 01-14
    "Leavetaking of the Theophany of our Lord and Savior Jesus Christ": "Отдание на Богоявление",
    "Holy Monastic Fathers slain at Sinai and Raithu": "Преп. отци, избити в Синай и Раита",
    "Saint Nino (Nina), Equal of the Apostles, Enlightener of Georgia": "Св. равноап. Нина",

    # 01-16
    "Veneration of the Precious Chains of the Holy and All-Glorious Apostle Peter": "Честни вериги на св. ап. Петър",

    # 01-17
    "Venerable and God-bearing Father Anthony the Great": "Преп. Антоний Велики",

    # 01-19
    "Venerable Macarius the Great of Egypt": "Преп. Макарий Египетски",
    "Saint Mark, Archbishop of Ephesus": "Св. Марк, еп. Ефески",

    # 01-20
    "Venerable Euthymius the Great": "Преп. Евтимий Велики",

    # 01-21
    "Venerable Maximus the Confessor": "Преп. Максим Изповедник",
    "Martyr Neophytus of Nicea": "Св. мчк Неофит",

    # 01-22
    "Apostle Timothy of the Seventy": "Св. ап. Тимотей",
    "Monastic Martyr Anastasius the Persian": "Прпмчк Анастасий Перски",

    # 01-23
    "Hieromartyr Clement, Bishop of Ancyra, and Martyr Agathangelus": "Св. свщмчк Климент, еп. Анкирски. Св. мчк Агатангел",

    # 01-24
    "Venerable Xenia of Rome, and her two female servants": "Преп. Ксения Римлянка",
    "Martyr Babylas of Sicily, and his two disciples: Timothy and Agapius": "Мчк Вавила",

    # 01-25
    "Saint Gregory the Theologian, Archbishop of Constantinople": "Св. Григорий Богослов, архиепископ Константинополски",

    # 01-26
    "Venerable Xenophon, his wife, Mary, and their two sons, Arcadius and John, of Constantinople": "Преп. Ксенофонт и дружината му",

    # 01-27
    "Translation of the relics of Saint John Chrysostom, Archbishop of Constantinople": "Пренасяне мощите на св. Йоан Златоуст",

    # 01-28
    "Venerable Ephraim the Syrian": "Преп. Ефрем Сириец",

    # 01-29
    "Translation of the relics of the Hieromartyr Ignatius, the Godbearer and Bishop of Antioch": "Пренасяне мощите на св. Игнатий Богоносец",

    # 01-30
    "Synaxis of the Ecumenical Teachers and Hierarchs: Basil the Great, Gregory the Theologian, and John Chrysostom": "Св. Трисветители велики архиереи: Василий Велики, Григорий Богослов и Йоан Златоуст",
    "Hieromartyr Hippolytus, and those with him": "Св. свщмчк Иполит, папа Римски",

    # 01-31
    "Holy Wonderworkers and Unmercenaries Cyrus and John, and those with them": "Св. безсребреници и чудотворци Кир и Йоан",
}
