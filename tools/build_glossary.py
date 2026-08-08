#!/usr/bin/env python3
"""
Build data/glossary.v3.json.

Terms are held here rather than in the page so they stay reviewable in a diff
and can be regenerated. Each entry:

    id      stable slug, used in the URL (#t=antidoron)
    t       the headword in English usage
    forms   the word in its source languages - part of the definition, not a
            translation. el Greek, cu Church Slavonic, la Latin, ar Arabic,
            ka Georgian, hy Armenian, arc Syriac.
    d       definition, one to three sentences
    tags    for filtering and for the tag cloud
    see     related term ids

Translating the definitions is a separate pass: add a "tr" object keyed by
language code. Nothing here is translated yet, and glossary.html says so
plainly rather than showing English under a Greek flag.

    python3 tools/build_glossary.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n_glossary as I18N

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "glossary.v3.json"
TERMS_DIR = Path(__file__).resolve().parent / "glossary_terms"


def load_terms():
    """One module per language under tools/glossary_terms/, each holding
    TERMS = {term id: (headword, definition)}. A language is published the
    moment its file is complete; absent ones simply fall back to English."""
    import importlib
    out = {}
    for f in sorted(TERMS_DIR.glob("*.py")):
        if f.stem.startswith("_"):
            continue
        mod = importlib.import_module("glossary_terms." + f.stem)
        out[f.stem] = getattr(mod, "TERMS", {})
    return out

T = [
# ---------------------------------------------------------------- the services
("divine-liturgy", "Divine Liturgy", {"el": "Θεία Λειτουργία", "cu": "Боже́ственная Литургі́я"},
 "The eucharistic service of the Church, at which the bread and wine are offered and become the Body and Blood of Christ. Served most often in the form of St John Chrysostom.",
 ["service", "eucharist"], ["anaphora", "prothesis", "liturgy-of-basil"]),
("liturgy-of-basil", "Liturgy of St Basil", {"el": "Λειτουργία τοῦ Μεγάλου Βασιλείου"},
 "A longer form of the Divine Liturgy with its own anaphora, served ten times a year: the Sundays of Great Lent except Palm Sunday, Holy Thursday and Holy Saturday, the eves of Nativity and Theophany, and St Basil's feast on 1 January.",
 ["service", "eucharist"], ["divine-liturgy"]),
("presanctified", "Liturgy of the Presanctified Gifts", {"el": "Προηγιασμένη Θεία Λειτουργία"},
 "A vespers service with communion from Gifts consecrated at the preceding Sunday's Liturgy, served on weekdays of Great Lent, when the full Liturgy is not celebrated.",
 ["service", "lent", "eucharist"], ["great-lent"]),
("vespers", "Vespers", {"el": "Ἑσπερινός", "cu": "Вече́рня"},
 "The evening service, which begins the liturgical day. Opens with Psalm 103 and the lighting of lamps.",
 ["service", "hours"], ["orthros", "vigil", "compline"]),
("orthros", "Orthros (Matins)", {"el": "Ὄρθρος", "cu": "У́треня"},
 "The morning service, the longest of the daily offices, containing the six psalms, the canon, and in most uses the Great Doxology.",
 ["service", "hours"], ["vespers", "canon-hymn", "doxology"]),
("compline", "Compline", {"el": "Ἀπόδειπνον", "cu": "Повече́ріе"},
 "The service after supper, before sleep. Small Compline is used most of the year; Great Compline belongs to Great Lent and certain vigils.",
 ["service", "hours"], ["vespers"]),
("vigil", "All-Night Vigil", {"el": "Ἀγρυπνία", "cu": "Всено́щное бдѣ́ніе"},
 "Vespers, Orthros and the First Hour joined into one service on the eve of Sundays and great feasts.",
 ["service"], ["vespers", "orthros", "litya"]),
("hours", "The Hours", {"el": "Ὧραι", "cu": "Часы́"},
 "The four short offices of the day: First, Third, Sixth and Ninth, reckoned from sunrise and each with its own psalms and theme.",
 ["service", "hours"], ["vespers", "orthros"]),
("moleben", "Moleben", {"cu": "Молебенъ", "el": "Παράκλησις"},
 "A service of supplication to Christ, the Theotokos or a saint, outside the fixed cycle, for a particular need or thanksgiving.",
 ["service"], ["paraklesis", "panikhida"]),
("paraklesis", "Paraklesis", {"el": "Παράκλησις"},
 "The canon of supplication to the Theotokos. The Small Paraklesis is sung through the Dormition fast; the Great belongs to times of particular affliction.",
 ["service", "theotokos"], ["moleben", "canon-hymn"]),
("panikhida", "Panikhida", {"el": "Μνημόσυνον", "cu": "Пани́хида"},
 "The memorial service for the departed, served on the third, ninth and fortieth days, at anniversaries, and on the Soul Saturdays.",
 ["service", "departed"], ["soul-saturday", "koliva"]),
("litya", "Litya", {"el": "Λιτή"},
 "The procession and intercession at vigil, at which loaves, wheat, wine and oil are blessed.",
 ["service"], ["vigil", "artoklasia"]),
("artoklasia", "Artoklasia", {"el": "Ἀρτοκλασία"},
 "The blessing and breaking of five loaves at the litya, recalling the feeding of the five thousand.",
 ["service", "bread"], ["litya"]),

# ---------------------------------------------------------------- eucharist
("anaphora", "Anaphora", {"el": "Ἀναφορά"},
 "The central prayer of the Liturgy, the offering, containing the words of institution and the epiklesis.",
 ["eucharist", "prayer"], ["epiklesis", "divine-liturgy"]),
("epiklesis", "Epiklesis", {"el": "Ἐπίκλησις"},
 "The invocation of the Holy Spirit upon the gifts and upon those gathered, at which the Orthodox Church understands the consecration to be accomplished.",
 ["eucharist", "prayer"], ["anaphora"]),
("prothesis", "Prothesis (Proskomedia)", {"el": "Πρόθεσις, Προσκομιδή", "cu": "Проскоми́дія"},
 "The preparation of the bread and wine before the Liturgy, at the table of oblation, at which particles are cut for the living and the departed.",
 ["eucharist"], ["prosphora", "diskos", "lance"]),
("prosphora", "Prosphora", {"el": "Πρόσφορον", "cu": "Просфора́"},
 "The leavened loaf offered for the Liturgy, stamped with a seal from which the Lamb is cut.",
 ["eucharist", "bread"], ["prothesis", "antidoron", "lamb"]),
("lamb", "The Lamb", {"el": "Ἀμνός", "cu": "А́гнецъ"},
 "The square portion cut from the first prosphora which is consecrated and becomes the Body of Christ.",
 ["eucharist", "bread"], ["prosphora", "prothesis"]),
("antidoron", "Antidoron", {"el": "Ἀντίδωρον"},
 "The remainder of the prosphora, blessed but not consecrated, distributed at the end of the Liturgy. The name means 'instead of the gift': it is given to all present, including those who did not commune.",
 ["eucharist", "bread"], ["prosphora"]),
("zeon", "Zeon", {"el": "Ζέον"},
 "The hot water poured into the chalice before communion, signifying the warmth of the Holy Spirit and that the Body received is living.",
 ["eucharist"], ["chalice"]),
("chalice", "Chalice", {"el": "Ποτήριον", "cu": "Поти́ръ"},
 "The cup holding the wine of the offering and, after the consecration, the Blood of Christ.",
 ["vessel", "eucharist"], ["diskos", "zeon"]),
("diskos", "Diskos (Paten)", {"el": "Δίσκος"},
 "The footed plate on which the Lamb and the commemorative particles are placed.",
 ["vessel", "eucharist"], ["chalice", "asterisk", "prothesis"]),
("asterisk", "Asterisk", {"el": "Ἀστερίσκος", "cu": "Звѣзди́ца"},
 "The hinged star set over the diskos to keep the veil from disturbing the particles; it recalls the star over Bethlehem.",
 ["vessel", "eucharist"], ["diskos"]),
("lance", "Lance", {"el": "Λόγχη", "cu": "Копіе́"},
 "The small spear-shaped knife used at the prothesis to cut the Lamb and the particles, recalling the lance that pierced Christ's side.",
 ["vessel", "eucharist"], ["prothesis"]),
("spoon", "Communion Spoon", {"el": "Λαβίς"},
 "The spoon by which the faithful receive the Body and Blood together. Its Greek name means 'tongs', after the coal taken with tongs in Isaiah's vision.",
 ["vessel", "eucharist"], ["chalice"]),
("aer", "Aer", {"el": "Ἀήρ", "cu": "Воздýхъ"},
 "The largest of the veils, covering both diskos and chalice, waved over the gifts during the Creed.",
 ["vessel", "eucharist"], ["diskos", "chalice"]),
("tabernacle", "Tabernacle", {"el": "Ἀρτοφόριον"},
 "The vessel on the altar table in which the Presanctified Gifts are reserved for the sick and for the Presanctified Liturgy.",
 ["vessel", "eucharist"], ["presanctified", "altar-table"]),

# ---------------------------------------------------------------- books
("horologion", "Horologion", {"el": "Ὡρολόγιον", "cu": "Часосло́въ"},
 "The book of hours, containing the fixed portions of the daily cycle of services.",
 ["book"], ["hours", "psalter"]),
("euchologion", "Euchologion", {"el": "Εὐχολόγιον", "cu": "Требникъ"},
 "The priest's service book, holding the prayers of the Liturgy, the mysteries, and the occasional offices.",
 ["book"], ["divine-liturgy"]),
("menaion", "Menaion", {"el": "Μηναῖον", "cu": "Мине́я"},
 "The twelve volumes of hymns for the fixed feasts, one for each month of the year.",
 ["book", "calendar"], ["synaxarion", "typikon"]),
("triodion", "Triodion", {"el": "Τριῴδιον", "cu": "Тріо́дь По́стная"},
 "The book and the season of the weeks before and through Great Lent, up to Holy Saturday. Named for its canons of three odes.",
 ["book", "calendar", "lent"], ["pentecostarion", "great-lent"]),
("pentecostarion", "Pentecostarion", {"el": "Πεντηκοστάριον", "cu": "Тріо́дь Цвѣтна́я"},
 "The book and the season from Pascha to the Sunday of All Saints.",
 ["book", "calendar"], ["triodion", "pascha"]),
("octoechos", "Octoechos", {"el": "Ὀκτώηχος", "cu": "Октои́хъ"},
 "The book of the eight tones, governing the resurrectional hymns of the ordinary weeks in an eight-week cycle.",
 ["book", "music"], ["tone", "canon-hymn"]),
("typikon", "Typikon", {"el": "Τυπικόν", "cu": "Тѵпико́нъ"},
 "The book of rubrics, directing how the services and the fasts are kept and how the cycles are combined when they coincide.",
 ["book"], ["menaion", "octoechos"]),
("psalter", "Psalter", {"el": "Ψαλτήριον", "cu": "Псалти́рь"},
 "The 150 psalms divided into twenty kathismata for reading through the services, together with the nine biblical odes.",
 ["book", "scripture"], ["kathisma", "odes"]),
("synaxarion", "Synaxarion", {"el": "Συναξάριον"},
 "The account of the saints and feasts appointed for the day, read at Orthros; also the book collecting them.",
 ["book", "calendar", "saints"], ["menaion", "menologion"]),
("menologion", "Menologion", {"el": "Μηνολόγιον"},
 "A collection of saints' lives arranged by the days of the month.",
 ["book", "saints"], ["synaxarion"]),
("rudder", "The Rudder (Pedalion)", {"el": "Πηδάλιον"},
 "The principal Greek collection of the canons of the Church with commentary, compiled by St Nikodemos of the Holy Mountain and St Agapios, published 1800.",
 ["book", "canon-law"], ["canon-law", "ecumenical-council"]),
("philokalia", "Philokalia", {"el": "Φιλοκαλία"},
 "The anthology of ascetic and contemplative texts from the fourth to the fifteenth centuries, compiled by St Nikodemos and St Makarios of Corinth, published 1782.",
 ["book", "ascetic"], ["hesychasm", "jesus-prayer"]),

# ---------------------------------------------------------------- hymnography
("troparion", "Troparion", {"el": "Τροπάριον"},
 "The principal short hymn of a feast or saint, stating its theme. Also called the apolytikion when sung at the dismissal.",
 ["hymn"], ["kontakion", "tone"]),
("kontakion", "Kontakion", {"el": "Κοντάκιον"},
 "A second short hymn summarising the feast or the saint. Originally a long poetic sermon in many stanzas, of which the surviving kontakion is the first.",
 ["hymn"], ["troparion", "oikos", "akathist"]),
("oikos", "Oikos", {"el": "Οἶκος"},
 "The stanza that follows the kontakion, expanding its theme.",
 ["hymn"], ["kontakion"]),
("canon-hymn", "Canon", {"el": "Κανών", "cu": "Кано́нъ"},
 "The long hymn of Orthros in eight or nine odes, each keyed to one of the biblical canticles.",
 ["hymn"], ["irmos", "katavasia", "odes"]),
("irmos", "Irmos", {"el": "Εἱρμός"},
 "The first troparion of each ode of a canon, setting its melody and metre and linking it to the biblical canticle.",
 ["hymn", "music"], ["canon-hymn", "katavasia"]),
("katavasia", "Katavasia", {"el": "Καταβασία"},
 "The irmos repeated at the end of an ode, so called because the choirs descended from their places to sing it together.",
 ["hymn", "music"], ["irmos", "canon-hymn"]),
("sticheron", "Sticheron", {"el": "Στιχηρόν"},
 "A hymn sung between the verses of a psalm, chiefly at vespers and orthros.",
 ["hymn"], ["troparion"]),
("theotokion", "Theotokion", {"el": "Θεοτοκίον"},
 "A hymn to the Mother of God, placed at the end of a group of hymns.",
 ["hymn", "theotokos"], ["troparion", "stavrotheotokion"]),
("stavrotheotokion", "Stavrotheotokion", {"el": "Σταυροθεοτοκίον"},
 "A theotokion on the Mother of God at the Cross, used on Wednesdays and Fridays.",
 ["hymn", "theotokos"], ["theotokion"]),
("prokeimenon", "Prokeimenon", {"el": "Προκείμενον"},
 "A verse, usually from the psalms, sung before a scripture reading.",
 ["hymn", "scripture"], ["alleluiarion"]),
("alleluiarion", "Alleluiarion", {"el": "Ἀλληλουϊάριον"},
 "The Alleluia with its verses, sung between the Epistle and the Gospel.",
 ["hymn", "scripture"], ["prokeimenon"]),
("tone", "Tone (Echos)", {"el": "Ἦχος", "cu": "Гла́съ"},
 "One of the eight musical modes in which the hymns are sung, changing week by week through the Octoechos.",
 ["music"], ["octoechos", "irmos"]),
("trisagion", "Trisagion", {"el": "Τρισάγιον"},
 "'Holy God, Holy Mighty, Holy Immortal, have mercy on us', sung thrice; also the name of the short set of prayers that begins most services.",
 ["hymn", "prayer"], ["divine-liturgy"]),
("cherubic-hymn", "Cherubic Hymn", {"el": "Χερουβικὸς Ὕμνος"},
 "The hymn sung during the Great Entrance, at which the faithful set aside all earthly care to receive the King of all.",
 ["hymn", "eucharist"], ["great-entrance"]),
("doxology", "Great Doxology", {"el": "Δοξολογία"},
 "'Glory to God in the highest', sung towards the end of Orthros on Sundays and feasts.",
 ["hymn"], ["orthros"]),
("polyeleos", "Polyeleos", {"el": "Πολυέλεος"},
 "Psalms 134 and 135 sung at festal Orthros, so called from their refrain 'for His mercy endures forever'.",
 ["hymn"], ["orthros"]),
("akathist", "Akathist", {"el": "Ἀκάθιστος Ὕμνος"},
 "A hymn of twenty-four stanzas sung standing, the name meaning 'not seated'. The original is to the Theotokos; many later akathists follow its form.",
 ["hymn", "theotokos"], ["kontakion", "salutations"]),
("salutations", "Salutations", {"el": "Χαιρετισμοί"},
 "The Friday evening services of Great Lent at which the Akathist to the Theotokos is sung in parts.",
 ["service", "lent", "theotokos"], ["akathist", "great-lent"]),
("kathisma", "Kathisma", {"el": "Κάθισμα"},
 "One of the twenty divisions of the Psalter; also a sessional hymn sung after it, during which sitting is permitted.",
 ["hymn", "scripture"], ["psalter"]),
("odes", "Biblical Odes", {"el": "Ὠδαί"},
 "The nine scriptural canticles, from the songs of Moses to the Magnificat and the prayer of Zacharias, on which the odes of a canon are modelled.",
 ["hymn", "scripture"], ["canon-hymn", "psalter"]),

# ---------------------------------------------------------------- architecture
("altar-table", "Holy Table (Altar)", {"el": "Ἁγία Τράπεζα", "cu": "Престо́лъ"},
 "The table in the centre of the sanctuary on which the Liturgy is offered; it contains relics.",
 ["architecture"], ["sanctuary", "antimension"]),
("sanctuary", "Sanctuary (Altar)", {"el": "Ἱερόν, Βῆμα"},
 "The area behind the iconostasis containing the Holy Table, the table of oblation and the high place.",
 ["architecture"], ["altar-table", "iconostasis", "prothesis"]),
("iconostasis", "Iconostasis", {"el": "Εἰκονοστάσιον", "cu": "Иконоста́съ"},
 "The icon screen between the nave and the sanctuary, with the royal doors at its centre and a fixed order of icons.",
 ["architecture", "icon"], ["royal-doors", "sanctuary"]),
("royal-doors", "Royal Doors", {"el": "Ὡραία Πύλη", "cu": "Ца́рскія врата́"},
 "The central doors of the iconostasis, through which only the clergy pass and through which the Gifts are brought.",
 ["architecture"], ["iconostasis", "great-entrance"]),
("solea", "Solea", {"el": "Σολέα"},
 "The raised walkway before the iconostasis, from which the faithful commune.",
 ["architecture"], ["ambo", "iconostasis"]),
("ambo", "Ambo", {"el": "Ἄμβων"},
 "The projection of the solea before the royal doors, from which the Gospel is read and the prayer behind the ambo is said.",
 ["architecture"], ["solea"]),
("narthex", "Narthex", {"el": "Νάρθηξ", "cu": "Притво́ръ"},
 "The entrance hall of the church, where catechumens and penitents formerly stood and where several offices begin.",
 ["architecture"], ["nave"]),
("nave", "Nave", {"el": "Ναός"},
 "The body of the church where the faithful stand.",
 ["architecture"], ["narthex", "sanctuary"]),
("analogion", "Analogion", {"el": "Ἀναλόγιον"},
 "The sloped stand holding an icon or a service book.",
 ["architecture", "icon"], ["iconostasis"]),
("antimension", "Antimension", {"el": "Ἀντιμήνσιον"},
 "The cloth signed by the bishop, containing relics, spread on the Holy Table. Without it the Liturgy may not be served: it is the bishop's warrant for the altar.",
 ["vessel", "eucharist"], ["altar-table", "bishop"]),

# ---------------------------------------------------------------- vestments
("sticharion", "Sticharion", {"el": "Στιχάριον"},
 "The long tunic worn by all ranks of clergy, and by readers and servers.",
 ["vestment"], ["orarion", "epitrachelion"]),
("orarion", "Orarion", {"el": "Ὠράριον"},
 "The long narrow band worn over the deacon's left shoulder, lifted at the litanies.",
 ["vestment"], ["deacon", "sticharion"]),
("epitrachelion", "Epitrachelion", {"el": "Ἐπιτραχήλιον", "cu": "Епитрахи́ль"},
 "The priest's stole, worn about the neck. No priestly service may be performed without it.",
 ["vestment"], ["priest", "phelonion"]),
("phelonion", "Phelonion", {"el": "Φαιλόνιον", "cu": "Фело́нь"},
 "The wide sleeveless outer vestment of a priest at the Liturgy.",
 ["vestment"], ["priest", "epitrachelion"]),
("sakkos", "Sakkos", {"el": "Σάκκος"},
 "The bishop's outer vestment, which replaced the phelonion for hierarchs.",
 ["vestment"], ["bishop", "omophorion"]),
("omophorion", "Omophorion", {"el": "Ὠμοφόριον"},
 "The broad band worn over the bishop's shoulders, signifying the lost sheep carried by the Good Shepherd. It marks his office.",
 ["vestment"], ["bishop", "sakkos"]),
("epigonation", "Epigonation", {"el": "Ἐπιγονάτιον"},
 "The stiff diamond-shaped cloth hung at the right knee, given as an award; it signifies the sword of the Spirit.",
 ["vestment"], ["priest", "bishop"]),
("epimanikia", "Epimanikia", {"el": "Ἐπιμανίκια"},
 "The cuffs worn by clergy, binding the sleeves and signifying the bonds of Christ.",
 ["vestment"], ["sticharion"]),
("zone", "Zone", {"el": "Ζώνη"},
 "The belt worn by a priest or bishop over the sticharion and epitrachelion.",
 ["vestment"], ["priest"]),
("nabedrennik", "Nabedrennik", {"cu": "Набе́дренникъ"},
 "A rectangular cloth worn at the hip, an award of the Slavic churches with no Greek counterpart.",
 ["vestment"], ["epigonation"]),
("mandyas", "Mandyas", {"el": "Μανδύας"},
 "The full cape worn by a bishop in procession, and in simpler form by monastics of the great schema.",
 ["vestment", "monastic"], ["bishop", "great-schema"]),
("klobuk", "Klobuk", {"cu": "Клобу́къ", "el": "Καλυμμαύχιον"},
 "The monastic head covering: a cylindrical cap with a veil.",
 ["vestment", "monastic"], ["monk", "great-schema"]),
("panagia", "Panagia", {"el": "Παναγία"},
 "The medallion icon of the Theotokos worn on the breast by a bishop.",
 ["vestment", "theotokos"], ["bishop"]),

# ---------------------------------------------------------------- orders
("bishop", "Bishop", {"el": "Ἐπίσκοπος", "cu": "Епи́скопъ"},
 "The highest of the three major orders, holding the fullness of the priesthood, ordaining clergy and serving as the centre of unity for his diocese.",
 ["order", "clergy"], ["priest", "deacon", "metropolitan"]),
("priest", "Priest (Presbyter)", {"el": "Πρεσβύτερος, Ἱερεύς", "cu": "Свяще́нникъ"},
 "The second order, ordained by a bishop to serve the Liturgy and the mysteries in a parish.",
 ["order", "clergy"], ["bishop", "deacon", "archpriest"]),
("deacon", "Deacon", {"el": "Διάκονος", "cu": "Діа́конъ"},
 "The third order, who serves at the altar, leads the litanies, and may not celebrate the mysteries alone.",
 ["order", "clergy"], ["priest", "orarion"]),
("subdeacon", "Subdeacon", {"el": "Ὑποδιάκονος"},
 "A minor order who attends the bishop and cares for the vessels.",
 ["order", "clergy"], ["deacon", "reader"]),
("reader", "Reader", {"el": "Ἀναγνώστης", "cu": "Чте́цъ"},
 "A minor order set apart to read the Epistle and the appointed texts.",
 ["order", "clergy"], ["subdeacon"]),
("patriarch", "Patriarch", {"el": "Πατριάρχης"},
 "The primate of an autocephalous church of patriarchal rank.",
 ["order", "clergy"], ["bishop", "autocephaly", "metropolitan"]),
("metropolitan", "Metropolitan", {"el": "Μητροπολίτης"},
 "A bishop of a principal city, ranking above the bishops of his province. Usage differs between the Greek and Slavic churches.",
 ["order", "clergy"], ["bishop", "archbishop"]),
("archbishop", "Archbishop", {"el": "Ἀρχιεπίσκοπος"},
 "A senior bishop. In Greek practice it commonly ranks above a metropolitan, in Slavic practice below.",
 ["order", "clergy"], ["bishop", "metropolitan"]),
("archimandrite", "Archimandrite", {"el": "Ἀρχιμανδρίτης"},
 "A senior monastic priest, often the head of a monastery or a candidate for the episcopate.",
 ["order", "monastic"], ["hieromonk", "abbot"]),
("hieromonk", "Hieromonk", {"el": "Ἱερομόναχος"},
 "A monk ordained to the priesthood.",
 ["order", "monastic"], ["monk", "priest", "hierodeacon"]),
("hierodeacon", "Hierodeacon", {"el": "Ἱεροδιάκονος"},
 "A monk ordained to the diaconate.",
 ["order", "monastic"], ["deacon", "hieromonk"]),
("archpriest", "Archpriest", {"el": "Πρωτοπρεσβύτερος", "cu": "Протоіере́й"},
 "A senior parish priest, an award of rank rather than a distinct order.",
 ["order", "clergy"], ["priest"]),
("abbot", "Abbot (Igumen)", {"el": "Ἡγούμενος", "cu": "Игу́менъ"},
 "The head of a monastery.",
 ["order", "monastic"], ["archimandrite", "monk"]),
("monk", "Monk", {"el": "Μοναχός", "cu": "Мона́хъ"},
 "One tonsured to the monastic life, under vows of obedience, chastity and poverty.",
 ["monastic"], ["novice", "rassophore", "great-schema"]),
("novice", "Novice", {"el": "Δόκιμος", "cu": "Послу́шникъ"},
 "One living in a monastery in trial before tonsure.",
 ["monastic"], ["monk", "rassophore"]),
("rassophore", "Rassophore", {"el": "Ῥασοφόρος"},
 "The first degree of monastic tonsure, the 'robe-bearer', without the full vows.",
 ["monastic"], ["monk", "stavrophore"]),
("stavrophore", "Stavrophore (Little Schema)", {"el": "Σταυροφόρος"},
 "The second degree of monastic tonsure, the 'cross-bearer', at which the full vows are taken.",
 ["monastic"], ["rassophore", "great-schema"]),
("great-schema", "Great Schema", {"el": "Μεγαλόσχημος"},
 "The highest degree of monastic tonsure, with the analavos and a rule of intensified prayer and withdrawal.",
 ["monastic"], ["stavrophore", "analavos"]),
("analavos", "Analavos", {"el": "Ἀνάλαβος"},
 "The vestment of the great schema, embroidered with the Cross, the lance, the sponge and the words of the Passion.",
 ["monastic", "vestment"], ["great-schema"]),
("elder", "Elder (Starets, Geron)", {"el": "Γέρων", "cu": "Ста́рецъ"},
 "A monastic of discernment to whom others disclose their thoughts and from whom they receive direction.",
 ["monastic", "ascetic"], ["spiritual-father", "obedience"]),
("spiritual-father", "Spiritual Father", {"el": "Πνευματικός"},
 "The priest or elder who hears confession and guides a person's life in Christ.",
 ["ascetic", "confession"], ["elder", "confession", "obedience"]),

# ---------------------------------------------------------------- ascetic
("hesychasm", "Hesychasm", {"el": "Ἡσυχασμός"},
 "The tradition of inner stillness and unceasing prayer, defended by St Gregory Palamas and affirmed by the councils of the fourteenth century.",
 ["ascetic", "prayer"], ["jesus-prayer", "nepsis", "essence-energies"]),
("jesus-prayer", "Jesus Prayer", {"el": "Εὐχὴ τοῦ Ἰησοῦ"},
 "'Lord Jesus Christ, Son of God, have mercy on me, a sinner', repeated as the ground of unceasing prayer.",
 ["ascetic", "prayer"], ["hesychasm", "prayer-of-heart", "prayer-rope"]),
("prayer-of-heart", "Prayer of the Heart", {"el": "Καρδιακὴ προσευχή"},
 "The Jesus Prayer descended from the mind into the heart and become continual.",
 ["ascetic", "prayer"], ["jesus-prayer", "hesychasm", "nepsis"]),
("nepsis", "Nepsis", {"el": "Νῆψις"},
 "Watchfulness: sober attention to the thoughts as they arise, so that they are met before they take root.",
 ["ascetic"], ["logismoi", "hesychasm", "prosoche"]),
("prosoche", "Prosoche", {"el": "Προσοχή"},
 "Attention; the guarding of the mind in prayer.",
 ["ascetic", "prayer"], ["nepsis"]),
("logismoi", "Logismoi", {"el": "Λογισμοί"},
 "The thoughts or suggestions that assail the mind, to be discerned and rejected before they become assent.",
 ["ascetic"], ["nepsis", "passions"]),
("passions", "Passions", {"el": "Πάθη", "cu": "Стра́сти"},
 "The disordered movements of the soul, not the natural desires themselves but their corruption into slavery.",
 ["ascetic"], ["logismoi", "apatheia", "dispassion"]),
("apatheia", "Apatheia", {"el": "Ἀπάθεια"},
 "Dispassion: not insensibility, but the healing of the passions so that the soul's powers move rightly toward God.",
 ["ascetic"], ["passions", "theosis"]),
("dispassion", "Dispassion", {},
 "The English rendering of apatheia; see that entry.",
 ["ascetic"], ["apatheia"]),
("penthos", "Penthos", {"el": "Πένθος"},
 "Mourning for sin, the godly sorrow that works repentance, often joined with tears.",
 ["ascetic", "repentance"], ["compunction", "metanoia"]),
("compunction", "Compunction (Katanyxis)", {"el": "Κατάνυξις"},
 "The piercing of the heart that brings tears and softens it toward God.",
 ["ascetic", "repentance"], ["penthos", "metanoia"]),
("metanoia", "Metanoia", {"el": "Μετάνοια"},
 "Repentance: literally a change of mind, the turning of the whole person toward God. The same word names the prostration.",
 ["ascetic", "repentance"], ["prostration", "confession", "penthos"]),
("prostration", "Prostration", {"el": "Μετάνοια", "cu": "Земно́й покло́нъ"},
 "The bow to the ground made in penitence and worship. Prostrations are not made on Sundays or in the Paschal season.",
 ["ascetic", "prayer"], ["metanoia", "great-lent"]),
("obedience", "Obedience", {"el": "Ὑπακοή", "cu": "Послуша́ніе"},
 "The cutting off of one's own will before an elder or a rule; also the particular task assigned to a monastic.",
 ["ascetic", "monastic"], ["elder", "monk"]),
("prayer-rope", "Prayer Rope", {"el": "Κομποσχοίνι", "cu": "Чётки"},
 "The knotted woollen cord used to count the Jesus Prayer, commonly of thirty-three, fifty or a hundred knots.",
 ["ascetic", "prayer"], ["jesus-prayer"]),
("theosis", "Theosis", {"el": "Θέωσις"},
 "Deification: the participation of the human person in the divine life by grace, the end for which humanity was made. By grace and not by nature.",
 ["theology", "ascetic"], ["essence-energies", "apatheia"]),
("essence-energies", "Essence and Energies", {"el": "Οὐσία καὶ Ἐνέργειαι"},
 "The distinction, articulated by St Gregory Palamas, between God's unknowable essence and His uncreated energies, by which He is truly participated.",
 ["theology"], ["theosis", "hesychasm"]),
("kenosis", "Kenosis", {"el": "Κένωσις"},
 "The self-emptying of the Son in the Incarnation, spoken of in Philippians 2.",
 ["theology"], ["incarnation", "theosis"]),
("incarnation", "Incarnation", {"el": "Ἐνσάρκωσις"},
 "The taking of human nature by the eternal Word, true God and true man in one person.",
 ["theology"], ["kenosis", "theotokos", "hypostasis"]),
("hypostasis", "Hypostasis", {"el": "Ὑπόστασις"},
 "Person, as distinct from nature or essence. The Trinity is three hypostases in one essence; Christ is one hypostasis in two natures.",
 ["theology"], ["incarnation", "theotokos"]),
("theotokos", "Theotokos", {"el": "Θεοτόκος", "cu": "Богоро́дица"},
 "'Birth-giver of God', the title of the Virgin Mary affirmed at Ephesus in 431. It guards the truth that the one born of her is God.",
 ["theology", "theotokos"], ["incarnation", "hypostasis", "ecumenical-council"]),
("economia", "Economia", {"el": "Οἰκονομία"},
 "The pastoral discretion by which the strict application of a canon is relaxed for the salvation of souls; the counterpart of akriveia.",
 ["canon-law", "pastoral"], ["akriveia", "canon-law"]),
("akriveia", "Akriveia", {"el": "Ἀκρίβεια"},
 "Exactness: the strict application of the canons, the counterpart of economia.",
 ["canon-law", "pastoral"], ["economia"]),
("phronema", "Phronema", {"el": "Φρόνημα"},
 "The mind or mindset of the Church, formed by living within her rather than by study alone.",
 ["theology", "ascetic"], ["catholicity"]),
("catholicity", "Catholicity", {"el": "Καθολικότης"},
 "The wholeness of the Church: not extent but fullness, each local church gathered around its bishop possessing the whole. The phrase 'according to the whole' renders kath' holon.",
 ["theology"], ["phronema", "ecumenical-council"]),

# ---------------------------------------------------------------- calendar & fast
("pascha", "Pascha", {"el": "Πάσχα", "cu": "Па́сха"},
 "The Resurrection of Christ, the feast of feasts, from which the movable cycle is reckoned.",
 ["calendar", "feast"], ["paschalion", "pentecostarion", "great-lent"]),
("paschalion", "Paschalion", {"el": "Πασχάλιον"},
 "The reckoning of the date of Pascha, and the table by which it is found.",
 ["calendar"], ["pascha", "julian-calendar"]),
("julian-calendar", "Julian and Revised Julian Calendars", {},
 "The older Julian calendar, kept by several churches for the whole year, and the Revised Julian, which follows the Gregorian for fixed feasts while keeping the Julian Paschalion.",
 ["calendar"], ["paschalion", "menaion"]),
("great-lent", "Great Lent", {"el": "Μεγάλη Τεσσαρακοστή", "cu": "Вели́кій по́стъ"},
 "The forty-day fast before Holy Week and Pascha, beginning on Clean Monday.",
 ["calendar", "fast", "lent"], ["triodion", "presanctified", "clean-monday"]),
("clean-monday", "Clean Monday", {"el": "Καθαρὰ Δευτέρα"},
 "The first day of Great Lent, following Forgiveness Sunday.",
 ["calendar", "fast", "lent"], ["great-lent", "forgiveness-vespers"]),
("forgiveness-vespers", "Forgiveness Vespers", {},
 "The vespers on the evening before Great Lent begins, at which the faithful ask forgiveness of one another.",
 ["service", "lent"], ["clean-monday", "great-lent"]),
("holy-week", "Holy Week", {"el": "Μεγάλη Ἑβδομάς", "cu": "Страстна́я седми́ца"},
 "The week from Palm Sunday to Holy Saturday, following Great Lent and preceding Pascha.",
 ["calendar", "lent"], ["pascha", "great-lent"]),
("apostles-fast", "Apostles' Fast", {"cu": "Петро́въ по́стъ"},
 "The fast from the Monday after All Saints to the feast of Saints Peter and Paul on 29 June. Its length varies with the date of Pascha.",
 ["calendar", "fast"], ["dormition-fast", "nativity-fast"]),
("dormition-fast", "Dormition Fast", {},
 "The fast of 1 to 14 August, before the Dormition of the Theotokos.",
 ["calendar", "fast"], ["apostles-fast", "nativity-fast"]),
("nativity-fast", "Nativity Fast", {"cu": "Рожде́ственскій по́стъ"},
 "The forty-day fast from 15 November before the Nativity of Christ.",
 ["calendar", "fast"], ["dormition-fast", "apostles-fast"]),
("xerophagy", "Xerophagy", {"el": "Ξηροφαγία"},
 "Dry eating: the strictest ordinary degree of fasting, without oil or wine, kept on the weekdays of Great Lent.",
 ["fast"], ["great-lent"]),
("fast-free", "Fast-free Week", {"el": "Ἑβδομὰς κατάλυσις"},
 "A week in which the Wednesday and Friday fast is lifted, such as Bright Week and the week after Pentecost.",
 ["fast", "calendar"], ["bright-week"]),
("bright-week", "Bright Week", {"el": "Διακαινήσιμος"},
 "The week following Pascha, kept as one continuous day of the feast, fast-free and with the royal doors open.",
 ["calendar", "feast"], ["pascha", "fast-free"]),
("great-feasts", "Great Feasts", {},
 "The twelve major feasts of the year together with Pascha, which stands above them as the feast of feasts.",
 ["calendar", "feast"], ["pascha", "forefeast"]),
("forefeast", "Forefeast and Afterfeast", {"el": "Προεόρτια, Μεθέορτα"},
 "The days of preparation before a great feast and of continuation after it.",
 ["calendar", "feast"], ["leavetaking", "great-feasts"]),
("leavetaking", "Leavetaking (Apodosis)", {"el": "Ἀπόδοσις"},
 "The final day of a feast's afterfeast, kept with much of the feast's own hymnody.",
 ["calendar", "feast"], ["forefeast"]),
("soul-saturday", "Soul Saturday", {"el": "Ψυχοσάββατον"},
 "The Saturdays appointed for the commemoration of all the departed.",
 ["calendar", "departed"], ["panikhida", "koliva"]),
("koliva", "Koliva", {"el": "Κόλλυβα"},
 "Boiled wheat with honey and fruit, blessed at memorials, taken from the Lord's words that the grain must die to bear fruit.",
 ["departed", "food"], ["panikhida", "soul-saturday"]),
("indiction", "Indiction", {"el": "Ἰνδικτιών"},
 "The beginning of the church year on 1 September.",
 ["calendar"], ["menaion"]),

# ---------------------------------------------------------------- mysteries
("mystery", "Mystery (Sacrament)", {"el": "Μυστήριον", "cu": "Та́инство"},
 "An action of the Church in which grace is given through visible means. The Orthodox Church has never fixed their number by dogma, though seven are commonly listed.",
 ["mystery"], ["baptism", "chrismation", "confession", "unction"]),
("baptism", "Baptism", {"el": "Βάπτισμα", "cu": "Креще́ніе"},
 "Threefold immersion into the death and resurrection of Christ, by which one enters the Church.",
 ["mystery"], ["chrismation", "catechumen"]),
("chrismation", "Chrismation", {"el": "Χρῖσμα", "cu": "Мѵропома́заніе"},
 "Anointing with holy myron immediately after baptism, the seal of the gift of the Holy Spirit.",
 ["mystery"], ["baptism", "myron"]),
("myron", "Holy Myron (Chrism)", {"el": "Ἅγιον Μύρον"},
 "The fragrant oil consecrated by a patriarch or synod and used at chrismation.",
 ["mystery"], ["chrismation"]),
("confession", "Confession", {"el": "Ἐξομολόγησις", "cu": "И́споведь"},
 "The mystery of repentance, in which sins are confessed before God in the presence of a priest and absolution is given. Its frequency differs markedly between traditions.",
 ["mystery", "repentance"], ["metanoia", "spiritual-father", "epitimia"]),
("epitimia", "Epitimia (Penance)", {"el": "Ἐπιτίμιον"},
 "A rule given at confession as medicine rather than punishment, such as prostrations, almsgiving, or abstention from communion for a time.",
 ["mystery", "repentance", "pastoral"], ["confession", "economia"]),
("unction", "Holy Unction", {"el": "Εὐχέλαιον", "cu": "Собо́рованіе"},
 "The anointing of the sick with blessed oil for the healing of soul and body, served by several priests where possible.",
 ["mystery"], ["mystery"]),
("catechumen", "Catechumen", {"el": "Κατηχούμενος", "cu": "Оглаше́нный"},
 "One being instructed in the faith in preparation for baptism, dismissed before the Liturgy of the Faithful in the older practice.",
 ["mystery"], ["baptism"]),
("churching", "Churching", {"el": "Σαράντισμα"},
 "The bringing of mother and infant to the church on the fortieth day, with prayers of thanksgiving and blessing.",
 ["mystery", "pastoral"], ["baptism"]),
("crowning", "Crowning (Marriage)", {"el": "Στεφάνωμα", "cu": "Вѣнча́ніе"},
 "The mystery of marriage, so called from the crowns set on the heads of the couple, signifying both royalty and martyrdom.",
 ["mystery"], ["mystery"]),

# ---------------------------------------------------------------- misc
("great-entrance", "Great Entrance", {"el": "Μεγάλη Εἴσοδος"},
 "The procession bringing the prepared gifts from the table of oblation to the Holy Table, during the Cherubic Hymn.",
 ["eucharist", "service"], ["cherubic-hymn", "prothesis", "royal-doors"]),
("little-entrance", "Little Entrance", {"el": "Μικρὰ Εἴσοδος"},
 "The procession with the Gospel book near the beginning of the Liturgy.",
 ["eucharist", "service"], ["great-entrance"]),
("ecumenical-council", "Ecumenical Council", {"el": "Οἰκουμενικὴ Σύνοδος"},
 "A council whose definitions the whole Church has received. The Orthodox Church holds seven, from Nicaea in 325 to Nicaea II in 787.",
 ["council", "canon-law"], ["canon-law", "rudder", "theotokos"]),
("canon-law", "Canon", {"el": "Κανών"},
 "A rule of the Church given by a council or a father and received by the whole body. Distinct from the canon sung at Orthros.",
 ["canon-law"], ["ecumenical-council", "rudder", "economia"]),
("autocephaly", "Autocephaly", {"el": "Αὐτοκεφαλία"},
 "The status of a church that elects its own primate and is not subject to another, while remaining in communion with the rest.",
 ["church-order"], ["patriarch", "autonomy"]),
("autonomy", "Autonomy", {"el": "Αὐτονομία"},
 "The status of a church that governs itself but whose primate is confirmed by a mother church.",
 ["church-order"], ["autocephaly"]),
("diptychs", "Diptychs", {"el": "Δίπτυχα"},
 "The lists of the living and departed commemorated at the Liturgy, and among the primates the order of precedence and communion.",
 ["church-order", "eucharist"], ["autocephaly"]),
("phyletism", "Phyletism", {"el": "Φυλετισμός"},
 "The confusion of the Church with the nation, condemned as a heresy by the Council of Constantinople in 1872.",
 ["church-order", "heresy"], ["autocephaly", "catholicity"]),
("relics", "Relics", {"el": "Λείψανα", "cu": "Мо́щи"},
 "The bodily remains of the saints, honoured because the body is a temple of the Holy Spirit. Relics are sealed in the antimension and the altar.",
 ["saints"], ["antimension", "altar-table"]),
("incorrupt", "Incorruption", {"el": "Ἀφθαρσία"},
 "The preservation of a saint's body from decay, received as a sign of sanctity though not required for glorification.",
 ["saints"], ["relics", "glorification"]),
("glorification", "Glorification (Canonisation)", {"el": "Ἁγιοκατάταξις"},
 "The Church's recognition that a person is among the saints, formalising a veneration that has already arisen among the faithful.",
 ["saints"], ["relics", "incorrupt"]),
("toll-houses", "Aerial Toll-houses", {"el": "Τελώνια"},
 "An account of the soul's passage after death, in which it is examined by demons at successive stages. It is found in patristic, hagiographic and liturgical sources, and is taught by many of the saints.",
 ["eschatology", "departed"], ["departed-prayers", "panikhida"]),
("departed-prayers", "Prayer for the Departed", {},
 "The Church's practice of praying for those who have died, expressed in the panikhida, the Soul Saturdays, and the commemorations at the prothesis.",
 ["departed"], ["panikhida", "soul-saturday", "prothesis"]),
("iconography", "Icon", {"el": "Εἰκών", "cu": "Ико́на"},
 "A written image of Christ, the Theotokos or the saints, venerated as the honour passes to the prototype. Defended at the Seventh Ecumenical Council.",
 ["icon"], ["iconostasis", "ecumenical-council", "veneration"]),
("veneration", "Veneration and Worship", {"el": "Προσκύνησις, Λατρεία"},
 "The distinction affirmed at Nicaea II: worship (latreia) belongs to God alone, while veneration (proskynesis) is offered to icons, relics and the saints.",
 ["icon", "theology"], ["iconography", "ecumenical-council"]),
("censer", "Censer", {"el": "Θυμιατόν", "cu": "Кади́ло"},
 "The vessel in which incense is burned, hung with bells in the Slavic and most Greek use.",
 ["vessel"], ["incense"]),
("incense", "Incense", {"el": "Θυμίαμα"},
 "Burned at the services, signifying prayer rising before God.",
 ["vessel", "prayer"], ["censer"]),
("dikirion", "Dikirion and Trikirion", {"el": "Δικήριον, Τρικήριον"},
 "The two- and three-branched candlesticks with which a bishop blesses, signifying the two natures of Christ and the three Persons of the Trinity.",
 ["vessel"], ["bishop"]),
("epitaphios", "Epitaphios", {"el": "Ἐπιτάφιος", "cu": "Плащани́ца"},
 "The embroidered cloth bearing the image of Christ laid in the tomb, carried in procession on Holy Friday.",
 ["vessel", "lent"], ["holy-week"]),
("theophany-water", "Great Blessing of Water", {"el": "Μέγας Ἁγιασμός"},
 "The blessing of water at Theophany, kept through the year and drunk at need.",
 ["service", "feast"], ["mystery"]),
]


def main():
    ids = [t[0] for t in T]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        print("ERROR: duplicate ids: %s" % ", ".join(sorted(dup)))
        return 1

    known = set(ids)
    entries = []
    tags = {}
    for tid, head, forms, definition, tg, see in T:
        bad = [s for s in see if s not in known]
        if bad:
            print("ERROR: %s points at unknown term(s): %s" % (tid, ", ".join(bad)))
            return 1
        if not re.match(r"^[a-z0-9-]+$", tid):
            print("ERROR: bad id %r" % tid)
            return 1
        for x in tg:
            tags[x] = tags.get(x, 0) + 1
        entries.append({"id": tid, "t": head, "forms": forms,
                        "d": definition, "tags": tg, "see": see})

    entries.sort(key=lambda e: e["t"].lower())

    # The headwords and definitions are the bulk of the page, so each language
    # is written to its own file and fetched only when it is the one in front
    # of the reader. The chrome is small enough to travel with the base.
    by_lang = load_terms()
    ready = []
    for lang in I18N.LANGS:
        if lang == "en":
            continue
        t = by_lang.get(lang) or {}
        missing = [e["id"] for e in entries if e["id"] not in t]
        if not t:
            continue
        if missing:
            print("  %-4s incomplete: %d of %d terms; not published"
                  % (lang, len(entries) - len(missing), len(entries)))
            continue
        stray = [k for k in t if k not in known]
        if stray:
            print("ERROR: %s translates unknown term(s): %s"
                  % (lang, ", ".join(sorted(stray)[:5])))
            return 1
        f = ROOT / "data" / ("glossary-i18n.v1.%s.json" % lang)
        f.write_text(json.dumps({k: list(v) for k, v in t.items()},
                                ensure_ascii=False, separators=(",", ":")),
                     encoding="utf-8")
        ready.append(lang)
        print("  %-4s %3d terms  (%.0f KB)" % (lang, len(t), f.stat().st_size / 1024))

    payload = {
        "v": 2,
        "langs": I18N.LANGS,
        "ready": ready,               # languages whose entries are published
        "ui": I18N.UI,
        "lgNames": I18N.LGNAMES,
        "tagNames": I18N.TAGS,
        "tags": sorted(tags, key=lambda k: (-tags[k], k)),
        "terms": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")
    print("wrote %s" % OUT.relative_to(ROOT))
    print("  terms  %4d" % len(entries))
    print("  tags   %4d  (%s)" % (len(tags), ", ".join(payload["tags"][:10])))
    print("  with source-language forms: %d" % sum(1 for e in entries if e["forms"]))
    print("  size   %.0f KB" % (OUT.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
