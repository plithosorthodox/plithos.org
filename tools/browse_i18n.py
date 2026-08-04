#!/usr/bin/env python3
"""
The words the Library uses to sort itself, in the languages it is read in.

Browsing the shelf by author, century, purpose, and translator brought a
handful of new labels with it, and a labelled provenance block brought a
handful more. The reader's own vocabulary table already carries every other
label in twenty-one languages; leaving these in English would have put an
English column down the middle of a Greek or Georgian page.

The values themselves - the authors' names, the purposes, the editions -
stay as the catalogue records them.

    python3 tools/browse_i18n.py --check
    python3 tools/browse_i18n.py --write
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READER = ROOT / "plithos_reader.html"

KEYS = ["secBrowse", "fAuthor", "fCentury", "fPurpose", "fTranslator",
        "fClear", "fMore", "fFind", "fNone", "fTitle", "fTitles", "readLife",
        "mWritten", "mTrans", "mEdition", "mPub", "mDigit", "mRights", "mPD",
        "howReceived"]

T = {
 "en": ["The whole shelf", "Author", "Century", "Purpose", "Translator",
        "clear", "show all", "Find a title or a name",
        "Nothing on the shelf matches all of those.", "title", "titles",
        "The life", "Written", "Translated by", "Edition", "Published",
        "Digitized by", "Rights", "Public domain",
        "How the Church received this"],
 "el": ["Όλο το ράφι", "Συγγραφέας", "Αιώνας", "Σκοπός",
        "Μεταφραστής", "καθαρισμός", "όλα", "Αναζήτηση τίτλου ή ονόματος",
        "Τίποτε στο ράφι δεν ταιριάζει με όλα αυτά.", "τίτλος", "τίτλοι",
        "Ο βίος", "Γράφτηκε", "Μετάφραση", "Έκδοση", "Δημοσιεύθηκε",
        "Ψηφιοποίηση", "Δικαιώματα", "Κοινό κτήμα",
        "Πώς το δέχθηκε η Εκκλησία"],
 "ru": ["Вся полка", "Автор", "Век", "Назначение", "Переводчик",
        "сбросить", "показать все", "Поиск по названию или имени",
        "На полке нет ничего, что подходило бы под все это.", "название",
        "названий", "Житие", "Написано", "Перевод", "Издание",
        "Опубликовано", "Оцифровано", "Права", "Общественное достояние",
        "Как это принято Церковью"],
 "cu": ["Всѧ̑ книги", "Списатель", "Вѣ́къ", "Намѣре́ніе", "Прево́дникъ",
        "ѡчи́стити", "всѧ̑", "Иска́ніе и́мене и҆лѝ назва́ніѧ",
        "Ничто́же ѡбрѣ́тесѧ по си̑мъ.", "кни́га", "кни̑гъ", "Житіѐ",
        "Напи́сано", "Прево́дъ", "Изда́ніе", "И҆здано̀", "Ѡцифро́вано",
        "Права̀", "Ѻ҆́бщее достоѧ́ніе",
        "Ка́кѡ прїѧ́тъ сїѐ Це́рковь"],
 "ka": ["მთელი თარო", "ავტორი", "საუკუნე", "დანიშნულება", "მთარგმნელი",
        "გასუფთავება", "ყველა", "მოძებნეთ სათაური ან სახელი",
        "თაროზე ამ ყველაფერს არაფერი შეესაბამება.", "სათაური", "სათაური",
        "ცხოვრება", "დაიწერა", "თარგმანი", "გამოცემა", "გამოქვეყნდა",
        "ციფრული ასლი", "უფლებები", "საზოგადოებრივი საკუთრება",
        "როგორ მიიღო ეს ეკლესიამ"],
 "ro": ["Tot raftul", "Autor", "Secol", "Scop", "Traducător",
        "șterge", "arată tot", "Caută un titlu sau un nume",
        "Nimic din raft nu se potrivește cu toate acestea.", "titlu",
        "titluri", "Viața", "Scris", "Tradus de", "Ediție", "Publicat",
        "Digitizat de", "Drepturi", "Domeniu public",
        "Cum a primit Biserica aceasta"],
 "sr": ["Цела полица", "Аутор", "Век", "Сврха", "Преводилац",
        "поништи", "прикажи све", "Тражи наслов или име",
        "Ништа на полици не одговара свему томе.", "наслов", "наслова",
        "Житије", "Написано", "Превео", "Издање", "Објављено",
        "Дигитализовао", "Права", "Јавно власништво",
        "Како је Црква ово примила"],
 "uk": ["Уся полиця", "Автор", "Століття", "Призначення", "Перекладач",
        "скинути", "показати все", "Пошук за назвою або іменем",
        "На полиці немає нічого, що відповідало б усьому цьому.", "назва",
        "назв", "Житіє", "Написано", "Переклад", "Видання", "Опубліковано",
        "Оцифровано", "Права", "Суспільне надбання",
        "Як це прийняла Церква"],
 "ar": ["الرف كله", "المؤلف", "القرن", "الغرض", "المترجم",
        "مسح", "عرض الكل", "ابحث عن عنوان أو اسم",
        "لا شيء على الرف يطابق ذلك كله.", "عنوان", "عناوين", "السيرة",
        "كُتب", "ترجمة", "الطبعة", "نُشر", "رقمنة", "الحقوق", "ملك عام",
        "كيف تلقّت الكنيسة هذا"],
 "es": ["Todo el estante", "Autor", "Siglo", "Propósito", "Traductor",
        "limpiar", "ver todo", "Buscar un título o un nombre",
        "Nada en el estante coincide con todo eso.", "título", "títulos",
        "La vida", "Escrito", "Traducido por", "Edición", "Publicado",
        "Digitalizado por", "Derechos", "Dominio público",
        "Cómo lo recibió la Iglesia"],
 "pt": ["Toda a estante", "Autor", "Século", "Finalidade", "Tradutor",
        "limpar", "ver tudo", "Procurar um título ou um nome",
        "Nada na estante corresponde a tudo isso.", "título", "títulos",
        "A vida", "Escrito", "Traduzido por", "Edição", "Publicado",
        "Digitalizado por", "Direitos", "Domínio público",
        "Como a Igreja recebeu isto"],
 "it": ["Tutto lo scaffale", "Autore", "Secolo", "Scopo", "Traduttore",
        "azzera", "mostra tutto", "Cerca un titolo o un nome",
        "Nulla sullo scaffale corrisponde a tutto questo.", "opera", "opere",
        "La vita", "Scritto", "Tradotto da", "Edizione", "Pubblicato",
        "Digitalizzato da", "Diritti", "Pubblico dominio",
        "Come la Chiesa lo ha ricevuto"],
 "fr": ["Tout le rayon", "Auteur", "Siècle", "Objet", "Traducteur",
        "effacer", "tout afficher", "Chercher un titre ou un nom",
        "Rien sur le rayon ne correspond à tout cela.", "titre", "titres",
        "La vie", "Écrit", "Traduit par", "Édition", "Publié",
        "Numérisé par", "Droits", "Domaine public",
        "Comment l'Eglise l'a reçu"],
 "de": ["Das ganze Regal", "Verfasser", "Jahrhundert", "Zweck", "Übersetzer",
        "zurücksetzen", "alle anzeigen", "Titel oder Namen suchen",
        "Nichts im Regal entspricht all dem.", "Titel", "Titel",
        "Das Leben", "Verfasst", "Übersetzt von", "Ausgabe", "Erschienen",
        "Digitalisiert von", "Rechte", "Gemeinfrei",
        "Wie die Kirche dies aufnahm"],
 "zh": ["全部藏书", "作者", "世纪", "用途", "译者",
        "清除", "显示全部", "查找书名或人名",
        "没有符合以上全部条件的书。", "部", "部", "生平",
        "成书", "翻译", "版本", "出版", "数字化", "权利", "公有领域",
        "教会如何接纳此书"],
 "ja": ["蔵書のすべて", "著者", "世紀", "目的", "訳者",
        "解除", "すべて表示", "書名または人名で探す",
        "すべてに当てはまるものはありません。", "点", "点", "伝記",
        "成立", "翻訳", "版", "刊行", "電子化", "権利", "パブリックドメイン",
        "教会がこれをどう受け入れたか"],
 "ko": ["전체 장서", "저자", "세기", "용도", "역자",
        "해제", "모두 보기", "제목이나 이름으로 찾기",
        "그 모두에 해당하는 것이 없습니다.", "편", "편", "생애",
        "저술", "번역", "판본", "간행", "전산화", "권리", "퍼블릭 도메인",
        "교회가 이 책을 어떻게 받아들였는가"],
 "sw": ["Rafu nzima", "Mwandishi", "Karne", "Kusudi", "Mfasiri",
        "futa", "onyesha zote", "Tafuta kichwa au jina",
        "Hakuna kilicho rafuni kinacholingana na yote hayo.", "kichwa",
        "vichwa", "Maisha", "Iliandikwa", "Ilifasiriwa na", "Toleo",
        "Ilichapishwa", "Iliwekwa kidijitali na", "Haki", "Mali ya umma",
        "Jinsi Kanisa lilivyokipokea"],
 "hi": ["पूरा संग्रह", "लेखक", "शताब्दी", "प्रयोजन", "अनुवादक",
        "हटाएँ", "सभी दिखाएँ", "शीर्षक या नाम खोजें",
        "इन सबसे मेल खाता कुछ नहीं है।", "कृति", "कृतियाँ", "जीवनी",
        "रचना", "अनुवाद", "संस्करण", "प्रकाशन", "डिजिटलीकरण",
        "अधिकार", "सार्वजनिक अधिकार-क्षेत्र",
        "कलीसिया ने इसे कैसे स्वीकारा"],
 "hy": ["Ողջ գրադարակը", "Հեղինակ", "Դար", "Նպատակ", "Թարգմանիչ",
        "մաքրել", "ցույց տալ բոլորը", "Փնտրել վերնագիր կամ անուն",
        "Ոչինչ չի համապատասխանում այդ ամենին։", "երկ", "երկ", "Վարքը",
        "Գրվել է", "Թարգմանությունը", "Հրատարակություն", "Հրատարակվել է",
        "Թվայնացրել է", "Իրավունքներ", "Հանրային սեփականություն",
        "Ինչպես է Եկեղեցին ընդունել սա"],
 # Classical Syriac. Kept to words the language already carries: a shelf is
 # named as its books, and a saint's life as his life.
 "arc": ["ܟܠܗܘܢ ܟܬܒܐ", "ܟܬܘܒܐ", "ܕܪܐ", "ܢܝܫܐ", "ܡܦܫܩܢܐ",
         "ܒܛܠ", "ܟܠܗܘܢ", "ܒܥܝ ܫܡܐ ܐܘ ܟܘܢܝܐ",
         "ܠܝܬ ܡܕܡ ܕܡܫܬܘܐ ܠܗܠܝܢ ܟܠܗܝܢ.", "ܟܬܒܐ", "ܟܬܒܐ", "ܚܝ̈ܐ",
         "ܐܬܟܬܒ", "ܦܘܫܩܐ", "ܡܦܩܬܐ", "ܐܬܦܪܣ", "ܐܬܪܫܡ",
         "ܙܕܩܐ", "ܩܢܝܢܐ ܓܘܢܝܐ",
        "ܐܝܟܢܐ ܩܒܠܬܗ ܥܕܬܐ"],
}

LINE = re.compile(r'^(\s*)"?([a-z]{2,3})"?:\{(.*)\},?\s*$')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    for lang, vals in T.items():
        if len(vals) != len(KEYS):
            print("%s: %d strings for %d keys" % (lang, len(vals), len(KEYS)))
            return 1

    src = READER.read_text(encoding="utf-8").split("\n")
    start = next(i for i, l in enumerate(src) if l.startswith("const RLEX="))
    end = next(i for i in range(start, len(src)) if src[i].strip() == "};")

    seen, out = [], 0
    for i in range(start + 1, end):
        m = LINE.match(src[i])
        if not m:
            continue
        indent, lang, body = m.groups()
        seen.append(lang)
        if lang not in T:
            print("no strings written for %s" % lang)
            continue
        body = re.sub(r',?"?(?:%s)"?:"(?:[^"\\]|\\.)*"' % "|".join(KEYS), "", body)
        add = ",".join("%s:%s" % (k, json.dumps(v, ensure_ascii=False))
                       for k, v in zip(KEYS, T[lang]))
        src[i] = '%s%s:{%s,%s},' % (indent, lang, body, add)
        out += 1

    missing = [l for l in T if l not in seen]
    if missing:
        print("strings written for languages the reader does not list: %s"
              % ", ".join(missing))
    print("%d of %d languages given the new labels" % (out, len(seen)))

    if args.write:
        READER.write_text("\n".join(src), encoding="utf-8")
        print("wrote plithos_reader.html")
    elif not args.check:
        print("nothing written; pass --write")
    return 1 if missing or out != len(seen) else 0


if __name__ == "__main__":
    sys.exit(main())
