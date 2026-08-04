#!/usr/bin/env python3
"""
Add St John of Damascus on the holy images.

The shelf could say what the Church holds about icons only through one
chapter of the Exposition of the Faith. This is the defence itself: three
apologies written between 726 and 730, while the emperor was having them
taken down, arguing that the Word became flesh and that what has been seen
may be depicted, and that the honour paid to the image passes to its
prototype. The Seventh Council settled the matter on these grounds.

Sourced from Project Gutenberg's edition of Mary H. Allies' translation,
London 1898, public domain. CCEL has the same book but renders its text
through a script, so the pages carry only page numbers; the ThML source it
publishes is metadata. That route was tried first and abandoned.

The three sermons that follow the apologies are on the Dormition of the
Theotokos. Allies titles them "On the Assumption" and sets the Greek beside
it, and the Greek is koimesis, the falling asleep. Her headings are kept
exactly as she set them, Greek and all, and what they are is said in the
description instead. An earlier pass renamed them in the citation line, which
is the site correcting a translator in her own edition; that is not ours to
do, and the note belongs where the site is speaking in its own voice.

    python3 tools/ingest_images.py --check
    python3 tools/ingest_images.py --write
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "library" / "john-damascus-holy-images.json"
INDEX = ROOT / "data" / "library" / "works-index.json"
CACHE = Path("/tmp/plithos-images")
CACHE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PlithosLibraryBuilder/1.0; +https://plithos.org)"
SRC = "https://www.gutenberg.org/cache/epub/49917/pg49917-images.html"

WORK = {
    "work_id": "john-damascus-holy-images",
    "title": "On the Holy Images",
    "author": "St John of Damascus",
    "date": "726-730",
    "translator": "Mary H. Allies",
    "pub_year": 1898,
    "source": "St John Damascene on Holy Images, followed by three sermons on "
              "the Dormition",
    "publisher": "Thomas Baker, London",
    "source_class": "patristic",
    "description": "Three apologies written while the images were being taken "
                   "down by imperial order, and the defence on which the Seventh "
                   "Ecumenical Council settled the question: that the invisible "
                   "God, having become visible in the flesh, may be depicted in "
                   "what He assumed; that the honour paid to the image passes to "
                   "the one it represents; and that matter is not despised by the "
                   "God who made it and was born into it. Parts I, II and III are "
                   "the three apologies, each gathering the testimony of earlier "
                   "Fathers behind it. The three sermons that follow are on the "
                   "Dormition of the Theotokos; the translator gives them the "
                   "Western title and sets the Greek beside it, and the Greek is "
                   "koimesis, the falling asleep.",
    "digitized": "Project Gutenberg",
    "rights": "Public domain",
    "saint": "Venerable John of Damascus",
    "is_saint": True,
}

# The six top-level divisions, in order, with the citation each one takes.
# The headings are matched exactly as the edition sets them, so a change in
# the source shows up as a missing section rather than as a silent join.
# The citation is the edition's own division, not a description of it.
SECTIONS = [
    (r"PART I\. APOLOGIA OF ST JOHN DAMASCENE AGAINST THOSE WHO DECRY HOLY IMAGES\.",
     "Part I. Apologia Against Those Who Decry Holy Images"),
    (r"PART II\.", "Part II"),
    (r"PART III\.", "Part III"),
    (r"SERMON I\. ON THE ASSUMPTION", "Sermon I. On the Assumption (κοίμησις)"),
    (r"SERMON II\. ON THE ASSUMPTION", "Sermon II. On the Assumption (κοίμησις)"),
    (r"SERMON III\. ON THE ASSUMPTION", "Sermon III. On the Assumption (κοίμησις)"),
]
END = r"^INDEX$"

# One phrase per section that has to survive the fetch.
MUST = [
    "I see the Church which God founded on the Apostles",
    "I crave",
    "Every one must recognise",
    "",
    "",
    "",
]


def fetch():
    p = CACHE / "icons.html"
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(SRC, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        body = r.read().decode("utf-8", errors="replace")
    p.write_text(body, encoding="utf-8")
    time.sleep(1.0)
    return body


def to_text(seg):
    """House-style plain text. Greek and every other non-Latin script is
    carried through untouched; only the typography is normalised."""
    seg = re.sub(r"<(script|style)\b.*?</\1>", " ", seg, flags=re.S | re.I)
    # Gutenberg sets footnote markers as superscript links.
    seg = re.sub(r"<sup\b.*?</sup>", "", seg, flags=re.S | re.I)
    seg = re.sub(r'<a [^>]*class="[^"]*(pginternal|fnanchor)[^"]*"[^>]*>.*?</a>',
                 "", seg, flags=re.S | re.I)
    seg = re.sub(r"<(p|div|br|h\d|li|blockquote)\b[^>]*>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"</(p|div|h\d|li|blockquote)>", "\n\n", seg, flags=re.I)
    seg = re.sub(r"<[^>]+>", "", seg)
    seg = html.unescape(seg)
    seg = seg.translate(dict.fromkeys(map(ord, "–—‒―"), "-"))
    seg = seg.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
                         0x00A0: " "})
    paras = [re.sub(r"[ \t]+", " ", p).strip() for p in re.split(r"\n\s*\n", seg)]
    # A bare page number on its own line is apparatus, not text.
    paras = [p for p in paras if p and not re.fullmatch(r"\[?\d+\]?", p)]
    return "\n\n".join(paras)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    body = fetch()

    # The edition sets a page-number <span> inside its headings, so the
    # heading text is not adjacent to the tag that opens it. Strip each
    # heading to its words first, then match.
    heads = []
    for m in re.finditer(r"<h[1-4][^>]*>(.*?)</h[1-4]>", body, re.S | re.I):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
        heads.append((m.start(), re.sub(r"\s+", " ", t).strip()))

    end = next((pos for pos, t in heads if re.match(END, t, re.I)), None)
    if end is None:
        print("the index heading that ends the text was not found")
        return 1

    starts = []
    for pat, name in SECTIONS:
        hits = [pos for pos, t in heads if re.match(pat, t, re.I) and pos < end]
        if not hits:
            print("  FAIL  heading not found: %s" % name)
            return 1
        starts.append((hits[-1], name))
    if [s for s, _ in starts] != sorted(s for s, _ in starts):
        print("  FAIL  the sections are not in the order the edition prints them")
        return 1

    units = []
    for i, (pos, name) in enumerate(starts):
        stop = starts[i + 1][0] if i + 1 < len(starts) else end
        text = to_text(body[pos:stop])
        head, _, rest = text.partition("\n\n")
        if MUST[i] and MUST[i] not in rest:
            print("  FAIL  %-52s missing %r" % (name, MUST[i]))
            return 1
        units.append({
            "unit_id": "john-damascus-holy-images::u%02d" % (i + 1),
            "work_id": WORK["work_id"],
            "work_title": WORK["title"],
            "author": WORK["author"],
            "source_class": WORK["source_class"],
            "ordinal": i + 1,
            "citation_anchor": name,
            "chapter_title": re.sub(r"\s+", " ", head).strip(),
            "text": rest.strip(),
        })
        print("  ok    %-52s %6d words" % (name, len(rest.split())))

    greek = sum(len(re.findall(r"[Ͱ-Ͽἀ-῿]", u["text"]))
                for u in units)
    bad = sum(len(re.findall(r"[–—‘’“”]", u["text"]))
              for u in units)
    print("\n%d sections, %s words, %d Greek characters carried, "
          "%d dashes/smart quotes"
          % (len(units), format(sum(len(u["text"].split()) for u in units), ","),
             greek, bad))

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
