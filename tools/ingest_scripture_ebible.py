#!/usr/bin/env python3
"""An Old Testament for the languages that had none.

    python3 tools/ingest_scripture_ebible.py --check sw
    python3 tools/ingest_scripture_ebible.py --write sw hi bn ur

Swahili, Hindi, Bengali and Urdu are offered here as languages of the site and
a reader who opened a reading from the Old Testament in any of them was given
it in English. There is no Orthodox edition in any of the four, and none of
the free editions carries the whole canon: what exists is the thirty-nine
books of the Hebrew canon, translated in the last forty years, and the entry
for each says so plainly so that a reader knows what he has and what he has
not.

Where more than one edition was free to take, the later was preferred.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "scripture" / "index.json"
CACHE = ROOT / ".cache" / "ebible"
UA = {"User-Agent": "plithos.org scripture ingest"}

# The books of the Hebrew canon, against the numbers this site gives them and
# the codes eBible uses. The site counts the four books of Kingdoms as the
# Septuagint does, so 9 to 12 are Samuel and Kings.
OT = [
    (1, "GEN"), (2, "EXO"), (3, "LEV"), (4, "NUM"), (5, "DEU"), (6, "JOS"),
    (7, "JDG"), (8, "RUT"), (9, "1SA"), (10, "2SA"), (11, "1KI"), (12, "2KI"),
    (13, "1CH"), (14, "2CH"), (15, "EZR"), (16, "NEH"), (17, "EST"),
    (18, "JOB"), (19, "PSA"), (20, "PRO"), (21, "ECC"), (22, "SNG"),
    (23, "ISA"), (24, "JER"), (25, "LAM"), (26, "EZK"), (27, "DAN"),
    (28, "HOS"), (29, "JOL"), (30, "AMO"), (31, "OBA"), (32, "JON"),
    (33, "MIC"), (34, "NAM"), (35, "HAB"), (36, "ZEP"), (37, "HAG"),
    (38, "ZEC"), (39, "MAL"),
]

SHORT = ("This edition carries the thirty-nine books of the Hebrew canon. "
         "The deuterocanonical books the Church reads with them are not in it.")

# lang -> (eBible id, name, autonym, edition, licence, direction, note)
EDITIONS = {
    "sw": ("swh_onmm", "Swahili", "Kiswahili", "Maandiko Matakatifu",
           "Copyright 2018, 2024 Biblica, Inc. Released for free use.",
           "ltr", SHORT),
    "hi": ("hin_cvb", "Hindi", "हिन्दी",
           "Hindi Contemporary Version",
           "Copyright 1978, 2009, 2016, 2019 Biblica, Inc. "
           "Released for free use.", "ltr", SHORT),
    "bn": ("ben_ocv", "Bengali", "বাংলা",
           "Bengali Contemporary Version",
           "Copyright 2022 Biblica, Inc. Released for free use.",
           "ltr", SHORT),
    "ur": ("urd_oucv", "Urdu", "اردو",
           "Urdu Contemporary Version",
           "Copyright 1999, 2005, 2022, 2024 Biblica, Inc. "
           "Released for free use.", "rtl", SHORT),
}


def get(url, tries=4):
    for i in range(tries):
        try:
            r = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(r, timeout=90) as h:
                return h.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if i == tries - 1:
                raise
            time.sleep(2 ** i)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def cached(key, url):
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / (key + ".json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    raw = get(url)
    if raw is None:
        return None
    p.write_bytes(raw)
    return json.loads(raw.decode("utf-8"))


def clean(t):
    t = t.replace(" ", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return re.sub(r"\s+([,.;:!?])", r"\1", t)


def names(tid):
    d = cached("%s.books" % tid,
               "https://bible.helloao.org/api/%s/books.json" % tid)
    out = {}
    for b in (d or {}).get("books", []):
        out[b["id"]] = b.get("name") or b.get("commonName") or b["id"]
    return out


def book(tid, code):
    """One book, as a list of chapters, each a list of verses.

    A verse the edition does not print is left as an empty string rather than
    closed up, so that the chapter still numbers as the edition numbers it.
    """
    chapters = []
    n = 1
    while True:
        d = cached("%s.%s.%d" % (tid, code, n),
                   "https://bible.helloao.org/api/%s/%s/%d.json" % (tid, code, n))
        if d is None:
            break
        verses = {}
        for item in d.get("chapter", {}).get("content", []):
            if item.get("type") != "verse":
                continue
            parts = [x for x in item.get("content", []) if isinstance(x, str)]
            for x in item.get("content", []):
                if isinstance(x, dict) and isinstance(x.get("text"), str):
                    parts.append(x["text"])
            t = clean(" ".join(parts))
            if t:
                verses[int(item["number"])] = t
        if not verses:
            break
        top = max(verses)
        chapters.append([verses.get(k, "") for k in range(1, top + 1)])
        n += 1
    return chapters


def build(lang, write):
    tid, name, autonym, edition, lic, direction, note = EDITIONS[lang]
    local = names(tid)
    out = ROOT / "scripture" / lang
    built, total = [], 0
    for nr, code in OT:
        chapters = book(tid, code)
        if not chapters:
            print("  FAIL  %-4s %s" % (nr, code))
            continue
        n = sum(len([v for v in c if v]) for c in chapters)
        total += n
        print("  ok    %-24s %2d -> %3d chapters %6s verses"
              % (local.get(code, code)[:24], nr, len(chapters), format(n, ",")))
        built.append((nr, code, chapters))
    print("\n%s: %d books, %s verses" % (lang, len(built), format(total, ",")))
    if len(built) != 39:
        print("  WARNING: %d books, expected 39" % len(built))
    if not write:
        return
    out.mkdir(parents=True, exist_ok=True)
    for nr, code, chapters in built:
        (out / ("%d.json" % nr)).write_text(
            json.dumps({"l": lang, "b": nr, "n": local.get(code, code),
                        "c": chapters},
                       ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    idx["langs"] = [l for l in idx["langs"] if l["code"] != lang]
    idx["langs"].append({
        "code": lang, "name": name, "autonym": autonym,
        "tradition": "masoretic", "edition": edition,
        "license": lic, "dir": direction, "note": note})
    idx["langs"].sort(key=lambda l: l["code"])
    idx["avail"][lang] = sorted(nr for nr, _c, _ch in built)
    idx["names"][lang] = {str(nr): local.get(code, code)
                          for nr, code, _ch in built}
    INDEX.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    print("wrote %d books and told the index about them" % len(built))
    import scripture_index
    scripture_index.sync()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("langs", nargs="*")
    a = ap.parse_args()
    for l in (a.langs or sorted(EDITIONS)):
        print("==", l)
        build(l, a.write)
    return 0


if __name__ == "__main__":
    sys.exit(main())
