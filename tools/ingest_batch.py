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

    if entry["shape"] == "h2":
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
