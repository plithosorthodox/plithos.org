#!/usr/bin/env python3
"""Build the native Hapgood Service Book payload from the 1922 edition.

The prepared EPUB retains the printed page and block coordinates. This
ingester uses those coordinates to keep parallel texts in separate units
instead of flattening them into an unreadable scan order.

    python tools/ingest_hapgood_service_book.py --import-source
    python tools/ingest_hapgood_service_book.py --write
    python tools/ingest_hapgood_service_book.py --check
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
EPUB = ROOT / "tmp" / "hapgood-clean.epub"
IA_OCR = ROOT / "tmp" / "gtu_A32400004109975B_djvu.txt"
FIXTURE = ROOT / "tools" / "manuscripts" / "hapgood_service_book_1922.json"
OUT = ROOT / "data" / "library" / "service-book-hapgood-1906.json"
INDEX = ROOT / "data" / "library" / "works-index.json"

WORK_ID = "service-book-hapgood-1906"
PAYLOAD_VERSION = 2
EPUB_URL = (
    "https://www.agape-biblia.org/literatura/"
    "Service_Book_of_the_Holy_Orthodox_Catholic_Church.epub"
)
EPUB_SHA256 = "114df7851bd3f1358f09a71ce4a56dae9a22d55598dc984b1c098d3ba5ac00b0"
IA_OCR_URL = (
    "https://archive.org/download/gtu_A32400004109975B/"
    "gtu_A32400004109975B_djvu.txt"
)
IA_OCR_SHA1 = "5701e96fa38f2b41a62d834ee8cd8f1870d92b71"
FIXTURE_SHA256 = "815cbdf813220446d2e62ea8c082c63a1e628ebb941686ecc120c0013dc78d8e"


# The prepared EPUB solves the scan's column-order problems, but its text
# still carries a finite set of ordinary OCR errors. Each correction below
# was checked against the exact 1922 Internet Archive OCR, the independent
# prepared transcription, or the page image when the text witnesses differ.
# The expected occurrence count makes source drift or an over-broad repair
# fail loudly.
VERIFIED_OCR_CORRECTIONS = [
    # Psalm CIV, checked against the page image and both text witnesses.
    ("psalm-works-spacing", "works:In", "works: In", 1),
    ("psalm-they-get", "theyget", "they get", 1),
    ("psalm-sea-spacing", "thegreatandwidesea", "the great and wide sea", 1),
    ("psalm-ships", "There go the Father", "There go the ships", 1),
    ("rubric-followeth", "as followed:", "as followeth:", 1),

    # Fused words verified in the second text witness.
    ("and-profitable", "andprofitable", "and profitable", 2),
    ("with-the", "withthe", "with the", 1),
    ("compassion-of", "compassionof", "compassion of", 1),
    ("lord-god", "LordGod", "Lord God", 1),
    ("and-fifth", "andfifth", "and fifth", 1),
    ("and-approacheth", "andapproacheth", "and approacheth", 1),
    ("and-for", "andfor", "and for", 4),
    ("the-following", "thefollowing", "the following", 1),
    ("xc-from", "XCfrom", "XC from", 1),
    ("to-call", "tocall", "to call", 1),
    ("present-with", "presentwith", "present with", 1),
    ("and-placeth", "andplaceth", "and placeth", 2),
    ("presanctified-lamb", "PresanctifiedLamb", "Presanctified Lamb", 1),
    ("and-putteth", "andputteth", "and putteth", 1),
    ("my-heart", "my'heart", "my heart", 1),
    ("the-assaults", "theassaults", "the assaults", 1),
    ("showed-upon", "showedupon", "showed upon", 1),
    ("of-thine", "ofthine", "of thine", 2),
    ("and-the", "andthe", "and the", 1),
    ("substituted-for", "substitutedfor", "substituted for", 1),
    ("keep-us", "keepus", "keep us", 1),
    ("also-in", "alsoin", "also in", 1),
    ("supper-he", "supperhe", "supper he", 1),
    ("impotency-and", "impotencyand", "impotency and", 1),
    ("see-above", "Seeabove", "See above", 1),
    ("they-beheld", "theybeheld", "they beheld", 1),
    ("the-mother", "theMother", "the Mother", 1),
    ("maketh-with", "makethwith", "maketh with", 1),
    ("about-and", "aboutand", "about and", 1),
    ("holy-chrismation", "HOLYCHRISMATION", "HOLY CHRISMATION", 1),
    ("the-person", "theperson", "the person", 1),
    ("the-feet", "thefeet", "the feet", 1),
    ("the-servant", "theservant ", "the servant ", 1),
    ("shall-inquire", "shallinquire", "shall inquire", 1),
    ("the-servants", "theservants", "the servants", 1),
    ("his-palms", "hispalms", "his palms", 1),
    ("and-girdeth", "andgirdeth", "and girdeth", 1),
    ("most-holy", "MostHoly", "Most Holy", 1),
    ("and-with", "andwith", "and with", 1),
    ("stand-before", "standbefore", "stand before", 1),
    ("mercy-at", "mercyat", "mercy at", 1),
    ("how-there", "howthere", "how there", 1),
    ("faith-hath", "faithhath", "faith hath", 1),
    ("savest-those", "savestthose", "savest those", 1),
    ("the-following-apostrophe", "the'following", "the following", 1),
    ("freed-from", "freedfrom", "freed from", 1),
    ("prayed-for", "prayedfor", "prayed for", 2),
    ("and-when", "Andwhen", "And when", 1),
    ("they-have", "theyhave", "they have", 1),
    ("who-have", "whohave", "who have", 1),
    ("name-of", "Nameof", "Name of", 1),
    ("and-feet", "andfeet", "and feet", 1),
    ("cosmas-and", "Cosmasand", "Cosmas and", 1),
    ("he-goeth", "hegoeth", "he goeth", 1),
    ("and-poureth", "andpoureth", "and poureth", 2),
    ("and-from", "andfrom", "and from", 2),
    ("that-henceforth", "thathenceforth", "that henceforth", 1),
    ("of-foes", "offoes", "of foes", 1),
    ("thou-shalt", "thoushalt", "thou shalt", 1),
    ("for-the", "forthe", "for the", 1),
    ("mercy-upon", "mercyupon", "mercy upon", 1),
    ("are-here", "arehere", "are here", 1),
    ("polluted-lips", "pollutedlips", "polluted lips", 1),
    ("saints-who", "saintswho", "saints who", 1),
    ("have-filled", "havefilled", "have filled", 1),
    ("exultingly-to", "exultinglyto", "exultingly to", 1),
    ("the-shunammite", "theShunammite", "the Shunammite", 1),

    # Letter substitutions and damaged transliterations.
    ("valuable", "vatuable", "valuable", 1),
    ("letters", "tetters", "letters", 1),
    ("oecumenical", "CEcumenical", "Œcumenical", 4),
    ("us-the", "usthe", "us the", 1),
    ("holy", "hbly", "holy", 1),
    ("epitrakhil", "epitraklul", "epitrakhil", 1),
    ("litany", "The Great Litan ", "The Great Litany ", 1),
    ("entereth", "enterelh", "entereth", 1),
    ("they", "thev", "they", 1),
    ("shall-shill", "shill", "shall", 1),
    ("shall-shell", "shell", "shall", 1),
    ("taketh-l", "takelh", "taketh", 1),
    ("spears", "spearsj^by", "spears, by", 1),
    ("celebrateth", "celbrateth", "celebrateth", 1),
    ("bishop", "Btsiop", "Bishop", 1),
    ("bishop-h", "Bithop", "Bishop", 1),
    ("taketh-c", "takcth", "taketh", 1),
    ("that", " chat would", " that would", 1),
    ("after", "Ajter", "After", 1),
    ("approacheth", "approarheth", "approacheth", 1),
    ("prokimen-i", "Prokimeri", "Prokimen", 1),
    ("beareth", "bearelh", "beareth", 1),
    ("prokimen-m", "ProMmen", "Prokimen", 1),
    ("nationalities", "nationalties", "nationalities", 1),
    ("grapes", "Crapes", "Grapes", 1),
    ("herself", "hersetf", "herself", 1),
    ("being", "Bdng", "Being", 1),
    ("thrice", "thrive", "thrice", 1),
    ("page", "paige", "page", 1),
    ("standeth", "stiindeth", "standeth", 1),
    ("archpriest", "Archfiriest", "Archpriest", 1),
    ("with-i", "wiih", "with", 1),
    ("with-m", "imth", "with", 1),
    ("lieth", "licth", "lieth", 1),
    ("all", " nall the Righteous", " all the Righteous", 1),
    ("while", "vhile", "while", 1),
    ("hypocrisy", "hyprocrisy", "hypocrisy", 1),
    ("reconciliation", "reconcilation", "reconciliation", 1),
    ("effectual", "effctual", "effectual", 1),
    ("giveth", "givcth", "giveth", 1),
    ("tranquillity", "tranquility", "tranquillity", 1),
    ("proclaimeth", "proclaimelh", "proclaimeth", 1),
    ("choir", "Cnoir", "Choir", 1),
    ("willest", "wiliest", "willest", 1),
    ("remaining", "remaing", "remaining", 1),
    ("upon", "upcn", "upon", 1),
    ("conflict", "confliet", "conflict", 1),
    ("kutiya", "kutiyd", "kutiya", 1),
    ("stikhira", "StikMra", "Stikhira", 2),
    ("psalm-cxxxii", "exxxii", "cxxxii", 1),
    ("cosmas", "Cosmos", "Cosmas", 3),

    # Misread digits, page numbers, and footnote markers.
    ("year-1906", "I906", "1906", 1),
    ("year-1894", "1S94", "1894", 1),
    ("exodus-18", "Exodus xxv. i8-20", "Exodus xxv. 18-20", 1),
    ("felon", "fel6n", "felón", 1),
    ("rostov", "Rost6ff", "Rostóff", 1),
    ("radonezh", "Rad6nezh", "Radónezh", 1),
    ("vine-leading-five", "5and behold", "and behold", 1),
    ("footnote-15", "(i5)", "(15)", 2),
    ("footnote-16", "(i6)", "(16)", 2),
    ("isolated-4r", "4r", "", 1),
    ("unclean-spirits", "un- 2clean spirits", "unclean spirits", 1),
    ("from-the-dead", "from the U4e- dead", "from the dead", 1),
    ("page-163", "163For those", "For those", 1),
    ("all-night", "A11-Night", "All-Night", 1),
    ("prov-11-18", "Prov. iii. ii-i8", "Prov. iii. 11-18", 1),
    ("exodus-40", "Exodus xl. i-5", "Exodus xl. 1-5", 1),
    ("first-kings", "i Kings viii. i,", "1 Kings viii. 1,", 1),
    ("ezekiel-1-4", "xliv. i-4", "xliv. 1-4", 1),
    ("hebrews-1-3", "Heb. i.' 10-14, I_3The Gospel", "Heb. i. 10-14, ii. 1-3. The Gospel", 1),
    ("epiphany-readings", "Joshua iii. 7, 8, i5-i7; 2 Kings ii. 6-i4, v. 9-i4; Isaiah i. i6-20; Genesis xxxii. i-i0; Exodus ii. 5-i0; Judges vi. 36-40; i Kings xviii. 30-39; 2 Kings ii. i9-22; Isaiah xlix. 8-i5", "Joshua iii. 7, 8, 15-17; 2 Kings ii. 6-14, v. 9-14; Isaiah i. 16-20; Genesis xxxii. 1-10; Exodus ii. 5-10; Judges vi. 36-40; 1 Kings xviii. 30-39; 2 Kings ii. 19-22; Isaiah xlix. 8-15", 1),
    ("epiphany-epistle", "i Cor. ix. i9-27, x. i-4", "1 Cor. ix. 19-27, x. 1-4", 1),
    ("epiphany-gospel", "Luke iii. i-i8", "Luke iii. 1-18", 1),
    ("luke-20", "Luke xx. i-39", "Luke xx. 1-39", 1),
    ("jeremiah-reading", "Jer. xi. 18-23, x»- I_5, 9-!1", "Jer. xi. 18-23, xii. 1-5, 9-11", 1),
    ("job-reading", "Job xxxviii. i-22", "Job xxxviii. 1-22", 1),
    ("gospel-ten", "(Jo) Mark xv. 43-47", "(10) Mark xv. 43-47", 1),
    ("good-friday-jeremiah", "Jer. xii. 18-23, x'i- I_I5", "Jer. xii. 18-23, xii. 1-15", 1),
    ("exodus-11", "Exodus xxxiii. n-23", "Exodus xxxiii. 11-23", 1),
    ("isaiah-lii", "Isaiah Hi. 13-15", "Isaiah lii. 13-15", 2),
    ("isaiah-liv", "liv. I.", "liv. 1.", 1),
    ("ascension-readings", "lxii. i0-i2, lxiii. 1-3, 7-10; Zech. xiv. i, 4, 8-11", "lxii. 10-12, lxiii. 1-3, 7-10; Zech. xiv. 1, 4, 8-11", 1),
    ("verse-three", "Verse 3:My", "Verse 3: My", 1),
    ("john-20", "John xx. i9-23", "John xx. 19-23", 1),
    ("verse-two", "Verse2:", "Verse 2:", 1),
    ("luke-19", "Luke xix. 1-n", "Luke xix. 1-11", 1),
    ("first-corinthians", "(/ Cor. xii.", "(1 Cor. xii.", 1),
    ("matthew-ten", "Matt. x. i, 5-9", "Matt. x. 1, 5-9", 1),
    ("second-corinthians", "2 Cor. vi. 16-vii. I", "2 Cor. vi. 16-vii. 1", 1),
    ("matthew-eight", "Matt. viii. i4-24", "Matt. viii. 14-24", 1),
    ("galatians", "{Gal. v. 22-vi.", "(Gal. v. 22-vi.", 1),
    ("john-five", "John v.24-30", "John v. 24-30", 1),
    ("footnote-10", "(i0)", "(10)", 1),
    ("footnote-12", "(i2)", "(12)", 2),
    ("footnote-13", "(i3)", "(13)", 1),
    ("footnote-14", "(i4)", "(14)", 1),
    ("footnote-17", "(i7)", "(17)", 1),
    ("footnote-18", "(i8)", "(18)", 1),
    ("triodion", "Tri6dion", "Triódion", 1),
    ("romans-11", "Rom. xi. i7", "Rom. xi. 17", 1),
    ("consecration-page", "THE CONSECRATION7 OF A CHURCH", "THE CONSECRATION OF A CHURCH", 1),

    # Layout and marginal-note debris checked directly on the facsimile.
    ("trailing-caret", "Deacon. Amen. ^", "Deacon. Amen.", 1),
    ("prescribed-hymns", "prescribed §\" hymns", "prescribed hymns", 1),
    ("pontifical-washing", "Then the ewer and basin are brought by the Proto-Deacon and the Deacon, getting. and the Bishop washeth his hands, if there be no Setting-apart of a Reader apart of or Chanter, or the Ordination of a Sub-Deacon. But if there be a Setting- Jj£lin*apart or an Ordination, then he who is to be set Chanters;apart or ordained bringeth the ewer and basin, after he hath been vested in his dalmatic, in the man- uJj'Jf\"ner set forth in the Order for the Laying-on of Hands: and the Bishop Snbsaith, secretly:", "Then the ewer and basin are brought by the Proto-Deacon and the Deacon, and the Bishop washeth his hands, if there be no Setting-apart of a Reader or Chanter, or the Ordination of a Sub-Deacon. But if there be a Setting-apart or an Ordination, then he who is to be set apart or ordained bringeth the ewer and basin, after he hath been vested in his dalmatic, in the manner set forth in the Order for the Laying-on of Hands: and the Bishop saith, secretly: Setting-apart of Readers and Chanters; Ordination of Sub-Deacons.", 1),
    ("response-r-left", "laity: R«", "laity: ℟", 1),
    ("gospel-bullet", "Priest. Let us attend. •", "Priest. Let us attend.", 1),
    ("wisdom-bar", "Wisdom! |Then", "Wisdom! Then", 1),
    ("give-thanks", "giv£ thanks", "give thanks", 1),
    ("isolated-noise", "~5", "", 1),
    ("invisibly-caret", "here ^ invisibly", "here invisibly", 1),
    ("proto-deacon-bullet", "Proto•Deacon", "Proto-Deacon", 1),
    ("gladness-layout", "glad- | ^ness", "gladness", 1),
    ("basil-hymn-layout", "this Hymn 03 (Tropar), in Tone I.: ^", "this Hymn (Tropar), in Tone I.:", 1),
    ("unto-god-caret", "unto ^ God", "unto God", 1),
    ("communion-caret", "the ^ Communion", "the Communion", 1),
    ("beseech-layout", "be- ^ seech", "beseech", 1),
    ("double-tilde", "mankind. ~~", "mankind.", 1),
    ("response-r-caret", "unquiet: R^", "unquiet: ℟", 1),
    ("pentecost-layout", "make all things^through the cooperation .tftthe Holy Spirit", "make all things through the cooperation of the Holy Spirit", 1),
    ("ordination-creed-layout", "kingdom, ^ . . . Lord, have mercy. (Thrice.) I believe in one God, ... 4?", "kingdom, . . . Lord, have mercy. (Thrice.) I believe in one God, . . .", 1),
    ("knowledge-layout", "knowl- ^edge", "knowledge", 1),
    ("ritual-bullet", "Ritual. • See", "Ritual. See", 1),
    ("response-r-caret-two", "their hands: R^", "their hands: ℟", 1),
    ("servant-plural", "servant^)", "servant(s)", 4),
    ("oil-leading-bar", "| sanctify this Oil", "sanctify this Oil", 1),
    ("page-369-layout", ". . ^See P- 369->", ". . . See page 369.", 1),
    ("convinced-bullet", "convinced of them. •", "convinced of them.", 1),
    ("water-blessing-layout", "and bless all *P of us who by the bowing of our necks do show forth our apprehen- ^ sion that we are thy servants; and grant that we may be filled with v$\" thy sanctification", "and bless all of us who by the bowing of our necks do show forth our apprehension that we are thy servants; and grant that we may be filled with thy sanctification", 1),
    ("obedience-layout", "obedience unto § thee", "obedience unto thee", 1),
    ("consolation-layout", "hope in the ^ g.consolation of Christ", "hope in the consolation of Christ", 1),
    ("warriors-margin", "the Orthodox Warriors who have val- orthodox iantly contended", "the Orthodox Warriors who have valiantly contended", 1),
    ("glory-response-noise", "Lord of glory: † 'S nT", "Lord of glory: ℟", 1),
    ("sorrowing-margin", "hope in the 2. £consolation of Christ: †", "hope in the consolation of Christ: ℟", 1),
    ("make-glad-margin", "and appoint him (her, them) glad where the light of God's countenance shall visit him (her, them), ty 3- o", "and make him (her, them) glad where the light of God's countenance shall visit him (her, them): ℟", 1),
    ("establish-margin", "soul (their souls) ! % jj,in a place of brightness, a place of verdure, a place of rest, where * all the Righteous dwell: R> § o", "soul (their souls) in a place of brightness, a place of verdure, a place of rest, where all the Righteous dwell: ℟", 1),
    ("bosom-margin", "in the Q 3.bosom of Abraham", "in the bosom of Abraham", 1),
    ("warriors-page-440", "of the orthodox ever-to-be-commemorated Orthodox Warriors who have fallen warrior*. asleePi ancj 0f an those who have laid down their life", "of the ever-to-be-commemorated Orthodox Warriors who have fallen asleep, and of all those who have laid down their life", 1),

    # Residual word and reference errors found by the full-text audit. Each
    # reading is supported by the second OCR witness or the facsimile.
    ("chalice", "Chatice", "Chalice", 1),
    ("dalmatic", "Datmatic", "Dalmatic", 1),
    ("stole", "Stote", "Stole", 1),
    ("temple", "Tempte", "Temple", 1),
    ("with-refrain", "unth the Refrain", "with the Refrain", 1),
    ("choir-my-soul", "Clwir. My soul", "Choir. My soul", 1),
    ("orar", "stole (ordr)", "stole (orár)", 1),
    ("trikiri", "trikhi", "trikíri", 1),
    ("saith", "the Deacon satth:", "the Deacon saith:", 1),
    ("may-be", "maybe", "may be", 3),
    ("for-lo-lower", "forlo!", "for lo!", 1),
    ("for-lo-upper", "Forlo,", "For lo,", 1),
    ("stikhiri", "StikMri", "Stikhiri", 1),
    ("and-as", "Mary, andas a babe", "Mary, and as a babe", 1),
    ("priest", "The Pr'est beginnelh", "The Priest beginneth", 1),
    ("thee", "tJiee do we ascribe", "thee do we ascribe", 1),
    ("but-lo", "Butlo!", "But lo!", 1),
    ("panikhidi", "(panikhi'di)", "(panikhídi)", 1),
    ("church", "Churoh.", "Church.", 1),
    ("and-it", "Andit passeth", "And it passeth", 1),
    ("psalm-xciii", "Psal M Xciii. is read", "Psalm XCIII. is read", 1),
    ("me-to", "for meto hope", "for me to hope", 1),
    ("rising-do", "thy risingdo celebrate", "thy rising do celebrate", 1),
    ("up-for", "shut upfor three", "shut up for three", 1),
    ("before-us", "before usin the hope", "before us in the hope", 1),
    ("him-in", "himin outer darkness", "him in outer darkness", 1),
    ("non-avariciousness", "non-avari-ciousness", "non-avariciousness", 1),
    ("isaiah-reference", "Isaiah lxi. 10, n, Ixii. 1-5", "Isaiah lxi. 10, 11, lxii. 1-5", 1),
    ("are-contrite", "arc of a contrite heart", "are of a contrite heart", 1),
    ("people-by-oil", "peoplejjy oil", "people by oil", 1),
    ("senses", "sense?. Knit", "senses. Knit", 1),
    ("steadfast", "adtast will", "steadfast will", 1),
    ("tomb-even", "tombeven from", "tomb even from", 1),
    ("and-life-giving", "andlife-giving Mysteries", "and life-giving Mysteries", 1),
    ("promised-that", "promised,that", "promised, that", 1),
    ("sub-deacons", "Sub- Deacons", "Sub-Deacons", 1),
    ("trikiri-misread", "triktri", "trikíri", 3),
    ("tropari", "Tropart", "Tropari", 2),
    ("foreign-country", "beina foreign country", "be in a foreign country", 1),
    ("mark-reference", "(Ch. i. 9-ii.)", "(Ch. i. 9-11.)", 1),
    ("gladness-footnote", "gladness;(5)", "gladness; (5)", 1),
    ("first-john", "(i John i-3).", "(1 John i. 3).", 1),
    ("response-r-angle-left", "R<", "℟", 6),
    ("response-r-angle-right", "R>", "℟", 1),
    ("response-prisoners", "prisoners: If For", "prisoners: ℟ For", 1),
    ("response-departed", "brethren: If For", "brethren: ℟ For", 1),
    ("response-sailors", "sea: If For those who lie sick", "sea: ℟ For those who lie sick", 1),
    ("response-jordan", "blessing of Jordan: fy", "blessing of Jordan: ℟", 1),
    ("response-foreign-country", "foreign country), fy", "foreign country). ℟", 1),
    ("baptism-reference", "• Baptism.", "* Baptism.", 1),
    ("if-a-bishop", "// a Bishop", "If a Bishop", 3),

    # Second residual scan against the independently cleaned transcription.
    ("morning-watch", "w,atch", "watch", 1),
    ("apostles", "Apos- atles", "Apostles", 1),
    ("bogoroditchen-b", "Bogorbditchen", "Bogoróditchen", 1),
    ("bogoroditchen-d", "Bogorodichen", "Bogoróditchen", 1),
    ("bogoroditchen-t", "Bogoroitchen", "Bogoróditchen", 1),
    ("catholic", "Cath- cfolic", "Catholic", 1),
    ("entereth-c", "cntereth", "entereth", 1),
    ("epitrakhil-e", "Efitrakhil", "Epitrakhil", 1),
    ("exclaimeth-h", "exclaimelh", "exclaimeth", 1),
    ("inditia", "Iuditia", "Indítia", 1),
    ("lord-p", "Lprd", "Lord", 1),
    ("miniya", "Mintiya", "Miníya", 1),
    ("o-god", "OGod", "O God", 1),
    ("o-holy", "OHoly", "O Holy", 1),
    ("o-lord", "OLord", "O Lord", 1),
    ("o-son", "OSon", "O Son", 1),
    ("parastasa", "Parastdsa", "Parastása", 1),
    ("proto-deacon-l", "Prolo-Deacon", "Proto-Deacon", 1),
    ("sanctification-hyphen", "sanc-tification", "sanctification", 1),
    ("setting-up", "Selting-up", "Setting-up", 1),
    ("alleluia", "AlleIeluia", "Alleluia", 1),
    ("all-powerful", "AU-Powerful", "All-Powerful", 1),
    ("bestoweth", "bestouueth", "bestoweth", 1),
    ("bogoroditchen-k", "Bogorodikhen", "Bogoróditchen", 1),
    ("ekteniya", "Ekheniya", "Ekténiya", 1),
    ("i-will", "Lwjll", "I will", 1),
    ("commemorateth", "com- memorateth", "commemorateth", 1),
    ("o-lord-apostrophe", "O'Lord", "O Lord", 1),
    ("of-joy", "ofjoy", "of joy", 1),
    ("choir-margin", "Oraat Choir", "Choir", 1),
    ("procession", "proces- sion", "procession", 1),
    ("syen", "Syfoi", "Syén", 1),
    ("transmuting", "transmuti.ig", "transmuting", 1),
    ("with-thee", "with'thee", "with thee", 1),
    ("xc-the", "XC-the", "XC - the", 1),
    ("of-thy", "ofthy", "of thy", 2),
    ("antimins-h", "Antimhin", "Antimíns", 2),
    ("soul-plural-j", "soul(j)", "soul(s)", 15),
    ("have-brace", "{have)", "(have)", 10),
    ("lord-for", "O Lord,for", "O Lord, for", 1),
    ("glory-thy", "glory,thy", "glory, thy", 1),
    ("all-blessed", "Allblessed", "All-blessed", 1),
    ("all-glorified", "allglorified", "all-glorified", 1),
    ("all-gracious", "allgracious", "all-gracious", 1),
    ("all-hymned", "allhymned", "all-hymned", 1),
    ("all-laudable", "alllaudable", "all-laudable", 1),
    ("altar-breads", "Altarbreads", "Altar-breads", 1),
    ("balance-beam", "balancebeam", "balance-beam", 1),
    ("burnt-offering", "burntoffering", "burnt-offering", 1),
    ("dung-hill", "dunghill", "dung-hill", 1),
    ("dwelling-place", "dwellingplace", "dwelling-place", 1),
    ("earth-born", "earthborn", "earth-born", 1),
    ("ever-virgin", "evervirgin", "ever-virgin", 1),
    ("faint-hearted", "fainthearted", "faint-hearted", 1),
    ("first-fruits", "firstfruits", "first-fruits", 1),
    ("forth-going", "forthgoing", "forth-going", 1),
    ("god-fearing", "Godfearing", "God-fearing", 1),
    ("god-saved", "Godsaved", "God-saved", 1),
    ("hiero-monk", "HieroMonk", "Hiero-monk", 1),
    ("life-bearing", "lifebearing", "life-bearing", 1),
    ("life-creating", "lifecreating", "life-creating", 1),
    ("life-giving", "lifegiving", "life-giving", 4),
    ("long-suffering", "longsuffering", "long-suffering", 1),
    ("loving-kindness", "lovingkindness", "loving-kindness", 4),
    ("most-bright", "mostbright", "most-bright", 1),
    ("only-begotten", "Onlybegotten", "Only-begotten", 2),
    ("home-country", "homecountry", "home-country", 2),
    ("star-cover", "starcover", "star-cover", 2),
    ("vain-glory", "vainglory", "vain-glory", 1),
    ("well-being", "wellbeing", "well-being", 1),
    ("well-pleasing", "wellpleasing", "well-pleasing", 1),
    ("wide-sleeved", "widesleeved", "wide-sleeved", 1),
    ("christ-god", "ChristGod", "Christ-God", 2),
    ("chaldaeans", "Chaldseans", "Chaldaeans", 1),
    ("comforteth", "comfort-eth", "comforteth", 1),
    ("euphrosyne", "Euph-rosyne", "Euphrosyne", 1),
    ("exapostilarion", "Exapostil-arion", "Exapostilárion", 1),
    ("sratchitza", "Sratchtiza", "Sratchitza", 1),
    ("antidoron", "antiddron", "antidōron", 2),
    ("antidoron-capital", "Antiddron", "Antidōron", 3),
    ("koliva", "kdliva", "kóliva", 2),
    ("ikona-lower", "ikdna", "ikóna", 3),
    ("ikoni-lower", "ikdni", "ikóni", 1),
    ("ikonostas", "ikonostds", "ikonostás", 1),
    ("jonah-reference", "Jonah i. 1-16, ii.t-n,iii. 1-10", "Jonah i. 1-16, ii. 1-10, iii. 1-10", 1),
    ("response-baptism-r", "salvation: R.", "salvation: ℟", 1),
    ("response-departed-j", "Lord. J$", "Lord. ℟", 1),
    ("response-journey-i", "unharmed: I$", "unharmed: ℟", 1),
    ("response-founders-percent", "holy Temple: %", "holy Temple: ℟", 1),
    ("requiem-stand-slash", "(Panikhidnik),\\ with", "(Panikhidnik), with", 1),
    ("orletz-is", "(Orletz) \\s", "(Orletz) is", 1),
    ("faithfulness-slash", "feathers;\"\\his", "feathers; his", 1),
    ("cherubim-slash", "voice:\\.et us.", "voice: Let us,", 1),
    ("thrice-slash", "(Thrice.\\", "(Thrice).", 1),
    ("amen-slash", "Amen. \\", "Amen.", 1),
    ("response-mercy-slash", "mercy. I\\", "mercy. ℟", 1),
    ("if-there-slash", "// there be", "If there be", 1),
    ("righteousness-slash", "Righteousness,/and", "Righteousness, and", 1),
    ("first-corinthians-slash", "(/ Cor.", "(1 Cor.", 3),
    ("every-man-slash", "intent cf ever/ man", "intent of every man", 1),
    ("candidate-slash", "// the Candidate", "If the Candidate", 1),
    ("canticle-one-slash", "Canticle /.,", "Canticle I.,", 1),
    ("first-timothy-slash", "(/ Timothy", "(1 Timothy", 1),
    ("moses-miriam-slash", "Moses/and Miriam", "Moses and Miriam", 1),

    # Final full-text comparison against the independent transcription and
    # the page images. These are confined to exact strings so that later
    # source drift cannot silently broaden a repair.
    ("holy-images-ikoni", "Holy Images (lkoni)", "Holy Images (Ikóni)", 1),
    ("appendix-b-twelve", "t See Appendix U, XII.", "† See Appendix B, XII.", 1),
    ("steadfast-prefatory", "stesteadfast", "steadfast", 1),
    ("wheaten-flour", "wheaten Hour", "wheaten flour", 1),
    ("curtain-it", "Lt is opened again", "It is opened again", 1),
    ("bishop-pall", "the pal! (omofor)", "the pall (omofor)", 1),
    ("post-communion-washing", "The Priest and Beacon leash their hands", "The Priest and Deacon wash their hands", 1),
    ("kafisma", "(Kajisma)", "(Kafisma)", 1),
    ("baptism-romans", "(Rom. vi. J-ii.)", "(Rom. vi. 3-11.)", 1),
    ("equal-to-apostles", "Saints-equalto-the-Apostles", "Saints-equal-to-the-Apostles", 1),
    ("annunciation-margin", "Annan- And if it be also the Feast of the Annunciation, then the Verses for that otaUon. Feast shall be sung", "And if it be also the Feast of the Annunciation, then the Verses for that Feast shall be sung", 1),
    ("epigonation", "epigondtion", "epigonation", 1),
    ("ascendancy", "ascendency", "ascendancy", 1),
    ("alleviation", "great allevation", "great alleviation", 1),
    ("soul-attaining", "soul-attainting", "soul-attaining", 1),
    ("honourable-arms", "holy andhonourable arms", "holy and honourable arms", 1),
    ("pernicious-breezes", "hurtful andpernicious breezes", "hurtful and pernicious breezes", 1),
    ("art-os-blessing", "spiritual health andblessing", "spiritual health and blessing", 1),
    ("communion-enlightenest", "whole heart; thou cleansest andenlightenest them", "whole heart; thou enlightenest them", 1),
    ("sakkos", "dalmatic (sdkkos)", "dalmatic (sákkos)", 1),
    ("dogmatik", "Dogmdtik", "Dogmátik", 2),
    ("kathedra", "(kdthedra)", "(káthedra)", 2),
    ("word-mercy-spacing", "word- mercy -is", "word - mercy - is", 1),
    ("plural-initials", "N. (AW.)", "N. (NN.)", 1),
    ("appendix-b-two", "Appendix B, LL", "Appendix B, II.", 1),
    ("according-split", "ac- .cording", "according", 1),
    ("bishop-hymn-noise", "while the Choir singeth slowly: g!", "while the Choir singeth slowly:", 1),
    ("fled-away-noise", "fled m away", "fled away", 1),
    ("gospel-of", "book oj the Holy Gospels", "book of the Holy Gospels", 1),
    ("easter-life-noise", "bestowing life. u\"", "bestowing life.", 1),
    ("potir", "Chalice (Potir)y for the wine", "Chalice (Potír), for the wine", 1),
    ("litiya", "The Liti yd is", "The Litiya is", 1),
    ("baptism-response", "servant of God, N. I f", "servant of God, N. ℟", 1),
    ("saint-nicholas-noise", "O Saint f thou", "O Saint thou", 1),
    ("reader-tunic-omission", "rarely worn except ty. It", "rarely worn except upon that day. It", 1),
    ("kneeling-response", "For those who entreat from him his aid: ty", "For those who entreat from him his aid: ℟", 1),
    ("ordinary-liturgy-footnote", "t See the ordinary Liturgy.", "† See the ordinary Liturgy.", 1),
    ("nicholas-footnote", "t Saint Nicholas the Wonder-worker.", "† Saint Nicholas the Wonder-worker.", 1),
    ("baptism-response-brace", "resurrection of Christ our God: I}", "resurrection of Christ our God: ℟", 1),
    ("warriors-response-bracket", "pray to the Lord. IJ]", "pray to the Lord. ℟", 1),
    ("rational-powers", "who hast brought into being by thy will all the powers", "who hast brought into subjection to thy will all the powers", 1),
    ("right-margin-noise", "o ft", "", 1),
    ("all-holy-joined", "allholy", "all-holy", 6),
    ("all-magnified-joined", "allmagnified", "all-magnified", 1),
    ("and-from-capital", "Andfrom", "And from", 1),
    ("and-jaws", "andjaws", "and jaws", 1),
    (
        "image-screen-layout",
        "The customary arrangement Images is as follows: On the right of the Holy cod the image",
        "The customary arrangement of the holy Images is as follows: On the right of the Holy Door is placed the image",
        1,
    ),
    ("god-of-spirits", "the Lord. Cod of spirits,...", "the Lord. O God of spirits, . . .", 1),
    ("following-prayer", "folImring Prayer", "following Prayer", 1),
    ("fortieth-day-heading", "FORTIETHDAYAFTER CHILDBIRTH", "FORTIETH DAY AFTER CHILDBIRTH", 1),
    ("here-follow", "Herefollcnv petitions", "Here follow petitions", 1),
    ("holy-baptism-heading", "HOLYBAPTISMThe Priest", "HOLY BAPTISM The Priest", 1),
    ("acts-one", "Acts i. I-II.", "Acts i. 1-11.", 1),
    ("isaiah-thirty-five", "Isaiah xxxv. I-io.", "Isaiah xxxv. 1-10.", 1),
    ("journey-response", "mercy. Ifc", "mercy. ℟", 1),
    ("imc-iihc", "IIIC", "IMC", 1),
    ("imc-ihc", "IHC", "IMC", 2),
    ("infant-from", "infantfrom", "infant from", 1),
    ("page-one-hundred-header", "ioo THE DIVINE", "", 1),
    ("likewise", "Likmnse", "Likewise", 1),
    ("bishop-now", "the Bishop nmv Bishop. cometh", "the Bishop now cometh", 1),
    ("psalm-afraid", "not'Sereafraid", "not be afraid", 1),
    ("persons-represented", "personsrepresented", "persons represented", 1),
    ("soul-why", "soulwhy", "soul, why", 1),
    ("all-night-spacing", "theAll-Night", "the All-Night", 1),
    ("communion-spacing", "thecommunion", "the communion", 1),
    ("thou-art", "thoirart", "thou art", 1),
    ("the-spirit", "tne Holy Spirit", "the Holy Spirit", 1),
    ("triodion-second", "Triddion", "Triódion", 1),
    ("vested-themselves", "vested'themselves", "vested themselves", 1),
    ("who-confess", "who-confess", "who confess", 1),
    ("who-had", "who-had", "who had", 1),
    ("proto-deacon-joined", "ProtoDeacon", "Proto-Deacon", 2),
    ("omofor", "omofdr", "omofór", 1),
    ("posokh", "pdsokh", "pósokh", 1),
    ("pritchasten", "Pritchdsten", "Pritchásten", 2),
    ("eis-polla", "Eis polli eti", "Eis polla eti", 1),
    ("all-creation", "doth atl Creation", "doth all Creation", 1),
    ("and-the-misread", " ana the ", " and the ", 2),
    ("as-i", "forasmuch asI entreat", "forasmuch as I entreat", 1),
    ("christ-our", "Christ cur God", "Christ our God", 1),
    ("the-great-fast", "not Hie Great Fast", "not the Great Fast", 1),
    ("see-page", "(Sec page 428.)", "(See page 428.)", 1),
    ("easter-margin-noise", "tid?\"\" Christ is risen", "Christ is risen", 1),
    ("drop-cap-and", "A nd", "And", 5),
    ("plural-holy-bread-noise", "Holy j Bread", "Holy Bread", 1),
    ("o-god-noise", "(J God", "O God", 1),
    ("god-hath-noise", "God J hath arisen", "God hath arisen", 1),
    ("servants-period", "servant(j.)", "servant(s.)", 1),
    ("servants-parenthesis", "servant(j)", "servant(s)", 1),
    ("altars-parenthesis", "Altar(j)", "Altar(s)", 2),
    ("homes-parenthesis", "home(j)", "home(s)", 1),
    (
        "turning-error",
        "replacing error into truth acceptable to God",
        "turning error into truth meet for God",
        1,
    ),
    ("akafist", "Akafist", "Akáfiṣṭ", 2),
    ("pentecostaron", "Pentecostarion", "Pentecostáron", 1),
    ("panikhidnik", "Panikhidnik", "Panikhíd-nik", 1),
    ("sotchenik", "Sotchelnik", "Sotchénik", 3),
    ("syedalen", "Syeddlen", "Syedálen", 7),
    ("zhervenik", "Zhertvennik", "Zhérvennik", 1),
    ("tzarskiya", "Tsarskiya Vrata", "Tzárskiya Vratá", 1),
    ("eastertide-layout", "Easter- Christ is risen", "Easter-tide. Christ is risen", 3),
    ("proto-deacon-split", "Proto- Deacon", "Proto-Deacon", 1),
    ("collect-hymn-split", "Collect- Hymn", "Collect-Hymn", 1),
    ("psalm-one-oh-three", "Psalm cm.", "Psalm CIII.", 1),
    ("psalm-one-ten", "Psalms ex., cxi.", "Psalms cx., cxi.", 1),
    ("omofor-pall", "Omofor-Pall", "Omofór-Pall", 1),
]

PUNCTUATION_JOIN_EXPECTED = 142
STANDALONE_ZERO_EXPECTED = 38
STANDALONE_ONE_EXPECTED = 24
OPEN_BRACE_EXPECTED = 75
LOWER_PUNCTUATION_JOIN_EXPECTED = 56
RESPONSE_R_COMMA_EXPECTED = 2
RESPONSE_R_EXPECTED = 25
RESPONSE_FT_EXPECTED = 10
RESPONSE_B_SEMICOLON_EXPECTED = 11

LAYOUT_CORRECTION_EXPECTED = {
    "layout-frontmatter-illustrations": 22,
    "layout-page-67": 2,
    "layout-page-80": 2,
    "layout-page-87": 5,
    "layout-page-114": 2,
    "layout-page-128": 1,
    "layout-page-133": 1,
    "layout-page-143": 2,
    "layout-page-146": 2,
    "layout-page-135": 2,
    "layout-page-309": 2,
    "layout-page-320": 1,
    "layout-page-378": 5,
    "layout-page-441": 1,
}


# Words divided between positioned blocks must be restored only after the
# blocks have been assembled into sections. All of these joins occur once and
# are confirmed by the independent text witness.
VERIFIED_BOUNDARY_CORRECTIONS = [
    (
        "frontmatter-altar-lord",
        "and the\n\nLord God Almighty",
        "and the Lord God Almighty",
        1,
    ),
    (
        "frontmatter-oblation",
        "wherewith the\n\nBishop bestows",
        "wherewith the Bishop bestows",
        1,
    ),
    (
        "frontmatter-sponge",
        "the Sponge\n\nwith which the Chalice",
        "the Sponge with which the Chalice",
        1,
    ),
    (
        "frontmatter-birth-giver",
        "of our\n\nLord; of the Holy Angels",
        "of our Lord; of the Holy Angels",
        1,
    ),
    (
        "frontmatter-stole",
        "over the left shoulder,\n\nsometimes crossed",
        "over the left shoulder, sometimes crossed",
        1,
    ),
    (
        "frontmatter-cuffs",
        "the Cuffs\n\n(Porutchi), for convenience",
        "the Cuffs (Porutchi), for convenience",
        1,
    ),
    (
        "frontmatter-zone",
        "girds himself\n\nabove his cassock",
        "girds himself above his cassock",
        1,
    ),
    (
        "frontmatter-bishop",
        "veil or cowl.\n\nIn place of the Chasuble",
        "veil or cowl. In place of the Chasuble",
        1,
    ),
    ("forgive", "for\n\ngive", "forgive", 1),
    ("orthodox", "Or\n\nthodox", "Orthodox", 1),
    ("persecuted", "perse\n\ncuted", "persecuted", 1),
    ("soberness", "sober\n\nness", "soberness", 1),
    ("christians", "Chris\n\ntians", "Christians", 1),
    ("supersensual", "super\n\nsensual", "supersensual", 1),
    ("enemies", "en\n\nemies", "enemies", 1),
    ("celebrate", "cele\n\nbrate", "celebrate", 1),
    ("sanctification", "sanctifica\n\ntion", "sanctification", 1),
    ("trinity", "Trin\n\nity", "Trinity", 1),
    ("betrayed", "be\n\ntrayed", "betrayed", 1),
    ("foreshadowing", "fore\n\nshadowing", "foreshadowing", 1),
    ("supplications", "supplica\n\ntions", "supplications", 1),
    ("redeemer", "Re\n\ndeemer", "Redeemer", 1),
    ("incarnate", "incar\n\nnate", "incarnate", 1),
    ("anticipation", "anticipa\n\ntion", "anticipation", 1),
    ("baptized", "bap\n\ntized", "baptized", 1),
    ("himself", "him\n\nself", "himself", 1),
    ("repose", "re\n\npose", "repose", 1),
    ("forerunner", "Forerun\n\nner", "Forerunner", 1),
    ("salvation", "salva\n\ntion", "salvation", 1),
    ("persons", "per\n\nsons", "persons", 1),
    ("tone-three", "Tone\n\nin.", "Tone III.", 1),
    ("altar-lower", "Al- tar", "Altar", 2),
    ("deacon-lower", "Dea- con", "Deacon", 1),
    ("accompanied-lower", "accom- panied", "accompanied", 1),
    ("because-lower", "be- cause", "because", 1),
    ("blamelessness-lower", "blameless- ness", "blamelessness", 1),
    ("brightness-lower", "bright- ness", "brightness", 1),
    ("censer-lower", "cen- ser", "censer", 1),
    ("committed-lower", "com- mitted", "committed", 1),
    ("condemnation-lower", "condemna- tion", "condemnation", 1),
    ("defilement-lower", "defile- ment", "defilement", 1),
    ("displeased-lower", "dis- pleased", "displeased", 1),
    ("himself-lower", "him- self", "himself", 1),
    ("ignorance-lower", "igno- rance", "ignorance", 1),
    ("mankind-lower", "man- kind", "mankind", 1),
    ("people-lower", "peo- ple", "people", 1),
    ("recompense-lower", "recom- pense", "recompense", 1),
    ("remember-lower", "remem- ber", "remember", 1),
    ("righteousness-lower", "righteous- ness", "righteousness", 1),
    ("sacrifices-lower", "sacri- fices", "sacrifices", 1),
    ("salvation-lower", "salva- tion", "salvation", 1),
    ("secretly-lower", "se- cretly", "secretly", 1),
    ("transgression-lower", "transgres- sion", "transgression", 1),
    ("undefiled-lower", "unde- filed", "undefiled", 1),
    ("understanding-lower", "understand- ing", "understanding", 1),
    ("unprofitable-lower", "unprofit- able", "unprofitable", 1),
]


# The major divisions follow the printed contents and printed headings. A
# source marker is included because several divisions begin on the same page.
SERVICE_SPECS = [
    ("The church and its worship", "THE SYMBOLISM OF THE CHURCH AND THE SACERDOTAL VESTMENTS", -12, "THE SYMBOLISM OF THE CHURCH"),
    ("Daily offices and the Divine Liturgy", "THE ALL-NIGHT VIGIL: GREAT VESPERS AND MATINS", 1, "THE ALL-NIGHT VIGIL SERVICE"),
    ("Daily offices and the Divine Liturgy", "THE HOURS: FIRST, THIRD, SIXTH AND NINTH", 38, "THE FIRST HOUR"),
    ("Daily offices and the Divine Liturgy", "THE TYPICAL PSALMS AND THE BEATITUDES", 58, "THE TYPICAL PSALMS"),
    ("Daily offices and the Divine Liturgy", "THE DIVINE LITURGY OF SAINT JOHN CHRYSOSTOM AND SAINT BASIL THE GREAT", 64, "THE DIVINE LITURGY"),
    ("Daily offices and the Divine Liturgy", "THE LITURGY OF THE PRESANCTIFIED GIFTS", 127, "THE OFFICE OF THE DIVINE LITURGY OF THE PRESANCTIFIED"),
    ("Daily offices and the Divine Liturgy", "THE OFFICE OF GRAND COMPLINE", 147, "THE OFFICE OF GRAND COMPLINE"),
    ("Principal feasts", "THE NATIVITY OF THE BIRTH-GIVER OF GOD", 164, "THE NATIVITY OF THE MOST HOLY BIRTHGIVER OF GOD"),
    ("Principal feasts", "THE ELEVATION OF THE PRECIOUS CROSS", 167, "THE ELEVATION OF THE PRECIOUS CROSS"),
    ("Principal feasts", "THE ENTRANCE OF THE BIRTH-GIVER OF GOD INTO THE TEMPLE", 171, "THE ENTRANCE INTO (PRESENTATION IN) THE TEMPLE"),
    ("Principal feasts", "THE NATIVITY OF CHRIST", 174, "THE NATIVITY OF CHRIST"),
    ("Principal feasts", "THE EPIPHANY AND THE GREAT BLESSING OF WATERS", 182, "THE EPIPHANY"),
    ("Principal feasts", "THE MEETING OF THE LORD", 198, "THE MEETING OF THE LORD"),
    ("Principal feasts", "THE ANNUNCIATION", 201, "THE ANNUNCIATION OF THE MOST HOLY VIRGIN"),
    ("Principal feasts", "THE ENTRANCE OF THE LORD INTO JERUSALEM (PALM SUNDAY)", 204, "THE ENTRANCE OF THE LORD INTO JERUSALEM"),
    ("Principal feasts", "GREAT THURSDAY", 208, "GREAT THURSDAY"),
    ("Principal feasts", "GREAT FRIDAY", 214, "GREAT (GOOD) FRIDAY"),
    ("Principal feasts", "GREAT SATURDAY", 220, "GREAT SATURDAY"),
    ("Principal feasts", "EASTER", 226, "EASTER"),
    ("Principal feasts", "THE ASCENSION", 242, "THE ASCENSION OF OUR LORD JESUS CHRIST"),
    ("Principal feasts", "PENTECOST", 245, "PENTECOST (WHITSUNDAY)"),
    ("Principal feasts", "THE TRANSFIGURATION", 258, "THE TRANSFIGURATION OF THE LORD"),
    ("Principal feasts", "THE FALLING-ASLEEP OF THE BIRTH-GIVER OF GOD", 263, "THE FALLING-ASLEEP (ASSUMPTION)"),
    ("Sacraments and pastoral offices", "PRAYERS FOR A MOTHER AND CHILD", 266, "PRAYERS"),
    ("Sacraments and pastoral offices", "AT THE NAMING OF A CHILD, WHEN HE RECEIVETH HIS NAME, ON THE EIGHTH DAY AFTER HIS BIRTH", 267, "AT THE NAMING OF A CHILD"),
    ("Sacraments and pastoral offices", "FOR A WOMAN ON THE FORTIETH DAY AFTER CHILDBIRTH", 268, "FOR A WOMAN ON THE FORTIETH"),
    ("Sacraments and pastoral offices", "THE OFFICE OF HOLY BAPTISM", 271, "THE OFFICE OF HOLY BAPTISM"),
    ("Sacraments and pastoral offices", "THE OFFICE OF HOLY CHRISMATION", 281, "THE OFFICE OF HOLY CHRISMATION"),
    ("Sacraments and pastoral offices", "THE RITE OF CONFESSION", 286, "THE RITE OF CONFESSION"),
    ("Sacraments and pastoral offices", "THE RITE OF HOLY MATRIMONY", 291, "THE RITE OF HOLY MATRIMONY"),
    ("Sacraments and pastoral offices", "ORDINATIONS: READERS, DEACONS, PRIESTS, ABBOTS AND BISHOPS", 306, "THE OFFICE OF SETTING APART READERS AND CHANTERS"),
    ("Sacraments and pastoral offices", "THE OFFICE OF HOLY UNCTION", 332, "THE OFFICE OF HOLY UNCTION"),
    ("Sacraments and pastoral offices", "THE OFFICE AT THE PARTING OF THE SOUL FROM THE BODY", 360, "THE OFFICE AT THE PARTING OF THE SOUL FROM THE BODY"),
    ("Burial and commemoration", "THE ORDER FOR THE BURIAL OF THE DEAD (LAYMEN)", 368, "THE ORDER FOR THE BURIAL OF THE DEAD (LAYMEN)"),
    ("Burial and commemoration", "THE ORDER FOR THE BURIAL OF THE DEAD (PRIESTS)", 394, "THE ORDER FOR THE BURIAL OF THE DEAD (PRIESTS)"),
    ("Burial and commemoration", "THE ORDER FOR THE BURIAL OF A CHILD", 424, "THE ORDER FOR THE BURIAL OF A CHILD"),
    ("Burial and commemoration", "THE BURIAL OF THOSE WHO DIE AT EASTER", 435, "THE ORDER FOR THE BURIAL OF THOSE WHO DIE AT HOLY EASTER"),
    ("Burial and commemoration", "THE REQUIEM OFFICE FOR THE DEAD", 437, "THE REQUIEM OFFICE FOR THE DEAD"),
    ("Burial and commemoration", "THE CANON FOR ORTHODOX WARRIORS SLAIN ON THE FIELD OF BATTLE FOR THE FAITH AND THE FATHERLAND.", 449, "THE CANON FOR ORTHODOX WARRIORS"),
    ("Reception into the Church", "THE OFFICE FOR RECEIVING INTO THE ORTHODOX FAITH", 454, "THE OFFICE FOR RECEIVING INTO THE ORTHODOX FAITH"),
    ("Reception into the Church", "THE OFFICE FOR THE RECEPTION INTO THE ORTHODOX CHURCH OF JEWS, MAHOMETANS (SARACENS) AND HEATHENS", 467, "THE OFFICE FOR THE RECEPTION INTO THE ORTHODOX CHURCH OF JEWS"),
    ("Blessings and occasional offices", "THE LESSER BLESSING OF WATER", 470, "THE LESSER BLESSING OF WATER"),
    ("Blessings and occasional offices", "THE OFFICE USED AT THE FOUNDING OF A CHURCH", 479, "THE OFFICE USED AT THE FOUNDING OF A CHURCH"),
    ("Blessings and occasional offices", "THE OFFICE AT THE CONSECRATION OF A CHURCH", 493, "THE OFFICE AT THE CONSECRATION OF A CHURCH"),
    ("Blessings and occasional offices", "A SERVICE OF THANKSGIVING FOR AN ANSWER TO PRAYER, AND FOR EVERY FAVOUR FROM GOD", 512, "A SERVICE OF THANKSGIVING FOR AN ANSWER TO PRAYER"),
    ("Blessings and occasional offices", "A SERVICE OF PRAYER WHEN CHILDREN BEGIN THEIR INSTRUCTION", 519, "A SERVICE OF PRAYER WHEN CHILDREN BEGIN THEIR INSTRUCTION"),
    ("Blessings and occasional offices", "BLESSINGS FOR A JOURNEY BY LAND AND WATER", 524, "THE RITE OF BLESSING FOR A JOURNEY"),
    ("Thanksgiving services", "THE OFFICE OF THANKSGIVING AT THE NEW YEAR", 534, "THE OFFICE OF THANKSGIVING AT THE NEW YEAR"),
    ("Thanksgiving services", "THE OFFICE OF PRAISE AND THANKSGIVING TO THE LORD GOD", 541, "THE OFFICE OF PRAISE AND THANKSGIVING TO THE LORD GOD"),
    ("Thanksgiving services", "THE GREAT OFFICE OF THANKSGIVING (TE DEUM): FOR OCCASIONS OF SOLEMN THANKSGIVING", 550, "THE GREAT OFFICE OF THANKSGIVING (TE DEUM)"),
    ("Blessings and occasional offices", "MANY YEARS (LONG LIFE)", 556, "MANY YEARS (LONG LIFE)"),
    ("Blessings and occasional offices", "PRAYERS AT THE FOUNDING OF A HOUSE", 557, "PRAYERS AT THE FOUNDING OF A HOUSE"),
    ("Blessings and occasional offices", "WHEN ONE IS ABOUT TO TAKE UP HIS ABODE IN A NEW HOUSE", 557, "WHEN ONE IS ABOUT TO TAKE UP HIS ABODE IN A NEW HOUSE"),
    ("Blessings and occasional offices", "FOR THE BLESSING OF ANY OBJECT", 557, "FOR THE BLESSING OF ANY OBJECT"),
    ("Blessings and occasional offices", "A GENERAL SERVICE OF PRAYER (MOLIEBEN)", 559, "A GENERAL SERVICE OF PRAYER"),
    ("Burial and commemoration", "THE GENERAL PANIKHIDA OR REQUIEM SERVICE", 564, "THE GENERAL PANIKHIDA OR REQUIEM SERVICE"),
    ("Preparation for Holy Communion", "PRAYERS IN PREPARATION FOR THE HOLY COMMUNION (A SELECTION)", 570, "PRAYERS IN PREPARATION FOR THE HOLY COMMUNION"),
    ("Appendices", "APPENDIX A: THE EIGHT TONES", 577, "APPENDIX A"),
    ("Appendices", "APPENDIX B: EXPLANATORY NOTES ON THE SERVICES", 592, "APPENDIX B"),
]


# These page ranges contain two independent streams printed beside one
# another. They were established by auditing every page with overlapping
# left and right coordinate blocks in the prepared EPUB.
PARALLEL_RANGES = [
    (1, 4), (6, 7), (20, 24), (80, 88), (91, 100), (105, 122),
    (128, 145), (192, 193), (276, 277), (313, 313), (316, 317),
    (340, 341), (369, 369), (458, 460),
]

# The coordinate detector originally reported these 22 regions. Printed page
# -25 is a two-column table in the front matter, before the first ingested
# service. The remaining 21 regions are covered by the 14 broader ranges
# above. Small one-page gaps are retained inside a broader range so that a
# stream which temporarily leaves one column does not rejoin the other.
DETECTED_PARALLEL_REGIONS = [
    (-25, -25), (1, 4), (6, 7), (20, 20), (24, 24), (80, 88),
    (91, 94), (96, 100), (105, 108), (110, 112), (114, 117),
    (120, 122), (128, 133), (135, 140), (145, 145), (192, 193),
    (276, 277), (313, 313), (316, 317), (340, 341), (369, 369),
    (458, 460),
]

TRACK_TITLES = {
    (1, 4, "right"): "THE PRAYERS OF LIGHT",
    (20, 24, "right"): "THE MORNING PRAYERS",
}

SOURCE_HEADINGS = {
    "THE LITURGY OF THE PRESANCTIFIED GIFTS": ["THE SHORT CANON."],
}

PARA_ID = re.compile(
    r"para\.(\d+)\.(\d+)\.(\d+)\.box\."
    r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
)


def sha1(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def apply_ocr_corrections(value):
    counts = Counter()
    for label, bad, good, unused_expected in VERIFIED_OCR_CORRECTIONS:
        count = value.count(bad)
        if count:
            value = value.replace(bad, good)
            counts[label] += count

    value, count = re.subn(r"(?<!\d)0(?!\d)", "O", value)
    counts["standalone-zero-to-o"] += count
    value, count = re.subn(
        r"(?<!\d)1 (?=(?:have|will|am|forget|beseech|know|deal|had|go|may)\b)",
        "I ",
        value,
    )
    counts["standalone-one-to-i"] += count
    value, count = re.subn(r"(?<![A-Za-z])R,(?![A-Za-z])", "℟", value)
    counts["response-r-comma"] += count
    value, count = re.subn(r"(?<![A-Za-z])R(?![A-Za-z.,])", "℟", value)
    counts["response-r"] += count
    value, count = re.subn(r"(?<![A-Za-z])ft(?![A-Za-z])", "℟", value)
    counts["response-ft"] += count
    value, count = re.subn(r"B;", "℟", value)
    counts["response-b-semicolon"] += count
    count = value.count("{")
    value = value.replace("{", "(")
    counts["open-brace-to-parenthesis"] += count

    value, count = re.subn(r"(?<=[a-z])([,;:])(?=[a-z])", r"\1 ", value)
    counts["lower-punctuation-join"] += count
    value, count = re.subn(r"(?<=[a-z])([.])(?=[a-z])", r"\1 ", value)
    counts["lower-punctuation-join"] += count

    # Missing spaces after punctuation are a separate scan failure. A period
    # between capital letters is excluded so A.D., N.S., and initials retain
    # the form printed in the edition.
    value, count = re.subn(
        r"(?<=[A-Za-z0-9)\]])([:;!?])(?=[A-Z])", r"\1 ", value
    )
    counts["punctuation-join"] += count
    value, count = re.subn(
        r"(?<=[a-z0-9)\]])([.,])(?=[A-Z])", r"\1 ", value
    )
    counts["punctuation-join"] += count
    value, count = re.subn(r"(?<=[)\]])(?=[A-Z])", " ", value)
    counts["punctuation-join"] += count
    return value, counts


def assert_ocr_correction_counts(counts):
    expected = {
        label: count
        for label, unused_bad, unused_good, count
        in VERIFIED_OCR_CORRECTIONS
    }
    expected["punctuation-join"] = PUNCTUATION_JOIN_EXPECTED
    expected["standalone-zero-to-o"] = STANDALONE_ZERO_EXPECTED
    expected["standalone-one-to-i"] = STANDALONE_ONE_EXPECTED
    expected["open-brace-to-parenthesis"] = OPEN_BRACE_EXPECTED
    expected["lower-punctuation-join"] = LOWER_PUNCTUATION_JOIN_EXPECTED
    expected["response-r-comma"] = RESPONSE_R_COMMA_EXPECTED
    expected["response-r"] = RESPONSE_R_EXPECTED
    expected["response-ft"] = RESPONSE_FT_EXPECTED
    expected["response-b-semicolon"] = RESPONSE_B_SEMICOLON_EXPECTED
    expected.update(LAYOUT_CORRECTION_EXPECTED)
    mismatches = []
    for label, count in sorted(expected.items()):
        if counts[label] != count:
            mismatches.append(
                "%s expected %d, found %d" % (label, count, counts[label])
            )
    unexpected = sorted(set(counts) - set(expected))
    if unexpected:
        mismatches.append("unexpected rules: %s" % ", ".join(unexpected))
    if mismatches:
        raise ValueError("OCR correction audit failed: " + "; ".join(mismatches))


def clean_text(value, correct_ocr=False):
    value = value.replace("\u00a0", " ")
    value = value.replace("\u2014", "-").replace("\u2013", "-")
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.replace("\u201c", '"').replace("\u201d", '"')
    value = value.replace("\x1b", "")
    value = re.sub(r"\s+", " ", value)
    counts = Counter()
    if correct_ocr:
        value, counts = apply_ocr_corrections(value)
    value = re.sub(r"\s+", " ", value)
    if correct_ocr:
        return value.strip(), counts
    return value.strip()


def own_text(element):
    values = []

    def visit(node):
        if node.text:
            values.append(node.text)
        for child in node:
            if child.get("id", "").startswith("para."):
                if child.tail:
                    values.append(child.tail)
                continue
            visit(child)
            if child.tail:
                values.append(child.tail)

    visit(element)
    return clean_text("".join(values), correct_ocr=True)


def epub_xml_members():
    if not EPUB.exists():
        raise FileNotFoundError(EPUB)
    if sha256(EPUB) != EPUB_SHA256:
        raise ValueError("unexpected prepared EPUB hash")
    if IA_OCR.exists() and sha1(IA_OCR) != IA_OCR_SHA1:
        raise ValueError("unexpected Internet Archive OCR hash")
    with zipfile.ZipFile(EPUB) as archive:
        names = [
            name for name in archive.namelist()
            if re.fullmatch(r"OEBPS/Text/content-\d+\.xml", name)
        ]
        names.sort()
        for name in names:
            value = archive.read(name).decode("utf-8")
            value = value.replace("&nbsp;", "&#160;")
            value = value.replace("&dagger;", "&#8224;")
            value = value.replace("\x1b", "")
            yield name, value


def extract_records(with_audit=False):
    records = []
    seen = defaultdict(list)
    source_order = 0
    correction_counts = Counter()
    for member, value in epub_xml_members():
        root = ET.fromstring(value)
        for element in root.iter():
            identifier = element.get("id", "")
            match = PARA_ID.match(identifier)
            if not match:
                continue
            obj, block, sub, x, y, width, height = map(int, match.groups())
            text, local_corrections = own_text(element)
            if not text:
                correction_counts.update(local_corrections)
                continue
            if text in seen[identifier]:
                continue
            seen[identifier].append(text)
            correction_counts.update(local_corrections)
            if len(seen[identifier]) > 1:
                identifier += "::duplicate-%d" % len(seen[identifier])
            source_order += 1
            records.append({
                "record_id": identifier,
                "page": obj - 43,
                "block": block,
                "sub": sub,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "class": element.get("class", ""),
                "member": member,
                "source_order": source_order,
                "text": text,
            })
    layout_counts = reconstruct_layout_records(records)
    correction_counts.update(layout_counts)
    records.sort(key=lambda row: (
        row["page"], row["block"], row["sub"], row["y"], row["x"],
        row["source_order"],
    ))
    if not records:
        raise ValueError("prepared EPUB contains no positioned paragraphs")
    assert_ocr_correction_counts(correction_counts)
    if with_audit:
        return records, correction_counts
    return records


def reconstruct_layout_records(records):
    """Separate text streams which the prepared source still interleaves."""
    counts = Counter()

    def identified(identifier):
        matches = [row for row in records if row["record_id"] == identifier]
        if len(matches) != 1:
            raise ValueError("layout record is missing or duplicated: %s" % identifier)
        return matches[0]

    def selected(identifier, expected):
        row = identified(identifier)
        if row["text"] != expected:
            raise ValueError("layout record changed: %s" % identifier)
        return row

    def replace_once(row, before, after):
        if row["text"].count(before) != 1:
            raise ValueError("layout fragment changed: %s" % row["record_id"])
        row["text"] = row["text"].replace(before, after)

    # The opening symbolism and vestment essay is set around illustrations.
    # The prepared text treated several image captions as running prose, split
    # sentences around them, and interleaved a mitre footnote with the prior
    # paragraph. Retain the essay and printed footnote, but omit labels for
    # illustrations which are not reproduced in the native text.
    frontmatter_captions = [
        selected(
            "para.33.5.0.box.948.2161.226.22.q.70",
            "Table of Oblation",
        ),
        selected(
            "para.34.2.0.box.204.960.153.51.q.70",
            "Sacramental Fan",
        ),
        selected("para.34.9.0.box.940.2095.93.22.q.70", "Chalice"),
        selected("para.34.10.0.box.1227.2102.68.21.q.70", "spear"),
        selected("para.35.2.0.box.302.885.71.21.q.60", "Ladle"),
        selected("para.36.1.0.box.298.204.87.30.q.60", "Lord"),
        selected(
            "para.36.3.0.box.396.200.1071.1049.q.60",
            "Banner",
        ),
        selected(
            "para.38.3.0.box.134.1821.287.109.q.70",
            "Position of the fingers of the right hand in making the sign "
            "of the cross",
        ),
        selected(
            "para.38.5.0.box.1173.1880.287.202.q.60",
            "Position of the fingers of the right hand for Bishops and "
            "Priests, in bestowing the benediction. The letters IC, XC, "
            "Jesus Christ, are formed",
        ),
        selected(
            "para.39.3.0.box.378.2058.678.34.q.60",
            "Dalmatic (Stikhar) Stole (Orar)",
        ),
        selected(
            "para.40.3.0.box.283.1552.1179.34.q.60",
            "Zone, or Girdle Cassock Stole (Epitrakhil)",
        ),
        selected("para.42.5.0.box.344.1690.70.23.q.60", "Mitre"),
        selected(
            "para.42.7.0.box.1138.2093.351.29.q.70",
            "Pectoral Image (Panagia)",
        ),
        selected(
            "para.43.3.0.box.377.1201.208.28.q.70",
            "Bishop's Mantle",
        ),
    ]
    for caption in frontmatter_captions:
        records.remove(caption)

    vessels = identified("para.34.7.1.box.190.1716.1165.522.q.50")
    replace_once(
        vessels,
        "the Chalice (Potír), for the wine and the Spear (Kopyo), with which",
        "the Chalice (Potír), for the wine; the Spear (Kopyo), with which",
    )

    banner = identified("para.36.6.2.box.124.1514.1342.164.q.60")
    if not banner["text"].endswith(
        "typifying the victorious of Christ's Church, which wages incessant "
        "warfare with the enemies of salvation."
    ):
        raise ValueError("frontmatter banner text changed")
    banner["text"] = (
        "At each Kliros (Choir-place) stands a holy Banner (Khorugv); that "
        "is, a holy picture mounted upon a staff, typifying the victorious "
        "Banner of Christ's Church, which wages incessant warfare with the "
        "enemies of salvation."
    )

    vestibule = identified("para.37.4.1.box.159.1475.1322.305.q.60")
    replace_once(
        vestibule,
        "such as the Litiya. litany of fervent supplication",
        "such as the Litiya (a litany of fervent supplication",
    )

    wax = identified("para.37.4.3.box.203.2043.1278.41.q.60")
    matter = identified("para.38.1.0.box.126.222.1328.176.q.60")
    if not wax["text"].endswith("free from animal"):
        raise ValueError("frontmatter wax paragraph changed")
    if not matter["text"].startswith("matter, are used for lighting"):
        raise ValueError("frontmatter wax continuation changed")
    wax["text"] += " " + matter["text"]
    records.remove(matter)

    bishop_start = identified("para.41.4.3.box.181.2155.1323.86.q.60")
    replace_once(
        bishop_start,
        "his biretta being perpendicular, black, and draped with upon "
        "Archimandrites, or Abbots, and upon certain Archpriests.)",
        "his biretta being perpendicular, black, and draped with the "
        "monastic veil or cowl.",
    )

    bishop_body = identified("para.42.3.0.box.160.225.729.915.q.60")
    replace_once(
        bishop_body,
        "the monastic veil or cowl. In place of the Chasuble",
        "In place of the Chasuble",
    )
    replace_once(
        bishop_body,
        "The Mitre is typical of a diadem or crown, and serves as an emblem "
        "of the power bestowed upon a minister of the Church. (The Mitre is "
        "conferred also",
        "The Mitre is typical of a diadem or crown, and serves as an emblem "
        "of the power bestowed upon a minister of the Church. (The Mitre is "
        "conferred also upon Archimandrites, or Abbots, and upon certain "
        "Archpriests.)",
    )

    crozier = identified(
        "para.43.2.0.box.153.221.1339.1225.q.60::duplicate-2"
    )
    if not crozier["text"].endswith("battlemented city. A"):
        raise ValueError("frontmatter crozier text changed")
    crozier["text"] = (
        "The Crozier, or Pastoral Staff (Posokh), is given to Bishops and to "
        "Archimandrites, in token of their spiritual authority over the "
        "monasteries or cities which they rule; and as a sign that it "
        "behooves them to feed the flock of Christ. The Eagle (Orletz) is a "
        "small circular rug, with the representation of a one-headed eagle "
        "soaring over a battlemented city. A Bishop stands on this rug "
        "during divine service, and to him alone is its use accorded. He is "
        "led upon a large \"Eagle\" at his Consecration, as the Office of "
        "Consecration sets forth. (See that Office.) The view of the city "
        "betokens the Prelate's rule over the city; the Eagle denotes the "
        "loftiness and purity of his teaching. Thus the Eagle-rug spread "
        "for a Bishop to stand upon signifies that he, by his life and "
        "doctrine, must resemble the eagle, which soars above all lower "
        "things, and aspires unto heaven."
    )
    counts["layout-frontmatter-illustrations"] = 22

    # A footnote at the bottom of page 67 divides "iniquities" across the
    # page break. Restore the word without moving or suppressing the note.
    page_67_end = selected(
        "para.110.1.16.box.173.2079.1275.85.q.50",
        "Have mercy upon us, O Lord, for in thee have we trusted, and be not "
        "very wroth with us, neither call thou to remembrance our iniqui",
    )
    page_68_start = selected(
        "para.111.1.0.box.149.199.1278.177.q.60",
        "ties; but look down even now upon us, inasmuch as thou art of tender "
        "compassion, and deliver us from our enemies: for thou art our God, "
        "and we are thy people, we are all the work of thy hand, and we call "
        "upon thy Name.",
    )
    page_67_end["text"] = (
        "Have mercy upon us, O Lord, for in thee have we trusted, and be not "
        "very wroth with us, neither call thou to remembrance our iniquities"
    )
    page_68_start["text"] = (
        "but look down even now upon us, inasmuch as thou art of tender "
        "compassion, and deliver us from our enemies: for thou art our God, "
        "and we are thy people, we are all the work of thy hand, and we call "
        "upon thy Name."
    )
    counts["layout-page-67"] = 2

    # Page 80 prints the Great Litany in the left column and a secret prayer
    # in the right. The prepared text retained one line containing the end of
    # the left-column petition beside the middle of the heading. Restore the
    # printed reading order and remove that duplicate mixed line.
    page_80_main = selected(
        "para.123.3.0.box.174.908.651.328.q.60",
        "The Great Litany Deacon. In peace let us pray to Choir. Lord, have "
        "mercy. For the peace that is from above, and for the salvation of "
        "our souls, let us pray to the Lord. †",
    )
    page_80_mixed = selected(
        "para.123.4.0.box.826.907.366.81.q.60",
        "Y (Velikaya Ekténiya). the Lord.",
    )
    page_80_main["text"] = (
        "The Great Litany (Velikaya Ekténiya). Deacon. In peace let us pray "
        "to the Lord. Choir. Lord, have mercy. For the peace that is from "
        "above, and for the salvation of our souls, let us pray to the Lord. †"
    )
    records.remove(page_80_mixed)
    counts["layout-page-80"] = 2

    # Page 87 carries fragments of its vertical margin label in the OCR and
    # splits the last line of the pontifical column across four records.
    page_87_main = selected(
        "para.130.2.6.box.772.911.676.372.q.60",
        "Bishop. Blessed art thou on the throne of glory of thy kingdom, who "
        "sittest on the Cherubim all-hymned and exalted forever. (11) The "
        "Bishop then ascendeth the High Place, and standeth there, looking "
        "towards the People. And he giveth the dikiri to the Deacon. And the "
        "Proto-Deacon giveth the trikiri to",
    )
    page_87_co = selected("para.130.2.0.box.1481.459.21.17.q.50", "Co")
    page_87_ba = selected("para.130.3.0.box.1485.1192.29.28.q.50", "ba")
    page_87_in = selected("para.130.3.1.box.1484.1231.21.21.q.60", "in")
    page_87_hymn = selected(
        "para.130.3.2.box.171.1264.1334.240.q.60",
        "5 the Bishop, reciting the Hymn. In Jordan was the Trinity made "
        "manifest; for the Most-Divine Person of the Father Himself "
        "proclaimed: He that is baptized, the same is my beloved Son. And the "
        "Spirit descended upon Him that was like unto Himself. For which "
        "cause men shall bless Him and exalt him forever.",
    )
    page_87_main["text"] += " the Bishop, reciting the Hymn."
    page_87_hymn["text"] = (
        "In Jordan was the Trinity made manifest; for the Most-Divine Person "
        "of the Father Himself proclaimed: He that is baptized, the same is "
        "my beloved Son. And the Spirit descended upon Him that was like unto "
        "Himself. For which cause men shall bless Him and exalt him forever."
    )
    records.remove(page_87_co)
    records.remove(page_87_ba)
    records.remove(page_87_in)
    counts["layout-page-87"] = 5

    # Page 114 places a secret rubric to the right of the public exclamation.
    page_114_a = selected(
        "para.157.2.3.box.195.422.1276.36.q.60",
        "loudly: Here the Holy Door",
    )
    page_114_b = selected(
        "para.157.2.4.box.161.459.1309.182.q.50",
        "is closed, and the cur Let us attend. tain is drawn. And the Priest, "
        "as he elevateth the Holy Bread, shall say: Holy things unto the Holy.",
    )
    page_114_a["text"] = "loudly: Let us attend."
    page_114_b["text"] = (
        "And the Priest, as he elevateth the Holy Bread, shall say: "
        "Holy things unto the Holy."
    )
    rubric = dict(page_114_a)
    rubric.update({
        "record_id": page_114_a["record_id"] + "::rubric",
        "x": 950,
        "width": 460,
        "height": 150,
        "source_order": page_114_a["source_order"] + 0.1,
        "text": "Here the Holy Door is closed, and the curtain is drawn.",
    })
    records.append(rubric)
    counts["layout-page-114"] = 2

    # Page 128 retains two letters from a vertical margin label.
    page_128_co = selected("para.171.5.0.box.1488.1593.33.27.q.80", "Co")
    records.remove(page_128_co)
    counts["layout-page-128"] = 1

    # Page 133 prints the ordinary action and the pontifical variant in
    # parallel columns beneath a single introductory sentence.
    page_133 = selected(
        "para.176.2.9.box.162.1626.1329.166.q.60",
        "The Deacon exclaimeth: Command! And the Priest taketh the candlestick "
        "I If it be a Pontifical Service, Bishop. with its taper, and the "
        "censer, in his the Bishop taketh the trikíri and the hands, censer,",
    )
    page_133["text"] = "The Deacon exclaimeth: Command!"
    ordinary = dict(page_133)
    ordinary.update({
        "record_id": page_133["record_id"] + "::ordinary",
        "x": 162,
        "width": 500,
        "source_order": page_133["source_order"] + 0.1,
        "text": (
            "And the Priest taketh the candlestick with its taper, and the "
            "censer, in his hands,"
        ),
    })
    pontifical = dict(page_133)
    pontifical.update({
        "record_id": page_133["record_id"] + "::pontifical",
        "x": 779,
        "width": 700,
        "source_order": page_133["source_order"] + 0.2,
        "text": (
            "Bishop. If it be a Pontifical Service, the Bishop taketh the "
            "trikíri and the censer,"
        ),
    })
    records.extend([ordinary, pontifical])
    counts["layout-page-133"] = 1

    # Page 135 places a short corporal rubric in the outer margin across two
    # lines of the public litany. Restore the litany and retain that rubric as
    # its own coordinate stream.
    page_135_ruler = selected(
        "para.178.5.6.box.129.1763.1223.224.q.60",
        "Again we pray for (the Ruler of the Land, according to the elements "
        "and nationalities of which the Parish is constituted); for his "
        "might, victory, maintenance, peace, health, salvation; and that the "
        "Lord our God will abundantly aid and prosper them in all things, "
        "and subdue under their feet every foe and adversary. † Here the "
        "Priest",
    )
    page_135_synod = selected(
        "para.178.5.7.box.130.1989.1220.135.q.20",
        "Again we pray for our Holy Synod (or Patri- unfoldeth the arch); "
        "for our Bishop (or Archbishop, or Metropolitan), N., and for all "
        "our brethren in Christ. †",
    )
    page_135_ruler["text"] = (
        "Again we pray for (the Ruler of the Land, according to the elements "
        "and nationalities of which the Parish is constituted); for his "
        "might, victory, maintenance, peace, health, salvation; and that the "
        "Lord our God will abundantly aid and prosper them in all things, "
        "and subdue under their feet every foe and adversary. †"
    )
    page_135_synod["text"] = (
        "Again we pray for our Holy Synod (or Patriarch); for our Bishop "
        "(or Archbishop, or Metropolitan), N., and for all our brethren in "
        "Christ. †"
    )
    page_135_rubric = dict(page_135_ruler)
    page_135_rubric.update({
        "record_id": page_135_ruler["record_id"] + "::rubric",
        "x": 1070,
        "y": 1970,
        "width": 300,
        "height": 180,
        "source_order": page_135_ruler["source_order"] + 0.1,
        "text": (
            "Here the Priest unfoldeth the corporal, except the upper edge."
        ),
    })
    records.append(page_135_rubric)
    counts["layout-page-135"] = 2

    # The final word on page 309 is divided by a page break and a footnote.
    # Restore the word on the printed line and begin the next page with the
    # conjunction that follows it.
    page_309_end = selected(
        "para.352.1.6.box.206.2095.1231.42.q.60",
        "Pardon, remit, forgive, O God, our transgressions, both vol",
    )
    page_310_start = selected(
        "para.353.1.0.box.144.210.1350.233.q.60",
        "untary and involuntary, whether of word or of deed, whether of "
        "knowledge or of ignorance, whether of the day or of the night, "
        "whether of the mind or of the intentions: forgive us all, inasmuch "
        "as thou art good and lovest mankind. And if he desireth to say "
        "anything further, he doth so secretly.",
    )
    page_309_end["text"] = (
        "Pardon, remit, forgive, O God, our transgressions, both voluntary"
    )
    page_310_start["text"] = (
        "and involuntary, whether of word or of deed, whether of knowledge "
        "or of ignorance, whether of the day or of the night, whether of the "
        "mind or of the intentions: forgive us all, inasmuch as thou art "
        "good and lovest mankind. And if he desireth to say anything further, "
        "he doth so secretly."
    )
    counts["layout-page-309"] = 2

    # Page 320 contains the isolated letters "CI" in the outer margin. They
    # do not appear in either text witness or in the prayer's syntax.
    page_320_noise = selected(
        "para.363.1.0.box.1480.2019.20.14.q.60",
        "CI",
    )
    records.remove(page_320_noise)
    counts["layout-page-320"] = 1

    # Page 143 prints the Short Canon beside the end of the Priest's prayer.
    page_143_main = selected(
        "para.186.2.3.box.144.1742.1266.222.q.60",
        "Of thy Mystical Supper, O Son of God, accept me to-day as a "
        "communicant: for I will not speak of thy Mystery to thine enemies, "
        "neither like Judas will I give thee a kiss; but like the thief will I "
        "confess thee: Remember me, O Lord, in thy kingdom. And let not this "
        "Choir. The Short Canon. participation in thy Holy Myster",
    )
    page_143_canon = selected(
        "para.186.2.4.box.145.1971.1266.130.q.60",
        "O taste, and see how good the ies be unto judgment upon me, or Lord "
        "is. Alleluia, alleluia, alle- unto condemnation, O Lord, but unto the "
        "healing of soul and body.",
    )
    page_143_main["text"] = (
        "Of thy Mystical Supper, O Son of God, accept me to-day as a "
        "communicant: for I will not speak of thy Mystery to thine enemies, "
        "neither like Judas will I give thee a kiss; but like the thief will I "
        "confess thee: Remember me, O Lord, in thy kingdom. And let not this "
        "participation in thy Holy Mysteries be unto judgment upon me, or unto "
        "condemnation, O Lord, but unto the healing of soul and body."
    )
    page_143_canon.update({
        "x": 145,
        "width": 500,
        "text": (
            "Choir. The Short Canon. O taste, and see how good the Lord is. "
            "Alleluia, alleluia, alleluia."
        ),
    })
    counts["layout-page-143"] = 2

    # Page 146 begins with a running page header and a clipped ornament before
    # the continuation of the dismissal. Neither is part of the service text.
    page_146_ornament = selected(
        "para.189.0.0.box.16.12.57.50.q.50",
        "r",
    )
    page_146_header = selected(
        "para.189.0.1.box.162.158.1354.234.q.60",
        "146 THE DIVINE LITURGY OF THE PRESANCTIFIEDThen the Priest cometh "
        "forth, and standing in his accustomed place, he saith: The blessing "
        "of the Lord, through his grace and love towards mankind, be upon you "
        "always, now, and ever, and unto ages of ages. Choir. Amen.",
    )
    page_146_header["text"] = (
        "Then the Priest cometh forth, and standing in his accustomed place, "
        "he saith: The blessing of the Lord, through his grace and love "
        "towards mankind, be upon you always, now, and ever, and unto ages of "
        "ages. Choir. Amen."
    )
    records.remove(page_146_ornament)
    counts["layout-page-146"] = 2

    # Page 378 prints the Priest's secret prayer as a narrow marginal rubric
    # beside the public Litany. The OCR flattened that rubric into two public
    # lines and split its words between them.
    page_378_glory = selected(
        "para.421.1.4.box.162.575.1352.90.q.60",
        "Glory to the Father, and to the Son, and to the Holy Spirit, now, "
        "and ever, and unto ages of ages. Amen. Alleluia. tne priest re",
    )
    page_378_deacon = selected(
        "para.421.1.5.box.164.668.1339.82.q.60",
        "Deacon. Again, yet again, in peace let us pray citeth, secretly, "
        "the to the Lord. Prayer: O God of",
    )
    page_378_choir = selected(
        "para.421.1.6.box.208.747.1305.53.q.50",
        "Choir. Lord, have mercy. (Thrice.) . . . See page 369.",
    )
    page_378_response = selected(
        "para.421.1.9.box.168.942.1349.270.q.60",
        "That the Lord God will establish his (her) soul where the Just "
        "repose. ℟ The mercy of God, the kingdom of heaven, and the "
        "remission of his (her) sins, we entreat of Christ, our King "
        "Immortal and our God. Choir. Grant it O Lord. Deacon. Let us pray "
        "to the Lord. Choir. Lord, have mercy.",
    )
    page_378_testimonies = selected(
        "para.421.2.0.box.163.1617.1353.131.q.60",
        "Thy testimonies are wonderful; therefore doth my soul keep them. "
        "If When thy word goeth forth; it giveth light and understanding "
        "unto the simple. †",
    )
    page_378_glory["text"] = (
        "Glory to the Father, and to the Son, and to the Holy Spirit, now, "
        "and ever, and unto ages of ages. Amen. Alleluia."
    )
    page_378_deacon["text"] = (
        "Deacon. Again, yet again, in peace let us pray to the Lord."
    )
    page_378_choir["text"] = (
        "Choir. Lord, have mercy. (Thrice.) The Priest reciteth, secretly, "
        "the Prayer: O God of spirits, . . . (See page 369.)"
    )
    page_378_testimonies["text"] = page_378_testimonies["text"].replace(
        "keep them. If When", "keep them. ℟ When"
    )
    counts["layout-page-378"] = 5

    # Page 441 carries the vertical label "Orthodox Warriors" through the
    # middle of a petition. It is a marginal label, not running text.
    page_441 = selected(
        "para.484.1.3.box.122.597.1352.223.q.60",
        "[Furthermore we pray for the repose of the souls of the servants "
        "of God who have fallen asleep, Orthodox Warriors, and of all who "
        "orthodox have laid down their life in battle for the Faith and the "
        "Father- warriors, land: and that He will pardon them every sin, "
        "both voluntary and involuntary.]",
    )
    page_441["text"] = (
        "[Furthermore we pray for the repose of the souls of the servants "
        "of God who have fallen asleep, Orthodox Warriors, and of all who "
        "have laid down their life in battle for the Faith and the "
        "Fatherland: and that He will pardon them every sin, both voluntary "
        "and involuntary.]"
    )
    counts["layout-page-441"] = 1
    return counts


def apply_boundary_corrections(services):
    counts = Counter()
    for label, bad, good, unused_expected in VERIFIED_BOUNDARY_CORRECTIONS:
        for service in services:
            for section in service["sections"]:
                count = section["text"].count(bad)
                if count:
                    section["text"] = section["text"].replace(bad, good)
                    counts["boundary-" + label] += count
    mismatches = []
    for label, unused_bad, unused_good, expected in VERIFIED_BOUNDARY_CORRECTIONS:
        actual = counts["boundary-" + label]
        if actual != expected:
            mismatches.append(
                "%s expected %d, found %d" % (label, expected, actual)
            )
    if mismatches:
        raise ValueError(
            "boundary correction audit failed: " + "; ".join(mismatches)
        )
    return counts


def split_record(records, index, marker):
    record = records[index]
    position = record["text"].upper().find(marker.upper())
    if position < 0:
        raise ValueError("marker not found in selected paragraph: %s" % marker)
    if position == 0:
        return index
    before = dict(record)
    after = dict(record)
    before["record_id"] += "::before"
    before["text"] = clean_text(record["text"][:position])
    after["record_id"] += "::after"
    after["text"] = clean_text(record["text"][position:])
    if not before["text"] or not after["text"]:
        raise ValueError("invalid service-boundary split for %s" % marker)
    records[index:index + 1] = [before, after]
    return index + 1


def service_boundaries(records):
    positions = []
    cursor = 0
    for unused_part, unused_title, page, marker in SERVICE_SPECS:
        matches = []
        for index in range(cursor, len(records)):
            row = records[index]
            if row["page"] < page:
                continue
            if row["page"] > page:
                break
            if marker.upper() in row["text"].upper():
                matches.append(index)
        if not matches:
            raise ValueError("missing service marker on page %s: %s" % (page, marker))
        index = split_record(records, matches[0], marker)
        positions.append(index)
        cursor = index + 1
    if positions != sorted(positions) or len(set(positions)) != len(positions):
        raise ValueError("service markers are not in source order")
    return positions


def existing_headings():
    values = defaultdict(list)
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        for unit in old.get("units", []):
            heading = unit.get("section_title")
            service = unit.get("service_title")
            letters = "".join(char for char in (heading or "") if char.isalpha())
            generic = normalized(heading or "") in {
                "choir", "deacon", "priest", "reader", "exclamation",
            }
            if (
                    heading
                    and len(letters) >= 4
                    and letters == letters.upper()
                    and not heading.startswith("CONTINUATION ON PAGE")
                    and not generic
                    and heading not in values[service]
            ):
                values[service].append(heading)
    return values


def parallel_range(page):
    for start, end in PARALLEL_RANGES:
        if start <= page <= end:
            return (start, end)
    return None


def assert_parallel_audit_coverage():
    for start, end in DETECTED_PARALLEL_REGIONS:
        if (start, end) == (-25, -25):
            continue
        for page in range(start, end + 1):
            if parallel_range(page) is None:
                raise ValueError(
                    "unaccounted parallel-layout page: %s" % page
                )


def record_track(record):
    page_range = parallel_range(record["page"])
    if not page_range:
        return "main", None
    center = record["x"] + record["width"] / 2.0
    if record["width"] < 950 and center < 760:
        return "left", page_range
    if record["width"] < 950 and center > 820:
        return "right", page_range
    return "main", None


def choose_heading(text, headings):
    text_key = normalized(text)
    candidates = []
    for heading in headings:
        key = normalized(heading)
        position = text_key.find(key)
        if len(key) >= 4 and 0 <= position <= 12:
            candidates.append((len(key), heading))
    return max(candidates)[1] if candidates else None


def synthetic_title(records, track, page_range):
    if page_range and (page_range[0], page_range[1], track) in TRACK_TITLES:
        return TRACK_TITLES[(page_range[0], page_range[1], track)]
    first = records[0]["text"].strip()
    prefix = re.split(r"(?<=[.!?])\s+", first, maxsplit=1)[0]
    if 4 <= len(prefix) <= 96 and not prefix[:1].islower():
        return prefix
    pages = sorted({row["page"] for row in records})
    if pages[0] == pages[-1]:
        return "CONTINUATION ON PAGE %s" % pages[0]
    return "CONTINUATION ON PAGES %s-%s" % (pages[0], pages[-1])


def make_sections(records, headings, track, page_range):
    sections = []
    current = []
    current_heading = None
    for record in records:
        heading = choose_heading(record["text"], headings)
        if heading and current:
            sections.append((current_heading, current))
            current = []
        if heading:
            current_heading = heading
        current.append(record)
    if current:
        sections.append((current_heading, current))
    result = []
    for heading, rows in sections:
        if not heading:
            heading = synthetic_title(rows, track, page_range)
        result.append({
            "section_title": heading,
            "source_track": track,
            "source_pages": sorted({row["page"] for row in rows}),
            "source_record_ids": [row["record_id"] for row in rows],
            "sort_key": [
                rows[0]["page"], rows[0]["y"],
                {"main": 0, "left": 1, "right": 2}[track],
            ],
            "text": "\n\n".join(row["text"] for row in rows),
        })
    return result


def build_service_fixture(spec, rows, headings):
    part_title, service_title, unused_page, unused_marker = spec
    grouped = defaultdict(list)
    for row in rows:
        track, page_range = record_track(row)
        grouped[(track, page_range)].append(row)
    sections = []
    for (track, page_range), stream in grouped.items():
        stream.sort(key=lambda row: (
            row["page"], row["y"], row["x"], row["block"], row["sub"],
        ))
        sections.extend(make_sections(stream, headings, track, page_range))
    sections.sort(key=lambda section: section["sort_key"])
    merged = []
    for section in sections:
        if (
                merged
                and merged[-1]["section_title"] == section["section_title"]
                and merged[-1]["source_track"] == section["source_track"]
        ):
            merged[-1]["text"] += "\n\n" + section["text"]
            merged[-1]["source_pages"] = sorted(set(
                merged[-1]["source_pages"] + section["source_pages"]
            ))
            merged[-1]["source_record_ids"].extend(
                section["source_record_ids"]
            )
        else:
            merged.append(section)
    sections = []
    index = 0
    while index < len(merged):
        section = merged[index]
        if (
                normalized(section["text"])
                == normalized(section["section_title"])
                and index + 1 < len(merged)
                and section["source_track"]
                == merged[index + 1]["source_track"]
        ):
            following = merged[index + 1]
            following["text"] = section["text"] + "\n\n" + following["text"]
            following["source_pages"] = sorted(set(
                section["source_pages"] + following["source_pages"]
            ))
            following["source_record_ids"] = (
                section["source_record_ids"]
                + following["source_record_ids"]
            )
            following["sort_key"] = section["sort_key"]
            index += 1
            continue
        else:
            sections.append(section)
        index += 1
    if not sections:
        raise ValueError("empty service: %s" % service_title)
    return {
        "part_title": part_title,
        "service_title": service_title,
        "sections": sections,
    }


def prepare_fixture():
    assert_parallel_audit_coverage()
    records, correction_counts = extract_records(with_audit=True)
    boundaries = service_boundaries(records)
    headings = existing_headings()
    for service_title, source_headings in SOURCE_HEADINGS.items():
        for source_heading in source_headings:
            if source_heading not in headings[service_title]:
                headings[service_title].append(source_heading)
    services = []
    assigned = []
    for index, spec in enumerate(SERVICE_SPECS):
        start = boundaries[index]
        end = boundaries[index + 1] if index + 1 < len(boundaries) else len(records)
        rows = records[start:end]
        assigned.extend(row["record_id"] for row in rows)
        services.append(build_service_fixture(spec, rows, headings[spec[1]]))
    correction_counts.update(apply_boundary_corrections(services))
    if len(assigned) != len(set(assigned)):
        raise ValueError("a source paragraph was assigned more than once")
    expected = [row["record_id"] for row in records[boundaries[0]:]]
    if assigned != expected:
        raise ValueError("source paragraph assignment lost or reordered text")
    fixture = {
        "source": {
            "title": (
                "Service Book of the Holy Orthodox-Catholic Apostolic "
                "(Greco-Russian) Church"
            ),
            "edition": "Revised edition, Association Press, 1922",
            "prepared_text_url": EPUB_URL,
            "prepared_text_sha256": EPUB_SHA256,
            "internet_archive_ocr_url": IA_OCR_URL,
            "internet_archive_ocr_sha1": IA_OCR_SHA1,
            "source_record_count": len(assigned),
            "verified_ocr_correction_count": sum(correction_counts.values()),
            "verified_ocr_corrections": dict(sorted(correction_counts.items())),
            "parallel_ranges": [list(value) for value in PARALLEL_RANGES],
        },
        "services": services,
    }
    assert_parallel_reconstruction(fixture)
    assert_text_fidelity(fixture)
    return fixture


def assert_parallel_reconstruction(fixture):
    sections = [
        section
        for service in fixture["services"]
        for section in service["sections"]
    ]
    psalm = next(
        (
            item for item in sections
            if item["section_title"] == "PSALM CIV."
            and item["source_track"] == "left"
        ),
        None,
    )
    prayers = next(
        (item for item in sections if item["section_title"] == "THE PRAYERS OF LIGHT"),
        None,
    )
    if not psalm or not prayers:
        raise ValueError("missing reconstructed Psalm CIV or Prayers of Light")
    if "thou art become exceeding glorious" not in psalm["text"]:
        raise ValueError("Psalm CIV lost its continuation")
    if "O Lord, bountiful and compassionate" in psalm["text"]:
        raise ValueError("Psalm CIV still contains the Prayers of Light")
    if "O Lord, bountiful and compassionate" not in prayers["text"]:
        raise ValueError("Prayers of Light lost their first prayer")
    if "thou art become exceeding glorious" in prayers["text"]:
        raise ValueError("Prayers of Light still contain Psalm CIV")
    for section in sections:
        if section["source_track"] in ("left", "right"):
            ranges = {
                parallel_range(page) for page in section["source_pages"]
            }
            if len(ranges) != 1 or None in ranges:
                raise ValueError("parallel unit crosses coordinate tracks")
    for start, end in PARALLEL_RANGES:
        tracks = {
            section["source_track"]
            for section in sections
            if any(start <= page <= end for page in section["source_pages"])
        }
        if not {"left", "right"}.issubset(tracks):
            raise ValueError(
                "parallel range lacks separate tracks: %s-%s" % (start, end)
            )


def assert_text_fidelity(fixture):
    sections = [
        section
        for service in fixture["services"]
        for section in service["sections"]
    ]
    text = "\n\n".join(section["text"] for section in sections)
    source = fixture["source"]
    expected_counts = {
        "source records": (source["source_record_count"], 7894),
        "verified corrections": (
            source["verified_ocr_correction_count"], 1064
        ),
        "services": (len(fixture["services"]), 59),
        "sections": (len(sections), 406),
    }
    mismatches = [
        "%s expected %d, found %d" % (label, expected, actual)
        for label, (actual, expected) in expected_counts.items()
        if actual != expected
    ]
    if mismatches:
        raise ValueError("Hapgood source count changed: " + "; ".join(mismatches))

    required = [
        "There go the ships",
        "the great and wide sea",
        "The Great Litany (Velikaya Ekténiya). Deacon. In peace let us pray "
        "to the Lord.",
        "Here the Priest unfoldeth the corporal, except the upper edge.",
        "The Priest reciteth, secretly, the Prayer: O God of spirits",
        "Orthodox Warriors, and of all who have laid down their life",
        "N. (NN.), who hath (have) been taken from us",
        "The Communion Hymn (Pritchásten)",
        "He shall lay the IMC at the upper part of the holy paten",
        "wherewith the Bishop bestows his blessing on the people",
        "the Sponge with which the Chalice is wiped out",
        "of our Lord; of the Holy Angels, Prophets and Apostles",
        "such as the Litiya (a litany of fervent supplication",
        "his biretta being perpendicular, black, and draped with the "
        "monastic veil or cowl",
        "The Mitre is conferred also upon Archimandrites, or Abbots, and "
        "upon certain Archpriests",
        "A Bishop stands on this rug during divine service",
        "which soars above all lower things, and aspires unto heaven",
    ]
    missing = [value for value in required if value not in text]
    if missing:
        raise ValueError("required source readings are missing: %r" % missing)

    forbidden = [
        "works:In",
        "theyget",
        "thegreatandwidesea",
        "There go the Father",
        "Choir. The Short Canon. participation",
        "candlestick I If",
        "tne priest re",
        "orthodox have laid",
        "Y (Velikaya Ekténiya). the Lord.",
        "\n\nCI\n\n",
        "Appendix B, LL",
        "ac- .cording",
        "book oj the Holy Gospels",
        "The Liti yd",
        "not'Sereafraid",
        "ProtoDeacon",
        "allholy",
        "allmagnified",
        "personsrepresented",
        "thecommunion",
        "Pritchdsten",
        "Triddion",
        "Dogmdtik",
        "kdthedra",
        "sdkkos",
        "IIIC",
        "IHC",
        "B;",
        "IJ]",
        "I}",
        "for the wine and the Spear",
        "typifying the victorious of Christ's Church",
        "such as the Litiya. litany",
        "draped with upon Archimandrites",
        "The Mitre is conferred also\n\nThe Panagia",
        "battlemented city. A\n\nBishop's Mantle",
    ]
    present = [value for value in forbidden if value in text]
    if present:
        raise ValueError("known OCR defects remain: %r" % present)

    artifact_patterns = [
        r"\b[A-Za-z]{2,}- [a-z]{2,}\b",
        r"(?<=[a-z])[,;:.](?=[a-z])",
        r"(?<!\w)R,(?!\w)",
        r"(?<!\w)ft(?!\w)",
        r"[{}|\\^~£«»•§$%]",
        r"//",
    ]
    found = [pattern for pattern in artifact_patterns if re.search(pattern, text)]
    if found:
        raise ValueError("residual OCR artifact patterns remain: %r" % found)
    short = [
        (section["section_title"], section["text"])
        for section in sections
        if len(section["text"].strip()) < 20
    ]
    if short:
        raise ValueError("implausibly short native sections remain: %r" % short)


def slug(value):
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return "hapgood-" + value


def work_metadata(unit_count):
    return {
        "work_id": WORK_ID,
        "payload_version": PAYLOAD_VERSION,
        "title": (
            "Service Book of the Holy Orthodox-Catholic Apostolic "
            "(Greco-Russian) Church"
        ),
        "author": "Orthodox Church",
        "language": "en",
        "date": "1906; revised edition 1922",
        "translator": "Isabel Florence Hapgood",
        "pub_year": 1922,
        "publisher": "Association Press",
        "source": (
            "Service Book of the Holy Orthodox-Catholic Apostolic Church, "
            "revised edition with endorsement by Patriarch Tikhon "
            "(New York: Association Press, 1922)"
        ),
        "source_url": EPUB_URL,
        "prepared_text_sha256": EPUB_SHA256,
        "internet_archive_ocr_sha1": IA_OCR_SHA1,
        "facsimile_url": (
            "https://archive.org/download/gtu_A32400004109975B/"
            "gtu_A32400004109975B.pdf"
        ),
        "facsimile_label": "Open the 1922 facsimile",
        "facsimile_only": False,
        "native_text": True,
        "service_book": True,
        "service_count": len(SERVICE_SPECS),
        "unit_count": unit_count,
        "source_class": "liturgical",
        "description": (
            "Isabel Florence Hapgood's revised English service book, "
            "compiled from the Church Slavonic service books of the Russian "
            "Church and collated with Greek service books. It includes the "
            "daily offices, the Divine Liturgies, principal feasts, Baptism, "
            "Chrismation, Confession, Crowning, Unction, ordinations, burial "
            "offices, water blessings, prayers for journeys, thanksgivings, "
            "and other blessings. The services and their principal sections "
            "are available here as a native Library text."
        ),
        "digitized": "Agape-Biblia and Internet Archive",
        "rights": "Public Domain",
        "rights_url": "https://archive.org/details/gtu_A32400004109975B",
        "saint": None,
        "is_saint": False,
        "purpose": "The life of prayer",
        "centuries": [20],
        "century": 20,
        "period": "20th century",
    }


def load_fixture():
    assert_parallel_audit_coverage()
    if not FIXTURE.exists():
        raise FileNotFoundError(FIXTURE)
    if FIXTURE_SHA256 and sha256(FIXTURE) != FIXTURE_SHA256:
        raise ValueError("canonical Hapgood fixture hash does not match")
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if fixture["source"]["prepared_text_sha256"] != EPUB_SHA256:
        raise ValueError("fixture prepared-text provenance does not match")
    if fixture["source"]["internet_archive_ocr_sha1"] != IA_OCR_SHA1:
        raise ValueError("fixture Internet Archive provenance does not match")
    assert_parallel_reconstruction(fixture)
    assert_text_fidelity(fixture)
    return fixture


def build_payload():
    fixture = load_fixture()
    units = []
    ordinal = 0
    service_ids = set()
    for service in fixture["services"]:
        service_title = service["service_title"]
        service_id = slug(service_title)
        if service_id in service_ids:
            raise ValueError("duplicate service ID: %s" % service_id)
        service_ids.add(service_id)
        counts = Counter(
            section["section_title"] for section in service["sections"]
        )
        seen = Counter()
        for section in service["sections"]:
            ordinal += 1
            section_title = section["section_title"]
            seen[section_title] += 1
            anchor = "Hapgood 1922, " + service_title
            if section_title:
                anchor += ", " + section_title
                if counts[section_title] > 1:
                    anchor += " (%d)" % seen[section_title]
            pages = section.get("source_pages", [])
            if pages:
                anchor += ", p. " + ", ".join(str(page) for page in pages)
            units.append({
                "unit_id": "%s::u%04d" % (WORK_ID, ordinal),
                "work_id": WORK_ID,
                "work_title": (
                    "Service Book of the Holy Orthodox-Catholic Apostolic "
                    "(Greco-Russian) Church"
                ),
                "author": "Orthodox Church",
                "source_class": "liturgical",
                "ordinal": ordinal,
                "part_title": service["part_title"],
                "service_id": service_id,
                "service_title": service_title,
                "section_title": section_title,
                "chapter_title": service_title,
                "subsection_title": section_title,
                "citation_anchor": anchor,
                "unit_type": "service_book_section",
                "text": section["text"],
            })
    if len(fixture["services"]) != len(SERVICE_SPECS):
        raise ValueError("unexpected service count")
    if len({unit["unit_id"] for unit in units}) != len(units):
        raise ValueError("duplicate unit IDs")
    if any(not unit["text"].strip() for unit in units):
        raise ValueError("empty native unit")
    payload = {"work": work_metadata(len(units)), "units": units}
    audit_payload(payload)
    return payload


def audit_payload(payload):
    serialized = json.dumps(payload, ensure_ascii=False)
    forbidden = ["\ufffd", "\u2013", "\u2014", "Ã", "â€", "Â"]
    present = [value for value in forbidden if value in serialized]
    if present:
        raise ValueError("forbidden encoding artifacts: %r" % present)
    if len({unit["unit_id"] for unit in payload["units"]}) != len(payload["units"]):
        raise ValueError("duplicate unit IDs")
    if len({unit["service_id"] for unit in payload["units"]}) != len(SERVICE_SPECS):
        raise ValueError("service IDs do not cover the printed hierarchy")


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def expected_index(payload):
    rows = json.loads(INDEX.read_text(encoding="utf-8"))
    rows = [row for row in rows if row.get("work_id") != WORK_ID]
    rows.append(payload["work"])
    rows.sort(key=lambda row: row.get("work_id", ""))
    return rows


def report(payload):
    chars = sum(len(unit["text"]) for unit in payload["units"])
    words = sum(
        len(re.findall(r"\b[\w']+\b", unit["text"], flags=re.UNICODE))
        for unit in payload["units"]
    )
    return (
        "Hapgood: %d services, %d native units, %d characters, %d words"
        % (len(SERVICE_SPECS), len(payload["units"]), chars, words)
    )


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--import-source", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    if args.import_source:
        fixture = prepare_fixture()
        FIXTURE.parent.mkdir(parents=True, exist_ok=True)
        FIXTURE.write_bytes(encoded(fixture))
        print("wrote %s" % FIXTURE.relative_to(ROOT))
        print("sha256 %s" % sha256(FIXTURE))
        print(
            "source records %d; services %d"
            % (fixture["source"]["source_record_count"], len(fixture["services"]))
        )
        return 0

    payload = build_payload()
    rows = expected_index(payload)
    if args.write:
        OUT.write_bytes(encoded(payload))
        INDEX.write_bytes(encoded(rows))

    stale = []
    if not OUT.exists() or OUT.read_bytes() != encoded(payload):
        stale.append(str(OUT.relative_to(ROOT)))
    if json.loads(INDEX.read_text(encoding="utf-8")) != rows:
        stale.append(str(INDEX.relative_to(ROOT)))
    if stale:
        print("stale: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(report(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
