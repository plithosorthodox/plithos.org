#!/usr/bin/env python3
"""
Build data/search-index.v1.json: one compact index covering every kind of
thing on the site, so a single search box can reach all of it.

The three HTML apps each hold their own dataset inline and none of them can
see the others'. This script reads all three, extracts the searchable spine of
each record, and writes a single small file that any page can fetch.

Record shape, kept terse because there are ~1,700 of them:

    k    kind: s=saint  p=prayer  w=library work  b=scripture book
    n    display name
    u    where it goes (URL, relative to site root)
    m    one line of context shown under the name
    d    feast date MM-DD, saints only
    g    1 if a great feast / major commemoration

Run from the repository root:

    python3 tools/build_search_index.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "search-index.v1.json"


def one_line_assignment(src, name, opener):
    """Pull `const NAME=<json>` off its single line and parse it."""
    needle = "const " + name + opener
    i = src.index(needle)
    start = i + len("const " + name)
    j = src.index("\n", i)
    raw = src[start:j].lstrip()
    if raw.startswith("="):
        raw = raw[1:]
    return json.loads(raw.strip().rstrip(";"))


def saints(records):
    out = []
    for r in records:
        name = r.get("name") or ""
        if not name:
            continue
        feasts = r.get("feasts") or []
        day = feasts[0] if feasts else ""
        bits = [b for b in (r.get("type"), r.get("place") or r.get("region")) if b]
        out.append({
            "k": "s",
            "n": name,
            "u": "plithos_saints.html#n=" + name,
            "m": " · ".join(bits)[:90],
            "d": day,
            "g": 1 if r.get("great") else 0,
        })
    return out


def prayers(records):
    out = []
    for i, r in enumerate(records):
        title = r.get("title") or ""
        if not title:
            continue
        out.append({
            "k": "p",
            "n": title,
            "u": "prayers.html#p=" + str(i),
            "m": (r.get("cat") or "")[:90],
        })
    return out


def works(corpus, lazy):
    """Works embedded in plithos_reader.html plus those lazy-loaded from
    data/library/works-index.json. Both are real library entries; only the
    delivery differs."""
    out = []
    seen = set()
    for w in list(corpus.get("works", [])) + list(lazy):
        wid = w.get("work_id")
        title = w.get("title") or ""
        if not wid or not title or wid in seen:
            continue
        seen.add(wid)
        bits = [b for b in (w.get("author"), w.get("date")) if b]
        out.append({
            "k": "w",
            "n": title,
            "u": "plithos_reader.html#work=" + wid,
            "m": " · ".join(bits)[:90],
        })
    return out


def books(index):
    out = []
    avail = index.get("avail", {})
    # A book is worth indexing if any language ships it.
    shipped = set()
    for langbooks in avail.values():
        shipped.update(langbooks)
    langs_for = {}
    for code, nrs in avail.items():
        for nr in nrs:
            langs_for.setdefault(nr, []).append(code)
    for b in index.get("books", []):
        nr = b.get("nr")
        if nr not in shipped:
            continue
        n = len(langs_for.get(nr, []))
        out.append({
            "k": "b",
            "n": b.get("en") or "",
            "u": "plithos_reader.html#book=" + str(nr),
            "m": "%s · %d language%s" % (b.get("group", ""), n, "" if n == 1 else "s"),
        })
    return out


def main():
    idx_html = (ROOT / "index.html").read_text(encoding="utf-8")
    sai_html = (ROOT / "plithos_saints.html").read_text(encoding="utf-8")
    rea_html = (ROOT / "plithos_reader.html").read_text(encoding="utf-8")
    scrip = json.loads((ROOT / "scripture" / "index.json").read_text(encoding="utf-8"))

    lazy_path = ROOT / "data" / "library" / "works-index.json"
    lazy = []
    if lazy_path.exists():
        lazy = json.loads(lazy_path.read_text(encoding="utf-8")) or []

    entries = []
    entries += saints(one_line_assignment(sai_html, "SAINTS", "=["))
    entries += prayers(one_line_assignment(idx_html, "PRAYERS", "=["))
    entries += works(one_line_assignment(rea_html, "CORPUS", " = {"), lazy)
    entries += books(scrip)

    counts = {}
    for e in entries:
        counts[e["k"]] = counts.get(e["k"], 0) + 1

    payload = {"v": 1, "counts": counts, "e": entries}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print("wrote %s" % OUT.relative_to(ROOT))
    print("  saints  %5d" % counts.get("s", 0))
    print("  prayers %5d" % counts.get("p", 0))
    print("  works   %5d" % counts.get("w", 0))
    print("  books   %5d" % counts.get("b", 0))
    print("  total   %5d entries, %.0f KB" % (len(entries), kb))
    return 0


if __name__ == "__main__":
    sys.exit(main())
