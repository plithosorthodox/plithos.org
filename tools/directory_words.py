#!/usr/bin/env python3
"""
The words the directory page speaks, in the twenty-two languages.

Gathered where the site already had them and written where it did not, in
the register each language uses on its own pages here. The gathered ones
are taken rather than composed:

  - the word for Church is the one in the Creed as this site publishes it,
    checked against every file that language has: Bengali's Creed reads
    chart twenty-two times against girja three thousand, so girja is the
    Bengali word and the Creed is the outlier; Syriac writes the plural
    with seyame, attested two hundred and thirty-three times.
  - All, and the line for an empty result, come from the Glossary.
  - the word for Language comes from the shared interface bundle.
  - what a body is called - Eparchy, Metropolis, Diocese, Archdiocese,
    Metropolia and the rest - is read off the names each language already
    gives these very bodies in tools/directory_names, which carry the word
    inside them: Митрополия Бельгии, Μητρόπολη Βελγίου, Eparhia Mexicului.
    Five of those words cover all but a few dozen rows and every language
    has them.

Not every language divides them where English does, and none is made to.
Russian, Ukrainian, Serbian, Bulgarian, Romanian, Arabic, Georgian,
Armenian, Syriac, Swahili, Chinese, Japanese, Korean, Hindi, Bengali and
Urdu have one word where English has both Eparchy and Diocese, because a
Ukrainian eparchy and a Romanian diocese are the same kind of body and only
the English of their own Churches differs. Hindi, Bengali and Urdu likewise
write one word for a Metropolis and an Archdiocese. Where a language has
no word at all for one of the rarer ranks it keeps the English, which is
visible, rather than being given something composed for the occasion.

Country names are not here at all. The browser knows them in every one of
these languages and gives the received form, so the page asks it rather
than keeping a table of two hundred names that would have to be written by
someone who does not read most of them.

    python3 tools/directory_words.py --check
    python3 tools/directory_words.py --write

The audit does not have to reach zero and cannot. A city this site has never
had occasion to name has no form in the corpus to gather, and Tokyo, Tirana,
Skopje, Presov, Tallinn and Syosset are in that position in most of these
languages: no saint here is of any of them. What the audit is for is the
other case - a word written by ear when the site already had one - and every
word it reports is declared in its language's file, with what was gathered
and what was built said apart.
"""
import argparse
import bisect
import glob
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import directory_names

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory-i18n.v1.json"

LANGS = "en el ru ro uk de es ar fr pt it sr ka zh ja ko sw hy arc hi bn ur bg".split()

# The word for Churches, read out of the Creed and settled against each
# language's own corpus. See the module docstring for the two that needed
# settling.
CHURCHES = {
 "en": "Churches",      "el": "Εκκλησίες",     "ru": "Церкви",
 "ro": "Biserici",      "uk": "Церкви",        "de": "Kirchen",
 "es": "Iglesias",      "ar": "كنائس",          "fr": "Églises",
 "pt": "Igrejas",       "it": "Chiese",        "sr": "Цркве",
 "ka": "ეკლესიები",      "zh": "教会",           "ja": "教会",
 "ko": "교회",           "sw": "Makanisa",      "hy": "Եկեղեցիներ",
 "arc": "ܥܕ̈ܬܐ",          "hi": "कलीसियाएँ",       "bn": "গির্জা",
 "ur": "کلیسیائیں",       "bg": "Църкви",
}

# Everything the page says in its own voice.
W = {
"en": dict(
 lede="The Orthodox Churches of the world, with the seat and the address each one publishes.",
 note="A body is listed here because an autocephalous Church names it among its own. Where the Churches differ, the entry says who names it, and Plithos does not say which is right.",
 spread="Where a people has gone abroad, more than one Church may keep a diocese in the same country, and they are different bodies with different histories rather than duplicates of one another. Every row names the Church it belongs to.",
 partial="This list is being built. A Church is here once it has been read from an official source and so are its dioceses, which means a Church may have many more dioceses than are shown, and a Church may be missing altogether.",
 ph="Search by name, city or country",
 gauto="Autocephalous Churches", gnom="Autonomous Churches",
 address=u"Address", website=u"Website", founded=u"Founded",
 languages=u"Languages",
 dioceses=u"Dioceses", administered=u"Administered",
 confirmed="Confirmed",
 ranks={"Eparchy": u"Eparchy", "Metropolis": u"Metropolis",
  "Diocese": u"Diocese", "Archdiocese": u"Archdiocese",
  "Metropolia": u"Metropolia", "Exarchate": u"Exarchate",
  "Patriarchal Exarchate": u"Patriarchal Exarchate",
  "Patriarchal Commissaryship": u"Patriarchal Commissaryship",
  "Metropolitanate": u"Metropolitanate",
  "Archbishopric": u"Archbishopric", "Bishopric": u"Bishopric",
  "Episcopate": u"Episcopate",
  "Metropolitan District": u"Metropolitan District",
  "Eparchial Synod": u"Eparchial Synod",
  "Stavropegion": u"Stavropegion", "Deanery": u"Deanery",
  "Vicariate": u"Vicariate", "Ordinariate": u"Ordinariate",
  "Patriarchal and Stavropegic Monastery": u"Patriarchal and Stavropegic Monastery",
  "Royal, Patriarchal and Stavropegic Monastery": u"Royal, Patriarchal and Stavropegic Monastery"}),
"el": dict(
 lede="Οι Ορθόδοξες Εκκλησίες του κόσμου, με την έδρα και τη διεύθυνση που δημοσιεύει η καθεμία.",
 note="Μια Εκκλησία γράφεται εδώ επειδή μια αυτοκέφαλη Εκκλησία την αναγνωρίζει ως δική της. Όπου οι Εκκλησίες διαφέρουν, η εγγραφή λέει ποια την αναγνωρίζει· το Plithos δεν λέει ποια έχει δίκιο.",
 ph="Αναζήτηση με όνομα, πόλη ή χώρα",
 gauto="Αυτοκέφαλες Εκκλησίες", gnom="Αυτόνομες Εκκλησίες",
 address=u"Διεύθυνση",
 dioceses=u"Επισκοπές", confirmed="Βεβαιωμένο",
 ranks={"Eparchy": u"Επαρχία", "Metropolis": u"Μητρόπολη",
  "Diocese": u"Επισκοπή", "Archdiocese": u"Αρχιεπισκοπή",
  "Metropolia": u"Μητρόπολη", "Exarchate": u"Εξαρχία",
  "Patriarchal Exarchate": u"Πατριαρχική Εξαρχία",
  "Metropolitanate": u"Μητρόπολη", "Archbishopric": u"Αρχιεπισκοπή",
  "Bishopric": u"Επισκοπή", "Episcopate": u"Επισκοπή"}),
"ru": dict(
 lede="Православные Церкви мира, с кафедрой и адресом, которые каждая из них объявляет.",
 note="Церковь внесена сюда потому, что автокефальная Церковь признаёт её своей. Там, где Церкви расходятся, запись говорит, кто её признаёт; Plithos не говорит, кто прав.",
 ph="Поиск по названию, городу или стране",
 gauto="Автокефальные Церкви", gnom="Автономные Церкви",
 address=u"Адрес",
 dioceses=u"Епархии", confirmed="Подтверждено",
 ranks={"Eparchy": u"Епархия", "Metropolis": u"Митрополия",
  "Diocese": u"Епархия", "Archdiocese": u"Архиепископия",
  "Metropolia": u"Митрополия", "Exarchate": u"Экзархат",
  "Patriarchal Exarchate": u"Патриарший экзархат",
  "Metropolitanate": u"Митрополия",
  "Archbishopric": u"Архиепископия", "Bishopric": u"Епископия",
  "Episcopate": u"Епископия",
  "Metropolitan District": u"Митрополичий округ",
  "Deanery": u"Благочиние"}),
"ro": dict(
 lede="Bisericile Ortodoxe ale lumii, cu scaunul și adresa pe care fiecare le face cunoscute.",
 note="Un așezământ este trecut aici pentru că o Biserică autocefală îl recunoaște ca al său. Acolo unde Bisericile se despart, însemnarea spune cine îl recunoaște; Plithos nu spune cine are dreptate.",
 ph="Caută după nume, oraș sau țară",
 gauto="Biserici autocefale", gnom="Biserici autonome",
 address=u"Adresă",
 dioceses=u"Eparhii", confirmed="Confirmat",
 ranks={"Eparchy": u"Eparhie", "Metropolis": u"Mitropolie",
  "Diocese": u"Eparhie", "Archdiocese": u"Arhiepiscopie",
  "Metropolia": u"Mitropolie", "Exarchate": u"Exarhat",
  "Patriarchal Exarchate": u"Exarhat patriarhal",
  "Metropolitanate": u"Mitropolie",
  "Archbishopric": u"Arhiepiscopie", "Bishopric": u"Episcopie",
  "Episcopate": u"Episcopie"}),
"uk": dict(
 lede="Православні Церкви світу, з кафедрою та адресою, які кожна з них подає.",
 note="Церква внесена сюди тому, що автокефальна Церква визнає її своєю. Там, де Церкви розходяться, запис каже, хто її визнає; Plithos не каже, хто має рацію.",
 ph="Пошук за назвою, містом або країною",
 gauto="Автокефальні Церкви", gnom="Автономні Церкви",
 address=u"Адреса",
 dioceses=u"Єпархії", confirmed="Підтверджено",
 ranks={"Eparchy": u"Єпархія", "Metropolis": u"Митрополія",
  "Diocese": u"Єпархія", "Archdiocese": u"Архієпископія",
  "Metropolia": u"Митрополія", "Exarchate": u"Екзархат",
  "Patriarchal Exarchate": u"Патріарший екзархат",
  "Metropolitanate": u"Митрополія",
  "Archbishopric": u"Архієпископія", "Bishopric": u"Єпископія",
  "Episcopate": u"Єпископія",
  "Metropolitan District": u"Митрополичий округ"}),
"de": dict(
 lede="Die orthodoxen Kirchen der Welt, mit dem Sitz und der Anschrift, die jede von ihnen veröffentlicht.",
 note="Eine Kirche steht hier, weil eine autokephale Kirche sie zu den ihren zählt. Wo die Kirchen auseinandergehen, nennt der Eintrag, wer sie zählt; Plithos sagt nicht, wer recht hat.",
 ph="Suche nach Name, Stadt oder Land",
 gauto="Autokephale Kirchen", gnom="Autonome Kirchen",
 address=u"Anschrift",
 dioceses=u"Diözesen", confirmed="Bestätigt",
 ranks={"Eparchy": u"Eparchie", "Metropolis": u"Metropolie",
  "Diocese": u"Diözese", "Archdiocese": u"Erzdiözese",
  "Metropolia": u"Metropolie", "Exarchate": u"Exarchat",
  "Patriarchal Exarchate": u"Patriarchales Exarchat",
  "Metropolitanate": u"Metropolie", "Archbishopric": u"Erzbistum",
  "Bishopric": u"Bistum", "Episcopate": u"Bistum"}),
"es": dict(
 lede="Las Iglesias Ortodoxas del mundo, con la sede y la dirección que cada una publica.",
 note="Una Iglesia figura aquí porque una Iglesia autocéfala la cuenta entre las suyas. Donde las Iglesias difieren, la entrada dice quién la cuenta; Plithos no dice quién tiene razón.",
 ph="Buscar por nombre, ciudad o país",
 gauto="Iglesias autocéfalas", gnom="Iglesias autónomas",
 address=u"Dirección",
 dioceses=u"Diócesis", confirmed="Comprobado",
 ranks={"Eparchy": u"Eparquía", "Metropolis": u"Metrópoli",
  "Diocese": u"Diócesis", "Archdiocese": u"Arzobispado",
  "Metropolia": u"Metrópoli", "Exarchate": u"Exarcado",
  "Patriarchal Exarchate": u"Exarcado patriarcal",
  "Metropolitanate": u"Metrópoli", "Archbishopric": u"Arzobispado",
  "Bishopric": u"Obispado", "Episcopate": u"Obispado"}),
"ar": dict(
 lede="الكنائس الأرثوذكسية في العالم، مع الكرسي والعنوان الذي تنشره كل منها.",
 note="تُدرَج الكنيسة هنا لأن كنيسة مستقلة تعدّها من كنائسها. وحيث تختلف الكنائس، يذكر المدخل من يعدّها، ولا يقول Plithos من على حق.",
 ph="ابحث بالاسم أو المدينة أو البلد",
 gauto="الكنائس المستقلة", gnom="الكنائس ذات الحكم الذاتي",
 address=u"العنوان",
 dioceses=u"أبرشيات", confirmed="تم التثبت",
 ranks={"Eparchy": u"أبرشية", "Metropolis": u"متروبوليتية",
  "Diocese": u"أبرشية", "Archdiocese": u"رئاسة أساقفة",
  "Metropolia": u"متروبوليتية", "Metropolitanate": u"متروبوليتية",
  "Archbishopric": u"رئاسة أساقفة", "Bishopric": u"أبرشية",
  "Episcopate": u"أبرشية"}),
"fr": dict(
 lede="Les Églises orthodoxes du monde, avec le siège et l'adresse que chacune publie.",
 note="Une Église figure ici parce qu'une Église autocéphale la compte parmi les siennes. Là où les Églises diffèrent, la notice dit qui la compte ; Plithos ne dit pas qui a raison.",
 ph="Rechercher par nom, ville ou pays",
 gauto="Églises autocéphales", gnom="Églises autonomes",
 address=u"Adresse",
 dioceses=u"Diocèses", confirmed="Vérifié",
 ranks={"Eparchy": u"Éparchie", "Metropolis": u"Métropole",
  "Diocese": u"Diocèse", "Archdiocese": u"Archidiocèse",
  "Metropolia": u"Métropole", "Exarchate": u"Exarchat",
  "Patriarchal Exarchate": u"Exarchat patriarcal",
  "Metropolitanate": u"Métropole", "Archbishopric": u"Archevêché",
  "Bishopric": u"Évêché", "Episcopate": u"Évêché"}),
"pt": dict(
 lede="As Igrejas Ortodoxas do mundo, com a sede e o endereço que cada uma publica.",
 note="Uma Igreja consta aqui porque uma Igreja autocéfala a conta entre as suas. Onde as Igrejas divergem, a entrada diz quem a conta; o Plithos não diz quem tem razão.",
 ph="Buscar por nome, cidade ou país",
 gauto="Igrejas autocéfalas", gnom="Igrejas autônomas",
 address=u"Endereço",
 dioceses=u"Dioceses", confirmed="Verificado",
 ranks={"Eparchy": u"Eparquia", "Metropolis": u"Metrópole",
  "Diocese": u"Diocese", "Archdiocese": u"Arcebispado",
  "Metropolia": u"Metropolia", "Exarchate": u"Exarcado",
  "Patriarchal Exarchate": u"Exarcado patriarcal",
  "Metropolitanate": u"Metropolia", "Archbishopric": u"Arcebispado",
  "Bishopric": u"Bispado", "Episcopate": u"Bispado"}),
"it": dict(
 lede="Le Chiese ortodosse del mondo, con la sede e l'indirizzo che ciascuna pubblica.",
 note="Una Chiesa figura qui perché una Chiesa autocefala la annovera fra le proprie. Dove le Chiese divergono, la voce dice chi la annovera; Plithos non dice chi abbia ragione.",
 ph="Cerca per nome, citta o paese",
 gauto="Chiese autocefale", gnom="Chiese autonome",
 address=u"Indirizzo",
 dioceses=u"Diocesi", confirmed="Verificato",
 ranks={"Eparchy": u"Eparchia", "Metropolis": u"Metropolia",
  "Diocese": u"Diocesi", "Archdiocese": u"Arcidiocesi",
  "Metropolia": u"Metropolia", "Exarchate": u"Esarcato",
  "Patriarchal Exarchate": u"Esarcato patriarcale",
  "Metropolitanate": u"Metropolitanato",
  "Archbishopric": u"Arcivescovado", "Bishopric": u"Vescovado",
  "Episcopate": u"Vescovado"}),
"sr": dict(
 lede="Православне Цркве света, са седиштем и адресом које свака од њих објављује.",
 note="Црква је уписана овде зато што је аутокефална Црква признаје за своју. Тамо где се Цркве разилазе, запис каже ко је признаје; Plithos не каже ко је у праву.",
 ph="Претрага по имену, граду или земљи",
 gauto="Аутокефалне Цркве", gnom="Аутономне Цркве",
 address=u"Адреса",
 dioceses=u"Епархије", confirmed="Проверено",
 ranks={"Eparchy": u"Епархија", "Metropolis": u"Митрополија",
  "Diocese": u"Епархија", "Archdiocese": u"Архиепископија",
  "Metropolia": u"Митрополија", "Exarchate": u"Егзархат",
  "Patriarchal Exarchate": u"Патријаршијски егзархат",
  "Metropolitanate": u"Митрополија",
  "Archbishopric": u"Архиепископија", "Bishopric": u"Епископија",
  "Episcopate": u"Епископија"}),
"ka": dict(
 lede="მსოფლიოს მართლმადიდებელი ეკლესიები, კათედრითა და მისამართით, რომელსაც თითოეული აქვეყნებს.",
 note="ეკლესია აქ ჩაწერილია იმიტომ, რომ ავტოკეფალური ეკლესია მას თავისად მიიჩნევს. სადაც ეკლესიები განსხვავდებიან, ჩანაწერი ამბობს ვინ მიიჩნევს მას; Plithos არ ამბობს ვინ არის მართალი.",
 ph="ძიება სახელით, ქალაქით ან ქვეყნით",
 gauto="ავტოკეფალური ეკლესიები", gnom="ავტონომიური ეკლესიები",
 address=u"მისამართი",
 dioceses=u"ეპარქიები", confirmed="დამოწმებული",
 ranks={"Eparchy": u"ეპარქია", "Metropolis": u"მიტროპოლია",
  "Diocese": u"ეპარქია", "Archdiocese": u"მთავარეპისკოპოსო",
  "Metropolia": u"მიტროპოლია", "Metropolitanate": u"მიტროპოლია",
  "Archbishopric": u"მთავარეპისკოპოსო", "Bishopric": u"ეპარქია",
  "Episcopate": u"ეპარქია"}),
"zh": dict(
 lede="世界各地的正教会，附有各自公布的驻地与地址。",
 note="列在此处的教会，是因为有自主教会将其列为自己的教会。各教会看法不同之处，条目只说明是谁将其列入，Plithos 不判断谁对。",
 ph="按名称、城市或国家搜索",
 gauto="自主教会", gnom="自治教会",
 address=u"地址",
 dioceses=u"教区", confirmed="已核实",
 ranks={"Eparchy": u"教区", "Metropolis": u"都主教区", "Diocese": u"教区",
  "Archdiocese": u"大主教区", "Metropolia": u"都主教区",
  "Metropolitanate": u"都主教区", "Archbishopric": u"大主教区",
  "Bishopric": u"教区", "Episcopate": u"教区"}),
"ja": dict(
 lede="世界の正教会と、それぞれが公にしている座所と住所。",
 note="ここに載る教会は、独立教会がこれを自らのものとして挙げているからです。教会の間で異なる場合、項目は誰が挙げているかを記すのみで、Plithos はどちらが正しいかを述べません。",
 ph="名称、都市、国で検索",
 gauto="独立教会", gnom="自治教会",
 address=u"住所",
 dioceses=u"教区", confirmed="確認済み",
 ranks={"Eparchy": u"教区", "Metropolis": u"府主教区", "Diocese": u"教区",
  "Archdiocese": u"大主教区", "Metropolia": u"府主教区",
  "Metropolitanate": u"府主教区", "Archbishopric": u"大主教区",
  "Bishopric": u"教区", "Episcopate": u"教区"}),
"ko": dict(
 lede="세계의 정교회와 각 교회가 공표한 소재지와 주소.",
 note="여기에 실린 교회는 독립 교회가 그 교회를 자기 교회로 인정하기 때문입니다. 교회마다 다를 때에는 누가 인정하는지를 적을 뿐, Plithos는 어느 쪽이 옳은지 말하지 않습니다.",
 ph="이름, 도시, 나라로 검색",
 gauto="독립 교회", gnom="자치 교회",
 address=u"주소",
 dioceses=u"교구", confirmed="확인됨",
 ranks={"Eparchy": u"교구", "Metropolis": u"관구", "Diocese": u"교구",
  "Archdiocese": u"대교구", "Metropolia": u"관구",
  "Metropolitanate": u"관구", "Archbishopric": u"대교구",
  "Bishopric": u"교구", "Episcopate": u"교구"}),
"sw": dict(
 lede="Makanisa ya Orthodoksi ya ulimwengu, pamoja na makao na anwani ambayo kila moja hutangaza.",
 note="Kanisa liko katika orodha hii kwa sababu Kanisa huru linahesabu kuwa lake. Makanisa yakitofautiana, kiingilio husema ni nani anahesabu; Plithos hasemi ni nani yuko sahihi.",
 ph="Tafuta kwa jina, mji au nchi",
 gauto="Makanisa huru", gnom="Makanisa yenye kujitegemea",
 address=u"Anwani",
 dioceses=u"Dayosisi", confirmed="Imethibitishwa",
 ranks={"Eparchy": u"Dayosisi", "Metropolis": u"Mitropolia",
  "Diocese": u"Dayosisi", "Archdiocese": u"Jimbo Kuu",
  "Metropolia": u"Mitropolia", "Metropolitanate": u"Mitropolia",
  "Archbishopric": u"Jimbo Kuu", "Bishopric": u"Dayosisi",
  "Episcopate": u"Dayosisi"}),
"hy": dict(
 lede="Աշխարհի ուղղափառ Եկեղեցիները՝ իրենց աթոռով եւ հասցեով, ինչպէս իւրաքանչիւրը հրապարակում է։",
 note="Եկեղեցին այստեղ գրուած է, որովհետեւ ինքնագլուխ Եկեղեցին այն իւրն է համարում։ Ուր Եկեղեցիները տարբերւում են, գրառումը ասում է, թէ ով է այն համարում. Plithos չի ասում, թէ ով է իրաւացի։",
 ph="Որոնում ըստ անուան, քաղաքի կամ երկրի",
 gauto="Ինքնագլուխ Եկեղեցիներ", gnom="Ինքնավար Եկեղեցիներ",
 address=u"Հասցե",
 dioceses=u"Թեմեր", confirmed="Հաստատուած",
 ranks={"Eparchy": u"Թեմ", "Metropolis": u"Մետրոպոլիտութիւն",
  "Diocese": u"Թեմ", "Archdiocese": u"Արքեպիսկոպոսութիւն",
  "Metropolia": u"Մետրոպոլիտութիւն",
  "Metropolitanate": u"Մետրոպոլիտութիւն",
  "Archbishopric": u"Արքեպիսկոպոսութիւն", "Bishopric": u"Թեմ",
  "Episcopate": u"Թեմ"}),
"arc": dict(
 lede="ܥܕ̈ܬܐ ܬܪ̈ܝܨܝ ܫܘܒܚܐ ܕܥܠܡܐ ܥܡ ܟܘܪܣܝܐ ܘܐܬܪܐ ܕܟܠ ܚܕܐ ܡܘܕܥܐ.",
 note="ܥܕܬܐ ܟܬܝܒܐ ܗܪܟܐ ܡܛܠ ܕܥܕܬܐ ܕܢܦܫܗ̇ ܫܠܝܛܐ ܚܫܒܐ ܠܗ̇ ܡܢ ܕܝܠܗ̇. ܐܝܟܐ ܕܥܕ̈ܬܐ ܦܪ̈ܝܫܢ ܟܬܒܐ ܐܡܪ ܡܢܘ ܚܫܒ ܠܗ̇. ܘPlithos ܠܐ ܐܡܪ ܡܢܘ ܫܪܝܪܐ.",
 ph="ܒܥܝ ܒܫܡܐ ܐܘ ܡܕܝܢܬܐ ܐܘ ܐܬܪܐ",
 gauto="ܥܕ̈ܬܐ ܕܢܦܫܗܝܢ ܫܠܝ̈ܛܢ", gnom="ܥܕ̈ܬܐ ܕܡܕܒܪ̈ܢ ܢܦܫܗܝܢ",
 address=u"ܕܘܟܬܐ",
 dioceses=u"ܡܪ̈ܥܝܬܐ", confirmed="ܐܫܬܪܪ",
 ranks={"Eparchy": u"ܡܪܥܝܬܐ", "Metropolis": u"ܗܘܦܪܟܝܐ",
  "Diocese": u"ܡܪܥܝܬܐ", "Archdiocese": u"ܪܝܫ ܐܦܣܩܘܦܘܬܐ",
  "Metropolia": u"ܗܘܦܪܟܝܐ", "Metropolitanate": u"ܗܘܦܪܟܝܐ",
  "Archbishopric": u"ܪܝܫ ܐܦܣܩܘܦܘܬܐ", "Bishopric": u"ܡܪܥܝܬܐ",
  "Episcopate": u"ܡܪܥܝܬܐ"}),
"hi": dict(
 lede="संसार की रूढ़िवादी कलीसियाएँ, उनके आसन और पते के साथ जो प्रत्येक प्रकाशित करती है।",
 note="कोई कलीसिया यहाँ इसलिए दर्ज है कि कोई स्वतंत्र कलीसिया उसे अपनी मानती है। जहाँ कलीसियाओं में भेद है, वहाँ प्रविष्टि बताती है कि उसे कौन मानता है; Plithos यह नहीं कहता कि कौन सही है।",
 ph="नाम, नगर या देश से खोजें",
 gauto="स्वतंत्र कलीसियाएँ", gnom="स्वायत्त कलीसियाएँ",
 address=u"पता",
 dioceses=u"धर्मप्रांत", confirmed="पुष्ट",
 ranks={"Eparchy": u"धर्मप्रांत", "Metropolis": u"महाधर्मप्रांत",
  "Diocese": u"धर्मप्रांत", "Archdiocese": u"महाधर्मप्रांत",
  "Metropolia": u"महाधर्मप्रांत",
  "Metropolitanate": u"महाधर्मप्रांत",
  "Archbishopric": u"महाधर्मप्रांत", "Bishopric": u"धर्मप्रांत",
  "Episcopate": u"धर्मप्रांत"}),
"bn": dict(
 lede="জগতের অর্থোডক্স গির্জা, প্রত্যেকের প্রকাশিত আসন ও ঠিকানা সহ।",
 note="কোনো গির্জা এখানে রয়েছে কারণ কোনো স্বাধীন গির্জা তাকে নিজের বলে গণ্য করে। যেখানে গির্জাগুলির মধ্যে পার্থক্য, সেখানে ভুক্তি বলে কে তাকে গণ্য করে; Plithos বলে না কে ঠিক।",
 ph="নাম, শহর বা দেশ দিয়ে খুঁজুন",
 gauto="স্বাধীন গির্জা", gnom="স্বায়ত্তশাসিত গির্জা",
 address=u"ঠিকানা",
 dioceses=u"ধর্মপ্রদেশ", confirmed="নিশ্চিত",
 ranks={"Eparchy": u"ধর্মপ্রদেশ", "Metropolis": u"মহাধর্মপ্রদেশ",
  "Diocese": u"ধর্মপ্রদেশ", "Archdiocese": u"মহাধর্মপ্রদেশ",
  "Metropolia": u"মহাধর্মপ্রদেশ",
  "Metropolitanate": u"মহাধর্মপ্রদেশ",
  "Archbishopric": u"মহাধর্মপ্রদেশ", "Bishopric": u"ধর্মপ্রদেশ",
  "Episcopate": u"ধর্মপ্রদেশ"}),
"ur": dict(
 lede="دنیا کی راست عقیدہ کلیسیائیں، اُس کرسی اور پتے کے ساتھ جو ہر ایک شائع کرتی ہے۔",
 note="کوئی کلیسیا یہاں اِس لیے درج ہے کہ کوئی خود مختار کلیسیا اُسے اپنی شمار کرتی ہے۔ جہاں کلیسیاؤں میں فرق ہو، وہاں اندراج بتاتا ہے کہ اُسے کون شمار کرتا ہے؛ Plithos یہ نہیں کہتا کہ کون درست ہے۔",
 ph="نام، شہر یا ملک سے تلاش کریں",
 gauto="خود مختار کلیسیائیں", gnom="خود اختیار کلیسیائیں",
 address=u"پتہ",
 dioceses=u"اسقفی حلقہ", confirmed="تصدیق شدہ",
 ranks={"Eparchy": u"اسقفی حلقہ", "Metropolis": u"سردار اسقفی حلقہ",
  "Diocese": u"اسقفی حلقہ", "Archdiocese": u"سردار اسقفی حلقہ",
  "Metropolia": u"سردار اسقفی حلقہ",
  "Metropolitanate": u"سردار اسقفی حلقہ",
  "Archbishopric": u"سردار اسقفی حلقہ", "Bishopric": u"اسقفی حلقہ",
  "Episcopate": u"اسقفی حلقہ"}),
"bg": dict(
 lede="Православните църкви по света, със седалището и адреса, които всяка от тях публикува.",
 note="Една църковна структура е включена тук, защото автокефална църква я посочва като своя. Когато църквите се различават, записът казва коя я посочва; Plithos не казва коя е права.",
 spread="Когато един народ се е преселил в чужбина, повече от една църква може да има епархия в една и съща държава. Това са различни църковни структури с различна история, а не повторения на една и съща. Всеки ред посочва към коя църква принадлежи.",
 partial="Този списък се изгражда. Една църква и нейните епархии са включени тук, след като бъдат прочетени от това, което самата Църква публикува. Затова една църква може да има много повече епархии от показаните, а някоя църква може изобщо да липсва.",
 ph="Търсене по име, град или държава",
 gauto="Автокефални църкви", gnom="Автономни църкви",
 address=u"Адрес", website="Уебсайт", founded="Основана",
 dioceses=u"Епархии", administered="Администрирани", confirmed="Потвърдено",
 all="Всички", none="Няма намерени църкви.", language="Език",
 ranks={"Eparchy": u"Епархия", "Metropolis": u"Митрополия",
  "Diocese": u"Епархия", "Archdiocese": u"Архиепископия",
  "Metropolia": u"Митрополия", "Exarchate": u"Екзархия",
  "Patriarchal Exarchate": u"Патриаршеска екзархия",
  "Patriarchal Commissaryship": u"Патриаршеско наместничество",
  "Metropolitanate": u"Митрополия",
  "Archbishopric": u"Архиепископия", "Bishopric": u"Епископия",
  "Episcopate": u"Епископия",
  "Metropolitan District": u"Митрополитски окръг",
  "Eparchial Synod": u"Епархийски синод",
  "Stavropegion": u"Ставропигиален манастир",
  "Deanery": u"Благочиние", "Vicariate": u"Викариатство",
  "Ordinariate": u"Ординариат",
  "Patriarchal and Stavropegic Monastery": u"Свещен патриаршески и ставропигиален манастир",
  "Royal, Patriarchal and Stavropegic Monastery": u"Свещен царски патриаршески и ставропигиален манастир"}),
}

# The parish-scale branches speak only when a reader opens a diocese or asks
# for a filtered result. These words stay together because every language
# needs the complete set before that part of the directory can be published.
BRANCH_UI = {
 "en": dict(kindFilter="Type", kindChurches="Churches", kindDioceses="Dioceses",
  kindParishes="Parishes", kindMonasteries="Monasteries",
  communities="Parishes and monasteries", loading="Loading...",
  loadFailed="This part of the directory could not be loaded.", retry="Try again"),
 "el": dict(kindFilter="Τύπος", kindChurches="Εκκλησίες", kindDioceses="Επισκοπές",
  kindParishes="Ενορίες", kindMonasteries="Μονές",
  communities="Ενορίες και μονές", loading="Φόρτωση...",
  loadFailed="Δεν ήταν δυνατή η φόρτωση αυτού του μέρους του καταλόγου.", retry="Δοκιμάστε ξανά"),
 "ru": dict(kindFilter="Тип", kindChurches="Церкви", kindDioceses="Епархии",
  kindParishes="Приходы", kindMonasteries="Монастыри",
  communities="Приходы и монастыри", loading="Загрузка...",
  loadFailed="Не удалось загрузить эту часть справочника.", retry="Повторить"),
 "ro": dict(kindFilter="Tip", kindChurches="Biserici", kindDioceses="Eparhii",
  kindParishes="Parohii", kindMonasteries="Mănăstiri",
  communities="Parohii și mănăstiri", loading="Se încarcă...",
  loadFailed="Această parte a directorului nu a putut fi încărcată.", retry="Încercați din nou"),
 "uk": dict(kindFilter="Тип", kindChurches="Церкви", kindDioceses="Єпархії",
  kindParishes="Парафії", kindMonasteries="Монастирі",
  communities="Парафії та монастирі", loading="Завантаження...",
  loadFailed="Не вдалося завантажити цю частину довідника.", retry="Спробувати ще раз"),
 "de": dict(kindFilter="Art", kindChurches="Kirchen", kindDioceses="Diözesen",
  kindParishes="Kirchengemeinden", kindMonasteries="Klöster",
  communities="Kirchengemeinden und Klöster", loading="Wird geladen...",
  loadFailed="Dieser Teil des Verzeichnisses konnte nicht geladen werden.", retry="Erneut versuchen"),
 "es": dict(kindFilter="Tipo", kindChurches="Iglesias", kindDioceses="Diócesis",
  kindParishes="Parroquias", kindMonasteries="Monasterios",
  communities="Parroquias y monasterios", loading="Cargando...",
  loadFailed="No se pudo cargar esta parte del directorio.", retry="Intentar de nuevo"),
 "ar": dict(kindFilter="النوع", kindChurches="الكنائس", kindDioceses="الأبرشيات",
  kindParishes="الرعايا", kindMonasteries="الأديرة",
  communities="الرعايا والأديرة", loading="جار التحميل...",
  loadFailed="تعذر تحميل هذا الجزء من الدليل.", retry="إعادة المحاولة"),
 "fr": dict(kindFilter="Type", kindChurches="Églises", kindDioceses="Diocèses",
  kindParishes="Paroisses", kindMonasteries="Monastères",
  communities="Paroisses et monastères", loading="Chargement...",
  loadFailed="Cette partie de l'annuaire n'a pas pu être chargée.", retry="Réessayer"),
 "pt": dict(kindFilter="Tipo", kindChurches="Igrejas", kindDioceses="Dioceses",
  kindParishes="Paróquias", kindMonasteries="Mosteiros",
  communities="Paróquias e mosteiros", loading="A carregar...",
  loadFailed="Não foi possível carregar esta parte do diretório.", retry="Tentar novamente"),
 "it": dict(kindFilter="Tipo", kindChurches="Chiese", kindDioceses="Diocesi",
  kindParishes="Parrocchie", kindMonasteries="Monasteri",
  communities="Parrocchie e monasteri", loading="Caricamento...",
  loadFailed="Non è stato possibile caricare questa parte dell'elenco.", retry="Riprova"),
 "sr": dict(kindFilter="Врста", kindChurches="Цркве", kindDioceses="Епархије",
  kindParishes="Парохије", kindMonasteries="Манастири",
  communities="Парохије и манастири", loading="Учитавање...",
  loadFailed="Овај део именика није могао бити учитан.", retry="Покушај поново"),
 "ka": dict(kindFilter="ტიპი", kindChurches="ეკლესიები", kindDioceses="ეპარქიები",
  kindParishes="სამრევლოები", kindMonasteries="მონასტრები",
  communities="სამრევლოები და მონასტრები", loading="იტვირთება...",
  loadFailed="ცნობარის ამ ნაწილის ჩატვირთვა ვერ მოხერხდა.", retry="ხელახლა ცდა"),
 "zh": dict(kindFilter="类型", kindChurches="教会", kindDioceses="教区",
  kindParishes="堂区", kindMonasteries="修道院", communities="堂区和修道院",
  loading="正在加载...", loadFailed="无法加载名录的这一部分。", retry="重试"),
 "ja": dict(kindFilter="種別", kindChurches="諸正教会", kindDioceses="教区",
  kindParishes="教会", kindMonasteries="修道院", communities="教会と修道院",
  loading="読み込み中...", loadFailed="名簿のこの部分を読み込めませんでした。", retry="再試行"),
 "ko": dict(kindFilter="유형", kindChurches="교회", kindDioceses="교구",
  kindParishes="본당", kindMonasteries="수도원", communities="본당과 수도원",
  loading="불러오는 중...", loadFailed="명부의 이 부분을 불러오지 못했습니다.", retry="다시 시도"),
 "sw": dict(kindFilter="Aina", kindChurches="Makanisa", kindDioceses="Dayosisi",
  kindParishes="Parokia", kindMonasteries="Monasteri",
  communities="Parokia na monasteri", loading="Inapakia...",
  loadFailed="Sehemu hii ya orodha haikuweza kupakiwa.", retry="Jaribu tena"),
 "hy": dict(kindFilter="Տեսակ", kindChurches="Եկեղեցիներ", kindDioceses="Թեմեր",
  kindParishes="Ծուխեր", kindMonasteries="Վանքեր", communities="Ծուխեր եւ վանքեր",
  loading="Կը բեռնուի...", loadFailed="Ցուցակի այս մասը չյաջողեցաւ բեռնել։", retry="Կրկին փորձել"),
 "arc": dict(kindFilter="ܓܢܣܐ", kindChurches="ܥܕ̈ܬܐ", kindDioceses="ܡܪ̈ܥܝܬܐ",
  kindParishes="ܥܕ̈ܬܐ", kindMonasteries="ܕܝܪ̈ܬܐ", communities="ܥܕ̈ܬܐ ܘܕܝܪ̈ܬܐ",
  loading="ܡܬܛܥܢ...", loadFailed="ܠܐ ܐܬܡܨܝ ܠܡܛܥܢ ܠܗܢܐ ܡܢܬܐ ܕܡܟܬܒܢܐ.", retry="ܢܣܐ ܬܘܒ"),
 "hi": dict(kindFilter="प्रकार", kindChurches="कलीसियाएँ", kindDioceses="धर्मप्रांत",
  kindParishes="पल्लियाँ", kindMonasteries="मठ", communities="पल्लियाँ और मठ",
  loading="खुल रहा है...", loadFailed="निर्देशिका का यह भाग नहीं खुल सका।", retry="फिर प्रयास करें"),
 "bn": dict(kindFilter="ধরন", kindChurches="গির্জা", kindDioceses="ধর্মপ্রদেশ",
  kindParishes="প্যারিশ", kindMonasteries="মঠ", communities="প্যারিশ ও মঠ",
  loading="লোড হচ্ছে...", loadFailed="নির্দেশিকার এই অংশটি লোড করা যায়নি।", retry="আবার চেষ্টা করুন"),
 "ur": dict(kindFilter="قسم", kindChurches="کلیسیائیں", kindDioceses="اسقفی حلقے",
  kindParishes="پیرشیں", kindMonasteries="خانقاہیں", communities="پیرشیں اور خانقاہیں",
  loading="کھولا جا رہا ہے...", loadFailed="فہرست کا یہ حصہ نہیں کھل سکا۔", retry="دوبارہ کوشش کریں"),
 "bg": dict(kindFilter="Вид", kindChurches="Църкви", kindDioceses="Епархии",
  kindParishes="Енории", kindMonasteries="Манастири",
  communities="Енории и манастири", loading="Зареждане...",
  loadFailed="Тази част от указателя не можа да се зареди.", retry="Опитайте отново"),
}

# The compact directory controls. The size control counts published rows in
# this directory, not members, parishes in a jurisdiction, or any other figure
# the sources do not provide consistently.
FILTER_UI = {
 "en": dict(countryFilter="Country", jurisdictionFilter="Jurisdiction", rankFilter="Rank",
  listedFilter="Directory entries", clearFilters="Clear filters"),
 "el": dict(countryFilter="Χώρα", jurisdictionFilter="Δικαιοδοσία", rankFilter="Βαθμός",
  listedFilter="Εγγραφές καταλόγου", clearFilters="Καθαρισμός φίλτρων"),
 "ru": dict(countryFilter="Страна", jurisdictionFilter="Юрисдикция", rankFilter="Ранг",
  listedFilter="Записи", clearFilters="Очистить отбор"),
 "ro": dict(countryFilter="Țară", jurisdictionFilter="Jurisdicție", rankFilter="Rang",
  listedFilter="Înregistrări în catalog", clearFilters="Șterge filtrele"),
 "uk": dict(countryFilter="Країна", jurisdictionFilter="Юрисдикція", rankFilter="Ранг",
  listedFilter="Записи в довіднику", clearFilters="Очистити"),
 "de": dict(countryFilter="Land", jurisdictionFilter="Jurisdiktion", rankFilter="Rang",
  listedFilter="Einträge im Verzeichnis", clearFilters="Auswahl löschen"),
 "es": dict(countryFilter="País", jurisdictionFilter="Jurisdicción", rankFilter="Rango",
  listedFilter="Entradas del directorio", clearFilters="Borrar filtros"),
 "ar": dict(countryFilter="البلد", jurisdictionFilter="الولاية الكنسية", rankFilter="الرتبة",
  listedFilter="إدخالات الدليل", clearFilters="مسح عوامل التصفية"),
 "fr": dict(countryFilter="Pays", jurisdictionFilter="Juridiction", rankFilter="Rang",
  listedFilter="Entrées de l'annuaire", clearFilters="Effacer les filtres"),
 "pt": dict(countryFilter="País", jurisdictionFilter="Jurisdição", rankFilter="Categoria",
  listedFilter="Entradas do diretório", clearFilters="Limpar filtros"),
 "it": dict(countryFilter="Paese", jurisdictionFilter="Giurisdizione", rankFilter="Rango",
  listedFilter="Voci dell'elenco", clearFilters="Cancella filtri"),
 "sr": dict(countryFilter="Земља", jurisdictionFilter="Јурисдикција", rankFilter="Ранг",
  listedFilter="Уноси у именику", clearFilters="Обриши филтере"),
 "ka": dict(countryFilter="ქვეყანა", jurisdictionFilter="იურისდიქცია", rankFilter="რანგი",
  listedFilter="ჩანაწერები ცნობარში", clearFilters="ფილტრების გასუფთავება"),
 "zh": dict(countryFilter="国家或地区", jurisdictionFilter="教会管辖", rankFilter="等级",
  listedFilter="名录条目数", clearFilters="清除筛选"),
 "ja": dict(countryFilter="国・地域", jurisdictionFilter="管轄教会", rankFilter="位階",
  listedFilter="名簿の掲載数", clearFilters="フィルターを解除"),
 "ko": dict(countryFilter="국가 또는 지역", jurisdictionFilter="관할 교회", rankFilter="지위",
  listedFilter="명부 항목 수", clearFilters="필터 지우기"),
 "sw": dict(countryFilter="Nchi", jurisdictionFilter="Mamlaka ya kanisa", rankFilter="Cheo",
  listedFilter="Maingizo ya orodha", clearFilters="Futa vichujio"),
 "hy": dict(countryFilter="Երկիր", jurisdictionFilter="Իրաւասութիւն", rankFilter="Աստիճան",
  listedFilter="Ցուցակի գրառումներ", clearFilters="Մաքրել զտիչները"),
 "arc": dict(countryFilter="ܐܬܪܐ", jurisdictionFilter="ܫܘܠܛܢܐ ܥܕܬܢܝܐ", rankFilter="ܕܪܓܐ",
  listedFilter="ܣܘܪ̈ܓܕܐ ܕܡܟܬܒܢܐ", clearFilters="ܕܟܐ ܡܨܦܝ̈ܢܐ"),
 "hi": dict(countryFilter="देश", jurisdictionFilter="क्षेत्राधिकार", rankFilter="पद",
  listedFilter="निर्देशिका प्रविष्टियाँ", clearFilters="फ़िल्टर हटाएँ"),
 "bn": dict(countryFilter="দেশ", jurisdictionFilter="অধিক্ষেত্র", rankFilter="পদ",
  listedFilter="নির্দেশিকার এন্ট্রি", clearFilters="ফিল্টার মুছুন"),
 "ur": dict(countryFilter="ملک", jurisdictionFilter="دائرہ اختیار", rankFilter="رتبہ",
  listedFilter="فہرست کے اندراجات", clearFilters="فلٹر صاف کریں"),
 "bg": dict(countryFilter="Държава", jurisdictionFilter="Юрисдикция", rankFilter="Ранг",
  listedFilter="Записи в указателя", clearFilters="Изчисти филтрите"),
}

BRANCH_RANKS = {
 "en": ("Parish", "Chapel Parish", "Monastery"),
 "el": ("Ενορία", "Ενορία παρεκκλησίου", "Μονή"),
 "ru": ("Приход", "Часовенный приход", "Монастырь"),
 "ro": ("Parohie", "Parohie de capelă", "Mănăstire"),
 "uk": ("Парафія", "Каплична парафія", "Монастир"),
 "de": ("Kirchengemeinde", "Kapellengemeinde", "Kloster"),
 "es": ("Parroquia", "Parroquia de capilla", "Monasterio"),
 "ar": ("رعية", "رعية كنيسة صغيرة", "دير"),
 "fr": ("Paroisse", "Paroisse de chapelle", "Monastère"),
 "pt": ("Paróquia", "Paróquia de capela", "Mosteiro"),
 "it": ("Parrocchia", "Parrocchia di cappella", "Monastero"),
 "sr": ("Парохија", "Капелска парохија", "Манастир"),
 "ka": ("სამრევლო", "სამლოცველოს სამრევლო", "მონასტერი"),
 "zh": ("堂区", "小堂堂区", "修道院"),
 "ja": ("教会", "礼拝所教会", "修道院"),
 "ko": ("본당", "경당 본당", "수도원"),
 "sw": ("Parokia", "Parokia ya kapela", "Monasteri"),
 "hy": ("Ծուխ", "Մատուռի ծուխ", "Վանք"),
 "arc": ("ܥܕܬܐ", "ܥܕܬܐ ܕܒܝܬ ܨܠܘܬܐ", "ܕܝܪܐ"),
 "hi": ("पल्ली", "प्रार्थनालय की पल्ली", "मठ"),
 "bn": ("প্যারিশ", "উপাসনালয় প্যারিশ", "মঠ"),
 "ur": ("پیرش", "عبادت گاہ کا پیرش", "خانقاہ"),
 "bg": ("Енория", "Параклисна енория", "Манастир"),
}

SERVICES = {
 "en": "Services", "el": "Ακολουθίες", "ru": "Богослужения",
 "ro": "Slujbe", "uk": "Богослужіння", "de": "Gottesdienste",
 "es": "Oficios", "ar": "الخِدَم", "fr": "Offices",
 "pt": "Ofícios", "it": "Funzioni", "sr": "Богослужења",
 "ka": "ღვთისმსახურებები", "zh": "礼仪", "ja": "奉神礼",
 "ko": "예배", "sw": "Ibada", "hy": "Ժամերգութիւններ",
 "arc": "ܬܫܡܫܬܐ", "hi": "आराधनाएँ", "bn": "উপাসনা",
 "ur": "عبادات", "bg": "Богослужения",
}


def page_words(lang):
    """All words the page speaks for one language."""
    out = dict(W[lang])
    out.update(BRANCH_UI[lang])
    out.update(FILTER_UI[lang])
    out["services"] = SERVICES[lang]
    ranks = dict(out["ranks"])
    parish, chapel, monastery = BRANCH_RANKS[lang]
    ranks.update({"Parish": parish, "Chapel Parish": chapel,
                  "Monastery": monastery})
    out["ranks"] = ranks
    return out


# Countries, for the three languages the browser cannot name them in.
#
# Every other language gets them from Intl.DisplayNames, which gives the
# received form and needs no table. Georgian, Armenian and Syriac have no
# region data there at all, and an English chip standing among Georgian ones
# is simply broken, so these twenty are written down.
#
# Three of them were wrong, and the lanes writing the rows found it by doing
# what this file tells everyone else to do: counting. Armenian Romania was
# written Rumania where the corpus says Rumink 32 times to 3; Syriac Poland
# and Ukraine were written in forms that stand nowhere at all, beside forms
# standing 30 and 173 times. The audit passed all three, because a wrong
# choice between real forms shares a stem with the right one and only
# counting the rivals can separate them. The audit catches an invention; it
# cannot catch a preference.
#
# Most of them were not written. They were read off the names this site
# already publishes, where a saint of Egypt or a patriarch of All Russia
# carries the country inside his title in every language: fifteen of the
# twenty stand whole in the Georgian, fourteen in the Armenian, sixteen in
# the Syriac. The remainder are Estonia, Finland, Japan, Slovakia, Poland,
# Ukraine, Turkey and the United States in one language or another, and they
# follow the pattern that reading established - Georgian's -ეთი, Armenian in
# the classical orthography this site's Armenian is written in, and the
# Syriac habit of ending a transcribed land in -ܝܐ. Every one of them, whole
# or built, answers to a stem the language already has here.
COUNTRIES = {
 "ka": {  # gathered: BG EG GE RS RU SY UA
  "AD": "ანდორა", "AL": "ალბანეთი", "AU": "ავსტრალია", "BG": "ბულგარეთი", "CY": "კვიპროსი", "DK": "დანია", "EE": "ესტონეთი",
  "EG": "ეგვიპტე", "FI": "ფინეთი", "FO": "ფარერის კუნძულები", "GE": "საქართველო", "GI": "გიბრალტარი", "GL": "გრენლანდია", "GR": "საბერძნეთი",
  "IL": "ისრაელი", "IS": "ისლანდია", "JP": "იაპონია", "LI": "ლიხტენშტაინი", "LU": "ლუქსემბურგი", "MC": "მონაკო", "MK": "ჩრდილოეთ მაკედონია", "NO": "ნორვეგია",
  "NZ": "ახალი ზელანდია", "PL": "პოლონეთი", "PT": "პორტუგალია", "RO": "რუმინეთი", "RS": "სერბეთი", "RU": "რუსეთი",
  "SI": "სლოვენია", "SK": "სლოვაკეთი", "SM": "სან-მარინო", "SY": "სირია", "TR": "თურქეთი", "UA": "უკრაინა",
  "US": "ამერიკის შეერთებული შტატები"},
 "hy": {  # gathered: BG EG GE RS RU UA US
  "AD": "Անդորրա", "AL": "Ալբանիա", "AU": "Աւստրալիա", "BG": "Բուլղարիա", "CY": "Կիպրոս", "DK": "Դանիա", "EE": "Էստոնիա",
  "EG": "Եգիպտոս", "FI": "Ֆինլանդիա", "FO": "Ֆարերյան կղզիներ", "GE": "Վրաստան", "GI": "Ճիպրալթար", "GL": "Գրենլանդիա", "GR": "Յունաստան",
  "IL": "Իսրայէլ", "IS": "Իսլանդիա", "JP": "Ճապոնիա", "LI": "Լիխտենշտայն", "LU": "Լիւքսամպուրկ", "MC": "Մոնակո", "MK": "Հիւսիսային Մակեդոնիա", "NO": "Նորվեգիա",
  "NZ": "Նոր Զելանդիա", "PL": "Լեհաստան", "PT": "Պորտուգալիա", "RO": "Ռումինիա", "RS": "Սերբիա", "RU": "Ռուսիա",
  "SI": "Սլովենիա", "SK": "Սլովակիա", "SM": "Սան Մարինո", "SY": "Սուրիա", "TR": "Թուրքիա", "UA": "Ուկրաինա",
  "US": "Ամերիկայի Միացեալ Նահանգներ"},
 "arc": {  # gathered forms preserved; the rest follow CLDR Syriac
  "AD": "ܐܢܕܘܪܐ", "AL": "ܐܠܒܢܝܐ", "AM": "ܐܪܡܢܝܐ", "AR": "ܐܪܓܢܬܝܢܐ", "AT": "ܐܘܣܛܪܝܐ", "AU": "ܐܘܣܛܪܠܝܐ",
  "AZ": "ܐܙܪܒܝܓܐܢ", "BA": "ܒܘܣܢܐ ܘܗܪܬܣܓܘܒܝܢܐ", "BE": "ܒܠܓܝܩܐ", "BG": "ܒܘܠܓܪܝܐ", "BI": "ܒܘܪܘܢܕܝ",
  "BJ": "ܒܢܝܢ", "BR": "ܒܪܐܙܝܠ", "BW": "ܒܘܛܣܘܐܢܐ", "BY": "ܒܠܐܪܘܣ", "CA": "ܟܢܕܐ",
  "CD": "ܟܘܢܓܘ - ܟܝܢܫܐܣܐ", "CG": "ܟܘܢܓܘ - ܒܪܐܙܐܒܝܠ", "CH": "ܣܘܝܣܪܐ", "CL": "ܬܫܝܠܝ", "CM": "ܟܐܡܪܘܢ",
  "CN": "ܨܝܢ", "CY": "ܩܘܦܪܘܣ", "CZ": "ܬܫܝܟܝܐ", "DE": "ܐܠܡܢܝܐ", "DK": "ܕܐܢܡܐܪܩ", "EE": "ܐܣܛܘܢܝܐ",
  "EG": "ܡܨܪܝܢ", "ES": "ܐܣܦܢܝܐ", "ET": "ܟܘܫ", "FI": "ܦܝܢܠܢܕܝܐ", "FO": "ܓܙܪ̈ܬܐ ܕܦܪܘ", "FR": "ܦܪܢܣܐ",
  "GB": "ܡܠܟܘܬܐ ܡܚܝܕܬܐ", "GE": "ܓܘܪܓܝܐ", "GH": "ܓܐܢܐ", "GI": "ܓܝܒܪܠܛܪ", "GL": "ܓܪܝܢܠܢܕ", "GN": "ܓܝܢܝܐ", "GR": "ܝܘܢܝܐ",
  "HK": "ܗܘܢܓ ܟܘܢܓ", "HR": "ܩܪܘܐܛܝܐ", "HU": "ܡܓܪ", "IE": "ܐܝܪܠܢܕ", "IL": "ܐܝܣܪܐܝܠ", "IS": "ܐܝܣܠܢܕ",
  "IQ": "ܥܝܪܩ", "IT": "ܐܝܛܠܝܐ", "JO": "ܝܘܪܕܢܢ", "JP": "ܝܦܢ", "KE": "ܟܝܢܝܐ",
  "KG": "ܩܝܪܓܝܙܣܬܐܢ", "KR": "ܟܘܪܝܐ ܬܝܡܢܝܬܐ", "KZ": "ܟܙܩܣܬܐܢ", "LB": "ܠܒܢܢ", "LI": "ܠܝܟܛܢܫܛܝܢ",
  "LT": "ܠܬܘܢܝܐ", "LU": "ܠܘܟܣܡܒܘܪܓ", "LV": "ܠܐܛܒܝܐ", "LY": "ܠܘܒܐ", "MC": "ܡܘܢܐܩܘ", "MD": "ܡܘܠܕܘܒܐ",
  "ME": "ܡܘܢܛܝܢܝܓܪܘ", "MG": "ܡܕܓܣܩܪ", "MK": "ܡܩܕܘܢܝܐ", "MT": "ܡܝܠܛܐ", "MW": "ܡܠܐܘܝ",
  "MX": "ܡܟܣܝܟܘ", "NG": "ܢܝܓܝܪܝܐ", "NL": "ܗܘܠܢܕܐ", "NO": "ܢܘܪܒܝܓ", "NZ": "ܢܝܘ ܙܝܠܢܕ", "PH": "ܦܝܠܝܦܝܢܝܐ",
  "PL": "ܦܘܠܢܝܐ", "PS": "ܐܬܪ̈ܘܬܐ ܕܦܠܣܛܝܢ", "PT": "ܦܘܪܛܘܓܠ", "QA": "ܩܛܪ", "RO": "ܪܘܡܢܝܐ", "RS": "ܣܪܒܝܐ",
  "RU": "ܪܘܣܝܐ", "RW": "ܪܘܐܢܕܐ", "SD": "ܣܘܕܐܢ", "SE": "ܣܘܝܕ", "SG": "ܣܝܢܓܐܦܘܪ",
  "SI": "ܣܠܘܒܢܝܐ", "SK": "ܣܠܘܒܩܝܐ", "SM": "ܣܢ ܡܪܝܢܘ", "SS": "ܬܝܡܢ ܣܘܕܐܢ", "SY": "ܣܘܪܝܐ", "TH": "ܬܐܝܠܢܕ", "TJ": "ܬܐܓܝܟܣܬܐܢ",
  "TM": "ܬܘܪܟܡܢܣܬܐܢ", "TN": "ܬܘܢܣ", "TR": "ܬܘܪܩܝܐ", "TZ": "ܛܢܙܢܝܐ", "UA": "ܐܘܩܪܐܝܢܐ",
  "UG": "ܐܘܓܢܕܐ", "US": "ܐܡܪܝܩܐ", "UZ": "ܐܘܙܒܟܣܬܐܢ", "ZA": "ܬܝܡܢ ܐܦܪܝܩܐ", "ZM": "ܙܐܡܒܝܐ",
  "ZW": "ܙܝܡܒܐܒܘܝ"},
}


def gathered():
    """All, the empty line, and the word Language, taken from the site."""
    g = json.loads((ROOT / "data" / "glossary.v6.json").read_text("utf-8"))["ui"]
    out = {}
    for L in LANGS:
        row = {}
        if L in g:
            row.update({"all": g[L]["all"], "none": g[L]["none"]})
        p = ROOT / "data" / ("ui-i18n.v6.%s.json" % L)
        if p.exists():
            row["language"] = json.loads(p.read_text("utf-8"))["language"]
        out[L] = row
    return out


def build():
    got = gathered()
    out = {}
    for L in LANGS:
        w = page_words(L)
        w["h1"] = CHURCHES[L]
        w["churches"] = CHURCHES[L]
        w.update(got[L])
        if L in COUNTRIES:
            w["countries"] = COUNTRIES[L]
        # What the rows themselves are called. A row a language has not been
        # asked about is simply absent, and the page falls back to English
        # for that row alone, so a half-written language still reads.
        names, seats, styled = directory_names.load(L)
        if names:
            w["names"] = names
        if seats:
            w["seats"] = seats
        if styled:
            w["styled"] = styled
        out[L] = w
    return {"v": 1, "langs": LANGS, "w": out,
            "named": directory_names.written()}


def corpus(L):
    blob = []
    for f in glob.glob(str(ROOT / ("data/*.%s.json" % L))) + \
             glob.glob(str(ROOT / ("tools/saint_*/%s.py" % L))):
        try:
            blob.append(Path(f).read_text("utf-8"))
        except Exception:
            pass
    return "\n".join(blob).casefold()


def words_in(text):
    """Every word in a string, for any script this site is written in.

    Python's \\w is letters and digits and holds no combining marks, so a
    regex built on it cuts Hindi pataa into three pieces and Syriac loses
    the seyame that makes a plural a plural. Both then fail to match
    themselves. A word here is a run of letters and the marks that belong
    to them, which is what every one of these twenty-two scripts means by
    one."""
    out, cur = [], []
    for ch in text:
        if unicodedata.category(ch)[0] in "LM":
            cur.append(ch)
        elif cur:
            if len(cur) > 1:
                out.append("".join(cur))
            cur = []
    if len(cur) > 1:
        out.append("".join(cur))
    return out


def vocabulary(L):
    """Every word the language uses here, and every word reversed.

    The stem test used to look for the stem anywhere in the text, which let
    a new word pass on somebody else's middle: Greek Skopia passed inside
    episkop-, Russian Tallin inside metallichesky, Tokio inside potoki,
    Tirana inside tiranstva. Four words that had never been written here were
    reported as already in use, and the lane that wrote them said so rather
    than taking the pass.

    A stem now has to start a word the language actually uses, or - for
    Swahili, which builds on the front - end one. The reversed list is what
    makes the second question answerable with the same search."""
    words = sorted(set(words_in(corpus(L))))
    back = sorted(set(w[::-1] for w in words))
    return words, back


def begins(sorted_words, stem):
    """Does any word in the list start with this stem?"""
    i = bisect.bisect_left(sorted_words, stem)
    return i < len(sorted_words) and sorted_words[i].startswith(stem)


def attested(fore, back, word, unspaced=False, text=""):
    """Is this word, or a stem of it, one the language already uses here?

    An ending may be added or removed - no language here is written without
    them and a table of every ending is a worse thing to maintain than this -
    but the stem has to begin a real word, or end one where the language
    builds on the front.

    Han, kana and Hangul are asked a character at a time, because a run of
    them is not a word and a stem of one is not a prefix. Asking them the
    word-boundary question returned no for every Chinese word ever written,
    which is the answer a wrong question gets."""
    w = word.casefold()
    if unspaced:
        return all(ch in text for ch in w if ch.isalpha())
    # A short word must still be able to match itself: with a floor of four
    # the loop below was empty for anything shorter, and a three-letter word
    # was unattested by arithmetic rather than by evidence.
    lo = min(len(w), max(4, len(w) - 4))
    for n in range(len(w), lo - 1, -1):
        if begins(fore, w[:n]):
            return True
        if begins(back, w[len(w) - n:][::-1]):
            return True
    return False


# Han, kana and Hangul write without spaces, so a run of them is not a word
# and a stem is not a prefix. Those three are checked a character at a time,
# which is the unit their corpus can actually answer for.
UNSPACED = {"zh", "ja", "ko"}


def audit():
    """Every word the page says, against everything that language publishes.

    An inflection of an attested word passes: the corpus is asked for the
    stem, not the form, because no language here is written without endings
    and a table of every ending is a worse thing to maintain than this. The
    stem is sought at either end, since Swahili builds on the front of a
    verb where Greek and Russian build on the back.
    The site's own name is not a word in any of them and is skipped."""
    bad = 0
    for L in LANGS:
        if L == "en":
            continue
        c = corpus(L)
        fore, back = vocabulary(L)
        miss = []
        # What the rows are called is a map from the English word to this
        # language's, so the language's side of it is what gets asked.
        said = []
        for k, v in page_words(L).items():
            if k == "ranks":
                said.extend(("%s rank" % r, w) for r, w in v.items())
            else:
                said.append((k, v))
        for k, v in said:
            v = v.replace("Plithos", " ")
            if L in UNSPACED:
                for ch in v:
                    if ch.isalpha() and ch not in c:
                        miss.append("%s:%s" % (k, ch))
                continue
            for word in words_in(v):
                if len(word) < 4 or attested(fore, back, word, L in UNSPACED, c):
                    continue
                miss.append("%s:%s" % (k, word))
        names, seats, styled = directory_names.load(L)
        en_n, en_s, en_st = directory_names.load("en")
        en_all = {}
        en_all.update(en_n)
        en_all.update(en_s)
        en_all.update(en_st)
        for key, v in (list(names.items()) + list(seats.items()) +
                       list(styled.items())):
            # A word a language leaves exactly as English has it is not a
            # composition - Presov is Presov in German, and Spanish writes
            # "Syosset, Nueva York", translating the state and leaving the
            # village alone. Only what actually changed is checked.
            kept = set(w.casefold() for w in words_in(en_all.get(key) or ""))
            if L in UNSPACED:
                # Naming the character is the whole use of the report here:
                # saying the phrase said only that something in it was new.
                for ch in v:
                    if ch.isalpha() and ch not in c and ch.casefold() not in kept:
                        miss.append("%s:%s" % (key, ch))
                continue
            for word in words_in(v):
                if len(word) < 4 or word.casefold() in kept:
                    continue
                if attested(fore, back, word):
                    continue
                miss.append("%s:%s" % (key, word))
        for cc, v in (COUNTRIES.get(L) or {}).items():
            for word in words_in(v):
                if len(word) < 4 or attested(fore, back, word, L in UNSPACED, c):
                    continue
                miss.append("%s:%s" % (cc, word))
        if miss:
            bad += len(miss)
            print("  %-4s %s" % (L, " ".join(miss)))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    if a.audit:
        n = audit()
        print("%d words not found in the language's own corpus" % n)
        en, es, _ = directory_names.load("en")
        done = directory_names.written()
        for L in LANGS:
            if L in ("en",):
                continue
            nm, st, sy = directory_names.load(L)
            if L not in done:
                print("  %-4s rows not written" % L)
            elif len(nm) < len(en) or len(st) < len(es) or not sy:
                print("  %-4s %d/%d names, %d/%d seats, %d official names"
                      % (L, len(nm), len(en), len(st), len(es), len(sy)))
        print("rows named in %d of %d languages" % (len(done), len(LANGS)))
        return 0
    d = build()
    text = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    if a.write:
        OUT.write_text(text, encoding="utf-8")
        print("wrote %s  (%d languages, %d KB)"
              % (OUT.relative_to(ROOT), len(d["langs"]),
                 len(text.encode("utf-8")) // 1024 or 1))
        return 0
    have = OUT.read_text("utf-8") if OUT.exists() else ""
    if have != text:
        print("data/directory-i18n.v1.json is out of date", file=sys.stderr)
        return 1
    print("%d languages" % len(d["langs"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
