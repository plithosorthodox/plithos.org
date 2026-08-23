"""Where each language's New Testament comes from.

The site carried a New Testament in nineteen languages and, in eighteen of
them, carried only the verses the lectionary reads. A reader who opened the
Apocalypse in Russian was given the seventh chapter and no other; Luke stood
at four hundred and eighty-six verses of eleven hundred and fifty-one. The
numbering went with it: where a verse had been dropped the ones after it moved
up to fill the space, so Matthew 3:16 in Russian gave the words of 3:17 and a
citation could not be trusted. Nothing was ever short at the source.

This names, for every language, the edition already published here and the
place that holds it whole, so the same translation can be carried entire and
numbered as the edition numbers it.
"""

# lang -> (backend, key, edition, licence, direction)
#
# Editions were confirmed by taking every verse the site already published and
# looking for it in the candidate source: an edition that is the same edition
# holds essentially all of them. Where the confirmed source does not carry the
# whole book, or the text disagreed with the language the site offers, the
# reason is written against the entry.
SOURCES = {
    # Confirmed against what was published, verse for verse.
    "arc": ("getbible", "peshitta",       "Peshitta",                   "Public Domain", "rtl"),
    "hy":  ("getbible", "westernarmenian", "Western Armenian",          "Public Domain", "ltr"),
    "it":  ("getbible", "riveduta",       "Riveduta (1927)",            "Public Domain", "ltr"),
    "ja":  ("getbible", "japraguet",      "Raguet-yaku (1910)",         "Public Domain", "ltr"),
    "sr":  ("getbible", "srkdekavski",    "Danicic-Karadzic (Ekavian)", "Public Domain", "ltr"),
    "uk":  ("getbible", "ukranian",       "Kulish (1871)",              "Public Domain", "ltr"),
    "ru":  ("getbible", "synodal",        "Synodal (1876)",             "Public Domain", "ltr"),
    "de":  ("getbible", "schlachter",     "Schlachter (1951)",          "Public Domain", "ltr"),
    "es":  ("getbible", "valera",         "Reina Valera (1909)",        "Public Domain", "ltr"),

    # The same Korean Bible in a later orthography; three quarters of the
    # published verses stand unchanged and the rest differ only in spelling.
    "ko":  ("getbible", "korean",         "Korean",                     "Public Domain", "ltr"),

    # Van Dyke, as printed: with the vowel points. The copy published here had
    # them stripped.
    "ar":  ("getbible", "arabicsv",       "Smith & Van Dyke (1865)",    "Public Domain", "rtl"),

    # The site offers Chinese as 简体中文 and was serving the Union Version in
    # traditional characters, one space between every glyph. Same translation,
    # the script the reader asked for.
    "zh":  ("getbible", "cus",            "Union Version (Simplified)", "Public Domain", "ltr"),

    # Greek reads the Byzantine text the Church uses, as it did before.
    "el":  ("helloao",  "grc_byz",        "Byzantine Majority Text",    "Public Domain", "ltr"),

    # French and Portuguese were published from an edition that could not be
    # identified: the text matched no French or Portuguese Bible on offer
    # anywhere. Each now reads the edition this site's own Old Testament reads,
    # so the two halves are one Bible at last.
    "fr":  ("getbible", "darby",          "Darby",                      "Public Domain", "ltr"),
    "pt":  ("getbible", "livre",          "Biblia Livre",               "CC BY", "ltr"),

    # Swahili was published from a source that does not carry Philippians at
    # all. This edition carries the whole of both Testaments.
    "sw":  ("helloao",  "swh_onmm",       "Maandiko Matakatifu",
            "Copyright 2018, 2024 Biblica, Inc. Released for free use.", "ltr"),

    # Church Slavonic had an Old Testament here and no New Testament. This is
    # the same Elizabeth Bible of 1751 that the Old Testament is taken from.
    "cu":  ("getbible", "csielizabeth",   "Elizabeth Bible (1751)",     "Public Domain", "ltr"),

    # Hindi, Bengali and Urdu. Hindi had a New Testament here whose source
    # states no licence at all; Bengali and Urdu had none. There is no
    # Orthodox edition in any of the three and no edition of the whole canon,
    # so each reads the latest that is free to take, and the entry for it says
    # what it carries and what it does not. Each is the edition that language's
    # Old Testament is taken from, so the two halves are one Bible.
    "hi":  ("helloao", "hin_cvb", "Hindi Contemporary Version",
            "Copyright 1978, 2009, 2016, 2019 Biblica, Inc. "
            "Released for free use.", "ltr"),
    "bn":  ("helloao", "ben_ocv", "Bengali Contemporary Version",
            "Copyright 2022 Biblica, Inc. Released for free use.", "ltr"),
    "ur":  ("helloao", "urd_oucv", "Urdu Contemporary Version",
            "Copyright 1999, 2005, 2022, 2024 Biblica, Inc. "
            "Released for free use.", "rtl"),

    # Georgian, in the recension of St George the Hagiorite, which is the
    # text the Georgian Church reads and the register her Old Testament is
    # already published in here. See tools/nt_ka.py.
    "ka":  ("allgeo-ka", "giorgi", "St George the Hagiorite's recension",
            "Public Domain", "ltr"),

    # English is already whole and is left exactly as it was published.
    "en":  ("published", "en",            "King James Version (1611)",  "Public Domain", "ltr"),

    # Romanian reads the Holy Synod's edition of 1914, the Orthodox Church of
    # Romania's own and the edition this site's Romanian Old Testament is
    # already taken from. What was published was Cornilescu, a Protestant
    # translation whose author died in 1975.
    "ro":  ("wikisource-ro", "Biblia 1914", "Editia Sfantului Sinod (1914)",
            "Public Domain", "ltr"),
}

# The Synod's own names for the books of the New Testament, against the names
# the reader shows. Read off the edition's own table of contents.
RO_NT = {
    "Matthew": "Matei", "Mark": "Marcu", "Luke": "Luca", "John": "Ioan",
    "Acts": "Faptele Apostolilor", "Romans": "Romani",
    "1 Corinthians": "1 Corinteni", "2 Corinthians": "2 Corinteni",
    "Galatians": "Galateni", "Ephesians": "Efeseni",
    "Philippians": "Filippiseni", "Colossians": "Colaseni",
    "1 Thessalonians": "1 Tesalonicheni", "2 Thessalonians": "2 Tesalonicheni",
    "1 Timothy": "1 Timotei", "2 Timothy": "2 Timotei", "Titus": "Tit",
    "Philemon": "Filimon", "Hebrews": "Evrei", "James": "Iacov",
    "1 Peter": "1 Petru", "2 Peter": "2 Petru", "1 John": "1 Ioan",
    "2 John": "2 Ioan", "3 John": "3 Ioan", "Jude": "Iuda",
    "Revelation": "Apocalipsis",
}

# The order the reader shows, and the numbers getbible and eBible use.
NT_ORDER = [
    ("Matthew", 40, "MAT"), ("Mark", 41, "MRK"), ("Luke", 42, "LUK"),
    ("John", 43, "JHN"), ("Acts", 44, "ACT"), ("Romans", 45, "ROM"),
    ("1 Corinthians", 46, "1CO"), ("2 Corinthians", 47, "2CO"),
    ("Galatians", 48, "GAL"), ("Ephesians", 49, "EPH"),
    ("Philippians", 50, "PHP"), ("Colossians", 51, "COL"),
    ("1 Thessalonians", 52, "1TH"), ("2 Thessalonians", 53, "2TH"),
    ("1 Timothy", 54, "1TI"), ("2 Timothy", 55, "2TI"), ("Titus", 56, "TIT"),
    ("Philemon", 57, "PHM"), ("Hebrews", 58, "HEB"), ("James", 59, "JAS"),
    ("1 Peter", 60, "1PE"), ("2 Peter", 61, "2PE"), ("1 John", 62, "1JN"),
    ("2 John", 63, "2JN"), ("3 John", 64, "3JN"), ("Jude", 65, "JUD"),
    ("Revelation", 66, "REV"),
]
