#!/usr/bin/env python3
"""
Build data/search-index.v5.json: one compact index covering every kind of
thing on the site, so a single search box can reach all of it.

The three HTML apps each hold their own dataset inline and none of them can
see the others'. This script reads all three, extracts the searchable spine of
each record, and writes a single small file that any page can fetch.

Record shape, kept terse because there are ~1,700 of them:

    k    kind: s=saint  p=prayer  w=library work  b=scripture book
         t=a tag on the shelf: a subject, an author, a century, a
           purpose or a translator. Opens the shelf already filtered.
    n    display name
    u    where it goes (URL, relative to site root)
    m    one line of context shown under the name
    d    feast date MM-DD, saints only
    g    1 if a great feast / major commemoration
    x    tag only: "<dimension>:<value>", the pair the shelf filters on.
         Kept beside the English name so a translation can replace the
         name without the link ceasing to work.
    c    tag only: how many titles carry it. The context line is composed
         from x and c rather than read from m, so it reads in whatever
         language the reader has chosen.

Run from the repository root:

    python3 tools/build_search_index.py
"""
import json
import re
import sys
from urllib.parse import quote
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "search-index.v5.json"


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
            "u": "/saints#n=" + name,
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
    """Works embedded in library.html plus those lazy-loaded from
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
        # The palette matches on this line as well as on the title, so what
        # a work was written to do is searchable from any page on the site.
        bits = [b for b in (w.get("author"), w.get("date"), w.get("purpose")) if b]
        out.append({
            "k": "w",
            "n": title,
            "u": "/library#work=" + wid,
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
            "u": "/library#book=" + str(nr),
            "m": "%s · %d language%s" % (b.get("group", ""), n, "" if n == 1 else "s"),
        })
    return out


def glossary(gl):
    out = []
    for e in gl.get("terms", []):
        forms = " · ".join(v for v in (e.get("forms") or {}).values())
        out.append({
            "k": "g",
            "n": e.get("t") or "",
            "u": "/glossary#" + e["id"],
            "m": (forms or ", ".join(e.get("tags") or []))[:90],
        })
    return out


# The shelf can be sorted by subject, by who wrote it, by century, by what a
# work was written to do, and by who translated it. Those are the tags, and
# until now they could only be reached by opening the Library and knowing the
# rail was there. Indexing them puts every one of them behind the same search
# box as everything else: type "martyrdom" anywhere on the site and the
# subject answers with the shelf already narrowed to it.
#
# The dimension order is the order the rail shows, and the order results
# group in.
TAG_DIMS = [("topics", "Subject"), ("author", "Author"), ("century", "Century"),
            ("purpose", "Purpose"), ("translator", "Translator")]


def tags(corpus, lazy):
    """One entry per distinct value of every dimension the shelf filters on."""
    works_all = list(corpus.get("works", [])) + list(lazy)
    # The shelf counts titles, not editions: the New Testament in nineteen
    # languages is one book on it. The count printed beside a tag is what the
    # reader will find after following it, so this has to collapse editions by
    # exactly the rule shelfKey() uses in library.html and not one that merely
    # resembles it. Grouping the Fathers by title and author instead of by
    # edition_of put "13 titles" over a shelf of twelve.
    groups = set()
    for w in works_all:
        if w.get("source_class") == "liturgical":
            g = re.sub(r"-[a-z]{2,3}$", "", w.get("work_id") or "")
            if g != (w.get("work_id") or ""):
                groups.add(g)

    def shelf_key(w):
        cls, wid = w.get("source_class"), w.get("work_id") or ""
        if cls == "liturgical":
            g = re.sub(r"-[a-z]{2,3}$", "", wid)
            if g in groups:
                return "lit:" + g
        if cls == "scripture":
            return "nt"
        return "w:" + (w.get("edition_of") or wid)

    # shelf() takes the English edition as the one that stands for the group
    # where there is one, and the tags are read off that edition. The Greek
    # Didache and the English name different translators, so taking whichever
    # came first put a translator on the shelf who is not the one shown.
    seen_title = {}
    for w in works_all:
        k = shelf_key(w)
        if k not in seen_title or w.get("language") == "en":
            if k in seen_title and seen_title[k].get("language") == "en":
                continue
            seen_title[k] = w

    # facetValues() in library.html reads `centuries` and never `century`, so
    # a work dated to more than one is counted under each of them.
    def values_of(w, dim):
        if dim == "century":
            return [str(c) for c in (w.get("centuries") or [])]
        v = w.get(dim)
        return v if isinstance(v, list) else ([v] if v else [])

    out = []
    for dim, label in TAG_DIMS:
        counts = {}
        for w in seen_title.values():
            for one in values_of(w, dim):
                one = str(one).strip()
                if one:
                    counts[one] = counts.get(one, 0) + 1
        for value, n in sorted(counts.items()):
            name = value + ("th century" if dim == "century" else "")
            out.append({
                "k": "t",
                "n": name,
                "u": "/library#browse=" + quote(dim + ":" + value, safe=""),
                "m": "%s · %d title%s" % (label, n, "" if n == 1 else "s"),
                "x": dim + ":" + value,
                "c": n,
            })
    return out


def refresh_ui_bundles(tag_entries):
    """Keep every translation of the shared chrome in step with the shelf.

    data/ui-i18n.v4.<lang>.json carries the words the search box and the theme
    toggle say, and a `tags` table giving the name of each tag on the shelf in
    that language. The tags themselves move as works are added, so the key set
    is refreshed here: a new tag arrives as an empty string, waiting to be
    written, and an empty string falls back to the English name rather than to
    nothing. A translation already written is never touched.

    English is the fallback and lives in the shared script; its file is the
    sheet a translator copies, and its tag table stays empty.
    """
    wanted = {}
    for e in tag_entries:
        wanted[e["x"]] = e["n"]
    for path in sorted((ROOT / "data").glob("ui-i18n.v4.*.json")):
        lang = path.name.split(".")[-2]
        if lang == "en":
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        have = d.get("tags") or {}
        d["tags"] = {k: have.get(k, "") for k in sorted(wanted)}
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        done = sum(1 for v in d["tags"].values() if v)
        print("  %s tags %d of %d" % (lang, done, len(wanted)))


def main():
    idx_html = (ROOT / "index.html").read_text(encoding="utf-8")
    sai_html = (ROOT / "saints.html").read_text(encoding="utf-8")
    rea_html = (ROOT / "library.html").read_text(encoding="utf-8")
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
    tag_entries = tags(one_line_assignment(rea_html, "CORPUS", " = {"), lazy)
    entries += tag_entries

    gl_path = ROOT / "data" / "glossary.v4.json"
    if gl_path.exists():
        entries += glossary(json.loads(gl_path.read_text(encoding="utf-8")))

    counts = {}
    for e in entries:
        counts[e["k"]] = counts.get(e["k"], 0) + 1

    payload = {"v": 5, "counts": counts, "e": entries}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print("wrote %s" % OUT.relative_to(ROOT))
    print("  saints  %5d" % counts.get("s", 0))
    print("  prayers %5d" % counts.get("p", 0))
    print("  works   %5d" % counts.get("w", 0))
    print("  books   %5d" % counts.get("b", 0))
    print("  terms   %5d" % counts.get("g", 0))
    print("  tags    %5d" % counts.get("t", 0))
    print("  total   %5d entries, %.0f KB" % (len(entries), kb))
    refresh_ui_bundles(tag_entries)
    return 0


if __name__ == "__main__":
    sys.exit(main())
