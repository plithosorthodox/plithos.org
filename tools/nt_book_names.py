#!/usr/bin/env python3
"""
The names of the books of the New Testament, in the languages it is read in
here.

NT_BOOK_NAMES in library.html carried Greek and Ukrainian and nothing else,
so a reader in Russian, Romanian or Arabic opened his own New Testament and
found "Matthew" over the chapter. The Old Testament never had this problem:
scripture/index.json carries its names per language.

Each set follows the edition this site actually prints, named beside it, so
the headings agree with the text under them:

    ar   Van Dyke (SVD)            it   Riveduta 1927
    de   Schlachter                ko   Korean, public domain
    es   Reina-Valera              pt   Almeida
    fr   Ostervald / Martin        ro   Cornilescu
    hi   Hindi O.V. (BSI)          ru   Synodal
    hy   Western Armenian          sr   Danicic-Karadzic
    sw   Swahili                   zh   Chinese Union Version

Japanese and Syriac are absent on purpose. The Japanese here is the Raguet
translation of 1910, whose headings are in classical Japanese and are not the
modern ones a search would return; the Syriac is the Peshitta. Neither should
be guessed at, and both fall back to the English name until someone who reads
those editions supplies them.

    python3 tools/nt_book_names.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"

ORDER = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans',
         '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
         'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
         '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James',
         '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude',
         'Revelation']

NAMES = {
"ru": ["От Матфея", "От Марка", "От Луки", "От Иоанна", "Деяния апостолов",
       "К Римлянам", "1-е Коринфянам", "2-е Коринфянам", "К Галатам",
       "К Ефесянам", "К Филиппийцам", "К Колоссянам", "1-е Фессалоникийцам",
       "2-е Фессалоникийцам", "1-е Тимофею", "2-е Тимофею", "К Титу",
       "К Филимону", "К Евреям", "Иакова", "1-е Петра", "2-е Петра",
       "1-е Иоанна", "2-е Иоанна", "3-е Иоанна", "Иуды", "Откровение"],
"sr": ["По Матеју", "По Марку", "По Луки", "По Јовану", "Дела апостолска",
       "Римљанима", "1. Коринћанима", "2. Коринћанима", "Галатима",
       "Ефесцима", "Филипљанима", "Колошанима", "1. Солуњанима",
       "2. Солуњанима", "1. Тимотеју", "2. Тимотеју", "Титу", "Филимону",
       "Јеврејима", "Јаковљева", "1. Петрова", "2. Петрова", "1. Јованова",
       "2. Јованова", "3. Јованова", "Јудина", "Откривење"],
"ro": ["După Matei", "După Marcu", "După Luca", "După Ioan",
       "Faptele Apostolilor", "Către Romani", "1 Corinteni", "2 Corinteni",
       "Către Galateni", "Către Efeseni", "Către Filipeni", "Către Coloseni",
       "1 Tesaloniceni", "2 Tesaloniceni", "1 Timotei", "2 Timotei",
       "Către Tit", "Către Filimon", "Către Evrei", "Iacov", "1 Petru",
       "2 Petru", "1 Ioan", "2 Ioan", "3 Ioan", "Iuda", "Apocalipsa"],
"de": ["Matthäus", "Markus", "Lukas", "Johannes", "Apostelgeschichte",
       "Römer", "1. Korinther", "2. Korinther", "Galater", "Epheser",
       "Philipper", "Kolosser", "1. Thessalonicher", "2. Thessalonicher",
       "1. Timotheus", "2. Timotheus", "Titus", "Philemon", "Hebräer",
       "Jakobus", "1. Petrus", "2. Petrus", "1. Johannes", "2. Johannes",
       "3. Johannes", "Judas", "Offenbarung"],
"es": ["San Mateo", "San Marcos", "San Lucas", "San Juan",
       "Hechos de los Apóstoles", "Romanos", "1 Corintios", "2 Corintios",
       "Gálatas", "Efesios", "Filipenses", "Colosenses", "1 Tesalonicenses",
       "2 Tesalonicenses", "1 Timoteo", "2 Timoteo", "Tito", "Filemón",
       "Hebreos", "Santiago", "1 Pedro", "2 Pedro", "1 Juan", "2 Juan",
       "3 Juan", "Judas", "Apocalipsis"],
"pt": ["São Mateus", "São Marcos", "São Lucas", "São João",
       "Atos dos Apóstolos", "Romanos", "1 Coríntios", "2 Coríntios",
       "Gálatas", "Efésios", "Filipenses", "Colossenses",
       "1 Tessalonicenses", "2 Tessalonicenses", "1 Timóteo", "2 Timóteo",
       "Tito", "Filemom", "Hebreus", "Tiago", "1 Pedro", "2 Pedro",
       "1 João", "2 João", "3 João", "Judas", "Apocalipse"],
"it": ["Matteo", "Marco", "Luca", "Giovanni", "Atti degli Apostoli",
       "Romani", "1 Corinzi", "2 Corinzi", "Galati", "Efesini", "Filippesi",
       "Colossesi", "1 Tessalonicesi", "2 Tessalonicesi", "1 Timoteo",
       "2 Timoteo", "Tito", "Filemone", "Ebrei", "Giacomo", "1 Pietro",
       "2 Pietro", "1 Giovanni", "2 Giovanni", "3 Giovanni", "Giuda",
       "Apocalisse"],
"fr": ["Matthieu", "Marc", "Luc", "Jean", "Actes des Apôtres", "Romains",
       "1 Corinthiens", "2 Corinthiens", "Galates", "Éphésiens",
       "Philippiens", "Colossiens", "1 Thessaloniciens", "2 Thessaloniciens",
       "1 Timothée", "2 Timothée", "Tite", "Philémon", "Hébreux", "Jacques",
       "1 Pierre", "2 Pierre", "1 Jean", "2 Jean", "3 Jean", "Jude",
       "Apocalypse"],
"ar": ["إنجيل متى", "إنجيل مرقس", "إنجيل لوقا", "إنجيل يوحنا", "أعمال الرسل",
       "رومية", "كورنثوس الأولى", "كورنثوس الثانية", "غلاطية", "أفسس",
       "فيلبي", "كولوسي", "تسالونيكي الأولى", "تسالونيكي الثانية",
       "تيموثاوس الأولى", "تيموثاوس الثانية", "تيطس", "فليمون", "العبرانيين",
       "يعقوب", "بطرس الأولى", "بطرس الثانية", "يوحنا الأولى",
       "يوحنا الثانية", "يوحنا الثالثة", "يهوذا", "الرؤيا"],
"zh": ["馬太福音", "馬可福音", "路加福音", "約翰福音", "使徒行傳", "羅馬書",
       "哥林多前書", "哥林多後書", "加拉太書", "以弗所書", "腓立比書",
       "歌羅西書", "帖撒羅尼迦前書", "帖撒羅尼迦後書", "提摩太前書",
       "提摩太後書", "提多書", "腓利門書", "希伯來書", "雅各書", "彼得前書",
       "彼得後書", "約翰壹書", "約翰貳書", "約翰參書", "猶大書", "啟示錄"],
"ko": ["마태복음", "마가복음", "누가복음", "요한복음", "사도행전", "로마서",
       "고린도전서", "고린도후서", "갈라디아서", "에베소서", "빌립보서",
       "골로새서", "데살로니가전서", "데살로니가후서", "디모데전서",
       "디모데후서", "디도서", "빌레몬서", "히브리서", "야고보서",
       "베드로전서", "베드로후서", "요한1서", "요한2서", "요한3서",
       "유다서", "요한계시록"],
"sw": ["Mathayo", "Marko", "Luka", "Yohana", "Matendo ya Mitume", "Warumi",
       "1 Wakorintho", "2 Wakorintho", "Wagalatia", "Waefeso", "Wafilipi",
       "Wakolosai", "1 Wathesalonike", "2 Wathesalonike", "1 Timotheo",
       "2 Timotheo", "Tito", "Filemoni", "Waebrania", "Yakobo", "1 Petro",
       "2 Petro", "1 Yohana", "2 Yohana", "3 Yohana", "Yuda", "Ufunuo"],
"hi": ["मत्ती", "मरकुस", "लूका", "यूहन्ना", "प्रेरितों के काम", "रोमियों",
       "1 कुरिन्थियों", "2 कुरिन्थियों", "गलातियों", "इफिसियों",
       "फिलिप्पियों", "कुलुस्सियों", "1 थिस्सलुनीकियों",
       "2 थिस्सलुनीकियों", "1 तीमुथियुस", "2 तीमुथियुस", "तीतुस",
       "फिलेमोन", "इब्रानियों", "याकूब", "1 पतरस", "2 पतरस", "1 यूहन्ना",
       "2 यूहन्ना", "3 यूहन्ना", "यहूदा", "प्रकाशितवाक्य"],
"hy": ["Ըստ Մատթէոսի", "Ըստ Մարկոսի", "Ըստ Ղուկասու", "Ըստ Յովհաննու",
       "Գործք Առաքելոց", "Հռոմայեցիս", "Ա Կորնթացիս", "Բ Կորնթացիս",
       "Գաղատացիս", "Եփեսացիս", "Փիլիպպեցիս", "Կողոսացիս",
       "Ա Թեսաղոնիկեցիս", "Բ Թեսաղոնիկեցիս", "Ա Տիմոթէոս", "Բ Տիմոթէոս",
       "Տիտոս", "Փիլիմոն", "Եբրայեցիս", "Յակոբոս", "Ա Պետրոս", "Բ Պետրոս",
       "Ա Յովհաննէս", "Բ Յովհաննէս", "Գ Յովհաննէս", "Յուդա", "Յայտնութիւն"],
}


def main():
    s = PAGE.read_text(encoding="utf-8")
    i = s.index("const NT_BOOK_NAMES")
    eq = s.index("=", i)
    j = s.index("\n", i)
    existing = json.loads(s[eq + 1:j].rstrip().rstrip(";"))

    for code, names in NAMES.items():
        if len(names) != len(ORDER):
            print("%s has %d names for %d books" % (code, len(names), len(ORDER)),
                  file=sys.stderr)
            return 1
        if len(set(names)) != len(names):
            print("%s repeats a name" % code, file=sys.stderr)
            return 1
        existing[code] = dict(zip(ORDER, names))

    line = "const NT_BOOK_NAMES=" + json.dumps(existing, ensure_ascii=False,
                                               separators=(",", ":")) + ";"
    PAGE.write_text(s[:i] + line + s[j:], encoding="utf-8")
    print("New Testament book names in %d languages: %s"
          % (len(existing), " ".join(sorted(existing))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
