"""Carry each New Testament here whole.

    python3 tools/ingest_nt.py --verify ru
    python3 tools/ingest_nt.py --build ru --write

Every edition already published on the site is fetched again from the source
that holds it complete, and --verify compares what comes back against the
verses the site already had. A translation that disagrees with itself is the
wrong translation, and the check says so before anything is written.
"""

import argparse, base64, json, os, re, sys, time, unicodedata, urllib.request, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, ".cache", "nt")
sys.path.insert(0, HERE)
from nt_sources import SOURCES, NT_ORDER, RO_NT

UA = {"User-Agent": "plithos.org scripture ingest"}


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
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, key + ".json")
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    raw = get(url)
    if raw is None:
        return None
    d = json.loads(raw.decode("utf-8"))
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return d


def getbible_book(key, nr):
    return cached("%s.%d" % (key, nr),
                  "https://api.getbible.net/v2/%s/%d.json" % (key, nr))


def helloao_book(key, code):
    """One book from eBible, chapter by chapter."""
    chaps = {}
    n = 1
    while True:
        d = cached("%s.%s.%d" % (key, code, n),
                   "https://bible.helloao.org/api/%s/%s/%d.json" % (key, code, n))
        if d is None:
            break
        vs = {}
        for item in d.get("chapter", {}).get("content", []):
            if item.get("type") != "verse":
                continue
            parts = [x for x in item.get("content", []) if isinstance(x, str)]
            for x in item.get("content", []):
                if isinstance(x, dict) and isinstance(x.get("text"), str):
                    parts.append(x["text"])
            t = clean(" ".join(parts))
            if t:
                vs[str(item["number"])] = t
        if not vs:
            break
        chaps[str(n)] = vs
        n += 1
    return chaps


def wikisource_ro_book(name):
    """One book of the Synod's 1914 New Testament.

    The Old Testament of this edition is already read by
    tools/ingest_scripture_ro.py, and the New is set on the same pages in the
    same way, so it is read by the same code and numbered as the edition
    numbers it.
    """
    import ingest_scripture_ro as ro
    chapters, err = ro.book(RO_NT[name])
    if err:
        return {}
    out = {}
    for i, verses in enumerate(chapters, 1):
        vs = {str(j): t for j, t in enumerate(verses, 1) if t}
        if vs:
            out[str(i)] = vs
    return out


def clean(t):
    t = t.replace(" ", " ")
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    return t


def fetch(lang):
    """The whole New Testament, {book: {chapter: {verse: text}}}."""
    backend, key = SOURCES[lang][0], SOURCES[lang][1]
    if backend == "published":
        return existing(lang) or {}
    out = {}
    missing = []
    for name, nr, code in NT_ORDER:
        if backend == "getbible":
            d = getbible_book(key, nr)
            chaps = {}
            if d is not None:
                for c in d.get("chapters", []):
                    vs = {}
                    for v in c.get("verses", []):
                        t = clean(v.get("text", ""))
                        if t:
                            vs[str(v["verse"])] = t
                    if vs:
                        chaps[str(c["chapter"])] = vs
        elif backend == "helloao":
            chaps = helloao_book(key, code)
        elif backend == "wikisource-ro":
            chaps = wikisource_ro_book(name)
        else:
            raise SystemExit("unknown backend %s" % backend)
        if chaps:
            out[name] = chaps
        else:
            missing.append(name)
    if missing:
        print("      %s: the source does not carry %s"
              % (lang, ", ".join(missing)))
    return out


def existing(lang, ver="v2"):
    p = os.path.join(ROOT, "data", "bible.%s.%s.b64" % (ver, lang))
    if not os.path.exists(p):
        return None
    d = json.loads(zlib.decompress(base64.b64decode(open(p).read())))[lang]
    return {k: v for k, v in d.items() if k != "__metadata__"}


def norm(t):
    """Down to the letters alone.

    The published copy fuses words where a space was lost ("Naassonbegat"),
    and editions differ over ae-ligatures and the shape of a dash. None of
    that tells you whether it is the same translation, so none of it is kept.
    """
    t = unicodedata.normalize("NFKD", t)
    t = t.replace(u"\u00e6", "ae").replace(u"\u00c6", "AE")
    t = "".join(c for c in t if c.isalnum())
    return t.lower()


def verify(lang):
    """Is the source holding the same translation the site already published?

    Not verse by verse: the published copy is misnumbered in places, so a
    comparison keyed on the number reports a disagreement where the text is
    word for word the same. The question is only whether the translation is
    the same one, so each published verse is looked for anywhere in its own
    book.
    """
    old = existing(lang)
    if old is None:
        print("%s: nothing published yet, nothing to compare" % lang)
        return True
    new = fetch(lang)
    found = absent = 0
    examples = []
    for b in old:
        pool = set()
        for c in new.get(b, {}).values():
            for t in c.values():
                pool.add(norm(t))
        for c in old[b]:
            for v, t in old[b][c].items():
                if norm(t) in pool:
                    found += 1
                else:
                    absent += 1
                    if len(examples) < 3:
                        examples.append((b, c, v, t))
    total = found + absent
    ov = sum(len(ch) for bk in old.values() for ch in bk.values())
    nv = sum(len(ch) for bk in new.values() for ch in bk.values())
    rate = 100.0 * found / total if total else 0
    print("%-4s published %5d verses, source has %5d - %5d of them found "
          "in the source, %d not (%.1f%%)" % (lang, ov, nv, found, absent, rate))
    for b, c, v, t in examples:
        print("      not in source: %s %s:%s  %s" % (b, c, v, t[:70]))
    return rate > 95.0


def build(lang, write):
    src = SOURCES[lang]
    nt = fetch(lang)
    nt["__metadata__"] = {
        "edition": src[2],
        "license": src[3],
        "dir": src[4],
    }
    books = [b for b in nt if b != "__metadata__"]
    nv = sum(len(c) for b in books for c in nt[b].values())
    print("%s: %d books, %d chapters, %d verses"
          % (lang, len(books),
             sum(len(nt[b]) for b in books), nv))
    if len(books) != 27:
        print("  WARNING: %d books, expected 27" % len(books))
    if not write:
        return
    raw = json.dumps({lang: nt}, ensure_ascii=False, separators=(",", ":"))
    blob = base64.b64encode(zlib.compress(raw.encode("utf-8"), 9)).decode()
    p = os.path.join(ROOT, "data", "bible.v3.%s.b64" % lang)
    open(p, "w").write(blob)
    print("  wrote %s (%.1f MB)" % (p, len(blob) / 1e6))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("langs", nargs="*")
    a = ap.parse_args()
    langs = a.langs or sorted(SOURCES)
    bad = []
    for l in langs:
        if a.verify:
            if not verify(l):
                bad.append(l)
        if a.build:
            build(l, a.write)
    if bad:
        print("\nEDITION MISMATCH: %s" % ", ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
