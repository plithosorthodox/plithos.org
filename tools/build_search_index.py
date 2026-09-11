#!/usr/bin/env python3
"""
Build data/search-index.v10.<lang>.json: one compact index per language,
covering every kind of thing on the site, so a single search box can reach
all of it and answer in the language the reader chose.

The three HTML apps each hold their own dataset inline and none of them can
see the others'. This script reads all three, extracts the searchable spine of
each record, and writes a single small file that any page can fetch.

Record shape, kept terse because there are ~1,700 of them:

    k    kind: s=saint  p=prayer  w=library work  b=scripture book
         t=a tag on the shelf: a subject, an author, a century, a
           purpose or a translator. Opens the shelf already filtered.
    n    display name, in this file's language
    e    the English name, when the display name is not it. The box matches
         on both, so a reader who knows a saint by his English name finds
         him in a Greek index and is shown the Greek.
    u    where it goes (URL, relative to site root). Always built from the
         English name, because that is the key the page it opens looks up.
    m    one line of context shown under the name
    d    feast date MM-DD, saints only
    g    1 if a great feast / major commemoration
    x    tag only: "<dimension>:<value>", the pair the shelf filters on.
         Kept beside the English name so a translation can replace the
         name without the link ceasing to work.
    c    tag only: how many titles carry it. The context line is composed
         from x and c rather than read from m, so it reads in whatever
         language the reader has chosen.

Nothing here is translated. Every name is taken from a file this site
already publishes in that language - the saints from saint-names and the
calendar's own names, the prayers from the prayer bundles, the books from
the scripture index and the New Testament table, the terms from the
glossary. A name with no published translation keeps its English, which is
what the reader would have seen in any case.

Run from the repository root:

    python3 tools/build_search_index.py
"""
import json
import re
import sys
from urllib.parse import quote
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "search-index.v10.%s.json"


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
            # What the line under the name is made of, so it can be made
            # again in another language instead of being taken apart.
            "_type": r.get("type") or "",
            "_where": r.get("place") or r.get("region") or "",
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
            "_cat": r.get("cat") or "",
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
            # The title is the edition's own and stays as its title page has
            # it; who wrote it and what it was written to do are the shelf's
            # words, and the shelf has them in every language.
            "_author": w.get("author") or "",
            "_date": w.get("date") or "",
            "_purpose": w.get("purpose") or "",
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
            "_nr": nr,
            "_group": b.get("group", ""),
            "_langs": n,
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
            # The forms are Greek and Slavonic and stay as they are; the tags
            # are the glossary's own and it names them in every language.
            "_id": e["id"],
            "_forms": forms,
            "_tags": list(e.get("tags") or []),
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


# --------------------------------------------------------------------------
# The languages
#
# Every name below is read from a file this site already publishes. Nothing
# is composed here, and a name with no published translation keeps the
# English it had, which is what the reader was being shown before.
# --------------------------------------------------------------------------

def ui_langs(idx_html):
    """The languages the site offers, in the order the picker shows them."""
    m = re.search(r"LANG_NAMES=\{(.*?)\};", idx_html)
    return [x.group(1) for x in re.finditer(r"(\w+):\"", m.group(1))]


def load_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}
    return json.loads(path.read_text(encoding="utf-8"))


def brace_literal(src, name):
    """The whole of a brace-balanced assignment, parsed."""
    i = src.index(name)
    start = src.index("{", i)
    depth = 0
    for k in range(start, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if not depth:
                return json.loads(src[start:k + 1])
    raise SystemExit("%s never closes" % name)


def century_key(value):
    n = int(value)
    s, v = ["th", "st", "nd", "rd"], n % 100
    suf = s[(v - 20) % 10] if 0 <= (v - 20) % 10 < 4 else (s[v] if v < 4 else s[0])
    return "%d%s century" % (n, suf)


class Tongue(object):
    """Everything this site has already said in one language."""

    def __init__(self, lang, rlex, groups, nt_books, ot_books, gloss_tags):
        self.lang = lang
        self.en = lang == "en"
        d = ROOT / "data"
        # A saint is named in the Saints index and in the calendar, and the
        # two together name all but one of the 1,456.
        self.saints = {}
        if not self.en:
            self.saints.update(load_json(d / ("saint-names.v1.%s.json" % lang)))
            self.saints.update(load_json(d / ("calendar-names.v1.%s.json" % lang)))
        self.terms = {} if self.en else load_json(d / ("saint-terms.v5.%s.json" % lang))
        self.prayers = {} if self.en else load_json(d / ("prayers-i18n.v2.%s.json" % lang))
        self.gloss = {} if self.en else load_json(d / ("glossary-i18n.v1.%s.json" % lang))
        self.lex = rlex.get(lang) or rlex.get("en") or {}
        self.groups = groups
        self.nt = nt_books.get(lang) or {}
        self.ot = ot_books.get(lang) or {}
        self.gtags = gloss_tags
        # scripture/index.json carries a byte-order mark inside the Chinese
        # book names, which is invisible in a file and a stray glyph in a
        # search result.
        self.ot = dict((k, v.lstrip(u"\ufeff")) for k, v in self.ot.items())

    def lx(self, value):
        """A word off the Library's shelf: an author, a subject, a purpose."""
        return self.lex.get("lx:" + value) or value

    def term(self, value):
        return self.terms.get(value) or value

    def count(self, one, many, n):
        pat = self.lex.get(many if n != 1 else one) or "%1 " + many
        return pat.replace("%1", str(n))

    def line(self, *bits):
        return " · ".join([b for b in bits if b])[:90]

    def render(self, e):
        k, out = e["k"], dict(e)
        for key in [x for x in out if x.startswith("_")]:
            del out[key]
        if self.en:
            return out
        name, meta = out["n"], out["m"]
        if k == "s":
            name = self.saints.get(out["n"], out["n"])
            meta = self.line(self.term(e["_type"]), self.term(e["_where"]))
        elif k == "p":
            name = (self.prayers.get(out["n"]) or {}).get("title") or out["n"]
            cat = (self.groups.get(e["_cat"]) or {}).get(self.lang) or e["_cat"]
            meta = self.line(cat)
        elif k == "w":
            # The title belongs to the edition and is left where its title
            # page put it. The rest is the shelf speaking.
            meta = self.line(self.lx(e["_author"]), self.lx(e["_date"]),
                             self.lx(e["_purpose"]))
        elif k == "b":
            name = self.ot.get(str(e["_nr"])) or self.nt.get(out["n"]) or out["n"]
            grp = self.lex.get(GRP_KEY.get(e["_group"], "")) or e["_group"]
            meta = self.line(grp, self.count("cntLanguage", "cntLanguages",
                                             e["_langs"]))
        elif k == "g":
            # The glossary bundles are keyed by the term's id, not by the
            # heading it prints, and the two are not the same word.
            name = (self.gloss.get(e["_id"]) or [None])[0] or out["n"]
            tags = [(self.gtags.get(t) or {}).get(self.lang) or
                    t.replace("-", " ") for t in e["_tags"]]
            meta = e["_forms"] or ", ".join(tags)[:90]
        elif k == "t":
            # The shelf's tags are named in the shared chrome's own bundle
            # and composed there, so the index leaves them in English and
            # the page substitutes. One name, in one place.
            return out
        out["m"] = meta[:90]
        if name != out["n"]:
            out["e"] = out["n"]
            out["n"] = name
        return out


GRP_KEY = {"pentateuch": "grpLaw", "historical": "grpHistory",
           "wisdom": "grpWisdom", "prophets": "grpProphets",
           "deuterocanon": "grpDeutero"}


def refresh_ui_bundles(tag_entries, rlex):
    """Keep every translation of the shared chrome in step with the shelf.

    data/ui-i18n.v5.<lang>.json carries the words the search box and the theme
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
    # v5 is served immutable for a year, so the filled table goes out under a
    # new name and v5 is left exactly as the readers holding it have it.
    for old in sorted((ROOT / "data").glob("ui-i18n.v5.*.json")):
        lang = old.name.split(".")[-2]
        path = old.with_name("ui-i18n.v6.%s.json" % lang)
        if lang == "en":
            path.write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
            continue
        d = json.loads((path if path.exists() else old)
                       .read_text(encoding="utf-8"))
        have = d.get("tags") or {}
        lex = rlex.get(lang) or {}
        tags = {}
        for k in sorted(wanted):
            dim, value = k.split(":", 1)
            if have.get(k):
                tags[k] = have[k]
                continue
            # The Library already names its subjects, its authors, its
            # centuries and its purposes in this language. A tag is the same
            # word on a different page, so it is read from there rather than
            # asked for again.
            key = "lx:" + (century_key(value) if dim == "century" else value)
            tags[k] = lex.get(key, "")
        d["tags"] = tags
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        # A translator is a person, and his name is what his title page says
        # it is. Those are not gaps and are not counted as any.
        nameable = [k for k in tags if not k.startswith("translator:")]
        done = sum(1 for k in nameable if tags[k])
        print("  %s tags %d of %d (%d translators keep their own names)"
              % (lang, done, len(nameable), len(tags) - len(nameable)))


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

    rlex = brace_literal(rea_html, "RLEX")
    nt_books = brace_literal(rea_html, "NT_BOOK_NAMES")
    ot_books = (scrip.get("names") or {})
    prayers_meta = load_json(ROOT / "data" / "prayers.v2.json")
    gloss_all = load_json(ROOT / "data" / "glossary.v4.json")

    print("  saints  %5d" % counts.get("s", 0))
    print("  prayers %5d" % counts.get("p", 0))
    print("  works   %5d" % counts.get("w", 0))
    print("  books   %5d" % counts.get("b", 0))
    print("  terms   %5d" % counts.get("g", 0))
    print("  tags    %5d" % counts.get("t", 0))
    print("  total   %5d entries" % len(entries))

    total = 0
    for lang in ui_langs(idx_html):
        t = Tongue(lang, rlex, prayers_meta.get("groups") or {},
                   nt_books, ot_books, gloss_all.get("tagNames") or {})
        rows = [t.render(e) for e in entries]
        payload = {"v": 6, "lang": lang, "counts": counts, "e": rows}
        out = Path(str(OUT) % lang)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False,
                                  separators=(",", ":")), encoding="utf-8")
        kb = out.stat().st_size / 1024
        total += kb
        named = sum(1 for r in rows if "e" in r)
        print("  %-4s %4.0f KB, %d of %d named in the language"
              % (lang, kb, named, len(rows) - counts.get("t", 0)))
    print("  %d files, %.1f MB in all, one fetched per reader"
          % (len(ui_langs(idx_html)), total / 1024))
    refresh_ui_bundles(tag_entries, rlex)
    return 0


if __name__ == "__main__":
    sys.exit(main())
