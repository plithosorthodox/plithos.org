#!/usr/bin/env python3
"""
Add the prayers proper to the Divine Liturgy of St Basil the Great.

The shelf holds three liturgies now and this is the fourth text, but it is not
a fourth liturgy: the Liturgy of St Basil is the same service as the Liturgy
of St John Chrysostom except in certain prayers the priest says secretly, one
hymn, and three phrases in the consecration. Isabel Hapgood's Service Book
says exactly that in its own prefatory note, and prints those prayers in
place, each in a bracket beginning "Or, if the Liturgy of St. Basil the Great
be used". They are gathered here in the order the service takes them.

Nothing is assembled. Each unit is one of her brackets, whole, and the work
does not present itself as the Liturgy of St Basil entire, because what she
prints is not that.

The source is the 1906 Service Book, of which no clean text exists; the
machine readings of the scans are the starting point and not the authority.
Three independent readings of the same pages were compared word by word,
which left twenty-two places where they did not agree over some three
thousand six hundred words, and every one of those - together with both
places where a reading ran two columns of the page into one - was settled
against the page itself. Each such decision is written out below with the
page it was taken from. A reading that all three share and that no page was
consulted for is marked as such in this file and nowhere else; nothing is
guessed at, and no word here was supplied from anywhere but that book.

    python3 tools/ingest_basil_liturgy.py --check
    python3 tools/ingest_basil_liturgy.py --write
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "library" / "liturgy-of-st-basil-propers.json"
INDEX = ROOT / "data" / "library" / "works-index.json"
CACHE = Path("/tmp/plithos-hapgood")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
SRC = ("https://archive.org/download/ServiceBookOfHolyOrthodoxChurchByHapgood/"
       "Service_Book_Orthodox_Church_Hapgood_djvu.txt")

WORK = {
    "work_id": "liturgy-of-st-basil-propers",
    "title": "The Prayers Proper to the Liturgy of St Basil the Great",
    "author": "St Basil the Great",
    "date": "4th century",
    "translator": "Isabel Florence Hapgood",
    "pub_year": 1906,
    "source": "Service Book of the Holy Orthodox-Catholic Apostolic "
              "(Greco-Russian) Church",
    "publisher": "Houghton, Mifflin and Company, Boston and New York",
    "source_class": "liturgical",
    "language": "en",
    "description": "The Liturgy of St Basil is the Liturgy the Church serves "
                   "ten times in the year - on the Sundays of the Great Fast, "
                   "on Holy Thursday and Holy Saturday, at the Nativity and "
                   "the Theophany, and on his own feast - and it is the same "
                   "service as the Liturgy of St John Chrysostom except in "
                   "certain prayers the priest says secretly, one hymn, and "
                   "three phrases in the consecration. Those are given here, "
                   "in the order the service takes them, from an English "
                   "service book of the Orthodox Church. The longest of them "
                   "is the anaphora, which tells the whole history of "
                   "salvation from the making of man to the second coming in "
                   "one sentence after another, and which the Chrysostom "
                   "shortens; the reader who wants to know why the Church "
                   "keeps two liturgies will find the answer there.",
    "digitized": "Internet Archive",
    "rights": "Public domain",
    "saint": "Saint Basil the Great, Archbishop of Caesarea in Cappadocia",
    "is_saint": True,
}

# Lines that are the scanner's or the printer's and not the book's.
FURNITURE = re.compile(r"(?i)^\s*(digitized by\b.*|the divine liturgy(\s+\d+)?"
                       r"|the liturgy of st\..*|\d{1,3}|10\^ r r)\s*$")

# A word broken at the end of a line is joined up. Some words are hyphenated
# in the first place, and joining those would coin a new one, so a hyphen is
# kept wherever the same word stands hyphenated elsewhere in the book.
KEEP_HYPHEN = {
    "all-holy", "marriage-bond", "storm-tossed", "Only-begotten", "sup-port",
    "well-pleasing", "first-fruits", "life-giving", "loving-kindness",
    "faint-hearted", "God-fearing", "Christ-loving", "Coming-again",
    "Birth-giver", "ever-virgin", "never-ceasing", "burnt-offerings",
    "peace-offerings", "life-creating", "ever-memorable", "first-born",
    "many-eyed", "self-same",
}

# Every place where the three readings of the page did not agree, or where one
# of them ran two columns of the page into a single line, settled against the
# page named. Left: what the scan gives. Right: what the page carries.
FROM_THE_PAGE = [
    # p.93. A speck of ink after the closing bracket.
    ("in thy sight.] f", "in thy sight.]", "93"),
    # p.94. Four characters of the facing column caught in the line.
    ("Strengthen us by r us the power", "Strengthen us by the power", "94"),
    # p.102. The exclamation and the Sanctus stand in a narrow column beside
    # the prayer and belong to both liturgies, not to this bracket; one
    # reading set the column down in the middle of the sentence it interrupts.
    ("in keeping thy commandments. Exclamation, Priest Singing the "
     "triumphant song, crying, calling aloud,and saying ; Choir. Holy, holy, "
     "holy, Lord of Sabaoth ; heaven and earth are full of thy glory : "
     "Hosanna in the highest: Blessed is he that cometh in the Name of the "
     "Lord. Hosanna in the highest. But when he disobeyed thee",
     "in keeping thy commandments. But when he disobeyed thee", "102"),
    # p.103.
    ("and be shall be all things", "and he shall be all things", "103"),
    ("at the right band of thy Majesty", "at the right hand of thy Majesty",
     "103"),
    # p.104. The c and the l of proclaim run together in this printing.
    ("ye do prooiaim my death", "ye do proclaim my death", "104"),
    ("his Sitting on the, right hand of thee",
     "his Sitting on the right hand of thee", "104"),
    # p.108. An accent from the line above falls on the a of battle.
    ("in the day of bdttle", "in the day of battle", "108"),
    ("Glory of Virgin^, of whom God", "Glory of Virgins, of whom God", "108"),
    # p.108. Hapgood's own parenthesis, the opening half read as a bracket.
    ("N. [in Russia, the Emperor", "N. (in Russia, the Emperor", "108"),
    # p.125. The f of "of" in the rubric that is kept as part of the hymn.
    ("But if the Liturgy op St. Basil the Great hath been used",
     "But if the Liturgy of St. Basil the Great hath been used", "125"),
    # p.109.
    ("Have rh remembrance, also, O Lord, my unworthiness",
     "Have in remembrance, also, O Lord, my unworthiness", "109"),
    # pp.111-112. The deacon's litany runs down the left of both pages while
    # the priest prays on the right, and one reading laid the left column into
    # the middle of the prayer.
    ("purify us from every defilement of flesh and spirit, and are profitable "
     "to our souls, and peace to the world, let us beseech of the Lord. Tfr "
     "That we may pass the residue of our life in peace and penitence, let us "
     "beseech of the Lord. I£ A Christian ending to our life, painless, "
     "blameless, peaceful ; and a good defence before the dread Judgment Seat "
     "of Christ, let us beseech of the Lord. # Having made our petition for "
     "the unity of the faith, and the communion of the Holy Spirit, let us "
     "commend ourselves, and each other, and all our life unto Christ our "
     "God. Choir. To thee, O Lord. teach us to perfect holiness in thy fear",
     "purify us from every defilement of flesh and spirit, and teach us to "
     "perfect holiness in thy fear", "111-112"),
    # p.119. A speck before the word, and a footnote mark after it.
    ("unto love .unfeigned", "unto love unfeigned", "119"),
    ("an acceptable defence* at the dread", "an acceptable defence at the dread",
     "119"),
    # p.125. Hapgood accents her transliterations of the Greek names of the
    # two hymns; the accents defeat the scan.
    ("this Hymn (Tropdr\\ in Tone I .*", "this Hymn (Tropár), in Tone I.:",
     "125"),
    ("Collect-Hymn (Kond&k\\ in Tone IV :",
     "Collect-Hymn (Kondák), in Tone IV.:", "125"),
]

# p.108 again. The hymn is the choir's and the intercession is the priest's,
# and the page sets them in two columns because they happen at once. Read
# down one column and then the other, the hymn lands in the middle of a
# sentence. It is placed at the head of its bracket, where its column begins.
HYMN = ("Choir. In thee rejoiceth, O thou who art full of Grace, every "
        "created being, the Hierarchy of the Angels, and all mankind, O "
        "Consecrated Temple and supersensual Paradise, Glory of Virgins, of "
        "whom God, who is our God before all the ages, was incarnate and "
        "became a little child. For he made of thy womb a throne, and thy "
        "belly did he make more spacious than the heavens. In thee doth all "
        "Creation rejoice, O thou who art full of Glory : Glory to thee. Or, "
        "at the different Feasts, there shall be sung the appointed Hymn to "
        "the Birth-giver of God.")

# Distinctive words from each of the eighteen brackets, in the order the
# service takes them. The run stops if any is missing or out of order, so a
# bracket that failed to come down cannot pass unnoticed.
EXPECTED = [
    "who dwellest in the heavens",
    "this great mystery of salvation",
    "who in mercy and bounties",
    "who hast created us, and hast brought us",
    "who in verity existest",
    "With these blessed Powers",
    "the cup of the fruit of the vine",
    "This do, in remembrance of me",
    "Wherefore, O all-holy Master",
    "For this bread is in very truth",
    "For this chalice, in very truth",
    "And unite all us who partake",
    "And give them rest where the light",
    "every Bishopric of the Orthodox",
    "the God of salvation",
    "the Father of bounties",
    "for the participation in thy holy",
    "Thy voice is gone out into all the world",
]


def source():
    p = CACHE / "hapgood.txt"
    if not p.exists():
        req = urllib.request.Request(SRC, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            p.write_bytes(r.read())
        time.sleep(0.3)
    return p.read_text(encoding="utf-8", errors="replace")


def flatten(block, whole):
    keep = [l.strip() for l in block.split("\n") if not FURNITURE.match(l)]
    s = " ".join(x for x in keep if x)

    def join(m):
        joined = m.group(1) + "-" + m.group(2)
        return joined if joined.lower() in {h.lower() for h in KEEP_HYPHEN} \
            else m.group(1) + m.group(2)

    s = re.sub(r"(\w+)-\s+(\w+)", join, s)
    s = s.translate(dict.fromkeys(map(ord, "\u2013\u2014\u2012\u2015"), "-"))
    s = s.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
                     0x00A0: " "})
    return re.sub(r"\s+", " ", s).strip()


def brackets(text):
    """Each passage the book marks as proper to the Liturgy of St Basil."""
    lines = text.split("\n")
    try:
        first = next(i for i, l in enumerate(lines)
                     if l.strip().startswith("THE LITURGY OF ST. BASIL"))
    except StopIteration:
        return None, "the Liturgy is not where it should be in this text"
    seg = lines[first:first + 5600]
    opens = [i for i, l in enumerate(seg)
             if re.search(r"(?i)liturgy o[fp]\s*st\.?\s*basil", l)
             and re.match(r"\s*[\[\\|(]", l)]
    out = []
    for s in opens:
        end = next((j for j in range(s, min(s + 170, len(seg)))
                    if "]" in seg[j]), None)
        if end is None:
            return None, "a bracket opened at line %d and never closed" % s
        body = flatten("\n".join(seg[s:end + 1]), seg)
        # The rubric that opens the bracket is the book's own signpost and is
        # said again by the entry; the text begins after it.
        # Searched only in the opening of the passage, so that a "the Great"
        # further down in a prayer cannot be taken for the end of the rubric.
        head = body[:150]
        # The opening bracket and the italic "Or," are read several ways.
        m = re.match(r"[\[\\|(]?\s*(?:Or|But|At|If|CV|pr)\b"
                     r".*(?:be used|hath been used|the Great)\s*[,:;]?\s*",
                     head)
        if m and "Hymn" not in head[m.end():m.end() + 40]:
            body = body[m.end():]
            body = re.sub(r"^(?:this Prayer is said, secretly|this Prayer"
                          r"|the following Prayer)\s*[,:;]\s*", "", body,
                          count=1)
        else:
            # The last bracket names which hymn is sung and in which tone,
            # which is not a signpost but the thing itself, so it is kept.
            body = re.sub(r"^[\[\\|(]\s*", "", body)
        out.append(body.strip())
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    got, err = brackets(source())
    if err:
        print(err)
        return 1
    if len(got) != len(EXPECTED):
        print("%d prayers, %d expected" % (len(got), len(EXPECTED)))
        return 1

    applied = set()
    units = []
    for n, (body, want) in enumerate(zip(got, EXPECTED), start=1):
        for bad, good, page in FROM_THE_PAGE:
            if bad in body:
                body = body.replace(bad, good)
                applied.add(bad)
        if n == 13:
            body = HYMN + "\n\n" + body.replace(HYMN, "").replace("  ", " ")
            body = re.sub(r"\s+([,;.])", r"\1", body)
        if want not in body:
            print("prayer %d does not carry %r" % (n, want))
            return 1
        body = body.rstrip("] ").strip()
        # The book's brackets are its way of saying "this is St Basil's", and
        # every one of them should have been consumed by now. One left over
        # means a passage was cut in the wrong place.
        if "�" in body or "[" in body or "]" in body:
            print("prayer %d still carries a bracket or a lost character" % n)
            return 1
        units.append({
            "unit_id": "%s::u%02d" % (WORK["work_id"], n),
            "work_id": WORK["work_id"],
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": "liturgical",
            "ordinal": n,
            # Cited by its own opening words, which is how a prayer is named.
            "citation_anchor": " ".join(re.sub(r"^Choir\.[^\n]*\n\n", "",
                                               body).split()[:7]).rstrip(",;:"),
            "text": body,
        })

    missed = [b for b, _, _ in FROM_THE_PAGE if b not in applied]
    if missed:
        print("%d readings from the page found nothing to correct; the text "
              "has changed underneath them:" % len(missed))
        for m in missed:
            print("   %s..." % m[:60])
        return 1

    words = sum(len(u["text"].split()) for u in units)
    print("%d prayers, %s words" % (len(units), format(words, ",")))
    for u in units:
        print("  %2d  %5s words  %s" % (u["ordinal"],
                                        format(len(u["text"].split()), ","),
                                        u["citation_anchor"]))

    if args.write:
        OUT.write_text(json.dumps({"work": WORK, "units": units},
                                  ensure_ascii=False, indent=1),
                       encoding="utf-8")
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        cat = [w for w in cat if w["work_id"] != WORK["work_id"]]
        cat.append(dict(WORK))
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("\nwrote %s" % OUT.relative_to(ROOT))
    elif not args.check:
        print("\nnothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
