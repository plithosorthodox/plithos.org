#!/usr/bin/env python3
"""
Pre-deploy sanity checks for plithos.org.

There is no build step, so this is the only gate between a commit and
production. It checks the things that have actually gone wrong on this site,
all of which were invisible in the browser:

  - a catalogue entry with no matching file (shows in the UI, opens empty)
  - a fetch target that does not exist (Cloudflare Pages answers those with
    HTTP 200 and the whole 6.8 MB of index.html, so nothing looks broken)
  - a stale search index after content changed
  - a page that lost its shared UI layer

Exit code 1 on any error. Warnings do not fail the build.

    python3 tools/check_site.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_library():
    idx = ROOT / "data" / "library" / "works-index.json"
    if not idx.exists():
        err("data/library/works-index.json is missing. plithos_reader.html "
            "fetches it unconditionally on every load.")
        return
    try:
        entries = json.loads(idx.read_text(encoding="utf-8"))
    except Exception as e:
        err("data/library/works-index.json is not valid JSON: %s" % e)
        return
    for w in entries:
        wid = w.get("work_id")
        if not wid:
            err("works-index.json has an entry with no work_id")
            continue
        f = ROOT / "data" / "library" / (wid + ".json")
        if not f.exists():
            err("works-index.json lists '%s' but data/library/%s.json does "
                "not exist. It would appear in the Library and open empty."
                % (wid, wid))
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            err("data/library/%s.json is not valid JSON: %s" % (wid, e))
            continue
        if not d.get("units"):
            err("data/library/%s.json has no units" % wid)


def check_library_dates():
    """Every work in the Library must say when it is from. The reader prints
    the date first and in bold, and drops the whole line when the field is
    absent, so a work with no date looks deliberate rather than incomplete.
    Nineteen scripture entries sat like that, and the catalogue entry for the
    canons lost its date to an installer that skipped an existing row instead
    of replacing it. Neither raised anything anywhere."""
    works = []
    idx = ROOT / "data" / "library" / "works-index.json"
    if idx.exists():
        try:
            works += [("works-index.json", w)
                      for w in json.loads(idx.read_text(encoding="utf-8"))]
        except Exception:
            return
    reader = ROOT / "plithos_reader.html"
    if reader.exists():
        s = reader.read_text(encoding="utf-8")
        try:
            i = s.index("const CORPUS")
            eq = s.index("=", i)
            j = s.index("\n", i)
            d = json.loads(s[eq + 1:j].rstrip().rstrip(";"))
            works += [("plithos_reader.html", w) for w in d.get("works", [])]
        except Exception:
            pass

    for where, w in works:
        wid = w.get("work_id") or "(no work_id)"
        if not w.get("date"):
            err("%s: '%s' has no date. The Library shows the date first, and "
                "shows nothing at all when it is missing." % (where, wid))
        # The reader reads these names and silently ignores any others, so a
        # renamed field is invisible rather than wrong.
        for field in ("title", "author"):
            if not w.get(field):
                warn("%s: '%s' has no %s" % (where, wid, field))
        # Scripture and the liturgy texts are named by their edition, not by a
        # translator, so either one satisfies the provenance line. Neither is
        # the case worth reporting.
        if not (w.get("translator") or w.get("source")):
            warn("%s: '%s' names neither a translator nor an edition"
                 % (where, wid))


def check_scripture():
    idx = ROOT / "scripture" / "index.json"
    if not idx.exists():
        err("scripture/index.json is missing")
        return
    d = json.loads(idx.read_text(encoding="utf-8"))
    for lang, nrs in (d.get("avail") or {}).items():
        for nr in nrs:
            if not (ROOT / "scripture" / lang / ("%d.json" % nr)).exists():
                err("scripture/index.json says %s has book %d but "
                    "scripture/%s/%d.json does not exist" % (lang, nr, lang, nr))


def check_bible_bundles():
    """UI languages whose New Testament bundle is absent. Not fatal - the
    loader now guards against it - but each one is a language quietly
    falling back to English."""
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r"const LANG_NAMES=\{(.*?)\};", idx, re.S)
    if not m:
        warn("could not find LANG_NAMES in index.html")
        return
    langs = re.findall(r"([a-z]{2,3}):\"", m.group(1))
    missing = [L for L in langs
               if L != "en" and not (ROOT / "data" / ("bible.v1.%s.b64" % L)).exists()]
    if missing:
        warn("no New Testament bundle for: %s (these languages fall back to "
             "English scripture)" % ", ".join(sorted(missing)))


def check_prayers():
    """prayers.html reads data/prayers.v2.json; index.html keeps its own inline
    copy for the calendar overlay. If they drift, the two disagree about what
    the prayer book contains."""
    p = ROOT / "data" / "prayers.v2.json"
    if not p.exists():
        err("data/prayers.v2.json is missing; prayers.html will load empty. "
            "Run tools/build_prayers.py.")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        err("data/prayers.v2.json is not valid JSON: %s" % e)
        return
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    i = idx.index("const PRAYERS=")
    j = idx.index("\n", i)
    inline = json.loads(idx[i + len("const PRAYERS="):j].rstrip().rstrip(";"))
    if len(inline) != len(d.get("prayers", [])):
        err("data/prayers.v2.json has %d prayers but index.html has %d. "
            "Run tools/build_prayers.py."
            % (len(d.get("prayers", [])), len(inline)))
        return
    sections = {s["id"] for s in d.get("sections", [])}
    for pr in d.get("prayers", []):
        if pr.get("s") not in sections:
            err("prayer %r has section %r, which is not declared. It would be "
                "unreachable on prayers.html." % (pr.get("title"), pr.get("s")))


def check_index_version():
    """The index is served immutable for a year under a versioned filename, so
    changing its content without changing its name leaves returning visitors
    searching last year's site. This catches the case the convention exists to
    prevent: the file the shared script asks for is not the one just built."""
    m = re.search(r'INDEX_URL\s*=\s*"([^"]+)"',
                  (ROOT / "assets" / "plithos-ui.v4.js").read_text(encoding="utf-8"))
    if not m:
        err("cannot find INDEX_URL in the shared script")
        return
    asked = m.group(1).split("/")[-1]
    built = re.search(r'search-index\.v\d+\.json',
                      (ROOT / "tools" / "build_search_index.py").read_text(encoding="utf-8"))
    if built and asked != built.group(0):
        err("the shared script fetches %s but the index is built as %s. One of "
            "them is a year out of date for every returning visitor."
            % (asked, built.group(0)))
    if not (ROOT / "data" / asked).exists():
        err("the shared script fetches data/%s, which does not exist. "
            "Cloudflare answers that with the whole of index.html." % asked)


def check_search_index():
    p = ROOT / "data" / "search-index.v2.json"
    if not p.exists():
        err("data/search-index.v2.json is missing; the command palette will "
            "open empty on every page")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        err("data/search-index.v2.json is not valid JSON: %s" % e)
        return
    counts = d.get("counts") or {}

    saints_html = (ROOT / "plithos_saints.html").read_text(encoding="utf-8")
    i = saints_html.index("const SAINTS=")
    j = saints_html.index("\n", i)
    n_saints = len(json.loads(saints_html[i + len("const SAINTS="):j].rstrip().rstrip(";")))
    if counts.get("s") != n_saints:
        err("search index is stale: %s saints indexed but plithos_saints.html "
            "has %d. Run tools/build_search_index.py."
            % (counts.get("s"), n_saints))

    lazy = ROOT / "data" / "library" / "works-index.json"
    if lazy.exists():
        n_lazy = len(json.loads(lazy.read_text(encoding="utf-8")))
        if n_lazy and counts.get("w", 0) < n_lazy:
            err("search index is stale: %s works indexed but the lazy "
                "catalogue alone has %d. Run tools/build_search_index.py."
                % (counts.get("w"), n_lazy))


CURVED_QUOTE_SCRIPTS = {"zh", "ja", "ko"}


def check_rule_i18n():
    """A translation of the Rule page must carry the same markup as the English.

    Each string is inserted as HTML, so a translation that loses an <a> loses
    the link to the source, and one that loses a <strong> loses the emphasis
    the sentence was built around. Neither shows up as an error anywhere: the
    page renders, in the reader's language, quietly missing the citation."""
    page = ROOT / "rule.html"
    if not page.exists():
        return
    src = page.read_text(encoding="utf-8")
    eng = {}
    for m in re.finditer(r"<(?:h1|h2|h3|p|li)\b([^>]*)>(.*?)</(?:h1|h2|h3|p|li)>",
                         src, re.S):
        km = re.search(r'data-t="([^"]+)"', m.group(1))
        if km:
            eng[km.group(1)] = m.group(2)
    if not eng:
        return

    langs = json.loads((ROOT / "data" / "rule-langs.json").read_text(encoding="utf-8")
                       ) if (ROOT / "data" / "rule-langs.json").exists() else {}
    for lang in (langs.get("langs") or []):
        if lang == "en":
            continue
        p = ROOT / "data" / ("rule-i18n.v1.%s.json" % lang)
        if not p.exists():
            err("data/rule-langs.json offers %s but data/%s does not exist. The "
                "picker would show a language that does nothing." % (lang, p.name))
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            err("%s is not valid JSON: %s" % (p.name, e))
            continue
        for k, e in eng.items():
            v = d.get(k)
            if not v:
                err("rule %s: no text for %s" % (lang, k))
                continue
            for label, pat in (("link", r'<a\s+href="[^"]+"'),
                               ("strong", r"<strong>"), ("em", r"<em>")):
                if len(re.findall(pat, e)) != len(re.findall(pat, v)):
                    err("rule %s, string %s: %d %s tags in English, %d in the "
                        "translation" % (lang, k, len(re.findall(pat, e)),
                                         label, len(re.findall(pat, v))))
            for a in re.findall(r'<a\s+href="([^"]+)"', e):
                if a not in v:
                    err("rule %s, string %s: the link to %s is gone"
                        % (lang, k, a))
            if re.search(r"[–—]", v):
                err("rule %s, string %s: an em or en dash; the house rule is "
                    "hyphens" % (lang, k))
            # Straight quotes are the house rule for the scripts that have a
            # straight quote. In Chinese, Japanese and Korean the curved marks
            # are the correct ones and a straight quote is the error, so the
            # rule does not reach them.
            if lang not in CURVED_QUOTE_SCRIPTS and re.search(r"[‘’“”]", v):
                err("rule %s, string %s: curly quotes; the house rule is "
                    "straight quotes" % (lang, k))


def check_pages():
    for name in ["index.html", "plithos_saints.html", "plithos_reader.html",
                 "prayers.html", "rule.html", "glossary.html", "contact.html"]:
        p = ROOT / name
        if not p.exists():
            err("%s is missing" % name)
            continue
        s = p.read_text(encoding="utf-8")
        if "assets/plithos-ui.v2.css" not in s:
            err("%s does not load the shared stylesheet" % name)
        if "assets/plithos-ui.v4.js" not in s:
            err("%s does not load the shared script" % name)
        if 'charset="utf-8"' not in s.lower():
            err("%s does not declare <meta charset=\"utf-8\">" % name)
        if 'href="contact.html"' not in s:
            warn("%s has no link to the contact page" % name)
    for name in ["assets/plithos-ui.v2.css", "assets/plithos-ui.v4.js",
                 "robots.txt", "sitemap.xml", "_headers", "_redirects"]:
        if not (ROOT / name).exists():
            err("%s is missing" % name)


# Wording that frames the content as processed rather than published. The
# site's authority rests on faithful transmission of the Church's texts;
# pipeline vocabulary in reader-visible copy undercuts it, and denying
# machine translation still raises the question. Working notes belong in
# docs/ and commit messages, which are not deployed.
PROCESS_TALK = [
    "machine-translat", "machine translat", "auto-generat", "autogenerat",
    "separate pass", "translation pass", "has not been done",
    "build script", "pipeline", "tools/", ".py",
]

# The embedded datasets sit on single enormous lines. Only shorter lines are
# hand-written markup, copy and comments, and only those are checked - the
# corpus itself legitimately contains words like "regenerate" (baptismal) and
# phrases like "another pass".
DATA_LINE = 2000


def check_voice():
    served = ["index.html", "plithos_saints.html", "plithos_reader.html",
              "prayers.html", "rule.html", "glossary.html", "contact.html",
              "assets/plithos-ui.v4.js", "assets/plithos-ui.v2.css"]
    for name in served:
        p = ROOT / name
        if not p.exists():
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if len(line) > DATA_LINE:
                continue
            low = line.lower()
            for phrase in PROCESS_TALK:
                if phrase in low:
                    err("%s line %d contains %r. Reader-visible copy must not "
                        "describe how the content was produced - see 'Voice of "
                        "the site' in CLAUDE.md." % (name, n, phrase))


def check_quotations():
    """Every blockquote on an authored page must appear verbatim in a text
    this site hosts. Patristic and scriptural quotations are not to be
    paraphrased, tidied, or stripped of a translator's brackets; this catches
    drift that reads perfectly well and is still wrong.

    The haystack is everything the site actually serves as a text: the library
    works, the prayer book, and the scripture bundle. A page may quote from any
    of them and from nothing else."""
    import html as _html
    corpus = []
    for f in sorted((ROOT / "data" / "library").glob("*.json")):
        if f.name == "works-index.json":
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        corpus.append(" ".join(u.get("text", "") for u in d.get("units", [])))

    p = ROOT / "data" / "prayers.v2.json"
    if p.exists():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            corpus.append(" ".join(pr.get("body", "") for pr in d.get("prayers", [])))
        except Exception:
            pass

    nt = ROOT / "data" / "bible.v1.en.b64"
    if nt.exists():
        try:
            import base64
            import zlib
            d = json.loads(zlib.decompress(base64.b64decode(nt.read_bytes())))
            for lang, books in d.items():
                for book, chapters in (books or {}).items():
                    if not isinstance(chapters, dict):
                        continue
                    for ch in chapters.values():
                        if isinstance(ch, dict):
                            corpus.append(" ".join(ch.values()))
        except Exception:
            pass
    for f in sorted((ROOT / "scripture" / "en").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for ch in (d.get("chapters") or d.get("ch") or {}).values():
            if isinstance(ch, dict):
                corpus.append(" ".join(str(v) for v in ch.values()))
            elif isinstance(ch, list):
                corpus.append(" ".join(str(v) for v in ch))

    def norm(t):
        t = re.sub(r"<[^>]+>", " ", t)
        return re.sub(r"\s+", " ", _html.unescape(t)).strip()

    hay = norm(" ".join(corpus))
    if not hay:
        return
    for name in ["rule.html"]:
        page = ROOT / name
        if not page.exists():
            continue
        for q in re.findall(r"<blockquote>(.*?)</blockquote>",
                            page.read_text(encoding="utf-8"), re.S):
            for piece in [x.strip() for x in norm(q).split("...") if len(x.strip()) > 40]:
                if piece not in hay:
                    err("%s quotes text that does not appear verbatim in any "
                        "hosted work: %r" % (name, piece[:70]))


def check_redirects():
    """An alias in _redirects shadows a real page. /prayers pointed at
    index.html from when prayers lived in a dropdown; once prayers.html
    existed, every link to it silently served the calendar instead."""
    red = ROOT / "_redirects"
    if not red.exists():
        return
    for line in red.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        src, dest = parts[0], parts[1]
        real = ROOT / (src.lstrip("/") + ".html")
        if real.exists() and dest.lstrip("/") != real.name:
            err("_redirects maps %s to %s, but %s exists. The alias wins and "
                "the real page becomes unreachable. Delete the alias."
                % (src, dest, real.name))


def check_headers():
    """/data/*.json once matched both /data/* and /*.json, and Cloudflare
    concatenated the two Cache-Control values into one malformed header."""
    s = (ROOT / "_headers").read_text(encoding="utf-8")
    rules = re.findall(r"^(/\S+)$", s, re.M)
    if "/*.json" in rules and any(r.startswith("/data/") for r in rules):
        err("_headers has both /*.json and a /data/ rule; they will both "
            "match /data/*.json and Cloudflare will emit two Cache-Control "
            "values in one header")


def check_build():
    """Every page must carry the build it is published as, and version.json
    must agree. When they drift, a reader holding an old copy of a page is
    never told, and a section that has since moved simply does nothing."""
    v = ROOT / "version.json"
    if not v.exists():
        err("version.json is missing; no page can tell it has been replaced. "
            "Run tools/stamp_build.py.")
        return
    try:
        build = json.loads(v.read_text(encoding="utf-8")).get("build")
    except Exception as e:
        err("version.json is not valid JSON: %s" % e)
        return
    if not build:
        err("version.json declares no build")
        return
    tag = '<meta name="plithos-build" content="%s">' % build
    for name in ["index.html", "plithos_saints.html", "plithos_reader.html",
                 "prayers.html", "rule.html", "glossary.html", "contact.html"]:
        p = ROOT / name
        if p.exists() and tag not in p.read_text(encoding="utf-8"):
            err("%s is not stamped %s. Run tools/stamp_build.py."
                % (name, build))


def main():
    check_pages()
    check_rule_i18n()
    check_build()
    check_library()
    check_library_dates()
    check_scripture()
    check_prayers()
    check_bible_bundles()
    check_search_index()
    check_index_version()
    check_voice()
    check_quotations()
    check_redirects()
    check_headers()

    for w in warnings:
        print("warning: %s" % w)
    for e in errors:
        print("ERROR: %s" % e)
    if errors:
        print("\n%d error(s). Not safe to deploy." % len(errors))
        return 1
    print("\nAll checks passed%s." %
          (" (%d warning(s))" % len(warnings) if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
