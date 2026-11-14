#!/usr/bin/env python3
"""Build the native Library payload for G. V. Shann's 1891 Euchology."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "tools" / "manuscripts" / "shann_euchology_1891"
TARGET = ROOT / "data" / "library" / "euchology-shann-1891.json"
WORK_ID = "euchology-shann-1891"
WORK_TITLE = "Euchology: A Manual of Prayers of the Holy Orthodox Church"

NON_TEXT_IMAGES = {
    "0031=1-1.jpg", "0074=44-1.jpg", "0075=45-1.jpg", "0084=54-1.jpg",
    "0091=61-2.jpg", "0111=81-1.jpg", "0142=112-1.jpg", "0149=119-1.jpg",
    "0154=124-1.jpg", "0160=130-1.jpg", "0195=165-1.jpg", "0208=178-1.jpg",
    "0232=202-1.jpg", "0250=220-1.jpg", "0289=259-1.jpg", "0290=260-1.jpg",
    "0408=378-1.jpg", "0446=416-1.jpg", "0447=417-2.jpg", "0456=426-1.jpg",
    "0457=427-1.jpg", "0462=432-1.jpg", "0463=433-1.jpg", "0491=461-3.jpg",
    "0501=471-1.jpg", "0506=476-1.jpg", "0510=480-1.jpg", "0519=489-1.jpg",
    "0520=490-1.jpg", "0552=522-1.jpg",
}


@dataclass(frozen=True)
class Chapter:
    number: int
    roman: str
    title: str
    start_page: int
    part_title: str


CHAPTERS = [
    Chapter(1, "I", "The All-Night Vigil", 1, "Daily Offices"),
    Chapter(2, "II", "The Great Vespers", 44, "Daily Offices"),
    Chapter(3, "III", "The Nocturns on Sundays", 45, "Daily Offices"),
    Chapter(4, "IV", "The Great Matins", 52, "Daily Offices"),
    Chapter(5, "V", "The Little Daily Vespers", 55, "Daily Offices"),
    Chapter(6, "VI", "The Great Compline", 62, "Daily Offices"),
    Chapter(7, "VII", "The Little Compline", 82, "Daily Offices"),
    Chapter(8, "VIII", "The Daily Nocturns", 85, "Daily Offices"),
    Chapter(9, "IX", "The Daily Matins", 94, "Daily Offices"),
    Chapter(10, "X", "The First Hour, or Prime", 108, "The Hours and Typica"),
    Chapter(11, "XI", "The Third Hour, or Terce", 113, "The Hours and Typica"),
    Chapter(12, "XII", "The Sixth Hour, or Sext", 116, "The Hours and Typica"),
    Chapter(13, "XIII", "The Ninth Hour, or None", 120, "The Hours and Typica"),
    Chapter(14, "XIV", "The Pro-Liturgy Service, called The Typica", 124, "The Hours and Typica"),
    Chapter(15, "XV", "At the Liturgies of Saint Chrysostom and Saint Basil", 130, "The Divine Liturgies"),
    Chapter(16, "XVI", "At the Liturgy of the Pre-Sanctified", 166, "The Divine Liturgies"),
    Chapter(17, "XVII", "Sunday Service in the Sixth Tone", 179, "Sunday and Communion Offices"),
    Chapter(18, "XVIII", "Penitential Service to Our Lord Jesus Christ", 203, "Sunday and Communion Offices"),
    Chapter(19, "XIX", "The Office for the Holy Communion of the Divine Mystery of the Body and Blood of Christ", 221, "Sunday and Communion Offices"),
    Chapter(20, "XX", "Extracts from the Lenten Triodion", 260, "The Triodion and Pentecostarion"),
    Chapter(21, "XXI", "Extracts from the Ferial Triodion, or Pentecostarion", 378, "The Triodion and Pentecostarion"),
    Chapter(22, "XXII", "Troparia on the Resurrection in the Eight Tones for Sundays", 417, "Troparia and Commemorations"),
    Chapter(23, "XXIII", "Troparia for Week Days", 426, "Troparia and Commemorations"),
    Chapter(24, "XXIV", "Troparia for the Festivals of the Lord and of the Holy Mother of God", 433, "Troparia and Commemorations"),
    Chapter(25, "XXV", "Troparia and Condakia Common for the Saints", 461, "Troparia and Commemorations"),
    Chapter(26, "XXVI", "Diptychs, or Remembrancer", 471, "Reference and Remembrance"),
    Chapter(27, "XXVII", "Of the Recitation of the Psalter", 476, "Reference and Remembrance"),
    Chapter(28, "XXVIII", "Table of Epistle and Gospel Lessons", 480, "Reference and Remembrance"),
    Chapter(29, "XXIX", "The Kalendar", 490, "Reference and Remembrance"),
    Chapter(30, "XXX", "An Almanack for Fifty Years", 522, "Reference and Remembrance"),
]


MAIN_MARKERS = {
    1: ("I. THE ALL-NIGHT VIGIL",), 2: ("II. THE GREAT VESPERS",),
    3: ("III. THE NOCTURNS ON SUNDAYS",), 4: ("IV. THE GREAT MATINS",),
    5: ("V. THE LITTLE DAILY VESPERS",), 6: ("VI. THE GREAT COMPLINE",),
    7: ("VII. THE LITTLE COMPLINE",), 8: ("VIII. THE DAILY NOCTURNS", "III. THE DAILY NOCTURNS"),
    9: ("IX. THE DAILY MATINS",),
    10: ("X. THE FIRST HOUR",), 11: ("XL THE THIRD HOUR", "XI. THE THIRD HOUR"),
    12: ("XII. THE SIXTH HOUR",), 13: ("XIII. THE NINTH HOUR",),
    14: ("XIV. THE PRO-LITURGY SERVICE",),
    15: ("XV. AT THE LITURGIES OF SAINT CHRYSOSTOM AND SAINT BASIL",),
    16: ("XVI. AT THE LITURGY OF THE",), 17: ("XVII. SUNDAY SERVICE IN THE SIXTH TONE",),
    18: ("XVIII. PENITENTIAL SERVICE TO OUR LORD JESUS CHRIST",),
    19: ("XIX. THE OFFICE FOR THE HOLY COMMUNION",),
    20: ("XX. EXTRACTS FROM THE LENTEN TRIODION", "XX. EXTRACTS FROM THE"),
    21: ("XXI. EXTRACTS FROM THE FERIAL TRIODION",),
    22: ("XXII. TROPARIA ETC. ON THE RESURRECTION",),
    23: ("XXIII. TROPARIA ETC. FOR WEEK DAYS", "XXIII. TROPARIA ETC. FOR"),
    24: ("XXIV. TROPARIA ETC. FOR THE FESTIVALS",),
    25: ("XXV. TROPARIA AND CONDAKIA",), 26: ("XXVI. DIPTYCHS",),
    27: ("XXVII. OF THE RECITATION",),
    28: ("XXVIII. TABLE OF EPISTLE AND GOSPEL LESSONS",),
    29: ("XXIX. THE KALENDAR",), 30: ("XXX. AN ALMANACK FOR",),
}

FALLBACK_MARKERS = {
    7: "VII. THE LITTLE COMPLINE.", 8: "III. THE DAILY NOCTURNS.",
    9: "IX. THE DAILY MATINS.", 10: "X. THE FIRST HOUR,",
}

MOJIBAKE_REPLACEMENTS = {
    "\u201a\u00c4\u00f4": "'", "\u201a\u00c4\u00fa": '"', "\u201a\u00c4\u00f9": '"',
    "\u201a\u00c4\u00ee": "-", "\u201a\u00c4\u00ec": "-", "\u221a\u00b6": "ae",
    "\u221a\u00a9": "e", "\u221a\u00b4": "e", "\u221a\u00df": "c",
}

BLOCK_TAGS = {
    "p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote",
    "tr", "td", "th", "center", "table", "div",
}


class BlockParser(HTMLParser):
    def __init__(self, drop_caps: dict[str, str] | None = None) -> None:
        super().__init__(convert_charrefs=True)
        self.drop_caps = drop_caps or {}
        self.blocks: list[str] = []
        self.current: list[str] = []
        self.skip_depth = 0
        self.drop_cap_uses: list[str] = []

    def flush(self) -> None:
        text = " ".join("".join(self.current).replace("\u00a0", " ").split())
        self.current = []
        if text:
            self.blocks.append(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in BLOCK_TAGS:
            self.flush()
        if tag == "br":
            self.flush()
        if tag != "img":
            return
        attr = {key: value or "" for key, value in attrs}
        match = re.search(r"/([^/]+\.jpg)$", attr.get("src", ""), re.I)
        if match and match.group(1) in self.drop_caps:
            name = match.group(1)
            self.current.append("[[DROP:" + name + "]]")
            self.drop_cap_uses.append(name)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if not self.skip_depth and tag in BLOCK_TAGS:
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.current.append(data)


def repair_macroman_mojibake(text: str) -> str:
    """Reverse the mixed UTF-8-as-MacRoman decoding inherited by the EPUB."""
    result: list[str] = []
    index = 0
    while index < len(text):
        repaired = False
        for width in (4, 3, 2):
            chunk = text[index:index + width]
            if len(chunk) != width:
                continue
            try:
                decoded = chunk.encode("mac_roman").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            if len(decoded) == 1 and ord(decoded) > 127:
                result.append(decoded)
                index += width
                repaired = True
                break
        if not repaired:
            result.append(text[index])
            index += 1
    return "".join(result)


def apply_source_ocr_repairs(text: str) -> str:
    """Apply facsimile-checked OCR repairs without duplicating initials."""
    for bad, good in SOURCE_OCR_REPAIRS.items():
        if bad in good and good.endswith(bad):
            prefix = good[:-len(bad)]
            if len(prefix) == 1:
                text = re.sub(
                    rf"(?<!{re.escape(prefix)}){re.escape(bad)}",
                    lambda _match, replacement=good: replacement,
                    text,
                )
                continue
        text = text.replace(bad, good)
    return text


def repair_text(text: str) -> str:
    text = repair_macroman_mojibake(text)
    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        text = text.replace(bad, good)
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u00ad", "")
    text = apply_source_ocr_repairs(text)
    text = re.sub(r"\s*style='mso-tab-count:\s*\d+'\s*&gt;\s*", " ", text, flags=re.I)
    text = text.replace('style="', " ").replace("'&gt;", " ").replace("&gt;", " ")
    return " ".join(text.split())


def extract_html_blocks(path: Path, drop_caps: dict[str, str], segmented: bool) -> tuple[list[str], list[str]]:
    if segmented:
        source = path.read_bytes().decode("cp1252")
        start = source.find("<div ")
        end = source.rfind('<p class="Center"><a')
        if start < 0 or end < 0 or end <= start:
            raise ValueError(f"Cannot isolate source text in {path}")
        source = source[start:end]
    else:
        source = path.read_text(encoding="utf-8")
    parser = BlockParser(drop_caps)
    parser.feed(source)
    parser.flush()
    blocks: list[str] = []
    pending = ""
    for raw in parser.blocks:
        marker = re.fullmatch(r"\[\[DROP:([^\]]+)\]\]", raw.strip())
        if marker:
            if pending:
                raise ValueError(f"Consecutive unresolved initials in {path}: {pending}, {marker.group(1)}")
            pending = drop_caps[marker.group(1)]
            continue

        def replace_drop(match: re.Match[str]) -> str:
            return drop_caps[match.group(1)]

        text = repair_text(re.sub(r"\[\[DROP:([^\]]+)\]\]", replace_drop, raw))
        if pending:
            text = pending + text
            pending = ""
        if text:
            blocks.append(text)
    if pending:
        blocks.append(pending)
    return blocks, parser.drop_cap_uses


# These are source-decoding repairs at ornamental-initial boundaries. Each is
# an unmistakable letter or word-space loss in the CCEL transcription, checked
# against the source PDF rather than silently inferred while building units.
EPUB_BOUNDARY_REPAIRS = {
    "A.nd with thankful songs": "And with thankful songs",
    "A1L! thou, O Queen": "HAIL! thou, O Queen",
    "ACOB bewaileth": "JACOB bewaileth",
    "AFEARFUL and strange": "A FEARFUL and strange",
    "AHELP and protectionhath": "A HELP and protection hath",
    "AKING the command": "TAKING the command",
    "AIL! Virgin": "HAIL! Virgin",
    "ASTER": "MASTER",
    "AVING": "HAVING",
    "AVE mercy": "HAVE mercy",
    "AVE me": "SAVE me",
    "AY thy": "MAY thy",
    "ECOME sharer": "BECOME sharer",
    "E faithful": "YE faithful",
    "E first-throned": "YE first-throned",
    "E glad": "BE glad",
    "E unworthy": "WE unworthy",
    "E bless thee, O God": "WE bless thee, O God",
    "E celebrate": "WE celebrate",
    "E, who": "WE, who",
    "EHOLD": "BEHOLD",
    "ELIVERER of captives": "DELIVERER of captives",
    "EMEMBER me": "REMEMBER me",
    "EMEMBER, O Lord,": "REMEMBER, O Lord,",
    "EMEMBER, O Lord Jesus Christ": "REMEMBER, O Lord Jesus Christ",
    "EARFUL shall be": "FEARFUL shall be",
    "ESUS hath risen": "JESUS hath risen",
    "ET ": "LET ",
    "F thy mysterious": "OF thy mysterious",
    "GAIN and again": "AGAIN and again",
    "HAT ": "WHAT ",
    "HEN thou": "WHEN thou",
    "HEN ": "WHEN ",
    "HEN, ": "WHEN, ",
    "HE assembly": "THE assembly",
    "HE Mid-feast": "THE Mid-feast",
    "HE grace": "THE grace",
    "HE honourable": "THE honourable",
    "HE incarnate": "THE incarnate",
    "HE lawless": "THE lawless",
    "HE Lord": "THE Lord",
    "HE memory": "THE memory",
    "HE more": "THE more",
    "HE mystery": "THE mystery",
    "HE spotless": "THE spotless",
    "HE women": "THE women",
    "HEE": "THEE",
    "HEY": "THEY",
    "HO ": "WHO ",
    "HOUGH": "THOUGH",
    "HOU didst arise": "THOU didst arise",
    "HOU ": "THOU ",
    "HRIST": "CHRIST",
    "HROUGH": "THROUGH",
    "HY ": "THY ",
    "HIS is the chosen": "THIS is the chosen",
    "IM ": "HIM ",
    "LL creation": "ALL creation",
    "LORY": "GLORY",
    "LESSED be our God": "BLESSED be our God",
    "LESSED is the man": "BLESSED is the man",
    "LESSED": "BLESSED",
    "LESS the Lord": "BLESS the Lord",
    "LMIGHTY Lord": "ALMIGHTY Lord",
    "NLY-BEGOTTEN Son": "ONLY-BEGOTTEN Son",
    "NSTRUCTOR of orthodoxy": "INSTRUCTOR of orthodoxy",
    "N Jordan": "IN Jordan",
    "N the vale": "IN the vale",
    "N thee": "IN thee",
    "N thy kingdom": "IN thy kingdom",
    "ND ": "AND ",
    "NGELIC": "ANGELIC",
    "NTO ": "UNTO ",
    "OD ": "GOD ",
    "OBLESSED": "O BLESSED",
    "OARCHANGELS of God": "O ARCHANGELS of God",
    "OBABE, in manger": "O BABE, in manger",
    "OBAPTIST and Forerunner": "O BAPTIST and Forerunner",
    "OCOME, let us": "O COME, let us",
    "OCONSUBSTANTIAL and undivided": "O CONSUBSTANTIAL and undivided",
    "OCHRIST": "O CHRIST",
    "ODIVINE Martyrs": "O DIVINE Martyrs",
    "ODIVINELY wise": "O DIVINELY wise",
    "OGOD-BEARING Virgin": "O GOD-BEARING Virgin",
    "OGOD": "O GOD",
    "OHEAVENLY King": "O HEAVENLY King",
    "OHOLY": "O HOLY",
    "OHOW could Judas": "O HOW could Judas",
    "OIMPIOUS and lawless": "O IMPIOUS and lawless",
    "OMAN, behold": "O MAN, behold",
    "OMOST": "O MOST",
    "OMOTHER of God": "O MOTHER of God",
    "OMY soul": "O MY soul",
    "OPURE Mary": "O PURE Mary",
    "OLORD": "O LORD",
    "OSAVIOUR, Physician": "O SAVIOUR, Physician",
    "OSENTIENT vine": "O SENTIENT vine",
    "OTASTE and see": "O TASTE and see",
    "OTHOU good Lord": "O THOU good Lord",
    "OTHOU": "O THOU",
    "OUNCREATED Nature": "O UNCREATED Nature",
    "OVIRGIN Mother": "O VIRGIN Mother",
    "OVIRGIN": "O VIRGIN",
    "OYE": "O YE",
    "OLY ": "HOLY ",
    "ORD": "LORD",
    "OR I am ready": "FOR I am ready",
    "OST ": "MOST ",
    "OUCHSAFE": "VOUCHSAFE",
    "O thy most pure Icon": "TO thy most pure Icon",
    "O thee, O Virgin": "TO thee, O Virgin",
    "POSTLE beloved": "APOSTLE beloved",
    "POSTLES": "APOSTLES",
    "RANT": "GRANT",
    "RANQUIL Light": "TRANQUIL Light",
    "REAT": "GREAT",
    "RETHREN! Be strong": "BRETHREN! Be strong",
    "RETHREN!": "BRETHREN!",
    "ROM my youth": "FROM my youth",
    "ROPHET and Forerunner": "PROPHET and Forerunner",
    "S equals": "AS equals",
    "T is": "IT is",
    "T that time": "AT that time",
    "T thy fearful": "AT thy fearful",
    "URIED": "BURIED",
    "UR Father, which art": "OUR Father, which art",
    "Y Maker": "MY Maker",
    "Y son": "MY son",
    "Y soul": "MY soul",
    "Y the waters": "BY the waters",
    "Y thoughtful immaterial mind": "BY thoughtful immaterial mind",
    "WO wicked deeds": "TWO wicked deeds",
    "WILL magnify thee exceedingly": "I WILL magnify thee exceedingly",
    "GOD, come to mine assistance": "O GOD, come to mine assistance",
    "MOST holy Trinity": "O MOST holy Trinity",
    "Lord, Giver": "O Lord, Giver",
}

# These repairs become available only after page furniture has been removed and
# a separated ornamental initial is rejoined to its paragraph.
DEFERRED_BOUNDARY_REPAIRS = {
    "AVE, O Lord": "SAVE, O Lord",
    "IKNOW": "I KNOW",
}


# These are narrow OCR corrections checked against the printed facsimile. They
# repair the CCEL transcription without modernising the edition's wording.
SOURCE_OCR_REPAIRS = {
    "(needs greek text Char map won't copy to this page), 1866.":
        "Ἀπόστολος. - ἐν Βενετίᾳ, 1866.",
    "PASC HA": "PASCHA",
    "HOLT PASCHA": "HOLY PASCHA",
    "JULY 2O.": "JULY 20.",
    "A&lt; D.": "A. D.",
    "The Deacon beginneth, ASTER": "The Deacon beginneth, MASTER",
    "HOU, who didst call": "THOU, who didst call",
    "HHAIL!": "HAIL!",
    "AVE , O Lord": "SAVE, O Lord",
    "Santification of Water": "Sanctification of Water",
    "Office for the Load's Day": "Office for the Lord's Day",
    "BBLESS": "BLESS",
    "Vide pape 73": "Vide page 73",
    "LORDER my steps": "ORDER my steps",
    "RETHREN, let us": "BRETHREN, let us",
    "OW the heavenly Powers": "NOW the heavenly Powers",
    "hast aved all men": "hast saved all men",
    "glorified td' ages": "glorified to ages",
    "conlinueth": "continueth",
    "To this end was Iborn": "To this end was I born",
    "the eaith did quake": "the earth did quake",
    "the Creater of all things": "the Creator of all things",
    "Stickera": "Stichera",
    "CCEPT our evening prayers": "ACCEPT our evening prayers",
    "bfessed": "blessed",
    "ProMmenon": "Prokimenon",
    "whicn": "which",
    "3I8 God-bearing Fathers": "318 God-bearing Fathers",
    "Niccea": "Nicæa",
    "thou dist arise": "thou didst arise",
    "earth ofFereth": "earth offereth",
    "go to greet' him": "go to greet him",
    "sigKt": "sight",
    "could beai": "could bear",
    "giving -bjrth": "giving-birth",
    "ThreeDivines": "Three Divines",
    "LukeXXI.": "Luke XXI.",
    "1Oth": "10th",
    "c. 2r.": "c. 21.",
    "c. 1O.": "c. 10.",
    "Bp.ofCyzicum": "Bp. of Cyzicum",
    "HONOUR ABLE": "HONOURABLE",
    "Luke XXV": "Luke XXIV.",
    "3O. Sun. 17 aft. Pent.": "Sun. 17 aft. Pent.",
    "be-fore": "before",
    "Sun-day": "Sunday",
    "Pro-digal": "Prodigal",
    "Sept. 2I.": "Sept. 21.",
    "b. ig.": "b. 19.",
    "Men. 26.": "Mch. 26.",
    "OO Lord, Giver": "O Lord, Giver",
    "ROM soiled lips": "FROM soiled lips",
    "HOU, our God-bearing": "THOU, our God-bearing",
    "F into the tomb": "IF into the tomb",
    "E that is pious": "HE that is pious",
    "II God be merciful": "II. God be merciful",
    "re ward me": "reward me",
    "Hal-lowed": "Hallowed",
    "aud all ye": "and all ye",
    "temptations\n\nTHE LITTLE DAILY VESPERS.\n\nand imaginings":
        "temptations and imaginings",
    "advo-cates": "advocates",
    "(\\afi)": "(146)",
    "Christ- mas": "Christmas",
    "Anti-phons": "Antiphons",
    "18 th.": "18th.",
    "pur- suer": "pursuer",
    "aw-ful": "awful",
    "Corn ointilled": "Corn untilled",
    "bod)'": "body",
    "nour-isheth": "nourisheth",
    "ex claimed": "exclaimed",
    "vest- ments": "vestments",
    "fol-loweth": "followeth",
    "Tropar-ion": "Troparion",
    "be- stoweth": "bestoweth",
    "enterelh": "entereth",
    "Paschd": "Pascha",
    "deatfi": "death",
    "Sty lite": "Stylite",
    "IIth": "11th",
    "Theo-dulus": "Theodulus",
    "BBBBRETHREN": "BRETHREN",
    "NNNNOW": "NOW",
    "FFFFROM": "FROM",
    "TTTTHOU": "THOU",
    "AAAACCEPT": "ACCEPT",
    "IIIIF": "IF",
    "HHHHE": "HE",
    "TTTHOU": "THOU",
    "TTHOU": "THOU",
    "all ye\n\nTHE LITTLE DAILY VESPERS.\n\nSaints": "all ye Saints",
    "sing and\n\nTHE LITTLE DAILY VESPERS. 6l worship": "sing and worship",
    "me,\n\n48 NOCTURNS\n\nO my God": "me, O my God",
    "O Christ\n\nTHE GT. MATINS WHEN NO VIGIL HELD. 53 our God.":
        "O Christ our God.",
    "Father,\n\nTHE GT. MATINS WHEN NO VIGIL HELD.\n\nSon": "Father, Son",
    "statutes.\n\nTHE GREAT COMPLINE.\n\nO Lord": "statutes. O Lord",
    "my\n\nTHE DAILY NOCTURNS.\n\nrefuge": "my refuge",
    "THE DAILY NOCTURNS.\n\n": "",
    "of the\n\nTHE DAILY MATINS.\n\nVirgin": "of the Virgin",
    "58(59)-60(51)": "58(59)-60(61)",
    "he hath\n\nTR0PAR1A ETC. FOR FESTIVALS. 453 chosen": "he hath chosen",
    "nuirfber of evils": "number of evils",
    "undi- vided": "undivided",
    "Sun- day": "Sunday",
    "Re- membrance": "Remembrance",
    "An- gels": "Angels",
    "accord- ing": "according",
    "un- worthily": "unworthily",
    "for- he is holy": "for he is holy",
    "Psalm 50 (5I)": "Psalm 50 (51)",
    "Vide page I2": "Vide page 12",
    "Vide page I0": "Vide page 10",
    "Vide page I48": "Vide page 148",
    "Vide page I29": "Vide page 129",
    "Vide page IO": "Vide page 10",
    "Vide page 26I": "Vide page 261",
    "Vide page I45": "Vide page 145",
    "Vide page 6I": "Vide page 61",
    "Ist.": "1st.",
    "Tone l is sung": "Tone 1 is sung",
    "Qiurch": "Church",
    "Chariion": "Chariton",
    "Aber-cius": "Abercius",
    "Ex-acustodianus": "Exacustodianus",
    "Diony-sius": "Dionysius",
    "Pres byter": "Presbyter",
    "Amphi-lochius": "Amphilochius",
    "Athan-asius": "Athanasius",
    "Strato-nicus": "Stratonicus",
    "Martys, Eugene": "Martyrs, Eugene",
    "Hyp-atius": "Hypatius",
    "A. D. 541. 33*": "A. D. 541.",
    "Damiah": "Damian",
    "Araastrida": "Amastrida",
    "the-Apostles": "the Apostles",
    "Pro-chorus": "Prochorus",
    "Michseus": "Michæus",
    "Theodostus": "Theodosius",
    "OCOME, ye people": "O COME, ye people",
    "for it burned\n\nVII.\n\nnot the Youths": "for it burned not the Youths",
    "destroying and scattering its powers Hades is held bound":
        "destroying and scattering its powers. Hades is held bound",
    "Abba-cum": "Abbacum",
    "An-tiphon": "Antiphon",
    "Be-lievest": "Believest",
    "Con-dakion": "Condakion",
    "Caia-phas": "Caiaphas",
    "Draw-nigh": "Draw nigh",
    "Im-mortal": "Immortal",
    "Nico-demus": "Nicodemus",
    "Noc-turns": "Nocturns",
    "Pro-kimenon": "Prokimenon",
    "Tro-paria": "Troparia",
    "accord-ing": "according",
    "an-swereth": "answereth",
    "be-ginneth": "beginneth",
    "consi-dereth": "considereth",
    "de-liver": "deliver",
    "end-ing": "ending",
    "fruit-lessness": "fruitlessness",
    "in-comparable": "incomparable",
    "me-diatress": "mediatress",
    "remem-berest": "rememberest",
    "re-generateth": "regenerateth",
    "re-pentance": "repentance",
    "un-defiled": "undefiled",
    "un-taken": "untaken",
    "deceit-fulness": "deceitfulness",
    "anti-phonally": "antiphonally",
    "be-trayeth": "betrayeth",
    "im-movable": "immovable",
    "in corruptible": "incorruptible",
    "Pas-sion": "Passion",
    "one Godhead, one Might I be gracious":
        "one Godhead, one Might! be gracious",
    "thou sands": "thousands",
    "disiributeth": "distributeth",
    "com panions": "companions",
    "A, D. 1334": "A. D. 1334",
    "Presanctified": "Pre-sanctified",
    "evervirgin": "ever-virgin",
    "bloodguiltiness": "blood-guiltiness",
    "Godfearing": "God-fearing",
    "longsuffering": "long-suffering",
    "divinebride": "divine-bride",
    "lifeeffecting": "life-effecting",
    "Priestmartyr": "Priest-martyr",
    "rightbelieving Princes": "right-believing Princes",
    "Tro-parion": "Troparion",
    "unbe-ginning": "unbeginning",
    "Un-beginning": "Unbeginning",
    "re-joiceth": "rejoiceth",
    "be-stoweth": "bestoweth",
}


# The EPUB inserts page breaks, running footnotes, and column boundaries as
# paragraph breaks. These facsimile-checked groups are continuous source
# paragraphs. Numbers are one-based within the finished unit before joining.
UNIT_PARAGRAPH_JOIN_GROUPS = {
    "c01-u02": (
        (84, 85), (87, 88), (89, 90, 91), (93, 94, 95, 96),
        (172, 173), (110, 116), (115, 117),
    ),
    "c05-u01": ((6, 7),),
    "c06-u01": ((85, 86), (88, 89)),
    "c08-u01": ((37, 38),),
    "c09-u01": ((34, 35), (46, 47, 48), (53, 54), (111, 112), (113, 114)),
    "c11-u01": ((5, 6),),
    "c15-u01": ((138, 139),),
    "c16-u01": ((34, 35),),
    "c17-u02": ((14, 15),),
    "c18-u02": ((15, 16),),
    "c18-u03": ((4, 5), (10, 11)),
    "c19-u03": ((21, 22),),
    "c20-u02": ((8, 9, 10),),
    "c20-u06": ((4, 5),),
    "c20-u20": ((52, 53), (59, 60), (226, 227), (232, 233)),
    "c20-u24": ((24, 25, 26),),
    "c20-u27": ((31, 32), (59, 60), (66, 67)),
    "c20-u28": ((69, 71),),
    "c21-u01": ((83, 84),),
    "c21-u14": ((15, 16), (17, 18), (23, 24, 25), (26, 27), (32, 33)),
    "c22-u05": ((6, 7),),
    "c24-u11": ((6, 7), (11, 12, 13), (17, 18)),
    "c24-u21": ((3, 4),),
    "c28-u02": ((19, 20),),
}


# Prefix-only repairs cannot live in SOURCE_OCR_REPAIRS because a global
# substring replacement is not idempotent: ON contains N, and IN contains N.
PARAGRAPH_PREFIX_REPAIRS = {
    "N the morrow that followeth": "ON the morrow that followeth",
    "N the tomb bodily": "IN the tomb bodily",
    "N the beginning was the Word": "IN the beginning was the Word",
    "HE grave being open": "THE grave being open",
    "HE Life is placed": "THE Life is placed",
    "HE enemy found me": "THE enemy found me",
    "HE earth is the Lord's": "THE earth is the Lord's",
    "HE former treatise": "THE former treatise",
    "O-DAY": "TO-DAY",
    "LORD, rebuke me not": "O LORD, rebuke me not",
    "LORD, hear my prayer": "O LORD, hear my prayer",
    "GOD, my God, for thee do I watch": "O GOD, my God, for thee do I watch",
    "RAISE ye the name of the Lord": "PRAISE ye the name of the Lord",
    "BELIEVE in one God, the Father": "I BELIEVE in one God, the Father",
    "LORD almighty, God of our fathers": "O LORD almighty, God of our fathers",
    "LORD, forgive them that hate": "O LORD, forgive them that hate",
    "BELIEVE, Lord, and confess": "I BELIEVE, Lord, and confess",
    "SAVIOUR, when thou wast risen": "O SAVIOUR, when thou wast risen",
    "THINK of the terrible day": "I THINK of the terrible day",
    "BELIEVED, and therefore": "I BELIEVED, and therefore",
    "Lord Jesus Christ our God, Source": "O Lord Jesus Christ our God, Source",
    "KNOW, O Lord my God": "I KNOW, O Lord my God",
    "KNOW, O Lord, that I receive": "I KNOW, O Lord, that I receive",
    "CHRIST my God, as though": "O CHRIST my God, as though",
    "LORD Jesus Christ our God, who alone": "O LORD Jesus Christ our God, who alone",
    "GOD, loosen, remit": "O GOD, loosen, remit",
    "LORD and God, I am not worthy": "O LORD and God, I am not worthy",
    "LORD Jesus Christ my God, loosen": "O LORD Jesus Christ my God, loosen",
    "STAND before the gates": "I STAND before the gates",
    "BELIEVE, O Lord, and confess": "I BELIEVE, O Lord, and confess",
    "THANK thee, O Lord my God": "I THANK thee, O Lord my God",
    "LORD Christ our God, King": "O LORD Christ our God, King",
    "THOU who, of thine own good will": "O THOU who, of thine own good will",
    "MOST holy Mother of God, light": "O MOST holy Mother of God, light",
    "THOU Creator, who in the depth": "O THOU Creator, who in the depth",
    "WONDERWORKING Gregory": "O WONDERWORKING Gregory",
    "CHRIST God, thou didst, before thy": "O CHRIST God, thou didst, before thy",
    "WILL bless the Lord at all times": "I WILL bless the Lord at all times",
    "GOD, save thy people": "O GOD, save thy people",
    "MOTHER of God, thou art": "O MOTHER of God, thou art",
    "GOD and Lord of hosts": "O GOD and Lord of hosts",
    "LORD, when the thrones": "O LORD, when the thrones",
    "RISE! Master": "ARISE! Master",
    "THOU Virgin, spotless": "O THOU Virgin, spotless",
    "COME ye all, and let us sing him": "O COME ye all, and let us sing him",
    "CHRIST, the Life of all things": "O CHRIST, the Life of all things",
    "ALL ye works of the Lord": "O ALL ye works of the Lord",
    "LORD God of my salvation": "O LORD God of my salvation",
    "HEAVENLY King, O Paraclete": "O HEAVENLY King, O Paraclete",
    "LORD, save thy people": "O LORD, save thy people",
}


# The edition's own errata are applied to the body, while the Errata leaf is
# retained verbatim as part of the published front matter.
EDITION_ERRATA_REPAIRS = {
    "siek": "sick",
    "plenteons": "plenteous",
    "remaining time of our life may he spent": "remaining time of our life may be spent",
    "desolute": "desolate",
    "occassion": "occasion",
    "according io": "according to",
    "Thee that all the earth-born sing": "Thou that all the earth-born sing",
    "of the Virgin unspeakably became incarnate, even Christ the Life-giver, whom with fear":
        "of the Virgin unspeakably become incarnate, even Christ the Life-giver, with fear",
    "Who for us men, and for our salvation, come down from the heavens":
        "Who for us men, and for our salvation, came down from the heavens",
    "strenghtened": "strengthened",
    "As o Monday": "As on Monday",
    "God-head": "Godhead",
    "The following Antiphons may however be substituted.":
        "The following Antiphons may however be substituted on Week Days.",
    "because be hath heard": "because he hath heard",
    "hand-maiden": "handmaiden",
    "(or, hand-maid)": "(or, handmaid)",
    "salvaton": "salvation",
    "jugdment": "judgment",
    "aquaintance": "acquaintance",
    "falsely accused hy roaming sinners": "falsely accused by roaming sinners",
    "the stone sealed hy hands": "the stone sealed by hands",
    "annointed": "anointed",
    "suffered fcr the faith": "suffered for the faith",
    "ceaslessly": "ceaselessly",
}


def repair_epub_boundary(text: str) -> tuple[str, str | None]:
    for old, new in {**EPUB_BOUNDARY_REPAIRS, **DEFERRED_BOUNDARY_REPAIRS}.items():
        if text.startswith(old):
            return new + text[len(old):], old
    return text, None


def join_paragraph_parts(parts: list[str]) -> str:
    joined = parts[0]
    for part in parts[1:]:
        if joined.endswith("-") and part[:1].islower():
            joined = joined[:-1] + part
        else:
            joined += " " + part
    return joined


def repair_unit_paragraphs(unit: dict) -> int:
    suffix = unit["unit_id"].split("::", 1)[1]
    groups = UNIT_PARAGRAPH_JOIN_GROUPS.get(suffix)
    if not groups:
        return 0
    paragraphs = unit["text"].split("\n\n")
    removals: set[int] = set()
    anchors: set[int] = set()
    joins = 0
    for one_based_group in groups:
        indexes = [number - 1 for number in one_based_group]
        if any(index < 0 or index >= len(paragraphs) for index in indexes):
            raise ValueError(
                f"Paragraph join index drifted for {unit['unit_id']}: "
                f"{one_based_group} of {len(paragraphs)}"
            )
        anchor = indexes[0]
        consumed = set(indexes[1:])
        if anchor in anchors or anchor in removals or consumed & (anchors | removals):
            raise ValueError(
                f"Overlapping paragraph joins for {unit['unit_id']}: {one_based_group}"
            )
        paragraphs[anchor] = join_paragraph_parts([paragraphs[index] for index in indexes])
        anchors.add(anchor)
        removals.update(consumed)
        joins += len(indexes) - 1
    unit["text"] = "\n\n".join(
        paragraph for index, paragraph in enumerate(paragraphs)
        if index not in removals
    )
    return joins


def join_source_initial(initial: str, following: str) -> str:
    if following.startswith("A1L"):
        following = "AIL" + following[3:]
    if following.startswith("AV1NG"):
        following = "AVING" + following[5:]
    if following.startswith("ORB1D"):
        following = "ORBID" + following[5:]
    if initial == "I" and re.match(r"^(HAVE|BELIEVE|CRIED)\b", following):
        joined = initial + " " + following
    else:
        joined = initial + following
    if joined.startswith("TODAY"):
        joined = "TO-DAY" + joined[5:]
    return joined


def extract_epub_blocks(path: Path) -> tuple[list[str], int, int]:
    """Decode the CCEL EPUB and rejoin its separately encoded initials."""
    source = path.read_text(encoding="utf-8")
    parser = BlockParser()
    parser.feed(source)
    parser.flush()
    decoded = [repair_text(raw) for raw in parser.blocks if repair_text(raw)]
    chapter_xxvii = next(i for i, block in enumerate(decoded) if block.startswith("XXVII. OF THE RECITATION"))
    blocks: list[str] = []
    initial_joins = 0
    boundary_repairs: set[str] = set()
    index = 0
    while index < len(decoded):
        block = decoded[index]
        following = decoded[index + 1] if index + 1 < len(decoded) else ""
        is_initial = bool(re.fullmatch(r"[A-Z]", block))
        is_word_tail = bool(
            re.match(r"^[a-z]", following)
            or re.match(r"^[A-Z]{2,}", following)
            or re.match(r"^[A-Z](?:\s|[-!?,.;:])", following)
        )
        if index < chapter_xxvii and is_initial and is_word_tail:
            joined = join_source_initial(block, following)
            repaired, repair_key = repair_epub_boundary(joined)
            if repair_key:
                boundary_repairs.add(repair_key)
            blocks.append(repaired)
            initial_joins += 1
            index += 2
            continue
        repaired, repair_key = repair_epub_boundary(block)
        if repair_key:
            boundary_repairs.add(repair_key)
        blocks.append(repaired)
        index += 1
    missing = set(EPUB_BOUNDARY_REPAIRS) - boundary_repairs
    if missing:
        raise ValueError(f"Expected EPUB boundary repairs were not found: {sorted(missing)}")
    return blocks, initial_joins, len(boundary_repairs)


def is_marker(block: str, choices: tuple[str, ...]) -> bool:
    upper = block.upper().strip()
    return any(upper.startswith(choice) for choice in choices)


def locate_chapters(blocks: list[str]) -> dict[int, int]:
    positions: dict[int, int] = {}
    cursor = 0
    order = list(range(1, 31))
    for number in order:
        found = next((
            i for i in range(cursor, len(blocks))
            if any(blocks[i].strip().startswith(choice) for choice in MAIN_MARKERS[number])
        ), None)
        if found is None:
            raise ValueError(f"Chapter {number} not found")
        positions[number] = found
        cursor = found + 1
    return positions


def fallback_chapters(drop_caps: dict[str, str]) -> tuple[dict[int, list[str]], int]:
    blocks, _ = extract_html_blocks(SOURCE_DIR / "epub-body.xhtml", {}, segmented=False)
    positions: dict[int, int] = {}
    cursor = 0
    for number in [7, 8, 9, 10]:
        marker = FALLBACK_MARKERS[number]
        found = next((i for i in range(cursor, len(blocks)) if blocks[i].upper().startswith(marker)), None)
        if found is None:
            raise ValueError(f"EPUB fallback chapter {number} not found")
        positions[number] = found
        cursor = found + 1
    result = {
        7: blocks[positions[7] + 1:positions[8]],
        8: blocks[positions[8] + 1:positions[9]],
        9: blocks[positions[9] + 1:positions[10]],
    }
    expected_repairs = {
        "GOD, come to mine assistance": ("O GOD, come to mine assistance", "0112=82-2.jpg"),
        "EHOLD the Bridegroom": ("BEHOLD the Bridegroom", "0115=85-2.jpg"),
        "E bless thee, O God": ("WE bless thee, O God", "0119=89-1.jpg"),
        "WILL magnify thee exceedingly": ("I WILL magnify thee exceedingly", "0119=89-2.jpg"),
        "EMEMBER, O Lord, our fathers": ("REMEMBER, O Lord, our fathers", "0122=92-1.jpg"),
        "Y thoughtful immaterial mind": ("BY thoughtful immaterial mind", "0125=95-1.jpg"),
    }
    repaired = 0
    for chapter_blocks in result.values():
        for index, block in enumerate(chapter_blocks):
            for old, (new, image_name) in expected_repairs.items():
                if block.startswith(old):
                    if drop_caps[image_name] != new[0]:
                        raise ValueError(f"Drop cap map disagrees for {image_name}")
                    chapter_blocks[index] = new + block[len(old):]
                    repaired += 1
    if repaired != len(expected_repairs):
        raise ValueError(f"Expected {len(expected_repairs)} EPUB initial repairs, found {repaired}")
    joined_glyphs = sum(
        1 for chapter_blocks in result.values() for block in chapter_blocks
        if block.startswith("OUNCREATED Nature") or block.startswith("REMEMBER thy servants")
    )
    if joined_glyphs != 2:
        raise ValueError(f"Expected 2 encoded EPUB initials, found {joined_glyphs}")
    return result, repaired + joined_glyphs


def strip_chapter_heading(number: int, blocks: list[str]) -> list[str]:
    blocks = blocks[1:]
    continuation_counts = {
        1: 3, 2: 1, 4: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 2,
        20: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 30: 1,
    }
    return blocks[continuation_counts.get(number, 0):]


RUNNING_HEADER = (
    r"(?:THE ALL-NIGHT VIGIL|THE GREAT VESPERS|THE GREAT MATINS|THE GREAT COMPLINE|"
    r"THE DAILY MATINS|THE FIRST HOUR, OR PRIME|THE THIRD HOUR, OR TERCE|"
    r"THE SIXTH HOUR, OR SEXT|THE NINTH HOUR, OR NONE|THE TYPICA|"
    r"CALLED, THE TYPICA|THE PRO-LITURGY(?:-| )SERVICE|AT THE LITURGIES(?: ETC)?|"
    r"OF SAINTS CHRYSOSTOM AND BASIL|AT THE LITURGY(?: ETC)?|"
    r"OF THE PRE-SANCTIFIED|AT VESPERS ON HOLY PASCHA|"
    r"THE MATINS ON HOLY PASCHA|THE HOURS ON HOLY PASCHA|"
    r"EXTRACTS FROM THE (?:LENTEN|FERIAL) TRIOD[1I]ON|"
    r"KXTB\.ACTS FROM THE FERIAL TRIODION)[.,]?"
)
OCR_PAGE_TOKEN = r"[0-9IOlqA*%.-]{1,8}"


def strip_running_header(text: str) -> str:
    """Remove page furniture fused to a continued line by the CCEL OCR."""
    if text.startswith("A. THE TYPICA"):
        return text
    patterns = (
        rf"^{RUNNING_HEADER}\s+{OCR_PAGE_TOKEN}(?:\s+|$)",
        rf"^{OCR_PAGE_TOKEN}\s+{RUNNING_HEADER}(?:\s+|$)",
    )
    result = text
    for pattern in patterns:
        result = re.sub(pattern, "", result, count=1, flags=re.I)
    result = re.sub(r"^(?:AT THE LITURGY|AT THE LITURGIES)\s+(?=[a-z])", "", result)
    return result.strip()


def is_page_noise(block: str, preserve_numbers: bool = False) -> bool:
    text = block.strip()
    if text.upper() == "A. PRAYERS BEFORE HOLY COMMUNION." or text.upper().startswith("A. THE TYPICA"):
        return False
    if not preserve_numbers and re.fullmatch(r"(?:[0-9IOl]+[A-Z*]?|[ivxlcdm]+)", text, re.I):
        return True
    upper = text.upper()
    running_phrases = (
        "SUNDAY SERVICE", "IN THE SIXTH TONE", "PENITENTIAL SERVICE",
        "TO OUR LORD JESUS CHRIST", "PRAYERS BEFORE HOLY COMMUNION",
        "THANKSGIVINGS AFTER HOLY COMMUNION", "EXTRACTS FROM THE LENTEN TRIODION",
        "EXTRACTS FROM THE FERIAL TRIODION", "THE PASSION OF THE LORD",
        "THE HOURS ON HOLY FRIDAY", "AT VESPERS ON HOLY FRIDAY",
        "AT MATINS ON HOLY SATURDAY", "THE MATINS ON HOLY PASCHA",
        "THE HOURS ON HOLY PASCHA",
        "SUNDAY TROPARIA", "TROPARIA ETC. FOR", "TROPARIA AND CONDAKIA",
        "COMMON FOR THE SAINTS", "DIPTYCHS", "OR REMEMBRANCER",
        "TABLE OF LESSONS", "THE KALENDAR", "AN ALMANACK FOR FIFTY YEARS",
    )
    if any(phrase in upper for phrase in running_phrases) and (
        re.search(r"\d", upper) or "STYLE=" in upper or "&GT;" in upper
    ):
        return True
    if upper in {
        "EXTRACTS FROM THE LENTEN TRIODION.", "EXTRACTS FROM THE FERIAL TRIODION.",
        "TROPARIA ETC. FOR FESTIVALS.", "COMMON FOR THE SAINTS.",
        "DIPTYCHS,", "OR REMEMBRANCER.", "THE KALENDAR.",
        "AT THE LITURGY", "AT THE LITURGIES", "OF THE PRE-SANCTIFIED.",
    }:
        return True
    if re.fullmatch(r"\d+\s+.+\s+\d+", upper) and any(word in upper for word in ("THE ", "EXTRACTS", "TROPARIA", "PRAYERS", "DIPTYCHS", "COMMON")):
        return True
    if re.search(r"\s+\d+$", upper) and any(upper.startswith(prefix) for prefix in (
        "THE GREAT", "THE DAILY", "THE LITTLE", "THE FIRST", "THE THIRD", "THE SIXTH",
        "THE NINTH", "THE PASSION", "AT VESPERS", "AT MATINS", "OF SAINTS", "ON SUNDAYS",
        "IN THE SIXTH", "COMMON FOR", "PRAYERS BEFORE", "THANKSGIVINGS AFTER", "SUNDAY TROPARIA",
        "TROPARIA ETC", "EXTRACTS FROM", "AN ALMANACK", "TABLE OF LESSONS",
    )):
        return True
    if re.match(r"^[0-9IOlqA*%.-]{2,8}\s+", upper) and any(phrase in upper for phrase in (
        "THE ALL-NIGHT", "THE NOCTURNS", "THE LITTLE", "THE GREAT", "THE DAILY", "AT THE LITURGY",
        "SUNDAY SERVICE", "PENITENTIAL SERVICE", "PRAYERS BEFORE", "THANKSGIVINGS AFTER",
        "EXTRACTS FROM", "TROPARIA", "DIPTYCHS",
    )):
        return True
    if re.match(
        r"^[0-9IOlqA*%.-]+\s+(?:THK ALL-NIGHT VIGIL|PRATERS BEFORE HOLY COMMUNION|"
        r"TROPAR1A ETC\. FOR FESTIVALS)\.?$",
        upper,
    ):
        return True
    if re.fullmatch(r"THB GREAT COMPLINE\.?(?:\s+[0-9IO]+)?", upper):
        return True
    if re.fullmatch(r"[0-9IO]+\s+THK ALL-NIGHT VLGIL\.?", upper):
        return True
    return False


def canonical_section_heading(chapter: int, block: str) -> str | None:
    text = block.strip()
    upper = text.upper()
    if len(text) > 220:
        return None
    if chapter == 1 and upper in {"THE GREAT VESPERS.", "THE GREAT MATINS."}:
        return text
    if chapter == 14 and re.match(r"^[AB]\. THE TYPICA", upper):
        return text
    if chapter == 15 and re.match(r"^[AB]\. THE LITURGY OF THE", upper):
        return text
    if chapter == 17 and upper in {"AT THE GREAT VESPERS.", "AT THE GREAT MATINS.", "THE CANON ON THE RESURRECTION.", "AT THE LITURGY."}:
        return text
    if chapter == 18 and upper in {"AT VESPERS.", "AT MATINS.", "AT LITURGY."}:
        return text
    if chapter == 19 and (re.match(r"^[AB]\. PRAYERS", upper) or upper.startswith("ON THE MORROW, THE USUAL OFFICE")):
        return text
    if chapter in {20, 21} and upper == text and upper.startswith((
        "ON THE ", "ON HOLY ", "ON THURSDAY ", "ON SATURDAY ", "AT VESPERS ", "AT MATINS ",
        "THE HOURS ", "THE FIRST HOUR", "THE THIRD HOUR", "THE SIXTH HOUR", "THE NINTH HOUR", "THE MATINS ON",
    )):
        return text
    if chapter == 20 and upper == "THE PASSION OF THE LORD.":
        return text
    if chapter == 22:
        match = re.search(r"TONE\s+([1-8]|I{1,3}|IV|V|VI{0,3})", upper)
        if match and (upper.startswith("TONE") or "SUNDAY TROPARIA" in upper):
            return "TONE " + match.group(1) + "."
    if chapter == 23 and upper == text and re.match(r"^ON (MONDAYS|TUESDAYS|WEDNESDAYS|THURSDAYS|FRIDAYS|SATURDAYS)\.", upper):
        return text
    if chapter == 24 and upper == text and re.match(r"^(SEP\.|OCT\.|NOV\.|DEC\.|JAN\.|FEB\.|MARCH|APRIL|MAY|JUNE|JULY|AUG\.)\s+", upper):
        return text
    if chapter == 25 and upper == text and upper.startswith("FOR "):
        return text
    if chapter == 26 and upper == "FOR THE DEPARTED.":
        return text
    if chapter == 27 and upper in {"TABLE I.", "TABLE II."}:
        return text
    if chapter == 28 and upper in {"AT LITURGY", "AT MATINS."}:
        return text
    if chapter == 29 and upper in {"SEPTEMBER.", "OCTOBER.", "NOVEMBER.", "DECEMBER.", "JANUARY.", "FEBRUARY.", "MARCH.", "APRIL.", "MAY.", "JUNE.", "JULY.", "AUGUST."}:
        return text
    return None


CHAPTER_23_HEADINGS = (
    "ON MONDAYS. TO THE ANGELS.",
    "ON TUESDAYS. TO THE FORERUNNER.",
    "ON WEDNESDAYS. TO THE MOTHER OF GOD AT THE CROSS.",
    "ON THURSDAYS. TO THE APOSTLES, AND TO NICOLAS THE WONDERWORKER.",
    "ON FRIDAYS. TO THE HOLY CROSS.",
    "ON SATURDAYS. TO ALL SAINTS, AND FOR THE DEPARTED.",
)

CHAPTER_25_HEADINGS = (
    "FOR A VENERABLE WOMAN MARTYR.", "FOR A VENERABLE MARTYR.",
    "FOR VENERABLE MARTYRS.", "FOR A VENERABLE WOMAN.",
    "FOR VENERABLE WOMEN.", "FOR A PRIEST-MARTYR", "FOR PRIEST-MARTYRS.",
    "FOR A WOMAN MARTYR.", "FOR WOMEN MARTYRS.", "FOR THE UNMERCENARY.",
    "FOR AN APOSTLE.", "FOR APOSTLES.", "FOR A DIVINE.", "FOR DIVINES.",
    "FOR A VENERABLE.", "FOR VENERABLES.", "FOR A MARTYR.", "FOR MARTYRS.",
    "FOR A CONFESSOR.", "FOR PROPHETS.",
)


def split_embedded_heading(chapter: int, block: str) -> tuple[str | None, str]:
    headings: tuple[str, ...] = ()
    if chapter == 23:
        headings = CHAPTER_23_HEADINGS
    elif chapter == 25:
        headings = CHAPTER_25_HEADINGS
    for heading in headings:
        if block.startswith(heading):
            return heading, block[len(heading):].strip()
    return None, block


def is_all_caps_line(text: str) -> bool:
    return bool(re.search(r"[A-Z]", text)) and text.upper() == text


def merge_multiline_headings(chapter: int, blocks: list[str]) -> list[str]:
    if chapter not in {14, 20, 21, 23, 24}:
        return blocks
    result: list[str] = []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if (
            chapter == 14
            and block == "A. THE TYPICA IN THE GREAT"
            and index + 1 < len(blocks)
            and blocks[index + 1] == "FASTS."
        ):
            result.append("A. THE TYPICA IN THE GREAT FASTS.")
            index += 2
            continue
        if (
            chapter == 23
            and block == "ON SATURDAYS. TO ALL SAINTS, AND"
            and index + 1 < len(blocks)
            and blocks[index + 1].startswith("FOR THE DEPARTED.")
        ):
            following = blocks[index + 1]
            result.append("ON SATURDAYS. TO ALL SAINTS, AND FOR THE DEPARTED.")
            remainder = following[len("FOR THE DEPARTED."):].strip()
            if remainder:
                result.append(remainder)
            index += 2
            continue
        starts_heading = False
        if chapter in {20, 21}:
            starts_heading = bool(re.match(r"^(?:ON |AT |THE MATINS$|THE HOURS )", block))
        elif chapter == 23:
            starts_heading = block == "ON SATURDAYS. TO ALL SAINTS, AND"
        elif chapter == 24:
            starts_heading = bool(re.match(r"^(?:SEP\.|OCT\.|NOV\.|DEC\.|JAN\.|FEB\.|MARCH|APRIL|MAY|JUNE|JULY|AUG\.)\s+", block))
        if not starts_heading or not is_all_caps_line(block):
            result.append(block)
            index += 1
            continue
        pieces = [block]
        cursor = index + 1
        while cursor < len(blocks) and len(" ".join(pieces)) < 320:
            following = blocks[cursor]
            if not is_all_caps_line(following):
                break
            if chapter in {20, 21} and re.match(r"^(?:ON |AT |THE HOURS |THE FIRST HOUR|THE THIRD HOUR|THE SIXTH HOUR|THE NINTH HOUR)", following):
                break
            if chapter == 24 and re.match(r"^(?:SEP\.|OCT\.|NOV\.|DEC\.|JAN\.|FEB\.|MARCH|APRIL|MAY|JUNE|JULY|AUG\.)\s+", following):
                break
            pieces.append(following)
            cursor += 1
        result.append(" ".join(pieces))
        index = cursor
    return result


def rejoin_orphan_initials(blocks: list[str]) -> tuple[list[str], int]:
    result: list[str] = []
    joins = 0
    index = 0
    while index < len(blocks):
        block = blocks[index]
        following = blocks[index + 1] if index + 1 < len(blocks) else ""
        if re.fullmatch(r"[A-Z]", block) and following and (
            re.match(r"^[a-z]", following)
            or re.match(r"^[A-Z]{2,}", following)
            or re.match(r"^[A-Z](?:\s|[-!?,.;:])", following)
        ):
            joined = join_source_initial(block, following)
            repaired, _ = repair_epub_boundary(joined)
            result.append(repaired)
            joins += 1
            index += 2
            continue
        result.append(block)
        index += 1
    placements = {
        "O": (
            ("COME, let us", "O COME, let us"),
            ("LORD, thou", "O LORD, thou"),
            ("GOD, almighty", "O GOD, almighty"),
            ("CHRIST, the Peace", "O CHRIST, the Peace"),
            ("MOST pure", "O MOST pure"),
            ("YE works", "O YE works"),
        ),
        "T": (
            ("TO thee, O Virgin", "TO thee, O Virgin"),
            ("O thee, O Virgin", "TO thee, O Virgin"),
            ("O-DAY", "TO-DAY"),
            ("HE fool", "THE fool"),
            ("TTHOU", "THOU"),
            ("HOU, who didst call", "THOU, who didst call"),
            ("THE ", "THE "), ("THEE ", "THEE "), ("THEE,", "THEE,"), ("THEY ", "THEY "),
            ("THOU ", "THOU "), ("THOU,", "THOU,"),
            ("THIS ", "THIS "), ("THROUGH ", "THROUGH "),
        ),
        "B": (("BLESSED ", "BLESSED "), ("BEHOLD ", "BEHOLD ")),
        "F": (("FEARFUL ", "FEARFUL "), ("FOR ", "FOR ")),
        "G": (("OD is gone up", "GOD is gone up"), ("GOD is gone up", "GOD is gone up")),
        "H": (("E was brought out", "HE was brought out"), ("HIM ", "HIM "), ("HOLY ", "HOLY ")),
        "J": (("JACOB ", "JACOB "), ("JESUS ", "JESUS ")),
        "S": (("SAVE ", "SAVE "), ("SAVE,", "SAVE,"), ("AVE, O Lord", "SAVE, O Lord")),
        "W": (("WHO ", "WHO "),),
    }
    removed: set[int] = set()
    for index, initial in enumerate(result):
        if initial == "'3":
            removed.add(index)
            joins += 1
            continue
        choices = placements.get(initial)
        if not choices:
            continue
        target_index = None
        replacement = None
        prefix = None
        for cursor in range(index + 1, min(index + 7, len(result))):
            for candidate_prefix, candidate_replacement in choices:
                if result[cursor].startswith(candidate_prefix):
                    target_index = cursor
                    prefix = candidate_prefix
                    replacement = candidate_replacement
                    break
            if target_index is not None:
                break
        if target_index is None or prefix is None or replacement is None:
            continue
        result[target_index] = replacement + result[target_index][len(prefix):]
        removed.add(index)
        joins += 1
    return [block for position, block in enumerate(result) if position not in removed], joins


def audit_source_images(drop_caps: dict[str, str]) -> tuple[int, int, int, int]:
    image_occurrences: list[str] = []
    image_refs: set[str] = set()
    probable_initials: set[str] = set()
    pattern = re.compile(
        r'<img\s+[^>]*src="[^"]*/([^/"=]+=[^/"=]+\.jpg)"[^>]*'
        r'style="\s*width:([0-9.]+)pt;\s*height:([0-9.]+)pt;"',
        re.I,
    )
    for path in sorted(SOURCE_DIR.glob("*.htm")):
        source = path.read_bytes().decode("cp1252")
        for match in pattern.finditer(source):
            name = match.group(1)
            image_occurrences.append(name)
            image_refs.add(name)
            if float(match.group(2)) <= 60 and float(match.group(3)) <= 60:
                probable_initials.add(name)
    unknown = image_refs - set(drop_caps) - NON_TEXT_IMAGES
    missing_initials = probable_initials - set(drop_caps)
    missing_ornaments = NON_TEXT_IMAGES - image_refs
    epub_only_initials = set(drop_caps) - image_refs
    if unknown or missing_initials or missing_ornaments:
        raise ValueError(
            "Incomplete source-image classification; "
            f"unknown={sorted(unknown)}, missing_initials={sorted(missing_initials)}, "
            f"missing_ornaments={sorted(missing_ornaments)}"
        )
    if len(epub_only_initials) != 7:
        raise ValueError(f"Expected 7 EPUB-only initial images, found {sorted(epub_only_initials)}")
    return (
        len(image_refs), len(image_occurrences), len(probable_initials),
        len(epub_only_initials),
    )


def coalesce(blocks: list[str], preserve_layout: bool = False) -> list[str]:
    if preserve_layout:
        return blocks
    result: list[str] = []
    for block in blocks:
        if not result:
            result.append(block)
            continue
        previous = result[-1]
        if previous.endswith("-") and block and block[0].islower():
            result[-1] = previous[:-1] + block
        elif block and block[0].islower() and not re.search(r"[.!?:;\]\)]$", previous):
            result[-1] = previous + " " + block
        else:
            result.append(block)
    return result


def split_chapter(chapter: Chapter, blocks: list[str]) -> tuple[list[tuple[str | None, list[str]]], int]:
    preserve_numbers = chapter.number >= 27
    cleaned = [strip_running_header(repair_text(block)) for block in blocks]
    filtered = [block for block in cleaned if block and not is_page_noise(block, preserve_numbers)]
    orphan_joins = 0
    if chapter.number < 27:
        filtered, orphan_joins = rejoin_orphan_initials(filtered)
    for index in range(len(filtered) - 1):
        if filtered[index] == "upon" and filtered[index + 1].startswith("Eliss"):
            filtered[index] = "upon " + filtered[index + 1]
            filtered[index + 1] = ""
    filtered = [block for block in filtered if block]
    filtered = merge_multiline_headings(chapter.number, filtered)
    segments: list[tuple[str | None, list[str]]] = []
    current_title: str | None = None
    current_blocks: list[str] = []
    seen_headings: set[str] = set()
    for block in filtered:
        embedded_heading, remainder = split_embedded_heading(chapter.number, block)
        heading = embedded_heading or canonical_section_heading(chapter.number, block)
        if heading:
            if heading in seen_headings:
                if remainder:
                    current_blocks.append(remainder)
                continue
            if current_blocks:
                segments.append((current_title, current_blocks))
            current_title = heading
            current_blocks = []
            seen_headings.add(heading)
            if remainder:
                current_blocks.append(remainder)
        else:
            current_blocks.append(block)
    if current_blocks:
        segments.append((current_title, current_blocks))
    if not segments:
        raise ValueError(f"Chapter {chapter.number} produced no text")
    if chapter.number != 26 and len(segments) > 1 and segments[0][0] is None:
        preamble = segments.pop(0)[1]
        title, content = segments[0]
        segments[0] = (title, preamble + content)
    return segments, orphan_joins


def reshape_psalter_table_one(blocks: list[str]) -> list[str]:
    marker = blocks.index("TABLE I.")
    kathism_start = marker + 6
    kathisms = blocks[kathism_start:kathism_start + 20]
    first_start = kathism_start + 21
    first = blocks[first_start:first_start + 20]
    second_start = first_start + 21
    second = blocks[second_start:second_start + 20]
    third_start = second_start + 21
    third = blocks[third_start:third_start + 20]
    if any(len(column) != 20 for column in (kathisms, first, second, third)):
        raise ValueError("Psalter Table I did not yield twenty complete rows")
    rows = [
        "Kathism | First Stasis | Second Stasis | Third Stasis",
        *[
            f"{kathisms[index]} | {first[index]} | {second[index]} | {third[index]}"
            for index in range(20)
        ],
    ]
    return blocks[:marker] + rows + blocks[third_start + 20:]


def reshape_psalter_table_two(blocks: list[str]) -> list[str]:
    days = ("Sunday", "Monday", "Tuesday", "Wednesd.", "Thursday", "Friday", "Saturday")
    positions = [blocks.index(day) for day in days]
    if positions != sorted(positions):
        raise ValueError("Psalter Table II day order drifted")
    rows = blocks[:positions[0]]
    if rows[2:4] != ["Name of the", "Office"] or rows[8:10] != ["E. In", "Holy Passion Week."]:
        raise ValueError("Psalter Table II headings drifted")
    rows[2:4] = ["Name of the Office"]
    rows[7:9] = ["E. In Holy Passion Week."]
    for index, day in enumerate(days):
        end = positions[index + 1] if index + 1 < len(days) else len(blocks)
        entries = blocks[positions[index] + 1:end]
        rows.append(day.rstrip(".") + ". " + " ".join(entries))
    return rows


SCRIPTURE_PREFIX = re.compile(
    r"^(?:(?:[123I]+)\s+)?(?:Gen|Ex|Lev|Num|Deut|Josh|Judg|Ruth|Kings|Chron|"
    r"Esd|Neh|Tob|Judith|Esth|Job|Ps|Prov|Eccl|Song|Wis|Sir|Isa|Jer|Bar|Ezek|"
    r"Dan|Hos|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|Matt|Mark|"
    r"Luke|John|Acts|Rom|Cor|Gal|Eph|Philip|Col|Thess|Tim|Titus|Philem|Heb|"
    r"James|Pet|Jude|Rev)\.?\b",
    re.I,
)


def join_wrapped_words(blocks: list[str]) -> list[str]:
    result: list[str] = []
    for block in blocks:
        if result and result[-1].endswith("-") and block and block[0].islower():
            result[-1] = result[-1][:-1] + block
        else:
            result.append(block)
    return result


def reshape_lesson_table(blocks: list[str]) -> list[str]:
    source: list[str] = []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if (
            block == "Matt. XXV. 14-"
            and index + 1 < len(blocks)
            and blocks[index + 1] == "3O."
        ):
            source.append("Matt. XXV. 14-30.")
            index += 2
            continue
        source.append(block)
        index += 1
    source = join_wrapped_words(source)
    if_falling = source.index("If falling on")
    if source[if_falling + 1] != "Sat. or Sun.":
        raise ValueError("Christmas Eve alternate lesson label drifted")
    source[if_falling] = "If falling on Sat. or Sun."
    source.pop(if_falling + 1)
    thursday = source.index("Thursday.")
    holy_thursday = max(
        index for index, block in enumerate(source[:thursday])
        if block == "Holy and Gt."
    )
    if thursday - holy_thursday != 3:
        raise ValueError("Holy and Great Thursday source order drifted")
    source[holy_thursday] = "Holy and Gt. Thursday."
    source.pop(thursday)
    source = [
        "Aug. 29. Beheading of the" if block == "29. Beheading of the" else block
        for block in source
    ]
    rows: list[str] = []
    label: list[str] = []
    references: list[str] = []

    def join_reference(fragments: list[str]) -> str:
        result = ""
        for fragment in fragments:
            if not result:
                result = fragment
            elif result.endswith("-") or fragment.startswith("-"):
                result += fragment
            else:
                result += " " + fragment
        return result

    def flush() -> None:
        if not label and not references:
            return
        if references:
            gospel_start = next((
                index for index, reference in enumerate(references)
                if re.match(r"^(?:Matt|Mark|Luke|John)\.?\b", reference)
                or reference.startswith("As on ")
                or re.match(r"^Or, (?:Matt|Mark|Luke|John)\.?\b", reference)
            ), None)
            if gospel_start is None or gospel_start == 0:
                cells = [join_reference(references)]
            else:
                cells = [
                    join_reference(references[:gospel_start]),
                    join_reference(references[gospel_start:]),
                ]
            rows.append(" ".join(label).strip() + " | " + " | ".join(cells))
        else:
            rows.append(" ".join(label).strip())
        label.clear()
        references.clear()

    label_start = re.compile(
        r"^(?:Easter |Sun\.|Sunday |Ascension\.|Pentecost |Sat\.|Palm Sunday|"
        r"Holy and Gt\.|Sep\.|Oct\.|Nov\.|Dec\.|Jan\.? |Feb\.|Mch\.|Apl\.|May |"
        r"June |Jun |July |Aug\.|If falling on(?: |$)|For |On Fest\.)"
    )
    for block in source:
        if block.startswith("Lessons ") or block == "AT MATINS.":
            flush()
            rows.append(block)
            continue
        if label_start.match(block):
            flush()
            label.append(block)
            continue
        is_reference = bool(SCRIPTURE_PREFIX.match(block)) or block.startswith((
            "Epis. And Gos.", "Epis. and Gos.", "As on ", "Or, ", "-",
        ))
        if is_reference or references:
            references.append(block)
            continue
        label.append(block)
    flush()
    if len(rows) < 3:
        raise ValueError(f"Lesson table produced too few logical rows: rows={rows}, blocks={blocks[:8]}")
    return rows


KALENDAR_DATE = re.compile(r"^(?:A|[b-g])[.,]\s+(?:[I1-9][0-9Or]?[.,]?)\s+")


def reshape_kalendar(blocks: list[str]) -> list[str]:
    months = "SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST"
    cleaned = [
        block for block in blocks
        if block not in {"THB KALENDAR.", "32", "32*", "33"}
        and not re.fullmatch(rf"(?:{months})\.\s+[0-9IO]+", block)
    ]
    expanded: list[str] = []
    embedded_date = re.compile(r"\s+(?=(?:A|[b-g])[.,]\s+(?:[I1-9][0-9Or]?[.,]?)\s+)")
    for block in cleaned:
        expanded.extend(piece for piece in embedded_date.split(block) if piece)
    source = join_wrapped_words(expanded)
    records: list[str] = []
    current: list[str] = []
    for block in source:
        if KALENDAR_DATE.match(block) and current:
            records.append(" ".join(current))
            current = [block]
        elif KALENDAR_DATE.match(block):
            current = [block]
        elif current:
            current.append(block)
        else:
            records.append(block)
    if current:
        records.append(" ".join(current))
    repaired = []
    for record in records:
        record = record.replace("Re lics", "Relics").replace("NIC OLAS", "NICOLAS")
        record = record.replace("hon ourable", "honourable")
        repaired.append(record)
    if len(repaired) < 25:
        raise ValueError("Kalendar month produced too few logical records")
    return repaired


def normalize_almanack_number(text: str) -> str:
    return text.translate(str.maketrans({"I": "1", "O": "0"}))


def reshape_almanack(blocks: list[str]) -> list[str]:
    subtitle = blocks[0]
    data: list[str] = []
    index = 1
    while index < len(blocks):
        if blocks[index] == "A.M.":
            index += 13
            continue
        if blocks[index] == "FINIS.":
            break
        data.append(blocks[index])
        index += 1
    if len(data) != 400:
        raise ValueError(f"Almanack expected 400 cells, found {len(data)}")
    rows = [
        "A.M. | A.D. | Indict. | Cycle of the Sun | Cycle of the Moon | Dominical Letter | The Triodion beginneth | Pascha"
    ]
    for row_index in range(50):
        cells = data[row_index * 8:(row_index + 1) * 8]
        expected_am = str(7399 + row_index)
        expected_ad = str(1891 + row_index)
        actual_am = normalize_almanack_number(cells[0]).replace("?", "2")
        actual_ad = normalize_almanack_number(cells[1]).replace(" *", "")
        if actual_am != expected_am or actual_ad != expected_ad:
            raise ValueError(f"Almanack year sequence drifted at row {row_index + 1}: {cells[:2]}")
        normalized = [expected_am, expected_ad]
        normalized.extend(normalize_almanack_number(cell) for cell in cells[2:5])
        normalized.append(cells[5])
        normalized.append(normalize_almanack_number(cells[6]).replace("Men.", "Mch.").replace("Jan,", "Jan."))
        normalized.append(normalize_almanack_number(cells[7]))
        rows.append(" | ".join(normalized))
    return [subtitle, *rows, "FINIS."]


def reshape_reference_content(chapter: int, section_title: str | None, blocks: list[str]) -> list[str]:
    if chapter == 27 and section_title == "TABLE I.":
        return reshape_psalter_table_one(blocks)
    if chapter == 27 and section_title == "TABLE II.":
        return reshape_psalter_table_two(blocks)
    if chapter == 28 and section_title != "AT MATINS.":
        return reshape_lesson_table(blocks)
    if chapter == 29:
        return reshape_kalendar(blocks)
    if chapter == 30:
        return reshape_almanack(blocks)
    return blocks


def unit_text(blocks: list[str], preserve_layout: bool = False) -> str:
    return "\n\n".join(coalesce(blocks, preserve_layout)).strip()


def front_matter_units(drop_caps: dict[str, str]) -> tuple[list[dict], list[str]]:
    blocks, uses = extract_html_blocks(SOURCE_DIR / "i.htm", drop_caps, segmented=True)
    markers = [
        ("preface", "Preface", "PREFACE."),
        ("note-1", "Note 1. On the Arrangement of the Church, and on the Ritual", "NOTES."),
        ("note-2", "Note 2. On the Books Containing the Divine Service", "NOTE 2."),
        ("note-3", "Note 3. On Some Untranslatable Terms", "NOTE 3."),
        ("note-4", "Note 4. Explanation of Rubrics", "NOTE 4."),
        ("note-5", "Note 5. List of Books Consulted", "NOTE 5."),
        ("errata", "Errata", "ERRATA."), ("contents", "Contents", "CONTENTS."),
    ]
    starts: list[tuple[str, str, int]] = []
    cursor = 0
    for service_id, title, prefix in markers:
        found = next((i for i in range(cursor, len(blocks)) if blocks[i].upper().startswith(prefix)), None)
        if found is None:
            raise ValueError(f"Front matter marker not found: {prefix}")
        starts.append((service_id, title, found))
        cursor = found + 1
    raw_sections = [("title", "Title and Dedication", 0)] + starts
    units: list[dict] = []
    for index, (service_id, title, start) in enumerate(raw_sections):
        end = raw_sections[index + 1][2] if index + 1 < len(raw_sections) else len(blocks)
        text = unit_text([b for b in blocks[start:end] if not is_page_noise(b)])
        if not text:
            raise ValueError(f"Empty front matter service: {service_id}")
        units.append({
            "service_id": f"{WORK_ID}::service-{service_id}", "service_title": title,
            "section_title": None, "part_title": "Front Matter", "chapter_title": title,
            "subsection_title": None, "citation_anchor": f"Shann (1891), {title}",
            "printed_page_start": None, "text": text,
        })
    return units, uses


def build_payload() -> tuple[dict, dict]:
    drop_caps = json.loads((SOURCE_DIR / "drop_caps.json").read_text(encoding="utf-8"))
    (
        image_ref_count, image_occurrence_count, probable_initial_count,
        epub_only_initial_count,
    ) = audit_source_images(drop_caps)
    epub_blocks, epub_initial_joins, boundary_repair_count = extract_epub_blocks(SOURCE_DIR / "epub-body.xhtml")
    positions = locate_chapters(epub_blocks)
    chapter_blocks: dict[int, list[str]] = {}
    order = list(range(1, 31))
    for index, number in enumerate(order):
        start = positions[number]
        end = positions[order[index + 1]] if index + 1 < len(order) else len(epub_blocks)
        chapter_blocks[number] = strip_chapter_heading(number, epub_blocks[start:end])

    units, front_uses = front_matter_units(drop_caps)
    service_ids = {unit["service_id"] for unit in units}
    orphan_initial_joins = 0
    for chapter in CHAPTERS:
        service_id = f"{WORK_ID}::service-c{chapter.number:02d}"
        service_ids.add(service_id)
        segments, chapter_orphan_joins = split_chapter(chapter, chapter_blocks[chapter.number])
        orphan_initial_joins += chapter_orphan_joins
        for segment_index, (section_title, content) in enumerate(segments):
            content = reshape_reference_content(chapter.number, section_title, content)
            content = [
                repair_epub_boundary(repair_text(block))[0]
                for block in content
            ]
            text = unit_text(content, preserve_layout=chapter.number >= 27)
            if not text:
                raise ValueError(f"Empty chapter unit: {chapter.number} {section_title}")
            citation = f"Shann (1891), Chapter {chapter.roman}"
            if section_title:
                citation += f", {section_title}"
            elif segment_index == 0:
                citation += f", p. {chapter.start_page}"
            units.append({
                "service_id": service_id, "service_title": chapter.title,
                "section_title": section_title, "part_title": chapter.part_title,
                "chapter_title": f"Chapter {chapter.roman}. {chapter.title}",
                "subsection_title": section_title, "citation_anchor": citation,
                "printed_page_start": chapter.start_page if segment_index == 0 else None,
                "text": text,
            })

    payload_units: list[dict] = []
    service_counts: dict[str, int] = {}
    for ordinal, unit in enumerate(units, start=1):
        service_id = unit["service_id"]
        service_counts[service_id] = service_counts.get(service_id, 0) + 1
        suffix = service_id.split("::service-", 1)[1]
        payload_units.append({
            "unit_id": f"{WORK_ID}::{suffix}-u{service_counts[service_id]:02d}",
            "work_id": WORK_ID, "work_title": WORK_TITLE, "author": "Orthodox Church",
            "source_class": "liturgical", "ordinal": ordinal, **unit, "unit_type": "liturgical_text",
        })

    paragraph_boundary_joins = 0
    joined_unit_suffixes: set[str] = set()
    for unit in payload_units:
        joins = repair_unit_paragraphs(unit)
        if joins:
            paragraph_boundary_joins += joins
            joined_unit_suffixes.add(unit["unit_id"].split("::", 1)[1])
        if unit["service_id"] == f"{WORK_ID}::service-errata":
            continue
        for bad, good in EDITION_ERRATA_REPAIRS.items():
            unit["text"] = unit["text"].replace(bad, good)
        unit["text"] = apply_source_ocr_repairs(unit["text"])
        paragraphs = unit["text"].split("\n\n")
        for index, paragraph in enumerate(paragraphs):
            for bad, good in PARAGRAPH_PREFIX_REPAIRS.items():
                if paragraph.startswith(bad):
                    paragraphs[index] = good + paragraph[len(bad):]
                    break
        unit["text"] = "\n\n".join(paragraphs)

    if joined_unit_suffixes != set(UNIT_PARAGRAPH_JOIN_GROUPS):
        raise ValueError(
            "Paragraph-join units drifted: "
            f"expected={sorted(UNIT_PARAGRAPH_JOIN_GROUPS)}, "
            f"actual={sorted(joined_unit_suffixes)}"
        )
    if paragraph_boundary_joins != 55:
        raise ValueError(
            f"Expected 55 source-verified paragraph joins, found {paragraph_boundary_joins}"
        )

    work = {
        "work_id": WORK_ID, "payload_version": 2, "title": WORK_TITLE,
        "author": "Orthodox Church", "language": "en", "date": "1891",
        "translator": "G. V. Shann", "pub_year": 1891,
        "publisher": "T. W. Stainbank; reprinted by AMS Press",
        "reprint_year": 1969,
        "source": "Euchology: A Manual of Prayers of the Holy Orthodox Church, done into English by G. V. Shann (Kidderminster: T. W. Stainbank, 1891), as reprinted by AMS Press in 1969",
        "source_url": "https://ccel.org/ccel/shann/euchology/euchology.ii.html",
        "facsimile_url": "https://www.ccel.org/ccel/s/shann/euchology/cache/euchology.pdf",
        "facsimile_label": "Open the complete public-domain edition", "facsimile_only": False,
        "native_text": True, "service_book": True, "source_class": "liturgical",
        "description": "The complete text of G. V. Shann's 1891 English manual of Orthodox daily worship. CCEL digitized the AMS Press 1969 reprint of the Kidderminster edition. Its thirty chapters include Vespers, Compline, Nocturns, Matins, the Hours, Typica, audible portions of the Divine Liturgies, preparation and thanksgiving for Holy Communion, services from the Lenten and Ferial Triodia, troparia and condakia, diptychs, tables of readings, the Kalendar, and the original almanack.",
        "source_limitations": "CCEL's electronic edition flattens the A-E seasonal columns in Psalter Table II. Their definitions and source order are preserved here, but missing cell associations are not inferred.",
        "digitized": "Christian Classics Ethereal Library, from the AMS Press 1969 reprint (Library of Congress Catalogue Card 75-82260)", "rights": "Public Domain",
        "rights_url": "https://ccel.org/ccel/shann/euchology/euchology.ii.html",
        "saint": None, "is_saint": False, "purpose": "The life of prayer",
        "centuries": [19], "century": 19, "period": "19th century",
        "service_count": len(service_ids), "unit_count": len(payload_units),
    }
    payload = {"work": work, "units": payload_units}
    all_text = json.dumps(payload, ensure_ascii=False)
    bad_sequences = [
        "\ufffd", "\u201a\u00c4", "\u00c3", "\u00e2", "\u221a", "\u0152", "\u2013", "\u2014",
        "&gt;", "&lt;", "style=",
    ]
    found_bad = [bad for bad in bad_sequences if bad in all_text]
    if found_bad:
        raise ValueError(f"Unrepaired encoding or long-dash sequences: {found_bad}")
    unit_ids = [unit["unit_id"] for unit in payload_units]
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("Duplicate unit IDs")
    citation_anchors = [unit["citation_anchor"] for unit in payload_units]
    if len(citation_anchors) != len(set(citation_anchors)):
        raise ValueError("Duplicate citation anchors")
    if len(service_ids) != 39 or len(payload_units) != 157:
        raise ValueError(
            f"Hierarchy count drifted: services={len(service_ids)}, units={len(payload_units)}"
        )
    if any(not unit["text"].strip() for unit in payload_units):
        raise ValueError("Empty unit text")
    orphan_paragraphs = []
    for unit in payload_units:
        match = re.search(r"::service-c(\d+)$", unit["service_id"])
        if not match or int(match.group(1)) >= 27:
            continue
        orphan_paragraphs.extend(
            (unit["unit_id"], paragraph)
            for paragraph in unit["text"].split("\n\n")
            if len(paragraph.strip()) <= 2
        )
    if orphan_paragraphs:
        raise ValueError(f"Unresolved ornamental-initial paragraphs: {orphan_paragraphs}")
    short_units = [(unit["unit_id"], len(unit["text"].strip())) for unit in payload_units if len(unit["text"].strip()) < 20]
    if short_units:
        raise ValueError(f"Units too short to be meaningful: {short_units}")
    if set(chapter_blocks) != set(range(1, 31)):
        raise ValueError("The thirty chapters were not all ingested")
    if (
        len(drop_caps) != 218 or image_ref_count != 241
        or image_occurrence_count != 250 or probable_initial_count != 211
        or len(drop_caps) + len(NON_TEXT_IMAGES) != 248
    ):
        raise ValueError(
            f"Source-image audit drifted: mapped={len(drop_caps)}, refs={image_ref_count}, "
            f"occurrences={image_occurrence_count}, "
            f"probable_initials={probable_initial_count}, "
            f"classified_identifiers={len(drop_caps) + len(NON_TEXT_IMAGES)}"
        )
    if epub_initial_joins != 418 or boundary_repair_count != len(EPUB_BOUNDARY_REPAIRS):
        raise ValueError(
            f"EPUB initial audit drifted: joins={epub_initial_joins}, "
            f"boundary_repairs={boundary_repair_count}"
        )
    known_bad = [
        "W1", '"IWTY', "AH The Troparion", "OMING <n", "YX/'ITH", "TpOR",
        "^HOUGH", "TLTAV1NG", "HTHOU", "AV1NG", "ORB1D", "A1L!",
        "THK ALL-NIGHT", "THB GREAT COMPLINE", "PRATERS BEFORE HOLY COMMUNION",
        "TROPAR1A ETC. FOR FESTIVALS", "THB KALENDAR", "PASC HA", "HOLT PASCHA",
        "BBLESS", "LORDER my steps", "needs greek text",
        "THE LITTLE DAILY VESPERS.", "TTHOU",
        "48 NOCTURNS", "THE GT. MATINS WHEN NO VIGIL HELD.",
        "THE GREAT COMPLINE.", "THE DAILY NOCTURNS.", "THE DAILY MATINS.",
        "58(59)-60(51)", "Matt. XXV. 14-\n",
        "TR0PAR1A ETC. FOR FESTIVALS.",
        "Bethlehem re-", "Re lics", "NIC OLAS", "HONOUR ABLE", "Men. 26.",
    ]
    body_text = json.dumps([
        unit for unit in payload_units
        if unit["service_id"] != f"{WORK_ID}::service-errata"
    ], ensure_ascii=False)
    unstable_source_repairs = [
        unit["unit_id"] for unit in payload_units
        if unit["service_id"] != f"{WORK_ID}::service-errata"
        and apply_source_ocr_repairs(unit["text"]) != unit["text"]
    ]
    if unstable_source_repairs:
        raise ValueError(
            f"Source OCR repairs are not idempotent: {unstable_source_repairs}"
        )
    found_known_bad = [bad for bad in known_bad if bad in body_text]
    if found_known_bad:
        contexts = {
            bad: [unit["unit_id"] for unit in payload_units if bad in unit["text"]]
            for bad in found_known_bad
        }
        raise ValueError(f"Known ornamental-initial defects remain: {contexts}")
    bad_prefixes = ("RETHREN, let us", "OW the heavenly Powers")
    prefix_defects = [
        (unit["unit_id"], paragraph)
        for unit in payload_units
        if unit["service_id"] != f"{WORK_ID}::service-errata"
        for paragraph in unit["text"].split("\n\n")
        if paragraph.startswith(bad_prefixes)
    ]
    if prefix_defects:
        raise ValueError(f"Known paragraph-prefix defects remain: {prefix_defects}")
    if "Ἀπόστολος. - ἐν Βενετίᾳ, 1866." not in body_text:
        raise ValueError("The facsimile-verified Greek bibliography entry is missing")
    duplicated_initials = []
    for unit in payload_units:
        for token in re.findall(r"\b[A-Z]{4,}\b", unit["text"]):
            if (
                re.fullmatch(r"([A-Z])\1{2,}[A-Z]+", token)
                and not set(token) <= set("IVXLCDM")
            ):
                duplicated_initials.append((unit["unit_id"], token))
    if duplicated_initials:
        raise ValueError(f"Duplicated ornamental initials remain: {duplicated_initials}")
    required_unit_fields = {
        "service_id", "service_title", "section_title", "part_title",
        "chapter_title", "subsection_title", "citation_anchor",
    }
    missing_fields = [
        unit["unit_id"] for unit in payload_units
        if not required_unit_fields.issubset(unit)
    ]
    if missing_fields:
        raise ValueError(f"Hierarchy fields missing from units: {missing_fields}")
    duplicate_sections: list[tuple[str, str]] = []
    for service_id in service_ids:
        titles = [
            unit["section_title"] for unit in payload_units
            if unit["service_id"] == service_id and unit["section_title"]
        ]
        duplicate_sections.extend((service_id, title) for title in set(titles) if titles.count(title) > 1)
    if duplicate_sections:
        raise ValueError(f"Duplicate section headings: {sorted(duplicate_sections)}")
    by_service = {}
    for unit in payload_units:
        by_service.setdefault(unit["service_id"], []).append(unit)
    required_service_sections = {
        f"{WORK_ID}::service-c14": [
            "A. THE TYPICA IN THE GREAT FASTS.",
            "B. THE TYPICA ON ORDINARY DAYS.",
        ],
        f"{WORK_ID}::service-c19": [
            "A. PRAYERS BEFORE HOLY COMMUNION.",
            "ON THE MORROW, THE USUAL OFFICE OF HOURS.",
            "B. PRAYERS OF THANKSGIVING AFTER HOLY COMMUNION.",
        ],
    }
    for service_id, expected_sections in required_service_sections.items():
        actual_sections = [unit["section_title"] for unit in by_service[service_id]]
        if actual_sections != expected_sections:
            raise ValueError(
                f"Service hierarchy drifted for {service_id}: {actual_sections}"
            )
    table_one = next(unit for unit in by_service[f"{WORK_ID}::service-c27"] if unit["section_title"] == "TABLE I.")
    if "I. | 1-3. | 4-6. | 7, 8." not in table_one["text"] or "XX. | 143(144), 144(145). | 145(146)-147. | 148-150." not in table_one["text"]:
        raise ValueError("Psalter Table I row associations drifted")
    table_two = next(unit for unit in by_service[f"{WORK_ID}::service-c27"] if unit["section_title"] == "TABLE II.")
    if sum(
        1 for day in ("Sunday", "Monday", "Tuesday", "Wednesd.", "Thursday", "Friday", "Saturday")
        if f"\n\n{day.rstrip('.')}. " in "\n\n" + table_two["text"]
    ) != 7:
        raise ValueError("Psalter Table II did not preserve seven day rows")
    lesson_table = next(unit for unit in by_service[f"{WORK_ID}::service-c28"] if unit["section_title"] == "AT LITURGY")
    if sum(paragraph.count(" | ") == 2 for paragraph in lesson_table["text"].split("\n\n")) < 100:
        raise ValueError("Liturgy lesson table did not preserve logical records")
    lesson_rows = lesson_table["text"].split("\n\n")
    required_lesson_rows = {
        "Sun. 16 aft. Pent. | 2 Cor. VI. 1-10. | Matt. XXV. 14-30.",
        "Holy and Gt. Thursday. | I Cor. XI. 23-32. | Matt. XXVI. 1-20. John XIII. 3-17. Matt. XXVI. 21-39. Luke. XXII. 43-45. Matt. XXVI. 40-XXVII. 2.",
        "June 24. Nativity of the Forerunner. | Rom. XIII. 11-XIV. 4. | Luke I. 1-25, 57-68, 76, 80.",
        "Aug. 29. Beheading of the Forerunner. | Acts XIII. 25-33. | Mark VI. 14-30.",
        "If falling on Sat. or Sun. | Gal. III. 15-22. | Matt.XIII. 31-36.",
    }
    missing_lesson_rows = required_lesson_rows - set(lesson_rows)
    if missing_lesson_rows:
        raise ValueError(f"Lesson-table row associations drifted: {sorted(missing_lesson_rows)}")
    lesson_labels = [row.split(" | ", 1)[0] for row in lesson_rows]
    for expected_label in (
        "For Prophets.", "For an Apostle.", "For Ven. Martyrs.",
        "For Martyrs (women).",
    ):
        if lesson_labels.count(expected_label) != 1:
            raise ValueError(f"Lesson-table label association drifted: {expected_label}")
    if lesson_table["text"].count("Matt. XXV. 14-30.") != 1 or "30.30" in lesson_table["text"]:
        raise ValueError("Lesson-table Matthew XXV reference drifted")
    month_days = {
        "SEPTEMBER.": 30, "OCTOBER.": 31, "NOVEMBER.": 30, "DECEMBER.": 31,
        "JANUARY.": 31, "FEBRUARY.": 29, "MARCH.": 31, "APRIL.": 30,
        "MAY.": 31, "JUNE.": 30, "JULY.": 31, "AUGUST.": 31,
    }
    for unit in by_service[f"{WORK_ID}::service-c29"]:
        expected = month_days[unit["section_title"]]
        if len(unit["text"].split("\n\n")) != expected + 1:
            raise ValueError(
                f"Kalendar row count drifted for {unit['section_title']}: "
                f"expected={expected + 1}, actual={len(unit['text'].split(chr(10) + chr(10)))}, "
                f"rows={unit['text'].split(chr(10) + chr(10))}"
            )
    almanack = by_service[f"{WORK_ID}::service-c30"][0]
    almanack_rows = [row for row in almanack["text"].split("\n\n") if re.match(r"^7\d{3} \| 1\d{3} \|", row)]
    if len(almanack_rows) != 50:
        raise ValueError(f"Almanack expected 50 logical rows, found {len(almanack_rows)}")
    stats = {
        "chapters": 30, "services": len(service_ids), "units": len(payload_units),
        "characters": sum(len(unit["text"]) for unit in payload_units),
        "verified_drop_cap_files": len(drop_caps),
        "segmented_source_image_refs": image_ref_count,
        "segmented_source_image_occurrences": image_occurrence_count,
        "total_classified_image_identifiers": len(drop_caps) + len(NON_TEXT_IMAGES),
        "referenced_initial_images": probable_initial_count,
        "epub_only_initial_images": epub_only_initial_count,
        "nontext_ornament_images": len(NON_TEXT_IMAGES),
        "epub_initial_joins": epub_initial_joins,
        "orphan_initial_joins": orphan_initial_joins,
        "paragraph_boundary_joins": paragraph_boundary_joins,
        "boundary_repairs": boundary_repair_count,
    }
    return payload, stats


def serialized(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload, stats = build_payload()
    expected = serialized(payload)
    if args.write:
        TARGET.write_text(expected, encoding="utf-8", newline="\n")
        print(f"Wrote {TARGET.relative_to(ROOT)}")
    else:
        actual = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
        if actual != expected:
            print(f"Out of date: {TARGET.relative_to(ROOT)}", file=sys.stderr)
            return 1
    print(json.dumps(stats, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
