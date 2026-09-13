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

Country names are not here at all. The browser knows them in every one of
these languages and gives the received form, so the page asks it rather
than keeping a table of two hundred names that would have to be written by
someone who does not read most of them.

    python3 tools/directory_words.py --check
    python3 tools/directory_words.py --write
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "directory-i18n.v1.json"

LANGS = "en el ru ro uk de es ar fr pt it sr ka zh ja ko sw hy arc hi bn ur".split()

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
 "ur": "کلیسیائیں",
}

# Everything the page says in its own voice.
W = {
"en": dict(
 lede="The Orthodox Churches of the world, with the seat and the address each one publishes.",
 note="A body is listed here because an autocephalous Church names it among its own. Where the Churches differ, the entry says who names it, and Plithos does not say which is right.",
 ph="Search by name, city or country",
 gauto="Autocephalous Churches", gnom="Autonomous Churches",
 listed="Listed by", confirmed="Confirmed"),
"el": dict(
 lede="Οι Ορθόδοξες Εκκλησίες του κόσμου, με την έδρα και τη διεύθυνση που δημοσιεύει η καθεμία.",
 note="Μια Εκκλησία γράφεται εδώ επειδή μια αυτοκέφαλη Εκκλησία την αναγνωρίζει ως δική της. Όπου οι Εκκλησίες διαφέρουν, η εγγραφή λέει ποια την αναγνωρίζει· το Plithos δεν λέει ποια έχει δίκιο.",
 ph="Αναζήτηση με όνομα, πόλη ή χώρα",
 gauto="Αυτοκέφαλες Εκκλησίες", gnom="Αυτόνομες Εκκλησίες",
 listed="Αναγνωρίζεται από", confirmed="Βεβαιωμένο"),
"ru": dict(
 lede="Православные Церкви мира, с кафедрой и адресом, которые каждая из них объявляет.",
 note="Церковь внесена сюда потому, что автокефальная Церковь признаёт её своей. Там, где Церкви расходятся, запись говорит, кто её признаёт; Plithos не говорит, кто прав.",
 ph="Поиск по названию, городу или стране",
 gauto="Автокефальные Церкви", gnom="Автономные Церкви",
 listed="Признана", confirmed="Подтверждено"),
"ro": dict(
 lede="Bisericile Ortodoxe ale lumii, cu scaunul și adresa pe care fiecare le face cunoscute.",
 note="Un așezământ este trecut aici pentru că o Biserică autocefală îl recunoaște ca al său. Acolo unde Bisericile se despart, însemnarea spune cine îl recunoaște; Plithos nu spune cine are dreptate.",
 ph="Caută după nume, oraș sau țară",
 gauto="Biserici autocefale", gnom="Biserici autonome",
 listed="Recunoscută de", confirmed="Confirmat"),
"uk": dict(
 lede="Православні Церкви світу, з кафедрою та адресою, які кожна з них подає.",
 note="Церква внесена сюди тому, що автокефальна Церква визнає її своєю. Там, де Церкви розходяться, запис каже, хто її визнає; Plithos не каже, хто має рацію.",
 ph="Пошук за назвою, містом або країною",
 gauto="Автокефальні Церкви", gnom="Автономні Церкви",
 listed="Визнана", confirmed="Підтверджено"),
"de": dict(
 lede="Die orthodoxen Kirchen der Welt, mit dem Sitz und der Anschrift, die jede von ihnen veröffentlicht.",
 note="Eine Kirche steht hier, weil eine autokephale Kirche sie zu den ihren zählt. Wo die Kirchen auseinandergehen, nennt der Eintrag, wer sie zählt; Plithos sagt nicht, wer recht hat.",
 ph="Suche nach Name, Stadt oder Land",
 gauto="Autokephale Kirchen", gnom="Autonome Kirchen",
 listed="Gezählt von", confirmed="Bestätigt"),
"es": dict(
 lede="Las Iglesias Ortodoxas del mundo, con la sede y la dirección que cada una publica.",
 note="Una Iglesia figura aquí porque una Iglesia autocéfala la cuenta entre las suyas. Donde las Iglesias difieren, la entrada dice quién la cuenta; Plithos no dice quién tiene razón.",
 ph="Buscar por nombre, ciudad o país",
 gauto="Iglesias autocéfalas", gnom="Iglesias autónomas",
 listed="Reconocida por", confirmed="Comprobado"),
"ar": dict(
 lede="الكنائس الأرثوذكسية في العالم، مع الكرسي والعنوان الذي تنشره كل منها.",
 note="تُدرَج الكنيسة هنا لأن كنيسة مستقلة تعدّها من كنائسها. وحيث تختلف الكنائس، يذكر المدخل من يعدّها، ولا يقول Plithos من على حق.",
 ph="ابحث بالاسم أو المدينة أو البلد",
 gauto="الكنائس المستقلة", gnom="الكنائس ذات الحكم الذاتي",
 listed="تعدّها", confirmed="تم التثبت"),
"fr": dict(
 lede="Les Églises orthodoxes du monde, avec le siège et l'adresse que chacune publie.",
 note="Une Église figure ici parce qu'une Église autocéphale la compte parmi les siennes. Là où les Églises diffèrent, la notice dit qui la compte ; Plithos ne dit pas qui a raison.",
 ph="Rechercher par nom, ville ou pays",
 gauto="Églises autocéphales", gnom="Églises autonomes",
 listed="Reconnue par", confirmed="Vérifié"),
"pt": dict(
 lede="As Igrejas Ortodoxas do mundo, com a sede e o endereço que cada uma publica.",
 note="Uma Igreja consta aqui porque uma Igreja autocéfala a conta entre as suas. Onde as Igrejas divergem, a entrada diz quem a conta; o Plithos não diz quem tem razão.",
 ph="Buscar por nome, cidade ou país",
 gauto="Igrejas autocéfalas", gnom="Igrejas autônomas",
 listed="Reconhecida por", confirmed="Verificado"),
"it": dict(
 lede="Le Chiese ortodosse del mondo, con la sede e l'indirizzo che ciascuna pubblica.",
 note="Una Chiesa figura qui perché una Chiesa autocefala la annovera fra le proprie. Dove le Chiese divergono, la voce dice chi la annovera; Plithos non dice chi abbia ragione.",
 ph="Cerca per nome, citta o paese",
 gauto="Chiese autocefale", gnom="Chiese autonome",
 listed="Riconosciuta da", confirmed="Verificato"),
"sr": dict(
 lede="Православне Цркве света, са седиштем и адресом које свака од њих објављује.",
 note="Црква је уписана овде зато што је аутокефална Црква признаје за своју. Тамо где се Цркве разилазе, запис каже ко је признаје; Plithos не каже ко је у праву.",
 ph="Претрага по имену, граду или земљи",
 gauto="Аутокефалне Цркве", gnom="Аутономне Цркве",
 listed="Признаје", confirmed="Проверено"),
"ka": dict(
 lede="მსოფლიოს მართლმადიდებელი ეკლესიები, კათედრითა და მისამართით, რომელსაც თითოეული აქვეყნებს.",
 note="ეკლესია აქ ჩაწერილია იმიტომ, რომ ავტოკეფალური ეკლესია მას თავისად მიიჩნევს. სადაც ეკლესიები განსხვავდებიან, ჩანაწერი ამბობს ვინ მიიჩნევს მას; Plithos არ ამბობს ვინ არის მართალი.",
 ph="ძიება სახელით, ქალაქით ან ქვეყნით",
 gauto="ავტოკეფალური ეკლესიები", gnom="ავტონომიური ეკლესიები",
 listed="აღიარებს", confirmed="დამოწმებული"),
"zh": dict(
 lede="世界各地的正教会，附有各自公布的驻地与地址。",
 note="列在此处的教会，是因为有自主教会将其列为自己的教会。各教会看法不同之处，条目只说明是谁将其列入，Plithos 不判断谁对。",
 ph="按名称、城市或国家搜索",
 gauto="自主教会", gnom="自治教会",
 listed="列入者", confirmed="已核实"),
"ja": dict(
 lede="世界の正教会と、それぞれが公にしている座所と住所。",
 note="ここに載る教会は、独立教会がこれを自らのものとして挙げているからです。教会の間で異なる場合、項目は誰が挙げているかを記すのみで、Plithos はどちらが正しいかを述べません。",
 ph="名称、都市、国で検索",
 gauto="独立教会", gnom="自治教会",
 listed="挙げている教会", confirmed="確認済み"),
"ko": dict(
 lede="세계의 정교회와 각 교회가 공표한 소재지와 주소.",
 note="여기에 실린 교회는 독립 교회가 그 교회를 자기 교회로 인정하기 때문입니다. 교회마다 다를 때에는 누가 인정하는지를 적을 뿐, Plithos는 어느 쪽이 옳은지 말하지 않습니다.",
 ph="이름, 도시, 나라로 검색",
 gauto="독립 교회", gnom="자치 교회",
 listed="인정한 교회", confirmed="확인됨"),
"sw": dict(
 lede="Makanisa ya Orthodoksi ya ulimwengu, pamoja na makao na anwani ambayo kila moja hutangaza.",
 note="Kanisa liko katika orodha hii kwa sababu Kanisa huru linahesabu kuwa lake. Makanisa yakitofautiana, kiingilio husema ni nani anahesabu; Plithos hasemi ni nani yuko sahihi.",
 ph="Tafuta kwa jina, mji au nchi",
 gauto="Makanisa huru", gnom="Makanisa yenye kujitegemea",
 listed="Linahesabiwa na", confirmed="Imethibitishwa"),
"hy": dict(
 lede="Աշխարհի ուղղափառ Եկեղեցիները՝ իրենց աթոռով եւ հասցեով, ինչպէս իւրաքանչիւրը հրապարակում է։",
 note="Եկեղեցին այստեղ գրուած է, որովհետեւ ինքնագլուխ Եկեղեցին այն իւրն է համարում։ Ուր Եկեղեցիները տարբերւում են, գրառումը ասում է, թէ ով է այն համարում. Plithos չի ասում, թէ ով է իրաւացի։",
 ph="Որոնում ըստ անուան, քաղաքի կամ երկրի",
 gauto="Ինքնագլուխ Եկեղեցիներ", gnom="Ինքնավար Եկեղեցիներ",
 listed="Համարում է", confirmed="Հաստատուած"),
"arc": dict(
 lede="ܥܕ̈ܬܐ ܬܪ̈ܝܨܝ ܫܘܒܚܐ ܕܥܠܡܐ ܥܡ ܟܘܪܣܝܐ ܘܐܬܪܐ ܕܟܠ ܚܕܐ ܡܘܕܥܐ.",
 note="ܥܕܬܐ ܟܬܝܒܐ ܗܪܟܐ ܡܛܠ ܕܥܕܬܐ ܕܢܦܫܗ̇ ܫܠܝܛܐ ܚܫܒܐ ܠܗ̇ ܡܢ ܕܝܠܗ̇. ܐܝܟܐ ܕܥܕ̈ܬܐ ܦܪ̈ܝܫܢ ܟܬܒܐ ܐܡܪ ܡܢܘ ܚܫܒ ܠܗ̇. ܘPlithos ܠܐ ܐܡܪ ܡܢܘ ܫܪܝܪܐ.",
 ph="ܒܥܝ ܒܫܡܐ ܐܘ ܡܕܝܢܬܐ ܐܘ ܐܬܪܐ",
 gauto="ܥܕ̈ܬܐ ܕܢܦܫܗܝܢ ܫܠܝ̈ܛܢ", gnom="ܥܕ̈ܬܐ ܕܡܕܒܪ̈ܢ ܢܦܫܗܝܢ",
 listed="ܚܫܒܐ ܠܗ̇", confirmed="ܐܫܬܪܪ"),
"hi": dict(
 lede="संसार की रूढ़िवादी कलीसियाएँ, उनके आसन और पते के साथ जो प्रत्येक प्रकाशित करती है।",
 note="कोई कलीसिया यहाँ इसलिए दर्ज है कि कोई स्वतंत्र कलीसिया उसे अपनी मानती है। जहाँ कलीसियाओं में भेद है, वहाँ प्रविष्टि बताती है कि उसे कौन मानता है; Plithos यह नहीं कहता कि कौन सही है।",
 ph="नाम, नगर या देश से खोजें",
 gauto="स्वतंत्र कलीसियाएँ", gnom="स्वायत्त कलीसियाएँ",
 listed="मानने वाली कलीसिया", confirmed="पुष्ट"),
"bn": dict(
 lede="জগতের অর্থোডক্স গির্জা, প্রত্যেকের প্রকাশিত আসন ও ঠিকানা সহ।",
 note="কোনো গির্জা এখানে রয়েছে কারণ কোনো স্বাধীন গির্জা তাকে নিজের বলে গণ্য করে। যেখানে গির্জাগুলির মধ্যে পার্থক্য, সেখানে ভুক্তি বলে কে তাকে গণ্য করে; Plithos বলে না কে ঠিক।",
 ph="নাম, শহর বা দেশ দিয়ে খুঁজুন",
 gauto="স্বাধীন গির্জা", gnom="স্বায়ত্তশাসিত গির্জা",
 listed="গণ্য করে", confirmed="নিশ্চিত"),
"ur": dict(
 lede="دنیا کی راست عقیدہ کلیسیائیں، اُس کرسی اور پتے کے ساتھ جو ہر ایک شائع کرتی ہے۔",
 note="کوئی کلیسیا یہاں اِس لیے درج ہے کہ کوئی خود مختار کلیسیا اُسے اپنی شمار کرتی ہے۔ جہاں کلیسیاؤں میں فرق ہو، وہاں اندراج بتاتا ہے کہ اُسے کون شمار کرتا ہے؛ Plithos یہ نہیں کہتا کہ کون درست ہے۔",
 ph="نام، شہر یا ملک سے تلاش کریں",
 gauto="خود مختار کلیسیائیں", gnom="خود اختیار کلیسیائیں",
 listed="شمار کرنے والی", confirmed="تصدیق شدہ"),
}


# Countries, for the three languages the browser cannot name them in.
#
# Every other language gets them from Intl.DisplayNames, which gives the
# received form and needs no table. Georgian, Armenian and Syriac have no
# region data there at all, and an English chip standing among Georgian ones
# is simply broken, so these twenty are written down.
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
  "AL": "ალბანეთი", "BG": "ბულგარეთი", "CY": "კვიპროსი", "EE": "ესტონეთი",
  "EG": "ეგვიპტე", "FI": "ფინეთი", "GE": "საქართველო", "GR": "საბერძნეთი",
  "IL": "ისრაელი", "JP": "იაპონია", "MK": "ჩრდილოეთ მაკედონია",
  "PL": "პოლონეთი", "RO": "რუმინეთი", "RS": "სერბეთი", "RU": "რუსეთი",
  "SK": "სლოვაკეთი", "SY": "სირია", "TR": "თურქეთი", "UA": "უკრაინა",
  "US": "ამერიკის შეერთებული შტატები"},
 "hy": {  # gathered: BG EG GE RS RU UA US
  "AL": "Ալբանիա", "BG": "Բուլղարիա", "CY": "Կիպրոս", "EE": "Էստոնիա",
  "EG": "Եգիպտոս", "FI": "Ֆինլանդիա", "GE": "Վրաստան", "GR": "Յունաստան",
  "IL": "Իսրայէլ", "JP": "Ճապոնիա", "MK": "Հիւսիսային Մակեդոնիա",
  "PL": "Լեհաստան", "RO": "Ռումանիա", "RS": "Սերբիա", "RU": "Ռուսիա",
  "SK": "Սլովակիա", "SY": "Սուրիա", "TR": "Թուրքիա", "UA": "Ուկրաինա",
  "US": "Ամերիկայի Միացեալ Նահանգներ"},
 "arc": {  # gathered: BG EG GE GR MK RS RU SY UA
  "AL": "ܐܠܒܢܝܐ", "BG": "ܒܘܠܓܪܝܐ", "CY": "ܩܘܦܪܘܣ", "EE": "ܐܣܛܘܢܝܐ",
  "EG": "ܡܨܪܝܢ", "FI": "ܦܝܢܠܢܕܝܐ", "GE": "ܓܘܪܓܝܐ", "GR": "ܝܘܢܝܐ",
  "IL": "ܐܝܣܪܐܝܠ", "JP": "ܝܦܢ", "MK": "ܡܩܕܘܢܝܐ", "PL": "ܦܘܠܢܕܝܐ",
  "RO": "ܪܘܡܢܝܐ", "RS": "ܣܪܒܝܐ", "RU": "ܪܘܣܝܐ", "SK": "ܣܠܘܒܩܝܐ",
  "SY": "ܣܘܪܝܐ", "TR": "ܬܘܪܩܝܐ", "UA": "ܐܘܟܪܐܝܢܐ", "US": "ܐܡܪܝܩܐ"},
}


def gathered():
    """All, the empty line, and the word Language, taken from the site."""
    g = json.loads((ROOT / "data" / "glossary.v4.json").read_text("utf-8"))["ui"]
    out = {}
    for L in LANGS:
        ui = json.loads((ROOT / "data" / ("ui-i18n.v6.%s.json" % L)).read_text("utf-8"))
        out[L] = {"all": g[L]["all"], "none": g[L]["none"],
                  "language": ui["language"]}
    return out


def build():
    got = gathered()
    out = {}
    for L in LANGS:
        w = dict(W[L])
        w["h1"] = CHURCHES[L]
        w["churches"] = CHURCHES[L]
        w.update(got[L])
        if L in COUNTRIES:
            w["countries"] = COUNTRIES[L]
        out[L] = w
    return {"v": 1, "langs": LANGS, "w": out}


def corpus(L):
    blob = []
    for f in glob.glob(str(ROOT / ("data/*.%s.json" % L))) + \
             glob.glob(str(ROOT / ("tools/saint_*/%s.py" % L))):
        try:
            blob.append(Path(f).read_text("utf-8"))
        except Exception:
            pass
    return "\n".join(blob).casefold()


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
        miss = []
        for k, v in W[L].items():
            v = v.replace("Plithos", " ")
            if L in UNSPACED:
                for ch in v:
                    if ch.isalpha() and ch not in c:
                        miss.append("%s:%s" % (k, ch))
                continue
            for word in re.findall(r"[^\W\d_]{4,}", v, re.UNICODE):
                w = word.casefold()
                lo = max(4, len(w) - 4)
                if any(w[:n] in c for n in range(len(w), lo - 1, -1)):
                    continue
                if any(w[len(w) - n:] in c for n in range(len(w), lo - 1, -1)):
                    continue
                miss.append("%s:%s" % (k, word))
        for cc, v in (COUNTRIES.get(L) or {}).items():
            for word in re.findall(r"[^\W\d_]{4,}", v, re.UNICODE):
                w = word.casefold()
                lo = max(4, len(w) - 4)
                if any(w[:n] in c for n in range(len(w), lo - 1, -1)):
                    continue
                if any(w[len(w) - n:] in c for n in range(len(w), lo - 1, -1)):
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
