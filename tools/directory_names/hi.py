# -*- coding: utf-8 -*-
"""The directory's rows in Hindi.

Devanagari alone, as docs/HINDI.md requires, and the word order the published
commemorations keep without exception: the place first, in the genitive, then
the head. कलीसिया is feminine, so the postposition is की and not का. रूस की
कलीसिया and अमेरिका की रूढ़िवादी कलीसिया are not built here; they are what the
site already prints.

Three spellings compete in the corpus and were settled by counting.

  - **Athens is एथेंस**, 73 times across the calendar, the names and the
    lives, against अथेने 14, which stands only in the vocabulary table.
  - **Alexandria is सिकंदरिया**, 132 to अलेक्जेंड्रिया 62. Both are the site's
    own; the first is the one it shows most often and the one the register
    names first.
  - **Sinai is सिनाई**, 40 to सीनै 21, and the mountain is सिनाई पर्वत, 8 to
    सीनै पर्वत 4.

Constantinople keeps its received form कुस्तुंतुनिया, which the site writes
1,117 times and which no इस्तांबुल stands beside; it is the seat the
Ecumenical Patriarchate is known by here.

Written here because the site has never named them in Hindi, and named so that
nobody later mistakes them for received forms: तिराना Tirana, स्कोप्ये
Skopje, प्रेशोव Presov, तोक्यो Tokyo, तालिन Tallinn, सियोसेट Syosset,
फ़िनलैंड Finland, जापान Japan and स्लोवाकिया Slovakia, the last built on
स्लोवाक, which the site already writes of the faithful of that land. Two of
them - जापान and तोक्यो - are what the audit reports, and the report is
right: the corpus holds nothing they can be read off. The rest answer to
stems it already has.

महाधर्मप्रांत, for the Archbishopric of Ohrid, is धर्मप्रांत - the site's own
word for a diocese - under the महा- it takes everywhere else.
"""
NAMES = {
    "constantinople": u"कुस्तुंतुनिया की कलीसिया",
    "alexandria": u"सिकंदरिया की कलीसिया",
    "antioch": u"अंताकिया की कलीसिया",
    "jerusalem": u"यरूशलेम की कलीसिया",
    "russia": u"रूस की कलीसिया",
    "georgia": u"जॉर्जिया की कलीसिया",
    "serbia": u"सर्बिया की कलीसिया",
    "romania": u"रोमानिया की कलीसिया",
    "bulgaria": u"बुल्गारिया की कलीसिया",
    "cyprus": u"साइप्रस की कलीसिया",
    "greece": u"यूनान की कलीसिया",
    "albania": u"अल्बानिया की कलीसिया",
    "poland": u"पोलैंड की कलीसिया",
    "czech-slovakia": u"चेक भूमि और स्लोवाकिया की कलीसिया",
    "oca": u"अमेरिका की रूढ़िवादी कलीसिया",
    "macedonia": u"मकिदुनियाई रूढ़िवादी कलीसिया - ओहरिद महाधर्मप्रांत",
    "ukraine-uoc": u"यूक्रेन की कलीसिया",
    "ukraine-ocu": u"यूक्रेन की रूढ़िवादी कलीसिया",
    "sinai": u"सिनाई की कलीसिया",
    "finland": u"फ़िनलैंड की स्वायत्त कलीसिया",
    "japan": u"जापान की कलीसिया",
    "estonia-eaok": u"एस्तोनिया की रूढ़िवादी कलीसिया",
}
SEATS = {
    "Istanbul": u"कुस्तुंतुनिया",
    "Alexandria": u"सिकंदरिया",
    "Damascus": u"दमिश्क",
    "Jerusalem": u"यरूशलेम",
    "Moscow": u"मास्को",
    "Tbilisi": u"त्बिलिसी",
    "Belgrade": u"बेलग्रेड",
    "Bucharest": u"बुखारेस्ट",
    "Sofia": u"सोफिया",
    "Nicosia": u"निकोसिया",
    "Athens": u"एथेंस",
    "Tirana": u"तिराना",
    "Warsaw": u"वारसा",
    "Prešov": u"प्रेशोव",
    "Syosset, New York": u"सियोसेट, न्यूयॉर्क",
    "Skopje": u"स्कोप्ये",
    "Kyiv": u"कीव",
    "Mount Sinai": u"सिनाई पर्वत",
    "Helsinki": u"हेलसिंकी",
    "Tokyo": u"तोक्यो",
    "Tallinn": u"तालिन",
}
