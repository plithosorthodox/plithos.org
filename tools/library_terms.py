#!/usr/bin/env python3
"""
Give the Library's own words a language to be written in.

The Saints page and the calendar have carried every reader-facing word in a
language-keyed table for months. The Library carried some of them - RLEX has
seventy-four and every one of the twenty-one languages fills all seventy-four -
and said the rest in English no matter who was reading. A Korean reader picked
a collection from a list reading 전체 장서 and 교부, and the shelf it opened
called itself The whole shelf and The Fathers, on the same screen, because the
cards were built from the section's own English label instead of asking the
table that already had the answer.

Those are wired now. What this adds is the words that had nowhere to live:

    secHome            the first entry of the collection picker
    homeSub            the sentence under the title
    sec*Desc           the seven shelf descriptions, out of HOME_DESC
    secNTShelf/Desc    the New Testament's own heading, out of SHELF_TITLE
    cnt*               how a shelf counts what is on it - "%1 titles" and the
                       rest, patterns rather than a number with a word stuck
                       on the end, because counting is the language's business

Nothing here is translated. It puts the English in the table under a key, and
a key in RLEX.en is exactly what tools/loop_ui.py offers a lane: the queue is
derived from RLEX["en"], so a word added here is a word the lanes will be
asked for, in all twenty-one, without anything else being told about it.

    python3 tools/library_terms.py --check
    python3 tools/library_terms.py --write
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import check_i18n as ci                                      # noqa: E402

# key -> where the English already is, or the English itself
FROM_HOME_DESC = {
    "secBrowseDesc": "browse",   "secLiturgyDesc": "liturgy",
    "secOTDesc": "scripture",    "secNTDesc": "nt",
    "secFathersDesc": "fathers", "secCouncilsDesc": "councils",
    "secLivesDesc": "lives",
}
COUNTS = {
    "cntTitle": "%1 title",       "cntTitles": "%1 titles",
    "cntWork": "%1 work",         "cntWorks": "%1 works",
    "cntLiturgy": "%1 liturgy",   "cntLiturgies": "%1 liturgies",
    "cntLanguages": "%1 languages",
    "cntSeptuagint": "Septuagint · many languages",
}
# The words a work brings with it. These are not a list anybody maintains:
# they are read off the shelf itself, so a work added tomorrow puts its own
# subjects and its own use into the queue without this file being touched.
#
# Two fields are deliberately not here. A translator's name and the volume a
# text was taken from are the citation of an edition, and an edition is
# reproduced as it was printed - rendering "Ante-Nicene Fathers, Vol. 8" into
# Korean would be the site correcting a book it did not publish.
FACET_FIELDS = (("topics", True), ("purpose", False),
                ("period", False), ("author", False))

PLAIN = {
    "secHome": "Home",
    "homeSub": ("A library of the Fathers, the Scriptures, the Councils, and "
                "the Divine Liturgy of the Orthodox Church. Choose a "
                "collection to begin."),
}


def literal_of(src, var):
    for name, lit in ci.literals(src):
        if name == var:
            return lit
    raise SystemExit("no %s in library.html" % var)


def evaluate(src, var):
    o, err = ci.evaluate(literal_of(src, var))
    if o is None:
        raise SystemExit("%s would not evaluate: %s" % (var, err))
    return o


def serialise(obj):
    tmp = TOOLS / ".library-terms.js"
    tmp.write_text("const O=" + json.dumps(obj, ensure_ascii=False)
                   + ";process.stdout.write(JSON.stringify(O));",
                   encoding="utf-8")
    try:
        r = subprocess.run(["node", str(tmp)], capture_output=True, text=True,
                           timeout=180)
    finally:
        tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        raise SystemExit("node: " + r.stderr[:200])
    return r.stdout


def wanted(src):
    home = evaluate(src, "HOME_DESC")
    stitle = evaluate(src, "SHELF_TITLE")
    sdesc = evaluate(src, "SHELF_DESC")
    out = dict(PLAIN)
    out.update(COUNTS)
    for key, sec in FROM_HOME_DESC.items():
        if home.get(sec):
            out[key] = home[sec]
    if stitle.get("nt"):
        out["secNTShelf"] = stitle["nt"]
    if sdesc.get("nt"):
        out["secNTShelfDesc"] = sdesc["nt"]
    for t in facet_terms(src):
        out["lx:" + t] = t
    return out


def facet_terms(src):
    """Every subject, use, century and author the shelf actually carries."""
    works = [w for w in evaluate(src, "CORPUS") if isinstance(w, dict)]
    idx = ROOT / "data" / "library" / "works-index.json"
    if idx.exists():
        works += [w for w in json.loads(idx.read_text(encoding="utf-8"))
                  if isinstance(w, dict)]
    seen = set()
    for w in works:
        for field, listy in FACET_FIELDS:
            v = w.get(field)
            if not v:
                continue
            if listy:
                seen.update(x for x in v if isinstance(x, str) and x.strip())
            elif isinstance(v, str) and v.strip():
                seen.add(v)
    return sorted(seen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    page = ROOT / "library.html"
    src = page.read_text(encoding="utf-8")
    rlex = evaluate(src, "RLEX")
    en = rlex.get("en") or {}
    want = wanted(src)

    add = {k: v for k, v in want.items() if k not in en}
    print("RLEX.en carries %d keys; %d wanted, %d missing"
          % (len(en), len(want), len(add)))
    for k in sorted(add):
        print("   + %-16s %s" % (k, add[k][:64]))
    if not add:
        print("\nnothing to add")
        return 0
    if not a.write:
        print("\n%d key(s) to add" % len(add))
        return 0

    en.update(add)
    rlex["en"] = en
    shutil.copy(page, str(page) + ".bak")
    page.write_text(src.replace(literal_of(src, "RLEX"), serialise(rlex), 1),
                    encoding="utf-8")
    again = evaluate(page.read_text(encoding="utf-8"), "RLEX")
    if len(again.get("en", {})) != len(en) or len(again) != len(rlex):
        shutil.copy(str(page) + ".bak", page)
        raise SystemExit("RLEX did not come back whole; library.html restored")
    Path(str(page) + ".bak").unlink(missing_ok=True)
    print("\nRLEX.en now carries %d keys, %d languages"
          % (len(again["en"]), len(again)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
