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


def check_search_index():
    p = ROOT / "data" / "search-index.v1.json"
    if not p.exists():
        err("data/search-index.v1.json is missing; the command palette will "
            "open empty on every page")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        err("data/search-index.v1.json is not valid JSON: %s" % e)
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


def check_pages():
    for name in ["index.html", "plithos_saints.html", "plithos_reader.html",
                 "contact.html"]:
        p = ROOT / name
        if not p.exists():
            err("%s is missing" % name)
            continue
        s = p.read_text(encoding="utf-8")
        if "assets/plithos-ui.css" not in s:
            err("%s does not load assets/plithos-ui.css" % name)
        if "assets/plithos-ui.js" not in s:
            err("%s does not load assets/plithos-ui.js" % name)
        if 'charset="utf-8"' not in s.lower():
            err("%s does not declare <meta charset=\"utf-8\">" % name)
        if 'href="contact.html"' not in s:
            warn("%s has no link to the contact page" % name)
    for name in ["assets/plithos-ui.css", "assets/plithos-ui.js",
                 "robots.txt", "sitemap.xml", "_headers", "_redirects"]:
        if not (ROOT / name).exists():
            err("%s is missing" % name)


def check_headers():
    """/data/*.json once matched both /data/* and /*.json, and Cloudflare
    concatenated the two Cache-Control values into one malformed header."""
    s = (ROOT / "_headers").read_text(encoding="utf-8")
    rules = re.findall(r"^(/\S+)$", s, re.M)
    if "/*.json" in rules and any(r.startswith("/data/") for r in rules):
        err("_headers has both /*.json and a /data/ rule; they will both "
            "match /data/*.json and Cloudflare will emit two Cache-Control "
            "values in one header")


def main():
    check_pages()
    check_library()
    check_scripture()
    check_bible_bundles()
    check_search_index()
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
