#!/usr/bin/env python3
"""
Add works that New Advent serves whole, one page to a work.

Against Heresies needed its own script because it runs to 173 pages. Most of
what the shelf still wants is the opposite shape: one page holding the whole
treatise, divided either by <h2> headings or by numbered sections. This takes
a catalogue of those and builds them all.

Every entry declares how many sections the work has. That number is not read
off the page; it is the known length of the work, and the run stops if the
page does not yield it. ingest_canons.py once assembled its structure from a
hand-listed guess and dropped seven councils without raising a single error,
which is the failure this guards against: a short book looks exactly like a
complete one to everybody except a reader who knows what is missing.

    python3 tools/ingest_batch.py --check
    python3 tools/ingest_batch.py --write
    python3 tools/ingest_batch.py --check --only cyprian-unity
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest import clean_text, strip_scripture_refs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data" / "library"
INDEX = OUTDIR / "works-index.json"
CACHE = Path("/tmp/plithos-batch")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"

ANF_PUB = "Christian Literature Publishing Company, Buffalo"

CATALOGUE = [
    {
        "work_id": "second-clement",
        "url": "https://www.newadvent.org/fathers/1011.htm",
        "shape": "h2",
        "sections": 20,
        "anchor": "An Ancient Homily, Chapter %d",
        "work": {
            "title": "An Ancient Homily",
            "author": "An unknown preacher",
            "date": "c. 140",
            "translator": "John Keith",
            "pub_year": 1897,
            "source": "Ante-Nicene Fathers, Vol. 9",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "The earliest Christian sermon that survives: not a "
                           "letter and not by Clement, but an address preached to "
                           "a congregation and copied afterwards beside his, which "
                           "is how it came to be called his second epistle. It "
                           "opens by telling the hearers to think of Jesus Christ "
                           "as of God, and of themselves as having been rescued "
                           "from very little into very much.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": None,
            "is_saint": False,
            # The reception note lives in tools/reception.py, which owns that
            # field for every work and strips any it did not write.
        },
    },
    {
        "work_id": "cyprian-unity-of-the-church",
        "url": "https://www.newadvent.org/fathers/050701.htm",
        "shape": "numbered",
        "sections": 27,
        "anchor": "On the Unity of the Church, %d",
        "work": {
            "title": "On the Unity of the Church",
            "author": "St Cyprian of Carthage",
            "date": "c. 251",
            "translator": "Robert Ernest Wallis",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "Written when a schism had opened at Rome and another "
                           "threatened at Carthage, and the earliest sustained "
                           "argument that the Church is one thing and not many: "
                           "that her unity is not an achievement to be worked "
                           "towards but a fact to be kept, and that the man who "
                           "leaves her leaves what he was seeking.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage",
            "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-lords-prayer",
        "url": "https://www.newadvent.org/fathers/050704.htm",
        "shape": "numbered",
        "sections": 36,
        "anchor": "On the Lord's Prayer, %d",
        "work": {
            "title": "On the Lord's Prayer",
            "author": "St Cyprian of Carthage",
            "date": "c. 252",
            "translator": "Robert Ernest Wallis",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "A commentary on the Our Father, petition by petition, "
                           "and the earliest one the Church has. Cyprian's point "
                           "throughout is that the prayer is said in the plural: "
                           "we do not say my Father but our Father, because "
                           "prayer for a Christian is never a private transaction.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage",
            "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-on-mortality",
        "url": "https://www.newadvent.org/fathers/050707.htm",
        "shape": "numbered",
        "sections": 26,
        "anchor": "On the Mortality, %d",
        "work": {
            "title": "On the Mortality",
            "author": "St Cyprian of Carthage",
            "date": "c. 252",
            "translator": "Robert Ernest Wallis",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "Written during the plague that emptied Carthage, to a "
                           "people asking why Christians were dying with everyone "
                           "else. Cyprian answers that the plague does not "
                           "distinguish because it is not meant to, and that what "
                           "it tests is whether a man believes what he says at the "
                           "grave.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage",
            "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-works-and-alms",
        "url": "https://www.newadvent.org/fathers/050708.htm",
        "shape": "numbered",
        "sections": 26,
        "anchor": "On Works and Alms, %d",
        "work": {
            "title": "On Works and Alms",
            "author": "St Cyprian of Carthage",
            "date": "c. 253",
            "translator": "Robert Ernest Wallis",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "On almsgiving, and on the sins committed after baptism "
                           "that a Christian supposes he can do nothing about. "
                           "Cyprian's answer is that mercy shown is the remedy the "
                           "Lord Himself named, and that the man who keeps his "
                           "money keeps his wound.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage",
            "is_saint": True,
        },
    },
    {
        "work_id": "hippolytus-christ-and-antichrist",
        "url": "https://www.newadvent.org/fathers/0516.htm",
        "shape": "numbered",
        "sections": 67,
        "anchor": "Treatise on Christ and Antichrist, %d",
        "work": {
            "title": "Treatise on Christ and Antichrist",
            "author": "St Hippolytus of Rome",
            "date": "c. 200",
            "translator": "J. H. MacMahon",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "The earliest surviving Christian treatment of the last "
                           "things as a subject in its own right, reading Daniel "
                           "and the Apocalypse together. Hippolytus was a "
                           "presbyter of Rome and a hearer of Irenaeus, who had "
                           "heard Polycarp, who had heard the Apostle John.",
            "digitized": "New Advent",
            "rights": "Public domain",
            "saint": "Hieromartyr Hippolytus, and those with him",
            "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-on-the-lapsed",
        "url": "https://www.newadvent.org/fathers/050703.htm",
        "shape": "numbered", "sections": 36,
        "anchor": "On the Lapsed, %d",
        "work": {
            "title": "On the Lapsed", "author": "St Cyprian of Carthage",
            "date": "251", "translator": "Robert Ernest Wallis", "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5", "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "Written when the persecution lifted and the Christians who had sacrificed to the idols came back asking to be received. The earliest treatment of a question the Church has faced in every generation since: what is done for a baptised man who has fallen, and on what terms he returns.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage", "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-dress-of-virgins",
        "url": "https://www.newadvent.org/fathers/050702.htm",
        "shape": "numbered", "sections": 24,
        "anchor": "On the Dress of Virgins, %d",
        "work": {
            "title": "On the Dress of Virgins", "author": "St Cyprian of Carthage",
            "date": "c. 249", "translator": "Robert Ernest Wallis", "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5", "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "To the women of Carthage who had vowed virginity, on modesty, wealth and display. One of the earliest witnesses to consecrated virginity as a settled state of life in the Church, a century before the monasteries.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage", "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-to-demetrian",
        "url": "https://www.newadvent.org/fathers/050705.htm",
        "shape": "numbered", "sections": 25,
        "anchor": "To Demetrian, %d",
        "work": {
            "title": "To Demetrian", "author": "St Cyprian of Carthage",
            "date": "c. 252", "translator": "Robert Ernest Wallis", "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5", "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "An answer to a pagan who blamed the Christians for the plagues, the wars and the failing harvests, which is the oldest accusation there is. Cyprian replies that the world is growing old, and that the man who blames the Christians has not asked what he himself owes.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage", "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-vanity-of-idols",
        "url": "https://www.newadvent.org/fathers/050706.htm",
        "shape": "numbered", "sections": 15,
        "anchor": "On the Vanity of Idols, %d",
        "work": {
            "title": "On the Vanity of Idols", "author": "St Cyprian of Carthage",
            "date": "c. 247", "translator": "Robert Ernest Wallis", "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5", "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "That the gods of the nations were men, that the demons took their names, and that the God the Christians worship is the one who made what the others are carved from.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage", "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-on-patience",
        "url": "https://www.newadvent.org/fathers/050709.htm",
        "shape": "numbered", "sections": 24,
        "anchor": "On the Advantage of Patience, %d",
        "work": {
            "title": "On the Advantage of Patience", "author": "St Cyprian of Carthage",
            "date": "256", "translator": "Robert Ernest Wallis", "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5", "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "That patience is not the temper of a man who does not mind, but a virtue learned from God, who bears with the world daily and makes His sun rise on the ungrateful.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage", "is_saint": True,
        },
    },
    {
        "work_id": "cyprian-jealousy-and-envy",
        "url": "https://www.newadvent.org/fathers/050710.htm",
        "shape": "numbered", "sections": 18,
        "anchor": "On Jealousy and Envy, %d",
        "work": {
            "title": "On Jealousy and Envy", "author": "St Cyprian of Carthage",
            "date": "256", "translator": "Robert Ernest Wallis", "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5", "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "On the passion Cyprian says opened the first grave, since it was by the devil's envy that death entered the world, and on how it works inside a congregation.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Cyprian, Bishop of Carthage", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-on-virginity",
        "url": "https://www.newadvent.org/fathers/2907.htm",
        "shape": "h2", "sections": 24,
        "anchor": "On Virginity, Chapter %d",
        "work": {
            "title": "On Virginity", "author": "St Gregory of Nyssa",
            "date": "c. 371", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "Written for those considering the celibate life, and against the notion that it is a rejection of marriage. Gregory, who was himself married, argues that virginity is a way of loving God undivided, and that the man who despises marriage has misunderstood both.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-making-of-man",
        "url": "https://www.newadvent.org/fathers/2914.htm",
        "shape": "h2", "sections": 32,
        "anchor": "On the Making of Man, %d",
        "work": {
            "title": "On the Making of Man", "author": "St Gregory of Nyssa",
            "date": "379", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "Written to finish what his brother Basil left at the sixth day of the Hexaemeron. On what it means that man was made in the image of God, on the union of soul and body, and on the resurrection of the body, with a long look at how the body is built.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-soul-and-resurrection",
        "url": "https://www.newadvent.org/fathers/2915.htm",
        "shape": "whole", "sections": 20000,
        "anchor": "On the Soul and the Resurrection",
        "work": {
            "title": "On the Soul and the Resurrection", "author": "St Gregory of Nyssa",
            "date": "c. 380", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "A dialogue held at the deathbed of his sister Macrina, who does most of the arguing. On what the soul is, what becomes of it at death, what the resurrection of the body means, and why grief is not a reason to doubt any of it.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-holy-spirit-macedonians",
        "url": "https://www.newadvent.org/fathers/2903.htm",
        "shape": "whole", "sections": 6000,
        "anchor": "On the Holy Spirit, Against the Macedonians",
        "work": {
            "title": "On the Holy Spirit, Against the Macedonians", "author": "St Gregory of Nyssa",
            "date": "c. 381", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "Against those who confessed the Son and denied the Spirit, written in the years around the Council of Constantinople, which settled the question.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-holy-trinity",
        "url": "https://www.newadvent.org/fathers/2904.htm",
        "shape": "whole", "sections": 2500,
        "anchor": "On the Holy Trinity",
        "work": {
            "title": "On the Holy Trinity", "author": "St Gregory of Nyssa",
            "date": "c. 375", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "A letter to Eustathius on why confessing three persons is not confessing three Gods.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-not-three-gods",
        "url": "https://www.newadvent.org/fathers/2905.htm",
        "shape": "whole", "sections": 3500,
        "anchor": "On \"Not Three Gods\"",
        "work": {
            "title": "On \"Not Three Gods\"", "author": "St Gregory of Nyssa",
            "date": "c. 390", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "To Ablabius, who had asked the obvious question: if Peter, James and John are three men, why are the Father, the Son and the Spirit not three Gods. The answer turns on what a nature is and what a person is.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-on-the-faith",
        "url": "https://www.newadvent.org/fathers/2906.htm",
        "shape": "whole", "sections": 1400,
        "anchor": "On the Faith",
        "work": {
            "title": "On the Faith", "author": "St Gregory of Nyssa",
            "date": "c. 383", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "A short statement of the faith addressed to Simplicius.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-meletius",
        "url": "https://www.newadvent.org/fathers/2909.htm",
        "shape": "whole", "sections": 2200,
        "anchor": "Funeral Oration on Meletius",
        "work": {
            "title": "Funeral Oration on Meletius", "author": "St Gregory of Nyssa",
            "date": "381", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "Preached at Constantinople over the bishop who had presided at the Council and died while it was sitting.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-baptism-of-christ",
        "url": "https://www.newadvent.org/fathers/2910.htm",
        "shape": "whole", "sections": 4000,
        "anchor": "On the Baptism of Christ",
        "work": {
            "title": "On the Baptism of Christ", "author": "St Gregory of Nyssa",
            "date": "c. 383", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "A sermon for the Theophany, on what is done in the water, and on why the Lord who needed no cleansing went down into it.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-infants-early-deaths",
        "url": "https://www.newadvent.org/fathers/2912.htm",
        "shape": "whole", "sections": 5500,
        "anchor": "On Infants' Early Deaths",
        "work": {
            "title": "On Infants' Early Deaths", "author": "St Gregory of Nyssa",
            "date": "c. 381", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "To Hierius, who had asked what becomes of children who die before they can choose anything. Gregory refuses the easy answers on both sides and reasons instead from what God is.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "gregory-nyssa-on-pilgrimages",
        "url": "https://www.newadvent.org/fathers/2913.htm",
        "shape": "whole", "sections": 1000,
        "anchor": "On Pilgrimages",
        "work": {
            "title": "On Pilgrimages", "author": "St Gregory of Nyssa",
            "date": "c. 380", "translator": "William Moore and Henry Austin Wilson",
            "pub_year": 1893,
            "source": "Nicene and Post-Nicene Fathers, Series 2, Vol. 5",
            "publisher": "Christian Literature Company, New York",
            "source_class": "patristic",
            "description": "A letter arguing that going to Jerusalem is not itself a means of grace, and that a change of place is not a change of heart.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Saint Gregory, Bishop of Nyssa", "is_saint": True,
        },
    },
    {
        "work_id": "hippolytus-scriptural-fragments",
        "url": "https://www.newadvent.org/fathers/0502.htm",
        "shape": "h2", "sections": 18,
        "anchor": "Scriptural Commentaries, %d",
        "work": {
            "title": "Fragments from the Scriptural Commentaries",
            "author": "St Hippolytus of Rome",
            "date": "c. 204",
            "translator": "S. D. F. Salmond",
            "pub_year": 1886,
            "source": "Ante-Nicene Fathers, Vol. 5",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "What survives of Hippolytus reading the Scriptures: "
                           "on the six days, on Genesis, on Kings, the Psalms, "
                           "Proverbs, the Song of Songs, Isaiah, Jeremiah and "
                           "Ezekiel, Matthew and Luke, and at length on Daniel, "
                           "where the seventy weeks and the fourth kingdom are "
                           "read as the Church has read them since. The edition "
                           "prints the doubtful fragments separately and says so "
                           "in its own headings.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Hippolytus, and those with him", "is_saint": True,
        },
    },
    {
        "work_id": "clement-of-rome-first-epistle",
        "url": "https://www.newadvent.org/fathers/1010.htm",
        "shape": "h2", "sections": 65,
        "anchor": "First Epistle to the Corinthians, %d",
        "work": {
            "title": "The First Epistle of Clement to the Corinthians",
            "author": "St Clement of Rome",
            "date": "c. 96",
            "language": "en",
            "edition_of": "clement-of-rome-first-epistle",
            "translator": "John Keith",
            "pub_year": 1896,
            "source": "Ante-Nicene Fathers, Vol. 9",
            "publisher": ANF_PUB,
            "source_class": "patristic",
            "description": "A letter from the church at Rome to the church at "
                           "Corinth, which had deposed its presbyters. It appeals "
                           "to the order the apostles left, names the succession "
                           "by which bishops and deacons are appointed, and closes "
                           "with a long prayer for rulers and for the whole world "
                           "that is the earliest Christian liturgical prayer "
                           "written down outside the Scriptures.",
            "digitized": "New Advent", "rights": "Public domain",
            "saint": "Hieromartyr Clement, Pope of Rome", "is_saint": True,
        },
    },
]


def fetch(url, name, delay=1.2):
    p = CACHE / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


def trunk_of(body):
    m = re.search(r"<h1[^>]*>(.*?)</h1>(.*?)(?=<h2[^>]*>\s*About this page|\Z)",
                  body, re.S | re.I)
    if not m:
        raise ValueError("page shape not recognised")
    return re.sub(r"<em>.*?Please help support the mission.*?</em>", "",
                  m.group(2), flags=re.S | re.I)


def split_h2(trunk):
    """Chapters carried as <h2> headings, as in the ancient homily."""
    parts = re.split(r"<h2[^>]*>(.*?)</h2>", trunk, flags=re.S | re.I)
    out = []
    for i in range(1, len(parts) - 1, 2):
        heading = clean_text(parts[i])
        text = strip_scripture_refs(clean_text(parts[i + 1]))
        if text:
            out.append((heading, text))
    return out


def split_numbered(trunk):
    """Sections opening '1.', '2.', ... in their own paragraph, as in Cyprian."""
    paras = re.findall(r"<p[^>]*>(.*?)</p>", trunk, flags=re.S | re.I)
    out, cur, num = [], [], None
    for p in paras:
        txt = clean_text(p)
        if not txt.strip():
            continue
        m = re.match(r"\s*(\d+)\.\s", txt)
        if m:
            if num is not None:
                out.append((num, "\n\n".join(cur)))
            num = int(m.group(1))
            cur = [txt]
        elif num is not None:
            cur.append(txt)
    if num is not None:
        out.append((num, "\n\n".join(cur)))
    return [(n, strip_scripture_refs(t)) for n, t in out]


def build(entry):
    body = fetch(entry["url"], entry["work_id"] + ".htm")
    trunk = trunk_of(body)
    wid = entry["work_id"]

    if entry["shape"] == "whole":
        # A short treatise the source prints without internal divisions. It
        # stands as one unit because that is how it is set, not because the
        # divisions were missed; "sections" is the word count it must reach,
        # so a page that silently empties is caught.
        text = strip_scripture_refs(clean_text(trunk))
        if len(text.split()) < entry["sections"]:
            return None, ("%d words, at least %d expected"
                          % (len(text.split()), entry["sections"]))
        units = [(entry["anchor"], None, text)]
    elif entry["shape"] == "h2":
        got = split_h2(trunk)
        if len(got) != entry["sections"]:
            return None, "%d sections on the page, %d expected" % (
                len(got), entry["sections"])
        units = [(entry["anchor"] % (i + 1), head, text)
                 for i, (head, text) in enumerate(got)]
    else:
        got = split_numbered(trunk)
        nums = [n for n, _ in got]
        if nums != list(range(1, entry["sections"] + 1)):
            missing = sorted(set(range(1, entry["sections"] + 1)) - set(nums))
            return None, ("sections run %s, %d expected%s"
                          % ("%d-%d" % (min(nums), max(nums)) if nums else "empty",
                             entry["sections"],
                             "; missing %s" % missing[:12] if missing else ""))
        units = [(entry["anchor"] % n, None, text) for n, text in got]

    out = []
    for i, (anchor, head, text) in enumerate(units, start=1):
        anchor = anchor if isinstance(anchor, str) else anchor
        if not text.strip():
            return None, "section %d is empty" % i
        u = {
            "unit_id": "%s::u%03d" % (wid, i),
            "work_id": wid,
            "work_title": entry["work"]["title"],
            "author": entry["work"]["author"],
            "source_class": entry["work"]["source_class"],
            "ordinal": i,
            "citation_anchor": anchor,
            "text": text,
        }
        if head:
            u["chapter_title"] = head
        out.append(u)
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    todo = [e for e in CATALOGUE if not args.only or e["work_id"] == args.only]
    built, failed = [], []
    for entry in todo:
        units, err = build(entry)
        if err:
            failed.append((entry["work_id"], err))
            print("  FAIL  %-34s %s" % (entry["work_id"], err))
            continue
        words = sum(len(u["text"].split()) for u in units)
        bad = sum(len(re.findall(r"[–—‘’“”]", u["text"]))
                  for u in units)
        print("  ok    %-34s %3d units  %8s words  %d dashes/smart quotes"
              % (entry["work_id"], len(units), format(words, ","), bad))
        built.append((entry, units))

    if failed:
        print("\n%d of %d failed; nothing written" % (len(failed), len(todo)))
        return 1

    if args.write:
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        for entry, units in built:
            meta = dict(entry["work"], work_id=entry["work_id"])
            OUTDIR.joinpath(entry["work_id"] + ".json").write_text(
                json.dumps({"work": meta, "units": units},
                           ensure_ascii=False, indent=1), encoding="utf-8")
            cat = [w for w in cat if w["work_id"] != entry["work_id"]]
            cat.append(meta)
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %d works and updated the catalogue" % len(built))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
