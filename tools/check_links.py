#!/usr/bin/env python3
"""Every link the directory publishes, read rather than pinged.

Domains a Church still prints keep turning up in strangers' hands - a
video-game weblog, a gambling site, a physiotherapist, casino ads, an
advertising redirect, a shop selling warning stickers - and every one of them
answered HTTP 200. Another still serves its eparchy's own menu under "Hacked
by Antonkill". So a status code is not a test and never was, and a check that
only looked at one would have passed all of them.

Nor is one reading always enough. The domain the Moscow Patriarchate prints
for the Yekaterinburg see gave one reader the diocese over https and the shop
over http, and gave two later readers the shop at both doors. That row now
publishes no link, because a link that answers differently to different
people is worse than no link at all: whoever gets the shop was sent there by
this site.

What this does instead is fetch each link and ask whether the page still
looks like the body the row says it is: whether any word of the body's name,
or of the name it gives itself in its own language, or of its seat, appears
in what came back. A page that answers and carries none of them is reported
to be looked at by a person. It is not proof of seizure - a site can be
rebuilt, a diocese renamed, a page put behind a script - which is why this
reports and does not edit.

    python3 tools/check_links.py                  every row
    python3 tools/check_links.py --church russia  one Church and what is under it
    python3 tools/check_links.py --json out.json  keep the answers

Rows whose link is not their own are skipped: they point at a Church that
this will check once on its own row rather than nine hundred times.
"""
import argparse
import json
import re
import ssl
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from html import unescape as html_unescape
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "directory.v1.json"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
      " Chrome/120.0 Safari/537.36")

# A word shorter than this proves nothing: "of", "and", "St" turn up on any
# page in any language, and a page of casino advertising would pass on them.
SHORTEST = 4

# Words that name no body. They are the furniture of every ecclesiastical
# title and would match a stranger's page as readily as the right one.
SKIP = set("""orthodox holy church churches diocese dioceses eparchy eparchia
metropolis metropolitan archdiocese archbishopric bishopric exarchate
patriarchate patriarchal district vicariate mission monastery stavropegion
saint sain and the of for its""".split())


def words(text):
    out, cur = [], []
    for ch in text or "":
        if unicodedata.category(ch)[0] in ("L", "M", "N"):
            cur.append(ch)
        elif cur:
            out.append("".join(cur))
            cur = []
    if cur:
        out.append("".join(cur))
    return out


def marks(row):
    """The words that would show this page belongs to this body."""
    got = set()
    for field in ("name", "local", "styled", "seat"):
        for w in words(row.get(field) or ""):
            w = w.lower()
            if len(w) >= SHORTEST and w not in SKIP and not w.isdigit():
                got.add(w)
    return got


def ascii_url(url):
    """A Russian diocese answers at a Russian address.

    Nine sees publish a domain in Cyrillic - gubeparh.rf is written
    губепарх.рф - and urllib will not put a non-ASCII host in a request line.
    Encoding the host to punycode is what a browser does silently, and
    without it the checker reported nine live dioceses as unreachable, which
    is the checker failing and saying the Church failed."""
    m = re.match(r"^(https?://)([^/]+)(.*)$", url or "", re.S)
    if not m:
        return url
    scheme, host, rest = m.groups()
    try:
        host.encode("ascii")
    except UnicodeEncodeError:
        userinfo, at, hostport = host.rpartition("@")
        hostname, colon, port = hostport.partition(":")
        hostname = hostname.encode("idna").decode("ascii")
        host = userinfo + at + hostname + colon + port
    return scheme + host + urllib.parse.quote(rest, safe="/?&=#%+,;:@!$'()*~")


def unescape(text):
    """What the markup carries, not only what it renders.

    The Georgian Patriarchate's whole site ships as JSON inside one attribute
    with every Georgian letter written as a backslash-u escape, so a search
    of the raw bytes for a Georgian word finds nothing and the page reads as
    empty. Undoing
    the two escapings that hide real text - JSON's and HTML's - is the
    difference between reading a site and giving up on it."""
    def one(m):
        try:
            return chr(int(m.group(1), 16))
        except ValueError:
            return m.group(0)
    text = re.sub(r"\\u([0-9a-fA-F]{4})", one, text)
    return html_unescape(text)


SCRIPTS = ("LATIN GREEK CYRILLIC GEORGIAN ARMENIAN ARABIC HEBREW SYRIAC"
           " DEVANAGARI BENGALI CJK HIRAGANA KATAKANA HANGUL").split()


def script(ch):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    for s in SCRIPTS:
        if name.startswith(s):
            return s
    return None


def written_in(text):
    """The alphabet a page is actually written in.

    Not every alphabet on it. A Greek metropolis's site is full of Latin -
    its own web address, the word email, the name of whoever built it - so
    asking whether Latin appears at all answers yes for every page on earth
    and told the checker it could read thirteen Greek sites it could not.
    What matters is the one the page is mostly in."""
    seen = {}
    for ch in text:
        s = script(ch)
        if s:
            seen[s] = seen.get(s, 0) + 1
    if not seen:
        return None
    return max(seen.items(), key=lambda kv: kv[1])[0]


def fetch(url, timeout=25):
    url = ascii_url(url)
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en,*;q=0.5",
    })
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        raw = r.read(600000)
        enc = "utf-8"
        ct = (r.headers.get("content-type") or "").lower()
        m = re.search(r"charset=([\w-]+)", ct)
        if m:
            enc = m.group(1)
        return r.getcode(), r.geturl(), raw.decode(enc, "replace"), ct


def visible(html):
    html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?s)<!--.*?-->", " ", html)
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text)


def look(row):
    url = row.get("site")
    try:
        code, final, body, ct = fetch(url)
    except urllib.error.HTTPError as e:
        # A door held shut against a script says nothing about who is behind
        # it. Four Churches looked refused this week and every one answered by
        # another route, so these are reported apart from the rows that
        # answered and did not name themselves.
        kind = "refused" if e.code in (401, 403, 405, 406, 429, 451, 503) \
            else "http"
        return dict(id=row["id"], url=url, verdict=kind, detail=str(e.code))
    except Exception as e:
        return dict(id=row["id"], url=url, verdict="unreachable",
                    detail=type(e).__name__)
    out = dict(id=row["id"], url=url, code=code)
    if final.rstrip("/") != url.rstrip("/"):
        out["moved"] = final
    if "html" not in ct and "xml" not in ct:
        out["verdict"] = "not a page"
        out["detail"] = ct or "no content type"
        return out
    text = visible(body).lower()
    want = marks(row)
    # The whole markup, not only what a reader sees: a title, a meta
    # description or a link in a menu names the body just as well, and the
    # Georgian Patriarchate's entire site lives inside one attribute.
    whole = unescape(body).lower()
    hit = sorted(w for w in want if w in text)
    faint = sorted(w for w in want if w not in text and w in whole)
    out["found"] = hit
    if hit:
        out["verdict"] = "named"
    elif faint:
        out["verdict"] = "named in markup"
        out["found"] = faint
    elif not want:
        out["verdict"] = "nothing to look for"
    elif len(text) < 400:
        # A page whose text is written by a script has none to read here.
        # That is a thing this cannot see, not a thing that is wrong.
        out["verdict"] = "no text"
        out["detail"] = "%d characters of text" % len(text)
    else:
        # A Greek metropolis writes its site in Greek, and a row that holds
        # only an English name has nothing this could find there. That is a
        # gap in what the row records, not a dead link, and calling it a dead
        # link put eighteen live Greek and Romanian sees on a list of
        # suspects. Where no alphabet the row can spell is on the page, the
        # honest answer is that this cannot check it - and the remedy is the
        # body's own name in its own language, which the row should carry
        # anyway.
        mine = set()
        for w in want:
            for ch in w:
                s = script(ch)
                if s:
                    mine.add(s)
                    break
        theirs = written_in(text)
        if mine and theirs and theirs not in mine:
            out["verdict"] = "cannot check"
            out["detail"] = ("row is written in %s, the page in %s%s"
                             % ("/".join(sorted(mine)).lower(),
                                theirs.lower(),
                                "" if row.get("local")
                                else "; the row has no name in its own language"))
        else:
            out["verdict"] = "not named"
            out["detail"] = "%d characters, none of %d marks" % (len(text),
                                                                 len(want))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--church", help="one Church id and everything under it")
    ap.add_argument("--json", help="write every answer here")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    rows = json.loads(DATA.read_text(encoding="utf-8"))["rows"]
    if a.church:
        keep, by = set(), dict((r["id"], r.get("parent") or r.get("within"))
                               for r in rows)

        def under(i):
            seen = set()
            while i:
                if i == a.church:
                    return True
                if i in seen:
                    return False
                seen.add(i)
                i = by.get(i)
            return False
        rows = [r for r in rows if r["id"] == a.church or under(r["id"])]
    # A row whose link is somebody else's is that body's to answer for.
    todo = [r for r in rows if r.get("site") and not r.get("site_of")]
    print("%d rows, %d with a door of their own" % (len(rows), len(todo)),
          file=sys.stderr)

    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        got = list(pool.map(look, todo))

    # Worst first, and the two at the end are not faults: a door held shut
    # against a script, and a page a script writes, are both things this
    # cannot see rather than things that are wrong.
    order = ["not named", "not a page", "unreachable", "http",
             "nothing to look for", "cannot check", "no text", "refused",
             "named in markup", "named"]
    got.sort(key=lambda r: (order.index(r["verdict"]), r["id"]))
    name = dict((r["id"], r["name"]) for r in rows)
    bad, blind = 0, 0
    for r in got:
        if r["verdict"] in ("named", "named in markup"):
            continue
        if r["verdict"] in ("refused", "no text", "cannot check"):
            blind += 1
        else:
            bad += 1
        print("%-14s %-34s %s" % (r["verdict"], r["id"], r["url"]))
        if r.get("detail"):
            print("%-14s   %s" % ("", r["detail"]))
        if r.get("moved"):
            print("%-14s   now at %s" % ("", r["moved"]))
        print("%-14s   %s" % ("", name.get(r["id"], "")))
    if a.json:
        Path(a.json).write_text(json.dumps(got, ensure_ascii=False, indent=1),
                                encoding="utf-8")
        print("wrote " + a.json, file=sys.stderr)
    ok = len(got) - bad - blind
    print("\n%d of %d links still name the body they belong to;"
          " %d to look at, %d this cannot see"
          % (ok, len(got), bad, blind))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
