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
        err("data/library/works-index.json is missing. library.html "
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
    reader = ROOT / "library.html"
    if reader.exists():
        s = reader.read_text(encoding="utf-8")
        try:
            i = s.index("const CORPUS")
            eq = s.index("=", i)
            j = s.index("\n", i)
            d = json.loads(s[eq + 1:j].rstrip().rstrip(";"))
            works += [("library.html", w) for w in d.get("works", [])]
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


def shared_script():
    """The versioned shared script the pages actually load.

    Read from a page rather than named here. Bumping the version means
    renaming the file and editing seven pages, and a checker that carries an
    eighth copy of the name is one more thing to forget: it would go looking
    for a file that had moved and report the site broken, or worse, keep
    passing against the version nobody serves any more."""
    m = re.search(r'assets/(plithos-ui\.v\d+\.js)',
                  (ROOT / "index.html").read_text(encoding="utf-8"))
    if not m:
        err("index.html loads no versioned shared script")
        return None
    p = ROOT / "assets" / m.group(1)
    if not p.exists():
        err("the pages load assets/%s, which does not exist" % m.group(1))
        return None
    return p


def index_asked_for():
    """The name of the search index the shared script fetches."""
    p = shared_script()
    if not p:
        return None
    m = re.search(r'INDEX_URL\s*=\s*"([^"]+)"', p.read_text(encoding="utf-8"))
    if not m:
        err("cannot find INDEX_URL in the shared script")
        return None
    return m.group(1).split("/")[-1]


def check_index_version():
    """The index is served immutable for a year under a versioned filename, so
    changing its content without changing its name leaves returning visitors
    searching last year's site. This catches the case the convention exists to
    prevent: the file the shared script asks for is not the one just built."""
    asked = index_asked_for()
    if not asked:
        return
    built = re.search(r'search-index\.v\d+\.json',
                      (ROOT / "tools" / "build_search_index.py").read_text(encoding="utf-8"))
    if built and asked != built.group(0):
        err("the shared script fetches %s but the index is built as %s. One of "
            "them is a year out of date for every returning visitor."
            % (asked, built.group(0)))
    if not (ROOT / "data" / asked).exists():
        err("the shared script fetches data/%s, which does not exist. "
            "Cloudflare answers that with the whole of index.html." % asked)


def check_saint_terms_version():
    """The same trap as the index, one page over.

    data/saint-terms.v*.json is served immutable for a year. The Saints page
    names it in a fetch and the builder writes it; if the two drift apart, a
    returning reader keeps last year's vocabulary beside this year's lives,
    and there is nothing on the page to tell him so."""
    page = (ROOT / "saints.html").read_text(encoding="utf-8")
    asked = re.search(r'saint-terms\.v\d+\.', page)
    built = re.search(r'saint-terms\.v\d+\.',
                      (ROOT / "tools" / "build_saint_terms.py").read_text(encoding="utf-8"))
    if not asked or not built:
        return
    if asked.group(0) != built.group(0):
        err("the Saints page fetches %s<lang>.json but the vocabulary is built "
            "as %s<lang>.json. One of them is a year out of date for every "
            "returning visitor." % (asked.group(0), built.group(0)))
        return
    # Earlier versions stay where they are: they were served immutable, so
    # browsers hold them, and a page held from before a bump still asks for
    # that exact name.


def check_saint_lives_version():
    """And the same again for the lives themselves.

    The lives are the largest thing the Saints page fetches and the slowest
    to be written, a language arriving over many sittings. Every sitting
    rewrites the file under the same name, so a reader who opened a life
    while a language was half done holds that half for a year unless the
    name moves with the content."""
    page = (ROOT / "saints.html").read_text(encoding="utf-8")
    asked = re.search(r'saint-lives\.v\d+\.', page)
    built = re.search(r'saint-lives\.v\d+\.',
                      (ROOT / "tools" / "build_saint_lives.py").read_text(encoding="utf-8"))
    if not asked or not built:
        return
    if asked.group(0) != built.group(0):
        err("the Saints page fetches %s<lang>.json but the lives are built "
            "as %s<lang>.json. One of them is a year out of date for every "
            "returning visitor." % (asked.group(0), built.group(0)))
        return
    for lang in ("el", "ru"):
        if not (ROOT / "data" / ("%s%s.json" % (asked.group(0), lang))).exists():
            err("the Saints page fetches data/%s%s.json, which does not "
                "exist. Cloudflare answers that with the whole of index.html."
                % (asked.group(0), lang))


def check_search_index():
    asked = index_asked_for()
    if not asked:
        return
    p = ROOT / "data" / asked
    if not p.exists():
        err("data/%s is missing; the command palette will open empty on "
            "every page" % asked)
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        err("data/%s is not valid JSON: %s" % (asked, e))
        return
    counts = d.get("counts") or {}

    saints_html = (ROOT / "saints.html").read_text(encoding="utf-8")
    i = saints_html.index("const SAINTS=")
    j = saints_html.index("\n", i)
    n_saints = len(json.loads(saints_html[i + len("const SAINTS="):j].rstrip().rstrip(";")))
    if counts.get("s") != n_saints:
        err("search index is stale: %s saints indexed but saints.html "
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
        p = ROOT / "data" / ("rule-i18n.v4.%s.json" % lang)
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


def shared_assets():
    """The versioned names of the shared stylesheet and script, taken from the
    calendar rather than written here. A bump has to be applied to all seven
    pages, and the check should be that they agree with each other, not that
    they agree with a number in this file that would have to be edited too."""
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    out = []
    for pat in (r'assets/plithos-ui\.v\d+\.css', r'assets/plithos-ui\.v\d+\.js'):
        m = re.search(pat, s)
        if not m:
            err("index.html does not load a shared %s" % pat.rsplit(".", 1)[-1])
            return None
        out.append(m.group(0))
    return out


def check_pages():
    assets = shared_assets()
    for name in ["index.html", "saints.html", "library.html",
                 "prayers.html", "rule.html", "glossary.html", "contact.html"]:
        p = ROOT / name
        if not p.exists():
            err("%s is missing" % name)
            continue
        s = p.read_text(encoding="utf-8")
        if assets:
            if assets[0] not in s:
                err("%s does not load %s. The shared layer is versioned in its "
                    "filename and a bump has to reach all seven pages together."
                    % (name, assets[0]))
            if assets[1] not in s:
                err("%s does not load %s. The shared layer is versioned in its "
                    "filename and a bump has to reach all seven pages together."
                    % (name, assets[1]))
        if 'charset="utf-8"' not in s.lower():
            err("%s does not declare <meta charset=\"utf-8\">" % name)
        if 'href="/contact"' not in s:
            warn("%s has no link to the contact page" % name)
    for name in (assets or []) + ["robots.txt", "sitemap.xml",
                                  "_headers", "_redirects"]:
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


def check_sitemap():
    """Every URL offered to a search engine must be the one that answers.

    The sitemap advertised /saints and /library while the pages were named
    plithos_saints.html and plithos_reader.html. Cloudflare answered both
    with a 308, so Google fetched the sitemap, followed a redirect on every
    entry, and indexed one page out of seven. Nothing here caught it, because
    nothing here read the sitemap. This does.

    A <loc> is served directly only when a file of that name exists:
    https://plithos.org/saints needs saints.html, and the bare origin needs
    index.html. Anything else is a redirect or a 404 wearing a sitemap entry.
    """
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        return
    src = sm.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", src)
    if not locs:
        err("sitemap.xml lists no URLs")
        return

    # Paths that _redirects sends elsewhere, which must never be advertised.
    sent_away = set()
    red = ROOT / "_redirects"
    if red.exists():
        for line in red.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 3 and parts[2].startswith("3"):
                    sent_away.add(parts[0])

    for loc in locs:
        if not loc.startswith("https://plithos.org/"):
            err("sitemap.xml lists %s; every URL must be an https://plithos.org "
                "address, or Google indexes a host you did not mean" % loc)
            continue
        path = loc[len("https://plithos.org"):]
        if path.endswith(".html"):
            err("sitemap.xml lists %s. Cloudflare 308s the .html form to the "
                "extensionless path, so this entry is a redirect. List %s."
                % (loc, path[:-len(".html")] or "/"))
            continue
        if path in sent_away:
            err("sitemap.xml lists %s, which _redirects sends elsewhere. A "
                "sitemap entry that redirects is not indexed." % loc)
            continue
        name = "index.html" if path == "/" else path.lstrip("/") + ".html"
        if not (ROOT / name).exists():
            err("sitemap.xml lists %s, but %s does not exist, so that path is "
                "a redirect or a 404. Rename the file to match the URL you "
                "want indexed - do not add a rewrite." % (loc, name))
            continue
        page = (ROOT / name).read_text(encoding="utf-8")
        m = re.search(r'<link rel="canonical" href="([^"]+)"', page)
        if not m:
            err("%s declares no canonical URL. Without one Google picks its "
                "own and may index a duplicate instead." % name)
        elif m.group(1) != loc:
            err("%s declares canonical %s but the sitemap offers %s. They must "
                "be the same URL, or Google indexes neither with confidence."
                % (name, m.group(1), loc))
        if '<meta name="description"' not in page:
            warn("%s has no meta description; Google will invent a snippet "
                 "from the page text" % name)


def check_decoding():
    """No served text may carry a replacement character.

    U+FFFD is never text. It is what a decoder leaves behind when it was
    told the wrong encoding, and it is invisible in review because the rest
    of the page still reads correctly. Eight Greek works reached the shelf
    carrying four hundred and sixteen of them, from pages CCEL serves as
    windows-1252 that were being read as UTF-8. Every phrase check in the
    ingesters passed, because the damage was never inside the phrase.
    """
    def report(name, bad):
        if bad:
            err("%s: %d replacement characters. U+FFFD is a failed decode, "
                "not text; the source was read in the wrong encoding."
                % (name, bad))

    for f in sorted((ROOT / "data" / "library").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        units = d.get("units") if isinstance(d, dict) else None
        if not units:
            continue
        report(f.name, sum(u.get("text", "").count("\ufffd") for u in units))

    # Scripture is read the same way, and it is the text this site can least
    # afford to serve broken. The Chinese New Testament carried five.
    for f in sorted((ROOT / "scripture").rglob("*.json")):
        report(str(f.relative_to(ROOT)),
               f.read_text(encoding="utf-8").count("\ufffd"))
    for f in sorted((ROOT / "data").glob("bible.v*.b64")):
        try:
            t = zlib.decompress(base64.b64decode(f.read_bytes())).decode("utf-8")
        except Exception:
            continue
        report(f.name, t.count("\ufffd"))
    for f in sorted((ROOT / "data").glob("prayers-i18n.*.json")):
        report(f.name, f.read_text(encoding="utf-8").count("\ufffd"))


def check_voice():
    served = ["index.html", "saints.html", "library.html",
              "prayers.html", "rule.html", "glossary.html",
              "contact.html"] + (shared_assets() or [])
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
    for name in ["index.html", "saints.html", "library.html",
                 "prayers.html", "rule.html", "glossary.html", "contact.html"]:
        p = ROOT / name
        if p.exists() and tag not in p.read_text(encoding="utf-8"):
            err("%s is not stamped %s. Run tools/stamp_build.py."
                % (name, build))


def check_ui_coverage():
    """A language offered in the picker whose chrome is still English.

    The Saints page carried its whole interface - the heading, the filters,
    the count, and the month names - in three languages while the picker
    offered twenty-two, and nothing here noticed through five completed
    languages. A missing key falls back to English silently, which is right
    for the reader and invisible to everyone else, so it has to be counted.
    """
    page = ROOT / "saints.html"
    s = page.read_text(encoding="utf-8")
    m = re.search(r"(?:const|var|let)\s+SUI\s*=\s*\{", s)
    if not m:
        err("saints.html has no SUI table")
        return
    i = s.index("{", m.end() - 1)
    d, j = 0, i
    while j < len(s):
        if s[j] == "{":
            d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                break
        j += 1
    body = s[i:j + 1]

    def sub(k):
        mm = re.search(r"[{,]\s*[\"\']?%s[\"\']?\s*:\s*\{" % k, body)
        if not mm:
            return None
        ii = body.index("{", mm.end() - 1)
        dd, jj = 0, ii
        while jj < len(body):
            if body[jj] == "{":
                dd += 1
            elif body[jj] == "}":
                dd -= 1
                if dd == 0:
                    break
            jj += 1
        return body[ii:jj + 1]

    lm = re.search(r"LANG_NAMES\s*=\s*\{", s)
    li = s.index("{", lm.end() - 1)
    ld, lj = 0, li
    while lj < len(s):
        if s[lj] == "{":
            ld += 1
        elif s[lj] == "}":
            ld -= 1
            if ld == 0:
                break
        lj += 1
    # The offered languages are read from the picker rather than listed here,
    # so a language added to one and not the other cannot pass unnoticed.
    offered = re.findall(r"[{,]\s*[\"\']?([a-z]{2,3})[\"\']?\s*:", s[li:lj + 1])

    en = sub("en")
    keys = set(re.findall(r"[{,]\s*[\"\']?([A-Za-z_][\w]*)[\"\']?\s*:", en))
    written = []
    for lang in offered:
        t = sub(lang)
        if t is None:
            continue
        have = set(re.findall(r"[{,]\s*[\"\']?([A-Za-z_][\w]*)[\"\']?\s*:", t))
        short = keys - have
        if short:
            err("saints.html SUI %s is missing %d string(s): %s"
                % (lang, len(short), " ".join(sorted(short)[:6])))
        else:
            written.append(lang)
    print("saints.html interface written in %d of %d offered languages: %s"
          % (len(written), len(offered), " ".join(written)))
    silent = [l for l in offered if sub(l) is None]
    if silent:
        warn("saints.html interface is still English for: %s" % " ".join(silent))


def main():
    check_pages()
    check_rule_i18n()
    check_build()
    check_library()
    check_library_dates()
    check_decoding()
    check_scripture()
    check_prayers()
    check_bible_bundles()
    check_search_index()
    check_index_version()
    check_saint_terms_version()
    check_saint_lives_version()
    check_voice()
    check_quotations()
    check_redirects()
    check_headers()
    check_sitemap()
    check_ui_coverage()

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
