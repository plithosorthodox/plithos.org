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

# The languages that answer at a path of their own, served by
# functions/<lang>/. Kept beside the other constants so a language added
# there and forgotten here fails loudly rather than silently.
LANG_PATHS = {"el", "ru", "ro", "uk", "de", "es", "ar", "fr", "pt", "it",
              "sr", "ka", "zh", "ja", "ko", "sw", "hy", "arc", "hi",
              "bn", "ur"}
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
    blank = [w.get("work_id") for w in entries if not w.get("language")]
    if blank:
        err("%d works in works-index.json do not say what language their "
            "edition is in: %s. library.html fills that in itself, in two "
            "places, so nothing looks wrong and the catalogue says nothing "
            "where the reader is shown English. Run "
            "tools/catalogue_language.py."
            % (len(blank), ", ".join(sorted(blank)[:4])
               + (" and others" if len(blank) > 4 else "")))
    else:
        print("%d works in the Library, every one naming its edition's "
              "language" % len(entries))


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
               if L != "en"
               and not (ROOT / "data" / ("bible.v4.%s.b64" % L)).exists()]
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
    for lang in ("en", "el", "ru"):
        if not (ROOT / "data" / ("%s%s.json" % (asked.group(0), lang))).exists():
            err("the Saints page fetches data/%s%s.json, which does not "
                "exist. Cloudflare answers that with the whole of index.html."
                % (asked.group(0), lang))

    # English is a file like the rest now. A life back in the index is 2.17 MB
    # sent to every reader whether he opens one or not, so it fails here
    # rather than being noticed in a page-weight audit six months later.
    i = page.index("const SAINTS=")
    j = page.index("\n", i)
    try:
        saints = json.loads(page[i + len("const SAINTS="):j].rstrip().rstrip(";"))
    except Exception:
        return
    back = [s["name"] for s in saints if "life" in s]
    if back:
        err("%d saints carry their life inside saints.html again (%s). The "
            "lives belong in data/saint-lives.v6.<lang>.json."
            % (len(back), back[0]))
    else:
        print("%d saints in the index, their lives in files" % len(saints))


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
        # A language path is answered by functions/<lang>/, which hands back
        # the page's own file with its language set. It is not a rewrite and
        # not a redirect: the address answers, with the page it names. What
        # has to exist is the handler and the file it will serve.
        parts = path.strip("/").split("/")
        if parts and parts[0] in LANG_PATHS:
            lang, rest = parts[0], "/".join(parts[1:])
            handler = ROOT / "functions" / lang / "[[path]].js"
            if not handler.exists():
                err("sitemap.xml lists %s, but %s does not exist, so that "
                    "path falls through to the catch-all and answers with the "
                    "whole calendar." % (loc, handler.relative_to(ROOT)))
                continue
            served = "index.html" if not rest else rest + ".html"
            if not (ROOT / served).exists():
                err("sitemap.xml lists %s, but the page it would serve (%s) "
                    "does not exist." % (loc, served))
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


def check_bible_langs():
    """The list of languages that have a New Testament, against the files.

    Both the calendar and the Library build the bundle's name from the
    language, and three of the twenty-one have no bundle. Pages answers a path
    that does not exist with the whole of the calendar and a 200, so asking
    for one cost the reader 6.8 MB on every reading he opened - and the
    Library's loader tested only r.ok, so it would have handed that HTML to
    the inflater. Both now carry a list. A list is only worth having if it
    cannot go quietly stale, which is what this is for."""
    have = {p.name.split(".")[2]
            for p in (ROOT / "data").glob("bible.v4.*.b64")}
    for name in ("index.html", "library.html"):
        s = (ROOT / name).read_text(encoding="utf-8")
        m = re.search(r"var BIBLE_LANGS=\{([^}]*)\}", s)
        if not m:
            err("%s has no BIBLE_LANGS: it will ask for bundles that do not "
                "exist" % name)
            continue
        listed = set(re.findall(r"([a-z]{2,3}):1", m.group(1)))
        if listed != have:
            err("%s BIBLE_LANGS disagrees with the files: %s"
                % (name, " ".join(sorted(listed ^ have))))
    print("New Testament in %d languages, and both pages ask only for those"
          % len(have))
    check_bible_whole(have)


def check_book_names():
    """Every language names every book, and the index the page asks for is
    the index the tools write.

    The buttons that carry a reader from one book to the next are labelled in
    the language the site is set to, which only works if that language has a
    name for the book. Church Slavonic, Japanese and Serbian had every Old
    Testament book named in English over text that is not English, and no
    check asked. Sixteen deuterocanonical books were named in five languages
    and no others."""
    base = ROOT / "scripture" / "index.json"
    live = ROOT / "scripture" / "index.v2.json"
    if not live.exists():
        err("scripture/index.v2.json is missing: the Library asks for it")
        return
    if base.read_text(encoding="utf-8") != live.read_text(encoding="utf-8"):
        err("scripture/index.json and index.v2.json disagree - run "
            "the scripture index sync")
        return
    idx = json.loads(base.read_text(encoding="utf-8"))
    carried = set()
    for v in idx["avail"].values():
        carried |= set(v)
    idxhtml = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r"const LANG_NAMES=\{(.*?)\};", idxhtml, re.S)
    langs = set(re.findall(r"([a-z]{2,3}):\"", m.group(1))) | {"cu"}
    short = []
    for l in sorted(langs):
        miss = [n for n in sorted(carried) if str(n) not in idx["names"].get(l, {})]
        if miss:
            short.append("%s (%d)" % (l, len(miss)))
    if short:
        err("a language cannot name the books it is shown: %s"
            % ", ".join(short))
    else:
        print("all %d books named in every one of the %d languages offered"
              % (len(carried), len(langs)))
    lib = (ROOT / "library.html").read_text(encoding="utf-8")
    i = lib.index("NT_BOOK_NAMES")
    j = lib.index("=", i)
    k = lib.index("\n", j)
    nt = json.loads(lib[j + 1:k].rstrip(";"))
    nomiss = sorted(l for l in langs if l != "en" and l not in nt)
    if nomiss:
        warn("no New Testament book names for: %s" % ", ".join(nomiss))


def check_bible_whole(langs):
    """Every bundle carries the whole New Testament.

    For a long time none of them did. Eighteen of nineteen languages held only
    the verses the lectionary reads: the Apocalypse in Russian was its seventh
    chapter and no other, Luke stood at 486 verses of 1,151, and Philemon was
    in no language but English. Nothing failed, because nothing asked. The
    book list looked complete because every book was named, and every book was
    a quarter of itself. This asks."""
    import base64
    import zlib
    short = []
    for lang in sorted(langs):
        p = ROOT / "data" / ("bible.v4.%s.b64" % lang)
        d = json.loads(zlib.decompress(
            base64.b64decode(p.read_text())))[lang]
        books = [b for b in d if b != "__metadata__"]
        verses = sum(len(c) for b in books for c in d[b].values())
        if len(books) != 27 or verses < 7800:
            short.append("%s (%d books, %d verses)"
                         % (lang, len(books), verses))
    if short:
        err("a New Testament here is not the whole New Testament: %s"
            % "; ".join(short))
    else:
        print("every New Testament carries 27 books and the whole text")


# A Church's own commemoration must not repeat one the base calendar already
# carries. Six did, and the reason none of them was caught by eye is that the
# base spells them differently: Gerasimus of Cephalonia against Gerasimos of
# Kephalonia, John-Vladimir against Jovan Vladimir. So the comparison is on
# the shape of the name rather than the letters - vowels dropped, the endings
# that differ between transliterations folded, and the words every entry has
# in common ignored.
LOCAL_STOP = set((
    "saint st ss the of and his her their new venerable holy martyr martyrs "
    "hieromartyr great greatmartyr blessed righteous repose synaxis "
    "translation relics bishop king queen prince archbishop metropolitan "
    "patriarch catholicos confessor abbot elder fool christ wonderworker "
    "equal apostles all first second brothers brother sister mother children "
    "hierarch voivode uncovering apostle prophet icon afterfeast forefeast "
    "with those them who").split())


def _fold(word):
    """A transliteration-insensitive skeleton of a proper name."""
    import unicodedata
    w = unicodedata.normalize("NFD", word)
    w = "".join(c for c in w if not unicodedata.combining(c)).lower()
    w = w.replace("kh", "h").replace("ph", "f").replace("th", "t")
    w = w.replace("k", "c").replace("j", "i").replace("y", "i").replace("w", "v")
    w = re.sub(r"[^a-z]", "", w)
    skel = re.sub(r"[aeiou]+", "", w)
    # Isaac is two consonants and would vanish, taking the difference between
    # Isaac the Syrian and Ephraim the Syrian with it. Where the consonants
    # are too few to tell names apart, keep the word.
    return skel if len(skel) >= 3 else w


def _skeleton(name):
    words = re.split(r"[^A-Za-z\u00c0-\u024f]+", name)
    out = set()
    for w in words:
        if len(w) < 4 or w.lower() in LOCAL_STOP:
            continue
        f = _fold(w)
        if len(f) >= 3:
            out.add(f)
    return out


def check_local_saints():
    src = (ROOT / "index.html").read_text(encoding="utf-8")

    def table(name):
        # SYNAXARION runs over many lines, so the literal is taken by
        # balancing braces rather than by reading to the end of the line
        h = "const %s=" % name
        k = src.index(h) + len(h)
        while src[k] not in "{[":
            k += 1
        a, depth, instr, quote, esc = k, 0, False, "", False
        while k < len(src):
            c = src[k]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == quote:
                    instr = False
            elif c in "\"'":
                instr, quote = True, c
            elif c in "{[":
                depth += 1
            elif c in "}]":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        raw = src[a:k + 1]
        # the tables are JS, and some carry bare keys
        raw = re.sub(r'([{,])([A-Za-z_][A-Za-z0-9_]*):', r'\1"\2":', raw)
        return json.loads(raw)

    try:
        syn = table("SYNAXARION")
        local = table("LOCAL_FIXED")
    except Exception as e:
        err("index.html: the calendar tables would not parse (%s)" % e)
        return

    base = {}
    for k, entries in syn.items():
        base[k] = [(e["n"], _skeleton(e["n"])) for e in entries]

    # Two findings, and the difference matters. An ERROR is a local entry
    # every distinctive word of which is inside a base entry for the same day:
    # that is the same saint written twice. A REVIEW is an overlap - a shared
    # given name, a shared place - which two different saints on one day may
    # perfectly well have, and which a script cannot judge.
    bad = review = total = 0
    for juris, entries in sorted(local.items()):
        for e in entries:
            total += 1
            if e.get("base"):
                continue          # this one deliberately renames a base entry
            k = "%02d-%02d" % (e["mo"], e["da"])
            mine = _skeleton(e["name"])
            if not mine:
                continue
            for bn, bs in base.get(k, []):
                if not (mine & bs):
                    continue
                if mine <= bs:
                    bad += 1
                    err("%s keeps %r on %s, which the base already carries as "
                        "%r" % (juris, e["name"], k, bn))
                else:
                    review += 1
                    print("  review: %s %s %r beside the base's %r"
                          % (juris, k, e["name"], bn))
    print("%d local commemorations, %d repeating the base, %d to look at"
          % (total, bad, review))



def check_library_lazy():
    """A work the page will not send but cannot fetch opens empty.

    The twenty-four works whose text used to sit inside library.html are
    marked lazy there and read from data/library/<id>.json, the same path the
    catalogue's works use. A missing one is answered by the catch-all with the
    whole of index.html and a 200, and held for an hour.
    """
    src = (ROOT / "library.html").read_text(encoding="utf-8")
    head = "const CORPUS = "
    i = src.index(head)
    j = src.index("\n", i)
    try:
        corpus = json.loads(src[i + len(head):j].rstrip().rstrip(";"))
    except Exception as e:
        err("library.html: CORPUS would not parse (%s)" % e)
        return
    lazy = [w["work_id"] for w in corpus["works"] if w.get("lazy")]
    missing = [w for w in lazy
               if not (ROOT / "data" / "library" / (w + ".json")).exists()]
    for w in missing:
        err("library.html marks %s lazy but data/library/%s.json is not there"
            % (w, w))
    inline = len(corpus.get("units") or [])
    if not missing:
        print("%d works read from files, %d units still inside the page"
              % (len(lazy), inline))



def check_saint_info_en():
    """The English day-panel entries are a file, and must stay one.

    They were 811 KB inside index.html, a quarter of the page, long after the
    other twenty-one languages had moved out. English is also the base every
    other language falls back to, so the file is asked for on every visit
    whatever the reader's language: if it is not there, Cloudflare answers
    with the whole of the calendar and a 200 and nothing looks broken."""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    i = src.index("const SAINT_INFO=")
    j = src.index("\n", i)
    raw = src[i + len("const SAINT_INFO="):j].rstrip().rstrip(";")
    try:
        info = json.loads(raw)
    except Exception:
        return
    if info:
        err("%d day-panel entries are back inside index.html. They belong in "
            "data/saint-info.v1.en.json." % len(info))
    f = ROOT / "data" / "saint-info.v1.en.json"
    if not f.exists():
        err("data/saint-info.v1.en.json is not there, and every reader asks "
            "for it whatever his language.")
    # The file existing is not the same as the page asking for it. The loader
    # returns early for any language not in SAINT_INFO_LANGS, and English was
    # not in it: the file shipped, nothing fetched it, and every English
    # reader saw a day panel with no saint's life in it. Nothing failed.
    m = re.search(r"SAINT_INFO_LANGS=\{([^}]*)\}", src)
    if not m:
        err("SAINT_INFO_LANGS is not in index.html; nothing gates the loader")
    elif not re.search(r"\ben\s*:", m.group(1)):
        err("SAINT_INFO_LANGS does not name en, so loadSaintInfo returns "
            "before fetching it and the English day panel carries no lives.")
    elif not info:
        n = len(json.loads(f.read_text(encoding="utf-8")))
        print("%d day-panel entries, read from a file in every language" % n)



def check_header_rules():
    """Every versioned family under /data must be named in _headers.

    This has now happened twice. The New Testament was bumped from v1 to v2
    and the rule was not, so for months the bundles matched nothing, fell
    through to the default and were answered uncached - half a megabyte again
    on every visit, and nothing failed. The prayers were bumped from v1 to v2
    and the same thing happened to 364 KB in twenty-one languages, and was
    found only by looking. A filename carries the version; the rule has to
    move with it, and a frozen stem stays where it is."""
    hdr = (ROOT / "_headers").read_text(encoding="utf-8")
    rules = set(re.findall(r"^/data/([^\s]+)", hdr, re.M))
    stems = {}
    for f in (ROOT / "data").iterdir():
        m = re.match(r"(.+?\.v\d+)\.", f.name)
        if m:
            stems.setdefault(m.group(1), 0)
            stems[m.group(1)] += 1
    missing = [(k, v) for k, v in sorted(stems.items())
               if not any(r.startswith(k + ".") for r in rules)]
    for stem, n in missing:
        err("data/%s.* is %d file(s) with no rule in _headers. It falls "
            "through to the default and is answered uncached." % (stem, n))
    if not missing:
        print("%d versioned families under /data, every one named in _headers"
              % len(stems))



def check_lectionary():
    """Every reading the calendar prints must be a passage the site can show.

    Forty-four of the hundred and seventy references were dead and nothing
    said so: the Western rite's Old Testament sat in index.html, loadBibleEn
    replaced the object rather than merging into it, and the books were gone
    the moment the file landed. vlink asks pericope whether a passage is there
    before it makes a link, so those readings were not even underlined."""
    import subprocess
    try:
        out = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "check_lectionary.py")],
            capture_output=True, text=True, timeout=120)
    except Exception as e:
        warn("the lectionary check would not run (%s)" % e)
        return
    for line in out.stdout.strip().splitlines():
        line = line.strip()
        if line.startswith("ERROR:"):
            err("lectionary: %s" % line[6:].strip())
        elif line.startswith("review:"):
            print("  %s" % line)
        elif line:
            print(line)



def check_movable_days_are_movable():
    """Lent must not be pinned to the dates it fell on in one year.

    Eight movable Lenten commemorations were sitting in the fixed synaxarion
    on their 2024 civil dates, so every seventh of April the calendar
    announced the Sunday of the Veneration of the Cross - in every
    jurisdiction and every language, whatever day of the week it was.

    And a saint of the twentieth century is kept on the day he reposed by the
    civil clock, which is the same day for every Church; the synaxarion is a
    table of menaion dates and shifted him thirteen days for a Church on the
    old calendar."""
    import subprocess
    for tool, what in (("lenten_strays.py", "Lent"),
                       ("civil_commemorations.py",
                        "the saints kept on the civil date")):
        try:
            out = subprocess.run(
                [sys.executable, str(ROOT / "tools" / tool), "--check"],
                capture_output=True, text=True, timeout=120)
        except Exception as e:
            warn("%s could not be checked (%s)" % (what, e))
            continue
        line = (out.stdout or out.stderr).strip().splitlines()
        line = line[0] if line else "(no output)"
        if out.returncode != 0:
            err("%s: %s  Run tools/%s --write." % (what, line, tool))
        else:
            print(line)


def check_local_names():
    """The Churches' own saints, in the reader's language.

    A hundred and twenty-seven commemorations belong to one Church and not
    the rest. They were carried in in English, so a reader who chose his own
    Church met the whole calendar in his language and his own Church's saints
    in English. This reports how far that has been put right; it does not
    fail, because a name with no rendering keeps the English, which is where
    it stood before."""
    import subprocess
    try:
        out = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_local_names.py"),
             "--check"], capture_output=True, text=True, timeout=120)
    except Exception as e:
        warn("the Churches' own commemorations could not be counted (%s)" % e)
        return
    lines = [l for l in (out.stdout or "").splitlines() if l.strip()]
    done = [l.split()[1] for l in lines
            if l.startswith("  ") and len(l.split()) > 1]
    started = [l.split()[1] for l in lines
               if l.startswith("! ") and "not begun" not in l]
    total = len(done) + len(started) + sum(
        1 for l in lines if "not begun" in l)
    if not total:
        return
    if done:
        print("the Churches' own commemorations are named in %d of %d "
              "languages: %s" % (len(done), total, " ".join(done)))
    else:
        print("the Churches' own commemorations: %d of %d languages begun"
              % (len(started), total))
    if len(done) < total:
        warn("the Churches' own saints are still English for %d language(s); "
             "run tools/build_local_names.py --check" % (total - len(done)))


def check_calendar_engine():
    """The copied engine must still be the calendar's own.

    tools/build_calendar_engine.py copies the reckoning out of index.html so
    an embeddable panel and a JSON endpoint can run it. Nothing in the copy is
    edited, and this regenerates it and compares, so a change to the calendar
    that is not carried across fails here rather than being discovered by a
    reader whose parish site shows last month's fast."""
    import subprocess
    try:
        out = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_calendar_engine.py"),
             "--check"], capture_output=True, text=True, timeout=180)
    except Exception as e:
        warn("the calendar engine check would not run (%s)" % e)
        return
    line = (out.stdout or out.stderr).strip().splitlines()
    line = line[-1] if line else "(no output)"
    if out.returncode != 0:
        err("the calendar engine or its data no longer matches index.html. "
            "Run tools/build_calendar_engine.py --write. (%s)" % line)
    else:
        print(line)

    # The endpoint names the engine and the tables in its own source, one
    # level away from the builder that writes them. That is the shape of
    # every cache bug on this site: the reference nobody thought to follow.
    src = (ROOT / "tools" / "build_calendar_engine.py").read_text(encoding="utf-8")
    api = ROOT / "functions" / "api" / "day.js"
    if not api.exists():
        err("functions/api/day.js is missing; the endpoint has no handler")
        return
    day = api.read_text(encoding="utf-8")
    for what, pat in (("engine", r'"(plithos-calendar\.v\d+\.js)"'),
                      ("tables", r'"(calendar-tables\.v\d+\.json)"')):
        m = re.search(pat, src)
        if not m:
            warn("could not read the %s filename out of the builder" % what)
            continue
        name = m.group(1)
        if name not in day:
            err("functions/api/day.js does not ask for %s, which is the %s "
                "the builder writes. The endpoint is reading a stale copy."
                % (name, what))
        if not (ROOT / ("assets" if what == "engine" else "data") / name).exists():
            err("%s does not exist, though the endpoint asks for it" % name)



def check_guide_i18n():
    """The Guide's prose, in the languages it is read in.

    The fasting section was added in English on 24 August and the terms have
    been in seven languages for months. This reports how far the rest has got
    and fails on a translation that is the wrong shape - a dropped section, an
    invented one, a positional terms array of the wrong length, or a language
    written in its own alphabet that has come back pure ASCII."""
    import subprocess
    try:
        out = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build_guide_i18n.py"),
             "--check"], capture_output=True, text=True, timeout=120)
    except Exception as e:
        warn("the guide translation check would not run (%s)" % e)
        return
    for line in (out.stdout or "").strip().splitlines():
        t = line.strip()
        if t.startswith("PROBLEM"):
            err("guide: %s" % t[7:].strip())
        elif t:
            print(t if not line.startswith("  ") else "  " + t)



def main():
    check_pages()
    check_bible_langs()
    check_book_names()
    check_rule_i18n()
    check_build()
    check_library()
    check_library_dates()
    check_library_lazy()
    check_decoding()
    check_scripture()
    check_prayers()
    check_bible_bundles()
    check_search_index()
    check_index_version()
    check_saint_terms_version()
    check_saint_lives_version()
    check_saint_info_en()
    check_voice()
    check_quotations()
    check_redirects()
    check_headers()
    check_header_rules()
    check_lectionary()
    check_movable_days_are_movable()
    check_local_names()
    check_calendar_engine()
    check_guide_i18n()
    check_sitemap()
    check_ui_coverage()
    check_local_saints()

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
