#!/usr/bin/env python3
"""
The words the Library's results page says, in every language it offers.

The results bar was written in English inside the markup: "12 passages",
"for", "Clear", "No passages match". So was the invitation to open the
Scriptures, which is new. All of it goes into the lexicon instead, where the
rest of the page's words already are.

Run once from the repository root:

    python3 tools/search_words.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"

# resPassage and resPassages are the one word before and after one: the count
# stands in front of it, as it does for "works" and "units" already on this
# page. Two forms is not enough for the Slavic languages, which want a third
# for two to four, but it is right for one, which is the count a reader sees
# most often and the one that reads wrong without it.
WORDS = {
"en": {
  "resPassage": "passage", "resPassages": "passages", "resFor": "for", "resClear": "Clear",
  "resNone": "Nothing matches", "resHint": "Try fewer words, or wrap a phrase in quotation marks.",
  "scripHead": "Holy Scripture",
  "scripAlso": "Search Holy Scripture as well",
  "scripOpening": "Opening the Scriptures",
  "scripNone": "nothing here",
  "scripFailed": "Holy Scripture could not be opened.",
},
"ru": {
  "resPassage": "место", "resPassages": "мест", "resFor": "по запросу", "resClear": "Очистить",
  "resNone": "Ничего не найдено", "resHint": "Попробуйте меньше слов или заключите выражение в кавычки.",
  "scripHead": "Священное Писание",
  "scripAlso": "Искать и в Священном Писании",
  "scripOpening": "Открываем Писание",
  "scripNone": "здесь ничего нет",
  "scripFailed": "Не удалось открыть Священное Писание.",
},
"uk": {
  "resPassage": "місце", "resPassages": "місць", "resFor": "за запитом", "resClear": "Очистити",
  "resNone": "Нічого не знайдено", "resHint": "Спробуйте менше слів або візьміть вираз у лапки.",
  "scripHead": "Святе Письмо",
  "scripAlso": "Шукати і у Святому Письмі",
  "scripOpening": "Відкриваємо Писання",
  "scripNone": "тут нічого немає",
  "scripFailed": "Не вдалося відкрити Святе Письмо.",
},
"sr": {
  "resPassage": "место", "resPassages": "места", "resFor": "за упит", "resClear": "Обриши",
  "resNone": "Ништа није нађено", "resHint": "Покушајте са мање речи или ставите израз под наводнике.",
  "scripHead": "Свето Писмо",
  "scripAlso": "Тражи и у Светом Писму",
  "scripOpening": "Отварамо Писмо",
  "scripNone": "овде нема ничега",
  "scripFailed": "Свето Писмо није могло бити отворено.",
},
"el": {
  "resPassage": "χωρίο", "resPassages": "χωρία", "resFor": "για", "resClear": "Καθαρισμός",
  "resNone": "Δεν βρέθηκε τίποτε", "resHint": "Δοκιμάστε λιγότερες λέξεις ή βάλτε μια φράση σε εισαγωγικά.",
  "scripHead": "Αγία Γραφή",
  "scripAlso": "Αναζήτηση και στην Αγία Γραφή",
  "scripOpening": "Ανοίγουμε τις Γραφές",
  "scripNone": "τίποτε εδώ",
  "scripFailed": "Η Αγία Γραφή δεν άνοιξε.",
},
"ro": {
  "resPassage": "loc", "resPassages": "locuri", "resFor": "pentru", "resClear": "Șterge",
  "resNone": "Nu s-a găsit nimic", "resHint": "Încercați mai puține cuvinte sau puneți o expresie între ghilimele.",
  "scripHead": "Sfânta Scriptură",
  "scripAlso": "Caută și în Sfânta Scriptură",
  "scripOpening": "Se deschid Scripturile",
  "scripNone": "nimic aici",
  "scripFailed": "Sfânta Scriptură nu a putut fi deschisă.",
},
"cu": {
  "resPassage": "мѣ́сто", "resPassages": "мѣстъ", "resFor": "о", "resClear": "Очи́стити",
  "resNone": "Ничто́же обрѣ́теся", "resHint": "Искуси́ мнѣ́е слове́съ, или́ рече́нїе въ кавы́чки заключи́.",
  "scripHead": "Свяще́нное Писа́нїе",
  "scripAlso": "Иска́ти и въ Свяще́нномъ Писа́нїи",
  "scripOpening": "Tверза́ются Писа́нїя",
  "scripNone": "здѣ́ ничто́же",
  "scripFailed": "Свяще́нное Писа́нїе не tве́рзеся.",
},
"ka": {
  "resPassage": "ადგილი", "resPassages": "ადგილი", "resFor": "ძიება", "resClear": "გასუფთავება",
  "resNone": "ვერაფერი მოიძებნა", "resHint": "სცადეთ ნაკლები სიტყვა, ან ფრაზა ბრჭყალებში ჩასვით.",
  "scripHead": "წმიდა წერილი",
  "scripAlso": "ძიება წმიდა წერილშიც",
  "scripOpening": "იხსნება წერილი",
  "scripNone": "აქ არაფერია",
  "scripFailed": "წმიდა წერილი ვერ გაიხსნა.",
},
"es": {
  "resPassage": "pasaje", "resPassages": "pasajes", "resFor": "para", "resClear": "Limpiar",
  "resNone": "No se encontró nada", "resHint": "Pruebe con menos palabras, o encierre una frase entre comillas.",
  "scripHead": "Sagrada Escritura",
  "scripAlso": "Buscar también en la Sagrada Escritura",
  "scripOpening": "Abriendo las Escrituras",
  "scripNone": "nada aquí",
  "scripFailed": "No se pudo abrir la Sagrada Escritura.",
},
"pt": {
  "resPassage": "passagem", "resPassages": "passagens", "resFor": "para", "resClear": "Limpar",
  "resNone": "Nada foi encontrado", "resHint": "Tente menos palavras, ou coloque uma frase entre aspas.",
  "scripHead": "Sagrada Escritura",
  "scripAlso": "Buscar também na Sagrada Escritura",
  "scripOpening": "Abrindo as Escrituras",
  "scripNone": "nada aqui",
  "scripFailed": "Não foi possível abrir a Sagrada Escritura.",
},
"it": {
  "resPassage": "passo", "resPassages": "passi", "resFor": "per", "resClear": "Cancella",
  "resNone": "Non è stato trovato nulla", "resHint": "Provi con meno parole, o racchiuda una frase tra virgolette.",
  "scripHead": "Sacra Scrittura",
  "scripAlso": "Cerca anche nella Sacra Scrittura",
  "scripOpening": "Si aprono le Scritture",
  "scripNone": "nulla qui",
  "scripFailed": "Non è stato possibile aprire la Sacra Scrittura.",
},
"fr": {
  "resPassage": "passage", "resPassages": "passages", "resFor": "pour", "resClear": "Effacer",
  "resNone": "Rien n'a été trouvé", "resHint": "Essayez moins de mots, ou mettez une expression entre guillemets.",
  "scripHead": "Sainte Écriture",
  "scripAlso": "Chercher aussi dans la Sainte Écriture",
  "scripOpening": "Ouverture des Écritures",
  "scripNone": "rien ici",
  "scripFailed": "La Sainte Écriture n'a pas pu être ouverte.",
},
"de": {
  "resPassage": "Stelle", "resPassages": "Stellen", "resFor": "für", "resClear": "Löschen",
  "resNone": "Nichts gefunden", "resHint": "Versuchen Sie weniger Worte, oder setzen Sie eine Wendung in Anführungszeichen.",
  "scripHead": "Heilige Schrift",
  "scripAlso": "Auch in der Heiligen Schrift suchen",
  "scripOpening": "Die Schriften werden geöffnet",
  "scripNone": "hier nichts",
  "scripFailed": "Die Heilige Schrift konnte nicht geöffnet werden.",
},
"ar": {
  "resPassage": "موضع", "resPassages": "مواضع", "resFor": "عن", "resClear": "مسح",
  "resNone": "لم يوجد شيء", "resHint": "جرب كلمات أقل، أو ضع العبارة بين علامتي اقتباس.",
  "scripHead": "الكتاب المقدس",
  "scripAlso": "ابحث في الكتاب المقدس أيضا",
  "scripOpening": "تفتح الكتب",
  "scripNone": "لا شيء هنا",
  "scripFailed": "تعذر فتح الكتاب المقدس.",
},
"zh": {
  "resPassage": "处", "resPassages": "处", "resFor": "关于", "resClear": "清除",
  "resNone": "没有找到", "resHint": "请减少词语，或用引号括住短语。",
  "scripHead": "圣经",
  "scripAlso": "同时搜索圣经",
  "scripOpening": "正在打开圣经",
  "scripNone": "此处没有",
  "scripFailed": "圣经无法打开。",
},
"ja": {
  "resPassage": "箇所", "resPassages": "箇所", "resFor": "検索語", "resClear": "消去",
  "resNone": "見つかりません", "resHint": "語を減らすか、句を引用符で囲んでください。",
  "scripHead": "聖書",
  "scripAlso": "聖書も検索する",
  "scripOpening": "聖書を開いています",
  "scripNone": "ここには何もありません",
  "scripFailed": "聖書を開けませんでした。",
},
"ko": {
  "resPassage": "곳", "resPassages": "곳", "resFor": "검색어", "resClear": "지우기",
  "resNone": "찾을 수 없습니다", "resHint": "단어를 줄이거나 구절을 따옴표로 묶어 보십시오.",
  "scripHead": "성경",
  "scripAlso": "성경에서도 찾기",
  "scripOpening": "성경을 여는 중",
  "scripNone": "여기에는 없습니다",
  "scripFailed": "성경을 열 수 없었습니다.",
},
"sw": {
  "resPassage": "kifungu", "resPassages": "vifungu", "resFor": "kwa", "resClear": "Futa",
  "resNone": "Hakuna kilichopatikana", "resHint": "Jaribu maneno machache, au weka msemo katika alama za nukuu.",
  "scripHead": "Maandiko Matakatifu",
  "scripAlso": "Tafuta pia katika Maandiko Matakatifu",
  "scripOpening": "Maandiko yanafunguliwa",
  "scripNone": "hakuna kitu hapa",
  "scripFailed": "Maandiko Matakatifu hayakuweza kufunguliwa.",
},
"hi": {
  "resPassage": "स्थान", "resPassages": "स्थान", "resFor": "के लिए", "resClear": "साफ़ करें",
  "resNone": "कुछ नहीं मिला", "resHint": "कम शब्द आज़माएँ, या वाक्यांश को उद्धरण चिह्नों में रखें.",
  "scripHead": "पवित्र शास्त्र",
  "scripAlso": "पवित्र शास्त्र में भी खोजें",
  "scripOpening": "शास्त्र खोले जा रहे हैं",
  "scripNone": "यहाँ कुछ नहीं",
  "scripFailed": "पवित्र शास्त्र नहीं खुल सका.",
},
"hy": {
  "resPassage": "տեղ", "resPassages": "տեղ", "resFor": "ըստ", "resClear": "Մաքրել",
  "resNone": "Ոչինչ չգտնվեց", "resHint": "Փորձեք ավելի քիչ բառ, կամ արտահայտությունը դրեք չակերտների մեջ.",
  "scripHead": "Սուրբ Գիրք",
  "scripAlso": "Փնտրել նաև Սուրբ Գրքում",
  "scripOpening": "Բացվում են Գրքերը",
  "scripNone": "այստեղ ոչինչ",
  "scripFailed": "Սուրբ Գիրքը չբացվեց.",
},
"arc": {
  "resPassage": "ܕܘܟܬܐ", "resPassages": "ܕܘܟܝܬܐ", "resFor": "ܥܠ", "resClear": "ܡܪܘܩ",
  "resNone": "ܠܐ ܐܫܬܟܚ ܡܕܡ", "resHint": "ܢܣܝ ܡܠܐ ܒܨܝܪܬܐ, ܐܘ ܣܝܡ ܡܡܠܠܐ ܒܝܬ ܢܝܫܐ ܕܡܡܠܠܐ.",
  "scripHead": "ܟܬܒܐ ܩܕܝܫܐ",
  "scripAlso": "ܒܥܝ ܐܦ ܒܟܬܒܐ ܩܕܝܫܐ",
  "scripOpening": "ܡܬܦܬܚܝܢ ܟܬܒܐ",
  "scripNone": "ܠܝܬ ܡܕܡ ܗܪܟܐ",
  "scripFailed": "ܟܬܒܐ ܩܕܝܫܐ ܠܐ ܐܬܦܬܚ.",
},
}

CURVED = ("–", "—", "‘", "’", "“", "”")
# French and the Syriac note above use the apostrophe as a letter, not as a
# quotation mark; the house rule is about the curved forms, which are absent.


def main():
    s = PAGE.read_text(encoding="utf-8")
    i = s.index("const RLEX={")
    j = s.index("\n};", i)
    head, block, tail = s[:i], s[i:j + 2], s[j + 2:]

    added = 0
    for code, words in WORDS.items():
        for k, v in words.items():
            for ch in CURVED:
                if ch in v:
                    print("house rule: %r in %s/%s" % (ch, code, k), file=sys.stderr)
                    return 1
        m = re.search(r'\n ("?)%s\1:\{' % re.escape(code), block)
        if not m:
            print("no such language in the lexicon: %s" % code, file=sys.stderr)
            return 1
        at = m.end()
        line_end = block.index("\n", at)
        ins = "".join('"%s":%s,' % (k, json.dumps(v, ensure_ascii=False))
                      for k, v in words.items()
                      if ('"%s"' % k) not in block[at:line_end])
        if not ins:
            continue
        block = block[:at] + ins + block[at:]
        added += 1

    PAGE.write_text(head + block + tail, encoding="utf-8")
    print("wrote the results words to %d languages" % added)
    return 0


if __name__ == "__main__":
    sys.exit(main())
