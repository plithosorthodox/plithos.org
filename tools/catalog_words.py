#!/usr/bin/env python3
"""
The words the Library's two search boxes say, in every language it offers.

The catalog used to be reachable only by opening the rail, and the box that
was visible said "Search the corpus", which is not how a library speaks and
did not say what it searched. There are now two boxes side by side in the
masthead: one reads inside the books, the other reads across the shelf.

searchPh was already in the lexicon and translated, but nothing ever applied
it - the placeholder was written into the markup. It is applied now, so this
rewrites it in every language to say what that box actually does.

    python3 tools/catalog_words.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "library.html"

# fTagsMatching and fTitlesMatching head the two halves of a catalog result:
# the subjects, authors, centuries, purposes and translators that answer to
# the words, and then the books themselves.
WORDS = {
"en": {"searchPh": "Search inside the books - a word, or a phrase in quotation marks",
       "catalogPh": "Search the catalog - a title, an author, a subject",
       "fTagsMatching": "On the shelf", "fTitlesMatching": "Titles"},
"ru": {"searchPh": "Поиск внутри книг - слово или выражение в кавычках",
       "catalogPh": "Поиск по каталогу - название, автор, тема",
       "fTagsMatching": "На полке", "fTitlesMatching": "Названия"},
"uk": {"searchPh": "Пошук усередині книг - слово або вираз у лапках",
       "catalogPh": "Пошук у каталозі - назва, автор, тема",
       "fTagsMatching": "На полиці", "fTitlesMatching": "Назви"},
"sr": {"searchPh": "Претрага унутар књига - реч или израз под наводницима",
       "catalogPh": "Претрага каталога - наслов, аутор, тема",
       "fTagsMatching": "На полици", "fTitlesMatching": "Наслови"},
"el": {"searchPh": "Αναζήτηση μέσα στα βιβλία - μια λέξη ή μια φράση σε εισαγωγικά",
       "catalogPh": "Αναζήτηση στον κατάλογο - τίτλος, συγγραφέας, θέμα",
       "fTagsMatching": "Στο ράφι", "fTitlesMatching": "Τίτλοι"},
"ro": {"searchPh": "Caută în cărți - un cuvânt sau o expresie între ghilimele",
       "catalogPh": "Caută în catalog - un titlu, un autor, un subiect",
       "fTagsMatching": "În raft", "fTitlesMatching": "Titluri"},
"cu": {"searchPh": "Иска́нїе внꙋ́трь кни́гъ - сло́во или́ рече́нїе въ кавы́чкахъ",
       "catalogPh": "Иска́нїе по ро́списи - загла́вїе, списа́тель, предме́тъ",
       "fTagsMatching": "На поли́цѣ", "fTitlesMatching": "Загла́вїя"},
"ka": {"searchPh": "ძიება წიგნებში - სიტყვა ან ფრაზა ბრჭყალებში",
       "catalogPh": "ძიება კატალოგში - სათაური, ავტორი, თემა",
       "fTagsMatching": "თაროზე", "fTitlesMatching": "სათაურები"},
"es": {"searchPh": "Buscar dentro de los libros - una palabra o una frase entre comillas",
       "catalogPh": "Buscar en el catálogo - un título, un autor, un tema",
       "fTagsMatching": "En el estante", "fTitlesMatching": "Títulos"},
"pt": {"searchPh": "Buscar dentro dos livros - uma palavra ou uma frase entre aspas",
       "catalogPh": "Buscar no catálogo - um título, um autor, um tema",
       "fTagsMatching": "Na estante", "fTitlesMatching": "Títulos"},
"it": {"searchPh": "Cerca dentro i libri - una parola o una frase tra virgolette",
       "catalogPh": "Cerca nel catalogo - un titolo, un autore, un argomento",
       "fTagsMatching": "Sullo scaffale", "fTitlesMatching": "Titoli"},
"fr": {"searchPh": "Chercher dans les livres - un mot ou une expression entre guillemets",
       "catalogPh": "Chercher dans le catalogue - un titre, un auteur, un sujet",
       "fTagsMatching": "Sur le rayon", "fTitlesMatching": "Titres"},
"de": {"searchPh": "In den Büchern suchen - ein Wort oder eine Wendung in Anführungszeichen",
       "catalogPh": "Im Katalog suchen - ein Titel, ein Verfasser, ein Thema",
       "fTagsMatching": "Im Regal", "fTitlesMatching": "Titel"},
"ar": {"searchPh": "ابحث داخل الكتب - كلمة أو عبارة بين علامتي اقتباس",
       "catalogPh": "ابحث في الفهرس - عنوان أو مؤلف أو موضوع",
       "fTagsMatching": "على الرف", "fTitlesMatching": "العناوين"},
"zh": {"searchPh": "在书中搜索 - 一个词，或用引号括住的短语",
       "catalogPh": "搜索书目 - 书名、作者、主题",
       "fTagsMatching": "书架上", "fTitlesMatching": "书名"},
"ja": {"searchPh": "本文を検索 - 語、または引用符で囲んだ句",
       "catalogPh": "目録を検索 - 書名、著者、主題",
       "fTagsMatching": "書架", "fTitlesMatching": "書名"},
"ko": {"searchPh": "본문 검색 - 단어 또는 따옴표로 묶은 구절",
       "catalogPh": "목록 검색 - 서명, 저자, 주제",
       "fTagsMatching": "서가", "fTitlesMatching": "서명"},
"sw": {"searchPh": "Tafuta ndani ya vitabu - neno, au msemo katika alama za nukuu",
       "catalogPh": "Tafuta katika orodha - kichwa, mwandishi, mada",
       "fTagsMatching": "Rafuni", "fTitlesMatching": "Vichwa"},
"hi": {"searchPh": "पुस्तकों में खोजें - एक शब्द, या उद्धरण चिह्नों में वाक्यांश",
       "catalogPh": "सूची में खोजें - शीर्षक, लेखक, विषय",
       "fTagsMatching": "शेल्फ़ पर", "fTitlesMatching": "शीर्षक"},
"hy": {"searchPh": "Փնտրել գրքերի մեջ - բառ կամ չակերտների մեջ արտահայտություն",
       "catalogPh": "Փնտրել ցանկում - վերնագիր, հեղինակ, թեմա",
       "fTagsMatching": "Դարակին", "fTitlesMatching": "Վերնագրեր"},
"arc": {"searchPh": "ܒܥܝ ܓܘ ܟܬܒܐ - ܡܠܬܐ ܐܘ ܡܡܠܠܐ ܒܝܬ ܢܝܫܐ",
        "catalogPh": "ܒܥܝ ܒܪܘܫܡܐ - ܟܘܢܝܐ, ܟܬܘܒܐ, ܢܝܫܐ",
        "fTagsMatching": "ܥܠ ܐܣܛܘܐ", "fTitlesMatching": "ܟܘܢܝܐ"},
}

CURVED = ("–", "—", "‘", "’", "“", "”")


def main():
    s = PAGE.read_text(encoding="utf-8")
    i = s.index("const RLEX={")
    j = s.index("\n};", i)
    head, block, tail = s[:i], s[i:j + 2], s[j + 2:]

    touched = 0
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
        end = block.index("\n", at)
        line = block[at:end]

        add = []
        for k, v in words.items():
            enc = json.dumps(v, ensure_ascii=False)
            # An existing key is replaced in place; a new one is inserted.
            pat = re.compile(r'"?%s"?:"(?:[^"\\]|\\.)*"' % re.escape(k))
            if pat.search(line):
                line = pat.sub('"%s":%s' % (k, enc.replace("\\", "\\\\")), line, count=1)
            else:
                add.append('"%s":%s,' % (k, enc))
        line = "".join(add) + line
        block = block[:at] + line + block[end:]
        touched += 1

    PAGE.write_text(head + block + tail, encoding="utf-8")
    print("wrote the search words to %d languages" % touched)
    return 0


if __name__ == "__main__":
    sys.exit(main())
