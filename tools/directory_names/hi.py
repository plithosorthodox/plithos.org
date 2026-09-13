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

The official names are a third table, STYLED, and not a second version of the
first: the label is the list's word for a body and the style is the body's
own. Five of the nine stood already in the Hindi this site publishes and are
taken whole - विश्वव्यापी पितृसत्ता and the रूसी, सर्बियाई, रोमानियाई and
यूक्रेनी रूढ़िवादी कलीसिया of the commemorations.

पितृसत्ता is the site's own word for a patriarchate against प्राधिधर्माध्यक्ष for the
man, and the three ancient sees take it with की, as अंताकिया की पितृसत्ता already
does. अंताकिया और समस्त पूर्व follows the मास्को और समस्त रूस of the patriarch of
Moscow.

The word Greek in the English style of Antioch and of Jerusalem is the Rum
rite and communion, not the Greek nation, and no Hindi name for either body
carries it, so it is not written here.
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
    "albanian-americas": u"अमेरिका का अल्बानियाई रूढ़िवादी धर्मप्रांत",
    "acrod": u"उत्तर अमेरिका का अमेरिकी कार्पेथो-रूसी रूढ़िवादी धर्मप्रांत",
    "ep-thyateira": u"थुआतीरा और ग्रेट ब्रिटेन का महाधर्मप्रांत",
    "goarch": u"अमेरिका का यूनानी रूढ़िवादी महाधर्मप्रांत",
    "ep-france": u"फ़्रांस का यूनानी रूढ़िवादी महाधर्मप्रांत",
    "ep-germany": u"जर्मनी का यूनानी रूढ़िवादी महाधर्मप्रांत",
    "ep-austria": u"ऑस्ट्रिया का पवित्र महाधर्मप्रांत",
    "ep-korea": u"कोरिया का पवित्र महाधर्मप्रांत",
    "ep-spain": u"स्पेन और पुर्तगाल का पवित्र महाधर्मप्रांत",
    "ep-belgium": u"बेल्जियम का महाधर्मप्रांत",
    "ep-sweden": u"स्वीडन और समस्त स्कैंडिनेविया का महाधर्मप्रांत",
    "ep-switzerland": u"स्विट्ज़रलैंड का महाधर्मप्रांत",
    "ep-hongkong": u"हांगकांग और दक्षिण-पूर्व एशिया का रूढ़िवादी महाधर्मप्रांत",
    "ep-singapore": u"सिंगापुर और दक्षिण एशिया का रूढ़िवादी महाधर्मप्रांत",
    "ep-italy": u"इटली और माल्टा का पवित्र रूढ़िवादी महाधर्मप्रांत",
    "uocc": u"कनाडा की यूक्रेनी रूढ़िवादी कलीसिया",
    "uoc-usa": u"संयुक्त राज्य अमेरिका की यूक्रेनी रूढ़िवादी कलीसिया",
    "antiochian-na": u"उत्तर अमेरिका का अन्ताकियाई रूढ़िवादी मसीही महाधर्मप्रांत",
    "rocor": u"विदेश की रूसी रूढ़िवादी कलीसिया",
    "mp-parishes-usa": u"संयुक्त राज्य अमेरिका में पितृसत्ता की पल्लियाँ",
    "serbian-eastern": u"पूर्वी अमेरिका का धर्मप्रांत",
    "serbian-midwestern": u"नई ग्राचानित्सा और मध्यपश्चिमी अमेरिका का धर्मप्रांत",
    "serbian-western": u"पश्चिमी अमेरिका का धर्मप्रांत",
    "romanian-americas": u"अमेरिका का रोमानियाई रूढ़िवादी महाधर्मप्रांत",
    "bulgarian-usa": u"संयुक्त राज्य अमेरिका, कनाडा और ऑस्ट्रेलिया का बुल्गारियाई पूर्वी रूढ़िवादी धर्मप्रांत",
    "oca-albanian": u"अल्बानियाई महाधर्मप्रांत",
    "oca-canada": u"कनाडा का महाधर्मप्रांत",
    "oca-washington": u"वाशिंगटन का महाधर्मप्रांत",
    "oca-western-pa": u"पश्चिमी पेन्सिल्वेनिया का महाधर्मप्रांत",
    "oca-bulgarian": u"बुल्गारियाई धर्मप्रांत",
    "oca-eastern-pa": u"पूर्वी पेन्सिल्वेनिया का धर्मप्रांत",
    "oca-mexico": u"मेक्सिको का धर्मप्रांत",
    "oca-new-england": u"न्यू इंग्लैंड का धर्मप्रांत",
    "oca-ny-nj": u"न्यूयॉर्क और न्यू जर्सी का धर्मप्रांत",
    "oca-alaska": u"सिटका और अलास्का का धर्मप्रांत",
    "oca-midwest": u"अमेरिका के मध्यपश्चिम का धर्मप्रांत",
    "oca-south": u"अमेरिका के दक्षिण का धर्मप्रांत",
    "oca-west": u"अमेरिका के पश्चिम का धर्मप्रांत",
    "oca-romanian": u"रोमानियाई धर्माध्यक्षता",
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
    "Alexandria, Virginia": u"अलेक्जेंड्रिया, वर्जीनिया",
    "Alhambra, California": u"अल्हाम्ब्रा, कैलिफ़ोर्निया",
    "Anchorage, Alaska": u"एंकरेज, अलास्का",
    "Bath, Pennsylvania": u"बाथ, पेन्सिल्वेनिया",
    "Bonn": u"बॉन",
    "Boston, Massachusetts": u"बोस्टन, मैसाचुसेट्स",
    "Bronxville, New York": u"ब्रॉन्क्सविल, न्यूयॉर्क",
    "Brussels": u"ब्रुसेल्स",
    "Chambesy": u"शांबेज़ी",
    "Chicago, Illinois": u"शिकागो, इलिनोइस",
    "Cranberry Township, Pennsylvania": u"क्रैनबेरी टाउनशिप, पेन्सिल्वेनिया",
    "Dallas, Texas": u"डलास, टेक्सास",
    "Englewood, New Jersey": u"एंगलवुड, न्यू जर्सी",
    "Hong Kong": u"हांगकांग",
    "Jackson, Michigan": u"जैक्सन, मिशिगन",
    "Johnstown, Pennsylvania": u"जॉन्सटाउन, पेन्सिल्वेनिया",
    "London": u"लंदन",
    "Madrid": u"मैड्रिड",
    "Mexico City": u"मेक्सिको सिटी",
    "New Rochelle, New York": u"न्यू रोशेल, न्यूयॉर्क",
    "New York": u"न्यूयॉर्क",
    "Paris": u"पेरिस",
    "Rawdon, Quebec": u"रॉडन, क्यूबेक",
    "San Francisco, California": u"सैन फ्रांसिस्को, कैलिफ़ोर्निया",
    "Seoul": u"सियोल",
    "Singapore": u"सिंगापुर",
    "Somerset, New Jersey": u"सॉमरसेट, न्यू जर्सी",
    "Stockholm": u"स्टॉकहोम",
    "Third Lake, Illinois": u"थर्ड लेक, इलिनोइस",
    "Toledo, Ohio": u"टोलीडो, ओहायो",
    "Venice": u"वेनिस",
    "Vienna": u"वियना",
    "Windsor, Connecticut": u"विंडसर, कनेक्टिकट",
    "Winnipeg, Manitoba": u"विनिपेग, मैनिटोबा",
}
STYLED = {
    "constantinople": u"विश्वव्यापी पितृसत्ता",
    "alexandria": u"सिकंदरिया की पितृसत्ता",
    "antioch": u"अंताकिया और समस्त पूर्व की पितृसत्ता",
    "jerusalem": u"यरूशलेम की पितृसत्ता",
    "russia": u"रूसी रूढ़िवादी कलीसिया",
    "serbia": u"सर्बियाई रूढ़िवादी कलीसिया",
    "romania": u"रोमानियाई रूढ़िवादी कलीसिया",
    "bulgaria": u"बुल्गारियाई रूढ़िवादी कलीसिया - बुल्गारियाई पितृसत्ता",
    "ukraine-uoc": u"यूक्रेनी रूढ़िवादी कलीसिया",
}
