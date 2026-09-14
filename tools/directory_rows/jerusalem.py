# -*- coding: utf-8 -*-
"""The ten sees of the Greek Orthodox Patriarchate of Jerusalem.

Few, and that is the shape of this Patriarchate rather than a gap in the
reading. Its own pages of administrative structure name two metropolises
with a see and a flock - Ptolemais at Akko and Nazareth - four patriarchal
commissaryships, at Amman, Jaffa, Gaza and Doha, and four exarchates of the
Holy Sepulchre, at Athens, Constantinople, Nicosia and Moscow. The rest of
its hierarchy holds titular sees without territory, and titles are not
rows.

All three of those pages were counted again on 14 September 2026, in Greek
and then in English, and they name the same ten bodies they named before:
two under Ἱεραί Μητροπόλεις, which the English site publishes as Holy
Bishoprics, four numbered under Πατριαρχικαί Ἐπιτροπεῖαι, and four under
Ἐξαρχίαι Παναγίου Τάφου. Ten rows, ten entries, and nothing missing. The
Patriarchate states no total in prose - neither its Greek portal nor its
English one puts a number on itself anywhere - so the count is its own three
lists and nothing else, which is why they were counted rather than trusted.

Two further pages of the same section were read and hold nothing for this
file. Εξωτερικά Ηγουμενεία names five external abbacies - Beit Jala, Haifa,
Rafidia and Nablus, Burqin, Nuss Ijbeil - which are churches and their
rectories rather than sees. Ἐνορίαι Ρωσοφώνου Κοινότητος names parishes.
Neither is a diocese, and parishes come with the pass that does parishes.

The Monastery of the Holy Cross on Long Island stands on the same page and
is not here: it is a monastery, and monasteries come as their own kind.
Mount Sinai stands there too and already has its row as an autonomous
Church.
"""

JE_M = ("https://jerusalem-patriarchate.info/"
        "%ce%b4%ce%b9%ce%bf%ce%b9%ce%ba%ce%b7%cf%84%ce%b9%ce%ba%ce%ae-"
        "%ce%b4%ce%b9%ce%ac%cf%81%ce%b8%cf%81%cf%89%cf%83%ce%b9%cf%82/"
        "%e1%bc%b1%ce%b5%cf%81%ce%b1%ce%af-%ce%bc%ce%b7%cf%84%cf%81%ce%bf"
        "%cf%80%cf%8c%ce%bb%ce%b5%ce%b9%cf%82/")
JE_E = ("https://jerusalem-patriarchate.info/"
        "%ce%b4%ce%b9%ce%bf%ce%b9%ce%ba%ce%b7%cf%84%ce%b9%ce%ba%ce%ae-"
        "%ce%b4%ce%b9%ce%ac%cf%81%ce%b8%cf%81%cf%89%cf%83%ce%b9%cf%82/"
        "%cf%80%ce%b1%cf%84%cf%81%ce%b9%ce%b1%cf%81%cf%87%ce%b9%ce%ba%ce%b1"
        "%ce%af-%e1%bc%90%cf%80%ce%b9%cf%84%cf%81%ce%bf%cf%80%ce%b5%e1%bf"
        "%96%ce%b1%ce%b9/")
JE_X = ("https://jerusalem-patriarchate.info/"
        "%ce%b4%ce%b9%ce%bf%ce%b9%ce%ba%ce%b7%cf%84%ce%b9%ce%ba%ce%ae-"
        "%ce%b4%ce%b9%ce%ac%cf%81%ce%b8%cf%81%cf%89%cf%83%ce%b9%cf%82/"
        "%e1%bc%90%ce%be%ce%b1%cf%81%cf%87%ce%af%ce%b1%ce%b9-%cf%80%ce%b1"
        "%ce%bd%ce%b1%ce%b3%ce%af%ce%bf%cf%85-%cf%84%ce%ac%cf%86%ce%bf%cf%85/")

ROWS = [
 dict(id="je-ptolemais", parent="jerusalem",
      name="Holy Metropolis of Ptolemais",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΙΣ ΠΤΟΛΕΜΑΪΔΟΣ",
      seat="Akko", country="IL",
      address=["Greek Orthodox Convent",
               "Old City, P. O. Box 2946, Akko"],
      sources=[JE_M]),

 dict(id="je-nazareth", parent="jerusalem",
      name="Holy Metropolis of Nazareth",
      local=u"ΙΕΡΑ ΜΗΤΡΟΠΟΛΙΣ ΝΑΖΑΡΕΤ",
      seat="Nazareth", country="IL",
      address=["Greek Orthodox Mitropolis, P.O. Box 15, Nazareth-Israel."],
      sources=[JE_M]),

 dict(id="je-amman", parent="jerusalem",
      name="Patriarchal Commissaryship in Amman",
      local=u"Πατριαρχική Ἐπιτροπεία ἐν Ἀμμάν",
      seat="Amman", country="JO",
      address=["Greek Orthodox Archdiocese, P.O. Box 910933, Amman 11191, Jordan."],
      site="https://orthodoxjordan.org/",
      sources=["https://orthodoxjordan.org/", JE_E]),

 dict(id="je-jaffa", parent="jerusalem",
      name="Patriarchal Commissaryship in Jaffa",
      local=u"Πατριαρχική Ἐπιτροπεία ἐν Ἰόππῃ",
      seat="Jaffa", country="IL",
      address=["Greek Orthodox Convent, Nativ Hamazalot 8, Jaffa 68021."],
      sources=[JE_E]),

 dict(id="je-gaza", parent="jerusalem",
      name="Patriarchal Commissaryship in Gaza",
      local=u"Πατριαρχική Ἐπιτροπεία ἐν Γάζῃ",
      seat="Gaza", country="PS",
      address=["Greek Orthodox Convent Gaza"],
      sources=[JE_E]),

 dict(id="je-qatar", parent="jerusalem",
      name="Patriarchal Commissaryship in Qatar",
      local=u"Πατριαρχική Ἐπιτροπεία ἐν Κάταρ",
      seat="Doha", country="QA",
      address=["Patriarchal Representation in Qatar, P.O. Box 23417, Doha, Qatar."],
      sources=[JE_E]),

 dict(id="je-exarch-greece", parent="jerusalem",
      name="Exarchate of the Holy Sepulchre in Greece",
      seat="Athens", country="GR",
      address=[u"Ἐρεχθέως 18, Πλάκα, Τ.Κ. 10556 Ἀθῆναι"],
      sources=[JE_X]),

 dict(id="je-exarch-constantinople", parent="jerusalem",
      name="Exarchate of the Holy Sepulchre in Constantinople",
      seat="Istanbul", country="TR",
      address=["Oruc Reis Sokak 24/7 Aya Yorgi Monastiri Heybeliada, Instanbul, Turkey"],
      sources=[JE_X]),

 dict(id="je-exarch-cyprus", parent="jerusalem",
      name="Exarchate of the Holy Sepulchre in Cyprus",
      seat="Nicosia", country="CY",
      address=[u"Ὁδὸς Ἀρχιμ. Κυπριανοῦ 4, 1015 Λευκωσία"],
      site="https://www.exarhiaptcy.com/",
      sources=["https://www.exarhiaptcy.com/", JE_X]),

 dict(id="je-exarch-moscow", parent="jerusalem",
      name="Exarchate of the Holy Sepulchre in Moscow",
      seat="Moscow", country="RU",
      address=["Philippovsky Str. 20, Moscow 121019, Russian Republic."],
      sources=[JE_X]),
]
