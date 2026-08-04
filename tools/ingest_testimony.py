#!/usr/bin/env python3
"""
What outsiders wrote about the Christians, while the Church was still young.

Everything else on the shelf is the Church describing herself. This is the
other kind of witness: a Roman governor, a Roman historian and a Greek
satirist, none of them Christians, all of them hostile, writing down what
these people did. A governor of Bithynia interrogating
Christians about 112 records that they met before dawn on a fixed day, sang
a hymn to Christ as to a god, bound themselves by oath against theft and
adultery and breach of faith, and met again later to eat together. He wrote
that to explain why he was executing them.

Testimony of this kind is worth exactly what it is and no more. It does not
teach the faith and it is not a Father. It establishes that the thing being
described was there to describe, in a form a stranger could recognise, within
living memory of the apostles.

Each passage is taken from a published public-domain translation and checked
against a phrase that must survive the fetch. If a source changes underneath
us the run stops rather than publish a paraphrase of somebody's summary.

    python3 tools/ingest_testimony.py --check
    python3 tools/ingest_testimony.py --write
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest import clean_text  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "library" / "outside-testimony.json"
INDEX = ROOT / "data" / "library" / "works-index.json"
CACHE = Path("/tmp/plithos-testimony")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"

WORK = {
    "work_id": "outside-testimony",
    "title": "The Christians in Outside Eyes",
    "author": "Witnesses outside the Church",
    "date": "1st to 2nd century",
    "translator": "William Stearns Davis (Pliny and Trajan); Alfred Church and "
                  "William Brodribb (Tacitus); H. W. Fowler and F. G. Fowler "
                  "(Lucian)",
    "pub_year": 1913,
    "source": "Readings in Ancient History, Vol. II; The Annals of Tacitus; "
              "The Works of Lucian of Samosata, Vol. IV",
    "source_class": "testimony",
    "description": "What men outside the Church wrote about the Christians in the "
                   "first two centuries: a Roman governor reporting to his emperor "
                   "on how they worshipped, a Roman historian on Nero's executions, "
                   "and a Greek satirist on how they cared for their own. None of "
                   "them believed; all of them were hostile; every one of them "
                   "describes a thing that was there to be described.",
    "digitized": "Fordham University; Wikisource; sacred-texts.com",
    "rights": "Public domain",
    "saint": None,
    "is_saint": False,
}

# Each entry: where it comes from, the span to take, and a phrase that has to
# survive. The phrase is the guard: a site can change its markup and still
# yield text, and the failure looks exactly like success.
SOURCES = [
    {
        "anchor": "Pliny the Younger to the Emperor Trajan, c. 112",
        "note": "Pliny governed Bithynia and Pontus. He is writing to ask how to "
                "try Christians, having already executed some, and describes their "
                "worship in the course of explaining the case.",
        "url": "https://sourcebooks.fordham.edu/ancient/pliny-trajan1.asp",
        "cache": "pliny.htm",
        "start": "It is my custom, Sire",
        "end": "if only there were a chance given for repentance.",
        "must": "on a fixed day they used to meet before dawn and recite a hymn",
    },
    {
        "anchor": "The Emperor Trajan to Pliny, c. 112",
        "note": "The reply. Anonymous accusations are not to be entertained, and "
                "Christians are not to be sought out; but those convicted are to "
                "be punished, and those who deny it and prove the denial by "
                "worshipping the gods are to be pardoned.",
        "url": "https://sourcebooks.fordham.edu/ancient/pliny-trajan1.asp",
        "cache": "pliny.htm",
        "start": "You have adopted the right course",
        "end": "they do not accord with the spirit of our age.",
        "must": "The Christians are not to be hunted out",
    },
    {
        "anchor": "Tacitus, Annals XV.44, c. 116",
        "note": "On the fire at Rome in the year 64 and the executions that "
                "followed it. Tacitus despises the Christians and says so, which "
                "is why the passage is worth what it is.",
        "url": "https://en.wikisource.org/wiki/The_Annals_(Tacitus)/Book_15",
        "cache": "tacitus15.htm",
        "start": "Such indeed were the precautions of human wisdom.",
        "end": "to glut one man's cruelty, that they were being destroyed.",
        "must": "Christus, from whom the name had its origin",
    },
    {
        "anchor": "Lucian of Samosata, The Passing of Peregrinus, c. 165",
        "note": "A satirist writing to mock a charlatan who imposed on the "
                "Christians. What he reports in passing, to explain how the fraud "
                "worked, is how they treated a man in prison and what they held "
                "about death.",
        "url": "https://www.sacred-texts.com/cla/luc/wl4/wl420.htm",
        "cache": "lucian.htm",
        "start": "It was now that he came across the priests",
        "end": "the contempt of death and voluntary self-devotion",
        "must": "was crucified on that account",
    },
]


def fetch(url, name, delay=1.0):
    p = CACHE / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(delay)
    return body


def page_text(body):
    """Plain text with real paragraph breaks kept and hard wraps removed.

    The sources wrap their lines inside a paragraph, and a newline from that
    wrapping looks exactly like a newline from a <p>. Matching a phrase that
    happens to straddle a wrap then fails for no visible reason. So the tags
    that start a paragraph are marked first, every other newline is flattened
    to a space, and the marks become the breaks.
    """
    MARK = "\x00"
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<sup\b.*?</sup>", "", body, flags=re.S | re.I)
    # Marginal section numbers are set inside the sentence they mark, so they
    # land mid-clause: "he came across the priests and scribes of the 11
    # Christians". They are apparatus, not text.
    body = re.sub(r'<span class="margnote".*?</span>', " ", body, flags=re.S | re.I)
    body = re.sub(r"<p[^>]*>\s*p\.\s*\d+\s*</p>", " ", body, flags=re.I)
    body = re.sub(r"<(p|br|div|h\d|tr|li)\b[^>]*>", MARK, body, flags=re.I)
    body = re.sub(r"</(p|div|h\d|tr|li)>", MARK, body, flags=re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(body)
    body = body.translate(dict.fromkeys(map(ord, "–—‒―"), "-"))
    body = body.translate({0x2018: "'", 0x2019: "'", 0x201C: '"',
                           0x201D: '"', 0x00A0: " "})
    body = body.replace("\n", " ").replace("\r", " ")
    paras = [re.sub(r"\s+", " ", p).strip() for p in body.split(MARK)]
    return "\n".join(p for p in paras if p)


def extract(src):
    raw = fetch(src["url"], src["cache"])
    text = page_text(raw)
    i = text.find(src["start"])
    if i < 0:
        return None, "opening phrase not found: %r" % src["start"]
    j = text.find(src["end"], i)
    if j < 0:
        return None, "closing phrase not found: %r" % src["end"]
    body = text[i:j + len(src["end"])].strip()
    if src["must"] not in body:
        return None, "the passage does not contain %r" % src["must"]
    paras = [p.strip() for p in body.split("\n") if p.strip()]
    return "\n\n".join(paras), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    units, failed = [], []
    for n, src in enumerate(SOURCES, start=1):
        body, err = extract(src)
        if err:
            failed.append((src["anchor"], err))
            print("  FAIL  %-46s %s" % (src["anchor"][:46], err))
            continue
        words = len(body.split())
        print("  ok    %-46s %5d words" % (src["anchor"][:46], words))
        units.append({
            "unit_id": "outside-testimony::u%02d" % n,
            "work_id": WORK["work_id"],
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": WORK["source_class"],
            "ordinal": n,
            "citation_anchor": src["anchor"],
            "note": src["note"],
            "text": body,
        })

    if failed:
        print("\n%d of %d passages failed; nothing written"
              % (len(failed), len(SOURCES)))
        return 1

    bad = sum(len(re.findall(r"[–—‘’“”]", u["text"]))
              for u in units)
    print("\n%d passages, %s words, %d dashes/smart quotes"
          % (len(units), format(sum(len(u["text"].split()) for u in units), ","), bad))

    if args.write:
        OUT.write_text(json.dumps({"work": WORK, "units": units},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
        cat = json.loads(INDEX.read_text(encoding="utf-8"))
        cat = [w for w in cat if w["work_id"] != WORK["work_id"]]
        cat.append(dict(WORK))
        cat.sort(key=lambda w: w["work_id"])
        INDEX.write_text(json.dumps(cat, ensure_ascii=False, indent=1),
                         encoding="utf-8")
        print("wrote %s" % OUT.relative_to(ROOT))
    elif not args.check:
        print("nothing written; pass --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
